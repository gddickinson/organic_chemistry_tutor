"""Tests for Phase 24l — 3D protein-structure viewer HTML builder."""
from __future__ import annotations
import os
import pytest

pytest.importorskip("rdkit")


_MINI_PDB = """\
TITLE     MINI FIXTURE
ATOM      1  N   ALA A   1       0.000   0.000   0.000  1.00 10.00           N
ATOM      2  CA  ALA A   1       1.000   0.000   0.000  1.00 10.00           C
ATOM      3  C   ALA A   1       2.000   0.000   0.000  1.00 10.00           C
ATOM      4  O   ALA A   1       2.500   1.000   0.000  1.00 10.00           O
HETATM    5  C1  LIG A 100       5.000   5.000   5.000  1.00 10.00           C
HETATM    6  O1  LIG A 100       6.000   5.000   5.000  1.00 10.00           O
END
"""


def test_build_protein_html_contains_pdb_text(monkeypatch):
    """HTML must carry the input PDB text so 3Dmol.js can parse it."""
    import orgchem.render.draw_protein_3d as d3d
    monkeypatch.setattr(d3d, "local_3dmol_available", lambda: False)
    html = d3d.build_protein_html(_MINI_PDB)
    # The ATOM/HETATM lines should appear inside the backtick-quoted pdb
    assert "ATOM      1" in html
    assert "HETATM    5" in html
    assert '3dmol.org' in html.lower() or "3Dmol-min" in html


def test_protein_styles_render_different_js(monkeypatch):
    import orgchem.render.draw_protein_3d as d3d
    monkeypatch.setattr(d3d, "local_3dmol_available", lambda: False)
    cartoon = d3d.build_protein_html(_MINI_PDB, protein_style="cartoon")
    surface = d3d.build_protein_html(_MINI_PDB, protein_style="surface")
    trace = d3d.build_protein_html(_MINI_PDB, protein_style="trace")
    assert "cartoon" in cartoon.lower()
    assert "surface" in surface.lower()
    # Trace is a cartoon substyle — at least the word "trace" should
    # show up in the styling JS.
    assert "trace" in trace.lower()


def test_ligand_style_ballstick_includes_sphere(monkeypatch):
    import orgchem.render.draw_protein_3d as d3d
    monkeypatch.setattr(d3d, "local_3dmol_available", lambda: False)
    html = d3d.build_protein_html(
        _MINI_PDB, ligand_style="ball-and-stick")
    assert "sphere" in html.lower()
    assert "stick" in html.lower()


def test_highlight_residues_adds_labels(monkeypatch):
    import orgchem.render.draw_protein_3d as d3d
    monkeypatch.setattr(d3d, "local_3dmol_available", lambda: False)
    html = d3d.build_protein_html(
        _MINI_PDB, highlight_residues=["A:ALA1", "LIG100"])
    assert "addResLabels" in html
    # Each highlight entry should generate a valid JS selection object
    assert 'resn: "ALA"' in html
    assert "resi: 1" in html


def test_water_hidden_by_default(monkeypatch):
    import orgchem.render.draw_protein_3d as d3d
    monkeypatch.setattr(d3d, "local_3dmol_available", lambda: False)
    html = d3d.build_protein_html(_MINI_PDB, show_waters=False)
    # A setStyle call hiding HOH/WAT/DOD should be present
    assert '"HOH"' in html or "'HOH'" in html


def test_water_kept_when_show_waters_true(monkeypatch):
    import orgchem.render.draw_protein_3d as d3d
    monkeypatch.setattr(d3d, "local_3dmol_available", lambda: False)
    html_on = d3d.build_protein_html(_MINI_PDB, show_waters=True)
    html_off = d3d.build_protein_html(_MINI_PDB, show_waters=False)
    assert html_on != html_off


def test_surface_option_adds_surface_call(monkeypatch):
    import orgchem.render.draw_protein_3d as d3d
    monkeypatch.setattr(d3d, "local_3dmol_available", lambda: False)
    html = d3d.build_protein_html(_MINI_PDB, show_ligand_surface=True)
    assert "addSurface" in html


def test_build_from_file_round_trip(tmp_path, monkeypatch):
    import orgchem.render.draw_protein_3d as d3d
    monkeypatch.setattr(d3d, "local_3dmol_available", lambda: False)
    p = tmp_path / "fix.pdb"
    p.write_text(_MINI_PDB)
    html = d3d.build_protein_html_from_file(p)
    assert "HETATM    5" in html


