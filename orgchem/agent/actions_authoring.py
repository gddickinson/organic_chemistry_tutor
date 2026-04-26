"""Content-authoring actions — round 55 follow-up to the tutor
capability boost.

User ask: *"It might also be useful if the tutor is able to populate
databases, seed reactions and tutorials with new items and modules —
as long as they are of high quality!"*

These actions let the tutor (or any agent driver) add new content
at runtime. Every writer validates the submission up front:

- Molecules: SMILES must parse via RDKit; name + SMILES required;
  duplicate name or canonical SMILES → reject.
- Reactions: reaction SMILES must parse as an ``rdkit.Chem.rxn``;
  name + description + category required; duplicate name → reject.
- Glossary terms: term + short definition required; duplicate
  term → reject unless ``overwrite=True``.
- Tutorial lessons: title + level + markdown_body required; the
  lesson is written to a new ``.md`` file inside
  ``orgchem/tutorial/content/<level>/`` and appended to
  :data:`orgchem.tutorial.curriculum.CURRICULUM` at runtime.

All writes log a clear message so the user can see what the tutor
just added. None of these actions commit to disk for the main
``Molecule`` / ``Reaction`` / ``GlossaryTerm`` DB tables — they go
through the SQLAlchemy session which is what the rest of the app
uses, so the new rows persist across launches like any other
seeded content.

If a rejection happens, the returned dict has ``"status":
"rejected"`` plus a ``"reason"`` string that tells the tutor *why*
and lets it try again.
"""
from __future__ import annotations
import json
import logging
import re
from pathlib import Path
from typing import Any, Dict, Optional

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


# ---------------------------------------------------------------------
# Helpers

def _rejected(reason: str, **extra: Any) -> Dict[str, Any]:
    return {"status": "rejected", "reason": reason, **extra}


def _accepted(**fields: Any) -> Dict[str, Any]:
    return {"status": "accepted", **fields}


# ---------------------------------------------------------------------
# Molecules

