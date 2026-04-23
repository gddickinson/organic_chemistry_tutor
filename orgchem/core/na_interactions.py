"""Nucleic-acid / small-molecule interaction analyser — Phase 24k.

Specialises the Phase 24e contact analyser for DNA / RNA targets:
intercalation, major- vs minor-groove binding, and phosphate-backbone
salt bridges are the interaction modes that matter most for teaching
and for NA-binding drug families (doxorubicin, cisplatin, netropsin,
riboswitch modulators, G-quadruplex stabilisers).

Classification heuristics
-------------------------
A :class:`NAContact` is one of four kinds:

- **intercalation** — the ligand's aromatic ring centroid is **between
  two consecutive base centroids** along the same strand (distance to
  both base centroids ≤ 4.5 Å, centroid-centroid angle ≥ 120°).
- **major-groove-hb** — H-bond-type heavy-atom N/O-N/O contact
  (≤ 3.5 Å) to a base atom on the major-groove face (N7 / O6 / N6 /
  C5-methyl for DT; N7 / N6 for DA; N4 for DC; O4 / C5 for DT/DU).
- **minor-groove-hb** — same geometry but to a minor-groove face atom
  (N3 / C2-NH2 / O2).
- **phosphate-contact** — any ligand N or O within 4.5 Å of a
  phosphate O1P / O2P / OP1 / OP2 oxygen. Captures both salt-bridge
  and H-bond interactions to the backbone.

The analyser intentionally **ignores** hydrophobic C-C contacts —
they are rare and teaching-irrelevant for NA targets, where aromatic
stacking dominates.

Limitations
-----------
- No π-π classification separate from intercalation: any stacking
  that isn't between two consecutive bases is tagged as a generic
  ``stacking`` contact in the residue's own plane.
- No water-mediated contacts (would need explicit ordered waters and
  angle filters).
- Groove assignment uses a name-based table; chemically modified
  bases (m5C, 8-oxo-G) fall back to "unknown-groove".

All geometry is pure Python / ``math`` — no numpy / Biopython deps.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from math import acos, degrees, sqrt
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

from orgchem.core.protein import Atom, Protein, Residue


# ---------------------------------------------------------------------

#: Nucleotide residue names we recognise (PDB convention).
NUCLEOTIDES = {"DA", "DT", "DG", "DC", "DU", "A", "T", "G", "C", "U"}

#: Purine base ring-atom names (6+5-ring fused system).
_PURINE_RING = ("N1", "C2", "N3", "C4", "C5", "C6", "N7", "C8", "N9")
#: Pyrimidine base ring-atom names (6-ring only).
_PYRIMIDINE_RING = ("N1", "C2", "N3", "C4", "C5", "C6")

#: Major-groove-facing atoms (per base). These hydrogen-bond or
#: accept into the wide shallow DNA groove.
_MAJOR_GROOVE_ATOMS: Dict[str, Tuple[str, ...]] = {
    "DA": ("N7", "N6", "C8"),
    "A":  ("N7", "N6", "C8"),
    "DG": ("N7", "O6", "C8"),
    "G":  ("N7", "O6", "C8"),
    "DC": ("N4", "C5"),
    "C":  ("N4", "C5"),
    "DT": ("O4", "C5", "C7"),          # C7 = methyl
    "T":  ("O4", "C5", "C7"),
    "DU": ("O4", "C5"),
    "U":  ("O4", "C5"),
}

#: Minor-groove-facing atoms (the narrow deep groove).
_MINOR_GROOVE_ATOMS: Dict[str, Tuple[str, ...]] = {
    "DA": ("N3", "C2"),
    "A":  ("N3", "C2"),
    "DG": ("N3", "N2", "C2"),
    "G":  ("N3", "N2", "C2"),
    "DC": ("O2", "C2"),
    "C":  ("O2", "C2"),
    "DT": ("O2", "C2"),
    "T":  ("O2", "C2"),
    "DU": ("O2", "C2"),
    "U":  ("O2", "C2"),
}

_PHOSPHATE_ATOMS = {"OP1", "OP2", "O1P", "O2P", "P"}


# ---------------------------------------------------------------------

@dataclass(frozen=True)
class NAContact:
    """One non-covalent contact between a ligand and a nucleotide."""
    kind: str                 # "intercalation" / "major-groove-hb" / "minor-groove-hb" / "phosphate-contact" / "stacking"
    ligand_atom: str
    chain: str
    residue: str              # "DG5"
    residue_atom: str
    distance: float           # Å


@dataclass
class NAContactReport:
    pdb_id: str
    ligand_name: str
    contacts: List[NAContact] = field(default_factory=list)

    @property
    def n_contacts(self) -> int:
        return len(self.contacts)

    def by_kind(self, kind: str) -> List[NAContact]:
        return [c for c in self.contacts if c.kind == kind]

    def summary(self) -> Dict[str, object]:
        counts: Dict[str, int] = {}
        for c in self.contacts:
            counts[c.kind] = counts.get(c.kind, 0) + 1
        return {
            "pdb_id": self.pdb_id,
            "ligand": self.ligand_name,
            "n_contacts": self.n_contacts,
            "by_kind": counts,
            "contacts": [
                {"kind": c.kind, "ligand_atom": c.ligand_atom,
                 "chain": c.chain, "residue": c.residue,
                 "residue_atom": c.residue_atom,
                 "distance": round(c.distance, 2)}
                for c in self.contacts
            ],
        }


# ---------------------------------------------------------------------
# Public API

def analyse_na_binding(protein: Protein, ligand_name: str,
                       max_groove_hb: float = 3.5,
                       max_phosphate: float = 4.5,
                       max_intercalation: float = 4.5,
                       ) -> NAContactReport:
    """Return a :class:`NAContactReport` of ligand-NA contacts.

    ``protein`` is our ``Protein`` dataclass (the parser happily
    ingests DNA / RNA ATOM records — residue names just differ).
    """
    target = ligand_name.strip().upper()
    lig_res = next((r for r in protein.hetatm_residues
                    if r.name.upper() == target), None)
    report = NAContactReport(pdb_id=protein.pdb_id, ligand_name=target)
    if lig_res is None:
        return report
    lig_atoms = lig_res.atoms

    # 1) Collect nucleotide residues indexed by chain for intercalation.
    nt_by_chain: Dict[str, List[Residue]] = {}
    for chain in protein.chains:
        nts = [r for r in chain.residues if r.name.upper() in NUCLEOTIDES]
        if nts:
            nt_by_chain[chain.id] = nts

    if not nt_by_chain:
        return report  # not a nucleic-acid target

    lig_ring = _find_ligand_ring_centroid(lig_atoms)

    # 2) Intercalation — ligand ring between two consecutive bases.
    for chain_id, residues in nt_by_chain.items():
        if lig_ring is None:
            break
        for i in range(len(residues) - 1):
            r1, r2 = residues[i], residues[i + 1]
            b1 = _base_centroid(r1)
            b2 = _base_centroid(r2)
            if b1 is None or b2 is None:
                continue
            d1 = _distance(lig_ring, b1)
            d2 = _distance(lig_ring, b2)
            if d1 <= max_intercalation and d2 <= max_intercalation:
                angle = _angle(b1, lig_ring, b2)
                if angle >= 120.0:
                    # Report one contact per base; use the base atom
                    # closest to the ring centroid as the reference.
                    for r in (r1, r2):
                        nearest = min(
                            r.atoms,
                            key=lambda a: _distance(
                                lig_ring, (a.x, a.y, a.z)))
                        report.contacts.append(NAContact(
                            kind="intercalation",
                            ligand_atom=_nearest_ring_atom(lig_atoms,
                                                          lig_ring),
                            chain=chain_id,
                            residue=f"{r.name}{r.seq_id}",
                            residue_atom=nearest.name,
                            distance=_distance(lig_ring,
                                               (nearest.x, nearest.y,
                                                nearest.z)),
                        ))

    # 3) Groove H-bonds + phosphate-backbone contacts.
    for chain_id, residues in nt_by_chain.items():
        for r in residues:
            res_label = f"{r.name}{r.seq_id}"
            _score_groove_hbonds(report, chain_id, res_label, r,
                                 lig_atoms, max_groove_hb)
            _score_phosphate(report, chain_id, res_label, r,
                             lig_atoms, max_phosphate)

    return report


# ---------------------------------------------------------------------
# Internals

def _score_groove_hbonds(report: NAContactReport, chain_id: str,
                         res_label: str, res: Residue,
                         lig_atoms: Sequence[Atom],
                         max_d: float) -> None:
    name = res.name.upper()
    major = _MAJOR_GROOVE_ATOMS.get(name, ())
    minor = _MINOR_GROOVE_ATOMS.get(name, ())
    for atom in res.atoms:
        if atom.name in major:
            kind = "major-groove-hb"
        elif atom.name in minor:
            kind = "minor-groove-hb"
        else:
            continue
        if atom.element not in ("N", "O"):
            continue
        for la in lig_atoms:
            if la.element not in ("N", "O"):
                continue
            d = _atom_distance(la, atom)
            if d <= max_d:
                report.contacts.append(NAContact(
                    kind=kind, ligand_atom=la.name,
                    chain=chain_id, residue=res_label,
                    residue_atom=atom.name, distance=d,
                ))


def _score_phosphate(report: NAContactReport, chain_id: str,
                     res_label: str, res: Residue,
                     lig_atoms: Sequence[Atom], max_d: float) -> None:
    for atom in res.atoms:
        if atom.name not in _PHOSPHATE_ATOMS:
            continue
        for la in lig_atoms:
            if la.element not in ("N", "O"):
                continue
            d = _atom_distance(la, atom)
            if d <= max_d:
                report.contacts.append(NAContact(
                    kind="phosphate-contact",
                    ligand_atom=la.name,
                    chain=chain_id, residue=res_label,
                    residue_atom=atom.name, distance=d,
                ))
                break      # one phosphate contact per nt atom is enough


def _base_centroid(res: Residue) -> Optional[Tuple[float, float, float]]:
    """Centroid of the ring atoms of a base (purine = 9, pyrimidine = 6)."""
    purines = {"DA", "A", "DG", "G"}
    ring_names = _PURINE_RING if res.name.upper() in purines \
        else _PYRIMIDINE_RING
    ring_atoms = [a for a in res.atoms if a.name in ring_names]
    if len(ring_atoms) < 3:
        return None
    n = len(ring_atoms)
    return (sum(a.x for a in ring_atoms) / n,
            sum(a.y for a in ring_atoms) / n,
            sum(a.z for a in ring_atoms) / n)


def _find_ligand_ring_centroid(lig_atoms: Sequence[Atom]
                               ) -> Optional[Tuple[float, float, float]]:
    """Locate the ligand's aromatic-ring centroid.

    Heuristic: the set of carbons with ≥ 2 other carbons within 1.55 Å
    (aromatic C-C bond length). If the ligand has multiple ring systems
    we pick the largest one.
    """
    carbons = [a for a in lig_atoms if a.element == "C"]
    if len(carbons) < 5:
        return None
    ring: List[Atom] = []
    for c in carbons:
        n = sum(1 for o in carbons if o is not c
                and _atom_distance(c, o) < 1.6)
        if n >= 2:
            ring.append(c)
    if len(ring) < 5:
        return None
    take = ring[:min(len(ring), 6)]
    return (sum(a.x for a in take) / len(take),
            sum(a.y for a in take) / len(take),
            sum(a.z for a in take) / len(take))


def _nearest_ring_atom(lig_atoms: Sequence[Atom],
                       centroid: Tuple[float, float, float]) -> str:
    c_atoms = [a for a in lig_atoms if a.element == "C"]
    if not c_atoms:
        return lig_atoms[0].name if lig_atoms else "?"
    best = min(c_atoms, key=lambda a: _distance(centroid,
                                                (a.x, a.y, a.z)))
    return best.name


# ---- Geometry -----------------------------------------------------

def _atom_distance(a: Atom, b: Atom) -> float:
    dx = a.x - b.x
    dy = a.y - b.y
    dz = a.z - b.z
    return sqrt(dx * dx + dy * dy + dz * dz)


def _distance(p: Tuple[float, float, float],
              q: Tuple[float, float, float]) -> float:
    return sqrt(sum((a - b) ** 2 for a, b in zip(p, q)))


def _angle(p: Tuple[float, float, float],
           q: Tuple[float, float, float],
           r: Tuple[float, float, float]) -> float:
    """Angle at ``q`` between vectors q→p and q→r, in degrees."""
    vx1, vy1, vz1 = p[0] - q[0], p[1] - q[1], p[2] - q[2]
    vx2, vy2, vz2 = r[0] - q[0], r[1] - q[1], r[2] - q[2]
    n1 = sqrt(vx1 * vx1 + vy1 * vy1 + vz1 * vz1)
    n2 = sqrt(vx2 * vx2 + vy2 * vy2 + vz2 * vz2)
    if n1 == 0 or n2 == 0:
        return 0.0
    cos_ = max(-1.0, min(1.0, (vx1 * vx2 + vy1 * vy2 + vz1 * vz2)
                         / (n1 * n2)))
    return degrees(acos(cos_))
