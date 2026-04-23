"""Agent actions for Phase 12a — IUPAC nomenclature rule catalogue."""
from __future__ import annotations
import logging
from typing import Any, Dict, List

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


@action(category="naming")
def list_naming_rules(category: str = "") -> List[Dict[str, str]]:
    """Enumerate IUPAC naming rules, optionally filtered by category."""
    from orgchem.naming import list_rules
    return list_rules(category=category)


@action(category="naming")
def get_naming_rule(rule_id: str) -> Dict[str, str]:
    """Return full detail (description, examples, pitfalls) for one naming rule."""
    from orgchem.naming import get_rule
    return get_rule(rule_id)


@action(category="naming")
def naming_rule_categories() -> List[str]:
    """Distinct categories present in the catalogue (alkanes, aromatics, …)."""
    from orgchem.naming import rule_categories
    return rule_categories()
