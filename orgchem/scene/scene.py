"""Phase 32b — Scene class and Track model.

A Scene is an ordered list of named Tracks (molecule / protein /
ligand).  Mutating the scene is always safe: the internal state
updates regardless of whether a view is attached, and attached
listeners are notified so they can re-render.  Fully headless-
testable — no Qt imports in this module.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

log = logging.getLogger(__name__)


class TrackKind(str, Enum):
    MOLECULE = "molecule"
    PROTEIN = "protein"
    LIGAND = "ligand"


@dataclass
class Track:
    """One element of the scene.  Immutable name, mutable style."""

    name: str
    kind: TrackKind
    #: The raw data the 3Dmol.js layer renders.  For ``molecule`` this
    #: is a molblock string; for ``protein`` it's the full PDB text;
    #: for ``ligand`` it's a molblock.
    data: str
    #: Source format tag passed to ``v.addModel(data, fmt)`` in 3Dmol.js.
    #: ``'mol'`` for molblock, ``'pdb'`` for PDB text.
    source_format: str
    style: str = "stick"        # stick / sphere / line / cartoon / surface
    colour: str = "cpk"         # cpk / chain / residue / spectrum
    visible: bool = True
    opacity: float = 1.0
    #: Free-form metadata for the track list UI (e.g. {'smiles': 'CCO',
    #: 'pdb_id': '2YDO', 'descriptors': {...}}).
    meta: Dict[str, Any] = field(default_factory=dict)

    def summary(self) -> str:
        """One-line human summary used by the tracks list widget."""
        bits = [self.style]
        if self.meta.get("smiles"):
            bits.append(self.meta["smiles"])
        elif self.meta.get("pdb_id"):
            bits.append(self.meta["pdb_id"].upper())
        return f"{self.name}  ({self.kind.value}, {', '.join(bits)})"


class SceneEvent(str, Enum):
    """What happened to a Scene — passed to listeners so they know
    whether a full rebuild is needed or a cheap update suffices."""

    TRACK_ADDED = "track_added"
    TRACK_REMOVED = "track_removed"
    TRACK_STYLE_CHANGED = "track_style_changed"
    TRACK_VISIBILITY_CHANGED = "track_visibility_changed"
    CLEARED = "cleared"
    CAMERA_CHANGED = "camera_changed"


SceneListener = Callable[[SceneEvent, Optional[Track]], None]


class Scene:
    """Composable scene graph for the Workbench viewer.

    The Scene is observable: attach a listener with :meth:`listen`
    and it'll be called after every mutation.  Listeners are
    expected to be cheap (the Workbench's listener does a full
    HTML rebuild, but the rebuild is fast enough for interactive
    use with < 100 tracks).
    """

    def __init__(self) -> None:
        self._tracks: List[Track] = []
        self._listeners: List[SceneListener] = []
        self._auto_name_counter = 0

    # -------- Observer --------

    def listen(self, fn: SceneListener) -> Callable[[], None]:
        """Register a listener.  Returns an unsubscribe thunk."""
        self._listeners.append(fn)
        return lambda: (self._listeners.remove(fn)
                        if fn in self._listeners else None)

    def _emit(self, ev: SceneEvent, track: Optional[Track] = None) -> None:
        for fn in list(self._listeners):
            try:
                fn(ev, track)
            except Exception:     # pragma: no cover - defensive
                log.exception("Scene listener raised")

    # -------- Track management --------

    def tracks(self) -> List[Track]:
        """Return a copy of the current track list (mutating the
        copy is safe)."""
        return list(self._tracks)

    def _next_auto_name(self, prefix: str) -> str:
        while True:
            self._auto_name_counter += 1
            name = f"{prefix}{self._auto_name_counter}"
            if not self._track_by_name(name):
                return name

    def _track_by_name(self, name: str) -> Optional[Track]:
        for t in self._tracks:
            if t.name == name:
                return t
        return None

    def _add_track(self, t: Track) -> Track:
        if self._track_by_name(t.name):
            raise ValueError(
                f"track named {t.name!r} already exists — pick a "
                "different name or call scene.remove() first"
            )
        self._tracks.append(t)
        self._emit(SceneEvent.TRACK_ADDED, t)
        return t

    def remove(self, name: str) -> bool:
        """Drop a track by name.  Returns ``True`` if anything was
        removed, ``False`` if the name was absent."""
        t = self._track_by_name(name)
        if t is None:
            return False
        self._tracks.remove(t)
        self._emit(SceneEvent.TRACK_REMOVED, t)
        return True

    def clear(self) -> None:
        """Remove every track at once."""
        if not self._tracks:
            return
        self._tracks.clear()
        self._emit(SceneEvent.CLEARED, None)

    def set_visible(self, name: str, visible: bool) -> None:
        t = self._track_by_name(name)
        if t is None:
            raise KeyError(name)
        if t.visible == visible:
            return
        t.visible = visible
        self._emit(SceneEvent.TRACK_VISIBILITY_CHANGED, t)

    def set_style(self, name: str, *, style: Optional[str] = None,
                  colour: Optional[str] = None,
                  opacity: Optional[float] = None) -> None:
        t = self._track_by_name(name)
        if t is None:
            raise KeyError(name)
        if style is not None:
            t.style = style
        if colour is not None:
            t.colour = colour
        if opacity is not None:
            t.opacity = float(opacity)
        self._emit(SceneEvent.TRACK_STYLE_CHANGED, t)

    # -------- Add molecule / protein / ligand --------

    def add_molecule(self, smiles_or_mol: Any, *, track: Optional[str] = None,
                     style: str = "stick", colour: str = "cpk") -> Track:
        """Embed a small molecule into the scene.

        Accepts a SMILES string, an ``orgchem.core.Molecule``, or an
        RDKit ``Mol``.  3D coordinates are generated on the fly when
        the input lacks them.
        """
        molblock, meta = _mol_to_molblock(smiles_or_mol)
        name = track or self._next_auto_name("mol")
        t = Track(
            name=name, kind=TrackKind.MOLECULE,
            data=molblock, source_format="mol",
            style=style, colour=colour, meta=meta,
        )
        return self._add_track(t)

    def add_protein(self, pdb_id_or_text: str, *, track: Optional[str] = None,
                    style: str = "cartoon",
                    colour: str = "chain") -> Track:
        """Embed a protein by PDB ID (fetched + cached via
        :mod:`orgchem.sources.pdb`) or by raw PDB text.

        Heuristic: a 4-character alphanumeric input is treated as a
        PDB ID; anything else is read as PDB text.
        """
        stripped = pdb_id_or_text.strip()
        if _looks_like_pdb_id(stripped):
            from orgchem.sources.pdb import fetch_pdb_text
            pdb_text = fetch_pdb_text(stripped)
            meta = {"pdb_id": stripped.lower()}
        else:
            pdb_text = pdb_id_or_text
            meta = {}
        name = track or self._next_auto_name("prot")
        t = Track(
            name=name, kind=TrackKind.PROTEIN,
            data=pdb_text, source_format="pdb",
            style=style, colour=colour, meta=meta,
        )
        return self._add_track(t)

    # -------- Snapshot / camera --------

    def snapshot(self, path: Union[str, Path]) -> Path:
        """Save a PNG of the current 3Dmol.js view.

        Dispatches to any registered :class:`~orgchem.gui.panels.workbench`
        widget.  If no widget is attached (headless scripts, unit
        tests), raises ``RuntimeError``.
        """
        for fn in list(self._listeners):
            if hasattr(fn, "__self__") and hasattr(fn.__self__,
                                                   "grab_png"):
                return fn.__self__.grab_png(Path(path))   # type: ignore[attr-defined]
        raise RuntimeError(
            "No Workbench widget is attached — snapshot needs the "
            "GUI. Open the Workbench tab first."
        )


# ---------------------------------------------------------------
# Module-level "current scene" — the Workbench and the ScriptContext
# both bind to this single instance.

_CURRENT_SCENE: Optional[Scene] = None


def current_scene() -> Scene:
    """Return the process-wide Scene used by the Workbench + scripts."""
    global _CURRENT_SCENE
    if _CURRENT_SCENE is None:
        _CURRENT_SCENE = Scene()
    return _CURRENT_SCENE


def reset_current_scene() -> None:
    """Test / debug hook — start fresh."""
    global _CURRENT_SCENE
    _CURRENT_SCENE = None


# ---------------------------------------------------------------
# Helpers

def _looks_like_pdb_id(s: str) -> bool:
    """Four-char alphanumeric heuristic — the PDB ID format."""
    return (len(s) == 4 and s.isalnum()
            and not s.isdigit()   # reject pure-digit edge cases
            and "\n" not in s)


def _mol_to_molblock(obj: Any) -> tuple[str, Dict[str, Any]]:
    """Coerce SMILES / ``Molecule`` / RDKit ``Mol`` → (molblock,
    metadata dict).  Generates 3D coords if missing."""
    from rdkit import Chem
    from rdkit.Chem import AllChem

    if hasattr(obj, "molblock_3d") and obj.molblock_3d:
        # orgchem.core.Molecule with cached 3D
        smiles = obj.smiles if hasattr(obj, "smiles") else ""
        return obj.molblock_3d, {"smiles": smiles}

    if isinstance(obj, str):
        mol = Chem.MolFromSmiles(obj)
        if mol is None:
            raise ValueError(f"could not parse SMILES {obj!r}")
        smiles_in = obj
    elif hasattr(obj, "GetNumAtoms"):     # rdkit Mol
        mol = obj
        try:
            smiles_in = Chem.MolToSmiles(mol)
        except Exception:
            smiles_in = ""
    elif hasattr(obj, "mol"):             # orgchem Molecule wrapper
        mol = obj.mol
        smiles_in = getattr(obj, "smiles", "") or Chem.MolToSmiles(mol)
    else:
        raise TypeError(
            f"add_molecule wants SMILES / Mol / Molecule; got {type(obj)}")

    if mol.GetNumConformers() == 0:
        mol = Chem.AddHs(mol)
        AllChem.EmbedMolecule(mol, randomSeed=0xF00D)
        try:
            AllChem.MMFFOptimizeMolecule(mol, maxIters=200)
        except Exception:
            pass
    return Chem.MolToMolBlock(mol), {"smiles": smiles_in}
