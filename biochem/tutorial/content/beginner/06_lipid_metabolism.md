# Lipid metabolism deep-dive

Lipids are the cell's energy store, membrane
building block, signalling messenger, and steroid-
hormone precursor.  Lipid metabolism integrates
nutrition, hormonal control, organ specialisation,
and disease risk in ways that no other macromolecule
quite matches.

## Fatty acid biology

### Structure + nomenclature

- **Saturated** — no double bonds (palmitic 16:0,
  stearic 18:0).
- **Monounsaturated (MUFA)** — one double bond
  (oleic 18:1 ω-9).
- **Polyunsaturated (PUFA)** — multiple double
  bonds; ω-3 (linolenic 18:3, EPA 20:5, DHA 22:6)
  + ω-6 (linoleic 18:2, arachidonic 20:4) families.
- **Essential** — linoleic + α-linolenic (humans
  cannot make ω-6 + ω-3 starting carbons).
- **Trans-fats** — trans-double-bond isomers;
  industrial hydrogenation by-products; banned in
  many countries since 2018+.

### Fatty acid synthesis

Site: **cytosol** (mostly liver + adipose +
lactating mammary).

- **Acetyl-CoA** comes from mitochondrial citrate
  via citrate-malate shuttle (cytosolic ATP-
  citrate lyase).
- **Acetyl-CoA carboxylase (ACC)** — biotin-
  dependent; carboxylates acetyl-CoA → malonyl-CoA.
  RATE-LIMITING + insulin/glucagon-regulated.
  Inhibited by long-chain acyl-CoA (feedback).
- **Fatty acid synthase (FAS)** — large
  multifunctional polypeptide; iteratively
  condenses acetyl + malonyl onto growing chain
  (2-carbon-at-a-time elongation) using NADPH from
  PPP.  Releases palmitate (16:0).
- Subsequent **elongation** (in ER + mito) →
  18:0, 20:0, etc.
- **Desaturation** by SCD-1 (Δ9), FADS1 (Δ5),
  FADS2 (Δ6) → MUFA + PUFA.

### β-oxidation

Site: **mitochondrial matrix** (long-chain) +
**peroxisomes** (very-long-chain + branched).

Each cycle:
1. Acyl-CoA dehydrogenase → trans-Δ²-enoyl-CoA
   (generates FADH₂).
2. Enoyl-CoA hydratase → L-3-hydroxyacyl-CoA.
3. β-hydroxyacyl-CoA dehydrogenase → β-ketoacyl-
   CoA (generates NADH).
4. Thiolase → acetyl-CoA + acyl-CoA (n-2).

Net per cycle: 1 FADH₂ + 1 NADH + 1 acetyl-CoA;
acyl chain shortens by 2 carbons.

Palmitate (16:0) → 8 acetyl-CoA + 7 FADH₂ + 7
NADH = 106 ATP equivalents (vs 32-38 for glucose).
Lipid is energy-dense — that's WHY adipose stores
energy as lipid not glycogen.

### Carnitine shuttle

Long-chain fatty acids enter mitochondria via:
- **CPT-I** (outer membrane) — converts acyl-CoA
  to acyl-carnitine.  Inhibited by malonyl-CoA
  (the ACC product → so when fat synthesis is on,
  fat oxidation is off).
- **Carnitine-acylcarnitine translocase**.
- **CPT-II** (inner membrane) — regenerates acyl-
  CoA in matrix.

CPT-II deficiency → exercise-induced
rhabdomyolysis (most-common adult lipid-myopathy).

### Ketogenesis

When acetyl-CoA outpaces TCA capacity (starvation,
prolonged exercise, low-carb diets, T1DM):

- HMG-CoA synthase + lyase in liver mitochondria
  → acetoacetate + β-hydroxybutyrate (the major
  circulating ketone).
- Acetone is a minor non-utilisable by-product
  (the "fruity breath").
- Brain + heart + muscle import + reconvert ketones
  to acetyl-CoA for energy.
- Liver itself can't use ketones (lacks succinyl-
  CoA-acetoacetate transferase).

