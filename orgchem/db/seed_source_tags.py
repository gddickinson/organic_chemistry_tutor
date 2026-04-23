"""Hand-curated source / drug-class tags for seeded molecules — Phase 28b.

The Phase 28a auto-tagger captures *structural* properties
(functional groups, size, charge, rings). This module adds the
*biological / pharmacological* dimension: "plant natural product",
"NSAID", "statin", "neurotransmitter", "hormone", "steroid",
"alkaloid", "antibiotic:β-lactam", etc.

Applied by :func:`backfill_source_tags`, called from
``seed_if_empty``. Idempotent: the version marker pattern from
``seed_tags`` re-runs when the taxonomy version changes.
"""
from __future__ import annotations
import json
import logging
from typing import Dict, List, Set

from sqlalchemy import select

from orgchem.db.models import Molecule
from orgchem.db.session import session_scope

log = logging.getLogger(__name__)

SEED_VERSION = 1


#: Canonical family taxonomy. Each row is {molecule name → list of
#: tags}. We keep tags short, lowercase, and in the user-facing style
#: (so "NSAID", "statin", etc. preserve their common usage).
_BY_NAME: Dict[str, List[str]] = {
    # ---- NSAIDs ---------------------------------------------------
    "Aspirin": ["drug", "NSAID", "prostaglandin-synthesis-inhibitor"],
    "Ibuprofen": ["drug", "NSAID"],
    "Paracetamol": ["drug", "analgesic"],
    # ---- Statins --------------------------------------------------
    "Atorvastatin": ["drug", "statin", "HMG-CoA-reductase-inhibitor"],
    "Simvastatin": ["drug", "statin", "HMG-CoA-reductase-inhibitor"],
    "Lovastatin": ["drug", "statin", "HMG-CoA-reductase-inhibitor",
                   "natural-product"],
    # ---- Antibiotics ----------------------------------------------
    "Penicillin G": ["drug", "antibiotic", "beta-lactam",
                     "natural-product"],
    "Amoxicillin": ["drug", "antibiotic", "beta-lactam"],
    # ---- Antivirals -----------------------------------------------
    "Oseltamivir": ["drug", "antiviral"],
    "Acyclovir": ["drug", "antiviral"],
    # ---- SSRIs & neuro --------------------------------------------
    "Fluoxetine": ["drug", "SSRI", "antidepressant"],
    "Citalopram": ["drug", "SSRI", "antidepressant"],
    # ---- β-blockers / ACE inhibitors ------------------------------
    "Propranolol": ["drug", "beta-blocker"],
    "Captopril": ["drug", "ACE-inhibitor"],
    "Enalapril": ["drug", "ACE-inhibitor"],
    "Losartan": ["drug", "angiotensin-receptor-blocker"],
    # ---- Other drugs ----------------------------------------------
    "Metformin": ["drug", "antidiabetic"],
    "Warfarin": ["drug", "anticoagulant"],
    "Omeprazole": ["drug", "proton-pump-inhibitor"],
    "Sildenafil": ["drug", "PDE5-inhibitor"],
    "Morphine": ["drug", "opioid", "alkaloid", "natural-product"],
    "Diphenhydramine": ["drug", "antihistamine"],
    "Lidocaine": ["drug", "local-anaesthetic"],
    "Atropine": ["drug", "anticholinergic", "alkaloid",
                 "natural-product"],
    "Quinine": ["drug", "antimalarial", "alkaloid",
                "natural-product"],
    # ---- Neurotransmitters ---------------------------------------
    "Dopamine": ["neurotransmitter", "catecholamine"],
    # ---- Hormones / steroids -------------------------------------
    "Testosterone": ["hormone", "steroid", "androgen"],
    "Estradiol": ["hormone", "steroid", "estrogen"],
    # ---- Nucleosides ---------------------------------------------
    "Adenosine": ["nucleoside", "biomolecule"],
    "Guanosine": ["nucleoside", "biomolecule"],
    "Thymidine": ["nucleoside", "biomolecule"],
    "Cytidine": ["nucleoside", "biomolecule"],
    "Uridine": ["nucleoside", "biomolecule"],
    # ---- Sugars ---------------------------------------------------
    "D-Ribose": ["sugar", "pentose", "biomolecule"],
    "D-Fructose": ["sugar", "hexose", "biomolecule"],
    "Sucrose": ["sugar", "disaccharide", "biomolecule"],
    "Maltose": ["sugar", "disaccharide", "biomolecule"],
    # ---- Fatty acids ---------------------------------------------
    "Palmitic acid": ["fatty-acid", "saturated", "biomolecule"],
    "Oleic acid": ["fatty-acid", "monounsaturated",
                   "omega-9", "biomolecule"],
    "Arachidonic acid": ["fatty-acid", "polyunsaturated",
                         "omega-6", "biomolecule"],
    # ---- Peptides -------------------------------------------------
    "Glutathione": ["peptide", "antioxidant", "biomolecule"],
    # ---- Dyes / pigments -----------------------------------------
    "Indigo": ["dye", "pigment", "vat-dye", "natural-product"],
    "Methyl orange": ["dye", "indicator"],
    "Phenolphthalein": ["dye", "indicator"],
    "Crystal violet": ["dye", "stain"],
    "Malachite green": ["dye", "stain"],
    "Fluorescein": ["dye", "fluorophore"],
    "Rhodamine B": ["dye", "fluorophore"],
    "Eosin Y": ["dye", "stain", "fluorophore"],
    # ---- Reagent subclasses --------------------------------------
    "LDA": ["reagent", "hindered-base"],
    "Lithium aluminium hydride": ["reagent", "hydride-reductant"],
    "Sodium borohydride": ["reagent", "hydride-reductant"],
    "Sodium hydride": ["reagent", "base"],
    "DBU": ["reagent", "hindered-base"],
    "DIPEA": ["reagent", "hindered-base"],
    "TBS chloride": ["reagent", "protecting-group"],
    "mCPBA": ["reagent", "oxidant", "peroxyacid"],
    "Boc anhydride": ["reagent", "protecting-group"],
    "Cbz chloride": ["reagent", "protecting-group"],
    "Dess-Martin periodinane": ["reagent", "oxidant"],
    "Tosyl chloride": ["reagent", "activating-group"],
    "Mesyl chloride": ["reagent", "activating-group"],
    "Sodium methoxide": ["reagent", "base"],
    "Potassium tert-butoxide": ["reagent", "hindered-base"],
    "TMS chloride": ["reagent", "protecting-group"],
    "Acetic anhydride": ["reagent", "acylating-agent"],
    "Benzoyl chloride": ["reagent", "acylating-agent"],
    "NBS": ["reagent", "halogenating-agent"],
    "Oxalyl chloride": ["reagent", "activating-group"],
}


