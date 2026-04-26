"""Phase 47c (round 168) — agent actions for the
biochemistry-by-kingdom catalogue + window.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


@action(category="kingdom")
def list_kingdom_topics(
    kingdom: str = "",
    subtab: str = "",
    sub_domain: str = "",
) -> List[Dict[str, object]]:
    """Return biochemistry-by-kingdom topics, optionally
    filtered by kingdom (one of: ``"eukarya"`` / ``"bacteria"``
    / ``"archaea"`` / ``"viruses"``), sub-tab (one of:
    ``"structure"`` / ``"physiology"`` / ``"genetics"``), and
    / or sub-domain (one of ``"animal"`` / ``"plant"`` /
    ``"fungus"`` / ``"protist"`` for Eukarya;
    ``"gram-positive"`` / ``"gram-negative"`` for Bacteria;
    ``"euryarchaeota"`` / ``"crenarchaeota"`` / ``"asgard"``
    for Archaea; ``"dna-virus"`` / ``"rna-virus"`` /
    ``"retrovirus"`` for Viruses).  Round 169 / Phase 47d:
    pan-domain topics with empty sub_domain match ANY
    sub-domain query within their kingdom."""
    from orgchem.core.biochemistry_by_kingdom import (
        KINGDOMS, SUB_DOMAINS, SUBTABS,
        list_topics, topic_to_dict,
    )
    k = (kingdom or "").strip()
    s = (subtab or "").strip()
    sd = (sub_domain or "").strip()
    if k and k not in KINGDOMS:
        return [{
            "error": f"Unknown kingdom {k!r}; valid: "
                     f"{', '.join(KINGDOMS)}.",
        }]
    if s and s not in SUBTABS:
        return [{
            "error": f"Unknown sub-tab {s!r}; valid: "
                     f"{', '.join(SUBTABS)}.",
        }]
    if sd and sd not in SUB_DOMAINS:
        return [{
            "error": f"Unknown sub-domain {sd!r}; valid: "
                     f"{', '.join(SUB_DOMAINS)}.",
        }]
    return [topic_to_dict(t)
            for t in list_topics(k or None, s or None,
                                 sd or None)]


@action(category="kingdom")
def get_kingdom_topic(
    topic_id: str,
) -> Dict[str, object]:
    """Return the full record for a single biochemistry-by-
    kingdom topic by id (e.g.
    ``"eukarya-genetics-endosymbiotic-origin"`` /
    ``"bacteria-genetics-crispr-defence"`` /
    ``"archaea-structure-ether-lipids"`` /
    ``"viruses-genetics-not-a-domain"``)."""
    from orgchem.core.biochemistry_by_kingdom import (
        get_topic, topic_to_dict,
    )
    t = get_topic(topic_id)
    if t is None:
        return {"error": f"Unknown kingdom-topic id: "
                         f"{topic_id!r}."}
    return topic_to_dict(t)


@action(category="kingdom")
def find_kingdom_topics(
    needle: str,
) -> List[Dict[str, object]]:
    """Case-insensitive substring search across id + title +
    body + cross-reference fields."""
    from orgchem.core.biochemistry_by_kingdom import (
        find_topics, topic_to_dict,
    )
    return [topic_to_dict(t) for t in find_topics(needle)]


@action(category="kingdom")
def open_biochemistry_by_kingdom(
    kingdom: str = "",
    subtab: str = "",
    topic_id: str = "",
) -> Dict[str, Any]:
    """Open the *Window → Biochemistry by Kingdom…* window
    and optionally focus a specific kingdom (outer tab) +
    sub-tab + topic.  Passing just ``kingdom`` switches the
    outer tab; passing all three drills all the way down to
    the topic."""
    from orgchem.agent import controller
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync
    win = controller.main_window()
    if win is None:
        return {"error": "Main window not available — run the "
                         "app interactively or via HeadlessApp "
                         "first."}

    def _open() -> Dict[str, Any]:
        bk = win.open_biochemistry_by_kingdom_window(
            kingdom=kingdom or None,
            subtab=subtab or None,
            topic_id=topic_id or None,
        )
        # Report what actually got selected so the agent can
        # introspect failure paths (e.g. unknown kingdom / id).
        selected_topic = False
        if kingdom and subtab and topic_id:
            selected_topic = bk.select_topic(
                kingdom, subtab, topic_id)
        elif kingdom:
            selected_topic = bk.switch_to_kingdom(kingdom)
        return {
            "opened": True,
            "kingdom": kingdom or None,
            "subtab": subtab or None,
            "topic_id": topic_id or None,
            "selected": selected_topic,
        }

    return run_on_main_thread_sync(_open)
