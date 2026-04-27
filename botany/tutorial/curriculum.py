"""Botany Studio — curriculum tree (Phase BT-1.0)."""
from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, List

_BASE = Path(__file__).parent / "content"


def _lesson(title: str, rel: str) -> Dict[str, Any]:
    return {"title": title, "path": _BASE / rel}


CURRICULUM: Dict[str, List[Dict[str, Any]]] = {
    "beginner": [
        _lesson("Welcome to Botany Studio",
                "beginner/01_welcome_botany.md"),
    ],
    "intermediate": [],
    "advanced": [],
    "graduate": [],
}
