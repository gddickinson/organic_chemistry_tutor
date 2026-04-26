"""Phase 39b (round 143) — *Tools → Lab calculator…* dialog.

Tabbed dialog wrapping every Phase-39a solver in a small
form widget.  One `QTabWidget` tab per `core/calc_*.py`
module; per-tab a stack of solver `_SolverPanel`
``QGroupBox``es.

Each `_SolverPanel`:
- Title (= panel name).
- N labelled `QDoubleSpinBox` fields.
- Optional ``solvent`` `QComboBox` (for the colligative tab).
- *Solve for empty field* button.
- *Clear* button.
- Status line below the buttons that displays the rearranged
  equation in human form (e.g. ``"c = A / (ε · l) = 4.0e-5 M"``)
  + any validation error returned by the solver.

Spin-box value of 0.0 means *unknown* — the solver picks it up
as ``None``.  Same convention as the Phase 37d Beer-Lambert
widget.

Singleton modeless dialog — re-opening preserves the tab
selection + entered values across the session.
"""
from __future__ import annotations
import logging
from typing import Callable, Dict, List, Optional, Tuple

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox, QDialog, QDoubleSpinBox, QFormLayout, QGroupBox,
    QHBoxLayout, QLabel, QPushButton, QScrollArea, QSizePolicy,
    QTabWidget, QVBoxLayout, QWidget,
)

log = logging.getLogger(__name__)


# ------------------------------------------------------------------
# Common solver panel
# ------------------------------------------------------------------

class _SolverPanel(QGroupBox):
    """One solver: titled group box with N spin boxes + Solve +
    Clear + status line.

    *fields* is a list of ``{name, label, suffix, decimals?,
    min?, max?, default?}`` dicts.  Spin value 0 (default) =
    unknown; the solver kwarg is ``None`` for those fields.
    *solver* is a callable that takes the field names as kwargs
    and returns a result dict mapping field_name → numeric
    value (or raises ``ValueError`` on bad input).
    """

    def __init__(self,
                 title: str,
                 fields: List[Dict[str, object]],
                 solver: Callable[..., Dict[str, float]],
                 zero_means_unknown: bool = True,
                 status_help: str = "",
                 parent: Optional[QWidget] = None):
        super().__init__(title, parent)
        self._fields = fields
        self._solver = solver
        self._zero_means_unknown = zero_means_unknown
        self._spin_by_name: Dict[str, QDoubleSpinBox] = {}
        self._extra_widgets: Dict[str, QWidget] = {}

        form = QFormLayout(self)
        for f in fields:
            spin = QDoubleSpinBox()
            spin.setDecimals(int(f.get("decimals", 4)))
            spin.setRange(float(f.get("min", 0.0)),
                          float(f.get("max", 1e12)))
            spin.setValue(float(f.get("default", 0.0)))
            suffix = f.get("suffix", "")
            if suffix:
                spin.setSuffix(f"  {suffix}")
            spin.setSizePolicy(QSizePolicy.Expanding,
                               QSizePolicy.Fixed)
            form.addRow(str(f.get("label", f["name"])), spin)
            self._spin_by_name[str(f["name"])] = spin

        btn_row = QHBoxLayout()
        self._solve_btn = QPushButton("Solve for empty field")
        self._solve_btn.clicked.connect(self._on_solve)
        btn_row.addWidget(self._solve_btn)
        self._clear_btn = QPushButton("Clear")
        self._clear_btn.clicked.connect(self._on_clear)
        btn_row.addWidget(self._clear_btn)
        btn_row.addStretch(1)
        form.addRow(btn_row)

        self._status = QLabel(
            status_help or
            "Leave one field at 0 (blank); the solver fills it.")
        self._status.setWordWrap(True)
        form.addRow(self._status)

    # ---- slot helpers -----------------------------------------

    def add_widget(self, name: str, widget: QWidget) -> None:
        """Register an arbitrary widget (e.g. a `QComboBox` for
        solvent selection) so the solver kwargs can pull from
        it via :meth:`extra_value`."""
        self._extra_widgets[name] = widget
        self.layout().insertRow(0, name + ":", widget)

    def extra_value(self, name: str) -> object:
        w = self._extra_widgets[name]
        if isinstance(w, QComboBox):
            return w.currentData() or w.currentText()
        return w.text() if hasattr(w, "text") else None

    def _on_solve(self) -> None:
        kwargs: Dict[str, object] = {}
        for name, spin in self._spin_by_name.items():
            v = spin.value()
            if self._zero_means_unknown and v == 0.0:
                kwargs[name] = None
            else:
                kwargs[name] = v
        # Fold any extra (e.g. solvent dropdown) into kwargs.
        for name in self._extra_widgets:
            value = self.extra_value(name)
            if value:
                kwargs[name] = value
        try:
            result = self._solver(**kwargs)
        except Exception as e:  # noqa: BLE001
            self._status.setText(f"<b>Error:</b> {e}")
            return
        # Populate spins from result.
        for name, spin in self._spin_by_name.items():
            if name in result and isinstance(
                    result[name], (int, float)):
                spin.blockSignals(True)
                spin.setValue(float(result[name]))
                spin.blockSignals(False)
        # Status: show every field as "name = value [suffix]".
        bits = []
        for f in self._fields:
            name = str(f["name"])
            if name in result:
                v = result[name]
                if isinstance(v, (int, float)):
                    bits.append(
                        f"{f.get('label', name)} = "
                        f"{_fmt_num(float(v))}")
        self._status.setText(" &nbsp; · &nbsp; ".join(bits))

    def _on_clear(self) -> None:
        for spin in self._spin_by_name.values():
            spin.blockSignals(True)
            spin.setValue(0.0)
            spin.blockSignals(False)
        self._status.setText(
            "Leave one field at 0 (blank); the solver fills it.")


