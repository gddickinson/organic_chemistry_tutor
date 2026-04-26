"""Phase 44 (round 150) — headless tests for the microscopy
techniques catalogue + agent actions + dialog.
"""
from __future__ import annotations
import os

import pytest


# ==================================================================
# Catalogue contents
# ==================================================================

def test_catalogue_size_at_least_twenty_five():
    from orgchem.core.microscopy import list_methods
    assert len(list_methods()) >= 25


def test_all_resolution_scales_represented():
    from orgchem.core.microscopy import (
        RESOLUTION_SCALES, list_methods,
    )
    seen = {m.resolution_scale for m in list_methods()}
    assert seen == set(RESOLUTION_SCALES), \
        f"missing: {set(RESOLUTION_SCALES) - seen}"


def test_user_requested_methods_present():
    """The user-flagged catalogue brief explicitly named these
    method families."""
    from orgchem.core.microscopy import find_methods
    for needle in ("stereo", "intravital", "OCT",
                   "histology", "light-sheet", "confocal",
                   "two-photon", "SIM", "STORM", "PALM",
                   "STED", "TIRF", "smFRET", "cryo-EM",
                   "AFM", "STM", "frozen", "IHC",
                   "digital-pathology"):
        hits = find_methods(needle)
        assert hits, f"no method hit for needle {needle!r}"


def test_every_entry_has_required_fields():
    from orgchem.core.microscopy import list_methods
    for m in list_methods():
        for fname in ("id", "name", "abbreviation",
                      "resolution_scale", "typical_resolution",
                      "light_source", "contrast_mechanism",
                      "typical_uses", "strengths",
                      "limitations",
                      "representative_instruments"):
            assert getattr(m, fname), \
                f"missing {fname} on {m.id}"
        assert m.sample_types, \
            f"empty sample_types on {m.id}"


def test_every_id_unique():
    from orgchem.core.microscopy import list_methods
    ids = [m.id for m in list_methods()]
    assert len(ids) == len(set(ids)), \
        f"duplicate ids: {[i for i in ids if ids.count(i) > 1]}"


def test_every_id_lowercase_kebab():
    from orgchem.core.microscopy import list_methods
    import re
    pat = re.compile(r"^[a-z0-9][a-z0-9-]*$")
    for m in list_methods():
        assert pat.match(m.id), f"bad id {m.id!r}"


def test_every_sample_type_in_canonical_set():
    from orgchem.core.microscopy import (
        SAMPLE_TYPES, list_methods,
    )
    sset = set(SAMPLE_TYPES)
    for m in list_methods():
        for s in m.sample_types:
            assert s in sset, \
                f"unknown sample type {s!r} on {m.id}"


def test_every_resolution_scale_in_canonical_set():
    from orgchem.core.microscopy import (
        RESOLUTION_SCALES, list_methods,
    )
    rset = set(RESOLUTION_SCALES)
    for m in list_methods():
        assert m.resolution_scale in rset, \
            f"unknown scale {m.resolution_scale!r} on {m.id}"


# ---- Per-row teaching invariants -----------------------------

def test_confocal_describes_pinhole():
    from orgchem.core.microscopy import get_method
    m = get_method("confocal")
    body = (m.contrast_mechanism + " " + m.strengths).lower()
    assert "pinhole" in body or "sectioning" in body


def test_storm_resolution_in_nm():
    """STORM is the gold-standard ~ 20 nm fluorescence
    resolution claim."""
    from orgchem.core.microscopy import get_method
    m = get_method("storm")
    assert "nm" in m.typical_resolution


def test_cryo_em_atomic_resolution():
    from orgchem.core.microscopy import get_method
    m = get_method("cryo-em")
    body = (m.typical_resolution + " " + m.strengths).lower()
    assert ("å" in body or "atomic" in body
            or "near-atomic" in body)


def test_afm_force_spectroscopy():
    from orgchem.core.microscopy import get_method
    m = get_method("afm")
    body = (m.typical_uses + " " + m.strengths).lower()
    assert "force" in body or "pn" in body


