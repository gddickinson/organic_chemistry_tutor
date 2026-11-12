// Minimal SMARTS matcher, enough for the app's functional-group library (orgchem/core/molecule_tags.py
// FUNCTIONAL_GROUPS, copied below unchanged): atom primitives (element, aromatic/aliphatic, #n, X, H, D, charge, *),
// logic (! & , ;), recursive $(...), branches, ring closures and the - = # : bonds (unspecified = single or aromatic).
import { atomicNumber } from './chem_engine.js';

// Verbatim from orgchem/core/molecule_tags.py (order kept; chem_engine.test.mjs checks results against RDKit).
export const FUNCTIONAL_GROUPS = [
  ['carboxylic_acid', '[CX3](=O)[OX2H1]'], ['ester', '[CX3](=O)[OX2][#6]'], ['amide', '[CX3](=O)[NX3]'],
  ['acyl_halide', '[CX3](=O)[F,Cl,Br,I]'], ['anhydride', '[CX3](=O)[OX2][CX3](=O)'], ['nitrile', '[C]#[N]'],
  ['aldehyde', '[CX3H1](=O)[#6]'], ['ketone', '[#6][CX3](=O)[#6]'], ['ether', '[OD2]([#6])[#6]'],
  ['alcohol', '[OX2H][CX4;!$(C=[O,N,S])]'], ['phenol', '[OX2H][c]'], ['primary_amine', '[NX3;H2;!$(NC=O)]'],
  ['secondary_amine', '[NX3;H1;!$(NC=O)]'], ['tertiary_amine', '[NX3;H0;!$(NC=O);!$(N=*)]'],
  ['aromatic', 'c1ccccc1'], ['heterocycle_N', '[n]'], ['heterocycle_O', '[o]'], ['heterocycle_S', '[s]'],
  ['sulfonate', '[SX4](=O)(=O)[OX2H,OX1-]'], ['sulfonamide', '[SX4](=O)(=O)[NX3]'], ['thioether', '[SX2]([#6])[#6]'],
  ['thiol', '[SX2H]'], ['phosphate', '[P](=O)([OH])([OH])[OX2]'], ['nitro', '[NX3+](=O)[O-]'],
  ['alkene', '[CX3]=[CX3]'], ['alkyne', '[CX2]#[CX2]'], ['halide', '[F,Cl,Br,I]'],
];

const ELEMS = ['Cl', 'Br', 'Na', 'Si', 'Se', 'B', 'C', 'N', 'O', 'P', 'S', 'F', 'I', 'H'];

// --- parsing ----------------------------------------------------------------------------------------------------
export function parseSmarts(src) {
  const atoms = [], bonds = [], stack = [], rings = {};
  let prev = -1, pend = null, i = 0;
  const add = test => { const k = atoms.push(test) - 1; if (prev >= 0) bonds.push([prev, k, pend || 'default']); prev = k; pend = null; };
  while (i < src.length) {
    const ch = src[i];
    if (ch === '(') { stack.push(prev); i++; }
    else if (ch === ')') { prev = stack.pop(); i++; }
    else if ('-=#:~'.includes(ch)) { pend = ch; i++; }
    else if (/\d/.test(ch)) {
      if (rings[ch] !== undefined) { bonds.push([rings[ch].a, prev, pend || rings[ch].b || 'default']); delete rings[ch]; }
      else rings[ch] = { a: prev, b: pend };
      pend = null; i++;
    } else if (ch === '[') {
      let depth = 0, j = i;
      for (; j < src.length; j++) { if (src[j] === '[') depth++; else if (src[j] === ']' && --depth === 0) break; }
      add(parseAtomExpr(src.slice(i + 1, j))); i = j + 1;
    } else {
      const sym = ['Cl', 'Br'].find(e => src.startsWith(e, i)) || ch;
      add(primitive(sym)); i += sym.length;
    }
  }
  return { atoms, bonds };
}

