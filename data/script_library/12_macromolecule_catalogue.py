# ---------------------------------------------------------------
# Demo 12 — Macromolecule catalogue iteration
# ---------------------------------------------------------------
# Sweep the Phase-29 macromolecule catalogues (carbohydrates +
# lipids + nucleic-acids) and tabulate counts per family.  Handy
# as a first-pass audit before writing a lesson, or for a tutor
# asked "what carbohydrates do we have seeded?"

from collections import Counter

def summarise(title: str, rows: list, key: str = "family") -> None:
    print(f"\n{title} ({len(rows)} entries)")
    fams = Counter(r.get(key, "—") for r in rows)
    print("  " + f"{'family':22s}  count")
    print("  " + "-" * 30)
    for fam, n in sorted(fams.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"  {fam:22s}  {n}")

summarise("Carbohydrates", app.list_carbohydrates())
summarise("Lipids",        app.list_lipids())
summarise("Nucleic acids", app.list_nucleic_acids())

# Cross-cutting: tag every nucleic-acid entry that's actually a
# PDB motif (the "pdb-motif" family) so the student can jump
# straight to a fetchable structure.  These power the Fetch-PDB
# button in the NA workspace panel.
nas = app.list_nucleic_acids()
motifs = [n for n in nas if n.get("family") == "pdb-motif"]
print(f"\nPDB-motif entries in the NA catalogue: {len(motifs)}")
for m in motifs:
    pdb = m.get("pdb_id", "—") or "—"
    print(f"  • {m['name']:28s}  PDB {pdb.upper()}  — {m.get('notes', '')[:50]}")
