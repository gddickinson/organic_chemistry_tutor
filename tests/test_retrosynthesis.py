"""Tests for Phase 8d — retrosynthesis template matcher."""
from __future__ import annotations
import os
import pytest

pytest.importorskip("rdkit")


# ---- Core engine -----------------------------------------------------

def test_catalogue_has_all_core_disconnections():
    from orgchem.core.retrosynthesis import RETRO_TEMPLATES
    ids = {t.id for t in RETRO_TEMPLATES}
    for required in ("retro-ester", "retro-amide", "retro-suzuki-biaryl",
                     "retro-williamson-ether", "retro-aldol",
                     "retro-diels-alder", "retro-nitration",
                     "retro-reductive-amination"):
        assert required in ids


def test_aspirin_ester_disconnection():
    """Aspirin ⇒ acetic acid + salicylic acid (Fischer-ester retro)."""
    from orgchem.core.retrosynthesis import find_retrosynthesis
    r = find_retrosynthesis("CC(=O)Oc1ccccc1C(=O)O")
    proposals = r["proposals"]
    ester_hits = [p for p in proposals if p["template_id"] == "retro-ester"]
    assert ester_hits
    precursors = set(ester_hits[0]["precursors"])
    assert "CC(=O)O" in precursors
    assert "O=C(O)c1ccccc1O" in precursors


def test_paracetamol_amide_disconnection():
    """Paracetamol ⇒ acetic acid + 4-aminophenol (amide retro)."""
    from orgchem.core.retrosynthesis import find_retrosynthesis
    r = find_retrosynthesis("CC(=O)Nc1ccc(O)cc1")
    hits = [p for p in r["proposals"] if p["template_id"] == "retro-amide"]
    assert hits
    precursors = set(hits[0]["precursors"])
    assert "CC(=O)O" in precursors
    assert "Nc1ccc(O)cc1" in precursors


def test_biphenyl_suzuki_disconnection():
    """Biphenyl ⇒ bromobenzene + phenylboronic acid (Suzuki retro)."""
    from orgchem.core.retrosynthesis import find_retrosynthesis
    r = find_retrosynthesis("c1ccc(-c2ccccc2)cc1")
    hits = [p for p in r["proposals"] if p["template_id"] == "retro-suzuki-biaryl"]
    assert hits
    pre = set(hits[0]["precursors"])
    assert "Brc1ccccc1" in pre
    assert "OB(O)c1ccccc1" in pre


def test_nitrobenzene_retro_nitration():
    """PhNO2 ⇒ benzene + HNO3."""
    from orgchem.core.retrosynthesis import find_retrosynthesis
    r = find_retrosynthesis("[O-][N+](=O)c1ccccc1")
    hits = [p for p in r["proposals"] if p["template_id"] == "retro-nitration"]
    assert hits


def test_cyclohexane_has_no_disconnections():
    """A plain alkane shouldn't match any retro template."""
    from orgchem.core.retrosynthesis import find_retrosynthesis
    r = find_retrosynthesis("C1CCCCC1")
    assert r["n_proposals"] == 0


def test_bad_smiles_returns_error():
    from orgchem.core.retrosynthesis import find_retrosynthesis
    r = find_retrosynthesis("not a molecule")
    assert "error" in r


def test_aldol_retro_on_beta_hydroxy_ketone():
    """4-hydroxy-4-methylpentan-2-one (diacetone alcohol) ⇒ 2 × acetone."""
    from orgchem.core.retrosynthesis import find_retrosynthesis
    r = find_retrosynthesis("CC(=O)CC(O)(C)C")
    hits = [p for p in r["proposals"] if p["template_id"] == "retro-aldol"]
    assert hits, "aldol retro should fire on a β-hydroxy ketone"


def test_n_proposals_is_consistent():
    from orgchem.core.retrosynthesis import find_retrosynthesis
    r = find_retrosynthesis("CC(=O)Oc1ccccc1C(=O)O")
    assert r["n_proposals"] == len(r["proposals"])


# ---- Agent actions --------------------------------------------------

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_find_retrosynthesis_action(app):
    r = app.call("find_retrosynthesis",
                 target_smiles="CC(=O)Oc1ccccc1C(=O)O")
    assert "error" not in r
    assert r["n_proposals"] >= 1


def test_list_retro_templates_action(app):
    rows = app.call("list_retro_templates")
    assert len(rows) >= 8
    assert any(r["id"] == "retro-ester" for r in rows)


def test_bad_target_via_action(app):
    r = app.call("find_retrosynthesis", target_smiles="not_a_molecule")
    assert "error" in r


# ---- Multi-step recursion (Phase 8d follow-up) ----------------------

def test_multi_step_aspirin_depth_2():
    """Aspirin at depth 2 should split to acetic acid + salicylic acid
    (step 1), and salicylic acid (which has no further disconnection in
    our template set) should end up terminal."""
    from orgchem.core.retrosynthesis import find_multi_step_retrosynthesis
    r = find_multi_step_retrosynthesis("CC(=O)Oc1ccccc1C(=O)O",
                                       max_depth=2, max_branches=2,
                                       top_paths=10)
    assert "error" not in r
    assert r["tree"]["smiles"] == "CC(=O)Oc1ccccc1C(=O)O"
    assert r["paths"]


def test_multi_step_terminates_on_simple_precursor():
    """A small target (≤8 heavy atoms) should be 'terminal' immediately."""
    from orgchem.core.retrosynthesis import find_multi_step_retrosynthesis
    r = find_multi_step_retrosynthesis("CCO", max_depth=3)
    # CCO is 3 heavy atoms → _is_simple_precursor returns True → terminal tree
    assert r["tree"]["terminal"] is True


def test_multi_step_bad_smiles_returns_error():
    from orgchem.core.retrosynthesis import find_multi_step_retrosynthesis
    r = find_multi_step_retrosynthesis("not_a_molecule", max_depth=2)
    assert "error" in r


def test_multi_step_depth_zero_errors():
    from orgchem.core.retrosynthesis import find_multi_step_retrosynthesis
    r = find_multi_step_retrosynthesis("CC(=O)Oc1ccccc1C(=O)O", max_depth=0)
    assert "error" in r


def test_multi_step_action(app):
    """Agent layer smoke test."""
    r = app.call("find_multi_step_retrosynthesis",
                 target_smiles="CC(=O)Oc1ccccc1C(=O)O",
                 max_depth=2, max_branches=2, top_paths=5)
    assert "error" not in r
    assert r["max_depth"] == 2
    assert "tree" in r and "paths" in r
