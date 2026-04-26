"""Phase 37d (round 139) — headless tests for the
spectrophotometry-method catalogue + Beer-Lambert solver +
agent actions.
"""
from __future__ import annotations
import math
import os

import pytest


# ---- catalogue contents ---------------------------------------

def test_catalogue_size_at_least_twelve():
    from orgchem.core.spectrophotometry_methods import list_methods
    assert len(list_methods()) >= 12


def test_five_categories_all_represented():
    from orgchem.core.spectrophotometry_methods import (
        VALID_CATEGORIES, list_methods,
    )
    seen = {m.category for m in list_methods()}
    assert seen == set(VALID_CATEGORIES), \
        f"missing: {set(VALID_CATEGORIES) - seen}"


def test_each_method_has_required_fields():
    from orgchem.core.spectrophotometry_methods import list_methods
    for m in list_methods():
        assert m.id, f"missing id"
        assert m.name, f"missing name on {m.id}"
        assert m.abbreviation, f"missing abbrev on {m.id}"
        assert m.category, f"missing category on {m.id}"
        assert m.principle, f"missing principle on {m.id}"
        assert m.light_source, f"missing source on {m.id}"
        assert m.sample_handling, f"missing sample-handling on {m.id}"
        assert m.detector, f"missing detector on {m.id}"
        assert m.wavelength_range, f"missing wavelength on {m.id}"
        assert m.typical_analytes, \
            f"missing typical_analytes on {m.id}"
        assert m.strengths, f"missing strengths on {m.id}"
        assert m.limitations, f"missing limitations on {m.id}"
        assert m.procedure, f"missing procedure on {m.id}"


def test_canonical_methods_present():
    """The user-explicitly-requested methods + the major
    catalogue entries."""
    from orgchem.core.spectrophotometry_methods import get_method
    for must in ("uv_vis", "fluorescence", "ir_ftir",
                 "atr_ftir", "nir", "raman", "sers", "cd",
                 "aas", "icp_oes", "icp_ms", "nmr"):
        assert get_method(must) is not None, \
            f"missing method {must}"


# ---- teaching invariants on individual rows -------------------

def test_uv_vis_describes_beer_lambert():
    from orgchem.core.spectrophotometry_methods import get_method
    body = get_method("uv_vis").principle.lower()
    assert "beer" in body or "ε·l·c" in body \
        or "molar absorptivity" in body


def test_fluorescence_describes_stokes_shift():
    from orgchem.core.spectrophotometry_methods import get_method
    body = (get_method("fluorescence").principle
            + get_method("fluorescence").notes).lower()
    assert "stokes" in body or "quantum yield" in body


def test_ir_ftir_cross_references_predictor():
    """The IR catalogue entry should point at the existing
    `core/spectroscopy.py` band predictor for the predictive
    use case — keeps the two layers of the app integrated
    in the user's mental model."""
    from orgchem.core.spectrophotometry_methods import get_method
    notes = get_method("ir_ftir").notes.lower()
    assert "spectroscopy" in notes or "predictor" in notes \
        or "predict" in notes


def test_atr_ftir_mentions_no_sample_prep():
    from orgchem.core.spectrophotometry_methods import get_method
    body = (get_method("atr_ftir").sample_handling
            + get_method("atr_ftir").strengths).lower()
    assert ("no sample prep" in body or "no prep" in body
            or "zero sample prep" in body)


def test_raman_describes_complementary_to_ir():
    from orgchem.core.spectrophotometry_methods import get_method
    body = (get_method("raman").principle
            + get_method("raman").strengths).lower()
    assert "complementary" in body or "polarisability" in body


def test_sers_describes_enhancement_factor():
    from orgchem.core.spectrophotometry_methods import get_method
    body = (get_method("sers").principle
            + get_method("sers").strengths).lower()
    assert "10⁴" in body or "10⁶" in body or "enhanc" in body


def test_cd_describes_secondary_structure():
    from orgchem.core.spectrophotometry_methods import get_method
    body = get_method("cd").typical_analytes.lower()
    assert "secondary structure" in body \
        or "α-helix" in body or "β-sheet" in body


def test_nmr_cross_references_predictor():
    from orgchem.core.spectrophotometry_methods import get_method
    notes = get_method("nmr").notes.lower()
    assert "core/nmr" in notes or "predictor" in notes \
        or "shift predictor" in notes


def test_icp_ms_mentions_polyatomic_interferences():
    from orgchem.core.spectrophotometry_methods import get_method
    body = (get_method("icp_ms").limitations
            + get_method("icp_ms").procedure).lower()
    assert "polyatomic" in body or "interfer" in body


# ---- filter / lookup -----------------------------------------

def test_list_filtered_by_category():
    from orgchem.core.spectrophotometry_methods import list_methods
    ir = list_methods(category="molecular-ir")
    assert all(m.category == "molecular-ir" for m in ir)
    # IR / FTIR + ATR-FTIR + NIR + Raman + SERS = 5
    assert len(ir) == 5
    atomic = list_methods(category="atomic")
    assert len(atomic) == 3   # AAS + ICP-OES + ICP-MS


