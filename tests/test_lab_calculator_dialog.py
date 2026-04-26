"""Phase 39b (round 143) — pytest-qt cases for the
*Tools → Lab calculator…* tabbed dialog.

Drives a representative solver per tab through the public
spin / button API to verify the dialog correctly bridges the
Phase-39a solvers to the GUI.
"""
from __future__ import annotations
import math
import os

import pytest

pytest.importorskip("pytestqt", reason="pytest-qt not installed")


@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(5)
        yield h


@pytest.fixture(autouse=True)
def _reset_singleton():
    from orgchem.gui.dialogs import lab_calculator as mod
    mod.LabCalculatorDialog._instance = None
    yield
    mod.LabCalculatorDialog._instance = None


# ---- construction ---------------------------------------------

def test_dialog_constructs_with_seven_tabs(app, qtbot):
    from orgchem.gui.dialogs.lab_calculator import (
        LabCalculatorDialog,
    )
    d = LabCalculatorDialog(parent=app.window)
    qtbot.addWidget(d)
    labels = d.tab_labels()
    assert len(labels) == 7
    for must in ("Solution", "Stoichiometry", "Acid-base",
                 "Gas law", "Colligative", "Thermo + kinetics",
                 "Equilibrium"):
        assert must in labels


def test_singleton_returns_same_instance(app):
    from orgchem.gui.dialogs.lab_calculator import (
        LabCalculatorDialog,
    )
    a = LabCalculatorDialog.singleton(parent=app.window)
    b = LabCalculatorDialog.singleton(parent=app.window)
    assert a is b


def test_select_tab_focuses_match(app, qtbot):
    from orgchem.gui.dialogs.lab_calculator import (
        LabCalculatorDialog,
    )
    d = LabCalculatorDialog(parent=app.window)
    qtbot.addWidget(d)
    assert d.select_tab("Acid-base") is True
    assert d._tabs.tabText(d._tabs.currentIndex()) == "Acid-base"


def test_select_tab_unknown_returns_false(app, qtbot):
    from orgchem.gui.dialogs.lab_calculator import (
        LabCalculatorDialog,
    )
    d = LabCalculatorDialog(parent=app.window)
    qtbot.addWidget(d)
    assert d.select_tab("NotARealTab") is False


# ---- helpers --------------------------------------------------

def _find_solver_panel(scroll_widget, title_substring: str):
    """Walk the scroll-area's content widget for a `_SolverPanel`
    whose title contains the given substring."""
    from orgchem.gui.dialogs.lab_calculator import _SolverPanel
    inner = scroll_widget.widget()
    for child in inner.findChildren(_SolverPanel):
        if title_substring.lower() in child.title().lower():
            return child
    raise AssertionError(
        f"no _SolverPanel matching {title_substring!r}")


def _spin_at(panel, name: str):
    return panel._spin_by_name[name]


# ---- solution tab: molarity solver ----------------------------

def test_molarity_panel_solves_for_mass(app, qtbot):
    """0.5 M × 1 L × 58.44 g/mol → 29.22 g (NaCl)."""
    from orgchem.gui.dialogs.lab_calculator import (
        LabCalculatorDialog,
    )
    d = LabCalculatorDialog(parent=app.window)
    qtbot.addWidget(d)
    scroll = d._tabs.widget(d._tabs.indexOf(
        d._tabs.findChild(type(d._tabs.widget(0)),
                          options=...)) if False else 0)
    # Simpler: tab 0 is Solution.
    scroll = d._tabs.widget(0)
    panel = _find_solver_panel(scroll, "molarity")
    _spin_at(panel, "molarity_M").setValue(0.5)
    _spin_at(panel, "volume_L").setValue(1.0)
    _spin_at(panel, "molecular_weight_gmol").setValue(58.44)
    # mass_g left at 0 = unknown.
    panel._on_solve()
    assert math.isclose(
        _spin_at(panel, "mass_g").value(), 29.22, rel_tol=1e-3)


