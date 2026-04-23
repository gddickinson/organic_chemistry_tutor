# Named Reactions: A Curated Tour

A **named reaction** is a transformation so widely used that chemists
save time by naming it after its discoverer(s) instead of describing
what bonds form. Graduate students are expected to recognise ~50 on
sight and explain the mechanism of at least 30. Industry chemists know
many more — the name *is* the shorthand for the whole mechanism +
conditions + scope.

This tutorial organises the canon into **six families**, anchors each
entry to whatever we have in the database (open in the Reactions tab
to see the scheme + the mechanism player where available), and flags
the reactions we should seed next (Phase 6b).

> Legend: ✅ = seeded reaction + mechanism, 🟡 = seeded reaction (no
> mechanism), ⬜ = not yet seeded.

## 1. C–C bond formation

### Polar / carbonyl

- **Aldol addition / condensation** (Wurtz 1872, Borodin 1869) ✅ —
  enolate + aldehyde → β-hydroxy carbonyl → α,β-unsaturated enone.
  Open **Aldol condensation** in the Reactions tab; click *Play
  mechanism*.
- **Claisen condensation** (Claisen 1887) 🟡 — ester-ester; enolate
  attacks another ester's C=O, expelling OR⁻.
- **Mannich reaction** (Mannich 1912) ⬜ — enolate + iminium →
  β-amino carbonyl. The asymmetric version (proline-catalysed) is the
  foundation of List-MacMillan organocatalysis.
- **Wittig olefination** (Wittig 1954; Nobel 1979) ✅ — Ph₃P=CHR +
  R'CHO → R-CH=CH-R' + Ph₃P=O.
- **Horner-Wadsworth-Emmons (HWE)** ⬜ — phosphonate variant of Wittig;
  E-selective, no Ph₃P=O waste.
- **Grignard / organolithium addition** (Grignard 1900; Nobel 1912) ✅
  — R-MgX / R-Li + aldehyde/ketone/ester → alcohol.
- **Michael addition (1,4-addition)** (Michael 1887) ✅ — stabilised
  nucleophile + α,β-unsaturated acceptor → 1,5-dicarbonyl.
- **Robinson annulation** (Robinson 1935) ⬜ — Michael + intramolecular
  aldol. Workhorse for 6-membered ring construction in steroid
  synthesis.
- **Reformatsky reaction** ⬜ — α-halo ester + Zn → zinc-enolate →
  attacks aldehyde/ketone → β-hydroxy ester.

### Aromatic / cross-coupling (Phase 21a organometallics lesson)

- **Friedel-Crafts alkylation / acylation** (Friedel & Crafts 1877) 🟡
  — Ar-H + R-X / RCOCl + AlCl₃ → Ar-R / Ar-COR.
- **Nitration of benzene** (Mitscherlich 1834) 🟡 — Ar-H + HNO₃ / H₂SO₄
  → Ar-NO₂.
- **Suzuki-Miyaura coupling** (Suzuki 1979; Nobel 2010) 🟡 — ArX +
  Ar'B(OH)₂ / Pd⁰ → Ar-Ar'.
- **Negishi coupling** (Negishi 1977; Nobel 2010) ⬜ — ArX + Ar'ZnX /
  Pd.
- **Sonogashira coupling** (Sonogashira 1975) ⬜ — ArX + R-C≡CH /
  Pd/Cu → Ar-C≡C-R.
- **Heck reaction** (Heck 1972; Nobel 2010) ⬜ — ArX + CH₂=CHR / Pd →
  ArCH=CHR (E).
- **Buchwald-Hartwig amination** (Buchwald & Hartwig 1994) ⬜ —
  ArX + HNR₂ / Pd + bulky phosphine → Ar-NR₂.

### Pericyclic (Phase 21a tutorial)

- **Diels-Alder [4+2] cycloaddition** (Diels & Alder 1928; Nobel 1950)
  ✅ — diene + dienophile → cyclohexene. Thermally allowed
  (see `check_wh_allowed(kind="cycloaddition", electron_count=6)`).
