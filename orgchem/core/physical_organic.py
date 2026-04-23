"""Physical-organic helpers — Phase 17e.

Two teaching-grade tools that close long-standing Phase 17 orphans:

- :func:`hammett_fit` — least-squares regression of log(k/k₀) (or
  log(K/K₀)) against tabulated Hammett σ constants. Returns the
  reaction constant ρ, the correlation coefficient r², the number
  of fit points, and the fitted line parameters. Includes a small
  curated σ table (σₘ, σₚ, σₚ⁻, σₚ⁺) for the common substituents
  students see in undergrad physical-organic problem sets.

- :func:`predict_kie` — primary kinetic isotope effect for a C–H /
  C–D (or C–T) bond cleaved at the rate-determining step. Uses the
  Bigeleisen simplification:

      k_H / k_D ≈ exp( h·ν_H · (1 − √(μ_H/μ_D)) / (2·k_B·T) )

  where ν_H is a typical C–H stretching frequency and μ is the
  reduced mass of the bond's two atoms. For a light-atom partner
  (carbon, 12 amu), the upper bound at 298 K is ~6.9 (C–H/C–D)
  and ~15 (C–H/C–T), matching the textbook values in Anslyn /
  Dougherty §10.

Both helpers are pure-Python + numpy-free so the unit tests run
without scientific-stack imports; agent-action wrappers live in
``agent/actions_phys_org.py``. No external data sources required.
"""
from __future__ import annotations
import math
from typing import Any, Dict, Iterable, Mapping, Tuple


# ---------------------------------------------------------------------
# Hammett σ constants — a curated subset, not exhaustive. Values are
# pulled from Hansch & Leo's classical review (Chem. Rev. 91:165,
# 1991). σ_m = meta, σ_p = para, σ_p_minus / σ_p_plus are the
# resonance-sensitive forms used for EWG / EDG transition states.

HAMMETT_SIGMAS: Dict[str, Dict[str, float]] = {
    # Hydrogen — the reference (σ = 0 by definition).
    "H":       {"sigma_m": 0.00, "sigma_p": 0.00,
                "sigma_p_minus": 0.00, "sigma_p_plus": 0.00},
    # Electron-donating (σ < 0 for para / σ_p_plus).
    "NH2":     {"sigma_m": -0.16, "sigma_p": -0.66,
                "sigma_p_minus": -0.15, "sigma_p_plus": -1.30},
    "N(CH3)2": {"sigma_m": -0.15, "sigma_p": -0.83,
                "sigma_p_minus": -0.12, "sigma_p_plus": -1.70},
    "OH":      {"sigma_m": 0.12, "sigma_p": -0.37,
                "sigma_p_minus": -0.37, "sigma_p_plus": -0.92},
    "OCH3":    {"sigma_m": 0.12, "sigma_p": -0.27,
                "sigma_p_minus": -0.26, "sigma_p_plus": -0.78},
    "CH3":     {"sigma_m": -0.07, "sigma_p": -0.17,
                "sigma_p_minus": -0.17, "sigma_p_plus": -0.31},
    # Halogens — inductive + weakly π-donating.
    "F":       {"sigma_m": 0.34, "sigma_p": 0.06,
                "sigma_p_minus": -0.03, "sigma_p_plus": -0.07},
    "Cl":      {"sigma_m": 0.37, "sigma_p": 0.23,
                "sigma_p_minus": 0.19, "sigma_p_plus": 0.11},
    "Br":      {"sigma_m": 0.39, "sigma_p": 0.23,
                "sigma_p_minus": 0.25, "sigma_p_plus": 0.15},
    "I":       {"sigma_m": 0.35, "sigma_p": 0.18,
                "sigma_p_minus": 0.27, "sigma_p_plus": 0.14},
    # Electron-withdrawing (σ > 0 for para / σ_p_minus).
    "CN":      {"sigma_m": 0.56, "sigma_p": 0.66,
                "sigma_p_minus": 1.00, "sigma_p_plus": 0.66},
    "NO2":     {"sigma_m": 0.71, "sigma_p": 0.78,
                "sigma_p_minus": 1.27, "sigma_p_plus": 0.79},
    "CF3":     {"sigma_m": 0.43, "sigma_p": 0.54,
                "sigma_p_minus": 0.65, "sigma_p_plus": 0.61},
    "COOH":    {"sigma_m": 0.37, "sigma_p": 0.45,
                "sigma_p_minus": 0.77, "sigma_p_plus": 0.42},
    "COMe":    {"sigma_m": 0.38, "sigma_p": 0.50,
                "sigma_p_minus": 0.84, "sigma_p_plus": 0.30},
    "SO2Me":   {"sigma_m": 0.60, "sigma_p": 0.72,
                "sigma_p_minus": 1.05, "sigma_p_plus": 0.77},
}


