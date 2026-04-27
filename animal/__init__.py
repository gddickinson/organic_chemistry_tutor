"""Animal Biology Studio — sibling package #6 in the multi-studio
life-sciences platform.  **The final sibling — completes the
6-studio platform.**

**Phase AB-1.0** — sixth + final sibling (after Cell Bio CB-1.0,
Biochem BC-1.0, Pharmacology PH-1.0, Microbiology MB-1.0,
Botany BT-1.0).  Catalogues animal taxa across the major phyla
(porifera → chordata, plus model organisms — *D. melanogaster*,
*C. elegans*, mouse, zebrafish, *Xenopus*, sea urchin, …) +
their cellular-signalling + enzyme cross-references.

Importing ``animal`` triggers registration of animal's agent
actions into the shared ``orgchem.agent.actions._REGISTRY``.
"""
from __future__ import annotations

from animal.agent import actions_taxa  # noqa: F401
# Phase AB-2.0 (round 223) — additive organ-systems catalogue
# — FINAL deep-phase round, closes the -2 chain.
from animal.agent import actions_organ_systems  # noqa: F401
