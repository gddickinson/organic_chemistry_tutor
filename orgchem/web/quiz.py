"""Quiz bank built only from the app's seeded content (no hand-written questions, no invented facts).

Five question kinds, each answer checked against repo data:
- name:     a structure drawn from a seeded molecule -> its name (distractors: other seeded molecules)
- group:    a structure -> a functional group it contains, per the app's SMARTS tagger (core/molecule_tags.auto_tag);
            distractors are groups the same tagger says it does NOT contain
- formula:  a molecule name -> its molecular formula (RDKit CalcMolFormula, as stored by the seeder)
- reaction: a seeded reaction scheme -> the named reaction (distractors: other seeded reactions)
- glossary: a glossary definition with the term blanked out -> the term (distractors: other glossary terms)
The bank is deterministic (fixed seed) so the static site and the server serve the same questions.
"""
from __future__ import annotations

import random
import re
from functools import lru_cache
from urllib.parse import quote

from orgchem.web import chemdata, depict

# Molecule groups whose names make sense as "name this structure" answers (not ions / intermediates / SAR analogues).
NAME_SOURCES = {"basics", "reference-set", "amino-acid", "drug", "solvent", "natural-product", "biomolecule",
                "dye", "pah", "heterocycle", "terpene", "alkane", "alkene", "alkyne", "alcohol", "ketone",
                "aldehyde", "acid", "ester", "amine", "amide", "ether", "monomer", "agrochemical"}
PER_KIND = 30


def pretty_group(g: str) -> str:
    return {"heterocycle_N": "N-heterocycle (aromatic n)", "heterocycle_O": "O-heterocycle (aromatic o)",
            "heterocycle_S": "S-heterocycle (aromatic s)", "aromatic": "benzene ring"}.get(g, g.replace("_", " "))


def short_reaction_name(name: str) -> str:
    """'Fischer esterification' from 'Fischer esterification'; 'SN2' from 'SN2: methyl bromide + hydroxide'."""
    return re.split(r":| \(", name, maxsplit=1)[0].strip()


def _options(rnd, correct, pool, n=3):
    others = [p for p in dict.fromkeys(pool) if p != correct]
    opts = rnd.sample(others, min(n, len(others))) + [correct]
    rnd.shuffle(opts)
    return opts


@lru_cache(maxsize=1)
def bank() -> dict:
    from orgchem.core.molecule_tags import FUNCTIONAL_GROUPS, auto_tag
    rnd = random.Random(20261112)
    snap = chemdata.snapshot()
    mols = [m for m in snap["molecules"] if m["source"] in NAME_SOURCES and m["smiles"] and len(m["name"]) < 40]
    by_name = {m["name"]: m for m in mols}
    names = sorted(by_name)
    qs = []

    for m in rnd.sample(mols, min(PER_KIND, len(mols))):
        same = [x["name"] for x in mols if x["source"] == m["source"]]
        pool = same if len(same) > 4 else names
        qs.append({"kind": "name", "prompt": "Which molecule is this?", "mol": depict.depict_molblock(
            m["molblock_2d"], m["smiles"]), "options": _options(rnd, m["name"], pool), "answer": m["name"],
            "explain": f"{m['name']}: {m['formula']} ({m['smiles']}).", "link": f"#/molecule/{m['id']}"})

    all_groups = [g for g, _ in FUNCTIONAL_GROUPS]
    tagged = [(m, auto_tag(m["smiles"]).functional_groups) for m in mols]
    tagged = [(m, g) for m, g in tagged if g and len(g) < len(all_groups) - 3]
    for m, groups in rnd.sample(tagged, min(PER_KIND, len(tagged))):
        correct = rnd.choice(groups)
        absent = [g for g in all_groups if g not in groups]
        opts = rnd.sample(absent, 3) + [correct]
        rnd.shuffle(opts)
        qs.append({"kind": "group", "prompt": f"Which functional group does {m['name']} contain?",
                   "mol": depict.depict_molblock(m["molblock_2d"], m["smiles"]),
                   "options": [pretty_group(o) for o in opts], "answer": pretty_group(correct),
                   "explain": "The app's SMARTS tagger finds: " + ", ".join(pretty_group(g) for g in groups) + ".",
                   "link": f"#/molecule/{m['id']}"})

    formulas = sorted({m["formula"] for m in mols if m["formula"]})
    for m in rnd.sample(mols, min(PER_KIND, len(mols))):
        near = sorted(formulas, key=lambda f: abs(by_name[m["name"]]["heavy_atom_count"] - _heavy(f)))[:12]
        qs.append({"kind": "formula", "prompt": f"What is the molecular formula of {m['name']}?",
                   "options": _options(rnd, m["formula"], near), "answer": m["formula"],
                   "explain": f"{m['name']} is {m['smiles']}.", "link": f"#/molecule/{m['id']}"})

    rxns = snap["reactions"]
    short = {r["id"]: short_reaction_name(r["name"]) for r in rxns}
    for r in rnd.sample(rxns, min(PER_KIND, len(rxns))):
        qs.append({"kind": "reaction", "prompt": "Which named reaction is this?",
                   "scheme": scheme(r["reaction_smiles"]), "options": _options(rnd, short[r["id"]],
                   sorted(set(short.values()))), "answer": short[r["id"]], "explain": r["name"] + ". "
                   + (r["description"] or ""), "link": f"#/reaction/{r['id']}"})

    gloss = [g for g in snap["glossary"] if g["definition_md"]]
    terms = [g["term"] for g in gloss]
    for g in rnd.sample(gloss, min(PER_KIND, len(gloss))):
        text = g["definition_md"]
        for t in [g["term"], *g["aliases"]]:
            text = re.sub(re.escape(t), "_____", text, flags=re.I)
        qs.append({"kind": "glossary", "prompt": "Which term matches this definition?", "text": text,
                   "options": _options(rnd, g["term"], terms), "answer": g["term"],
                   "explain": "", "link": "#/glossary/" + quote(g["term"], safe="")})
    counts = {k: sum(q["kind"] == k for q in qs) for k in ("name", "group", "formula", "reaction", "glossary")}
    return {"questions": qs, "counts": counts}


def _heavy(formula: str) -> int:
    n = 0
    for el, k in re.findall(r"([A-Z][a-z]?)(\d*)", formula):
        if el != "H":
            n += int(k or 1)
    return n


def scheme(rxn_smiles: str) -> dict:
    """Reactants / agents / products of a reaction SMILES, each fragment drawn on its own."""
    parts = rxn_smiles.split(">")
    lhs, mid, rhs = (parts[0], "", parts[-1]) if len(parts) != 3 else parts
    side = lambda s: [d for d in (depict.depict_smiles(f) for f in s.split(".") if f) if d]  # noqa: E731
    return {"reactants": side(lhs), "agents": side(mid), "products": side(rhs)}
