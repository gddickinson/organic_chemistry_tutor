"""Phase GM-1.0 (round 230) — molecular-biology-techniques
catalogue.

The flagship Genetics + Molecular Biology Studio catalogue.
~ 36 techniques spanning every major class: PCR, sequencing
(Sanger + NGS), cloning, CRISPR, blots, in-situ
hybridisation, chromatin profiling, transcriptomics (bulk +
single-cell + spatial), proteomics, interactions,
structural / 3D-genome, epigenetics, genome-editing
delivery.

Each entry is a long-form bench card with: principle,
sample types, throughput, key reagents (with cross-link to
BC-1.0 enzymes), typical readouts, limitations,
representative platforms / kits, year of introduction, key
references.

Pure-headless: no Qt, no DB.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Tuple


# ----------------------------------------------------------------
# Categories
# ----------------------------------------------------------------
CATEGORIES: Tuple[str, ...] = (
    "pcr",                  # PCR family
    "sequencing",           # Sanger + NGS platforms
    "cloning",              # restriction / Gibson / Golden Gate / TOPO / Gateway
    "crispr",               # Cas9 / 12 / 13 / base editors / prime editors / diagnostics
    "blot",                 # Northern / Southern / Western / dot
    "in-situ",              # FISH / smFISH / MERFISH / HCR
    "chromatin",            # ChIP / CUT&RUN / ATAC / DNase / MNase
    "transcriptomics",      # RNA-seq / scRNA-seq / snRNA-seq / ribo-seq
    "spatial",              # Visium / Stereo-seq / MERSCOPE / Slide-seq
    "proteomics",           # MS-based + AP-MS + BioID + APEX
    "interaction",          # Y2H / NanoBiT / BiFC / FRET
    "structural",           # Hi-C / Micro-C / capture Hi-C
    "epigenetics",          # bisulfite-seq / EM-seq / methyl-CpG IP
    "delivery",             # RNP / lentiviral / AAV / lipid-nanoparticle
)


@dataclass(frozen=True)
class MolecularBiologyTechnique:
    """One molecular-biology technique entry in the GM-1.0
    catalogue."""
    id: str                                # canonical short id
    name: str                              # display name
    abbreviation: str                      # short form (e.g. "qPCR", "smFISH")
    category: str                          # one of CATEGORIES
    principle: str                         # paragraph
    sample_types: str                      # what goes in
    throughput: str                        # rough scale + day-rate
    typical_readout: str                   # what comes out
    key_reagents: str                      # main consumables / kits / buffers
    representative_platforms: str          # vendors / kits / instruments
    year_introduced: str                   # canonical first paper or commercial release
    key_references: str                    # short-form refs
    strengths: str
    limitations: str
    notes: str
    # Cross-references (the multi-studio link layer)
    cross_reference_enzyme_ids: Tuple[str, ...]
    # ↑ ids in biochem.core.enzymes
    cross_reference_cell_cycle_ids: Tuple[str, ...]
    # ↑ ids in cellbio.core.cell_cycle
    cross_reference_signaling_pathway_ids: Tuple[str, ...]
    # ↑ ids in cellbio.core.cell_signaling
    cross_reference_animal_taxon_ids: Tuple[str, ...]
    # ↑ ids in animal.core.taxa (model organisms used)
    cross_reference_molecule_names: Tuple[str, ...]
    # ↑ exact-name matches for orgchem.db.Molecule rows

    def __post_init__(self) -> None:
        """Validator pattern carried over from BC-2.0 — refuses
        plain ``str`` where a ``Tuple[str, ...]`` field is
        expected.  Permanently closes the trailing-comma single-
        element-tuple bug class introduced when forgetting the
        comma in ``("foo")`` vs ``("foo",)``.
        """
        for field in (
            "cross_reference_enzyme_ids",
            "cross_reference_cell_cycle_ids",
            "cross_reference_signaling_pathway_ids",
            "cross_reference_animal_taxon_ids",
            "cross_reference_molecule_names",
        ):
            value = getattr(self, field)
            if isinstance(value, str):
                raise TypeError(
                    f"{self.__class__.__name__}.{field} must "
                    f"be a tuple of strings, got plain str "
                    f"{value!r}; missing trailing comma?")
            if not isinstance(value, tuple):
                raise TypeError(
                    f"{self.__class__.__name__}.{field} must "
                    f"be a tuple of strings, got "
                    f"{type(value).__name__}.")
        if self.category not in CATEGORIES:
            raise ValueError(
                f"{self.id}: category {self.category!r} not "
                f"in {CATEGORIES}")


# ----------------------------------------------------------------
# Lookup helpers
# ----------------------------------------------------------------

def _entry_list() -> List[MolecularBiologyTechnique]:
    """Lazy import of the data file so each file stays under
    the 500-line cap."""
    from genetics.core.techniques_data import TECHNIQUES
    return TECHNIQUES


def list_techniques(
    category: Optional[str] = None,
) -> List[MolecularBiologyTechnique]:
    """Return techniques, optionally filtered by category."""
    out = list(_entry_list())
    if category:
        out = [t for t in out if t.category == category]
    return out


def get_technique(
    technique_id: str,
) -> Optional[MolecularBiologyTechnique]:
    """Return one technique entry by id, or ``None``."""
    for t in _entry_list():
        if t.id == technique_id:
            return t
    return None


def find_techniques(
    needle: str,
) -> List[MolecularBiologyTechnique]:
    """Case-insensitive substring search across id + name +
    abbreviation + category + principle + sample types +
    typical readout + key reagents + representative platforms +
    notes."""
    n = (needle or "").strip().lower()
    if not n:
        return []
    out: List[MolecularBiologyTechnique] = []
    for t in _entry_list():
        parts = [t.id, t.name, t.abbreviation, t.category,
                 t.principle, t.sample_types,
                 t.typical_readout, t.key_reagents,
                 t.representative_platforms, t.notes]
        if n in " ".join(parts).lower():
            out.append(t)
    return out


def techniques_for_application(
    application: str,
) -> List[MolecularBiologyTechnique]:
    """All techniques whose typical-readout, principle, or
    notes matches the given application keyword (e.g.
    ``"diagnostic"`` / ``"single-cell"`` / ``"variant
    calling"`` / ``"chromatin"``)."""
    return find_techniques(application)


def technique_to_dict(
    t: MolecularBiologyTechnique,
) -> Dict[str, object]:
    """JSON-friendly serialiser for agent actions."""
    return asdict(t)


def categories() -> Tuple[str, ...]:
    return CATEGORIES
