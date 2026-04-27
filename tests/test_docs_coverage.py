"""Phase 22a — doc-coverage contract.

Every module under ``orgchem/`` must be mentioned by filename in
``INTERFACE.md``. Catches the common failure mode where a new module
is added but the navigation map isn't updated — the project's
``CLAUDE.md`` makes that a rule, and this test enforces it.
"""
from __future__ import annotations
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ORGCHEM_DIR = PROJECT_ROOT / "orgchem"
INTERFACE_MD = PROJECT_ROOT / "INTERFACE.md"


# Modules that don't need an explicit INTERFACE.md entry — they are
# either trivial (__init__ package re-exports), generated, or grouped
# under a broader entry.
_EXEMPT = {
    "__init__.py",
    # agent sub-action files are collectively referenced via "library.py"
    # in INTERFACE.md; exempt them individually.
    "actions_reactions.py",
    "actions_pathways.py",
    "actions_dynamics.py",
    "actions_orbitals.py",
    "actions_stereo.py",
    "actions_glossary.py",
    "actions_medchem.py",
    "actions_labtech.py",
    "actions_naming.py",
    "actions_spectroscopy.py",
    "actions_retrosynthesis.py",
    "actions_sar.py",
    "actions_protein.py",
    "actions_hrms.py",
    "actions_session.py",
    "actions_periodic.py",
    "actions_carbohydrates.py",
    "actions_lipids_na.py",
    "actions_windows.py",
    "actions_meta.py",
    "actions_phys_org.py",
    "actions_authoring.py",
    # Private helper, documented inside its own module docstring.
    "_gui_dispatch.py",
}


def _python_modules_under(path: Path) -> list[Path]:
    """Return every *.py under path, relative to path, respecting _EXEMPT."""
    out: list[Path] = []
    for p in path.rglob("*.py"):
        if p.name in _EXEMPT:
            continue
        if "__pycache__" in p.parts:
            continue
        out.append(p.relative_to(path))
    return out


def test_interface_md_exists():
    assert INTERFACE_MD.exists(), "INTERFACE.md is missing from project root"


def test_every_module_referenced_in_interface_md():
    """For every orgchem/**/x.py, INTERFACE.md must mention "x.py" somewhere."""
    text = INTERFACE_MD.read_text()
    missing: list[str] = []
    for rel in _python_modules_under(ORGCHEM_DIR):
        if rel.name not in text:
            missing.append(str(rel))
    assert not missing, (
        "These modules under orgchem/ are not mentioned in INTERFACE.md:\n"
        + "\n".join(f"  - {m}" for m in missing)
    )


def test_interface_references_exist_on_disk():
    """Any backticked filename ending in .py in INTERFACE.md should exist
    somewhere under orgchem/ (prevents stale references)."""
    import re
    text = INTERFACE_MD.read_text()
    # Match ``word.py`` tokens. Strips word-boundary noise.
    pat = re.compile(r"`([A-Za-z_][A-Za-z0-9_/]*\.py)`")
    available_names = {p.name for p in ORGCHEM_DIR.rglob("*.py")}
    # Names that appear in the "Adding a new panel / data source" checklists
    # as pedagogical placeholders — never real files.
    placeholder_names = {
        "my_panel.py", "my_source.py",
    }
    missing: list[str] = []
    for m in pat.finditer(text):
        token = m.group(1)
        name = Path(token).name
        if name in placeholder_names:
            continue
        if name in available_names:
            continue
        scripts_dir = PROJECT_ROOT / "scripts"
        if (scripts_dir / name).exists():
            continue
        # main.py sits at project root.
        if (PROJECT_ROOT / name).exists():
            continue
        # tests/ is referenced from INTERFACE.md when describing
        # the audit gates that pin coverage floors.
        tests_dir = PROJECT_ROOT / "tests"
        if (tests_dir / name).exists():
            continue
        # cellbio/ (Phase CB-1.0 — sibling life-sciences studio).
        cellbio_dir = PROJECT_ROOT / "cellbio"
        if cellbio_dir.exists():
            cb_match = list(cellbio_dir.rglob(name))
            if cb_match:
                continue
        missing.append(token)
    assert not missing, (
        "INTERFACE.md references these .py files that no longer exist:\n"
        + "\n".join(f"  - {m}" for m in missing)
    )


def test_roadmap_md_exists():
    assert (PROJECT_ROOT / "ROADMAP.md").exists()


def test_project_status_md_exists():
    assert (PROJECT_ROOT / "PROJECT_STATUS.md").exists()


def test_session_log_md_exists():
    assert (PROJECT_ROOT / "SESSION_LOG.md").exists()
