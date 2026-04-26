# Cis/trans + E/Z naming deeper

Two systems describe geometric isomerism at C=C double
bonds + ring substituents:

- **cis/trans** — the older system; works only for
  disubstituted double bonds.
- **E/Z** — the modern IUPAC system; works for any double
  bond, based on CIP priority.

## cis vs trans (qualitative)

For a 1,2-disubstituted alkene:

```
H     H              H     CH₃
 \   /                \   /
  C=C                  C=C
 /   \                /   \
CH₃   CH₃            CH₃   H
   cis (Z)              trans (E)
```

- **cis**: the two like (or analogous) groups on same side.
- **trans**: on opposite sides.

For 1,1-disubstituted (e.g. CH₂=CMe₂) or trisubstituted /
tetrasubstituted alkenes, there's no "obvious like group"
→ cis/trans fails.

## E/Z — the CIP rules

For each carbon of the C=C, identify the **higher-priority
substituent** by Cahn-Ingold-Prelog rules (atomic number;
go further out if tied).

- **Z** (zusammen, German "together"): both higher-priority
  substituents on **same side** of the double bond.
- **E** (entgegen, German "opposite"): higher-priority
  groups on **opposite sides**.

### CIP priority quick rules

1. Higher atomic number = higher priority.
2. If tied, look at next atoms out (working away).
3. Double / triple bonds count as if the atoms were
   duplicated.

```
example: 2-bromo-1-chloropropene
        Br    H
         \   /
          C=C
         /   \
        Cl   CH₃

C1 (left):  Br > Cl  → top group higher
C2 (right): CH₃ > H  → bottom group higher
Top higher (Br) on opposite side from bottom higher (CH₃)
                     → E
```

## Common pitfalls

- **Don't confuse "cis" with "Z"**: cis-2-butene = Z-2-butene
  IS true here, but for cinnamic acid (PhCH=CHCOOH), trans
  = E (because Ph + COOH are higher priority).
- **Visual symmetry is not E/Z** — CIP applies regardless
  of how you drew the molecule.

## Cycloalkane cis/trans

For 1,2-disubstituted cyclohexane:

- **cis**: both substituents on the same face (one up,
  one up; or one down, one down, after ring flip).
- **trans**: opposite faces.

In wedge-dash 2D:

- cis = both wedges, or both dashes.
- trans = one wedge + one dash.

## Polycyclic + bridgehead

For trans-decalin: the two ring-junction H's on opposite
faces (rigid; can't ring-flip). cis-decalin: same face
(can flip).

For norbornane bridgeheads: **endo** (toward the bridge,
2-position) vs **exo** (away).

## E/Z + biological activity

- **Retinal** (vision pigment) — 11-cis form binds
  rhodopsin; light flips to 11-trans → conformational
  change → nerve impulse.
- **Tamoxifen** — Z-isomer is the active anti-estrogen; E-
  isomer is weaker.
- **Stilbene** — cis form fluoresces; trans form
  isomerises to cis under UV (E → Z photoisomerisation).
- **Trans fatty acids** — natural unsaturated fats are
  cis; industrial hydrogenation creates trans isomers
  → cardiovascular risk.

## Try it in the app

- **Tools → Stereochemistry…** → input alkene SMILES → see
  E/Z assignment with CIP priorities.
- **Tools → Isomer relationships…** → *Classify pair* tab
  → input cis + trans SMILES → confirm relationship is
  *diastereomers* (not enantiomers).
- **Glossary** → search *Cis-trans isomerism*, *E/Z
  designation*, *CIP priority rules*, *Geometric isomers*.

Next: **Naming bicyclic compounds**.
