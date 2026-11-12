// Entry point: registers the page modules (loaded on first visit), sets the mode line, draws the background, starts
// the router.
import { start, route, lazy, app, $, isStatic } from './core.js';
import { background } from './background.js';

const PAGES = {
  'home.js': ['home', 'about'], 'lessons.js': ['lessons', 'lesson'], 'molecules.js': ['molecules', 'molecule'],
  'reactions.js': ['reactions', 'reaction', 'mechanisms', 'profiles'], 'pathways.js': ['pathways', 'pathway'],
  'glossary.js': ['glossary'], 'lab.js': ['lab'], 'quiz.js': ['quiz'],
};
lazy(Object.fromEntries(Object.entries(PAGES).flatMap(([file, names]) => names.map(n => [n, () => import('./' + file)]))));

route('notfound', () => { app().innerHTML = '<h1>Not found</h1><p><a href="#/">Back to the start</a></p>'; });

$('#mode').textContent = isStatic() ? 'static site (drawing new SMILES in 2D/3D needs the local app)' : 'local app';
background($('#bg'));
start();
