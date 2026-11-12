// Lessons: the curriculum index (filter by level and text) and one lesson page with previous / next.
import { route, api, app, esc, list } from './core.js';

const LEVELS = ['beginner', 'intermediate', 'advanced', 'graduate'];

route('lessons', async (_args, query) => {
  const all = await api('/lessons');
  app().innerHTML = `<p class="kicker">Curriculum</p><h1>Lessons</h1>
  <p class="lead">${all.length} lessons from the OrgChem Studio tutorial, in the app's curriculum order. Glossary terms
  in the text link to their definitions.</p>
  <div class="panel filters">
    <div><label for="l-q">Search titles</label><input id="l-q" type="search" placeholder="e.g. aldol, NMR, stereo" value="${esc(query.q || '')}"></div>
    <div><label for="l-lv">Level</label><select id="l-lv"><option value="">All levels</option>${list(LEVELS, l => `<option ${query.level === l ? 'selected' : ''}>${l}</option>`)}</select></div>
    <div class="mute small" id="l-n" aria-live="polite"></div>
  </div>
  <div id="l-out"></div>`;
  const q = document.getElementById('l-q'), lv = document.getElementById('l-lv');
  const draw = () => {
    const words = q.value.toLowerCase().split(/\s+/).filter(Boolean);
    const rows = all.filter(l => (!lv.value || l.level === lv.value) && words.every(w => l.title.toLowerCase().includes(w)));
    document.getElementById('l-n').textContent = `${rows.length} lessons`;
    document.getElementById('l-out').innerHTML = LEVELS.filter(L => rows.some(r => r.level === L)).map(L => `
      <h2 class="lvl-${L}">${L[0].toUpperCase() + L.slice(1)}</h2>
      <div class="grid">${list(rows.filter(r => r.level === L), r => `<a class="card" href="#/lesson/${r.slug}">
        <small>${L} · lesson ${r.n} · ${Math.max(1, Math.round(r.words / 200))} min read</small><b>${esc(r.title)}</b></a>`)}</div>`).join('')
      || '<p class="mute">No lessons match.</p>';
  };
  q.addEventListener('input', draw); lv.addEventListener('change', draw);
  draw();
});

route('lesson', async args => {
  const slug = args.join('/');
  const l = await api('/lessons/' + slug);
  app().innerHTML = `<p class="kicker"><a href="#/lessons?level=${l.level}" class="lvl-${l.level}">${l.level}</a> · lesson ${l.n}</p>
  <article class="md panel">${l.html}</article>
  <p class="mute small">Source: <code>${esc(l.source)}</code></p>
  <nav class="pager" aria-label="Lesson navigation">
    ${l.prev ? `<a class="btn alt" href="#/lesson/${l.prev.slug}">← ${esc(l.prev.title)}</a>` : '<span></span>'}
    ${l.next ? `<a class="btn" href="#/lesson/${l.next.slug}">${esc(l.next.title)} →</a>` : ''}
  </nav>`;
});
