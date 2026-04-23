"""Curriculum tree — lessons grouped by level.

Each lesson is a ``dict`` with ``title`` and ``path`` (absolute path to a
markdown file under ``content/``). The tutorial panel reads this directly;
the agent exposes ``list_tutorials`` / ``open_tutorial`` actions against it.
"""
from __future__ import annotations
from pathlib import Path
from typing import Dict, List, Any

_BASE = Path(__file__).parent / "content"


def _lesson(title: str, rel: str) -> Dict[str, Any]:
    return {"title": title, "path": _BASE / rel}


CURRICULUM: Dict[str, List[Dict[str, Any]]] = {
    "beginner": [
        _lesson("Welcome to organic chemistry",           "beginner/01_welcome.md"),
        _lesson("Atoms, bonds, hybridisation",            "beginner/02_atoms_bonds.md"),
        _lesson("Lewis & skeletal structures",            "beginner/03_structures.md"),
        _lesson("Functional groups overview",             "beginner/04_functional_groups.md"),
        _lesson("IUPAC nomenclature (introduction)",      "beginner/05_nomenclature.md"),
    ],
    "intermediate": [
        _lesson("Stereochemistry (R/S, E/Z, chirality)",  "intermediate/01_stereochemistry.md"),
        _lesson("Substitution (SN1 / SN2)",               "intermediate/02_substitution.md"),
        _lesson("Elimination (E1 / E2)",                  "intermediate/03_elimination.md"),
        _lesson("Aromaticity and electrophilic aromatic substitution", "intermediate/04_aromaticity.md"),
        _lesson("Carbonyl chemistry",                     "intermediate/05_carbonyl.md"),
        _lesson("Reaction energetics (profiles + kinetics)", "intermediate/06_energetics.md"),
    ],
    "advanced": [
        _lesson("Pericyclic reactions",                   "advanced/01_pericyclic.md"),
        _lesson("Organometallic chemistry",               "advanced/02_organometallics.md"),
        _lesson("Retrosynthesis",                         "advanced/03_retrosynthesis.md"),
        _lesson("Spectroscopy (NMR / IR / MS)",           "advanced/04_spectroscopy.md"),
    ],
    "graduate": [
        _lesson("Named reactions library",                "graduate/01_named_reactions.md"),
        _lesson("Asymmetric synthesis",                   "graduate/02_asymmetric.md"),
        _lesson("Molecular orbital theory & reactivity", "graduate/03_mo_theory.md"),
        _lesson("Case studies in total synthesis",        "graduate/04_total_synthesis.md"),
    ],
}
