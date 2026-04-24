# ---------------------------------------------------------------
# Demo 09 — Diels-Alder energy profile walk-through
# ---------------------------------------------------------------
# Enumerate seeded reaction-coordinate diagrams, pick the Diels-
# Alder entry, and print every stationary point (reactants → TS‡
# → product) with its energy + label.  Mirrors what the energy-
# profile viewer dialog shows graphically.

profiles = app.list_energy_profiles()
print(f"Seeded energy profiles ({len(profiles)}):")
for p in profiles:
    print(f"  • {p['name']:42s}  ({p['points']} stationary points)")

target = next((p for p in profiles if "Diels" in p["name"]), None)
if target is None:
    print("\nNo Diels-Alder profile seeded.")
else:
    detail = app.get_energy_profile(reaction_id=target["id"])
    if "error" in detail:
        print(f"\n{detail['error']}")
    else:
        prof = detail["profile"]
        unit = prof.get("unit", "kJ/mol")
        print(f"\n=== {detail['name']} ===")
        print(f"  stationary points  (energies in {unit}):")
        for pt in prof.get("points", []):
            label = pt.get("label", "?")
            energy = pt.get("energy", 0.0)
            marker = "‡" if pt.get("is_ts") else " "
            print(f"    {marker} {label:22s}  E = {energy:8.2f}")
        # Derived quantities — compute them from the stationary-
        # point list (the JSON blob is a plain dict; the dataclass
        # methods that normally return these live in
        # orgchem.core.energy_profile).
        pts = prof.get("points", [])
        if pts:
            e_reactants = pts[0].get("energy", 0.0)
            e_product = pts[-1].get("energy", 0.0)
            max_ts = max(
                (p.get("energy", 0.0) for p in pts if p.get("is_ts")),
                default=None,
            )
            if max_ts is not None:
                print(f"\n  Ea (forward):  {max_ts - e_reactants:8.2f} "
                      f"{unit}")
                print(f"  Ea (reverse):  {max_ts - e_product:8.2f} "
                      f"{unit}")
            print(f"  ΔH (overall):  {e_product - e_reactants:8.2f} "
                  f"{unit}  "
                  f"({'exothermic' if e_product < e_reactants else 'endothermic'})")
