# Bioorthogonal chemistry — labelling biology in real time

**Bioorthogonal reactions** are chemical transformations
that proceed selectively in living systems without
interfering with native biochemistry. The 2022 Nobel Prize
(Bertozzi + Sharpless + Meldal) recognised the field
alongside click chemistry.

## Design criteria

A reaction is bioorthogonal if:

- Both partners are **absent from biology** (no native
  azides, alkynes, tetrazines, …).
- Reactants are **non-toxic** to cells.
- Reaction is **fast** (k > 1 M⁻¹s⁻¹) at biological
  concentrations (μM-nM).
- Conditions: **water + neutral pH + 37 °C + ambient O₂**.

## The toolbox

### 1. CuAAC click chemistry

Azide + terminal alkyne + Cu(I) → 1,4-triazole. Sharpless +
Meldal (2002). Workhorse for *in vitro* labelling +
bioconjugation, but Cu is cytotoxic — limits use *in vivo*.

### 2. SPAAC — Strain-promoted click

Azide + cyclooctyne (DBCO, BCN, DIBO) → triazole, **no
copper**. Bertozzi + Agard (2004). Driven by the strain
energy of the cyclooctyne (~ 18 kcal/mol). Used in mice +
zebrafish embryos — first true *in vivo* bioconjugation.

### 3. Tetrazine ligation

Trans-cyclooctene (TCO) + tetrazine → dihydropyridazine via
an inverse-electron-demand Diels-Alder reaction. Fox + Hilderbrand +
Weissleder. **k ~ 10⁵ M⁻¹s⁻¹** — fastest known bioorthogonal
ligation, 1000-10000 × faster than SPAAC.

Now standard for PET imaging + antibody-drug conjugates +
cell-surface labelling.

### 4. Staudinger ligation

Azide + phosphine + ester → amide bond + phosphine oxide.
Bertozzi (2000). Slower (~ 10⁻³ M⁻¹s⁻¹) but historic — first
truly bioorthogonal reaction demonstrated in living cells.

### 5. Photoclick

Tetrazole + alkene + UV → pyrazoline. Lin (2008). Spatial +
temporal control via light — turn the reaction on with a
laser focused at one part of a cell.

### 6. Other workhorses

- **Oxime / hydrazone formation** — aldehyde + aminooxy /
  hydrazide → C=N. Native amino + carbonyl partners present
  in biology so weakly bioorthogonal but useful.
- **Boronic acid + diol** — reversible ester, sugar
  detection.
- **Sulfo-click** + **thiol-ene + thiol-yne** — radical
  click chemistry under photoinitiation.

## Applications

### Metabolic labelling

Feed cells an **azido-sugar** (Ac₄ManNAz) → the cell's own
sialic-acid biosynthesis incorporates the azide into surface
glycans → click in a fluorophore for imaging. Bertozzi's
foundational demonstration (2004).

Modern variants: azido-amino-acid for proteins (Tirrell),
alkyne-fatty-acid for lipidomics.

### Antibody-drug conjugates (ADCs)

Trastuzumab (Herceptin) + tetrazine-linker-payload + TCO-
tagged-cytotoxin → site-specific ADC with controlled drug-
antibody ratio. Adcetris + Kadcyla + Polivy use related
bioconjugation chemistry.

### Pretargeted PET imaging

Inject TCO-modified antibody → wait 2-3 days for it to find
the tumour + clear from blood → inject ¹⁸F- or ⁶⁴Cu-tagged
tetrazine → imaging signal at the tumour, fast clearance of
unbound radioligand. Higher resolution + lower dose than
direct ¹⁸F-antibody.

### Activity-based protein profiling (ABPP)

Activity-based probes contain a reactive warhead + an
azide / alkyne handle. Apply to a cell lysate → warhead
covalently tags only active enzymes → click in a
fluorophore / biotin → detect by gel / pull down. Cravatt's
toolbox — > 1000 papers since 2000.

## Designing a bioorthogonal handle

Practical guidelines:

- **Small** (< 200 Da) so it doesn't perturb the host
  molecule's behaviour.
- **Stable** in cell media for hours-days (no hydrolysis,
  no thiol attack from glutathione).
- **Compatible** with the biosynthetic machinery (azido-
  sugars must be tolerated by GalNAc-T glycosyltransferases).
- **Orthogonal** to your other handles if multiplexing —
  e.g., azide + tetrazine in the same cell needs no cross-
  reactivity.

## Try it in the app

- **Reactions tab** → load *CuAAC click chemistry* — see the
  catalytic cycle.
- **Glossary** → search *Click chemistry*, *Bioorthogonal*,
  *CuAAC*, *Strain-promoted azide-alkyne cycloaddition
  (SPAAC)*, *Tetrazine ligation*.
- **Tools → Medicinal chemistry → SAR series…** → look at
  ADC payload SAR (vedotin, mertansine).

Next: **Macrocycle synthesis — escaping flatland**.
