"""Tests for Phase 25a — GUI wiring audit."""
from __future__ import annotations
import pytest

pytest.importorskip("rdkit")


def test_audit_returns_rows_for_every_registered_action():
    from orgchem.gui.audit import audit
    import orgchem.agent  # noqa: F401 — registers all actions
    from orgchem.agent.actions import registry
    rows = audit()
    reg = registry()
    assert len(rows) == len(reg)
    # Every action name must round-trip through the audit.
    assert {r.name for r in rows} == set(reg.keys())


def test_audit_flags_missing_entries_via_empty_string():
    """An action without a GUI entry must appear as is_wired=False."""
    from orgchem.gui.audit import audit
    rows = audit()
    by_name = {r.name: r for r in rows}
    # list_sessions is explicitly wired (File → Recent sessions).
    assert by_name["list_sessions"].is_wired
    # As of round 38 every action is wired. Sanity-check two that
    # were closed late: reaction_atom_economy (Green metrics dialog)
    # and get_glossary_figure (Glossary tab → View figure button).
    assert by_name["drug_likeness"].is_wired
    assert by_name["reaction_atom_economy"].is_wired
    assert by_name["get_glossary_figure"].is_wired


def test_audit_summary_shape():
    from orgchem.gui.audit import audit_summary
    s = audit_summary()
    for key in ("total_actions", "wired", "missing",
                "coverage_pct", "missing_actions"):
        assert key in s
    assert s["total_actions"] == s["wired"] + s["missing"]
    assert 0.0 <= s["coverage_pct"] <= 100.0
    assert isinstance(s["missing_actions"], list)


def test_coverage_is_at_least_baseline():
    """Guard-rail: coverage must not regress. Round 38 pushed the
    baseline to 100 %; any future regression (new agent action
    without a GUI entry) trips this immediately."""
    from orgchem.gui.audit import audit_summary
    s = audit_summary()
    assert s["coverage_pct"] >= 100.0, (
        f"GUI coverage regressed — now at "
        f"{s['coverage_pct']}%. Wire up: "
        f"{[r['name'] for r in s['missing_actions'][:10]]}"
    )


def test_wired_entries_reference_real_ui_terms():
    """Every non-empty entry should describe a menu / tab / dialog
    path — sanity-check that they're not stub placeholders."""
    from orgchem.gui.audit import audit
    for row in audit():
        if not row.is_wired:
            continue
        entry = row.gui_entry.lower()
        # We accept any of these UI-path markers.
        markers = ("menu", "tab", "dialog", "dock", "→", "panel",
                   "viewer", "browser", "window", "ctrl+", "button",
                   "player", "search", "properties", "tutorials",
                   "glossary", "reactions", "synthesis", "molecule",
                   "compare", "proteins", "slot", "combo",
                   "file", "tools", "badge")
        assert any(m in entry for m in markers), \
            f"Suspicious GUI entry for {row.name!r}: {row.gui_entry!r}"
