"""Phase 32d smoke tests — every bundled demo script under
``data/script_library/`` must run to completion without raising.

Each demo doubles as a regression test for the Scene + action-
registry surface.  Because the demos exercise real seeded content
(mechanisms, lipids, retro templates), they also catch
content-drift regressions that pure unit tests miss.

**Round 71 strengthening (user report 2026-04-23):** in addition
to "ran without raising + non-empty stdout", each demo now has
a curated list of content markers that MUST appear in stdout —
specific numeric values, compound names, category labels.  This
catches the silent-zero class of bug where a demo read an action
response under made-up keys, formatted ``0`` everywhere, and
still passed the non-empty-stdout check (demo 03 did exactly
this round 70 before the user caught it).
"""
from __future__ import annotations

from pathlib import Path

import pytest

from orgchem.agent.headless import HeadlessApp
from orgchem.agent.script_context import ScriptContext
from orgchem.scene import reset_current_scene

_SCRIPT_DIR = Path(__file__).resolve().parents[1] / "data" / "script_library"


#: Per-demo content markers.  Each key is a script filename; each
#: value is a list of substrings that MUST appear in the demo's
#: stdout.  Pick stable landmarks — a well-known MW, a compound
#: name, a category label — so the check catches silent-zero /
#: wrong-key bugs but isn't brittle to minor formatting tweaks.
_CONTENT_MARKERS: dict[str, list[str]] = {
    "01_caffeine_tour.py": [
        "Caffeine", "194.19",          # real MW of caffeine
        "Aromatic C–H",           # IR band label
        "QED =",                       # not "QED = 0.000" anymore
    ],
    "02_scene_composer_basics.py": [
        "methane", "cyclohex",
        "Added 6 tracks",
        "style=sphere",                # butane was restyled
    ],
    "03_nsaids_overlay.py": [
        "aspirin", "ibuprofen", "naproxen", "celecoxib",
        "180.", "206.", "230.", "381.",    # real MW values
        "pass",                            # Lipinski column
    ],
    "04_mechanism_walkthrough.py": [
        "Seeded mechanisms:",
        "Diels-Alder",
        "Substitution",
        # Enriched in round 81 — demo now uses get_mechanism_details
        # to print the real arrow + lone-pair data for the DA entry.
        "full arrow walkthrough",
        "arrows",
        "curly",
    ],
    "05_lipid_mw_report.py": [
        "Caprylic acid",
        "144.",                # real MW of caprylic
        "DHA",
        "ω-3",            # ω-3 greek-omega marker
    ],
    "06_retrosynthesis_demo.py": [
        "aspirin",
        "Ester ⇒ Carboxylic acid",
        "Fischer esterification",
        "CC(=O)O",
    ],
    "07_aspirin_pathway.py": [
        "Aspirin",
        "75.",                 # AE (~75%) for the Hoffmann route
        "atom economy",
    ],
    "08_stereochem_tour.py": [
        "L-alanine",
        "'S'", "'R'",          # descriptors as strings in repr
        "enantiomer_of",
    ],
    "09_energy_profile_diels_alder.py": [
        "Diels-Alder",
        "Ea (forward):",
        "115.",                # real TS energy
        "-165.",               # real ΔH
        "exothermic",
    ],
    "10_huckel_benzene.py": [
        "Benzene",
        "π atoms:     6",
        "HOMO",
        "LUMO",
        "+2.",        # textbook most-bonding MO energy: α + 2β
        "-2.",        # textbook most-antibonding: α − 2β
    ],
    "11_nsaid_sar.py": [
        "NSAID",
        "Ibuprofen",
        "Naproxen",
        "COX1 IC50",
        "206.",     # ibuprofen MW
    ],
    "12_macromolecule_catalogue.py": [
        "Carbohydrates",
        "Lipids",
        "Nucleic acids",
        "monosaccharide",
        "fatty-acid",
        "PDB-motif",
    ],
    "13_butane_dihedral.py": [
        "butane",
        "frames:",
        "36",              # default n_frames
        "butane_dihedral.html",
    ],
    "14_retrosynthesis_tree.py": [
        "methyl 4-phenyl",
        "Routes found:",
        "Ester ⇒ Carboxylic acid",
        "Biaryl ⇒ Aryl halide",
        "terminal precursor",
    ],
    "15_glossary_tour.py": [
        "Glossary catalogue:",
        "terms",
        "mechanism",       # a known category name
        "Bürgi-Dunitz",    # the demo term we define()
    ],
}


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

    # Content markers — spot-check specific values per demo so a
    # silent-zero bug (wrong key name returning 0 / empty) fails
    # here instead of slipping past like demo 03 did round 70.
    markers = _CONTENT_MARKERS.get(script_path.name, [])
    missing = [m for m in markers if m not in result.stdout]
    assert not missing, (
        f"{script_path.name} is missing content markers "
        f"{missing!r} — a silent-output regression?\n"
        f"--- stdout ---\n{result.stdout}"
    )


def test_every_demo_has_content_markers():
    """Every discovered script must appear in ``_CONTENT_MARKERS``.
    Prevents a new demo from landing without a quality gate."""
    missing = [p.name for p in _discover_scripts()
               if p.name not in _CONTENT_MARKERS]
    assert not missing, (
        f"Scripts without _CONTENT_MARKERS entries: {missing}.  "
        f"Add at least 2 stable markers per script to "
        f"tests/test_script_library.py::_CONTENT_MARKERS."
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
