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
    assert len(rows) >= 20, f"expected ≥20 energy profiles, got {len(rows)}"
    # All mechanism-carrying reactions should have profiles —
    # Phase 31e closes at 20/20 in round 106.
    for expected in ("SN2: methyl bromide", "SN1: tert-butyl",
                     "E1: tert-butyl", "E2: 2-bromobutane",
                     "Diels-Alder", "Aldol", "Grignard",
                     "Wittig", "Michael",
                     "Sonogashira", "Horner", "Mitsunobu",
                     "Claisen condensation",
                     "Fischer esterification",
                     "Nitration of benzene",
                     "NaBH4 reduction",
                     "Bromination of ethene",
                     "Pinacol rearrangement",
                     "Chymotrypsin",
                     "Friedel-Crafts alkylation"):
        assert any(expected in n for n in names), f"missing profile for {expected!r}"


def test_friedel_crafts_profile_has_free_cation(app):
    """Phase 31e round 106 — Friedel-Crafts alkylation must
    show the distinctive pre-equilibrium free-cation step
    that separates it pedagogically from nitration.  The
    methyl cation intermediate (step 2) sits above the
    reactant baseline — a genuine endergonic free-cation
    minimum — unlike nitration where the nitronium ion is
    pre-formed in the H₂SO₄ / HNO₃ mixture.  That "cation is
    real and unstable" shape is why FC alkylation suffers
    rearrangement + poly-alkylation."""
    from orgchem.core.energy_profile import ReactionEnergyProfile
    rows = app.call("list_energy_profiles")
    fc = next(r for r in rows if "Friedel-Crafts alkylation" in r["name"])
    got = app.call("get_energy_profile", reaction_id=fc["id"])
    prof = ReactionEnergyProfile.from_dict(got["profile"])
    pts = prof.points
    ts_count = sum(1 for p in pts if p.is_ts)
    # 3 TSs (cation gen, attack, deprotonation) vs nitration's 2 TSs.
    assert ts_count == 3, ts_count
    # Methyl cation intermediate present and strictly above
    # the reactant baseline (endergonic).
    cation_min = next(p for p in pts
                      if "Methyl cation" in p.label)
    assert cation_min.energy > 0, (
        "Free CH₃⁺ intermediate should sit above the reactant "
        "baseline — that's the FC teaching point")
    # Wheland intermediate also present; its energy is the
    # σ-complex valley familiar from nitration.
    wheland = next(p for p in pts
                   if "Wheland" in p.label or "arenium" in p.label.lower())
    # Wheland sits above the reactant baseline too (like nitration).
    assert wheland.energy > 0


def test_chymotrypsin_profile_acyl_enzyme_well(app):
    """Phase 31e round 105 — enzyme-catalysed serine protease
    hydrolysis must encode the **covalent-catalysis double-hump**
    shape: two tetrahedral intermediates bracketing a covalent
    acyl-enzyme minimum that sits BELOW the starting Michaelis
    complex.  The acyl-enzyme as a real isolable intermediate is
    THE structural feature that separates serine proteases from
    solution-phase amide hydrolysis."""
    from orgchem.core.energy_profile import ReactionEnergyProfile
    rows = app.call("list_energy_profiles")
    ch = next(r for r in rows if "Chymotrypsin" in r["name"])
    got = app.call("get_energy_profile", reaction_id=ch["id"])
    prof = ReactionEnergyProfile.from_dict(got["profile"])
    pts = prof.points
    ts_count = sum(1 for p in pts if p.is_ts)
    assert ts_count == 4, ts_count
    # Locate the acyl-enzyme minimum and both tetrahedral
    # intermediates by name.
    acyl = next(p for p in pts if "Acyl-enzyme" in p.label)
    t1 = next(p for p in pts if "Tetrahedral intermediate 1" in p.label)
    t2 = next(p for p in pts if "Tetrahedral intermediate 2" in p.label)
    michaelis = pts[0]
    # Acyl-enzyme sits BELOW the Michaelis complex — the key
    # "first half is favourable" inequality.
    assert acyl.energy < michaelis.energy, (
        "Acyl-enzyme intermediate should sit below the Michaelis "
        "complex: the acylation half-reaction is favourable, the "
        "deacylation half-reaction does the remaining work")
    # Both tetrahedral intermediates sit above Michaelis but
    # below the highest TS — the oxyanion-hole stabilisation
    # point.  (They're real minima, not saddles.)
    highest_ts_energy = max(p.energy for p in pts if p.is_ts)
    for tet in (t1, t2):
        assert tet.energy > michaelis.energy
        assert tet.energy < highest_ts_energy


