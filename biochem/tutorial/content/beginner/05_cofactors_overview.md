# Cofactors and coenzymes — chemistry the protein can't do

Many enzymes can't do their reactions with amino-acid
side chains alone.  They need **cofactors** — small non-
protein molecules that bring chemistry the 20 amino acids
can't access.

## Why amino acids aren't enough

The 20 amino acid side chains give you:

- Acid-base catalysis (Asp / Glu / His / Cys / Lys / Tyr).
- Nucleophilic attack (Ser-OH, Cys-SH).
- Hydrogen bonding (Ser / Thr / Asn / Gln / Tyr).
- Electrostatic stabilisation (charged residues).
- Hydrophobic surfaces (Phe, Leu, Ile, Val, Met, Trp).

But you can't easily do:

- **Single-electron chemistry** — biology runs on
  reductive + oxidative reactions; amino acids are bad
  one-electron carriers.
- **Hydride transfer** (2 electrons + 1 proton) — the
  workhorse of metabolic redox biochemistry.
- **Methyl-group transfer** with electrophilic methyl.
- **Carbon-skeleton rearrangements**.
- **Multi-electron oxygen chemistry**.

For these, biology evolved cofactors.

## The major cofactor classes

### Nicotinamide (NAD+ / NADH, NADP+ / NADPH)

Hydride (H⁻) carriers.  NAD+ is reduced to NADH on
catabolic dehydrogenase reactions; NADH then donates
electrons to the mitochondrial ETC.

NADP+/NADPH plays the parallel role for **anabolic**
reductive biosynthesis (fatty acids, cholesterol,
nucleotides) — kept mostly reduced so it can drive
biosynthetic reduction.

The cellular mnemonic: **"NADH for catabolism, NADPH for
biosynthesis"**.

### Flavin (FAD / FADH₂, FMN)

Tightly-bound (often covalent) prosthetic groups on
flavoproteins.  Two-electron + two-proton carriers, but
can also do one-electron chemistry via a stable
semiquinone intermediate.  This 1e⁻/2e⁻ flexibility is
what makes flavins the bridge between two-electron
biochemistry + one-electron chemistry of the ETC.

### Coenzyme A (CoA / acetyl-CoA)

Carries acyl groups via thioester linkage.  Acetyl-CoA
is the central 2-carbon currency connecting carbohydrate,
fat, + amino-acid metabolism into the TCA cycle for
oxidation, or fatty-acid + cholesterol biosynthesis +
histone acetylation for biosynthesis + epigenetics.

### S-adenosyl methionine (SAM)

The universal methyl donor.  Sulfonium centre makes the
methyl group electrophilic + transferable — drives DNA +
RNA + protein + small-molecule methylation.  Becomes
SAH (S-adenosyl homocysteine) after methyl transfer.

### Phosphate-energy currency (ATP / ADP / AMP, GTP)

Not a "cofactor" in the prosthetic-group sense, but the
energy currency that drives unfavourable reactions:

- **ATP hydrolysis ΔG° = -30.5 kJ/mol** at standard
  conditions, ~ -55 kJ/mol intracellularly.
- **Phosphoryl-group transfer** to a substrate primes it
  for further reaction (kinase reactions).
- **Adenylylation** (AMP transfer with PPi loss) is the
  initiation step of many ligase reactions (aminoacyl-
  tRNA synthetase).

### Vitamin-derived prosthetic groups

Many cofactors come from B-vitamins:

- **Biotin (B7)** — carboxylase prosthetic; carries
  CO₂.
- **Thiamine pyrophosphate (TPP, B1)** — α-keto-acid
  decarboxylase + transketolase; carries 2-carbon active-
  aldehyde unit.
- **Pyridoxal phosphate (PLP, B6)** — universal amino-
  acid cofactor; transamination, decarboxylation,
  racemisation.
- **Lipoate** — α-keto-acid dehydrogenase complexes
  (PDH, α-KGDH); shuttle acyl groups + electrons.
- **Cobalamin (B12)** — methionine synthase (methyl
  carrier) + methylmalonyl-CoA mutase (radical chemistry).
- **Tetrahydrofolate (B9)** — universal one-carbon
  donor for nucleotide biosynthesis + methionine
  recycling.

### Metal cofactors

- **Heme** — Fe-protoporphyrin-IX; O₂ binding (hemoglobin),
  electron transfer (cytochromes), oxygen activation
  (P450s).
- **Mg²⁺** — every ATP-dependent enzyme uses Mg²⁺-ATP
  as the actual substrate.
- **Zn²⁺** — Lewis-acid catalysis (carbonic anhydrase,
  alcohol dehydrogenase) + structural (Zn-finger TFs).
- **Fe-S clusters** — electron-transfer relays in
  Complexes I + II + III, aconitase, nitrogenase.
- **Cu** — Complex IV, lysyl oxidase, dopamine β-
  hydroxylase.

### Quinones

Membrane-soluble electron carriers:

- **Ubiquinone (CoQ10)** — between Complex I/II + Complex
  III in the mitochondrial ETC.
- **Plastoquinone** — between PSII + cyt b₆f in the
  chloroplast photosynthetic chain.
- **Menaquinone (vitamin K)** — γ-glutamyl carboxylation
  cofactor (clotting-factor activation, target of warfarin).

### Redox-buffer small molecules

- **Glutathione (GSH)** — cellular redox buffer at ~ 5 mM;
  protects against oxidative stress.
- **Ascorbate (vitamin C)** — Fe-dependent dioxygenase
  cofactor + aqueous antioxidant; humans don't make it,
  must eat it.

## The vitamin connection

Almost every B-vitamin maps to a cofactor:

| Vitamin | Cofactor | Deficiency |
|---------|----------|------------|
| B1 (thiamine) | TPP | Beriberi, Wernicke-Korsakoff |
| B2 (riboflavin) | FAD, FMN | Ariboflavinosis |
| B3 (niacin) | NAD+/H, NADP+/H | Pellagra (the four Ds) |
| B5 (pantothenate) | CoA | Rare; Hallervorden-Spatz |
| B6 (pyridoxine) | PLP | Neuropathy, sideroblastic anaemia |
| B7 (biotin) | Biotin | Dermatitis, alopecia |
| B9 (folate) | THF | Megaloblastic anaemia, NTDs |
| B12 (cobalamin) | Methylcobalamin, AdoB12 | Megaloblastic + SCDC |

Plus C (ascorbate), D (vitamin D — hormone, not enzyme
cofactor), K (menaquinone — γ-carboxylation cofactor).

## Try it in the app

- **Window → Biochem Studio → Cofactors** — full BC-2.0
  cofactor catalogue with chemistry + role + vitamin
  origin + deficiency-disease per entry.
- **Window → Biochem Studio → Enzymes** — every enzyme
  entry lists its cofactor requirements.

Next: **Enzyme kinetics — Michaelis-Menten**.
