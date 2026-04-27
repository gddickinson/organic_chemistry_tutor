# Photosynthesis

Photosynthesis converts light energy into chemical
energy + atmospheric CO2 into organic carbon.  It is
the engine of essentially the entire biosphere + the
source of essentially all the oxygen we breathe.

## The big picture

Net photosynthesis:

6 CO2 + 6 H2O + light → C6H12O6 + 6 O2

Two coupled stages happen in the chloroplast:
- **Light reactions** in the thylakoid membrane —
  use light energy to oxidise water + reduce NADP+ +
  generate ATP.
- **Calvin-Benson-Bassham cycle (Calvin cycle)** in
  the stroma — uses ATP + NADPH to fix CO2 onto a
  5-carbon sugar acceptor + reduce it to a 3-carbon
  product (G3P).

## Light reactions — the Z-scheme

Two photosystems work in series, named (counter-
intuitively) by discovery order:

- **Photosystem II (PSII)** — first in the path of
  electrons; oxidises water → O2.
- **Photosystem I (PSI)** — second; reduces NADP+
  → NADPH.

The Z-scheme energy diagram (electrons gain energy
in two photochemical steps):

```
PSII* (-1 V) → PQ → cyt b6f → PC → PSI* (-1.4 V)
   ↑                                       ↓
hν                                        hν
   ↑                                       ↓
PSII (+1.1 V) ← H2O                  PSI (+0.4 V) → Fd → NADP+ → NADPH
```

### Photosystem II

- Reaction-centre pigment **P680** (chlorophyll a
  dimer with 680-nm absorption peak) absorbs a
  photon → P680*.
- P680* transfers an electron → pheophytin → PQA
  → PQB → plastoquinone (PQ) pool.
- The oxidised P680+ (one of the most powerful
  biological oxidants known) extracts electrons from
  the **oxygen-evolving complex (OEC)** — a
  Mn4CaO5 cluster on the lumenal side.
- 4 photons + 4 e- + 2 H2O → O2 + 4 H+
  (released into thylakoid lumen).

### Cytochrome b6f complex

Plastoquinol (PQH2) → cytochrome b6f → plastocyanin
(PC) on the lumenal side.

The "Q-cycle" doubles the proton-pumping
stoichiometry — for every PQH2 oxidised, 4 H+ are
delivered to the lumen.

### Photosystem I

- Reaction centre **P700** absorbs a photon → P700*.
- P700* → A0 (chlorophyll a monomer) → A1
  (phylloquinone) → 4Fe-4S clusters → ferredoxin
  (Fd).
- Fd + ferredoxin-NADP+-reductase (FNR) → NADP+ →
  NADPH on the stromal side.

### Linear vs cyclic electron flow

- **Linear (LEF)** — H2O → PSII → PQ → cyt b6f → PC
  → PSI → Fd → NADPH.  Generates NADPH + ATP at
  ~ 1:1.
- **Cyclic (CEF)** — Fd → cyt b6f → PC → PSI → Fd.
  Generates ATP only.  Tunes the ATP/NADPH ratio
  to match Calvin cycle demand (~ 3 ATP : 2 NADPH).

The proton gradient powers:
- **ATP synthase** (chloroplast CF1F0) — Boyer +
  Walker rotary mechanism.
- **NADPH** + **ATP** = "assimilatory power" for the
  Calvin cycle.

### Pigments + light harvesting

Chlorophylls + carotenoids in the thylakoid membrane
are organised into **light-harvesting complexes
(LHCII + LHCI)** that funnel excitation energy by
Förster resonance energy transfer (FRET) to the
reaction centres.

When light is excessive, **non-photochemical
quenching (NPQ)** dissipates excess excitation as
heat — driven by zeaxanthin in the xanthophyll
cycle + the PsbS protein.  Critical for protecting
PSII from photoinhibition.

## Calvin-Benson-Bassham cycle

In the stroma; named after its discoverers (Melvin
Calvin Nobel 1961).  Three phases:

### Phase 1 — carboxylation

**RuBisCO** (Ribulose-1,5-Bisphosphate Carboxylase /
Oxygenase) catalyses:

CO2 + ribulose-1,5-bisphosphate (RuBP) →
2 × 3-phosphoglycerate (3-PGA)

RuBisCO is the most abundant protein on Earth —
constitutes ~ 30 % of soluble leaf protein.  It is
also famously inefficient:
- Slow turnover (~ 3-10 / sec).
- Promiscuous active site oxygenates RuBP as well
  (photorespiration; below).

### Phase 2 — reduction

3-PGA → 1,3-bisphosphoglycerate → glyceraldehyde-3-
phosphate (G3P) via phosphoglycerate kinase + GAPDH.

Each turn consumes 1 ATP + 1 NADPH per 3-PGA → 2 ATP
+ 2 NADPH per CO2 fixed.

### Phase 3 — regeneration

5 G3P → 3 RuBP via a complex network of 4-, 5-, 6-,
7-carbon sugar phosphate intermediates +
transketolase + sedoheptulose-1,7-bisphosphatase
+ fructose-1,6-bisphosphatase + ribulose-5-phosphate
kinase.

