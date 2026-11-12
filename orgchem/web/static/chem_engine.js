// Small chemistry engine for the browser: SMILES -> molecule graph with RDKit-style implicit hydrogens, aromaticity
// perception for Kekule input, molecular formula (Hill order, RDKit CalcMolFormula style), average molecular weight
// (RDKit MolWt) and monoisotopic mass (RDKit ExactMolWt). Functional groups (the app's SMARTS list) live in smarts.js.
// chem_engine.test.mjs checks it against RDKit on every SMILES the app seeds (tests/fixtures/chem_engine_fixture.json).
import { MASSES } from './chem_masses.js';

export const ELECTRON_MASS = 0.00054857990907;
export const SYMBOLS = Object.keys(MASSES);
export const atomicNumber = sym => SYMBOLS.indexOf(sym) + 1;
// Allowed valences of the SMILES organic subset (RDKit's defaults for these elements).
const VALENCES = { B: [3], C: [4], N: [3, 5], O: [2], P: [3, 5, 7], S: [2, 4, 6], F: [1], Cl: [1], Br: [1], I: [1, 3, 5] };
const ORGANIC = ['Cl', 'Br', 'B', 'C', 'N', 'O', 'P', 'S', 'F', 'I'];
const AROM_ORGANIC = ['b', 'c', 'n', 'o', 'p', 's'];
const BOND = { '-': 1, '=': 2, '#': 3, '$': 4, ':': 1.5, '/': 1, '\\': 1 };

function err(msg, i) { const e = new Error(`${msg} at position ${i + 1}`); e.pos = i; throw e; }

// Parse a SMILES string. Returns { atoms: [{el, arom, charge, iso, hExplicit, bracket}], bonds: [{a, b, order}] }.
export function parseSmiles(smi) {
  const s = String(smi || '').trim();
  if (!s) throw new Error('Empty SMILES');
  const atoms = [], bonds = [], stack = [], rings = {};
  let prev = -1, pend = null, i = 0;
  const addAtom = at => {
    const idx = atoms.push(at) - 1;
    if (prev >= 0) bonds.push({ a: prev, b: idx, order: pend ?? 0 });
    prev = idx; pend = null;
  };
  while (i < s.length) {
    const ch = s[i];
    if (ch === '(') { if (prev < 0) err('Branch before any atom', i); stack.push(prev); i++; continue; }
    if (ch === ')') { if (!stack.length) err('Unmatched )', i); prev = stack.pop(); pend = null; i++; continue; }
    if (ch === '.') { prev = -1; pend = null; i++; continue; }
    if (ch in BOND) { pend = BOND[ch]; i++; continue; }
    if (/[0-9%]/.test(ch)) {
      if (prev < 0) err('Ring bond before any atom', i);
      let n;
      if (ch === '%') { n = s.slice(i + 1, i + 3); if (!/^\d\d$/.test(n)) err('Bad %nn ring number', i); i += 3; }
      else { n = ch; i++; }
      if (rings[n]) {
        const r = rings[n]; delete rings[n];
        if (r.atom === prev) err('Ring bond to itself', i);
        bonds.push({ a: r.atom, b: prev, order: pend ?? r.order ?? 0 });
      } else rings[n] = { atom: prev, order: pend };
      pend = null; continue;
    }
    if (ch === '[') {
      const j = s.indexOf(']', i);
      if (j < 0) err('Unclosed [', i);
      addAtom(parseBracket(s.slice(i + 1, j), i));
      i = j + 1; continue;
    }
    if (ch === '*') { addAtom({ el: '*', arom: false, charge: 0, iso: 0, hExplicit: 0, bracket: true }); i++; continue; }
    const two = s.slice(i, i + 2), sym = ORGANIC.find(e => s.startsWith(e, i));
    if (sym && !(two === 'Cl' && false)) { addAtom({ el: sym, arom: false, charge: 0, iso: 0, hExplicit: 0, bracket: false }); i += sym.length; continue; }
    if (AROM_ORGANIC.includes(ch)) { addAtom({ el: ch.toUpperCase(), arom: true, charge: 0, iso: 0, hExplicit: 0, bracket: false }); i++; continue; }
    err(`Unexpected '${ch}'`, i);
  }
  if (stack.length) throw new Error('Unclosed branch (');
  if (Object.keys(rings).length) throw new Error(`Unclosed ring bond ${Object.keys(rings).join(', ')}`);
  // Unspecified bonds: aromatic between two aromatic atoms, else single.
  for (const b of bonds) if (!b.order) b.order = atoms[b.a].arom && atoms[b.b].arom ? 1.5 : 1;
  return finish(atoms, bonds);
}

