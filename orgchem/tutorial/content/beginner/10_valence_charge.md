# Valence, formal charge, and oxidation state

Three different ways to count electrons. They're easy to confuse,
and the difference matters a lot when you're predicting
mechanisms.

## Valence

The **valence** of an atom is the **number of bonds it normally
forms** in a neutral molecule:

| Atom | Normal valence | Common in |
|------|----------------|-----------|
| C    | 4              | Everything |
| N    | 3              | Amines, amides, nitriles |
| O    | 2              | Alcohols, ethers, carbonyls |
| H    | 1              | Bound to anything |
| F, Cl, Br, I | 1     | Alkyl halides |
| S    | 2 (or 4 / 6 in oxidised forms) | Thiols, sulfones |
| P    | 3 (or 5 in phosphates) | Phosphines, phosphates |

If an atom shows a different number of bonds, it's almost
certainly carrying a formal charge.

## Formal charge

Formal charge tracks **electron bookkeeping** — who "owns" the
shared electrons in a bond:

```
formal charge = (valence electrons in free atom)
              − (lone-pair electrons)
              − (½ × bonding electrons)
```

Simpler form: `(group #) − (lone pairs × 2 + bonds)`.

- **NH₄⁺** — nitrogen has 4 bonds + 0 lone pairs → 5 − (0 + 4)
  = **+1**.
- **OH⁻** — oxygen has 1 bond + 3 lone pairs → 6 − (6 + 1) =
  **−1**.
- **A carbocation** — central C has 3 bonds, 0 lone pairs → 4 −
  (0 + 3) = **+1**.

Formal charge tells you where the positive / negative end of an
ion is + which atoms are electrophilic / nucleophilic.

## Oxidation state

Oxidation state is a **bookkeeping device for redox** — it
assumes every bond is fully ionic + assigns both electrons to
the more electronegative atom:

| Bond | More-EN atom claims |
|------|---------------------|
| C–H  | C (so C drops by 1, H goes up by 1) |
| C–C  | tie — neither moves |
| C–O / C–N / C–halogen | O / N / halogen (so C goes up by 1) |
| O–H / N–H | O / N (so H goes up by 1, O / N down by 1) |

The oxidation state of carbon in **methane** (CH₄) is **−4**;
in **CO₂** it's **+4**. Going from methane → methanol → formaldehyde
→ formic acid → CO₂ steps the carbon by +2 each time — exactly
the **redox ladder** used in synthesis.

## Why these three matter

- **Valence** tells you what's normal — a 5-bonded carbon is a
  hint you've drawn something wrong.
- **Formal charge** tells you where the electrostatic action is
  — which atoms are nucleophilic / electrophilic.
- **Oxidation state** tells you whether a step is a redox event
  — and what reagent class to use (NaBH₄ for reduction,
  PCC / Swern / Jones for oxidation).

## Try it in the app

- **Tools → Periodic table…** (Ctrl+Shift+T) — click each atom
  to see oxidation states + valence electron counts.
- **Molecule Workspace** → load **Aspirin** + count: are all
  C atoms tetravalent? All O atoms divalent (or marked with
  formal charge)? Practice on every molecule you load.
- **Glossary** → search for *Inductive effect* + *Polar bond* —
  these tie formal charge to electronegativity differences.

Next: **Resonance + electron delocalization** — the multi-
structure trick that explains why some bonds aren't where they
look.
