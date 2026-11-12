"""Write tests/fixtures/chem_engine_fixture.json: RDKit / orgchem results the JS chemistry engine is tested against.

Covers every SMILES the app seeds (molecules, reaction components, mechanism steps, pathway steps, glossary examples)
plus the Kekule form of every aromatic molecule:
per SMILES the RDKit atom list (element, aromatic flag, total H count), molecular formula, average and monoisotopic
mass, formal charge and the functional groups of orgchem.core.molecule_tags.auto_tag. Also the element mass tables
and orgchem.core.formula.compute_formula on the Verma et al. 2024 worked examples used in tests/test_formula.py.

Run: python scripts/make_chem_fixture.py     (static/chem_engine.test.mjs reads the fixture;
tests/test_web_chem.py checks it is current)
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
OUT = ROOT / "tests" / "fixtures" / "chem_engine_fixture.json"

# Inputs of tests/test_formula.py (Verma et al. 2024 Table 1): (name, percentages, molar mass)
FORMULA_CASES = [
    ("Nicotine", {"C": 74.00, "H": 8.70, "N": 17.27}, 162.0),
    ("Caffeine", {"C": 49.38, "H": 5.16, "N": 28.76, "O": 16.70}, 194.19),
    ("D-Glucose", {"C": 40.00, "H": 6.67, "O": 53.33}, 180.0),
    ("Cholesterol", {"C": 83.87, "H": 11.91, "O": 4.14}, 386.27),
    ("Porphyrin", {"C": 77.33, "H": 4.51, "N": 18.04}, 310.35),
    ("Codeine", {"C": 72.00, "H": 7.08, "N": 4.69, "O": 16.22}, 299.30),
]


def all_smiles():
    from orgchem.web import chemdata
    s = chemdata.snapshot()
    out = [m["smiles"] for m in s["molecules"]]
    for r in s["reactions"]:
        out += [f for side in r["reaction_smiles"].split(">") for f in side.split(".") if f]
        for st in (r["mechanism"] or {}).get("steps", []):
            out.append(st["smiles"])
    for p in s["pathways"]:
        for st in p["steps"]:
            out += [f for side in st["reaction_smiles"].split(">") for f in side.split(".") if f]
    out += [g["example_smiles"] for g in s["glossary"] if g["example_smiles"] and ">" not in g["example_smiles"]]
    # Kekule forms of every molecule, so the JS aromaticity perception is tested on Kekule input too.
    from rdkit import Chem
    for m in s["molecules"]:
        mol = Chem.MolFromSmiles(m["smiles"])
        if mol is not None and mol.GetNumAtoms() and any(a.GetIsAromatic() for a in mol.GetAtoms()):
            Chem.Kekulize(mol, clearAromaticFlags=True)
            out.append(Chem.MolToSmiles(mol, kekuleSmiles=True))
    return list(dict.fromkeys(out))


def record(smi):
    from rdkit import Chem
    from rdkit.Chem import Descriptors, rdMolDescriptors
    from orgchem.core.molecule_tags import auto_tag
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
        return {"smiles": smi, "error": True}
    return {
        "smiles": smi,
        "atoms": " ".join(f"{a.GetSymbol()}{'a' if a.GetIsAromatic() else ''}{a.GetTotalNumHs()}" for a in mol.GetAtoms()),
        "formula": rdMolDescriptors.CalcMolFormula(mol),
        "mw": Descriptors.MolWt(mol), "exact": Descriptors.ExactMolWt(mol),
        "charge": Chem.GetFormalCharge(mol), "heavy": mol.GetNumHeavyAtoms(),
        "groups": auto_tag(mol).functional_groups,
    }


def build():
    from rdkit import Chem
    from orgchem.core.formula import ATOMIC_MASSES, ATOMIC_MASSES_INTEGER, compute_formula
    pt = Chem.GetPeriodicTable()
    symbols = [pt.GetElementSymbol(z) for z in range(1, 87)]
    masses = {s: [pt.GetAtomicWeight(s), pt.GetMostCommonIsotopeMass(s)] for s in symbols}
    formula = []
    for name, pct, mw in FORMULA_CASES:
        for table, label in ((None, "iupac"), (ATOMIC_MASSES_INTEGER, "integer")):
            try:
                r = compute_formula(pct, mw, masses=table)
                formula.append({"name": name, "masses": label, "pct": pct, "mw": mw,
                                "empirical": r.empirical_formula, "molecular": r.molecular_formula,
                                "empirical_mass": r.empirical_mass, "scale": r.scale_factor,
                                "max_residual": r.max_residual})
            except ValueError as e:
                formula.append({"name": name, "masses": label, "pct": pct, "mw": mw, "error": str(e)})
    return {"masses": masses, "formula_tables": {"iupac": ATOMIC_MASSES, "integer": ATOMIC_MASSES_INTEGER},
            "formula": formula, "molecules": [record(s) for s in all_smiles()]}


if __name__ == "__main__":
    OUT.write_text(json.dumps(build(), indent=0, ensure_ascii=False))
    print(f"wrote {OUT}")
