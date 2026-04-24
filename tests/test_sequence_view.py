"""Phase 34a round 112 tests for the headless `SequenceView` core."""
from __future__ import annotations
import os

import pytest

pytest.importorskip("rdkit")


# Minimal in-memory PDB text: 3 chains — a tiny protein (2 AAs),
# a DNA strand (3 nt), and an ion-only chain (should be skipped).
_FIXTURE = """\
HEADER    TEST PROTEIN                              01-JAN-26   1TST
TITLE     Tiny protein + DNA + ion for sequence-view tests
ATOM      1  N   ALA A   1       0.000   0.000   0.000  1.00 20.00           N
ATOM      2  CA  ALA A   1       1.458   0.000   0.000  1.00 20.00           C
ATOM      3  C   ALA A   1       2.009   1.420   0.000  1.00 20.00           C
ATOM      4  O   ALA A   1       1.251   2.390   0.000  1.00 20.00           O
ATOM      5  N   GLY A   2       3.332   1.548   0.000  1.00 20.00           N
ATOM      6  CA  GLY A   2       4.000   2.870   0.000  1.00 20.00           C
ATOM      7  P   DA  B   1      10.000  10.000  10.000  1.00 25.00           P
ATOM      8  OP1 DA  B   1      10.000  11.000  10.000  1.00 25.00           O
ATOM      9  P   DT  B   2      12.000  10.000  10.000  1.00 25.00           P
ATOM     10  OP1 DT  B   2      12.000  11.000  10.000  1.00 25.00           O
ATOM     11  P   DG  B   3      14.000  10.000  10.000  1.00 25.00           P
ATOM     12  OP1 DG  B   3      14.000  11.000  10.000  1.00 25.00           O
HETATM   13 ZN    ZN C   1      20.000  20.000  20.000  1.00 30.00          ZN
END
"""


# ---- dataclass shape --------------------------------------------

def test_build_sequence_view_splits_protein_and_dna():
    from orgchem.core.protein import parse_pdb_text
    from orgchem.core.sequence_view import build_sequence_view
    protein = parse_pdb_text(_FIXTURE, pdb_id="1TST")
    view = build_sequence_view(protein)
    assert view.pdb_id == "1TST"
    assert len(view.protein_chains) == 1
    assert len(view.dna_chains) == 1
    # Ion-only chain (C / ZN) should not appear as a sequence chain.
    ids = {c.chain_id for c in view.all_chains}
    assert "C" not in ids, ids


def test_chain_sequence_fields():
    from orgchem.core.protein import parse_pdb_text
    from orgchem.core.sequence_view import build_sequence_view
    protein = parse_pdb_text(_FIXTURE, pdb_id="1TST")
    view = build_sequence_view(protein)
    prot = view.protein_chains[0]
    assert prot.chain_id == "A"
    assert prot.one_letter == "AG", prot.one_letter
    assert prot.three_letter == ["ALA", "GLY"]
    assert prot.residue_numbers == [1, 2]
    assert prot.kind == "protein"
    assert prot.length == 2

    dna = view.dna_chains[0]
    assert dna.chain_id == "B"
    assert dna.one_letter == "ATG"
    assert dna.three_letter == ["DA", "DT", "DG"]
    assert dna.residue_numbers == [1, 2, 3]
    assert dna.kind == "dna"


def test_get_chain_and_all_chains():
    from orgchem.core.protein import parse_pdb_text
    from orgchem.core.sequence_view import build_sequence_view
    protein = parse_pdb_text(_FIXTURE, pdb_id="1TST")
    view = build_sequence_view(protein)
    assert view.get_chain("A") is view.protein_chains[0]
    assert view.get_chain("B") is view.dna_chains[0]
    assert view.get_chain("Z") is None
    assert len(view.all_chains) == 2


# ---- highlight helpers ------------------------------------------

def test_highlight_span_to_dict_uses_colour_default():
    from orgchem.core.sequence_view import HighlightSpan, HIGHLIGHT_COLOURS
    span = HighlightSpan(chain_id="A", start=10, end=12,
                         kind="pocket", label="Pocket #1")
    d = span.to_dict()
    assert d["colour"] == HIGHLIGHT_COLOURS["pocket"]
    # Explicit colour wins over the default.
    span2 = HighlightSpan(chain_id="A", start=1, end=1,
                          kind="user", label="mine",
                          colour="#ABCDEF")
    assert span2.to_dict()["colour"] == "#ABCDEF"


