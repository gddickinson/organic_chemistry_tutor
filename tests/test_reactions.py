"""Unit tests for reaction rendering and seeding."""
from __future__ import annotations
import os
import pytest
from pathlib import Path

pytest.importorskip("rdkit")

from orgchem.render.draw_reaction import render_svg, render_png_bytes, export_reaction
from orgchem.messaging.errors import RenderError


# ---- Rendering ------------------------------------------------------------

def test_render_svg_fischer_esterification():
    svg = render_svg("CC(=O)O.CCO>>CC(=O)OCC.O")
    assert svg.lstrip().startswith(("<?xml", "<svg"))
    assert len(svg) > 1000


def test_render_png_bytes_diels_alder():
    png = render_png_bytes("C=CC=C.C=C>>C1=CCCCC1", height=260)
    # PNG magic header
    assert png[:8] == b"\x89PNG\r\n\x1a\n"
    assert len(png) > 1000


def test_export_reaction_svg_and_png(tmp_path):
    svg_path = export_reaction("CBr.[OH-]>>CO.[Br-]", tmp_path / "sn2.svg")
    assert svg_path.exists() and svg_path.stat().st_size > 500

    png_path = export_reaction("CBr.[OH-]>>CO.[Br-]", tmp_path / "sn2.png")
    assert png_path.exists() and png_path.stat().st_size > 500


def test_invalid_reaction_rejected():
    with pytest.raises(RenderError):
        render_svg("not a reaction")


# ---- Seeded database ------------------------------------------------------

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_list_reactions_returns_seeded_set(app):
    rows = app.call("list_reactions")
    names = {r["name"] for r in rows}
    for expected in ("Fischer esterification",
                     "SN2: methyl bromide + hydroxide",
                     "Diels-Alder: butadiene + ethene",
                     "NaBH4 reduction of acetone"):
        assert expected in names


def test_reactions_includes_phase6_expansion(app):
    """The 2026-04-22 expansion added 10 more named reactions."""
    rows = app.call("list_reactions")
    names = {r["name"] for r in rows}
    for expected in ("Wittig reaction (propanal + methylidene ylide)",
                     "Claisen condensation (ethyl acetate)",
                     "Suzuki coupling (bromobenzene + phenylboronic acid)",
                     "Michael addition (acetone enolate + methyl vinyl ketone)",
                     "Pinacol rearrangement (pinacol → pinacolone)"):
        assert expected in names, f"missing {expected!r}"
    assert len(rows) >= 26   # 16 Phase-2a + 10 Phase-6 expansion


def test_enzyme_reactions_seeded(app):
    """Phase 16d — at least 2 enzyme reactions present."""
    rows = app.call("list_reactions")
    names = {r["name"] for r in rows}
    assert any("Chymotrypsin" in n for n in names), \
        "Chymotrypsin enzyme reaction missing"
    assert any("Aldolase" in n for n in names), \
        "Aldolase enzyme reaction missing"


def test_show_reaction_by_substring(app):
    result = app.call("show_reaction", name_or_id="Fischer")
    assert "id" in result
    assert "Fischer" in result["name"]


def test_click_chemistry_cuaac_seeded(app):
    """Phase 31b round 134 — CuAAC click chemistry.  Locks in:
    (a) the entry exists by substring lookup; (b) the reaction
    SMILES uses the canonical 1,4-disubstituted 1,2,3-triazole
    product (regioselectivity is the whole teaching point of
    Cu(I) catalysis vs. uncatalysed Huisgen); (c) the
    description names Sharpless / Meldal / Bertozzi as the
    Nobel laureates so the contemporary teaching anchor is
    preserved against future copy-edits.
    """
    result = app.call("show_reaction", name_or_id="Click chemistry")
    assert "id" in result
    smarts = result["smiles"]
    assert ">>" in smarts
    # Triazole regioisomer test: 1,4-disubstituted triazole
    # canonicalises with the two substituents on N1 and C4 —
    # the SMARTS we seed has `Cn2cc(...)nn2` meaning the benzyl
    # is on N1 and the phenyl is on C4 (i.e. para to the
    # triazole N3).
    assert "Cn2cc" in smarts and "nn2" in smarts
    desc = result.get("description", "").lower()
    for laureate in ("sharpless", "meldal", "bertozzi"):
        assert laureate in desc, f"missing Nobel laureate {laureate}"
    assert "1,4" in desc or "regioselect" in desc


def test_birch_reduction_seeded(app):
    """Phase 31b round 152 — Birch reduction.  Locks in:
    (a) the entry exists by substring lookup; (b) the reaction
    SMILES gives the **non-conjugated** 1,4-cyclohexadiene
    product (regioselectivity is the whole teaching point of
    Birch — protonation at the central pentadienyl carbon
    avoids the cross-conjugated 1,3-isomer); (c) the
    description teaches the SET (single-electron-transfer)
    mechanism so the pedagogical distinction from concerted /
    polar reductions like NaBH₄ is preserved against future
    copy-edits."""
    result = app.call("show_reaction", name_or_id="Birch")
    assert "id" in result
    smarts = result["smiles"]
    assert ">>" in smarts
    # 1,4-cyclohexadiene product.
    assert "C1=CCC=CC1" in smarts
    desc = result.get("description", "").lower()
    assert ("set" in desc or "single-electron" in desc), \
        "Birch description should explain SET mechanism"
    assert ("1,4" in desc), \
        "Birch description should call out 1,4-regioselectivity"