Net stoichiometry: 6 CO2 + 18 ATP + 12 NADPH →
1 hexose + 18 ADP + 12 NADP+ + 6 H2O.

## Photorespiration — the RuBisCO mistake

When RuBisCO uses O2 instead of CO2:

RuBP + O2 → 3-PGA + 2-phosphoglycolate

2-phosphoglycolate is metabolically toxic.  Salvage
involves chloroplast → peroxisome → mitochondrion
shuttle:
1. 2-phosphoglycolate → glycolate (chloroplast).
2. Glycolate → glyoxylate → glycine (peroxisome).
3. 2 glycines → serine + CO2 + NH3 (mitochondrion).
4. Serine → 3-PGA, ammonia re-fixed via GS-GOGAT.

Net loss: 25 % of carbon goes to CO2 + ATP/NADPH /
NADH consumed.  Photorespiration costs C3 plants
~ 25-30 % of potential photosynthetic productivity
in warm climates.

## C3 vs C4 vs CAM

Three CO2-fixation strategies handle the
photorespiration problem differently.

### C3 (~ 95 % of plant species)

- RuBisCO is in the mesophyll; first stable product
  is the 3-carbon 3-PGA.
- Ancestral + most efficient at low temperatures + low
  irradiance.
- Suffers most from photorespiration in hot / dry /
  CO2-low conditions.
- Examples: rice, wheat, soybean, most temperate
  plants.

### C4 (~ 3 % of species but a major fraction of
biomass)

- Spatial separation: PEP carboxylase (PEPC) in
  mesophyll fixes CO2 onto PEP → 4-carbon oxaloacetate
  (hence "C4"); shuttled to bundle-sheath cells where
  decarboxylated → CO2 concentrated near RuBisCO.
- PEPC has no oxygenase activity → no
  photorespiration.
- Energy cost: extra ATP for the CO2 pump.
- Better in hot + sunny + dry environments.
- **Kranz anatomy** — concentric bundle-sheath +
  mesophyll cells.
- Examples: maize, sugarcane, sorghum, millet, many
  grasses.
- Evolved independently > 60 times in 19 plant
  families — convergent evolution.

### CAM (crassulacean acid metabolism)

- Temporal separation: stomata open at NIGHT (cool
  + humid) → PEPC fixes CO2 to malate, stored in
  vacuole.  By DAY, stomata close (water saved!) →
  malate decarboxylated → CO2 concentrated near
  RuBisCO.
- Best for arid environments.
- Examples: cacti, succulents, pineapple, agave,
  orchids.
- Some plants are facultative CAM (switch to CAM
  under stress).

## Evolutionary + agricultural context

### C4 in a changing world

Higher CO2 (anthropogenic) reduces the C3
photorespiration penalty → C3 advantage in elevated
CO2.  But C4 retains advantages in heat + drought +
nitrogen-use efficiency.

### Engineering C4 into rice

The **C4 Rice Project** aims to transfer the C4
machinery into rice (a C3 crop) to boost yield
~ 50 % + improve water + nitrogen efficiency.
Major-philanthropy-funded; technically feasible but
genetically complex (Kranz anatomy + multiple
transcription factors).  In pilot trials.

### Beyond Calvin — alternative carbon-fixation
pathways

Non-Calvin carbon-fixation routes exist in some
prokaryotes (reductive TCA, 3-hydroxypropionate
bicycle, Wood-Ljungdahl).  Engineered alternatives
(synthetic CO2-fixation pathways like CETCH) being
explored for synthetic biology.

## Photoprotection + photoinhibition

In excess light or stress:
- PSII D1 protein damaged at high turnover.
- Repair cycle: D1 turns over every ~ 30 min in full
  sunlight.
- Photoinhibition occurs when damage rate > repair
  rate — productivity declines.
- NPQ (above) + state transitions + ROS scavenging
  (ascorbate-glutathione cycle, plastoquinone redox
  signalling, alternative electron sinks) all help.

## Pigments + colour

- **Chlorophyll a + b** absorb blue + red, transmit
  green → leaves are green.
- **Carotenoids** (β-carotene, lutein, zeaxanthin,
  violaxanthin) absorb blue-green; structurally
  protective + accessory pigments.  Become visible
  in autumn as chlorophyll degrades.
- **Anthocyanins + other flavonoids** in vacuoles —
  red / blue / purple flowers + autumn leaves.
- **Phycobiliproteins** — red + blue-green algae +
  cyanobacteria; absorb where chlorophyll doesn't.

## Cross-link

The Z-scheme + Calvin-cycle enzymes are a major theme
in **BC-3.0 advanced "Oxidative phosphorylation +
chemiosmosis"** (the analogous mitochondrial process)
+ **BC-3.0 graduate "Computational enzymology"** for
RuBisCO mechanism.

## Try it in the app

- **OrgChem → Tools → Cell components** — chloroplast
  + thylakoid + grana entries.
- **Window → Biochem Studio → Metabolic pathways** —
  Calvin cycle.
- **Window → Biochem Studio → Enzymes** — RuBisCO,
  PSII OEC.
- **Window → Botany Studio → Plant taxa** — C3 vs C4
  vs CAM species.

Next: **Plant water + nutrient transport**.
