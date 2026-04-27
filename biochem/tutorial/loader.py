"""Biochem Studio — tutorial markdown loader."""
from __future__ import annotations
from pathlib import Path
from typing import Union


def load_lesson(path: Union[str, Path]) -> str:
    return Path(path).read_text(encoding="utf-8")
