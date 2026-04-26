"""Phase 46 (round 148) — headless tests for the pH +
buffer explorer catalogue + solvers + agent actions + dialog.
"""
from __future__ import annotations
import math
import os

import pytest


# ==================================================================
# pKa catalogue
# ==================================================================

class TestPkaCatalogue:
    def test_size_at_least_forty(self):
        from orgchem.core.ph_explorer import list_acids
        assert len(list_acids()) >= 40

    def test_seven_categories_represented(self):
        from orgchem.core.ph_explorer import (
            VALID_CATEGORIES, list_acids,
        )
        seen = {a.category for a in list_acids()}
        assert seen == set(VALID_CATEGORIES)

    def test_canonical_acids_present(self):
        from orgchem.core.ph_explorer import get_acid
        for must in ("hcl", "h2so4", "h3po4", "h2co3",
                     "acetic", "citric", "nh4",
                     "histidine", "tris", "hepes", "mes",
                     "mops", "phenol"):
            assert get_acid(must) is not None, must

    def test_polyprotic_acids_have_multiple_pkas(self):
        from orgchem.core.ph_explorer import get_acid
        # H₃PO₄ → 3 pKa values
        assert len(get_acid("h3po4").pka_values) == 3
        # Citric → 3 pKa values
        assert len(get_acid("citric").pka_values) == 3
        # H₂CO₃ → 2
        assert len(get_acid("h2co3").pka_values) == 2

    def test_acetic_acid_pka_4_76(self):
        from orgchem.core.ph_explorer import get_acid
        a = get_acid("acetic")
        assert math.isclose(a.pka_values[0], 4.76, abs_tol=0.01)

    def test_histidine_imidazole_near_physiological(self):
        """Histidine R-group pKa ≈ 6 — the canonical
        active-site acid-base catalyst at physiological pH."""
        from orgchem.core.ph_explorer import get_acid
        h = get_acid("histidine")
        assert len(h.pka_values) == 3   # α-COOH, α-NH3+, R
        # R-group pKa is the third value.
        assert math.isclose(h.pka_values[2], 6.00, abs_tol=0.1)

    def test_amino_acid_pkas_match_canonical(self):
        """A handful of textbook pKa values for spot-check."""
        from orgchem.core.ph_explorer import get_acid
        gly = get_acid("glycine")
        assert math.isclose(gly.pka_values[0], 2.34, abs_tol=0.05)
        assert math.isclose(gly.pka_values[1], 9.60, abs_tol=0.05)
        lys = get_acid("lysine")
        assert math.isclose(lys.pka_values[2], 10.79,
                            abs_tol=0.05)

    def test_tris_pka_8_1(self):
        """Tris at 25 °C has pKa 8.10 — the canonical pH 7-9
        biology buffer."""
        from orgchem.core.ph_explorer import get_acid
        t = get_acid("tris")
        assert math.isclose(t.pka_values[0], 8.10, abs_tol=0.05)

    def test_filter_by_category(self):
        from orgchem.core.ph_explorer import list_acids
        bio = list_acids(category="biological-buffer")
        assert all(a.category == "biological-buffer"
                   for a in bio)
        assert len(bio) >= 5   # MES + BIS-TRIS + PIPES +
                                # MOPS + HEPES + Tris + CHES

    def test_unknown_category_returns_empty(self):
        from orgchem.core.ph_explorer import list_acids
        assert list_acids(category="bogus") == []

    def test_get_unknown_returns_none(self):
        from orgchem.core.ph_explorer import get_acid
        assert get_acid("does-not-exist") is None

    def test_find_substring(self):
        from orgchem.core.ph_explorer import find_acids
        rows = find_acids("acetic")
        assert any(r.id == "acetic" for r in rows)


# ==================================================================
# Reference cards
# ==================================================================

