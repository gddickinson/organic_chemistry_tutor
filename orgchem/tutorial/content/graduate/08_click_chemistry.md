# Click chemistry & bioconjugation

The 2022 Nobel Prize in Chemistry went to **Carolyn Bertozzi**,
**Morten Meldal**, and **K. Barry Sharpless** for **click
chemistry** + bioorthogonal chemistry — the philosophy that
chemistry should be **modular, fast, selective, and high-yielding
in any solvent (water included)** so chemical bonds can be made
inside living organisms without disturbing the rest of biology.

Sharpless coined the *click* term in 2001 with five criteria:

1. **Modular**: works on a wide range of substrates
2. **Wide scope**: many partners participate
3. **High yield** (> 80 %)
4. **Stereospecific** (or stereoinconsequential)
5. **Simple conditions** + insensitive to oxygen / water +
   bypoducts removable without chromatography

A *click* reaction is **bioorthogonal** if it works inside a
living cell — non-toxic, won't react with anything else
in the cellular zoo of nucleophiles + electrophiles.  Bertozzi
established this term + showed how to **track sugars on cell
surfaces in live mice** using bioorthogonal click chemistry.

## The CuAAC: original click

The **copper-catalysed azide-alkyne cycloaddition (CuAAC)** —
discovered independently by Meldal (Carlsberg Laboratories,
2002) and Sharpless (Scripps, 2002) — fuses an azide + a
terminal alkyne into a **1,4-disubstituted 1,2,3-triazole**:

```
R-N₃ + R'-C≡CH  →[Cu(I)]→  R-N(N=N)C(R')=C-H   (1,4-triazole)
```

The Cu(I) catalyst (CuSO₄ + ascorbate, or CuI) lowers the
activation energy of the [3+2] cycloaddition by ~ 20 kcal/mol +
turns it stereospecific (always 1,4 — the uncatalysed Huisgen
reaction gives ~ 1:1 1,4 / 1,5 mixtures).  Run at room
temperature in water; the triazole product is metabolically
stable + a good amide bioisostere.

See the seeded *Click chemistry: CuAAC* entry in the
**Reactions** tab for the full SMARTS + reaction scheme.

## The SPAAC: copper-free for biology

CuAAC's catalyst is **toxic to cells** — Cu(I) generates
reactive oxygen species that kill mammalian cultures.  Bertozzi
+ Bertozzi-school chemists eliminated copper by using **strained
cyclooctynes** as the alkyne partner — the ring strain (~ 18
kcal/mol in cyclooctyne; > 20 kcal/mol in DIBO + BCN) provides
the kinetic boost that copper used to provide:

```
R-N₃ + cyclooctyne  →  triazole-fused cyclooctene
                       (no catalyst, biocompatible)
```

The **strain-promoted azide-alkyne cycloaddition (SPAAC)** runs
at physiological pH + temperature with no metal — directly
inside living cells.  Common cyclooctyne reagents: **DIBO**
(dibenzocyclooctyne), **BCN** (bicyclononyne), **DBCO**
(dibenzo-fused with the [3.2.1] core).

## Tetrazine ligation: the fastest click

The **inverse-electron-demand Diels-Alder (iEDDA)** between a
**tetrazine** and a strained dienophile (TCO — *trans*-
cyclooctene, norbornene, methylcyclopropene) is even faster
than SPAAC — second-order rate constants up to 10⁶ M⁻¹ s⁻¹
(SPAAC peaks around 1 M⁻¹ s⁻¹; CuAAC at the catalysed rate is
~ 10²-10⁴).

```
[1,2,4,5-tetrazine] + TCO  →  dihydropyridazine + N₂
```

The dihydropyridazine product is irreversible + the only
byproduct is N₂ gas.  Used for **PET imaging**: a TCO-tagged
antibody is injected into a patient hours before injection of
a ¹⁸F-labelled tetrazine; the tetrazine clicks onto the
antibody at the tumour site + the patient is imaged within
minutes.

## What makes it bioorthogonal

