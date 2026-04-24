"""Round-62 regression tests: bromination of ethene + Friedel-Crafts
alkylation mechanisms land in the seeded ``_MECH_MAP`` with the
expected step counts and arrow patterns.  Also pins the Phase 31c
total at 20 mechanisms.
"""
from __future__ import annotations

import pytest
from rdkit import Chem


def test_round62_mechanisms_registered():
    from orgchem.db.seed_mechanisms import _MECH_MAP

    assert "Bromination of ethene" in _MECH_MAP
    assert "Friedel-Crafts alkylation" in _MECH_MAP


def test_mech_map_has_20_entries():
    """Phase 31c target is 20 multi-step mechanisms."""
    from orgchem.db.seed_mechanisms import _MECH_MAP

    assert len(_MECH_MAP) == 20


def test_bromination_ethene_three_steps():
    from orgchem.db.seed_mechanisms_extra import _bromination_ethene

    mech = _bromination_ethene()
    assert len(mech.steps) == 3
    # Step 1: two arrows (π attack + Br-Br heterolysis).
    assert len(mech.steps[0].arrows) == 2
    # Step 2: backside attack + ring opening + lone-pair dot on Br⁻.
    assert len(mech.steps[1].arrows) == 2
    assert mech.steps[1].lone_pairs == [3]
    # Final step is the anti-addition product.
    assert mech.steps[2].smiles == "BrCCBr"


def test_friedel_crafts_three_steps():
    from orgchem.db.seed_mechanisms_extra import _friedel_crafts_alkylation

    mech = _friedel_crafts_alkylation()
    assert len(mech.steps) == 3
    # Step 1 activation: Cl lone pair + C-Cl breakage.
    assert len(mech.steps[0].arrows) == 2
    assert mech.steps[0].lone_pairs == [1]
    # Step 2 forms the Wheland intermediate.
    assert len(mech.steps[1].arrows) == 1
    # Step 3 product: toluene + HCl + AlCl3.
    prods = mech.steps[2].smiles
    assert "Cc1ccccc1" in prods
    assert "Al" in prods
    assert "Cl" in prods


@pytest.mark.parametrize(
    "builder_name",
    ["_bromination_ethene", "_friedel_crafts_alkylation"],
)
def test_round62_smiles_parse_and_arrows_in_range(builder_name):
    """Every arrow + lone-pair index must fit its step's atom count."""
    from orgchem.db import seed_mechanisms_extra

    mech = getattr(seed_mechanisms_extra, builder_name)()
    for i, step in enumerate(mech.steps):
        if not step.smiles:
            continue
        mol = Chem.MolFromSmiles(step.smiles)
        assert mol is not None, f"step {i}: bad SMILES {step.smiles!r}"
        nat = mol.GetNumAtoms()
        for arrow in step.arrows:
            for idx in (arrow.from_atom, arrow.to_atom):
                if idx is not None:
                    assert 0 <= idx < nat
        for lp in step.lone_pairs:
            assert 0 <= lp < nat


def test_seed_version_bumped_to_11():
    """Round 62 bumps SEED_VERSION so existing DBs pick up the new
    two mechanisms + any label tweaks on upgrade."""
    from orgchem.db.seed_mechanisms import SEED_VERSION

    assert SEED_VERSION >= 11
