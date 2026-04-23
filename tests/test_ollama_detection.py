"""Regression tests for the Ollama auto-detect fix (round 51).

The real problem reported by the user: 'Ollama is running but not
being picked up by the tutor'. Root cause was a hard-coded default
model (``llama3.1``) that wasn't actually installed. The fix makes
the Ollama backend probe ``/api/tags`` and auto-pick a matching
tool-use-capable model from what the user has pulled.
"""
from __future__ import annotations
from unittest.mock import patch

import pytest


def test_pick_best_model_prefers_tool_use_family():
    from orgchem.agent.llm.ollama_backend import _pick_best_model
    # User has mixed models. The tool-use-capable llama3.1 should win
    # over plain llama3.
    installed = ["llama3:latest", "llama3.1:8b", "codellama:7b"]
    assert _pick_best_model(installed) == "llama3.1:8b"


def test_pick_best_model_falls_back_to_first_entry():
    from orgchem.agent.llm.ollama_backend import _pick_best_model
    # No known tool-use family — take the first entry.
    installed = ["phi3:mini", "gemma:2b"]
    assert _pick_best_model(installed) == "phi3:mini"


def test_pick_best_model_returns_none_on_empty():
    from orgchem.agent.llm.ollama_backend import _pick_best_model
    assert _pick_best_model([]) is None


def test_pick_best_model_skips_vision_in_favour_of_plain_llama3():
    """Round-52 correction of the round-51 assertion. When the user
    has only ``llama3.2-vision`` and ``llama3``, the vision tag
    must NOT win: it's a specialist that expects images and can be
    incompatible with the running Ollama runtime. Falling through
    to plain ``llama3`` is the right behaviour — it at least
    supports text chat."""
    from orgchem.agent.llm.ollama_backend import _pick_best_model
    installed = ["llama3.2-vision:latest", "llama3:latest"]
    assert _pick_best_model(installed) == "llama3:latest"


def test_ollama_backend_constructor_uses_probed_model():
    """With auto_select=True and the probe returning real installed
    models, the backend's `model` attribute should be replaced with
    the best-matching installed tag."""
    from orgchem.agent.llm.ollama_backend import OllamaBackend
    with patch("orgchem.agent.llm.ollama_backend.ollama_list_models",
               return_value=["llama3:latest", "llama3.1:8b"]):
        b = OllamaBackend()
    assert b.model == "llama3.1:8b"
    assert "llama3:latest" in b.available_models


def test_ollama_backend_graceful_when_server_down():
    """If Ollama isn't running, `__init__` must not raise. Instead
    `available_models` stays empty and `model` falls back to the
    class default. This keeps the agent registry / headless tests
    usable on machines without Ollama."""
    from orgchem.agent.llm.ollama_backend import OllamaBackend
    from orgchem.messaging.errors import NetworkError
    with patch("orgchem.agent.llm.ollama_backend.ollama_list_models",
               side_effect=NetworkError("boom")):
        b = OllamaBackend()
    assert b.available_models == []
    assert b.model == "llama3.1"   # class default


def test_ollama_backend_respects_explicit_model():
    """If the caller passes ``model=``, that tag is honoured verbatim.
    The probe still runs (so ``available_models`` is populated for
    the tutor status line), but the explicit pick is never overridden."""
    from orgchem.agent.llm.ollama_backend import OllamaBackend
    with patch("orgchem.agent.llm.ollama_backend.ollama_list_models",
               return_value=["llama3.1:8b", "qwen2.5:14b"]):
        b = OllamaBackend(model="qwen2.5:14b")
    assert b.model == "qwen2.5:14b"
    # Probe still populates the catalogue so the UI can show a count.
    assert "llama3.1:8b" in b.available_models


def test_ollama_backend_auto_select_disabled():
    """`auto_select=False` is the escape hatch for pure unit tests."""
    from orgchem.agent.llm.ollama_backend import OllamaBackend
    with patch("orgchem.agent.llm.ollama_backend.ollama_list_models") as p:
        b = OllamaBackend(auto_select=False)
    assert b.model == "llama3.1"
    p.assert_not_called()


def test_ollama_list_models_raises_networkerror_on_connection_failure():
    from orgchem.agent.llm.ollama_backend import ollama_list_models
    from orgchem.messaging.errors import NetworkError
    import requests
    with patch("orgchem.agent.llm.ollama_backend.requests.get",
               side_effect=requests.ConnectionError("refused")):
        with pytest.raises(NetworkError):
            ollama_list_models()


# ---- model_supports_tools (round 52 bugfix) -----------------------

def test_model_supports_tools_accepts_known_tool_families():
    from orgchem.agent.llm.ollama_backend import model_supports_tools
    assert model_supports_tools("llama3.1:8b")
    assert model_supports_tools("llama3.2:3b")
    assert model_supports_tools("qwen2.5:14b")
    assert model_supports_tools("mixtral:latest")


def test_model_supports_tools_rejects_vision_variants():
    """Regression: the user reported that ``llama3.2-vision`` got
    picked as tool-capable and then Ollama 500'd. That tag must
    now be rejected by the support check."""
    from orgchem.agent.llm.ollama_backend import model_supports_tools
    assert not model_supports_tools("llama3.2-vision:latest")
    assert not model_supports_tools("llava:latest")