For an in-cell reaction to qualify as bioorthogonal:

- Both partners must be **biostable** for hours (no
  hydrolysis, no nucleophilic attack by Cys / Lys / His).
- Both partners must be **biologically silent** (no enzymes
  recognise them, no metabolic pathways modify them).
- The reaction must be **non-toxic** at relevant concentrations.
- The reaction must be **selective** — it must not react with
  the millions of other functional groups in the cell.

The azide is the gold-standard bioorthogonal handle: small
(~ 41 g/mol), non-toxic, absent from natural biology, kinetically
inert to almost everything except phosphines (Staudinger
ligation) and alkynes (CuAAC / SPAAC).  Tetrazines are
larger but pair with TCO to give the fastest known
bioorthogonal reaction.

## Applications

- **Drug discovery**: build large compound libraries by
  clicking azide + alkyne fragments (e.g. fragment-based
  drug design at GlaxoSmithKline + Astellas).
- **Antibody-drug conjugates (ADCs)**: tether a cytotoxic
  payload to an antibody via a click linker — the
  **brentuximab vedotin** ADC for Hodgkin lymphoma uses a
  click-style cleavable linker.
- **PET / SPECT imaging**: pretarget with a TCO-antibody,
  image with a tetrazine-radioligand (Mehta + Rossin et al.).
- **Glycoproteomics**: feed cells with N-azidoacetylgalactosamine
  → cell-surface glycoproteins display azides → click on a
  fluorophore → image the glycome (Bertozzi, 2003).
- **Surface + materials chemistry**: hydrogels formed by
  clicking azide-PEG + alkyne-PEG; biofunctionalised
  surfaces for biosensors.

## How click chemistry connects to the rest of organic chemistry

Click chemistry is a **systematic distillation of pericyclic
+ catalysed cycloaddition methodology** into a "design
philosophy" that prioritises practical use.  The CuAAC + SPAAC
mechanisms ARE classical [3+2] cycloadditions (the Huisgen
reaction); the iEDDA tetrazine ligation IS a Diels-Alder; the
Staudinger ligation IS an aza-ylide acyl transfer.  The
innovation isn't the reactions themselves — it's the
**combinatorial framing** + the **bioorthogonal design
constraint** that makes a small subset of those reactions
universally usable.

The same "click" principles drive **photoredox catalysis**
(see Phase-198 lesson) and **enzymatic ligations** (sortase,
butelase, transglutaminase).

## Try it in the app

- **Reactions tab** → search for *Click chemistry* to load the
  CuAAC entry; inspect the SMARTS + the triazole product.
- **Glossary tab** → search for *cycloaddition* + *pericyclic*
  to see how click chemistry sits in the broader pericyclic
  framework.
- **Tools → Lab techniques → Recrystallisation** to think
  about how a click reaction's "byproducts removable without
  chromatography" criterion plays out in practice.
- **Tools → Spectroscopy** → predict ¹H NMR for 1,4-disubstituted
  1,2,3-triazole — the diagnostic singlet at ~ 7.5 ppm
  confirms a successful click.

## Further reading

- Kolb, H. C.; Finn, M. G.; Sharpless, K. B. (2001) "Click
  chemistry: diverse chemical function from a few good
  reactions" *Angew. Chem. Int. Ed.* **40**, 2004.  The
  founding paper.
- Bertozzi, C. R. (2011) "A decade of bioorthogonal chemistry"
  *Acc. Chem. Res.* **44**, 651.  The bioorthogonal-design
  retrospective.
- Devaraj, N. K. (2018) "The future of bioorthogonal chemistry"
  *ACS Cent. Sci.* **4**, 952.  Modern survey including
  tetrazine ligation.

Next: Phase 38d's process simulator gives you the full lab-
benchtop simulation of running a click reaction (CuAAC fits
neatly into the standard reflux setup).  Or try a multi-step
synthesis in the Synthesis tab that uses a Wittig olefination
to make an alkene partner for a SPAAC click downstream.
