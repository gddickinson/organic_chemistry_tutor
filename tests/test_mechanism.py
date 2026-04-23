"""Unit + headless-integration tests for the mechanism player."""
from __future__ import annotations
import os
import json
import pytest
from pathlib import Path

pytest.importorskip("rdkit")


# ---- Data model round-trip -----------------------------------------------

def test_mechanism_json_roundtrip():
    from orgchem.core.mechanism import Arrow, Mechanism, MechanismStep
    mech = Mechanism(reaction_id=42, steps=[
        MechanismStep(
            title="Attack",
            description="Hydroxide attacks the carbon",
            smiles="C[Br].[OH-]",
            arrows=[
                Arrow(from_atom=2, to_atom=0, kind="curly"),
                Arrow(from_atom=0, to_atom=1, kind="fishhook", bend=0.4,
                      label="unusual radical step"),
            ],
        ),
    ])
    text = mech.to_json()
    data = json.loads(text)
    assert data["reaction_id"] == 42
    assert len(data["steps"]) == 1
    assert data["steps"][0]["arrows"][1]["kind"] == "fishhook"

    mech2 = Mechanism.from_json(text)
    assert mech2.reaction_id == 42
    assert mech2.steps[0].arrows[0].from_atom == 2
    assert mech2.steps[0].arrows[1].label == "unusual radical step"


def test_mechanism_len_and_index():
    from orgchem.core.mechanism import Mechanism, MechanismStep
    mech = Mechanism(steps=[
        MechanismStep(title="A", description="", smiles="CO"),
        MechanismStep(title="B", description="", smiles="CC"),
        MechanismStep(title="C", description="", smiles="C"),
    ])
    assert len(mech) == 3
    assert mech[1].title == "B"


# ---- SVG rendering --------------------------------------------------------

def test_render_step_svg_includes_arrow_paths():
    from orgchem.core.mechanism import Arrow, MechanismStep
    from orgchem.render.draw_mechanism import render_step_svg
    step = MechanismStep(
        title="SN2 attack",
        description="hydroxide attacks methyl bromide backside",
        smiles="C[Br].[OH-]",
        arrows=[
            Arrow(from_atom=2, to_atom=0, kind="curly"),
            Arrow(from_atom=0, to_atom=1, kind="curly"),
        ],
    )
    svg = render_step_svg(step)
    assert svg.lstrip().startswith(("<?xml", "<svg"))
    assert "mech-curly" in svg
    assert svg.count("stroke-linecap=\"round\"") == 2   # two arrow paths


def test_render_step_svg_bad_smiles_raises():
    from orgchem.core.mechanism import MechanismStep
    from orgchem.render.draw_mechanism import render_step_svg
    from orgchem.messaging.errors import RenderError
    with pytest.raises(RenderError):
        render_step_svg(MechanismStep(title="bad", description="",
                                      smiles="not a molecule"))


def test_render_step_svg_ignores_out_of_range_arrows():
    from orgchem.core.mechanism import Arrow, MechanismStep
    from orgchem.render.draw_mechanism import render_step_svg
    step = MechanismStep(
        title="bounds",
        description="arrow indices way out of range",
        smiles="CC",
        arrows=[Arrow(from_atom=100, to_atom=200, kind="curly")],
    )
    svg = render_step_svg(step)  # should not raise
    # out-of-range arrow silently skipped → no arrow path
    assert "stroke-linecap=\"round\"" not in svg


# ---- Seeded DB / agent integration ---------------------------------------

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_mechanism_seed_populated_for_textbook_reactions(app):
    rows = app.call("list_mechanisms")
    names = {r["name"] for r in rows}
    # Core 5 from Phase 2b + aldol/Grignard + Wittig/Michael (session 10) +
    # enzyme mechanisms (Phase 16d, session 11).
    for expected in ("SN2: methyl bromide", "SN1: tert-butyl",
                     "E2: 2-bromobutane", "E1: tert-butyl",
                     "Diels-Alder",
                     "Aldol condensation",
                     "Grignard addition",
                     "Wittig reaction",
                     "Michael addition",
                     "Chymotrypsin",
                     "Aldolase class I"):
        assert any(expected in n for n in names), f"missing mechanism for {expected!r}"
    assert len(rows) >= 11