def test_dilution_panel_solves_for_v2(app, qtbot):
    """1 M × 10 mL → 0.1 M × ? = 100 mL."""
    from orgchem.gui.dialogs.lab_calculator import (
        LabCalculatorDialog,
    )
    d = LabCalculatorDialog(parent=app.window)
    qtbot.addWidget(d)
    scroll = d._tabs.widget(0)
    panel = _find_solver_panel(scroll, "dilution")
    _spin_at(panel, "M1").setValue(1.0)
    _spin_at(panel, "V1").setValue(10.0)
    _spin_at(panel, "M2").setValue(0.1)
    panel._on_solve()
    assert math.isclose(_spin_at(panel, "V2").value(), 100.0,
                        rel_tol=1e-9)


def test_clear_resets_all_spins(app, qtbot):
    from orgchem.gui.dialogs.lab_calculator import (
        LabCalculatorDialog,
    )
    d = LabCalculatorDialog(parent=app.window)
    qtbot.addWidget(d)
    scroll = d._tabs.widget(0)
    panel = _find_solver_panel(scroll, "molarity")
    _spin_at(panel, "molarity_M").setValue(0.5)
    _spin_at(panel, "volume_L").setValue(1.0)
    panel._on_clear()
    for spin in panel._spin_by_name.values():
        assert spin.value() == 0.0


def test_solver_error_path_is_displayed(app, qtbot):
    from orgchem.gui.dialogs.lab_calculator import (
        LabCalculatorDialog,
    )
    d = LabCalculatorDialog(parent=app.window)
    qtbot.addWidget(d)
    scroll = d._tabs.widget(0)
    panel = _find_solver_panel(scroll, "molarity")
    # Leave 2 fields blank — solver expects exactly 1.
    _spin_at(panel, "molarity_M").setValue(0.5)
    panel._on_solve()
    assert "error" in panel._status.text().lower()


# ---- gas law tab: ideal gas solver ----------------------------

def test_ideal_gas_panel_solves_for_volume(app, qtbot):
    """1 atm × ? × 1 mol × 273.15 K = 22.414 L (STP)."""
    from orgchem.gui.dialogs.lab_calculator import (
        LabCalculatorDialog,
    )
    d = LabCalculatorDialog(parent=app.window)
    qtbot.addWidget(d)
    scroll = d._tabs.widget(d.tab_labels().index("Gas law"))
    panel = _find_solver_panel(scroll, "ideal gas")
    _spin_at(panel, "pressure_atm").setValue(1.0)
    _spin_at(panel, "moles").setValue(1.0)
    _spin_at(panel, "temperature_K").setValue(273.15)
    panel._on_solve()
    assert math.isclose(_spin_at(panel, "volume_L").value(),
                        22.414, rel_tol=1e-3)


# ---- colligative tab: solvent-dropdown auto-fill --------------

def test_freezing_point_solvent_dropdown_auto_fills_kf(
        app, qtbot):
    """Pick water from the dropdown + enter molality + i → ΔTf
    auto-uses K_f = 1.86 → ΔTf = 3.72 °C for 1 m NaCl (i = 2)."""
    from orgchem.gui.dialogs.lab_calculator import (
        LabCalculatorDialog,
    )
    d = LabCalculatorDialog(parent=app.window)
    qtbot.addWidget(d)
    scroll = d._tabs.widget(
        d.tab_labels().index("Colligative"))
    panel = _find_solver_panel(scroll, "freezing-point")
    # Set solvent dropdown to water.
    combo = panel._extra_widgets["solvent"]
    idx = combo.findData("water")
    assert idx >= 0
    combo.setCurrentIndex(idx)
    # K_f left at 0 (unknown) — solver must use the lookup.
    _spin_at(panel, "molality_b").setValue(1.0)
    _spin_at(panel, "van_t_hoff_i").setValue(2.0)
    panel._on_solve()
    assert math.isclose(_spin_at(panel, "delta_T_f").value(),
                        3.72, rel_tol=1e-3)
    # K_f spin should now show the auto-filled water value.
    assert math.isclose(_spin_at(panel, "K_f").value(),
                        1.86, rel_tol=1e-3)


