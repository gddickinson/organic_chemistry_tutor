"""Web interface tests: every exported endpoint answers, the static build is complete, and the JS engine tests pass.

Run: python -m pytest -q tests/test_web.py
"""
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from orgchem.web.app import STATIC, STATIC_ENDPOINTS, app  # noqa: E402

client = TestClient(app)


def test_index_served():
    r = client.get("/")
    assert r.status_code == 200 and "static/main.js" in r.text


@pytest.mark.parametrize("path", STATIC_ENDPOINTS)
def test_endpoint(path):
    r = client.get("/api" + path)
    assert r.status_code == 200, r.text
    assert r.json() is not None


def test_static_build(tmp_path):
    sys.path.insert(0, str(ROOT / "scripts"))
    import build_static
    build_static.build(tmp_path / "site")
    assert (tmp_path / "site" / "index.html").read_text().count("APP_STATIC") == 1
    for path in STATIC_ENDPOINTS:
        assert (tmp_path / "site" / "api" / (path.strip("/") + ".json")).exists()


def test_static_assets_referenced_exist():
    html = (STATIC / "index.html").read_text()
    for name in ("style.css", "main.js"):
        assert f"static/{name}" in html and (STATIC / name).exists()


@pytest.mark.skipif(not shutil.which("node"), reason="node not installed")
def test_js_engine():
    tests = sorted(STATIC.glob("*.test.mjs"))
    for t in tests:
        r = subprocess.run(["node", str(t)], capture_output=True, text=True)
        assert r.returncode == 0, r.stdout + r.stderr


# --- OrgChem-specific API tests ---------------------------------------------------------------------------------

def test_info_counts_match_seed():
    s = client.get("/api/info").json()
    assert s["molecules"] > 400 and s["reactions"] >= 37 and s["mechanisms"] >= 20 and s["lessons"] >= 200
    assert sum(s["lesson_levels"].values()) == s["lessons"]


def test_snapshot_never_touches_user_db():
    """The web app seeds a private temp DB and restores whatever DB engine was active before."""
    from orgchem.db import session as dbsession
    from orgchem.web import chemdata
    before = (dbsession._engine, dbsession._SessionLocal)
    snap = chemdata.snapshot.__wrapped__()  # uncached run
    assert snap["molecules"] and (dbsession._engine, dbsession._SessionLocal) == before


def test_lesson_glossary_links_are_routes():
    idx = client.get("/api/lessons").json()
    htmls = [client.get("/api/lessons/" + le["slug"]).json()["html"] for le in idx[:80]]
    assert any('href="#/glossary/' in h for h in htmls)
    assert not any("orgchem-glossary:" in h for h in htmls)


def test_mechanism_arrows_index_existing_atoms():
    """Every curly arrow / lone pair points at an atom of its step's drawing (atom order = SMILES order)."""
    for r in client.get("/api/reactions").json():
        if not r["mechanism_steps"]:
            continue
        for st in client.get(f"/api/reactions/{r['id']}").json()["mechanism"]["steps"]:
            n = len(st["d2"]["a"])
            for a in st["arrows"]:
                ends = [a["from_atom"], a["to_atom"]] + list(a["from_bond"] or []) + list(a["to_bond"] or [])
                assert all(0 <= i < n for i in ends), (r["name"], st["title"])
            assert all(0 <= i < n for i in st["lone_pairs"])


def test_molecule_detail_uses_app_descriptors():
    from rdkit import Chem
    from orgchem.core.descriptors import compute_all
    m = next(x for x in client.get("/api/molecules").json() if x["name"] == "Caffeine")
    d = client.get(f"/api/molecules/{m['id']}").json()
    assert d["descriptors"]["formula"] == "C8H10N4O2"
    assert d["descriptors"] == pytest.approx(compute_all(Chem.MolFromSmiles(d["smiles"])))
    assert d["d3"] and any(a[0] == "H" for a in d["d3"]["a"])  # explicit-H 3D conformer


def test_quiz_answers_come_from_data():
    from orgchem.core.molecule_tags import auto_tag
    from orgchem.web.quiz import pretty_group
    bank = client.get("/api/quiz").json()
    mols = {m["name"]: m for m in client.get("/api/molecules").json()}
    for q in bank["questions"]:
        assert q["answer"] in q["options"] and len(set(q["options"])) == len(q["options"])
        if q["kind"] == "formula":
            name = q["prompt"].split(" of ", 1)[1].rstrip("?")
            assert mols[name]["formula"] == q["answer"]
        if q["kind"] == "group":
            name = q["prompt"].split(" does ", 1)[1].rsplit(" contain", 1)[0]
            groups = [pretty_group(g) for g in auto_tag(mols[name]["smiles"]).functional_groups]
            assert q["answer"] in groups and all(o == q["answer"] or o not in groups for o in q["options"])


def test_depict_post_local_only():
    r = client.post("/api/depict", json={"smiles": "CC(=O)O"})
    assert r.status_code == 200 and r.json()["descriptors"]["formula"] == "C2H4O2"
    assert client.post("/api/depict", json={"smiles": "C1CC"}).status_code == 422


def test_chem_fixture_is_current():
    """tests/fixtures/chem_engine_fixture.json still matches RDKit + the seed data (rerun make_chem_fixture.py)."""
    import json
    sys.path.insert(0, str(ROOT / "scripts"))
    import make_chem_fixture
    old = json.loads((ROOT / "tests" / "fixtures" / "chem_engine_fixture.json").read_text())
    new = make_chem_fixture.build()
    assert [m["smiles"] for m in old["molecules"]] == [m["smiles"] for m in new["molecules"]]
    for a, b in zip(old["molecules"], new["molecules"]):
        assert (a.get("atoms"), a.get("formula"), a.get("groups")) == (b.get("atoms"), b.get("formula"), b.get("groups"))
        if "mw" in a:
            assert a["mw"] == pytest.approx(b["mw"], rel=1e-9) and a["exact"] == pytest.approx(b["exact"], rel=1e-9)
    assert len(old["formula"]) == len(new["formula"])
    for a, b in zip(old["formula"], new["formula"]):
        assert (a.get("empirical"), a.get("molecular"), a.get("error")) == (b.get("empirical"), b.get("molecular"), b.get("error"))
        if "empirical_mass" in a:
            assert a["empirical_mass"] == pytest.approx(b["empirical_mass"], rel=1e-9)
