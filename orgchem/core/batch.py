"""Batch-render helper — Phase 20e.

Takes a list of ``(name, smiles)`` pairs and produces, for each:

- ``<out>/2d/<safe_name>.png`` — RDKit 2D structure
- ``<out>/ir/<safe_name>.png`` — Phase 4 schematic IR spectrum
- ``<out>/descriptors.csv`` — MW / logP / TPSA / HBD / HBA / QED /
  Lipinski-violations rows (one per molecule)
- ``<out>/report.md`` — one-screen markdown summary with thumbnails
  and the descriptor table

Designed for instructors building handouts ("make a 20-molecule
PowerPoint slide") and for regression / corpus dumps (every molecule
in the DB → one directory). Pure Python, no external deps beyond what's
already in ``requirements.txt``.
"""
from __future__ import annotations
import csv
import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Tuple, Union

log = logging.getLogger(__name__)


# --------------------------------------------------------------------

@dataclass
class BatchResult:
    n_input: int
    n_rendered: int
    n_failed: int
    out_dir: Path
    descriptor_csv: Path
    report_md: Path
    failures: List[Tuple[str, str]]   # (name, error_message)


def _safe_name(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_\-.]+", "_", name).strip("._") or "mol"


def _parse_input(path: Path) -> List[Tuple[str, str]]:
    """Read a CSV or TXT input file; return [(name, smiles), ...].

    CSV expects a header line with ``name`` and ``smiles`` columns (any
    order). TXT accepts one ``smiles`` per line or ``smiles<TAB>name``
    / ``smiles<SPACE>name``. Empty lines and lines starting with ``#``
    are ignored.
    """
    entries: List[Tuple[str, str]] = []
    text = path.read_text()
    if path.suffix.lower() == ".csv":
        reader = csv.DictReader(text.splitlines())
        if reader.fieldnames is None:
            return entries
        cols = {c.lower().strip(): c for c in reader.fieldnames}
        smi_col = cols.get("smiles")
        name_col = cols.get("name") or cols.get("label")
        if smi_col is None:
            raise ValueError(f"{path}: CSV must have a 'smiles' column")
        for row in reader:
            smi = (row.get(smi_col) or "").strip()
            if not smi:
                continue
            nm = (row.get(name_col) if name_col else "") or smi
            entries.append((nm.strip(), smi))
    else:
        # TXT: one SMILES per line, optional whitespace-separated name.
        for raw in text.splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(None, 1)
            smi = parts[0]
            nm = parts[1] if len(parts) > 1 else smi
            entries.append((nm, smi))
    return entries


def _render_mol2d(smiles: str, path: Path) -> None:
    from rdkit import Chem
    from rdkit.Chem.Draw import rdMolDraw2D
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"unparseable SMILES: {smiles!r}")
    d = rdMolDraw2D.MolDraw2DCairo(500, 400)
    d.drawOptions().bondLineWidth = 2
    d.DrawMolecule(mol)
    d.FinishDrawing()
    path.write_bytes(d.GetDrawingText())


def _render_ir(smiles: str, path: Path, name: str) -> None:
    from orgchem.render.draw_ir import export_ir_spectrum
    export_ir_spectrum(smiles, path, title=f"IR — {name}")


def _descriptors(smiles: str) -> dict:
    from orgchem.core.druglike import drug_likeness_report
    rep = drug_likeness_report(smiles)
    return {
        "mw": rep["lipinski"]["mw"],
        "logp": rep["lipinski"]["logp"],
        "tpsa": rep["veber"]["tpsa"],
        "hbd": rep["lipinski"]["hbd"],
        "hba": rep["lipinski"]["hba"],
        "qed": rep["qed"],
        "lipinski_pass": int(rep["lipinski"]["passes"]),
        "veber_pass": int(rep["veber"]["passes"]),
    }


