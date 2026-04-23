"""Template-based retrosynthesis engine — Phase 8d.

Given a target SMILES, apply a small catalogue of **retrosynthesis
templates** (hand-written SMARTS reactions written in the *product →
reactants* direction) and return the top-K proposed disconnections.

This is a **teaching-grade** engine — not a rival to AiZynthFinder /
SYNTHIA. The template library covers the 8 classical disconnections
highlighted in the retrosynthesis tutorial (ester, amide, biaryl /
Suzuki, ether / Williamson, aldol, Diels-Alder, reductive amination,
nitration), enough for first- and second-year graduate teaching and
for the LLM tutor to reason concretely about "how would you make this?"

Each template:

    RetroTemplate(
        id              — machine-readable identifier,
        label           — short human-readable name,
        description     — markdown explanation,
        smarts_retro    — SMARTS reaction string in product → reactants
                          direction (with atom maps),
        forward_reaction_name — optional cross-reference to the seeded
                          `Reaction.name` that implements the forward step.
    )
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from contextlib import contextmanager

from rdkit import Chem, RDLogger
from rdkit.Chem import AllChem


@contextmanager
def _silence_rdkit_warnings():
    """Suppress RDKit's "product has no mapped atoms" warnings that we
    intentionally trigger for retro-templates with unmapped byproducts
    (e.g. the HNO3 partner of nitration-retro)."""
    RDLogger.DisableLog("rdApp.warning")
    try:
        yield
    finally:
        RDLogger.EnableLog("rdApp.warning")


@dataclass(frozen=True)
class RetroTemplate:
    id: str
    label: str
    description: str
    smarts_retro: str
    forward_reaction_name: Optional[str] = None


# ---------------------------------------------------------------------
# Template catalogue. SMARTS use ``#6`` instead of ``C`` so aromatic
# carbons are matched too; ``[O:n]``, ``[N:n]`` track heteroatoms.

RETRO_TEMPLATES: List[RetroTemplate] = [
    RetroTemplate(
        id="retro-ester",
        label="Ester ⇒ Carboxylic acid + Alcohol",
        description=(
            "Classic Fischer-esterification disconnection. The ester "
            "C–O bond cleaves; the acyl side keeps C=O, the alkyl side "
            "gets a new O–H. Works for both aliphatic and aromatic (phenyl) "
            "ester carbons."
        ),
        smarts_retro="[#6:1](=[O:2])[O:3][#6:4]>>[#6:1](=[O:2])[O:3].[OH][#6:4]",
        forward_reaction_name="Fischer esterification",
    ),
    RetroTemplate(
        id="retro-amide",
        label="Amide ⇒ Carboxylic acid + Amine",
        description=(
            "Amide coupling disconnection (EDC / HATU / activated-ester "
            "forward). The amide C–N bond cleaves; acyl side becomes "
            "acid, amine side becomes free amine."
        ),
        smarts_retro="[#6:1](=[O:2])[NH:3][#6:4]>>[#6:1](=[O:2])O.[NH2:3][#6:4]",
        forward_reaction_name="Amide formation (carboxylic acid + amine)",
    ),
    RetroTemplate(
        id="retro-suzuki-biaryl",
        label="Biaryl ⇒ Aryl halide + Aryl boronic acid",
        description=(
            "Suzuki-Miyaura retrodisconnection. Break the biaryl C–C "
            "bond into Ar–Br + Ar'B(OH)₂ — the standard Pd-catalysed "
            "cross-coupling disconnection."
        ),
        smarts_retro="[c:1]-[c:2]>>[c:1]Br.OB(O)[c:2]",
        forward_reaction_name="Suzuki coupling",
    ),
    RetroTemplate(
        id="retro-williamson-ether",
        label="Ether ⇒ Alkoxide + Alkyl halide",
        description=(
            "Williamson ether synthesis disconnection. Break a C–O–C "
            "aliphatic ether into an alcohol (→ alkoxide under base) "
            "and an alkyl halide. Note: not applicable to aryl ethers "
            "(those need a Buchwald C–O or Ullmann coupling)."
        ),
        smarts_retro="[#6;X4:1][O:2][#6;X4:3]>>[#6;X4:1][O:2][H].Br[#6;X4:3]",
        forward_reaction_name=None,
    ),
    RetroTemplate(
        id="retro-aldol",
        label="β-Hydroxy ketone ⇒ Ketone + Aldehyde",
        description=(
            "Aldol disconnection. A β-hydroxy carbonyl cleaves at the "
            "α-C / β-C bond: the α-side keeps the carbonyl, the β-side "
            "gets a new C=O (aldehyde). Forward step is base- or "
            "acid-catalysed aldol addition."
        ),
        smarts_retro="[#6:1](=[O:2])[#6:3][#6:4]([OH])[#6:5]>>[#6:1](=[O:2])[#6:3].[#6:4](=O)[#6:5]",
        forward_reaction_name="Aldol condensation",
    ),
    RetroTemplate(
        id="retro-diels-alder",
        label="Cyclohexene ⇒ Diene + Dienophile",
        description=(
            "Retro-Diels-Alder: cleave two C–C single bonds across a "
            "cyclohexene to unmask the underlying 1,3-butadiene + "
            "ethylene (or substituted equivalents). Powerful when the "
            "target has a cyclohexene with retro-synthetic symmetry."
        ),
        # Ring-opening retro-[4+2]: cyclohexene → 1,3-butadiene + ethene
        smarts_retro="[#6:1]1[#6:2]=[#6:3][#6:4][#6:5][#6:6]1>>[#6:1]=[#6:2][#6:3]=[#6:4].[#6:5]=[#6:6]",
        forward_reaction_name="Diels-Alder",
    ),
    RetroTemplate(
        id="retro-nitration",
        label="Nitroarene ⇒ Arene + HNO₃",
        description=(
            "Nitration retrodisconnection. A nitrobenzene target came "
            "from the unsubstituted arene + HNO₃/H₂SO₄ electrophilic "
            "aromatic substitution."
        ),
        smarts_retro="[c:1][N+](=O)[O-]>>[c:1][H].O[N+](=O)[O-]",
        forward_reaction_name="Nitration of benzene",
    ),
    RetroTemplate(
        id="retro-reductive-amination",
        label="2° amine ⇒ Ketone + 1° amine (reductive amination)",
        description=(
            "Reductive-amination disconnection. Break the C–N bond of "
            "a secondary amine: one side becomes a ketone (the "
            "imine-forming partner), the other becomes the primary "
            "amine. NaBH₄ / NaBH₃CN / H₂-Pd all work forwardly."
        ),
        smarts_retro="[#6:1][NH:2][CH;X4:3][#6:4]>>[#6:1][NH2:2].[#6:3](=O)[#6:4]",
        forward_reaction_name=None,
    ),
]


# ---------------------------------------------------------------------

def _dedup_products(results: List[Tuple[Chem.Mol, ...]]) -> List[Tuple[str, ...]]:
    """Canonicalise and deduplicate RunReactants output."""
    seen: set = set()
    out: List[Tuple[str, ...]] = []
    for prods in results:
        canon: List[str] = []
        for p in prods:
            try:
                Chem.SanitizeMol(p)
            except Exception:
                # drop a bad product set entirely
                canon = []
                break
            canon.append(Chem.MolToSmiles(p))
        if not canon:
            continue
        key = tuple(sorted(canon))
        if key in seen:
            continue
        seen.add(key)
        out.append(tuple(canon))
    return out


def apply_template(template: RetroTemplate, target_smiles: str
                   ) -> List[Tuple[str, ...]]:
    """Apply one retro-template to a target; return deduplicated precursor sets."""
    mol = Chem.MolFromSmiles(target_smiles)
    if mol is None:
        return []
    try:
        rxn = AllChem.ReactionFromSmarts(template.smarts_retro)
    except Exception:
        return []
    with _silence_rdkit_warnings():
        results = rxn.RunReactants((mol,))
    return _dedup_products(list(results))


def find_retrosynthesis(target_smiles: str,
                        max_templates: int = 0) -> Dict[str, Any]:
    """Return every retro-disconnection the template library can suggest.

    Each proposal is ``{"template_id", "label", "description",
    "precursors": [smiles, ...]}``.

    ``max_templates=0`` means "try all templates"; > 0 limits the
    number of *template types* attempted (not the total number of
    proposals).
    """
    mol = Chem.MolFromSmiles(target_smiles)
    if mol is None:
        return {"error": f"Unparseable SMILES: {target_smiles!r}"}
    proposals: List[Dict[str, Any]] = []
    templates = RETRO_TEMPLATES
    if max_templates > 0:
        templates = templates[:max_templates]
    for t in templates:
        outs = apply_template(t, target_smiles)
        for precursors in outs:
            proposals.append({
                "template_id": t.id,
                "label": t.label,
                "description": t.description,
                "forward_reaction": t.forward_reaction_name,
                "precursors": list(precursors),
            })
    return {
        "target": target_smiles,
        "canonical_target": Chem.MolToSmiles(mol),
        "n_proposals": len(proposals),
        "proposals": proposals,
    }


def list_templates() -> List[Dict[str, str]]:
    """Enumerate the retro-template catalogue for the agent layer."""
    return [
        {"id": t.id, "label": t.label,
         "forward_reaction": t.forward_reaction_name or ""}
        for t in RETRO_TEMPLATES
    ]


# ---------------------------------------------------------------------
# Phase 8d follow-up — multi-step recursive retrosynthesis
# ---------------------------------------------------------------------

def _is_simple_precursor(smiles: str,
                         max_heavy_atoms: int = 8,
                         db_names: Optional[set] = None) -> bool:
    """Heuristic: a precursor is 'simple' (terminate recursion) when
    it's small, in the molecule DB, or has no disconnectable handles
    under any retro template.

    ``db_names`` is an optional pre-loaded set of canonical SMILES
    already in the molecule DB; passing it avoids per-call DB lookups.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return True   # no template will match anyway; terminate
    if mol.GetNumHeavyAtoms() <= max_heavy_atoms:
        return True
    if db_names is not None:
        canon = Chem.MolToSmiles(mol)
        if canon in db_names:
            return True
    # No template applies → inherently terminal
    for t in RETRO_TEMPLATES:
        try:
            rxn = AllChem.ReactionFromSmarts(t.smarts_retro)
        except Exception:
            continue
        with _silence_rdkit_warnings():
            if rxn.RunReactants((mol,)):
                return False
    return True


