# Catalytic asymmetric dihydroxylation + aminohydroxylation

The Sharpless toolkit added two more landmark methods to
the asymmetric arsenal: **AD (asymmetric dihydroxylation)**
+ **AA (asymmetric aminohydroxylation)**. Both use
inexpensive cinchona-alkaloid ligands + catalytic OsO₄.

## Sharpless asymmetric dihydroxylation (AD, 1988)

Substrate: any alkene (no directing group needed).

Reagent system (sold as a pre-mixed kit):

```
AD-mix-α: K₂OsO₄·2H₂O / K₃Fe(CN)₆ / K₂CO₃ / (DHQ)₂PHAL
AD-mix-β: K₂OsO₄·2H₂O / K₃Fe(CN)₆ / K₂CO₃ / (DHQD)₂PHAL
```

- **Os(VIII)** is the actual oxidant; turned over to Os(VI)
  by alkene addition then re-oxidised by ferricyanide.
- **(DHQ)₂PHAL** + **(DHQD)₂PHAL** are the chiral cinchona-
  alkaloid dimer ligands; they pre-coordinate Os.
- Both faces of the chiral ligand wrap around the active
  Os, presenting the alkene with a chiral pocket.

### Mnemonic for face delivery

Draw the alkene in the standard orientation (large group
upper left + small group upper right):

- **AD-mix-α** ((DHQ)₂PHAL) delivers OH groups from the
  **bottom** face.
- **AD-mix-β** ((DHQD)₂PHAL) delivers OH from the **top**.

Predicts > 95 % ee on most trans-disubstituted +
trisubstituted alkenes.

### Substrate scope (best to worst)

```
trans-disubstituted ≈ trisubstituted ≈ 1,1-disubstituted
            >    cis-disubstituted    >    monosubstituted
                                          (poor ee)
```

### Industrial impact

- **Diltiazem** (heart medication) intermediate.
- **Propranolol + timolol** intermediates (β-blockers).
- **Camptothecin + analogue** synthesis (DNA topoisomerase
  inhibitors).
- **Reverse-transcriptase inhibitors** (e.g.
  emtricitabine).

## Sharpless asymmetric aminohydroxylation (AA, 1996)

Same alkene + same ligand family, different oxidant /
nitrogen source.

Reagent system:

```
K₂OsO₄·2H₂O + Chloramine-T (or ROC(=O)NHCl, or sulfonamide chloramine)
            + (DHQ)₂PHAL or (DHQD)₂PHAL
```

Net: **alkene → β-amino alcohol** in one step, ee > 90 %.

### Why this matters

β-amino alcohols are everywhere in pharmacology —
analgesics (oxycodone), β-blockers, β-agonists
(salbutamol), antibiotics (chloramphenicol). The traditional
synthesis sequence: epoxide → SN2 with amine → β-amino
alcohol; AA collapses this into one step.

### Industrial example

**Chloramphenicol** synthesis — AA on cinnamyl alcohol
followed by aldol → key intermediate. Less waste than the
classical 6-step route.

## OsO₄ safety + catalyst handling

- **OsO₄** is volatile + highly toxic (eye damage; lung
  damage). Stored as solid or in solution; NEVER opened
  outside fume hood.
- Catalytic loading (1-10 mol %) keeps Os exposure manageable.
- Modern alternatives:
  - **NMO + OsO₄** (Upjohn) — uses NMO as terminal
    oxidant, more atom-economical than ferricyanide.
  - **OsO₄ on polymer support** — easier removal.
  - **Encapsulated Os in microreactors** — flow chemistry
    minimises operator exposure.

## Beyond Os — alternative dihydroxylation

- **Ru-based** (RuO₄ / RuO₂ / NaIO₄) — cheaper, harsher.
- **Mn-salen + H₂O₂** — emerging metal-free dihydroxylation.
- **Iron / α-ketoglutarate / O₂** (biomimetic) — α-KG
  dependent dioxygenase mimics.
- **Biocatalytic** — Rieske-type oxygenases (e.g., toluene
  dioxygenase) installs cis-diol on aromatic rings →
  intermediate to chiral cyclohexadiene synthons (Hudlicky,
  Boyd).

## DHQ vs DHQD — what's the difference?

DHQ (dihydroquinine) + DHQD (dihydroquinidine) are
diastereomers (almost-mirror-image cinchona alkaloids).
PHAL = phthalazine spacer that links two ligand units.
Other spacer variants:

- **PYR** — pyridine-based spacer, slightly different
  selectivity.
- **AQN** — anthraquinone spacer, complementary scope.
- **DPP** — diphenylpyrimidine, often best for terminal
  alkenes.

Picking spacer + ligand is part of method optimisation
(Sharpless's original 1992 paper on AD published a long
substrate-vs-ligand selection table).

## Sharpless's rule

> If a chiral product can be made via Sharpless AE / AD /
> AA, do that — these methods usually beat any other
> asymmetric synthesis on rate, ee, scalability, and
> setup.

This rule held from ~ 1990 until ~ 2010 when
organocatalysis + biocatalysis closed the gap on cost +
substrate scope. Sharpless AD + AA still dominate for
their target alkene classes.

## Try it in the app

- **Reactions tab** → load *Sharpless dihydroxylation* (if
  seeded).
- **Tools → Stereochemistry…** → input the diol product
  → see R/S assignments + cis vs trans.
- **Glossary** → search *Sharpless dihydroxylation*,
  *Asymmetric aminohydroxylation*, *Cinchona alkaloid*,
  *β-Amino alcohol*.

Next: **Hydroformylation + carbonylation chemistry**.
