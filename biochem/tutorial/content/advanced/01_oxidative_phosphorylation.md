# Oxidative phosphorylation + chemiosmosis

The mitochondrial inner membrane is biology's most-elegant
energy-conversion machine.  Reducing equivalents (NADH +
FADH₂) flow through the electron-transport chain, pumping
protons across the membrane.  The proton gradient drives
ATP synthesis via a rotary motor.

## The four respiratory complexes

Embedded in the inner mitochondrial membrane:

### Complex I — NADH:ubiquinone oxidoreductase

The largest (~ 1 MDa, > 40 subunits in mammals).
L-shaped: peripheral arm in the matrix binds NADH +
holds Fe-S clusters; membrane arm pumps protons.

NADH + Q + 5 H+(matrix) → NAD+ + QH₂ + 4 H+(IMS)

Pumps 4 H+ per NADH oxidised.

### Complex II — Succinate dehydrogenase

The smallest + the only complex that's also a TCA enzyme.
Doesn't pump protons.

Succinate + Q → fumarate + QH₂.  FAD prosthetic group +
3 Fe-S clusters relay electrons.

### Complex III — Ubiquinol:cytochrome c oxidoreductase

The "Q cycle" — oxidises 2 QH₂ at a quinol-oxidising
(Qo) site + reduces 1 Q at a quinone-reducing (Qi) site,
net pumping 4 H+ per 2 electrons that arrive at
cytochrome c.

QH₂ + 2 cyt c(ox) + 2 H+(matrix) → Q + 2 cyt c(red) +
4 H+(IMS)

Mitchell's Q cycle (1976) doubled the proton-pumping
efficiency over the simple linear pumping model.

### Complex IV — Cytochrome c oxidase

Reduces O₂ to H₂O — the terminal electron acceptor +
why we breathe.

4 cyt c(red) + O₂ + 8 H+(matrix) → 4 cyt c(ox) + 2 H₂O
+ 4 H+(IMS)

Pumps 4 H+ per 4 electrons + consumes 4 H+ from the
matrix to make H₂O.  The O₂-binding active site has
heme a₃ + Cu_B.  Inhibited by cyanide + carbon monoxide
+ azide.

### Complex V — F1F0-ATP synthase

Not part of the ETC proper but the consumer of the
proton gradient.  Two rotary motors:

- **F0** — membrane-embedded, contains a ring of c
  subunits (8-15 depending on organism) + the a
  subunit.  Protons flowing through drive c-ring
  rotation.
- **F1** — matrix-side; α₃β₃γ stalk; the γ subunit
  rotates with the c-ring + drives sequential
  conformational changes in the three β subunits → ATP
  synthesis at each β site in turn.

## The chemiosmotic theory — Mitchell 1961

Peter Mitchell's 1961 chemiosmotic hypothesis was
revolutionary + initially controversial: oxidation +
phosphorylation are coupled by a **proton gradient**
across a membrane, not by a "high-energy intermediate"
(the prevailing wrong idea of the time).

Three predictions, all confirmed:

1. The membrane must be impermeable to protons (yes —
   inner mitochondrial membrane is famously tight).
2. ETC components must be vectorially organised (yes
   — Complexes I/III/IV all pump out, Complex IV
   consumes matrix protons).
3. ATP synthase must be reversible + driven by ΔµH+
   (yes — runs forward + can run backward as a proton-
   pumping ATPase).

Mitchell got the 1978 Nobel; Walker + Boyer got the 1997
Nobel for ATP synthase structure + binding-change
mechanism.

## ATP yield bookkeeping (modern)

The classical "38 ATP per glucose" overstated efficiency.
Modern estimates use:

- Each NADH → 2.5 ATP (10 H+ pumped, 4 H+ per ATP made
  + 1 H+ for ATP/Pi/ADP transport).
- Each FADH₂ → 1.5 ATP (6 H+ pumped).
- Mitochondrial NADH (PDH + TCA) → full 2.5 ATP each.
- Cytoplasmic NADH (glycolysis) → 1.5-2.5 ATP via
  shuttles.

Per glucose:

- Glycolysis: 2 ATP + 2 NADH (cyt) → ~ 5-7 ATP.
- PDH: 2 NADH (mt) → 5 ATP.
- TCA: 6 NADH + 2 FADH₂ + 2 GTP → 18 ATP from NADH +
  3 ATP from FADH₂ + 2 ATP-equivalents from GTP = 23.

**Total ~ 30-32 ATP per glucose.**

## Uncouplers + uncoupling proteins

Anything that lets protons leak across the inner
mitochondrial membrane uncouples electron transport from
ATP synthesis — energy released as heat.

- **2,4-Dinitrophenol (DNP)** — a weak acid that carries
  H+ across membranes.  Used as a weight-loss drug in the
  1930s; banned after deaths from hyperthermia.
- **CCCP, FCCP** — research uncouplers.
- **UCP1 (thermogenin)** — the brown-fat uncoupling
  protein.  Mammalian non-shivering thermogenesis.
  Activated by free fatty acids + cold.
- **UCP2/UCP3** — broader tissue distribution; metabolic-
  regulator roles still being characterised.

Brown-fat-mediated thermogenesis is an active drug-
discovery target for obesity / metabolic disease (β3-
adrenergic agonists like mirabegron activate brown
adipocyte UCP1).

## Inhibitors as research tools (and poisons)

- **Rotenone** (Complex I) — pesticide; Parkinson's
  research model when injected.
- **Antimycin A** (Complex III) — research reagent.
- **Cyanide / azide / CO** (Complex IV) — clinical
  poisons.  CO + cyanide are the leading causes of toxic
  inhalation death.
- **Oligomycin** (ATP synthase) — antibiotic.

## Diseases of OXPHOS

Mitochondrial diseases are genetically heterogeneous +
clinically variable:

- **Leber's hereditary optic neuropathy (LHON)** —
  Complex I subunit mtDNA mutations; sudden bilateral
  vision loss in young adults.
- **MELAS** (mitochondrial encephalopathy + lactic
  acidosis + stroke-like episodes) — mtDNA tRNA-Leu
  mutation A3243G.
- **MERRF** (myoclonic epilepsy + ragged-red fibres) —
  mtDNA tRNA-Lys mutation.
- **Leigh syndrome** — pediatric encephalopathy from
  many mt or nuclear mutations affecting OXPHOS.

mtDNA inheritance is maternal + heteroplasmic (mix of
WT + mutant mt copies per cell) — explains incomplete
penetrance + variable severity.

## Try it in the app

- **Window → Biochem Studio → Enzymes** — `cytochrome-
  c-oxidase` + `atp-synthase` entries.
- **Window → Biochem Studio → Cofactors** — `nadh`,
  `fadh2`, `ubiquinone`, `heme` entries.
- **Window → Biochem Studio → Metabolic pathways** —
  `ox_phos` entry.

Next: **Signalling-related enzymes**.