function parseBracket(t, at) {
  const m = /^(\d*)([A-Z][a-z]?|[a-z][a-z]?|\*)(@*(?:TH\d|AL\d|SP\d|TB\d+|OH\d+)?)?(H\d*)?([+-]+\d*)?(:\d+)?$/.exec(t);
  if (!m) err(`Cannot read bracket atom [${t}]`, at);
  let sym = m[2], arom = false;
  if (/^[a-z]/.test(sym)) {
    if (!['b', 'c', 'n', 'o', 'p', 's', 'se', 'as', 'te'].includes(sym)) err(`Unknown aromatic atom ${sym}`, at);
    arom = true; sym = sym[0].toUpperCase() + sym.slice(1);
  } else if (sym !== '*' && !MASSES[sym]) err(`Unknown element ${sym}`, at);
  let charge = 0;
  if (m[5]) {
    const sign = m[5][0] === '+' ? 1 : -1, digits = m[5].replace(/[+-]/g, '');
    charge = sign * (digits ? +digits : m[5].length);
  }
  return { el: sym, arom, charge, iso: m[1] ? +m[1] : 0, hExplicit: m[4] ? (m[4].length > 1 ? +m[4].slice(1) : 1) : 0, bracket: true };
}

// RDKit-like sanitisation: drop plain [H] atoms into their neighbour's H count, charge-separate N(=O)=O,
// work out implicit hydrogens, then perceive aromaticity.
function finish(atoms, bonds) {
  const nb = atoms.map(() => []);
  bonds.forEach((b, k) => { nb[b.a].push(k); nb[b.b].push(k); });
  const drop = new Set();
  atoms.forEach((a, i) => {
    if (a.el !== 'H' || a.iso || a.charge || nb[i].length !== 1) return;
    const b = bonds[nb[i][0]], o = b.a === i ? b.b : b.a;
    if (atoms[o].el === 'H' || b.order !== 1) return;
    drop.add(i); atoms[o].hExplicit += 1;
  });
  if (drop.size) {
    const map = [], keep = [];
    atoms.forEach((a, i) => { if (!drop.has(i)) { map[i] = keep.length; keep.push(a); } });
    const nbonds = bonds.filter(b => !drop.has(b.a) && !drop.has(b.b)).map(b => ({ a: map[b.a], b: map[b.b], order: b.order }));
    return finish2(keep, nbonds);
  }
  return finish2(atoms, bonds);
}

function finish2(atoms, bonds) {
  const mol = { atoms, bonds, nbrs: atoms.map(() => []) };
  bonds.forEach((b, k) => { mol.nbrs[b.a].push([b.b, k]); mol.nbrs[b.b].push([b.a, k]); });
  // Nitro-style N(=O)=O -> [N+](=O)[O-] (RDKit cleanUp).
  atoms.forEach((a, i) => {
    if (a.el !== 'N' || a.charge) return;
    const dbl = mol.nbrs[i].filter(([j, k]) => bonds[k].order === 2 && atoms[j].el === 'O' && !atoms[j].charge);
    if (dbl.length === 2 && valenceSum(mol, i) + a.hExplicit === 5) {
      a.charge = 1; bonds[dbl[1][1]].order = 1; atoms[dbl[1][0]].charge = -1;
      a.fixedH = atoms[dbl[1][0]].fixedH = true; // charges set: no further implicit H on either atom
    }
  });
  atoms.forEach((a, i) => { a.hImplicit = a.bracket || a.fixedH ? 0 : implicitH(mol, i); });
  perceiveAromaticity(mol);
  atoms.forEach(a => { a.hTotal = a.hExplicit + a.hImplicit; });
  return mol;
}

function valenceSum(mol, i) { return mol.nbrs[i].reduce((s, [, k]) => s + mol.bonds[k].order, 0); }

function implicitH(mol, i) {
  const a = mol.atoms[i], allowed = VALENCES[a.el];
  if (!allowed) return 0;
  if (a.arom) {
    if (a.el !== 'C' && a.el !== 'B') return 0;
    let v = 1;
    for (const [, k] of mol.nbrs[i]) v += mol.bonds[k].order === 1.5 ? 1 : mol.bonds[k].order;
    return Math.max(0, (a.el === 'C' ? 4 : 3) - v);
  }
  const v = valenceSum(mol, i) + a.hExplicit, ok = allowed.find(x => x >= v);  // hExplicit: merged [H] atoms
  return ok === undefined ? 0 : ok - v;
}

// --- aromaticity ------------------------------------------------------------------------------------------------
// Pi electrons an atom gives to a ring (RDKit-style counting), or null if it cannot be part of an aromatic ring.
function piElectrons(mol, i, ringSet) {
  const a = mol.atoms[i];
  if (a.arom) return a.el === 'C' ? (a.charge < 0 ? 2 : a.charge > 0 ? 0 : 1) : null;
  let ringDouble = false, exoDouble = null, nDouble = 0;
  for (const [j, k] of mol.nbrs[i]) {
    const o = mol.bonds[k].order;
    if (o === 3) return null;
    if (o === 2) { nDouble++; if (ringSet.has(j)) ringDouble = true; else exoDouble = mol.atoms[j].el; }
  }
  if (nDouble > 1 && a.el === 'C') return null;
  if (ringDouble) return 1;
  if (exoDouble) return a.el === 'C' && ['O', 'N', 'S'].includes(exoDouble) ? 0 : null;
  const deg = mol.nbrs[i].length + a.hExplicit + a.hImplicit;
  if (a.el === 'C') return a.charge === -1 ? 2 : a.charge === 1 ? 0 : null;
  if (a.el === 'B') return a.charge === 0 && deg <= 3 ? 0 : null;
  if (['N', 'P'].includes(a.el)) return a.charge === 0 && deg <= 3 ? 2 : a.charge === -1 ? 2 : null;
  if (['O', 'S', 'Se', 'Te'].includes(a.el)) return a.charge === 0 && deg <= 2 ? 2 : a.charge === 1 && deg <= 3 ? 1 : null;
  return null;
}

