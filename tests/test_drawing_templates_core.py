"""Phase 36c (round 129) — headless tests for the template core.

Covers the catalogue contents + :func:`apply_template` semantics
(merge vs attach, free-standing vs fused placement) without
spinning up a Qt event loop.  GUI integration is tested
separately in ``test_drawing_panel_templates.py``.
"""
from __future__ import annotations

import pytest

pytest.importorskip("rdkit")

from orgchem.core.drawing import (
    Structure, structure_to_smiles,
)
from orgchem.core.drawing_templates import (
    DEFAULT_SCALE_PX,
    apply_template,
    get_template,
    list_template_names,
    list_templates,
)


# ---- catalogue --------------------------------------------------

def test_catalogue_contains_expected_rings():
    names = set(list_template_names())
    for ring in ("cyclopropane", "cyclobutane", "cyclopentane",
                 "cyclohexane", "benzene", "pyridine", "pyrimidine",
                 "furan", "thiophene", "pyrrole"):
        assert ring in names


def test_catalogue_contains_expected_fgs():
    names = set(list_template_names())
    for fg in ("oh", "nh2", "me", "cooh", "cho", "co", "no2",
               "cn", "ome", "cf3"):
        assert fg in names


def test_list_templates_filters_by_kind():
    rings = list_templates(kind="ring")
    fgs = list_templates(kind="fg")
    assert all(t.kind == "ring" for t in rings)
    assert all(t.kind == "fg" for t in fgs)
    # Non-trivial counts.
    assert len(rings) >= 7
    assert len(fgs) >= 9


def test_get_template_returns_none_for_unknown():
    assert get_template("does-not-exist") is None


# ---- ring placement on empty canvas -----------------------------

def test_benzene_on_empty_canvas_yields_six_atoms_six_bonds():
    s = Structure()
    pos = []
    new_s, new_pos = apply_template(
        s, pos, get_template("benzene"),
        anchor_pos=(0.0, 0.0),
    )
    assert new_s.n_atoms == 6
    assert new_s.n_bonds == 6
    assert all(a.element == "C" for a in new_s.atoms)
    smi = structure_to_smiles(new_s)
    from rdkit import Chem
    assert Chem.CanonSmiles(smi) == Chem.CanonSmiles("c1ccccc1")


def test_cyclohexane_on_empty_canvas_is_saturated():
    s = Structure()
    new_s, _ = apply_template(
        s, [], get_template("cyclohexane"),
        anchor_pos=(0.0, 0.0),
    )
    assert new_s.n_atoms == 6
    assert new_s.n_bonds == 6
    assert all(b.order == 1 for b in new_s.bonds)
    from rdkit import Chem
    smi = structure_to_smiles(new_s)
    assert Chem.CanonSmiles(smi) == Chem.CanonSmiles("C1CCCCC1")


def test_pyridine_has_one_nitrogen():
    new_s, _ = apply_template(
        Structure(), [], get_template("pyridine"),
        anchor_pos=(0.0, 0.0),
    )
    n_count = sum(1 for a in new_s.atoms if a.element == "N")
    assert n_count == 1


def test_furan_has_one_oxygen():
    new_s, _ = apply_template(
        Structure(), [], get_template("furan"),
        anchor_pos=(0.0, 0.0),
    )
    o_count = sum(1 for a in new_s.atoms if a.element == "O")
    assert o_count == 1
    assert new_s.n_atoms == 5


# ---- ring fusion onto existing atom -----------------------------

def test_benzene_fused_onto_existing_atom_adds_five_atoms():
    """The anchor atom MERGES with the host — only n-1 new atoms."""
    s = Structure()
    s.add_atom("C")
    pos = [(100.0, 100.0)]
    new_s, new_pos = apply_template(
        s, pos, get_template("benzene"),
        anchor_pos=(100.0, 100.0),
        host_atom_idx=0,
    )
    assert new_s.n_atoms == 6        # 1 existing + 5 new
    assert new_s.n_bonds == 6        # full ring
    # Host atom (index 0) should have two ring neighbours.
    assert len(new_s.neighbours(0)) == 2


def test_cyclopropane_fused_onto_existing_atom_yields_propane_ring():
    s = Structure()
    s.add_atom("C")
    new_s, _ = apply_template(
        s, [(0.0, 0.0)], get_template("cyclopropane"),
        anchor_pos=(0.0, 0.0),
        host_atom_idx=0,
    )
    assert new_s.n_atoms == 3
    assert new_s.n_bonds == 3
    from rdkit import Chem
    smi = structure_to_smiles(new_s)
    assert Chem.CanonSmiles(smi) == Chem.CanonSmiles("C1CC1")


# ---- FG placement -----------------------------------------------

