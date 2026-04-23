"""Reaction wrapper — SMARTS + metadata. Mechanism renderer is Phase-2 work."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional

from rdkit.Chem import AllChem


@dataclass
class Reaction:
    name: str
    reaction_smarts: str
    description: str = ""
    category: str = ""
    reactant_names: List[str] = field(default_factory=list)
    product_names: List[str] = field(default_factory=list)
    db_id: Optional[int] = None

    def rdkit_reaction(self):
        """Return an ``rdkit.Chem.rdChemReactions.ChemicalReaction``."""
        return AllChem.ReactionFromSmarts(self.reaction_smarts)
