# ---------------------------------------------------------------
# Demo 05 — Lipid catalogue report
# ---------------------------------------------------------------
# Iterate the seeded fatty-acid + steroid catalogue, sort by MW,
# and report chain-length / unsaturation / ω-designation for each.
# Demonstrates the app.<action>(...) attribute-access path and
# turning structured action output into a human-readable table.

lipids = app.list_lipids()
fatty = [l for l in lipids if l["family"] == "fatty-acid"]
fatty.sort(key=lambda l: (l.get("chain_length") or 0,
                          l.get("unsaturations") or 0))

print(f"{'Name':28s} {'C#':>4s} {'=#':>4s} {'ω':>5s} "
      f"{'mp °C':>7s}")
print("-" * 52)
for l in fatty:
    cl = l.get("chain_length")
    uns = l.get("unsaturations")
    omega = l.get("omega_designation") or "—"
    mp = l.get("melting_point_c")
    mp_s = f"{mp:>7.1f}" if mp is not None else f"{'—':>7s}"
    print(f"{l['name'][:28]:28s} "
          f"{cl if cl is not None else '?':>4} "
          f"{uns if uns is not None else '?':>4} "
          f"{omega:>5s} {mp_s}")

print(f"\n{len(fatty)} fatty acids — range C"
      f"{min((l.get('chain_length') or 99) for l in fatty)}"
      f" to C"
      f"{max((l.get('chain_length') or 0) for l in fatty)}.")
