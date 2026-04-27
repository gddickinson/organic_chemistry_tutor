"""Pharm Studio — curriculum tree.

Same shape as ``orgchem.tutorial.curriculum.CURRICULUM`` +
``cellbio.tutorial.curriculum.CURRICULUM`` so the audit + panel
patterns can be reused.

Phase PH-3.0 (round 226) expanded the curriculum from the PH-1.0
starter to 13 lessons across all four tiers covering pharmacology
fundamentals, PK + PD, dose-response, DDIs, drug development,
biologics, pharmacogenomics, computational drug discovery,
real-world evidence, and modern modalities.
"""
from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, List

_BASE = Path(__file__).parent / "content"


def _lesson(title: str, rel: str) -> Dict[str, Any]:
    return {"title": title, "path": _BASE / rel}


CURRICULUM: Dict[str, List[Dict[str, Any]]] = {
    "beginner": [
        _lesson("Welcome to Pharmacology Studio",
                "beginner/01_welcome_pharm.md"),
        _lesson("What pharmacology is",
                "beginner/02_what_pharmacology_is.md"),
        _lesson("Drug names + classes",
                "beginner/03_drug_names_and_classes.md"),
        _lesson("Routes of administration",
                "beginner/04_routes_of_administration.md"),
        _lesson("Drug-receptor basics",
                "beginner/05_drug_receptor_basics.md"),
    ],
    "intermediate": [
        _lesson("Pharmacokinetics",
                "intermediate/01_pharmacokinetics.md"),
        _lesson("Pharmacodynamics",
                "intermediate/02_pharmacodynamics.md"),
        _lesson("Dose-response in practice",
                "intermediate/03_dose_response_in_practice.md"),
        _lesson("Drug-drug interactions",
                "intermediate/04_drug_drug_interactions.md"),
    ],
    "advanced": [
        _lesson("Drug development pipeline",
                "advanced/01_drug_development_pipeline.md"),
        _lesson("Biologics",
                "advanced/02_biologics.md"),
        _lesson("Pharmacogenomics",
                "advanced/03_pharmacogenomics.md"),
    ],
    "graduate": [
        _lesson("Computational drug discovery",
                "graduate/01_computational_drug_discovery.md"),
        _lesson("Real-world evidence + RCTs",
                "graduate/02_real_world_evidence_and_rcts.md"),
        _lesson("Modern modalities",
                "graduate/03_modern_modalities.md"),
    ],
}