def test_sn2_mechanism_has_two_steps(app):
    rows = app.call("list_mechanisms")
    sn2 = next(r for r in rows if "SN2: methyl bromide" in r["name"])
    assert sn2["steps"] == 2


def test_export_mechanism_step(app, tmp_path):
    rows = app.call("list_mechanisms")
    diels = next(r for r in rows if "Diels-Alder" in r["name"])
    out = app.call("export_mechanism_step",
                   reaction_id=diels["id"], step_index=0,
                   path=str(tmp_path / "da_step0.svg"))
    assert "error" not in out, out
    content = Path(out["path"]).read_text()
    assert "<svg" in content
    # Concerted Diels-Alder has 3 arrows in step 0.
    assert content.count("stroke-linecap=\"round\"") == 3


# ---- Phase 13c full-kinetics composite --------------------------------

def test_composite_render_direct(tmp_path):
    from orgchem.core.mechanism import Arrow, Mechanism, MechanismStep
    from orgchem.render.draw_mechanism_composite import export_composite
    mech = Mechanism(steps=[
        MechanismStep(
            title="Step 1: attack",
            description="Hydroxide attacks methyl bromide backside.",
            smiles="C[Br].[OH-]",
            arrows=[Arrow(from_atom=2, to_atom=0, kind="curly"),
                    Arrow(from_atom=0, to_atom=1, kind="curly")],
        ),
        MechanismStep(
            title="Step 2: products",
            description="Methanol + bromide.",
            smiles="CO.[Br-]",
        ),
    ])
    out = export_composite(mech, tmp_path / "composite.svg",
                           reaction_name="TestRxn")
    text = out.read_text()
    assert text.startswith("<svg")
    # Every step appears as "Step N" in the composite
    assert "Step 1" in text
    assert "Step 2" in text
    # And the top-level title block
    assert "TestRxn" in text


def test_composite_render_empty_raises(tmp_path):
    from orgchem.core.mechanism import Mechanism
    from orgchem.render.draw_mechanism_composite import export_composite
    from orgchem.messaging.errors import RenderError
    with pytest.raises(RenderError):
        export_composite(Mechanism(steps=[]), tmp_path / "empty.svg")


def test_composite_png_output(tmp_path):
    from orgchem.core.mechanism import Arrow, Mechanism, MechanismStep
    from orgchem.render.draw_mechanism_composite import export_composite
    mech = Mechanism(steps=[
        MechanismStep(title="s1", description="first",
                      smiles="C[Br]", arrows=[]),
        MechanismStep(title="s2", description="second", smiles="CO"),
    ])
    out = export_composite(mech, tmp_path / "composite.png")
    assert out.exists() and out.stat().st_size > 1000


def test_export_mechanism_composite_action(app, tmp_path):
    """Agent-layer smoke: composite export via the action registry."""
    rows = app.call("list_mechanisms")
    sn1 = next(r for r in rows if "SN1: tert-butyl" in r["name"])
    out = app.call("export_mechanism_composite",
                   reaction_id=sn1["id"],
                   path=str(tmp_path / "sn1_composite.svg"))
    assert "error" not in out
    # SN1 seed has 4 steps
    assert out["steps"] == 4
    text = Path(out["path"]).read_text()
    assert "Step 1" in text
    assert "Step 4" in text


def test_export_mechanism_composite_missing(app, tmp_path):
    out = app.call("export_mechanism_composite",
                   reaction_id=99_999,
                   path=str(tmp_path / "none.svg"))
    assert "error" in out