def _fmt_num(v: float) -> str:
    """Format a number with appropriate precision: scientific
    when |v| < 1e-3 or > 1e6, fixed otherwise."""
    if v == 0:
        return "0"
    abs_v = abs(v)
    if abs_v < 1e-3 or abs_v >= 1e6:
        return f"{v:.4g}"
    if abs_v < 1:
        return f"{v:.4g}"
    return f"{v:.4f}".rstrip("0").rstrip(".")


# ------------------------------------------------------------------
# Tab builders
# ------------------------------------------------------------------

def _build_solution_tab() -> QWidget:
    from orgchem.core import calc_solution
    page = QWidget()
    lay = QVBoxLayout(page)
    lay.addWidget(_SolverPanel(
        title="Molarity (m = M·V·MW)",
        fields=[
            {"name": "mass_g", "label": "Mass m",
             "suffix": "g"},
            {"name": "molarity_M", "label": "Molarity M",
             "suffix": "M"},
            {"name": "volume_L", "label": "Volume V",
             "suffix": "L"},
            {"name": "molecular_weight_gmol",
             "label": "MW", "suffix": "g/mol", "decimals": 2},
        ],
        solver=calc_solution.molarity_solve,
    ))
    lay.addWidget(_SolverPanel(
        title="Dilution (M₁·V₁ = M₂·V₂)",
        fields=[
            {"name": "M1", "label": "M₁", "suffix": "M"},
            {"name": "V1", "label": "V₁", "suffix": "mL"},
            {"name": "M2", "label": "M₂", "suffix": "M"},
            {"name": "V2", "label": "V₂", "suffix": "mL"},
        ],
        solver=calc_solution.dilution_solve,
    ))
    lay.addWidget(_SolverPanel(
        title="Molarity from %w/w + density",
        fields=[
            {"name": "mass_percent",
             "label": "Mass %", "suffix": "%", "max": 100.0},
            {"name": "density_g_per_mL",
             "label": "Density ρ", "suffix": "g/mL"},
            {"name": "molecular_weight_gmol",
             "label": "MW", "suffix": "g/mol", "decimals": 2},
        ],
        solver=calc_solution.molarity_from_mass_percent,
        zero_means_unknown=False,
        status_help=(
            "Concentrated HCl: 37 % w/w · 1.18 g/mL ÷ 36.46 "
            "g/mol → ~12 M.  All three inputs required."),
    ))
    lay.addStretch(1)
    return page