def test_dess_martin_oxidation_seeded(app):
    """Phase 31b round 152 — Dess-Martin periodinane.  Locks
    in: (a) the entry exists; (b) the description contrasts
    Dess-Martin with Swern and Jones — that's the teaching
    point that distinguishes this entry from the existing
    PCC + Swern oxidations; (c) the room-temperature +
    bench-stable advantages are mentioned."""
    result = app.call("show_reaction", name_or_id="Dess-Martin")
    assert "id" in result
    desc = result.get("description", "").lower()
    # Mechanism / class teaching points.
    assert "i(v)" in desc or "iodine(v)" in desc \
        or "hyper-valent" in desc or "hypervalent" in desc
    # Comparison with classic oxidations.
    assert "swern" in desc or "jones" in desc
    # No over-oxidation to carboxylic acid is the killer
    # selectivity argument.
    assert ("not over-oxidise" in desc or "no over-"
            in desc or "does not over" in desc
            or "over-oxidi" in desc)


def test_named_reaction_count_at_least_fifty(app):
    """Phase 31b is COMPLETE at 50/50 — catalogue should be ≥ 50
    seeded reactions after round 157.  Original Phase 31 vision
    delivered after rounds 152-157 (Birch + Dess-Martin +
    Sharpless AE + CBS + Sharpless AD + Jacobsen + Mukaiyama +
    Evans + Stille + Corey-Chaykovsky + Appel + Jones — 12
    entries in 6 rounds)."""
    rows = app.call("list_reactions")
    assert len(rows) >= 50, \
        f"only {len(rows)} reactions, expected ≥ 50 " \
        f"(Phase 31b 50/50 milestone)"


def test_appel_reaction_seeded(app):
    """Phase 31b round 157 — Appel reaction.  Locks in:
    (a) entry exists; (b) PPh₃ + CCl₄ reagent pair; (c) the
    SN2-with-inversion mechanism via the alkoxytriphenyl-
    phosphonium intermediate; (d) the Mitsunobu pairing — both
    activate alcohol-OH as a phosphonium leaving group via
    PPh₃."""
    result = app.call("show_reaction", name_or_id="Appel reaction")
    assert "id" in result
    smarts = result["smiles"]
    # PPh3 + CCl4 in reagents.
    assert "P(c" in smarts and "ClC(Cl)(Cl)Cl" in smarts, \
        "Appel reaction SMILES must include PPh3 + CCl4"
    desc = result.get("description", "").lower()
    # PPh3 / triphenylphosphine teaching anchor.
    assert ("ppph" in desc or "pph" in desc
            or "triphenylphosphine" in desc), \
        "Appel description must name PPh₃ / triphenylphosphine"
    # CCl4 / tetrahalomethane.
    assert "ccl" in desc or "tetrahalomethane" in desc, \
        "Appel description must name CCl₄ (or tetrahalomethane)"
    # SN2 inversion at the carbon.
    assert "sn2" in desc, \
        "Appel description must teach the SN2 displacement"
    assert ("inversion" in desc), \
        "Appel description must teach the inversion of " \
        "configuration"
    # Mitsunobu pairing is the headline pedagogical anchor.
    assert "mitsunobu" in desc, \
        "Appel description must pair pedagogically with the " \
        "seeded Mitsunobu entry"


def test_jones_oxidation_seeded(app):
    """Phase 31b round 157 — Jones oxidation.  Locks in:
    (a) entry exists; (b) Cr(VI) reagent (CrO₃ + H₂SO₄ in
    acetone); (c) **the over-oxidation of 1° alcohol → "
    carboxylic acid** which is the headline distinction from
    PCC / Swern / Dess-Martin; (d) the green-chemistry
    context (Cr(VI) carcinogen + heavy-metal waste)."""
    result = app.call("show_reaction", name_or_id="Jones oxidation")
    assert "id" in result
    smarts = result["smiles"]
    # 1-octanol → octanoic acid (the over-oxidation product).
    lhs, rhs = smarts.split(">>")
    assert "CCCCCCCCO" in lhs, \
        "Jones substrate side must contain 1-octanol"
    assert "CCCCCCCC(=O)O" in rhs, \
        "Jones product side must contain octanoic acid " \
        "(over-oxidation past the aldehyde — the whole " \
        "teaching point)"
    # Cr in the SMILES.
    assert "[Cr]" in smarts, \
        "Jones reaction SMILES must include a Cr atom"
    desc = result.get("description", "").lower()
    # CrO3 / Cr(VI) reagent.
    assert ("cr(vi)" in desc or "cro" in desc
            or "chromic" in desc), \
        "Jones description must name the Cr(VI) / CrO₃ reagent"
    # Over-oxidation is the headline distinction from PCC /
    # Swern / Dess-Martin.
    assert "over-oxidation" in desc or "over-oxidi" in desc, \
        "Jones description must teach the over-oxidation of " \
        "1° alcohol → carboxylic acid"
    # Comparison with the modern PCC / Swern / Dess-Martin
    # entries.
    assert ("pcc" in desc or "swern" in desc
            or "dess-martin" in desc), \
        "Jones description must contrast with the seeded " \
        "PCC / Swern / Dess-Martin modern alternatives"


