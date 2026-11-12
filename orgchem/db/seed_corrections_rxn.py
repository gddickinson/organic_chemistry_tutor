"""Correct seeded reactions and synthesis pathways whose SMILES were fixed in a later release.

Reactions and pathways are seeded only into an empty DB, so an existing DB keeps the old SMILES. Each row is matched
by its name AND the exact old SMILES string it was seeded with, so reactions/pathways a user added or edited are left
alone. Fixed on 2026-11-12 together with the molecule rows in ``seed_corrections``: product stereo that contradicted
the reaction's own title (CBS, Sharpless AE/AD, Jacobsen, Mukaiyama, Evans), the aldolase reaction (L-G3P, and a
product that had lost DHAP's phosphate) and the aspartame pathway (D-Phe in the product). Idempotent.
"""
from __future__ import annotations

import logging
from typing import List, Tuple

from orgchem.db.models import Reaction, SynthesisPathway, SynthesisStep
from orgchem.db.session import session_scope

log = logging.getLogger(__name__)

# (reaction name, old reaction SMILES as seeded, corrected reaction SMILES)
REACTION_CORRECTIONS: List[Tuple[str, str, str]] = [
    ("Aldolase class I: DHAP + G3P → F1,6BP",
     "OCC(=O)COP(=O)(O)O.O=C[C@@H](O)COP(=O)(O)O>>OCC(=O)[C@@H](O)[C@H](O)[C@@H](O)COP(=O)(O)O",
     "OCC(=O)COP(=O)(O)O.O=C[C@H](O)COP(=O)(O)O>>O=C(COP(=O)(O)O)[C@@H](O)[C@H](O)[C@H](O)COP(=O)(O)O"),
    ("Sharpless asymmetric epoxidation (trans-crotyl alcohol → 2,3-epoxybutan-1-ol)",
     "C/C=C/CO.CC(C)(C)OO>>C[C@@H]1O[C@H]1CO.CC(C)(C)O",
     "C/C=C/CO.CC(C)(C)OO>>C[C@H]1O[C@@H]1CO.CC(C)(C)O"),
    ("CBS reduction (acetophenone → (R)-1-phenylethanol)",
     "CC(=O)c1ccccc1.B>>O[C@@H](C)c1ccccc1",
     "CC(=O)c1ccccc1.B>>O[C@H](C)c1ccccc1"),
    ("Sharpless asymmetric dihydroxylation (trans-stilbene → (R,R)-1,2-diphenylethane-1,2-diol)",
     "c1ccc(/C=C/c2ccccc2)cc1.O=[Os](=O)(=O)=O.O>>O[C@@H](c1ccccc1)[C@H](O)c1ccccc1.O=[Os]=O",
     "c1ccc(/C=C/c2ccccc2)cc1.O=[Os](=O)(=O)=O.O>>O[C@H](c1ccccc1)[C@H](O)c1ccccc1.O=[Os]=O"),
    ("Jacobsen-Katsuki epoxidation (cis-β-methylstyrene → (2R,3S)-2-methyl-3-phenyloxirane)",
     "C/C=C\\c1ccccc1.[Na+].[O-]Cl>>C[C@H]1O[C@@H]1c1ccccc1.[Na+].[Cl-]",
     "C/C=C\\c1ccccc1.[Na+].[O-]Cl>>C[C@H]1O[C@H]1c1ccccc1.[Na+].[Cl-]"),
    ("Mukaiyama aldol (TMS enol ether of acetone + benzaldehyde → 4-hydroxy-4-phenyl-2-butanone)",
     "C=C(O[Si](C)(C)C)C.O=Cc1ccccc1>>O[C@H](c1ccccc1)CC(=O)C.O[Si](C)(C)C",
     "C=C(O[Si](C)(C)C)C.O=Cc1ccccc1>>O[C@@H](c1ccccc1)CC(=O)C.O[Si](C)(C)C"),
    ("Evans aldol (N-propionyl-(S)-4-benzyloxazolidinone + propanal → syn-(2S,3R)-aldol)",
     "CCC(=O)N1[C@@H](Cc2ccccc2)COC1=O.CCC=O>>CC[C@H](O)[C@@H](C)C(=O)N1[C@@H](Cc2ccccc2)COC1=O",
     "CCC(=O)N1[C@@H](Cc2ccccc2)COC1=O.CCC=O>>CC[C@@H](O)[C@H](C)C(=O)N1[C@@H](Cc2ccccc2)COC1=O"),
]
# (pathway name, old target SMILES, corrected target SMILES, [(step index, old step SMILES, corrected step SMILES)])
PATHWAY_CORRECTIONS: List[Tuple[str, str, str, List[Tuple[int, str, str]]]] = [
    ("Aspartame — Z-protected peptide-coupling route (2-step)",
     "COC(=O)[C@@H](Cc1ccccc1)NC(=O)[C@@H](N)CC(=O)O", "COC(=O)[C@H](Cc1ccccc1)NC(=O)[C@@H](N)CC(=O)O",
     [(1, "O=C(OCc1ccccc1)N[C@@H](CC(=O)O)C(=O)N[C@@H](Cc1ccccc1)C(=O)OC.[H][H].[H][H]>>COC(=O)[C@@H](Cc1ccccc1)NC(=O)[C@@H](N)CC(=O)O.Cc1ccccc1.O=C=O",
       "O=C(OCc1ccccc1)N[C@@H](CC(=O)O)C(=O)N[C@@H](Cc1ccccc1)C(=O)OC.[H][H].[H][H]>>COC(=O)[C@H](Cc1ccccc1)NC(=O)[C@@H](N)CC(=O)O.Cc1ccccc1.O=C=O")]),
]


def apply_reaction_corrections() -> int:
    """Rewrite seeded reactions / pathway SMILES still holding a known-wrong value. Returns the number of fields fixed."""
    fixed = 0
    with session_scope() as s:
        for name, old, new in REACTION_CORRECTIONS:
            for row in s.query(Reaction).filter(Reaction.name == name, Reaction.reaction_smarts == old):
                row.reaction_smarts = new
                fixed += 1
                log.info("Corrected seeded reaction %s", name)
        for name, old_target, new_target, steps in PATHWAY_CORRECTIONS:
            for p in s.query(SynthesisPathway).filter(SynthesisPathway.name == name):
                if p.target_smiles == old_target:
                    p.target_smiles = new_target
                    fixed += 1
                for idx, old, new in steps:
                    for st in s.query(SynthesisStep).filter_by(pathway_id=p.id, step_index=idx, reaction_smiles=old):
                        st.reaction_smiles = new
                        fixed += 1
                log.info("Checked seeded pathway %s for corrections", name)
    return fixed
