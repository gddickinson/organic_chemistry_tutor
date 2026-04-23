"""Tests for Phase 26b — glossary example-figure generator."""
from __future__ import annotations
import os
import pytest

pytest.importorskip("rdkit")


def test_term_slug_is_filename_safe():
    from orgchem.core.glossary_figures import term_slug
    assert term_slug("Aromaticity") == "aromaticity"
    assert term_slug("Diels-Alder reaction") == "diels_alder_reaction"
    # Unicode / spaces / punctuation collapse cleanly.
    assert term_slug("  SN 2 → nu!") == "sn_2_nu"


def test_render_molecule_to_png(tmp_path):
    from orgchem.core.glossary_figures import render_term
    r = render_term("Aromaticity", "c1ccccc1", out_dir=tmp_path,
                    force=True, fmt="png")
    assert r.rendered
    assert r.path.exists()
    # PNG magic number.
    assert r.path.read_bytes()[:4] == b"\x89PNG"


def test_render_reaction_to_png(tmp_path):
    from orgchem.core.glossary_figures import render_term
    r = render_term("Aldol reaction",
                    "CC(=O)C.CC=O>>CC(=O)CC(O)C",
                    out_dir=tmp_path, force=True, fmt="png")
    assert r.rendered
    assert r.path.exists()


def test_render_svg(tmp_path):
    from orgchem.core.glossary_figures import render_term
    r = render_term("Aromaticity", "c1ccccc1", out_dir=tmp_path,
                    force=True, fmt="svg")
    assert r.rendered
    assert r.path.suffix == ".svg"
    assert "<svg" in r.path.read_text()


def test_render_is_incremental(tmp_path):
    """When force=False, a second call skips with 'already exists'."""
    from orgchem.core.glossary_figures import render_term
    r1 = render_term("Aromaticity", "c1ccccc1", out_dir=tmp_path)
    r2 = render_term("Aromaticity", "c1ccccc1", out_dir=tmp_path)
    assert r1.rendered
    assert not r2.rendered
    assert r2.skipped_reason == "already exists"


def test_invalid_smiles_skipped(tmp_path):
    from orgchem.core.glossary_figures import render_term
    r = render_term("bad", "not_a_real_smiles", out_dir=tmp_path,
                    force=True)
    assert not r.rendered
    assert "invalid SMILES" in (r.skipped_reason or "")


def test_empty_smiles_skipped(tmp_path):
    from orgchem.core.glossary_figures import render_term
    r = render_term("bad", "", out_dir=tmp_path, force=True)
    assert not r.rendered
    assert r.skipped_reason == "no example_smiles"


def test_regenerate_all_hits_seed_anchors(tmp_path):
    from orgchem.core.glossary_figures import regenerate_all
    results = regenerate_all(out_dir=tmp_path, force=True, fmt="png")
    rendered_terms = {r.term for r in results if r.rendered}
    # Four anchors seeded in round 32.
    for t in ("Aromaticity", "Carbocation",
              "Diels-Alder reaction", "Aldol reaction"):
        assert t in rendered_terms


# ---- Agent action -------------------------------------------------

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_get_glossary_figure_action(app, tmp_path):
    out = tmp_path / "aromaticity.png"
    r = app.call("get_glossary_figure", term="Aromaticity",
                 path=str(out))
    assert "error" not in r
    assert out.exists()
    assert r["size_bytes"] > 0


def test_get_glossary_figure_unknown_term(app, tmp_path):
    r = app.call("get_glossary_figure", term="NotARealTerm",
                 path=str(tmp_path / "x.png"))
    assert "error" in r


def test_get_glossary_figure_no_example(app, tmp_path):
    """A term without example_smiles returns an error. Transition state
    is a concept without a canonical SMILES, so it stays unannotated."""
    r = app.call("get_glossary_figure", term="Transition state",
                 path=str(tmp_path / "x.png"))
    assert "error" in r
