"""Phase 26b — regenerate glossary example figures.

Usage:
    python scripts/regen_glossary_figures.py            # incremental PNG
    python scripts/regen_glossary_figures.py --force    # overwrite
    python scripts/regen_glossary_figures.py --svg      # SVG output

Walks every glossary entry that carries an ``example_smiles`` field
and writes a PNG (or SVG) into ``data/glossary/``. Safe to run any
number of times — incremental by default.
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from orgchem.core.glossary_figures import (
    regenerate_all, default_figure_dir,
)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--force", action="store_true",
                   help="Overwrite existing figures")
    p.add_argument("--svg", action="store_true",
                   help="Output SVG instead of PNG")
    p.add_argument("--out-dir", default=None,
                   help="Override output directory (default: data/glossary/)")
    args = p.parse_args()

    fmt = "svg" if args.svg else "png"
    out_dir = Path(args.out_dir) if args.out_dir else default_figure_dir()
    print(f"Rendering to {out_dir} (format={fmt}, force={args.force})")

    results = regenerate_all(out_dir=out_dir, force=args.force, fmt=fmt)
    for r in results:
        tag = "✓" if r.rendered else "—"
        note = "" if r.rendered else f"  ({r.skipped_reason})"
        print(f"  {tag} {r.term:<30} → {r.path.name}{note}")

    rendered = sum(1 for r in results if r.rendered)
    print(f"\n{rendered} / {len(results)} figures rendered.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
