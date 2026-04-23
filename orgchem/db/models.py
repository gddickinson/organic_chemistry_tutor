"""SQLAlchemy ORM models: Molecule, Reaction, Tutorial, Tag."""
from __future__ import annotations
from datetime import datetime
from typing import List, Optional

from sqlalchemy import String, Integer, Float, Text, DateTime, ForeignKey, Column, Table, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


molecule_tags = Table(
    "molecule_tags", Base.metadata,
    Column("molecule_id", ForeignKey("molecules.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)

reaction_tags = Table(
    "reaction_tags", Base.metadata,
    Column("reaction_id", ForeignKey("reactions.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)


class Tag(Base):
    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True)


class Molecule(Base):
    __tablename__ = "molecules"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    smiles: Mapped[str] = mapped_column(String(1024))
    inchi: Mapped[Optional[str]] = mapped_column(Text)
    inchikey: Mapped[Optional[str]] = mapped_column(String(30), index=True)
    formula: Mapped[Optional[str]] = mapped_column(String(80))
    molblock_2d: Mapped[Optional[str]] = mapped_column(Text)
    molblock_3d: Mapped[Optional[str]] = mapped_column(Text)
    properties_json: Mapped[Optional[str]] = mapped_column(Text)
    source: Mapped[Optional[str]] = mapped_column(String(80))
    # Phase 28a — multi-category filter columns. All optional /
    # NULL-defaulted; legacy rows keep working.
    source_tags_json: Mapped[Optional[str]] = mapped_column(Text)
    functional_group_tags_json: Mapped[Optional[str]] = mapped_column(Text)
    heavy_atom_count: Mapped[Optional[int]] = mapped_column(Integer)
    formal_charge: Mapped[Optional[int]] = mapped_column(Integer)
    n_rings: Mapped[Optional[int]] = mapped_column(Integer)
    has_stereo: Mapped[Optional[bool]] = mapped_column(Boolean)
    # Round 58 — JSON list of common synonyms (``["Retinol",
    # "Vitamin A"]``). Lets name-based search resolve either the
    # IUPAC name or any trivial alias to the same row.
    synonyms_json: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    tags: Mapped[List["Tag"]] = relationship(secondary=molecule_tags)


class Reaction(Base):
    __tablename__ = "reactions"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    reaction_smarts: Mapped[str] = mapped_column(Text)
    #: Atom-mapped reaction SMARTS for the 3D renderer and future
    #: animation layer (Phase 2c.1+). Optional — not every reaction has
    #: one recorded yet, and user-imported reactions typically won't.
    reaction_smarts_mapped: Mapped[Optional[str]] = mapped_column(Text)
    description: Mapped[Optional[str]] = mapped_column(Text)
    category: Mapped[Optional[str]] = mapped_column(String(80))
    mechanism_json: Mapped[Optional[str]] = mapped_column(Text)
    #: Reaction-coordinate energy profile as JSON — Phase 13b. Stationary
    #: points (reactant / TS / intermediate / product) with relative energies
    #: in the unit given by the profile. Optional.
    energy_profile_json: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    tags: Mapped[List["Tag"]] = relationship(secondary=reaction_tags)


class Tutorial(Base):
    __tablename__ = "tutorials"
    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True)
    title: Mapped[str] = mapped_column(String(200))
    level: Mapped[str] = mapped_column(String(40))  # beginner / intermediate / advanced / graduate
    order_index: Mapped[int] = mapped_column(Integer, default=0)
    content_path: Mapped[str] = mapped_column(String(400))
    completed: Mapped[bool] = mapped_column(Boolean, default=False)


class SynthesisPathway(Base):
    """A named multi-step route from commercially available starting
    materials to a target molecule. Phase 8."""

    __tablename__ = "synthesis_pathways"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    target_name: Mapped[str] = mapped_column(String(200))
    target_smiles: Mapped[Optional[str]] = mapped_column(String(1024))
    description: Mapped[Optional[str]] = mapped_column(Text)
    category: Mapped[Optional[str]] = mapped_column(String(80))
    source: Mapped[Optional[str]] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    steps: Mapped[List["SynthesisStep"]] = relationship(
        back_populates="pathway",
        cascade="all, delete-orphan",
        order_by="SynthesisStep.step_index",
    )


class GlossaryTerm(Base):
    """A single glossary / dictionary entry — Phase 11a.

    ``aliases_json``, ``see_also_json``, and ``example_ids_json`` store
    lists as JSON strings so we don't need per-term join tables.
    """

    __tablename__ = "glossary_terms"
    id: Mapped[int] = mapped_column(primary_key=True)
    term: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    aliases_json: Mapped[Optional[str]] = mapped_column(Text)
    definition_md: Mapped[str] = mapped_column(Text)
    category: Mapped[Optional[str]] = mapped_column(String(80), index=True)
    see_also_json: Mapped[Optional[str]] = mapped_column(Text)
    example_ids_json: Mapped[Optional[str]] = mapped_column(Text)
    # Phase 26a: optional SMILES for auto-generating an illustrative
    # figure, and an optional cached PNG/SVG path (relative to
    # data/glossary/). Both default to NULL — legacy terms stay
    # figure-less.
    example_smiles: Mapped[Optional[str]] = mapped_column(String(500))
    example_figure_path: Mapped[Optional[str]] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class SynthesisStep(Base):
    """A single reaction in a synthesis pathway."""

    __tablename__ = "synthesis_steps"
    id: Mapped[int] = mapped_column(primary_key=True)
    pathway_id: Mapped[int] = mapped_column(ForeignKey("synthesis_pathways.id"))
    step_index: Mapped[int] = mapped_column(Integer, default=0)
    reaction_smiles: Mapped[str] = mapped_column(Text)   # full 'R.R>>P.P' string
    reagents: Mapped[Optional[str]] = mapped_column(String(400))   # above the arrow
    conditions: Mapped[Optional[str]] = mapped_column(String(400)) # below the arrow
    yield_pct: Mapped[Optional[float]] = mapped_column(Float)
    notes: Mapped[Optional[str]] = mapped_column(Text)

    pathway: Mapped[SynthesisPathway] = relationship(back_populates="steps")
