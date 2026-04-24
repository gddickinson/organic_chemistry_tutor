# ---------------------------------------------------------------
# Demo 01 — Caffeine molecule tour
# ---------------------------------------------------------------
# A walk-through of the core molecule workflow on a single compound:
#   * find caffeine in the seeded DB
#   * print its RDKit-computed descriptors (MW, logP, TPSA, HBD/HBA)
#   * grab its predicted IR band list
#   * query the Lipinski-style drug-likeness report
#
# Run from the Script Editor (Tools → Script editor… / Ctrl+Shift+E).
# Uses the pre-imported globals: app, chem, orgchem, viewer.

hits = app.list_all_molecules(filter="caffeine")
if not hits:
    print("Caffeine is not in the DB — seed or re-seed first.")
else:
    caf = hits[0]
    details = app.get_molecule_details(molecule_id=caf["id"])
    d = details.get("descriptors", {})
    print(f"Caffeine — {details['smiles']}  ({details['formula']})")
    print(f"  MW       = {d.get('mol_weight'):.2f}")
    print(f"  logP     = {d.get('logp'):.2f}")
    print(f"  TPSA     = {d.get('tpsa'):.1f}")
    print(f"  HBD/HBA  = {d.get('h_bond_donors')}/"
          f"{d.get('h_bond_acceptors')}")
    print(f"  rot-bnds = {d.get('rotatable_bonds')}")

    # Spectroscopy: IR bands matched from the functional-group table.
    ir = app.predict_ir_bands(smiles=details["smiles"])
    bands = ir.get("bands", [])
    print(f"\nIR bands ({len(bands)} detected):")
    for b in bands[:5]:
        lo, hi = b.get("range_cm1", [0, 0])
        print(f"  {lo}–{hi} cm⁻¹  ({b.get('intensity', '?')} "
              f"{b.get('mode', '?')})  — {b.get('group')}")

    # Medicinal chemistry: Lipinski / Veber / Ghose summary.
    # `drug_likeness` returns top-level `qed` plus per-rule
    # sub-dicts (lipinski / veber / ghose / pains) — each with
    # its own `violations` list + `passes` bool.
    dl = app.drug_likeness(smiles=details["smiles"])
    lip = dl.get("lipinski", {})
    veb = dl.get("veber", {})
    print(f"\nDrug-likeness: QED = {dl.get('qed', 0):.3f}, "
          f"Lipinski: {lip.get('n_violations', 0)} violation(s) "
          f"({'pass' if lip.get('passes') else 'fail'}), "
          f"Veber: {'pass' if veb.get('passes') else 'fail'}")