def test_stm_individual_atoms():
    from orgchem.core.microscopy import get_method
    m = get_method("stm")
    body = (m.typical_uses + " " + m.strengths
            + " " + m.notes).lower()
    assert "atom" in body


def test_frozen_section_intra_op():
    from orgchem.core.microscopy import get_method
    m = get_method("frozen-section")
    body = (m.typical_uses + " " + m.strengths).lower()
    assert ("intra-op" in body or "real-time" in body
            or "rapid" in body or "surgery" in body
            or "20 min" in body)


def test_two_photon_deep_penetration():
    from orgchem.core.microscopy import get_method
    m = get_method("two-photon")
    body = (m.typical_uses + " " + m.strengths
            + " " + m.typical_resolution).lower()
    assert "deep" in body or "500" in body or "1000" in body \
        or "penetrat" in body


def test_oct_clinical_use():
    """OCT's killer-app is ophthalmology (retinal scans)."""
    from orgchem.core.microscopy import get_method
    m = get_method("oct")
    body = (m.typical_uses + " " + m.strengths).lower()
    assert ("retina" in body or "ophthalm" in body
            or "clinical" in body)


def test_clinical_histology_scale_includes_routine_workflow():
    """The clinical-histology scale should include the
    pathology workhorse + frozen-section + IHC + WSI."""
    from orgchem.core.microscopy import list_methods
    ids = {m.id for m in list_methods("clinical-histology")}
    for must_have in ("clinical-light-microscope",
                      "frozen-section", "ihc-clinical",
                      "digital-pathology-scanner"):
        assert must_have in ids, \
            f"clinical-histology missing {must_have}"


def test_super_resolution_methods_grouped_in_subcellular():
    """SIM / STORM / PALM / STED / Airyscan / TIRF — the
    super-resolution + membrane-evanescent methods —
    should land in 'sub-cellular'."""
    from orgchem.core.microscopy import list_methods
    ids = {m.id for m in list_methods("sub-cellular")}
    for must_have in ("sim", "storm", "palm", "sted",
                      "airyscan", "tirf"):
        assert must_have in ids, \
            f"sub-cellular missing {must_have}"


def test_single_molecule_includes_smfret_and_cryo():
    from orgchem.core.microscopy import list_methods
    ids = {m.id for m in list_methods("single-molecule")}
    for must_have in ("smfret", "cryo-em", "cryo-et", "afm",
                      "stm"):
        assert must_have in ids, \
            f"single-molecule missing {must_have}"


# ---- Cross-references to Phase 40a lab-analysers --------------

def test_cryo_em_xrefs_krios():
    """cryo-EM should cross-reference the Phase-40a Krios
    lab-analyser entry."""
    from orgchem.core.microscopy import get_method
    m = get_method("cryo-em")
    assert "thermo_krios_g4" in m.cross_reference_lab_analyser_ids


def test_xrefs_resolve_to_real_lab_analyser_ids():
    """Every cross-referenced lab_analyser_id must exist in
    the Phase-40a catalogue — guard against rot."""
    from orgchem.core.microscopy import list_methods
    from orgchem.core.lab_analysers import (
        get_analyser, list_analysers,
    )
    valid = {a.id for a in list_analysers()}
    for m in list_methods():
        for xref in m.cross_reference_lab_analyser_ids:
            assert xref in valid, \
                f"{m.id} xrefs unknown analyser {xref!r}; " \
                f"valid: {sorted(valid)}"


# ---- Filter / lookup ------------------------------------------

def test_list_filtered_by_scale():
    from orgchem.core.microscopy import list_methods
    cell = list_methods("cellular")
    assert all(m.resolution_scale == "cellular" for m in cell)
    assert len(cell) >= 5


def test_list_unknown_scale_returns_empty():
    from orgchem.core.microscopy import list_methods
    assert list_methods("not-a-real-scale") == []


def test_get_unknown_id_returns_none():
    from orgchem.core.microscopy import get_method
    assert get_method("does-not-exist") is None


