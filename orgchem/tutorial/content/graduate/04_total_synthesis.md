# Case Studies in Total Synthesis

If the earlier lessons were vocabulary — mechanisms, reactions, orbital
symmetry, asymmetric catalysis — **total synthesis** is the sentence
you construct with them. A total synthesis paper picks a non-trivial
natural product, announces a route from commercial starting materials
to the target, and proves the route works with NMR / IR / MS / HRMS /
optical rotation that matches an authentic sample.

The classics of the field — Woodward's strychnine, Woodward-Eschenmoser
Vitamin B₁₂, Nicolaou and Holton's taxol, Kishi's palytoxin — are as
much cultural milestones as they are chemistry. This final graduate
lesson walks through what made each one historically significant, so
you can recognise the moves when you read the literature.

## The ground rules

A total synthesis demonstrates:

1. **Route design**. Retrosynthetic strategy; choice of disconnections;
   which bonds form under which conditions.
2. **Method application**. How every named reaction, stereo-controller,
   and protecting-group manoeuvre actually behaves on complex substrates.
3. **Spectral confirmation**. Every intermediate characterised; the
   final product's spectra **must** match the natural material.

The goal isn't always the grams — some targets (strychnine, taxol) were
first synthesised at sub-milligram scale for **proof of concept**, with
industrial-scale routes developed only later or never at all.

## Case study 1: Strychnine (Woodward, 1954)

Strychnine is a 24-atom indole alkaloid with 6 stereocentres and 7
rings, including a 3-heteroatom bridged bicycle that terrified 1950s
organic chemists. Woodward's 1954 synthesis is widely regarded as the
moment total synthesis became a "proper" scientific field.

Key features:

- **28 steps** from 2-veratrylindole. Final yield < 0.0001 %.
- Key C-C bond-forming: a **Fischer indole synthesis** to install the
  indoline core; a **Mannich cyclisation** to close the tetracyclic
  framework; an **aldol-type** annulation for the last ring.
- Stereocontrol: Woodward relied on **substrate control** — every
  stereocentre came from the geometry of the previous one, set by
  thermodynamic preference. No chiral catalysts existed yet.

