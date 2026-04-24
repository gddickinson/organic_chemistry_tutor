# ---------------------------------------------------------------
# Demo 06 — Retrosynthesis templates on Aspirin
# ---------------------------------------------------------------
# Apply every SMARTS retro-disconnection template to acetylsalicylic
# acid and print the proposed (reactant → product) precursor pairs.
# A teaching tour of the Phase 8d retro engine.

target = "CC(=O)Oc1ccccc1C(=O)O"    # aspirin
print(f"Target: {target}  (aspirin)\n")

templates = app.list_retro_templates()
print(f"Available retro-templates ({len(templates)}):")
for t in templates:
    print(f"  • {t['label']}")

result = app.find_retrosynthesis(target_smiles=target)
print(f"\n{result['n_proposals']} disconnections found for target:")
for i, p in enumerate(result.get("proposals", []), 1):
    tpl = p.get("template", "?")
    precursors = p.get("precursors", [])
    if isinstance(precursors, list):
        precs = " + ".join(precursors)
    else:
        precs = str(precursors)
    print(f"  {i}. via {tpl}:  {precs}  →  target")
