# Organometallic Chemistry & Cross-Coupling

If pericyclic reactions are the "third family" (concerted, symmetry-
driven), transition-metal catalysis is the **fourth** — and it's
arguably the one that defines modern synthesis. The 2010 Nobel Prize
(Heck, Negishi, Suzuki) recognised what was by then already the single
most-used strategy for making C-C bonds in the pharmaceutical industry.

Open **Suzuki coupling (bromobenzene + phenylboronic acid)** in the
Reactions tab to follow along. It's seeded with a full reaction SMILES
and a description.

## The core idea: break C-C bond formation into three elementary steps

A bare hot flask usually can't persuade two halves of a molecule to
bond. But a **transition-metal catalyst** (most often Pd, sometimes Ni,
Cu, Rh, Ru, Fe) can shuttle both pieces through its coordination
sphere:

1. **Oxidative addition (OA)**: an Ar-X bond (X = Br, I, OTf, Cl) adds
   across a low-valent metal (Pd⁰), giving Ar-Pd(II)-X.
2. **Transmetalation (TM)**: a nucleophilic coupling partner (boronate,
   zincate, stannate, cuprate, Grignard) hands its organyl group to
   the metal, kicking out X⁻.
3. **Reductive elimination (RE)**: the two organyl groups on Pd(II)
   collapse into a new σ bond, regenerating Pd⁰ and closing the cycle.

    Pd⁰ + Ar-X ──(OA)──► Ar-Pd(II)-X
    Ar-Pd(II)-X + Ar'-[B/Zn/Cu]──(TM)──► Ar-Pd(II)-Ar' + X-[B/Zn/Cu]
    Ar-Pd(II)-Ar' ──(RE)──► Ar-Ar' + Pd⁰

Each step is microscopically reversible; the whole cycle is driven by
the stability of the product Ar-Ar'.

## The big four cross-couplings (same cycle, different TM partner)

| Reaction | Nucleophilic partner | Discovered | Typical catalyst |
|----------|---------------------|------------|------------------|
| **Suzuki-Miyaura** | Ar-B(OH)₂ boronic acid | 1979 (Suzuki) | Pd(PPh₃)₄ / Pd(OAc)₂ + ligand |
| **Negishi** | Ar-ZnX organozinc | 1977 (Negishi) | Pd(PPh₃)₄ / Ni catalyst |
| **Stille** | Ar-SnR₃ organostannane | 1978 (Stille) | Pd(PPh₃)₂Cl₂ |
| **Heck** | H₂C=CH-R alkene (not pre-metallated) | 1972 (Mizoroki / Heck) | Pd(OAc)₂ + base |
| **Sonogashira** | H-C≡C-R terminal alkyne | 1975 | Pd + Cu co-catalyst |
| **Buchwald-Hartwig** | Ar-NH₂ amine (C-N bond) | 1994 | Pd + bulky phosphine |

**Suzuki has won.** The boronic acids are air-stable, non-toxic, and
commercially available by the hundreds. The by-product is boric acid
(essentially harmless). That's why roughly a third of all modern
medicinal-chemistry bond formations are Suzuki couplings.

## The Suzuki catalytic cycle in detail

Open the **Reactions tab** and select Suzuki coupling. The seeded SMILES
is simplified (no ligands / base shown) but the overall transformation
is correct:

    Br-C₆H₅ + (HO)₂B-C₆H₅  →  C₆H₅-C₆H₅ (biphenyl) + B(OH)₃ + NaBr

The full cycle:

1. **OA**: Pd⁰(PPh₃)₄ loses 2 phosphines, binds PhBr; OA gives
   PhPd(II)Br(PPh₃)₂.
2. **Ligand exchange**: PhPd(II)Br → PhPd(II)OH (the NaOH / K₂CO₃
   base swaps Br for OH). Critical — Pd-Br won't transmetalate with
   a boronate; Pd-OH will.
3. **TM**: (HO)₂B-Ph reacts with PhPd(II)OH; the Ph migrates onto Pd
   and B(OH)₃ leaves.
4. **RE**: Ph-Pd(II)-Ph → Ph-Ph + Pd⁰(PPh₃)₂. The regenerated Pd⁰
   starts another cycle.

Turnover numbers of 10⁴–10⁶ are routine — a tiny amount of Pd powers
stoichiometric substrate transformation.

## Ligand choice matters enormously

Ligands on Pd tune **rate**, **selectivity**, and **substrate scope**:

