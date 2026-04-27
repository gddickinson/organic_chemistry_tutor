"""Phase GM-1.0 (round 230) — tests for the
``genetics.agent.actions_techniques`` agent-action layer.
"""
from __future__ import annotations
import pytest


# ----------------------------------------------------------------
# Registration
# ----------------------------------------------------------------

def test_all_five_actions_registered():
    """The five GM-1.0 actions must all register into the
    shared ``orgchem.agent.actions._REGISTRY``."""
    from orgchem.agent.actions import registry
    reg = registry()
    expected = (
        "list_genetics_techniques",
        "get_genetics_technique",
        "find_genetics_techniques",
        "genetics_techniques_for_application",
        "open_genetics_studio",
    )
    for name in expected:
        assert name in reg, \
            f"Action {name!r} not registered"


def test_all_five_actions_have_genetics_techniques_category():
    from orgchem.agent.actions import _REGISTRY
    expected = (
        "list_genetics_techniques",
        "get_genetics_technique",
        "find_genetics_techniques",
        "genetics_techniques_for_application",
        "open_genetics_studio",
    )
    for name in expected:
        spec = _REGISTRY[name]
        assert spec.category == "genetics-techniques", \
            (f"{name} has category "
             f"{spec.category!r}, expected "
             f"'genetics-techniques'")


# ----------------------------------------------------------------
# list_genetics_techniques
# ----------------------------------------------------------------

def test_list_returns_full_catalogue_when_no_filter():
    from orgchem.agent.actions import invoke
    out = invoke("list_genetics_techniques")
    assert isinstance(out, list)
    assert len(out) >= 30
    assert all(isinstance(d, dict) for d in out)
    assert all("id" in d for d in out)


def test_list_filters_by_known_category():
    from orgchem.agent.actions import invoke
    crispr_only = invoke(
        "list_genetics_techniques", category="crispr")
    assert all(d["category"] == "crispr"
               for d in crispr_only)
    assert len(crispr_only) >= 5


def test_list_returns_error_for_unknown_category():
    from orgchem.agent.actions import invoke
    out = invoke(
        "list_genetics_techniques", category="bogus")
    assert isinstance(out, list)
    assert len(out) == 1
    assert "error" in out[0]
    assert "bogus" in out[0]["error"]


# ----------------------------------------------------------------
# get_genetics_technique
# ----------------------------------------------------------------

def test_get_returns_full_record_for_known_id():
    from orgchem.agent.actions import invoke
    out = invoke(
        "get_genetics_technique", technique_id="crispr-cas9")
    assert isinstance(out, dict)
    assert out["id"] == "crispr-cas9"
    assert out["category"] == "crispr"
    assert "principle" in out


def test_get_returns_error_for_unknown_id():
    from orgchem.agent.actions import invoke
    out = invoke(
        "get_genetics_technique",
        technique_id="does-not-exist")
    assert isinstance(out, dict)
    assert "error" in out


# ----------------------------------------------------------------
# find_genetics_techniques
# ----------------------------------------------------------------

def test_find_returns_substring_matches():
    from orgchem.agent.actions import invoke
    out = invoke(
        "find_genetics_techniques", needle="polymerase")
    assert isinstance(out, list)
    assert len(out) >= 2
    assert all("id" in d for d in out)


def test_find_returns_empty_for_no_match():
    from orgchem.agent.actions import invoke
    out = invoke(
        "find_genetics_techniques", needle="zzzzunlikely")
    assert out == []


def test_find_empty_needle_returns_empty():
    from orgchem.agent.actions import invoke
    out = invoke("find_genetics_techniques", needle="")
    assert out == []


# ----------------------------------------------------------------
# genetics_techniques_for_application
# ----------------------------------------------------------------

def test_application_filter_finds_single_cell():
    from orgchem.agent.actions import invoke
    out = invoke(
        "genetics_techniques_for_application",
        application="single-cell")
    assert any(d["id"] == "scrna-seq" for d in out)


# ----------------------------------------------------------------
# open_genetics_studio (no main window → error path)
# ----------------------------------------------------------------

def test_open_genetics_studio_returns_error_without_main_window():
    """Without a HeadlessApp / interactive main window
    initialised, ``open_genetics_studio`` must return a
    structured error rather than raising."""
    from orgchem.agent.actions import invoke
    from orgchem.agent import controller
    # Save + clear any existing main window for this test.
    saved = controller.main_window()
    controller.set_main_window(None)
    try:
        out = invoke("open_genetics_studio")
        assert isinstance(out, dict)
        assert "error" in out
    finally:
        controller.set_main_window(saved)
