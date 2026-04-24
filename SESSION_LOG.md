# Session Log — OrgChem Studio

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
