// Named reactions (list + page with scheme, mechanism player and energy profile), and the Mechanisms and Energy
// profiles index pages.
import { route, api, app, esc, list } from './core.js';
import { schemeHtml, mechanismSvg } from './draw2d.js';
import { energyChartSvg } from './energy_chart.js';

const card = r => `<a class="card" href="#/reaction/${r.id}"><small>${esc(r.category || '')}</small><b>${esc(r.name)}</b>
  <span>${r.mechanism_steps ? `<span class="tag a">mechanism · ${r.mechanism_steps} steps</span>` : ''}${r.has_profile ? '<span class="tag b">energy profile</span>' : ''}</span></a>`;

route('reactions', async (_args, query) => {
  const all = await api('/reactions');
  app().innerHTML = `<p class="kicker">Reactions</p><h1>Named reactions</h1>
  <p class="lead">${all.length} reactions seeded by the app, from SN1/SN2 to cross-couplings and asymmetric catalysis.
  ${all.filter(r => r.mechanism_steps).length} carry a step-by-step curly-arrow mechanism and ${all.filter(r => r.has_profile).length} an energy profile.</p>
  <div class="panel filters"><div><label for="r-q">Search</label><input id="r-q" type="search" value="${esc(query.q || '')}" placeholder="e.g. Diels, oxidation, Pd"></div>
  <div><label for="r-f">Show</label><select id="r-f"><option value="">All reactions</option><option value="m">With a mechanism</option><option value="p">With an energy profile</option></select></div>
  <div class="mute small" id="r-n" aria-live="polite"></div></div><div class="grid" id="r-out"></div>`;
  const q = document.getElementById('r-q'), fsel = document.getElementById('r-f');
  const draw = () => {
    const words = q.value.toLowerCase().split(/\s+/).filter(Boolean);
    const rows = all.filter(r => words.every(w => (r.name + ' ' + r.category).toLowerCase().includes(w))
      && (!fsel.value || (fsel.value === 'm' ? r.mechanism_steps : r.has_profile)));
    document.getElementById('r-n').textContent = `${rows.length} reactions`;
    document.getElementById('r-out').innerHTML = list(rows, card) || '<p class="mute">No reactions match.</p>';
  };
  q.addEventListener('input', draw); fsel.addEventListener('change', draw); draw();
});

route('mechanisms', async () => {
  const all = (await api('/reactions')).filter(r => r.mechanism_steps);
  app().innerHTML = `<p class="kicker">Arrow pushing</p><h1>Mechanisms</h1>
  <p class="lead">${all.length} multi-step mechanisms. Each step shows the structure with curly arrows (two-electron
  flow) or fishhook arrows (one electron), lone pairs where the app marks them, and the app's explanation.</p>
  <div class="callout a">New to curly arrows? Start with the lesson <a href="#/lesson/beginner/15_curly_arrows">Curly arrows: the mechanism alphabet</a>.</div>
  <div class="grid">${list(all, card)}</div>`;
});

route('profiles', async () => {
  const all = (await api('/reactions')).filter(r => r.has_profile);
  const details = await Promise.all(all.map(r => api('/reactions/' + r.id)));
  app().innerHTML = `<p class="kicker">Reaction coordinate</p><h1>Energy profiles</h1>
  <p class="lead">${all.length} reaction-coordinate diagrams. The numbers are the app's pedagogical estimates
  (textbook-shaped; the source of each is given), not computed kinetics.</p>
  <div class="scroll"><table><thead><tr><th>Reaction</th><th>Points</th><th>Ea (first TS)</th><th>Overall change</th><th>Source</th></tr></thead><tbody>
  ${list(details, r => { const p = r.energy_profile; return `<tr><td><a href="#/reaction/${r.id}">${esc(r.name)}</a></td><td>${p.points.length}</td>
    <td class="mono">${p.activation_energies.length ? +p.activation_energies[0].toFixed(1) + ' ' + esc(p.energy_unit) : ''}</td>
    <td class="mono">${p.delta_h != null ? +p.delta_h.toFixed(1) + ' ' + esc(p.energy_unit) : ''}</td><td class="small mute">${esc(p.source)}</td></tr>`; })}
  </tbody></table></div>`;
});

