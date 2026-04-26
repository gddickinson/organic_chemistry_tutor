"""Phase 49e (round 180) — tutor-panel feature-discovery audit.

Locks in that **the AI tutor backend can discover every feature
the app ships**.  Three failure modes guarded:

1. Schema-coverage gap: action exists but isn't surfaced in
   `tool_schemas()` (the LLM literally can't call it).
2. Description gap: action ships with no docstring (the LLM
   sees an empty description in the tool schema).
3. Category-summary gap: a registered category is missing from
   `actions_meta._CATEGORY_SUMMARIES` (the tutor's
   `list_capabilities()` self-introspection returns an empty
   description for that category).

Round-180 baseline: 254 actions × 36 categories all clean.
"""
from __future__ import annotations
import pytest

pytest.importorskip("rdkit")


def test_audit_runs_clean():
    """The full feature-discovery audit reports no gaps.  Failure
    surfaces the broken entries + a summary block."""
    from orgchem.core.feature_discovery_audit import (
        audit_feature_discovery, render_report_text,
    )
    report = audit_feature_discovery()
    assert report.is_clean(), (
        "Feature-discovery audit found gaps:\n"
        + render_report_text(report)
    )


def test_registry_size_floor():
    """The registry has at least 200 actions — sanity floor that
    catches a global registry-loading regression."""
    from orgchem.core.feature_discovery_audit import (
        audit_feature_discovery,
    )
    report = audit_feature_discovery()
    assert report.total_actions >= 200, (
        f"only {report.total_actions} actions registered; "
        f"expected ≥ 200"
    )


def test_every_action_has_a_schema():
    """`tool_schemas()` returns one schema per registered action
    (no silent dropouts)."""
    from orgchem.agent.actions import registry, tool_schemas
    assert len(tool_schemas()) == len(registry())


def test_every_schema_has_required_keys():
    """Every tool schema has the Anthropic / OpenAI-required keys
    (`name`, `description`, `input_schema.type / properties /
    required`)."""
    from orgchem.agent.actions import tool_schemas
    for s in tool_schemas():
        assert "name" in s, f"schema {s} missing name"
        assert "description" in s
        ip = s.get("input_schema", {})
        assert ip.get("type") == "object", \
            f"{s.get('name')} input_schema.type != object"
        assert "properties" in ip
        assert "required" in ip


def test_categories_summary_covers_every_registered_category():
    """`actions_meta._CATEGORY_SUMMARIES` has a non-empty entry
    for every category present in the registry.  Caught 19
    missing categories on the round-180 baseline run; all
    backfilled in the same round."""
    from orgchem.agent.actions import registry
    from orgchem.agent.actions_meta import _CATEGORY_SUMMARIES
    cats = sorted({s.category for s in registry().values()})
    missing = [
        c for c in cats
        if not _CATEGORY_SUMMARIES.get(c, "").strip()
    ]
    assert not missing, (
        f"{len(missing)} categories missing from "
        f"_CATEGORY_SUMMARIES: {missing}"
    )


def test_no_stale_category_summaries():
    """`_CATEGORY_SUMMARIES` doesn't carry entries for categories
    that no longer exist in the registry — keeps the dict
    honest."""
    from orgchem.agent.actions import registry
    from orgchem.agent.actions_meta import _CATEGORY_SUMMARIES
    cats = {s.category for s in registry().values()}
    stale = sorted(
        c for c in _CATEGORY_SUMMARIES if c not in cats
    )
    assert not stale, (
        f"_CATEGORY_SUMMARIES contains stale entries: {stale}"
    )


def test_list_capabilities_smoke():
    """The tutor's `list_capabilities()` self-introspection
    action returns a non-empty inventory + every category has a
    non-empty description."""
    from orgchem.core.feature_discovery_audit import (
        list_capabilities_smoke,
    )
    inv = list_capabilities_smoke()
    assert inv["total_actions"] > 0
    assert inv["categories"], "no categories returned"
    for c in inv["categories"]:
        assert c["description"], (
            f"category {c['category']!r} has empty description"
        )


def test_round_180_specific_descriptions_present():
    """The 19 categories backfilled in round 180 have substantive
    descriptions (not placeholder strings)."""
    from orgchem.agent.actions_meta import _CATEGORY_SUMMARIES
    backfilled = (
        "authoring", "biochem", "calc", "cell", "centrifugation",
        "chromatography", "clinical", "drawing", "instrumentation",
        "isomer", "kingdom", "microscopy", "ph", "phys-org",
        "qualitative", "reagent", "scripting", "search",
        "spectrophotometry",
    )
    for cat in backfilled:
        desc = _CATEGORY_SUMMARIES.get(cat, "")
        assert len(desc) >= 30, (
            f"category {cat!r} description too short: {desc!r}"
        )


def test_round_180_centrifuge_docstrings_filled():
    """The two empty-docstring actions caught in round 180
    (`get_centrifuge_action` / `get_rotor_action`) now have
    descriptions."""
    from orgchem.agent.actions import registry
    r = registry()
    assert r["get_centrifuge_action"].description.strip()
    assert r["get_rotor_action"].description.strip()