Why it mattered: proved that *any* natural product, no matter how
ornate, was in principle synthesisable. Retrosynthesis as a formal
discipline (Corey's 1960s revolution) grew out of post-Woodward
analysis of *what made his route work*.

**In the app**: strychnine is too complex for a seeded pathway (we'd
need ~28 steps), but ask the tutor: *"Sketch the retrosynthetic plan
for strychnine at the top-two disconnections level."* It should
propose (a) disconnection of the indolic C−C bond across the Mannich
junction; (b) disconnection of the E-ring to unmask the Fischer indole
partners.

## Case study 2: Vitamin B₁₂ (Woodward + Eschenmoser, 1973)

Corrin-ring natural product with a cobalt centre, 9 stereocentres, 66
atoms. A **bi-group** 11-year project between Harvard (Woodward) and
ETH (Eschenmoser) involving **100+ graduate students / postdocs**.

Key features:

- **92 steps total**, spread across two convergent branches (A/B
  and C/D rings) that joined at a pyrrolenine intermediate.
- **Landmark methodology**: the synthesis demanded new methods that
  didn't exist in 1960. Eschenmoser developed sulfide-contraction
  methodology *specifically for this project* to forge the
  challenging C-C bonds between pyrrole rings.
- **Orbital-symmetry insight**: the thermal ring closure of a
  hexatriene-like intermediate was **disrotatory** (6π electrocyclic
  — see WH rules lesson). Woodward and Hoffmann formalised the orbital-
  symmetry rules *in response to problems they encountered on this
  project*. The 1965 Woodward-Hoffmann rules were literally born
  out of B₁₂ synthesis.

Why it mattered: drove the creation of the WH rules themselves and
demonstrated that convergent, multi-researcher total synthesis was
feasible at industrial-lab scale.

## Case study 3: Taxol (Nicolaou 1994; Holton 1994)

Anti-cancer natural product; 11-step linear chain from the baccatin
core → 4 stereocentres in the side chain + 11 in the ring system.
Two complete syntheses appeared within days of each other in 1994
(Nicolaou's Scripps group, Holton's Florida State).

Key features (Nicolaou route):

- **Convergent assembly**: A-ring (Diels-Alder on a dienone),
  C-ring (McMurry coupling to close the 8-membered ring), tied
  together via a **Shapiro reaction** + nucleophilic addition.
- **Stereocontrol**: substrate-controlled for most centres (reading
  the steric face of each intermediate); one asymmetric
  dihydroxylation (Sharpless AD-mix-β) for the side chain.
- **Protecting-group choreography**: at peak, 4 orthogonal protections
  (TBS, TES, Bz, Troc) on one intermediate. Every late-stage step
  needed a specific group removed.
- **38 total steps**; sub-milligram final product in academic hands.

Why it mattered: first synthesis of a bona-fide block-buster
anticancer drug on paper; enabled production of **analogs** that
would never have been accessible from natural sourcing.

## Case study 4: Palytoxin (Kishi, 1989–94)

129 carbons, 64 stereocentres, 8 rings, full molecular weight 2681
g/mol. The most complex non-polymeric natural product ever total-
synthesised.

Key features:

- **Convergent in 8 fragments** that joined in the last ~6 steps.
  The convergent strategy alone was the breakthrough — linear would
  have been hopeless (64 steps × 90% yield each ≈ 0.1% overall).
- Kishi's **Ni / Cr reaction** (NHK coupling) was invented for this
  project and is now a workhorse for complex-molecule macrocyclisation.
- Every one of the 64 stereocentres was set by a **specific reaction**
  with stereospecific or highly selective precedent — no guessing,
  no substrate-control luck.

Why it mattered: proved that synthesis of arbitrarily complex natural
products was **routine if you had enough strategy**, and pushed the
envelope on how convergent synthesis scales.

## Case study 5: Erythromycin (Woodward, 1981)

14-membered macrolactone antibiotic. Important for demonstrating
**reiterative asymmetric aldol** using chiral auxiliaries to set 8
contiguous stereocentres.

Key features:

- **Evans oxazolidinone aldols** — the asymmetric method that Evans
  formalised in 1981 was on full display here. Each aldol set 2
  stereocentres; 4 consecutive aldols gave 8 centres.
- Key macrocyclisation: **Yamaguchi lactonisation** (a protocol
  developed for exactly this sort of challenging macrolactone
  closure).

Why it mattered: proved that systematic, iterative asymmetric catalysis
could reliably generate long-chain polyketide natural products. The
method has since been used on ~every macrolide antibiotic.

## Shared strategic themes

Across all five:

1. **Convergence beats linearity.** Every synthesis of > 20 steps is
   convergent. Palytoxin at 8 fragments is extreme; taxol at 3 branches
   is typical.
2. **The right disconnection is often the "obvious" one that nobody
   tried.** Taxol's A/B/C split looks obvious in hindsight — it
   organises along ring boundaries.
3. **New methods get invented during total synthesis.** WH rules
   from B₁₂, NHK coupling from palytoxin, sulfide contraction from
   B₁₂, Yamaguchi from erythromycin. The project drives the tool.
4. **Protecting-group strategy is half the battle.** With 15+ polar
   functionalities sitting at once on a complex intermediate,
   orthogonal masking (TBS / TES / Bz / Cbz / acetonide / Boc / Fmoc /
   MOM) is the hidden engine of every route.
5. **Stereocontrol is either *catalysed* or *substrate-controlled*.**
   Before 2000 most centres were substrate-controlled (relying on the
   last centre set to bias the next one). Post-2000, asymmetric
   catalysis (Noyori, Sharpless, List, MacMillan) sets centres with
   external chiral catalysts — more general, usually higher ee.

## Practice

1. In the Molecule Workspace load **Morphine** (seeded) and ask the
   tutor: *"Sketch a modern retrosynthesis in 3–4 disconnections."*
   Morphine was the first natural-product total synthesis (Gates
   1952, 29 steps); modern routes land in 10–12.
2. Ask for *"Three reasons why the Woodward Vitamin B₁₂ synthesis is
   considered a cornerstone of 20th-century organic chemistry"*.
   Expected: (a) scale and convergence, (b) birth of the WH rules,
   (c) proof that unthinkably complex targets are reachable with
   strategy and personnel.
3. Explore **Penicillin G** and **Lovastatin** (both in the DB). Both
   have landmark total syntheses — Sheehan's penicillin (1957) and
   the 30-step statin routes (Hirama 1982) are each worth a weekend
   of reading.

## Further reading

- Nicolaou, K. C. & Sorensen, E. J. *Classics in Total Synthesis I–III*
  (1996–2011). Essentially canonical.
- Hudlicky, T. & Reed, J. W. *The Way of Synthesis* (2007). Shorter;
  good for the logic of choices.
- Seeman, J. I. "The Mallory-Weiss syntheses of the Paciolo
  molecules" — *actually* Seeman, J. I. (2020) "The woodward‐hoffmann
  rules: chemistry's ultimate reductio ad absurdum?" *Angew. Chem.
  Int. Ed.* 59, 12898. Historical context for B₁₂ → WH rules.
- *Journal of the American Chemical Society* — the actual papers:
  Woodward et al. 1954 (strychnine), Woodward-Eschenmoser 1973
  (B₁₂), Nicolaou 1994 (taxol), Suh-Kishi 1989–94 (palytoxin),
  Woodward 1981 (erythromycin). Read them — **as a graduate student,
  this is the canon**.

---

## Closing note

You've reached the end of the curriculum in this project — 18 lessons
across 4 tiers, from "what is a covalent bond" through "how do you
plan a 64-stereocentre total synthesis?". The natural next step is to
pick a research-level topic and contribute it upstream as a new
lesson. The tutor panel, the reaction / mechanism / pathway database,
and the headless rendering pipeline are all designed so new content is
accretive — a future you (or contributor) can add lessons at any tier
without touching the rest.

Thanks for reading. Now go make something.