class TestReferenceCards:
    def test_six_cards_present(self):
        from orgchem.core.ph_explorer import REFERENCE_CARDS
        assert len(REFERENCE_CARDS) == 6

    def test_canonical_topics_present(self):
        from orgchem.core.ph_explorer import (
            list_reference_cards,
        )
        ids = {c.id for c in list_reference_cards()}
        assert "ph_definition" in ids
        assert "henderson_hasselbalch" in ids
        assert "buffer_capacity" in ids
        assert "polyprotic" in ids
        assert "biological_buffers" in ids

    def test_get_card_by_id(self):
        from orgchem.core.ph_explorer import get_reference_card
        c = get_reference_card("henderson_hasselbalch")
        assert c is not None
        assert "Henderson" in c.title
        assert "pKa" in c.body_html


# ==================================================================
# Buffer designer
# ==================================================================

class TestDesignBuffer:
    def test_pH_equals_pKa_gives_unity_ratio(self):
        """At target pH = pKa, [A⁻] / [HA] = 1, so each
        species is exactly half the total concentration."""
        from orgchem.core.ph_explorer import design_buffer
        r = design_buffer(target_pH=4.76, pKa=4.76,
                          total_concentration_M=0.1)
        assert math.isclose(r["base_acid_ratio"], 1.0,
                            rel_tol=1e-9)
        assert math.isclose(r["acid_concentration_M"], 0.05,
                            rel_tol=1e-9)
        assert math.isclose(r["base_concentration_M"], 0.05,
                            rel_tol=1e-9)
        assert r["capacity_warning"] is False

    def test_phosphate_buffer_pH_7_4(self):
        """Phosphate (pKa 7.20) at pH 7.4: ratio = 10^0.2 ≈
        1.585, so [HA]/[A-] split is 38.7 mM / 61.3 mM at
        100 mM total."""
        from orgchem.core.ph_explorer import design_buffer
        r = design_buffer(target_pH=7.4, pKa=7.20,
                          total_concentration_M=0.1)
        assert math.isclose(r["base_acid_ratio"],
                            10 ** 0.2, rel_tol=1e-6)
        assert math.isclose(
            r["acid_concentration_M"] * 1000, 38.7,
            abs_tol=0.5)
        assert math.isclose(
            r["base_concentration_M"] * 1000, 61.3,
            abs_tol=0.5)
        assert r["capacity_warning"] is False

    def test_far_from_pka_warns(self):
        """Target pH 7.0 with pKa 4.76 → 2.24 units off →
        capacity warning."""
        from orgchem.core.ph_explorer import design_buffer
        r = design_buffer(target_pH=7.0, pKa=4.76,
                          total_concentration_M=0.1)
        assert r["capacity_warning"] is True
        assert "capacity" in r["capacity_message"].lower()

    def test_acid_plus_base_equals_total(self):
        from orgchem.core.ph_explorer import design_buffer
        r = design_buffer(target_pH=5.5, pKa=4.76,
                          total_concentration_M=0.2)
        total = (r["acid_concentration_M"]
                 + r["base_concentration_M"])
        assert math.isclose(total, 0.2, rel_tol=1e-9)

    def test_moles_track_volume(self):
        from orgchem.core.ph_explorer import design_buffer
        r1 = design_buffer(target_pH=7.4, pKa=7.20,
                           total_concentration_M=0.1,
                           volume_L=1.0)
        r2 = design_buffer(target_pH=7.4, pKa=7.20,
                           total_concentration_M=0.1,
                           volume_L=2.0)
        assert math.isclose(r2["acid_moles"],
                            r1["acid_moles"] * 2,
                            rel_tol=1e-9)

    def test_rejects_zero_concentration(self):
        from orgchem.core.ph_explorer import design_buffer
        with pytest.raises(ValueError):
            design_buffer(target_pH=7.0, pKa=7.0,
                          total_concentration_M=0.0)

    def test_rejects_zero_volume(self):
        from orgchem.core.ph_explorer import design_buffer
        with pytest.raises(ValueError):
            design_buffer(target_pH=7.0, pKa=7.0,
                          total_concentration_M=0.1,
                          volume_L=0.0)