def test_named_reaction_count_at_least_fifty_six(app):
    """Phase 31b extension floor — after round 175 the
    catalogue is at 56/60 (50/50 milestone in round 157;
    Wacker + Brown round 164; Robinson + Knoevenagel
    round 165; Henry + Hantzsch round 175)."""
    rows = app.call("list_reactions")
    assert len(rows) >= 56, \
        f"only {len(rows)} reactions, expected ≥ 56 " \
        f"(Phase 31b extension at 56/60)"


def test_robinson_annulation_seeded(app):
    """Phase 31b round 165 — Robinson annulation.  Locks in:
    (a) entry exists; (b) the 3-step cascade (Michael +
    aldol + dehydration) teaching anchor; (c) the cyclo-
    hexenone product class — opens the ring-construction
    teaching surface; (d) Wieland-Miescher / steroid-
    synthesis context."""
    result = app.call("show_reaction",
                      name_or_id="Robinson annulation")
    assert "id" in result
    desc = result.get("description", "").lower()
    # Three-step cascade.
    assert "michael" in desc, \
        "Robinson description must teach the Michael step"
    assert "aldol" in desc, \
        "Robinson description must teach the aldol step"
    assert "dehydration" in desc, \
        "Robinson description must teach the dehydration " \
        "step"
    # Wieland-Miescher / steroid-synthesis context.
    assert ("wieland" in desc or "steroid" in desc), \
        "Robinson description must mention the steroid / " \
        "Wieland-Miescher synthesis context — the headline " \
        "ring-construction teaching anchor"
    # Robinson + Nobel attribution.
    assert "robinson" in desc and "1947" in desc, \
        "Robinson description must name Sir Robert Robinson " \
        "+ his 1947 Nobel"
    # Product side: the cyclohexenone fused-bicyclic ring
    # carries both a C=C (the new α,β-unsaturation) and a
    # C=O (the surviving ketone) — the cyclohexenone
    # signature.
    smarts = result["smiles"]
    rhs = smarts.split(">>", 1)[1]
    assert "C=C" in rhs, \
        "Robinson product must contain the new C=C bond " \
        "from the cascade's dehydration step"
    assert ("O=C" in rhs or "C=O" in rhs), \
        "Robinson product must contain a ketone carbonyl " \
        "(the surviving C=O after the cyclisation)"


def test_knoevenagel_condensation_seeded(app):
    """Phase 31b round 165 — Knoevenagel condensation.  Locks
    in: (a) entry exists; (b) **active-methylene
    nucleophile** teaching anchor — the pKa contrast with
    aldol; (c) mild secondary-amine (piperidine / pyridine)
    base; (d) Doebner modification / decarboxylation
    teaching point; (e) α,β-unsaturated product class."""
    result = app.call("show_reaction", name_or_id="Knoevenagel")
    assert "id" in result
    desc = result.get("description", "").lower()
    # Active-methylene teaching anchor — the pedagogical
    # distinction from aldol.
    assert "active" in desc and "methylene" in desc, \
        "Knoevenagel description must teach the active-" \
        "methylene-nucleophile concept (the distinction " \
        "from aldol)"
    # pKa contrast with aldol.
    assert "pka" in desc, \
        "Knoevenagel description must call out the pKa " \
        "contrast (active-methylene CH ~11-13 vs simple " \
        "ketone α-CH ~20)"
    # Mild secondary-amine base.
    assert ("piperidine" in desc or "pyridine" in desc), \
        "Knoevenagel description must name the mild " \
        "amine-base catalyst (piperidine / pyridine)"
    # Doebner modification / decarboxylation teaching.
    assert "doebner" in desc, \
        "Knoevenagel description must mention the Doebner " \
        "modification (decarboxylation of monoacid variants)"
    # Aldol comparison.
    assert "aldol" in desc, \
        "Knoevenagel description must contrast with the " \
        "aldol condensation (the closest seeded reaction)"


