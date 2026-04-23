"""EI-MS fragmentation sketch — Phase 4 follow-up.

Teaching-grade predictor for the peaks students see in a standard
electron-impact mass spectrum. Given a SMILES, propose plausible
fragment m/z values and the common-neutral-loss label that produced
them. Covers the neutral losses every organic-chem textbook walks
through (Silverstein / Pretsch, chapter on mass-spectrometry
fragmentation):

========  =================================  ==============================
ΔM        Neutral loss (formula)             Common cause
========  =================================  ==============================
 −1       H·                                 carbonyl α-cleavage, arenes
−15       CH₃·                               methyl substituent loss
−17       OH·                                alcohol, carboxylic acid
−18       H₂O                                alcohol, enol, α-H ketone
−27       HCN                                nitrile, aromatic N
−28       CO / C₂H₄                          carbonyl (CO), alkene/McLafferty
−29       CHO· / C₂H₅·                       aldehyde
−31       OCH₃·                              methyl ester
−43       C₃H₇· / CH₃CO·                     isopropyl / acetyl
−44       CO₂                                carboxylic acid / ester
−45       COOH· / OC₂H₅·                     carboxylic acid / ethyl ester
−57       C₄H₉·                              tert-butyl
−77       C₆H₅·                              phenyl
========  =================================  ==============================

Each rule carries a SMARTS precondition — we only suggest a loss if
the molecule actually contains the requisite functional group. The
result is a sorted list of candidate peaks (m/z, Δ, label,
mechanism) plus the molecular ion. Intensities are *not* predicted;
real intensities depend on ionisation, stability, and relative rates
beyond the scope of a lookup table.

The implementation is pure RDKit, no external dependencies.
"""
from __future__ import annotations
import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from rdkit import Chem
from rdkit.Chem import AllChem  # noqa: F401 — RDKit init side-effects

from orgchem.core.ms import monoisotopic_mass

log = logging.getLogger(__name__)


# ---------------------------------------------------------------------

@dataclass(frozen=True)
class FragmentRule:
    delta: float                  # mass lost (Da, always positive)
    label: str                    # neutral-loss label, e.g. "H2O"
    mechanism: str                # short description for teaching
    #: If given, rule fires when ANY of these SMARTS match.
    smarts: Optional[tuple] = None


#: Lookup table of common neutral losses. Ordered by Δ ascending so
#: the output is easier to scan. SMARTS uses RDKit semantics (with
#: `[#1]` for explicit H and `[CH3]`/`[CX3]` etc.).
RULES: List[FragmentRule] = [
    FragmentRule(1.00783, "H",
                 "α-cleavage / arene H· loss",
                 smarts=("[#6]",)),
    FragmentRule(15.02348, "CH3",
                 "Methyl loss (α-cleavage, tert-methyl)",
                 smarts=("[CH3]",)),
    FragmentRule(17.00274, "OH",
                 "Hydroxyl loss (alcohols / carboxylic acids)",
                 smarts=("[OX2H]",)),
    FragmentRule(18.01056, "H2O",
                 "Dehydration (alcohols, α-H ketones, enols)",
                 smarts=("[OX2H]", "[CX3]=[OX1]")),
    FragmentRule(27.01090, "HCN",
                 "HCN loss (nitriles / aromatic amines)",
                 smarts=("[C]#[N]", "[nH]")),
    FragmentRule(28.00274, "CO",
                 "CO loss (carbonyl / quinone)",
                 smarts=("[CX3]=[OX1]",)),
    FragmentRule(28.03130, "C2H4",
                 "Ethylene loss (alkene / McLafferty-style)",
                 smarts=("[CX4;H2,H3][CX4;H2,H3]",)),
    FragmentRule(29.00274, "CHO",
                 "Aldehyde CHO· loss",
                 smarts=("[CX3H1]=O", "[CH]=O")),
    FragmentRule(29.03913, "C2H5",
                 "Ethyl loss (α-cleavage)",
                 smarts=("[CH2][CH3]",)),
    FragmentRule(31.01839, "OCH3",
                 "Methoxy loss (methyl ester / methyl ether)",
                 smarts=("[OX2][CH3]",)),
    FragmentRule(43.05478, "C3H7",
                 "Propyl / isopropyl loss",
                 smarts=("[CX4;H1,H2][CX4;H2,H3][CH3]",)),
    FragmentRule(43.01839, "CH3CO",
                 "Acetyl (CH3C=O·) loss",
                 smarts=("[CH3]C(=O)[#6,#7,#8]",)),
    FragmentRule(44.99765, "COOH",
                 "Carboxyl loss (acid / ester)",
                 smarts=("C(=O)[OX2H]",)),
    FragmentRule(43.98983, "CO2",
                 "Carbon-dioxide loss (acid / ester)",
                 smarts=("C(=O)[OX2]",)),
    FragmentRule(45.03404, "OC2H5",
                 "Ethoxy loss (ethyl ester)",
                 smarts=("C(=O)[OX2][CH2][CH3]",)),
    FragmentRule(57.07043, "C4H9",
                 "tert-Butyl loss",
                 smarts=("[CX4](C)(C)C",)),
    FragmentRule(77.03913, "C6H5",
                 "Phenyl loss",
                 smarts=("c1ccccc1",)),
]