def _build_stoich_tab() -> QWidget:
    from orgchem.core import calc_stoichiometry
    page = QWidget()
    lay = QVBoxLayout(page)
    lay.addWidget(_SolverPanel(
        title="Percent yield (% = 100 · actual / theoretical)",
        fields=[
            {"name": "actual_yield_g",
             "label": "Actual yield", "suffix": "g"},
            {"name": "theoretical_yield_g",
             "label": "Theoretical yield", "suffix": "g"},
            {"name": "percent",
             "label": "Yield %", "suffix": "%", "max": 100.0},
        ],
        solver=calc_stoichiometry.percent_yield,
    ))
    lay.addWidget(_SolverPanel(
        title="Percent purity",
        fields=[
            {"name": "pure_mass_g",
             "label": "Pure mass", "suffix": "g"},
            {"name": "sample_mass_g",
             "label": "Sample mass", "suffix": "g"},
        ],
        solver=calc_stoichiometry.percent_purity,
        zero_means_unknown=False,
    ))
    lay.addWidget(_SolverPanel(
        title="Theoretical yield (from limiting reagent)",
        fields=[
            {"name": "limiting_moles",
             "label": "Limiting reagent (mol)", "suffix": "mol"},
            {"name": "limiting_stoich_coeff",
             "label": "Limiting coeff", "suffix": "",
             "default": 1.0},
            {"name": "product_stoich_coeff",
             "label": "Product coeff", "suffix": "",
             "default": 1.0},
            {"name": "product_mw_gmol",
             "label": "Product MW", "suffix": "g/mol",
             "decimals": 2},
        ],
        solver=calc_stoichiometry.theoretical_yield_g,
        zero_means_unknown=False,
        status_help=(
            "All four inputs required.  Output: theoretical "
            "yield in grams + moles of product."),
    ))
    lay.addStretch(1)
    return page


def _build_acid_base_tab() -> QWidget:
    from orgchem.core import calc_acid_base
    page = QWidget()
    lay = QVBoxLayout(page)

    # pH ↔ [H⁺]: two halves wired to the dedicated solvers.
    panel = QGroupBox("pH ↔ [H⁺] (aqueous, 25 °C)")
    form = QFormLayout(panel)
    h_spin = QDoubleSpinBox()
    h_spin.setDecimals(12)
    h_spin.setRange(1e-15, 100.0)
    h_spin.setValue(1e-7)
    h_spin.setSuffix("  M [H⁺]")
    pH_spin = QDoubleSpinBox()
    pH_spin.setDecimals(3)
    pH_spin.setRange(0.0, 14.0)
    pH_spin.setValue(7.0)
    pH_spin.setSuffix("  pH")
    form.addRow("[H⁺]:", h_spin)
    form.addRow("pH:", pH_spin)
    btn_row = QHBoxLayout()
    btn_h_to_ph = QPushButton("[H⁺] → pH")
    btn_ph_to_h = QPushButton("pH → [H⁺]")
    btn_row.addWidget(btn_h_to_ph)
    btn_row.addWidget(btn_ph_to_h)
    btn_row.addStretch(1)
    form.addRow(btn_row)
    status = QLabel("Enter [H⁺] (M) → pH, or pH → [H⁺].")
    status.setWordWrap(True)
    form.addRow(status)

    def _h_to_ph():
        try:
            r = calc_acid_base.ph_from_h(h_spin.value())
        except ValueError as e:
            status.setText(f"<b>Error:</b> {e}")
            return
        pH_spin.setValue(r["pH"])
        status.setText(
            f"pH = {_fmt_num(r['pH'])} &nbsp;·&nbsp; pOH = "
            f"{_fmt_num(r['pOH'])} &nbsp;·&nbsp; [OH⁻] = "
            f"{_fmt_num(r['oh_concentration_M'])} M")

    def _ph_to_h():
        try:
            r = calc_acid_base.h_from_ph(pH_spin.value())
        except ValueError as e:
            status.setText(f"<b>Error:</b> {e}")
            return
        h_spin.setValue(r["h_concentration_M"])
        status.setText(
            f"[H⁺] = {_fmt_num(r['h_concentration_M'])} M "
            f"&nbsp;·&nbsp; pOH = {_fmt_num(r['pOH'])}")

    btn_h_to_ph.clicked.connect(_h_to_ph)
    btn_ph_to_h.clicked.connect(_ph_to_h)
    lay.addWidget(panel)

    # pKa ↔ Ka via the symmetric panel.
    pka_panel = QGroupBox("pKa ↔ Ka")
    pf = QFormLayout(pka_panel)
    pka_spin = QDoubleSpinBox()
    pka_spin.setDecimals(3)
    pka_spin.setRange(-10.0, 50.0)
    pka_spin.setValue(4.76)
    pka_spin.setSuffix("  pKa")
    ka_spin = QDoubleSpinBox()
    ka_spin.setDecimals(12)
    ka_spin.setRange(1e-50, 1e10)
    ka_spin.setValue(10 ** -4.76)
    ka_spin.setSuffix("  Ka")
    pf.addRow("pKa:", pka_spin)
    pf.addRow("Ka:", ka_spin)
    pka_btns = QHBoxLayout()
    pka_to_ka_btn = QPushButton("pKa → Ka")
    ka_to_pka_btn = QPushButton("Ka → pKa")
    pka_btns.addWidget(pka_to_ka_btn)
    pka_btns.addWidget(ka_to_pka_btn)
    pka_btns.addStretch(1)
    pf.addRow(pka_btns)
    pka_status = QLabel("Default: acetic acid pKa 4.76.")
    pka_status.setWordWrap(True)
    pf.addRow(pka_status)

    def _pka_to_ka():
        try:
            r = calc_acid_base.pka_to_ka(pka_spin.value())
        except ValueError as e:
            pka_status.setText(f"<b>Error:</b> {e}")
            return
        ka_spin.setValue(r["Ka"])
        pka_status.setText(
            f"Ka = {_fmt_num(r['Ka'])}")

    def _ka_to_pka():
        try:
            r = calc_acid_base.ka_to_pka(ka_spin.value())
        except ValueError as e:
            pka_status.setText(f"<b>Error:</b> {e}")
            return
        pka_spin.setValue(r["pKa"])
        pka_status.setText(
            f"pKa = {_fmt_num(r['pKa'])}")

    pka_to_ka_btn.clicked.connect(_pka_to_ka)
    ka_to_pka_btn.clicked.connect(_ka_to_pka)
    lay.addWidget(pka_panel)

    lay.addWidget(_SolverPanel(
        title="Henderson-Hasselbalch (pH = pKa + log [A⁻]/[HA])",
        fields=[
            {"name": "pH", "label": "pH",
             "suffix": "", "min": -5.0, "max": 20.0,
             "decimals": 3},
            {"name": "pKa", "label": "pKa",
             "suffix": "", "min": -5.0, "max": 50.0,
             "decimals": 3},
            {"name": "base_acid_ratio",
             "label": "[A⁻]/[HA]",
             "suffix": "", "decimals": 6},
        ],
        solver=calc_acid_base.henderson_hasselbalch,
        status_help=(
            "Buffer-design entry point.  Pass 2 of 3 (use "
            "0 for the unknown)."),
    ))
    lay.addStretch(1)
    return page


