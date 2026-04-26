"""Phase 43 (round 151) — headless tests for the cell-component
explorer + agent actions + dialog.
"""
from __future__ import annotations
import os

import pytest


# ==================================================================
# Catalogue contents
# ==================================================================

def test_catalogue_size_at_least_thirty_five():
    from orgchem.core.cell_components import list_components
    assert len(list_components()) >= 35


def test_all_three_domains_represented():
    from orgchem.core.cell_components import (
        DOMAINS, list_components,
    )
    seen = {c.domain for c in list_components()}
    assert seen == set(DOMAINS), \
        f"missing: {set(DOMAINS) - seen}"


def test_eukarya_has_substantial_coverage():
    """Eukarya is the focus, should have ≥ 20 entries
    (membranes / organelles / nuclear / cytoskeleton)."""
    from orgchem.core.cell_components import list_components
    assert len(list_components(domain="eukarya")) >= 20


def test_bacteria_has_required_components():
    from orgchem.core.cell_components import list_components
    ids = {c.id for c in list_components(domain="bacteria")}
    for must_have in ("bacterial-plasma-membrane",
                      "peptidoglycan-gram-positive",
                      "peptidoglycan-gram-negative",
                      "outer-membrane-gram-negative",
                      "bacterial-nucleoid",
                      "bacterial-flagellum",
                      "70s-ribosome"):
        assert must_have in ids, f"missing {must_have}"


def test_archaea_has_required_components():
    """Archaea: the unique features are the ether lipids + "
    pseudopeptidoglycan + S-layer + archaellum."""
    from orgchem.core.cell_components import list_components
    ids = {c.id for c in list_components(domain="archaea")}
    for must_have in ("archaeal-plasma-membrane",
                      "pseudopeptidoglycan",
                      "s-layer",
                      "archaeal-ribosome",
                      "archaeal-flagellum"):
        assert must_have in ids, f"missing {must_have}"


def test_user_requested_components_present():
    """The user-flagged catalogue brief explicitly named these."""
    from orgchem.core.cell_components import find_components
    for needle in ("plasma membrane", "nuclear envelope",
                   "endoplasmic reticulum", "Golgi",
                   "mitochondrion", "chloroplast",
                   "lysosome", "peroxisome", "ribosome",
                   "nucleolus", "chromatin", "telomere",
                   "centrosome", "actin", "microtubule",
                   "intermediate filament", "cilium",
                   "extracellular matrix", "plant cell wall",
                   "fungal cell wall", "peptidoglycan",
                   "outer membrane", "bacterial flagellum",
                   "pilus", "capsule", "biofilm",
                   "ether-linked"):
        hits = find_components(needle)
        assert hits, f"no component hit for needle {needle!r}"


def test_every_entry_has_required_fields():
    from orgchem.core.cell_components import list_components
    for c in list_components():
        for fname in ("id", "name", "domain", "category",
                      "location", "function"):
            assert getattr(c, fname), \
                f"missing {fname} on {c.id}"
        assert c.constituents, \
            f"empty constituents on {c.id}"


def test_every_id_unique():
    from orgchem.core.cell_components import list_components
    ids = [c.id for c in list_components()]
    assert len(ids) == len(set(ids)), \
        f"duplicate ids: {[i for i in ids if ids.count(i) > 1]}"


def test_every_id_lowercase_kebab():
    from orgchem.core.cell_components import list_components
    import re
    pat = re.compile(r"^[a-z0-9][a-z0-9-]*$")
    for c in list_components():
        assert pat.match(c.id), f"bad id {c.id!r}"


def test_every_domain_in_canonical_set():
    from orgchem.core.cell_components import (
        DOMAINS, list_components,
    )
    dset = set(DOMAINS)
    for c in list_components():
        assert c.domain in dset, \
            f"unknown domain {c.domain!r} on {c.id}"


def test_every_sub_domain_in_canonical_set():
    from orgchem.core.cell_components import (
        SUB_DOMAINS, list_components,
    )
    sset = set(SUB_DOMAINS)
    for c in list_components():
        for s in c.sub_domains:
            assert s in sset, \
                f"unknown sub-domain {s!r} on {c.id}"


def test_every_category_in_canonical_set():
    from orgchem.core.cell_components import (
        CATEGORIES, list_components,
    )
    cset = set(CATEGORIES)
    for c in list_components():
        assert c.category in cset, \
            f"unknown category {c.category!r} on {c.id}"


