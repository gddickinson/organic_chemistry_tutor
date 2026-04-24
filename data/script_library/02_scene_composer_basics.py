# ---------------------------------------------------------------
# Demo 02 — Scene composer basics
# ---------------------------------------------------------------
# The scripted path to the Workbench viewer. Builds a small scene
# of hydrocarbon homologues, shows how to toggle visibility / style,
# and how to read back the track list.
#
# Open the Workbench tab (Ctrl+Shift+B) before running — every
# mutation below shows up live in the embedded 3Dmol.js view.

viewer.clear()

for name, smi in [
    ("methane",  "C"),
    ("ethane",   "CC"),
    ("propane",  "CCC"),
    ("butane",   "CCCC"),
    ("pentane",  "CCCCC"),
    ("cyclohex", "C1CCCCC1"),
]:
    viewer.add_molecule(smi, track=name, style="ball-and-stick")

print(f"Added {len(viewer.tracks())} tracks:")
for t in viewer.tracks():
    print(f"  {t.name:10s}  {t.kind.value:8s}  "
          f"style={t.style}, visible={t.visible}")

# Hide the cyclohexane, then restyle butane as spheres.
viewer.set_visible("cyclohex", False)
viewer.set_style("butane", style="sphere")

print("\nAfter visibility + style toggles:")
for t in viewer.tracks():
    marker = "✗" if not t.visible else " "
    print(f"  {marker} {t.name:10s}  style={t.style}")
