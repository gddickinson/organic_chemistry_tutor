# Electronic structure of atoms — Aufbau in detail

Electrons fill atomic orbitals in a specific order set by
energy. **Aufbau** (German: "building up") + **Hund's rule** +
**Pauli exclusion** together let you write any element's
electron configuration.

## Three rules

1. **Aufbau**: fill lower-energy orbitals first.
2. **Pauli exclusion**: max 2 electrons per orbital,
   opposite spins.
3. **Hund's rule**: in degenerate orbitals (e.g. three 2p
   sub-orbitals), put one electron in each before pairing.

## Orbital energy order

The famous "Madelung diagonal":

```
1s
2s 2p
3s 3p [3d]
4s 3d 4p
5s 4d 5p
6s 4f 5d 6p
7s 5f 6d 7p
```

Read down the diagonals:
1s → 2s → 2p → 3s → 3p → 4s → 3d → 4p → 5s → 4d → 5p → 6s → 4f → 5d → 6p → 7s ...

4s fills before 3d (controversial but the rule mostly works
for ground states). The d block + f block insert as you'd
expect from the periodic table.

## Notation

Write the noble-gas core in brackets:

```
H: 1s¹
He: 1s²
Li: [He] 2s¹
C: [He] 2s² 2p²
N: [He] 2s² 2p³
O: [He] 2s² 2p⁴
F: [He] 2s² 2p⁵
Ne: [He] 2s² 2p⁶
Na: [Ne] 3s¹
Cl: [Ne] 3s² 3p⁵
Ar: [Ne] 3s² 3p⁶
K: [Ar] 4s¹
Ca: [Ar] 4s²
Sc: [Ar] 4s² 3d¹
Cr: [Ar] 4s¹ 3d⁵    ← anomaly: half-filled stability
Cu: [Ar] 4s¹ 3d¹⁰   ← anomaly: full-filled d⁵s¹ → d¹⁰s¹
Zn: [Ar] 4s² 3d¹⁰
Br: [Ar] 4s² 3d¹⁰ 4p⁵
```

## Hund's rule in action

Carbon's 2p² configuration: instead of putting both
electrons in 2px, put one in 2px and one in 2py with
parallel spins:

```
2p:  [↑] [↑] [ ]
     px  py  pz
```

NOT [↑↓] [ ] [ ]. The same-spin parallel arrangement is
~ 1 eV lower in energy than the paired arrangement
(electron repulsion).

## Half-filled + full-filled stability

Cr ([Ar] 4s¹ 3d⁵) and Cu ([Ar] 4s¹ 3d¹⁰) are anomalies
because half-filled (5 same-spin) + full-filled (10) sub-
shells have extra exchange-energy stabilisation.

Other elements with anomalies: Mo, Ag, Au, La, Ce, Gd,
Nb, Pt — about 20 in total.

## Ions

Lose electrons from the **highest n** first:

```
Fe: [Ar] 4s² 3d⁶ → Fe²⁺: [Ar] 3d⁶ (lose 4s, NOT 3d)
                  → Fe³⁺: [Ar] 3d⁵
```

This is why the 3d block transition metals lose 4s
electrons before 3d.

Negative ions just add electrons in normal order:

```
Cl⁻: [Ar]
O²⁻: [Ne]
```

## Connection to periodic trends

- **Period number** = principal quantum number n of the
  outermost shell.
- **Group number** = number of valence electrons (s + p
  for main groups; s + d for transition metals).
- **Atomic radius** decreases left-to-right within a period
  (more nuclear charge, same shell), increases top-to-bottom
  in a group (extra shells).
- **Ionisation energy** increases left-to-right (harder to
  pull e⁻ off cation), decreases top-to-bottom.
- **Electronegativity** same trend as IE.

## Try it in the app

- **Tools → Periodic table…** → click any element → see
  electron configuration + electronegativity + oxidation
  states.
- **Glossary** → search *Aufbau principle*, *Hund's rule*,
  *Pauli exclusion principle*, *Electron configuration*,
  *Atomic orbital*.

Next: **Drawing 3D models (chairs, Newman, sawhorse)**.
