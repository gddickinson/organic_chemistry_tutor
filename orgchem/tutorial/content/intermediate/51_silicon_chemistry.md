# Silicon chemistry intro

Silicon (Group 14, just below carbon) shares many of carbon's
properties but with a much weaker C-Si bond + a strong
fluorophilic affinity. Used as protecting groups, leaving
groups, ligands, allyl-Si nucleophiles.

## Silyl protecting groups

| Group | Abbrev | Stability | Removal |
|-------|--------|-----------|---------|
| Trimethylsilyl | TMS / SiMe₃ | least stable; cleaves with mild aqueous base | TBAF, KF, dilute acid |
| Triethylsilyl | TES | medium | TBAF, mild acid |
| Triisopropylsilyl | TIPS | more stable | TBAF (longer) |
| tert-Butyldimethylsilyl | TBS / TBDMS | stable to bases, mild acids | TBAF, F⁻, HF·py |
| tert-Butyldiphenylsilyl | TBDPS | most stable; survives more conditions | TBAF + heat |
| Triethylsilyl ether | TES | medium |
| Triphenylsilyl | TPS | very stable; rare |

The pattern: **larger silyl group = more stable**. Choose a
silyl group based on what other reactions you'll run; remove
selectively at the end.

## Common silyl-installing recipes

```
ROH + TBSCl + imidazole + DMF → R-O-TBS  (workhorse)
ROH + TBSOTf + 2,6-lutidine + DCM → R-O-TBS (faster, selective for hindered alcohols)
ROH + TMSCl + Et₃N + THF → R-O-TMS (small-scale, fastest)
```

Imidazole or 2,6-lutidine traps HCl / HOTf; pyridine works
too.

## Removal

- **TBAF (n-Bu₄N F)** — fluoride attack on Si forms strong
  Si-F bond; removes any silyl ether. Workhorse.
- **HF·pyridine** — gentler, for sensitive substrates.
- **HF·NEt₃** — even gentler; for very sensitive groups.
- **KF in MeOH** — slow, mild.
- **Aqueous AcOH** — TMS only; gentle.
- **HCl / aqueous workup** — most silyls survive brief
  aqueous acid; HCl in MeOH cleaves TMS specifically.

## Silyl as leaving group — Brook rearrangement

```
R-CH(SiR'₃)-OH + base → R-CH(OSiR'₃)-H (silyl migrates from C to O)
```

Si migrates from C to O when an α-OH is deprotonated. The
1,3 Brook rearrangement enables homoenolate-like
chemistry → C-acylation in unusual positions.

## Si as a stable "carbocation surrogate"

Allyl-Si:

```
CH₂=CH-CH₂-SiMe₃ + RCHO + Lewis acid → CH₂=CH-CH₂-CH(OH)-R
```

Silyl-allyl is a soft nucleophile that adds to electrophilic
carbonyls (Hosomi-Sakurai allylation). Lewis acid activates
the carbonyl + the silyl group.

Asymmetric variants: chiral Lewis acids (BINOL-Ti) or chiral
ammonium fluoride catalysts.

## Vinyl + alkynyl-silanes

```
RC≡C-Si(R')₃ + electrophile + F⁻ → RC≡C-E (Hiyama-like)
```

Hiyama coupling: Pd + F⁻ activator + vinyl/aryl-silane →
cross-coupling product. Less popular than Suzuki because Si
reagents are pricier, but tolerates more functional groups.

## Silyl ketene acetals

```
R-CH₂-CO-OR' → R-CH=C(OSiMe₃)(OR') (silyl ketene acetal)
```

The carbon is now nucleophilic (Mukaiyama aldol):

```
silyl ketene acetal + RCHO + Lewis acid → β-hydroxy ester
```

Mukaiyama aldol → asymmetric variants via chiral Lewis
acids.

## Silylation reagents (table)

| Reagent | Use |
|---------|-----|
| TMS-Cl | TMS protection |
| TBSCl | TBS protection |
| TBSOTf | TBS for hindered alcohols |
| TIPSCl | TIPS protection |
| TBDPSCl | TBDPS for very stable protection |
| TMSI | silyl iodide; cleaves esters + ethers |
| TMSOTf | silyl triflate; activates many things |
| TMSCN | silyl cyanide (mild CN source for cyanohydrins) |
| BSA / BSTFA | silylating agents for GC-MS derivatisation |
| TIPSCl + AgOTf | makes TIPSOTf in situ |

## Trick: silyl directing groups

A bulky silyl group on a directing group can steer
asymmetric chemistry — Aggarwal sulfur ylides + Trost asymmetric
allylation use silyl-bearing chirality.

## Try it in the app

- **Tools → Lab reagents…** → look up TBSCl, TMSCl, TBAF,
  pyridine, imidazole.
- **Reactions tab** → look at *Mukaiyama aldol* (if seeded)
  for silyl ketene acetal chemistry.
- **Glossary** → search *Silyl protecting group*, *TBS*,
  *TBAF*, *Mukaiyama aldol*, *Brook rearrangement*,
  *Hiyama coupling*.

Next: **Carbohydrate-protein conjugation chemistry**
(advanced tier picks this up at lessons 27+).
