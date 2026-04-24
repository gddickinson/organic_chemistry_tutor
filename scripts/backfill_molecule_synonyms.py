"""Phase 35c (round 120) — one-shot CLI that backfills
``Molecule.synonyms_json`` from PubChem by InChIKey.

Usage::

    python scripts/backfill_molecule_synonyms.py
    python scripts/backfill_molecule_synonyms.py --limit 20
    python scripts/backfill_molecule_synonyms.py --rate-delay 0.5

Safe: rate-limited (default 200 ms/request stays under PubChem's
5 req/sec ceiling), pollution-safe (skips ``Tutor-test…`` rows),
idempotent (only hits rows with an empty synonym list).  See
``orgchem.db.backfill_synonyms`` for the core function this
script wraps.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Let the script run as `python scripts/backfill_molecule_synonyms.py`
# from the repo root without requiring PYTHONPATH to be set — prepend
# the repo root to sys.path.
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Bulk-backfill PubChem synonyms onto every "
                    "Molecule row with an empty synonyms_json.")
    parser.add_argument(
        "--limit", type=int, default=None,
        help="Max number of network requests to make in one run "
             "(default: no limit; a full ~415-row walk takes ~85 s "
             "at 200 ms/request).")
    parser.add_argument(
        "--rate-delay", type=float, default=0.2,
        help="Seconds to sleep between PubChem requests (default "
             "0.2 — stays under the free-tier 5 req/sec ceiling).")
    parser.add_argument(
        "--min-existing", type=int, default=1,
        help="Skip rows whose synonyms_json already holds at least "
             "this many entries (default 1 — top-up only empty "
             "rows; pass 0 to refresh every row).")
    args = parser.parse_args()

    # Heavy imports deferred until after --help flag would fire.
    from orgchem.agent.headless import HeadlessApp
    from orgchem.db.backfill_synonyms import backfill_synonyms

    print("Phase 35c — bulk PubChem synonym backfill")
    if args.limit is not None:
        print(f"  limit:         {args.limit} requests")
    print(f"  rate_delay_s:  {args.rate_delay}")
    print(f"  min_existing:  {args.min_existing}")
    print()

    with HeadlessApp():
        counts = backfill_synonyms(
            limit=args.limit,
            rate_delay_s=args.rate_delay,
            min_existing=args.min_existing,
        )
    print(counts)
    print(f"Done — added {counts.added_total} synonym string(s) "
          f"to {counts.fetched} molecule(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
