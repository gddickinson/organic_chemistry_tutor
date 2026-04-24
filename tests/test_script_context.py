"""Phase 32a regression tests for :class:`ScriptContext` — the
headless half of the scripting workbench.  No Qt imports."""
from __future__ import annotations

import pytest

from orgchem.agent.script_context import (
    AppProxy,
    ExecResult,
    ScriptContext,
    WorkbenchNotReadyError,
)


def test_simple_expression_returns_repr():
    ctx = ScriptContext()
    result = ctx.run("1 + 2")
    assert result.ok
    assert result.repr_value == "3"
    assert result.stdout == ""
    assert result.traceback == ""


def test_print_capture():
    ctx = ScriptContext()
    result = ctx.run("print('hello'); print('world')")
    assert result.ok
    assert result.stdout == "hello\nworld\n"
    # Multi-statement → no repr_value.
    assert result.repr_value == ""


def test_globals_persist_between_runs():
    ctx = ScriptContext()
    ctx.run("x = 10")
    result = ctx.run("x * 4")
    assert result.repr_value == "40"


def test_reset_flushes_globals():
    ctx = ScriptContext()
    ctx.run("spam = 'eggs'")
    ctx.reset()
    result = ctx.run("spam")
    assert not result.ok
    assert "NameError" in result.traceback


def test_syntax_error_caught():
    ctx = ScriptContext()
    result = ctx.run("def foo(:")   # intentionally bad
    assert not result.ok
    assert "SyntaxError" in result.traceback


def test_runtime_error_caught_and_continues():
    ctx = ScriptContext()
    bad = ctx.run("1 / 0")
    assert not bad.ok
    assert "ZeroDivisionError" in bad.traceback
    # Subsequent runs still work — state is preserved.
    ok = ctx.run("2 + 2")
    assert ok.ok
    assert ok.repr_value == "4"


def test_preimported_globals_are_present():
    ctx = ScriptContext()
    result = ctx.run("type(app).__name__")
    assert result.ok
    assert "AppProxy" in result.repr_value


def test_chem_import_exposed_as_alias():
    ctx = ScriptContext()
    result = ctx.run("chem.MolFromSmiles('CCO').GetNumAtoms()")
    assert result.ok
    assert result.repr_value == "3"


def test_viewer_is_a_real_scene_object():
    """Phase 32b graduates ``viewer`` from a stub to the process-wide
    Scene.  It should accept ``add_molecule(...)`` without raising."""
    from orgchem.scene import Scene, reset_current_scene
    reset_current_scene()
    ctx = ScriptContext()
    result = ctx.run("type(viewer).__name__")
    assert result.ok
    assert result.repr_value == "'Scene'"
    # ...and actually accepts scene mutations:
    result = ctx.run(
        "viewer.add_molecule('CCO', track='eth')\n"
        "print(len(viewer.tracks()))")
    assert result.ok, result.traceback
    assert result.stdout.strip() == "1"


def test_app_proxy_lists_actions():
    proxy = AppProxy()
    names = proxy.list_actions()
    assert isinstance(names, list)
    # These should exist no matter what gets added later.
    for expected in ("show_molecule", "list_reactions",
                     "open_script_editor"):
        assert expected in names, f"action {expected!r} missing"


def test_app_proxy_unknown_action_raises_attribute_error():
    proxy = AppProxy()
    with pytest.raises(AttributeError):
        _ = proxy.definitely_not_a_real_action


def test_app_call_routes_through_registry():
    """The canonical ``app.call('…')`` path should invoke the named
    action and return its result."""
    proxy = AppProxy()
    # Use a read-only action that doesn't touch the GUI.
    result = proxy.call("list_naming_rules")
    assert isinstance(result, (list, dict)), type(result)


def test_stderr_capture_separate_from_stdout():
    import sys
    ctx = ScriptContext()
    result = ctx.run(
        "import sys; sys.stdout.write('a'); sys.stderr.write('b')"
    )
    assert result.ok
    assert result.stdout == "a"
    assert result.stderr == "b"


def test_exec_result_ok_true_when_no_traceback():
    assert ExecResult().ok is True
    assert ExecResult(traceback="boom").ok is False
