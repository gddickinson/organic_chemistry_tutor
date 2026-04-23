"""Optional PLIP integration — Phase 24i.

`PLIP <https://plip-tool.biotec.tu-dresden.de/>`_ is the gold-standard
open-source protein-ligand interaction profiler. It detects:

* hydrogen bonds (with angle filter)
* salt bridges / electrostatic interactions
* π-stacking (parallel + T-shaped)
* π-cation
* hydrophobic contacts
* halogen bonds
* water-mediated bridges
* metal coordination

...each with the correct directional / angular filters that our pure-
geometric :mod:`orgchem.core.binding_contacts` module intentionally
skips for simplicity.

This module is a **thin adapter**: it detects whether PLIP is
available (either as an importable library or as the ``plip`` / ``plipcmd``
CLI) and — if so — runs it on a cached PDB and converts its output
into our own :class:`~orgchem.core.binding_contacts.ContactReport`
schema so downstream renderers (Phase 24c interaction map) work
interchangeably.

When PLIP isn't installed the helper returns the built-in
``analyse_binding`` result and flags ``engine="builtin"`` on the
report so callers can display a "install plip for deeper analysis"
banner.

We keep no persistent PLIP dependency — tests monkeypatch the
availability probe and CLI runner so they exercise the adapter
without PLIP installed.
"""
from __future__ import annotations
import logging
import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional
from xml.etree import ElementTree as ET

from orgchem.core.binding_contacts import (
    Contact,
    ContactReport,
    analyse_binding as _builtin_analyse,
)
from orgchem.core.protein import Protein

log = logging.getLogger(__name__)


# ---------------------------------------------------------------------
# Availability probe

_PLIP_CLI_CANDIDATES = ("plip", "plipcmd")


def plip_available() -> bool:
    """True if either the PLIP Python package or the CLI is installed."""
    try:
        import plip  # noqa: F401
        return True
    except ImportError:
        pass
    return any(shutil.which(c) for c in _PLIP_CLI_CANDIDATES)


def _find_plip_cli() -> Optional[str]:
    for c in _PLIP_CLI_CANDIDATES:
        p = shutil.which(c)
        if p:
            return p
    return None


# ---------------------------------------------------------------------
# Public API

@dataclass
class PLIPResult:
    """Wraps a :class:`ContactReport` plus an ``engine`` tag so callers
    know whether the data came from PLIP or the built-in fallback."""
    report: ContactReport
    engine: str              # "plip" / "builtin"
    plip_version: str = ""
    notes: str = ""

    def summary(self) -> Dict[str, Any]:
        out = self.report.summary()
        out["engine"] = self.engine
        if self.plip_version:
            out["plip_version"] = self.plip_version
        if self.notes:
            out["notes"] = self.notes
        return out


def analyse_binding_plip(protein: Protein, ligand_name: str,
                         pdb_path: Optional[Path] = None,
                         require_plip: bool = False) -> PLIPResult:
    """Analyse protein-ligand contacts via PLIP when available.

    - If PLIP is importable, use the Python API (preferred).
    - Else if the CLI is on PATH, invoke it on ``pdb_path`` (must be
      provided — PLIP CLI can't accept an in-memory :class:`Protein`).
    - Else fall back to the built-in geometric analyser
      (:func:`analyse_binding`), unless ``require_plip=True`` in which
      case return an empty :class:`PLIPResult` with
      ``engine="unavailable"``.
    """
    target = ligand_name.strip().upper()

    # 1) Try the Python API path.
    try:
        from plip.structure.preparation import PDBComplex  # type: ignore
        return _run_plip_python_api(protein, target, pdb_path)
    except ImportError:
        pass
    except Exception as e:  # noqa: BLE001
        log.warning("PLIP Python API failed: %s — trying CLI", e)

    # 2) CLI path.
    cli = _find_plip_cli()
    if cli and pdb_path is not None:
        try:
            return _run_plip_cli(cli, pdb_path, target)
        except Exception as e:  # noqa: BLE001
            log.warning("PLIP CLI failed: %s — falling back to builtin", e)

    # 3) Fallback.
    if require_plip:
        report = ContactReport(pdb_id=protein.pdb_id, ligand_name=target)
        return PLIPResult(report=report, engine="unavailable",
                          notes="PLIP is not installed "
                                "(install via 'pip install plip').")
    report = _builtin_analyse(protein, target)
    return PLIPResult(report=report, engine="builtin",
                      notes="PLIP not installed; used built-in "
                            "geometric analyser.")


