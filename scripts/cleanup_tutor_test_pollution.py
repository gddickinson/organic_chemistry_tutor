"""One-shot purge of the Tutor-test-* rows left in a user's local
DB by prior runs of the content-authoring action tests.

Usage::

    python scripts/cleanup_tutor_test_pollution.py

Safe: targets only names starting with the literal
``Tutor-test-`` prefix every authoring test uses.  Idempotent —
running twice is a no-op.

See :mod:`orgchem.db.cleanup` for the module-level function that
this script wraps.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Let the script be invoked as `python scripts/cleanup_tutor_test_pollution.py`
# from either the repo root or anywhere else — prepend the repo root
# so the `orgchem` package is importable without PYTHONPATH.
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


def main() -> int:
    # Import inside main() so --help runs without the heavy deps.
    from orgchem.agent.headless import HeadlessApp
    from orgchem.db.cleanup import purge_tutor_test_pollution

    print("Inventorying + purging Tutor-test-* rows…")
    with HeadlessApp():
        counts = purge_tutor_test_pollution()
    print(counts)
    print(f"Purged {counts.total()} row(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
