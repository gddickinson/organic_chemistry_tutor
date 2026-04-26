"""Phase 48a (round 170) — isomer-relationship core.

Headless RDKit-backed helpers for the upcoming Phase-48
isomers exploration tool.  The user-flagged design
(round 165) recommended a 4-pronged integration:

1. **Isomer-relationship explorer dialog** (Tools → *Isomer
   relationships…*, Ctrl+Shift+B) — input a SMILES, get back
   stereoisomers + tautomers + classification of arbitrary
   molecule pairs.
2. Inline **'View isomers' button** on the molecule
   workspace.
3. **Glossary expansion** — 8-10 isomer-related terms
   (constitutional, stereoisomer, enantiomer, diastereomer,
   meso, conformational, tautomer, atropisomer, geometric /
   cis-trans, optical activity).
4. **Tutorial-content cross-link**.

This module ships piece (1)'s headless data core + the
classifier engine.  The dialog (48b), inline button (48c),
glossary expansion (48d), agent actions (48e), and tutorial
cross-link (48f) ship in subsequent rounds.

Pure-headless: no Qt imports.  RDKit is required.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional


# Canonical isomer-relationship vocabulary.
RELATIONSHIPS = (
    "identical",          # same canonical SMILES (incl. stereo)
    "constitutional",     # same molecular formula, different
                          # connectivity
    "enantiomer",         # mirror-image stereoisomers,
                          # non-superimposable
    "diastereomer",       # stereoisomers that are NOT mirror
                          # images
    "meso",               # contains a stereocentre but is
                          # superimposable on its mirror image
                          # (achiral overall)
    "tautomer",           # proton-transfer isomers (keto/enol,
                          # amide/iminol, etc.)
    "different-molecule", # different molecular formula —
                          # not isomers at all
)


@dataclass(frozen=True)
class IsomerEnumerationResult:
    """Return value for the stereoisomer + tautomer
    enumerators.  Carries the input SMILES, a list of
    canonical SMILES strings for the enumerated isomers, and
    a flag noting whether the enumeration was truncated by
    the ``max_results`` cap."""
    input_smiles: str
    canonical_smiles_list: List[str]
    truncated: bool = False


def _canonical(smi: str) -> Optional[str]:
    """Return RDKit's canonical SMILES (with stereo) or
    None if the input doesn't parse."""
    from rdkit import Chem
    if not smi:
        return None
    m = Chem.MolFromSmiles(smi)
    if m is None:
        return None
    return Chem.MolToSmiles(m, isomericSmiles=True)


def _canonical_no_stereo(smi: str) -> Optional[str]:
    """Return canonical SMILES with stereo stripped — used
    for connectivity-only comparison (constitutional vs
    stereoisomeric distinction)."""
    from rdkit import Chem
    if not smi:
        return None
    m = Chem.MolFromSmiles(smi)
    if m is None:
        return None
    return Chem.MolToSmiles(m, isomericSmiles=False)


def molecular_formula(smi: str) -> Optional[str]:
    """Return the molecular formula for a SMILES, or None
    if the input doesn't parse."""
    from rdkit import Chem
    from rdkit.Chem.rdMolDescriptors import CalcMolFormula
    if not smi:
        return None
    m = Chem.MolFromSmiles(smi)
    if m is None:
        return None
    return CalcMolFormula(m)


def enumerate_stereoisomers(
    smiles: str,
    max_results: int = 16,
) -> IsomerEnumerationResult:
    """Enumerate the unassigned stereoisomers of a SMILES.

    Uses RDKit's ``EnumerateStereoisomers`` with
    ``onlyUnassigned=True`` so a fully-specified input
    returns just itself, while an under-specified input
    expands to every consistent stereoisomer.  Capped at
    ``max_results`` to keep highly-stereogenic substrates
    from blowing up the result set.
    """
    from rdkit import Chem
    from rdkit.Chem.EnumerateStereoisomers import (
        EnumerateStereoisomers, StereoEnumerationOptions,
    )
    m = Chem.MolFromSmiles(smiles)
    if m is None:
        return IsomerEnumerationResult(
            input_smiles=smiles, canonical_smiles_list=[],
            truncated=False)
    opts = StereoEnumerationOptions(
        onlyUnassigned=True, maxIsomers=max_results + 1)
    out: List[str] = []
    truncated = False
    for variant in EnumerateStereoisomers(m, options=opts):
        if len(out) >= max_results:
            truncated = True
            break
        out.append(Chem.MolToSmiles(variant, isomericSmiles=True))
    # De-duplicate while preserving order — the enumerator
    # can emit duplicates for symmetric scaffolds.
    seen = set()
    unique = []
    for smi in out:
        if smi not in seen:
            seen.add(smi)
            unique.append(smi)
    return IsomerEnumerationResult(
        input_smiles=smiles, canonical_smiles_list=unique,
        truncated=truncated)


