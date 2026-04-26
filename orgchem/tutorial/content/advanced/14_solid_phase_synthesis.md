# Solid-phase synthesis — building peptides + nucleic acids on resin

In **solid-phase synthesis (SPS)** the growing molecule is
covalently anchored to an insoluble polymer bead.
By-products + excess reagents wash away with each filtration
— only the desired species stays on the bead. Merrifield won
the 1984 Nobel Prize for inventing SPS.

## Why solids?

Classical solution-phase peptide / oligonucleotide synthesis
loses 1-5 % yield per step; over 10-20 couplings the overall
yield collapses (0.95²⁰ = 36 %; 0.99²⁰ = 82 %).

SPS achieves > 99.5 % per step because:

- **Excess reagents** — drive every step to completion (e.g.
  4 eq of activated amino acid).
- **Filtration washes away by-products** — no
  chromatography between steps.
- **No solubility issues** — the chain stays on the bead
  even when the side chains would otherwise precipitate.
- **Automation** — robotic synthesisers cycle through
  hundreds of monomers a day.

## Peptide SPPS — the workhorse

Two parallel chemistries dominate:

### Fmoc / tBu (modern standard)

- **N-protection**: Fmoc (9-fluorenylmethyloxycarbonyl) —
  base-labile (20 % piperidine/DMF removes in 5 min).
- **Side-chain protection**: tBu, Boc, Trt, Pbf — all
  acid-labile.
- **Cleavage**: TFA cocktail (95 % TFA / 2.5 % H₂O / 2.5 %
  TIPS) removes side-chain PGs + cleaves chain from
  Wang/Rink resin in one pot.

### Boc / Bzl (Merrifield's original)

- **N-Boc**: TFA-labile.
- **Side-chain Bzl/cHex**: HF-labile.
- Final HF cleavage — corrosive + hazardous (needs Teflon
  apparatus). Largely retired except for difficult sequences.

### Coupling reagents

The activated species is a carbodiimide-, uronium-, or
phosphonium-derived ester:

- **HBTU, HATU** — uronium salts; HATU's HOAt buffer
  suppresses racemisation.
- **PyBOP, PyBrOP** — phosphonium; for hindered residues.
- **DIC + HOBt / Oxyma** — carbodiimide + nucleophilic
  catalyst; cheaper than HATU.
- **T3P** — propanephosphonic anhydride; mild, scalable.

### Resins + linkers

- **Wang resin** — for Fmoc, gives free C-terminal acid.
- **Rink amide** — gives C-terminal amide (most common in
  pharma).
- **2-Chlorotrityl** — mild cleavage with HFIP, peptide
  retains side-chain protection (for fragment condensation).
- **Sasrin** — even milder, photolabile alternatives exist.

## Phosphoramidite oligonucleotide synthesis

Caruthers (1981) — DNA synthesis on controlled-pore glass:

1. **Detrytilation** — TCA removes 5'-DMT.
2. **Coupling** — phosphoramidite + tetrazole activator (~
   30 sec, > 99.5 %).
3. **Capping** — Ac₂O / N-methylimidazole acetylates any
   unreacted 5'-OH (prevents deletion mutations).
4. **Oxidation** — I₂ / pyridine / H₂O converts P(III) →
   P(V).

Repeat for each nucleotide; final NH₃ cleavage removes
protecting groups + frees the strand.

Modern instruments synthesise 100-mer oligos overnight.
**Twist Bioscience** + **IDT** + **Genscript** dominate
commercial DNA-synthesis services; 96-well-plate scales
deliver to anywhere in the world in days.

## Solid-phase peptide → oligonucleotide → small molecule

Beyond peptides + DNA:

- **Oligosaccharides** (Seeberger) — glycosylation on
  resin; harder than peptides because no universal
  protecting-group strategy.
- **Combinatorial small-molecule libraries** — split-and-
  pool synthesis on resin (Furka, Lam, 1991) generates
  thousands of compounds for drug screening.
- **DNA-encoded libraries** (DEL) — covers in lesson 15.

## Modern variants

- **Microwave-assisted SPPS** — heated couplings shave
  cycle times 30-60 sec, useful for difficult sequences.
- **Continuous flow SPPS** (Pentelute) — chain-elongation
  in a packed column → 10 sec per residue, 4-5 hour
  insulin synthesis.
- **Ligation strategies** — native chemical ligation (Kent),
  expressed protein ligation (Muir) link multiple SPS-
  synthesised fragments into 100+ residue proteins.

## Try it in the app

- **Synthesis tab** → load *Met-enkephalin via Fmoc SPPS
  5-step* — see the step-by-step SPS scheme rendered.
- **Tools → Lab reagents…** → look up Fmoc-AA building
  blocks, HATU, piperidine, TFA-cleavage cocktail entries.
- **Glossary** → search *SPPS*, *Fmoc protection*, *Boc
  protection*, *HATU*, *Phosphoramidite*.

Next: **Combinatorial chemistry + DNA-encoded libraries**.
