# Glycolysis and the citric-acid cycle

The two central pathways of energy metabolism.  Glycolysis
breaks glucose to pyruvate in the cytoplasm; the TCA cycle
oxidises pyruvate-derived acetyl-CoA to CO₂ in the
mitochondrial matrix.  Together they extract reducing
equivalents for ATP synthesis.

## Glycolysis — the 10 steps

Universal across all kingdoms.  Two phases:

### Energy investment (steps 1-5)

- **Step 1: Hexokinase** — glucose + ATP → glucose-6-
  phosphate + ADP.  Traps glucose in the cell + commits
  to metabolism.
- **Step 2: Phosphoglucose isomerase** — G6P → fructose-
  6-phosphate.
- **Step 3: PFK-1 (phosphofructokinase-1)** — F6P + ATP
  → fructose-1,6-bisphosphate + ADP.  **The main
  regulatory step.**
- **Step 4: Aldolase** — F1,6BP → DHAP + GAP (two
  3-carbon units).
- **Step 5: Triose-phosphate isomerase (TIM)** — DHAP
  ↔ GAP.  Both DHAP molecules are interconverted to
  GAP for further metabolism.

After step 5, you've spent **2 ATP** + you have **2 GAP**.

### Energy yield (steps 6-10)

- **Step 6: GAPDH (glyceraldehyde-3-phosphate
  dehydrogenase)** — GAP + NAD+ + Pi → 1,3-bisphospho-
  glycerate + NADH.  The oxidation step.
- **Step 7: Phosphoglycerate kinase** — 1,3-BPG + ADP →
  3-phosphoglycerate + **ATP**.  Substrate-level
  phosphorylation.
- **Step 8: Phosphoglycerate mutase (PGAM)** — 3-PG ↔
  2-PG.
- **Step 9: Enolase** — 2-PG → phosphoenolpyruvate (PEP)
  + H₂O.
- **Step 10: Pyruvate kinase (PK)** — PEP + ADP →
  pyruvate + **ATP**.  Substrate-level phosphorylation.

## Glycolysis bookkeeping

Per glucose (counting both 3-C halves):

- Spent: 2 ATP (steps 1, 3).
- Made: 4 ATP (steps 7, 10 — twice each).
- **Net: 2 ATP, 2 NADH, 2 pyruvate.**

The NADH must be re-oxidised so glycolysis can continue.
Two main fates:

- **Aerobic** — pyruvate enters mitochondria, NADH used
  in the ETC for ~ 2.5 ATP each.
- **Anaerobic** — lactate dehydrogenase regenerates NAD+
  by reducing pyruvate to lactate.  No additional ATP,
  but glycolysis can keep running.  Muscle during
  intense exercise; red blood cells (no mitochondria);
  fermentative microbes.

## Glycolysis regulation

Three irreversible steps are regulated:

- **Hexokinase** — feedback-inhibited by G6P
  (accumulates if downstream is blocked).  Liver
  isozyme (glucokinase / hexokinase IV) has higher Km
  + isn't inhibited by G6P → liver only takes up
  glucose at high blood glucose.
- **PFK-1** — the main rate-controlling step.  Inhibited
  by ATP + citrate (high energy = stop), activated by
  AMP + ADP (low energy = go), activated by **fructose-
  2,6-bisphosphate** (the master glycolysis-vs-gluconeo-
  genesis signal, controlled by hormone-driven PFK-2/
  FBPase-2 bifunctional enzyme).
- **Pyruvate kinase** — feedback-inhibited by ATP +
  alanine; allosterically activated by F1,6BP (feed-
  forward).  Liver isozyme phosphorylated + inhibited
  by glucagon-driven PKA.

## Pyruvate dehydrogenase — the gateway

Pyruvate enters mitochondria via the pyruvate carrier,
where the **pyruvate dehydrogenase complex (PDH)**
oxidatively decarboxylates it to acetyl-CoA:

```
Pyruvate + CoA + NAD+ → Acetyl-CoA + NADH + CO₂
```

PDH is a massive complex (~ 9 MDa, > 100 subunits)
combining three enzymes (E1 = decarboxylase, TPP
cofactor; E2 = acetyl-transferase, lipoyl + CoA; E3 =
dihydrolipoyl dehydrogenase, FAD + NAD+).  The lipoyl-
arm "swinging arm" shuttles acetyl groups + electrons
between active sites.

