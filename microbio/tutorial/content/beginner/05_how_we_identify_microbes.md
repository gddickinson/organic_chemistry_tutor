# How we identify microbes

The clinical microbiology lab faces a deceptively
simple question: "what is causing this infection?"
The toolkit has expanded enormously over the past
two decades — from a half-day Gram-stain-plus-culture
workflow to molecular panels that return identification
+ resistance profile in 1-2 hours.

## Specimen + Gram stain — the first 30 minutes

Every clinical microbiology specimen starts with:
- Macroscopic inspection (sputum quality, urine
  appearance, CSF clarity).
- **Gram stain** of a smear — purple gram-positives,
  pink gram-negatives, presence of leukocytes,
  cellular morphology (cocci / rods / coccobacilli).

A Gram stain alone often narrows the differential
enough to start empirical antibiotics:
- Gram-positive cocci in clusters → *Staphylococcus*.
- Gram-positive cocci in chains / pairs →
  *Streptococcus* / *Enterococcus*.
- Gram-positive rods → *Listeria*, *Bacillus*,
  *Clostridium*, *Corynebacterium*.
- Gram-negative diplococci → *Neisseria* (gonococci /
  meningococci).
- Gram-negative rods → *E. coli*, *Klebsiella*,
  *Pseudomonas*, *Enterobacter*.
- Gram-negative coccobacilli → *Haemophilus*,
  *Brucella*, *Bordetella*.

## Special stains

- **Acid-fast (Ziehl-Neelsen / Kinyoun)** — *Mycobacterium*,
  *Nocardia*.  Auramine-rhodamine fluorescence is the
  rapid alternative.
- **India ink** — *Cryptococcus neoformans* capsule
  in CSF (yellow halo around yeast).
- **KOH prep** — fungal hyphae visualisation in
  skin / nail / hair scrapings.
- **Calcofluor white** — fluorescent fungal stain.
- **Wet mount + dark field** — *Treponema pallidum*
  spirochaetes, *Trichomonas*.
- **Giemsa** — blood films for malaria + Borrelia +
  Babesia + Trypanosoma.
- **Methenamine silver** — *Pneumocystis jirovecii*
  cysts.

## Culture

Most bacteria + many fungi can be cultivated on
agar media:

### Selective media

Suppress unwanted organisms while permitting target.
Examples:
- **MacConkey** — bile salts inhibit gram-positives;
  selects gram-negatives + differentiates lactose
  fermenters (pink) from non-fermenters (colourless).
- **Hektoen / XLD** — selects *Salmonella* +
  *Shigella* from stool.
- **Mannitol salt agar** — high salt selects
  staphylococci; mannitol fermentation differentiates
  *S. aureus* (yellow) from CoNS (red).
- **CCFA** — *C. difficile*-selective.
- **Sabouraud + dermatophyte test medium (DTM)** —
  fungal isolation.
- **Lowenstein-Jensen + Middlebrook** — *Mycobacterium*
  isolation; weeks of incubation.
- **Buffered charcoal yeast extract (BCYE)** —
  *Legionella*.
- **Thayer-Martin** — *Neisseria gonorrhoeae* +
  *meningitidis*.

### Differential media

Show colour / pH / haemolysis differences between
species.  Examples:
- **Blood agar** — α (greenish, partial; viridans
  strep, *S. pneumoniae*), β (clear; *S. pyogenes*,
  *S. aureus*), γ (none; enterococci) haemolysis.
- **Chocolate agar** — heated blood releases hemin +
  NAD; cultures fastidious *Haemophilus* + *Neisseria*.
- **CHROMagar** — chromogenic enzyme reactions
  differentiate species (*Candida albicans* green,
  *C. tropicalis* blue, *C. krusei* pink, *C. auris*
  pink-pale).

### Anaerobic culture

Many gut + oral commensals + pathogens are obligate
anaerobes — must be cultured in anaerobic chambers
or with disposable anaerobic-jar systems (GasPak).

Pathogenic anaerobes: *Bacteroides fragilis*,
*Clostridium perfringens / tetani / botulinum /
difficile*, *Fusobacterium*, *Peptostreptococcus*.

## Biochemical identification

Once colonies grow, biochemical tests define species:

- **Catalase** (H2O2 → O2 + water) — distinguishes
  staph (positive) from strep (negative).
- **Coagulase** — distinguishes *S. aureus* (positive)
  from coagulase-negative staphylococci (CoNS).
- **Oxidase** — separates oxidase-positive
  (*Pseudomonas*, *Neisseria*, *Vibrio*, *Aeromonas*,
  *Helicobacter*) from oxidase-negative.
- **Indole** — *E. coli* indole-positive.
- **Urease** — *H. pylori*, *Proteus*,
  *Klebsiella* (urea breath test diagnoses *H. pylori*).
- **Citrate, methyl red, Voges-Proskauer** (IMViC) —
  classic enterobacterial differentiation.

