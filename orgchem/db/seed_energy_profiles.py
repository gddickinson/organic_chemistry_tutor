"""Seed textbook reaction-coordinate energy profiles — Phase 13b.

Numbers are *pedagogical estimates* in kJ/mol. They reproduce the
qualitative shape of each profile (barrier heights, intermediate-well
depth, net ΔH sign) drawn from canonical textbook sources
(Clayden 2nd ed., Carey & Sundberg 5th ed.). They are **not** intended
for kinetic prediction — a real study needs DFT, not a teaching figure.

Profiles are stored in ``Reaction.energy_profile_json`` with a
``seed_version`` stamp so upgrades roll out without a DB migration.
"""
from __future__ import annotations
import json
import logging
from typing import Callable, Dict

from sqlalchemy import select

from orgchem.core.energy_profile import ReactionEnergyProfile, StationaryPoint
from orgchem.db.models import Reaction as DBRxn
from orgchem.db.session import session_scope

log = logging.getLogger(__name__)


#: Bump whenever seed data changes. Existing rows with a lower embedded
#: ``seed_version`` are overwritten on next app launch.
SEED_VERSION = 3


# ------------------------------------------------------------------
# Profile definitions — keyed by substring match against reaction name.

def _sn2_profile() -> ReactionEnergyProfile:
    """SN2 methyl bromide + hydroxide: single concerted barrier."""
    return ReactionEnergyProfile(
        title="SN2: hydroxide + methyl bromide",
        energy_unit="kJ/mol",
        source="pedagogical estimate (Clayden 2e §15)",
        points=[
            StationaryPoint(label="Reactants", energy=0.0,
                            note="CH₃Br + OH⁻"),
            StationaryPoint(label="TS", energy=95.0, is_ts=True,
                            note="pentacoordinate C"),
            StationaryPoint(label="Products", energy=-65.0,
                            note="CH₃OH + Br⁻"),
        ],
    )


def _sn1_profile() -> ReactionEnergyProfile:
    """SN1 tert-butyl bromide in water: two barriers with a carbocation well."""
    return ReactionEnergyProfile(
        title="SN1: tert-butyl bromide in water",
        energy_unit="kJ/mol",
        source="pedagogical estimate (Clayden 2e §15)",
        points=[
            StationaryPoint(label="Reactants", energy=0.0,
                            note="t-BuBr + H₂O"),
            StationaryPoint(label="TS ionisation", energy=105.0, is_ts=True,
                            note="rate-limiting"),
            StationaryPoint(label="Carbocation", energy=70.0,
                            note="t-Bu⁺ + Br⁻"),
            StationaryPoint(label="TS capture", energy=85.0, is_ts=True),
            StationaryPoint(label="Products", energy=-20.0,
                            note="t-BuOH + HBr"),
        ],
    )


def _e1_profile() -> ReactionEnergyProfile:
    """E1 from tert-butyl bromide: ionisation then rapid deprotonation."""
    return ReactionEnergyProfile(
        title="E1: tert-butyl bromide",
        energy_unit="kJ/mol",
        source="pedagogical estimate (Carey-Sundberg 5e §5)",
        points=[
            StationaryPoint(label="Reactants", energy=0.0,
                            note="t-BuBr"),
            StationaryPoint(label="TS ionisation", energy=105.0, is_ts=True,
                            note="rate-limiting"),
            StationaryPoint(label="Carbocation", energy=70.0,
                            note="t-Bu⁺ + Br⁻"),
            StationaryPoint(label="TS deprotonation", energy=80.0, is_ts=True),
            StationaryPoint(label="Products", energy=-10.0,
                            note="isobutylene + HBr"),
        ],
    )


def _diels_alder_profile() -> ReactionEnergyProfile:
    """Concerted Diels-Alder: single aromatic-TS barrier, strongly exothermic."""
    return ReactionEnergyProfile(
        title="Diels-Alder: butadiene + ethylene",
        energy_unit="kJ/mol",
        source="pedagogical estimate (Clayden 2e §35)",
        points=[
            StationaryPoint(label="Reactants", energy=0.0,
                            note="butadiene + ethylene"),
            StationaryPoint(label="TS", energy=115.0, is_ts=True,
                            note="concerted, aromatic-like"),
            StationaryPoint(label="Products", energy=-165.0,
                            note="cyclohexene"),
        ],
    )


def _e2_profile() -> ReactionEnergyProfile:
    """E2 elimination: concerted, single TS, mildly exothermic."""
    return ReactionEnergyProfile(
        title="E2: base + 2-bromobutane",
        energy_unit="kJ/mol",
        source="pedagogical estimate (Clayden 2e §17)",
        points=[
            StationaryPoint(label="Reactants", energy=0.0,
                            note="2-BrBu + EtO⁻"),
            StationaryPoint(label="TS", energy=80.0, is_ts=True,
                            note="anti-periplanar H–C–C–Br"),
            StationaryPoint(label="Products", energy=-35.0,
                            note="2-butene + EtOH + Br⁻"),
        ],
    )


