// SMILES lab: formula, masses and functional groups computed in the browser (chem_engine.js + smarts.js, tested
// against RDKit), RDKit drawing in 2D/3D on the local server, and the empirical / molecular formula calculator.
import { route, api, app, esc, list, isStatic, needsServer, onLeave } from './core.js';
import { analyse } from './chem_engine.js';
import { functionalGroups } from './smarts.js';
import { computeFormula, ATOMIC_MASSES, ATOMIC_MASSES_INTEGER } from './formula_calc.js';
import { molSvg } from './draw2d.js';
import { viewer3d } from './viewer3d.js';

const EXAMPLES = [['Aspirin', 'CC(=O)Oc1ccccc1C(=O)O'], ['Caffeine', 'Cn1cnc2n(C)c(=O)n(C)c(=O)c12'],
  ['Glycine', 'NCC(=O)O'], ['Nitrobenzene (Kekule)', 'O=N(=O)C1=CC=CC=C1'], ['Acetate', 'CC(=O)[O-]'], ['Vanillin', 'COc1cc(C=O)ccc1O']];
// Inputs of tests/test_formula.py: Verma et al. 2024 Table 1 worked examples (percent by mass, molar mass).
const FORMULA_EXAMPLES = [
  ['Nicotine', { C: 74.00, H: 8.70, N: 17.27 }, 162.0], ['Caffeine', { C: 49.38, H: 5.16, N: 28.76, O: 16.70 }, 194.19],
  ['D-Glucose', { C: 40.00, H: 6.67, O: 53.33 }, 180.0], ['Cholesterol', { C: 83.87, H: 11.91, O: 4.14 }, 386.27],
  ['Porphyrin', { C: 77.33, H: 4.51, N: 18.04 }, 310.35], ['Codeine', { C: 72.00, H: 7.08, N: 4.69, O: 16.22 }, 299.30],
];
const pretty = g => g.replace(/_/g, ' ');

