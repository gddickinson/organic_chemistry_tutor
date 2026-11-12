// Home (hero, live counts, entry cards) and About.
import { route, api, app, esc, list, isStatic } from './core.js';
import { molSvg } from './draw2d.js';

const DOORS = [
  ['#/lessons', 'Lessons', 'The full curriculum from the desktop app: beginner to graduate, with glossary links.', 'lessons'],
  ['#/molecules', 'Molecules', 'Every seeded molecule with its 2D structure, 3D model, descriptors and functional groups.', 'molecules'],
  ['#/reactions', 'Named reactions', 'Reaction schemes with descriptions, atom economy and links to mechanisms.', 'reactions'],
  ['#/mechanisms', 'Mechanisms', 'Step through curly-arrow mechanisms, with lone pairs and bond-midpoint arrows.', 'mechanisms'],
  ['#/profiles', 'Energy profiles', 'Reaction-coordinate diagrams with activation energies and overall energy change.', 'energy_profiles'],
  ['#/pathways', 'Synthesis pathways', 'Multi-step routes to aspirin, paracetamol, ibuprofen and more, step by step.', 'pathways'],
  ['#/lab', 'SMILES lab', 'Type a SMILES: formula, masses and functional groups in your browser, plus the formula calculator.', null],
  ['#/quiz', 'Quiz', 'Name the structure, spot the functional group, pick the formula, the reaction or the term.', null],
  ['#/glossary', 'Glossary', 'Short definitions of the terms the lessons link to.', 'glossary'],
];

route('home', async () => {
  const [s, mols] = await Promise.all([api('/info'), api('/molecules/7').catch(() => null)]);
  app().innerHTML = `
  <section class="hero two">
    <div>
      <p class="kicker">Learn · Draw · React · Practise</p>
      <h1 class="glow">OrgChem Studio</h1>
      <p class="lead">An interactive tutor for learning and teaching organic chemistry. This site carries the
      desktop app's own lessons, molecule database, named reactions, curly-arrow mechanisms, energy profiles and
      synthesis routes, with quizzes built from them.</p>
      <a class="btn" href="#/lessons">Start the lessons</a><a class="btn alt" href="#/molecules">Browse molecules</a>
    </div>
    <a class="molbox" href="#/molecule/7" aria-label="Caffeine: open the molecule page">${mols ? molSvg(mols.d2, { bondPx: 40, title: 'Caffeine' }).svg : ''}</a>
  </section>
  <div class="tiles">
    <a class="tile" href="#/lessons"><b>${s.lessons}</b><span>lessons</span></a>
    <a class="tile" href="#/molecules"><b>${s.molecules}</b><span>molecules</span></a>
    <a class="tile" href="#/reactions"><b>${s.reactions}</b><span>reactions</span></a>
    <a class="tile" href="#/mechanisms"><b>${s.mechanisms}</b><span>mechanisms</span></a>
    <a class="tile" href="#/profiles"><b>${s.energy_profiles}</b><span>energy profiles</span></a>
    <a class="tile" href="#/pathways"><b>${s.pathways}</b><span>synthesis routes</span></a>
  </div>
  <div class="grid wide">${list(DOORS, ([href, t, d, k]) => `<a class="card door" href="${href}"><b>${t}${k ? ` <em class="n">${s[k]}</em>` : ''}</b><span>${d}</span></a>`)}</div>
  <h2>Curriculum</h2>
  <p class="mute">${list(Object.entries(s.lesson_levels), ([lv, n]) => `<a class="tag" href="#/lessons?level=${lv}"><span class="lvl-${lv}">${esc(lv)}</span> ${n}</a>`, ' ')}</p>`;
});

route('about', async () => {
  const s = await api('/info');
  app().innerHTML = `<p class="kicker">About</p><h1>About OrgChem Studio</h1>
  <p class="lead">OrgChem Studio is an interactive PySide6 desktop application for learning and teaching organic
  chemistry, built on RDKit, 3Dmol.js and SQLAlchemy/SQLite. This web interface shows its teaching content.</p>
  <h2>What is here</h2>
  <ul>
    <li><b>${s.lessons} lessons</b> from <code>orgchem/tutorial/content</code>, rendered with the same Markdown pipeline as the app's Tutorial panel.</li>
    <li><b>${s.molecules} molecules</b>, <b>${s.reactions} reactions</b> (${s.mechanisms} with mechanisms, ${s.energy_profiles} with energy profiles), <b>${s.pathways} synthesis pathways</b> and <b>${s.glossary} glossary terms</b>, all from the app's seed data (<code>orgchem/db/seed*.py</code>).</li>
    <li>Descriptors, functional-group tags, 2D layouts and 3D conformers computed by the app's own code (<code>orgchem/core</code>, RDKit). Structures are drawn in your browser (SVG and a small WebGL viewer).</li>
    <li>A JavaScript chemistry engine for the SMILES lab (formula, average and monoisotopic mass, the app's functional-group SMARTS), tested against RDKit on every SMILES the app seeds, and a port of the empirical-formula calculator (<code>orgchem/core/formula.py</code>, after Verma, Singh &amp; Passey 2024, <i>Rasayan J. Chem.</i> 17(4) 1460-1472).</li>
    <li>Quizzes generated from that content: ${list(Object.entries(s.quiz), ([k, n]) => `${n} ${esc(k)}`, ', ')} questions.</li>
  </ul>
  <p class="mute small">Energy profiles are the app's pedagogical estimates (textbook-shaped, not computed kinetics), as the app itself states.</p>
  <h2>Not on this site</h2>
  <p>The desktop app does much more: the six sibling life-science studios (cell biology, biochemistry, pharmacology,
  microbiology, botany, animal biology, genetics), protein and PDB tools, spectroscopy predictors, retrosynthesis,
  the drawing tool, lab calculators and the AI tutor. Run the app for those.</p>
  <h2>Run it yourself</h2>
  <p>Desktop app:</p><pre>pip install -r requirements.txt
python main.py</pre>
  <p>This web interface (local, http://127.0.0.1:8131), which can also draw any new SMILES in 2D and 3D with RDKit:</p>
  <pre>pip install -r requirements-web.txt
python run_web.py</pre>
  ${isStatic() ? '<p class="static-note">You are on the static site: everything works except drawing a brand-new SMILES (needs RDKit on the local server).</p>' : ''}
  <h2>Credits</h2>
  <p>OrgChem Studio by George Dickinson. Built on RDKit, SQLAlchemy and PySide6. Empirical-formula method after
  Verma, Singh &amp; Passey (2024). <a href="https://github.com/gddickinson/organic_chemistry_tutor">Source on GitHub</a>.</p>`;
});