def test_every_constituent_has_role():
    from orgchem.core.cell_components import list_components
    for c in list_components():
        for m in c.constituents:
            assert m.name and m.role, \
                f"empty constituent on {c.id}: {m}"


# ---- Per-row teaching invariants ------------------------------

def test_eukaryotic_plasma_membrane_has_cholesterol():
    """Cholesterol is THE distinguishing feature of the
    animal plasma membrane vs bacterial."""
    from orgchem.core.cell_components import get_component
    pm = get_component("eukaryotic-plasma-membrane")
    names = " ".join(m.name for m in pm.constituents).lower()
    assert "cholesterol" in names


def test_bacterial_plasma_membrane_has_no_cholesterol():
    """Bacteria don't make cholesterol — they use hopanoids."""
    from orgchem.core.cell_components import get_component
    pm = get_component("bacterial-plasma-membrane")
    names = " ".join(m.name for m in pm.constituents).lower()
    assert "cholesterol" not in names
    assert "hopanoid" in names


def test_archaeal_membrane_has_ether_linked_lipids():
    """Ether-linked isoprenoid lipids are the defining
    archaeal feature — the lipid divide."""
    from orgchem.core.cell_components import get_component
    pm = get_component("archaeal-plasma-membrane")
    names = " ".join(m.name for m in pm.constituents).lower()
    assert "ether" in names
    assert "isoprenoid" in names


def test_mitochondrion_has_atp_synthase_and_etc():
    from orgchem.core.cell_components import get_component
    m = get_component("mitochondrion")
    names = " ".join(x.name for x in m.constituents).lower()
    assert "atp synthase" in names
    assert ("complex" in names or "electron transport"
            in m.function.lower())
    assert "mtdna" in names or "mitochondrial dna" in names \
        or "mtdna" in m.function.lower()


def test_chloroplast_only_in_plant():
    from orgchem.core.cell_components import get_component
    c = get_component("chloroplast")
    assert c.domain == "eukarya"
    assert "plant" in c.sub_domains


def test_chromatin_has_histone_octamer():
    from orgchem.core.cell_components import get_component
    c = get_component("chromatin")
    names = " ".join(m.name for m in c.constituents).lower()
    assert "histone" in names


def test_telomere_has_telomerase():
    from orgchem.core.cell_components import get_component
    c = get_component("telomere")
    names = " ".join(m.name for m in c.constituents).lower()
    assert "telomerase" in names


def test_lysosome_only_animal():
    from orgchem.core.cell_components import get_component
    c = get_component("lysosome")
    assert "animal" in c.sub_domains


def test_plant_cell_wall_has_cellulose():
    from orgchem.core.cell_components import get_component
    c = get_component("plant-cell-wall")
    assert "plant" in c.sub_domains
    names = " ".join(m.name for m in c.constituents).lower()
    assert "cellulose" in names


def test_fungal_cell_wall_has_chitin():
    from orgchem.core.cell_components import get_component
    c = get_component("fungal-cell-wall")
    assert "fungus" in c.sub_domains
    names = " ".join(m.name for m in c.constituents).lower()
    assert "chitin" in names


def test_peptidoglycan_gram_positive_has_pentaglycine_bridge():
    """The pentaglycine bridge is the defining structural
    feature of Staph cell wall."""
    from orgchem.core.cell_components import get_component
    c = get_component("peptidoglycan-gram-positive")
    names = " ".join(m.name for m in c.constituents).lower()
    assert "pentaglycine" in names or "glycine" in names


def test_outer_membrane_gram_negative_has_lps():
    """LPS / endotoxin is the defining outer-membrane
    component."""
    from orgchem.core.cell_components import get_component
    c = get_component("outer-membrane-gram-negative")
    names = " ".join(m.name for m in c.constituents).lower()
    assert "lipopolysaccharide" in names or "lps" in names


def test_pseudopeptidoglycan_has_l_amino_acids():
    """Defining archaeal feature: L-amino acids (vs D-AA in
    bacterial peptidoglycan), explains lysozyme + β-lactam
    resistance."""
    from orgchem.core.cell_components import get_component
    c = get_component("pseudopeptidoglycan")
    body = (c.notes + " "
            + " ".join(m.role for m in c.constituents)).lower()
    assert "l-amino" in body or "l-aa" in body \
        or "β-lactam" in body or "lysozyme" in body


def test_archaellum_distinct_from_bacterial_flagellum():
    from orgchem.core.cell_components import get_component
    c = get_component("archaeal-flagellum")
    body = (c.notes + " " + c.function).lower()
    assert "atp" in body
    # The archaellum is evolutionarily distinct — that's the
    # teaching point, not just a renamed bacterial flagellum.


