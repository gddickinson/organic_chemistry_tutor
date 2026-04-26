"""Phase 44 (round 150) — microscopy across resolution scales.

Catalogue of microscopy techniques organised by **resolution
scale** (whole-organism → tissue → cellular → sub-cellular →
single-molecule + clinical histology workflow).  Pedagogically
the answer to *"which microscope do I use?"* depends on what
you want to see + at what resolution.  This catalogue makes
that decision tree explicit and cross-references the Phase-40a
`lab_analysers.py` entries when the same instrument appears
both as an *instrument* (40a) and as a *resolution-anchored
technique* (here).

Pure-headless: no Qt imports.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Tuple

# Resolution scales (canonical order coarsest → finest).
RESOLUTION_SCALES: Tuple[str, ...] = (
    "whole-organism",
    "tissue",
    "cellular",
    "sub-cellular",
    "single-molecule",
    "clinical-histology",
)


# Sample types — what the technique is typically applied to.
SAMPLE_TYPES: Tuple[str, ...] = (
    "live-organism",
    "fixed-tissue",
    "live-cells",
    "fixed-cells",
    "isolated-organelles",
    "single-molecules",
    "biopsy",
    "non-biological",
)


@dataclass(frozen=True)
class MicroscopyMethod:
    """One microscopy technique anchored to a resolution scale."""
    id: str
    name: str
    abbreviation: str
    resolution_scale: str
    sample_types: Tuple[str, ...]
    typical_resolution: str
    light_source: str
    contrast_mechanism: str
    typical_uses: str
    strengths: str
    limitations: str
    representative_instruments: str
    cross_reference_lab_analyser_ids: Tuple[str, ...] = ()
    notes: str = ""


_METHODS: List[MicroscopyMethod] = [

    # ---------------- Whole-organism (mm-cm) ----------------
    MicroscopyMethod(
        id="stereo-dissecting",
        name="Stereo dissecting microscope",
        abbreviation="Stereo",
        resolution_scale="whole-organism",
        sample_types=("live-organism", "fixed-tissue"),
        typical_resolution="50–100 µm; 5×–50× magnification",
        light_source="Reflected white LED + transmitted base "
                     "illumination",
        contrast_mechanism="Reflected + transmitted brightfield",
        typical_uses="Organism dissection (Drosophila, "
                     "C. elegans, zebrafish embryos); embryo "
                     "manipulation; surgical training",
        strengths="Long working distance for tools; 3D "
                  "stereoscopic view; cheap and ubiquitous",
        limitations="Diffraction-limited well above cell size; "
                    "no fluorescence on most models",
        representative_instruments="Leica M165, Zeiss SteREO "
                                   "Discovery, Olympus SZX",
        notes="Stereoscopic = two slightly offset light paths "
              "give the operator depth perception, essential "
              "for fine micro-manipulation.",
    ),
    MicroscopyMethod(
        id="intravital",
        name="Intravital microscopy",
        abbreviation="IVM",
        resolution_scale="whole-organism",
        sample_types=("live-organism",),
        typical_resolution="1–5 µm (lateral); 5–10 µm (axial)",
        light_source="Multi-photon (NIR femtosecond pulsed "
                     "laser, typically 800–1100 nm)",
        contrast_mechanism="Multi-photon excitation of "
                           "fluorescent reporters in live "
                           "anaesthetised mice",
        typical_uses="In-vivo imaging of tumour vasculature, "
                     "immune-cell trafficking, neural activity "
                     "in awake animals",
        strengths="Watch biology happen in real time in a "
                  "living organism; preserves tissue context",
        limitations="Surgical preparation required; access "
                    "limited to surface-near tissue (typically "
                    "< 500 µm depth)",
        representative_instruments="Leica SP8 DIVE, Bruker "
                                   "Ultima, custom 2P rigs",
    ),
    MicroscopyMethod(
        id="oct",
        name="Optical-coherence tomography",
        abbreviation="OCT",
        resolution_scale="whole-organism",
        sample_types=("live-organism", "biopsy"),
        typical_resolution="1–10 µm (axial); 10–30 µm "
                           "(lateral)",
        light_source="Broad-bandwidth NIR (~830 or 1310 nm)",
        contrast_mechanism="Low-coherence interferometry; "
                           "backscatter from refractive-index "
                           "boundaries",
        typical_uses="Retinal imaging (ophthalmology gold "
                     "standard); intra-vascular OCT for "
                     "coronary plaques; dermatology",
        strengths="Non-invasive; cross-sectional 'optical "
                  "biopsy' to ~ 2 mm depth; clinical-grade "
                  "ubiquitous in ophthalmology",
        limitations="Limited penetration in highly-scattering "
                    "tissue; no molecular specificity",
        representative_instruments="Heidelberg Spectralis, "
                                   "Zeiss Cirrus, Topcon DRI "
                                   "OCT",
    ),
    MicroscopyMethod(
        id="small-animal-mri",
        name="Small-animal MRI",
        abbreviation="MRI",
        resolution_scale="whole-organism",
        sample_types=("live-organism",),
        typical_resolution="50–200 µm voxel at 7 T+",
        light_source="Static magnetic field (7–11.7 T) + RF "
                     "pulses",
        contrast_mechanism="Nuclear magnetic resonance of ¹H "
                           "(plus contrast agents like Gd, Mn, "
                           "USPIO)",
        typical_uses="Mouse / rat brain imaging; tumour growth "
                     "tracking; cardiac function; longitudinal "
                     "drug-efficacy studies",
        strengths="Non-ionising; deep tissue; soft-tissue "
                  "contrast unmatched by CT",
        limitations="Slow (minutes per scan); expensive "
                    "infrastructure (cryogen-cooled magnets); "
                    "millimetre-scale resolution at clinical "
                    "field strengths",
        representative_instruments="Bruker BioSpec 70/20, "
                                   "Agilent / Varian, MR Solutions",
    ),

    # ---------------- Tissue (μm-mm) ----------------
    MicroscopyMethod(
        id="brightfield-histology",
        name="Brightfield histology (H&E, IHC, special stains)",
        abbreviation="BF-histo",
        resolution_scale="tissue",
        sample_types=("fixed-tissue", "biopsy"),
        typical_resolution="0.5–1 µm with 40×–100× objective",
        light_source="Halogen / LED transmitted white",
        contrast_mechanism="Stain absorption (haematoxylin = "
                           "blue nuclei, eosin = pink "
                           "cytoplasm); chromogenic IHC (DAB)",
        typical_uses="Routine pathology; cancer diagnosis; "
                     "tumour grading + staging; trichrome / "
                     "PAS / silver special stains",
        strengths="Diagnostic gold standard; simple; cheap; "
                  "vast pathologist expertise",
        limitations="2D thin sections (3–5 µm); no live "
                    "imaging; molecular specificity limited "
                    "to antibody-detectable targets",
        representative_instruments="Olympus BX53, Leica DM6, "
                                   "Zeiss Axioscope 7",
    ),
    MicroscopyMethod(
        id="multiplex-ihc",
        name="Multiplex IHC (CODEX / Vectra Polaris)",
        abbreviation="mIHC",
        resolution_scale="tissue",
        sample_types=("fixed-tissue",),
        typical_resolution="0.5 µm lateral; 30+ markers / "
                           "section",
        light_source="Multi-channel LED + filter wheel "
                     "(Vectra) or cyclic fluorophore-conjugated "
                     "oligo strategy (CODEX / Akoya)",
        contrast_mechanism="Cyclic-staining + multispectral "
                           "imaging + spectral unmixing",
        typical_uses="Tumour-microenvironment immunophenotyping; "
                     "spatial transcriptomics validation; "
                     "biomarker discovery",
        strengths="Quantitative single-cell phenotyping in "
                  "tissue context; preserves spatial info "
                  "that scRNA-seq destroys",
        limitations="Slow (hours per slide); expensive; "
                    "requires careful panel design + spectral "
                    "unmixing",
        representative_instruments="Akoya CODEX, Akoya "
                                   "PhenoCycler, Vectra Polaris",
    ),
    MicroscopyMethod(
        id="light-sheet",
        name="Light-sheet fluorescence microscopy",
        abbreviation="LSFM",
        resolution_scale="tissue",
        sample_types=("fixed-tissue", "live-organism"),
        typical_resolution="0.5–1 µm lateral; 1–5 µm axial",
        light_source="Cylindrical-lens or scanned Bessel/Gaussian "
                     "sheet (typically 488 / 561 / 640 nm)",
        contrast_mechanism="Side-illumination of a thin "
                           "fluorescence sheet, perpendicular "
                           "detection",
        typical_uses="Whole-mouse-brain imaging post-CLARITY "
                     "/ iDISCO clearing; embryo development; "
                     "thick organoids",
        strengths="Low photo-toxicity (only the focal plane "
                  "is illuminated); fast volumetric imaging; "
                  "preserves 3D context",
        limitations="Sample size constrained by clearing "
                    "compatibility; high data rate (TBs/day)",
        representative_instruments="Zeiss Lattice Lightsheet 7, "
                                   "Leica DLS, Bruker MuVi-SPIM",
        cross_reference_lab_analyser_ids=("zeiss_lattice_lightsheet",),
    ),
    MicroscopyMethod(
        id="maldi-imaging",
        name="MALDI imaging mass spectrometry",
        abbreviation="MALDI-MSI",
        resolution_scale="tissue",
        sample_types=("fixed-tissue",),
        typical_resolution="5–50 µm pixel; m/z resolution "
                           "depends on analyser",
        light_source="UV or IR laser (337 nm N₂ or 355 nm "
                     "Nd:YAG)",
        contrast_mechanism="Matrix-assisted laser-desorption "
                           "ionisation followed by mass-spec "
                           "detection",
        typical_uses="Spatial drug distribution; lipid + "
                     "metabolite mapping in tissue sections; "
                     "label-free protein imaging",
        strengths="Untargeted molecular discovery; works on "
                  "FFPE; thousands of m/z per pixel",
        limitations="Slow (hours per slide); needs careful "
                    "matrix application; limited resolution "
                    "vs optical methods",
        representative_instruments="Bruker rapifleX MALDI, "
                                   "Waters HDI MALDI Synapt",
        cross_reference_lab_analyser_ids=("bruker_biotyper",),
    ),

    # ---------------- Cellular (μm) ----------------
    MicroscopyMethod(
        id="phase-contrast",
        name="Phase contrast",
        abbreviation="PC",
        resolution_scale="cellular",
        sample_types=("live-cells",),
        typical_resolution="0.2 µm with 40×–100× objective",
        light_source="Transmitted halogen / LED with phase "
                     "ring",
        contrast_mechanism="Phase ring + condenser annulus "
                           "convert refractive-index "
                           "differences into amplitude "
                           "contrast",
        typical_uses="Live-cell observation; cell-culture "
                     "monitoring; mitosis / apoptosis "
                     "morphology; no staining required",
        strengths="Label-free live imaging; cheap; intuitive",
        limitations="Halo artefacts around dense objects; "
                    "limited contrast for cell-organelle "
                    "structures",
        representative_instruments="Nikon Eclipse Ts2, "
                                   "Olympus CKX53, Zeiss "
                                   "Primovert",
    ),
    MicroscopyMethod(
        id="dic",
        name="Differential interference contrast (Nomarski)",
        abbreviation="DIC",
        resolution_scale="cellular",
        sample_types=("live-cells", "fixed-cells"),
        typical_resolution="0.2 µm with 60×–100× / 1.4 NA",
        light_source="Polarised transmitted white",
        contrast_mechanism="Wollaston prisms + polariser + "
                           "analyser convert phase gradients "
                           "into pseudo-3D shadow contrast",
        typical_uses="High-resolution live-cell + organelle "
                     "imaging; thick samples like embryos",
        strengths="Pseudo-3D appearance; sharper than phase "
                  "contrast; works on thick cells",
        limitations="Birefringent samples (e.g. cell walls, "
                    "starch) confuse the contrast; requires "
                    "matched objective + condenser",
        representative_instruments="Nikon Eclipse Ti2, Zeiss "
                                   "Axio Observer, Olympus IX83",
    ),
    MicroscopyMethod(
        id="widefield-epifluorescence",
        name="Widefield epifluorescence",
        abbreviation="WF",
        resolution_scale="cellular",
        sample_types=("live-cells", "fixed-cells"),
        typical_resolution="0.2 µm lateral; ~ 1 µm axial",
        light_source="Hg arc lamp / metal-halide / LED + "
                     "excitation filter",
        contrast_mechanism="Fluorophore excitation + emission "
                           "filter + dichroic mirror; whole "
                           "field illuminated",
        typical_uses="Routine fluorescence imaging; "
                     "immunofluorescence; live reporters; "
                     "high-throughput screening",
        strengths="Fast; high-quantum-yield detection; "
                  "compatible with most fluorophores",
        limitations="Out-of-focus blur degrades thick-sample "
                    "imaging — confocal needed for sectioning",
        representative_instruments="Nikon Eclipse Ti2, Zeiss "
                                   "Axio Observer 7, Leica DMi8",
    ),
    MicroscopyMethod(
        id="confocal",
        name="Laser-scanning confocal",
        abbreviation="LSCM",
        resolution_scale="cellular",
        sample_types=("live-cells", "fixed-cells",
                      "fixed-tissue"),
        typical_resolution="180–250 nm lateral; 500–700 nm "
                           "axial",
        light_source="Ar / Kr / DPSS / diode lasers (typical "
                     "405 / 488 / 561 / 640 nm)",
        contrast_mechanism="Pinhole rejects out-of-focus "
                           "light; raster-scanned single-point "
                           "excitation",
        typical_uses="Optical sectioning of fluorescently "
                     "labelled samples; 3D z-stacks; co-"
                     "localisation studies",
        strengths="True optical sectioning; multi-channel; "
                  "high signal-to-background",
        limitations="Slow (point-by-point scan); photo-"
                    "bleaching during long acquisitions; "
                    "expensive",
        representative_instruments="Zeiss LSM 980, Leica "
                                   "STELLARIS, Nikon AX",
        cross_reference_lab_analyser_ids=("zeiss_lsm_980",),
    ),
    MicroscopyMethod(
        id="spinning-disk-confocal",
        name="Spinning-disk confocal",
        abbreviation="SDC",
        resolution_scale="cellular",
        sample_types=("live-cells",),
        typical_resolution="200–250 nm lateral; 500–700 nm "
                           "axial",
        light_source="Lasers + Yokogawa Nipkow disk (1000+ "
                     "pinholes)",
        contrast_mechanism="Parallel pinhole confocal; sCMOS "
                           "or EMCCD camera detection",
        typical_uses="Live-cell imaging at video rate (30 "
                     "fps+); calcium signalling; vesicle "
                     "trafficking; mitotic dynamics",
        strengths="Fast (camera-limited frame rate); much "
                  "lower phototoxicity than LSCM",
        limitations="Pinhole crosstalk in thick samples; "
                    "less optical-sectioning precision than "
                    "LSCM",
        representative_instruments="Yokogawa CSU-W1, "
                                   "PerkinElmer UltraVIEW VoX",
    ),
    MicroscopyMethod(
        id="two-photon",
        name="Two-photon (multi-photon) microscopy",
        abbreviation="2P / MPM",
        resolution_scale="cellular",
        sample_types=("live-cells", "fixed-tissue",
                      "live-organism"),
        typical_resolution="300–500 nm lateral; 1 µm axial; "
                           "depth penetration > 500 µm",
        light_source="NIR femtosecond pulsed laser "
                     "(Ti:sapphire 700–1000 nm)",
        contrast_mechanism="Non-linear simultaneous absorption "
                           "of 2 NIR photons, fluorescence "
                           "only at the focal point",
        typical_uses="Deep-tissue imaging (brain, embryos); "
                     "intravital imaging; reduced "
                     "photo-bleaching outside focus",
        strengths="Inherent optical sectioning (no pinhole "
                  "needed); deep penetration; reduced "
                  "phototoxicity outside focus",
        limitations="Expensive (Ti:sapph laser ~ $200k+); "
                    "lower resolution than 1-photon; complex "
                    "alignment",
        representative_instruments="Bruker Ultima Investigator, "
                                   "Leica SP8 DIVE, Olympus "
                                   "FVMPE-RS",
    ),

    # ---------------- Sub-cellular (organelle) (100-500 nm) ----------------
    MicroscopyMethod(
        id="sim",
        name="Structured illumination microscopy",
        abbreviation="SIM",
        resolution_scale="sub-cellular",
        sample_types=("fixed-cells", "live-cells"),
        typical_resolution="~ 100 nm lateral (2× WF); ~ 250 "
                           "nm axial",
        light_source="LED or laser through grating / SLM",
        contrast_mechanism="Patterned illumination + Fourier "
                           "reconstruction; 9–15 raw frames "
                           "per super-resolved frame",
        typical_uses="Live-cell super-resolution; mitochondrial "
                     "cristae; cytoskeletal dynamics; nuclear "
                     "organisation",
        strengths="Live-cell compatible; works with standard "
                  "fluorophores; relatively low light dose",
        limitations="Reconstruction artefacts if undersampled; "
                    "modest 2× resolution gain only",
        representative_instruments="Zeiss Elyra 7, Nikon "
                                   "N-SIM, GE OMX",
    ),
    MicroscopyMethod(
        id="storm",
        name="STORM / dSTORM (single-molecule localisation)",
        abbreviation="STORM",
        resolution_scale="sub-cellular",
        sample_types=("fixed-cells", "fixed-tissue"),
        typical_resolution="20–30 nm lateral; 50 nm axial",
        light_source="High-power lasers (640 / 561 / 488 nm)",
        contrast_mechanism="Stochastic photoswitching of dyes; "
                           "centroid-fit single emitters from "
                           "thousands of frames",
        typical_uses="Cytoskeletal architecture (actin, "
                     "microtubules); receptor clustering at "
                     "synapses; nuclear-pore architecture",
        strengths="Highest practical lateral resolution in "
                  "fluorescence (10–20 nm); molecular "
                  "specificity",
        limitations="Mostly fixed samples; specialised dyes / "
                    "buffers (oxygen scavengers); minutes "
                    "per frame",
        representative_instruments="Bruker Vutara, Nikon "
                                   "N-STORM, ONI Nanoimager",
    ),
    MicroscopyMethod(
        id="palm",
        name="PALM (photoactivated localisation microscopy)",
        abbreviation="PALM",
        resolution_scale="sub-cellular",
        sample_types=("fixed-cells", "live-cells"),
        typical_resolution="20–50 nm lateral",
        light_source="Activation 405 nm + readout 488 / 561 nm",
        contrast_mechanism="Photo-activatable / -convertible "
                           "fluorescent proteins (PA-GFP, "
                           "mEos, Dendra)",
        typical_uses="Single-molecule tracking in live cells; "
                     "membrane-protein dynamics; "
                     "diffusion-coefficient mapping",
        strengths="Genetically encoded labels (no antibody "
                  "needed); live-cell single-molecule "
                  "tracking",
        limitations="Limited photon budget vs organic dyes; "
                    "PA-FP photobleaching",
        representative_instruments="Zeiss Elyra (PALM/STORM "
                                   "mode), custom builds",
    ),
    MicroscopyMethod(
        id="sted",
        name="Stimulated-emission depletion microscopy",
        abbreviation="STED",
        resolution_scale="sub-cellular",
        sample_types=("fixed-cells", "live-cells"),
        typical_resolution="30–60 nm lateral; ~ 100 nm axial",
        light_source="Excitation laser + co-aligned doughnut-"
                     "shaped depletion laser (775 nm typical)",
        contrast_mechanism="Stimulated emission outside the "
                           "doughnut centre depletes "
                           "fluorescence to a sub-diffraction "
                           "spot",
        typical_uses="Live-cell super-resolution; "
                     "neuronal-spine dynamics; vesicle "
                     "fusion events",
        strengths="Real-time super-resolution image (no "
                  "post-processing reconstruction); video-rate "
                  "possible at small FOV",
        limitations="High light dose (depletion laser); "
                    "specialised STED-compatible dyes; "
                    "expensive",
        representative_instruments="Leica STELLARIS 8 STED, "
                                   "Abberior Facility Line",
    ),
    MicroscopyMethod(
        id="airyscan",
        name="Airyscan",
        abbreviation="Airyscan",
        resolution_scale="sub-cellular",
        sample_types=("fixed-cells", "live-cells"),
        typical_resolution="120–140 nm lateral; 350 nm axial",
        light_source="Standard confocal lasers",
        contrast_mechanism="32-element GaAsP detector array + "
                           "pixel reassignment + deconvolution",
        typical_uses="Routine super-resolution upgrade for "
                     "confocal users; live-cell organelle "
                     "imaging",
        strengths="Easy upgrade from confocal; ~ 1.7× "
                  "resolution gain + 4–8× SNR; live-cell "
                  "friendly",
        limitations="Modest resolution gain vs SIM / STORM / "
                    "STED; vendor-locked to Zeiss",
        representative_instruments="Zeiss LSM 880 / 980 with "
                                   "Airyscan",
        cross_reference_lab_analyser_ids=("zeiss_lsm_980",),
    ),
    MicroscopyMethod(
        id="tirf",
        name="Total internal reflection fluorescence",
        abbreviation="TIRF",
        resolution_scale="sub-cellular",
        sample_types=("live-cells", "fixed-cells"),
        typical_resolution="200 nm lateral; 100 nm axial "
                           "(evanescent field)",
        light_source="Lasers at supercritical angle through "
                     "high-NA (1.45+) objective",
        contrast_mechanism="Evanescent wave excites only "
                           "fluorophores within ~ 100 nm of "
                           "the coverslip",
        typical_uses="Membrane-receptor dynamics; "
                     "exocytosis / endocytosis; focal-"
                     "adhesion imaging",
        strengths="Extremely thin axial section; high SNR; "
                  "single-molecule sensitivity at the "
                  "membrane",
        limitations="Restricted to ~ 100 nm of basal "
                    "membrane; no 3D imaging",
        representative_instruments="Nikon N-STORM TIRF, "
                                   "Olympus IX83 TIRF, "
                                   "Leica AM TIRF",
    ),

    # ---------------- Single-molecule (nm-Å) ----------------
    MicroscopyMethod(
        id="smfret",
        name="Single-molecule FRET",
        abbreviation="smFRET",
        resolution_scale="single-molecule",
        sample_types=("single-molecules",),
        typical_resolution="2–10 nm distance precision",
        light_source="Pulsed picosecond lasers + TIRF / "
                     "confocal excitation",
        contrast_mechanism="Förster resonance energy transfer "
                           "between donor + acceptor "
                           "fluorophores on one molecule",
        typical_uses="Protein conformational dynamics; "
                     "DNA-protein interactions; ribosome "
                     "translocation; ALEX / PIE for "
                     "stoichiometry",
        strengths="Reads sub-population behaviour invisible "
                  "in ensemble; ångström-scale distance "
                  "ruler",
        limitations="Requires site-specific labelling; "
                    "complex data analysis; slow throughput",
        representative_instruments="PicoQuant MicroTime 200, "
                                   "custom TIRF rigs",
    ),
    MicroscopyMethod(
        id="cryo-em",
        name="Cryo-electron microscopy",
        abbreviation="cryo-EM",
        resolution_scale="single-molecule",
        sample_types=("single-molecules",
                      "isolated-organelles"),
        typical_resolution="2–4 Å for routine SPA today; "
                           "1.2 Å recently demonstrated",
        light_source="Field-emission electron gun (200 / "
                     "300 keV)",
        contrast_mechanism="Phase contrast from frozen-"
                           "hydrated single particles; "
                           "thousands averaged",
        typical_uses="Ribosomes, viruses, membrane proteins; "
                     "drug-target structure determination "
                     "without crystals",
        strengths="No crystals required; native-like "
                  "hydrated state; near-atomic resolution",
        limitations="Sample-prep is the limiting step "
                    "(grid-vitrification reproducibility); "
                    "instrument cost > $5M",
        representative_instruments="Thermo Scientific Krios "
                                   "G4, JEOL CRYO ARM 300",
        cross_reference_lab_analyser_ids=("thermo_krios_g4",),
    ),
    MicroscopyMethod(
        id="cryo-et",
        name="Cryo-electron tomography",
        abbreviation="cryo-ET",
        resolution_scale="single-molecule",
        sample_types=("isolated-organelles", "fixed-cells"),
        typical_resolution="20–40 Å for tomograms; sub-"
                           "tomogram averaging → 5–10 Å",
        light_source="Field-emission electron gun (200 / 300 "
                     "keV) with tilt-series acquisition",
        contrast_mechanism="3D reconstruction from a tilt "
                           "series of 2D projections",
        typical_uses="In-situ macromolecular complexes "
                     "(ribosomes inside cells, nuclear pores, "
                     "cilia); FIB-milled cryo-lamellae",
        strengths="Macromolecular structures in cellular "
                  "context; reveals quaternary architecture",
        limitations="Limited tilt range causes 'missing "
                    "wedge' artefacts; sample thickness "
                    "<300 nm needed",
        representative_instruments="Thermo Krios + Volta "
                                   "phase plate, JEOL CRYO "
                                   "ARM, Leica EM ICE",
        cross_reference_lab_analyser_ids=("thermo_krios_g4",),
    ),
    MicroscopyMethod(
        id="afm",
        name="Atomic-force microscopy",
        abbreviation="AFM",
        resolution_scale="single-molecule",
        sample_types=("single-molecules", "fixed-cells",
                      "non-biological"),
        typical_resolution="~ 1 nm lateral; 0.1 nm axial in "
                           "ideal conditions",
        light_source="Cantilever + laser-deflection readout",
        contrast_mechanism="Nano-scale tip raster-scans "
                           "surface; cantilever deflection "
                           "or oscillation amplitude shifts "
                           "encode topography / forces",
        typical_uses="Single-molecule force spectroscopy "
                     "(protein unfolding); membrane-protein "
                     "topography; mechanical mapping of "
                     "live cells",
        strengths="Ångström-axial resolution on biological "
                  "samples; works in liquid; force "
                  "measurements (pN sensitivity)",
        limitations="Slow (minutes per image); tip-shape "
                    "artefacts; limited lateral resolution "
                    "vs EM",
        representative_instruments="Bruker Dimension Icon, "
                                   "JPK NanoWizard, Asylum MFP-3D",
    ),
    MicroscopyMethod(
        id="stm",
        name="Scanning-tunnelling microscopy",
        abbreviation="STM",
        resolution_scale="single-molecule",
        sample_types=("non-biological", "single-molecules"),
        typical_resolution="0.1 nm lateral; 0.01 nm axial — "
                           "sees individual atoms",
        light_source="Atomically-sharp metal tip + bias "
                     "voltage",
        contrast_mechanism="Quantum tunnelling current "
                           "between tip + conductive surface; "
                           "current ~ exp(−distance)",
        typical_uses="Surface-science atomic imaging; "
                     "single-molecule manipulation on metals; "
                     "the technique that proved Feynman's "
                     "atom-by-atom future",
        strengths="True atomic resolution; can manipulate "
                  "individual atoms; STS spectroscopy reads "
                  "electronic states",
        limitations="Conductive samples only; UHV + low "
                    "temperature for best resolution; not "
                    "for typical biological samples",
        representative_instruments="Omicron VT-STM, "
                                   "Createc LT-STM, Unisoku "
                                   "USM 1500",
        notes="Won the 1986 Nobel for Binnig + Rohrer.  "
              "First imaging technique to see individual "
              "atoms.",
    ),

    # ---------------- Clinical histology workflow ----------------
    MicroscopyMethod(
        id="clinical-light-microscope",
        name="Clinical light microscope (pathology workhorse)",
        abbreviation="LM",
        resolution_scale="clinical-histology",
        sample_types=("biopsy", "fixed-tissue"),
        typical_resolution="0.5 µm with 100× / 1.4 NA oil",
        light_source="LED transmitted white",
        contrast_mechanism="Standard brightfield + H&E + "
                           "special stains (Trichrome, PAS, "
                           "Reticulin, Congo red, GMS, AFB)",
        typical_uses="Daily pathology diagnosis; tumour "
                     "grading + staging; infectious-disease "
                     "identification (acid-fast bacilli, "
                     "fungi)",
        strengths="Universal; pathologist-trained; cheap; "
                  "fast turnaround",
        limitations="2D thin sections; subjective; "
                    "inter-observer variability",
        representative_instruments="Olympus BX46, Leica DM2000, "
                                   "Nikon Eclipse Ci-L",
    ),
    MicroscopyMethod(
        id="frozen-section",
        name="Frozen-section cryostat microscopy",
        abbreviation="FS",
        resolution_scale="clinical-histology",
        sample_types=("biopsy",),
        typical_resolution="1 µm; 5–10 µm section thickness",
        light_source="Standard brightfield + rapid H&E",
        contrast_mechanism="Tissue snap-frozen in OCT "
                           "compound, cryostat sectioned, "
                           "stained in 5 min",
        typical_uses="Intra-operative surgical margins "
                     "consultation (Mohs surgery, breast "
                     "lumpectomy); rapid diagnosis < 20 min",
        strengths="Real-time diagnosis during surgery; "
                  "preserves enzyme activity for histochem",
        limitations="Lower morphological detail vs "
                    "FFPE-paraffin sections; freezing "
                    "artefacts",
        representative_instruments="Leica CM1950 cryostat, "
                                   "Thermo CryoStar NX70",
    ),
    MicroscopyMethod(
        id="ihc-clinical",
        name="Clinical immunohistochemistry (IHC)",
        abbreviation="IHC",
        resolution_scale="clinical-histology",
        sample_types=("biopsy", "fixed-tissue"),
        typical_resolution="0.5 µm; chromogenic DAB / AEC",
        light_source="Standard brightfield",
        contrast_mechanism="Antibody-targeted enzyme "
                           "(HRP / AP) generates a coloured "
                           "precipitate at antigen sites",
        typical_uses="Cancer biomarker staining (HER2, ER, "
                     "PR, Ki-67, p53, PD-L1); diagnostic "
                     "panel for unknown-primary tumour",
        strengths="Single-marker quantitation in routine "
                  "pathology; integrates with H&E workflow; "
                  "FDA-approved companion-diagnostics",
        limitations="One marker per slide; antigen-retrieval "
                    "step optimisation; subjective scoring "
                    "(though digital path now quantitates)",
        representative_instruments="Roche Ventana BenchMark, "
                                   "Leica BOND-MAX, Dako "
                                   "Omnis",
    ),
    MicroscopyMethod(
        id="digital-pathology-scanner",
        name="Digital-pathology slide scanner",
        abbreviation="WSI",
        resolution_scale="clinical-histology",
        sample_types=("biopsy", "fixed-tissue"),
        typical_resolution="0.25–0.5 µm/pixel at 40× "
                           "scanning",
        light_source="LED + line-scan or area-scan camera",
        contrast_mechanism="Whole-slide imaging at 20× / "
                           "40×; produces TIFF / SVS "
                           "pyramidal tile",
        typical_uses="Telepathology; digital archive of "
                     "diagnostic slides; AI-assisted "
                     "quantitation (HER2, mitotic count, "
                     "PD-L1)",
        strengths="Remote review; AI integration; multi-"
                  "viewer collaboration; permanent digital "
                  "record",
        limitations="Large file size (~ 2 GB / slide); "
                    "calibration variability between "
                    "scanners; clinical-validation "
                    "workflow heavy",
        representative_instruments="Hamamatsu NanoZoomer S360, "
                                   "Leica Aperio AT2 / GT 450, "
                                   "Philips IntelliSite",
    ),
    MicroscopyMethod(
        id="polarised-light",
        name="Polarised-light microscopy",
        abbreviation="PLM",
        resolution_scale="tissue",
        sample_types=("biopsy", "fixed-tissue",
                      "non-biological"),
        typical_resolution="0.5 µm with 40× objective",
        light_source="Polarised transmitted white",
        contrast_mechanism="Polariser + analyser detect "
                           "birefringent materials (crystals, "
                           "collagen, amyloid)",
        typical_uses="Crystal arthropathy diagnosis (gout "
                     "monosodium urate, pseudogout calcium "
                     "pyrophosphate); amyloid Congo-red "
                     "apple-green birefringence",
        strengths="Diagnostic specificity for birefringent "
                  "deposits; cheap add-on to standard light "
                  "microscope",
        limitations="Only detects birefringent species; "
                    "operator skill required",
        representative_instruments="Olympus BX53-P, Leica "
                                   "DM4 P",
    ),
]


# ----------------------------------------------------------------
# Lookup helpers
# ----------------------------------------------------------------
_BY_ID: Dict[str, MicroscopyMethod] = {m.id: m for m in _METHODS}


def list_methods(
    resolution_scale: Optional[str] = None,
) -> List[MicroscopyMethod]:
    """Return every microscopy method, optionally filtered by
    resolution scale.

    Returns empty for unknown scales.
    """
    if resolution_scale is None or resolution_scale == "":
        return list(_METHODS)
    if resolution_scale not in RESOLUTION_SCALES:
        return []
    return [m for m in _METHODS
            if m.resolution_scale == resolution_scale]


def get_method(method_id: str) -> Optional[MicroscopyMethod]:
    """Return the method with this id, or None."""
    return _BY_ID.get(method_id)


def find_methods(needle: str) -> List[MicroscopyMethod]:
    """Case-insensitive substring search across id + name +
    abbreviation + typical_uses + representative_instruments."""
    n = (needle or "").strip().lower()
    if not n:
        return []
    out = []
    for m in _METHODS:
        hay = " ".join([
            m.id, m.name, m.abbreviation, m.typical_uses,
            m.representative_instruments,
        ]).lower()
        if n in hay:
            out.append(m)
    return out


def methods_for_sample_type(sample_type: str) -> List[MicroscopyMethod]:
    """Return methods that list the given sample type as
    typical."""
    if not sample_type or sample_type not in SAMPLE_TYPES:
        return []
    return [m for m in _METHODS if sample_type in m.sample_types]


def resolution_scales() -> Tuple[str, ...]:
    """Canonical resolution-scale tuple, coarsest first."""
    return RESOLUTION_SCALES


def sample_types() -> Tuple[str, ...]:
    """Canonical sample-type tuple."""
    return SAMPLE_TYPES


def method_to_dict(m: MicroscopyMethod) -> Dict[str, object]:
    """JSON-serialisable view of a single method."""
    return asdict(m)
