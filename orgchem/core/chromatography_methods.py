"""Phase 37c (round 138) — chromatography-method catalogue.

Headless reference data for the *Tools → Chromatography
techniques…* dialog.  Each entry describes a separation method
— principle, stationary + mobile phase, detector(s), typical
analytes, strengths / limitations, and a one-paragraph
procedure summary.

Categories
----------
- ``"planar"`` — TLC, paper.
- ``"preparative-column"`` — gravity column, flash.
- ``"gas"`` — GC, GC-MS.
- ``"liquid"`` — HPLC, LC-MS, HILIC, reverse-phase.
- ``"protein"`` — FPLC, SEC, IEX, affinity.
- ``"ion"`` — ion chromatography.
- ``"supercritical"`` — SFC.

This is reference data for teaching, not a method-development
tool.  Real-world chromatography is dominated by column / mobile-
phase / detector trade-offs that students need to internalise
before they can pick a method for a given separation problem;
the catalogue is structured so each row surfaces those
trade-offs explicitly via the ``strengths`` + ``limitations``
fields.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass(frozen=True)
class ChromatographyMethod:
    id: str
    name: str
    abbreviation: str
    category: str
    principle: str
    stationary_phase: str
    mobile_phase: str
    detectors: str            # comma-separated list
    typical_analytes: str
    strengths: str
    limitations: str
    procedure: str
    notes: str = ""


VALID_CATEGORIES: tuple = (
    "planar", "preparative-column", "gas",
    "liquid", "protein", "ion", "supercritical",
)


# ------------------------------------------------------------------
# Catalogue
# ------------------------------------------------------------------

def _build_catalogue() -> List[ChromatographyMethod]:
    return [
        # ---- Planar ----
        ChromatographyMethod(
            id="tlc",
            name="Thin-layer chromatography",
            abbreviation="TLC",
            category="planar",
            principle=(
                "Adsorption equilibrium between the analyte, "
                "a polar stationary phase coated on a thin "
                "plate, and a less-polar mobile phase rising by "
                "capillary action.  Retention factor "
                "Rf = (distance migrated by spot) / (distance "
                "migrated by solvent front), 0 < Rf < 1."
            ),
            stationary_phase=(
                "Silica gel (most common; SiO₂ with surface "
                "Si-OH groups) or alumina (Al₂O₃) coated 0.1-"
                "0.25 mm thick on a glass / Al / plastic backing"
            ),
            mobile_phase=(
                "Single solvent or graded mixture chosen for "
                "polarity (e.g. hexane / EtOAc; CHCl₃ / MeOH).  "
                "Eluotropic series: hexane < toluene < CH₂Cl₂ "
                "< EtOAc < acetone < MeOH < H₂O."
            ),
            detectors=(
                "UV lamp (254 / 365 nm; uses fluorescent F254 "
                "indicator on the plate); iodine vapour "
                "(general); ninhydrin (amino acids); "
                "phosphomolybdic acid (general char); "
                "ceric ammonium molybdate (general char)"
            ),
            typical_analytes=(
                "Reaction-progress monitoring; small organic "
                "molecules (MW 50-1000); natural-product "
                "fractions; amino acids; fast purity check"
            ),
            strengths=(
                "Cheap, fast (<10 min/run), parallel "
                "(multiple lanes / spots per plate), tiny "
                "sample requirement (μg), no instrument "
                "needed, enables multiple visualisation "
                "stains in sequence"
            ),
            limitations=(
                "Qualitative-to-semi-quantitative only; Rf "
                "varies with humidity / temperature / plate "
                "lot; non-volatile / non-UV-active "
                "compounds need stains; resolution limited "
                "(10-20 plates equivalent)"
            ),
            procedure=(
                "Spot ~1 μL of analyte solution near the "
                "bottom edge of the plate.  Place plate in a "
                "developing chamber containing solvent up to "
                "below the spots.  Cover; let solvent rise by "
                "capillary action.  Remove when the front "
                "approaches the top.  Mark the front, dry, "
                "visualise."
            ),
            notes=(
                "2D-TLC (run a second eluent perpendicular "
                "after rotating the plate) doubles peak "
                "capacity for complex mixtures.  HPTLC (high-"
                "performance TLC) uses 2-5 μm particle plates "
                "for sharper spots and quantitative density "
                "scanning."
            ),
        ),
        ChromatographyMethod(
            id="paper",
            name="Paper chromatography",
            abbreviation="Paper",
            category="planar",
            principle=(
                "Partition between water trapped in cellulose "
                "fibres (stationary phase) and an organic "
                "mobile phase, OR adsorption on the cellulose "
                "OH groups for very polar mobile phases."
            ),
            stationary_phase=(
                "Cellulose paper (Whatman No. 1 / 3MM) — "
                "water held within the cellulose matrix"
            ),
            mobile_phase=(
                "Polar solvents (n-butanol / acetic acid / "
                "water for amino acids; phenol / water for "
                "sugars)"
            ),
            detectors=(
                "Ninhydrin (amino acids → purple); aniline / "
                "diphenylamine / phthalic acid (sugars → "
                "brown); UV; iodine"
            ),
            typical_analytes=(
                "Amino acids, sugars, plant pigments, "
                "inks / dyes — historical workhorse for "
                "biological separations before TLC"
            ),
            strengths=(
                "Even cheaper than TLC; standard biology "
                "teaching demo; long-term stable (paper "
                "lasts decades)"
            ),
            limitations=(
                "Slower than TLC (1-4 hours); diffuse spots; "
                "lower resolution; mostly displaced by TLC "
                "for serious analytical work"
            ),
            procedure=(
                "Spot analyte at one end of a paper strip; "
                "suspend strip in a chamber so its bottom "
                "edge dips into the developing solvent; let "
                "the solvent climb (ascending) or descend "
                "(descending) past the spots.  Mark the "
                "front, dry, visualise."
            ),
            notes=(
                "Two-dimensional paper chromatography (2D-"
                "PC) was the foundation method that let "
                "Sanger sequence insulin in 1955 — the first "
                "primary-structure determination of a protein."
            ),
        ),

        # ---- Preparative column ----
        ChromatographyMethod(
            id="column",
            name="Gravity column chromatography",
            abbreviation="Column",
            category="preparative-column",
            principle=(
                "Same adsorption equilibrium as TLC scaled to "
                "g-quantity preparative scale.  Components elute "
                "in order of increasing affinity for the "
                "stationary phase."
            ),
            stationary_phase=(
                "Silica gel (40-63 μm 'flash' grade or 70-230 "
                "mesh 'gravity' grade); occasionally alumina, "
                "Florisil, or reverse-phase C18 silica"
            ),
            mobile_phase=(
                "Same eluotropic series as TLC; usually a "
                "stepwise gradient (start non-polar, increase "
                "polarity) optimised against TLC of the "
                "starting material"
            ),
            detectors=(
                "TLC of every fraction; UV monitor in flash "
                "systems; charring / staining off-line"
            ),
            typical_analytes=(
                "Synthetic intermediates; natural-product "
                "isolation; mg-to-g preparative scale; "
                "anywhere a TLC-resolved mixture needs "
                "weighable separated fractions"
            ),
            strengths=(
                "Scalable from mg to kg; cheap consumables; "
                "any stationary / mobile phase the chemist "
                "can dream up; the workhorse of every "
                "synthetic-organic teaching lab"
            ),
            limitations=(
                "Slow (hours per separation); large solvent "
                "consumption; manual fraction collection; "
                "lower resolution than HPLC; column-packing "
                "skill matters"
            ),
            procedure=(
                "Slurry-pack a column with silica in the "
                "starting solvent.  Load sample (dry-load on "
                "silica or solvent-load).  Elute in fractions, "
                "monitoring each by TLC.  Combine fractions "
                "containing the same component; rotovap to "
                "isolate."
            ),
            notes=(
                "Dry-loading (adsorb the sample onto silica + "
                "load that as a solid plug at the column top) "
                "is essential for samples that don't dissolve "
                "well in the starting eluent.  Air pressure "
                "(flash) cuts run time by ~10× vs gravity."
            ),
        ),
        ChromatographyMethod(
            id="flash",
            name="Flash column chromatography",
            abbreviation="Flash",
            category="preparative-column",
            principle=(
                "Pressurised gravity column (1-3 bar air or "
                "N₂) using fine silica (40-63 μm) for higher "
                "separation efficiency at usable run times.  "
                "Modern automated systems (CombiFlash, "
                "Biotage) integrate UV detection + fraction "
                "collection."
            ),
            stationary_phase=(
                "Pre-packed disposable cartridges of 40-63 μm "
                "silica (or C18 reverse-phase); 4-1500 g sizes"
            ),
            mobile_phase=(
                "Programmed gradient (typically hexane → "
                "EtOAc, or H₂O → MeCN for reverse-phase); "
                "managed automatically"
            ),
            detectors=(
                "In-line UV (single or multi-wavelength); "
                "ELSD (evaporative light-scattering); MS in "
                "high-end systems"
            ),
            typical_analytes=(
                "Same as gravity column but with higher "
                "throughput; standard for medicinal-chemistry "
                "intermediate purification (50 mg - 50 g)"
            ),
            strengths=(
                "Fast (15-45 min); reproducible (automated "
                "gradient + fraction collection); built-in "
                "UV detection; disposable cartridges = no "
                "column-packing skill needed"
            ),
            limitations=(
                "Cartridges + instrument cost (~$50k for an "
                "automated system); UV-only detection "
                "misses non-chromophoric compounds; gradient "
                "method development still required"
            ),
            procedure=(
                "Equilibrate cartridge in starting solvent.  "
                "Load sample (liquid or dry-loaded).  Run "
                "programmed gradient.  System collects "
                "fractions automatically when UV signal "
                "exceeds a user-set threshold."
            ),
            notes=(
                "Reverse-phase flash (C18) is the modern "
                "alternative to normal-phase silica for "
                "polar compounds + water-soluble natural "
                "products."
            ),
        ),

        # ---- Gas ----
        ChromatographyMethod(
            id="gc",
            name="Gas chromatography",
            abbreviation="GC",
            category="gas",
            principle=(
                "Volatile analytes partition between an inert "
                "carrier-gas mobile phase and a thin liquid / "
                "polymer film coating the inside of a long "
                "capillary column.  Separation order is by "
                "volatility (boiling point) modulated by "
                "stationary-phase polarity.  Each peak's "
                "retention time at fixed conditions is a "
                "fingerprint."
            ),
            stationary_phase=(
                "Capillary column (typically 15-60 m × 0.25 "
                "mm i.d., 0.25 μm film thickness): non-polar "
                "5%-phenyl-methylpolysiloxane (DB-5/HP-5) for "
                "general use; polar polyethylene-glycol "
                "(DB-Wax) for alcohols / acids; chiral "
                "cyclodextrin phases for enantiomers"
            ),
            mobile_phase=(
                "He, H₂, or N₂ carrier gas at 1-3 mL/min — "
                "doesn't interact with analytes, only "
                "transports them"
            ),
            detectors=(
                "FID (universal for organics, ng sensitivity, "
                "log-linear over 6 orders); ECD (halogens / "
                "organochlorines, pg sensitivity); TCD "
                "(universal but less sensitive); NPD "
                "(N / P-containing); MS (structural ID)"
            ),
            typical_analytes=(
                "Volatile organics (BP < 350 °C without "
                "decomposition); fatty-acid methyl esters; "
                "essential oils; petrochemicals; "
                "environmental VOCs; arson investigation"
            ),
            strengths=(
                "High resolution (capillary columns: 100k+ "
                "theoretical plates); ng-pg sensitivity with "
                "ECD / MS; absolute retention-time "
                "reproducibility; inexpensive consumables; "
                "fast (5-30 min per run)"
            ),
            limitations=(
                "Only volatile + thermally stable analytes "
                "(BP < ~350 °C); polar compounds need "
                "derivatisation (e.g. silylation); not "
                "applicable to most peptides / proteins / "
                "ionic species"
            ),
            procedure=(
                "Inject 1 μL of dilute sample via a heated "
                "split / splitless injector.  Carrier gas "
                "sweeps the analyte through the column under "
                "a programmed temperature ramp (e.g. 50 °C "
                "→ 280 °C at 10 °C/min).  Detector signal "
                "vs time = chromatogram."
            ),
            notes=(
                "Kovats retention indices (referenced against "
                "n-alkane standards) make GC retention "
                "transferable across labs / instruments — the "
                "library backbone of NIST / Wiley spectral "
                "libraries."
            ),
        ),
        ChromatographyMethod(
            id="gc_ms",
            name="Gas chromatography - mass spectrometry",
            abbreviation="GC-MS",
            category="gas",
            principle=(
                "GC separation followed by MS structural / "
                "quantitative detection.  Each chromatographic "
                "peak fragments through the EI source giving a "
                "library-searchable mass spectrum."
            ),
            stationary_phase=(
                "Same capillary GC columns as plain GC; MS-"
                "compatible (low bleed)"
            ),
            mobile_phase=(
                "He carrier (low ionisation cross-section, "
                "MS-friendly)"
            ),
            detectors=(
                "Quadrupole MS (EI ionisation, m/z 30-650); "
                "ion-trap; time-of-flight (high-resolution); "
                "triple-quadrupole (MRM for quantitation)"
            ),
            typical_analytes=(
                "Same as GC but with mass-spectral structural "
                "ID; forensic toxicology, environmental "
                "monitoring, doping control, metabolomics, "
                "essential-oil profiling"
            ),
            strengths=(
                "Combines GC's separation power with MS's "
                "structural ID; NIST library search → "
                "instant identification for known compounds; "
                "selected-ion monitoring (SIM) gives ppb / "
                "ppt sensitivity"
            ),
            limitations=(
                "Same volatility constraints as GC; MS adds "
                "instrument cost ($50-200k) + complexity; "
                "EI fragmentation can obscure molecular ion "
                "(use CI or soft ionisation)"
            ),
            procedure=(
                "Same as GC injection; column effluent enters "
                "the MS via a heated transfer line.  EI source "
                "ionises + fragments analytes; quadrupole / "
                "TOF separates by m/z; data system reconstructs "
                "extracted-ion chromatograms + library searches "
                "each peak."
            ),
            notes=(
                "MRM (multiple reaction monitoring) on triple-"
                "quadrupole instruments achieves orders-of-"
                "magnitude lower LOD than full-scan, at the "
                "cost of restricting analysis to pre-selected "
                "transitions."
            ),
        ),

        # ---- Liquid (HPLC family) ----
        ChromatographyMethod(
            id="hplc",
            name="High-performance liquid chromatography",
            abbreviation="HPLC",
            category="liquid",
            principle=(
                "Sample dissolved in a liquid mobile phase is "
                "pumped at high pressure (5-400 bar) through a "
                "column packed with very fine particles (1.7-"
                "5 μm).  Separation by partition / adsorption "
                "between the mobile phase + a chemically-bonded "
                "stationary phase.  Most modern work is "
                "reverse-phase (RP-HPLC) — non-polar C18 "
                "stationary phase, polar (water/MeCN) mobile."
            ),
            stationary_phase=(
                "Reverse-phase: C18 (octadecylsilane on silica, "
                "most common); C8; phenyl; pentafluorophenyl.  "
                "Normal phase: bare silica.  HILIC: amide / "
                "zwitterionic for very polar analytes.  "
                "Particle sizes 1.7-5 μm; column dimensions "
                "50-250 mm × 2.1-4.6 mm i.d."
            ),
            mobile_phase=(
                "RP: water / MeCN or water / MeOH gradient, "
                "often with 0.1% formic acid or TFA modifier; "
                "isocratic or programmed gradient"
            ),
            detectors=(
                "UV / DAD (most common); fluorescence (for "
                "fluorophores); ELSD (universal but lower "
                "sensitivity); refractive index (sugars); MS "
                "(LC-MS); charged-aerosol detector (CAD)"
            ),
            typical_analytes=(
                "Pharmaceuticals (purity / impurity profiling); "
                "natural products; peptides; metabolites; "
                "anything soluble in a liquid mobile phase; "
                "the workhorse analytical method of the "
                "modern pharmaceutical industry"
            ),
            strengths=(
                "Extremely high resolution (100k+ plates with "
                "sub-2 μm particles); applicable to non-"
                "volatile / thermally labile compounds; "
                "scalable from analytical (μg) to preparative "
                "(g); quantitative + reproducible"
            ),
            limitations=(
                "Higher consumables cost than GC; sample "
                "must be solubilised; UV-only detection "
                "misses non-chromophoric compounds (use ELSD "
                "/ CAD); column equilibration after gradient "
                "adds dead time"
            ),
            procedure=(
                "Equilibrate column in starting mobile phase.  "
                "Inject 1-50 μL via autosampler.  Run "
                "programmed gradient (e.g. 5% MeCN → 95% MeCN "
                "over 20 min).  UV / MS detector records "
                "absorbance / mass at each time point.  "
                "Re-equilibrate before the next injection."
            ),
            notes=(
                "UPLC / UHPLC (Waters / Agilent / Thermo "
                "tradenames) uses sub-2 μm particles at >400 "
                "bar — same separation in 1/3 the time.  "
                "Van Deemter equation H = A + B/u + Cu "
                "describes plate height vs flow velocity, "
                "with C-term shrinking on smaller particles."
            ),
        ),
        ChromatographyMethod(
            id="lc_ms",
            name="Liquid chromatography - mass spectrometry",
            abbreviation="LC-MS",
            category="liquid",
            principle=(
                "HPLC followed by MS.  Atmospheric-pressure "
                "ionisation (ESI for polar / ionisable, APCI "
                "for less polar) bridges the LC liquid effluent "
                "into the gas-phase MS analyser."
            ),
            stationary_phase=(
                "Same as HPLC; MS-compatible mobile phase (no "
                "non-volatile buffers like phosphate; switch "
                "to formate / acetate / TFA)"
            ),
            mobile_phase=(
                "Volatile aqueous / organic mixtures + "
                "volatile additives (formic acid, ammonium "
                "formate, ammonium acetate)"
            ),
            detectors=(
                "ESI-quadrupole (most common); ESI-TOF (high "
                "resolution); Orbitrap (ultra-high resolution); "
                "triple-quadrupole (MRM quantitation); ion-"
                "mobility (IM-MS)"
            ),
            typical_analytes=(
                "Pharmaceutical bioanalysis (drug levels in "
                "plasma); peptide / protein characterisation; "
                "metabolomics; lipidomics; environmental "
                "trace analysis"
            ),
            strengths=(
                "MS structural ID + quantitation in one run; "
                "MRM gives ppt sensitivity; Orbitrap gives "
                "sub-1-ppm mass accuracy enabling formula "
                "elucidation; works with non-volatile / labile "
                "analytes"
            ),
            limitations=(
                "Phosphate buffers + non-volatile additives "
                "incompatible (clog ion source); ion "
                "suppression from co-eluting matrix is the "
                "main quantitation pitfall; instrument cost "
                "($150-1000k+)"
            ),
            procedure=(
                "Same as HPLC; column eluent enters the ESI "
                "source via a fused-silica capillary.  ESI "
                "voltage (~3 kV) generates analyte ions in "
                "vacuum; MS records m/z + intensity for every "
                "scan / MRM transition."
            ),
            notes=(
                "Negative-ion ESI is preferred for acidic "
                "compounds (carboxylic acids, sulfates, "
                "phosphates) — better signal than positive "
                "mode."
            ),
        ),
        ChromatographyMethod(
            id="hilic",
            name="Hydrophilic interaction liquid chromatography",
            abbreviation="HILIC",
            category="liquid",
            principle=(
                "Inverse of reverse-phase HPLC: a polar "
                "stationary phase + a high-organic mobile "
                "phase (typically 70-95% MeCN).  Polar "
                "analytes partition into a water-rich layer at "
                "the stationary-phase surface, retained by "
                "hydrophilic interaction.  Order of elution is "
                "by decreasing polarity — the opposite of RP."
            ),
            stationary_phase=(
                "Bare silica, amide-bonded silica, "
                "zwitterionic (sulfobetaine), diol; particle "
                "sizes 1.7-5 μm"
            ),
            mobile_phase=(
                "MeCN / water 95:5 → 50:50 gradient with "
                "ammonium formate or acetate buffer (5-20 mM)"
            ),
            detectors=(
                "Same as HPLC: UV, MS, ELSD, CAD"
            ),
            typical_analytes=(
                "Very polar compounds that don't retain on "
                "C18: sugars, polar metabolites (TCA-cycle "
                "acids), nucleotides, amino acids, polar "
                "drugs (amlodipine, metformin), "
                "phosphopeptides"
            ),
            strengths=(
                "Retains compounds RP can't; ESI-MS-friendly "
                "high organic mobile phase gives 5-10× "
                "better signal than RP-MS; complementary "
                "separation orthogonality to RP"
            ),
            limitations=(
                "Long equilibration times (40+ column "
                "volumes); narrow useful organic range; "
                "method development is harder than RP "
                "because the retention model is more complex"
            ),
            procedure=(
                "Equilibrate at high MeCN starting "
                "composition (~95%); inject in mobile-"
                "phase-compatible solvent (MeCN-rich!); "
                "elute by decreasing organic / increasing "
                "water."
            ),
            notes=(
                "If you inject in water on a HILIC column "
                "you'll see a giant solvent front and "
                "deformed peaks — sample diluent must be "
                "more organic-rich than the starting "
                "mobile phase."
            ),
        ),

        # ---- Protein purification ----
        ChromatographyMethod(
            id="fplc",
            name="Fast protein liquid chromatography",
            abbreviation="FPLC",
            category="protein",
            principle=(
                "Low-pressure (<10 bar) preparative LC "
                "designed for biomolecule purification.  Uses "
                "biocompatible columns + buffers + materials "
                "to keep proteins folded.  Workflow combines "
                "ion-exchange + size-exclusion + affinity "
                "modes (the same hardware runs all three with "
                "column swaps)."
            ),
            stationary_phase=(
                "Soft agarose / dextran / polymer-based "
                "media (Sepharose, Superdex, Mono Q / Mono "
                "S) — much larger particles (15-100 μm) than "
                "HPLC; functionalised for IEX / SEC / "
                "affinity"
            ),
            mobile_phase=(
                "Aqueous buffers (Tris, phosphate, HEPES) at "
                "controlled pH + ionic strength; gradient "
                "elution (salt, pH, or competitive ligand)"
            ),
            detectors=(
                "UV at 280 nm (Trp / Tyr); conductivity (for "
                "salt-gradient monitoring); pH; refractive "
                "index"
            ),
            typical_analytes=(
                "Recombinant proteins (His-tagged, GST-"
                "tagged, MBP-tagged); endogenous proteins "
                "after cell lysis; antibodies; vaccines; "
                "enzyme purification at mg-g scale"
            ),
            strengths=(
                "Native / non-denaturing conditions preserve "
                "protein folding + activity; scalable from "
                "mg (lab) to kg (industrial); reproducible "
                "automated gradients; in-line buffer mixing"
            ),
            limitations=(
                "Lower resolution than HPLC; resin cost is "
                "high (~$1000/L for affinity media); "
                "gradient separations take longer than HPLC; "
                "hardware ~$50-100k"
            ),
            procedure=(
                "Equilibrate column in binding buffer.  Load "
                "sample (clarified cell lysate).  Wash to "
                "remove non-binding contaminants.  Elute by "
                "imidazole gradient (Ni-NTA), salt gradient "
                "(IEX), competitor (affinity), or isocratic "
                "(SEC).  Pool peak fractions, measure "
                "concentration + purity."
            ),
            notes=(
                "Modern instruments (ÄKTA family from "
                "Cytiva, formerly GE Healthcare) are the "
                "lab-standard FPLC platform — modular pumps + "
                "valves + column swap let one chassis run all "
                "three purification modes back-to-back."
            ),
        ),
        ChromatographyMethod(
            id="iex",
            name="Ion-exchange chromatography",
            abbreviation="IEX",
            category="protein",
            principle=(
                "Charged stationary-phase functional groups "
                "(strong / weak anion or cation exchanger) "
                "bind oppositely-charged analytes "
                "electrostatically.  Elution by increasing "
                "salt (competitive ion displacement) or pH "
                "shift through the analyte's pI."
            ),
            stationary_phase=(
                "Cation exchangers: SP-Sepharose (sulfopropyl, "
                "strong); CM-Sepharose (carboxymethyl, weak).  "
                "Anion exchangers: Q-Sepharose (quaternary "
                "amine, strong); DEAE-Sepharose (diethyl-"
                "aminoethyl, weak)"
            ),
            mobile_phase=(
                "Low-salt binding buffer at pH chosen to give "
                "the analyte the desired charge; elute by NaCl "
                "or KCl gradient (50 mM → 1 M typical)"
            ),
            detectors=(
                "UV 280 nm (proteins); conductivity (salt "
                "gradient monitoring)"
            ),
            typical_analytes=(
                "Proteins (separation by surface charge); "
                "peptides; oligonucleotides; small ions (in "
                "the IC variant)"
            ),
            strengths=(
                "High loading capacity (10-100 mg protein per "
                "mL of resin); strong selectivity for "
                "isoelectric point differences; scalable to "
                "industrial scale"
            ),
            limitations=(
                "Choice of pH determines what's bound — "
                "method development requires knowing the "
                "analyte's pI; harsh elution (high salt) "
                "needs subsequent buffer exchange / "
                "desalting"
            ),
            procedure=(
                "Choose buffer pH ~ 1 unit away from analyte "
                "pI in the direction that gives the desired "
                "charge.  Load in low-salt buffer.  Wash.  "
                "Elute with linear NaCl gradient.  Each "
                "protein elutes at the salt concentration "
                "needed to outcompete its electrostatic "
                "binding."
            ),
            notes=(
                "Step elution (single salt jump) is faster "
                "but loses resolution between similarly-"
                "charged analytes — use linear gradient when "
                "resolution matters."
            ),
        ),
        ChromatographyMethod(
            id="sec",
            name="Size-exclusion chromatography",
            abbreviation="SEC",
            category="protein",
            principle=(
                "Porous beads with a defined pore-size "
                "distribution.  Large molecules can't enter "
                "the pores → elute early at the column void "
                "volume.  Small molecules access all the "
                "pore volume → elute last.  Purely physical "
                "(no chemical interaction) — the only "
                "chromatography mode where elution order is "
                "determined by molecular size, not affinity."
            ),
            stationary_phase=(
                "Porous polymer / silica / agarose beads with "
                "defined fractionation range: Superdex 75 "
                "(3-70 kDa); Superdex 200 (10-600 kDa); "
                "Sephacryl S-300 (10 kDa - 1.5 MDa)"
            ),
            mobile_phase=(
                "Isocratic — single buffer matching analyte "
                "stability needs; common: PBS, 150 mM NaCl + "
                "20 mM Tris pH 7.5"
            ),
            detectors=(
                "UV 280 nm; refractive index; multi-angle "
                "light scattering (MALS) for absolute "
                "molecular weight"
            ),
            typical_analytes=(
                "Protein oligomeric state assessment "
                "(monomer / dimer / aggregate); polishing "
                "step in purification protocols (removes "
                "aggregates); buffer exchange (when run "
                "fast — desalting columns)"
            ),
            strengths=(
                "Native / non-denaturing; simple isocratic "
                "elution; molecular-weight calibration with "
                "standards gives MW estimates for unknowns; "
                "co-pairs naturally with MALS for absolute MW"
            ),
            limitations=(
                "Low loading capacity (<5% of column volume); "
                "low resolution (cannot separate proteins "
                "differing by less than ~2× in MW); slow "
                "(long equilibration not needed but elution "
                "itself takes hours)"
            ),
            procedure=(
                "Equilibrate column (1-2 column volumes).  "
                "Load small sample volume (<5% column "
                "volume).  Run isocratically — single buffer, "
                "single flow rate.  Elute order: void → "
                "large → medium → small → totally included "
                "(salt etc.)."
            ),
            notes=(
                "Always the LAST step in a multi-step "
                "purification because it dilutes the "
                "sample and can't tolerate large loads — but "
                "it's the gold standard for proving "
                "monodispersity / single oligomeric state."
            ),
        ),
        ChromatographyMethod(
            id="affinity",
            name="Affinity chromatography",
            abbreviation="Affinity",
            category="protein",
            principle=(
                "Specific reversible biomolecular recognition "
                "between a stationary-phase ligand and the "
                "analyte: enzyme-substrate analogue, "
                "antibody-antigen, lectin-glycan, "
                "metal-chelate-His6.  Enables single-step "
                "purification from crude lysate."
            ),
            stationary_phase=(
                "Resin-immobilised affinity ligand: "
                "Ni-NTA / Co-TALON (His-tag); glutathione-"
                "Sepharose (GST-tag); amylose (MBP-tag); "
                "Streptactin (Strep-tag); Protein A / G "
                "(IgG); concanavalin A (mannose-rich "
                "glycoproteins); inhibitor-functionalised "
                "for enzyme purification"
            ),
            mobile_phase=(
                "Binding buffer matching native conditions; "
                "elution by competitor (imidazole for "
                "His-tag, glutathione for GST), pH shift, "
                "denaturant (urea, guanidine), or analogue "
                "displacement"
            ),
            detectors=(
                "UV 280 nm; SDS-PAGE of fractions for purity"
            ),
            typical_analytes=(
                "Recombinant tagged proteins (the standard "
                "first-step capture in 90 % of modern "
                "lab purifications); endogenous proteins "
                "with known ligands; antibody purification "
                "(Protein A); IgG isolation"
            ),
            strengths=(
                "10-1000× enrichment in a single step; "
                "very high purity from crude lysate; mild "
                "competitor elution preserves protein "
                "activity; scalable"
            ),
            limitations=(
                "Resin cost is the highest of any "
                "chromatography mode (~$1000/L); ligand-"
                "specific (different tag = different "
                "resin); some elution conditions denature "
                "the protein"
            ),
            procedure=(
                "Equilibrate column in binding buffer "
                "(e.g. 20 mM imidazole for Ni-NTA).  Load "
                "clarified cell lysate.  Wash extensively.  "
                "Elute with competitor (250 mM imidazole "
                "for Ni-NTA, 10 mM glutathione for GST).  "
                "Confirm purity by SDS-PAGE."
            ),
            notes=(
                "His6-tag + Ni-NTA is the modern lab "
                "default — works for ~80 % of recombinant "
                "proteins, mild elution, cheap resin "
                "(~$200/L)."
            ),
        ),

        # ---- Ion ----
        ChromatographyMethod(
            id="ion",
            name="Ion chromatography",
            abbreviation="IC",
            category="ion",
            principle=(
                "IEX adapted for small inorganic + small "
                "organic ions, with conductivity detection "
                "after a chemical suppressor that strips "
                "background eluent ions.  Quantifies anions "
                "(F⁻ / Cl⁻ / NO₂⁻ / NO₃⁻ / SO₄²⁻ / PO₄³⁻) "
                "and cations (Na⁺ / K⁺ / Ca²⁺ / Mg²⁺ / NH₄⁺) "
                "in environmental + drinking-water samples "
                "to ppb."
            ),
            stationary_phase=(
                "Polymer-based strong-anion or strong-cation "
                "exchanger (e.g. Dionex AS / CS series), "
                "5-9 μm particle, low-capacity for sharp "
                "peaks"
            ),
            mobile_phase=(
                "Anion analysis: KOH or Na₂CO₃ / NaHCO₃ "
                "gradient (with KOH-eluent generator).  "
                "Cation analysis: dilute methanesulfonic "
                "acid (MSA)"
            ),
            detectors=(
                "Suppressed conductivity (background-"
                "subtracted by membrane suppressor for "
                "1000× sensitivity); UV (for chromophoric "
                "ions like nitrate); MS (in some modern "
                "applications)"
            ),
            typical_analytes=(
                "Drinking-water + wastewater anion / cation "
                "profile; food-grade salts; pharmaceutical "
                "counter-ions; battery / electrolyte "
                "analysis; environmental NO₃⁻ / SO₄²⁻ "
                "monitoring"
            ),
            strengths=(
                "Excellent ppb sensitivity for inorganic "
                "ions that nothing else handles well; "
                "automated eluent-generator chemistry gives "
                "simple, salt-free gradients; EPA-method-"
                "validated workhorse"
            ),
            limitations=(
                "Ion-only — no use for neutral organic "
                "analytes; suppressors add complexity / "
                "maintenance burden; long re-equilibration "
                "after gradient runs"
            ),
            procedure=(
                "Equilibrate column in starting eluent.  "
                "Inject diluted sample (<200 ppm total ions).  "
                "Run isocratic or programmed gradient.  "
                "Eluent passes through suppressor (membrane / "
                "self-regenerating) which converts KOH → "
                "H₂O before the conductivity cell, dropping "
                "background by 1000×."
            ),
            notes=(
                "For inorganic anions the 'standard 7' "
                "panel (F / Cl / Br / NO₂ / NO₃ / SO₄ / "
                "PO₄) runs in <15 min on a modern AS18 "
                "column — the analytical workhorse for "
                "every municipal-water-quality lab."
            ),
        ),

        # ---- Supercritical ----
        ChromatographyMethod(
            id="sfc",
            name="Supercritical fluid chromatography",
            abbreviation="SFC",
            category="supercritical",
            principle=(
                "Supercritical CO₂ (T > 31 °C, P > 74 bar) "
                "as the primary mobile phase, modified with "
                "0-50 % methanol or other polar co-solvent.  "
                "Combines the low viscosity + high diffusivity "
                "of a gas (fast separations) with the "
                "solvating power of a liquid (handles non-"
                "volatile analytes)."
            ),
            stationary_phase=(
                "Same column chemistries as HPLC (silica, "
                "C18, amide); chiral stationary phases "
                "(Chiralpak / Chiralcel) for enantiomer "
                "separation, where SFC is the dominant "
                "modern method"
            ),
            mobile_phase=(
                "Supercritical CO₂ (the bulk of the mobile "
                "phase) + methanol / ethanol / IPA modifier "
                "(0-50 %); often 0.1 % NH₄OH or formic acid "
                "as additive"
            ),
            detectors=(
                "UV / DAD (most common); MS (after BPR "
                "decompression); ELSD; CAD; FID for "
                "non-modifier-containing runs"
            ),
            typical_analytes=(
                "Chiral pharmaceuticals (the standard "
                "method for production-scale enantiomer "
                "separation); lipids; natural products; "
                "petrochemicals; preparative-scale "
                "purification (CO₂ evaporates spontaneously, "
                "leaving solvent-free product)"
            ),
            strengths=(
                "5-10× faster than HPLC at equal "
                "resolution; CO₂ is cheap, non-toxic, "
                "evaporates → solvent-free product (huge "
                "win for prep work); orthogonal selectivity "
                "to RP-HPLC; the dominant modern chiral-"
                "separation method"
            ),
            limitations=(
                "Instrument complexity (high-pressure CO₂ "
                "handling); back-pressure regulator (BPR) "
                "is a wear part; small share of analytical "
                "labs (most stick with HPLC); MS interface "
                "needs careful design"
            ),
            procedure=(
                "Equilibrate column at run pressure (100-150 "
                "bar) + temperature (35-40 °C) + starting "
                "modifier %.  Inject in modifier-compatible "
                "solvent.  Run programmed gradient (typically "
                "5 % → 50 % methanol).  BPR maintains "
                "supercritical conditions through the column."
            ),
            notes=(
                "Modern preparative SFC systems (Waters "
                "Investigator, Sepiatec, Thar) routinely "
                "deliver kg/day of separated enantiomer at a "
                "fraction of the solvent cost of preparative "
                "HPLC — the green-chemistry win that has "
                "driven SFC's adoption in pharma."
            ),
        ),
    ]


_METHODS: List[ChromatographyMethod] = _build_catalogue()


# ------------------------------------------------------------------
# Public lookup helpers
# ------------------------------------------------------------------

def list_methods(category: Optional[str] = None
                 ) -> List[ChromatographyMethod]:
    if category is None:
        return list(_METHODS)
    if category not in VALID_CATEGORIES:
        return []
    return [m for m in _METHODS if m.category == category]


def get_method(method_id: str) -> Optional[ChromatographyMethod]:
    for m in _METHODS:
        if m.id == method_id:
            return m
    return None


def find_methods(needle: str) -> List[ChromatographyMethod]:
    """Case-insensitive substring search across id / name /
    abbreviation."""
    if not needle:
        return []
    n = needle.lower().strip()
    out: List[ChromatographyMethod] = []
    for m in _METHODS:
        if (n in m.id.lower()
                or n in m.name.lower()
                or n in m.abbreviation.lower()):
            out.append(m)
    return out


def categories() -> List[str]:
    return list(VALID_CATEGORIES)


def to_dict(m: ChromatographyMethod) -> Dict[str, str]:
    return {
        "id": m.id,
        "name": m.name,
        "abbreviation": m.abbreviation,
        "category": m.category,
        "principle": m.principle,
        "stationary_phase": m.stationary_phase,
        "mobile_phase": m.mobile_phase,
        "detectors": m.detectors,
        "typical_analytes": m.typical_analytes,
        "strengths": m.strengths,
        "limitations": m.limitations,
        "procedure": m.procedure,
        "notes": m.notes,
    }