def test_find_substring_case_insensitive():
    from orgchem.core.microscopy import find_methods
    a = {m.id for m in find_methods("CONFOCAL")}
    b = {m.id for m in find_methods("confocal")}
    assert a == b
    assert "confocal" in a


def test_find_empty_returns_empty():
    from orgchem.core.microscopy import find_methods
    assert find_methods("") == []


def test_methods_for_sample_type_live_cells():
    from orgchem.core.microscopy import methods_for_sample_type
    live = methods_for_sample_type("live-cells")
    ids = {m.id for m in live}
    for must_have in ("phase-contrast", "widefield-epifluorescence",
                      "spinning-disk-confocal", "two-photon",
                      "tirf"):
        assert must_have in ids, \
            f"live-cells missing {must_have}"


def test_methods_for_sample_type_unknown_returns_empty():
    from orgchem.core.microscopy import methods_for_sample_type
    assert methods_for_sample_type("not-a-real-sample") == []


def test_resolution_scales_canonical_order():
    """Coarsest → finest; clinical-histology slotted at end
    (it's a workflow, not a scale)."""
    from orgchem.core.microscopy import resolution_scales
    s = resolution_scales()
    assert s[0] == "whole-organism"
    assert s[-1] == "clinical-histology"


# ---- method_to_dict serialisation ----------------------------

def test_method_to_dict_keys():
    from orgchem.core.microscopy import (
        get_method, method_to_dict,
    )
    d = method_to_dict(get_method("confocal"))
    expected = {
        "id", "name", "abbreviation", "resolution_scale",
        "sample_types", "typical_resolution", "light_source",
        "contrast_mechanism", "typical_uses", "strengths",
        "limitations", "representative_instruments",
        "cross_reference_lab_analyser_ids", "notes",
    }
    assert set(d.keys()) == expected
    # Tuple fields should serialise to tuples / lists
    # (asdict preserves tuples).
    assert isinstance(d["sample_types"], (tuple, list))


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


def test_action_list_methods(app):
    rows = app.call("list_microscopy_methods")
    assert len(rows) >= 25


def test_action_list_methods_filtered(app):
    rows = app.call("list_microscopy_methods",
                    resolution_scale="cellular")
    assert all(r["resolution_scale"] == "cellular" for r in rows)
    assert len(rows) >= 5


def test_action_list_methods_unknown_scale(app):
    rows = app.call("list_microscopy_methods",
                    resolution_scale="bogus")
    assert "error" in rows[0]


def test_action_get_method(app):
    r = app.call("get_microscopy_method", method_id="cryo-em")
    assert "error" not in r
    assert r["abbreviation"] == "cryo-EM"


def test_action_get_unknown_method(app):
    r = app.call("get_microscopy_method", method_id="bogus")
    assert "error" in r


def test_action_find_methods(app):
    rows = app.call("find_microscopy_methods", needle="confocal")
    ids = {r["id"] for r in rows}
    assert "confocal" in ids
    assert "spinning-disk-confocal" in ids


def test_action_methods_for_sample(app):
    rows = app.call("microscopy_methods_for_sample",
                    sample_type="single-molecules")
    ids = {r["id"] for r in rows}
    assert "smfret" in ids
    assert "cryo-em" in ids


def test_action_methods_for_unknown_sample(app):
    rows = app.call("microscopy_methods_for_sample",
                    sample_type="bogus-sample")
    assert "error" in rows[0]


def test_action_methods_for_empty_sample(app):
    rows = app.call("microscopy_methods_for_sample",
                    sample_type="")
    assert rows == []


# ==================================================================
# Dialog
# ==================================================================

@pytest.fixture(autouse=True)
def _reset_singleton():
    from orgchem.gui.dialogs import microscopy as mod
    mod.MicroscopyDialog._instance = None
    yield
    mod.MicroscopyDialog._instance = None