def _aldol_profile() -> ReactionEnergyProfile:
    """Base-catalysed aldol addition: fast enolate formation + slow addition."""
    return ReactionEnergyProfile(
        title="Aldol addition: acetaldehyde (base-catalysed)",
        energy_unit="kJ/mol",
        source="pedagogical estimate (Clayden 2e §26)",
        points=[
            StationaryPoint(label="Reactants", energy=0.0,
                            note="aldehyde + base"),
            StationaryPoint(label="TS enolisation", energy=65.0, is_ts=True,
                            note="α-proton removal"),
            StationaryPoint(label="Enolate", energy=35.0,
                            note="resonance-stabilised"),
            StationaryPoint(label="TS addition", energy=75.0, is_ts=True,
                            note="rate-limiting C–C bond forming"),
            StationaryPoint(label="Alkoxide", energy=5.0,
                            note="β-alkoxy aldehyde"),
            StationaryPoint(label="Products", energy=-10.0,
                            note="β-hydroxy aldehyde + base"),
        ],
    )


def _grignard_profile() -> ReactionEnergyProfile:
    """Grignard addition: strongly exothermic, irreversible, one TS + workup."""
    return ReactionEnergyProfile(
        title="Grignard addition: MeMgBr + acetaldehyde",
        energy_unit="kJ/mol",
        source="pedagogical estimate (Clayden 2e §9)",
        points=[
            StationaryPoint(label="Reactants", energy=0.0,
                            note="RMgX + R'CHO"),
            StationaryPoint(label="TS addition", energy=40.0, is_ts=True,
                            note="Mg coordinates O; C–C forms"),
            StationaryPoint(label="Alkoxide", energy=-85.0,
                            note="magnesium alkoxide"),
            StationaryPoint(label="TS protonation", energy=-60.0, is_ts=True,
                            note="aqueous workup"),
            StationaryPoint(label="Products", energy=-140.0,
                            note="2° alcohol"),
        ],
    )


def _wittig_profile() -> ReactionEnergyProfile:
    """Wittig olefination: via betaine + oxaphosphetane intermediates."""
    return ReactionEnergyProfile(
        title="Wittig: ylide + acetaldehyde",
        energy_unit="kJ/mol",
        source="pedagogical estimate (Clayden 2e §14)",
        points=[
            StationaryPoint(label="Reactants", energy=0.0,
                            note="Ph₃P=CHR + R'CHO"),
            StationaryPoint(label="TS 1", energy=55.0, is_ts=True,
                            note="C–C forming"),
            StationaryPoint(label="Oxaphosphetane", energy=-20.0,
                            note="4-membered ring intermediate"),
            StationaryPoint(label="TS 2", energy=10.0, is_ts=True,
                            note="fragmentation, C=O forming"),
            StationaryPoint(label="Products", energy=-120.0,
                            note="alkene + Ph₃P=O"),
        ],
    )


def _michael_profile() -> ReactionEnergyProfile:
    """Michael addition: single concerted TS from stabilised carbanion + enone."""
    return ReactionEnergyProfile(
        title="Michael addition: enolate + α,β-unsaturated ketone",
        energy_unit="kJ/mol",
        source="pedagogical estimate (Carey-Sundberg 5e §10)",
        points=[
            StationaryPoint(label="Reactants", energy=0.0,
                            note="stabilised Nu⁻ + enone"),
            StationaryPoint(label="TS", energy=55.0, is_ts=True,
                            note="1,4-addition to β-C"),
            StationaryPoint(label="Enolate", energy=-15.0,
                            note="resonance-stabilised"),
            StationaryPoint(label="Products", energy=-50.0,
                            note="1,5-dicarbonyl"),
        ],
    )


# ---- Phase 31e content expansion (2026-04-23) -----------------------

def _sonogashira_profile() -> ReactionEnergyProfile:
    """Sonogashira catalytic cycle: OA of ArI (RDS) → Cu-acetylide
    transmetalation → reductive elimination. Energies are qualitative
    estimates in the palladium-catalysed regime."""
    return ReactionEnergyProfile(
        title="Sonogashira coupling: Pd(0) / CuI dual catalysis",
        energy_unit="kJ/mol",
        source="pedagogical estimate (Hartwig OTM §18)",
        points=[
            StationaryPoint(label="Ar-I + Pd(0)", energy=0.0,
                            note="plus Cu-acetylide (formed on Cu cycle)"),
            StationaryPoint(label="TS OA", energy=85.0, is_ts=True,
                            note="rate-determining oxidative addition"),
            StationaryPoint(label="Ar-Pd-I", energy=-10.0,
                            note="Pd(II) intermediate"),
            StationaryPoint(label="TS transmetalation", energy=40.0,
                            is_ts=True,
                            note="Cu-C ↔ Pd-C swap"),
            StationaryPoint(label="Ar-Pd-C≡C-Ar'", energy=-35.0,
                            note="diaryl Pd(II) complex"),
            StationaryPoint(label="TS red. elim.", energy=15.0,
                            is_ts=True,
                            note="C(sp²)–C(sp) bond forms"),
            StationaryPoint(label="Ar-C≡C-Ar' + Pd(0)", energy=-130.0,
                            note="product + regenerated catalyst"),
        ],
    )


