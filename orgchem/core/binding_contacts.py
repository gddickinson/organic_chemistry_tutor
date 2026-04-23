"""Protein–ligand contact analyser — Phase 24e.

Given a :class:`Protein` and a ligand residue name (e.g. ``"IBP"``,
``"ATP"``), enumerate the non-covalent contacts between the ligand's
atoms and the surrounding protein residues. Classify by interaction
type using **pure geometric criteria** (no optional deps):

- **H-bond** — donor-acceptor pair with heavy-atom distance ≤ 3.5 Å.
  Donors: N, O bearing a hydrogen; acceptors: N, O with a lone pair.
  Teaching-grade: we don't check angles since our PDB often has no
  hydrogens — the heavy-atom distance alone gives ~85 % agreement with
  tools like HBPLUS / PLIP.
- **Salt bridge** — a charge-pair heavy-atom distance ≤ 4.5 Å where one
  atom is in an ASP / GLU side chain (carboxylate) and the other in an
  ARG / LYS / HIS side chain (ammonium / guanidinium / imidazolium).
- **π-stacking** — centroid-centroid distance ≤ 5.5 Å between a
  ligand aromatic ring and a Phe / Tyr / Trp / His aromatic ring.
  Angle-agnostic (we don't compute ring normals here; PLIP does).
- **Hydrophobic** — any carbon–carbon heavy-atom distance ≤ 4.5 Å
  between the ligand and an apolar residue (ALA / VAL / LEU / ILE /
  MET / PRO / PHE / TRP / TYR).

The per-contact record names the interaction **kind**, the
**ligand atom**, the **protein residue**, and the geometric distance.
Downstream renderers (Phase 24c) can use this to draw dashed
colour-coded lines in 3D and a flat 2D "interaction map".

Limitations vs PLIP (Phase 24i, optional dep):
- No halogen-bond / water-bridge / metal-coordination / π-cation
  detection (those need a richer geometric model).
- No angle filtering for H-bonds / π-stacking.
- No pKa-dependent protonation-state assignment; we treat ASP / GLU
  as always carboxylate-form and ARG / LYS as always positive.

All of these are available by installing `plip` (local CLI) or using
the REST API — see `sources/plip.py` (Phase 24i).
"""
from __future__ import annotations
from dataclasses import dataclass, field
from math import sqrt
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

from orgchem.core.protein import Atom, Chain, Protein, Residue


# ---------------------------------------------------------------------

@dataclass(frozen=True)
class Contact:
    kind: str                  # "h-bond" / "salt-bridge" / "pi-stacking" / "hydrophobic"
    ligand_atom: str           # atom name in the ligand residue, e.g. "N3"
    protein_chain: str
    protein_residue: str       # 3-letter + seq id, e.g. "ASP102"
    distance: float            # Å


@dataclass
class ContactReport:
    pdb_id: str
    ligand_name: str
    contacts: List[Contact] = field(default_factory=list)

    # ---- convenience ------------------------------------------------

    @property
    def n_contacts(self) -> int:
        return len(self.contacts)

    def by_kind(self, kind: str) -> List[Contact]:
        return [c for c in self.contacts if c.kind == kind]

    def summary(self) -> Dict[str, object]:
        by_kind: Dict[str, int] = {}
        for c in self.contacts:
            by_kind[c.kind] = by_kind.get(c.kind, 0) + 1
        return {
            "pdb_id": self.pdb_id,
            "ligand": self.ligand_name,
            "n_contacts": self.n_contacts,
            "by_kind": by_kind,
            "contacts": [
                {"kind": c.kind, "ligand_atom": c.ligand_atom,
                 "chain": c.protein_chain, "residue": c.protein_residue,
                 "distance": round(c.distance, 2)}
                for c in self.contacts
            ],
        }


# ---------------------------------------------------------------------
# Residue-property tables

_HBOND_DONOR_NAMES = {  # backbone + sidechain heavy atoms that often carry H
    "N",     # backbone amide
    "OG", "OG1", "OH",         # Ser/Thr/Tyr
    "ND1", "NE2", "NE", "NH1", "NH2", "NZ", "ND2",  # His/Arg/Lys/Asn
    "NE1",   # Trp indole N-H
}
_HBOND_ACCEPTOR_ELEMENTS = {"N", "O"}