- **[2+2] photocycloaddition** ⬜ — photochemically allowed, thermally
  forbidden (Hückel-antiaromatic TS).
- **Azide-alkyne click (CuAAC)** (Sharpless, Meldal 2002; Nobel 2022)
  ⬜ — azide + terminal alkyne / Cu catalyst → 1,4-disubstituted-1,2,3-
  triazole. The reaction of the 2010s.
- **Cope / Claisen [3,3]-sigmatropic rearrangement** ⬜ — 6-electron
  TS, thermally allowed.
- **6π electrocyclic** 🟡 — thermal disrotatory closure.

## 2. Oxidations

- **PCC / PDC** (Corey 1975) ✅ — 1° alcohol → aldehyde; 2° → ketone.
  Milder than CrO₃ / Jones.
- **Swern oxidation** ⬜ — (COCl)₂ + DMSO + Et₃N; alcohol → aldehyde /
  ketone. No over-oxidation. Typical undergraduate lab technique.
- **Dess-Martin periodinane (DMP)** ⬜ — modern neutral oxidant.
  Reagent already in DB (`DMP`).
- **Jones oxidation** ⬜ — CrO₃ / H₂SO₄ / acetone. Aggressive; 1°
  alcohol → carboxylic acid.
- **Baeyer-Villiger oxidation** 🟡 — ketone + mCPBA → ester (inserts
  O between C=O and neighbour). Migratory-aptitude controlled.
- **Sharpless epoxidation** (Sharpless 1980; Nobel 2001) ⬜ — allylic
  alcohol + Ti(OiPr)₄ + tartrate + t-BuOOH → chiral epoxide. 99% ee
  on good substrates.
- **Jacobsen / Shi epoxidation** ⬜ — more general (non-allyl) enantio-
  selective epoxidation.
- **Upjohn dihydroxylation** / **Sharpless AD** ⬜ — OsO₄ (cat.) +
  NMO / DHQD-PHAL → syn-diol, chiral version.
- **Ozonolysis** ⬜ — O₃ then Me₂S / Zn-AcOH → two carbonyl fragments.
- **Wacker oxidation** ⬜ — PdCl₂ / CuCl₂ / H₂O; terminal alkene →
  methyl ketone.

## 3. Reductions

- **Catalytic hydrogenation** (Sabatier 1897; Nobel 1912) 🟡 — H₂ /
  Pd, Pt, Ni → alkene → alkane; also reduces ketones, aldehydes,
  nitriles, nitro groups (metal-dependent).
- **NaBH₄ reduction** (Brown 1943) ✅ — mild; aldehyde / ketone →
  alcohol.
- **LiAlH₄ reduction** ⬜ — aggressive; also reduces esters / amides /
  carboxylic acids to alcohols / amines.
- **DIBAL-H** ⬜ — selective reduction of esters to aldehydes (at −78 °C,
  1 equiv).
- **Wolff-Kishner reduction** ⬜ — C=O → CH₂ via hydrazone under
  strong base. Alkaline conditions; good for acid-sensitive substrates.
- **Clemmensen reduction** ⬜ — C=O → CH₂ via Zn/Hg + HCl. Acidic
  counterpart of Wolff-Kishner.
- **Meerwein-Ponndorf-Verley (MPV)** ⬜ — Al(OiPr)₃ / iPrOH; very
  mild; ketone ↔ alcohol via hydride transfer.
- **Noyori asymmetric hydrogenation** (Noyori 1980s; Nobel 2001) ⬜ —
  Ru-BINAP / H₂; prochiral ketone → chiral alcohol, 99 % ee.

## 4. Rearrangements

- **Pinacol rearrangement** 🟡 — diol + acid → migration → ketone.
  1,2-shift classic.
- **Beckmann rearrangement** ⬜ — ketoxime + acid → amide. Migratory
  aptitude matters.
- **Baeyer-Villiger** (counted under oxidations above) 🟡.
- **Curtius rearrangement** ⬜ — acyl azide → heating → isocyanate +
  N₂. Route to amines (after hydrolysis).
- **Schmidt reaction** ⬜ — ketone + HN₃ / acid → amide (analogous to
  Beckmann).
