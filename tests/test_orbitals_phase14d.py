"""Tests for Phase 14d agent actions (round 49) —
``show_molecular_orbital`` + ``explain_wh`` + the pericyclic↔WH
lookup helper added as a Phase 14b follow-up."""
from __future__ import annotations
import pytest

pytest.importorskip("rdkit")


def test_show_molecular_orbital_homo_default():
    from orgchem.agent.actions import invoke
    # butadiene — 4 π e⁻ in 4 atoms, HOMO at index 1 (Ψ₂).
    res = invoke("show_molecular_orbital", smiles="C=CC=C")
    assert "error" not in res, res
    assert res["role"] == "HOMO"
    assert res["n_pi_atoms"] == 4
    assert res["n_pi_electrons"] == 4
    assert res["homo_index"] == 1
    assert res["lumo_index"] == 2
    assert res["energy_beta"] > 0    # bonding (k > 0 in α+kβ with β < 0)


def test_show_molecular_orbital_lumo_by_index():
    from orgchem.agent.actions import invoke
    # benzene — 6 π e⁻ in 6 atoms, HOMO at index 2 (degenerate with 1).
    res = invoke("show_molecular_orbital",
                 smiles="c1ccccc1", index=3)   # LUMO (degen)
    assert "error" not in res, res
    # LUMO energy is anti-bonding (k < 0) for benzene.
    assert res["role"] == "LUMO"
    assert res["energy_beta"] < 0


def test_show_molecular_orbital_out_of_range():
    from orgchem.agent.actions import invoke
    res = invoke("show_molecular_orbital", smiles="C=CC=C", index=99)
    assert "error" in res and "out of range" in res["error"]


def test_show_molecular_orbital_non_pi_system():
    from orgchem.agent.actions import invoke
    # Saturated alkane has no π system.
    res = invoke("show_molecular_orbital", smiles="CCCC")
    # Either the Hückel helper rejects it, or n_pi_atoms == 0.
    assert ("error" in res) or (res.get("n_pi_atoms", 0) == 0)


def test_explain_wh_diels_alder():
    from orgchem.agent.actions import invoke
    res = invoke("explain_wh",
                 reaction_name_or_id="Diels-Alder: butadiene + ethene")
    assert res.get("matched") is True, res
    assert res["rule_id"] == "cyclo-4plus2-thermal"
    assert res["rule"]["regime"] == "thermal"
    # Outcome should indicate allowed
    assert "allowed" in res["rule"]["outcome"].lower()


def test_explain_wh_ionic_reaction_no_match():
    from orgchem.agent.actions import invoke
    res = invoke("explain_wh",
                 reaction_name_or_id="SN2: methyl bromide + hydroxide")
    # SN2 is not pericyclic — should cleanly report "no match" with a note.
    assert res.get("matched") is False
    assert "No pericyclic" in res.get("note", "")


def test_explain_wh_unknown_name():
    from orgchem.agent.actions import invoke
    res = invoke("explain_wh",
                 reaction_name_or_id="reaction-that-does-not-exist")
    # Not a DB row and no substring match — still returns matched=False
    # with a note rather than erroring.
    assert res.get("matched") is False
    assert "note" in res


def test_gui_audit_entries_exist():
    from orgchem.gui.audit import GUI_ENTRY_POINTS
    for name in ("show_molecular_orbital", "explain_wh"):
        entry = GUI_ENTRY_POINTS.get(name, "")
        assert "Orbitals" in entry, (name, entry)


def test_gui_coverage_still_100():
    from orgchem.gui.audit import audit_summary
    s = audit_summary()
    assert s["coverage_pct"] == 100.0
