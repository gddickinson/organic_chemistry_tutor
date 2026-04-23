"""Abstract LLM backend interface."""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List


@dataclass
class ToolCall:
    name: str
    id: str
    arguments: Dict[str, Any]


@dataclass
class ToolResult:
    tool_use_id: str
    content: Any
    is_error: bool = False


@dataclass
class ChatMessage:
    role: str                        # "user" | "assistant" | "system" | "tool"
    text: str = ""
    tool_calls: List[ToolCall] = field(default_factory=list)
    tool_results: List[ToolResult] = field(default_factory=list)


class LLMBackend(ABC):
    """Minimum interface every backend must implement."""

    name: str = "abstract"
    default_model: str = ""

    def __init__(self, model: str = "", **cfg: Any):
        self.model = model or self.default_model
        self.cfg = cfg

    @abstractmethod
    def chat(self, history: List[ChatMessage], tools: List[Dict[str, Any]],
             system: str = "") -> ChatMessage:
        """Synchronous chat completion.

        *history* is the full conversation so far (user + assistant + any
        tool_result blocks). *tools* is the list of JSON schemas from
        :func:`orgchem.agent.actions.tool_schemas`. Returns the next
        assistant message, which may contain tool-use blocks.
        """


def available_backends() -> Dict[str, type]:
    """Return the registry of known backend classes, discovered lazily."""
    from orgchem.agent.llm.anthropic_backend import AnthropicBackend
    from orgchem.agent.llm.openai_backend import OpenAIBackend
    from orgchem.agent.llm.ollama_backend import OllamaBackend
    return {
        "anthropic": AnthropicBackend,
        "openai":    OpenAIBackend,
        "ollama":    OllamaBackend,
    }