- **Electron-rich bulky phosphines** (tricyclohexylphosphine,
  tri-tert-butylphosphine) accelerate OA on sluggish Ar-Cl substrates
  (otherwise you need Ar-I/Br/OTf).
- **Chelating bidentate** (dppf, Xantphos) enforce cis-geometry at Pd
  for faster RE.
- **N-heterocyclic carbenes** (NHCs like IMes, IPr) are even more
  electron-donating than phosphines; excellent for bulky coupling
  partners.

**Buchwald's dialkylbiaryl phosphines** (SPhos, XPhos, BrettPhos,
RuPhos, …) are the modern workhorses. They solved the Ar-Cl problem
in the late 1990s — since then Ar-Cl is just as viable as Ar-Br in
Suzuki, which is why chlorobenzenes (cheap, commodity) are the
preferred feedstock for industrial couplings.

## Beyond Pd — other metals, other couplings

- **Ni** catalysis: cheaper, more Earth-abundant, can couple Ar-OMe
  (!) or aryl amines (Buchwald-Hartwig analogues). Reactivity is
  closer to radical chemistry at times — single-electron transfers
  common.
- **Cu**: Ullmann (C-N / C-O), older and milder than Buchwald-Hartwig
  but with narrower substrate scope. Now being revisited with ligand
  acceleration (phenanthroline, oxalamide).
- **Fe / Co / Mn**: the "base-metal renaissance" — cross-couplings
  with abundant first-row metals. Still a research frontier.
- **Photoredox dual-catalysis**: merging Ir/Ru photocatalysts with
  Ni or Cu unlocks radical couplings that classical two-electron
  cycles can't reach (decarboxylative cross-coupling, C-H
  functionalisation).

## Key mechanisms that aren't cross-coupling but share the vocabulary

- **Olefin metathesis** (Grubbs, Schrock catalysts): Ru/Mo carbenes
  swap partners at a C=C bond. 2005 Nobel Prize. No OA / RE — it's a
  [2+2] between the metal carbene and the alkene, followed by retro-
  [2+2].
- **Hydrogenation** (Wilkinson's Rh, Noyori's Ru-BINAP): OA of H₂
  across the metal, then syn-addition across a C=C. The **Noyori
  asymmetric hydrogenation** turns prochiral ketones / olefins into
  single enantiomers with 99%+ ee.
- **Hydroformylation** (cobalt / rhodium): alkene + CO + H₂ →
  aldehyde. The oldest industrial organometallic process (BASF 1938);
  >10 Mt/year.

## The 18-electron rule

Most stable transition-metal complexes have **18 valence electrons**
(the total count at the metal centre). Count:

- Each metal d-electron: 1 each (Pd⁰: 10).
- Each 2-electron donor ligand (PR₃, PPh₃, CO): 2.
- Each X-type ligand (halide, alkyl, aryl): 1 if neutral convention,
  2 if ionic convention — pick one and stay consistent.
- π-ligand counts: η²-alkene 2, η⁴-diene 4, η⁵-Cp 5, η⁶-arene 6.

Intermediate Pd species often break the rule — 14- / 16-electron Pd
complexes are kinetically important because the vacant coordination
site is where substrates bind. "Coordinatively unsaturated" = "ready
to react".

## Practice

1. Select **Suzuki coupling** in the Reactions tab. Try clicking
   *Export reaction…* to save an SVG. The scheme uses the new Phase 6f
   DB-canonical fragment renderer so benzene, boronic acid, biphenyl,
   and boric acid all have the same layouts they'd have in the
   Molecule Workspace.
2. Ask the tutor: "Walk me through the Suzuki catalytic cycle step
   by step" — it should describe OA, TM, RE against the Pd⁰/Pd(II)
   oxidation states.
3. Look up **Bromobenzene** and **Biphenyl** in the Molecule browser.
   Note the molecular weight change and what atoms survived the
   coupling.
4. Ask the tutor to compare the Negishi and Suzuki mechanisms. The
   cycle is the same; only the transmetalation partner differs.

## Further reading

- Jana, Pathak, Sigman (2011) "Advances in transition metal
  (Pd,Ni,Fe)-catalyzed cross-coupling reactions using alkyl-
  organometallics as reaction partners" *Chem. Rev.* 111, 1417.
- Noyori (2001) Nobel Lecture, *Angew. Chem. Int. Ed.* 41, 2008.
- Hartwig, *Organotransition Metal Chemistry: From Bonding to
  Catalysis* (2010) — the standard graduate textbook.

Next: **Retrosynthesis** — how to use all this reactivity knowledge to
design a synthesis from scratch.
