"""Phase 36a (round 124) — headless structure-editor data core.

Pure-Python data model for a molecular drawing + RDKit-backed
round-trip to SMILES / mol-block.  No Qt imports, so the tests
run offline and any future GUI (Phase 36b `QGraphicsScene`
canvas) builds on a stable foundation.

Shape::

    Structure
        atoms:  list[Atom]
        bonds:  list[Bond]

    Atom
        element:   str    # "C", "N", "O", …
        charge:    int    # 0, ±1, ±2
        isotope:   int    # 0 = natural, else mass-number override
        radical:   int    # 0/1/2 unpaired electrons
        h_count:   int    # -1 → let RDKit infer; else explicit
        aromatic:  bool

    Bond
        begin_idx: int
        end_idx:   int
        order:     int   # 1 / 2 / 3; 4 = aromatic
        stereo:    str   # "none" / "wedge" / "dash" / "either"

Helpers:

- :func:`structure_from_smiles(smi)` → `Structure`
- :func:`structure_to_smiles(s)` → str (canonical)
- :func:`structure_to_molblock(s)` → str (CTAB / mol-block V2000)
- :func:`structure_from_molblock(block)` → `Structure`

Never raises on malformed input — returns ``None`` so GUI
callers can surface a clean error message instead of an
RDKit traceback.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional


#: Wedge-stereo tags the renderer recognises.  Mirrors the
#: `Chem.BondDir` enum minus rare cases the GUI won't expose.
_VALID_STEREO = ("none", "wedge", "dash", "either")

#: Maximum valence-neutral element set the tool palette will
#: expose directly.  Anything else flows through the *"custom…"*
#: dialog (Phase 36b).
_COMMON_ELEMENTS = (
    "C", "N", "O", "P", "S",
    "F", "Cl", "Br", "I",
    "H", "B", "Si", "Se",
)


@dataclass
class Atom:
    element: str = "C"
    charge: int = 0
    isotope: int = 0
    radical: int = 0
    h_count: int = -1        # -1 = infer from valence model
    aromatic: bool = False
    #: Tetrahedral stereochemistry tag — ``"none"`` / ``"CW"`` /
    #: ``"CCW"``.  Mirrors RDKit's ``ChiralType`` so SMILES-style
    #: `[C@H]` / `[C@@H]` atom-centric stereo survives the
    #: round-trip without needing explicit wedge/dash bonds.
    chirality: str = "none"

    def __post_init__(self) -> None:
        if not self.element:
            self.element = "C"
        if self.chirality not in ("none", "CW", "CCW"):
            self.chirality = "none"


@dataclass
class Bond:
    begin_idx: int
    end_idx: int
    order: int = 1           # 1 / 2 / 3; 4 = aromatic
    stereo: str = "none"

    def __post_init__(self) -> None:
        if self.stereo not in _VALID_STEREO:
            self.stereo = "none"


@dataclass
class Structure:
    atoms: List[Atom] = field(default_factory=list)
    bonds: List[Bond] = field(default_factory=list)

    def add_atom(self, element: str = "C", **kw) -> int:
        """Append an :class:`Atom` and return its index."""
        self.atoms.append(Atom(element=element, **kw))
        return len(self.atoms) - 1

    def add_bond(self, a: int, b: int, order: int = 1,
                 stereo: str = "none") -> int:
        """Append a :class:`Bond` between atoms *a* and *b*.
        Returns the bond index."""
        if a == b:
            raise ValueError("Self-loop: bond endpoints must differ.")
        if not (0 <= a < len(self.atoms) and 0 <= b < len(self.atoms)):
            raise IndexError(f"bond {(a, b)} references atoms "
                             f"outside the structure.")
        self.bonds.append(Bond(begin_idx=a, end_idx=b,
                               order=order, stereo=stereo))
        return len(self.bonds) - 1

    # ---- introspection -------------------------------------

    @property
    def n_atoms(self) -> int:
        return len(self.atoms)

    @property
    def n_bonds(self) -> int:
        return len(self.bonds)

    @property
    def is_empty(self) -> bool:
        return not self.atoms

    def neighbours(self, atom_idx: int) -> List[int]:
        """Return the atom indices directly bonded to *atom_idx*."""
        out: List[int] = []
        for b in self.bonds:
            if b.begin_idx == atom_idx:
                out.append(b.end_idx)
            elif b.end_idx == atom_idx:
                out.append(b.begin_idx)
        return out


# ---- RDKit round-trip ----------------------------------------

_BOND_ORDER_TO_RDKIT = {1: "SINGLE", 2: "DOUBLE", 3: "TRIPLE", 4: "AROMATIC"}
_BOND_STEREO_TO_RDKIT = {
    "none":   "NONE",
    "wedge":  "BEGINWEDGE",
    "dash":   "BEGINDASH",
    "either": "UNKNOWN",
}
_BOND_STEREO_FROM_RDKIT = {v: k for k, v in _BOND_STEREO_TO_RDKIT.items()}


def _rdkit():
    """Lazy RDKit import so the dataclasses above can be used
    in environments where RDKit isn't installed yet (headless
    workers, minimal CI configs)."""
    from rdkit import Chem
    return Chem


def structure_from_smiles(smi: str) -> Optional[Structure]:
    """Parse a SMILES into a :class:`Structure`.  Returns
    ``None`` if RDKit can't parse the string — no exception."""
    if not smi or not isinstance(smi, str):
        return None
    Chem = _rdkit()
    try:
        mol = Chem.MolFromSmiles(smi.strip())
    except Exception:  # noqa: BLE001
        return None
    if mol is None:
        return None
    return _structure_from_rdkit(mol)