def test_oh_on_empty_canvas_creates_methanol():
    """auto_attach_element="C" means empty-canvas-OH = HOCH3."""
    new_s, _ = apply_template(
        Structure(), [], get_template("oh"),
        anchor_pos=(0.0, 0.0),
    )
    assert new_s.n_atoms == 2     # synthesised C + template O
    assert new_s.n_bonds == 1
    from rdkit import Chem
    smi = structure_to_smiles(new_s)
    assert Chem.CanonSmiles(smi) == Chem.CanonSmiles("CO")


def test_oh_on_existing_atom_attaches_as_alcohol():
    s = Structure()
    s.add_atom("C")
    new_s, _ = apply_template(
        s, [(0.0, 0.0)], get_template("oh"),
        anchor_pos=(0.0, 0.0),
        host_atom_idx=0,
    )
    assert new_s.n_atoms == 2     # host C + new O
    assert new_s.n_bonds == 1
    # Host (0) should be bonded to the new O (1).
    assert {new_s.bonds[0].begin_idx, new_s.bonds[0].end_idx} == {0, 1}
    from rdkit import Chem
    smi = structure_to_smiles(new_s)
    assert Chem.CanonSmiles(smi) == Chem.CanonSmiles("CO")


def test_cooh_on_existing_atom_yields_acetic_acid():
    """Methyl + COOH template = acetic acid round-trip."""
    s = Structure()
    s.add_atom("C")
    new_s, _ = apply_template(
        s, [(0.0, 0.0)], get_template("cooh"),
        anchor_pos=(0.0, 0.0),
        host_atom_idx=0,
    )
    from rdkit import Chem
    smi = structure_to_smiles(new_s)
    assert Chem.CanonSmiles(smi) == Chem.CanonSmiles("CC(=O)O")


def test_co_template_attaches_double_bond():
    """C=O template uses attach_order=2 → ketone-ish behaviour."""
    s = Structure()
    s.add_atom("C")
    s.add_atom("C")
    s.add_bond(0, 1, order=1)
    new_s, _ = apply_template(
        s, [(0.0, 0.0), (40.0, 0.0)], get_template("co"),
        anchor_pos=(40.0, 0.0),
        host_atom_idx=1,
    )
    # New O atom + a double bond to atom 1.
    assert new_s.n_atoms == 3
    assert new_s.n_bonds == 2
    new_bond = new_s.bonds[-1]
    assert new_bond.order == 2
    assert {new_bond.begin_idx, new_bond.end_idx} == {1, 2}
    from rdkit import Chem
    smi = structure_to_smiles(new_s)
    # CC(=O) loses the implicit-H trailing carbon → "CC=O"
    # (acetaldehyde-like) since RDKit fills H by valence.
    assert Chem.CanonSmiles(smi) == Chem.CanonSmiles("CC=O")


def test_no2_round_trips_as_zwitterion():
    s = Structure()
    s.add_atom("C")
    new_s, _ = apply_template(
        s, [(0.0, 0.0)], get_template("no2"),
        anchor_pos=(0.0, 0.0), host_atom_idx=0,
    )
    from rdkit import Chem
    smi = structure_to_smiles(new_s)
    assert Chem.CanonSmiles(smi) == Chem.CanonSmiles(
        "C[N+](=O)[O-]")


def test_cn_template_yields_acetonitrile_via_methyl_host():
    s = Structure()
    s.add_atom("C")
    new_s, _ = apply_template(
        s, [(0.0, 0.0)], get_template("cn"),
        anchor_pos=(0.0, 0.0), host_atom_idx=0,
    )
    from rdkit import Chem
    smi = structure_to_smiles(new_s)
    assert Chem.CanonSmiles(smi) == Chem.CanonSmiles("CC#N")


def test_apply_template_does_not_mutate_input():
    s = Structure()
    s.add_atom("C")
    pos = [(0.0, 0.0)]
    apply_template(s, pos, get_template("benzene"),
                   anchor_pos=(0.0, 0.0), host_atom_idx=0)
    # Original untouched.
    assert s.n_atoms == 1
    assert pos == [(0.0, 0.0)]


# ---- positions -----------------------------------------------

def test_ring_positions_are_scaled_to_pixels():
    new_s, new_pos = apply_template(
        Structure(), [], get_template("benzene"),
        anchor_pos=(100.0, 100.0),
        scale=DEFAULT_SCALE_PX,
    )
    # Anchor lands at click point.
    assert new_pos[0] == (100.0, 100.0)
    # Other atoms sit roughly DEFAULT_SCALE_PX pixels away.
    import math
    for i in range(1, len(new_pos)):
        dx = new_pos[i][0] - new_pos[0][0]
        dy = new_pos[i][1] - new_pos[0][1]
        # Distance from anchor must be >0 (template not collapsed).
        assert math.hypot(dx, dy) > 0
