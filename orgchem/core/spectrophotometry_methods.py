"""Phase 37d (round 139) — spectrophotometry-method catalogue.

Headless reference data for the *Tools → Spectrophotometry…*
dialog.  Same shape as the Phase-37c chromatography catalogue
— each entry is a long-form reference card with principle,
light source, sample handling, detector, wavelength range,
strengths / limitations, procedure, notes.

Categories
----------
- ``"molecular-uv-vis"`` — UV-Vis, fluorescence.
- ``"molecular-ir"`` — IR / FTIR, ATR-FTIR, NIR, Raman, SERS.
- ``"molecular-chirality"`` — circular dichroism.
- ``"atomic"`` — AA, ICP-OES, ICP-MS.
- ``"magnetic-resonance"`` — NMR.

The catalogue is intentionally instrument-method-focused —
a method-development reference, not a prediction tool.  IR
band correlations + NMR shift tables already live in
:mod:`orgchem.core.spectroscopy` / :mod:`orgchem.core.nmr` /
:mod:`orgchem.core.ms` and the entries here cross-reference
those for predictive use.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass(frozen=True)
class SpectrophotometryMethod:
    id: str
    name: str
    abbreviation: str
    category: str
    principle: str
    light_source: str
    sample_handling: str
    detector: str
    wavelength_range: str
    typical_analytes: str
    strengths: str
    limitations: str
    procedure: str
    notes: str = ""


VALID_CATEGORIES: tuple = (
    "molecular-uv-vis", "molecular-ir",
    "molecular-chirality", "atomic", "magnetic-resonance",
)


# ------------------------------------------------------------------
# Beer-Lambert helpers (small calculator surface used by the
# dialog + agent action)
# ------------------------------------------------------------------

def beer_lambert_solve(absorbance: Optional[float] = None,
                       molar_absorptivity: Optional[float] = None,
                       path_length_cm: Optional[float] = None,
                       concentration_M: Optional[float] = None,
                       ) -> Dict[str, float]:
    """Beer-Lambert: A = ε · l · c.

    Pass any 3 of the 4 quantities; the 4th is computed and
    returned alongside the inputs.  All values use SI / molar
    units: ε in M⁻¹·cm⁻¹, l in cm, c in M.  Raises
    ``ValueError`` if more than one quantity is missing or if
    any input is non-positive.
    """
    given = {
        "absorbance": absorbance,
        "molar_absorptivity": molar_absorptivity,
        "path_length_cm": path_length_cm,
        "concentration_M": concentration_M,
    }
    missing = [k for k, v in given.items() if v is None]
    if len(missing) != 1:
        raise ValueError(
            f"Pass exactly 3 of 4 Beer-Lambert quantities; "
            f"got {len(missing)} missing ({missing}).")
    for k, v in given.items():
        if v is not None and v <= 0:
            raise ValueError(
                f"{k} must be positive; got {v!r}.")
    if missing == ["absorbance"]:
        given["absorbance"] = (
            molar_absorptivity * path_length_cm * concentration_M)
    elif missing == ["molar_absorptivity"]:
        given["molar_absorptivity"] = (
            absorbance / (path_length_cm * concentration_M))
    elif missing == ["path_length_cm"]:
        given["path_length_cm"] = (
            absorbance / (molar_absorptivity * concentration_M))
    else:  # concentration_M
        given["concentration_M"] = (
            absorbance / (molar_absorptivity * path_length_cm))
    return given


# ------------------------------------------------------------------
# Catalogue
# ------------------------------------------------------------------

def _build_catalogue() -> List[SpectrophotometryMethod]:
    return [
        # ---- Molecular UV-Vis + fluorescence ----
        SpectrophotometryMethod(
            id="uv_vis",
            name="UV-Visible spectrophotometry",
            abbreviation="UV-Vis",
            category="molecular-uv-vis",
            principle=(
                "Absorption of UV / visible light promotes a "
                "valence electron from a bonding / non-bonding "
                "orbital to an antibonding orbital "
                "(σ→σ*, n→σ*, π→π*, n→π*).  Quantitatively "
                "described by the Beer-Lambert law A = ε·l·c "
                "where A is dimensionless absorbance "
                "(log₁₀ I₀/I), ε is the molar absorptivity "
                "(M⁻¹·cm⁻¹), l is the path length (cm), and "
                "c is the analyte concentration (M)."
            ),
            light_source=(
                "Deuterium arc lamp (190-400 nm UV) + tungsten-"
                "halogen lamp (350-1100 nm visible); modern "
                "instruments switch automatically at ~340 nm.  "
                "Newer single-source xenon-flash designs cover "
                "the entire range with one lamp."
            ),
            sample_handling=(
                "Optical-grade quartz cuvettes (UV-transparent, "
                "1-cm standard path length; 200-µL micro and "
                "10-cm long-path variants); plastic "
                "(polystyrene / PMMA) cuvettes acceptable "
                "above ~340 nm only.  Solvent must not absorb "
                "in the analyte's wavelength range — water, "
                "acetonitrile, methanol, ethanol are common; "
                "chloroform / DMSO have UV cut-offs."
            ),
            detector=(
                "Photomultiplier tube (PMT) for highest "
                "sensitivity; photodiode arrays (PDA) for "
                "simultaneous multi-wavelength acquisition "
                "(spectral acquisition in <1 second); "
                "CCD for imaging applications"
            ),
            wavelength_range="190-1100 nm typical; some down to 175 nm",
            typical_analytes=(
                "Protein quantitation (A₂₈₀ = 1 mg/mL ≈ 1 OD "
                "for typical Trp/Tyr content); DNA / RNA "
                "(A₂₆₀ = 50 µg/mL for dsDNA, 40 for ssDNA, "
                "33 for ssRNA); chlorophyll / carotenoid "
                "pigments; transition-metal complexes; "
                "enzyme-kinetics monitoring (e.g. NADH at "
                "340 nm); reaction-progress curves"
            ),
            strengths=(
                "Cheap, fast (<1 s spectrum), reproducible, "
                "non-destructive (sample recoverable), "
                "wide concentration range with cuvette path-"
                "length choice, established Beer-Lambert "
                "quantitation"
            ),
            limitations=(
                "Requires a chromophore (no absorbance = no "
                "signal); deviates from Beer-Lambert at "
                "high concentrations (chemical equilibria, "
                "stray light); turbidity / scattering "
                "overestimates absorbance; cuvette quality "
                "matters at the extremes"
            ),
            procedure=(
                "Zero the spectrophotometer with the solvent "
                "blank in a matched cuvette.  Insert the "
                "sample cuvette in the same orientation "
                "(cuvettes have ground glass + clear "
                "windows).  Read absorbance at the "
                "λ_max if quantitating a known analyte, or "
                "scan the full wavelength range for a "
                "spectrum.  For kinetic runs, sample at "
                "fixed wavelength every ∆t."
            ),
            notes=(
                "Beer-Lambert holds linearly up to A ≈ 1.0 — "
                "above that, dilute the sample.  For "
                "ultra-dilute samples (<10 µM) use a 10-cm "
                "long-path cuvette.  NanoDrop / DropletQuant "
                "platforms use a 1-mm path through a 2-µL "
                "droplet to span the same A range without "
                "sample-volume fuss — the de-facto standard "
                "for bench protein / DNA quant."
            ),
        ),
        SpectrophotometryMethod(
            id="fluorescence",
            name="Fluorescence spectrophotometry",
            abbreviation="Fluor",
            category="molecular-uv-vis",
            principle=(
                "An absorbed UV / visible photon excites the "
                "molecule to a vibrational sub-level of the "
                "first excited singlet S₁.  Vibrational "
                "relaxation drops the molecule to v=0 of S₁ "
                "(picoseconds), then radiative decay to S₀ "
                "emits a longer-wavelength photon "
                "(nanoseconds).  The wavelength gap between "
                "absorption and emission peaks is the "
                "Stokes shift; the fraction of absorbed "
                "photons that re-emit is the quantum yield Φ."
            ),
            light_source=(
                "Xenon arc lamp (continuous 200-900 nm) for "
                "scanning excitation spectra; fixed-"
                "wavelength UV LED or laser for single-"
                "wavelength assays; pulsed lasers for time-"
                "resolved fluorescence"
            ),
            sample_handling=(
                "Four-clear-side quartz cuvettes (right-angle "
                "geometry — emission collected at 90° from "
                "excitation to avoid direct lamp light); "
                "micro-cuvettes for precious samples; "
                "front-face geometry for opaque / scattering "
                "samples"
            ),
            detector=(
                "Photomultiplier tube (sensitivity required "
                "for nanomolar analytes); some instruments "
                "use CCD for full-spectrum acquisition"
            ),
            wavelength_range=(
                "Excitation 200-700 nm; emission 250-800 nm "
                "(emission always > excitation due to Stokes "
                "shift)"
            ),
            typical_analytes=(
                "Intrinsic protein fluorescence (Trp 280→340 nm, "
                "Tyr 275→304 nm); fluorescent labels (FITC, "
                "Cy3, Cy5, GFP variants); DNA-binding probes "
                "(SYBR Green, ethidium bromide); ion sensors "
                "(Fura-2 for Ca²⁺); fluorescent enzyme "
                "substrates"
            ),
            strengths=(
                "100-1000× more sensitive than UV-Vis "
                "absorption (limit-of-detection in pM range); "
                "wavelength-selective (two-dimensional ex/em "
                "matrix discriminates components); kinetic "
                "ranges sub-millisecond"
            ),
            limitations=(
                "Only chromophores that fluoresce work; "
                "inner-filter effects at high concentrations "
                "(absorption of excitation OR emission "
                "light); fluorophore photobleaching during "
                "long acquisitions; quenching by O₂, "
                "halides, paramagnetic species"
            ),
            procedure=(
                "Set excitation monochromator to the absorbance "
                "λ_max (or scan to find it); set emission "
                "monochromator to the expected emission λ_max; "
                "blank with solvent; measure intensity.  For "
                "spectra: scan emission at fixed excitation, "
                "or scan excitation at fixed emission."
            ),
            notes=(
                "Quantum yield Φ = photons emitted / photons "
                "absorbed; standard reference compounds "
                "(quinine sulfate Φ = 0.546 in 0.1 N H₂SO₄; "
                "tryptophan Φ = 0.13 in water) make Φ "
                "measurement straightforward via a relative "
                "method.  Time-resolved fluorescence (TRF) and "
                "fluorescence lifetime imaging (FLIM) extract "
                "structural information from the nanosecond "
                "decay curve."
            ),
        ),

        # ---- Molecular IR / vibrational ----
        SpectrophotometryMethod(
            id="ir_ftir",
            name="Infrared / Fourier-transform infrared",
            abbreviation="IR / FTIR",
            category="molecular-ir",
            principle=(
                "Mid-IR photons (4000-400 cm⁻¹) match the "
                "vibrational quanta of bonds.  Absorption "
                "occurs only when a vibration changes the "
                "molecular dipole moment (selection rule).  "
                "Each functional group has a characteristic "
                "fingerprint of stretches + bends; the "
                "fingerprint region (1500-500 cm⁻¹) "
                "uniquely identifies a compound.  FTIR "
                "instruments use a Michelson interferometer "
                "+ FFT to acquire the entire spectrum "
                "simultaneously, with a 100-1000× signal-"
                "to-noise advantage over dispersive IR."
            ),
            light_source=(
                "Globar (silicon-carbide rod heated to "
                "~1500 K, broadband 4000-50 cm⁻¹); "
                "tungsten-halogen for near-IR; mercury "
                "discharge for far-IR"
            ),
            sample_handling=(
                "Solid: KBr disc (mortar-grind sample with "
                "KBr 1:100, press into transparent disc) or "
                "Nujol mull on NaCl plates.  Liquid: thin "
                "film between NaCl plates or in a 0.025 mm "
                "fixed-path liquid cell.  Gas: 10-100 cm "
                "gas cell.  Cuvette material must be "
                "IR-transparent (NOT glass — KBr, NaCl, "
                "CaF₂, ZnSe, Ge)."
            ),
            detector=(
                "DTGS (deuterated triglycine sulfate, room "
                "temperature, slow); MCT (mercury cadmium "
                "telluride, liquid-nitrogen cooled, fast + "
                "sensitive — required for kinetic / "
                "microscopic FTIR)"
            ),
            wavelength_range=(
                "Mid-IR: 4000-400 cm⁻¹ (2.5-25 µm); "
                "near-IR: 14000-4000 cm⁻¹; far-IR: 400-10 "
                "cm⁻¹"
            ),
            typical_analytes=(
                "Functional-group identification in synthetic "
                "organic chemistry (C=O ~1700, O-H ~3300, "
                "N-H ~3400, C≡C ~2200, C-H stretches "
                "2800-3100); polymer characterisation; "
                "QC of pharmaceuticals; forensic "
                "identification of unknowns; reaction "
                "monitoring (in-situ ATR probes)"
            ),
            strengths=(
                "Universal (every covalent bond is IR-active "
                "if dipole-changing); functional-group "
                "fingerprint; non-destructive; FTIR "
                "millisecond acquisition; small sample (mg)"
            ),
            limitations=(
                "Water is a strong IR absorber — aqueous "
                "samples need short path (15 µm) or D₂O "
                "substitution; symmetrical bonds (C=C in "
                "ethylene, N=N in N₂) are IR-inactive (use "
                "Raman); no concentration / quantitative "
                "info without careful calibration"
            ),
            procedure=(
                "Background scan (clean salt window or empty "
                "ATR crystal) → sample scan → ratio gives "
                "the absorption spectrum.  For solids on KBr: "
                "grind 1-2 mg sample with 100 mg KBr; press "
                "with a hydraulic press at 10 tons; mount "
                "the disc in the beam path."
            ),
            notes=(
                "OrgChem Studio also ships an IR-band "
                "*predictor* in `core/spectroscopy.py` "
                "(Phase 4) — paste a SMILES and get the "
                "expected band table.  Predictor uses "
                "26 SMARTS-matched functional-group rules "
                "covering the Silverstein / Pretsch teaching "
                "chart."
            ),
        ),
        SpectrophotometryMethod(
            id="atr_ftir",
            name="Attenuated total reflectance FTIR",
            abbreviation="ATR-FTIR",
            category="molecular-ir",
            principle=(
                "FTIR measured via an evanescent wave "
                "penetrating ~1-2 µm into a sample pressed "
                "against a high-refractive-index crystal "
                "(diamond, Ge, ZnSe).  Light totally-"
                "internally-reflects through the crystal; the "
                "evanescent component extends into the sample "
                "and gets absorbed wherever the sample has IR-"
                "active vibrations."
            ),
            light_source=(
                "Same Globar / mercury source as transmission "
                "FTIR (the ATR accessory bolts onto a "
                "standard FTIR instrument)"
            ),
            sample_handling=(
                "Place sample directly on the ATR crystal; "
                "press down for solids (clamp + force gauge).  "
                "Liquids: drop directly.  Films: just lay them "
                "down.  No dilution / grinding / pressing — "
                "the killer-app is *no sample prep*."
            ),
            detector=(
                "Same as transmission FTIR (DTGS or MCT)"
            ),
            wavelength_range="Same as FTIR (4000-400 cm⁻¹)",
            typical_analytes=(
                "Solids that won't make a KBr disc "
                "(elastomers, intractable polymers, leather, "
                "paint chips); liquids that would be too "
                "absorbing in transmission (aqueous solutions, "
                "neat liquids); contaminants on surfaces; "
                "real-time reaction monitoring with an "
                "in-situ probe"
            ),
            strengths=(
                "Zero sample prep — drop and read; works on "
                "intractable / opaque samples; reproducible "
                "(no path-length variation); can run aqueous "
                "samples (only 1-2 µm penetration depth keeps "
                "water absorbance manageable); same FTIR "
                "spectrometer + library can be used"
            ),
            limitations=(
                "Penetration depth is wavelength-dependent — "
                "spectra differ slightly from transmission "
                "(longer wavelengths penetrate further → "
                "intensity skewed); shallow depth means "
                "surface contamination dominates; crystal "
                "must be cleaned between samples"
            ),
            procedure=(
                "Background scan (clean dry crystal) → place "
                "sample on crystal (clamp solids, drop "
                "liquids) → sample scan → ratio."
            ),
            notes=(
                "Diamond crystals have replaced ZnSe / Ge in "
                "modern instruments — diamond is mechanically "
                "robust (won't scratch from hard solids), "
                "chemically inert (won't dissolve in "
                "aggressive solvents), and has a wider "
                "spectral window."
            ),
        ),
        SpectrophotometryMethod(
            id="nir",
            name="Near-infrared spectrophotometry",
            abbreviation="NIR",
            category="molecular-ir",
            principle=(
                "Higher-frequency overtones + combination "
                "bands of mid-IR fundamentals.  Bands are "
                "much weaker (10-100×) than mid-IR but "
                "broader and overlapping — interpretation "
                "requires multivariate chemometrics (PLS, "
                "PCA) rather than peak-by-peak assignment."
            ),
            light_source=(
                "Tungsten-halogen lamp (broadband 800-2500 nm)"
            ),
            sample_handling=(
                "Solids reflect NIR with high efficiency — "
                "diffuse-reflectance NIR (DR-NIR) lets you "
                "scan tablets / powders / grain through a "
                "sample-port window without any prep at all.  "
                "Liquids in 1-cm or 1-mm cuvettes (water "
                "absorbs less in NIR than mid-IR)."
            ),
            detector=(
                "InGaAs photodiode (room temperature, "
                "800-1700 nm); extended InGaAs or PbS for "
                "longer wavelengths"
            ),
            wavelength_range="800-2500 nm (12500-4000 cm⁻¹)",
            typical_analytes=(
                "Pharmaceutical QA — content uniformity of "
                "tablets, excipient verification, identity "
                "confirmation through blister packs (no "
                "destructive sampling); agricultural QA — "
                "moisture / protein / starch / oil in grain; "
                "polymer composition; petrochemical octane "
                "rating; clinical glucose monitoring "
                "(hand-held devices)"
            ),
            strengths=(
                "Rapid (<1 s spectrum); non-destructive; "
                "non-invasive (through-package, through-skin); "
                "no sample prep for solids; portable hand-"
                "held instruments are cheap (<$10k); "
                "PAT-friendly (process analytical technology)"
            ),
            limitations=(
                "Broad overlapping bands — NEED chemometric "
                "calibration model built from a training set "
                "of representative samples; less specific than "
                "mid-IR; calibration transferability between "
                "instruments is poor"
            ),
            procedure=(
                "Build calibration model on a training set "
                "with known reference values (HPLC, gravimetry, "
                "etc.).  Scan unknown sample.  Apply model "
                "(PLS regression / PCA / SIMCA classification)."
            ),
            notes=(
                "Pulse-oximeters use a 2-wavelength NIR "
                "approach (660 nm + 940 nm) to derive SpO₂ "
                "from oxy- vs deoxy-haemoglobin absorbance — "
                "a simplified single-purpose NIR application "
                "now ubiquitous in clinical care."
            ),
        ),
        SpectrophotometryMethod(
            id="raman",
            name="Raman spectroscopy",
            abbreviation="Raman",
            category="molecular-ir",
            principle=(
                "Inelastic scattering of monochromatic laser "
                "light off molecular vibrations.  Most "
                "scattered photons are elastic (Rayleigh, "
                "same wavelength); a small fraction "
                "(~1 in 10⁷) are shifted in wavelength by "
                "the energy of a vibrational quantum (Stokes "
                "shift).  Selection rule: Raman-active "
                "vibrations CHANGE THE POLARISABILITY (vs "
                "IR's dipole-moment-change rule), making "
                "Raman complementary — symmetric stretches "
                "(C=C, S-S, C-S) that are IR-weak are "
                "Raman-strong."
            ),
            light_source=(
                "Continuous-wave laser: 532 nm (green, "
                "biological samples — but fluorescent "
                "background risk); 633 nm (HeNe red); 785 nm "
                "(NIR, low fluorescence); 1064 nm "
                "(deep NIR, FT-Raman)"
            ),
            sample_handling=(
                "Direct illumination — solids, liquids, gases, "
                "thin films, all without prep.  Glass / quartz "
                "vials transparent to most laser wavelengths.  "
                "Aqueous samples work fine (water is a poor "
                "Raman scatterer)."
            ),
            detector=(
                "CCD (charge-coupled device, scientific "
                "grade with cooling for low dark current); "
                "InGaAs for FT-Raman"
            ),
            wavelength_range=(
                "Raman shifts 100-4000 cm⁻¹ (relative to "
                "the laser line; absolute wavelength depends "
                "on laser)"
            ),
            typical_analytes=(
                "Polymorph identification in pharmaceutical "
                "solids (crystal-form fingerprint); carbon "
                "characterisation (graphene, graphite, "
                "diamond, amorphous carbon — all distinguish "
                "by their characteristic G / D / 2D bands); "
                "pigments + minerals (art / archaeology "
                "non-destructive ID); biological tissue "
                "imaging (Raman microscopy); aqueous "
                "samples (where IR is hopeless)"
            ),
            strengths=(
                "Complementary selection rule to IR — "
                "covers the symmetric / non-polar bonds IR "
                "misses; aqueous-sample friendly; no sample "
                "prep; through-glass / through-vial measurement; "
                "high spatial resolution in microscopy "
                "(<1 µm)"
            ),
            limitations=(
                "Inherently weak signal (10⁷ photons in for "
                "1 Raman photon out) — fluorescent samples "
                "swamp the Raman signal entirely; expensive "
                "instrument ($30-100k+); laser power can "
                "burn dark / pigmented samples; sample "
                "heating from focused laser"
            ),
            procedure=(
                "Choose laser wavelength to balance Raman "
                "cross-section (∝ 1/λ⁴ — shorter λ stronger) "
                "vs fluorescence risk (longer λ less "
                "fluorescence).  Focus laser on sample; "
                "collect scattered light through a notch "
                "filter (rejects Rayleigh) into the "
                "spectrometer."
            ),
            notes=(
                "Surface-enhanced Raman (SERS — see separate "
                "entry) uses gold / silver nanoparticles to "
                "boost the Raman cross-section by 10⁶-10⁸×, "
                "bringing single-molecule detection into "
                "reach.  CARS (coherent anti-Stokes Raman) "
                "and SRS (stimulated Raman scattering) are "
                "non-linear variants used in label-free "
                "biological imaging."
            ),
        ),
        SpectrophotometryMethod(
            id="sers",
            name="Surface-enhanced Raman scattering",
            abbreviation="SERS",
            category="molecular-ir",
            principle=(
                "Raman cross-section enhancement of 10⁴-10⁸× "
                "when the analyte adsorbs on or near a "
                "roughened noble-metal surface (gold, silver) "
                "or nanoparticle.  Mechanism is a combination "
                "of electromagnetic enhancement (plasmon "
                "resonance amplifies the local field) and "
                "chemical enhancement (charge transfer with "
                "the metal).  Single-molecule detection is "
                "achievable at hot-spots between adjacent "
                "nanoparticles."
            ),
            light_source=(
                "Visible / NIR laser tuned to the metal "
                "nanoparticle plasmon resonance (Au: ~530 nm "
                "for spheres, red-shifted for rods + "
                "aggregates; Ag: ~400 nm)"
            ),
            sample_handling=(
                "Mix analyte with colloidal Au or Ag "
                "nanoparticle suspension; or deposit analyte "
                "on a SERS-active substrate (Klarite, "
                "Q-SERS — engineered nanoarrays); or "
                "evaporate analyte on a roughened metal foil"
            ),
            detector=(
                "Same CCD as conventional Raman (the "
                "enhancement factor compensates for low "
                "Raman cross-section)"
            ),
            wavelength_range=(
                "Same Raman shift range (100-4000 cm⁻¹), "
                "absolute wavelength tied to laser"
            ),
            typical_analytes=(
                "Trace explosives (TNT, RDX) at ng / mL; "
                "drugs of abuse (cocaine, methamphetamine); "
                "mycotoxins / food contaminants; clinical "
                "biomarkers in serum / urine; environmental "
                "pollutants — anywhere ppb sensitivity is "
                "needed for a Raman-active analyte"
            ),
            strengths=(
                "10⁴-10⁸× sensitivity boost over conventional "
                "Raman; single-molecule detection in "
                "favourable cases; works in aqueous samples; "
                "portable handheld SERS instruments commercial"
            ),
            limitations=(
                "Reproducibility is the biggest problem — "
                "enhancement varies enormously between hot-"
                "spots; quantitation requires careful internal "
                "standards; analyte must adsorb on the metal "
                "(non-binding analytes get no enhancement); "
                "Ag substrates oxidise; expensive "
                "engineered substrates"
            ),
            procedure=(
                "Mix sample with nanoparticle colloid in a "
                "1-cm cuvette OR pipette sample onto a SERS "
                "substrate.  Allow ~5 min for analyte "
                "adsorption.  Acquire Raman spectrum with "
                "low laser power to avoid analyte "
                "destruction."
            ),
            notes=(
                "TERS (tip-enhanced Raman spectroscopy) brings "
                "SERS to AFM-tip resolution (<10 nm), enabling "
                "single-cell + sub-organelle Raman imaging."
            ),
        ),

        # ---- Molecular chirality ----
        SpectrophotometryMethod(
            id="cd",
            name="Circular dichroism spectroscopy",
            abbreviation="CD",
            category="molecular-chirality",
            principle=(
                "Differential absorbance of left- vs right-"
                "circularly-polarised light by chiral "
                "molecules: ∆A = A_L - A_R.  Reported as "
                "molar circular dichroism ∆ε (M⁻¹·cm⁻¹) or "
                "as ellipticity θ (degrees, related by "
                "θ = 32.98 · ∆ε · l · c).  Achiral molecules "
                "give zero CD signal."
            ),
            light_source=(
                "Xenon arc lamp (170-1100 nm) modulated by "
                "a photoelastic modulator (PEM) at ~50 kHz "
                "to alternate left- vs right-circularly-"
                "polarised light through the sample"
            ),
            sample_handling=(
                "Quartz cuvettes — same as UV-Vis but "
                "demountable / cylindrical for short path "
                "lengths.  Path length 0.01-1 cm chosen so "
                "absorbance ≤ 1 at every wavelength of "
                "interest.  Buffer must be CD-transparent — "
                "phosphate is fine, Tris is questionable, "
                "NaCl high concentrations OK; aromatic "
                "buffers are not."
            ),
            detector=(
                "Photomultiplier tube — same as UV-Vis but "
                "with phase-sensitive detection at the PEM "
                "modulation frequency to extract the ∆A "
                "signal from the much larger total absorbance"
            ),
            wavelength_range="180-700 nm",
            typical_analytes=(
                "Protein secondary structure (far-UV "
                "180-260 nm; α-helix gives a characteristic "
                "double minimum at 208 + 222 nm; β-sheet "
                "gives a single minimum at ~218 nm; random "
                "coil gives a strong minimum at ~200 nm); "
                "DNA / RNA conformation (B-form vs A-form "
                "vs Z-form fingerprints); ligand binding "
                "(induced CD on chromophores in chiral "
                "binding sites); enantiomer ratio in chiral "
                "drugs; conformational dynamics monitoring"
            ),
            strengths=(
                "Direct readout of chirality / secondary "
                "structure; works in solution under near-"
                "physiological conditions; sensitive to "
                "conformational changes (folding, ligand "
                "binding, denaturation); deconvolution "
                "algorithms (CONTIN, SELCON, K2D) give "
                "quantitative α / β / coil percentages"
            ),
            limitations=(
                "Low intrinsic signal — needs μM-mM protein "
                "(~0.1-1 mg/mL); UV-buffer-transparent system "
                "limits the buffer choice; aggregation / "
                "scattering distorts spectra; not specific "
                "to a single residue (an ensemble average)"
            ),
            procedure=(
                "Blank with buffer in matched cuvette.  "
                "Scan sample over the wavelength range of "
                "interest (typically 190-260 nm for protein "
                "secondary-structure work) at 0.5 nm step "
                "with ~3-second response time; average 3-5 "
                "scans for noise reduction.  Subtract buffer "
                "blank.  Convert raw ellipticity (mdeg) to "
                "mean residue ellipticity for protein analysis."
            ),
            notes=(
                "Vibrational CD (VCD) extends the technique "
                "into the IR region (1800-800 cm⁻¹) for "
                "absolute-configuration determination of "
                "small-molecule chiral drugs — increasingly "
                "used in pharmaceutical industry as an "
                "alternative to X-ray crystallography of "
                "heavy-atom derivatives."
            ),
        ),

        # ---- Atomic spectroscopy ----
        SpectrophotometryMethod(
            id="aas",
            name="Atomic absorption spectroscopy",
            abbreviation="AAS",
            category="atomic",
            principle=(
                "Atomise the sample (dissolve in flame or "
                "graphite furnace) so analyte exists as "
                "free ground-state atoms; pass narrow-line "
                "light from a hollow-cathode lamp specific to "
                "that element; ground-state atoms absorb the "
                "characteristic resonance wavelength.  "
                "Quantitation by Beer-Lambert."
            ),
            light_source=(
                "Hollow-cathode lamp (HCL) — element-specific "
                "(one lamp per element, or multi-element "
                "lamps for ~5 metals); newer continuum-source "
                "AAS instruments use a high-intensity xenon "
                "arc + high-resolution spectrometer to "
                "measure all elements with one lamp"
            ),
            sample_handling=(
                "Liquid sample (acid digest of solid).  "
                "Aspirated into a flame (flame AAS, ppm "
                "sensitivity) or injected into a graphite "
                "furnace (GFAAS, ppb sensitivity, much "
                "smaller sample volume of ~20 µL)"
            ),
            detector=(
                "Photomultiplier tube (UV-Vis range)"
            ),
            wavelength_range=(
                "190-900 nm; each element has 1-3 useful "
                "resonance lines"
            ),
            typical_analytes=(
                "Metal trace analysis: lead in drinking water "
                "(EPA Method 200.7 / 200.9), iron in serum, "
                "copper / zinc in supplements, "
                "calcium / magnesium in food, environmental "
                "trace metals.  ~70 elements addressable "
                "(metals + metalloids; non-metals not "
                "addressable by AAS)."
            ),
            strengths=(
                "Excellent ppm-ppb sensitivity for individual "
                "metals; element-specific (chemical "
                "interferences low); cheap (~$30-50k flame "
                "AAS); robust workhorse for environmental + "
                "regulatory labs"
            ),
            limitations=(
                "One element at a time (slow for multi-element "
                "panels); HCL changes between elements; "
                "matrix interferences (especially in "
                "graphite furnace); element coverage limited "
                "(non-metals / halogens not addressable)"
            ),
            procedure=(
                "Install element-specific HCL.  Set spectrometer "
                "to resonance line.  Aspirate aqueous standards "
                "(0.1, 0.5, 1, 5 ppm) to build calibration "
                "curve.  Aspirate sample.  Read absorbance + "
                "convert to concentration via curve."
            ),
            notes=(
                "Cold-vapour AAS (CV-AAS) is the standard "
                "method for mercury — Hg²⁺ is reduced to "
                "elemental Hg vapour by SnCl₂, then "
                "transported into a quartz absorption cell.  "
                "Hydride generation AAS (HG-AAS) does the "
                "same trick for As, Se, Sb, Sn, Te (the "
                "hydride-forming elements)."
            ),
        ),
        SpectrophotometryMethod(
            id="icp_oes",
            name="Inductively-coupled-plasma optical emission",
            abbreviation="ICP-OES",
            category="atomic",
            principle=(
                "Argon plasma (8000-10000 K) atomises and "
                "excites the sample.  As the excited atoms "
                "relax, they emit element-specific "
                "wavelengths.  An echelle spectrometer + 2D "
                "CCD detector captures all wavelengths "
                "simultaneously, giving multi-element "
                "analysis in a single run."
            ),
            light_source=(
                "(self-emitted) — the plasma IS the source.  "
                "RF generator (1-2 kW, 27 or 40 MHz) "
                "induces eddy currents in argon flowing "
                "through a torch, creating the plasma."
            ),
            sample_handling=(
                "Aqueous sample aspirated by a peristaltic "
                "pump → nebuliser → spray chamber → torch.  "
                "Solids must be acid-digested (HNO₃ + HCl "
                "+ HF as needed; microwave digestion in "
                "modern labs) to a clear liquid."
            ),
            detector=(
                "Echelle / cross-disperser polychromator + "
                "2D CCD, OR sequential monochromator with PMT"
            ),
            wavelength_range="160-900 nm (vacuum-UV to NIR)",
            typical_analytes=(
                "Multi-element trace metal panels in "
                "environmental water, soil, food, biological "
                "fluids; geological + mineralogical "
                "characterisation; metals in oils + "
                "lubricants; ICH Q3D heavy-metals testing "
                "for pharmaceutical raw materials"
            ),
            strengths=(
                "Multi-element (60+ elements simultaneously); "
                "wide linear dynamic range (5-6 orders of "
                "magnitude); ppm-ppb sensitivity; low "
                "chemical interferences; automated"
            ),
            limitations=(
                "Higher capital cost than AAS (~$100-200k); "
                "argon consumption (~10 L/min during runs); "
                "not as sensitive as ICP-MS for the "
                "lowest-trace elements; spectral "
                "interferences require careful line "
                "selection"
            ),
            procedure=(
                "Daily calibration with multi-element "
                "standards (NIST-traceable).  Acid-digest "
                "samples to clear liquid.  Aspirate; the "
                "instrument scans pre-selected lines for "
                "every element of interest in one ~2-minute "
                "acquisition.  Internal standard (Sc, Y, In, "
                "Bi) corrects for matrix-induced drift."
            ),
            notes=(
                "Axial-view torches (light collected along "
                "the plasma axis) give 5-10× better "
                "sensitivity than radial; modern instruments "
                "switch dynamically between views per element "
                "to balance sensitivity vs interference."
            ),
        ),
        SpectrophotometryMethod(
            id="icp_ms",
            name="Inductively-coupled-plasma mass spectrometry",
            abbreviation="ICP-MS",
            category="atomic",
            principle=(
                "Same argon plasma as ICP-OES (8000-10000 K) "
                "but ions extracted from the plasma into a "
                "vacuum mass spectrometer instead of being "
                "detected via emission.  Quadrupole or TOF "
                "MS separates by m/z, giving unambiguous "
                "isotope assignment + ultra-trace "
                "sensitivity."
            ),
            light_source=(
                "Same RF-induced argon plasma as ICP-OES — "
                "but the plasma's role here is ionisation, "
                "not emission"
            ),
            sample_handling=(
                "Same as ICP-OES: aqueous sample, "
                "peristaltic pump, nebuliser, spray "
                "chamber, torch.  Cleaner samples needed "
                "than ICP-OES (high salt loads cone-foul)."
            ),
            detector=(
                "Quadrupole MS (most common, sequential m/z "
                "scan); TOF-MS (full m/z scan in <100 µs, "
                "isotope ratios); high-resolution sector-"
                "field MS (for isobaric interferences)"
            ),
            wavelength_range=(
                "N/A — MS is m/z-based, not wavelength-based.  "
                "Mass range typically 5-260 amu."
            ),
            typical_analytes=(
                "Ultra-trace metals (ppt-ppq sensitivity for "
                "many elements); isotope-ratio analysis "
                "(geochronology — Pb/U dating, "
                "biogeochemistry — δ¹³C / δ¹⁵N proxies for "
                "ICP-MS-compatible elements); single-cell "
                "analysis (mass cytometry / CyTOF); "
                "speciation analysis with HPLC / GC pre-"
                "separation"
            ),
            strengths=(
                "ppt-ppq sensitivity (1000× better than "
                "ICP-OES for many elements); isotope ratios "
                "to 0.01 % precision; multi-element + "
                "isobaric resolution; can be coupled to "
                "HPLC / GC / single-cell sources"
            ),
            limitations=(
                "Most expensive of the atomic methods "
                "($300-800k); polyatomic interferences "
                "(ArO⁺ at m/z 56 swamps ⁵⁶Fe — needs "
                "collision cell with He / H₂); cones / "
                "skimmers wear out + need cleaning; sample "
                "TDS must be < 0.2 % to avoid clogging"
            ),
            procedure=(
                "Same sample-prep workflow as ICP-OES but "
                "with stricter cleanliness.  Tune the "
                "instrument daily on a multi-element tune "
                "solution.  Use collision-cell mode (He) "
                "for elements with polyatomic interferences "
                "(Fe, As, V, Cr).  Internal standards "
                "(Sc, Y, In, Bi) correct drift."
            ),
            notes=(
                "Triple-quadrupole ICP-MS (e.g. Agilent "
                "8900) adds a reaction cell that chemically "
                "shifts polyatomic interferences off the "
                "analyte mass — extends the technique into "
                "previously impossible isotopes (³²S, ³¹P)."
            ),
        ),

        # ---- Magnetic resonance ----
        SpectrophotometryMethod(
            id="nmr",
            name="Nuclear magnetic resonance spectroscopy",
            abbreviation="NMR",
            category="magnetic-resonance",
            principle=(
                "Nuclei with non-zero spin (¹H, ¹³C, ¹⁵N, "
                "¹⁹F, ³¹P, …) precess in a strong magnetic "
                "field at the Larmor frequency.  An RF pulse "
                "tilts the nuclear magnetisation; precessing "
                "magnetisation induces a free induction "
                "decay (FID) in the receiver coil.  Fourier "
                "transform of the FID gives a spectrum where "
                "each chemically distinct nucleus appears at "
                "its own frequency (chemical shift) — the "
                "single most powerful structural-elucidation "
                "tool in organic chemistry."
            ),
            light_source=(
                "(none — RF rather than light).  RF coil + "
                "transmitter at the nucleus's Larmor "
                "frequency (¹H: 400-900 MHz at 9.4-21.1 T)"
            ),
            sample_handling=(
                "Sample dissolved in deuterated solvent "
                "(CDCl₃, DMSO-d₆, D₂O, MeOD-d₄, …) in a "
                "5-mm o.d. precision NMR tube.  Need ~10 mg "
                "in 0.5 mL for routine ¹H + ¹³C; modern "
                "cryo-probe instruments do ¹H NMR on "
                "<1 mg / 50 µL.  Long-term sample stability "
                "in solution required (NMR runs are "
                "minutes to overnight)."
            ),
            detector=(
                "RF coil (transmit + receive); pre-"
                "amplifier; ADC; digital signal-processing "
                "chain.  Cryogenically cooled probes "
                "improve signal-to-noise 4× for the same "
                "field."
            ),
            wavelength_range=(
                "RF: 50-1000 MHz typical (the value depends "
                "on field strength: H Larmor freq ≈ 42.58 "
                "MHz/T)"
            ),
            typical_analytes=(
                "Organic / pharmaceutical compounds — "
                "structural elucidation (1D ¹H + ¹³C; 2D "
                "COSY / HSQC / HMBC / NOESY); reaction "
                "monitoring (real-time ¹H NMR); ligand-"
                "binding affinity (STD-NMR / WaterLOGSY); "
                "protein structure determination "
                "(15N-HSQC, ¹⁵N/¹³C-labelled samples, "
                "TROSY for proteins > 30 kDa); metabolomics"
            ),
            strengths=(
                "Most informative single technique for "
                "structure elucidation — each ¹H / ¹³C "
                "nucleus reports its own chemical environment; "
                "non-destructive (sample recoverable); "
                "quantitative (peak area ∝ nucleus count); "
                "2D experiments establish through-bond "
                "(COSY / HMBC) + through-space (NOESY) "
                "connectivity; works in solution under "
                "physiological conditions (protein NMR)"
            ),
            limitations=(
                "Inherently insensitive (~10⁻⁵ vs UV) — "
                "needs mg amounts for ¹³C, mM concentrations "
                "for protein NMR; expensive instrument "
                "(>$500k for a 400-MHz; >$5M for 900-MHz "
                "+ cryo-probe); slow (1D ¹H ~1 min, "
                "2D HSQC 30 min, 3D protein experiments days); "
                "requires deuterated solvent + reference "
                "(TMS / DSS)"
            ),
            procedure=(
                "Dissolve sample in deuterated solvent; "
                "transfer to NMR tube; insert into magnet.  "
                "Lock on deuterium signal; shim for line "
                "narrowing.  Run 1D ¹H (90° pulse + "
                "acquire); for ¹³C add NOE saturation + "
                "decoupling.  For 2D experiments program a "
                "specific pulse sequence (COSY: 90°-t1-90°-"
                "acquire; HSQC: heteronuclear chemical-shift "
                "correlation; NOESY: through-space)."
            ),
            notes=(
                "OrgChem Studio also ships an NMR-shift "
                "*predictor* in `core/nmr.py` — paste a "
                "SMILES and get expected ¹H + ¹³C shifts "
                "from a SMARTS environment table.  HSQC + "
                "HMBC predictors are the natural follow-up.  "
                "The 2002 Nobel Prize (MRI) and 1991 Nobel "
                "(2D NMR — Ernst) testify to NMR's "
                "central role in modern science."
            ),
        ),
    ]


_METHODS: List[SpectrophotometryMethod] = _build_catalogue()


# ------------------------------------------------------------------
# Public lookup helpers
# ------------------------------------------------------------------

def list_methods(category: Optional[str] = None
                 ) -> List[SpectrophotometryMethod]:
    if category is None:
        return list(_METHODS)
    if category not in VALID_CATEGORIES:
        return []
    return [m for m in _METHODS if m.category == category]


def get_method(method_id: str) -> Optional[SpectrophotometryMethod]:
    for m in _METHODS:
        if m.id == method_id:
            return m
    return None


def find_methods(needle: str) -> List[SpectrophotometryMethod]:
    """Case-insensitive substring search across id / name /
    abbreviation."""
    if not needle:
        return []
    n = needle.lower().strip()
    out: List[SpectrophotometryMethod] = []
    for m in _METHODS:
        if (n in m.id.lower()
                or n in m.name.lower()
                or n in m.abbreviation.lower()):
            out.append(m)
    return out


def categories() -> List[str]:
    return list(VALID_CATEGORIES)


def to_dict(m: SpectrophotometryMethod) -> Dict[str, str]:
    return {
        "id": m.id,
        "name": m.name,
        "abbreviation": m.abbreviation,
        "category": m.category,
        "principle": m.principle,
        "light_source": m.light_source,
        "sample_handling": m.sample_handling,
        "detector": m.detector,
        "wavelength_range": m.wavelength_range,
        "typical_analytes": m.typical_analytes,
        "strengths": m.strengths,
        "limitations": m.limitations,
        "procedure": m.procedure,
        "notes": m.notes,
    }
