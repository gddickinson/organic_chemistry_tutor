"""Regression test for the round-204 user-reported bug.

The tutor's chat backend occasionally calls `show_molecule` with
an INTEGER for the `name_or_id` parameter (e.g. `{"name_or_id":
7}`) — typically because a prior tool response surfaced an `id:
7` field and the LLM passed it back verbatim instead of casting
to a string.  The original implementations of seven `*_by_id`
agent actions did `name_or_id.isdigit()` directly, which raises
``AttributeError: 'int' object has no attribute 'isdigit'``.

Round 204 fixed all seven sites by coercing
`name_or_id = str(name_or_id)` at the top of each function.
This test locks in the fix.
"""
from __future__ import annotations
import os
import pytest

pytest.importorskip("rdkit")
pytest.importorskip("PySide6")
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


@pytest.fixture(scope="module")
def app():
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(5)
        yield h


# ==================================================================
# show_molecule (library.py) — the original bug site
# ==================================================================

def test_show_molecule_accepts_int_id(app):
    """`show_molecule(7)` should NOT raise — equivalent to
    `show_molecule("7")`."""
    from orgchem.db.queries import list_molecules
    rows = list_molecules()
    assert rows, "no molecules seeded"
    a_row = rows[0]
    # Pass the id as a plain int (the bug repro).
    res = app.call("show_molecule", name_or_id=int(a_row.id))
    assert "error" not in res, f"unexpected error: {res}"
    assert res["id"] == int(a_row.id)


def test_show_molecule_accepts_string_id(app):
    """The original code path (string id) still works."""
    from orgchem.db.queries import list_molecules
    rows = list_molecules()
    a_row = rows[0]
    res = app.call("show_molecule", name_or_id=str(a_row.id))
    assert "error" not in res
    assert res["id"] == int(a_row.id)


def test_show_molecule_accepts_name(app):
    """Name lookup unchanged."""
    res = app.call("show_molecule", name_or_id="Caffeine")
    assert "error" not in res
    assert res["name"] == "Caffeine"


# ==================================================================
# show_reaction / play_reaction_trajectory / get_mechanism_details /
# open_mechanism (actions_reactions.py) + add_molecule_synonym
# (actions_authoring.py) + show_pathway (actions_pathways.py)
# ==================================================================

def test_show_reaction_accepts_int_id(app):
    """Same int-tolerance for show_reaction."""
    from orgchem.db.queries import list_reactions
    rows = list_reactions()
    if not rows:
        pytest.skip("no reactions seeded")
    a_row = rows[0]
    res = app.call("show_reaction", name_or_id=int(a_row.id))
    # Either resolves (no error) OR returns a structured error
    # (NEVER raises the AttributeError).
    assert isinstance(res, dict)
    assert "AttributeError" not in str(res)


def test_open_mechanism_accepts_int_id(app):
    """open_mechanism does its own DB lookup; same tolerance."""
    res = app.call("open_mechanism", name_or_id=1)
    assert isinstance(res, dict)
    assert "AttributeError" not in str(res)


def test_get_mechanism_details_accepts_int_id(app):
    """get_mechanism_details was the 4th reactions-file site."""
    res = app.call("get_mechanism_details", name_or_id=1)
    assert isinstance(res, dict)
    assert "AttributeError" not in str(res)


def test_play_reaction_trajectory_accepts_int_id(app):
    """play_reaction_trajectory was the 2nd reactions-file site."""
    res = app.call("play_reaction_trajectory", name_or_id=1)
    assert isinstance(res, dict)
    assert "AttributeError" not in str(res)


def test_show_pathway_accepts_int_id(app):
    """show_pathway in actions_pathways.py."""
    res = app.call("show_pathway", name_or_id=1)
    assert isinstance(res, dict)
    assert "AttributeError" not in str(res)


def test_add_molecule_synonym_accepts_int_id(app):
    """add_molecule_synonym in actions_authoring.py.  Use a
    Tutor-test name so the round-94 cleanup hook scrubs it."""
    from orgchem.db.queries import list_molecules
    rows = list_molecules()
    a_row = rows[0]
    res = app.call(
        "add_molecule_synonym",
        name_or_id=int(a_row.id),
        synonym="Tutor-test-int-tolerance-synonym",
    )
    assert isinstance(res, dict)
    assert "AttributeError" not in str(res)


# ==================================================================
# All-at-once sweep — every name_or_id-taking action survives
# an int input
# ==================================================================

def test_invoke_handles_action_with_name_kwarg(app):
    """Round-204b (driver-test discovery): `import_smiles(name,
    smiles)` declares a parameter literally called `name`.  The
    conversation loop calls `invoke(tc.name, **tc.arguments)` — if
    `tc.arguments` contains `{"name": "glucose"}`, the dispatcher's
    own `name` parameter collides + Python raises
    ``TypeError: invoke() got multiple values for argument 'name'``.
    Fixed by making `invoke()`'s name argument **positional-only**.
    """
    from orgchem.agent.actions import invoke
    res = invoke(
        "import_smiles",
        name="Tutor-test-import-name-collision",
        smiles="CCO",
    )
    assert isinstance(res, dict)
    # Either added a new row or matched an existing InChIKey row;
    # both are valid.  What we care about is no TypeError raised.
    assert "id" in res or "error" in res


def test_invoke_signature_is_positional_only(app):
    """Lock in the positional-only contract so a future signature
    change can't reintroduce the import_smiles collision."""
    import inspect
    from orgchem.agent.actions import invoke
    sig = inspect.signature(invoke)
    name_param = sig.parameters["name"]
    assert name_param.kind == inspect.Parameter.POSITIONAL_ONLY, (
        f"invoke()'s `name` must stay positional-only "
        f"(currently {name_param.kind})"
    )


def test_all_name_or_id_actions_tolerate_int(app):
    """Walk the registry for actions whose schema declares a
    `name_or_id` parameter and verify each one is int-tolerant."""
    from orgchem.agent.actions import registry
    failures = []
    for name, spec in registry().items():
        params = {p["name"]: p for p in spec.params}
        if "name_or_id" not in params:
            continue
        # Build minimal required-arg dict; pass int for name_or_id.
        kwargs = {}
        for p in spec.params:
            if not p["required"]:
                continue
            if p["name"] == "name_or_id":
                kwargs[p["name"]] = 1
            elif p["name"] == "synonym":
                kwargs[p["name"]] = "Tutor-test-sweep"
            elif p["type"] == "string":
                kwargs[p["name"]] = ""
            elif p["type"] == "integer":
                kwargs[p["name"]] = 0
            else:
                kwargs[p["name"]] = None
        try:
            res = app.call(name, **kwargs)
            if not isinstance(res, dict):
                continue
            if "AttributeError" in str(res):
                failures.append(f"{name}: {res}")
        except AttributeError as e:
            failures.append(f"{name}: AttributeError: {e}")
    assert not failures, (
        "Actions that don't tolerate int name_or_id:\n"
        + "\n".join(f"  - {f}" for f in failures)
    )