route('lab', async (_args, query) => {
  app().innerHTML = `<p class="kicker">Tools</p><h1>SMILES lab</h1>
  <p class="lead">Type a SMILES string. Formula, masses and the app's 27 functional-group patterns are computed right
  here in your browser by a small engine that agrees with RDKit on every SMILES the app seeds.</p>
  <div class="panel">
    <label for="s-in">SMILES</label><input id="s-in" spellcheck="false" autocomplete="off" value="${esc(query.smiles || EXAMPLES[0][1])}">
    <p class="small">${list(EXAMPLES, ([n, s]) => `<button class="alt" data-s="${esc(s)}">${esc(n)}</button>`)}</p>
    <div id="s-out" aria-live="polite"></div>
    <button id="s-draw">Draw in 2D and 3D (RDKit)</button><div id="s-rd"></div>
  </div>
  <h2>Empirical and molecular formula calculator</h2>
  <p>From percent composition by mass and the molar mass: atoms(X) = (%X / 100) × M / A(X), rounded; the empirical
  formula divides by the common factor. Port of the app's <code>orgchem/core/formula.py</code> (after Verma, Singh &amp;
  Passey 2024, <i>Rasayan J. Chem.</i> 17(4) 1460-1472).</p>
  <div class="panel">
    <div class="row"><div><label for="f-pct">Percent by mass (e.g. C 40.00, H 6.67, O 53.33)</label><input id="f-pct" value="C 40.00, H 6.67, O 53.33"></div>
    <div style="max-width:180px"><label for="f-mw">Molar mass (g/mol)</label><input id="f-mw" type="number" step="any" value="180.0"></div>
    <div style="max-width:220px"><label for="f-tab">Atomic masses</label><select id="f-tab"><option value="iupac">IUPAC 2019 (default)</option><option value="integer">Whole numbers (as the paper)</option></select></div></div>
    <p class="small">Worked examples from the paper: ${list(FORMULA_EXAMPLES, ([n], i) => `<button class="alt" data-f="${i}">${esc(n)}</button>`)}</p>
    <div id="f-out" aria-live="polite"></div>
  </div>`;
  const inp = document.getElementById('s-in');
  const run = () => {
    const out = document.getElementById('s-out');
    try {
      const r = analyse(inp.value), groups = functionalGroups(r.mol);
      out.innerHTML = `<div class="kv"><div><b>${esc(r.formula)}</b><span>molecular formula</span></div>
        <div><b>${r.mw.toFixed(3)}</b><span>average mass (g/mol)</span></div><div><b>${r.exact.toFixed(5)}</b><span>monoisotopic mass</span></div>
        <div><b>${r.heavy}</b><span>heavy atoms</span></div><div><b>${r.charge > 0 ? '+' : ''}${r.charge}</b><span>net charge</span></div>
        <div><b>${r.aromaticAtoms}</b><span>aromatic atoms</span></div></div>
        <p>Functional groups: ${groups.length ? list(groups, g => `<a class="tag a" href="#/molecules?group=${g}">${esc(pretty(g))}</a>`) : '<span class="mute">none of the 27 patterns</span>'}</p>`;
    } catch (e) {
      out.innerHTML = `<p class="err-pos">${esc(e.message)}</p>${e.pos != null ? `<pre>${esc(inp.value)}\n${' '.repeat(e.pos)}^</pre>` : ''}`;
    }
    document.getElementById('s-rd').innerHTML = '';
  };
  inp.addEventListener('input', run);
  document.querySelectorAll('[data-s]').forEach(b => b.addEventListener('click', () => { inp.value = b.dataset.s; run(); }));
  let viewer = null;
  onLeave(() => viewer && viewer.stop());
  document.getElementById('s-draw').addEventListener('click', async () => {
    const host = document.getElementById('s-rd');
    if (isStatic()) { host.innerHTML = needsServer('Drawing a new SMILES with RDKit'); return; }
    host.innerHTML = '<p class="mute">Drawing...</p>';
    try {
      const d = await api('/depict', { body: { smiles: inp.value } });
      if (viewer) viewer.stop();
      host.innerHTML = `<div class="two"><div class="molbox">${molSvg(d.d2, { bondPx: 36 }).svg}</div>
        <div>${d.d3 ? '<canvas class="view3d" id="lab3d" tabindex="0" aria-label="3D model: drag to rotate"></canvas>' : '<p class="mute">No 3D conformer could be embedded.</p>'}</div></div>
        <p class="small mute">RDKit canonical SMILES: <span class="mono">${esc(d.canonical)}</span> · logP ${d.descriptors.logp.toFixed(2)} · TPSA ${d.descriptors.tpsa.toFixed(1)}
        · Lipinski violations ${d.descriptors.lipinski_violations}</p>`;
      if (d.d3) viewer = viewer3d(document.getElementById('lab3d'), d.d3);
    } catch (e) { host.innerHTML = `<p class="err">${esc(e.message)}</p>`; }
  });
  run();

  const pct = document.getElementById('f-pct'), mw = document.getElementById('f-mw'), tab = document.getElementById('f-tab');
  const calc = () => {
    const out = document.getElementById('f-out');
    try {
      const p = {};
      for (const m of pct.value.matchAll(/([A-Z][a-z]?)\s*[:=]?\s*([0-9.]+)/g)) p[m[1]] = +m[2];
      if (!Object.keys(p).length) throw new Error('Enter element symbols with percentages, e.g. C 40, H 6.7, O 53.3');
      const r = computeFormula(p, +mw.value, { masses: tab.value === 'integer' ? ATOMIC_MASSES_INTEGER : ATOMIC_MASSES });
      const sum = Object.values(p).reduce((a, b) => a + b, 0);
      out.innerHTML = `<div class="kv"><div><b>${esc(r.empirical)}</b><span>empirical formula</span></div><div><b>${esc(r.molecular)}</b><span>molecular formula</span></div>
        <div><b>${r.scale}</b><span>molecular / empirical</span></div><div><b>${r.empiricalMass.toFixed(3)}</b><span>empirical mass</span></div>
        <div><b>${r.maxResidual.toFixed(3)}</b><span>largest rounding residual${r.worstElement ? ' (' + esc(r.worstElement) + ')' : ''}</span></div></div>
        ${Math.abs(sum - 100) > 1 ? `<p class="static-note">Percentages sum to ${sum.toFixed(2)}, not about 100.</p>` : ''}`;
    } catch (e) { out.innerHTML = `<p class="err">${esc(e.message)}</p>`; }
  };
  [pct, mw].forEach(el => el.addEventListener('input', calc)); tab.addEventListener('change', calc);
  document.querySelectorAll('[data-f]').forEach(b => b.addEventListener('click', () => {
    const [, p, m] = FORMULA_EXAMPLES[+b.dataset.f];
    pct.value = Object.entries(p).map(([e, v]) => `${e} ${v.toFixed(2)}`).join(', '); mw.value = m; calc();
  }));
  calc();
});
