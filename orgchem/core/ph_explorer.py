"""Phase 46a (round 148) — pH + buffer explorer core.

Three pieces of headless content for the *Tools → pH
explorer…* dialog (Phase 46b):

1. **`AcidEntry` catalogue** — ~40 acids spanning mineral
   acids + carboxylic acids + ammonium / amine bases +
   amino acids + phenols, with pKa values from CRC
   Handbook 100th ed.  Polyprotic acids carry a tuple of
   pKa values.

2. **`REFERENCE_CARDS` table** — 6 short pedagogical
   explainers (pH definition / Kw, strong vs weak,
   Henderson-Hasselbalch derivation, buffer capacity,
   polyprotic + amphiprotic species, biological-buffer
   selection).

3. **Solvers**:
   - :func:`design_buffer(target_pH, pKa,
     total_concentration_M, volume_L)` — Henderson-
     Hasselbalch buffer-design entry point.  Returns the
     full mixing recipe (HA + A⁻ concentrations + moles)
     + a buffer-capacity warning when the target pH is
     > 1 unit from the pKa.
   - :func:`buffer_capacity(total_concentration_M, pH,
     pKa)` — β = 2.3 · C_total · α · (1 − α).
   - :func:`titration_curve(weak_acid_pKa, acid_initial_M,
     volume_acid_mL, base_concentration_M, n_points)` —
     simulates dropwise NaOH addition to a weak acid +
     returns (volume_added_mL, pH) pairs for plotting.

The dialog (Phase 46b) consumes all three to provide a
buffer designer + pKa lookup table + reference panel.
"""
from __future__ import annotations
import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


# ------------------------------------------------------------------
# pKa catalogue
# ------------------------------------------------------------------

@dataclass(frozen=True)
class AcidEntry:
    id: str
    name: str
    formula: str             # human-readable formula
    category: str            # see VALID_CATEGORIES below
    pka_values: Tuple[float, ...]   # one entry for monoprotic
    notes: str = ""


VALID_CATEGORIES: tuple = (
    "mineral", "carboxylic", "amine", "amino-acid",
    "phenol", "biological-buffer", "other",
)


