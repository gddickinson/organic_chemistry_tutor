"""Phase 32e tests — tutor Reply-with-a-script mode.

Three layers:
1. Headless: ``extract_python_blocks`` pulls fenced code out of
   mixed markdown/prose.
2. Headless: ``build_script_mode_system_prompt`` extends the
   tutor system prompt with the Phase 32e addendum.
3. GUI (pytest-qt): toggling the ``Reply with a script`` checkbox
   on ``TutorPanel`` swaps the live Conversation's system prompt;
   a fenced code block in the transcript renders a clickable
   ``orgchem-script:<idx>`` anchor whose handler loads the block
   into the singleton Script Editor dialog.
"""
from __future__ import annotations

import pytest

from orgchem.agent.conversation import (
    _SCRIPT_MODE_ADDENDUM,
    _SYSTEM_PROMPT,
    build_script_mode_system_prompt,
)
from orgchem.agent.script_context import extract_python_blocks


# ---------------------------------------------------------------
# Layer 1 — headless extractor

def test_extract_blocks_python_fence():
    text = (
        "Here is a script:\n"
        "```python\n"
        "print('hi')\n"
        "viewer.add_molecule('CCO')\n"
        "```\n"
        "All done."
    )
    blocks = extract_python_blocks(text)
    assert len(blocks) == 1
    assert "viewer.add_molecule('CCO')" in blocks[0]
    assert blocks[0].startswith("print('hi')")


def test_extract_blocks_multiple():
    text = (
        "```python\nprint(1)\n```\n"
        "and\n"
        "```python\nprint(2)\n```"
    )
    blocks = extract_python_blocks(text)
    assert blocks == ["print(1)", "print(2)"]


def test_extract_blocks_bare_fence_also_works():
    """The LLM sometimes omits the language tag; we still want
    the Run-button to appear."""
    text = "```\nprint('hi')\n```"
    assert extract_python_blocks(text) == ["print('hi')"]


def test_extract_blocks_py_alias():
    text = "```py\nprint('x')\n```"
    assert extract_python_blocks(text) == ["print('x')"]


def test_extract_blocks_no_fence_returns_empty():
    assert extract_python_blocks("just some prose with no code.") == []
    assert extract_python_blocks("") == []


def test_extract_blocks_handles_nested_triple_backticks_in_prose():
    """If the LLM puts ``` inline in plain prose without a
    newline-delimited block, we should not spuriously match."""
    text = "use ``` to delimit fences. That's it."
    assert extract_python_blocks(text) == []


# ---------------------------------------------------------------
# Layer 2 — headless system-prompt builder

def test_system_prompt_addendum_is_appended():
    combined = build_script_mode_system_prompt()
    assert combined.startswith(_SYSTEM_PROMPT.rstrip()[:80])
    assert _SCRIPT_MODE_ADDENDUM.strip() in combined


def test_system_prompt_addendum_mentions_key_globals():
    """The addendum is the only thing the LLM sees about the
    script-mode contract — make sure every pre-imported global
    is named."""
    for name in ("app", "chem", "orgchem", "viewer"):
        assert name in _SCRIPT_MODE_ADDENDUM, (
            f"script-mode addendum is missing {name!r}")
    for fn in ("add_molecule", "add_protein", "list_actions"):
        assert fn in _SCRIPT_MODE_ADDENDUM


def test_build_with_custom_base():
    custom = "You are a short-answer tutor. Always be terse."
    combined = build_script_mode_system_prompt(custom)
    assert custom in combined
    assert _SCRIPT_MODE_ADDENDUM.strip() in combined


# ---------------------------------------------------------------
# Layer 3 — GUI integration

pytest.importorskip("pytestqt", reason="pytest-qt not installed")


@pytest.fixture(scope="module")
def _app():
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as app:
        yield app


def test_script_mode_toggle_swaps_system_prompt(_app, qtbot):
    """Ticking the checkbox on a connected TutorPanel should
    swap ``Conversation.system_prompt`` to the extended version
    (and back when unticked)."""
    from orgchem.config import AppConfig
    from orgchem.gui.panels.tutor_panel import TutorPanel
    from orgchem.agent.conversation import Conversation

    cfg = AppConfig.load()
    panel = TutorPanel(cfg)
    qtbot.addWidget(panel)
    # Fake a connected conversation without actually hitting an
    # LLM backend — the conversation object is enough for the
    # toggle logic.
    panel._convo = Conversation.__new__(Conversation)
    panel._convo.system_prompt = _SYSTEM_PROMPT
    panel._convo.history = []
    panel._convo.backend = None
    panel._convo.max_tool_rounds = 8

    panel.script_mode_cb.setChecked(True)
    assert "Reply-with-a-script mode" in panel._convo.system_prompt

    panel.script_mode_cb.setChecked(False)
    assert panel._convo.system_prompt == _SYSTEM_PROMPT


def test_fenced_block_in_assistant_reply_renders_run_anchor(
    _app, qtbot,
):
    from orgchem.config import AppConfig
    from orgchem.gui.panels.tutor_panel import TutorPanel

    cfg = AppConfig.load()
    panel = TutorPanel(cfg)
    qtbot.addWidget(panel)

    reply = (
        "Here's how to show caffeine:\n"
        "```python\n"
        "app.show_molecule(name_or_id='Caffeine')\n"
        "```\n"
    )
    panel._append_assistant(reply)

    # The extracted block must have been stashed for the
    # anchor handler to retrieve.
    assert 0 in panel._script_blocks
    assert "show_molecule" in panel._script_blocks[0]

    # Transcript HTML should contain both the preview pre-block
    # AND the orgchem-script:0 anchor href.
    html = panel.transcript.toHtml()
    assert "show_molecule" in html
    assert "orgchem-script:0" in html


def test_anchor_click_loads_block_into_editor(_app, qtbot):
    from PySide6.QtCore import QUrl
    from orgchem.config import AppConfig
    from orgchem.gui.dialogs.script_editor import ScriptEditorDialog
    from orgchem.gui.panels.tutor_panel import TutorPanel

    cfg = AppConfig.load()
    panel = TutorPanel(cfg)
    qtbot.addWidget(panel)

    panel._script_blocks[0] = "print('loaded via anchor')"
    panel._on_anchor_clicked(QUrl("orgchem-script:0"))

    # Singleton dialog should now carry the block in its editor.
    # (Do NOT register it with qtbot — the singleton is owned by
    # the class and qtbot's teardown would double-close it.)
    dlg = ScriptEditorDialog.singleton(parent=panel.window())
    try:
        assert "loaded via anchor" in dlg._editor.toPlainText()
    finally:
        dlg.close()
        ScriptEditorDialog._instance = None
