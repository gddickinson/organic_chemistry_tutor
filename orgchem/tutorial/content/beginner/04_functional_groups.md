# Functional Groups

Organic chemistry is organised by **functional groups** — small
structural motifs that determine how a molecule reacts. Two molecules
with the same functional group often react the same way, regardless of
the rest of the structure. Learn these ~15 groups and you'll read most
reactions on sight.

## The essential set

### Hydrocarbons (no heteroatom)

| Group | Structure | SMILES | Example |
|-------|-----------|--------|---------|
| **Alkane** | C–C, only single bonds | `CCCC` | Butane |
| **Alkene** | C=C | `C=CCC` | 1-Butene |
| **Alkyne** | C≡C | `C#CCC` | 1-Butyne |
| **Arene** | aromatic ring | `c1ccccc1` | Benzene |

Alkanes are unreactive and sit quietly until a radical / combustion
reagent comes along. Alkenes and alkynes have π electrons that react
with electrophiles and transition metals. Arenes have delocalised π
electrons that react via electrophilic aromatic substitution.

### Oxygen-containing

| Group | Structure | SMILES | Example |
|-------|-----------|--------|---------|
| **Alcohol** | C–OH | `CCO` | Ethanol |
| **Ether** | C–O–C | `COC` | Dimethyl ether |
| **Aldehyde** | C(=O)H | `CC=O` | Acetaldehyde |
| **Ketone** | C–C(=O)–C | `CC(=O)C` | Acetone |
| **Carboxylic acid** | C(=O)OH | `CC(=O)O` | Acetic acid |
| **Ester** | C(=O)O–C | `CC(=O)OC` | Methyl acetate |

### Nitrogen-containing

| Group | Structure | SMILES | Example |
|-------|-----------|--------|---------|
| **Amine** | C–NH₂ (primary), C–NH–C (secondary) | `CCN` | Ethylamine |
| **Amide** | C(=O)N | `CC(=O)N` | Acetamide |
| **Nitrile** | C≡N | `CCC#N` | Propionitrile |
| **Nitro** | C–NO₂ | `CC[N+](=O)[O-]` | Nitroethane |

### Halogens

| Group | Structure | SMILES | Example |
|-------|-----------|--------|---------|
| **Alkyl halide** | C–X (X = F/Cl/Br/I) | `CCBr` | Ethyl bromide |
| **Acyl halide** | C(=O)X | `CC(=O)Cl` | Acetyl chloride |

## Why functional groups matter

**Substitution and elimination** (see the intermediate lesson): any
alkyl halide is a possible SN1/SN2/E1/E2 substrate. Change F→Br→I and
the *rates* change (I is the best leaving group), but the mechanism
choices don't.

**Carbonyl chemistry**: aldehydes, ketones, carboxylic acids, esters,
amides, acyl halides are all related by oxidation state and leaving-
group identity. The same nucleophilic addition arrow works for all of
them — the difference is whether a leaving group can then depart.

**Protection groups**: a synthetic chemist often has to hide one
functional group (say, an alcohol) so they can do chemistry at another.
The "protected" form is a different functional group (often an ether);
the protection / deprotection steps just shuffle functional groups
around without building the target.

## Try it

Click through these molecules in the browser and identify every
functional group you see:

1. **Caffeine** — how many different functional groups? (Look for
   amide, aromatic amine, aromatic heterocycle, methyl groups, carbonyl.)
2. **Cholesterol** — find the lone alcohol, the lone C=C, and the
   hydrocarbon backbone.
3. **Sulfasalazine** — find the sulfonamide, the azo group (N=N), the
   carboxylic acid, and the phenol. (It's a classic drug for IBD
   treatment; the azo linker gets cleaved by gut bacteria to release
   the active component.)
4. **Thiamine** (vitamin B1) — find the thiazolium and the pyrimidine.

## Try it with the Tutor

Open the tutor console and ask:

    > "Walk me through every functional group in cocaine — for each one,
    > tell me one thing it does."

The LLM can see the structure via the agent actions and will annotate
them one by one. (Connect a backend first — Anthropic / OpenAI / Ollama.)

Next lesson: **IUPAC nomenclature** — giving each functional group a
consistent name.