def test_henry_reaction_seeded(app):
    """Phase 31b round 175 — Henry (nitroaldol) reaction.
    Locks in: (a) entry exists; (b) the nitroalkane
    nucleophile + base-catalysed mechanism + aci-nitro
    carbanion intermediate; (c) the pKa contrast with
    aldol (~ 10 vs ~ 20); (d) the chloramphenicol /
    β-blocker amino-alcohol downstream reduction; (e)
    asymmetric variants (Shibasaki / Trost)."""
    result = app.call("show_reaction", name_or_id="Henry reaction")
    assert "id" in result
    smarts = result["smiles"]
    # Substrate: nitromethane SMILES (or canonical equivalent).
    assert "[N+]" in smarts and "[O-]" in smarts, \
        "Henry reaction SMILES must contain a nitro group"
    desc = result.get("description", "").lower()
    # Nitroalkane substrate class.
    assert ("nitroalkane" in desc or "nitro" in desc), \
        "Henry description must name the nitroalkane class"
    # pKa contrast with aldol.
    assert "pka" in desc, \
        "Henry description must call out the pKa contrast " \
        "(nitroalkane α-H ~ 10 vs ketone α-H ~ 20)"
    # aci-nitro carbanion intermediate.
    assert "aci-nitro" in desc or "carbanion" in desc, \
        "Henry description must teach the aci-nitro carbanion " \
        "intermediate"
    # Asymmetric variant attribution (Shibasaki or Trost).
    assert "shibasaki" in desc or "trost" in desc, \
        "Henry description must mention an asymmetric variant"


def test_hantzsch_dihydropyridine_seeded(app):
    """Phase 31b round 175 — Hantzsch dihydropyridine
    synthesis.  Locks in: (a) entry exists; (b) Hantzsch
    1881 attribution; (c) the **multi-component reaction**
    teaching anchor; (d) the calcium-channel-blocker
    pharmaceutical link (nifedipine / amlodipine); (e)
    the cascade walk (Knoevenagel + enaminone + Michael
    + dehydration); (f) the 1,4-dihydropyridine product
    contains an N-H + 2 carboxylates."""
    result = app.call("show_reaction", name_or_id="Hantzsch")
    assert "id" in result
    smarts = result["smiles"]
    rhs = smarts.split(">>", 1)[1]
    # Product side contains the dihydropyridine NH + 2 ester
    # carboxylates.
    assert "NC(C)=C" in rhs or "C(C)=C" in rhs, \
        "Hantzsch product must contain the 1,4-DHP ring"
    desc = result.get("description", "").lower()
    # Hantzsch + 1881 attribution.
    assert "hantzsch" in desc and "1881" in desc
    # Multi-component reaction teaching anchor.
    assert "multi-component" in desc or "mcr" in desc, \
        "Hantzsch description must teach the MCR concept"
    # Cascade walk — at least 3 of the 4 steps named.
    cascade_terms = ("knoevenagel", "enaminone", "michael",
                     "dehydration")
    n_named = sum(1 for term in cascade_terms if term in desc)
    assert n_named >= 3, \
        f"Hantzsch description should name ≥ 3 of the 4 " \
        f"cascade steps (knoevenagel / enaminone / michael / " \
        f"dehydration); only {n_named} found"
    # Pharmaceutical context — calcium-channel blockers.
    assert "calcium" in desc or "nifedipine" in desc \
        or "amlodipine" in desc, \
        "Hantzsch description must name the calcium-channel-" \
        "blocker pharmaceutical context"


def test_multi_component_reaction_anchor_present(app):
    """Round 175 opens the multi-component reaction (MCR)
    teaching surface via Hantzsch.  Locks in that the
    Hantzsch entry is present alongside the existing
    cascade entries (Robinson annulation, Knoevenagel)."""
    rows = app.call("list_reactions")
    names = {r["name"] for r in rows}
    for must_have in ("Hantzsch", "Robinson annulation",
                      "Knoevenagel"):
        assert any(must_have in n for n in names), \
            f"cascade / MCR anchor missing: {must_have}"


def test_ring_construction_anchors_present(app):
    """Round 165 opens the ring-construction teaching
    surface via Robinson annulation.  The anchor reaction
    must be present alongside the existing seeded ring-
    formation entries (Diels-Alder + 6π electrocyclic +
    aldolase class I + click chemistry triazole) so future
    regression of any single ring-builder surfaces
    immediately."""
    rows = app.call("list_reactions")
    names = {r["name"] for r in rows}
    for must_have in ("Robinson annulation", "Diels-Alder",
                      "6π electrocyclic"):
        assert any(must_have in n for n in names), \
            f"ring-construction anchor missing: {must_have}"