def batch_render(entries: Iterable[Tuple[str, str]],
                 out_dir: Union[str, Path],
                 render_2d: bool = True,
                 render_ir: bool = True,
                 write_report: bool = True) -> BatchResult:
    """Render a batch of SMILES to ``out_dir``. Returns a :class:`BatchResult`."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    if render_2d:
        (out / "2d").mkdir(exist_ok=True)
    if render_ir:
        (out / "ir").mkdir(exist_ok=True)

    csv_path = out / "descriptors.csv"
    report_path = out / "report.md"

    rows: List[dict] = []
    failures: List[Tuple[str, str]] = []
    entries = list(entries)

    for name, smi in entries:
        safe = _safe_name(name)
        row: dict = {"name": name, "smiles": smi}
        try:
            row.update(_descriptors(smi))
        except Exception as e:  # noqa: BLE001
            failures.append((name, f"descriptors: {e}"))
            log.warning("descriptor compute failed for %s: %s", name, e)
            # still include partial row
        if render_2d:
            try:
                _render_mol2d(smi, out / "2d" / f"{safe}.png")
            except Exception as e:  # noqa: BLE001
                failures.append((name, f"2d: {e}"))
                log.warning("2D render failed for %s: %s", name, e)
        if render_ir:
            try:
                _render_ir(smi, out / "ir" / f"{safe}.png", name)
            except Exception as e:  # noqa: BLE001
                failures.append((name, f"ir: {e}"))
                log.warning("IR render failed for %s: %s", name, e)
        rows.append(row)

    _write_csv(csv_path, rows)
    if write_report:
        _write_report(report_path, rows, failures,
                      have_2d=render_2d, have_ir=render_ir)

    return BatchResult(
        n_input=len(entries),
        n_rendered=len(rows) - sum(1 for f in failures if f[1].startswith("descriptors")),
        n_failed=len(failures),
        out_dir=out,
        descriptor_csv=csv_path,
        report_md=report_path,
        failures=failures,
    )


def batch_render_from_file(input_path: Union[str, Path],
                           out_dir: Union[str, Path],
                           **kwargs) -> BatchResult:
    """Shortcut: parse input file then render."""
    return batch_render(_parse_input(Path(input_path)), out_dir, **kwargs)


# --------------------------------------------------------------------
# Writers

_CSV_COLS = [
    "name", "smiles",
    "mw", "logp", "tpsa",
    "hbd", "hba", "qed",
    "lipinski_pass", "veber_pass",
]


def _write_csv(path: Path, rows: List[dict]) -> None:
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=_CSV_COLS, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def _write_report(path: Path, rows: List[dict],
                  failures: List[Tuple[str, str]],
                  have_2d: bool, have_ir: bool) -> None:
    lines: List[str] = []
    lines.append(f"# Batch render report — {len(rows)} molecule(s)")
    lines.append("")
    lines.append("| Name | SMILES | MW | logP | TPSA | QED | Lipinski |")
    lines.append("|------|--------|----|------|------|-----|----------|")
    for r in rows:
        lines.append(
            f"| {r['name']} | `{r['smiles']}` | "
            f"{r.get('mw', '—'):.1f} | {r.get('logp', '—'):.2f} | "
            f"{r.get('tpsa', '—'):.1f} | {r.get('qed', '—'):.2f} | "
            f"{'✓' if r.get('lipinski_pass') else '✗'} |"
            if isinstance(r.get('mw'), (int, float)) else
            f"| {r['name']} | `{r['smiles']}` | — | — | — | — | — |"
        )
    if have_2d or have_ir:
        lines.append("")
        lines.append("## Thumbnails")
        for r in rows:
            safe = _safe_name(r["name"])
            lines.append(f"### {r['name']}")
            if have_2d:
                lines.append(f"![2D](2d/{safe}.png)")
            if have_ir:
                lines.append(f"![IR](ir/{safe}.png)")
            lines.append("")
    if failures:
        lines.append("## Failures")
        for nm, msg in failures:
            lines.append(f"- **{nm}** — {msg}")
    path.write_text("\n".join(lines))