DKA (diabetic ketoacidosis) — uncontrolled
hepatic ketogenesis with insulin lack →
acidosis + dehydration; medical emergency.

## Triglyceride storage + mobilisation

### Storage (fed state)

Adipocytes import fatty acids via:
- **LPL (lipoprotein lipase)** — endothelial-
  capillary-luminal; hydrolyses TG in chylomicrons
  + VLDL → free fatty acids + glycerol → adipocyte
  uptake.
- Esterification to TG via DGAT1 + DGAT2 → lipid
  droplet storage.

### Mobilisation (fasted / stressed state)

Adipose lipolysis:
- **ATGL (PNPLA2)** — TG → DAG (rate-limiting).
- **HSL (hormone-sensitive lipase)** — DAG → MAG;
  PKA-phosphorylated → activated by glucagon +
  catecholamines.
- **MGL** — MAG → glycerol + free fatty acid.
- **Perilipin** — phosphorylated by PKA → exposes
  lipid droplet to lipases.

FFAs released → blood → bound to albumin → liver
+ muscle uptake.

## Cholesterol biosynthesis

The **mevalonate pathway** in cytosol + ER:

1. Acetyl-CoA + acetyl-CoA → acetoacetyl-CoA.
2. + acetyl-CoA → HMG-CoA.
3. **HMG-CoA reductase** → mevalonate (RATE-
   LIMITING; statin target).
4. ATP-dependent phosphorylation + decarboxylation
   → IPP (isopentenyl pyrophosphate, the C5
   building block).
5. IPP + DMAPP condense to FPP (C15) + GGPP (C20)
   + squalene (C30) → cyclisation → lanosterol →
   ~ 19 enzymatic steps → cholesterol.

Cholesterol regulation:
- **SREBP-2** transcription factor, ER-membrane-
  bound; sensed via SCAP-Insig + cleaved by S1P /
  S2P proteases when cholesterol is low →
  upregulates HMGCR + LDLR + other biosynthesis +
  uptake genes.
- **LDLR** (LDL receptor) — clathrin-mediated
  endocytic uptake of plasma LDL particles.

## Lipoprotein metabolism

Lipoproteins solubilise lipids in plasma:

| Class | Origin | Triglycerides | Cholesterol | Apolipoproteins | Function |
|-------|--------|---------------|-------------|-----------------|----------|
| Chylomicron | Intestine | Very high | Low | ApoB-48, ApoC, ApoE | Dietary lipid transport |
| VLDL | Liver | High | Moderate | ApoB-100, ApoC, ApoE | Endogenous TG transport |
| IDL | VLDL remnant | Moderate | Moderate | ApoB-100, ApoE | Transient |
| LDL | IDL → LDL | Low | High | ApoB-100 | Cholesterol delivery to peripheral tissues |
| HDL | Liver + intestine | Low | Variable | ApoA-I, ApoA-II | Reverse cholesterol transport |

### Clinical relevance

- **High LDL** → atherosclerosis + CV disease
  risk.
- **Low HDL** → CV risk.
- **Hypertriglyceridaemia** > 5 mmol/L → acute
  pancreatitis risk.
- **Familial hypercholesterolaemia (FH)** — LDLR
  / APOB / PCSK9 / LDLRAP1 mutations; AD; LDL
  > 5 mmol/L untreated; high CV risk.
- **Familial chylomicronaemia syndrome** — LPL /
  APOC2 / APOA5 / GPIHBP1 / LMF1 mutations.

### Drugs

- **Statins** — HMG-CoA reductase inhibitors;
  workhorse LDL-lowering.
- **Ezetimibe** — NPC1L1 inhibitor; intestinal
  cholesterol absorption.
- **PCSK9 inhibitors** — alirocumab + evolocumab
  (mAbs); inclisiran (siRNA) — long-acting LDL
  lowering.
- **Bempedoic acid** — ATP-citrate lyase
  inhibitor.
- **Fibrates** (fenofibrate, gemfibrozil) — PPARα
  agonists; lower TG + raise HDL.
- **Omega-3 fatty acids** (icosapent ethyl /
  Vascepa) — TG lowering + REDUCE-IT CV benefit.
