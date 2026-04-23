"""Tests for Phase 14b — Woodward-Hoffmann rules catalogue."""
from __future__ import annotations
import os
import pytest

pytest.importorskip("rdkit")


# ---- Core catalogue -------------------------------------------------

def test_catalogue_size():
    from orgchem.core.wh_rules import RULES
    assert len(RULES) >= 15


def test_rule_ids_unique():
    from orgchem.core.wh_rules import RULES
    ids = [r.id for r in RULES]
    assert len(ids) == len(set(ids))


def test_all_families_covered():
    from orgchem.core.wh_rules import rule_families
    fams = set(rule_families())
    for f in ("cycloaddition", "electrocyclic", "sigmatropic", "general"):
        assert f in fams


def test_list_rules_filter():
    from orgchem.core.wh_rules import list_rules
    cyclo = list_rules(family="cycloaddition")
    assert all(r["family"] == "cycloaddition" for r in cyclo)
    assert len(cyclo) >= 4


def test_get_rule_known():
    from orgchem.core.wh_rules import get_rule
    r = get_rule("cyclo-4plus2-thermal")
    assert "error" not in r
    assert "Diels-Alder" in r["description_md"]
    assert r["outcome"].startswith("allowed")


def test_get_rule_missing():
    from orgchem.core.wh_rules import get_rule
    r = get_rule("nope")
    assert "error" in r


# ---- check_allowed engine ------------------------------------------

def test_diels_alder_thermal_allowed():
    from orgchem.core.wh_rules import check_allowed
    r = check_allowed("cycloaddition", 6, "thermal")
    assert r["allowed"] is True


def test_2_plus_2_thermal_forbidden():
    from orgchem.core.wh_rules import check_allowed
    r = check_allowed("cycloaddition", 4, "thermal")
    assert r["allowed"] is False


def test_2_plus_2_photochemical_allowed():
    from orgchem.core.wh_rules import check_allowed
    r = check_allowed("cycloaddition", 4, "photochemical")
    assert r["allowed"] is True


def test_6pi_electrocyclic_thermal_is_disrotatory():
    from orgchem.core.wh_rules import check_allowed
    r = check_allowed("electrocyclic", 6, "thermal")
    assert r["geometry"] == "disrotatory"


def test_4pi_electrocyclic_thermal_is_conrotatory():
    from orgchem.core.wh_rules import check_allowed
    r = check_allowed("electrocyclic", 4, "thermal")
    assert r["geometry"] == "conrotatory"


def test_photochemical_flips_electrocyclic_rotation():
    from orgchem.core.wh_rules import check_allowed
    r = check_allowed("electrocyclic", 6, "photochemical")
    assert r["geometry"] == "conrotatory"


def test_3_3_sigmatropic_thermal_allowed():
    from orgchem.core.wh_rules import check_allowed
    r = check_allowed("sigmatropic", 6, "thermal")
    assert r["allowed"] is True


def test_1_3_h_sigmatropic_thermal_forbidden():
    from orgchem.core.wh_rules import check_allowed
    r = check_allowed("sigmatropic", 4, "thermal")
    assert r["allowed"] is False


def test_check_allowed_rejects_bogus_inputs():
    from orgchem.core.wh_rules import check_allowed
    assert "error" in check_allowed("not a thing", 6)
    assert "error" in check_allowed("cycloaddition", 6, "flashbulb")
    assert "error" in check_allowed("cycloaddition", 1)


# ---- Agent actions ---------------------------------------------------

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_list_wh_rules_action(app):
    rows = app.call("list_wh_rules")
    assert len(rows) >= 15


def test_list_wh_rules_filter_action(app):
    rows = app.call("list_wh_rules", family="electrocyclic")
    assert rows
    assert all(r["family"] == "electrocyclic" for r in rows)


def test_get_wh_rule_action(app):
    r = app.call("get_wh_rule", rule_id="electro-6pi-thermal")
    assert "error" not in r
    assert "disrotatory" in r["outcome"]


def test_check_wh_allowed_action_diels_alder(app):
    r = app.call("check_wh_allowed",
                 kind="cycloaddition", electron_count=6, regime="thermal")
    assert r["allowed"] is True


def test_check_wh_allowed_action_4n_electrocyclic(app):
    r = app.call("check_wh_allowed",
                 kind="electrocyclic", electron_count=4)
    assert r["geometry"] == "conrotatory"
