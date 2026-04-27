# Second messengers — cAMP, IP3, Ca²⁺

When an extracellular signal binds a cell-surface receptor,
how does the message get from the membrane to the nucleus?
Through **second messengers** — small intracellular
molecules whose concentration spikes in response to receptor
activation, then triggers downstream cascades.

The "first messenger" is the extracellular signal; the
"second messenger" is the intracellular relay.

## cAMP — the original second messenger

Earl Sutherland discovered cyclic AMP in the 1950s while
working on hormone-stimulated glycogenolysis. He won the
1971 Nobel for showing that adrenaline + glucagon don't
enter cells — they trigger membrane-bound adenylate cyclase
to make cAMP, which then activates downstream kinases.

The pathway:

1. Hormone binds Gαs-coupled GPCR.
2. Gαs activates adenylate cyclase.
3. Adenylate cyclase converts ATP → cAMP (rate ~ 1000
   cAMP per second per active enzyme).
4. cAMP binds the regulatory subunits of PKA, releasing
   the catalytic subunits.
5. Active PKA phosphorylates serines + threonines on
   target proteins (CREB, glycogen-synthase kinase 3,
   phosphorylase kinase, etc.).

Termination: phosphodiesterases (PDE1-11) hydrolyse cAMP
to AMP. Caffeine is a non-selective PDE inhibitor —
prolonging cAMP signals → bronchodilation + CNS
stimulation.

PDE5 inhibitors (sildenafil, tadalafil) selectively
prolong cGMP in penile smooth muscle — the molecular basis
of erectile-dysfunction therapy.

## IP3 + DAG — the lipid messengers

Second-messenger logic from the 1980s (Berridge + Nishizuka,
joint Lasker 1989) added a parallel pathway from Gαq-
coupled receptors:

1. Hormone binds Gαq-coupled GPCR.
2. Gαq activates phospholipase C-β (PLCβ).
3. PLCβ hydrolyses membrane PIP2 (phosphatidylinositol
   4,5-bisphosphate) into two products:
   - **IP3** (inositol-1,4,5-trisphosphate) — soluble,
     diffuses to ER, opens IP3-receptor Ca²⁺ channels.
   - **DAG** (diacylglycerol) — stays in the membrane,
     recruits + activates PKC.

The same enzyme cuts one substrate into two simultaneously-
generated second messengers. Beautiful chemistry.

## Ca²⁺ — the universal second messenger

Cells maintain a 10 000-fold gradient of free Ca²⁺ across
the plasma membrane: ~ 1.2 mM outside, ~ 100 nM inside at
rest. This gradient + the gradient between cytosol and ER/
mitochondria are the substrate for Ca²⁺ signalling.

On stimulation, cytosolic [Ca²⁺] rises 10-100×. Sources:

- **ER release** via IP3 receptors (Gαq pathway above) or
  ryanodine receptors (cardiac + skeletal muscle).
- **Plasma-membrane influx** via voltage-gated channels
  (Cav1.x in cardiac/smooth muscle), store-operated
  channels (Orai-STIM), or ligand-gated (NMDA in neurons).

Downstream sensors:

- **Calmodulin** — small Ca²⁺-binding protein; binds 4
  Ca²⁺ + activates CaMKII, calcineurin, MLCK, etc.
- **Troponin C** — striated-muscle Ca²⁺ sensor that drives
  contraction.
- **Synaptotagmin** — vesicle-fusion Ca²⁺ sensor that
  triggers neurotransmitter release.

Termination: SERCA (ER Ca²⁺-ATPase) + plasma-membrane
Ca²⁺-ATPase + Na+/Ca²⁺ exchangers pump Ca²⁺ back to its
storage compartments.

## Why have so many second messengers?

Different second messengers + different sensors give cells
the resolution to respond differently to different signals:

- A neuron firing an action potential generates a
  millisecond Ca²⁺ spike at the active zone for vesicle
  release.
- A hepatocyte responding to glucagon sustains a minutes-
  long cAMP elevation for glycogenolysis.
- A T cell receiving a TCR signal builds a long-lasting
  Ca²⁺ oscillation that drives nuclear NFAT translocation
  + gene expression for hours.

Same chemistry; different temporal + spatial profiles
encode different information.

## Try it in the app

- **Window → Cell Biology Studio → Signalling tab** — find
  `gpcr-camp-pka`, `gpcr-ip3-ca`, `pkc-dag-ca`, `camkii`
  for the full mechanism.
- **Window → Biochem Studio → Cofactors tab** — `cAMP`
  entry covers the chemistry of the second messenger.

Next: **MAPK / ERK — the prototype kinase cascade**.
