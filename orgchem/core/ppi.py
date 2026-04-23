"""Protein-protein interface analyser — Phase 24j.

Given a multi-chain :class:`Protein`, enumerate the non-covalent
contacts that stitch each pair of chains together. Same geometric
criteria as the Phase 24e ligand-binding analyser, applied to *two
protein chains* rather than *chain vs ligand*:

- **H-bond** — heavy-atom N/O-to-N/O distance ≤ 3.5 Å.
- **Salt bridge** — charged side-chain atom distance ≤ 4.5 Å between
  an ASP/GLU carboxylate and an ARG/LYS/HIS basic nitrogen (either
  direction).
- **π-stacking** — aromatic-ring centroid distance ≤ 5.5 Å between
  two PHE / TYR / TRP / HIS rings.
- **Hydrophobic** — any C-C distance ≤ 4.5 Å where both atoms are on
  apolar side chains (ALA/VAL/LEU/ILE/MET/PRO/PHE/TRP/TYR).

The output is a list of :class:`PPIInterface` records — one per chain
*pair* that has at least one contact. Each record carries the
contacts list, per-kind counts, and the "interface residue" sets on
either side (a bite-sized view suitable for teaching and for
downstream ΔSASA / rim-vs-core analyses).

This module is deliberately **dep-free** (no numpy/scipy/Biopython)
and reuses the residue-property tables from
:mod:`orgchem.core.binding_contacts` so the two analysers behave
consistently.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from math import sqrt
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

from orgchem.core.binding_contacts import (
    _AROMATIC_ATOM_NAMES,
    _AROMATIC_RESIDUES,
    _HBOND_ACCEPTOR_ELEMENTS,
    _HBOND_DONOR_NAMES,
    _HYDROPHOBIC_RESIDUES,
    _NEGATIVE_RESIDUES,
    _POSITIVE_RESIDUES,
)
from orgchem.core.protein import Atom, Chain, Protein, Residue


# ---------------------------------------------------------------------

@dataclass(frozen=True)
class PPIContact:
    """One non-covalent contact between two protein chains."""
    kind: str                 # "h-bond" / "salt-bridge" / "pi-stacking" / "hydrophobic"
    chain_a: str
    residue_a: str            # "ASP102"
    atom_a: str               # "OD1"
    chain_b: str
    residue_b: str
    atom_b: str
    distance: float           # Å


@dataclass
class PPIInterface:
    """All contacts between one pair of chains (``chain_a`` / ``chain_b``)."""
    pdb_id: str
    chain_a: str
    chain_b: str
    contacts: List[PPIContact] = field(default_factory=list)

    @property
    def n_contacts(self) -> int:
        return len(self.contacts)

    @property
    def residues_a(self) -> List[str]:
        """Ordered unique ``"ASP102"``-style residues on chain A."""
        return sorted({c.residue_a for c in self.contacts})

    @property
    def residues_b(self) -> List[str]:
        return sorted({c.residue_b for c in self.contacts})

    def by_kind(self, kind: str) -> List[PPIContact]:
        return [c for c in self.contacts if c.kind == kind]

    def summary(self) -> Dict[str, object]:
        counts: Dict[str, int] = {}
        for c in self.contacts:
            counts[c.kind] = counts.get(c.kind, 0) + 1
        return {
            "pdb_id": self.pdb_id,
            "chain_a": self.chain_a,
            "chain_b": self.chain_b,
            "n_contacts": self.n_contacts,
            "by_kind": counts,
            "interface_residues_a": self.residues_a,
            "interface_residues_b": self.residues_b,
            "contacts": [
                {"kind": c.kind,
                 "a": f"{c.chain_a}:{c.residue_a}:{c.atom_a}",
                 "b": f"{c.chain_b}:{c.residue_b}:{c.atom_b}",
                 "distance": round(c.distance, 2)}
                for c in self.contacts
            ],
        }


# ---------------------------------------------------------------------
# Public API

def analyse_ppi(protein: Protein,
                max_hbond: float = 3.5,
                max_salt_bridge: float = 4.5,
                max_pi_stacking: float = 5.5,
                max_hydrophobic: float = 4.5) -> List[PPIInterface]:
    """Return one :class:`PPIInterface` per chain pair with ≥1 contact.

    Order: lexicographic by ``(chain_a, chain_b)`` where ``chain_a <
    chain_b``. Interfaces with no contacts are omitted entirely.
    """
    interfaces: List[PPIInterface] = []
    chains = protein.chains
    for i, ca in enumerate(chains):
        for cb in chains[i + 1:]:
            iface = analyse_ppi_pair(
                protein, ca.id, cb.id,
                max_hbond=max_hbond,
                max_salt_bridge=max_salt_bridge,
                max_pi_stacking=max_pi_stacking,
                max_hydrophobic=max_hydrophobic,
            )
            if iface.n_contacts:
                interfaces.append(iface)
    return interfaces


def analyse_ppi_pair(protein: Protein, chain_a_id: str, chain_b_id: str,
                     max_hbond: float = 3.5,
                     max_salt_bridge: float = 4.5,
                     max_pi_stacking: float = 5.5,
                     max_hydrophobic: float = 4.5) -> PPIInterface:
    """Analyse a single chain pair. Empty interface if a chain is missing."""
    iface = PPIInterface(pdb_id=protein.pdb_id,
                         chain_a=chain_a_id, chain_b=chain_b_id)
    ca = protein.get_chain(chain_a_id)
    cb = protein.get_chain(chain_b_id)
    if ca is None or cb is None:
        return iface
    max_cut = max(max_hbond, max_salt_bridge,
                  max_pi_stacking, max_hydrophobic)
    # Pre-compute residue pivots for early-exit pruning.
    b_pivots = [(_residue_pivot(rb), rb) for rb in cb.residues]
    for ra in ca.residues:
        pa = _residue_pivot(ra)
        if pa is None:
            continue
        for pb, rb in b_pivots:
            if pb is None:
                continue
            if _distance(pa, pb) > 15.0 + max_cut:
                continue
            _score_residue_pair(iface, ra, rb, chain_a_id, chain_b_id,
                                max_hbond=max_hbond,
                                max_salt_bridge=max_salt_bridge,
                                max_pi_stacking=max_pi_stacking,
                                max_hydrophobic=max_hydrophobic)
    return iface


def ppi_summary(interfaces: Sequence[PPIInterface]) -> Dict[str, object]:
    """Top-level dict for the whole protein — suitable for agent return."""
    total = sum(i.n_contacts for i in interfaces)
    return {
        "n_interfaces": len(interfaces),
        "total_contacts": total,
        "interfaces": [i.summary() for i in interfaces],
    }


# ---------------------------------------------------------------------
# Internals

def _score_residue_pair(iface: PPIInterface,
                        res_a: Residue, res_b: Residue,
                        chain_a: str, chain_b: str,
                        max_hbond: float,
                        max_salt_bridge: float,
                        max_pi_stacking: float,
                        max_hydrophobic: float) -> None:
    label_a = f"{res_a.name}{res_a.seq_id}"
    label_b = f"{res_b.name}{res_b.seq_id}"

    # H-bond (bidirectional donor/acceptor)
    for aa in res_a.atoms:
        if aa.element not in _HBOND_ACCEPTOR_ELEMENTS:
            continue
        for bb in res_b.atoms:
            if bb.element not in _HBOND_ACCEPTOR_ELEMENTS:
                continue
            d = _atom_distance(aa, bb)
            if d <= max_hbond:
                donor_ok = (aa.name in _HBOND_DONOR_NAMES
                            or bb.name in _HBOND_DONOR_NAMES
                            or aa.name == "N" or bb.name == "N")
                if donor_ok:
                    iface.contacts.append(PPIContact(
                        kind="h-bond",
                        chain_a=chain_a, residue_a=label_a, atom_a=aa.name,
                        chain_b=chain_b, residue_b=label_b, atom_b=bb.name,
                        distance=d,
                    ))
                    break

    # Salt bridge — opposite charges only
    if (res_a.name in _POSITIVE_RESIDUES and res_b.name in _NEGATIVE_RESIDUES) or \
       (res_a.name in _NEGATIVE_RESIDUES and res_b.name in _POSITIVE_RESIDUES):
        sb_a = [a for a in res_a.atoms
                if a.element in ("N", "O")
                and a.name not in ("N", "O", "CA", "C")]
        sb_b = [a for a in res_b.atoms
                if a.element in ("N", "O")
                and a.name not in ("N", "O", "CA", "C")]
        found = False
        for aa in sb_a:
            if found:
                break
            for bb in sb_b:
                d = _atom_distance(aa, bb)
                if d <= max_salt_bridge:
                    iface.contacts.append(PPIContact(
                        kind="salt-bridge",
                        chain_a=chain_a, residue_a=label_a, atom_a=aa.name,
                        chain_b=chain_b, residue_b=label_b, atom_b=bb.name,
                        distance=d,
                    ))
                    found = True
                    break

    # π-stacking — two aromatic residues, centroid-to-centroid
    if res_a.name in _AROMATIC_RESIDUES and res_b.name in _AROMATIC_RESIDUES:
        ring_a = [a for a in res_a.atoms
                  if a.name in _AROMATIC_ATOM_NAMES.get(res_a.name, [])]
        ring_b = [a for a in res_b.atoms
                  if a.name in _AROMATIC_ATOM_NAMES.get(res_b.name, [])]
        if len(ring_a) >= 5 and len(ring_b) >= 5:
            ca_ = _centroid(ring_a)
            cb_ = _centroid(ring_b)
            d = _distance(ca_, cb_)
            if d <= max_pi_stacking:
                # Label with each side's CG as a representative ring atom.
                repa = next((a for a in ring_a if a.name == "CG"), ring_a[0])
                repb = next((a for a in ring_b if a.name == "CG"), ring_b[0])
                iface.contacts.append(PPIContact(
                    kind="pi-stacking",
                    chain_a=chain_a, residue_a=label_a, atom_a=repa.name,
                    chain_b=chain_b, residue_b=label_b, atom_b=repb.name,
                    distance=d,
                ))

    # Hydrophobic — any C-C short contact between apolar side-chains.
    if (res_a.name in _HYDROPHOBIC_RESIDUES
            and res_b.name in _HYDROPHOBIC_RESIDUES):
        found = False
        for aa in res_a.atoms:
            if found:
                break
            if aa.element != "C" or aa.name in ("CA", "C"):
                continue
            for bb in res_b.atoms:
                if bb.element != "C" or bb.name in ("CA", "C"):
                    continue
                d = _atom_distance(aa, bb)
                if d <= max_hydrophobic:
                    iface.contacts.append(PPIContact(
                        kind="hydrophobic",
                        chain_a=chain_a, residue_a=label_a, atom_a=aa.name,
                        chain_b=chain_b, residue_b=label_b, atom_b=bb.name,
                        distance=d,
                    ))
                    found = True
                    break


# Geometry primitives duplicated from binding_contacts (kept private so
# we don't re-export module internals).

def _atom_distance(a: Atom, b: Atom) -> float:
    dx = a.x - b.x
    dy = a.y - b.y
    dz = a.z - b.z
    return sqrt(dx * dx + dy * dy + dz * dz)


def _distance(p: Tuple[float, float, float],
              q: Tuple[float, float, float]) -> float:
    return sqrt(sum((a - b) ** 2 for a, b in zip(p, q)))


def _centroid(atoms: Sequence[Atom]) -> Tuple[float, float, float]:
    n = len(atoms)
    return (sum(a.x for a in atoms) / n,
            sum(a.y for a in atoms) / n,
            sum(a.z for a in atoms) / n)


def _residue_pivot(res: Residue) -> Optional[Tuple[float, float, float]]:
    ca = next((a for a in res.atoms if a.name == "CA"), None)
    if ca is not None:
        return (ca.x, ca.y, ca.z)
    if res.atoms:
        a0 = res.atoms[0]
        return (a0.x, a0.y, a0.z)
    return None
