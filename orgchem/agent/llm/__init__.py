"""Pluggable LLM backends for the in-app chat console.

Every backend implements :class:`LLMBackend` and is chosen at runtime from
config. The chat console (``gui/panels/tutor_panel.py``) calls the backend
and feeds tool-use blocks through the action registry.
"""
from orgchem.agent.llm.base import LLMBackend, ChatMessage, ToolCall, ToolResult, available_backends

__all__ = ["LLMBackend", "ChatMessage", "ToolCall", "ToolResult", "available_backends"]
