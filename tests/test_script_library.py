"""Phase 32d smoke tests — every bundled demo script under
``data/script_library/`` must run to completion without raising.

Each demo doubles as a regression test for the Scene + action-
registry surface.  Because the demos exercise real seeded content
(mechanisms, lipids, retro templates), they also catch
content-drift regressions that pure unit tests miss.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from orgchem.agent.headless import HeadlessApp
from orgchem.agent.script_context import ScriptContext
from orgchem.scene import reset_current_scene

_SCRIPT_DIR = Path(__file__).resolve().parents[1] / "data" / "script_library"


def _discover_scripts() -> list[Path]:
    if not _SCRIPT_DIR.exists():
        return []
    return sorted(p for p in _SCRIPT_DIR.glob("*.py"))


@pytest.fixture(scope="module")
def _app():
    """One HeadlessApp shared across every script — each boot takes
    ~1 s so a per-test fixture would dominate the test suite time."""
    with HeadlessApp() as app:
        yield app


@pytest.mark.parametrize(
    "script_path", _discover_scripts(),
    ids=lambda p: p.name,
)
def test_script_library_demo_runs_clean(script_path: Path, _app):
    """Run each demo through ``ScriptContext`` and assert it
    completes without an unhandled exception.

    Any demo that raises would fail here with the full traceback
    — same diagnostic the Script Editor gives the user.
    """
    reset_current_scene()    # fresh viewer / scene each script
    ctx = ScriptContext()
    src = script_path.read_text()
    result = ctx.run(src)
    assert result.ok, (
        f"{script_path.name} raised:\n"
        f"--- traceback ---\n{result.traceback}\n"
        f"--- stdout ---\n{result.stdout}\n"
        f"--- stderr ---\n{result.stderr}"
    )
    # Every demo should print *something* — an empty stdout would
    # be a silent no-op and probably a bug in the demo.
    assert result.stdout.strip(), (
        f"{script_path.name} produced no stdout — demo broken?"
    )


def test_script_library_is_not_empty():
    """Guard against a regression where the script directory
    accidentally lands empty (e.g. after a merge conflict).
    Round 67 ships 6 demos; the library is expected to keep
    growing — enforce a floor, not a ceiling."""
    scripts = _discover_scripts()
    assert len(scripts) >= 6, (
        f"Expected ≥ 6 demo scripts in {_SCRIPT_DIR}, "
        f"found {len(scripts)}"
    )
