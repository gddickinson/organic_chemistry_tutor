"""Microbiology Studio — sibling package #4 in the multi-studio
life-sciences platform.

**Phase MB-1.0** — fourth sibling (after Cell Bio CB-1.0,
Biochem BC-1.0, Pharmacology PH-1.0).  Catalogues bacterial,
archaeal, fungal, viral, and protist pathogens + their cell-
biology / drug-treatment / enzyme cross-references.

Importing ``microbio`` triggers registration of microbio's agent
actions into the shared ``orgchem.agent.actions._REGISTRY``.
"""
from __future__ import annotations

from microbio.agent import actions_microbes  # noqa: F401
# Phase MB-2.0 (round 221) — additive virulence-factors catalogue.
from microbio.agent import actions_virulence  # noqa: F401
