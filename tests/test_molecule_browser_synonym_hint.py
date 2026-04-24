"""Phase 35f round 110 regression tests for the molecule-browser
synonym hint — confirms the list row shows the first natural-language
synonym after the canonical name / formula, and that registry IDs
are filtered out of both the row label and the tooltip."""
from __future__ import annotations

import json
import pytest

from PySide6.QtCore import Qt

pytest.importorskip("rdkit")
pytest.importorskip("pytestqt", reason="pytest-qt not installed")


@pytest.fixture(scope="module")
def _app():
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as app:
        yield app


def test_first_natural_synonym_strips_registry_noise():
    """Helper must drop CAS numbers, CHEMBL IDs, InChI strings from
    the 'first synonym' pick."""
    from orgchem.gui.panels.molecule_browser import (
        _first_natural_synonym, _all_synonyms,
    )

    class _Row:
        name = "Acetaminophen"
        synonyms_json = json.dumps([
            "103-90-2",      # CAS — reject
            "CHEMBL112",     # reject
            "Paracetamol",   # keep — should win
            "APAP",          # keep (but paracetamol is first)
            "4-Acetamidophenol",
        ])

    assert _first_natural_synonym(_Row()) == "Paracetamol"
    # Full list preserves natural-language synonyms in order.
    assert _all_synonyms(_Row()) == [
        "Paracetamol", "APAP", "4-Acetamidophenol"
    ]


def test_first_natural_synonym_empty_when_no_synonyms():
    from orgchem.gui.panels.molecule_browser import _first_natural_synonym

    class _Row:
        name = "Caffeine"
        synonyms_json = None

    assert _first_natural_synonym(_Row()) == ""

    class _Row2:
        name = "Caffeine"
        synonyms_json = json.dumps([])

    assert _first_natural_synonym(_Row2()) == ""


def test_first_natural_synonym_drops_canonical_self_reference():
    """A synonym equal to the canonical name (case-insensitive) must
    not be offered as the hint — that's just noise."""
    from orgchem.gui.panels.molecule_browser import _first_natural_synonym

    class _Row:
        name = "Aspirin"
        synonyms_json = json.dumps(["aspirin", "Acetylsalicylic acid"])

    assert _first_natural_synonym(_Row()) == "Acetylsalicylic acid"


def test_browser_display_role_includes_synonym(_app, qtbot):
    """Integration: load the real browser model + confirm ≥1 row
    surfaces a natural-language synonym in its Display string."""
    from orgchem.gui.panels.molecule_browser import _MolListModel
    m = _MolListModel()
    m.reload("")
    assert m.rowCount() > 0
    found_synonym_hint = False
    for i in range(m.rowCount()):
        idx = m.index(i, 0)
        label = m.data(idx, Qt.DisplayRole)
        if label and " · " in label:
            found_synonym_hint = True
            # The sidecar string is a natural-language synonym,
            # never a CAS / ChEMBL / InChI token.
            _, hint = label.rsplit(" · ", 1)
            from orgchem.gui.dialogs.command_palette import (
                _looks_like_registry_id,
            )
            assert not _looks_like_registry_id(hint), hint
            break
    assert found_synonym_hint, (
        "Expected ≥1 browser row to show a synonym hint after the "
        "round-58 + curated synonyms landed")


def test_browser_tooltip_lists_synonyms(_app, qtbot):
    """Tooltip must include the 'Also known as: …' line when
    synonyms are present, SMILES alone otherwise."""
    from orgchem.gui.panels.molecule_browser import _MolListModel
    m = _MolListModel()
    m.reload("")
    saw_aka = False
    saw_plain = False
    for i in range(m.rowCount()):
        tip = m.data(m.index(i, 0), Qt.ToolTipRole)
        if tip and "Also known as:" in tip:
            saw_aka = True
        elif tip and "Also known as:" not in tip:
            saw_plain = True
        if saw_aka and saw_plain:
            break
    assert saw_aka, "Expected ≥1 row with 'Also known as:' tooltip"
    assert saw_plain, "Expected ≥1 row with plain-SMILES tooltip"
