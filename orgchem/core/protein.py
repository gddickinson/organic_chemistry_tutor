"""Lightweight PDB parser + ``Protein`` accessor — Phase 24a.

Built deliberately **without Biopython** so the base install stays slim
(Biopython is a ~40 MB dep and not every OrgChem user will need it).
Parses only ``ATOM`` / ``HETATM`` records, which is enough for:

- Chain / residue enumeration (24a)
- Binding-site residue lookups (24d)
- Contact geometry for PLIP-free interaction analysis (24e)

For anything deeper (DSSP secondary structure, SASA, super-position),
callers should install Biopython and use the raw `Bio.PDB` API —
documented as an optional enhancement in `ROADMAP.md`.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple, Union


@dataclass(frozen=True)
class Atom:
    serial: int
    name: str               # "CA", "N", "OG", etc.
    element: str            # "C", "N", "O", "S", ...
    x: float
    y: float
    z: float
    b_factor: float = 0.0
    alt_loc: str = ""       # alternate-location indicator (A / B / "")
    is_hetatm: bool = False


@dataclass
class Residue:
    name: str               # 3-letter code, e.g. "ALA", "HIS", "HOH", "ATP"
    seq_id: int             # residue sequence number
    chain: str              # chain letter, e.g. "A"
    insertion_code: str = ""
    atoms: List[Atom] = field(default_factory=list)

    @property
    def is_standard_amino_acid(self) -> bool:
        return self.name in _STANDARD_AA

    @property
    def is_nucleotide(self) -> bool:
        return self.name in _NUCLEOTIDES

    @property
    def is_hetero(self) -> bool:
        """True for non-standard residues (HETATMs, excluding water)."""
        return bool(self.atoms) and self.atoms[0].is_hetatm


@dataclass
class Chain:
    id: str
    residues: List[Residue] = field(default_factory=list)

    @property
    def sequence(self) -> str:
        """1-letter amino-acid sequence for standard residues in this chain."""
        return "".join(_AA_3_TO_1.get(r.name, "X")
                       for r in self.residues
                       if r.is_standard_amino_acid)


@dataclass
class Protein:
    """Parsed PDB structure."""
    pdb_id: str
    title: str = ""
    chains: List[Chain] = field(default_factory=list)
    hetatm_residues: List[Residue] = field(default_factory=list)

    # -------------------- convenience -----------------------

    @property
    def chain_ids(self) -> List[str]:
        return [c.id for c in self.chains]

    def get_chain(self, chain_id: str) -> Optional[Chain]:
        for c in self.chains:
            if c.id == chain_id:
                return c
        return None

    @property
    def ligand_residues(self) -> List[Residue]:
        """HETATM residues excluding water and standard ions."""
        return [r for r in self.hetatm_residues
                if r.name not in _IGNORE_HET]

    @property
    def n_residues(self) -> int:
        return sum(len(c.residues) for c in self.chains)

    @property
    def n_atoms(self) -> int:
        n = sum(len(r.atoms) for c in self.chains for r in c.residues)
        n += sum(len(r.atoms) for r in self.hetatm_residues)
        return n

    def summary(self) -> Dict[str, object]:
        return {
            "pdb_id": self.pdb_id,
            "title": self.title,
            "n_chains": len(self.chains),
            "chain_ids": self.chain_ids,
            "n_residues": self.n_residues,
            "n_atoms": self.n_atoms,
            "ligands": sorted({r.name for r in self.ligand_residues}),
            "has_water": any(r.name == "HOH" for r in self.hetatm_residues),
        }


# -------------------- parser -----------------------

_IGNORE_HET = {"HOH", "WAT", "DOD", "D2O",
               "NA", "K", "MG", "CA", "ZN", "FE", "MN", "CL"}

_STANDARD_AA = {
    "ALA", "ARG", "ASN", "ASP", "CYS", "GLN", "GLU", "GLY",
    "HIS", "ILE", "LEU", "LYS", "MET", "PHE", "PRO", "SER",
    "THR", "TRP", "TYR", "VAL",
    "SEC", "PYL",            # selenocysteine, pyrrolysine
}
_NUCLEOTIDES = {"DA", "DT", "DG", "DC", "DU", "A", "T", "G", "C", "U"}

_AA_3_TO_1 = {
    "ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C",
    "GLN": "Q", "GLU": "E", "GLY": "G", "HIS": "H", "ILE": "I",
    "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F", "PRO": "P",
    "SER": "S", "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V",
    "SEC": "U", "PYL": "O",
}


def parse_pdb_text(text: str, pdb_id: str = "") -> Protein:
    """Parse a PDB-format string into a :class:`Protein`.

    Handles ATOM, HETATM, TITLE records. Uses strict column offsets
    per the PDB specification (columns are character-fixed, not
    whitespace-split).
    """
    protein = Protein(pdb_id=pdb_id)
    title_parts: List[str] = []
    chain_map: Dict[str, Chain] = {}
    current_residue_key: Optional[Tuple[str, int, str, str]] = None
    current_residue: Optional[Residue] = None
    hetatm_map: Dict[Tuple[str, int, str, str], Residue] = {}

    for raw in text.splitlines():
        if raw.startswith("TITLE"):
            # col 11-80 after "TITLE   " prefix
            title_parts.append(raw[10:80].strip())
            continue
        if raw.startswith(("ATOM", "HETATM")):
            try:
                atom = _parse_atom_line(raw)
            except Exception:
                continue
            is_het = raw.startswith("HETATM")
            resname = raw[17:20].strip()
            chain_id = raw[21:22].strip() or "A"
            seq_id = int(raw[22:26])
            icode = raw[26:27].strip()

            key = (resname, seq_id, chain_id, icode)
            if is_het and resname in _IGNORE_HET:
                # Waters + metal ions kept in hetatm_residues for
                # completeness but not counted as ligands.
                pass

            if is_het:
                residue = hetatm_map.get(key)
                if residue is None:
                    residue = Residue(name=resname, seq_id=seq_id,
                                      chain=chain_id, insertion_code=icode)
                    hetatm_map[key] = residue
                    protein.hetatm_residues.append(residue)
                residue.atoms.append(atom)
            else:
                # Standard residue
                if key != current_residue_key:
                    chain = chain_map.get(chain_id)
                    if chain is None:
                        chain = Chain(id=chain_id)
                        chain_map[chain_id] = chain
                        protein.chains.append(chain)
                    current_residue = Residue(
                        name=resname, seq_id=seq_id, chain=chain_id,
                        insertion_code=icode,
                    )
                    chain.residues.append(current_residue)
                    current_residue_key = key
                current_residue.atoms.append(atom)

    protein.title = " ".join(p for p in title_parts if p).strip()
    return protein


def _parse_atom_line(line: str) -> Atom:
    """Parse one ATOM or HETATM line per PDB column-fixed spec.

    PDB format (1-indexed columns):
      1-6    record name
      7-11   serial
      13-16  atom name (right-justified in some writers)
      17     alt loc
      18-20  residue name
      22     chain
      23-26  residue seq id
      27     insertion code
      31-38  x (real 8.3)
      39-46  y
      47-54  z
      55-60  occupancy
      61-66  b-factor
      77-78  element (right-justified)
    """
    serial = int(line[6:11].strip() or 0)
    name = line[12:16].strip()
    alt_loc = line[16:17].strip()
    x = float(line[30:38].strip())
    y = float(line[38:46].strip())
    z = float(line[46:54].strip())
    b_factor = float(line[60:66].strip() or 0.0)
    elem = line[76:78].strip() or _infer_element(name)
    return Atom(
        serial=serial, name=name, element=elem,
        x=x, y=y, z=z, b_factor=b_factor, alt_loc=alt_loc,
        is_hetatm=line.startswith("HETATM"),
    )


def _infer_element(atom_name: str) -> str:
    """Last-resort element inference when cols 77-78 are blank."""
    if not atom_name:
        return ""
    # Heavy atoms usually start with letter(s); H atoms named HA/HB etc.
    first = atom_name[0]
    if first.isdigit():
        return atom_name[1:2].upper() if len(atom_name) > 1 else ""
    return first.upper()


def parse_pdb_file(path: Union[str, Path], pdb_id: str = "") -> Protein:
    p = Path(path)
    if not pdb_id:
        pdb_id = p.stem.upper()
    return parse_pdb_text(p.read_text(), pdb_id=pdb_id)


# -------------------- seeded teaching set -----------------------

@dataclass(frozen=True)
class SeededProtein:
    pdb_id: str
    name: str
    ligand_name: str
    teaching_story: str


SEEDED_PROTEINS: List[SeededProtein] = [
    SeededProtein(
        pdb_id="2YDO",
        name="Human adenosine A2A receptor",
        ligand_name="Adenosine",
        teaching_story=(
            "Caffeine antagonises this receptor — the 'why caffeine "
            "keeps you awake' case study. Compare to 2AK4 for "
            "caffeine-bound form."
        ),
    ),
    SeededProtein(
        pdb_id="1EQG",
        name="Cyclooxygenase-1 (COX-1)",
        ligand_name="IBP (ibuprofen)",
        teaching_story=(
            "Ibuprofen bound in the arachidonic-acid channel. "
            "Shows how NSAIDs compete with substrate binding."
        ),
    ),
    SeededProtein(
        pdb_id="1HWK",
        name="HMG-CoA reductase (catalytic portion)",
        ligand_name="Atorvastatin",
        teaching_story=(
            "Statin bound to the mevalonate-forming active site. "
            "Direct view of the pharmacophore that defined the 'greatest "
            "drug class of the 1990s'."
        ),
    ),
    SeededProtein(
        pdb_id="1HPV",
        name="HIV-1 protease homodimer with ritonavir",
        ligand_name="Ritonavir (RIT)",
        teaching_story=(
            "Active site at the homodimer interface — the PPI-vs-ligand "
            "unification teaching story. Ritonavir is a peptidomimetic "
            "transition-state mimic."
        ),
    ),
    SeededProtein(
        pdb_id="4INS",
        name="Insulin hexamer",
        ligand_name="Zn (structural)",
        teaching_story=(
            "Classical PPI teaching case. Six chains (two insulin dimers "
            "+ zinc coordination) — illustrates how storage form of a "
            "hormone is oligomeric."
        ),
    ),
    SeededProtein(
        pdb_id="1D12",
        name="Doxorubicin-DNA intercalation complex",
        ligand_name="Doxorubicin (DM1)",
        teaching_story=(
            "Classic DNA-ligand intercalation. Aglycone stacks between "
            "base pairs; amino sugar projects into the minor groove. "
            "Teaching anchor for NA-ligand analysis (Phase 24k)."
        ),
    ),

    # ---- Phase 31l content expansion (2026-04-23) ---------------------
    SeededProtein(
        pdb_id="1LYZ",
        name="Hen egg-white lysozyme",
        ligand_name="",
        teaching_story=(
            "The first enzyme to have its 3D structure solved (Phillips, "
            "1965) and the archetypal glycosidase mechanism. Hydrolyses "
            "β-1,4 GlcNAc–MurNAc bonds in bacterial peptidoglycan. Glu35 "
            "+ Asp52 act as general acid + nucleophile-stabiliser — the "
            "canonical Koshland double-displacement / Phillips oxocarbenium "
            "mechanism debate lives here."
        ),
    ),
    SeededProtein(
        pdb_id="1MBN",
        name="Sperm-whale myoglobin",
        ligand_name="HEM (heme-b)",
        teaching_story=(
            "The first protein structure ever solved (Kendrew, 1958 — "
            "shared 1962 Nobel). Single globin fold with a heme prosthetic "
            "group. Shows how a distal histidine tunes O₂ vs CO "
            "discrimination. Foundation structure for the globin family."
        ),
    ),
    SeededProtein(
        pdb_id="1EMA",
        name="Green fluorescent protein (GFP)",
        ligand_name="CRO (chromophore: Thr-Tyr-Gly autocycle)",
        teaching_story=(
            "The 11-strand β-barrel that revolutionised cell biology "
            "(Shimomura / Chalfie / Tsien, 2008 Nobel). Chromophore is "
            "formed post-translationally by autocyclisation of the S65-"
            "Y66-G67 tripeptide inside the barrel. Structural anchor for "
            "fluorescent-tag teaching and protein-engineering case studies "
            "(EGFP, YFP, CFP)."
        ),
    ),

    # ---- Phase 31l round 107 — haemoglobin R-state -----------------
    SeededProtein(
        pdb_id="1HHO",
        name="Human oxy-haemoglobin (R-state)",
        ligand_name="HEM (heme-b) + OXY (bound O₂)",
        teaching_story=(
            "The R-state (oxygenated) tetramer of adult human Hb (α₂β₂) "
            "solved by Shaanan 1983 at 2.1 Å. Pairs pedagogically with "
            "the round-47 myoglobin 1MBN entry: same globin fold, same "
            "heme-b prosthetic group, but four subunits interlocking at "
            "an α₁β₂ interface that rotates ~15° between T (deoxy) and "
            "R (oxy) quaternary states. The canonical Monod-Wyman-Changeux "
            "cooperativity teaching anchor — why oxygen binding is "
            "sigmoidal, not hyperbolic. Compare with 2HHB for the T-state "
            "deoxy form to see the ~15° rotation directly."
        ),
    ),

    # ---- Phase 31l round 114 — KcsA K⁺ channel ---------------------
    SeededProtein(
        pdb_id="1BL8",
        name="KcsA potassium channel (Streptomyces lividans)",
        ligand_name="K (four K⁺ ions in the selectivity filter)",
        teaching_story=(
            "Doyle / MacKinnon 1998 *Science* 280:69 — the first "
            "structure of an ion channel at atomic resolution (Nobel "
            "2003). Homotetrameric transmembrane helix bundle with a "
            "central pore lined by the canonical TVGYG selectivity "
            "filter: four backbone carbonyl O atoms per ring exactly "
            "mimic the hydration shell of a K⁺ ion, so dehydration + "
            "re-solvation inside the filter is nearly isoergic for K⁺ "
            "— but energetically costly for the smaller Na⁺ (which "
            "doesn't fill the cage). The 'molecular calipers' "
            "explanation for ~10 000-fold K⁺/Na⁺ selectivity. Pairs "
            "with 1HHO as a second 'protein architecture dictates "
            "specificity' teaching anchor — cooperativity in Hb, "
            "dehydration geometry in KcsA."
        ),
    ),

    # ---- Phase 31l round 115 — nucleosome + antibody Fab -----------
    SeededProtein(
        pdb_id="1AOI",
        name="Nucleosome core particle (X. laevis)",
        ligand_name="",
        teaching_story=(
            "Luger / Richmond 1997 *Nature* 389:251 — the 2.8 Å "
            "structure that showed the world how ~147 bp of DNA wraps "
            "1.65 times around a histone octamer (H2A / H2B / H3 / "
            "H4, two of each). Anchor for every chromatin teaching "
            "point: positive-charge histone-tail interactions with "
            "the DNA phosphate backbone, the ~10 bp/turn rotation "
            "that sets nucleosome positioning, and the subsequent "
            "epigenetic modification stories (acetylation / "
            "methylation on H3 / H4 N-terminal tails). Pairs with "
            "1BNA / 143D / 1EHZ nucleic-acid entries for the "
            "protein-DNA interaction arc."
        ),
    ),
    SeededProtein(
        pdb_id="1IGT",
        name="Intact murine IgG2a antibody",
        ligand_name="NAG (N-linked glycans at Asn297)",
        teaching_story=(
            "Harris / Edmundson 1997 *Biochemistry* 36:1581 — the "
            "first complete IgG structure at 2.8 Å.  Y-shaped "
            "tetramer: two heavy chains + two light chains held "
            "together by disulfides and by the conserved Fc-region "
            "interactions.  Teaches (a) Ig-domain fold (β-sandwich "
            "with disulfide-stabilised fold) × 12 repeats per antibody; "
            "(b) CDR loops at the Fab tips as the antigen-binding "
            "surface; (c) the Fc glycan at Asn297 that gates "
            "Fc-receptor engagement — the whole biological-drug "
            "glycosylation-engineering story starts here.  Canonical "
            "structure for every 'how do antibodies work' lesson."
        ),
    ),

    # ---- Phase 31l round 116 — close the phase at 15/15 ------------
    SeededProtein(
        pdb_id="5CHA",
        name="Bovine α-chymotrypsin (native)",
        ligand_name="",
        teaching_story=(
            "Structural anchor for the round-62 chymotrypsin "
            "catalytic-triad mechanism JSON and the round-105 "
            "enzyme-reaction energy profile.  Three-chain α-chymo "
            "generated by post-translational cleavage of chymotrypsinogen "
            "— A (1-13), B (16-146), C (149-245) — held together by "
            "the same two inter-chain disulfides that define the "
            "mature serine-protease fold. Ser195-His57-Asp102 triad "
            "sits at the cleft with the oxyanion hole (backbone NH of "
            "Gly193 + Ser195) ready to stabilise the tetrahedral "
            "intermediates of acylation and deacylation. Completes the "
            "'structure + mechanism + energy profile' teaching triad "
            "for the most-taught serine protease in undergraduate "
            "biochemistry."
        ),
    ),
    SeededProtein(
        pdb_id="6LU7",
        name="SARS-CoV-2 main protease (Mpro) with N3 inhibitor",
        ligand_name="02J (N3 covalent peptidomimetic inhibitor)",
        teaching_story=(
            "Jin / Yang / Rao 2020 *Nature* 582:289 — the first "
            "Mpro structure solved during the COVID-19 pandemic; "
            "ignited the fragment-based + structure-guided Mpro "
            "drug-design wave that ultimately produced nirmatrelvir "
            "(Paxlovid). Cysteine protease (Cys145-His41 dyad, not "
            "the classic triad); the N3 inhibitor makes a covalent "
            "bond to Cys145 via its vinyl-ester Michael acceptor. "
            "Pairs pedagogically with the round-57 HIV protease "
            "(1HPV) entry — HIV Mpro is an aspartic protease with "
            "non-covalent peptidomimetic inhibitors; SARS-CoV-2 Mpro "
            "is a cysteine protease with covalent warhead drugs. "
            "Same functional class, two completely different "
            "catalytic chemistries — that comparison is the "
            "teaching payload of this entry."
        ),
    ),
]


def list_seeded_proteins() -> List[Dict[str, str]]:
    return [
        {"pdb_id": s.pdb_id, "name": s.name,
         "ligand": s.ligand_name, "story": s.teaching_story}
        for s in SEEDED_PROTEINS
    ]


def get_seeded_protein(pdb_id: str) -> Optional[SeededProtein]:
    pid = pdb_id.upper()
    for s in SEEDED_PROTEINS:
        if s.pdb_id.upper() == pid:
            return s
    return None
