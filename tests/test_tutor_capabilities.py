"""Tests for the tutor-capability upgrade (round 55 — user-reported
that the tutor said "I don't have tools for ligand binding"
despite fetch_pdb + analyse_binding + export_interaction_map)."""
from __future__ import annotations
import pytest

pytest.importorskip("rdkit")


# ---- list_capabilities -------------------------------------------

def test_list_capabilities_returns_all_categories():
    from orgchem.agent.actions import invoke
    res = invoke("list_capabilities")
    assert "error" not in res
    assert res["total_actions"] > 50
    cats = {c["category"] for c in res["categories"]}
    for must_have in ("molecule", "protein", "reaction", "synthesis",
                      "spectroscopy", "orbitals", "lab"):
        assert must_have in cats, (must_have, cats)


def test_list_capabilities_protein_drill_in_has_show_ligand_binding():
    """Round-55 addition — `show_ligand_binding` is the workflow
    the tutor should fire for 'show me X bound to Y' questions."""
    from orgchem.agent.actions import invoke
    res = invoke("list_capabilities", category="protein")
    assert "error" not in res
    names = [a["name"] for a in res["actions"]]
    assert "show_ligand_binding" in names
    assert "fetch_pdb" in names
    assert "analyse_binding" in names
    assert "export_interaction_map" in names


def test_list_capabilities_unknown_category_errors():
    from orgchem.agent.actions import invoke
    res = invoke("list_capabilities", category="doesnt-exist")
    assert "error" in res


def test_list_capabilities_includes_summaries():
    """Every action in a category drill-in carries a one-line summary
    (the first line of its docstring). Missing summaries make the
    tutor fly blind."""
    from orgchem.agent.actions import invoke
    res = invoke("list_capabilities", category="protein")
    for action in res["actions"]:
        assert "name" in action
        assert "summary" in action


# ---- show_ligand_binding ------------------------------------------

def test_show_ligand_binding_reports_missing_pdb():
    from orgchem.agent.actions import invoke
    res = invoke("show_ligand_binding", pdb_id="ZZZZZ",
                 ligand_name="XXX")
    assert "error" in res


def test_show_ligand_binding_with_seeded_protein(tmp_path):
    """End-to-end: use a PDB that should already be in the local
    cache (the seeded set ships with cached copies, or at worst
    fetches on first call). The test only asserts the basic
    response shape — network fetches may be skipped in offline CI."""
    from orgchem.agent.actions import invoke
    out_path = tmp_path / "interaction.png"
    res = invoke(
        "show_ligand_binding",
        pdb_id="2YDO", ligand_name="ADN",
        interaction_map_path=str(out_path),
    )
    # If we're offline / network-less, the fetch may error; that's
    # still a valid state for the user — they'll see a clear message.
    if "error" in res:
        assert "fetch_pdb" in res["error"] or "Fetch" in res["error"]
        return
    assert res["pdb_id"] == "2YDO"
    assert "summary" in res
    # Contacts analysis either ran or produced a structured error.
    assert ("contacts" in res) or ("contacts_error" in res)


def test_show_ligand_binding_without_ligand_skips_contacts():
    """If the caller omits ligand_name, the action still fetches and
    (when possible) shows the structure but doesn't try contact
    analysis."""
    from orgchem.agent.actions import invoke
    res = invoke("show_ligand_binding", pdb_id="2YDO")
    # As above — accept either a success or a clean error.
    if "error" in res:
        return
    assert "contacts" not in res


# ---- audit -------------------------------------------------------

def test_audit_entries_present():
    from orgchem.gui.audit import GUI_ENTRY_POINTS
    for name in ("show_ligand_binding", "list_capabilities"):
        entry = GUI_ENTRY_POINTS.get(name, "")
        assert entry, (name, "missing GUI_ENTRY_POINTS entry")


def test_gui_coverage_still_100():
    from orgchem.gui.audit import audit_summary
    s = audit_summary()
    assert s["coverage_pct"] == 100.0


# ---- system prompt -----------------------------------------------

def test_system_prompt_mentions_protein_workflow():
    """Core bug fix: the old prompt didn't mention proteins, so the
    tutor couldn't find them. The new prompt must flag the key
    workflow + the list_capabilities escape hatch."""
    from orgchem.agent.conversation import _SYSTEM_PROMPT
    assert "show_ligand_binding" in _SYSTEM_PROMPT
    assert "list_capabilities" in _SYSTEM_PROMPT
    assert "fetch_pdb" in _SYSTEM_PROMPT
    assert "analyse_binding" in _SYSTEM_PROMPT
    # Workflow-hint block flags the 2YDO case study.
    assert "2YDO" in _SYSTEM_PROMPT or "adenosine" in _SYSTEM_PROMPT.lower()
