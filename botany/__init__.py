"""Botany Studio — sibling package #5 in the multi-studio life-
sciences platform.

**Phase BT-1.0** — fifth sibling (after Cell Bio CB-1.0, Biochem
BC-1.0, Pharmacology PH-1.0, Microbiology MB-1.0).  Catalogues
plant taxa across the major divisions (bryophytes, lycophytes,
ferns, gymnosperms, angiosperm-monocots, angiosperm-eudicots)
+ their secondary-metabolite cross-references into the OrgChem
molecule DB + their photosynthetic / metabolic-pathway cross-
references.

Importing ``botany`` triggers registration of botany's agent
actions into the shared ``orgchem.agent.actions._REGISTRY``.
"""
from __future__ import annotations

from botany.agent import actions_taxa  # noqa: F401
# Phase BT-2.0 (round 222) — additive plant-hormones catalogue.
from botany.agent import actions_plant_hormones  # noqa: F401
