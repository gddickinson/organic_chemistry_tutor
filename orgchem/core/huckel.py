"""Simple Hückel MO theory — Phase 14a.

Computes π-system molecular orbitals for planar conjugated systems by
eigendecomposing the adjacency (connectivity) matrix of the π atoms.

Convention:
- Coulomb integral α = 0 (energies reported relative to α).
- Resonance integral β = −1 (negative by convention; bonding orbitals
  therefore have positive coefficients and **negative** energies).

So an MO energy of ``+1`` means ``α + β`` (bonding, 1 β-unit below α),
and ``−1`` means ``α − β`` (antibonding). We follow the Clayden /
Fleming convention where β is negative, so **bonding orbitals have
the most positive eigenvalues** of the adjacency matrix.

The π-atom subset is identified automatically for RDKit molecules:
every atom that (a) is aromatic or (b) participates in at least one
double bond contributes a π-electron. For canonical teaching demos
(ethene, butadiene, benzene, allyl cation / radical / anion,
cyclopentadienyl) this rule gives the right answer.

API:
    >>> from orgchem.core.huckel import huckel_for_smiles
    >>> res = huckel_for_smiles("C=CC=C")
    >>> res.n_pi_atoms, res.n_pi_electrons
    (4, 4)
    >>> [round(e, 3) for e in res.energies]
    [1.618, 0.618, -0.618, -1.618]
"""
from __future__ import annotations
from dataclasses import dataclass, field
import logging
from typing import List, Optional, Tuple

import numpy as np

log = logging.getLogger(__name__)


@dataclass
class HuckelResult:
    atom_indices: List[int]            # RDKit atom indices participating in π system
    n_pi_electrons: int                # total electrons filling the levels
    energies: List[float]              # eigenvalues, sorted descending (most bonding first)
    coefficients: List[List[float]]    # one MO coefficients list per eigenvalue
    adjacency: List[List[int]]         # π-subsystem adjacency (for diagnostics)

    # ---- convenience --------------------------------------------------

    @property
    def n_pi_atoms(self) -> int:
        return len(self.atom_indices)

    @property
    def occupations(self) -> List[int]:
        """Electrons in each MO (0, 1, or 2), in the same order as ``energies``."""
        n = len(self.energies)
        occ = [0] * n
        remaining = self.n_pi_electrons
        for i in range(n):
            take = min(2, remaining)
            occ[i] = take
            remaining -= take
            if remaining == 0:
                break
        return occ

    @property
    def homo_index(self) -> Optional[int]:
        last = None
        for i, o in enumerate(self.occupations):
            if o > 0:
                last = i
        return last

    @property
    def lumo_index(self) -> Optional[int]:
        for i, o in enumerate(self.occupations):
            if o == 0:
                return i
        return None

    @property
    def homo_energy(self) -> Optional[float]:
        i = self.homo_index
        return self.energies[i] if i is not None else None

    @property
    def lumo_energy(self) -> Optional[float]:
        i = self.lumo_index
        return self.energies[i] if i is not None else None

    @property
    def total_pi_energy(self) -> float:
        """Sum of occupied-orbital energies × occupancy."""
        return sum(o * e for o, e in zip(self.occupations, self.energies))


# ---------------------------------------------------------------------

def _identify_pi_atoms(mol) -> Tuple[List[int], List[Tuple[int, int]]]:
    """Return (atom indices in π system, list of π-bond pairs).

    An atom is in the π system if it's aromatic or involved in at least one
    non-single (double / aromatic) bond. Then we extend the subgraph one
    bond outward to any adjacent **sp²-like** atom — one with a formal
    charge, a radical electron, or that is otherwise conjugable — so the
    allyl cation / radical / anion series is captured automatically.
    π-bonds are the bonds between π atoms.
    """
    pi_atoms: List[int] = []
    for atom in mol.GetAtoms():
        if atom.GetIsAromatic():
            pi_atoms.append(atom.GetIdx())
            continue
        if any(b.GetBondTypeAsDouble() >= 1.5 for b in atom.GetBonds()):
            pi_atoms.append(atom.GetIdx())

    # Extend outward: include atoms directly bonded to an existing π atom
    # that carry a formal charge or radical electron (carbocation / carbanion
    # / carbon radical adjacent to C=C).
    pi_set = set(pi_atoms)
    extra: List[int] = []
    for idx in list(pi_set):
        for nbr in mol.GetAtomWithIdx(idx).GetNeighbors():
            if nbr.GetIdx() in pi_set:
                continue
            if nbr.GetFormalCharge() != 0 or nbr.GetNumRadicalElectrons() > 0:
                extra.append(nbr.GetIdx())
    pi_atoms = sorted(set(pi_atoms) | set(extra))
    pi_set = set(pi_atoms)

    pi_bonds: List[Tuple[int, int]] = []
    for bond in mol.GetBonds():
        a, b = bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()
        if a in pi_set and b in pi_set:
            pi_bonds.append((a, b))
    return pi_atoms, pi_bonds


