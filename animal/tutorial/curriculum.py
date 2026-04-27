"""Animal Biology Studio — curriculum tree.

Same shape as ``orgchem.tutorial.curriculum.CURRICULUM`` +
sibling-studio curricula so the audit + panel patterns
can be reused.

Phase AB-3.0 (round 229) expanded the curriculum from the
AB-1.0 starter (welcome + platform retrospective) to 14
lessons across all four tiers covering animal scope, body
plans, tissue + organ systems, development, comparative
physiology, neuroscience, endocrinology, immunology,
phylogenetics, behaviour + ethology, conservation biology,
comparative genomics, neuroscience frontiers, and animal
biotech + One Health.

This is the closing round of the **-3 tutorial-expansion
chain** (rounds 224-229, CB-3.0 → AB-3.0).  See
SESSION_LOG.md for the chain retrospective.
"""
from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, List

_BASE = Path(__file__).parent / "content"


def _lesson(title: str, rel: str) -> Dict[str, Any]:
    return {"title": title, "path": _BASE / rel}


CURRICULUM: Dict[str, List[Dict[str, Any]]] = {
    "beginner": [
        _lesson("Welcome to Animal Biology Studio",
                "beginner/01_welcome_animal.md"),
        _lesson("Platform retrospective — the 6-studio "
                "build chain",
                "beginner/02_platform_retrospective.md"),
        _lesson("What animal biology is",
                "beginner/03_what_animal_biology_is.md"),
        _lesson("Animal body plans",
                "beginner/04_animal_body_plans.md"),
        _lesson("Tissue + organ systems overview",
                "beginner/05_tissue_and_organ_systems_overview.md"),
        _lesson("How animals develop",
                "beginner/06_how_animals_develop.md"),
    ],
    "intermediate": [
        _lesson("Comparative animal physiology",
                "intermediate/01_comparative_animal_physiology.md"),
        _lesson("Nervous systems + neuroscience essentials",
                "intermediate/02_nervous_systems_neuroscience.md"),
        _lesson("Animal endocrinology + hormones",
                "intermediate/03_animal_endocrinology.md"),
        _lesson("Animal immunology essentials",
                "intermediate/04_animal_immunology.md"),
    ],
    "advanced": [
        _lesson("Animal evolution + phylogenetics",
                "advanced/01_animal_evolution_phylogenetics.md"),
        _lesson("Behaviour + ethology",
                "advanced/02_behaviour_and_ethology.md"),
        _lesson("Conservation biology + biodiversity loss",
                "advanced/03_conservation_biology.md"),
    ],
    "graduate": [
        _lesson("Comparative genomics + animal evolution",
                "graduate/01_comparative_genomics.md"),
        _lesson("Neuroscience frontiers",
                "graduate/02_neuroscience_frontiers.md"),
        _lesson("Modern animal biotech + One Health",
                "graduate/03_animal_biotech_one_health.md"),
    ],
}
