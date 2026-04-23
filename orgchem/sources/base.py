"""Abstract base class for online molecule / reaction data sources."""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List

from orgchem.core.molecule import Molecule


class DataSource(ABC):
    """Implement two methods and drop the class into ``search_panel._SOURCES``."""

    name: str = "abstract"

    @abstractmethod
    def search(self, query: str, limit: int = 10) -> List[dict]:
        """Return lightweight search results as list of dicts.

        Each dict must include at least ``id`` (source-specific identifier)
        and ``name``. Optional: ``formula``, ``description``.
        """

    @abstractmethod
    def fetch(self, identifier: str) -> Molecule:
        """Retrieve a full :class:`Molecule` by source-specific identifier."""
