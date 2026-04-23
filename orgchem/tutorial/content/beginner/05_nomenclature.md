# IUPAC Nomenclature: Giving Molecules Their Real Names

Common names like *caffeine*, *aspirin*, *methanol* are convenient but
they don't scale. Chemistry has roughly 10⁸ known compounds; you can't
memorise a different name for each. **IUPAC nomenclature** solves the
problem by assigning every molecule a deterministic, systematic name
built from its structure.

This lesson walks through the core rules. It's backed by the **naming
rule catalogue** (`list_naming_rules()` in the tutor), which has 22
searchable rules + illustrated examples.

## The 5-step recipe for naming any molecule

1. **Pick the parent chain** — the longest continuous carbon chain
   that contains the principal functional group.
2. **Number the chain** to give the principal group the lowest locant.
3. **Identify substituents** and name each.
4. **Alphabetise substituents** (ignoring multiplier prefixes like
   *di-* / *tri-*).
5. **Assemble**: `substituent-locants-substituent-names-parent-name`.

Let's see it in action.

## Example 1: 2-methylbutane (SMILES `CC(C)CC`)

- Longest chain: 4 carbons. Parent = **butane**.
- Locants: number from either end; the methyl goes at position 2
  (the other direction would give position 3). Lower wins.
- Substituents: one methyl.
- Name: **2-methylbutane**.

Numbering from the wrong end would give `3-methylbutane` — the
*same molecule* but with a wrong locant. IUPAC requires the lowest
locant set; always compare both directions.

## Example 2: 3-ethyl-2-methylpentane

- Parent: 5 carbons = **pentane**.
- Two substituents: ethyl at 3, methyl at 2.
- Alphabetise: **e**thyl before **m**ethyl (don't count the "2-" / "3-";
  those are locants, not prefixes).
- Name: **3-ethyl-2-methylpentane**.

## Example 3: butan-2-ol (a.k.a. 2-butanol)

Alcohols use the **-ol** suffix. The OH outranks any alkyl branches
for numbering.

- Parent: 4 carbons → butan-.
- OH at C2 → **butan-2-ol**.
- (Older style: `2-butanol`. Both are recognised in journals; newer
  IUPAC recommends the first form.)

## Example 4: propanoic acid (`CCC(=O)O`)

Carboxylic acids use the **-oic acid** suffix. The COOH carbon is
**always C1** — no locant needed.

- Parent: 3 carbons including the COOH → **propanoic acid**.
- Common name: propionic acid.

## Example 5: (2E)-but-2-enoic acid (trans-crotonic acid)

- Parent: 4 carbons including C=C and COOH → **but-** with -**enoic
  acid** suffix.
- Double bond between C2 and C3 → locant 2 → **but-2-enoic acid**.
- The substituents across C=C define E/Z: methyl vs COOH at one end,
  H vs H at the other. Higher-priority groups (methyl and COOH) on
  *opposite* sides → **(2E)**.
- Full name: **(2E)-but-2-enoic acid**.

Ask the tutor:

> What's the IUPAC name of trans-crotonic acid?

It should resolve via `get_naming_rule("alkene-ez")` and return the
answer above.

## Substituent priority (the order that matters)

When a molecule has multiple functional groups, **one** becomes the
suffix (the *principal characteristic group*) and the rest become
prefixes. The priority order, highest to lowest:

| Rank | Group | Suffix | Prefix |
|------|-------|--------|--------|
| 1 | Cation | -onium | — |
| 2 | Carboxylic acid | -oic acid | carboxy- |
| 3 | Anhydride | -oic anhydride | — |
| 4 | Ester | -oate | -oxycarbonyl |
| 5 | Acid halide | -oyl chloride | halocarbonyl- |
| 6 | Amide | -amide | carbamoyl- |
| 7 | Nitrile | -nitrile | cyano- |
| 8 | Aldehyde | -al | oxo- |
| 9 | Ketone | -one | oxo- |
| 10 | Alcohol | -ol | hydroxy- |
| 11 | Amine | -amine | amino- |
| 12 | Ether | — | -oxy |
| 13 | Alkene | -ene | — |
| 14 | Alkyne | -yne | — |
| 15 | Alkane | -ane | — |

