"""Phase 41 (round 144) — centrifugation reference catalogue +
g↔rpm calculator.

Three frozen dataclasses:

- :class:`Centrifuge` — instrument-class entry (microfuge,
  benchtop, high-speed, ultracentrifuge, refrigerated).
- :class:`Rotor` — rotor type entry with the radius the
  g↔rpm calculator needs.
- :class:`Application` — protocol entry (differential
  centrifugation, density-gradient, subcellular fractionation,
  etc.) with recommended speeds + durations.

Headless solvers:

- :func:`rpm_to_g` / :func:`g_to_rpm` — closed-form using
  ``g = 1.118e-5 · RPM² · r`` (r in cm, the rotor's max
  radius from the rotor entry).

Reference data only — no centrifuge actually spins.  The
calculator + reference catalogue together are the most-used
bench tool for any wet-lab worker who's ever asked *"what
RPM is 13 000 × g on this rotor?"*.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


# ------------------------------------------------------------------
# Constant + closed-form solvers
# ------------------------------------------------------------------

#: Conversion constant for the canonical g↔rpm formula
#: (g = K · RPM² · r where r is in cm; K = 1.118e-5).  Derived
#: from g = ω²·r / 9.80665 with ω in rad/s and 1 RPM = 2π/60
#: rad/s; matches every Beckman / Eppendorf / Sorvall data
#: sheet.
G_FORCE_CONSTANT: float = 1.118e-5


def rpm_to_g(rpm: float, radius_cm: float) -> Dict[str, float]:
    """Convert RPM + rotor radius (cm) to relative centrifugal
    force (× g).  Returns ``{rpm, radius_cm, g_force}``."""
    if rpm <= 0:
        raise ValueError(f"rpm must be > 0; got {rpm!r}.")
    if radius_cm <= 0:
        raise ValueError(
            f"radius_cm must be > 0; got {radius_cm!r}.")
    g_force = G_FORCE_CONSTANT * rpm * rpm * radius_cm
    return {
        "rpm": rpm,
        "radius_cm": radius_cm,
        "g_force": g_force,
    }


def g_to_rpm(g_force: float, radius_cm: float) -> Dict[str, float]:
    """Inverse: given target × g + rotor radius, return the
    required RPM.  Returns ``{rpm, radius_cm, g_force}``."""
    if g_force <= 0:
        raise ValueError(f"g_force must be > 0; got {g_force!r}.")
    if radius_cm <= 0:
        raise ValueError(
            f"radius_cm must be > 0; got {radius_cm!r}.")
    rpm = (g_force / (G_FORCE_CONSTANT * radius_cm)) ** 0.5
    return {
        "rpm": rpm,
        "radius_cm": radius_cm,
        "g_force": g_force,
    }


# ------------------------------------------------------------------
# Catalogue dataclasses
# ------------------------------------------------------------------

@dataclass(frozen=True)
class Centrifuge:
    id: str
    name: str
    manufacturer: str
    centrifuge_class: str    # microfuge / benchtop / high-speed /
                             # ultracentrifuge
    max_speed_rpm: int
    max_g_force: int
    typical_capacity: str
    refrigerated: bool
    typical_uses: str
    notes: str = ""


@dataclass(frozen=True)
class Rotor:
    id: str
    name: str
    rotor_type: str          # fixed-angle / swinging-bucket /
                             # vertical / continuous-flow
    max_radius_cm: float     # used by the g↔rpm calculator
    min_radius_cm: float     # for swinging-bucket rotors with
                             # variable radius (max with arms
                             # extended)
    max_speed_rpm: int
    typical_tubes: str
    notes: str = ""


@dataclass(frozen=True)
class Application:
    id: str
    name: str
    protocol_class: str      # differential / density-gradient /
                             # cell-pellet / protein-concentration
    recommended_g_force: str
    recommended_duration: str
    recommended_rotor_type: str
    description: str
    notes: str = ""


VALID_CENTRIFUGE_CLASSES: tuple = (
    "microfuge", "benchtop", "high-speed", "ultracentrifuge",
)

VALID_ROTOR_TYPES: tuple = (
    "fixed-angle", "swinging-bucket", "vertical",
    "continuous-flow",
)

VALID_PROTOCOL_CLASSES: tuple = (
    "differential", "density-gradient",
    "cell-pellet", "protein-concentration",
)


# ------------------------------------------------------------------
# Catalogue
# ------------------------------------------------------------------

def _build_centrifuges() -> List[Centrifuge]:
    return [
        Centrifuge(
            id="microfuge_5424",
            name="Eppendorf 5424",
            manufacturer="Eppendorf",
            centrifuge_class="microfuge",
            max_speed_rpm=15000,
            max_g_force=21130,
            typical_capacity="24 × 1.5/2.0 mL tubes",
            refrigerated=False,
            typical_uses=(
                "Daily benchtop spins of 1.5/2.0 mL tubes — "
                "DNA/RNA prep, protein-precipitation pellets, "
                "PCR clean-up.  The ubiquitous benchtop "
                "microfuge."
            ),
            notes=(
                "5424R variant adds refrigeration (-9 to "
                "+40 °C); essential for RNA / enzyme work."
            ),
        ),
        Centrifuge(
            id="microfuge_5425",
            name="Eppendorf 5425",
            manufacturer="Eppendorf",
            centrifuge_class="microfuge",
            max_speed_rpm=21300,
            max_g_force=21300,
            typical_capacity="24 × 1.5/2.0 mL tubes",
            refrigerated=False,
            typical_uses=(
                "Updated successor to the 5424; small, "
                "quiet, fast acceleration.  Same use case "
                "as 5424."
            ),
        ),
        Centrifuge(
            id="benchtop_5810",
            name="Eppendorf 5810/5810R",
            manufacturer="Eppendorf",
            centrifuge_class="benchtop",
            max_speed_rpm=14000,
            max_g_force=20800,
            typical_capacity="4 × 250 mL or 4 × 100 conical",
            refrigerated=True,
            typical_uses=(
                "Standard tissue-culture / molecular-biology "
                "benchtop centrifuge — pelleting cells from "
                "50 mL conicals, large-scale protein "
                "preps, plate-format spins (4 × 96-well)."
            ),
            notes=(
                "5810R = refrigerated version; the lab "
                "default for routine cell-pelleting at "
                "200-1000 × g."
            ),
        ),
        Centrifuge(
            id="benchtop_5910",
            name="Eppendorf 5910 Ri",
            manufacturer="Eppendorf",
            centrifuge_class="benchtop",
            max_speed_rpm=15000,
            max_g_force=24328,
            typical_capacity="4 × 750 mL or 28 × 50 mL",
            refrigerated=True,
            typical_uses=(
                "High-capacity refrigerated benchtop — "
                "the workhorse for clinical-lab workflows + "
                "blood-bag processing."
            ),
        ),
        Centrifuge(
            id="benchtop_allegra",
            name="Beckman Allegra X-15R",
            manufacturer="Beckman Coulter",
            centrifuge_class="benchtop",
            max_speed_rpm=15300,
            max_g_force=27200,
            typical_capacity="4 × 750 mL",
            refrigerated=True,
            typical_uses=(
                "Direct competitor to the Eppendorf 5810R; "
                "refrigerated benchtop, common in clinical "
                "+ academic labs."
            ),
        ),
        Centrifuge(
            id="hispeed_avanti",
            name="Beckman Avanti J-26 XPI",
            manufacturer="Beckman Coulter",
            centrifuge_class="high-speed",
            max_speed_rpm=26000,
            max_g_force=98300,
            typical_capacity="6 × 500 mL or 6 × 250 mL",
            refrigerated=True,
            typical_uses=(
                "High-speed protein purification (collecting "
                "membrane fractions, viral particles, "
                "inclusion bodies); large-volume bacterial "
                "harvests; the workhorse between benchtop + "
                "ultracentrifuge."
            ),
            notes=(
                "Avanti J-30I extends max RPM to 30 000; "
                "JE-5.0 elutriator adapter for cell-size "
                "fractionation."
            ),
        ),
        Centrifuge(
            id="hispeed_sorvall_rc6",
            name="Sorvall RC-6 Plus",
            manufacturer="Thermo Fisher",
            centrifuge_class="high-speed",
            max_speed_rpm=22000,
            max_g_force=55200,
            typical_capacity="6 × 500 mL or 8 × 250 mL",
            refrigerated=True,
            typical_uses=(
                "Workhorse high-speed in protein-prep + "
                "lentivirus production labs.  Direct competitor "
                "to the Beckman Avanti."
            ),
        ),
        Centrifuge(
            id="ultra_optima_xpn",
            name="Beckman Optima XPN",
            manufacturer="Beckman Coulter",
            centrifuge_class="ultracentrifuge",
            max_speed_rpm=100000,
            max_g_force=802000,
            typical_capacity="6 × 38.5 mL (swinging) / "
                             "12 × 13.5 mL (fixed-angle)",
            refrigerated=True,
            typical_uses=(
                "Ultracentrifugation: density-gradient "
                "separation (sucrose / CsCl / Percoll / "
                "Nycodenz), microsome / ribosome / virus "
                "isolation, exosome purification, plasmid "
                "midi-/maxi-prep CsCl banding."
            ),
            notes=(
                "Vacuum-jacketed chamber to prevent rotor "
                "heating from air friction at high RPM.  "
                "Most expensive class of standard lab "
                "centrifuge ($150-300k+)."
            ),
        ),
        Centrifuge(
            id="ultra_sorvall_wx100",
            name="Sorvall WX 100",
            manufacturer="Thermo Fisher",
            centrifuge_class="ultracentrifuge",
            max_speed_rpm=100000,
            max_g_force=802000,
            typical_capacity="6 × 38.5 mL (swinging) / "
                             "12 × 13.5 mL (fixed-angle)",
            refrigerated=True,
            typical_uses=(
                "Direct competitor to the Beckman Optima; "
                "same applications + capacity range."
            ),
        ),
    ]


def _build_rotors() -> List[Rotor]:
    return [
        # ---- Microfuge rotors ----
        Rotor(
            id="rotor_fa_45_24_11",
            name="Eppendorf FA-45-24-11",
            rotor_type="fixed-angle",
            max_radius_cm=8.4,
            min_radius_cm=8.4,
            max_speed_rpm=21300,
            typical_tubes="24 × 1.5/2.0 mL",
            notes=(
                "Standard fixed-angle rotor for the Eppendorf "
                "5424/5425 microfuges.  21 130 × g max."
            ),
        ),
        # ---- Benchtop rotors ----
        Rotor(
            id="rotor_a_4_81",
            name="Eppendorf A-4-81",
            rotor_type="swinging-bucket",
            max_radius_cm=18.7,
            min_radius_cm=11.0,
            max_speed_rpm=4000,
            typical_tubes="4 × 750 mL",
            notes=(
                "Workhorse swinging-bucket for the Eppendorf "
                "5810/5910.  Buckets swing out to horizontal "
                "during run; max radius is the 'arms out' "
                "value."
            ),
        ),
        Rotor(
            id="rotor_fa_45_30_11",
            name="Eppendorf FA-45-30-11",
            rotor_type="fixed-angle",
            max_radius_cm=10.2,
            min_radius_cm=10.2,
            max_speed_rpm=14000,
            typical_tubes="30 × 1.5/2.0 mL",
            notes=(
                "Higher-throughput microfuge-style rotor for "
                "the 5810/5910 — runs the same small tubes "
                "as a microfuge but takes 30 instead of 24."
            ),
        ),
        # ---- High-speed rotors ----
        Rotor(
            id="rotor_ja_25_50",
            name="Beckman JA-25.50",
            rotor_type="fixed-angle",
            max_radius_cm=10.85,
            min_radius_cm=10.85,
            max_speed_rpm=25000,
            typical_tubes="8 × 50 mL",
            notes=(
                "Standard high-speed fixed-angle rotor for "
                "the Beckman Avanti J-26.  75 600 × g max."
            ),
        ),
        Rotor(
            id="rotor_ja_10",
            name="Beckman JA-10",
            rotor_type="fixed-angle",
            max_radius_cm=15.8,
            min_radius_cm=15.8,
            max_speed_rpm=10000,
            typical_tubes="6 × 500 mL",
            notes=(
                "High-volume fixed-angle for harvesting "
                "bacterial cultures + large protein preps.  "
                "17 700 × g max."
            ),
        ),
        Rotor(
            id="rotor_jla_8_1000",
            name="Beckman JLA-8.1000",
            rotor_type="fixed-angle",
            max_radius_cm=13.7,
            min_radius_cm=13.7,
            max_speed_rpm=8000,
            typical_tubes="6 × 1000 mL",
            notes=(
                "Largest standard high-speed fixed-angle.  "
                "Used for fermenter harvests (10 L+ bacterial "
                "cultures into 6 × 1 L bottles)."
            ),
        ),
        # ---- Ultracentrifuge rotors ----
        Rotor(
            id="rotor_ti_70",
            name="Beckman Ti-70",
            rotor_type="fixed-angle",
            max_radius_cm=8.2,
            min_radius_cm=8.2,
            max_speed_rpm=70000,
            typical_tubes="8 × 39 mL",
            notes=(
                "Standard ultracentrifuge fixed-angle for "
                "Beckman Optima.  450 000 × g max — "
                "microsome / membrane / virus pellets."
            ),
        ),
        Rotor(
            id="rotor_sw_41_ti",
            name="Beckman SW 41 Ti",
            rotor_type="swinging-bucket",
            max_radius_cm=15.3,
            min_radius_cm=6.7,
            max_speed_rpm=41000,
            typical_tubes="6 × 13.2 mL",
            notes=(
                "Swinging-bucket ultracentrifuge rotor for "
                "density-gradient work (sucrose, CsCl, "
                "Percoll).  287 000 × g max.  The standard "
                "polysome / mRNP gradient rotor."
            ),
        ),
        Rotor(
            id="rotor_tla_100",
            name="Beckman TLA-100",
            rotor_type="fixed-angle",
            max_radius_cm=3.5,
            min_radius_cm=3.5,
            max_speed_rpm=100000,
            typical_tubes="20 × 0.2 mL",
            notes=(
                "Smallest / fastest tabletop-ultracentrifuge "
                "rotor (Beckman Optima Max).  390 000 × g "
                "max — exosome / micro-vesicle isolation."
            ),
        ),
        Rotor(
            id="rotor_vti_50",
            name="Beckman VTi 50",
            rotor_type="vertical",
            max_radius_cm=8.7,
            min_radius_cm=4.2,
            max_speed_rpm=50000,
            typical_tubes="8 × 39 mL",
            notes=(
                "Vertical-tube rotor for fast isopycnic "
                "(equilibrium) gradients.  CsCl plasmid "
                "midi-prep is the canonical application — "
                "shorter run time than a swinging-bucket "
                "for the same separation."
            ),
        ),
    ]


def _build_applications() -> List[Application]:
    return [
        Application(
            id="cell_pellet_mammalian",
            name="Pellet mammalian cells",
            protocol_class="cell-pellet",
            recommended_g_force="200-300 × g",
            recommended_duration="5 min",
            recommended_rotor_type="swinging-bucket",
            description=(
                "Gently pellet adherent or suspension "
                "mammalian cells without lysing.  Higher g "
                "(>500) pelts the membrane = lysis = "
                "intracellular contamination of the "
                "supernatant."
            ),
            notes=(
                "Brake set to LOW to avoid resuspending the "
                "loose pellet on deceleration."
            ),
        ),
        Application(
            id="cell_pellet_ecoli",
            name="Harvest E. coli culture",
            protocol_class="cell-pellet",
            recommended_g_force="5 000 × g",
            recommended_duration="5-10 min",
            recommended_rotor_type="fixed-angle",
            description=(
                "Pellet bacterial cells from overnight LB "
                "culture for protein preps + plasmid prep "
                "starting material."
            ),
            notes=(
                "Brake on full — bacterial pellet is dense + "
                "doesn't resuspend on deceleration.  500 mL "
                "centrifuge bottles + JLA-8.1000 for "
                "fermenter harvests."
            ),
        ),
        Application(
            id="differential_organelle",
            name="Differential centrifugation (organelles)",
            protocol_class="differential",
            recommended_g_force=(
                "Sequential: 600 × g (nuclei) → 7 000 × g "
                "(mitochondria) → 100 000 × g (microsomes)"
            ),
            recommended_duration="10 / 10 / 60 min",
            recommended_rotor_type="fixed-angle (each stage)",
            description=(
                "Classical subcellular fractionation by "
                "stepped pelleting.  Each pellet contains "
                "the heavier organelles up to that step's "
                "g-force; the supernatant is then re-spun "
                "at higher g to pellet the next organelle "
                "class."
            ),
            notes=(
                "100 000 × g step requires an "
                "ultracentrifuge (Ti-70 in the Beckman "
                "Optima at ~40 000 RPM)."
            ),
        ),
        Application(
            id="density_gradient_sucrose",
            name="Sucrose density-gradient (polysomes / mRNP)",
            protocol_class="density-gradient",
            recommended_g_force="200 000 × g",
            recommended_duration="2-3 hours",
            recommended_rotor_type="swinging-bucket",
            description=(
                "Continuous or stepped sucrose gradient "
                "(typically 10-50 % w/v) in an SW 41 Ti — "
                "separates ribosomes (40S / 60S / 80S / "
                "polysomes) by sedimentation rate.  The "
                "RNA-biology workhorse."
            ),
        ),
        Application(
            id="density_gradient_cscl_plasmid",
            name="CsCl plasmid prep (isopycnic)",
            protocol_class="density-gradient",
            recommended_g_force="350 000 × g",
            recommended_duration="16-20 hours",
            recommended_rotor_type="vertical",
            description=(
                "Equilibrium (isopycnic) CsCl + "
                "ethidium-bromide gradient in a VTi 50 "
                "vertical rotor.  Plasmid DNA bands at "
                "1.55 g/mL; chromosomal DNA at 1.71 g/mL.  "
                "The pre-kit gold standard for "
                "endotoxin-free plasmid."
            ),
            notes=(
                "Mostly displaced by silica-column kits "
                "for routine work, but CsCl is still the "
                "best for absolute purity (cell-line "
                "transfection, gene therapy)."
            ),
        ),
        Application(
            id="protein_concentration_amicon",
            name="Amicon centrifugal filter",
            protocol_class="protein-concentration",
            recommended_g_force=(
                "4 000 × g (swinging-bucket) or "
                "7 500 × g (fixed-angle)"
            ),
            recommended_duration="10-30 min",
            recommended_rotor_type=(
                "swinging-bucket OR fixed-angle "
                "(check Amicon manual)"
            ),
            description=(
                "Concentrate dilute protein samples through "
                "a molecular-weight-cutoff (MWCO) ultrafiltration "
                "membrane — e.g. Amicon Ultra 10K cuts off "
                "everything < 10 kDa.  Buffer-exchange + "
                "concentrate in one step."
            ),
            notes=(
                "Maximum g-force is filter-specific; over-"
                "spinning damages the membrane.  Pre-rinse "
                "with buffer to remove glycerol storage "
                "additive."
            ),
        ),
        Application(
            id="exosome_isolation",
            name="Exosome isolation",
            protocol_class="differential",
            recommended_g_force=(
                "Sequential: 300 × g (cells) → 2 000 × g "
                "(debris) → 10 000 × g (large vesicles) → "
                "100 000 × g (exosomes)"
            ),
            recommended_duration="10 / 10 / 30 / 70 min",
            recommended_rotor_type="fixed-angle (each stage)",
            description=(
                "Differential ultracentrifugation protocol "
                "for isolating exosomes (~30-150 nm) from "
                "cell-culture supernatant or biofluids.  "
                "Final 100 000 × g step requires an "
                "ultracentrifuge."
            ),
            notes=(
                "Density-gradient purification (sucrose / "
                "iodixanol) often follows the differential "
                "protocol to separate exosomes from "
                "microvesicles + protein aggregates."
            ),
        ),
        Application(
            id="serum_separation",
            name="Serum separation from clotted blood",
            protocol_class="cell-pellet",
            recommended_g_force="1 500 × g",
            recommended_duration="10 min",
            recommended_rotor_type="swinging-bucket",
            description=(
                "Standard clinical-lab serum-prep step — "
                "centrifuge a clotted SST tube to pellet "
                "the clot + cells, leaving clear serum on "
                "top for downstream chemistry / immunoassay "
                "panels."
            ),
            notes=(
                "Plasma (anticoagulated EDTA / heparin tube) "
                "uses the same g-force + duration but no "
                "clot forms; the pellet is just the cellular "
                "components."
            ),
        ),
    ]


_CENTRIFUGES: List[Centrifuge] = _build_centrifuges()
_ROTORS: List[Rotor] = _build_rotors()
_APPLICATIONS: List[Application] = _build_applications()


# ------------------------------------------------------------------
# Public lookup helpers
# ------------------------------------------------------------------

def list_centrifuges(centrifuge_class: Optional[str] = None
                     ) -> List[Centrifuge]:
    if centrifuge_class is None:
        return list(_CENTRIFUGES)
    if centrifuge_class not in VALID_CENTRIFUGE_CLASSES:
        return []
    return [c for c in _CENTRIFUGES
            if c.centrifuge_class == centrifuge_class]


def get_centrifuge(centrifuge_id: str) -> Optional[Centrifuge]:
    for c in _CENTRIFUGES:
        if c.id == centrifuge_id:
            return c
    return None


def list_rotors(rotor_type: Optional[str] = None) -> List[Rotor]:
    if rotor_type is None:
        return list(_ROTORS)
    if rotor_type not in VALID_ROTOR_TYPES:
        return []
    return [r for r in _ROTORS if r.rotor_type == rotor_type]


def get_rotor(rotor_id: str) -> Optional[Rotor]:
    for r in _ROTORS:
        if r.id == rotor_id:
            return r
    return None


def list_applications(protocol_class: Optional[str] = None
                      ) -> List[Application]:
    if protocol_class is None:
        return list(_APPLICATIONS)
    if protocol_class not in VALID_PROTOCOL_CLASSES:
        return []
    return [a for a in _APPLICATIONS
            if a.protocol_class == protocol_class]


def get_application(app_id: str) -> Optional[Application]:
    for a in _APPLICATIONS:
        if a.id == app_id:
            return a
    return None


def find_centrifuges(needle: str) -> List[Centrifuge]:
    if not needle:
        return []
    n = needle.lower().strip()
    return [c for c in _CENTRIFUGES
            if n in c.id.lower() or n in c.name.lower()
            or n in c.manufacturer.lower()
            or n in c.centrifuge_class.lower()]


def centrifuge_to_dict(c: Centrifuge) -> Dict[str, object]:
    return {
        "id": c.id, "name": c.name,
        "manufacturer": c.manufacturer,
        "centrifuge_class": c.centrifuge_class,
        "max_speed_rpm": c.max_speed_rpm,
        "max_g_force": c.max_g_force,
        "typical_capacity": c.typical_capacity,
        "refrigerated": c.refrigerated,
        "typical_uses": c.typical_uses,
        "notes": c.notes,
    }


def rotor_to_dict(r: Rotor) -> Dict[str, object]:
    return {
        "id": r.id, "name": r.name,
        "rotor_type": r.rotor_type,
        "max_radius_cm": r.max_radius_cm,
        "min_radius_cm": r.min_radius_cm,
        "max_speed_rpm": r.max_speed_rpm,
        "typical_tubes": r.typical_tubes,
        "notes": r.notes,
    }


def application_to_dict(a: Application) -> Dict[str, object]:
    return {
        "id": a.id, "name": a.name,
        "protocol_class": a.protocol_class,
        "recommended_g_force": a.recommended_g_force,
        "recommended_duration": a.recommended_duration,
        "recommended_rotor_type": a.recommended_rotor_type,
        "description": a.description,
        "notes": a.notes,
    }
