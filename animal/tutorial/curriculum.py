"""Animal Biology Studio — curriculum tree (Phase AB-1.0)."""
from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, List

_BASE = Path(__file__).parent / "content"


def _lesson(title: str, rel: str) -> Dict[str, Any]:
    return {"title": title, "path": _BASE / rel}


CURRICULUM: Dict[str, List[Dict[str, Any]]] = {
    "beginner": [
        _lesson("Welcome to Animal Biology Studio",
                "beginner/01_welcome_animal.md"),
        _lesson("Platform retrospective — the 6-studio "
                "build chain",
                "beginner/02_platform_retrospective.md"),
    ],
    "intermediate": [],
    "advanced": [],
    "graduate": [],
}