# ---------------------------------------------------------------------
# Internals — Python API

def _run_plip_python_api(protein: Protein, ligand_name: str,
                         pdb_path: Optional[Path]) -> PLIPResult:
    """Use PLIP's :class:`PDBComplex` to analyse the structure.

    Requires the PDB source text (not just our parsed :class:`Protein`)
    because PLIP re-parses with OpenBabel for protonation-aware
    chemistry. If ``pdb_path`` isn't given, we spill the parsed
    structure back out to a temp file using the raw lines preserved
    via :mod:`orgchem.sources.pdb`.
    """
    from plip.structure.preparation import PDBComplex  # type: ignore

    # Re-fetch the raw text if the caller didn't give us a file path.
    if pdb_path is None:
        from orgchem.sources.pdb import cached_pdb_path
        pdb_path = cached_pdb_path(protein.pdb_id)
        if not pdb_path.exists():
            raise FileNotFoundError(
                f"Cannot locate cached PDB for {protein.pdb_id!r}; "
                "pass pdb_path=... or fetch_pdb first.")

    cplx = PDBComplex()
    cplx.load_pdb(str(pdb_path))
    cplx.analyze()

    contacts: List[Contact] = []
    plip_version = _extract_plip_version()

    for site_name, site in cplx.interaction_sets.items():
        # PLIP names binding sites like "IBP:A:1000" — accept if
        # the hetid matches our ligand.
        hetid = getattr(site, "hetid", "")
        if hetid.upper() != ligand_name:
            continue
        contacts.extend(_convert_plip_hbonds(site))
        contacts.extend(_convert_plip_saltbridges(site))
        contacts.extend(_convert_plip_pistacking(site))
        contacts.extend(_convert_plip_hydrophobic(site))

    report = ContactReport(pdb_id=protein.pdb_id,
                           ligand_name=ligand_name, contacts=contacts)
    return PLIPResult(report=report, engine="plip",
                      plip_version=plip_version)


def _extract_plip_version() -> str:
    try:
        from plip import __version__  # type: ignore
        return str(__version__)
    except Exception:  # noqa: BLE001
        return ""


def _convert_plip_hbonds(site) -> List[Contact]:
    out: List[Contact] = []
    for hb in getattr(site, "hbonds_ldon", []) + \
              getattr(site, "hbonds_pdon", []):
        out.append(Contact(
            kind="h-bond",
            ligand_atom=_plip_atom_name(getattr(hb, "a", None)
                                        or getattr(hb, "d", None)),
            protein_chain=getattr(hb, "reschain", ""),
            protein_residue=f"{getattr(hb, 'restype', '?')}"
                            f"{getattr(hb, 'resnr', '')}",
            distance=float(getattr(hb, "distance_ah",
                                   getattr(hb, "distance_ad", 0.0))),
        ))
    return out


def _convert_plip_saltbridges(site) -> List[Contact]:
    out: List[Contact] = []
    for sb in getattr(site, "saltbridge_lneg", []) + \
              getattr(site, "saltbridge_pneg", []):
        out.append(Contact(
            kind="salt-bridge",
            ligand_atom="",
            protein_chain=getattr(sb, "reschain", ""),
            protein_residue=f"{getattr(sb, 'restype', '?')}"
                            f"{getattr(sb, 'resnr', '')}",
            distance=float(getattr(sb, "distance", 0.0)),
        ))
    return out


def _convert_plip_pistacking(site) -> List[Contact]:
    out: List[Contact] = []
    for ps in getattr(site, "pistacking", []):
        out.append(Contact(
            kind="pi-stacking",
            ligand_atom="",
            protein_chain=getattr(ps, "reschain", ""),
            protein_residue=f"{getattr(ps, 'restype', '?')}"
                            f"{getattr(ps, 'resnr', '')}",
            distance=float(getattr(ps, "distance", 0.0)),
        ))
    return out


def _convert_plip_hydrophobic(site) -> List[Contact]:
    out: List[Contact] = []
    for h in getattr(site, "hydrophobic_contacts", []):
        out.append(Contact(
            kind="hydrophobic",
            ligand_atom=_plip_atom_name(getattr(h, "ligatom", None)),
            protein_chain=getattr(h, "reschain", ""),
            protein_residue=f"{getattr(h, 'restype', '?')}"
                            f"{getattr(h, 'resnr', '')}",
            distance=float(getattr(h, "distance", 0.0)),
        ))
    return out


