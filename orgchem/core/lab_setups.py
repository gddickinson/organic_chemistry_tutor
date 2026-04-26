"""Phase 38b (round 141) — canonical lab-setup catalogue.

Headless reference data for the *Tools → Lab setups…* dialog
and the future Phase-38c canvas.  Each :class:`Setup` is a
named apparatus configuration — an ordered list of
:mod:`orgchem.core.lab_equipment` items plus the connections
between specific ports on those items.

The :class:`SetupConnection` records reference equipment by
**index into the setup's equipment list** (not by id) so the
same piece can appear twice in one setup — e.g. two RBFs in a
distillation (the boiling pot + the receiver).

Connection validation
---------------------
:func:`validate_setup` walks every `SetupConnection`, looks up
the named ports on the referenced equipment via the Phase-38a
catalogue, and returns a list of error strings (empty when the
setup is valid).  Validation rules:

- Equipment indices must be in range.
- Both port names must exist on their respective equipment.
- Ground-glass joints must match by joint type
  (``"24/29"`` ↔ ``"24/29"``).
- Hose / socket / open ports must connect to the same kind
  (no joint-size strictness).
- A male port on one side must match a female port on the
  other (hose-hose is allowed since rubber tubing is
  symmetric).
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from orgchem.core.lab_equipment import (
    Equipment, get_equipment,
)


@dataclass(frozen=True)
class SetupConnection:
    """A single connection between two pieces in a setup.
    Equipment refs are indices into :attr:`Setup.equipment`."""
    from_equipment_idx: int
    from_port: str
    to_equipment_idx: int
    to_port: str
    note: str = ""           # optional human-friendly description


@dataclass(frozen=True)
class Setup:
    id: str
    name: str
    purpose: str             # what is this setup FOR
    equipment: Tuple[str, ...]   # ids from core/lab_equipment.py
    connections: Tuple[SetupConnection, ...] = field(
        default_factory=tuple)
    procedure: str = ""
    safety_notes: str = ""
    pedagogical_notes: str = ""   # what students learn
    typical_reactions: str = ""   # comma-list of reaction names
    icon_id: str = ""


VALID_CATEGORIES: tuple = (
    "distillation", "reflux", "extraction",
    "filtration", "purification",
)


# ------------------------------------------------------------------
# Connection validation
# ------------------------------------------------------------------

#: Joint families that require strict equality (e.g. 24/29
#: connects only to 24/29).  Unknown / equipment-specific
#: joint tags fall through to a relaxed string-equality check.
_STRICT_JOINT_FAMILIES = frozenset({
    "14/20", "19/22", "24/29", "29/32",
})

#: Joint families that don't enforce male/female complementarity
#: (rubber tubing is symmetric, open ports accept anything).
_SEX_NEUTRAL_JOINTS = frozenset({
    "hose", "open", "socket",
})


def validate_port_pair(equipment_a: Equipment, port_a_name: str,
                       equipment_b: Equipment, port_b_name: str,
                       ) -> Optional[str]:
    """Phase 38c.4 (round 189) — validate a single connection
    between two equipment items at the named ports.

    Returns ``None`` when the pair is compatible (joint types
    match or one side is ``open``; sex-complementary for ground-
    glass joints), or a short human-readable error string
    otherwise.

    Same compatibility rules as :func:`validate_setup`, but
    callable on the per-pair level so the Phase-38c canvas can
    snap two glyphs together (or shout a port-mismatch warning)
    in real time.  Note: this validator does NOT enforce a
    self-loop check on the equipment object, because two
    different placed glyphs in the canvas legitimately share the
    same `Equipment` instance (frozen catalogue dataclass).
    The canvas enforces "don't connect a glyph to itself" at the
    glyph level."""
    port_a = _find_port(equipment_a, port_a_name)
    if port_a is None:
        return (f"port {port_a_name!r} not on "
                f"{equipment_a.id}")
    port_b = _find_port(equipment_b, port_b_name)
    if port_b is None:
        return (f"port {port_b_name!r} not on "
                f"{equipment_b.id}")
    f_type = port_a.joint_type
    t_type = port_b.joint_type
    if (f_type != "open" and t_type != "open"
            and f_type != t_type):
        return f"joint mismatch: {f_type} vs {t_type}"
    if (f_type not in _SEX_NEUTRAL_JOINTS
            and t_type not in _SEX_NEUTRAL_JOINTS
            and port_a.is_male == port_b.is_male):
        sex = "male" if port_a.is_male else "female"
        return (f"port-sex mismatch (both {sex}); ground-glass "
                f"joints need male ↔ female")
    return None


def validate_setup(setup: Setup) -> List[str]:
    """Validate every connection in a setup.  Returns a list of
    human-readable error strings; empty list = setup is valid."""
    errors: List[str] = []
    n = len(setup.equipment)

    # 1. Resolve equipment + cache.
    items: List[Optional[Equipment]] = []
    for i, eid in enumerate(setup.equipment):
        e = get_equipment(eid)
        items.append(e)
        if e is None:
            errors.append(
                f"setup {setup.id!r}: equipment[{i}] = "
                f"unknown id {eid!r}")
    if errors:
        return errors

    # 2. Walk each connection.
    for ci, conn in enumerate(setup.connections):
        from_idx = conn.from_equipment_idx
        to_idx = conn.to_equipment_idx
        if not (0 <= from_idx < n) or not (0 <= to_idx < n):
            errors.append(
                f"setup {setup.id!r}: connection[{ci}] equipment "
                f"index out of range ({from_idx} → {to_idx}, "
                f"N={n})")
            continue
        if from_idx == to_idx:
            errors.append(
                f"setup {setup.id!r}: connection[{ci}] is a "
                f"self-loop on equipment[{from_idx}]")
            continue
        e_from = items[from_idx]
        e_to = items[to_idx]
        port_from = _find_port(e_from, conn.from_port)
        port_to = _find_port(e_to, conn.to_port)
        if port_from is None:
            errors.append(
                f"setup {setup.id!r}: connection[{ci}] "
                f"port {conn.from_port!r} not on "
                f"equipment[{from_idx}] ({e_from.id})")
            continue
        if port_to is None:
            errors.append(
                f"setup {setup.id!r}: connection[{ci}] "
                f"port {conn.to_port!r} not on "
                f"equipment[{to_idx}] ({e_to.id})")
            continue
        # Joint-type check.  `open` is the wildcard — a generic
        # physical-contact port (clamp grip, hot-plate top,
        # vessel-on-bench) that pairs with anything.
        f_type = port_from.joint_type
        t_type = port_to.joint_type
        if (f_type != "open" and t_type != "open"
                and f_type != t_type):
            errors.append(
                f"setup {setup.id!r}: connection[{ci}] "
                f"joint mismatch: {f_type} vs {t_type}")
            continue
        # Sex check (skip for symmetric joint kinds + `open`).
        if (f_type not in _SEX_NEUTRAL_JOINTS
                and t_type not in _SEX_NEUTRAL_JOINTS
                and port_from.is_male == port_to.is_male):
            sex = "male" if port_from.is_male else "female"
            errors.append(
                f"setup {setup.id!r}: connection[{ci}] "
                f"port-sex mismatch (both {sex}); ground-glass "
                f"joints need male ↔ female")
    return errors


def _find_port(equipment: Equipment, name: str):
    for p in equipment.connection_ports:
        if p.name == name:
            return p
    return None


# ------------------------------------------------------------------
# Catalogue
# ------------------------------------------------------------------

def _build_catalogue() -> List[Setup]:
    setups: List[Setup] = []

    # ---- Simple distillation -----------------------------------
    # equipment[0] = pot RBF
    # equipment[1] = heating mantle
    # equipment[2] = Variac
    # equipment[3] = distillation head
    # equipment[4] = thermometer adapter
    # equipment[5] = thermometer
    # equipment[6] = Liebig condenser
    # equipment[7] = vacuum adapter
    # equipment[8] = receiver RBF
    setups.append(Setup(
        id="simple_distillation",
        name="Simple distillation",
        purpose=(
            "Purify a liquid OR separate two liquids whose "
            "boiling points differ by ≥ 50 °C.  The standard "
            "first-pass purification setup for any neat liquid "
            "or simple binary mixture."
        ),
        equipment=(
            "rbf", "heating_mantle", "variac",
            "distillation_head", "thermometer_adapter",
            "thermometer", "liebig_condenser",
            "vacuum_adapter", "rbf",
        ),
        connections=(
            SetupConnection(0, "neck", 3, "bottom",
                "Pot RBF neck → distillation head bottom joint"),
            SetupConnection(3, "thermometer", 4, "bottom",
                "Distillation head top → thermometer adapter"),
            SetupConnection(4, "therm-sleeve", 5, "stem",
                "Thermometer adapter → thermometer bulb"),
            SetupConnection(3, "side", 6, "bottom-joint",
                "Distillation head side arm → Liebig bottom"),
            SetupConnection(6, "top-joint", 7, "top",
                "Liebig top → vacuum adapter top"),
            SetupConnection(7, "bottom", 8, "neck",
                "Vacuum adapter bottom → receiver RBF neck"),
        ),
        procedure=(
            "1. Charge ~1/3 to 1/2 of the pot RBF with the "
            "liquid + a few boiling chips / stir bar.  2. "
            "Assemble pot in heating mantle, clamped to a "
            "ring stand by the distillation head neck.  3. "
            "Connect Liebig condenser water IN at the lower "
            "port + OUT at the upper for counter-current "
            "flow.  4. Apply vacuum at the vacuum adapter "
            "side port (or leave open for atmospheric).  5. "
            "Slowly increase the Variac setting until the "
            "first drop of distillate appears.  6. Note "
            "vapour temperature on the thermometer + collect "
            "fractions as the temperature stabilises at each "
            "component's BP."
        ),
        safety_notes=(
            "Always include boiling chips OR a stir bar to "
            "prevent superheating + bumping.  Verify cooling "
            "water flow BEFORE applying heat.  Keep the "
            "receiver flask vented (vacuum adapter side port) "
            "even for atmospheric distillations."
        ),
        pedagogical_notes=(
            "Vapour temperature at the distillation head reads "
            "the BP of whatever is currently distilling — NOT "
            "the pot temperature.  A sharp single-temperature "
            "plateau means a pure component; a sloping "
            "temperature trace means a mixture (collect "
            "fractions + redistil).  This is the workhorse "
            "purification setup students see in their first "
            "synthetic-organic lab."
        ),
        typical_reactions=(
            "Solvent purification (THF / Et₂O drying); "
            "post-reaction product isolation; recovering "
            "unreacted starting material"
        ),
        icon_id="setup_simple_dist",
    ))

    # ---- Fractional distillation -------------------------------
    # Same as simple but with a Vigreux column between RBF + head.
    setups.append(Setup(
        id="fractional_distillation",
        name="Fractional distillation",
        purpose=(
            "Separate two or more liquids with boiling points "
            "differing by < 50 °C.  The Vigreux column "
            "provides 5-15 theoretical plates of additional "
            "separation power vs simple distillation."
        ),
        equipment=(
            "rbf", "heating_mantle", "variac",
            "vigreux_column",
            "distillation_head", "thermometer_adapter",
            "thermometer", "liebig_condenser",
            "vacuum_adapter", "rbf",
        ),
        connections=(
            SetupConnection(0, "neck", 3, "bottom",
                "Pot RBF → Vigreux column bottom"),
            SetupConnection(3, "top", 4, "bottom",
                "Vigreux top → distillation head bottom"),
            SetupConnection(4, "thermometer", 5, "bottom",
                "Distillation head top → thermometer adapter"),
            SetupConnection(5, "therm-sleeve", 6, "stem",
                "Thermometer adapter → thermometer bulb"),
            SetupConnection(4, "side", 7, "bottom-joint",
                "Distillation head side arm → Liebig"),
            SetupConnection(7, "top-joint", 8, "top",
                "Liebig top → vacuum adapter"),
            SetupConnection(8, "bottom", 9, "neck",
                "Vacuum adapter → receiver RBF"),
        ),
        procedure=(
            "Same as simple distillation but with the Vigreux "
            "column inserted between pot + distillation head.  "
            "Heat slowly — the column needs time to "
            "equilibrate (lots of fractionation = lots of "
            "vapour ↔ liquid cycling on the indentations).  "
            "Wrap the column in glass wool / aluminium foil "
            "to insulate against heat loss → improves "
            "separation efficiency."
        ),
        safety_notes=(
            "The column adds height — clamp it AND the "
            "distillation head independently.  Heat too "
            "fast and you overshoot the equilibrium → "
            "fractions contaminate.  Watch the vapour "
            "temperature climb stepwise as each component "
            "starts distilling."
        ),
        pedagogical_notes=(
            "The number of theoretical plates (a measure of "
            "vapour-liquid equilibration cycles) scales "
            "roughly with column length and inversely with "
            "heating rate — slower distillation = better "
            "separation.  For very-close-BP separations "
            "(<10 °C apart, e.g. ortho/meta xylene) even "
            "Vigreux fails and a packed column or spinning-"
            "band column is needed."
        ),
        typical_reactions=(
            "Solvent mixture separation (EtOH/H₂O 78/100 °C, "
            "MeOH/H₂O 65/100 °C); separating reaction "
            "products from solvents with similar BPs"
        ),
        icon_id="setup_fractional_dist",
    ))

    # ---- Reflux ------------------------------------------------
    # equipment[0] = RBF
    # equipment[1] = heating mantle
    # equipment[2] = Variac
    # equipment[3] = Allihn condenser
    # equipment[4] = drying tube (atmospheric protection)
    setups.append(Setup(
        id="reflux",
        name="Standard reflux",
        purpose=(
            "Heat a reaction mixture at the solvent's boiling "
            "point indefinitely without losing solvent.  The "
            "single most-common synthetic-organic setup — used "
            "for any reaction needing sustained elevated "
            "temperature (Fischer esterification, condensation, "
            "ester hydrolysis, …)."
        ),
        equipment=(
            "rbf", "heating_mantle", "variac",
            "allihn_condenser", "drying_tube",
        ),
        connections=(
            SetupConnection(0, "neck", 3, "bottom-joint",
                "RBF → Allihn bottom joint"),
            SetupConnection(3, "top-joint", 4, "bottom",
                "Allihn top → drying tube (atmospheric "
                "moisture protection)"),
        ),
        procedure=(
            "1. Charge RBF with reactants + solvent + stir "
            "bar.  2. Connect Allihn condenser; turn on "
            "cooling water (lower port IN, upper OUT).  3. "
            "Cap the top with a drying tube if moisture-"
            "sensitive.  4. Set Variac to gently boil the "
            "solvent.  5. Vapour rises into the Allihn, "
            "condenses, drips back into the pot — solvent "
            "level stays constant indefinitely."
        ),
        safety_notes=(
            "ALWAYS turn on cooling water BEFORE applying "
            "heat — dry condenser + hot vapour = solvent "
            "loss + fire risk.  Allihn (bulb) condenser "
            "is preferred over Liebig for long reflux runs "
            "because the bulbs increase residence time + "
            "vapour-recovery efficiency."
        ),
        pedagogical_notes=(
            "Reflux is THE workhorse heated reaction setup — "
            "every organic-chemistry student builds this in "
            "their first lab.  The drying tube is the "
            "low-effort moisture-protection (CaCl₂ pellets "
            "absorb water but pass air); for serious air-"
            "sensitive work, swap for a Schlenk-line gas "
            "inlet and use a 3-neck RBF."
        ),
        typical_reactions=(
            "Fischer esterification; saponification (ester "
            "hydrolysis); imine / hydrazone formation; "
            "Williamson ether synthesis; SN1 / SN2 "
            "substitutions; reductive amination"
        ),
        icon_id="setup_reflux",
    ))

    # ---- Reflux with addition funnel ---------------------------
    # 3-neck RBF + mantle + Allihn + addition funnel + thermometer
    # NB: addition funnel ≠ separatory funnel functionally but
    # geometry is similar; we model with sep_funnel as the
    # closest catalogued piece.  A dedicated `addition_funnel`
    # entry can land in 38a polish.
    setups.append(Setup(
        id="reflux_with_addition",
        name="Reflux with controlled addition",
        purpose=(
            "Reflux setup where one reagent is added drop-by-"
            "drop (or stream) over the course of the reaction "
            "— used when a fast initial mixing would runaway "
            "thermally (Grignard formation, exothermic "
            "acylations, etc.)."
        ),
        equipment=(
            "rbf_3neck", "heating_mantle", "variac",
            "allihn_condenser", "sep_funnel",
            "thermometer_adapter", "thermometer",
        ),
        connections=(
            SetupConnection(0, "center", 3, "bottom-joint",
                "3-neck RBF center → Allihn condenser"),
            SetupConnection(0, "left", 4, "outlet",
                "3-neck left → addition funnel outlet "
                "(sep funnel used as an addition funnel; "
                "spout pegs into the side neck)"),
            SetupConnection(0, "right", 5, "bottom",
                "3-neck right → thermometer adapter"),
            SetupConnection(5, "therm-sleeve", 6, "stem",
                "Thermometer adapter → thermometer bulb"),
        ),
        procedure=(
            "1. Charge the substrate + solvent into the "
            "3-neck RBF.  Add stir bar.  2. Charge the "
            "addition funnel with the second reagent + "
            "appropriate solvent.  3. Begin gentle reflux + "
            "stirring.  4. Open the funnel stopcock to drip "
            "the reagent at a controlled rate (typically 1 "
            "drop per 1-2 seconds).  5. Monitor reaction "
            "temperature on the thermometer; throttle "
            "addition if temperature spikes."
        ),
        safety_notes=(
            "ALWAYS pre-reflux briefly with just the "
            "substrate to verify the cooling water + stirrer "
            "work BEFORE adding the reactive reagent.  For "
            "Grignard formation, also have a cooling bath "
            "ready in case the reaction needs to be quenched."
        ),
        pedagogical_notes=(
            "The 3-neck RBF gives you simultaneous reflux "
            "(centre) + reagent addition (one side) + "
            "temperature monitoring (other side) — the "
            "control surface for any non-trivial heated "
            "reaction.  Drop rate matters: too fast = heat "
            "build-up + side products; too slow = day-long "
            "addition + decomposition of the dropping "
            "reagent."
        ),
        typical_reactions=(
            "Grignard formation (RX + Mg → RMgX + addition "
            "to electrophile); acid chloride + amine → amide "
            "(exothermic); LDA-mediated deprotonation + "
            "alkylation"
        ),
        icon_id="setup_reflux_addition",
    ))

    # ---- Soxhlet extraction ------------------------------------
    setups.append(Setup(
        id="soxhlet_extraction",
        name="Soxhlet extraction",
        purpose=(
            "Continuously extract a solid analyte with hot "
            "fresh solvent over many hours / days.  Used when "
            "shake-flask extraction can't get all the analyte "
            "out (natural products from plant material, "
            "lipids from seeds, organics from soil)."
        ),
        equipment=(
            "rbf", "heating_mantle", "variac",
            "soxhlet_extractor", "allihn_condenser",
        ),
        connections=(
            SetupConnection(0, "neck", 3, "bottom",
                "Pot RBF → Soxhlet extractor bottom"),
            SetupConnection(3, "top", 4, "bottom-joint",
                "Soxhlet top → Allihn condenser"),
        ),
        procedure=(
            "1. Place the powdered solid analyte in a "
            "cellulose thimble inside the Soxhlet body.  2. "
            "Charge the pot RBF with extracting solvent "
            "(common: hexane / EtOH / DCM).  3. Connect + "
            "turn on cooling water.  4. Heat to gentle "
            "reflux.  5. Solvent vapour rises through the "
            "Soxhlet side arm + condenses onto the thimble + "
            "fills the thimble chamber + automatic siphon "
            "drains extract back to the pot.  6. Repeat "
            "indefinitely (typically overnight)."
        ),
        safety_notes=(
            "Long unattended runs — use a flow-monitor / "
            "moisture-detector on the cooling water in case "
            "water supply fails overnight.  Use the SMALLEST "
            "RBF that holds enough solvent (~150-300 % of "
            "the Soxhlet body capacity); minimises both "
            "solvent waste + fire risk."
        ),
        pedagogical_notes=(
            "Soxhlet IS continuous fresh-solvent extraction.  "
            "The cycle (boil → vapour → condense → fill "
            "thimble → siphon → repeat) means the analyte is "
            "always seeing pristine solvent, not a saturated "
            "one — that's why Soxhlet beats simple "
            "shake-flask extraction even after the "
            "shake-flask reaches apparent equilibrium."
        ),
        typical_reactions=(
            "Natural-product isolation (alkaloids from "
            "leaves, oils from seeds, flavanoids from "
            "fruits); environmental analysis (PAHs / "
            "pesticides from soil)"
        ),
        icon_id="setup_soxhlet",
    ))

    # ---- Vacuum filtration -------------------------------------
    setups.append(Setup(
        id="vacuum_filtration",
        name="Vacuum filtration (Büchner)",
        purpose=(
            "Rapidly separate solid + liquid by sucking the "
            "liquid through filter paper supported on a "
            "perforated funnel.  Used after recrystallisation, "
            "for collecting precipitates, and for removing "
            "drying agents (MgSO₄ / Na₂SO₄)."
        ),
        equipment=(
            "buchner_funnel", "filter_flask",
            "vacuum_trap", "aspirator",
        ),
        connections=(
            SetupConnection(0, "stem", 1, "mouth",
                "Büchner funnel stem → filter flask mouth "
                "(via rubber stopper)"),
            SetupConnection(1, "vacuum", 2, "system-side",
                "Filter flask side arm → cold trap "
                "(system side)"),
            SetupConnection(2, "pump-side", 3, "vacuum-port",
                "Cold trap → aspirator vacuum port"),
        ),
        procedure=(
            "1. Place a filter paper of the right diameter "
            "on the Büchner plate; wet with a few drops of "
            "filtrate solvent to seal.  2. Mount on the "
            "filter flask via a rubber stopper (or PTFE "
            "adapter).  3. Apply vacuum through the flask "
            "side arm (via cold trap → aspirator).  4. Pour "
            "solid + liquid mixture into the funnel; liquid "
            "passes through, solid retained on paper.  5. "
            "Wash solid with cold solvent if needed.  6. "
            "Break vacuum BEFORE turning off the aspirator "
            "(prevents back-suction)."
        ),
        safety_notes=(
            "Filter flask must be thick-walled / vacuum-"
            "rated — a normal Erlenmeyer can implode.  "
            "Always include a cold trap (or at minimum a "
            "trap bottle) between flask + aspirator — "
            "back-siphon of water on tap shutoff ruins "
            "the experiment + can splash chemicals.  "
            "Inspect filter flask for star cracks."
        ),
        pedagogical_notes=(
            "The vacuum-filtration setup IS the standard "
            "endpoint of every recrystallisation, every "
            "precipitate-isolation, every Soxhlet workup.  "
            "Filter paper choice matters — fast paper for "
            "coarse precipitates, slow paper for fine; "
            "fritted glass for the most demanding particle-"
            "size cuts."
        ),
        typical_reactions=(
            "Collecting recrystallised product; isolating "
            "a precipitate (e.g. acetylsalicylic acid from "
            "aspirin synthesis); filtering off MgSO₄ from "
            "an organic extract before rotovap"
        ),
        icon_id="setup_vacuum_filtration",
    ))

    # ---- Liquid-liquid extraction ------------------------------
    setups.append(Setup(
        id="liquid_liquid_extraction",
        name="Liquid-liquid extraction (separatory funnel)",
        purpose=(
            "Separate two immiscible liquids by gravity after "
            "shaking + letting them settle.  The standard "
            "aqueous-organic work-up step in every synthetic "
            "reaction — moves product from water into an "
            "organic phase (or vice versa) for further "
            "purification."
        ),
        equipment=(
            "sep_funnel", "ring_stand", "clamp_3prong",
            "erlenmeyer", "erlenmeyer",
        ),
        connections=(
            SetupConnection(0, "top", 2, "jaws",
                "Sep funnel neck clamped to 3-prong (boss "
                "on ring stand)"),
            SetupConnection(2, "boss", 1, "rod",
                "3-prong clamp boss → ring stand rod"),
            # Funnel stopcock drains into the lower (aqueous)
            # Erlenmeyer; upper organic phase poured out the
            # top into the second Erlenmeyer.  No port-level
            # connections to the Erlenmeyer flasks — they sit
            # below the funnel.
        ),
        procedure=(
            "1. Combine aqueous + organic phases in the "
            "sep funnel.  Stopper the top.  2. Invert + "
            "swirl gently — vent through the stopcock "
            "after each invert (organic vapour pressure).  "
            "3. Continue venting + shaking for 30-60 s.  "
            "4. Re-clamp on the ring stand; let phases "
            "separate by gravity (1-5 min).  5. Drain the "
            "lower (denser) phase through the stopcock into "
            "Erlenmeyer #1; pour the upper phase out the "
            "top into Erlenmeyer #2.  6. Repeat the "
            "extraction 2-3× to maximise recovery."
        ),
        safety_notes=(
            "VENT ALWAYS — pressure build-up (especially "
            "with low-BP solvents like Et₂O / DCM) can pop "
            "the stopper + spray contents.  Hold stopper in "
            "place while inverting.  Three small extractions "
            "recover more product than one large one (the "
            "math works out — Nernst equilibrium)."
        ),
        pedagogical_notes=(
            "The single most-used post-reaction work-up "
            "step.  Phase identification: ORGANIC is "
            "usually on TOP (less dense; e.g. Et₂O, EtOAc, "
            "hexane); chlorinated solvents (CHCl₃, DCM) are "
            "DENSER than water and end up on the BOTTOM.  "
            "When in doubt, add a drop of water to the "
            "decanted layer — if it sinks, that layer is "
            "organic; if it dissolves / mixes, it's aqueous."
        ),
        typical_reactions=(
            "Post-Fischer-esterification work-up "
            "(NaHCO₃ wash → brine wash → Na₂SO₄ dry); "
            "extracting amines into HCl then back-"
            "extracting after basification; pH-controlled "
            "separations of acidic / basic / neutral "
            "fractions"
        ),
        icon_id="setup_lle",
    ))

    # ---- Recrystallisation (apparatus only) --------------------
    setups.append(Setup(
        id="recrystallisation",
        name="Recrystallisation",
        purpose=(
            "Purify a solid by dissolving it in hot solvent + "
            "letting it crystallise on cooling.  The standard "
            "purification method for solid synthetic products "
            "— exploits the steeper solubility curve of the "
            "product vs the impurities."
        ),
        equipment=(
            "erlenmeyer", "hotplate_stirrer",
            "ice_bath", "buchner_funnel",
            "filter_flask", "aspirator",
        ),
        connections=(
            SetupConnection(0, "mouth", 1, "top",
                "Erlenmeyer placed on hot-plate top "
                "(open contact, no joint)"),
            SetupConnection(3, "stem", 4, "mouth",
                "Büchner stem → filter flask (collection "
                "stage)"),
            SetupConnection(4, "vacuum", 5, "vacuum-port",
                "Filter flask → aspirator vacuum"),
        ),
        procedure=(
            "1. Add crude solid + a few mL of solvent to "
            "the Erlenmeyer; warm on the hot plate to gentle "
            "boil.  2. Add solvent dropwise + swirl until "
            "everything just dissolves (minimum-solvent "
            "principle).  3. If coloured impurities present, "
            "add ~5 % activated carbon, boil briefly, hot-"
            "filter through fluted paper.  4. Let the "
            "filtered hot solution cool slowly to room "
            "temperature → crystals form.  5. Cool further "
            "in an ice bath for 15-30 min to maximise "
            "yield.  6. Vacuum-filter the crystals through "
            "a Büchner funnel; wash with a SMALL amount of "
            "ICE-COLD solvent.  7. Air-dry."
        ),
        safety_notes=(
            "Hot solvent on a hot plate = ignition risk for "
            "low-BP organics; prefer water bath / oil bath "
            "for Et₂O / pentane.  Don't add too much solvent "
            "— excess solvent dissolves the desired crystals "
            "AND keeps impurities in solution → defeats the "
            "purpose."
        ),
        pedagogical_notes=(
            "Recrystallisation works because the desired "
            "product's solubility curve is steeper than the "
            "impurities'.  As the solution cools, the "
            "supersaturated product crystallises out; the "
            "impurities stay below their saturation "
            "threshold + remain in the mother liquor (the "
            "filtrate).  Slow cooling = larger / purer "
            "crystals; fast cooling traps impurities in "
            "the lattice."
        ),
        typical_reactions=(
            "Aspirin (acetylsalicylic acid) synthesis "
            "purification; benzoic acid recrystallisation "
            "(EtOH/H₂O); paracetamol purification"
        ),
        icon_id="setup_recrystallisation",
    ))

    return setups


_SETUPS: List[Setup] = _build_catalogue()


# ------------------------------------------------------------------
# Public lookup helpers
# ------------------------------------------------------------------

def list_setups(category: Optional[str] = None) -> List[Setup]:
    """Return every catalogued setup.  ``category`` filtering
    is reserved for a future polish round — current setups
    don't carry a category field, so the parameter is a no-op
    + accepts ``None`` for forward-compatibility."""
    if category is None:
        return list(_SETUPS)
    return []   # placeholder — categories arrive in 38b polish


def get_setup(setup_id: str) -> Optional[Setup]:
    for s in _SETUPS:
        if s.id == setup_id:
            return s
    return None


def find_setups(needle: str) -> List[Setup]:
    """Case-insensitive substring search across id + name +
    purpose."""
    if not needle:
        return []
    n = needle.lower().strip()
    out: List[Setup] = []
    for s in _SETUPS:
        if (n in s.id.lower()
                or n in s.name.lower()
                or n in s.purpose.lower()):
            out.append(s)
    return out


def to_dict(s: Setup) -> Dict[str, object]:
    return {
        "id": s.id,
        "name": s.name,
        "purpose": s.purpose,
        "equipment": list(s.equipment),
        "connections": [
            {
                "from_equipment_idx": c.from_equipment_idx,
                "from_port": c.from_port,
                "to_equipment_idx": c.to_equipment_idx,
                "to_port": c.to_port,
                "note": c.note,
            } for c in s.connections
        ],
        "procedure": s.procedure,
        "safety_notes": s.safety_notes,
        "pedagogical_notes": s.pedagogical_notes,
        "typical_reactions": s.typical_reactions,
        "icon_id": s.icon_id,
    }
