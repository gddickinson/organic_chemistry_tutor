# Retrosynthesis: Designing a Synthesis Backwards

When a chemist sees a target molecule, the practical question isn't
"what reaction did this come from?" — it's "**how would I make this from
simpler pieces that I can actually buy?**". Retrosynthesis, introduced
by E. J. Corey in the 1960s (Nobel 1990), is the formal language for
answering that question.

The key move: **work backwards**. Instead of *A + B → C*, you write
*C ⇒ A + B* (open arrow, pronounced "is made from"). Each ⇒ is a
**disconnection**. You keep disconnecting until every piece is
commercially available or trivially obtainable.

Open the **Synthesis tab** and browse the 12 seeded pathways — every
one was designed retrosynthetically. This lesson uses them as worked
examples.

## The vocabulary

- **Target molecule (TM)**: the thing you want to make.
- **Synthon**: an idealised fragment — often charged — that captures
  the *reactivity* of a piece (acyl cation⁺, enolate⁻, aryl anion⁻).
  Synthons aren't real reagents; they're thinking tools.
- **Synthetic equivalent**: a real, bench-stable reagent that
  delivers the synthon's reactivity. Acyl cation⁺ → acyl chloride.
  Enolate⁻ → ketone + LDA. Aryl anion⁻ → ArLi / ArMgBr / ArBpin.
- **Disconnection**: one step in the retro direction, converting a
  bond in the TM into two synthons.
- **FGI (functional-group interconversion)**: a non-disconnecting
  move — swap one FG for another (e.g. COOH → COCl, CHO → CH=PPh₃).
  Needed to set up a disconnectable handle.

## The three core questions at every step

1. **Where can I disconnect?** Bonds formed by *reliable* reactions
   (C=C, C–C α to C=O, amide, ester, aryl–aryl, heterocycle ring
   construction).
2. **What's the synthon on each side?** Polarity matters — one side is
   nucleophile, the other electrophile (or it's a radical/pericyclic
   disconnection).
3. **Is there a real reagent for each synthon?** If yes, write the
   forward reaction. If not, FGI first, then disconnect again.

## Worked example 1: Aspirin (1 disconnection)

**Target:** acetylsalicylic acid, `CC(=O)Oc1ccccc1C(=O)O`.

Look for a bond that a **reliable, high-yielding reaction** could have
formed. The **ester oxygen** (O–C=O) jumps out — acid + anhydride / acyl
chloride + alcohol / phenol is textbook.

    [Aspirin]  ⇒  salicylic acid  +  Ac₂O

Forward: phenol OH of salicylic acid attacks acetic anhydride; catalytic
H⁺ or base; room temperature. Seeded under **Aspirin (acetylsalicylic
acid)** in the Synthesis tab.

Salicylic acid itself is a commodity (Kolbe-Schmitt); stop here. Alternative
route: **Aspirin via Kolbe-Schmitt** (seeded) starts one disconnection
earlier — salicylic acid from phenol + CO₂. Two routes, same target — this
is typical. Students should always consider ≥ 2 disconnections and pick
on cost + atom economy + ee requirements.

## Worked example 2: Ibuprofen (the BHC green route, 3 disconnections)

**Target:** (RS)-ibuprofen, `CC(C)Cc1ccc(cc1)C(C)C(=O)O`.

The BHC Boots 1992 industrial process does this in **3 steps**, vs.
the Boots original from 1962 in 6. The seeded BHC pathway is:

    Step 1: Isobutylbenzene + Ac₂O / HF  →  4-isobutylacetophenone (FC acylation)
    Step 2: 4-isobutylacetophenone + H₂ / Raney Ni  →  4-isobutyl-1-phenylethanol
    Step 3: 4-isobutyl-1-phenylethanol + CO / Pd catalyst  →  ibuprofen

Retrosynthetically:

    Ibuprofen
        ⇒ FGI: ester / acid side chain ← CO insertion into benzylic C–OH
    4-isobutyl-1-phenylethanol
        ⇒ hydrogenation / acetophenone reduction
    4-isobutylacetophenone
        ⇒ Friedel-Crafts acylation disconnection
    Isobutylbenzene + Ac₂O

Each disconnection uses a **high-yielding, catalytic, atom-economic**
step. The atom economy of the BHC route (≈ 77 %) is one of the highest
in industrial synthesis — the seeded pathway's `pathway_green_metrics`
action reports it live.

## Worked example 3: Paracetamol (2 routes, same target)

Both routes are seeded. Compare them:

    Route A (industrial 1-step):
        Paracetamol  ⇒  4-aminophenol + Ac₂O   (acylation)
    Route B (Hoechst 3-step, from phenol):
        Paracetamol  ⇒  4-aminophenol + Ac₂O   (same last step)
        4-aminophenol  ⇒  4-nitrophenol + H₂ (reduction)
        4-nitrophenol  ⇒  phenol + HNO₃ (nitration)

Route A uses a commodity intermediate (4-aminophenol). Route B starts
from a cheaper commodity (phenol) but requires two FGIs. Industrial
decision: which raw material is cheaper right now. Pedagogically: a
reminder that **"best" depends on the cost structure at the time**.

