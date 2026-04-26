# Drawing 3D models — chairs, Newman, sawhorse, wedge-dash

Organic chemists routinely draw 3D structures on flat
paper. Five conventions cover most cases:

- **Wedge / dash** — for stereocentres in line drawings.
- **Newman projections** — for conformations around one
  bond.
- **Sawhorse** — for conformations around one bond,
  alternative perspective.
- **Chair / boat** — for cyclohexane + 6-membered rings.
- **Fischer projections** — for chains of stereocentres
  (carbohydrates, amino acids).

## Wedge / dash

Standard perspective:

- **Solid wedge (▲)** — bond points TOWARD viewer.
- **Dashed wedge (||||)** — bond points AWAY from viewer.
- **Plain line** — bond in plane of paper.

Conventions:

- Two non-stereo bonds in plane → two stereo bonds (wedge +
  dash) point opposite directions.
- Don't draw 3 wedges (or 3 dashes) on one carbon — confusing.

## Newman projections

Look down a specific C-C bond:

```
         A  B
          \ /
           C₁ (front; small dot)
          / \
         C  D
          ___
         /   \
   E -- C₂ -- G    (back; circle)
         \___/
            F
```

- Front carbon: 3 substituents at 120°.
- Back carbon: 3 substituents at 120°, drawn outside the
  circle.
- Dihedral angle between front + back substituents = 0° to
  60° to 120° to 180° (eclipsed → gauche → eclipsed → anti).

Used to analyse rotational energy + conformations.

## Sawhorse

Same information as Newman but a tilted perspective on
the C-C bond:

```
       A
        \
   B--C₁
   /  / \
  D  C₂--E
       \
        F
```

Easier to relate to wedge-dash; harder to read dihedral
angles.

## Chair conformations

Cyclohexane's preferred shape. Each carbon has one
**axial** + one **equatorial** position:

```
      Axial (up at top, down at bottom)
       \    /     \    /
        C--C       C--C
       / \  \    /  / \
       |   \  \  /  /   |
       |   C--C  C--C    |
       \   /    \    \   /
        \ /      \    \ /
       Equatorial (alternating directions around the ring)
```

Substituents on a chair:

- **Axial** — vertical up or down.
- **Equatorial** — diagonal, slightly above or below the
  mean ring plane.
- **Ring flip** swaps every axial ↔ equatorial.
- Larger groups prefer equatorial (less 1,3-diaxial strain).

## A-values (axial-equatorial preference)

| Substituent | -ΔG (kcal/mol) preferring eq |
|-------------|------------------------------|
| F | 0.15 |
| Cl | 0.4 |
| OH | 0.5-0.9 |
| Me | 1.7 |
| Et | 1.8 |
| iPr | 2.2 |
| Ph | 2.9 |
| t-Bu | > 4.5 (essentially always equatorial) |

Tert-butyl "locks" a chair: t-Bu group always equatorial.

## Drawing conventions

The "wedge-dash chair" convention:

- Draw the chair as 6 lines (zigzag), 3 up + 3 down.
- Add axial bonds (vertical from each C).
- Add equatorial bonds (parallel-ish to nearest ring bond).

Practice: 4-tert-butylcyclohexane shows t-Bu axial-or-eq
locked (t-Bu always eq).

## Fischer projections

Carbon chain vertical; horizontal bonds come forward,
vertical go back. Used for sugars + amino acids:

```
CHO
H-C-OH        (D-glyceraldehyde)
 CH₂OH
```

The right-side OH = D enantiomer (highest-numbered chiral
C has OH on the right).

## When to use each

| Convention | Use for |
|------------|---------|
| Wedge / dash | Stereocentres in 2D line structures |
| Newman | Conformational analysis, ethane / butane / vicinal stereocentres |
| Sawhorse | Same as Newman, less common |
| Chair | Cyclohexane + 6-membered rings |
| Fischer | Carbohydrate / amino acid CIP discussions |

## Try it in the app

- **Tools → Drawing tool…** → wedge / dash atoms with the
  ChemDraw-style canvas.
- **2D viewer** → toggle stereo labels (R/S, E/Z) on any
  molecule.
- **3D viewer** → rotate any molecule to confirm chair vs
  boat preferences.
- **Glossary** → search *Newman projection*, *Chair
  conformation*, *Wedge bond*, *Dashed bond*, *Axial*,
  *Equatorial*, *Fischer projection*.

Next: **Cis/trans + E/Z naming deeper**.