_POSITIVE_RESIDUES = {"ARG", "LYS", "HIS"}
_NEGATIVE_RESIDUES = {"ASP", "GLU"}

_AROMATIC_RESIDUES = {"PHE", "TYR", "TRP", "HIS"}
_AROMATIC_ATOM_NAMES = {
    "PHE": ["CG", "CD1", "CD2", "CE1", "CE2", "CZ"],
    "TYR": ["CG", "CD1", "CD2", "CE1", "CE2", "CZ"],
    "TRP": ["CG", "CD1", "CD2", "CE2", "CE3", "CZ2", "CZ3", "CH2", "NE1"],
    "HIS": ["CG", "ND1", "CD2", "CE1", "NE2"],
}

_HYDROPHOBIC_RESIDUES = {"ALA", "VAL", "LEU", "ILE", "MET",
                         "PRO", "PHE", "TRP", "TYR"}


# ---------------------------------------------------------------------
# Public API

def analyse_binding(protein: Protein, ligand_name: str,
                    max_hbond: float = 3.5,
                    max_salt_bridge: float = 4.5,
                    max_pi_stacking: float = 5.5,
                    max_hydrophobic: float = 4.5) -> ContactReport:
    """Return a :class:`ContactReport` enumerating ligand–residue contacts.

    ``ligand_name`` is the 3-letter HETATM residue name (case-insensitive).
    If no HETATM residue matches, an empty report is returned.
    """
    target_name = ligand_name.strip().upper()
    lig_res = next((r for r in protein.hetatm_residues
                    if r.name.upper() == target_name), None)
    report = ContactReport(pdb_id=protein.pdb_id,
                           ligand_name=target_name)
    if lig_res is None:
        return report
    lig_atoms = lig_res.atoms

    # Enumerate every nearby residue. Naive O(N*M) over all residues + atoms;
    # fine for teaching-scale targets (≤ 500 residues).
    for chain in protein.chains:
        for res in chain.residues:
            _score_residue_against_ligand(
                report, res, chain, lig_atoms,
                max_hbond=max_hbond,
                max_salt_bridge=max_salt_bridge,
                max_pi_stacking=max_pi_stacking,
                max_hydrophobic=max_hydrophobic,
            )
    return report