- **Volanesorsen** (ASO targeting APOC3) +
  **olezarsen** — chylomicronaemia / severe HTG.
- **Lomitapide** — MTP inhibitor; HoFH.

## Phospholipid + sphingolipid synthesis

### Glycerophospholipids

- **Kennedy pathway** — choline + ATP →
  phosphocholine → CDP-choline → PC.  Analogous
  for ethanolamine → PE.
- **PSS-1 + PSS-2** — PS synthesis from PC + PE
  via base exchange.
- **PG + cardiolipin** in mitochondria.

### Sphingolipids

- Serine + palmitoyl-CoA → sphinganine →
  ceramide.
- Ceramide → SM (sphingomyelin) + glucosylceramide
  + galactosylceramide.
- Sphingosine-1-phosphate is a signalling
  metabolite (S1P-receptor GPCR target;
  fingolimod).

## Eicosanoids

Arachidonic acid (20:4 ω-6) released from
membrane PL by **PLA2** + metabolised by:
- **COX-1 + COX-2** → prostaglandins +
  thromboxanes.
- **5-LOX + 12-LOX + 15-LOX** → leukotrienes +
  lipoxins.
- **CYP450 epoxygenases** → EETs.

Drug targets:
- NSAIDs + coxibs — COX inhibitors.
- Montelukast + zafirlukast — LTC₄/D₄/E₄ receptor
  antagonists.
- Zileuton — 5-LOX inhibitor.
- Aspirin — irreversible COX acetylator.

## Tissue specialisation

- **Liver** — major lipogenesis + ketogenesis +
  cholesterol synthesis + lipoprotein assembly +
  bile-acid synthesis.
- **Adipose** — TG storage; lipolysis on demand.
- **Muscle** — β-oxidation during exercise +
  fasting.
- **Heart** — heavy fatty-acid utilisation
  (~ 60-70 % of cardiac fuel).
- **Brain** — long-chain PUFA dependent (DHA);
  myelin = mostly sphingolipids + cholesterol.
- **Adrenal cortex** + **gonads** — steroid-
  hormone biosynthesis (pregnenolone →
  progesterone → cortisol / aldosterone /
  androgens / oestrogens).
- **Intestine** — chylomicron assembly + bile-
  acid recycling.

## Lipid disorders + IEMs

- **Familial hypercholesterolaemia** — covered above.
- **Familial chylomicronaemia syndrome** — covered.
- **Tangier disease** — ABCA1 mutation; very-low
  HDL.
- **LCAT deficiency** + **fish-eye disease** —
  HDL maturation.
- **CESD + Wolman** — lysosomal acid lipase
  deficiency (covered in **CB-4.0 advanced
  "Lysosomal storage diseases"**).
- **Adrenoleukodystrophy (X-ALD)** — VLCFA
  accumulation (peroxisomal ABCD1 defect).
- **Refsum disease** — phytanic acid accumulation
  (peroxisomal α-oxidation).
- **Sphingolipidoses** — Gaucher, Tay-Sachs,
  Niemann-Pick, Fabry, Krabbe, MLD (CB-4.0
  LSD lesson).

## Cross-link

For sphingolipid-storage diseases, see **CB-4.0
advanced "Lysosomal storage diseases"**.  For
membrane-lipid biology + rafts, see **CB-4.0
beginner "Membrane lipids + rafts"**.  For
metabolism integration, see the upcoming **BC-4.0
intermediate "Pentose phosphate + integrated
metabolism" lesson** + **BC-4.0 intermediate
"Hormonal control of metabolism" lesson**.

## Try it in the app

- **OrgChem → Macromolecules → Lipids** — full
  lipid catalogue.
- **Window → Biochem Studio → Metabolic pathways**
  — fatty-acid synthesis + β-oxidation +
  cholesterol-biosynthesis pathways.
- **Window → Biochem Studio → Enzymes** — ACC +
  HMG-CoA reductase + CPT-I + fatty-acid
  synthase entries.
- **Window → Pharmacology Studio → Drug classes**
  — statins + PCSK9 inhibitors + fibrates +
  fish-oil + ezetimibe.

Next: **Amino-acid metabolism**.
