"""Phase AB-1.0 (round 217) — animal-taxa catalogue.

The flagship Animal Biology Studio catalogue.  ~ 30 animal
taxa spanning all 9 major phyla (porifera / cnidaria /
platyhelminthes / nematoda / mollusca / annelida / arthropoda
/ echinodermata / chordata), each with cellular-signalling
+ enzyme + animal-derived-metabolite cross-references.

Pure-headless: no Qt, no DB.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Tuple


# ----------------------------------------------------------------
# Taxonomy + traits
# ----------------------------------------------------------------
PHYLA: Tuple[str, ...] = (
    "porifera",          # sponges
    "cnidaria",          # jellyfish, hydra, anemones, corals
    "platyhelminthes",   # flatworms
    "nematoda",          # roundworms
    "mollusca",          # snails, octopus, squid
    "annelida",          # segmented worms
    "arthropoda",        # insects, crustaceans, arachnids
    "echinodermata",     # starfish, sea urchins
    "chordata",          # tunicates → vertebrates
)

BODY_PLANS: Tuple[str, ...] = (
    "asymmetric",        # sponges
    "radial",            # cnidarians, adult echinoderms
    "bilateral",         # everything else (most animals)
)

GERM_LAYERS: Tuple[str, ...] = (
    "diploblast",        # cnidarians
    "triploblast",       # bilaterians
    "not-applicable",    # sponges (no true germ layers)
)

COELOM_TYPES: Tuple[str, ...] = (
    "acoelomate",        # platyhelminthes
    "pseudocoelomate",   # nematoda
    "coelomate",         # most bilaterians
    "not-applicable",    # sponges, cnidarians
)


@dataclass(frozen=True)
class AnimalTaxon:
    """One animal entry in the AB-1.0 catalogue."""
    id: str
    name: str                              # common name
    full_taxonomic_name: str               # binomial / clade
    phylum: str                            # one of PHYLA
    animal_class: str                      # mammalia / insecta / asteroidea / etc.
    body_plan: str                         # one of BODY_PLANS
    germ_layers: str                       # one of GERM_LAYERS
    coelom_type: str                       # one of COELOM_TYPES
    reproductive_strategy: str
    ecological_role: str
    model_organism: bool
    genome_size_or_mb: str
    # Cross-references (the multi-studio link layer)
    cross_reference_molecule_names: Tuple[str, ...]
    # ↑ exact-name matches for orgchem.db.Molecule rows
    cross_reference_signaling_pathway_ids: Tuple[str, ...]
    # ↑ ids in cellbio.core.cell_signaling
    cross_reference_enzyme_ids: Tuple[str, ...]
    # ↑ ids in biochem.core.enzymes
    notes: str = ""


# ----------------------------------------------------------------
# Lookup helpers
# ----------------------------------------------------------------

def _taxon_list() -> List[AnimalTaxon]:
    """Lazy import of the data file so each file stays under the
    500-line cap."""
    from animal.core.taxa_data import ANIMAL_TAXA
    return ANIMAL_TAXA


def list_animal_taxa(
    phylum: Optional[str] = None,
    body_plan: Optional[str] = None,
) -> List[AnimalTaxon]:
    """Return animal taxa, optionally filtered."""
    out = list(_taxon_list())
    if phylum:
        out = [t for t in out if t.phylum == phylum]
    if body_plan:
        out = [t for t in out if t.body_plan == body_plan]
    return out


def get_animal_taxon(taxon_id: str) -> Optional[AnimalTaxon]:
    """Return one animal taxon by id, or ``None``."""
    for t in _taxon_list():
        if t.id == taxon_id:
            return t
    return None


def find_animal_taxa(needle: str) -> List[AnimalTaxon]:
    """Case-insensitive substring search across id + names +
    class + reproductive strategy + ecological role + notes +
    cross-reference molecule names."""
    n = (needle or "").strip().lower()
    if not n:
        return []
    out: List[AnimalTaxon] = []
    for t in _taxon_list():
        parts = [t.id, t.name, t.full_taxonomic_name,
                 t.animal_class, t.reproductive_strategy,
                 t.ecological_role, t.notes]
        parts.extend(t.cross_reference_molecule_names)
        if n in " ".join(parts).lower():
            out.append(t)
    return out


def animal_taxa_for_phylum(phylum: str) -> List[AnimalTaxon]:
    """All animal taxa in a given phylum."""
    return list_animal_taxa(phylum=phylum)


def animal_taxon_to_dict(t: AnimalTaxon) -> Dict[str, object]:
    """JSON-friendly serialiser for agent actions."""
    return asdict(t)


def phyla() -> Tuple[str, ...]:
    return PHYLA


def body_plans() -> Tuple[str, ...]:
    return BODY_PLANS


def germ_layers() -> Tuple[str, ...]:
    return GERM_LAYERS


def coelom_types() -> Tuple[str, ...]:
    return COELOM_TYPES
