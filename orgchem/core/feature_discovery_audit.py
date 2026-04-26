"""Phase 49e (round 180) — tutor-panel feature-discovery audit.

Test-time helper that walks the agent action registry + the
LLM-facing tool-schema generator + the `list_capabilities` meta
action and verifies the AI tutor backend can actually **discover
every feature** the app ships.

Three failure modes audited:

1. **Schema-coverage gap.**  An action exists in the registry
   but `tool_schemas()` doesn't surface it (or surfaces it with
   missing required fields).  The LLM literally can't call it.
2. **Description gap.**  An action ships with no docstring.  The
   LLM-facing description ends up empty, so the model has to
   guess from the function name what the tool does.  Catches the
   `def foo(a, b): pass` regression.
3. **Category-summary gap.**  An action's category isn't listed
   in `actions_meta._CATEGORY_SUMMARIES`.  The tutor's
   `list_capabilities()` self-introspection then returns an empty
   description for that category, hiding the feature area from
   the LLM's discovery loop.  Caught 19 categories on the round-
   180 baseline run, all backfilled in the same round.

Pure-headless: imports the agent registry only.  No Qt imports.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Set


@dataclass
class FeatureDiscoveryReport:
    """Result of a single feature-discovery audit run."""
    total_actions: int = 0
    total_categories: int = 0
    total_schemas: int = 0
    actions_missing_description: List[str] = field(default_factory=list)
    actions_missing_from_schemas: List[str] = field(default_factory=list)
    schemas_missing_required_keys: List[str] = field(default_factory=list)
    categories_missing_summary: List[str] = field(default_factory=list)

    def is_clean(self) -> bool:
        return not (
            self.actions_missing_description
            or self.actions_missing_from_schemas
            or self.schemas_missing_required_keys
            or self.categories_missing_summary
        )


REQUIRED_SCHEMA_KEYS = ("name", "description", "input_schema")
REQUIRED_INPUT_SCHEMA_KEYS = ("type", "properties", "required")


def audit_feature_discovery() -> FeatureDiscoveryReport:
    """Run the full feature-discovery audit and return a single
    aggregated report."""
    from orgchem.agent.actions import registry, tool_schemas
    from orgchem.agent.actions_meta import _CATEGORY_SUMMARIES

    reg = registry()
    schemas = tool_schemas()
    summary_keys = set(_CATEGORY_SUMMARIES.keys())

    report = FeatureDiscoveryReport(
        total_actions=len(reg),
        total_schemas=len(schemas),
    )

    # Description audit — every action has a non-empty
    # docstring-derived description.
    for name, spec in reg.items():
        if not (spec.description or "").strip():
            report.actions_missing_description.append(name)

    # Schema-coverage audit — every registered action shows up
    # in the schemas list with the required top-level keys.
    schema_names = {s.get("name") for s in schemas}
    for name in reg:
        if name not in schema_names:
            report.actions_missing_from_schemas.append(name)

    for s in schemas:
        for key in REQUIRED_SCHEMA_KEYS:
            if key not in s:
                report.schemas_missing_required_keys.append(
                    f"{s.get('name', '?')}: missing top-level "
                    f"key {key!r}")
        ip = s.get("input_schema", {})
        for key in REQUIRED_INPUT_SCHEMA_KEYS:
            if key not in ip:
                report.schemas_missing_required_keys.append(
                    f"{s.get('name', '?')}: missing "
                    f"input_schema.{key!r}")

    # Category-summary audit — every category surfaced via the
    # registry has a non-empty entry in `_CATEGORY_SUMMARIES` so
    # `list_capabilities()` returns useful descriptions.
    cats_in_registry: Set[str] = {
        getattr(s, "category", "") or "(uncategorised)"
        for s in reg.values()
    }
    for cat in sorted(cats_in_registry):
        if cat not in summary_keys:
            report.categories_missing_summary.append(cat)
        elif not _CATEGORY_SUMMARIES.get(cat, "").strip():
            report.categories_missing_summary.append(cat)
    report.total_categories = len(cats_in_registry)
    return report


def list_capabilities_smoke() -> Dict[str, Any]:
    """Run the `list_capabilities()` meta-action without any
    arguments and return the result.  Useful as a smoke check
    that the tutor's self-introspection entry point still
    works."""
    from orgchem.agent.actions_meta import list_capabilities
    return list_capabilities()


def render_report_text(report: FeatureDiscoveryReport) -> str:
    """Render a feature-discovery report as a human-readable
    block.  Used by the failure messages + the Phase-49e doc."""
    rows = []
    rows.append("Feature-discovery audit")
    rows.append("=" * 60)
    rows.append(f"Registered actions: {report.total_actions}")
    rows.append(f"Tool schemas:       {report.total_schemas}")
    rows.append(f"Categories:         {report.total_categories}")
    rows.append("")
    rows.append(f"Actions missing description: "
                f"{len(report.actions_missing_description)}")
    if report.actions_missing_description:
        for n in report.actions_missing_description[:10]:
            rows.append(f"  - {n}")
    rows.append(f"Actions missing from tool_schemas: "
                f"{len(report.actions_missing_from_schemas)}")
    if report.actions_missing_from_schemas:
        for n in report.actions_missing_from_schemas[:10]:
            rows.append(f"  - {n}")
    rows.append(f"Schemas missing required keys: "
                f"{len(report.schemas_missing_required_keys)}")
    if report.schemas_missing_required_keys:
        for s in report.schemas_missing_required_keys[:10]:
            rows.append(f"  - {s}")
    rows.append(f"Categories missing summary: "
                f"{len(report.categories_missing_summary)}")
    if report.categories_missing_summary:
        for c in report.categories_missing_summary[:10]:
            rows.append(f"  - {c}")
    rows.append("=" * 60)
    rows.append(
        "STATUS: " + ("CLEAN" if report.is_clean() else "GAPS")
    )
    return "\n".join(rows)
