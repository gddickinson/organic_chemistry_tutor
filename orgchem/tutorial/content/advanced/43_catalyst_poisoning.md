# Catalyst poisoning + sulfur tolerance

Many transition-metal catalysts get **poisoned** by trace
impurities — sulfur, halides, amines, sometimes oxygen or
water. Understanding poisons + their mitigation is critical
for both robust academic chemistry + scaling.

## What "catalyst poisoning" means

A poison binds the catalyst's active site irreversibly (or
near-irreversibly), removing it from the catalytic cycle.
Symptoms:

- Initial activity drops to zero.
- Substrate sits unconsumed.
- Higher catalyst loading "fixes" temporarily.

## Common poisons

### Sulfur (the worst)

Sulfide, thiol, thioether, sulfoxide bind soft metals (Pt,
Pd, Rh, Ir, Au) extremely strongly:

- **Lindlar catalyst** is intentionally poisoned by Pb +
  quinoline → less reactive but selective for partial
  alkyne reduction.
- **DMS, thiophene, SO₂** in feedstocks → kill many
  catalysts.
- **Cysteine + glutathione** in biological samples →
  destroy Pt anti-cancer drugs.

Sulfur is used **deliberately** as a poison in selective
hydrogenation:

- Lindlar (Pd / CaCO₃ / Pb / quinoline).
- Rosenmund (Pd / BaSO₄ / quinoline) for acid chloride
  → aldehyde.

### Halide (Cl⁻, Br⁻, I⁻)

Halides bind Pd(II) strongly. Excess Cl⁻ slows Suzuki +
other Pd cycles → use less reactive base (KOAc, K₃PO₄
instead of CsCl-containing systems).

### Amines (basic)

Strongly basic amines bind Lewis-acid catalysts +
displace ligands. Use a sterically hindered amine
(2,6-lutidine, DIPEA) instead.

### Oxygen + water

Most organometallic catalysts are O₂- + H₂O-sensitive.
Schlenk technique + glovebox + sparging are standard.

Modern catalysts (XPhos-Pd-G3, Buchwald 4th-gen
preformed Pd) are bench-stable + air-stable.

## Tolerance design

Modern catalyst design specifically combats poisoning:

### Sulfur-tolerant Pt catalysts (Toste, others)

For natural-product synthesis with intact sulfide groups:

- **N-heterocyclic carbene + Pt** — NHC-Pt
  catalysts.
- **Pt nanoparticles in silica matrix** — diffusion-limited
  binding mitigates poisoning.

### Sulfur-tolerant hydrogenation (industrial petrochem)

Petrochemicals contain sulfur (sulphide, thiophene). Bulk
processes use:

- **Co-Mo-S sulfidic catalysts** — INTENTIONALLY sulphided;
  H₂ + sulphur both bind cooperatively (HDS = hydrodesulphurisation).
- **Ni-Mo-S catalysts** — same idea, fewer S in feedstock.

### Single-atom catalysts (SACs) — sulphur tolerance

Pt-N₄ + Co-N₄ on N-doped carbon support → less sensitive to
S than nanoparticle Pt because the active site geometry is
fundamentally different.

## Catalyst recovery + recycling

For expensive catalysts, recovery is critical:

- **Heterogeneous Pd / Pt on carbon** — filter off + reuse.
- **Pd on resin / fibre** — fixed-bed flow chemistry.
- **TPPTS-Pd in water** — Pd stays in aqueous phase;
  product extracts into organic.
- **Magnetic-nanoparticle-supported Pd** — pulls out with
  a magnet.
- **NHC ligand recovery** — usable for Pd-NHC systems.

## Poison detection (PoiSon-MS, ICP)

In process development:

- **ICP-MS** measures trace metal in product (FDA limit for
  Pd in oral API: < 10 ppm).
- **ICP-OES** for higher concentrations.
- **Hg-amalgam test** for unwanted Pd / Pt residues.

## Standard catalyst clean-up

After Pd-catalysed coupling at scale:

- **SiO₂-thiol / SiO₂-thiourea pads** — remove Pd to <
  ppm.
- **Quadrasil-MP / SmoPex / N-acetylcysteine** scavengers
  — commercial Pd scavengers used by Pfizer + others.
- **Activated carbon** — non-specific scavenger; absorbs
  many residues.

## Try it in the app

- **Tools → Lab reagents…** → look up Lindlar catalyst,
  Pd/C, Pt/C, Quadrasil-MP for storage + handling.
- **Glossary** → search *Catalyst poisoning*, *Lindlar
  catalyst*, *Sulfur tolerance*, *Pd scavenger*, *ICP-MS*,
  *Photoredox catalysis*, *Catalytic triad*.

Next: **Continuous-flow process design**.