**Rule of thumb**: acids outrank everything; carbonyls (aldehyde /
ketone) outrank alcohols; alcohols outrank amines.

In a molecule with both an OH and a C=O, the C=O takes the suffix
(-one for ketone, -al for aldehyde), and the OH becomes the
**hydroxy-** prefix:

- `CC(=O)CCO` → 4-hydroxybutan-2-one (hydroxy is the prefix; butan-2-one
  is the principal name).

## Common names IUPAC grandfathered in

Some names are so entrenched that IUPAC permits them:

| Common name | IUPAC | SMILES |
|-------------|-------|--------|
| Acetic acid | ethanoic acid | `CC(=O)O` |
| Acetone | propan-2-one | `CC(=O)C` |
| Formaldehyde | methanal | `C=O` |
| Acetaldehyde | ethanal | `CC=O` |
| Toluene | methylbenzene | `Cc1ccccc1` |
| Phenol | hydroxybenzene (IUPAC accepts both) | `Oc1ccccc1` |
| Aniline | aminobenzene | `Nc1ccccc1` |
| Anisole | methoxybenzene | `COc1ccccc1` |
| Benzaldehyde | benzenecarbaldehyde | `O=Cc1ccccc1` |
| Benzoic acid | benzenecarboxylic acid | `OC(=O)c1ccccc1` |

For retained names on heterocycles (pyridine, pyrrole, furan,
thiophene, imidazole, etc.), see the **heterocycle-retained** entry in
the naming rule catalogue.

## Stereodescriptors in names

When a molecule has stereochemistry, the **(R)/(S)** or **(E)/(Z)**
descriptor goes at the front of the name in parentheses, with a
locant:

- **(2R)-butan-2-ol** — one stereocentre at C2, R configuration.
- **(2E,4Z)-hexa-2,4-dien-1-ol** — two double bonds, E at 2-3, Z at 4-5.
- **(2R,3S)-2,3-dibromosuccinic acid** — two stereocentres.

Run `assign_stereodescriptors(smiles=…)` on any chiral molecule to
see the descriptors RDKit assigns.

## Complex molecules: when do you give up?

IUPAC names get unwieldy for complex natural products:

- Caffeine: **1,3,7-trimethyl-3,7-dihydro-1H-purine-2,6-dione**. Most
  chemists say "caffeine".
- Cholesterol: **(3β)-cholest-5-en-3-ol**. Most say "cholesterol".
- Atorvastatin: IUPAC is ~100 characters. Everyone says "atorvastatin".

Rule of thumb: use the IUPAC name when clarity matters (graduate
coursework, patents, regulatory filings), and the common name
everywhere else. Both are valid.

## Practice

1. Load any molecule from the Molecule browser and look up its name.
   Open the **Properties** panel to see the IUPAC formula + common
   name. Does the common name give away the IUPAC?
2. Ask the tutor: *"Name this SMILES: `CC(=O)CCCO`"*. Expected:
   5-hydroxypentan-2-one.
3. Browse the naming rule catalogue with `list_naming_rules()`.
   Try `get_naming_rule("functional-group-priority")` for the
   master priority table in machine-readable form.
4. Use `assign_stereodescriptors(smiles=…)` on **L-Alanine** (its
   seeded SMILES is `C[C@@H](N)C(=O)O`). You should get one S
   stereocentre — so the full name is **(2S)-2-aminopropanoic acid**.

## Further reading

- IUPAC *Nomenclature of Organic Chemistry: IUPAC Recommendations
  and Preferred Names 2013* (the "Blue Book"). Free PDF at iupac.org.
- OpenEye's *Lexichem* or IBM *RXN* can round-trip structures to
  names automatically. Useful for rare / complex targets.
- Favre, H. & Powell, W. *Nomenclature of Organic Chemistry* (2013).
  The authoritative reference.

Next: continue to **Intermediate → Stereochemistry**. Once you know
how to *name* a molecule, you need to know how to describe its 3D
arrangement.
