# Solubility — "like dissolves like"

The textbook rule of thumb works because dissolving is a
**competition between intermolecular forces**: the solvent must
break solute-solute interactions + form replacement solvent-
solute interactions of comparable strength.

## The rule, formalised

A solute dissolves well in a solvent when their **dominant
intermolecular forces match**:

| Solute IMFs | Solvent that dissolves it |
|-------------|---------------------------|
| Non-polar dispersion | Non-polar solvent: hexane, toluene, DCM |
| Polar / dipole | Polar aprotic: acetone, DMF, DMSO, MeCN |
| H-bonding | Polar protic: water, methanol, ethanol |
| Ionic | Polar protic (water dissolves most salts) |

A simple predictor is the **logP** (octanol-water partition
coefficient):

- logP > 3 → strongly hydrophobic, dissolves in oils + lipids
- logP 0-3 → moderately polar, dissolves in EtOH/MeOH
- logP < 0 → hydrophilic, dissolves in water

## Why it matters in lab

- **Reaction setup** — pick a solvent that dissolves both
  reactants + doesn't compete with the chemistry.  Strongly
  H-bonding solvents (water, alcohols) are bad for Grignard
  reactions because they protonate the organometallic; THF or
  Et₂O are inert + dissolve both Mg and the alkyl halide.
- **Workup** — extract products by partitioning between an
  organic + aqueous phase. Ionic byproducts (salts, acids,
  bases) wash into water; neutral organics stay in the
  organic phase.  Ester products go to ether + away from
  unreacted carboxylic-acid starting material when the
  aqueous layer is basic (deprotonates the acid into the
  water-soluble carboxylate).
- **Recrystallisation** — pick a solvent the impure solid
  dissolves in HOT but not COLD.  Slow cooling delivers
  pure crystals; impurities stay in the warm mother liquor.
- **Drug delivery** — too hydrophobic + the drug doesn't
  dissolve in plasma; too hydrophilic + it can't cross
  membranes.  **Lipinski's rule of 5** prescribes logP < 5
  + MW < 500 + H-bond donors ≤ 5 + H-bond acceptors ≤ 10
  for orally available drugs.

## Common laboratory solvents by polarity

Increasing polarity:

```
hexane → toluene → DCM → CHCl₃ → THF → Et₂O → EtOAc → acetone
   → MeCN → DMF → DMSO → 2-propanol → ethanol → methanol → water
```

The Phase-45 lab-reagents catalogue (in **Tools → Lab
reagents…**, Ctrl+Shift+R) has full per-solvent reference
cards (CAS number, freezing point, hazards, prep notes).

## Try it in the app

- **Tools → Lab techniques → Recrystallisation** — input a
  crude SMILES + solvent + crude mass; the calculator
  predicts the maximum recovery using the solvent's hot /
  cold solubility.
- **Tools → Lab techniques → TLC / Rf simulator** — load
  several compounds + an eluent solvent; the simulator
  predicts where each compound runs based on its logP +
  solvent polarity.
- **Molecule Workspace** → load **DMSO** + **Hexane** + check
  their dipole moments + logP in the *Properties* panel.

Next: **Boiling and melting points** — IMF + molecular shape
together.