def _build_gas_law_tab() -> QWidget:
    from orgchem.core import calc_gas_law
    page = QWidget()
    lay = QVBoxLayout(page)
    lay.addWidget(_SolverPanel(
        title="Ideal gas (PV = nRT)",
        fields=[
            {"name": "pressure_atm",
             "label": "Pressure P", "suffix": "atm"},
            {"name": "volume_L",
             "label": "Volume V", "suffix": "L"},
            {"name": "moles", "label": "Moles n",
             "suffix": "mol"},
            {"name": "temperature_K",
             "label": "Temperature T", "suffix": "K"},
        ],
        solver=calc_gas_law.ideal_gas_solve,
    ))
    lay.addWidget(_SolverPanel(
        title="Combined gas law (P₁V₁/T₁ = P₂V₂/T₂)",
        fields=[
            {"name": "P1", "label": "P₁", "suffix": "atm"},
            {"name": "V1", "label": "V₁", "suffix": "L"},
            {"name": "T1", "label": "T₁", "suffix": "K"},
            {"name": "P2", "label": "P₂", "suffix": "atm"},
            {"name": "V2", "label": "V₂", "suffix": "L"},
            {"name": "T2", "label": "T₂", "suffix": "K"},
        ],
        solver=calc_gas_law.combined_gas_law,
    ))
    lay.addWidget(_SolverPanel(
        title="Gas density (ρ = PM / RT)",
        fields=[
            {"name": "pressure_atm",
             "label": "Pressure", "suffix": "atm"},
            {"name": "molecular_weight_gmol",
             "label": "MW", "suffix": "g/mol",
             "decimals": 2},
            {"name": "temperature_K",
             "label": "Temperature", "suffix": "K"},
        ],
        solver=calc_gas_law.gas_density,
        zero_means_unknown=False,
    ))
    lay.addStretch(1)
    return page


