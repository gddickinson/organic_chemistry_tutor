"""Phase 38a (round 140) — lab equipment catalogue.

Headless reference data for the *Tools → Lab equipment…* dialog
and the future Phase-38c canvas.  Each :class:`Equipment` entry
describes a piece of lab apparatus the way an undergraduate /
medicinal-chem student needs to see it: name, what it does,
which setups it appears in, common variants (sizes, joint
types), safety notes, and the named connection ports the future
canvas will use to snap items together.

Categories
----------
- ``"glassware"`` — RBFs, Erlenmeyers, beakers, distillation
  flasks.
- ``"adapter"`` — Claisen / vacuum / take-off / thermometer
  adapters, stoppers, septa.
- ``"condenser"`` — Liebig, Allihn, Graham, Friedrichs,
  Dimroth, air, cold finger.
- ``"heating"`` — heating mantle, hot plate, Variac, oil /
  sand / water bath, Bunsen.
- ``"cooling"`` — ice / NaCl / dry-ice baths, cold fingers.
- ``"separation"`` — separatory funnel, Soxhlet, Vigreux /
  packed fractionating column.
- ``"filtration"`` — Büchner / Hirsch / fritted funnels.
- ``"vacuum"`` — vacuum pump, aspirator, vacuum trap, drying
  tube.
- ``"stirring"`` — magnetic stir bar, mechanical overhead
  stirrer, cannula.
- ``"support"`` — ring stand, clamps, Keck clip, iron ring,
  cork ring.
- ``"safety"`` — fume hood, thermometer, pH meter,
  inert-gas balloon.
- ``"analytical"`` — melting-point apparatus, IR / GC-MS /
  HPLC station references (placeholder cross-refs to the
  Phase 37c/d catalogue tools).

The :class:`ConnectionPort` records on each item define the
named joints / connections the future Phase-38c canvas will
snap together when the user drags item A onto item B.  For
ground-glass joints we use the ANSI standard taper ratio
(``"14/20"``, ``"24/29"``, ``"29/32"``); rubber tubing
connections are tagged ``"hose"``; electrical / thermometer
sockets are tagged ``"socket"``.  ``"open"`` ports (Erlenmeyer
necks, beaker tops) accept any compatible piece without a
joint constraint.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class ConnectionPort:
    """A named joint / port on a piece of equipment.  Used by
    the future Phase-38c canvas to validate item-to-item
    snapping (round-bottom flask 24/29 neck pairs with
    distillation-head 24/29 male joint, etc.)."""
    name: str
    location: str           # "top" / "bottom" / "side-left" / etc.
    joint_type: str         # "24/29" / "14/20" / "hose" / "open" / …
    is_male: bool = False   # True = peg, False = socket


@dataclass(frozen=True)
class Equipment:
    id: str
    name: str
    category: str
    description: str
    typical_uses: str           # what setups this appears in
    variants: str = ""          # size / material variants
    safety_notes: str = ""
    icon_id: str = ""           # placeholder; SVG path lands in 38c
    connection_ports: Tuple[ConnectionPort, ...] = field(
        default_factory=tuple)


VALID_CATEGORIES: tuple = (
    "glassware", "adapter", "condenser",
    "heating", "cooling",
    "separation", "filtration",
    "vacuum", "stirring", "support",
    "safety", "analytical",
)


# ------------------------------------------------------------------
# Catalogue helpers
# ------------------------------------------------------------------

def _glassware_neck(size: str = "24/29") -> ConnectionPort:
    """Standard ground-glass top opening on a flask."""
    return ConnectionPort(
        name="neck", location="top",
        joint_type=size, is_male=False)


def _hose(name: str, location: str) -> ConnectionPort:
    return ConnectionPort(
        name=name, location=location,
        joint_type="hose", is_male=False)


def _make_male(size: str = "24/29",
               name: str = "male", location: str = "bottom"
               ) -> ConnectionPort:
    return ConnectionPort(
        name=name, location=location,
        joint_type=size, is_male=True)


def _make_female(size: str = "24/29",
                 name: str = "female", location: str = "top"
                 ) -> ConnectionPort:
    return ConnectionPort(
        name=name, location=location,
        joint_type=size, is_male=False)


# ------------------------------------------------------------------
# Catalogue
# ------------------------------------------------------------------

def _build_catalogue() -> List[Equipment]:
    return [

        # ---- Glassware ----
        Equipment(
            id="rbf",
            name="Round-bottom flask",
            category="glassware",
            description=(
                "Spherical glass flask with a single ground-"
                "glass neck.  Round profile distributes "
                "thermal stress evenly + maximises surface "
                "area for heating, making it the universal "
                "vessel for heated reactions, distillations, "
                "and reflux."
            ),
            typical_uses=(
                "Reflux setup; simple + fractional "
                "distillation pot; rotary evaporation; "
                "Soxhlet extraction reservoir; reaction "
                "vessel for heated work-ups"
            ),
            variants=(
                "Common sizes: 25 / 50 / 100 / 250 / 500 / "
                "1000 / 2000 mL.  Joint sizes 14/20 (micro-"
                "scale) / 19/22 / 24/29 (US standard) / "
                "29/32 (large)."
            ),
            safety_notes=(
                "Always support in a cork ring or clamp — "
                "round bottom won't sit flat.  Inspect for "
                "star cracks before any heated / pressurised "
                "use; a cracked RBF can implode under "
                "vacuum."
            ),
            icon_id="rbf",
            connection_ports=(_glassware_neck("24/29"),),
        ),
        Equipment(
            id="rbf_3neck",
            name="Three-neck round-bottom flask",
            category="glassware",
            description=(
                "RBF with one central + two angled side "
                "necks.  Lets you combine reflux condenser "
                "+ thermometer + dropping funnel / cannula "
                "/ gas inlet on a single pot — essential "
                "for any reaction needing temperature "
                "monitoring AND controlled reagent addition."
            ),
            typical_uses=(
                "Reactions with controlled-rate addition "
                "(Grignard formation, exothermic acylations); "
                "Schlenk-line reactions under inert "
                "atmosphere; simultaneous reflux + "
                "temperature monitoring; multi-step one-pot "
                "syntheses"
            ),
            variants=(
                "100 / 250 / 500 / 1000 mL most common.  "
                "Side necks angled (typical) or vertical "
                "(less common).  All necks usually 24/29; "
                "side necks may be smaller (14/20) for "
                "thermometer / cannula access."
            ),
            safety_notes=(
                "Heavier than a single-neck RBF — clamp "
                "the central neck securely.  More joints = "
                "more potential leak points; grease or use "
                "Keck clips on every joint for vacuum / "
                "inert-atmosphere work."
            ),
            icon_id="rbf_3neck",
            connection_ports=(
                ConnectionPort("center", "top", "24/29", False),
                ConnectionPort("left", "top-left", "24/29", False),
                ConnectionPort("right", "top-right", "24/29", False),
            ),
        ),
        Equipment(
            id="erlenmeyer",
            name="Erlenmeyer flask",
            category="glassware",
            description=(
                "Conical flask with a flat bottom + narrow "
                "neck.  Profile lets you swirl the contents "
                "without splashing, while the narrow neck "
                "minimises evaporation.  General-purpose "
                "vessel for unheated work, recrystallisation, "
                "titrations."
            ),
            typical_uses=(
                "Titration; recrystallisation; collecting "
                "filtrate; mixing solutions; storing reagent "
                "solutions; bacterial cell culture (sterile "
                "version)"
            ),
            variants=(
                "Sizes 25 / 50 / 125 / 250 / 500 / 1000 / "
                "2000 / 4000 mL.  Plain mouth (most common) "
                "or 19/22 / 24/29 ground-glass joint "
                "(filter-flask / air-tight variants)."
            ),
            safety_notes=(
                "Flat bottom means it can heat directly on "
                "a hotplate — but flat-bottomed vessels can "
                "implode under vacuum (use only if rated; "
                "filter flasks are rated).  Don't use a "
                "regular Erlenmeyer for vacuum filtration."
            ),
            icon_id="erlenmeyer",
            connection_ports=(
                ConnectionPort("mouth", "top", "open", False),
            ),
        ),
        Equipment(
            id="beaker",
            name="Beaker",
            category="glassware",
            description=(
                "Cylindrical flat-bottomed glass with a "
                "spout.  Lowest-precision liquid measure but "
                "easy pouring + stirring + dissolution.  "
                "Workhorse for any unheated / non-sealed "
                "task."
            ),
            typical_uses=(
                "Solution preparation; dilution; rough "
                "transfer; scale-tare for mass; cooling "
                "bath water reservoir; temporary holding "
                "of intermediate fractions"
            ),
            variants=(
                "Sizes 10 / 25 / 50 / 100 / 250 / 500 / 1000 "
                "/ 2000 / 4000 mL.  Glass (standard, "
                "borosilicate) or polypropylene (acid / base "
                "compatible, autoclavable)."
            ),
            safety_notes=(
                "Open top → no contamination protection.  "
                "Beakers are rough volumetric only "
                "(±5 % accuracy at best — use volumetric "
                "flask / pipette for accurate measurement)."
            ),
            icon_id="beaker",
            connection_ports=(
                ConnectionPort("top", "top", "open", False),
            ),
        ),

        # ---- Adapters ----
        Equipment(
            id="distillation_head",
            name="Distillation head (3-way)",
            category="adapter",
            description=(
                "Y-shaped glass adapter that sits on the "
                "distillation pot, accepts a thermometer "
                "in the vertical arm, and routes the vapour "
                "horizontally into a condenser.  The "
                "'simple distillation' workhorse adapter."
            ),
            typical_uses=(
                "Simple distillation (RBF + heating mantle "
                "→ distillation head + thermometer → "
                "condenser → vacuum adapter → receiver); "
                "short-path distillation; vapour-temperature "
                "monitoring"
            ),
            variants=(
                "Standard 24/29 joints throughout; 14/20 "
                "thermometer-arm variants exist for micro-"
                "scale work.  Some include a side-arm with "
                "vacuum take-off (eliminates the need for a "
                "separate vacuum adapter)."
            ),
            safety_notes=(
                "Brittle joint between the head + the "
                "condenser if not properly supported.  "
                "Always Keck-clip OR clamp the head + "
                "condenser independently."
            ),
            icon_id="distill_head",
            connection_ports=(
                _make_male("24/29", "bottom", "bottom"),
                ConnectionPort("thermometer", "top",
                               "24/29", False),
                # Side arm pegs into the condenser inlet (which is
                # female).  Male = True.
                ConnectionPort("side", "side-right",
                               "24/29", True),
            ),
        ),
        Equipment(
            id="claisen_adapter",
            name="Claisen adapter",
            category="adapter",
            description=(
                "Two-necked Y-adapter that converts a "
                "single-neck RBF into a pseudo-two-neck "
                "flask.  Lets you add a dropping funnel / "
                "thermometer / gas inlet on top of an "
                "existing reflux condenser without buying a "
                "three-neck flask."
            ),
            typical_uses=(
                "Adding a thermometer to a reflux setup; "
                "dropping funnel + reflux without a 3-neck "
                "RBF; gas inlet for inert-atmosphere work; "
                "the 'I need an extra neck' adapter"
            ),
            variants=(
                "Standard 24/29 joints throughout.  Some "
                "variants have one 14/20 side neck for "
                "thermometer + one 24/29 for funnel."
            ),
            safety_notes=(
                "Adds height to the column; clamp sturdily "
                "near the top to prevent the assembly from "
                "falling forward.  Each joint adds friction "
                "loss for vacuum work."
            ),
            icon_id="claisen",
            connection_ports=(
                _make_male("24/29", "bottom", "bottom"),
                ConnectionPort("center", "top", "24/29", False),
                ConnectionPort("side", "top-right", "24/29", False),
            ),
        ),
        Equipment(
            id="vacuum_adapter",
            name="Vacuum take-off adapter",
            category="adapter",
            description=(
                "Bent-tube adapter with a side hose-port for "
                "vacuum + a vertical joint to receive the "
                "distillate from a condenser.  Routes the "
                "condensed vapour into a receiving flask "
                "while applying vacuum to the system."
            ),
            typical_uses=(
                "End piece on every distillation: receives "
                "condensate from the condenser, drips it "
                "into the receiver, applies vacuum from a "
                "side port; connects vacuum line for "
                "rotovap reduced-pressure setups"
            ),
            variants=(
                "Plain (no stopcock) or with a stopcock for "
                "atmosphere-vs-vacuum switching.  Cow / "
                "spider-multi-receiver variants let you "
                "switch between fraction-collection flasks "
                "without breaking vacuum."
            ),
            safety_notes=(
                "Stopcock vacuum adapters can leak around "
                "the plug if Teflon barrel is worn; check "
                "+ regrease."
            ),
            icon_id="vacuum_adapter",
            connection_ports=(
                # Top is the condenser-side socket (female,
                # accepts the condenser male outlet).
                _make_female("24/29", "top", "top"),
                # Bottom is the receiver-side peg (male).
                _make_male("24/29", "bottom", "bottom"),
                _hose("vacuum", "side-right"),
            ),
        ),
        Equipment(
            id="thermometer_adapter",
            name="Thermometer adapter",
            category="adapter",
            description=(
                "Short connector with a rubber / Teflon "
                "sleeve at the top that grips a glass "
                "thermometer + a ground-glass joint at the "
                "bottom.  Lets you insert a thermometer "
                "into any standard joint."
            ),
            typical_uses=(
                "Adding a thermometer to a distillation "
                "head; monitoring reaction temperature in a "
                "Claisen-adapted RBF; vapour-temperature "
                "measurement"
            ),
            variants=(
                "14/20 or 24/29 joint; rubber / silicone / "
                "Teflon sleeve.  Screw-cap variants "
                "(thermometer through a PTFE-lined cap) for "
                "Schlenk-line air-free work."
            ),
            safety_notes=(
                "Insert + remove the thermometer SLOWLY — "
                "fast forcing can snap the bulb (mercury "
                "spill is a hazardous-waste event)."
            ),
            icon_id="therm_adapter",
            connection_ports=(
                _make_male("24/29", "bottom", "bottom"),
                ConnectionPort("therm-sleeve", "top",
                               "thermometer-sleeve", False),
            ),
        ),
        Equipment(
            id="stopper",
            name="Glass stopper",
            category="adapter",
            description=(
                "Solid ground-glass plug to seal an "
                "unused joint.  Maintains the airtight "
                "seal of a reaction vessel without needing "
                "a real adapter / piece of glassware."
            ),
            typical_uses=(
                "Sealing the unused side neck of a 3-neck "
                "RBF; closing a separatory funnel during "
                "shaking; capping a sample vial during "
                "storage"
            ),
            variants=(
                "Hollow (regular) or solid (used as "
                "weights).  Numbered series (#13 / #19 / "
                "#22 / #27 / #32) match standard ground-"
                "glass neck sizes."
            ),
            safety_notes=(
                "Frozen stoppers happen — apply gentle heat "
                "OR dilute warm water around the joint to "
                "free; never force with pliers."
            ),
            icon_id="stopper",
            connection_ports=(
                _make_male("24/29", "bottom", "bottom"),
            ),
        ),
        Equipment(
            id="septum",
            name="Rubber septum",
            category="adapter",
            description=(
                "Thick rubber / silicone disc that fits "
                "into a ground-glass joint.  Allows syringe "
                "/ cannula access to the reaction without "
                "breaking the seal — essential for "
                "moisture- or air-sensitive work."
            ),
            typical_uses=(
                "Cannula transfer of air-sensitive reagents "
                "(BuLi, Grignards, alkyl boranes); syringe "
                "addition of sub-mL reagents; gas-sampling "
                "headspace of a reaction"
            ),
            variants=(
                "Red rubber (cheap, OK for short-term work, "
                "swells in many organics); white / clear "
                "silicone (more solvent-resistant); "
                "PTFE-faced (most resistant; one-shot use)."
            ),
            safety_notes=(
                "Punctures accumulate — replace any septum "
                "with > ~5 needle holes.  Some solvents "
                "(THF, DCM) extract plasticisers from rubber "
                "→ contamination."
            ),
            icon_id="septum",
            connection_ports=(
                ConnectionPort("body", "bottom",
                               "24/29", True),
                ConnectionPort("syringe-port", "top",
                               "syringe-needle", False),
            ),
        ),

        # ---- Condensers ----
        Equipment(
            id="liebig_condenser",
            name="Liebig condenser",
            category="condenser",
            description=(
                "Straight-tube water-jacketed condenser, "
                "the simplest + most common condenser type.  "
                "Cooling water flows through the outer "
                "jacket counter-current to the vapour in "
                "the inner tube."
            ),
            typical_uses=(
                "Simple distillation (the standard horizontal "
                "condenser between distillation head + "
                "vacuum adapter); reflux setup (vertical "
                "orientation; less efficient than Allihn for "
                "long-term reflux but cheap + simple)"
            ),
            variants=(
                "Lengths: 200 / 300 / 400 mm.  Joint sizes "
                "14/20 / 24/29 / 29/32.  Hose connectors are "
                "standard rubber-tubing sized."
            ),
            safety_notes=(
                "Always confirm cooling water flow BEFORE "
                "applying heat.  Connect water IN at the "
                "lower port + OUT at the upper for "
                "counter-current efficiency."
            ),
            icon_id="liebig",
            connection_ports=(
                # Liebig is the *distillation* condenser —
                # canonical orientation has the female end
                # toward the distillation head (which has a
                # male side arm) and the male end toward the
                # vacuum adapter (which has a female top).
                _make_female("24/29", "bottom-joint", "bottom"),
                _make_male("24/29", "top-joint", "top"),
                _hose("water-in", "side-right-low"),
                _hose("water-out", "side-right-high"),
            ),
        ),
        Equipment(
            id="allihn_condenser",
            name="Allihn condenser (bulb)",
            category="condenser",
            description=(
                "Inner tube formed into a series of bulbs "
                "(typically 3-5).  Bulbs increase surface "
                "area + residence time for falling "
                "condensate, making this the preferred "
                "condenser for reflux."
            ),
            typical_uses=(
                "Reflux of solvents with moderate boiling "
                "points (acetone, EtOH, MeOH, THF); "
                "preferred over Liebig for any reflux "
                "needing > 30 min sustained vapour return"
            ),
            variants=(
                "Number of bulbs (3 / 5 / 7); lengths "
                "200-400 mm; standard joint sizes."
            ),
            safety_notes=(
                "Same water-flow precaution as Liebig.  "
                "Bulbs trap condensate momentarily — for "
                "very-low-BP solvents (Et₂O, pentane) use "
                "Friedrichs / Dimroth instead."
            ),
            icon_id="allihn",
            connection_ports=(
                # Bottom = male peg (slots into the flask /
                # head female above when reflux-mounted; or
                # accepts the head's male side arm when used
                # horizontally — either way, bottom-as-male
                # is the canonical condenser orientation).
                _make_male("24/29", "bottom-joint", "bottom"),
                # Top = female socket (accepts a drying tube,
                # vacuum adapter, or stopper).
                _make_female("24/29", "top-joint", "top"),
                _hose("water-in", "side-right-low"),
                _hose("water-out", "side-right-high"),
            ),
        ),
        Equipment(
            id="graham_condenser",
            name="Graham condenser (coil)",
            category="condenser",
            description=(
                "Coiled inner tube — maximum cooling surface "
                "area for the same column height.  Most "
                "efficient single-pass condenser type.  "
                "BUT the long coil collects + retains "
                "condensate, making it poor for distillation "
                "(low fraction recovery) and only OK for "
                "reflux."
            ),
            typical_uses=(
                "Low-volume reflux of high-BP solvents; "
                "specialty applications where condenser "
                "footprint matters more than fraction "
                "recovery"
            ),
            variants=(
                "Standard joint sizes; lengths 200-400 mm."
            ),
            safety_notes=(
                "Coil condensate is hard to drain "
                "completely — bake out at the end of every "
                "use to remove residual solvent."
            ),
            icon_id="graham",
            connection_ports=(
                # Bottom = male peg (slots into the flask /
                # head female above when reflux-mounted; or
                # accepts the head's male side arm when used
                # horizontally — either way, bottom-as-male
                # is the canonical condenser orientation).
                _make_male("24/29", "bottom-joint", "bottom"),
                # Top = female socket (accepts a drying tube,
                # vacuum adapter, or stopper).
                _make_female("24/29", "top-joint", "top"),
                _hose("water-in", "side-right-low"),
                _hose("water-out", "side-right-high"),
            ),
        ),
        Equipment(
            id="friedrichs_condenser",
            name="Friedrichs condenser",
            category="condenser",
            description=(
                "Inner tube formed into a coiled spiral "
                "INSIDE a wide outer jacket — maximum "
                "vapour-cooling efficiency for low-BP "
                "solvents under reflux.  The most efficient "
                "reflux condenser available."
            ),
            typical_uses=(
                "Reflux of very-low-BP solvents (diethyl "
                "ether, pentane, dichloromethane); "
                "high-temperature reflux where Allihn / "
                "Liebig let too much vapour escape"
            ),
            variants=(
                "Standard joint sizes; lengths 250-500 mm; "
                "Dimroth (similar geometry, internal coil "
                "carries the COOLING water rather than the "
                "vapour) is a close cousin."
            ),
            safety_notes=(
                "Heavier than Liebig / Allihn; clamp the "
                "joint AND a body clamp partway up.  More "
                "expensive — handle with care."
            ),
            icon_id="friedrichs",
            connection_ports=(
                # Bottom = male peg (slots into the flask /
                # head female above when reflux-mounted; or
                # accepts the head's male side arm when used
                # horizontally — either way, bottom-as-male
                # is the canonical condenser orientation).
                _make_male("24/29", "bottom-joint", "bottom"),
                # Top = female socket (accepts a drying tube,
                # vacuum adapter, or stopper).
                _make_female("24/29", "top-joint", "top"),
                _hose("water-in", "side-right-low"),
                _hose("water-out", "side-right-high"),
            ),
        ),
        Equipment(
            id="dimroth_condenser",
            name="Dimroth condenser",
            category="condenser",
            description=(
                "Coiled inner-tube condenser with a double-"
                "ended cooling coil.  Cooling water enters + "
                "exits at the SAME end (top), with the coil "
                "extending down through the vapour space.  "
                "Excellent vapour-recovery efficiency."
            ),
            typical_uses=(
                "Long-duration reflux; rotary evaporator "
                "(the standard rotovap condenser is "
                "Dimroth-style); low-BP solvents"
            ),
            variants=(
                "Joint sizes 24/29 / 29/32; lengths 250-500 "
                "mm; some designs include a vacuum jacket "
                "for cryogenic applications."
            ),
            safety_notes=(
                "Both water-tubing connections at the same "
                "end → easy to swap inlet/outlet by mistake "
                "(reduces efficiency but doesn't fail).  "
                "Label the connections."
            ),
            icon_id="dimroth",
            connection_ports=(
                # Bottom = male peg (slots into the flask /
                # head female above when reflux-mounted; or
                # accepts the head's male side arm when used
                # horizontally — either way, bottom-as-male
                # is the canonical condenser orientation).
                _make_male("24/29", "bottom-joint", "bottom"),
                # Top = female socket (accepts a drying tube,
                # vacuum adapter, or stopper).
                _make_female("24/29", "top-joint", "top"),
                _hose("water-in", "side-top-1"),
                _hose("water-out", "side-top-2"),
            ),
        ),
        Equipment(
            id="air_condenser",
            name="Air condenser",
            category="condenser",
            description=(
                "Long unjacketed glass tube — relies on "
                "ambient air convection for cooling.  Useful "
                "ONLY for very-high-boiling solvents "
                "(>150 °C) where water cooling would cause "
                "condenser cracking from thermal shock."
            ),
            typical_uses=(
                "Reflux of high-boiling solvents (DMSO, "
                "DMF, decalin, mineral oil); pyrolysis-style "
                "reactions; situations where running cold "
                "water onto a hot column would crack the "
                "glass"
            ),
            variants=(
                "Lengths 300-600 mm; sometimes ribbed "
                "outside for extra cooling surface."
            ),
            safety_notes=(
                "Low cooling capacity — vapour LOSS is "
                "expected.  Fume hood essential."
            ),
            icon_id="air_condenser",
            connection_ports=(
                # Bottom = male peg (slots into the flask /
                # head female above when reflux-mounted; or
                # accepts the head's male side arm when used
                # horizontally — either way, bottom-as-male
                # is the canonical condenser orientation).
                _make_male("24/29", "bottom-joint", "bottom"),
                # Top = female socket (accepts a drying tube,
                # vacuum adapter, or stopper).
                _make_female("24/29", "top-joint", "top"),
            ),
        ),

        # ---- Heating ----
        Equipment(
            id="heating_mantle",
            name="Heating mantle",
            category="heating",
            description=(
                "Hemispherical fabric / fibreglass shell "
                "with embedded resistance wire that wraps "
                "around the bottom of an RBF.  Even heating "
                "across the flask surface; no naked flame.  "
                "Almost universal for synthetic organic work "
                "above ~100 °C."
            ),
            typical_uses=(
                "Reflux at any solvent BP; distillation "
                "pot heating; any reaction with "
                "flammable solvents (avoids open flame); "
                "the standard RBF heater for most lab "
                "work above 100 °C"
            ),
            variants=(
                "Sized to match RBF volume (50 / 100 / 250 "
                "/ 500 / 1000 / 2000 mL).  Built-in stir "
                "(combined stirrer-mantle) or plain.  Often "
                "paired with a Variac for temperature "
                "control."
            ),
            safety_notes=(
                "Match mantle size to flask — undersize "
                "creates hot spots that crack the flask; "
                "oversize wastes power.  Plug into a Variac, "
                "NOT direct mains, to avoid runaway heating."
            ),
            icon_id="heating_mantle",
            connection_ports=(
                ConnectionPort("flask-cradle", "top",
                               "rbf-shell", False),
                ConnectionPort("power", "side-right",
                               "socket", False),
            ),
        ),
        Equipment(
            id="variac",
            name="Variac (variable autotransformer)",
            category="heating",
            description=(
                "Voltage controller — a knob-driven "
                "transformer that outputs 0-140 V from a "
                "120 V mains input.  Used to set the heating-"
                "mantle output anywhere from 0 to maximum "
                "without on/off cycling."
            ),
            typical_uses=(
                "Temperature control of heating mantles; "
                "ramping up to reaction temperature; "
                "anywhere a heater needs continuous-"
                "variable power"
            ),
            variants=(
                "5 A (small mantles); 10 A; 20 A.  Some "
                "include a digital voltmeter; basic ones "
                "are knob-only."
            ),
            safety_notes=(
                "Settings are NOT a temperature — same "
                "Variac setting on different mantles + "
                "flask combinations gives different "
                "temperatures.  Always monitor with a "
                "thermometer in the reaction."
            ),
            icon_id="variac",
            connection_ports=(
                ConnectionPort("mains-in", "back-left",
                               "socket", True),
                ConnectionPort("output", "back-right",
                               "socket", False),
            ),
        ),
        Equipment(
            id="hotplate_stirrer",
            name="Hot plate / magnetic stirrer",
            category="heating",
            description=(
                "Combined magnetic-stir + flat-top heating "
                "platform.  Magnetic field below the plate "
                "spins a stir bar in the vessel above; "
                "ceramic / aluminium top heats by "
                "resistance.  The benchtop workhorse for "
                "small-scale work below ~250 °C."
            ),
            typical_uses=(
                "Stirring + heating Erlenmeyer flasks, "
                "beakers, RBFs (with appropriate clamping); "
                "oil baths / sand baths sit ON the hot "
                "plate; recrystallisation; titrations"
            ),
            variants=(
                "Top size (small 100×100 mm to large "
                "200×200 mm); ceramic vs aluminium top "
                "(ceramic cleaner, aluminium more conductive); "
                "with / without external temperature-probe "
                "feedback."
            ),
            safety_notes=(
                "Top stays HOT for 10-20 minutes after "
                "switch-off — never assume cool.  Don't put "
                "round-bottom flasks directly on a flat "
                "hotplate; use an oil / sand bath or a "
                "heating mantle."
            ),
            icon_id="hotplate",
            connection_ports=(
                # Top is a flat surface that any vessel can
                # sit on — modelled as `open` so the validator
                # doesn't enforce a joint match for "vessel
                # placed on plate".
                ConnectionPort("top", "top",
                               "open", False),
                ConnectionPort("temperature-probe", "side-right",
                               "thermocouple-jack", False),
            ),
        ),
        Equipment(
            id="oil_bath",
            name="Silicone oil bath",
            category="heating",
            description=(
                "Pyrex or stainless-steel container of "
                "high-temperature silicone oil heated on a "
                "hot plate.  RBF or 3-neck flask is "
                "submerged + heated by the bath.  Good "
                "thermal contact (vs sand) + precise "
                "temperature (vs naked flame); usable to "
                "~200 °C with standard silicone oil."
            ),
            typical_uses=(
                "Reflux of medium-BP solvents on a hot "
                "plate; controlled-temperature reactions "
                "without a heating mantle; any setup where "
                "even thermal coupling matters more than "
                "the convenience of a hemispherical mantle"
            ),
            variants=(
                "Standard silicone oil to 200 °C; high-"
                "temperature silicone to 300 °C; mineral "
                "oil to 250 °C (cheaper but smokes earlier); "
                "Wood's metal alloy bath for >300 °C "
                "(aggressive, mostly historical)."
            ),
            safety_notes=(
                "Water + hot oil = explosive splatter — "
                "keep all aqueous reagents away.  Don't "
                "exceed the oil's rated temperature (smoke "
                "/ ignition risk).  Decant + store the oil "
                "between uses to prevent dust contamination."
            ),
            icon_id="oil_bath",
            connection_ports=(
                ConnectionPort("flask", "top",
                               "open", False),
            ),
        ),
        Equipment(
            id="bunsen_burner",
            name="Bunsen burner",
            category="heating",
            description=(
                "Gas-air burner producing an open flame.  "
                "Once the universal lab heater; now mostly "
                "displaced by hot plates + heating mantles "
                "for safety reasons (open flames + organic "
                "solvents = bad).  Still used for glass "
                "bending, flame testing of metal salts, and "
                "high-temperature inorganic work."
            ),
            typical_uses=(
                "Flame test for cation identification "
                "(see Phase 37a qualitative-tests catalogue); "
                "glass bending / sealing; sterilisation of "
                "inoculation loops in microbiology; high-"
                "temperature inorganic syntheses"
            ),
            variants=(
                "Single-burner (most common); Tirrill "
                "burner (built-in flame regulator); "
                "Meker burner (multi-jet for higher "
                "temperatures + larger flame area)."
            ),
            safety_notes=(
                "NEVER use near flammable organic solvents.  "
                "Hot tip stays dangerous for minutes after "
                "shut-off.  Always cap the gas tap when "
                "done.  Many institutions ban Bunsens "
                "outright in synthetic-chemistry labs."
            ),
            icon_id="bunsen",
            connection_ports=(
                ConnectionPort("gas-in", "side-bottom",
                               "gas-tube", False),
            ),
        ),

        # ---- Cooling ----
        Equipment(
            id="ice_bath",
            name="Ice / water bath (0 °C)",
            category="cooling",
            description=(
                "Crushed ice + a small amount of water in a "
                "Dewar / beaker.  Maintains 0 °C reliably "
                "for the duration of the ice supply.  The "
                "cheapest cooling bath."
            ),
            typical_uses=(
                "Quenching exothermic reactions; "
                "recrystallisation cool-down; controlled-"
                "temperature additions of reactive "
                "reagents (e.g. Br₂, SOCl₂)"
            ),
            variants=(
                "Plain ice/water (0 °C); ice + NaCl 3:1 "
                "→ -10 °C / -20 °C; ice + CaCl₂·6H₂O 1:1 "
                "→ -40 °C; brine slush."
            ),
            safety_notes=(
                "Water-soluble waste streams contaminate "
                "the bath — keep separate from product "
                "isolation."
            ),
            icon_id="ice_bath",
            connection_ports=(
                ConnectionPort("flask", "top",
                               "open", False),
            ),
        ),
        Equipment(
            id="dry_ice_bath",
            name="Dry ice / acetone bath (-78 °C)",
            category="cooling",
            description=(
                "Crushed dry ice (solid CO₂) + acetone in a "
                "Dewar.  Maintains -78 °C reliably (the "
                "sublimation temperature of CO₂).  The "
                "standard 'cryogenic' bath in a synthetic "
                "lab — needed for n-BuLi, LDA-mediated "
                "deprotonations, ozonolysis."
            ),
            typical_uses=(
                "n-BuLi / s-BuLi / t-BuLi reactions; "
                "lithium dialkylamide (LDA) generation + "
                "use; ozonolysis (O₃ generator); generally "
                "any reactive-organometallic chemistry"
            ),
            variants=(
                "Dry ice + acetone (-78 °C, classic); dry "
                "ice + IPA (-78 °C, less hygroscopic); "
                "dry ice + ethylene glycol (-15 °C, slush)."
            ),
            safety_notes=(
                "Always wear cryogenic gloves when handling "
                "dry ice — frostbite within seconds.  Dry "
                "ice + acetone foams violently when first "
                "combined; add dry ice slowly to acetone "
                "in a wide-mouth Dewar, NOT a narrow vessel."
            ),
            icon_id="dry_ice_bath",
            connection_ports=(
                ConnectionPort("flask", "top",
                               "open", False),
            ),
        ),

        # ---- Separation ----
        Equipment(
            id="sep_funnel",
            name="Separatory funnel",
            category="separation",
            description=(
                "Pear / cylindrical glass funnel with a "
                "ground-glass stopper at the top + a "
                "PTFE stopcock at the bottom.  Allows "
                "two immiscible liquids (typically aqueous "
                "+ organic) to be combined, shaken, "
                "separated by gravity, and drawn off "
                "individually — the standard liquid-liquid "
                "extraction tool."
            ),
            typical_uses=(
                "Aqueous work-up of synthetic reactions "
                "(extracting product from water with EtOAc "
                "/ DCM / Et₂O); washing organic phase with "
                "brine / NaHCO₃ / HCl; pH-driven extraction "
                "of basic / acidic compounds"
            ),
            variants=(
                "Sizes 50 / 125 / 250 / 500 / 1000 / 2000 "
                "mL.  PTFE stopcock (default modern) vs "
                "glass stopcock (vintage; needs grease).  "
                "Squibb (pear) shape standard; cylindrical "
                "rare."
            ),
            safety_notes=(
                "ALWAYS vent the funnel through the stopcock "
                "after every shake — pressure build-up "
                "from organic-solvent vapour can pop the "
                "stopper + spray contents.  Hold the stopper "
                "in place while inverting."
            ),
            icon_id="sep_funnel",
            connection_ports=(
                # Top neck takes a stopper (female 24/29).
                ConnectionPort("top", "top",
                               "24/29", False),
                # Stopcock outlet — modelled as a hose port
                # for the typical "drain into a beaker" use.
                _hose("stopcock", "bottom"),
                # Same funnel doubles as an addition funnel
                # when used in `reflux_with_addition` setup
                # — the lower spout pegs into a 3-neck RBF
                # side neck (male 24/29).
                _make_male("24/29", "outlet", "bottom"),
            ),
        ),
        Equipment(
            id="vigreux_column",
            name="Vigreux fractionating column",
            category="separation",
            description=(
                "Long vertical glass column with internal "
                "indentations / spikes that disrupt "
                "vapour flow + force re-condensation.  "
                "Provides 5-15 theoretical plates — enough "
                "to separate components differing by ~25 °C "
                "in boiling point."
            ),
            typical_uses=(
                "Fractional distillation of mixtures with "
                "moderately-different BPs (separating "
                "EtOH/H₂O, hexane/heptane, "
                "EtOAc/CHCl₃); pre-concentration before "
                "more-precise separation"
            ),
            variants=(
                "Lengths 200 / 300 / 400 / 500 mm; "
                "vacuum-jacketed (better insulation, more "
                "plates); 14/20 / 24/29 joints."
            ),
            safety_notes=(
                "Long + thin → fragile.  Clamp at top + "
                "bottom independently.  Adiabatic vacuum-"
                "jacketed columns can implode if dropped."
            ),
            icon_id="vigreux",
            connection_ports=(
                _make_male("24/29", "bottom", "bottom"),
                _make_female("24/29", "top", "top"),
            ),
        ),
        Equipment(
            id="soxhlet_extractor",
            name="Soxhlet extractor",
            category="separation",
            description=(
                "Cyclic-extraction apparatus: solvent "
                "vapour rises through a side tube + "
                "condenses onto a cellulose thimble holding "
                "the solid analyte; condensate fills the "
                "thimble chamber + drains via an automatic "
                "siphon when full, returning extract to the "
                "boiling flask.  Net effect: the analyte "
                "is continuously washed with fresh solvent "
                "for many hours / days."
            ),
            typical_uses=(
                "Extraction of natural products from solid "
                "matrices (alkaloids from leaves, lipids "
                "from seeds); extraction of organics from "
                "soil / sediment for environmental analysis; "
                "any case where 'shake-flask' extraction "
                "won't get all the analyte out"
            ),
            variants=(
                "Sizes (thimble capacity 25 / 50 / 100 / "
                "200 mL); standard joint sizes throughout."
            ),
            safety_notes=(
                "Long unattended runs (overnight) are "
                "common — set up cooling water with a "
                "flow indicator so a water failure doesn't "
                "let solvent vapour escape.  Use the "
                "minimum boiling-flask volume needed."
            ),
            icon_id="soxhlet",
            connection_ports=(
                _make_male("24/29", "bottom", "bottom"),
                _make_female("24/29", "top", "top"),
            ),
        ),

        # ---- Filtration ----
        Equipment(
            id="buchner_funnel",
            name="Büchner funnel",
            category="filtration",
            description=(
                "Porcelain / plastic funnel with a "
                "perforated plate near the top + a stem "
                "that fits into a filter flask.  Filter "
                "paper covers the plate; vacuum draws "
                "liquid through while solid collects on "
                "top.  The standard vacuum-filtration "
                "funnel for crystals + precipitates."
            ),
            typical_uses=(
                "Collecting recrystallised product; "
                "isolating precipitates; removing drying "
                "agents (MgSO₄ / Na₂SO₄) from organic "
                "solutions"
            ),
            variants=(
                "Sizes (60 / 90 / 110 / 150 mm diameter); "
                "porcelain (classic), polypropylene (PP, "
                "acid/base resistant), or borosilicate "
                "glass."
            ),
            safety_notes=(
                "Filter paper MUST be the right diameter "
                "+ wetted before applying vacuum, else "
                "solid leaks around the edges.  Trap the "
                "filtrate flask between the funnel + "
                "vacuum source to protect the pump."
            ),
            icon_id="buchner",
            connection_ports=(
                ConnectionPort("plate", "top",
                               "filter-paper", False),
                ConnectionPort("stem", "bottom",
                               "filter-flask-stopper", True),
            ),
        ),
        Equipment(
            id="hirsch_funnel",
            name="Hirsch funnel",
            category="filtration",
            description=(
                "Like a Büchner funnel but smaller + "
                "tapered (cone-shaped instead of "
                "cylindrical).  Better for filtering "
                "small quantities of solid (mg-g range)."
            ),
            typical_uses=(
                "Microscale recrystallisation collection; "
                "small quantities of precipitate; analytical "
                "collection where a Büchner would lose "
                "sample on the plate"
            ),
            variants=(
                "Sizes (30 / 40 / 50 mm); same materials as "
                "Büchner."
            ),
            safety_notes="Same as Büchner.",
            icon_id="hirsch",
            connection_ports=(
                ConnectionPort("plate", "top",
                               "filter-paper-small", False),
                ConnectionPort("stem", "bottom",
                               "filter-flask-stopper", True),
            ),
        ),
        Equipment(
            id="filter_flask",
            name="Filter / suction flask",
            category="filtration",
            description=(
                "Heavy-walled Erlenmeyer with a side-arm "
                "for vacuum.  The receiver of choice for "
                "Büchner / Hirsch filtration — its thick "
                "walls + heavy base resist vacuum implosion."
            ),
            typical_uses=(
                "Vacuum filtration with Büchner / Hirsch "
                "funnels; rough vacuum reservoir (with a "
                "small Schlenk-line setup); collecting "
                "filtrate from cell-culture work-ups"
            ),
            variants=(
                "Sizes 125 / 250 / 500 / 1000 / 2000 mL; "
                "tubulated side-arm or threaded-port for "
                "vacuum hose."
            ),
            safety_notes=(
                "USE ONLY thick-walled / vacuum-rated "
                "filter flasks — a normal Erlenmeyer can "
                "implode under vacuum.  Inspect for star "
                "cracks before each use."
            ),
            icon_id="filter_flask",
            connection_ports=(
                # Mouth accepts a Büchner / Hirsch funnel via
                # a rubber stopper — joint type matches the
                # funnel stem.
                ConnectionPort("mouth", "top",
                               "filter-flask-stopper", False),
                _hose("vacuum", "side-right"),
            ),
        ),

        # ---- Vacuum ----
        Equipment(
            id="vacuum_pump",
            name="Rotary-vane vacuum pump",
            category="vacuum",
            description=(
                "Oil-sealed rotary pump providing high "
                "vacuum (1-10 mbar typical lab use; "
                "0.1 mbar with two-stage pumps).  Standard "
                "for rotovap reduced-pressure distillation, "
                "vacuum filtration of low-volatile solvents, "
                "Schlenk-line work."
            ),
            typical_uses=(
                "Rotovap (rotary evaporator); vacuum "
                "filtration of high-BP solvents; freeze-"
                "drying; Schlenk-line + glove-box gas "
                "evacuation"
            ),
            variants=(
                "Single-stage (~1 mbar) vs two-stage "
                "(0.01-0.1 mbar); oil-sealed (cheap, "
                "needs trap) vs dry / membrane (no oil "
                "contamination, more expensive, less deep "
                "vacuum)."
            ),
            safety_notes=(
                "ALWAYS install a cold trap between the "
                "system + pump to capture solvent vapours.  "
                "Solvent ingress destroys vacuum oil + "
                "shortens pump life dramatically.  "
                "Replace oil every 6-12 months."
            ),
            icon_id="vacuum_pump",
            connection_ports=(
                _hose("vacuum-in", "back"),
                ConnectionPort("exhaust", "back-low",
                               "exhaust-port", False),
                ConnectionPort("power", "side-right",
                               "socket", False),
            ),
        ),
        Equipment(
            id="aspirator",
            name="Water aspirator (water vacuum)",
            category="vacuum",
            description=(
                "Venturi-effect vacuum source — fast water "
                "flow through a constricted nozzle creates "
                "suction at a side port.  Provides ~20-30 "
                "mbar vacuum (water vapour pressure floor).  "
                "Cheap + simple; standard in undergraduate "
                "teaching labs."
            ),
            typical_uses=(
                "Vacuum filtration; rough vacuum work; "
                "rotovap when no rotary pump is available; "
                "everyday teaching-lab vacuum work"
            ),
            variants=(
                "Plastic / brass / stainless body; some "
                "incorporate a check valve to prevent "
                "back-suction of water on shutdown."
            ),
            safety_notes=(
                "ALWAYS put a vacuum trap between the "
                "system + aspirator — pressure drop on tap "
                "shutoff can siphon water back into your "
                "system + ruin the experiment.  Wastes "
                "tap water (~3-5 L/min) — many institutions "
                "ban or restrict aspirator use for "
                "environmental reasons."
            ),
            icon_id="aspirator",
            connection_ports=(
                _hose("water-in", "top"),
                _hose("water-out", "bottom"),
                _hose("vacuum-port", "side-right"),
            ),
        ),
        Equipment(
            id="vacuum_trap",
            name="Cold-trap vacuum protection",
            category="vacuum",
            description=(
                "Glass cold-finger or vacuum-jacketed bulb "
                "submerged in a dry-ice / liquid-N₂ bath, "
                "placed between the experiment + the vacuum "
                "pump.  Solvent vapour condenses on the "
                "cold surface BEFORE reaching the pump, "
                "protecting it from oil contamination."
            ),
            typical_uses=(
                "Rotovap protection (cold trap on the "
                "vacuum line); Schlenk-line manifold; "
                "any vacuum work involving volatile "
                "solvents"
            ),
            variants=(
                "Cold-finger (in liquid-N₂ Dewar); "
                "vacuum-jacketed cold trap (no Dewar "
                "needed); two-stage cold + cryotraps for "
                "maximum protection."
            ),
            safety_notes=(
                "EMPTY BEFORE / AFTER each use — accumulated "
                "solvent in a cold trap will boil off + "
                "spike the pressure when warmed.  Liquid O₂ "
                "can condense in a liquid-N₂ trap if air "
                "is admitted (oxidiser hazard)."
            ),
            icon_id="vac_trap",
            connection_ports=(
                _hose("system-side", "top-left"),
                _hose("pump-side", "top-right"),
                ConnectionPort("dewar-cradle", "bottom",
                               "dewar-fit", True),
            ),
        ),
        Equipment(
            id="drying_tube",
            name="Drying tube (CaCl₂ / molecular sieves)",
            category="vacuum",
            description=(
                "Cylindrical glass tube packed with a "
                "desiccant (anhydrous CaCl₂ pellets, "
                "molecular sieves, P₂O₅).  Allows pressure "
                "equalisation with the atmosphere while "
                "preventing moisture ingress — the simplest "
                "way to keep a non-Schlenk reaction "
                "moisture-free."
            ),
            typical_uses=(
                "Reflux setups under partially-protected "
                "atmosphere; addition funnel pressure "
                "equalisation; storage of moisture-"
                "sensitive solids; carbonyl reactions where "
                "Schlenk-line setup is overkill"
            ),
            variants=(
                "U-shaped (can hold liquid drying agent "
                "like H₂SO₄); straight-tube (most common); "
                "with / without ground-glass joint (slip-"
                "on rubber tubing for joint-less)."
            ),
            safety_notes=(
                "Replace desiccant at the first sign of "
                "colour change / clumping (CaCl₂ goes "
                "deliquescent).  Don't use H₂SO₄ "
                "drying-tubes near amines / alcohols — "
                "violent acid-base reaction risk."
            ),
            icon_id="drying_tube",
            connection_ports=(
                _make_male("24/29", "bottom", "bottom"),
                ConnectionPort("top", "top",
                               "open", False),
            ),
        ),

        # ---- Stirring ----
        Equipment(
            id="stir_bar",
            name="Magnetic stir bar",
            category="stirring",
            description=(
                "PTFE-coated magnet placed inside the "
                "reaction vessel.  Spins when driven by the "
                "rotating magnetic field of a stirrer-"
                "hotplate underneath.  The standard small-"
                "to-medium-scale mixing solution."
            ),
            typical_uses=(
                "Routine mixing of reactions in flasks ≤ "
                "1 L; dissolution + crystallisation; "
                "titration mixing; anywhere shaking by hand "
                "would be too slow / inconsistent"
            ),
            variants=(
                "Octagonal (most common, plain bottom); "
                "egg-shaped / cylindrical; cross / triangle; "
                "with retrievable PTFE-coated steel ring on "
                "top.  Lengths 5-50 mm.  PTFE-coated AlNiCo "
                "for high-temperature work."
            ),
            safety_notes=(
                "Stir-bar bouncing at very high RPM can "
                "crack RBF bottoms — start at low RPM + "
                "ramp up.  Retrieve with a stir-bar "
                "magnet on a stick, NOT pliers."
            ),
            icon_id="stir_bar",
            connection_ports=(
                ConnectionPort("body", "inside-flask",
                               "in-flask", False),
            ),
        ),
        Equipment(
            id="overhead_stirrer",
            name="Mechanical overhead stirrer",
            category="stirring",
            description=(
                "Motor + shaft + impeller blade lowered "
                "into a wide-mouth flask.  Used for "
                "viscous / large-volume mixtures where a "
                "magnetic stir bar can't keep up.  Standard "
                "for slurries, polymerisations, > 2 L "
                "volumes."
            ),
            typical_uses=(
                "Polymerisation reactions; slurries / "
                "thick suspensions; > 2 L scale work; "
                "anaerobic / Schlenk reactions through a "
                "septum-equipped 3-neck RBF"
            ),
            variants=(
                "Glass / PTFE / stainless-steel impeller; "
                "anchor / paddle / propeller blade shapes; "
                "up to 2000 RPM; some include direct "
                "torque + temperature sensors."
            ),
            safety_notes=(
                "Ensure the impeller doesn't touch the "
                "flask wall (cracking / wobble risk).  "
                "Long-running mechanical stirrers heat the "
                "shaft from friction — note when "
                "performing temperature-sensitive work."
            ),
            icon_id="overhead_stirrer",
            connection_ports=(
                ConnectionPort("shaft", "bottom",
                               "stirrer-shaft", True),
                ConnectionPort("power", "back-right",
                               "socket", False),
            ),
        ),

        # ---- Support ----
        Equipment(
            id="ring_stand",
            name="Ring stand (lab stand)",
            category="support",
            description=(
                "Vertical metal rod on a heavy base.  "
                "Holds clamps that grip glassware.  The "
                "skeletal foundation of every lab setup."
            ),
            typical_uses=(
                "Holding RBFs / condensers / sep funnels / "
                "burettes — anywhere glassware needs to be "
                "held in place above the bench"
            ),
            variants=(
                "Rod heights 24 / 36 / 48 inches; base "
                "weights 4-12 lb; with or without "
                "magnetic-base option."
            ),
            safety_notes=(
                "Heavy base prevents tipping — but a "
                "tall stand carrying a heavy flask becomes "
                "unstable.  Centre the load over the base."
            ),
            icon_id="ring_stand",
            connection_ports=(
                ConnectionPort("rod", "side",
                               "rod", False),
            ),
        ),
        Equipment(
            id="clamp_3prong",
            name="Three-prong clamp",
            category="support",
            description=(
                "Spring-loaded clamp with three rubber-"
                "lined fingers that grips a flask neck "
                "or a column securely.  The standard "
                "all-purpose lab clamp."
            ),
            typical_uses=(
                "Clamping RBF necks; supporting "
                "condensers; holding distillation columns; "
                "securing sep funnels"
            ),
            variants=(
                "Open-faced (3 fingers, 2 in front); "
                "closed (4 fingers, full encirclement); "
                "swivel-head; aluminium / steel."
            ),
            safety_notes=(
                "Tighten enough to grip but NOT enough to "
                "crack the glass.  Replace cracked rubber "
                "tips before they leave glass-on-metal "
                "contact."
            ),
            icon_id="clamp",
            connection_ports=(
                # Clamp jaws are a mechanical grip, not a
                # ground-glass joint — modelled as `open` so
                # the validator doesn't enforce port-sex
                # complementarity (the clamp can grip any
                # tubular glass piece).
                ConnectionPort("jaws", "front",
                               "open", False),
                ConnectionPort("boss", "back",
                               "rod", True),
            ),
        ),
        Equipment(
            id="keck_clip",
            name="Keck clip (joint clip)",
            category="support",
            description=(
                "Plastic spring clip that snaps over a "
                "ground-glass joint, mechanically locking "
                "the male + female pieces together.  "
                "Prevents accidental separation during "
                "stirring + heating."
            ),
            typical_uses=(
                "Securing every ground-glass joint in a "
                "multi-piece setup; standard practice in "
                "modern synthetic labs (replaces the "
                "older grease-only seal)"
            ),
            variants=(
                "Sized to match joint sizes (#13 = 14/20, "
                "#19 = 19/22, #22 = 24/29, #27 = 29/32).  "
                "Colour-coded by size in modern brands.  "
                "Plastic (cheap) vs metal (high-temperature)."
            ),
            safety_notes=(
                "Plastic Keck clips melt above ~140 °C — "
                "use metal at high temperatures.  Don't "
                "rely on Keck clips alone for vacuum work; "
                "still grease the joint."
            ),
            icon_id="keck",
            connection_ports=(
                ConnectionPort("joint", "center",
                               "glass-joint", False),
            ),
        ),
        Equipment(
            id="cork_ring",
            name="Cork ring (RBF support)",
            category="support",
            description=(
                "Round / rectangular cork base with a "
                "circular depression matched to an RBF "
                "size.  Lets a round-bottom flask sit "
                "stably on the bench when not clamped."
            ),
            typical_uses=(
                "Setting an RBF down between operations; "
                "tare on a balance; transferring an RBF "
                "from a heating mantle to a cooling bath"
            ),
            variants=(
                "Sized to match RBF volumes; some variants "
                "include a notch for the neck to clear."
            ),
            safety_notes=(
                "Cork burns — never put a cork ring on a "
                "hot surface.  Replace any cork ring "
                "showing solvent damage / charring."
            ),
            icon_id="cork_ring",
            connection_ports=(
                ConnectionPort("cradle", "top",
                               "rbf-shell", False),
            ),
        ),

        # ---- Safety ----
        Equipment(
            id="fume_hood",
            name="Fume hood",
            category="safety",
            description=(
                "Enclosed bench with an exhaust fan that "
                "draws air + chemical vapours up + away "
                "from the chemist.  Airflow specification "
                "is typically 0.4-0.5 m/s face velocity at "
                "the sash opening.  Mandatory for any work "
                "with toxic / flammable / corrosive vapours."
            ),
            typical_uses=(
                "ALL synthetic chemistry involving organic "
                "solvents; concentrated acid / base work; "
                "toxic-gas reactions (SO₂, Cl₂, HCN); "
                "ozonolysis; any reaction that smells"
            ),
            variants=(
                "Conventional (constant-flow), VAV "
                "(variable-air-volume — adjusts flow as "
                "sash moves), ductless (filter, doesn't "
                "vent outside, limited solvent compatibility)."
            ),
            safety_notes=(
                "Sash height is the safety knob — keep at "
                "or below the labeled stop for adequate "
                "containment.  Don't store reagent bottles "
                "inside the hood (blocks airflow + "
                "contamination); use a dedicated reagent "
                "shelf."
            ),
            icon_id="fume_hood",
            connection_ports=(
                ConnectionPort("workspace", "front",
                               "open-bench", False),
                ConnectionPort("services", "back",
                               "gas-water-vacuum", False),
            ),
        ),
        Equipment(
            id="thermometer",
            name="Thermometer (mercury / digital)",
            category="safety",
            description=(
                "Glass tube with a mercury / dyed-alcohol "
                "column OR a digital probe with a "
                "thermocouple tip.  Reads reaction or "
                "vapour temperature.  Mandatory for any "
                "controlled-temperature work."
            ),
            typical_uses=(
                "Vapour-temperature monitoring in "
                "distillation; reaction temperature in "
                "reflux + addition; oil-bath temperature "
                "control; melting-point determination "
                "(in the dedicated apparatus)"
            ),
            variants=(
                "Mercury-in-glass (-10 to 250 / 360 °C); "
                "alcohol-in-glass (-50 to 100 °C, safer "
                "for low-T work); digital thermocouple "
                "(K / J / T types, range -200 to 1000+ °C); "
                "RTD probes (high precision, ±0.1 °C)."
            ),
            safety_notes=(
                "Mercury thermometers are increasingly "
                "banned in undergraduate labs (Hg spill = "
                "hazardous-waste event); switch to alcohol "
                "or digital where possible.  ALWAYS check "
                "for cracks before use."
            ),
            icon_id="thermometer",
            connection_ports=(
                # Stem slides into a thermometer adapter's
                # rubber / Teflon sleeve (male peg, sleeve =
                # socket).  Joint type matches the adapter's
                # `therm-sleeve` port.
                ConnectionPort("stem", "bottom",
                               "thermometer-sleeve", True),
            ),
        ),

        # ---- Analytical (cross-references to Phase 37 dialogs) ----
        Equipment(
            id="melting_point",
            name="Melting-point apparatus",
            category="analytical",
            description=(
                "Heated stage with a magnifier + "
                "thermometer.  Holds a sealed capillary "
                "tube containing a tiny amount of "
                "crystalline sample; user watches for the "
                "melt + records the temperature range.  "
                "Quick purity / identity check for solid "
                "compounds."
            ),
            typical_uses=(
                "Quick identity confirmation of a "
                "synthetic intermediate or product; "
                "purity assessment (sharp narrow melt = "
                "pure; broad melt or low-T melt = impure); "
                "comparison with literature MP values"
            ),
            variants=(
                "Manual capillary (Thiele tube — old-school, "
                "still common); Mel-Temp / Buchi (electric "
                "block + magnifier); fully-automated digital "
                "(camera-based melt detection)."
            ),
            safety_notes=(
                "Sample loaded into a thin-walled "
                "capillary — handle with care to avoid "
                "punctures / crushing."
            ),
            icon_id="melting_point",
            connection_ports=(
                ConnectionPort("capillary-slot", "top",
                               "MP-capillary", False),
                ConnectionPort("power", "back",
                               "socket", False),
            ),
        ),
    ]


_EQUIPMENT: List[Equipment] = _build_catalogue()


# ------------------------------------------------------------------
# Public lookup helpers
# ------------------------------------------------------------------

def list_equipment(category: Optional[str] = None
                   ) -> List[Equipment]:
    if category is None:
        return list(_EQUIPMENT)
    if category not in VALID_CATEGORIES:
        return []
    return [e for e in _EQUIPMENT if e.category == category]


def get_equipment(equipment_id: str) -> Optional[Equipment]:
    for e in _EQUIPMENT:
        if e.id == equipment_id:
            return e
    return None


def find_equipment(needle: str) -> List[Equipment]:
    """Case-insensitive substring search across id + name +
    category."""
    if not needle:
        return []
    n = needle.lower().strip()
    out: List[Equipment] = []
    for e in _EQUIPMENT:
        if (n in e.id.lower()
                or n in e.name.lower()
                or n in e.category.lower()):
            out.append(e)
    return out


def categories() -> List[str]:
    return list(VALID_CATEGORIES)


def to_dict(e: Equipment) -> Dict[str, object]:
    return {
        "id": e.id,
        "name": e.name,
        "category": e.category,
        "description": e.description,
        "typical_uses": e.typical_uses,
        "variants": e.variants,
        "safety_notes": e.safety_notes,
        "icon_id": e.icon_id,
        "connection_ports": [
            {
                "name": p.name,
                "location": p.location,
                "joint_type": p.joint_type,
                "is_male": p.is_male,
            } for p in e.connection_ports
        ],
    }
