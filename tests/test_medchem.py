"""Tests for Phase 19b (drug-likeness) and Phase 15b (TLC/Rf)."""
from __future__ import annotations
import os
import pytest

pytest.importorskip("rdkit")


# ---- Drug-likeness ---------------------------------------------------

def test_lipinski_ibuprofen_passes():
    from orgchem.core.druglike import lipinski
    r = lipinski("CC(C)Cc1ccc(cc1)C(C)C(=O)O")
    assert r["passes"] is True
    assert r["n_violations"] == 0


def test_lipinski_violates_for_large_molecule():
    """Cyclosporine A — classic Lipinski violator."""
    from orgchem.core.druglike import lipinski
    cya = ("CC[C@H](C)[C@@H]1[NH]C(=O)[C@H](C(C)C)N(C)C(=O)[C@H](CC(C)C)"
           "N(C)C(=O)[C@H](CC(C)C)N(C)C(=O)C[C@@H]([NH]...)")  # short invalid
    # Use a simpler known violator instead
    r = lipinski(
        "CCCCCCCCCCCCCCCCCCCCCC(=O)OCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCO")
    assert r["passes"] is False


def test_veber_basic():
    from orgchem.core.druglike import veber
    r = veber("CC(C)Cc1ccc(cc1)C(C)C(=O)O")
    assert r["passes"] is True


def test_pains_clean_molecule():
    from orgchem.core.druglike import pains
    r = pains("CC(=O)Oc1ccccc1C(=O)O")  # aspirin — PAINS-clean
    assert r["passes"] is True
    assert r["n_matches"] == 0


def test_qed_range():
    """QED is in [0, 1]; a drug-like molecule should score > 0.4."""
    from orgchem.core.druglike import qed_score
    s = qed_score("CC(C)Cc1ccc(cc1)C(C)C(=O)O")  # ibuprofen
    assert 0.0 <= s <= 1.0
    assert s > 0.4


def test_drug_likeness_report_complete():
    from orgchem.core.druglike import drug_likeness_report
    r = drug_likeness_report("CC(=O)Oc1ccccc1C(=O)O")
    for key in ("lipinski", "veber", "ghose", "pains", "qed"):
        assert key in r


# ---- TLC / Rf --------------------------------------------------------

def test_solvent_polarity_lookup():
    from orgchem.core.chromatography import solvent_polarity
    assert solvent_polarity("hexane") == 0.0
    assert solvent_polarity("methanol") == pytest.approx(0.95)


def test_solvent_polarity_mixture():
    from orgchem.core.chromatography import solvent_polarity
    # 1:1 hexane:EA → (0 + 0.58) / 2 = 0.29
    assert solvent_polarity("hexane:ethyl_acetate:1:1") == pytest.approx(0.29)
    # 3:1 hex:EA → (0*3 + 0.58*1)/4 = 0.145
    assert solvent_polarity("hexane:ethyl_acetate:3:1") == pytest.approx(0.145)


def test_predict_rf_ordering_non_polar_vs_polar():
    """In any solvent system, the hydrocarbon should have higher Rf than an alcohol."""
    from orgchem.core.chromatography import predict_rf
    hex_rf = predict_rf("CCCCCCCC", "hexane:ethyl_acetate:1:1")["rf"]
    ol_rf = predict_rf("CCCCCCCCO", "hexane:ethyl_acetate:1:1")["rf"]
    assert hex_rf > ol_rf


def test_increasing_solvent_polarity_pushes_everything_up():
    """More polar solvent → higher Rf for the same compound."""
    from orgchem.core.chromatography import predict_rf
    low = predict_rf("CCCCCCCCO", "hexane")["rf"]
    high = predict_rf("CCCCCCCCO", "ethyl_acetate")["rf"]
    assert high > low


def test_rf_bounded_in_open_interval():
    from orgchem.core.chromatography import predict_rf
    for smi in ("CCCCCCCCCCCCCCCC", "OC(=O)C(O)C(O)C(O)C(O)CO"):
        r = predict_rf(smi, "hexane:ethyl_acetate:1:1")
        assert 0.0 < r["rf"] < 1.0


def test_simulate_tlc_sorts_by_rf():
    from orgchem.core.chromatography import simulate_tlc
    r = simulate_tlc(["CCO", "CCCCCCCCCC", "CC(=O)O", "c1ccccc1"],
                     "hexane:ethyl_acetate:1:1")
    rfs = [c["rf"] for c in r["compounds"]]
    assert rfs == sorted(rfs, reverse=True)


def test_predict_rf_bad_smiles():
    from orgchem.core.chromatography import predict_rf
    r = predict_rf("not a molecule")
    assert "error" in r


# ---- Agent actions ---------------------------------------------------

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_drug_likeness_action_by_smiles(app):
    r = app.call("drug_likeness", smiles="CC(C)Cc1ccc(cc1)C(C)C(=O)O")
    assert "error" not in r
    assert "lipinski" in r
    assert r["lipinski"]["passes"] is True
    assert 0 <= r["qed"] <= 1


def test_drug_likeness_by_db_id(app):
    mols = app.call("list_all_molecules", filter="Aspirin")
    assert mols
    r = app.call("drug_likeness", molecule_id=mols[0]["id"])
    assert "error" not in r
    assert r["name"] == "Aspirin"


def test_drug_likeness_missing_input(app):
    r = app.call("drug_likeness")
    assert "error" in r


def test_predict_tlc_action(app):
    r = app.call("predict_tlc",
                 smiles_list=["CCCCCC", "CCO", "CC(=O)O"],
                 solvent="hexane:ethyl_acetate:1:1")
    assert "compounds" in r
    assert len(r["compounds"]) == 3


def test_predict_rf_action(app):
    r = app.call("predict_rf", smiles="c1ccccc1", solvent="hexane")
    assert "rf" in r
    assert 0 < r["rf"] < 1
