# PCR + qPCR + diagnostics — practical considerations

The GM-1.0 catalogue lists endpoint PCR + qPCR + dPCR
as headline techniques.  This intermediate lesson
covers the practical bench-side details: primer design,
optimisation, troubleshooting, controls, and the
clinical-diagnostic considerations that distinguish a
successful assay from a failed one.

## Primer design

A good primer pair determines almost everything.

### Length + Tm

- **Primer length** — 18-25 nt typical.
- **Tm** — match within ~ 2-5 °C between forward +
  reverse; use Wallace rule for short oligos or
  nearest-neighbor for accurate predictions.
- **Annealing temperature** — typically Tm − 5 °C.

### GC content + 3' end

- **GC content** — 40-60 % ideal.
- **3' end** — avoid GC-rich runs (mispriming risk);
  end on G or C (improved binding) but not GG / CC /
  GGC.
- **Avoid** > 4 same-base runs, especially T (poly-T
  is a low-info anchor).

### Specificity

- BLAST every primer against the relevant transcriptome
  + genome before ordering.
- Avoid primers spanning common SNPs (use dbSNP +
  gnomAD lookup).
- For RNA assays, span an exon-exon junction to
  exclude gDNA contamination.

### Duplex avoidance

- **Self-complementarity** — avoid hairpins (5+ bp
  stems with low ΔG).
- **Primer-dimer** — avoid forward + reverse
  3'-end complementarity.
- Use OligoAnalyzer / Primer3 / Beacon Designer for
  thermodynamic analysis.

### Primer concentration

- Endpoint PCR: 0.2-0.5 µM each.
- qPCR: 0.1-0.4 µM each (lower because high-cycle).
- Multiplex: 0.05-0.2 µM each per pair (avoid
  saturation).

## Polymerase choice

| Polymerase | Use case | Notes |
|------------|----------|-------|
| Taq | Cheap routine PCR + diagnostics | High error rate (~ 10⁻⁴); 5'→3' exonuclease (TaqMan-compatible); A-tailed product |
| Phusion / Q5 / KAPA HiFi | Cloning + sequencing-grade | High fidelity (~ 10⁻⁶); 3'→5' proofreading; blunt product |
| Pfu | Cloning (legacy) | High fidelity but slower than Phusion / Q5 |
| Phusion U / KAPA HiFi U | dU-tolerant cloning | For UDG carryover prevention; for damaged-DNA handling |
| Bst (LF) | Isothermal LAMP | Strand-displacing; ~ 60-65 °C |
| Sau / RPA polymerases | RPA isothermal | ~ 37-42 °C |
| iTaq / SsoAdvanced | qPCR | Optimised buffer + reporters bundled |

## Cycling parameters

Standard 3-step cycle:
1. **Initial denaturation** — 95 °C, 30 s-3 min
   (depends on polymerase activation).
2. **Cycle** (typically 25-40 cycles):
   - Denature: 95 °C, 10-30 s.
   - Anneal: Tm − 5 °C, 15-30 s.
   - Extend: 72 °C (Taq) or 60 °C (Q5 / Phusion),
     ~ 1 min / kb.
3. **Final extension** — 72 °C, 5 min.

Two-step cycling (fast PCR) combines anneal +
extend at a single temperature (~ 60-65 °C); used
for short amplicons + automated systems.

Touchdown PCR — start anneal high (Tm + 5 °C) +
decrement 1 °C / cycle for the first 10-15 cycles
to improve specificity.

## Controls

Every diagnostic + research PCR should include:

- **No-template control (NTC)** — water in place of
  template; detects reagent / cross-contamination.
- **Positive control** — known target template;
  detects inhibition + reagent issues.
- **Internal control / housekeeping target** —
  detects sample-prep failure.
- **Inhibition control** — spiked exogenous template;
  detects sample-derived PCR inhibition.
- **Genomic-DNA control (for cDNA)** — confirms RNA
  prep wasn't contaminated.

For clinical diagnostics:
- Run-to-run + lot-to-lot positive controls.
- Validated cut-offs from analytical / clinical
  performance studies (LoD, LoQ, sensitivity,
  specificity).

## qPCR analysis

### Curve interpretation

- **Baseline** — fluorescence noise before signal;
  typically cycles 3-15.
- **Threshold** — set above noise but in the
  exponential phase.
- **Cq / Ct** — cycle at which signal crosses
  threshold; lower Cq = more starting template.
- **Plateau** — saturated signal; uninformative.

### Quantification approaches

- **Absolute** — standard curve of known-
  concentration template; report copies / µL.
- **Relative ΔΔCt (Livak)** — compare gene-of-
  interest to reference gene across conditions;
  assumes 100 % efficiency + matched references.
- **Pfaffl method** — efficiency-corrected ΔΔCt.

### Efficiency calculation

- Standard curve: serial dilutions over 5-6 logs.
- Slope = -3.32 → 100 % efficiency (E = 10^(-1/slope)
  − 1).
- Acceptable range: 90-110 % (slope -3.6 to -3.1).
- R² ≥ 0.99 expected.

