"""Tests for Phase 24b — AlphaFold ingestion (no network)."""
from __future__ import annotations
import os
from pathlib import Path
import pytest

pytest.importorskip("rdkit")


_FIXTURE_AF_PDB = """\
HEADER    ALPHAFOLD MONOMER V4 MODEL (P12345)    2024-01-01
TITLE     Predicted structure of test-protein
ATOM      1  N   ALA A   1       0.000   0.000   0.000  1.00 95.00           N
ATOM      2  CA  ALA A   1       1.500   0.000   0.000  1.00 95.00           C
ATOM      3  C   ALA A   1       2.000   1.500   0.000  1.00 95.00           C
ATOM      4  O   ALA A   1       1.500   2.500   0.000  1.00 95.00           O
ATOM      5  CB  ALA A   1       2.000  -1.500   0.000  1.00 95.00           C
ATOM      6  N   GLY A   2       3.500   1.500   0.000  1.00 60.00           N
ATOM      7  CA  GLY A   2       4.500   2.500   0.000  1.00 60.00           C
ATOM      8  C   GLY A   2       5.000   3.500   1.000  1.00 60.00           C
ATOM      9  O   GLY A   2       4.500   4.500   1.000  1.00 60.00           O
END
"""


def test_parse_from_cache_or_string_text_mode():
    from orgchem.sources.alphafold import parse_from_cache_or_string
    r = parse_from_cache_or_string(_FIXTURE_AF_PDB, treat_as_text=True)
    assert r is not None
    assert r.uniprot_id == "TEST"
    # Two residues
    chain = r.protein.get_chain("A")
    assert chain is not None
    assert len(chain.residues) == 2
    # Mean pLDDT = (95 + 60) / 2 = 77.5 → "confident"
    assert abs(r.mean_plddt - 77.5) < 0.1
    assert r.confidence_bucket == "confident"


def test_plddt_bucket_thresholds():
    from orgchem.sources.alphafold import AlphaFoldResult
    from orgchem.core.protein import Protein

    def mk(mean_b):
        return AlphaFoldResult(
            uniprot_id="X", version=4, protein=Protein(pdb_id="X"),
            plddt_by_residue={("A", 1): mean_b},
        )
    assert mk(95).confidence_bucket == "very high"
    assert mk(80).confidence_bucket == "confident"
    assert mk(60).confidence_bucket == "low"
    assert mk(40).confidence_bucket == "very low"


def test_summary_contains_alphafold_fields():
    from orgchem.sources.alphafold import parse_from_cache_or_string
    r = parse_from_cache_or_string(_FIXTURE_AF_PDB, treat_as_text=True)
    s = r.summary()
    for k in ("uniprot_id", "version", "mean_plddt",
              "confidence_bucket", "source"):
        assert k in s
    assert s["source"].startswith("AlphaFold")


def test_cached_path_formats():
    from orgchem.sources.alphafold import cached_af_path
    p = cached_af_path("p12345")
    assert p.name.startswith("AF-P12345-F1-v")


def test_parse_from_cache_missing_returns_none(tmp_path, monkeypatch):
    import orgchem.sources.alphafold as af
    monkeypatch.setattr(af, "_af_cache_dir", lambda: tmp_path)
    assert af.parse_from_cache_or_string("MISSINGID") is None


def test_fetch_rejects_empty_id():
    from orgchem.sources.alphafold import fetch_alphafold_text
    with pytest.raises(ValueError):
        fetch_alphafold_text("")


# ---- Agent actions --------------------------------------------------

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_get_alphafold_info_uncached_returns_error(app, tmp_path, monkeypatch):
    import orgchem.sources.alphafold as af
    monkeypatch.setattr(af, "_af_cache_dir", lambda: tmp_path)
    r = app.call("get_alphafold_info", uniprot_id="NOSUCH")
    assert "error" in r


def test_get_alphafold_info_with_primed_cache(app, tmp_path, monkeypatch):
    import orgchem.sources.alphafold as af
    monkeypatch.setattr(af, "_af_cache_dir", lambda: tmp_path)
    # Prime a fake cache entry matching the default version (4).
    (tmp_path / "AF-P12345-F1-v4.pdb").write_text(_FIXTURE_AF_PDB)
    r = app.call("get_alphafold_info", uniprot_id="p12345")
    assert "error" not in r
    assert r["uniprot_id"] == "P12345"
    assert r["confidence_bucket"] in ("very high", "confident", "low", "very low")