def test_ribosomes_present_for_all_three_domains():
    """80S (eukarya) + 70S (bacteria) + archaeal 70S."""
    from orgchem.core.cell_components import (
        components_for_category,
    )
    ribo_domains = {c.domain
                    for c in components_for_category("ribosome")}
    assert ribo_domains == {"eukarya", "bacteria", "archaea"}


# ---- Cross-references to the molecule database ----------------

def test_constituents_with_xrefs_are_well_formed():
    """If a constituent has a cross-reference, it should be a
    non-trivial string (allows rot-detection later)."""
    from orgchem.core.cell_components import list_components
    for c in list_components():
        for m in c.constituents:
            if m.cross_reference_molecule_name:
                assert (len(m.cross_reference_molecule_name) >= 3
                        and m.cross_reference_molecule_name
                        == m.cross_reference_molecule_name.strip()), \
                    f"weird xref {m.cross_reference_molecule_name!r} " \
                    f"on {c.id}"


def test_xrefs_resolve_to_molecule_db(app):
    """Every cross-reference set on a constituent MUST resolve
    to an actual molecule-DB row — the xref field is meant
    to bridge the cell-component view to the canonical
    molecule database, so a stale xref breaks that bridge.
    Uses the ``app`` fixture so the DB is initialised."""
    from orgchem.core.cell_components import list_components
    from orgchem.db.queries import find_molecule_by_name
    failed = []
    total_xrefs = 0
    for c in list_components():
        for m in c.constituents:
            if not m.cross_reference_molecule_name:
                continue
            total_xrefs += 1
            row = find_molecule_by_name(
                m.cross_reference_molecule_name)
            if row is None:
                failed.append(
                    (c.id, m.name,
                     m.cross_reference_molecule_name))
    assert total_xrefs >= 1, \
        "no cross-references found — too lenient a baseline"
    assert not failed, \
        f"unresolved xrefs: {failed}"


# ---- Filter / lookup ------------------------------------------

def test_list_filtered_by_domain():
    from orgchem.core.cell_components import list_components
    bact = list_components("bacteria")
    assert all(c.domain == "bacteria" for c in bact)
    assert len(bact) >= 8


def test_list_filtered_by_sub_domain_includes_pan_domain():
    """Components with empty sub_domains (whole-domain
    applicability) should still surface for any sub-domain
    query within their domain — e.g. mitochondrion appears
    under sub_domain='animal'."""
    from orgchem.core.cell_components import list_components
    animal = list_components(domain="eukarya",
                             sub_domain="animal")
    ids = {c.id for c in animal}
    assert "mitochondrion" in ids   # pan-eukaryotic
    assert "lysosome" in ids        # animal-specific
    assert "chloroplast" not in ids   # plant-only


def test_list_filtered_by_sub_domain_plant():
    from orgchem.core.cell_components import list_components
    plant = list_components(domain="eukarya",
                            sub_domain="plant")
    ids = {c.id for c in plant}
    assert "chloroplast" in ids
    assert "plant-cell-wall" in ids
    assert "lysosome" not in ids   # animal-specific


def test_list_unknown_domain_returns_empty():
    from orgchem.core.cell_components import list_components
    assert list_components(domain="not-a-domain") == []


def test_list_unknown_sub_domain_returns_empty():
    from orgchem.core.cell_components import list_components
    assert list_components(sub_domain="not-a-sub") == []


def test_get_unknown_id_returns_none():
    from orgchem.core.cell_components import get_component
    assert get_component("does-not-exist") is None


def test_find_substring_case_insensitive():
    from orgchem.core.cell_components import find_components
    a = {c.id for c in find_components("MITOCHONDRION")}
    b = {c.id for c in find_components("mitochondrion")}
    assert a == b
    assert "mitochondrion" in a


def test_find_empty_returns_empty():
    from orgchem.core.cell_components import find_components
    assert find_components("") == []


def test_find_searches_constituent_names():
    """A search for 'cellulose' should find the plant cell
    wall (where it's a constituent), not just components
    named 'cellulose'."""
    from orgchem.core.cell_components import find_components
    hits = {c.id for c in find_components("cellulose")}
    assert "plant-cell-wall" in hits


def test_components_for_category():
    from orgchem.core.cell_components import (
        components_for_category,
    )
    organelles = components_for_category("organelle")
    assert len(organelles) >= 5
    ids = {c.id for c in organelles}
    assert "mitochondrion" in ids
    assert "lysosome" in ids


