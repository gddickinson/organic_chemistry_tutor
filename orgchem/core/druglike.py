"""Drug-likeness descriptors — Phase 19b.

Separate from ``core/descriptors.py`` because drug-likeness is a distinct
domain (medicinal-chemistry filters + rules of thumb) and separating it
keeps ``descriptors.py`` small and physical-property-focused.

Rules implemented:
- **Lipinski's rule of five** (already partially in descriptors.py) — the
  canonical oral-drug filter.
- **Veber's rule** — rotatable bonds ≤ 10 and TPSA ≤ 140 Å² for oral
  bioavailability.
- **Ghose filter** — 160 ≤ MW ≤ 480, −0.4 ≤ logP ≤ 5.6, 40 ≤ MR ≤ 130,
  20 ≤ heavy-atom count ≤ 70.
- **PAINS** — pan-assay interference compounds, via RDKit's built-in
  FilterCatalog.
- **QED** — Bickerton et al. quantitative estimate of drug-likeness
  (0 = poor, 1 = excellent).
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List, Optional

from rdkit import Chem
from rdkit.Chem import Descriptors, Crippen, Lipinski, rdMolDescriptors, QED
from rdkit.Chem.FilterCatalog import FilterCatalog, FilterCatalogParams

log = logging.getLogger(__name__)

# Lazy singleton — building the PAINS catalog is costly (~0.1 s).
_pains_catalog: Optional[FilterCatalog] = None


def _get_pains_catalog() -> FilterCatalog:
    global _pains_catalog
    if _pains_catalog is None:
        params = FilterCatalogParams()
        params.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS)
        _pains_catalog = FilterCatalog(params)
    return _pains_catalog


def _parse(smiles_or_mol) -> Chem.Mol:
    if isinstance(smiles_or_mol, str):
        m = Chem.MolFromSmiles(smiles_or_mol)
        if m is None:
            raise ValueError(f"Unparseable SMILES: {smiles_or_mol!r}")
        return m
    return smiles_or_mol


def lipinski(mol_or_smiles) -> Dict[str, Any]:
    """Lipinski rule-of-five: MW ≤ 500, logP ≤ 5, HBD ≤ 5, HBA ≤ 10."""
    m = _parse(mol_or_smiles)
    mw = Descriptors.MolWt(m)
    logp = Crippen.MolLogP(m)
    hbd = Lipinski.NumHDonors(m)
    hba = Lipinski.NumHAcceptors(m)
    violations: List[str] = []
    if mw > 500: violations.append("MW > 500")
    if logp > 5: violations.append("logP > 5")
    if hbd > 5: violations.append("HBD > 5")
    if hba > 10: violations.append("HBA > 10")
    return {"mw": mw, "logp": logp, "hbd": hbd, "hba": hba,
            "violations": violations, "n_violations": len(violations),
            "passes": len(violations) == 0}


def veber(mol_or_smiles) -> Dict[str, Any]:
    """Veber's oral-bioavailability rules: RotB ≤ 10 and TPSA ≤ 140 Å²."""
    m = _parse(mol_or_smiles)
    rotb = Descriptors.NumRotatableBonds(m)
    tpsa = Descriptors.TPSA(m)
    violations: List[str] = []
    if rotb > 10: violations.append("RotB > 10")
    if tpsa > 140: violations.append("TPSA > 140")
    return {"rotb": rotb, "tpsa": tpsa, "violations": violations,
            "passes": len(violations) == 0}


def ghose(mol_or_smiles) -> Dict[str, Any]:
    """Ghose filter: 160 ≤ MW ≤ 480, −0.4 ≤ logP ≤ 5.6, 40 ≤ MR ≤ 130,
    20 ≤ heavy atoms ≤ 70."""
    m = _parse(mol_or_smiles)
    mw = Descriptors.MolWt(m)
    logp = Crippen.MolLogP(m)
    mr = Crippen.MolMR(m)
    heavy = m.GetNumHeavyAtoms()
    violations: List[str] = []
    if not (160 <= mw <= 480): violations.append(f"MW {mw:.1f} outside 160–480")
    if not (-0.4 <= logp <= 5.6): violations.append(f"logP {logp:.2f} outside −0.4–5.6")
    if not (40 <= mr <= 130): violations.append(f"MR {mr:.1f} outside 40–130")
    if not (20 <= heavy <= 70): violations.append(f"heavy-atom {heavy} outside 20–70")
    return {"mw": mw, "logp": logp, "mr": mr, "heavy_atoms": heavy,
            "violations": violations, "passes": len(violations) == 0}


def pains(mol_or_smiles) -> Dict[str, Any]:
    """PAINS match — pan-assay interference compounds."""
    m = _parse(mol_or_smiles)
    cat = _get_pains_catalog()
    matches = cat.GetMatches(m)
    names = [entry.GetDescription() for entry in matches]
    return {"matches": names, "n_matches": len(names), "passes": len(names) == 0}


def qed_score(mol_or_smiles) -> float:
    """Bickerton QED score (0 = poor, 1 = excellent drug-likeness)."""
    m = _parse(mol_or_smiles)
    return float(QED.qed(m))


def drug_likeness_report(mol_or_smiles) -> Dict[str, Any]:
    """Full drug-likeness roll-up — what the GUI / agent display shows.

    Combines Lipinski, Veber, Ghose, PAINS, QED into one dict. Every
    sub-section reports ``passes: bool`` so the GUI can show a traffic-
    light summary.
    """
    m = _parse(mol_or_smiles)
    return {
        "lipinski": lipinski(m),
        "veber": veber(m),
        "ghose": ghose(m),
        "pains": pains(m),
        "qed": qed_score(m),
    }