def enumerate_tautomers(
    smiles: str,
    max_results: int = 16,
) -> IsomerEnumerationResult:
    """Enumerate the tautomers of a SMILES.

    Uses RDKit's ``MolStandardize.TautomerEnumerator`` —
    covers keto/enol, amide/iminol, hydroxypyridine /
    pyridone, nitroso/oxime, and ~20 other documented rules.
    Capped at ``max_results`` for substrates with many
    tautomeric protons.
    """
    from rdkit import Chem
    from rdkit.Chem.MolStandardize.rdMolStandardize import (
        TautomerEnumerator,
    )
    m = Chem.MolFromSmiles(smiles)
    if m is None:
        return IsomerEnumerationResult(
            input_smiles=smiles, canonical_smiles_list=[],
            truncated=False)
    te = TautomerEnumerator()
    res = te.Enumerate(m)
    n = len(res)
    out: List[str] = []
    truncated = False
    for i in range(n):
        if len(out) >= max_results:
            truncated = True
            break
        out.append(Chem.MolToSmiles(res[i], isomericSmiles=True))
    # De-duplicate while preserving order.
    seen = set()
    unique = []
    for smi in out:
        if smi not in seen:
            seen.add(smi)
            unique.append(smi)
    return IsomerEnumerationResult(
        input_smiles=smiles, canonical_smiles_list=unique,
        truncated=truncated)


def classify_isomer_relationship(
    smiles_a: str,
    smiles_b: str,
) -> str:
    """Classify the relationship between two molecules as one
    of the canonical RELATIONSHIPS strings.

    Decision tree:
    1. Either SMILES unparseable → ``"different-molecule"``
       (the conservative answer).
    2. Same canonical SMILES (with stereo) → ``"identical"``.
    3. Same connectivity (canonical SMILES without stereo)
       AND ``a`` is the RDKit-computed enantiomer of ``b``
       → ``"enantiomer"``.
    4. Same connectivity AND ``a == b`` after stripping stereo
       AND has at least one stereocentre AND is achiral
       overall (symmetric meso compound) → ``"meso"``.
    5. Same connectivity, different stereo descriptors →
       ``"diastereomer"``.
    6. Different connectivity, same molecular formula →
       ``"constitutional"``.
    7. ``b`` appears in the tautomer enumeration of ``a`` (or
       vice-versa) AND not yet classified above →
       ``"tautomer"``.
    8. Anything else → ``"different-molecule"``.

    The order matters: identical / enantiomer / meso /
    diastereomer all imply same molecular formula, so
    constitutional + tautomer + different-molecule fall
    through.
    """
    from rdkit import Chem
    can_a = _canonical(smiles_a)
    can_b = _canonical(smiles_b)
    if can_a is None or can_b is None:
        return "different-molecule"
    if can_a == can_b:
        return "identical"
    nostereo_a = _canonical_no_stereo(smiles_a)
    nostereo_b = _canonical_no_stereo(smiles_b)

    # Same connectivity → stereoisomeric variant.
    if nostereo_a == nostereo_b:
        # Try the enantiomer test by inverting all
        # stereocentres of `a` and comparing to `b`.
        m_a = Chem.MolFromSmiles(smiles_a)
        inverted = Chem.RWMol(m_a)
        for atom in inverted.GetAtoms():
            tag = atom.GetChiralTag()
            if tag == Chem.ChiralType.CHI_TETRAHEDRAL_CW:
                atom.SetChiralTag(
                    Chem.ChiralType.CHI_TETRAHEDRAL_CCW)
            elif tag == Chem.ChiralType.CHI_TETRAHEDRAL_CCW:
                atom.SetChiralTag(
                    Chem.ChiralType.CHI_TETRAHEDRAL_CW)
        inv_smi = Chem.MolToSmiles(
            inverted.GetMol(), isomericSmiles=True)
        if inv_smi == can_b:
            # If a == its own mirror image (meso compound),
            # the two SMILES are actually identical — that
            # branch was caught above.  Reaching here means
            # a real enantiomeric pair.
            return "enantiomer"
        # Same connectivity, different stereo, NOT mirror
        # image → diastereomeric.
        return "diastereomer"

    # Different connectivity.  Check formula to distinguish
    # constitutional from different-molecule.
    f_a = molecular_formula(smiles_a)
    f_b = molecular_formula(smiles_b)
    if f_a == f_b and f_a is not None:
        # Could still be a tautomer (proton transfer
        # changes connectivity but not formula).  Test
        # tautomer enumeration before falling back to
        # constitutional.
        taut_a = set(enumerate_tautomers(
            smiles_a, max_results=64).canonical_smiles_list)
        if can_b in taut_a:
            return "tautomer"
        return "constitutional"

    return "different-molecule"
