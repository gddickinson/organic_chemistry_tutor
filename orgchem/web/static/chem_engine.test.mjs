// Node test: the JS chemistry engine against RDKit / orgchem on every SMILES the app seeds.
// Fixture: tests/fixtures/chem_engine_fixture.json (python scripts/make_chem_fixture.py). Run: node chem_engine.test.mjs
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import assert from 'node:assert/strict';
import { analyse, atomSignature, parseSmiles } from './chem_engine.js';
import { MASSES } from './chem_masses.js';
import { functionalGroups } from './smarts.js';
import { computeFormula, ATOMIC_MASSES, ATOMIC_MASSES_INTEGER } from './formula_calc.js';

const here = dirname(fileURLToPath(import.meta.url));
const fx = JSON.parse(readFileSync(join(here, '../../../tests/fixtures/chem_engine_fixture.json'), 'utf8'));
const close = (a, b, tol = 1e-6) => Math.abs(a - b) <= tol * Math.max(1, Math.abs(b));
let fails = 0;
const fail = msg => { fails++; if (fails <= 25) console.log('FAIL', msg); };

// Mass tables match RDKit's periodic table exactly.
for (const [el, [avg, mono]] of Object.entries(fx.masses)) {
  if (!MASSES[el] || MASSES[el][0] !== avg || MASSES[el][1] !== mono) fail(`mass table ${el}`);
}
assert.deepEqual(ATOMIC_MASSES, fx.formula_tables.iupac);
assert.deepEqual(ATOMIC_MASSES_INTEGER, fx.formula_tables.integer);

// Known, documented difference: in Kekule porphyrin macrocycles RDKit's fused-ring aromaticity model marks the
// 18-pi pathway aromatic; the simpler per-cycle 4n+2 rule here does not (the seeded aromatic SMILES are fine).
const KNOWN = new Set(['C1=CC2=NC1=CC1=CC=C(C=C3C=CC(=N3)C=C3C=CC(=C2)N3)N1',
  'C1=CC2=NC1=CC1=CC=C(C=C3C=CC(=CC4=NC(=C2)C=C4)N3)N1']);

// Every seeded SMILES: atoms (aromaticity + H counts), formula, masses, charge, functional groups.
let n = 0, skipped = 0;
for (const m of fx.molecules) {
  if (m.error) continue;
  if (KNOWN.has(m.smiles)) { skipped++; assert.equal(analyse(m.smiles).formula, m.formula); continue; }
  n++;
  let r;
  try { r = analyse(m.smiles); } catch (e) { fail(`${m.smiles}: ${e.message}`); continue; }
  const sig = atomSignature(r.mol);
  if (sig !== m.atoms) fail(`${m.smiles} atoms\n   js    ${sig}\n   rdkit ${m.atoms}`);
  if (r.formula !== m.formula) fail(`${m.smiles} formula ${r.formula} != ${m.formula}`);
  if (!close(r.mw, m.mw, 1e-9)) fail(`${m.smiles} mw ${r.mw} != ${m.mw}`);
  if (!close(r.exact, m.exact, 1e-9)) fail(`${m.smiles} exact ${r.exact} != ${m.exact}`);
  if (r.charge !== m.charge) fail(`${m.smiles} charge`);
  if (r.heavy !== m.heavy) fail(`${m.smiles} heavy ${r.heavy} != ${m.heavy}`);
  const g = functionalGroups(r.mol);
  if (g.join() !== m.groups.join()) fail(`${m.smiles} groups\n   js    ${g}\n   rdkit ${m.groups}`);
}

// Empirical / molecular formula calculator (port of orgchem/core/formula.py).
for (const c of fx.formula) {
  const masses = c.masses === 'integer' ? ATOMIC_MASSES_INTEGER : ATOMIC_MASSES;
  let r = null, err = null;
  try { r = computeFormula(c.pct, c.mw, { masses }); } catch (e) { err = e; }
  if (c.error) { if (!err) fail(`${c.name}/${c.masses} should raise`); continue; }
  if (err) { fail(`${c.name}/${c.masses}: ${err.message}`); continue; }
  if (r.empirical !== c.empirical || r.molecular !== c.molecular || r.scale !== c.scale) fail(`${c.name}/${c.masses} formula`);
  if (!close(r.empiricalMass, c.empirical_mass, 1e-9) || !close(r.maxResidual, c.max_residual, 1e-9)) fail(`${c.name}/${c.masses} numbers`);
}

// Parser errors are reported, not swallowed.
for (const bad of ['C1CC', 'C(C', 'X', '[Zz]']) assert.throws(() => parseSmiles(bad), new RegExp('.'), bad);

console.log(`${n} SMILES + ${fx.formula.length} formula cases checked (${skipped} known aromaticity differences: formula only), ${fails} failures`);
if (fails) process.exit(1);
