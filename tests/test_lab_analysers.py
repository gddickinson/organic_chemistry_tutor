"""Phase 40a (round 146) — headless tests for the major lab
analysers catalogue + agent actions + dialog.
"""
from __future__ import annotations
import os

import pytest


# ==================================================================
# Catalogue contents
# ==================================================================

def test_catalogue_size_at_least_twenty_five():
    from orgchem.core.lab_analysers import list_analysers
    assert len(list_analysers()) >= 25


def test_all_categories_represented():
    from orgchem.core.lab_analysers import (
        VALID_CATEGORIES, list_analysers,
    )
    seen = {a.category for a in list_analysers()}
    assert seen == set(VALID_CATEGORIES), \
        f"missing: {set(VALID_CATEGORIES) - seen}"


def test_user_requested_systems_present():
    """The user-flagged catalogue brief explicitly named these
    instrument families — verify they're present."""
    from orgchem.core.lab_analysers import find_analysers
    # Each substring should hit at least one entry.
    for needle in ("cobas", "atellica", "sysmex", "stago",
                   "alinity", "panther", "genexpert",
                   "novaseq", "nanopore", "biotyper",
                   "flipr", "krios", "hamilton", "tecan"):
        hits = find_analysers(needle)
        assert hits, f"no analyser hit for needle {needle!r}"


def test_every_entry_has_required_fields():
    from orgchem.core.lab_analysers import list_analysers
    for a in list_analysers():
        for fname in ("id", "name", "manufacturer", "category",
                      "function", "typical_throughput",
                      "sample_volume", "detection_method",
                      "typical_assays", "strengths",
                      "limitations"):
            assert getattr(a, fname), \
                f"missing {fname} on {a.id}"


def test_every_id_unique():
    from orgchem.core.lab_analysers import list_analysers
    ids = [a.id for a in list_analysers()]
    assert len(ids) == len(set(ids)), \
        f"duplicate ids: {[i for i in ids if ids.count(i) > 1]}"


# ---- Per-row teaching invariants -----------------------------

def test_cobas_c702_clinical_chemistry():
    """The Roche cobas c 702 must run BMP / CMP-style assays
    (the link between Phase 37b clinical lab panels + Phase
    40a analysers)."""
    from orgchem.core.lab_analysers import get_analyser
    c = get_analyser("cobas_c702")
    assert c is not None
    assert c.category == "clinical-chemistry"
    body = (c.typical_assays + " " + c.strengths).lower()
    assert "bmp" in body or "panel" in body


def test_sysmex_xn1000_hematology():
    """Sysmex XN-series should describe CBC + 5-part diff."""
    from orgchem.core.lab_analysers import get_analyser
    s = get_analyser("sysmex_xn1000")
    body = (s.function + " " + s.typical_assays).lower()
    assert ("cbc" in body or "differential" in body)


def test_genexpert_describes_cartridge_format():
    from orgchem.core.lab_analysers import get_analyser
    g = get_analyser("cepheid_genexpert")
    body = (g.function + " " + g.detection_method).lower()
    assert "cartridge" in body


def test_novaseq_throughput_in_terabases():
    from orgchem.core.lab_analysers import get_analyser
    n = get_analyser("illumina_novaseq_x")
    assert "tbp" in n.typical_throughput.lower() \
        or "tb" in n.typical_throughput.lower()


def test_nanopore_describes_long_reads():
    from orgchem.core.lab_analysers import get_analyser
    n = get_analyser("oxford_promethion")
    body = (n.strengths + " " + n.typical_assays).lower()
    assert "long" in body or "read" in body


def test_flipr_describes_calcium_or_membrane_potential():
    from orgchem.core.lab_analysers import get_analyser
    f = get_analyser("flipr_penta")
    body = (f.function + " " + f.typical_assays).lower()
    assert "ca" in body or "calcium" in body \
        or "membrane potential" in body


def test_krios_describes_cryo_em_or_single_particle():
    from orgchem.core.lab_analysers import get_analyser
    k = get_analyser("thermo_krios_g4")
    body = (k.function + " " + k.typical_assays).lower()
    assert "cryo" in body or "single-particle" in body \
        or "spa" in body


def test_opentrons_lower_cost_than_hamilton():
    """Opentrons OT-2 limitations / strengths should call out
    its capital-cost advantage."""
    from orgchem.core.lab_analysers import get_analyser
    o = get_analyser("opentrons_ot2")
    body = (o.strengths + " " + o.notes).lower()
    assert ("$10-15k" in body or "10-15" in body
            or "academic" in body or "open-source" in body)


# ---- Filter / lookup ------------------------------------------

def test_list_filtered_by_category():
    from orgchem.core.lab_analysers import list_analysers
    mol = list_analysers(category="molecular")
    assert all(a.category == "molecular" for a in mol)
    assert len(mol) >= 4   # cobas 8800 + Panther + GeneXpert
                           # + NovaSeq + Nanopore = 5


def test_list_unknown_category_returns_empty():
    from orgchem.core.lab_analysers import list_analysers
    assert list_analysers(category="not-a-real-category") == []


def test_get_unknown_id_returns_none():
    from orgchem.core.lab_analysers import get_analyser
    assert get_analyser("does-not-exist") is None


def test_find_substring_case_insensitive():
    from orgchem.core.lab_analysers import find_analysers
    a = {x.id for x in find_analysers("ROCHE")}
    b = {x.id for x in find_analysers("roche")}
    assert a == b
    assert "cobas_c702" in a and "cobas_e801" in a