def test_dialog_constructs(app, qtbot):
    from orgchem.gui.dialogs.microscopy import MicroscopyDialog
    d = MicroscopyDialog(parent=app.window)
    qtbot.addWidget(d)
    assert d._list.count() >= 25


def test_dialog_singleton(app):
    from orgchem.gui.dialogs.microscopy import MicroscopyDialog
    a = MicroscopyDialog.singleton(parent=app.window)
    b = MicroscopyDialog.singleton(parent=app.window)
    assert a is b


def test_dialog_scale_combo_filters(app, qtbot):
    from orgchem.gui.dialogs.microscopy import MicroscopyDialog
    d = MicroscopyDialog(parent=app.window)
    qtbot.addWidget(d)
    idx = d._scale_combo.findText("sub-cellular")
    assert idx >= 0
    d._scale_combo.setCurrentIndex(idx)
    assert d._list.count() >= 6


def test_dialog_sample_combo_filters(app, qtbot):
    from orgchem.gui.dialogs.microscopy import MicroscopyDialog
    d = MicroscopyDialog(parent=app.window)
    qtbot.addWidget(d)
    idx = d._sample_combo.findText("live-cells")
    assert idx >= 0
    d._sample_combo.setCurrentIndex(idx)
    assert d._list.count() >= 5


def test_dialog_text_filter(app, qtbot):
    from orgchem.gui.dialogs.microscopy import MicroscopyDialog
    d = MicroscopyDialog(parent=app.window)
    qtbot.addWidget(d)
    d._filter_edit.setText("STED")
    assert d._list.count() >= 1


def test_dialog_filter_no_match(app, qtbot):
    from orgchem.gui.dialogs.microscopy import MicroscopyDialog
    d = MicroscopyDialog(parent=app.window)
    qtbot.addWidget(d)
    d._filter_edit.setText("zzzz-no-match")
    assert d._list.count() == 0
    assert "no methods" in d._title.text().lower()


def test_dialog_select_method(app, qtbot):
    from orgchem.gui.dialogs.microscopy import MicroscopyDialog
    d = MicroscopyDialog(parent=app.window)
    qtbot.addWidget(d)
    ok = d.select_method("cryo-em")
    assert ok is True
    assert "Cryo-electron" in d._title.text()


def test_dialog_select_unknown_method(app, qtbot):
    from orgchem.gui.dialogs.microscopy import MicroscopyDialog
    d = MicroscopyDialog(parent=app.window)
    qtbot.addWidget(d)
    assert d.select_method("does-not-exist") is False


def test_dialog_default_first_row_selected(app, qtbot):
    from orgchem.gui.dialogs.microscopy import MicroscopyDialog
    d = MicroscopyDialog(parent=app.window)
    qtbot.addWidget(d)
    title = d._title.text()
    assert "Select" not in title
    html = d._detail.toHtml()
    for section in ("Typical resolution", "Light source",
                    "Contrast mechanism", "Sample types",
                    "Strengths"):
        assert section in html


def test_dialog_xref_section_shown_for_cryo_em(app, qtbot):
    from orgchem.gui.dialogs.microscopy import MicroscopyDialog
    d = MicroscopyDialog(parent=app.window)
    qtbot.addWidget(d)
    d.select_method("cryo-em")
    html = d._detail.toHtml()
    assert "Cross-reference" in html or "thermo_krios" in html


# ---- agent action open path -----------------------------------

def test_open_action_fires(app, qtbot):
    from orgchem.agent.actions import invoke
    from orgchem.gui.dialogs.microscopy import MicroscopyDialog
    res = invoke("open_microscopy")
    assert res.get("opened") is True
    assert MicroscopyDialog._instance is not None


def test_open_action_with_id(app, qtbot):
    from orgchem.agent.actions import invoke
    res = invoke("open_microscopy", method_id="storm")
    assert res.get("opened") is True
    assert res.get("selected") is True


def test_open_action_with_unknown_id(app, qtbot):
    from orgchem.agent.actions import invoke
    res = invoke("open_microscopy", method_id="bogus")
    assert res.get("opened") is True
    assert res.get("selected") is False
