"""Phase 37a (round 136) — qualitative inorganic-test catalogue.

Headless reference data for the *Tools → Qualitative inorganic
tests…* dialog.  Each entry describes a wet-lab procedure that
identifies a single ion or gas: the reagents, the procedure
(short — one or two sentences), the positive observation
(colour + state), and any common interferences or follow-up
tests.

Categories
----------
- ``"flame"`` — flame test for cations (Na⁺, K⁺, Ca²⁺, …).
- ``"hydroxide"`` — NaOH precipitation test for cations.
- ``"halide"`` — AgNO₃ / HNO₃ test for halide anions.
- ``"sulfate"`` — BaCl₂ / acid test for SO₄²⁻.
- ``"carbonate"`` — dilute-acid test for CO₃²⁻ / HCO₃⁻.
- ``"ammonium"`` — NaOH + heat test for NH₄⁺.
- ``"gas"`` — common gas-identification tests.

The ``colour_hex`` field on each entry is the colour of the
characteristic observation (flame colour, precipitate colour,
gas colour) and is used by the Phase-37a dialog as a
side-by-side colour swatch.  ``"#FFFFFF"`` is the catalogue
default for white precipitates / colourless gases /
non-visual observations.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass(frozen=True)
class InorganicTest:
    id: str
    name: str
    category: str          # see module docstring
    target: str            # e.g. "Na⁺", "Cu²⁺", "Cl⁻", "H₂"
    target_class: str      # "cation" / "anion" / "gas"
    reagents: str
    procedure: str
    positive_observation: str
    colour_hex: str = "#FFFFFF"
    notes: str = ""


VALID_CATEGORIES: tuple = (
    "flame", "hydroxide", "halide", "sulfate",
    "carbonate", "ammonium", "gas",
)


# ---- catalogue --------------------------------------------------

def _build_catalogue() -> List[InorganicTest]:
    out: List[InorganicTest] = []

    # ---- Flame tests (cations) ---------------------------------
    flame = [
        ("flame-li", "Lithium flame test", "Li⁺", "crimson red",
         "#DC143C",
         "Crimson red colour can be confused with strontium; "
         "a cobalt-blue glass screens out yellow Na⁺ "
         "contamination so the lithium colour shows clearly."),
        ("flame-na", "Sodium flame test", "Na⁺", "bright yellow",
         "#FFD700",
         "Sodium yellow is intense and persistent — the most "
         "common contaminant of any flame test.  Use a "
         "cobalt-blue glass to mask Na⁺ when looking for "
         "K⁺ / Li⁺."),
        ("flame-k", "Potassium flame test", "K⁺", "lilac (pale violet)",
         "#9370DB",
         "Lilac colour is masked by the slightest sodium "
         "contamination.  View through cobalt-blue glass to "
         "filter out the yellow Na line."),
        ("flame-ca", "Calcium flame test", "Ca²⁺", "brick red (orange-red)",
         "#B22222",
         "Brick red is darker / more orange than lithium "
         "crimson.  Distinguished from Sr²⁺ by spectroscopy."),
        ("flame-sr", "Strontium flame test", "Sr²⁺", "scarlet / crimson red",
         "#FF2400",
         "Used in red fireworks.  Brighter and more "
         "scarlet than calcium brick-red."),
        ("flame-ba", "Barium flame test", "Ba²⁺", "apple green",
         "#8DB600",
         "Apple-green flame; characteristic of Ba(NO₃)₂ "
         "in green fireworks."),
        ("flame-cu", "Copper flame test", "Cu²⁺", "blue-green",
         "#33A1C9",
         "Copper(II) compounds give a vivid blue-green; "
         "copper(I) halides give a separate blue colour."),
        ("flame-cs", "Caesium flame test", "Cs⁺", "blue-violet",
         "#9966CC",
         "Caesium gives a faint blue-violet — much weaker "
         "than the alkaline earths."),
    ]
    for tid, name, target, obs, col, notes in flame:
        out.append(InorganicTest(
            id=tid, name=name, category="flame", target=target,
            target_class="cation",
            reagents="Bunsen burner flame; clean nichrome / "
                     "platinum wire moistened with concentrated HCl",
            procedure="Dip a clean wire in concentrated HCl, then "
                      "in the powdered sample, and hold the wire in "
                      "the edge of a non-luminous Bunsen flame.",
            positive_observation=obs,
            colour_hex=col,
            notes=notes,
        ))

    # ---- Hydroxide precipitation tests (cations) ---------------
    hydrox = [
        ("hydroxide-cu2", "Copper(II) hydroxide test", "Cu²⁺",
         "blue gelatinous precipitate",
         "#1E90FF",
         "Cu(OH)₂ — does not dissolve in excess NaOH; "
         "dissolves in excess ammonia to give a deep "
         "royal-blue [Cu(NH₃)₄]²⁺ complex (Schweizer's "
         "reagent confirmation)."),
        ("hydroxide-fe2", "Iron(II) hydroxide test", "Fe²⁺",
         "green gelatinous precipitate",
         "#228B22",
         "Fe(OH)₂ — turns brown on standing as air "
         "oxidises it to Fe(OH)₃.  Distinguishes ferrous "
         "from ferric."),
        ("hydroxide-fe3", "Iron(III) hydroxide test", "Fe³⁺",
         "rust-brown gelatinous precipitate",
         "#A0522D",
         "Fe(OH)₃ — rusty brown.  Confirmed by the deep "
         "blood-red colour with KSCN (ferric thiocyanate)."),
        ("hydroxide-al3", "Aluminium hydroxide test", "Al³⁺",
         "white gelatinous precipitate",
         "#F5F5F5",
         "Al(OH)₃ — amphoteric, dissolves in EXCESS NaOH "
         "to give the soluble [Al(OH)₄]⁻ aluminate.  "
         "Distinguishes Al³⁺ from Mg²⁺ + Ca²⁺ (which stay "
         "as white ppt)."),
        ("hydroxide-mg2", "Magnesium hydroxide test", "Mg²⁺",
         "white gelatinous precipitate",
         "#F5F5F5",
         "Mg(OH)₂ — insoluble in excess NaOH (unlike "
         "Al³⁺).  Soluble in dilute acid + ammonium-salt "
         "solutions."),
        ("hydroxide-ca2", "Calcium hydroxide test", "Ca²⁺",
         "white precipitate (cloudy)",
         "#F5F5F5",
         "Ca(OH)₂ — sparingly soluble; the precipitate "
         "may be slow to form from dilute solutions.  "
         "Also called slaked lime / lime water."),
        ("hydroxide-zn2", "Zinc hydroxide test", "Zn²⁺",
         "white gelatinous precipitate",
         "#F5F5F5",
         "Zn(OH)₂ — amphoteric like Al(OH)₃; dissolves in "
         "excess NaOH to give [Zn(OH)₄]²⁻ zincate.  Also "
         "dissolves in excess ammonia → [Zn(NH₃)₄]²⁺."),
        ("hydroxide-pb2", "Lead(II) hydroxide test", "Pb²⁺",
         "white gelatinous precipitate",
         "#F5F5F5",
         "Pb(OH)₂ — amphoteric, dissolves in excess NaOH "
         "to give [Pb(OH)₄]²⁻ plumbate.  Also confirmed "
         "with KI giving yellow PbI₂."),
        ("hydroxide-mn2", "Manganese(II) hydroxide test", "Mn²⁺",
         "off-white precipitate (browns on standing)",
         "#D3D3D3",
         "Mn(OH)₂ — initially off-white but rapidly air-"
         "oxidises to brown MnO(OH).  The colour change "
         "is the diagnostic, not the initial precipitate."),
    ]
    for tid, name, target, obs, col, notes in hydrox:
        out.append(InorganicTest(
            id=tid, name=name, category="hydroxide", target=target,
            target_class="cation",
            reagents="dilute aqueous NaOH",
            procedure="Add a few drops of NaOH to the sample "
                      "solution.  Then add EXCESS NaOH to test for "
                      "amphoteric behaviour (re-dissolution).",
            positive_observation=obs,
            colour_hex=col,
            notes=notes,
        ))

    # ---- Halide tests (anions) ---------------------------------
    hal = [
        ("halide-cl", "Chloride test (AgNO₃)", "Cl⁻",
         "white curdy precipitate (soluble in dilute NH₃)",
         "#F5F5F5",
         "AgCl — dissolves in dilute (∼2 M) ammonia to give "
         "[Ag(NH₃)₂]⁺.  Distinguishes Cl⁻ from Br⁻ + I⁻ by "
         "ammonia solubility."),
        ("halide-br", "Bromide test (AgNO₃)", "Br⁻",
         "cream / pale-yellow precipitate (soluble in conc. NH₃)",
         "#FFFACD",
         "AgBr — only dissolves in CONCENTRATED ammonia.  "
         "Used in early photographic emulsions."),
        ("halide-i", "Iodide test (AgNO₃)", "I⁻",
         "yellow precipitate (insoluble in NH₃)",
         "#FFFF00",
         "AgI — yellow, insoluble in both dilute and "
         "concentrated ammonia.  Distinguishes I⁻ from "
         "Cl⁻ + Br⁻."),
    ]
    for tid, name, target, obs, col, notes in hal:
        out.append(InorganicTest(
            id=tid, name=name, category="halide", target=target,
            target_class="anion",
            reagents="dilute HNO₃, then dilute AgNO₃",
            procedure="Acidify the sample with dilute nitric acid "
                      "(eliminates carbonate / sulfite "
                      "interference), then add silver-nitrate "
                      "solution.  Add ammonia to test the "
                      "precipitate's solubility for the colour-"
                      "based confirmation.",
            positive_observation=obs,
            colour_hex=col,
            notes=notes,
        ))

    # ---- Sulfate ----------------------------------------------
    out.append(InorganicTest(
        id="sulfate-so4",
        name="Sulfate test (BaCl₂)",
        category="sulfate",
        target="SO₄²⁻",
        target_class="anion",
        reagents="dilute HCl (or HNO₃), then BaCl₂ "
                 "(or Ba(NO₃)₂)",
        procedure="Acidify the sample with dilute HCl to "
                  "destroy carbonates / sulfites, then add "
                  "barium chloride solution.",
        positive_observation="white precipitate (insoluble in acid)",
        colour_hex="#F5F5F5",
        notes="BaSO₄ — characteristically insoluble in dilute "
              "acid (BaCO₃ would dissolve, BaSO₃ would dissolve "
              "with SO₂ release).  The acid step is what makes "
              "this a SPECIFIC sulfate test rather than a "
              "general 'this anion gives a barium ppt' one.",
    ))

    # ---- Carbonate --------------------------------------------
    out.append(InorganicTest(
        id="carbonate-co3",
        name="Carbonate / bicarbonate test (acid + limewater)",
        category="carbonate",
        target="CO₃²⁻ / HCO₃⁻",
        target_class="anion",
        reagents="dilute HCl (or HNO₃); limewater "
                 "(saturated Ca(OH)₂)",
        procedure="Add dilute acid to the solid / solution.  "
                  "Pass any evolved gas through limewater.",
        positive_observation="effervescence; gas turns "
                             "limewater milky",
        colour_hex="#FFFFFF",
        notes="CO₂ from the carbonate reduces Ca(OH)₂ to "
              "insoluble CaCO₃ — the milky cloud.  Excess "
              "CO₂ re-dissolves the precipitate as soluble "
              "Ca(HCO₃)₂, so don't bubble gas through "
              "indefinitely.",
    ))

    # ---- Ammonium ---------------------------------------------
    out.append(InorganicTest(
        id="ammonium-nh4",
        name="Ammonium test (NaOH + heat)",
        category="ammonium",
        target="NH₄⁺",
        target_class="cation",
        reagents="aqueous NaOH; damp red litmus paper",
        procedure="Add NaOH to the sample and warm gently.  "
                  "Hold a piece of damp red litmus paper at "
                  "the mouth of the test tube.",
        positive_observation="pungent gas (NH₃) turns damp "
                             "red litmus paper blue",
        colour_hex="#87CEEB",   # litmus blue
        notes="Ammonia gas + water → NH₄OH (a weak base) on "
              "the litmus paper.  Also confirmed by white "
              "fumes when a glass rod dipped in concentrated "
              "HCl is brought near the gas.",
    ))

    # ---- Common gas tests --------------------------------------
    gas = [
        ("gas-h2", "Hydrogen test", "H₂",
         "lighted splint gives a 'pop' sound",
         "#FFFFFF",
         "Tiny rapid combustion of a hydrogen-air mixture.  "
         "The pop is loudest when the H₂:O₂ stoichiometry "
         "is close to 2:1.",
         "lighted wooden splint"),
        ("gas-o2", "Oxygen test", "O₂",
         "relights a glowing splint",
         "#FFFFFF",
         "A glowing (not flaming) splint re-ignites in "
         "pure or O₂-enriched air.  The splint must already "
         "be smouldering — it doesn't ignite a cold splint.",
         "glowing wooden splint"),
        ("gas-co2", "Carbon dioxide test", "CO₂",
         "turns limewater milky",
         "#FFFFFF",
         "Same chemistry as the carbonate test: CO₂ + "
         "Ca(OH)₂ → CaCO₃ (s) + H₂O.  Only test for CO₂ "
         "that's specific enough to use in a teaching lab.",
         "limewater (saturated Ca(OH)₂)"),
        ("gas-cl2", "Chlorine test", "Cl₂",
         "bleaches damp blue litmus paper (after first "
         "turning it red)",
         "#9ACD32",
         "Cl₂ + H₂O → HCl + HOCl; HCl turns litmus red, "
         "HOCl bleaches it.  Also identified by the pale-"
         "green colour of the gas itself.",
         "damp blue litmus paper"),
        ("gas-nh3", "Ammonia test", "NH₃",
         "turns damp red litmus paper blue",
         "#87CEEB",
         "Same observation as the ammonium-cation test "
         "(NH₃ is the gas released in that test).  Also "
         "identified by white fumes with concentrated HCl "
         "(NH₄Cl smoke).",
         "damp red litmus paper"),
        ("gas-hcl", "Hydrogen chloride test", "HCl",
         "white fumes with ammonia (NH₃)",
         "#FFFFFF",
         "Volatile NH₄Cl forms a dense white smoke when "
         "HCl gas meets NH₃ gas.  Both ends of the colour "
         "change — pH indicators turning red are also "
         "acceptable.",
         "concentrated NH₃ (or damp blue litmus paper)"),
        ("gas-so2", "Sulfur dioxide test", "SO₂",
         "turns acidified orange K₂Cr₂O₇ paper green",
         "#228B22",
         "SO₂ reduces Cr(VI) (orange dichromate) to "
         "Cr(III) (green chromium ion).  Distinct from "
         "Cl₂ which would bleach the same paper.",
         "filter paper soaked in acidified K₂Cr₂O₇"),
        ("gas-no2", "Nitrogen dioxide test", "NO₂",
         "characteristic brown gas; turns damp blue litmus red",
         "#A0522D",
         "NO₂ is one of the few common coloured gases — "
         "deep red-brown.  Also acidic (forms HNO₂ + HNO₃ "
         "with water).",
         "visual + damp blue litmus paper"),
    ]
    for tid, name, target, obs, col, notes, reagent in gas:
        out.append(InorganicTest(
            id=tid, name=name, category="gas", target=target,
            target_class="gas",
            reagents=reagent,
            procedure="Hold the indicating reagent at the "
                      "mouth of the gas-evolving vessel and "
                      "observe the change.",
            positive_observation=obs,
            colour_hex=col,
            notes=notes,
        ))

    return out


_TESTS: List[InorganicTest] = _build_catalogue()


# ---- public lookup helpers --------------------------------------

def list_tests(category: Optional[str] = None
               ) -> List[InorganicTest]:
    """Return every test, optionally filtered by *category*
    (one of :data:`VALID_CATEGORIES`)."""
    if category is None:
        return list(_TESTS)
    if category not in VALID_CATEGORIES:
        return []
    return [t for t in _TESTS if t.category == category]


def get_test(test_id: str) -> Optional[InorganicTest]:
    for t in _TESTS:
        if t.id == test_id:
            return t
    return None


def find_tests_for(target: str) -> List[InorganicTest]:
    """Return every test whose *target* (e.g. ``"Cu²⁺"`` /
    ``"Cl⁻"`` / ``"CO2"`` / ``"co2"``) matches a known entry.

    Lookup is case-insensitive and tolerates ASCII-only forms
    (``"Cu2+"`` / ``"Cl-"`` / ``"CO3 2-"``) by stripping common
    sub/superscript markers before comparison.  This is what
    lets the agent action accept a free-text query from the
    tutor without the user having to copy-paste Unicode.
    """
    if not target:
        return []
    needle = _normalise_ion_label(target)
    out: List[InorganicTest] = []
    for t in _TESTS:
        if _normalise_ion_label(t.target) == needle:
            out.append(t)
    return out


def _normalise_ion_label(label: str) -> str:
    """Strip common Unicode super / subscript markers + case so
    ``"Cu²⁺"``, ``"Cu2+"``, and ``"cu 2 +"`` all hash the same."""
    sub_super = {
        "⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4",
        "⁵": "5", "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9",
        "₀": "0", "₁": "1", "₂": "2", "₃": "3", "₄": "4",
        "₅": "5", "₆": "6", "₇": "7", "₈": "8", "₉": "9",
        "⁺": "+", "⁻": "-",
    }
    out_chars = []
    for ch in label.lower():
        out_chars.append(sub_super.get(ch, ch))
    s = "".join(out_chars)
    # Drop whitespace; keep + / - / digits / letters.
    return "".join(c for c in s if not c.isspace())


def categories() -> List[str]:
    return list(VALID_CATEGORIES)


def to_dict(test: InorganicTest) -> Dict[str, str]:
    """JSON-friendly serialisation for the agent action."""
    return {
        "id": test.id,
        "name": test.name,
        "category": test.category,
        "target": test.target,
        "target_class": test.target_class,
        "reagents": test.reagents,
        "procedure": test.procedure,
        "positive_observation": test.positive_observation,
        "colour_hex": test.colour_hex,
        "notes": test.notes,
    }
