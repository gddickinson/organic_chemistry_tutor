"""Regenerate golden-file baselines for Phase 20b regression tests.

Run this when a legitimate rendering change lands (upgrading
matplotlib, switching to coord-gen v2, changing the IR band table,
etc.) and the perceptual-hash diff starts firing. Writes PNGs to
``tests/golden/`` which the CI then compares against on every run.

Each entry is a ``(key, producer)`` pair — the key is the filename
(sans extension); the producer takes a `Path` and writes the baseline
image there.
"""
from __future__ import annotations
import os
import sys
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

GOLDEN_DIR = ROOT / "tests" / "golden"


# ------------------------------------------------------------------
# Producers — pure functions that take an output path and write a PNG.

def _mol2d(smiles: str):
    def producer(path: Path) -> None:
        from rdkit import Chem
        from orgchem.render.draw2d import render_svg
        # Save as PNG — convert SVG to PNG via RDKit's Cairo path for
        # deterministic pixel output.
        from rdkit.Chem.Draw import rdMolDraw2D
        mol = Chem.MolFromSmiles(smiles)
        d = rdMolDraw2D.MolDraw2DCairo(500, 400)
        d.drawOptions().bondLineWidth = 2
        d.DrawMolecule(mol)
        d.FinishDrawing()
        path.write_bytes(d.GetDrawingText())
    return producer


def _energy_profile(reaction_name_substr: str):
    def producer(path: Path) -> None:
        from orgchem.agent.headless import HeadlessApp
        with HeadlessApp() as app:
            rows = app.call("list_energy_profiles")
            match = next(r for r in rows if reaction_name_substr in r["name"])
            app.call("export_energy_profile",
                     reaction_id=match["id"], path=str(path))
    return producer


def _mo_diagram(smiles: str):
    def producer(path: Path) -> None:
        from orgchem.core.huckel import huckel_for_smiles
        from orgchem.render.draw_mo import export_mo_diagram
        res = huckel_for_smiles(smiles)
        export_mo_diagram(res, path, title=f"MO — {smiles}")
    return producer


def _ir_spectrum(smiles: str):
    def producer(path: Path) -> None:
        from orgchem.render.draw_ir import export_ir_spectrum
        export_ir_spectrum(smiles, path, title=f"IR — {smiles}")
    return producer


def _reaction_scheme(smarts: str):
    def producer(path: Path) -> None:
        from orgchem.render.draw_reaction import export_reaction
        export_reaction(smarts, path)
    return producer


GOLDENS = [
    ("mol2d_benzene",       _mol2d("c1ccccc1")),
    ("mol2d_aspirin",       _mol2d("CC(=O)Oc1ccccc1C(=O)O")),
    ("mol2d_ibuprofen_R",   _mol2d("CC(C)Cc1ccc(cc1)[C@@H](C)C(=O)O")),
    ("mol2d_caffeine",      _mol2d("Cn1cnc2n(C)c(=O)n(C)c(=O)c12")),

    ("reaction_diels_alder", _reaction_scheme("C=CC=C.C=C>>C1=CCCCC1")),
    ("reaction_sn2",         _reaction_scheme("CBr.[OH-]>>CO.[Br-]")),

    ("energy_sn1",           _energy_profile("SN1: tert-butyl")),
    ("energy_diels_alder",   _energy_profile("Diels-Alder")),

    ("mo_benzene",           _mo_diagram("c1ccccc1")),
    ("mo_butadiene",         _mo_diagram("C=CC=C")),

    ("ir_acetic_acid",       _ir_spectrum("CC(=O)O")),
    ("ir_acetone",           _ir_spectrum("CC(=O)C")),
]


def main() -> int:
    GOLDEN_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Regenerating {len(GOLDENS)} golden baselines → {GOLDEN_DIR}")
    for key, producer in GOLDENS:
        out = GOLDEN_DIR / f"{key}.png"
        print(f"  {key} → ", end="", flush=True)
        producer(out)
        print(f"{out.stat().st_size} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