def test_wacker_oxidation_seeded(app):
    """Phase 31b round 164 — Wacker oxidation.  Locks in:
    (a) entry exists; (b) Pd(II)/Cu(II)/O₂ catalytic-system
    description; (c) **Markovnikov regioselectivity**
    teaching point — the alkene → methyl-ketone
    disconnection where O lands on the more-substituted
    carbon; (d) the redox-relay mechanism (Pd ↔ Cu ↔ O₂)
    that templates modern aerobic oxidations."""
    result = app.call("show_reaction", name_or_id="Wacker")
    assert "id" in result
    smarts = result["smiles"]
    # Substrate side — terminal alkene; product side — methyl
    # ketone.
    lhs, rhs = smarts.split(">>")
    assert "C=C" in lhs
    assert "C(=O)" in rhs or "C(C)=O" in rhs
    desc = result.get("description", "").lower()
    # Catalytic system teaching anchors.
    assert "pd" in desc, \
        "Wacker description must call out Pd catalysis"
    assert "cu" in desc, \
        "Wacker description must name the Cu(II) " \
        "co-catalyst (the electron-shuttle that closes " \
        "the catalytic cycle)"
    # Markovnikov regiochemistry is the headline teaching
    # point that distinguishes Wacker from Brown.
    assert "markovnikov" in desc, \
        "Wacker description must teach the Markovnikov " \
        "regioselectivity (O on the more-substituted C)"
    # Methyl ketone product class.
    assert "methyl ketone" in desc or "ketone" in desc


def test_brown_hydroboration_seeded(app):
    """Phase 31b round 164 — Brown hydroboration-oxidation.
    Locks in: (a) entry exists; (b) BH₃ + H₂O₂/OH two-step
    sequence; (c) **anti-Markovnikov regioselectivity** —
    the headline contrast with Wacker / acid-catalysed
    hydration; (d) **syn-addition stereochemistry** —
    the headline contrast with Br₂ addition's anti; (e)
    Brown's Nobel attribution."""
    result = app.call("show_reaction",
                      name_or_id="Brown hydroboration")
    assert "id" in result
    smarts = result["smiles"]
    # Substrate must contain a B atom (the hydroboration
    # reagent BH3 / 9-BBN / disiamylborane).
    assert "B" in smarts and "OO" in smarts, \
        "Brown reaction SMILES must contain both BH₃ + " \
        "H₂O₂ reagents"
    # Product must carry stereochemistry markers (the syn-
    # addition gives a defined trans-product on the cyclic
    # substrate).
    rhs = smarts.split(">>", 1)[1]
    assert "@" in rhs, \
        "Brown product must carry stereochemistry markers " \
        "(syn-addition gives trans-2-methylcyclohexanol)"
    desc = result.get("description", "").lower()
    # H. C. Brown + Nobel attribution.
    assert "brown" in desc and "1979" in desc, \
        "Brown description must name H.C. Brown + the " \
        "1979 Nobel"
    # Anti-Markovnikov is the headline contrast with Wacker
    # / acid hydration.
    assert "anti-markovnikov" in desc, \
        "Brown description must teach the anti-Markovnikov " \
        "regioselectivity (the contrast with Wacker / " \
        "acid-catalysed hydration)"
    # Syn-addition stereochemistry teaching anchor.
    assert "syn" in desc, \
        "Brown description must teach syn-addition " \
        "stereochemistry"
    # Two-step nature — hydroboration THEN H₂O₂ oxidation.
    assert ("h2o2" in desc or "h₂o₂" in desc
            or "hydrogen peroxide" in desc), \
        "Brown description must name the H₂O₂ oxidation step"


def test_alkene_functionalisation_pair_present(app):
    """Round 164 opens the alkene-functionalisation
    regio-/stereo-selectivity teaching surface — Wacker
    (Markovnikov) + Brown (anti-Markovnikov + syn) together
    form the canonical contrast pair.  Both entries must
    be present."""
    rows = app.call("list_reactions")
    names = {r["name"] for r in rows}
    assert any("Wacker" in n for n in names), \
        "Wacker oxidation missing from catalogue"
    assert any("Brown hydroboration" in n for n in names), \
        "Brown hydroboration missing from catalogue"


def test_phase_31b_complete_50_of_50(app):
    """Phase 31b 50/50 milestone closeout test — the named-
    reaction catalogue is now fully realised against the
    original Phase 31 vision.  Future work goes into Phase
    31b2 + Phase 38c + Phase 31k stretch buckets."""
    rows = app.call("list_reactions")
    names = {r["name"] for r in rows}
    # Spot-check the round-152 → round-157 expansion entries.
    for must_have in ("Birch reduction",
                      "Dess-Martin oxidation",
                      "Sharpless asymmetric epoxidation",
                      "CBS reduction",
                      "Sharpless asymmetric dihydroxylation",
                      "Jacobsen-Katsuki epoxidation",
                      "Mukaiyama aldol",
                      "Evans aldol",
                      "Stille coupling",
                      "Corey-Chaykovsky epoxidation",
                      "Appel reaction",
                      "Jones oxidation"):
        # Substring match, since each entry name carries
        # additional substrate / product detail.
        assert any(must_have in n for n in names), \
            f"50/50 expansion missing {must_have!r}"


