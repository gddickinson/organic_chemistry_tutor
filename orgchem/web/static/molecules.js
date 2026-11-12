// Molecule browser (search, source group, functional-group filter) and the molecule page (2D, 3D, descriptors).
import { route, api, app, esc, list, onLeave } from './core.js';
import { molSvg } from './draw2d.js';
import { viewer3d } from './viewer3d.js';

const GROUP_LABEL = g => g.replace(/_/g, ' ');
const PAGE = 60;

route('molecules', async (_args, query) => {
  const all = await api('/molecules');
  const sources = [...new Set(all.map(m => m.source))].sort();
  const groups = [...new Set(all.flatMap(m => m.tags))].filter(t => t !== 'pure_organic').sort();
  app().innerHTML = `<p class="kicker">Database</p><h1>Molecules</h1>
  <p class="lead">${all.length} molecules seeded by the app: basics, the Verma et al. 2024 reference set, amino acids,
  drugs, reagents, natural products, reactive intermediates and more. Open one for its 2D structure, 3D model and descriptors.</p>
  <div class="panel filters">
    <div><label for="m-q">Name, synonym, formula or SMILES</label><input id="m-q" type="search" value="${esc(query.q || '')}" placeholder="e.g. caffeine, C9H8O4, indole"></div>
    <div><label for="m-s">Group</label><select id="m-s"><option value="">All groups</option>${list(sources, s => `<option ${query.source === s ? 'selected' : ''}>${esc(s)}</option>`)}</select></div>
    <div><label for="m-g">Functional group</label><select id="m-g"><option value="">Any</option>${list(groups, g => `<option value="${g}" ${query.group === g ? 'selected' : ''}>${esc(GROUP_LABEL(g))}</option>`)}</select></div>
  </div>
  <p class="mute small" id="m-n" aria-live="polite"></p>
  <div class="scroll"><table><thead><tr><th>Name</th><th>Formula</th><th>MW</th><th>Group</th><th>Functional groups</th></tr></thead><tbody id="m-out"></tbody></table></div>
  <button class="alt" id="m-more" hidden>Show more</button>`;
  const q = document.getElementById('m-q'), s = document.getElementById('m-s'), g = document.getElementById('m-g');
  let shown = PAGE;
  const draw = () => {
    const words = q.value.toLowerCase().split(/\s+/).filter(Boolean);
    const rows = all.filter(m => (!s.value || m.source === s.value) && (!g.value || m.tags.includes(g.value))
      && words.every(w => [m.name, m.formula, m.smiles, ...m.synonyms].join(' ').toLowerCase().includes(w)));
    document.getElementById('m-n').textContent = `${rows.length} of ${all.length} molecules`;
    document.getElementById('m-out').innerHTML = list(rows.slice(0, shown), m => `<tr>
      <td><a href="#/molecule/${m.id}">${esc(m.name)}</a></td><td class="mono">${esc(m.formula)}</td>
      <td class="mono">${m.mw != null ? m.mw.toFixed(2) : ''}</td><td class="small mute">${esc(m.source)}</td>
      <td class="small">${esc(m.tags.filter(t => t !== 'pure_organic').map(GROUP_LABEL).join(', '))}</td></tr>`);
    const more = document.getElementById('m-more');
    more.hidden = rows.length <= shown;
    more.textContent = `Show more (${rows.length - shown} left)`;
  };
  const reset = () => { shown = PAGE; draw(); };
  q.addEventListener('input', reset); s.addEventListener('change', reset); g.addEventListener('change', reset);
  document.getElementById('m-more').addEventListener('click', () => { shown += PAGE * 2; draw(); });
  draw();
});

const fmt = (v, d = 2) => (typeof v === 'number' ? (Number.isInteger(v) ? String(v) : v.toFixed(d)) : esc(v ?? ''));

