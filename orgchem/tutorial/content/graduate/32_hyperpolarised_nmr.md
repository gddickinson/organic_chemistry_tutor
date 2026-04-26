# Hyperpolarised NMR — DNP, PHIP, SABRE

NMR's Achilles heel is **sensitivity**. The Boltzmann
population difference at room T + 11.7 T magnet is ~ 1 in
10⁵ — most of the spins are useless. **Hyperpolarisation**
techniques boost the polarisation by 10³-10⁵× → enable
NMR signals from minuscule sample amounts.

## Why hyperpolarise?

For ¹H at 500 MHz / 11.7 T at 298 K:

```
N_+ - N_- ≈ 1 × 10⁻⁵ × N
```

Hyperpolarised:

```
N_+ - N_- ≈ 0.1 - 1 × N (orders of magnitude greater)
```

Result: signal-to-noise scales linearly with polarisation
→ 10⁴ × signal increase = 10⁸ × time saving.

## Three main techniques

### 1. DNP (dynamic nuclear polarisation)

Mix sample with a stable radical (TEMPO derivative, AMUPol,
trityl) at low T (~ 100 K). Microwave irradiation at the
electron resonance frequency drives polarisation transfer
from electrons to nuclei.

```
electron polarisation: ~ 1 part in 100 (γ_e ~ 660 × γ_H)
+ μw irradiation at 263 GHz (for 9.4 T) → transfer to ¹H
→ ¹H polarisation ~ 100 × thermal
```

### Variants

- **MAS-DNP** (in solid state) — combine MAS + μw +
  cold N₂ at 100 K → ssNMR sensitivity gain.
- **D-DNP (dissolution DNP)** — polarise sample at 1 K +
  3.35 T, dissolve in pre-heated solvent + transfer to
  high-field magnet → > 10⁴× ¹³C signal for tens of
  seconds.

### Applications

- **In vivo metabolic imaging** — hyperpolarise [1-¹³C]
  pyruvate, inject into patient or animal, watch real-time
  metabolic flux into lactate, alanine, bicarbonate. GE
  Healthcare's SpinPolaris commercial system.
- **Reaction monitoring** — D-DNP-prepared reagent injected
  into reaction → real-time NMR of intermediates.
- **MAS-DNP** for membrane proteins, polymorphs, materials.

### 2. PHIP (parahydrogen-induced polarisation)

```
n-H₂ (75% ortho + 25% para at rt) → cool to 30 K → enrich p-H₂
+ catalyst (Ir-IMes-COD) + alkene/alkyne → product gains spin order
```

Para-H₂ has both spins paired (singlet); when added across
a substrate's bond, the resulting hydrogens retain a
correlated state → strong NMR enhancement.

### Variants

- **PASADENA** — high-field PHIP; gives anti-phase signal.
- **ALTADENA** — low-field PHIP, then transfer to high-
  field; gives in-phase signal.
- **SABRE** (signal amplification by reversible exchange,
  Duckett 2009) — substrate + Ir(IMes) catalyst + p-H₂ in
  the *NMR magnet* → polarisation transfers via temporary
  Ir-substrate complex, no bond formation needed.

### SABRE applications

Hyperpolarisation works without consuming the substrate
or hydrogenating it:

- Polarise pharmaceuticals, natural products,
  drugs of interest.
- ¹⁵N polarisation for biomolecules.
- Oxford / Duke / AKM groups working on biomedical
  applications.

### 3. Optical pumping (Xe, Hg)

For noble gases:

- ¹²⁹Xe (I = 1/2, 26 % nat. abun.) gas pumped with circularly
  polarised laser light tuned to Rb 794.7 nm → Rb spin
  polarisation → ¹²⁹Xe via spin exchange → polarised
  ¹²⁹Xe ~ 50 % polarisation at 1 atm.

Used for:

- **Lung imaging** in cystic fibrosis + COPD patients
  (inhale hyperpolarised ¹²⁹Xe, image alveoli with MRI).
- **Surface chemistry** on porous materials.

## Compared to conventional NMR

| Method | Polarisation | Lifetime | Use |
|--------|-------------|----------|-----|
| Thermal | 10⁻⁵ | indefinite | bulk solutions |
| MAS-DNP | ~ 0.1 | minutes | solid-state, polymers, MOFs |
| D-DNP | ~ 0.1-0.5 | seconds (T₁) | metabolic imaging, fast reactions |
| PHIP | ~ 0.1-0.5 | T₁ (seconds) | catalysis, real-time |
| SABRE | ~ 0.05-0.2 | T₁ | substrate-preserving |
| Optical pumping (Xe) | ~ 0.5 | minutes (gas) | medical lung imaging |

## Limits

- **D-DNP** — single-shot; signal decays in seconds; needs
  fast experiment.
- **PHIP / SABRE** — requires p-H₂ generator + Ir catalyst;
  scope of substrates limited.
- **MAS-DNP** — at low T (100 K), some samples have
  artefacts.
- **Cost** — DNP polariser ~ $1 M; SABRE setup ~ $50 k;
  PHIP generator ~ $20 k.

## Industrial / clinical uses

- **GE Healthcare SpinPolaris** — clinical D-DNP for
  prostate cancer + breast cancer real-time metabolic
  imaging (hyperpolarised pyruvate).
- **NMRNorthwest, MedImmune** — research SABRE platforms
  for drug-discovery NMR screening.
- **Bruker DNP-NMR** — academic + industrial for
  membrane proteins + materials.

## Try it in the app

- **Tools → Lab analysers…** → look up Bruker / Magritek
  hyperpolarised NMR (if seeded).
- **Glossary** → search *Hyperpolarisation*, *DNP*, *PHIP*,
  *SABRE*, *Optical pumping*.

Next: **EPR spectroscopy**.