def _build_colligative_tab() -> QWidget:
    from orgchem.core import calc_colligative
    page = QWidget()
    lay = QVBoxLayout(page)

    bp_panel = _SolverPanel(
        title="Boiling-point elevation (ΔT_b = K_b · b · i)",
        fields=[
            {"name": "K_b", "label": "K_b",
             "suffix": "°C·kg/mol", "decimals": 3},
            {"name": "molality_b",
             "label": "Molality b", "suffix": "mol/kg"},
            {"name": "van_t_hoff_i",
             "label": "i", "suffix": "", "default": 1.0,
             "decimals": 2},
            {"name": "delta_T_b",
             "label": "ΔT_b", "suffix": "°C", "decimals": 3},
        ],
        solver=calc_colligative.boiling_point_elevation,
        status_help=(
            "Pick a solvent below to auto-fill K_b, OR enter "
            "K_b directly + leave the rest blank as needed."),
    )
    bp_combo = QComboBox()
    bp_combo.addItem("(custom)", "")
    for name in calc_colligative.SOLVENT_CONSTANTS:
        bp_combo.addItem(name, name)
    bp_panel.add_widget("solvent", bp_combo)
    lay.addWidget(bp_panel)

    fp_panel = _SolverPanel(
        title="Freezing-point depression (ΔT_f = K_f · b · i)",
        fields=[
            {"name": "K_f", "label": "K_f",
             "suffix": "°C·kg/mol", "decimals": 3},
            {"name": "molality_b",
             "label": "Molality b", "suffix": "mol/kg"},
            {"name": "van_t_hoff_i",
             "label": "i", "suffix": "", "default": 1.0,
             "decimals": 2},
            {"name": "delta_T_f",
             "label": "ΔT_f", "suffix": "°C", "decimals": 3},
        ],
        solver=calc_colligative.freezing_point_depression,
    )
    fp_combo = QComboBox()
    fp_combo.addItem("(custom)", "")
    for name in calc_colligative.SOLVENT_CONSTANTS:
        fp_combo.addItem(name, name)
    fp_panel.add_widget("solvent", fp_combo)
    lay.addWidget(fp_panel)

    lay.addWidget(_SolverPanel(
        title="Osmotic pressure (Π = M·R·T·i)",
        fields=[
            {"name": "molarity_M",
             "label": "Molarity M", "suffix": "M",
             "decimals": 6},
            {"name": "temperature_K",
             "label": "Temperature", "suffix": "K"},
            {"name": "van_t_hoff_i",
             "label": "i", "suffix": "", "default": 1.0,
             "decimals": 2},
            {"name": "pressure_atm",
             "label": "Π", "suffix": "atm", "decimals": 3},
        ],
        solver=calc_colligative.osmotic_pressure,
    ))
    lay.addStretch(1)
    return page


def _build_thermo_kinetics_tab() -> QWidget:
    from orgchem.core import calc_thermo_kinetics
    page = QWidget()
    lay = QVBoxLayout(page)
    lay.addWidget(_SolverPanel(
        title="Heat capacity (q = m · c · ΔT)",
        fields=[
            {"name": "heat_q_J", "label": "Heat q",
             "suffix": "J", "min": -1e9},
            {"name": "mass_g", "label": "Mass m",
             "suffix": "g"},
            {"name": "specific_heat_J_per_g_K",
             "label": "Specific heat c",
             "suffix": "J/(g·K)", "decimals": 4},
            {"name": "delta_T_K",
             "label": "ΔT", "suffix": "K", "min": -1000.0,
             "decimals": 3},
        ],
        solver=calc_thermo_kinetics.heat_capacity_solve,
    ))
    lay.addWidget(_SolverPanel(
        title="First-order half-life (t½ = ln 2 / k)",
        fields=[
            {"name": "rate_constant_per_s",
             "label": "Rate constant k",
             "suffix": "s⁻¹", "decimals": 9},
            {"name": "half_life_s",
             "label": "Half-life t½", "suffix": "s",
             "decimals": 4},
        ],
        solver=calc_thermo_kinetics.first_order_half_life,
    ))
    lay.addWidget(_SolverPanel(
        title="Arrhenius (k = A · exp(-Ea / RT))",
        fields=[
            {"name": "rate_constant", "label": "k",
             "suffix": "s⁻¹", "decimals": 9, "max": 1e20},
            {"name": "pre_exponential_A",
             "label": "Prefactor A",
             "suffix": "s⁻¹", "decimals": 4, "max": 1e20},
            {"name": "activation_energy_J_per_mol",
             "label": "Eₐ",
             "suffix": "J/mol", "max": 1e7},
            {"name": "temperature_K",
             "label": "T", "suffix": "K"},
        ],
        solver=calc_thermo_kinetics.arrhenius_solve,
    ))
    lay.addStretch(1)
    return page