## Worked example 4: SPPS Met-enkephalin (5 disconnections — convergent vs linear)

Peptide retrosynthesis is a special case — every amide is disconnected
back to acid + amine. The chain is built linearly from C-terminus:

    Tyr-Gly-Gly-Phe-Met (YGGFM)
        ⇒ H-Tyr + Gly-Gly-Phe-Met
        ⇒ H-Tyr + Gly + Gly-Phe-Met
        ⇒ H-Tyr + Gly + Gly + Phe-Met
        ⇒ H-Tyr + Gly + Gly + Phe + Met

In SPPS the Met is attached to the resin; each subsequent residue is
Fmoc-protected at its α-amine so the coupling is directional. The
seeded pathway walks this forward. **Retrosynthetically** the residues
are just a shopping list — which is why peptide synthesis is
algorithmic and automatable.

## The four classical disconnection strategies

1. **Carbonyl α-disconnection** (aldol condensation / Claisen
   condensation / Michael addition). Break a C–C bond α to a C=O.
   Synthons: enolate⁻ + electrophilic carbonyl⁺.  Unlocks almost
   all C–C bonds next to a carbonyl.
2. **Olefin disconnection** (Wittig reaction / Grubbs olefin
   metathesis). Break a C=C bond. Synthons: phosphorus ylide +
   aldehyde (Wittig) or alkene + alkene (metathesis).
3. **Aromatic disconnection** (EAS / Suzuki coupling /
   cross-coupling). Break a C(aryl)–X bond. Synthons: Ar⁻ + X⁺
   (for cross-coupling) or Ar-H + E⁺ (for EAS).
4. **Heteroatom disconnection (amide / ester / ether)**. Break a
   C–O–C or C–N–C bond. Synthons: acyl⁺ + heteronucleophile⁻.

Everything else is an elaboration of these four themes.

## FGI cheat-sheet

When you hit a wall — no good disconnection available at the bond you
need — try an FGI first:

| Convert | To | Reagent |
|---------|-----|---------|
| COOH | COCl | SOCl₂ or (COCl)₂ |
| COOH | CONH₂ | (COCl)₂ then NH₃, or coupling via HBTU/HATU |
| COOH | CHO | BH₃ then Swern / DIBAL |
| CHO | =CH– | Wittig |
| CHO | CN | NH₂OH then dehydration |
| C=O | C=S | Lawesson's reagent |
| CH=CH | CHOH–CHOH | OsO₄ or mCPBA then H₂O |
| OH | X (halide) | SOCl₂ / PBr₃ / Mitsunobu |
| OH | OMs | MsCl + NEt₃ |
| NH₂ | N₃ | Diazotisation or TfN₃ |
| C-H (aromatic) | C-Br | Br₂ / FeBr₃ |

Each FGI is a roundtrip ticket between functional groups that lets you
reach a disconnectable bond.

## Convergent vs. linear — a critical strategy decision

- **Linear synthesis**: A → B → C → D → E. Yield multiplies: five 80 %
  steps = 33 % overall. A late-stage failure wipes out all prior work.
- **Convergent synthesis**: (A → B → C) + (X → Y → Z) → BZ-type
  intermediate → TM. Two short branches that join late. For the same
  average step yield, convergent wins *every time* because more product
  is carried at each stage.

Almost every total synthesis with ≥ 6 steps is convergent. Our seeded
SPPS pathway is linear (peptide chains must be) but the BHC ibuprofen
route is essentially one-shot convergent on isobutylbenzene.

## Computer-aided retrosynthesis (coming in Phase 8d / 21d)

Modern tools — Chematica / SYNTHIA (Grzybowski), AiZynthFinder (AstraZeneca),
IBM RXN — walk trillions of possible trees in seconds. They disconnect
the TM with SMARTS-matched templates (millions, mined from literature)
and score each path against yield heuristics, step cost, and safety
flags.

Phase 8d of this project will ship a teaching-scale template matcher
that runs in browser-speed against the ~28 seeded reaction templates —
enough to walk a 3-step path for a typical target.

## Practice

1. In the Synthesis tab, pick a pathway you haven't seen (try **Wöhler
   urea** or **Aniline from benzene**). Open it, read the steps, then
   **close** the panel and try to write the retrosynthesis from memory.
2. Ask the tutor: "Propose two retrosynthetic disconnections for
   paracetamol and explain which is cheaper industrially."
3. The Compare tab lets you put two possible intermediates side by side
   — useful when deciding between disconnection options.
4. Use `pathway_green_metrics(pathway_id)` to score each seeded pathway's
   atom economy — the lowest-AE route is usually the one that *wouldn't*
   be chosen in a modern industrial setting.

## Further reading

- Corey, E. J. & Cheng, X.-M. *The Logic of Chemical Synthesis* (1989)
  — the classic.
- Warren & Wyatt, *Organic Synthesis: The Disconnection Approach*
  (2nd ed., 2008).
- Grzybowski et al. (2018) "Efficient syntheses of diverse, medicinally
  relevant targets planned by computer and executed in the laboratory"
  *Chem* 4, 522.

Next: **Spectroscopy (NMR / IR / MS)** — how you check that the
retrosynthesis actually delivered what you wanted.