def test_build_from_file_missing_raises(tmp_path):
    from orgchem.render.draw_protein_3d import build_protein_html_from_file
    with pytest.raises(FileNotFoundError):
        build_protein_html_from_file(tmp_path / "nope.pdb")


def test_export_writes_file(tmp_path, monkeypatch):
    import orgchem.render.draw_protein_3d as d3d
    monkeypatch.setattr(d3d, "local_3dmol_available", lambda: False)
    out = tmp_path / "viewer.html"
    result = d3d.export_protein_html(_MINI_PDB, out)
    assert result.exists()
    assert result.read_text().startswith("<!DOCTYPE html>")


def test_local_3dmol_inlined_when_available(monkeypatch, tmp_path):
    """If the local 3Dmol.js asset exists, the HTML must inline it (no CDN)."""
    import orgchem.render.draw_protein_3d as d3d
    fake = tmp_path / "3Dmol-min.js"
    fake.write_text("// fake bundle\n" + "x" * 2000)
    monkeypatch.setattr(d3d, "_LOCAL_3DMOL_JS", fake)
    monkeypatch.setattr(d3d, "local_3dmol_available", lambda: True)
    html = d3d.build_protein_html(_MINI_PDB)
    assert "fake bundle" in html
    assert "3dmol.org" not in html.lower()


# ---- Agent action ---------------------------------------------------

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_export_protein_3d_html_action(app, tmp_path, monkeypatch):
    import orgchem.sources.pdb as pdb_mod
    monkeypatch.setattr(pdb_mod, "_pdb_cache_dir", lambda: tmp_path)
    (tmp_path / "MINI.pdb").write_text(_MINI_PDB)
    out = tmp_path / "MINI.html"
    r = app.call("export_protein_3d_html", pdb_id="MINI", path=str(out))
    assert "error" not in r
    assert out.exists()
    assert r["size_bytes"] > 0


def test_export_protein_3d_html_missing_cache(app, tmp_path, monkeypatch):
    import orgchem.sources.pdb as pdb_mod
    monkeypatch.setattr(pdb_mod, "_pdb_cache_dir", lambda: tmp_path)
    r = app.call("export_protein_3d_html", pdb_id="NOPE",
                 path=str(tmp_path / "x.html"))
    assert "error" in r


# ---- pLDDT colour overlay (Phase 24l follow-up) --------------------


def test_plddt_mode_emits_colorfunc(monkeypatch):
    import orgchem.render.draw_protein_3d as d3d
    monkeypatch.setattr(d3d, "local_3dmol_available", lambda: False)
    html = d3d.build_protein_html(_MINI_PDB, colour_mode="plddt")
    assert "colorfunc" in html
    # The AlphaFold DB colours must all appear in the JS colourfunc body.
    for _, colour in d3d._PLDDT_COLOURS:
        assert colour in html


def test_chain_mode_still_emits_colorscheme(monkeypatch):
    import orgchem.render.draw_protein_3d as d3d
    monkeypatch.setattr(d3d, "local_3dmol_available", lambda: False)
    html = d3d.build_protein_html(_MINI_PDB, colour_mode="chain")
    assert 'colorscheme: "chain"' in html
    # None of the pLDDT colour tokens should appear in chain mode.
    for _, colour in d3d._PLDDT_COLOURS:
        assert colour not in html


def test_plddt_mode_compatible_with_surface(monkeypatch):
    """pLDDT colouring must keep working for the surface protein-style."""
    import orgchem.render.draw_protein_3d as d3d
    monkeypatch.setattr(d3d, "local_3dmol_available", lambda: False)
    html = d3d.build_protein_html(
        _MINI_PDB, protein_style="surface", colour_mode="plddt")
    assert "colorfunc" in html
    assert "addSurface" in html


def test_plddt_colourfunc_bucket_boundaries():
    """The JS colourfunc must include the canonical cutoff comparisons."""
    from orgchem.render.draw_protein_3d import _plddt_colourfunc_js
    js = _plddt_colourfunc_js()
    # Four buckets ⇒ three comparisons (90, 70, 50) + terminal fallback.
    assert "> 90" in js
    assert "> 70" in js
    assert "> 50" in js