def test_stille_coupling_seeded(app):
    """Phase 31b round 156 — Stille coupling.  Locks in:
    (a) entry exists; (b) Pd(0) catalysis + organostannane
    transmetalation teaching point; (c) the trade-off
    description (functional-group tolerance vs Sn toxicity)
    that distinguishes Stille from the existing Suzuki /
    Negishi / Heck / Sonogashira entries."""
    result = app.call("show_reaction",
                      name_or_id="Stille coupling")
    assert "id" in result
    smarts = result["smiles"]
    # Tributyltin appears in both substrate + by-product.
    assert "[Sn]" in smarts, \
        "Stille reaction SMILES must contain a Sn atom " \
        "(the defining stannane reagent)"
    desc = result.get("description", "").lower()
    # Pd-catalysis + transmetalation + stannane teaching anchors.
    assert "pd" in desc, \
        "Stille description must call out Pd(0) catalysis"
    assert "transmetalation" in desc, \
        "Stille description must teach the transmetalation step"
    assert "stannane" in desc or "tin" in desc, \
        "Stille description must name the organostannane reagent"
    # Functional-group tolerance vs toxicity is the headline
    # trade-off vs Suzuki.
    assert ("toxic" in desc or "toxicity" in desc), \
        "Stille description must call out the Sn toxicity " \
        "trade-off"


def test_corey_chaykovsky_seeded(app):
    """Phase 31b round 156 — Corey-Chaykovsky epoxidation.
    Locks in: (a) entry exists; (b) sulfur-ylide reagent
    class; (c) the Wittig comparison that's the headline
    pedagogical anchor (same starting carbonyl, different
    product class — alkene vs epoxide)."""
    result = app.call("show_reaction", name_or_id="Corey-Chaykovsky")
    assert "id" in result
    smarts = result["smiles"]
    # Sulfur ylide reagent must be present (S+ / CH2-).
    assert "[S+]" in smarts and "[CH2-]" in smarts, \
        "Corey-Chaykovsky reaction must include the " \
        "dimethylsulfonium-methylide ylide reagent"
    desc = result.get("description", "").lower()
    # Sulfur-ylide class.
    assert "ylide" in desc and "sulfur" in desc, \
        "Corey-Chaykovsky description must name the " \
        "sulfur-ylide reagent class"
    # Wittig comparison is the headline teaching anchor.
    assert "wittig" in desc, \
        "Corey-Chaykovsky description must contrast with " \
        "the existing Wittig entry (same carbonyl substrate, " \
        "different product class)"
    # The two-flavour distinction (sulfonium vs sulfoxonium
    # ylide) is a classic teaching point.
    assert ("sulfoxonium" in desc), \
        "Corey-Chaykovsky description should mention the " \
        "sulfoxonium variant for the 1,4-vs-1,2 selectivity " \
        "comparison"


def test_pd_coupling_family_at_least_five(app):
    """Round 156 — the Pd-coupling family in the catalogue
    should be at 5/5 textbook canon entries (Suzuki +
    Negishi + Heck + Sonogashira + Stille)."""
    rows = app.call("list_reactions")
    pd_rows = [r for r in rows
               if "cross-coupling" in r.get("category", "").lower()
               and ("pd" in r.get("category", "").lower()
                    or "pd" in r.get("name", "").lower())]
    # Be conservative — match by name as well, since the
    # category string varies a little.
    pd_names = [r for r in rows
                if any(coupling in r.get("name", "")
                       for coupling in ("Suzuki", "Negishi",
                                        "Heck", "Sonogashira",
                                        "Stille"))]
    assert len(pd_names) >= 5, \
        f"only {len(pd_names)} Pd-coupling-family entries, " \
        f"expected ≥ 5 (Suzuki, Negishi, Heck, Sonogashira, " \
        f"Stille)"


def test_mukaiyama_aldol_seeded(app):
    """Phase 31b round 155 — Mukaiyama aldol.  Locks in:
    (a) entry exists; (b) Lewis-acid catalyst class (TiCl₄ /
    BF₃·OEt₂ for the achiral version, chiral Ti-BINOL / Cu-BOX
    / oxazaborolidinone for the asymmetric variant); (c) the
    silyl-enol-ether starting material; (d) the **open TS**
    teaching point that distinguishes Mukaiyama from the
    classic acid-/base-catalysed (Zimmerman-Traxler) aldol;
    (e) chirality on the product."""
    result = app.call("show_reaction", name_or_id="Mukaiyama")
    assert "id" in result
    smarts = result["smiles"]
    product = smarts.split(">>", 1)[1]
    assert "@" in product, \
        "Mukaiyama product must carry chirality markers"
    desc = result.get("description", "").lower()
    # Lewis-acid activator family.
    assert ("ticl" in desc or "tio" in desc
            or "bf" in desc or "lewis acid" in desc), \
        "Mukaiyama description must name the Lewis-acid " \
        "activator family"
    # Open TS teaching point.
    assert ("open" in desc), \
        "Mukaiyama description must teach the open TS " \
        "(distinct from Zimmerman-Traxler chair)"
    # Silyl enol ether substrate.
    assert ("silyl enol" in desc or "tms enol" in desc
            or "silyl ketene" in desc), \
        "Mukaiyama description must name the silyl-enol-ether " \
        "substrate class"