def _build_pka_table() -> List[AcidEntry]:
    return [
        # ---- Mineral acids ----
        AcidEntry("hcl", "Hydrochloric acid", "HCl",
                  "mineral", (-7.0,),
                  "Strong acid; fully dissociated in water"),
        AcidEntry("h2so4", "Sulfuric acid",
                  "H₂SO₄", "mineral", (-3.0, 1.99),
                  "First proton fully dissociated; "
                  "second has pKa₂ = 1.99 (HSO₄⁻ is a weak acid)"),
        AcidEntry("hno3", "Nitric acid", "HNO₃",
                  "mineral", (-1.4,),
                  "Strong acid"),
        AcidEntry("h3po4", "Phosphoric acid", "H₃PO₄",
                  "mineral", (2.15, 7.20, 12.35),
                  "Triprotic; pKa₂ = 7.2 makes it a useful "
                  "physiological buffer (intracellular pH "
                  "~7.0-7.4)"),
        AcidEntry("h2co3", "Carbonic acid", "H₂CO₃",
                  "mineral", (6.35, 10.33),
                  "Diprotic; pKa₁ = 6.35 makes the bicarbonate "
                  "buffer system the major blood buffer"),
        AcidEntry("hf", "Hydrofluoric acid", "HF",
                  "mineral", (3.17,),
                  "Weak acid despite being a hydrohalic acid; "
                  "F⁻ is a small + tightly-bound anion"),
        AcidEntry("hcn", "Hydrocyanic acid", "HCN",
                  "mineral", (9.21,),
                  "Weak acid; conjugate base CN⁻ is a strong "
                  "ligand for transition metals"),
        AcidEntry("h2s", "Hydrogen sulfide", "H₂S",
                  "mineral", (7.0, 12.9),
                  "Diprotic; pKa₁ = 7.0 means HS⁻ + H₂S coexist "
                  "at physiological pH"),

        # ---- Carboxylic acids ----
        AcidEntry("formic", "Formic acid", "HCOOH",
                  "carboxylic", (3.75,),
                  "Smallest carboxylic acid; produced by ants + "
                  "in methanol metabolism"),
        AcidEntry("acetic", "Acetic acid", "CH₃COOH",
                  "carboxylic", (4.76,),
                  "Reference textbook weak acid; the "
                  "acetate / acetic-acid buffer (pKa 4.76) "
                  "covers pH 3.8-5.8 — workhorse for low-pH "
                  "biology"),
        AcidEntry("propanoic", "Propanoic acid",
                  "CH₃CH₂COOH", "carboxylic", (4.87,)),
        AcidEntry("benzoic", "Benzoic acid",
                  "C₆H₅COOH", "carboxylic", (4.20,)),
        AcidEntry("salicylic", "Salicylic acid",
                  "2-HO-C₆H₄-COOH", "carboxylic", (2.97, 13.4),
                  "Active metabolite of aspirin; intramolecular "
                  "H-bond stabilises the conjugate base, "
                  "lowering pKa₁ vs benzoic"),
        AcidEntry("citric", "Citric acid", "C₃H₅O(COOH)₃",
                  "carboxylic", (3.13, 4.76, 6.40),
                  "Triprotic; pKa₂ = 4.76 makes citrate one "
                  "of the most useful weak-acid buffer systems "
                  "(citrate-phosphate buffer covers pH 2.6-7.6)"),
        AcidEntry("oxalic", "Oxalic acid", "(COOH)₂",
                  "carboxylic", (1.27, 4.27),
                  "Diprotic dicarboxylic acid; pKa₁ depressed "
                  "by σ-electron withdrawal of the second COOH"),
        AcidEntry("lactic", "Lactic acid",
                  "CH₃CH(OH)COOH", "carboxylic", (3.86,),
                  "Glycolysis end-product in anaerobic muscle; "
                  "lactic-acidosis acid"),
        AcidEntry("glycolic", "Glycolic acid",
                  "HOCH₂COOH", "carboxylic", (3.83,)),
        AcidEntry("pyruvic", "Pyruvic acid",
                  "CH₃C(=O)COOH", "carboxylic", (2.39,),
                  "α-Keto acid; glycolysis end-product"),
        AcidEntry("fumaric", "Fumaric acid",
                  "trans-HOOC-CH=CH-COOH", "carboxylic",
                  (3.03, 4.44), "TCA-cycle intermediate"),

        # ---- Amine bases (pKa of the conjugate ammonium) ----
        AcidEntry("nh4", "Ammonium / ammonia",
                  "NH₄⁺ / NH₃", "amine", (9.25,),
                  "Conjugate ammonium of NH₃; pKa = 9.25 "
                  "means NH₄⁺ is the dominant species at "
                  "physiological pH"),
        AcidEntry("methylammonium",
                  "Methylammonium / methylamine",
                  "CH₃NH₃⁺ / CH₃NH₂", "amine", (10.66,)),
        AcidEntry("pyridinium", "Pyridinium / pyridine",
                  "C₅H₅NH⁺ / C₅H₅N", "amine", (5.25,),
                  "Aromatic amine — much weaker base than "
                  "aliphatic amines (pKa 5.25 vs 10+) due to "
                  "sp² N lone-pair geometry"),
        AcidEntry("imidazolium",
                  "Imidazolium / imidazole",
                  "C₃H₅N₂⁺ / C₃H₄N₂", "amine", (6.95,),
                  "Side chain of histidine; pKa near "
                  "physiological pH makes histidine the "
                  "ideal acid-base catalyst at active sites"),
        AcidEntry("morpholine", "Morpholine",
                  "C₄H₉NO", "amine", (8.36,)),
        AcidEntry("triethylamine",
                  "Triethylammonium / triethylamine",
                  "(CH₃CH₂)₃NH⁺ / (CH₃CH₂)₃N", "amine",
                  (10.75,), "Common organic-chem base "
                  "(Hünig-type); pKa(BH⁺) ≈ 10.75"),

        # ---- Amino acids (α-COOH / α-NH₃⁺ / R-group) ----
        AcidEntry("glycine", "Glycine", "Gly / G",
                  "amino-acid", (2.34, 9.60),
                  "Simplest amino acid; no R-group pKa; "
                  "pI ≈ 5.97"),
        AcidEntry("alanine", "Alanine", "Ala / A",
                  "amino-acid", (2.34, 9.69),
                  "Methyl R-group; pI ≈ 6.00"),
        AcidEntry("aspartic_acid", "Aspartic acid",
                  "Asp / D", "amino-acid",
                  (2.10, 9.82, 3.86),
                  "R-group COOH (pKa_R = 3.86); pI ≈ 2.98 "
                  "(acidic side chain)"),
        AcidEntry("glutamic_acid", "Glutamic acid",
                  "Glu / E", "amino-acid",
                  (2.19, 9.67, 4.25),
                  "R-group COOH (pKa_R = 4.25); pI ≈ 3.22"),
        AcidEntry("histidine", "Histidine", "His / H",
                  "amino-acid", (1.82, 9.17, 6.00),
                  "R-group imidazole (pKa_R = 6.00); the only "
                  "amino acid with a side chain titrating near "
                  "physiological pH — the active-site acid-"
                  "base catalyst in many enzymes"),
        AcidEntry("lysine", "Lysine", "Lys / K",
                  "amino-acid", (2.18, 8.95, 10.79),
                  "R-group ε-NH₃⁺ (pKa_R = 10.79); pI ≈ 9.74 "
                  "(basic side chain)"),
        AcidEntry("arginine", "Arginine", "Arg / R",
                  "amino-acid", (2.18, 9.09, 12.48),
                  "R-group guanidinium (pKa_R = 12.48); the "
                  "most basic of the 20 amino acids"),
        AcidEntry("cysteine", "Cysteine", "Cys / C",
                  "amino-acid", (1.71, 10.78, 8.33),
                  "R-group thiol (pKa_R = 8.33); active-site "
                  "nucleophile in cysteine proteases + key "
                  "redox couple as the disulfide / thiol"),
        AcidEntry("tyrosine", "Tyrosine", "Tyr / Y",
                  "amino-acid", (2.20, 9.11, 10.07),
                  "R-group phenol (pKa_R = 10.07); aromatic "
                  "ring contributes to A₂₈₀ protein quant"),

        # ---- Phenols ----
        AcidEntry("phenol", "Phenol", "C₆H₅OH",
                  "phenol", (10.0,),
                  "Reference weak acid; phenoxide stabilised "
                  "by aromatic-ring delocalisation"),
        AcidEntry("4_nitrophenol", "4-Nitrophenol",
                  "4-NO₂-C₆H₄-OH", "phenol", (7.15,),
                  "EWG NO₂ at the para position drops pKa "
                  "from 10.0 (phenol) to 7.15 — reference "
                  "compound for chromogenic enzyme assays"),
        AcidEntry("p_cresol", "p-Cresol",
                  "4-CH₃-C₆H₄-OH", "phenol", (10.26,),
                  "Slight EDG bump above phenol baseline"),

        # ---- Biological buffers (zwitterionic Good's buffers) ----
        AcidEntry("tris", "Tris (THAM)",
                  "(HOCH₂)₃CNH₃⁺ / (HOCH₂)₃CNH₂",
                  "biological-buffer", (8.10,),
                  "Tris(hydroxymethyl)aminomethane — the "
                  "default pH 7-9 biology buffer; pKa is "
                  "strongly T-dependent (Δ -0.028 pH/°C), "
                  "so calibrate at the working temperature"),
        AcidEntry("hepes", "HEPES",
                  "C₈H₁₈N₂O₄S",
                  "biological-buffer", (7.55,),
                  "Good's buffer for pH 6.8-8.2; widely used "
                  "in cell culture (less metal-binding than "
                  "phosphate); slight UV absorbance below "
                  "240 nm"),
        AcidEntry("mops", "MOPS",
                  "C₇H₁₅NO₄S",
                  "biological-buffer", (7.20,),
                  "Good's buffer for pH 6.5-7.9; "
                  "preferred for RNA work (low metal binding)"),
        AcidEntry("mes", "MES",
                  "C₆H₁₃NO₄S",
                  "biological-buffer", (6.15,),
                  "Good's buffer for pH 5.5-6.7; "
                  "useful for organic / chromatography work "
                  "where Tris pKa is too high"),
        AcidEntry("bistris", "BIS-TRIS",
                  "C₈H₁₉NO₅",
                  "biological-buffer", (6.50,),
                  "Good's buffer for pH 5.8-7.2; "
                  "bridges the gap between MES + HEPES"),
        AcidEntry("pipes", "PIPES",
                  "C₈H₁₈N₂O₆S₂",
                  "biological-buffer", (6.76,),
                  "Good's buffer for pH 6.1-7.5; "
                  "very low Ca²⁺ binding"),
        AcidEntry("ches", "CHES",
                  "C₈H₁₇NO₃S",
                  "biological-buffer", (9.50,),
                  "Good's buffer for pH 8.6-10.0 — covers "
                  "the alkaline range above HEPES"),

        # ---- Other reference acids ----
        AcidEntry("water", "Water (autoionisation)",
                  "H₂O / OH⁻", "other", (15.7,),
                  "K_w = 1e-14 at 25 °C → autoionisation pKa "
                  "= 15.7 (corrected for the 55.5 M water "
                  "concentration)"),
        AcidEntry("methanol", "Methanol",
                  "CH₃OH", "other", (15.5,),
                  "Slightly more acidic than water"),
    ]


