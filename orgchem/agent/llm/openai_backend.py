"""OpenAI-compatible backend (also works with Azure OpenAI, DeepSeek, Groq, …
anything that speaks the OpenAI chat-completions schema)."""
from __future__ import annotations
import json
import os
from typing import Any, Dict, List

from orgchem.agent.llm.base import LLMBackend, ChatMessage, ToolCall
from orgchem.messaging.errors import NetworkError


class OpenAIBackend(LLMBackend):
    name = "openai"
    default_model = "gpt-4o-mini"

    def __init__(self, model: str = "", api_key_env: str = "OPENAI_API_KEY",
                 base_url: str = "", **cfg: Any):
        super().__init__(model=model, **cfg)
        self._api_key_env = api_key_env
        self._base_url = base_url

    def _client(self):
        try:
            import openai
        except ImportError as e:
            raise NetworkError("openai SDK not installed — pip install openai") from e
        key = os.environ.get(self._api_key_env)
        if not key:
            raise NetworkError(f"Set {self._api_key_env} to use the OpenAI backend")
        kw: Dict[str, Any] = {"api_key": key}
        if self._base_url:
            kw["base_url"] = self._base_url
        return openai.OpenAI(**kw)

    def chat(self, history: List[ChatMessage], tools: List[Dict[str, Any]],
             system: str = "") -> ChatMessage:
        client = self._client()
        msgs = _history_to_openai(history, system)
        oai_tools = [_tool_to_openai(t) for t in (tools or [])]
        resp = client.chat.completions.create(
            model=self.model or self.default_model,
            messages=msgs,
            tools=oai_tools or None,
        )
        choice = resp.choices[0].message
        tool_calls: List[ToolCall] = []
        for tc in (choice.tool_calls or []):
            try:
                args = json.loads(tc.function.arguments or "{}")
            except Exception:
                args = {}
            tool_calls.append(ToolCall(name=tc.function.name, id=tc.id, arguments=args))
        return ChatMessage(role="assistant", text=choice.content or "", tool_calls=tool_calls)


def _history_to_openai(history: List[ChatMessage], system: str) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    if system:
        out.append({"role": "system", "content": system})
    for m in history:
        if m.role == "user":
            out.append({"role": "user", "content": m.text})
            for tr in m.tool_results:
                out.append({
                    "role": "tool", "tool_call_id": tr.tool_use_id,
                    "content": json.dumps(tr.content, default=str),
                })
        elif m.role == "assistant":
            entry: Dict[str, Any] = {"role": "assistant", "content": m.text}
            if m.tool_calls:
                entry["tool_calls"] = [{
                    "id": tc.id, "type": "function",
                    "function": {"name": tc.name, "arguments": json.dumps(tc.arguments)},
                } for tc in m.tool_calls]
            out.append(entry)
    return out


def _tool_to_openai(schema: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "type": "function",
        "function": {
            "name": schema["name"],
            "description": schema.get("description", ""),
            "parameters": schema.get("input_schema", {"type": "object", "properties": {}}),
        },
    }