@dataclass
class Fragment:
    mz: float                    # fragment monoisotopic m/z (assumes z = 1+)
    delta: float                 # Δ from molecular ion (positive)
    label: str                   # neutral-loss label
    mechanism: str               # teaching description


@dataclass
class FragmentReport:
    smiles: str
    molecular_mass: float
    fragments: List[Fragment] = field(default_factory=list)

    @property
    def n_fragments(self) -> int:
        return len(self.fragments)

    def summary(self) -> Dict[str, object]:
        return {
            "smiles": self.smiles,
            "molecular_mass": round(self.molecular_mass, 5),
            "n_fragments": self.n_fragments,
            "fragments": [
                {"mz": round(f.mz, 4),
                 "delta": round(f.delta, 4),
                 "label": f.label,
                 "mechanism": f.mechanism}
                for f in self.fragments
            ],
        }


# ---------------------------------------------------------------------
# Public API

def predict_fragments(smiles: str,
                      min_mz: float = 20.0) -> FragmentReport:
    """Enumerate plausible EI-MS fragment peaks for ``smiles``.

    Returns a :class:`FragmentReport` including the molecular ion
    (Δ = 0) plus every rule whose SMARTS precondition matches. The
    ``min_mz`` cutoff drops the low-mass baseline so "M − 180 g/mol"
    style losses on benzene don't sneak through as m/z < 20 ghosts.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"Invalid SMILES: {smiles!r}")
    mol_mass = monoisotopic_mass(smiles)
    if not mol_mass:
        raise ValueError(f"Cannot compute monoisotopic mass for {smiles!r}")

    frags: List[Fragment] = [
        Fragment(mz=mol_mass, delta=0.0,
                 label="M+", mechanism="Molecular ion")
    ]
    for rule in RULES:
        if rule.smarts:
            matched = False
            for smart in rule.smarts:
                patt = Chem.MolFromSmarts(smart)
                if patt is not None and mol.HasSubstructMatch(patt):
                    matched = True
                    break
            if not matched:
                continue
        mz = mol_mass - rule.delta
        if mz < min_mz:
            continue
        frags.append(Fragment(mz=mz, delta=rule.delta,
                              label=rule.label,
                              mechanism=rule.mechanism))
    # Sort highest-m/z first so the molecular ion sits at the top.
    frags.sort(key=lambda f: f.mz, reverse=True)
    return FragmentReport(smiles=smiles,
                          molecular_mass=mol_mass,
                          fragments=frags)


def fragmentation_summary(smiles: str) -> Dict[str, object]:
    """Agent-friendly round-trip summary — no live RDKit objects."""
    report = predict_fragments(smiles)
    return report.summary()
