# Buffers + Henderson-Hasselbalch deeper

A **buffer** is an aqueous solution that resists pH change
on addition of small amounts of acid or base. Buffers are
essential for biology + most analytical chemistry.

## The Henderson-Hasselbalch equation

```
pH = pKa + log([A⁻]/[HA])
```

The pH of a buffer depends on:

- The **pKa** of the weak acid (HA).
- The **ratio** of conjugate base to acid, NOT their absolute
  amounts.

At **pH = pKa**, [A⁻] = [HA] (1:1 mix).

## Buffer choice

Use a buffer with pKa within ± 1 of your target pH (the
"useful range" is ~ ± 1 pH unit around pKa).

| Buffer | pKa | Useful range |
|--------|-----|--------------|
| Citrate | 3.1, 4.8, 6.4 | 2-7 |
| Acetate | 4.76 | 3.7-5.7 |
| MES | 6.10 | 5.5-6.7 |
| BIS-TRIS | 6.50 | 5.8-7.2 |
| PIPES | 6.76 | 6.1-7.5 |
| Phosphate | 7.20 | 6.2-8.2 |
| HEPES | 7.55 | 6.8-8.2 |
| MOPS | 7.20 | 6.5-7.9 |
| Tris | 8.10 | 7.0-9.0 |
| Carbonate | 6.4, 10.3 | 9-11 |
| CHES | 9.30 | 8.6-10.0 |

Match buffer + target pH carefully — phosphate at pH 8.5
is essentially useless (off the useful range; β capacity
collapses).

## Buffer capacity (β)

How much acid or base can you add before pH changes
significantly?

```
β = 2.303 × C_total × α × (1 - α)        where α = [A⁻]/C_total
```

- **Maximum β** at pH = pKa (α = 0.5).
- β scales linearly with **total concentration** C_total.
- β collapses outside ± 1 pH unit from pKa.

For "useful" buffers, C_total typically 50-200 mM.

## Practical pitfalls

- **Tris pH-drifts ~ 0.03 / °C** — adjust at use temperature,
  not 25 °C.
- **Phosphate precipitates Mg²⁺ + Ca²⁺** — incompatible
  with many enzyme assays.
- **HEPES forms peroxides under UV** — bad for radiation-
  sensitive enzymes.
- **Tris forms a complex with Cu²⁺ + Pb²⁺** — interferes
  with metal-ion experiments.

## Common biology buffers

- **PBS** (phosphate-buffered saline) — pH 7.4, ~ 150 mM
  NaCl, 10 mM phosphate.
- **TBS** (Tris-buffered saline) — pH 7.5, similar.
- **TAE / TBE** — DNA gel buffers.
- **Tricine SDS-PAGE** — protein gel.

## Mineral acid + base ladder

For high-buffering at extremes:

- **pH 0-2**: HCl, H₂SO₄.
- **pH 13-14**: NaOH.

These aren't true "buffers" (no weak conjugate) but they
do hold pH within a useful range when in excess.

## Try it in the app

- **Tools → pH explorer…** → *Buffer designer* tab — input
  pKa + target pH + total concentration → recipe with
  capacity warning.
- **Tools → pH explorer…** → *Buffer capacity* tab —
  calculate β at any pH.
- **Glossary** → search *Buffer*, *Henderson-Hasselbalch
  equation*, *Buffer capacity*, *pKa*.

Next: **Spectroscopy unit conversions**.
