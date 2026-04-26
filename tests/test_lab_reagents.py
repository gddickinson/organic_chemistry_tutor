"""Phase 45 (round 149) — headless tests for the lab-reagents
catalogue + agent actions + dialog.
"""
from __future__ import annotations
import os

import pytest


# ==================================================================
# Catalogue contents
# ==================================================================

def test_catalogue_size_at_least_fifty():
    from orgchem.core.lab_reagents import list_reagents
    assert len(list_reagents()) >= 50


def test_all_categories_represented():
    from orgchem.core.lab_reagents import (
        VALID_CATEGORIES, list_reagents,
    )
    seen = {r.category for r in list_reagents()}
    assert seen == set(VALID_CATEGORIES), \
        f"missing: {set(VALID_CATEGORIES) - seen}"


def test_user_requested_reagents_present():
    """The user-flagged catalogue brief explicitly named these
    reagent families — verify they're present."""
    from orgchem.core.lab_reagents import find_reagents
    for needle in ("tris", "hepes", "mops", "mes", "pbs",
                   "tbs", "sds", "triton", "tween", "dtt",
                   "tcep", "edta", "bsa", "coomassie",
                   "ethidium", "dmso", "dmf", "dmem",
                   "rpmi", "trypsin", "agarose", "taq",
                   "ecori", "rnase"):
        hits = find_reagents(needle)
        assert hits, f"no reagent hit for needle {needle!r}"


def test_every_entry_has_required_fields():
    from orgchem.core.lab_reagents import list_reagents
    for r in list_reagents():
        for fname in ("id", "name", "category",
                      "typical_concentration", "storage",
                      "hazards", "preparation_notes",
                      "cas_number", "typical_usage"):
            assert getattr(r, fname), \
                f"missing {fname} on {r.id}"


def test_every_id_unique():
    from orgchem.core.lab_reagents import list_reagents
    ids = [r.id for r in list_reagents()]
    assert len(ids) == len(set(ids)), \
        f"duplicate ids: {[i for i in ids if ids.count(i) > 1]}"


def test_every_id_lowercase_kebab():
    """Ids should be lowercase + hyphens / digits — no
    underscores or upper-case letters (so they're URL- and
    cli-friendly)."""
    from orgchem.core.lab_reagents import list_reagents
    import re
    pat = re.compile(r"^[a-z0-9][a-z0-9-]*$")
    for r in list_reagents():
        assert pat.match(r.id), f"bad id {r.id!r}"


# ---- Per-row teaching invariants ------------------------------

def test_tris_has_correct_cas():
    from orgchem.core.lab_reagents import get_reagent
    r = get_reagent("tris-hcl")
    assert r is not None
    assert r.cas_number == "77-86-1"
    assert r.category == "buffer"


def test_hepes_pka_mentioned():
    """HEPES card should mention its pKa near 7.55 — that's
    the headline teaching fact about it."""
    from orgchem.core.lab_reagents import get_reagent
    r = get_reagent("hepes")
    body = (r.typical_usage + " " + r.notes).lower()
    assert "pka" in body or "ph" in body


def test_sds_describes_anionic_or_denaturing():
    from orgchem.core.lab_reagents import get_reagent
    r = get_reagent("sds")
    body = (r.preparation_notes + " " + r.typical_usage
            + " " + r.notes).lower()
    assert "anionic" in body or "denatur" in body


def test_triton_x100_non_ionic():
    from orgchem.core.lab_reagents import get_reagent
    r = get_reagent("triton-x100")
    body = r.preparation_notes.lower()
    assert "non-ionic" in body or "nonionic" in body


def test_dtt_has_dithiothreitol_in_name():
    from orgchem.core.lab_reagents import get_reagent
    r = get_reagent("dtt")
    assert "dithiothreitol" in r.name.lower()


def test_tcep_described_as_odourless_or_stable():
    """TCEP is the modern DTT replacement — its key advantage
    over DTT (no smell, more stable) should be in the card."""
    from orgchem.core.lab_reagents import get_reagent
    r = get_reagent("tcep")
    body = (r.storage + " " + r.typical_usage
            + " " + r.notes).lower()
    assert ("odourless" in body or "odorless" in body
            or "stable" in body or "ms-friendly" in body)


def test_dmso_freezing_point_warning():
    """The DMSO card must warn about freezing at ~18 °C —
    a classic gotcha when working at low room temperature."""
    from orgchem.core.lab_reagents import get_reagent
    r = get_reagent("dmso")
    body = (r.storage + " " + r.preparation_notes).lower()
    assert "18" in body or "freez" in body or "rewarm" in body


