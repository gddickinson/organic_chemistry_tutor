"""Tests for the round-50 orphan-sweep bundle:
- `compare_pathways_green(pathway_ids)` (Phase 18a orphan)
- Glossary-linker autolink + reaction-description hyperlinks (Phase 11c)
"""
from __future__ import annotations
import os
import pytest

pytest.importorskip("rdkit")


@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


# ---- compare_pathways_green ---------------------------------------

def test_compare_pathways_green_ranks_by_overall_ae(app):
    from orgchem.agent.actions import invoke
    # Pick any 2+ seeded pathways.
    rows = invoke("list_pathways")
    assert len(rows) >= 2
    ids = [r["id"] for r in rows[:3]]
    res = invoke("compare_pathways_green", pathway_ids=ids)
    assert "error" not in res, res
    assert res["pathway_count"] == 3
    assert len(res["ranking"]) == 3
    aes = [r["overall_atom_economy"] for r in res["ranking"]]
    assert aes == sorted(aes, reverse=True), aes
    # `best_overall_ae` should equal rank-1 entry's AE
    assert res["best_overall_ae"] == aes[0]


def test_compare_pathways_green_empty_input():
    from orgchem.agent.actions import invoke
    res = invoke("compare_pathways_green", pathway_ids=[])
    assert "error" in res


def test_compare_pathways_green_bad_id_is_reported(app):
    from orgchem.agent.actions import invoke
    rows = invoke("list_pathways")
    good = rows[0]["id"]
    res = invoke("compare_pathways_green",
                 pathway_ids=[good, 999_999])
    assert "error" not in res
    # one good, one error row
    errors = [r for r in res["rows"] if "error" in r]
    assert len(errors) == 1
    # ranking should exclude the errored row
    ranked_ids = [r["id"] for r in res["ranking"]]
    assert 999_999 not in ranked_ids
    assert good in ranked_ids


def test_compare_pathways_audit_entry(app):
    from orgchem.gui.audit import GUI_ENTRY_POINTS
    entry = GUI_ENTRY_POINTS.get("compare_pathways_green", "")
    assert "Compare pathways" in entry


# ---- glossary autolink --------------------------------------------

def test_autolink_wraps_known_term():
    from orgchem.gui.widgets.glossary_linker import autolink, SCHEME
    html = autolink("Classical SN2 backside attack inverts stereo.")
    # Note: the seeded catalogue has "SN2" as a term.
    assert f'href="{SCHEME}:' in html
    # Raw text outside matches is HTML-escaped but otherwise preserved.
    assert "backside attack" in html


def test_autolink_preserves_non_matches():
    from orgchem.gui.widgets.glossary_linker import autolink
    html = autolink("A molecule with no glossary hits here.")
    assert "molecule with no glossary hits" in html
    assert "href=" not in html


def test_autolink_escapes_html_outside_matches():
    from orgchem.gui.widgets.glossary_linker import autolink
    html = autolink("Test <script>alert(1)</script> text.")
    # Angle brackets in the literal text should be escaped.
    assert "&lt;script&gt;" in html
    assert "<script>" not in html


def test_autolink_longest_first_prevents_shadowing():
    """Multi-word terms must be wrapped as a *single* anchor, not split
    into multiple shorter matches. The linker sorts surface forms by
    length descending before building its regex, so e.g. 'Hammond
    postulate' resolves as one span."""
    from orgchem.gui.widgets.glossary_linker import autolink, SCHEME
    html = autolink("The Hammond postulate predicts the geometry.")
    # Exactly one anchor for Hammond postulate as a whole; no separate
    # sub-anchor for the word "Hammond".
    assert f'"{SCHEME}:Hammond%20postulate"' in html, html
    # The anchor body should be the full two-word phrase.
    import re
    anchors = re.findall(
        r'<a href="' + re.escape(SCHEME)
        + r':([^"]+)"[^>]*>([^<]+)</a>', html)
    assert any(body == "Hammond postulate" for _, body in anchors), anchors


def test_reaction_description_renders_with_anchors(app):
    """End-to-end: open a reaction whose description contains a
    glossary term and check the description pane HTML has an anchor."""
    win = app.window
    panel = win.reactions
    # Pick the first reaction (seeded SN2 has 'SN2' in its name + description).
    rows = panel.model._rows
    assert rows, "no seeded reactions?"
    # Find one whose description is likely to contain a glossary term.
    target = next((r for r in rows if "SN2" in (r.description or "")),
                  rows[0])
    panel._display(target.id)
    html = panel.description.toHtml()
    # If the description had any recognised term, we should see an
    # `orgchem-glossary:` anchor. If not (unlikely for seed data),
    # the test still validates the widget rendering path.
    if target.description and any(
            tok in target.description.lower()
            for tok in ("sn2", "aromatic", "mechanism", "resonance")):
        assert "orgchem-glossary:" in html, html
