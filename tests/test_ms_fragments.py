"""Tests for Phase 4 EI-MS fragmentation sketch."""
from __future__ import annotations
import os
import pytest

pytest.importorskip("rdkit")


def test_molecular_ion_present():
    """Every prediction must include the molecular ion (Δ = 0)."""
    from orgchem.core.ms_fragments import predict_fragments
    r = predict_fragments("CCO")
    labels = [f.label for f in r.fragments]
    assert "M+" in labels


def test_alcohol_loses_water_and_hydroxyl():
    from orgchem.core.ms_fragments import predict_fragments
    r = predict_fragments("CCO")
    labels = [f.label for f in r.fragments]
    assert "OH" in labels
    assert "H2O" in labels


def test_aldehyde_loses_cho():
    from orgchem.core.ms_fragments import predict_fragments
    r = predict_fragments("O=Cc1ccccc1")   # benzaldehyde, M = 106
    labels = [f.label for f in r.fragments]
    assert "CHO" in labels


def test_ketone_loses_co():
    from orgchem.core.ms_fragments import predict_fragments
    r = predict_fragments("CC(=O)CC")  # 2-butanone
    labels = [f.label for f in r.fragments]
    assert "CO" in labels


def test_carboxylic_acid_loses_cooh_and_co2():
    from orgchem.core.ms_fragments import predict_fragments
    r = predict_fragments("OC(=O)c1ccccc1")   # benzoic acid, M = 122
    labels = [f.label for f in r.fragments]
    assert "COOH" in labels
    assert "CO2" in labels


def test_methyl_ester_loses_methoxy():
    from orgchem.core.ms_fragments import predict_fragments
    r = predict_fragments("CC(=O)OC")   # methyl acetate
    labels = [f.label for f in r.fragments]
    assert "OCH3" in labels


def test_phenyl_ring_loses_phenyl():
    from orgchem.core.ms_fragments import predict_fragments
    r = predict_fragments("c1ccccc1CC")  # ethylbenzene
    labels = [f.label for f in r.fragments]
    assert "C6H5" in labels


def test_fragments_below_min_mz_are_dropped():
    from orgchem.core.ms_fragments import predict_fragments
    # Benzene is 78 Da; a CH3 loss lands at 63 — above default cutoff 20.
    # But setting min_mz=70 should drop any loss > 8 Da.
    r = predict_fragments("c1ccccc1CC", min_mz=200.0)
    # All predicted fragments must be >= 200 — only the M+ should survive
    # if it's above cutoff. For a ~106 Da molecule that means zero non-M+.
    non_mp = [f for f in r.fragments if f.label != "M+"]
    assert non_mp == []


def test_invalid_smiles_raises():
    from orgchem.core.ms_fragments import predict_fragments
    with pytest.raises(ValueError):
        predict_fragments("not_a_real_smiles")


def test_summary_shape():
    from orgchem.core.ms_fragments import predict_fragments
    s = predict_fragments("CC(=O)Oc1ccccc1C(=O)O").summary()
    for key in ("smiles", "molecular_mass", "n_fragments", "fragments"):
        assert key in s
    assert s["fragments"][0]["mz"] >= s["fragments"][-1]["mz"]  # desc order


def test_alkane_only_emits_m_plus():
    """A plain alkane (no functional groups except C-H) should still at
    least emit M+ and usually a methyl loss."""
    from orgchem.core.ms_fragments import predict_fragments
    r = predict_fragments("CCCCCC")  # hexane
    assert r.fragments[0].label == "M+"


# ---- Agent action ----------------------------------------------------

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_predict_ms_fragments_action(app):
    r = app.call("predict_ms_fragments", smiles="OC(=O)c1ccccc1")  # benzoic
    assert "error" not in r
    labels = [f["label"] for f in r["fragments"]]
    assert "M+" in labels
    assert "COOH" in labels


def test_predict_ms_fragments_bad_smiles(app):
    r = app.call("predict_ms_fragments", smiles="not_smiles")
    assert "error" in r
