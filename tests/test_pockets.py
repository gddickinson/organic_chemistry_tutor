"""Tests for Phase 24d — grid-based pocket detection."""
from __future__ import annotations
import os
from math import cos, sin, pi
import pytest

pytest.importorskip("rdkit")


def _spherical_shell_pdb(radius: float = 10.0, n_atoms: int = 60,
                         open_angle_degrees: float = 60.0,
                         cavity_radius: float = 0.0) -> str:
    """Build a synthetic 'hollow-sphere-with-an-opening' protein:
    n_atoms placed on a sphere of given radius, skipping a cap of
    ``open_angle_degrees`` so there's a clear pocket at the centre.
    """
    import math
    open_cos = math.cos(math.radians(open_angle_degrees))
    lines = ["TITLE     SYNTHETIC SPHERICAL CAVITY"]
    serial = 1
    # Fibonacci-sphere sampling for even distribution
    for i in range(n_atoms):
        phi = math.acos(1 - 2 * (i + 0.5) / n_atoms)
        theta = math.pi * (1 + 5 ** 0.5) * i
        x = radius * sin(phi) * cos(theta)
        y = radius * sin(phi) * sin(theta)
        z = radius * cos(phi)
        # Skip atoms in the opening cap (on +z side)
        if z / radius > open_cos:
            continue
        lines.append(
            f"ATOM  {serial:>5d}  CA  ALA A{serial:>4d}    "
            f"{x:>8.3f}{y:>8.3f}{z:>8.3f}  1.00 10.00           C"
        )
        serial += 1
    lines.append("END")
    return "\n".join(lines)


def test_find_pockets_on_hollow_sphere():
    """A hollow sphere with a small opening should produce at least one
    pocket cluster near the origin."""
    from orgchem.core.protein import parse_pdb_text
    from orgchem.core.pockets import find_pockets
    pdb = _spherical_shell_pdb(radius=8.0, n_atoms=80, open_angle_degrees=30)
    protein = parse_pdb_text(pdb, pdb_id="SHELL")
    pockets = find_pockets(protein, grid_spacing=1.5, margin=3.0,
                           probe_min=2.0, probe_max=7.0,
                           min_cluster_size=5, top_k=5)
    assert pockets, "expected at least one pocket in hollow sphere"
    # Centre of largest pocket should be near the origin (within ~3 Å)
    cx, cy, cz = pockets[0].centre
    assert cx * cx + cy * cy + cz * cz < 4.0 ** 2


def test_find_pockets_returns_empty_for_unfolded_peptide():
    """A tiny dipeptide with no buried cavities should return no pockets."""
    from orgchem.core.protein import parse_pdb_text
    from orgchem.core.pockets import find_pockets
    minimal = """\
ATOM      1  CA  ALA A   1       0.000   0.000   0.000  1.00 10.00           C
ATOM      2  CA  GLY A   2       3.800   0.000   0.000  1.00 10.00           C
END
"""
    protein = parse_pdb_text(minimal, pdb_id="MINI")
    pockets = find_pockets(protein, min_cluster_size=10)
    # Two isolated CAs don't form a cavity.
    assert pockets == []


def test_pocket_lining_residues_populated():
    from orgchem.core.protein import parse_pdb_text
    from orgchem.core.pockets import find_pockets
    pdb = _spherical_shell_pdb(radius=7.0, n_atoms=60, open_angle_degrees=30)
    protein = parse_pdb_text(pdb, pdb_id="SHELL")
    pockets = find_pockets(protein, grid_spacing=1.5, margin=3.0,
                           min_cluster_size=5, top_k=3)
    assert pockets
    assert pockets[0].lining_residues, \
        "top pocket should have lining residues annotated"
    assert all("A:" in r for r in pockets[0].lining_residues)


def test_pockets_summary_dict():
    from orgchem.core.protein import parse_pdb_text
    from orgchem.core.pockets import find_pockets, pockets_summary
    pdb = _spherical_shell_pdb(radius=7.0, n_atoms=60, open_angle_degrees=30)
    protein = parse_pdb_text(pdb, pdb_id="SHELL")
    pockets = find_pockets(protein, grid_spacing=1.5, margin=3.0,
                           min_cluster_size=5, top_k=3)
    summary = pockets_summary(pockets)
    assert summary["n_pockets"] == len(pockets)
    for p_dict in summary["pockets"]:
        assert "volume_voxels" in p_dict
        assert "centre" in p_dict
        assert isinstance(p_dict["lining_residues"], list)


# ---- Agent action ---------------------------------------------------

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_find_binding_sites_uncached_error(app, tmp_path, monkeypatch):
    import orgchem.sources.pdb as pdb_mod
    monkeypatch.setattr(pdb_mod, "_pdb_cache_dir", lambda: tmp_path)
    r = app.call("find_binding_sites", pdb_id="NOPE")
    assert "error" in r


def test_find_binding_sites_with_cache(app, tmp_path, monkeypatch):
    import orgchem.sources.pdb as pdb_mod
    monkeypatch.setattr(pdb_mod, "_pdb_cache_dir", lambda: tmp_path)
    pdb_text = _spherical_shell_pdb(radius=8.0, n_atoms=80,
                                    open_angle_degrees=30)
    (tmp_path / "SHELL.pdb").write_text(pdb_text)
    r = app.call("find_binding_sites", pdb_id="shell", top_k=3)
    assert "error" not in r
    assert r["n_pockets"] >= 1
