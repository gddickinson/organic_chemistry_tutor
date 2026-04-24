"""Phase 33a — full-text search core + agent-action tests."""
from __future__ import annotations

import pytest

from orgchem.agent.headless import HeadlessApp
from orgchem.core.fulltext_search import (
    SEARCHABLE_KINDS,
    SearchResult,
    _score,
    _snippet,
    search,
)


@pytest.fixture(scope="module")
def _app():
    with HeadlessApp() as app:
        yield app


# ---------- scoring helpers ----------

def test_score_returns_zero_on_empty_query():
    assert _score("anything", "") == 0.0
    assert _score("", "sn2") == 0.0


def test_score_counts_occurrences():
    assert _score("aaa bbb aaa", "aaa") >= 2.0


def test_score_word_boundary_bonus():
    # "SN2" as a standalone token should rank higher than
    # "SN2-substrate" continued-text match.
    s_word = _score("SN2 reaction mechanism", "sn2")
    s_embed = _score("XSN2Y blob", "sn2")
    assert s_word > s_embed


def test_snippet_extracts_context_window():
    txt = ("The Diels-Alder reaction is a concerted [4+2] "
           "cycloaddition of a diene and a dienophile.")
    sn = _snippet(txt, "diene", window=30)
    assert "diene" in sn.lower()
    # Ellipses on either side when the excerpt is trimmed.
    assert sn.startswith("…") or sn.endswith("…") or len(sn) < 70


def test_snippet_head_fallback_when_no_hit():
    sn = _snippet("some prose without the word", "xyz", window=20)
    assert sn  # non-empty; it's just the head of the string


# ---------- corpus-backed search (requires seeded DB) ----------

def test_search_empty_query_returns_empty(_app):
    assert search("", limit=10) == []
    assert search("   ", limit=10) == []


def test_search_finds_caffeine(_app):
    hits = search("caffeine", limit=20)
    assert hits, "caffeine should return at least one result"
    # The Caffeine molecule must appear in the hit list; top rank
    # may be shared with a pathway that also has caffeine in its
    # title (e.g. "Caffeine from theobromine"), so just check
    # for the molecule row anywhere near the top.
    top5_kinds = [(h.kind, h.title.lower()) for h in hits[:5]]
    assert any(k == "molecule" and "caffeine" in t
               for k, t in top5_kinds), top5_kinds


def test_search_finds_enolate_in_mechanism_steps(_app):
    """Seeded Claisen / aldol mechanism descriptions mention
    'enolate' heavily — this is the kind of hit palette
    name-match couldn't reach."""
    hits = search("enolate", limit=30)
    assert any(h.kind == "mechanism-step" for h in hits), hits


def test_search_finds_glossary_term(_app):
    hits = search("regioselectivity", limit=20)
    assert any(h.kind == "glossary"
               and "regioselectivity" in h.title.lower()
               for h in hits)


def test_search_finds_pathway_step_detail(_app):
    """The 'DIPAMP' chiral ligand is mentioned in the L-DOPA
    pathway step-2 notes — this is the kind of hit palette
    name-match couldn't reach."""
    hits = search("DIPAMP", limit=20)
    assert any(h.kind == "pathway" for h in hits), hits


def test_search_respects_kinds_filter(_app):
    hits_all = search("aspirin", limit=50)
    assert len(hits_all) > 0
    hits_only_glossary = search("aspirin", kinds=["glossary"],
                                limit=50)
    for h in hits_only_glossary:
        assert h.kind == "glossary"


def test_search_rejects_unknown_kind():
    with pytest.raises(ValueError):
        search("anything", kinds=["bogus-kind"])


def test_title_hits_outrank_body_hits(_app):
    """A molecule literally named 'Aspirin' should rank above
    any description that merely mentions aspirin."""
    hits = search("aspirin", limit=30)
    top = hits[0]
    assert "aspirin" in top.title.lower()
    assert top.score >= hits[-1].score


def test_search_results_are_sorted_by_score_desc(_app):
    hits = search("nitration", limit=20)
    assert hits
    scores = [h.score for h in hits]
    assert scores == sorted(scores, reverse=True)


def test_search_respects_limit(_app):
    hits = search("reaction", limit=5)
    assert len(hits) <= 5


# ---------- agent action ----------

def test_fulltext_search_action_returns_serialisable_dict(_app):
    r = _app.call("fulltext_search", query="caffeine", limit=5)
    assert "query" in r and "n_results" in r and "results" in r
    assert r["query"] == "caffeine"
    assert r["n_results"] > 0
    # Each result is a plain dict (JSON-serialisable).
    for hit in r["results"]:
        for key in ("kind", "title", "snippet", "score", "key"):
            assert key in hit


def test_fulltext_search_action_accepts_kinds_csv(_app):
    r = _app.call("fulltext_search", query="aspirin",
                  kinds="glossary,pathway")
    kinds_seen = {h["kind"] for h in r["results"]}
    assert kinds_seen <= {"glossary", "pathway"}


def test_fulltext_search_action_rejects_bad_kind(_app):
    r = _app.call("fulltext_search", query="x", kinds="bogus")
    assert "error" in r
    assert r["n_results"] == 0


def test_searchable_kinds_constant_is_stable():
    """Round-88 contract: the 5 kinds are a stable public API."""
    assert SEARCHABLE_KINDS == (
        "molecule", "reaction", "pathway", "glossary",
        "mechanism-step",
    )
