"""Application exception hierarchy.

All application code raises one of these when a *domain* error occurs; code
that calls into RDKit / SQLAlchemy / requests wraps lower-level exceptions
into these so the GUI can present sensible messages without leaking internals.
"""


class OrgChemError(Exception):
    """Base class for all OrgChem application errors."""


class ChemistryError(OrgChemError):
    """Chemistry / parsing / structure errors."""


class InvalidSMILESError(ChemistryError):
    """Raised when a SMILES string cannot be parsed."""


class ConformerGenerationError(ChemistryError):
    """Raised when 3D conformer embedding / optimisation fails."""


class DatabaseError(OrgChemError):
    """Database-layer errors (wraps SQLAlchemy errors where meaningful)."""


class NetworkError(OrgChemError):
    """Errors raised by online data sources."""


class RenderError(OrgChemError):
    """Errors raised by 2D / 3D rendering helpers."""
