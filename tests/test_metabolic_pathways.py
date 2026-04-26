"""Phase 42a (round 147) — headless tests for the metabolic-
pathways catalogue + agent actions + dialog.
"""
from __future__ import annotations
import os

import pytest


# ==================================================================
# Catalogue contents
# ==================================================================

def test_catalogue_size_at_least_ten():
    from orgchem.core.metabolic_pathways import list_pathways
    assert len(list_pathways()) >= 10


def test_canonical_pathways_present():
    from orgchem.core.metabolic_pathways import get_pathway
    for must in ("glycolysis", "tca_cycle", "ox_phos",
                 "beta_oxidation", "fatty_acid_synthesis",
                 "cholesterol_biosynthesis", "urea_cycle",
                 "pentose_phosphate", "heme_biosynthesis",
                 "calvin_cycle", "glycogen_metabolism"):
        assert get_pathway(must) is not None, \
            f"missing pathway {must}"


def test_every_pathway_has_required_fields():
    from orgchem.core.metabolic_pathways import list_pathways
    for p in list_pathways():
        assert p.id and p.name and p.category
        assert p.cellular_compartment
        assert p.overview
        assert p.steps, f"empty steps on {p.id}"


def test_every_step_has_required_fields():
    from orgchem.core.metabolic_pathways import list_pathways
    for p in list_pathways():
        for s in p.steps:
            assert s.step_number > 0
            assert s.substrates
            assert s.enzyme_name
            assert s.products
            assert s.reversibility in (
                "reversible", "irreversible")


def test_glycolysis_has_ten_steps():
    """The 10 canonical Embden-Meyerhof-Parnas steps."""
    from orgchem.core.metabolic_pathways import get_pathway
    g = get_pathway("glycolysis")
    assert len(g.steps) == 10


def test_glycolysis_step_3_is_pfk_rate_limiting():
    """Step 3 is the PFK-1 rate-limiting step + carries
    multiple regulatory effectors."""
    from orgchem.core.metabolic_pathways import get_pathway
    g = get_pathway("glycolysis")
    s3 = g.steps[2]
    assert "phosphofructokinase" in s3.enzyme_name.lower() \
        or "pfk" in s3.enzyme_name.lower()
    assert s3.reversibility == "irreversible"
    assert len(s3.regulatory_effectors) >= 3
    # Must include both inhibitor + activator effectors.
    modes = {r.mode for r in s3.regulatory_effectors}
    assert "inhibitor" in modes and "activator" in modes


def test_tca_cycle_has_eight_steps():
    from orgchem.core.metabolic_pathways import get_pathway
    t = get_pathway("tca_cycle")
    assert len(t.steps) == 8


def test_ox_phos_has_five_complexes():
    from orgchem.core.metabolic_pathways import get_pathway
    o = get_pathway("ox_phos")
    assert len(o.steps) == 5
    # Each step references a Complex I-V enzyme.
    for i, s in enumerate(o.steps, start=1):
        assert f"Complex {['I', 'II', 'III', 'IV', 'V'][i-1]}" \
            in s.enzyme_name


def test_urea_cycle_has_five_steps():
    from orgchem.core.metabolic_pathways import get_pathway
    u = get_pathway("urea_cycle")
    assert len(u.steps) == 5


def test_heme_biosynthesis_has_eight_steps():
    """Heme biosynthesis has 8 enzyme steps total (one per
    enzyme deficiency / porphyria)."""
    from orgchem.core.metabolic_pathways import get_pathway
    h = get_pathway("heme_biosynthesis")
    assert len(h.steps) == 8


# ---- Per-pathway teaching invariants -------------------------

def test_glycolysis_step_1_hexokinase_inhibition():
    """Hexokinase step must surface G6P product inhibition."""
    from orgchem.core.metabolic_pathways import get_pathway
    s1 = get_pathway("glycolysis").steps[0]
    effectors = {r.name.lower() for r in s1.regulatory_effectors}
    assert any("glucose-6" in e for e in effectors)


def test_tca_cycle_membrane_enzyme():
    """Succinate dehydrogenase is the only membrane-bound TCA
    enzyme — that's a textbook teaching point."""
    from orgchem.core.metabolic_pathways import get_pathway
    t = get_pathway("tca_cycle")
    sdh = next(s for s in t.steps
               if "succinate dehydrogenase" in s.enzyme_name.lower())
    assert "membrane" in sdh.notes.lower()


def test_ox_phos_complex_iv_describes_terminal_acceptor():
    from orgchem.core.metabolic_pathways import get_pathway
    o = get_pathway("ox_phos")
    cIV = next(s for s in o.steps if "Complex IV" in s.enzyme_name)
    body = (cIV.notes + " " + " ".join(cIV.products)).lower()
    assert "h₂o" in body or "h2o" in body


