"""Tests for Phase 13c follow-up — lone-pair dots + bond-midpoint arrows."""
from __future__ import annotations
import pytest

pytest.importorskip("rdkit")


# -------------------------- data-model tests ------------------------

def test_arrow_default_has_no_bond_endpoints():
    from orgchem.core.mechanism import Arrow
    a = Arrow(from_atom=0, to_atom=1)
    assert a.from_bond is None
    assert a.to_bond is None


def test_arrow_accepts_bond_endpoints():
    from orgchem.core.mechanism import Arrow
    a = Arrow(from_atom=0, to_atom=1, from_bond=(0, 1), to_bond=(2, 3))
    assert a.from_bond == (0, 1)
    assert a.to_bond == (2, 3)


def test_step_default_lone_pairs_empty():
    from orgchem.core.mechanism import MechanismStep
    s = MechanismStep(title="t", description="d", smiles="O")
    assert s.lone_pairs == []


def test_mechanism_json_roundtrips_new_fields():
    """Bond-midpoint tuples become lists in JSON, must coerce back."""
    from orgchem.core.mechanism import Arrow, Mechanism, MechanismStep
    mech = Mechanism(
        reaction_id=1,
        steps=[
            MechanismStep(
                title="step", description="x", smiles="CC=C",
                arrows=[
                    Arrow(from_atom=0, to_atom=0, from_bond=(1, 2),
                          to_bond=None, label="π"),
                ],
                lone_pairs=[0, 2],
            ),
        ],
    )
    text = mech.to_json()
    r = Mechanism.from_json(text)
    assert r.steps[0].arrows[0].from_bond == (1, 2)
    assert r.steps[0].arrows[0].to_bond is None
    assert r.steps[0].lone_pairs == [0, 2]


def test_mechanism_old_json_still_parses():
    """Files saved before Phase 13c must still load — no lone_pairs key,
    no bond fields on arrows."""
    from orgchem.core.mechanism import Mechanism
    legacy = """\
{
  "reaction_id": 1,
  "steps": [
    {"title": "t", "description": "d", "smiles": "O",
     "arrows": [{"from_atom": 0, "to_atom": 0, "kind": "curly",
                 "bend": 0.35, "label": ""}]}
  ]
}
"""
    mech = Mechanism.from_json(legacy)
    assert len(mech) == 1
    assert mech.steps[0].lone_pairs == []
    assert mech.steps[0].arrows[0].from_bond is None


# -------------------------- renderer tests --------------------------

def test_lone_pair_renders_two_circles():
    from orgchem.core.mechanism import MechanismStep
    from orgchem.render.draw_mechanism import render_step_svg
    step = MechanismStep(title="lone", description="", smiles="O",
                         lone_pairs=[0])
    svg = render_step_svg(step)
    # Two <circle> elements whose fill matches our lone-pair colour.
    assert svg.count("#1a1a1a") >= 2


def test_lone_pair_out_of_range_is_skipped():
    from orgchem.core.mechanism import MechanismStep
    from orgchem.render.draw_mechanism import render_step_svg
    step = MechanismStep(title="oob", description="", smiles="CC",
                         lone_pairs=[99])
    # No crash; the out-of-range index is logged and skipped.
    svg = render_step_svg(step)
    assert svg.startswith("<?xml") or svg.startswith("<svg")


def test_bond_midpoint_arrow_renders():
    """An arrow whose from_bond is set should produce a path element."""
    from orgchem.core.mechanism import Arrow, MechanismStep
    from orgchem.render.draw_mechanism import render_step_svg
    step = MechanismStep(
        title="bond-midpoint", description="", smiles="C=CC=C",
        arrows=[Arrow(from_atom=0, to_atom=2, from_bond=(0, 1))],
    )
    svg = render_step_svg(step)
    # The curved-arrow path should be present.
    assert 'marker-end="url(#mech-curly)"' in svg


def test_bond_midpoint_out_of_range_skipped():
    """Arrow with an out-of-range bond endpoint must not crash."""
    from orgchem.core.mechanism import Arrow, MechanismStep
    from orgchem.render.draw_mechanism import render_step_svg
    step = MechanismStep(
        title="oob", description="", smiles="CC",
        arrows=[
            Arrow(from_atom=0, to_atom=1, from_bond=(99, 100)),
        ],
    )
    svg = render_step_svg(step)
    # Still produced a molecule; just no extra arrow path added.
    assert "<svg" in svg


def test_arrow_to_bond_midpoint():
    """Arrow *ending* at a bond midpoint (e.g. lone pair attacking a
    π-bond) should also render."""
    from orgchem.core.mechanism import Arrow, MechanismStep
    from orgchem.render.draw_mechanism import render_step_svg
    step = MechanismStep(
        title="to-bond", description="", smiles="C=CCO",
        arrows=[Arrow(from_atom=3, to_atom=0, to_bond=(0, 1))],
        lone_pairs=[3],
    )
    svg = render_step_svg(step)
    assert 'marker-end="url(#mech-curly)"' in svg
    assert svg.count("#1a1a1a") >= 2  # lone-pair dots too


def test_fishhook_still_supported():
    """Ensure we didn't break the radical-arrow path."""
    from orgchem.core.mechanism import Arrow, MechanismStep
    from orgchem.render.draw_mechanism import render_step_svg
    step = MechanismStep(
        title="radical", description="", smiles="C-O",
        arrows=[Arrow(from_atom=0, to_atom=1, kind="fishhook")],
    )
    svg = render_step_svg(step)
    assert 'marker-end="url(#mech-fish)"' in svg
