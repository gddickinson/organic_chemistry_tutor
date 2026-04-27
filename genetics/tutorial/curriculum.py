"""Genetics + Molecular Biology Studio — curriculum tree.

Same shape as ``orgchem.tutorial.curriculum.CURRICULUM`` +
sibling-studio curricula so the audit + panel patterns can
be reused.

Phase GM-3.0 (round 231) expanded the curriculum from the
GM-1.0 starter to 14 lessons across all four tiers covering
the foundations of molecular biology, DNA / RNA chemistry,
Mendelian + classical genetics, sequence-data formats,
PCR / qPCR / diagnostics, NGS workflows, CRISPR
experimental design, cloning + synthbio, Mendelian +
polygenic disease, cancer genomics, single-cell + spatial
omics, population genetics + ancient DNA, comparative +
functional genomics, and AI for genomics.
"""
from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, List

_BASE = Path(__file__).parent / "content"


def _lesson(title: str, rel: str) -> Dict[str, Any]:
    return {"title": title, "path": _BASE / rel}


CURRICULUM: Dict[str, List[Dict[str, Any]]] = {
    "beginner": [
        _lesson("Welcome to Genetics + Molecular Biology "
                "Studio",
                "beginner/01_welcome_genetics.md"),
        _lesson("What molecular biology is",
                "beginner/02_what_molecular_biology_is.md"),
        _lesson("DNA + RNA chemistry basics",
                "beginner/03_dna_rna_chemistry.md"),
        _lesson("Mendelian genetics + classical chromosomes",
                "beginner/04_mendelian_genetics.md"),
        _lesson("Reading sequence data",
                "beginner/05_reading_sequence_data.md"),
    ],
    "intermediate": [
        _lesson("PCR + qPCR + diagnostics — practical "
                "considerations",
                "intermediate/01_pcr_qpcr_diagnostics.md"),
        _lesson("NGS workflow + bioinformatics",
                "intermediate/02_ngs_workflow.md"),
        _lesson("CRISPR experimental design",
                "intermediate/03_crispr_experimental_design.md"),
        _lesson("Cloning + synthetic biology basics",
                "intermediate/04_cloning_synthbio.md"),
    ],
    "advanced": [
        _lesson("Mendelian + polygenic disease genetics",
                "advanced/01_disease_genetics.md"),
        _lesson("Cancer genomics",
                "advanced/02_cancer_genomics.md"),
        _lesson("Single-cell + spatial omics workflows",
                "advanced/03_single_cell_spatial_workflows.md"),
    ],
    "graduate": [
        _lesson("Population genetics + ancient DNA",
                "graduate/01_popgen_ancient_dna.md"),
        _lesson("Comparative + functional genomics",
                "graduate/02_comparative_functional_genomics.md"),
        _lesson("AI for genomics",
                "graduate/03_ai_for_genomics.md"),
    ],
}
