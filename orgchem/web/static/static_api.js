// Static-site data layer: answers api(path) from the JSON files exported by scripts/build_static.py
// (api/<path>.json). Everything the pages read is exported; only POST /depict (RDKit drawing of a new SMILES) needs
// the Python server, and the SMILES lab shows needsServer() for it while still running the JS chemistry engine.
const files = new Map();
function file(rel) {
  if (!files.has(rel)) {
    files.set(rel, fetch('api/' + rel + '.json').then(r => { if (!r.ok) throw new Error(`${r.status} ${rel}`); return r.json(); }));
  }
  return files.get(rel);
}

export async function staticApi(path, body) {
  if (body) throw new Error('This needs the full app running locally (Python server with RDKit).');
  const clean = path.split('?')[0].replace(/^\/+|\/+$/g, '');
  return file(clean);
}
