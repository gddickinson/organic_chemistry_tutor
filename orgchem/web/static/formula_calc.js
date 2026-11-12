// Empirical / molecular formula from mass percentages + molar mass: a line-by-line port of
// orgchem/core/formula.py compute_formula (after Verma, Singh & Passey 2024, Rasayan J. Chem. 17(4) 1460-1472).
// atoms(X) = (%X / 100) * molar_mass / atomic_mass(X), rounded; empirical = molecular / GCD.

// IUPAC 2019 standard atomic weights, as ATOMIC_MASSES in formula.py.
export const ATOMIC_MASSES = {
  H: 1.008, He: 4.003, Li: 6.94, Be: 9.012, B: 10.81, C: 12.011, N: 14.007, O: 15.999, F: 18.998, Ne: 20.180,
  Na: 22.990, Mg: 24.305, Al: 26.982, Si: 28.085, P: 30.974, S: 32.06, Cl: 35.45, Ar: 39.948, K: 39.098,
  Ca: 40.078, Fe: 55.845, Cu: 63.546, Zn: 65.38, Br: 79.904, I: 126.904,
};
// Whole-number masses of the paper (ATOMIC_MASSES_INTEGER in formula.py).
export const ATOMIC_MASSES_INTEGER = {
  H: 1, He: 4, Li: 7, Be: 9, B: 11, C: 12, N: 14, O: 16, F: 19, Ne: 20, Na: 23, Mg: 24, Al: 27, Si: 28, P: 31,
  S: 32, Cl: 35.5, Ar: 40, K: 39, Ca: 40, Fe: 56, Cu: 63.5, Zn: 65, Br: 79.9, I: 126.9,
};

const gcd = (a, b) => (b ? gcd(b, a % b) : a);
// Python's round(): halves go to the even neighbour.
function pyRound(x) {
  const f = Math.floor(x), d = x - f;
  if (d > 0.5) return f + 1;
  if (d < 0.5) return f;
  return f % 2 === 0 ? f : f + 1;
}

export function formatHill(counts) {
  const parts = [], rest = { ...counts };
  for (const el of ['C', 'H']) if (el in rest) { const n = rest[el]; delete rest[el]; parts.push(n === 1 ? el : el + n); }
  for (const el of Object.keys(rest).sort()) parts.push(rest[el] === 1 ? el : el + rest[el]);
  return parts.join('');
}

export function computeFormula(percentages, molarMass, { tol = 0.4, masses = ATOMIC_MASSES } = {}) {
  const els = Object.keys(percentages);
  if (!els.length) throw new Error('Need at least one element');
  const unknown = els.filter(e => !(e in masses));
  if (unknown.length) throw new Error(`Unknown element symbols: ${unknown.join(', ')}`);
  if (!(molarMass > 0)) throw new Error('molar_mass must be positive');
  if (els.some(e => percentages[e] < 0)) throw new Error('All percentages must be non-negative');
  const molecular = {};
  let worst = 0, worstEl = '';
  for (const el of els) {
    const pct = percentages[el];
    if (pct === 0) continue;
    const raw = (pct / 100) * molarMass / masses[el];
    let rounded = pyRound(raw);
    if (rounded < 1) { if (raw > 0.5) rounded = 1; else continue; }
    const residual = Math.abs(raw - rounded);
    if (residual > worst) { worst = residual; worstEl = el; }
    molecular[el] = rounded;
  }
  if (!Object.keys(molecular).length) throw new Error('No element yielded at least 1 atom: check percentages / molar mass');
  if (worst > tol) {
    throw new Error(`Element '${worstEl}' does not round to an integer atom count within ±${tol} (residual ${worst.toFixed(3)}). `
      + 'Check that the percentages sum to ~100 and the molar mass is correct.');
  }
  const g = Object.values(molecular).reduce(gcd);
  const empirical = Object.fromEntries(Object.entries(molecular).map(([e, n]) => [e, n / g]));
  const empiricalMass = Object.entries(empirical).reduce((s, [e, n]) => s + masses[e] * n, 0);
  return { empirical: formatHill(empirical), molecular: formatHill(molecular), empiricalMass, scale: g,
    empiricalCounts: empirical, molecularCounts: molecular, maxResidual: worst, worstElement: worstEl };
}