API strips + Vitek / Phoenix automated panels
combined ~ 20-30 biochemical tests; widely used
through ~ 2010-2015 before being supplanted by
MALDI-TOF in many labs.

## MALDI-TOF mass spectrometry

A revolutionary technology since ~ 2010-2015.

Workflow:
1. Smear a colony on a target plate.
2. Apply matrix (α-cyano-4-hydroxycinnamic acid).
3. Laser ionises ribosomal proteins primarily.
4. Mass spectrum recorded in time-of-flight detector.
5. Spectrum matched against a reference database
   (Bruker Biotyper, bioMérieux Vitek MS).

Identifies most cultivated bacteria + yeasts in
~ 2 minutes for ~ $1 / sample (after initial
instrument cost ~ $200K).  Now standard in most
mid-sized + large clinical microbiology labs
worldwide.

Limitations:
- Requires growth (still need overnight culture
  for slow growers).
- Closely-related species (*Streptococcus mitis*
  vs *pneumoniae*) sometimes confused.
- Filamentous fungi need extraction + sometimes
  fail.
- *Mycobacterium* + *Nocardia* require specialised
  extraction.

## Molecular diagnostics

### PCR / multiplex panels

Direct from clinical specimen, no culture needed:

- **BioFire FilmArray** — multiplex syndromic panels
  (respiratory, GI, blood culture, meningitis /
  encephalitis, joint infection); 1 hour, ~ 20-50
  pathogens per panel.
- **Cepheid GeneXpert** — single-cartridge nucleic-
  acid tests (TB / RIF, MRSA, *C. difficile*, GBS,
  influenza).
- **In-house qPCR** for specific organisms.

### 16S rRNA sequencing

Universal bacterial identifier — the 16S gene is
present in every bacterium with conserved + variable
regions.  Sequence the V3-V4 hypervariable region +
match against a database (SILVA, Greengenes, RDP).

Use cases:
- Identify culture-negative or unusual isolates.
- Microbiome profiling.
- Detect bacteria in normally-sterile sites
  (heart valves, joint aspirates).

### Whole-genome sequencing (WGS)

Increasingly used for:
- **Outbreak investigation** — phylogenetic clustering
  to identify transmission chains.
- **Resistance gene + virulence factor profiling**.
- **MTBC drug resistance prediction** from genome.
- **Reference labs** for unusual / rare organisms.
- **Public-health surveillance** (PulseNet, GenomeTrakr).

### Metagenomic sequencing

Sequence everything in a sample, taxonomic +
functional profiling.  Use cases:
- Pathogen ID in culture-negative serious infections
  (encephalitis with meningitis-panel-negative CSF;
  MNGS rescues 7-15 % of these cases).
- Microbiome research.
- Environmental surveillance.

A future **Genetics + Molecular Biology Studio**
sibling will deepen the technique side of these
molecular methods.

## Antibiotic susceptibility testing (AST)

Once the organism is identified, susceptibility tells
the clinician which antibiotics will work:

### Disk diffusion (Kirby-Bauer)

Antibiotic-impregnated paper disks placed on lawn
culture; zones of inhibition measured.  CLSI / EUCAST
breakpoints classify zone diameter as susceptible /
intermediate / resistant.

### Broth microdilution

Doubling-dilution series in 96-well plates; lowest
concentration with no growth = MIC (minimum inhibitory
concentration).  The reference method.

### Etest

Plastic strip with continuous antibiotic gradient on
agar; MIC read directly from intersection of growth
ellipse with strip.  Convenient but ~ $1-3 per
strip.

### Automated systems

Vitek / Phoenix / MicroScan: combine ID + MIC in
plate-based or card-based assays; 4-18 hours
turnaround.

### Genotypic AST

Detect resistance genes / mutations directly:
- **Xpert MTB/RIF** — TB + rifampicin resistance in
  2 hours.
- **mecA** for MRSA detection.
- **vanA / vanB** for VRE.
- **CTX-M / NDM / KPC / OXA** ESBL / carbapenemase
  panels.

## Antifungal + antiparasitic + antiviral testing

- **Antifungal MIC** — broth microdilution per CLSI
  M27 / M38 reference methods.
- **Antiparasitic** — mostly clinical / phenotypic;
  PCR + sequencing for resistance markers
  (chloroquine *Pf*-CRT, artemisinin *Pf*-K13).
- **Antiviral** — phenotypic culture-based assays
  (HSV plaque reduction, HIV phenotypic) +
  genotypic resistance assays (HIV, HCV, HBV,
  CMV).

## Try it in the app

- **Window → Microbiology Studio → Microbes** —
  per-microbe entries note Gram + key biochemicals
  + selective media.
- **OrgChem → Tools → Lab analysers** — MALDI Biotyper
  + GeneXpert + automated culture entries.
- **OrgChem → Tools → Microscopy techniques** —
  Gram + acid-fast + fluorescence microscopy
  entries.

Next: **Antibiotic mechanisms + classes**.
