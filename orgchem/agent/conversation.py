"""Conversation orchestrator.

Wraps an :class:`LLMBackend` and the action registry into a tool-use loop:
user turn → model turn → (model asks for a tool) → invoke action → feed
result back into the model → repeat until the model produces a plain text
reply.

The tutor panel uses this; the stdio bridge and the headless test harness
reuse it so every driver benefits from the same orchestration.
"""
from __future__ import annotations
import logging
from dataclasses import field, dataclass
from typing import Any, Dict, Iterator, List, Optional

from orgchem.agent.actions import invoke, tool_schemas
from orgchem.agent.llm.base import LLMBackend, ChatMessage, ToolResult

log = logging.getLogger(__name__)

_SYSTEM_PROMPT = """\
You are an interactive organic-chemistry tutor embedded in a desktop app
called OrgChem Studio. You teach students from a complete beginner to a
graduate level. You have tools that let you:
  - search, display, and describe molecules from a local database
  - download new molecules from PubChem
  - open curriculum tutorials
  - compute empirical and molecular formulas
Use tools liberally — it is better to *show* a student the caffeine
structure than to describe it in words. Confirm the molecule you just
opened and invite the student's next question.
"""


@dataclass
class Conversation:
    backend: LLMBackend
    history: List[ChatMessage] = field(default_factory=list)
    system_prompt: str = _SYSTEM_PROMPT
    max_tool_rounds: int = 8

    def send(self, user_text: str) -> Iterator[ChatMessage]:
        """Advance the conversation one user turn. Yields assistant turns
        (including intermediate tool-result turns) as they are produced."""
        self.history.append(ChatMessage(role="user", text=user_text))
        for _ in range(self.max_tool_rounds):
            tools = tool_schemas()
            assistant = self.backend.chat(self.history, tools=tools, system=self.system_prompt)
            self.history.append(assistant)
            yield assistant
            if not assistant.tool_calls:
                return

            tool_results: List[ToolResult] = []
            for tc in assistant.tool_calls:
                try:
                    result = invoke(tc.name, **(tc.arguments or {}))
                    tool_results.append(ToolResult(tool_use_id=tc.id, content=result))
                except Exception as e:
                    log.exception("Tool %s failed", tc.name)
                    tool_results.append(ToolResult(
                        tool_use_id=tc.id,
                        content={"error": f"{type(e).__name__}: {e}"},
                        is_error=True,
                    ))
            self.history.append(ChatMessage(role="user", tool_results=tool_results))
        log.warning("Conversation hit max_tool_rounds=%d", self.max_tool_rounds)