_PKA_TABLE: List[AcidEntry] = _build_pka_table()


# ------------------------------------------------------------------
# Reference cards (short HTML pedagogical explainers)
# ------------------------------------------------------------------

@dataclass(frozen=True)
class ReferenceCard:
    id: str
    title: str
    body_html: str   # short rendered HTML — typeset in the dialog


REFERENCE_CARDS: List[ReferenceCard] = [
    ReferenceCard(
        "ph_definition",
        "pH definition + autoionisation of water",
        """
        <p><b>pH = -log₁₀([H⁺])</b>; <b>pOH = -log₁₀([OH⁻])</b>.
        At 25 °C the autoionisation constant
        K<sub>w</sub> = [H⁺][OH⁻] = 10⁻¹⁴ → pH + pOH = 14.</p>
        <p>K<sub>w</sub> is temperature-dependent: at 0 °C
        K<sub>w</sub> ≈ 1.1×10⁻¹⁵ (pK<sub>w</sub> ≈ 14.96), at
        100 °C K<sub>w</sub> ≈ 5×10⁻¹³ (pK<sub>w</sub> ≈ 12.3).
        That's why the pH of pure water at body temperature
        (37 °C) is ~6.81, not 7.0 — pure water is still
        neutral, but neutral pH ≠ 7 at non-25 °C
        temperatures.</p>
        <p>The pH scale isn't bounded at 0 + 14; concentrated
        HCl ([H⁺] = 12 M) has pH ≈ -1.1, and 10 M NaOH has
        pH ≈ 15.</p>
        """),
    ReferenceCard(
        "strong_weak",
        "Strong vs weak acids + bases",
        """
        <p>A <b>strong acid</b> dissociates fully:
        [H⁺] = [HA]<sub>0</sub> — pH = -log
        [HA]<sub>0</sub> directly (above ~10⁻⁶ M; below that
        the water autoionisation matters).</p>
        <p>A <b>weak acid</b> partially dissociates:
        K<sub>a</sub> = [H⁺][A⁻] / [HA].  For a pure weak-
        acid solution (no added A⁻):
        [H⁺] ≈ √(K<sub>a</sub> · [HA]<sub>0</sub>) when
        K<sub>a</sub> &lt;&lt; [HA]<sub>0</sub>.</p>
        <p>Common rule of thumb: <b>pK<sub>a</sub> &lt; 0</b>
        = strong (HCl, HNO₃, HBr, HI, H₂SO₄ pKa₁, HClO₄);
        <b>0 &lt; pK<sub>a</sub> &lt; 14</b> = weak; <b>pK<sub>a</sub>
        &gt; 14</b> = "non-acid" in water.</p>
        """),
    ReferenceCard(
        "henderson_hasselbalch",
        "Henderson-Hasselbalch derivation",
        """
        <p>Start from K<sub>a</sub> = [H⁺][A⁻] / [HA].
        Take -log<sub>10</sub> of both sides: -log K<sub>a</sub>
        = -log [H⁺] + (-log [A⁻] / [HA]).</p>
        <p>Rearrange: <b>pH = pK<sub>a</sub> + log([A⁻] /
        [HA])</b> — the Henderson-Hasselbalch equation.
        At [A⁻] = [HA] (half-titration), the log term is
        zero → pH = pK<sub>a</sub>.</p>
        <p>Use case 1: predict the pH of a buffer when you
        know the [HA] / [A⁻] mixing ratio.  Use case 2:
        design a buffer — pick a weak acid with pK<sub>a</sub>
        within ±1 of the target pH, then compute the ratio.</p>
        <p>The Phase-39a <code>henderson_hasselbalch</code>
        agent action solves any 2 of 3 (pH / pKa / ratio).
        The Phase-46b buffer-designer widget extends this
        with masses + volumes for actual buffer
        preparation.</p>
        """),
    ReferenceCard(
        "buffer_capacity",
        "Buffer capacity (β)",
        """
        <p>Buffer capacity quantifies how much added strong
        acid / base a buffer can absorb before pH changes
        appreciably:
        <b>β = -dn<sub>HA</sub>/dpH</b>
        (mol of strong base added per pH unit shifted).</p>
        <p>For a weak-acid / conjugate-base buffer at fixed
        total concentration C<sub>total</sub>:
        <b>β = 2.303 · C<sub>total</sub> · α · (1 − α)</b>
        where α = [A⁻] / C<sub>total</sub>.</p>
        <p>β is maximal at <b>α = 0.5</b> (i.e. pH =
        pK<sub>a</sub>), where β<sub>max</sub> ≈ 0.576 ·
        C<sub>total</sub>.  At pH = pK<sub>a</sub> ± 1, β
        drops to 30 % of max.  Beyond ±1 unit, the buffer
        stops working — pick a different weak acid for
        that pH range.</p>
        <p>Practical: a buffer holds best when target pH
        sits within pK<sub>a</sub> ± 1.  Outside that
        range, the Phase-46b buffer-designer widget shows
        a capacity warning.</p>
        """),
    ReferenceCard(
        "polyprotic",
        "Polyprotic + amphiprotic species",
        """
        <p>A <b>polyprotic</b> acid has multiple ionisable
        protons: H₃PO₄ (pKa 2.15 / 7.20 / 12.35), H₂CO₃
        (pKa 6.35 / 10.33), citric acid (pKa 3.13 / 4.76 /
        6.40).  Each pK<sub>a</sub> defines a separate
        titration step.</p>
        <p>For a polyprotic acid, the <b>amphiprotic</b>
        species (e.g. HCO₃⁻, H₂PO₄⁻, HPO₄²⁻) has both an
        acidic H AND a basic site.  Its solution pH is
        approximated by the geometric mean of the
        bracketing pK<sub>a</sub>s:
        <b>pH ≈ ½(pK<sub>a₁</sub> + pK<sub>a₂</sub>)</b>.</p>
        <p>Example: NaH₂PO₄ in water has pH ≈ ½(2.15 +
        7.20) = 4.68; Na₂HPO₄ has pH ≈ ½(7.20 + 12.35) =
        9.78.  This is why phosphate buffer prep is a
        ratio of NaH₂PO₄ + Na₂HPO₄ to hit a target pH near
        7 (between the two pK<sub>a</sub>s).</p>
        <p>Amino-acid <b>isoelectric point pI</b> (zero net
        charge) is computed similarly: average the two
        pK<sub>a</sub>s flanking the zero-charge point.
        Glycine: pI = ½(2.34 + 9.60) = 5.97.</p>
        """),
    ReferenceCard(
        "biological_buffers",
        "Choosing a biological buffer (Good's series)",
        """
        <p>Good's buffers (Norman Good, 1966) are
        zwitterionic compounds chosen for biology + biochem:
        pK<sub>a</sub> in the physiological range (6-9),
        low metal binding, cell-membrane impermeable, no
        UV absorbance above 240 nm, water-soluble +
        chemically inert, low T-dependence.</p>
        <p>Pick by target pH (use within pK<sub>a</sub> ± 1):</p>
        <ul>
        <li><b>MES</b> — pK<sub>a</sub> 6.15 (pH 5.5-6.7)</li>
        <li><b>BIS-TRIS</b> — pK<sub>a</sub> 6.50 (pH 5.8-7.2)</li>
        <li><b>PIPES</b> — pK<sub>a</sub> 6.76 (pH 6.1-7.5;
        very low Ca²⁺ binding — use for Ca²⁺-imaging buffers)</li>
        <li><b>MOPS</b> — pK<sub>a</sub> 7.20 (pH 6.5-7.9;
        low metal binding — preferred for RNA work)</li>
        <li><b>HEPES</b> — pK<sub>a</sub> 7.55 (pH 6.8-8.2;
        the cell-culture default)</li>
        <li><b>Tris</b> — pK<sub>a</sub> 8.10 (pH 7.0-9.0;
        cheap workhorse; T-dependent — calibrate hot)</li>
        <li><b>CHES</b> — pK<sub>a</sub> 9.50 (pH 8.6-10.0)</li>
        </ul>
        <p>For the very-low-pH range (&lt; 5), citrate (pK<sub>a₂</sub>
        4.76) or acetate (pK<sub>a</sub> 4.76) are the
        non-Good's-buffer go-tos.  For pH &gt; 10, glycine /
        carbonate.</p>
        """),
]


