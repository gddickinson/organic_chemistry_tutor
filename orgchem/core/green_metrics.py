"""Green-chemistry metrics — Phase 17a / 18a.

Canonical quantitative measures for the environmental footprint of a
synthetic route:

- **Atom economy (AE)**  Trost, 1991. The mass fraction of the reactant
  atoms that ends up in the desired product. Independent of experimental
  yield — purely a feature of the balanced equation.

      AE = MW(product) / Σ MW(reactants)   × 100 %

- **E-factor**  Sheldon, 1992. Mass of waste per mass of product. Zero is
  ideal; industrial fine chemicals are often 25–100, pharmaceuticals
  25–100+. Requires experimental masses.

      E-factor = (total mass of inputs − mass of product) / mass of product

- **Process-mass intensity (PMI)** total mass of everything fed into the
  process (reactants, reagents, solvents, water) divided by mass of
  product. PMI = E-factor + 1.

Inputs are SMILES / reaction-SMILES strings; we pull molecular weights
via RDKit. No external deps beyond the ones already in requirements.txt.
"""
from __future__ import annotations
import logging
from typing import Dict, List, Tuple

from rdkit import Chem
from rdkit.Chem import Descriptors

log = logging.getLogger(__name__)


def mol_weight(smiles: str) -> float:
    """MW of a single SMILES fragment, in g/mol.

    Uses RDKit's ``ExactMolWt``. An unparseable fragment yields 0.0 and
    logs a warning — we don't raise because batch pathway analyses shouldn't
    abort on one dodgy side-product SMILES.
    """
    if not smiles:
        return 0.0
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        log.warning("mol_weight: unparseable SMILES %r", smiles)
        return 0.0
    return float(Descriptors.ExactMolWt(mol))


def _split_reaction(reaction_smiles: str) -> Tuple[List[str], List[str]]:
    """Parse a ``reactants>reagents>products`` or ``reactants>>products`` string.

    Returns (reactant_smiles_list, product_smiles_list). Reagents above the
    arrow are treated as reactants for atom-accounting (they contribute atoms
    too). Individual fragments come from splitting on ``.``.
    """
    s = reaction_smiles.strip()
    # Reaction SMILES uses '>' separators; SMARTS/SMILES-only falls back.
    if ">" in s:
        parts = s.split(">")
        if len(parts) == 3:
            reactants, reagents, products = parts
            lhs = [f for f in _split_fragments(reactants) if f]
            lhs += [f for f in _split_fragments(reagents) if f]
            rhs = [f for f in _split_fragments(products) if f]
            return lhs, rhs
        if len(parts) == 2:
            lhs = [f for f in _split_fragments(parts[0]) if f]
            rhs = [f for f in _split_fragments(parts[1]) if f]
            return lhs, rhs
    # Fallback: no arrow — treat the whole thing as products (AE undefined).
    return [], [f for f in _split_fragments(s) if f]


def _split_fragments(smiles: str) -> List[str]:
    return [f for f in smiles.split(".") if f]


def atom_economy(reaction_smiles: str, product_index: int = None) -> Dict[str, float]:
    """Atom economy for a reaction SMILES.

    ``product_index`` selects which product fragment to treat as the
    *desired* product (the rest count as by-products whose mass is
    "wasted atoms"). Default: the fragment with the largest MW — the
    convention for named reactions where the intended product is typically
    the heaviest fragment on the right-hand side (water and HX by-products
    are the rest).

    Returns ``{"atom_economy": %, "mw_product": g/mol, "mw_reactants": g/mol,
    "desired_product": smi}`` or ``{"error": ...}``.
    """
    reactants, products = _split_reaction(reaction_smiles)
    if not reactants or not products:
        return {"error": f"Cannot parse reaction SMILES {reaction_smiles!r}"}
    if product_index is None:
        # pick heaviest product fragment
        mws = [mol_weight(s) for s in products]
        product_index = max(range(len(products)), key=lambda i: mws[i])
    elif not (-len(products) <= product_index < len(products)):
        return {"error": f"product_index {product_index} out of range "
                         f"for {len(products)} products"}
    mw_reactants = sum(mol_weight(s) for s in reactants)
    mw_product = mol_weight(products[product_index])
    if mw_reactants <= 0.0 or mw_product <= 0.0:
        return {"error": "Zero or negative MW — one fragment failed to parse"}
    ae_pct = 100.0 * mw_product / mw_reactants
    return {
        "atom_economy": ae_pct,
        "mw_product": mw_product,
        "mw_reactants": mw_reactants,
        "desired_product": products[product_index],
        "n_reactants": len(reactants),
        "n_products": len(products),
    }


def e_factor(mass_inputs: float, mass_product: float) -> Dict[str, float]:
    """E-factor and PMI from experimental masses (any consistent units).

    ``mass_inputs`` is total mass fed into the process (reactants, reagents,
    solvents, water). ``mass_product`` is mass of isolated, purified product.
    """
    if mass_product <= 0.0:
        return {"error": "mass_product must be > 0"}
    if mass_inputs < mass_product:
        return {"error": "mass_inputs < mass_product — are units consistent?"}
    ef = (mass_inputs - mass_product) / mass_product
    pmi = mass_inputs / mass_product
    return {"e_factor": ef, "pmi": pmi,
            "mass_inputs": mass_inputs, "mass_product": mass_product}


def pathway_atom_economy(step_reaction_smiles: List[str]) -> Dict[str, float]:
    """Overall atom economy for a multi-step pathway.

    Each step's AE is computed; the overall value is their product (in
    fraction form), i.e. the fraction of the *initial* reactant atoms that
    survive all the way to the final product. Returns per-step AE too.
    """
    step_ae: List[float] = []
    for rxn in step_reaction_smiles:
        r = atom_economy(rxn)
        if "error" in r:
            return {"error": f"Step {len(step_ae) + 1}: {r['error']}"}
        step_ae.append(r["atom_economy"])
    if not step_ae:
        return {"error": "No steps supplied"}
    overall_frac = 1.0
    for v in step_ae:
        overall_frac *= v / 100.0
    return {
        "overall_atom_economy": 100.0 * overall_frac,
        "step_atom_economies": step_ae,
        "n_steps": len(step_ae),
    }
