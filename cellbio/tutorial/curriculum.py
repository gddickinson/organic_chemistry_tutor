"""Cell Bio Studio — curriculum tree.

Phase CB-1.0 (round 212) shipped a single Welcome lesson.
Phase CB-3.0 (round 224) expanded the curriculum to 13
lessons spanning all 4 tiers (5 beginner / 4 intermediate
/ 3 advanced / 3 graduate).
Phase CB-4.0 (round 232) added 12 more lessons (3 per tier)
for a total of 25 — round 2 of the new -4 tutorial-
expansion chain.

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
        _lesson("Organelles deep-dive",
                "beginner/06_organelles_deep_dive.md"),
        _lesson("Cytoskeleton + motility (intro)",
                "beginner/07_cytoskeleton_intro.md"),
        _lesson("Membrane lipids + rafts",
                "beginner/08_membrane_lipids_rafts.md"),
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
        _lesson("Autophagy + ubiquitin-proteasome system",
                "intermediate/05_autophagy_ups.md"),
        _lesson("Cell-cell adhesion + extracellular matrix",
                "intermediate/06_cell_adhesion_ecm.md"),
        _lesson("Ion channels + electrical signalling",
                "intermediate/07_ion_channels_electrical.md"),
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
        _lesson("Calcium signalling",
                "advanced/04_calcium_signalling.md"),
        _lesson("Cell migration + cancer invasion",
                "advanced/05_cell_migration_cancer_invasion.md"),
        _lesson("Lysosomal degradation + lysosomal storage "
                "diseases",
                "advanced/06_lysosomal_storage_diseases.md"),
    ],
    "graduate": [
        _lesson("Quantitative signalling — kinetics, "
                "dynamics, and the modern frontier",
                "graduate/01_quantitative_signalling.md"),
        _lesson("Cytoskeleton + cell motility",
                "graduate/02_cytoskeleton_and_motility.md"),
        _lesson("Membrane trafficking + secretion",
                "graduate/03_membrane_trafficking.md"),
        _lesson("Organelle contact sites",
                "graduate/04_organelle_contact_sites.md"),
        _lesson("Oxidative stress + redox signalling",
                "graduate/05_oxidative_stress_redox_signalling.md"),
        _lesson("Intracellular pH + organelle pH",
                "graduate/06_intracellular_ph.md"),
    ],
}