# ------------------------------------------------------------------
# Buffer-design + capacity solvers
# ------------------------------------------------------------------

def design_buffer(
    target_pH: float,
    pKa: float,
    total_concentration_M: float,
    volume_L: float = 1.0,
) -> Dict[str, object]:
    """Design a buffer at *target_pH* using a weak acid of
    given *pKa* + total acid+base concentration.

    Returns the full mixing recipe:

    - ``base_acid_ratio`` = [A⁻] / [HA] (from H-H equation).
    - ``acid_concentration_M`` + ``base_concentration_M``
      such that they sum to ``total_concentration_M``.
    - ``acid_moles`` + ``base_moles`` = conc × volume_L.
    - ``capacity_warning`` (bool) — True when |pH - pKa| > 1
      (buffer capacity drops sharply outside this range).
    - ``capacity_message`` (str) — guidance text describing
      the warning.
    """
    if total_concentration_M <= 0:
        raise ValueError(
            "total_concentration_M must be > 0; "
            f"got {total_concentration_M!r}.")
    if volume_L <= 0:
        raise ValueError(
            f"volume_L must be > 0; got {volume_L!r}.")
    ratio = 10 ** (target_pH - pKa)
    # Solve: [HA] + [A⁻] = total; [A⁻] / [HA] = ratio.
    acid_concentration = total_concentration_M / (1 + ratio)
    base_concentration = total_concentration_M - acid_concentration
    acid_moles = acid_concentration * volume_L
    base_moles = base_concentration * volume_L
    delta = abs(target_pH - pKa)
    capacity_warning = delta > 1.0
    if capacity_warning:
        msg = (
            f"target_pH ({target_pH:.2f}) is {delta:.2f} pH "
            f"units away from pKa ({pKa:.2f}).  "
            f"Buffer capacity drops to ~30 % of max at "
            f"|ΔpH| = 1.  Consider a different weak acid "
            f"with pKa closer to your target."
        )
    else:
        msg = (
            f"Target within pKa ± 1 — buffer capacity is "
            f"good ({(1 - delta) * 100:.0f}% of maximum)."
        )
    return {
        "target_pH": target_pH,
        "pKa": pKa,
        "total_concentration_M": total_concentration_M,
        "volume_L": volume_L,
        "base_acid_ratio": ratio,
        "acid_concentration_M": acid_concentration,
        "base_concentration_M": base_concentration,
        "acid_moles": acid_moles,
        "base_moles": base_moles,
        "capacity_warning": capacity_warning,
        "capacity_message": msg,
    }