def _build_equilibrium_tab() -> QWidget:
    from orgchem.core import calc_equilibrium
    page = QWidget()
    lay = QVBoxLayout(page)

    # K_sp ↔ molar solubility — 4 spin boxes (s, K_sp, n, m) +
    # two buttons.  Dedicated panel since neither direction is
    # a simple "leave one blank" solve.
    panel = QGroupBox("K_sp ↔ molar solubility (AnBm salt)")
    form = QFormLayout(panel)
    s_spin = QDoubleSpinBox()
    s_spin.setDecimals(12)
    s_spin.setRange(0.0, 100.0)
    s_spin.setValue(0.0)
    s_spin.setSuffix("  M")
    ksp_spin = QDoubleSpinBox()
    ksp_spin.setDecimals(15)
    ksp_spin.setRange(0.0, 1e10)
    ksp_spin.setValue(0.0)
    ksp_spin.setSuffix("  K_sp")
    n_spin = QDoubleSpinBox()
    n_spin.setDecimals(0)
    n_spin.setRange(1, 10)
    n_spin.setValue(1)
    m_spin = QDoubleSpinBox()
    m_spin.setDecimals(0)
    m_spin.setRange(1, 10)
    m_spin.setValue(1)
    form.addRow("Molar solubility s:", s_spin)
    form.addRow("K_sp:", ksp_spin)
    form.addRow("n (cation count):", n_spin)
    form.addRow("m (anion count):", m_spin)
    ksp_btns = QHBoxLayout()
    s_to_ksp_btn = QPushButton("s + n,m → K_sp")
    ksp_to_s_btn = QPushButton("K_sp + n,m → s")
    ksp_btns.addWidget(s_to_ksp_btn)
    ksp_btns.addWidget(ksp_to_s_btn)
    ksp_btns.addStretch(1)
    form.addRow(ksp_btns)
    ksp_status = QLabel(
        "AgCl: n=m=1, s=1.3e-5 → K_sp=1.69e-10.  "
        "PbI₂: n=1, m=2.")
    ksp_status.setWordWrap(True)
    form.addRow(ksp_status)

    def _s_to_ksp():
        try:
            r = calc_equilibrium.ksp_from_solubility(
                s_spin.value(), int(n_spin.value()),
                int(m_spin.value()))
        except ValueError as e:
            ksp_status.setText(f"<b>Error:</b> {e}")
            return
        ksp_spin.blockSignals(True)
        ksp_spin.setValue(r["K_sp"])
        ksp_spin.blockSignals(False)
        ksp_status.setText(f"K_sp = {_fmt_num(r['K_sp'])}")

    def _ksp_to_s():
        try:
            r = calc_equilibrium.solubility_from_ksp(
                ksp_spin.value(), int(n_spin.value()),
                int(m_spin.value()))
        except ValueError as e:
            ksp_status.setText(f"<b>Error:</b> {e}")
            return
        s_spin.blockSignals(True)
        s_spin.setValue(r["molar_solubility"])
        s_spin.blockSignals(False)
        ksp_status.setText(
            f"s = {_fmt_num(r['molar_solubility'])} M")

    s_to_ksp_btn.clicked.connect(_s_to_ksp)
    ksp_to_s_btn.clicked.connect(_ksp_to_s)
    lay.addWidget(panel)

    # ICE solver for A + B ⇌ C + D — 5 inputs + 5 outputs
    # (extent + 4 equilibrium concentrations).  Full-form
    # custom panel.
    ice_panel = QGroupBox("ICE solver — A + B ⇌ C + D (1:1:1:1)")
    ice_form = QFormLayout(ice_panel)
    K_spin = QDoubleSpinBox()
    K_spin.setDecimals(6)
    K_spin.setRange(1e-20, 1e20)
    K_spin.setValue(1.0)
    K_spin.setSuffix("  K")
    a0_spin = QDoubleSpinBox()
    a0_spin.setDecimals(4)
    a0_spin.setRange(0.0, 1000.0)
    a0_spin.setValue(1.0)
    a0_spin.setSuffix("  M")
    b0_spin = QDoubleSpinBox()
    b0_spin.setDecimals(4)
    b0_spin.setRange(0.0, 1000.0)
    b0_spin.setValue(1.0)
    b0_spin.setSuffix("  M")
    c0_spin = QDoubleSpinBox()
    c0_spin.setDecimals(4)
    c0_spin.setRange(0.0, 1000.0)
    c0_spin.setValue(0.0)
    c0_spin.setSuffix("  M")
    d0_spin = QDoubleSpinBox()
    d0_spin.setDecimals(4)
    d0_spin.setRange(0.0, 1000.0)
    d0_spin.setValue(0.0)
    d0_spin.setSuffix("  M")
    ice_form.addRow("K:", K_spin)
    ice_form.addRow("A₀:", a0_spin)
    ice_form.addRow("B₀:", b0_spin)
    ice_form.addRow("C₀:", c0_spin)
    ice_form.addRow("D₀:", d0_spin)
    ice_solve_btn = QPushButton("Solve ICE")
    ice_form.addRow(ice_solve_btn)
    ice_status = QLabel(
        "K = 1, A₀ = B₀ = 1 → x = 0.5; A_eq = B_eq = 0.5; "
        "C_eq = D_eq = 0.5.")
    ice_status.setWordWrap(True)
    ice_form.addRow(ice_status)

    def _solve_ice():
        try:
            r = calc_equilibrium.ice_solve_a_plus_b(
                K=K_spin.value(),
                initial_A=a0_spin.value(),
                initial_B=b0_spin.value(),
                initial_C=c0_spin.value(),
                initial_D=d0_spin.value())
        except ValueError as e:
            ice_status.setText(f"<b>Error:</b> {e}")
            return
        ice_status.setText(
            f"x = {_fmt_num(r['extent_x'])} &nbsp;·&nbsp; "
            f"A_eq = {_fmt_num(r['A_eq'])} &nbsp;·&nbsp; "
            f"B_eq = {_fmt_num(r['B_eq'])} &nbsp;·&nbsp; "
            f"C_eq = {_fmt_num(r['C_eq'])} &nbsp;·&nbsp; "
            f"D_eq = {_fmt_num(r['D_eq'])}")

    ice_solve_btn.clicked.connect(_solve_ice)
    lay.addWidget(ice_panel)

    lay.addStretch(1)
    return page