route('reaction', async args => {
  const [r, all] = await Promise.all([api('/reactions/' + args[0]), api('/reactions')]);
  const pos = all.findIndex(x => x.id === r.id), prev = all[pos - 1], next = all[pos + 1];
  const ae = r.atom_economy && !r.atom_economy.error ? r.atom_economy : null;
  const p = r.energy_profile, steps = r.mechanism ? r.mechanism.steps : [];
  app().innerHTML = `<p class="kicker"><a href="#/reactions">Reactions</a> · ${esc(r.category || '')}</p>
  <h1>${esc(r.name)}</h1>
  ${schemeHtml(r.scheme, { small: false })}
  <p>${esc(r.description || '')}</p>
  <p class="mono small mute">${esc(r.reaction_smiles)}</p>
  ${ae ? `<div class="kv"><div><b>${ae.atom_economy.toFixed(1)}%</b><span>atom economy (desired product: heaviest fragment)</span></div>
    <div><b>${ae.mw_product.toFixed(2)}</b><span>product mass (g/mol)</span></div><div><b>${ae.mw_reactants.toFixed(2)}</b><span>reactant mass (g/mol)</span></div></div>` : ''}
  ${steps.length ? `<h2>Mechanism</h2><div class="steps" role="tablist" aria-label="Mechanism steps">${list(steps, (s, i) => `<button class="alt" role="tab" data-i="${i}">${/^step\s*\d/i.test(s.title) ? '' : `${i + 1}. `}${esc(s.title)}</button>`)}</div>
    <div id="mech" aria-live="polite"></div>` : ''}
  ${p ? `<h2>Energy profile</h2>${energyChartSvg(p)}
    <p class="small mute">${esc(p.title)} · ${esc(p.source)}. Ea per transition state: ${p.activation_energies.map(e => +e.toFixed(1)).join(', ') || 'none'}
    ${esc(p.energy_unit)}${p.delta_h != null ? `; overall change ${+p.delta_h.toFixed(1)} ${esc(p.energy_unit)}` : ''}.</p>
    <div class="scroll"><table><thead><tr><th>Point</th><th>Energy</th><th>Note</th></tr></thead><tbody>${list(p.points, q => `<tr><td>${esc(q.label)}${q.is_ts ? ' <span class="tag b">TS</span>' : ''}</td><td class="mono">${q.energy}</td><td class="small">${esc(q.note || '')}</td></tr>`)}</tbody></table></div>` : ''}
  <nav class="pager" aria-label="Reaction navigation">${prev ? `<a class="btn alt" href="#/reaction/${prev.id}">← ${esc(prev.short)}</a>` : '<span></span>'}
    ${next ? `<a class="btn alt" href="#/reaction/${next.id}">${esc(next.short)} →</a>` : ''}</nav>`;
  if (steps.length) {
    const host = document.getElementById('mech'), btns = [...document.querySelectorAll('.steps button')];
    const show = i => {
      btns.forEach((b, k) => { b.classList.toggle('on', k === i); b.setAttribute('aria-selected', k === i); b.className = k === i ? '' : 'alt'; });
      const s = steps[i];
      host.innerHTML = `<div class="mechbox">${mechanismSvg(s)}</div>
        <p><span class="mute small">${i + 1} / ${steps.length}</span> <b>${esc(s.title)}</b><br>${esc(s.description)}</p>
        <p class="mono small mute">${esc(s.smiles)}</p>
        <button class="alt" id="m-prev" ${i ? '' : 'disabled'}>Previous step</button><button id="m-next" ${i < steps.length - 1 ? '' : 'disabled'}>Next step</button>`;
      document.getElementById('m-prev').onclick = () => show(i - 1);
      document.getElementById('m-next').onclick = () => show(i + 1);
    };
    btns.forEach((b, i) => b.addEventListener('click', () => show(i)));
    show(0);
  }
});
