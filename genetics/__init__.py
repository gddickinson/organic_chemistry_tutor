"""Genetics + Molecular Biology Studio — sibling package #7
in the multi-studio life-sciences platform.

**Phase GM-1.0** (round 230) — first round of the new
-1-extension phase, post -3 tutorial-expansion chain.  The
seventh sibling alongside ``orgchem/``, ``cellbio/``,
``biochem/``, ``pharm/``, ``microbio/``, ``botany/``, and
``animal/``.

Catalogues molecular-biology TECHNIQUES — the practical
toolkit underpinning all of biology research + diagnostics
+ industry: PCR family, sequencing (Sanger + NGS), cloning,
CRISPR, blots, in-situ hybridisation, chromatin profiling,
transcriptomics (bulk + single-cell + spatial), proteomics,
interactions, structural / 3D-genome, epigenetics, genome-
editing delivery.

Cross-references reach into:
- ``biochem.core.enzymes`` — DNA + RNA polymerases, ligases,
  restriction enzymes, reverse transcriptases (the molecular
  workhorses of every technique).
- ``cellbio.core.cell_cycle`` + ``cellbio.core.cell_signaling``
  — chromatin / DDR / apoptosis context for ChIP-seq +
  CRISPR + replication-related techniques.
- ``animal.core.taxa`` — model organisms used to develop +
  validate techniques (worm + fly + zebrafish + mouse).
- ``orgchem.db.Molecule`` — nucleotides + nucleic acids +
  intercalators + dyes (the chemical reagents).

Importing ``genetics`` triggers registration of the genetics
agent actions into the shared ``orgchem.agent.actions._
REGISTRY``.
"""
from __future__ import annotations

from genetics.agent import actions_techniques  # noqa: F401