@action(category="authoring")
def add_molecule(mol_name: str, smiles: str, notes: str = "",
                 source_tags: Optional[list] = None,
                 fetch_synonyms: bool = False,
                 ) -> Dict[str, Any]:
    """Add a new molecule to the seeded DB at runtime.

    Validates the SMILES with RDKit (rejects unparseable strings),
    checks for a duplicate ``mol_name`` or canonical SMILES, and if
    everything looks good inserts a new ``Molecule`` row through
    the normal SQLAlchemy session. Returns
    ``{"status": "accepted", "id": int, "name": str, "smiles":
    canonical_smiles}`` on success, or
    ``{"status": "rejected", "reason": ...}`` otherwise.

    Tutors should use this for compounds that don't appear in the
    seeded catalogue — e.g. a student asks about a drug the app
    doesn't know. Canonical SMILES from PubChem or the
    `search_pubchem` action is safer than hand-typed fragments.

    **Phase 35b** — pass ``fetch_synonyms=True`` to also query
    PubChem by InChIKey after validation and populate
    ``Molecule.synonyms_json``.  Best-effort: silent skip on
    missing ``pubchempy`` / network error; never affects the
    accepted/rejected outcome.  The accepted response's
    ``synonyms_fetched`` field reports how many natural-language
    aliases were added (0 when offline / no match).
    """
    name = mol_name
    if not name or not name.strip():
        return _rejected("`mol_name` is required.")
    if not smiles or not smiles.strip():
        return _rejected("`smiles` is required.")
    try:
        from rdkit import Chem
    except ImportError:
        return _rejected("RDKit unavailable — can't validate SMILES.")
    mol = Chem.MolFromSmiles(smiles.strip())
    if mol is None:
        return _rejected(
            f"SMILES {smiles!r} doesn't parse. Check for typos — "
            f"common fixes: close brackets, match case (lowercase "
            f"aromatic atoms, uppercase sp³).")
    canonical = Chem.MolToSmiles(mol, canonical=True)
    # Round 58 — compute InChIKey so we can dedup against entries
    # stored with a different-looking SMILES for the same molecule.
    from orgchem.core.identity import inchikey as _inchikey
    key = _inchikey(canonical)

    from orgchem.db.models import Molecule as DBMol
    from orgchem.db.session import session_scope
    with session_scope() as s:
        existing_by_name = s.query(DBMol).filter(
            DBMol.name == name.strip()).one_or_none()
        if existing_by_name is not None:
            return _rejected(
                f"A molecule named {name!r} already exists "
                f"(id={existing_by_name.id}). Use "
                f"`get_molecule_details` to inspect it, or pick a "
                f"different name.",
                existing_id=existing_by_name.id,
            )
        # Canonical-SMILES dedup (cheap indexed check).
        existing_by_smiles = s.query(DBMol).filter(
            DBMol.smiles == canonical).one_or_none()
        if existing_by_smiles is not None:
            return _rejected(
                f"That canonical SMILES is already seeded as "
                f"{existing_by_smiles.name!r} "
                f"(id={existing_by_smiles.id}). If you know it by "
                f"another name, add {name!r} as a synonym on the "
                f"existing row instead.",
                existing_id=existing_by_smiles.id,
            )
        # InChIKey dedup — catches the round-58 bug where the same
        # compound is submitted with a differently-written SMILES
        # (e.g. retinol from PubChem vs the lipid catalogue form).
        if key is not None:
            existing_by_key = s.query(DBMol).filter(
                DBMol.inchikey == key).one_or_none()
            if existing_by_key is not None:
                return _rejected(
                    f"Same molecule (InChIKey {key}) is already "
                    f"seeded as {existing_by_key.name!r} "
                    f"(id={existing_by_key.id}). The SMILES string "
                    f"differs but it's the same compound — add "
                    f"{name!r} as a synonym on that row instead.",
                    existing_id=existing_by_key.id,
                )
        # Phase 35b — best-effort PubChem synonym lookup.
        syns_payload: Optional[str] = None
        synonyms_fetched = 0
        if fetch_synonyms and key:
            from orgchem.sources.pubchem import fetch_synonyms_by_inchikey
            from orgchem.gui.dialogs.command_palette import (
                _looks_like_registry_id,
            )
            raw = fetch_synonyms_by_inchikey(key)
            name_lower = name.strip().lower()
            cleaned: list[str] = []
            seen = {name_lower}
            for s_ in raw:
                if not isinstance(s_, str):
                    continue
                s_ = s_.strip()
                if not s_ or s_.lower() in seen:
                    continue
                if _looks_like_registry_id(s_):
                    continue
                seen.add(s_.lower())
                cleaned.append(s_)
                if len(cleaned) >= 10:
                    break
            if cleaned:
                syns_payload = json.dumps(cleaned)
                synonyms_fetched = len(cleaned)
        row = DBMol(
            name=name.strip(),
            smiles=canonical,
            inchikey=key,
            # ``Molecule`` has no `notes` column — the note lives in
            # ``properties_json`` under the "tutor_notes" key so it
            # round-trips without a schema migration.
            properties_json=json.dumps({
                "tutor_notes": notes or "",
            }) if notes else None,
            source_tags_json=json.dumps(list(source_tags or [])),
            synonyms_json=syns_payload,
        )
        s.add(row)
        s.flush()
        new_id = row.id
    log.info("Tutor-authored molecule added: %s (id=%d)", name, new_id)
    return _accepted(id=new_id, name=name.strip(),
                     smiles=canonical, notes=notes,
                     synonyms_fetched=synonyms_fetched)


# ---------------------------------------------------------------------
# Synonyms