def buffer_capacity(
    total_concentration_M: float,
    pH: float,
    pKa: float,
) -> Dict[str, float]:
    """Compute β = 2.303 · C_total · α · (1 − α) where
    α = [A⁻] / C_total at the given pH.

    β has units of mol/L per pH unit — the moles of strong
    base needed to shift this buffer's pH up by 1.
    Maximum at pH = pKa where β = 0.576 · C_total.
    """
    if total_concentration_M <= 0:
        raise ValueError(
            "total_concentration_M must be > 0; "
            f"got {total_concentration_M!r}.")
    ratio = 10 ** (pH - pKa)
    alpha = ratio / (1 + ratio)
    beta = 2.303 * total_concentration_M * alpha * (1 - alpha)
    beta_max = 2.303 * total_concentration_M * 0.25
    return {
        "buffer_capacity_M_per_pH": beta,
        "buffer_capacity_max_M_per_pH": beta_max,
        "alpha": alpha,
        "fraction_of_max": beta / beta_max if beta_max > 0 else 0,
        "pH": pH,
        "pKa": pKa,
        "total_concentration_M": total_concentration_M,
    }


def titration_curve(
    weak_acid_pKa: float,
    acid_initial_M: float,
    volume_acid_mL: float,
    base_concentration_M: float,
    n_points: int = 50,
) -> Dict[str, object]:
    """Simulate the titration of a weak acid with a strong
    base (NaOH) — return (volume_added_mL, pH) pairs for
    plotting.

    Uses the Henderson-Hasselbalch approximation away from
    the equivalence point + a near-equivalence-point
    correction via the conjugate-base hydrolysis.
    """
    if not (0 < weak_acid_pKa < 14):
        raise ValueError(
            f"weak_acid_pKa outside aqueous range; "
            f"got {weak_acid_pKa!r}.")
    if acid_initial_M <= 0 or volume_acid_mL <= 0 \
            or base_concentration_M <= 0:
        raise ValueError("All concentrations + volumes must be > 0.")
    if n_points < 5:
        raise ValueError("n_points must be ≥ 5.")
    # Total moles of acid in the flask.
    moles_acid = acid_initial_M * volume_acid_mL / 1000.0
    # Volume to reach equivalence point (in mL).
    v_eq_mL = (moles_acid / base_concentration_M) * 1000.0
    Ka = 10 ** (-weak_acid_pKa)
    points = []
    # Sample n_points uniformly from 0 to 2 × v_eq.
    for i in range(n_points + 1):
        v_added = (2 * v_eq_mL) * i / n_points
        moles_base_added = (v_added * base_concentration_M
                            / 1000.0)
        total_volume_L = (volume_acid_mL + v_added) / 1000.0
        if i == 0:
            # Pure weak acid — [H⁺] ≈ √(Ka · C).
            h = math.sqrt(Ka * acid_initial_M)
            pH = -math.log10(h)
        elif moles_base_added < moles_acid:
            # Buffer region: HH equation.
            ratio = moles_base_added / (moles_acid -
                                         moles_base_added)
            if ratio <= 0:
                pH = weak_acid_pKa - 5
            else:
                pH = weak_acid_pKa + math.log10(ratio)
        elif abs(moles_base_added - moles_acid) < 1e-12:
            # Equivalence point: only A⁻ in solution.
            # pH from Kb of the conjugate base.
            Kb = 1e-14 / Ka
            conjugate_conc = moles_acid / total_volume_L
            oh = math.sqrt(Kb * conjugate_conc)
            pOH = -math.log10(oh)
            pH = 14 - pOH
        else:
            # Past equivalence: excess strong base dominates.
            excess_base_moles = moles_base_added - moles_acid
            oh = excess_base_moles / total_volume_L
            pOH = -math.log10(oh)
            pH = 14 - pOH
        points.append((v_added, pH))
    return {
        "weak_acid_pKa": weak_acid_pKa,
        "acid_initial_M": acid_initial_M,
        "volume_acid_mL": volume_acid_mL,
        "base_concentration_M": base_concentration_M,
        "n_points": n_points,
        "equivalence_point_mL": v_eq_mL,
        "points": points,
    }