def structure_from_molblock(block: str) -> Optional[Structure]:
    """Parse a V2000 mol-block (CTAB).  Returns ``None`` on
    parse failure."""
    if not block or not isinstance(block, str):
        return None
    Chem = _rdkit()
    try:
        mol = Chem.MolFromMolBlock(block, sanitize=True, removeHs=True)
    except Exception:  # noqa: BLE001
        return None
    if mol is None:
        return None
    return _structure_from_rdkit(mol)


def structure_to_smiles(s: Structure,
                        *, canonical: bool = True) -> Optional[str]:
    """Convert a :class:`Structure` to SMILES.  Returns ``None``
    if the structure is empty or the RDKit conversion fails."""
    if s.is_empty:
        return None
    mol = _rdkit_from_structure(s)
    if mol is None:
        return None
    Chem = _rdkit()
    try:
        return Chem.MolToSmiles(mol, canonical=canonical)
    except Exception:  # noqa: BLE001
        return None


def structure_to_molblock(s: Structure) -> Optional[str]:
    """Convert a :class:`Structure` to a V2000 mol-block, suitable
    for *File → Export → MOL* (Phase 36g)."""
    if s.is_empty:
        return None
    mol = _rdkit_from_structure(s)
    if mol is None:
        return None
    Chem = _rdkit()
    try:
        from rdkit.Chem import AllChem
        AllChem.Compute2DCoords(mol)
        return Chem.MolToMolBlock(mol)
    except Exception:  # noqa: BLE001
        return None


# ---- internal bridge -----------------------------------------