@action(category="authoring")
def add_molecule_synonym(name_or_id: str, synonym: str) -> Dict[str, Any]:
    """Attach an alternate name to an existing ``Molecule`` row.

    Solves the round-58 reported bug: a compound is stored under
    one name ("(2E,4E,6E,8E)-3,7-dimethyl-9-(2,6,6-trimethyl…)")
    but the user searches by another ("retinol"). Calling
    ``add_molecule_synonym("…trimethyl…", "Retinol")`` tags the
    row so the normal search path picks it up.

    Accepts either a numeric id (string form) or a name (the same
    forgiving match as :func:`find_molecule_by_name`). Idempotent:
    if the synonym is already attached, returns ``updated=False``.
    """
    name_or_id = str(name_or_id)   # tolerate int from prior tool result
    if not name_or_id or not name_or_id.strip():
        return _rejected("`name_or_id` is required.")
    if not synonym or not synonym.strip():
        return _rejected("`synonym` is required.")
    from orgchem.db.models import Molecule as DBMol
    from orgchem.db.session import session_scope
    from orgchem.db.queries import find_molecule_by_name
    with session_scope() as s:
        row = None
        if name_or_id.isdigit():
            row = s.get(DBMol, int(name_or_id))
        if row is None:
            row = find_molecule_by_name(name_or_id)
            if row is not None:
                # Rebind into this session.
                row = s.get(DBMol, row.id)
        if row is None:
            return _rejected(
                f"No molecule matches {name_or_id!r}.")
        try:
            existing = json.loads(row.synonyms_json) \
                if row.synonyms_json else []
        except Exception:  # noqa: BLE001
            existing = []
        new_syn = synonym.strip()
        from orgchem.core.identity import normalise_name
        existing_norm = {normalise_name(s) for s in existing}
        if normalise_name(new_syn) in existing_norm \
                or normalise_name(new_syn) == normalise_name(row.name):
            return _accepted(id=row.id, name=row.name,
                             synonyms=existing, updated=False)
        existing.append(new_syn)
        row.synonyms_json = json.dumps(existing)
        log.info("Tagged molecule %r (id=%d) with synonym %r",
                 row.name, row.id, new_syn)
        return _accepted(id=row.id, name=row.name,
                         synonyms=existing, updated=True)


# ---------------------------------------------------------------------
# Reactions

@action(category="authoring")
def add_reaction(rxn_name: str, reaction_smiles: str, description: str,
                 rxn_category: str = "General") -> Dict[str, Any]:
    """Add a new named reaction to the seeded DB.

    Validates the reaction SMILES with RDKit
    (``AllChem.ReactionFromSmarts(..., useSmiles=True)``), checks
    for duplicates by name, and writes a new ``Reaction`` row.
    Description should be 2–6 sentences explaining the mechanism,
    conditions, and teaching point — this is what shows up in the
    Reactions tab.
    """
    name = rxn_name
    category = rxn_category
    for field, label in ((name, "rxn_name"),
                         (reaction_smiles, "reaction_smiles"),
                         (description, "description")):
        if not field or not field.strip():
            return _rejected(f"`{label}` is required.")
    try:
        from rdkit.Chem import AllChem
    except ImportError:
        return _rejected("RDKit unavailable — can't validate reaction.")
    try:
        rxn = AllChem.ReactionFromSmarts(reaction_smiles,
                                         useSmiles=True)
    except Exception as e:  # noqa: BLE001
        return _rejected(
            f"reaction_smiles {reaction_smiles!r} doesn't parse: {e}")
    if rxn is None or rxn.GetNumReactantTemplates() == 0 \
            or rxn.GetNumProductTemplates() == 0:
        return _rejected(
            "reaction_smiles parsed but has no reactants or "
            "products. Expected format: 'ReactantA.ReactantB>>Product'.")

    from orgchem.db.models import Reaction as DBRxn
    from orgchem.db.session import session_scope
    with session_scope() as s:
        existing = s.query(DBRxn).filter(
            DBRxn.name == name.strip()).one_or_none()
        if existing is not None:
            return _rejected(
                f"A reaction named {name!r} already exists "
                f"(id={existing.id}).",
                existing_id=existing.id,
            )
        row = DBRxn(
            name=name.strip(),
            reaction_smarts=reaction_smiles.strip(),
            category=category or "General",
            description=description.strip(),
        )
        s.add(row)
        s.flush()
        new_id = row.id
    log.info("Tutor-authored reaction added: %s (id=%d)", name, new_id)
    return _accepted(id=new_id, name=name.strip(), category=category)


# ---------------------------------------------------------------------
# Glossary