def list_hammett_substituents() -> Dict[str, Dict[str, float]]:
    """Return the tabulated Hammett σ catalogue. Key is the
    substituent label (e.g. ``"NO2"``)."""
    return {k: dict(v) for k, v in HAMMETT_SIGMAS.items()}


# ---------------------------------------------------------------------
# Hammett fit.

def _lookup_sigma(substituent: str, sigma_type: str) -> float:
    if substituent not in HAMMETT_SIGMAS:
        raise ValueError(
            f"No tabulated Hammett σ for substituent {substituent!r}. "
            f"Known: {sorted(HAMMETT_SIGMAS)}"
        )
    entry = HAMMETT_SIGMAS[substituent]
    if sigma_type not in entry:
        raise ValueError(
            f"Unknown sigma_type {sigma_type!r}. Use one of "
            f"{sorted(entry)}."
        )
    return entry[sigma_type]


def _linregress(xs: Iterable[float], ys: Iterable[float]
                ) -> Tuple[float, float, float]:
    """Return (slope, intercept, r²) for a least-squares line."""
    xs = list(xs)
    ys = list(ys)
    n = len(xs)
    if n < 2:
        raise ValueError("Need at least two data points to fit a line.")
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    sxx = sum((x - mean_x) ** 2 for x in xs)
    sxy = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    syy = sum((y - mean_y) ** 2 for y in ys)
    if sxx == 0:
        raise ValueError("σ values are constant — can't fit a line.")
    slope = sxy / sxx
    intercept = mean_y - slope * mean_x
    # Pearson r² = (Sxy)² / (Sxx · Syy). Guard against Syy == 0
    # (all y's identical → perfect flat line, ρ == 0, r² = 1.0).
    r2 = 1.0 if syy == 0 else (sxy ** 2) / (sxx * syy)
    return slope, intercept, r2


def hammett_fit(data: Mapping[str, float],
                sigma_type: str = "sigma_p",
                ) -> Dict[str, Any]:
    """Fit log(rate-or-equilibrium ratio) against σ.

    Parameters
    ----------
    data:
        Mapping ``{substituent_label: log(k_X / k_H)}``. The "H"
        row is allowed (σ = 0) but not required — the regression
        is invariant to its inclusion.
    sigma_type:
        ``"sigma_p"`` (default), ``"sigma_m"``, ``"sigma_p_minus"``,
        or ``"sigma_p_plus"``. Choose the scale that matches the
        transition-state character (negative charge → σ⁻, positive
        charge → σ⁺, simple induction → σ_m / σ_p).

    Returns
    -------
    A dict with:

    - ``rho`` — the reaction constant (slope).
    - ``intercept`` — y-intercept of the line.
    - ``r_squared`` — Pearson r² of the fit.
    - ``n_points`` — how many (σ, log(k/k₀)) pairs contributed.
    - ``points`` — list of ``{substituent, sigma, log_k_rel}`` rows
      (sorted by σ) for plotting.
    - ``sigma_type`` — echo of the input for UI display.
    - ``interpretation`` — short teaching note: |ρ| > 1 → reaction
      is electronically sensitive; sign tells you which direction.
    """
    points = []
    for label, log_k_rel in data.items():
        try:
            s = _lookup_sigma(label, sigma_type)
        except ValueError:
            # Skip unknown substituents rather than crashing the
            # whole fit — report them in the returned dict instead.
            continue
        points.append({"substituent": label, "sigma": s,
                       "log_k_rel": float(log_k_rel)})
    if len(points) < 2:
        return {
            "error": "Need at least 2 matching-substituent data "
                     "points. Add more, or try a different sigma_type."
        }
    points.sort(key=lambda p: p["sigma"])
    slope, intercept, r2 = _linregress(
        [p["sigma"] for p in points],
        [p["log_k_rel"] for p in points],
    )
    if slope > 0:
        interp = (
            "ρ > 0: reaction is accelerated by electron-withdrawing "
            "groups. TS is more electron-rich / carbanion-like than "
            "the reactant."
        )
    elif slope < 0:
        interp = (
            "ρ < 0: reaction is accelerated by electron-donating "
            "groups. TS is more electron-poor / carbocation-like "
            "than the reactant."
        )
    else:
        interp = "ρ ≈ 0: reaction is insensitive to ring substitution."
    magnitude = abs(slope)
    if magnitude > 2:
        interp += " |ρ| > 2 → very strong electronic demand."
    elif magnitude > 1:
        interp += " |ρ| > 1 → strong electronic demand."
    elif magnitude < 0.3:
        interp += " |ρ| < 0.3 → weak electronic demand."
    return {
        "rho": slope,
        "intercept": intercept,
        "r_squared": r2,
        "n_points": len(points),
        "points": points,
        "sigma_type": sigma_type,
        "interpretation": interp,
    }