def test_components_for_unknown_category_empty():
    from orgchem.core.cell_components import (
        components_for_category,
    )
    assert components_for_category("not-a-category") == []


def test_canonical_tuples_round_trip():
    from orgchem.core.cell_components import (
        DOMAINS, SUB_DOMAINS, CATEGORIES,
        domains, sub_domains, categories,
    )
    assert domains() == DOMAINS
    assert sub_domains() == SUB_DOMAINS
    assert categories() == CATEGORIES


# ---- component_to_dict serialisation --------------------------

def test_component_to_dict_keys():
    from orgchem.core.cell_components import (
        component_to_dict, get_component,
    )
    d = component_to_dict(get_component("mitochondrion"))
    expected = {
        "id", "name", "domain", "sub_domains", "category",
        "location", "function", "constituents",
        "notable_diseases", "notes",
    }
    assert set(d.keys()) == expected
    # Constituents serialise as list-of-dicts, each with the
    # MolecularConstituent fields.
    cons = d["constituents"]
    assert isinstance(cons, (list, tuple))
    assert cons, "empty constituents in dict"
    sample = cons[0]
    if hasattr(sample, "keys"):
        assert {"name", "role", "notes",
                "cross_reference_molecule_name"} == set(sample.keys())


# ==================================================================
# Agent actions
# ==================================================================

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(5)
        yield h


def test_action_list_components(app):
    rows = app.call("list_cell_components")
    assert len(rows) >= 35


def test_action_list_components_filtered_by_domain(app):
    rows = app.call("list_cell_components", domain="bacteria")
    assert all(r["domain"] == "bacteria" for r in rows)
    assert len(rows) >= 8


def test_action_list_components_filtered_by_sub_domain(app):
    rows = app.call("list_cell_components",
                    domain="eukarya", sub_domain="plant")
    ids = {r["id"] for r in rows}
    assert "chloroplast" in ids


def test_action_list_components_unknown_domain(app):
    rows = app.call("list_cell_components", domain="bogus")
    assert "error" in rows[0]


def test_action_list_components_unknown_sub_domain(app):
    rows = app.call("list_cell_components", sub_domain="bogus")
    assert "error" in rows[0]


def test_action_get_component(app):
    r = app.call("get_cell_component",
                 component_id="mitochondrion")
    assert "error" not in r
    assert r["domain"] == "eukarya"
    assert r["category"] == "organelle"


def test_action_get_unknown_component(app):
    r = app.call("get_cell_component", component_id="bogus")
    assert "error" in r


def test_action_find_components(app):
    rows = app.call("find_cell_components", needle="ribosome")
    ids = {r["id"] for r in rows}
    assert "80s-ribosome" in ids
    assert "70s-ribosome" in ids
    assert "archaeal-ribosome" in ids


def test_action_components_for_category(app):
    rows = app.call("cell_components_for_category",
                    category="cytoskeleton")
    assert all(r["category"] == "cytoskeleton" for r in rows)
    ids = {r["id"] for r in rows}
    assert "actin-microfilament" in ids
    assert "microtubule" in ids


def test_action_components_for_unknown_category(app):
    rows = app.call("cell_components_for_category",
                    category="bogus")
    assert "error" in rows[0]


def test_action_components_for_empty_category(app):
    rows = app.call("cell_components_for_category", category="")
    assert rows == []


# ==================================================================
# Dialog
# ==================================================================

@pytest.fixture(autouse=True)
def _reset_singleton():
    from orgchem.gui.dialogs import cell_components as mod
    mod.CellComponentsDialog._instance = None
    yield
    mod.CellComponentsDialog._instance = None


def test_dialog_constructs(app, qtbot):
    from orgchem.gui.dialogs.cell_components import (
        CellComponentsDialog,
    )
    d = CellComponentsDialog(parent=app.window)
    qtbot.addWidget(d)
    assert d._list.count() >= 35


def test_dialog_singleton(app):
    from orgchem.gui.dialogs.cell_components import (
        CellComponentsDialog,
    )
    a = CellComponentsDialog.singleton(parent=app.window)
    b = CellComponentsDialog.singleton(parent=app.window)
    assert a is b


def test_dialog_domain_combo_filters(app, qtbot):
    from orgchem.gui.dialogs.cell_components import (
        CellComponentsDialog,
    )
    d = CellComponentsDialog(parent=app.window)
    qtbot.addWidget(d)
    idx = d._dom_combo.findText("bacteria")
    assert idx >= 0
    d._dom_combo.setCurrentIndex(idx)
    assert d._list.count() >= 8