def _count_pi_electrons(mol, pi_atoms: List[int]) -> int:
    """Pedagogical π-electron count.

    - Aromatic C / double-bonded sp² C → 1 π electron each.
    - Aromatic N with a lone pair in the ring plane (like pyridine) → 1 electron;
      aromatic N bonded to H (like pyrrole) contributes 2 (lone pair donated).
    - Aromatic O (furan) / S (thiophene) → 2 electrons (lone pair donated).
    - Charge adjustments: positive → remove 1, negative → add 1, summed over
      π atoms.

    This handles all the canonical 5/6-ring pedagogical cases plus neutral /
    cation / anion open-chain π systems.
    """
    total = 0
    for idx in pi_atoms:
        atom = mol.GetAtomWithIdx(idx)
        sym = atom.GetSymbol()
        aro = atom.GetIsAromatic()
        if sym in ("O", "S") and aro:
            total += 2
        elif sym == "N" and aro:
            if atom.GetTotalNumHs() >= 1:
                total += 2  # pyrrole-type
            else:
                total += 1  # pyridine-type
        else:
            total += 1
    # charge corrections
    charge = sum(mol.GetAtomWithIdx(i).GetFormalCharge() for i in pi_atoms)
    total -= charge
    return max(0, total)


def huckel(mol, pi_atoms: Optional[List[int]] = None,
           n_pi_electrons: Optional[int] = None) -> HuckelResult:
    """Run simple Hückel on an RDKit molecule.

    ``pi_atoms`` and ``n_pi_electrons`` are auto-detected by default; supply
    them to override when the heuristic doesn't capture the pedagogical case
    (e.g. the allyl cation — same atoms, different electron count).
    """
    if pi_atoms is None:
        pi_atoms, pi_bonds = _identify_pi_atoms(mol)
    else:
        pi_set = set(pi_atoms)
        pi_bonds = []
        for bond in mol.GetBonds():
            a, b = bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()
            if a in pi_set and b in pi_set:
                pi_bonds.append((a, b))

    if not pi_atoms:
        return HuckelResult(atom_indices=[], n_pi_electrons=0,
                            energies=[], coefficients=[], adjacency=[])

    n = len(pi_atoms)
    index_of = {idx: i for i, idx in enumerate(pi_atoms)}
    adj = np.zeros((n, n), dtype=float)
    for a, b in pi_bonds:
        i, j = index_of[a], index_of[b]
        adj[i, j] = 1.0
        adj[j, i] = 1.0

    # Eigendecomposition. The adjacency matrix is symmetric, so use eigh.
    eigvals, eigvecs = np.linalg.eigh(adj)
    # Sort descending — most bonding (largest +eigenvalue) first.
    order = np.argsort(-eigvals)
    eigvals = eigvals[order]
    eigvecs = eigvecs[:, order]

    if n_pi_electrons is None:
        n_pi_electrons = _count_pi_electrons(mol, pi_atoms)

    return HuckelResult(
        atom_indices=list(pi_atoms),
        n_pi_electrons=int(n_pi_electrons),
        energies=[float(e) for e in eigvals],
        coefficients=[list(map(float, eigvecs[:, i])) for i in range(n)],
        adjacency=[[int(x) for x in row] for row in adj.astype(int)],
    )


def huckel_for_smiles(smiles: str,
                      n_pi_electrons: Optional[int] = None) -> HuckelResult:
    """Convenience wrapper — parse SMILES then run :func:`huckel`."""
    from rdkit import Chem
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"Unparseable SMILES: {smiles!r}")
    return huckel(mol, n_pi_electrons=n_pi_electrons)
