"""Cell Bio Studio — curriculum tree.

Phase CB-1.0 (round 212) shipped a single Welcome lesson.
Phase CB-3.0 (round 224) expanded the curriculum to 13
lessons spanning all 4 tiers (5 beginner / 4 intermediate
/ 3 advanced / 3 graduate).

Same shape as ``orgchem.tutorial.curriculum.CURRICULUM`` so
the tutorial-panel widget pattern + tutorial-coverage audit
can be reused.
"""
from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, List

_BASE = Path(__file__).parent / "content"


def _lesson(title: str, rel: str) -> Dict[str, Any]:
    return {"title": title, "path": _BASE / rel}


CURRICULUM: Dict[str, List[Dict[str, Any]]] = {
    "beginner": [
        _lesson("Welcome to Cell Biology Studio",
                "beginner/01_welcome_cellbio.md"),
        _lesson("What is a cell?",
                "beginner/02_what_is_a_cell.md"),
        _lesson("Cell signalling — the basics",
                "beginner/03_cell_signalling_basics.md"),
        _lesson("Receptors and ligands",
                "beginner/04_receptors_and_ligands.md"),
        _lesson("Second messengers — cAMP, IP3, Ca2+",
                "beginner/05_second_messengers.md"),
    ],
    "intermediate": [
        _lesson("MAPK / ERK — the prototype kinase cascade",
                "intermediate/01_mapk_erk_cascade.md"),
        _lesson("GPCR signalling deep-dive",
                "intermediate/02_gpcr_signalling.md"),
        _lesson("Receptor tyrosine kinases + JAK-STAT",
                "intermediate/03_rtks_and_jak_stat.md"),
        _lesson("Apoptosis + cell-death pathways",
                "intermediate/04_apoptosis_pathways.md"),
    ],
    "advanced": [
        _lesson("Wnt / beta-catenin — from embryo to colon "
                "cancer",
                "advanced/01_wnt_in_dev_and_cancer.md"),
        _lesson("DNA damage response + cell-cycle "
                "checkpoints",
                "advanced/02_dna_damage_response.md"),
        _lesson("Cancer signalling networks — putting it "
                "together",
                "advanced/03_cancer_signalling_networks.md"),
    ],
    "graduate": [
        _lesson("Quantitative signalling — kinetics, "
                "dynamics, and the modern frontier",
                "graduate/01_quantitative_signalling.md"),
        _lesson("Cytoskeleton + cell motility",
                "graduate/02_cytoskeleton_and_motility.md"),
        _lesson("Membrane trafficking + secretion",
                "graduate/03_membrane_trafficking.md"),
    ],
}