def _structure_from_rdkit(mol) -> Structure:
    """Convert an RDKit `Mol` into the headless :class:`Structure`
    shape.  Called by the public SMILES + mol-block parsers."""
    Chem = _rdkit()
    s = Structure()
    _chi_to_str = {
        Chem.ChiralType.CHI_UNSPECIFIED: "none",
        Chem.ChiralType.CHI_TETRAHEDRAL_CW: "CW",
        Chem.ChiralType.CHI_TETRAHEDRAL_CCW: "CCW",
    }
    for atom in mol.GetAtoms():
        s.atoms.append(Atom(
            element=atom.GetSymbol(),
            charge=atom.GetFormalCharge(),
            isotope=atom.GetIsotope(),
            radical=atom.GetNumRadicalElectrons(),
            # Keep h_count at -1 (infer) unless the input
            # explicitly set explicit hydrogens.
            h_count=(atom.GetNumExplicitHs()
                     if atom.GetNoImplicit() else -1),
            aromatic=atom.GetIsAromatic(),
            chirality=_chi_to_str.get(atom.GetChiralTag(), "none"),
        ))
    for bond in mol.GetBonds():
        bt = bond.GetBondType()
        if bt == Chem.BondType.SINGLE:
            order = 1
        elif bt == Chem.BondType.DOUBLE:
            order = 2
        elif bt == Chem.BondType.TRIPLE:
            order = 3
        elif bt == Chem.BondType.AROMATIC:
            order = 4
        else:
            order = 1   # unknown / dative treated as single
        stereo = _BOND_STEREO_FROM_RDKIT.get(
            bond.GetBondDir().name, "none")
        s.bonds.append(Bond(
            begin_idx=bond.GetBeginAtomIdx(),
            end_idx=bond.GetEndAtomIdx(),
            order=order,
            stereo=stereo,
        ))
    return s


def _rdkit_from_structure(s: Structure):
    """Rebuild an RDKit editable `Mol` from a :class:`Structure`.
    Returns the sanitised `Mol`, or ``None`` if sanitisation
    fails (invalid valence, disconnected graph with bad flags, …)."""
    Chem = _rdkit()
    emol = Chem.EditableMol(Chem.Mol())
    chi_from_str = {
        "none": Chem.ChiralType.CHI_UNSPECIFIED,
        "CW":   Chem.ChiralType.CHI_TETRAHEDRAL_CW,
        "CCW":  Chem.ChiralType.CHI_TETRAHEDRAL_CCW,
    }
    for atom in s.atoms:
        at = Chem.Atom(atom.element)
        at.SetFormalCharge(int(atom.charge))
        if atom.isotope:
            at.SetIsotope(int(atom.isotope))
        if atom.radical:
            at.SetNumRadicalElectrons(int(atom.radical))
        if atom.h_count >= 0:
            at.SetNoImplicit(True)
            at.SetNumExplicitHs(int(atom.h_count))
        if atom.aromatic:
            at.SetIsAromatic(True)
        at.SetChiralTag(chi_from_str.get(atom.chirality,
                                         Chem.ChiralType.CHI_UNSPECIFIED))
        emol.AddAtom(at)
    bond_type_map = {
        1: Chem.BondType.SINGLE,
        2: Chem.BondType.DOUBLE,
        3: Chem.BondType.TRIPLE,
        4: Chem.BondType.AROMATIC,
    }
    bond_dir_map = {
        "none":   Chem.BondDir.NONE,
        "wedge":  Chem.BondDir.BEGINWEDGE,
        "dash":   Chem.BondDir.BEGINDASH,
        "either": Chem.BondDir.UNKNOWN,
    }
    for b in s.bonds:
        bt = bond_type_map.get(b.order, Chem.BondType.SINGLE)
        bidx = emol.AddBond(b.begin_idx, b.end_idx, bt)
    mol = emol.GetMol()
    # Apply bond directions after AddBond (RDKit needs the
    # final Mol to index by bond pointer, not index).
    for i, b in enumerate(s.bonds):
        if b.stereo != "none":
            bond = mol.GetBondBetweenAtoms(b.begin_idx, b.end_idx)
            if bond is not None:
                bond.SetBondDir(bond_dir_map[b.stereo])
    try:
        Chem.SanitizeMol(mol)
    except Exception:  # noqa: BLE001
        # Try again without aromaticity / valence to support
        # partially-valid user drawings.
        try:
            Chem.SanitizeMol(
                mol,
                sanitizeOps=Chem.SanitizeFlags.SANITIZE_ALL
                - Chem.SanitizeFlags.SANITIZE_PROPERTIES
                - Chem.SanitizeFlags.SANITIZE_KEKULIZE,
            )
        except Exception:  # noqa: BLE001
            return None
    return mol