# ==================================================================
# Buffer capacity
# ==================================================================

class TestBufferCapacity:
    def test_max_at_pH_equals_pKa(self):
        """β reaches max β = 0.576 · C_total at pH = pKa."""
        from orgchem.core.ph_explorer import buffer_capacity
        r = buffer_capacity(total_concentration_M=0.1,
                            pH=4.76, pKa=4.76)
        assert math.isclose(r["alpha"], 0.5, rel_tol=1e-9)
        assert math.isclose(r["fraction_of_max"], 1.0,
                            rel_tol=1e-9)
        # β = 0.576 · 0.1 ≈ 0.0576 M/pH.
        assert math.isclose(
            r["buffer_capacity_M_per_pH"], 0.0576,
            rel_tol=1e-3)

    def test_drops_off_at_distance(self):
        """At |ΔpH| = 1, fraction_of_max should be ≈ 0.32."""
        from orgchem.core.ph_explorer import buffer_capacity
        r = buffer_capacity(total_concentration_M=0.1,
                            pH=5.76, pKa=4.76)
        assert r["fraction_of_max"] < 0.4


# ==================================================================
# Titration curve
# ==================================================================

class TestTitrationCurve:
    def test_acetic_acid_acidic_initial_pH(self):
        """0.1 M acetic acid (pKa 4.76) → initial pH ≈ 2.88."""
        from orgchem.core.ph_explorer import titration_curve
        r = titration_curve(weak_acid_pKa=4.76,
                            acid_initial_M=0.1,
                            volume_acid_mL=25.0,
                            base_concentration_M=0.1,
                            n_points=10)
        v0, ph0 = r["points"][0]
        assert v0 == 0.0
        assert math.isclose(ph0, 2.88, abs_tol=0.05)

    def test_equivalence_point_at_25_mL(self):
        """0.1 M × 25 mL acid + 0.1 M base → v_eq = 25 mL."""
        from orgchem.core.ph_explorer import titration_curve
        r = titration_curve(weak_acid_pKa=4.76,
                            acid_initial_M=0.1,
                            volume_acid_mL=25.0,
                            base_concentration_M=0.1,
                            n_points=10)
        assert math.isclose(r["equivalence_point_mL"], 25.0,
                            rel_tol=1e-9)

    def test_pH_at_equivalence_above_7(self):
        """Weak acid + strong base → equivalence-point pH > 7
        (basic, due to A⁻ hydrolysis)."""
        from orgchem.core.ph_explorer import titration_curve
        r = titration_curve(weak_acid_pKa=4.76,
                            acid_initial_M=0.1,
                            volume_acid_mL=25.0,
                            base_concentration_M=0.1,
                            n_points=10)
        # Find the point closest to 25 mL.
        for v, ph in r["points"]:
            if abs(v - 25.0) < 0.5:
                assert ph > 7.0
                break

    def test_rejects_zero_concentration(self):
        from orgchem.core.ph_explorer import titration_curve
        with pytest.raises(ValueError):
            titration_curve(weak_acid_pKa=4.76,
                            acid_initial_M=0.0,
                            volume_acid_mL=25.0,
                            base_concentration_M=0.1)

    def test_rejects_pka_outside_aqueous_range(self):
        from orgchem.core.ph_explorer import titration_curve
        with pytest.raises(ValueError):
            titration_curve(weak_acid_pKa=20.0,
                            acid_initial_M=0.1,
                            volume_acid_mL=25.0,
                            base_concentration_M=0.1)


# ==================================================================
# to_dict serialisation
# ==================================================================

def test_acid_to_dict_keys():
    from orgchem.core.ph_explorer import (
        acid_to_dict, get_acid,
    )
    d = acid_to_dict(get_acid("acetic"))
    expected = {"id", "name", "formula", "category",
                "pka_values", "n_pka", "notes"}
    assert set(d.keys()) == expected
    assert d["n_pka"] == 1


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