route('molecule', async args => {
  const m = await api('/molecules/' + args[0]);
  const d = m.descriptors, t = m.auto_tags;
  app().innerHTML = `<p class="kicker"><a href="#/molecules?source=${encodeURIComponent(m.source)}">${esc(m.source_label)}</a></p>
  <h1>${esc(m.name)}</h1>
  ${m.synonyms.length ? `<p class="mute">Also: ${esc(m.synonyms.slice(0, 6).join(' · '))}</p>` : ''}
  <div class="two">
    <div><h3>2D structure</h3><div class="molbox">${molSvg(m.d2, { bondPx: 38, maxW: 520, title: m.name }).svg}</div></div>
    <div><h3>3D model</h3>${m.d3 ? `<canvas class="view3d" id="v3" tabindex="0" aria-label="3D model of ${esc(m.name)}: drag or use arrow keys to rotate, wheel or +/- to zoom"></canvas>
      <div class="seg" role="group" aria-label="3D style"><button data-st="ball" class="on">Ball and stick</button><button data-st="stick">Sticks</button><button data-st="space">Space-filling</button></div>
      <label style="display:inline-flex;gap:6px;margin-left:10px"><input type="checkbox" id="v3h" checked> hydrogens</label>`
      : '<p class="mute">No 3D conformer: RDKit could not embed this structure with the app\'s settings (ETKDG, fixed seed).</p>'}</div>
  </div>
  <div class="kv">
    <div><b>${esc(d.formula)}</b><span>formula</span></div><div><b>${fmt(d.mol_weight)}</b><span>mol. weight (g/mol)</span></div>
    <div><b>${fmt(d.exact_mass, 4)}</b><span>monoisotopic mass</span></div><div><b>${fmt(d.logp)}</b><span>logP (Crippen)</span></div>
    <div><b>${fmt(d.tpsa)}</b><span>TPSA (A²)</span></div><div><b>${d.h_bond_donors} / ${d.h_bond_acceptors}</b><span>H-bond donors / acceptors</span></div>
    <div><b>${d.rotatable_bonds}</b><span>rotatable bonds</span></div><div><b>${d.aromatic_rings} / ${d.rings_total}</b><span>aromatic / all rings</span></div>
    <div><b>${d.heavy_atom_count}</b><span>heavy atoms</span></div><div><b>${d.lipinski_violations}</b><span>Lipinski violations</span></div>
  </div>
  <h3>Functional groups and tags</h3>
  <p>${t.functional_groups.length ? list(t.functional_groups, g => `<a class="tag a" href="#/molecules?group=${g}">${esc(GROUP_LABEL(g))}</a>`) : '<span class="mute">none of the app\'s 27 SMARTS groups</span>'}
  ${list(t.composition_flags, f => `<span class="tag">${esc(GROUP_LABEL(f))}</span>`)}
  <span class="tag c">${esc(t.charge_category)}</span><span class="tag c">${esc(t.size_band)}</span>${t.has_stereo ? '<span class="tag b">stereocentres</span>' : ''}</p>
  <h3>Identifiers</h3>
  <div class="scroll"><table><tr><th>SMILES</th><td class="mono">${esc(m.smiles)}</td></tr>
  <tr><th>InChIKey</th><td class="mono">${esc(m.inchikey || '')}</td></tr></table></div>
  <p><a class="btn alt" href="#/lab?smiles=${encodeURIComponent(m.smiles)}">Open in the SMILES lab</a></p>`;
  if (m.d3) {
    const v = viewer3d(document.getElementById('v3'), m.d3);
    if (!v) { document.getElementById('v3').outerHTML = '<p class="mute">WebGL is not available in this browser.</p>'; return; }
    onLeave(() => v.stop());
    document.querySelectorAll('[data-st]').forEach(b => b.addEventListener('click', () => {
      document.querySelectorAll('[data-st]').forEach(x => x.classList.toggle('on', x === b)); v.set('style', b.dataset.st);
    }));
    document.getElementById('v3h').addEventListener('change', e => v.set('showH', e.target.checked));
  }
});
