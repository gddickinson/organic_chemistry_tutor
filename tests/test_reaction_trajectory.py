"""Tests for the reaction trajectory builder + 3Dmol HTML wrapper (Phase 2c.2)."""
from __future__ import annotations
import os
import pytest
from pathlib import Path

import numpy as np

pytest.importorskip("rdkit")


# ---- Core trajectory -----------------------------------------------------

def test_xyz_trajectory_sn2_frames_and_atoms():
    from orgchem.core.reaction_trajectory import build_xyz_trajectory
    xyz = build_xyz_trajectory(
        "[C:1][Br:2].[OH:3]>>[C:1][O:3].[Br:2]", n_frames=8)
    assert xyz.count("frame ") == 8
    # Every frame starts with an atom-count line. SN2 has 3 mapped heavy atoms.
    lines = xyz.strip().splitlines()
    atom_count_lines = lines[::5]  # lines 0, 5, 10, ... (3 atoms → 5 lines/frame)
    assert all(l == "3" for l in atom_count_lines)
    # Each frame must contain one of each expected element symbol.
    for i in range(8):
        frame_body = lines[i * 5 + 2: i * 5 + 5]
        elts = {l.split()[0] for l in frame_body}
        assert elts == {"C", "Br", "O"}


def test_xyz_trajectory_endpoints_are_not_identical():
    """First and last frames should differ — otherwise nothing is moving."""
    from orgchem.core.reaction_trajectory import build_xyz_trajectory
    xyz = build_xyz_trajectory(
        "[C:1][Br:2].[OH:3]>>[C:1][O:3].[Br:2]", n_frames=5)
    parts = xyz.split("frame ")
    f1 = parts[1]    # contents of first frame
    f_last = parts[-1]
    assert f1 != f_last


def test_xyz_trajectory_rejects_unmapped():
    from orgchem.core.reaction_trajectory import build_xyz_trajectory
    from orgchem.messaging.errors import RenderError
    with pytest.raises(RenderError):
        build_xyz_trajectory("CC.CC>>CC.CC", n_frames=4)


def test_xyz_trajectory_n_frames_knob():
    from orgchem.core.reaction_trajectory import build_xyz_trajectory
    short = build_xyz_trajectory(
        "[C:1][Br:2].[OH:3]>>[C:1][O:3].[Br:2]", n_frames=3)
    long_ = build_xyz_trajectory(
        "[C:1][Br:2].[OH:3]>>[C:1][O:3].[Br:2]", n_frames=30)
    assert short.count("frame ") == 3
    assert long_.count("frame ") == 30


def test_xyz_trajectory_min_frames():
    from orgchem.core.reaction_trajectory import build_xyz_trajectory
    with pytest.raises(ValueError):
        build_xyz_trajectory(
            "[C:1][Br:2].[OH:3]>>[C:1][O:3].[Br:2]", n_frames=1)


# ---- Kabsch alignment ----------------------------------------------------

def test_kabsch_recovers_identity_on_same_points():
    from orgchem.core.reaction_trajectory import kabsch_align
    p = np.array([[1.0, 2.0, 3.0], [4.0, 0.0, 0.0], [0.0, 5.0, 1.0]])
    aligned = kabsch_align(p, p)
    assert np.allclose(aligned, p, atol=1e-6)


def test_kabsch_aligns_rotated_copy():
    """A 90° rotation applied to a point set should be reversible via Kabsch."""
    from orgchem.core.reaction_trajectory import kabsch_align
    rng = np.random.default_rng(0)
    p = rng.normal(size=(6, 3))
    # Rotate by 90° about z-axis
    R = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
    q = p @ R.T
    q_back = kabsch_align(q, p)
    # RMSD should be near zero.
    rmsd = np.sqrt(np.mean(np.sum((p - q_back) ** 2, axis=1)))
    assert rmsd < 1e-4


# ---- HTML wrapper + agent integration ------------------------------------

def test_html_wrapper_contains_3dmol_call():
    from orgchem.render.draw_reaction_3d import build_trajectory_html
    html = build_trajectory_html("3\nx\nC 0 0 0\nBr 1 0 0\nO 2 0 0\n",
                                 title="test")
    assert "3Dmol" in html
    assert "addModelsAsFrames" in html
    assert "animate" in html
    assert "test" in html


@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_export_trajectory_html_agent_action(app, tmp_path):
    rxns = app.call("list_reactions")
    sn2 = next(r for r in rxns if "SN2: methyl" in r["name"])
    out = app.call("export_reaction_trajectory_html",
                   reaction_id=sn2["id"],
                   path=str(tmp_path / "sn2_traj.html"),
                   n_frames=10)
    assert "error" not in out, out
    text = Path(out["path"]).read_text()
    assert "3Dmol" in text
    assert text.count("frame ") == 10
    assert out["frames"] == 10


def test_export_trajectory_html_unmapped_returns_error(app, tmp_path):
    rxns = app.call("list_reactions")
    fc = next(r for r in rxns if "Friedel-Crafts alkylation" in r["name"])
    out = app.call("export_reaction_trajectory_html",
                   reaction_id=fc["id"],
                   path=str(tmp_path / "nope.html"))
    assert "error" in out
