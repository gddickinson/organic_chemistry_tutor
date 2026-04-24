# ---------------------------------------------------------------
# Demo 03 — NSAIDs overlay
# ---------------------------------------------------------------
# Drop four common NSAIDs into the Workbench side-by-side and
# tabulate the drug-likeness descriptors that predict oral absorption.
#
# Run from the Script Editor; open the Workbench tab to see the
# molecules rendered together.

viewer.clear()

nsaids = [
    ("aspirin",    "CC(=O)Oc1ccccc1C(=O)O"),
    ("ibuprofen",  "CC(C)Cc1ccc(cc1)C(C)C(=O)O"),
    ("naproxen",   "COc1ccc2cc(ccc2c1)C(C)C(=O)O"),
    ("celecoxib",  "Cc1ccc(cc1)c1cc(nn1c1ccc(cc1)S(=O)(=O)N)C(F)(F)F"),
]

print(f"{'Drug':12s} {'MW':>7s} {'logP':>6s} {'HBD':>4s} "
      f"{'HBA':>4s} {'TPSA':>6s} {'QED':>6s}")
print("-" * 50)

for name, smi in nsaids:
    viewer.add_molecule(smi, track=name, style="stick")
    dl = app.drug_likeness(smiles=smi)
    desc = dl.get("descriptors", {})
    print(f"{name:12s} {desc.get('mol_weight', 0):7.1f} "
          f"{desc.get('logp', 0):6.2f} "
          f"{desc.get('h_bond_donors', 0):4d} "
          f"{desc.get('h_bond_acceptors', 0):4d} "
          f"{desc.get('tpsa', 0):6.1f} "
          f"{dl.get('qed_score', 0):6.3f}")

print(f"\nScene now shows {len(viewer.tracks())} NSAIDs — rotate "
      "in the Workbench to compare scaffolds.")