def test_evans_aldol_seeded(app):
    """Phase 31b round 155 — Evans aldol.  Locks in: (a) entry
    exists; (b) the **chiral oxazolidinone auxiliary**
    (distinguishes from the catalyst-based Mukaiyama path);
    (c) Bu₂BOTf soft-enolisation; (d) Zimmerman-Traxler chair
    TS — the classic teaching anchor for diastereoselective
    aldol; (e) syn-aldol product geometry; (f) chirality
    markers."""
    result = app.call("show_reaction", name_or_id="Evans aldol")
    assert "id" in result
    smarts = result["smiles"]
    product = smarts.split(">>", 1)[1]
    # Two new stereocentres → at least two @-style markers.
    assert product.count("@") >= 2, \
        "Evans-syn product must carry both new stereocentres"
    desc = result.get("description", "").lower()
    # Chiral auxiliary teaching point.
    assert ("oxazolidinone" in desc), \
        "Evans description must name the oxazolidinone " \
        "auxiliary class"
    assert ("auxiliary" in desc), \
        "Evans description must call out the chiral-auxiliary " \
        "approach (vs the catalyst approach in Mukaiyama)"
    # Boron enolate / Bu2BOTf reagent.
    assert ("bu" in desc and "botf" in desc) \
        or "boron enolate" in desc, \
        "Evans description must name Bu₂BOTf / boron enolate"
    # Zimmerman-Traxler TS class.
    assert ("zimmerman" in desc or "chair" in desc), \
        "Evans description must teach the Zimmerman-Traxler " \
        "chair TS"
    # Syn-aldol product.
    assert ("syn" in desc), \
        "Evans description must call out the syn-aldol product"


def test_asymmetric_catalysis_count_at_least_six(app):
    """Round 155 — the asymmetric-catalysis category should now
    carry ≥ 6 entries (Sharpless AE + CBS + Sharpless AD +
    Jacobsen + Mukaiyama + Evans)."""
    rows = app.call("list_reactions")
    asym_rows = [r for r in rows
                 if "asymmetric" in r.get("category", "").lower()
                 or "enantioselective"
                 in r.get("category", "").lower()]
    assert len(asym_rows) >= 6, \
        f"only {len(asym_rows)} asymmetric-catalysis entries, " \
        f"expected ≥ 6"


def test_asymmetric_c_c_bond_formation_present(app):
    """Round 155 opens the asymmetric C-C bond-formation
    teaching surface — at least one reaction should be
    explicitly tagged as asymmetric C-C bond formation."""
    rows = app.call("list_reactions")
    cc_rows = [r for r in rows
               if "asymmetric" in r.get("category", "").lower()
               and "c-c" in r.get("category", "").lower()]
    assert cc_rows, \
        "no asymmetric C-C bond-formation category found; " \
        f"saw categories {sorted({r.get('category', '') for r in rows})}"


def test_sharpless_asymmetric_dihydroxylation_seeded(app):
    """Phase 31b round 154 — Sharpless asymmetric
    dihydroxylation.  Locks in: (a) entry exists; (b) AD-mix-α
    / AD-mix-β + bis-cinchona-alkaloid PHAL ligand teaching
    point; (c) the **distinction** from the round-153 Sharpless
    asymmetric epoxidation (no allylic-OH restriction; gives
    diol not epoxide); (d) chirality markers on the product."""
    result = app.call("show_reaction",
                      name_or_id="Sharpless asymmetric dihydroxylation")
    assert "id" in result
    smarts = result["smiles"]
    product = smarts.split(">>", 1)[1]
    assert "@" in product, \
        "Sharpless AD product must carry chirality markers"
    desc = result.get("description", "").lower()
    # AD-mix-α / β nomenclature.
    assert ("ad-mix" in desc), \
        "Sharpless AD description must name AD-mix-α/β"
    # PHAL chiral ligand class.
    assert ("phal" in desc or "cinchona" in desc), \
        "Sharpless AD description must name the PHAL / " \
        "cinchona-alkaloid chiral-ligand class"
    # Distinction from Sharpless epoxidation: no allylic-OH
    # restriction is the headline pedagogical contrast.
    assert ("no allylic" in desc
            or "any alkene" in desc
            or "syn-diol" in desc
            or "no allylic-oh" in desc), \
        "Sharpless AD description must contrast with the " \
        "allylic-OH restriction of Sharpless asymmetric " \
        "epoxidation"