def test_export_protein_3d_html_plddt_action(app, tmp_path, monkeypatch):
    import orgchem.sources.pdb as pdb_mod
    monkeypatch.setattr(pdb_mod, "_pdb_cache_dir", lambda: tmp_path)
    (tmp_path / "AF.pdb").write_text(_MINI_PDB)
    out = tmp_path / "af.html"
    r = app.call("export_protein_3d_html", pdb_id="AF", path=str(out),
                 colour_mode="plddt")
    assert "error" not in r
    assert r["colour_mode"] == "plddt"
    text = out.read_text()
    assert "colorfunc" in text


# ---- Click-to-inspect picking (Phase 24l follow-up) ---------------


def test_picking_off_by_default(monkeypatch):
    import orgchem.render.draw_protein_3d as d3d
    monkeypatch.setattr(d3d, "local_3dmol_available", lambda: False)
    html = d3d.build_protein_html(_MINI_PDB)
    assert "pick-label" not in html
    assert "setClickable" not in html


def test_picking_injects_overlay_and_handler(monkeypatch):
    import orgchem.render.draw_protein_3d as d3d
    monkeypatch.setattr(d3d, "local_3dmol_available", lambda: False)
    html = d3d.build_protein_html(_MINI_PDB, enable_picking=True)
    # CSS overlay block
    assert "#pick-label" in html
    # In-page label div
    assert 'id="pick-label"' in html
    # 3Dmol click handler
    assert "setClickable" in html
    # QWebChannel loader reference (qrc resource path)
    assert "qtwebchannel/qwebchannel.js" in html


def test_picking_handler_bridges_to_qt(monkeypatch):
    import orgchem.render.draw_protein_3d as d3d
    monkeypatch.setattr(d3d, "local_3dmol_available", lambda: False)
    html = d3d.build_protein_html(_MINI_PDB, enable_picking=True)
    # The JS must reference both the in-page label and the optional
    # Qt bridge with onAtomPicked.
    assert "pickLabel" in html
    assert "onAtomPicked" in html
    assert "qtBridge" in html


def test_picking_compatible_with_plddt(monkeypatch):
    import orgchem.render.draw_protein_3d as d3d
    monkeypatch.setattr(d3d, "local_3dmol_available", lambda: False)
    html = d3d.build_protein_html(
        _MINI_PDB, enable_picking=True, colour_mode="plddt")
    assert "colorfunc" in html
    assert "setClickable" in html


# ---- Rotation animation (Phase 24l follow-up, round 31) ----------


def test_spin_off_by_default(monkeypatch):
    import orgchem.render.draw_protein_3d as d3d
    monkeypatch.setattr(d3d, "local_3dmol_available", lambda: False)
    html = d3d.build_protein_html(_MINI_PDB)
    assert "v.spin(" not in html


def test_spin_emits_spin_call(monkeypatch):
    import orgchem.render.draw_protein_3d as d3d
    monkeypatch.setattr(d3d, "local_3dmol_available", lambda: False)
    html = d3d.build_protein_html(_MINI_PDB, spin=True)
    # Default axis is y.
    assert 'v.spin("y", 1.0);' in html


def test_spin_axis_and_speed(monkeypatch):
    import orgchem.render.draw_protein_3d as d3d
    monkeypatch.setattr(d3d, "local_3dmol_available", lambda: False)
    html = d3d.build_protein_html(_MINI_PDB, spin=True,
                                  spin_axis="x", spin_speed=2.5)
    assert 'v.spin("x", 2.5);' in html


def test_spin_axis_clamped_to_valid():
    """A rogue axis string falls back to y rather than injecting arbitrary JS."""
    import orgchem.render.draw_protein_3d as d3d
    html = d3d.build_protein_html(_MINI_PDB, spin=True,
                                  spin_axis="bogus; alert(1)",
                                  prefer_local=False)
    # No injection: the generated call only uses "y".
    assert 'v.spin("y"' in html
    assert "alert(1)" not in html


def test_export_spin_agent_action(app, tmp_path, monkeypatch):
    import orgchem.sources.pdb as pdb_mod
    monkeypatch.setattr(pdb_mod, "_pdb_cache_dir", lambda: tmp_path)
    (tmp_path / "SPN.pdb").write_text(_MINI_PDB)
    out = tmp_path / "spn.html"
    r = app.call("export_protein_3d_html", pdb_id="SPN",
                 path=str(out), spin=True)
    assert "error" not in r
    assert r["spin"] is True
    assert "v.spin(" in out.read_text()
