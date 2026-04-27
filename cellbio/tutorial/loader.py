"""Cell Bio Studio — tutorial markdown loader."""
from __future__ import annotations
from pathlib import Path
from typing import Union


def load_lesson(path: Union[str, Path]) -> str:
    """Read a tutorial markdown file from disk + return its
    contents as text."""
    p = Path(path)
    return p.read_text(encoding="utf-8")
