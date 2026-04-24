# ---------------------------------------------------------------
# Demo 08 — Stereochemistry tour on L-alanine
# ---------------------------------------------------------------
# Walk through R/S descriptor assignment on L-alanine, generate
# its enantiomer, and round-trip the descriptors to confirm the
# centre flipped as expected.  Shows the stereo-chem module + how
# to drop both enantiomers into the Workbench side-by-side.

viewer.clear()

alanine_S = "C[C@H](N)C(=O)O"    # L-alanine = (S)-alanine
alanine_R = "C[C@@H](N)C(=O)O"   # D-alanine = (R)-alanine, for reference

rs_S = app.assign_stereodescriptors(smiles=alanine_S)
print(f"L-alanine  ({alanine_S})")
print(f"  is_chiral: {rs_S['is_chiral']}")
print(f"  n_stereocentres: {rs_S['n_stereocentres']}")
print(f"  R/S descriptors: {rs_S['rs']}")

enant = app.enantiomer_of(smiles=alanine_S)
print(f"\nenantiomer_of → {enant['enantiomer_smiles']}")
print(f"  new R/S: {enant['rs']}")

# Sanity check — the enantiomer's descriptors must have FLIPPED
# on every assigned centre.
for idx, rs in rs_S["rs"].items():
    other = enant["rs"].get(idx, "?")
    flipped = "✓" if other != rs else "✗"
    print(f"  atom {idx}: {rs} → {other}  {flipped}")

# Drop both enantiomers into the Workbench so the student can
# rotate them and compare.  Labels come from Track.meta['smiles'].
viewer.add_molecule(alanine_S, track="L-alanine (S)")
viewer.add_molecule(alanine_R, track="D-alanine (R)")
print(f"\nScene tracks: {[t.name for t in viewer.tracks()]}")
