"""Pharmacology Studio — sibling package #3 in the multi-studio
life-sciences platform.

**Phase PH-1.0** — third sibling (after Cell Bio CB-1.0 + Biochem
BC-1.0).  Shares OrgChem's process, agent registry, SQLite DB,
and global glossary.  Distinctive v0.1 catalogue: drug classes
keyed by molecular target.  Distinctive v0.1 architectural
validation: **two bridge panels** that surface
``biochem.core.enzymes`` (drug-target enzymes) and
``cellbio.core.cell_signaling`` (drug-target receptor pathways)
read-only — proving the cross-studio data-sharing pattern works
multi-hop, not just from a single sibling.

Importing ``pharm`` triggers registration of pharm's agent
actions into the shared registry — same pattern as
``cellbio`` + ``biochem``.
"""
from __future__ import annotations

from pharm.agent import actions_drug_classes  # noqa: F401
# Phase PH-2.0 (round 220) — additive receptor pharmacology catalogue.
from pharm.agent import actions_receptors  # noqa: F401