PDH is regulated by:

- **PDH kinase** — phosphorylates + inactivates E1 when
  energy is high (high acetyl-CoA / CoA ratio, high
  NADH / NAD+).
- **PDH phosphatase** — reverses; activated by Ca²⁺
  (muscle contraction signal).

## The TCA cycle — the 8 steps

Hans Krebs's 1937 cycle (Nobel 1953).  All in the
mitochondrial matrix; 8 enzymes:

1. **Citrate synthase** — acetyl-CoA + oxaloacetate +
   H₂O → citrate + CoA.  **Strongly exergonic** + the
   committed step.
2. **Aconitase** — citrate ↔ isocitrate (via cis-aconitate
   intermediate; Fe-S protein).
3. **Isocitrate dehydrogenase (IDH)** — isocitrate +
   NAD+ → α-ketoglutarate + CO₂ + NADH.  Major
   regulatory step; activated by ADP + Ca²⁺, inhibited
   by NADH + ATP.
4. **α-Ketoglutarate dehydrogenase (α-KGDH)** —
   α-KG + CoA + NAD+ → succinyl-CoA + CO₂ + NADH.
   Mechanistically identical to PDH (TPP + lipoate +
   FAD + NAD+).  Inhibited by NADH + succinyl-CoA.
5. **Succinyl-CoA synthetase** — succinyl-CoA + GDP +
   Pi → succinate + CoA + **GTP**.  Substrate-level
   phosphorylation.
6. **Succinate dehydrogenase (Complex II of the ETC)** —
   succinate + FAD → fumarate + FADH₂.  The only
   membrane-bound TCA enzyme; embedded in the inner
   mitochondrial membrane.
7. **Fumarase** — fumarate + H₂O → malate.
8. **Malate dehydrogenase** — malate + NAD+ →
   oxaloacetate + NADH.  Closes the cycle.

## TCA bookkeeping

Per acetyl-CoA processed:

- 3 NADH (steps 3, 4, 8).
- 1 FADH₂ (step 6 — succinate dehydrogenase).
- 1 GTP (step 5 — substrate-level).
- 2 CO₂ (steps 3, 4).

Each glucose feeds 2 acetyl-CoA into the cycle, so per
glucose: **6 NADH + 2 FADH₂ + 2 GTP** from the TCA
phase.

## The full glucose ledger

Adding glycolysis + PDH + TCA + ETC:

- Glycolysis: 2 ATP, 2 NADH (cytoplasm).
- PDH: 2 NADH (matrix).
- TCA: 6 NADH + 2 FADH₂ + 2 GTP.
- ETC: each NADH → ~ 2.5 ATP, each FADH₂ → ~ 1.5 ATP.
- Cytoplasmic NADH transfer to matrix via shuttles
  (malate-aspartate or glycerol-3-P): efficient ~ 2.5,
  inefficient ~ 1.5 ATP per cytoplasmic NADH.

**Total: ~ 30-32 ATP per glucose.**  The historical
"38 ATP" textbook figure assumed integer stoichiometry
that turned out to be optimistic.

## Why this matters clinically

- **Warburg effect** — many cancers preferentially do
  aerobic glycolysis (high glucose uptake + lactate
  output even with O₂ available).  Basis of FDG-PET
  imaging.
- **PDH deficiency** — paediatric lactic acidosis +
  neurological dysfunction.
- **IDH1/2 mutations** — gain-of-function R132H in IDH1
  produces 2-hydroxyglutarate (oncometabolite), drives
  ~ 70 % of secondary glioblastoma + 20 % of AML.
  Targeted by enasidenib (IDH2) + ivosidenib (IDH1).
- **Fumarase + SDH mutations** — rare familial cancer
  syndromes (HLRCC, paragangliomas).

## Try it in the app

- **Window → Biochem Studio → Enzymes** — `hexokinase`,
  `gapdh`, `aldolase-a`, `tim`, `phosphoglycerate-
  mutase` cover the glycolysis enzymes; `cytochrome-c-
  oxidase` covers the ETC integration.
- **Window → Biochem Studio → Cofactors** — `nad-plus`,
  `nadh`, `acetyl-coa`, `tpp`, `lipoate`, `coa` cover
  the cofactors.
- **Window → Biochem Studio → Metabolic pathways** for
  full pathway diagrams.

Next: **Oxidative phosphorylation + chemiosmosis**.
