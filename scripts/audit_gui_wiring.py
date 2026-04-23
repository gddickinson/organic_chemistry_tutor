"""Phase 25a — CLI wrapper around ``orgchem.gui.audit``.

Usage:
    python scripts/audit_gui_wiring.py

Prints a table of every registered agent action alongside its user-
facing entry point (or "— missing" when no GUI route exists) plus a
coverage summary. Exits with code 0 even when gaps exist — the
point of the audit is visibility, not gating CI.
"""
from __future__ import annotations
import sys

# Ensure we import the in-tree package when run from the repo root.
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import orgchem.agent  # noqa: F401 — side-effect: register all actions
from orgchem.gui.audit import audit, audit_summary


def main() -> int:
    rows = audit()
    summary = audit_summary()
    print("=" * 84)
    print(f"OrgChem Studio — GUI wiring audit")
    print(f"  Actions total : {summary['total_actions']}")
    print(f"  Wired         : {summary['wired']}")
    print(f"  Missing       : {summary['missing']}")
    print(f"  Coverage      : {summary['coverage_pct']} %")
    print("=" * 84)
    print(f"{'CATEGORY':<16}{'ACTION':<36} GUI ENTRY")
    print("-" * 84)
    for r in rows:
        entry = r.gui_entry if r.gui_entry else "— missing"
        print(f"{r.category:<16}{r.name:<36} {entry}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