def test_find_empty_returns_empty():
    from orgchem.core.lab_analysers import find_analysers
    assert find_analysers("") == []


# ---- to_dict serialisation ------------------------------------

def test_to_dict_keys():
    from orgchem.core.lab_analysers import (
        get_analyser, to_dict,
    )
    d = to_dict(get_analyser("cobas_c702"))
    expected = {
        "id", "name", "manufacturer", "category", "function",
        "typical_throughput", "sample_volume",
        "detection_method", "typical_assays", "strengths",
        "limitations", "notes",
    }
    assert set(d.keys()) == expected


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


def test_action_list_analysers(app):
    rows = app.call("list_lab_analysers")
    assert len(rows) >= 25


def test_action_list_analysers_filtered(app):
    rows = app.call("list_lab_analysers", category="molecular")
    assert all(r["category"] == "molecular" for r in rows)


def test_action_list_analysers_unknown_category(app):
    rows = app.call("list_lab_analysers", category="bogus")
    assert "error" in rows[0]


def test_action_get_analyser(app):
    r = app.call("get_lab_analyser", analyser_id="cobas_c702")
    assert "error" not in r
    assert r["manufacturer"] == "Roche Diagnostics"


def test_action_get_unknown_analyser(app):
    r = app.call("get_lab_analyser", analyser_id="bogus")
    assert "error" in r


def test_action_find_analysers(app):
    rows = app.call("find_lab_analysers", needle="sysmex")
    ids = {r["id"] for r in rows}
    assert "sysmex_xn1000" in ids
    assert "sysmex_cs5100" in ids


# ==================================================================
# Dialog
# ==================================================================

@pytest.fixture(autouse=True)
def _reset_singleton():
    from orgchem.gui.dialogs import lab_analysers as mod
    mod.LabAnalysersDialog._instance = None
    yield
    mod.LabAnalysersDialog._instance = None


def test_dialog_constructs(app, qtbot):
    from orgchem.gui.dialogs.lab_analysers import (
        LabAnalysersDialog,
    )
    d = LabAnalysersDialog(parent=app.window)
    qtbot.addWidget(d)
    assert d._list.count() >= 25


def test_dialog_singleton(app):
    from orgchem.gui.dialogs.lab_analysers import (
        LabAnalysersDialog,
    )
    a = LabAnalysersDialog.singleton(parent=app.window)
    b = LabAnalysersDialog.singleton(parent=app.window)
    assert a is b


def test_dialog_category_combo_filters(app, qtbot):
    from orgchem.gui.dialogs.lab_analysers import (
        LabAnalysersDialog,
    )
    d = LabAnalysersDialog(parent=app.window)
    qtbot.addWidget(d)
    # Switch to molecular only.
    idx = d._cat_combo.findText("molecular")
    assert idx >= 0
    d._cat_combo.setCurrentIndex(idx)
    assert d._list.count() >= 4


def test_dialog_text_filter(app, qtbot):
    from orgchem.gui.dialogs.lab_analysers import (
        LabAnalysersDialog,
    )
    d = LabAnalysersDialog(parent=app.window)
    qtbot.addWidget(d)
    d._filter_edit.setText("Roche")
    assert d._list.count() >= 2   # cobas c702 + e801 + 8800


def test_dialog_filter_no_match(app, qtbot):
    from orgchem.gui.dialogs.lab_analysers import (
        LabAnalysersDialog,
    )
    d = LabAnalysersDialog(parent=app.window)
    qtbot.addWidget(d)
    d._filter_edit.setText("zzzz-no-match")
    assert d._list.count() == 0
    assert "no analysers" in d._title.text().lower()


def test_dialog_select_analyser(app, qtbot):
    from orgchem.gui.dialogs.lab_analysers import (
        LabAnalysersDialog,
    )
    d = LabAnalysersDialog(parent=app.window)
    qtbot.addWidget(d)
    ok = d.select_analyser("illumina_novaseq_x")
    assert ok is True
    assert "NovaSeq" in d._title.text()


def test_dialog_select_unknown_analyser(app, qtbot):
    from orgchem.gui.dialogs.lab_analysers import (
        LabAnalysersDialog,
    )
    d = LabAnalysersDialog(parent=app.window)
    qtbot.addWidget(d)
    assert d.select_analyser("does-not-exist") is False


def test_dialog_default_first_row_selected(app, qtbot):
    from orgchem.gui.dialogs.lab_analysers import (
        LabAnalysersDialog,
    )
    d = LabAnalysersDialog(parent=app.window)
    qtbot.addWidget(d)
    title = d._title.text()
    assert "Select" not in title
    html = d._detail.toHtml()
    for section in ("Function", "Typical throughput",
                    "Sample", "Detection method",
                    "Strengths"):
        assert section in html


# ---- agent action open path ----------------------------------

def test_open_action_fires(app, qtbot):
    from orgchem.agent.actions import invoke
    from orgchem.gui.dialogs.lab_analysers import (
        LabAnalysersDialog,
    )
    res = invoke("open_lab_analysers")
    assert res.get("opened") is True
    assert LabAnalysersDialog._instance is not None


def test_open_action_with_id(app, qtbot):
    from orgchem.agent.actions import invoke
    res = invoke("open_lab_analysers",
                 analyser_id="thermo_krios_g4")
    assert res.get("opened") is True
    assert res.get("selected") is True
