# MAPK / ERK — the prototype kinase cascade

The mitogen-activated protein kinase (MAPK) cascades are
the workhorses of growth-factor + stress signalling.
Three-tier kinase relays that amplify + filter signals on
the way from receptor to nucleus.

## The three-tier architecture

Every MAPK cascade has the same shape:

- **MAPKKK** (MAP kinase kinase kinase, e.g. RAF, ASK1)
  — phosphorylated by upstream small GTPase or scaffold.
- **MAPKK** (MAP kinase kinase, e.g. MEK1/2, MKK4/7)
  — phosphorylated by MAPKKK on Ser/Thr.
- **MAPK** (e.g. ERK1/2, JNK, p38) — phosphorylated by
  MAPKK on a TXY motif (TEY in ERK, TPY in JNK, TGY in
  p38).

Three sequential phosphorylation events between receptor +
gene-expression program. Each tier amplifies the signal.

## The canonical RAS → RAF → MEK → ERK pathway

The growth-factor branch:

1. **Growth-factor binding** — EGF binds EGFR; HGF binds
   MET; PDGF binds PDGFR; insulin binds insulin receptor.
2. **Receptor dimerisation + autophosphorylation** — RTK
   dimers trans-phosphorylate each other on C-terminal
   tyrosines.
3. **Adaptor recruitment** — phosphotyrosines bind GRB2's
   SH2 domain. GRB2 carries SOS (a Ras GEF) bound via SH3
   domains.
4. **Ras activation** — SOS exchanges GDP for GTP on Ras.
   Ras-GTP recruits Raf to the membrane.
5. **Raf activation** — membrane recruitment + 14-3-3
   release + phosphorylation activate Raf.
6. **MEK phosphorylation** — Raf phosphorylates MEK1/2 on
   two activation-loop serines.
7. **ERK phosphorylation** — MEK is a dual-specificity
   kinase that phosphorylates ERK1/2 on the TEY motif
   (T202 + Y204 in ERK1).
8. **Nuclear translocation** — phosphorylated ERK
   dimerises + translocates to the nucleus, phosphorylates
   transcription factors (Elk1, Myc, Fos), drives
   immediate-early gene expression (Fos, Jun) → AP-1
   transcription factor → cell-cycle entry.

## Why three tiers?

Three sequential kinases with cooperative input thresholds
give the cascade ultrasensitive switch-like behaviour
(Goldbeter + Koshland's "zero-order ultrasensitivity",
1981; Huang + Ferrell's MAPK switch demonstration in
*Xenopus* eggs, 1996).

Each kinase needs both activation-loop sites
phosphorylated (cooperative dual-phosphorylation), so the
input-output curve sharpens at each tier. The combined
cascade behaves like a near-step-function switch — perfect
for binary cell-fate decisions like proliferate vs not.

## Negative feedback + tuning

Several built-in negative feedback loops shape the response:

- **DUSPs** (dual-specificity phosphatases) — ERK targets
  that themselves dephosphorylate ERK. Negative feedback.
- **MAPK phosphatases** — soluble PP2A + nuclear DUSP1/6/9.
- **Sprouty + Spred proteins** — induced by ERK, inhibit
  upstream RAF + Ras.
- **Raf negative-feedback phosphorylation** — ERK
  phosphorylates Raf on inhibitory sites.

These shape ERK kinetics into transient pulses (mitogenic
proliferation) vs sustained signals (cell-cycle exit +
differentiation). Same molecules, different temporal
profile, different cell fate (Marshall 1995).

## Other MAPK branches

The same architecture supports other modules:

- **JNK** (c-Jun N-terminal kinase) — stress + cytokine +
  UV; phosphorylates Jun + ATF2.
- **p38** — inflammation + osmotic stress; activates
  MK2 + MNK + MSK kinases + numerous transcription
  factors.
- **ERK5** — stress + growth factors; less well-studied.

Cross-talk between branches gives cells nuanced stress vs
growth integration.

## Disease + therapeutic relevance

The RAS-RAF-MEK-ERK pathway is the most-mutated signalling
network in human cancer:

- **RAS mutations** (KRAS, NRAS, HRAS) — ~ 30 % of all
  human cancers. KRAS-G12C in NSCLC is now druggable
  (sotorasib, adagrasib).
- **BRAF mutations** — V600E in 50 % of melanomas, 5 % of
  CRCs. Vemurafenib + dabrafenib + encorafenib are
  approved BRAF inhibitors.
- **MEK inhibitors** — trametinib, cobimetinib, binimetinib;
  used in combo with BRAF inhibitors to delay resistance.
- **EGFR mutations** — exon 19 deletions + L858R in
  NSCLC; targeted by erlotinib, gefitinib, osimertinib.

The pathway's centrality to cancer is why kinase inhibitors
are the dominant modern oncology drug class.

## Try it in the app

- **Window → Cell Biology Studio → Signalling** — `mapk-
  erk` + `egfr-ras-raf` entries.
- **Window → Cell Biology Studio → Cell cycle** — `cyclin-
  d-cdk4-cdk6` entry shows MAPK output driving G1
  progression.
- **Window → Pharmacology Studio → Drug classes** —
  `kinase-inhibitors` entry covers the BRAF + MEK + EGFR
  drug families.

Next: **GPCR signalling deep-dive**.
