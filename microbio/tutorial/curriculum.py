"""Microbio Studio — curriculum tree.

Same shape as ``orgchem.tutorial.curriculum.CURRICULUM`` +
``cellbio.tutorial.curriculum.CURRICULUM`` so the audit + panel
patterns can be reused.

Phase MB-3.0 (round 227) expanded the curriculum from the MB-1.0
starter to 13 lessons across all four tiers covering microbial
diversity + identification, antibiotic mechanisms + resistance,
vaccines, virology, microbiome, emerging zoonotic infections,
mycology + parasitology, phage therapy, CRISPR, and AMR
epidemiology + stewardship.
"""
from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, List

_BASE = Path(__file__).parent / "content"


def _lesson(title: str, rel: str) -> Dict[str, Any]:
    return {"title": title, "path": _BASE / rel}


CURRICULUM: Dict[str, List[Dict[str, Any]]] = {
    "beginner": [
        _lesson("Welcome to Microbiology Studio",
                "beginner/01_welcome_microbio.md"),
        _lesson("What microbiology is",
                "beginner/02_what_microbiology_is.md"),
        _lesson("Bacterial cell architecture",
                "beginner/03_bacterial_cell_architecture.md"),
        _lesson("Microbial diversity",
                "beginner/04_microbial_diversity.md"),
        _lesson("How we identify microbes",
                "beginner/05_how_we_identify_microbes.md"),
    ],
    "intermediate": [
        _lesson("Antibiotic mechanisms + classes",
                "intermediate/01_antibiotic_mechanisms.md"),
        _lesson("Antibiotic resistance",
                "intermediate/02_antibiotic_resistance.md"),
        _lesson("Vaccines",
                "intermediate/03_vaccines.md"),
        _lesson("Virology essentials",
                "intermediate/04_virology_essentials.md"),
    ],
    "advanced": [
        _lesson("Microbiome + metagenomics",
                "advanced/01_microbiome_metagenomics.md"),
        _lesson("Emerging + zoonotic infections",
                "advanced/02_emerging_zoonotic_infections.md"),
        _lesson("Mycology + parasitology",
                "advanced/03_mycology_parasitology.md"),
    ],
    "graduate": [
        _lesson("Phage therapy + bacteriophage biology",
                "graduate/01_phage_therapy.md"),
        _lesson("CRISPR + microbial molecular biology",
                "graduate/02_crispr_microbial_biology.md"),
        _lesson("AMR epidemiology + stewardship",
                "graduate/03_amr_epidemiology_stewardship.md"),
    ],
}