def _plip_atom_name(atom) -> str:
    if atom is None:
        return ""
    for attr in ("atomname", "name", "GetName"):
        val = getattr(atom, attr, None)
        if val is None:
            continue
        if callable(val):
            try:
                return str(val())
            except Exception:  # noqa: BLE001
                continue
        return str(val)
    return ""


# ---------------------------------------------------------------------
# Internals — CLI

def _run_plip_cli(cli: str, pdb_path: Path, ligand_name: str) -> PLIPResult:
    """Invoke ``plip -f in.pdb -x`` (XML output) and parse the result.

    PLIP CLI writes ``report.xml`` into the chosen output directory.
    """
    with tempfile.TemporaryDirectory(prefix="plip_") as tmp:
        proc = subprocess.run(
            [cli, "-f", str(pdb_path), "-o", tmp, "-x"],
            check=False, capture_output=True, text=True,
            timeout=120,
        )
        if proc.returncode != 0:
            raise RuntimeError(f"PLIP CLI failed: {proc.stderr or proc.stdout}")
        xml_path = Path(tmp) / "report.xml"
        if not xml_path.exists():
            # Some PLIP versions emit per-site files.
            xml_files = list(Path(tmp).glob("*.xml"))
            if not xml_files:
                raise RuntimeError("PLIP CLI produced no XML output")
            xml_path = xml_files[0]
        contacts = _parse_plip_xml(xml_path, ligand_name)

    pdb_id = pdb_path.stem.upper()
    report = ContactReport(pdb_id=pdb_id, ligand_name=ligand_name,
                           contacts=contacts)
    return PLIPResult(report=report, engine="plip-cli")


def _parse_plip_xml(xml_path: Path, ligand_name: str) -> List[Contact]:
    tree = ET.parse(xml_path)
    root = tree.getroot()
    contacts: List[Contact] = []
    for site in root.iter("bindingsite"):
        hetid = _xml_text(site, "identifiers/hetid")
        if hetid.upper() != ligand_name:
            continue
        for hb in site.iter("hydrogen_bond"):
            contacts.append(Contact(
                kind="h-bond",
                ligand_atom=_xml_text(hb, "ligcarbonidx") or "",
                protein_chain=_xml_text(hb, "reschain"),
                protein_residue=(_xml_text(hb, "restype") +
                                 _xml_text(hb, "resnr")),
                distance=_xml_float(hb, "dist_h-a") or
                         _xml_float(hb, "dist_d-a") or 0.0,
            ))
        for sb in site.iter("salt_bridge"):
            contacts.append(Contact(
                kind="salt-bridge", ligand_atom="",
                protein_chain=_xml_text(sb, "reschain"),
                protein_residue=(_xml_text(sb, "restype") +
                                 _xml_text(sb, "resnr")),
                distance=_xml_float(sb, "dist") or 0.0,
            ))
        for ps in site.iter("pi_stack"):
            contacts.append(Contact(
                kind="pi-stacking", ligand_atom="",
                protein_chain=_xml_text(ps, "reschain"),
                protein_residue=(_xml_text(ps, "restype") +
                                 _xml_text(ps, "resnr")),
                distance=_xml_float(ps, "centdist") or 0.0,
            ))
        for h in site.iter("hydrophobic_interaction"):
            contacts.append(Contact(
                kind="hydrophobic", ligand_atom="",
                protein_chain=_xml_text(h, "reschain"),
                protein_residue=(_xml_text(h, "restype") +
                                 _xml_text(h, "resnr")),
                distance=_xml_float(h, "dist") or 0.0,
            ))
    return contacts


def _xml_text(parent, path: str) -> str:
    el = parent.find(path)
    if el is None or el.text is None:
        return ""
    return el.text.strip()


def _xml_float(parent, path: str) -> Optional[float]:
    txt = _xml_text(parent, path)
    if not txt:
        return None
    try:
        return float(txt)
    except ValueError:
        return None


# ---------------------------------------------------------------------
# Convenience

def capabilities() -> Dict[str, Any]:
    """Describe the current PLIP environment (for diagnostics / UI)."""
    info: Dict[str, Any] = {"available": plip_available()}
    try:
        import plip  # noqa: F401
        info["python_api"] = True
        info["version"] = _extract_plip_version()
    except ImportError:
        info["python_api"] = False
    cli = _find_plip_cli()
    info["cli"] = cli or ""
    return info
