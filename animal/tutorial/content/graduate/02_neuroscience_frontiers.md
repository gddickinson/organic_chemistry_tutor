# Neuroscience frontiers

The 2010s + 2020s have witnessed a transformation
of neuroscience: connectomes at unprecedented
resolution, optogenetic + chemogenetic perturbation
of defined cell types, brain organoids modelling
cortical development, brain-computer interfaces
restoring function + decoding speech, and the
emerging dialogue between AI + the brain.

## Connectomics

Mapping the complete wiring diagram of nervous
systems — the "connectome" — has been a
multi-decade goal.

### Achievements

- **C. elegans** (302 neurons) — Sydney Brenner +
  John White's 1986 connectome; updated +
  re-annotated 2019.  The only ANIMAL with a
  complete connectome at synaptic resolution
  for almost 40 years.
- **Drosophila larva** (3 000 neurons) — Cardona +
  Schneider-Mizell 2023 — first complete insect
  larval connectome.
- **Adult Drosophila brain hemibrain** (25 K neurons,
  20 M synapses) — Janelia FlyEM 2020.
- **Adult Drosophila full brain** (130 K neurons,
  > 50 M synapses) — Janelia + Princeton + others
  2024 milestone.
- **Mouse cortex EM** — multiple projects pursuing
  cortical column reconstruction (Allen Institute,
  IARPA MICrONS, Janelia).  Cubic-mm scale
  reconstructions completed 2021-2023.
- **Human cortex** — H01 sample (1 mm³, ~ 50 K
  neurons, ~ 130 M synapses) — Lichtman +
  Connectomics group at Google + Harvard 2021.

Methods: serial-section EM (TEM, SEM, FIB-SEM) +
ML-driven segmentation + manual proofreading.
Generates petabyte-scale image volumes;
reconstruction is the bottleneck.

### What connectomes reveal

- Cell types + their detailed morphology.
- Connectivity patterns + circuit motifs.
- Comparative analysis across species + individuals.
- Substrate for biophysical + ML circuit modelling.

Limitations:
- Static snapshot; no functional recordings on the
  same cells.
- Dead tissue; no chemical neurotransmitter
  identity (though some cell-type inferences
  possible).
- Whole-mammal brains still beyond reach (rodent
  whole-brain connectome pursued 2030s+).

## Live functional imaging

### Two-photon calcium imaging

GCaMP family genetically encoded calcium indicators
allow direct readout of neuronal activity in
living mice + flies + zebrafish + worms +
non-human primates.

- ~ 1 000-100 000 neurons simultaneously imaged in
  cortex.
- Volumetric / mesoscale + multi-region recording.
- Behavioural correlation possible.

### Voltage indicators

ASAP3, JEDI-2P, Voltron — direct membrane voltage
imaging at action-potential resolution.  Less
mature than calcium imaging but rapidly
improving.

### Multi-electrode arrays + Neuropixels

Silicon-probe technology recording 1 000+ neurons
simultaneously across multiple brain regions in
freely-behaving animals.  Allen Institute Brain
Observatory open data + Neuropixels 2.0 enabling
chronic recording.

## Optogenetics + chemogenetics

### Optogenetics

Genetically targeted light-activated ion channels
(channelrhodopsin variants — ChR2, ChrimsonR,
Chronos; halorhodopsins for inhibition) allow
sub-millisecond control of specific neurons in
living animals.

Karl Deisseroth + Ed Boyden 2005 + subsequent
Brain Prize 2013, Lasker 2021.

Applications:
- **Causal circuit dissection** — testing whether a
  cell type is necessary or sufficient for a
  behaviour.
- **All-optical experiments** — combine
  optogenetics + calcium imaging via spectral
  separation.
- **Closed-loop** — record + perturb in real time.

### Chemogenetics

DREADDs (designer receptors exclusively activated by
designer drugs) — engineered GPCRs activated by
otherwise-inert ligands (CNO, deschloroclozapine).
Slower than optogenetics but easier in deep brain
+ longer-term control.

## Brain organoids

3D in-vitro human-cell models.

Methods:
- Human iPSCs differentiated under specific
  morphogen + growth-factor cues → cerebral cortex,
  cerebellar, midbrain, hindbrain, retinal, choroid-
  plexus organoids.
- Madeline Lancaster + Yoshiki Sasai pioneered
  in 2008-2013.

Capabilities:
- Recapitulate early human cortical development
  (~ first 6 months equivalent).
- Layered cortical structure + diverse neuronal
  cell types.
- Spontaneous oscillatory activity emerging.
- Disease modelling — autism, schizophrenia,
  microcephaly, Alzheimer's, ZIKV neurotropism.

Limitations:
- No vascularisation → necrotic cores after
  ~ 60-90 days.
- Limited maturation beyond fetal-equivalent stages.
- Heterogeneity between organoids.
- Ethical considerations as complexity grows.

Recent progress:
- Vascularised + assembloid systems (linking
  cortical + striatal + ventral organoids).
- Implant into rodent brains for
  vascularisation + integration (Stanford
  Pasca lab 2022 — human cortical organoids
  integrate into rat sensory cortex).
- Published intermediate "thinking" responses
  to electrical stimulation (controversial).

## Brain-computer interfaces (BCIs)

Restoring function or expanding capability through
electrode-brain interfaces.

### Clinical milestones

- **BrainGate** — paralysed patients controlling
  cursor, robotic arm, speech via implanted Utah
  arrays since ~ 2004; ongoing trials.
- **Neuralink** — N1 implant; first human implant
  May 2024; multiple-patient trials.
