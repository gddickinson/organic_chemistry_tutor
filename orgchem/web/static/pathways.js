// Synthesis pathways: list and step-by-step route (reagents above the arrow, conditions and yield below, notes).
import { route, api, app, esc, list } from './core.js';
import { schemeHtml, molSvg } from './draw2d.js';

route('pathways', async () => {
  const all = await api('/pathways');
  const cats = [...new Set(all.map(p => p.category || 'Other'))];
  app().innerHTML = `<p class="kicker">Synthesis</p><h1>Synthesis pathways</h1>
  <p class="lead">${all.length} multi-step teaching routes seeded by the app: pharmaceuticals, polymers, bio-organic and
  historic syntheses, each step with its reagents and conditions.</p>
  ${list(cats, c => `<h2>${esc(c)}</h2><div class="grid">${list(all.filter(p => (p.category || 'Other') === c), p => `<a class="card" href="#/pathway/${p.id}">
    <small>${p.n_steps} step${p.n_steps > 1 ? 's' : ''} · target: ${esc(p.target_name)}</small><b>${esc(p.name)}</b></a>`)}</div>`)}`;
});

route('pathway', async args => {
  const p = await api('/pathways/' + args[0]);
  app().innerHTML = `<p class="kicker"><a href="#/pathways">Synthesis pathways</a> · ${esc(p.category || '')}</p>
  <h1>${esc(p.name)}</h1>
  <div class="two"><div><p>${esc(p.description || '')}</p>${p.source ? `<p class="small mute">Source: ${esc(p.source)}</p>` : ''}</div>
  <div><h3>Target: ${esc(p.target_name)}</h3><div class="molbox">${p.target ? molSvg(p.target, { bondPx: 32, title: p.target_name }).svg : ''}</div></div></div>
  ${list(p.steps, (s, i) => `<h2>Step ${i + 1}</h2>
    ${schemeHtml(s.scheme, { above: s.reagents || '', below: [s.conditions, s.yield_pct != null ? s.yield_pct + '% yield' : ''].filter(Boolean).join(' · ') })}
    ${s.notes ? `<p>${esc(s.notes)}</p>` : ''}`)}`;
});