def _load_db_simple_precursor_set() -> Optional[set]:
    """Return a set of canonical SMILES of every DB molecule, or None
    if the DB isn't initialised (so the recursion still works in
    unit tests that don't start a HeadlessApp)."""
    from orgchem.db import session as _session_mod
    if _session_mod._SessionLocal is None:  # type: ignore[attr-defined]
        return None
    try:
        from orgchem.db.session import session_scope
        from orgchem.db.models import Molecule as DBMol
        with session_scope() as s:
            rows = s.query(DBMol.smiles).all()
        out = set()
        for (smi,) in rows:
            if not smi:
                continue
            m = Chem.MolFromSmiles(smi)
            if m is not None:
                out.add(Chem.MolToSmiles(m))
        return out
    except Exception:
        return None


def find_multi_step_retrosynthesis(target_smiles: str,
                                   max_depth: int = 3,
                                   max_branches: int = 3,
                                   top_paths: int = 10
                                   ) -> Dict[str, Any]:
    """Recursive retrosynthesis (Phase 8d follow-up).

    Starts from ``target_smiles`` and walks every matching retro
    template, then recurses on each precursor that isn't yet "simple"
    (≤8 heavy atoms, in DB, or no templates apply). Caps at
    ``max_depth`` disconnections and ``max_branches`` alternatives
    *per intermediate*.

    Returns ``{"target", "tree": {...}, "paths": [...top_paths...]}``.
    Each path is a list of steps from the target back to its
    terminals; shorter paths come first.
    """
    if max_depth < 1:
        return {"error": "max_depth must be ≥ 1"}
    root_mol = Chem.MolFromSmiles(target_smiles)
    if root_mol is None:
        return {"error": f"Unparseable SMILES: {target_smiles!r}"}

    db_names = _load_db_simple_precursor_set()

    def _recurse(smi: str, depth: int, visited: set) -> Dict[str, Any]:
        canon_mol = Chem.MolFromSmiles(smi)
        canon = Chem.MolToSmiles(canon_mol) if canon_mol else smi
        node: Dict[str, Any] = {
            "smiles": canon,
            "terminal": False,
            "disconnections": [],
        }
        if depth <= 0 or canon in visited or _is_simple_precursor(
                canon, db_names=db_names):
            node["terminal"] = True
            return node
        visited = visited | {canon}
        proposals = find_retrosynthesis(canon)["proposals"]
        proposals = proposals[:max_branches]
        for p in proposals:
            disc = {
                "template_id": p["template_id"],
                "label": p["label"],
                "precursors": [],
            }
            for pre in p["precursors"]:
                disc["precursors"].append(
                    _recurse(pre, depth - 1, visited))
            node["disconnections"].append(disc)
        if not node["disconnections"]:
            node["terminal"] = True
        return node

    tree = _recurse(target_smiles, max_depth, set())

    # Flatten paths from target to leaves
    paths = _extract_paths(tree)
    paths.sort(key=lambda p: (len(p), sum(len(s.get("precursors", []))
                                          for s in p)))
    return {
        "target": Chem.MolToSmiles(root_mol),
        "max_depth": max_depth,
        "tree": tree,
        "paths": paths[:top_paths],
        "n_paths_found": len(paths),
    }


