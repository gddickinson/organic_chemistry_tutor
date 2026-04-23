"""Built-in actions — the LLM's toolbox for driving the app.

Importing this module is enough to register every action defined below.
"""
from __future__ import annotations
import json
import logging
from typing import Any, Dict, List, Optional

from orgchem.agent.actions import action
from orgchem.core.formula import compute_formula
from orgchem.core.molecule import Molecule as ChemMol
from orgchem.core.descriptors import compute_all
from orgchem.core.formats import mol_from_smiles
from orgchem.db.models import Molecule as DBMol
from orgchem.db.queries import list_molecules, get_molecule, find_molecule_by_name
from orgchem.db.session import session_scope
from orgchem.messaging.bus import bus

log = logging.getLogger(__name__)


def _row_to_dict(row: DBMol) -> Dict[str, Any]:
    return {
        "id": row.id, "name": row.name, "smiles": row.smiles,
        "formula": row.formula, "inchikey": row.inchikey,
        "source": row.source,
    }


# ---- Molecule database actions ----------------------------------------

@action(category="molecule")
def list_all_molecules(filter: str = "") -> List[Dict[str, Any]]:
    """List molecules in the database, optionally filtered by name/formula/SMILES substring."""
    rows = list_molecules(query=filter or None)
    return [_row_to_dict(r) for r in rows]


@action(category="molecule")
def list_molecule_categories() -> Dict[str, List[str]]:
    """Enumerate the Phase 28 filter axes + possible values — the
    taxonomy surfaced by the Molecule browser filter bar."""
    from orgchem.db.queries import list_molecule_category_values
    return list_molecule_category_values()


@action(category="molecule")
def filter_molecules(axis_a: str = "", value_a: str = "",
                     axis_b: str = "", value_b: str = "",
                     text_query: str = "",
                     limit: int = 200) -> List[Dict[str, Any]]:
    """Filter molecules by up to two tag axes + a free-text substring.

    Axes (from :func:`list_molecule_categories`):
    ``functional_group`` / ``composition`` / ``charge`` / ``size``
    / ``ring_count`` / ``has_stereo``. AND semantics across axes.
    Empty axis / value pairs are ignored so callers can omit the
    second axis for a single-filter query.
    """
    from orgchem.db.queries import query_by_tags
    rows = query_by_tags(
        axis_a=axis_a or None, value_a=value_a or None,
        axis_b=axis_b or None, value_b=value_b or None,
        text_query=text_query or None, limit=limit,
    )
    return [_row_to_dict(r) for r in rows]


@action(category="molecule")
def get_molecule_details(molecule_id: int) -> Dict[str, Any]:
    """Return full details (incl. computed descriptors) for a database molecule."""
    row = get_molecule(molecule_id)
    if row is None:
        return {"error": f"No molecule with id {molecule_id}"}
    d = _row_to_dict(row)
    try:
        d["descriptors"] = compute_all(mol_from_smiles(row.smiles))
    except Exception as e:
        d["descriptors_error"] = str(e)
    if row.properties_json:
        try:
            d["stored_properties"] = json.loads(row.properties_json)
        except Exception:
            pass
    return d


@action(category="molecule")
def show_molecule(name_or_id: str) -> Dict[str, Any]:
    """Display a molecule in the 2D and 3D viewers by DB id, name, or SMILES substring.

    The app's Molecule Workspace tab updates via the signal bus.
    """
    row: Optional[DBMol] = None
    if name_or_id.isdigit():
        row = get_molecule(int(name_or_id))
    if row is None:
        row = find_molecule_by_name(name_or_id)
    if row is None:
        rows = list_molecules(query=name_or_id, limit=1)
        row = rows[0] if rows else None
    if row is None:
        return {"error": f"No molecule matching {name_or_id!r}"}
    bus().molecule_selected.emit(int(row.id))
    log.info("Agent action show_molecule: %s (id=%d)", row.name, row.id)
    return _row_to_dict(row)


@action(category="molecule")
def import_smiles(name: str, smiles: str) -> Dict[str, Any]:
    """Add a new molecule (by SMILES + name) to the database and select it."""
    m = ChemMol.from_smiles(smiles, name=name)
    m.ensure_properties()
    with session_scope() as s:
        row = DBMol(
            name=m.name, smiles=m.smiles, inchi=m.inchi, inchikey=m.inchikey,
            formula=m.formula, molblock_3d=m.molblock_3d,
            properties_json=json.dumps(m.properties, default=str),
            source="agent-import",
        )
        s.add(row)
        s.flush()
        new_id = row.id
    bus().database_changed.emit()
    bus().molecule_selected.emit(int(new_id))
    return {"id": new_id, "name": m.name, "formula": m.formula}


# ---- Stoichiometry (Verma et al. Section A) ---------------------------

