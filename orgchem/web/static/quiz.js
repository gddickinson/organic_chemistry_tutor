// Quiz: rounds of 10 questions drawn from the bank the API builds out of the app's own content (orgchem/web/quiz.py).
import { route, api, app, esc, list, rng } from './core.js';
import { molSvg, schemeHtml } from './draw2d.js';
import { inlineMd } from './glossary.js';

const KINDS = { all: 'Mixed', name: 'Name the structure', group: 'Functional groups', formula: 'Molecular formulas',
  reaction: 'Named reactions', glossary: 'Glossary terms' };
const ROUND = 10;

route('quiz', async (_args, query) => {
  const bank = await api('/quiz');
  let kind = KINDS[query.kind] ? query.kind : 'all', qs = [], at = 0, score = 0, answered = false;
  const rand = rng(Date.now() % 1e9);
  app().innerHTML = `<p class="kicker">Practise</p><h1>Quiz</h1>
  <p class="lead">Questions generated from the app's own molecules, functional-group patterns, reactions and glossary.
  Every answer is checked against that data.</p>
  <div class="seg" role="group" aria-label="Question type">${list(Object.entries(KINDS), ([k, t]) => `<button data-k="${k}">${esc(t)}</button>`)}</div>
  <div class="panel quiz" id="qz" aria-live="polite"></div>`;
  const host = document.getElementById('qz');
  const newRound = () => {
    const pool = bank.questions.filter(q => kind === 'all' || q.kind === kind);
    const a = [...pool];
    for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(rand() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; }
    qs = a.slice(0, ROUND); at = 0; score = 0;
    document.querySelectorAll('[data-k]').forEach(b => b.classList.toggle('on', b.dataset.k === kind));
    show();
  };
  const show = () => {
    if (at >= qs.length) {
      host.innerHTML = `<h2>Score: ${score} / ${qs.length}</h2><p>${score === qs.length ? 'Perfect round.' : 'Each answer links to its source page if you want to review it.'}</p>
        <button id="qz-again">Another round</button>`;
      document.getElementById('qz-again').onclick = newRound; return;
    }
    const q = qs[at]; answered = false;
    host.innerHTML = `<p class="small mute">Question ${at + 1} of ${qs.length} · ${esc(KINDS[q.kind])} · score ${score}</p>
      <p class="def"><b>${esc(q.prompt)}</b></p>
      ${q.mol ? `<div class="molbox">${molSvg(q.mol, { bondPx: 34, maxW: 460, maxH: 300 }).svg}</div>` : ''}
      ${q.scheme ? schemeHtml(q.scheme) : ''}
      ${q.text ? `<p class="def">${inlineMd(q.text)}</p>` : ''}
      <div class="opts">${list(q.options, (o, i) => `<button data-o="${i}">${esc(o)}</button>`)}</div>
      <div id="qz-fb"></div>`;
    host.querySelectorAll('[data-o]').forEach(b => b.addEventListener('click', () => pick(b)));
  };
  const pick = b => {
    if (answered) return;
    answered = true;
    const q = qs[at], ok = q.options[+b.dataset.o] === q.answer;
    if (ok) score++;
    host.querySelectorAll('[data-o]').forEach(x => {
      const o = q.options[+x.dataset.o];
      if (o === q.answer) x.classList.add('right'); else if (x === b) x.classList.add('wrong');
      x.setAttribute('aria-disabled', 'true');
    });
    document.getElementById('qz-fb').innerHTML = `<p class="${ok ? 'ok' : 'err'}"><b>${ok ? 'Correct.' : 'Not quite: ' + esc(q.answer) + '.'}</b>
      ${esc(q.explain || '')} <a href="${q.link}">Open</a></p><button id="qz-next">${at + 1 < qs.length ? 'Next question' : 'See score'}</button>`;
    const nx = document.getElementById('qz-next');
    nx.onclick = () => { at++; show(); }; nx.focus();
  };
  document.querySelectorAll('[data-k]').forEach(b => b.addEventListener('click', () => { kind = b.dataset.k; newRound(); }));
  newRound();
});
