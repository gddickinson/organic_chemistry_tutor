"""Phase 32b regression tests for :mod:`orgchem.scene` — headless, no Qt."""
from __future__ import annotations

import pytest

from orgchem.scene import (
    Scene,
    SceneEvent,
    Track,
    current_scene,
    reset_current_scene,
)
from orgchem.scene.html import build_scene_html
from orgchem.scene.scene import TrackKind, _looks_like_pdb_id


@pytest.fixture(autouse=True)
def _fresh_scene():
    """Start each test with an empty current_scene()."""
    reset_current_scene()
    yield
    reset_current_scene()


def test_add_molecule_creates_track():
    s = Scene()
    t = s.add_molecule("CCO")
    assert isinstance(t, Track)
    assert t.kind == TrackKind.MOLECULE
    assert t.source_format == "mol"
    assert t.name.startswith("mol")
    assert "CCO" in t.meta.get("smiles", "")
    # Molblock must carry at least one atom line.
    assert "V2000" in t.data


def test_add_molecule_with_explicit_track_name():
    s = Scene()
    t = s.add_molecule("CCO", track="ethanol")
    assert t.name == "ethanol"


def test_duplicate_track_name_raises():
    s = Scene()
    s.add_molecule("CCO", track="ethanol")
    with pytest.raises(ValueError):
        s.add_molecule("CCO", track="ethanol")


def test_auto_names_do_not_collide():
    s = Scene()
    s.add_molecule("CCO")
    s.add_molecule("CC", track="ethane")
    s.add_molecule("c1ccccc1")
    names = [t.name for t in s.tracks()]
    assert len(set(names)) == 3
    assert "mol1" in names and "ethane" in names


def test_remove_and_clear():
    s = Scene()
    s.add_molecule("CCO", track="a")
    s.add_molecule("CC",  track="b")
    assert s.remove("a") is True
    assert s.remove("a") is False        # already gone
    assert [t.name for t in s.tracks()] == ["b"]
    s.clear()
    assert s.tracks() == []


def test_set_visible_and_set_style():
    s = Scene()
    s.add_molecule("CCO", track="eth")
    s.set_visible("eth", False)
    assert s.tracks()[0].visible is False
    s.set_style("eth", style="sphere", colour="spectrum", opacity=0.5)
    t = s.tracks()[0]
    assert t.style == "sphere"
    assert t.colour == "spectrum"
    assert t.opacity == 0.5


def test_listeners_receive_events():
    s = Scene()
    calls: list[tuple[SceneEvent, str | None]] = []
    s.listen(lambda ev, tr: calls.append(
        (ev, tr.name if tr else None)))
    s.add_molecule("CCO", track="eth")
    s.set_visible("eth", False)
    s.set_style("eth", style="sphere")
    s.remove("eth")
    s.clear()
    kinds = [c[0] for c in calls]
    assert SceneEvent.TRACK_ADDED in kinds
    assert SceneEvent.TRACK_VISIBILITY_CHANGED in kinds
    assert SceneEvent.TRACK_STYLE_CHANGED in kinds
    assert SceneEvent.TRACK_REMOVED in kinds


def test_listener_unsubscribe():
    s = Scene()
    calls = []
    unsub = s.listen(lambda ev, tr: calls.append(ev))
    s.add_molecule("CCO")
    first_count = len(calls)
    unsub()
    s.add_molecule("CC")
    assert len(calls) == first_count    # no new events


def test_current_scene_is_process_wide_singleton():
    a = current_scene()
    b = current_scene()
    assert a is b


def test_reset_current_scene_releases_singleton():
    a = current_scene()
    a.add_molecule("CCO")
    reset_current_scene()
    b = current_scene()
    assert b is not a
    assert b.tracks() == []


def test_build_scene_html_empty_scene_is_safe():
    s = Scene()
    html = build_scene_html(s)
    assert "<html>" in html.lower() or "<!DOCTYPE html>" in html
    assert "Scene empty" in html or "addLabel" in html
    assert "v.addModel" not in html    # no models yet


def test_build_scene_html_embeds_every_visible_track():
    s = Scene()
    s.add_molecule("CCO", track="a")
    s.add_molecule("CC",  track="b")
    s.add_molecule("c1ccccc1", track="c")
    html = build_scene_html(s)
    assert html.count("v.addModel") == 3
    s.set_visible("b", False)
    html2 = build_scene_html(s)
    assert html2.count("v.addModel") == 2


def test_build_scene_html_protein_adds_het_overlay():
    """Protein tracks should also apply a ligand (HETATM) stick
    style so bound cofactors aren't lost under the cartoon."""
    s = Scene()
    # Hand-roll a minimal Track so we avoid a PDB-fetch network hop.
    t = Track(
        name="p", kind=TrackKind.PROTEIN,
        data="HEADER    TEST\nEND\n",
        source_format="pdb",
        style="cartoon", colour="chain",
    )
    s._add_track(t)   # direct insertion — safe because we own the Scene
    html = build_scene_html(s)
    assert "hetflag: true" in html


def test_add_molecule_rejects_bogus_smiles():
    s = Scene()
    with pytest.raises(ValueError):
        s.add_molecule("not a molecule @#$%")


def test_add_molecule_accepts_rdkit_mol():
    from rdkit import Chem
    s = Scene()
    mol = Chem.MolFromSmiles("CCO")
    t = s.add_molecule(mol)
    assert "V2000" in t.data


def test_looks_like_pdb_id():
    assert _looks_like_pdb_id("2YDO")
    assert _looks_like_pdb_id("1hxw")
    # Pure-digit rejected (real PDB IDs always start with a digit
    # but also contain letters).
    assert not _looks_like_pdb_id("1234")
    # Longer strings are clearly not IDs.
    assert not _looks_like_pdb_id("HEADER    TEST\n")
    assert not _looks_like_pdb_id("toolong")


def test_snapshot_without_view_raises():
    """Headless Scene (no Workbench widget) should raise a clear
    error when snapshot is attempted — rather than silently failing."""
    s = Scene()
    s.add_molecule("CCO")
    with pytest.raises(RuntimeError, match="Workbench"):
        s.snapshot("/tmp/should-not-write.png")