def test_model_supports_tools_rejects_code_variants():
    from orgchem.agent.llm.ollama_backend import model_supports_tools
    assert not model_supports_tools("codellama:7b")
    assert not model_supports_tools("deepseek-coder:latest")


def test_model_supports_tools_rejects_bare_llama3():
    """Plain ``llama3`` (the original 8B) returns
    "does not support tools" from Ollama. Don't send tools to it."""
    from orgchem.agent.llm.ollama_backend import model_supports_tools
    assert not model_supports_tools("llama3:latest")
    assert not model_supports_tools("llama3")


def test_pick_best_model_skips_vision_variants_in_fallback():
    """The user's reported install was ``llama3.2-vision`` +
    ``llama3``. Neither supports tools, but the picker must **not**
    land on the vision specialist as a fallback — those models
    are text-hostile and in the wild can be out-of-sync with the
    running Ollama runtime (the original round-52 bug). Fall
    through to ``llama3:latest``, which at least works for
    plain-text chat."""
    from orgchem.agent.llm.ollama_backend import _pick_best_model
    installed = ["llama3.2-vision:latest", "llama3:latest"]
    assert _pick_best_model(installed) == "llama3:latest"


def test_pick_best_model_prefers_real_tool_llama_over_vision():
    """If the user has BOTH llama3.2-vision and llama3.1, prefer
    llama3.1 even though llama3.2 appears first alphabetically —
    only llama3.1 is tool-capable here."""
    from orgchem.agent.llm.ollama_backend import _pick_best_model
    installed = ["llama3.2-vision:latest", "llama3.1:8b",
                 "llama3:latest"]
    assert _pick_best_model(installed) == "llama3.1:8b"


def test_chat_drops_tools_field_for_non_capable_model(monkeypatch):
    """When the selected model isn't tool-capable, the backend must
    NOT send the ``tools`` field — otherwise Ollama 500s with
    'does not support tools'."""
    from orgchem.agent.llm.ollama_backend import OllamaBackend
    from orgchem.agent.llm.base import ChatMessage
    from types import SimpleNamespace

    sent_bodies = []

    def fake_post(url, json=None, timeout=None, **_):
        sent_bodies.append(json)
        return SimpleNamespace(
            status_code=200,
            raise_for_status=lambda: None,
            json=lambda: {"message": {"content": "ok"}},
        )

    monkeypatch.setattr(
        "orgchem.agent.llm.ollama_backend.requests.post", fake_post)
    b = OllamaBackend(model="llama3:latest", auto_select=False)
    tools = [{"name": "demo", "description": "demo", "input_schema": {}}]
    b.chat([ChatMessage(role="user", text="hi")], tools=tools)
    assert sent_bodies, "chat() never called requests.post"
    assert "tools" not in sent_bodies[0], sent_bodies[0]


def test_chat_includes_tools_for_capable_model(monkeypatch):
    from orgchem.agent.llm.ollama_backend import OllamaBackend
    from orgchem.agent.llm.base import ChatMessage
    from types import SimpleNamespace

    sent_bodies = []

    def fake_post(url, json=None, timeout=None, **_):
        sent_bodies.append(json)
        return SimpleNamespace(
            status_code=200,
            raise_for_status=lambda: None,
            json=lambda: {"message": {"content": "ok"}},
        )

    monkeypatch.setattr(
        "orgchem.agent.llm.ollama_backend.requests.post", fake_post)
    b = OllamaBackend(model="llama3.1:8b", auto_select=False)
    tools = [{"name": "demo", "description": "demo", "input_schema": {}}]
    b.chat([ChatMessage(role="user", text="hi")], tools=tools)
    assert "tools" in sent_bodies[0], sent_bodies[0]


def test_chat_retries_without_tools_on_ollama_500(monkeypatch):
    """Edge case: our allowlist is stale and Ollama says 'does not
    support tools' on a model we thought was fine. The backend
    should transparently retry without tools on exactly that 500."""
    from orgchem.agent.llm.ollama_backend import OllamaBackend
    from orgchem.agent.llm.base import ChatMessage
    from types import SimpleNamespace

    calls = []

    def fake_post(url, json=None, timeout=None, **_):
        calls.append(dict(json))
        if "tools" in json:
            return SimpleNamespace(
                status_code=500,
                text=("registry.ollama.ai/library/llama3.1:8b "
                      "does not support tools"),
                raise_for_status=lambda: None,
                json=lambda: {},
            )
        return SimpleNamespace(
            status_code=200,
            raise_for_status=lambda: None,
            json=lambda: {"message": {"content": "fallback"}},
        )

    monkeypatch.setattr(
        "orgchem.agent.llm.ollama_backend.requests.post", fake_post)
    b = OllamaBackend(model="llama3.1:8b", auto_select=False)
    tools = [{"name": "demo", "description": "demo", "input_schema": {}}]
    msg = b.chat([ChatMessage(role="user", text="hi")], tools=tools)
    # First call included tools; second retry didn't.
    assert len(calls) == 2
    assert "tools" in calls[0]
    assert "tools" not in calls[1]
    assert msg.text == "fallback"