def test_cholesterol_step_2_is_statin_target():
    """HMG-CoA reductase step must surface statin inhibition
    + cholesterol feedback."""
    from orgchem.core.metabolic_pathways import get_pathway
    c = get_pathway("cholesterol_biosynthesis")
    hmgcr = c.steps[1]
    assert "hmg-coa reductase" in hmgcr.enzyme_name.lower()
    effectors = [r.name.lower() for r in hmgcr.regulatory_effectors]
    assert any("statin" in e for e in effectors)
    assert any("cholesterol" in e for e in effectors)


def test_pentose_phosphate_g6pd_deficiency_note():
    """G6PD step should mention the inherited deficiency
    (most common human enzyme deficiency)."""
    from orgchem.core.metabolic_pathways import get_pathway
    p = get_pathway("pentose_phosphate")
    g6pd = p.steps[0]
    assert "g6pd" in g6pd.notes.lower() \
        or "deficiency" in g6pd.notes.lower()


def test_glycogen_phosphorylase_has_hormonal_regulation():
    from orgchem.core.metabolic_pathways import get_pathway
    g = get_pathway("glycogen_metabolism")
    phos = next(s for s in g.steps
                if "glycogen phosphorylase" in s.enzyme_name.lower())
    effectors = [r.name.lower() for r in phos.regulatory_effectors]
    # Glucagon / epinephrine / insulin / AMP / ATP all should
    # be present.
    body = " ".join(effectors)
    assert "amp" in body or "atp" in body
    assert "insulin" in body or "glucagon" in body \
        or "epinephrine" in body


# ---- Filter / lookup ------------------------------------------

def test_list_filtered_by_category():
    from orgchem.core.metabolic_pathways import list_pathways
    cc = list_pathways(category="central-carbon")
    assert all(p.category == "central-carbon" for p in cc)
    assert len(cc) >= 4   # glyco + TCA + ox-phos + PPP


def test_list_unknown_category_returns_empty():
    from orgchem.core.metabolic_pathways import list_pathways
    assert list_pathways(category="not-a-real-category") == []


def test_get_unknown_pathway_returns_none():
    from orgchem.core.metabolic_pathways import get_pathway
    assert get_pathway("does-not-exist") is None


def test_find_pathways_substring():
    from orgchem.core.metabolic_pathways import find_pathways
    rows = find_pathways("krebs")
    assert any(r.id == "tca_cycle" for r in rows)


def test_find_pathways_case_insensitive():
    from orgchem.core.metabolic_pathways import find_pathways
    a = {r.id for r in find_pathways("UREA")}
    b = {r.id for r in find_pathways("urea")}
    assert a == b


def test_find_pathways_empty_returns_empty():
    from orgchem.core.metabolic_pathways import find_pathways
    assert find_pathways("") == []


# ---- to_dict serialisation ------------------------------------

def test_pathway_to_dict_keys():
    from orgchem.core.metabolic_pathways import (
        get_pathway, pathway_to_dict,
    )
    d = pathway_to_dict(get_pathway("glycolysis"))
    expected = {
        "id", "name", "category", "cellular_compartment",
        "overview", "overall_delta_g_kjmol",
        "textbook_reference", "n_steps", "steps",
    }
    assert set(d.keys()) == expected
    assert d["n_steps"] == 10
    assert isinstance(d["steps"], list)


def test_step_to_dict_includes_regulators():
    from orgchem.core.metabolic_pathways import (
        get_pathway, step_to_dict,
    )
    g = get_pathway("glycolysis")
    s3 = step_to_dict(g.steps[2])  # PFK-1
    expected = {"step_number", "substrates", "enzyme_name",
                "ec_number", "products", "reversibility",
                "delta_g_kjmol", "regulatory_effectors",
                "notes"}
    assert set(s3.keys()) == expected
    assert isinstance(s3["regulatory_effectors"], list)
    assert len(s3["regulatory_effectors"]) >= 3


# ==================================================================
# Agent actions
# ==================================================================

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(5)
        yield h


def test_action_list_pathways(app):
    rows = app.call("list_metabolic_pathways")
    assert len(rows) >= 10


def test_action_list_pathways_filtered(app):
    rows = app.call("list_metabolic_pathways",
                    category="lipid")
    assert all(r["category"] == "lipid" for r in rows)


def test_action_list_pathways_unknown_category(app):
    rows = app.call("list_metabolic_pathways",
                    category="not-a-real-category")
    assert "error" in rows[0]


