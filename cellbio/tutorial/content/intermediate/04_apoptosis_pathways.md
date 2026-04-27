# Apoptosis + cell-death pathways

Apoptosis is regulated cell suicide — a clean, controlled
death without inflammation or release of cellular contents.
First named by Kerr, Wyllie + Currie in 1972 as the
counterpart to necrotic cell death.

## Why cells die on purpose

Programmed cell death is essential for:

- **Development** — interdigital web cells in mammalian
  embryos die to give us fingers; ~ 1000 of *C. elegans*'
  ~ 1090 cells die during development on a fixed
  developmental schedule (Brenner / Horvitz / Sulston
  Nobel 2002).
- **Tissue homeostasis** — your gut epithelium turns
  over completely every 5-7 days; senescent neutrophils
  die after a few days.
- **Immune-system shaping** — thymic negative selection
  kills self-reactive T-cell clones; B-cell germinal-
  centre selection kills low-affinity clones.
- **DNA damage** — irreparably damaged cells die rather
  than risk transformation.
- **Pathogen defence** — virally infected cells can
  trigger apoptosis to deny the virus a replication
  niche.

## Two major apoptosis pathways

### Intrinsic (mitochondrial) apoptosis

Triggered by intracellular stress — DNA damage, ER stress,
growth-factor withdrawal, oncogene activation.

The decision integrator is the **BCL-2 family** at the
mitochondrial outer membrane:

- **Anti-apoptotic** members: BCL-2, BCL-XL, MCL-1, A1.
  Hold death in check.
- **Pro-apoptotic effectors**: BAX, BAK. When activated,
  oligomerise to form pores in mitochondrial outer
  membrane.
- **BH3-only sensors**: BIM, BID, BAD, NOXA, PUMA.
  Sense cellular stress + tip the balance toward death
  by binding + inhibiting anti-apoptotic members or
  directly activating BAX/BAK.

When BAX/BAK pores open, **cytochrome c** spills from the
mitochondrial intermembrane space into cytosol →
assembles with APAF-1 + caspase-9 into the **apoptosome**
→ caspase-9 cleaves + activates executioner caspases
(caspase-3, -7) → cellular dismantling.

### Extrinsic (death-receptor) apoptosis

Triggered by extracellular signals — death-ligand binding
to a TNF-family death receptor.

Key ligand-receptor pairs:

- **FasL → Fas** (CD95) — T cells use this to kill virus-
  infected targets.
- **TRAIL → DR4 / DR5** — selectively triggers apoptosis
  in transformed cells (still under therapeutic
  exploration).
- **TNF-α → TNFR1** — context-dependent apoptosis vs
  pro-survival NF-κB activation.

Pathway:

1. Death-ligand trimerises death receptor.
2. Cytoplasmic death domain recruits FADD adaptor.
3. FADD recruits procaspase-8 (or -10) via DED-DED
   interactions → forms the **DISC** (death-inducing
   signalling complex).
4. Procaspase-8 trans-activates → cleaves caspase-3
   directly + cleaves BID → tBID activates BAX/BAK at
   mitochondria → amplifies via the intrinsic pathway.

## Other cell-death modalities

Apoptosis is not the only programmed death:

- **Necroptosis** — RIPK1-RIPK3-MLKL-driven; cell membrane
  ruptures + releases DAMPs that drive inflammation.
  Bypasses caspase block.
- **Pyroptosis** — caspase-1/4/5/11 cleave gasdermin →
  pore formation + inflammatory IL-1β release. Innate
  immune defence + sepsis driver.
- **Ferroptosis** — iron-dependent lipid peroxidation;
  GPX4 + glutathione protect against it. Active drug
  target in cancer (induce ferroptosis selectively in
  tumour cells).
- **Autophagy + autophagic cell death** — cytoplasm
  packaged into double-membrane autophagosomes that fuse
  with lysosomes. Mostly survival but excessive autophagy
  can kill cells.

## Caspases — the executioners

The caspase family of cysteine-aspartate proteases drives
apoptotic dismantling:

- **Initiator caspases**: 8, 9, 10. Activated by induced
  proximity in death-signalling complexes.
- **Executioner caspases**: 3, 6, 7. Cleave hundreds of
  substrates: PARP, ICAD/CAD (releases CAD to fragment
  DNA), lamins (nuclear envelope dissolution), structural
  proteins. Also cleaves + activates each other.
- **Inflammatory caspases**: 1, 4, 5, 11. Pyroptosis +
  inflammasome biology.

## Disease + therapy

Cancer cells routinely escape apoptosis by:
- Overexpressing BCL-2 (follicular lymphoma t(14;18)
  translocation puts BCL-2 under IGH promoter).
- Loss of p53 (most common cancer mutation; p53 induces
  PUMA + NOXA + BAX).
- Overexpressing IAPs (inhibitor of apoptosis proteins).

**BCL-2 inhibitors** (venetoclax) restore apoptosis in
CLL + AML — one of the textbook successes of targeted
therapy.

## Try it in the app

- **Cell Bio → Signalling** — `intrinsic-apoptosis`,
  `tnf-extrinsic-apoptosis`, `necroptosis`, `pyroptosis`
  entries.
- **Cell Bio → Cell cycle** — `p53-master-tumour-
  suppressor` entry covers the link from DNA damage to
  apoptosis.
- **Biochem → Enzymes** — `caspase-3` entry.

Next: **Wnt + Hedgehog + Notch — developmental signalling**.