def test_action_list_pka_acids(app):
    rows = app.call("list_pka_acids")
    assert len(rows) >= 40


def test_action_list_pka_acids_filtered(app):
    rows = app.call("list_pka_acids",
                    category="biological-buffer")
    assert all(r["category"] == "biological-buffer"
               for r in rows)


def test_action_list_pka_acids_unknown_category(app):
    rows = app.call("list_pka_acids", category="bogus")
    assert "error" in rows[0]


def test_action_get_pka_acid(app):
    r = app.call("get_pka_acid", acid_id="hepes")
    assert "error" not in r
    assert r["category"] == "biological-buffer"
    assert math.isclose(r["pka_values"][0], 7.55, abs_tol=0.05)


def test_action_get_unknown_pka_acid(app):
    r = app.call("get_pka_acid", acid_id="bogus")
    assert "error" in r


def test_action_find_pka_acids(app):
    rows = app.call("find_pka_acids", needle="histidine")
    assert any(r["id"] == "histidine" for r in rows)


def test_action_design_buffer(app):
    """Phosphate at pH 7.4."""
    r = app.call("design_buffer",
                 target_pH=7.4, pKa=7.20,
                 total_concentration_M=0.1)
    assert math.isclose(r["acid_concentration_M"] * 1000,
                        38.7, abs_tol=0.5)
    assert r["capacity_warning"] is False


def test_action_design_buffer_capacity_warning(app):
    """Big pH-pKa gap → warning."""
    r = app.call("design_buffer",
                 target_pH=7.0, pKa=4.76,
                 total_concentration_M=0.1)
    assert r["capacity_warning"] is True


def test_action_design_buffer_error_path(app):
    r = app.call("design_buffer",
                 target_pH=7.4, pKa=7.20,
                 total_concentration_M=0.0)
    assert "error" in r


def test_action_buffer_capacity(app):
    r = app.call("buffer_capacity",
                 total_concentration_M=0.1,
                 pH=4.76, pKa=4.76)
    assert math.isclose(r["fraction_of_max"], 1.0,
                        rel_tol=1e-9)


def test_action_simulate_titration(app):
    r = app.call("simulate_titration",
                 weak_acid_pKa=4.76,
                 acid_initial_M=0.1,
                 volume_acid_mL=25.0,
                 base_concentration_M=0.1,
                 n_points=20)
    assert math.isclose(r["equivalence_point_mL"], 25.0,
                        rel_tol=1e-9)
    assert len(r["points"]) == 21


def test_action_simulate_titration_error_path(app):
    r = app.call("simulate_titration",
                 weak_acid_pKa=4.76,
                 acid_initial_M=0.0,
                 volume_acid_mL=25.0,
                 base_concentration_M=0.1)
    assert "error" in r


# ==================================================================
# Dialog
# ==================================================================

@pytest.fixture(autouse=True)
def _reset_singleton():
    from orgchem.gui.dialogs import ph_explorer as mod
    mod.PHExplorerDialog._instance = None
    yield
    mod.PHExplorerDialog._instance = None


def test_dialog_constructs_with_four_tabs(app, qtbot):
    from orgchem.gui.dialogs.ph_explorer import PHExplorerDialog
    d = PHExplorerDialog(parent=app.window)
    qtbot.addWidget(d)
    labels = d.tab_labels()
    for must in ("Reference", "Buffer designer",
                 "Titration curve", "pKa lookup"):
        assert must in labels


def test_dialog_singleton(app):
    from orgchem.gui.dialogs.ph_explorer import PHExplorerDialog
    a = PHExplorerDialog.singleton(parent=app.window)
    b = PHExplorerDialog.singleton(parent=app.window)
    assert a is b


def test_dialog_select_tab_buffer(app, qtbot):
    from orgchem.gui.dialogs.ph_explorer import PHExplorerDialog
    d = PHExplorerDialog(parent=app.window)
    qtbot.addWidget(d)
    assert d.select_tab("Buffer designer") is True


