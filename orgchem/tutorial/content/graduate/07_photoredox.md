# Photoredox catalysis & visible-light chemistry

The 2010s overhaul of organic synthesis: photons replace chemical
oxidants and reductants, opening single-electron-transfer (SET)
disconnections that were impossible by classical two-electron polar
mechanisms.  Photoredox catalysis now appears in **>10 % of all
modern total-synthesis publications**, with three Nobel-level
research programmes — MacMillan (Princeton), Yoon (Wisconsin), and
Doyle (UCLA) — driving most of the methodology development.

## Why visible light?

UV light (< 400 nm) is energetic enough to homolyse C–C and C–H
bonds directly but lacks selectivity — it ionises everything in
its path, photodegrades substrates, and demands quartz reactors.
**Visible light** (400 – 700 nm) is too low-energy to break σ
bonds directly, so it requires a **photocatalyst** that absorbs the
photon, climbs to a long-lived excited state, then transfers a
single electron to or from the substrate.

The key visible-light advantages:
- **Functional-group tolerance** — no random photochemistry on
  innocent π-systems.
- **Mild conditions** — usually room-temperature, ambient atmosphere
  (often O₂-tolerant).
- **Abundant, cheap light sources** — household blue LEDs work for
  most photocatalysts.

## The two canonical photocatalyst families

1. **Ru / Ir polypyridyl complexes** — Ru(bpy)₃²⁺ is the
   archetype.  Long-lived excited state (~ 1 µs), reversible
   single-electron transfer, well-characterised redox potentials
   (E°(Ru³⁺/Ru²⁺*) ≈ –0.81 V; E°(Ru²⁺*/Ru⁺) ≈ +0.77 V vs SCE
   make Ru(bpy)₃²⁺ a moderate single-electron oxidant + reductant
   from the same excited state).  Ir(ppy)₃ + Ir(dF(CF₃)ppy)₂(dtbbpy)
   variants tune the redox window across ~ 1.5 V.
2. **Organic dyes** — much cheaper.  Eosin Y, fluorescein,
   acridinium salts (Mes-Acr⁺ from Fukuzumi & Nicewicz), 4CzIPN
   (the bright-yellow donor-acceptor MacMillan-favourite).  Acridinium
   salts excel as strong single-electron oxidants (E*ᵣₑd up to +2.0
   V).

## The two cycles: oxidative vs reductive quenching

**Oxidative quenching cycle** (photocatalyst → reductant in the
excited state):
1. PC + hν → PC* (singlet → triplet via ISC).
2. PC* + e-acceptor → PC⁺• + acceptor⁻• (PC* gives up an electron).
3. PC⁺• + sacrificial reductant → PC + reductant⁺• (closes the
   cycle).

**Reductive quenching cycle** (photocatalyst → oxidant in the
excited state):
1. PC + hν → PC*.
2. PC* + e-donor → PC⁻• + donor⁺• (PC* steals an electron).
3. PC⁻• + sacrificial oxidant → PC + oxidant⁻• (closes the cycle).

Picking which cycle a substrate enters is just a matter of comparing
its redox potential to the photocatalyst's excited-state E°.

## Key reactions

- **MacMillan decarboxylative coupling** — α-amino acid + Ni / Ir
  dual catalysis → α-arylated amine + CO₂.  The amino-acid carboxylate
  is the single-electron donor; the Ir photocatalyst removes the
  electron, decarboxylation generates an α-amino radical, the Ni
  cycle forms the C–C bond with an aryl halide.  Replaces multi-step
  protecting-group dances with one operation.
- **C–H fluorination** (Doyle, Sanford, MacMillan) — Selectfluor +
  photocatalyst transfers fluorine atoms to specific C–H bonds via
  a radical chain.
- **[2+2] photocycloadditions** (Yoon) — Ru-photocatalysed [2+2]
  of enones gives cyclobutanes with controlled stereochemistry —
  geometrically inaccessible by classical Diels-Alder thinking.
- **Minisci reaction** (radical addition to heteroaromatics) — modernised
  with photocatalysts to generate the radical from a carboxylic
  acid + Ag(II) or directly from the C–H bond.
- **HAT photocatalysis** — quinuclidine + photoredox lets the
  catalyst abstract a hydrogen atom from an unfunctionalised C–H
  bond; the carbon radical is then funnelled into C–N, C–C, or
  C–O bond formation.

## How it connects to the rest of organic chemistry

Photoredox is a **third disconnection axis** alongside polar (two-
electron) and pericyclic chemistry.  Substrates that can't be
combined by classical Wittig / Suzuki / aldol thinking — for example
two C(sp³) fragments — often surrender to photoredox + Ni dual
catalysis (the metallaphotoredox approach pioneered by Doyle +
MacMillan + Molander).

The same photocatalyst can drive utterly different transformations
depending on the substrates present.  Mechanism-first thinking
**stops being optional** in the photoredox era: the organic chemist
needs to know SET potentials, triplet lifetimes, and quenching
rate constants alongside pKa and bond dissociation energies.

## Try it in the app

- Open the **Reactions** tab → look at *Diels-Alder* and *Click
  chemistry: CuAAC*.  Both are pericyclic-style [4+2] / [3+2]
  cycloadditions; the Yoon photoredox [2+2] is the visible-light
  cousin that closes a 4-ring with the same conceptual move.
- Open the **Glossary** tab → search for *radical*, *HOMO/LUMO*,
  *kinetic isotope effect*.  Photoredox mechanisms hinge on all
  three.
- Open *Tools → Spectroscopy* → predict UV-Vis absorption for
  Ru(bpy)₃²⁺ to see the MLCT band that drives the catalysis.

## Further reading

- Prier, C. K.; Rankic, D. A.; MacMillan, D. W. C. (2013) "Visible
  light photoredox catalysis with transition metal complexes:
  applications in organic synthesis" *Chem. Rev.* **113**, 5322.
  The textbook + most-cited review of the field.
- Romero, N. A.; Nicewicz, D. A. (2016) "Organic photoredox
  catalysis" *Chem. Rev.* **116**, 10075.  Companion review for
  the metal-free dye photocatalysts.
- Nature *Reviews* Chemistry articles by Doyle, Yoon, and Knowles
  for the modern updates.

Next: there's no formal "next" — Phase 38d's process simulator and
Phase 30's Macromolecules window are both worth a tour.  See you
in the lab.
