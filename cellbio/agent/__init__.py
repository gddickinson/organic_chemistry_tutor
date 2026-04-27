"""Cell Bio Studio — agent actions.

Importing any module under ``cellbio.agent`` triggers registration
into the shared ``orgchem.agent.actions._REGISTRY``.  ``cellbio``'s
top-level ``__init__.py`` imports each `actions_*` module so the
whole studio's surface registers as soon as ``cellbio`` is imported.
"""
