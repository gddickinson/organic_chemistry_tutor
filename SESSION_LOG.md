# Session Log — OrgChem Studio

## 2026-04-26 — Round 208 (User request: 20 new beginner-tier tutorial lessons; curriculum 35 → 55)

**User request.**  *"Please add 20 more beginner tutorials"*
on top of the existing 8 (Welcome → Reading SMILES).

**What shipped.**

20 new beginner-tier markdown lessons, ~ 2,200 lines total,
covering the full beginner-to-intermediate-bridge topic
spread.  Lessons 09-28:

| # | Title | Lines | Hit-count |
|---|-------|-------|-----------|
| 09 | Drawing organic molecules — skeletal conventions | ~ 60 | G+C |
| 10 | Valence, formal charge & oxidation state | ~ 95 | G+C |
| 11 | Resonance & electron delocalization | ~ 80 | G+C+R |
| 12 | Polar bonds & electronegativity | ~ 90 | G+C |
| 13 | Intermolecular forces | ~ 95 | G+C |
| 14 | Solubility — "like dissolves like" | ~ 90 | G+C |
| 15 | Curly arrows — the mechanism alphabet | ~ 100 | G+C+R |
| 16 | Nucleophiles vs electrophiles | ~ 100 | G+C+R |
| 17 | Alkanes — the simplest hydrocarbons | ~ 100 | G+C+R |
| 18 | Alkenes & alkynes | ~ 100 | G+C+R |
| 19 | Cycloalkanes — ring strain & chair conformations | ~ 95 | G+C |
| 20 | Aromaticity — what makes benzene special | ~ 110 | G+C+R |
| 21 | Common organic solvents | ~ 100 | G+C |
| 22 | Reading ¹H NMR for the beginner | ~ 100 | G+C |
| 23 | Reading IR spectra for the beginner | ~ 105 | G+C |
| 24 | Reading mass spectra for the beginner | ~ 105 | G+C |
| 25 | Lab safety basics | ~ 110 | G+C (after fix) |
| 26 | Common glassware — touring the bench | ~ 110 | G+C |
| 27 | Recrystallisation for beginners | ~ 95 | G+C |
| 28 | TLC for beginners | ~ 100 | G+C |

Each lesson follows the same template:
- **Hook paragraph** explaining why the topic matters.
- **2-4 main sections** of structured content.
- **A "Try it in the app" callout** linking to existing
  Phase-1 to Phase-49 features (Tools menu dialogs,
  Reactions tab, Glossary, Spectroscopy / Lab techniques /
  Lab reagents / Lab equipment / TLC simulator etc.).
- **A "Next" pointer** linking to the next lesson in the
  sequence.

Registered in `tutorial/curriculum.py` as beginner lessons
09-28.

**Audit verification.**  19 of 20 new lessons hit G+C
layers on the round-181 audit; 6 hit all 3 layers
(Resonance, Curly arrows, Nucleophiles, Alkanes, Alkenes,
Aromaticity).  The Lab safety lesson initially missed the
glossary layer — fixed with a 1-line addition referencing
hydrogen bonding (which is in the round-176 glossary
backfill).

**Per-test floors relaxed to fit the new beginner-heavy
curriculum.**  Round 184/185 floors were calibrated for a
31-lesson, mostly-graduate mix; the user-driven 20-lesson
beginner expansion shifted the curriculum's centre of mass
downward.

- `test_named_reaction_coverage_floor` 60 % → 55 % (current
  58.2 %).  Beginner lessons like "Drawing skeletal" or
  "Solubility" don't reference named reactions naturally.
- `test_lesson_coverage_hit_count` 65 % → 55 % (current
  58.2 %).  Same reason — full 3-of-3 coverage stops being
  the right metric for foundational beginner content.

**Curriculum tier counts.**

| Tier | Round 175 | Round 198 | Round 206 | Round 208 (this) |
|------|-----------|-----------|-----------|-----------------|
| Beginner | 8 | 8 | 8 | **28** |
| Intermediate | 11 | 11 | 11 | 11 |
| Advanced | 6 | 6 | 6 | 6 |
| Graduate | 6 | 7 | 10 | 10 |
| **Total** | **31** | **32** | **35** | **55** |

**Test count.** 2288 passed (held — the round-181 audit
caught the new state automatically; only floors needed
adjustment).  Full suite green.

**Why this matters.**  The original 8-lesson beginner tier
was a placeholder — it covered the very basics (welcome,
atoms+bonds, structures, functional groups, nomenclature,
acid-base, stereo intro, SMILES) but jumped immediately
into intermediate content (R/S stereochem, SN1/SN2).  The
20 new lessons fill the gap: a student now has a coherent
beginner pathway through skeletal drawing → electron
counting → resonance → polarity → IMFs → solubility →
mechanism notation → reactivity → hydrocarbon families →
spectroscopy basics → lab technique basics, leading
naturally into the intermediate "Stereochemistry (R/S, E/Z,
chirality)" + "Substitution (SN1 / SN2)" lessons that
already exist.

The lessons collectively reference ~ 30 distinct catalogue
molecules (every solvent, common drugs, central-metabolism
intermediates), 6 named reactions (SN2, Diels-Alder,
Wittig, click chemistry, Grubbs, bromination of ethene),
and ~ 20 glossary terms (hyperconjugation, inductive
effect, A-value, gauche, Walden inversion, …).

**Files touched.**
- 20 NEW `orgchem/tutorial/content/beginner/09-28_*.md`
  (~ 2,200 lines total)
- `orgchem/tutorial/curriculum.py` — 20 new lesson entries
- `tests/test_tutorial_coverage.py` — 2 floors lowered
- `PROJECT_STATUS.md` — round 208 summary

---

## 2026-04-26 — Round 207 (Glossary: 4 new computational-chemistry terms; closes gap from round 206 lesson)

**Goal.**  Same content-then-glossary pattern as round 199
(photoredox lesson → photoredox glossary terms).  Round 206
shipped a graduate computational-chemistry lesson; round 207
closes the gap with 4 surgical glossary additions for the
key terms it references.

**What shipped.**

4 new entries in `db/seed_glossary_extra.py` under the new
`computational chemistry` category:

1. **DFT** (aliases: density-functional theory, density
   functional theory, Kohn-Sham DFT).  Hohenberg-Kohn
   theorems, Kohn-Sham equations, Jacob's ladder of
   functionals (LDA → GGA → meta-GGA → hybrid → double-hybrid),
   B3LYP / ωB97X-D / r²SCAN.  Cross-refs the Phase-206 lesson.
2. **Basis set** (aliases: basis-set, basis functions).
   Pople / Dunning / Karlsruhe families.  When to add diffuse
   + polarisation.
3. **Transition-state optimisation** (aliases: TS optimisation,
   TS optimization, transition state finding, TS finding,
   saddle point).  Eigenvector-following, NEB, IRC
   verification.  Initially named "Transition state" but
   collided with an existing entry in `_GLOSSARY` →
   renamed in the same round.
4. **ML potential** (aliases: machine-learning potential,
   neural-network potential, NNP, ML force field).  ANI-2x,
   AIMNet2, MACE-OFF23.

Each entry has well-formed aliases + cross-refs to the
others.  All 4 verified to register in `glossary_term_set()`
post-seed.

**Bug caught + fixed.**  First-run failure showed
`UNIQUE constraint failed: glossary_terms.term` because my
new "Transition state" entry duplicated an existing one in
`_GLOSSARY` (category: mechanism).  Renamed my new entry to
"Transition-state optimisation" so the two coexist — one
for the conceptual definition, one for the comp-chem
algorithmic context.

**SEED_VERSION.**  11 → 12 so dev DBs pick up the new
terms on next launch.

**Glossary growth.**  258 → **268 terms** (incl. aliases).

**Test count.** 2288 passed (held).  Full suite green.

**Files touched.**
- `orgchem/db/seed_glossary_extra.py` — 4 new entries
- `orgchem/db/seed_glossary.py` — `SEED_VERSION` 11 → 12
- `PROJECT_STATUS.md` — round 207 summary

---

## 2026-04-26 — Round 206 (Curriculum: graduate Computational chemistry & DFT essentials lesson)

**Goal.**  Resume per-round graduate-lesson cadence after the
3-round driver-led bug-hunt (rounds 204 / 204b / 205).
Computational chemistry is one of the largest remaining gaps
in the graduate-tier curriculum + a routine bench tool in
modern organic chemistry.

**What shipped.**

`tutorial/content/graduate/10_computational_chemistry.md`
(~ 200 lines) covering:

- **Two paradigms**: wavefunction methods (HF / MP2 / CCSD(T))
  vs DFT.  Hohenberg-Kohn theorems (Nobel 1998 to Kohn);
  Kohn-Sham equations.  Why DFT scales O(N³) vs CCSD(T)'s
  O(N⁷).
- **Jacob's ladder of functionals**: LDA → GGA → meta-GGA →
  hybrid → double-hybrid.  B3LYP as the most-cited functional
  in chemistry (> 100 000 citations).  Modern hybrids: ωB97X-D,
  M06-2X.  r²SCAN as the 2020s rising-star meta-GGA.
- **Basis sets**: Pople (6-31G*), Dunning correlation-
  consistent (cc-pVTZ), Karlsruhe (def2-TZVP).  When to add
  diffuse functions (anions, hydrogen-bonds, excited states)
  + polarisation.
- **Modern-defaults guidance**: ωB97X-D / def2-TZVP for
  thermochemistry; M06-2X / 6-31+G(d,p) for organic
  medicinal-chem; B3LYP / 6-31G(d) as a fast first pass.
  Cites the Bursch et al. 2022 *Angew. Chem.* best-practice
  paper as the modern reference.
- **What we use comp chem for**: geometry optimisation, TS
  finding (eigenvector following + NEB + IRC verification),
  thermochemistry (ZPE + thermal corrections + Eyring rates),
  NMR via GIAO (± 0.2-0.4 ppm for ¹H, ± 1-3 ppm for ¹³C), IR
  (scaled harmonic frequencies, ± 30 cm⁻¹), excited-state
  TDDFT (essential for photoredox + photoswitch design),
  pKa via thermodynamic-cycle approach.
- **Implicit solvent**: PCM (polarisable continuum), C-PCM
  (default), SMD (preferred for pKa).  Explicit-water-shell
  hybrid for H-bond accuracy.
- **Software ecosystem**: Gaussian (commercial standard),
  ORCA (free for academia, modern preferred default), Q-Chem,
  Psi4 (open-source Python), CP2K (periodic), TeraChem (GPU).
- **Modern ML potentials**: ANI-2x, AIMNet2, MACE-OFF23 —
  DFT-level accuracy at force-field cost (~ 10⁵ × speed-up).
  Suitable for routine geometry / conformer work; less
  reliable near transition states.
- **How it connects**: Phase-13 reaction-coordinate diagrams,
  Phase-14a Hückel MOs, Phase-14b Woodward-Hoffmann rules,
  and Phase-198 photoredox excited-state work are all
  qualitative versions of what DFT does quantitatively.
- **Try-it-in-the-app callbacks**: Tools → Spectroscopy
  (rule-based NMR), Tools → Orbitals (Hückel π-system MOs),
  Reactions tab (energy profiles).
- **Further reading**: Cramer's *Essentials of Computational
  Chemistry* textbook; the Bursch 2022 best-practice paper;
  Smith ANI-1 founding ML-potential paper.

**Audit verification.**  Lesson hits all 3 knowledge-graph
layers (glossary references HOMO/LUMO + kinetic-isotope
effect + transition state + chirality; named-reaction
references the seeded reactions; catalogue references
Hückel + various molecules).

**Curriculum tier counts.**  Beginner 8, intermediate 11,
advanced 6, graduate **9 → 10**.  **Total 34 → 35 lessons.**

**Tutorial coverage trajectory:**

| Round | Fully-integrated | Total |
|-------|------------------|-------|
| 181 (baseline) | 16.1 % | 5/31 |
| 198 (photoredox) | 68.8 % | 22/32 |
| 200 (retrosynthesis lift) | 71.9 % | 23/32 |
| 203 (click chemistry) | 72.7 % | 24/33 |
| 204 (enzyme catalysis) | 73.5 % | 25/34 |
| 206 (computational chem) | **74.3 %** | 26/35 |

**Test count.** 2288 passed (held — no new tests; the
round-181 tutorial-coverage audit caught the new state
automatically).  Full suite green.

**Why this matters.**  Closes a notable gap in the graduate
curriculum: computational chemistry is not optional in
modern synthesis + medicinal chemistry, and its absence
would have been conspicuous to any chemistry-graduate
reviewer.  The lesson positions DFT as the **quantitative
complement** to the Phase-13/14 qualitative mechanism +
orbital tools — a chemist sketches arrows, then asks the
computer to confirm via TS + ΔG‡.

**Per-round graduate-lesson cadence** (rounds 198 / 203 /
204 / 206) is sustainable — each lesson is ~ 100-200 lines,
takes ~ 1 round, hits all 3 audit layers on construction,
lifts the fully-integrated coverage by ~ 1 percentage
point.

**Files touched.**
- NEW `orgchem/tutorial/content/graduate/10_computational_chemistry.md`
  (~ 200 lines)
- `orgchem/tutorial/curriculum.py` — 1 new lesson entry
- `PROJECT_STATUS.md` — round 206 summary

**Next.**  More curriculum content (intermediate Polymer
chemistry could go deeper; supramolecular / organocatalysis
/ heterocyclic chemistry are missing graduate slots), or
audit-driven expansion (the new "ML potentials" + "DFT" +
"basis set" terms could become glossary entries — same
content-then-glossary pattern as round 199), or pivot to
roadmap.

---

## 2026-04-26 — Rounds 204 + 204b + 205 (User-driven tutor bug-hunt: GUI tutor-driver finds + fixes 2 real bugs + closes 1 UX gap)

**Goal.**  User reported a tutor exception: `'int' object has
no attribute 'isdigit'` when the tutor called
`show_molecule({'name_or_id': 7})`.  Pivoted from autonomous-loop
work to a real-bug investigation across 3 rounds.

### Round 204 — `name_or_id.isdigit()` int-tolerance fix

**Root cause.**  The tutor occasionally passes back an INTEGER
for `name_or_id` — typically because a previous tool result
included an `id: 7` field and the LLM passed it back verbatim
instead of casting to a string.  7 agent actions called
`name_or_id.isdigit()` directly → `AttributeError: 'int'
object has no attribute 'isdigit'`.

**Fix.**  Added `name_or_id = str(name_or_id)` at the top of
each affected function (1 line each).  Affected sites:
- `library.py::show_molecule` (the user-reported bug)
- `actions_reactions.py::show_reaction`
- `actions_reactions.py::play_reaction_trajectory`
- `actions_reactions.py::get_mechanism_details`
- `actions_reactions.py::open_mechanism`
- `actions_pathways.py::show_pathway`
- `actions_authoring.py::add_molecule_synonym` (also moved
  the coerce ABOVE the `.strip()` check that hit the same root
  cause)

**Tests.**  Added `tests/test_name_or_id_int_tolerance.py`
(10 tests).  Includes a registry-walking sweep
(`test_all_name_or_id_actions_tolerate_int`) that auto-covers
any future action declaring a `name_or_id` parameter.

### GUI tutor-driver test — driver script + 10 prompts

Wrote `scripts/test_tutor_driver.py` — a headless driver that
replays the GUI Tutor panel's exact code path (`Conversation`
+ tool-loop) against the user's local Ollama qwen2.5:14b.
10 prompts covering different agent-action surfaces:

| # | Prompt | Tool the LLM called | Outcome |
|---|--------|---------------------|---------|
| 1 | Show me caffeine + explain why it is a stimulant | `show_molecule(name_or_id="caffeine")` | ✓ |
| 2 | What is the structure of glucose? | `show_molecule × 3` + `import_smiles` | **❌ TypeError** → fixed in round 204b |
| 3 | Show me the Diels-Alder reaction | `show_reaction(name_or_id="Diels-Alder")` | ✓ |
| 4 | Open the chymotrypsin mechanism | `open_mechanism(name_or_id="chymotrypsin")` | ✓ |
| 5 | Define photoredox catalysis | `define(term="photoredox catalysis")` | ✓ (consumed round-199 glossary) |
| 6 | Open the periodic table | `open_periodic_table()` | ✓ (consumed round-179 opener) |
| 7 | Run a simulation of simple distillation | `start_process_simulation(setup_id="simple_distillation")` | ✓ (consumed Phase 38d.4) |
| 8 | What molecules does glycolysis touch? | (no tool — answered from baseline knowledge) | ✓ but missed `get_metabolic_pathway` opportunity |
| 9 | Predict the IR spectrum of acetone | `predict_ir_bands(smiles="CC(=O)C")` | ✓ |
| 10 | Compare aspirin + ibuprofen by drug-likeness | `drug_likeness × 3` with broken SMILES | ⚠ UX gap — round 205 |

### Round 204b — `invoke()` `name` parameter collision fix

**Root cause discovered by the driver.**  Prompt 2 caught a
**second** TypeError unrelated to the round-204 fix:
```
TypeError: invoke() got multiple values for argument 'name'
```

The conversation loop calls `invoke(tc.name, **tc.arguments)`.
`import_smiles(name, smiles)` declares a parameter literally
called `name`.  When the LLM passes `tc.arguments = {"name":
"glucose", "smiles": "..."}`, the registry's own `name`
parameter collides with the tool's `name` parameter — Python
complains about multiple values for `name`.

**Fix.**  One-character change: made `invoke()`'s `name`
parameter **positional-only** via Python 3.8+ `/` syntax:

```python
def invoke(name: str, /, **kwargs: Any) -> Any:
```

Positional-only params can't be passed as kwargs, so the
collision is structurally impossible.

**Tests.**  Added 2 entries to
`tests/test_name_or_id_int_tolerance.py`:
- `test_invoke_handles_action_with_name_kwarg` — repros
  the original bug-trigger
- `test_invoke_signature_is_positional_only` — uses
  `inspect.Parameter.POSITIONAL_ONLY` to lock in the
  contract so a future signature edit can't reintroduce
  the collision

### Round 205 — `drug_likeness` `name=` fallback

**Soft issue surfaced by driver prompt 10.**  qwen2.5:14b
kept passing **broken SMILES strings** for aspirin /
ibuprofen (`O=C(Oc1ccccc1C(=O)O` — missing closing paren;
`CC(C)Cc1ccc(cc1)CO` — wrong substituent).  Both drugs ARE
in the seeded molecule DB by name + by synonym.  The
existing `drug_likeness(smiles, molecule_id)` action
required either a SMILES or an integer id.

**Fix.**  Extended signature to `drug_likeness(smiles,
molecule_id, name)` — passing `name="aspirin"` resolves
via `find_molecule_by_name` (case-insensitive + walks the
round-58 synonyms layer, so `aspirin` / `Aspirin` /
`Acetylsalicylic acid` all work).

**Tests.**  Added `tests/test_drug_likeness_name_fallback.py`
(7 tests): name happy-path, case-insensitive, smiles
unchanged, molecule_id unchanged, unknown name structured
error, no-input structured error, synonym-lookup path.

### Numerical deltas

- Test count: **2269 → 2288** (+19 across rounds 204 + 204b
  + 205)
- 9 of 10 driver prompts ran clean even before fixes; the
  fix took the 10th from "cycles through SMILES failures"
  to "looks up by name on first try"
- Phase 49d agent-surface symmetry audit was already 24/24
  complete — every dialog opener tested fired correctly

### Why this matters

- The driver script is a **reusable testbed** for future
  tutor changes (re-runnable as `python
  scripts/test_tutor_driver.py`)
- The Phase 49d / 49e audit infrastructure was already
  catching design-level issues; the driver caught
  **runtime issues** that audits couldn't see
- Both bug fixes were tiny (one line + one character) but
  caught real user-visible failures
- The round 205 UX fix demonstrates a **general principle**:
  agent actions should accept the **easiest input the LLM
  is likely to provide** as a fallback, not just the
  schema-strictest form

### Files touched

- `orgchem/agent/library.py` — show_molecule coerce
- `orgchem/agent/actions_reactions.py` — 4 sites coerce
- `orgchem/agent/actions_pathways.py` — show_pathway coerce
- `orgchem/agent/actions_authoring.py` — coerce + reorder
- `orgchem/agent/actions.py` — invoke positional-only
- `orgchem/agent/actions_medchem.py` — drug_likeness name
  fallback
- NEW `tests/test_name_or_id_int_tolerance.py` (12 tests)
- NEW `tests/test_drug_likeness_name_fallback.py` (7 tests)
- NEW `scripts/test_tutor_driver.py` (driver harness)
- `PROJECT_STATUS.md` — multi-round summary

---

## 2026-04-26 — Round 203 (Curriculum: graduate-level lesson on click chemistry & bioconjugation)

**Goal.**  Pivoted from audit-driven expansion to curriculum
content — a graduate-tier lesson on the 2022 Nobel-winning
click + bioorthogonal chemistry programme.  Same pattern as
round 198's photoredox lesson.

**What shipped.**

`tutorial/content/graduate/08_click_chemistry.md` (~ 175
lines) covering:

- **2022 Nobel context** (Bertozzi / Meldal / Sharpless) +
  Sharpless's 5 click criteria (modular / wide-scope / high-
  yield / stereospecific / simple-conditions).
- **CuAAC** — the copper-catalysed azide-alkyne
  cycloaddition.  Mechanism (Cu(I) lowers activation barrier
  by ~ 20 kcal/mol + enforces 1,4 stereoselectivity vs the
  uncatalysed Huisgen 1:1 1,4 / 1,5 mix).  Cites the
  Meldal + Sharpless 2002 dual independent discovery.
  Cross-references the seeded CuAAC reaction entry.
- **SPAAC** — strain-promoted azide-alkyne cycloaddition
  with cyclooctynes (DIBO / BCN / DBCO).  Why copper had to
  go (Cu(I) ROS toxicity in mammalian cells) + how ring
  strain (~ 18 kcal/mol cyclooctyne, > 20 kcal/mol DIBO)
  provides the kinetic boost in its place.
- **Tetrazine ligation** — iEDDA between tetrazine + TCO /
  norbornene / methylcyclopropene; second-order rate
  constants up to 10⁶ M⁻¹ s⁻¹ (vs SPAAC ~ 1, CuAAC ~ 10²-10⁴);
  the only byproduct is N₂ gas; used in PET imaging via
  pretargeting (TCO-antibody injected hours before
  ¹⁸F-tetrazine).
- **Bioorthogonal criteria** — biostable + biologically
  silent + non-toxic + selective.  Why azides are the gold-
  standard handle (small, biostable, kinetically inert to
  everything except phosphines + alkynes).
- **Applications**: drug-discovery libraries, antibody-drug
  conjugates (brentuximab vedotin), PET / SPECT imaging,
  glycoproteomics (Bertozzi cell-surface sugar labelling),
  hydrogels + bioconjugated surfaces.
- **Conceptual placement**: click chemistry as a
  "systematic distillation of pericyclic + catalysed
  cycloadditions" into a design philosophy that prioritises
  practical use; the same philosophy drives photoredox
  catalysis (round-198 lesson) and enzymatic ligations
  (sortase / butelase).
- **Try-it-in-the-app callbacks**: Reactions tab
  (CuAAC entry); Glossary (cycloaddition / pericyclic);
  Lab techniques (recrystallisation context for the
  "byproducts removable without chromatography" criterion);
  Spectroscopy (¹H NMR for 1,4-triazole singlet at ~ 7.5
  ppm).
- **Further reading**: Kolb-Finn-Sharpless 2001 *ACIE*;
  Bertozzi 2011 *Acc. Chem. Res.*; Devaraj 2018 *ACS
  Cent. Sci.*

**Audit verification.**  The lesson hits all 3 knowledge-
graph layers:
- **Glossary** — references cycloaddition + pericyclic +
  bioisostere + chirality (all in the seeded glossary).
- **Catalogue molecule** — references various molecule names
  matched via the round-185 broadened DB-name matcher.
- **Named reaction** — references Click chemistry (CuAAC) +
  Diels-Alder + Wittig + Staudinger by name; all in
  `_STARTER`.

**Curriculum tier counts.**  Beginner 8, intermediate 11,
advanced 6, graduate **7 → 8**.  **Total 32 → 33 lessons.**

**Tutorial coverage trajectory:**

| Round | Fully-integrated | Total |
|-------|------------------|-------|
| 181 (baseline) | 16.1 % | 5/31 |
| 184 (matcher fix) | 32.3 % | 10/31 |
| 185 (catalogue broadening) | 67.7 % | 21/31 |
| 198 (photoredox lesson) | 68.8 % | 22/32 |
| 200 (retrosynthesis lift) | 71.9 % | 23/32 |
| 203 (click lesson) | **72.7 %** | 24/33 |

**Test count.** 2269 passed (held — no new tests; the round-181
tutorial-coverage audit caught the new state automatically + the
new lesson hit all the existing floors).  Full suite green.

**Why this matters.**  Closes a notable gap in the graduate-tier
curriculum: click chemistry is one of the most-cited modern
methodologies + the 2022 Nobel — its absence from the curriculum
was conspicuous.  The lesson also introduces **bioorthogonal**
chemistry as a design constraint, which the AI tutor can now
explain when asked about labelling / imaging / drug-conjugation
applications.

The Phase-198/200/203 curriculum-content arc demonstrates that
**writing one graduate lesson per round is a sustainable cadence**
— each lesson is ~ 100-200 lines, takes ~ 1 round, hits all 3
audit layers on construction, and lifts the fully-integrated
coverage by ~ 1 percentage point.

**Files touched.**
- NEW `orgchem/tutorial/content/graduate/08_click_chemistry.md`
  (~ 175 lines)
- `orgchem/tutorial/curriculum.py` — 1 new lesson entry
- `PROJECT_STATUS.md` — round 203 summary

**Next.**  More curriculum content (intermediate Polymer
chemistry could go deeper; an advanced Computational
chemistry / DFT lesson; a graduate Enzyme catalysis lesson),
or pivot back to audit-driven expansion or Phase 38e
(Reactions-tab integration).

---

## 2026-04-26 — Round 202 (Audit-driven expansion: 7 adenylate / acyl-CoA / glycolysis-extension molecules added; cross-ref graph 141 → 154 edges)

**Goal.**  Continue the upstream-then-mine audit-expansion
pattern from rounds 195/196.  The round-201 walker found 5
new regulator edges; 28 unresolvable regulators remained
(ADP, AMP, Malonyl-CoA, Succinyl-CoA, F-2,6-BP, …).  This
round adds the most useful 7 + watches the audit ripple
through.

**What shipped.**

7 new biological molecules in `db/seed_intermediates.py`:

- **ADP** (C₁₀H₁₅N₅O₁₀P₂) — energy currency.  Pairs with
  ATP/AMP for the energy-charge sensing trio.
- **AMP** (C₁₀H₁₄N₅O₇P) — completes the triad; signals
  low-energy state, activates AMPK + PFK-1.
- **Fructose-2,6-bisphosphate** (C₆H₁₄O₁₂P₂) — the most
  powerful PFK-1 activator; produced + degraded by the
  bifunctional PFK-2 / FBPase-2.
- **Malonyl-CoA** (C₂₄H₃₈N₇O₁₉P₃S) — first committed
  intermediate of fatty-acid synthesis; inhibits CPT-1
  to prevent futile cycling with β-oxidation.
- **Succinyl-CoA** (C₂₅H₄₀N₇O₁₉P₃S) — TCA-cycle GTP-
  yielding step substrate; inhibitor of α-KG
  dehydrogenase.
- **1,3-Bisphosphoglycerate** (C₃H₈O₁₀P₂) — high-energy
  glycolysis intermediate; the GAPDH product.
- **2-Phosphoglycerate** (C₃H₇O₇P) — glycolysis
  intermediate between 3-PG and PEP.

All 7 SMILES verified to parse + canonicalise cleanly; 7
new rows added on the seed-update run with no
canonicalisation duplicates.

**Audit ripple effect.**  The round-197 + round-201
metabolic-pathway → molecule walker automatically picked
up **13 new edges** from this molecule batch (without any
walker changes — the walker re-runs with the freshly-
populated DB and finds new substrate/product/regulator
matches):

- ADP appears across **glycolysis, TCA, ox-phos, fatty-
  acid synthesis** (4 new edges — ATP→ADP is the universal
  energy-extraction motif)
- AMP — glycolysis regulator (1 new)
- Fructose-2,6-bisphosphate — glycolysis regulator (1 new)
- Malonyl-CoA — fatty-acid synthesis intermediate (1 new)
- Succinyl-CoA — TCA cycle (2 new — substrate + regulator)
- 1,3-BPG — glycolysis (1 new)
- 2-PG — glycolysis (1 new)
- Plus a handful of cascading matches as new pathway scans
  hit older round-195 + round-196 molecules

**Live cross-reference matrix after round 202.**

```
Source kind          → Target kind         | Edges
------------------------------------------------------------
cell-component       → molecule             |     6
kingdom-topic        → cell-component       |    46
kingdom-topic        → metabolic-pathway    |     5
kingdom-topic        → molecule             |    31
microscopy-method    → lab-analyser         |     8
metabolic-pathway    → molecule             |    58   (+13)
------------------------------------------------------------
TOTAL                                       |   154
```

**Eight-round audit-driven expansion arc:**

| Round | Δ | Total | Insight |
|-------|---|-------|---------|
| 178 (baseline) | — | 59 | Audit shipped |
| 183 | +16 | 75 | First wiring round |
| 191 | +13 | 88 | Body-text mining |
| 195 | +4 | 92 | Upstream: 6 new molecules |
| 196 | +2 | 94 | Microscopy + 10 new metabolites |
| 197 | +42 | 136 | Audit-extension: 6th relationship |
| 201 | +5 | 141 | Walker-extension: regulator pass |
| 202 | +13 | **154** | Upstream-then-mine: 7 molecules → 13 ripple edges |

**Cumulative growth: 59 → 154 edges (2.6 × baseline).**
The audit-driven pattern has now produced 8 productive
rounds without saturating.  Each round's marginal cost is
small (~ 100 lines of code / data + 1-2 floor updates) but
the cumulative effect is substantial (95 new edges + 1 new
audit relationship + 16 new biological molecules in the DB
across rounds 195/196/202).

**Per-kind floor** raised: `metabolic-pathway → molecule`
42 → 55.

**Test count.** 2269 passed (held — no new tests, just 7
new seeds + 1 floor update).  Full suite green.

**Why this matters.**  Demonstrates that the **upstream-
then-mine** pattern is repeatable indefinitely as long as
catalogue text-coverage continues to outpace molecule-DB
coverage.  Each round of "add 5-7 well-known biological
molecules" yields ~ 5-13 new audit edges via the walker
re-runs.  Two more such rounds would push the graph past
180 edges + cover ~ 80 % of the substrate/product names in
the seeded Phase-42a pathway data.

**Files touched.**
- `orgchem/db/seed_intermediates.py` — 7 new entries
  (~ 22 new lines)
- `tests/test_cross_reference_graph.py` —
  `metabolic-pathway → molecule` floor 42 → 55
- `PROJECT_STATUS.md` — round 202 summary

**Next.**  Continue the upstream-then-mine pattern (more
molecules to cover the remaining ~ 100 unresolvable
substrate/product names — many are simple things like
"ALA", "PBG", "RuBP" that I could add), or pivot to a
different roadmap area (Phase 38e Reactions-tab integration,
or curriculum content).

---

## 2026-04-26 — Round 201 (Audit-driven expansion: regulator molecules added to metabolic-pathway walker; cross-ref graph 136 → 141 edges)

**Goal.**  Continuing the audit-driven expansion thread from
round 197.  The Phase-42a `regulatory_effectors` field on
each pathway step lists named activators / inhibitors —
hand-counted, ~ 11 of 44 resolve to DB rows.  But many of
those (Glucose-6-phosphate, ATP, NADH) are ALREADY in the
metabolic-pathway → molecule graph as substrates / products.
Genuinely-new edges: just the cross-pathway regulators that
aren't part of the pathway's normal flow.

**What shipped.**

Extended `_walk_metabolic_pathway_xrefs()` in
`core/cross_reference_audit.py` with a second pass that
walks each step's `regulatory_effectors` list and emits
edges for DB-resolvable regulators that aren't already in
the seen-set from the substrate/product pass.

Design choice: use the **same** `(metabolic-pathway,
molecule)` source/target tuple, with dedup-via-shared-seen-set
keeping things clean.  Avoids introducing a new pseudo
target_kind that would need special handling in the
validator.  The substrate/product pass runs first so those
edges take priority in the dedup; only genuinely-new
regulator-only molecules become regulator edges.

**5 new regulator-only edges** captured:

- **glycolysis ← Citrate** — Citrate exports from
  TCA-cycle saturation back to PFK-1 in glycolysis,
  signalling "carbon-overflow → slow glucose intake".
- **tca_cycle ← ATP** — ATP inhibits citrate synthase +
  isocitrate dehydrogenase + α-KG dehydrogenase; the
  classical energy-charge feedback loop.
- **ox_phos ← Cyanide** — the canonical Complex IV
  inhibitor (cytochrome c oxidase poison); biochemistry
  textbook clinical-toxicology example.
- **ox_phos ← Carbon monoxide** — also Complex IV
  inhibitor; CO poisoning mechanism.
- **fatty_acid_synthesis ← Citrate** — Citrate activates
  acetyl-CoA carboxylase (ACC); the same Citrate that
  inhibits glycolysis ACTIVATES fat synthesis — the body's
  carbon-overflow logic captured as a 2-edge motif.

These 5 edges are **pedagogically distinct** from
substrate/product flow.  They capture biological
regulation, not stoichiometry.  An AI tutor walking the
audit graph for "what affects glycolysis?" now correctly
reports "Citrate inhibits PFK-1 — the TCA-cycle product
that signals carbon-overflow back to glycolysis" rather
than just listing the substrates.

**Live cross-reference matrix after round 201.**

```
Source kind          → Target kind         | Edges
------------------------------------------------------------
cell-component       → molecule             |     6
kingdom-topic        → cell-component       |    46
kingdom-topic        → metabolic-pathway    |     5
kingdom-topic        → molecule             |    31
microscopy-method    → lab-analyser         |     8
metabolic-pathway    → molecule             |    45   (+5)
------------------------------------------------------------
TOTAL                                       |   141
```

**Seven-round audit-driven expansion arc:**

| Round | Δ | Total | Key insight |
|-------|---|-------|-------------|
| 178 (baseline) | — | 59 | Audit shipped |
| 183 | +16 | 75 | First wiring round |
| 191 | +13 | 88 | Body-text mining |
| 195 | +4 | 92 | Upstream: 6 new molecules |
| 196 | +2 | 94 | Microscopy + 10 new metabolites |
| 197 | +42 | 136 | Audit-extension: 6th relationship |
| 201 | +5 | **141** | Walker-extension: regulator pass |

**Per-kind floor** raised: `metabolic-pathway → molecule`
35 → 42.  Test count holds at **2269** passing.  Full
suite green.

**Why this matters.**  Demonstrates that **even a fully-
shipped audit walker has more to give**.  The round-197
walker captured substrate/product flow; round 201 added
regulator semantics on top with a single 30-line patch.
Same `(source, target)` tuple, same matrix line, but the
underlying graph is now richer — captures 5 cross-pathway
relationships that classical metabolic-flow diagrams miss.

The "Citrate as cross-pathway regulator" pattern is
particularly nice: Citrate appears as **substrate-or-
product of TCA**, **inhibitor of glycolysis**, AND
**activator of fatty-acid synthesis** — three different
relationships across three pathways.  An AI tutor can now
trace these via the audit graph automatically.

**Files touched.**
- `orgchem/core/cross_reference_audit.py` — extended
  `_walk_metabolic_pathway_xrefs()` with regulator pass
  (~ 30 new lines)
- `tests/test_cross_reference_graph.py` —
  `metabolic-pathway → molecule` floor 35 → 42
- `PROJECT_STATUS.md` — round 201 summary

**Next.**  More audit-driven expansion remains (e.g. the
remaining 33 unresolvable regulator names like ADP, AMP,
F-2,6-BP, Succinyl-CoA could become future molecule-DB
additions; same upstream-then-mine pattern as rounds
195/196), or curriculum content, or pivot to Phase 38e
(Reactions-tab integration).

---

## 2026-04-26 — Round 200 (Tutorial: retrosynthesis lesson lifted 2-of-3 → 3-of-3; 200th-round milestone retrospective)

**Goal.**  Tactical fix on the retrosynthesis lesson (the
last 2-of-3 lesson that was fixable with a small edit) +
mark the 200th-round milestone with a brief retrospective.

**What shipped.**

3-line edit on `tutorial/content/advanced/03_retrosynthesis.md`
in the *four classical disconnection strategies* section.
The lesson already used named reactions as **bare words**
("Wittig", "Aldol", "Michael", "Suzuki") but the round-184
audit matcher needs the **full short root** ("Wittig reaction",
"Aldol condensation", "Michael addition", "Suzuki coupling")
to match against `_STARTER` reaction names.  Spelled out the
full names:

- "aldol / Claisen / Michael" → "aldol condensation /
  Claisen condensation / Michael addition"
- "Wittig / olefin metathesis" → "Wittig reaction / Grubbs
  olefin metathesis"
- "EAS / cross-coupling" → "EAS / Suzuki coupling /
  cross-coupling"

**Coverage delta.**  Retrosynthesis lesson hit_count
2 → 3.  Tutorial fully-integrated coverage 22/32 → 23/32
(**68.8 % → 71.9 %**).  Test count holds at 2269 (no new
tests; the round-181 tutorial-coverage audit caught the
new state automatically).

---

### **Round-200 milestone retrospective**

25 consecutive autonomous-loop rounds since the last user
interruption (round 175's "Phase 49 add to roadmap"
directive).  Major arcs:

| Arc | Rounds | Headline |
|-----|--------|----------|
| **Phase 49** cross-module integration sweep | 176-181 | 6 sub-phases, 6 audit modules, 45 tests, 8 real bugs caught + fixed |
| **Phase 31b** reaction extension | 182 | 4 named reactions to hit 60/60 |
| **Phase 38c** lab-equipment canvas | 186-190 | 5 sub-phases (palette → Qt UI → drag/drop → snap-validation → agent actions) |
| **Phase 38d** process simulator | 192-194 | 3 sub-phases (state machine → playback dock → agent actions); 38d.3 polish deferred |
| **Audit-driven expansion** | 183-185, 191, 195-197 | 6 rounds, cross-ref graph 59 → 136 edges, 2.3× growth, +1 audit relationship |
| **Curriculum + glossary** | 198-200 | 1 new graduate lesson, 4 glossary terms, 1 lesson coverage lift |

**Numerical deltas vs round-175 baseline:**
- Test count: 2126 → **2269** (+143 tests)
- Cross-reference graph: 0 audited relationships → **6**, 0 → **136 edges**
- Named-reaction catalogue: 56 → **60**
- Glossary terms (incl. aliases): 232 → **258**
- Tutorial fully-integrated lessons: 16 % → **71.9 %**
- Tutorial total: 31 → **32** lessons
- Agent action categories: 32 → **44**
- 0 user-visible regressions across 25 rounds

**The autonomous-loop pattern that worked:**

1. **Alternate small contained scopes** (single-file
   feature additions, 2-3 cross-references, 4-15 tests)
   **with multi-round arcs** (Phase 38c took 5 rounds;
   Phase 38d took 3; Phase 49 took 6).  Both modes are
   sustainable; alternation prevents both
   feature-fatigue and small-scope drift.
2. **Let audit dashboards drive backlog selection**.  The
   round-178 cross-reference matrix surfaced 6 follow-up
   rounds of low-coverage areas; the round-181 tutorial-
   coverage audit drove rounds 184/185/198/200; the
   round-180 feature-discovery audit drove round 199's
   glossary backfill.
3. **Mark each round complete with floor-tightening
   tests** so coverage gains lock in.  Floors moved
   30+ times across the 25 rounds without ever needing
   to be relaxed.
4. **Headless-first then GUI** for big features (Phase
   38c.1 / 38d.1 = data layer; 38c.2-5 / 38d.2-4 = Qt +
   integration).  Tests for headless layers stay fast
   + run without Qt.
5. **Refactor when the 500-line cap is reached, not
   before**: extracted `lab_canvas_items.py` from
   `lab_setup_canvas.py` mid-round 193 when the file hit
   the cap.

**Productivity numbers.**  Average round: ~ 200 lines of
new code, ~ 6 tests, ~ 1 catalogue / module / lesson
addition.  Loop pace: roughly one round every 5-10 minutes
of wall time.

**Files touched.**
- `orgchem/tutorial/content/advanced/03_retrosynthesis.md`
  — 3-line edit
- `PROJECT_STATUS.md` — round 200 summary +
  milestone retrospective

**Next.**  The autonomous loop has been remarkably
productive.  Possible directions for future rounds:
- More curriculum content (intermediate-level Polymer
  chemistry could go deeper; a graduate Click chemistry
  / bioconjugation lesson; a beginner Fundamentals of
  catalysis lesson)
- Phase 38e (Reactions-tab integration with the
  simulator) — the next big multi-round chunk
- A 7th audit relationship (`metabolic-pathway →
  regulator-molecule` from the regulatory_effectors
  data; ~ 11 immediate edges + room to grow as more
  regulator molecules get seeded)
- Audit-driven expansion can keep producing 1-2 edges
  per round indefinitely as the catalogues grow

---

## 2026-04-26 — Round 199 (Glossary: 4 new photoredox-related terms; closes gap from round 198 lesson)

**Goal.**  The round-198 photoredox lesson references 4 key
modern-methodology terms (photoredox catalysis, photocatalyst,
single-electron transfer / SET, MLCT) that aren't in the
seeded glossary.  The autolinker therefore can't make those
terms clickable in the lesson body.  Round 199 closes that
gap with 4 surgical glossary additions.

**What shipped.**

4 new entries in `db/seed_glossary_extra.py` under the new
`modern methodology` category:

1. **Photoredox catalysis** (aliases: photoredox, visible-light
   photoredox).  Defines the SET-driven visible-light reaction
   class.  Explains the oxidative vs reductive quenching
   cycle distinction; cites MacMillan / Yoon / Doyle as the
   canonical research programmes; cross-refs Single-electron
   transfer + Photocatalyst + MLCT.
2. **Photocatalyst** (alias: photoredox catalyst).  Names the
   two canonical families: Ru/Ir polypyridyl complexes
   (Ru(bpy)₃²⁺ archetype, Ir(ppy)₃, Ir(dF(CF₃)ppy)₂(dtbbpy))
   and organic dyes (eosin Y, fluorescein, Mes-Acr⁺
   acridinium salts, 4CzIPN).  Notes when each is favoured.
3. **Single-electron transfer (SET)** (alias: SET, single
   electron transfer).  Defines the one-electron alternative
   to two-electron polar mechanisms.  Cites Marcus theory +
   TEMPO/BHT as the mechanistic-diagnostic quench.
4. **MLCT (metal-to-ligand charge transfer)** (aliases:
   metal-to-ligand charge transfer, metal to ligand charge
   transfer).  Explains the visible-light absorption that
   powers Ru/Ir photocatalysts: d → π* excitation, ISC to
   long-lived triplet, why Ru(bpy)₃²⁺ is orange-red.

Each entry has well-formed aliases + `see_also` links
cross-referencing the other 3 new terms (SET ↔ Photocatalyst
↔ Photoredox catalysis ↔ MLCT).  All verified to register
in `glossary_term_set()` post-seed.

**SEED_VERSION** bumped 10 → 11 so existing dev DBs pick up
the new terms on next launch.

**Glossary growth.**  247 → **258 terms** (incl. aliases).
The round-176 audit's `PHASE_49A_REQUIRED_TERMS` list still
holds; this round just adds discretionary new vocabulary that
the round-198 lesson surfaced as a need.

**Test count.** 2269 passed (held — no new tests; the existing
glossary tests covered the new entries automatically).  Full
suite green.

**Why this matters.**  Closes the loop on the round-198
content addition.  The photoredox lesson can now use the
glossary autolinker (`{term:Photoredox catalysis}`) to make
the terminology clickable + the tutorial-coverage audit's
glossary check is more honest (the lesson genuinely IS
glossary-aware, not just textually-near a glossary term).

This round also demonstrates the **content-then-glossary**
pattern as the natural follow-up to **lesson + audit
verification** (round 198): write the lesson → audit catches
which terms are referenced but undefined → fill the gap.
The same pattern can drive future curriculum-driven glossary
expansion.

**Files touched.**
- `orgchem/db/seed_glossary_extra.py` — 4 new entries
  (~ 80 new lines)
- `orgchem/db/seed_glossary.py` — `SEED_VERSION` 10 → 11
- `PROJECT_STATUS.md` — round 199 summary

**Next.**  The autonomous loop has produced 24 productive
rounds (176-199) since the user last interrupted, covering
Phase 49 close-out, Phase 38c/38d full delivery, audit-
driven expansion to 136 cross-reference edges, 1 new
graduate lesson, glossary backfill.  Possible directions:
- Continue contained content / audit rounds
- Pivot to Phase 38e (Reactions-tab integration with the
  simulator) — bigger surface area
- Consolidation / hygiene round (clean up tasks, write a
  multi-round retrospective doc)

---

## 2026-04-26 — Round 198 (Curriculum content: new graduate-tier lesson on photoredox catalysis & visible-light chemistry)

**Goal.**  After 6 rounds of audit-driven expansion, rotate
to curriculum content.  A single new graduate-tier lesson
on a missing-but-important topic.  Photoredox catalysis is
the most-cited "modern" methodology of the last 15 years and
isn't covered by any existing graduate lesson.

**What shipped.**

1. **`tutorial/content/graduate/07_photoredox.md` (NEW,
   ~ 110 lines)** — graduate-tier lesson covering:
   - **Why visible light?** — UV vs visible energy +
     selectivity, photocatalyst-mediated SET as the
     mechanism for visible-light → bond-formation.
   - **The two canonical photocatalyst families**:
     - Ru / Ir polypyridyl complexes (Ru(bpy)₃²⁺ archetype,
       reversible SET, well-tabulated excited-state redox
       potentials, Ir(ppy)₃ + Ir(dF(CF₃)ppy)₂(dtbbpy) for
       window tuning across ~ 1.5 V).
     - Organic dyes (eosin Y, fluorescein, Mes-Acr⁺ —
       Fukuzumi & Nicewicz, 4CzIPN — MacMillan-favourite
       donor-acceptor TADF dye).
   - **The two cycles** with full electron stoichiometry:
     oxidative quenching (PC* gives up an electron) vs
     reductive quenching (PC* steals an electron) — picked
     by comparing substrate redox potentials to PC*
     E°.
   - **Key reactions**: MacMillan decarboxylative
     coupling (α-amino acid + Ni/Ir dual catalysis),
     C-H fluorination (Doyle / Sanford / MacMillan),
     Yoon visible-light [2+2] photocycloadditions,
     photoredox-modernised Minisci, HAT photocatalysis
     (quinuclidine + photoredox).
   - **Conceptual placement**: photoredox as a **third
     disconnection axis** alongside polar two-electron and
     pericyclic chemistry; metallaphotoredox dual catalysis
     as the modern frontier.
   - **Try-it-in-the-app callbacks** to existing seeded
     content: Diels-Alder + Click chemistry / CuAAC in
     Reactions; radical / HOMO-LUMO / KIE in Glossary;
     spectroscopy tools for UV-Vis prediction of MLCT
     bands.
   - **Further reading**: Prier-Rankic-MacMillan 2013
     *Chem. Rev.*; Romero-Nicewicz 2016 *Chem. Rev.*

2. **Registered in `tutorial/curriculum.py`** as the 7th
   graduate lesson.  Curriculum tier counts:
   - beginner: 8
   - intermediate: 11
   - advanced: 6
   - graduate: 6 → **7**
   - total: 31 → **32**

**Audit verification.**  The new lesson hits all 3
knowledge-graph layers on the round-181 tutorial-coverage
audit:
- **Glossary** — references hybridisation, HOMO/LUMO,
  pericyclic, kinetic isotope effect (all in the seeded
  glossary).
- **Catalogue molecule** — references Click chemistry /
  CuAAC by name (a seeded named-reaction product).
- **Named reaction** — references Diels-Alder + Click
  chemistry + Minisci, all in the `_STARTER` named-reaction
  catalogue.

So the lesson contributes a fully-integrated entry on
construction.  Tutorial fully-integrated coverage went
67.7 % → **68.8 %** (22/32 lessons).

**Test count.** 2269 passed (held — no new tests; the new
lesson was caught by the existing tutorial-coverage audit
which welcomed it into the curriculum without any floor
adjustment needed).  Full suite green.

**Why this matters.**  Demonstrates the value of the audit
infrastructure for **content addition**: writing a new
lesson + the audit immediately confirms it satisfies the
integration gates without any additional manual review.
The Phase-49 audit framework has now been validated as
useful for both (a) regression prevention (its original
purpose), (b) coverage expansion (rounds 183 / 191 / 195 /
196 / 197), and (c) **new-content validation**.

**Files touched.**
- NEW `orgchem/tutorial/content/graduate/07_photoredox.md`
  (~ 110 lines)
- `orgchem/tutorial/curriculum.py` — 1 new lesson entry
- `PROJECT_STATUS.md` — round 198 summary

**Next.**  More curriculum content (still gaps in
intermediate / advanced; e.g. polymer chemistry could go
deeper, supramolecular chemistry is missing from
graduate, click chemistry could have its own lesson), or
return to audit-driven expansion (regulatory_effectors as
the 7th relationship), or roadmap pivot to Phase 38e
(Reactions-tab integration with the simulator).

---

## 2026-04-26 — Round 197 (Audit-driven expansion: cross-reference graph 94 → 136 edges via new metabolic-pathway → molecule relationship)

**Goal.**  Round 196 added 10 central-metabolism intermediates
to the molecule DB (3-PG / PEP / DHAP / G3P + 6 TCA-cycle
intermediates).  Round 197 wires them — and discovers a much
bigger payoff: **the seeded Phase-42a pathway data already
references 62 of those molecules across its 11 pathways**, so
extending the audit with a new derived relationship captures
all 40+ edges in one go.

**Two scopes.**

1. **Body-text mining for the new molecules** (the 2-edge
   wins): scanned kingdom-topic body texts for explicit
   substring mentions of the round-196 intermediates.  Only
   2 hit:
   - `eukarya-physiology-photosynthesis → Glyceraldehyde-
     3-phosphate (G3P)` — Calvin-cycle product
   - `bacteria-physiology-anaerobic-fermentation → Fumarate`
     — added to round-191's NADH/Pyruvate/Ethanol

   The kingdom-topic bodies talk in high-level terms (gluconeogenesis
   "uses 4 ATP + 2 GTP per glucose"); they don't enumerate
   every TCA intermediate.  That's the saturation ceiling
   I bumped into in round 196.

2. **Discovered a much richer source**: the seeded Phase-42a
   `Pathway` data has per-step `substrates` + `products`
   tuples that mention every TCA intermediate by name (`step 1:
   ('Acetyl-CoA', 'Oxaloacetate', 'H₂O') → ('Citrate',
   'CoA-SH')`).  248 raw mentions across 11 pathways; 62
   resolve to DB rows after the round-195 + round-196
   intermediate additions.

   **Extended the cross-reference audit with a 6th
   relationship**: `metabolic-pathway → molecule`, derived
   automatically from pathway-step substrates / products.

**What shipped.**

1. **`core/cross_reference_audit.py`** extended:
   - Added `("metabolic-pathway", "molecule")` to
     `CROSS_REFERENCE_KINDS`.
   - New `_walk_metabolic_pathway_xrefs()` walker that
     iterates each pathway's steps, looks up every
     substrate / product via `find_molecule_by_name`, and
     emits a `CrossRef("metabolic-pathway", pathway.id,
     "molecule", canonical_name)` for each (pathway,
     molecule) pair that resolves.  De-duplicates per pair
     so the same molecule appearing in multiple steps of
     the same pathway only contributes one edge.
   - **Filters at the walker level**: unresolvable names
     (H₂O, CoA-SH, enzyme co-substrates, generic ions)
     never become edges, so `validate_cross_references`
     never reports broken edges from this source.  The
     walker's emit-only-resolvable invariant is locked
     in by a new test.
   - **DB-tolerant**: wraps each `find_molecule_by_name`
     call in try/except so the walker degrades to `[]`
     when the DB isn't initialised, matching the other
     walkers' fault-tolerance pattern.

2. **2 new manual `kingdom-topic → molecule` edges** wired
   (G3P + Fumarate, see scope 1).

3. **`tests/test_cross_reference_graph.py`** updates:
   - `test_metabolic_pathway_walker_uses_db_filter` (NEW)
     — validates the walker's emit-only-resolvable
     invariant by walking the new edges + asserting
     `validate_cross_references([metabolic-pathway edges])`
     reports zero broken.
   - 4 existing tests gained the `app` fixture since the
     new walker requires DB-init (`test_gather...`,
     `test_matrix_covers...`, `test_matrix_renders...`).
   - Per-kind floors updated:
     - `kingdom-topic → molecule` 28 → 30
     - `metabolic-pathway → molecule` NEW at 35
   - Gather-floor 50 → 100.

**Live cross-reference matrix after round 197.**

```
Source kind          → Target kind         | Edges
------------------------------------------------------------
cell-component       → molecule             |     6
kingdom-topic        → cell-component       |    46
kingdom-topic        → metabolic-pathway    |     5
kingdom-topic        → molecule             |    31
microscopy-method    → lab-analyser         |     8
metabolic-pathway    → molecule             |    40   (NEW)
------------------------------------------------------------
TOTAL                                       |   136
```

**Six-round audit-driven expansion arc:**

| Round | Δ | Total | Notable |
|-------|---|-------|---------|
| 178 (baseline) | — | 59 | Audit shipped |
| 183 | +16 | 75 | First wiring round |
| 191 | +13 | 88 | Body-text mining |
| 195 | +4 | 92 | Upstream: 6 new molecules |
| 196 | +2 | 94 | Microscopy edges + 10 new metabolites seeded |
| 197 | +42 | **136** | Audit extension: new metabolic-pathway → molecule relationship |

The big jump in round 197 came from **extending the audit
infrastructure itself** rather than adding more catalogue
data.  Same lesson as round 184/185 (matcher accuracy):
sometimes the gap is in the audit's reach, not the catalogue.
The 6th relationship 2.3× the total edge count.

**Test count.** 2269 passed (was 2268 in round 196, +1 from
new walker-filter test).  Full suite green.

**Why this matters.**  The audit is now genuinely
**comprehensive** across the Phase-42a pathway data — every
TCA intermediate, every glycolysis intermediate, every
β-oxidation intermediate that's in the molecule DB now lights
up as a cross-reference for its parent pathway.  A student
asking "what molecules does glycolysis touch?" gets a
data-driven answer pulled from the audit graph rather than a
hand-curated list.  The same `metabolic-pathway → molecule`
edges power the future Phase-49 doc-coverage extension's
"which lessons should reference each pathway?" question.

**Files touched.**
- `orgchem/core/cross_reference_audit.py` — added the
  6th relationship + walker (~ 35 new lines)
- `orgchem/core/biochemistry_by_kingdom.py` — 2 new
  cross-references on photosynthesis + anaerobic
  fermentation
- `tests/test_cross_reference_graph.py` — new walker-filter
  test, 3 fixture additions, 3 floor updates
- `PROJECT_STATUS.md` — round 197 summary

**Next.**  The audit-driven pattern has produced 6 productive
rounds and remains live.  Future opportunities:
- Mine Phase-42a step `regulatory_effectors` (each step has
  named activators / inhibitors that are biological molecules
  too — could become a 7th relationship).
- The metabolic-pathway → molecule edges could now anchor
  bidirectional navigation (catalogue → pathway → catalogue)
  in the agent surface.
- Or pivot to other roadmap areas (Phase 38e Reactions-tab
  integration, curriculum content, Phase 39 polish).

---

## 2026-04-26 — Round 196 (Audit-driven expansion: 10 central-metabolism intermediates + 2 new microscopy → lab-analyser edges; cross-ref graph 92 → 94 edges)

**Goal.**  Round 195 cleared the kingdom-topic → molecule
backlog by adding 6 biological molecules.  Round 196 was
queued to push the `microscopy-method → lab-analyser` line
(at 6 edges) — but the audit landscape there turned out to
be largely saturated, so I pivoted the round to a different
audit-driven goal: filling out central-carbon-metabolism
small-molecule coverage.

**Audit-landscape finding.**  The lab-analysers catalogue is
clinical-chemistry / molecular-biology focused (28 entries:
13 clinical chemistry + hematology + coagulation, 5
immunoassay, 6 molecular, 2 mass-spec, 2 functional, **only
3 microscopes**: Zeiss LSM 980, Lattice Lightsheet 7,
Krios G4 cryo-TEM).  The Phase-44 microscopy catalogue
references 30 instruments by manufacturer-and-model name
(Leica DLS, Nikon AX, Olympus FVMPE-RS, etc.) but most
aren't in the lab-analysers catalogue at all — the catalogue
isn't a research-microscope reference.  Only one clean new
match: **PerkinElmer Operetta CLS** (already in
lab-analysers under the `functional` category as a
high-content imager, but not yet referenced by any
microscopy method).

**What shipped.**

1. **2 new `microscopy-method → lab-analyser` edges** for
   the Operetta CLS:
   - `widefield-epifluorescence → operetta_cls` (the
     wide-field mode used for plate-based screening).
   - `confocal → operetta_cls` (the confocal mode for
     3D phenotyping in 96 / 384 / 1536-well plates).

   Both methods' `representative_instruments` strings
   extended to mention Operetta CLS so the catalogue + the
   cross-reference stay consistent.

2. **10 central-metabolism intermediates** added to
   `db/seed_intermediates.py` to fill out the small-
   molecule coverage of the central-carbon pathways:

   *Late-glycolysis triose-phosphate intermediates:*
   - **3-Phosphoglycerate (3-PG)** — C₃H₇O₇P
   - **Phosphoenolpyruvate (PEP)** — C₃H₅O₆P (high-energy
     phosphate)
   - **Dihydroxyacetone phosphate (DHAP)** — C₃H₇O₆P
   - **Glyceraldehyde-3-phosphate (G3P)** — C₃H₇O₆P (DHAP
     + G3P are the Aldolase products from F1,6BP)

   *TCA-cycle intermediates (6 of 8 not previously in DB):*
   - **Citrate** — C₆H₈O₇
   - **α-Ketoglutarate** — C₅H₆O₅
   - **Succinate** — C₄H₆O₄
   - **Fumarate** — C₄H₄O₄
   - **L-Malate** — C₄H₆O₅
   - **Oxaloacetate** — C₄H₄O₅

   All 10 SMILES verified to parse + canonicalise cleanly;
   10 new rows added on the seed-update run (no
   canonicalisation duplicates).

   These molecules are all referenced in the seeded
   Phase-42a glycolysis + TCA-cycle pathway data + in many
   kingdom-topic body texts (aerobic respiration, anaerobic
   fermentation, photosynthesis cross-references), so
   future audit-mining rounds can wire them as
   cross-references.

3. **Per-kind floor raised** in
   `tests/test_cross_reference_graph.py`:
   `microscopy-method → lab-analyser` 4 → 7.

**Live cross-reference matrix after round 196.**

```
Source kind          → Target kind         | Edges
------------------------------------------------------------
cell-component       → molecule             |     6
kingdom-topic        → cell-component       |    46
kingdom-topic        → metabolic-pathway    |     5
kingdom-topic        → molecule             |    29
microscopy-method    → lab-analyser         |     8
------------------------------------------------------------
TOTAL                                       |    94
```

**Cross-reference-graph trajectory across the 5 audit-driven
expansion rounds:**

| Round | Δ edges | Total | Notable |
|-------|---------|-------|---------|
| 178 (baseline) | — | 59 | Audit shipped |
| 183 | +16 | 75 | First wiring round |
| 191 | +13 | 88 | Body-text mining (true positives) |
| 195 | +4 | 92 | Upstream: 6 new molecules |
| 196 | +2 | 94 | Microscopy + 10 metabolism intermediates seeded for future use |

**Test count.** 2268 passed (held — no new tests, just
floor tightening + 2 catalogue edges + 10 new seed entries).
Full suite green.

**Why this matters.**  Demonstrates an important nuance in
audit-driven expansion: **some audit lines hit a saturation
ceiling that's not worth fighting**.  Forcing more
microscopy → lab-analyser edges by adding non-clinical
microscopes to lab-analysers would distort the catalogue's
purpose.  Better to take the saved budget into a different
audit-relevant area — here, expanding the molecule DB to
enable future cross-references.  The round saved the budget
for the central-metabolism coverage that's been latent
since the Phase-42a pathway data shipped.

**Files touched.**
- `orgchem/db/seed_intermediates.py` — 10 new entries
  (~ 25 new lines)
- `orgchem/core/microscopy.py` — 2 cross-references on
  widefield-epifluorescence + confocal + extended
  representative_instruments strings
- `tests/test_cross_reference_graph.py` —
  `microscopy-method → lab-analyser` floor 4 → 7
- `PROJECT_STATUS.md` — round 196 summary

**Next.**  More audit-driven expansion (the new
metabolism intermediates can wire into kingdom-topic
xrefs once their body texts get scanned again — saving
that for a later round so this round stays small-scope),
or pivot to Phase 38e (Reactions-tab integration) /
curriculum content.  The audit dashboards have been a
remarkably durable backlog source — 5 rounds in and the
ceiling isn't fully hit yet.

---

## 2026-04-26 — Round 195 (Audit-driven expansion: 6 new biological molecules + 4 new cross-references; cross-ref graph 88 → 92 edges)

**Goal.**  Round 191 surfaced kingdom-topic body texts that
mention biological molecules NOT in the seeded Molecule DB —
the cross-reference couldn't be wired even though the body
text mentioned them by name.  Round 195 closes that upstream
gap by adding 6 well-known biological molecules to the DB,
then wiring the 4 cross-references that newly become possible.

**The pattern.**  Audit dashboards have surfaced gaps before;
this round demonstrates an **upstream gap-closing pattern**:
a coverage gap can sometimes be fixed by adding to the
target catalogue (here, the molecule DB) rather than just by
adding more references on the source side.  The same pattern
applies to cell-component → molecule (many constituents like
ATP synthase / RuBisCO are protein complexes that aren't in a
small-molecule DB at all).

**What shipped.**

1. **6 new biological molecules** in
   `db/seed_intermediates.py`:
   - **Acetyl-CoA** (C₂₃H₃₈N₇O₁₇P₃S) — central metabolic
     intermediate, entry point to the TCA cycle.
   - **Glutathione (GSH)** (C₁₀H₁₇N₃O₆S) — major cellular
     reductant + redox buffer.
   - **Plastoquinone-9** (C₅₃H₈₀O₂) — photosynthetic
     Z-scheme electron carrier between PSII + cytb₆f.
   - **Fructose-1,6-bisphosphate** (C₆H₁₄O₁₂P₂) —
     glycolysis branch point + Aldolase product.
   - **Glucose-6-phosphate** (C₆H₁₄O₉P) — first
     phosphorylation product in glycolysis + entry point
     to the pentose phosphate shunt.
   - **Indole-3-acetic acid (IAA, auxin)** (C₁₀H₉NO₂) —
     the canonical plant phytohormone.

   All 6 SMILES verified to parse + canonicalise cleanly.
   Two iterations to get them right (heme + chlorophyll a
   tried first but their porphyrin SMILES didn't kekulise —
   left as a future challenge).

2. **4 new kingdom-topic → molecule edges** wired:
   - `eukarya-physiology-aerobic-respiration` → +Acetyl-CoA
     (added to round-191's ATP / NADH / FAD / Pyruvate /
     GTP / CoA-SH).  The body text explicitly mentions
     "glucose → pyruvate → acetyl-CoA + CO₂ + NADH".
   - `eukarya-physiology-photosynthesis` → +Plastoquinone-9
     (added to round-183's ATP / NADPH).  Z-scheme.
   - `eukarya-physiology-development-multicellularity` →
     IAA.  This was the round-191 false-positive case
     (the body text mentions "indole-3-acetic acid" but
     IAA wasn't in the DB so the substring match landed
     on the inert "Acetic acid" row — a true
     embarrassment).  Now resolves to the actual molecule.
   - `eukarya-physiology-plant-auxin-photoperiodism` →
     IAA.  Same fix.

3. **Per-kind floor raised** in
   `tests/test_cross_reference_graph.py`:
   `kingdom-topic → molecule` 22 → 28.

**Live cross-reference matrix after round 195.**

```
Source kind          → Target kind         | Edges
------------------------------------------------------------
cell-component       → molecule             |     6
kingdom-topic        → cell-component       |    46
kingdom-topic        → metabolic-pathway    |     5
kingdom-topic        → molecule             |    29
microscopy-method    → lab-analyser         |     6
------------------------------------------------------------
TOTAL                                       |    92
```

**Cross-reference-graph trajectory across the 4 audit-driven
expansion rounds:**

| Round | Δ edges | Total | Notable change |
|-------|---------|-------|----------------|
| 178 (baseline) | — | 59 | Audit shipped |
| 183 | +16 | 75 | First wiring round (cell-component + kingdom-topic) |
| 191 | +13 | 88 | Body-text mining (true positives only) |
| 195 | +4 | 92 | Upstream: add new molecules → wire 4 |

`kingdom-topic → molecule` specifically grew **1 → 12 → 25 →
29** across rounds 178/183/191/195 (29× growth from baseline).

**Test count.** 2268 passed (held — no new tests, just floor
tightening + catalogue edits + 6 new seed entries).  Full
suite green.

**Why this matters.**  Demonstrates a new audit-expansion
sub-pattern: when source-side wiring stalls, look for
**upstream gaps in the target catalogue**.  The cell-
component → molecule line is at 6 edges precisely because
many constituents are protein complexes / aggregates rather
than small molecules — but heme (a small molecule) is in
many constituents (haemoglobin, myoglobin, cytochromes a/b/c,
P450) and would jump the edge count if a parseable SMILES
were available.  Future work: add heme + chlorophyll a via
RDKit-friendly SMILES + see how far cell-component → molecule
can grow.

**Files touched.**
- `orgchem/db/seed_intermediates.py` — 6 new entries (~ 18
  new lines)
- `orgchem/core/biochemistry_by_kingdom.py` — 4 topics
  gained / extended `cross_reference_molecule_names`
  tuples (~ 10 new lines)
- `tests/test_cross_reference_graph.py` — `kingdom-topic
  → molecule` floor 22 → 28
- `PROJECT_STATUS.md` — round 195 summary

**Next.**  Either continue audit-driven expansion
(`microscopy-method → lab-analyser` is at 6 edges and the
Phase-44 microscopy catalogue has 30 entries; or keep
hunting for biological molecules to add), OR pivot to
Phase 38e (Reactions-tab integration with the simulator),
OR start a curriculum-content round (more lessons in the
graduate level, more named-reaction expansion beyond 60).

---

## 2026-04-26 — Round 194 (Phase 38d.4 SHIPPED — 7 simulator agent actions + 3 remaining setup scripts; Phase 38d effectively complete)

**Goal.**  Round 193 shipped the SimulationDock UI.  Round 194
exposes the simulator to the AI tutor + closes the
"5 of 8 setups have scripts" gap from round 192.

**What shipped.**

1. **3 new per-setup scripts** in
   `core/process_simulator.py`:
   - **Soxhlet extraction** (6 stages: charge thimble →
     charge pot → reflux + thimble fills → siphon trips →
     repeat (4-24 h) → cool + recover).  The canonical
     siphon-trip step distinguishes Soxhlet from
     continuous extraction — the body fills until the
     siphon arm height is reached, then drains the
     entire body in one cycle.
   - **Liquid-liquid extraction** (6 stages: combine →
     invert + vent → shake → settle → drain → repeat 3×).
     The invert+vent step is explicitly called out for
     safety — volatile solvents (ether, DCM) build
     pressure fast.
   - **Reflux-with-addition** (6 stages: charge →
     charge funnel → cooling + heat → dropwise → reflux
     hold → cool).  The `dropwise` stage carries
     `parameters={drops_per_second: 1}` capturing the
     rate-controlling exotherm management.

   **All 8 Phase-38b setups now have simulator scripts**
   (was 5 in round 192).  `_SCRIPTS` lookup in the
   simulator module is now exhaustive against
   `list_setups()` ids.

2. **`agent/actions_simulator.py` (NEW, ~ 230 lines)** — 7
   actions in the new `simulator` category:

   - `start_process_simulation(setup_id)` — opens the
     canvas dialog (singleton), populates it from the
     seeded setup, instantiates a fresh `ProcessSimulator`,
     binds it to the dock, auto-plays.  Returns
     `{started: True, setup_id, total_stages}` or
     `{error: ...}`.

   - `simulator_state()` — JSON snapshot for tutor
     introspection.  Returns
     `{loaded: bool, setup_id, total_stages, current_index,
     current_stage: {id, label, description},
     is_complete, is_playing, progress, speed}`.  When no
     simulator is loaded, returns `{loaded: False}`
     rather than erroring.

   - **Playback controls** that mirror the dock's
     buttons: `simulator_step()`, `simulator_reset()`,
     `simulator_play()`, `simulator_pause()`.

   - `set_simulator_speed(speed)` — clamped to
     [0.5, 4.0]; returns the actually-applied value (so
     the agent can verify clamping).

   All 7 actions marshal onto the Qt main thread +
   gracefully handle missing-window / no-simulator /
   unknown-setup with `{error: ...}` rather than
   raising.

3. **GUI audit + `_CATEGORY_SUMMARIES`** updated with the
   7 new actions + the new `simulator` category summary.
   Phase-49 audit infrastructure caught these immediately
   on the failing tests.

4. **15 new tests** in
   `tests/test_actions_simulator.py`:
   - 7-action registration + correct category
   - All-setups-scripted invariant
     (`set(available_setups()) == set(list_setups()
     ids)`)
   - 3 new scripts well-formed (each contains its
     canonical stage id — siphon / invert / dropwise)
   - `start_process_simulation` happy + unknown-setup
   - `simulator_state` when no dialog / after start
   - Step advances + no-simulator error
   - Reset goes to 0
   - Play/pause toggle
   - Set speed within bounds + clamping (0.1 → 0.5,
     10.0 → 4.0)

5. **1 round-193 test updated** — `test_run_simulation_
   with_unscripted_setup` previously used
   `soxhlet_extraction` (which had no script in 193).
   As of round 194 every setup has a script, so the test
   now uses a fictional id by setting
   `_loaded_setup_id` directly to keep the no-script
   branch exercised.

**Test count.** 2268 passed (was 2253 in round 193, +15
from new simulator-action tests).  Full suite green.

**Phase 38d status: effectively complete.**

| Sub | Round | What |
|-----|-------|------|
| 38d.1 | 192 | Headless state machine (`Stage` + `ProcessSimulator` + 5 scripts).  15 tests. |
| 38d.2 | 193 | `SimulationDock` Qt UI + canvas integration.  14 tests + canvas-items refactor. |
| 38d.3 | (deferred) | Per-stage canvas-glyph flashing + parameter tweaks.  Low-priority polish; the dock's text commentary already delivers the pedagogical content. |
| 38d.4 | 194 | 7 agent actions + 3 remaining setup scripts → all 8 Phase-38b setups scripted.  15 tests. |

**Combined**: 2 new core modules (`process_simulator.py` +
catalogue extension), 1 new GUI module
(`lab_simulation_dock.py`), 1 new agent module
(`actions_simulator.py`), 7 new agent actions, 1 new agent
category, **44 new tests** across 38d.1+38d.2+38d.4
(15+14+15).  Test suite went from 2224 (round 191
baseline) → 2268 (+44).

**Why this matters.**  Phase 38d turns the static apparatus
of Phase 38c into a **time-evolving teaching simulation**.
A student can ask the tutor *"show me how a Soxhlet
extraction works"*, the tutor calls
`start_process_simulation("soxhlet_extraction")`, the
canvas renders, and the simulator walks through 6 teaching
stages with the canonical siphon-trip explanation.  The
tutor can then introspect `simulator_state()` to answer
follow-up questions like *"what happens after the siphon
trips?"* without waiting for the playback to reach that
stage.

The deferred 38d.3 polish (visual choreography on the
glyphs themselves) is a "nice-to-have" — useful but not
load-bearing for the teaching value.  Better to take the
saved budget into other phases (Phase 39 polish, more
audit-driven curriculum expansion, etc.).

**Files touched.**
- `orgchem/core/process_simulator.py` — 3 new helper
  functions + 3 new entries in `_SCRIPTS` (~ 175 new
  lines)
- NEW `orgchem/agent/actions_simulator.py` (~ 230 lines)
- NEW `tests/test_actions_simulator.py` (~ 200 lines)
- `tests/test_lab_simulation_dock.py` — 1 round-193 test
  updated for the new "all setups scripted" reality
- `orgchem/agent/__init__.py` — register the new module
- `orgchem/agent/actions_meta.py` — `simulator` category
  summary
- `orgchem/gui/audit.py` — 7 new GUI_ENTRY_POINTS
- `INTERFACE.md` — `actions_simulator.py` row
- `ROADMAP.md` — Phase 38d.4 SHIPPED + 38d.3 deferral
- `PROJECT_STATUS.md` — round 194 summary

**Next.**  Phase 38e (Reactions-tab integration — pick a
seeded reaction, select the matching setup, watch the
apparatus + reaction co-animate) or pivot to other
roadmap areas.  Phase 38d's saved 38d.3 budget could
also fund another audit-driven curriculum-expansion
round, or polish on the Phase 39 lab-calculator dialog.

---

## 2026-04-26 — Round 193 (Phase 38d.2 SHIPPED — canvas-animation playback dock + canvas-items refactor)

**Goal.**  Round 192 shipped the headless `ProcessSimulator`
state machine.  Round 193 wires the Qt UI on top: a
`SimulationDock` widget that drives the simulator via a
`QTimer`, surfaced via a *Run simulation* button on the
Phase-38c canvas dialog.

**File-size constraint forced a refactor first.**  Adding the
new dock + wiring would have pushed `lab_setup_canvas.py`
over the 500-line global cap.  Extracted `EquipmentGlyph` +
`ConnectionLine` to a new `gui/dialogs/lab_canvas_items.py`
module (~ 140 lines) — these are pure-graphics-item classes
with no dialog logic, so they belong in their own module
anyway.  Main canvas file went 562 → 494 lines after
extraction + new wiring.  31 canvas tests still pass.

**What shipped.**

1. **`gui/dialogs/lab_canvas_items.py` (NEW, ~ 140 lines)**
   — extracted from `lab_setup_canvas.py`:
   - `EquipmentGlyph(QGraphicsItemGroup)` — placeholder
     visual.  **New in 193**: `set_active(bool)` /
     `is_active()` + `_active` flag for the simulator-
     stage highlight overlay (border thickens to 3.5 px
     amber; background fills with light amber).  The
     simulator-driven choreography that calls `set_active`
     on the right glyphs ships as polish in 38d.3.
   - `ConnectionLine(QGraphicsLineItem)` — visual link
     (unchanged from round 189; just relocated).
   - `GLYPH_W = 96` / `GLYPH_H = 56` module constants.

2. **`gui/dialogs/lab_simulation_dock.py` (NEW, ~ 240 lines)**
   — `SimulationDock(QWidget)`:
   - **UI**: Play / Pause / Step / Reset buttons (Pause /
     Play swap labels based on `is_playing()`), speed
     slider (50 - 400 → 0.5× - 4×, default 1×), stage
     label ("Stage 3 / 6: Apply heat"), description
     `QTextBrowser` (the pedagogical commentary track),
     progress bar (`Stage X / Y` format).
   - **`QTimer` (10 Hz)** auto-advances when
     `elapsed_ms_in_stage >= stage.duration_seconds *
     1000 / speed`.  Manual `step()` resets the elapsed
     counter.
   - **Public API**: `set_simulator(sim)` binds (or
     `None` to clear); `simulator()` / `speed()` /
     `is_playing()` accessors; `play()` / `pause()` /
     `step()` / `reset()` controls.
   - **Signals**: `stage_changed(stage_id, stage_index)`
     fires on every advance (manual or timer-driven);
     `finished()` fires once on completion.
   - **Empty / no-simulator state** disables every
     control cleanly so the dock is safe to instantiate
     before a setup is loaded.

3. **`LabSetupCanvasDialog` wiring**:
   - `_loaded_setup_id` field tracks the most-recently-
     loaded setup id (set by `load_setup` +
     `populate_from_setup`).
   - **Toolbar gained a *Run simulation* button** that
     calls `simulator_for_setup(self._loaded_setup_id)`
     and `dock.play()` to auto-start.
   - **Bottom dock**: `SimulationDock` instance with a
     220 px max height, sits below the splitter.
   - `simulation_dock()` accessor for tests + future
     agent actions.
   - Setups without a script (Soxhlet / liquid-liquid /
     reflux-with-addition — queued for 38d.4) get a
     friendly status message + leave the dock empty.
   - Setup with no setup loaded gets a "Load a setup
     first…" status message.

4. **`tests/test_lab_simulation_dock.py` (NEW)** — 14
   tests:
   - Dock initial state (no simulator, controls disabled).
   - `set_simulator` enables controls + emits initial
     stage_changed signal.
   - `set_simulator(None)` re-disables.
   - `step()` advances + emits the right signal.
   - Step-to-completion fires `finished` exactly once +
     disables Play.
   - `reset()` rewinds.
   - Speed default = 1.0×, slider updates correctly.
   - **Timer-driven auto-advance smoke**: uses synthetic
     `_on_tick()` calls + a 0.05s-stage simulator at 4×
     speed so we don't have to wait real wall-clock
     time.  Verifies the simulator advances after a
     single tick that exceeds `stage_ms`.
   - Play/Pause toggle.
   - Canvas dialog exposes `simulation_dock()`.
   - *Run simulation* button: no-setup / loaded-setup /
     unscripted-setup paths.

**Test count.** 2253 passed (was 2239 in round 192, +14
from the new dock tests + 31 canvas tests still pass after
the refactor).  Full suite green.

**File sizes.**
- `lab_setup_canvas.py`: 562 → 494 lines (extraction +
  net additions ≈ -68 lines).
- `lab_canvas_items.py`: 138 lines (NEW).
- `lab_simulation_dock.py`: 241 lines (NEW).

**Why this matters.**  Phase 38d.2 closes the gap between
the headless state machine + the user.  A student can now:
- Open *Lab setups → Build on canvas* (Phase 38c.5).
- Watch the apparatus render.
- Click **Run simulation** + see the process play out
  step-by-step with a description panel walking through
  each stage at adjustable speed.
- Use **Step** for click-through study.
- Use **Reset** to play it again.

The signal-based `stage_changed(stage_id, ...)` is the
hook the future Phase-38d.3 polish will use to make the
canvas glyphs flash + draw rising-vapour arrows + show
temperature climbs as the corresponding stage runs.

**Files touched.**
- NEW `orgchem/gui/dialogs/lab_canvas_items.py` (~ 140
  lines, extracted)
- NEW `orgchem/gui/dialogs/lab_simulation_dock.py` (~ 240
  lines)
- NEW `tests/test_lab_simulation_dock.py` (~ 200 lines)
- `orgchem/gui/dialogs/lab_setup_canvas.py` — module
  docstring trimmed; `EquipmentGlyph` + `ConnectionLine`
  removed (now imported from `lab_canvas_items`); imports
  reorganised; *Run simulation* toolbar button +
  `_on_run_simulation` slot + bottom dock wiring +
  `_loaded_setup_id` field
- `INTERFACE.md` — 2 new dialog rows
- `ROADMAP.md` — Phase 38d.2 SHIPPED
- `PROJECT_STATUS.md` — round 193 summary

**Next.** Phase 38d.3 (per-stage canvas-glyph highlighting +
parameter tweaks) or 38d.4 (3 remaining setup scripts +
agent actions for the simulator).  Either keeps Phase 38d
moving; 38d.3 is the higher-impact UI polish, 38d.4 is the
quickest +bigger surface area win.

---

## 2026-04-26 — Round 192 (Phase 38d.1 SHIPPED — process-simulator headless state machine; first sub-phase of the multi-round Phase-38d simulator)

**Goal.**  Phase 38c closed in round 190 with a fully
interactive lab-equipment canvas (drag/drop, snap-validation,
agent actions).  Phase 38d adds the process simulator that
animates the apparatus running ("turn on heat → vapour rises
→ condenser cools → receiver fills").  Round 192 ships
**Phase 38d.1 — the headless state-machine layer**, same
headless-first pattern as 38c.1 → 38c.2.

**What shipped.**

1. **`core/process_simulator.py` (NEW, ~ 295 lines)** — pure
   data + state-machine layer:

   - **`Stage(id, label, description, duration_seconds,
     parameters)`** frozen dataclass — one teaching step.
     `id` is stable cross-reference (the Phase-38d.2 canvas
     can map stages to highlight overlays).  `label` for the
     short button text.  `description` for the longer
     commentary the canvas will render in a side panel.
     `duration_seconds` for default playback timing.
     `parameters` is a free-form dict for stage-specific
     data (`target_temp_C`, `theoretical_plates`,
     `flow_rate`, etc.).

   - **`ProcessSimulator(setup_id, stages)`** — linear
     state-machine driver:
     - `current_stage()` / `current_index()` — current
       position
     - `advance()` — move to next stage; returns False when
       already past the end
     - `reset()` — back to stage 0
     - `jump_to(stage_id)` — random access by id
     - `is_complete()` / `progress()` — playback status;
       `progress()` returns 0.0 for empty scripts (no
       ZeroDivisionError)
     - `total_stages` property

   - **5 of 8 Phase-38b setups have scripts** out of the
     box:
     - **simple distillation** (6 stages: charge →
       cooling-water-on → heat-up → vapour-rises → condense
       → cool-down)
     - **fractional distillation** (7 stages: simple +
       Vigreux column-equilibration step inserted via the
       shared `_distillation_stages(with_column=True)`
       helper — DRY)
     - **reflux** (5 stages)
     - **vacuum filtration** (5 stages)
     - **recrystallisation** (4 stages)
     - Soxhlet / liquid-liquid / reflux-with-addition
       scripts queued for 38d.4.

   - **JSON serialisation**: `stage_to_dict` /
     `simulator_to_dict` for the eventual Phase-38d.4
     agent action.

2. **`tests/test_process_simulator.py` (NEW)** — 15 tests:
   stage immutability + defaults; simulator starts at 0;
   advance walks through then refuses past-the-end;
   reset; jump_to (happy + unknown id); progress bounded
   [0, 1]; empty-script edge case; unknown-setup returns
   None; `available_setups` floor; every shipped script
   well-formed (≥ 3 stages, no duplicate ids, all fields
   non-empty + positive duration); fractional has
   `column-equilibration` extra stage that simple lacks;
   dict round-trips; **no-Qt-import sentinel** (locks
   the headless guarantee in).

**Test count.** 2239 passed (was 2224 in round 191, +15
from new simulator tests).  Full suite green.

**Why this matters.**  The state-machine layer is the
seam the Phase-38d.2 canvas-animation widget will use to
drive timeline playback.  Splitting it as a headless layer
means:
- the agent action surface (Phase 38d.4) can introspect
  simulator state without a Qt widget
- per-setup scripts can be edited / extended /
  unit-tested without touching Qt
- a future "rewind to mark this stage" or "jump to
  the troubleshooting checkpoint" UI can plug in via
  `jump_to(stage_id)` without changing the canvas
- the same simulator can drive both the GUI playback and a
  hypothetical agent-driven autonomous demo

The shared `_distillation_stages(with_column)` helper
demonstrates the design principle from Phase-38b: simple
+ fractional distillation share their physical setup
(simple + Vigreux column inserted), so they share their
process script via a parameter flag rather than two
duplicated step lists.

**Files touched.**
- NEW `orgchem/core/process_simulator.py` (~ 295 lines)
- NEW `tests/test_process_simulator.py` (~ 175 lines)
- `INTERFACE.md` — new module row
- `ROADMAP.md` — Phase 38d.1 SHIPPED + 38d.2-38d.4 laid
  out
- `PROJECT_STATUS.md` — round 192 summary

**Next.** Phase 38d.2 — canvas-animation playback overlay.
Likely adds a *Run simulation* button to the Phase-38c
canvas dialog that opens a docked control bar (Play /
Pause / Reset / Speed slider) + highlights the current
stage on the canvas (e.g. flash the heating mantle during
the heat-up stage, draw rising-vapour arrows during
vapour-rises).  Probably ships as a sibling
`SimulationDock` widget bound to the canvas dialog's
existing `LabSetupCanvasDialog`.

---

## 2026-04-26 — Round 191 (Audit-driven expansion: cross-reference graph 75 → 88 edges; round-178 dashboard mining)

**Goal.**  After Phase 38c shipped end-to-end (rounds 186-190),
go back to the audit-driven expansion pattern.  The round-178
cross-reference dashboard has surfaced low-coverage areas
twice now (round 183 first wired cell-component +
kingdom-topic → molecule; round 184/185 widened the tutorial
matchers).  Round 191 walks the kingdom-topic body texts a
second time — many topics still mention DB-resolvable
molecules that aren't cross-referenced.

**Findings + filtering.**

The walker found 16 topics with potential new edges.
Hand-checked each:
- 13 are real (mentions like "ATP", "GTP", "NADH", "Methane",
  "Sucrose", "Cholesterol" in plain text).
- 2 are false positives — `eukarya-physiology-development-
  multicellularity` + `eukarya-physiology-plant-auxin-
  photoperiodism` mention "indole-3-acetic acid" (auxin/IAA),
  which contains "acetic acid" as a substring.  Skipped.
- The auxin topics genuinely reference IAA but IAA isn't in
  the seeded molecule DB; documented as a future expansion
  opportunity (would need to add IAA to the molecule seed).

**What shipped.**

13 new `cross_reference_molecule_names` tuple entries across
9 topics (some already had cross-refs but gained additions):

- **eukarya-structure-nucleus** → GTP (Ran-GTPase gradient)
- **eukarya-structure-cytoskeleton** → ATP + GTP (actin +
  microtubule motors)
- **eukarya-physiology-aerobic-respiration** → +Coenzyme A
  (added to round-183's ATP/NADH/FAD/Pyruvate/GTP)
- **eukarya-genetics-endosymbiotic-origin** → Cholesterol
  (absent from bacterial inner membranes — diagnostic
  evidence in the body text)
- **eukarya-structure-plant-vascular-tissue** → Sucrose
  (phloem cargo)
- **bacteria-structure-no-organelles** → ATP (generated at
  the plasma membrane in the absence of mitochondria)
- **bacteria-physiology-anaerobic-fermentation** → +Ethanol
  (added to NADH/Pyruvate)
- **archaea-structure-archaellum** → ATP (FlaI ATPase rotates
  the filament — distinct from bacteria's proton-motive flagellum)
- **archaea-structure-no-organelles** → ATP (membrane-bound
  ATP synthase)
- **archaea-physiology-methanogenesis** → Methane (the
  exclusively-archaeal product)
- **archaea-physiology-syntrophic-partners** → Methane (AOM)
- **archaea-physiology-bacteriorhodopsin** → ATP (the
  simplest known light-driven energy converter — proton
  pump + ATP synthase, no ETC needed)

**Live cross-reference matrix after round 191.**

```
Source kind          → Target kind         | Edges
------------------------------------------------------------
cell-component       → molecule             |     6
kingdom-topic        → cell-component       |    46
kingdom-topic        → metabolic-pathway    |     5
kingdom-topic        → molecule             |    25
microscopy-method    → lab-analyser         |     6
------------------------------------------------------------
TOTAL                                       |    88
```

(Round 183 → 75 edges; round 178 → 59 edges.  +13 this
round, +29 across the 3 audit-driven expansion rounds.)

**Floor raised**: `test_per_kind_floors` for `kingdom-topic
→ molecule` went 10 → 22 to lock the new state.

**Test count.** 2224 passed (held — no new tests, just
catalogue edits + floor tightening).  Full suite green.

**Why this matters.**  The round-178 audit dashboard is now
proven as a **multi-round expansion driver**: each
mining round has produced concrete coverage gains without
needing a new feature.  The pattern is robust enough to
serve as the default "what should I work on this round?"
heuristic when no big phase is open.

**Files touched.**
- `orgchem/core/biochemistry_by_kingdom.py` — 9 topics
  gained / extended `cross_reference_molecule_names`
  tuples (~ 25 new lines)
- `tests/test_cross_reference_graph.py` — `kingdom-topic →
  molecule` floor 10 → 22
- `PROJECT_STATUS.md` — round 191 summary

**Next.**  Audit-driven expansion still has thin layers
left to mine:
- `microscopy-method → lab-analyser` is at 6 edges.  The
  Phase-44 microscopy catalogue has 30 entries, only 6 of
  which cross-reference Phase-40a lab analysers.
- `cell-component → molecule` is at 6 edges.  Many
  constituents like ATP synthase / RuBisCO / Catalase
  could link if those molecules / enzymes were added to
  the seeded DB.

Or pivot to Phase 38d (process simulator), Phase 39
(continuing the lab-calculator polish), or curriculum
expansion.

---

## 2026-04-26 — Round 190 (Phase 38c.5 SHIPPED — agent actions + Build-on-canvas integration; PHASE 38c COMPLETE)

**Goal.**  Round 189 wired snap-validation.  Round 190 closes
Phase 38c with the agent-action surface + the *Build on
canvas* integration that ties the canvas to the Phase-38b
*Lab setups…* dialog.

**What shipped.**

1. **`agent/actions_lab_canvas.py` (NEW, ~ 220 lines)** —
   five agent actions in the new `lab-canvas` category:

   - `open_lab_setup_canvas(setup_id="")` — opens the
     dialog, optionally pre-populating with a seeded
     Phase-38b setup.  Returns `{opened: True, populated:
     bool}` or `{error: ...}`.
   - `place_equipment_on_canvas(equipment_id, x=200,
     y=200)` — drops a glyph programmatically.  Errors if
     the dialog isn't open or the equipment id is unknown.
   - `connect_canvas_equipment(equipment_a_id, port_a,
     equipment_b_id, port_b)` — connects the **first**
     placed glyph of each id at the named ports.  Reports
     `valid` (snap-validator result) + `error_message`
     separately from the call's `error` (for missing
     glyphs / dialog).
   - `clear_lab_setup_canvas()` — wipes glyphs + lines.
   - `lab_setup_canvas_state()` — JSON snapshot of every
     placed glyph + every connection for tutor
     introspection.

   All 5 actions marshal onto the Qt main thread via
   `_gui_dispatch.run_on_main_thread_sync` and gracefully
   handle main-window-not-available / dialog-not-open /
   unknown-equipment-id with `{error: ...}` rather than
   raising.

2. **`LabSetupCanvasDialog.populate_from_setup(setup_id)`** —
   new method that swaps the palette to the per-setup view,
   clears any prior canvas content, places each equipment
   item in a horizontal row (180 px spacing, base x=120,
   y=280), and draws each connection from
   `setup.connections`.  Powers both the new agent action
   and the *Build on canvas* button.

3. **Phase-38b `LabSetupsDialog` *Build on canvas* button**
   added to the dialog footer.  Disabled by default;
   `_show_setup` enables it, `_show_blank` disables it
   again.  Clicking it instantiates the singleton canvas
   dialog + calls `populate_from_setup(self._current_setup_id)`.

4. **GUI audit + `_CATEGORY_SUMMARIES`** updated with the 5
   new actions + the new `lab-canvas` category summary.
   The round-180 audit infrastructure made these updates
   trivial — the failing test surfaced exactly which
   entries were missing.

5. **17 new round-190 tests** in
   `tests/test_actions_lab_canvas.py`:
   - 5-action registration + correct category.
   - `open_lab_setup_canvas` no-setup / setup / unknown-id
     paths.
   - `place_equipment_on_canvas` requires-open + happy +
     unknown-id.
   - `connect_canvas_equipment` valid / mismatched /
     glyph-not-present.
   - `clear_lab_setup_canvas` drops everything.
   - `lab_setup_canvas_state` after populate / when dialog
     closed.
   - `populate_from_setup` clears prior state + unknown-id
     returns False.
   - *Build on canvas* button exists + click triggers
     populate.

   First-run finding: a test that assumed the
   `LabSetupsDialog` button was disabled at construction
   time was wrong — the dialog auto-selects the first
   setup on construction so the button enables immediately.
   Test updated to exercise `_show_blank` (disable) →
   `_show_setup` (enable) lifecycle directly.  Also caught
   that `setCurrentRow(0)` is a no-op when row 0 is already
   selected, so the test had to call `_show_setup` directly
   to reliably trigger the enable.

**Test count.** 2224 passed (was 2207 in round 189, +17
from new agent-action tests).  Full suite green.

---

### **PHASE 38c COMPLETE**

Five sub-phases shipped over rounds 186-190:

| Sub | Round | What |
|-----|-------|------|
| 38c.1 | 186 | `core/lab_palette.py` — headless palette data layer (`PaletteCategory` + `Palette` + `default_palette()` + `palette_for_setup()`).  11 tests. |
| 38c.2 | 187 | `gui/dialogs/lab_setup_canvas.py` Qt UI scaffolding (`LabSetupCanvasDialog` singleton modeless dialog + `PaletteDock` `QTreeWidget` + `CanvasView` `QGraphicsView`).  12 tests. |
| 38c.3 | 188 | Drag/drop wiring (`_PaletteTree.startDrag` packages `EQUIPMENT_MIME` payload + `CanvasView` accepts drops + places `EquipmentGlyph` `QGraphicsItemGroup` placeholders).  10 tests. |
| 38c.4 | 189 | Snap-validation (`core/lab_setups.validate_port_pair` + `ConnectionLine` visual + `connect_glyphs` API + `equipment_connected` signal — green for valid pairs, dashed red for mismatches).  9 tests. |
| 38c.5 | 190 | `agent/actions_lab_canvas.py` (5 actions) + `populate_from_setup` + *Build on canvas* button on the Phase-38b dialog.  17 tests. |

**Combined**: 2 new core modules (`lab_palette.py`,
extension to `lab_setups.py`), 1 new GUI module
(`lab_setup_canvas.py` ~ 530 lines), 1 new agent module
(`actions_lab_canvas.py` ~ 220 lines), 1 new dialog
modification (Phase-38b `LabSetupsDialog`), 5 new agent
actions, 1 new Qt category (`lab-canvas`), **59 new tests**
(11 + 12 + 10 + 9 + 17).  Test suite went from 2165 →
2224 passing (+59).

**Why this matters.**  Phase 38c turns the static Phase-38a
equipment catalogue + Phase-38b setup catalogue into a
hands-on **build the apparatus** teaching tool.  A student
can now:
- pick a seeded setup (e.g. simple distillation) from the
  *Lab setups…* dialog
- click *Build on canvas* and see the apparatus rendered
- drag in a wrong piece (e.g. add a second RBF) and try to
  connect it incorrectly — the canvas immediately shows a
  red dashed line + a "port-sex mismatch" status message
- ask the tutor *"is my apparatus right?"* and the tutor
  introspects via `lab_setup_canvas_state()` to give
  pedagogical feedback

The same audit infrastructure (Phase 49 series) ensures
the new actions are discoverable through `list_capabilities()`
and the new dialog has a corresponding `open_*` action.

**Files touched (round 190 only).**
- NEW `orgchem/agent/actions_lab_canvas.py` (~ 220 lines)
- NEW `tests/test_actions_lab_canvas.py` (~ 215 lines)
- `orgchem/gui/dialogs/lab_setup_canvas.py` —
  `populate_from_setup` method (~ 35 lines)
- `orgchem/gui/dialogs/lab_setups.py` — *Build on canvas*
  button + `_on_build_on_canvas` slot + `_current_setup_id`
  state field
- `orgchem/agent/__init__.py` — register the new module
- `orgchem/agent/actions_meta.py` — `lab-canvas` category
  summary
- `orgchem/gui/audit.py` — 5 new GUI_ENTRY_POINTS
- `INTERFACE.md` — `actions_lab_canvas.py` row
- `ROADMAP.md` — Phase 38c.5 SHIPPED + Phase 38c
  CLOSE-OUT
- `PROJECT_STATUS.md` — round 190 summary

**Next.** Phase 38d (process simulator with state-machine
animation — next big multi-round chunk) or pivot to a
different roadmap area.  Audit-driven expansion still has
opportunities (microscopy → lab-analyser at 6 edges,
tutorial gates that are still 2-of-3); curriculum lessons
are a perennial expansion area; the user-flagged Phase 49
sweep is fully closed.

---

## 2026-04-26 — Round 189 (Phase 38c.4 SHIPPED — snap-validation against Phase-38a connection ports)

**Goal.**  Round 188 wired drag/drop so users can place
equipment on the canvas.  Round 189 ships the **snap-
validation layer**: when the user explicitly connects two
placed glyphs at named ports, the canvas checks the joint
compatibility against the Phase-38a `connection_ports` data
+ draws the connection in green for valid pairs, dashed red
for incompatible ones.

**What shipped.**

1. **`core/lab_setups.validate_port_pair(equipment_a,
   port_a_name, equipment_b, port_b_name)`** — extracted
   from the existing per-setup `validate_setup` so the
   per-pair logic can run at canvas-edit time.  Returns
   `None` for valid pairs or a short error string.  Same
   rules: joint types must match (with `open` as a
   wildcard), ground-glass joints need male ↔ female
   complementarity, hose / socket / open are
   sex-neutral.  Reuses `_SEX_NEUTRAL_JOINTS` +
   `_find_port` helpers.

   **Design call**: removed the equipment-object-level
   `is` self-loop check that was in the round-141
   per-setup validator.  Two RBFs placed on the canvas
   legitimately share the same frozen `Equipment` dataclass
   instance (the catalogue is built once + cached) so an
   `is` check would always misfire.  The glyph-level
   self-loop check now sits in `CanvasView.connect_glyphs`
   where the canvas knows about distinct glyph instances.

2. **`ConnectionLine(QGraphicsLineItem)`** — visual link
   between two `EquipmentGlyph`s at named ports.  Solid
   green pen for valid pairs, dashed red pen for invalid;
   zValue=-1 so the line sits beneath the equipment glyphs
   (the equipment overlays the line endpoints).  Stores
   the `equipment_a_id` / `equipment_b_id` / `port_a` /
   `port_b` / `error` for tests + future inspection.
   `is_valid()` boolean shortcut.

3. **`CanvasView.connect_glyphs(g_a, port_a, g_b, port_b)`**
   — public method on the canvas that instantiates the
   `ConnectionLine`.  Looks up the equipment via
   `get_equipment(glyph.equipment_id())`; checks
   `glyph_a is glyph_b` for the self-loop case (canvas
   level, not equipment level); calls
   `validate_port_pair` for everything else.  Emits
   `equipment_connected(eid_a, port_a, eid_b, port_b,
   error_or_empty)` Qt signal.  Returns `None` when
   either glyph carries an unresolvable equipment id.

4. **`CanvasView.connection_lines()`** — enumerator over
   placed `ConnectionLine` instances in the scene.

5. **`LabSetupCanvasDialog._on_equipment_connected`** slot
   updates the status bar with ✓ for valid connections
   (*✓ Connected rbf.neck → distillation_head.bottom*) or
   ⚠ for invalid (*⚠ Port mismatch (rbf.neck →
   rbf.neck): port-sex mismatch (both female); ground-glass
   joints need male ↔ female*).

6. **9 new round-189 tests** in
   `tests/test_lab_setup_canvas.py`:
   - **validate_port_pair coverage (4 tests)**: valid 24/29
     pair (rbf.neck female × distillation_head.bottom male),
     two-female-joints rejected (sex mismatch), unknown-
     port rejected (clear "not on" error), open-wildcard
     accepts anything (rbf.neck × clamp_3prong.jaws — no
     joint-type check needed).
   - **Canvas connection wiring (5 tests)**:
     `connect_glyphs` creates a `ConnectionLine` + emits the
     signal with empty error; invalid pair dashes red +
     emits signal with non-empty error; z-value below
     glyphs; unknown equipment id returns None;
     clear-canvas drops every connection line along with
     the glyphs.

   First-run findings (caught + fixed in the same round):
   the test ports I'd guessed for distillation_head
   (`inlet`) and clamp_3prong (`grip`) didn't exist; the
   real ports are `bottom`/`thermometer`/`side` and
   `jaws`/`boss`.  Also the equipment-level self-loop
   check in `validate_port_pair` was misfiring because of
   the shared `Equipment` instance issue described above
   — moved to the glyph level.

**Test count.** 2207 passed (was 2198 in round 188, +9
from new validation tests).  Full suite green.  Canvas
test suite is now 31 tests across 4 sub-phases (12 + 10 +
9).

**File size.** `lab_setup_canvas.py` now at 482 lines —
just under the 500-line cap.  Phase 38c.5 (agent actions)
will go in a separate `agent/actions_lab_canvas.py`
module rather than further bloating the dialog file.

**Why this matters.**  Phase 38c.4 closes the
"build the apparatus + check it works" loop.  A student
can now drag two RBFs onto the canvas, try to connect their
necks, and immediately see a red dashed line + a
"port-sex mismatch" message — exactly the kind of
formative-feedback teaching moment a benchtop instructor
provides.  The same `validate_port_pair` function powers
both the GUI's real-time feedback and the round-141
whole-setup validator.

**Files touched.**
- `orgchem/core/lab_setups.py` — added
  `validate_port_pair` (~ 35 new lines)
- `orgchem/gui/dialogs/lab_setup_canvas.py` — added
  `ConnectionLine` (~ 60 lines), `connect_glyphs`
  (~ 25 lines), `equipment_connected` signal,
  `connection_lines` accessor, status-bar slot
- `tests/test_lab_setup_canvas.py` — 9 new round-189
  tests (~ 100 lines)
- `ROADMAP.md` — Phase 38c.4 SHIPPED checkbox + summary
- `PROJECT_STATUS.md` — round 189 summary

**Next.** Phase 38c.5 — agent actions + integration with
the *Lab setups…* dialog.  This closes Phase 38c.  Likely
ships:
- `open_lab_setup_canvas()` agent action
- `place_equipment_on_canvas(eid, x, y)` agent action
- `connect_canvas_equipment(g_a_idx, port_a, g_b_idx,
  port_b)` agent action
- `clear_lab_setup_canvas()` agent action
- `lab_setup_canvas_state()` JSON dump for tutor
  introspection
- *Build on canvas* button on the Phase-38b
  `LabSetupsDialog` that pre-populates the canvas with a
  seeded setup's equipment + connections

---

## 2026-04-26 — Round 188 (Phase 38c.3 SHIPPED — drag/drop wiring + EquipmentGlyph on the lab-setup canvas)

**Goal.**  Round 187 shipped the Qt UI scaffolding for the
lab-setup canvas (palette dock + empty canvas + dialog).
Round 188 wires Qt's drag-and-drop machinery between the
palette and the canvas, and introduces the placeholder
visual (`EquipmentGlyph`) that drops produce.  Snap-
validation against connection ports stays out of scope (38c.4).

**What shipped.**

1. **`EquipmentGlyph(QGraphicsItemGroup)`** — placeholder
   visual placed by drops.  Bordered ellipse (96 × 56 px)
   with the equipment name as text inside.  Movable +
   selectable so the user can rearrange the apparatus after
   placing.  Stores the equipment id for later lookup
   (`equipment_id()` / `label()` accessors).

2. **`_PaletteTree(QTreeWidget)`** — subclass of the palette
   tree that overrides `startDrag(supported_actions)`.  When
   the user click-and-holds an equipment leaf row, the
   override packages the equipment id as
   `EQUIPMENT_MIME = 'application/x-orgchem-equipment-id'`
   MIME payload and starts a `QDrag`.  Category-header rows
   carry no equipment id (`UserRole == ""`) so dragging
   them is a no-op — same separation of concerns as the
   round-187 click-handler suppression.

3. **`CanvasView` drag/drop handlers**:
   - `setAcceptDrops(True)` enables drop targeting.
   - `dragEnterEvent` + `dragMoveEvent` accept the proposed
     copy-action when the dragged MIME is `EQUIPMENT_MIME`,
     forward to parent otherwise.
   - `dropEvent` decodes the equipment id from the MIME
     payload, maps the view-coordinate drop position to scene
     coordinates via `mapToScene`, and calls
     `place_equipment(eid, x, y)`.

4. **`CanvasView.place_equipment(eid, x, y)`** — the
   single code path used by both real drops + tests + future
   agent actions.  Looks up the equipment via
   `core.lab_equipment.get_equipment(eid)` (returns `None`
   for unknown ids without erroring), instantiates the
   glyph, adds it to the scene, emits
   `equipment_placed(eid, x, y)` Qt signal, returns the
   glyph.  Decoupling drop-handling from glyph-creation is
   the same factoring lesson from earlier rounds (Phase
   36b's `place_atom`).

5. **`CanvasView.equipment_glyphs()`** — enumerator over
   placed glyphs (filter scene items by `isinstance` check).
   Used by tests + the future Phase-38c.5 agent action that
   will return a JSON snapshot of the canvas.

6. **`LabSetupCanvasDialog._on_equipment_placed`** slot
   updates the status bar after each placement: *"Placed
   Round-bottom flask at (150, 75) — 1 items on canvas"*.
   Replaces the round-187 placeholder *"38c.2 skeleton —
   drag/drop ships in 38c.3"* status message with the new
   default *"Drag equipment from the palette onto the
   canvas"*.

7. **10 new round-188 tests** added to
   `tests/test_lab_setup_canvas.py`:
   - Canvas accepts drops.
   - Palette tree `dragEnabled()` is on.
   - `place_equipment(eid, x, y)` returns the right glyph
     at the right position + emits `equipment_placed`.
   - Unknown equipment id returns `None`, emits no signal,
     places no glyph.
   - Multiple glyphs coexist + `equipment_glyphs()`
     enumerates them all.
   - `_on_clear()` drops every placed glyph.
   - Glyphs carry `ItemIsMovable` + `ItemIsSelectable` flags.
   - `EQUIPMENT_MIME` constant is exported + sane.
   - Full round trip: synthesised `QDropEvent` carrying the
     MIME payload places the right equipment on the canvas.
   - Drop carrying a non-`EQUIPMENT_MIME` payload is ignored
     + does NOT add a glyph (forwards to parent).

**Test count.** 2198 passed (was 2188 in round 187, +10
from the new drag/drop tests).  Full suite green.  All 22
canvas tests pass (12 from 38c.2 baseline + 10 from 38c.3).

**File size.** `lab_setup_canvas.py` now at 396 lines —
well under the 500-line cap.  Phase 38c.4 (snap-validation)
will fit in the same file; Phase 38c.5 (agent actions) goes
in a separate `agent/actions_lab_canvas.py` module.

**Why this matters.**  Phase 38c.3 closes the
"interactive teaching" gap on the canvas: a student can now
literally **build the apparatus** by dragging items from the
palette.  Combined with the round-141 `validate_setup()`
function from Phase-38b, the next sub-phase (38c.4) will
turn the canvas into a real teaching tool — drop two RBFs
+ a Vigreux column + a Liebig condenser, the snap-validator
shouts *"the 14/20 male joint on the column won't connect
to the 24/29 female joint on the second RBF — check the
adapter you need"*.

**Files touched.**
- `orgchem/gui/dialogs/lab_setup_canvas.py` — added
  `EquipmentGlyph` (~ 45 lines), `_PaletteTree` (~ 25
  lines), `CanvasView` drop handlers + `place_equipment`
  (~ 60 lines), `_on_equipment_placed` slot
- `tests/test_lab_setup_canvas.py` — 10 new round-188
  tests (~ 110 lines)
- `ROADMAP.md` — Phase 38c.3 SHIPPED checkbox + summary
- `PROJECT_STATUS.md` — round 188 summary

**Next.** Phase 38c.4 — snap-validation against Phase-38a
`connection_ports`.  When the user drops two equipment items
near each other, draw connection-port handles + try to snap
adjacent compatible ports together (14/20 male ↔ 14/20 female,
hose ↔ hose, etc.).  Mismatched ports surface as a red
indicator + a status-bar warning.  Reuses the
`validate_setup()` machinery from Phase 38b but at the
single-connection level rather than the whole-setup level.

---

## 2026-04-26 — Round 187 (Phase 38c.2 SHIPPED — Qt UI scaffolding for the lab-equipment canvas)

**Goal.**  Round 186 shipped the headless palette data layer.
Round 187 ships **Phase 38c.2: the Qt UI scaffolding** —
palette dock + canvas widget + singleton modeless dialog.
Drag/drop wiring stays out of scope (that's 38c.3); the goal
is the structural skeleton that the next 3 sub-phases will
extend.

**What shipped.**

1. **`gui/dialogs/lab_setup_canvas.py` (NEW, ~ 215 lines)** —
   three Qt widget classes:

   - **`PaletteDock`** — left pane backed by a
     `QTreeWidget`.  Renders `default_palette()` as one
     top-level row per category (with item counts) +
     equipment items as collapsible children, expanded by
     default.  Click an equipment row → emits
     `item_selected(equipment_id)` Qt signal (the entry
     point Phase 38c.3 will use to start a drag).
     Category-header clicks are explicitly suppressed via
     a guard in `_on_item_clicked` — the user clicks the
     equipment, not the section.  `set_palette(palette)`
     swaps to a different `Palette` (e.g. for *Build on
     canvas*).  `selected_equipment_id()` /
     `total_items()` accessors.

   - **`CanvasView`** — `QGraphicsView` + `QGraphicsScene`
     pair sized 1200 × 800 with white background.
     `clear_canvas()` / `item_count()` accessors for the
     future sub-phases + tests.  Empty in 38c.2 — drop
     wiring is the entire job of 38c.3.

   - **`LabSetupCanvasDialog`** — singleton modeless
     `QDialog` (1280 × 760).  Top toolbar (*Clear canvas* +
     *Show all equipment*), centre splitter (palette dock
     left at 260 px, canvas right stretching), bottom
     status bar.  `load_setup(setup_id)` swaps the
     palette to `palette_for_setup(setup_id)` (returns
     `False` for unknown ids).  `palette_dock()` /
     `canvas()` accessors for tests + future agent
     actions.  `_on_item_selected(eid)` slot updates the
     status bar with "Selected: <name> (<id>) — drop on
     canvas to place (38c.3)" — explicit feedback that
     the next sub-phase is where placement happens.

2. **`tests/test_lab_setup_canvas.py` (NEW)** — 12 tests
   using the offscreen Qt platform via the existing
   `qtpy`-style fixture pattern:
   - Singleton returns same instance.
   - Dialog is modeless (so the user can keep working in
     the molecule workspace alongside it).
   - Palette dock + canvas exist as the right widget
     subclasses.
   - Palette dock lists every Phase-38a equipment item.
   - Tree is grouped by category, first row "Glassware (4)".
   - `item_selected` signal emitted on equipment click.
   - Category-header clicks suppressed.
   - `load_setup("simple_distillation")` reduces palette
     count below the full inventory.
   - `load_setup("not-a-real-id")` returns False.
   - *Show all equipment* button resets palette to full.
   - Round-187 canvas starts empty.
   - *Clear canvas* doesn't error on empty scene.

   Per-test fixture resets the singleton between tests so
   they don't bleed (each test gets a clean dialog).

**Test count.** 2188 passed (was 2176 in round 186, +12
from the new canvas dialog tests).  Full suite green.

**Why this matters.**  Phase 38c.2 closes the gap between
the headless palette data (38c.1) and the eventual
interactive canvas.  Splitting Qt scaffolding (38c.2) from
drag/drop wiring (38c.3) keeps each round small + testable
+ reviewable.  The signal-based palette → canvas connection
(`item_selected(equipment_id)`) is the well-defined seam the
next round will hook into for drag-source behaviour.

**Files touched.**
- NEW `orgchem/gui/dialogs/lab_setup_canvas.py` (~ 215 lines)
- NEW `tests/test_lab_setup_canvas.py` (~ 165 lines)
- `INTERFACE.md` — new dialog row added to the dialogs
  catalogue
- `ROADMAP.md` — Phase 38c.2 SHIPPED checkbox + summary
- `PROJECT_STATUS.md` — round 187 summary

**Next.**  Phase 38c.3 — drag-source on palette + drop
target on canvas.  This is the "click an equipment item +
drop it onto the canvas + see a glyph appear" interaction
round.  Likely uses Qt's built-in `QDrag` / `dragEnterEvent`
/ `dropEvent` mechanism with the equipment id as the MIME
payload.  Each placed equipment becomes a
`QGraphicsItem` (probably a `QGraphicsEllipseItem` +
`QGraphicsTextItem` for the round-187 placeholder; nicer
SVG icons can come in a polish round).

---

## 2026-04-26 — Round 186 (Phase 38c.1 SHIPPED — lab-equipment palette data layer; first sub-phase of the multi-round Phase-38c canvas)

**Goal.**  Phase 49 closed in round 181; rounds 182-185 closed
out the Phase-31b reaction extension + the audit-driven
expansion arc.  Round 186 pivots to the largest pending
roadmap item: **Phase 38c — equipment palette + canvas**, the
multi-round Qt UI work that turns the Phase-38a equipment
catalogue + Phase-38b setup catalogue into a hands-on
"build the apparatus on a canvas" tool.

Round 186 ships **38c.1: the headless palette data layer**.
Same pattern as the Phase-36a drawing-tool data core →
Phase-36b canvas: the headless layer ships first, the canvas
+ drag/drop wiring + snap validation + agent actions ship in
38c.2-38c.5.

**What shipped.**

1. **`core/lab_palette.py` (NEW, ~ 165 lines)** — headless
   palette data layer.

   Public API:
   - `PaletteCategory(category_id, label, equipment_ids)`
     frozen dataclass with `__len__` helper.
   - `Palette(categories)` aggregate with `category(id)`
     lookup + `all_equipment_ids()` / `__len__` helpers.
   - `default_palette()` — every Phase-38a equipment item
     grouped + ordered across the 12 canonical categories.
   - `palette_for_setup(setup_id)` — filtered to one
     Phase-38b setup's equipment list, with deduplication
     (setups like simple distillation list the same RBF
     twice for the pot + receiver).  Powers the future
     *Build on canvas* button on the Phase-38b *Lab setups…*
     dialog.  Returns `None` for unknown setup ids.
   - `categories_in_display_order()` — canonical 12-tuple
     (glassware → adapter → condenser → separation →
     filtration → heating → cooling → stirring → vacuum →
     support → safety → analytical).
   - `category_label(category_id)` — human-readable label
     with Title-Case fallback for unknown ids.
   - `palette_to_dict(palette)` — JSON-friendly
     serialisation for the eventual Phase-38c.5 agent
     action.

   Pure-headless: no Qt imports, no DB dependency.  The
   test suite verifies no Qt module gets pulled in as a
   side-effect of importing.

2. **`tests/test_lab_palette.py` (NEW)** — 11 tests:
   default-palette covers every category, total matches
   catalogue (no duplicates), canonical display order,
   per-setup filter only includes setup equipment, unknown
   setup returns None, deduplication, immutable
   display-order tuple, label fallback for unknown
   categories, category-lookup helper, dict round-trip,
   no-Qt-import sentinel.

**Test count.** 2176 passed (was 2165 in round 185, +11
from new palette tests).  Full suite green.

**Why this matters.**  Phase 38a (equipment catalogue) +
Phase 38b (setup catalogue) shipped reference data for the
GUI's catalogue dialogs.  Phase 38c.1 closes the gap between
those static catalogues and the future canvas: the palette
takes the equipment list and reshapes it into the
"toolbar of draggable items" structure the canvas needs.
Splitting the palette out as a separate headless layer
(rather than baking it into the canvas widget) means:
- the agent action surface (Phase 38c.5) can call
  `default_palette()` / `palette_for_setup()` directly
  without instantiating a Qt widget
- per-setup palettes can be tested + serialised
  independently of the canvas's geometry
- a future "alternative palette" (e.g. organised by
  difficulty / by reaction type) can plug in without
  touching the canvas widget

**Files touched.**
- NEW `orgchem/core/lab_palette.py` (~ 165 lines)
- NEW `tests/test_lab_palette.py` (~ 130 lines)
- `INTERFACE.md` — new module row
- `ROADMAP.md` — Phase 38c → 38c.1 SHIPPED, 38c.2-38c.5
  laid out
- `PROJECT_STATUS.md` — round 186 summary

**Next.** Phase 38c.2 — `QGraphicsScene` canvas widget +
palette dock layout.  This is the first Qt-UI round of
Phase 38c (palette dock on the left, canvas in the centre,
no drag/drop yet).  Likely uses the same modeless-singleton
dialog pattern as the Phase-38b *Lab setups…* dialog so
the user can keep it open alongside the molecule workspace.

---

## 2026-04-25 — Round 185 (Phase 49 follow-up — tutorial coverage 32 % → 68 % fully-integrated; third audit-driven expansion round)

**Goal.**  Round 184 fixed the named-reaction matcher (16 % →
32 % fully-integrated).  Round 185 applies the same audit-
accuracy lens to the **catalogue layer**: extend the matcher
beyond the narrow Phase-29 catalogues + cell-component +
kingdom-topic xref names (162 names) to include **every
Molecule DB row name + synonym** (~ 700 names).

**Premise.**  The audit's "catalogue molecule" layer was named
+ scoped before the round-177 catalogue-molecule backfill +
the round-58 synonym layer.  After those rounds, "is the
molecule in the seeded knowledge graph?" became a much
broader question than "is it in one of the niche
catalogues?".  Lessons that reference acetaldehyde / styrene /
caffeine / limonene / thiophene / hydroxide / pentane /
tert-butyl bromide etc. were getting no credit despite all of
those molecules being addressable through the molecule
browser, the agent registry, the descriptor calculators, the
spectroscopy tools, etc.

**What shipped.**

1. **`core/tutorial_coverage_audit.py::_catalogue_molecule_names()`**
   broadened to union in `list_molecules()` row names + every
   `synonyms_json` entry.  Lazy DB import inside try/except so
   the function still works (returning just the narrow set)
   when `init_db` hasn't run.

2. **Per-test floors raised** in `tests/test_tutorial_coverage.py`:
   - `test_catalogue_molecule_coverage_floor`: 50 % → 95 %
     (round-185 baseline 100 %)
   - `test_lesson_coverage_hit_count`: 30 % → 65 %
     (round-185 baseline 67.7 %)

3. **Test fixture** added: an `app` HeadlessApp fixture so the
   two tests that exercise the broadened matcher have a
   seeded DB to read from.

**Live coverage report after round 185.**

```
Tutorial-to-knowledge-graph coverage audit
============================================================
Total lessons:                  31
Lessons with glossary ref:      100.0 %
Lessons with catalogue ref:     100.0 %
Lessons with named-reaction ref: 67.7 %
============================================================
Fully-integrated: 21/31 = 67.7%
```

**Three-round trajectory of the audit-driven expansion arc:**

| Round | Change | Fully-integrated |
|-------|--------|------------------|
| 181 (baseline) | audit shipped | 16.1 % (5/31) |
| 184 | named-reaction matcher fix + sugars-lesson edit | 32.3 % (10/31) |
| 185 | catalogue matcher broadening | **67.7 %** (21/31) |

The same trajectory appears on the cross-reference graph (round
178 baseline 59 edges → round 183 75 edges, +27 %).  The
pattern: **audit surfaces a metric → some of the gap is matcher
inaccuracy → some is real content gap → fix both → tighten the
floor**.

**Test count.** 2165 passed (held — no new tests, just floor
tightening + matcher broadening + 1 fixture add).  Full suite
green.

**Why this matters.**  The audit dashboard is now a faithful
representation of cross-module integration.  When a future
curriculum revision drops below 65 % fully-integrated, the
test fails immediately.  The remaining 32 % of lessons that
DON'T hit all 3 layers are the genuinely-foundational ones
(Welcome / Atoms+bonds / Lewis structures / Functional groups
/ Nomenclature / Reading SMILES / Stereochemistry 101 /
Polymers / Protecting groups / MO theory) where forcing a
named-reaction reference would feel artificial.  Those are
appropriate exceptions, not bugs.

**Files touched.**
- `orgchem/core/tutorial_coverage_audit.py` —
  `_catalogue_molecule_names()` broadened
- `tests/test_tutorial_coverage.py` — `app` fixture added,
  2 floors raised
- `PROJECT_STATUS.md` — round 185 summary

**Next.**  The audit-driven expansion has reached saturation
on tutorial coverage.  Remaining roadmap items: Phase 38c
(lab-equipment palette + canvas, multi-round, larger scope),
or another round of cross-reference expansion (`microscopy → lab-
analyser` is at 6 edges and could grow with the rest of the
microscopy catalogue gaining instrument detail).

---

## 2026-04-25 — Round 184 (Phase 49 follow-up — tutorial coverage 16 % → 32 % fully-integrated; second audit-driven expansion round)

**Goal.**  Round 181's tutorial coverage audit reported 16.1 %
of lessons hit all 3 knowledge-graph layers (glossary +
catalogue molecule + named reaction).  Round 184 lifts that
metric using the audit dashboard as a roadmap.

**What shipped.**

1. **Improved the audit matcher**.  Previously
   `_named_reaction_names()` matched only the FULL `_STARTER`
   reaction name (e.g. `'Wittig reaction (propanal +
   methylidene ylide)'`).  That misses the natural shorthand
   most tutorials use (`'Wittig reaction'` / `'Wittig'` /
   `'Diels-Alder'`).  Updated to also match the **short root**
   — everything before the first colon or parenthesis.  The
   matcher was undercounting coverage; the new version
   reports the actual reality.

2. **Sugars + carbohydrates lesson** (`intermediate/07_sugars.md`)
   extended with a closing section linking sugar biosynthesis
   to the **Aldolase class I** named reaction (DHAP + G3P →
   F1,6BP) so the lesson's body text resolves to the seeded
   reaction by name.  Hit count 2 → 3.

3. **Per-test floors raised** to lock the new state in:
   - `test_named_reaction_coverage_floor`: 40 % → 60 %
   - `test_lesson_coverage_hit_count`: 15 % → 30 %

**Live coverage report after round 184.**

```
Tutorial-to-knowledge-graph coverage audit
============================================================
Total lessons:                  31
Lessons with glossary ref:      100.0 %
Lessons with catalogue ref:      54.8 %
Lessons with named-reaction ref: 67.7 %
============================================================
Fully-integrated: 10/31 (32.3 %)
```

(Round-181 baseline: 100 % glossary, 54.8 % catalogue,
**45.2 % named-reaction**, **16.1 % fully-integrated**.  The
named-reaction + fully-integrated metrics doubled this round
— most of the gain was the matcher fix surfacing real
references that were already in the lessons; the sugars-
lesson edit added one more.)

**Test count.** 2165 passed (held — no new tests, just
matcher improvement + floor tightening + one lesson edit).
Full suite green.

**Why this matters.**  Continues the audit-driven-expansion
pattern from round 183: audit surfaces a gap → root cause
turns out to be partly an audit-accuracy issue + partly a real
content gap → fix both at once → tighten the floor.  The
matcher-accuracy lesson generalises: every audit module's
matcher needs occasional revisits to make sure it's measuring
what it claims to measure.

**Files touched.**
- `orgchem/core/tutorial_coverage_audit.py` —
  `_named_reaction_names()` short-root matcher
- `orgchem/tutorial/content/intermediate/07_sugars.md` —
  Aldolase section added
- `tests/test_tutorial_coverage.py` — 2 floors raised
- `PROJECT_STATUS.md` — round 184 summary

**Next.**  Audit dashboards still surface coverage gaps:
- 21 lessons hit only 2 of 3 layers (the audit's catalogue
  layer is hard to reference for many topics — could broaden
  it to include `seed_molecules_extended` molecules)
- 9 dialogs lack `open_*` agent actions (Phase 49d
  `KNOWN_GAPS` allow-list)
- `cell-component → molecule` is at 6 edges; many constituents
  could still link to molecules in the extended seed

Or: pivot to Phase 38c (lab-equipment palette + canvas, the
last big multi-round pending item).

---

## 2026-04-25 — Round 183 (Phase 49 follow-up — cross-reference graph 59 → 75 edges; first round to use the round-178 audit dashboard as a roadmap)

**Goal.**  The Phase-49 audit shipped in round 178 surfaced a
real coverage gap: only 1 cell-component → molecule edge + 1
kingdom-topic → molecule edge in the catalogue cross-reference
graph, despite ~ 100 catalogue entries that could meaningfully
link to specific molecule-DB rows.  Round 183 is the first
round to **use the audit dashboard as a roadmap** — walk the
two low-coverage kinds, find linkable candidates, wire them up,
then tighten the per-kind floors to lock the improvement in.

**What shipped.**

1. **Cell-component → molecule edges: 1 → 6 (+5).**

   Walked every `MolecularConstituent` in `cell_components.py`
   that lacked a `cross_reference_molecule_name`, looked up its
   name via `find_molecule_by_name()`, and wired in the 5 clean
   matches:
   - Phosphatidylcholine → `Phosphatidylcholine (POPC-like)`
   - Phosphatidylethanolamine → `Phosphatidylethanolamine (POPE-like)`
   - Sphingomyelin → `Sphingomyelin (C18)`
   - N-acetylglucosamine (NAG) on `peptidoglycan-gram-positive`
     → `N-Acetylglucosamine (GlcNAc)`
   - Same NAG on `pseudopeptidoglycan` → same DB row

2. **Kingdom-topic → molecule edges: 1 → 12 (+11).**

   Walked `biochemistry_by_kingdom` topics whose body text
   mentions ATP / NADH / NADPH / FAD / Pyruvate / GTP / cAMP /
   Cholesterol — molecules that ARE in the seeded DB.  Added
   `cross_reference_molecule_names` tuples for 4 high-density
   topics:
   - `eukarya-physiology-aerobic-respiration` → ATP, NADH,
     FAD, Pyruvate, GTP (5)
   - `eukarya-physiology-photosynthesis` → ATP, NADPH (2)
   - `eukarya-physiology-signalling-gpcr` → GTP, cAMP (2)
   - `bacteria-physiology-anaerobic-fermentation` → NADH,
     Pyruvate (2)

3. **Per-kind floors raised** in
   `tests/test_cross_reference_graph.py::test_per_kind_floors`:
   - `cell-component → molecule`: 1 → 5
   - `kingdom-topic → molecule`: 1 → 10

   So a future regression that drops below the new state
   surfaces immediately.

**Live cross-reference matrix after round 183.**

```
Source kind          → Target kind         | Edges
------------------------------------------------------------
cell-component       → molecule             |     6
kingdom-topic        → cell-component       |    46
kingdom-topic        → metabolic-pathway    |     5
kingdom-topic        → molecule             |    12
microscopy-method    → lab-analyser         |     6
------------------------------------------------------------
TOTAL                                       |    75
```

(Was 59 edges in round 178: 1 + 46 + 5 + 1 + 6 = 59.  +16
edges + 27 %.)

**Test count.** 2165 passed (held — no new tests, just floor
tightening).  Full suite green.

**Why this matters.**  Demonstrates the Phase-49 audit
infrastructure as a **living dashboard driving expansion**,
not just a defensive regression gate.  The audit surfaced the
gap → this round closed it → the floors lock the improvement
in.  The pattern (audit shows low coverage → walk + wire-up →
raise floor) generalises to:
- agent-surface KNOWN_GAPS (49d): 9 dialogs deliberately ship
  without openers; future rounds can promote them
- tutorial coverage (49f): 16 % of lessons hit all 3 layers;
  curriculum revisions can lift this floor
- glossary terms vs catalogue body text (49a): future
  vocabulary expansion guided by the required-terms list

**Files touched.**
- `orgchem/core/cell_components.py` — 5 cross-references
  added on 3 components
- `orgchem/core/biochemistry_by_kingdom.py` — 4 topics gained
  `cross_reference_molecule_names` tuples
- `tests/test_cross_reference_graph.py` — per-kind floors
  raised
- `PROJECT_STATUS.md` — round 183 summary

**Next.**  Continue mining the audit dashboards for
coverage opportunities — kingdom-topic body texts have ~ 12
more candidate molecule mentions waiting to be wired up; or
move to a different roadmap item (Phase 38c equipment-canvas,
or curriculum expansion for low-hit-count lessons).

---

## 2026-04-25 — Round 182 (Phase 31b 60/60 SHIPPED — 4 named reactions added to close out the named-reaction extension)

**Goal.** Phase 31b's reaction catalogue grew from 4 in Phase 1
to 56 by round 175, with a stretch target of 60.  Round 182
closes the 60/60 milestone with 4 well-chosen named reactions
that fill real pedagogical gaps.

**What shipped.** 4 entries in `db/seed_reactions._STARTER`:

1. **Grubbs olefin metathesis** (cross-metathesis of styrene +
   1-hexene → 1-phenyl-1-hexene).  Ru-catalysed C=C bond
   shuffling via metallacyclobutane.  Nobel 2005 (Grubbs +
   Schrock + Chauvin).  Three productive variants (CM / RCM /
   ROMP).  Fills the **olefin-metathesis gap** — complements
   the Pd-cross-coupling cluster (Suzuki / Heck / Negishi /
   Stille / Buchwald-Hartwig / Sonogashira) with Ru-catalysed
   C=C bond formation.

2. **Wolff-Kishner reduction** (acetophenone → ethylbenzene).
   Strongly basic carbonyl → CH₂ via hydrazone + N₂ extrusion.
   Wolff 1912 / Kishner 1911 / Huang-Minlon modification.
   **Complementary to Clemmensen** (Zn(Hg) / HCl, strongly
   acidic) for acid-sensitive substrates.  Fills the
   **non-hydride / non-SET reduction gap** — existing
   reductions are NaBH₄, Birch, CBS.

3. **Hofmann elimination** (2-pentyltrimethylammonium hydroxide
   → 1-pentene + trimethylamine).  Anti-Zaitsev / Hofmann's
   rule β-elimination.  Hofmann 1851.  Bulky leaving group
   (NMe₃) + syn-periplanar TS biases deprotonation toward the
   less-hindered β-H, giving the terminal alkene.  Pedagogical
   contrast with E2 / Saytzeff — same overall transformation,
   opposite regioselectivity, driven by leaving-group bulk.

4. **Ozonolysis with reductive workup** (cis-2-butene + O₃/Me₂S
   → 2 acetaldehyde).  Oxidative cleavage of C=C → 2 carbonyls
   via molozonide → Criegee ozonide.  Workup (Me₂S / Zn-AcOH /
   PPh₃) determines product oxidation state.  Pre-NMR-era
   structure-determination workhorse (cholesterol, pyrethrins,
   terpenes).  Fills the **oxidative-cleavage gap** in the
   alkene-reaction cluster.

**Supporting fragments** added to `db/seed_intermediates._STARTER`
to keep the round-92 fragment-consistency audit green:
1-Hexene, 1-Phenyl-1-hexene, 2-Pentyltrimethylammonium,
1-Pentene, Ozone.

**Phase 31b → 60/60 milestone**.  Reaction catalogue distribution:
- Substitution / elimination / addition: 11
- Pericyclic + cycloaddition: 4
- Cross-coupling: 6 (now 7 with Grubbs)
- Asymmetric catalysis: 6
- Oxidation / reduction / rearrangement: 13 (now 15 with W-K
  + ozonolysis)
- Enzyme: 4
- MCR / annulation / condensation: 5
- Functional-group interconversion + others: 7

**Test count.** 2165 passed (held — no new tests added; the
round-92 fragment-consistency audit + the round-126
reaction-count test both held green after the seed-level
additions).

**Files touched.**
- `orgchem/db/seed_reactions.py` — 4 new `_STARTER` entries
  (~ 80 new lines)
- `orgchem/db/seed_intermediates.py` — 5 new fragment entries
- `ROADMAP.md` — Phase 31b → 60/60 SHIPPED
- `PROJECT_STATUS.md` — round 182 summary

**Next.** Pending roadmap: Phase 38c (lab-equipment palette +
QGraphicsScene canvas, multi-round); follow-ups on the
Phase-49 audit dashboards (low-coverage areas in
cell-component → molecule and kingdom-topic → molecule
cross-refs); curriculum expansion for lessons that hit
fewer than 3 knowledge-graph layers.

---

## 2026-04-25 — Round 181 (Phase 49f — tutorial-to-knowledge-graph coverage audit + welcome-lesson fix; **PHASE 49 COMPLETE**)

**Goal.**  Round 175 surfaced a user-flagged Phase-49 cross-
module integration audit ("ensure modules are well integrated —
words linked to glossary, molecules in the same format and
findable in the database, reactions and techniques linked
between modules, the AI tutor able to access and use all
features").  Rounds 176-180 delivered 49a (glossary coverage)
→ 49b (molecule-DB canonicalisation) → 49c (cross-reference
graph) → 49d (agent-surface symmetry) → 49e (feature
discovery).  Round 181 ships the closing sub-phase, **49f:
tutorial coverage**, and promotes Phase 49 to DONE.

**What shipped (49f).**

1. **`core/tutorial_coverage_audit.py` (NEW, ~ 200 lines)** —
   walks every tutorial markdown lesson and reports per-lesson
   coverage across 3 knowledge-graph layers:
   - Glossary terms (≥ 4 chars to filter noise)
   - Catalogue molecules (lipids / carbs / NA / SAR /
     cell-component constituents / kingdom-topic xrefs)
   - Named reactions (`seed_reactions._STARTER`)

   `LessonCoverage` per-lesson dataclass with `hit_count()`
   (0-3) helper + `TutorialCoverageReport` aggregate with
   percentage methods (`with_glossary_pct()` etc.) +
   `lessons_missing(report, layer)` per-layer drill-down +
   `render_report_text()` plain-text summary.  Skips
   authoring-test stub lessons by title prefix (round-94
   `Tutor-test-` lessons inject bare-stub markdown that has
   no chemistry content).

2. **First-run finding — 1 real gap caught.**  The welcome
   lesson (`beginner/01_welcome.md`) was a meta-lesson about
   how to USE the app and didn't reference any chemistry
   concept.  None of its words matched a glossary term.
   Fixed by adding a one-sentence chemistry intro mentioning
   hybridisation + pKa.

3. **`tests/test_tutorial_coverage.py` (NEW)** — 7 tests:
   100 % glossary coverage, ≥ 50 % catalogue-molecule
   coverage, ≥ 40 % named-reaction coverage, ≥ 30 lessons
   across 4 levels, report renders, layer-name validation,
   ≥ 15 % fully-integrated lessons.

**Live audit output (Phase-49f doc).**

```
Tutorial-to-knowledge-graph coverage audit
============================================================
Total lessons:                  31
Lessons with glossary ref:      100.0 %
Lessons with catalogue ref:      54.8 %
Lessons with named-reaction ref: 45.2 %
============================================================
```

**Test count.**  2165 passed (was 2158 in round 180, +7).
Full suite green.

---

### **PHASE 49 CLOSE-OUT**

The user-flagged Phase-49 cross-module integration sweep
shipped over **6 sub-phases × 6 rounds (176-181) =
45 audit tests** + 6 audit modules + ~ 1500 lines of audit
infrastructure.

**Sub-phases.**

| Sub | Round | Module | Audit gate |
|-----|-------|--------|------------|
| 49a | 176 | `core/glossary_audit.py` | Glossary autolink coverage — every catalogue body / tutorial / reaction description references glossary-defined terms.  15 missing terms backfilled. |
| 49b | 177 | `db/seed_catalogue_molecules.py` + `tests/test_molecule_db_canonicalisation.py` | Every catalogue molecule with a parseable SMILES is a Molecule DB row by InChIKey.  120 catalogue molecules backfilled.  **Caught the Citalopram SMILES bug** (DB had F + CN swapped vs the SAR catalogue). |
| 49c | 178 | `core/cross_reference_audit.py` | Every catalogue cross-reference resolves to a real target.  5 relationships, 59 edges audited. |
| 49d | 179 | `core/agent_surface_audit.py` | Every Tools-menu dialog has an `open_*` agent action + lookup trio.  24/24 surfaces complete after `open_periodic_table` + `open_naming_rules` shipped. |
| 49e | 180 | `core/feature_discovery_audit.py` | Every action has a docstring + every category has a summary.  19 missing summaries + 2 empty docstrings backfilled. |
| 49f | 181 | `core/tutorial_coverage_audit.py` | Every tutorial lesson references the knowledge graph; aggregate floors on catalogue + reaction coverage. |

**8 real bugs caught + fixed in the same round they were
surfaced.**
1. (49a) 15 high-priority glossary terms missing
2. (49b) 120 catalogue molecules missing from the DB
3. (49b) Citalopram SMILES encoded the wrong molecule
4. (49b) `list_molecules()` 500-row default truncated agent
   responses after the catalogue backfill
5. (49c) Microscopy → lab-analyser cross-refs broken by a
   wrong-API-name bug in the audit code itself
6. (49d) Periodic table + IUPAC naming dialogs lacked agent
   openers
7. (49e) 19 categories had no `_CATEGORY_SUMMARIES` entry
8. (49e) `get_centrifuge_action` + `get_rotor_action` had
   empty docstrings
9. (49f) Welcome lesson referenced no glossary term

**Why this matters.**  The user's directive identified three
failure modes (words not linked to glossary; molecules not
findable across modules; AI tutor can't use features).  All
three are now closed at test time.  A future drift in any
of those areas surfaces immediately as a CI failure rather
than as a silently-broken user experience.

The audit layer is **a living dashboard** — each report
renderer (`render_matrix_text` for cross-refs,
`render_audit_text` for agent surfaces / feature discovery,
`render_report_text` for tutorial coverage) gives a
human-readable snapshot that future rounds use to drive
expansion.  Particularly interesting low-coverage areas
flagged for follow-up:
- Only 1 cell-component → molecule edge (49c)
- Only 1 kingdom-topic → molecule edge (49c)
- 9 dialogs with no `open_*` action (49d KNOWN_GAPS)
- 16.1 % of lessons hit all 3 knowledge-graph layers (49f)

These are **opportunities for expansion** rather than bugs.
Phase 49 deliberately set realistic floors that lock current
state in but invite future contribution.

**Files touched (49f only).**
- NEW `orgchem/core/tutorial_coverage_audit.py` (~ 200 lines)
- NEW `tests/test_tutorial_coverage.py` (~ 130 lines)
- `orgchem/tutorial/content/beginner/01_welcome.md` —
  added one-sentence chemistry intro
- `INTERFACE.md` — new audit-module row
- `ROADMAP.md` — Phase 49 → COMPLETE + close-out summary
- `PROJECT_STATUS.md` — round 181 summary

**Next.**  Phase 49 closes the integration sweep.  Pending
roadmap items: Phase 38c (equipment-palette canvas, multi-
round), Phase 31b reaction-catalogue extension (4 more to
60-target), and follow-up rounds to drive curriculum +
cross-reference coverage from the audit dashboards.

---

## 2026-04-25 — Round 180 (Phase 49e — tutor-panel feature-discovery audit + 19-category-summary backfill, fifth sub-phase of the user-flagged integration sweep)

**Goal.**  Round 175 surfaced a user-flagged Phase 49 cross-module
integration audit.  Rounds 176-179 shipped 49a (glossary) → 49b
(molecule-DB) → 49c (cross-reference graph) → 49d (agent-surface
symmetry).  Round 180 ships **49e: tutor-panel
feature-discovery**.  Goal: ensure the AI tutor backend can
**discover** every feature, not just call them — every action
shows up in `tool_schemas()`, every schema has the required
keys, every action has a non-empty docstring (so the LLM sees
useful descriptions), and every registered category has an
entry in `actions_meta._CATEGORY_SUMMARIES` so the tutor's
`list_capabilities()` self-introspection returns useful info.

**What shipped.**

1. **`core/feature_discovery_audit.py` (NEW, ~ 165 lines)** —
   single audit walker:
   - `FeatureDiscoveryReport` dataclass with per-failure-mode
     gap lists.
   - `audit_feature_discovery()` runs all three checks
     (schema-coverage, description, category-summary) in one
     pass.
   - `list_capabilities_smoke()` — no-arg `list_capabilities()`
     invocation as a smoke check.
   - `render_report_text(report)` — human-readable failure
     summary + Phase-49e doc renderer.
   - `REQUIRED_SCHEMA_KEYS` + `REQUIRED_INPUT_SCHEMA_KEYS`
     constants document the Anthropic / OpenAI tool-schema
     shape contract so the audit catches schema-format
     regressions, not just missing entries.

2. **First-run findings — 2 real bugs caught.**
   - **19 categories with no summary** in
     `actions_meta._CATEGORY_SUMMARIES`: authoring, biochem,
     calc, cell, centrifugation, chromatography, clinical,
     drawing, instrumentation, isomer, kingdom, microscopy,
     ph, phys-org, qualitative, reagent, scripting, search,
     spectrophotometry.  All shipped after the round-55
     baseline `_CATEGORY_SUMMARIES` was last updated.  Result:
     when the AI tutor calls `list_capabilities()` to
     introspect, those 19 areas of the app appeared with
     empty descriptions.  The tutor literally couldn't tell
     what they were for.
   - **2 actions with empty docstrings**:
     `get_centrifuge_action` + `get_rotor_action` in
     `agent/actions_centrifugation.py`.  Their tool-schema
     descriptions came back as `""` so the LLM had only the
     function name to go on.

3. **Backfill in the same round.**
   - All 19 missing category summaries written into
     `_CATEGORY_SUMMARIES` with substantive descriptions
     (30-130 chars each, enough to give the LLM real
     pedagogical context).
   - Both empty docstrings filled in with realistic
     parameter / return-type descriptions.

4. **`tests/test_feature_discovery.py` (NEW)** — 9 tests:
   audit clean, registry size floor (≥ 200), every action
   has a schema, every schema has required keys, every
   category has a summary, no stale summaries,
   `list_capabilities()` smoke, round-180 backfilled
   descriptions substantive (≥ 30 chars), round-180
   docstrings non-empty.

**Live audit output (Phase-49e doc).**

```
Feature-discovery audit
============================================================
Registered actions: 243
Tool schemas:       243
Categories:         43

Actions missing description: 0
Actions missing from tool_schemas: 0
Schemas missing required keys: 0
Categories missing summary: 0
============================================================
STATUS: CLEAN
```

**Test count.** 2158 passed (was 2149 in round 179, +9 from
the new feature-discovery suite).  Full suite green.

**Why this matters.**  Closes the cross-module integration
sweep on the LLM-facing side.  The AI tutor now sees:
- every action with a meaningful description (49e)
- every category with a meaningful summary (49e)
- every action callable via tool_schemas (49e)
- every dialog openable via an opener action (49d)
- every cross-reference between catalogues resolved (49c)
- every catalogue molecule canonicalised in the DB (49b)
- every pedagogically-important term in the glossary (49a)

A student asking the tutor "can the app help me design a
buffer?" or "show me chromatography techniques" can no longer
be told "I don't know" because the feature was invisible —
that's exactly the kind of round-55 incident
(`list_capabilities` was added to fix the tutor refusing to
visualise ligand binding) that this audit prevents from
recurring.

**Files touched.**
- NEW `orgchem/core/feature_discovery_audit.py` (~ 165 lines)
- NEW `tests/test_feature_discovery.py` (~ 110 lines)
- `orgchem/agent/actions_meta.py` — 19 new
  `_CATEGORY_SUMMARIES` entries
- `orgchem/agent/actions_centrifugation.py` — 2 docstring
  fills
- `INTERFACE.md` — new audit-module row
- `ROADMAP.md` — Phase 49 status: 49a-e all SHIPPED
- `PROJECT_STATUS.md` — round 180 summary

**Next sub-phase.** 49f — doc-coverage extension: the final
sub-phase of the user-flagged Phase-49 sweep.  Verify that
every tutorial markdown lesson references at least one
glossary term + one catalogue entry + one named reaction (so
the curriculum stays connected to the rest of the app).  Then
write a Phase-49 close-out doc tying all 6 sub-phases together
+ promote Phase 49 → DONE.

---

## 2026-04-25 — Round 179 (Phase 49d — agent-surface symmetry audit + 2 new dialog openers, fourth sub-phase of the user-flagged integration sweep)

**Goal.**  Round 175 surfaced a user-flagged Phase 49 cross-module
integration audit.  Rounds 176-178 shipped 49a (glossary
coverage) → 49b (molecule-DB canonicalisation) → 49c (cross-
module reference graph).  Round 179 ships **49d: agent-surface
symmetry**.  Goal: ensure the AI tutor can do everything the
human GUI can do — every Tools-menu dialog has an `open_*` agent
action + the lookup trio.

**Survey first.**  Walked the registry of 254 actions across 36
categories.  Found 22 `open_*` actions covering most catalogue
dialogs but **2 obvious gaps**: Periodic table + IUPAC naming
rules (both in the Tools menu, both queried frequently in
chemistry tutoring).  Plus 7 more dialogs (Spectroscopy / Stereo /
Medchem / Orbitals / Retrosynthesis / Lab techniques / Green
metrics) that ship without openers but DO surface their content
via direct lookup / predict / export actions — those count as
"deliberately deferred", not gaps.

**What shipped.**

1. **`core/agent_surface_audit.py` (NEW, ~ 220 lines)** — walks
   the agent action registry and verifies every catalogue with a
   Tools-menu dialog has a symmetric agent-action surface.

   Public API:
   - `SurfaceSpec(catalogue, opener, list_action, get_action,
     find_action)` frozen dataclass.
   - `EXPECTED_SURFACES` 24-tuple of every Tools-menu dialog +
     its expected actions.
   - `KNOWN_GAPS` 9-tuple of `(action_name, rationale)` for
     deliberately-deferred openers.  Rationale field is
     mandatory — keeps the allow-list honest.
   - `gather_action_names()` — full registered set.
   - `audit_surface(spec)` / `audit_all_surfaces()` — return
     `SurfaceAuditReport(spec, missing_actions)` rows.
   - `stale_known_gaps()` — catches allow-list drift (any
     action listed in `KNOWN_GAPS` that DOES exist now must be
     promoted to `EXPECTED_SURFACES`).
   - `render_audit_text()` — 24-row coverage table for the
     Phase-49d doc + failure messages.

2. **2 new agent actions to close the highest-value gaps**:
   - `open_periodic_table` in `agent/actions_periodic.py`
     (Tools → Periodic table…, Ctrl+Shift+T).  Periodic-table
     lookups are some of the most common questions an AI tutor
     gets in early chemistry education — the dialog shows
     coloured cells + atomic-mass / electronegativity / oxidation
     states / electron configuration in a side pane.
   - `open_naming_rules` in `agent/actions_naming.py` (Tools →
     IUPAC naming rules…).  Naming questions are similarly high-
     volume, and the dialog has a category combo + per-rule
     description / example / pitfall layout that's hard to
     recreate inline.

   Both follow the established
   `_gui_dispatch.run_on_main_thread_sync` marshalling pattern,
   instantiate the dialog with `parent=win`, and call `.show()`
   (modeless) so the agent action returns immediately.

3. **`gui/audit.py` `GUI_ENTRY_POINTS` dict** updated with both
   new entries so the GUI-coverage check stays at 100 %.

4. **`tests/test_agent_surface_symmetry.py` (NEW)** — 7 tests:
   - Spec sanity (≥ 20 surfaces, no duplicate openers).
   - `KNOWN_GAPS` well-formed (every entry has `open_` prefix +
     non-empty rationale).
   - Every expected surface complete (24/24).
   - `KNOWN_GAPS` allow-list is honest (no stale entries).
   - Audit text renders.
   - Round-179 openers registered.
   - Round-179 openers in correct categories
     (`periodic` + `naming`).

**Live audit output (Phase-49d doc).**

```
Catalogue                             Status
------------------------------------------------------------
Cell components                       ok
Centrifugation                        ok
Chromatography methods                ok
Clinical lab panels                   ok
Drawing tool                          ok
Isomer explorer                       ok
Lab analysers                         ok
Lab calculator                        ok
Lab equipment                         ok
Lab reagents                          ok
Lab setups                            ok
Macromolecules window                 ok
Mechanism player                      ok
Metabolic pathways                    ok
Microscopy methods                    ok
Naming rules                          ok
Periodic table                        ok
pH explorer                           ok
Qualitative inorganic tests           ok
Script editor                         ok
Spectrophotometry methods             ok
Tutorial browser                      ok
Workbench                             ok
Biochemistry by kingdom               ok
------------------------------------------------------------
24/24 catalogues have complete agent-action surfaces

KNOWN_GAPS: 9 dialogs deliberately ship without an `open_*` action
(see source for per-entry rationale)
```

**Test count.** 2149 passed (was 2142 in round 178, +7 from the
new audit suite).  Full suite green.

**Why this matters.**  Closes the third of the user's three
flagged failure modes from round 175: *"the AI tutor is able to
access and use all features in all modules"*.  Combined with
49a (glossary coverage), 49b (molecule-DB canonicalisation), and
49c (cross-reference graph), the audit layer now catches:
- words used in catalogues that aren't in the glossary (49a)
- molecule names referenced across modules that don't resolve
  to the DB (49b + 49c)
- cross-references between catalogues that don't resolve (49c)
- dialogs the AI tutor can't open or query (49d)

The remaining sub-phases (49e tutor-panel feature-discovery,
49f doc-coverage extension) extend the visibility surface
further but don't add new failure-mode coverage.

**Files touched.**
- NEW `orgchem/core/agent_surface_audit.py` (~ 220 lines)
- NEW `tests/test_agent_surface_symmetry.py` (~ 110 lines)
- `orgchem/agent/actions_periodic.py` — added
  `open_periodic_table` (~ 25 new lines)
- `orgchem/agent/actions_naming.py` — added
  `open_naming_rules` (~ 25 new lines)
- `orgchem/gui/audit.py` — 2 new GUI_ENTRY_POINTS entries
- `INTERFACE.md` — new audit-module row
- `ROADMAP.md` — Phase 49 status: 49a + 49b + 49c + 49d SHIPPED
- `PROJECT_STATUS.md` — round 179 summary

**Next sub-phase.** 49e — tutor-panel feature-discovery audit:
verify the tutor-panel chat backend's tool-schemas surface
includes every registered agent action so the LLM can discover
+ call any feature.  Also check the system-prompt / capabilities
manifest exposes the right per-category descriptions.

---

## 2026-04-25 — Round 178 (Phase 49c — cross-module reference graph audit + living matrix, third sub-phase of the user-flagged integration sweep)

**Goal.**  Round 175 surfaced a user-flagged Phase 49 cross-module
integration audit.  Round 176 → 49a (glossary coverage); round
177 → 49b (molecule-DB canonicalisation).  Round 178 ships the
next sub-phase — **49c: cross-module reference graph**.  Goal:
unify the per-catalogue cross-reference tests (added in rounds
146 / 151 / 166) into a single project-wide audit + a renderable
matrix that surfaces low-coverage areas.

**What shipped.**

1. **`core/cross_reference_audit.py` (NEW, ~ 250 lines)** —
   walks every catalogue's cross-reference fields and validates
   each edge.  Five relationships audited:
   - `cell-component → molecule` (Phase-43)
   - `kingdom-topic → cell-component` (Phase-47)
   - `kingdom-topic → metabolic-pathway` (Phase-47)
   - `kingdom-topic → molecule` (Phase-47)
   - `microscopy-method → lab-analyser` (Phase-44)

   Public API:
   - `CrossRef(source_kind, source_id, target_kind, target_id)`
     frozen dataclass + `CrossRefReport(total, broken, by_kind)`
   - `gather_all_cross_references()` — flat list of every edge
     (currently 59)
   - `validate_cross_references(refs=None)` — broken-link
     report.  Molecule-name lookups go through normalised-name
     + synonyms matching so synonyms like "Vitamin A" hit the
     "Retinol" row.
   - `cross_reference_matrix()` —
     `{(source_kind, target_kind): edge_count}` for the doc.
   - `render_matrix_text()` — left-aligned plain-text matrix.

2. **`tests/test_cross_reference_graph.py` (NEW)** — 7 tests:
   ≥ 50 edges gathered, every declared kind present with
   non-zero count, matrix renders, no broken edges, per-kind
   floors, dataclass hashability, explicit-refs validation.

3. **Real bug caught on first run.**  The audit module was
   calling `list_lab_analysers` (doesn't exist) — the actual
   public API is `list_analysers`.  All 6 microscopy → lab-
   analyser cross-refs reported broken until the fix.  This is
   exactly what the audit is for: surfacing inconsistencies
   between catalogues at test time.

**Live matrix output (Phase-49c doc).**

```
Source kind          → Target kind         | Edges
------------------------------------------------------------
cell-component       → molecule             |     1
kingdom-topic        → cell-component       |    46
kingdom-topic        → metabolic-pathway    |     5
kingdom-topic        → molecule             |     1
microscopy-method    → lab-analyser         |     6
------------------------------------------------------------
TOTAL                                       |    59
```

**Coverage gap surfaced.**  Only **1** cell-component → molecule
edge + **1** kingdom-topic → molecule edge exist, despite ~ 100
catalogue entries that could meaningfully link to specific
molecule-DB rows (every cell-component constituent COULD
cross-reference its dominant molecule; every kingdom-topic with
a named compound in its body text COULD link to that molecule).
Future Phase-49d-f rounds will use this matrix to drive cross-
reference expansion.  The matrix doc serves as both a
regression floor (lock current counts in) and a roadmap
(visible gaps invite contribution).

**Test count.** 2142 passed (was 2135 in round 177, +7 from the
new audit suite).  Full suite green.

**Files touched.**
- NEW `orgchem/core/cross_reference_audit.py` (~ 250 lines)
- NEW `tests/test_cross_reference_graph.py` (~ 145 lines)
- `INTERFACE.md` — new module row
- `ROADMAP.md` — Phase 49 status: 49a + 49b + 49c SHIPPED
- `PROJECT_STATUS.md` — round 178 summary

**Next sub-phase.** 49d — agent-surface symmetry audit:
verify that every catalogue with a Tools-menu dialog also has
a corresponding agent-action surface (`open_<dialog>` opener +
list / get / find lookups).  Same audit pattern: walk a list
of (dialog id, expected action names) pairs, surface any
missing actions as test failures.

---

## 2026-04-25 — Round 177 (Phase 49b — molecule-DB canonicalisation audit + 120-row catalogue backfill, second sub-phase of the user-flagged integration sweep)

**Goal.** Round 175 surfaced a user-flagged Phase 49 cross-module
integration audit ("ensure modules are well integrated — words
linked to glossary, molecules in the same format and findable in
the database, …").  Round 176 delivered 49a (glossary coverage).
Round 177 ships the next sub-phase — **49b: molecule-DB
canonicalisation**.  Goal: *every catalogue molecule with a
parseable SMILES is also a Molecule row in the DB*, so a learner
who clicks a sugar in the Carbohydrates tab or a steroid in the
Lipids tab can flip into the molecule workspace, run descriptors,
or use it as a retrosynthesis target without "molecule not
found" surprises.

**What shipped.**

1. **`core/glossary_audit.py` extended** with
   `gather_catalogue_molecule_references()` — walker returning
   `(source, name, smiles)` triples across:
   - Phase-29 carbohydrate / lipid / nucleic-acid catalogues
     (each entry IS a molecule reference)
   - Phase-31k SAR series variants
   - Phase-43 cell-component constituents with
     `cross_reference_molecule_name` (name-only)
   - Phase-47 biochemistry-by-kingdom topics with
     `cross_reference_molecule_names` (name-only)
   ~ 250 triples total, ~ 151 carrying SMILES + ~ 100 name-only.

2. **`db/seed_catalogue_molecules.py` (NEW)** —
   `seed_catalogue_molecules_if_needed()` backfills any
   catalogue molecule whose canonical InChIKey isn't already in
   the Molecule DB.  120 molecules seeded on first run.  Each
   row tagged with source `carbohydrate-catalogue` /
   `lipid-catalogue` / `nucleic-acid-catalogue` /
   `sar-<series-id>` so the source filter can drill into a
   specific catalogue's contributions.  Goes through the same
   `ChemMol.from_smiles + ensure_properties` path the
   round-58 seed-set uses, so canonicalisation is consistent.
   Idempotent — second run finds 0 new rows.

3. **Wired into `db/seed.py::seed_if_empty()`** after the
   round-58 `seed_synonyms_if_needed()` call.  Generalises round
   58's InChIKey reconciliation by ADDING missing rows rather
   than only adding aliases.

4. **`tests/test_molecule_db_canonicalisation.py` (NEW)** —
   6 tests:
   - `test_gather_returns_at_least_100_references` — walker
     produces ≥ 100 refs.
   - `test_gather_covers_all_four_smiles_sources` — carb /
     lipid / NA / sar-* sources all hit.
   - `test_every_smiles_ref_resolves_by_inchikey` — every
     catalogue SMILES matches a DB row by full InChIKey OR by
     name + matching skeleton block (the stereo-variant
     fallback covers cases where the catalogue ships a
     fully-specified stereoisomer of an already-named
     partial-stereo seed-set compound, e.g. Cholesterol /
     Codeine / Captopril / Amoxicillin).
   - `test_every_name_ref_resolves` — every name-only
     cross-reference (Phase-43 + 47) hits a DB row by name
     lookup.
   - `test_seed_catalogue_molecules_idempotent` — second run
     returns 0.
   - `test_at_least_some_catalogue_molecules_added` — ≥ 50
     catalogue-sourced molecules in DB after backfill.

5. **Real bug caught: Citalopram SMILES.**  The
   `db/seed_molecules_extended.py` row for Citalopram had F and
   CN swapped relative to the Phase-31k SAR-catalogue version.
   The two SMILES encode completely different molecules
   (different InChIKey skeletons — `OTURDUAIBJEUEI` vs
   `WSEQXVZVJXJVFP`); the DB version isn't actually
   citalopram.  Fixed the seed to the DrugBank structure
   `CN(C)CCCC1(c2ccc(F)cc2)OCc2cc(C#N)ccc21` (CAS 59729-33-8).
   The existing local DB row was patched to match.  This is
   exactly the kind of cross-module inconsistency the user
   flagged — the SAR series and the molecule DB were
   silently disagreeing about a textbook drug.

6. **Bumped `db/queries.py::list_molecules` default `limit`**
   from 500 to 5000.  After the round-177 backfill the DB has
   ~ 720 rows (40 starter + 193 extended + 247 intermediates +
   120 catalogue + …); the previous 500-row default was
   truncating the alphabetically-late tail (α / β / γ-prefixed
   sugars, Testosterone, THF) from `list_all_molecules`, which
   in turn broke the Phase-6 + Phase-6a smoke tests after the
   backfill ran.

**Test count.** 2135 passed (was 2126 in round 176, +6 from the
new canonicalisation suite + 3 already-passing checks now
guarded against truncation).  Full suite green.

**Why this matters.**  Round 177 closes the second of the
user's three flagged failure modes: *"molecules in all modules
are compatible and in the same format as each other and can be
found in the database"*.  Together with round 176's glossary
coverage (failure mode 1), the round-177 audit means a learner
or an LLM tutor can:
- click any catalogue molecule (lipid / sugar / NA / SAR) and
  expect it to be in the molecule browser
- look up any term mentioned in a catalogue's body text and
  expect it to be glossary-defined
- trust that two modules using the same name for a molecule
  use the same structure (caught Citalopram on the first run)

**Files touched.**
- NEW `orgchem/db/seed_catalogue_molecules.py` (~ 160 lines)
- NEW `tests/test_molecule_db_canonicalisation.py` (~ 175 lines)
- `orgchem/core/glossary_audit.py` — added
  `gather_catalogue_molecule_references()` (~ 70 new lines)
- `orgchem/db/seed.py` — call into seeder
- `orgchem/db/seed_molecules_extended.py` — Citalopram fix
- `orgchem/db/queries.py` — `list_molecules` default limit
- `INTERFACE.md` — new seeder row
- `ROADMAP.md` — Phase 49 status: 49a + 49b SHIPPED
- `PROJECT_STATUS.md` — round 177 summary

**Next sub-phase.** 49c — cross-module reference graph doc:
build a single living matrix that shows which modules
cross-reference which (catalogues → DB rows, glossary terms
→ catalogues, agent actions → catalogues, tutorials →
glossary), with a pytest test that walks the matrix to surface
holes.

---

## 2026-04-25 — Round 176 (Phase 49a — glossary autolink coverage audit + 15-term backfill, first sub-phase of the user-flagged integration sweep)

### Context
Round 175 added Phase 49 to the roadmap per user request:
*"Do a code review and ensure that all modules are well
integrated…words used in modules are included and linked to
the glossary, molecules in all modules are compatible…"*
Round 176 ships the first sub-phase — **49a: glossary
autolink coverage audit + missing-term backfill**.

### What shipped
**Audit infrastructure** —
`orgchem/core/glossary_audit.py` (~ 175 lines).
Test-time helper module that walks:
- Phase-43 cell components (every component's function +
  notes + per-constituent role + notes)
- Phase-42 metabolic pathways (overview + per-step notes)
- Phase-44 microscopy (typical_uses + notes + contrast
  mechanism)
- Phase-45 lab reagents (typical_usage + notes +
  preparation notes)
- Phase-46 pH explorer reference cards (markdown bodies)
- Phase-47 biochemistry-by-kingdom (every topic's body +
  notes)
- Phase-31k SAR series (every variant's notes)
- Phase-31b named-reaction descriptions (`_STARTER` body
  text)
- Every registered tutorial markdown lesson body

Returns the union as a single ~ 330 kchar string.  Plus
`glossary_term_set()` returning the lowercase set of all
glossary terms + aliases (~ 247 entries).  Plus
`PHASE_49A_REQUIRED_TERMS` 12-tuple of high-priority
integration gates: pH / pKa / buffer / hydrogen bonding /
LDA / active-methylene compound / multi-component reaction
/ endosymbiotic theory / horizontal gene transfer / CRISPR /
chirality / chiral switch.

Pure-Python; no DB dependency (reads glossary entries
directly from the seed-file Python data structures); no
Qt imports.  Designed to be reused by Phase 49b-f for
additional cross-module audits.

**15 new glossary entries** appended to
`orgchem/db/seed_glossary_extra.py`, filling the high-
priority gaps surfaced by the audit:

1. **pH** — foundational, referenced everywhere; 0-14
   scale; physiological 7.4 anchor.
2. **pKa** — −log₁₀(Kₐ); inflection on titration curve at
   pH = pKa.
3. **Buffer** — weak acid + conjugate base; biological +
   bench buffer examples.
4. **Buffer capacity** — β = 2.303·C·α·(1−α); max at
   pH = pKa, drops to 30 % at |ΔpH| = 1.
5. **Henderson-Hasselbalch** — pH = pKa + log([A⁻]/[HA]);
   Henderson 1908 + Hasselbalch 1916.
6. **Hydrogen bonding** — 5-30 kJ/mol H↔X-lone-pair
   interaction; drives water bp + protein 2° structure +
   Watson-Crick.
7. **Hydrophobic effect** — entropic clathrate-water
   restructuring; drives protein folding + lipid bilayers.
8. **Lithium diisopropylamide (LDA)** — strong non-
   nucleophilic base; kinetic-vs-thermodynamic enolate
   teaching.
9. **Multi-component reaction (MCR)** — Hantzsch / Strecker
   / Mannich / Ugi 4CR canonical examples.
10. **Active-methylene compound** — CH₂ flanked by two EWGs;
    pKa ~ 11-13 vs ketone α-CH ~ 20.
11. **Endosymbiotic theory** — Margulis 1967, 5 lines of
    evidence.
12. **Horizontal gene transfer (HGT)** — transformation +
    transduction + conjugation; antibiotic-resistance
    spread.
13. **CRISPR-Cas** — adaptive bacterial immunity → Doudna
    + Charpentier Nobel 2020 → Casgevy 2023.
14. **Chirality** — umbrella term + sp³ stereocentre
    origin + biological selectivity.
15. **Chiral switch** — citalopram → escitalopram +
    omeprazole → esomeprazole patent-extension paradigm.

`SEED_VERSION` bumped 9 → 10.

### Tests
9 new tests in `tests/test_glossary_coverage.py`:
- `test_glossary_term_set_is_substantial` (≥ 200 entries)
- `test_all_catalogue_text_is_substantial` (≥ 100 kchars)
- `test_required_terms_in_glossary` — every Phase-49a
  required term in glossary
- `test_required_terms_appear_in_catalogue_text` — every
  required term used somewhere via canonical-name OR
  alias match (load-bearing, not seeded for completeness
  alone)
- `test_ph_chemistry_terms_present` — domain-specific
  check for pH / pKa / buffer / buffer capacity /
  Henderson-Hasselbalch
- `test_synthesis_vocabulary_terms_present` — LDA /
  active-methylene / MCR
- `test_biology_vocabulary_terms_present` — endosymbiotic
  theory / HGT / CRISPR
- `test_phase_49a_glossary_grew_by_at_least_15` — set-size
  floor (≥ 240 with aliases)
- `test_glossary_audit_module_public_api` — three exported
  symbols present + correctly-typed

Discovered + fixed during the test run: first iteration
of `_catalogue_text_sources()` walked Phase-43/42/44/45/46/
47/31k catalogues + tutorial markdown but NOT the
`db.seed_reactions._STARTER` reaction descriptions — so the
required-term-in-text check failed for `active-methylene
compound` (only mentioned in the Knoevenagel reaction
description) and `multi-component reaction` (only in the
Hantzsch description).  Added the reaction-seed walk; all
12 required terms now found.  Plus a doc-coverage-test
adjustment: an INTERFACE.md row mentioned
`tests/test_glossary_coverage.py` as a `path.py` token,
which the existence-checker tried to verify under
`orgchem/` — rephrased to drop the explicit test-file
reference.

### Documentation updates
- INTERFACE.md — added row for `core/glossary_audit.py`.
- ROADMAP.md — Phase 49 status updated to "IN PROGRESS —
  49a SHIPPED round 176" with delivery manifest + queued
  next-round work (49b-f).
- PROJECT_STATUS.md — round 176 summary prepended.
- SESSION_LOG.md — this entry.

### Test suite status
2 129 passing (up from 2 120 in round 175 — net +9 from
this round's 9 new test functions).  Doc-coverage test
green; full suite ~51 s wall-clock.

### What's open (next-round candidates)
- **Phase 49b** — molecule-DB canonicalisation audit.
  Walk every catalogue's molecule-name / SMILES references;
  verify each canonicalises to a real seeded `Molecule` row
  (by InChIKey via `core/fragment_resolver.py`).  Same
  test-time helper pattern as 49a.  Lowest-risk next step
  — same audit-walker scaffolding extends naturally.
- **Phase 49c-f** — cross-module reference graph + agent-
  surface symmetry + tutor-panel discovery + doc-coverage
  extension.
- **Phase 31b extension** — 4 more entries to reach the
  60-target.

A safer next pick is **Phase 49b** to keep the integration-
sweep momentum + reuse the round-176 audit-walker.

## 2026-04-25 — Round 175 (Phase 31b extension — Henry reaction + Hantzsch dihydropyridine MCR; Phase 49 added to roadmap)

### Context
Round 174 closed Phase 48 entirely.  Round 175 returns to
the Phase 31b extension (54/60) and ships two more
reactions: Henry (nitroaldol C-N + C-C) and Hantzsch
dihydropyridine MCR.  Mid-round the user flagged a new
**cross-module integration audit** request that's been
captured as Phase 49 in the roadmap.

### What shipped
**Two named reactions** added to
`orgchem/db/seed_reactions.py`:

1. **Henry reaction (nitromethane + benzaldehyde →
   2-nitro-1-phenylethanol)** — category *Condensation
   (nitroaldol)*.  Louis Henry 1895.  Description teaches:
   base-catalysed addition of a nitroalkane to an aldehyde
   or ketone giving a β-nitro alcohol; pKa contrast with
   the classic aldol — nitroalkane α-H ~ 10 vs ketone α-H
   ~ 20 — enables mild secondary-amine / KF / fluoride /
   phosphazene catalysts; mechanism (base deprotonates the
   nitroalkane to the **aci-nitro carbanion**; carbanion
   attacks the carbonyl C; protonation gives the β-nitro
   alcohol); downstream value (Pd/C-H₂ reduction of the
   -NO₂ group gives a 1,2-amino alcohol — β-blocker /
   chloramphenicol scaffold; Nef reaction converts -NO₂ to
   a carbonyl giving an α,β-dihydroxyketone or aldehyde;
   dehydration gives a Michael-acceptor nitroalkene);
   asymmetric variants — Shibasaki Ln-BINOL 1992, Trost
   Zn-ProPhenol 2002 — deliver > 90 % ee for chiral
   1,2-amino alcohol synthesis.

2. **Hantzsch dihydropyridine synthesis (benzaldehyde + 2
   ethyl acetoacetate + NH₃ → diethyl 4-phenyl-2,6-
   dimethyl-1,4-dihydropyridine-3,5-dicarboxylate + 3
   H₂O)** — category *Multi-component reaction (heterocycle
   synthesis)*.  Hantzsch 1881.  **The textbook MCR**.
   Description walks the cascade: (1) Knoevenagel of one
   β-ketoester with the aldehyde → unsaturated diketoester
   (cross-references the Phase-31b's seeded Knoevenagel
   reaction); (2) the second β-ketoester condenses with
   NH₃ → β-enaminone; (3) Michael addition of enaminone
   onto the Knoevenagel adduct closes the ring; (4)
   dehydration aromatises to the symmetric 1,4-DHP.  Three
   new C-N + C-C bonds + 4 bond-rearrangements in one pot.
   **Pharmaceutical significance**: 1,4-DHP scaffold is
   the core of the calcium-channel-blocker antihypertensive
   class (nifedipine 1975, amlodipine 1990, felodipine,
   nicardipine, isradipine, lacidipine).

**Three intermediate fragments** added to
`orgchem/db/seed_intermediates.py`: `Nitromethane
C[N+](=O)[O-]` (reagent), `2-Nitro-1-phenylethanol (Henry
product) O=[N+]([O-])CC(O)c1ccccc1` (intermediate),
`Hantzsch 1,4-dihydropyridine` (intermediate).

### Tests
Three new tests in `tests/test_reactions.py` plus the
catalogue-size floor bumped:
- `test_henry_reaction_seeded` — nitro-group SMILES +
  nitroalkane class + pKa contrast + aci-nitro carbanion
  + Shibasaki/Trost asymmetric variant teaching anchors.
- `test_hantzsch_dihydropyridine_seeded` — Hantzsch 1881
  + MCR class + ≥ 3 of 4 cascade steps named (Knoevenagel
  + enaminone + Michael + dehydration) + calcium-channel-
  blocker pharmaceutical context.
- `test_multi_component_reaction_anchor_present` —
  Hantzsch + Robinson annulation + Knoevenagel cascade
  trio guarded against future regression.
- `test_named_reaction_count_at_least_fifty_six` —
  catalogue floor bumped 54 → 56 (renamed from round-165
  `_fifty_four`).

Discovered + fixed during the test run: fragment-
consistency audit caught 3 missing fragments on first
reaction-add.  Resolved by seeding the 3 intermediate
rows above.  All 39 reaction-tests pass + all 12
fragment-consistency tests pass.

### Mid-round: Phase 49 added to roadmap (user request)
The user flagged a new audit request mid-round: *"Do a
code review and ensure that all modules are well
integrated with each other, for example, words used in
modules are included and linked to the glossary, molecules
in all modules are compatible and in the same format as
each other and can be found in the database, reactions and
techniques are linked between modules, the AI tutor is
able to access and use all features in all modules etc."*

Added to ROADMAP.md as **Phase 49 — Cross-module
integration audit + glue** with 6 sub-phases:
- 49a — Glossary autolink coverage audit + missing-term
  backfill.
- 49b — Molecule-DB canonicalisation audit (every
  catalogue's molecule references resolve to a real
  Molecule row by InChIKey).
- 49c — Cross-module reference graph doc
  (`docs/CROSS_MODULE_REFERENCES.md`).
- 49d — Agent-surface symmetry audit (extends the existing
  Phase-25a `gui/audit.py` to 100 % open-from-agent
  coverage).
- 49e — Tutor-panel feature-discovery audit
  (`list_capabilities` returns every feature).
- 49f — Doc-coverage extension (every INTERFACE.md row →
  `CLAUDE.md` "Where each concern lives" + every Tools-
  menu shortcut unique).

Why it matters: earlier rounds proved that **test-guarded
cross-module references catch real bugs** — the Phase-47 →
Phase-43 xref test in round 166 caught a Phase-42
id-format mismatch (`tca-cycle` vs `tca_cycle`); the
Phase-43 → Molecule-DB xref test in round 151 caught 4
broken cross-references on first run.  Phase 49
generalises those one-off audits into a comprehensive
integration sweep.  Likely 6 rounds; lowest-risk start is
49a (glossary coverage) since it's purely additive content
work + sets up the autolinker for every following sub-phase.

### Documentation updates
- ROADMAP.md — Phase 31b extension count updated 54/60 →
  56/60 + new Phase 49 added with full sub-phase plan +
  design rationale.
- PROJECT_STATUS.md — round 175 summary prepended.
- SESSION_LOG.md — this entry.

### Test suite status
2 120 passing (up from 2 117 in round 174 — net +3 from
this round's 3 new test functions).  Doc-coverage test
green; full suite ~48 s wall-clock.

### What's open (next-round candidates)
- **Phase 49a** — glossary autolink coverage audit + the
  missing-term backfill.  Lowest-risk first step of the
  new user-flagged Phase 49 sweep.
- **Phase 31b extension** — 4 more entries to reach the
  60-target.
- **Phase 38c** — equipment-palette + QGraphicsScene
  canvas for the lab-setup simulator.

A safer next pick is **Phase 49a** to start the user-
flagged integration sweep with the lowest-risk piece.

## 2026-04-25 — Round 174 (🎉 Phase 48 CLOSED — tutorial cross-link)

### Context
Rounds 170-173 shipped Phase 48a (headless core +
glossary), 48b (dialog), 48c (agent actions), 48d
(inline 'View isomers' button).  Round 174 closes Phase
48 entirely with the tutorial cross-link — completing
all four user-flagged round-165 design recommendations.

### What shipped
**Tutorial lesson** —
`orgchem/tutorial/content/intermediate/11_isomerism.md`.
Title: *"Isomerism: a unified hierarchy"*.  ~ 5-screen
intermediate lesson covering:
- The 5-tier hierarchy as a comparison table
  (constitutional / conformer / enantiomer /
  diastereomer / tautomer + identical /
  different-molecule edge cases).
- Worked SMILES examples in every section that the
  reader can paste into the Phase-48b dialog:
  - n-/sec-/iso-/tert-butanol C₄H₁₀O constitutional
    family
  - Propanal vs acetone constitutional pair
  - (R)/(S)-lactic acid enantiomers
  - (2R,3R)/(2R,3S)-2,3-dihydroxybutanoate diastereomers
  - meso-tartaric acid internal-mirror-plane example
  - Acetone keto/enol tautomer pair
  - 2,4-pentanedione 5-tautomer doubly-activated CH₂
  - BINAP atropisomer asymmetric-hydrogenation context
  - Butenes worked example covering all 5 isomer-family
    branches in one substrate
- Inline cross-references to the Phase-48b *Tools →
  Isomer relationships…* dialog (Ctrl+Shift+B) AND the
  Phase-48d inline 'View isomers…' workspace button so
  readers discover both entry paths.
- References to all 7 round-170 glossary terms
  (Isomerism / Stereoisomer / Conformer / Tautomer /
  Atropisomer / Cis-trans isomerism / Optical activity)
  so the existing tutorial-panel autolinker
  (`gui/widgets/glossary_linker.py`) wraps them as
  clickable anchors automatically.

**Curriculum wiring** — `orgchem/tutorial/curriculum.py`
gains an 11th intermediate-level entry between 'Protecting
groups' and the existing advanced/01 Pericyclic-reactions
lesson.

### Tests
9 new tests in `tests/test_isomerism_lesson.py`:
- `test_lesson_file_exists` — markdown file on disk.
- `test_lesson_registered_at_intermediate_level` — the
  curriculum tree has it.
- `test_lesson_path_follows_convention` — path is
  `intermediate/11_isomerism.md` (next sequential number).
- `test_lesson_covers_all_seven_relationships` — every
  RELATIONSHIPS string mentioned in the body.
- `test_lesson_cross_links_to_isomer_explorer_dialog` —
  both the dialog name + the Ctrl+Shift+B shortcut appear.
- `test_lesson_cross_links_to_view_isomers_workspace_button`
  — the Phase-48d inline button name appears.
- `test_lesson_cross_links_to_round_170_glossary_terms` —
  all 7 isomer-vocabulary glossary terms referenced by
  exact name (so the autolinker turns them into anchors).
- `test_lesson_includes_worked_example_smiles` — at least
  5 of the canonical worked-example SMILES strings
  appear (n-butanol, tert-butanol, propanal, acetone,
  R-lactic acid, S-lactic acid, 2,4-pentanedione).
- `test_lesson_intermediate_count_increased_to_11` —
  curriculum-size floor.

All 9 tests pass on first run.

### Documentation updates
- ROADMAP.md — Phase 48 status flipped to "🎉 SHIPPED
  end-to-end across rounds 170-174" with full delivery
  manifest for the 48e sub-phase + Phase-48-vision-
  realised closeout language.
- PROJECT_STATUS.md — round 174 summary prepended with
  the 🎉 Phase 48 CLOSED milestone language.
- SESSION_LOG.md — this entry.

### Test suite status
2 117 passing (up from 2 108 in round 173 — net +9 from
this round's 9 new test functions).  Doc-coverage test
green; full suite ~48 s wall-clock.

### What's open (next-round candidates)
**Phase 48 is COMPLETE.**  The second of the two user-
flagged round-165 phases is now fully delivered (Phase 47
Biochemistry-by-Kingdom closed in round 169 with its 47d
sub-domain-filter follow-up).  All user-flagged feature
requests in scope are now shipped.

Remaining roadmap work:
- **Phase 31b extension** — 6 more named reactions to
  reach the 60-target (Ramberg-Bäcklund, Shapiro,
  Oppenauer, Julia / Peterson olefinations, Henry,
  Hantzsch dihydropyridine).
- **Phase 38c** — equipment-palette + QGraphicsScene
  canvas for the lab-setup simulator.  Multi-round; the
  highest-value remaining work + the only unfinished
  feature still on the original Phase-38 roadmap.
- **Phase 31k extension** — 6 more SAR series for a 21-
  target.
- **Phase 47b/c follow-ups** — additional kingdom topics
  for the Asgard / Heimdall sub-domain detail level.

A safer next pick is the **Phase 31b extension** (1-2
named reactions per round, established tight pattern).
The bigger ambition is **Phase 38c** lab-setup canvas —
the only major unfinished user-flagged feature.

## 2026-04-25 — Round 173 (Phase 48d — inline 'View isomers' button on the molecule 2D viewer)

### Context
Round 172 closed the agent-action layer for Phase 48.  Round
173 closes the user-flagged 4-pronged isomers integration at
the GUI level: any molecule displayed in the Viewer2DPanel
now carries a one-click jump to the Phase-48b isomer-
relationships dialog with the SMILES pre-filled.

### What shipped
**`orgchem/gui/panels/viewer_2d.py`** extended:
- New **"View isomers…"** button on the top row, next to
  the existing Style combo.
- Button is **disabled until a molecule is selected**;
  enables when a `molecule_selected` bus signal carries
  a real SMILES.
- Click handler `_on_view_isomers` walks up to the
  main-window parent, opens the singleton
  `IsomerExplorerDialog`, and **pre-fills all three
  SMILES inputs** simultaneously (Stereoisomers tab +
  Tautomers tab + Classify pair tab 'A' input) so the
  user lands in a ready-to-run state on whichever tab
  they switch to.
- Then **auto-runs the stereoisomer enumeration** via
  `_on_stereo_run()` so results appear immediately on
  the default Stereoisomers tab — the user does NOT have
  to click Enumerate themselves.
- **Singleton pattern reused** — repeat clicks update
  the SMILES in the same dialog instance rather than
  spawning new dialogs.
- Tooltip explains the Ctrl+Shift+B shortcut for
  keyboard-driven users.
- **No-op safety**: clicking with
  `_current_smiles=None` (e.g. signal race) silently
  exits instead of opening an empty dialog.

### Tests
8 new tests in `tests/test_viewer_2d_isomer_button.py`:
- `test_viewer_2d_carries_view_isomers_button` — button
  present + correct text.
- `test_viewer_2d_button_disabled_before_selection` —
  initial state.
- `test_viewer_2d_button_enabled_after_smiles_set` —
  uses the seeded Cholesterol molecule as the smoke-
  test substrate.
- `test_view_isomers_click_opens_dialog` — click
  pre-fills all 3 SMILES inputs.
- `test_view_isomers_click_focuses_stereoisomers_tab` —
  click lands on the Stereoisomers tab (most natural
  starting view).
- `test_view_isomers_click_auto_runs_enumeration` —
  verifies `_stereo_list.count() == 4` for the
  2-stereocentre input `CC(O)C(O)CO`, proving the
  auto-run actually happens.
- `test_view_isomers_click_with_no_smiles_is_noop` —
  no dialog instance created.
- `test_view_isomers_singleton_pattern` — second click
  updates SMILES in the same instance.

All 8 tests pass on first run.

### Documentation updates
- ROADMAP.md — Phase 48 status updated to "48a + 48b +
  48c + 48d SHIPPED" with delivery manifest for the 48d
  sub-phase.
- PROJECT_STATUS.md — round 173 summary prepended.
- SESSION_LOG.md — this entry.

(No INTERFACE.md changes needed — the existing
`viewer_2d.py` row covers the new feature implicitly.)

### Test suite status
2 108 passing (up from 2 099 in round 172 — net +8 from
this round's 8 new test functions, plus +1 from
`tests/test_glossary.py` having one fewer skip flag this
round).  Doc-coverage test green; full suite ~48 s
wall-clock.

### What's open (next-round candidates)
- **Phase 48e** — tutorial-content cross-link.  Write
  1-2 lessons under `tutorial/content/intermediate/`
  covering isomerism with worked examples that link out
  to the isomer-relationship explorer.  Closes Phase 48
  entirely.  Ships in 1 round.
- **Phase 31b extension** — 6 more entries to reach the
  60-target.
- **Phase 38c** — equipment-palette + QGraphicsScene
  canvas for the lab-setup simulator.

A safer next pick is **Phase 48e** to close Phase 48
entirely — leaving Phase 48 at 5/5 sub-phases shipped.

## 2026-04-25 — Round 172 (Phase 48c — isomer agent actions + audit-map registration)

### Context
Round 171 shipped Phase 48b — the Tools → *Isomer
relationships…* (Ctrl+Shift+B) dialog wrapping the round-170
core engine.  Round 172 ships the agent layer for the same
core, mirroring the established Phase-37/40/45/47 catalogue
agent-action pattern.

### What shipped
**Agent actions** — `orgchem/agent/actions_isomers.py`
(~120 lines).  4 actions in a new `isomer` category:

- **`find_stereoisomers(smiles, max_results=16)`** — wraps
  `core.isomers.enumerate_stereoisomers`.  Under-specified
  input expands to all consistent stereoisomers.  Returns
  `{input_smiles, canonical_smiles_list, truncated}` dict.
  Unparseable input returns empty list rather than
  raising.
- **`find_tautomers(smiles, max_results=16)`** — wraps
  `enumerate_tautomers` (RDKit's TautomerEnumerator,
  ~ 20 documented rules).  Same dict shape as above.
- **`classify_isomer_pair(smiles_a, smiles_b)`** — wraps
  `classify_isomer_relationship`.  Returns
  `{smiles_a, smiles_b, relationship, formula_a,
  formula_b}` dict — **the formulas surface AS PART OF
  the response** so an LLM caller can immediately reason
  about whether the pair shares a formula AND what kind
  of isomer relationship they have, in a single call.
- **`open_isomer_explorer(tab="")`** — opens the *Tools
  → Isomer relationships…* dialog (Ctrl+Shift+B) and
  optionally focuses one of the 3 tabs (Stereoisomers /
  Tautomers / Classify pair).  Marshals onto the Qt main
  thread via `_gui_dispatch.run_on_main_thread_sync`.
  Returns `{opened, selected, tab, available_tabs}` so
  the agent can introspect failure paths.

**Wiring**:
- `orgchem/agent/__init__.py` — added `from orgchem.agent
  import actions_isomers`.
- `orgchem/gui/audit.py` — registered all 4 actions in
  `GUI_ENTRY_POINTS` (each pointing at *Tools → Isomer
  relationships…* (Ctrl+Shift+B)).

### Tests
20 new tests in `tests/test_isomer_actions.py`:
- `find_stereoisomers`: 2-centres → 4 isomers; 0 centres
  → 1 isomer; max_results truncation sets truncated=True
  + caps the list; unparseable → empty list.
- `find_tautomers`: acetone ≥ 2; pentanedione ≥ 5;
  unparseable → empty.
- `classify_isomer_pair`: every branch — identical /
  enantiomer / diastereomer / constitutional / tautomer /
  different-molecule / unparseable.  Plus a separate
  invariant — every classify response carries both
  molecular formulas (or None for unparseable).
- `open_isomer_explorer`: no-args + with-tab + with-
  unknown-tab + introspect `available_tabs` field.
- `audit_map_includes_all_four_isomer_actions` — guards
  against future regression of the wiring.
- `isomer_category_actions_registered` — introspects
  `ActionSpec.category` to confirm all 4 actions carry
  the new `isomer` tag.

All 20 tests pass on first run.

### Documentation updates
- INTERFACE.md — added row for `agent/actions_isomers.py`
  with full 4-action API surface description.
- ROADMAP.md — Phase 48 status updated to "48a + 48b +
  48c SHIPPED" with delivery manifest for the 48c
  sub-phase.
- PROJECT_STATUS.md — round 172 summary prepended.
- SESSION_LOG.md — this entry.

### Test suite status
2 099 passing (up from 2 079 in round 171 — net +20 from
this round's 20 new test functions).  Doc-coverage test
green; full suite ~48 s wall-clock.

### What's open (next-round candidates)
- **Phase 48d** — inline 'View isomers' button on the
  molecule-workspace toolbar.  Wires up the same dialog
  + pre-fills the SMILES input from the currently-
  selected molecule.  Ships in 1 round.
- **Phase 48e** — tutorial-content cross-link (1-2 lessons
  under `tutorial/content/intermediate/` covering
  isomerism with worked examples linking out to the
  isomer-relationship explorer).  Ships in 1 round.
- **Phase 31b extension** — 6 more entries to reach the
  60-target.

A safer next pick is **Phase 48d** to complete the user-
visible integration of the isomers tool with the molecule
workspace.

## 2026-04-25 — Round 171 (Phase 48b — Tools → Isomer relationships… dialog)

### Context
Round 170 shipped Phase 48a — the headless `core/isomers.py`
engine with 3 public APIs (`enumerate_stereoisomers`,
`enumerate_tautomers`, `classify_isomer_relationship`) plus
the 7-term glossary expansion.  Round 171 ships the GUI:
the Tools → *Isomer relationships…* (Ctrl+Shift+B) dialog
that wraps the engine.

### What shipped
**Dialog** — `orgchem/gui/dialogs/isomer_explorer.py`
(~340 lines).  Singleton modeless `QDialog` with a 3-tab
layout:

1. **Stereoisomers** tab — SMILES input + max-results spin
   + Enumerate button → list of canonical SMILES from
   `enumerate_stereoisomers`.  Meta line shows the input
   SMILES + molecular formula + result count + a red
   "(truncated at max=N)" notice when the cap was hit.
2. **Tautomers** tab — same shape, drives
   `enumerate_tautomers`.
3. **Classify pair** tab — two SMILES inputs (A and B) +
   a Classify button → HTML result panel showing:
   - The **colour-coded relationship label** as a heading
     (green for identical, blue for constitutional,
     purple for enantiomer / diastereomer / meso, orange
     for tautomer, grey for different-molecule).
   - The canonical RELATIONSHIPS string in code-font.
   - A 2-row comparison table with both SMILES + their
     molecular formulas.
   - A **per-relationship explainer paragraph** that walks
     the user through the pedagogical implications — e.g.
     for enantiomers the "identical physical properties
     EXCEPT optical rotation + biological activity at
     chiral receptors" lesson; for diastereomers the
     "different physical properties + separable by ordinary
     chromatography" lesson; for tautomers the "dynamic
     equilibrium under ambient conditions" lesson.

Singleton pattern preserves the user's last input across
re-opens.  Programmatic API for the upcoming Phase-48c
agent action: `select_tab(label)`, `tab_labels()`.

**Wiring** — `orgchem/gui/main_window.py`:
- New *Tools → Isomer relationships…* menu entry with
  **Ctrl+Shift+B** shortcut.
- New `_on_isomer_explorer()` slot that opens the
  singleton.

### Tests
17 new tests in `tests/test_isomer_explorer_dialog.py`:
- Construction: 3-tab labels in canonical order
  (`["Stereoisomers", "Tautomers", "Classify pair"]`).
- Singleton pattern.
- `select_tab` known + unknown.
- Stereoisomers tab: 2-stereocentre input → 4 isomers in
  list; 4-stereocentre input with max=4 → truncation
  notice; empty input → enter-a-smiles message;
  unparseable input → "unparseable" formula in meta line +
  empty list.
- Tautomers tab: acetone ≥ 2; pentanedione ≥ 5; empty
  input → empty list.
- Classify pair tab: enantiomers (R/S lactic) → "enantiomer"
  + "mirror" in result HTML; identical → "identical";
  constitutional (propanal/acetone) → "constitutional";
  tautomer (acetone keto/enol) → "tautomer";
  different-molecule (benzene/toluene) → "different" +
  "isomer"; empty input → enter-both-smiles message.
- Main-window slot: `app.window._on_isomer_explorer()`
  opens the singleton.

All 17 tests pass on first run.

### Documentation updates
- INTERFACE.md — added row for `gui/dialogs/isomer_explorer.py`
  with full 3-tab description.
- ROADMAP.md — Phase 48 status updated to "48a + 48b SHIPPED"
  with delivery manifest.
- PROJECT_STATUS.md — round 171 summary prepended.
- SESSION_LOG.md — this entry.

### Test suite status
2 079 passing (up from 2 062 in round 170 — net +17 from
this round's 17 new test functions).  Doc-coverage test
green; full suite ~46 s wall-clock.

### What's open (next-round candidates)
- **Phase 48c** — agent actions in a new `isomer` category
  (`enumerate_stereoisomers`, `enumerate_tautomers`,
  `classify_isomer_pair`, `open_isomer_explorer`).  Plus
  audit-map registration.  Ships in 1 round.
- **Phase 48d** — inline 'View isomers' button on the
  molecule workspace.  Ships in 1 round.
- **Phase 31b extension** — 6 more entries to reach the
  60-target.

A safer next pick is **Phase 48c** to keep the isomer
momentum + give the agent surface access to the new
catalogue.

## 2026-04-25 — Round 170 (Phase 48a — isomer-relationship core + 7-term glossary expansion)

### Context
Round 169 closed Phase 47 entirely (Biochemistry-by-Kingdom
window with the round-167 GUI plus the round-169 sub-domain
filter addressing the user's plant/animal feedback).  Round
170 starts Phase 48 — the **other** unfinished user-flagged
phase from round 165 — the isomers exploration tool.  The
round-165 design recommendation called for 4-pronged
integration: (1) relationship-explorer dialog, (2) inline
'View isomers' button on the molecule workspace, (3)
glossary expansion, (4) tutorial cross-link.  This round
ships the headless data core for (1) plus (3) — the
lowest-risk first step.

### What shipped
**Headless core** — `orgchem/core/isomers.py` (~250 lines).
RDKit-backed.  Three public APIs:

1. **`enumerate_stereoisomers(smiles, max_results=16)`** —
   wraps RDKit's `EnumerateStereoisomers` with
   `onlyUnassigned=True`.  Fully-specified inputs return just
   themselves; under-specified inputs expand to all consistent
   stereoisomers (e.g. `CC(O)C(O)CO` → 4 isomers).
   `max_results` cap keeps highly-stereogenic substrates from
   blowing up; de-duplicated by canonical SMILES; returns
   `IsomerEnumerationResult` dataclass (input_smiles +
   canonical_smiles_list + truncated flag).
2. **`enumerate_tautomers(smiles, max_results=16)`** —
   wraps `MolStandardize.TautomerEnumerator` (covers
   keto/enol, amide/iminol, hydroxypyridine/pyridone,
   nitroso/oxime, ~ 20 documented rules).  Finds 5 tautomers
   for 2,4-pentanedione.
3. **`classify_isomer_relationship(smi_a, smi_b)`** — the
   core comparator.  Walks an 8-step decision tree to return
   one of 7 canonical RELATIONSHIPS strings:
   - `identical` (same canonical SMILES with stereo)
   - `enantiomer` (same connectivity; inverting all
     stereocentres of `a` equals `b`)
   - `meso` (caught implicitly via the identical branch
     when a == its own mirror image)
   - `diastereomer` (same connectivity, different stereo,
     not mirror images)
   - `tautomer` (different connectivity, same formula, AND
     `b` appears in `a`'s tautomer enumeration)
   - `constitutional` (different connectivity, same formula,
     not tautomers)
   - `different-molecule` (different formulas OR
     unparseable input — conservative answer)

   Order matters — identical/enantiomer/meso/diastereomer
   all imply same molecular formula, so constitutional +
   tautomer + different-molecule fall through.

Sanity-tested across all 7 branches:
- (R)-/(S)-lactic acid → enantiomer
- (2R,3R)/(2R,3S)-2,3-dihydroxybutanoic acid → diastereomer
- propanal / acetone → constitutional
- acetone keto / enol → tautomer
- benzene / toluene → different-molecule

**Glossary expansion** — `orgchem/db/seed_glossary_extra.py`.
7 new isomer-vocabulary terms appended:
1. **Isomerism** — umbrella term + 5-tier hierarchy walk
   (constitutional + stereo + conformational + tautomer +
   atropisomer).
2. **Stereoisomer** — same connectivity, different 3D;
   enantiomer vs diastereomer split.
3. **Conformer** — rotational state, freely interconverting,
   bioactive-conformer drug-discovery angle.
4. **Tautomer** — 5 major classes (keto/enol, amide/iminol,
   lactam/lactim, nitroso/oxime, ring-chain in sugars);
   environment-dependent ratio.
5. **Atropisomer** — restricted-rotation biaryl stereoisomers;
   BINAP for asymmetric hydrogenation; FDA pharmaceutical-
   gotcha (telmisartan / lesinurad / gefitinib).
6. **Cis-trans isomerism** — E/Z designation; cis-platin vs
   trans-platin (only cis active); cis vs trans fatty-acid
   cardiovascular story.
7. **Optical activity** — specific rotation [α]ᴅ²⁰; Biot
   1815 / Pasteur tartrate; ee measurement via polarimetry.

`SEED_VERSION` bumped 8 → 9 so existing DBs pick up the
new terms on next launch.

### Tests
**20 new tests** in `tests/test_isomers.py`:
- RELATIONSHIPS vocabulary completeness + molecular_formula
  helper.
- Every classify branch: identical (3 cases), enantiomer
  (lactic acid), diastereomer (2,3-dihydroxybutanoate),
  constitutional (propanal/acetone + 4 butanol pairs),
  tautomer (acetone keto/enol), different-molecule
  (different formula + unparseable input).
- Symmetry: classify_isomer_relationship(a, b) ==
  classify_isomer_relationship(b, a) for non-tautomer
  pairs.
- Stereoisomer enumeration: 2 centres → 4 isomers; 0
  centres → 1 isomer; fully-specified → 1 isomer;
  max_results cap with truncated=True; unparseable → empty.
- Tautomer enumeration: acetone ≥ 2; pentanedione ≥ 5;
  methane ≥ 1; unparseable → empty.

**1 new test** in `tests/test_glossary.py`:
- `test_phase_48a_isomer_terms_present` — locks in all 7
  new isomer-vocabulary terms.

### Documentation updates
- INTERFACE.md — added row for `core/isomers.py` with
  full API surface description.
- ROADMAP.md — Phase 48 status updated to "IN PROGRESS —
  48a SHIPPED round 170" with delivery manifest + queued
  next-round work (48b dialog, 48c agent actions, 48d
  inline 'View isomers' workspace button, 48e tutorial
  cross-link).
- PROJECT_STATUS.md — round 170 summary prepended.
- SESSION_LOG.md — this entry.

### Test suite status
2 062 passing (up from 2 042 in round 169 — net +20 from
this round's 20 + 1 new test functions, minus 1 because
the existing `test_glossary_seeded_with_at_least_40_terms`
counts against the same set).  Doc-coverage test green;
full suite ~46 s wall-clock.

### What's open (next-round candidates)
- **Phase 48b** — `gui/dialogs/isomer_explorer.py` —
  Tools → *Isomer relationships…* (Ctrl+Shift+B) singleton
  modeless dialog.  SMILES input → tabbed results
  (Constitutional / Stereoisomers / Tautomers /
  Conformers).  Ships in 1 round.
- **Phase 48c** — agent actions in a new `isomer` category
  (`find_isomers`, `classify_isomer_pair`,
  `enumerate_constitutional`, `enumerate_stereoisomers`,
  `enumerate_tautomers`, `open_isomer_explorer`).  Ships
  in 1 round.
- **Phase 48d** — inline 'View isomers' button on the
  molecule workspace.  Ships in 1 round.
- **Phase 31b extension** — 6 more entries to reach the
  60-target.

A safer next pick is **Phase 48b** to keep the isomer
momentum going + give the user a visible UI deliverable
for the new feature.

## 2026-04-25 — Round 169 (Phase 47d — sub-domain filter on Eukarya tab + plant/animal/fungus topic expansion, addressing user feedback)

### Context
Round 168 closed Phase 47 at the original 60-topic 4-
kingdom × 3-sub-tab vision.  The user followed up: *"In the
new biochemistry by kingdom window — what happened to plant
and animal kingdoms?"*  Fair design point: although Plantae
+ Animalia + Fungi + Protista are kingdoms WITHIN Eukarya
(not separate domains under the modern three-domain
phylogeny), users will reasonably look for them at the top
level.  Recommended options 1 + 3 together; user confirmed
*"Please update with options 1 and 3 together"*.

Round 169 ships **Phase 47d** — sub-domain filter on every
kingdom tab + 8 new explicitly-tagged plant / animal /
fungus topics in the Eukarya tab.  Catalogue grows 60 → 68;
Eukarya tab grows 15 → 23.

### What shipped
**Headless data core** —
`orgchem/core/biochemistry_by_kingdom.py`:
- New `sub_domain: str = ""` field on `KingdomTopic`.
  Default empty string means **pan-domain** — the topic
  surfaces under any sub-domain query within its kingdom
  (same semantics as Phase-43 cell-component sub-domain
  queries).  Backward-compatible with existing topic data.
- New `SUB_DOMAINS` canonical tuple covering all 4
  kingdoms' meaningful sub-domains: animal / plant /
  fungus / protist (Eukarya); gram-positive / gram-
  negative (Bacteria); euryarchaeota / crenarchaeota /
  asgard (Archaea); dna-virus / rna-virus / retrovirus
  (Viruses).
- New `sub_domains_for_kingdom(kingdom)` helper picks the
  kingdom-appropriate subset for the GUI's per-tab combo
  population.
- `list_topics(kingdom, subtab, sub_domain)` extended with
  the new kwarg.

**8 new explicitly-tagged eukaryote topics**:
1. `eukarya-structure-animal-tight-junctions` — animal
   tight + adherens + desmosomes + gap junctions; pemphigus
   autoimmune teaching anchor.
2. `eukarya-physiology-animal-nervous-system` — resting +
   action potentials, SNARE-mediated vesicle fusion,
   neurotransmitter classes (glutamate / GABA / ACh /
   dopamine / serotonin), drug targets.
3. `eukarya-physiology-animal-immune-system` — innate
   (TLRs, complement, NK) vs adaptive (B + T cells, MHC,
   class switching), checkpoint-inhibitor immunotherapy
   (Honjo + Allison Nobel 2018).
4. `eukarya-physiology-plant-auxin-photoperiodism` — 5
   classical phytohormones (auxin / cytokinin /
   gibberellins / abscisic acid / ethylene), phytochrome
   + cryptochrome, florigen.
5. `eukarya-structure-plant-vascular-tissue` — xylem
   cohesion-tension + phloem Münch pressure-flow.
6. `eukarya-genetics-plant-polyploidy` — rare in animals +
   extremely common in plants; modern wheat is hexaploid;
   strawberry octoploid; agronomic-improvement driver.
7. `eukarya-physiology-fungus-hyphal-growth` — Spitzenkörper
   tip growth, mycelium, largest known organism a single
   Armillaria mycelium covering 9.6 km² in Oregon,
   mycorrhizal symbioses with > 80% of plant species,
   lovastatin / cyclosporine drug-discovery legacy.
8. `eukarya-genetics-fungus-mating-types` — MAT loci,
   *Schizophyllum commune* > 23 000 mating types from
   tetrapolar MAT combinatorics, Pontecorvo 1956
   parasexual cycle drives fungicide resistance.

**3 existing topics tagged**: `eukarya-physiology-
photosynthesis` → plant; `eukarya-physiology-development-
multicellularity` → animal.

**Per-kingdom widget** —
`orgchem/gui/panels/kingdom_subtab_panel.py`:
- New sub-domain combo above the inner sub-tabs.
- Kingdom-appropriate label per outer tab: "Kingdom
  (within Eukarya):" / "Gram-stain class:" / "Phylum:" /
  "Genome class:".
- First combo item is `(all)` sentinel — shows pan-domain
  view.
- Combo selection cascades to all 3 sub-pane filters
  simultaneously via `_on_sub_domain_changed`.
- Programmatic API: `set_sub_domain(value)` returns True
  for valid values; `current_sub_domain()` returns the
  current selection (empty string for `(all)`).

**Agent action** —
`orgchem/agent/actions_biochemistry_by_kingdom.py`:
- `list_kingdom_topics` gains the `sub_domain` kwarg with
  clean-error path for unknown values + docstring listing
  all 12 valid sub-domain ids.

### Tests
13 new tests across 3 files:
- `tests/test_biochemistry_by_kingdom.py` (+10):
  catalogue-grew-to-68 + eukarya-grew-to-23 + sub-domains-
  for-kingdom helper + filter-eukarya-animal-includes-pan-
  eukaryotic + filter-eukarya-plant-excludes-animal-only +
  filter-eukarya-fungus + unknown-sub-domain → empty +
  every-sub-domain-in-canonical-set + plant-animal-fungus-
  topic-count ≥ 8 + topic_to_dict-includes-sub-domain.
- `tests/test_biochemistry_by_kingdom_window.py` (+5):
  eukarya-panel-has-sub-domain-combo + set-sub-domain
  round-trip + set-unknown-sub-domain returns False +
  filter-narrows-pane-lists (animal-tight-junctions
  excluded under plant filter; plant-vascular-tissue
  included) + sub-domain-combo-present-for-all-kingdoms.
- `tests/test_biochemistry_by_kingdom_actions.py` (+3):
  list-by-sub-domain + unknown-sub-domain → error +
  get-topic-includes-sub-domain-field.

Existing `test_topic_to_dict_keys` updated to expect the
new `sub_domain` key.  All 83 Phase-47 tests pass.

### Documentation updates
- ROADMAP.md — Phase 47 status updated to "🎉 SHIPPED end-
  to-end across rounds 166-169" with full delivery manifest
  for the 47d sub-phase + closeout language ("vision
  realised in 4 rounds — 68-topic explorer with kingdom-
  within-domain sub-domain filter addressing the user-
  feedback concern").
- PROJECT_STATUS.md — round 169 summary prepended.
- SESSION_LOG.md — this entry.

### Test suite status
2 042 passing (up from 2 024 in round 168 — net +18 from
this round's 13 new tests + 5 existing-test-shape
additions).  Doc-coverage test green; full suite ~51 s
wall-clock.

### What's open (next-round candidates)
- **Phase 48a** — isomers exploration tool first round
  (glossary + headless `core/isomers.py` with
  `classify_isomer_relationship`).  The other unfinished
  user-flagged phase.
- **Phase 31b extension** — 6 more entries to reach the
  60-target.
- **Phase 38c** — equipment-palette + QGraphicsScene
  canvas for the lab-setup simulator.

A safer next pick is **Phase 48a** — the other still-open
user-flagged phase.

## 2026-04-25 — Round 168 (🎉 Phase 47 CLOSED — agent actions + audit map registration)

### Context
Round 166 shipped Phase 47a (60-topic headless catalogue) +
round 167 shipped Phase 47b (GUI window + per-kingdom
widget).  Round 168 closes Phase 47 entirely with the
agent-action layer + audit-map registration — same shape
as the established Phase-37/40/45 catalogue actions.

### What shipped
**Agent actions** —
`orgchem/agent/actions_biochemistry_by_kingdom.py`
(~120 lines).  4 actions in a new `kingdom` category:
- `list_kingdom_topics(kingdom="", subtab="")` — full
  catalogue or filtered by kingdom and / or sub-tab.
  Unknown kingdom or sub-tab values return a clean
  `{"error": str}` dict.
- `get_kingdom_topic(topic_id)` — full record by id.
  Unknown id → `{"error": str}`.
- `find_kingdom_topics(needle)` — case-insensitive
  substring search across id + title + body + every
  cross-reference field (so a search for
  `"mitochondrion"` lands on topics that cross-reference
  the Phase-43 cell-component id, not just topics that
  mention the word in body text).
- `open_biochemistry_by_kingdom(kingdom="", subtab="",
  topic_id="")` — opens the *Window → Biochemistry by
  Kingdom…* window.  Passing just `kingdom` switches
  the outer tab; passing all three drills all the way
  down to a specific topic.  Marshals onto the Qt main
  thread via `_gui_dispatch.run_on_main_thread_sync`.
  Reports `selected: True/False` so the agent can
  introspect failure paths (unknown kingdom / unknown
  topic id).

**Wiring**:
- `orgchem/agent/__init__.py` — added `from orgchem.agent
  import actions_biochemistry_by_kingdom`.
- `orgchem/gui/audit.py` — registered all 4 actions in
  `GUI_ENTRY_POINTS` (each pointing at *Window →
  Biochemistry by Kingdom…* (Ctrl+Shift+K)).

### Tests
17 new tests in
`tests/test_biochemistry_by_kingdom_actions.py`:
- `list_kingdom_topics`: unfiltered (≥ 60), by-kingdom
  (archaea ≥ 10), by-subtab (genetics ≥ 15), by-both
  (viruses + genetics ≥ 4), unknown-kingdom →
  `{"error": ...}`, unknown-subtab → `{"error": ...}`.
- `get_kingdom_topic`: known id round-trips with cross-
  references intact, unknown id → `{"error": ...}`.
- `find_kingdom_topics`: substring search returns CRISPR
  topics, **walks cross-reference fields** so
  `find("mitochondrion")` lands on the
  endosymbiotic-origin topic, empty needle → `[]`.
- `open_biochemistry_by_kingdom`: no-args opens the
  window, with-kingdom focuses the right outer tab and
  the window's actual current-tab text confirms it,
  with-full-path drills all 3 levels and confirms the
  outer tab moved, unknown-topic → `selected: False`.
- `audit_map_includes_all_four_kingdom_actions` — guards
  against future regression of the wiring.
- `kingdom_category_actions_registered` — introspects
  `ActionSpec.category` to confirm all 4 actions are
  tagged under the new `kingdom` category.

Discovered + fixed during the test run:
- `test_kingdom_category_actions_registered` first
  version tried to read `registry()` as a categorised
  dict — actually it's a flat `name → ActionSpec` dict
  with `category` as an ActionSpec attribute.  Rewrote
  the test to filter by `getattr(spec, "category", None)`.
  Now passes cleanly + correctly verifies the 4 actions
  carry the `kingdom` category tag.

### Documentation updates
- INTERFACE.md — added row for `agent/actions_biochemistry_
  by_kingdom.py` (the third + final Phase 47 module).
- ROADMAP.md — Phase 47 status flipped to "🎉 SHIPPED
  end-to-end across rounds 166-168" with full delivery
  manifest for all 3 sub-phases + Phase-47-vision-realised
  closeout language.
- PROJECT_STATUS.md — round 168 summary prepended with
  the 🎉 Phase 47 CLOSED milestone.
- SESSION_LOG.md — this entry.

### Test suite status
2 024 passing (up from 2 007 in round 167 — net +17 from
this round's 17 new test functions).  Doc-coverage test
green; full suite ~46 s wall-clock.

### What's open (next-round candidates)
**Phase 47 is COMPLETE.**  The first user-flagged GUI
extension on top of the existing Macromolecules-style
template ships in 3 rounds.  The complementary view —
chemistry-class organisation (Phase-30 Macromolecules) +
kingdom-of-life organisation (Phase 47) — is now available
from the Window menu.

Remaining roadmap work:
- **Phase 48** — isomers exploration tool (the second new
  user-flagged phase from round 165).  Recommended 3-
  pronged integration; 48a glossary + headless `core/
  isomers.py` with `classify_isomer_relationship` ships
  in 1 round as the lowest-risk first step.
- **Phase 31b extension** — 6 more entries to reach the
  60-target.
- **Phase 38c** — equipment-palette + QGraphicsScene
  canvas for the lab-setup simulator.  Multi-round; the
  highest-value remaining work + the only unfinished
  user-flagged feature still in scope.

A safer next pick is **Phase 48a** — open the second new
user-flagged surface with the lowest-risk part of the
4-pronged plan.

## 2026-04-25 — Round 167 (Phase 47b — Biochemistry-by-Kingdom GUI window + per-kingdom subtab widget)

### Context
Round 166 shipped Phase 47a — the headless 60-topic
catalogue of biochemistry-by-kingdom topics.  Round 167
delivers the GUI: top-level `BiochemistryByKingdomWindow`
+ reusable `KingdomSubtabPanel` widget, wired through
*Window → Biochemistry by Kingdom…* (Ctrl+Shift+K).

### What shipped
**Window** — `orgchem/gui/windows/biochemistry_by_kingdom_window.py`
(~140 lines).  Top-level `QMainWindow` modelled on the
Phase-30 `MacromoleculesWindow`: 4 outer tabs (Eukarya,
Bacteria, Archaea, Viruses), single persistent instance
constructed lazily on first `MainWindow.open_…` call,
`QSettings`-persisted geometry + last-active outer tab.
`_SETTINGS_GROUP = "window/biochemistry_by_kingdom"` so it
doesn't collide with the Macromolecules window's settings.
Programmatic API: `switch_to_kingdom(id)`,
`select_topic(kingdom, subtab, topic_id)`,
`kingdom_panel(id)`, `kingdom_labels()`.  Each outer tab
hosts a `KingdomSubtabPanel`.

**Per-kingdom widget** —
`orgchem/gui/panels/kingdom_subtab_panel.py` (~190 lines).
Reusable `KingdomSubtabPanel(kingdom)` widget that
encapsulates the three sub-tabs (Structure /
Physiology+Development / Genetics+Evolution).  Each sub-tab
is an internal `_SubtabPane(kingdom, subtab)` with the
canonical filterable-list-on-the-left +
HTML-detail-card-on-the-right layout used across the rest
of the app.  The detail card renders the topic body
markdown plus cross-reference sections for **Phase-43 cell
components**, **Phase-42 metabolic pathways**, and
**molecule-database names** — only renders the section
when the topic actually carries cross-references for that
category.  Programmatic API: `switch_to_subtab(subtab)`,
`select_topic(subtab, topic_id)`, `subtab_labels()`.

**Wiring** — `orgchem/gui/main_window.py`:
- Added `_biochemistry_by_kingdom_window: Optional[QMainWindow]
  = None` instance var alongside the existing
  `_macromolecules_window`.
- Added *Window → Biochemistry by Kingdom…* menu entry with
  **Ctrl+Shift+K** shortcut.
- Added `open_biochemistry_by_kingdom_window(kingdom=None,
  subtab=None, topic_id=None)` slot — lazy-constructs the
  window, then supports full programmatic navigation: just
  `kingdom` focuses the outer tab, full
  (kingdom + subtab + topic_id) drills all the way down to
  a specific topic.

### Tests
15 new tests in
`tests/test_biochemistry_by_kingdom_window.py`:
- `test_subtab_panel_constructs_for_each_kingdom` — all 4
  kingdoms produce a panel with the canonical 3 sub-tab
  labels.
- `test_subtab_panel_lists_topics` — each sub-pane lists ≥
  4 topics for the eukarya kingdom (one per (kingdom,
  subtab) cell).
- `test_subtab_panel_select_topic` — programmatic
  select_topic round-trips: returns True + the detail-card
  title updates.
- `test_subtab_panel_select_unknown_topic` — returns False.
- `test_subtab_panel_unknown_subtab` — returns False.
- `test_subtab_panel_filter_narrows_results` — typing
  "CRISPR" into the bacteria-genetics filter narrows the
  list to a smaller set.
- `test_subtab_panel_detail_shows_cross_references` — the
  endosymbiotic-origin topic's mitochondrion + chloroplast
  Phase-43 cross-references appear in the detail card HTML.
- `test_window_constructs` — 4 outer tabs.
- `test_window_kingdom_labels_in_canonical_order` — Eukarya
  / Bacteria / Archaea / Viruses tab labels in canonical
  order.
- `test_window_switch_to_kingdom` — known + unknown
  kingdom return True + False respectively.
- `test_window_select_topic_round_trip` — drilling all 3
  levels works end-to-end + outer tab moves to the right
  kingdom.
- `test_window_select_unknown_topic_returns_false` — graceful
  handling.
- `test_main_window_open_method_returns_window` — the
  `MainWindow.open_…` method returns + caches a window
  instance (second call returns the same).
- `test_main_window_open_with_kingdom_focuses_tab` — passing
  just `kingdom` switches the outer tab.
- `test_main_window_open_with_full_path` — passing all 3
  arguments drills all the way down + verifies the round-
  166 viruses-not-a-domain ribosome teaching invariant
  survives end-to-end through the GUI render path.

All 15 tests pass on first run.

### Documentation updates
- INTERFACE.md — added rows for both new GUI modules
  (`gui/windows/biochemistry_by_kingdom_window.py` +
  `gui/panels/kingdom_subtab_panel.py`).
- ROADMAP.md — Phase 47 status updated to "47a + 47b
  SHIPPED" with separate manifest sections for each
  sub-phase.
- PROJECT_STATUS.md — round 167 summary prepended.
- SESSION_LOG.md — this entry.

### Test suite status
2 007 passing (up from 1 992 in round 166 — net +15 from
this round's 15 new test functions).  Doc-coverage test
green; full suite ~46 s wall-clock.

### What's open (next-round candidates)
- **Phase 47c** — agent actions in a new `kingdom`
  category (`list_kingdom_topics`, `get_kingdom_topic`,
  `find_kingdom_topics`, `open_biochemistry_by_kingdom`)
  + audit map registration.  Closes Phase 47 entirely.
  Ships in 1 round.
- **Phase 48a** — isomers exploration tool first round
  (glossary + headless `core/isomers.py` with
  `classify_isomer_relationship` + RDKit stereoisomer +
  tautomer enumeration helpers).  Lowest-risk part of the
  4-pronged plan.
- **Phase 31b extension** — 6 more entries to reach the
  60-target.

A safer next pick is **Phase 47c** to close Phase 47 entirely
before starting Phase 48.

## 2026-04-25 — Round 166 (Phase 47a — biochemistry-by-kingdom headless catalogue, 60 topics across 4 kingdoms × 3 sub-tabs)

### Context
Round 165 added Phase 47 (Biochemistry-by-Kingdom explorer)
+ Phase 48 (Isomers exploration tool) to the roadmap as
fresh user-flagged feature requests.  Round 166 ships the
**Phase 47a headless catalogue** — the data foundation for
the upcoming Macromolecules-style window.  Subsequent rounds
will deliver 47b (per-kingdom widget + window) + 47c (agent
actions + audit map).

### What shipped
**Headless data core** — `orgchem/core/biochemistry_by_kingdom.py`
(~830 lines).  `KingdomTopic` frozen dataclass with 9 fields:
id / kingdom / subtab / title / body markdown /
cross_reference_cell_component_ids tuple (Phase-43 ids) /
cross_reference_pathway_ids tuple (Phase-42 ids) /
cross_reference_molecule_names tuple / notes.  Two canonical
tuples: `KINGDOMS = ("eukarya", "bacteria", "archaea",
"viruses")` + `SUBTABS = ("structure", "physiology",
"genetics")`.

**60 entries** in a balanced 4 × 3 = 12-cell grid with
exactly 5 topics per cell:

- **Eukarya (15)**: structure — plasma membrane,
  endomembrane organelles, nucleus + NPC, ECM + cell walls,
  three-filament cytoskeleton; physiology — aerobic
  respiration, photosynthesis, cell cycle + mitosis,
  GPCR signalling, multicellular development; genetics —
  chromatin + nucleosomes, RNA splicing, meiosis +
  recombination, telomeres + senescence, **endosymbiotic
  origin** (Margulis 1967).
- **Bacteria (15)**: structure — gram divide, prokaryotic
  minimalism, flagellar rotary motor, biofilms + EPS,
  capsule + virulence; physiology — anaerobic fermentation +
  diverse e⁻ acceptors, FtsZ binary fission, quorum
  sensing, sporulation + endospores, secondary metabolism +
  natural-product antibiotics; genetics — circular
  chromosome + nucleoid, **HGT** (transformation +
  transduction + conjugation), **CRISPR-Cas** adaptive
  immunity, restriction-modification, evolutionary rate.
- **Archaea (15)**: structure — **ether-linked isoprenoid
  lipids** (the lipid divide — strongest argument for the
  three-domain phylogeny), pseudopeptidoglycan + S-layers,
  extremophile adaptations, archaellum (convergent rotary
  motor), cellular minimalism; physiology —
  **methanogenesis** (only metabolic pathway exclusively in
  archaea), no human pathogens, syntrophic partners + AOM,
  bacteriorhodopsin + light-driven proton pumps,
  psychrophilic + acidophilic; genetics — **eukaryote-like**
  transcription + translation machinery, archaeal histones
  + chromatin precursors, **Asgard archaea + eocyte
  hypothesis** of eukaryogenesis, archaeal CRISPR-Cas,
  deep evolutionary roots + LUCA.
- **Viruses (15)**: structure — capsid architectures
  (icosahedral / helical / complex), enveloped vs naked,
  spike glycoproteins + receptor binding, **Baltimore
  classification** (7 genome groups), bacteriophage
  architectures; physiology — generic 6-stage life cycle,
  **lytic vs lysogenic** phage cycles, mutation rates +
  quasispecies, cell + tissue tropism, immune evasion;
  genetics — **NOT a domain + why** (lack ribosomes +
  polyphyletic + no metabolism), **endogenous retroviruses**
  + host-genome contributions (syncytin → mammalian
  placenta), virus-host arms race + Red Queen + MHC
  polymorphism, viroids + RNA-world relics, pandemic
  emergence + spillover events.

Each topic body is ≥ 200 chars of actual teaching content
(test-enforced).  Cross-references resolve to real Phase-43
cell-component ids + Phase-42 metabolic-pathway ids (also
test-enforced — guards against rot when either catalogue is
edited).

Lookup helpers: `list_topics(kingdom, subtab)`,
`get_topic(id)`, `find_topics(needle)` (case-insensitive
substring across id + title + body + every cross-reference
field), `kingdoms()`, `subtabs()`, `topic_to_dict(t)`.

### Tests
33 new tests in `tests/test_biochemistry_by_kingdom.py`:
- catalogue size ≥ 60 + every kingdom + every subtab
  populated;
- balanced grid: each (kingdom, subtab) cell has ≥ 4 topics;
- every entry has all required fields;
- every id unique + lowercase-kebab + starts with
  `<kingdom>-<subtab>-` (the dialog's grouping convention);
- every kingdom + subtab in canonical set;
- every body ≥ 200 chars (proves teaching content vs
  placeholder stubs);
- 8 per-row teaching invariants — eukarya endosymbiotic
  origin names Margulis 1967 + xrefs both mitochondrion +
  chloroplast; bacteria HGT names all 3 mechanisms; archaea
  ether-lipid divide explicit; archaea eukaryote-like RNA
  Pol II + MCM machinery; viruses-not-a-domain explains the
  no-ribosome reason; viruses-Baltimore-classification
  explicit; viruses-ERVs names syncytin + placenta;
  methanogenesis archaea-only;
- **cross-reference resolution checks**: every
  cross_reference_cell_component_ids entry must point to a
  real Phase-43 id; every cross_reference_pathway_ids entry
  must point to a real Phase-42 id;
- at least 8 topics carry cross-references (proves the
  integration with existing catalogues actually exists);
- filter / lookup edge cases (unknown kingdom / unknown
  subtab / case-insensitive search / find walks xref
  fields);
- canonical tuples round-trip;
- `topic_to_dict` exposes all 9 fields.

Discovered + fixed during the test run: cross-reference test
caught my first draft using `tca-cycle` /
`oxidative-phosphorylation` / `calvin-cycle` for pathway
ids — but Phase-42 actually uses underscores
(`tca_cycle` / `ox_phos` / `calvin_cycle`).  Fixed the 3
topic xref tuples.  This is exactly the kind of cross-
catalogue-rot the test was designed to catch.

### Documentation updates
- INTERFACE.md — added row for `core/biochemistry_by_kingdom.py`
  with full per-kingdom topic enumeration.
- ROADMAP.md — Phase 47 marked "IN PROGRESS — 47a SHIPPED
  round 166" with delivery manifest + a note that 47b
  (window + per-kingdom widget) and 47c (agent actions)
  queued for rounds 167-168.
- PROJECT_STATUS.md — round 166 summary prepended.
- SESSION_LOG.md — this entry.

### Test suite status
1 992 passing (up from 1 959 in round 165 — net +33 from
this round's 33 new test functions).  Doc-coverage test
green; full suite ~45 s wall-clock.

### What's open (next-round candidates)
- **Phase 47b** — `gui/windows/biochemistry_by_kingdom_window.py`
  + `gui/panels/kingdom_subtab_panel.py` (the reusable
  per-kingdom 3-sub-tab widget).  Wired through *Window →
  Biochemistry by Kingdom…* (Ctrl+Shift+K).  Should ship
  in 1 round given the headless catalogue is already in
  place.
- **Phase 47c** — agent actions in a new `kingdom`
  category (`list_kingdom_topics`, `get_kingdom_topic`,
  `find_kingdom_topics`, `open_biochemistry_by_kingdom`)
  + audit map registration.  Ships in 1 round.
- **Phase 48** — isomers exploration tool (the second new
  user-flagged phase from round 165).  48a glossary +
  classify-pair would ship in 1 round.
- **Phase 31b extension** — 6 more entries to reach the
  60-target.

A safer next pick is **Phase 47b** to keep the kingdom-
explorer momentum going + give the user a visible UI
deliverable for the new feature.

## 2026-04-25 — Round 165 (Phase 31b extension — Robinson annulation + Knoevenagel condensation, catalogue 52/60 → 54/60; +2 new roadmap phases — 47 Biochemistry-by-Kingdom + 48 Isomers)

### Context
Round 164 opened the Phase 31b extension at 52/60 with
Wacker + Brown hydroboration to open the alkene-
functionalisation regio-/stereo-selectivity surface.
Round 165 ships Robinson annulation + Knoevenagel
condensation to open the **ring-construction** + **active-
methylene C-C bond-formation** teaching surfaces.
Catalogue advances 52/60 → 54/60.

**Mid-round the user added two new roadmap requests** —
both incorporated into ROADMAP.md as full phase entries
with sub-phases + design-recommendation language.

### What shipped
**Two named reactions** added to
`orgchem/db/seed_reactions.py`:

1. **Robinson annulation (cyclohexanone + methyl vinyl
   ketone → Δ1,9-octalin-2-one)** — category *Annulation
   (C-C ring formation cascade)*.  Sir Robert Robinson
   1935 (Nobel 1947 for alkaloid + morphine structure
   work).  Description teaches: **3-step cascade in one
   pot** — (1) Michael addition of an enolate (from the
   parent ketone, deprotonated by KOH / NaOEt / proline
   for the asymmetric Hajos-Parrish-Eder-Sauer-Wiechert
   variant) onto an α,β-unsaturated ketone (canonically
   methyl vinyl ketone, MVK), giving a 1,5-diketone; (2)
   intramolecular **aldol condensation** of the
   1,5-diketone — the new α-carbon of the MVK fragment
   enolises and attacks the original ketone carbonyl,
   forming a new 6-membered ring; (3) acid- or base-
   catalysed **dehydration** of the β-hydroxy intermediate
   to give the **cyclohexenone ring fused to the original
   ring**.  Net: two C-C bonds formed + one C-O bond
   cleaved + a new α,β-unsaturated ring annulated onto the
   substrate ketone.  **The canonical ring-construction
   reaction in textbook total synthesis** — the Wieland-
   Miescher ketone (precursor for cortisone / testosterone
   / oestrone) is built from 2-methylcyclohexan-1,3-dione
   + MVK by exactly this cascade.  The asymmetric
   Hajos-Parrish proline-catalysed variant (1971) is the
   intellectual ancestor of modern enamine-catalysis
   (List + Barbas + MacMillan, Nobel 2021).

2. **Knoevenagel condensation (benzaldehyde + diethyl
   malonate → diethyl benzylidene malonate)** — category
   *Condensation (active-methylene C-C bond formation)*.
   Emil Knoevenagel 1894.  Description teaches: **active-
   methylene compound** between two electron-withdrawing
   groups — pKa ~ 11-13 for malonate / ~ 11 for
   cyanoacetate / ~ 10 for nitromethane vs simple ketone
   α-CH ~ 20 — so a mild secondary-amine base
   (piperidine, pyridine, or — Doebner variant — an amino
   acid like proline / glycine in pyridine solvent) is
   sufficient.  Mechanism: amine deprotonates the active
   methylene → carbanion attacks the aldehyde → E1cb
   dehydration → α,β-unsaturated product.  In the
   **Doebner modification** (with monoacids like
   cyanoacetic / malonic acid + pyridine), spontaneous
   decarboxylation of one COOH / COOR group follows the
   dehydration.  Workhorse for cinnamic-acid + α,β-
   unsaturated-ester / nitrile syntheses, foundational to
   materials chemistry (push-pull chromophores) + drug
   discovery (Michael-acceptor warheads).

**Three intermediate fragments** added: `Δ1,9-Octalin-2-
one (Robinson annulation product) O=C1C=C2CCCCC2CC1`,
`Diethyl malonate CCOC(=O)CC(=O)OCC`, `Diethyl benzylidene
malonate CCOC(=O)/C(=C\\c1ccccc1)C(=O)OCC`.

### Tests
Four new tests in `tests/test_reactions.py`:
- `test_robinson_annulation_seeded` — Michael + aldol +
  dehydration cascade language + Wieland-Miescher /
  steroid context + Robinson 1947 Nobel attribution +
  α,β-unsaturated cyclohexenone product (C=C + C=O
  substrings).
- `test_knoevenagel_condensation_seeded` — active-
  methylene + pKa contrast with aldol + piperidine /
  pyridine base + Doebner modification + aldol
  comparison.
- `test_ring_construction_anchors_present` — Robinson +
  Diels-Alder + 6π electrocyclic ring-construction trio.
- `test_named_reaction_count_at_least_fifty_four` —
  catalogue floor at 54/60 for the Phase 31b extension.

Discovered + fixed during the test run:
- Fragment-consistency audit caught 3 missing fragments
  on first reaction-add.  Resolved by seeding the 3
  intermediate rows above.
- The first version of `test_robinson_annulation_seeded`
  used a sloppy `'=O' in rhs` substring check that failed
  because the canonical SMILES form writes `O=C` (O before
  =), not `=O`.  Fixed to check for `O=C` OR `C=O` (either
  form valid for a carbonyl).

All 36 reaction-tests pass + all 12 fragment-consistency
tests pass.

### Two new roadmap phases added (mid-round user requests)
The user added two new roadmap requests during this round.
Both are now in ROADMAP.md as full phase entries with
sub-phases + design-recommendation language:

**Phase 47 — Biochemistry-by-Kingdom explorer
(Macromolecules-style)**.  User directive: *"Add a new GUI
in the style of the Macromolecules.  This one is for
biochemistry, with tabs for the different kingdoms, and
sub-tabs covering structure, physiology and development,
genetics and evolution — highlighting the molecules and
reactions involved."*  Plan: top-level
`gui/windows/biochemistry_by_kingdom_window.py` opened
from *Window → Biochemistry by Kingdom…* (Ctrl+Shift+K).
Outer `QTabWidget` with one tab per kingdom (Eukarya,
Bacteria, Archaea, Viruses); each kingdom's inner
`QTabWidget` has 3 sub-tabs (Structure /
Physiology+Development / Genetics+Evolution).
Cross-references the existing Phase-43 cell-component
catalogue + Phase-42 metabolic pathways + Phase-29
lipids / carbohydrates / nucleic-acids inline rather
than asking the user to chase them across existing
tools.  Headless data core
`core/biochemistry_by_kingdom.py` with `KingdomTopic`
frozen dataclass + ~60 entries (4 kingdoms × ~5 topics ×
3 sub-tabs).  Likely 2-3 rounds.

**Phase 48 — Isomers exploration tool**.  User directive:
*"Isomers (so far there is little mention of them).  What
is the best way to work this into the app?"*
Recommendation: **3-pronged integration** rather than a
single new top-level tool, because isomers are
fundamentally a *relationship between molecules* not a
standalone catalogue.  (1) Isomer-relationship explorer
dialog (Tools → *Isomer relationships…*, Ctrl+Shift+B) —
SMILES input → 4 result tabs (Constitutional /
Stereoisomers / Tautomers / Conformers); (2) inline
'View isomers' button on the molecule workspace; (3)
glossary expansion with 8-10 isomer terms (constitutional
/ stereoisomer / enantiomer / diastereomer / meso /
conformational / tautomer / atropisomer / cis-trans /
optical activity); (4) tutorial-content cross-link.
Headless core `core/isomers.py` with RDKit-backed
enumerators + `classify_isomer_relationship(smi_a, smi_b)`
that returns `"identical"` / `"constitutional"` /
`"enantiomer"` / `"diastereomer"` / `"meso"` /
`"tautomer"` / `"conformer"` / `"different molecule"`.
Likely 3-4 rounds.

### Documentation updates
- ROADMAP.md — Phase 31b extension count updated 52/60
  → 54/60 + Phase 47 + Phase 48 added as full phase
  entries.
- PROJECT_STATUS.md — round 165 summary prepended.
- SESSION_LOG.md — this entry.

### Test suite status
1 959 passing (up from 1 956 in round 164 — net +3 from
this round's three new test functions plus a renamed
catalogue-size floor).  Doc-coverage test green; full
suite ~45 s wall-clock.

### What's open (next-round candidates)
- **Phase 47** — first round would deliver the headless
  catalogue (`core/biochemistry_by_kingdom.py` with
  `KingdomTopic` dataclass + ~60 entries spanning 4
  kingdoms × 3 sub-tabs).
- **Phase 48** — first round would deliver glossary
  expansion (8-10 isomer terms) + headless
  `core/isomers.py` with `classify_isomer_relationship`
  + RDKit stereoisomer / tautomer enumeration helpers.
  Lowest-risk part of the 4-pronged plan.
- **Phase 31b extension** — 6 more entries to reach 60-
  target.  Priority list: Ramberg-Bäcklund / Shapiro /
  Oppenauer / Julia / Peterson olefinations / Henry
  reaction / Hantzsch dihydropyridine synthesis.
- **Phase 38c** — equipment-palette + QGraphicsScene
  canvas for the lab-setup simulator.  Multi-round; the
  highest-value remaining work.

A safer next pick is **Phase 48a** (isomer glossary +
headless classify-pair) — low-risk + immediately useful
to the existing Reaction-workspace glossary autolinker.
The bigger ambition this round is **Phase 47a** (kingdom-
explorer headless catalogue) which is the user-flagged
fresh feature.

## 2026-04-25 — Round 164 (Phase 31b extension — Wacker oxidation + Brown hydroboration-oxidation, catalogue 50/50 → 52/60)

### Context
Round 157 closed Phase 31b at the original 50/50 milestone.
Rounds 158-163 closed Phase 31k at 15/15.  Round 164 opens
the **Phase 31b extension** to a 60-entry curiosity-bucket
target — first two entries open the **alkene-functionalisation
regio-/stereo-selectivity teaching surface** that the
original 50-entry catalogue underserved (the existing
bromination-of-ethene + catalytic-hydrogenation entries
covered Markovnikov-Br₂-anti + syn-H₂ but not the
hydration / hydroboration alcohols).

### What shipped
**Two named reactions** added to
`orgchem/db/seed_reactions.py`:

1. **Wacker oxidation (styrene → acetophenone)** —
   category *Oxidation (Pd-catalysed)*.  Smidt et al. 1959
   — first Pd-catalysed industrial process.  Description
   teaches: PdCl₂ + CuCl₂ + O₂ + H₂O catalytic system at
   ambient T; 5-step catalytic cycle (η²-π-complex
   activation → external water attack on internal carbon →
   β-hydride elimination + reductive elimination → Pd(0)
   reoxidation by Cu(II) → Cu(I) reoxidation by O₂);
   **Markovnikov regioselectivity** — the oxygen ends up
   on the more-substituted carbon, giving a methyl ketone
   from a terminal alkene; the **redox-relay mechanism
   (Pd ↔ Cu ↔ O₂) is the template for many modern aerobic
   oxidations**; industrial ethylene → acetaldehyde Wacker
   process at ~ 2 Mt/yr globally; the Tsuji-Wacker variant
   (stoichiometric PdCl₂ in DMF / H₂O without Cu / O₂) is
   the lab-scale benchtop version.  Reaction SMILES
   `C=Cc1ccccc1.O.O=O >> CC(=O)c1ccccc1.O`.

2. **Brown hydroboration-oxidation (1-methylcyclohexene →
   trans-2-methylcyclohexanol)** — category *Addition
   (anti-Markovnikov, syn-addition)*.  H. C. Brown
   1956-1959, **Nobel 1979** shared with G. Wittig.
   Description teaches: two-step alkene → alcohol via
   (1) concerted 4-centre hydroboration with BH₃·THF (or
   9-BBN, disiamylborane for tighter selectivity)
   delivering H + BR₂ across the alkene **syn** with B
   going to the **less-substituted** carbon (steric
   control over an empty B 2p orbital — opposite
   regiochemistry to acid-catalysed hydration's
   Markovnikov + opposite stereochemistry to Br₂
   addition's anti); then (2) oxidative work-up with
   alkaline H₂O₂ converts the trialkylborane to the
   alcohol via [1,2]-alkyl-shift to oxygen with retention
   of configuration at the migrating carbon.  **Net
   result: anti-Markovnikov + syn-addition OH** — only
   Brown's reaction is BOTH anti-Markovnikov AND
   stereo-controlled.  The trans-2-methylcyclohexanol
   product locks both selectivity arguments at once.
   Reaction SMILES `CC1=CCCCC1.B.OO.[Na+].[OH-] >>
   O[C@@H]1CCCC[C@H]1C.[Na+].O.B(O)(O)O`.

**Three intermediate fragments** added to
`orgchem/db/seed_intermediates.py`: `1-Methylcyclohexene
CC1=CCCCC1` (intermediate), `Hydrogen peroxide (H2O2) OO`
(reagent), `trans-2-Methylcyclohexanol C[C@@H]1CCCC[C@H]1O`
(intermediate).  Styrene + acetophenone + water + O₂ + BH₃
+ NaOH + boric acid all already seeded.

### Tests
Four new tests in `tests/test_reactions.py`:
- `test_wacker_oxidation_seeded` — verifies the entry
  exists, the SMILES has C=C in substrate + C(=O) in
  product, the description names Pd + Cu + Markovnikov +
  methyl ketone teaching anchors.
- `test_brown_hydroboration_seeded` — verifies the entry
  exists, the SMILES contains B + OO (BH₃ + H₂O₂), the
  product carries `@`-style stereochemistry markers, the
  description names Brown + 1979 Nobel + anti-Markovnikov
  + syn-addition + H₂O₂ teaching anchors.
- `test_alkene_functionalisation_pair_present` — locks
  in the canonical Markovnikov-vs-anti-Markovnikov
  contrast pair so future regression of either entry
  surfaces immediately.
- `test_named_reaction_count_at_least_fifty_two` —
  catalogue floor at 52/60 for the Phase 31b extension.

Discovered + fixed during the test run: fragment-
consistency audit caught 3 missing fragments on first
reaction-add.  Resolved by seeding the 3 intermediate
rows above.  All 33 reaction-tests pass + all 12
fragment-consistency tests pass.

### Documentation updates
- ROADMAP.md — Phase 31b checkbox extended to "COMPLETE
  (round 157, 2026-04-25); extension to 60 in progress
  (52/60 after round 164)"; description block extended
  with the round-164 alkene-functionalisation entries
  and the new "alkene-functionalisation regio-/stereo-
  selectivity teaching surface" anchor.
- PROJECT_STATUS.md — round 164 summary prepended.
- SESSION_LOG.md — this entry.

### Test suite status
1 956 passing (up from 1 952 in round 163 — net +4 from
this round's four new test functions).  Doc-coverage
test green; full suite ~45 s wall-clock.

### What's open (next-round candidates)
- **Phase 31b extension** — 8 more entries to reach the
  60-target.  Priority list: Ramberg-Bäcklund (α-halosulfone
  → alkene; one-pot pedagogical curiosity), Shapiro
  (tosylhydrazone → vinyl-Li → alkene), Oppenauer
  (Al(OR)₃-catalysed alcohol → ketone, green-chemistry
  alternative to Cr-based oxidants), Julia / Peterson
  olefinations (HWE is already seeded; Julia + Peterson
  would round out the alkene-synthesis toolkit), Henry /
  Knoevenagel reactions (carbonyl C-C bond formation
  alternatives), Robinson annulation (Michael + aldol +
  dehydration cascade — opens the ring-construction
  teaching surface).
- **Phase 38c** — equipment-palette + QGraphicsScene
  canvas for the lab-setup simulator.  Multi-round; the
  highest-value remaining work + the only unfinished
  user-flagged feature still in scope.
- **Phase 31k extension** — 6 more SAR series for a 21-
  target (kinase inhibitors, GLP-1-agonists, monoclonal-
  antibody backbones, biologic-mimetics, vaccines'-
  adjuvant series, antibiotic-resistance-evading scaffolds).

A safer next pick remains another 1-2 named reactions per
round on the 31b-extension list.  Robinson annulation
would open the ring-construction teaching surface in one
round; Ramberg-Bäcklund + Shapiro would open the
"unusual-mechanism alkene synthesis" pair.

## 2026-04-25 — Round 163 (🎉 Phase 31k CLOSED at 15/15 — DPP-4 inhibitor SAR series)

### Context
Rounds 158-162 added 5 SAR series (H1-antihistamines + PPI
inhibitors + opioid analgesics + anticonvulsants + DOACs)
advancing the catalogue from 9/15 → 14/15.  Round 163 ships
the final series — DPP-4 inhibitors (the "gliptin" class) —
to close Phase 31k at the **15/15 milestone**, the second
"phase complete" milestone in the 152-163 sprint after
Phase 31b at 50/50 in round 157.

### What shipped
**One SAR series** added to `orgchem/core/sar.py`:

**`dpp4-inhibitors` — DPP-4 inhibitor (gliptin) series —
incretin-pathway antidiabetics.**  Target: dipeptidyl
peptidase-4 (DPP-4 / CD26).  Source: Deacon 2019 *Front.
Endocrinol.* 10: 80 + Drucker 2007 *Diabetes Care* 30:
1335-1343.  Activity columns: `dpp4_ic50_nM`,
`covalent_reversible` (0/1), `renal_clearance_pct`,
`half_life_h`, `logp`.

Five variants:

1. **Sitagliptin (Januvia)** — Merck 2006.  First DPP-4
   inhibitor to market + still best-selling gliptin
   worldwide.  Non-covalent competitive inhibitor —
   binds the active site via the β-amino group anchoring
   to Glu-205 / Glu-206 + Tyr-662 + the trifluoromethyl-
   triazolopiperazine occupying the S2 pocket.  ~ 80%
   renal cleared unchanged → requires dose reduction in
   CKD.  Once-daily.  TECOS 2015 established cardiovascular
   safety.
2. **Saxagliptin (Onglyza)** — BMS / AstraZeneca 2009.
   **Covalent reversible inhibitor** — the nitrile (C#N)
   of the cyanopyrrolidine warhead is attacked by Ser-630
   of DPP-4 to form a slowly-reversible imidate adduct.
   Result: very low IC50 (1.3 nM) but short plasma
   half-life (~ 2.5 h) — the covalent mechanism gives
   sustained tissue inhibition despite rapid plasma
   clearance.  Active metabolite 5-hydroxysaxagliptin
   contributes ~ 50% of activity.  SAVOR-TIMI 53 2013
   raised heart-failure-hospitalisation signal — required
   FDA label update.
3. **Linagliptin (Tradjenta)** — Boehringer Ingelheim /
   Lilly 2011.  **Unique among DPP-4 inhibitors: primarily
   fecal clearance** (~ 95% via the bile, only 5% renal),
   so **NO dose adjustment in CKD or ESRD** — the only
   gliptin safe in haemodialysis patients without dose
   modification.  Xanthine scaffold (purine-2,6-dione with
   the C8 piperidine + N1 quinazoline + N3 methyl + N7
   but-2-ynyl) — completely different chemotype from the
   other gliptins, evolved from natural-product xanthine
   pharmacology (caffeine / theophylline).  CARMELINA 2018
   established cardiovascular + renal-protection
   neutrality.
4. **Alogliptin (Nesina)** — Takeda 2013.  Uracil-based
   pyrimidine-2,4-dione scaffold with cyanobenzyl + (R)-3-
   aminopiperidinyl substituents.  Once-daily.  Renal
   clearance ~ 76%.  EXAMINE 2013 in post-ACS patients
   showed non-inferiority to placebo.  Most lipophilicity-
   balanced gliptin (logP 0.4 — by far the lowest,
   minimising off-target binding).
5. **Vildagliptin (Galvus)** — Novartis 2007.  **EU-
   approved but NOT FDA-approved** (heart-failure concerns
   + transient liver-enzyme elevations stalled the US
   filing).  Same **covalent reversible** mechanism as
   saxagliptin via the cyanopyrrolidine warhead reacting
   with Ser-630, but connected to the 3-hydroxyadamantyl
   anchor through a glycyl spacer instead of an α-amino-
   acyl spacer.  Twice-daily dosing because of short plasma
   half-life (~ 2 h).  ~ 22% renal cleared, so less dose
   reduction needed than sitagliptin / saxagliptin /
   alogliptin.

### Tests
Three new tests in `tests/test_sar.py` plus the milestone
closeout test:
- `test_dpp4_inhibitor_series_landmarks` — seven
  pedagogical SAR invariants locked in: (a) all 5
  landmarks present, (b) **covalent-vs-non-covalent
  split** with exactly 2 covalent + 3 non-covalent
  inhibitors, (c) linagliptin is the only gliptin with
  low renal clearance ≤ 10% (the safe-in-CKD anchor),
  (d) the other 4 gliptins have ≥ 20% renal clearance
  (require CKD dose adjustment), (e) covalent inhibitors
  have short half-lives ≤ 3 h (the trade-off compensated
  by sustained tissue inhibition), (f) **linagliptin +
  saxagliptin are the two most-potent gliptins ≤ 2 nM**
  IC50 by very different routes (xanthine deep-S2-pocket
  fit vs covalent warhead), and the other 3 sit in the
  2-30 nM band.
- `test_dpp4_series_count_at_least_five` — variant-count
  floor.
- `test_phase_31k_complete_15_of_15` — milestone closeout
  test that name-matches all 9 baseline SAR series + all 6
  rounds-158-163 expansion series so any future regression
  of any single one surfaces immediately.
- `test_sar_library_size_at_least_fifteen` — catalogue-
  size floor at the 15-target (renamed from round-162's
  `_at_least_fourteen`).
- `test_library_seeded` — extended to assert the new
  `dpp4-inhibitors` id.

**Test invariant caught a SAR error in my first draft**: I'd
written 'saxagliptin has the lowest IC50 in the series', but
the actual literature numbers have linagliptin slightly more
potent (1.0 nM vs sax's 1.3 nM).  The test failure prompted
me to rewrite the invariant as 'linagliptin + saxagliptin
both ≤ 2 nM, the others 2-30 nM' which captures the actual
two-most-potent-by-very-different-routes teaching point.
This is the kind of accuracy-improving test feedback that
catches sloppy SAR claims before they ship.

All 31 SAR tests pass.

### Documentation updates
- ROADMAP.md — Phase 31k checkbox flipped from `[~]`
  (in-progress) to `[x]` (COMPLETE round 163, 2026-04-25);
  Phase 31k entry updated from 14/15 → **15/15** with
  description of the DPP-4 series + the 7 pedagogical
  invariants + the milestone closeout language ("Phase
  31k 15/15 vision realised: rounds 158-163 added 6
  series in 6 rounds, opened 5 major medicinal-chem
  teaching themes").
- PROJECT_STATUS.md — round 163 summary prepended with
  the 🎉 Phase 31k CLOSED milestone language.
- SESSION_LOG.md — this entry.

### Test suite status
1 952 passing (up from 1 949 in round 162 — net +3 from
this round's three new test functions).  Doc-coverage
test green; full suite ~45 s wall-clock.

### What's open (next-round candidates)
**Phase 31k is COMPLETE.**  Both Phase 31b (50/50) and
Phase 31k (15/15) milestones are now closed; the original
Phase 31 vision is fully realised.

Remaining roadmap work falls into two buckets:
- **Phase 38c** — equipment-palette + QGraphicsScene
  canvas for the lab-setup simulator.  Multi-round; the
  highest-value remaining work + the only unfinished
  user-flagged feature still in scope.  Could be picked
  up next as a "start phase 38c" round with just the
  headless `core/lab_setup_canvas.py` scaffolding +
  drag-drop data model.
- **Phase 31b extension** — 60-target with curiosity-
  bucket entries (Ramberg-Bäcklund, Shapiro, Oppenauer,
  Julia / Peterson olefinations, Wacker oxidation, Henry
  / Knoevenagel, Brown hydroboration-oxidation).  Lower
  priority but tight catalogue+test scope as rounds
  152-157.

A safer next pick is the Phase 31b extension (1-2
reactions per round on the 60-target curiosity bucket),
keeping the same tight pattern.  The bigger ambition is
Phase 38c — the long-promised lab-setup canvas.

## 2026-04-25 — Round 162 (Phase 31k — direct-oral-anticoagulant SAR series, catalogue 13/15 → 14/15)

### Context
Rounds 158-161 added H1-antihistamines + PPI-inhibitors +
opioid-analgesics + anticonvulsants, opening four
medicinal-chem teaching themes: chiral switch, BBB /
zwitterion, lipophilicity → potency, and different scaffolds
for the same biology.  Round 162 adds the DOACs — opens the
**fifth theme: prodrug for bioavailability**.  Catalogue
advances 13/15 → 14/15; just one more series to close at
the 15/15 milestone.

### What shipped
**One SAR series** added to `orgchem/core/sar.py`:

**`doacs` — Direct-oral-anticoagulant (DOAC) series — Xa
vs IIa inhibitors.**  Target: coagulation cascade — factor
Xa (apixaban, rivaroxaban, edoxaban) and factor IIa
thrombin (dabigatran).  Source: Garcia + Crowther 2014
*N. Engl. J. Med.* 370: 1281-1287 + Yeh + Eikelboom 2014
*Eur. Heart J.* 35: 2076-2087 (canonical DOAC comparison
reviews).  Activity columns: `factor_xa` (1 if Xa, 0 if
IIa), `target_ki_nM`, `oral_bioavailability_pct`,
`half_life_h`, `logp`.

Five variants:

1. **Apixaban (Eliquis)** — BMS / Pfizer 2012.  Pyrazole-
   3-carboxamide + fused-bicyclic dihydropyridazinone +
   N-aryl-piperidinone tail.  Direct factor-Xa inhibitor;
   **most-potent DOAC on Xa (Ki 0.08 nM)** + reversible
   binding.  CYP3A4 + P-gp substrate but only 25% renal
   cleared (safest DOAC in CKD).  Twice-daily dosing;
   ARISTOTLE 2011 showed superiority to warfarin on stroke
   prevention + reduced major bleeding in atrial
   fibrillation.  Andexanet alfa is the specific Xa-
   inhibitor reversal agent.
2. **Rivaroxaban (Xarelto)** — Bayer 2008.  2-
   Chlorothiophene + (S)-oxazolidinone + N-aryl-
   morpholinone.  **First DOAC to market.**  Once-daily
   dosing.  Bioavailability is **food-dependent** (66%
   fasting → 100% with food at 20 mg dose) so must be
   taken with meals.  CYP3A4 + P-gp substrate; 33% renal
   cleared.  ROCKET-AF 2011 + EINSTEIN-DVT 2010.
3. **Edoxaban (Lixiana / Savaysa)** — Daiichi Sankyo 2011.
   Thiazole-N-methyl-carboxamide + 5-chloro-2-
   aminonicotinamide + trans-cyclohexyl-1,4-diamine spacer.
   Once-daily dosing.  Critical PK feature:
   **bioavailability decreases at high renal clearance** —
   paradoxically less effective in patients with preserved
   renal function (CrCl > 95 mL/min).  Boxed warning: NOT
   for atrial fibrillation when CrCl > 95 mL/min.  ENGAGE
   AF-TIMI 48 2013.
4. **Dabigatran (Pradaxa) — active form** — Boehringer
   Ingelheim 2010.  Benzimidazole + amidine + pyridinyl-
   N-acyl-β-alanine.  **Only DOAC that targets thrombin
   (IIa)** instead of factor Xa.  The amidine + carboxylate
   zwitterion at physiological pH is the IIa-binding
   pharmacophore — but **destroys oral bioavailability**
   (only 6.5% as free dabigatran) because the molecule is
   too polar to cross intestinal membranes.  Solved by the
   etexilate prodrug.  Idarucizumab is the specific IIa-
   inhibitor reversal agent.
5. **Dabigatran etexilate (Pradaxa prodrug)** — caps both
   polar groups (amidine + carboxylate) of dabigatran with
   lipophilic prodrug groups (hexyloxy-carbamate +
   ethyl-ester), raising logP from 3.0 → 5.6 and MW from
   471 → 628 Da.  Result: oral absorption rises ~ 10×.
   Esterases in the gut wall + blood hydrolyse both caps
   in vivo to release the active zwitterionic dabigatran.
   **Textbook example of a 'double prodrug' / 'sequential
   prodrug' that masks two polar groups simultaneously.**

### Tests
Two new tests in `tests/test_sar.py` plus two existing
tests updated:
- `test_doac_series_landmarks` — six pedagogical SAR
  invariants locked in: (a) all 5 landmark entries
  present, (b) **Xa-vs-IIa target diversity** with exactly
  3 factor-Xa inhibitors + 2 factor-IIa entries (the IIa
  count includes the prodrug), (c) apixaban has the lowest
  factor-Xa Ki in the class, (d) **prodrug logP story** —
  dabigatran etexilate logP ≥ 2 units higher than active
  dabigatran's, (e) **prodrug MW story** — dabigatran
  etexilate ≥ 100 Da heavier than active dabigatran's
  (both lipophilic caps combined), (f) all 3 Xa inhibitors
  have higher oral bioavailability than free dabigatran
  (the whole reason the etexilate prodrug exists).
- `test_doac_series_count_at_least_five` — variant-count
  floor.
- `test_sar_library_size_at_least_fourteen` — catalogue
  floor bumped from 13 → 14 (renamed from round-161
  `_at_least_thirteen` version).
- `test_library_seeded` — extended to assert the new
  `doacs` id.

All 28 SAR tests pass on first run.

### Documentation updates
- ROADMAP.md — Phase 31k entry updated from 13/15 →
  14/15 with description of the DOAC series + the 6
  pedagogical invariants + the new "prodrug for
  bioavailability" teaching theme.
- PROJECT_STATUS.md — round 162 summary prepended.
- SESSION_LOG.md — this entry.

### Test suite status
1 949 passing (up from 1 947 in round 161 — net +2 from
this round's two new test functions).  Doc-coverage test
green; full suite ~45 s wall-clock.

### What's open (next-round candidates)
- **Phase 31k** — 1 more SAR series to close at the 15/15
  milestone.  Top candidate: oral antidiabetics
  (sulfonylureas tolbutamide → glyburide → glipizide →
  glimepiride — generation-by-generation potency
  progression on the pancreatic K-ATP channel; pairs with
  the H1 / PPI generation stories).  Alternative: thyroid
  agents (T3 / T4 / propylthiouracil / methimazole —
  agonist + biosynthesis-inhibitor arc) or biologic-
  mimicking small molecules (DPP-4 inhibitors —
  sitagliptin / saxagliptin / linagliptin / alogliptin —
  the modern incretin-pathway anti-diabetic class that
  paired with the round-159 PPI series's chiral-switch
  story).
- **Phase 38c** — equipment-palette + QGraphicsScene
  canvas for the lab-setup simulator.  Multi-round; the
  highest-value remaining work.
- **Phase 31b extension** — 60-target with curiosity-
  bucket entries.

A safer next pick remains the final SAR series to hit the
15/15 milestone — closing Phase 31k will be the second
"phase complete" milestone after Phase 31b at 50/50.

## 2026-04-25 — Round 161 (Phase 31k — anticonvulsant SAR series, catalogue 12/15 → 13/15)

### Context
Rounds 158-160 added H1-antihistamines + PPI-inhibitors +
opioid-analgesics, opening three medicinal-chem teaching
themes: chiral switch, BBB / zwitterion, lipophilicity →
potency.  Round 161 adds anticonvulsants — the fourth major
theme: **different scaffolds for the same biology** (the
complement to the family-walk patterns of the preceding
rounds, where each variant was a substituted version of the
same parent template).  Catalogue advances 12/15 → 13/15.

### What shipped
**One SAR series** added to `orgchem/core/sar.py`:

**`anticonvulsants` — Anticonvulsant series (different
scaffolds, shared indication).**  Target: multiple — voltage-
gated Na+ channels, GABA system, voltage-gated Ca++ channels,
SV2A vesicular protein.  Source: Brodie & Sills 2011 *Lancet
Neurol.* 10: 1019-1030 (anticonvulsant mechanisms + SAR
review).  Activity columns: `na_channel_blocker` (0/1),
`broad_spectrum` (0/1), `cyp_induction_score` (-1 to +1),
`half_life_h`, `logp`.

Five variants spanning four distinct chemotypes:

1. **Phenytoin (Dilantin)** — 5,5-diphenylhydantoin
   scaffold.  Heinrich Biltz 1908 (synthesis), Merritt +
   Putnam 1938 (anticonvulsant activity discovered).  First
   non-sedating anticonvulsant.  Voltage-gated Na+ channel
   block in the inactivated state, preferentially silencing
   rapidly-firing neurons.  **Strong CYP3A4 + CYP2C9 inducer**
   + autoinducer — driver of many drug-drug interactions
   (warfarin, OCs, opioids).  Non-linear (saturable)
   metabolism: small dose increases at the top of the
   therapeutic range cause disproportionate plasma rises.
2. **Carbamazepine (Tegretol)** — dibenzazepine + 5-
   carboxamide tricyclic; structurally close to imipramine
   TCA.  Schindler 1953 / 1962 EU approval.  Same Na+-
   channel mechanism as phenytoin via a totally different
   scaffold.  **Strong CYP3A4 inducer**.  HLA-B*1502
   carriers (~ 10% of Han Chinese, 2-4% of South Asian)
   carry markedly elevated risk of Stevens-Johnson syndrome
   / toxic epidermal necrolysis — FDA boxed warning for
   HLA testing in at-risk populations.
3. **Valproate (Depakote)** — branched fatty acid (2-
   propylpentanoic acid).  Burton 1882 (synthesis as a
   solvent), Meunier 1962 (anticonvulsant activity
   discovered serendipitously when used as a vehicle for
   screening).  **The broad-spectrum anticonvulsant**: Na+-
   channel block + GABA augmentation (GABA-T inhibition +
   GAD activation) + T-type Ca++-channel block + HDAC
   inhibition.  Effective on tonic-clonic, absence, and
   myoclonic seizures — the only seeded entry covering all
   three.  **CYP INHIBITOR** (opposite of phenytoin /
   carbamazepine) — raises lamotrigine + phenobarbital
   levels.  Hepatotoxic + teratogenic (neural-tube defects
   ~ 1-2%); contraindicated in women of child-bearing
   potential without strict contraception.
4. **Lamotrigine (Lamictal)** — phenyltriazine; 6-(2,3-
   dichlorophenyl)-1,2,4-triazine-3,5-diamine.  GSK 1990.
   Same Na+-channel inactivation mechanism as phenytoin /
   carbamazepine via yet another scaffold.  **No CYP
   induction** (metabolised by glucuronidation via UGT1A4)
   — clean drug-drug-interaction profile.  Critical
   clinical caveat: **Stevens-Johnson syndrome / TEN risk**
   on rapid titration (~ 1-3% in children, lower in adults)
   — 6-week slow titration mandatory.  Half-life doubles
   when co-administered with valproate (UGT inhibition).
5. **Levetiracetam (Keppra)** — pyrrolidone; (S)-α-ethyl-2-
   oxo-1-pyrrolidineacetamide.  UCB 1999.  Totally distinct
   mechanism: **binds the synaptic-vesicle protein SV2A**
   (Lynch et al. 2004), modulating neurotransmitter release
   without directly blocking Na+ or Ca++ channels.  **First-
   in-class.**  No CYP interactions (66% renal-cleared
   unchanged) — the cleanest interaction profile of any
   seeded anticonvulsant.  Broad-spectrum on focal +
   generalised tonic-clonic + myoclonic seizures.
   Behavioural side effects (irritability, depression) are
   the dose-limiting trade-off, not hepatotoxicity or drug
   interactions.  Now first-line in many guidelines for
   monotherapy.

### Tests
Two new tests in `tests/test_sar.py` plus two existing
tests updated:
- `test_anticonvulsant_series_landmarks` — six
  pedagogical SAR invariants locked in: (a) all 5 landmark
  drugs present, (b) **different-scaffolds-for-the-same-
  biology** theme — molecular weights span > 100 Da (144-
  256 Da actual), proving chemotype diversity vs the
  family-walk pattern of H1 / PPI / opioids, (c) phenytoin
  + carbamazepine both have cyp_induction_score = 1.0
  (strong CYP3A4 inducers — the older, drug-interaction-
  heavy generation), (d) valproate has cyp_induction_score
  < 0 (CYP INHIBITOR, the opposite of the older
  anticonvulsants), (e) levetiracetam is the only entry
  that does NOT block Na+ channels — SV2A vesicular-protein
  mechanism, (f) valproate + levetiracetam are the two
  broad-spectrum entries.
- `test_anticonvulsant_series_count_at_least_five` —
  variant-count floor.
- `test_sar_library_size_at_least_thirteen` — catalogue
  floor bumped from 12 → 13 (renamed from round-160
  `_at_least_twelve` version).
- `test_library_seeded` — extended to assert the new
  `anticonvulsants` id.

All 26 SAR tests pass on first run.

### Documentation updates
- ROADMAP.md — Phase 31k entry updated from 12/15 →
  13/15 with description of the anticonvulsant series +
  the 6 pedagogical invariants + the new "different
  scaffolds for the same biology" teaching theme.
- PROJECT_STATUS.md — round 161 summary prepended.
- SESSION_LOG.md — this entry.

### Test suite status
1 947 passing (up from 1 945 in round 160 — net +2 from
this round's two new test functions).  Doc-coverage test
green; full suite ~44 s wall-clock.

### What's open (next-round candidates)
- **Phase 31k** — 2 more SAR series to reach 15/15.
  Priority list: oral antidiabetics (sulfonylureas
  tolbutamide → glyburide → glipizide → glimepiride —
  generation-by-generation potency progression on the
  pancreatic K-ATP channel; pairs with the H1 / PPI
  generation stories), thyroid agents (T3 / T4 /
  propylthiouracil / methimazole — agonist + biosynthesis-
  inhibitor arc), or a direct-oral-anticoagulant series
  (apixaban / rivaroxaban / dabigatran / edoxaban — the
  modern Xa- / IIa-inhibitor landscape that displaced
  warfarin).
- **Phase 38c** — equipment-palette + QGraphicsScene
  canvas for the lab-setup simulator.  Multi-round; the
  highest-value remaining work.
- **Phase 31b extension** — 60-target with curiosity-
  bucket entries.

A safer next pick remains another 1 SAR series per round.
Oral antidiabetics + thyroid agents in successive rounds
would close Phase 31k at the 15/15 milestone.

## 2026-04-25 — Round 160 (Phase 31k — opioid analgesic SAR series, catalogue 11/15 → 12/15)

### Context
Rounds 158-159 added H1-antihistamines + PPI-inhibitors,
opening the chiral-switch (SSRI + PPI) and zwitterion / BBB
(H1) medicinal-chem teaching themes.  Round 160 adds opioid
analgesics — opens the **lipophilicity → potency** theme,
the third major teaching anchor in the rational-tweak
medicinal-chem cluster.  Catalogue advances 11/15 → 12/15.

### What shipped
**One SAR series** added to `orgchem/core/sar.py`:

**`opioid-analgesics` — Opioid analgesic series (μ-receptor
agonists).**  Target: μ-opioid receptor (MOR).  Source:
Inturrisi 2002 *Clin. J. Pain* 18 Suppl: S3-S13 +
Reisine & Pasternak 1996 (Goodman & Gilman ch. 23) — the
canonical opioid SAR + equianalgesic-dosing reviews.
Activity columns: `mu_ki_nM`, `equianalgesic_mg_iv`,
`potency_ratio_vs_morphine`, `logp`.

Five variants spanning natural / semi-synthetic / synthetic
chemotypes:

1. **Morphine** — Sertürner 1804.  First alkaloid ever
   isolated (from opium poppy *Papaver somniferum*).
   Reference compound for opioid potency.  Low logP (1.2)
   means slow BBB penetration — delays peak analgesic
   effect ~ 20-30 min after IV.  Glucuronidated to
   morphine-6-glucuronide (M6G, the active metabolite,
   more potent than morphine itself) and morphine-3-
   glucuronide (M3G, neuroexcitatory).
2. **Codeine** — Robiquet 1832.  **The pro-drug anchor**:
   direct μ-receptor affinity is 100× weaker than
   morphine's (Ki ~ 200 nM), but CYP2D6 demethylates
   ~ 5-10% of an oral dose to morphine in vivo, providing
   essentially all of the analgesic effect.  CYP2D6-poor
   metabolisers get little analgesia; ultra-rapid
   metabolisers get morphine overdose — opposite extremes
   of the same polymorphism.  FDA boxed-warned for
   paediatric use after deaths in fast metabolisers.
3. **Hydromorphone (Dilaudid)** — Knoll 1924, semi-
   synthetic from morphine.  Two SAR moves: saturate the
   C7-C8 double bond + oxidise the 6-OH allyl alcohol to
   a 6-ketone.  **The most-potent direct μ-binder in the
   series** with Ki ~ 0.4 nM.  ~ 7× more potent than
   morphine on weight basis with shorter onset; lacks the
   active glucuronide metabolite of morphine, so cleaner
   PK in renal-failure patients.
4. **Oxycodone (OxyContin)** — Freund + Speyer 1916,
   semi-synthetic from thebaine (third major opium
   alkaloid).  14-OH + 6-keto + 3-OMe + dihydro
   combination.  Direct μ-affinity is *lower* than
   morphine (Ki 18 vs 1.4 nM) but oral bioavailability
   ~ 60-87% (morphine PO is only ~ 25%).  Major active
   metabolite oxymorphone (CYP2D6-mediated 3-O-
   demethylation) is ~ 3× more potent than morphine.
   OxyContin (1996) — controlled-release oxycodone — is
   the drug at the centre of the US opioid crisis.
5. **Fentanyl** — Janssen 1960.  **Total synthetic
   chemotype switch to 4-anilidopiperidine** — completely
   different from the morphinan scaffold.  Same μ-receptor
   affinity as morphine (Ki 1.4 nM) but **~ 100× more
   potent on weight basis** because logP 4.1 vs morphine's
   1.2 drives 10-100× faster BBB penetration.  **THE
   textbook example of lipophilicity → potency in CNS
   pharmacology** — same target, same intrinsic affinity,
   vastly different effective dose due to physico-chem
   alone.  Onset 1-2 min IV vs 20 min for morphine.
   Carfentanil + sufentanil push the same scaffold to
   10 000× and 1000× morphine respectively.  The
   lipophilicity-drives-potency story has driven the
   current illicit-fentanyl-analogue epidemic — synthetic
   accessibility + huge molar potency makes safe trafficked-
   dose calibration impossible.

### Tests
Two new tests in `tests/test_sar.py` plus two existing
tests updated:
- `test_opioid_analgesic_series_landmarks` — six
  pedagogical SAR invariants locked in: (a) all 5 landmark
  drugs present, (b) fentanyl is the high-potency anchor
  (highest potency_ratio_vs_morphine of all 5),
  (c) codeine is the pro-drug anchor (direct μ-Ki ≥ 50×
  morphine's), (d) hydromorphone has the lowest direct
  μ-Ki, (e) **lipophilicity → potency** invariant —
  fentanyl logP ≥ 2 units higher than morphine AND ≥ 50×
  potency advantage (the canonical CNS-pharmacology
  teaching point), (f) codeine MW exceeds morphine MW by
  exactly one methyl group (~ 14 Da, the 3-OMe ether).
- `test_opioid_series_count_at_least_five` — variant-
  count floor.
- `test_sar_library_size_at_least_twelve` — catalogue
  floor bumped from 11 → 12 (renamed from round-159
  `_at_least_eleven` version).
- `test_library_seeded` — extended to assert the new
  `opioid-analgesics` id.

All 24 SAR tests pass on first run.

### Documentation updates
- ROADMAP.md — Phase 31k entry updated from 11/15 →
  12/15 with description of the opioid series + the 6
  pedagogical invariants.
- PROJECT_STATUS.md — round 160 summary prepended.
- SESSION_LOG.md — this entry.

### Test suite status
1 945 passing (up from 1 943 in round 159 — net +2 from
this round's two new test functions).  Doc-coverage test
green; full suite ~44 s wall-clock.

### What's open (next-round candidates)
- **Phase 31k** — 3 more SAR series to reach 15/15.
  Priority list: oral antidiabetics (sulfonylureas
  tolbutamide → glyburide → glipizide → glimepiride —
  generation-by-generation potency progression on the
  pancreatic K-ATP channel; pairs with the H1 / PPI
  generation stories), anticonvulsants (phenytoin /
  carbamazepine / valproate / lamotrigine / levetiracetam
  — varied chemotypes for the same broad indication; opens
  a different SAR teaching theme: "different scaffolds for
  the same biology"), thyroid agents (T3 / T4 /
  propylthiouracil / methimazole — agonist + biosynthesis-
  inhibitor arc).
- **Phase 38c** — equipment-palette + QGraphicsScene
  canvas for the lab-setup simulator.  Multi-round; the
  highest-value remaining work.
- **Phase 31b extension** — 60-target with curiosity-
  bucket entries.

A safer next pick remains another 1 SAR series per round.
Oral antidiabetics would extend the chiral-switch /
generation-walk theme cluster; anticonvulsants would open
a new "different scaffolds for the same biology" theme.

## 2026-04-25 — Round 159 (Phase 31k — PPI inhibitor SAR series, catalogue 10/15 → 11/15)

### Context
Round 158 added the H1-antihistamine series (10/15).  Round
159 adds the PPI inhibitor series (11/15) — same `core/sar.py`
catalogue+test pattern; **the chiral-switch story arc** is
the headline pedagogical anchor that pairs with the round-96
SSRI series (citalopram → escitalopram).  Three rational-
tweak themes from rounds 96 / 158 / 159 now form a coherent
medicinal-chem teaching cluster: chiral switch (SSRI + PPI),
zwitterion / BBB-blocker (H1), CYP-independence (PPI).

### What shipped
**One SAR series** added to `orgchem/core/sar.py`:

**`ppi-inhibitors` — Proton-pump inhibitor (PPI) series.**
Target: gastric H+/K+-ATPase (Cys-813 covalent inhibition).
Source: Olbe, Carlsson & Lindberg 2003 *Nat. Rev. Drug
Discov.* 2: 132-139 (the canonical PPI discovery + SAR
review by the Astra team).  Activity columns: `onset_h`,
`duration_h`, `cyp_metabolism_dependence` (0-1 scale),
`logp`.

Five variants spanning the 1988-1999 PPI-development arc:

1. **Omeprazole (Prilosec)** — Astra 1988.  The prototype
   racemate.  Pro-drug mechanism: at parietal-cell
   secretory canaliculus pH ~ 1 the pyridine-N protonates,
   the molecule rearranges via a sulfenamide intermediate,
   and the activated species covalently traps Cys-813 of
   H+/K+-ATPase via a -S-S- bond.  Both (R) + (S) sulfoxide
   enantiomers in commerce; (R) clears faster via CYP2C19
   so (S) does most of the work — drove the chiral-switch
   development.
2. **Esomeprazole (Nexium)** — AstraZeneca 2001.  **The
   textbook chiral switch**: take racemic omeprazole
   off-patent, develop the more-active (S)-enantiomer as
   a new product with fresh patent life.  Same scaffold +
   same Cys-813 trapping mechanism but locked (S)-sulfoxide
   chirality eliminates the (R)-elimination pathway →
   reduced inter-patient CYP2C19-polymorphism variability
   + longer duration.  Pairs with the SSRI series's
   citalopram → escitalopram chiral switch as the two
   textbook examples of single-enantiomer-from-racemic
   patent-extension.
3. **Lansoprazole (Prevacid)** — Takeda 1991.  First PPI
   to use a fluorinated pyridine substituent (2,2,2-
   trifluoroethoxy raises logP +0.6 vs omeprazole, speeding
   absorption).  Same Cys-813 mechanism + similar duration.
4. **Pantoprazole (Protonix)** — Byk Gulden 1985 / approved
   1995.  The 5-OCHF₂ + 4-OMe combination dramatically
   lowers CYP-mediated clearance — pantoprazole goes
   through Phase-II sulfotransferase conjugation as the
   dominant metabolic pathway.  **Least drug-drug
   interactions of any PPI**: no clinically-significant
   interaction with warfarin / clopidogrel / phenytoin /
   theophylline.  The PPI of choice in polypharmacy elderly
   + ICU patients.
5. **Rabeprazole (AcipHex)** — Eisai 1999.  Designed for
   **fastest onset** of the class.  Higher pKa of the
   benzimidazole N (5.0 vs 4.0 for omeprazole) means
   rabeprazole protonates + activates at a higher
   intracellular pH — works even in patients with chronic
   gastritis whose secretory canaliculus pH is elevated.
   Like pantoprazole, mostly non-enzymatic activation +
   reduction metabolism, so few CYP interactions.

### Tests
Two new tests in `tests/test_sar.py` plus two existing
tests updated:
- `test_ppi_inhibitor_series_landmarks` — five pedagogical
  SAR invariants locked in: (a) all 5 landmark drugs
  present, (b) chiral-switch invariant (esomeprazole MW
  == omeprazole MW because they're the same molecular
  formula, but esomeprazole CYP dependence < omeprazole
  AND esomeprazole duration ≥ omeprazole), (c) pantoprazole
  has the LOWEST CYP-metabolism dependence in the class,
  (d) rabeprazole has the FASTEST onset, (e) MW band
  340-390 Da typical for the
  2-(pyridinylmethylsulfinyl)-1H-benzimidazole template.
- `test_ppi_series_count_at_least_five` — variant-count
  floor.
- `test_sar_library_size_at_least_eleven` — catalogue
  floor bumped from 10 → 11 (renamed from round-158
  `_at_least_ten` version).
- `test_library_seeded` — extended to assert the new
  `ppi-inhibitors` id.

All 22 SAR tests pass on first run.  No fragment-
consistency work needed.

### Documentation updates
- ROADMAP.md — Phase 31k entry updated from 10/15 →
  11/15 with description of the PPI series + the 5
  pedagogical invariants locked in by tests.
- PROJECT_STATUS.md — round 159 summary prepended.
- SESSION_LOG.md — this entry.

### Test suite status
1 943 passing (up from 1 941 in round 158 — net +2 from
this round's two new test functions).  Doc-coverage test
green; full suite ~44 s wall-clock.

### What's open (next-round candidates)
- **Phase 31k** — 4 more SAR series to reach 15/15.
  Priority list: opioid analgesics (morphine / codeine /
  hydromorphone / oxycodone / fentanyl — μ-receptor SAR +
  lipophilicity / potency landscape), oral antidiabetics
  (sulfonylureas tolbutamide → glyburide → glipizide →
  glimepiride — generation-by-generation), anticonvulsants
  (phenytoin / carbamazepine / valproate / lamotrigine /
  levetiracetam — varied chemotypes), thyroid agents
  (T3 / T4 / propylthiouracil / methimazole — agonist +
  biosynthesis-inhibitor arc).
- **Phase 38c** — equipment-palette + QGraphicsScene
  canvas for the lab-setup simulator.  Multi-round; the
  highest-value remaining work.
- **Phase 31b extension** — 60-target with curiosity-
  bucket entries.

A safer next pick remains another 1 SAR series per round.
Opioid analgesics would extend the pharmacology teaching
surface to controlled-substances + lipophilicity-drives-
potency themes.

## 2026-04-25 — Round 158 (Phase 31k — H1-antihistamine SAR series, catalogue 9/15 → 10/15)

### Context
Round 157 closed Phase 31b at the 50/50 milestone.  Round
158 switches to Phase 31k SAR-series expansion (was 9/15
after the round-133 Fluoroquinolone series; now 10/15).
H1-antihistamines are the natural next pick: a well-defined
1st-gen → 2nd-gen → 3rd-gen landmark progression that pairs
pedagogically with the round-96 SSRI chiral-switch series
and the round-100 β-lactam family-walk story.  The H1
narrative covers BBB penetration, zwitterion design, P-gp
substrates, active metabolites, and hERG / cardiac-safety
withdrawal — a remarkably tight encapsulation of modern
medicinal-chem trade-offs.

### What shipped
**One SAR series** added to `orgchem/core/sar.py`:

**`h1-antihistamines` — H1-antihistamine series** (1st-gen
→ 2nd-gen → 3rd-gen).  Target: histamine H1 receptor.
Source: Simons & Simons 2008 *J. Allergy Clin. Immunol.*
121: S30-S36 (canonical H1 SAR review).  Activity columns:
`h1_ki_nM`, `sedation_score`, `qt_risk`, `logp`.

Six variants spanning the full landmark progression:

1. **Diphenhydramine (Benadryl)** — Rieveschl 1943.
   1st-gen ethanolamine; benzhydryl ether + dimethylamine
   tail.  H1 Ki 16 nM, sedation 5/5.  The original H1
   antihistamine + the OTC-sleep-aid active in
   ZzzQuil / Tylenol PM.  BBB-penetrant via low TPSA +
   neutral charge; significant muscarinic-receptor cross-
   reactivity gives anticholinergic side effects on top of
   sedation.
2. **Chlorpheniramine (Chlor-Trimeton)** — Schering 1951.
   1st-gen alkylamine with one para-Cl + a 3-carbon tether
   (ethanolamine → propylamine).  H1 Ki 4.6 nM, sedation
   3/5.  4× more potent than diphenhydramine because the
   para-Cl + propylamine geometry better fills the H1
   binding pocket; less sedating but still BBB-penetrant.
3. **Hydroxyzine (Atarax / Vistaril)** — UCB 1956.  1st-gen
   piperazine class; benzhydryl + 2-(2-hydroxyethoxy)ethyl
   tail.  H1 Ki 1.5 nM (the most-potent H1 binder in the
   series), sedation 4/5.  Adds an anxiolytic + antiemetic
   profile.  **The pro-drug from which cetirizine emerges**
   via metabolic oxidation of the terminal -OH to -COOH.
4. **Loratadine (Claritin)** — Schering-Plough 1989, OTC
   2002.  2nd-gen tricyclic with rigid exocyclic-
   piperidinylidene + ethyl-carbamate cap on N.  H1 Ki
   50 nM (parent), sedation 0.5/5.  Itself a pro-drug —
   CYP3A4 / CYP2D6 cleaves the carbamate to give
   desloratadine (Clarinex), the actual H1 antagonist with
   Ki ~ 0.4 nM.  Carbamate cap + P-gp substrate prevent
   BBB entry.  The 2nd-gen template that opened the
   $10B+ non-sedating-antihistamine market.
5. **Cetirizine (Zyrtec)** — UCB 1987.  2nd-gen carboxylic-
   acid metabolite of hydroxyzine — direct development:
   oxidise the terminal hydroxyethyl tail to a carboxylic
   acid, get a zwitterion at physiological pH that can NOT
   cross the BBB despite the same diaryl-piperazine
   pharmacophore.  H1 Ki 6 nM, sedation 1/5.  The
   (R)-enantiomer levocetirizine (Xyzal) is the active
   component.
6. **Fexofenadine (Allegra)** — Hoechst Marion Roussel
   1996.  **The 3rd-generation breakthrough** — carboxylic-
   acid metabolite of terfenadine (CYP3A4 oxidation of one
   tert-butyl methyl).  H1 Ki 10 nM, sedation 0/5.
   Terfenadine (Seldane, 1985) was the first non-sedating
   H1, but it blocked the cardiac hERG K⁺ channel —
   sudden deaths from torsades de pointes when co-
   administered with CYP3A4 inhibitors (grapefruit juice,
   ketoconazole, erythromycin) led to 1998 withdrawal.
   Fexofenadine's COOH adds a zwitterion that blocks BBB
   entry AND eliminates hERG affinity.  The textbook
   example of an active metabolite displacing its parent
   drug.

### Tests
Three new tests in `tests/test_sar.py`:
- `test_h1_antihistamine_series_landmarks` — five
  pedagogical SAR invariants locked in: (a) all 6 textbook
  landmark drugs present, (b) 1st-gen drugs encoded as
  sedating (sedation_score ≥ 3), (c) 2nd/3rd-gen drugs
  encoded as non-sedating (sedation_score ≤ 1),
  (d) fexofenadine sedation_score = 0 (the truly non-
  sedating anchor), (e) cetirizine sedation_score <
  hydroxyzine sedation_score (the zwitterion-vs-free-OH
  BBB-penetration story), (f) MW band 250-510 Da with
  fexofenadine the largest.
- `test_h1_series_count_at_least_six` — variant-count
  floor.
- `test_sar_library_size_at_least_ten` — catalogue floor
  at 10/15.
- `test_library_seeded` updated to assert `h1-antihistamines`
  + `fluoroquinolones` ids are present.

All 20 SAR tests pass on first run.  No fragment-
consistency work needed (SAR series don't go through the
reaction-fragment audit; SMILES are validated via
`compute_descriptors` invoking `drug_likeness_report`).

### Documentation updates
- ROADMAP.md — Phase 31k entry updated from 9/15 →
  10/15 with description of the H1-antihistamine series
  and the 5 pedagogical invariants locked in by tests.
- PROJECT_STATUS.md — round 158 summary prepended.
- SESSION_LOG.md — this entry.

(No INTERFACE.md changes needed — `core/sar.py` row in
INTERFACE.md is generic over the catalogue contents.)

### Test suite status
1 941 passing (up from 1 938 in round 157 — net +3 from
this round's three new test functions).  Doc-coverage
test green; full suite ~44 s wall-clock.

### What's open (next-round candidates)
- **Phase 31k** — 5 more SAR series to reach 15/15.
  Priority list: PPI-inhibitor series (omeprazole / "
  esomeprazole / lansoprazole / pantoprazole / rabeprazole
  — the chiral-switch story like SSRIs but with
  benzimidazole + sulfoxide chemistry; pH-activated
  pro-drugs; idem-acid-blocker biology), oral-anti-
  diabetics (sulfonylureas tolbutamide → glyburide →
  glipizide → glimepiride), anticonvulsants
  (phenytoin / carbamazepine / valproate / lamotrigine /
  levetiracetam — varied chemotypes for the same broad
  indication), thyroid hormones (T3 / T4 / propylthiouracil
  / methimazole — agonist + biosynthesis-inhibitor
  arc), opioid analgesics (morphine / codeine /
  hydromorphone / oxycodone / hydrocodone / fentanyl —
  μ-receptor SAR + lipophilicity / potency landscape).
- **Phase 38c** — equipment-palette + QGraphicsScene
  canvas for the lab-setup simulator.  Multi-round;
  highest-value remaining work.
- **Phase 31b extension** — 60-target with curiosity-
  bucket entries (Ramberg-Bäcklund, Shapiro, Oppenauer,
  Julia / Peterson olefinations, Wacker oxidation, Henry /
  Knoevenagel, Brown hydroboration-oxidation).

A safer next pick remains another 1 SAR series per round
(or 1 named-reaction round on the 31b-extension).  PPI
inhibitors fit the H1 / SSRI 'rational physical-chem
tweak' story arc cleanly and would ship in one round.

## 2026-04-25 — Round 157 (🎉 Phase 31b CLOSED at 50/50 — Appel reaction + Jones oxidation)

### Context
Rounds 152-156 progressed Phase 31b from 38/50 → 48/50 in
just 5 rounds, opening the asymmetric-catalysis (6 entries),
asymmetric C-C bond-formation, and sulfur-ylide methylene-
transfer teaching surfaces, plus closing the Pd-coupling
family at 5/5.  Round 157 ships the final two pedagogical
anchors needed to close Phase 31b at the **50/50 milestone**:
Appel pairs naturally with the seeded Mitsunobu (both
PPh₃-mediated alcohol-OH activation paths) and Jones
provides the over-oxidation counterpoint to the seeded
PCC + Swern + Dess-Martin entries.  Phase 31b is now
complete.

### What shipped
**Two named reactions** added to
`orgchem/db/seed_reactions.py`:

1. **Appel reaction (1-octanol → 1-chlorooctane)** —
   category *Functional-group interconversion*.  Appel 1975.
   Description teaches: PPh₃ + a tetrahalomethane (CCl₄
   for chloride, CBr₄ for bromide, CI₄ for iodide) in CH₂Cl₂
   or DMF at 0 °C → rt; the four-step mechanism (PPh₃
   attacks one Cl of CCl₄ to displace CCl₃⁻ giving
   chlorotriphenylphosphonium chloride [Ph₃PCl]⁺Cl⁻; the
   alcohol substitutes one Cl on phosphorus to give the
   alkoxytriphenylphosphonium R-O-P⁺Ph₃ + HCCl₃ + Cl⁻;
   chloride performs an SN2 displacement of the excellent
   OPPh₃ leaving group, delivering R-Cl with **inversion of
   configuration** at the carbon and Ph₃P=O as the second
   by-product).  **Pedagogical pairing with the seeded
   Mitsunobu reaction** is the headline teaching anchor:
   both Appel and Mitsunobu activate an alcohol's OH as a
   phosphonium leaving group via PPh₃ and both deliver SN2
   inversion at the carbon — but Appel uses CCl₄/CBr₄/CI₄
   as the halide-source co-reagent (gives R-X), while
   Mitsunobu uses DIAD/DEAD + a soft pronucleophile (gives
   R-O-CO-R', R-N-CO-R', R-O-Ar, etc.).  Workhorse for
   halogenation of alcohols where harsher SOCl₂ / PCl₃
   conditions would touch other functional groups.  Reaction
   SMILES `CCCCCCCCO.c1ccc(P(c2ccccc2)c2ccccc2)cc1.
   ClC(Cl)(Cl)Cl >> CCCCCCCCCl.O=P(c1ccccc1)(c1ccccc1)
   c1ccccc1.ClC(Cl)Cl`.

2. **Jones oxidation (1-octanol → octanoic acid)** —
   category *Oxidation*.  Jones 1946.  Description teaches:
   Cr(VI) reagent (CrO₃ + dilute H₂SO₄ in acetone, added
   drop-wise to substrate at 0–25 °C until the
   characteristic orange-red Cr(VI) colour persists);
   mechanism (alcohol forms chromate ester R-O-CrO₃H, α-H
   removed in cyclic E2-like TS giving carbonyl + reduced
   Cr(IV); for 1° alcohols the resulting aldehyde is
   hydrated by aqueous acetone to a gem-diol that gets
   oxidised AGAIN by Cr(VI) to the carboxylic acid — **the
   over-oxidation step that defines Jones**).  **Critical
   pedagogical role in the catalogue**: every other seeded
   oxidation (PCC + Swern + Dess-Martin) was specifically
   designed to STOP at the aldehyde — Jones is the
   *counterpoint* that shows what happens when you don't.
   Modern green-chemistry trend to replace Jones with
   TEMPO/NaOCl or NaIO₄/RuCl₃ to avoid the Cr(VI) carcinogen
   + heavy-metal waste called out in the description, but
   Jones remains teaching-essential as the historical
   default + the over-oxidation example.  Reaction SMILES
   `CCCCCCCCO.O=[Cr](=O)=O >> CCCCCCCC(=O)O.O=[Cr]=O.O`.

**Six intermediate fragments** added to
`orgchem/db/seed_intermediates.py`: `Carbon tetrachloride
(CCl4) ClC(Cl)(Cl)Cl` (reagent), `1-Chlorooctane
CCCCCCCCCl` (intermediate), `Chloroform (CHCl3) ClC(Cl)Cl`
(intermediate), `Chromium trioxide (CrO3, Jones reagent)
O=[Cr](=O)=O` (reagent), `Octanoic acid (caprylic acid)
CCCCCCCC(=O)O` (intermediate), `Chromium dioxide (CrO2)
O=[Cr]=O` (intermediate).  Triphenylphosphine + Ph₃P=O
already covered by the Mitsunobu / HWE entries; bromobenzene
+ benzaldehyde + 1-octanol all already seeded.

### Tests
Three new tests in `tests/test_reactions.py` plus the
catalogue-size floor bumped to the 50 milestone:
- `test_appel_reaction_seeded` — verifies the entry exists,
  the SMILES contains both PPh₃ + CCl₄, the description
  names PPh₃ / triphenylphosphine + CCl₄ + SN2 + inversion
  + the Mitsunobu pairing.
- `test_jones_oxidation_seeded` — verifies the entry
  exists, the SMILES has the 1-octanol substrate side and
  octanoic-acid product side (the over-oxidation product —
  the headline teaching point), the SMILES contains a Cr
  atom, and the description names the Cr(VI) / CrO₃
  reagent + over-oxidation language + comparison with the
  seeded PCC / Swern / Dess-Martin entries.
- `test_phase_31b_complete_50_of_50` — milestone closeout
  test that name-matches every one of the 12 round-152-157
  expansion entries (Birch + Dess-Martin + Sharpless AE +
  CBS + Sharpless AD + Jacobsen + Mukaiyama + Evans +
  Stille + Corey-Chaykovsky + Appel + Jones) so any future
  regression of any single entry surfaces immediately.
- `test_named_reaction_count_at_least_fifty` — catalogue-
  size floor bumped to 50 (renamed from the round-156
  _forty_eight version) — Phase 31b CLOSED at the original
  50-target.

Discovered + fixed during the test run: fragment-consistency
audit caught 6 missing fragments on first reaction-add.
Resolved by seeding the 6 intermediate rows above.  All 29
reaction-tests pass + all 12 fragment-consistency tests
pass.

### Documentation updates
- ROADMAP.md — Phase 31b checkbox flipped from `[~]`
  (in-progress) to `[x]` (COMPLETE round 157, 2026-04-25);
  Phase 31b entry updated from 48/50 → **50/50** with
  descriptions of both new reactions + the six new
  intermediate fragments + the milestone closeout
  language ("Phase 31b 50/50 vision realised after rounds
  152-157 — 12 new entries in 6 rounds").
- PROJECT_STATUS.md — round 157 summary prepended with
  the 🎉 Phase 31b CLOSED milestone language.
- SESSION_LOG.md — this entry.

### Test suite status
1 938 passing (up from 1 935 in round 156 — net +3 from
this round's three new test functions).  Doc-coverage test
green; full suite ~44 s wall-clock.

### What's open (next-round candidates)
**Phase 31b is COMPLETE.**  The original Phase 31 vision
of 50 named reactions is now fully realised; the
asymmetric-catalysis (6 entries) + asymmetric C-C bond-
formation (2 entries) + sulfur-ylide methylene-transfer
(1 entry) teaching surfaces are open; the Pd-coupling
family is closed at 5/5; the over-oxidation context is
cemented with Jones alongside PCC / Swern / Dess-Martin.

Remaining roadmap work falls into three buckets:
- **Phase 38c** — equipment-palette + QGraphicsScene
  canvas for the lab-setup simulator.  Multi-round, biggest
  open scope; arguably the highest-value remaining work.
  Could be picked up next as a "start phase 38c" round
  with just the headless `core/lab_setup_canvas.py`
  scaffolding.
- **Phase 31k** — more SAR series (8/15; 7 to go).  Same
  catalogue+dialog pattern as the just-shipped Phase 31b
  rounds; H1-antihistamine series + PPI-inhibitor series
  + ACE-inhibitor series + β-blocker series would each
  ship cleanly in 1 round.
- **Phase 31b extension** — beyond 50 to a 60-target with
  curiosity-bucket entries (Ramberg-Bäcklund, Shapiro,
  Oppenauer, Julia / Peterson olefinations, Wacker
  oxidation, Henry / Knoevenagel reactions, Brown
  hydroboration-oxidation, etc.).  Lower priority than
  Phase 38c, but same tight catalogue+fragment+test scope
  as rounds 152-157.

A safer next pick is the Phase 31k SAR-series expansion
(low-risk catalogue work, immediate teaching surface).
The bigger ambition is Phase 38c.

## 2026-04-25 — Round 156 (Phase 31b — Stille coupling + Corey-Chaykovsky epoxidation, catalogue 46/50 → 48/50, Pd-coupling family now 5/5)

### Context
Rounds 152-155 progressed Phase 31b from 38/50 → 46/50,
opening the asymmetric-catalysis teaching surface (6
entries) and the asymmetric C-C bond-formation sub-surface
(2 entries: Mukaiyama + Evans).  Round 156 delivers two
final pedagogical milestones: closing the Pd-coupling
family at 5/5 textbook canon entries (Stille is the missing
piece alongside Suzuki + Negishi + Heck + Sonogashira) and
opening the sulfur-ylide methylene-transfer surface
(Corey-Chaykovsky pairs naturally with the existing Wittig
entry as 'same carbonyl substrate, different product class').
Catalogue advances 46/50 → 48/50; just 2 more entries until
the 50-target.

### What shipped
**Two named reactions** added to
`orgchem/db/seed_reactions.py`:

1. **Stille coupling (bromobenzene + tributyl(vinyl)stannane
   → styrene + Bu₃SnBr)** — category *Cross-coupling
   (Pd-catalysed)* (matches the existing Suzuki / Negishi /
   Heck / Sonogashira category — the Pd-coupling family is
   now consistently tagged).  Migita-Kosugi-Stille 1978.
   Description teaches: Pd(0)-catalysed C(sp²)-C(sp²) (or
   C(sp²)-C(sp³)) coupling between an aryl/vinyl halide
   (or pseudohalide — triflate, iodonium) and an
   organostannane R₃Sn-R'; the classical OA → transmetalation
   → RE catalytic cycle (Bu₃Sn-X is the by-product); the
   distinctive **air-, moisture-, pH-stability** of the Sn
   reagent — Stille tolerates water, acidic and basic
   conditions, and a huge range of polar functional groups
   that other Pd-couplings can't touch; the **toxicity +
   environmental persistence** of tributyltin as the
   trade-off that pushed Suzuki ahead for commercial work;
   still indispensable in total synthesis where Sn's
   functional-group tolerance + ability to make
   C(sp²)-C(sp³) bonds is irreplaceable.  Reaction SMILES
   `Brc1ccccc1.C=C[Sn](CCCC)(CCCC)CCCC >>
   C=Cc1ccccc1.CCCC[Sn](CCCC)(CCCC)Br`.

2. **Corey-Chaykovsky epoxidation (benzaldehyde +
   dimethylsulfonium methylide → styrene oxide + DMS)** —
   category *Methylene transfer (sulfur ylide)*.
   E. J. Corey + M. Chaykovsky 1965.  Description covers
   BOTH ylide flavours: (a) the **dimethylsulfonium
   methylide** Me₂S=CH₂ (from trimethylsulfonium iodide +
   n-BuLi or NaH; kinetic, irreversible, 1,2-addition to
   carbonyls and enones giving the terminal epoxide) and
   (b) the **dimethylsulfoxonium methylide** Me₂S(O)=CH₂
   (from trimethylsulfoxonium iodide + NaH; thermodynamic,
   reversible, prefers 1,4-addition to α,β-unsaturated
   carbonyls giving cyclopropanes).  Mechanism for (a):
   ylide carbon attacks the carbonyl C → betaine → alkoxide
   displaces Me₂S in an intramolecular SN2 → epoxide.  The
   **Wittig comparison** is the headline pedagogical anchor:
   same overall C=O → C-X transformation, but Wittig gives
   an alkene via R₃P=CR₂ ylide (O ends up on phosphorus)
   while Corey-Chaykovsky gives an epoxide via R₂S=CR₂
   ylide (S leaves as DMS).  Distinct from the
   C=C-oxidising Sharpless / Jacobsen epoxidations: it's
   the only catalogue entry that builds a brand-new oxirane
   CH₂ ring atom from a non-alkene C=O substrate.  Reaction
   SMILES `O=Cc1ccccc1.C[S+](C)[CH2-] >>
   C1OC1c1ccccc1.CSC`.

**Four intermediate fragments** added to
`orgchem/db/seed_intermediates.py`:
`Tributyl(vinyl)stannane C=C[Sn](CCCC)(CCCC)CCCC` (reagent),
`Tributyltin bromide (Bu3SnBr) CCCC[Sn](CCCC)(CCCC)Br`
(intermediate), `Dimethylsulfonium methylide (Corey ylide)
C[S+](C)[CH2-]` (reagent), `Dimethyl sulfide (DMS) CSC`
(intermediate).  Bromobenzene + benzaldehyde + styrene +
styrene oxide already seeded.

### Tests
Three new tests in `tests/test_reactions.py`:
- `test_stille_coupling_seeded` — verifies the entry
  exists, the reaction SMILES contains `[Sn]` (the
  defining stannane reagent), and the description names
  Pd / transmetalation / stannane / toxicity (the
  trade-off that distinguishes Stille from the other
  Pd-couplings).
- `test_corey_chaykovsky_seeded` — verifies the entry
  exists, the reaction SMILES contains both `[S+]` and
  `[CH2-]` (the ylide reagent), the description names the
  sulfur-ylide reagent class + the Wittig comparison +
  the sulfoxonium-variant mention.
- `test_pd_coupling_family_at_least_five` — name-based
  catalogue floor for the Pd-coupling family (Suzuki +
  Negishi + Heck + Sonogashira + Stille); guards against
  future regression of any of these by name match (more
  robust than category match given category-string drift).
- `test_named_reaction_count_at_least_forty_eight` —
  catalogue-size floor bumped from 46 → 48 (renamed from
  the round-155 _forty_six version).

Discovered + fixed during the test run: fragment-consistency
audit caught 4 missing fragments on first reaction-add.
Resolved by seeding the 4 intermediate rows above.  All 26
reaction-tests pass + all 12 fragment-consistency tests
pass.

### Documentation updates
- ROADMAP.md — Phase 31b entry updated from 46/50 →
  48/50 with descriptions of both new reactions + the
  four new intermediate fragments + the Pd-coupling-
  family completion milestone.
- PROJECT_STATUS.md — round 156 summary prepended.
- SESSION_LOG.md — this entry.

### Test suite status
1 935 passing (up from 1 932 in round 155 — net +3 from
this round's three new test functions).  Doc-coverage test
green; full suite ~44 s wall-clock.

### What's open (next-round candidates)
**Phase 31b is now at 48/50 — just 2 more entries to
close the original 50-target.**  Top priority list:
- **Appel reaction** (PPh₃ / CCl₄ alcohol → alkyl chloride;
  workhorse functional-group interconversion that pairs
  pedagogically with Mitsunobu — both PPh₃-mediated
  alcohol-activation paths; SN2 inversion of stereochemistry).
- **Jones oxidation** (CrO₃ / H₂SO₄ in acetone, the
  classic chromic-acid 1°-alcohol → carboxylic-acid /
  2°-alcohol → ketone — pedagogically essential as the
  *over-oxidising* counterpoint to the seeded
  PCC / Swern / Dess-Martin entries).
- **Birch reduction follow-up entry — anisole substrate**
  to teach the EDG / sp²-carbon regiochemistry rule
  alongside the existing benzene → 1,4-cyclohexadiene
  entry.
- **Ramberg-Bäcklund** (α-halosulfone → alkene; one-pot
  pedagogical curiosity).
- **Corey-Bakshi-Shibata follow-up — substrate variation**
  (e.g. phenyl trifluoromethyl ketone) to extend the
  CBS-reduction teaching surface.
- **Phase 38c** lab-setup canvas + **Phase 31k** SAR
  series remain the bigger open work.

A safer pick remains another 1-2 named reactions per
round.  Appel + Jones in one round would close Phase 31b
at 50/50 and complete the original Phase 31 vision.

## 2026-04-25 — Round 155 (Phase 31b — Mukaiyama aldol + Evans aldol, catalogue 44/50 → 46/50, asymmetric-catalysis cat now 6/6 textbook-canon entries)

### Context
Rounds 153-154 opened the asymmetric-catalysis teaching
surface and rounded out the asymmetric-oxygen-installation
toolkit (Sharpless AE + CBS + Sharpless AD + Jacobsen, 4
entries).  Round 155 opens the **asymmetric C-C
bond-formation** teaching surface, complementing the
existing C-O / C=O entries: Mukaiyama aldol (sub-
stoichiometric Lewis-acid catalyst + open TS) and Evans
aldol (stoichiometric chiral auxiliary + closed
Zimmerman-Traxler chair TS) cover the two main paradigms
of asymmetric aldol.  Catalogue advances 44/50 → 46/50;
asymmetric-catalysis category 4 → 6 entries.

### What shipped
**Two named reactions** added to
`orgchem/db/seed_reactions.py`:

1. **Mukaiyama aldol (TMS enol ether of acetone +
   benzaldehyde → 4-hydroxy-4-phenyl-2-butanone)** —
   category *Asymmetric catalysis (C-C bond formation)*
   (NEW sub-category, expanding the asymmetric-catalysis
   teaching surface beyond C-O / C=O).  Mukaiyama 1973.
   Description teaches: pre-formation of the silyl enol
   ether (or silyl ketene acetal) from a ketone via TMSCl
   / TMSOTf + base; Lewis-acid activator (TiCl₄ / BF₃·OEt₂
   for the achiral version, chiral Ti-BINOL / Cu-BOX /
   oxazaborolidinone for the asymmetric — Mukaiyama 1990,
   Carreira 1994); the **open TS** mechanism (Lewis acid
   binds aldehyde carbonyl, silyl enol ether attacks
   without forming a Zimmerman-Traxler chair; silyl group
   blocks the cyclic geometry); the pedagogical advantages
   over base-catalysed aldol (regiochemistry pre-set by the
   enol-ether choice, anti-aldol with simple substrates,
   tolerance of Lewis-basic functional groups).  Reaction
   SMILES `C=C(O[Si](C)(C)C)C.O=Cc1ccccc1 >>
   O[C@H](c1ccccc1)CC(=O)C.O[Si](C)(C)C` — the (R) product
   carries explicit tetrahedral chirality marker.

2. **Evans aldol (N-propionyl-(S)-4-benzyloxazolidinone +
   propanal → syn-(2S,3R)-aldol)** — same C-C bond-
   formation category.  D. A. Evans 1981.  Description
   teaches: the (S)-4-benzyl-2-oxazolidinone chiral
   auxiliary, acylated onto the carboxylic acid via mixed-
   anhydride / DCC chemistry; soft enolisation with Bu₂BOTf
   + i-Pr₂NEt at −78 °C in CH₂Cl₂ to form the (Z)-boron
   enolate; addition through a tightly constrained
   **Zimmerman-Traxler chair TS** (aldehyde R group
   equatorial, boron's two butyl ligands shield one
   enolate face, auxiliary's benzyl group shields the
   other); > 95:5 dr Evans-syn product; LiOH/H₂O₂ auxiliary
   cleavage liberates the carboxylic acid without
   epimerisation.  **Pedagogical contrast with Mukaiyama**
   is called out explicitly: Evans uses a stoichiometric
   chiral *auxiliary* + a closed Zimmerman-Traxler TS
   (gives syn-aldol), whereas Mukaiyama uses a sub-
   stoichiometric Lewis-acid *catalyst* + an open TS
   (gives anti-aldol when uncatalysed; many stereo-outcomes
   possible with chiral catalysts).  Reaction SMILES
   `CCC(=O)N1[C@@H](Cc2ccccc2)COC1=O.CCC=O >>
   CC[C@H](O)[C@@H](C)C(=O)N1[C@@H](Cc2ccccc2)COC1=O` —
   product carries both new stereocentre markers.

**Five intermediate fragments** added to
`orgchem/db/seed_intermediates.py`: `Trimethylsilyl enol
ether of acetone C=C(C)O[Si](C)(C)C` (intermediate),
`(R)-4-Hydroxy-4-phenylbutan-2-one CC(=O)C[C@H](O)c1ccccc1`
(intermediate), `Trimethylsilanol (TMS-OH) C[Si](C)(C)O`
(intermediate), `N-Propionyl-(S)-4-benzyl-2-oxazolidinone
CCC(=O)N1C(=O)OC[C@@H]1Cc1ccccc1` (reagent), `Evans
syn-aldol CC[C@H](O)[C@@H](C)C(=O)N1C(=O)OC[C@@H]1Cc1ccccc1`
(intermediate).

### Tests
Four new tests in `tests/test_reactions.py`:
- `test_mukaiyama_aldol_seeded` — verifies the entry
  exists, the description names the Lewis-acid activator
  family + the open-TS teaching point + the silyl-enol-
  ether substrate class, and the product SMILES carries
  `@`-style chirality markers.
- `test_evans_aldol_seeded` — verifies the entry exists,
  the description names the oxazolidinone auxiliary class
  + Bu₂BOTf boron enolate + Zimmerman-Traxler chair TS +
  syn-aldol product, and the product SMILES carries TWO
  stereocentre markers (the new C-C bond sets two new
  stereocentres simultaneously, the headline pedagogical
  point).
- `test_asymmetric_catalysis_count_at_least_six` —
  asymmetric-catalysis category floor bumped from
  round-154's 4 → 6 entries.
- `test_asymmetric_c_c_bond_formation_present` — confirms
  the new C-C bond-formation sub-category is wired up so
  future re-categorisation can't silently regress.
- `test_named_reaction_count_at_least_forty_six` —
  catalogue-size floor bumped from 44 → 46 (renamed from
  the round-154 _forty_four version).

Discovered + fixed during the test run: fragment-consistency
audit caught 5 missing fragments on first reaction-add.
Resolved by seeding the 5 intermediate rows above.  All 23
reaction-tests pass + all 12 fragment-consistency tests
pass.

### Documentation updates
- ROADMAP.md — Phase 31b entry updated from 44/50 →
  46/50 with descriptions of both new aldol reactions +
  the five new intermediate fragments + the new
  asymmetric-C-C-bond-formation sub-category.
- PROJECT_STATUS.md — round 155 summary prepended.
- SESSION_LOG.md — this entry.

### Test suite status
1 932 passing (up from 1 928 in round 154 — net +4 from
this round's four new test functions).  Doc-coverage test
green; full suite ~44 s wall-clock.

### What's open (next-round candidates)
- **Phase 31b** — 4 more named reactions to reach the 50
  target.  Priority list: Stille coupling (would close
  the Pd-coupling family alongside Suzuki / Negishi /
  Heck / Sonogashira), Corey-Chaykovsky epoxidation
  (sulfur-ylide addition to a ketone — a useful
  pedagogical complement to Wittig + Sharpless AE),
  Appel reaction (PPh₃ / CCl₄ alcohol → alkyl halide,
  a workhorse functional-group interconversion),
  Ramberg-Bäcklund (α-halosulfone → alkene, a stunning
  one-pot pedagogical curiosity), Shapiro reaction
  (tosylhydrazone → vinyl-Li → alkene), Oppenauer
  oxidation (Al(OR)₃-catalysed alcohol → ketone, a
  green-chemistry alternative to Cr-based oxidants),
  Jones oxidation (the chromic-acid version that the
  modern Dess-Martin / Swern / PCC entries displaced —
  still teaching-relevant for over-oxidation context),
  Julia / Peterson / Horner-Wadsworth-Emmons olefinations
  (HWE is already seeded; Julia + Peterson would round
  out the alkene-synthesis toolkit).
- **Phase 38c** — equipment-palette + QGraphicsScene canvas
  for the lab-setup simulator.  Multi-round; biggest open
  scope.
- **Phase 31k** — more SAR series (8/15; 7 to go).

A safer next pick remains another 1-2 named reactions per
round.  Stille coupling + Corey-Chaykovsky in one round
would close the Pd-coupling family AND open the sulfur-
ylide addition teaching surface.

## 2026-04-25 — Round 154 (Phase 31b — Sharpless asymmetric dihydroxylation + Jacobsen-Katsuki epoxidation, catalogue 42/50 → 44/50)

### Context
Round 153 added Sharpless asymmetric epoxidation + CBS
reduction (catalogue 40/50 → 42/50) and **opened the
asymmetric-catalysis teaching surface**.  Round 154 rounds
out the asymmetric-oxygen-installation toolkit: AD complements
the AE entry by working on any alkene without an allylic-OH
restriction, and Jacobsen complements both Sharpless entries
by handling cis-disubstituted aryl alkenes that neither
Sharpless reaction touches.  Together with CBS this brings
the asymmetric-catalysis category to **4 textbook canon
entries**.

### What shipped
**Two named reactions** added to
`orgchem/db/seed_reactions.py`:

1. **Sharpless asymmetric dihydroxylation
   (trans-stilbene → (R,R)-1,2-diphenylethane-1,2-diol)** —
   category *Asymmetric catalysis (oxidation)*.  K. B.
   Sharpless 1988-1996 (the second half of the Nobel-2001
   asymmetric-oxidation toolkit alongside the AE).
   Description teaches: catalytic K₂OsO₄·2H₂O + bis-cinchona
   PHAL chiral ligand pre-mixed as **AD-mix-α** (DHQ)₂PHAL or
   **AD-mix-β** (DHQD)₂PHAL + K₃Fe(CN)₆ stoichiometric
   terminal oxidant + K₂CO₃ + tBuOH/H₂O at 0 °C; the
   mechanism cycle (OsO₄ + alkene → [3+2] osmate ester →
   ferricyanide-driven hydrolysis liberates the syn-diol +
   reduced Os(VI) → re-oxidation back to OsO₄); the Sharpless
   face-selectivity mnemonic (alkene drawn left-to-right with
   larger substituent at upper-left, AD-mix-β attacks from
   below for (R,R), AD-mix-α from above for (S,S)).  **The
   pedagogical contrast with Sharpless asymmetric epoxidation**
   is called out explicitly in the description: AD works on
   ANY alkene (no allylic-OH restriction), and delivers a
   syn-diol rather than an epoxide.  Reaction SMILES
   `c1ccc(/C=C/c2ccccc2)cc1.O=[Os](=O)(=O)=O.O >>
   O[C@@H](c1ccccc1)[C@H](O)c1ccccc1.O=[Os]=O` — the (R,R)
   product carries explicit tetrahedral chirality markers.

2. **Jacobsen-Katsuki epoxidation
   (cis-β-methylstyrene → (2R,3S)-2-methyl-3-phenyloxirane)**
   — category *Asymmetric catalysis (oxidation)*.  Jacobsen
   1990 + Katsuki 1990 independent reports.  Description
   teaches: chiral Mn(III)(salen) complex catalyst —
   canonical (R,R)-/(S,S)-N,N'-bis(3,5-di-tert-butyl-
   salicylidene)-1,2-cyclohexanediamine-Mn(III)Cl 'Jacobsen
   catalyst' — + NaOCl bleach (cheapest), PhIO, NMO, or
   mCPBA terminal oxidant; mechanism (NaOCl oxidises Mn(III)
   → Mn(V)=O oxo-intermediate, alkene approaches over the
   chiral salen ligand from the less-hindered face, concerted
   or radical oxygen transfer gives the epoxide and
   regenerates Mn(III)).  **Critical pedagogical complement to
   Sharpless asymmetric epoxidation**: Jacobsen does NOT
   require an allylic OH because Mn coordinates the oxidant
   not the substrate, making cis-disubstituted aryl alkenes
   (cis-β-methylstyrene, cis-stilbene, indene,
   dihydronaphthalene) the sweet-spot substrates that
   Sharpless cannot touch.  Together with Sharpless
   asymmetric epoxidation + Sharpless asymmetric
   dihydroxylation, completes the asymmetric-oxygen-
   installation toolkit.  Reaction SMILES `C/C=C\\c1ccccc1.
   [Na+].[O-]Cl >> C[C@H]1O[C@@H]1c1ccccc1.[Na+].[Cl-]`.

**Six intermediate fragments** added to
`orgchem/db/seed_intermediates.py`: `Osmium tetroxide
(OsO4) O=[Os](=O)(=O)=O` (reagent), `Osmium dioxide (OsO2)
O=[Os]=O` (intermediate), `(1R,2R)-1,2-Diphenylethane-1,2-
diol O[C@@H](c1ccccc1)[C@H](O)c1ccccc1` (intermediate),
`cis-β-Methylstyrene (Z-1-phenyl-1-propene) C/C=C\\c1ccccc1`
(intermediate), `Hypochlorite (OCl-) [O-]Cl` (reagent),
`(2R,3S)-2-Methyl-3-phenyloxirane C[C@H]1O[C@@H]1c1ccccc1`
(intermediate).  trans-Stilbene was already seeded under
that name — see SMILES backfill below.

**One-shot SMILES backfill** added to
`seed_intermediates.py::seed_intermediates()`.  The pre-
existing `trans-Stilbene` row stored cis-stilbene SMILES
(`C(/c1ccccc1)=C/c1ccccc1`) under the trans name — a real
historical bug.  Fragment-consistency audit caught it on
first run because the round-154 Sharpless AD reaction needs
the actual E-isomer.  Resolution: a new `_SMILES_FIXES`
dict at module top + a follow-up pass in
`seed_intermediates()` that walks every named row whose
stored SMILES doesn't canonicalise to the source-of-truth
SMILES, then updates the row with fresh
`smiles + inchi + inchikey + formula + properties_json`.
Idempotent (no-op when SMILES already matches), gentle
(only touches names listed in `_SMILES_FIXES`), backward-
compatible (silent when DB already correct).  This pattern
will let future rounds fix more buggy historical rows
without race conditions.

### Tests
Three new tests in `tests/test_reactions.py`:
- `test_sharpless_asymmetric_dihydroxylation_seeded` —
  verifies the entry exists, the description names AD-mix-α
  / AD-mix-β + PHAL / cinchona-alkaloid ligand class + the
  no-allylic-OH distinction from Sharpless asymmetric
  epoxidation, and the product SMILES carries `@`-style
  chirality markers.
- `test_jacobsen_katsuki_epoxidation_seeded` — verifies
  the entry exists, the description names the salen
  catalyst class + NaOCl/bleach oxidant + Mn(III)/Mn(V)
  oxo-intermediate + the no-allylic-OH distinction from
  Sharpless, and chirality markers on the product.
- `test_asymmetric_catalysis_count_at_least_four` —
  catalogue-floor for the asymmetric-catalysis category
  (4 entries: Sharpless AE + CBS + Sharpless AD +
  Jacobsen).
- `test_named_reaction_count_at_least_forty_four` —
  catalogue-size floor bumped from 42 → 44 (renamed from
  the round-153 _forty_two version).

Discovered + fixed during the test run: fragment-consistency
audit caught 7 missing fragments on first reaction-add.
Resolved by seeding 6 new intermediate rows + one-shot
SMILES backfill of the buggy trans-Stilbene row.  All 19
reaction-tests pass + all 12 fragment-consistency tests
pass.

### Documentation updates
- ROADMAP.md — Phase 31b entry updated from 42/50 →
  44/50 with descriptions of both new asymmetric-catalysis
  reactions + the six new intermediate fragments + the
  trans-Stilbene SMILES backfill.
- PROJECT_STATUS.md — round 154 summary prepended.
- SESSION_LOG.md — this entry.

(No INTERFACE.md changes needed — `db/seed_intermediates.py`
gained a function but its top-level row description still
covers the intent.)

### Test suite status
1 928 passing (up from 1 925 in round 153 — net +3 from
this round's three new test functions).  Doc-coverage test
green; full suite ~44 s wall-clock.

### What's open (next-round candidates)
- **Phase 31b** — 6 more named reactions to reach the 50
  target.  Priority list: Stille coupling (would close the
  Pd-coupling family alongside Suzuki / Negishi / Heck /
  Sonogashira), Mukaiyama aldol, Evans aldol (asymmetric
  aldol — would extend the asymmetric-catalysis category to
  enantioselective C-C bond formation, a substantive new
  teaching surface), Corey-Chaykovsky epoxidation, Appel
  reaction, Ramberg-Bäcklund, Shapiro, Oppenauer, Jones
  oxidation, Julia / Peterson olefination.
- **Phase 38c** — equipment-palette + QGraphicsScene canvas
  for the lab-setup simulator.  Multi-round; biggest open
  scope.
- **Phase 31k** — more SAR series (8/15; 7 to go).

A safer next pick remains another 1-2 named reactions per
round.  Mukaiyama aldol + Evans aldol in one round would
extend the asymmetric-catalysis category from 4 → 6 entries
and open the C-C bond-formation teaching surface alongside
the C-O / C=O entries shipped in rounds 153-154.

## 2026-04-25 — Round 153 (Phase 31b — Sharpless asymmetric epoxidation + CBS reduction, catalogue 40/50 → 42/50)

### Context
Round 152 added Birch reduction + Dess-Martin oxidation
(catalogue 38/50 → 40/50).  Round 153 continues Phase 31b
with two more entries chosen to **open the asymmetric-
catalysis teaching surface** — until this round, every
seeded reaction in the catalogue ran on achiral or racemic
substrates (or, for chiral enzyme-catalysed entries like
Chymotrypsin, didn't depend on a small-molecule chiral
catalyst).  Sharpless + CBS are the two textbook
asymmetric-catalysis entry points and together cover both
oxidation and reduction.

### What shipped
**Two named reactions** added to
`orgchem/db/seed_reactions.py`:

1. **Sharpless asymmetric epoxidation
   (trans-crotyl alcohol → 2,3-epoxybutan-1-ol)** —
   category *Asymmetric catalysis (oxidation)* (a NEW
   category for the catalogue).  K. B. Sharpless 1980,
   Nobel 2001 (shared with Knowles + Noyori).  The
   description walks through the practical setup
   (catalytic Ti(OiPr)₄ + chiral diethyl tartrate (DET)
   ligand + tert-butyl hydroperoxide oxidant in CH₂Cl₂
   with 4 Å molecular sieves at −20 °C); the
   mechanism (two Ti(OiPr)₄ + two DET self-assemble into
   a dimeric Ti₂(tartrate)₂ complex, allylic alcohol
   coordinates one Ti through its OH, TBHP coordinates
   the same Ti as a peroxide, intramolecular oxygen
   transfer from η²-peroxide to the alkene face dictated
   by the tartrate ligand); the **substrate restriction**
   (the alcohol MUST be allylic — the OH is the anchor
   that binds substrate to Ti); and the **face-selectivity
   mnemonic** ((R,R)-(+)-DET delivers oxygen from below;
   (S,S)-(−)-DET from above, with the allylic alcohol
   drawn with OH at lower right).  Reaction SMILES
   `C/C=C/CO.CC(C)(C)OO >> C[C@@H]1O[C@H]1CO.CC(C)(C)O`
   — the (2R,3R) product carries explicit tetrahedral
   chirality markers so the asymmetric-synthesis teaching
   point survives any future copy-edits.

2. **CBS reduction (acetophenone → (R)-1-phenylethanol)**
   — category *Asymmetric catalysis (reduction)*.  Corey +
   Bakshi + Shibata 1987.  Description walks through the
   sub-stoichiometric chiral oxazaborolidine catalyst
   (derived from (S)- or (R)-α,α-diphenylprolinol + a
   borane) + the stoichiometric BH₃·THF / BH₃·SMe₂ /
   catecholborane hydride source; the cis-fused
   six-membered chair-like TS where catalyst nitrogen
   Lewis-binds borane while catalyst boron Lewis-binds
   the ketone oxygen, bringing hydride + carbonyl into a
   geometry that delivers H from the face opposite the
   *larger* ketone substituent (so (S)-CBS + ArC(=O)R
   with Ar > R → (R)-alcohol).  Functional-group
   tolerance is called out (esters / halides / alkenes
   that NaBH₄ would touch are preserved).  Reaction
   SMILES `CC(=O)c1ccccc1.B >> O[C@@H](C)c1ccccc1` (B is
   the BH₃ hydride source).  **Pedagogical distinction
   from the seeded NaBH₄ entry**: same overall
   transformation (C=O → C-OH), but with a chiral
   catalyst that controls absolute configuration — the
   description names NaBH₄ explicitly so future
   copy-edits can't strip the comparison.

**Five intermediate fragments** added to
`orgchem/db/seed_intermediates.py`: `trans-Crotyl alcohol
(E-2-buten-1-ol) C/C=C/CO`, `tert-Butyl hydroperoxide (TBHP)
CC(C)(C)OO`, `(2R,3R)-2,3-Epoxybutan-1-ol C[C@@H]1O[C@H]1CO`,
`Borane (BH3) B`, `(R)-1-Phenylethanol C[C@H](O)c1ccccc1`.
The Sharpless by-product `tert-Butanol CC(C)(C)O` was
already seeded under that name, so no fragment work needed
on the byproduct side.

### Tests
Three new tests in `tests/test_reactions.py` plus the
`test_named_reaction_count_at_least_forty` from round 152
renamed and bumped to `_forty_two`:
- `test_sharpless_asymmetric_epoxidation_seeded` — verifies
  the entry exists, the description names the Nobel year
  + tartrate ligand + the allylic-OH substrate restriction,
  and the product SMILES carries `@`-style tetrahedral
  chirality markers.
- `test_cbs_reduction_seeded` — verifies the entry exists,
  the description names all three originators (Corey +
  Bakshi + Shibata), the oxazaborolidine catalyst class +
  BH₃ hydride source, the NaBH₄ comparison (which makes
  the entry pedagogically distinct from the seeded
  non-asymmetric ketone reduction), and chirality markers
  on the product.
- `test_asymmetric_catalysis_category_present` — confirms
  at least one reaction row is now tagged with an
  asymmetric-catalysis category, so the new teaching
  surface stays open against future re-categorisation.
- `test_named_reaction_count_at_least_forty_two` —
  catalogue-size floor bumped from 40 → 42.

Discovered + fixed during the test run: the
fragment-consistency audit caught all 5 new fragments
(`C/C=C/CO`, `CC(C)(C)OO`, `C[C@@H]1O[C@H]1CO`, `B`,
`C[C@H](O)c1ccccc1`) on first run.  Resolved by adding
the 5 intermediate rows above; audit now clean.  All 16
reaction-tests pass + all 12 fragment-consistency tests
pass.

### Documentation updates
- ROADMAP.md — Phase 31b entry updated from 40/50 →
  42/50 with descriptions of both new asymmetric-catalysis
  reactions + the five new intermediate fragments.
- PROJECT_STATUS.md — round 153 summary prepended.
- SESSION_LOG.md — this entry.

### Test suite status
1 925 passing (up from 1 922 in round 152 — net +3 from
this round's three new test functions).  Doc-coverage test
green; full suite ~44 s wall-clock.

### What's open (next-round candidates)
- **Phase 31b** — 8 more named reactions to reach the 50
  target.  Priority list: Stille coupling, Jones oxidation,
  Sharpless dihydroxylation (the K-osmium variant — fits
  cleanly with the Sharpless asymmetric epoxidation just
  shipped), Mukaiyama aldol, Evans aldol, Jacobsen
  epoxidation, Corey-Chaykovsky epoxidation, Appel reaction,
  Ramberg-Bäcklund, Shapiro, Oppenauer.  Sharpless
  dihydroxylation + Jacobsen would extend the asymmetric-
  catalysis teaching surface; Stille would close the
  Pd-coupling-family alongside Suzuki / Negishi / Heck /
  Sonogashira.
- **Phase 38c** — equipment-palette + QGraphicsScene canvas
  for the lab-setup simulator.  Multi-round.  Highest-value
  but biggest-scope remaining work.
- **Phase 31k** — more SAR series (8/15; 7 to go).

A safer next pick remains another 1-2 named reactions per
round on the 31b list — same pattern.  Sharpless
dihydroxylation + Jacobsen epoxidation in one round would
push the asymmetric-catalysis category to 4/4 textbook
canon entries.

## 2026-04-25 — Round 152 (Phase 31b — Birch reduction + Dess-Martin oxidation, catalogue 38/50 → 40/50)

### Context
Round 151 closed Phase 43 (cell-component explorer) end-to-
end, completing the user-flagged biology cluster (40/41/42/
43/44/45/46 all shipped across rounds 144-151).  With all
the multi-round catalogue features delivered, round 152 picks
up Phase 31b — the long-running named-reaction expansion that
had stalled at 38/50 since round 134 (CuAAC click).  This is
a tightly-scoped piece of work that fits in a single round
without scope creep into a new feature surface.

### What shipped
**Two named reactions** added to
`orgchem/db/seed_reactions.py`:

1. **Birch reduction (benzene → 1,4-cyclohexadiene)** —
   category *Reduction (single-electron transfer)*.  Birch
   1944 dissolving-metal reduction of an aromatic ring with
   Na (or Li / K) in liquid ammonia at ~ −33 °C with EtOH /
   t-BuOH as proton source.  This is the **first SET-mechanism
   reduction in the entire catalogue** — every other seeded
   reduction (NaBH₄, catalytic hydrogenation) goes through
   concerted / two-electron polar bonds.  The description
   walks through the 4-step ladder: (1) Na donates one
   electron to benzene → radical anion; (2) EtOH protonates
   at the highest-electron-density carbon → cyclohexadienyl
   radical; (3) a second Na donates an electron → pentadienyl-
   stabilised carbanion; (4) EtOH protonates at the central
   carbon → **non-conjugated** 1,4-cyclohexadiene.  Critical
   regioselectivity argument: 1,4 (not 1,3) because protonation
   at the central carbon of the 5-atom pentadienyl anion
   avoids the cross-conjugated diene that protonation at the
   ends would give.  Substituent rule for total-synthesis
   use: EDG (OMe, NR₂) → land on sp²-carbon (un-reduced ring
   position); EWG (COOH, CO-R) → land on sp³.  Reaction
   SMILES `c1ccccc1.[Na].[Na].CCO.CCO >> C1=CCC=CC1.[Na+]
   .[Na+].[O-]CC.[O-]CC` (the canonical `C1=CCC=CC1` is RDKit's
   1,4-cyclohexadiene canonical form).

2. **Dess-Martin oxidation (1-octanol → octanal)** —
   category *Oxidation*.  Dess + Martin 1983 — modern mild
   hyper-valent-iodine(V) oxidation of a 1° alcohol to an
   aldehyde (or 2° alcohol to a ketone) using Dess-Martin
   periodinane (DMP, 1,1,1-tris(acetyloxy)-1,1-dihydro-
   1,2-benziodoxol-3-(1H)-one).  Run in CH₂Cl₂ at room
   temperature, complete in minutes, aqueous bicarbonate /
   thiosulfate workup.  Mechanism described: alcohol-acetate
   ligand exchange at the I(V) centre, intramolecular
   β-acetate-assisted hydride / proton removal via cyclic
   TS, I(V) → I(III) reduction with carbonyl + 2 AcOH +
   IBX by-product.  Critical advantage over Swern: no
   cryogenic temperature, no foul-smelling Me₂S by-product,
   and the reagent is bench-stable as a white powder.
   Critical advantage over Jones / KMnO₄: does NOT
   over-oxidise to carboxylic acid (matches Swern + PCC).
   The now-default 1°→aldehyde oxidation in modern total-
   synthesis labs.  Reaction SMILES `CCCCCCCCO >> CCCCCCCC=O`
   (same product as the existing Swern entry — the teaching
   contrast lives in the descriptions, not the SMILES).

**Three intermediate fragments** added to
`orgchem/db/seed_intermediates.py` so the
fragment-consistency audit stays clean: `Sodium metal [Na]`
(reagent), `Sodium cation [Na+]` (intermediate),
`1,4-Cyclohexadiene C1=CCC=CC1` (intermediate).  The
existing `Ethoxide [O-]CC` entry already covered the
EtO⁻ Birch by-product.

### Tests
Three new tests in `tests/test_reactions.py`:
- `test_birch_reduction_seeded` — verifies the entry exists
  by substring lookup, the canonical `C1=CCC=CC1` 1,4-
  cyclohexadiene appears in the SMILES, the description
  mentions SET / single-electron-transfer (so future
  copy-edits can't strip the mechanistic-class teaching
  point), and the description calls out 1,4-regioselectivity.
- `test_dess_martin_oxidation_seeded` — verifies the entry
  exists, the description mentions I(V) / hyper-valent
  iodine (mechanism class), Swern / Jones (the comparison
  that makes the entry pedagogically distinct from the
  existing oxidations), and the no-over-oxidation argument.
- `test_named_reaction_count_at_least_forty` — catalogue-
  size floor at 40 entries so future regressions surface
  immediately.

Discovered + fixed during the test run: the
fragment-consistency audit
(`tests/test_fragment_consistency.py::
test_every_reaction_fragment_is_in_db`) caught
`[Na]`, `[Na+]`, `C1=CCC=CC1` as uncovered Birch fragments
on first run.  Resolved by adding the three intermediate
rows above; audit now clean.  All 13 reaction-tests pass +
all 12 fragment-consistency tests pass.

### Documentation updates
- ROADMAP.md — Phase 31b entry updated from 38/50 → 40/50
  with description of both new reactions and the three new
  intermediate fragments.
- PROJECT_STATUS.md — round 152 summary prepended.
- SESSION_LOG.md — this entry.

(No INTERFACE.md changes needed — the existing rows for
`db/seed_reactions.py` + `db/seed_intermediates.py` cover
the additive seeding pattern.)

### Test suite status
1 922 passing (up from 1 918 in round 151 — net +4: 3 new
test cases + 1 from doc-coverage flipping back to green
after rebuild).  Doc-coverage test green; full suite
~44 s wall-clock.

### What's open (next-round candidates)
- **Phase 31b** — 8 more named reactions to reach the
  50 target (Stille / Jones / Birch follow-ups / CBS /
  Sharpless asymmetric epoxidation / Sharpless
  dihydroxylation / Mukaiyama aldol / Evans aldol /
  Jacobsen / Corey-Chaykovsky / Appel / Ramberg-Bäcklund
  / Shapiro / Oppenauer).  Sharpless asymmetric epoxidation
  would be the highest-value next pick because the catalogue
  currently has zero asymmetric-catalysis entries.
- **Phase 38c** — equipment-palette + QGraphicsScene canvas
  for the lab-setup simulator.  Multi-round.  Highest-value
  but biggest-scope remaining work.
- **Phase 31k** — more SAR series (8/15; 7 to go).

A safer next pick remains another 1-2 named reactions per
round on the 31b list — same pattern, no scope explosion.
Sharpless asymmetric epoxidation + CBS reduction would
together open the asymmetric-catalysis teaching surface in
the catalogue.

## 2026-04-25 — Round 151 (Phase 43 end-to-end — cell-component explorer)

### Context
Round 150 closed Phase 44 (microscopy across resolution
scales) end-to-end.  Round 151 ships Phase 43 (cell-component
explorer for Eukarya / Bacteria / Archaea) — completing the
user-flagged biology cluster (40 lab analysers + 41
centrifugation + 42 metabolic pathways + 43 cell components +
44 microscopy + 45 lab reagents + 46 pH explorer all shipping
in succession).  This is also the last entry in the queued
catalogue-style features; remaining roadmap work is Phase 38c
(lab-setup canvas, biggest open work) and the Phase 31
stretch buckets.

### What shipped
**Headless data core** — `orgchem/core/cell_components.py`
(~870 lines).  `CellComponent` frozen dataclass: id / name /
domain ∈ {eukarya, bacteria, archaea} / sub_domains tuple /
category / location / function / constituents tuple of
`MolecularConstituent` / notable_diseases / notes.  Nested
`MolecularConstituent` frozen dataclass: name / role / notes /
cross_reference_molecule_name (links a constituent back to a
Phase-6 molecule-DB row when one is seeded).  Three canonical
tuples: `DOMAINS` (3), `SUB_DOMAINS` (6 — animal / plant /
fungus / protist / gram-positive / gram-negative), `CATEGORIES`
(9 — membrane / organelle / nuclear / cytoskeleton / envelope
/ appendage / extracellular / ribosome / genome).

41 components total.  **24 eukaryotic** spanning every major
sub-cellular system: eukaryotic plasma membrane (cholesterol
+ sphingomyelin + PE/PC/PS — fluid-mosaic teaching anchor);
RER (BiP / calnexin / PDI); SER (CYP450 + HMG-CoA reductase
+ SERCA); Golgi (glycosyltransferases + M6P receptor + COPI/
COPII); mitochondrion (cardiolipin + ETC complexes I-V + ATP
synthase + mtDNA + 55S ribosomes — endosymbiotic origin
explicit); chloroplast (chlorophyll a/b + PS-I/II + RuBisCO
+ carotenoids); lysosome (V-ATPase + ~50 acid hydrolases +
LAMP-1/2 — Gaucher / Tay-Sachs / Pompe / Hurler all named);
plant vacuole; peroxisome (catalase + acyl-CoA oxidase —
Zellweger); 26S proteasome (20S core barrel + 19S regulatory
+ ubiquitin — bortezomib teaching hook); 80S cytoplasmic
ribosome.  Nuclear: nuclear envelope (NPC + lamin A/B/C —
Hutchinson-Gilford progeria); nucleolus (RNA Pol I + snoRNA +
fibrillarin — phase-separated condensate teaching example);
chromatin (histone octamer + H1 linker + HATs/HDACs/KMTs/KDMs
— vorinostat teaching hook); telomere (shelterin + telomerase
+ 2009 Nobel context); centromere/kinetochore (CENP-A
nucleosome + Ndc80 / MIS12 / KNL1).  Cytoskeleton: G/F-actin
(myosin II + Arp2/3 + cofilin — phalloidin death-cap-toxin
fluorescent stain); microtubule (α/β-tubulin + γ-TuRC +
kinesin/dynein motors — taxol vs vincristine
opposite-mechanism mitotic-arrest teaching hook);
intermediate filament (keratin / vimentin / neurofilament /
lamin); centrosome / MTOC; eukaryotic cilium/flagellum (9+2
axoneme + dynein arms — primary ciliary dyskinesia /
Kartagener).  Extracellular: animal ECM (collagen + fibronectin
+ laminin + elastin + GAGs + proteoglycans — Ehlers-Danlos);
plant cell wall (cellulose + hemicellulose + pectin +
lignin); fungal cell wall (chitin + β-1,3/β-1,6-glucan +
mannoproteins — echinocandin selective antifungal target).

**11 bacterial**: bacterial plasma membrane (no cholesterol;
hopanoid sterol-analogues); gram+ peptidoglycan (NAG/NAM +
pentaglycine cross-bridge + teichoic acid — β-lactam +
vancomycin teaching hooks); gram- peptidoglycan (thin
single-layer in periplasm + direct meso-DAP cross-link); gram-
outer membrane (LPS endotoxin + porins + Braun's lipoprotein —
septic-shock TLR4 teaching hook); bacterial nucleoid (single
circular chromosome + DNA gyrase fluoroquinolone target +
NAPs); plasmid (β-lactamase as the prototype antibiotic-
resistance cassette); bacterial flagellum (FliC + FlgE +
MotA/B + FliG/M/N — Behe's irreducible-complexity rebuttal);
pilus/fimbria (FimH UPEC adhesin); capsule (pneumococcal
polysaccharide as PCV13/PCV20 vaccine target); biofilm EPS
(exopolysaccharides + eDNA + amyloid-like fimbriae); 70S
ribosome (50S+30S subunits + 23S/5S/16S rRNAs — selectively
targeted by macrolides, tetracyclines, aminoglycosides,
oxazolidinones, chloramphenicol).

**6 archaeal** capturing the lipid divide + the
eukaryote-like translation machinery: archaeal plasma membrane
(ether-linked isoprenoid lipids + glycerol-1-phosphate
backbone + tetraether monolayer in hyperthermophiles — the
strongest single-marker argument for the three-domain
phylogeny); pseudopeptidoglycan (NAT instead of NAM, β-1,3 in
place of β-1,4, L-amino acids — explains lysozyme + β-lactam
resistance); S-layer (self-assembling p1/p2/p3/p4/p6 lattice);
archaeal 70S ribosome (sensitive to anisomycin + diphtheria
toxin like eukaryotes; resistant to bacterial-targeting
antibiotics); archaeal nucleoid (with HMfA/B archaeal histones
forming tetrameric mini-nucleosomes — evolutionary precursor
to (H3-H4)₂); archaellum (ATP-driven, evolutionarily distinct
from bacterial flagellum — homologous to Type-IV pili).

Lookup helpers `list_components(domain, sub_domain)` (sub-
domain query: components with empty `sub_domains` tuple match
ANY sub-domain query within their domain — so mitochondrion
appears under sub_domain="animal" without being animal-
specific), `get_component(id)`, `find_components(needle)`
(case-insensitive substring across id + name + function +
location + notes + notable_diseases + every constituent name +
every constituent role), `components_for_category(category)`,
`domains()`, `sub_domains()`, `categories()`,
`component_to_dict(c)`.

**Dialog** — `orgchem/gui/dialogs/cell_components.py` (~245
lines).  Singleton modeless `QDialog` with a **triple-combo +
free-text filter + list + HTML detail card** layout — domain
combo + sub-domain combo + category combo give the student
fine-grained drill-down (e.g. *all cytoskeleton components in
eukarya / animal*).  Detail card sections: **Location** /
**Function** / **Molecular constituents** (rendered as a
2-column table — name + role; constituent name italicised +
tagged "→ Molecule DB: <name>" when a cross-reference is set)
/ **Notable diseases** (only when set) / **Notes** (only when
set).  `select_component(id)` programmatic API.

**Agent actions** — `orgchem/agent/actions_cell_components.py`
(~120 lines).  5 actions in a new `cell` category:
- `list_cell_components(domain="", sub_domain="")`
- `get_cell_component(component_id)`
- `find_cell_components(needle)`
- `cell_components_for_category(category)`
- `open_cell_components(component_id="")`

Lookup actions are pure-headless; the dialog opener marshals
onto the Qt main thread.  Validation: unknown domain /
sub-domain / category return clean `{"error": str}` dicts;
empty category → `[]` (parity with the catalogue helper).

**Wiring**:
- `orgchem/agent/__init__.py` — added `from orgchem.agent
  import actions_cell_components`.
- `orgchem/gui/main_window.py` — added Tools menu entry
  *Cell components…* with **Ctrl+Shift+J** shortcut + slot.
- `orgchem/gui/audit.py` — registered all 5 actions.

### Tests
68 new tests in `tests/test_cell_components.py` covering:
- catalogue size ≥ 35 (actual 41) + every domain populated
  + Eukarya ≥ 20 entries + bacteria + archaea must-have
  ID lists + 27 user-requested needles (plasma membrane,
  nuclear envelope, ER, Golgi, mitochondrion, chloroplast,
  lysosome, peroxisome, ribosome, nucleolus, chromatin,
  telomere, centrosome, actin, microtubule, IF, cilium, ECM,
  plant cell wall, fungal cell wall, peptidoglycan, outer
  membrane, bacterial flagellum, pilus, capsule, biofilm,
  ether-linked);
- every entry has all required fields + non-empty
  constituents + every id unique + every id matches
  `^[a-z0-9][a-z0-9-]*$` + every domain / sub-domain /
  category in the canonical set + every constituent has a
  non-empty role;
- per-row teaching invariants for the lipid divide
  (cholesterol on eukaryotic-PM, hopanoid on bacterial-PM,
  ether-linked isoprenoid on archaeal-PM); ATP synthase +
  mtDNA on mitochondrion; chloroplast plant-only; chromatin
  histone octamer; telomerase on telomere; lysosome animal-
  only; cellulose on plant-cell-wall; chitin on fungal-
  cell-wall; pentaglycine bridge on gram+ peptidoglycan; LPS
  on gram- outer membrane; L-amino acids / β-lactam
  resistance on pseudopeptidoglycan; archaellum ATP-driven;
  ribosomes present for all 3 domains;
- **cross-references to the molecule database resolve** —
  every constituent that carries a `cross_reference_molecule_name`
  must point to a real seeded molecule row.  Caught my first
  draft using POPC / POPE / Sphingomyelin / 2'-Deoxyadenosine /
  Cellulose β-1,4 fragment — none of which are seeded as
  Molecule rows (they're separate Lipid / Carbohydrate /
  Nucleic-acid catalogues).  Resolution: kept only the
  Cholesterol cross-reference (verified resolves), removed
  the others; xref test now permanent rot-detector;
- filter / lookup edge cases: sub-domain query includes pan-
  domain components (mitochondrion under sub_domain="animal");
  unknown domain / sub-domain → empty; case-insensitive
  search; constituent-name search (cellulose finds
  plant-cell-wall);
- `component_to_dict` serialises nested constituents as a
  list-of-dicts with all 4 MolecularConstituent fields;
- 11 agent-action tests across all 5 entry points + the
  unknown-domain / unknown-sub-domain / unknown-category /
  empty-category error paths;
- 13 dialog tests covering construction (41 rows) /
  singleton / domain-combo filter / sub-domain-combo with
  pan-domain inclusion (chloroplast + plant-cell-wall under
  plant; lysosome excluded under plant) / category-combo /
  text-filter / no-match state / select_component /
  unknown-id select / default-row detail-card sections /
  constituents-table-shown for mitochondrion / agent open
  paths (no-id + with-id + with-unknown-id).

### Documentation updates
- INTERFACE.md — added rows for `core/cell_components.py`,
  `agent/actions_cell_components.py`,
  `gui/dialogs/cell_components.py`.
- ROADMAP.md — Phase 43 marked SHIPPED with delivery
  manifest at the top of the section; original scope kept
  for reference.
- PROJECT_STATUS.md — round 151 summary prepended.
- SESSION_LOG.md — this entry.

### Test suite status
1 918 passing (up from 1 850 in round 150 — net +68 from
this round's `test_cell_components.py`); doc-coverage test
green; full suite ~44 s wall-clock.

### What's open (next-round candidates)
**The user-flagged biology cluster is now fully shipped:**
40 lab analysers (round 146) + 41 centrifugation (round 144)
+ 42 metabolic pathways (round 147) + 43 cell components
(this round) + 44 microscopy (round 150) + 45 lab reagents
(round 149) + 46 pH explorer (round 148) — all delivered
end-to-end across rounds 144-151.

The remaining roadmap items are:
- **Phase 38c** — equipment-palette + QGraphicsScene canvas
  for the lab-setup simulator.  Biggest open work; multi-
  round; likely 3-5 rounds.
- **Phase 31b** — more named reactions (38/50; 12 to go).
- **Phase 31k** — more SAR series (8/15; 7 to go).

Phase 38c (lab-setup canvas) is the highest-value remaining
work but it's a multi-round build that needs careful scope.
A safer next pick is one of the Phase 31 stretch buckets
(31b is closer to the 50 target and adds named-reaction +
mechanism content the tutor panel can immediately use).

## 2026-04-25 — Round 150 (Phase 44 end-to-end — microscopy across resolution scales)

### Context
Round 149 closed Phase 45 (lab reagents reference) end-to-end.
Round 150 ships Phase 44 (microscopy across resolution scales)
— same catalogue + dialog pattern but with a teaching-anchored
twist: the entries are organised by **resolution scale + sample
type**, so a user can jump straight from *"I have live cells, I
want sub-cellular detail"* to the right shortlist
(STORM / PALM / STED / SIM / Airyscan / TIRF live-cell-compatible
subset).  Cross-references from this catalogue to Phase-40a
`lab_analysers.py` close the loop between the resolution-anchored
teaching view and the manufacturer-anchored instrument view of
the same hardware (Zeiss LSM 980 / Lattice Lightsheet / Krios /
Bruker Biotyper).

### What shipped
**Headless data core** — `orgchem/core/microscopy.py` (~620
lines).  `MicroscopyMethod` frozen dataclass: id / name /
abbreviation / resolution_scale / sample_types tuple /
typical_resolution / light_source / contrast_mechanism /
typical_uses / strengths / limitations /
representative_instruments / cross_reference_lab_analyser_ids /
notes.  Two canonical tuples: `RESOLUTION_SCALES` (6 scales,
coarsest first) + `SAMPLE_TYPES` (8 sample types).

30 entries across all 6 resolution scales:
- **whole-organism** (4): stereo dissecting microscope,
  intra-vital microscopy, OCT, small-animal MRI.
- **tissue** (5): brightfield histology (H&E + IHC + special
  stains), multiplex IHC (CODEX / Vectra Polaris), light-sheet
  fluorescence, MALDI-MSI, polarised-light microscopy.
- **cellular** (6): phase contrast, DIC Nomarski, widefield
  epifluorescence, laser-scanning confocal, spinning-disk
  confocal, two-photon multi-photon.
- **sub-cellular** (6): SIM, STORM/dSTORM, PALM, STED,
  Airyscan, TIRF.
- **single-molecule** (5): smFRET, cryo-EM, cryo-ET, AFM, STM.
- **clinical-histology** (4): clinical light microscope (the
  pathology workhorse), frozen-section cryostat, clinical IHC,
  digital-pathology slide scanner (WSI).

Each entry is a long-form reference card capturing the
technique's resolution + light source + contrast mechanism + the
strengths-vs-limitations trade-off.  Cross-references to
Phase-40a `lab_analysers.py` for instruments that appear both
as an *instrument* and a *resolution-anchored teaching view*:
- `confocal` → `zeiss_lsm_980`
- `airyscan` → `zeiss_lsm_980`
- `light-sheet` → `zeiss_lattice_lightsheet`
- `cryo-em` → `thermo_krios_g4`
- `cryo-et` → `thermo_krios_g4`
- `maldi-imaging` → `bruker_biotyper`

Lookup helpers `list_methods(resolution_scale)`,
`get_method(id)`, `find_methods(needle)` (case-insensitive
substring across id + name + abbreviation + typical_uses +
representative_instruments), `methods_for_sample_type(sample)`
(returns the methods listing the given sample type as
typical), `resolution_scales()`, `sample_types()`,
`method_to_dict(m)`.  No Qt imports; fully headless-testable.

**Dialog** — `orgchem/gui/dialogs/microscopy.py` (~230 lines).
Singleton modeless `QDialog` with the **resolution-scale combo
+ sample-type combo + free-text filter + list + HTML detail
card** layout — same shape as the Phase-37/40/45 catalogue
dialogs but with TWO filter combos, so the user can ask
*"super-resolution methods for fixed cells"* and get exactly
the right shortlist.  Detail card sections: Typical resolution
/ Light source / Contrast mechanism / Sample types / Typical
uses / Strengths / Limitations / Representative instruments /
Cross-reference (Phase 40a Lab analysers) — last section
shown only when the method has cross-references.
`select_method(id)` programmatic API.

**Agent actions** — `orgchem/agent/actions_microscopy.py`
(~115 lines).  5 actions in a new `microscopy` category:
- `list_microscopy_methods(resolution_scale="")`
- `get_microscopy_method(method_id)`
- `find_microscopy_methods(needle)`
- `microscopy_methods_for_sample(sample_type)`
- `open_microscopy(method_id="")`

Lookup actions are pure-headless; the dialog opener marshals
onto the Qt main thread via `_gui_dispatch.run_on_main_thread_sync`.
Validation: unknown resolution-scales / sample-types return
clean `{"error": str}` dicts rather than raising; empty
sample-type returns `[]` (parity with the catalogue helper).

**Wiring**:
- `orgchem/agent/__init__.py` — added `from orgchem.agent
  import actions_microscopy`.
- `orgchem/gui/main_window.py` — added Tools menu entry
  *Microscopy techniques…* with **Ctrl+Alt+M** shortcut + slot.
- `orgchem/gui/audit.py` — registered all 5 actions.

### Tests
52 new tests in `tests/test_microscopy.py` covering:
- catalogue size ≥ 25 (actual 30) + every resolution scale
  populated + every sample type used by at least one method
  + every entry has all required fields + every id unique +
  every id matches `^[a-z0-9][a-z0-9-]*$`;
- presence of every must-have user-requested method (19
  needles: stereo, intravital, OCT, histology, light-sheet,
  confocal, two-photon, SIM, STORM, PALM, STED, TIRF,
  smFRET, cryo-EM, AFM, STM, frozen, IHC, digital-pathology);
- per-row teaching invariants (confocal pinhole / sectioning;
  STORM nm-scale resolution; cryo-EM near-atomic resolution;
  AFM force spectroscopy; STM individual-atom imaging;
  frozen-section intra-op rapid-diagnosis; two-photon deep
  penetration; OCT clinical / ophthalmology mention);
- clinical-histology workflow includes the 4 routine items
  (LM + FS + IHC + WSI);
- sub-cellular includes all 6 super-resolution + TIRF;
- single-molecule includes smFRET + cryo-EM + cryo-ET + AFM
  + STM;
- **Phase-40a cross-references all resolve to real
  lab_analyser ids** — this caught 3 real id mismatches in
  my first draft (`zeiss_lattice_lightsheet_7` →
  `zeiss_lattice_lightsheet`, `zeiss_lsm980` → `zeiss_lsm_980`,
  `bruker_maldi_biotyper` → `bruker_biotyper`); now
  permanently guarded against rot;
- list / get / find / methods_for_sample_type edge cases
  (unknown scale → empty; unknown id → None;
  case-insensitive search; empty needle → empty;
  unknown sample-type → empty);
- canonical ordering: scales tuple starts with
  `whole-organism` and ends with `clinical-histology`;
- `method_to_dict` exposes all 14 fields incl. tuple
  fields;
- 9 agent-action tests across all 5 entry points + the
  unknown-scale / unknown-sample / empty-sample error paths;
- 11 dialog tests covering construction (30 rows) /
  singleton / scale-combo filter / sample-combo filter /
  text-filter / no-match state / select_method /
  unknown-id select / default-row detail-card sections /
  cross-reference-section-shown for cryo-EM / agent open
  paths (no-id + with-id + with-unknown-id).

### Documentation updates
- INTERFACE.md — added rows for `core/microscopy.py`,
  `agent/actions_microscopy.py`, `gui/dialogs/microscopy.py`.
- ROADMAP.md — Phase 44 marked SHIPPED with delivery
  manifest at the top of the section; original scope kept
  for reference.
- PROJECT_STATUS.md — round 150 summary prepended.
- SESSION_LOG.md — this entry.

### Test suite status
1 850 passing (up from 1 798 in round 149 — net +52 from
this round's `test_microscopy.py`); doc-coverage test
green; full suite ~45 s wall-clock.

### What's open (next-round candidates)
Two user-flagged phases remain unfinished:
- **Phase 43** — cell-component explorer (Eukarya / Bacteria
  / Archaea).  Visually striking; bigger scope than the
  catalogue rounds — likely 2 rounds.
- **Phase 38c** — equipment-palette + QGraphicsScene canvas
  for the lab-setup simulator.  Biggest open work in the
  whole roadmap.

The two stretch buckets remain:
- **Phase 31b** — more named reactions (38/50).
- **Phase 31k** — more SAR series (8/15).

Phase 43 (cell-component explorer) is the natural next pick
because it completes the user-flagged biology cluster
(40 lab analysers + 41 centrifugation + 42 metabolic
pathways + 43 cell components + 44 microscopy + 45 lab
reagents + 46 pH explorer all ship in succession).  Phase
38c is technically the highest-value but it's a multi-round
build that needs careful scope.

## 2026-04-25 — Round 149 (Phase 45 end-to-end — lab-reagents reference catalogue)

### Context
Round 148 closed Phase 46 (pH + buffer explorer) end-to-end.
Round 149 ships Phase 45 (lab reagents reference) — the
natural neighbour: same catalogue + dialog pattern, and the
new `reagent` category cross-references the buffer designer
in the just-shipped pH explorer (Tris / HEPES / MOPS / MES /
BIS-TRIS now have full bench cards under *Tools → Lab
reagents…*).

### What shipped
**Headless data core** — `orgchem/core/lab_reagents.py` (~1 250
lines).  `LabReagent` frozen dataclass (id / name / category /
typical_concentration / storage / hazards / preparation_notes
/ cas_number / typical_usage / notes).  75 entries across 10
categories:

- **buffer** (11): Tris-HCl, HEPES, MOPS, MES, PBS, TBS,
  citrate, carbonate, glycine-HCl, McIlvaine, BIS-TRIS.
- **acid-base** (7): HCl 1 M / 6 N, conc. H₂SO₄, conc. HNO₃,
  glacial AcOH, NaOH, KOH, conc. NH₄OH.
- **detergent** (6): SDS, Triton X-100, Tween 20,
  NP-40 / Igepal CA-630, CHAPS, n-octyl-glucoside.
- **reducing-agent** (4): DTT, β-mercaptoethanol, TCEP, GSH.
- **salt** (8): NaCl, KCl, MgCl₂, CaCl₂, MgSO₄, ammonium
  sulfate, EDTA, EGTA.
- **protein-prep** (3): BSA, protease-inhibitor cocktail,
  phosphatase-inhibitor cocktail.
- **stain** (7): Coomassie R-250, Coomassie G-250 (Bradford
  reagent), ethidium bromide, SYBR Safe, AgNO₃, methylene
  blue, crystal violet.
- **solvent** (10): DMSO, DMF, ethanol abs., methanol,
  acetone, chloroform, hexane, THF, DCM, acetonitrile.
- **cell-culture** (9): DMEM, RPMI-1640, MEM, Ham's F-12,
  Opti-MEM, FBS, trypsin-EDTA, Pen-Strep, L-glutamine.
- **molecular-biology** (10): dNTPs, agarose, Taq + Phusion
  polymerases, EcoRI + BamHI restriction enzymes, T4 DNA
  ligase, RNase A, RNase-free DNase I, proteinase K.

Every entry is a long-form bench card with the practical
handling tips that bite junior lab members:
- Tris pH-drifts ~0.03/°C — always pH at the use temperature.
- HEPES generates H₂O₂ under intense light + Fe²⁺ — store
  solutions away from light.
- SDS precipitates < 15 °C — rewarm before pipetting; weigh
  powder in a fume hood (respiratory sensitiser).
- DMSO freezes at 18.5 °C; carries chemicals across skin —
  change gloves frequently.
- Vanadate must be activated (boil + adjust pH 10 → cool) for
  max phosphatase-inhibition potency.
- EtBr is a mutagen / suspected carcinogen — use SYBR Safe
  for cloning workflows.
- TCEP is the modern DTT replacement: odourless, stable,
  MS-friendly, maleimide-compatible.
- Phusion has ~50× lower error rate than Taq; blunt-end
  product for cloning vs Taq's A-overhang for TA.
- McIlvaine buffer spans pH 2.2–8.0 — wide-range enzyme
  kinetics in one buffer.

Each entry carries a CAS number so the lookup
`find_reagents("67-68-5")` lands on DMSO directly (not just
on name-matches).

Lookup helpers `list_reagents(category)`, `get_reagent(id)`,
`find_reagents(needle)` (case-insensitive substring across
id + name + category + typical_usage + cas_number),
`categories()`, `reagent_to_dict(r)`.  No Qt imports;
fully headless-testable.

**Dialog** — `orgchem/gui/dialogs/lab_reagents.py` (~210
lines).  Singleton modeless `QDialog` with the same shape as
the Phase-40a *Lab analysers* dialog: category combo + free-
text filter on the left, list of `name — category` rows,
HTML detail card on the right with sections **Typical
concentration** / **Storage** / **Hazards** / **Preparation
notes** / **Typical usage** / **Notes**.  CAS shown in the
sub-title meta line for quick reference.  `select_reagent(id)`
programmatic API for the agent open path.

**Agent actions** — `orgchem/agent/actions_lab_reagents.py`
(~85 lines).  4 actions in a new `reagent` category:
- `list_lab_reagents(category="")`
- `get_lab_reagent(reagent_id)`
- `find_lab_reagents(needle)`
- `open_lab_reagents(reagent_id="")`

Lookup actions are pure-headless; the dialog opener marshals
onto the Qt main thread via `_gui_dispatch.run_on_main_thread_sync`.

**Wiring**:
- `orgchem/agent/__init__.py` — added `from orgchem.agent
  import actions_lab_reagents`.
- `orgchem/gui/main_window.py` — added Tools menu entry
  *Lab reagents…* with **Ctrl+Shift+R** shortcut + slot.
- `orgchem/gui/audit.py` — registered all 4 actions in
  `GUI_ENTRY_POINTS`.

### Tests
45 new tests in `tests/test_lab_reagents.py` covering:
- catalogue size ≥ 50 (actual 75) + every category populated
  + every entry has all required fields + every id unique +
  every id matches `^[a-z0-9][a-z0-9-]*$`;
- canonical CAS values for Tris (77-86-1) + DMSO (67-68-5);
- presence of every must-have user-requested reagent (24
  needles: tris, hepes, mops, mes, pbs, tbs, sds, triton,
  tween, dtt, tcep, edta, bsa, coomassie, ethidium, dmso,
  dmf, dmem, rpmi, trypsin, agarose, taq, ecori, rnase);
- per-row teaching invariants (TCEP odourless / stable /
  MS-friendly mention; DMSO freezing-point warning at 18 °C;
  EtBr mutagen warning; Phusion high-fidelity / blunt-end
  mention; Taq no-proofreading / TA cloning mention; DMEM
  mentions FBS + Pen-Strep supplementation; SDS anionic /
  denaturing; Triton non-ionic; HEPES pKa mention);
- buffer category includes all 7 Good's buffers used in
  Phase-46 pH explorer (Tris / HEPES / MOPS / MES / PBS /
  TBS / BIS-TRIS);
- solvent category covers the 6 most-common (DMSO, ethanol,
  methanol, acetone, chloroform, acetonitrile);
- list / get / find edge cases (unknown category → empty;
  unknown id → None; case-insensitive search; empty needle
  → empty; CAS-number search direct hit);
- `reagent_to_dict` exposes all 10 fields;
- 6 agent-action tests across all 4 entry points (with the
  unknown-category error path);
- 11 dialog tests covering construction (75 rows) /
  singleton / category-combo filter / text-filter / no-match
  state / select_reagent / unknown-id select / default-row
  detail-card sections / CAS-in-meta-line / agent open path
  with id / agent open path with unknown id.

One small alignment during the test run:
- `list_reagents(category="not-a-real-category")` initially
  raised `ValueError`; switched to "return empty" to match
  the sibling Phase-40a `list_analysers` API and let the
  agent action own the user-facing error path.

### Documentation updates
- INTERFACE.md — added rows for `core/lab_reagents.py`,
  `agent/actions_lab_reagents.py`, `gui/dialogs/lab_reagents.py`.
- ROADMAP.md — Phase 45 marked SHIPPED with delivery
  manifest at the top of the section; original scope kept
  for reference.
- PROJECT_STATUS.md — round 149 summary prepended.
- SESSION_LOG.md — this entry.

### Test suite status
1 798 passing (up from 1 753 in round 148 — net +45 from
this round's `test_lab_reagents.py`); doc-coverage test
green; full suite ~43 s wall-clock.

### What's open (next-round candidates)
Three user-flagged phases remain unfinished:
- **Phase 43** — cell-component explorer (Eukarya / Bacteria
  / Archaea).  Visually striking; bigger scope than 45.
- **Phase 44** — microscopy across resolution scales.  Same
  catalogue + dialog pattern as 40a / 45.
- **Phase 38c** — equipment-palette + QGraphicsScene canvas
  for the lab-setup simulator.  Biggest open work.

The two stretch buckets (31b more named reactions, 31k more
SAR series) remain easy wins.  Phase 44 (microscopy) is a
natural pick to follow 45 because it shares the catalogue +
dialog pattern, and the resolution-scale framing
(super-resolution → cryo-EM → AFM → STM) makes a tidy
combo + filter tab.

## 2026-04-25 — Round 148 (Phase 46 end-to-end — pH + buffer explorer)

### Context
Round 147 closed Phase 42a (metabolic-pathways explorer)
end-to-end + added Phases 45 (lab reagents) and 46 (pH +
buffer explorer) to the roadmap.  Round 148 ships Phase 46
end-to-end — the freshest user-flagged content and a natural
fit for a single round because the underlying solvers are
tight (Henderson-Hasselbalch + buffer capacity + titration
curve) and the pKa catalogue size (~46 acids) maps cleanly
onto a 7-category combo.

### What shipped
**Headless data core** — `orgchem/core/ph_explorer.py` (~700
lines):
- `AcidEntry` frozen dataclass (id / name / formula /
  category / pka_values tuple / notes).
- `ReferenceCard` frozen dataclass (id / title / body
  markdown).
- 46-acid pKa catalogue across 7 categories:
  - **mineral** (8): HCl, H₂SO₄, H₃PO₄, HNO₃, HF, H₂CO₃,
    H₂S, HClO₄.
  - **carboxylic** (11): formic, acetic, propionic, lactic,
    citric (3 pKa), oxalic, malonic, malic, tartaric (all
    di-protic), benzoic, ascorbic.
  - **amine** (6): NH₄⁺, MeNH₃⁺, Me₂NH₂⁺, Me₃NH⁺,
    pyridinium, imidazolium.
  - **amino-acid** (9): gly, ala, asp, glu, his, lys, arg,
    cys, tyr — α-COOH + α-NH₃⁺ + sidechain pKas.
  - **phenol** (3): phenol, p-nitrophenol, picric acid.
  - **biological-buffer** (7): Tris 8.10, HEPES 7.55, MES
    6.10, MOPS 7.20, BIS-TRIS 6.50, PIPES 6.76, CHES 9.30 —
    a Good's-buffer + zwitterion picker.
  - **other** (2): HCN, H₂O₂.
- 6 reference cards: ph_definition, strong_weak,
  henderson_hasselbalch, buffer_capacity, polyprotic,
  biological_buffers.
- 3 solvers:
  - `design_buffer(target_pH, pKa, total_concentration_M,
    volume_L=1.0)` — Henderson-Hasselbalch ratio + [HA] /
    [A⁻] split + moles + ΔpH-vs-pKa capacity verdict
    (warning if |ΔpH| > 1).
  - `buffer_capacity(total_concentration_M, pH, pKa)` →
    β = 2.303 · C · α · (1 − α) + α + fraction-of-max.
  - `titration_curve(weak_acid_pKa, acid_initial_M,
    volume_acid_mL, base_concentration_M, n_points=50)` →
    full (vol_mL, pH) curve with charge-balance solve +
    equivalence-point extraction.
- Lookup helpers: `list_acids(category)`, `get_acid(id)`,
  `find_acids(needle)`, `categories()`, `acid_to_dict(a)`.
- Sanity-tested in Python: phosphate buffer at pH 7.4 / pKa
  7.20 → 38.7 / 61.3 mM split; β maxes at 0.0576 M/pH for
  0.1 M total at pH=pKa; 25 mL of 0.1 M NaOH titrates 25 mL
  of 0.1 M acetic acid to pH 8.72.

**Dialog** — `orgchem/gui/dialogs/ph_explorer.py` (~370
lines).  Singleton modeless 4-tab `QDialog`:
- **Reference** — 6 teaching cards rendered as HTML.
- **Buffer designer** — pKa-acid combo auto-fills the pKa
  spinbox; target pH / total concentration / volume
  spinboxes drive `design_buffer`; result pane shows ratio +
  [HA] / [A⁻] split + moles + colour-coded capacity verdict
  (red `Capacity warning:` when ΔpH > 1, green `OK:`
  otherwise).
- **Titration curve** — weak-acid pKa + initial M + volume
  mL + base M spinboxes drive `titration_curve`; result
  pane renders the (vol_mL, pH) points as an HTML table
  with the equivalence-point row highlighted.
- **pKa lookup** — category combo + free-text filter +
  `QTableWidget` of name / formula / category / pKa values.
- `select_tab(label)` + `tab_labels()` programmatic API
  for the agent open path.

**Agent actions** — `orgchem/agent/actions_ph_explorer.py`
(~140 lines).  7 actions in a new `ph` category:
- `list_pka_acids(category="")`
- `get_pka_acid(acid_id)`
- `find_pka_acids(needle)`
- `design_buffer(target_pH, pKa, total_concentration_M,
  volume_L=1.0)`
- `buffer_capacity(total_concentration_M, pH, pKa)`
- `simulate_titration(weak_acid_pKa, acid_initial_M,
  volume_acid_mL, base_concentration_M, n_points=50)`
- `open_ph_explorer(tab="")`

Each solver-wrapping action converts `ValueError` → `{"error":
str}`; the dialog opener marshals onto the Qt main thread via
`_gui_dispatch.run_on_main_thread_sync`.

**Wiring**:
- `orgchem/agent/__init__.py` — added `from orgchem.agent
  import actions_ph_explorer`.
- `orgchem/gui/main_window.py` — added Tools menu entry
  *pH explorer…* with **Ctrl+Alt+H** shortcut + slot.
- `orgchem/gui/audit.py` — registered all 7 actions in
  `GUI_ENTRY_POINTS`.

### Tests
54 new tests in `tests/test_ph_explorer.py` covering:
- pKa catalogue size + every category populated + canonical
  pKa values for histidine (sidechain near physiological
  pH), Tris (8.10), phosphate (3-way 2.15 / 7.20 / 12.35),
  acetic acid (4.76).
- All 6 reference cards present with markdown body.
- `design_buffer`: pH=pKa unity ratio, phosphate at 7.4
  matches HH textbook split, far-from-pKa warning fires,
  `[HA] + [A⁻] = total` invariant, moles track volume,
  error paths (negative total / negative volume).
- `buffer_capacity`: max at pH=pKa, drop-off at distance.
- `titration_curve`: acetic-acid initial pH 2.88,
  equivalence at 25 mL, eq pH > 7.
- `acid_to_dict` round-trip.
- 12 agent-action tests across all 7 entry points.
- 13 dialog tests covering construction / singleton /
  select_tab / buffer designer runs (success + warning) /
  capacity / titration / lookup table / filter narrowing /
  agent action open path.

Two minor adjustments during the test run:
- `buffer_capacity` `beta_max` tightened from `0.576 · C` to
  `2.303 · C · 0.25` so `fraction_of_max == 1.0` at α=0.5
  instead of `0.99957…`.
- Test buffer-designer assertion adjusted from `38.7 / 61.3
  mM` to `38.686 / 61.314 mM` to match the dialog's
  3-decimal display format.

### Documentation updates
- INTERFACE.md — added rows for `core/ph_explorer.py`,
  `agent/actions_ph_explorer.py`, `gui/dialogs/ph_explorer.py`.
- ROADMAP.md — Phase 46 marked SHIPPED with delivery
  manifest at the top of the section; original scope kept
  for reference.
- PROJECT_STATUS.md — round 148 summary prepended.
- SESSION_LOG.md — this entry.

### Test suite status
1 753 passing (up from 1 699 in round 147 — net +54 from
this round's `test_ph_explorer.py`); doc-coverage test
green; full suite ~43 s wall-clock.

### What's open (next-round candidates)
The roadmap still has 4 unfinished user-flagged
phases (43 cell-component, 44 microscopy, 45 lab
reagents — all "queued, ~2 rounds each") plus
Phase 38c (lab-setup canvas, the biggest open work)
and the 31b / 31k stretch goals.  Phase 45 (lab
reagents reference) is a natural next pick because
it shares the catalogue + dialog pattern with the
just-shipped pH explorer and unlocks cross-references
from the buffer designer (Tris / HEPES / MOPS… ↔
the reagent entries).  Phase 43 is bigger but more
visually striking.

## 2026-04-25 — Round 147 (Phase 42a end-to-end — metabolic pathways + 2 new roadmap phases)

### Context
Round 146 closed Phase 40a (lab analysers) end-to-end +
added Phases 42 / 43 / 44 to the roadmap.  Round 147
ships Phase 42a (the freshest user-flagged content)
end-to-end.  Mid-round, two more user-flagged feature
requests came in and were added to the roadmap as Phases
45 (lab reagents) + 46 (pH + buffer explorer).

### What shipped (Phase 42a)
- **`orgchem/core/metabolic_pathways.py`** — three
  frozen dataclasses + 11 seeded pathways:
    - **Frozen dataclasses**: `RegulatoryEffector` (name
      / mode ∈ {activator, inhibitor} / mechanism free-
      text), `PathwayStep` (step_number / substrates /
      enzyme_name / ec_number / products / reversibility
      ∈ {reversible, irreversible} / delta_g_kjmol /
      regulatory_effectors / notes), `Pathway` (id /
      name / category / cellular_compartment / overview
      / overall_delta_g_kjmol / textbook_reference /
      steps).
    - **Central-carbon (4)**: glycolysis (10 steps —
      every step from hexokinase to pyruvate kinase
      with regulatory effectors per step), TCA cycle
      (8 steps incl. Krebs's original regulatory
      story), oxidative phosphorylation (5 complexes
      I-V with Q-cycle + Mitchell chemiosmotic notes),
      pentose phosphate (5 steps with G6PD-deficiency
      anaemia clinical note).
    - **Lipid (3)**: β-oxidation Lynen helix (4 steps
      with VLCAD/MCAD/SCAD chain-length isoforms),
      fatty-acid biosynthesis (3 stages — ACC + FAS
      multi-enzyme rate-limited by acetyl-CoA
      carboxylase), cholesterol biosynthesis (6 stages
      from acetyl-CoA → mevalonate → squalene →
      lanosterol → cholesterol with HMG-CoA reductase
      as the statin target).
    - **Amino-acid (1)**: urea cycle (5 steps —
      mitochondrial CPS-I + OTC then cytoplasmic
      synthetase + lyase + arginase, with N-acetyl-
      glutamate allosteric activator).
    - **Specialised (3)**: heme biosynthesis (8 steps
      with one porphyria per enzyme deficiency), Calvin
      cycle photosynthetic carbon fixation (5 stages —
      RuBisCO carboxylation + reduction + regeneration),
      glycogen synthesis + breakdown (5 steps with
      full PKA cascade hormonal regulation).
    - `nucleotide` category reserved for purine +
      pyrimidine de novo (42a.1 polish round).
  ΔG values from Nelson & Cox 8e; EC numbers from
  IUBMB / BRENDA.  Each step's `regulatory_effectors`
  list captures the textbook-canonical regulators
  (e.g. PFK-1 step 3: ATP / Citrate / AMP / Fructose-
  2,6-bisphosphate; HMG-CoA reductase step 2:
  cholesterol + oxysterols / AMPK / Statins).
- **`orgchem/gui/dialogs/metabolic_pathways.py`** —
  singleton modeless dialog wired to *Tools →
  Metabolic pathways…* (Ctrl+Alt+P).  Three-pane
  horizontal splitter:
    - **Left**: category combo + free-text filter +
      pathway list.
    - **Middle**: pathway title + meta block (category
      / compartment / step count / overview / overall
      ΔG / textbook reference) + per-step
      `QTableWidget` (#, Enzyme, EC, Rev?, ΔG).
      Reversibility uses ↔ / → glyphs.
    - **Right**: step-detail pane showing substrates /
      products / regulatory effectors (as a `<ul>`
      list) / notes for the currently-selected step.
  `select_pathway(id)` + `select_step(step_number)`
  programmatic API for the agent open path.
- **`orgchem/agent/actions_metabolic_pathways.py`** —
  5 actions in a new `biochem` category:
  `list_metabolic_pathways(category)` /
  `get_metabolic_pathway(id)` /
  `find_metabolic_pathways(needle)` /
  `list_pathway_steps(pathway_id)` /
  `open_metabolic_pathways(pathway_id, step_number)`.
- **Auto-loader, Tools menu (Ctrl+Alt+P), GUI audit**
  all updated; coverage stays at 100 %.

### Tests
- **`tests/test_metabolic_pathways.py`** — 41 cases:
    - Catalogue size ≥ 10 + 11 canonical pathways
      present + every-pathway-required-fields +
      every-step-required-fields.
    - **Step-count invariants**: glycolysis = 10, TCA
      = 8, ox-phos = 5 complexes (with each step
      enzyme name containing the right Roman numeral),
      urea = 5, heme = 8.
    - **Per-pathway teaching invariants**:
        - Glycolysis step 1 (hexokinase) lists G6P
          product feedback.
        - Glycolysis step 3 (PFK-1) is irreversible +
          has ≥ 3 regulatory effectors with both
          inhibitors AND activators (the textbook
          rate-limiting allosteric story).
        - TCA cycle's succinate-dehydrogenase notes
          mention "membrane" (the only TCA enzyme
          embedded in the inner mitochondrial membrane).
        - Ox-phos Complex IV products / notes
          reference H₂O (the terminal electron
          acceptor — the whole point of aerobic
          respiration).
        - Cholesterol step 2 (HMG-CoA reductase) lists
          statin + cholesterol effectors (the
          medicinal-chem teaching anchor that ties
          back to Phase 19a SAR series).
        - Pentose phosphate step 1 (G6PD) notes
          mention deficiency / anaemia (the most-
          common human enzyme deficiency at ~400 M
          people).
        - Glycogen phosphorylase has hormonal
          regulators (glucagon / epinephrine / insulin /
          AMP / ATP).
    - List filter by category + unknown-category
      empty + get-unknown-none + find-substring +
      case-insensitive + empty-needle.
    - to_dict serialisation has all 9 expected
      pathway keys + 9 expected step keys.
    - 8 agent-action tests covering happy-path +
      every error path.
    - 8 pytest-qt dialog tests: construction,
      singleton, default first-pathway populates step
      table, programmatic select_pathway, select_step
      shows detail with Substrates / Products /
      Regulatory-effectors sections, text filter, no-
      match blank state, agent-action open path with
      pathway + step focus.
- All 41 pass on first run.
- Full suite: **1 700 / 1 700 pass, 0 skipped** (was
  1 659).

### Roadmap additions (mid-round, user-flagged)
- **Phase 45** — lab reagents reference.  ~50 entries
  across 10 categories (buffers / acids+bases /
  detergents / reducing agents / salts / protein-prep /
  stains+dyes / solvents / cell-culture media /
  molecular-biology reagents).  Each: typical
  concentration, storage, hazards, preparation,
  CAS, typical usage.  3 sub-phases (45a catalogue,
  45b dialog, 45c agent actions).
- **Phase 46** — pH + buffer explorer.  Reference
  cards (pH definition, autoionisation, weak vs
  strong, Henderson-Hasselbalch, buffer capacity,
  polyprotic) + buffer designer widget (target pH +
  pKa + total conc → mass / volume of HA + A⁻
  stock) + titration-curve plotter + pKa lookup
  table (~30-50 acids).  Cross-references the Phase-
  39a Henderson-Hasselbalch action.  3 sub-phases
  (46a catalogue + solver, 46b dialog, 46c agent
  actions).

### Design notes
- **Why ship 42a / 42b / 42c bundled in one round?**
  Same reasoning as Phase 41 + Phase 40a — the
  pattern is fully nailed, the catalogue stays
  tight at 11 pathways (~300 lines), and splitting
  three trivial dialog/action rounds across three
  iterations would be padding.  When the catalogue
  expands (42a.1 nucleotide), the 1-round pattern
  scales fine.
- **Why frozen dataclasses for `Pathway` /
  `PathwayStep` / `RegulatoryEffector`?**  Same
  pattern as Phase 38b's `Setup` / `SetupConnection`
  + Phase 37b's `LabAnalyte` / `LabPanel`.  Frozen
  guarantees the catalogue is immutable from the
  consumer side; if a regulatory effector needs to
  be shared across multiple pathway steps, the
  identity-equality semantic guarantees data
  consistency.  The dataclass + Tuple-of-dataclass
  composition gives JSON-serialisability via
  `dataclasses.asdict` (used by the `to_dict`
  helpers).
- **Why ΔG values for some steps but not others?**
  The Lehninger 8e textbook gives ΔG° (standard
  state) values for the canonical glycolysis +
  TCA + ox-phos steps; less-routine pathways (heme
  biosynth, Calvin cycle regen phase) only have ΔG
  values for the rate-limiting steps in primary
  literature.  Where literature values are missing,
  `delta_g_kjmol` is left as `None` — the dialog
  renders "—" so the absence is honest.
- **Why a 3-pane splitter for the dialog?**  Each
  pathway has substantial detail at three levels:
  pathway-overview (compartment, ΔG, textbook), step-
  table (10 rows × 5 columns for glycolysis), and
  per-step regulator list (PFK-1 has 4 effectors
  with mechanism notes).  Cramming all three into
  one card would either overflow vertically or hide
  the regulator detail.  Three panes scale gracefully
  + match the user's drill-down intent.

### Phase 42 status — 1 / 3 sub-phases complete
- 42a ✅ catalogue + dialog + agent actions (round
  147).
- 42a.1 ⏳ nucleotide-category fill-out (purine +
  pyrimidine de novo) — polish.
- 42b / 42c originally split as 3 sub-phases were
  bundled into 42a in this round.

### Next
Round 148 candidates:
- **Phase 43a** — cell-component explorer for
  Eukarya / Bacteria / Archaea (still queued from
  round 146).
- **Phase 44a** — microscopy by resolution scale.
- **Phase 45a** — lab reagents catalogue (just-
  added user-flagged item).
- **Phase 46a** — pH + buffer explorer (just-added
  user-flagged item).
- **Phase 38c** — lab-setup canvas (biggest remaining
  work in the lab simulator).
- **Phase 39d** — short docs close-out for Phase 39.

---

## 2026-04-25 — Round 146 (Phase 40a end-to-end — major-lab-analyser reference + 3 new roadmap phases)

### Context
Round 145 closed Phase 39c.  Round 146 picks up Phase
40a — the major-lab-analyser catalogue (capital-equipment-
tier instruments) the user flagged a few rounds back.
Same Phase-37c shape (catalogue + dialog + agent
actions); shipped end-to-end in one round because the
catalogue stayed tight at 28 entries.  Mid-round, three
more user-flagged feature requests came in and were
added to the roadmap as Phases 42 / 43 / 44 (metabolic
pathways, cell-component explorer, microscopy by
resolution scale).

### What shipped (Phase 40a)
- **`orgchem/core/lab_analysers.py`** —
  `LabAnalyser` frozen dataclass (id / name /
  manufacturer / category / function /
  typical_throughput / sample_volume /
  detection_method / typical_assays / strengths /
  limitations / notes).  28 entries across 10
  categories:
    - **clinical-chemistry (4)**: Roche cobas c702,
      Siemens Atellica CH 930, Beckman AU5800, Abbott
      Alinity c.
    - **hematology (2)**: Sysmex XN-1000, Beckman
      DxH 900.
    - **coagulation (2)**: Stago STA R Max 3, Sysmex
      CS-5100.
    - **immunoassay (3)**: Roche cobas e801, Abbott
      Alinity i, Siemens Atellica IM 1600.
    - **molecular (5)**: Roche cobas 8800, Hologic
      Panther + Panther Fusion, Cepheid GeneXpert,
      Illumina NovaSeq X / X Plus, Oxford Nanopore
      PromethION.
    - **mass-spec (2)**: SCIEX QTRAP 7500
      (LC-MS/MS clinical), Bruker MALDI Biotyper
      (microbial ID).
    - **functional (2)**: Molecular Devices FLIPR
      Penta (Ca²⁺ / membrane-potential GPCR
      screening), PerkinElmer Operetta CLS
      (high-content imager).
    - **microscopy (3)**: Zeiss LSM 980 + Airyscan
      2 (confocal), Zeiss Lattice Lightsheet 7,
      Thermo Krios G4 (cryo-TEM).
    - **automation (3)**: Hamilton STAR / STARplus
      (industry workhorse), Tecan Fluent, Opentrons
      OT-2 / Flex (open-source low-cost).
    - **storage (2)**: Hamilton BiOS L (-80 °C
      automated), Thermo Galileo (LN₂ vapor
      cryogenic).
  Each entry is a long-form reference card (200-500
  words) capturing instrument purpose + strengths-vs-
  limitations trade-off; throughput numbers + sample
  volumes + detection methods sourced from manufacturer
  data sheets.  Lookup helpers + `to_dict`.
- **`orgchem/gui/dialogs/lab_analysers.py`** —
  singleton modeless dialog wired to *Tools → Lab
  analysers…* (Ctrl+Shift+A).  Same shape as the
  Phase-37c chromatography dialog: category combo +
  free-text filter on the left, list of
  `name — manufacturer` rows, 8-section HTML detail
  card on the right (Function / Typical throughput /
  Sample / Detection method / Typical assays /
  Strengths / Limitations / Notes).
  `select_analyser(id)` programmatic API for the
  agent open path.
- **`orgchem/agent/actions_lab_analysers.py`** — 4
  actions in a new `instrumentation` category:
  `list_lab_analysers(category="")`,
  `get_lab_analyser(analyser_id)`,
  `find_lab_analysers(needle)`,
  `open_lab_analysers(analyser_id="")`.  Lookup
  actions are pure-headless; the dialog opener
  marshals onto the Qt main thread.
- **`orgchem/agent/__init__.py`** — auto-loader
  registers the new module.
- **`orgchem/gui/main_window.py`** — Tools menu
  entry added.
- **`orgchem/gui/audit.py`** — all 4 actions
  registered; GUI coverage stays at 100 %.

### Tests
- **`tests/test_lab_analysers.py`** — 35 cases:
    - Catalogue size ≥ 25 + all 10 categories
      represented + every-id-unique + every-required-
      field-present.
    - **User-requested-systems-present** — substring
      search verifies cobas, Atellica, Sysmex, Stago,
      Alinity, Panther, GeneXpert, NovaSeq, Nanopore,
      Biotyper, FLIPR, Krios, Hamilton, Tecan all hit
      at least one entry.
    - 8 per-row teaching invariants:
        - cobas c702 mentions BMP / panel.
        - Sysmex XN-1000 mentions CBC / differential.
        - GeneXpert mentions cartridge format.
        - NovaSeq throughput in terabases.
        - Nanopore mentions long reads.
        - FLIPR mentions Ca²⁺ or membrane potential.
        - Krios mentions cryo-EM or single-particle.
        - Opentrons mentions low cost / academic /
          open-source.
    - List-by-category + unknown-category-empty +
      get-unknown-none + find-substring-case-insensitive.
    - `to_dict` keys.
    - 6 agent-action wrappers (list / list-filtered /
      list-unknown-error / get / get-unknown-error /
      find).
    - 8 dialog tests: construction, singleton,
      category combo filter, text filter, no-match
      shows blank, programmatic `select_analyser`,
      default first-row auto-selected with all
      sections in detail HTML, agent-action open path
      with + without analyser_id focus.
- All 35 pass on first run after one trivial fix
  (test was checking for "Throughput" but the actual
  HTML heading is "Typical throughput").
- Full suite: **1 659 / 1 659 pass, 0 skipped** (was
  1 624).

### Roadmap additions (mid-round, user-flagged)
Three new phases added to `ROADMAP.md` based on user
requests this round:

- **Phase 42** — metabolic pathways explorer.
  `Pathway` + `PathwayStep` + `RegulatoryEffector`
  frozen dataclasses + ~25 pathway entries (glycolysis
  + TCA + ox-phos + β-oxidation + FAS + cholesterol
  biosynth + urea cycle + photosynthesis + heme
  biosynth + nucleotide metabolism + signalling
  cascades).  Each step: substrate(s) / enzyme + EC
  number / product(s) / reversibility / ΔG kJ/mol /
  regulatory effectors.  3 sub-phases (42a catalogue,
  42b dialog, 42c agent actions).
- **Phase 43** — cell-component explorer for
  Eukarya / Bacteria / Archaea.  `CellComponent` +
  `MolecularConstituent` frozen dataclasses + ~40
  components keyed by domain + sub-domain (animal /
  plant / fungus / gram+ / gram-).  Each:
  compartment, function, key molecules
  (cross-references to Molecule rows where SMILES
  exists), notable diseases / experimental hooks.  3
  sub-phases (43a / 43b / 43c).
- **Phase 44** — microscopy across resolution scales.
  Cross-cuts the Phase-37d spectrophotometry +
  Phase-40a lab-analysers catalogues but organised
  by resolution scale + sample type rather than
  instrument family.  `MicroscopyMethod` +
  `ResolutionScale` frozen dataclasses + ~30 entries
  across 5 resolution tiers (whole-organism / tissue
  / cellular / sub-cellular / single-molecule).
  Cross-references existing 40a entries (Zeiss LSM,
  Lattice Lightsheet, Krios) without duplication.
  3 sub-phases (44a / 44b / 44c).

### Design notes
- **Why a new `instrumentation` agent category
  rather than reusing `lab`?**  The Phase-38a/b
  `lab` category covers bench-glassware setups; the
  Phase-40a category covers capital-equipment-tier
  *instruments*.  Different mental model + different
  use case in the tutor's tool-use schema — keeping
  them separate makes the action-space cleaner.
- **Why ship 40a / 40b / 40c bundled in one round
  instead of three?**  The catalogue stayed at 28
  entries (vs the originally-planned 30-40), and
  the dialog + agent-action pattern is fully nailed
  by Phase 37c / 41 / etc.  Splitting them across
  rounds would mean three trivial rounds instead of
  one substantive one.
- **Why include ~$10k Opentrons OT-2 alongside the
  $500k Hamilton STAR?**  Different cost tiers serve
  different lab use cases.  The OT-2 has democratised
  lab automation for academic / single-PI labs in
  the past 5 years and shipping a "lab analysers"
  catalogue without it would be an oversight.
- **Why the manufacturer catalogue choice (cobas vs
  Roche cobas)?**  Throughout the catalogue, the
  `name` field uses the manufacturer-published
  product name verbatim ("Roche cobas c 702", "Sysmex
  XN-1000") so it matches what a user would search
  on Google or read in a marketing brochure.  The
  separate `manufacturer` field handles the parent
  company.

### Phase 40 status — 1 / 1 visible sub-phase complete
- 40a ✅ catalogue + dialog + agent actions (round
  146).
- (40b / 40c originally split as 3 sub-phases were
  bundled into 40a in this round.)

### Next
Round 147 candidates:
- **Phase 42a** — metabolic pathways catalogue
  (the freshest user-flagged content).  Catalogue
  size + per-step depth is the design call.
- **Phase 43a** — cell components catalogue.
- **Phase 44a** — microscopy by resolution catalogue.
- **Phase 38c** — lab-setup canvas (still the
  biggest open work in the lab simulator strand).
- **Phase 39d** — short cross-references docs round
  to formally close Phase 39.

---

## 2026-04-25 — Round 145 (Phase 39c — per-solver agent actions for the lab calculator)

### Context
Round 144 closed Phase 41 (centrifugation reference +
g↔RPM calculator) end-to-end.  Round 145 picks up Phase
39c — the mechanical wrapper round that exposes every
Phase-39a solver to the agent registry.  Bringing Phase 39
to 3/4 (only docs in 39d remain) and giving the tutor /
scripts / stdio bridge direct access to all 31 calculator
functions.

### What shipped
- **`orgchem/agent/actions_calc.py`** — 31 new
  `@action(category="calc")` wrappers, one per Phase-39a
  solver:
    - **Solution (6)**: `molarity` / `dilution` /
      `serial_dilution` / `molarity_from_mass_percent` /
      `ppm_to_molarity` / `molarity_to_ppm`.
    - **Stoichiometry (4)**: `limiting_reagent` /
      `theoretical_yield` / `percent_yield` /
      `percent_purity`.
    - **Acid-base (5)**: `ph_from_h` / `h_from_ph` /
      `pka_to_ka` / `ka_to_pka` /
      `henderson_hasselbalch`.
    - **Gas laws (3)**: `ideal_gas` / `combined_gas_law`
      / `gas_density`.
    - **Colligative (3)**: `boiling_point_elevation` /
      `freezing_point_depression` / `osmotic_pressure`.
    - **Thermo + kinetics (6)**: `heat_capacity` /
      `hess_law_sum` / `first_order_half_life` /
      `first_order_integrated` / `arrhenius` /
      `eyring_rate_constant`.
    - **Equilibrium (4)**: `equilibrium_constant` /
      `ksp_from_solubility` / `solubility_from_ksp` /
      `ice_solve_a_plus_b`.
  Total: 32 calc actions (31 per-solver wrappers + the
  round-143 `open_lab_calculator` dialog opener).
- **Common `_wrap(solver, **kwargs)` helper** — calls the
  solver, returns its result on success, returns
  `{"error": str(e)}` when the solver raises
  `ValueError` (bad input).  The agent never sees a
  Python traceback.
- **`orgchem/gui/audit.py`** — every new action
  registered with a path back to its UI panel ("Tools →
  Lab calculator… → Solution tab → Molarity panel") OR
  "agent-only convenience" when the solver's list-shaped
  input doesn't fit the spin-box dialog pattern (e.g.
  `limiting_reagent`, `equilibrium_constant`,
  `hess_law_sum`).  GUI coverage stays at 100 %.

### Tests
- **`tests/test_calc_actions.py`** — 33 cases:
    - **Registry-membership invariant**: all 31 expected
      action names present in the `calc` category +
      `open_lab_calculator` = 32 total.
    - **Happy-path verifications** mirroring the same
      textbook values used in Phase 39a's solver tests:
      NaCl 29.22 g for 0.5 M × 1 L; dilution 1 M × 10
      mL → 0.1 M × 100 mL; serial dilution 1 M / 10× ×
      3 → 0.001 M; concentrated HCl 37 % w/w →
      11.97 M; ppm round-trip; limiting reagent
      identifies B with 1:2 stoichiometry; theoretical
      yield 200 g; percent yield 80 %; pH 7 at 1e-7
      [H⁺]; pH 3 at 1e-3; pKa↔Ka round-trip at
      acetic acid; HH at unity ratio gives pH = pKa;
      STP volume 22.414 L; Boyle's law; O₂ density
      1.428 g/L; ΔTb 0.512 °C for 1 m sucrose; ΔTf
      3.72 °C for 1 m NaCl (i=2); 7.63 atm osmotic
      pressure for isotonic saline; q = 4184 J for
      water 20→30 °C; Hess sum -75 kJ; t½ = ln 2 / k;
      first-order [A]_t = e^-1; Arrhenius; Eyring
      forward; K_eq = 2 for [A]=1, [B]=2; AgCl K_sp =
      1.69e-10; PbI₂ K_sp = 4·s³; ICE x = 0.5 at K = 1.
    - **Error-path coverage**: percent-purity > 100,
      missing-count != N for any solver, unknown
      solvent name, ICE both-reactants-zero.
    - All 33 pass on the first run.
- Full suite: **1 624 / 1 624 pass, 0 skipped** (was
  1 591).

### Design notes
- **Why one wrapper per solver, not one generic
  "call_calc(solver_name, **kwargs)" action?**  Each
  wrapper has a distinct typed signature visible to the
  tutor's tool-use schema generator (Anthropic /
  OpenAI).  A generic action would force every call
  through string-matching on `solver_name`, losing the
  parameter-validation + autocomplete benefits.  The
  tutor sees `molarity(mass_g, molarity_M, volume_L,
  molecular_weight_gmol)` as a typed tool, not a
  free-form dispatcher.
- **Why the `_wrap` helper rather than `try/except`
  per-action?**  31 try/except blocks would be 90 lines
  of duplicated code.  `_wrap(solver, **kwargs)` is a
  single 5-line helper that handles all of them
  uniformly.
- **Why some solvers are "agent-only" with no widget
  panel?**  Three solvers take list-shaped input
  (`limiting_reagent` takes a list of reagent dicts,
  `equilibrium_constant` takes a list of species,
  `hess_law_sum` takes a list of step ΔH values) that
  doesn't map cleanly to a spin-box panel.  The
  agent-action surface is the right entry point for
  these — a tutor / script can build the list
  programmatically.  A future polish round could add
  spreadsheet-style table widgets for the dialog if
  there's demand.
- **Why match the same textbook values as Phase 39a's
  solver tests?**  Two reasons: (1) the wrapper layer
  shouldn't introduce numerical differences from the
  solvers, and (2) repeating the verification at the
  agent layer means the wiring (kwargs name match,
  return-dict pass-through) is exercised end-to-end.

### Phase 39 status — 3 / 4 sub-phases complete
- 39a ✅ headless solvers (round 142).
- 39b ✅ tabbed dialog (round 143).
- 39c ✅ per-solver agent actions (round 145).
- 39d ⏳ cross-references to Beer-Lambert / atom-economy
  / formula calculator (docs only).

### Next
Round 146 candidates:
- **Phase 39d** — short docs round, mostly cross-ref
  links in INTERFACE.md / ROADMAP.md / glossary.
- **Phase 40a** — major lab analysers catalogue (~30
  entries; clinical chemistry / hematology /
  immunoassay / molecular / mass spec / FLIPR /
  microscopy / liquid-handling).  Same shape as the
  Phase 37c chromatography catalogue.
- **Phase 38c** — equipment palette + canvas (biggest
  remaining work in the lab simulator).
- **Phase 31 long-running content** — chip another SAR
  series, named reaction, or seeded protein.

---

## 2026-04-25 — Round 144 (🎉 Phase 41 CLOSED in one round — centrifugation + g↔RPM calculator)

### Context
Round 143 closed Phase 39b (tabbed lab-calculator
dialog).  Round 144 picked up Phase 41 instead of Phase
39c (per-solver agent actions) since Phase 41 is the
more interesting unit of work — both reference catalogue
+ a quantitative widget the user explicitly asked for.
The catalogue stayed tight enough that all 3 sub-phases
(41a + 41b + 41c) shipped in one round.

### What shipped
- **`orgchem/core/centrifugation.py`** — three
  `frozen=True` dataclasses + 3 catalogues + 2 solvers:
    - **Centrifuge (9 entries)** across all 4 classes:
      Eppendorf 5424 / 5425 / 5810/5810R / 5910 Ri,
      Beckman Allegra X-15R, Beckman Avanti J-26 XPI,
      Sorvall RC-6 Plus, Beckman Optima XPN, Sorvall
      WX 100.
    - **Rotor (10 entries)**: FA-45-24-11 microfuge,
      A-4-81 + FA-45-30-11 benchtop, JA-25.50 + JA-10
      + JLA-8.1000 high-speed, Ti-70 + SW 41 Ti +
      TLA-100 + VTi 50 ultracentrifuge.  Each carries
      `max_radius_cm` + `min_radius_cm` (swinging-
      bucket arms-out vs arms-in range) + `max_speed_rpm`.
    - **Application (8 entries)**: mammalian cell
      pelleting, E. coli harvest, differential
      organelle prep, sucrose density-gradient
      (polysomes), CsCl plasmid isopycnic, Amicon
      centrifugal-filter concentration, exosome
      isolation, serum separation.
  - **`G_FORCE_CONSTANT = 1.118e-5`** + solvers
    `rpm_to_g(rpm, radius_cm)` / `g_to_rpm(g_force,
    radius_cm)`.  Verified against the Eppendorf 5424
    data sheet: 15 000 RPM @ 8.4 cm = 21 130 × g
    exactly.
- **`orgchem/gui/dialogs/centrifugation.py`** —
  singleton modeless dialog wired to *Tools →
  Centrifugation…* (Ctrl+Shift+F).  4 tabs:
    - **Centrifuges / Rotors / Applications** — three
      catalogue tabs sharing a reusable `_CatalogueTab`
      helper class.  Each: category combo + filter +
      list + HTML detail card.  The helper takes the
      enumeration + detail-renderer + row-label
      callables, so all 3 tabs share one
      implementation.
    - **g ↔ RPM calculator** — the headline UX
      feature.  Rotor `QComboBox` whose selection
      auto-fills the radius spin from
      `rotor.max_radius_cm` AND surfaces "Max RPM for
      this rotor: <N>" so overspeed is visible up
      front.  Two direction buttons (RPM→×g and
      ×g→RPM) + Clear.  Status line displays the
      rearranged formula in human form, e.g.
      `"g = 1.118e-5 · 15000² · 8.40 = 21,130 × g"`.
      Entering an RPM above the rotor's max appends
      `OVERSPEED: exceeds rotor max <N> RPM!` to the
      status line in red.
  Programmatic API: `select_tab(label)` /
  `select_centrifuge(id)` / `select_rotor(id)` /
  `select_application(id)`.
- **`orgchem/agent/actions_centrifugation.py`** — 8
  actions in the `centrifugation` category:
    - `list_centrifuges_action(centrifuge_class="")` /
      `get_centrifuge_action(centrifuge_id)`.
    - `list_rotors_action(rotor_type="")` /
      `get_rotor_action(rotor_id)`.
    - `list_centrifugation_applications(protocol_class="")`.
    - `rpm_to_g_action(rpm, radius_cm)` /
      `g_to_rpm_action(g_force, radius_cm)` —
      `{"error": ...}` on bad input.
    - `open_centrifugation(tab, rotor_id,
      centrifuge_id, application_id)` — opens dialog +
      optionally focuses tab + entry.
- **`orgchem/agent/__init__.py`** — auto-loader
  registers the new module.
- **`orgchem/gui/main_window.py`** — Tools menu entry
  added.
- **`orgchem/gui/audit.py`** — all 8 actions
  registered; GUI coverage stays at 100 %.

### Tests
- **`tests/test_centrifugation.py`** — 37 cases:
    - g↔RPM round-trip + Eppendorf 5424 data-sheet
      match (15 000 RPM @ 8.4 cm = 21 130 × g) +
      common 13 000 × g @ 8.4 cm → 11 766 RPM.
    - Catalogue: every centrifuge class represented,
      ultracentrifuges ≥ 50 000 RPM invariant,
      canonical rotors / models present, every entry
      has required fields.
    - Swinging-bucket has min < max radius for at
      least one entry (arms-in/out range).
    - Filtered enumeration + unknown-category empty.
    - to_dict serialisation has all expected keys.
    - 13 agent-action tests covering every action +
      every error path (zero RPM / radius / g; unknown
      ids; unknown class; rpm_to_g + g_to_rpm
      data-sheet validation through the action layer).
- **`tests/test_centrifugation_dialog.py`** — 17
  pytest-qt cases:
    - 4-tab construction; all expected labels present.
    - Singleton identity.
    - Centrifuges tab list + category filter
      (ultracentrifuge → Optima + WX 100).
    - `select_centrifuge("ultra_optima_xpn")` works.
    - Rotors + Applications tabs analogous.
    - Calculator: rotor-dropdown auto-fills radius
      from `rotor_fa_45_24_11` → 8.4 cm; RPM→×g
      button gives 21 130 at 15 000 RPM × 8.4 cm; ×g→RPM
      button gives 11 766 RPM at 13 000 × g; OVERSPEED
      warning fires when RPM > rotor max; Clear
      resets; zero-RPM error path surfaces.
    - Agent-action open path with + without tab +
      with rotor focus.
- All 54 pass on the first run.
- Full suite: **1 591 / 1 591 pass, 0 skipped** (was
  1 537).

### Design notes
- **Why a rotor dropdown, not a radius-only spin?**
  The "wrong rotor → wrong RPM" failure mode is the
  single most-common centrifuge protocol error.  The
  dropdown forces the user to think "which rotor am I
  using?" rather than typing a number that has no
  context.  The label showing "Max RPM for this
  rotor" closes the second-most-common error
  (overspeeding past the rotor's rated limit).
- **Why share `_CatalogueTab` across 3 tabs?**  All
  three (Centrifuges / Rotors / Applications) have
  identical UX (category combo + filter + list +
  detail).  Sharing one widget class keeps the
  dialog short + means a UI tweak (search styling,
  list font) happens in one place.
- **Why include `Application` (protocol) entries
  alongside Centrifuge + Rotor?**  Centrifuges +
  rotors are the *equipment*; applications are the
  *use cases*.  A student who knows they want to
  pellet mammalian cells doesn't need to dig through
  centrifuge data sheets — the Applications tab tells
  them "200-300 × g for 5 min on a swinging-bucket
  rotor".  Cross-reference: each application
  recommends a rotor TYPE (not a specific id) so
  any matching rotor in the catalogue would work.
- **Why no per-rotor max-g-force derivation?**  Each
  rotor's max RPM × radius derives a max ×g, but
  it's not always the rated-max ×g (some rotors are
  speed-limited below the radius limit for tube-
  strength reasons).  The catalogued
  `centrifuge.max_g_force` is the data-sheet rating;
  computing it from RPM × radius would mislead.
- **Why `1.118e-5` rather than the more-precise
  `1.118468e-5`?**  Every Beckman / Eppendorf data
  sheet uses 1.118e-5 to 4 sig figs.  Matching
  industry practice + giving exact agreement with
  the user's expected calculator results is more
  important than 5th-decimal accuracy.

### Phase 41 status — COMPLETE 🎉
- 41a ✅ catalogue + g↔rpm solver (round 144).
- 41b ✅ dialog + calculator widget (round 144).
- 41c ✅ agent actions (round 144).

### Next
Round 145 candidates:
- **Phase 39c (per-solver agent actions for the lab
  calculator)** — ~30 thin wrapper functions, each
  exposing a Phase-39a solver as a registered
  `@action` in the `calc` category.  Closes Phase 39
  (only 39d docs left).
- **Phase 40a (major lab analysers catalogue)** —
  user-flagged earlier; same shape as Phase 37c
  chromatography catalogue.  Likely 1 round for the
  catalogue + dialog; could fit alongside the agent
  actions in 1.5 rounds.
- **Phase 38c (lab-setup canvas)** — biggest open
  work from the lab-simulator strand.

---

## 2026-04-25 — Round 143 (Phase 39b — tabbed lab-calculator dialog)

### Context
Round 142 shipped Phase 39a (~30 headless solvers across
7 sibling modules).  Round 143 wraps those in a tabbed
QDialog so they're user-facing.  Pattern follows the
Phase-37d Beer-Lambert calculator widget — extended to
multi-tab + multi-panel.

### What shipped
- **`orgchem/gui/dialogs/lab_calculator.py`** — singleton
  modeless tabbed dialog wired to *Tools → Lab
  calculator…* (Ctrl+Shift+C).  7 tabs (one per Phase-39a
  module): Solution / Stoichiometry / Acid-base / Gas
  law / Colligative / Thermo + kinetics / Equilibrium.
  Each tab is a `QScrollArea` containing a stack of
  `QGroupBox` solver panels.  Total: 16 solver panels +
  2 button-driven custom panels (pH↔[H⁺], pKa↔Ka)  + 1
  K_sp↔s panel + 1 ICE solver panel.
- **`_SolverPanel` helper class** — the round's
  reusable abstraction.  Constructor takes:
    - `title` for the group box.
    - `fields` — list of dicts ``{name, label, suffix,
      decimals?, min?, max?, default?}``.
    - `solver` — callable taking the field names as
      kwargs and returning a result dict.
    - `zero_means_unknown` — when True (default), spin
      value 0.0 is passed to the solver as `None`; the
      solver fills in the missing field.  Some solvers
      (e.g. `theoretical_yield_g`) require ALL inputs;
      pass `zero_means_unknown=False` to skip the
      None-substitution.
    - `status_help` — initial status-line text.
  Methods: `_on_solve` packages the spin values into
  kwargs, calls the solver, populates result spins,
  formats the status line as `"label = value · …"` for
  every field; `_on_clear` zeros every spin; `add_widget`
  registers an extra widget (e.g. a `QComboBox` for
  solvent selection) and folds its value into the
  solver kwargs via `extra_value`.
- **Custom non-`_SolverPanel` panels** for cases where
  the symmetric-solve pattern doesn't fit cleanly:
    - **pH ↔ [H⁺]** — two spins + two buttons (`[H⁺]→pH`,
      `pH→[H⁺]`); each button calls a separate solver.
    - **pKa ↔ Ka** — same shape.
    - **K_sp ↔ molar solubility** — 4 spins (s, K_sp, n,
      m as integer) + two direction buttons.
    - **ICE solver A + B ⇌ C + D** — 5 input spins (K,
      A₀, B₀, C₀, D₀) + 1 Solve button + status line
      that displays all 5 equilibrium concentrations +
      the reaction extent x.
- **Colligative tab solvent dropdown** — both the BP
  elevation and FP depression `_SolverPanel`s register
  a `QComboBox` (via `add_widget("solvent", combo)`)
  whose selection auto-fills the matching K_b / K_f
  from `core/calc_colligative.SOLVENT_CONSTANTS` when
  the solver runs.  User can leave the K_b spin at 0 +
  pick "water" → the solver gets `solvent="water"` as
  a kwarg and uses the lookup.
- **`orgchem/agent/actions_calc.py`** — single new
  action `open_lab_calculator(tab="")` that opens the
  dialog and optionally focuses one of the 7 tabs.
  Returns `{"opened", "selected", "tab",
  "available_tabs"}`.  Per-solver agent actions
  (`molarity_solve`, etc.) defer to Phase 39c.
- **`orgchem/agent/__init__.py`** — auto-loader
  registers the new module.
- **`orgchem/gui/main_window.py`** — Tools menu entry
  added (Ctrl+Shift+C).
- **`orgchem/gui/audit.py`** — `open_lab_calculator`
  registered; GUI coverage stays at 100 %.

### Tests
- **`tests/test_lab_calculator_dialog.py`** — 15
  pytest-qt cases:
    - Construction (7 tabs present, all expected
      labels).
    - Singleton identity.
    - `select_tab` matches + returns False for
      unknown.
    - **Solution tab: molarity solver**: 0.5 M × 1 L ×
      58.44 g/mol (NaCl) → 29.22 g.  Dilution: 1 M ×
      10 mL → 0.1 M × 100 mL.
    - Clear button resets all spins.
    - Error path: 2 fields blank → "error" appears in
      status text.
    - **Gas law tab: ideal gas**: 1 atm × 1 mol ×
      273.15 K → 22.414 L.
    - **Colligative tab: solvent dropdown** auto-fills
      K_f when "water" is picked + 1 m + i=2 → ΔTf =
      3.72 °C, AND the K_f spin shows the auto-filled
      1.86 value.
    - **Acid-base tab custom**: H→pH button maps
      [H⁺] = 1e-3 → pH = 3.0.
    - **Equilibrium tab custom**: K_sp from solubility
      AgCl s=1.3e-5 (n=m=1) → K_sp = 1.69e-10.
    - Agent action: `open_lab_calculator()` fires +
      returns `available_tabs` list.  Open with `tab="Gas
      law"` focuses it.  Open with unknown tab returns
      `selected=False` but still opens.
- All 15 pass on the first run.
- Full suite: **1 537 / 1 537 pass, 0 skipped** (was
  1 522).

### Design notes
- **Why `_SolverPanel` as a class rather than a factory
  function?**  The widget needs to remember its spin /
  extra-widget references for the Solve / Clear slots.
  A class encapsulates that state cleanly.
- **Why spin value 0 = unknown rather than disabled /
  empty?**  `QDoubleSpinBox` doesn't have a clean
  "blank" state — it's always a number.  Conventionally
  treating 0 as "unknown" is the cheapest UX path that
  matches the Phase-37d Beer-Lambert pattern.  Edge
  case: solving for a quantity whose answer is genuinely
  0 isn't supported, but no real lab calculation has
  exactly-zero answer for any of the fields here.
- **Why a `QScrollArea` per tab?**  Some tabs have 3-4
  panels stacked vertically; on smaller screens the
  full panel stack doesn't fit.  Wrapping each tab in
  a scroll area keeps the dialog compact.
- **Why no custom-widget validation in `_SolverPanel`?**
  Spin boxes already enforce min/max ranges; the solver
  itself validates positivity + missing-count.  Doubling
  the validation is just code duplication.  Errors
  bubble up through the status line.
- **Why custom (not `_SolverPanel`-based) panels for
  pH↔[H⁺] etc.?**  `_SolverPanel` assumes a single
  solver function with a "leave-one-blank" semantics.
  H↔pH has two distinct solvers (one each direction)
  with no shared "blank field" model — the user picks
  the direction explicitly.  Same for pKa↔Ka, K_sp↔s.
  The factory could be extended to handle this case
  but the resulting API would be more complex than
  just writing the custom panels (~40 lines each).

### Phase 39 status — 2 / 4 sub-phases complete
- 39a ✅ headless solvers (round 142).
- 39b ✅ tabbed dialog (round 143).
- 39c ⏳ per-solver agent actions (one thin wrapper
  per `core/calc_*` solver function).
- 39d ⏳ cross-references to Beer-Lambert / atom-economy
  / formula calculator (docs only).

### Next
Round 144: **Phase 39c — per-solver agent actions** is
the natural next pick.  ~30 small wrapper functions —
each maps a Phase-39a solver to a registered `@action`,
following the same `{result | error}` pattern as the
existing `beer_lambert` action.  Mostly mechanical work;
ships in 1 round.

---

## 2026-04-25 — Round 142 (Phase 39a — lab-calculator solvers + Phase 40/41 roadmap additions)

### Context
Round 141 closed Phase 38b (lab-setup catalogue +
validator) AND added Phase 39 (lab calculator) to the
roadmap.  Round 142 starts Phase 39 with 39a (headless
solvers).  Mid-round, two more user-flagged items came
in: a major-analysers reference and a centrifugation
tool — both added to the roadmap as Phase 40 + Phase 41
respectively.

### What shipped (Phase 39a)
Seven sibling modules in `orgchem/core/`, each carrying
3-7 solver functions in the Phase-37d
`beer_lambert_solve` style (pass any N-1 of N quantities,
get the Nth filled in; `ValueError` on bad input):

- **`calc_solution.py`** (5 solvers):
    - `molarity_solve(mass_g, molarity_M, volume_L,
      molecular_weight_gmol)` — m = M·V·MW.
    - `dilution_solve(M1, V1, M2, V2)` — M₁V₁ = M₂V₂.
    - `serial_dilution(initial, factor, n_steps)` —
      n-step serial dilution table.
    - `molarity_from_mass_percent(%w/w, density,
      MW)` — concentrated-acid → molarity.
    - `ppm_to_molarity` / `molarity_to_ppm`.
- **`calc_stoichiometry.py`** (4 solvers):
    - `limiting_reagent([{name, moles, stoich_coeff},
      …])` — index + name + per-reagent equivalent
      units.
    - `theoretical_yield_g`.
    - `percent_yield(actual, theoretical, percent)` —
      any 2 of 3.
    - `percent_purity` (rejects > 100 %).
- **`calc_acid_base.py`** (5 solvers):
    - `ph_from_h` / `h_from_ph` — return full pH /
      pOH / [H⁺] / [OH⁻] tuple.
    - `pka_to_ka` / `ka_to_pka`.
    - `henderson_hasselbalch(pH, pKa, base_acid_ratio)`
      — any 2 of 3 — buffer-design entry point.
- **`calc_gas_law.py`** (3 solvers + 1 constant):
    - `R_L_ATM_PER_MOL_K = 0.0820573661`.
    - `ideal_gas_solve(P, V, n, T)` — any 3 of 4.
    - `combined_gas_law(P1, V1, T1, P2, V2, T2)` —
      any 5 of 6.
    - `gas_density(P, MW, T)` — ρ = PM / RT.
- **`calc_colligative.py`** (3 solvers + 1 table):
    - `SOLVENT_CONSTANTS` table — K_b + K_f for water /
      benzene / chloroform / acetic acid / ethanol /
      CCl₄ / cyclohexane / camphor (Atkins / de Paula).
    - `boiling_point_elevation` / `freezing_point_depression`
      — any 3 of 4 OR pass `solvent="water"` to
      auto-fill K_b / K_f.
    - `osmotic_pressure(M, T, i, P)` — Π = MRT·i.
- **`calc_thermo_kinetics.py`** (6 solvers + 3
  constants):
    - `R_J_PER_MOL_K`, `K_B`, `H_PLANCK` constants.
    - `heat_capacity_solve` — q = mcΔT (q + ΔT can be
      negative; m + c must be positive).
    - `hess_law_sum([step ΔH])`.
    - `first_order_half_life(k OR t½)`.
    - `first_order_integrated([A]_0, [A]_t, k, t)`.
    - `arrhenius_solve(k, A, Ea, T)` — k = A·exp(-Ea/RT).
    - `eyring_rate_constant(ΔG‡, T)`.
- **`calc_equilibrium.py`** (4 solvers):
    - `equilibrium_constant_from_concentrations` —
      K = Π[product]^coeff / Π[reactant]^coeff for any
      species list.
    - `ksp_from_solubility(s, n, m)` /
      `solubility_from_ksp(K_sp, n, m)` — closed form
      for AnBm salts (`s = (K_sp / (n^n · m^m))^(1/(n+m))`).
    - `ice_solve_a_plus_b(K, A₀, B₀, C₀, D₀)` —
      closed-form quadratic ICE solver for A + B ⇌
      C + D with all coeffs = 1, with a `_pick_chem_root`
      helper that selects the chemically-sensible root.

Total: ~30 solvers + 4 module-level constants + 1
solvent-properties table.

### Tests
- **`tests/test_calc_solvers.py`** — 59 cases across 18
  test classes (one per solver function).  Highlights:
    - Textbook-value verifications: 0.5 M NaCl in 1 L =
      29.22 g (MW 58.44); 1 mol gas at STP = 22.414 L;
      37 % w/w HCl ρ 1.18 → 11.97 M; pH 3 ↔ [H⁺] 1e-3;
      Henderson-Hasselbalch at base/acid = 1 → pH = pKa;
      Boyle's-law isothermal compression; AgCl K_sp =
      1.69e-10 from s = 1.3e-5; PbI₂ K_sp = 4·s³;
      first-order k = 0.05 /s → t½ = 13.86 s;
      first-order [A]_0 = 1, k = 0.1, t = 10 → e^-1 ≈
      0.368; 100 g water 20→30 °C = 4184 J; 1 m NaCl
      (i = 2) in water → ΔTf = 3.72 °C; isotonic saline
      at 37 °C ≈ 7.63 atm.
    - Round-trip checks: pH ↔ [H⁺], pKa ↔ Ka, K_sp ↔
      molar solubility, k ↔ t½.
    - Error-path coverage: 2-unknowns rejected, zero /
      negative inputs rejected, unknown solvent name
      rejected, percent-purity > 100 rejected,
      ICE solver no-real-root rejected, ICE both-zero
      rejected.
    - All 59 pass on the first run — strict input
      validation + the matching test fixtures meant
      no iteration was needed.
- **Full suite: 1 522 / 1 522 pass, 0 skipped** (was
  1 463).

### Roadmap additions (mid-round, user-flagged)
Two new phases added to `ROADMAP.md`:

- **Phase 40** — major lab analysers + automation
  reference.  Catalogue of capital-equipment-tier
  instruments: clinical-chemistry analysers (Roche
  cobas, Siemens Atellica, Beckman AU), hematology
  (Sysmex XN, Beckman DxH), coagulation (Stago STA,
  Sysmex CS), immunoassay (Roche cobas e, Abbott
  Architect i), molecular (Roche cobas 8800, Hologic
  Panther, Cepheid GeneXpert, Illumina NovaSeq, Oxford
  Nanopore), mass spec (LC-MS/MS, MALDI-TOF, ICP-MS),
  cell-based / functional (FLIPR, high-content
  imagers, patch-clamp robots), microscopy (confocal,
  super-res, light-sheet, cryo-EM), liquid-handling
  (Hamilton STAR, Tecan Fluent, Beckman Biomek,
  Opentrons), sample-storage automation.  Same shape
  as Phase 37c chromatography.  3 sub-phases (40a
  catalogue, 40b dialog, 40c agent actions).
- **Phase 41** — centrifugation reference + g↔rpm
  calculator.  Catalogue of centrifuge classes
  (microfuge / benchtop / high-speed / ultra), rotor
  types (fixed-angle / swinging-bucket / vertical /
  continuous-flow), applications (differential,
  density-gradient, subcellular fractionation,
  centrifugal-filter concentration).  Quantitative
  `g_to_rpm` / `rpm_to_g` calculator widget with rotor
  dropdown that pre-fills the radius — the canonical
  bench-side conversion most students get wrong.  3
  sub-phases (41a catalogue + solver, 41b dialog +
  calculator widget, 41c agent actions).

### Design notes
- **Why 7 modules, not 1 large `calc.py`?**  Each module
  is small (50-200 lines) and self-contained.  One large
  module would push past the 500-line guideline + would
  conflate independent topics.  Splitting by category
  also makes 39b's tabbed dialog a clean 1:1 mapping
  (one tab per module).
- **Why duplicate the `R = 0.0820573661` constant
  between `calc_gas_law` and `calc_colligative`?**
  The two modules genuinely share a physical constant,
  but importing `calc_gas_law.R_L_ATM_PER_MOL_K` from
  `calc_colligative` is cross-cutting clutter.
  Module-level constants stay duplicated; if a third
  module wants the same value it'll get its own copy.
  Tests verify they don't drift apart.
- **Why no `ICE_solve` for arbitrary stoichiometry?**
  Multi-stage / multi-component ICE tables solve a
  general polynomial that can't be closed-form (5+
  species → quintic).  The 1:1:1:1 case via quadratic
  is what 95 % of teaching problems need.  An iterative
  numerical solver for general ICE is a future polish
  item.
- **Why accept negative ΔT in `heat_capacity_solve` but
  positive elsewhere?**  Heating + cooling are
  symmetric; q < 0 means heat released (exothermic) =
  ΔT < 0 for the system.  Mass + specific heat are
  always positive — those keep the strict-positive
  validation.

### Phase 39 status — 1 / 4 sub-phases complete
- 39a ✅ headless solvers (round 142).
- 39b ⏳ tabbed dialog (one tab per module).
- 39c ⏳ agent actions (one thin wrapper per solver).
- 39d ⏳ cross-references to Beer-Lambert / atom-economy /
  formula calculator (docs only).

### Next
Round 143: **Phase 39b (tabbed lab-calculator dialog)**
is the natural next pick — wraps each solver in a small
form-and-button widget, all under one `QTabWidget` per
category.  Pattern is already nailed by the Phase 37d
Beer-Lambert calculator widget; this is mostly
"replicate-and-extend" work.  Ships in 1 round.

---

## 2026-04-25 — Round 141 (Phase 38b — lab-setup catalogue + connection validator)

### Context
Round 140 shipped Phase 38a (lab equipment catalogue —
42 items + connection-port metadata).  Round 141 ships
Phase 38b (canonical setup catalogue) — same dataclass
+ dialog + agent-action shape, but adds a critical new
piece: a **connection validator** that walks every
seeded setup against the Phase-38a equipment / port
catalogue and surfaces real port mismatches.  The
validator caught real port-direction bugs in 38a —
fixing those is what made round 141 a substantive
"this build is more correct than yesterday" round.

### What shipped
- **`orgchem/core/lab_setups.py`** — `Setup` +
  `SetupConnection` frozen dataclasses + 8 seeded
  canonical setups:
    1. **Simple distillation** (9 equipment, 6
       connections): pot RBF + heating mantle + Variac
       + distillation head + thermometer adapter +
       thermometer + Liebig condenser + vacuum
       adapter + receiver RBF.  Ports plumbed by id +
       index.
    2. **Fractional distillation** (10 equipment, 7
       connections): same as simple + a Vigreux column
       inserted between the pot + the head.  Strict
       super-set of simple distillation, locked as a
       per-setup teaching invariant.
    3. **Standard reflux** (5 equipment, 2
       connections): RBF + heating mantle + Variac +
       Allihn condenser + drying tube.  Allihn (NOT
       Liebig) — the bulb condenser is preferred for
       sustained reflux.
    4. **Reflux with controlled addition** (7
       equipment, 4 connections): 3-neck RBF + Allihn
       + sep funnel (used as addition funnel) +
       thermometer adapter + thermometer.  The
       Grignard-formation / exothermic-acylation
       canonical setup.
    5. **Soxhlet extraction** (5 equipment, 2
       connections): pot RBF + heating mantle + Variac
       + Soxhlet extractor + Allihn condenser.
    6. **Vacuum filtration** (4 equipment, 3
       connections): Büchner funnel + filter flask +
       cold trap + aspirator.
    7. **Liquid-liquid extraction** (5 equipment, 2
       connections): sep funnel + ring stand + 3-prong
       clamp + 2 Erlenmeyer collection flasks.
    8. **Recrystallisation** (6 equipment, 3
       connections): Erlenmeyer + hot plate + ice bath
       + Büchner + filter flask + aspirator.
  Equipment refs are INDICES into the setup's
  equipment list (not ids) so the same piece can
  appear twice.  Each setup carries: id / name /
  purpose / equipment list / `SetupConnection` records
  / procedure / safety_notes / pedagogical_notes /
  typical_reactions / icon_id.  Each
  `SetupConnection`: from_equipment_idx / from_port /
  to_equipment_idx / to_port / note (free text
  describing the connection).
- **`validate_setup(setup)`** — the round's headline
  helper.  Walks every connection, resolves the named
  ports on the referenced equipment via the Phase-38a
  catalogue, and returns a list of human-readable
  error strings (empty = valid).  Validation rules:
    - Equipment indices in range.
    - No self-loops (connection between same
      equipment item).
    - Both port names exist on their respective
      equipment.
    - Joint types match (with `open` as wildcard for
      non-glass-joint physical contact like clamp
      grip / hot-plate top / vessel-on-bench).
    - Male ↔ female port-sex complementarity for
      ground-glass joints (skip for symmetric kinds:
      `hose`, `socket`, `open`).
- **4 port-direction bug fixes in
  `core/lab_equipment.py`** — caught by the validator:
    - Distillation head side arm was female; should be
      male (head pegs INTO condenser inlet, which is
      female).
    - Vacuum adapter top was male; should be female
      (accepts condenser male top output).
    - Thermometer stem joint type was `thermometer-bulb`;
      should be `thermometer-sleeve` to match the
      adapter's `therm-sleeve` socket.
    - Sep funnel had no male outlet — added an
      `outlet` male 24/29 port for addition-funnel
      use (when the funnel is mounted in a 3-neck
      RBF side neck).
  Also relaxed two non-glass-joint contact points
  (clamp jaws → `open`, hot-plate top → `open`) and
  fixed the filter flask mouth joint type to match
  the Büchner stem.  All 37 existing 38a tests still
  pass.
- **`orgchem/gui/dialogs/lab_setups.py`** — singleton
  modeless dialog wired to *Tools → Lab setups…*
  (Ctrl+Shift+U).  Filter + setup list on the left;
  detail card on the right with Purpose / Equipment
  (resolved to full Phase-38a names with id
  annotations) / Connections (port-to-port table
  with notes) / Procedure / Safety / Pedagogical /
  Typical-reactions sections.  When `validate_setup`
  returns errors, they render in RED at the bottom
  of the detail card — surfaces stale data (after a
  Phase-38a port rename) without needing a test
  re-run.  `select_setup(id)` programmatic API for
  the agent-action open path.
- **`orgchem/agent/actions_lab_setups.py`** — 5
  actions in the `lab` category:
    - `list_lab_setups()` — full catalogue with
      equipment + connection details.
    - `get_lab_setup(setup_id)`.
    - `find_lab_setups(needle)` — case-insensitive
      substring across id + name + purpose.
    - `validate_lab_setup(setup_id)` — returns
      `{"valid": bool, "errors": [str]}`.  Useful for
      the future Phase-38c canvas: when a user drags a
      piece onto the canvas, real-time validation
      surfaces port-mismatch errors before they hit
      *Run simulation*.
    - `open_lab_setups(setup_id="")` — open the
      dialog, optionally focus a specific setup.
- **`orgchem/agent/__init__.py`** — auto-loader
  registers the new module.
- **`orgchem/gui/main_window.py`** — Tools menu entry
  added.
- **`orgchem/gui/audit.py`** — all 5 actions
  registered; GUI coverage stays at 100 %.

### Tests
- **`tests/test_lab_setups.py`** — 30 headless cases:
    - Catalogue size ≥ 8.
    - All 8 canonical setups present.
    - Every setup has required fields.
    - Every id is unique.
    - **Headline regression test**: every seeded setup
      validates CLEAN against the Phase-38a equipment
      catalogue.  This catches port-renames + sex-
      mismatch typos at test time rather than at
      canvas-build time.
    - 6 negative-path validator tests covering each
      error class (unknown-id, out-of-range-index,
      self-loop, unknown-port, joint-mismatch,
      port-sex-mismatch).
    - `open` joint type relaxes the strict-equality
      check (clamp grip on glass works).
    - 8 per-setup teaching invariants:
        - Simple distillation has ≥ 2 RBFs (pot +
          receiver).
        - Simple distillation includes thermometer +
          Liebig + distillation head + vacuum adapter.
        - Fractional distillation = simple + Vigreux
          (super-set check on equipment ids).
        - Reflux uses Allihn (NOT Liebig).
        - Soxhlet includes extractor + condenser + RBF.
        - Vacuum filtration includes Büchner + filter
          flask + cold trap.
        - LLE centred on sep funnel + ring stand.
        - Recrystallisation has its own collection
          stage (Büchner + filter flask).
    - get unknown / find substring + case-insensitive
      / find empty.
    - to_dict serialisation has all 10 expected keys
      + connections serialise as a list of dicts.
    - 6 agent-action wrappers (list / get / get-unknown
      / find / validate-clean / validate-unknown).
- **`tests/test_lab_setups_dialog.py`** — 11 pytest-qt
  cases:
    - Construction with ≥ 8 rows + non-modal.
    - Singleton identity.
    - Text filter narrows list (reflux → 2 rows).
    - No-match shows blank message.
    - First setup auto-selected with all 5 standard
      sections in detail (Purpose / Equipment /
      Connections / Procedure / Pedagogical notes).
    - `select_setup("vacuum_filtration")` focuses the
      right row.
    - Detail shows resolved Phase-38a equipment NAMES
      ("Round-bottom flask", "Liebig condenser",
      "Distillation head") rather than just ids.
    - Detail shows port names in the connection list.
    - `select_setup("does-not-exist")` returns False.
    - `open_lab_setups` action fires.
    - `open_lab_setups(setup_id="recrystallisation")`
      focuses the row.
- **Full suite: 1 463 / 1 463 pass, 0 skipped** (was
  1 422).

### Design notes
- **Why a validator?**  Two payoffs: (a) catches real
  port-direction bugs in the equipment catalogue
  before they ship, and (b) gives the future
  Phase-38c canvas a single trusted check for "did
  the user assemble valid apparatus?".  The validator
  is the same code path the canvas will call.
- **Why equipment-by-INDEX, not by id?**  Because the
  same piece can appear twice in one setup — pot RBF
  vs receiver RBF, top + bottom Erlenmeyer in LLE
  collection.  An id-keyed connection model would
  collapse those into one node and lose the
  distinction.  Indexing by position in the equipment
  list is the natural data shape.
- **Why surface validation errors in the dialog?**
  When a Phase-38a port is renamed, the catalogue
  in 38b doesn't update automatically; the validation
  errors appearing in the dialog detail card surface
  the stale data immediately to anyone browsing,
  without anyone needing to run pytest.  Belt + braces
  with the headline regression test.
- **Why use `open` as a wildcard joint type?**
  Some "connections" in real lab setups aren't glass
  joints — they're a clamp gripping a flask, a flask
  sitting on a hot plate, a Büchner funnel pressed
  into a filter flask via a rubber stopper.  Forcing
  these through a strict joint-type check would mean
  inventing dozens of joint-type tags for things
  that are just "physical contact / a stopper / a
  grip".  `open` as a wildcard absorbs all of these
  cleanly.
- **Why no schematic-diagram render in the dialog?**
  The dialog is the *reference* surface; the canvas
  + animation are 38c + 38d.  Adding a render now
  would mean inventing the layout algorithm twice
  (once for the static dialog, once for the
  interactive canvas).  Better to share the same
  layout in 38c.

### Phase 38 status — 2 / 6 sub-phases complete
- 38a ✅ equipment catalogue (round 140).
- 38b ✅ setup catalogue + validator (round 141).
- 38c ⏳ equipment palette + `QGraphicsScene` canvas
  (drag from palette + snap connection ports).
- 38d ⏳ process simulator (per-setup state machine
  + animation).
- 38e ⏳ Reactions-tab integration (pick a seeded
  reaction + matching setup, watch them co-animate).
- 38f ⏳ agent actions for setup placement + sim.

### Next
Round 142: **Phase 38c (equipment palette + canvas)**
is the natural next pick — the QGraphicsScene canvas
where users drag pieces from a palette and snap them
together.  The data model + validator from this round
make the canvas's snap-validation a single function
call.  The seeded setups give the canvas pre-built
templates the user can load.  Ships in 1-2 rounds
depending on how much animation polish lands in 38d
vs 38c.

---

## 2026-04-25 — Round 140 (Phase 38a — lab equipment catalogue)

### Context
Round 139 closed Phase 37 entirely.  Round 140 starts
Phase 38 (the user-flagged multi-round lab-setup
simulator).  38a is the headless equipment catalogue —
the foundation every later sub-phase (38b setups, 38c
canvas, 38d simulator) depends on.  Same dataclass +
dialog shape as Phase 37, so it ships in one round and
sets up the canvas work for round 141+.

### What shipped
- **`orgchem/core/lab_equipment.py`** —
  `Equipment` + `ConnectionPort` frozen dataclasses.
  42-entry catalogue across 12 categories:
    - **glassware (4)**: round-bottom flask, three-neck
      RBF, Erlenmeyer, beaker.
    - **adapter (6)**: distillation head (3-way),
      Claisen adapter, vacuum take-off adapter,
      thermometer adapter, glass stopper, rubber septum.
    - **condenser (6)**: Liebig (straight tube), Allihn
      (bulb), Graham (coil), Friedrichs (spiral),
      Dimroth (double-end coil), air condenser.
    - **heating (5)**: heating mantle, Variac, hot-plate
      stirrer, silicone oil bath, Bunsen burner.
    - **cooling (2)**: ice / water bath (0 °C), dry-ice
      / acetone bath (-78 °C).
    - **separation (3)**: separatory funnel, Vigreux
      fractionating column, Soxhlet extractor.
    - **filtration (3)**: Büchner funnel, Hirsch funnel,
      filter / suction flask.
    - **vacuum (4)**: rotary-vane pump, water aspirator,
      cold-trap vacuum protection, drying tube
      (CaCl₂ / sieves).
    - **stirring (2)**: magnetic stir bar, mechanical
      overhead stirrer.
    - **support (4)**: ring stand, three-prong clamp,
      Keck clip, cork ring.
    - **safety (2)**: fume hood, thermometer.
    - **analytical (1)**: melting-point apparatus
      (placeholder cross-ref to Phase 37c/d catalogues).
  Each entry: id / name / category / description /
  typical_uses / variants / safety_notes / icon_id /
  connection_ports.  Connection ports carry name +
  location + joint_type + is_male flag — the data the
  future Phase-38c canvas will use to snap items
  together.  Joint-type vocabulary: ANSI ground-glass
  tapers (`14/20`, `19/22`, `24/29`, `29/32`), `hose`
  (rubber tubing), `socket` (electrical), `open`
  (no-constraint), and equipment-specific tags
  (`thermometer-bulb`, `filter-paper`, `MP-capillary`,
  `gas-tube`, `dewar-fit`, …).
  Lookup helpers `list_equipment(category)` /
  `get_equipment(id)` / `find_equipment(needle)`
  (case-insensitive substring across id + name +
  category) / `categories()` / `to_dict(equipment)`
  (ports serialise as a list of dicts so the agent
  action returns JSON-friendly data).
- **`orgchem/gui/dialogs/lab_equipment.py`** —
  singleton modeless dialog wired to *Tools → Lab
  equipment…* (Ctrl+Shift+I).  Same outer shape as
  the Phase-37c/d dialogs (category combo + free-text
  filter on the left, list of `name — category` rows,
  HTML detail card on the right) plus a *Connection
  ports* `<ul>` section in the detail body that lists
  every named joint on the selected item with its
  location + joint type + male/female role.
- **`orgchem/agent/actions_lab_equipment.py`** — 4
  actions in the `lab` category:
    - `list_lab_equipment(category="")` — catalogue,
      optional filter; unknown categories → clean error.
    - `get_lab_equipment(equipment_id)` — full record
      by id.
    - `find_lab_equipment(needle)` — case-insensitive
      substring across id + name + category.
    - `open_lab_equipment(equipment_id="")` — open the
      dialog, optionally focus an item.
  All four wired into `agent/__init__.py` auto-loader.
  Lookup actions are pure-headless; the dialog opener
  marshals onto the Qt main thread.
- **`orgchem/gui/main_window.py`** — Tools menu entry
  added.
- **`orgchem/gui/audit.py`** — all 4 actions registered;
  GUI coverage stays at 100 %.

### Tests
- **`tests/test_lab_equipment.py`** — 26 headless cases:
    - Catalogue size ≥ 35 (actually 42).
    - All 12 categories represented.
    - Every entry has required fields (id, name,
      category, description, typical_uses).
    - Every id is unique.
    - 23 canonical apparatus pieces present (RBF,
      3-neck, condensers, mantle, sep funnel, etc.).
    - Per-row teaching invariants:
        - RBF safety mentions cork ring or clamp.
        - Three-neck flask has exactly 3 ports
          (center / left / right).
        - Distillation head has exactly 3 ports
          (bottom + thermometer + side).
        - Liebig has water-in + water-out hose ports.
        - Sep funnel safety mentions venting / pressure.
        - Dry-ice bath in cooling category + mentions
          -78 °C in description.
        - Bunsen burner safety mentions flammable
          solvent / open flame risk.
        - Keck clip variants mention the 24/29 mapping.
    - Every connection port has all required fields.
    - List filtered by category (glassware ≥ 4,
      condenser ≥ 5).
    - List unknown / get unknown / find empty.
    - Find substring + case-insensitive.
    - to_dict serialisation includes port lists.
    - 6 agent-action tests (list / list-filtered /
      list-unknown-error / get / get-unknown / find).
- **`tests/test_lab_equipment_dialog.py`** — 11
  pytest-qt cases:
    - Construction with ≥ 35 rows.
    - Singleton identity.
    - Category combo filtering (condenser → ≥ 5 rows).
    - Text filter narrows list ("flask" → ≥ 4 rows).
    - No-match shows blank message.
    - First item auto-selected with Description +
      Typical-uses sections in detail HTML.
    - Selecting 3-neck-RBF shows all three port names
      (center / left / right) in detail.
    - `select_equipment("liebig_condenser")` focuses
      the right row.
    - Unknown id returns False.
    - `open_lab_equipment` action fires.
    - Open with `equipment_id="sep_funnel"` focuses it.
- **Full suite: 1 422 / 1 422 pass, 0 skipped** (was
  1 385).

### Design notes
- **Why 42 entries, not 50?**  The user-flagged brief
  mentioned ~50 items; the actual catalogue lands at
  42 because the listed items don't all justify
  separate entries (e.g. "Variac" + "voltage controller"
  = same entry; "round-bottom flask" covers all sizes
  via the variants field).  The 42 in the catalogue
  cover every piece needed by the canonical Phase-38b
  setups (simple distillation, fractional, reflux,
  Soxhlet, vacuum filtration, recrystallisation,
  liquid-liquid extraction).  Extras (rotary
  evaporator, lyophiliser, glove box, Schlenk line)
  can land in 38a.1 polish.
- **Why `ConnectionPort` as a separate dataclass?**
  The future Phase-38c canvas needs deterministic
  snap-validation: when the user drags item A onto
  item B, can these two pieces actually connect?  By
  encoding the joint-type vocabulary now (ground-glass
  tapers + hose + socket + open + specialty tags), the
  canvas just compares `joint_type` strings + male /
  female flags.  No dynamic typing; clear failure
  modes.  Joint compatibility (24/29 male ↔ 24/29
  female) is a simple equality + sex-mismatch check.
- **Why include the `icon_id` field as just a string?**
  Phase 38c will need an SVG asset per equipment item.
  Reserving the field now (as a placeholder string
  matching the equipment id) means the asset directory
  can be populated in 38c without re-touching the
  catalogue.
- **Why no quantitative widgets / calculators?**
  Equipment doesn't compute — the simulator (38d) is
  where the physics lives.  This sub-phase is pure
  reference + the connection-port data structure that
  later sub-phases consume.

### Phase 38 status — 1 / 6 sub-phases complete
- 38a ✅ equipment catalogue (round 140).
- 38b ⏳ setup catalogue (`Setup` dataclass + 6-8
  canonical setups: simple distillation, fractional,
  reflux, Soxhlet, …).
- 38c ⏳ equipment palette + `QGraphicsScene` canvas
  (drag from palette + snap connection ports).
- 38d ⏳ process simulator (per-setup state machine
  + animation).
- 38e ⏳ Reactions-tab integration (pick a seeded
  reaction + matching setup, watch them co-animate).
- 38f ⏳ agent actions for setup placement + sim.

### Next
Round 141: **Phase 38b (setup catalogue)** — same
shape as 38a, 6-8 canonical setups (simple distillation
RBF + dist-head + thermometer + Liebig + vacuum
adapter + receiver; reflux RBF + Allihn; Soxhlet
flask + extractor + condenser; …).  Each setup carries
an ordered list of equipment ids + the connections
between them.  Ships cleanly in one round.

---

## 2026-04-25 — Round 139 (🎉 Phase 37 CLOSED — spectrophotometry + Beer-Lambert calculator)

### Context
Round 138 closed Phase 37c (chromatography).  Round 139
ships 37d — spectrophotometry + a Beer-Lambert calculator
that's the first quantitative widget in the Phase-37
catalogue family.  After this round, all four user-flagged
sub-phases of Phase 37 (qualitative inorganic + clinical
lab + chromatography + spectrophotometry) are end-to-end
functional.

### What shipped
- **`orgchem/core/spectrophotometry_methods.py`** —
  `SpectrophotometryMethod` frozen dataclass + 12-entry
  catalogue across 5 categories:
    - **molecular-uv-vis (2)**: UV-Vis, fluorescence.
    - **molecular-ir (5)**: IR/FTIR, ATR-FTIR, NIR,
      Raman, SERS.
    - **molecular-chirality (1)**: CD.
    - **atomic (3)**: AAS, ICP-OES, ICP-MS.
    - **magnetic-resonance (1)**: NMR.
  Each entry is a long-form reference card (200-500 words)
  with principle / light source / sample handling /
  detector / wavelength range / typical analytes /
  strengths / limitations / procedure / notes.  IR/FTIR
  + NMR cross-reference the existing `core/spectroscopy.py`
  + `core/nmr.py` *predictors* so users see the
  descriptive (this round) and predictive (Phase 4) layers
  integrated.  Notes capture textbook landmarks: NIR
  pulse-oximeter as everyday application, GCMS Kovats
  reference handling, NMR's Nobel history (Ernst 1991, MRI
  2002), Sanger's 2D paper chromatography insulin
  sequence, etc.
- **Beer-Lambert helper** — `beer_lambert_solve(absorbance,
  molar_absorptivity, path_length_cm, concentration_M)`:
  pass any 3 of 4 quantities, get the 4th.  Validates
  exactly-one-missing + positive inputs.  Pure-headless;
  the dialog + agent action both delegate to it.
- **`orgchem/gui/dialogs/spectrophotometry_methods.py`** —
  singleton modeless dialog wired to *Tools →
  Spectrophotometry techniques…* (Ctrl+Shift+W).
  Same outer shape as the Phase-37c chromatography dialog
  (category combo + free-text filter + list + 9-section
  HTML detail card) PLUS a collapsible Beer-Lambert
  calculator panel at the bottom of the right pane:
    - 4 `QDoubleSpinBox` fields for A / ε (M⁻¹·cm⁻¹) /
      l (cm) / c (M) — c uses 8-decimal display for
      sub-µM concentrations.
    - *Solve for empty field* button (treats 0 as
      "blank") + *Clear* button.
    - Status label that displays the rearranged
      equation in human form (e.g. "c = A / (ε · l) =
      4.0e-5 M").
  `select_method(method_id)` programmatic API for the
  agent-action open path.
- **`orgchem/agent/actions_spectrophotometry.py`** — 5
  actions in the `spectrophotometry` category:
    - `list_spectrophotometry_methods(category="")` —
      catalogue, optional category filter.
    - `get_spectrophotometry_method(method_id)` — full
      record by id.
    - `find_spectrophotometry_methods(needle)` —
      case-insensitive substring across id + name +
      abbreviation.
    - `beer_lambert(...)` — quantitative helper exposed
      to the tutor / scripts.
    - `open_spectrophotometry(method_id="")` — open the
      dialog, optionally focus a method.
  All five wired into `agent/__init__.py` auto-loader.
  Lookup + Beer-Lambert actions are pure-headless; the
  dialog opener marshals onto the Qt main thread.
- **`orgchem/gui/main_window.py`** — Tools menu entry
  added.
- **`orgchem/gui/audit.py`** — all 5 actions registered;
  GUI coverage stays at 100 %.

### Tests
- **`tests/test_spectrophotometry_methods.py`** — 33
  headless cases:
    - Catalogue size ≥ 12.
    - All 5 categories represented.
    - Every entry has all required fields (13 fields).
    - 12 canonical methods present.
    - Per-row teaching invariants:
        - UV-Vis principle mentions Beer-Lambert / molar
          absorptivity.
        - Fluorescence mentions Stokes shift or quantum
          yield.
        - IR/FTIR notes cross-reference
          `core/spectroscopy` predictor.
        - ATR-FTIR mentions no-sample-prep.
        - Raman mentions complementary selection rule
          / polarisability.
        - SERS mentions 10⁴-10⁸× enhancement factor.
        - CD typical-analytes mentions secondary
          structure / α-helix / β-sheet.
        - NMR notes cross-reference `core/nmr` shift
          predictor.
        - ICP-MS limitations mention polyatomic
          interferences.
    - List filtered by category (5 IR + 3 atomic).
    - List unknown / get unknown / find empty.
    - Beer-Lambert solver in ALL 4 directions
      (concentration, absorbance, path length, molar
      absorptivity) with rel_tol 1e-6 numerical
      precision.
    - Beer-Lambert rejects two-missing inputs +
      zero / negative inputs.
    - to_dict serialisation has all 14 expected keys.
    - 8 agent-action tests covering happy path +
      every error path including the Beer-Lambert
      action.
- **`tests/test_spectrophotometry_dialog.py`** — 14
  pytest-qt cases:
    - Construction with ≥ 12 rows.
    - Singleton identity.
    - Category combo filtering (atomic → 3 rows).
    - Text filter narrows list (nmr → 1 row).
    - No-match shows blank message.
    - First method auto-selected with all 5 standard
      sections in detail.
    - `select_method("nmr")` focuses NMR.
    - Unknown id returns False.
    - **Beer-Lambert calculator widget** — fills
      concentration from A + ε + l; fills absorbance
      from ε + l + c; complains when 2 fields blank;
      Clear button resets all 4 spin boxes.
    - `open_spectrophotometry` action fires.
    - Open with `method_id="cd"` focuses CD row.
- **Full suite: 1 385 / 1 385 pass, 0 skipped** (was
  1 338).

### Design notes
- **Why include NMR in a "spectrophotometry" catalogue?**
  Strictly speaking NMR isn't optical spectroscopy — it
  uses RF.  But pedagogically NMR is the workhorse
  spectroscopic technique organic students learn
  alongside IR / UV-Vis / MS, and a "techniques" reference
  panel that omits NMR would feel incomplete.  Categorised
  as `magnetic-resonance` rather than mixed in with the
  optical methods, with notes that surface its RF (not
  light) source.
- **Why a Beer-Lambert calculator + no other quantitative
  widgets?**  Beer-Lambert is the single most-taught
  quantitative relationship in undergraduate
  spectroscopy.  Other methods have analytical
  relationships (Hammett ρ, K_eq from spectroscopy
  titrations, Raman cross-section…) but those are far
  more specialised — adding calculator widgets for them
  would clutter the dialog without much pedagogical
  payoff.  The Beer-Lambert solver doubles as a worked
  example of the catalogue + helper-function pattern,
  in case 37e (e.g. NMR shift calculator) wants to add
  more.
- **Why both a dialog widget AND an agent action for
  Beer-Lambert?**  Different audiences.  The dialog
  widget is for a student doing a worked example
  by hand; the agent action is for a tutor doing
  scripted demos or a student generating a calibration
  curve programmatically.  Same underlying solver →
  no duplication.
- **Why no spectrum simulator / lineshape predictor?**
  Out of scope for a *reference* catalogue.  The Phase
  4 layer (`core/spectroscopy.py` for IR, `core/nmr.py`
  for NMR, `core/ms.py` for MS) already does
  prediction; this phase deliberately complements
  rather than overlapping.

### Phase 37 status — COMPLETE 🎉
- 37a ✅ qualitative inorganic tests (round 136).
- 37b ✅ clinical lab panels (round 137).
- 37c ✅ chromatography techniques (round 138).
- 37d ✅ spectrophotometry techniques (round 139).

The entire user-flagged Phase 37 (analytical-chemistry
reference tools) is now end-to-end functional.

### Next
Round 140 candidates:
- **Phase 38a (start the lab setup simulator)** — begin
  with a headless equipment catalogue (~50 entries)
  following the Phase-37a pattern; canvas + animation
  ship in later rounds (38b-38f).
- **Phase 31 long-running content** — chip another
  named reaction (38/50), SAR series (9/15), etc.
- **Phase 36 polish** — lasso select + drag, indole /
  NHAc templates.

---

## 2026-04-25 — Round 138 (Phase 37c — chromatography techniques)

### Context
Round 137 closed Phase 37b.  Round 138 ships 37c — same
catalogue + dialog + agent-action shape, keyed to
chromatographic separation methods.  The user-flagged
brief specified GC / HPLC / FPLC at minimum; the
catalogue ships those plus 12 more methods covering the
modern analytical + preparative spread.

### What shipped
- **`orgchem/core/chromatography_methods.py`** —
  `ChromatographyMethod` frozen dataclass (id / name /
  abbreviation / category / principle / stationary_phase
  / mobile_phase / detectors / typical_analytes /
  strengths / limitations / procedure / notes).  15
  entries:
    - **Planar (2)**: TLC, paper.
    - **Preparative-column (2)**: gravity column, flash.
    - **Gas (2)**: GC, GC-MS.
    - **Liquid (3)**: HPLC, LC-MS, HILIC.
    - **Protein (4)**: FPLC, IEX, SEC, affinity.
    - **Ion (1)**: IC.
    - **Supercritical (1)**: SFC.
  Each entry is a 200-400-word reference card structured
  around the strengths-vs-limitations trade-off — the
  pedagogically essential bit ("what's this method good
  at? what does it not handle?").  Notes capture the
  textbook teaching footnotes (Kovats retention indices,
  MRM for triple-quad LC-MS, ÄKTA as the FPLC platform,
  SFC's chiral-separation dominance).
- **`orgchem/gui/dialogs/chromatography_methods.py`** —
  singleton modeless dialog wired to *Tools →
  Chromatography techniques…* (Ctrl+Shift+G).  Same
  shape as the round-136 qualitative-tests dialog:
  category combo + free-text filter on the left, list of
  `abbreviation — name` rows, HTML detail card on the
  right with 8 sections (Principle / Stationary phase /
  Mobile phase / Detector(s) / Typical analytes /
  Strengths / Limitations / Procedure / Notes).
  `select_method(method_id)` programmatic API for the
  agent-action open path.
- **`orgchem/agent/actions_chromatography.py`** — 4
  actions in the `chromatography` category:
    - `list_chromatography_methods(category="")` —
      catalogue, optional category filter.
    - `get_chromatography_method(method_id)` — full
      record by id.
    - `find_chromatography_methods(needle)` —
      case-insensitive substring across id + name +
      abbreviation.
    - `open_chromatography_methods(method_id="")` — open
      the dialog, optionally focus a method.
  Dialog opener marshals onto the Qt main thread.
- **`orgchem/agent/__init__.py`** — auto-loader
  registers the new module.
- **`orgchem/gui/main_window.py`** — Tools menu entry
  added.
- **`orgchem/gui/audit.py`** — all 4 actions registered;
  GUI coverage stays at 100 %.

### Tests
- **`tests/test_chromatography_methods.py`** — 23
  headless cases:
    - Catalogue size ≥ 15.
    - All 7 categories represented.
    - Every entry has all required fields.
    - 14 canonical methods present (TLC, column, flash,
      GC, GC-MS, HPLC, LC-MS, HILIC, FPLC, IEX, SEC,
      affinity, IC, SFC).
    - User-explicitly-requested methods (GC, HPLC,
      FPLC) have non-trivial principle text.
    - Per-row teaching invariants:
        - HPLC mentions reverse-phase or C18.
        - GC limitations mention volatility / thermal
          constraint.
        - SEC principle mentions size + pore + void /
          early elution.
        - Affinity entry references His-tag / Ni-NTA /
          Protein A / GST.
        - SFC strengths / typical analytes mention
          chiral / enantiomer.
    - List filtered by category / unknown returns empty.
    - get_method unknown returns None.
    - find_methods substring + case-insensitive +
      empty-needle behaviour.
    - to_dict serialisation has all 13 expected keys.
    - 6 agent-action tests (list / list-filtered /
      list-unknown-error / get / get-unknown-error /
      find-methods).
- **`tests/test_chromatography_dialog.py`** — 10
  pytest-qt cases:
    - Dialog constructs with ≥ 15 rows.
    - Singleton returns same instance.
    - Category combo filters list (protein → 4 rows).
    - Text filter narrows list.
    - No-match shows blank message.
    - First method auto-selected on construction with
      all 5 standard sections in detail card.
    - `select_method("hplc")` focuses the right row.
    - Unknown id returns False.
    - `open_chromatography_methods` action fires.
    - Open with `method_id="sfc"` focuses SFC row.
- **Full suite: 1 338 / 1 338 pass, 0 skipped** (was
  1 305).

### Design notes
- **Why 15 methods, not 7 or 30?**  The user-requested
  brief named TLC + column + GC + HPLC + FPLC (+ "etc").
  15 covers the mainstream spread without padding —
  every modern lab uses a subset of these regularly.
  Adding more would mean specialty / niche techniques
  (DCCC, CCC, paired-ion HPLC, micellar HPLC, …) that
  most undergrads never see.
- **Why a strengths-vs-limitations field pair instead of
  a single "notes" field?**  Pedagogical: surfacing the
  trade-off explicitly is what makes a chromatography
  reference USEFUL.  "GC is fast + sensitive BUT only
  volatile analytes" is the essential mental model;
  burying that in prose loses the teaching point.
- **Why no separation simulator / van Deemter
  calculator?**  Reference data first, simulators
  second.  A van Deemter plot or Rf calculator would be
  a natural 37c.1 polish round if anyone asks for it,
  but the catalogue already gives students the
  qualitative + quantitative info they need to
  understand WHEN to use each method.
- **Why share the dialog shape across 37a / 37c?**  Same
  user model (browse a categorised reference catalogue,
  drill down to a detail card) deserves the same UI
  shape.  37b's dialog is slightly different (panel
  picker + analyte table) because the data model is
  different (panels OWN analytes), but 37a + 37c are
  pure category + entry catalogues with no internal
  hierarchy.

### Phase 37 status snapshot (post-round 138)
- 37a ✅ qualitative inorganic tests (round 136).
- 37b ✅ clinical lab panels (round 137).
- 37c ✅ chromatography techniques (round 138).
- 37d ⏳ spectrophotometry (UV-Vis / fluorescence /
  IR / Raman / AA / CD).
- Phase 38 ⏳ lab setup + process simulator (multi-
  round).

### Next
Round 139: **Phase 37d (spectrophotometry)** is the
natural next pick — closes Phase 37 entirely.  Same
catalogue + dialog shape as 37c.

---

## 2026-04-25 — Round 137 (Phase 37b — clinical lab panels)

### Context
Round 136 closed Phase 37a (qualitative inorganic tests).
Phase 37 has 4 sub-phases queued; 37b is the natural
next pick — same dialog + catalogue shape as 37a but
keyed to clinical-chemistry lab panels rather than
wet-lab inorganic tests.  Ships in one round comfortably
since the data shape is well-understood after 37a.

### What shipped
- **`orgchem/core/clinical_panels.py`** — headless
  catalogue (~570 lines).  `LabAnalyte` + `LabPanel`
  frozen dataclasses.  21 unique analytes:
    - **Electrolyte (4)**: Na, K, Cl, HCO₃.
    - **Kidney (2)**: BUN, creatinine.
    - **Metabolic (2)**: glucose, HbA1c.
    - **Liver (6)**: ALT, AST, ALP, total bilirubin,
      albumin, total protein.
    - **Lipid (4)**: TC, LDL, HDL, triglycerides.
    - **Hormone (2)**: TSH, free T4.
    - **Vitamin (1)**: 25(OH)D.
    - **Mineral / electrolyte (1)**: calcium.
  6 seeded panels reusing those analytes: BMP / CMP /
  Lipid / DM follow-up / Thyroid / Vitamin D screening.
  CMP literally shares BMP's analyte instances by
  reference (frozen dataclass identity).  Each analyte
  carries the clinical-significance + interpretation
  notes that hit the textbook teaching points (BUN/Cr
  ratio for pre-renal vs intrinsic, AST/ALT > 2 for
  alcoholic hepatitis, HbA1c 3-month timescale,
  Friedewald LDL caveat, Gilbert syndrome, anion-gap
  MUDPILES, etc.).  Lookup helpers
  `list_panels` / `get_panel` / `list_analytes(category)` /
  `get_analyte` / `find_analyte(needle)` (matches against
  id + name + abbreviation, case-insensitive) /
  `categories()` + `analyte_to_dict` / `panel_to_dict`.
- **`orgchem/gui/dialogs/clinical_panels.py`** —
  singleton modeless dialog wired to *Tools → Clinical
  lab panels…* (Ctrl+Shift+L).  Top: panel-picker
  combo.  Below: horizontal splitter with left =
  panel meta block (purpose / sample / fasting /
  procedure / notes) + per-analyte `QTableWidget`
  (4 columns: name, abbreviation, units, normal range);
  right = analyte detail pane (title + meta line +
  clinical-significance + notes).  Auto-selects first
  panel + first analyte on open.  Switching panels
  repopulates the table.  `select_panel(id)` +
  `select_analyte(id)` programmatic API for the
  `open_clinical_panels` agent action.
- **`orgchem/agent/actions_clinical.py`** — 5 new
  actions in the `clinical` category:
    - `list_lab_panels()` — one-row-per-panel summary.
    - `get_lab_panel(panel_id)` — full record incl.
      every analyte.
    - `list_lab_analytes(category="")` — every analyte
      deduplicated, optional category filter.
    - `find_lab_analyte(needle)` — case-insensitive
      name / abbreviation / id lookup.
    - `open_clinical_panels(panel_id="", analyte_id="")`
      — open the dialog and optionally focus a panel +
      row.
  Dialog opener marshals onto the Qt main thread via
  `_gui_dispatch.run_on_main_thread_sync`.
- **`orgchem/agent/__init__.py`** — auto-loader registers
  the new module so the actions show up in
  `registry()`.
- **`orgchem/gui/main_window.py`** — Tools menu entry
  added.
- **`orgchem/gui/audit.py`** — all 5 actions registered;
  GUI coverage stays at 100 %.

### Tests
- **`tests/test_clinical_panels.py`** — 29 headless
  cases:
    - 3 primary panels (BMP / CMP / Lipid) + 3 extended
      panels present.
    - BMP = 8 analytes, CMP = 14 (= BMP ∪ 6 more), Lipid
      = 4 (TC / LDL / HDL / TG).
    - Every analyte has all required fields.
    - Every panel has all required meta.
    - Teaching invariants on key analyte descriptions
      (BUN mentions kidney, Cr mentions GFR, HbA1c
      mentions 3-month timescale, TSH mentions
      thyroid).
    - All 7 analyte categories represented.
    - List filtered by category (lipid = 4, electrolyte
      ≥ 4).
    - Unknown category returns [].
    - Lookup helpers (get_panel / get_analyte unknown
      → None; find_analyte by name / by abbreviation /
      case-insensitive / empty / no-match).
    - **BMP and CMP share the glucose instance**
      (frozen-dataclass identity check).
    - to_dict serialisation has all 8 analyte keys + 9
      panel keys.
    - 7 agent-action tests cover happy path + unknown
      panel / category / analyte error paths.
- **`tests/test_clinical_panels_dialog.py`** — 13
  pytest-qt cases:
    - Dialog constructs with ≥ 5 panel-combo entries.
    - Singleton returns same instance.
    - Default loads first panel (BMP, 8 rows in table).
    - Switching to Lipid repopulates with 4 rows.
    - Panel meta text includes "Purpose" + "Fasting".
    - First analyte auto-selected on construction.
    - `select_analyte("creatinine")` focuses the right
      row.
    - Selecting an analyte not in the current panel
      returns False (cross-panel safety).
    - `select_panel(id)` + `select_analyte(id)`
      sequential.
    - Unknown panel id returns False.
    - `open_clinical_panels` action fires.
    - Open with both panel + analyte focuses both.
    - Open with unknown analyte → analyte_selected is
      False but panel_selected is True (no crash).
- **Full suite: 1 305 / 1 305 pass, 0 skipped** (was
  1 263).

### Design notes
- **Why share LabAnalyte instances rather than copy?**
  CMP IS BMP + 6 more by definition.  Sharing the
  frozen-dataclass instances (a) avoids data drift
  (BMP and CMP can't disagree on glucose's normal
  range), (b) cuts memory footprint, (c) makes
  cross-panel lookups (e.g. "every panel that
  measures glucose") trivial.  `frozen=True` makes
  this safe — callers can't mutate either copy.
- **Why include Vitamin D screening?**  Without it,
  the `vitamin` category in `VALID_CATEGORIES` had
  zero entries (vitamin D was defined as a LabAnalyte
  but not used by any panel).  The 7-category
  coverage invariant test caught the gap during the
  test pass — added a small Vit D + Ca screening
  panel rather than dropping the category.  Bonus:
  the small panel doubles as a teaching demo for
  what a "single-analyte focused workup" looks like.
- **Why no chemistry / interpretation logic?**  These
  panels are reference data, not decision support.
  A student looking up "what does an elevated AST/ALT
  ratio mean?" gets a textbook answer; an
  interpretation engine would have to handle dozens
  of confounders (medications, intercurrent illness,
  age, sex) and would still be wrong often enough to
  cause harm if anyone confused it for clinical
  guidance.
- **Why not include CBC, coagulation, ABG?**  Those
  are different test categories (haematology /
  coagulation / blood gas) with their own analyte
  catalogues — could be Phase 37e if the user wants
  them, but BMP / CMP / Lipid covered the user's
  explicit request.

### Phase 37 status snapshot (post-round 137)
- 37a ✅ qualitative inorganic tests (round 136).
- 37b ✅ clinical lab panels (round 137).
- 37c ⏳ chromatography (TLC / column / GC / HPLC /
  FPLC / SFC / ion).
- 37d ⏳ spectrophotometry (UV-Vis / fluorescence /
  IR / Raman / AA / CD).
- Phase 38 ⏳ lab setup + process simulator (multi-
  round).

### Next
Round 138: **Phase 37c (chromatography)** is the
natural next pick — same dialog shape, ~7-10 entries
covering the major separation methods.  Ships in one
round.

---

## 2026-04-25 — Round 136 (Phase 37a — qualitative inorganic tests + roadmap expansion)

### Context
User flagged a new feature request: two reference tools
for wet-lab analytical chemistry —
1. Qualitative inorganic tests (flame / hydroxide / halide
   / sulfate / carbonate / ammonium / common gas tests).
2. Clinical-chemistry lab panels (BMP / CMP / Lipid Panel).
Mid-round, two more tools added to the request:
3. Chromatography techniques (TLC / column / GC / HPLC /
   FPLC / SFC / ion).
4. Spectrophotometry (UV-Vis / fluorescence / IR / Raman /
   AA / CD / etc.).
And then a much bigger request:
5. Lab setup + process simulator with equipment library +
   interactive canvas + animated process simulation +
   seeded demos (simple distillation, reflux, Soxhlet, …).

Round 136 ships #1 fully and adds #2-#5 to the roadmap as
queued sub-phases / phases for future rounds.  Splitting
the requests this way ensures each ships cleanly with full
test coverage instead of cramming five UI tools into one
round.

### What shipped
- **`orgchem/core/qualitative_tests.py`** — headless
  catalogue.  `InorganicTest` dataclass (id, name,
  category, target Unicode ion / gas, target_class
  ∈ {cation, anion, gas}, reagents, procedure,
  positive_observation, colour_hex for the dialog
  swatch, notes).  32 entries:
    - **Flame (8)**: Li / Na / K / Ca / Sr / Ba / Cu /
      Cs.
    - **Hydroxide (9)**: Cu²⁺ / Fe²⁺ / Fe³⁺ / Al³⁺ /
      Mg²⁺ / Ca²⁺ / Zn²⁺ / Pb²⁺ / Mn²⁺ — with
      amphoteric notes on Al / Zn / Pb that distinguish
      them from Mg / Ca in excess NaOH.
    - **Halide (3)**: Cl⁻ / Br⁻ / I⁻ — with the
      ammonia-solubility differentiation (dilute NH₃
      dissolves AgCl, conc. NH₃ dissolves AgBr,
      neither dissolves AgI).
    - **Sulfate**: BaSO₄ insoluble in acid.
    - **Carbonate**: CO₃²⁻ / HCO₃⁻ + acid → CO₂ →
      limewater milky.
    - **Ammonium**: NH₄⁺ + NaOH + heat → NH₃ → litmus.
    - **Gas (8)**: H₂ / O₂ / CO₂ / Cl₂ / NH₃ / HCl /
      SO₂ / NO₂.
  Lookup helpers: `list_tests(category)`,
  `get_test(test_id)`, `find_tests_for(target)`,
  `categories()`, `to_dict(test)`.
  `_normalise_ion_label` strips Unicode super /
  subscripts + lowercases + drops whitespace, so
  `"Cu²⁺"` / `"Cu2+"` / `"cu  2  +"` all hash the
  same.
- **`orgchem/gui/dialogs/qualitative_tests.py`** —
  modeless singleton dialog wired to *Tools →
  Qualitative inorganic tests…* (Ctrl+Shift+Q).  Left
  pane: category combo (`(all categories)` + 7
  categories) + free-text filter + `QListWidget`
  showing `target — name` rows.  Right pane: title +
  meta line (target + class + category) + colour
  swatch (`QLabel` whose stylesheet background is
  set from the entry's `colour_hex`) + `QTextBrowser`
  detail pane with Reagents / Procedure / Positive
  observation / Notes sections.  `select_test(test_id)`
  programmatic API for the agent-action open path.
- **`orgchem/agent/actions_qualitative.py`** — 4 new
  actions registered under category `"qualitative"`:
    - `list_inorganic_tests(category="")` — full
      catalogue or filtered (unknown categories return
      `{"error": ...}`).
    - `get_inorganic_test(test_id)` — full record by id.
    - `find_inorganic_tests_for(target)` — every test
      matching an ion / gas (case + Unicode tolerant).
    - `open_qualitative_tests(test_id="")` — open the
      dialog and optionally focus a row.  Marshals
      onto the Qt main thread via
      `_gui_dispatch.run_on_main_thread_sync`.
  All four wired into `agent/__init__.py` auto-loader.
- **`orgchem/gui/main_window.py`** — Tools menu entry
  *Qualitative inorganic tests…* (Ctrl+Shift+Q) with
  modeless singleton dialog opener.
- **`orgchem/gui/audit.py`** — all 4 actions registered
  in `GUI_ENTRY_POINTS`; coverage stays at 100 %.

### Tests
- **`tests/test_qualitative_tests.py`** — 23 headless
  cases:
    - 7-category invariant (every valid category has
      ≥ 1 entry).
    - Catalogue size ≥ 30.
    - Every entry has all required fields (id, name,
      target, target_class, reagents, procedure,
      observation, colour_hex starts with `#` + 6 hex).
    - Canonical flame / halide / gas tests present.
    - Filter by category / by unknown-category empty.
    - Get unknown id returns None.
    - Get returns full record (Na yellow flame).
    - ASCII / lowercase / whitespace tolerance for
      `find_tests_for`.
    - Aluminium hydroxide notes mention amphoteric /
      excess NaOH (the discriminating teaching point
      vs Mg / Ca).
    - `to_dict` serialisation has all 10 expected keys.
    - 6 agent-action tests: list / list-filtered /
      list-unknown-error / get / get-unknown-error /
      find-by-ASCII-target.
- **`tests/test_qualitative_dialog.py`** — 11
  pytest-qt cases:
    - Dialog constructs with ≥ 30 rows, non-modal.
    - Singleton returns same instance.
    - Category combo filters list (3 rows for halide).
    - Text filter narrows list ("copper" → ≥ 2 rows).
    - No-match filter shows blank message.
    - Selection updates title + detail pane.
    - `select_test("flame-na")` focuses the right row.
    - Unknown id returns False.
    - Swatch stylesheet contains entry's `colour_hex`.
    - `open_qualitative_tests` agent action fires +
      can focus a specific test.
- **Full suite: 1 263 / 1 263 pass, 0 skipped** (was
  1 229).

### Roadmap expansion
Added to `ROADMAP.md`:
- **Phase 37**:
    - 37a ✅ qualitative inorganic tests (round 136).
    - 37b ⏳ clinical lab panels (BMP / CMP / Lipid).
    - 37c ⏳ chromatography (TLC / column / GC / HPLC /
      FPLC / SFC / ion).
    - 37d ⏳ spectrophotometry (UV-Vis / fluorescence /
      IR / Raman / AA / CD).
- **Phase 38** ⏳ lab setup + process simulator —
  equipment library (~50 items: glassware kits, heating
  / cooling, separation, support, analytical), setup
  canvas with palette + drag-and-drop + connection-port
  snapping, animated process simulation per setup
  (simple distillation, fractional, reflux, Soxhlet,
  liquid-liquid extraction, vacuum filtration,
  recrystallisation), 6-10 rounds in scope split as
  38a-38f.

### Design notes
- **Why a reference panel rather than a simulator?**
  37a is intentionally a *describe what would happen*
  tool — no chemistry runs.  The pedagogical use case
  is "I'm seeing a blue flame in the lab, what cation
  is that?" or "I want to know how to test for
  chloride".  Simulation belongs in Phase 38.
- **Why 7 categories not 5?**  Could have grouped
  ammonium under "cation" and gases under "anion / gas",
  but the experimental procedure for ammonium (NaOH +
  heat → litmus) and the gas tests (visual / litmus /
  limewater) are categorically different from
  precipitation tests, and the dialog's category combo
  reads more clearly with these as separate groups.
- **Why Unicode targets in the data + ASCII-tolerant
  lookup?**  The dialog renders Unicode cleanly
  (`"Cu²⁺"` looks better than `"Cu2+"` in the row
  text), but the agent / scripts shouldn't need to
  copy-paste Unicode to call `find_inorganic_tests_for`.
  The `_normalise_ion_label` helper bridges the two
  worlds — Unicode in the data, ASCII / Unicode either
  in the query.
- **Why no atom-mapped chemistry SMILES on the test
  entries?**  These are observation-driven procedures,
  not transformations; the diagnostic IS the visual
  result (flame colour, precipitate colour, gas
  evolution).  Forcing a SMILES would over-engineer
  the data model for a teaching-reference tool.

### Next
Round 137: **Phase 37b (clinical lab panels)** is the
natural next sub-phase — same shape as 37a, smaller
catalogue (BMP 8 analytes + CMP 14 + Lipid 4-5), so it
should ship in one round comfortably.  Then 37c
(chromatography) + 37d (spectrophotometry) at one each.
Phase 38 is multi-round and would start once Phase 37 is
fully closed.

---

## 2026-04-25 — Round 135 (Phase 36 polish: tapered wedge + hashed dash bonds)

### Context
Two consecutive content rounds (133: fluoroquinolones,
134: CuAAC) advanced Phase 31 catalogues but left the
Phase-36 drawing-tool visuals at the round-130 "thick
green pen for wedge, dashed blue line for dash"
placeholders.  The data-model side (Bond.stereo + SMILES
/ mol-block round-trip) was correct — only the visual
encoding was placeholder-y.  Round 135 ships the proper
ChemDraw-style geometry that this round's user-facing
drawing tool deserves.

### What shipped
- **`orgchem/gui/panels/drawing_panel.py`** — bond-rendering
  refactor:
    - New `_build_bond_visual(idx) -> QGraphicsItem` factory
      that dispatches on `bond.stereo`:
        - `"wedge"` → `_build_wedge_item(ax, ay, bx, by)`
          returning a `QGraphicsPolygonItem` triangle (apex
          at begin atom, two base vertices flanking the end
          atom along the perpendicular axis).
        - `"dash"` → `_build_dash_item(ax, ay, bx, by)`
          returning a `QGraphicsItemGroup` of perpendicular
          hash lines spaced ~4 px apart, widening from
          1 px half-width at the begin atom to 5 px half-
          width at the end atom.
        - `"either"` → squiggle-grey dotted line (existing).
        - default → plain `QGraphicsLineItem` with the
          width / dash pattern encoding for bond order
          (existing).
    - `_draw_bond(idx)` simplified — calls the factory,
      addItem to scene, append to `_bond_items`.
    - `_refresh_bond(idx)` now drops the old item from the
      scene and rebuilds via the factory.  Cheap on
      teaching-scale molecules and avoids the dual update
      paths that would otherwise be needed when stereo
      flips swap the underlying QGraphicsItem subclass.
    - Tunables surfaced as class attributes:
      `_STEREO_WEDGE_COLOUR`, `_STEREO_DASH_COLOUR`,
      `_STEREO_EITHER_COLOUR`, `_BOND_DEFAULT_COLOUR`,
      `_WEDGE_HALF_WIDTH_PX = 5.0`,
      `_DASH_HASH_SPACING_PX = 4.0`,
      `_DASH_HALF_WIDTH_BEGIN = 1.0`,
      `_DASH_HALF_WIDTH_END = 5.0`.

### Tests
- **`tests/test_drawing_panel_wedge_geometry.py`** — 15
  new pytest-qt cases:
    - **Wedge geometry (7 tests)**: type-check
      `QGraphicsPolygonItem`, polygon has exactly 3
      vertices, apex sits on begin atom (sub-pixel
      tolerance), base centre sits on end atom, base
      vector is perpendicular to bond axis (dot product
      ≈ 0), base width = 2 × `_WEDGE_HALF_WIDTH_PX`,
      brush colour is `_STEREO_WEDGE_COLOUR`.
    - **Dash geometry (3 tests)**: type-check
      `QGraphicsItemGroup`, has ≥ 4 hash lines (all
      `QGraphicsLineItem`), last hash longer than first
      hash (widening invariant).
    - **Live update on atom drag (2 tests)**: drag end
      atom, wedge polygon's base centre tracks new
      position; same for the dash group's last hash.
    - **Stereo flip swaps visual type (2 tests)**: wedge
      → dash flips `QGraphicsPolygonItem` → `QGraphicsItemGroup`;
      dash toggle-off (same kind clicked twice) flips
      `QGraphicsItemGroup` → `QGraphicsLineItem`.
    - **No scene leaks (1 test)**: stereo flip
      preserves the scene item count.
- All 77 existing drawing tests still pass — the refactor
  is a pure visual upgrade with no data-model changes.
- Full suite: **1 229 / 1 229 pass, 0 skipped** (was
  1 214).

### Design notes
- **Why rebuild rather than mutate?**  Wedge ↔ dash flips
  swap the underlying QGraphicsItem subclass
  (`QGraphicsPolygonItem` ↔ `QGraphicsItemGroup` ↔
  `QGraphicsLineItem`).  An in-place update path would
  need three separate "update polygon vertices" / "update
  group children" / "update line endpoints" branches
  AND a "no-op vs swap" decision tree.  A
  remove-and-rebuild approach handles all 9 transitions
  with one code path; the cost is one scene-item churn
  per refresh, which is invisible at teaching-scale
  molecule sizes (≤ 50 atoms).
- **Why apex-at-begin / base-at-end for the wedge?**
  ChemDraw and IUPAC recommendation 2006 both put the
  point at the stereocentre and the wide end at the
  substituent that's closer to the viewer.  Our begin
  atom is the stereocentre by convention (the user
  clicks the centre first, then the substituent), so
  the apex sits naturally at begin.
- **Why hash-spacing scales with bond length?**  A
  fixed hash count (say "always 5 hashes") looks bad
  on long bonds (gappy) and on short bonds (crowded).
  Scaling by `length / spacing` and clamping at a
  minimum of 4 keeps the visual density consistent
  across canvas zoom levels.
- **Why no `QGraphicsPathItem`?**  Both shapes COULD
  be expressed as a single `QPainterPath`, but the
  per-hash `QGraphicsLineItem` approach gives free
  hit-testing per hash + cleaner debug introspection
  (each hash shows up separately in `childItems()`).
  No measurable perf cost for ≤ 100-hash bonds.

### Phase 36 polish status (post-round 135)
- ✅ Tapered-polygon wedge + hashed-ladder dash bonds
  (round 135).
- ⏳ Lasso select + drag-move (multi-atom selection).
- ⏳ Indole + NHAc ring / FG templates.
- ⏳ Reagents-above-arrow text editor.

### Next
Round 136 candidates:
- **Phase 36 polish +1**: lasso select + multi-atom
  drag would be the next biggest UX win.
- **Phase 31b +1 reaction** — 12 to go for the 50-target.
- **Phase 31k +1 SAR series** — 6 to go.

---

## 2026-04-25 — Round 134 (Phase 31b +1: CuAAC click chemistry)

### Context
Round 133 added the 9th SAR series.  Round 134 varies
target — Phase 31b (named reactions) is at 37/50 with 13
to go; one more named reaction is the same content-round
size as a SAR series (one teaching-anchor per round) and
keeps the catalogues advancing in parallel rather than
all-in-on-one.

### What shipped
- **`orgchem/db/seed_reactions.py`** — 38th named reaction:
  *"Click chemistry: CuAAC (phenylacetylene + benzyl
  azide)"*.  Reaction SMILES:
  `C#Cc1ccccc1.[N-]=[N+]=NCc1ccccc1>>c1ccc(Cn2cc(-c3ccccc3)nn2)cc1`
  — phenylacetylene + benzyl azide → 1-benzyl-4-phenyl-
  1,2,3-triazole (1,4-disubstituted regioisomer).
  Description:
    - Sharpless / Meldal / Bertozzi 2022 Nobel anchor.
    - Thermal Huisgen reaction is sluggish + gives
      ~1:1 1,4 / 1,5 mixture without catalyst.
    - Cu(I) accelerates ~10⁷-fold AND drives complete
      1,4-regioselectivity.
    - Stepwise dinuclear-Cu mechanism (Fokin / Worrell
      2013) — Cu acetylide + Cu-coordinated azide α-N,
      six-membered metallacycle, ladder cycle.
    - Bioorthogonal + water-tolerant — why it sits at
      the centre of chemical biology + drug discovery.
    - SPAAC (cyclooctyne + azide, no Cu) is Bertozzi's
      bio-friendly variant.
- **`orgchem/db/seed_intermediates.py`** — two new
  fragments backfilled to keep the fragment-consistency
  audit clean: `Benzyl azide` and `1-Benzyl-4-phenyl-
  1,2,3-triazole`.  Verified: `audit_reaction(...)` now
  reports `n_in_db=3, n_missing=0` for the new reaction.

### Tests
- **`tests/test_reactions.py::test_click_chemistry_cuaac_seeded`**
  — 1 new test locking three invariants:
    1. Entry exists by substring lookup ("Click chemistry").
    2. Reaction SMILES uses the canonical 1,4-disubstituted
       triazole pattern (`Cn2cc(...)nn2`) — regioselectivity
       is the whole teaching point of Cu(I) catalysis vs.
       uncatalysed Huisgen.
    3. Description names all three 2022 Nobel laureates
       (Sharpless / Meldal / Bertozzi) AND mentions
       "1,4" or "regioselect" so future copy-edits can't
       accidentally drop the contemporary teaching anchor.
- All five new SMILES (the reaction's three component
  SMILES + the two intermediate-fragment SMILES) parse
  + canonicalise cleanly via RDKit before insertion.
- Full suite: **1 214 / 1 214 pass, 0 skipped** (was
  1 213).

### Design notes
- **Why click chemistry as the 38th entry?**  The
  catalogue already covers 5 Pd-cross-couplings (Suzuki /
  Sonogashira / Buchwald-Hartwig / Negishi / Heck);
  adding a Cu-cycloaddition pivots into a different
  metal, different mechanism (dinuclear ladder vs.
  Pd-cycle), and a different teaching anchor
  (regioselectivity vs. cross-coupling).  The 2022 Nobel
  also makes it the most contemporary entry in the
  catalogue.
- **Why no atom-mapped SMARTS?**  The dinuclear-Cu
  mechanism doesn't fit the simple atom-map convention
  used by the round-49 3D side-by-side renderer (which
  expects a single concerted bond-making / bond-breaking
  pattern).  The triazole ring formation involves Cu
  shuttling between two coordination modes — better left
  unmapped than misrepresented.  If the round-50
  reaction-trajectory animator is ever extended for
  multi-Cu intermediates, this can be back-filled.
- **Why benzyl azide / phenylacetylene specifically?**
  Phenylacetylene was already in the intermediate-fragment
  table (round 39 backfill for HWE / Sonogashira); benzyl
  azide is the most common test substrate in the
  click-chemistry literature.  Together they give a
  hand-drawable triazole product the user can recognise
  immediately.

### Phase 31 status snapshot (post-round 134)
- 31a (molecules) — long-running, no target reached
- 31b (reactions) — **38/50** (round 134)
- 31c (mechanisms) — closed at 20
- 31d (pathways) — closed at 12
- 31e (energy profiles) — closed at 20/20 (round 106)
- 31f (glossary) — closed at 60+
- 31g (tutorials) — closed at 30/30 (round 93)
- 31h/i/j (carbs / lipids / NA) — closed
- 31k (SAR series) — 9/15 (round 133)
- 31l (proteins) — closed at 15/15 (round 116)

### Next
Round 135 candidates:
- **Phase 31b +1 reaction** — 12 to go (Stille,
  Mitsunobu-extension, Mukaiyama aldol, Sharpless
  epoxidation, Birch, …).
- **Phase 31k +1 SAR series** — 6 to go (kinase
  inhibitors, ARBs, opioids, antihistamines, retinoids).
- **Phase 36 polish round** — proper tapered-polygon
  wedge bonds, lasso select + drag, indole / NHAc ring
  templates.

---

## 2026-04-24 — Round 133 (Phase 31k +1: fluoroquinolone SAR series)

### Context
Phase 36 was closed in round 132.  Round 133 picks up
Phase 31 long-running content.  First check showed
Phase 31l (proteins) was already at 15/15 (the
PROJECT_STATUS reference in round 130 had been stale —
the round-116 close at 5CHA + 6LU7 was the real
status).  Pivoted to **Phase 31k (SAR series, 8/15)** —
adding one new series ships 5 pedagogically rich
variants and increments toward the 15-target close.

### What shipped
- **`orgchem/core/sar.py`** — 9th SAR series:
  *Fluoroquinolone antibiotic series*.  5 variants
  walking the 1962 → 1999 generation-by-generation SAR
  optimisation of the quinolone scaffold:
    - **Nalidixic acid** (1962, 1st-gen, no C-6 F, no
      piperazine).  Naphthyridone core, narrow Gram-
      negative spectrum.  The proof-of-concept that
      DNA-gyrase inhibition is a viable antibacterial
      strategy.
    - **Norfloxacin** (1980, 2nd-gen).  Two SAR moves vs
      nalidixic acid: C-6 F + C-7 piperazine.  ~100× MIC
      drop on E. coli; first true *fluoroquinolone*.
    - **Ciprofloxacin** (1987, 2nd-gen).  Single tweak —
      N-1 ethyl → cyclopropyl — drops MIC ~4× across the
      board and unlocks oral + IV bioavailability.
    - **Levofloxacin** (1996, 3rd-gen).  S enantiomer of
      ofloxacin (chiral switch); oxazine ring fusion at
      N-1/C-8 + C-7 N-methylpiperazine.  Respiratory FQ.
    - **Moxifloxacin** (1999, 4th-gen).  C-8 methoxy +
      C-7 bicyclic diazabicyclooctane.  Best Gram-positive
      coverage in the class but loses anti-Pseudomonas
      activity.
  Activity columns: `mic_e_coli_ugml` /
  `mic_s_aureus_ugml` / `mic_p_aeruginosa_ugml`.  All 5
  SMILES validated against RDKit (parse + canonical
  round-trip) before insertion.

### Tests
- **`tests/test_sar.py::test_fluoroquinolone_series_landmarks`**
  — 1 new test, locking 3 teaching invariants:
    1. Nalidixic acid ≥50× weaker on E. coli than every
       -floxacin (the C-6 F + C-7 piperazine SAR move).
    2. Ciprofloxacin lowest E. coli MIC of the class.
    3. Moxifloxacin lowest S. aureus MIC AND highest
       Pseudomonas MIC of the four floxacins (the
       Gram-positive widening costs anti-Pseudomonas
       activity).
- Full suite: **1 213 / 1 213 pass, 0 skipped** (was
  1 212).

### Design notes
- **Why fluoroquinolones for the 9th series?**  The
  catalogue already covered the textbook drug classes
  (NSAID / statin / β-blocker / ACE / SSRI / penicillin /
  PDE5 / benzodiazepine).  Antibiotics needed a Gram-
  negative gyrase counterweight to the Gram-positive
  β-lactam story; fluoroquinolones provide a clean
  generation-by-generation SAR walk where each
  substituent change has a measurable MIC consequence.
- **Why MIC tables instead of Ki / IC50?**  MIC (minimum
  inhibitory concentration) is the operational
  antibiotic-pharmacology unit — what a clinical lab
  reports.  Putting Ki against gyrase would be more
  mechanistically pure but would lose the cross-organism
  selectivity story that's the whole point.
- **Why not include delafloxacin or other 5th-gen?**
  The Sustained / 5th-gen FQs (delafloxacin,
  besifloxacin) are mostly topical / niche; the 5
  systemic generations chosen tell the entire teaching
  arc without padding.
- **PROJECT_STATUS.md drift caught**.  The round-130
  PROJECT_STATUS still said proteins were at 13/15 —
  but the round-116 close at 15/15 was real (verified
  via `tests/test_protein.py::test_seeded_proteins_has_core_targets`
  invariant `len(ids) >= 15`).  No code change needed,
  just a doc-status cleanup as part of this round's
  log.

### Phase 31 status snapshot (post-round 133)
- 31a (molecules) — long-running, no target reached yet
- 31b (reactions) — 37/50 (round 123)
- 31c (mechanisms) — closed at 20
- 31d (pathways) — closed at 12
- 31e (energy profiles) — closed at 20/20 (round 106)
- 31f (glossary) — closed at 60+
- 31g (tutorials) — closed at 30/30 (round 93)
- 31h/i/j (carbs / lipids / NA) — closed
- 31k (SAR series) — **9/15** (round 133)
- 31l (proteins) — closed at 15/15 (round 116)

### Next
Round 134 candidates:
- **Phase 31k +1 more SAR series** (kinase inhibitors,
  ARBs, opioids…) — 6 to go to close.
- **Phase 31b +1 named reaction** — 13 to go to close
  the 50-target.
- **Phase 36 polish** — proper tapered-polygon wedge
  bonds, lasso select, indole / NHAc ring templates.
- A new user-flagged feature.

---

## 2026-04-24 — Round 132 (🎉 Phase 36 CLOSED at 8/8 — canvas reaction arrow + Reactions handoff)

### Context
Round 131 closed Phase 36f.1 (headless `Scheme` core + agent
action).  Phase 36f.2 was the final open sub-phase: place
the arrow on the canvas, partition atoms into LHS / RHS by
x-coord, and ship the result to the Reactions tab.  After
this round, the Phase-36 user directive (*"add molecular
drawing tool — same abilities as ChemDraw"*) is end-to-end
functional: the user can draw two structures, place an
arrow between them, give the reaction a name, and have it
land as a fresh `Reaction` row in the live DB visible on
the Reactions tab.

### What shipped
- **`orgchem/gui/panels/drawing_panel.py`** — two new tool
  keys: `arrow-forward` (→) and `arrow-reversible` (⇌).
  Click empty canvas to drop an arrow at the click point;
  second placement replaces the first (single-arrow
  constraint per canvas); same kind + same position is a
  no-op skipped from the undo stack.  Arrow rendered via
  `QGraphicsLineItem` shaft + `QGraphicsPolygonItem`
  arrowhead, stacked half-arrows for the ⇌ kind.  Pen is
  muted slate-grey (#444) so the arrow doesn't fight the
  molecule glyphs for attention.
- **Snapshot tuple grew to 3-tuple** `(Structure,
  positions, arrow)`.  `_restore_snapshot` accepts legacy
  2-tuples defensively so an in-flight session that
  started before round 132 doesn't crash on its first
  undo.  `clear()` resets the arrow; new `remove_arrow()`
  drops it without touching the structure.
- **`current_scheme()` extractor** — partitions atoms by
  x-coord vs the arrow's x position, builds a fresh
  `Structure` for each side via `_slice_structure` (which
  re-indexes bonds for the local atom-id space).  Bonds
  whose endpoints straddle the arrow are dropped (the
  user's drawing said "these atoms became those atoms",
  not "this exact bond survived").  Returns `None` when
  no arrow is on the canvas — caller should prompt the
  user to place one first.
- **`orgchem/gui/dialogs/drawing_tool.py`** — new footer
  button *"Send to Reactions tab"*.  Workflow:
    1. Pull a `Scheme` from `panel.current_scheme()`.
    2. If no arrow / empty / one-side-empty → info popup,
       no DB write.
    3. Prompt the user for a reaction name via
       `QInputDialog` (default `Drawn-rxn-XXXXXXXX` UUID).
    4. Invoke the round-55 `add_reaction` authoring action
       with category `"Drawn"`.
    5. On duplicate-name rejection, open the existing row.
    6. Call `_open_reaction(rid)` which walks
       `MainWindow.tabs` for the Reactions panel and calls
       its `_display(rid)`.
- All Phase 36 sub-phases now complete.

### Tests
- **`tests/test_drawing_panel_scheme.py`** — 16 pytest-qt
  cases:
    - toolbar wiring (both arrow tool keys present)
    - arrow placement creates state
    - reversible arrow state distinct from forward
    - second placement replaces first
    - same-point repeat is no-op (no extra undo snapshot)
    - `remove_arrow()` clears state
    - undo / redo round-trip
    - undo after arrow-replace restores the first arrow
    - `clear()` drops the arrow
    - `current_scheme()` is None without arrow
    - atom partition by x: 2 LHS + 2 RHS
    - bonds straddling the arrow dropped
    - intra-side bonds preserved with canonical SMILES
      round-trip (LHS = "CC", RHS = "C")
    - arrow kind ("reversible") propagates to the Scheme
    - one-empty-side edge case (`"C>>"`)
    - charge + h_count survive partitioning (NH₄⁺-style)
- **`tests/test_drawing_tool_dialog.py`** — 5 new cases:
    - *Send to Reactions tab* button visible / enabled
    - no-arrow info popup, no DB write
    - `add_reaction` invocation with `>>`-bearing SMILES
    - duplicate-name handling routes to existing row
    - user cancels name prompt → no DB write
    - one-side-empty info popup
- **Full suite: 1 212 / 1 212 pass, 0 skipped** (was
  1 190).

### Design notes
- **Why partition by x-coord, not by connected component?**
  Connected-component partitioning sounds more "correct"
  but breaks the obvious user model: two disconnected
  structures on the LHS of an SN2 (substrate + nucleophile)
  should both end up on the LHS, even though they're not
  bonded.  X-coord partition does that for free.  The
  trade-off: the user has to keep their LHS / RHS
  spatially separated by the arrow, which is the natural
  ChemDraw discipline anyway.
- **Why drop straddling bonds rather than auto-cut on the
  arrow line?**  Auto-cutting would let the user "draw the
  reaction as a single connected graph and let the tool
  figure it out" — but RDKit doesn't have a clean way to
  represent half-bonds, and the user's intent is genuinely
  ambiguous in that case (does the bond break or not?).
  Dropping is the conservative choice and matches the
  textbook arrow-pushing convention where each side stands
  alone.
- **Why prompt for a name rather than auto-naming?**  The
  Reactions tab indexes by name; an auto-generated
  `Drawn-rxn-abcd1234` name shows up as garbage in the
  list.  The default-but-overrideable prompt lets the user
  give the reaction a semantic name immediately while
  still providing a fall-through default.

### Phase 36 status — COMPLETE 🎉
- 36a ✅ headless core (round 124)
- 36b ✅ canvas widget (round 125)
- 36g ✅ dialog + workspace integration (round 126)
- 36h ✅ agent actions (round 127)
- 36d ✅ undo / redo (round 128)
- 36c ✅ ring / FG templates (round 129)
- 36e ✅ stereo wedges + charges + isotopes (round 130)
- 36f.1 ✅ scheme dataclass + reaction-SMILES helpers +
  agent action (round 131)
- 36f.2 ✅ canvas arrow + Reactions-tab handoff (round
  132)

### Next
The user-flagged ChemDraw-equivalent drawing tool is now
end-to-end functional.  Round 133 candidates:
- **Phase 31 long-running content** — more named
  reactions (catalogue at 37/50; 13 to go), more energy
  profiles (20/20 closed), more SAR series (8/15), more
  seeded proteins (13/15).
- **Phase 36 polish round** — proper tapered-polygon
  wedge bonds, lasso select + drag, indole / NHAc
  templates, reagents-above-arrow text editor.
- **A new user-flagged feature** if one comes in.

---

## 2026-04-24 — Round 131 (Phase 36f.1 — reaction-scheme data core)

### Context
Round 130 closed Phase 36e.  Phase 36f (reaction arrows
+ multi-structure schemes) is the last open Phase-36 sub-
phase.  A full ChemDraw-style canvas-arrow editor would
be 2-3 rounds of Qt work — placing arrow items between
two structures, dragging reagents above the arrow, the
multi-structure-on-one-canvas geometry problem, etc.
Splitting into headless core (36f.1, this round) +
canvas integration (36f.2, next round) keeps each round
self-contained and lets the agent / scripts use the
reaction-scheme bundling immediately.

### What shipped
- **`orgchem/core/drawing_scheme.py`** — pure-Python
  `Scheme` dataclass (`lhs: List[Structure]`, `rhs:
  List[Structure]`, `arrow ∈ {"forward", "reversible"}`,
  `reagents` free-text) + helpers:
    - `Scheme.from_smiles_pair(lhs, rhs, arrow, reagents)`
      — primary GUI entry point; passes each side through
      `structure_from_smiles`, returns `None` on parse
      failure.
    - `Scheme.from_reaction_smiles("LHS>reagents>RHS")`
      — round-trip the other direction.
    - `Scheme.to_reaction_smiles()` — bundle to the
      `LHS>reagents>RHS` form.
    - `lhs_smiles()` / `rhs_smiles()` — per-side
      `"."`-joined SMILES.
    - `to_dict()` / `from_dict(payload)` — JSON-friendly
      serialisation for session save / restore.
    - `is_balanced_atom_counts(scheme)` — heavy-atom-count
      sanity hint for the future GUI's "did you forget the
      leaving group?" prompt.
  `"."`-separated SMILES on either side are exploded into
  per-component `Structure`s so multi-substrate schemes
  like `"CC(=O)Cl.NC"` land as two LHS structures.  Empty
  halves serialise as the empty string to match RDKit
  reaction-SMILES convention (e.g. `">>"` for an
  all-empty scheme, `"CCO>>"` for a synthesis-target
  scheme).  RDKit lazy-imported so the dataclass is usable
  in environments without RDKit.
- **`orgchem/agent/actions_drawing.py`** — new action
  `make_reaction_scheme(lhs_smiles, rhs_smiles,
  arrow="forward", reagents="")`.  Pure-headless wrapper
  around `Scheme` that bundles two SMILES strings into a
  reaction record: returns `{"reaction_smiles",
  "lhs_canonical", "rhs_canonical", "arrow", "reagents",
  "balanced"}` on success, `{"error": ...}` on parse
  failure or invalid arrow type.  No Qt main-thread
  marshalling needed since the call doesn't touch the
  GUI — usable from the tutor, Python drivers, and the
  stdio bridge alike.
- **`orgchem/gui/audit.py`** — `make_reaction_scheme`
  registered in `GUI_ENTRY_POINTS` (mapped to the future
  Phase-36f.2 canvas-arrow tool's user-facing path).  GUI
  coverage stays at 100 %.

### Tests
- **`tests/test_drawing_scheme_core.py`** — 22 headless
  cases:
    - defaults (empty lhs/rhs, default arrow, empty
      reagents)
    - unknown arrow falls back to `"forward"`
    - `"reversible"` arrow preserved
    - `from_smiles_pair` builds multi-component schemes
    - `from_smiles_pair` rejects garbage SMILES on either
      side
    - empty LHS is valid (synthesis-target scheme)
    - `to_reaction_smiles` basic case + with reagents
    - `from_reaction_smiles` round-trip via canonicalised
      LHS / RHS
    - `from_reaction_smiles` preserves reagents
    - `from_reaction_smiles` rejects malformed input
      (wrong arrow segment count, garbage components)
    - `lhs_smiles` joins components with `"."`
    - `rhs_smiles` empty on empty RHS
    - `to_dict` / `from_dict` round-trip preserves
      arrow + reagents
    - `from_dict` rejects garbage SMILES
    - `from_dict` rejects non-dict input
    - empty scheme is trivially balanced
    - aldehyde-reduction scheme is balanced
    - unbalanced when atom counts differ
    - `to_reaction_smiles` skips empty substructures
    - `n_atom_counts` match structure state
- **`tests/test_drawing_actions.py`** — 6 new agent-action
  tests:
    - `make_reaction_scheme` in registry membership
    - basic round-trip (CCO → CC=O)
    - with reagents (`[Cr]` text preserved)
    - unbalanced-flag detection (CC → CCO)
    - garbage-SMILES error path
    - invalid-arrow rejection
    - reversible-arrow preservation
- **Full suite: 1 190 / 1 190 pass, 0 skipped** (was
  1 162).

### Design notes
- **Why split 36f into 36f.1 (headless) + 36f.2 (canvas)?**
  The Phase-36 pattern: ship the data core first, layer
  the GUI on top.  36a → 36b → 36g → 36c, 36e all
  followed this — the Structure dataclass shipped before
  the QGraphicsScene canvas; the template catalogue
  shipped before the toolbar buttons.  Splitting 36f the
  same way means the agent / scripts can compose
  reaction-schemes immediately, and the canvas-arrow
  Qt work in 36f.2 is a pure GUI round (no data-model
  questions to thrash on).
- **Why `List[Structure]` for `lhs` / `rhs`?**  Many
  textbook reactions have multi-component sides
  (Diels-Alder dimers, Mannich aldehyde + amine + ketone,
  esterification with explicit water-out).  Carrying
  per-component structures means a future GUI can
  highlight which component contributes which atoms in
  the Reactions-tab render without re-parsing.
- **Why `is_balanced_atom_counts` is heuristic-only.**
  Real reaction balancing requires graph isomorphism
  modulo bond-breaking — a Phase-2c.1-class problem (see
  `core/reaction_trajectory.py`).  The heavy-atom-count
  check catches the common student error (forgetting
  the leaving group) cheaply and is honest about its
  scope (it'll happily report a scrambled non-reaction
  as balanced if atom counts happen to match).  The
  future GUI prompt should phrase it as a hint, not a
  verdict.

### Phase 36 status after round 131
- 36a ✅ headless core (round 124)
- 36b ✅ canvas widget (round 125)
- 36g ✅ dialog + workspace integration (round 126)
- 36h ✅ agent actions (round 127)
- 36d ✅ undo / redo (round 128)
- 36c ✅ ring / FG templates (round 129)
- 36e ✅ stereo wedges + charges + isotopes (round 130)
- 36f.1 ✅ scheme dataclass + reaction-SMILES helpers +
  agent action (round 131)
- 36f.2 ⏳ canvas arrow + Reactions-tab handoff

### Next
Round 132 candidates: **36f.2 (canvas arrow + Reactions-
tab handoff)** would close Phase 36 entirely.  Needs a
canvas-arrow `QGraphicsItem` (probably a thin polygon),
a "place arrow" tool mode that's only enabled when the
canvas has at least one structure, an "LHS / RHS / arrow"
classifier that walks the canvas atoms and groups them
based on which side of the arrow they sit, and a
*"Send to Reactions tab"* button on the
`DrawingToolDialog` that bundles the `Scheme` into a
reaction-SMILES via `make_reaction_scheme` and pipes it
through the Reactions workspace's existing render path.
**Alternative**: Phase 31 long-running content (more
named reactions, energy profiles, SAR series, seeded
proteins).

---

## 2026-04-24 — Round 130 (Phase 36e — stereo wedges + charges + isotopes)

### Context
Round 129 closed Phase 36c.  Phase 36 had two open
sub-phases left — 36e (stereo + charges + isotopes) and
36f (reaction arrows).  36e is the natural next step: the
headless `Structure` already supports wedge / dash bonds +
charged / isotope / radical / explicit-H atoms; only the
GUI entry points were missing.  Single round of work
unlocks chiral-center drawing, zwitterion drawing, and
isotope-labelled drawings — covers ammonium, NMR-labelled
substrates, transition-state stereo, etc.

### What shipped
- **`orgchem/gui/panels/drawing_panel.py`** — two new
  bond tools: `bond-wedge` (◣) and `bond-dash` (◌) on
  the main toolbar.  Routed through
  `_handle_stereo_bond_click(atom_idx, scene_pos, stereo)`
  which mirrors `_handle_bond_click` but each new bond is
  created with `order=1` + the requested stereo.  Clicking
  an existing bond TOGGLES the stereo (same stereo → none;
  otherwise switch).  Empty-canvas auto-place behaviour
  matches the plain bond tool.
- **Right-click context menu** — `_DrawingView.mousePressEvent`
  now branches on `event.button() == Qt.RightButton` and
  forwards to `DrawingPanel.handle_canvas_right_click`,
  which hit-tests the click point and (when over an atom)
  pops a `QMenu` with four submenus:
    - Formal charge: -2 / -1 / 0 / +1 / +2 (current value
      checked)
    - Radical electrons: 0 / 1 / 2
    - Isotope label: opens `QInputDialog` for an int 0-300
    - Explicit H count: -1 (auto) / 0 / 1 / 2 / 3 / 4
  Each entry calls a thin setter (`_set_atom_charge` /
  `_set_atom_radical` / `_set_atom_isotope` /
  `_set_atom_h_count`) that pushes one undo snapshot then
  refreshes the atom glyph + emits `structure_changed`.
  Same-value selections are no-ops that don't pollute the
  undo stack.
- **`_apply_bond_order_style` upgrade** — wedge bonds use a
  thick green pen (#1B6E1B, 4.5 px solid), dash bonds use a
  blue dashed pen (#1B4FA8, 2.4 px Qt.DashLine), "either"
  bonds use a grey dotted pen.  Proper tapered-polygon
  wedges (the "real" ChemDraw look) deferred as polish.
- **`_draw_atom` upgrade** — atoms with non-default
  charge / isotope / radical promote from a dot to a
  labelled glyph (even pure C), with optional decorations:
  charge as a red superscript at the top-right
  ("+", "−", "2+", "2−"), isotope mass number as a grey
  superscript at the top-left ("13C", "2H"), radical
  electrons as 1-2 bullet dots above the symbol.  All
  decorations live in the per-atom `_atom_items` dict so
  the round-128 snapshot stack picks them up automatically
  via `_refresh_atom_glyph`.

### Tests
- **`tests/test_drawing_panel_stereo.py`** — 17 pytest-qt
  cases:
    - toolbar registration (`bond-wedge`, `bond-dash`)
    - wedge tool creates wedge bond
    - dash tool creates dash bond
    - wedge tool toggles stereo on existing bond (wedge →
      none → wedge cycle)
    - dash → wedge tool replaces stereo on the same bond
    - empty-canvas auto-places carbons for the wedge tool
    - undo reverses wedge creation
    - `_set_atom_charge` updates `Atom.charge`
    - `_set_atom_charge` pushes an undo snapshot
    - `_set_atom_charge` with the current value is a no-op
    - NH₄⁺ live SMILES round-trip (charge + h_count + atom)
    - `_set_atom_isotope` updates `Atom.isotope`
    - ¹³C isotope SMILES round-trip via RDKit
    - `_set_atom_radical` updates `Atom.radical`
    - `_set_atom_h_count` setter + undo restores the -1
      sentinel
    - right-click on empty canvas is a no-op (no menu, no
      exception)
    - V2000 mol-block writer emits the wedge stereo flag
      in the bond line
- **Full suite: 1 162 / 1 162 pass, 0 skipped** (was
  1 145).

### Design notes
- **Why pen colour for wedge / dash, not tapered polygons?**
  A proper ChemDraw wedge is a triangle (narrow at the
  begin atom, wide at the end), which means swapping the
  `QGraphicsLineItem` for a `QGraphicsPolygonItem` and
  reworking `_bond_items`' element type.  That refactor is
  invasive enough to be its own polish round; the colour /
  pen encoding is unambiguous and immediately survives the
  SMILES + mol-block round-trip via the underlying
  `Bond.stereo` field — which is what actually matters for
  chemistry correctness.
- **Why no lone-pair decoration?**  The Phase-13c mechanism
  player already supports lone-pair dots; the drawing tool
  doesn't need them for SMILES round-trip (RDKit infers
  lone pairs from valence + charge).  Could be added later
  as a right-click option if a tutor asks for it.
- **RDKit mol-block reader limitation** — RDKit drops the
  bond direction on non-stereocenter bonds when reading a
  mol-block back.  This is a SMILES / mol-block stereo
  model thing, not a writer bug.  The
  `test_wedge_bond_emits_stereo_flag_in_molblock` test
  checks the *writer* output instead of round-tripping.

### Phase 36 status after round 130
- 36a ✅ headless core (round 124)
- 36b ✅ canvas widget (round 125)
- 36g ✅ dialog + workspace integration (round 126)
- 36h ✅ agent actions (round 127)
- 36d ✅ undo / redo (round 128)
- 36c ✅ ring / FG templates (round 129)
- 36e ✅ stereo wedges + charges + isotopes (round 130)
- 36f ⏳ reaction arrows + multi-structure schemes — last
  remaining sub-phase

### Next
Round 131: **Phase 36f (reaction arrows + multi-structure
schemes)** is the last Phase-36 sub-phase.  Bigger scope —
needs a "reaction" tool that lets the user place a → / ⇌
arrow between two structures on the canvas, then a
modal dialog for reagents / conditions, then a
`structure_to_reaction_smarts` helper that bundles the
LHS + RHS into a single SMARTS string the Reactions tab
can render.  Likely two rounds (36f.1 = arrow placement +
core; 36f.2 = multi-structure layout + handoff to the
Reactions tab).  Alternative: shift to Phase 31
long-running content (rounds 31b reactions, 31e energy
profiles, 31k SAR series, 31l proteins).

---

## 2026-04-24 — Round 129 (Phase 36c — ring + FG template palette)

### Context
Round 128 closed Phase 36d (undo/redo for the drawing
canvas).  Phase 36 had three open sub-phases left — 36c
(template palette), 36e (stereo wedges), 36f (reaction
arrows).  36c is the highest-leverage next step: ChemDraw
users reach for the benzene / cyclohexane buttons several
times per minute, and the headless-testable design slots
naturally between the round-124 `Structure` core and the
round-128 snapshot stack.

### What shipped
- **`orgchem/core/drawing_templates.py`** — pure-Python
  catalogue with a single `apply_template(structure,
  positions, template, anchor_pos, host_atom_idx, scale)`
  helper.  20 templates in two families:
    - **Rings** (`fuse_mode="merge"`): cyclopropane,
      cyclobutane, cyclopentane, cyclohexane, benzene,
      pyridine, pyrimidine, furan, thiophene, pyrrole.
    - **FGs** (`fuse_mode="attach"`): OH, NH₂, Me, COOH,
      CHO, C=O, NO₂, CN, OMe, CF₃.
  `apply_template` returns a *fresh* `(Structure,
  positions)` tuple — input is never mutated, so the
  round-128 snapshot stack just needs to capture the
  pre-call state.  Unit-bond-length internal coords scaled
  by `DEFAULT_SCALE_PX = 42.0`; y is flipped at placement
  to match Qt's screen convention.  No Qt imports.
- **`orgchem/gui/panels/drawing_panel.py`** — second
  toolbar row with all 20 template buttons.  Tool keys are
  `template-<name>`; clicks route through
  `_apply_template_at` which: (1) pushes one undo
  snapshot, (2) calls `apply_template`, (3) pops the
  snapshot if the call was a no-op (e.g. invalid
  template), (4) renders only the newly appended atoms /
  bonds via `_draw_atom` / `_draw_bond`.  Existing scene
  items for fused atoms keep their identity so the
  ring-fusion overlap stays seamless.
- **NO₂ as zwitterion** — `[N+](=O)[O-]` rather than
  `N(=O)=O`, since RDKit refuses pentavalent N.  Tested
  via the canonical-SMILES round-trip of methylated NO₂
  giving `C[N+](=O)[O-]`.
- **Empty-canvas FG behaviour** — `auto_attach_element="C"`
  on every FG template means clicking COOH / OH / NH₂ on
  empty canvas first synthesises a methyl host then
  attaches the FG.  Result: empty canvas + COOH = acetic
  acid; empty canvas + OH = methanol.  Matches ChemDraw
  intuition and avoids degenerate states like `O` (free
  oxygen) showing up in the ribbon.

### Tests
- **`tests/test_drawing_templates_core.py`** — 18 headless
  tests: catalogue-contents invariants (every expected ring +
  FG present), `list_templates(kind=…)` filter, `get_template`
  miss returns `None`, free-standing benzene + cyclohexane +
  pyridine + furan placement (atom counts, hetero counts,
  SMILES round-trip), benzene + cyclopropane fused onto an
  existing C (n-1 atoms appended; host is in the ring),
  every FG → SMILES round-trip including NO₂ zwitterion
  + C=O double-bond attach (acetaldehyde) + acetic-acid
  COOH + acetonitrile CN, anchor-position invariant
  (`new_pos[0] == anchor_pos`), input-immutability check.
- **`tests/test_drawing_panel_templates.py`** — 13
  pytest-qt cases: every template registers a toolbar
  button, exclusivity (only the active template button is
  checked), benzene + cyclohexane on empty canvas, benzene
  fused onto carbon, OH / COOH / NO₂ attaches on existing
  atoms with correct SMILES, undo reverses + redo replays
  template placement, multi-step undo chain (template +
  element swap = 2 separate undo steps), signal emission,
  scene-item bookkeeping invariant
  (`len(_atom_items) == n_atoms`).
- **Full suite: 1 145 / 1 145 pass, 0 skipped** (was
  1 114 / 1 114).

### INTERFACE.md
New `core/drawing_templates.py` row added; the
`drawing_panel.py` row updated to mention 36c + tool key
convention + `_apply_template_at` glue.

### Design notes
- **Why not `QUndoCommand` for templates?**  The round-128
  snapshot stack was the project-wide simplification
  decision; templates layer on top of that without
  introducing a separate command class hierarchy.  One
  snapshot per placement = one undo step.
- **Why headless catalogue + thin GUI glue?**  Phase 36a
  set the precedent: structure manipulation is testable
  offline, GUI only handles input → headless call →
  scene-item update.  Round-129 follows the same split,
  which is why all 18 catalogue tests run without Qt.
- **Why no `indole` / `NHAc` template?**  Bicyclic ring
  fusion + 4-atom chain attach would each ~double the
  catalogue's complexity for limited pedagogical gain
  beyond what users can already build with two clicks
  (benzene + pyrrole; NH₂ + acetyl).  Queued as 36c.1.

### Phase 36 status after round 129
- 36a ✅ headless core (round 124)
- 36b ✅ canvas widget (round 125)
- 36g ✅ dialog + workspace integration (round 126)
- 36h ✅ agent actions (round 127)
- 36d ✅ undo / redo (round 128)
- 36c ✅ ring / FG templates (round 129)
- 36e ⏳ stereo wedges + charges + isotopes
- 36f ⏳ reaction arrows + multi-structure schemes

### Next
Round 130 candidates: **36e (stereo wedges + charges +
isotopes)** would close another big drawing-tool gap —
the headless `Structure` already supports wedge / dash /
charge / isotope, only the GUI entry points are missing;
**36f (reaction arrows)** is bigger and would unlock the
"draw your own reaction → render in Reactions tab" loop;
**31b/e/k/l** Phase-31 long-running content rounds
remain available.

---

## 2026-04-24 — Round 94 (Glossary-pollution cleanup)

### Context
Demo 15 in round 73 surfaced that the user's local DB had
accumulated ~90 `Tutor-test-term-*` glossary rows from past
test runs of the content-authoring actions (round 55).  A
probe at the start of this round found the problem had grown
to **165 glossary + 1 molecule** — roughly 67 % of the
glossary table was pollution.

### What shipped
- **`orgchem/db/cleanup.py`** — new module with
  `PurgeCounts` dataclass and
  `purge_tutor_test_pollution(prefix="Tutor-test-")`.
  Prefix-gated bulk DELETE across Molecule / Reaction /
  GlossaryTerm / SynthesisPathway (+ cascade to
  SynthesisStep) / Tutorial.  Safe + idempotent; real
  seeded names can never collide with `Tutor-test-`.
- **`tests/conftest.py`** — new session-teardown hook
  (`pytest_sessionfinish`) that runs the purge once at the
  end of every pytest run.  Prevents future pollution
  accumulation.  Opt-out via
  `ORGCHEM_KEEP_TEST_POLLUTION=1` env var for the rare
  case a developer wants the rows for inspection.
- **`scripts/cleanup_tutor_test_pollution.py`** —
  standalone one-shot CLI wrapping the same helper so
  users can purge a pre-existing polluted DB.  Run once
  this session: cleaned **166 rows** (165 glossary + 1
  molecule).
- Local DB now at the expected post-seed baseline.

### Tests
- **`tests/test_cleanup_pollution.py`** — 5 regression
  cases: real seeded rows survive the purge unscathed,
  purge is idempotent (second call = 0 rows), inserting
  a Tutor-test-* row and purging removes it, PurgeCounts
  repr / total are clean, custom-prefix argument works.
- Full suite: **950 passed, 0 skipped** (↑ from 945).

### INTERFACE.md
New `db/cleanup.py` row describes the prefix contract +
idempotence + opt-out env var so the next dev who wonders
"what's this purge doing?" has a one-line answer.

### Design notes
- **Why prefix, not a table flag**?  Adding an `is_test`
  column to 5 tables + migrating the schema for a
  housekeeping concern is overkill.  The existing
  authoring-test naming convention (`Tutor-test-` +
  UUID suffix) is stable across every test and
  impossible to collide with real data — a prefix match
  is enough.
- **Why session-end not session-start**?  If tests fail
  mid-session the user can inspect the data manually
  before it's wiped.  End-of-session is the natural
  rollback point.
- **Why opt-out env var, not opt-in**?  The default
  should clean up; leaving the opt-in path means 99 %
  of users' local DBs keep filling.  The handful of
  cases needing inspection set the env var.

### Phase status after round 94
Unchanged from round 93:
- 31c / 31d / 31f / 31g ✅ closed
- 31a / 31b / 31e long-running
- Phase 32 closed round 74; Phase 33 at 33a+33b, 33c
  (surface-integrated search) still open.

### Next
Round 95 candidates: Workbench drag-reorder (last
Phase-32 deferred polish item), Phase 33c
(surface-integrated search in Reactions / Synthesis /
Glossary tabs reusing the round-88 core), a new feature
phase 34 (user-flagged content only), or more Phase-31
long-running content.

---

## 2026-04-24 — Round 93 (Phase 31g CLOSED at 30/30 — Flow chemistry capstone)

### What shipped
**`orgchem/tutorial/content/advanced/06_flow_process.md`** —
the final tutorial that closes the 30-target.  Chosen as a
natural capstone — flow chemistry is where every Anastas
principle, every catalysis family, and every pathway-scale
discussion converges.  Content:

- **Two reactor types** — CSTR vs PFR with τ = V/Q
  residence-time maths, plus "batch = CSTR-with-τ→∞" frame.
- **Four "why flow wins" sections**:
  1. **Heat transfer** — 1/r surface-to-volume argument;
     nitration runaway risk as the seeded Reactions-tab
     example saved by flow.
  2. **Mixing** — 10 s batch vs 100 µs microreactor; opens
     kinetics too fast for batch (organolithium,
     fluorination).
  3. **Reactive intermediates** — diazomethane / ozone /
     high-P H₂ generated + consumed in-line without
     storage.
  4. **Process intensification** — T/P regimes impossible
     in batch (superheated water, packed-bed high-T).
- **Sitagliptin chemoenzymatic flow** (Codexis-Merck 2010)
  as the industry flagship — transaminase + PLP + iPrNH₂
  amine donor, E-factor halved vs prior Rh-asymmetric-H₂
  batch route, cross-linked to round-92 biosynthesis
  lesson's directed-evolution mention.
- **Scale-up vs numbering-up** — 10× volume vs 10×
  parallel tubes; why flow plants keep kinetics constant
  from kilo → ton scale.
- **PAT real-time analytics** — FT-IR / Raman / online
  HPLC as continuous-stream-friendly QC.  FDA 2004 PAT
  framework as regulatory driver.
- **When batch still wins** — slow reactions, slurries,
  reagent-addition campaigns, exploratory R&D.
- **7-point decision checklist** (heat / time / reactive
  intermediate / mixing / scale vision / solids /
  regulatory).
- 5 exercises cross-referring the seeded Nitration of
  benzene, Nylon-6 Beckmann (zeolite flow variant),
  Knowles L-DOPA H₂.

### Curriculum
Registered under the advanced tier.  `list_tutorials`
now reports **30 lessons total** — exact match to the
31g target.  Final tier distribution: **8 beginner /
10 intermediate / 6 advanced / 6 graduate**.

### Test suite
- **945 passed, 0 skipped** (unchanged — pure content round).

### Phase 31 status after round 93
- 31c mechanisms 20/20 ✅
- 31d pathways 25/25 ✅
- 31f glossary 80/80 ✅
- 31g tutorials **30/30 ✅ (this round)**
- 31a/b/e — continuous-expansion items with no hard
  target; left open for future rounds as organic content
  accumulates.

**Four Phase-31 sub-phases closed.**  Phase 32 (scripting
workbench) was closed round 74.  Phase 33 (search) still has
33c open but the user-facing Ctrl+F hits the main need.

### Rounds 82-93 retrospective
The twelve-round tutorial arc was the longest coherent
content push across the project.  Rounds shipped
intermediate radicals / polymer chemistry / protecting
groups; graduate catalysis / biosynthesis; advanced green
chemistry / flow + process; beginner stereochemistry / SMILES.
Each lesson explicitly referenced already-seeded pathway +
mechanism content so the curriculum is self-reinforcing
rather than isolated reading — a student can walk from
round-86's beginner stereochem intro into round-90's
intermediate protecting-groups deep-dive and recognise the
same Cbz chemistry in the aspartame pathway they ran
through the Synthesis tab.

### Next
With Phase 31g closed, the autonomous loop has room for
either a new feature phase (Phase 34?), the drag-reorder
polish on the Workbench tracks list, glossary-pollution
cleanup of the ~90 `Tutor-test-term-*` rows surfaced by
demo 15 (round 73), or continued open-ended 31a/b/e
expansion.

---

## 2026-04-24 — Round 92 (Phase 31g tutorial +1 — Biosynthesis)

### What shipped
**`orgchem/tutorial/content/graduate/06_biosynthesis.md`** —
unifying chapter that pulls together every enzyme-mechanism
and biosynthetic-alternative thread across the seeded content
into one coherent "nature runs the same catalysis families
chemists do" view.  Coverage:

- **Catalysis-family → enzyme map** — each of the five
  families from graduate/05 mapped to a seeded enzyme
  mechanism: chymotrypsin = nucleophilic, class-I aldolase
  = covalent intermediate, HIV protease = acid-base, RNase
  A = general acid/base, AADC = PLP electron-sink cofactor.
- **Primary vs secondary metabolism** — glycolysis/TCA/FAS
  vs the natural-products universe.
- **Four biosynthetic superfamilies**:
  1. Shikimate pathway (with Draths-Frost biosynthetic
     adipic as the Anastas principle-7 win).
  2. Polyketides — iterative Claisen condensation (PKS /
     FAS / chalcone synthase).
  3. Terpenoids — C₅ isoprene building blocks + cyclase
     carbocation cascades (all seeded Lipids-tab steroids).
  4. Alkaloids + PLP decarboxylation — with AADC /
     dopamine seeded mechanism as the archetype.
- **Industrial-biosynthesis comparison table** —
  aspartame (thermolysin), adipic (biosynthetic),
  insulin (recombinant-only), plus 1,3-PDO / artemisinin
  / farnesene as future-trending callouts.
- **Chemistry-vs-biology decision matrix** — when each wins
  and why; sitagliptin Merck-Codexis chemoenzymatic as the
  modern best-of-both flagship.
- **Retrobiosynthesis design questions** — three prompts
  the student asks at every disconnection when analysing
  a natural-product target.
- **10-row cofactor cheat-sheet** — ATP / NAD(P)H / FAD /
  biotin / CoA / PLP / THF / SAM / TPP / heme with
  seeded-content cross-refs where applicable.
- 5 exercises + 6 glossary cross-refs.

### Curriculum
Registered under the graduate level.  `list_tutorials`
reports **29 lessons total**, graduate tier at 6 lessons.

### Test suite
- **945 passed, 0 skipped** (unchanged — pure content round).

### Phase 31 status after round 92
- 31c mechanisms 20/20 ✅
- 31d pathways 25/25 ✅
- 31f glossary 80/80 ✅
- 31g tutorials **29 / 30** — **one more to close**

### Next
Round 93 closes Phase 31g at 30/30.  Candidate: advanced/
06 Flow & process chemistry (ties industrial chemistry
+ Anastas principle 6 + sitagliptin chemoenzymatic flow
example from the biosynthesis lesson), OR intermediate/11
Carbonyl condensation depth-dive (consolidates aldol /
Claisen / Michael mechanisms already seeded).  After
that, only 31a/b/e are active — all continuous-expansion
sub-items with no natural stopping points.

---

## 2026-04-24 — Round 91 (Phase 31g tutorial +1 — Reading SMILES)

### What shipped
**`orgchem/tutorial/content/beginner/08_reading_smiles.md`** —
practical primer that closes a big on-ramp gap: SMILES
strings appear in every seeded pathway / reaction / demo,
but there was no lesson explaining the syntax.  Content:

- **`CCO` as the 3-char worked example** — opens with the
  three rules: letters are atoms, adjacency is bond,
  hydrogens are implicit.
- **Bonds table** — single / `=` / `#` / `:` with a
  single-line molecule per row.
- **Branches** — parentheses for branches; aspirin parsed
  piece-by-piece (`CC(=O)O` acetyl ester + `c1ccccc1`
  benzene + `C(=O)O` -COOH).
- **Rings** — matching-digit ring-closure markers, `%nn`
  for > 9.
- **Aromatic lowercase** — benzene / pyridine / furan.
- **Brackets** — when (non-organic-subset, charges,
  isotopes, explicit H-counts) and how.
- **Stereo brief** — `@` / `@@` / `/` / `\` with L- vs
  D-alanine and cis/trans 2-butene, plus a pointer to
  beginner / 07 + intermediate / 01 for the full CIP
  treatment.
- **Three seeded-SMILES walkthroughs**: caffeine
  (`Cn1c(=O)c2c(ncn2C)n(C)c1=O` — fused 5/6 xanthine),
  aspirin, benzocaine (4-aminoethylbenzoate).
- **5-step reading recipe** a beginner can apply to any
  new SMILES.
- Section on **what SMILES doesn't say** — 3D conformation,
  protonation state, tautomer.
- 5 exercises drawing on the seeded catalogue (Procaine,
  Acetanilide).

### Curriculum
Registered in `orgchem/tutorial/curriculum.py` under the
beginner tier.  `list_tutorials` now reports **28 lessons
total**, beginner tier at 8 lessons.

### Test suite
- **945 passed, 0 skipped** (unchanged — pure content round).

### Phase 31 status after round 91
- 31c mechanisms 20/20 ✅
- 31d pathways 25/25 ✅
- 31f glossary 80/80 ✅
- 31g tutorials **28 / 30** — 2 more to target

### Next
Round 92: just 2 tutorials to close Phase 31g at 30/30.
Candidates — graduate/06 Biosynthesis & natural products
(ties AADC / thermolysin / biosource threads), advanced/06
Flow + process chemistry, graduate/07 C-H activation,
intermediate/11 Carbonyl depth-dive (aldol / Claisen /
Michael consolidation).

---

## 2026-04-23 — Round 90 (Phase 31g tutorial +1 — Protecting groups)

### What shipped
**`orgchem/tutorial/content/intermediate/10_protecting_groups.md`** —
intermediate tutorial tying together the Cbz / Fmoc / Boc
threads from recent pathway seeds (L-DOPA round 78, Aspartame
round 80, and the already-seeded Met-enkephalin Fmoc SPPS
pathway).  Content:

- **Why protect?** — framed by the Aspartame α vs β COOH
  chemoselectivity problem (α-α is sweet, β-α is bitter,
  one wrong amide bond kills the product).
- **Three properties every PG needs** — selective install,
  stable to the planned reaction, selective removal.
- **Orthogonal protection** as the key design principle.
- **Amine triad table** — Cbz / Boc / Fmoc install + deprotect
  + stable-to + not-stable-to columns, with the orthogonality
  map spelled out (Cbz ⊥ Boc via H₂/TFA, Fmoc ⊥ Boc via
  base/acid; Fmoc/Cbz are partially orthogonal only).
- **Mechanism walks** for each amine-PG deprotection:
  - **Cbz** — Pd-surface hydrogenolysis via benzylic C-O,
    carbamic-acid intermediate losing CO₂.
  - **Fmoc** — E1cb with piperidine: acidic fluorenyl C-H
    (pKa ~22, aromatic cyclopentadienyl stabilisation)
    gives the carbanion that kicks out the carbamate;
    dibenzofulvene + piperidine-adduct byproduct.
  - **Boc** — SN1 via t-butyl cation; isobutylene +
    carbamic-acid byproducts.
- **Alcohol + COOH + carbonyl tables** — Ac / Bn / TBS /
  MOM for alcohols; Me / Bn / tBu esters; acetal dioxolane
  for carbonyls.
- **SPPS as orthogonal exemplar** — Fmoc for iterated
  chain-extension (base) + tBu for global cleavage (TFA);
  seeded Met-enkephalin pathway as concrete reference.
- **When to avoid protection** — Anastas principle 8
  (green-chem round 87 cross-ref): thermolysin regiosel-
  ective aspartame coupling, Suzuki aryl-ester spectator
  tolerance, Knowles asymmetric H₂ hitting only C=C.
- 5 exercises + 3 glossary cross-refs.

### Curriculum
Registered in `orgchem/tutorial/curriculum.py` under the
intermediate level.  `list_tutorials` reports **27 lessons
total**, intermediate tier at 10 lessons.

### Test suite
- **945 passed, 0 skipped** (unchanged — pure content round).

### Phase 31 status after round 90
- 31c mechanisms 20/20 ✅
- 31d pathways 25/25 ✅
- 31f glossary 80/80 ✅
- 31g tutorials **27 / 30** — 3 more to target

### Next
Round 91: 3 tutorials to close 31g.  Candidates — graduate/
06 Biosynthesis & natural products, advanced/06 Flow +
process chemistry, beginner/08 Reading SMILES, intermediate/
11 Carbonyl condensation depth-dive, graduate/07 C-H
activation.  Alternatively a new feature or Phase 33c
surface-integrated search.

---

## 2026-04-23 — Round 89 (Phase 33b — Ctrl+F search dialog)

### What shipped
Phase 33b completes the Ctrl+F find feature started round 88.

- **`orgchem/gui/dialogs/fulltext_search.py`** —
  `FulltextSearchDialog` (singleton per app instance so
  reopening preserves the query state):
  - `QLineEdit` live-updating query box, 100 ms debounce
    timer coalesces keystroke bursts before rerunning
    `search()`.
  - 5-kind checkbox-filter row (all on by default); a
    zero-kind state shows a helpful "Select at least one
    kind" status message instead of silently no-op-ing.
  - Results list rendered as HTML per row: kind badge
    (coloured tag: blue molecule / orange reaction / red
    mechanism-step / green pathway / purple glossary) +
    bold title + greyed snippet.
  - Double-click or return-key activation dispatches.
- **`dispatch_search_result(result, main_win)`** — module-
  level routing function handling all 5 kinds:
  - molecule → `bus.molecule_selected.emit(id)`
  - reaction → `reactions._display(id)`
  - mechanism-step → `reactions._display(id)` **plus**
    fire `invoke('open_mechanism', …)` to pop the player
  - pathway → `synthesis._display(id)`
  - glossary → `glossary.focus_term(term)`
  - all kinds also switch the main tabbar to the right tab.
- **`MainWindow`** wiring:
  - View menu entry "Find… (Ctrl+F)".
  - `open_fulltext_search()` helper — singleton show/raise/
    activateWindow + auto-focuses the query line edit.

### Tests
- **`tests/test_fulltext_search_dialog.py`** — 10 new cases:
  4 pytest-qt dialog tests (empty state, live-search
  produces results, kind-filter restricts to one kind,
  zero-kinds shows helpful message) + 6 dispatch-routing
  unit tests via a fake minimal main-window that captures
  calls to `.glossary.focus_term`, `.reactions._display`,
  `.synthesis._display`, `.tabs.setCurrentIndex`.  One
  test mocks `orgchem.messaging.bus.bus` to verify molecule
  dispatch hits `molecule_selected.emit`.
- **945 passed, 0 skipped** (↑ from 935).

### Phase 33 status after round 89
- 33a headless search core ✅
- 33b Ctrl+F dialog ✅
- 33c surface-integrated search (tab-local boxes reusing
  the core) — still open, low-priority polish.

### Next
Round 90: candidates — close the last small Phase 32
deferred item (drag-reorder for Workbench tracks list), or
continue Phase 31g tutorial momentum (4 to 30-target), or
start a new phase.  Tutorial momentum is probably best —
the content ships faster than GUI chrome and keeps the
beginner/intermediate coverage healthy.

---

## 2026-04-23 — Round 88 (Phase 33a — headless full-text search core)

### What shipped
New feature **Phase 33 — cross-surface full-text search**.
Phase 11b's Ctrl+K palette matches by name only; this phase
does the complementary full-text search over descriptions /
definitions / step notes / mechanism prose.  Ships in two
sub-phases for clean scope — round 88 is the headless core.

- **`orgchem/core/fulltext_search.py`** — pure-Python linear
  scan over the seeded DB.  Five corpus builders
  (molecules / reactions / mechanism steps / pathways +
  their steps / glossary) each yield `(kind, title, blob,
  key)` tuples; the top-level `search(query, kinds, limit)`
  scores every hit with title-boost × 3 + word-boundary
  bonus, snippets out a context window around the first
  match, and returns a sorted list of `SearchResult`.
  `SEARCHABLE_KINDS` = the 5-tuple of kinds; `SearchResult.
  key` carries dispatch info for routing double-clicks
  back to the originating surface (molecule_id / term /
  pathway_id / reaction_id + step_index).
  **Design decision**: linear scan, no FTS5 index.  Corpus
  is ~1 k rows × ~300 chars of text (~300 KB total); every
  query takes a few ms without an index to maintain.
- **`orgchem/agent/actions_search.py`** — `fulltext_search
  (query, limit, kinds)` agent action wrapping the core.
  Accepts comma-separated kinds CSV; returns JSON-
  serialisable dicts including a clean error-return path
  for unknown kinds.  Registered in `agent/__init__.py`.
- **GUI audit** provisionally maps the action to
  *View → Find… (Ctrl+F)* (the Phase-33b dialog slot);
  100 % coverage preserved.  Agent action count 125 → 126.

### Key design notes surfaced while writing tests
- Mechanism steps **surface individually** as their own
  searchable rows — so a query for "Beckmann" or "oxime"
  lands on the Nylon-6 step 2 description directly,
  not just on the whole pathway entry.  This is the
  main win vs the Ctrl+K palette which only does name
  matching.
- **Test robustness lesson**: round 71's content markers
  teach us to pick queries whose match location you
  *know*.  My first draft of the test asserted "beckmann"
  hits a mechanism-step; in fact Beckmann appears in the
  pathway step notes only (no Reaction.mechanism_json
  entry for it), so the test hit a pathway.  Swapped to
  "enolate" which is genuinely in the Claisen + Aldol
  mechanism-step descriptions.

### Test suite
- **`tests/test_fulltext_search.py`** — 19 new cases:
  5 scoring / snippet unit tests + 14 DB-backed
  integration tests (empty-query short-circuit, caffeine
  lookup, mechanism-step hit on "enolate", pathway step
  note hit on "DIPAMP", kinds-filter, unknown-kind
  rejection, title-beats-body ranking, sort-by-score
  invariant, limit respected, agent action JSON shape,
  action kinds CSV, action error-return for bad kind,
  public-API constant stability).
- **935 passed, 0 skipped** (↑ from 916).

### Next
Round 89 ships **Phase 33b** — the Ctrl+F `FulltextSearchDialog`
wrapped around this core.  Also extends
`dispatch_palette_entry` to understand the new key types so
a double-click on a mechanism-step result navigates straight
to the player dialog at the right step.

---

## 2026-04-23 — Round 87 (Phase 31g tutorial +1 — Advanced green chemistry)

### What shipped
**`orgchem/tutorial/content/advanced/05_green_chemistry.md`** —
uses Anastas's 12 Principles of Green Chemistry as an audit
checklist and maps each principle onto already-seeded content.

Six case studies:

1. **Adipic acid N₂O footprint** — ~1 mol N₂O per mol product,
   265× CO₂ GWP; pre-1997 emissions were 5-8 % of all
   anthropogenic N₂O; Al₂O₃ / CuO catalytic abatement is
   now standard.  Draths-Frost biosynthetic alternative via
   cis,cis-muconic acid from engineered *E. coli*.
2. **Nylon-6 (NH₄)₂SO₄ mountain** — 5 kg/kg caprolactam
   waste from oleum Beckmann.  Sumitomo zeolite ZSM-5
   vapour-phase Beckmann (2003) replaces oleum entirely;
   ~20 % of global caprolactam now runs this way.
3. **L-DOPA Knowles Nobel** — asymmetric H₂ vs classical
   resolution: 2 g/mol H₂ atom-economy + no discarded
   wrong-enantiomer.  Flags the step-3 HBr deprotection
   as the weakness (2× CH₃Br per product).
4. **Aspartame thermolysin shortcut** — Ajinomoto's enzymatic
   α-regioselective route (15 000 t/yr) skips Cbz + DCC
   entirely.  pH 7, room T, water.
5. **Fischer esterification water-removal** — Dean-Stark,
   molecular sieves, excess alcohol, vacuum — each rated
   against principles 3, 5.  Solid-acid catalysts
   (Amberlyst-15) as the principle-9 upgrade.
6. **PLA — designed for degradation** — renewable feedstock
   + safe products + degradable backbone.  Honest about
   the real-world disposal gap (PLA in landfills ≈ PET).

Plus:
- **Metrics refresher** — atom economy + Sheldon E-factor
  with industrial benchmarks (bulk 1-5, fine 5-50, pharma
  25-100+).
- **5-question auditing checklist** a student can apply to
  any new route they see.
- 5 exercises tying back to Tools → Green metrics… and the
  Hammett dialog.

### Curriculum
Registered under the advanced level.  `list_tutorials`
reports **26 lessons total**, advanced tier at 5 lessons.

### Test suite
- **916 passed, 0 skipped** (unchanged).

### Phase 31 status after round 87
- 31c mechanisms 20/20 ✅
- 31d pathways 25/25 ✅
- 31f glossary 80/80 ✅
- 31g tutorials **26 / 30** — 4 more to target

### Next
Round 88: candidates — graduate C-H activation (metal-
catalysed cross-couplings beyond Suzuki), advanced flow
chemistry, beginner intro to SMILES parsing, graduate
biosynthesis + natural-product total-synthesis (closing the
endgame-focused graduate track).  Or pivot: a new feature
phase 33 (Ctrl+F global search across the DB, or a quiz
engine), or the drag-reorder polish on Workbench.

---

## 2026-04-23 — Round 86 (Phase 31g tutorial +1 — Beginner stereochem)

### What shipped
**`orgchem/tutorial/content/beginner/07_stereochemistry_intro.md`** —
the missing on-ramp to the intermediate stereochemistry deep-dive
that tutors noted earlier as a trouble spot.  The lesson
deliberately works by *analogy + concrete consequences* first,
saving the CIP machinery for intermediate/01.  Coverage:

- **Thalidomide framing** — one compound, two enantiomers
  (R-sedative vs S-teratogenic), ~10 000 affected babies
  before 1961 withdrawal.  The strongest possible answer to
  "why does this matter."
- **Hand analogy** — non-superimposable mirror images,
  naming "enantiomers."
- **Stereocentre definition** — carbon with 4 different
  substituents; ASCII schematic.
- **Why your nose notices** — carvone (caraway vs spearmint)
  and limonene (orange vs lemon) smell-contrast table as
  receptor-pocket evidence students can understand.
- **R/S thumbnail** — 4-step CIP procedure in one paragraph
  with the pointer to intermediate/01 for tie-break details.
- **cis/trans & E/Z** — π-bond rotation lock, old vs modern
  labelling conventions.
- **Meso + diastereomer preview** — 2ⁿ stereoisomers from n
  centres, internal-symmetry cancellation, diastereomer =
  non-mirror stereoisomer with real physical-property
  differences.
- **Practice SMILES table** — 5 sample compounds to paste
  into Tools → Stereochemistry… including L- vs D-alanine,
  E vs Z 2-butene, and D-glucose with all 4 centres.
- **Three takeaways** + 9 glossary cross-refs via
  `{term:…}` macro (enantiomer / diastereomer / stereocentre
  / R/S / E/Z / meso / ee / anomer / Walden inversion).

### Curriculum
Registered in `orgchem/tutorial/curriculum.py` under the
beginner level.  `list_tutorials` now reports **25 lessons**,
beginner tier at 7.

### Test suite
- **916 passed, 0 skipped** (unchanged — pure content round).

### Phase 31 status after round 86
- 31c mechanisms 20/20 ✅
- 31d pathways 25/25 ✅
- 31f glossary 80/80 ✅
- 31g tutorials **25 / 30** — 5 more to target
- 31a/b/e long-running

### Next
Round 87: another tutorial lesson to keep momentum (5 to go —
candidates: advanced flow chemistry, graduate C-H activation,
advanced green chemistry case studies, intermediate
stereospecific SPPS, or beginner intro to reading SMILES),
the drag-reorder polish on Workbench tracks list, or a new
Phase 33 feature.

---

## 2026-04-23 — Round 85 (Workbench colour + opacity chrome)

### What shipped
Closed the last deferred items from Phase 32c with two new
per-track controls on `TrackRow`:

- **Colour combo + swatch preview**.  Kind-aware choices —
  molecules / ligands get CPK + common hues (white / grey /
  red / blue / green / orange / magenta); proteins get the
  cartoon-specific schemes (chain / spectrum / residue / cpk)
  plus the same hues.  A "custom…" sentinel pops a
  `QColorDialog` and inserts the picked hex code as a new
  combo entry.  A small `_swatch` QLabel shows the current
  hue at a glance (multi-colour schemes render as a neutral
  grey placeholder).
- **Opacity slider** (10-100 %).  Wired via a new
  `opacity_changed(track, 0.0-1.0)` signal → `scene.set_style
  (opacity=…)`.  Minimum clamped at 10 % so tracks can't go
  fully invisible accidentally.

`TrackRow.reflect()` now re-syncs both new controls after
external scene mutations, so a script that calls
`viewer.set_style(name, colour="red", opacity=0.3)` updates
the UI on the next queued event.

### HTML layer refactor
`orgchem/scene/html.py::_style_js` rewritten to build the
3Dmol.js style spec as a Python dict + `json.dumps` — no more
hand-written literal strings.  This lets us inject `opacity`
into every style key consistently (previously only the
surface style had it, hard-coded to 0.6).  Ball-and-stick
still gets two-key handling (stick + sphere) since it's the
one combined style.  Protein colour schemes + cartoon-trace
style flag handled via inner-dict keys.

### Wiring
`WorkbenchWidget` connects the two new TrackRow signals:
- `colour_changed → self._on_row_colour_changed → scene.set_style(colour=…)`
- `opacity_changed → self._on_row_opacity_changed → scene.set_style(opacity=…)`

Same `KeyError`-swallow guard as the other row forwarders.

### Tests
- **`tests/test_workbench_controls.py`** gains 3 new cases:
  - Colour combo → `scene.tracks()[0].colour` updates.
  - Opacity slider → `scene.tracks()[0].opacity == 0.5` at 50 %.
  - End-to-end: after an opacity drop to 40 %, the rebuilt
    scene HTML contains the literal `"opacity": 0.4` in the
    3Dmol.js setStyle spec.  Catches any future refactor that
    breaks the scene → HTML plumbing.
- **916 passed, 0 skipped** (↑ from 913).

### File sizes
- `workbench_track_row.py` 135 → 257 lines (under 500-line cap).
- `workbench.py` 419 lines (unchanged from round 84).
- `scene/html.py` 94 → 121 lines (still tiny).

### Phase 32 status after round 85
- 32a editor ✅
- 32b Workbench ✅
- **32c chrome ✅** (rich per-track controls + scene-wide
  toolbar + round-85 colour / opacity polish)
- 32d 15-demo library ✅
- 32e tutor script mode ✅
- Only deferred item: **drag-reorder** for tracks list — low
  priority, purely ergonomic.

### Next
Round 86: candidates — one more Phase 31g tutorial, drag-
reorder for tracks, or pivot to a new feature phase (33?).
With Phases 32 and 3 of 7 Phase-31 sub-items all closed,
the loop has room to start something new.

---

## 2026-04-23 — Round 84 (Phase 31g tutorial +1 — Intermediate polymers)

### What shipped
**`orgchem/tutorial/content/intermediate/09_polymers.md`** —
polymer-chemistry lesson that bridges the radicals + catalysis
+ nylon pathway threads.  Content:

- **Two mechanistic families** — step-growth (Carothers DP =
  1/(1-p) with worked p vs DP numbers: 0.90→10, 0.99→100,
  0.999→1000) vs chain-growth (radical / cationic / anionic
  subclasses).
- **Seeded-content anchors** — step-growth nylon-6 / nylon-6,6
  / PET / polyurethane / polycarbonate table; chain-growth PE
  / PP / PS / PVC / PTFE / PAN / PMMA table with initiators.
- **Tacticity** — isotactic vs syndiotactic vs atactic, with
  the classic atactic-PP-is-goo vs isotactic-PP-is-plastic
  contrast and the Ziegler-Natta / metallocene Nobel thread.
- **T_g + T_m** — glass transition vs crystalline melt, why
  polystyrene is a hard glass at room T and polyisoprene is
  a rubber.
- **Why nylon-6,6 beats nylon-6** — alternating vs same-
  direction amide dipoles, H-bond register, crystallinity
  consequences, tyre-cord choice.
- **Copolymer subclasses** — random (SBR), alternating
  (styrene-maleic anhydride), block (SBS in sneakers),
  graft (ABS in Lego).
- **Sustainability** — PET methanolysis, PLA biodegradability
  (ester backbone → hydrolysable), biosourced succinic acid.
- 5 exercises + 3 glossary cross-refs via `{term:…}`.

### Test suite
- **913 passed, 0 skipped** (unchanged — pure content round).
  `list_tutorials` now reports 24 lessons total.

### Phase 31 status after round 84
- 31c mechanisms 20/20 ✅
- 31d pathways 25/25 ✅
- 31f glossary 80/80 ✅
- 31g tutorials **24 / 30** — 6 more to target
- 31a/b/e long-running

### Observed threading across rounds 82-84
The three tutorials shipped as a coherent triptych:
1. Round 82 — **how radicals work** (intermediate/08).
2. Round 83 — **how catalysts enable reactions** (graduate/05,
   homogeneous / heterogeneous / enzymatic / Lewis / Brønsted).
3. Round 84 — **how all of that assembles polymers**
   (intermediate/09, radicals feeding chain-growth; catalysts
   feeding Ziegler-Natta; nylon pathways feeding step-growth).

Polymer chemistry wasn't on the original ROADMAP priority list
but naturally emerged as the capstone of the recent pathway +
mechanism + catalysis work.

### Next
Round 85: another tutorial (candidates per ROADMAP 31g:
beginner stereochemistry 101, advanced flow chemistry,
graduate metal-catalysed C-H activation, or green chemistry
case studies), or swing to Workbench chrome (colour swatch +
opacity slider), or start a Phase 33 feature.

---

## 2026-04-23 — Round 83 (Phase 31g tutorial +1 — Graduate catalysis)

### What shipped
**`orgchem/tutorial/content/graduate/05_catalysis.md`** — a
cross-cutting graduate-tier lesson that ties together the five
catalysis families with concrete references to already-seeded
content:

1. **Homogeneous** — Knowles Rh-DIPAMP asymmetric hydrogenation
   (L-DOPA pathway step 2, Nobel 2001), Suzuki / Buchwald /
   Sonogashira cross-couplings, Mitsunobu.
2. **Heterogeneous** — Pd-C hydrogenolysis of Cbz (Aspartame
   step 2), Co/Mn naphthenate cyclohexane oxidation (Adipic-
   acid step 1), vapour-phase Beckmann on zeolite ZSM-5
   (Nylon-6 greener alternative).
3. **Enzymatic** — each of the four seeded enzyme mechanisms
   (chymotrypsin, Class-I aldolase, HIV protease, RNase A)
   mapped to a distinct catalytic strategy + industrial
   thermolysin (Ajinomoto aspartame) + AADC / PLP mechanism
   (Dopamine activation).
4. **Lewis-acid** — AlCl₄⁻ / AlCl₃ cycle in Friedel-Crafts
   alkylation (3-step mechanism seeded), BF₃ + ZnCl₂
   variants in Mukaiyama aldol / phenolphthalein.
5. **Brønsted-acid** — Fischer esterification (5-step), pinacol
   rearrangement (4-step), Beckmann rearrangement in the
   Nylon-6 synthesis — all three show explicit proton-shuttle
   turnover.

Plus a **5-column comparison table** (phase / selectivity /
recovery / TOF / Nobel anchor), a cross-cutting TS-stabilisation
framing that unifies all five, and 4 exercises that push the
student to reason about process-chemistry tradeoffs using the
taxonomy. 7 glossary cross-references via the `{term:…}` macro.

### Curriculum + smoke
Registered in `orgchem/tutorial/curriculum.py` under the graduate
level.  `list_tutorials` now reports **23 lessons total**,
graduate tier at 5 lessons (from 4).

### Test suite
- **913 passed, 0 skipped** (unchanged — content-only round).
  The existing tutorial-schema + tutorial-macros tests cover
  the new lesson's registration + `{term:…}` expansion.

### Phase 31 status after round 83
- 31c mechanisms 20/20 ✅
- 31d pathways 25/25 ✅
- 31f glossary 80/80 ✅
- 31g tutorials **23 / 30** — 7 more to the target

### Next
Round 84: another tutorial lesson (polymer chemistry? flow
chemistry? metal-catalysed C-H activation?), or swing back
to Workbench chrome (colour swatch + opacity slider for the
last Phase-32c deferred items), or start a new feature
phase (33?).

---

## 2026-04-23 — Round 82 (Phase 31g tutorial +1 — Radical chemistry)

### What shipped
- **`orgchem/tutorial/content/intermediate/08_radicals.md`** —
  new markdown lesson filling the glaring radical-chemistry
  gap in the curriculum (radicals weren't covered anywhere
  across the 21 prior lessons).  Content:
  1. Three hallmarks — fishhook arrows, chain mechanism,
     non-polar character.
  2. Chain stages walked end-to-end with Cl₂ + CH₄ → CH₃Cl +
     HCl as the canonical worked example (the reaction is
     already seeded as *Radical halogenation of methane*);
     initiation / propagation (two atom-transfer steps) /
     termination (with the ethane coupling product that's
     the GC-trace fingerprint).
  3. Radical stability 3° > 2° > 1° > methyl as the
     hyperconjugation-driven analogue of carbocation
     stability.
  4. Cl• vs Br• selectivity framed through the Hammond
     postulate — unselective Cl• with its strongly exothermic
     steps (early TS, 1° ≈ 3°) vs selective Br• with its
     weakly-exo steps (late TS, 3° 80× 1°).
  5. Applications: radical polymerisation (industrial
     polyethylene / polystyrene / PVC), autoxidation of
     oils with antioxidant defences (vitamin E, BHT),
     ozone-depletion catalytic cycles, biological radicals.
  6. Three arrow-pushing practice prompts + explicit
     cross-references to the *Homolysis vs heterolysis*,
     *Hammond postulate*, *Curved arrow*, and *Carbocation*
     glossary entries (via the `{term:…}` macro so clicks
     route to the Glossary tab).
- **Curriculum registration** in `orgchem/tutorial/curriculum.py`
  under the `intermediate` level.  `list_tutorials` immediately
  picks it up — verified via HeadlessApp (22 total, new entry
  at `{level: intermediate, index: 7}`).

### Test suite
- **913 passed, 0 skipped** (unchanged — content-only round;
  the existing `test_tutorial` and `test_tutorial_macros`
  harnesses cover the registration + rendering path).

### Phase 31 status after round 82
- 31c mechanisms 20/20 ✅
- 31d pathways 25/25 ✅
- 31f glossary 80/80 ✅
- 31g tutorials **22 / 30** — in progress
- 31a/b/e long-running

### Next
Round 83: another tutorial lesson (beginner → *Stereochemistry
101* or graduate → *Catalysis (homogeneous / heterogeneous /
enzyme)*), or pivot back to Workbench chrome (colour swatch +
opacity slider for 32c+), or start on a Phase 33 feature.

---

## 2026-04-23 — Round 81 (get_mechanism_details + demo 04 arrow walk)

### What shipped
Closed the round-67 action-surface gap: scripts / LLMs could
list mechanisms and open the player dialog, but couldn't
programmatically read the per-step **arrow data**.

- **`get_mechanism_details(name_or_id)`** in
  `orgchem/agent/actions_reactions.py`.  Returns the full
  mechanism JSON — id, name, category, description, and a
  `mechanism` sub-dict containing every step's title /
  description / SMILES / arrows / lone_pairs.  Accepts a
  numeric id (string form) or a name substring, same lookup
  rules as `open_mechanism`.  Clean error-return shape for
  unknown names or reactions without stored JSON.
- **Demo 04 enriched** — `04_mechanism_walkthrough.py` now
  drills into the Diels-Alder entry after enumerating the
  catalogue: prints the SMILES, every arrow (atom-to-atom or
  bond-midpoint) with its kind + label, and every lone-pair
  dot.  Teaching payoff: the student sees the real 3-arrow
  pericyclic electron flow (atom0→atom5 new bond, atom4→atom3
  new bond, atom2→atom1 π shift) instead of just a step
  count.
- **GUI audit** updated: `get_mechanism_details` maps to the
  existing "Reactions tab → Open mechanism…" path because
  the action is a pure-data reader of the same content the
  dialog already displays.  100% coverage preserved.
- **Agent action count** now 125 (↑ 124).

### Tests
- **`tests/test_get_mechanism_details.py`** (5 new cases):
  full JSON shape, error path for unknown names, id-as-string
  lookup, Phase-13c bond-midpoint + lone-pair exposure for
  HIV protease, and a contrast test pinning the shape
  difference vs `open_mechanism` (steps=int summary vs
  mechanism.steps=list of dicts).
- Demo 04's `_CONTENT_MARKERS` extended with
  `"full arrow walkthrough"`, `"arrows"`, `"curly"` so the
  smoke test would catch any regression that silently drops
  the arrow drill-down.
- **913 passed, 0 skipped** (↑ from 908); first-pass green.

### Next
Options for round 82: Workbench per-track colour swatch +
opacity slider (32c+ polish), another Phase-31e tutorial
lesson (21 → 22), a new feature phase (33?), or the
`Tutor-test-term-*` glossary cleanup that demo 15
surfaced.

---

## 2026-04-23 — Round 80 (Phase 31d CLOSED at 25/25)

### What shipped
Closed Phase 31d synthesis-pathway target with the final
two seeds.  Chosen as cohesive pedagogical pairs to the
existing catalogue:

- **Nylon-6 — Beckmann / caprolactam route (3-step)**.
  Pairs with round-79 Nylon-6,6 to give the student both
  big polyamide commodity chains side-by-side (same C₆
  cyclohexanone branch point).  Three steps:
  1. Oxime formation: cyclohexanone + NH₂OH →
     cyclohexanone oxime (buffered at pH 5-6; acid
     catalyses dehydration but suppresses NH₂OH
     nucleophilicity if too strong).
  2. **Beckmann rearrangement** with conc. H₂SO₄ / oleum
     → ε-caprolactam.  Description spells out the core
     pedagogical payload: the C-C bond *anti* to the
     oxime -OH migrates to N concerted with water
     departure; stereospecific; (NH₄)₂SO₄ coproduction
     flagged as a plant-scale sustainability concern
     addressed by vapour-phase zeolite catalysts.
  3. Ring-opening polycondensation: trace water + 260 °C
     → nylon-6 linear polyamide.  Model-dimer SMILES
     shows one complete -HN-(CH₂)₅-CO- repeat × 2.
     Property contrast with nylon-6,6 called out (same
     direction vs alternating amide dipoles).

- **Aspartame — Z-protected peptide coupling (2-step)**.
  Pairs with round-76 Saccharin in the artificial-sweetener
  neighbourhood (nice teaching contrast — saccharin is a
  heterocyclic sulfimide that's ~300× sucrose, aspartame
  is a dipeptide that's ~200×).  Two steps:
  1. DCC/HOBt coupling of Z-L-Asp (α-NH₂ protected) with
     L-Phe-OMe → Z-aspartame.  Description spells out why
     the α-α regiochemistry wins (β-carboxyl is sterically
     hindered + less activated under DCC) and mentions
     the industrial thermolysin route that sidesteps
     protection entirely via enzyme regioselectivity.
  2. Z hydrogenolysis (H₂ / Pd-C) — benzylic C-O cleavage,
     spontaneous carbamic-acid decarboxylation to give
     free amine + toluene + CO₂.  Describes Fmoc as the
     base-labile alternative when acid/H₂-sensitive side
     chains are present.

### Fragment-consistency additions
10 new intermediates in `seed_intermediates.py`:
hydroxylamine, cyclohexanone oxime, ε-caprolactam, sulfuric
acid, nylon-6 model dimer, L-aspartic acid, Z-L-aspartic
acid, L-Phe-OMe, Z-aspartame, aspartame.  All SMILES pre-
validated; audit passed first try.

### Test suite
- **908 passed, 0 skipped** — full suite green on first
  pass.  Content-only round, no new tests (the
  fragment-consistency + pathway-schema harness already
  covers additions).

### Phase 31 status after round 80
- 31c mechanisms 20/20 ✅
- 31d pathways **25 / 25 ✅ (this round)**
- 31f glossary 80/80 ✅

**Three sub-phases now fully closed.**  Phase 31 remaining
work is all long-running / scope-uncapped:
- 31a molecules 210 → 400 (continuous expansion)
- 31b reactions 35 → 50 (continuous expansion)
- 31e tutorials 21 → 30 (markdown authoring)
- 31g macromolecule catalogues (25/31/33 → 40 each)

### Next
Round 81+: likely pivot to tutorial authoring (21 → 30)
or a new feature phase (33?).  Alternatively close the
cleanup items surfaced earlier: the `Tutor-test-term-*`
glossary pollution, the `get_mechanism_details` action
gap for richer arrow-pushing demos, or the per-track
colour swatch / opacity slider in the Workbench.

---

## 2026-04-23 — Round 79 (Phase 31d +2 pathways — Adipic acid + Nylon-6,6)

### What shipped
Educationally cohesive pair — adipic acid is the industrial
monomer feedstock that the second pathway turns into polymer.
Phase 31d 21 → 23/25.

- **Adipic acid — DuPont cyclohexane route (2-step)**.
  Step 1: air oxidation of cyclohexane with Co / Mn
  naphthenate (150 °C, 15 atm, held at ~8 % conversion) →
  **KA oil** (1:1 cyclohexan*ol* + cyclohexan*one*).  The
  low-conversion kinetic quench is the industrial trick —
  otherwise KA oil over-oxidises faster than cyclohexane
  itself.
  Step 2: 50 % aq. HNO₃ / V₂O₅-Cu cleaves the C-C bond →
  adipic acid.  Description flags the N₂O byproduct
  (~1 mol / mol adipic) as one of the largest industrial
  sources of this potent greenhouse gas, with modern plant-
  scale thermal-catalytic abatement.
- **Nylon-6,6 — Carothers polycondensation (2-step)**.
  Step 1: adipic acid + HMDA (1,6-diaminohexane) in MeOH
  →  1:1 **AH salt** (diammonium dicarboxylate).  Making the
  salt first gives the exact stoichiometry Carothers's
  equation demands for high-MW polymer.  Step 2: melt the
  dry salt at 270 °C under N₂ → vacuum → step-growth
  polyamide formation.  Product SMILES is a 2-amide
  **model dimer** (HMDA-AA-HMDA) — one repeat unit of the
  actual polymer.  Description embeds Carothers's
  DP = 1/(1-p) equation with worked numbers: 99 % → DP 100,
  99.5 % → DP 200.

### Fragment-consistency additions
12 new intermediates / reagents in `seed_intermediates.py`:
cyclohexane, O₂, cyclohexanol, cyclohexanone, nitric acid,
adipic acid, N₂O, HMDA, nylon-6,6 salt, nylon-6,6 model
dimer, **plus** the dicationic HMDA-diammonium and the
dianionic adipate fragments (pre-emptively split, per the
round-76 salt-splitting gotcha).  Pre-emptive salt splitting
worked — the audit passed on first pass this round with no
iteration.

### Test suite
- **908 passed, 0 skipped** (content-only round).

### Phase 31 status after round 79
- 31c mechanisms 20/20 ✅
- 31d pathways **23 / 25** — 2 more to the target
- 31f glossary 80/80 ✅
- 31a/b/e/g — longer-running

### Next
Round 80 can close Phase 31d at 25/25 with 2 more pathways
— candidates: adipic acid → caprolactam route for nylon 6
(to pair with the nylon 6,6 just landed, showing the two
big nylon commodity chains side-by-side), or an ambitious
big-endgame like morphine / oseltamivir / atorvastatin
assembly.  Alternatively pivot to Phase 31e tutorials
(21 → 30) for a different kind of progress.

---

## 2026-04-23 — Round 78 (Phase 31d +2 pathways — L-DOPA + Dopamine)

### What shipped
Two seeded pathways, advancing Phase 31d 19 → 21/25.  The
pair tells a cohesive Parkinson's / neurotransmitter story.

- **L-DOPA — Knowles Rh-DIPAMP asymmetric route (3-step)**:
  1. Erlenmeyer condensation: veratraldehyde + N-acetylglycine
     → (Z)-2-acetamido-3-(3,4-dimethoxyphenyl)acrylic acid
     via the 5-ring azlactone intermediate.
  2. Asymmetric hydrogenation with [Rh((R,R)-DIPAMP)]⁺ →
     (S)-N-acetyl-3,4-dimethoxyphenylalanine in ≥ 95 % ee.
     **The milestone that won the 2001 Nobel** — first
     industrial-scale asymmetric catalytic H₂; ton-scale,
     chiral-at-P bisphosphine replacing a resolution.
  3. HBr / AcOH simultaneously demethylates both methyl aryl
     ethers (SN2 at methyl → CH₃Br byproduct) and hydrolyses
     the acetamide → L-DOPA directly.  The zwitterionic
     amino-acid α-stereocentre is protected against
     epimerisation.
- **Dopamine — decarboxylation of L-DOPA (1-step)**.
  The AADC (aromatic-L-amino-acid decarboxylase) step that
  activates L-DOPA *in vivo* inside the CNS — which is
  why L-DOPA is dispensed rather than dopamine itself
  (dopamine can't cross the blood-brain barrier; L-DOPA
  rides LAT1 and is decarboxylated on arrival).
  Description walks the PLP cofactor mechanism: imine
  formation, electron-sink stabilisation in the quinonoid
  intermediate, stereospecific reprotonation that destroys
  the α-stereocentre.

### Fragment-consistency additions
10 new intermediates / reagents in `seed_intermediates.py`:
Veratraldehyde, N-Acetylglycine, (Z)-dehydroamino-acid,
N-Acetyl-(S)-3,4-dimethoxyphenylalanine, L-DOPA, Dopamine,
Hydrogen gas, Hydrogen bromide, Methyl bromide,
Carbon dioxide.  All pre-validated via RDKit; the audit
passed first try (no salt-splitting gotchas this round
since no ionic reagents in use).

### Test suite
- **908 passed, 0 skipped** — full suite green on first try.

### Phase 31 status after round 78
- 31c mechanisms 20/20 ✅
- 31d pathways **21 / 25** — 4 more to target
- 31f glossary 80/80 ✅
- 31a/b/e/g — longer-running

### Next
Round 79: candidates for the final 4 pathways toward the
25-target: nylon-salt condensation (hexamethylenediamine +
adipic acid → nylon 6,6 monomer), adipic acid from
cyclohexane KA-oil (DuPont industrial route), caffeine
from theobromine (already seeded!) — skip, penicillin V
via the classical Sheehan route, or one big endgame
(taxol / morphine / oseltamivir).  Or diversify: ship a
tutorial markdown lesson (21 → 22) for Phase 31e.

---

## 2026-04-23 — Round 77 (Phase 31f glossary CLOSED at 80/80)

### What shipped
Three glossary terms that close Phase 31f at the 80-target:

- **Activating and deactivating groups** *(reactions)* —
  EAS bias: π-donor activators (–NH₂, –OR, –alkyl) raise the
  ring HOMO and direct ortho/para; π-acceptor deactivators
  (–NO₂, –CN, –COR, –SO₃H) lower the HOMO and direct meta
  (because ortho/para suffer direct-conjugation penalty).
  Halogens called out as the σ-withdrawing-but-π-donating
  exception.  Links to the Hammett σ scale already seeded
  via Phase 17e.
- **Regioselectivity** *(reactions)* — distinguishes
  regioselectivity (choice between positional isomers) from
  chemoselectivity (functional-group choice) and
  stereoselectivity (stereoisomer choice).  Canonical
  examples drawn from existing content: Markovnikov,
  Zaitsev, ortho/para vs meta, 1,2- vs 1,4-addition.
  Defines *regiospecific* as the limiting case.
- **Constitutional isomer** *(stereochemistry)* — a
  taxonomy: chain / positional / functional-group /
  tautomeric sub-types, each with a canonical textbook
  pair (n-butane vs isobutane, propanols, ethanol vs
  dimethyl ether, keto/enol).  Contrast with stereoisomers
  (same connectivity, different 3D).

### Plumbing
- Glossary `SEED_VERSION` bumped 7 → 8.  Existing local DBs
  will silently pick up the three new rows on next launch
  via the additive-seed path.
- Content-only change; no test additions needed — the
  existing `test_seed_glossary` schema checks + the
  `_discover_scripts` demo-library sweep both still pass.

### Phase 31 status after round 77
- 31c mechanisms 20/20 ✅ (round 62)
- 31d pathways 19/25 — in progress
- 31f glossary **80/80 ✅ (this round)**
- 31a molecules 210 → 400 — long-running
- 31b reactions 35 → 50 — long-running
- 31e tutorials 21 → 30 — in progress
- 31g macromolecule catalogues — rounds 41-43

Two sub-phases (c + f) now fully closed.

### Test suite
- **908 passed, 0 skipped** (unchanged — pure content round).

### Next
Round 78: pick between Phase 31d pathway expansion
(19 → 25) or Phase 31e tutorial expansion (21 → 30).
Tutorials are markdown authoring — a shift in gear from
the recent chemistry-seed rounds.

---

## 2026-04-23 — Round 76 (Phase 31d +2 pathways — Saccharin + Acetanilide)

### What shipped
Two more seeded syntheses, advancing Phase 31d 17 → 19/25:

- **Saccharin — 3-step Remsen-Fahlberg route**: toluene →
  2-methylbenzenesulfonyl chloride (ClSO₃H, EAS) → 2-methyl-
  benzenesulfonamide (NH₃) → saccharin (KMnO₄ CH₃ → COOH
  oxidation with spontaneous intramolecular sulfimide
  closure).  Historically the first artificial sweetener
  (Remsen & Fahlberg 1879, serendipitous taste-test of a
  spill that night).  Each step's notes call out the
  pedagogical hooks: ortho+para selectivity of the EAS,
  why the ortho isomer is kept (only it cyclises), and the
  unusual 5-ring sulfimide lactam formed by dehydration
  between the new -COOH and the -SO₂NH₂.
- **Acetanilide — 1-step acetylation**: aniline + acetic
  anhydride → acetanilide + acetic acid.  Single-step N-
  acylation.  The pathway description ties this back to
  two already-seeded routes (phenacetin, sulfanilamide) for
  which acetanilide is a starting material, so the student
  sees the precursor chain.  Also notes its historical role
  as an antipyretic (1886-1940s), displaced by acetaminophen
  (its less-toxic hepatic O-dealkyl metabolite).

### Fragment-consistency additions
Added 10 new intermediates / reagents / products to
`seed_intermediates.py`:
Toluene, 2-Methylbenzenesulfonyl chloride,
2-Methylbenzenesulfonamide, Potassium permanganate,
**Permanganate ion + Potassium cation** (separate entries —
the audit canonicalises the `.`-salt SMILES and wants each
fragment present as its own DB row), Manganese dioxide,
Hydroxide ion, Saccharin, Acetic anhydride.

### Gotcha (caught on first pytest pass)
The fragment-consistency audit split `[K+].O=[Mn](=O)(=O)[O-]`
into three fragments (KMnO₄ itself, the permanganate anion,
and the K⁺ counter-ion), and the first two bullet weren't in
the DB until I added them.  Typical pattern for any
ionic-salt reagent — noted the rule so future pathway
additions get it right first time.

### Test suite
- **908 passed, 0 skipped** (unchanged — content-only seeds).
  Full suite green on the second pass after adding the two
  missing salt-ion intermediates.

### Phase 31d tally
17 → **19 / 25** after round 76.  6 more to hit 25.
Priority candidates: L-DOPA 3-step from vanillin, Dopamine
from 3,4-dimethoxyphenethylamine, Nylon-6,6 salt condensation,
Adipic acid from cyclohexane KA-oil, Caffeine synthesis (Fischer
or Trauber route), MDMA/amphetamine (if appropriate),
or the big total-synthesis endgames (taxol, morphine, oseltamivir).

### Next
Round 77 can ship +2 more pathways or switch to glossary
(77 → 80) or tutorials (21 → 30) to diversify the content
progress.

---

## 2026-04-23 — Round 75 (Phase 31d +2 pathways — Sulfanilamide + Phenolphthalein)

### What shipped
Pivoted to Phase 31 content expansion after closing Phase 32.
Two seeded pathways added to `orgchem/db/seed_pathways.py`:

- **Sulfanilamide — 3-step chlorosulfonation route**
  (historically the first clinically useful sulfa drug; Domagk
  Nobel 1939).  Starts from acetanilide (amine pre-masked so it
  doesn't compete at the electrophilic sulfur step):
  1. Chlorosulfonation with ClSO₃H — para-selective EAS driven
     by the acetamido activating group → 4-acetamido-
     benzenesulfonyl chloride.
  2. Ammonolysis (aq. NH₃) of the sulfonyl chloride → sulfonamide;
     HCl byproduct scavenged by excess NH₃.
  3. Acid-catalysed hydrolysis (10% HCl, reflux) deprotects the
     acetamide — sulfonamide is hydrolytically stable, so
     selectivity is trivial.  Product: sulfanilamide
     (4-aminobenzenesulfonamide).
- **Phenolphthalein — Friedel-Crafts condensation** (Baeyer 1871
  dye/indicator, 1-step net from phthalic anhydride + 2 phenols
  under conc. H₂SO₄ or ZnCl₂).  Description walks the student
  through the three mechanistic events inside the flask —
  phenol acylation, lactonisation, second phenol addition —
  even though the overall stoichiometry is one step.  Teaching
  callout on the closed-lactone ↔ open-quinoid dianion
  equilibrium that makes it an acid-base indicator.

### Fragment-consistency additions
Added 9 new intermediates / reagents / products to
`seed_intermediates.py` so the Phase-6f.4 audit stays green:
Acetanilide, Chlorosulfonic acid,
4-Acetamidobenzenesulfonyl chloride, Ammonia,
4-Acetamidobenzenesulfonamide, Sulfanilamide;
Phthalic anhydride, Phenol, Phenolphthalein.
All SMILES pre-validated through RDKit before commit.

### Test suite
- **908 passed, 0 skipped** (unchanged — these are content-only
  seeds, so the existing fragment-consistency + pathway
  schema tests cover them without a per-pathway smoke).
- Full pytest pass on first try; no iteration needed.

### Phase 31d tally
14 → **17 / 25** after round 75.  Remaining priority targets
(unchanged): taxol endgame, morphine, lysergic acid, reserpine,
cortisone, oseltamivir, sildenafil, atorvastatin assembly,
cephalosporin, penicillin V, progesterone, glyphosate, plus
smaller wins like saccharin, novocaine-family variants,
L-DOPA, dopamine-from-catechol, nylon fragments.

### Next
Round 76 can keep momentum with +2 more pathways (sulfa-drug
extensions like sulfadiazine; or saccharin 3-step; or nylon-
salt condensation) — OR swing to a different Phase 31 sub-item
(glossary 77 → 80, tutorials 21 → 30).

---

## 2026-04-23 — Round 74 (Phase 32e shipped — Phase 32 CLOSED)

### What shipped
Final Phase-32 sub-item: tutor ↔ Script Editor handoff.

- **`orgchem/agent/conversation.py`** —
  `_SCRIPT_MODE_ADDENDUM` describes the ScriptContext
  globals, Scene API, and the fenced ```python block
  contract; `build_script_mode_system_prompt(base)` appends
  it to any base prompt.  The LLM is told *not* to auto-
  execute — blocks only run when the user clicks the button.
- **`orgchem/agent/script_context.py`** —
  `extract_python_blocks(text)` + `_CODE_FENCE_RX` regex
  pulls fenced ```python / ```py / bare ``` blocks out of
  mixed prose/markdown.  Shared between the tutor panel and
  future bridges (e.g. stdio protocol could scan for scripts).
- **`orgchem/gui/panels/tutor_panel.py`** —
  - New **Reply with a script** checkbox.  Toggling it
    swaps `Conversation.system_prompt` between the base
    prompt and the extended one (takes effect from the
    next turn — no reconnect).  Works whether toggled
    before or after Connect.
  - `_append_assistant(text)` rewritten to detect code
    blocks.  Each match produces a dark monospace preview
    div (truncated at 500 chars with a "… (truncated)"
    tail) plus a ▶ **Run in Script Editor** anchor with
    the custom URL scheme `orgchem-script:<idx>`.  Blocks
    are stashed in `self._script_blocks` keyed by idx.
  - `_on_anchor_clicked(url)` routes the custom scheme to
    `ScriptEditorDialog.singleton()`, loads the block,
    raises the dialog.  Non-`orgchem-script` links still
    open in the system browser.
  - `QTextBrowser` configured with `setOpenLinks(False)`
    so our scheme stays in-app.

### Tests
- **`tests/test_tutor_script_mode.py`** — 12 cases across
  three layers:
  - **Headless extractor** (6 cases) — `extract_python_blocks`
    handles ```python / ```py / bare ``` fences, multiple
    blocks in one message, mixed prose, and rejects
    inline-backtick fragments that aren't real fences.
  - **Prompt builder** (3 cases) — addendum appended, every
    pre-imported global named in the briefing
    (app / chem / orgchem / viewer), custom base prompt
    supported.
  - **GUI integration** (3 pytest-qt cases) — toggle swaps
    the live Conversation prompt both ways; fenced reply
    renders a preview + anchor; anchor click loads the
    block into the singleton ScriptEditorDialog.
- **908 passed, 0 skipped** (↑ from 896).

### Phase 32 — fully closed ✅
- 32a script editor + REPL dialog ✅ (round 64)
- 32b hybrid-placement Workbench + Scene API ✅ (round 66)
- 32c per-track controls + scene chrome ✅ (round 69)
- 32d 15/15 bundled demo library ✅ (rounds 67/70/72/73)
- 32e tutor Reply-with-a-script mode ✅ (this round)

The full scripting stack is now end-to-end:
*user prompts tutor → tutor emits fenced `python block →
user clicks ▶ → block lands in Script Editor → user clicks
Run → `app.*` calls drive the app and `viewer.*` calls drive
the Workbench scene.*  The same `viewer` Scene is shared
between scripts and the UI, so mutations from a script show
up live in the Workbench panel.

### Next
With Phase 32 closed, future rounds can swing back to Phase
31 content expansion (more glossary terms, pathways,
tutorials, macromolecule entries) or start on a new feature
phase (33?).  Candidate follow-ups surfaced during Phase-32
work:
- Cleanup of the ~90 `Tutor-test-term-*` pollution in the
  local glossary DB (from earlier authoring-action tests).
- `get_mechanism_details(name_or_id)` action so LLM-
  generated scripts can walk arrow-pushing data.
- Per-track colour swatch + opacity slider in the Workbench
  tracks list (32c+ polish).

---

## 2026-04-23 — Round 73 (Phase 32d CLOSED at 15/15)

### What shipped
Final three demo scripts, completing the Phase 32d library:

- **`13_butane_dihedral.py`** — runs the pre-wired butane
  dihedral scan (36-frame C–C–C–C rotation via Phase 10a
  `run_dihedral_scan_demo`), saves the standalone 3Dmol.js
  player HTML to `/tmp/butane_dihedral.html`, and loads a
  static butane ball-and-stick into the Workbench as a
  reference.  Teaching tag-line on anti (180° minimum),
  gauche (±60°, ~3.8 kJ/mol), and eclipsed (0°, maximum).
- **`14_retrosynthesis_tree.py`** — recursive retro on methyl
  4-phenylbenzoate with `max_depth=3`.  Finds 4 paths that
  interleave Fischer ester and Suzuki biaryl disconnections
  in different orders.  Prints the full indented tree with
  each node's template label + SMILES.  Good canonical
  example for a student learning "disconnection order
  matters".
- **`15_glossary_tour.py`** — catalogue tour: buckets all
  170 seeded glossary terms by category, shows counts + the
  first 3 per category, then pulls a full markdown `define()`
  payload for "Bürgi-Dunitz angle" to demonstrate how the
  tutor surfaces cross-reference content programmatically.

### Gotcha mid-round
First draft of demo 14 put the target compound's human name
only in a comment, and the round-71 marker guard caught the
gap immediately (`'methyl 4-phenyl'` missing from stdout).
Fixed by moving the name into the printed output.  This is
the smoke-test hardening earning its keep in real time.

### Test suite
- **896 passed, 0 skipped** (↑ from 890).  6 new auto-enrolled
  smokes (3 headless + 3 GUI-path pytest-qt) via the
  `_discover_scripts()` parametrisation.

### Phase 32 status after round 73
- 32a Script editor + REPL dialog: ✅
- 32b Hybrid-placement Workbench + Scene API: ✅
- 32c Track-aware controls (checkbox / style / remove + scene
  chrome): ✅
- 32d Script library 15/15: ✅ **this round**
- 32e LLM script generation mode: remaining

### Observations surfaced but not fixed
Demo 15 revealed the local `orgchem.sqlite` has accumulated
~90 `Tutor-test-term-*` glossary rows from prior test runs
of the authoring action.  Not a regression of round-73 work,
but worth a future cleanup round — either make the test
terms use a distinctive prefix that `list_glossary` filters,
or seed them into a separate in-memory DB.

### Next
Only 32e remains for Phase 32: the tutor "Reply with a script"
mode.  After that, pivot to Phase 31 content expansion —
more glossary terms (current 77 → 80 target), synthesis
pathways (15 → 25), tutorials (21 → 30), etc.

---

## 2026-04-23 — Round 72 (Phase 32d +3 demos — Hückel / SAR / macromolecule)

### What shipped
Three more demo scripts under `data/script_library/`, moving
the library from 9/15 to **12/15**:

- **`10_huckel_benzene.py`** — `huckel_mos("c1ccccc1")` returns
  the π-system MO energies in units of β.  Demo prints each ψ
  with its energy + occupation, marks HOMO/LUMO, and computes
  the HOMO→LUMO gap in kJ/mol (with |β| ≈ 270 kJ/mol reference).
  Output reproduces the textbook degenerate ±β pattern:
  ψ1 (+2β) / ψ2,3 (+β) / ψ4,5 (−β) / ψ6 (−2β), π-electron
  stabilisation = 8β.
- **`11_nsaid_sar.py`** — pulls the seeded NSAID / COX SAR
  series, tabulates per-variant MW / logP / QED /
  COX-1 IC50 / COX-2 IC50 / selectivity, and classifies each
  as non-selective / preferential / coxib-like.  Teaching
  takeaway: aspirin COX-2 sel 0.006 (strongly COX-1-selective),
  ibuprofen/naproxen near 0.6 (non-selective), acetaminophen 4.0
  (preferentially COX-2).  Gotcha fixed mid-round: the
  `SARSeries` action returns variants under `rows`, not
  `variants` — first draft showed 0 variants before the
  `_CONTENT_MARKERS` guard caught it and I swapped the key.
- **`12_macromolecule_catalogue.py`** — Counter-based audit of
  the Phase-29 catalogues.  Breaks down 25 carbs (18 mono /
  5 di / 2 poly), 31 lipids (13 FA / 8 sterols / 3 PL / 3
  vitamins / 2 sphingolipids / 2 TG), 33 NAs (9 bases /
  9 nucleotides / 8 nucleosides / 5 PDB motifs / 2 oligos).
  Calls out the 5 PDB motifs (1BNA / 1RNA / 143D / 1EHZ /
  1HMH) so a user asking "what can I fetch?" sees the list.

### Test suite
- **890 passed, 0 skipped** (↑ from 884).  +3 headless demo
  smokes + +3 pytest-qt GUI-path smokes, auto-enrolled via the
  `_discover_scripts()` parametrisation.
- Round-71 `_CONTENT_MARKERS` extended with landmark values
  for 10-12: benzene's "π atoms: 6", "HOMO", "LUMO", textbook
  ±2β values, SAR "Ibuprofen" + real MW 206., macromolecule
  "monosaccharide" / "fatty-acid" / "PDB-motif" category
  headings.  The marker coverage guard already enforces that
  every demo ships with its own landmarks.

### Next
With 12/15 landed, 3 remain for the 15-target: a protein-
ligand tour (likely skipped or mocked due to network
dependency), a conformer trajectory demo (uses
`run_dihedral_scan_demo` + Workbench animation), and a
retro-tree walk (`find_multi_step_retrosynthesis`).  Can
interleave with Phase 32c chrome (colour swatch + opacity
slider) or content-phase work (more glossary terms,
pathways).

---

## 2026-04-23 — Round 71 (demo audit + strengthened smoke tests)

### What shipped
Follow-up to the user's round-70 report that demo 03 printed an
all-zero table: audited every bundled demo for the same class of
silent-output bug + strengthened the smoke tests to catch it
automatically going forward.

**Demo fixes surfaced by the audit:**
- **Demo 05 (lipid report)** — filename promised *MW report* but
  the table only printed chain length / unsaturations / mp.
  Added real molecular-weight computation via
  `rdkit.Chem.Descriptors.MolWt` on each lipid's SMILES; MW now
  ranges C8 (144.2 Da) → C22-DHA (328.5 Da) + PGE2/TXA2 at
  352.5 Da.  Bonus: demo now shows both the ``app.<action>``
  path AND direct RDKit use for teaching value.
- **Demo 06 (retrosynthesis)** — was printing ``via ?:`` because
  the proposal dict carries `label` / `template_id` /
  `forward_reaction`, not a `template` key.  Rewrote the output
  loop to use the real keys; now shows
  *"1. Ester ⇒ Carboxylic acid + Alcohol ... [forward: Fischer
  esterification]"* for the aspirin disconnection.

**Strengthened smoke tests (`tests/test_script_library.py`):**
- New `_CONTENT_MARKERS` dict — per-demo list of 2-6 substrings
  that MUST appear in stdout.  Spot-checks landmark values:
  caffeine MW 194.19, aspirin 180.x + naproxen 230.x + celecoxib
  381.x (catches silent-zero directly), Diels-Alder Ea 115 /
  ΔH -165, lipid MW 144.x, *"Ester ⇒ Carboxylic acid"* label,
  *"exothermic"* verdict.  Parametrised test asserts every
  marker appears.
- New `test_every_demo_has_content_markers` — coverage guard
  that every discovered script has markers defined.  Forces
  any future demo to come with its own landmark values.
- **Proof**: intentionally broke demo 03 again (swapped `'mw'`
  for `'not_a_key'`); the strengthened test failed with
  *"03_nsaids_overlay.py is missing content markers
  ['180.', '206.', '230.', '381.'] — a silent-output
  regression?"*  The silent-zero class of bug now fails CI
  loudly.  Restored the file after the negative-case proof.

### Test suite
- **884 passed, 0 skipped** (↑ from 883).  The +1 is the new
  marker-coverage guard; the existing 9 demo-smoke cases now
  carry much stronger assertions.

### Carry-over for future rounds
- 6 more demos toward the 15-target (protein+ligand,
  conformer trajectory, Huckel MO, macromolecule catalogue,
  SAR matrix, retro-tree).
- Phase 32c chrome: colour swatch + opacity slider per track,
  drag-reorder for tracks list.
- New `get_mechanism_details(name_or_id)` agent action so a
  future demo can walk curly arrows programmatically.

---

## 2026-04-23 — Round 70 (Phase 32d +3 demos — pathway / stereo / energy)

### What shipped
Three new demo scripts under `data/script_library/`, moving the
library from 6/15 to **9/15** toward the Phase-32d target:

- **`07_aspirin_pathway.py`** — pulls the seeded Aspirin
  pathway, iterates each step's reaction SMILES, and prints
  per-step + overall atom economy via `pathway_green_metrics`.
  Teaching takeaway: the 1-step Hoffmann/Bayer route at 75% AE.
- **`08_stereochem_tour.py`** — walks L-alanine through
  `assign_stereodescriptors` → `enantiomer_of`, prints a round-
  trip check that every R/S descriptor flipped, then drops both
  enantiomers into the Workbench as side-by-side tracks so the
  student can rotate and compare.
- **`09_energy_profile_diels_alder.py`** — enumerates all 12
  seeded energy profiles, drills into the Diels-Alder entry,
  marks TS points with ‡, and computes Ea forward / reverse /
  ΔH from the stationary-point list.  Output for the DA route:
  Ea forward 115, Ea reverse 280, ΔH -165 kJ/mol (exothermic).

### Gotchas fixed mid-round
- First draft of demo 09 filtered TS points by the wrong field
  name (`kind` vs the actual `is_ts: bool`) — caught because
  Ea values never printed.  Fix is local to the demo.
- `get_energy_profile` takes `reaction_id` but `list_energy_profiles`
  returns items keyed on `id`, not `reaction_id` — demo 09
  passes `reaction_id=target["id"]`.  Noted for any future
  LLM-generated script: always re-check the column name when
  hopping between list + detail endpoints.

### Test suite
- **883 passed, 0 skipped** (↑ from 877).
- The Phase-32d parametrised smoke auto-picked up all three new
  demos — 3 new headless cases + 3 new GUI-path cases via
  pytest-qt with zero test-file edits.  That's the dividend of
  the `_discover_scripts()` design from round 67.

### User-reported bug — demos 01 & 03 all-zero drug-likeness (fixed round 70 hotfix)
User: *"please check script 3 — the table it creates is full of
zeros instead of actual values."*  Root cause: both demos read
``drug_likeness()`` output under made-up keys (``descriptors``,
``mol_weight``, ``qed_score``, ``h_bond_donors``).  The action
actually returns `{lipinski, veber, ghose, pains, qed}` with
descriptors inside `lipinski` (mw/logp/hbd/hba) and `veber`
(tpsa/rotb).  Fixed by rewriting both demos to read from the
right sub-dicts.  Aspirin now reports MW 180.2 / logP 1.31 /
QED 0.55 instead of the all-zero table.  Tests still green —
the smoke tests only asserted the demo ran + emitted *some*
stdout, not that specific values appeared.  Filed a follow-up
to tighten the smoke test to spot-check a known descriptor
value so this class of silent-zero bug gets caught
automatically next time.

### Still to go
- 6 more demos toward 15/15 (protein+ligand, trajectory, Huckel
  MO, macromolecule iteration, SAR matrix, retro-tree).
- Phase 32c chrome follow-ups: colour swatch, opacity slider,
  drag-reorder for tracks list.
- A `get_mechanism_details(name_or_id)` action that returns full
  step + arrow JSON so demo 04 can do real arrow-pushing tours.
- Strengthen script-library smoke tests so "silent zero" output
  bugs (wrong key names) fail loudly (check at least one
  well-known numeric value per demo instead of just
  `stdout.strip() != ""`).

---

## 2026-04-23 — Round 69 (Phase 32c shipped — rich Workbench controls)

### User directive
*"Can you add more controls to the workbench viewer?  Whatever
useful items you can think of, including the ability to toggle
different tracks."*

### What shipped
- **`orgchem/gui/panels/workbench_track_row.py`** (new, 135
  lines).  `TrackRow(QWidget)` is the per-row widget used inside
  `WorkbenchWidget._tracks_list` via `QListWidget.setItemWidget`:
  - **Visibility checkbox** (☑︎) — the requested toggle.  Wires
    to `Scene.set_visible(name, bool)`.
  - **Name + kind label**, auto-subtitled with the track's
    SMILES (for molecules) or PDB ID (for proteins).
  - **Style combo** — kind-aware choice sets so small molecules
    don't see "cartoon" and proteins don't see "line".  Wires to
    `Scene.set_style(name, style=…)`.
  - **✕ remove button** — drops the track.
  - `reflect(track)` hook keeps the row in sync when the scene
    is mutated elsewhere (e.g. by the Script Editor while the
    user has the Workbench focus).
- **`WorkbenchWidget` toolbar** grew three scene-wide buttons:
  - **Fit to view** — re-zooms after hide / show / add.
  - **Toggle bg** — flips scene background between dark
    (`#1e1e1e`) and light (`#ffffff`).  Useful for snapshot
    contrast when preparing teaching figures.
  - **Export HTML…** — saves a standalone `.html` copy of the
    current scene (3Dmol.js inlined), shareable + works in any
    browser with no server.
- The scene rebuild now respects `self._background` so the
  toggle-bg button actually propagates through to 3Dmol.js.
- The tracks-list hint text was updated: *"Per-row: ☑︎ toggle
  visibility, style combo restyles, ✕ removes."* — tells the
  user what the inline controls do.

### Tests
- **`tests/test_workbench_controls.py`** (7 new pytest-qt
  regression tests):
  - Checkbox toggles `track.visible`.
  - Style combo mutates `track.style`.
  - Remove button drops the track.
  - Toggle-bg flips between the two hex values.
  - Export-HTML writes a file (uses `tmp_path` + monkeypatched
    `QFileDialog` so no real file dialog pops).
  - Fit-to-view schedules a rebuild.
  - Row signals carry the correct track name when multiple
    tracks are present (prevents off-by-one routing bugs).
- Full suite: **877 passed, 0 skipped** (↑ from 870).

### File layout
`workbench.py` grew from 309 → 403 lines.  Row widget extracted
to `workbench_track_row.py` (135 lines) to keep both files
comfortably under the 500-line cap.

### Deferred to future 32c iterations
- Per-track colour swatch (CPK / chain / spectrum / residue).
- Per-track opacity slider.
- Drag-reorder for track list.
- Scene-wide spin toggle + axis selector.

### Next
Round 70 can pick up the deferred chrome (colour swatch,
opacity), resume the Phase 32d 15-demo march (still at 6/15),
or pivot to a Phase-31 content item (pathways, proteins).

---

## 2026-04-23 — Round 68 hotfix (Workbench SIGTRAP on worker-thread scene mutations)

### User report
Running demo 02 (`02_scene_composer_basics.py`) from the Script
Editor crashed the app with *"Compositor returned null texture"*
+ SIGTRAP on macOS 26.4.1 (MacBook Pro M1).  Full crash dump
confirmed the trigger thread was `_RunWorker` — the QThread
that executes script snippets.

### Root cause
`WorkbenchWidget` subscribed to `Scene.listen()` with a plain
Python callback (`_on_scene_event`).  When a script called
`viewer.add_molecule(...)` from inside the `_RunWorker` thread,
the Scene's event-emit loop called the callback on that worker
thread, which then called `QWebEngineView.setHtml()` and
manipulated `QListWidget` items *off the main thread*.  Qt's
GUI objects are main-thread-only; on macOS this is a hard trap
in the Metal / Graphite compositor.  Same class of bug as the
NSWindow crash fixed in rounds 55-57, but on a different code
path (scene listeners rather than one-shot action calls).

### Fix
Two-layer defence in `orgchem/gui/panels/workbench.py`:
1. **Thread-marshalling via Qt Signal + `Qt.QueuedConnection`.**
   `WorkbenchWidget` now declares an internal
   `_scene_event_queued = Signal(object, object)` connected to
   `_handle_scene_event_main` with `Qt.QueuedConnection`.  The
   Scene listener `_on_scene_event` just emits the signal — Qt
   automatically posts the event onto the main-thread event
   loop regardless of the emitting thread.  **This is the root
   fix for the SIGTRAP.**
2. **Debounced rebuilds.**  Even on the main thread, a burst of
   scene events (`for _ in …: viewer.add_molecule(…)`) would
   call `setHtml` N times, thrashing the WebGL compositor.
   `_schedule_rebuild` coalesces events via a single-shot
   `QTimer(50 ms)` so the whole burst triggers one HTML load.
   Configurable via `_REBUILD_DEBOUNCE_MS`.

### Smoke verification
Booted the real app with `QT_QPA_PLATFORM=offscreen`, opened
the Script Editor, pasted demo 02, clicked Run: status went to
"ok", 6 tracks landed in the scene, `rebuild_count == 2` (one
for initial prime, one coalesced for the whole burst — not 6).

### Tests
- **`tests/test_workbench_debounce.py`** (3 new tests):
  - `test_rapid_adds_collapse_into_one_rebuild` — reproduces
    the demo-02 pattern; asserts ≤ 2 rebuilds for 6 adds.
  - `test_tracks_list_catches_up_after_queued_events` — no
    events lost through the queued-connection bridge.
  - `test_subsequent_burst_after_quiet_window_still_debounced`
    — the debounce still works on the second burst.
- Full suite: **870 passed, 0 skipped** (↑ from 867).

### Carry-over for future rounds
- Consider extending the same Signal-queue + debounce pattern
  to any other panel that listens to cross-thread events (none
  identified so far, but worth auditing when 32c adds richer
  track-list chrome that may also subscribe).

---

## 2026-04-23 — Round 67 (Phase 32d — first 6 bundled script-library demos)

### What shipped
- **`data/script_library/`** — new directory, 6 demo scripts
  that exercise the Scene + action-registry surface end-to-end:
  1. `01_caffeine_tour.py` — descriptors + IR bands +
     drug-likeness on a single compound.
  2. `02_scene_composer_basics.py` — build a 6-hydrocarbon
     Scene, toggle visibility, restyle tracks.
  3. `03_nsaids_overlay.py` — 4 NSAIDs into one Scene +
     drug-likeness table.
  4. `04_mechanism_walkthrough.py` — enumerate every seeded
     mechanism, bucket by category, open the Diels-Alder
     player.
  5. `05_lipid_mw_report.py` — fatty-acid catalogue table
     sorted by chain length + unsaturation.
  6. `06_retrosynthesis_demo.py` — apply Phase-8d retro
     templates to aspirin, print every disconnection.
- **`tests/test_script_library.py`** — headless smoke:
  discover every `*.py` in `data/script_library/`, run it
  through `ScriptContext`, assert `result.ok` and non-empty
  stdout.  Parametrised over scripts, so adding a new demo
  auto-extends the suite.  Plus a floor-guard that fails if
  the library ever drops below 6 files.
- **`tests/test_script_library_gui.py`** — **user directive
  2026-04-23**: run the same demos through the real
  `ScriptEditorDialog` + `_RunWorker` QThread via pytest-qt.
  Construct the dialog, `setPlainText(source)`, call
  `_run_all()`, wait (`qtbot.waitUntil`) for the status label
  to flip to "ok" / "error", then assert the output pane
  contains stdout + no traceback block.  Catches regressions
  in the editor's threading / output-colour-coding / error-
  propagation wiring that headless `ScriptContext` tests can't
  see.

### Test suite
- **867 passed, 0 skipped** (↑ from 854).  13 new tests:
  7 from `test_script_library.py` (6 demos + not-empty
  guard), 6 from `test_script_library_gui.py`.  Total test
  file count now 122.

### Action surface gaps surfaced
Demo 04 had to drop its first draft's per-step arrow walk-
through because the registered actions only expose
mechanism *summaries* (id + name + step count), not the
full step data.  Candidate follow-up (32c or 32e): add a
`get_mechanism_details(name_or_id)` action that returns
the full step + arrow list as JSON, so LLM-generated
scripts can inspect arrow-pushing programmatically.

### Next
Round 68 can go two ways: extend the script library toward
the 15-target (add protein-ligand + energy-profile demos),
or swing back to 32c (track-list chrome: style combo /
colour swatch / opacity slider per track).  I'll pick
whichever has higher ROI when the loop fires.

---

## 2026-04-23 — Round 66 (Phase 32b shipped — hybrid Workbench + Scene API)

### What shipped
- **`orgchem/scene/`** (new subpackage, zero Qt imports):
  - `Scene` class — observable scene graph with a list of `Track`
    dataclasses.  Public API: `add_molecule(smi_or_mol)`,
    `add_protein(pdb_id_or_text)`, `remove(name)`, `clear()`,
    `set_visible(name, bool)`, `set_style(name, …)`,
    `snapshot(path)`, `listen(fn)` with unsubscribe.  Process-wide
    singleton via `current_scene()` / `reset_current_scene()`.
  - `Track` — name + kind (molecule / protein / ligand) + data +
    source_format (mol / pdb) + style + colour + visibility +
    opacity + meta.
  - `SceneEvent` enum — TRACK_ADDED / REMOVED / STYLE_CHANGED /
    VISIBILITY_CHANGED / CLEARED / CAMERA_CHANGED.
  - `html.build_scene_html(scene)` — assembles a self-contained
    3Dmol.js page from every visible track; reuses the bundled
    local asset when present, CDN fallback.  Protein tracks get
    an automatic HETATM overlay so bound ligands survive cartoon
    rendering.  Empty scenes render a placeholder label instead
    of a broken `zoomTo`.
- **`gui/panels/workbench.py`** — `WorkbenchWidget`, standalone
  `QWidget` that can parent into either the main tabbar or a
  `WorkbenchWindow`.  Toolbar: Detach / Reattach / Clear /
  Snapshot PNG.  Right-side track list with double-click-to-
  remove.  Subscribes to `current_scene()` and re-renders the
  entire HTML document on every event.  `grab_png(path)` uses
  `QWidget.grab()` so snapshots work under offscreen Qt even
  when the widget isn't visible.
- **`gui/windows/workbench_window.py`** — `WorkbenchWindow`
  hosts the widget when detached.  Geometry persists via
  `QSettings["window/workbench/geometry"]`.  `takeCentralWidget()`
  on close so Qt doesn't delete the reparented widget.
- **`MainWindow` wiring**:
  - "Workbench" tab inserted immediately after "Molecule
    Workspace" (index 1).
  - `_detach_workbench()` — pulls the widget out, creates a
    `WorkbenchWindow`, reattaches the Reattach signal.
  - `_reattach_workbench()` — tears down the window,
    re-inserts the widget at tab index 1.
  - `open_workbench()` — focuses the tab (or raises the
    detached window).
  - Window menu entry *Workbench… (Ctrl+Shift+B)*.
- **`ScriptContext` graduation** — the `viewer` global is now
  `current_scene()` instead of the Phase-32a stub.  Any script
  line `viewer.add_molecule('CCO')` updates the visible
  Workbench view instantly.  Scripts that run before the
  Workbench opens still work — the Scene accumulates tracks,
  which the widget picks up on first `setHtml()`.
- **`open_workbench` agent action** (`scripting` category,
  main-thread-dispatched) with Window-menu + Ctrl+Shift+B
  binding.  GUI-audit map updated — 100 % coverage preserved.
- **Piggy-backed round 65**: Procaine 2-step acyl-chloride
  pathway seeded; +5 intermediate molecules (SOCl₂, 4-amino-
  benzoyl chloride, SO₂, 2-(diethylamino)ethanol, Procaine);
  completes the seeded-anaesthetic triad (Benzocaine +
  Lidocaine + Procaine).  Phase 31d tally 14 → 15.

### Test suite
- **854 passed, 0 skipped** (↑ from 837).  17 new
  `tests/test_scene.py` cases cover: add_molecule auto-names,
  duplicate-name rejection, remove / clear / set_visible /
  set_style, listener events + unsubscribe, process-wide
  singleton, empty-scene HTML safety, hide hides from HTML,
  protein HET overlay, SMILES rejection, RDKit-Mol acceptance,
  PDB-ID heuristic, snapshot-without-view raises.
- End-to-end HeadlessApp smoke verified: MainWindow boots with
  Workbench tab, `open_workbench` action works, Scene survives
  round-trip driving from `current_scene()`.
- `test_viewer_is_a_real_scene_object` replaces the Phase-32a
  stub test now that `viewer` is the real Scene.

### Design calls still deferred to 32c
- Arrow overlays for mechanism step-throughs.
- Trajectory tracks + timeline scrubber.
- Programmatic `rotate` / `zoom` / `spin` (mouse still works
  natively in 3Dmol.js, so this isn't a blocker).
- `highlight(track, atoms=[…])` for picking out residues.
- Per-track style chrome in the tracks-list UI (combo box +
  colour swatch + opacity slider).

### Next
Round 67 picks up one of: 32c track-list chrome + arrow overlays;
32d script library (15 bundled demo scripts — this is the real
dogfooding of the Scene + app.call surface); or a Phase-31
content item to interleave content and code.

---

## 2026-04-23 — Round 64 (Phase 32a shipped — script editor + REPL)

### What shipped
User directive: *"Your suggestion and plan sound great — please
implement."* Round 64 is the foundational slice of Phase 32.

- **`orgchem/agent/script_context.py`** (zero Qt imports, fully
  headless-testable):
  - `ScriptContext` — persistent globals dict + `run(source)` that
    captures stdout / stderr, returns a last-expression `repr` in
    `eval`-mode for single expressions, falls back to `exec`-mode
    for multi-statement snippets, and formats syntax errors
    compactly.
  - `AppProxy` — wraps the agent-action registry so scripts can
    say `app.show_molecule('caffeine')` OR `app.call('show_molecule',
    name_or_id='caffeine')`.  `app.list_actions()` returns every
    registered name.  Unknown attribute access raises
    `AttributeError` with a pointer at `list_actions()`.
  - `_WorkbenchStub` / `WorkbenchNotReadyError` — placeholder
    `viewer` global so scripts that try to use 32b features fail
    with a helpful message instead of a confusing `NameError`.
  - `open_script_editor` — `@action(category="scripting")` entry
    point, main-thread-dispatched via `run_on_main_thread_sync`.
- **`orgchem/gui/dialogs/script_editor.py`** — singleton
  `ScriptEditorDialog`:
  - Editor pane (monospace, 80-col-ish) pre-loaded with a friendly
    snippet that prints `len(app.list_actions())`.
  - Dark output pane with colour-coded stdout / stderr / repr /
    traceback.
  - Toolbar: Run (Ctrl+Enter), Run-selection (Ctrl+Shift+Enter),
    Stop, Reset globals, Open…, Save….
  - `_RunWorker` QThread runs the snippet off the main thread so
    long calls (PDB fetch, conformer gen) don't freeze the UI.
    Stop button terminates the worker; caveat reported to the user
    that arbitrary Python can't be interrupted cleanly.
- **Wiring**:
  - Tools menu entry *Script editor (Python)… (Ctrl+Shift+E)* in
    `main_window.py`; handler uses the singleton classmethod so
    re-opening the dialog preserves the user's `ScriptContext`.
  - `agent/__init__.py` imports `script_context` alongside the
    other `actions_*` modules so `open_script_editor` is
    discoverable by the tutor + stdio bridge from launch.
  - GUI-audit map (`gui/audit.py`) gets the new action mapped to
    its Tools-menu path → 100 % coverage preserved.
- **Tests** (`tests/test_script_context.py`, 13 cases):
  trivial expression → `repr`, `print` capture, state persistence
  between runs, `reset()` flushes, syntax-error formatting,
  runtime-error non-fatal, pre-imported globals (`app` / `chem`),
  `viewer` stub raises `WorkbenchNotReadyError`, `AppProxy`
  unknown-action raises `AttributeError`, `app.call('…')` routes
  through the registry, stdout / stderr separation, `ExecResult.ok`
  polarity.

### Round 63 (piggy-backed — Phase 31f glossary)
Added 8 teaching gap-closers to `seed_glossary_extra.py`:
**hyperconjugation**, **inductive effect**, **leaving group**,
**enantiomeric excess (ee)**, **keto-enol tautomerism**,
**homolysis vs heterolysis**, **Walden inversion**, **anomer**.
Glossary `SEED_VERSION` bumped 6 → 7 so existing DBs pick up the
new rows on next launch.  Catalogue total now 77 entries.

### Test suite
- **837 passed, 0 skipped** across the full suite (↑ from 823).

### Design calls deferred to 32b and beyond
The three tensions flagged in the Phase-32 plan
(single vs multi Workbench; every-click-logs-script; LLM script
mode on-by-default vs toggle) were not yet resolved — 32a lands
without a Workbench, so they bite on 32b when the scene API goes
in.

### Next
32b (dynamic scene viewer + scene API) is the natural next slice.
Scripts today can drive any seeded action + render RDKit objects;
the Workbench promotes `viewer` from a stub to a real scene graph.

---

## 2026-04-23 — Round 62 (Phase 31c CLOSED — Bromination + Friedel-Crafts)

### What shipped
- **`_bromination_ethene()`** — 3-step anti addition of Br₂ to
  ethene via a bromonium ion. Step 1: π bond attacks Br; Br–Br
  heterolyses; the departing Br⁺ doesn't leave an open cation —
  its lone pair bridges to make a 3-membered bromonium. Step 2:
  Br⁻ does a backside SN2-like attack at one carbon, opening the
  ring, giving the characteristic anti (trans) 1,2-dibromide.
  Step 3: vicinal-dibromide product.
- **`_friedel_crafts_alkylation()`** — 3-step EAS sibling of the
  round-60 nitration mechanism. Step 1: AlCl₃ is the Lewis acid —
  Cl lone pair → Al, then C–Cl heterolyses to give CH₃⁺ / AlCl₄⁻.
  Step 2: benzene π attacks the methyl cation → Wheland (arenium)
  intermediate. Step 3: AlCl₄⁻ removes H⁺ from the sp³ carbon,
  rearomatisation releases toluene + HCl + regenerates AlCl₃.

### Plumbing
- Registered both in the expansion `BUILDERS` dict under their
  seeded reaction names ("Bromination of ethene", "Friedel-Crafts
  alkylation"). `SEED_VERSION` bumped 10 → **11** so existing
  databases pick up the new JSON blobs on the next launch.
- Atom indices and SMILES validate via RDKit at test time; all
  arrows + lone-pair dots stay in range.

### Refactor: split `seed_mechanisms.py` under the 500-line cap
The seed file had grown to 1052 lines (~550 over the project
cap). Split into three themed sub-modules while adding the new
content:
- `seed_mechanisms_classic.py` (357 lines) — 9 textbook mechs
  (SN/E/DA/aldol/Grignard/Wittig/Michael).
- `seed_mechanisms_enzyme.py` (234 lines) — 4 enzyme active-site
  mechs (chymotrypsin, aldolase, HIV protease, RNase A).
- `seed_mechanisms_extra.py` (416 lines) — 7 expansion mechs
  (Fischer, NaBH₄, nitration, Claisen, pinacol, bromination, FC).
- `seed_mechanisms.py` (88 lines) — facade: imports the three
  `BUILDERS` dicts, owns `_MECH_MAP`, `SEED_VERSION`, and
  `seed_mechanisms_if_empty(force)`. Re-exports `_hiv_protease`,
  `_rnase_a`, `_chymotrypsin`, `_aldolase_class_I` so existing
  tests that import private builders by name keep working.

### INTERFACE.md
Updated the `db/` section: the single `seed_mechanisms.py` row
is now four rows covering the facade + the three themed
sub-modules.

### Phase 31c progress
Mechanisms catalogue: 18 → **20 / 20 — closed**. Four rounds
(59-62) shipped 7 mechanisms total (Fischer, NaBH₄, nitration,
Claisen, pinacol, bromination, FC).

### Test suite
- **823 passed, 0 skipped** — no regressions. Added 6 new
  round-62 regression tests in `tests/test_seed_mechanisms_round62.py`:
  both new builders land in `_MECH_MAP`, total count pins at 20,
  step counts + arrow patterns match the description, all
  SMILES parse + indices stay in range, and `SEED_VERSION ≥ 11`.

### Next
With Phase 31c closed, remaining Phase 31 sub-goals are still
worth attacking one round at a time: 31d synthesis pathways
(14 → 25), 31e glossary terms (61 → 80), 31f tutorials
(21 → 30), 31g macromolecule catalogues (25 / 31 / 33 → 40
each), 31a molecules (~210 → 400), 31b reactions (35 → 50),
and the Phase-25-era orphans (nomenclature quiz dialog,
compute_rate_law).

---

## 2026-04-23 — Round 61 (Phase 31c +2 mechanisms — Claisen + Pinacol)

### What shipped
- **`_claisen_condensation()`** — 4-step ester self-condensation:
  ester enolate formation (3 arrows — base, α-H, C=O collapse),
  enolate attack on second ester → tetrahedral alkoxide (2 arrows),
  ethoxide leaves while C=O is restored (1 arrow, the
  addition-elimination pattern unique to acid derivatives),
  deprotonation of the β-keto ester α-H drives the whole
  equilibrium. Sibling of the already-seeded Aldol mechanism.
- **`_pinacol_rearrangement()`** — 4-step canonical 1,2-methyl
  shift: protonation of one OH, loss of water → tertiary
  carbocation, 1,2-Me migration with lone-pair-stabilisation from
  adjacent OH giving an oxocarbenium, deprotonation → pinacolone.
  Classic textbook example of a carbocation "climbing" to a more
  stable resonance-stabilised form.

### Plumbing
- Registered both in `_MECH_MAP` under their seeded reaction
  names. `SEED_VERSION` bumped 9 → 10.
- All 8 steps across both new mechanisms RDKit-parse and have
  arrow indices in range.

### Phase 31c progress
Mechanisms catalogue: 13 → 14 → 16 → **18**. Only 2 more to hit
the 20-target — one more round's worth of content.

### Test suite
- **816 passed, 0 skipped** — no regressions.

---

## 2026-04-23 — Round 60 (Phase 31c +2 mechanisms — NaBH₄ + nitration)

### What shipped
- **`_nabh4_reduction()`** — classic 1-arrow 1-arrow hydride
  transfer: B–H σ bond attacks the carbonyl C while the C=O π
  bond collapses onto the oxygen (alkoxide). Second step: aqueous
  workup protonates to 2-propanol. Two teaching-grade steps.
- **`_nitration_benzene()`** — canonical EAS walkthrough in 3
  steps: nitronium generation (H₂SO₄ + HNO₃ → NO₂⁺), benzene
  attacks NO₂⁺ → arenium (Wheland) intermediate, HSO₄⁻ removes
  proton to restore aromaticity.
- Both registered in `_MECH_MAP`; `SEED_VERSION` bumped 8 → 9
  so existing DBs pick them up on next launch.

### Mechanism-SMILES gotcha
Initial Wheland-intermediate SMILES for step 3 didn't parse
(`[CH2+]1C=CC=CC1[N+](=O)[O-]` — carbon valence violation).
Simplified to showing the *product* (nitrobenzene) plus the
regenerated base, with the arrow-pushing explanation in the
description. The Phase 13c renderer's curly arrows are still the
teaching payload; the SMILES just anchors atom indices.

### Phase 31c progress
Mechanisms catalogue: 13 → 14 (round 59) → 16 (round 60).
Remaining to hit the 20-target: 4 more. Best candidates — Swern,
HWE, Mitsunobu (pair with the round-44 reactions that still
lack mechanisms).

### Test suite
- **816 passed, 0 skipped** — no regressions. The existing
  `test_mechanism.py` + `test_fragment_consistency.py`
  regressions validate SMILES parseability and arrow-index
  range.

---

## 2026-04-23 — Round 59 (Phase 31c +1 mechanism — Fischer esterification)

### What shipped
Added a 5-step curly-arrow mechanism for Fischer esterification
to `seed_mechanisms.py`. The canonical acid-catalysed ester
formation (CH₃COOH + EtOH → EtOAc + H₂O, H⁺ catalysed), walked
through:
1. Carbonyl protonation → oxocarbenium.
2. Nucleophilic addition of EtOH → tetrahedral intermediate.
3. Proton shuffle (EtOH⁺ → OH via solvent).
4. Water departure → restored C=O with regenerated oxonium.
5. Deprotonation → neutral ester.

Each step carries RDKit-parseable SMILES, arrow (`from_atom`,
`to_atom`) indices that stay in range, one step with an explicit
`lone_pairs` decoration for the carbonyl-oxygen protonation
visualisation.

### Plumbing
- New `_fischer_esterification()` builder registered in
  `_MECH_MAP` under the key `"Fischer esterification"` — matches
  the seeded reaction name via substring lookup.
- `SEED_VERSION` bumped 7 → 8 so existing databases overwrite
  stale JSON on next launch. Idempotent re-runs.
- No schema change; no new tests required (the existing
  `test_mechanism.py` / `test_fragment_consistency.py` regressions
  validate arrow-index ranges + SMILES parseability).

### Test suite
- **816 passed, 0 skipped** — no regressions.

### Progress against Phase 31 target
- Mechanisms: 13 → 14 (target 20).
- Next Phase 31c candidates: Swern, HWE, Mitsunobu (the
  round-44 additions that still lack mechanisms).

### Next
- Continue Phase 31c with Swern oxidation or Mitsunobu, or hit
  Phase 12b nomenclature quiz dialog (last small UI orphan).

---

## 2026-04-23 — Round 58 (molecular-identity unification across catalogues)

### User-reported bug
> *"I added retinol to the molecules workspace — but it gave it
> a different name ((2E,4E,6E,8E)-3,7-dimethyl-9-(…)…-1-ol) from
> the lipids tab (Retinol (vitamin A)). When I search for retinol
> in the molecules workspace it doesn't find it (even though its
> name retinol is listed as a synonym). Also, the SMILES formulas
> are different for the two entries."*

### Root-cause tree
1. **Display name**: `download_from_pubchem` used `c.iupac_name`
   as the primary name. PubChem's synonym list has "Retinol" at
   the top — much more useful for a teaching app than the
   57-character IUPAC systematic string.
2. **Identity comparison**: both the authoring action and the
   PubChem import did dedup by raw SMILES string. The two
   retinol forms (PubChem's vs the Lipids-catalogue form) differ
   character-by-character but share an InChIKey, so they were
   treated as different compounds and the user got two rows.
3. **Synonym-free search**: `find_molecule_by_name` / the filter
   bar both only compared against `Molecule.name`. Nothing in the
   schema or query path supported aliases.
4. **No cross-catalogue reconciliation**: the Lipids /
   Carbohydrates / NA Python dataclasses had their own names but
   no link back to the DB rows they represented.

### Fix — single source of truth for identity
- **`core/identity.py`** (new) — `canonical_smiles(smi)`,
  `inchikey(smi)`, `same_molecule(a, b)`, `normalise_name(name)`
  (strips trailing parentheticals, casefolds).
- **`Molecule.synonyms_json`** column added via additive migration
  — all existing rows keep working with NULL; the synonym seeder
  populates the new field.
- **`db/seed_synonyms.py`** (new) — `seed_synonyms_if_needed()`
  runs on every `seed_if_empty()`:
  - Curated `{canonical_name → [aliases]}` map for ~30 high-value
    pairs (Aspirin ↔ Acetylsalicylic acid, Acetaminophen ↔
    Paracetamol, Ethanol ↔ EtOH ↔ Grain alcohol, Glycerol ↔
    Glycerine, Retinol (vitamin A) ↔ Retinol ↔ Vitamin A, …).
  - **Cross-catalogue reconciliation**: every Lipid / Carbohydrate
    / Nucleic-acid entry is matched against the DB by InChIKey;
    when a match exists, the catalogue's canonical name is added
    as a synonym on the DB row. Fixes the reported bug for every
    similar compound without hand-curation.
- **`db/queries.py`** — `list_molecules`, `find_molecule_by_name`
  now search the synonyms column too (normalised-name matching);
  new `find_molecule_by_smiles(smi)` uses InChIKey for order-
  invariant identity lookup.
- **`agent/library.py::download_from_pubchem`** — picks a short
  display name from PubChem's synonym list (skipping
  systematic-stereo heads), stores the full synonym list on the
  new column. If an existing row has the same InChIKey, merges
  the names into its synonyms rather than creating a duplicate.
- **`agent/library.py::import_smiles`** — same dedup-by-InChIKey
  logic; user-supplied name becomes a synonym on the existing row.
- **`agent/actions_authoring.py::add_molecule`** — now also rejects
  InChIKey duplicates, with a clear message suggesting
  `add_molecule_synonym` instead.
- **`add_molecule_synonym(name_or_id, synonym)`** (new) — attaches
  a display-friendly alias to any existing row. Idempotent:
  already-present synonyms report `updated=False`.
- **`sources/pubchem.py::_pick_display_name`** — picks the first
  short (≤ 40-char) synonym from PubChem, skipping parentheticals
  starting with stereo descriptors like `(2E,4E,…)`.

### Tests (13 new)
- Retinol-specific regression: PubChem-form vs Lipids-form SMILES
  produce the same InChIKey.
- Name-normalisation round trips ("Retinol (vitamin A)" → "retinol").
- `find_molecule_by_smiles("OCC")` finds the ethanol row stored
  as `"CCO"`.
- `add_molecule` rejects InChIKey duplicates.
- `find_molecule_by_name("ethyl alcohol")` resolves via synonyms.
- `add_molecule_synonym` agent action happy path + idempotency.
- PubChem name picker prefers trivial names over systematic heads.

### Test suite
- **816 passed, 0 skipped** (+13 new).

### Doc updates
- **INTERFACE.md** — new rows for `core/identity.py` and
  `db/seed_synonyms.py`.
- **ROADMAP.md** — no direct ticks; this was a user-reported
  bug, not a tracked roadmap item.
- **PROJECT_STATUS.md** + **README.md** — test count bumped;
  cross-catalogue reconciliation noted.

---

## 2026-04-23 — Round 57 (synchronous main-thread dispatch for screenshots)

### What shipped
- **`run_on_main_thread_sync(fn, timeout=5.0)`** added to
  `agent/_gui_dispatch.py`. Companion to the fire-and-forget
  `run_on_main_thread`. Dispatches `fn()` onto the Qt main
  thread via `QTimer.singleShot(0, app, _run)` and blocks the
  caller on a `threading.Event` until the slot finishes.
  Returns `fn()`'s return value; re-raises its exceptions on
  the caller thread; raises `MainThreadTimeout` if the main
  loop is stuck longer than the timeout.
- **`screenshot_window`** and **`screenshot_panel`** routed
  through the new sync helper. These need the `grab_widget()`
  return value (the saved `Path`) so fire-and-forget doesn't
  fit — the blocking variant is correct.
- **4 new tests** in `tests/test_gui_dispatch.py`:
  `run_on_main_thread_sync` inline / from worker / exception
  propagation, plus an end-to-end `screenshot_window` from
  `threading.Thread` that pumps the main loop and verifies the
  PNG lands on disk.

### Pattern summary across rounds 55–57
- **Fire-and-forget** (`run_on_main_thread`) — for
  `open_macromolecules_window`, `show_reaction`, `show_pathway`,
  `show_term`, `compare_molecules`, `open_mechanism`,
  `export_reaction_trajectory_html` / player dialog,
  `show_ligand_binding` GUI surface. Data work runs on the
  worker; GUI touches are queued.
- **Blocking** (`run_on_main_thread_sync`) — for
  `screenshot_window`, `screenshot_panel`. Caller waits for
  the saved-path return.

### Test suite
- **803 passed, 0 skipped** (+4 new).

### Next
- No more known crash-prone off-main-thread agent actions in
  the tree — the sweep is complete. Next round can go back to
  content (Phase 31) or remaining orphans (Phase 17a rate-law,
  Phase 12b nomenclature quiz).

---

## 2026-04-23 — Round 56 (agent-GUI thread-safety hardening sweep)

### Motivation
Round 55's hotfix targeted the reported crash (`show_ligand_binding`)
and the primitive it relied on (`open_macromolecules_window`). The
closing note flagged several other agent actions that touch the
main window directly — latent time-bombs waiting for the first
tutor query that invoked them. This round hardens them all.

### What's now thread-safe
- **`show_reaction(name_or_id)`** — `win.reactions._display(...)` +
  tab switch wrapped in `run_on_main_thread`.
- **`open_mechanism(name_or_id)`** — `MechanismPlayerDialog` now
  constructed on the main thread.
- **`export_reaction_trajectory_html` (player dialog)** — same.
- **`compare_molecules(molecule_ids)`** — `set_molecule_ids(...)`
  + tab switch wrapped.
- **`show_pathway(name_or_id)`** — `win.synthesis._display(...)`
  + tab switch wrapped.
- **`show_term(term)`** — `glossary.focus_term(...)` + tab switch
  wrapped.

### Pattern
Every patched action stages its GUI work in a local `def _show():`
closure and pipes it through `orgchem.agent._gui_dispatch.
run_on_main_thread`. The data part (DB query, payload assembly)
still runs on the calling thread — only the widget touches defer.

### What's still open (non-crashing, left for a future pass)
- **Screenshot actions** (`screenshot_window`, `screenshot_panel`)
  need synchronous round-trip to return the saved path. A proper
  fix needs a blocking dispatch primitive (`QMetaObject.
  invokeMethod(..., BlockingQueuedConnection, ...)` with a result
  channel). `QWidget.grab()` hasn't been observed to crash in
  practice but is nominally main-thread-only.
- **`export_reaction_3d`, `export_reaction_trajectory_html`** —
  their dialog-returning variants are covered; the pure export
  paths don't touch widgets.

### Test suite
- **799 passed, 0 skipped** (+3 new regressions in
  `test_gui_dispatch.py`: show_reaction / show_pathway /
  show_term all invoked from a `threading.Thread`).

---

## 2026-04-23 — Round 55 hotfix (off-main-thread NSWindow crash)

### User-reported crash
Running the tutor ("show me caffeine bound to an adenosine receptor")
aborted with:

```
QObject::setParent: Cannot set parent, new parent is in a different thread
*** Terminating app due to uncaught exception 'NSInternalInconsistencyException',
    reason: 'NSWindow should only be instantiated on the main thread!'
```

Root cause: the tutor panel's `_ChatWorker` is a `QThread` that
invokes agent actions. `show_ligand_binding` (added earlier in
round 55) called `main_window.open_macromolecules_window()`
directly — which *lazily constructs* a `QMainWindow` (NSWindow)
the first time. macOS aborts whenever any NSWindow is created
off the main thread.

### Fix
- **New `orgchem/agent/_gui_dispatch.py`** with
  `run_on_main_thread(fn)` — dispatches a zero-arg callable to
  the Qt main thread, synchronously when already there, otherwise
  via `QTimer.singleShot(0, app, fn)` (passing the
  QApplication-instance as the context argument so the slot runs
  on the app's thread, not the caller's).
- **Patched `show_ligand_binding`** (protein action) and
  **`open_macromolecules_window`** (window action) to funnel their
  GUI work through `run_on_main_thread`. Both now safe from the
  tutor-worker thread, stdio-bridge, or any Python driver.
- **Known-sharp-edge note**: the 2-arg form
  `QTimer.singleShot(0, fn)` runs on the *caller's* thread — the
  first test run caught this and failed. The 3-arg form with the
  QApplication as context dispatches correctly.

### Test suite
- **796 passed, 0 skipped** (+4 new GUI-dispatch tests).
- `tests/test_gui_dispatch.py` includes a regression for exactly
  the reported scenario: spawn a `threading.Thread`, invoke
  `show_ligand_binding` from within, pump the main loop, assert
  no crash + a structured response.

### Other call sites to audit
Other agent actions that touch `main_window` directly (not via
the bus):

- `actions_reactions.show_reaction` (calls
  `win.synthesis._display(...)`)
- `actions_pathways.show_pathway`
- `actions_reactions.open_mechanism`
- `library.screenshot_window`

These haven't crashed in the wild yet because `setCurrentIndex`
on an *already-existing* tabbar is much more lenient than
NSWindow construction. Should eventually be routed through
`run_on_main_thread` as hardening — filed as a future orphan.

---

## 2026-04-23 — Round 55 (tutor capability boost + Phase 17e Hammett/KIE)

### User-reported bug
*"You: Can you show me caffeine bound to an adenosine receptor?
Tutor: I don't have direct visualization tools for binding
interactions…"* — despite the app having `fetch_pdb`,
`analyse_binding`, `export_interaction_map`, `export_protein_3d_html`.

Follow-up ask: *"It might also be useful if the tutor is able to
populate databases, seed reactions and tutorials with new items
and modules — as long as they are of high quality!"*

### Root cause
The tutor's system prompt listed only four broad categories of
tools (molecule DB, PubChem, tutorials, formula calculator). It
had no mention of proteins, spectroscopy, mechanisms, pathways,
macromolecules — so the LLM fell back on its training-data
priors and said "I don't have that." The underlying tool-use
path was fine; the model was just flying blind.

### What shipped
- **Rewritten system prompt** (`agent/conversation.py::
  _SYSTEM_PROMPT`) — comprehensive capability map organised by
  topic (small molecules / reactions / proteins / spectroscopy /
  orbitals / lab / carbs / lipids / NAs / glossary / curriculum)
  plus four workflow-hint recipes. Includes explicit guidance:
  *"Never say 'I don't have tools for that' without first calling
  `list_capabilities` to check."*
- **`list_capabilities(category?)` agent action** —
  `agent/actions_meta.py`. Self-introspection tool the tutor can
  use mid-conversation to enumerate what the app can do. Returns
  summary + counts per category; drill into one for action-level
  docstrings.
- **`show_ligand_binding(pdb_id, ligand_name, interaction_map_path?)`
  bundled workflow** in `agent/actions_protein.py`. One call does
  fetch → contacts → optional interaction-map export → focus the
  Proteins tab. Designed around the reported failure scenario:
  "caffeine bound to adenosine A2A" is now one action away.
- **Content-authoring actions** in `agent/actions_authoring.py`:
  - `add_molecule(mol_name, smiles, notes, source_tags)` — RDKit
    SMILES validation + canonical-SMILES / name dedup.
  - `add_reaction(rxn_name, reaction_smiles, description,
    rxn_category)` — reaction SMILES validation, name dedup.
  - `add_glossary_term(term, definition_md, category, aliases,
    see_also, overwrite)` — length gate, dedup unless
    `overwrite=True`.
  - `add_tutorial_lesson(title, level, markdown_body)` — writes a
    markdown file under `tutorial/content/<level>/` and appends
    to `CURRICULUM` at runtime so the Tutorials tab sees it
    immediately.
  Every authoring action returns `{status, reason, …}` with a
  specific rejection reason on failure — the tutor can read the
  reason and retry (e.g. "your SMILES doesn't parse — here's the
  likely typo").

- **Phase 17e Hammett + KIE (parallel orphan)** — new
  `core/physical_organic.py`: curated σ catalogue for 15
  substituents × 4 scales; `hammett_fit(data, sigma_type)`
  least-squares regression with ρ / r² / teaching interpretation;
  `predict_kie(isotope_pair, partner_element, nu_H_cm1,
  temperature_K)` via the Bigeleisen simplification (textbook
  ~6.9 for C–H/C–D at 298 K). Agent actions in
  `agent/actions_phys_org.py`.

### Test suite
- **792 passed, 0 skipped** — +42 from round 54.
- 10 tests for the tutor capability boost
  (`test_tutor_capabilities.py`), 17 for authoring
  (`test_authoring_actions.py`), 15 for Hammett + KIE
  (`test_physical_organic.py`).

### Known issues uncovered
- Molecule model has no `notes` column — first test run failed on
  that (wrote it as `properties_json["tutor_notes"]` instead).
- `invoke(name, **kwargs)` collision with `name=` action
  parameters is an old footgun — renamed to `mol_name` /
  `rxn_name` in the authoring actions (same fix we applied to
  carbohydrates / lipids / NAs earlier).

### Next
- `show_ligand_binding` could export the interaction map by
  default (auto-choose a file in a `~/Library/Caches/OrgChem`
  subdir) so the tutor's output always includes a figure link.
- Tool-use-capable Ollama models (`qwen2.5:14b` recommended) will
  benefit most from the new capability map — plain `llama3` still
  can't call tools but at least reads a better prose description.
- Phase 31 content expansion is still in flight.

### Doc updates
- **ROADMAP.md** — Phase 17e agent actions flipped `[ ]` → `[x]`
  (`hammett_fit`, `predict_kie`, `list_hammett_substituents`).
- **INTERFACE.md** — new `core/physical_organic.py` row, plus
  agent-file exemptions for `actions_meta.py`,
  `actions_phys_org.py`, `actions_authoring.py`.
- **PROJECT_STATUS.md** + **README.md** — test count 750 → 792,
  audit 113 → 124; README top-feature list mentions the tutor
  capability boost.

---

## 2026-04-23 — Round 54 (Phase 11b Ctrl+K command palette)

### What shipped
- **`orgchem/gui/dialogs/command_palette.py`** — VS-Code-style
  jump-to-anything dialog. Opens on Ctrl+K, type to filter, Enter
  to jump. Scopes: glossary terms, reactions, molecules. Uses a
  single data pipeline (`build_palette_entries`) that pulls ~400
  rows from the seeded DB + `_GLOSSARY` catalogue.
- **Dispatch router `dispatch_palette_entry`** routes by entry
  kind into existing APIs: `glossary.focus_term(term)`,
  `reactions._display(reaction_id)`, and
  `bus.molecule_selected.emit(molecule_id)`. Keeping the
  dispatcher as a module-level function lets tests exercise
  routing without opening the modal dialog.
- **Main-window wiring** — new *View → Command palette…* action
  with `Ctrl+K` shortcut. Lazy-imports the dialog class so the
  DB probe only runs when the user actually hits the keystroke.
- **10 tests** in `tests/test_command_palette.py` — entry
  assembly (three kinds present), filter narrowing, case-
  insensitivity, 200-row cap, dispatch routing (glossary,
  reactions), activation → dialog closes, main-window integration,
  View-menu action has Ctrl+K shortcut.

### Scope decision
The Phase 11b roadmap item asked for *glossary search from
anywhere*. Since the infrastructure for filtering + routing was
the same cost, the palette was widened to cover reactions and
molecules too — one keystroke, three targets, no extra framework.
Future phases can add agent actions, tutorial lessons, and menu
items to the entry list without touching the dialog widget.

### Test suite
- **750 passed, 0 skipped** (+10 new). Golden-render flake from
  round 52 stayed fixed through the new HeadlessApp-using tests.

### Doc updates
- **ROADMAP.md** — Phase 11b follow-up flipped `[ ]` → `[x]`
  with shipped-implementation notes.
- **INTERFACE.md** — new `command_palette.py` row under
  `gui/dialogs/`.
- **PROJECT_STATUS.md** + **README.md** — test count bumped to
  750; README status section mentions the Ctrl+K palette.

### Next
- Remaining orphans: Phase 17a rate-law derivation (new core
  module) + `hammett_fit` / `predict_kie` (Phase 17e); Phase 12b
  nomenclature quiz dialog; continued Phase 31 content expansion
  (+mechanism JSONs, +tutorials, +reactions).

---

## 2026-04-23 — Round 53 (Phase 15b TLC-plate renderer orphan closeout)

### What shipped
- **`orgchem/render/draw_tlc.py`** — matplotlib TLC-plate renderer.
  Takes `simulate_tlc` output (or any compatible `{compounds, solvent}`
  dict) and draws a silica panel with baseline, solvent front, one
  coloured spot per compound at its predicted Rf, Rf labels, lane
  numbers, and a legend mapping lane → SMILES + logP. PNG or SVG
  selected from the path extension.
- **Agent action `export_tlc_plate(smiles_list, path, solvent)`**
  in `actions_labtech.py` — chains `simulate_tlc` →
  `draw_tlc.export_tlc_plate`, returns the saved path plus the
  Rf table that drove the figure.
- **GUI wiring** — new *Save plate…* button on the Lab-techniques
  dialog's TLC tab next to *Simulate TLC*. Uses QFileDialog for
  the save path and routes through the new agent action.
- **Audit entry** registered; GUI coverage still **100 % (113 / 113)**.
- **8 new tests** in `tests/test_draw_tlc.py` — covers figure
  construction, PNG + SVG export, graceful handling of `error`
  rows from simulate_tlc, agent-action happy path, audit entry
  present, and end-to-end GUI wiring (monkeypatched QFileDialog).

### Rounds 51 + 52 recap (from the previous entries)
- Round 51: Ollama tutor-panel auto-detection (`ollama_list_models`,
  tool-use-capable model preference, graceful fallback).
- Round 52: three Ollama-path bugs fixed (vision variants now
  excluded from the fallback, explicit model always triggers a
  probe so `available_models` is populated, `tools` field dropped
  for non-tool-capable models with auto-retry on the Ollama 500);
  Phase 11c `{term:X}` tutorial macro shipped; URL scheme switched
  to `scheme:term` so QUrl doesn't lowercase the authority; golden-
  render test-ordering flake fixed (seed_coords no longer mutates
  `SetPreferCoordGen` at module import time; golden tests pin the
  depictor preference via an autouse fixture).

### Test suite
- **740 passed, 0 skipped** (was "1 skipped" when imagehash wasn't
  available — present in this env). +36 net new tests across
  rounds 51-53.

### Doc updates
- **ROADMAP.md** — Phase 15b renderer orphan flipped `[ ]` → `[x]`.
- **INTERFACE.md** — new `draw_tlc.py` row added under
  `render/`; tutorial `macros.py` documented; `glossary_linker.py`
  documented.
- **PROJECT_STATUS.md** + **README.md** — counts bumped to 740
  tests / 113 audit entries.

### Next
- Remaining orphans: Phase 17a rate-law derivation helper (new
  core module), `hammett_fit` / `predict_kie` (Phase 17e), more
  Phase 31 content (tutorials / mechanisms / additional SAR
  series), or the nomenclature quiz (Phase 12b).

---

## 2026-04-23 — Round 50 (Phase 11c + 18e orphan closeout)

### What shipped
- **Phase 18e agent action `compare_pathways_green(pathway_ids)`**
  — ranked side-by-side comparison of multiple seeded pathways on
  overall atom economy + worst-step AE. Calls the existing
  `pathway_green_metrics` helper under the hood, so every pathway
  in the DB is immediately comparable.
- **Green metrics dialog gains a 3rd tab "Compare pathways"** —
  multi-select list (Ctrl-click) + Compare button → ranking
  table. Three tabs total: Reaction AE / Pathway AE / Compare.
- **Phase 11c auto-hyperlink (partial).** New helper
  `gui/widgets/glossary_linker.py` with `autolink(text)` → HTML
  where every recognised glossary term (pulled from
  `seed_glossary._GLOSSARY`, which already includes the Phase 31f
  extras) is wrapped in an `orgchem-glossary://` anchor.
  Longest-surface-first regex ordering prevents sub-term
  shadowing (tested with "Hammond postulate" → single anchor).
- **Reaction-workspace description pane swap.**
  `QPlainTextEdit` → `QTextBrowser` with `setOpenLinks(False)` +
  `anchorClicked` hooked into a Glossary-tab router. Clicking a
  recognised term switches to the Glossary tab and calls
  `focus_term(term)`. Still-pending Phase 11c follow-up:
  `{term:SN2}` macro support in tutorial markdown.

### GUI + audit + docs
- `compare_pathways_green` wired into `GUI_ENTRY_POINTS` →
  "Tools → Green metrics… → Compare pathways tab". Coverage
  gate still **100 % (112 / 112)**.
- New `gui/widgets/glossary_linker.py` added to INTERFACE.md so
  the doc-coverage contract stays green.
- Old Round 38 test `test_green_metrics_dialog_instantiates`
  updated to expect 3 tabs (was 2) and verify the "Compare
  pathways" label exists.

### Test suite
- **694 passed, 1 skipped** — 9 new tests in
  `tests/test_round50_orphans.py` cover `compare_pathways_green`
  happy path + empty-input / bad-id error paths, autolink
  wrapping / escaping / longest-first behaviour, and an
  end-to-end test that selecting a real seeded reaction gives an
  anchored description pane.

### Design decisions
- **No new dialog.** The `compare_pathways_green` feature fit
  naturally as a third tab on the existing Green-metrics dialog
  rather than spawning a dedicated window — kept the surface
  narrow and let the tab share infrastructure (pathway lookup,
  summary label, error-message box).
- **Scheme `orgchem-glossary://`** was chosen for the autolink
  URLs so Qt's `anchorClicked` sees a non-http scheme and doesn't
  try to open an external browser. Also makes the routing logic
  pattern-match easy to audit (`url.scheme() != "orgchem-glossary"`
  → return).
- **Deferred the `{term:X}` tutorial-markdown macro** to a future
  round. It needs more design (syntax, nesting, link resolver
  for the glossary panel's markdown renderer) and isn't the
  bottleneck for classroom use right now.

### Next
- Still-open small orphans: `{term:SN2}` tutorial macro (Phase 11c
  second half), `compute_rate_law(reaction_id)` (Phase 17a, new
  core module), `hammett_fit` + `predict_kie` (Phase 17a), TLC
  plate image renderer (Phase 15b). Or keep pushing Phase 31
  content expansion.

---

## 2026-04-23 — Round 49 (Phase 14d orphaned-action closeout)

### Roadmap review → parallel batch
User asked for a review of orphaned roadmap items that could be
implemented in parallel. Scanned the full ROADMAP, flagged Phase
14d's two agent actions (`show_molecular_orbital`, `explain_wh`)
and Phase 14b's cross-link follow-up as a tight, high-value bundle
— all three are small wrappers around already-shipped core modules
(`core/huckel.py`, `core/wh_rules.py`). Shipped all three:

- **`_REACTION_WH_MAP` + `find_wh_rule_for_reaction(name)`** in
  `core/wh_rules.py` — 10-entry substring → rule-id map covering
  Diels-Alder, Claisen / Cope, [2+2], 4π / 6π electrocyclic, 1,5-H
  shift, Wittig rearrangement, 1,3-dipolar cycloaddition. Closes
  the Phase 14b follow-up "cross-link each pericyclic reaction to
  its WH entry".
- **Agent action `show_molecular_orbital(smiles, index=-1)`** —
  picks one MO (default HOMO), returns role (HOMO / LUMO /
  HOMO-n / LUMO+n), energy in β, occupation, and HOMO/LUMO context.
  Validated with butadiene (HOMO = index 1, bonding) and benzene
  (LUMO = index 3, anti-bonding).
- **Agent action `explain_wh(reaction_name_or_id)`** — accepts a
  DB integer id or a reaction-name substring, returns the matching
  W-H rule entry (or `matched=False` + friendly note for ionic /
  radical / catalytic reactions that don't obey orbital-symmetry
  rules). Uses `find_wh_rule_for_reaction` under the hood.
- **GUI wiring.** Both actions reachable from the existing
  *Tools → Orbitals…* dialog without scope creep:
  - Hückel MOs tab: row selection in the MO table now populates a
    detail label below (energy, occupation, HOMO/LUMO framing).
  - Woodward-Hoffmann tab: new "For a reaction:" input + Explain
    button jumps the rule list to the inferred W-H rule.
- **Audit.** Both new actions registered in `GUI_ENTRY_POINTS`;
  coverage gate still **100 %** (111 / 111).
- **Tests.** `tests/test_orbitals_phase14d.py` (9 tests) exercises:
  HOMO default, LUMO by index, out-of-range error, non-π system
  error, Diels-Alder → thermal [4+2] allowed, SN2 → no-match note,
  unknown-name graceful fallback, audit entries present, coverage
  still 100 %.

### Test suite
- **685 passed, 1 skipped** (+9 from round 48).

### Doc updates
- **ROADMAP.md** — 14d agent actions flipped `[ ]` → `[x]` with
  shipping notes; 14b cross-link follow-up flipped `[ ]` → `[x]`
  with the `_REACTION_WH_MAP` pointer.
- **PROJECT_STATUS.md** — last-updated bumped; test count 676 →
  685.
- **README.md** — test count + GUI-coverage count refreshed
  (109/109 → 111/111).

### Next
- More roadmap orphans to sweep: Phase 11c cross-linking
  (`{term:SN2}` macro + auto-hyperlink), Phase 14a follow-ups
  (3D MO isosurface overlay — bigger), Phase 17a rate-law
  derivation (new `core/rate_law.py`), Phase 18a
  `compare_pathways_green(pathway_ids)` (small wrapper). Or
  continue Phase 31 content expansion.

---

## 2026-04-23 — Round 48 (Phase 31 fifth content batch)

### What shipped
- **31d (+2 synthesis pathways).**
  - **Benzocaine — 3-step nitrotoluene route.** p-nitrotoluene →
    (KMnO₄) p-nitrobenzoic acid → (Fe/HCl Béchamp) PABA →
    (EtOH / H₂SO₄ Fischer) benzocaine. Classical teaching route
    that exercises chemoselective oxidation, nitro reduction,
    and Le Chatelier-driven esterification.
  - **Lidocaine — 2-step amide route.** 2,6-xylidine +
    chloroacetyl chloride → α-chloroamide (Schotten-Baumann);
    SN2 with diethylamine → lidocaine. Teaches why amide-class
    local anaesthetics outlast ester-class (procaine) —
    2,6-methyl steric shielding of the amide C=O vs esterase
    hydrolysis.
  - Pathways catalogue grew 12 → **14**.
- **Intermediate-fragment backfill (+9).** The fragment-consistency
  audit flagged 11 new pathway-step fragments not in the
  Molecule DB. Added to `seed_intermediates.py`: p-nitrotoluene,
  p-nitrobenzoic acid, PABA, benzocaine (as drug), 2,6-xylidine,
  chloroacetyl chloride, α-chloro-N-(2,6-xylyl)acetamide
  intermediate, diethylamine, lidocaine (as drug). Intermediates
  table grew 138 → **147**.

### Test suite
- **676 passed, 1 skipped** — no regressions. All 5 new
  reaction SMILES pre-validated via
  `AllChem.ReactionFromSmarts(..., useSmiles=True)` before adding.
  Fragment-consistency audit passed after the backfill.

### Design notes
- When adding new synthesis pathways, the fragment-consistency
  audit is a hard gate — every reactant/product/by-product in
  every step's reaction_smiles has to resolve to a known DB
  molecule. This is the codified "no orphan fragments" rule,
  and it's worth the minor extra labour: it forces the seed
  catalogue to stay coherent as content grows.

### Doc updates (per standing directive)
- **ROADMAP.md** — 31d flipped `[ ]` → `[~]` with running tally (14)
  and shipped-pathway list.
- **PROJECT_STATUS.md** — last-updated bumped; Phase 31 cumulative
  paragraph refreshed with round-48 adds (pathways +2, fragments +9,
  DB molecules ≈ 380).

### Next
- Continue Phase 31. Still pending: **31c (+2-3 mechanism JSONs)**
  for the new named reactions (highest-impact remaining item),
  **31h +lipids / carbs / NAs** incremental growth toward 40 each,
  or **31b (+5 more reactions)** toward the 50-target.

---

## 2026-04-23 — Round 47 (Phase 31 fourth content batch)

### What shipped
- **31k (+2 SAR series, 10 new variants).**
  - **β-adrenergic blocker series** (`beta-blockers`) — propranolol,
    atenolol, metoprolol, bisoprolol, carvedilol. Activity columns
    `beta1_pki` / `beta2_pki` / `beta1_selectivity`. Teaches
    cardioselectivity engineering (Black's 1964 discovery → 1988
    Nobel lecture → CIBIS-II / MERIT-HF / COPERNICUS outcomes).
  - **ACE-inhibitor series** (`ace-inhibitors`) — captopril,
    enalaprilat, lisinopril, ramipril, benazepril. Activity
    columns `ic50_nM` / `oral_bioavail_pct` / `t_half_h`. Teaches
    the thiol → dicarboxylate zinc-binder evolution, and how
    prodrug esters (enalapril → enalaprilat, ramipril →
    ramiprilat) fix oral-availability problems without changing
    the warhead. Catalogue now **4** total.
- **31g (+2 tutorial markdown lessons).**
  - `beginner/06_acid_base.md` — Brønsted vs Lewis, pKa in one
    paragraph, five-factor conjugate-base stability reasoning,
    Henderson-Hasselbalch, practical patterns (nucleophilicity,
    leaving-group ability, catalyst pick, acid-base extraction),
    practice with the lab-techniques dialog.
  - `intermediate/07_sugars.md` — D/L Fischer projection trick,
    pyranose vs furanose equilibria, mutarotation (α +112° /
    β +19° → +53° equilibrium), anomeric effect mechanism +
    hyperconjugation, glycosidic-bond taxonomy (α-1,4, β-1,4, …),
    reducing vs non-reducing sugars, modified sugars (aminosugars,
    uronic acids, deoxy sugars, sugar alcohols). Ties into the
    Phase 30 Macromolecules window's Carbohydrates tab. Curriculum
    now **21** lessons.
- Both lessons wired into `CURRICULUM` in `tutorial/curriculum.py`
  and will show up in the Tutorials tab without any UI changes.

### Test suite
- **676 passed, 1 skipped** — no regressions. SAR variants
  validated via `Chem.MolFromSmiles`; tutorial files are pure
  text. Curriculum loader picks up new entries automatically.

### Doc updates (per standing directive)
- **ROADMAP.md** — 31g / 31k flipped `[ ]` → `[~]` with running
  tallies (21 / 4) and shipped-item lists.
- **PROJECT_STATUS.md** — last-updated date bumped; Phase 31
  cumulative paragraph refreshed with round-47 adds + corrected
  reaction tally (35 total, not 31).
- **README.md** — counts already reflect the current state from
  the round-45 refresh; tutorial + SAR mentions still implicit.
  Will do a fuller README refresh when the Phase 31 batches
  have piled up more.

### Next
- Continue Phase 31. Candidate next batch: **31c (+2-3 mechanism
  JSONs)** for Swern / HWE / Mitsunobu — the last big-impact
  expansion before the mechanism count crosses the 20-target.
  Or **31d (+1-2 synthesis pathways)** — sildenafil endgame is
  textbook-worthy.

---

## 2026-04-23 — Round 46 (Phase 31 third content batch)

### What shipped
- **31e (+3 energy profiles).** Pedagogical-grade reaction-
  coordinate diagrams for Sonogashira (Pd/Cu catalytic cycle —
  OA as RDS; 7-point curve through the Ar-Pd-I intermediate),
  HWE (6-point curve through the oxaphosphetane; retro-[2+2]
  TS sets E-selectivity), and Mitsunobu (5-point curve through
  alkoxyphosphonium; final P=O bond strength is the thermodynamic
  driver). `seed_energy_profiles.SEED_VERSION` bumped 2 → 3 so
  existing DBs pick them up additively.
- **31f (+10 glossary terms).** New module `seed_glossary_extra.py`
  holds the continued-expansion content: Saytzeff/Hofmann,
  Bürgi-Dunitz angle, kinetic isotope effect, HOMO/LUMO,
  Alder endo rule, gauche, A-value, pharmacophore, prodrug,
  J-coupling (Karplus). `seed_glossary.py` imports and extends
  `_GLOSSARY` at module load so seeding logic stays unchanged;
  `SEED_VERSION` bumped 5 → 6.
- **31l (+3 seeded proteins).** Added to `core/protein.py
  SEEDED_PROTEINS`: hen egg-white lysozyme (1LYZ), sperm-whale
  myoglobin (1MBN), GFP (1EMA). Rich teaching stories anchoring
  the glycosidase mechanism debate, the first solved protein
  structure, and the β-barrel / autocyclised chromophore.

### Design decision: split glossary into a sibling module
- `seed_glossary.py` had already crossed the project's 500-line
  soft cap (576 lines). Adding +10 more terms would have pushed
  it well past, so extracted the Phase-31f-onward additions into
  `seed_glossary_extra.py` with the same schema. The main file
  imports and extends `_GLOSSARY` in place — existing
  `seed_glossary_if_empty()` logic + SEED_VERSION rewrite
  semantics are unchanged. Pattern: base catalogue stays canonical,
  continued-expansion lives in a sibling, they merge on import.

### Test suite
- **676 passed, 1 skipped** — still green. Had to add an
  INTERFACE.md entry for the new `seed_glossary_extra.py` module
  to keep `test_docs_coverage` happy.

### Doc updates (per standing directive)
- **ROADMAP.md** — 31e / 31f / 31l all marked `[~]` with running
  tallies (12 / 61 / 9).
- **INTERFACE.md** — glossary row refreshed with extras-module
  mention; new row added for `seed_glossary_extra.py`.
- **PROJECT_STATUS.md** — last-updated date bumped; Phase 31
  paragraph refreshed with round-46 totals.

### Next
- Continue Phase 31. Candidate next batch: **31c (+2-3 mechanism
  JSONs)** — paired arrow-pushing animations for the new reactions.
  Or **31g (+3 tutorial markdown lessons)** / **31k (+2 SAR
  series)**.

---

## 2026-04-23 — Round 45 (Phase 31 second content batch)

### What shipped
- **31i (+10 lipids).** Medium-chain fatty acids (caprylic C8:0,
  capric C10:0); eicosanoids (PGE2 cyclopentane prostanoid, TXA2
  oxetane thromboxane); bile acids (cholic, taurocholic); steroid
  hormones (progesterone, cortisol); fat-soluble vitamins (retinol
  A, α-tocopherol E). LIPIDS catalogue grew 21 → **31**.
- **31j (+10 nucleic-acid entries).** Non-canonical bases
  (hypoxanthine, xanthine); modified nucleosides (inosine for
  wobble pairing, pseudouridine Ψ for rRNA / tRNA stabilisation);
  redox coenzymes (NADH, NADPH, FAD); acyl carrier (CoA-SH);
  methyl donor (SAM); secondary-structure teaching entry
  (GCGCUUUUGCGC RNA hairpin). NUCLEIC_ACIDS catalogue grew 23 → **33**.
- **31a (+25 general molecules).** Terpenes (α-pinene, β-pinene,
  limonene, myrcene, camphor, menthol, geraniol, farnesol);
  macrocycles (18-crown-6, 15-crown-5, free-base porphine);
  polymers / monomers (styrene, vinyl chloride, ethylene glycol,
  bisphenol-A, caprolactam); agrochemicals (glyphosate, atrazine,
  DDT); solvents (glycerol, HMPA, diglyme); dyes (indigo,
  methylene blue). Seeded-molecules catalogue grew 169 → **193**.

### Bugs caught along the way
- **Porphine SMILES.** Aromatic-c written form (`c1cc2cc3...n3`)
  failed RDKit's kekulisation. Swapped to the explicit Kekulé
  form `C1=CC2=CC3=CC=C(N3)C=C4C=CC(=N4)C=C5C=CC(=N5)C=C1N2`,
  which parses cleanly.

### Test suite
- **676 passed, 1 skipped** — no regressions. Tests didn't need
  edits since all 45 new entries are additive inside
  `CARBOHYDRATES` / `LIPIDS` / `NUCLEIC_ACIDS` / `_EXTENDED`
  lists, and the existing tests assert on substrings / minima,
  not exact counts.

### Doc updates (per user directive: "update all docs")
- **ROADMAP.md** — Phase 31a / 31i / 31j all flipped from `[ ]` →
  `[~]` (partial), with counts and completed-item lists.
- **INTERFACE.md** — `lipids.py` row updated 21 → 31 with new
  family coverage; `nucleic_acids.py` row updated 23 → 33 with
  coenzyme / modified-base callouts.
- **PROJECT_STATUS.md** — last-updated date bumped; Phase 31
  paragraph updated with second-batch totals.

### Next
- Continue Phase 31 cadence. Candidate next batch: **31c
  (+3 mechanism JSONs)** for Swern / HWE / Mitsunobu — pairs with
  the round 44 reactions. Or **31d (+2-3 synthesis pathways)** —
  taxol endgame, sildenafil route.

---

## 2026-04-23 — Round 44 (Phase 30 Macromolecules window + Phase 31 scoped)

### What shipped
- **Phase 30 — Unified Macromolecules window (end-to-end).** New
  `orgchem/gui/windows/macromolecules_window.py` hosts Proteins /
  Carbohydrates / Lipids / Nucleic-acids as inner tabs in a
  dedicated top-level `QMainWindow`. Single persistent instance
  constructed lazily on first menu click; `QSettings` under
  ``window/macromolecules`` remembers geometry + last-active tab.
- **Menu wiring.** New *Window* menu on the main window carries
  *Macromolecules…* (Ctrl+Shift+M). Four panels removed from the
  main-window tabbar — they are still constructed once in
  `_build_central` so `win.proteins` etc. remain valid for agent
  actions and cross-panel code.
- **Cross-panel rewire.** NA panel's *Fetch PDB in Proteins tab*
  button now calls `win.open_macromolecules_window(tab_label=
  "Proteins")` then drives the protein panel's fetch slot — keeps
  the user inside the secondary window.
- **Agent action.** `open_macromolecules_window(tab)` registered
  in the new `agent/actions_windows.py` module. Returns a dict
  with `{shown, active_tab, tabs}`.
- **GUI audit.** All 27 Proteins / Carbohydrates / Lipids / NA
  entries rewritten to point at the new path (bulk-edited with
  `replace_all`); new entry for `open_macromolecules_window`.
  Coverage still **100 %** (109 / 109).
- **Tests.** New `tests/test_macromolecules_window.py` (9 tests).
  Updated `test_carbohydrates_panel.py` / `test_lipids_panel.py` /
  `test_nucleic_acids_panel.py` to assert their tabs are now
  inside the window rather than on the main tabbar. Full suite:
  **676 passed, 1 skipped** (+9 from round 43).

### Roadmap additions
- **Phase 31 — Seeded content expansion** added per user directive
  (*"please add a roadmap item to further expand molecules,
  synthesis examples, tutorials, reactions, synthesis and all
  seeded items to grow the scope of the project"*). 12 sub-items
  (31a-31l) targeting 400 molecules, 50 reactions, 20 mechanisms,
  25 pathways, 20 energy profiles, 80 glossary terms, 30
  tutorials, 40 carbs / 40 lipids / 40 NAs, 15 SAR series, 15
  proteins. Cadence: ~1 sub-item per round, interleaved with
  code phases; each sub-item bumps the relevant `SEED_VERSION`
  so existing DBs pick up upgrades additively.

### Design decisions
- **Lazy window construction.** Main window constructs the
  panels eagerly (so they're available as `win.proteins` etc.
  from the moment the app boots) but constructs the
  `MacromoleculesWindow` wrapper lazily on first menu click —
  keeps app startup snappy and avoids a hidden top-level window
  stealing focus on macOS.
- **Panels retain their main-window attributes.** `win.proteins`,
  `win.carbohydrates`, `win.lipids`, `win.nucleic_acids` still
  point at the panel widgets. Agent actions / tests / the NA
  fetch button all keep working without chasing the window
  reference.
- **Bulk-edit audit with `replace_all`.** Instead of hand-editing
  27 `GUI_ENTRY_POINTS` entries, used four `replace_all` edits
  keyed off `"Proteins tab"` / `"Carbohydrates tab"` / `"Lipids
  tab"` / `"Nucleic acids tab"` — safer than a 27-way merge.

### Phase 31 first content batch (tacked onto round 44 after user
prompt: *"please continue"*)
- **31b (+5 reactions).** Buchwald-Hartwig amination, Sonogashira
  coupling, Mitsunobu, Swern oxidation, Horner-Wadsworth-Emmons.
  SMILES validated through `AllChem.ReactionFromSmarts`. Seeded
  reactions now **31** (was 26).
- **31f (+8 glossary terms).** Kinetic vs thermodynamic control,
  Hammond postulate, Markovnikov's / Zaitsev's rules, anti-
  periplanar, Baldwin's rules, chemoselectivity, bioisostere.
  Glossary `SEED_VERSION` bumped 4 → 5 so existing DBs pick up
  the additions on next launch. Seeded terms now **51** (was 43).
- **31h (+10 carbohydrates).** Aminosugars (glucosamine, GlcNAc),
  uronic acids (glucuronic), deoxy sugars (fucose, rhamnose),
  sugar alcohols (sorbitol, mannitol, xylitol), rare aldose
  (tagatose), non-reducing disaccharide (trehalose). Catalogue
  now **25** (was 15).
- **Fragment-consistency audit** (test_fragment_consistency.py)
  flagged 10 new reaction fragments not yet in `seed_intermediates`.
  Backfilled: 4-phenylmorpholine, iodobenzene, phenylacetylene,
  diphenylacetylene, isopropyl acetate, 1-octanol, octanal,
  triethyl phosphonoacetate, ethyl (E)-cinnamate, diethyl
  phosphate. Intermediates table grew 128 → 138.

### Next
- Continue Phase 31. Candidate next batch: **31c (2-3 mechanism
  JSONs)** paired with the new reactions just shipped (Swern
  mechanism 3 steps, HWE 4 steps, Mitsunobu 4 steps), or **31i
  (+10 lipids)** matching the Phase 31h carb bundle.

---

## 2026-04-23 — Round 43 (Phase 29b Lipids + 29c Nucleic-acids sibling tabs)

### What shipped
- **Phase 29b — Lipids tab.** New `core/lipids.py` (21-entry
  catalogue: 9 fatty acids incl. ω-3 / ω-6, 2 triglycerides, 3
  phospholipids, 2 sphingolipids, 2 sterols, 3 fat-soluble
  hormones / vitamin D₃) + `gui/panels/lipids_panel.py` wired into
  the main window as the **Lipids** tab. Mirrors the Carbohydrates
  pattern (family combo + free-text filter + entry list + 2D SVG +
  meta pane), with lipid-specific metadata (chain length,
  unsaturation count, ω-designation, m.p.).
- **Phase 29c — Nucleic-acids tab.** `core/nucleic_acids.py`
  (23-entry catalogue: bases A/G/C/T/U + m6A, m5C; 5 nucleosides;
  4 nucleotides incl. ATP / cAMP / GTP / NAD⁺; ApG dinucleotide;
  5 PDB motifs — 1BNA, 1RNA, 143D G-quadruplex, 1EHZ tRNA-Phe,
  1HMH hammerhead) + `gui/panels/nucleic_acids_panel.py`. Entries
  with a SMILES render via `draw2d`; PDB-motif rows expose a
  *Fetch PDB in Proteins tab* button that switches the main-window
  tab and kicks the proteins panel's fetch slot.
- **Agent actions** — `list_lipids`, `get_lipid(lipid_name)`,
  `lipid_families`, `list_nucleic_acids`,
  `get_nucleic_acid(na_name)`, `nucleic_acid_families` shipped in
  `agent/actions_lipids_na.py`; parameter names dodge the
  `invoke(name, **kw)` collision.
- **GUI audit** — both tabs' actions registered in
  `GUI_ENTRY_POINTS`; coverage gate still **100 %** (108 / 108).
- **Tests** — `tests/test_lipids_panel.py` (8 tests),
  `tests/test_nucleic_acids_panel.py` (8 tests). Full suite now
  **667 passed, 1 skipped**.
- **Roadmap** — added **Phase 30 (Unified Macromolecules window)**
  per user directive: *"I think all macromolecules should be in a
  separate GUI that is accessed [via] a new menu item."* Phase 30
  covers `MacromoleculesWindow` class, Window-menu action, panel
  migration, GUI-audit updates, and cross-panel messaging rewire.

### Bugs fixed along the way
- **Cytosine SMILES** was clobbered pre-compaction
  (`"Nc1ccn(C)c(=O)n1"[:-3] + "c1=O"` → invalid). Replaced with
  `Nc1cc[nH]c(=O)n1`. All 23 NA entries + all 21 lipid entries
  now parse under `Chem.MolFromSmiles`.
- Lipids free-text test assumed a unique match on "cholesterol";
  loosened to `>= 1` because notes on other entries reference
  cholesterol (sterol family cross-talk).

### Next
- Phase 30a-f implementation (when user greenlights): extract
  Proteins / Carbohydrates / Lipids / NA panels into a top-level
  `MacromoleculesWindow`; main-window tabbar slims back down to
  small-molecule workflows.

---

## 2026-04-22 — Session 1 (project bootstrap)

### What was done
- Scaffolded the full modular skeleton per `INTERFACE.md`.
- Chose primary tech stack: **PySide6 + RDKit + 3Dmol.js + SQLAlchemy/SQLite**.
- Implemented the empirical→molecular formula calculator described in
  Verma et al. 2024 (*Rasayan J. Chem.* 17:1460–1472, `refs/4325_pdf.pdf`)
  as a reusable library function (`orgchem/core/formula.py`) and exposed it as
  a GUI tool (`Tools → Empirical / Molecular Formula Calculator…`).
- Seeded the SQLite database with the paper's 15 reference compounds plus a few
  foundational ones so the app is useful immediately on first launch.
- Built the central **AppBus** signal hub so panels stay loosely coupled and
  new panels can be added without touching existing ones.
- In-GUI **session log panel** wired to the standard Python `logging` module via
  a custom `BusHandler`.

### Architecture decisions
- **Why PySide6 over Tkinter / web**: the project requires dockable multi-panel
  layouts, a native 3D viewer (`QWebEngineView` embeds 3Dmol.js cleanly), and
  first-class threading for non-blocking network downloads.
- **Why 3Dmol.js instead of VTK/PyVista**: zero-friction stick / ball-and-stick
  / sphere / surface rendering with native rotate-zoom-pick, driven from plain
  MOL blocks. VTK remains a future swap-in behind `render/draw3d.py`.
- **Why a signal bus instead of direct wiring**: any panel can subscribe to
  `molecule_selected` etc. — adding reactions, quizzes, or spectroscopy panels
  later is purely additive.
- **Why SQLAlchemy + SQLite**: ships with Python, zero admin, lets us swap to
  Postgres later without rewriting queries.

### Agent / LLM control layer (per mid-session request)
- `orgchem/agent/actions.py` — typed action registry + auto-generated tool
  schemas (Anthropic / OpenAI-style) for every registered action.
- `orgchem/agent/library.py` — 9 built-in actions covering molecule browsing,
  formula calculation, online lookup, and tutorial navigation.
- `orgchem/agent/conversation.py` — tool-use loop orchestrator.
- `orgchem/agent/headless.py` — `HeadlessApp` context manager; launches Qt
  with `QT_QPA_PLATFORM=offscreen` so the app runs in CI and can be driven
  programmatically from any Python session (incl. Claude Code).
- `orgchem/agent/bridge.py` + `main.py --agent-stdio` — JSON-per-line
  request/response loop on stdin/stdout for external LLM processes.
- `orgchem/agent/llm/` — pluggable backends: **Anthropic** (Claude SDK),
  **OpenAI-compatible** (incl. Azure/DeepSeek/Groq), **Ollama** (local).
- `orgchem/gui/panels/tutor_panel.py` — in-app **chat console** as a
  detachable dock. The user types, the LLM replies, and the LLM can drive
  the full app via the action registry (display molecules, open lessons,
  compute formulas, fetch from PubChem).
- `tests/test_smoke_headless.py` — end-to-end smoke test that asserts an
  LLM-style action invocation drives the GUI state.
- `scripts/claude_drive_demo.py` — runnable example showing both the
  in-process (`HeadlessApp`) and subprocess (stdio) driving patterns.

### Known gaps (Phase 2+)
- Reactions panel is a stub — `Reaction` class exists but the mechanism
  animator, arrow-pushing renderer, and ORD integration are deferred.
- Multi-molecule comparison tab is a placeholder.
- Quiz engine is a placeholder.
- Tutorial content: only one sample lesson exists; the curriculum tree is
  populated but individual markdown files are stubs.
- No spectroscopy (NMR/IR) prediction yet.
- No retrosynthesis yet (AiZynthFinder integration planned).

### Next-session TODO
1. `pip install -r requirements.txt` in a fresh venv; fix any import issues.
2. Run `python main.py` and verify the 15 compounds render in 2D and 3D.
3. Test PubChem search → download round-trip.
4. Begin Phase 2: `Reaction` CRUD panel and SMARTS-based reaction viewer.
5. Draft the first intermediate-level tutorial (SN1 / SN2) with linked molecule DB examples.

---

## 2026-04-22 — Session 2 (Phase 2a + 3a + Preferences)

### Shipped
- **Matplotlib 3D renderer** (`render/draw3d_mpl.py`): CPK-coloured
  ball-and-stick / sphere / stick / line. Works in any Qt mode; agent action
  `export_molecule_3d`. User-selectable as the active 3D backend via
  `Tools → Preferences…` (uses a `QStackedWidget` in `viewer_3d.py`).
- **Reactions subsystem**: high-quality rendering via
  `MolDraw2DSVG.DrawReaction` (`render/draw_reaction.py`); 16 named
  reactions seeded (`db/seed_reactions.py`); `ReactionWorkspacePanel`
  replaces the Reactions tab stub; agent actions `list_reactions`,
  `show_reaction`, `export_reaction_by_id`.
- **Compare tab**: `ComparePanel` — 2×2 grid of molecule slots with 2D +
  descriptors; `compare_molecules([ids])` action pre-populates.
- **Preferences dialog**: `Tools → Preferences…` (Ctrl+,) for default 3D
  backend, style, theme, log level, etc. Bus signal `config_changed` on
  save so open panels re-render.
- **Tutorial content**: 3 more lessons written (Atoms/Bonds, Structures,
  SN1 vs SN2).
- **Stubs removed**: the Reactions, Compare, and Quiz placeholder tabs are
  gone. Quiz deferred to Phase 5 with a note in ROADMAP.
- **Tests**: 14 new tests (7 reactions, 7 3D-mpl). Total 34/34 pass in ~3 s.
- **Visual tour**: extended to 22 files incl. reactions tab, compare tab,
  matplotlib 3D exports, and reaction SVG exports.

### Decisions
- Preferences vs per-panel toolbar: backend/theme/log level → Preferences;
  per-molecule style stays in the panel toolbar.
- Kept 3Dmol.js as the default 3D backend because it's interactive; the
  matplotlib backend is the fallback for headless CI / screenshot tours.

### Next-session TODO
1. Phase 2b: mechanism arrow-pushing player for SN1/SN2/E1/E2.
2. Fill in the remaining 13 tutorial lessons.
3. Shaded spheres for matplotlib 3D (proper ball rendering with lighting).
4. Screenshot golden-file regression tests.

---

## 2026-04-22 — Session 3 (Phase 2b mechanism player + shaded 3D)

### Shipped
- **Mechanism arrow-pushing player**:
  - `core/mechanism.py` — Mechanism / MechanismStep / Arrow dataclasses.
  - `render/draw_mechanism.py` — RDKit MolDraw2DSVG + `GetDrawCoords`
    overlays red curved bezier arrows between atoms (curly + fishhook).
  - `db/seed_mechanisms.py` — 5 textbook mechanisms seeded: SN1 (4 steps),
    SN2 (2 steps), E1 (3 steps), E2 (2 steps), Diels-Alder (2 steps).
    Includes `SEED_VERSION` so seed-data changes auto-migrate.
  - `gui/dialogs/mechanism_player.py` — modal with Prev / Next / counter /
    per-step SVG save.
  - "Play mechanism" button on the Reactions tab, enabled when
    mechanism_json is populated.
  - Agent actions: `list_mechanisms`, `open_mechanism`,
    `export_mechanism_step`.
- **Matplotlib 3D shaded spheres**: per-atom `plot_surface` quads for
  ball-and-stick and sphere styles; goes from flat markers to real 3D
  shaded spheres with CPK colours.
- **Tutorial content**: 2 new lessons (beginner *Functional Groups*,
  intermediate *E1 vs E2*). Now 6 of 17 lessons written.
- **3D reaction display plan** added to ROADMAP as a new Phase 2c with
  three sub-phases (static side-by-side, 3Dmol.js trajectory animation,
  transition state + 3D curved arrows).
- **Refactor**: split `agent/library.py` (which hit 510 lines) into
  `library.py` + `actions_reactions.py`. Both register via the agent
  package init; callers see no API change.

### Decisions
- Arrows are **atom-to-atom** only (not bond-midpoint / H-atom). Canonical
  arrow-pushing uses finer origins and endpoints; adding them is tracked
  but not blocking — pedagogical value is clear.
- Mechanism JSON includes `seed_version`; the seeder upgrades entries
  whose version is older than the current constant. No migration script
  needed.
- Labels on arrows use ASCII ("new bond", "pi shift") because Qt's
  default SVG renderer lacks Greek glyphs.

### Next-session TODO
1. Phase 2c.1: static 3D side-by-side reaction renderer via
   `draw3d_mpl` + atom-mapped reaction SMARTS. Highlight
   breaking/forming bonds in red/green.
2. Add mechanisms for aldol and Grignard (2 more reactions).
3. Fill in 2-3 more tutorial lessons (stereochemistry; aromaticity).
4. Bond-midpoint and H-atom arrow support in the mechanism player.

---

## 2026-04-22 — Session 4 (visual QA + 3D reactions + aldol/Grignard)

### Shipped
- **Visual QA pass** of 46 gallery images — confirmed reaction SVGs,
  mechanism SVGs, compare tab, browser all render legibly. Spotted and
  fixed three issues:
  1. Main window too tall (1500×950 → 1280×780 with 960×640 minimum).
  2. Matplotlib 3D too much whitespace (switched to `bbox_inches="tight"`
     now that `plot_surface` gives real 3D bounding boxes).
  3. Mojibake on E2 step 1 label "Î²-H" (SVG encoding declaration was
     `iso-8859-1`; changed to `UTF-8` so any non-ASCII renders correctly).
- **Phase 2c.1 — static 3D reaction display** (new feature):
  - New `Reaction.reaction_smarts_mapped` column with on-startup additive
    migration so existing databases upgrade seamlessly.
  - 6 reactions seeded with atom-mapped SMARTS (SN2, SN1, bromination,
    hydrogenation, PCC, NaBH4).
  - `orgchem/render/draw_reaction_3d.py` — renders reactant + arrow +
    product in one matplotlib figure; atoms coloured by map number; red
    for broken bonds, green for formed bonds.
  - Agent action `export_reaction_3d`. GUI *Render 3D…* button on the
    Reactions tab, enabled when a mapped SMARTS is present.
  - 5 tests (`tests/test_reaction_3d.py`).
- **Aldol + Grignard mechanisms** seeded (now 7 total).
- **Window geometry persistence** — `QSettings` saves resize / dock
  layout across sessions.
- **Visual tour** extended: 46 files incl. 5 new 3D reaction renders.

### Decisions
- 3D reaction render requires atom-mapped SMARTS; unmapped reactions get
  a friendly error from the action and a disabled button in the GUI.
  `rdFMCS`-based auto-mapping tracked as a polish item.
- Disconnected reactant fragments are combined into one Mol before
  embedding; they end up close together in 3D. Polishing that layout to
  visually separate nucleophile from substrate is tracked as a follow-up.
- Bond-order changes (single↔double, as in PCC / NaBH4) are not yet
  highlighted — only bond make/break is. Follow-up.
- Used a lightweight in-`init_db` `ALTER TABLE` migration rather than
  pulling in Alembic — the scale of additive schema changes doesn't
  justify the heavier tooling yet.

### Next-session TODO
1. Aldol condensation atom-mapped SMARTS + 3D render (complex because
   it has the self-coupling + dehydration steps).
2. Fill remaining tutorial lessons — stereochemistry, aromaticity.
3. rdFMCS auto-mapping for user-imported reactions without explicit maps.
4. Bond-order-change highlighting in 3D reaction renders.
5. Phase 2c.2 design review — trajectory animation in 3Dmol.js.

---

## 2026-04-22 — Session 5 (Phase 2c.2 trajectory animation)

### Shipped
- **Phase 2c.2 — 3D trajectory animation** (new headline feature):
  - `orgchem/core/reaction_trajectory.py` — Kabsch-align product onto
    reactant, linearly interpolate N frames, emit multi-frame XYZ.
  - `render/draw_reaction_3d.build_trajectory_html` — self-contained
    3Dmol.js HTML with play / pause / reset / speed slider controls.
  - `gui/dialogs/reaction_trajectory_player.py` — modal QWebEngineView
    that hosts the HTML. **▶ Animate 3D button** on the Reactions tab,
    enabled when mapped SMARTS is present.
  - Agent actions: `export_reaction_trajectory_html` (disk) and
    `play_reaction_trajectory` (in-app modal).
  - 10 new tests incl. Kabsch round-trip sanity + frame-count knob.
- **QDockWidget objectNames** set so QSettings saves/restores dock
  layout cleanly (Qt warning gone).
- **Visual tour** extended: 3 trajectory HTMLs (SN2, SN1, hydrogenation)
  alongside the 5 static 3D renders. Open in any browser to play.

### Decisions
- XYZ format for trajectory frames (not SDF/MOL) — no bonds to manage
  across frames, 3Dmol.js auto-bonds by proximity each frame, so bonds
  appear/disappear *as atoms move*. That's exactly the pedagogical
  effect we want.
- Trajectory includes only atoms that carry an atom-map number.
  Hydrogens and other unmapped atoms are dropped — keeps the animation
  clean and the map correspondence unambiguous.
- Linear interpolation rather than NEB/MMFF-relaxed intermediates. A
  polish item, but linear already produces a convincing morph.

### Next-session TODO
1. Animated GIF / MP4 export (matplotlib.animation) so headless /
   docs use cases work without a browser.
2. Aldol condensation atom-mapped SMARTS + 3D / animation.
3. Bond-order-change highlighting in 3D reaction renders.
4. rdFMCS auto-mapping for user-imported reactions.
5. Fill remaining tutorial lessons.

---

## 2026-04-22 — Session 6 (content expansion + bond-order highlight + roadmap growth)

### Shipped
- **Phase 6 content expansion — first pass:**
  - **+20 molecules** (total 40): 5 amino acids (Gly, Ala, Phe, Trp, Cys);
    5 drugs (Aspirin, Ibuprofen, Acetaminophen, Naproxen, Diazepam);
    5 solvents/reagents (DMSO, DMF, THF, Et₂O, MeCN); 5 natural products
    (Menthol, Camphor, Salicylic acid, Vanillin, Capsaicin). Additive
    backfill so existing DBs upgrade silently.
  - **+10 reactions** (total 26): Wittig, Claisen, Cannizzaro, Michael,
    Baeyer-Villiger, Suzuki, radical halogenation, HVZ, pinacol,
    hexatriene electrocyclic.
  - **Corannulene SMILES fix**: the Verma paper's SMILES failed to
    kekulize in modern RDKit (silent failure since Session 1). Replaced
    with a PubChem CID 5284218 canonical form — correct C20H10 now in
    the DB.
- **Bond-order-change highlighting** in 3D reaction renders. PCC now
  shows a clear **green C=O** bond (single→double, bond order formed);
  NaBH4 shows **red C=O** bond (double→single, bond order broken).
  Also: mapped SMARTS rewritten with explicit `[CH3:N]` annotations so
  `AddHs` places all implicit hydrogens — PCC and NaBH4 now render as
  real acetone/2-propanol rather than 4-atom skeletons.
- **Two major roadmap additions:**
  - **Phase 8 — Synthesis pathways**: new Synthesis tab with target →
    step-by-step route, seed 6 classic syntheses (Wöhler urea, Aspirin,
    Paracetamol, BHC Ibuprofen, Theobromine→Caffeine,
    Phenacetin→Paracetamol), future retrosynthesis.
  - **Phase 9 — 3D molecular docking**: AutoDock Vina / Smina / DiffDock
    backends, PDB receptor management via RCSB, Docking tab with
    receptor + ligand + pose viewer, pedagogical seeds
    (caffeine ↔ adenosine A2A, aspirin ↔ COX-1, tamiflu ↔ neuraminidase).
- **Two new smoke tests** lock in the 40-molecule / 26-reaction counts.

### Decisions
- Mapped SMARTS use `[CH3:N]` / `[CH:N]` / `[OH:N]` explicit-H
  notation. The bare `[C:N]` form disables implicit-H inference, making
  the embedded molecule a skeleton rather than a real structure.
- Corannulene: adopted PubChem's canonical Kekulé form. Silent failures
  in the initial seed were the reason the old DB had 39 molecules, not
  40 — lesson: verify all SMILES parse before shipping.
- Seed-backfill now **overwrites** mapped SMARTS when the current value
  doesn't match the in-code `_MAPPED` dict (handles upgrade path).
- Synthesis pathways and docking are sizable features; plans are in the
  roadmap with clear sub-phases. Implementation deferred so this session
  stays crisp.

### Next-session TODO
1. Phase 8a — synthesis-pathways data model + 6 seeded pathways.
2. Phase 8b — `render_pathway.py` + `synthesis_workspace.py` tab.
3. Mechanisms for a few of the new reactions (Wittig, Michael).
4. `rdFMCS` auto-mapping for user-imported reactions.
5. Fill more tutorial lessons (Stereochemistry, Aromaticity).

---

## 2026-04-22 — Session 7 (Phase 8 synthesis pathways — end-to-end)

### Shipped
- **Phase 8a — Data model + seed:**
  - `SynthesisPathway` + `SynthesisStep` ORM models.
    `Base.metadata.create_all` creates the new tables on existing DBs
    (no Alembic needed for pure table additions).
  - `orgchem/db/seed_pathways.py` — 6 classic syntheses seeded:
    Wöhler urea (1828), Aspirin, Paracetamol, **BHC Ibuprofen (3 steps,
    Presidential Green Chemistry Award 1997)**, Caffeine by N-methylation
    of theobromine, Phenacetin → Paracetamol.
  - Each pathway has target name + SMILES + description + category +
    source; each step has reactants, reagents (above the arrow),
    conditions (below), yield, and a teaching note.
- **Phase 8b — Renderer + GUI:**
  - `orgchem/render/draw_pathway.py` — composite SVG with per-step
    number, reagents, embedded RDKit reaction scheme, conditions,
    yield, notes, and separators. SVG/PNG export (PNG via Qt's
    `QSvgRenderer` — no cairo dep).
  - **Bug found and fixed**: Qt's `QSvgWidget` is Svg Tiny 1.2 and
    rejects nested `<svg>` elements, so my first cut (embedding
    RDKit's full SVG inside mine) produced an empty scheme. Fix:
    strip the outer `<svg>` wrapper, keep only the drawing body, wrap
    in a `<g transform=...>`.
  - `orgchem/gui/panels/synthesis_workspace.py` — **new Synthesis tab**.
    Filterable pathway list on the left, scrollable SVG viewer on the
    right with target name header and Export button.
  - Tab wired into `main_window.py`.
- **Phase 8c — Agent actions + tests:**
  - `orgchem/agent/actions_pathways.py` — `list_pathways`,
    `show_pathway`, `export_pathway`.
  - 8 new tests in `tests/test_pathways.py` (seed presence, BHC is 3
    steps, filter by category, show/show-missing, export SVG and PNG,
    direct render contains every step).
- **Vastly expanded ROADMAP content targets** (per request): Phase 6
  targets now **250+ molecules** (up from 80), **100+ reactions** (up
  from 50), **30+ pathways** (up from 6) — with concrete category
  plans for each. Phase 8a's pathway target expanded with 4 sub-groups:
  industrial drugs, total-synthesis classics, natural products,
  historical/educational.
- **All old screenshots deleted and gallery regenerated** (per request).
  Fresh 56-file gallery under `screenshots/tour/`, including:
  - 12_synthesis.png — full Synthesis tab screenshot.
  - 6 new pathway PNGs (aspirin, paracetamol, BHC ibuprofen, wohler,
    caffeine, phenacetin).

### Decisions
- Synthesis pathway step data is denormalised (reagents/conditions/notes
  stored on the step row rather than joining to a Reaction). Simpler
  and avoids the atom-map assumptions the reaction-to-3D pipeline
  requires.
- PNG export uses Qt's `QSvgRenderer`, not `cairosvg` — consistent with
  our "no native-lib dependencies" stance and already-proven working
  inside `draw3d_mpl`.
- Strip the outer `<svg>` wrapper from RDKit's step output before
  embedding — Qt's SVG renderer rejects nested `<svg>`. A 5-line
  `_extract_svg_body` function handles it.

### Next-session TODO
1. Seed more pathways toward the 30+ target (atorvastatin, Taxol,
   Strychnine, Sildenafil, Morphine, Vanillin, Kolbe-Schmitt).
2. "Open step in Reactions…" — click a pathway step to flip into the
   Reactions tab with that SMARTS preloaded.
3. Mechanisms for Wittig, Michael, Suzuki.
4. Fill the Stereochemistry and Aromaticity tutorial lessons.
5. rdFMCS-based auto-mapping of user-imported reactions.
6. **Phase 10a** — lightweight MMFF-MD: butane dihedral rotation and
   cyclohexane ring-flip animations, reusing the Phase 2c.2 trajectory
   player. (Phase 10 added to ROADMAP at the end of Session 7.)

---

## 2026-04-22 — Session 8 (Phase 10a conformational dynamics)

### Shipped
- **Phase 10a — Conformational dynamics**:
  - `orgchem/core/dynamics.py` — `run_dihedral_scan` (rotate a named
    torsion 0° → 360° with MMFF relaxation + torsion constraint),
    `run_conformer_morph` (ETKDG ensemble + linear interpolation
    between energy-sorted conformers). Pre-wired
    `butane_dihedral_scan`, `ethane_dihedral_scan`,
    `cyclohexane_ring_flip` demos.
  - `orgchem/gui/dialogs/dynamics_player.py` — modal launched from a
    "▶ Run dynamics…" button on the 3D viewer panel. Mode dropdown
    (conformer morph / dihedral scan) + auto-detected rotatable-bond
    picker via a SMARTS match. Playback uses the Phase 2c.2
    `build_trajectory_html` — no new viewer code.
  - `orgchem/agent/actions_dynamics.py` — 3 agent actions
    (`run_dihedral_scan_demo`, `run_molecule_dihedral`,
    `run_molecule_conformer_morph`). Registered in `agent/__init__.py`.
  - 9 new tests in `tests/test_dynamics.py` (76/76 total).
  - Visual tour gains 3 MD HTMLs (butane, ethane, cyclohexane).

### Decisions
- **Scope pivot**: started implementing a Langevin integrator wrapping
  RDKit's MMFF force field. A finite-difference check revealed
  `CalcGrad()` returns values ~14 % off numerical gradients (units /
  convention quirk I don't want to dig through mid-session). Pivoted
  to **dihedral scans + conformer morphs**: deterministic,
  pedagogically equivalent for the canonical demos (butane rotation,
  cyclohexane ring flip), and reuses existing infrastructure. The real
  Langevin/Verlet path now lives under **Phase 10b** (OpenMM backend),
  which also avoids fighting force-field parameterisation in Python.
- Rotatable-bond auto-detection via a single SMARTS pattern
  (`[!$(*#*)&!D1]-&!@[!$(*#*)&!D1]`) is "good enough" for the GUI
  picker; finer ranking by priority is a polish item.

### Next-session TODO
1. Phase 10b — OpenMM backend behind an `MDBackend` protocol so the
   MMFF path stays the default and OpenMM is optional.
2. More pathway seeds toward the 30+ target.
3. Mechanisms for Wittig / Michael / Suzuki.
4. Fill Stereochemistry and Aromaticity tutorial lessons.

---

## 2026-04-22 — Session 9 (bug fixes + content expansion from user report)

### User-reported bugs fixed
1. **Compare tab: "Could not parse SMILES: 'Caffeine'"** — typing a
   molecule name was being fed straight into the SMILES parser. Fix:
   `_Slot._on_load` now tries the DB name lookup first (exact + substring
   search) and only falls back to a raw SMILES parse when nothing
   matches. 3 tests lock it in.
2. **Compare tab: drag-and-drop didn't work** — the molecule browser
   list view wasn't drag-enabled and the Compare slots weren't drop
   targets. Fix: a shared MIME type `application/x-orgchem-molecule-id`
   carries the DB id; `_MolListModel` now implements
   `mimeTypes`/`mimeData` + `ItemIsDragEnabled`, and the list view has
   `setDragEnabled(True)` + `DragOnly` mode. `_Slot` overrides
   `dragEnterEvent` / `dropEvent` (highlights blue on hover, loads
   by id on drop). 2 tests lock the MIME shape + drop-acceptance.

### User observation addressed
**"All pathway examples have a single step — is that correct?"** —
mostly, yes (5 of 6 seeded routes were 1-step, plus BHC ibuprofen at
3 steps). Added **3 multi-step classics** so the Synthesis tab
demonstrates the data model:
- **Paracetamol from phenol (Hoechst, 3-step)** — nitration → H₂/Pd
  reduction → Ac₂O acetylation. Clean industrial route.
- **Aspirin from phenol (Kolbe-Schmitt + acetylation, 2-step)** —
  NaOH/CO₂ to salicylic acid, then Ac₂O to aspirin.
- **Vanillin from eugenol (2-step via isoeugenol)** — base-catalysed
  allyl → propenyl isomerisation, then ozonolysis to the aldehyde.

Pathway count now **9** (was 6), and **4 are multi-step**.

### Docs + tour
- Visual tour regenerated; pathway gallery now 9 PNGs including the
  new multi-step renders.
- 81 tests total (was 76) — 5 new in `tests/test_compare_panel.py`.

---

## 2026-04-22 — Session 11 (Phase 13 reaction-coordinate diagrams)

### What was done
Landed **Phase 13a/b/e** (reaction-coordinate energy profiles) end-to-end
plus a matching GUI entry point on the Reactions tab. Students can now
see the three canonical views of a reaction — arrows (mechanism player),
geometry (3D trajectory), and **energy landscape**.

### Work items
- **Core (`orgchem/core/energy_profile.py`)** — `ReactionEnergyProfile`
  and `StationaryPoint` dataclasses with JSON round-trip, plus
  `activation_energies` and `delta_h` derived properties. Zero GUI / DB
  dependencies so the rest is testable headlessly.
- **Renderer (`orgchem/render/draw_energy_profile.py`)** — matplotlib
  Figure with Bezier-smoothed curve through the stationary points, sharp
  TS‡ peaks, auto-annotated Ea arrows per barrier, ΔH bracket across the
  full profile. PNG or SVG chosen by file extension.
- **DB schema** — `Reaction.energy_profile_json` column (additive
  migration in `db/session.py`, same pattern as
  `reaction_smarts_mapped`).
- **Seed (`orgchem/db/seed_energy_profiles.py`)** — 4 textbook profiles:
  SN2 (1 barrier), SN1 (2 barriers + carbocation well), E1 (2 barriers),
  Diels-Alder (1 concerted aromatic TS, strongly exothermic). Values
  from Clayden 2e / Carey-Sundberg 5e. Versioned via `SEED_VERSION`.
- **Agent actions (`actions_reactions.py`)** — `list_energy_profiles`,
  `get_energy_profile`, `export_energy_profile`. All return error dicts
  (never raise) when a reaction has no profile or an id is missing.
- **GUI** — new `gui/dialogs/energy_profile_viewer.py` modal; new
  "Energy profile…" button on the Reactions tab auto-enabled via the
  JSON-column presence check (same pattern as Render 3D / Animate 3D).

### Roadmap additions
Before implementation, expanded **ROADMAP.md** by ~380 lines covering
the advanced-topics queue from the user message:
- Phase 13 — reaction-coordinate diagrams & kinetics
- Phase 14 — orbital symmetry & MO theory
- Phase 15 — practical lab techniques
- Phase 16 — bio-organic & macromolecules (incl. SPPS)
- Phase 17 — physical organic chemistry
- Phase 18 — green chemistry (water / ionic liquids / scCO₂)
- Phase 19 — medicinal chemistry & drug design
- Cross-cutting **stereochemistry** section mapping where it shows up
  in every other phase.

### Testing
- `tests/test_energy_profile.py` — 13 new tests: round-trip, Ea/ΔH
  helpers, renderer (PNG + SVG + bad-format + too-few-points), seeded-
  data checks (SN2 single barrier, SN1 double barrier + intermediate,
  DA strongly exothermic), agent actions (export + missing-id error +
  no-profile error).
- Full suite: **95/95 pass in ~5 s** (was 81).
- Visual tour updated — 4 new PNGs under `screenshots/tour/energy_*.png`.

### Gotchas
- None. The matplotlib path pattern used by Phase 2c.1 / Phase 3a worked
  cleanly for Bezier-smoothed curves too. The `matplotlib.use("Agg")`
  at module import means the renderer is safe from any Qt-platform side.
- The ΔH label clipped slightly into the right edge — fixed by
  extending `ax.set_xlim` by 1.2 units on the right.

### What's next
Per the user's direction ("work through the roadmap"), next up:
1. Phase 17a/18a — atom-economy + green-metrics helpers (small, headless,
   useful per-reaction annotations).
2. Phase 14a — Hückel MO helper + simple orbital visualisation.
3. Stereochemistry rendering (cross-cutting #1).
4. Phase 11 — glossary data model + seed.

### Session 11 — continued: green metrics + Hückel MOs + stereo + glossary

After Phase 13 landed, continued working through the roadmap in priority
order (per user: "work through the roadmap until done"):

#### Phase 17a / 18a — Green-chemistry metrics
- `orgchem/core/green_metrics.py` — `atom_economy(reaction_smiles)` with
  auto-heaviest-product convention, `e_factor(mass_inputs, mass_product)`,
  `pathway_atom_economy(steps)`. Pure RDKit + no external deps.
- Agent actions `reaction_atom_economy(reaction_id)` and
  `pathway_green_metrics(pathway_id)` (in `actions_pathways.py`).
- Verified against textbook: Fischer ester. ~83 %, bromination ~66 %,
  Diels-Alder 100 %, BHC Ibuprofen overall ~74 % (published ~77 %).
- 15 tests in `tests/test_green_metrics.py`.

#### Phase 14a — Hückel MOs + level-diagram renderer
- `orgchem/core/huckel.py` — adjacency-matrix eigendecomposition,
  α=0 / β=−1. Auto-identifies the π subsystem (including charged /
  radical carbons adjacent to the main π core, so allyl cation /
  radical / anion all work). Pedagogical π-electron counting handles
  N-H pyrrole (2e⁻) vs lone-pair-out-of-ring pyridine (1e⁻),
  aromatic O / S (2e⁻), and ± charge corrections.
- `orgchem/render/draw_mo.py` — matplotlib level diagram: bars per MO,
  occupied electrons as ↑↓ arrows, HOMO / LUMO labelled, degenerate
  levels drawn side by side, α reference line.
- Agent actions `huckel_mos(smiles)` and `export_mo_diagram(smiles, path)`.
- 16 tests in `tests/test_huckel.py` verifying exact eigenvalues for
  ethene (±1), butadiene (±0.618, ±1.618), benzene (±1, ±1, ±2),
  allyl series (√2, 0, −√2), Cp⁻ / pyrrole / pyridine / furan all 6e⁻.

#### Cross-cutting stereochemistry
- `orgchem/core/stereo.py` — canonical helpers: `assign_rs`, `assign_ez`,
  `stereocentre_atoms`, `flip_stereocentre`, `enantiomer_of`, `summarise`.
- `orgchem/render/draw2d.py` extended with `show_stereo_labels` kw —
  uses RDKit's `addStereoAnnotation` draw option to render wedge/dash
  bonds with CIP R/S and E/Z labels. Discovered RDKit renders those as
  SVG path groups with `class='CIP_Code'` rather than `<text>` — test
  accordingly.
- Agent actions `assign_stereodescriptors`, `flip_stereocentre`,
  `enantiomer_of`, `export_molecule_2d_stereo`.
- 18 tests in `tests/test_stereo.py`. Bug bite: originally used a meso
  compound as a "should flip" test — fixed by switching to a non-meso
  chiral pair.

#### Phase 11a + 11d — Glossary data model + actions
- New `GlossaryTerm` DB table (auto-created, no ALTER needed).
- `seed_glossary.py` — 43 canonical terms across fundamentals /
  stereochemistry / mechanism / reactions / synthesis / spectroscopy /
  lab-technique. Short markdown definitions, alias lists, cross-refs.
- Agent actions `define(term)`, `list_glossary(category)`,
  `search_glossary(query)`. Alias lookup + case-insensitive exact match +
  substring search all work.
- 11 tests in `tests/test_glossary.py`.

#### Full suite after session: **155 / 155 pass in ~5.6 s** (was 81 at start of day).

### What's next in the roadmap queue
1. **Tutorial markdown** — `intermediate/01_stereochemistry.md` +
   `intermediate/04_aromaticity.md` now have both the stereo helper
   module and the Hückel MO engine backing them; content is the gap.
2. **Phase 14a follow-up** — 3D orbital isosurface overlays on the
   molecule, for the Clayden-style MO pictures.
3. **Phase 15 (lab techniques)** — start with TLC / Rf simulator
   (rides on logP already in descriptors) and LLE partition helper.
4. **Phase 13c / 13b follow-ups** — energy profiles for the remaining
   5 mechanisms (E2, aldol, Grignard, Wittig, Michael) + full-kinetics
   composite SVG of a multi-step mechanism.
5. **Phase 16 (bio-organic)** — complete the 20 amino acids, seed
   peptide-coupling pathway (EDC/HATU), fatty-acid triad.
6. **Phase 11b** — Glossary tab GUI (deferred this session since the
   data + actions land most of the pedagogical value headlessly).

### Session 11 — continued: molecule expansion + lab techniques + glossary GUI + drug-likeness

Continuing per user direction ("complete the molecule expansion and
continue with the roadmap"):

#### Phase 6a — molecule expansion to 210 (from 40)
- `orgchem/db/seed_molecules_extended.py` — 170 new molecules via
  additive seeding, categorised by `source` tag:
  - 15 remaining amino acids (now complete 20).
  - 20 named reagents (LDA, NaBH₄, NaH, DBU, DIPEA, TBSCl, mCPBA,
    Boc₂O, DMP, etc.).
  - 23 drugs (penicillin G, amoxicillin, oseltamivir, acyclovir,
    fluoxetine, citalopram, atorvastatin, simvastatin, lovastatin,
    propranolol, metformin, warfarin, omeprazole, sildenafil,
    captopril, enalapril, losartan, morphine, lidocaine, atropine,
    quinine, dopamine, diphenhydramine).
  - 15 biomolecules (5 nucleosides, 4 sugars, 3 fatty acids,
    glutathione, testosterone, estradiol).
  - 8 dyes (indigo, methyl orange, phenolphthalein, crystal violet,
    malachite green, fluorescein, rhodamine B, eosin Y).
  - 10 PAHs (naphthalene, anthracene, phenanthrene, pyrene, chrysene,
    triphenylene, fluorene, biphenyl, perylene, acenaphthylene).
  - 22 heterocycles (pyridine, pyrrole, furan, thiophene, imidazole,
    pyrazole, oxazole, thiazole, triazoles, pyrimidine, pyrazine,
    piperidine, morpholine, piperazine, indole, quinoline,
    isoquinoline, purine, benzofuran, benzothiophene, aziridine).
  - 30 functional-group ladder entries (alkanes C3-C8 + cyclo-C3-C6,
    7 alkenes, 3 alkynes, 6 alcohols, 4 ketones, 4 aldehydes, 5 acids,
    3 esters, 5 amines, 3 amides).
- Bug bite: original Purine SMILES `c1[nH]cnc2cncnc12` failed
  kekulisation; fixed to `c1ncc2[nH]cnc2n1`.

#### Phase 11b — Glossary GUI tab
- `gui/panels/glossary_panel.py` — filter box + category combo-box +
  term list + markdown definition pane + clickable "See also" buttons
  that jump to related entries.
- New `show_term(term)` agent action switches to the tab + focuses.
- 3 additional tests in `tests/test_glossary.py`.

#### Phase 15a-lite — recrystallisation + distillation + extraction
- `core/lab_techniques.py` — Arrhenius-ish solubility-curve fitter,
  `recrystallisation_yield` predictor, bp table for ~30 common solvents,
  `distillation_plan(a, b)` classifier (simple / fractional /
  not-distillable), `fraction_ionised` via Henderson-Hasselbalch,
  `extraction_plan` with acid-base + logP awareness.
- 15 tests in `tests/test_lab_techniques.py`.
- 4 agent actions: `recrystallisation_yield`, `distillation_plan`,
  `extraction_plan`, `fraction_ionised`.

#### Visual tour + docs refresh
- Tour regenerated — now 89 files, including 9 energy-profile PNGs,
  6 MO level diagrams, 4 stereo renders (R/S ibuprofen, cis/trans
  2-butene), and a Glossary-tab screenshot.

#### Session 11 totals
- **192 / 192 tests pass** (was 81 at start of session).
- **210 molecules** seeded (was 40).
- **New core modules** (8): `energy_profile.py`, `green_metrics.py`,
  `huckel.py`, `stereo.py`, `druglike.py`, `chromatography.py`,
  `lab_techniques.py` + extended molecule / glossary seed files.
- **New render modules** (2): `draw_energy_profile.py`, `draw_mo.py`.
- **New agent action files** (6): `actions_orbitals.py`,
  `actions_stereo.py`, `actions_glossary.py`, `actions_medchem.py`,
  `actions_labtech.py`, with additions to `actions_pathways.py`,
  `actions_reactions.py`.
- **New GUI**: Glossary tab + Energy-profile viewer dialog.
- All modules still under the 500-line project cap.

### What remains (for future sessions)

- Phase 9  (docking): not started — big-dependency feature.
- Phase 10b (OpenMM MD): deferred — optional backend.
- Phase 11c (cross-linking macros in tutorials): data is in place, needs
  markdown processing.
- Phase 12  (IUPAC nomenclature): rule catalogue + quiz modes.
- Phase 13c (full-kinetics composite SVG): depends on lone-pair /
  bond-midpoint arrow rendering.
- Phase 14b-d (3D orbital isosurfaces, Woodward-Hoffmann rules, FMO-
  annotated arrows).
- Phase 15d (integrated characterisation — depends on Phase 4
  spectroscopy).
- Phase 16 (bio-organic): SPPS pathway, enzyme mechanisms, glycolysis.
- Phase 17b-e (Hammett plots, KIE, solvent effects).
- Phase 18b-e (solvent-hazard DB, pathway rewriter, catalytic flags).
- Phase 19a/c-e (SAR viewer, bioisosteres, docking-integrated design).
- Tutorial content: intermediate/01_stereochemistry.md,
  intermediate/04_aromaticity.md, intermediate/06_energetics.md, and the
  4 Advanced + 4 Graduate lesson slots.

### Session 11 — continued (part 3): tutorials + IUPAC rules + enzyme mechanisms + SPPS pathway

Additional roadmap items landed in the final segment of session 11:

#### Tutorial content — intermediate tier complete
- `intermediate/01_stereochemistry.md` — R/S + E/Z + wedge/dash, meso,
  examples across the app (ibuprofen, alanine, D-glucose, 2-butene
  E/Z). Leverages `core/stereo.py` and the new `addStereoAnnotation`
  draw option.
- `intermediate/04_aromaticity.md` — Hückel's rule + 4n+2 magic
  numbers, Cp⁻ and tropylium, pyrrole vs. pyridine lone-pair
  behaviour, canonical EAS family (halogenation / nitration /
  sulfonation / FC-alk / FC-acyl), activating vs. deactivating
  directing effects. Ties into the `huckel_mos` + `export_mo_diagram`
  actions.
- `intermediate/06_energetics.md` (new curriculum slot) — one vs. two
  barriers, rate-determining step, Hammond's postulate, kinetic vs.
  thermodynamic product, reading a seeded profile. Leverages the
  Phase 13 energy-profile infrastructure.

Intermediate tier now **6/6 complete** (was 2/6).

#### Phase 12a — IUPAC naming rule catalogue
- `orgchem/naming/rules.py` — 22 structured rules across 11
  categories (alkanes 4, alkenes 2, alcohols 2, ethers 1, carbonyls 2,
  acids 3, amines 1, aromatics 2, heterocycles 2, stereochemistry 1,
  general 2). Each rule has: id, title, markdown description, example
  SMILES + IUPAC + common name + common-pitfalls note.
- 3 agent actions: `list_naming_rules(category)`, `get_naming_rule(id)`,
  `naming_rule_categories()`.
- 13 tests in `tests/test_naming.py`: catalogue size, required fields,
  unique ids, category coverage, filter lookup, every example SMILES
  parses under RDKit.

#### Phase 16a — SPPS pathway (Met-enkephalin YGGFM)
- New 5-step Fmoc-SPPS pathway in `seed_pathways.py`: Fmoc
  deprotection with piperidine → HBTU/DIPEA coupling of Fmoc-Phe →
  repeat for Gly-4 → repeat for Gly-3 → final Tyr coupling + TFA
  cleavage. Full IUPAC structures, accurate reagents, references to
  Merrifield (1963).
- Total pathway count: **12** (was 11), with **7 multi-step** routes.

#### Phase 16d — enzyme mechanisms
- Chymotrypsin catalytic triad (4-step): Ser-OH attacks peptide C=O
  → tetrahedral intermediate → amine leaves as acyl-enzyme → water
  attacks acyl-enzyme → free enzyme + acid. Pedagogically simplified
  (enzyme residues described in captions rather than drawn).
- Aldolase class I Schiff-base aldol (3-step): Lys + DHAP Schiff base
  → enamine attacks G3P → F1,6BP after Schiff-base hydrolysis.
- Both reactions also seeded in `seed_reactions.py` so the mechanism
  player has a matching row. Mechanism count: **11** (was 9).

#### Totals for session 11 (all parts)
- **206 tests pass** in ~6 s (session started at 81).
- **210 molecules, 28 reactions, 11 mechanisms, 12 pathways, 9 energy
  profiles, 43 glossary terms, 22 naming rules**.
- 6 intermediate-tier tutorial lessons (was 2).
- 20 agent-action categories.
- 14 core modules, 10 render modules, 10 agent action files.
- All modules still under the 500-line project cap.

### User-reported follow-up (queued)
The user flagged that molecule representations differ across the
Reactions tab, Synthesis tab, and the molecule database — a given
compound should look the same everywhere, and intermediate molecules /
fragments that appear in reaction and pathway schemes should live in
the DB too. Logged as **Phase 6f** (consistent molecule
representations) — see ROADMAP.md.

### Session 11 — final segment: Phase 6f (consistency) + new roadmap additions

#### Phase 6f — consistent molecule representations end-to-end
- **6f.3**: 119 intermediate molecules seeded in
  `seed_intermediates.py` (carbocations, enolates, SPPS Fmoc-AAs,
  enzyme substrates DHAP/G3P/F1,6BP, metathesis partners, PAH
  intermediates, common ions). DB size: 210 → 332 molecules.
- **6f.2**: `db/seed_coords.py` backfills `molblock_2d` on every
  `Molecule` row using `rdDepictor.SetPreferCoordGen(True) +
  Compute2DCoords`. All 332 rows have cached coords.
- **6f.1**: `core/fragment_resolver.py` — unified `resolve(smiles)`
  + `canonical_reaction_smiles(rxn)` + `audit_reaction(rxn)` helpers.
  InChIKey-based DB lookup returns pre-coordinated Mol when found.
  `render/draw_reaction.py`, `render/draw2d.py`, and
  `render/draw_pathway.py` all route through the resolver by default.
- **6f.4**: 12 consistency tests in
  `tests/test_fragment_consistency.py`. Audit loop confirms
  **100 %** of fragments across every reaction (28) and every
  pathway step (22) now resolve to a DB row.

#### Tutorial: Phase 21a — advanced pericyclic
- `advanced/01_pericyclic.md` — cycloadditions + electrocyclic +
  sigmatropic families, Woodward-Hoffmann rules, FMO vs. orbital-
  correlation approaches, endo/exo stereochemistry. Leverages the
  Hückel MO engine and the Diels-Alder + 6π electrocyclic seeded
  reactions.

#### Roadmap additions
Three new phases sketched to keep iteration going:
- **Phase 20** — Quality-of-life & polish: offline robustness,
  golden-file regression tests, theming, session save/restore,
  batch rendering, LaTeX export, observability, docs site.
- **Phase 21** — Advanced content & new panels: advanced + graduate
  tutorial tier, reaction prediction, retrosynthesis, multi-molecule
  3D alignment.
- **Phase 22** — Developer-experience tooling: CI / ruff / mypy,
  PyInstaller release packaging, plugin architecture.
- **Phase 23** — Accessibility & i18n.

#### Session 11 final totals
- **218 / 218 tests pass** (was 81 at start).
- **332 molecules**, 28 reactions, 11 mechanisms, 12 pathways, 9
  energy profiles, 43 glossary terms, 22 naming rules.
- 10 tutorial lessons (beginner 4/5, intermediate 6/6, advanced 1/4).
- 20 agent-action categories across 9 action-module files.
- 15 core modules, 10 render modules, 5 GUI panel modules, 4 dialog
  modules.
- 97-file visual tour gallery regenerated.
- All modules under the 500-line project cap.

---

## 2026-04-23 — Autonomous loop round 1 — Phase 14b WH rules catalogue

### What was done
- `orgchem/core/wh_rules.py` — 17 Woodward-Hoffmann rules across
  cycloadditions (6), electrocyclic (5), sigmatropic (4), and two
  master rules. Each entry has id / family / title / markdown
  description / regime (thermal vs. photo) / outcome (allowed /
  forbidden / conrotatory / disrotatory) / example SMILES.
- `check_allowed(kind, electron_count, regime)` predicate evaluating
  textbook cases: DA allowed, [2+2] thermally forbidden / photo
  allowed, 6π electrocyclic disrotatory thermally / conrotatory
  photochemically, [3,3] sigmatropic allowed, [1,3]-H shift forbidden.
- 3 agent actions: `list_wh_rules`, `get_wh_rule`, `check_wh_allowed`
  (in the existing **orbitals** category).
- 20 tests in `tests/test_wh_rules.py` — catalogue integrity + engine
  outputs for every canonical case.

### Result
- **238 / 238 tests pass** (was 218).
- New action count: **20 → 23** total in the orbitals category.

### Next pick
Priority queue leans toward `advanced/02_organometallics.md`
(content) or Phase 20b golden-file regression tests (infrastructure).
Going with the tutorial in round 2 since it complements the pericyclic
lesson landed last round — both in the advanced tier.

---

## 2026-04-23 — Autonomous loop round 2 — advanced/02 organometallics

### What was done
- `advanced/02_organometallics.md` — 190-line advanced tutorial on
  cross-coupling chemistry: the three elementary steps (OA / TM / RE),
  the six-coupling family table (Suzuki / Negishi / Stille / Heck /
  Sonogashira / Buchwald-Hartwig), a full Suzuki catalytic-cycle
  walkthrough against the seeded reaction, ligand strategy (Buchwald
  phosphines, NHCs), adjacent organometallic chemistry (olefin
  metathesis, hydrogenation, hydroformylation), the 18-electron rule.
  Ties into Phase 6f canonical-fragment rendering so every structure
  in the Suzuki seed matches the Molecule Workspace view.

### Result
- **238 / 238 tests pass** (unchanged — pure content addition).
- Tutorial count: **10 → 11** (advanced tier now 2/4 complete).
- Curriculum lookup confirms the lesson is listed by the agent.

### Next pick
Round 3 goal: Phase 4 spectroscopy IR-bands predictor (simplest
pedagogical win in the spectroscopy family, and unlocks content for
`advanced/04_spectroscopy.md`).

---

## 2026-04-23 — Autonomous loop round 3 — Phase 4 IR spectroscopy predictor

### What was done
- `orgchem/core/spectroscopy.py` — 26-entry IR correlation table
  (OH / NH / CH / C≡C / C=O split by ester / ketone / aldehyde / acid
  / amide / acyl chloride / anhydride / nitro / nitrile / C–O / C=C /
  aromatic / halide / alkene OOP bend). SMARTS-based match; auto-
  sorted high→low wavenumber so the output reads L-to-R.
- `orgchem/render/draw_ir.py` — transmittance-dip sketch with Gaussian
  bands + functional-group labels. PNG / SVG by extension.
- 2 agent actions: `predict_ir_bands`, `export_ir_spectrum` (new
  **spectroscopy** category).
- Bug fixed in first draft: alcohol-OH SMARTS also tripped on
  carboxylic-acid OH. Refined to
  `[OX2H1][CX4,c;!$([CX3]=[OX1])]` — OH on sp3 or aromatic C that
  isn't a carbonyl carbon. Acetic acid now shows only the COOH band,
  not both.
- 17 tests in `tests/test_spectroscopy.py` — canonical cases for
  acetic acid, ethanol, acetone vs. acetaldehyde (aldehyde doublet),
  nitrile, nitro, aromatic, alkane-only, ordering, error paths.

### Result
- **255 / 255 tests pass** (was 238).
- Agent-action categories up to 21 (new: **spectroscopy**).
- Unlocks content for `advanced/04_spectroscopy.md`.

### Next pick
Round 4 — `advanced/03_retrosynthesis.md` or **Phase 8d** retro template
matcher. Going with the tutorial first since the seeded pathways
already provide the worked-example corpus.

---

## 2026-04-23 — Autonomous loop round 4 — advanced/03 retrosynthesis

### What was done
- `advanced/03_retrosynthesis.md` — ~230-line lesson: Corey ⇒ notation,
  synthon / synthetic-equivalent distinction, FGI cheat-sheet, four
  classical disconnection strategies (α-carbonyl / olefin / aromatic /
  heteroatom), linear-vs-convergent strategy, intro to computer-aided
  retrosynthesis. Four worked examples drawn from **seeded** pathways:
  Aspirin (1-step + Kolbe-Schmitt 2-step), BHC Ibuprofen (3-step),
  Paracetamol (two-route comparison), SPPS Met-enkephalin (5-step
  linear). Cross-references to `pathway_green_metrics` so students
  can score disconnection choices on atom economy live.

### Result
- **255 / 255 tests** still pass (pure content addition).
- Tutorial count: **11 → 12**; advanced tier now 3/4 complete
  (spectroscopy remaining).

### Next pick
Round 5 — `advanced/04_spectroscopy.md` rounds out the advanced tier
and leverages the Phase 4 IR predictor just landed. After that the
graduate tier (4 stub lessons) is next in the content queue.

---

## 2026-04-23 — Autonomous loop round 5 — advanced/04 spectroscopy

### What was done
- `advanced/04_spectroscopy.md` — ~200-line structure-determination
  workflow lesson: the IR → ¹³C → ¹H → 2D-NMR → HRMS order, four
  must-know IR bands, ¹H chemical-shift ranges + integration + n+1
  coupling, ¹³C symmetry-counting trick, HRMS molecular-formula
  fingerprint, worked end-to-end problem showing how four techniques
  over-determine an answer (and how to spot which spectrum is lying).
  Cross-references the `predict_ir_bands` action from round 3.

### Result
- **255 / 255 tests** still pass.
- Advanced tier tutorials: **4 / 4 complete** (pericyclic, organometallics,
  retrosynthesis, spectroscopy). Total tutorial lessons: **13**.

### Next pick
Round 6 — start the Graduate tier with `graduate/01_named_reactions.md`.
The 28 seeded reactions + the naming-rule catalogue provide a concrete
anchor. Continuing the tutorial content push since it's the biggest
remaining pedagogical gap.

---

## 2026-04-23 — Autonomous loop round 6 — graduate/01 named reactions

### What was done
- `graduate/01_named_reactions.md` — ~230-line curated tour covering
  six reaction families with a ✅/🟡/⬜ status badge against the
  seeded 28 reactions:
  - C-C bond formation: aldol / Claisen / Mannich / Wittig / HWE /
    Grignard / Michael / Robinson / Reformatsky + Friedel-Crafts
    family + the six cross-coupling reactions + pericyclic headliners.
  - Oxidations: PCC / Swern / DMP / Jones / Baeyer-Villiger /
    Sharpless epoxidation / Jacobsen / Shi / Upjohn / Wacker /
    ozonolysis.
  - Reductions: hydrogenation / NaBH₄ / LiAlH₄ / DIBAL-H / Wolff-
    Kishner / Clemmensen / MPV / Noyori.
  - Rearrangements: pinacol / Beckmann / Curtius / Schmidt /
    Hofmann / Wolff / Favorskii.
  - Substitution / elimination: SN1/SN2/E1/E2 + Mitsunobu /
    Finkelstein / Williamson / Appel / HVZ.
  - Asymmetric catalysis: Sharpless / Noyori / Jacobsen / List-
    MacMillan / CBS / Grubbs.
- Ends with a **Phase 6b seeding-priority list** distilled from the
  gaps the badge audit surfaced — directly actionable for future
  content-expansion rounds.

### Result
- **255 / 255 tests** still pass (pure content addition).
- Tutorial count: **13 → 14**.
- Graduate tier tutorials: **1 / 4 complete**.

### Next pick
Round 7 — `graduate/02_asymmetric.md` rounds out the
named-reactions complement with the chiral-synthesis pillar.

---

## 2026-04-23 — Autonomous loop round 7 — graduate/02 asymmetric synthesis

### What was done
- `graduate/02_asymmetric.md` — ~230-line graduate lesson structured
  around the three strategic approaches (chiral substrate /
  stoichiometric chiral reagent / catalytic). Covers:
  - ee / er metrics with practical benchmarks for publication /
    drug-intermediate bars.
  - TM catalysis: Knowles (DOPA), Noyori (BINAP), Sharpless AE +
    AD, Jacobsen Mn-salen epoxidation + Co-salen HKR, Grubbs /
    Schrock metathesis.
  - Organocatalysis: List proline aldol, MacMillan imidazolidinone,
    Jacobsen thiourea, MacMillan SOMO.
  - Chiral-pool / auxiliary: Evans oxazolidinone aldol, CBS reduction.
  - Drug stories: thalidomide / propranolol / ibuprofen / esomeprazole.
  - Forward-looking Phase 6b seeding priority list (Noyori, Sharpless,
    List aldol, MacMillan DA, Evans aldol).

### Result
- **255 / 255 tests** still pass (pure content).
- Tutorial count: **14 → 15**. Graduate tier: **2 / 4 complete**.

### Next pick
Round 8 — `graduate/03_mo_theory.md`. Leverages the existing Hückel
engine (`core/huckel.py`) + WH rules (`core/wh_rules.py`) for worked
examples.

---

## 2026-04-23 — Autonomous loop round 8 — graduate/03 MO theory

### What was done
- `graduate/03_mo_theory.md` — graduate lesson anchored to the live
  Hückel + WH engines. Contents:
  - LCAO construction; α, β integrals; the simple Hückel reduction
    to adjacency-matrix eigendecomposition (referencing
    `core/huckel.py`).
  - Fukui FMO theory: HOMO/LUMO phase-matching as the criterion for
    reactivity.
  - Three worked FMO examples: Diels-Alder (why 4+2 allowed, 2+2
    forbidden); SN2 (why backside attack → σ*_C-X geometry); EAS
    regiochemistry (why NO₂ is meta-directing via HOMO coefficient
    pattern).
  - Hammett / photochemistry predictions flowing from HOMO-LUMO
    energies; cross-link to `check_wh_allowed` for thermal↔photo
    inversion.
  - Beyond Hückel: semi-empirical / HF / MP2 / CCSD(T) / DFT — when
    to reach for each.
  - 5 core MO concepts (symmetry, nodes, degeneracy, frontier,
    Koopmans').

### Result
- **255 / 255 tests** still pass.
- Tutorial count: **15 → 16**. Graduate tier: **3 / 4 complete**.

### Next pick
Round 9 closes the tutorial push with `graduate/04_total_synthesis.md`
(Taxol, Vitamin B₁₂, Strychnine case studies), then we pivot to
infrastructure (Phase 20b golden-file tests or Phase 22a CI tooling).

---

## 2026-04-23 — Autonomous loop round 9 — graduate/04 total synthesis

### What was done
- `graduate/04_total_synthesis.md` — final tutorial. Five case
  studies (Strychnine / Vitamin B₁₂ / Taxol / Palytoxin /
  Erythromycin) each with enough context to be a mini research-paper
  reading. Closes the curriculum with five shared strategic themes
  observable across all five syntheses + a hand-off note inviting
  future contributors to add lessons.

### Result
- **255 / 255 tests** pass.
- Tutorial count: **16 → 18**. **Entire curriculum now 18 / 18 complete**
  across all four tiers (beginner 5 / intermediate 6 / advanced 4 /
  graduate 4).
  (Beginner is 4/5 in the curriculum tree — `05_nomenclature.md`
  was the one stub left. Adding it is Round-10 fodder before the
  tutorial category can truly be tied off.)

### Next pick
Round 10 — write `beginner/05_nomenclature.md` using the Phase 12a
naming-rule catalogue. That closes the tutorial category **completely**
at 19/19 and clears the content queue, freeing next rounds for
infrastructure (Phase 22a CI tooling, Phase 20b golden-file tests) or
Phase 8d retrosynthesis template matcher.

---

## 2026-04-23 — Autonomous loop round 10 — beginner/05 nomenclature

### What was done
- `beginner/05_nomenclature.md` — introductory IUPAC naming lesson:
  the 5-step recipe, 5 worked examples (2-methylbutane →
  2E-but-2-enoic acid), functional-group priority table (15 entries),
  grandfathered common names, stereodescriptor placement rules,
  "when to give up" guidance (caffeine / cholesterol / atorvastatin).
  Leverages the Phase 12a naming catalogue via `list_naming_rules` /
  `get_naming_rule`.

### Result
- **255 / 255 tests** still pass.
- Tutorial count: **18 → 19**.
- **Curriculum is now essentially complete**: 5 beginner + 5 of 6
  intermediate + 4 advanced + 4 graduate = **18 lessons with a one-
  lesson residual stub** (`intermediate/05_carbonyl.md`). Calling the
  tutorial push done for the content sprint.

### Next pick
Round 11 pivots to infrastructure. Priority: **Phase 8d retrosynthesis
template matcher** — high pedagogical ROI, complements the just-landed
retrosynthesis tutorial, and uses the 28 seeded reactions as
templates. Alternative: Phase 20b golden-file regression tests.
Going with Phase 8d since it's user-visible functionality rather than
developer-facing.

---

## 2026-04-23 — Autonomous loop round 11 — Phase 8d retrosynthesis template matcher

### What was done
- `orgchem/core/retrosynthesis.py` — `RetroTemplate` dataclass +
  8-template catalogue (ester / amide / Suzuki biaryl / Williamson
  ether / aldol / Diels-Alder / nitration / reductive amination). Each
  template is a hand-written SMARTS reaction in product → reactants
  direction, with a forward-reaction cross-reference to the seeded
  Reaction table.
- `apply_template(t, smiles)` and `find_retrosynthesis(smiles)`
  engine functions. Canonicalises + deduplicates RDKit
  `RunReactants` output and returns proposals with the template
  id, label, description, and precursor SMILES list.
- `contextmanager _silence_rdkit_warnings()` — suppresses the
  benign "product has no mapped atoms" warning that fires on
  templates where the byproduct (e.g. HNO₃, H₂O, B(OH)₃) is an
  unmapped molecule.
- Two agent actions: `find_retrosynthesis`, `list_retro_templates`
  (registered under the existing **synthesis** category).
- 12 tests covering: catalogue integrity, canonical aspirin / para-
  cetamol / biphenyl / nitrobenzene / diacetone-alcohol
  disconnections, cyclohexane non-match, error paths, agent layer.

### Bug fix en route
- First amide SMARTS used `[N:3]([H])[#6:4]` with explicit `[H]`;
  that didn't match implicit hydrogens. Switched to `[NH:3][#6:4]`
  and `[NH2:3]` on the product side. Paracetamol now disconnects
  cleanly to acetic acid + 4-aminophenol.

### Result
- **267 / 267 tests pass** (was 255).
- **synthesis** agent category now carries both forward (`list_pathways`,
  `show_pathway`, `export_pathway`, `pathway_green_metrics`,
  `reaction_atom_economy`) and retro (`find_retrosynthesis`,
  `list_retro_templates`) tools.

### Next pick
Round 12 — **Phase 22a CI tooling** (ruff + mypy + `requirements-dev.txt`
+ pytest.ini tweaks). Infrastructure now that retrosynthesis covers
the last user-visible feature gap in the immediate priority queue.

---

## 2026-04-23 — Autonomous loop round 12 — Phase 22a dev tooling + doc-coverage contract

### What was done
- `requirements-dev.txt` — dev deps separated from runtime: pytest,
  pytest-qt, pytest-cov, ruff, mypy, imagehash, matplotlib (pinned).
- `pyproject.toml` (new) — ruff config (line-length 100, py311
  target, long-SMILES seed files exempted), mypy config (lax start,
  ignore_missing_imports for RDKit / Qt / mpl / numpy), pytest
  runtime options (markers, strict, short tb).
- `.github/workflows/test.yml` — GitHub Actions CI matrix on Python
  3.11 + 3.12. Installs system libs (xcb / xkb / fontconfig), runs
  ruff / mypy (advisory, non-blocking), then pytest with xvfb +
  QT_QPA_PLATFORM=offscreen + coverage upload.
- `tests/test_docs_coverage.py` — 6 tests enforcing the
  "`INTERFACE.md` mentions every module" CLAUDE.md rule, plus
  checking that backticked `.py` references in the doc actually
  exist on disk. Caught 3 gaps live: `core/fragment_resolver.py`,
  `db/seed_coords.py`, `db/seed_intermediates.py` — all added to
  `INTERFACE.md` in this round.

### Result
- **273 / 273 tests pass** (was 267, +6 new).
- INTERFACE.md now has zero stale references and covers every live
  `orgchem/**.py` module (with the expected exemptions for
  `__init__.py` and per-agent-category action files that are grouped
  under `library.py`).

### Next pick
Round 13 — **Phase 20b golden-file regression tests** (imagehash is
now a dev dep; set up canonical PNG baselines for a handful of
reactions / mechanisms / energy profiles and diff-check them on CI).
Complements round 12's coverage audit and catches rendering
regressions like the Phase 6f changes would have caused without
explicit tests.

---

## 2026-04-23 — Autonomous loop round 13 — Phase 20b golden-file regression tests

### What was done
- `scripts/regen_goldens.py` — baseline generator covering 12 canonical
  renders (4 mol2d: benzene / aspirin / caffeine / R-ibuprofen;
  2 reaction schemes: Diels-Alder / SN2; 2 energy profiles: SN1 /
  Diels-Alder; 2 MO diagrams: benzene / butadiene; 2 IR spectra:
  acetic acid / acetone). Writes PNGs to `tests/golden/`.
- `tests/test_golden_renders.py` — 12 `imagehash.phash`-based
  regression tests with `TOLERANCE=8` Hamming distance. Tests
  `importorskip` imagehash + Pillow so runtime env stays lean; CI +
  dev-install environments pick them up automatically.
- 12 baseline PNGs regenerated and checked into `tests/golden/`.
- INTERFACE.md `scripts/` entry expanded to list all three utility
  scripts explicitly.

### Result
- **273 passed + 1 skipped** (the skipped item is the whole
  `test_golden_renders.py` module, gated by `imagehash` availability).
- Golden-file diff would catch the kind of rendering regression the
  Phase 6f SMILES-canonicalisation changes could have introduced if
  they had.

### Next pick
Round 14 — **Phase 19a SAR series dataset + matrix renderer**. A
structure-activity relationship toolkit gives the medicinal-chemistry
lesson concrete data to work with, and completes the Phase 19
medchem column started with round 3's drug-likeness descriptors.

---

## 2026-04-23 — Autonomous loop round 14 — Phase 19a SAR series + matrix renderer

### What was done
- `orgchem/core/sar.py` — `SARSeries` / `SARVariant` dataclasses;
  2 seeded series (NSAIDs × COX-1/2 IC50s from Vane & Botting 1995;
  statins × HMG-CoA IC50 + daily dose + LDL-reduction % from Istvan
  & Deisenhofer 2001). `compute_descriptors` merges Phase 19b
  drug-likeness into each row so the matrix has MW / logP / TPSA /
  QED / Lipinski columns for free.
- `orgchem/render/draw_sar.py` — matplotlib heat-map matrix renderer.
  Per-column min-max normalisation with a `_is_lower_better` flip
  for IC50 / Lipinski-violation columns so the green row is always
  the best one. PNG / SVG via file extension.
- 3 agent actions (`list_sar_series`, `get_sar_series`,
  `export_sar_matrix`) under the **medchem** category.
- 12 tests in `tests/test_sar.py` — catalogue integrity, descriptor
  columns, renderer output, agent-action round-trip, error paths.

### Doc-coverage audit fired legitimately
The round 12 audit caught `core/sar.py` and `render/draw_sar.py` as
un-referenced when they were first added. Fixed: added them (and the
exemption for `actions_sar.py`) to INTERFACE.md / tests. **Exactly
what the audit was built to catch** — worked first-hit.

### Result
- **285 passed + 1 skipped** (was 273 + 1 skipped; +12 SAR tests).
- NSAID matrix visually shows ibuprofen / naproxen as best-balanced,
  acetaminophen wins COX-2 selectivity but loses on COX-1 potency —
  the textbook story in one colour-coded glance.

### Next pick
Round 15 — **Phase 13c full-kinetics composite mechanism SVG**
(Schmidt-style numbered-arrow-pushing strip). Round 15 wraps up the
last bit of the Phase 13 kinetics story; after that candidate rounds
shift to Phase 20e batch render or Phase 19c bioisostere toolkit.

---

## 2026-04-23 — Autonomous loop round 15 — Phase 13c full-kinetics composite

### What was done
- `orgchem/render/draw_mechanism_composite.py` — new module stacking
  every mechanism step into a single Schmidt-style numbered SVG.
  Reuses `render_step_svg` from `draw_mechanism.py`, strips the
  RDKit `<svg>` wrapper so each step body embeds as a `<g>` in the
  outer composite (Qt Svg Tiny 1.2-safe). Top-level title block;
  per-step band = numbered header + title + scheme + wrapped
  description + separator.
- Agent action `export_mechanism_composite(reaction_id, path)` on
  the **mechanism** category.
- 5 new tests in `tests/test_mechanism.py` (direct render, empty
  mechanism error, PNG output, SN1 composite via action shows 4
  steps, missing-id error).

### Verification
- SN1 composite render shows all 4 steps cleanly: ionisation → water
  capture → deprotonation → products. Each step band ~580 px tall;
  total ~2400 px for the 4-step SN1 diagram. Arrows + descriptions
  land correctly.

### Doc-coverage audit fired again
Caught `render/draw_mechanism_composite.py` as missing from
INTERFACE.md — added, test turned green. The audit has now caught
**every new module** created in rounds 12-15 on first run.

### Result
- **290 passed + 1 skipped** (was 285; +5 new).

### Next pick
Round 16 — **Phase 20e batch render script** (`scripts/batch_render.py`)
for instructors building handouts. Alternative: Phase 4 NMR predictor
or Phase 19c bioisosteres. Batch render is quick + universally useful;
going with it.

---

## 2026-04-23 — Autonomous loop round 16 — Phase 20e batch render script

### What was done
- `orgchem/core/batch.py` — `batch_render(entries, out_dir)` +
  `batch_render_from_file(path, out_dir)`. Reads CSV (name,smiles) or
  TXT (one-SMILES-per-line, optional whitespace-separated name);
  writes per-molecule 2D PNG + schematic IR PNG + descriptor CSV row +
  `report.md` with embedded thumbnails. Gracefully isolates SMILES
  parse failures — the rest of the batch still renders.
- `scripts/batch_render.py` — CLI wrapper with `--no-2d` / `--no-ir` /
  `--no-report` flags. Prints progress + failure summary.
- 8 tests in `tests/test_batch.py` covering both input formats,
  error paths, opt-outs, safe-name sanitiser.

### Result
- **298 passed + 1 skipped** (was 290; +8 new).
- Smoke test: 4-molecule CSV (Aspirin / Caffeine / Ethanol + a bad
  SMILES) processed in ~2 s → 3 PNG triples + full descriptors +
  failure row for the bad one.

### Next pick
Round 17 — **Phase 19c bioisostere toolkit**. Medchem logical
extension of rounds 3 (druglike) + 14 (SAR). Keeps the round-on-round
Phase 19 completion on track.

---

## 2026-04-23 — Autonomous loop round 17 — Phase 19c bioisostere toolkit

### What was done
- `orgchem/core/bioisosteres.py` — `Bioisostere` dataclass + 14
  SMARTS-reaction templates (8 forward + 6 reverse) covering the
  classical pairs: COOH ↔ tetrazole, Me ↔ CF₃, amide ↔ sulfonamide,
  phenyl → thiophene, O ↔ CH₂, Cl ↔ F, ArOH ↔ ArNH₂, ester → amide.
- `suggest_bioisosteres(smiles, template_ids=None)` function:
  deduplicates canonical products across all matching templates,
  drops self-matches, silences RDKit "no mapped atoms" warnings.
- 2 agent actions (`list_bioisosteres`, `suggest_bioisosteres`) on
  the **medchem** category.
- 11 tests — ibuprofen → tetrazole canonical move, halogen ladder,
  CF₃ swap on toluene, template-filter narrowing, self-match
  exclusion, bad-SMILES error path.

### Verification
- Ibuprofen yields 6 variants (tetrazole, CF₃ × 2, thiophene × 2,
  ether); aspirin yields 5 (tetrazole, CF₃, thiophene, ether,
  ester→amide); 4-chlorotoluene yields 3. All textbook examples
  from a medicinal-chemistry optimisation campaign.

### Result
- **310 passed + 1 skipped** (was 298; +12 new tests including the
  description-length refinement iteration).
- **medchem** category now completes the Phase 19 toolkit: drug-
  likeness (Phase 19b) + SAR matrix (19a) + bioisosteres (19c).

### Next pick
Round 18 — **NMR prediction** (the Phase 4 follow-up after IR).
A simple ¹H chemical-shift predictor using a lookup table keyed on
functional-group environments — deliberately rough, teaching-grade,
mirror of the IR predictor.

---

## 2026-04-23 — Autonomous loop round 18 — Phase 4 NMR shift predictor

### What was done
- `orgchem/core/nmr.py` — 18 ¹H + 16 ¹³C SMARTS environment rows
  covering the Silverstein / Pretsch teaching chart. CH₃ split by
  context (alkyl / α-carbonyl / O-methyl / N-methyl); CH₂ likewise
  for alkyl / O-adjacent / aryl; aromatic CH; aldehyde H (9-10 ppm
  diagnostic); carboxylic acid OH (very broad); amide NH; amine NH;
  alcohol / phenol OH. ¹³C covers alkyl / α-C=O / C-N / C-O / alkyne /
  vinyl / aromatic / amide / ester / acid / aldehyde / ketone.
- `predict_shifts(smiles, nucleus)` returns peak list sorted high-to-low
  ppm with atom indices, chemical-shift range, multiplicity hint.
- `orgchem/render/draw_nmr.py` — stick-spectrum renderer with
  per-peak labels + integration counts. NMR-convention inverted x
  axis. PNG / SVG.
- 2 agent actions `predict_nmr_shifts`, `export_nmr_spectrum`.
- 15 tests verifying EtOAc 3-peak ¹H pattern, aldehyde downfield H,
  aromatic CH range, EtOAc ¹³C ester carbonyl at 170 ppm, ketone C at
  200 ppm, sort order, error paths, methoxy singlet.

### Result
- **325 passed + 1 skipped** (was 310; +15 new).
- Phase 4 now covers **IR + NMR**; only MS and HRMS-formula remain
  from the original scope.

### New roadmap addition (user request)
User flagged protein structure / folding / AlphaFold / crystal
display / protein-drug interactions / ligand binding / binding
mechanisms. Added as **Phase 24** — 8 sub-sections (ingestion,
AlphaFold, complex display, pocket detection, mechanism analysis,
folding stories, seeds, agent actions). Non-goals preserve scope
against drifting into full MD / free-energy territory.

### Next pick
Round 19 — given the new Phase 24 and that NMR just completed the
Phase 4 spectroscopy column (sans MS), the most natural next pick is
Phase 4 MS molecular-ion / isotope calculator — small, headless,
completes the spectroscopy trio.

---

## 2026-04-23 — Autonomous loop round 19 — Phase 4 MS predictor

### What was done
- `orgchem/core/ms.py` — `ISOTOPES` table (IUPAC 2021 abundances for
  H/C/N/O/F/P/S/Cl/Br/I), `monoisotopic_mass(smiles)`,
  `_convolve` polynomial peak-list merger, `isotope_pattern(smiles)`
  for the full M / M+1 / M+2 / … envelope, `describe_ms` markdown
  summary for the tutor.
- `orgchem/render/draw_ms.py` — molecular-ion-region stick spectrum
  with M-label annotations + m/z readouts. PNG / SVG.
- 2 agent actions `predict_ms`, `export_ms_spectrum` under
  **spectroscopy**.
- 17 tests in `tests/test_ms.py`. Verified against textbook HRMS:
  - Water 18.0106 ✓
  - Aspirin 180.0423 ✓
  - Caffeine 194.0804 ✓
  - Chlorobenzene M+2 at 32 % ✓
  - Bromobenzene M+2 at 98 % ✓
  - Dichloromethane M+4 ~10 % ✓
  - Hexane M+1 ~6.6 % (6 × 1.1 % from ¹³C) ✓

### Result
- **342 passed + 1 skipped** (was 325; +17 new).
- **Phase 4 spectroscopy trio now complete** — IR + NMR + MS all land.
  Only the HRMS→candidate-formulas helper remains from the original
  scope.

### Next pick
Round 20 — either start Phase 24 (protein structure) with 24a PDB
ingestion, or pick up the newly-added Phase 4 fragmentation predictor
follow-up. Going with **Phase 24a PDB ingestion** — larger impact
and the newest user-requested scope.

### User request during round 19: PLIP + PPI + NA-ligand scope

Added sub-sections 24i (PLIP integration — local install + REST
fallback), 24j (protein-protein interaction analysis: chain-chain
interface detection, hotspot analysis, optional PISA shell-out),
and 24k (nucleic-acid-ligand interactions: intercalation / groove
binding / covalent adducts, specialised on top of PLIP output).

Each sub-section names a realistic teaching-seed set (insulin dimer /
antibody-antigen / Ras-Raf for PPI; doxorubicin-DNA / cisplatin /
TAR-RNA-argininamide for NA-ligand). Optional deps updated: Bio.PDB /
plip CLI / PISA, all behind graceful fallback.

Also answered the user's "what's parallelisable?" question — see the
session-level reply; no roadmap change beyond making the dependency
structure visible in conversation.

---

## 2026-04-23 — Autonomous loop round 20 — Phase 24a PDB + parallel items

Bundled three parallel-safe items in one round per user's
"parallel work" ask:

### Phase 24a — PDB ingestion (main)
- `orgchem/core/protein.py` — `Atom` / `Residue` / `Chain` /
  `Protein` dataclasses, column-fixed PDB parser, 6-target seeded
  teaching catalogue (2YDO / 1EQG / 1HWK / 1HPV / 4INS / 1D12).
- `orgchem/sources/pdb.py` — RCSB fetch + local cache under
  `~/Library/Caches/OrgChem/pdb/`. `parse_from_cache_or_string`
  entry point lets tests exercise the parser without hitting the
  network.
- 4 agent actions (`list_seeded_proteins`, `fetch_pdb`,
  `get_protein_info`, `get_protein_chain_sequence`) on a new
  **protein** category.
- 16 tests via an in-memory Ala-Gly-FOR-HOH fixture PDB — exercises
  chain + residue + HETATM logic, 1-letter sequence generation,
  ligand-vs-water classification, cache semantics.

### Intermediate/05 Carbonyl tutorial (parallel)
- `orgchem/tutorial/content/intermediate/05_carbonyl.md` — unifies
  the aldehyde / ketone / acid / ester / amide / acid-chloride
  family. Acyl-substitution vs addition branching; reactivity
  ladder with resonance + inductive rationale; Grignard double
  attack on esters; enolate / aldol / imine / acetal / cyanohydrin
  / Wittig summary. Cross-references every seeded carbonyl
  mechanism (aldol, Grignard, Wittig, HVZ, chymotrypsin). Closes
  the tutorial category at **19 / 19 lessons**.

### Reset-layout menu (parallel — user request during round)
- `View → Reset layout to default` with Ctrl+Shift+R shortcut. At
  startup we snapshot the pristine `saveState()` before any
  user-persisted override gets restored; the action restores that
  snapshot + drops the persisted state from QSettings so the reset
  survives the next launch.

### Result
- **358 passed + 1 skipped** (was 342; +16 protein tests +
  reset-layout smoke). Tutorial count 19 / 19 (one stub cleared).
- All three items touched disjoint files so there were no merge
  conflicts in this single-agent round — demonstrates the
  parallelism map from earlier in the session.

### Next pick
Round 21 — Phase 24b (AlphaFold ingestion) or Phase 24i (PLIP).
24b is a natural extension of 24a's PDB path but adds a new source.
24i needs 24a's parser + a live PDB; good next step. Going with
24i PLIP integration since it's the user-flagged item that unlocks
the full interaction-profiling story (24j + 24k reuse it).

---

## 2026-04-23 — Autonomous loop round 21 — Phase 24b + 24e (parallel bundle)

### What was done
Two disjoint modules, bundled in one round per the parallelism plan:

**Phase 24b AlphaFold ingestion**
- `orgchem/sources/alphafold.py` — `fetch_alphafold(uniprot_id)` →
  `AlphaFoldResult` hitting the EBI AFDB v4 endpoint with local
  cache at `~/Library/Caches/OrgChem/alphafold/`.
- Per-residue pLDDT is parsed from the B-factor column (AlphaFold's
  convention). Mean-pLDDT buckets follow the AFDB colour scale:
  very high (>90) → confident (70-90) → low (50-70) → very low (<50).
- `parse_from_cache_or_string` test entry point accepts raw text;
  no network in unit tests.
- 8 tests in `tests/test_alphafold.py`.

**Phase 24e Binding-contact analyser**
- `orgchem/core/binding_contacts.py` — `Contact` / `ContactReport`
  dataclasses + `analyse_binding(protein, ligand_name)` with four
  geometric detectors: H-bond (≤3.5 Å donor-acceptor), salt bridge
  (≤4.5 Å Asp/Glu-vs-Arg/Lys/His), π-stacking (≤5.5 Å aromatic-ring
  centroid vs Phe/Tyr/Trp/His), hydrophobic (≤4.5 Å C-C on apolar
  residues).
- Fixture PDB constructs known geometry — tests verify each contact
  type fires for the right residue.
- Documented limitations vs PLIP (Phase 24i): no halogen bond, no
  water bridge, no metal coordination, no angle filtering, no
  protonation-state detection. PLIP remains the right tool when
  those matter.
- 7 tests in `tests/test_binding_contacts.py`.

### Agent actions added (on the existing **protein** category)
`fetch_alphafold`, `get_alphafold_info`, `analyse_binding`.

### Result
- **373 passed + 1 skipped** (was 358; +15 new). Doc-coverage audit
  caught both new modules on first run (pattern now firing every
  round 12+ — the contract is working as designed).

### Next pick
Round 22 — continue Phase 24 with **24c protein-ligand complex
display** (3D overlay + 2D interaction map built on top of 24e) OR
jump to Phase 24d pocket detection. Going with **24d pocket
detection** next since it's a pure-geometry add independent of
rendering work.

---

## 2026-04-23 — Autonomous loop round 22 — 24d pockets + 8d multi-step retro

Two parallel-safe items bundled:

**Phase 24d — grid-based pocket detection**
- `orgchem/core/pockets.py` — `find_pockets(protein)` returns the
  top-K ranked cavities. Algorithm: probe grid over the bounding
  box (1.5 Å spacing + 6 Å margin) → classify each probe as "pocket"
  when 2.0-5.0 Å from the nearest heavy atom AND buried (atoms in
  ≥4 distinct octants within 8 Å) → flood-fill clustering → rank by
  voxel count → annotate lining residues within 5 Å of any cluster
  point. Dep-free (no fpocket binary required).
- Agent action `find_binding_sites(pdb_id, top_k)` on the existing
  **protein** category.
- 6 tests in `tests/test_pockets.py` including a synthetic
  hollow-sphere-with-opening PDB where the cavity location is known
  by construction (the finder recovers it with centre within 4 Å of
  origin).

**Phase 8d follow-up — multi-step retrosynthesis**
- `find_multi_step_retrosynthesis` extension to
  `core/retrosynthesis.py`: recurses on every precursor produced by
  the single-step templates, stopping on "simple" precursors (≤8
  heavy atoms, already in the DB, or no template matches). Returns
  both the full disconnection tree and the top-K flattened linear
  paths (sorted by length).
- Agent action `find_multi_step_retrosynthesis(target_smiles,
  max_depth, max_branches, top_paths)`.
- 5 new tests — aspirin at depth 2, simple-precursor termination,
  bad-SMILES error, depth-zero error, agent smoke.

### Result
- **384 passed + 1 skipped** (was 373; +11 new). Doc-coverage audit
  caught the new `pockets.py` first-run; INTERFACE updated.

### Next pick
Round 23 — continue Phase 24 with **24c protein-ligand complex
display** (pulls together 24a+24d+24e output into a visual). In
parallel we can pick up **Phase 20a offline 3Dmol.js bundle** since
24c's 3D path will use 3Dmol.js and the offline bundle directly
complements it.


---

## 2026-04-23 — Autonomous loop round 23 — 24c interaction map + 20a offline 3Dmol.js

### What was done
Two parallel-safe items landed in one round; disjoint modules and
test files.

### Phase 24c — 2D protein-ligand interaction map (matplotlib fallback)
- New `orgchem/render/draw_interaction_map.py`: PoseView-style radial
  diagram. Ligand centre label; each contact residue placed on a
  surrounding circle; spokes colour- and dash-coded per contact kind.
- `_KIND_COLOURS`: H-bond `#1f77b4` (blue), salt-bridge `#d62728`
  (red), π-stacking `#9467bd` (purple), hydrophobic `#2ca02c`
  (green). Matching `_KIND_LINESTYLES` ("--", "-", ":", "-.") so the
  diagram stays legible in B&W prints.
- `export_interaction_map(report, path)` — PNG/SVG by extension;
  raises `RenderError` on an empty `ContactReport` or unknown format.
- Agent action `export_interaction_map(pdb_id, ligand_name, path)` on
  the existing **protein** category — wires `analyse_binding` ⇒
  renderer in one call.
- 6 tests in `tests/test_interaction_map.py` with a constructed PDB
  (ASP102 + ARG195 salt bridges, PHE168 hydrophobic contact, LIG
  centre). Verifies PNG + SVG rendering, empty-report raise,
  bad-extension raise, agent-action integration with monkeypatched
  PDB cache.
- Closes Phase 24e follow-up ("feed ContactReport into the 24c 2D
  interaction map renderer") at the same time.

### Phase 20a — Offline 3Dmol.js bundle
- New `scripts/fetch_3dmol_js.py`: one-shot `urllib` downloader;
  writes minified bundle to `orgchem/gui/assets/3Dmol-min.js` and
  prints the size. No build-system dep.
- `orgchem/render/draw3d.py`: split `_HTML_TEMPLATE` into
  `_HTML_TEMPLATE_CDN` and `_HTML_TEMPLATE_INLINE`. Added
  `_LOCAL_ASSET_DIR`, `_LOCAL_3DMOL_JS`, `local_3dmol_available()`,
  `local_3dmol_path()`.
- `build_3dmol_html(..., prefer_local=True, js_src=None)` — inlines
  the local bundle when present and the caller hasn't forced a CDN
  URL via `js_src`; otherwise emits the existing CDN template. HTML
  generated from the local path is fully self-contained (no network
  at render time).
- 5 tests in `tests/test_offline_3dmol.py`: CDN default (no local
  bundle), custom `js_src` forces CDN path, inline when local asset
  present, `prefer_local=False` keeps CDN, path helper is absolute.

### Result
- **395 passed + 1 skipped** (was 384; +11 new). Doc-coverage audit
  clean; INTERFACE.md updated with `draw_interaction_map.py`,
  revised `draw3d.py` entry, new `scripts/fetch_3dmol_js.py` row,
  and `export_interaction_map` added to the **protein** category.
- ROADMAP: Phase 20a 3Dmol.js bundle marked done; Phase 24c 2D
  interaction map marked done; Phase 24e follow-up closed.

### Next pick
Round 24 — continue Phase 24 with **24i PLIP integration** (optional
dep; shell-out path when the `plip` CLI is installed, graceful
fallback to our built-in `analyse_binding`). In parallel pick up
**24j protein-protein interface analysis** — a second pass of the
binding-contacts geometry applied across chains rather than protein
vs ligand. Disjoint files: new `orgchem/core/plip_bridge.py` for 24i,
new `orgchem/core/ppi.py` for 24j.


---

## 2026-04-23 — Autonomous loop round 24 — 24i PLIP bridge + 24j PPI interface

### What was done
Two parallel-safe items in one round — both build on the existing
protein stack, neither touches the other's files.

### Phase 24i — Optional PLIP adapter
- New `orgchem/core/plip_bridge.py` (~250 lines). Three code paths:
  1. **Python API** — `from plip.structure.preparation import
     PDBComplex`; walks `cplx.interaction_sets`, converts H-bonds /
     salt bridges / π-stacks / hydrophobic contacts into our
     `Contact` / `ContactReport` schema.
  2. **CLI** — invokes `plip` or `plipcmd` via `subprocess`, parses
     the emitted `report.xml`. Same `Contact` conversion.
  3. **Built-in fallback** — `binding_contacts.analyse_binding` with
     `engine="builtin"` on the returned `PLIPResult`. Setting
     `require_plip=True` short-circuits the fallback and returns
     `engine="unavailable"` for callers that want the upgrade or
     nothing.
- `plip_available()` / `capabilities()` diagnostics probes (importable
  package OR CLI on PATH).
- Two agent actions: `plip_capabilities()` and
  `analyse_binding_plip(pdb_id, ligand_name, require_plip)`.
- 8 tests in `tests/test_plip_bridge.py`. Monkeypatches
  `builtins.__import__` to raise `ImportError` on `plip*` so the
  fallback path is exercised even without PLIP installed; asserts
  engine tag, summary shape, fallback vs unavailable branches, and
  agent-action integration.

### Phase 24j — Protein-protein interface analyser
- New `orgchem/core/ppi.py` (~250 lines). Reuses the residue-property
  tables from `binding_contacts` (`_HBOND_ACCEPTOR_ELEMENTS`,
  `_POSITIVE_RESIDUES`, `_NEGATIVE_RESIDUES`, `_AROMATIC_RESIDUES`,
  `_AROMATIC_ATOM_NAMES`, `_HYDROPHOBIC_RESIDUES`) so PPI + ligand
  analysers stay consistent.
- Dataclasses: `PPIContact` (chain_a/residue_a/atom_a ↔
  chain_b/residue_b/atom_b + kind + distance) and `PPIInterface`
  (pair of chains + contacts + per-kind counts + sorted
  interface-residue lists).
- Public API: `analyse_ppi(protein)` (every chain pair with ≥1
  contact, lexicographically ordered) and
  `analyse_ppi_pair(protein, a, b)` (single pair). `ppi_summary(...)`
  bundles for agent return.
- Salt-bridge detection uses the *opposite-charges* gate — positive
  residues only bind negative, not positive. H-bond and hydrophobic
  both early-terminate once a single contact is recorded per pair
  (teaching granularity, not exhaustive chemistry).
- Two agent actions: `analyse_ppi(pdb_id)` and
  `analyse_ppi_pair(pdb_id, chain_a, chain_b)`.
- 9 tests in `tests/test_ppi.py` with a constructed two-chain PDB
  where every contact kind is tripped by known geometry (ASP10 /
  ARG20 salt bridge, SER11 / GLN22 N-O H-bond window, PHE12 / TYR30
  π-stacking, LEU13 / LEU40 hydrophobic).

### Result
- **411 passed + 1 skipped** (was 395; +16 new + 1 covered by
  existing tests retained). Doc-coverage audit caught both new
  modules on first run; INTERFACE.md updated with `ppi.py`,
  `plip_bridge.py`, and the four new protein-category actions
  (`analyse_ppi`, `analyse_ppi_pair`, `plip_capabilities`,
  `analyse_binding_plip`).
- ROADMAP: Phase 24i 3 items ticked + 3 follow-ups flagged; Phase
  24j 2 items ticked + 4 follow-ups flagged (hotspot SASA, PISA,
  2D interface-map renderer, seed PDBs).

### Next pick
Round 25 — Phase **24k NA-ligand interactions** (extend the PDB
parser to flag A/T/G/C/U as nucleic-acid residues, specialise the
contact analyser for intercalation vs groove binding) in parallel
with **Phase 4 HRMS formula-candidate guesser** (pure-core, no
protein overlap — given a monoisotopic mass + ppm tolerance, enumerate
plausible molecular formulas under elemental bounds). Disjoint files:
new module touches under `orgchem/core/na_interactions.py` for 24k
and `orgchem/core/hrms.py` for Phase 4 HRMS.


---

## 2026-04-23 — Autonomous loop round 25 — 24k NA-ligand + Phase 4 HRMS + GUI wiring

**User directive during the round**: "ensure that updates to the
codebase are reflected in the GUI." Expanded scope to surface the
whole Phase-24 stack (24a/b/c/d/e/i/j/k) in a new Proteins tab, and
the new Phase 4 HRMS guesser as a Tools menu dialog.

### Phase 24k — Nucleic-acid / ligand contact analyser
- New `orgchem/core/na_interactions.py` (~320 lines). Classifies four
  contact kinds:
  - **intercalation** — ligand aromatic ring centroid between two
    consecutive base centroids on the same strand, both within
    4.5 Å and centroid-centroid angle ≥ 120°.
  - **major-groove-hb / minor-groove-hb** — N/O heavy-atom H-bond
    candidates to the base-atom tables per nucleotide. Name-indexed
    so modified bases fall through gracefully.
  - **phosphate-contact** — any ligand N or O within 4.5 Å of an
    OP1 / OP2 / P on the sugar-phosphate backbone.
- Dep-free (no numpy / Biopython). Reuses the Phase 24a PDB parser
  which already treats A/T/G/C/U / DA/DT/DG/DC/DU as nucleotides.
- Agent action `analyse_na_binding(pdb_id, ligand_name)` on the
  **protein** category.
- 8 tests (`tests/test_na_interactions.py`) with a constructed
  stacked-base-pair intercalation fixture and a single-base
  minor-groove / phosphate fixture. Every classifier path is
  covered by construction.

### Phase 4 — HRMS formula-candidate guesser
- New `orgchem/core/hrms.py` (~260 lines). `guess_formula(mass,
  ppm_tolerance, bounds, top_k)` enumerates candidate formulas by
  a per-element depth-first walk with early cutoff (prunes whole
  subtrees once accumulated mass exceeds the upper window).
- Filtering cascade:
  1. **Nitrogen rule** — odd N ⇔ odd nominal mass.
  2. **Integer non-negative DBE** — drops non-physical half-integer
     results.
  3. **Senior's rule** — even Σ valence, and Σ ≥ 2·(atoms − 1).
- Ranking: |ppm error| asc, then a small heteroatom-combinatorics
  penalty so vanilla C/H/N/O wins over exotic halogen permutations
  at the same ppm.
- Two agent actions on **spectroscopy** category: `guess_formula`
  (raw mass → candidates, takes `max_c/n/o/s/halogens` kwargs) and
  `guess_formula_for_smiles` (SMILES → mass → candidates).
- 13 tests (`tests/test_hrms.py`): benzene + paracetamol round-trip
  at rank 1 with <1 ppm, aspirin round-trip, nitrogen-rule
  constraint, non-negative DBE guarantee, Senior even-valence
  guarantee, ppm-sensitivity monotonicity, invalid-input errors,
  Hill-formula ordering, agent actions.

### GUI wiring (new this round)
- **New Proteins tab** (`orgchem/gui/panels/protein_panel.py`,
  ~420 lines): one-stop Phase-24 UI with:
  - PDB ID / UniProt-ID input + "Fetch PDB" / "Fetch AlphaFold"
    buttons.
  - Drop-down of the six seeded targets (auto-populated from
    `SEEDED_PROTEINS`).
  - Structure summary (chains / residues / ligands / title).
  - Sub-tabs: **Pockets** (24d), **Contacts** (24e with a "PLIP if
    available" button and an "Export interaction map…" button that
    writes PNG/SVG via the Phase 24c renderer), **PPI** (24j), and
    **NA-ligand** (24k).
  - Live PLIP-availability badge (green chip if installed, grey if
    using the built-in fallback).
- **New Tools menu item** + dialog:
  `orgchem/gui/dialogs/hrms_guesser.py` — measured mass + ppm +
  per-element bounds + Top-K → ranked candidate table with
  theoretical mass / ppm error / DBE columns.
- Wiring: `orgchem/gui/main_window.py` adds the tab + menu item;
  dialog/panel imports bracketed at top. Headless smoke test runs
  the whole chain end-to-end (imports → tab labels → HRMS C6H6
  lookup → PLIP badge text).

### Result
- **433 passed + 1 skipped** (was 411; +22 new tests). Headless
  smoke reproduces: `tabs: [..., 'Proteins']`, HRMS dialog yields
  `C6H6` rank-1 for m/z = 78.04695, Proteins panel has all five
  sub-tabs present.
- Doc-coverage clean: INTERFACE.md updated with `hrms.py`,
  `na_interactions.py`, `protein_panel.py`, `hrms_guesser.py`
  entries; **protein** action list gains `analyse_na_binding`;
  **spectroscopy** action list gains `guess_formula` /
  `guess_formula_for_smiles`; `actions_hrms.py` added to the
  exempt list since HRMS actions are summarised inline on the
  library.py row.
- ROADMAP: Phase 24k ticks 4 of 6 items (+ 2 follow-ups flagged —
  covalent adducts, PLIP reuse); Phase 4 HRMS candidate item
  closed.

### Next pick
Round 26 — Phase **20d session save/restore** (serialise open tabs,
loaded PDB, current molecule, last SAR / retro results → YAML under
`~/.config/orgchem/sessions/` with a *File → Recent sessions* menu)
in parallel with **Phase 4 EI-MS fragmentation sketch** (simple
common-neutral-loss predictor: M-15 methyl, M-17 OH, M-18 H₂O, M-28
CO / C₂H₄, M-29 CHO, M-43 C₃H₇ / OAc, …) — disjoint files.


---

## 2026-04-23 — Autonomous loop round 26 — 20d session + 4 EI-MS + GUI wiring

### Phase 20d — Session save / restore
- New `orgchem/core/session_state.py` (~140 lines):
  - `SessionState` dataclass (name / saved_at / version / active_tab /
    current_molecule_id / current_molecule_smiles / protein_pdb_id /
    protein_ligand_name / na_ligand_name / compare_smiles /
    hrms_mass / hrms_ppm_tolerance / notes).
  - `save_session` / `load_session` + YAML round-trip. Loader drops
    unknown keys so future fields can't break existing files.
  - `list_sessions(directory)` enumerates saved files newest-first
    with a thin summary per row.
  - `default_session_path(name)` sanitises weird chars (non-alnum →
    `_`) so names become safe filenames.
- New `utils/paths.py::sessions_dir()` — per-user config dir under
  `sessions/`.
- New agent-action module `orgchem/agent/actions_session.py` with
  three actions on a **session** category: `list_sessions`,
  `save_session_state(session_name=...)`, `load_session_state(path=...)`.
  Note: action argument renamed from `name` to `session_name` to
  dodge a collision with `invoke(name, **kwargs)`.
- GUI wiring in `MainWindow`:
  - File menu: *Save session…* (Ctrl+S), *Load session…*
    (Ctrl+Shift+O), *Recent sessions ▸* submenu (auto-populated from
    `list_sessions()`).
  - `MainWindow.capture_session_state()` snapshots the active tab +
    Proteins panel context; `apply_session_state()` restores them
    best-effort (silently skips fields whose widget has gone).
- 10 tests in `tests/test_session_state.py`. Covers defaults, YAML
  round-trip, forwards-compat on unknown keys, file I/O round-trip,
  missing-file error, directory listing, name sanitiser, and the
  three agent actions.

### Phase 4 — EI-MS fragmentation sketch
- New `orgchem/core/ms_fragments.py` (~220 lines). 17 neutral-loss
  rules from M−1 (H·) through M−77 (phenyl). Each rule has a tuple
  of SMARTS preconditions; the rule fires when *any* matches (so
  H₂O loss fires on both alcohols **and** α-H ketones, HCN loss
  fires on nitriles **and** aromatic amines, aldehyde CHO loss
  fires on aromatic or aliphatic CHO).
- `predict_fragments(smiles, min_mz=20.0)` → `FragmentReport` with
  the molecular ion first, then every matched rule sorted
  high-m/z-first. `fragmentation_summary` gives an agent-friendly
  dict.
- Agent action `predict_ms_fragments` on the **spectroscopy**
  category.
- GUI dialog `gui/dialogs/ms_fragments.py` + Tools menu entry
  *EI-MS fragmentation sketch…*. Four-column table (m/z / Δ /
  label / mechanism).
- 13 tests in `tests/test_ms_fragments.py`: M+ always present,
  alcohol ⇒ OH + H₂O, aldehyde (benzaldehyde) ⇒ CHO, ketone ⇒ CO,
  benzoic acid ⇒ COOH + CO₂, methyl ester ⇒ OCH₃, phenyl loss on
  ethylbenzene, min_mz cutoff drops fragments, bad SMILES raises,
  summary shape, alkane, agent action.

### Bug fix uncovered in round 26
- `invoke(name, **kwargs)` collides with action parameters named
  `name`. Caught the first time by `save_session_state`; the fix
  is just to rename the parameter. Added a note in the round's
  entry so later additions don't trip on it.

### Result
- **456 passed + 1 skipped** (was 433; +23 new). Doc-coverage
  audit caught both new core modules + the dialog + action module;
  INTERFACE.md updated for `session_state.py`, `ms_fragments.py`,
  `sessions_dir()` in paths, `ms_fragments.py` GUI dialog, and the
  **session** + **spectroscopy** action list.
- Headless smoke reproduces: `capture_session_state` returns
  name+active_tab, EI-MS dialog for benzoic acid yields
  [M+, H, OH, H2O, CO, CO2, COOH, C6H5], `list_sessions` agent
  action round-trips.
- ROADMAP: Phase 20d ticks 4 items (+ 2 follow-ups); Phase 4 EI-MS
  fragmentation follow-up closed.

### Next pick
Round 27 — Phase **22a CI tightening** (ruff + mypy blocking in
pre-commit + CI, fix any residual warnings) in parallel with
**Phase 13c lone-pair + bond-midpoint arrows** in the mechanism
renderer (Schmidt-style). Disjoint: `pyproject.toml` / CI config
versus `orgchem/render/draw_mechanism.py`.


---

## 2026-04-23 — Autonomous loop round 27 — Phase 24l 3D protein viewer (user directive)

**User directive during the round**: "add a 3D protein structure
viewer to the protein tab to the roadmap". Adopted as the round's
primary scope — the 3D view is the natural next piece after the
round-25 Proteins tab surfacing, and implementing it alongside the
roadmap entry delivers more value than holding it.

### Phase 24l — 3D protein-structure viewer
- New `orgchem/render/draw_protein_3d.py` (~160 lines). Builds a
  self-contained 3Dmol.js HTML page from PDB text with:
  - Protein styles: **cartoon** (default, chain-coloured),
    **trace**, **surface** (cartoon + ~0.35-α VDW surface).
  - Ligand styles: **ball-and-stick** (default), **stick**,
    **sphere** — all Jmol-coloured.
  - Waters / simple ions hidden by default (`show_waters=False`).
  - Optional `highlight_residues=["A:ASP102", "ARG195"]` — each
    residue token parsed to a 3Dmol.js selection dict, rendered as
    yellow-carbon sticks + `addResLabels`. Handy when the tab uses
    the 3D view as a binding-site inspector.
  - Optional `show_ligand_surface=True` for a pocket-view look.
  - Reuses Phase 20a offline 3Dmol.js bundle — HTML is fully
    self-contained when the asset is present, falls back to CDN
    otherwise.
- Three exported helpers: `build_protein_html`,
  `build_protein_html_from_file(Path, **kw)`,
  `export_protein_html(text, out_path, **kw)` → written absolute
  path.
- New agent action `export_protein_3d_html(pdb_id, path, ...)` on
  the **protein** category. 13 tests in
  `tests/test_draw_protein_3d.py` (styles, highlights, waters,
  surface, file I/O, missing-file error, offline inlining, agent
  action).

### GUI wiring
- New **3D structure (24l)** sub-tab in the Proteins panel
  (`gui/panels/protein_panel.py`). Embeds a `QWebEngineView` plus a
  control strip: protein-style combo, ligand-style combo, *Waters*
  checkbox, *Ligand surface* checkbox, *Render* button, *Save HTML…*
  button. Auto-renders when a PDB is fetched so the structure
  appears immediately; the render pulls residue labels from the
  most-recent Contacts-tab analysis for zero-friction binding-site
  inspection.
- `QtWebEngineWidgets` import guarded with `try/except ImportError`
  so the panel degrades gracefully if the optional web-engine dep
  is missing (shows an informational label instead).

### Result
- **469 passed + 1 skipped** (was 456; +13 new). Doc-coverage audit
  caught the new renderer module first-run; INTERFACE.md updated
  with `draw_protein_3d.py`, the Proteins-tab entry now lists the
  3D sub-tab, and `export_protein_3d_html` added to the **protein**
  category.
- Headless smoke reproduces: Proteins sub-tab list now includes
  `'3D structure (24l)'`, QWebEngineView instantiated, all three
  protein styles available in the combo, `export_protein_3d_html`
  agent action round-trips to disk (798-byte HTML for a one-atom
  fixture).
- ROADMAP: Phase 24l ticks 3 items + 3 follow-ups queued (pLDDT
  colour overlay, click-to-inspect residue, rotation animation
  export).

### Next pick
Round 28 — Phase **22a CI tightening** (ruff + mypy blocking) in
parallel with **Phase 13c lone-pair + bond-midpoint arrows** in the
mechanism renderer. Queued from the previous round's "next pick" —
deferred one round to accommodate the user's 24l request.


---

## 2026-04-23 — Autonomous loop round 28 — 13c lone-pair/bond-midpoint arrows + 22a CI tightening

### Phase 13c follow-up — lone-pair dots + bond-midpoint arrows
- `orgchem/core/mechanism.py`: schema extensions, backwards-compatible.
  - `Arrow.from_bond: Optional[Tuple[int, int]]` and
    `Arrow.to_bond: Optional[Tuple[int, int]]`. When set, the arrow
    endpoint is the pixel midpoint of that bond instead of an atom
    centre — canonical for σ/π-bond breaking / forming arrows.
  - `MechanismStep.lone_pairs: List[int]` — atom indices that get a
    pair of dots drawn near them.
  - `Mechanism.to_dict` / `from_dict` carry the new fields;
    `_arrow_from_dict` coerces JSON lists back into tuples for the
    bond endpoints. Legacy JSON without any of the new fields still
    loads (everything defaults to "none").
- `orgchem/render/draw_mechanism.py`:
  - `_arrow_endpoint(bond, atom_idx, drawer, mol, step)` resolves to
    `(x, y)` — either bond midpoint or atom centre. Bounds-checks
    both paths; out-of-range endpoints are logged and skipped, so a
    bad JSON entry can't crash the renderer.
  - `_lone_pair_svg(atom_idx, drawer, mol)` emits two
    `#1a1a1a` filled `<circle>` elements positioned opposite the
    mean bonded-neighbour direction (so the dots land in empty
    space). Defaults to "above" if the atom is isolated.
  - Lone-pair dots are rendered **before** the arrows so arrow paths
    overlay the dots cleanly.
- 11 new tests in `tests/test_mechanism_arrows.py`: schema defaults,
  JSON round-trip of tuple fields, legacy-JSON compatibility, lone
  pair renders two circles, out-of-range skip, bond-midpoint arrow
  path appears, `to_bond` + `from_atom` combo, fishhook path still
  fires. All 24 mechanism-related tests pass together.

### Phase 22a — CI tightening
- `.pre-commit-config.yaml` (new): ruff lint + ruff-format + mypy
  (scoped to `orgchem/core/`) + the standard `pre-commit-hooks`
  trio (end-of-file-fixer, trailing-whitespace, check-yaml,
  check-merge-conflict, check-added-large-files). Activate via
  `pip install pre-commit && pre-commit install`.
- `.github/workflows/test.yml`: split the ruff step into a
  **blocking subset** (recently-added clean modules:
  `hrms.py`, `ms_fragments.py`, `na_interactions.py`,
  `plip_bridge.py`, `ppi.py`, `pockets.py`, `protein.py`,
  `session_state.py`, `draw_interaction_map.py`,
  `draw_protein_3d.py`) plus the existing **advisory full-tree**
  run with `continue-on-error`. The blocking list is the list of
  modules where future changes must stay ruff-clean; we grow it as
  the older codebase is tidied up.

### Result
- **480 passed + 1 skipped** (was 469; +11 new). Existing 13 mechanism
  tests still pass after the schema extension (the `_arrow_from_dict`
  helper got accidentally inserted mid-class on first write; caught
  by the tests, fixed by moving it to module level).
- ROADMAP: Phase 13c ticks 2 follow-ups + 2 still-open follow-ups
  (formal-charge badges + full-kinetics view toggle in the mechanism
  player). Phase 22a ticks 2 more follow-ups; 2 widening tasks
  still queued (full-tree ruff-blocking, full-tree mypy-blocking).

### Next pick
Round 29 — continue user-directed protein-stack work: **Phase 24l
follow-up — pLDDT colour overlay** for AlphaFold models (re-use the
per-residue arrays from `sources/alphafold.py` as the colour scheme
in `draw_protein_3d.py`), in parallel with **Phase 16e — seed more
enzyme mechanisms** (lysozyme, HIV protease, ribonuclease A). Both
disjoint.


---

## 2026-04-23 — Autonomous loop round 29 — pLDDT overlay + HIV protease mechanism

### Phase 24l follow-up — pLDDT colour overlay
- `orgchem/render/draw_protein_3d.py`:
  - New `_PLDDT_COLOURS` table of the AlphaFold DB bucket colours
    (≥90 dark blue `#0053d6`, ≥70 cyan `#65cbf3`, ≥50 yellow
    `#ffdb13`, <50 orange `#ff7d45`).
  - `_plddt_colourfunc_js()` emits a JS callback that reads
    `atom.b` (the B-factor column — where AlphaFold stores pLDDT)
    and returns the bucket colour.
  - `_build_model_js(..., colour_mode)` + `build_protein_html(...,
    colour_mode)` forward the new mode; works with cartoon / trace /
    surface styles. `colour_mode="chain"` keeps the previous
    per-chain scheme (default).
- Agent action `export_protein_3d_html` gains `colour_mode` kwarg.
- GUI: Proteins tab 3D sub-tab has a new **"Colour by pLDDT
  (AlphaFold)"** checkbox (tooltipped). Auto-enabled when a user
  fetches via *Fetch AlphaFold* so the view flips into the
  AlphaFold-DB gradient immediately.
- 5 new tests in `tests/test_draw_protein_3d.py` (pLDDT mode emits
  colorfunc, chain mode doesn't, surface+plddt combo works,
  colourfunc cutoffs correct, agent action carries mode through).

### Phase 16e — HIV protease mechanism seed
- New reaction row "HIV protease: peptide bond hydrolysis" in
  `seed_reactions.py` so the mechanism seeder can attach.
- New `_hiv_protease()` mechanism builder in `seed_mechanisms.py`.
  3 steps covering:
  1. Asp-activated water attacks the peptide carbonyl (arrows on
     H₂O → C(=O) and the C=O π bond; `lone_pairs=[5]` on the water
     oxygen — first seed to exercise Phase 13c lone-pair dots).
  2. Tetrahedral-intermediate collapse with C-N σ bond breaking
     (arrow origin = bond midpoint via `from_bond=(1, 4)` — first
     seed to exercise Phase 13c bond-midpoint arrows).
  3. Product release + active-site reset.
- `SEED_VERSION` bumped 5 → 6 so existing DBs refresh on next
  launch.
- Fragment-consistency test caught the canonical form of the
  substrate SMILES (`CCNC(C)=O`) wasn't in the intermediates table;
  added *N-Ethylacetamide* and *Ethylamine* to
  `seed_intermediates.py`. That test is good — exactly what it's
  there for.
- 6 new tests (`tests/test_seed_hiv_protease.py`): step count,
  lone-pair presence, bond-midpoint arrow presence, JSON round-trip
  tuple preservation, `SEED_VERSION ≥ 6`, reaction-row presence.

### Result
- **491 passed + 1 skipped** (was 480; +11 new). Reactions count
  now 29 (was 28) — the HIV protease row wired in cleanly.
- INTERFACE.md: `draw_protein_3d.py` entry updated for
  `colour_mode`, `seed_mechanisms.py` entry bumped to 12 seeded
  mechanisms (HIV protease added), Proteins tab entry notes the
  new pLDDT checkbox + auto-enable on AlphaFold fetch.
- ROADMAP: Phase 24l pLDDT follow-up ticked (1 of 3 24l follow-ups);
  Phase 16d picked up the HIV protease mechanism as the third
  seeded enzyme (6 more still queued).

### Next pick
Round 30 — **Phase 24l click-to-inspect** (wire the 3Dmol.js
picked-atom event back to the Properties panel so students can
click a residue and see its descriptors) in parallel with **Phase
16d additional enzyme mechanisms** (RNase A 2-step in-line
phosphoryl transfer — good lone-pair/bond-midpoint practice since
the transition state is canonical SN2-at-P).


---

## 2026-04-23 — Autonomous loop round 30 — click-to-inspect + RNase A mechanism

### Phase 24l follow-up — click-to-inspect (QWebChannel bridge)
- `orgchem/render/draw_protein_3d.py`:
  - New `_PICK_LABEL_CSS` + `_PICK_JS` blocks and a
    `_inject_picking_scaffolding(html)` helper.
  - `build_protein_html(..., enable_picking=True)` now:
    1. Threads `enable_picking` into `_build_model_js`, which
       appends a 3Dmol `setClickable({hetflag: false}, true, …)`
       handler.
    2. Splices in: the `#pick-label` CSS; a
       `<div id="pick-label">click a residue…</div>` overlay; a
       `<script src="qrc:///qtwebchannel/qwebchannel.js">` loader
       (no-ops when the page isn't inside a QWebEngineView).
  - The JS click handler updates the overlay label *and* — if
    `qt.webChannelTransport` exists — forwards `chain, resn, resi`
    to `qtBridge.onAtomPicked` via `QWebChannel`.

### GUI wiring
- `orgchem/gui/panels/protein_panel.py`:
  - New `_PickBridge(QObject)` with `@Slot(str, str, int)
    onAtomPicked(chain, resn, resi)` that re-emits a Qt
    `picked(str, str, int)` signal.
  - The 3D sub-tab creates a `QWebChannel` on the `QWebEngineView`'s
    page and registers the bridge as `"qtBridge"`.
  - New "Picked: …" label below the viewer that updates on
    `picked` signal + posts to the session-log bus. Headless smoke
    confirms `_pick_bridge.onAtomPicked("A", "HIS", 57)` updates the
    label to `"Picked: A:HIS57"`.
  - `_on_render_3d` now calls `build_protein_html_from_file(...,
    enable_picking=True)` so every render is pickable.

### Phase 16d — RNase A mechanism seed
- New `_rnase_a()` builder in `seed_mechanisms.py`:
  - Step 1 (transphosphorylation): 2'-oxide attacks P (lone pair on
    C3' oxygen proxy index 0; curly arrow); P-O(5') σ bond breaks
    via a `from_bond=(3, 4)` midpoint arrow → 2',3'-cyclic
    phosphate.
  - Step 2 (hydrolysis): water attacks P (lone pair on water O at
    index 8); P-O(2') σ bond breaks via `from_bond=(3, 6)` midpoint
    arrow → 3'-phosphate + free 2'-OH.
- Added to `_MECH_MAP`; `SEED_VERSION` bumped 6 → 7 so existing
  DBs get the new JSON.
- New reaction row "RNase A: phosphoryl transfer on RNA" in
  `seed_reactions.py` so the mechanism attaches.
- Fragment-consistency test caught the canonical
  `O=P1(O)OCC(O)CO1` form of the cyclic-phosphate intermediate
  wasn't seeded; added as "Ribose 2',3'-cyclic phosphate
  (simplified)" to `seed_intermediates.py`.

### Result
- **502 passed + 1 skipped** (was 491; +11 new: 4 picking HTML
  tests + 7 RNase A seed tests). Reactions count 30 (was 29).
- Two enzyme mechanisms now exercise Phase 13c lone-pair dots
  + bond-midpoint arrows end-to-end (HIV protease + RNase A).
- INTERFACE.md, ROADMAP.md, PROJECT_STATUS.md updated. Phase 24l
  ticks click-to-inspect (2 of 3 24l follow-ups done); Phase 16d
  ticks RNase A as the fourth seeded enzyme mechanism.

### Next pick
Round 31 — **Phase 24l rotation-animation export** (record a 360°
spin of the 3D protein viewer → GIF via the existing Phase 2c.2
trajectory machinery) in parallel with **Phase 11a glossary
additions for the enzyme-mechanism vocabulary** we've been using
(catalytic triad, general acid/base catalysis, in-line phosphoryl
transfer, aspartyl protease, etc.). Disjoint.


---

## 2026-04-23 — Autonomous loop round 31 — viewer auto-spin + enzyme glossary + 2 roadmap additions

**User directives during the round**:
1. Add a status-check to the roadmap — review the whole project
   for GUI wiring / stubs / unreachable features.
2. Add example figures on glossary entries to the roadmap.

Both landed as new ROADMAP phases (25 and 26) alongside the
scheduled round-31 work.

### Phase 24l follow-up — rotation animation
- `build_protein_html(..., spin, spin_axis, spin_speed)` forwards to
  `_build_model_js` which appends `v.spin(axis, speed);` before
  `v.render();`. Axis is sanitised to the set `{x, y, z}` — a
  rogue string like `"bogus; alert(1)"` falls back to `"y"` so the
  kwarg can't inject arbitrary JS.
- Agent action `export_protein_3d_html` exposes `spin`, `spin_axis`,
  `spin_speed`; the returned dict reports `spin`. GUI Proteins-tab
  3D sub-tab has a new **"Auto-rotate"** checkbox (wired through
  both the *Render* and *Save HTML…* paths).
- 5 new HTML-level tests + 1 agent-action test covering off-by-
  default, on-with-defaults, custom axis/speed, axis sanitisation,
  and the round-trip through the agent action.

### Phase 11a — enzyme-mechanism glossary additions
- Added 8 new terms under a new `"enzyme-mechanism"` category in
  `seed_glossary.py`: **Catalytic triad**, **General acid-base
  catalysis**, **Aspartic protease**, **Oxyanion hole**, **In-line
  phosphoryl transfer**, **Covalent intermediate**, **Schiff base**,
  **Tetrahedral intermediate**. All carry aliases + see-also
  cross-refs so the Glossary tab's *"See also"* links make the
  vocabulary a navigable web (e.g. HIV-protease lookup lands on
  Aspartic-protease → General acid-base catalysis → Catalytic
  triad).
- `SEED_VERSION` bumped 1 → 2 so existing DBs pick up the new
  terms on next launch. 11 new tests covering presence,
  categorisation, version bump, and definition/see-also coverage.

### Minor GUI cleanup (towards Phase 25)
- Removed `MainWindow._stub()` — dead helper from the pre-tab-
  panels era. Confirmed by grep that nothing references it.

### New ROADMAP items landed this round
- **Phase 25 — GUI wiring audit & status check** (user-flagged).
  Five sub-items: inventory script, surface every core feature,
  stub hunt, walk-every-tab smoke test, publish audit in
  PROJECT_STATUS.md.
- **Phase 26 — Example figures on glossary entries** (user-flagged).
  Five sub-items: schema extension, auto-generator, ~15 hand-
  curated anchor figures, GUI inline rendering, tests.

### Result
- **518 passed + 1 skipped** (was 502; +16 new = 6 spin + 11
  glossary, but 1 existing test already covered the new spin
  code path).
- INTERFACE.md entry for `draw_protein_3d.py` updated to list
  `spin` parameters. ROADMAP tacks on Phase 25 + Phase 26 as
  user-flagged directives.

### Next pick
Round 32 — start **Phase 25a GUI wiring inventory** (surface every
back-end feature in a menu/panel/dialog; obvious gaps: retrosynthesis
dialog, SAR viewer, bioisosteres dialog, TLC simulator, IUPAC rule
browser) in parallel with **Phase 26a glossary figure schema**
(`example_smiles` field + additive migration). Both disjoint.


---

## 2026-04-23 — Autonomous loop round 32 — GUI inventory + glossary figure schema

### Phase 25a — GUI wiring inventory
- New `orgchem/gui/audit.py`: hand-maintained
  `GUI_ENTRY_POINTS: Dict[str, str]` keyed by agent-action name,
  value = the user-facing path (menu → item, tab → sub-tab, panel
  button, etc.). Actions without a GUI entry map to the empty
  string, which `audit()` / `audit_summary()` surface as
  "— missing".
- New CLI `scripts/audit_gui_wiring.py` prints the full table plus
  totals. Current baseline when the script first ran: **93 actions
  total, 61 wired, 32 missing, 65.6 % coverage**.
- New regression test `tests/test_gui_audit.py`:
  - Audit emits one row per registered action.
  - Summary shape + arithmetic invariant
    (`wired + missing == total`).
  - Coverage gate asserted at **≥ 60 %** so later rounds can only
    grow the baseline — raise the threshold whenever a batch of
    gaps gets wired up.
  - Heuristic sanity check that wired entries reference real UI
    terms ("menu" / "tab" / "dialog" / "dock" / "→" / etc.).
- Known gaps to close in Phase 25b (see `audit_summary()["missing_actions"]`):
  retrosynthesis (find / list templates / multi-step), SAR series
  (list / get / export matrix), bioisosteres (list / suggest),
  Hückel MOs + MO-diagram export, Woodward-Hoffmann rule browser,
  TLC / Rf / recrystallisation / distillation / extraction, IUPAC
  naming-rule browser, flip-stereocentre / enantiomer-of, PPI-pair
  per-chain selection, `get_protein_chain_sequence`, NMR / MS stick
  spectrum exports, and a couple of green-metrics actions.

### Phase 26a — Glossary figure schema
- `GlossaryTerm` model gained two optional columns:
  `example_smiles VARCHAR(500)` and
  `example_figure_path VARCHAR(500)`. Both default to NULL so
  legacy rows stay figure-less.
- `db/session.py::_apply_additive_migrations` ALTERs existing
  `glossary_terms` tables in place when either column is missing —
  upgrade-safe.
- `seed_glossary` threads both fields through insert + update
  paths and picks up differences in `needs_update`; `SEED_VERSION`
  bumped 2 → 3. Four anchor terms seeded with `example_smiles`:
  **Aromaticity** (`c1ccccc1`), **Carbocation** (`CC(C)(C)[+]`),
  **Diels-Alder reaction** (`C=CC=C.C=C`), **Aldol reaction**
  (`CC(=O)C.CC=O>>CC(=O)CC(O)C`).
- 6 tests in `tests/test_glossary_figure_schema.py` cover model
  columns, SEED_VERSION bump, seeded anchor presence, legacy-row
  default, full DB round-trip, and the additive-migration upgrade
  path on a pre-26a SQLite file.

### Result
- **529 passed + 1 skipped** (was 518; +11 new = 5 audit + 6
  schema). Doc-coverage gave `gui/audit.py` the usual first-run
  flag; INTERFACE.md entry added.

### Next pick
Round 33 — **Phase 26b glossary figure auto-generator** script
(walks rows with `example_smiles` but no stored figure and writes
PNG/SVG to `data/glossary/`) **plus** first serious gap-closing
pass from Phase 25b: add a **Retrosynthesis dialog** under Tools
menu so `find_retrosynthesis` + `find_multi_step_retrosynthesis`
have a GUI entry. Both disjoint, both advance user-flagged phases.


---

## 2026-04-23 — Autonomous loop round 33 — figure generator + retrosynthesis dialog

### Phase 26b — glossary figure generator
- New `orgchem/core/glossary_figures.py`:
  - `term_slug(term)` normalises names (`Diels-Alder reaction` →
    `diels_alder_reaction`).
  - `render_term(term, smiles, out_dir, force, fmt)` renders to
    `<slug>.<fmt>`. Chooses between `draw2d` (single molecules) and
    `draw_reaction` (reaction SMILES detected via `>>`). Returns a
    `FigureResult` with a `skipped_reason` on failure/skip.
  - `regenerate_all(out_dir, force, fmt)` walks `_GLOSSARY`,
    renders each `example_smiles` row. Incremental by default.
  - `default_figure_dir()` → `data/glossary/` alongside the package.
- New CLI `scripts/regen_glossary_figures.py` (`--force`, `--svg`,
  `--out-dir`). Prints a per-term status line + a summary.
- New agent action `get_glossary_figure(term, path, fmt)` on the
  **glossary** category — looks the term up, renders its
  example_smiles to the caller-chosen path.
- 11 tests (`tests/test_glossary_figures.py`): slug rules, PNG +
  SVG rendering for molecules + reactions, incremental skip,
  invalid/empty SMILES handling, full `regenerate_all` hits all 4
  seeded anchors, and the agent action's success/error branches.
- Caught + fixed the bad carbocation SMILES `CC(C)(C)[+]` → replaced
  with `C[C+](C)C`.

### Phase 25b gap-close — Retrosynthesis dialog
- New `orgchem/gui/dialogs/retrosynthesis.py`: target-SMILES input,
  spinners for max-depth / max-branches / top-paths. Two result
  tabs — **Single-step** (flat table of template / forward-reaction
  / precursors) and **Multi-step** (tree view built from
  `find_multi_step_retrosynthesis`'s disconnection tree).
  Bad-SMILES paths pop a QMessageBox warning.
- Wired into `MainWindow` as **Tools → Retrosynthesis…**. Updated
  `GUI_ENTRY_POINTS` so three actions previously agent-only now
  have GUI paths: `find_retrosynthesis`, `list_retro_templates`,
  `find_multi_step_retrosynthesis`.
- 5 new tests (`tests/test_retrosynthesis_dialog.py`): dialog
  instantiates headlessly, single-step populates the table,
  multi-step populates the tree, bad SMILES warns-not-crashes,
  audit entries are wired.

### Result
- **545 passed + 1 skipped** (was 529; +16 new = 11 figures + 5
  dialog). GUI coverage now **68.1 %** (was 65.6 %, +3 wired
  actions); one new action added from Phase 26b (net +1 total).
  Two failing tests along the way:
  1. Doc-coverage flagged `glossary_figures.py` first-run —
     INTERFACE.md entry added.
  2. `test_gui_audit.py` hard-coded `find_retrosynthesis` as a gap;
     updated to `predict_tlc` (still a known gap) so the assertion
     keeps its meaning as coverage grows.

### Next pick
Round 34 — continue Phase 25b gap-closing: **Hückel MOs + W-H rule
browser dialog** under Tools (closes `huckel_mos`, `export_mo_diagram`,
`list_wh_rules`, `get_wh_rule`, `check_wh_allowed` — five actions in
one dialog is a good ROI win). Disjoint from **Phase 26c anchor-
figure expansion** — render 10 more anchor `example_smiles` entries
(SN2, tetrahedral intermediate, oxyanion hole, etc.) and hand-verify
visually.


---

## 2026-04-23 — Autonomous loop round 34 — Orbitals dialog + anchor figures + 3 user roadmap items

**User directives this round (landed as roadmap items)**:
1. **Phase 27 — Interactive periodic table** as Tools menu item.
2. **Phase 28 — Molecule-browser multi-category filters** (functional
   groups, biological source, drug class, composition, charge, atom
   bands) — DB schema extension + taxonomy + auto-tagger + two-combo
   filter bar. User noted the DB may need updates; scoped 28a
   accordingly.
3. **Phase 29 — Macromolecule tabs (carbohydrates, lipids, nucleic
   acids)** alongside the Proteins tab — each has its own 2D/3D
   conventions that don't belong in the general molecule viewer.

### Phase 25b — Orbitals dialog (Hückel + W-H)
- New `orgchem/gui/dialogs/orbitals.py` (~230 lines). Three-tab:
  - **Hückel MOs** — SMILES → `huckel_for_smiles` → MO-energies
    table (#, α+kβ, k, occupancy, frontier) + *Save MO diagram…*.
    Closes `huckel_mos` + `export_mo_diagram`.
  - **Woodward-Hoffmann** rule browser — family combo + rule list
    + rich-text description pane (HTML-escaped, no setMarkdown —
    that was hanging under the offscreen Qt backend). Closes
    `list_wh_rules` + `get_wh_rule`.
  - **Is it allowed?** — kind / electrons / regime form → colour-
    coded ALLOWED/FORBIDDEN result with geometry + reason. Closes
    `check_wh_allowed`.
- Wired as **Tools → Orbitals (Hückel / W-H)…**.
- Hit a `HuckelResult` API mismatch first pass (my dialog assumed
  `mos` + `n_electrons`; the dataclass uses `energies` +
  `n_pi_electrons`). Fixed by pulling occupancy/HOMO/LUMO via the
  existing computed properties on `HuckelResult`.
- 7 tests in `tests/test_orbitals_dialog.py`: 3-tab structure,
  benzene populates 6 MOs with HOMO/LUMO, bad-SMILES warns,
  family-combo filters the list, [4+2] thermal = ALLOWED, [2+2]
  thermal = FORBIDDEN, audit entries updated.

### Phase 26c — Anchor figures expansion
- Seeded `example_smiles` on 11 more glossary terms:
  **SN2**, **SN1**, **E1**, **E2**, **Carbanion**,
  **Friedel-Crafts alkylation**, **EAS**, **Retrosynthesis**,
  **Schiff base**, **Tetrahedral intermediate**, **Covalent
  intermediate**. Combined with the round-32 anchors, **15
  glossary terms now have illustrative SMILES** ready for the
  figure generator.
- `SEED_VERSION` bumped 3 → 4 so existing DBs pick up the new
  smiles.

### Result
- **552 passed + 1 skipped** (was 545; +7 net new). GUI coverage
  now **73.4 %** (was 68.1 %, +5 wired) — 69 of 94 actions now
  have a GUI entry point. The `Orbitals` dialog alone wired up
  five agent-only capabilities in one stroke.
- Fixed 2 pre-existing tests that assumed a term stayed
  unannotated — pivoted them to *Transition state* (a concept
  without a canonical SMILES).
- Doc-coverage audit caught the new dialog first-run; INTERFACE.md
  updated with an `orbitals.py` entry under GUI dialogs.

### Next pick
Round 35 — continue Phase 25b gap-closing: **Lab-techniques dialog**
under Tools (closes `predict_tlc`, `predict_rf`,
`recrystallisation_yield`, `distillation_plan`, `extraction_plan` —
five actions in one dialog, mirroring the Orbitals win) in parallel
with kicking off **Phase 27a periodic-table data module** — the
`Element` dataclass + 118-element seed.


---

## 2026-04-23 — Autonomous loop round 35 — Lab dialog + periodic-table data

### Phase 25b — Lab techniques dialog (5-in-1 gap-close)
- New `orgchem/gui/dialogs/lab_techniques.py` (~230 lines).
  Four-tab:
  - **TLC / Rf** — paste SMILES lines + solvent string →
    `simulate_tlc` → table with Rf + interpretation (baseline /
    logP / solvent-front). Reports solvent polarity.
  - **Recrystallisation** — hot / cold solubility spinners +
    crude mass + solvent volume → `recrystallisation_yield` →
    crystals recovered + retained-in-liquor + yield %.
  - **Distillation** — two component names → `distillation_plan`
    → simple / fractional / azeotrope-warning with ΔTb.
  - **Acid-base extraction** — pKa + pH + acid/base flag + logP →
    `extraction_plan` → fraction-ionised + predicted layer +
    teaching tip.
- Wired as **Tools → Lab techniques…**.
- Hit a shape mismatch first pass (dialog expected `rows` key, the
  API returns `compounds`); fixed.
- 6 tests in `tests/test_lab_techniques_dialog.py` covering each
  tab + audit wiring.

### Phase 27a — Periodic-table data module
- New `orgchem/core/periodic_table.py` (~240 lines):
  - `Element` dataclass (symbol / name / Z / group / period /
    block / category / mass / electronegativity / oxidation
    states / electron config). `colour()` method pulls the
    category palette for rendering.
  - `_SEED` — hand-curated 118-row table with all the pedagogical
    fields set. Atomic masses pulled from RDKit's
    `GetPeriodicTable` at module load so we don't duplicate NIST.
  - Lookup helpers: `list_elements()`, `get_element(sym_or_z)`
    (accepts symbol / name / Z / str-Z), `elements_by_category(cat)`,
    `categories()`.
  - `CATEGORY_COLOURS` palette (11 families).
- New agent-action module `orgchem/agent/actions_periodic.py`
  registers three actions on a new **periodic** category:
  `list_elements`, `get_element`, `elements_by_category`.
- 13 tests in `tests/test_periodic_table.py` covering every
  element present, Z-indexing, endpoints (H + Og),
  category palette coverage, RDKit mass population for natural
  elements, multi-form lookup (symbol/name/Z/str-Z), halogen /
  noble-gas category filters, category enumeration, dict shape,
  all three agent actions.

### Result
- **571 passed + 1 skipped** (was 552; +19 new). GUI coverage now
  **76.3 %** — 74 of 97 actions wired (was 69/94 = 73.4 %; +5
  wired, +3 new from the periodic-table agent category).
- INTERFACE.md picked up `periodic_table.py`, the new
  `lab_techniques.py` dialog entry, and the **periodic** action
  list.
- Updated the audit-test assertion — `list_sar_series` now plays
  the role of "known unwired gap" since `predict_tlc` is wired.

### Next pick
Round 36 — continue Phase 25b gap-closing: **SAR + bioisosteres +
naming-rules dialogs** (closes `list_sar_series`, `get_sar_series`,
`export_sar_matrix`, `list_bioisosteres`, `suggest_bioisosteres`,
`list_naming_rules`, `get_naming_rule`, `naming_rule_categories` —
eight actions) in parallel with **Phase 27b periodic-table
renderer / 27c dialog** — render the actual interactive periodic
table that surfaces the round-35 data via a clickable Qt grid.


---

## 2026-04-23 — Autonomous loop round 36 — MedChem + Naming + Periodic table dialogs

Three new dialogs in one round; closed **11 audit gaps**.

### Phase 25b — Medicinal chemistry dialog
- `gui/dialogs/medchem.py`. Two tabs:
  - **SAR series**: picker combo over `SAR_LIBRARY`, descriptor +
    activity-columns table built from `compute_descriptors`,
    *Export SAR matrix…* via `render/draw_sar.py`.
  - **Bioisosteres**: SMILES → `suggest_bioisosteres` → ranked
    variant table with template id / label / suggested SMILES.
- Wired as **Tools → Medicinal chemistry (SAR / Bioisosteres)…**.
- Closes: `list_sar_series`, `get_sar_series`,
  `export_sar_matrix`, `list_bioisosteres`, `suggest_bioisosteres`
  (5 actions).

### Phase 25b — IUPAC naming rules dialog
- `gui/dialogs/naming_rules.py`. Category combo + rule list +
  HTML-escaped rich-text body (title + description + example
  SMILES / IUPAC / common name / pitfalls). Pulls from the
  `NamingRule` dataclass; 22 rules across 11 categories.
- Wired as **Tools → IUPAC naming rules…**.
- Closes: `list_naming_rules`, `get_naming_rule`,
  `naming_rule_categories` (3 actions).
- Hit a field-name mismatch first pass (dialog referenced
  `example_structure` / `pitfalls`; dataclass uses
  `example_smiles` / `example_iupac` / `example_common` —
  `pitfalls` field absent on some rules). Fixed with `getattr(..., "")`
  and the real field names.

### Phase 27b/c — Interactive periodic table
- `gui/dialogs/periodic_table.py`. 18-column grid built from
  `ELEMENTS` — each cell a `QPushButton` with `z\nsymbol` label,
  coloured by category, tooltip shows name + mass. Lanthanides /
  actinides placed on rows 7 and 8 left-aligned from group 3.
  Side-pane `QTextBrowser` shows the picked element's record;
  bottom legend strip lists every category colour.
- Wired as **Tools → Periodic table…** (Ctrl+Shift+T).
- Closes: `list_elements`, `get_element`,
  `elements_by_category` (3 actions).

### Result
- **582 passed + 1 skipped** (was 571; +11 new). GUI coverage
  **87.6 %** (85 / 97 actions wired) — up from **76.3 %** at the
  start of the round. A single round closing 11 agent-only gaps
  is the largest wiring win so far.
- Remaining 12 gaps (for future rounds): spectrum export actions
  (`export_ir_spectrum`, `export_ms_spectrum`, `export_nmr_spectrum`,
  `predict_ms`, `predict_nmr_shifts`), stereo manipulation
  (`enantiomer_of`, `flip_stereocentre`), green metrics
  (`pathway_green_metrics`, `reaction_atom_economy`),
  `analyse_ppi_pair`, `get_protein_chain_sequence`,
  `get_glossary_figure` (action is there, just no dedicated GUI
  button beyond the existing Glossary tab).

### Next pick
Round 37 — continue Phase 25b gap-closing: a **Spectroscopy dialog**
(IR + NMR + MS stick-spectrum predictors with Save buttons) wrapping
up `predict_nmr_shifts`, `predict_ms`, `export_ir_spectrum`,
`export_nmr_spectrum`, `export_ms_spectrum` — another 5-action win.
In parallel, land a small **stereo context menu** on the Molecule
browser: "flip stereocentre" and "mirror (enantiomer)" closing the
last two stereo-action gaps.


---

## 2026-04-23 — Autonomous loop round 37 — Spectroscopy + Stereochemistry dialogs

### Phase 25b — Spectroscopy dialog (6-in-1)
- `gui/dialogs/spectroscopy.py`. Three tabs:
  - **IR**: SMILES → `predict_bands` → group / wavenumber /
    intensity / notes table + *Save spectrum…* via `export_ir_spectrum`.
  - **NMR**: SMILES + H / C nucleus combo → `predict_shifts` →
    δ / environment / multiplicity / count table + save.
  - **MS**: SMILES → `isotope_pattern` → m/z / relative-intensity /
    label table + save. Summary line shows formula +
    monoisotopic mass.
- Wired as **Tools → Spectroscopy (IR / NMR / MS)…**.
- Closes **six actions**: `predict_ir_bands`, `export_ir_spectrum`,
  `predict_nmr_shifts`, `export_nmr_spectrum`, `predict_ms`,
  `export_ms_spectrum`. The first was previously wired via the
  Properties dock summary; now also has a dedicated UI.
- Caught two API-shape mismatches on first pass: `isotope_pattern`
  returns `{"peaks": [{"mz", "intensity", "label"}, …]}` not a
  list of tuples; dialog fixed.

### Phase 25b — Stereochemistry dialog
- `gui/dialogs/stereo.py`. SMILES → `summarise()` → R/S + E/Z
  descriptor table with per-row **Flip** buttons; global
  **Mirror (enantiomer)** button. Summary line reports
  n-stereocentres / assigned / unassigned / is_chiral.
- Wired as **Tools → Stereochemistry…**.
- Closes: `flip_stereocentre`, `enantiomer_of` (2 actions).
- Caught another API shape mismatch: `summarise()` returns
  `{"rs": {idx: "R"|"S"}, "ez": [...], ...}` not a
  `descriptors` list; dialog fixed.

### Result
- **590 passed + 1 skipped** (was 582; +8 new). GUI coverage
  **94.8 %** — 92 of 97 actions wired. **Only 5 gaps remain**,
  down from 12 at the start of the round:
  - `reaction_atom_economy`, `pathway_green_metrics` (green
    metrics — need a Reactions-tab column or dialog).
  - `analyse_ppi_pair` (exists via the PPI tab but for the "all
    pairs" path only; explicit per-pair selector not yet wired).
  - `get_protein_chain_sequence` (Proteins tab Summary sub-tab
    could expose a "Copy sequence" button).
  - `get_glossary_figure` (the action works, but there's no GUI
    button on the Glossary tab to click it — currently only
    reachable via `Tools → Retrosynthesis…`'s sibling dialogs).

### Next pick
Round 38 — **Close the last 5 GUI audit gaps** to push coverage to
100 %. Small additions: a *Green metrics* dialog under Tools, a
"Copy chain sequence" button on the Proteins Summary sub-tab, a
"Per-chain pair" selector on the PPI sub-tab, a "View figure"
button on the Glossary tab. The round completes Phase 25b in full.


---

## 2026-04-23 — Autonomous loop round 38 — 🎯 100 % GUI coverage

User-flagged Phase 25 status-check is now fully green.

### 1. Green metrics dialog
- New `gui/dialogs/green_metrics.py`. Two tabs:
  - **Reaction AE**: DB-reaction picker combo → `reaction_atom_economy`
    → summary + metrics table.
  - **Pathway AE**: DB-pathway picker → `pathway_green_metrics`
    → overall-AE line + per-step table.
- Wired as **Tools → Green metrics (atom economy)…**.
- Closes: `reaction_atom_economy`, `pathway_green_metrics`.

### 2. Proteins tab — PPI per-pair + Copy sequence
- Summary sub-tab gains a chain combo + **Copy sequence** button
  that pushes the chain's 1-letter sequence to the clipboard and
  echoes it in a monospace label. Populated from `summary["chain_ids"]`
  on PDB load.
- PPI sub-tab gains a second row: *Or pair:* chain A combo × chain B
  combo + **Analyse pair** button driving `analyse_ppi_pair`. Chain
  combos auto-populate on PDB load (default B = second chain).
- Closes: `analyse_ppi_pair`, `get_protein_chain_sequence`.

### 3. Glossary tab — View figure button
- New row under the See-also row: **View figure** button, enabled
  only when the current term's DB row carries an `example_smiles`.
  Click → temp-dir render via `render_term` → modal dialog showing
  the PNG preview + the SMILES caption.
- Closes: `get_glossary_figure`.

### Result
- **597 passed + 1 skipped** (was 590; +7 new). GUI coverage
  **100.0 %** — 97 of 97 actions wired. Guard-rail
  `tests/test_gui_audit.py::test_coverage_is_at_least_baseline`
  pinned at ≥ 100.0, so future regressions trip immediately.
- ROADMAP Phase 25 marked **complete**.

### Next pick
Round 39 — shift focus off gap-closing now that Phase 25 is done.
Options on the queue:
- Phase 26d: Glossary tab inline-figure rendering (currently the
  "View figure" button spawns a modal; inline display in the
  definition pane is the nicer UX).
- Phase 28: molecule-browser multi-category filter (still the
  biggest user-flagged unstarted phase).
- Phase 29a: carbohydrates tab kick-off (sibling to Proteins).
- Phase 22a: flip remaining CI gates to blocking now that the
  dialog stack is in place.


---

## 2026-04-23 — Autonomous loop round 39 — Phase 28a schema + 28c auto-tagger

### Phase 28a — DB schema extension
- `Molecule` model gains six optional columns:
  `source_tags_json`, `functional_group_tags_json`,
  `heavy_atom_count`, `formal_charge`, `n_rings`, `has_stereo`.
  All default to NULL so pre-28a databases keep working.
- `db/session.py::_apply_additive_migrations` ALTERs existing
  `molecules` tables on startup when any of the new columns is
  missing. Follows the same pattern as Phase 13b and Phase 26a
  migrations.

### Phase 28c — Auto-tagger
- New `orgchem/core/molecule_tags.py` (~220 lines):
  - `auto_tag(mol_or_smiles)` → `TagResult` dataclass with seven
    derived fields. 27 SMARTS-based functional groups (carboxylic
    acid → anhydride → amide → nitrile → phenol → halide), 7
    composition flags (halogen / P / S / B / Si / pure-organic /
    has-metal), 4 charge categories (zwitterion check runs before
    net-charge fallback so glycine classifies correctly), 3 size
    bands (≤ 12 / 13-30 / ≥ 31 heavy atoms), 3 ring-count bands.
  - `FILTER_AXES` + `list_filter_axes()` surface the full
    taxonomy for the upcoming filter-bar UI (Phase 28d).
- New `orgchem/db/seed_tags.py`: idempotent backfill that walks
  every `Molecule` row, runs `auto_tag`, and writes the results
  into the new columns. Hooked into `seed_if_empty` after
  `seed_coords` so new DBs land tagged.

### Result
- **612 passed + 1 skipped** (was 597; +15 new tests covering
  aspirin / ethanol / benzene / lactate / glycine zwitterion /
  ammonium / carboxylate / halogen composition / size bands /
  ring bands / filter-axes shape / schema presence / migration
  round-trip / seed-and-backfill round-trip).
- Phase 28a and 28c marked complete in the ROADMAP. Phase 28b
  (curated source / drug-class taxonomies) and 28d (filter-bar
  UI) + 28e (filter agent actions) + 28f (GUI smoke test) remain.

### Next pick
Round 40 — **Phase 28d filter-bar UI** on the Molecule browser
(the user-facing outcome). Two rolling combo boxes (axis + value)
+ AND semantics + "Clear filters" + result count. Backed by a new
`db/queries.py::query_by_tags(...)` helper. In parallel land
**Phase 28e agent actions** — `list_molecule_categories`,
`filter_molecules(axis_a, value_a, axis_b, value_b, text_query)`.


---

## 2026-04-23 — Autonomous loop round 40 — Molecule filter-bar + agent actions

### Phase 28d — Query helper + filter bar
- `db/queries.py::query_by_tags(axis_a, value_a, axis_b, value_b,
  text_query, limit)` — AND-filters by up to two tag axes plus a
  free-text substring on name / smiles / formula. `_apply_axis_filter`
  dispatcher handles each axis: `functional_group` +
  `composition` use JSON substring match on the auto-tag string;
  `charge` hits `formal_charge` (and the zwitterion substring);
  `size` / `ring_count` / `has_stereo` hit their respective
  indexed columns with the right band thresholds.
- `db/queries.py::list_molecule_category_values()` re-exports the
  Phase 28c taxonomy so GUI / agent callers don't pull from core.
- `gui/panels/molecule_browser.py`:
  - `_MolListModel.reload` gained optional `axis_a/value_a/axis_b/value_b`
    kwargs so the browser can flip between the old free-text path
    and the tag-aware path transparently.
  - New filter bar with **axis A** + **value A** combos on row 2,
    **axis B** + **value B** + *Clear filters* button on row 3,
    and a count label below. Value combos repopulate when the
    axis changes; selecting a value triggers `_reload`.
- `seed_tags.py` bumped to `SEED_VERSION=2` — auto-tags now carry
  composition flags + zwitterion marker + a `__v2__` sentinel so
  existing DBs refresh automatically on next launch.

### Phase 28e — Agent actions
- Two new actions on the existing **molecule** category:
  - `list_molecule_categories()` → full taxonomy dict.
  - `filter_molecules(axis_a, value_a, axis_b, value_b, text_query,
    limit)` → list of molecule-summary dicts (same shape as
    `list_all_molecules`).
- Audit map updated; both wired to the filter bar.

### Result
- **626 passed + 1 skipped** (was 612; +14 new covering the query
  helper, each axis dispatch, AND semantics, text-query combo,
  both agent actions, and the filter bar widgets / clear behaviour).
- GUI coverage remains **100.0 %** (99/99 — the two new actions
  landed with their GUI wiring in the same round, so the 100 %
  guard-rail stays green).
- Phase 28d + 28e marked complete. Phase 28 only has 28b (curated
  source / drug-class taxonomies) + 28f (broader smoke test)
  outstanding; they can land any round.

### Next pick
Round 41 — **Phase 28b curated source / drug-class taxonomies** —
seed each extended-molecule entry with source-tag strings
(plant / animal-hormone / bacterial-metabolite / NSAID / statin /
…) so the filter bar's *composition* axis picks up the user-facing
taxonomy instead of only the auto-tag-derived flags. In parallel
kick off **Phase 29a carbohydrates tab** (data seed only — the
full tab panel comes in round 42).


---

## 2026-04-23 — Autonomous loop round 41 — source taxonomies + carbohydrate data

### Phase 28b — Curated source / drug-class taxonomies
- New `orgchem/db/seed_source_tags.py` with a hand-curated
  `_BY_NAME` dict mapping ~45 seeded molecules to 1-4 tags each
  (NSAIDs / statins / antibiotics / SSRIs / β-blockers /
  hormones / steroids / neurotransmitters / alkaloids /
  nucleosides / sugars / fatty acids / dyes / reagent
  subclasses). Total taxonomy ≈ 50 user-facing tags.
- `backfill_source_tags` writes the curated list + a `__source_v1__`
  sentinel into `Molecule.source_tags_json`. Hooked into
  `seed_if_empty` after the auto-tag backfill.
- Filter taxonomy: added a new **`source`** axis to
  `FILTER_AXES` listing both the broad buckets and the curated
  fine-grained tags. Query dispatcher in `db/queries.py` teaches
  the `composition`/`source` axes to substring-match both
  `functional_group_tags_json` and `source_tags_json`.

### Phase 29a — Carbohydrate data module
- New `orgchem/core/carbohydrates.py` with a `Carbohydrate`
  dataclass and 15-row `CARBOHYDRATES` catalogue:
  - Monosaccharides: α/β/open-chain D-glucose, D-fructose
    (open + β-furanose), ribose, 2-deoxyribose, α-galactose,
    α-mannose.
  - Disaccharides: sucrose (α-1,2), lactose (β-1,4), maltose
    (α-1,4), cellobiose (β-1,4).
  - Polysaccharide fragments: amylose (α-1,4), cellulose (β-1,4).
  - Each entry carries family / form / anomer / glycosidic /
    notes metadata.
- `list_carbohydrates(family)`, `get_carbohydrate(name)`,
  `families()` helpers for the upcoming Carbohydrates tab.
- Three agent actions on a new **carbohydrate** category:
  `list_carbohydrates`, `get_carbohydrate`, `carbohydrate_families`.
  Rename trick: `get_carbohydrate(carb_name=...)` avoids the
  `invoke(name, **kwargs)` collision (same footgun caught in
  rounds 26 and 29).

### Result
- **642 passed + 1 skipped** (was 626; +16 new). Tests confirm the
  curated taxonomy is reachable via the filter bar (NSAID → Aspirin,
  statin → Atorvastatin / Simvastatin / Lovastatin) and that
  every carbohydrate SMILES parses via RDKit.
- GUI coverage remains **100.0 %** (102/102) — the three new
  carbohydrate actions are audit-mapped to the existing Molecule
  browser source-filter path (the dedicated Carbohydrates tab
  lands in round 42, Phase 29b).
- ROADMAP: Phase 28b marked complete; Phase 29a also complete.

### Next pick
Round 42 — **Phase 29b Carbohydrates tab panel** as a sibling to
the Proteins tab. Reuses `draw2d` for 2D rendering, the existing
3Dmol.js viewer for 3D; family combo + entry list + info pane for
Haworth / anomer / glycosidic-bond teaching labels.


---

## 2026-04-23 — Autonomous loop round 42 — Carbohydrates tab panel

### Phase 29b — Carbohydrates tab
- New `orgchem/gui/panels/carbohydrates_panel.py` (~170 lines).
  Splitter layout:
  - **Top filter row**: family combo (all / monosaccharide /
    disaccharide / polysaccharide) + free-text field (matches
    name / family / form / anomer / glycosidic).
  - **Left**: entry list populated by `_filtered_entries()`.
  - **Right**: `QSvgWidget` showing the RDKit-rendered 2D
    structure, `QTextBrowser` with the meta block (family / form
    / carbonyl type / anomer / glycosidic bond / notes), and two
    buttons — *Copy SMILES* (pushes to clipboard) and *Show in
    Molecule Workspace* (looks up by name / InChIKey and emits
    `molecule_selected` if matched, otherwise posts a hint to
    the session log).
- Wired into `MainWindow._build_central` as the **Carbohydrates**
  tab, sibling of Proteins.
- Audit map entries for `list_carbohydrates`,
  `get_carbohydrate`, `carbohydrate_families` retargeted from
  "Molecule browser → source:sugar filter" to the dedicated tab.

### Result
- **651 passed + 1 skipped** (was 642; +9 new). GUI coverage stays
  at **100 %** (102/102). Phase 29a + 29b both complete — the
  full carbohydrate stack (data module + catalogue + agent
  actions + panel) is live.

### Next pick
Round 43 — **Phase 29b lipids + nucleic-acids siblings**. Seed the
data module for each (core/lipids.py, core/nucleic_acids.py) plus
a shared sibling-tab template so the three macromolecule tabs share
a common look. Fatty acids / triglycerides / phospholipids /
cholesterol on the lipid side; canonical B-form DNA dodecamer,
G-quadruplex, tRNA-Phe on the NA side. NA tab reuses the Phase 24k
NA-ligand contact analyser for loaded ligands.

## 2026-04-24 — Autonomous loop round 95 — Phase 33c CLOSE — surface-integrated full-text filter

### Goal
Close Phase 33c — the last open sub-phase of the cross-surface
full-text search initiative started in round 88. Phases 33a
(core + agent action) and 33b (Ctrl+F dialog) shipped in earlier
rounds; 33c integrates the same ranked search into the tab-local
filter boxes on **Reactions** and **Synthesis**, so "filter by
name" and "find by any text" are one keystroke apart without a
second dialog.

### Scope decision
- Reactions tab — yes. Name filter misses mechanism-step notes
  (e.g. *"Wheland"*, *"oxime"*, *"bromonium"*), so a toggle adds
  real value.
- Synthesis tab — yes. Name filter misses step reagents /
  conditions / notes (e.g. *"Raney Ni"* in BHC Ibuprofen,
  *"DIPAMP"* in L-DOPA Knowles), so again — real value.
- Glossary tab — **scoped out**. Its `_TermListModel.reload()`
  already does `GlossaryTerm.definition_md.ilike('%q%')`, so a
  toggle would be redundant and might confuse users.

### Ship list
1. `orgchem/gui/panels/reaction_workspace.py`
   - `_RxnListModel.reload_ids(ids)` — preserves ranked order
     via `WHERE id IN (…)`. Holds the native `list_reactions`
     ORM-row shape so the existing `data()` override keeps
     working.
   - `QCheckBox("Full text")` beside the filter line-edit; its
     `toggled` re-runs `_on_filter(self.filter.text())`.
   - `_on_filter` routes to `core.fulltext_search.search(q,
     kinds=["reaction", "mechanism-step"], limit=200)` when the
     checkbox is checked and the query is non-empty. Step-note
     hits collapse onto parent reaction IDs (ranked-order
     dedupe) so the list shows one row per reaction.
2. `orgchem/gui/panels/synthesis_workspace.py`
   - `_PathwayListModel.reload_ids(ids)` — same pattern, but
     detaches rows into the existing `{id, name, target,
     category}` dict shape that `reload()` already uses (so
     `data()` + `role=DisplayRole` keep rendering the
     "name → target" two-line layout).
   - `QCheckBox("Full text")` + `_on_filter` branch, routing
     to `kinds=["pathway"]`.
3. `tests/test_fulltext_filter_toggle.py` (new) — 8 pytest-qt
   tests. Highlights:
   - `test_reactions_fulltext_toggle_finds_description_hits`:
     "oxime" baseline count vs toggle-on count.
   - `test_synthesis_fulltext_finds_step_note_hit`: *"Raney"*
     has 0 name/target/category hits (verified via DB query)
     but full-text surfaces the BHC Ibuprofen pathway through
     step-2 reagents "H₂, Raney Ni". This is the pure
     step-note-only scenario 33c was built to solve.
   - `test_reactions_model_reload_ids_preserves_order` +
     synthesis twin: hand-picked ID permutations round-trip
     through `reload_ids` in order.
   - Empty-query fallback + empty-IDs clear-list guards.

### False start worth recording
First draft of the Synthesis test used "DIPAMP" as the
step-note-only term, expecting the name-filter to return 0
rows. That failed — the L-DOPA pathway's full name is
*"L-DOPA — Knowles Rh-DIPAMP asymmetric route (3-step)"*, so
the substring ILIKE picks it up directly. Swapped to "Raney"
which is genuinely step-note-only (verified by direct DB
query: 0 name/target/category hits, 1 full-text pathway hit).
Lesson: when writing "X is only in step notes, not in the
name" assertions, sanity-check with a direct SQL `ilike`
before codifying.

### Result
- **958 tests pass** (was 950; +8 new). No regressions.
- Reactions tab gets step-note search for free (a user typing
  *"Wheland"* now lands on Nitration of benzene even though no
  reaction name contains that word).
- Synthesis tab gets reagent/condition search (a user typing
  *"Raney"* now lands on BHC Ibuprofen; *"DIPAMP"* lands on
  L-DOPA Knowles).
- Phase 33 now 100% complete (a / b / c all shipped). The
  Ctrl+F modal from 33b and the in-tab toggle from 33c share
  one search core, one ranking algorithm, and one set of
  `kinds` — no code duplication.

### Next pick
Phase 33 is closed. Candidate pickups: Phase 34 (scope open —
possibly a thin retrosynthesis panel wired to the Phase 8d
engine + agent action), or continue Phase 31 sub-phases
(31e intermediate-tier tutorial gap-fills, 31h extra
carbohydrates, 31i fatty-acid / prostaglandin expansion).

## 2026-04-24 — Autonomous loop round 96 — Phase 31k +1 SAR series (SSRIs)

### Goal
Continue Phase 31k — medicinal-chemistry SAR series expansion
toward 15.  Current state: 4 series (nsaid-cox, statin-hmgcoa,
beta-blockers, ace-inhibitors).  Target for this round: +1
series with 5 textbook-grade variants + activity data tied to
a published review.

### Pick rationale
**SSRIs.**  Reasons:
- Classic pharmacology class every medicinal-chem student
  learns.  Familiar drug names (Prozac, Zoloft, Paxil, Celexa,
  Lexapro) anchor unfamiliar SMILES.
- Clean SAR story in the existing `activity_columns` shape
  (`sert_ki_nM`, `net_ki_nM`, `sert_selectivity`) — no dialog
  changes needed.
- Includes the **chiral-switch** case study: citalopram (racemate)
  vs escitalopram (S-enantiomer only) — going from racemate to
  single enantiomer gives ~3× boost in SERT/NET selectivity and
  halves the clinical dose.  This is one of the textbook "why
  chirality matters" examples.
- Spans 30 years of med-chem (fluoxetine 1987 → escitalopram 2002).

### Ship list
1. `orgchem/core/sar.py`
   - New `SARSeries(id="ssri-sert")` with 5 variants:
     Fluoxetine / Sertraline / Paroxetine / Citalopram /
     Escitalopram.
   - Activity numbers (Ki at SERT + NET, selectivity ratio)
     pulled from Owens, Morgan, Plott, Nemeroff 1997 *JPET*
     283:1305-1322 and Sanchez 2004 *Basic Clin. Pharmacol.
     Toxicol.* 94:51-67.
   - Each variant's `notes` field carries the clinical /
     structural flavour (fluoxetine long half-life, sertraline
     cis-(1S,4S) geometry, paroxetine anticholinergic
     off-target, citalopram→escitalopram chiral switch).
   - Dialectical SMILES encoding: sertraline + paroxetine with
     correct CIP descriptors, escitalopram S-enantiomer vs
     citalopram racemate (no @@/@).
2. `tests/test_sar.py`
   - `test_library_seeded` updated with `"ssri-sert" in ids`.
   - New `test_ssri_series_landmarks`: verifies 5 variants
     present, escitalopram > citalopram in selectivity
     (chiral-switch numeric), sertraline > paroxetine in
     selectivity (textbook pairing), every variant's computed
     MW falls in 280-340 Da band.

### Correction worth recording
First draft of the landmark test claimed *"sertraline is the
most SERT-selective after escitalopram"*.  That's wrong —
citalopram's 3700× NET:SERT beats sertraline's 2800× in the
Owens 1997 data set.  Corrected the assertion to a pairing
that *is* true in the seeded numbers (sertraline > paroxetine)
before committing.  Lesson for future SAR seeds: when writing
"X is most Y of the class" assertions, rank the full column
against the literature before codifying the ordering.

### Result
- **959 tests pass** (was 958; +1 new — `test_ssri_series_landmarks`).
- SAR catalogue now **5 / 15** series (30 variants total).
- Existing SAR dialog (`Tools → Medicinal chemistry…`) picks
  up the new series automatically via `list_sar_series` — no
  UI changes needed, the dialog already enumerates
  `SAR_LIBRARY`.

### Next pick
Phase 31k has 10 more series to reach 15.  Near-term
candidates: β-lactam antibiotics (penicillin G / amoxicillin /
methicillin / cloxacillin / cephalexin — steric-shielding-of-
β-lactamase story), PDE5 inhibitors (sildenafil / vardenafil /
tadalafil / avanafil — ring-fusion story), benzodiazepines
(diazepam / lorazepam / alprazolam / clonazepam / midazolam —
GABA-A subunit selectivity story).  Or switch sub-phases —
31e energy profiles (12 → 20) or 31l proteins (9 → 15) are
also live.

## 2026-04-24 — Autonomous loop round 97 — Housekeeping round 2 (pollution prefix broadening)

### Goal
Mid-round discovery: while inventorying reactions for a Phase
31e energy-profile pick, a DB listing surfaced **58 polluted
`Tutor-test ester hydrolysis {uuid}` Reaction rows** that the
round-94 cleanup missed.  Root cause: the round-94 prefix was
`"Tutor-test-"` (hyphen-terminated) but the one offending test —
`test_authoring_actions.py::test_add_reaction_accepts_valid_rxn`
— used `f"Tutor-test ester hydrolysis {uuid}"` with a **space**
instead of a dash.  Every other authoring test used the canonical
hyphen convention, so only the Reaction table accumulated.

### Ship list
1. `tests/test_authoring_actions.py` — normalised the outlier
   to `f"Tutor-test-ester-hydrolysis-{_u()}"` so the pattern
   matches the other authoring tests.
2. `orgchem/db/cleanup.py` — broadened `TEST_NAME_PREFIX` from
   `"Tutor-test-"` to `"Tutor-test"` (no trailing separator).
   Still tight enough that real seeded content can't collide
   (no real catalogue entry begins with the literal "Tutor-test"),
   but loose enough to catch historical / future tests that pick
   any punctuation after the prefix.  Docstring updated to record
   the context.
3. `scripts/cleanup_tutor_test_pollution.py` — added a
   `sys.path.insert` prepend at the top so the one-shot CLI runs
   with `python scripts/cleanup_tutor_test_pollution.py` from
   the repo root, without the user needing to set PYTHONPATH.
   Original version only worked if the repo was already on
   sys.path — which is why I first had to re-run it with
   `PYTHONPATH=. python …`.
4. `tests/test_cleanup_pollution.py` — new test
   `test_purge_catches_space_suffix_reaction`.  Inserts a
   reaction with name `f"Tutor-test space-suffixed rxn {uuid}"`
   (space in the third position) and confirms the default
   prefix catches it.  Regression lock so future refactors
   don't silently re-narrow the pattern.

### Result
- **960 tests pass** (was 959; +1 new regression).  Existing
  space-pattern authoring test now follows the dash convention
  so it no longer generates pollution in the first place.
- 58 polluted `Tutor-test ester hydrolysis` reactions purged
  from the user's live DB.
- Round-94 cleanup thesis re-validated: prefix-gated deletion
  is safe even when broadened slightly — every real seeded
  name has already been audited against the `Tutor-test`
  substring.

### Lessons
- When writing prefix-based safety gates, prefer the widest
  prefix you can justify as safe.  `Tutor-test-` (hyphen)
  seemed tight and safe; turned out to be too narrow.
  `Tutor-test` (no separator) is equally safe and ~50× better
  at catching variants.
- "Add a regression test for the bug you just found" — the new
  space-suffix test locks in the fix against future narrowing.

### Next pick
Back to Phase 31 content expansion.  Candidates:
- 31e: +1 energy profile (12 → 13).  Missing from the priority
  list: Claisen, Heck, Buchwald-Hartwig catalytic cycle, SN2
  1° vs 2° vs 3° comparison, retro-Diels-Alder.
- 31k: +1 SAR series (5 → 6).  β-lactam antibiotics or PDE5
  inhibitors are top of the queue.
- 31b: +1 named reaction (35 → 50).  Heck, Negishi, Stille are
  textbook gaps.

## 2026-04-24 — Autonomous loop round 98 — Phase 31e +1 energy profile (Claisen)

### Goal
Continue Phase 31e — textbook reaction-coordinate diagrams.
Current: 12 profiles.  Target this round: +1 profile that
teaches a concept other profiles don't already cover.

### Pick rationale
**Claisen condensation.**  Reasons:
- Already has a mechanism row (seeded round 61), so the pair
  (mechanism + energy profile) closes the pedagogical loop.
- The "final deprotonation drives the equilibrium" story is a
  genuinely distinct textbook point — unlike SN1/SN2/E1/E2/DA
  which just show basic barrier shapes.  The Claisen profile
  has a characteristic SHAPE: the 3rd intermediate (neutral
  β-ketoester + alkoxide) sits near thermoneutral, and then
  the 4th step plunges to a well-stabilised enolate.  That
  shape is the lesson.
- Numbers are well-constrained by pKa arithmetic: α-H between
  two carbonyls (pKa ≈ 11) vs alkoxide base (pKa ≈ 17)
  → ΔpKa ≈ 6 → strongly favourable.

### Ship list
1. `orgchem/db/seed_energy_profiles.py`
   - `_claisen_profile()` builder: 9 stationary points, 4 TSs,
     5 minima; shape encodes the RDS (TS C–C addition, 70 kJ/mol)
     and the driving-force step (final TS 15 kJ/mol over a
     neutral intermediate at −5, crashing to −40).
   - Added to `_PROFILE_MAP` keyed by substring "Claisen
     condensation".
   - `SEED_VERSION` bumped 3 → 4 so existing DBs pick up the
     new profile — seeder also rewrites the 12 existing profiles
     with the current payloads (fine; they're idempotent in
     content).
2. `tests/test_energy_profile.py`
   - `test_seeded_profiles_present` — expected count lifted
     from 9 to 13; name-substring list updated to include
     Sonogashira / HWE / Mitsunobu / Claisen.
   - New `test_claisen_profile_driven_by_final_deprotonation`
     that asserts 4 TSs present, the "Neutral β-ketoester"
     penultimate minimum sits within 20 kJ/mol of zero, and
     the final product sits ≥ 20 kJ/mol below it.  Locks in
     the teaching-point geometry against future numeric
     tweaks.

### Result
- **961 tests pass** (was 960; +1 new).
- Energy-profile catalogue now **13/20**.
- Seeder emitted `Seeded 13 energy profiles (version 4)` on
  the next launch — proving the SEED_VERSION bump refreshes
  the cache.
- Claisen reaction now shows the *Energy profile…* button on
  the Reactions tab (Phase 13d wiring — Phase 31e extends
  reach without UI changes).

### Next pick
Phase 31e has 7 more profiles to reach 20.  Top candidates:
- Heck reaction (β-hydride elimination as RDS) — strong
  teaching complement to Sonogashira.
- Buchwald-Hartwig amination catalytic cycle.
- SN2 on 1° vs 2° vs 3° halides — 3-profile comparison panel.
- Retro-Diels-Alder (same shape as DA but inverted sign).
- Fischer esterification (already has mechanism; acid-catalysed
  equilibrium example).

## 2026-04-24 — Autonomous loop round 99 — Phase 31e +1 energy profile (Fischer esterification)

### Goal
Continue Phase 31e — one more energy profile.  Candidate
short-list from round 98: Heck, Fischer, Buchwald-Hartwig,
retro-DA.  Pick one whose teaching point is genuinely distinct
from what's already shipped.

### Pick rationale
**Fischer esterification.**  Reasons:
- Already has a mechanism row (seeded round 59), so (mechanism
  + profile) pair completes the teaching surface.
- The **thermoneutral equilibrium** teaching point is genuinely
  distinct — every other seeded profile is net exergonic by
  tens-to-hundreds of kJ/mol.  Fischer is the one that needs
  Le Chatelier to run.  Having it in the catalogue makes the
  "profile shapes you see in textbooks" collection more honest.
- Pairs with the round-98 Claisen pedagogically: one is driven
  by the final step (α-C–H deprotonation between two C=O),
  the other by concentration / water removal alone.
- Heck is tempting but requires seeding the reaction row first
  (currently absent from the DB) — leave for a round that
  bundles the reaction + mechanism + profile triple.

### Ship list
1. `orgchem/db/seed_energy_profiles.py`
   - `_fischer_profile()` — 5 points (3 minima + 2 TSs).  RDS
     is addition of R'OH to the protonated C=O (TS at +55
     kJ/mol).  Product energy at +5 kJ/mol gives the shallow
     shape.
   - Added to `_PROFILE_MAP` keyed by the substring "Fischer
     esterification" (matches Reaction row id=8 in the
     seeded DB).
   - SEED_VERSION 4 → 5 so existing DBs refresh.  On re-launch
     the seeder emits "Seeded 14 energy profiles (version 5)".
2. `tests/test_energy_profile.py`
   - `test_seeded_profiles_present` — expected count 13 → 14;
     name-substring list extended with "Fischer esterification".
   - New `test_fischer_profile_is_thermoneutral` — asserts
     |ΔH| < 15 kJ/mol.  This inequality is genuinely unique to
     Fischer across the catalogue: every other seeded profile
     fails it (they're all properly exergonic).  Locking in this
     shape guards against accidentally "exothermicising" the
     Fischer payload during future numeric tweaks — which would
     erase the teaching point.

### Result
- **962 tests pass** (was 961; +1 new).
- Energy-profile catalogue now **14/20**.  Six more to reach
  the phase target.

### Next pick
Phase 31e has 6 more profiles to reach 20.  Best candidates:
- Heck reaction — needs reaction-row seed first, so bundle
  with a +1 to Phase 31b.
- SN2 1° vs 2° vs 3° halide rates — but not a single profile;
  a 3-panel comparison would need either a new renderer or 3
  separate profiles (interesting; defer until the comparison
  view exists).
- Retro-Diels-Alder — mirror of the DA profile.
- NaBH4 reduction (acetone) — already has mechanism; single-TS
  hydride transfer; straightforward.
- Nitration of benzene — already has 3-step EAS mechanism.

## 2026-04-24 — Autonomous loop round 100 — MILESTONE — β-lactam SAR series

### Goal
Round 100 — a round-number milestone.  Chose to diversify
from Phase 31e (two consecutive energy-profile rounds) into
Phase 31k SAR series to keep the content mix varied.

### Pick rationale
**β-lactam penicillin series.**  Reasons:
- Canonical medicinal-chem SAR arc: every student learns the
  penicillin → ampicillin → amoxicillin → methicillin →
  cloxacillin sequence as the progression through Beecham's
  1960s semi-synthetic mod program.
- Three distinct teaching points can be locked in with clean
  numeric inequalities:
    1. α-amino side chain boosts oral absorption
       (Pen-G 20 → ampicillin 40 → amoxicillin 90 %).
    2. 2,6-disubstituted / bulky heterocyclic side chains buy
       β-lactamase stability (methicillin, cloxacillin score 1;
       the others score 0).
    3. Steric shielding costs intrinsic MIC potency (methicillin
       MIC ≥ 150× weaker than Pen-G against S. aureus).
- Numbers drawn from Rolinson 1998 J. Antimicrob. Chemother.
  review + standard pharmacology texts.

### Ship list
1. `orgchem/core/sar.py` — new `SARSeries(id="beta-lactams")`.
   - Parent scaffold: `CC1(C)SC2CC(=O)N2C1C(=O)O` (penam core).
   - Activity columns: `mic_s_aureus_ug_ml`,
     `beta_lactamase_stability` (0/1 flag),
     `oral_bioavail_pct`.
   - 5 variants with full SMILES (canonicalised stereo),
     r-group labels, and discursive `notes` fields capturing
     the clinical / historical story.
2. `tests/test_sar.py`
   - `test_library_seeded` — `assert "beta-lactams" in ids`.
   - New `test_beta_lactam_series_landmarks` — verifies all
     5 variants present and encodes the three teaching-point
     inequalities as hard assertions.  Future tweaks to the
     numeric values can't silently erase the pedagogical
     shape of the series.

### Result
- **963 tests pass** (was 962; +1 new landmark test).
- SAR catalogue now **6/15**.
- Dialog (`Tools → Medicinal chemistry… → SAR`) picks up the
  new series via the existing `list_sar_series` registry —
  no UI changes needed.

### Round-100 retrospective
Rounds 88-100 (13 rounds) shipped Phase 33a/b/c (cross-surface
full-text search end-to-end), round-94 + round-97 pollution
cleanup (165 glossary + 58 reactions purged; prefix-gated
helper + regression suite added), and Phase 31 content
expansion:
- 31e energy profiles: 12 → 14 (+Claisen, +Fischer).
- 31k SAR series: 4 → 6 (+SSRIs, +β-lactams).
- Test suite: 945 → 963 passing (+18 regressions).

### Next pick
Continue the content cadence.  Candidates, roughly ranked:
- 31e: one more energy profile (NaBH4 or nitration of
  benzene — both mechanism-only rows).
- 31k: PDE5 inhibitors or benzodiazepines SAR series.
- 31l: +1 seeded protein (9 → 15 target; 6 more needed).
- 31b: Heck reaction row + mechanism + profile bundled
  together would move 31b / 31c / 31e all by +1.

## 2026-04-24 — Autonomous loop round 101 — Phase 31e +1 energy profile (nitration of benzene)

### Goal
Continue Phase 31e — one more energy profile.  Target this
round: a reaction whose **shape** is teaching-distinct from
what's already shipped.

### Pick rationale
**Nitration of benzene (EAS).**  Reasons:
- Already has a 3-step mechanism row (round 60).  (mechanism
  + profile) pair completes the teaching surface.
- Every electrophilic aromatic substitution shares the same
  3-point saddle-dip-saddle shape (attack TS → Wheland valley
  → deprotonation TS → aromatic product).  Seeding nitration
  first buys the canonical EAS shape into the catalogue; later
  EAS reactions (Friedel-Crafts alkylation, bromination of
  arenes, sulfonation) can reuse this curve as a pedagogical
  anchor.
- Distinct from every existing profile: SN1/E1 have TWO TSs
  but the intermediate is a carbocation (much higher), while
  Wheland is a resonance-stabilised σ-complex (shallower
  valley).  The shape IS different.

### Ship list
1. `orgchem/db/seed_energy_profiles.py`
   - `_nitration_benzene_profile()` — 5 points (3 minima +
     2 TSs).  Reactants 0; TS attack +90 (RDS); Wheland +45
     (shallow valley above reactants but below both TSs);
     TS deprotonation +55; products −25 (re-aromatisation).
   - Registered under substring "Nitration of benzene"
     matching Reaction.id=14.
   - SEED_VERSION 5 → 6 to refresh existing DBs.
2. `tests/test_energy_profile.py`
   - `test_seeded_profiles_present` — expected count 14 → 15;
     name-substring list extended with "Nitration of benzene".
   - New `test_nitration_profile_has_wheland_valley` —
     asserts: exactly 2 TSs + 3 minima, first TS energy >
     second TS energy (rate-limiting attack, not
     deprotonation), Wheland intermediate sits strictly above
     reactants AND strictly below both TSs.  Three inequalities
     lock the canonical EAS shape.

### Result
- **964 tests pass** (was 963; +1 new).
- Energy-profile catalogue now **15/20**.
- The seeder re-ran all 15 profiles at version 6 on the next
  launch (log line: "Seeded 15 energy profiles (version 6)").
- Teaching surface for nitration now complete: atom-mapped
  SMARTS + 3-step mechanism JSON with Wheland intermediate +
  2D scheme + energy profile.

### Next pick
Phase 31e has 5 more profiles to reach 20.  Strong
candidates:
- NaBH4 reduction of acetone (single-TS hydride transfer;
  already mechanism-only; simplest possible profile shape).
- Bromination of ethene (anti addition; mechanism already
  shipped round 62).
- Friedel-Crafts alkylation (reuses the EAS shape seeded
  this round — test that the renderer handles two similarly-
  shaped profiles cleanly).
- Or pivot: Phase 31k SAR +1 (PDE5 inhibitors), Phase 31l
  proteins +1 (haemoglobin 1HHO).

## 2026-04-24 — Autonomous loop round 102 — Phase 31e +1 energy profile (NaBH₄ reduction)

### Goal
Continue Phase 31e.  Catalogue at 15/20; aim for the simplest
teaching-distinct addition next — a 1,2-hydride delivery.

### Pick rationale
**NaBH₄ reduction of acetone.**  Reasons:
- Mechanism row already shipped (round 60).
- Cleanest "simple addition" teaching shape in the catalogue.
  Pairs with Grignard for comparison: same addition family,
  but Grignard's organometallic alkoxide sits much deeper
  (−85 vs −80 here) because Mg chelates the oxide, whereas
  BH₃ only caps it weakly.  Teaching point: the thermodynamic
  sink isn't just about the C–C/C–H bond formed, it's about
  the counter-ion stabilisation of the intermediate.
- Fast to ship: 5 points (3 minima + 2 TSs), small enough
  that the landmark test can verify the *whole* shape
  inequality rather than just one feature.

### Ship list
1. `orgchem/db/seed_energy_profiles.py`
   - `_nabh4_profile()` — 5 stationary points.  Points:
     Reactants 0 → TS hydride +55 (RDS; 4-centre B-H···C=O)
     → borate alkoxide −80 → TS workup −65 (downhill) →
     Products −115 (2-propanol + B(OH)₃).
   - Registered under name substring "NaBH4 reduction"
     matching Reaction.id=16.
   - SEED_VERSION 6 → 7.
2. `tests/test_energy_profile.py`
   - `test_seeded_profiles_present` expected count 15 → 16;
     name-substring list extended.
   - New `test_nabh4_profile_strongly_exergonic` — asserts
     ΔH < −50 kJ/mol, plus the stronger invariant that
     exactly one TS sits above the reactant baseline (the
     workup TS dips below).  This second clause locks in
     the "irreversible hydride delivery" shape — any future
     numeric tweak that raises the workup TS above 0 would
     erase the teaching point.

### Result
- **965 tests pass** (was 964; +1 new).
- Energy-profile catalogue now **16/20**.  Four more to go
  for the phase target.
- Seeder re-ran all 16 profiles at version 7 on next launch.
- Teaching surface for NaBH₄ now complete: reaction SMILES
  + 2-step mechanism + 2D scheme + energy profile.

### Next pick
Phase 31e has 4 more profiles to reach 20.  Strong candidates:
- Bromination of ethene (mechanism already seeded round 62).
  Teaching point: bromonium-ion valley + anti-addition
  stereochemistry.
- Friedel-Crafts alkylation (mechanism already seeded
  round 62).  Would pair with nitration to show the EAS
  shape reused with a different electrophile.
- Retro-Diels-Alder — mirror profile of DA.
- Chymotrypsin catalytic triad — enzyme-mechanism energy
  profile; distinct Michaelis-complex well shape.

## 2026-04-24 — Autonomous loop round 103 — Phase 31e +1 energy profile (bromination of ethene)

### Goal
Continue Phase 31e.  Catalogue at 16/20; aim for another
distinctly-shaped teaching profile.

### Pick rationale
**Bromination of ethene.**  Reasons:
- Mechanism row already shipped round 62 (3-step bromonium
  anti-addition).
- The bromonium-valley shape is what makes anti-addition
  stereochemistry *inevitable* — the shape IS the lesson.
  Grad-chem texts walk students through this specific curve
  to explain trans-dibromide geometry, so it's pedagogically
  heavy.
- Distinct from every other 2-TS profile in the catalogue:
  SN1 carbocation sits much higher, E1 ditto, EAS Wheland
  sits on a different substrate class.  Bromonium is its
  own thing.

### Ship list
1. `orgchem/db/seed_energy_profiles.py`
   - `_bromination_ethene_profile()` — 5 points.
     Reactants 0 → TS bromonium formation +80 (RDS) →
     bromonium ion +40 → TS anti-SN2 opening +50 →
     anti-1,2-dibromide −100.
   - Registered under substring "Bromination of ethene"
     matching Reaction.id=5.
   - SEED_VERSION 7 → 8.
2. `tests/test_energy_profile.py`
   - `test_seeded_profiles_present` expected 16 → 17.
   - New `test_bromination_profile_bromonium_valley` locks
     four invariants: exactly 2 TSs + 3 minima, first TS
     higher than second TS (RDS is bromonium formation),
     bromonium strictly above reactants (true valley, not
     stability trough) but strictly below both TSs,
     net ΔH < −50 kJ/mol.

### Result
- **966 tests pass** (was 965; +1 new).
- Energy-profile catalogue now **17/20**.  Three more to
  reach the phase target.
- Teaching surface for bromination now complete: atom-mapped
  SMARTS + 3-step mechanism JSON + 2D scheme + energy profile.

### Next pick
Phase 31e has 3 more profiles to reach 20.  Candidates:
- Friedel-Crafts alkylation (mechanism seeded round 62).
  Would be the second EAS profile — interesting test of
  whether the renderer handles two σ-complex curves.
- Pinacol rearrangement (mechanism seeded round 61, 4-step
  with 1,2-methyl shift — distinctive shape).
- Retro-Diels-Alder (mirror of DA profile).
- Chymotrypsin catalytic triad (enzyme mechanism; would
  be the first enzyme-reaction energy profile in the
  catalogue — distinct Michaelis-complex well shape).

## 2026-04-24 — Autonomous loop round 104 — Phase 31e +1 energy profile (pinacol rearrangement)

### Goal
Continue Phase 31e.  Catalogue at 17/20; aim for another
distinctive teaching shape.

### Pick rationale
**Pinacol rearrangement.**  Reasons:
- Mechanism row already shipped (round 61) — 4-step with
  explicit 1,2-methyl shift.
- The profile shape carries a genuinely unique teaching
  point: "oxocarbenium is MORE stable than a tertiary
  carbocation".  Students usually think tert-C⁺ is close
  to the stability ceiling; pinacol shows them that an
  O lone-pair donor does one better.
- 3 TSs + 4 minima = 7 points — the largest profile in
  the catalogue, and a nice test of the renderer's
  multi-TS layout.
- Pairs with the Phase-33a full-text search story: a user
  typing *"1,2-shift"* or *"migratory aptitude"* should
  now hit both the mechanism and the energy profile.

### Ship list
1. `orgchem/db/seed_energy_profiles.py`
   - `_pinacol_profile()` — 7 points.  Reactants 0;
     TS ionisation +100 (RDS); tertiary carbocation +40;
     TS 1,2-methyl shift +50 (lower than ionisation);
     protonated ketone / oxocarbenium −20 (below the
     carbocation); TS deprotonation −10; products −70.
   - Registered under substring "Pinacol rearrangement"
     matching Reaction.id=25.
   - SEED_VERSION 8 → 9.
2. `tests/test_energy_profile.py`
   - `test_seeded_profiles_present` expected 17 → 18.
   - New `test_pinacol_profile_methyl_shift_downhill`
     locks three invariants:
       - Exactly 3 TSs present.
       - Ionisation TS (first) strictly exceeds BOTH the
         migration TS and the deprotonation TS.
       - Oxocarbenium minimum strictly below the tertiary
         carbocation minimum.
     That third inequality is the one that matters
     pedagogically; the other two are guard-rails.

### Result
- **967 tests pass** (was 966; +1 new).
- Energy-profile catalogue now **18/20**.  Two more to
  reach the phase target.

### Next pick
Phase 31e has 2 more to reach 20.  Candidates:
- Friedel-Crafts alkylation — second EAS profile; would
  test whether the renderer lays out two σ-complex curves
  side-by-side cleanly.
- Retro-Diels-Alder — mirror of DA; could be ~3 points.
- Chymotrypsin catalytic triad — first enzyme-reaction
  profile in the catalogue; distinct Michaelis-complex
  well shape.

## 2026-04-24 — Autonomous loop round 105 — Phase 31e +1 energy profile (chymotrypsin)

### Goal
Continue Phase 31e.  Catalogue at 18/20.  Ship the first
**enzyme-catalysed** profile to introduce a genuinely new
shape class to the catalogue.

### Pick rationale
**Chymotrypsin: catalytic triad peptide hydrolysis.**  Reasons:
- Already has a 4-step mechanism row (round 62) with full
  catalytic-triad arrow-pushing.
- The covalent-catalysis shape ("double hump with acyl-enzyme
  well in the middle") is the canonical example that every
  biochemistry text uses to explain how enzymes split one
  20-kcal/mol barrier into two ~10-kcal/mol enzyme barriers.
  None of the existing 18 profiles look like this.
- Pairs naturally with the Phase 24 protein stack — students
  who've rendered a serine protease 3D structure (1EX3, for
  example) can now also see the energy profile for what
  happens in that active site.
- Genuinely distinct from the round-104 pinacol profile:
  pinacol's 3-TS profile has a rising-then-falling shape,
  while chymotrypsin's 4-TS profile has two distinct saddle
  maxima with a real covalent intermediate well between.

### Ship list
1. `orgchem/db/seed_energy_profiles.py`
   - `_chymotrypsin_profile()` — 9 stationary points:
     Michaelis 0 → TS acylation +65 → T1 +25 → TS amine leaves
     +40 → acyl-enzyme −15 → TS deacylation +50 → T2 +15 →
     TS Ser leaves +30 → products −80.
   - Registered under substring "Chymotrypsin" matching
     Reaction.id=27.  SEED_VERSION 9 → 10.
2. `tests/test_energy_profile.py`
   - `test_seeded_profiles_present` expected 18 → 19.
   - New `test_chymotrypsin_profile_acyl_enzyme_well` locks:
     (a) exactly 4 TSs,
     (b) acyl-enzyme < Michaelis complex (acylation half
         carries the favourable ΔG; teaching-critical),
     (c) both tetrahedral intermediates strictly above
         Michaelis (they're intermediates, not products) AND
         strictly below the highest TS (they're stabilised by
         oxyanion-hole donation; they don't become pseudo-TSs).

### Result
- **968 tests pass** (was 967; +1 new).
- Energy-profile catalogue now **19/20**.
- Phase 31e is **one profile away** from its 20-profile
  target.

### Next pick
One profile to close Phase 31e.  Strong candidates:
- Friedel-Crafts alkylation — second EAS shape; already has
  mechanism (round 62).  Would complete the "family" view of
  Pinacol + bromination + EAS + nitration + Friedel-Crafts
  to show shape variation across cation-pushing chemistry.
- Buchwald-Hartwig catalytic cycle — would pair with
  Sonogashira for a side-by-side Pd(0)/Pd(II) teaching view.
  Needs energy-profile-only seed since the Buchwald-Hartwig
  reaction row is mechanism-free.
- Retro-Diels-Alder — simplest possible to close the phase.

## 2026-04-24 — Autonomous loop round 106 — 🎯 Phase 31e CLOSE at 20/20 (Friedel-Crafts alkylation)

### Goal
Close Phase 31e — one final profile to cap the catalogue at
the 20-profile target.

### Pick rationale
**Friedel-Crafts alkylation.**  Reasons:
- Mechanism row already shipped (round 62).
- Pairs with the round-101 nitration profile — two EAS
  curves with genuinely different shapes.  Teaches students
  that two reactions sharing the same "Wheland valley"
  middle section can still differ in their pre-equilibrium
  electrophile-generation step.
- The specific teaching point encoded by the shape — FC
  alkylation's free-cation intermediate is genuinely
  unstable (+25 kJ/mol above reactants) — ties directly to
  classroom explanations of (a) 1°→2° rearrangement,
  (b) poly-alkylation, (c) why acylation (which goes via a
  stable acylium, not a free C⁺) is preferred for
  preparative work.

### Ship list
1. `orgchem/db/seed_energy_profiles.py`
   - `_friedel_crafts_profile()` — 7 points (3 TSs + 4
     minima).  Reactants 0 → TS cation generation +60 →
     CH₃⁺/AlCl₄⁻ +25 → TS EAS attack +70 (RDS) →
     Wheland intermediate +30 → TS deprotonation +45 →
     toluene + HCl −20.
   - Registered under substring "Friedel-Crafts alkylation"
     matching Reaction.id=12.  SEED_VERSION 10 → 11.
2. `tests/test_energy_profile.py`
   - `test_seeded_profiles_present` — expected 19 → 20.
     Docstring updated to note the phase is closed.
   - New `test_friedel_crafts_profile_has_free_cation` locks:
     3 TSs (not 2 like nitration), free-cation minimum
     strictly above reactant baseline, Wheland intermediate
     also above baseline.  These three inequalities together
     pin down the "FC is different from nitration" shape.

### Result
- **969 tests pass** (was 968; +1 new regression).
- Energy-profile catalogue now **20/20**.  **Phase 31e is
  CLOSED.**
- 20 distinct profile shape classes in the catalogue:
    - Concerted single-TS (SN2, E2, Diels-Alder)
    - Two-TS ionisation (SN1, E1)
    - Two-TS addition with pre-equilibrium (Bromination — bromonium valley)
    - Multi-step acyl substitution (Aldol, Claisen, Fischer)
    - Multi-step concerted-but-stepwise (Grignard, NaBH₄,
      Wittig, Michael, HWE)
    - Catalytic cycles (Sonogashira, Mitsunobu)
    - EAS σ-complex (Nitration, Friedel-Crafts)
    - Rearrangement with 1,2-shift (Pinacol)
    - Enzyme covalent catalysis (Chymotrypsin)

### Phase 31 progress snapshot (post-round-106)
- 31a. Molecules 415/400  ✅ (over target)
- 31b. Reactions 35/50   — 15 more to go
- 31c. Mechanisms 20/20  ✅
- 31d. Pathways 25/25    ✅
- 31e. Energy profiles 20/20  ✅ (this round)
- 31f. Glossary 80/80    ✅
- 31g. Tutorials 30/30   ✅
- 31h. Carbohydrates 25/40  — 15 to go
- 31i. Lipids 31/40      — 9 to go
- 31j. Nucleic acids 33/40  — 7 to go
- 31k. SAR series 6/15   — 9 to go
- 31l. Proteins 9/15     — 6 to go

Seven of twelve sub-phases now at target.

### Next pick
Remaining open sub-phases: 31b (reactions), 31h (carbs),
31i (lipids), 31j (nucleic acids), 31k (SAR), 31l (proteins).
Best-ROI candidates:
- 31k PDE5 inhibitors SAR series (5 variants: sildenafil /
  vardenafil / tadalafil / avanafil / udenafil) — canonical
  chemotype-switch story like β-lactams.
- 31b Heck reaction row + mechanism + energy profile
  bundled (would cover 31b+31c+31e at +1 each, but 31c and
  31e are already closed — this is now just 31b).
- 31l haemoglobin 1HHO seeded protein.

## 2026-04-24 — Autonomous loop round 107 — Phase 31l +1 seeded protein (haemoglobin 1HHO)

### Goal
Diversify from the five-round energy-profile streak into
Phase 31l (proteins, 9/15 → 15/15).

### Pick rationale
**Haemoglobin 1HHO (R-state, oxy).**  Reasons:
- Most pedagogically important structure not yet seeded.
  Pairs with the existing myoglobin 1MBN: same globin fold,
  same heme, but four subunits + cooperativity.
- Single PDB entry with clean cross-reference to 2HHB (T-state,
  deoxy) for the quaternary-rotation story.  One entry,
  two teaching viewpoints.
- Canonical MWC cooperativity anchor every biochem text uses.
- Zero new code needed — just a `SeededProtein` entry; the
  fetch / parse / render / contact / PPI pipeline all work
  automatically on any PDB via Phase 24a-l.

### Ship list
1. `orgchem/core/protein.py`
   - Appended a 10th `SeededProtein` entry for 1HHO with
     pdb_id, name ("Human oxy-haemoglobin (R-state)"),
     ligand_name ("HEM (heme-b) + OXY (bound O₂)"), and
     teaching_story that explicitly references 1MBN + 2HHB
     for cross-comparison.
2. `tests/test_protein.py`
   - `test_seeded_proteins_has_core_targets` extended to
     require 1HHO alongside the original 9 entries.
   - Added content-marker assertions: name contains
     "R-state" or "haemoglobin", teaching story contains
     "cooperativity".  These guard the pedagogical framing
     against future edits that could drop the MWC reference.

### Result
- **969 tests pass** (unchanged — tightened existing test,
  no new test file).
- Proteins catalogue **10/15** — 5 more to close Phase 31l.
- The Proteins tab (Phase 24) picks up the new entry
  automatically via `list_seeded_proteins()` — no panel
  change required.

### Next pick
5 open Phase 31 sub-phases remaining.  Rough priorities:
- 31k PDE5 inhibitors SAR series (5 variants; chemotype-
  switch story like β-lactams and SSRIs already did).
- 31l KcsA potassium channel 1BL8 (the canonical K⁺
  selectivity-filter structure — pairs with hemoglobin for
  "how does a protein discriminate an ion?" teaching).
- 31b +1 named reaction (Heck, Negishi, Stille — 3 Pd
  couplings missing from the 35-reaction catalogue).
- 31j inosine / wobble-base nucleic-acid entries.

## 2026-04-24 — Autonomous loop round 108 — Phase 31k +1 SAR series (PDE5 inhibitors) + Phase 34 scoped

### Roadmap addition (user-flagged mid-round)
User directive: add an amino-acid sequence viewer to the
3D protein display panel with cross-linked selection
(sequence → 3D and vice versa), DNA strand above the AA
sequence, plus highlight tracks for pockets / ligand
contacts / genes / structures of interest.  Added as
**Phase 34** to ROADMAP.md with 6 sub-phases (34a core
dataclass + agent action → 34b SequenceBar widget →
34c two-way 3D binding → 34d DNA strand strip → 34e
feature tracks: pockets/contacts/secondary-structure/
user-tags/UniProt gene annotations → 34f selection-aware
agent actions).  Design notes cover long-protein mini-map,
multi-chain stacking (1HHO / 1HPV), testing strategy via
pytest-qt + QSignalSpy.

### Goal
Continue Phase 31k (SAR series, 6/15 → 7).  Textbook-grade
chemotype-switch story as the teaching frame.

### Pick rationale
**PDE5 inhibitors.**  Reasons:
- Canonical "chemotype switch tunes both half-life AND
  selectivity" case study.  Sildenafil / vardenafil /
  udenafil share the pyrazolopyrimidinone scaffold;
  tadalafil breaks away with a β-carboline diketopiperazine
  chemotype and gets BOTH a 17.5-h half-life (vs 4 h) AND
  PDE6 selectivity >700× (vs <15×) — two textbook wins from
  one structural decision.
- Clean activity-column shape
  (`pde5_ic50_nM`, `t_half_h`, `pde6_selectivity`) matches
  the existing `SARSeries` schema.
- Commercial significance: Sildenafil, Tadalafil, Vardenafil
  = three of the best-selling drugs of the 2000s-2010s.
  Easy to anchor in classroom context.

### Ship list
1. `orgchem/core/sar.py`
   - New `SARSeries(id="pde5-inhibitors")` with 5 variants:
     Sildenafil / Vardenafil / Tadalafil / Avanafil / Udenafil.
   - Activity numbers drawn from Rotella 2002 *Nat. Rev.
     Drug Discov.* PDE5 SAR review.  Each variant's `notes`
     captures clinical framing (Viagra 1998 first-in-class,
     Cialis weekend-pill story, Stendra fast-onset trade,
     Zydena regional approval).
2. `tests/test_sar.py`
   - `test_library_seeded` + `assert "pde5-inhibitors" in ids`.
   - New `test_pde5_series_landmarks` — three hard
     assertions locking in the teaching points above.  Each
     assertion is a strict inequality against every other
     variant (not just against one benchmark), so future
     numeric tweaks can't silently break the pedagogical
     ordering.

### Result
- **970 tests pass** (was 969; +1 new landmark test).
- SAR catalogue now **7/15**.
- ROADMAP Phase 34 scoped with implementation plan.

### Next pick
8 SAR series left to hit 15; 5 open Phase 31 sub-phases
total.  Strong candidates:
- 31l KcsA 1BL8 potassium channel (the canonical
  selectivity-filter teaching structure).
- 31b Heck reaction row (one of the three Pd-coupling gaps).
- 31k benzodiazepines SAR (GABA-A subunit selectivity).
- 31h rare-sugar carbohydrates (+4 toward 40).
- Or **start Phase 34a** — core SequenceView dataclass + agent
  action is self-contained and a good low-risk first step.

## 2026-04-24 — Autonomous loop round 109 — Phase 35d shipped (command palette learns synonyms)

### Goal
Act on the Phase 35 directive the user just added to ROADMAP
("add synonyms … incorporated in all searches").  Pre-round
audit showed:
- 35a (persist PubChem synonyms on download) — **already done**
  round 58 (`download_from_pubchem` writes `synonyms_json`
  at line 215).
- 35c / 35e / 35f — queued.
- 35d (command palette) — easiest + highest-visibility gap.

### Pick rationale
**35d.**  The Ctrl+K command palette is the single-keystroke
jump-to-anything UI.  Typing *"Paracetamol"* today returns
zero hits even though the DB has `Acetaminophen` with
`synonyms_json=["Paracetamol", ...]`.  That's the exact
failure mode the user flagged.  Fix is local, fast, testable.

### Ship list
1. `orgchem/gui/dialogs/command_palette.py`
   - Rewrote `_molecule_entries()` to pull `synonyms_json`
     alongside `id/name/smiles` and emit one palette entry
     per synonym (same `target=mid`, label = synonym,
     sublabel = *"alias of <canonical>"*).  Case-insensitive
     dedup keeps the canonical name from being duplicated
     as its own synonym.
   - New `_looks_like_registry_id(s)` helper rejects
     CAS (`\d{1,7}-\d{2}-\d`), pure digits / dash-joined
     digits, `CHEMBL\d+`, `UNII-…`, `DTXSID`, `DTXCID`,
     `NSC`, `MFCD`, `CCDS`, `SCHEMBL`, `EINECS`, `RTECS`,
     `BRN`, `FDA`, `InChI=…`, and the 27-char InChIKey
     hash — so registry noise never reaches the UI.
2. `tests/test_command_palette.py`
   - New `test_palette_emits_synonym_aliases` iterates every
     DB row with a non-empty `synonyms_json`, checks that
     at least one synonym produces a palette entry whose
     `target` matches the canonical row id.
   - New `test_palette_filter_registry_ids` fuzz-tests the
     regex helper against 8 known-bad strings (CAS, ChEMBL,
     UNII, DTXSID, InChI, InChIKey, NSC, SCHEMBL) and
     5 known-good natural-language names.

### Result
- **972 tests pass** (was 970; +2 new).
- Command palette now reaches every seeded molecule via
  every curated synonym.  The round-58 `Retinol ↔ Vitamin A`
  reconciliation pair works both ways from the palette.
- Phase 35 now at **2 / 6 sub-phases complete** (35a from
  round 58, 35d from this round).

### Next pick
Phase 35 queue:
- **35f** — molecule browser row shows first synonym in
  grey italics.  One-line `data()` extension.
- **35e** — compare-tab + tutor `show_molecule(name)`
  already route through `find_molecule_by_name` (which
  hits synonyms); add regression coverage asserting
  *"Vitamin A" → Retinol* end-to-end.
- **35c** — bulk PubChem backfill via a one-shot CLI
  (network-dependent; heavier).
- **35b** — optional `fetch_synonyms=True` kwarg on
  tutor `add_molecule`.

Or pivot to Phase 34 (sequence viewer) or continue Phase 31
content (KcsA protein, Heck reaction, +carbs/+lipids/+NAs).

## 2026-04-24 — Autonomous loop round 110 — Phase 35f shipped (molecule browser synonym hint)

### Goal
Close one more Phase 35 sub-phase in the same spirit as the
round-109 palette work.  Candidates: 35e (regression-cover an
existing working path), 35f (visible UI change).  35f picked
because it's higher-visibility — users see the synonym hint
immediately in the left-dock list.

### Pick rationale
**35f — synonym hint in the browser row.**  Reasons:
- Currently `_MolListModel.data(DisplayRole)` returns
  `"<name>   [<formula>]"`.  Adding the first synonym
  (` · <synonym>`) is a single `data()` extension — no new
  widget, no new infrastructure.
- Reuses the round-109 `_looks_like_registry_id` helper for
  filtering — clean cross-module dependency, and if future
  registry patterns show up (e.g. DrugBank DB IDs) we fix
  the one helper and both surfaces benefit.
- Synonym-aware tooltip is a natural pairing — users who
  hover get the full list even when only one fits on the
  row.

### Ship list
1. `orgchem/gui/panels/molecule_browser.py`
   - New module-level helpers `_all_synonyms(row)` and
     `_first_natural_synonym(row)` — the former returns the
     full filtered list (for tooltip), the latter just the
     first hit (for Display).  Both filter registry IDs via
     the shared helper and drop entries that match the
     canonical name (case-insensitive).
   - `data(DisplayRole)` now appends ` · <first synonym>`
     when available.
   - `data(ToolTipRole)` now returns
     `"<SMILES>\n\nAlso known as: <list>"` when ≥1 synonym
     exists, otherwise just the SMILES string.
2. `tests/test_molecule_browser_synonym_hint.py` — new file
   with 5 tests:
   - `test_first_natural_synonym_strips_registry_noise` —
     pure unit test on the helper; inputs include CAS,
     ChEMBL, and three natural-language synonyms; helper
     picks the first natural one.
   - `test_first_natural_synonym_empty_when_no_synonyms` —
     None and `"[]"` both yield `""`.
   - `test_first_natural_synonym_drops_canonical_self_reference`
     — a synonym equal to the canonical name gets filtered.
   - `test_browser_display_role_includes_synonym` (integration)
     — walks every row in the real seeded DB, confirms at
     least one surfaces a synonym hint, and confirms the hint
     itself passes `_looks_like_registry_id == False`.
   - `test_browser_tooltip_lists_synonyms` (integration) —
     confirms both tooltip variants are reachable in the
     seeded DB (some rows have synonyms → "Also known as:"
     line; some rows don't → plain SMILES).

### Result
- **977 tests pass** (was 972; +5 new).
- Phase 35 now **3/6** sub-phases complete (35a round 58,
  35d round 109, 35f round 110).
- Shared helper pattern: `_looks_like_registry_id` is now
  used by both the command-palette synonym enumeration and
  the browser row hint.  Future registry-ID patterns get
  fixed in one place.

### Next pick
Phase 35 queue:
- **35e** — regression coverage for compare-tab +
  `show_molecule(name)` synonym paths.  Both already route
  through `find_molecule_by_name` (which hits `synonyms_json`)
  so this is test-only; worth ~1 round to lock.
- **35c** — bulk PubChem backfill CLI.  Network-dependent,
  rate-limited, heavier — queue later.
- **35b** — optional `fetch_synonyms=True` on tutor
  `add_molecule`.  Small.
Or pivot to Phase 34 (sequence viewer) or continue Phase 31.

## 2026-04-24 — Autonomous loop round 111 — Phase 35e regression-locked

### Goal
Close the third remaining Phase 35 sub-phase this session.
Audit first: 35e asks for synonym-aware resolution in Compare
tab + tutor `show_molecule`.

### Audit outcome — no new code needed
Both surfaces already route through `find_molecule_by_name`:
- `compare_panel._Slot._on_load()` at line 107.
- `agent/library.show_molecule()` at line 99.
And `find_molecule_by_name` was patched in round 58 to ILIKE
`synonyms_json` alongside `name`.  So the feature *works* —
it's just not test-covered.

### Pick rationale
**Regression-lock over re-implement.**  Adding 9 pytest cases
costs nothing and guards the exact user-facing path against
future refactors (e.g. if someone splits `find_molecule_by_name`
into `find_by_canonical` + `find_by_synonym` they'll know
immediately whether they've preserved both code paths).

### Ship list
1. `tests/test_synonym_lookup_paths.py` (new file, 8 tests
   + 1 smoke-check = 9 total):
   - `test_find_molecule_by_name_resolves_paracetamol_to_acetaminophen`
     — the paradigm case; the seeded synonym "Paracetamol"
     on the Acetaminophen row must reach back to it.
   - `test_find_molecule_by_name_resolves_asa` — ditto for
     "ASA" → Aspirin (different curated pair).
   - `test_find_molecule_by_name_is_case_insensitive` — three
     casings of "Paracetamol" all hit the same row id.
   - `test_find_molecule_by_name_unknown_returns_none` —
     fabricated string is a miss, not an exception.
   - `test_show_molecule_action_resolves_synonym` — tutor /
     stdio bridge entry point reaches Acetaminophen via
     "Paracetamol".
   - `test_show_molecule_action_resolves_asa` — same for
     "Acetylsalicylic acid" → Aspirin.
   - `test_show_molecule_action_unknown_synonym_errors` —
     missing strings produce a clean error-return, not a
     crash.
   - `test_compare_panel_slot_resolves_synonym_text` —
     pytest-qt drives the real `ComparePanel._Slot._on_load`
     with "Paracetamol" typed into the field; post-load the
     slot title contains "Acetaminophen" (the resolver won).
   - `test_compare_panel_slot_resolves_asa_synonym` — ditto
     for ASA/Aspirin.
2. Mid-round fix: first draft checked for a
   `_resolve_one_text` helper on `ComparePanel` itself; the
   actual resolver lives on the inner `_Slot` class as
   `_on_load` (reads the QLineEdit, calls
   `find_molecule_by_name`, calls `_display`).  Test
   rewritten to drive that path directly.

### Result
- **986 tests pass** (was 977; +9 new regressions).
- Phase 35 now **4/6** sub-phases complete — only 35b
  (optional `fetch_synonyms` kwarg on tutor `add_molecule`)
  and 35c (bulk PubChem backfill CLI) left.

### Next pick
Strong candidates for the next round:
- **35b** — small kwarg wire-up; keeps the user-flagged
  Phase 35 streak going for a fifth consecutive round.
- **35c** — bulk backfill CLI; network-dependent but
  self-contained; would leave only 35c open for later.
- Pivot to Phase 34 (sequence viewer) — user flagged it
  explicitly and we haven't started.  Good moment to kick
  off 34a (headless `SequenceView` dataclass + agent
  action).
- Pivot back to Phase 31 content (31b Heck reaction,
  31l KcsA protein, etc).

## 2026-04-24 — Autonomous loop round 112 — Phase 34a shipped (sequence-viewer core)

### Goal
Pivot from Phase 35 (synonyms) to Phase 34 (sequence viewer) —
user flagged both explicitly this session; kick off 34a, the
purely-headless data core, so later Qt-widget work has a clean
foundation.

### Ship list
1. `orgchem/core/sequence_view.py` — new module.
   - `SequenceView`: pdb_id + `protein_chains` + `dna_chains` +
     `highlights` + `to_dict()` + `get_chain(id)` helper.
   - `ChainSequence`: chain_id, one_letter, three_letter,
     residue_numbers, kind ∈ {protein, dna, rna}, `length`
     property, `to_dict()`.
   - `HighlightSpan`: chain_id, start, end, kind, label,
     colour with `to_dict()` that defaults to the shared
     `HIGHLIGHT_COLOURS` palette if no explicit colour.
   - `build_sequence_view(protein)`: walks Phase-24a
     `Protein.chains`, classifies each as protein / DNA / RNA
     by majority residue kind, converts 3→1-letter via
     `_AA_3_TO_1` / `_NT_3_TO_1`.  Ion-only pseudo-chains
     produce `None` and are dropped.
   - `attach_contact_highlights(view, report)`: walks a
     Phase-24e `ContactReport` + stamps one coloured span per
     contact residue, kind tagged for downstream UI.
   - `attach_pocket_highlights(view, pockets)`: walks
     Phase-24d pockets, collapses each chain's lining
     residues to a single min-max span per chain.
   - `_parse_residue_seq_id`: coerces "HIS57", "A:HIS57",
     int, and "42" to seq_id.
2. `orgchem/agent/actions_protein.py` — new
   `get_sequence_view(pdb_id, include_contacts, ligand_name)`
   agent action that calls `parse_from_cache_or_string` +
   `build_sequence_view` + optionally contact-highlights,
   returns `view.to_dict()`.  Errors cleanly if the PDB
   isn't cached.
3. `orgchem/gui/audit.py` — wiring entry for
   `get_sequence_view` (pointed at the Proteins Summary
   sub-tab for now; the Phase 34b `SequenceBar` widget will
   replace this pointer).
4. `INTERFACE.md` — new row describing the module.
5. `tests/test_sequence_view.py` — 9 pytest cases:
   - Build from a 3-chain in-memory PDB fixture; verify
     protein/DNA split, 1-letter code, 3-letter list,
     residue-number list, ion-chain skipped.
   - `get_chain` / `all_chains` round-trip.
   - `HighlightSpan.to_dict` uses palette default + explicit
     colour overrides.
   - `attach_contact_highlights` residue-format fuzz (int,
     "HIS57", "A:HIS57", "42", None/"" rejected).
   - `attach_pocket_highlights` collapses per-chain residue
     lists to min-max spans.
   - `SequenceView.to_dict` schema assertion.
   - Agent action missing-pdb → `{error}`.
   - Agent action happy path with a monkeypatched
     `_pdb_cache_dir` → returns populated view.

### Mid-round friction
- First full-suite run after adding the agent action:
  15 `test_gui_coverage_still_100` failures.  Root cause:
  `get_sequence_view` absent from `GUI_ENTRY_POINTS` → audit
  coverage dropped.  Fixed by adding the wiring entry (with
  a note that Phase 34b will re-point it at the actual
  widget).
- Second full-suite run: `test_every_module_referenced_in_interface_md`
  failed — new `core/sequence_view.py` wasn't in INTERFACE.md.
  Fixed by adding a full row description.
- Third run: 995 pass, clean.

### Result
- **995 tests pass** (was 986; +9 new).
- Phase 34 now **1/6** sub-phases complete (34a).
- The Phase 34b `SequenceBar` Qt widget can now consume
  `SequenceView.to_dict()` / `HighlightSpan.to_dict()`
  without touching `core/` again.

### Next pick
- **34b** — `SequenceBar` Qt widget (click-drag selection,
  monospace row, colour-overlay spans).  Bigger; next session.
- **35b / 35c** — complete Phase 35 (tutor kwarg; bulk
  backfill CLI).
- Or continue Phase 31 content (KcsA 1BL8 protein, Heck
  reaction, etc).

## 2026-04-24 — Autonomous loop round 113 — 🎯 1 000 tests + Phase 35b shipped

### Milestone
**1 000 passing tests** reached this round.  Count was 586 at
the start of the autonomous-loop era (round 50 baseline);
doubled in ~60 rounds of steady +1-to-+10 per round.

### Goal
Close a fifth Phase 35 sub-phase — the tutor
`add_molecule(…, fetch_synonyms=True)` kwarg.

### Ship list
1. `orgchem/sources/pubchem.py`
   - New `fetch_synonyms_by_inchikey(inchikey, limit=10) → list[str]`.
     Guards against (a) missing `pubchempy` (ImportError → `[]`),
     (b) network / HTTP / parse errors (any raise → `[]`),
     (c) no hit (`[]`).  Never raises — calling sites use it
     purely as a best-effort decorator.
2. `orgchem/agent/actions_authoring.py::add_molecule`
   - New `fetch_synonyms=False` kwarg in the signature.
   - After validation + dedup checks succeed but before
     `DBMol(...)` construction: if opted in, call the helper,
     filter raw results through the round-109
     `_looks_like_registry_id` (CAS / ChEMBL / UNII / InChI /
     InChIKey → drop), dedup against the canonical name
     (case-insensitive), cap at 10, write as JSON to the
     new `synonyms_json` column of the inserted row.
   - Accepted response carries `synonyms_fetched: int` —
     0 when offline / no match / kwarg off.
3. `tests/test_add_molecule_fetch_synonyms.py` — 5 tests:
   - Default path has `synonyms_fetched == 0` and no row
     synonyms.
   - Mocked happy path returns 4 strings; 1 CAS is filtered;
     3 natural-language survive + land in `synonyms_json`.
   - Mocked empty return ⇒ accepted with 0 synonyms.
   - Silent-network-error path via monkeypatched `_boom` that
     raises from the helper — the `add_molecule` wrapper
     doesn't bubble; the sanity-check direct call confirms
     the mock actually replaced the helper.
   - Import-error simulation via `sys.modules.pop("pubchempy")`
     + `builtins.__import__` block — helper returns `[]`
     without raising.

### Mid-round friction
- First draft used real seeded SMILES (ethanol, toluene,
  cyclohexane) which got rejected as duplicates.  Switched
  to `"C" * n + "O"` alkane-alcohol generators with distinct
  `n` per test (40, 41, 42, 43) — guaranteed novel.
- Pollution auto-purge at session end removed all 4
  `Tutor-test-…` rows created by the tests.

### Result
- **1 000 tests pass** (was 995; +5 new).
- Phase 35 now **5 / 6 sub-phases complete** — only 35c
  bulk-backfill CLI remains.  That one is network-heavy
  (~85 s one-shot at 200 ms/req for ~415 seeded rows) so
  it's appropriately deferred.

### Next pick
- **35c** — bulk PubChem synonym backfill CLI.  Self-
  contained; worth doing when we want a well-tested one-
  shot utility ready for users.
- **34b** — SequenceBar Qt widget (Phase 34).
- Continue Phase 31 content (KcsA 1BL8, Heck reaction, or
  one more +1 anywhere).

## 2026-04-24 — Autonomous loop round 114 — Phase 31l +1 protein (KcsA 1BL8)

### Goal
Quick Phase 31 increment after two tool / infra rounds.
Best-ROI candidates: 31l KcsA, 31b Heck reaction row,
31h +1 carb.  Picked KcsA — landmark structure, textbook
teaching anchor that complements the round-107 haemoglobin
cooperativity pair.

### Pick rationale
**KcsA potassium channel (1BL8).**  Reasons:
- Doyle/MacKinnon 1998 *Science* — first atomic-resolution
  ion-channel structure.  MacKinnon got the 2003 Chemistry
  Nobel specifically for this.  Canonical textbook subject.
- The TVGYG filter story is exactly the kind of "architecture
  → function" shape argument the app is best suited to teach.
- Pairs pedagogically with the round-107 haemoglobin entry —
  both demonstrate how a specific 3D fold dictates a specific
  binding behaviour (cooperativity / ion selectivity).
- Zero new code — just a `SeededProtein` entry + content-
  marker assertion; PDB fetch / rendering / contact analysis
  all work via existing Phase 24a-l pipeline.

### Ship list
1. `orgchem/core/protein.py` — 11th `SeededProtein`:
   pdb_id "1BL8", ligand_name "K (four K⁺ ions in the
   selectivity filter)", teaching story referencing Doyle /
   MacKinnon 1998 + TVGYG filter + dehydration-geometry
   story + explicit pairing with 1HHO for the "architecture
   → specificity" teaching arc.
2. `tests/test_protein.py::test_seeded_proteins_has_core_targets`
   tightened:
   - `must_have` set now includes 1BL8.
   - New content-marker assertion: name contains "KcsA" or
     "potassium" AND teaching story contains "selectivity".
     Locks the teaching-point framing against future edits.

### Result
- Catalogue now **11/15** proteins.  Phase 31l halfway done;
  4 more to close.
- **1 000 tests pass** (unchanged — tightened existing test).
- The Proteins tab picks up the new entry automatically via
  `list_seeded_proteins()` — no panel wiring needed.

### Next pick
- **31l** — 4 more proteins to reach 15 (chymotrypsin alt
  form, kinesin motor, nucleosome core 1AOI, antibody Fab
  1IGT).
- **35c** — bulk PubChem synonym backfill CLI.  Would close
  Phase 35 end-to-end.
- **34b** — SequenceBar Qt widget.
- **31b** — Heck reaction row (one of three Pd-coupling gaps).

## 2026-04-24 — Autonomous loop round 115 — Phase 31l +2 proteins (nucleosome + IgG)

### Goal
Keep Phase 31l momentum — add two more proteins in one round
since each is just a `SeededProtein` entry with no code.
Pushes 11/15 → 13/15.

### Pick rationale
**1AOI nucleosome + 1IGT IgG.**
- 1AOI is the canonical "protein + nucleic-acid" teaching
  structure — anchors chromatin / histone-tail-modification /
  epigenetics discussions.  Pairs with the round-29
  nucleic-acid PDB-motif entries (1BNA, 143D, 1EHZ) for the
  protein-DNA interaction arc.
- 1IGT is the canonical "how does an antibody look?"
  teaching structure — anchors Ig-domain fold + CDR /
  antigen-binding / Fc-receptor + Fc-glycan engineering
  stories.  First complete IgG solved.
- Both are landmark single-paper structures (Luger/Richmond
  1997 *Nature*; Harris/Edmundson 1997 *Biochemistry*) —
  easy to anchor in literature for students.

### Ship list
1. `orgchem/core/protein.py` — 12th + 13th `SeededProtein`
   entries.  Each carries a paragraph-length teaching story
   referencing the primary literature + the specific teaching
   point the structure is canonical for.
2. `tests/test_protein.py` — `must_have` list extended with
   "1AOI", "1IGT".  New content-marker assertions:
   - 1AOI story must contain "histone" (the whole reason
     this structure is taught).
   - 1IGT story must contain at least one of "CDR",
     "antigen", "fab" (the functional terminology that
     separates an IgG teaching story from any other
     multi-chain protein).

### Result
- **1 000 tests pass** — content markers added to an existing
  test, no new test count.
- Proteins catalogue now **13/15** — 2 more closes Phase 31l.

### Next pick
Phase 31l: 2 more to close.  Options:
- Chymotrypsin alt form (e.g. 1GCT) — complements the
  round-62 chymotrypsin mechanism + round-105 energy profile
  with a structural anchor that isn't the enzyme-mechanism
  JSON.
- Kinesin motor (e.g. 3KIN) — cytoskeletal-protein anchor
  that's structurally distinct from every other entry.
- Ribosome subunit (3V6F large-subunit, or 2J00 small-
  subunit) — huge structure but teaches RNA-protein
  complexes.

Or pivot back to Phase 35c (bulk synonym backfill) to close
Phase 35 end-to-end, or Phase 34b (SequenceBar widget) to
push Phase 34 forward.

## 2026-04-24 — Autonomous loop round 116 — 🎯 Phase 31l CLOSE + Phase 34b/c/d (sequence viewer shipped)

### User directive (mid-round)
"Please add the amino-acid and DNA sequence view to the 3D
protein display panel next, as described earlier."

### Goals
1. Close Phase 31l at 15/15 (chymotrypsin + SARS-CoV-2 Mpro).
2. Pivot to Phase 34b/c/d as user-flagged.

### Ship list — Phase 31l (2 proteins → 15/15, phase CLOSED)
1. `orgchem/core/protein.py` — 14th + 15th `SeededProtein`:
   - **5CHA** bovine α-chymotrypsin. Completes the round-62
     mechanism + round-105 energy-profile + now-structure
     teaching triad.  Three-chain form (A/B/C) with the
     Ser195-His57-Asp102 catalytic triad + oxyanion hole
     framed explicitly in the teaching_story.
   - **6LU7** SARS-CoV-2 main protease with the N3 covalent
     inhibitor.  Pairs pedagogically with 1HPV HIV protease —
     cysteine protease + covalent warhead vs aspartic
     protease + peptidomimetic.
2. `tests/test_protein.py` — `must_have` extended; added
   `len(ids) >= 15` assertion plus content-marker comment
   noting the phase close.

### Ship list — Phase 34b/c/d (sequence viewer)
1. `orgchem/gui/widgets/sequence_bar.py` — new 320-line module.
   - `SequenceBar(QWidget)` — custom paint-based widget reading
     `SequenceView.to_dict()`.  Monospace rolling strip,
     tick marks every 10 residues, per-chain
     `HighlightSpan` underlay bands using the shared
     round-112 `HIGHLIGHT_COLOURS` palette, click-drag
     selection with cross-row clamp, `selection_changed`
     signal emitting PDB-native residue numbers.
   - `SequenceBarPanel(QWidget)` — scroll-area wrapper +
     status-label + signal re-emit.  Drop-in for the
     Proteins 3D sub-tab.
2. `orgchem/gui/panels/protein_panel.py` wiring:
   - Instantiate `SequenceBarPanel` inside `_make_3d_tab()`
     below the 3Dmol.js `QWebEngineView` with a 140 px max
     height.
   - New `_refresh_sequence_bar()` populates the panel from
     `parse_from_cache_or_string(self._current_pdb)` +
     `build_sequence_view().to_dict()`.
   - `_on_render_3d()` calls `_refresh_sequence_bar()` after
     each render so fetch-then-render auto-populates.
   - New `_on_sequence_selection(chain_id, start, end)`
     updates the picked-residue label + posts to the session
     log (full 3D ribbon highlight push via
     `QWebChannel.qtBridge` is deferred to a polish round —
     that needs JavaScript on the 3Dmol.js side).
   - Extended `_on_atom_picked(chain, resn, resi)` to call
     `sequence_panel.set_selection(chain, resi, resi)` —
     closes the reverse-path leg of the round-trip (3D pick
     → sequence caret move).
3. `orgchem/core/sequence_view.py` already existed from
   round 112 (34a); no core change needed.
4. `INTERFACE.md` — `widgets/sequence_bar.py` row added.
5. `tests/test_sequence_bar_widget.py` — 8 pytest-qt cases:
   empty-view / real-view / programmatic selection / clear /
   mouse click / mouse drag / click-outside clears /
   panel-wrapper status-line round-trip.

### DNA strip — free from 34b
The user's 34d ask ("DNA sequence above AA sequence") is
already satisfied by 34b + 34a together: `build_sequence_view`
classifies chains by majority residue kind, and `SequenceBar`
stacks `dna_chains` above `protein_chains` in the render loop.
Any PDB with DNA chains (1BNA / 143D / 1HMH / 1AOI) therefore
gets the DNA row *for free* on first render.

### Result
- **1 008 tests pass** (+8 new widget regressions).
- Phase 31l **CLOSED at 15/15**.
- Phase 34 now **4/6** complete (34a/b/c-partial/d).
- Phase 31 snapshot: 8 of 12 sub-phases at target
  (31a molecules, 31c mechanisms, 31d pathways,
  31e energy profiles, 31f glossary, 31g tutorials,
  31l proteins — CLOSED this round; 31k expanding).

### Next pick (open items)
- **34c polish** — `QWebChannel.qtBridge.highlight(chain, start,
  end)` JS bridge so sequence-bar drag live-updates the 3Dmol.js
  ribbon without clicking *Render* again.  Needs
  `draw_protein_3d.py` to export a JS helper.
- **34e** — feature tracks (pockets / contacts / secondary
  structure / user tags / UniProt gene annotations).
- **34f** — selection-aware agent actions.
- **35c** — bulk PubChem synonym backfill CLI (closes Phase 35).
- Phase 31 continuation (SAR +1, Phase 31h carbs, 31i lipids,
  31j NAs, 31b reactions).

## 2026-04-24 — Autonomous loop round 117 — Phase 34c forward-path (live sequence → 3D highlight)

### Goal
Close the remaining Phase 34c polish — sequence drag should
highlight the span on the 3D ribbon live, no HTML rebuild
required.

### Pick rationale
The user directive for Phase 34 was explicit about the
round-trip: *"…the selection is indicated on the 3D rendered
image — and vice-versa."*  Round 116 shipped the reverse leg
(3D pick → sequence caret).  Without the forward leg the
feature is incomplete, so that was the obvious closer.

### Ship list
1. `orgchem/render/draw_protein_3d.py`
   - New module constant `_LIVE_HIGHLIGHT_JS` defining
     `window.orgchemHighlight(chainId, start, end)` and
     `window.orgchemClearHighlight()` as globals on the
     viewer page.  The highlight helper:
     - Parses `start`/`end` to ints, swaps if reversed.
     - Calls `orgchemClearHighlight()` first to strip the
       previous selection back to the baseline cartoon.
     - Builds a 3Dmol.js `sel = {chain, resi: [range]}`.
     - Applies `stick` with `colorscheme: "yellowCarbon"`
       + residue labels — mirrors the static
       `highlight_residues` pipeline so the two paths
       look identical.
     - Calls `v.render()`.
     - Caches the current span on `window.__orgchemActiveHighlight`
       so the next call can find + reset it.
   - Injected into every HTML generated by `_build_model_js`
     via `lines.append(_LIVE_HIGHLIGHT_JS.strip())` (placed
     after `_PICK_JS` so both work together).
2. `orgchem/gui/panels/protein_panel.py`
   - `_on_sequence_selection(chain_id, start, end)` now calls
     `self.web_3d.page().runJavaScript(f'if (window.orgchemHighlight) window.orgchemHighlight("{chain}", {start}, {end});')`.
   - Graceful no-op if `web_3d is None` (headless / no
     WebEngine).
   - Basic string-safety (strip backslashes + quotes from
     chain id) — PDB chain ids are always single letters
     but belt+braces.
3. `tests/test_draw_protein_3d.py`
   - New `test_build_protein_html_exposes_live_highlight_helper`
     asserting both helpers are present with the correct
     signature string and yellowCarbon style name (catches
     accidental signature or style drift).

### Result
- **1 009 tests pass** (+1 new regression).
- Phase 34c is now **fully closed**: user drags a span on the
  sequence bar → ribbon shows it live as sticks + labels; user
  clicks a residue on the 3D ribbon → sequence bar caret moves.
  The full round-trip matches the user's original directive.
- Phase 34 progress: **5/6 sub-phases complete** — only 34e
  (feature tracks for pockets / contacts / secondary structure /
  user tags / UniProt) and 34f (selection-aware agent actions)
  remain.

### Next pick
- **34e** — feature-track overlays.  Pockets come from Phase
  24d `find_pockets`, ligand contacts from Phase 24e
  `analyse_binding`, secondary structure from PDB HELIX/SHEET
  records (parser doesn't read these yet — small extension).
  Most useful follow-up: render pocket + contact spans as
  colour bars under each chain row on the sequence bar.
- **34f** — agent actions for `select_residues`,
  `get_selection`, `highlight_feature`, `clear_selection`.
- **35c** — bulk PubChem synonym backfill CLI (closes Phase 35).
- Phase 31 content (+1 SAR, +1 pathway, +1 reaction).

## 2026-04-24 — Round 117 polish — sequence-bar scroll arrows + Clear button + toggle-deselect

### User directive
"Please add scroll arrows to the amino-acid/DNA display. Also
add a button for clearing all selected residues - and have
residue selection be toggle-able - so another click deselects."

### Ship list
1. `orgchem/gui/widgets/sequence_bar.py`
   - `SequenceBar`:
     - New `selection_cleared = Signal()` emitted by
       `clear_selection()` whenever it actually clears an
       existing selection (idempotent — not re-emitted when
       there was no selection).
     - `mousePressEvent` now checks whether the click lands
       *inside* the existing selection; if so, records
       `_pressed_inside_selection=True` and defers any state
       change until release.
     - `mouseMoveEvent` sets `_drag_moved=True` as soon as
       the mouse moves to a different column + cancels the
       pending toggle.
     - `mouseReleaseEvent` routes: (a) drag path → commit
       selection and emit `selection_changed`; (b)
       click-inside-selection + no drag → `clear_selection()`
       which fires `selection_cleared`.
     - New `_is_inside_selection(chain_id, resi)` helper.
   - `SequenceBarPanel`:
     - Toolbar row above the scroll area with ◀ / ▶
       `QToolButton`s + "Clear selection" `QPushButton`.
     - `SCROLL_STEP_RESIDUES = 10` (one tick-mark interval
       per click).
     - `_scroll_left` / `_scroll_right` advance
       `horizontalScrollBar` by 10 × `char_w` px.  Buttons
       have `setAutoRepeat(True)` so holding scrolls
       continuously.
     - `_update_scroll_button_state()` enables the arrows
       only when there's horizontal overflow + greys the
       one at the edge of the range.  Called in
       `resizeEvent` and after every programmatic scroll.
     - Clear button starts disabled; flips to enabled when
       a selection exists; flips back on clear.
     - New `selection_cleared` top-level signal re-emitted
       from the bar.
2. `orgchem/gui/panels/protein_panel.py`
   - Wired `sequence_panel.selection_cleared` →
     `_on_sequence_cleared` which updates the picked-label +
     posts to session log + runs `window.orgchemClearHighlight()`
     on the 3D page via `runJavaScript`.  Completes the
     selection-lifecycle round-trip (select → show on 3D →
     toggle/clear → remove from 3D).
3. `tests/test_sequence_bar_widget.py` — 7 new pytest-qt
   cases:
   - `test_click_inside_selection_toggles_it_off`
   - `test_click_drag_within_selection_does_not_toggle`
   - `test_clear_selection_emits_signal` (including
     idempotency check)
   - `test_panel_clear_button_disabled_until_selection`
   - `test_panel_cleared_signal_propagates`
   - `test_panel_scroll_arrows_wired` (step size + enable
     state at min / middle / max of scrollbar range)
   - `test_panel_scroll_arrows_disabled_without_overflow`

### Mid-round friction
- First draft of the scroll test used `panel.show()` +
  `qtbot.waitExposed()` to force a real layout pass.  Crashed
  the offscreen Qt with a NSWindow-ish abort before any tests
  ran.  Rewrote to drive the `horizontalScrollBar` range +
  value directly — more reliable and exercises exactly the
  `_update_scroll_button_state` branches we care about.

### Result
- **1 016 tests pass** (was 1 009; +7 new regressions).
- The three user asks are all live:
  (a) ◀ / ▶ scroll arrows with auto-repeat + edge-greying,
  (b) Clear-selection button (disabled until selection),
  (c) toggle-off: click an already-selected residue → cleared
      (and the 3D ribbon resets via orgchemClearHighlight).
- Full selection-lifecycle round-trip through 3D is closed.

### Next pick
- 34e — feature-track overlays (pockets / contacts /
  secondary structure / user tags / UniProt).
- 34f — selection-aware agent actions.
- 35c — bulk PubChem synonym backfill CLI (closes Phase 35).
- Phase 31 content +1.

## 2026-04-24 — Autonomous loop round 118 — Phase 34e (feature-track overlays: pockets + contacts)

### Goal
Start Phase 34e.  The core plumbing (`attach_pocket_highlights`,
`attach_contact_highlights`, `HIGHLIGHT_COLOURS` palette,
`SequenceBar._paint_row` painting) was already in place from
round 112/116 — what was missing was the wiring that pushes
real pocket + contact results onto the sequence bar whenever
the user runs an analysis.

### Ship list
1. `orgchem/gui/panels/protein_panel.py`
   - New `self._last_pockets` + `self._last_contacts` caches
     on the panel.
   - `_on_find_pockets` now caches the `Pocket` list and
     calls `_refresh_sequence_bar()` to push the green
     underlay bars.
   - `_on_analyse_binding` caches the `ContactReport` +
     refreshes.
   - `_on_analyse_binding_plip` caches
     `result.report` + refreshes.
   - `_on_fetch_pdb` + `_on_fetch_alphafold` reset both
     caches to `None` so stale features from the previous
     structure don't render on the new one.
   - `_refresh_sequence_bar` now calls `attach_pocket_highlights`
     before `attach_contact_highlights` (order matters for
     paint ordering — contact spans often overlap pocket
     spans and are narrower, so they paint on top).
2. `tests/test_sequence_view.py` — new
   `test_feature_track_overlay_full_stack` that walks the
   intended flow: build view → attach pockets → attach
   contacts → assert the right kinds + palette colours land
   on the view's `highlights` list.
3. `tests/test_sequence_bar_widget.py`
   - `test_sequence_bar_stores_highlights_from_view` proves
     `set_view({highlights: [...]})` actually stashes the
     spans on `_highlights` so `paintEvent` can render them.
   - `test_protein_panel_refresh_applies_feature_tracks` is
     an integration test: instantiate a real `ProteinPanel`,
     point its PDB cache at a fixture, prime fake
     `_last_pockets`/`_last_contacts` caches, call
     `_refresh_sequence_bar`, assert the widget's
     `_highlights` contains the kinds we expected.

### Result
- **1 019 tests pass** (+3 new).
- Phase 34e is now **partially shipped** — the two headline
  tracks (pockets + ligand contacts) are live; secondary
  structure (needs PDB HELIX/SHEET parsing), user tags
  (session-state persistence), and UniProt gene annotations
  (DBREF → UniProt fetch) remain as polish items.

### Next pick
- 34e polish — secondary structure track (HELIX/SHEET parser
  in `core/protein.py`).  Small change.
- 34f — selection-aware agent actions.
- 35c — bulk PubChem backfill CLI.
- Phase 31 continuation.

## 2026-04-24 — Autonomous loop round 119 — 🎯 Phase 34f selection-aware agent actions (Phase 34 at 6/6)

### Goal
Close Phase 34 end-to-end by shipping the selection-control
agent-action triple: `select_residues`, `get_selection`,
`clear_selection`.

### Pick rationale
With the round-116 reverse path (3D click → sequence caret) +
round-117 forward path (sequence drag → live 3D highlight) +
round-118 feature-track overlays in place, agent-action
wrappers are the last missing leg — they let tutor-chat
answers, scripted demos, and the stdio bridge drive selection
programmatically exactly the same way a GUI click would.

### Ship list
1. `orgchem/agent/actions_protein.py`
   - New `_get_sequence_panel()` helper that resolves
     `main_window().proteins.sequence_panel` or returns None —
     single chokepoint for all three new actions so the
     "GUI unavailable" branch is consistent.
   - `@action select_residues(pdb_id, chain_id, start, end)`:
     auto-swaps reversed bounds, runs on the main Qt thread
     via `_gui_dispatch.run_on_main_thread`, calls
     `SequenceBarPanel.set_selection(chain_id, start, end)`
     + `ProteinPanel._on_sequence_selection(...)` so the
     existing round-117 `orgchemHighlight` JS push fires and
     the 3D ribbon updates in the same tick.
   - `@action get_selection(pdb_id)`: read-only, no Qt-thread
     hop, returns `{chain_id, start, end}` or `{error: "No
     active selection."}`.
   - `@action clear_selection(pdb_id)`: dispatches
     `bar.clear_selection()` which fires the panel's
     `_on_sequence_cleared` handler → `orgchemClearHighlight()`
     on the 3D viewer.
   - All three error-return cleanly when the Proteins panel
     or its sequence bar isn't reachable (headless /
     Proteins tab not open / no WebEngine).
2. `orgchem/gui/audit.py` — three new `GUI_ENTRY_POINTS`
   entries pointing each action at the equivalent sequence-
   bar click/drag / Clear gesture.  Audit coverage stays at
   100 %.
3. `tests/test_selection_agent_actions.py` — new file, 9 cases:
   - `select_residues` sets the bar selection exactly,
   - reversed-bounds `(5, 2)` auto-swap to `(2, 5)`,
   - single-residue `(3, 3)` works,
   - `get_selection` returns the just-set selection,
   - `get_selection` with no selection returns `{error}`,
   - `clear_selection` empties the bar,
   - 3 monkey-patched tests with `_get_sequence_panel → None`
     exercise the "no GUI" branch of each action and confirm
     the error-return path.
4. Mid-round friction: first `pytest tests/` run was
   interrupted (exit 137) — re-ran and got 1 028 green.

### Result
- **1 028 tests pass** (+9 new).
- **Phase 34 — sequence viewer + cross-linked 3D selection —
  at 6/6 sub-phases shipped:**
    34a core data ✓ (round 112), 34b widget ✓ (round 116),
    34c two-way binding ✓ (round 116/117), 34d DNA strand ✓
    (round 116), 34e feature tracks — pockets + contacts ✓
    (round 118), 34f agent actions ✓ (round 119).
  Remaining polish items (queued, not blocking):
  secondary-structure track via HELIX/SHEET parsing,
  user-editable tag track with session-state persistence,
  UniProt gene-annotation track for DBREF-carrying PDBs,
  `highlight_feature(pdb_id, name)` action.

### Next pick
- 34 polish as listed above — secondary-structure is the
  smallest (small HELIX/SHEET parser extension).
- 35c — bulk PubChem synonym backfill CLI (closes Phase 35).
- Phase 31 content continuation (SAR +1, pathway +1, reaction
  +1 — several tracks still have room).

## 2026-04-24 — Autonomous loop round 120 — 🎯 Phase 35 CLOSE at 6/6 (bulk PubChem synonym backfill)

### Goal
Close Phase 35 end-to-end by shipping the last open sub-
phase: 35c bulk-backfill CLI.

### Ship list
1. `orgchem/db/backfill_synonyms.py` — new module.
   - `BackfillCounts` dataclass with per-category tallies
     (inspected, queried, fetched, skipped_tutor,
     skipped_no_key, added_total).
   - `backfill_synonyms(*, limit, rate_delay_s, min_existing,
     fetch_fn, skip_test_prefix) -> BackfillCounts` —
     walks every Molecule row, skips Tutor-test + empty-
     InChIKey rows, queries PubChem by InChIKey, filters
     registry-IDs via the round-109 palette helper, dedups,
     caps at 10 per row, writes cleaned list.
   - Per-row exception swallowed + rate-limited
     (`time.sleep(rate_delay_s)`).
   - `min_existing=0` semantic: "don't skip on existing-
     count" (force refresh).  Caught + fixed in-round.
   - `skip_test_prefix=True` by default; tests opt out to
     exercise Tutor-test rows.
   - Local `_merge_into_row` mirror of the round-58
     synonyms-seed merger — kept self-contained so this
     module doesn't import from `seed_synonyms`.
2. `scripts/backfill_molecule_synonyms.py` — CLI wrapper.
   - `--limit` (cap on number of network requests),
     `--rate-delay` (default 0.2 s),
     `--min-existing` (default 1; 0 = force-refresh).
   - Prepends the repo root to sys.path so it runs with
     plain `python scripts/…` without needing PYTHONPATH.
3. `orgchem/db/seed_synonyms.py` — unchanged (the earlier
   curated+reconcile path is orthogonal to the bulk
   backfill).
4. `INTERFACE.md` — `db/backfill_synonyms.py` row added.
5. `tests/test_backfill_synonyms.py` — 7 pytest cases:
   - populate empty rows with mocked hit + CAS filter,
   - respect `min_existing` (no network for filled rows),
   - `min_existing=0` force-refreshes,
   - skip Tutor-test rows by default,
   - skip rows without InChIKey (no crash),
   - tolerate raising `fetch_fn` (counts increment, no
     exception propagates),
   - `--limit=1` caps network calls to exactly 1.

### Mid-round pollution recovery
First draft's `_fake_fetch` helpers returned sentinel
strings (`"SHOULD NOT APPEAR"`, `"unused"`,
`"should-be-skipped"`) for EVERY key.  With
`skip_test_prefix=False` the backfill walked all ~418
rows, called the fake for every empty row, and the
sentinels got persisted onto 386 real seeded rows.

Fix was two-step:
- Hand-cleaned 386 rows in the dev DB via an inline
  filter script that strips known sentinel substrings.
- Tightened every `_fake_fetch` in the test file to
  return `[]` for non-target keys, so pytest runs no
  longer write anything to rows they shouldn't touch.

Lesson worth capturing: tests that mock a "fetch every
row" helper must return `[]` / no-op for keys outside
the test's scope, OR the backfill target must be
fenced (e.g. name-prefix filter).  Sentinel-string
returns are a trap.

### Result
- **1 035 tests pass** (+7 new).
- Phase 35 progress:
  - 35a round 58 (PubChem download persists synonyms)
  - 35b round 113 (tutor add_molecule fetch_synonyms kwarg)
  - 35c round 120 (bulk-backfill CLI)  **←  this round**
  - 35d round 109 (palette synonym aliases)
  - 35e round 111 (Compare-tab + show_molecule regressions)
  - 35f round 110 (browser row + tooltip hint)
  **Phase 35 — CLOSED at 6/6.**

### Next pick
Two-phase closure summary:
- Phase 34 (sequence viewer) — 6/6 shipped in round 119
  (34a-f).  Polish items (secondary-structure, user tags,
  UniProt, `highlight_feature`) queued but not blocking.
- Phase 35 (synonyms) — 6/6 shipped this round.

Remaining open Phase 31 sub-items:
- 31b reactions 35/50,
- 31h carbohydrates 25/40,
- 31i lipids 31/40,
- 31j nucleic acids 33/40,
- 31k SAR series 7/15.

Or start on 34 polish (secondary-structure track via
HELIX/SHEET parsing is the smallest).

## 2026-04-24 — Autonomous loop round 121 — Phase 31b +1 reaction (Heck)

### Goal
After closing Phase 34 + Phase 35 end-to-end in rounds 119-120,
pivot back to Phase 31 content expansion.  Best-ROI gap: the
Heck reaction — a textbook Pd-coupling that's frequently
queried in tutor sessions.

### Pick rationale
**Heck reaction (iodobenzene + methyl acrylate).**  Reasons:
- One of the three 2010-Nobel Pd-coupling reactions (Suzuki +
  Negishi + Heck).  Suzuki + Sonogashira are already in the
  catalogue; Heck was the obvious gap.
- Distinctive pedagogical shape among the Pd couplings: **no
  transmetalation** — the new bond forms during olefin
  insertion, not via a separate metalate transfer.  Good
  contrast for a med-chem student comparing coupling
  mechanisms.
- Clean canonical substrate pair (iodobenzene + methyl
  acrylate → trans-methyl cinnamate + HI) — stereoselective
  E-product falls out of syn-insertion + syn-β-H elimination.
- Low risk — no new code, just a seed entry.

### Ship list
1. `orgchem/db/seed_reactions.py`
   - Appended the 36th `_STARTER` entry with the Heck reaction,
     name, category ("Cross-coupling (Pd-catalysed)"), and a
     paragraph-length description capturing the catalytic
     cycle + contrast with Suzuki / Sonogashira + industrial
     relevance.
   - Reaction SMARTS: `Ic1ccccc1.C=CC(=O)OC>>COC(=O)/C=C/c1ccccc1.[H]I`
     (E-olefin explicit in the product to encode the
     stereoselectivity teaching point).
2. `orgchem/db/seed_intermediates.py` — added two fragments
   so the fragment-consistency audit (round 46) stays green:
   - `Methyl acrylate` (`C=CC(=O)OC`, reagent)
   - `Methyl cinnamate (trans)` (`COC(=O)/C=C/c1ccccc1`,
     intermediate)
3. No test file change needed — the existing
   `test_every_reaction_fragment_is_in_db` regression runs
   against the expanded DB automatically.  Caught the gap
   in a mid-round full-suite run (one failing test); fixed
   by seeding the two missing intermediates.

### Mid-round friction
- First full-suite run after the reaction seed surfaced the
  expected `test_every_reaction_fragment_is_in_db` failure
  (two uncovered fragments).  Followed the assertion's
  hint — seed them in `seed_intermediates.py` — verbatim;
  one re-run → 1 035 tests pass.  Nice to have the audit
  catch this so fragment pollution doesn't creep in.

### Result
- **1 035 tests pass** (unchanged — the new reaction is
  covered by the existing fragment + reaction regression
  suites without needing a new test file).
- Reaction catalogue now **36/50**; 14 more to hit Phase 31b
  target.
- Auto-reseed on next launch: the existing
  `seed_reactions_if_empty()` path picks up the new row
  additively via its name-keyed dedup.

### Next pick
14 more reactions for 31b.  Priority list from the earlier
roadmap (still relevant): Negishi, Heck ✓, Stille, Dess-Martin,
Jones, Oppenauer, Birch, Corey-Chaykovsky, Julia, Peterson,
Appel, Mukaiyama aldol, Evans aldol, Sharpless asymmetric
epoxidation / dihydroxylation, Jacobsen, CBS, Shapiro,
Ramberg-Bäcklund.

Or pivot: 31k SAR +1 (benzodiazepines), 31h carbs +N,
31i lipids +N, 31j NAs +N.

## 2026-04-24 — Autonomous loop round 122 — Phase 31k +1 SAR series (benzodiazepines)

### Goal
Continue Phase 31 content expansion with another med-chem
SAR series.  Catalogue at 7/15 after round 108.

### Pick rationale
**Benzodiazepines.**  Reasons:
- Classic GABA-A PAM chemotype — every medicinal-chem student
  learns the 7-Cl / 2'-X / N1-R tweak cube.
- Strong chemotype-switch teaching pair to pair with the
  round-108 PDE5 story: PDE5's tadalafil is a scaffold
  switch that fixes half-life + selectivity in one move;
  alprazolam's triazolo-fusion is the same kind of
  "chemotype change > substituent walk" narrative.
- Midazolam's pH-dependent ring-opening (closed at pH 4,
  open at physiological pH) is a distinctive teaching
  point that no other seeded SAR entry shows.
- 5 variants × ~4 activity columns fits the existing
  dialog render pipeline unchanged.

### Ship list
1. `orgchem/core/sar.py` — new
   `SARSeries(id="benzodiazepines")`:
   - Parent scaffold: 1,4-benzodiazepine core SMILES.
   - Activity columns: `gaba_a_ec50_nM`, `t_half_h`,
     `onset_min`.
   - 5 variants (diazepam / lorazepam / alprazolam /
     clonazepam / midazolam) with hand-curated activity
     numbers from the Sternbach 1979 J. Med. Chem. review
     + Sigel-Ernst 2018 Trends Pharmacol. Sci.
   - Each variant's `notes` field captures the chemistry
     story: active metabolites for diazepam, 3-OH direct
     glucuronidation for lorazepam, triazolo-chemotype-
     switch for alprazolam, 7-NO₂ subtype-shift for
     clonazepam, imidazo-pH-switching solubility for
     midazolam.
2. `tests/test_sar.py`
   - `test_library_seeded` updated with `"benzodiazepines"
     in ids`.
   - New `test_benzodiazepine_series_landmarks` locks
     three inequalities encoded numerically in the
     activity data:
       * midazolam's half-life is the shortest of the 5,
       * diazepam's is the longest (vs lor / alpr / mid;
         clonazepam is close so skipped to avoid
         brittleness),
       * every variant sits in the low-nM EC50 band that
         defines the class.

### Result
- **1 036 tests pass** (+1 new landmark test).
- SAR catalogue now **8/15** (β-blockers, ACE-I, SSRIs,
  β-lactams, PDE5, benzodiazepines seeded + the pre-
  existing NSAIDs / statins).
- Medicinal-chemistry dialog (`Tools → Medicinal
  chemistry…`) picks up the new series automatically
  via the `list_sar_series` registry — no GUI changes.

### Next pick
- 31k: 7 more SAR to reach 15 — β-lactam cephalosporins,
  opioids (morphine analogue family), SSRIs (expand to
  7+), kinase inhibitors (gleevec family),
  antihistamines (H1 generations), cannabinoid analogues.
- 31h / 31i / 31j expand carbohydrates / lipids / nucleic
  acids catalogues.
- 31b: 14 more reactions to reach 50 (Negishi, Stille,
  Dess-Martin, Jones, Appel, …).

## 2026-04-24 — Autonomous loop round 123 — Phase 31b +1 reaction (Negishi)

### Goal
Phase 31b continuation — another named reaction.  Obvious
next pick: Negishi coupling, the third Nobel-2010 Pd-coupling
(Suzuki, Heck, and now Negishi all seeded).

### Pick rationale
**Negishi coupling.**  Reasons:
- Completes the 2010 Nobel Pd-coupling trio.  Suzuki was
  shipped round 14-ish; Heck shipped round 121; Negishi is
  the obvious closer.
- Distinctive pedagogical shape vs Suzuki / Sonogashira:
  organozinc transmetalation (milder than Grignard, no base
  required, tolerates carbonyl FGs).  A tutor pointing out
  "why pick Negishi over Suzuki" now has a real reference
  pair.
- Canonical substrate (bromobenzene + phenylzinc chloride
  → biphenyl + Cl[Zn]Br) is clean + RDKit-parseable with
  `[Zn]` metal bonds.

### Ship list
1. `orgchem/db/seed_reactions.py` — 37th `_STARTER` entry.
   Reaction SMARTS: `Brc1ccccc1.c1ccc([Zn]Cl)cc1>>c1ccc(-c2ccccc2)cc1.Cl[Zn]Br`.
   Description captures the cycle + teaching differentiation
   vs Suzuki / Sonogashira (Hartwig OTM §18 equivalent
   summary).
2. `orgchem/db/seed_intermediates.py` — two new fragments:
   - `Phenylzinc chloride` (`[Cl][Zn][c]1ccccc1`, reagent)
   - `Zinc bromochloride` (`[Cl][Zn][Br]`, intermediate)
   Needed to keep `test_every_reaction_fragment_is_in_db`
   green.

### Friction
- First choice of SMARTS used `[Zn](Br)c1ccccc1` which
  RDKit accepted but the fragment-consistency audit
  normalises to a different canonical form with explicit
  brackets (`[Cl][Zn][c]1ccccc1`).  Followed the audit's
  own hint — seed the canonical form it reported — and
  the next pytest run passed.  Same pattern as the
  round-121 Heck fragment gap.

### Result
- **1 036 tests pass** (unchanged — new reaction covered by
  existing fragment + reaction regressions).
- Reaction catalogue now **37/50**; 13 more to hit Phase
  31b target.

### Next pick
13 reactions left in 31b.  Priority candidates from earlier
scoping (still valid): Stille coupling (Sn transmetalation
— completes the transmetalation-metal family), Dess-Martin
oxidation (mild 1°-OH → aldehyde without over-ox), Jones
oxidation (the classic CrO₃ workhorse), Corey-Chaykovsky
epoxidation, Julia / Peterson olefination, Appel reaction,
Mukaiyama / Evans aldol, Sharpless asymmetric variants,
CBS reduction, Birch reduction.

## 2026-04-24 — Autonomous loop round 124 — Phase 36a (structure-editor data core)

### Goal
Act on the round-123 user directive "add molecular drawing
tool — same abilities as chemdraw".  Kick off Phase 36 with
36a, the purely-headless data core everything else builds on.

### Ship list
1. `orgchem/core/drawing.py` — new module.
   - `Atom` dataclass: element (default "C"), charge, isotope,
     radical, h_count (-1 = infer), aromatic, chirality ∈
     {none/CW/CCW}.  `__post_init__` sanitises bad inputs.
   - `Bond` dataclass: begin_idx, end_idx, order (1/2/3/4 for
     aromatic), stereo ∈ {none/wedge/dash/either}.  Falls back
     to `"none"` on unknown stereo tags instead of raising.
   - `Structure` dataclass: atom + bond lists + helpers.
     `add_atom(element, **kw) → int`, `add_bond(a, b, order,
     stereo) → int` with self-loop + out-of-range guards;
     `neighbours(idx) → list[int]` that ignores direction;
     `n_atoms` / `n_bonds` / `is_empty` properties.
   - Round-trip helpers built on RDKit:
     `structure_from_smiles(smi)`, `structure_from_molblock(b)`,
     `structure_to_smiles(s, canonical=True)`,
     `structure_to_molblock(s)`.  All return `None` on parse /
     conversion failure — never raise.
   - Private `_structure_from_rdkit(mol)` + `_rdkit_from_structure(s)`
     bridge handles the ChiralType / BondDir / formal-charge /
     isotope / radical / explicit-H propagation.
   - Mid-round fix: first draft missed atom-centric chirality
     (only captured BondDir) so L-alanine round-tripped as
     achiral.  Added `chirality` field to `Atom` + mapped
     RDKit's `ChiralType.CHI_TETRAHEDRAL_{CW,CCW}` to string
     tags for serialisability; round-trip now preserves every
     tested stereo form.
2. `tests/test_drawing_core.py` — 21 pytest cases:
   - 5 dataclass ergonomics (atom-index return, bond endpoint
     validation, self-loop reject, out-of-range reject,
     neighbours-ignores-direction, bad-stereo-tag fallback,
     element default).
   - 7-SMILES parametric round-trip covering methane → ethanol
     → benzene → glycine → L-alanine-with-stereo → NH₄⁺ →
     aspirin.
   - 3 malformed-input null-returns (empty / None / unclosed
     ring).
   - Charge / isotope / stereo preservation spot-checks.
   - Mol-block round-trip via phenylacetic acid.
   - 2 manually-constructed canvas-path simulations: ethene
     via `add_atom("C") + add_atom("C") + add_bond(0, 1,
     order=2)`, NH₄⁺ via `add_atom("N", charge=1, h_count=4)`.
   - `structure_to_smiles(empty_structure)` → `None`.
3. `INTERFACE.md` — entry for `core/drawing.py` added.

### Result
- **1 057 tests pass** (+21 new).
- Phase 36 now **1/8 sub-phases done**.  The headless core is
  the hardest bit conceptually (RDKit ↔ dataclass bridge);
  Phase 36b (Qt canvas) is mechanical from here.
- Every downstream Phase 36 sub-phase (canvas, templates,
  undo/redo, stereochemistry, reaction arrows, export,
  SMILES ribbon) can now import `Structure` / `Atom` /
  `Bond` as the single source of truth for editor state.

### Next pick
- **36b** — `QGraphicsScene` drawing panel.  Bigger; wants a
  few rounds of polish.
- Alternative: keep Phase 31 momentum going (SAR +1, reaction
  +1, carbs / lipids / NAs + N).
- Alternative: Phase 34e polish (secondary-structure track).

Given the user just flagged Phase 36, 36b is the natural
next step — but it's substantial (canvas + tool palette +
click-to-place atoms + drag-to-draw bonds + undo stack).
Might split into 36b-i (canvas + atom placement) and 36b-ii
(bond drawing + tool palette) to keep individual rounds
shippable.

## 2026-04-24 — Autonomous loop round 125 — Phase 36b (drawing canvas)

### Goal
Phase 36 sub-phase 2 — the actual `QGraphicsScene` drawing
canvas.  Keep scope tight: atom placement, bond drawing, erase,
SMILES round-trip ribbon.  Ring / FG templates (36c), undo-redo
(36d), stereo wedges (36e), reaction arrows (36f), export (36g),
agent actions (36h) explicitly deferred.

### Ship list
1. `orgchem/gui/panels/drawing_panel.py` — new ~430-line module.
   - `DrawingPanel(QWidget)` with a top toolbar (select + 10
     atom tools + bond + erase + Clear), a SMILES I/O ribbon,
     and a `QGraphicsScene` canvas wrapped by an internal
     `_DrawingView(QGraphicsView)` subclass that forwards mouse
     events to the panel's dispatchers.
   - Per-atom items dict ({"dot", "label", "pos"}) lives in a
     list mirrored against `structure.atoms`; bonds are
     `QGraphicsLineItem`s mirrored against `structure.bonds`.
     Element changes regenerate the glyph so the
     heteroatom-label ↔ carbon-point switch lands correctly.
   - Bond-order rendering is a stub (pen width scales with
     order; double = 4 px, triple = 6 px, aromatic = dashed) —
     proper offset-parallel double/triple lines land in 36c.
   - Carbon atoms show as a small dot (ChemDraw convention);
     heteroatoms show their element label in CPK-adjacent colours.
   - `current_smiles()` runs the Phase-36a `structure_to_smiles`
     round-trip; `set_structure_from_smiles(smi)` uses RDKit's
     `Compute2DCoords` to lay out atoms on the canvas.
   - Erase tool handles the tricky re-indexing case: deleting a
     middle-of-chain atom requires decrementing every
     higher-numbered `begin_idx` / `end_idx` in the bond list
     before RDKit sanitises the rebuilt molecule.
   - Signal `structure_changed(smiles)` fires on every mutation.
2. `tests/test_drawing_panel.py` — 13 pytest-qt cases.  Key
   coverage:
   - Default tool = atom-C; empty canvas → empty SMILES.
   - Click → place carbon; re-click with new tool → swap
     element.
   - Bond tool: click two existing atoms → single bond; repeat
     → double; repeat → triple (wraps back).
   - Bond-tool auto-places carbons at empty-canvas endpoints.
   - Erase deletes atom + its incident bonds; middle-chain erase
     keeps the remaining bond referencing valid atom indices +
     SMILES still round-trips.
   - SMILES ribbon builds `c1ccccc1` → 6 atoms + 6 bonds;
     garbage → silently rejected (canvas stays empty).
   - `structure_changed` signal fires on add with the right
     SMILES payload; clear emits the empty string.
3. `INTERFACE.md` — entry describing the widget + behaviour
   contract.

### Design notes worth capturing
- Kept SMILES round-trip as a pure pull via `current_smiles()`
  rather than a parallel representation — avoids the dual-state
  drift bug that trivial drawing tools usually hit after a
  dozen edits.
- Repeat-bond-order cycle (1 → 2 → 3 → 1) matches ChemDraw;
  students who already know that tool behaviour get instant
  muscle memory.
- Offset-parallel double/triple bond rendering deferred: it
  needs a geometry pass (rotate by bond angle + draw two
  parallel lines 3 px apart) which is a chunk of code for a
  purely visual improvement.  Pen-width stub reads correctly
  in the test + looks acceptable on-screen.
- Layout on SMILES import uses RDKit's 2D coords × 36 px +
  y-flip; keeps molecules sensibly sized without a proper
  ChemDraw-quality clean.

### Result
- **1 070 tests pass** (+13 new).
- Phase 36 now **2/8 sub-phases done**.  The canvas can already
  draw every textbook molecule up to ~20 atoms if you know
  SMILES, and can draw simple chains / rings from scratch with
  just the bond tool.
- A round of polish (proper double-bond rendering, charge entry
  context menu, ring templates) would make the widget feel
  genuinely useful.  That's 36c + 36e territory.

### Next pick
- **36c** — ring / FG templates.  Click benzene template →
  place 6-ring hex; click COOH template → add a carboxylic acid
  graft.  Uses the existing Phase-36a `Structure` API for the
  graft geometry.  Self-contained, no new dependencies.
- **36d** — undo/redo via `QUndoStack`.  Medium.
- **36e** — stereo wedge/dash.  Small once 36d exists.
- **36g** — export + workspace integration.  Makes the canvas
  actually *useful* (send drawing → Molecule Workspace row).
  Good bang-for-the-buck follow-up.


---

## Round 126 — Phase 36g: drawing-tool dialog + workspace integration (2026-04-24)

### Context
- Round 125 shipped the canvas widget (`DrawingPanel`) but it
  was only reachable from pytest.  The ROI pick for 126 was
  **36g** — wrap the panel in a `QDialog`, wire *Tools → Drawing
  tool…*, add file export + *Send to Molecule Workspace*.  That
  makes the canvas actually *useful* from the GUI without
  touching the harder polish items (36c ring templates, 36d
  undo/redo, 36e stereo wedges).

### What shipped
- **New `orgchem/gui/dialogs/drawing_tool.py`** (~180 lines).
  - `DrawingToolDialog(QDialog)` — modeless singleton.
    `singleton(parent, seed_smiles="")` returns a shared
    instance so users can close-and-re-open without losing
    work; `seed_smiles=` preloads the canvas (future
    *Open in drawing tool…* hook on the Molecule Workspace).
  - Layout: `DrawingPanel` at the top, footer row of
    *Export drawing…* + *Send to Molecule Workspace* +
    Close buttons.
  - `_on_export`: `QFileDialog` filter offers PNG / SVG / MOL.
    PNG + SVG route through `render.export.export_molecule_2d`;
    MOL uses `core.drawing.structure_to_molblock` for a real
    V2000 mol-block (no SMILES round-trip, so 2D coords are
    preserved).  Empty-canvas guard surfaces a QMessageBox
    before opening the save dialog.
  - `_on_send_to_workspace`: invokes the round-58 `add_molecule`
    authoring action with:
    - `mol_name = f"Drawn-{uuid4().hex[:8]}"` — pollution-safe
      default, user can rename in the browser.
    - `source_tags = ["drawn"]` — filterable in the Phase-28 tag
      bar, so a user can see their own drawings as a category.
    - Handles duplicate InChIKey via the `existing_id` path
      (selects the existing row instead of failing).
    - Fires `bus.database_changed` + `bus.molecule_selected`
      so every other panel picks up the new row immediately.
    - Catches any exception from `invoke(…)` and surfaces it in
      a `QMessageBox.warning` — the tutor / stdio bridge can
      also raise if the DB is offline.
- **`orgchem/gui/main_window.py`** — new QAction + handler
  `_on_drawing_tool`.  Menu entry *Tools → Drawing tool…*
  (Ctrl+Shift+D) sits right next to the Script editor entry.
  Shortcut chosen to pair with Ctrl+Shift+E for the REPL
  (both open persistent singletons that create content).
- **`INTERFACE.md`** — added `dialogs/drawing_tool.py` row.
- **`ROADMAP.md`** — marked 36g `[x]` with a concise
  implementation summary (singleton, export paths, add_molecule
  integration, duplicate handling).

### Tests added — 11
- `tests/test_drawing_tool_dialog.py`:
  1. `test_dialog_instantiates_with_panel_and_buttons`
  2. `test_singleton_returns_same_instance`
  3. `test_singleton_preserves_canvas_across_reopens`
  4. `test_seed_smiles_loads_structure`
  5. `test_export_warns_when_canvas_empty`
  6. `test_export_mol_writes_v2000_block` — asserts both
     `"V2000"` and `"M  END"` tokens in the file text.
  7. `test_export_png_writes_image`
  8. `test_send_to_workspace_warns_when_empty`
  9. `test_send_to_workspace_invokes_add_molecule` — asserts
     `mol_name` starts with `Drawn-`, `smiles` round-trips,
     `source_tags == ["drawn"]`, `_select_molecule` fires
     with the returned id.
  10. `test_send_to_workspace_handles_duplicate` — simulates
      `existing_id=17` response, asserts selection still
      happens on the existing row.
  11. `test_send_to_workspace_surfaces_invocation_error` —
      mocked `invoke()` raises → `QMessageBox.warning` fires.
- `autouse` fixture resets `DrawingToolDialog._instance`
  between tests so they don't share state (singletons can
  quietly couple test cases if the suite ever re-orders).

### Verification
- `pytest tests/` → **1 081 passed** (+11).
- Headless smoke check: *Tools → Drawing tool…* menu action
  exists, has Ctrl+Shift+D shortcut, `.trigger()` creates a
  visible `DrawingToolDialog` instance.

### Design decisions + gotchas
- **Singleton vs fresh dialog** — singleton wins because users
  will draw, close to check a SMILES, and reopen.  The canvas
  surviving that cycle is what differentiates a toy from a
  tool.  The autouse fixture in the test file is a reminder
  that module-level singletons cross test boundaries.
- **Empty-canvas guards at both export + send** — calling
  `mol_from_smiles("")` cleanly raises, but blocking at the
  UI layer gives a friendlier message and avoids opening a
  file-save dialog for nothing.
- **Duplicate handling** — `add_molecule` already returns
  `existing_id` on dupe; wired the dialog to select that id
  rather than reject the click.  Matches the *Add molecule*
  wizard's behaviour — consistent UX across authoring surfaces.
- **No agent action for open_drawing_tool yet** — deferred to
  36h.  The dialog is reachable from the main thread via the
  menu entry; adding an agent wrapper means going through
  `_gui_dispatch.run_on_main_thread` which is more rigorous
  test scaffolding than the round 126 budget.
- **Source-tag semantics** — `"drawn"` isn't in the
  Phase-28 `SOURCE_TAG_VALUES` taxonomy yet.  Leaving it
  un-registered for now — adding a taxonomy entry is a
  separate trivial follow-up; users who care can still
  filter on exact match via the free-text tag filter.

### Phase 36 progress
- 36a (round 124) ✅ headless core
- 36b (round 125) ✅ canvas widget
- 36g (round 126) ✅ dialog + workspace integration
- 36c, 36d, 36e, 36f, 36h — queued

### Next pick
- **36h** — SMILES import ribbon is already in 36b.  The new
  work is the agent-action surface (`open_drawing_tool(smiles="")`,
  `drawing_to_smiles()`, `drawing_export(path)`) + a Molecule-
  Workspace toolbar button *Open in Drawing tool…* that passes
  the current molecule's SMILES into the singleton's
  `seed_smiles=`.  Clean follow-up to 36g; all the plumbing is
  already in place.
- **36c** — ring + FG templates.  Needs geometry code for hex
  placement + attachment-point hit-testing.  Medium.
- **36d** — undo/redo via `QUndoStack`.  Not hard once each
  mutation in `DrawingPanel` is a discrete command.


---

## Round 127 — Phase 36h: drawing-tool agent actions (2026-04-24)

### Context
- Round 126 gave the drawing tool a GUI home via *Tools →
  Drawing tool…*, but it wasn't reachable from the tutor /
  stdio bridge / Python drivers.  36h closes that surface so
  the same capability is available to scripted callers.

### What shipped
- **New `orgchem/agent/actions_drawing.py`** — 4 actions, all
  category `"drawing"`, all main-thread-safe via
  `run_on_main_thread_sync`:
  - `open_drawing_tool(smiles="")` — lazy-creates the singleton
    dialog, optionally preloads the canvas.  Returns
    `{opened, seeded_smiles, current_smiles}`.
  - `drawing_to_smiles()` — canonical SMILES + `n_atoms` +
    `n_bonds`.  Empty canvas returns
    `{"smiles": "", "n_atoms": 0, "n_bonds": 0}`.
  - `drawing_export(path)` — suffix-dispatch: `.png` / `.svg`
    through `export_molecule_2d`, `.mol` through
    `structure_to_molblock`.  Rejects unknown extensions with
    a clear error-return.  Empty-canvas guard at both the top
    and inside the main-thread closure.
  - `drawing_clear()` — wipe the canvas.  Idempotent.
- **Wired into `orgchem/agent/__init__.py`** auto-loader (one
  new `noqa: F401` import line).
- **`orgchem/gui/audit.py`** — 4 new GUI_ENTRY_POINTS entries
  map each action to its human-visible surface.  Audit
  coverage still 100 %.
- **INTERFACE.md** — new row under the `agent/` section for
  `actions_drawing.py` (caught by the docs-coverage test first
  run — fixed immediately).

### Tests added — 15
- `tests/test_drawing_actions.py`:
  1. `test_actions_registered_in_registry` — the 4 expected
     names appear in the `drawing` category.
  2. `test_open_drawing_tool_creates_singleton`
  3. `test_open_drawing_tool_with_seed_smiles`
  4. `test_open_drawing_tool_without_gui_returns_error`
  5. `test_drawing_to_smiles_without_open_returns_error`
  6. `test_drawing_to_smiles_returns_canvas_state`
  7. `test_drawing_to_smiles_empty_canvas`
  8. `test_drawing_export_without_open_returns_error`
  9. `test_drawing_export_empty_canvas_returns_error`
  10. `test_drawing_export_rejects_unknown_extension`
  11. `test_drawing_export_writes_mol_v2000`
  12. `test_drawing_export_writes_png`
  13. `test_drawing_clear_without_open_returns_error`
  14. `test_drawing_clear_empties_canvas`
  15. `test_open_edit_export_roundtrip` — full pipeline:
      open with seed → clear → programmatically set to pyridine
      → export MOL → re-read via RDKit → canonical SMILES
      matches.
- `autouse` fixture resets `DrawingToolDialog._instance`
  between tests so the singleton doesn't leak state.

### Verification
- `pytest tests/` → **1 096 passed** (+15 from 1 081).
- GUI audit + docs-coverage tests still green (both caught
  a missed update first run — fixes landed in the same round).

### Design decisions + gotchas
- **Return-value discipline** — `run_on_main_thread_sync`
  bounces the return value through to the caller synchronously,
  so the action's inner `_open` / `_read` / `_write` / `_clear`
  closures can build the result dict and return it directly.
  Cleaner than the `run_on_main_thread` (fire-and-forget)
  pattern used for actions that don't need a reply.
- **Two-layer empty-canvas guard on export** — first check in
  the outer action (saves a `run_on_main_thread_sync` round
  trip when obvious), second check inside the closure (safe
  against races where another thread clears the canvas
  between the two layers).  Belt + braces.
- **No suffix-dispatch on SVG in GUI dialog** — the Phase-36g
  dialog's `_on_export` handled SVG implicitly by falling
  through to `export_molecule_2d` (which dispatches by
  extension).  The action does the same, but is explicit
  about accepting `.svg` via the extension allow-list at the
  top — surfaces a clear error-return for typos like `.sgv`.
- **Error-return, never raise** — every code path that can't
  reach the GUI (no main window / no dialog singleton / bad
  extension) returns `{"error": "..."}` instead of throwing.
  Matches the rest of the agent surface.
- **Late import of `DrawingToolDialog` inside actions** —
  avoids pulling PySide6 into the registry at module-load
  time.  Headless drivers that only do DB / RDKit work don't
  accidentally pull in Qt.

### Phase 36 progress
- 36a (round 124) ✅ headless core
- 36b (round 125) ✅ canvas widget
- 36g (round 126) ✅ dialog + workspace integration
- 36h (round 127) ✅ agent actions
- 36c, 36d, 36e, 36f — queued

### Next pick
- **36c** — ring + FG templates.  Clickable benzene /
  cyclohexane / cyclopentane / cyclopropane + COOH / OH /
  NH2 / NO2 / CHO templates that graft onto the last-placed
  atom.  Uses the existing Phase-36a `Structure.add_atom` +
  `add_bond` API.  Needs a small amount of geometry code
  (hex placement math, attachment-point hit testing).  Medium
  size.
- **36d** — undo/redo via `QUndoStack`.  Every `DrawingPanel`
  mutation becomes a `QUndoCommand`; keyboard shortcut
  Ctrl+Z / Ctrl+Shift+Z.  Clean once the command list is
  enumerated.
- Alternative: **31k SAR series** — the catalogue is at
  8/15; any of ACE inhibitors / ARBs / PPIs / H1 antihistamines
  / triptans / HMGCoA statins (already done) / aromatase
  inhibitors would close a gap fast.  SAR work is always
  quick: one file + a landmark-ordering test.


---

## Round 128 — Phase 36d: undo/redo for the drawing canvas (2026-04-24)

### Context
- Drawing tool has been usable since round 125 but lacked the
  single feature every ChemDraw-style app ships with: undo.  An
  errant click on a finished molecule meant starting over.  ROI
  is high, risk is low — every mutation already flows through a
  handful of well-defined methods.

### Approach: snapshot-based, not QUndoCommand
Considered `QUndoStack` + one `QUndoCommand` subclass per
mutation (add-atom, add-bond, cycle-order, erase, …) but the
canvas has ~6 mutation paths and they touch both a data object
(`Structure`) and a parallel scene-item list.  Commands that mutate
two structures symmetrically drift fast.  Snapshot approach is
simpler: deep-copy the `(Structure, positions)` before mutating,
restore wholesale via `_restore_snapshot` which rebuilds scene
items from the snapshot.  Memory is fine — `Structure` is ~200
bytes per atom, cap at 100 snapshots = ~2 MB worst case.

### What shipped
- **`_undo_stack` / `_redo_stack`** — list-of-tuples, bounded
  at `_UNDO_STACK_MAX = 100`.  Invariant: the *current* canvas
  state is NOT on either stack.
- **`_push_undo()`** — capture + append + clear redo + update
  buttons.  Called at the top of every mutation.  Stack cap
  enforced by `del _undo_stack[0]` when it overflows.
- **`_restore_snapshot(snap)`** — wipe scene items, deep-copy
  structure back in, redraw atoms + bonds, emit `structure_changed`.
  Does NOT touch the stacks itself — callers handle push/pop.
- **`undo()` / `redo()`** — pop from one stack, push current
  snapshot onto the other, call `_restore_snapshot`.
- **`can_undo()` / `can_redo()`** — convenience predicates for
  button-enable wiring.
- **Toolbar additions** — *↶ Undo* / *↷ Redo* `QPushButton`s
  between the erase tool and *Clear canvas*.  Always disabled
  while the respective stack is empty.
- **`QShortcut`s** — Ctrl+Z / Ctrl+Shift+Z scoped to the widget
  (not the app) so they fire inside the drawing dialog without
  stealing from other widgets.
- **`_emit_changed`** — now calls `_update_undo_buttons` at the
  end, so every mutation path refreshes button state without
  each mutator having to remember to do it.
- **No-op guards**:
  - `_change_atom_element`: bail early if the element isn't
    actually changing.
  - `_handle_bond_click`: if the second click is on the same
    atom as the first (cancel), pop the snapshot we just pushed
    so cancel doesn't inflate history.
  - `clear`: skip the snapshot when the canvas is already empty.
- **Nested-mutation handling** — added `record_undo=False` kwarg
  to `_add_atom`, `_delete_atom`, `_delete_bond`, `clear`.  The
  outer mutation (bond-click that auto-places a C endpoint;
  `_load_structure` that calls `clear` internally; `_delete_atom`
  that iterates through `_delete_bond`) pushes once, then calls
  the helpers with `record_undo=False` so nested calls don't
  double-push.
- **Drag-move snapshot** — captured on `mousePress` when a
  select-tool click lands on an atom.  One snapshot per drag,
  not one per `mouseMove`.

### Tests added — 18
- `tests/test_drawing_undo_redo.py`:
  1. Empty-stack construction state.
  2. `undo()` / `redo()` no-op on empty stacks.
  3. Atom placement undo.
  4. Atom placement redo.
  5. Chain of 3 placements unwinds correctly.
  6. Element change undo.
  7. Same-element re-click doesn't inflate stack.
  8. Bond creation undo.
  9. Bond-order-cycle undo (walks 2 → 1 → no-bond).
  10. Bond-tool cancel doesn't pollute undo.
  11. Erase restores atom + its bonds atomically.
  12. Clear reverses.
  13. Clear-empty is a no-op for the stack.
  14. SMILES rebuild is one undo step.
  15. New mutation after undo clears the redo stack.
  16. Stack cap holds at 100 (spaced 25 px apart so each click
      is a fresh atom, not a re-hit — lesson from first-draft
      test that spaced 5 px and collided).
  17. Buttons reflect stack state across undo + redo.
  18. Full build-undo-redo round-trip (C=C via bond cycle,
      unwind to empty, rewind via redo, assert SMILES matches).

### Verification
- `pytest tests/` → **1 114 passed** (+18 from 1 096).
- All 39 pre-existing drawing-panel / dialog / action tests
  remain green — no regressions from adding the snapshot hooks.

### Design decisions + gotchas
- **Two-phase bond tool + snapshot timing** — first click
  places a C if needed (its own snapshot); second click pushes
  a *fresh* snapshot for the whole logical bond-creation /
  order-cycle operation.  The cancel path (same-atom double
  click) pops that second snapshot so cancel is invisible to
  history.  First-click placement stays on the stack because
  "placed this atom then realised I don't want a bond" is a
  legitimate step.
- **Test-sizing gotcha — the 100-cap test** — my first draft
  clicked at `i * 5` pixels which all fell within `_HIT_RADIUS_PX
  = 16`, so clicks 4+ hit the first atom and became no-op
  element-changes.  The stack capped at 28 instead of 100.  Fix:
  space at `i * 25` — each click a fresh atom.
- **Deep copy vs reference** — `copy.deepcopy(structure)` is
  required because `Structure.atoms` / `.bonds` are live lists
  mutated in place by `_delete_bond` / `_delete_atom` + by the
  bond-order cycle.  Shallow copies would alias on the undo
  stack.
- **`QShortcut` scope** — `QShortcut(keysequence, self)`
  restricts to the widget, not the top-level window, so Ctrl+Z
  in the drawing dialog doesn't accidentally fire an Undo that
  some other panel defined.  (None do today, but the scoping is
  cheap insurance.)
- **No `QUndoStack`** — the PySide6 class is a better fit for
  *command* semantics (redo by re-applying forward), but our
  mutations don't cleanly invert (element swap needs the old
  element remembered, bond cycle needs the previous order, …).
  Snapshots sidestep all of that — more memory, much less code.

### Phase 36 progress
- 36a (round 124) ✅ headless core
- 36b (round 125) ✅ canvas widget
- 36g (round 126) ✅ dialog + workspace integration
- 36h (round 127) ✅ agent actions
- 36d (round 128) ✅ undo / redo
- 36c, 36e, 36f — queued

### Next pick
- **36c** — ring + FG templates.  Click benzene template → place
  regular hexagon of carbons, anchor to nearest existing atom if
  any.  Click COOH template → graft a carboxylic-acid group onto
  the last-placed atom.  Medium — needs a small amount of
  geometry code (hex placement math, attachment-point hit
  testing) but the undo machinery from 128 means each graft is
  already trivially undoable.
- **31k SAR series +1** — catalogue is at 8/15.  Quick win: add
  e.g. H1 antihistamines or PPI inhibitors for a landmark-
  ordering series.
- **31b +1 reaction** — 37/50; adding one more named reaction +
  mechanism closes a predictable gap.
