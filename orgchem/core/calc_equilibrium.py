"""Phase 39a (round 142) — equilibrium calculators.

- K_eq from a list of {species, concentration, stoichiometric
  coefficient, side} entries.
- K_sp ↔ molar solubility.
- ICE-table solver for a simple A + B ⇌ C + D equilibrium step
  (closed-form quadratic).
"""
from __future__ import annotations
import math
from typing import Dict, List, Optional


def equilibrium_constant_from_concentrations(
    species: List[Dict[str, object]],
) -> Dict[str, float]:
    """Compute K_eq from a list of equilibrium-species entries.

    Each entry: ``{"name", "concentration_M", "stoich_coeff",
    "side"}`` where ``side`` is ``"product"`` or ``"reactant"``.

    K_eq = Π[product]^coeff / Π[reactant]^coeff.
    """
    if not species:
        raise ValueError("Need ≥ 1 species.")
    numerator = 1.0
    denominator = 1.0
    for i, s in enumerate(species):
        for k in ("name", "concentration_M",
                  "stoich_coeff", "side"):
            if k not in s:
                raise ValueError(
                    f"species[{i}] missing key {k!r}.")
        c = s["concentration_M"]
        coeff = s["stoich_coeff"]
        side = s["side"]
        if not isinstance(c, (int, float)) or c <= 0:
            raise ValueError(
                f"species[{i}].concentration_M must be > 0.")
        if not isinstance(coeff, (int, float)) or coeff <= 0:
            raise ValueError(
                f"species[{i}].stoich_coeff must be > 0.")
        if side == "product":
            numerator *= (c ** coeff)
        elif side == "reactant":
            denominator *= (c ** coeff)
        else:
            raise ValueError(
                f"species[{i}].side must be 'product' or "
                f"'reactant'; got {side!r}.")
    if denominator == 0:
        raise ValueError("denominator (reactant product) is zero")
    return {
        "K_eq": numerator / denominator,
        "numerator": numerator,
        "denominator": denominator,
        "n_species": len(species),
    }


# ------------------------------------------------------------------
# K_sp ↔ molar solubility for a simple AnBm salt:
#   AnBm  →  n A^z+  +  m B^z-
#   K_sp = [A]^n · [B]^m  =  (n·s)^n · (m·s)^m
# ------------------------------------------------------------------

def ksp_from_solubility(
    molar_solubility: float,
    n: int,
    m: int,
) -> Dict[str, float]:
    """K_sp = (n·s)^n · (m·s)^m.

    Example: AgCl (n=m=1, s=1.3e-5) → K_sp = 1.7e-10.
    Example: PbI₂ (n=1, m=2, s=1.5e-3) → K_sp = 1.4e-8.
    """
    if molar_solubility <= 0:
        raise ValueError(
            f"molar_solubility must be > 0; got "
            f"{molar_solubility!r}.")
    if n < 1 or m < 1:
        raise ValueError("n, m must be ≥ 1 (integer ratios).")
    K_sp = ((n * molar_solubility) ** n
            * (m * molar_solubility) ** m)
    return {
        "K_sp": K_sp, "molar_solubility": molar_solubility,
        "n": n, "m": m,
    }


def solubility_from_ksp(
    K_sp: float,
    n: int,
    m: int,
) -> Dict[str, float]:
    """Inverse of :func:`ksp_from_solubility`.  Solves
    K_sp = (n·s)^n · (m·s)^m for s, the molar solubility of
    a simple AnBm salt.

    Closed form: s = (K_sp / (n^n · m^m))^(1 / (n + m)).
    """
    if K_sp <= 0:
        raise ValueError(f"K_sp must be > 0; got {K_sp!r}.")
    if n < 1 or m < 1:
        raise ValueError("n, m must be ≥ 1 (integer ratios).")
    s = (K_sp / ((n ** n) * (m ** m))) ** (1.0 / (n + m))
    return {
        "molar_solubility": s, "K_sp": K_sp,
        "n": n, "m": m,
    }


# ------------------------------------------------------------------
# ICE table for a 1-stage 1:1:1:1 equilibrium step
#   A + B ⇌ C + D
# Returns equilibrium concentrations given the K + initial
# concentrations.  Closed-form quadratic.
# ------------------------------------------------------------------

def ice_solve_a_plus_b(
    K: float,
    initial_A: float,
    initial_B: float,
    initial_C: float = 0.0,
    initial_D: float = 0.0,
) -> Dict[str, float]:
    """Solve the ICE table for A + B ⇌ C + D with all
    coefficients = 1.

    Lets x = extent of reaction (amount of A + B consumed).
    Equilibrium: A=A₀-x, B=B₀-x, C=C₀+x, D=D₀+x.
    K = (C₀+x)(D₀+x) / ((A₀-x)(B₀-x)) → quadratic in x.

    Picks the chemically-meaningful root (0 ≤ x ≤
    min(A₀, B₀) when going forward, or analogous bound going
    reverse).  Raises ``ValueError`` if neither root lies in
    the valid range (typically a sign of impossible inputs).
    """
    if K <= 0:
        raise ValueError(f"K must be > 0; got {K!r}.")
    for n, v in (("initial_A", initial_A),
                 ("initial_B", initial_B),
                 ("initial_C", initial_C),
                 ("initial_D", initial_D)):
        if v < 0:
            raise ValueError(f"{n} must be ≥ 0; got {v!r}.")
    if initial_A == 0 and initial_B == 0:
        raise ValueError(
            "Both reactants start at zero — no forward "
            "reaction possible.")
    # Quadratic ax² + bx + c = 0 from (C₀+x)(D₀+x) =
    # K·(A₀-x)(B₀-x).
    a = 1.0 - K
    b = (initial_C + initial_D) + K * (initial_A + initial_B)
    c = initial_C * initial_D - K * initial_A * initial_B
    if abs(a) < 1e-12:
        # Degenerate (K = 1): linear equation.
        if abs(b) < 1e-12:
            raise ValueError("ICE solve degenerated to 0 = c.")
        x = -c / b
    else:
        disc = b * b - 4 * a * c
        if disc < 0:
            raise ValueError(
                f"ICE quadratic has no real root; disc={disc}.")
        sqrt_disc = math.sqrt(disc)
        x_plus = (-b + sqrt_disc) / (2 * a)
        x_minus = (-b - sqrt_disc) / (2 * a)
        # Pick the root that leaves all concentrations ≥ 0.
        x = _pick_chem_root(x_plus, x_minus, initial_A, initial_B,
                            initial_C, initial_D)
    return {
        "extent_x": x,
        "A_eq": initial_A - x,
        "B_eq": initial_B - x,
        "C_eq": initial_C + x,
        "D_eq": initial_D + x,
        "K": K,
    }


def _pick_chem_root(x1: float, x2: float, A0: float, B0: float,
                    C0: float, D0: float) -> float:
    """Pick the ICE root that leaves all concentrations
    physically sensible (≥ 0)."""
    def valid(x: float) -> bool:
        return (A0 - x >= -1e-9 and B0 - x >= -1e-9
                and C0 + x >= -1e-9 and D0 + x >= -1e-9)
    candidates = [x for x in (x1, x2) if valid(x)]
    if not candidates:
        raise ValueError(
            "Neither ICE root produces physical "
            "concentrations.")
    # If multiple valid roots, pick the smaller magnitude
    # (closer to equilibrium starting position).
    return min(candidates, key=abs)