- **Hofmann rearrangement** ⬜ — amide + Br₂ / OH⁻ → isocyanate →
  amine. One fewer carbon than the starting amide.
- **Wolff rearrangement** ⬜ — diazoketone → heated → ketene.
- **Favorskii rearrangement** ⬜ — α-halo ketone + base → ring-
  contracted carboxylic acid.

## 5. Substitution / elimination (foundations)

- **SN1, SN2, E1, E2** ✅ — all four mechanisms seeded with full
  arrow-pushing + energy profiles.
- **Appel reaction** ⬜ — ROH + CCl₄ / PPh₃ → RCl. Mitsunobu's
  neutral cousin.
- **Mitsunobu reaction** ⬜ — ROH + Nu-H + PPh₃ / DIAD → R-Nu with
  inversion. SN2 on "activated" alcohols.
- **Finkelstein reaction** ⬜ — R-Cl + NaI / acetone → R-I. Driven
  by NaCl precipitation.
- **Williamson ether synthesis** ⬜ — RO⁻ + R'X → R-O-R' (SN2 variant).
- **Hell-Volhard-Zelinsky (HVZ)** 🟡 — carboxylic acid + Br₂ / PBr₃ →
  α-bromo carboxylic acid.

## 6. Asymmetric catalysis (Phase 21b graduate lesson coming)

- **Sharpless epoxidation / dihydroxylation** (Nobel 2001) — see above.
- **Noyori hydrogenation** (Nobel 2001) — see above.
- **Jacobsen HKR** ⬜ — chiral Co-salen catalyst resolves racemic
  epoxides via H₂O.
- **List / MacMillan organocatalysis** (Nobel 2021) ⬜ — proline /
  imidazolidinone enamine or iminium activation of aldehydes for
  asymmetric aldol / Mannich / Michael / Diels-Alder.
- **CBS (Corey-Bakshi-Shibata) reduction** ⬜ — chiral
  oxazaborolidine + BH₃; prochiral ketone → chiral alcohol.
- **Grubbs olefin metathesis** (Grubbs, Schrock 2005; Nobel 2005) ⬜
  — Ru / Mo carbenes. Makes C=C from two C=C.

## What to seed next (Phase 6b priority)

From a teaching perspective the biggest gaps in the current 28-reaction
DB are:

1. **Mitsunobu**, **Williamson**, **Appel** — substitution workhorses.
2. **Wolff-Kishner**, **Clemmensen**, **DIBAL-H**, **LiAlH₄** — the
   reduction family is under-represented.
3. **Click (CuAAC)** and **Grubbs metathesis** — Nobel-level methods
   not yet seeded.
4. **Sharpless AD / AE** + **Noyori** + **List-MacMillan proline
   aldol** — the asymmetric pillar.
5. **Mannich**, **HWE**, **Robinson annulation** — C–C forming gaps.

## Practice

1. In the Reactions tab, work through every reaction tagged with a
   green *Play mechanism* button — those are the 11 with full
   arrow-pushing mechanisms.
2. Ask the tutor: "What's the difference between a Wittig and a
   Horner-Wadsworth-Emmons olefination?"
3. `list_reactions(filter="cross-coupling")` returns the Pd-catalysed
   reactions already in the DB (Suzuki so far; the rest will come in
   future expansion rounds).
4. Browse the `Morphine`, `Lovastatin`, `Penicillin G` entries in the
   Molecule browser — each is the product of a multi-step synthesis
   that uses 10+ of the named reactions above.

## Further reading

- Kürti, L. & Czakó, B. *Strategic Applications of Named Reactions in
  Organic Synthesis* (2005). The definitive reference, organised
  alphabetically.
- Li, J. J. *Name Reactions* (5th ed., 2014). Shorter; more recent
  methodology included.
- Clayden, Greeves, Warren, *Organic Chemistry* (2nd ed., 2012). The
  undergraduate text that teaches most of these by name without ever
  calling them out.

Next (graduate tier): **Asymmetric synthesis** — the chiral
counterpart to the canon above.
