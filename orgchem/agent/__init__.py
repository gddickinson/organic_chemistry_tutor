"""Agent / LLM integration layer.

This package provides three distinct capabilities:

1. **Action registry** (``actions.py``) — a decorator-based registry of
   high-level operations ("show molecule", "search PubChem", "open lesson",
   "compute formula", …) exposed with typed signatures and docstrings.
   Every capability an LLM needs is available here, *not* by poking at Qt
   widgets directly.

2. **Headless runner** (``headless.py``) — spins up a ``QApplication`` with
   the off-screen platform so the app works in CI and under any LLM that can
   execute Python. A unit test or an external Claude Code session can drive
   the app headlessly by importing ``HeadlessApp`` and calling actions.

3. **LLM backends** (``llm/``) — a pluggable abstraction over Anthropic
   Claude, OpenAI-compatible APIs, and Ollama (local). Plus a JSON-over-stdio
   ``bridge`` so any external process (including a Claude Code session) can
   drive the app without writing Python.
"""
from orgchem.agent.actions import action, registry, invoke, ActionSpec
from orgchem.agent import library             # noqa: F401 — core actions
from orgchem.agent import actions_reactions   # noqa: F401 — reactions + mechanisms
from orgchem.agent import actions_pathways    # noqa: F401 — synthesis pathways
from orgchem.agent import actions_dynamics    # noqa: F401 — conformational dynamics (Phase 10a)
from orgchem.agent import actions_orbitals    # noqa: F401 — Hückel MOs (Phase 14a)
from orgchem.agent import actions_stereo      # noqa: F401 — R/S / E/Z descriptors
from orgchem.agent import actions_glossary    # noqa: F401 — glossary lookup (Phase 11d)
from orgchem.agent import actions_medchem     # noqa: F401 — drug-likeness (Phase 19b)
from orgchem.agent import actions_labtech     # noqa: F401 — TLC / Rf (Phase 15b)
from orgchem.agent import actions_naming      # noqa: F401 — IUPAC rule catalogue (Phase 12a)
from orgchem.agent import actions_spectroscopy # noqa: F401 — IR prediction (Phase 4)
from orgchem.agent import actions_retrosynthesis # noqa: F401 — Phase 8d retro templates
from orgchem.agent import actions_sar           # noqa: F401 — Phase 19a SAR series
from orgchem.agent import actions_protein       # noqa: F401 — Phase 24a PDB ingestion
from orgchem.agent import actions_hrms          # noqa: F401 — Phase 4 HRMS formula guesser
from orgchem.agent import actions_session       # noqa: F401 — Phase 20d session state + Phase 4 EI-MS fragments
from orgchem.agent import actions_periodic      # noqa: F401 — Phase 27a periodic table
from orgchem.agent import actions_carbohydrates # noqa: F401 — Phase 29a carbohydrates
from orgchem.agent import actions_lipids_na      # noqa: F401 — Phase 29 lipids + nucleic acids
from orgchem.agent import actions_windows        # noqa: F401 — Phase 30 secondary windows
from orgchem.agent import actions_meta           # noqa: F401 — round 55 tutor-introspection
from orgchem.agent import actions_phys_org       # noqa: F401 — Phase 17e Hammett / KIE
from orgchem.agent import actions_authoring      # noqa: F401 — round 55 content-authoring
from orgchem.agent import actions_search         # noqa: F401 — Phase 33a full-text search
from orgchem.agent import script_context         # noqa: F401 — Phase 32a scripting

__all__ = ["action", "registry", "invoke", "ActionSpec"]
