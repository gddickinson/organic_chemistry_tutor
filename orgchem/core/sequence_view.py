"""Phase 34a — headless ``SequenceView`` core.

Builds the data structure that the Phase 34b `SequenceBar` Qt
widget will render.  Kept deliberately free of Qt imports so
tests (and the agent action) can exercise it without spinning
up the full GUI.

Schema::

    SequenceView
        pdb_id:  str
        protein_chains: list[ChainSequence]
        dna_chains:     list[ChainSequence]   # empty for pure proteins
        highlights: list[HighlightSpan]       # colour-overlay tracks

    ChainSequence
        chain_id:     str
        one_letter:   str                     # joined 1-letter code
        three_letter: list[str]
        residue_numbers: list[int]
        kind: Literal["protein", "dna", "rna"]

    HighlightSpan
        chain_id: str
        start:    int     # residue seq_id (1-based, PDB-native)
        end:      int     # inclusive
        kind:     str     # "pocket" / "ligand-contact" / "active-site" / ...
        label:    str     # human-readable tag
        colour:   str     # CSS colour string, e.g. "#9FD5A0"

Builder entry points:

- :func:`build_sequence_view(protein)` — pure conversion from the
  Phase 24a ``Protein`` dataclass.
- :func:`attach_contact_highlights(view, contact_report)` — stamp
  a :class:`HighlightSpan` per contact residue, using the Phase 24e
  H-bond / salt-bridge / π-stacking / hydrophobic kinds.
- :func:`attach_pocket_highlights(view, pockets)` — stamp one span
  per pocket, coloured by rank.

No network, no GUI — just data-shape transforms.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Literal, Optional

from orgchem.core.protein import (
    Protein, _AA_3_TO_1, _NUCLEOTIDES,
)


#: Canonical per-kind colour palette used by the Qt widget and
#: downstream feature-track renderers.  CSS colour strings so the
#: same values slot into HTML / SVG / Qt all three.
HIGHLIGHT_COLOURS: Dict[str, str] = {
    "pocket":          "#9FD5A0",   # light green
    "ligand-contact":  "#F5DF50",   # yellow
    "active-site":     "#E88B28",   # orange
    "h-bond":          "#4B8BD5",   # blue
    "salt-bridge":     "#D04040",   # red
    "pi-stacking":     "#A050C0",   # purple
    "hydrophobic":     "#E0984B",   # tan
    "user":            "#F18FB1",   # pink
    "gene":            "#8080C0",   # muted indigo
    "ss-helix":        "#C04848",   # dusty red
    "ss-strand":       "#4878C0",   # dusty blue
}


@dataclass(frozen=True)
class HighlightSpan:
    chain_id: str
    start: int
    end: int
    kind: str
    label: str = ""
    colour: str = ""

    def to_dict(self) -> Dict[str, object]:
        return {
            "chain_id": self.chain_id,
            "start": self.start,
            "end": self.end,
            "kind": self.kind,
            "label": self.label,
            "colour": self.colour or HIGHLIGHT_COLOURS.get(self.kind, "#808080"),
        }


@dataclass
class ChainSequence:
    chain_id: str
    one_letter: str
    three_letter: List[str]
    residue_numbers: List[int]
    kind: Literal["protein", "dna", "rna"] = "protein"

    @property
    def length(self) -> int:
        return len(self.one_letter)

    def to_dict(self) -> Dict[str, object]:
        return {
            "chain_id": self.chain_id,
            "one_letter": self.one_letter,
            "three_letter": list(self.three_letter),
            "residue_numbers": list(self.residue_numbers),
            "kind": self.kind,
            "length": self.length,
        }


@dataclass
class SequenceView:
    pdb_id: str
    protein_chains: List[ChainSequence] = field(default_factory=list)
    dna_chains: List[ChainSequence] = field(default_factory=list)
    highlights: List[HighlightSpan] = field(default_factory=list)

    @property
    def all_chains(self) -> List[ChainSequence]:
        return list(self.protein_chains) + list(self.dna_chains)

    def get_chain(self, chain_id: str) -> Optional[ChainSequence]:
        for c in self.all_chains:
            if c.chain_id == chain_id:
                return c
        return None

    def add_highlight(self, span: HighlightSpan) -> None:
        self.highlights.append(span)

    def to_dict(self) -> Dict[str, object]:
        return {
            "pdb_id": self.pdb_id,
            "protein_chains": [c.to_dict() for c in self.protein_chains],
            "dna_chains": [c.to_dict() for c in self.dna_chains],
            "highlights": [h.to_dict() for h in self.highlights],
        }


# -------------------- builder -----------------------

#: Residue codes treated as DNA in the SequenceView split.
_DNA_RESIDUES = {"DA", "DT", "DG", "DC", "DU"}
_RNA_RESIDUES = {"A", "T", "G", "C", "U"} & _NUCLEOTIDES
#: One-letter mapping for nucleotide residues — matches the
#: standard IUB/IUPAC single-letter codes.
_NT_3_TO_1 = {
    "DA": "A", "DT": "T", "DG": "G", "DC": "C", "DU": "U",
    "A": "A", "T": "T", "G": "G", "C": "C", "U": "U",
}


def _classify_chain(chain) -> Literal["protein", "dna", "rna"]:
    """Decide whether a chain is protein / DNA / RNA by majority
    residue type.  Mixed chains (rare) fall back to protein if any
    AA residues are present."""
    aa = sum(1 for r in chain.residues if r.is_standard_amino_acid)
    if aa > 0:
        return "protein"
    dna = sum(1 for r in chain.residues if r.name in _DNA_RESIDUES)
    rna = sum(1 for r in chain.residues
              if r.name in _RNA_RESIDUES and r.name not in _DNA_RESIDUES)
    return "dna" if dna >= rna else "rna"


def _chain_to_sequence(chain) -> Optional[ChainSequence]:
    """Convert one `Chain` → one `ChainSequence`.  Returns None for
    chains that contain only ions / waters (which do appear as
    pseudo-chains in some PDB files)."""
    kind = _classify_chain(chain)
    one_letters: List[str] = []
    three_letters: List[str] = []
    numbers: List[int] = []
    for r in chain.residues:
        if kind == "protein" and r.is_standard_amino_acid:
            one_letters.append(_AA_3_TO_1.get(r.name, "X"))
            three_letters.append(r.name)
            numbers.append(r.seq_id)
        elif kind in ("dna", "rna") and r.name in _NT_3_TO_1:
            one_letters.append(_NT_3_TO_1[r.name])
            three_letters.append(r.name)
            numbers.append(r.seq_id)
    if not one_letters:
        return None
    return ChainSequence(
        chain_id=chain.id,
        one_letter="".join(one_letters),
        three_letter=three_letters,
        residue_numbers=numbers,
        kind=kind,
    )


def build_sequence_view(protein: Protein) -> SequenceView:
    """Extract a :class:`SequenceView` from a parsed :class:`Protein`.

    Separates chains by kind into `protein_chains` and `dna_chains`
    (RNA-dominant chains currently join `dna_chains` — the
    Phase 34d DNA-strand renderer treats both as "nucleotide
    strand" and colour-codes the backbone kind).
    """
    view = SequenceView(pdb_id=protein.pdb_id)
    for chain in protein.chains:
        seq = _chain_to_sequence(chain)
        if seq is None:
            continue
        if seq.kind == "protein":
            view.protein_chains.append(seq)
        else:
            view.dna_chains.append(seq)
    return view


# -------------------- highlight helpers -----------------------

def attach_contact_highlights(view: SequenceView,
                              contacts) -> int:
    """Stamp one :class:`HighlightSpan` per ligand-contact residue
    onto *view*.  ``contacts`` is a Phase 24e ``ContactReport`` or
    anything with a ``contacts`` attribute that iterates records
    carrying ``chain``, ``residue`` (int seq_id or ``"HIS57"``
    style), and ``kind``.  Returns the number of spans added.
    """
    added = 0
    records = getattr(contacts, "contacts", None) or []
    for c in records:
        chain_id = getattr(c, "chain", "") or ""
        resi = _parse_residue_seq_id(getattr(c, "residue", None))
        if resi is None or not chain_id:
            continue
        kind = getattr(c, "kind", "ligand-contact")
        colour = HIGHLIGHT_COLOURS.get(kind,
                                       HIGHLIGHT_COLOURS["ligand-contact"])
        view.add_highlight(HighlightSpan(
            chain_id=chain_id,
            start=resi, end=resi,
            kind=kind,
            label=f"{chain_id}:{resi} · {kind}",
            colour=colour,
        ))
        added += 1
    return added


def attach_pocket_highlights(view: SequenceView,
                             pockets) -> int:
    """Stamp one span per pocket; each pocket is expected to carry
    a ``lining_residues`` iterable of ``(chain, seq_id)`` tuples.
    Pocket rank (0-indexed) controls the colour saturation via a
    simple alpha modulation in the label (Qt widget later reads
    both)."""
    added = 0
    for rank, p in enumerate(pockets or []):
        lining = getattr(p, "lining_residues", None) or []
        # Group by chain + collapse to min-max span per chain.
        by_chain: Dict[str, List[int]] = {}
        for (chain_id, seq_id) in lining:
            by_chain.setdefault(chain_id, []).append(seq_id)
        for chain_id, ids in by_chain.items():
            if not ids:
                continue
            view.add_highlight(HighlightSpan(
                chain_id=chain_id,
                start=min(ids), end=max(ids),
                kind="pocket",
                label=f"Pocket #{rank + 1}",
                colour=HIGHLIGHT_COLOURS["pocket"],
            ))
            added += 1
    return added


# -------------------- internals -----------------------

def _parse_residue_seq_id(v) -> Optional[int]:
    """Coerce a residue identifier to int seq_id.  Accepts:
    - plain int or numeric string
    - "HIS57" → 57
    - "A:HIS57" → 57
    """
    if v is None:
        return None
    if isinstance(v, int):
        return v
    s = str(v).strip()
    if not s:
        return None
    if ":" in s:
        s = s.split(":", 1)[1]
    # Strip trailing residue insertion code if any (e.g. "100A"→100).
    import re
    m = re.search(r"(\d+)", s)
    if m is None:
        return None
    try:
        return int(m.group(1))
    except ValueError:
        return None
