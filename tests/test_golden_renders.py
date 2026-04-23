"""Phase 20b — golden-file regression tests.

Every canonical render has a baseline PNG under ``tests/golden/``. We
compute a **perceptual hash** (pHash from the imagehash library) on a
fresh render and compare against the baseline's hash. A small Hamming
distance threshold allows minor font / anti-aliasing drift (different
matplotlib versions, different system fonts) without tripping.

When a legitimate change in rendering lands, re-run
``python scripts/regen_goldens.py`` to overwrite the baselines.

The tests gracefully ``importorskip`` when ``imagehash`` / ``Pillow``
isn't installed — so the runtime environment stays lean and CI picks
these up only when ``requirements-dev.txt`` is installed.
"""
from __future__ import annotations
import os
from pathlib import Path

import pytest

pytest.importorskip("rdkit")
imagehash = pytest.importorskip("imagehash")
PIL = pytest.importorskip("PIL")
from PIL import Image  # noqa: E402


# Pin RDKit's 2D-coord generator before any golden-producing code
# runs. The goldens were baked with the default (non-CoordGen)
# depictor; if another test in the same process has flipped the
# global preference to CoordGen (e.g. via
# `orgchem.db.seed_coords`), pHashes drift beyond the tolerance.
# Applying this as an autouse fixture keeps the tests deterministic
# regardless of test-ordering.
from rdkit.Chem import rdDepictor as _rd  # noqa: E402


@pytest.fixture(autouse=True)
def _pin_coord_gen_off():
    try:
        _rd.SetPreferCoordGen(False)
    except Exception:  # noqa: BLE001
        pass
    yield


GOLDEN_DIR = Path(__file__).resolve().parent / "golden"
#: Max Hamming distance between two pHash values that's still "identical".
#: 0   — bit-for-bit identical hashes.
#: 1-3 — minor font / aa drift, typical.
#: >5  — meaningful content change; likely a regression.
TOLERANCE = 8


def _phash_of(path: Path):
    return imagehash.phash(Image.open(path))


def _check(key: str, produce):
    """Shared helper: re-render via `produce(tmp_path)`, compare phash."""
    baseline = GOLDEN_DIR / f"{key}.png"
    if not baseline.exists():
        pytest.skip(f"no baseline for {key} — run scripts/regen_goldens.py")
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d) / f"{key}.png"
        produce(tmp)
        if not tmp.exists() or tmp.stat().st_size < 500:
            pytest.fail(f"renderer produced no / tiny output for {key}")
        baseline_hash = _phash_of(baseline)
        fresh_hash = _phash_of(tmp)
        diff = baseline_hash - fresh_hash
        assert diff <= TOLERANCE, (
            f"golden {key!r} drift too large: hamming distance {diff} "
            f"(threshold {TOLERANCE}). If this change is intentional, "
            f"run `python scripts/regen_goldens.py` to refresh baselines."
        )


# ---- 2D molecule baselines ------------------------------------------

def _produce_mol2d(smiles: str):
    def produce(path: Path) -> None:
        from rdkit import Chem
        from rdkit.Chem.Draw import rdMolDraw2D
        mol = Chem.MolFromSmiles(smiles)
        d = rdMolDraw2D.MolDraw2DCairo(500, 400)
        d.drawOptions().bondLineWidth = 2
        d.DrawMolecule(mol)
        d.FinishDrawing()
        path.write_bytes(d.GetDrawingText())
    return produce


def test_golden_mol2d_benzene():
    _check("mol2d_benzene", _produce_mol2d("c1ccccc1"))


def test_golden_mol2d_aspirin():
    _check("mol2d_aspirin", _produce_mol2d("CC(=O)Oc1ccccc1C(=O)O"))


def test_golden_mol2d_caffeine():
    _check("mol2d_caffeine", _produce_mol2d("Cn1cnc2n(C)c(=O)n(C)c(=O)c12"))


def test_golden_mol2d_ibuprofen_R():
    _check("mol2d_ibuprofen_R",
           _produce_mol2d("CC(C)Cc1ccc(cc1)[C@@H](C)C(=O)O"))


# ---- Reaction scheme baselines --------------------------------------

def _produce_reaction(smarts: str):
    def produce(path: Path) -> None:
        from orgchem.render.draw_reaction import export_reaction
        export_reaction(smarts, path)
    return produce


def test_golden_reaction_diels_alder():
    _check("reaction_diels_alder", _produce_reaction("C=CC=C.C=C>>C1=CCCCC1"))


def test_golden_reaction_sn2():
    _check("reaction_sn2", _produce_reaction("CBr.[OH-]>>CO.[Br-]"))


# ---- Energy-profile baselines ---------------------------------------

def _produce_energy(reaction_name_substr: str):
    def produce(path: Path) -> None:
        os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
        from orgchem.agent.headless import HeadlessApp
        with HeadlessApp() as app:
            rows = app.call("list_energy_profiles")
            match = next(r for r in rows if reaction_name_substr in r["name"])
            app.call("export_energy_profile",
                     reaction_id=match["id"], path=str(path))
    return produce


def test_golden_energy_sn1():
    _check("energy_sn1", _produce_energy("SN1: tert-butyl"))


def test_golden_energy_diels_alder():
    _check("energy_diels_alder", _produce_energy("Diels-Alder"))


# ---- Hückel MO baselines --------------------------------------------

def _produce_mo(smiles: str):
    def produce(path: Path) -> None:
        from orgchem.core.huckel import huckel_for_smiles
        from orgchem.render.draw_mo import export_mo_diagram
        res = huckel_for_smiles(smiles)
        export_mo_diagram(res, path, title=f"MO — {smiles}")
    return produce


def test_golden_mo_benzene():
    _check("mo_benzene", _produce_mo("c1ccccc1"))


def test_golden_mo_butadiene():
    _check("mo_butadiene", _produce_mo("C=CC=C"))


# ---- IR-spectrum baselines ------------------------------------------

def _produce_ir(smiles: str):
    def produce(path: Path) -> None:
        from orgchem.render.draw_ir import export_ir_spectrum
        export_ir_spectrum(smiles, path, title=f"IR — {smiles}")
    return produce


def test_golden_ir_acetic_acid():
    _check("ir_acetic_acid", _produce_ir("CC(=O)O"))


def test_golden_ir_acetone():
    _check("ir_acetone", _produce_ir("CC(=O)C"))