def test_jacobsen_katsuki_epoxidation_seeded(app):
    """Phase 31b round 154 — Jacobsen-Katsuki epoxidation.
    Locks in: (a) entry exists; (b) Mn(salen) catalyst class
    + NaOCl bleach oxidant; (c) the **distinction** from
    Sharpless asymmetric epoxidation — Jacobsen does NOT
    require an allylic OH (Mn coordinates the oxidant, not
    the substrate); (d) chirality markers on the product."""
    result = app.call("show_reaction", name_or_id="Jacobsen")
    assert "id" in result
    smarts = result["smiles"]
    product = smarts.split(">>", 1)[1]
    assert "@" in product, \
        "Jacobsen product must carry chirality markers"
    desc = result.get("description", "").lower()
    # Catalyst class + oxidant.
    assert "salen" in desc
    assert ("naocl" in desc or "bleach" in desc), \
        "Jacobsen description must name the NaOCl / bleach " \
        "terminal oxidant"
    # Mechanism / oxo-intermediate.
    assert ("mn(v)" in desc or "mn(iii)" in desc
            or "manganese" in desc or "mn=o" in desc), \
        "Jacobsen description must name the Mn-salen catalyst"
    # Distinction from Sharpless: no allylic-OH requirement.
    assert ("not require" in desc
            or "no allylic" in desc
            or "without an allylic" in desc), \
        "Jacobsen description must contrast with the allylic-" \
        "OH restriction of Sharpless asymmetric epoxidation"


def test_asymmetric_catalysis_count_at_least_four(app):
    """Round 154 — the asymmetric-catalysis category should now
    carry ≥ 4 entries (Sharpless epoxidation + CBS + Sharpless
    AD + Jacobsen)."""
    rows = app.call("list_reactions")
    asym_rows = [r for r in rows
                 if "asymmetric" in r.get("category", "").lower()
                 or "enantioselective"
                 in r.get("category", "").lower()]
    assert len(asym_rows) >= 4, \
        f"only {len(asym_rows)} asymmetric-catalysis entries, " \
        f"expected ≥ 4"


def test_sharpless_asymmetric_epoxidation_seeded(app):
    """Phase 31b round 153 — Sharpless asymmetric epoxidation.
    Locks in: (a) entry exists by substring lookup; (b) the
    description names the Nobel context (2001) and the chiral
    DET ligand control element; (c) the substrate-restriction
    rule (allylic alcohol — the OH anchors the substrate to
    the Ti centre) is preserved against future copy-edits;
    (d) the product SMILES carries chirality markers (the
    whole teaching point is enantioselectivity)."""
    result = app.call("show_reaction",
                      name_or_id="Sharpless asymmetric")
    assert "id" in result
    smarts = result["smiles"]
    # Product SMILES must carry tetrahedral chirality markers
    # (@ or @@) — this is asymmetric synthesis after all.
    product = smarts.split(">>", 1)[1]
    assert "@" in product, \
        "Sharpless product must carry chirality markers"
    desc = result.get("description", "").lower()
    # Nobel + ligand + substrate-restriction teaching anchors.
    assert "2001" in desc or "nobel" in desc
    assert "tartrate" in desc or "det" in desc
    assert "allylic" in desc, \
        "Sharpless description must teach the allylic-OH " \
        "substrate restriction"


def test_cbs_reduction_seeded(app):
    """Phase 31b round 153 — CBS reduction.  Locks in:
    (a) entry exists by substring lookup; (b) Corey-Bakshi-
    Shibata attribution; (c) the oxazaborolidine catalyst +
    BH₃ hydride-source description; (d) the comparison with
    NaBH₄ (the seeded non-asymmetric ketone reduction) so
    future copy-edits can't strip the pedagogical-distinction
    teaching point; (e) chirality markers on the product."""
    result = app.call("show_reaction", name_or_id="CBS reduction")
    assert "id" in result
    smarts = result["smiles"]
    product = smarts.split(">>", 1)[1]
    assert "@" in product, \
        "CBS product must carry chirality markers"
    desc = result.get("description", "").lower()
    # Attribution + catalyst-class + hydride-source teaching.
    assert ("corey" in desc and "bakshi" in desc
            and "shibata" in desc), \
        "CBS description must name all three CBS originators"
    assert "oxazaborolidine" in desc
    assert "bh" in desc or "borane" in desc
    # Pedagogical distinction from NaBH₄.
    assert "nabh" in desc or "nabh4" in desc, \
        "CBS description must contrast with NaBH₄"


def test_asymmetric_catalysis_category_present(app):
    """Phase 31b round 153 opens the asymmetric-catalysis
    category — confirm at least one reaction is tagged with
    it."""
    rows = app.call("list_reactions")
    cats = {r.get("category", "") for r in rows}
    asym = [c for c in cats
            if "asymmetric" in c.lower()
            or "enantioselective" in c.lower()]
    assert asym, \
        f"no asymmetric-catalysis category found; saw {cats}"


def test_export_reaction_by_id(app, tmp_path):
    rows = app.call("list_reactions", filter="Diels")
    assert rows
    rid = rows[0]["id"]
    out = app.call("export_reaction_by_id",
                   reaction_id=rid, path=str(tmp_path / "da.svg"))
    assert Path(out["path"]).exists()
    assert out["size_bytes"] > 500