def test_dialog_sub_domain_combo_filters(app, qtbot):
    from orgchem.gui.dialogs.cell_components import (
        CellComponentsDialog,
    )
    d = CellComponentsDialog(parent=app.window)
    qtbot.addWidget(d)
    # Eukarya + plant — should include chloroplast + plant
    # cell wall plus pan-eukaryotic items.
    idx = d._dom_combo.findText("eukarya")
    d._dom_combo.setCurrentIndex(idx)
    idx = d._sub_combo.findText("plant")
    d._sub_combo.setCurrentIndex(idx)
    visible = []
    for i in range(d._list.count()):
        visible.append(d._list.item(i).data(Qt_UserRole()))
    assert "chloroplast" in visible
    assert "plant-cell-wall" in visible
    # Animal-only items should be excluded.
    assert "lysosome" not in visible


def test_dialog_category_combo_filters(app, qtbot):
    from orgchem.gui.dialogs.cell_components import (
        CellComponentsDialog,
    )
    d = CellComponentsDialog(parent=app.window)
    qtbot.addWidget(d)
    idx = d._cat_combo.findText("cytoskeleton")
    d._cat_combo.setCurrentIndex(idx)
    assert d._list.count() >= 3


def test_dialog_text_filter(app, qtbot):
    from orgchem.gui.dialogs.cell_components import (
        CellComponentsDialog,
    )
    d = CellComponentsDialog(parent=app.window)
    qtbot.addWidget(d)
    d._filter_edit.setText("collagen")
    assert d._list.count() >= 1   # ECM has collagen


def test_dialog_filter_no_match(app, qtbot):
    from orgchem.gui.dialogs.cell_components import (
        CellComponentsDialog,
    )
    d = CellComponentsDialog(parent=app.window)
    qtbot.addWidget(d)
    d._filter_edit.setText("zzzz-no-match")
    assert d._list.count() == 0
    assert "no components" in d._title.text().lower()


def test_dialog_select_component(app, qtbot):
    from orgchem.gui.dialogs.cell_components import (
        CellComponentsDialog,
    )
    d = CellComponentsDialog(parent=app.window)
    qtbot.addWidget(d)
    ok = d.select_component("mitochondrion")
    assert ok is True
    assert "Mitochondrion" in d._title.text()


def test_dialog_select_unknown(app, qtbot):
    from orgchem.gui.dialogs.cell_components import (
        CellComponentsDialog,
    )
    d = CellComponentsDialog(parent=app.window)
    qtbot.addWidget(d)
    assert d.select_component("does-not-exist") is False


def test_dialog_default_first_row_selected(app, qtbot):
    from orgchem.gui.dialogs.cell_components import (
        CellComponentsDialog,
    )
    d = CellComponentsDialog(parent=app.window)
    qtbot.addWidget(d)
    title = d._title.text()
    assert "Select" not in title
    html = d._detail.toHtml()
    for section in ("Location", "Function",
                    "Molecular constituents"):
        assert section in html


def test_dialog_constituents_table_shown(app, qtbot):
    from orgchem.gui.dialogs.cell_components import (
        CellComponentsDialog,
    )
    d = CellComponentsDialog(parent=app.window)
    qtbot.addWidget(d)
    d.select_component("mitochondrion")
    html = d._detail.toHtml()
    assert "ATP synthase" in html
    assert "<table" in html.lower()


# ---- agent action open path -----------------------------------

def test_open_action_fires(app, qtbot):
    from orgchem.agent.actions import invoke
    from orgchem.gui.dialogs.cell_components import (
        CellComponentsDialog,
    )
    res = invoke("open_cell_components")
    assert res.get("opened") is True
    assert CellComponentsDialog._instance is not None


def test_open_action_with_id(app, qtbot):
    from orgchem.agent.actions import invoke
    res = invoke("open_cell_components",
                 component_id="chromatin")
    assert res.get("opened") is True
    assert res.get("selected") is True


def test_open_action_with_unknown_id(app, qtbot):
    from orgchem.agent.actions import invoke
    res = invoke("open_cell_components",
                 component_id="bogus")
    assert res.get("opened") is True
    assert res.get("selected") is False


# Helper for the sub-domain combo filter test that needs to
# pull QListWidgetItem.data(Qt.UserRole) — `Qt` is in qt-only
# namespace, so import it lazily inside the helper to avoid
# poisoning the headless-only test imports.
def Qt_UserRole():
    from PySide6.QtCore import Qt
    return Qt.UserRole
