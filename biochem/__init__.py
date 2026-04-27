"""Biochemistry Studio — sibling package to ``orgchem`` and
``cellbio``.

**Phase BC-1.0** — second sibling in the multi-studio life-
sciences platform.  Biochem Studio shares OrgChem's process,
agent registry, SQLite DB, and global glossary.  Distinctive
v0.1 catalogue: enzymes by EC class.  Distinctive v0.1
architectural validation: a **bridge panel** that surfaces
``orgchem.core.metabolic_pathways`` read-only — proving that
sibling studios can share data without forcing a refactor.

Importing ``biochem`` triggers registration of biochem's agent
actions into the shared registry — same pattern as ``cellbio``.
"""
from __future__ import annotations

from biochem.agent import actions_enzymes  # noqa: F401
# Phase BC-2.0 (round 219) — additive cofactors / coenzymes catalogue.
from biochem.agent import actions_cofactors  # noqa: F401
