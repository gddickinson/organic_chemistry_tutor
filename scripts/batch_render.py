"""CLI wrapper around :func:`orgchem.core.batch.batch_render_from_file`.

Usage:

    python scripts/batch_render.py INPUT [OUTDIR]

where ``INPUT`` is a ``.csv`` with ``name,smiles`` columns, or a
``.txt`` with one SMILES per line (optionally followed by whitespace
then a name). Outputs (2D PNG, IR PNG, descriptors.csv, report.md)
land in ``OUTDIR`` (default ``./batch_out``).
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Batch-render a list of SMILES.")
    p.add_argument("input", help="CSV or TXT of molecules (see docstring).")
    p.add_argument("outdir", nargs="?", default="./batch_out",
                   help="Output directory (default: ./batch_out).")
    p.add_argument("--no-2d", action="store_true",
                   help="Skip 2D PNG rendering.")
    p.add_argument("--no-ir", action="store_true",
                   help="Skip IR spectrum rendering.")
    p.add_argument("--no-report", action="store_true",
                   help="Skip writing report.md.")
    args = p.parse_args(argv)

    # Ensure project root is importable when running as a script from anywhere.
    ROOT = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(ROOT))

    from orgchem.core.batch import batch_render_from_file

    result = batch_render_from_file(
        args.input, args.outdir,
        render_2d=not args.no_2d,
        render_ir=not args.no_ir,
        write_report=not args.no_report,
    )

    print(f"Rendered {result.n_rendered}/{result.n_input} molecules → "
          f"{result.out_dir}")
    print(f"  descriptors CSV: {result.descriptor_csv}")
    if not args.no_report:
        print(f"  report markdown: {result.report_md}")
    if result.failures:
        print(f"  {len(result.failures)} failure(s):")
        for name, msg in result.failures[:10]:
            print(f"    - {name}: {msg}")
        if len(result.failures) > 10:
            print(f"    … and {len(result.failures) - 10} more")
    return 0 if not result.failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
