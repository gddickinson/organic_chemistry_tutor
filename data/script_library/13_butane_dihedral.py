# ---------------------------------------------------------------
# Demo 13 — Butane dihedral-scan trajectory
# ---------------------------------------------------------------
# Run the pre-wired butane C–C–C–C dihedral scan (Phase 10a),
# print the frame count + label, and save the interactive
# 3Dmol.js player as a standalone .html to ``/tmp``.  Opens in
# any browser — step through or play through the 36 frames to
# watch butane's anti / gauche / eclipsed conformers evolve.

import tempfile
from pathlib import Path

out = Path(tempfile.gettempdir()) / "butane_dihedral.html"
r = app.run_dihedral_scan_demo(demo="butane", path=str(out), n_frames=36)

print(f"Dynamics demo:  {r.get('demo')}")
print(f"  label:        {r.get('label')}")
print(f"  frames:       {r.get('frames')}")
print(f"  saved HTML:   {r.get('path')}")
print(f"  size:         {r.get('size_bytes')} bytes")
print(
    "\nOpen the file in any browser to step through the scan. "
    "Anti (180°) is the global minimum; gauche (±60°) ~3.8 kJ/mol "
    "above it; fully eclipsed (0°) is the syn-periplanar maximum."
)

# Also load the butane SMILES into the Workbench as a static
# reference so the user can inspect the starting geometry.
viewer.clear()
viewer.add_molecule("CCCC", track="butane", style="ball-and-stick")
print(f"\nScene tracks: {[t.name for t in viewer.tracks()]}")
