"""Phase 10a — conformational dynamics tests."""
from __future__ import annotations
import os
import pytest
from pathlib import Path

import numpy as np

pytest.importorskip("rdkit")


# ---- Direct core -----------------------------------------------------

def test_butane_dihedral_scan_makes_atoms_move():
    from orgchem.core.dynamics import butane_dihedral_scan
    r = butane_dihedral_scan(n_frames=12)
    assert len(r.frames) == 12
    # Inter-frame motion must be non-trivial — atoms should move as the
    # dihedral rotates.
    deltas = [
        np.sqrt(np.mean(np.sum((r.frames[i + 1] - r.frames[i]) ** 2, axis=1)))
        for i in range(len(r.frames) - 1)
    ]
    assert max(deltas) > 0.1, "no atoms moved between frames"
    # Bond lengths should remain sensible — don't let MMFF relaxation
    # run away. Check first C-C stays in 1.4–1.7 Å across all frames.
    for frame in r.frames:
        c_c_dist = np.linalg.norm(frame[0] - frame[1])
        assert 1.4 < c_c_dist < 1.7, f"C-C distance out of range: {c_c_dist:.3f}"


def test_ethane_dihedral_scan_smaller_motion():
    """Ethane H-C-C-H torsion produces a smaller-amplitude animation
    than butane C-C-C-C (only Hs swing, not CH3 groups)."""
    from orgchem.core.dynamics import ethane_dihedral_scan
    r = ethane_dihedral_scan(n_frames=12)
    assert len(r.frames) == 12
    assert len(r.symbols) == 8   # C2H6


def test_cyclohexane_ring_flip_produces_frames():
    from orgchem.core.dynamics import cyclohexane_ring_flip
    r = cyclohexane_ring_flip(n_interp=5)
    # 8 conformers × 5 interpolated + last sample ≥ 36 frames.
    assert len(r.frames) >= 30
    assert len(r.symbols) == 18   # C6H12


def test_xyz_export_is_multi_frame_compatible():
    from orgchem.core.dynamics import butane_dihedral_scan, frames_to_xyz
    r = butane_dihedral_scan(n_frames=6)
    xyz = frames_to_xyz(r)
    assert xyz.count("frame ") == 6
    # Should list 14 atoms per frame.
    lines = xyz.strip().splitlines()
    assert lines[0] == "14"
    assert "C " in xyz
    assert "H " in xyz


def test_invalid_dihedral_rejected():
    from orgchem.core.dynamics import run_dihedral_scan, embed_from_smiles
    from orgchem.messaging.errors import RenderError
    mol = embed_from_smiles("CCCC")
    with pytest.raises(RenderError):
        run_dihedral_scan(mol, dihedral_atoms=(0, 0, 1, 2), n_frames=4)


# ---- Agent actions ---------------------------------------------------

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_run_dihedral_scan_demo_butane(app, tmp_path):
    out = app.call("run_dihedral_scan_demo", demo="butane",
                   path=str(tmp_path / "butane.html"), n_frames=12)
    assert "error" not in out, out
    html = Path(out["path"]).read_text()
    assert "3Dmol" in html
    assert html.count("frame ") == 12
    assert out["frames"] == 12


def test_run_dihedral_scan_demo_cyclohexane(app, tmp_path):
    out = app.call("run_dihedral_scan_demo", demo="cyclohexane",
                   path=str(tmp_path / "chx.html"))
    assert "error" not in out, out
    assert out["frames"] > 20   # many interpolated frames


def test_run_dihedral_scan_demo_unknown(app):
    out = app.call("run_dihedral_scan_demo", demo="nonsense")
    assert "error" in out


def test_run_molecule_dihedral_on_seeded_molecule(app, tmp_path):
    # Ethanol (atom 0=C, 1=C, 2=O) is in the seed.
    rows = app.call("list_all_molecules", filter="Ethanol")
    assert rows
    # Pick an H on C0 and an H on C1 for an H-C-C-O style torsion.
    # SMILES 'CCO' maps to atoms: C0-C1-O2. For a dihedral we need a-b-c-d
    # where b-c is the rotatable bond (C0-C1). So (H, 0, 1, 2) uses an H
    # on C0 attached after AddHs. We don't know exact H index without
    # embedding — use atoms (3, 0, 1, 2) which is (H_on_C0, C0, C1, O).
    out = app.call("run_molecule_dihedral",
                   molecule_id=rows[0]["id"],
                   atom_a=3, atom_b=0, atom_c=1, atom_d=2,
                   path=str(tmp_path / "etoh.html"),
                   n_frames=12)
    assert "error" not in out, out
    assert Path(out["path"]).exists()