# ------------------------------------------------------------------
# Lookup helpers
# ------------------------------------------------------------------

def list_acids(category: Optional[str] = None
               ) -> List[AcidEntry]:
    if category is None:
        return list(_PKA_TABLE)
    if category not in VALID_CATEGORIES:
        return []
    return [a for a in _PKA_TABLE if a.category == category]


def get_acid(acid_id: str) -> Optional[AcidEntry]:
    for a in _PKA_TABLE:
        if a.id == acid_id:
            return a
    return None


def find_acids(needle: str) -> List[AcidEntry]:
    if not needle:
        return []
    n = needle.lower().strip()
    return [a for a in _PKA_TABLE
            if n in a.id.lower() or n in a.name.lower()
            or n in a.formula.lower()
            or n in a.category.lower()]


def categories() -> List[str]:
    return list(VALID_CATEGORIES)


def list_reference_cards() -> List[ReferenceCard]:
    return list(REFERENCE_CARDS)


def get_reference_card(card_id: str) -> Optional[ReferenceCard]:
    for c in REFERENCE_CARDS:
        if c.id == card_id:
            return c
    return None


def acid_to_dict(a: AcidEntry) -> Dict[str, object]:
    return {
        "id": a.id, "name": a.name,
        "formula": a.formula, "category": a.category,
        "pka_values": list(a.pka_values),
        "n_pka": len(a.pka_values),
        "notes": a.notes,
    }
