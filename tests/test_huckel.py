"""Tests for Phase 14a — simple Hückel MO theory."""
from __future__ import annotations
import math
import os
import pytest

pytest.importorskip("rdkit")


# ---- Canonical textbook eigenvalues -----------------------------------

def test_ethene_energies():
    from orgchem.core.huckel import huckel_for_smiles
    r = huckel_for_smiles("C=C")
    assert r.n_pi_atoms == 2
    assert r.n_pi_electrons == 2
    assert r.energies == pytest.approx([1.0, -1.0])
    # HOMO occupied, LUMO empty
    assert r.occupations == [2, 0]
    assert r.homo_index == 0
    assert r.lumo_index == 1


def test_butadiene_golden_ratio_energies():
    """Textbook: eigenvalues ±(1 + √5)/2 and ±(√5 − 1)/2."""
    from orgchem.core.huckel import huckel_for_smiles
    r = huckel_for_smiles("C=CC=C")
    phi = (1 + math.sqrt(5)) / 2.0        # 1.618...
    inv = 1.0 / phi                         # 0.618...
    assert r.energies == pytest.approx([phi, inv, -inv, -phi], abs=1e-6)
    assert r.n_pi_electrons == 4
    assert r.occupations == [2, 2, 0, 0]


def test_benzene_is_2_1_1_m1_m1_m2():
    from orgchem.core.huckel import huckel_for_smiles
    r = huckel_for_smiles("c1ccccc1")
    assert r.energies == pytest.approx([2.0, 1.0, 1.0, -1.0, -1.0, -2.0])
    # 6 π electrons fully occupy the 3 bonding MOs
    assert r.occupations == [2, 2, 2, 0, 0, 0]


def test_allyl_cation_radical_anion_same_structure_different_electrons():
    """All three have 3 π atoms and eigenvalues √2, 0, −√2 — only the
    electron count varies."""
    from orgchem.core.huckel import huckel_for_smiles
    sqrt2 = math.sqrt(2.0)
    for smi, e_count in (("[CH2+]C=C", 2),
                         ("[CH2]C=C", 3),
                         ("[CH2-]C=C", 4)):
        r = huckel_for_smiles(smi)
        assert r.n_pi_atoms == 3, f"{smi} should have 3 π atoms"
        assert r.energies == pytest.approx([sqrt2, 0.0, -sqrt2], abs=1e-6), smi
        assert r.n_pi_electrons == e_count, smi


def test_cyclopentadienide_is_aromatic_6e():
    """Cp⁻ has 6 π electrons (4n+2), aromatic."""
    from orgchem.core.huckel import huckel_for_smiles
    r = huckel_for_smiles("[cH-]1cccc1")
    assert r.n_pi_electrons == 6


def test_pyrrole_donates_lone_pair():
    """Pyrrole N-H contributes 2 electrons → 6 π electrons total."""
    from orgchem.core.huckel import huckel_for_smiles
    r = huckel_for_smiles("c1cc[nH]c1")
    assert r.n_pi_electrons == 6


def test_pyridine_retains_lone_pair():
    """Pyridine N contributes 1 electron → 6 π electrons total."""
    from orgchem.core.huckel import huckel_for_smiles
    r = huckel_for_smiles("c1ccncc1")
    assert r.n_pi_electrons == 6


def test_total_pi_energy_butadiene():
    """2(α + 1.618β) + 2(α + 0.618β) = 4α + 4.472β."""
    from orgchem.core.huckel import huckel_for_smiles
    r = huckel_for_smiles("C=CC=C")
    assert r.total_pi_energy == pytest.approx(4.472, abs=1e-2)


def test_alkane_has_no_pi_system():
    """Pure sp3 alkane: empty π system."""
    from orgchem.core.huckel import huckel_for_smiles
    r = huckel_for_smiles("CCCC")
    assert r.n_pi_atoms == 0
    assert r.energies == []


def test_bad_smiles_raises():
    from orgchem.core.huckel import huckel_for_smiles
    with pytest.raises(ValueError):
        huckel_for_smiles("not a molecule")


# ---- Renderer --------------------------------------------------------

def test_mo_diagram_png_and_svg(tmp_path):
    from orgchem.core.huckel import huckel_for_smiles
    from orgchem.render.draw_mo import export_mo_diagram
    r = huckel_for_smiles("c1ccccc1")
    png = export_mo_diagram(r, tmp_path / "benzene.png")
    svg = export_mo_diagram(r, tmp_path / "benzene.svg")
    assert png.exists() and png.stat().st_size > 5_000
    text = svg.read_text()
    assert "<svg" in text
    assert "HOMO" in text
    assert "LUMO" in text


def test_mo_diagram_empty_system_raises(tmp_path):
    from orgchem.core.huckel import huckel_for_smiles
    from orgchem.render.draw_mo import export_mo_diagram
    from orgchem.messaging.errors import RenderError
    r = huckel_for_smiles("CCCC")
    with pytest.raises(RenderError):
        export_mo_diagram(r, tmp_path / "empty.png")


def test_mo_diagram_bad_format_raises(tmp_path):
    from orgchem.core.huckel import huckel_for_smiles
    from orgchem.render.draw_mo import export_mo_diagram
    from orgchem.messaging.errors import RenderError
    r = huckel_for_smiles("C=C")
    with pytest.raises(RenderError):
        export_mo_diagram(r, tmp_path / "x.pdf")


# ---- Agent actions ---------------------------------------------------

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_huckel_action_benzene(app):
    r = app.call("huckel_mos", smiles="c1ccccc1")
    assert "error" not in r
    assert r["n_pi_atoms"] == 6
    assert r["n_pi_electrons"] == 6
    assert r["homo_energy"] == pytest.approx(1.0)
    assert r["lumo_energy"] == pytest.approx(-1.0)


def test_huckel_action_bad_smiles(app):
    r = app.call("huckel_mos", smiles="not a molecule")
    assert "error" in r


def test_export_mo_diagram_action(app, tmp_path):
    r = app.call("export_mo_diagram", smiles="C=CC=C",
                 path=str(tmp_path / "butadiene.png"))
    assert "error" not in r
    assert r["n_pi_atoms"] == 4
    assert r["n_pi_electrons"] == 4
    from pathlib import Path
    assert Path(r["path"]).stat().st_size > 5_000
