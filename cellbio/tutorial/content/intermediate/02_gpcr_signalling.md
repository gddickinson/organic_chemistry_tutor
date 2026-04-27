# GPCR signalling deep-dive

GPCRs are the largest family of cell-surface receptors
(~ 800 in the human genome) and the targets of about 30 %
of approved drugs. Understanding GPCR signalling
mechanically is understanding most of modern pharmacology.

## The 7-TM architecture

Every GPCR has the same fold: seven transmembrane α-helices
connected by three extracellular loops + three intracellular
loops, with an extracellular N-terminus and an intracellular
C-terminus.

Ligand-binding modes vary by class:

- **Class A** (rhodopsin-like, the largest) — small-
  molecule ligands bind in a transmembrane pocket
  (β-adrenergic agonists, opioid agonists, biogenic
  amines, peptide hormones via extracellular loops).
- **Class B** (secretin family) — peptide ligands bind
  the large extracellular N-terminal domain (glucagon,
  GLP-1, calcitonin, parathyroid hormone).
- **Class C** (metabotropic glutamate-like) — large bi-
  lobed Venus-flytrap extracellular domain (mGluRs,
  GABA-B, calcium-sensing receptor, sweet/umami taste).
- **Adhesion GPCRs** — long extracellular adhesion-domain
  N-terminus that gets autoproteolytically cleaved.

## Heterotrimeric G-proteins

The "G" in GPCR is for **G-protein** (heterotrimeric guanine-
nucleotide-binding protein). Each is α + β + γ subunits
held together when α is GDP-bound.

Receptor activation acts as a **GEF** (guanine nucleotide
exchange factor) for Gα: GDP leaves, GTP binds, the trimer
falls apart. Both Gα-GTP + Gβγ are signalling-active.

**Termination**: Gα has slow intrinsic GTPase activity (~
seconds-minutes), accelerated by **RGS** proteins (regulators
of G-protein signalling). GDP-bound Gα re-associates with
βγ, ready for the next round.

## Gα subfamilies

Four major Gα families couple to different downstream
effectors:

- **Gαs** (stimulatory) → activates adenylate cyclase →
  ↑cAMP → PKA. β-adrenergic, dopamine D1, glucagon, PTH.
- **Gαi/o** (inhibitory) → inhibits adenylate cyclase →
  ↓cAMP. βγ → activates GIRK K⁺ channels +
  inhibits Cav channels in neurons. M2 muscarinic,
  α2-adrenergic, opioid, dopamine D2.
- **Gαq/11** → activates PLCβ → IP3 + DAG → Ca²⁺ + PKC.
  α1-adrenergic, M1/M3/M5 muscarinic, AT1 angiotensin,
  H1 histamine.
- **Gα12/13** → activates Rho GEFs → Rho GTPases →
  cytoskeletal rearrangement. Thrombin (PAR-1), LPA,
  S1P.

A single receptor can couple to multiple Gα subtypes —
either weakly to several or strongly to one with weaker
secondary couplings. Promiscuity gives signalling breadth.

## Gβγ signalling

Long thought to be a "regulatory subunit", Gβγ is now
understood to be itself signalling-active:

- Activates **PI3Kγ** in immune cells.
- Activates **PLCβ** (β2/β3 isoforms).
- Opens **GIRK K⁺ channels** (cardiac M2 → vagal slowing).
- Inhibits **N-type Cav channels** (presynaptic
  neurotransmitter release).
- Recruits **GRKs** for receptor desensitisation.

## Desensitisation + arrestin signalling

After agonist binding, GRK kinases (G-protein-coupled
receptor kinases) phosphorylate the receptor's C-terminal
tail. Phosphorylated receptor recruits **β-arrestin**.

β-arrestin does three things:

1. **Sterically blocks** further G-protein coupling →
   homologous desensitisation.
2. **Recruits clathrin + AP2** → receptor endocytosis.
3. **Scaffolds its own signalling cascades** — recruits
   ERK, JNK, Akt, c-Src independently of G-protein.

This is **biased agonism**: ligands can preferentially
activate G-protein vs β-arrestin signalling. Oliceridine
(opioid analgesic, FDA 2020) was developed as a G-protein-
biased μ-agonist hoping to dissociate analgesia (G-protein-
mediated) from respiratory depression (β-arrestin-mediated)
— the clinical advantage remains debated.

## Why GPCRs are great drug targets

- **Cell-surface accessible** — drugs don't need to cross
  the plasma membrane.
- **Druggable pocket** — the orthosteric site is a defined
  small-molecule pocket.
- **Family diversity** — 800 GPCRs gives broad target
  space; subtype selectivity is achievable with careful
  medicinal chemistry.
- **Allosteric sites** — give cleaner subtype selectivity
  + ceiling effects.
- **Validated biology** — many GPCRs have well-known
  endogenous-ligand pharmacology that translates directly.

The major GPCR drug classes: β-blockers, α-blockers, ARBs,
β2-agonists, opioids, antihistamines, neuroleptics,
antiemetics, GLP-1 agonists, triptans, ergots, more.

## Try it in the app

- **Cell Bio → Signalling** — `gpcr-camp-pka`, `gpcr-ip3-
  ca`, `pkc-dag-ca`, `camkii` entries cover the major
  downstream branches.
- **Pharm → Receptors** — `adrenergic-beta1`, `adrenergic-
  beta2`, `adrenergic-alpha1`, `muscarinic-m3`, `dopamine-
  d2`, `opioid-mu`, `angiotensin-at1`, `glp1-receptor`,
  `histamine-h1`, `cannabinoid-cb1` are all GPCRs.

Next: **Receptor tyrosine kinases**.
