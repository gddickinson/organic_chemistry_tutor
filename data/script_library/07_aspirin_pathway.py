# ---------------------------------------------------------------
# Demo 07 — Aspirin synthesis pathway + green metrics
# ---------------------------------------------------------------
# Pull the seeded Aspirin pathway, inspect its steps, and print
# per-step atom economy + the overall route AE.  A template for
# analysing any of the 15 seeded multi-step syntheses.

paths = app.list_pathways()
aspirin = next((p for p in paths
                if "aspirin" in p["name"].lower()
                or "acetylsalic" in p["name"].lower()), None)

if aspirin is None:
    print("No Aspirin pathway seeded — check seed_pathways.")
else:
    print(f"Pathway: {aspirin['name']}")
    print(f"  Target: {aspirin['target']}")
    print(f"  Steps:  {aspirin['steps']}")
    print(f"  Source: {aspirin.get('source', '—')}")

    gm = app.pathway_green_metrics(pathway_id=aspirin["id"])
    print("\nGreen-metrics per step:")
    print(f"  {'Step':>4s}  {'AE %':>7s}  {'Reactants → product'}")
    print(f"  {'-'*4}  {'-'*7}  {'-'*40}")
    for step in gm["per_step"]:
        ae = step["atom_economy"]
        rxn = step["reaction"]
        # Short-form the SMILES for readability.
        r, p = rxn.split(">>", 1)
        print(f"  {step['step']:>4d}  {ae:>7.2f}  "
              f"{r[:25]:25s} → {p[:20]}")

    overall = gm["overall"]
    print(f"\nOverall atom economy:  "
          f"{overall['overall_atom_economy']:.2f}%"
          f"  ({overall['n_steps']} steps)")