def _hwe_profile() -> ReactionEnergyProfile:
    """Horner-Wadsworth-Emmons: stabilised carbanion + aldehyde → E-alkene.
    Oxaphosphetane collapse via retro-[2+2] is the selectivity-setting step."""
    return ReactionEnergyProfile(
        title="Horner-Wadsworth-Emmons: β-ketoester phosphonate + aldehyde",
        energy_unit="kJ/mol",
        source="pedagogical estimate (Clayden 2e §27)",
        points=[
            StationaryPoint(label="Reactants + base", energy=0.0,
                            note="phosphonate, aldehyde, NaH"),
            StationaryPoint(label="Phosphonate carbanion", energy=-25.0,
                            note="resonance-stabilised"),
            StationaryPoint(label="TS C-C bond", energy=30.0, is_ts=True,
                            note="carbanion attacks C=O"),
            StationaryPoint(label="Betaine / oxaphosphetane",
                            energy=-15.0,
                            note="4-membered P–C–C–O ring"),
            StationaryPoint(label="TS retro-[2+2]", energy=10.0,
                            is_ts=True,
                            note="E-selective fragmentation"),
            StationaryPoint(label="E-alkene + phosphate", energy=-120.0,
                            note="thermodynamic sink (P=O strength)"),
        ],
    )


def _mitsunobu_profile() -> ReactionEnergyProfile:
    """Mitsunobu reaction: PPh₃ + DIAD activates the alcohol; SN2 on
    oxyphosphonium inverts configuration. Driving force is P=O
    formation (≈ 580 kJ/mol bond-strength bonus)."""
    return ReactionEnergyProfile(
        title="Mitsunobu: PPh₃ / DIAD esterification with inversion",
        energy_unit="kJ/mol",
        source="pedagogical estimate (Clayden 2e §17)",
        points=[
            StationaryPoint(label="ROH + PPh₃ + DIAD",
                            energy=0.0,
                            note="plus acidic pronucleophile"),
            StationaryPoint(label="Betaine (PPh₃-DIAD adduct)",
                            energy=-15.0,
                            note="hydrazide dianion + P(V) cation"),
            StationaryPoint(label="Alkoxyphosphonium RO-PPh₃⁺",
                            energy=-30.0,
                            note="alcohol activated; Nu⁻ now free"),
            StationaryPoint(label="TS SN2 inversion", energy=55.0,
                            is_ts=True,
                            note="backside attack displaces O-PPh₃"),
            StationaryPoint(label="Products: R′-Nu + O=PPh₃",
                            energy=-115.0,
                            note="inverted at C; driven by P=O"),
        ],
    )


_PROFILE_MAP: Dict[str, Callable[[], ReactionEnergyProfile]] = {
    "SN2: methyl bromide":  _sn2_profile,
    "SN1: tert-butyl":      _sn1_profile,
    "E1: tert-butyl":       _e1_profile,
    "E2: 2-bromobutane":    _e2_profile,
    "Diels-Alder":          _diels_alder_profile,
    "Aldol condensation":   _aldol_profile,
    "Grignard addition":    _grignard_profile,
    "Wittig reaction":      _wittig_profile,
    "Michael addition":     _michael_profile,
    "Sonogashira coupling": _sonogashira_profile,
    "Horner-Wadsworth":     _hwe_profile,
    "Mitsunobu":            _mitsunobu_profile,
}


def seed_energy_profiles_if_empty(force: bool = False) -> int:
    """Attach energy-profile JSON to reactions with a matching name substring.

    Idempotent: rows whose stored JSON has a ``seed_version`` at least as new
    as :data:`SEED_VERSION` are left alone. Pass ``force=True`` to rewrite
    unconditionally.
    """
    updated = 0
    with session_scope() as s:
        for name_substr, builder in _PROFILE_MAP.items():
            stmt = select(DBRxn).where(DBRxn.name.like(f"%{name_substr}%"))
            for row in s.scalars(stmt):
                if row.energy_profile_json and not force:
                    try:
                        existing = json.loads(row.energy_profile_json)
                    except Exception:
                        existing = {}
                    if existing.get("seed_version", 0) >= SEED_VERSION:
                        continue
                prof = builder()
                prof.reaction_id = row.id
                payload = prof.to_dict()
                payload["seed_version"] = SEED_VERSION
                row.energy_profile_json = json.dumps(payload, indent=2)
                updated += 1
    log.info("Seeded %d energy profiles (version %d)", updated, SEED_VERSION)
    return updated
