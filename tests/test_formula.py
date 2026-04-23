"""Unit tests for the empirical/molecular formula calculator.

Validates every worked example in Verma et al. 2024 Table 1 (Nicotine,
Caffeine, D-Glucose, Cholesterol, Porphyrin, Corannulene, Codeine) under
both IUPAC 2019 atomic masses (default) and the paper's whole-number
masses. Cholesterol is the case that motivated the move away from the
paper's ratio-normalise algorithm: 46 hydrogens × 0.8 % mass error inflates
past any sensible tolerance with IUPAC masses.
"""
from __future__ import annotations
import pytest

from orgchem.core.formula import compute_formula, ATOMIC_MASSES_INTEGER


# ---- default (IUPAC 2019) masses ------------------------------------------

def test_nicotine():
    r = compute_formula({"C": 74.00, "H": 8.70, "N": 17.27}, 162.0)
    assert r.empirical_formula == "C5H7N"
    assert r.molecular_formula == "C10H14N2"


def test_caffeine():
    r = compute_formula({"C": 49.38, "H": 5.16, "N": 28.76, "O": 16.70}, 194.19)
    assert r.empirical_formula == "C4H5N2O"
    assert r.molecular_formula == "C8H10N4O2"


def test_d_glucose():
    r = compute_formula({"C": 40.00, "H": 6.67, "O": 53.33}, 180.0)
    assert r.empirical_formula == "CH2O"
    assert r.molecular_formula == "C6H12O6"


def test_cholesterol_with_iupac_masses():
    """The case that broke the paper's algorithm under IUPAC masses."""
    r = compute_formula({"C": 83.87, "H": 11.91, "O": 4.14}, 386.27)
    assert r.molecular_formula == "C27H46O"
    assert r.empirical_formula == "C27H46O"
    assert r.max_residual < 0.4


def test_porphyrin():
    r = compute_formula({"C": 77.33, "H": 4.51, "N": 18.04}, 310.35)
    assert r.empirical_formula == "C10H7N2"
    assert r.molecular_formula == "C20H14N4"


def test_codeine():
    r = compute_formula({"C": 72.00, "H": 7.08, "N": 4.69, "O": 16.22}, 299.30)
    assert r.molecular_formula == "C18H21NO3"


# ---- paper-exact reproduction (integer masses) ---------------------------

def test_cholesterol_with_paper_masses():
    r = compute_formula(
        {"C": 83.87, "H": 11.91, "O": 4.14}, 386.27,
        masses=ATOMIC_MASSES_INTEGER,
    )
    assert r.molecular_formula == "C27H46O"


# ---- error handling ------------------------------------------------------

def test_invalid_element():
    with pytest.raises(ValueError):
        compute_formula({"Xx": 50.0, "H": 50.0}, 100.0)


def test_negative_mass():
    with pytest.raises(ValueError):
        compute_formula({"C": 40.0, "H": 6.67, "O": 53.33}, -1.0)


def test_inconsistent_inputs_rejected():
    """Percentages summing to garbage (e.g. 200) should be flagged."""
    with pytest.raises(ValueError):
        # 100% H in a 386 g/mol compound would imply 383 H atoms in 1 O:
        # impossible, and the residual will blow past tol.
        compute_formula({"H": 100.0}, 3.14, tol=0.1)