# ---- acid-base tab: H ↔ pH custom panel -----------------------

def test_h_to_ph_custom_button(app, qtbot):
    """Acid-base tab has a custom H ↔ pH widget (not a
    `_SolverPanel`); verify the H→pH button path works."""
    from orgchem.gui.dialogs.lab_calculator import (
        LabCalculatorDialog,
    )
    from PySide6.QtWidgets import QPushButton, QGroupBox, QDoubleSpinBox
    d = LabCalculatorDialog(parent=app.window)
    qtbot.addWidget(d)
    scroll = d._tabs.widget(d.tab_labels().index("Acid-base"))
    inner = scroll.widget()
    # Find the H ↔ pH group box.
    box = None
    for child in inner.findChildren(QGroupBox):
        if "ph ↔ [h⁺]" in child.title().lower():
            box = child
            break
    assert box is not None, "missing pH ↔ [H⁺] panel"
    spins = box.findChildren(QDoubleSpinBox)
    btns = box.findChildren(QPushButton)
    h_to_ph_btn = next(b for b in btns
                       if "H⁺] → pH" in b.text())
    # spins[0] = h_spin, spins[1] = pH_spin (insertion order).
    spins[0].setValue(1e-3)
    h_to_ph_btn.click()
    assert math.isclose(spins[1].value(), 3.0, rel_tol=1e-6)


# ---- equilibrium tab: K_sp ↔ s custom panel -------------------

def test_ksp_from_solubility_button(app, qtbot):
    """AgCl: n=m=1, s=1.3e-5 → K_sp ≈ 1.69e-10."""
    from orgchem.gui.dialogs.lab_calculator import (
        LabCalculatorDialog,
    )
    from PySide6.QtWidgets import QPushButton, QGroupBox, QDoubleSpinBox
    d = LabCalculatorDialog(parent=app.window)
    qtbot.addWidget(d)
    scroll = d._tabs.widget(
        d.tab_labels().index("Equilibrium"))
    inner = scroll.widget()
    box = None
    for child in inner.findChildren(QGroupBox):
        if "ksp" in child.title().lower().replace("_", ""):
            box = child
            break
    assert box is not None
    spins = box.findChildren(QDoubleSpinBox)
    s_spin, ksp_spin, n_spin, m_spin = spins[:4]
    btns = box.findChildren(QPushButton)
    s_to_ksp_btn = next(b for b in btns if "→ K_sp" in b.text())
    s_spin.setValue(1.3e-5)
    n_spin.setValue(1)
    m_spin.setValue(1)
    s_to_ksp_btn.click()
    assert math.isclose(ksp_spin.value(), 1.69e-10, rel_tol=1e-3)


# ---- agent action ---------------------------------------------

def test_open_lab_calculator_action_fires(app, qtbot):
    from orgchem.agent.actions import invoke
    from orgchem.gui.dialogs.lab_calculator import (
        LabCalculatorDialog,
    )
    res = invoke("open_lab_calculator")
    assert res.get("opened") is True
    assert res.get("selected") is False
    assert "Solution" in res["available_tabs"]
    assert LabCalculatorDialog._instance is not None


def test_open_lab_calculator_with_tab_focuses(app, qtbot):
    from orgchem.agent.actions import invoke
    res = invoke("open_lab_calculator", tab="Gas law")
    assert res.get("opened") is True
    assert res.get("selected") is True


def test_open_lab_calculator_with_unknown_tab(app, qtbot):
    from orgchem.agent.actions import invoke
    res = invoke("open_lab_calculator", tab="NotARealTab")
    assert res.get("opened") is True
    assert res.get("selected") is False