def _tokens_for(row: Molecule) -> List[str]:
    """Assemble the source-tag list for a molecule row.

    Starts with the hand-curated list when the name is known, then
    appends the (existing) ``source`` column value so the broad
    bucket (amino-acid / drug / biomolecule / heterocycle / pah / …)
    is always present.
    """
    tags: List[str] = list(_BY_NAME.get(row.name, []))
    if row.source and row.source not in tags:
        tags.append(row.source)
    return tags


_VERSION_TAG = f"__source_v{SEED_VERSION}__"


def backfill_source_tags(force: bool = False) -> int:
    """Populate ``Molecule.source_tags_json`` from the curated map.

    Idempotent: rows whose source_tags already embed the current
    version marker are skipped unless ``force=True``.
    """
    updated = 0
    with session_scope() as s:
        for row in s.scalars(select(Molecule)).all():
            if (not force
                    and row.source_tags_json
                    and _VERSION_TAG in row.source_tags_json):
                continue
            tags = _tokens_for(row)
            tags.append(_VERSION_TAG)
            row.source_tags_json = json.dumps(tags)
            updated += 1
    if updated:
        log.info("Phase 28b backfill: tagged %d molecule(s) with "
                 "source taxonomy", updated)
    return updated


def list_source_tag_values() -> List[str]:
    """Distinct source-tag values (for the filter-bar combo)."""
    seen: Set[str] = set()
    for tokens in _BY_NAME.values():
        for t in tokens:
            if t.startswith("__"):
                continue
            seen.add(t)
    # Plus the broad bucket labels used on the auto-seed rows.
    for broad in ("amino-acid", "reagent", "drug", "biomolecule",
                  "dye", "pah", "heterocycle"):
        seen.add(broad)
    return sorted(seen)