def test_list_unknown_category_returns_empty():
    from orgchem.core.spectrophotometry_methods import list_methods
    assert list_methods(category="not-a-real-category") == []


def test_get_unknown_id_returns_none():
    from orgchem.core.spectrophotometry_methods import get_method
    assert get_method("does-not-exist") is None


def test_find_methods_substring_case_insensitive():
    from orgchem.core.spectrophotometry_methods import find_methods
    a = {m.id for m in find_methods("RAMAN")}
    b = {m.id for m in find_methods("raman")}
    assert a == b
    assert "raman" in a and "sers" in a   # SERS name contains "raman"


def test_find_methods_empty_returns_empty():
    from orgchem.core.spectrophotometry_methods import find_methods
    assert find_methods("") == []


# ---- Beer-Lambert solver --------------------------------------

def test_beer_lambert_solve_for_concentration():
    from orgchem.core.spectrophotometry_methods import (
        beer_lambert_solve,
    )
    res = beer_lambert_solve(
        absorbance=0.42, molar_absorptivity=10500.0,
        path_length_cm=1.0)
    assert math.isclose(res["concentration_M"], 4.0e-5,
                        rel_tol=1e-6)
    # All four keys present.
    assert set(res.keys()) == {
        "absorbance", "molar_absorptivity",
        "path_length_cm", "concentration_M",
    }


def test_beer_lambert_solve_for_absorbance():
    from orgchem.core.spectrophotometry_methods import (
        beer_lambert_solve,
    )
    res = beer_lambert_solve(
        molar_absorptivity=10500.0,
        path_length_cm=1.0, concentration_M=4.0e-5)
    assert math.isclose(res["absorbance"], 0.42, rel_tol=1e-6)


def test_beer_lambert_solve_for_path_length():
    from orgchem.core.spectrophotometry_methods import (
        beer_lambert_solve,
    )
    res = beer_lambert_solve(
        absorbance=0.84, molar_absorptivity=10500.0,
        concentration_M=4.0e-5)
    assert math.isclose(res["path_length_cm"], 2.0, rel_tol=1e-6)


def test_beer_lambert_solve_for_molar_absorptivity():
    from orgchem.core.spectrophotometry_methods import (
        beer_lambert_solve,
    )
    res = beer_lambert_solve(
        absorbance=0.42, path_length_cm=1.0,
        concentration_M=4.0e-5)
    assert math.isclose(res["molar_absorptivity"], 10500.0,
                        rel_tol=1e-6)


def test_beer_lambert_rejects_two_missing():
    from orgchem.core.spectrophotometry_methods import (
        beer_lambert_solve,
    )
    with pytest.raises(ValueError):
        beer_lambert_solve(absorbance=0.5)


def test_beer_lambert_rejects_zero_or_negative():
    from orgchem.core.spectrophotometry_methods import (
        beer_lambert_solve,
    )
    with pytest.raises(ValueError):
        beer_lambert_solve(absorbance=-0.1, molar_absorptivity=1.0,
                           path_length_cm=1.0)
    with pytest.raises(ValueError):
        beer_lambert_solve(absorbance=0.5, molar_absorptivity=1.0,
                           path_length_cm=0.0)


# ---- to_dict serialisation ------------------------------------

def test_to_dict_keys():
    from orgchem.core.spectrophotometry_methods import (
        get_method, to_dict,
    )
    d = to_dict(get_method("uv_vis"))
    expected = {
        "id", "name", "abbreviation", "category", "principle",
        "light_source", "sample_handling", "detector",
        "wavelength_range", "typical_analytes", "strengths",
        "limitations", "procedure", "notes",
    }
    assert set(d.keys()) == expected


# ---- agent actions --------------------------------------------

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(5)
        yield h


def test_action_list_methods(app):
    rows = app.call("list_spectrophotometry_methods")
    assert len(rows) >= 12


def test_action_list_methods_filtered(app):
    rows = app.call("list_spectrophotometry_methods",
                    category="atomic")
    assert all(r["category"] == "atomic" for r in rows)
    assert len(rows) == 3


def test_action_list_methods_unknown_category_errors(app):
    rows = app.call("list_spectrophotometry_methods",
                    category="bogus")
    assert len(rows) == 1
    assert "error" in rows[0]


def test_action_get_method(app):
    r = app.call("get_spectrophotometry_method",
                 method_id="uv_vis")
    assert "error" not in r
    assert r["abbreviation"] == "UV-Vis"


def test_action_get_unknown_method(app):
    r = app.call("get_spectrophotometry_method",
                 method_id="bogus")
    assert "error" in r


def test_action_find_methods(app):
    rows = app.call("find_spectrophotometry_methods",
                    needle="uv")
    ids = {r["id"] for r in rows}
    assert "uv_vis" in ids


def test_action_beer_lambert_solve_for_concentration(app):
    res = app.call("beer_lambert",
                   absorbance=0.42,
                   molar_absorptivity=10500.0,
                   path_length_cm=1.0)
    assert "error" not in res
    assert math.isclose(res["concentration_M"], 4.0e-5,
                        rel_tol=1e-6)


def test_action_beer_lambert_error_path(app):
    res = app.call("beer_lambert", absorbance=0.5)
    assert "error" in res