// All simple cycles up to maxLen atoms (each once), as atom index arrays.
export function cycles(mol, maxLen = 16, cap = 20000) {
  const out = [], seen = new Set(), n = mol.atoms.length;
  const path = [], onPath = new Uint8Array(n);
  const dfs = (start, cur) => {
    if (out.length >= cap) return;
    for (const [j] of mol.nbrs[cur]) {
      if (j === start && path.length >= 3) {
        const key = [...path].sort((x, y) => x - y).join(',');
        if (!seen.has(key)) { seen.add(key); out.push([...path]); }
      } else if (j > start && !onPath[j] && path.length < maxLen) {
        onPath[j] = 1; path.push(j); dfs(start, j); path.pop(); onPath[j] = 0;
      }
    }
  };
  for (let s = 0; s < n; s++) { onPath[s] = 1; path.push(s); dfs(s, s); path.pop(); onPath[s] = 0; }
  return out;
}

function perceiveAromaticity(mol) {
  const ringAtoms = new Set();
  const all = cycles(mol);
  all.forEach(c => c.forEach(i => ringAtoms.add(i)));
  // Kekule input: a ring (or fused perimeter) is aromatic if every atom contributes and the count is 4n+2.
  const arom = new Set(), ringBonds = new Set();
  for (const c of all) {
    const set = new Set(c);
    let e = 0, ok = true;
    for (const i of c) { const p = piElectrons(mol, i, set); if (p === null) { ok = false; break; } e += p; }
    if (ok && e % 4 === 2) {
      c.forEach(i => arom.add(i));
      c.forEach((i, k) => ringBonds.add(bondKey(c[k], c[(k + 1) % c.length])));
    }
  }
  mol.bonds.forEach(b => {
    if (ringBonds.has(bondKey(b.a, b.b)) && arom.has(b.a) && arom.has(b.b)) b.order = 1.5;
  });
  mol.atoms.forEach((a, i) => { a.ring = ringAtoms.has(i); if (arom.has(i)) a.arom = true; });
  // Aromatic atoms not in an aromatic ring (bad lowercase input) are left as given.
}
const bondKey = (a, b) => (a < b ? `${a}-${b}` : `${b}-${a}`);

// --- formula and masses -----------------------------------------------------------------------------------------
export function elementCounts(mol) {
  const c = {};
  for (const a of mol.atoms) {
    if (a.el === '*') continue;
    c[a.el] = (c[a.el] || 0) + 1;
    if (a.hTotal) c.H = (c.H || 0) + a.hTotal;
  }
  return c;
}

export const totalCharge = mol => mol.atoms.reduce((s, a) => s + a.charge, 0);

// RDKit CalcMolFormula order: C, H, then alphabetical (H still first without carbon); charge suffix like '+', '-2'.
export function hillFormula(counts, charge = 0) {
  const els = Object.keys(counts).sort();
  const first = [...(counts.C ? ['C'] : []), ...(counts.H ? ['H'] : [])];
  const order = [...first, ...els.filter(e => !first.includes(e))];
  let f = order.map(e => e + (counts[e] > 1 ? counts[e] : '')).join('');
  if (charge) f += (charge > 0 ? '+' : '-') + (Math.abs(charge) > 1 ? Math.abs(charge) : '');
  return f;
}

export function masses(mol) {
  let avg = 0, mono = 0;
  for (const [el, n] of Object.entries(elementCounts(mol))) { avg += n * MASSES[el][0]; mono += n * MASSES[el][1]; }
  // Like RDKit ExactMolWt: an ion's mass is corrected for the electrons it gained or lost.
  return { mw: avg, exact: mono - totalCharge(mol) * ELECTRON_MASS };
}

// One call for the SMILES lab: everything the engine knows about a SMILES.
export function analyse(smi) {
  const mol = parseSmiles(smi);
  const counts = elementCounts(mol), charge = totalCharge(mol);
  return { mol, counts, charge, formula: hillFormula(counts, charge), ...masses(mol),
    heavy: mol.atoms.filter(a => a.el !== 'H' && a.el !== '*').length,
    fragments: String(smi).split('.').filter(Boolean).length,
    aromaticAtoms: mol.atoms.filter(a => a.arom).length };
}

// Compact atom signature in the fixture's format: "C0 Ca1 O1 ..." (element, a if aromatic, total H).
export const atomSignature = mol => mol.atoms.map(a => `${a.el}${a.arom ? 'a' : ''}${a.hTotal}`).join(' ');