def test_action_get_pathway(app):
    r = app.call("get_metabolic_pathway",
                 pathway_id="glycolysis")
    assert "error" not in r
    assert r["n_steps"] == 10


def test_action_get_unknown_pathway(app):
    r = app.call("get_metabolic_pathway",
                 pathway_id="bogus")
    assert "error" in r


def test_action_find_pathways(app):
    rows = app.call("find_metabolic_pathways", needle="krebs")
    assert any(r["id"] == "tca_cycle" for r in rows)


def test_action_list_pathway_steps(app):
    rows = app.call("list_pathway_steps",
                    pathway_id="urea_cycle")
    assert len(rows) == 5
    assert rows[0]["enzyme_name"].startswith(
        "Carbamoyl phosphate")


def test_action_list_steps_unknown_pathway(app):
    rows = app.call("list_pathway_steps", pathway_id="bogus")
    assert "error" in rows[0]


# ==================================================================
# Dialog
# ==================================================================

@pytest.fixture(autouse=True)
def _reset_singleton():
    from orgchem.gui.dialogs import metabolic_pathways as mod
    mod.MetabolicPathwaysDialog._instance = None
    yield
    mod.MetabolicPathwaysDialog._instance = None


def test_dialog_constructs(app, qtbot):
    from orgchem.gui.dialogs.metabolic_pathways import (
        MetabolicPathwaysDialog,
    )
    d = MetabolicPathwaysDialog(parent=app.window)
    qtbot.addWidget(d)
    assert d._pathway_list.count() >= 10


def test_dialog_singleton(app):
    from orgchem.gui.dialogs.metabolic_pathways import (
        MetabolicPathwaysDialog,
    )
    a = MetabolicPathwaysDialog.singleton(parent=app.window)
    b = MetabolicPathwaysDialog.singleton(parent=app.window)
    assert a is b


def test_dialog_default_pathway_populates_step_table(app, qtbot):
    """First pathway auto-selected on open + step table
    populated with all its steps."""
    from orgchem.gui.dialogs.metabolic_pathways import (
        MetabolicPathwaysDialog,
    )
    d = MetabolicPathwaysDialog(parent=app.window)
    qtbot.addWidget(d)
    assert d._step_table.rowCount() > 0


def test_dialog_select_pathway_glycolysis(app, qtbot):
    from orgchem.gui.dialogs.metabolic_pathways import (
        MetabolicPathwaysDialog,
    )
    d = MetabolicPathwaysDialog(parent=app.window)
    qtbot.addWidget(d)
    ok = d.select_pathway("glycolysis")
    assert ok is True
    # Step table should have 10 rows after switch.
    assert d._step_table.rowCount() == 10


def test_dialog_select_step_shows_detail(app, qtbot):
    from orgchem.gui.dialogs.metabolic_pathways import (
        MetabolicPathwaysDialog,
    )
    d = MetabolicPathwaysDialog(parent=app.window)
    qtbot.addWidget(d)
    d.select_pathway("glycolysis")
    d.select_step(3)   # PFK-1
    title = d._step_title.text()
    assert "Phosphofructokinase" in title \
        or "PFK" in title
    html = d._step_detail.toHtml()
    assert "Substrates" in html
    assert "Products" in html
    assert "Regulatory effectors" in html


def test_dialog_text_filter(app, qtbot):
    from orgchem.gui.dialogs.metabolic_pathways import (
        MetabolicPathwaysDialog,
    )
    d = MetabolicPathwaysDialog(parent=app.window)
    qtbot.addWidget(d)
    d._filter_edit.setText("urea")
    assert d._pathway_list.count() == 1


def test_dialog_no_match_blank(app, qtbot):
    from orgchem.gui.dialogs.metabolic_pathways import (
        MetabolicPathwaysDialog,
    )
    d = MetabolicPathwaysDialog(parent=app.window)
    qtbot.addWidget(d)
    d._filter_edit.setText("zzzz-no-match")
    assert d._pathway_list.count() == 0
    assert "no pathways" in d._title.text().lower()


def test_open_action_fires(app, qtbot):
    from orgchem.agent.actions import invoke
    from orgchem.gui.dialogs.metabolic_pathways import (
        MetabolicPathwaysDialog,
    )
    res = invoke("open_metabolic_pathways")
    assert res.get("opened") is True
    assert MetabolicPathwaysDialog._instance is not None


def test_open_action_with_pathway_and_step(app, qtbot):
    from orgchem.agent.actions import invoke
    res = invoke("open_metabolic_pathways",
                 pathway_id="glycolysis",
                 step_number=3)
    assert res.get("opened") is True
    assert res.get("selected_pathway") is True
    assert res.get("selected_step") is True