def _extract_paths(tree: Dict[str, Any]) -> List[List[Dict[str, Any]]]:
    """Flatten the disconnection tree into a list of linear paths from
    target to leaves. Each path is a list of ``{smiles, template_id,
    label, precursors}`` steps."""
    paths: List[List[Dict[str, Any]]] = []
    if tree["terminal"] or not tree["disconnections"]:
        paths.append([{"smiles": tree["smiles"], "template_id": None,
                       "label": "terminal precursor",
                       "precursors": []}])
        return paths
    for disc in tree["disconnections"]:
        step = {
            "smiles": tree["smiles"],
            "template_id": disc["template_id"],
            "label": disc["label"],
            "precursors": [pre["smiles"] for pre in disc["precursors"]],
        }
        # For each precursor's subtree, prefix this step.
        sub_paths_combined: List[List[Dict[str, Any]]] = [[step]]
        for pre in disc["precursors"]:
            pre_paths = _extract_paths(pre)
            # Combine: each existing partial path × each precursor's paths.
            new_combined: List[List[Dict[str, Any]]] = []
            for combined in sub_paths_combined:
                for pp in pre_paths:
                    new_combined.append(combined + pp)
            sub_paths_combined = new_combined or sub_paths_combined
        paths.extend(sub_paths_combined)
    return paths
