# Aldol with chiral auxiliaries — Evans, Oppolzer, Myers

Before catalytic asymmetric aldol was reliable (~ 2000s),
**chiral auxiliaries** were the standard for
stereoselective aldol. They work by attaching a chiral
fragment, doing the diastereoselective reaction, then
removing the auxiliary.

## Why chiral auxiliaries

Pros:

- **Predictable stereochemistry** — a chair / Felkin-Anh
  TS is geometrically constrained.
- **High de** (> 95 % typically) — rivals catalytic
  asymmetric methods.
- **Easy purification** — diastereomers are separable on
  silica (unlike enantiomers).
- **Reliable scale-up** — works from mg to kg.

Cons:

- **Stoichiometric chiral material** — atom-uneconomical
  vs catalytic methods.
- **2 extra steps** — install + remove auxiliary.
- **Cost** — chiral auxiliary itself adds expense.

In modern practice, chiral auxiliaries still dominate for
some applications (Evans' aldol, Myers' alkylation in
total synthesis, kg-scale process chemistry).

## Evans oxazolidinone aldol (1981)

The most-cited chiral auxiliary in synthesis. Built from
chiral β-amino alcohol → cyclic carbamate.

```
chiral oxazolidinone + acyl chloride → chiral imide
                  + Bu₂BOTf + iPr₂NEt → boron Z-enolate
                  + RCHO → syn-aldol with > 95 % de
```

The boron enolate has a fixed Z-geometry; in the chair-
like TS, R group + boron sit equatorial → predictable
syn-product.

After aldol, the auxiliary is **removed**:

- LiBH₄ → β-hydroxy alcohol + recovered auxiliary.
- LiOH → β-hydroxy carboxylic acid + recovered auxiliary.
- LiOOH → β-hydroxy carboxylic acid (mild) + recovered
  aux.

### Why Evans

- Auxiliary is recoverable + reusable.
- The "Evans aldol" gives the **syn product** (vs anti
  with other methods).
- Very general — works with most RCHO + side chains.

### Famous targets

- Eribulin (Halichondrin B-related macrocycle).
- Discodermolide.
- Many polyketide natural products.
- Calystegine + alkaloid total syntheses.

## Oppolzer sultam (1989)

```
chiral camphor sultam + acyl chloride → chiral imide
                  + boron enolate / Mukaiyama aldol → high de
```

Camphor-derived; cheap chirality. Similar performance to
Evans for many substrates.

## Myers pseudoephedrine alkylation (1994)

```
chiral pseudoephedrine amide + LDA → Z-enolate
                  + RX → α-alkylated amide with > 95 % de
```

Used for asymmetric α-alkylation of amides, not aldol.
Pseudoephedrine is cheap chirality. Auxiliary is removed
by acid hydrolysis or base hydrolysis depending on
target product.

## Other chiral-auxiliary methods

- **Schöllkopf bislactim ether** — for amino-acid synthesis
  (1972).
- **Seebach aspartate alkylation**.
- **Davis chiral sulfinamide** (Ellman 1997) — for
  asymmetric amine + amino-acid synthesis.
- **8-Phenylmenthol** — historic chiral ester /
  carboxylic acid auxiliary.

## Boron enolate chemistry

Evans aldol uses **boron enolates** because of their:

- Defined geometry (Z-selective with Bu₂BOTf + iPr₂NEt).
- Tight 6-membered chair TS.
- Mild conditions (rt or 0 °C, no metal-halide salts).

Other boron enolate variants:

- **Brown anti-aldol** — uses chiral cyclohexyl borate +
  E-enolate → anti-product.
- **Ipc₂BOTf** — Brown's chiral boron triflate.

## Modern catalytic vs auxiliary

Modern catalytic asymmetric aldol (Sharpless AD doesn't
do aldol; List + MacMillan organocatalysis;
Evans / Carreira chiral Lewis acid) competes with
auxiliaries:

- **Cost** — catalysis at 0.5 mol % wins for big batches.
- **Substrate scope** — auxiliaries handle hindered
  substrates better.
- **Predictability** — auxiliaries give absolute control
  via chair TS; catalysts depend on substrate match.

In modern process chemistry: **catalysis preferred for
~ 70 %** of aldol problems; auxiliaries the other 30 %.

## Try it in the app

- **Reactions tab** → load *Aldol condensation* (seeded)
  for the parent + Mukaiyama / Evans concept.
- **Tools → Stereochemistry…** → check syn vs anti
  diastereomer designation.
- **Glossary** → search *Chiral auxiliary*, *Evans aldol*,
  *Oxazolidinone*, *Oppolzer sultam*, *Myers
  pseudoephedrine*.

Next: **Acylation + asymmetric acylation (Fu's nucleophilic
catalysis)**.
