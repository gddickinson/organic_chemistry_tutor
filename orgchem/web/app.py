"""FastAPI web app for OrgChem Studio: serves the front end in static/ and the JSON API under /api.

Run with `python run_web.py` (http://127.0.0.1:8131, local only). `scripts/build_static.py` exports every path in
static_endpoints() to JSON for the GitHub Pages site. All content is the desktop app's own: seeded molecules,
reactions, mechanisms, energy profiles, synthesis pathways and glossary (orgchem/db/seed*.py, via chemdata.py),
tutorial lessons (orgchem/tutorial), and descriptors / tags computed by orgchem/core with RDKit.
"""
from functools import lru_cache
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from orgchem.web import chemdata, depict, lessons, quiz

STATIC = Path(__file__).resolve().parent / "static"

app = FastAPI(title="OrgChem Studio")
app.mount("/static", StaticFiles(directory=STATIC), name="static")


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(STATIC / "index.html")


@app.get("/api/info")
def info():
    """Counts for the home page."""
    s = chemdata.snapshot()
    lv = {}
    for le in lessons.lesson_index():
        lv[le["level"]] = lv.get(le["level"], 0) + 1
    return {"title": "OrgChem Studio", "molecules": len(s["molecules"]), "reactions": len(s["reactions"]),
            "mechanisms": sum(1 for r in s["reactions"] if r["mechanism"]),
            "energy_profiles": sum(1 for r in s["reactions"] if r["energy_profile"]),
            "pathways": len(s["pathways"]), "glossary": len(s["glossary"]),
            "lessons": sum(lv.values()), "lesson_levels": lv, "quiz": quiz.bank()["counts"]}


@app.get("/api/lessons")
def lesson_list():
    return lessons.lesson_index()


@app.get("/api/lessons/{level}/{stem}")
def lesson_page(level: str, stem: str):
    le = lessons.lesson(f"{level}/{stem}")
    if le is None:
        raise HTTPException(404, "no such lesson")
    return le


@app.get("/api/molecules")
def molecule_list():
    """Browse list (no coordinates): id, name, formula, MW, source group, functional-group tags."""
    return [{"id": m["id"], "name": m["name"], "formula": m["formula"], "source": m["source"],
             "mw": m["properties"].get("mol_weight"), "tags": m["tags"], "smiles": m["smiles"],
             "synonyms": m["synonyms"][:4]} for m in chemdata.snapshot()["molecules"]]


@lru_cache(maxsize=None)
def _molecule_detail(mid: int):
    from orgchem.core.descriptors import compute_all
    from orgchem.core.formats import mol_from_smiles
    from orgchem.core.molecule_tags import auto_tag
    m = chemdata.molecule(mid)
    if m is None:
        return None
    rd = mol_from_smiles(m["smiles"])
    out = {k: v for k, v in m.items() if k != "molblock_2d"}
    out.update(descriptors=compute_all(rd), auto_tags=auto_tag(rd).to_dict(),
               d2=depict.depict_molblock(m["molblock_2d"], m["smiles"]), d3=depict.coords_3d(m["smiles"]),
               source_label=chemdata.SOURCE_LABELS.get(m["source"], m["source"]))
    return out


@app.get("/api/molecules/{mid}")
def molecule_page(mid: int):
    d = _molecule_detail(mid)
    if d is None:
        raise HTTPException(404, "no such molecule")
    return d


@app.get("/api/reactions")
def reaction_list():
    return [{"id": r["id"], "name": r["name"], "category": r["category"], "short": quiz.short_reaction_name(r["name"]),
             "mechanism_steps": len(r["mechanism"]["steps"]) if r["mechanism"] else 0,
             "has_profile": bool(r["energy_profile"])} for r in chemdata.snapshot()["reactions"]]


@lru_cache(maxsize=None)
def _reaction_detail(rid: int):
    r = chemdata.reaction(rid)
    if r is None:
        return None
    out = dict(r, scheme=quiz.scheme(r["reaction_smiles"]))
    if r["mechanism"]:
        out["mechanism"] = dict(r["mechanism"], steps=[dict(st, d2=depict.depict_smiles(st["smiles"]))
                                                       for st in r["mechanism"]["steps"]])
    try:
        from orgchem.core.green_metrics import atom_economy
        out["atom_economy"] = atom_economy(r["reaction_smiles"])
    except Exception:  # noqa: BLE001 - some schemes (e.g. bare metals) have no defined atom economy
        out["atom_economy"] = None
    return out


@app.get("/api/reactions/{rid}")
def reaction_page(rid: int):
    d = _reaction_detail(rid)
    if d is None:
        raise HTTPException(404, "no such reaction")
    return d


@app.get("/api/pathways")
def pathway_list():
    return [{k: p[k] for k in ("id", "name", "target_name", "category", "source")} | {"n_steps": len(p["steps"])}
            for p in chemdata.snapshot()["pathways"]]


@app.get("/api/pathways/{pid}")
def pathway_page(pid: int):
    p = chemdata.pathway(pid)
    if p is None:
        raise HTTPException(404, "no such pathway")
    return dict(p, steps=[dict(st, scheme=quiz.scheme(st["reaction_smiles"])) for st in p["steps"]],
                target=depict.depict_smiles(p["target_smiles"]) if p["target_smiles"] else None)


@app.get("/api/glossary")
def glossary():
    return chemdata.snapshot()["glossary"]


@app.get("/api/quiz")
def quiz_bank():
    return quiz.bank()


class SmilesIn(BaseModel):
    smiles: str


@app.post("/api/depict")
def depict_any(body: SmilesIn):
    """Local app only: draw any SMILES (RDKit 2D + 3D) with the app's descriptors and functional-group tags."""
    from orgchem.core.descriptors import compute_all
    from orgchem.core.molecule_tags import auto_tag
    from rdkit import Chem
    mol = Chem.MolFromSmiles(body.smiles.strip())
    if mol is None:
        raise HTTPException(422, "RDKit could not parse that SMILES")
    return {"d2": depict.depict_smiles(body.smiles.strip()), "d3": depict.coords_3d(body.smiles.strip()),
            "descriptors": compute_all(mol), "auto_tags": auto_tag(mol).to_dict(),
            "canonical": Chem.MolToSmiles(mol)}


def static_endpoints() -> list:
    """GET paths (without /api) written to the static site as api/<path>.json."""
    s = chemdata.snapshot()
    return (["/info", "/lessons", "/molecules", "/reactions", "/pathways", "/glossary", "/quiz"]
            + [f"/lessons/{le['slug']}" for le in lessons.lesson_index()]
            + [f"/molecules/{m['id']}" for m in s["molecules"]]
            + [f"/reactions/{r['id']}" for r in s["reactions"]]
            + [f"/pathways/{p['id']}" for p in s["pathways"]])


# Seeds the private snapshot DB on import (a few seconds); the build and test scripts need the full list.
STATIC_ENDPOINTS = static_endpoints()
