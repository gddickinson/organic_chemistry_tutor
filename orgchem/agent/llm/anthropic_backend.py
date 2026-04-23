"""Anthropic Claude backend (uses the ``anthropic`` Python SDK)."""
from __future__ import annotations
import json
import os
from typing import Any, Dict, List

from orgchem.agent.llm.base import LLMBackend, ChatMessage, ToolCall
from orgchem.messaging.errors import NetworkError


class AnthropicBackend(LLMBackend):
    name = "anthropic"
    default_model = "claude-opus-4-7"

    def __init__(self, model: str = "", api_key_env: str = "ANTHROPIC_API_KEY", **cfg: Any):
        super().__init__(model=model, **cfg)
        self._api_key_env = api_key_env

    def _client(self):
        try:
            import anthropic
        except ImportError as e:
            raise NetworkError("anthropic SDK not installed — pip install anthropic") from e
        key = os.environ.get(self._api_key_env)
        if not key:
            raise NetworkError(f"Set {self._api_key_env} to use the Anthropic backend")
        return anthropic.Anthropic(api_key=key)

    def chat(self, history: List[ChatMessage], tools: List[Dict[str, Any]],
             system: str = "") -> ChatMessage:
        client = self._client()
        msgs = _history_to_anthropic(history)
        resp = client.messages.create(
            model=self.model or self.default_model,
            max_tokens=4096,
            system=system or "You are an organic chemistry tutor.",
            messages=msgs,
            tools=tools or [],
        )
        return _response_to_message(resp)


def _history_to_anthropic(history: List[ChatMessage]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for m in history:
        if m.role == "user":
            blocks: List[Dict[str, Any]] = []
            if m.text:
                blocks.append({"type": "text", "text": m.text})
            for tr in m.tool_results:
                blocks.append({
                    "type": "tool_result",
                    "tool_use_id": tr.tool_use_id,
                    "content": json.dumps(tr.content, default=str),
                    "is_error": tr.is_error,
                })
            out.append({"role": "user", "content": blocks or m.text})
        elif m.role == "assistant":
            blocks = []
            if m.text:
                blocks.append({"type": "text", "text": m.text})
            for tc in m.tool_calls:
                blocks.append({
                    "type": "tool_use", "id": tc.id,
                    "name": tc.name, "input": tc.arguments,
                })
            out.append({"role": "assistant", "content": blocks})
    return out


def _response_to_message(resp) -> ChatMessage:
    text_parts: List[str] = []
    tool_calls: List[ToolCall] = []
    for block in resp.content:
        btype = getattr(block, "type", None)
        if btype == "text":
            text_parts.append(block.text)
        elif btype == "tool_use":
            tool_calls.append(ToolCall(
                name=block.name, id=block.id, arguments=block.input or {}
            ))
    return ChatMessage(role="assistant", text="\n".join(text_parts), tool_calls=tool_calls)
