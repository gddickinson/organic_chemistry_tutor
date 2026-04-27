"""Biochem Studio — curriculum tree.

Same shape as ``orgchem.tutorial.curriculum.CURRICULUM`` +
``cellbio.tutorial.curriculum.CURRICULUM`` so the audit + panel
patterns can be reused.

Phase BC-3.0 (round 225) expanded the curriculum from the BC-1.0
starter to 14 lessons across all four tiers covering amino acids,
proteins, enzymes, kinetics, allostery, central metabolism,
oxidative phosphorylation, signalling enzymes, drug metabolism,
computational enzymology, enzyme engineering, and metabolomics.
"""
from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, List

_BASE = Path(__file__).parent / "content"


def _lesson(title: str, rel: str) -> Dict[str, Any]:
    return {"title": title, "path": _BASE / rel}


CURRICULUM: Dict[str, List[Dict[str, Any]]] = {
    "beginner": [
        _lesson("Welcome to Biochemistry Studio",
                "beginner/01_welcome_biochem.md"),
        _lesson("What biochemistry is",
                "beginner/02_what_biochemistry_is.md"),
        _lesson("Amino acids + proteins",
                "beginner/03_amino_acids_and_proteins.md"),
        _lesson("Enzymes — basics",
                "beginner/04_enzymes_basics.md"),
        _lesson("Cofactors overview",
                "beginner/05_cofactors_overview.md"),
    ],
    "intermediate": [
        _lesson("Enzyme kinetics — Michaelis-Menten",
                "intermediate/01_enzyme_kinetics.md"),
        _lesson("Enzyme inhibition",
                "intermediate/02_enzyme_inhibition.md"),
        _lesson("Allostery + cooperativity",
                "intermediate/03_allostery.md"),
        _lesson("Glycolysis + the TCA cycle",
                "intermediate/04_glycolysis_tca.md"),
    ],
    "advanced": [
        _lesson("Oxidative phosphorylation + chemiosmosis",
                "advanced/01_oxidative_phosphorylation.md"),
        _lesson("Signalling-related enzymes",
                "advanced/02_signalling_related_enzymes.md"),
        _lesson("Drug metabolism enzymology",
                "advanced/03_drug_metabolism_enzymology.md"),
    ],
    "graduate": [
        _lesson("Computational enzymology",
                "graduate/01_computational_enzymology.md"),
        _lesson("Enzyme engineering + directed evolution",
                "graduate/02_enzyme_engineering.md"),
        _lesson("Metabolomics + flux analysis",
                "graduate/03_metabolomics_flux.md"),
    ],
}