# ------------------------------------------------------------------
# Dialog
# ------------------------------------------------------------------

#: Tab labels in display order, paired with tab-builder
#: callables.  Surfaced as a class attribute on the dialog so
#: the agent action's `select_tab(label)` can look it up.
_TABS: List[Tuple[str, Callable[[], QWidget]]] = [
    ("Solution", _build_solution_tab),
    ("Stoichiometry", _build_stoich_tab),
    ("Acid-base", _build_acid_base_tab),
    ("Gas law", _build_gas_law_tab),
    ("Colligative", _build_colligative_tab),
    ("Thermo + kinetics", _build_thermo_kinetics_tab),
    ("Equilibrium", _build_equilibrium_tab),
]


class LabCalculatorDialog(QDialog):
    """Tabbed lab-calculator dialog.  Singleton + modeless."""

    _instance: Optional["LabCalculatorDialog"] = None

    @classmethod
    def singleton(cls, parent: Optional[QWidget] = None
                  ) -> "LabCalculatorDialog":
        if cls._instance is None:
            cls._instance = cls(parent=parent)
        return cls._instance

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setWindowTitle("Lab calculator")
        self.setModal(False)
        self.resize(700, 720)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(6, 6, 6, 6)
        self._tabs = QTabWidget()
        for label, builder in _TABS:
            page = builder()
            scroll = QScrollArea()
            scroll.setWidget(page)
            scroll.setWidgetResizable(True)
            self._tabs.addTab(scroll, label)
        outer.addWidget(self._tabs, 1)
        footer = QHBoxLayout()
        footer.addStretch(1)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        footer.addWidget(close_btn)
        outer.addLayout(footer)

    # ---- programmatic API ------------------------------------

    def select_tab(self, label: str) -> bool:
        """Switch to the tab whose label matches.  Returns
        True on success."""
        for i in range(self._tabs.count()):
            if self._tabs.tabText(i).lower() == label.lower():
                self._tabs.setCurrentIndex(i)
                return True
        return False

    def tab_labels(self) -> List[str]:
        return [self._tabs.tabText(i)
                for i in range(self._tabs.count())]
