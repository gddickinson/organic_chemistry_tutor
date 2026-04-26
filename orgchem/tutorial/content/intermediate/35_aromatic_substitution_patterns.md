# Aromatic substitution patterns — DMG + ortho-lithiation

Beyond classical EAS, modern aromatic functionalisation
uses **directed metalation** + **C-H activation** to install
groups at specific positions with high regioselectivity.

## Directed ortho-metalation (DoM)

A **directing metallation group (DMG)** on the ring binds
a strong base (usually n-BuLi or s-BuLi) + delivers it to
the adjacent (ortho) position via a coordinated
intermediate.

```
ArH-DMG + n-BuLi → Ar(ortho-Li)-DMG + n-BuH
                 + R-X → Ar-R-DMG (ortho substituted)
```

### Common DMGs (decreasing strength)

| DMG | Co-ordination | Use |
|-----|---------------|-----|
| -OMOM (methoxymethyl ether) | medium | very common; protects + directs |
| -CON(iPr)₂ (Weinreb-style amide) | strong | Snieckus' favourite |
| -OCONiPr₂ (carbamate) | strong | Beak / Snieckus |
| -OMe (methoxy) | weak | works but slow |
| -F (fluoride) | weak-medium | F is a small DMG |
| -SO₂NR₂ (sulfonamide) | strong | tolerates many groups |
| -CHO (aldehyde, after MOM-protect or LDA at -78 °C) | needs care | |
| -NEt₂ (amine, sometimes) | medium | |

### Snieckus's rules

- DMG ortho-direction is dominated by **kinetic** (5-mem-
  metallacycle); thermodynamic might prefer different site.
- A second DMG nearby intensifies the effect (e.g. 1,3-
  dimethoxybenzene metallates at C2, between two OMe's).
- TMEDA (chelating diamine) accelerates n-BuLi.

### Workup electrophile examples

- **D₂O** → ortho-deuterated arene.
- **MeI** → ortho-methylated.
- **B(OMe)₃** → ortho-Bpin (after pinacol).
- **DMF** → ortho-CHO.
- **CO₂ / dry ice** → ortho-COOH.
- **R₂PCl** → arylphosphine.

## DoM in industrial synthesis

- **Vit. K analogues** — Snieckus + collaborators map
  meta + para via DMG manipulation.
- **Pesticide intermediates** — flonicamid + several
  fluorinated arene drugs.
- **Process chemistry** — replaces lengthy halogen-metal
  exchange routes for many regiochemistry problems.

## Halogen-metal exchange

```
ArBr + n-BuLi (or t-BuLi) → ArLi + n-BuBr
ArLi + R-X / B(OMe)₃ / etc. → functionalised arene
```

Fast (-78 °C, < 30 min). Works well for:

- Aryl bromides + iodides (NOT chlorides, generally).
- Vinyl + aryl halides.

Pitfall: t-BuLi is pyrophoric + dangerous. Modern flow
chemistry (Yoshida, Jensen) uses microreactors to safely
handle organolithium chemistry at scale.

## Modern alternatives

### Ir-catalysed C–H borylation (Hartwig-Ishiyama)

```
ArH + B₂pin₂ + Ir(cod)(OMe) / dtbpy → Ar-Bpin
```

- Selectivity by steric (most-accessible C-H wins, NOT
  electronic).
- No DMG needed; works on arene with no activator.
- Bpin product → Suzuki coupling for next step.

### Pd-catalysed C–H functionalisation

Pd(II) / Pd(IV) cycles (Sanford) install Cl, Br, OAc,
OAr, NR₂ at directed positions.

Most efficient with a pyridyl / oxime / amide directing
group on the substrate.

### Photoredox arylation

Decarboxylative arylation (MacMillan) + Minisci radical
substitution (heteroaromatic + acid + Ag/persulfate +
hv) → no DMG, no directing group, broad scope.

## Choosing the right method

| Goal | Best method |
|------|-------------|
| Install Bpin + then Suzuki on a non-DMG substrate | Ir borylation |
| Install F next to existing OMe or amide | Buchwald Pd-fluorination |
| Functionalise ortho to amide / carbamate at -78 °C | DoM |
| Halogenate a non-DMG arene | Pd-catalyzed C-H halogenation |
| α-arylation of a ketone | Buchwald-Hartwig |
| Substitute on heterocycle (e.g. pyridine 4-position) | Minisci photoredox |
| Late-stage functionalisation of advanced intermediate | DoM, photoredox, or Yu meta C-H |

## Try it in the app

- **Reactions tab** → load *Nitration of benzene*, *Friedel-
  Crafts*, *Suzuki* — see EAS + cross-coupling alongside.
- **Tools → Retrosynthesis…** → input arene targets → see
  how the disconnections hint at DoM vs cross-coupling.
- **Glossary** → search *Directed ortho-metalation
  (DoM)*, *DMG (directing metallation group)*, *Halogen-
  metal exchange*, *C-H activation*.

Next: **Oxime, hydrazone, imine chemistry**.
