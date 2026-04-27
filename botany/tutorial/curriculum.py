"""Botany Studio — curriculum tree.

Same shape as ``orgchem.tutorial.curriculum.CURRICULUM`` +
``cellbio.tutorial.curriculum.CURRICULUM`` so the audit + panel
patterns can be reused.

Phase BT-3.0 (round 228) expanded the curriculum from the BT-1.0
starter to 13 lessons across all four tiers covering plant cell
architecture, tissues + organs, life cycles, photosynthesis,
water + nutrient transport, phytohormones, plant defence,
evolution of land plants, biotechnology + crop improvement,
secondary metabolism, climate-change biology, single-cell +
spatial transcriptomics, and synthetic biology + engineering.
"""
from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, List

_BASE = Path(__file__).parent / "content"


def _lesson(title: str, rel: str) -> Dict[str, Any]:
    return {"title": title, "path": _BASE / rel}


CURRICULUM: Dict[str, List[Dict[str, Any]]] = {
    "beginner": [
        _lesson("Welcome to Botany Studio",
                "beginner/01_welcome_botany.md"),
        _lesson("What botany is",
                "beginner/02_what_botany_is.md"),
        _lesson("Plant cell architecture",
                "beginner/03_plant_cell_architecture.md"),
        _lesson("Plant tissues + organs",
                "beginner/04_plant_tissues_and_organs.md"),
        _lesson("Plant life cycles + reproduction",
                "beginner/05_life_cycles_and_reproduction.md"),
    ],
    "intermediate": [
        _lesson("Photosynthesis",
                "intermediate/01_photosynthesis.md"),
        _lesson("Plant water + nutrient transport",
                "intermediate/02_water_and_nutrient_transport.md"),
        _lesson("Phytohormones in depth",
                "intermediate/03_phytohormones_in_depth.md"),
        _lesson("Plant defence",
                "intermediate/04_plant_defence.md"),
    ],
    "advanced": [
        _lesson("Evolution of land plants",
                "advanced/01_evolution_of_land_plants.md"),
        _lesson("Plant biotechnology + crop improvement",
                "advanced/02_plant_biotechnology.md"),
        _lesson("Plant secondary metabolism",
                "advanced/03_plant_secondary_metabolism.md"),
    ],
    "graduate": [
        _lesson("Plant climate-change biology",
                "graduate/01_plant_climate_change_biology.md"),
        _lesson("Plant single-cell + spatial transcriptomics",
                "graduate/02_plant_single_cell_spatial.md"),
        _lesson("Synthetic biology + plant engineering",
                "graduate/03_synthetic_biology_plant_engineering.md"),
    ],
}