- **Synchron** — endovascular Stentrode; less-
  invasive; multiple US + Australian trial sites.
- **Precision Neuroscience** — surface-array Layer 7
  cortical interface.
- **Blackrock Neurotech** — Utah array vendor +
  clinical-trial sponsor.

### Capabilities (as of 2026)

- Cursor + keyboard + tablet control via thought.
- Robotic arm + prosthetic-limb control.
- Speech decoding from motor cortex (Edward Chang
  lab) — neuroprosthetic communication for
  paralysed patients.
- Direct cortical stimulation for sensory feedback.
- Pre-clinical: closed-loop control for epilepsy +
  Parkinson's + depression (DBS); bidirectional
  interfaces.

### Speech + language decoding

- **Edward Chang lab** — UCSF — deep-learning
  decoding of intended speech from ECoG signals;
  > 100 word/minute speech reconstruction (2023
  *Nature* + 2024 follow-ups).
- **Stanford / NPTL** — speech-decoding from intra-
  cortical electrodes.
- **Meta + Google + others** — non-invasive MEG +
  EEG decoding using deep nets — limited but
  proliferating papers.

## Large language models + brain decoding

Surprising convergence between LLMs + brain
representations:
- Speech-decoding via fMRI + LLM-conditioned
  stimulus reconstruction (Tang + Huth 2023
  *Nature Neuroscience*) — non-invasive
  reconstruction of intended speech meaning.
- Image reconstruction from fMRI + diffusion
  models.
- Word + scene semantic decoding from MEG /
  fMRI.

Implications:
- Privacy + ethical considerations for
  "mind-reading" technology.
- Accelerated communication for paralysed
  patients.
- Insights into representation + processing in
  the brain.

## AI / neuroscience interface

Neural networks + neuroscience inspire each other:
- **CNNs** drew on hierarchical-feature ideas
  from primate visual cortex (Hubel + Wiesel).
- **Transformers** + attention mechanisms inform
  models of working memory + frontal-cortex
  processing.
- **Reinforcement learning** + dopamine + striatal
  function deeply linked (Schultz, Dayan, Sutton).
- **Predictive coding** in cortical processing —
  Friston + Bayesian brain.
- **Hopfield networks + transformer dual nature**
  recently formalised (Dimitri Krotov, Hopfield
  2024 Nobel for foundational work).

NeuroAI as a discipline — using neural-network
models as testable hypotheses about brain
computation.

## Brain Atlases + cell-type taxonomies

- **Allen Brain Atlas** — multi-modal mouse +
  human atlases.
- **BICCN (BRAIN Initiative Cell Census)** —
  > 1 000 mouse cortical cell types defined by
  scRNA-seq + Patch-seq + connectomics.
- **HuBMAP + HCA + EBRAINS** — human atlases.
- **Allen MERFISH + Patch-seq + Visium** integration
  — multi-modal + spatial.

Now > 5 000 distinct mammalian neuronal cell types
catalogued by transcriptomic + morphological +
electrophysiological + connectomic features.

## Sleep + dreaming

- **REM sleep + memory consolidation** —
  hippocampal replay.
- **Slow-wave sleep (SWS) + clearance** —
  glymphatic system clears Aβ + tau (Maiken
  Nedergaard).
- **Sleep + immune + endocrine** dialogue.
- **Sleep across animals** — fish + cnidarians
  show sleep-like states; species-specific
  variation.

## Consciousness + perception

- **Global Workspace Theory (Baars + Dehaene)** vs
  **Integrated Information Theory (IIT, Tononi)**
  vs **Higher-Order Theory** vs **Predictive
  Processing**.
- Neural correlates of consciousness (NCC) —
  prefrontal vs posterior debates.
- Anaesthesia + recovery as a window onto
  consciousness mechanisms.
- Animal consciousness — Cambridge Declaration
  (2012) + welfare implications.

## Disease neurobiology

- **Alzheimer's** — Aβ + tau pathology; lecanemab +
  donanemab (anti-Aβ mAbs) modest clinical effect;
  microglia + neuroinflammation.
- **Parkinson's** — α-syn aggregates; mitochondrial
  + lysosomal pathology; LRRK2 + GBA + SNCA
  genetics.
- **ALS** — TDP-43 + FUS + SOD1 + C9orf72; tofersen
  ASO for SOD1.
- **Huntington's** — CAG-repeat expansion in HTT;
  ASO trials (tominersen failed for efficacy
  reasons).
- **Stroke + neuroinflammation + microglia** —
  active drug-target areas.

## Future directions

- **Whole-mouse-brain connectome** by ~ 2030s.
- **Functional connectomics at scale** —
  combining EM + activity recording.
- **Implantable BCIs** for broad clinical adoption.
- **AI-augmented neural prosthetics**.
- **Brain organoids** approaching adult-equivalent
  maturity + with vascularisation.
- **In-vivo molecular recording** of brain
  activity (CRISPR-based + DNA-tape "memory").
- **Neuroimaging at sub-mm resolution** in living
  humans (high-field 7T+ MRI).
- **Personalised brain medicine** — precision
  diagnostics + treatments.

## Cross-link

For the foundational neuroscience covered in
intermediate tier, see **AB-3.0 intermediate
"Nervous systems + neuroscience essentials"**.

## Try it in the app

- **OrgChem → Macromolecules → Proteins** — fetch
  channelrhodopsin + opsin + GCaMP structures.
- **Window → Pharmacology Studio → Receptors** —
  ligand-gated ion channels + GPCRs targeted in
  neuroscience.

Next: **Modern animal biotech + One Health**.
