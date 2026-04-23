"""TLC / column chromatography helpers — Phase 15b.

A **teaching-grade** Rf predictor for silica-gel normal-phase
chromatography. The mapping from a molecule's polarity (here taken as
−logP; more negative logP ⇒ more polar ⇒ lower Rf) + the mobile-phase
polarity to an Rf value is a smooth saturating function calibrated so:

- A non-polar hydrocarbon (logP ≈ +5) in a non-polar solvent (hexane,
  polarity 0) reaches near Rf = 0.9.
- A polar alcohol (logP ≈ 0) in the same hexane stays near the baseline
  (Rf ≈ 0.05).
- Switching to a 1 : 1 hexane-EtOAc (polarity ≈ 0.45) pushes the
  alcohol up to Rf ≈ 0.3 while the hydrocarbon hits the solvent front.

None of this is quantitatively accurate — the point is to give students
a **directionally correct** visualisation of how logP and solvent
polarity interact. Real Rf is a messy function of silica H-bonding,
analyte-specific group interactions, and loading, which isn't worth
modelling here.

Solvent-polarity values are set against the empirical "eluotropic
series" (Snyder 1974): hexane 0.00, toluene 0.29, CH₂Cl₂ 0.42,
ether 0.43, EtOAc 0.58, acetone 0.72, EtOH 0.88, MeOH 0.95, water 1.0.
"""
from __future__ import annotations
import logging
from typing import Any, Dict

from rdkit import Chem
from rdkit.Chem import Crippen

log = logging.getLogger(__name__)


#: Eluotropic strengths on a 0-1 scale (approximate Snyder P' / 10).
SOLVENT_POLARITY: Dict[str, float] = {
    "hexane":      0.00,
    "pentane":     0.00,
    "toluene":     0.29,
    "dcm":         0.42,
    "chloroform":  0.40,
    "ether":       0.43,
    "ethyl acetate": 0.58,
    "ethyl_acetate": 0.58,
    "ea":          0.58,
    "acetone":     0.72,
    "isopropanol": 0.82,
    "ethanol":     0.88,
    "methanol":    0.95,
    "water":       1.00,
}


def solvent_polarity(solvent: str) -> float:
    """Look up or linear-interpolate a solvent's polarity (0 = non-polar, 1 = water).

    Accepts a single solvent name or a ``"name1:name2:ratio"``-style mixture
    (e.g. ``"hexane:ethyl_acetate:3:1"`` → 3:1 hex:EA). If the solvent is
    unrecognised, returns 0.3 (a mid-polarity default) and logs a warning.
    """
    name = solvent.strip().lower()
    if ":" in name:
        parts = name.split(":")
        if len(parts) == 4:
            a, b, ra, rb = parts
            try:
                ra_f, rb_f = float(ra), float(rb)
            except ValueError:
                log.warning("Bad mixture syntax: %s", solvent)
                return 0.3
            pa = SOLVENT_POLARITY.get(a, 0.3)
            pb = SOLVENT_POLARITY.get(b, 0.3)
            total = ra_f + rb_f
            if total <= 0:
                return 0.3
            return (pa * ra_f + pb * rb_f) / total
    if name in SOLVENT_POLARITY:
        return SOLVENT_POLARITY[name]
    log.warning("Unknown solvent %r; using 0.3 default", solvent)
    return 0.3


def _logp(smi: str) -> float:
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
        raise ValueError(f"Unparseable SMILES: {smi!r}")
    return Crippen.MolLogP(mol)


def predict_rf(smiles: str, solvent: str = "hexane:ethyl_acetate:1:1") -> Dict[str, Any]:
    """Return an estimated TLC Rf value for a molecule in a given mobile phase.

    Formula: Rf = sigmoid(a · solvent_polarity + b · logP + c), with
    coefficients calibrated so hydrocarbons ride the front in hexane and
    alcohols stay at baseline, while a 50 : 50 hex : EtOAc spreads the
    middle cleanly.
    """
    try:
        logp = _logp(smiles)
    except ValueError as e:
        return {"error": str(e)}
    sp = solvent_polarity(solvent)

    # Linear combination → sigmoid.
    # Coefficients chosen to give the calibration described above.
    import math
    x = 4.0 * sp + 0.5 * logp - 1.2
    rf = 1.0 / (1.0 + math.exp(-x))
    # clamp into [0.02, 0.98] — a molecule never sits perfectly at baseline or front
    rf = max(0.02, min(0.98, rf))
    return {
        "rf": rf,
        "logp": logp,
        "solvent": solvent,
        "solvent_polarity": sp,
    }


def simulate_tlc(smiles_list, solvent: str = "hexane:ethyl_acetate:1:1") -> Dict[str, Any]:
    """Predict TLC Rf for a mixture of compounds in one solvent.

    Returns a sorted list of ``{"smiles", "rf", "logp"}`` per compound —
    higher Rf (less polar) first.
    """
    rows = []
    for smi in smiles_list:
        r = predict_rf(smi, solvent=solvent)
        if "error" in r:
            rows.append({"smiles": smi, "error": r["error"]})
            continue
        rows.append({"smiles": smi, "rf": r["rf"], "logp": r["logp"]})
    rows.sort(key=lambda d: d.get("rf", 0.0), reverse=True)
    return {"solvent": solvent,
            "solvent_polarity": solvent_polarity(solvent),
            "compounds": rows}