def test_attach_contact_highlights_parses_residue_formats():
    """The helper must coerce 'HIS57', 'A:HIS57', plain ints, and
    numeric strings to seq_id."""
    from orgchem.core.sequence_view import (
        SequenceView, attach_contact_highlights,
    )

    class _Contact:
        def __init__(self, chain, residue, kind):
            self.chain = chain
            self.residue = residue
            self.kind = kind

    class _Report:
        contacts = [
            _Contact("A", "HIS57", "h-bond"),
            _Contact("A", "A:SER195", "hydrophobic"),
            _Contact("B", 195, "salt-bridge"),
            _Contact("B", "42", "pi-stacking"),
            _Contact("A", None, "h-bond"),       # skipped
            _Contact("", "HIS57", "h-bond"),     # skipped (no chain)
        ]

    view = SequenceView(pdb_id="TEST")
    n = attach_contact_highlights(view, _Report())
    assert n == 4
    starts = sorted(h.start for h in view.highlights)
    assert starts == [42, 57, 195, 195]
    kinds = {h.kind for h in view.highlights}
    assert kinds == {"h-bond", "hydrophobic", "salt-bridge", "pi-stacking"}


def test_attach_pocket_highlights_collapses_to_span_per_chain():
    """Pocket lining residues across one chain should collapse to
    a single (start, end) span per chain."""
    from orgchem.core.sequence_view import (
        SequenceView, attach_pocket_highlights,
    )

    class _Pocket:
        lining_residues = [("A", 10), ("A", 12), ("A", 15),
                           ("B", 50), ("B", 52)]

    view = SequenceView(pdb_id="TEST")
    n = attach_pocket_highlights(view, [_Pocket()])
    assert n == 2
    spans_by_chain = {h.chain_id: (h.start, h.end) for h in view.highlights}
    assert spans_by_chain["A"] == (10, 15)
    assert spans_by_chain["B"] == (50, 52)


def test_feature_track_overlay_full_stack():
    """Phase 34e round 118 — verify the intended panel-flow: build
    the base view, layer pockets first, layer contacts second, and
    confirm both show up with kind-appropriate colours from the
    `HIGHLIGHT_COLOURS` palette."""
    from orgchem.core.protein import parse_pdb_text
    from orgchem.core.sequence_view import (
        build_sequence_view, attach_pocket_highlights,
        attach_contact_highlights, HIGHLIGHT_COLOURS,
    )

    class _Pocket:
        lining_residues = [("A", 1), ("A", 2)]   # res 1-2

    class _Contact:
        def __init__(self, chain, residue, kind):
            self.chain = chain
            self.residue = residue
            self.kind = kind

    class _Report:
        contacts = [_Contact("A", 2, "h-bond"),
                    _Contact("A", 2, "hydrophobic")]

    view = build_sequence_view(parse_pdb_text(_FIXTURE, pdb_id="1TST"))
    assert view.highlights == []   # clean slate before overlays

    n_pockets = attach_pocket_highlights(view, [_Pocket()])
    n_contacts = attach_contact_highlights(view, _Report())
    assert n_pockets == 1
    assert n_contacts == 2

    kinds = {h.kind for h in view.highlights}
    assert kinds == {"pocket", "h-bond", "hydrophobic"}
    colours = {h.kind: h.colour for h in view.highlights}
    assert colours["pocket"] == HIGHLIGHT_COLOURS["pocket"]
    assert colours["h-bond"] == HIGHLIGHT_COLOURS["h-bond"]
    assert colours["hydrophobic"] == HIGHLIGHT_COLOURS["hydrophobic"]


# ---- SequenceView dict round-trip --------------------------------

def test_sequence_view_to_dict_schema():
    from orgchem.core.protein import parse_pdb_text
    from orgchem.core.sequence_view import build_sequence_view
    view = build_sequence_view(parse_pdb_text(_FIXTURE, pdb_id="1TST"))
    d = view.to_dict()
    assert set(d.keys()) == {"pdb_id", "protein_chains", "dna_chains",
                             "highlights"}
    assert d["pdb_id"] == "1TST"
    # Each chain dict carries the expected keys.
    expected_chain_keys = {"chain_id", "one_letter", "three_letter",
                           "residue_numbers", "kind", "length"}
    for c in d["protein_chains"] + d["dna_chains"]:
        assert set(c.keys()) == expected_chain_keys


# ---- Agent action ------------------------------------------------

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_get_sequence_view_action_missing_pdb_errors(app):
    res = app.call("get_sequence_view", pdb_id="9XYZ")
    assert "error" in res, res


def test_get_sequence_view_action_returns_populated_view(app, tmp_path,
                                                         monkeypatch):
    """Prime the PDB cache with our fixture and confirm the action
    returns a full sequence view without network access."""
    import orgchem.sources.pdb as pdb_mod
    cache = tmp_path / "pdb_cache"
    cache.mkdir()
    (cache / "1TST.pdb").write_text(_FIXTURE)
    monkeypatch.setattr(pdb_mod, "_pdb_cache_dir", lambda: cache)

    res = app.call("get_sequence_view", pdb_id="1TST")
    assert "error" not in res, res
    assert res["pdb_id"] == "1TST"
    assert len(res["protein_chains"]) == 1
    assert len(res["dna_chains"]) == 1
    assert res["protein_chains"][0]["one_letter"] == "AG"
    assert res["dna_chains"][0]["one_letter"] == "ATG"
    # No contacts requested → no highlights.
    assert res["highlights"] == []