@action(category="authoring")
def add_glossary_term(term: str, definition_md: str,
                      category: str = "general",
                      aliases: Optional[list] = None,
                      see_also: Optional[list] = None,
                      overwrite: bool = False,
                      ) -> Dict[str, Any]:
    """Add a new glossary entry to the DB.

    ``term`` must be unique unless ``overwrite=True`` (which
    updates the existing row's definition). ``definition_md``
    should be a short, self-contained markdown paragraph.
    ``category`` defaults to ``"general"``; recommended buckets:
    fundamentals / mechanism / reactions / stereochemistry /
    spectroscopy / medicinal-chemistry / enzyme-mechanism.
    """
    if not term or not term.strip():
        return _rejected("`term` is required.")
    if not definition_md or not definition_md.strip():
        return _rejected("`definition_md` is required.")
    if len(definition_md.strip()) < 30:
        return _rejected(
            "Definition is too short (need ≥ 30 chars). "
            "A single complete sentence minimum.")

    from orgchem.db.models import GlossaryTerm
    from orgchem.db.session import session_scope
    with session_scope() as s:
        existing = s.query(GlossaryTerm).filter(
            GlossaryTerm.term == term.strip()).one_or_none()
        if existing is not None and not overwrite:
            return _rejected(
                f"A glossary term {term!r} already exists. Pass "
                f"overwrite=True to update it.",
                existing_id=existing.id,
            )
        if existing is not None:
            existing.definition_md = definition_md.strip()
            existing.aliases_json = json.dumps(list(aliases or []))
            existing.see_also_json = json.dumps(list(see_also or []))
            existing.category = category or "general"
            return _accepted(id=existing.id, term=term.strip(),
                             updated=True)
        row = GlossaryTerm(
            term=term.strip(),
            definition_md=definition_md.strip(),
            aliases_json=json.dumps(list(aliases or [])),
            see_also_json=json.dumps(list(see_also or [])),
            category=category or "general",
        )
        s.add(row)
        s.flush()
        new_id = row.id
    log.info("Tutor-authored glossary term added: %s (id=%d)",
             term, new_id)
    return _accepted(id=new_id, term=term.strip(), updated=False)


# ---------------------------------------------------------------------
# Tutorial lessons

_TUTORIAL_CONTENT = (
    Path(__file__).resolve().parent.parent / "tutorial" / "content"
)
_VALID_LEVELS = ("beginner", "intermediate", "advanced", "graduate")


def _slug(text: str) -> str:
    """Filesystem-safe slug from a lesson title."""
    base = re.sub(r"[^\w\- ]", "", text).strip().lower()
    return re.sub(r"\s+", "_", base)[:60] or "lesson"


@action(category="authoring")
def add_tutorial_lesson(title: str, level: str,
                        markdown_body: str) -> Dict[str, Any]:
    """Add a new curriculum lesson at runtime.

    Writes a new ``.md`` file under
    ``orgchem/tutorial/content/<level>/`` with a filename derived
    from the title (slug), and appends the lesson to
    :data:`orgchem.tutorial.curriculum.CURRICULUM` so it shows up
    in the Tutorials tab immediately (no app restart needed).
    """
    if not title.strip():
        return _rejected("`title` is required.")
    if level not in _VALID_LEVELS:
        return _rejected(
            f"`level` must be one of {_VALID_LEVELS}.")
    if not markdown_body or not markdown_body.strip():
        return _rejected("`markdown_body` is required.")
    if len(markdown_body.strip()) < 200:
        return _rejected(
            "Lesson body is too short (need ≥ 200 chars). "
            "Aim for a few paragraphs + at least one example.")
    # Encourage the {term:X} macro pattern — soft nudge, not a hard
    # reject: the tutor can add links later.
    has_heading = any(line.startswith("#") for line in
                      markdown_body.splitlines()[:3])
    if not has_heading:
        # Prepend a title heading so the rendered lesson has a banner.
        markdown_body = f"# {title.strip()}\n\n{markdown_body.strip()}\n"

    target_dir = _TUTORIAL_CONTENT / level
    target_dir.mkdir(parents=True, exist_ok=True)
    stem = _slug(title)
    path = target_dir / f"{stem}.md"
    i = 2
    while path.exists():
        path = target_dir / f"{stem}_{i}.md"
        i += 1
    path.write_text(markdown_body)

    # Append to the in-process curriculum so the Tutorials tab
    # picks up the new lesson on next tree rebuild.
    try:
        from orgchem.tutorial.curriculum import CURRICULUM
        CURRICULUM.setdefault(level, []).append(
            {"title": title.strip(), "path": path}
        )
    except Exception as e:  # noqa: BLE001
        log.warning("Wrote lesson file but couldn't append to "
                    "CURRICULUM: %s", e)
    log.info("Tutor-authored lesson written: %s", path)
    return _accepted(title=title.strip(), level=level,
                     path=str(path), bytes=len(markdown_body))
