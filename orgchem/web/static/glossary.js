// Glossary: every term with its definition (light Markdown), aliases and see-also links. #/glossary/<term> focuses one.
import { route, api, app, esc, list } from './core.js';

// Minimal inline Markdown for definitions: **bold**, *italic*, `code`; everything else escaped.
export const inlineMd = s => esc(s).replace(/\*\*(.+?)\*\*/g, '<b>$1</b>').replace(/\*(.+?)\*/g, '<i>$1</i>').replace(/`(.+?)`/g, '<code>$1</code>');
const id = t => 'g-' + t.toLowerCase().replace(/[^a-z0-9]+/g, '-');

route('glossary', async (args, query) => {
  const all = await api('/glossary');
  const want = (args[0] || '').toLowerCase();
  const hit = want && all.find(g => g.term.toLowerCase() === want || g.aliases.some(a => a.toLowerCase() === want));
  const cats = [...new Set(all.map(g => g.category || 'other'))].sort();
  app().innerHTML = `<p class="kicker">Reference</p><h1>Glossary</h1>
  <p class="lead">${all.length} terms from the app's glossary. Lessons link here.</p>
  ${want && !hit ? `<p class="callout">"${esc(args[0])}" is linked from a lesson but has no glossary entry yet.</p>` : ''}
  <div class="panel filters"><div><label for="g-q">Search terms and definitions</label><input id="g-q" type="search" value="${esc(query.q || '')}"></div>
  <div><label for="g-c">Category</label><select id="g-c"><option value="">All</option>${list(cats, c => `<option>${esc(c)}</option>`)}</select></div>
  <div class="mute small" id="g-n" aria-live="polite"></div></div>
  <div class="grid wide" id="g-out"></div>`;
  const q = document.getElementById('g-q'), c = document.getElementById('g-c');
  const draw = () => {
    const words = q.value.toLowerCase().split(/\s+/).filter(Boolean);
    const rows = all.filter(g => (!c.value || g.category === c.value)
      && words.every(w => [g.term, ...g.aliases, g.definition_md].join(' ').toLowerCase().includes(w)));
    document.getElementById('g-n').textContent = `${rows.length} terms`;
    document.getElementById('g-out').innerHTML = list(rows, g => `<div class="card gl-term${hit === g ? ' on' : ''}" id="${id(g.term)}">
      <small>${esc(g.category || '')}${g.aliases.length ? ' · also ' + esc(g.aliases.join(', ')) : ''}</small><b>${esc(g.term)}</b>
      <span>${inlineMd(g.definition_md)}</span>
      ${g.example_smiles ? `<span class="mono small mute">e.g. ${esc(g.example_smiles)}</span>` : ''}
      ${g.see_also.length ? `<span class="small">See also: ${list(g.see_also, t => `<a href="#/glossary/${encodeURIComponent(t)}">${esc(t)}</a>`, ', ')}</span>` : ''}</div>`);
  };
  q.addEventListener('input', draw); c.addEventListener('change', draw); draw();
  // After the router's own scroll-to-top
  if (hit) setTimeout(() => document.getElementById(id(hit.term))?.scrollIntoView({ block: 'center' }), 0);
});