def test_pinacol_profile_methyl_shift_downhill(app):
    """Phase 31e round 104 — pinacol rearrangement must encode
    the "migration goes downhill" teaching point: the TS for
    the 1,2-methyl shift is lower than the TS for ionisation
    (shift is fast once the carbocation exists), AND the
    post-shift oxocarbenium minimum is strictly below the
    pre-shift tertiary-carbocation minimum (the O lone pair
    stabilises the oxocarbenium better than hyperconjugation
    stabilises a tert-C⁺)."""
    from orgchem.core.energy_profile import ReactionEnergyProfile
    rows = app.call("list_energy_profiles")
    pr = next(r for r in rows if "Pinacol rearrangement" in r["name"])
    got = app.call("get_energy_profile", reaction_id=pr["id"])
    prof = ReactionEnergyProfile.from_dict(got["profile"])
    pts = prof.points
    ts_pts = [p for p in pts if p.is_ts]
    assert len(ts_pts) == 3, len(ts_pts)
    # Ionisation TS (first) must be the highest of the three.
    assert ts_pts[0].energy > ts_pts[1].energy
    assert ts_pts[0].energy > ts_pts[2].energy
    # The carbocation vs oxocarbenium stability inequality.
    cation = next(p for p in pts if "carbocation" in p.label.lower())
    oxo = next(p for p in pts if "Protonated ketone" in p.label)
    assert oxo.energy < cation.energy, (
        "Oxocarbenium (post-shift) should sit below the tertiary "
        "carbocation (pre-shift) — that's why 1,2-shifts run "
        "forward, not reverse")


def test_bromination_profile_bromonium_valley(app):
    """Phase 31e round 103 — bromination of an alkene must
    encode the bromonium-valley shape that rationalises
    anti-addition stereochemistry.  Bromonium intermediate
    sits above reactants (endergonic — small valley) but
    below the first (rate-limiting) TS; the second TS
    (anti-SN2 attack) is lower than the first.  Product
    strongly exergonic (new C-Br + C-Br bonds)."""
    from orgchem.core.energy_profile import ReactionEnergyProfile
    rows = app.call("list_energy_profiles")
    br = next(r for r in rows if "Bromination of ethene" in r["name"])
    got = app.call("get_energy_profile", reaction_id=br["id"])
    prof = ReactionEnergyProfile.from_dict(got["profile"])
    ts_points = [p for p in prof.points if p.is_ts]
    min_points = [p for p in prof.points if not p.is_ts]
    assert len(ts_points) == 2
    assert len(min_points) == 3
    # RDS is step 1 (bromonium formation) — first TS highest.
    assert ts_points[0].energy > ts_points[1].energy
    # Bromonium intermediate sits above reactants (endergonic
    # relative to starting alkene + Br₂) — that's the "valley".
    bromonium = min_points[1]
    reactants = min_points[0]
    assert bromonium.energy > reactants.energy
    # But strictly below both TSs.
    assert bromonium.energy < ts_points[0].energy
    assert bromonium.energy < ts_points[1].energy
    # Net exergonic — two C-Br bonds formed.
    assert prof.delta_h is not None and prof.delta_h < -50


def test_nabh4_profile_strongly_exergonic(app):
    """Phase 31e round 102 — NaBH₄ reduction is a canonical
    textbook example of an irreversible, highly-exergonic
    1,2-hydride addition.  Assert a single rate-limiting TS
    (the B-H···C=O 4-centre), a stabilised alkoxide well, and
    a net ΔH well below −50 kJ/mol."""
    from orgchem.core.energy_profile import ReactionEnergyProfile
    rows = app.call("list_energy_profiles")
    nb = next(r for r in rows if "NaBH4 reduction" in r["name"])
    got = app.call("get_energy_profile", reaction_id=nb["id"])
    prof = ReactionEnergyProfile.from_dict(got["profile"])
    assert prof.delta_h is not None
    assert prof.delta_h < -50, (
        f"NaBH₄ reduction should be strongly exergonic; "
        f"got ΔH = {prof.delta_h}")
    # The first TS (hydride transfer) must be the only real
    # barrier ABOVE the reactant baseline — workup is downhill.
    first_ts = next(p for p in prof.points if p.is_ts)
    assert first_ts.energy > 0
    above_zero_ts = [p for p in prof.points if p.is_ts and p.energy > 0]
    assert len(above_zero_ts) == 1, (
        "Only the hydride-transfer TS should sit above the "
        "reactant baseline; workup barrier is well below.")