// Atom expression with precedence: ! > & (and implicit) > , > ;
function parseAtomExpr(t) {
  let i = 0;
  const lowAnd = () => { const xs = [orExpr()]; while (t[i] === ';') { i++; xs.push(orExpr()); } return a => xs.every(f => f(a)); };
  const orExpr = () => { const xs = [highAnd()]; while (t[i] === ',') { i++; xs.push(highAnd()); } return a => xs.some(f => f(a)); };
  const highAnd = () => {
    const xs = [unary()];
    while (i < t.length && ![',', ';'].includes(t[i])) { if (t[i] === '&') i++; xs.push(unary()); }
    return a => xs.every(f => f(a));
  };
  const unary = () => { if (t[i] === '!') { i++; const f = unary(); return a => !f(a); } return prim(); };
  const num = def => { const m = /^\d+/.exec(t.slice(i)); if (!m) return def; i += m[0].length; return +m[0]; };
  const prim = () => {
    const ch = t[i];
    if (ch === '$') { // recursive SMARTS $( ... )
      let depth = 0, j = i + 1;
      for (; j < t.length; j++) { if (t[j] === '(') depth++; else if (t[j] === ')' && --depth === 0) break; }
      const sub = parseSmarts(t.slice(i + 2, j)); i = j + 1;
      return a => matchFrom(a.mol, sub, a.idx);
    }
    if (ch === '#') { i++; const z = num(0); return a => a.z === z; }
    if (ch === 'X') { i++; const n = num(1); return a => a.X === n; }
    if (ch === 'D') { i++; const n = num(1); return a => a.D === n; }
    if (ch === 'H') { i++; const n = num(1); return a => a.H === n; }
    if (ch === '+' || ch === '-') {
      let n = 0; const sign = ch === '+' ? 1 : -1;
      while (t[i] === ch) { n++; i++; }
      const d = num(null); const q = sign * (d ?? n);
      return a => a.charge === q;
    }
    if (ch === '*') { i++; return () => true; }
    if (ch === 'a') { i++; return a => a.arom; }
    if (ch === 'A') { i++; return a => !a.arom; }
    const sym = ELEMS.find(e => t.startsWith(e, i)) || (/[cnosp]/.test(ch) ? ch : null);
    if (!sym) throw new Error(`Unsupported SMARTS primitive in [${t}]`);
    i += sym.length;
    return primitive(sym);
  };
  return lowAnd();
}

function primitive(sym) {
  if (sym === '*') return () => true;
  const arom = /^[a-z]/.test(sym), z = atomicNumber(arom ? sym.toUpperCase() : sym);
  return a => a.z === z && a.arom === arom;
}

// --- matching ---------------------------------------------------------------------------------------------------
// Per-atom view used by the primitives (cached on the molecule).
function view(mol) {
  if (mol._view) return mol._view;
  mol._view = mol.atoms.map((at, idx) => ({
    mol, idx, z: atomicNumber(at.el), arom: !!at.arom, charge: at.charge, H: at.hTotal,
    D: mol.nbrs[idx].length, X: mol.nbrs[idx].length + at.hTotal,
  }));
  return mol._view;
}

function bondOk(kind, order) {
  if (kind === '~') return true;
  if (kind === 'default') return order === 1 || order === 1.5;
  return { '-': 1, '=': 2, '#': 3, ':': 1.5 }[kind] === order;
}

// Does pattern p match the molecule with pattern atom 0 on molecule atom `start`?
function matchFrom(mol, p, start) {
  const v = view(mol), map = new Array(p.atoms.length).fill(-1), used = new Set();
  // Visit pattern atoms in index order; each atom k > 0 has a parent bond to an earlier atom (tree bond).
  const parent = p.atoms.map(() => null), closures = [];
  for (const b of p.bonds) { if (parent[b[1]] === null && b[0] < b[1]) parent[b[1]] = b; else closures.push(b); }
  const bondOrder = (x, y) => { const e = mol.nbrs[x].find(([j]) => j === y); return e ? mol.bonds[e[1]].order : null; };
  const closuresOk = k => closures.every(([a, b, kind]) => {
    if (Math.max(a, b) !== k) return true;
    const o = bondOrder(map[a], map[b]);
    return o !== null && bondOk(kind, o);
  });
  const go = k => {
    if (k === p.atoms.length) return true;
    const cands = k === 0 ? [start] : mol.nbrs[map[parent[k][0]]].filter(([, bk]) => bondOk(parent[k][2], mol.bonds[bk].order)).map(([j]) => j);
    for (const c of cands) {
      if (used.has(c) || !p.atoms[k](v[c])) continue;
      map[k] = c; used.add(c);
      if (closuresOk(k) && go(k + 1)) return true;
      used.delete(c); map[k] = -1;
    }
    return false;
  };
  return go(0);
}

export function hasMatch(mol, smarts) {
  const p = typeof smarts === 'string' ? parseSmarts(smarts) : smarts;
  for (let s = 0; s < mol.atoms.length; s++) if (matchFrom(mol, p, s)) return true;
  return false;
}

const COMPILED = FUNCTIONAL_GROUPS.map(([name, s]) => [name, parseSmarts(s)]);
// Functional groups in the app's order, like auto_tag(mol).functional_groups.
export const functionalGroups = mol => COMPILED.filter(([, p]) => hasMatch(mol, p)).map(([name]) => name);
