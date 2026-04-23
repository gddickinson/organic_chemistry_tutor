"""Nucleic-acid data module — Phase 29 (nucleic-acids sibling).

Catalogue covers:

- **Nucleobases** — A / G / C / T / U plus a couple of modified
  bases (m⁶A, 5-methyl-C).
- **Nucleosides** — the ribose / deoxyribose-linked forms.
- **Nucleotides** — 5'-mono / di / triphosphates (ATP, cAMP).
- **Short oligonucleotides** — a dinucleotide teaching example and
  a hairpin motif SMILES is too awkward, so motifs are carried by
  name + PDB reference rather than SMILES.
- **PDB motifs** — entries that are best fetched through the
  Phase 24a PDB pipeline (B-form DNA dodecamer, tRNA, G-quadruplex).
  These reference a PDB id instead of a SMILES.

Pure data module, headless. The accompanying GUI tab mirrors the
carbohydrates panel pattern and falls back to the PDB / AlphaFold
viewers for the large-motif rows.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class NucleicAcidEntry:
    """One seeded nucleic-acid catalogue entry."""
    name: str
    family: str             # "nucleobase" / "nucleoside" / "nucleotide"
                            # / "oligonucleotide" / "pdb-motif"
    smiles: str = ""        # empty when the motif is PDB-only
    pdb_id: str = ""        # e.g. "4DNB" for B-form DNA dodecamer
    strand: str = ""        # "DNA" / "RNA" / "" for small molecules
    role: str = ""          # short teaching tag
    notes: str = ""

    def to_dict(self) -> Dict[str, object]:
        return {
            "name": self.name, "family": self.family,
            "smiles": self.smiles, "pdb_id": self.pdb_id,
            "strand": self.strand, "role": self.role,
            "notes": self.notes,
        }


# ---------------------------------------------------------------------

NUCLEIC_ACIDS: List[NucleicAcidEntry] = [
    # ---- Nucleobases ---------------------------------------------
    NucleicAcidEntry(
        name="Adenine", family="nucleobase",
        smiles="Nc1ncnc2[nH]cnc12", role="purine",
        notes="Canonical purine base; pairs with T/U via two H-bonds.",
    ),
    NucleicAcidEntry(
        name="Guanine", family="nucleobase",
        smiles="Nc1nc2[nH]cnc2c(=O)[nH]1", role="purine",
        notes="Purine base; G/C pair forms three H-bonds.",
    ),
    NucleicAcidEntry(
        name="Cytosine", family="nucleobase",
        smiles="Nc1cc[nH]c(=O)n1", role="pyrimidine",
        notes="Pyrimidine base; cytosine → uracil via hydrolytic "
              "deamination (mutagenic).",
    ),
    NucleicAcidEntry(
        name="Thymine", family="nucleobase",
        smiles="Cc1c[nH]c(=O)[nH]c1=O", role="pyrimidine",
        notes="DNA-specific pyrimidine; 5-methyl protects against "
              "cytosine deamination mix-ups.",
    ),
    NucleicAcidEntry(
        name="Uracil", family="nucleobase",
        smiles="O=c1cc[nH]c(=O)[nH]1", role="pyrimidine",
        notes="RNA pyrimidine. Structurally identical to thymine "
              "minus the 5-methyl.",
    ),
    NucleicAcidEntry(
        name="N6-Methyladenine (m6A)", family="nucleobase",
        smiles="CNc1ncnc2[nH]cnc12", role="modified-base",
        notes="RNA methylation mark; writers/erasers/readers are "
              "a major epitranscriptomic signalling system.",
    ),
    NucleicAcidEntry(
        name="5-Methylcytosine (m5C)", family="nucleobase",
        smiles="Cc1c[nH]c(=O)nc1N", role="modified-base",
        notes="DNA epigenetic mark; silencing signal at CpG sites.",
    ),
    # ---- Nucleosides ---------------------------------------------
    NucleicAcidEntry(
        name="Adenosine", family="nucleoside",
        smiles="Nc1ncnc2c1ncn2[C@@H]1O[C@H](CO)[C@@H](O)[C@H]1O",
        strand="RNA", role="ribonucleoside",
        notes="A + ribose. Also a neuromodulator (receptors antagonised "
              "by caffeine).",
    ),
    NucleicAcidEntry(
        name="Guanosine", family="nucleoside",
        smiles="Nc1nc2c(ncn2[C@@H]2O[C@H](CO)[C@@H](O)[C@H]2O)"
               "c(=O)[nH]1",
        strand="RNA", role="ribonucleoside",
    ),
    NucleicAcidEntry(
        name="Cytidine", family="nucleoside",
        smiles="Nc1ccn([C@@H]2O[C@H](CO)[C@@H](O)[C@H]2O)c(=O)n1",
        strand="RNA", role="ribonucleoside",
    ),
    NucleicAcidEntry(
        name="Uridine", family="nucleoside",
        smiles="O=c1[nH]c(=O)n([C@@H]2O[C@H](CO)[C@@H](O)[C@H]2O)cc1",
        strand="RNA", role="ribonucleoside",
    ),
    NucleicAcidEntry(
        name="Thymidine", family="nucleoside",
        smiles="Cc1cn([C@H]2C[C@H](O)[C@@H](CO)O2)c(=O)[nH]c1=O",
        strand="DNA", role="deoxyribonucleoside",
    ),
    NucleicAcidEntry(
        name="2'-Deoxyadenosine", family="nucleoside",
        smiles="Nc1ncnc2c1ncn2[C@H]1C[C@H](O)[C@@H](CO)O1",
        strand="DNA", role="deoxyribonucleoside",
    ),
    # ---- Nucleotides ---------------------------------------------
    NucleicAcidEntry(
        name="ATP (adenosine-5'-triphosphate)", family="nucleotide",
        smiles="Nc1ncnc2c1ncn2[C@@H]1O[C@H](COP(=O)(O)OP(=O)(O)"
               "OP(=O)(O)O)[C@@H](O)[C@H]1O",
        strand="RNA", role="high-energy-phosphate",
        notes="Universal energy currency. γ-phosphate hydrolysis ≈ "
              "−30 kJ/mol at cellular conditions.",
    ),
    NucleicAcidEntry(
        name="cAMP (3',5'-cyclic AMP)", family="nucleotide",
        smiles="Nc1ncnc2c1ncn2[C@H]1O[C@@H]2COP(=O)(O)O[C@@H]2"
               "[C@@H]1O",
        strand="RNA", role="second-messenger",
        notes="Second messenger downstream of GPCR-activated "
              "adenylate cyclase. Activates PKA.",
    ),
    NucleicAcidEntry(
        name="GTP (guanosine-5'-triphosphate)", family="nucleotide",
        smiles="Nc1nc2c(ncn2[C@@H]2O[C@H](COP(=O)(O)OP(=O)(O)"
               "OP(=O)(O)O)[C@@H](O)[C@H]2O)c(=O)[nH]1",
        strand="RNA", role="high-energy-phosphate",
        notes="Energy + signalling (GTPases, translation).",
    ),
    NucleicAcidEntry(
        name="NAD+ (nicotinamide adenine dinucleotide)",
        family="nucleotide",
        smiles="NC(=O)c1ccc[n+]([C@@H]2O[C@H](COP(=O)([O-])"
               "OP(=O)(O)OC[C@H]3O[C@@H](n4cnc5c(N)ncnc54)"
               "[C@H](O)[C@@H]3O)[C@@H](O)[C@H]2O)c1",
        strand="", role="coenzyme",
        notes="Dinucleotide coenzyme. Two-electron / one-proton carrier "
              "in central metabolism.",
    ),
    # ---- Short oligos --------------------------------------------
    NucleicAcidEntry(
        name="Dinucleotide 5'-ApG-3'",
        family="oligonucleotide",
        smiles="Nc1ncnc2c1ncn2[C@@H]1O[C@H](COP(=O)(O)O[C@H]2"
               "[C@@H](OC3=Nc4nc[nH]c4C(=O)N3)O[C@@H](CO)"
               "[C@H]2O)[C@@H](O)[C@H]1O",
        strand="RNA", role="dinucleotide",
        notes="Two ribonucleosides joined by a 3'→5' phosphodiester — "
              "the smallest meaningful RNA.",
    ),
    # ---- PDB motifs ----------------------------------------------
    NucleicAcidEntry(
        name="B-form DNA dodecamer", family="pdb-motif",
        pdb_id="1BNA", strand="DNA", role="canonical-duplex",
        notes="Dickerson-Drew dodecamer CGCGAATTCGCG — textbook "
              "B-form. Fetch via Proteins tab; 3D viewer renders "
              "the double helix.",
    ),
    NucleicAcidEntry(
        name="A-form RNA duplex", family="pdb-motif",
        pdb_id="1RNA", strand="RNA", role="duplex",
        notes="Wider / shorter A-form geometry typical of "
              "RNA:RNA and RNA:DNA duplexes.",
    ),
    NucleicAcidEntry(
        name="G-quadruplex (human telomere)", family="pdb-motif",
        pdb_id="143D", strand="DNA", role="non-canonical",
        notes="Four-stranded G-quartet structure at telomeres; "
              "target of anticancer G4 stabilisers.",
    ),
    NucleicAcidEntry(
        name="tRNA-Phe (yeast)", family="pdb-motif",
        pdb_id="1EHZ", strand="RNA", role="tRNA",
        notes="Cloverleaf secondary + L-shaped 3D. Anticodon arm at "
              "one end, CCA acceptor at the other.",
    ),
    NucleicAcidEntry(
        name="Hammerhead ribozyme", family="pdb-motif",
        pdb_id="1HMH", strand="RNA", role="ribozyme",
        notes="Self-cleaving RNA motif. Catalyses in-line phosphoryl "
              "transfer — canonical SN2-at-P mechanism.",
    ),

    # ---- Phase 31j content expansion (2026-04-23) -----------------
    # Non-canonical / wobble / modified bases
    NucleicAcidEntry(
        name="Hypoxanthine", family="nucleobase",
        smiles="O=c1[nH]cnc2[nH]cnc12", role="purine",
        notes="Purine with a keto group at C6. Base of inosine; "
              "arises from hydrolytic deamination of adenine.",
    ),
    NucleicAcidEntry(
        name="Xanthine", family="nucleobase",
        smiles="O=c1[nH]c(=O)c2[nH]cnc2[nH]1", role="purine",
        notes="2,6-dioxopurine. Intermediate in purine catabolism "
              "(xanthine oxidase → uric acid). Target of allopurinol.",
    ),
    NucleicAcidEntry(
        name="Inosine", family="nucleoside",
        smiles="O=c1[nH]cnc2c1ncn2[C@@H]1O[C@H](CO)[C@@H](O)[C@H]1O",
        strand="RNA", role="modified-nucleoside",
        notes="Hypoxanthine + ribose. Wobble-position base in tRNA "
              "(pairs with U, C, A). Basis of inosine-containing "
              "mRNA editing (ADAR enzymes).",
    ),
    NucleicAcidEntry(
        name="Pseudouridine (Ψ)", family="nucleoside",
        smiles="OC[C@H]1O[C@H]([C@@H](O)[C@@H]1O)"
               "c1cc(=O)[nH]c(=O)[nH]1",
        strand="RNA", role="modified-nucleoside",
        notes="C5-linked uracil — the most abundant RNA modification. "
              "Stabilises tRNA / rRNA helices; pseudouridylation is "
              "programmable via H/ACA snoRNAs.",
    ),
    # Coenzyme nucleotides
    NucleicAcidEntry(
        name="NADH", family="nucleotide",
        smiles="NC(=O)C1=CN(C=CC1)[C@@H]1O[C@H](COP(=O)(O)OP(=O)(O)"
               "OC[C@H]2O[C@@H](n3cnc4c(N)ncnc43)[C@H](O)[C@@H]2O)"
               "[C@@H](O)[C@H]1O",
        strand="RNA", role="redox-coenzyme",
        notes="Reduced form of NAD⁺. Hydride carrier in cellular "
              "metabolism; λmax 340 nm lets biochemists follow "
              "oxidoreductase kinetics.",
    ),
    NucleicAcidEntry(
        name="NADPH", family="nucleotide",
        smiles="NC(=O)C1=CN(C=CC1)[C@@H]1O[C@H](COP(=O)(O)OP(=O)(O)"
               "OC[C@H]2O[C@@H](n3cnc4c(N)ncnc43)[C@H](OP(=O)(O)O)"
               "[C@@H]2O)[C@@H](O)[C@H]1O",
        strand="RNA", role="redox-coenzyme",
        notes="2'-phosphorylated NADH. Reducing equivalents for "
              "biosynthesis (fatty-acid synthase, cholesterol "
              "biosynthesis, P450 reductases).",
    ),
    NucleicAcidEntry(
        name="FAD", family="nucleotide",
        smiles="Cc1cc2nc3c(=O)[nH]c(=O)n(C[C@H](O)[C@@H](O)[C@@H](O)"
               "COP(=O)(O)OP(=O)(O)OC[C@H]4O[C@@H](n5cnc6c(N)ncnc65)"
               "[C@H](O)[C@@H]4O)c3nc2cc1C",
        strand="RNA", role="redox-coenzyme",
        notes="Flavin adenine dinucleotide. Two-electron / one-"
              "electron capable; isoalloxazine ring handles radical "
              "chemistry (e.g. dehydrogenases, monoamine oxidase).",
    ),
    NucleicAcidEntry(
        name="Coenzyme A (CoA-SH)", family="nucleotide",
        smiles="CC(C)(COP(=O)(O)OP(=O)(O)OC[C@H]1O[C@@H]"
               "(n2cnc3c(N)ncnc32)[C@H](OP(=O)(O)O)[C@@H]1O)"
               "[C@@H](O)C(=O)NCCC(=O)NCCS",
        strand="RNA", role="acyl-carrier",
        notes="Carries acyl groups (via thioester at the terminal "
              "–SH). Central to fatty-acid metabolism, TCA cycle, "
              "and acetylation of histones / proteins.",
    ),
    NucleicAcidEntry(
        name="S-Adenosyl-L-methionine (SAM)", family="nucleotide",
        smiles="C[S+](CC[C@H](N)C(=O)O)C[C@H]1O[C@@H]"
               "(n2cnc3c(N)ncnc32)[C@H](O)[C@@H]1O",
        strand="RNA", role="methyl-donor",
        notes="Universal biological methyl donor. Sulfonium salt "
              "makes the methyl group electrophilic. Drives DNA / "
              "RNA / protein / small-molecule methylation.",
    ),
    # Secondary-structure / motif teaching entries
    NucleicAcidEntry(
        name="RNA hairpin (GCGCUUUUGCGC)", family="oligonucleotide",
        strand="RNA", role="secondary-structure",
        notes="Canonical tetraloop hairpin: 4-bp stem + UUUU loop. "
              "Common motif in ribosomal RNA and mRNA 3'-UTRs. "
              "Rendered as sequence — no single-ligand SMILES.",
    ),
]


# ---------------------------------------------------------------------
# Lookup helpers

def list_nucleic_acids(family: str = "") -> List[Dict[str, object]]:
    """Summary-dict list, optionally filtered by family."""
    fam = family.strip().lower()
    return [n.to_dict() for n in NUCLEIC_ACIDS
            if not fam or n.family == fam]


def get_nucleic_acid(name: str) -> Optional[NucleicAcidEntry]:
    """Exact-or-case-insensitive name lookup."""
    name = name.strip()
    for n in NUCLEIC_ACIDS:
        if n.name.lower() == name.lower():
            return n
    return None


def nucleic_acid_families() -> List[str]:
    seen: List[str] = []
    for n in NUCLEIC_ACIDS:
        if n.family not in seen:
            seen.append(n.family)
    return seen
