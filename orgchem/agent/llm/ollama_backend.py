"""Ollama backend — local LLM inference via the Ollama HTTP server.

Default endpoint: ``http://localhost:11434``. Tool-use is supported by
Ollama for models that expose a ``tools`` field (llama3.1+, qwen2.5+, etc.).
"""
from __future__ import annotations
import json
from typing import Any, Dict, List

import requests

from orgchem.agent.llm.base import LLMBackend, ChatMessage, ToolCall
from orgchem.messaging.errors import NetworkError


class OllamaBackend(LLMBackend):
    name = "ollama"
    default_model = "llama3.1"

    def __init__(self, model: str = "", host: str = "http://localhost:11434", **cfg: Any):
        super().__init__(model=model, **cfg)
        self.host = host.rstrip("/")

    def chat(self, history: List[ChatMessage], tools: List[Dict[str, Any]],
             system: str = "") -> ChatMessage:
        body: Dict[str, Any] = {
            "model": self.model or self.default_model,
            "messages": _history_to_ollama(history, system),
            "stream": False,
        }
        if tools:
            body["tools"] = [_tool_to_ollama(t) for t in tools]

        try:
            r = requests.post(f"{self.host}/api/chat", json=body, timeout=180)
            r.raise_for_status()
        except requests.RequestException as e:
            raise NetworkError(f"Ollama request failed: {e}") from e

        payload = r.json()
        msg = payload.get("message", {}) or {}
        tool_calls: List[ToolCall] = []
        for i, tc in enumerate(msg.get("tool_calls") or []):
            fn = tc.get("function", {}) or {}
            args = fn.get("arguments") or {}
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except Exception:
                    args = {}
            tool_calls.append(ToolCall(
                name=fn.get("name", ""),
                id=f"ollama-{i}",
                arguments=args,
            ))
        return ChatMessage(role="assistant", text=msg.get("content", "") or "",
                           tool_calls=tool_calls)


def _history_to_ollama(history: List[ChatMessage], system: str) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    if system:
        out.append({"role": "system", "content": system})
    for m in history:
        if m.role == "user":
            out.append({"role": "user", "content": m.text})
            for tr in m.tool_results:
                out.append({"role": "tool", "content": json.dumps(tr.content, default=str)})
        elif m.role == "assistant":
            entry: Dict[str, Any] = {"role": "assistant", "content": m.text}
            if m.tool_calls:
                entry["tool_calls"] = [{
                    "function": {"name": tc.name, "arguments": tc.arguments},
                } for tc in m.tool_calls]
            out.append(entry)
    return out


def _tool_to_ollama(schema: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "type": "function",
        "function": {
            "name": schema["name"],
            "description": schema.get("description", ""),
            "parameters": schema.get("input_schema", {"type": "object", "properties": {}}),
        },
    }
