# ---------------------------------------------------------------
# Demo 10 — Hückel MO tour on benzene
# ---------------------------------------------------------------
# Run a Hückel calculation on benzene, print every π MO with its
# energy (in units of β, with α = 0), highlight HOMO / LUMO,
# and compute the π-electron stabilisation.  A tiny demonstration
# of the Phase-14a quantum-chemistry module.
#
# Compare the result against the textbook pattern:
#   Energies:  α + 2β,  α + β (×2),  α - β (×2),  α - 2β
#   Occupied:  three lowest MOs, each with 2 electrons
#   Stabilisation: 8β  (6 from naïve localised + 2 from delocalisation)

result = app.huckel_mos(smiles="c1ccccc1")

print(f"Benzene — Hückel π system")
print(f"  π atoms:     {result['n_pi_atoms']}")
print(f"  π electrons: {result['n_pi_electrons']}")
print(f"  HOMO:        {result['homo_energy']:+.3f} β")
print(f"  LUMO:        {result['lumo_energy']:+.3f} β")
print(f"  Total π E:   {result['total_pi_energy']:+.3f} β")

print(f"\n  {'MO':>3s}  {'Energy (β)':>12s}  {'Occupancy':>10s}  label")
print(f"  {'-'*3}  {'-'*12}  {'-'*10}  {'-'*6}")
homo_e = result["homo_energy"]
lumo_e = result["lumo_energy"]
# MOs come sorted from lowest → highest energy.  Number them
# ψ1 (lowest) through ψN.
for i, (e, occ) in enumerate(zip(result["energies_beta"],
                                  result["occupations"]), 1):
    label = ""
    if abs(e - homo_e) < 1e-6 and occ > 0:
        label = "HOMO"
    elif abs(e - lumo_e) < 1e-6 and occ == 0:
        label = "LUMO"
    print(f"  ψ{i:<2d}  {e:+12.3f}  {occ:>10d}  {label}")

gap = homo_e - lumo_e
print(f"\n  HOMO → LUMO gap: {gap:.3f} β "
      f"(≈ {abs(gap) * 270:.0f} kJ/mol with |β| ≈ 270 kJ/mol)")