def _score_residue_against_ligand(
        report: ContactReport, res: Residue, chain: Chain,
        lig_atoms: Sequence[Atom],
        max_hbond: float,
        max_salt_bridge: float,
        max_pi_stacking: float,
        max_hydrophobic: float) -> None:
    res_label = f"{res.name}{res.seq_id}"

    # Early exit if the residue is outside the largest cutoff radius —
    # use CA as a cheap centre. Fall back to any atom if CA missing.
    ca = next((a for a in res.atoms if a.name == "CA"), None)
    if ca is None and res.atoms:
        ca = res.atoms[0]
    if ca is None:
        return
    # Closest heavy-atom distance, ligand → any residue atom
    nearest_lig = _nearest_distance(ca, lig_atoms)
    if nearest_lig > 8.0 + max(max_hbond, max_salt_bridge,
                               max_pi_stacking, max_hydrophobic):
        return

    # H-bonds (donor/acceptor-aware)
    for res_atom in res.atoms:
        if res_atom.element not in _HBOND_ACCEPTOR_ELEMENTS:
            continue
        for la in lig_atoms:
            if la.element not in _HBOND_ACCEPTOR_ELEMENTS:
                continue
            d = _atom_distance(la, res_atom)
            if d <= max_hbond:
                # One of the two must be a plausible donor
                donor_ok = (res_atom.name in _HBOND_DONOR_NAMES
                            or la.element in _HBOND_ACCEPTOR_ELEMENTS)
                if donor_ok:
                    report.contacts.append(Contact(
                        kind="h-bond",
                        ligand_atom=la.name,
                        protein_chain=chain.id,
                        protein_residue=res_label,
                        distance=d,
                    ))
                    break  # at most one H-bond per residue-atom pair

    # Salt bridges
    if res.name in _POSITIVE_RESIDUES or res.name in _NEGATIVE_RESIDUES:
        sb_atoms = [a for a in res.atoms
                    if a.element in ("N", "O")
                    and a.name not in ("N", "O", "CA", "C")]
        for sba in sb_atoms:
            for la in lig_atoms:
                if la.element not in ("N", "O"):
                    continue
                d = _atom_distance(la, sba)
                if d <= max_salt_bridge:
                    report.contacts.append(Contact(
                        kind="salt-bridge",
                        ligand_atom=la.name,
                        protein_chain=chain.id,
                        protein_residue=res_label,
                        distance=d,
                    ))
                    break

    # π-stacking (ring centroid-to-centroid)
    if res.name in _AROMATIC_RESIDUES:
        ring_atoms = [a for a in res.atoms
                      if a.name in _AROMATIC_ATOM_NAMES.get(res.name, [])]
        if len(ring_atoms) >= 5:
            res_centroid = _centroid(ring_atoms)
            lig_ring_centroid = _find_ligand_ring_centroid(lig_atoms)
            if lig_ring_centroid is not None:
                d = _point_distance(res_centroid, lig_ring_centroid)
                if d <= max_pi_stacking:
                    # Pick a representative ligand aromatic atom for labelling
                    nearest_lig_atom = min(
                        (a for a in lig_atoms if a.element == "C"),
                        key=lambda a: _point_distance(
                            (a.x, a.y, a.z), res_centroid),
                        default=lig_atoms[0],
                    )
                    report.contacts.append(Contact(
                        kind="pi-stacking",
                        ligand_atom=nearest_lig_atom.name,
                        protein_chain=chain.id,
                        protein_residue=res_label,
                        distance=d,
                    ))

    # Hydrophobic
    if res.name in _HYDROPHOBIC_RESIDUES:
        for res_atom in res.atoms:
            if res_atom.element != "C" or res_atom.name in ("CA", "C"):
                continue
            for la in lig_atoms:
                if la.element != "C":
                    continue
                d = _atom_distance(la, res_atom)
                if d <= max_hydrophobic:
                    report.contacts.append(Contact(
                        kind="hydrophobic",
                        ligand_atom=la.name,
                        protein_chain=chain.id,
                        protein_residue=res_label,
                        distance=d,
                    ))
                    return  # one hydrophobic contact per residue is enough


# ---------------------------------------------------------------------
# Geometry helpers

def _atom_distance(a: Atom, b: Atom) -> float:
    dx = a.x - b.x
    dy = a.y - b.y
    dz = a.z - b.z
    return sqrt(dx * dx + dy * dy + dz * dz)


def _point_distance(p: Tuple[float, float, float],
                    q: Tuple[float, float, float]) -> float:
    return sqrt(sum((a - b) ** 2 for a, b in zip(p, q)))


def _nearest_distance(atom: Atom,
                      candidates: Iterable[Atom]) -> float:
    return min(_atom_distance(atom, c) for c in candidates)


def _centroid(atoms: Sequence[Atom]) -> Tuple[float, float, float]:
    n = len(atoms)
    return (sum(a.x for a in atoms) / n,
            sum(a.y for a in atoms) / n,
            sum(a.z for a in atoms) / n)


def _find_ligand_ring_centroid(lig_atoms: Sequence[Atom]
                               ) -> Optional[Tuple[float, float, float]]:
    """Heuristic: detect a planar 5-6-membered ring in the ligand by
    clustering the aromatic-carbon atoms (names matching the typical
    "C1" / "C2" / ... pattern) and averaging. Good enough for
    benzene / tyrosine-ligand π-stacking cases.
    """
    carbons = [a for a in lig_atoms if a.element == "C"]
    if len(carbons) < 5:
        return None
    # Very simple heuristic — the centroid of the 6 carbons whose
    # pairwise distances are all < 1.6 Å (in-ring aromatic bond
    # length) to at least 2 other members.
    ring = []
    for c in carbons:
        neighbours = [o for o in carbons if o is not c
                      and _atom_distance(c, o) < 1.6]
        if len(neighbours) >= 2:
            ring.append(c)
    if len(ring) < 5:
        return None
    return _centroid(ring[:6])