def test_ethidium_bromide_mutagen_warning():
    from orgchem.core.lab_reagents import get_reagent
    r = get_reagent("ethidium-bromide")
    body = r.hazards.lower()
    assert "mutagen" in body or "carcinogen" in body


def test_taq_polymerase_no_proofreading():
    from orgchem.core.lab_reagents import get_reagent
    r = get_reagent("taq-polymerase")
    body = (r.typical_usage + " " + r.notes).lower()
    assert ("proof" in body or "error" in body
            or "ta cloning" in body)


def test_phusion_high_fidelity():
    from orgchem.core.lab_reagents import get_reagent
    r = get_reagent("phusion-polymerase")
    body = (r.typical_usage + " " + r.notes).lower()
    assert "fidelity" in body or "blunt" in body


def test_dmem_mentions_supplements():
    """The DMEM card should walk a user through the standard
    10 % FBS / Pen-Strep / glutamine supplementation."""
    from orgchem.core.lab_reagents import get_reagent
    r = get_reagent("dmem")
    body = (r.preparation_notes + " " + r.typical_usage).lower()
    assert "fbs" in body or "serum" in body or "pen-strep" in body


def test_buffer_category_includes_goods_buffers():
    """All 7 Good's buffers from Phase 46c should appear as
    reagent entries (HEPES / MES / MOPS / BIS-TRIS / Tris-HCl
    / PBS / TBS)."""
    from orgchem.core.lab_reagents import list_reagents
    buffer_ids = {r.id for r in list_reagents("buffer")}
    for must_have in ("tris-hcl", "hepes", "mops", "mes",
                      "pbs", "tbs", "bis-tris"):
        assert must_have in buffer_ids, \
            f"buffer category missing {must_have}"


def test_solvent_category_covers_common_solvents():
    from orgchem.core.lab_reagents import list_reagents
    solvent_ids = {r.id for r in list_reagents("solvent")}
    for must_have in ("dmso", "ethanol", "methanol", "acetone",
                      "chloroform", "acetonitrile"):
        assert must_have in solvent_ids, \
            f"solvent category missing {must_have}"


# ---- Filter / lookup ------------------------------------------

def test_list_filtered_by_category():
    from orgchem.core.lab_reagents import list_reagents
    detergents = list_reagents(category="detergent")
    assert all(r.category == "detergent" for r in detergents)
    assert len(detergents) >= 5


def test_list_unknown_category_returns_empty():
    from orgchem.core.lab_reagents import list_reagents
    assert list_reagents(category="not-a-real-category") == []


def test_get_unknown_id_returns_none():
    from orgchem.core.lab_reagents import get_reagent
    assert get_reagent("does-not-exist") is None


def test_find_substring_case_insensitive():
    from orgchem.core.lab_reagents import find_reagents
    a = {r.id for r in find_reagents("TRIS")}
    b = {r.id for r in find_reagents("tris")}
    assert a == b
    assert "tris-hcl" in a


def test_find_empty_returns_empty():
    from orgchem.core.lab_reagents import find_reagents
    assert find_reagents("") == []


def test_find_by_cas():
    """CAS numbers should be searchable (a common use-case
    when you know the CAS but not the name)."""
    from orgchem.core.lab_reagents import find_reagents
    hits = find_reagents("67-68-5")
    assert any(r.id == "dmso" for r in hits)


def test_categories_returns_canonical_tuple():
    from orgchem.core.lab_reagents import (
        VALID_CATEGORIES, categories,
    )
    assert categories() == VALID_CATEGORIES


# ---- reagent_to_dict serialisation ----------------------------

def test_reagent_to_dict_keys():
    from orgchem.core.lab_reagents import (
        get_reagent, reagent_to_dict,
    )
    d = reagent_to_dict(get_reagent("hepes"))
    expected = {
        "id", "name", "category", "typical_concentration",
        "storage", "hazards", "preparation_notes",
        "cas_number", "typical_usage", "notes",
    }
    assert set(d.keys()) == expected
    assert d["name"] == "HEPES"


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


def test_action_list_reagents(app):
    rows = app.call("list_lab_reagents")
    assert len(rows) >= 50


def test_action_list_reagents_filtered(app):
    rows = app.call("list_lab_reagents", category="solvent")
    assert all(r["category"] == "solvent" for r in rows)
    assert len(rows) >= 5


def test_action_list_reagents_unknown_category(app):
    rows = app.call("list_lab_reagents", category="bogus")
    assert "error" in rows[0]


def test_action_get_reagent(app):
    r = app.call("get_lab_reagent", reagent_id="tris-hcl")
    assert "error" not in r
    assert r["cas_number"] == "77-86-1"


