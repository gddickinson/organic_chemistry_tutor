"""Tests for Phase 13 — reaction-coordinate energy profiles."""
from __future__ import annotations
import json
import os
from pathlib import Path

import pytest


# ---- Core data model ------------------------------------------------

def test_profile_round_trip():
    from orgchem.core.energy_profile import ReactionEnergyProfile, StationaryPoint
    prof = ReactionEnergyProfile(
        reaction_id=7,
        title="Test profile",
        energy_unit="kJ/mol",
        source="unit test",
        points=[
            StationaryPoint(label="R", energy=0.0, note="reactants"),
            StationaryPoint(label="TS", energy=80.0, is_ts=True),
            StationaryPoint(label="P", energy=-20.0),
        ],
    )
    text = prof.to_json()
    data = json.loads(text)
    assert data["reaction_id"] == 7
    assert len(data["points"]) == 3
    assert data["points"][1]["is_ts"] is True

    clone = ReactionEnergyProfile.from_json(text)
    assert clone.title == "Test profile"
    assert clone.points[1].is_ts is True
    assert clone.points[0].note == "reactants"


def test_activation_energies_and_delta_h():
    from orgchem.core.energy_profile import ReactionEnergyProfile, StationaryPoint
    prof = ReactionEnergyProfile(points=[
        StationaryPoint(label="R", energy=0.0),
        StationaryPoint(label="TS1", energy=100.0, is_ts=True),
        StationaryPoint(label="Int", energy=60.0),
        StationaryPoint(label="TS2", energy=80.0, is_ts=True),
        StationaryPoint(label="P", energy=-15.0),
    ])
    assert prof.activation_energies == [100.0, 20.0]
    assert prof.delta_h == -15.0


def test_delta_h_none_with_single_minimum():
    from orgchem.core.energy_profile import ReactionEnergyProfile, StationaryPoint
    prof = ReactionEnergyProfile(points=[
        StationaryPoint(label="R", energy=0.0),
        StationaryPoint(label="TS", energy=80.0, is_ts=True),
    ])
    assert prof.delta_h is None


# ---- Renderer --------------------------------------------------------

def test_render_png_and_svg(tmp_path):
    from orgchem.core.energy_profile import ReactionEnergyProfile, StationaryPoint
    from orgchem.render.draw_energy_profile import export_profile
    prof = ReactionEnergyProfile(
        title="Render test",
        points=[
            StationaryPoint(label="R", energy=0.0),
            StationaryPoint(label="TS", energy=90.0, is_ts=True),
            StationaryPoint(label="P", energy=-50.0),
        ],
    )
    png = export_profile(prof, tmp_path / "p.png")
    svg = export_profile(prof, tmp_path / "p.svg")
    assert png.exists() and png.stat().st_size > 5_000
    svg_text = svg.read_text()
    assert "<svg" in svg_text
    # Key annotations should appear in the SVG
    assert "Ea" in svg_text
    assert "ΔH" in svg_text or "&#916;H" in svg_text  # mpl may entity-encode


def test_render_too_few_points_raises(tmp_path):
    from orgchem.core.energy_profile import ReactionEnergyProfile, StationaryPoint
    from orgchem.render.draw_energy_profile import export_profile
    from orgchem.messaging.errors import RenderError
    prof = ReactionEnergyProfile(points=[
        StationaryPoint(label="R", energy=0.0),
    ])
    with pytest.raises(RenderError):
        export_profile(prof, tmp_path / "bad.png")


def test_unsupported_format_raises(tmp_path):
    from orgchem.core.energy_profile import ReactionEnergyProfile, StationaryPoint
    from orgchem.render.draw_energy_profile import export_profile
    from orgchem.messaging.errors import RenderError
    prof = ReactionEnergyProfile(points=[
        StationaryPoint(label="R", energy=0.0),
        StationaryPoint(label="P", energy=-10.0),
    ])
    with pytest.raises(RenderError):
        export_profile(prof, tmp_path / "x.pdf")


# ---- Headless / seeded-data integration -----------------------------

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    pytest.importorskip("rdkit")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_seeded_profiles_present(app):
    rows = app.call("list_energy_profiles")
    names = {r["name"] for r in rows}
    assert len(rows) >= 9, f"expected ≥9 energy profiles, got {len(rows)}"
    # All 9 mechanism-carrying reactions should have profiles
    for expected in ("SN2: methyl bromide", "SN1: tert-butyl",
                     "E1: tert-butyl", "E2: 2-bromobutane",
                     "Diels-Alder", "Aldol", "Grignard",
                     "Wittig", "Michael"):
        assert any(expected in n for n in names), f"missing profile for {expected!r}"


def test_sn1_profile_has_two_transition_states(app):
    rows = app.call("list_energy_profiles")
    sn1 = next(r for r in rows if "SN1: tert-butyl" in r["name"])
    got = app.call("get_energy_profile", reaction_id=sn1["id"])
    pts = got["profile"]["points"]
    ts_count = sum(1 for p in pts if p["is_ts"])
    assert ts_count == 2, f"SN1 should have 2 TSs, got {ts_count}"
    # 2 TSs + 3 minima (R, intermediate, P)
    min_count = sum(1 for p in pts if not p["is_ts"])
    assert min_count == 3


def test_sn2_profile_single_barrier(app):
    rows = app.call("list_energy_profiles")
    sn2 = next(r for r in rows if "SN2: methyl bromide" in r["name"])
    got = app.call("get_energy_profile", reaction_id=sn2["id"])
    pts = got["profile"]["points"]
    ts_count = sum(1 for p in pts if p["is_ts"])
    assert ts_count == 1


def test_diels_alder_strongly_exothermic(app):
    """Textbook DA should have ΔH well below zero (cyclohexene is stable)."""
    from orgchem.core.energy_profile import ReactionEnergyProfile
    rows = app.call("list_energy_profiles")
    da = next(r for r in rows if "Diels-Alder" in r["name"])
    got = app.call("get_energy_profile", reaction_id=da["id"])
    prof = ReactionEnergyProfile.from_dict(got["profile"])
    assert prof.delta_h is not None
    assert prof.delta_h < -100  # kJ/mol — qualitative check


def test_export_via_agent(app, tmp_path):
    rows = app.call("list_energy_profiles")
    rid = rows[0]["id"]
    out = app.call("export_energy_profile", reaction_id=rid,
                   path=str(tmp_path / "profile.png"))
    assert "error" not in out
    assert Path(out["path"]).stat().st_size > 5_000

    out2 = app.call("export_energy_profile", reaction_id=rid,
                    path=str(tmp_path / "profile.svg"))
    assert "error" not in out2
    assert Path(out2["path"]).read_text().startswith(("<?xml", "<svg"))


def test_export_missing_id_returns_error(app, tmp_path):
    out = app.call("export_energy_profile", reaction_id=99_999,
                   path=str(tmp_path / "nope.png"))
    assert "error" in out


def test_get_without_profile_returns_error(app, tmp_path):
    """A reaction without a profile should return an error, not crash."""
    from orgchem.db.session import session_scope
    from orgchem.db.models import Reaction as DBRxn
    from sqlalchemy import select
    with session_scope() as s:
        row = s.scalars(select(DBRxn).where(
            DBRxn.energy_profile_json.is_(None)).limit(1)).first()
        assert row is not None
        rid_no_profile = row.id
    got = app.call("get_energy_profile", reaction_id=rid_no_profile)
    assert "error" in got