def test_dialog_select_unknown_tab(app, qtbot):
    from orgchem.gui.dialogs.ph_explorer import PHExplorerDialog
    d = PHExplorerDialog(parent=app.window)
    qtbot.addWidget(d)
    assert d.select_tab("NotARealTab") is False


def test_dialog_buffer_designer_runs(app, qtbot):
    """Drive the buffer-designer through the UI."""
    from orgchem.gui.dialogs.ph_explorer import PHExplorerDialog
    d = PHExplorerDialog(parent=app.window)
    qtbot.addWidget(d)
    d._buf_target_ph.setValue(7.4)
    d._buf_pka_spin.setValue(7.20)
    d._buf_total_M.setValue(0.1)
    d._on_design_buffer()
    html = d._buf_result.toHtml()
    assert "Buffer recipe" in html
    # 38.686 / 61.314 mM split (HH at pH 7.4, pKa 7.20).
    assert "38.686" in html or "38.7" in html
    assert "61.314" in html or "61.3" in html


def test_dialog_buffer_designer_warning_path(app, qtbot):
    from orgchem.gui.dialogs.ph_explorer import PHExplorerDialog
    d = PHExplorerDialog(parent=app.window)
    qtbot.addWidget(d)
    d._buf_target_ph.setValue(7.0)
    d._buf_pka_spin.setValue(4.76)
    d._buf_total_M.setValue(0.1)
    d._on_design_buffer()
    html = d._buf_result.toHtml().lower()
    assert "capacity warning" in html


def test_dialog_buffer_capacity_runs(app, qtbot):
    from orgchem.gui.dialogs.ph_explorer import PHExplorerDialog
    d = PHExplorerDialog(parent=app.window)
    qtbot.addWidget(d)
    d._buf_target_ph.setValue(4.76)
    d._buf_pka_spin.setValue(4.76)
    d._buf_total_M.setValue(0.1)
    d._on_capacity()
    html = d._buf_result.toHtml()
    assert "Buffer capacity" in html
    assert "100.0%" in html


def test_dialog_titration_runs(app, qtbot):
    from orgchem.gui.dialogs.ph_explorer import PHExplorerDialog
    d = PHExplorerDialog(parent=app.window)
    qtbot.addWidget(d)
    d._tit_pka.setValue(4.76)
    d._tit_acid_M.setValue(0.1)
    d._tit_acid_vol.setValue(25.0)
    d._tit_base_M.setValue(0.1)
    d._tit_npoints.setValue(20)
    d._on_simulate_titration()
    html = d._tit_result.toHtml()
    assert "Titration curve" in html
    assert "25.00" in html   # equivalence point


def test_dialog_lookup_table_populated(app, qtbot):
    from orgchem.gui.dialogs.ph_explorer import PHExplorerDialog
    d = PHExplorerDialog(parent=app.window)
    qtbot.addWidget(d)
    # Lookup tab is the 4th tab.
    assert d._lookup_table.rowCount() >= 40


def test_dialog_lookup_filter_narrows(app, qtbot):
    from orgchem.gui.dialogs.ph_explorer import PHExplorerDialog
    d = PHExplorerDialog(parent=app.window)
    qtbot.addWidget(d)
    d._lookup_filter.setText("hepes")
    assert d._lookup_table.rowCount() == 1


def test_open_action_fires(app, qtbot):
    from orgchem.agent.actions import invoke
    from orgchem.gui.dialogs.ph_explorer import PHExplorerDialog
    res = invoke("open_ph_explorer")
    assert res.get("opened") is True
    assert PHExplorerDialog._instance is not None


def test_open_action_with_tab(app, qtbot):
    from orgchem.agent.actions import invoke
    res = invoke("open_ph_explorer", tab="Titration curve")
    assert res.get("opened") is True
    assert res.get("selected") is True