def test_action_get_unknown_reagent(app):
    r = app.call("get_lab_reagent", reagent_id="bogus")
    assert "error" in r


def test_action_find_reagents(app):
    rows = app.call("find_lab_reagents", needle="tris")
    ids = {r["id"] for r in rows}
    assert "tris-hcl" in ids
    assert "tbs" in ids


# ==================================================================
# Dialog
# ==================================================================

@pytest.fixture(autouse=True)
def _reset_singleton():
    from orgchem.gui.dialogs import lab_reagents as mod
    mod.LabReagentsDialog._instance = None
    yield
    mod.LabReagentsDialog._instance = None


def test_dialog_constructs(app, qtbot):
    from orgchem.gui.dialogs.lab_reagents import (
        LabReagentsDialog,
    )
    d = LabReagentsDialog(parent=app.window)
    qtbot.addWidget(d)
    assert d._list.count() >= 50


def test_dialog_singleton(app):
    from orgchem.gui.dialogs.lab_reagents import (
        LabReagentsDialog,
    )
    a = LabReagentsDialog.singleton(parent=app.window)
    b = LabReagentsDialog.singleton(parent=app.window)
    assert a is b


def test_dialog_category_combo_filters(app, qtbot):
    from orgchem.gui.dialogs.lab_reagents import (
        LabReagentsDialog,
    )
    d = LabReagentsDialog(parent=app.window)
    qtbot.addWidget(d)
    idx = d._cat_combo.findText("buffer")
    assert idx >= 0
    d._cat_combo.setCurrentIndex(idx)
    assert d._list.count() >= 7


def test_dialog_text_filter(app, qtbot):
    from orgchem.gui.dialogs.lab_reagents import (
        LabReagentsDialog,
    )
    d = LabReagentsDialog(parent=app.window)
    qtbot.addWidget(d)
    d._filter_edit.setText("Tris")
    assert d._list.count() >= 2


def test_dialog_filter_no_match(app, qtbot):
    from orgchem.gui.dialogs.lab_reagents import (
        LabReagentsDialog,
    )
    d = LabReagentsDialog(parent=app.window)
    qtbot.addWidget(d)
    d._filter_edit.setText("zzzz-no-match")
    assert d._list.count() == 0
    assert "no reagents" in d._title.text().lower()


def test_dialog_select_reagent(app, qtbot):
    from orgchem.gui.dialogs.lab_reagents import (
        LabReagentsDialog,
    )
    d = LabReagentsDialog(parent=app.window)
    qtbot.addWidget(d)
    ok = d.select_reagent("hepes")
    assert ok is True
    assert "HEPES" in d._title.text()


def test_dialog_select_unknown_reagent(app, qtbot):
    from orgchem.gui.dialogs.lab_reagents import (
        LabReagentsDialog,
    )
    d = LabReagentsDialog(parent=app.window)
    qtbot.addWidget(d)
    assert d.select_reagent("does-not-exist") is False


def test_dialog_default_first_row_selected(app, qtbot):
    from orgchem.gui.dialogs.lab_reagents import (
        LabReagentsDialog,
    )
    d = LabReagentsDialog(parent=app.window)
    qtbot.addWidget(d)
    title = d._title.text()
    assert "Select" not in title
    html = d._detail.toHtml()
    for section in ("Typical concentration", "Storage",
                    "Hazards", "Preparation notes",
                    "Typical usage"):
        assert section in html


def test_dialog_detail_has_cas_in_meta(app, qtbot):
    from orgchem.gui.dialogs.lab_reagents import (
        LabReagentsDialog,
    )
    d = LabReagentsDialog(parent=app.window)
    qtbot.addWidget(d)
    d.select_reagent("dmso")
    meta = d._meta.text()
    assert "67-68-5" in meta


# ---- agent action open path -----------------------------------

def test_open_action_fires(app, qtbot):
    from orgchem.agent.actions import invoke
    from orgchem.gui.dialogs.lab_reagents import (
        LabReagentsDialog,
    )
    res = invoke("open_lab_reagents")
    assert res.get("opened") is True
    assert LabReagentsDialog._instance is not None


def test_open_action_with_id(app, qtbot):
    from orgchem.agent.actions import invoke
    res = invoke("open_lab_reagents", reagent_id="hepes")
    assert res.get("opened") is True
    assert res.get("selected") is True


def test_open_action_with_unknown_id(app, qtbot):
    from orgchem.agent.actions import invoke
    res = invoke("open_lab_reagents", reagent_id="bogus")
    assert res.get("opened") is True
    assert res.get("selected") is False