@action(category="tools")
def calculate_empirical_formula(percentages: dict, molar_mass: float,
                                use_integer_masses: bool = False) -> Dict[str, Any]:
    """Compute the empirical and molecular formula from element mass %s and molar mass.

    Uses IUPAC 2019 atomic masses by default (the more accurate choice, and
    what lab analysis produces). Set use_integer_masses=True to reproduce
    Verma et al. 2024 Table 1 exactly with their whole-number mass table.
    Example: percentages={"C": 74.0, "H": 8.7, "N": 17.27}, molar_mass=162.
    """
    from orgchem.core.formula import ATOMIC_MASSES_INTEGER
    masses = ATOMIC_MASSES_INTEGER if use_integer_masses else None
    res = compute_formula(percentages, molar_mass, masses=masses)
    return {
        "empirical_formula": res.empirical_formula,
        "molecular_formula": res.molecular_formula,
        "empirical_mass": res.empirical_mass,
        "scale_factor": res.scale_factor,
        "max_residual": res.max_residual,
        "worst_element": res.worst_element,
    }


# ---- Online sources ---------------------------------------------------

@action(category="online")
def search_pubchem(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Search PubChem by name; returns a list of candidates to pick from."""
    from orgchem.sources.pubchem import PubChemSource
    return PubChemSource().search(query, limit=limit)


@action(category="online")
def download_from_pubchem(cid: str) -> Dict[str, Any]:
    """Fetch a PubChem CID, store it in the local database, and select it in the viewers."""
    from orgchem.sources.pubchem import PubChemSource
    m = PubChemSource().fetch(cid)
    m.ensure_properties()
    with session_scope() as s:
        row = DBMol(
            name=m.name, smiles=m.smiles, inchi=m.inchi, inchikey=m.inchikey,
            formula=m.formula, molblock_3d=m.molblock_3d,
            properties_json=json.dumps(m.properties, default=str),
            source=m.source or "PubChem",
        )
        s.add(row)
        s.flush()
        new_id = row.id
    bus().database_changed.emit()
    bus().molecule_selected.emit(int(new_id))
    return {"id": new_id, "name": m.name, "formula": m.formula}


# ---- Tutorials --------------------------------------------------------

@action(category="tutorial")
def list_tutorials(level: str = "") -> List[Dict[str, Any]]:
    """List curriculum lessons; filter by level (beginner/intermediate/advanced/graduate)."""
    from orgchem.tutorial.curriculum import CURRICULUM
    out: List[Dict[str, Any]] = []
    for lvl, lessons in CURRICULUM.items():
        if level and lvl != level:
            continue
        for i, lesson in enumerate(lessons):
            out.append({"level": lvl, "index": i, "title": lesson["title"]})
    return out


@action(category="tutorial")
def open_tutorial(level: str, index: int) -> Dict[str, Any]:
    """Open a curriculum lesson in the Tutorials tab by level + index."""
    from orgchem.tutorial.curriculum import CURRICULUM
    from orgchem.tutorial.loader import load_tutorial_markdown
    lessons = CURRICULUM.get(level, [])
    if not (0 <= index < len(lessons)):
        return {"error": f"No lesson at {level}[{index}]"}
    lesson = lessons[index]
    bus().tutorial_step_changed.emit(f"{level}/{index}", 0)
    return {
        "title": lesson["title"],
        "markdown": load_tutorial_markdown(lesson["path"]),
    }


# ---- Image export & screenshots --------------------------------------

# Friendly alias → MainWindow attribute name.
_PANEL_ATTRS = {
    "browser":     "browser",
    "molecules":   "browser",
    "search":      "search",
    "viewer_2d":   "viewer_2d",
    "2d":          "viewer_2d",
    "viewer_3d":   "viewer_3d",
    "3d":          "viewer_3d",
    "props":       "props",
    "properties":  "props",
    "tutor":       "tutor",
    "chat":        "tutor",
    "session_log": "session_log",
    "log":         "session_log",
    "tutorial":    "tutorial_panel",
    "tutorials":   "tutorial_panel",
}


def _settle(ms: int) -> None:
    """Block locally while pumping Qt events for *ms* milliseconds.

    Used before a screenshot to let QWebEngineView / 3Dmol.js finish
    rendering. Does nothing if no QApplication exists.
    """
    from PySide6.QtCore import QEventLoop, QTimer
    from PySide6.QtWidgets import QApplication
    if QApplication.instance() is None or ms <= 0:
        return
    loop = QEventLoop()
    QTimer.singleShot(ms, loop.quit)
    loop.exec()


@action(category="export")
def export_molecule_2d_by_id(molecule_id: int, path: str,
                             width: int = 600, height: int = 600) -> Dict[str, Any]:
    """Export a 2D structure to a file. Extension picks the format (.png/.svg)."""
    from orgchem.render.export import export_molecule_2d
    row = get_molecule(molecule_id)
    if row is None:
        return {"error": f"No molecule id {molecule_id}"}
    mol = mol_from_smiles(row.smiles)
    out = export_molecule_2d(mol, path, width=width, height=height)
    return {
        "path": str(out),
        "format": out.suffix.lstrip(".").lower(),
        "name": row.name,
        "size_bytes": out.stat().st_size,
    }


@action(category="export")
def export_current_molecule_2d(path: str, width: int = 600, height: int = 600) -> Dict[str, Any]:
    """Export the molecule currently shown in the 2D viewer."""
    from orgchem.agent.controller import require_main_window
    from orgchem.render.export import export_molecule_2d
    win = require_main_window()
    smiles = getattr(win.viewer_2d, "_current_smiles", None)
    if not smiles:
        return {"error": "No molecule is currently selected"}
    mol = mol_from_smiles(smiles)
    out = export_molecule_2d(mol, path, width=width, height=height)
    return {"path": str(out), "format": out.suffix.lstrip(".").lower(),
            "size_bytes": out.stat().st_size}


@action(category="export")
def screenshot_window(path: str, settle_ms: int = 500) -> Dict[str, Any]:
    """Screenshot the main application window.

    ``settle_ms`` delays the grab so QWebEngineView (3Dmol.js) has time to
    finish rendering. 500 ms is usually enough for a single molecule; bump
    to 1000–2000 ms after switching molecules.
    """
    from orgchem.agent.controller import require_main_window
    from orgchem.render.screenshot import grab_widget
    win = require_main_window()
    _settle(settle_ms)
    out = grab_widget(win, path)
    return {"path": str(out), "size_bytes": out.stat().st_size}


@action(category="export")
def screenshot_panel(panel_name: str, path: str, settle_ms: int = 300) -> Dict[str, Any]:
    """Screenshot a single panel. panel_name accepts friendly aliases:
    viewer_2d / 2d, viewer_3d / 3d, browser / molecules, props / properties,
    tutor / chat, session_log / log, tutorial / tutorials, search,
    reactions, compare.
    """
    from orgchem.agent.controller import require_main_window
    from orgchem.render.screenshot import grab_widget
    _PANEL_ATTRS["reactions"] = "reactions"
    _PANEL_ATTRS["compare"] = "compare"
    win = require_main_window()
    attr = _PANEL_ATTRS.get(panel_name.lower())
    if attr is None:
        return {"error": f"Unknown panel {panel_name!r}. "
                         f"Known: {sorted(set(_PANEL_ATTRS))}"}
    panel = getattr(win, attr, None)
    if panel is None:
        return {"error": f"MainWindow has no attribute {attr!r}"}
    _settle(settle_ms)
    out = grab_widget(panel, path)
    return {"path": str(out), "panel": panel_name, "resolved": attr,
            "size_bytes": out.stat().st_size}


# ---- 3D export (matplotlib backend — works in any Qt mode) -----------

@action(category="export")
def export_molecule_3d(molecule_id: int, path: str,
                       style: str = "ball-and-stick",
                       width: int = 800, height: int = 600) -> Dict[str, Any]:
    """Render a molecule's 3D structure to PNG via matplotlib.

    Works in any Qt platform (including offscreen / headless). The 3D
    coordinates are generated via RDKit if not already stored.
    Styles: ball-and-stick, sphere, stick, line.
    """
    from orgchem.render import draw3d_mpl
    from orgchem.core.molecule import Molecule
    from rdkit import Chem

    row = get_molecule(molecule_id)
    if row is None:
        return {"error": f"No molecule id {molecule_id}"}
    mol = None
    if row.molblock_3d:
        mol = Chem.MolFromMolBlock(row.molblock_3d, removeHs=False)
    if mol is None or mol.GetNumConformers() == 0:
        m = Molecule.from_smiles(row.smiles, name=row.name, generate_3d=True)
        if not m.molblock_3d:
            return {"error": f"Could not generate 3D coordinates for {row.name}"}
        mol = Chem.MolFromMolBlock(m.molblock_3d, removeHs=False)

    from pathlib import Path as _P
    out = draw3d_mpl.render_png(mol, _P(path), style=style,
                                width=width, height=height)
    return {
        "path": str(out),
        "style": style,
        "name": row.name,
        "size_bytes": out.stat().st_size,
    }


# Reaction / mechanism / compare_molecules actions live in a sibling
# module to keep this file under the 500-line project cap. Importing
# :mod:`orgchem.agent.library` (or just :mod:`orgchem.agent`) registers
# both sets of actions transparently.
from orgchem.agent import actions_reactions  # noqa: F401