def test_nitration_profile_has_wheland_valley(app):
    """Phase 31e round 101 — EAS nitration must encode the
    textbook "shallow Wheland valley": first TS (RDS addition)
    higher than the second TS (deprotonation), with the arenium
    intermediate sitting ABOVE the reactant baseline but BELOW
    both TSs.  Classic 3-point EAS saddle-dip-saddle shape."""
    from orgchem.core.energy_profile import ReactionEnergyProfile
    rows = app.call("list_energy_profiles")
    ni = next(r for r in rows if "Nitration of benzene" in r["name"])
    got = app.call("get_energy_profile", reaction_id=ni["id"])
    prof = ReactionEnergyProfile.from_dict(got["profile"])
    ts_points = [p for p in prof.points if p.is_ts]
    min_points = [p for p in prof.points if not p.is_ts]
    # 2 TSs + 3 minima (reactants, Wheland, products).
    assert len(ts_points) == 2, len(ts_points)
    assert len(min_points) == 3, len(min_points)
    # First TS (attack) must be higher than second TS (deprotonation).
    assert ts_points[0].energy > ts_points[1].energy, (
        "First TS (rate-limiting NO₂⁺ addition) must exceed the "
        "second TS (deprotonation) for the EAS teaching shape to "
        "be correct")
    # Wheland intermediate (middle minimum) sits above reactants but
    # below both TSs.
    wheland = min_points[1]
    assert wheland.energy > min_points[0].energy  # above reactants
    assert wheland.energy < ts_points[0].energy
    assert wheland.energy < ts_points[1].energy


def test_fischer_profile_is_thermoneutral(app):
    """Phase 31e round 99 — Fischer esterification must encode
    the textbook teaching point: ΔG ≈ 0 (K ≈ 3), not a deep
    thermodynamic sink.  Without Le Chatelier drive (excess
    alcohol / Dean-Stark) the reaction barely proceeds.  Assert
    the product energy sits within ±15 kJ/mol of the reactant
    baseline — much shallower than any other seeded profile."""
    from orgchem.core.energy_profile import ReactionEnergyProfile
    rows = app.call("list_energy_profiles")
    fi = next(r for r in rows if "Fischer esterification" in r["name"])
    got = app.call("get_energy_profile", reaction_id=fi["id"])
    prof = ReactionEnergyProfile.from_dict(got["profile"])
    assert prof.delta_h is not None
    assert abs(prof.delta_h) < 15, (
        "Fischer is near-thermoneutral; |ΔH| should be < 15 kJ/mol "
        f"to visualise the 'need Le Chatelier drive' point, got {prof.delta_h}")


def test_claisen_profile_driven_by_final_deprotonation(app):
    """Phase 31e round 98 — Claisen condensation energy profile
    must encode the textbook teaching point: the FINAL step
    (deprotonation of the β-ketoester α-H) is what drives the
    equilibrium.  Check that the penultimate minimum ("Neutral
    β-ketoester") sits near zero and the final product sits
    well below it."""
    from orgchem.core.energy_profile import ReactionEnergyProfile
    rows = app.call("list_energy_profiles")
    cl = next(r for r in rows if "Claisen condensation" in r["name"])
    got = app.call("get_energy_profile", reaction_id=cl["id"])
    prof = ReactionEnergyProfile.from_dict(got["profile"])
    # 4-step mechanism → 4 transition states.
    ts_count = sum(1 for p in prof.points if p.is_ts)
    assert ts_count == 4, f"expected 4 TS, got {ts_count}"
    # Penultimate minimum is the neutral β-ketoester — should
    # sit near thermoneutral (|ΔG| < 20 kJ/mol).
    neutral = next(p for p in prof.points
                   if "Neutral β-ketoester" in p.label)
    assert abs(neutral.energy) < 20, neutral.energy
    # Final product (enolate + EtOH) must be well downhill from
    # that penultimate minimum — this IS the driving force.
    final = prof.points[-1]
    assert final.energy < neutral.energy - 20, (
        "Final deprotonation should drop ≥20 kJ/mol below the "
        "neutral β-ketoester intermediate")


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
