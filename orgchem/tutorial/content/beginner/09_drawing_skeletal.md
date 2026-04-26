# Drawing organic molecules — skeletal conventions

Organic chemists almost never draw every atom. The **skeletal
notation** (also called *line-angle*, *zig-zag*, or *bond-line*)
is the universal language: a few practiced rules let you draw a
20-carbon natural product in seconds.

## The five rules

1. **Vertices are carbons.** Every corner + every endpoint of
   a line is a carbon atom — unless explicitly labelled otherwise.
2. **Hydrogens on carbon are invisible.** Each carbon assumes
   exactly enough hydrogens to satisfy its valence (4 total
   connections). A vertex with 2 visible bonds carries 2 implicit
   H's.
3. **Heteroatoms (N, O, S, halogens, P) are written explicitly**
   with their bound H's (e.g. `OH`, `NH₂`, `SH`).
4. **Double + triple bonds are drawn explicitly** as parallel
   lines (=) or stacked lines (≡).
5. **Zig-zag the carbon chain** so each bond is at ~ 120°
   angles. This isn't decorative — sp³ carbon prefers tetrahedral
   geometry, so the zig-zag matches reality.

## Examples

- **Methane** (CH₄) — written as the formula, not as a line
  (a single dot doesn't communicate much).
- **Ethanol** (CH₃CH₂OH) — `\—OH` or `~OH` with a single
  zig-zag.
- **Benzene** — a hexagon with a circle inside (the circle
  conveys the aromatic π system; some textbooks use three
  alternating double bonds instead).
- **Caffeine** — a fused bicycle of two N-containing rings;
  every corner is a C unless otherwise marked.

## Why it works

Skeletal notation is **lossless** for connectivity: an organic
chemist can reconstruct the full Kekulé / Lewis structure from
the skeletal drawing in their head. It's also **fast**: a paper
showing 50 candidate molecules can render them all at once
without the reader's eye getting bogged down in CH-CH-CH
chains.

The Phase-6 Lewis-structure lesson goes the opposite direction
— teaches you to expand a skeletal drawing back into a fully-
labelled Lewis form. Keep both translations sharp.

## Try it in the app

- Open the **Molecule Workspace tab** + load **Caffeine**.
  The 2D viewer renders skeletal by default; toggle the style
  selector to compare against ball-and-stick + space-filling
  views.
- Click a few atoms — the rendered SMILES shows up below.
  Use the **Reading SMILES line notation** lesson to check
  your translations.
- Try **Tools → Drawing tool…** (Ctrl+Shift+D) — sketch a
  skeletal structure of your choice, hit *Send to Molecule
  Workspace* to verify the structure parses.

Next: **Valence, formal charge, and oxidation state** — count
electrons.
