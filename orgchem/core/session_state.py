"""Session state save / restore — Phase 20d.

Serialises the "user's place" in the app to a YAML file so a later
session can resume exactly where the last one left off. The captured
state intentionally stays small and GUI-framework-agnostic:

- Active tab (Molecule / Reactions / Compare / Synthesis / Glossary /
  Proteins).
- Current molecule by DB id and by SMILES (so the save file works
  even if the DB schema changes).
- Loaded PDB id + last ligand name used on the Proteins tab.
- Compare-panel slot SMILES list.
- Last HRMS measurement (mass + ppm tolerance) — lets students pick
  up a mid-problem calculation.

A minimal subset is enough for the workflows students actually want
to resume; more fields can be added without breaking existing files
because every field has a safe default in :class:`SessionState`.

The format is YAML via :mod:`yaml` (PyYAML) — same stack as the app
config — so sessions are human-readable and diff-able.
"""
from __future__ import annotations
import logging
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml

from orgchem.utils.paths import sessions_dir

log = logging.getLogger(__name__)


# ---------------------------------------------------------------------

@dataclass
class SessionState:
    """A snapshot of the user's current place in OrgChem Studio."""
    name: str = "session"
    saved_at: str = ""                # ISO-8601 timestamp
    version: int = 1

    # Navigation
    active_tab: str = ""              # tab label (or empty)

    # Molecule context
    current_molecule_id: Optional[int] = None
    current_molecule_smiles: str = ""

    # Proteins panel (Phase 24)
    protein_pdb_id: str = ""
    protein_ligand_name: str = ""
    na_ligand_name: str = ""

    # Compare panel
    compare_smiles: List[str] = field(default_factory=list)

    # HRMS guesser (Phase 4 follow-up)
    hrms_mass: Optional[float] = None
    hrms_ppm_tolerance: Optional[float] = None

    # Free-form notes the user can edit in the saved YAML — persisted
    # round-trip even though we never populate it ourselves.
    notes: str = ""

    # ----- API ------------------------------------------------------

    def to_yaml(self) -> str:
        return yaml.safe_dump(asdict(self), sort_keys=False)

    @classmethod
    def from_yaml(cls, text: str) -> "SessionState":
        data = yaml.safe_load(text) or {}
        # Drop keys we don't know about (forwards-compat) and defaults
        # will fill in missing ones.
        valid = {k for k in cls.__dataclass_fields__.keys()}
        return cls(**{k: v for k, v in data.items() if k in valid})


# ---------------------------------------------------------------------
# File I/O

def save_session(state: SessionState, path: Union[str, Path]) -> Path:
    """Write a :class:`SessionState` to ``path`` (creating parents).

    Automatically fills ``saved_at`` with the current timestamp so the
    value on disk always reflects the save moment, not whenever the
    dataclass was created.
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    state.saved_at = datetime.now().isoformat(timespec="seconds")
    p.write_text(state.to_yaml(), encoding="utf-8")
    log.info("Saved session → %s", p)
    return p


def load_session(path: Union[str, Path]) -> SessionState:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"No session file at {p}")
    return SessionState.from_yaml(p.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------
# Session-directory helpers

def list_sessions(directory: Optional[Union[str, Path]] = None
                  ) -> List[Dict[str, Any]]:
    """Enumerate saved sessions under ``directory`` (defaults to the
    per-user sessions dir). Each row carries the name, mtime, and path.
    Newest-first.
    """
    d = Path(directory) if directory else sessions_dir()
    if not d.exists():
        return []
    rows: List[Dict[str, Any]] = []
    for p in sorted(d.glob("*.yaml")):
        try:
            state = load_session(p)
        except Exception as e:  # noqa: BLE001
            log.warning("Skipping unreadable session %s (%s)", p, e)
            continue
        rows.append({
            "name": state.name,
            "path": str(p),
            "saved_at": state.saved_at,
            "active_tab": state.active_tab,
            "molecule_smiles": state.current_molecule_smiles,
            "protein_pdb_id": state.protein_pdb_id,
        })
    rows.sort(key=lambda r: r["saved_at"], reverse=True)
    return rows


def default_session_path(name: str,
                         directory: Optional[Union[str, Path]] = None
                         ) -> Path:
    """Build a ``directory/<slug>.yaml`` path for a session name."""
    d = Path(directory) if directory else sessions_dir()
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)
    if not safe:
        safe = "session"
    return d / f"{safe}.yaml"
