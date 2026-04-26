# Brønsted-acid asymmetric catalysis — BINOL phosphates deeper

A **chiral Brønsted acid** protonates a substrate to
form an ion pair where the chirality of the acid biases
the stereochemistry of the next step. By 2025, BINOL-
derived phosphoric acids are the dominant
chiral-Brønsted-acid family.

## The catalyst

```
BINOL = 1,1'-bi-2-naphthol (atropisomeric chirality)
+ POCl₃ → BINOL phosphate (BINOL-PO(OH))
+ 3,3'-substitution (e.g. TRIP = 2,4,6-triisopropylphenyl)
   → tunable steric environment
```

The 3,3'-substitution dictates how big the chiral pocket
is + how much steric demand the substrate sees.

Famous variants:

- **TRIP** — 2,4,6-triisopropylphenyl on each 3,3'-position.
  The original "good" BINOL phosphate.
- **TADDOL phosphate** — based on different chiral
  scaffold.
- **VAPOL phosphate** — vaulted biphenyl.
- **SPINOL phosphate** — spiro-dioxolane variant.
- **BINSA** — sulfonimide (stronger acid than phosphate).

The pKa of BINOL-PO(OH) ~ 2-3 in DMSO; BINSA ~ -4. Both
strong enough to protonate imines + α,β-unsat carbonyls.

## Mechanism

Bifunctional catalysis:

```
[BINOL-PO(OH)]
   ↓ deprotonate
[BINOL-PO(O⁻)]    +    H⁺ on substrate (e.g. imine N)
                       → [substrate-H⁺ ··· (BINOL-PO(O⁻))] ion pair
       (chiral counter-ion) → controls face of attack
```

Houk + Goodman + Akiyama have done detailed DFT studies
showing the substrate sits in a chiral pocket between the
two 3,3'-aryl walls.

## Reaction classes

### Mannich + Strecker

```
imine + nucleophile + chiral acid → α-amino product (> 95 % ee)
```

Examples:

- α-amino nitrile (Strecker) — Jacobsen thiourea is
  competitor; both work.
- α-amino phosphonate.
- α-amino ester.
- α-amino sulfide.

### Transfer hydrogenation

```
imine + Hantzsch ester (H source) + chiral acid →
                                    chiral amine (> 95 % ee)
```

Akiyama 2004 + List 2005 simultaneously discovered this.
Industrial route to chiral amine APIs.

### Friedel-Crafts alkylation of indoles + pyrroles

```
indole + α,β-unsat ester + chiral acid →
                       chiral indole adduct (> 90 % ee)
```

A workhorse for chiral 3-alkylindole synthesis.

### Asymmetric pinacol / semi-pinacol

```
β-hydroxy aldehyde + chiral acid →
                  → chiral α-hydroxy ketone
                  via 1,2-shift in chiral environment
```

Tu / Xu used this for tertiary alcohols.

### Asymmetric Pictet-Spengler

Mentioned in lesson 36 (thiourea); BINOL phosphate also
catalyses Pictet-Spengler with > 95 % ee.

### Asymmetric chlorination + fluorination

α-position of carbonyl + N-Cl-suc / Selectfluor + chiral
phosphoric acid → enantioenriched α-halo carbonyl.

### Asymmetric Diels-Alder

Inverse-electron-demand DA + chiral acid + dienophile →
chiral cycloadduct.

## Stronger acids — phosphoramides + sulfonimides

For substrates that BINOL-PO(OH) doesn't protonate:

- **BINOL-N-sulfonyl phosphoramidates** (List, 2008) — stronger
  + extends scope.
- **BINSA + cyclopentadiene-based BINOL sulfonates** — even
  stronger; extends to less basic substrates.
- **Thiophosphoric acids** — modulate pKa.

## Limits

- High catalyst loading (5-20 mol %).
- BINOL phosphates can be expensive ($100-500/g).
- Some substrates are too weak as bases or too weak as
  nucleophiles → no acceleration.

## Industrial uses

- **Sitagliptin** alternative routes (in addition to the
  KAH biocatalysis route).
- **Eliprodil + neuro-pharma chiral amine APIs** — chiral
  Brønsted acid + transfer hydrogenation route.
- **Chiral N-aryl piperidines** — via reductive Mannich +
  chiral acid.

## Try it in the app

- **Reactions tab** → look for asymmetric reductive
  amination + Strecker (if seeded).
- **Tools → Stereochemistry…** → input chiral product
  → confirm R/S configuration.
- **Glossary** → search *Brønsted acid catalysis*,
  *BINOL phosphate*, *Asymmetric reductive amination*,
  *Hantzsch ester*, *Atropisomerism*.

Next: **Allylation reactions (Tsuji-Trost, Mukaiyama,
allyl-B)**.