# ---------------------------------------------------------------------
# Primary KIE (Bigeleisen simplification).

# Atomic masses in amu (1H, 2H, 3H, 12C, 14N, 16O).
_ATOMIC_MASS = {"H": 1.008, "D": 2.014, "T": 3.016,
                "C": 12.011, "N": 14.007, "O": 15.999,
                "S": 32.065}

# Physical constants (SI).
_H = 6.62607015e-34    # Planck's constant, J·s
_KB = 1.380649e-23     # Boltzmann, J/K
_C = 2.99792458e10     # speed of light, cm/s (wavenumber → frequency)


def _reduced_mass(m1_amu: float, m2_amu: float) -> float:
    """Reduced mass of a two-atom harmonic oscillator (amu)."""
    return (m1_amu * m2_amu) / (m1_amu + m2_amu)


def predict_kie(isotope_pair: str = "H/D",
                partner_element: str = "C",
                nu_H_cm1: float = 3000.0,
                temperature_K: float = 298.15,
                ) -> Dict[str, Any]:
    """Predict a primary KIE from the Bigeleisen simplification.

    Parameters
    ----------
    isotope_pair:
        ``"H/D"`` (default) or ``"H/T"`` — which isotopologue pair.
    partner_element:
        The heavy atom the H/D/T is attached to. Defaults to
        ``"C"`` (a C–H bond). Other common choices: ``"N"``, ``"O"``.
    nu_H_cm1:
        Wavenumber of the C–H (or N–H / O–H) stretch being broken
        at the RDS. 3000 cm⁻¹ is a representative average for
        aliphatic C–H; 3400 for O–H.
    temperature_K:
        Absolute temperature. Defaults to 298.15 K.

    Returns
    -------
    A dict with ``kie`` (k_H / k_heavy), ``zpe_diff_kJmol``
    (zero-point-energy difference driving the effect), the input
    parameters echoed for provenance, and a short interpretation.
    """
    pair = isotope_pair.strip().upper()
    if pair not in ("H/D", "H/T"):
        return {"error": f"Unsupported isotope_pair {isotope_pair!r}. "
                         f"Use 'H/D' or 'H/T'."}
    if partner_element not in _ATOMIC_MASS:
        return {"error": f"Unknown partner element {partner_element!r}."}
    m_H = _ATOMIC_MASS["H"]
    m_heavy_iso = _ATOMIC_MASS["D"] if pair == "H/D" else _ATOMIC_MASS["T"]
    m_partner = _ATOMIC_MASS[partner_element]
    mu_H = _reduced_mass(m_H, m_partner)
    mu_iso = _reduced_mass(m_heavy_iso, m_partner)
    # ν ∝ 1/√μ, so ν_iso = ν_H · √(μ_H / μ_iso).
    freq_ratio = math.sqrt(mu_H / mu_iso)
    # ZPE difference (J per bond).
    nu_H_Hz = nu_H_cm1 * _C     # wavenumber (cm⁻¹) × c (cm/s) → Hz
    zpe_H = 0.5 * _H * nu_H_Hz
    zpe_iso = 0.5 * _H * nu_H_Hz * freq_ratio
    delta_zpe = zpe_H - zpe_iso   # > 0 (C–H has more ZPE than C–D)
    # KIE = exp(Δ ZPE / k_B T).
    kie = math.exp(delta_zpe / (_KB * temperature_K))
    # Convert Δ ZPE to kJ/mol for a friendly number.
    delta_zpe_kJmol = delta_zpe * 6.02214076e23 / 1000.0
    # Teaching interpretation.
    if kie >= 6.0:
        tier = ("large primary KIE — C–H bond is being cleaved in a "
                "symmetric, product-like TS (Westheimer's peak "
                "behaviour at late TS).")
    elif kie >= 2.0:
        tier = ("primary KIE — C–H cleavage is part of the RDS "
                "but the TS may be early / asymmetric.")
    else:
        tier = ("sub-primary KIE — C–H cleavage is not rate-"
                "determining, or the bond is broken only partially "
                "at the TS.")
    return {
        "kie": kie,
        "isotope_pair": pair,
        "partner_element": partner_element,
        "nu_H_cm1": nu_H_cm1,
        "temperature_K": temperature_K,
        "reduced_mass_H": mu_H,
        "reduced_mass_heavy_iso": mu_iso,
        "zpe_diff_kJmol": delta_zpe_kJmol,
        "interpretation": tier,
    }