### Melt-curve analysis (SYBR-based)

- Single peak = specific product.
- Multiple peaks = primer-dimer or non-specific
  amplification.
- Tm shift = SNP / variant detection (high-
  resolution melt, HRM).

### MIQE guidelines (Bustin 2009)

The Minimum Information for Publication of
Quantitative Real-Time PCR Experiments — a checklist
for reproducible qPCR reporting.  Cite when designing
+ when reading literature critically.

## Multiplexing

Combine multiple targets in one well:
- Sequence-specific probes (TaqMan / molecular-
  beacon / Scorpion) with distinct fluorophores.
- 4-5 plex routine; 8-12 plex with careful design.
- Avoid spectral overlap (FAM / VIC / TAMRA / Cy5 /
  ROX combinations).
- Validate that multiplex performance matches
  singleplex (no cross-reactivity, no efficiency
  loss).

Examples:
- BioFire FilmArray syndromic panels (~ 20-40
  targets per cartridge).
- GeneXpert MTB/RIF (TB + rifampicin resistance in
  one cartridge).
- COVID-19 multi-target screens (N + ORF1ab + RP
  human reference).

## Digital PCR (dPCR) practicalities

- Partition into 10⁴-10⁶ droplets / chambers.
- Each contains 0 or 1 template (Poisson).
- Endpoint PCR + binary fluorescence per partition.
- Poisson math gives absolute concentration WITHOUT
  standard curve.

When dPCR > qPCR:
- Rare-variant detection (cancer ctDNA, transplant
  monitoring).
- Absolute quantification (viral load standards,
  GMO quantification).
- Inhibitor-containing samples (partition isolates
  inhibition effects).

When qPCR > dPCR:
- High-throughput screening.
- Wider dynamic range at high concentrations.
- Cheaper per sample.
- Faster.

## Troubleshooting

| Symptom | Likely causes | Fix |
|---------|---------------|-----|
| No bands at all | Template degraded / no enzyme / wrong primers / wrong cycling | Run NTC + positive control; check primer Tm + concentration |
| Faint bands | Low template / suboptimal annealing / mediocre primers | Increase template; lower anneal Tm by 2-5 °C; redesign primers |
| Multiple bands | Non-specific priming / mispriming | Increase anneal Tm; touchdown PCR; reduce primer concentration; nest |
| Smear | Excessive cycles / low-quality template | Reduce cycles; clean up template; check for contamination |
| High NTC signal | Reagent / aerosol contamination | Trash + replace reagents; clean workspace; UDG / dUTP system |
| Primer-dimer (qPCR) | Poor primer design | Redesign primers; raise anneal Tm; reduce primer concentration |
| Plateau at low Cq | PCR inhibitors in sample | Re-purify template; dilute sample; spike inhibition control |

## Sample preparation

The molecular-biology adage: "garbage in, garbage out."

- **Blood** — EDTA + Heparin will inhibit PCR;
  use citrate or specialised collection tubes
  (Streck, Cell-Free DNA BCT) for cfDNA.
- **FFPE tissue** — fragmented + crosslinked DNA;
  use Qiagen FFPE kits + amplicon-based panels;
  consider EM-seq instead of bisulfite.
- **Saliva / swabs** — surface contamination from
  oral microbiome; primer specificity matters.
- **Plant tissue** — polysaccharides + phenolics
  inhibit; CTAB-based extractions standard.
- **Soil + environmental DNA** — humic acids inhibit
  severely; multi-stage extraction +
  inhibitor-removal kits (PowerClean, OneStep).
- **Stool** — bile salts + complex polysaccharides;
  specialised stool DNA kits (QIAamp PowerFecal).

## Diagnostic-context considerations

- **Analytical sensitivity** = limit of detection
  (LoD) — lowest concentration reliably detected
  (95 % +).
- **Analytical specificity** — does the assay
  detect the intended target without cross-
  reactivity?
- **Clinical sensitivity** = positive percent
  agreement (PPA) — fraction of true positives the
  assay finds.
- **Clinical specificity** = negative percent
  agreement (NPA) — fraction of true negatives
  the assay clears.
- **Positive + negative predictive values
  (PPV / NPV)** — depend on prevalence (Bayes).

For clinical-grade assays, expect formal validation
studies (LoD, LoQ, accuracy, precision, linearity,
interference, comparison-of-methods, stability) +
ongoing QC (Westgard rules, EQA / proficiency
testing).

## Cross-link

The GM-1.0 catalogue's `endpoint-pcr`, `qpcr`,
`digital-pcr`, and `isothermal-amplification` entries
provide the technology-card context.  This lesson
adds the bench-practical layer.

## Try it in the app

- **Window → Genetics + Molecular Biology Studio →
  Techniques → PCR family** — review the 4 PCR-
  family entries.
- **OrgChem → Database** — Adenine + Guanine +
  Cytosine + Thymine for the foundational
  chemistry.
- **Window → Microbiology Studio → Microbes** —
  pathogens diagnosed by qPCR + multiplex panels.

Next: **NGS workflow + bioinformatics**.
