# ---------------------------------------------------------------
# Demo 05 — Lipid catalogue MW report
# ---------------------------------------------------------------
# Iterate the seeded fatty-acid catalogue, compute the exact
# molecular weight from each SMILES via RDKit, and tabulate
# MW / chain length / unsaturation / ω-designation / mp.
#
# Demonstrates the app.<action>(...) path AND direct RDKit use
# (via the pre-imported ``chem`` alias) side-by-side.

from rdkit.Chem import Descriptors

lipids = app.list_lipids()
fatty = [l for l in lipids if l["family"] == "fatty-acid"]
fatty.sort(key=lambda l: (l.get("chain_length") or 0,
                          l.get("unsaturations") or 0))

print(f"{'Name':28s} {'MW':>7s} {'C#':>4s} {'=#':>4s} "
      f"{'ω':>5s} {'mp °C':>7s}")
print("-" * 60)
for l in fatty:
    mol = chem.MolFromSmiles(l["smiles"])
    mw = Descriptors.MolWt(mol) if mol else 0.0
    cl = l.get("chain_length")
    uns = l.get("unsaturations")
    omega = l.get("omega_designation") or "—"
    mp = l.get("melting_point_c")
    mp_s = f"{mp:>7.1f}" if mp is not None else f"{'—':>7s}"
    print(f"{l['name'][:28]:28s} {mw:7.2f} "
          f"{cl if cl is not None else '?':>4} "
          f"{uns if uns is not None else '?':>4} "
          f"{omega:>5s} {mp_s}")

# Quick summary: MW range + correlation hint.
mws = [Descriptors.MolWt(chem.MolFromSmiles(l["smiles"]))
       for l in fatty if chem.MolFromSmiles(l["smiles"])]
print(f"\n{len(fatty)} fatty acids — "
      f"MW {min(mws):.1f} → {max(mws):.1f} Da, "
      f"chains C"
      f"{min((l.get('chain_length') or 99) for l in fatty)}"
      f" to C"
      f"{max((l.get('chain_length') or 0) for l in fatty)}.")
