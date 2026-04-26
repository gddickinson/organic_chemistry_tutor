"""Phase 49d (round 179) — agent-surface symmetry audit.

Locks in that **every catalogue with a Tools-menu dialog has a
symmetric agent-action surface**: an opener + the canonical lookup
trio (list / get / find).  Round-179 baseline: 24 catalogues
audited; 9 dialog openers deliberately deferred (allow-listed in
:data:`KNOWN_GAPS` with rationale).

Catches three classes of regression:
1. A catalogue gains a dialog but no `open_*` action.
2. A catalogue's lookup actions get renamed and the audit spec
   doesn't catch up.
3. An allow-listed `open_*` ships but the allow-list isn't
   pruned.
"""
from __future__ import annotations
import pytest

pytest.importorskip("rdkit")


# ==================================================================
# Spec sanity
# ==================================================================

def test_expected_surfaces_non_empty_and_unique():
    """The expected-surfaces table covers ≥ 20 catalogues with no
    duplicate openers."""
    from orgchem.core.agent_surface_audit import EXPECTED_SURFACES
    assert len(EXPECTED_SURFACES) >= 20
    openers = [s.opener for s in EXPECTED_SURFACES]
    assert len(openers) == len(set(openers)), \
        "duplicate opener entries in EXPECTED_SURFACES"


def test_known_gaps_well_formed():
    """Each KNOWN_GAPS entry is `(action_name, rationale)` with a
    non-empty rationale (so future readers know WHY it's deferred)."""
    from orgchem.core.agent_surface_audit import KNOWN_GAPS
    for name, rationale in KNOWN_GAPS:
        assert name.startswith("open_"), f"weird gap entry: {name}"
        assert rationale.strip(), \
            f"KNOWN_GAPS entry {name!r} has empty rationale"


# ==================================================================
# Audit
# ==================================================================

def test_every_expected_surface_complete():
    """Every catalogue listed in EXPECTED_SURFACES has the
    required agent-action surface registered.  Failure surfaces
    the per-catalogue gap + a copy of the audit table."""
    from orgchem.core.agent_surface_audit import (
        audit_all_surfaces, render_audit_text,
    )
    reports = audit_all_surfaces()
    incomplete = [r for r in reports if not r.is_complete()]
    assert not incomplete, (
        f"{len(incomplete)} catalogue(s) have missing agent "
        f"actions:\n"
        + "\n".join(
            f"  [{r.spec.catalogue}] missing: "
            f"{', '.join(r.missing_actions)}"
            for r in incomplete)
        + "\n\nFull audit:\n"
        + render_audit_text(reports)
    )


def test_known_gaps_allowlist_is_honest():
    """If a previously-deferred `open_*` action has shipped, the
    KNOWN_GAPS allow-list entry must be deleted (and a matching
    EXPECTED_SURFACES entry added).  Catches stale allow-list
    drift."""
    from orgchem.core.agent_surface_audit import stale_known_gaps
    stale = stale_known_gaps()
    assert not stale, (
        f"KNOWN_GAPS lists {len(stale)} action(s) that DO exist "
        f"in the registry now: {stale}.  Promote them to "
        f"EXPECTED_SURFACES."
    )


def test_audit_text_renders():
    """Smoke-test the human-readable audit renderer used by
    failure messages + the Phase-49d doc."""
    from orgchem.core.agent_surface_audit import render_audit_text
    out = render_audit_text()
    assert "Catalogue" in out
    assert "ok" in out or "MISSING" in out
    assert "KNOWN_GAPS" in out


# ==================================================================
# Spot-check: round-179 newly-added openers wired correctly
# ==================================================================

def test_round_179_openers_registered():
    """The two openers added in round 179 (`open_periodic_table` +
    `open_naming_rules`) are in the registry — guards against
    accidental removal."""
    from orgchem.core.agent_surface_audit import gather_action_names
    available = gather_action_names()
    assert "open_periodic_table" in available
    assert "open_naming_rules" in available


def test_round_179_openers_in_periodic_and_naming_categories():
    """The new openers are tagged with the right categories so
    they group with the rest of their catalogue's actions."""
    from orgchem.agent.actions import registry
    r = registry()
    assert r["open_periodic_table"].category == "periodic"
    assert r["open_naming_rules"].category == "naming"
