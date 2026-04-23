"""Tutorial markdown loader."""
from __future__ import annotations
from pathlib import Path


def load_tutorial_markdown(path) -> str:
    p = Path(path)
    if not p.exists():
        return (
            f"# Content pending\n\n"
            f"This lesson has not been written yet.\n\n"
            f"Expected file: `{p}`\n\n"
            f"To contribute, add the markdown to `orgchem/tutorial/content/` "
            f"and update the curriculum if needed."
        )
    return p.read_text()
