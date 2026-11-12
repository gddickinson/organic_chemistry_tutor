// 2D structure drawing as SVG from the API's compact molecule JSON ({a: atoms, b: bonds}; see orgchem/web/depict.py),
// plus mechanism overlays (curly / fishhook arrows and lone-pair dots, same geometry as orgchem/render/draw_mechanism.py)
// and reaction schemes. Coordinates are RDKit's (y up); the drawing flips y.
import { esc } from './core.js';

export const COLORS = { C: '#d8dee9', H: '#c7ccd6', N: '#6ea8ff', O: '#ff6b6b', S: '#ffd166', P: '#ffa94d', F: '#7ee081',
  Cl: '#7ee081', Br: '#d08770', I: '#c792ea', B: '#f4a3a3', Si: '#e0c38c', Na: '#b38cff', K: '#b38cff', Li: '#b38cff',
  Mg: '#8cffb3', Zn: '#9aa9c2', Fe: '#ff9f6b', Cu: '#ff9f6b', Pd: '#9aa9c2', Pt: '#9aa9c2', Ag: '#d0d6e0' };
export const color = el => COLORS[el] || '#ff9de2';
const ARROW = '#ff4f9a';
let uid = 0;

const sub = n => (n > 1 ? `<tspan baseline-shift="sub" font-size="70%">${n}</tspan>` : '');
const chargeText = q => (q ? (Math.abs(q) > 1 ? Math.abs(q) : '') + (q > 0 ? '+' : '−') : '');

// Layout: returns screen points and a transform for a molecule scaled to bondPx per median bond.
export function layout(d, { bondPx = 34, pad = 22, maxW = 640, maxH = 420 } = {}) {
  const A = d.a, B = d.b;
  const lens = B.map(([i, j]) => Math.hypot(A[i][1] - A[j][1], A[i][2] - A[j][2])).filter(x => x > 1e-6).sort((x, y) => x - y);
  const med = lens.length ? lens[lens.length >> 1] : 1;
  let s = bondPx / med;
  const xs = A.map(a => a[1]), ys = A.map(a => a[2]);
  const x0 = Math.min(...xs), x1 = Math.max(...xs), y0 = Math.min(...ys), y1 = Math.max(...ys);
  s = Math.min(s, (maxW - 2 * pad) / Math.max(x1 - x0, 1e-6), (maxH - 2 * pad) / Math.max(y1 - y0, 1e-6));
  if (!isFinite(s) || s <= 0) s = bondPx;
  s = Math.min(s, bondPx * 1.4);
  const w = (x1 - x0) * s + 2 * pad, h = (y1 - y0) * s + 2 * pad;
  const pts = A.map(a => [pad + (a[1] - x0) * s, pad + (y1 - a[2]) * s]);
  return { pts, w: Math.max(w, 2 * pad), h: Math.max(h, 2 * pad), scale: s / (bondPx / med || 1) };
}

function showLabel(atom, deg) {
  const [el, , , q, , , iso, rad] = atom;
  return el !== 'C' || q || iso || rad || deg === 0;
}

// Draw a molecule; returns { svg, pts, w, h } (pts in SVG user units, for overlays).
export function molSvg(d, opts = {}) {
  if (!d || !d.a || !d.a.length) return { svg: '<p class="mute small">No structure</p>', pts: [], w: 0, h: 0 };
  const { pts, w, h } = layout(d, opts);
  const A = d.a, B = d.b, deg = A.map(() => 0), nbrs = A.map(() => []);
  B.forEach(([i, j]) => { deg[i]++; deg[j]++; nbrs[i].push(j); nbrs[j].push(i); });
  // Carbons get a label in tiny fragments (CH3Br, methanol) and where a mechanism arrow or lone pair points.
  const comp = components(A.length, nbrs), mark = new Set(opts.labelAtoms || []);
  const labelled = A.map((a, i) => showLabel(a, deg[i]) || comp.size[comp.of[i]] <= 2 || mark.has(i));
  const rings = ringCentres(A.length, B, nbrs, pts);
  const fs = opts.fontPx || 15, out = [];
  // Bonds
  for (const [i, j, order, stereo] of B) {
    let [x1, y1] = pts[i], [x2, y2] = pts[j];
    const L = Math.hypot(x2 - x1, y2 - y1) || 1, ux = (x2 - x1) / L, uy = (y2 - y1) / L;
    const cut = fs * 0.62;
    if (labelled[i]) { x1 += ux * cut; y1 += uy * cut; }
    if (labelled[j]) { x2 -= ux * cut; y2 -= uy * cut; }
    const nx = -uy, ny = ux, col = 'var(--bond, #d8dee9)';
    if (stereo === 1 || stereo === 6) {
      const wd = 4.2;
      if (stereo === 1) out.push(`<polygon points="${f(x1)},${f(y1)} ${f(x2 + nx * wd)},${f(y2 + ny * wd)} ${f(x2 - nx * wd)},${f(y2 - ny * wd)}" fill="${col}"/>`);
      else for (let k = 1; k <= 6; k++) {
        const t = k / 6.5, cx = x1 + (x2 - x1) * t, cy = y1 + (y2 - y1) * t, hw = wd * t;
        out.push(`<line x1="${f(cx + nx * hw)}" y1="${f(cy + ny * hw)}" x2="${f(cx - nx * hw)}" y2="${f(cy - ny * hw)}" stroke="${col}" stroke-width="1.4"/>`);
      }
      continue;
    }
    const line = (ax, ay, bx, by, extra = '') => out.push(`<line x1="${f(ax)}" y1="${f(ay)}" x2="${f(bx)}" y2="${f(by)}" stroke="${col}" stroke-width="1.9" stroke-linecap="round"${extra}/>`);
    if (order === 1) { line(x1, y1, x2, y2); continue; }
    if (order === 3) { const o = 4; line(x1, y1, x2, y2); line(x1 + nx * o, y1 + ny * o, x2 + nx * o, y2 + ny * o); line(x1 - nx * o, y1 - ny * o, x2 - nx * o, y2 - ny * o); continue; }
    // Double / aromatic: inner second line towards the ring centre, or centred pair for acyclic / terminal bonds
    const rc = rings.get(key(i, j));
    if (rc) {
      const side = Math.sign((rc[0] - (x1 + x2) / 2) * nx + (rc[1] - (y1 + y2) / 2) * ny) || 1, o = 5.5 * side, sh = 0.16;
      line(x1, y1, x2, y2);
      const ax = x1 + (x2 - x1) * sh + nx * o, ay = y1 + (y2 - y1) * sh + ny * o;
      const bx = x2 - (x2 - x1) * sh + nx * o, by = y2 - (y2 - y1) * sh + ny * o;
      line(ax, ay, bx, by, order === 4 ? ' stroke-dasharray="3 3"' : '');
    } else {
      const o = 2.8;
      line(x1 + nx * o, y1 + ny * o, x2 + nx * o, y2 + ny * o);
      line(x1 - nx * o, y1 - ny * o, x2 - nx * o, y2 - ny * o, order === 4 ? ' stroke-dasharray="3 3"' : '');
    }
  }
  // Atom labels
  A.forEach((a, i) => {
    if (!labelled[i]) return;
    const [el, , , q, nH, , iso, rad] = a, [x, y] = pts[i], c = color(el);
    // Hydrogens to the left when the neighbours sit to the right
    const right = nbrs[i].reduce((s, j) => s + (pts[j][0] - x), 0);
    const hs = nH ? 'H' + sub(nH) : '';
    const lab = (iso ? `<tspan baseline-shift="super" font-size="65%">${iso}</tspan>` : '')
      + (hs && right > 0.5 && nbrs[i].length ? hs + el : el + hs)
      + (q ? `<tspan baseline-shift="super" font-size="70%">${chargeText(q)}</tspan>` : '');
    out.push(`<text x="${f(x)}" y="${f(y)}" fill="${c}" font-size="${fs}" text-anchor="middle" dominant-baseline="central" class="al">${lab}</text>`);
    if (rad) for (let k = 0; k < rad; k++) out.push(`<circle cx="${f(x - 3 + k * 6)}" cy="${f(y - fs * 0.85)}" r="1.9" fill="${c}"/>`);
  });
  const id = opts.title ? `<title>${esc(opts.title)}</title>` : '';
  const cls = opts.cls || 'mol';
  return { pts, w, h, nbrs, body: out.join(''),
    svg: `<svg class="${cls}" viewBox="0 0 ${f(w)} ${f(h)}" width="${f(w)}" height="${f(h)}" role="img" aria-label="${esc(opts.title || 'structure')}">${id}${out.join('')}</svg>` };
}

function components(n, nbrs) {
  const of = new Array(n).fill(-1), size = [];
  for (let s = 0; s < n; s++) {
    if (of[s] >= 0) continue;
    const c = size.push(0) - 1, st = [s]; of[s] = c;
    while (st.length) { const u = st.pop(); size[c]++; for (const v of nbrs[u]) if (of[v] < 0) { of[v] = c; st.push(v); } }
  }
  return { of, size };
}

const key = (i, j) => (i < j ? i + '-' + j : j + '-' + i);
const f = v => (Math.round(v * 10) / 10).toString();

// Map bond -> centre of the smallest ring (<= 8 atoms) containing it.
function ringCentres(n, B, nbrs, pts) {
  const res = new Map();
  for (const [i, j] of B) {
    // BFS from j to i without using the i-j bond
    const prev = new Array(n).fill(-1), q = [j];
    prev[j] = j;
    let found = false;
    while (q.length && !found) {
      const u = q.shift();
      for (const v of nbrs[u]) {
        if ((u === j && v === i) || prev[v] !== -1) continue;
        prev[v] = u;
        if (v === i) { found = true; break; }
        q.push(v);
      }
    }
    if (!found) continue;
    const ring = [i];
    for (let u = i; u !== j; u = prev[u]) ring.push(prev[u]);
    if (ring.length > 8) continue;
    const cx = ring.reduce((s, k) => s + pts[k][0], 0) / ring.length, cy = ring.reduce((s, k) => s + pts[k][1], 0) / ring.length;
    res.set(key(i, j), [cx, cy]);
  }
  return res;
}

// Mechanism step: molecule + curved arrows + lone pairs (orgchem/core/mechanism.py data).
export function mechanismSvg(step, opts = {}) {
  const ends = (step.arrows || []).flatMap(a => [...(a.from_bond ? [] : [a.from_atom]), ...(a.to_bond ? [] : [a.to_atom])]);
  const m = molSvg(step.d2, { maxW: 560, maxH: 380, bondPx: 50, pad: 46, fontPx: 17,
    labelAtoms: [...ends, ...(step.lone_pairs || [])], ...opts });
  if (!m.pts.length) return m.svg;
  const id = 'mh' + (++uid), extra = [];
  const pt = (bond, atom) => {
    if (bond) { const [a, b] = bond; if (!m.pts[a] || !m.pts[b]) return null; return [(m.pts[a][0] + m.pts[b][0]) / 2, (m.pts[a][1] + m.pts[b][1]) / 2]; }
    return m.pts[atom] || null;
  };
  for (const ar of step.arrows || []) {
    const p1 = pt(ar.from_bond, ar.from_atom), p2 = pt(ar.to_bond, ar.to_atom);
    if (!p1 || !p2) continue;
    const dx = p2[0] - p1[0], dy = p2[1] - p1[1], bend = ar.bend ?? 0.35;
    const cx = (p1[0] + p2[0]) / 2 - dy * bend, cy = (p1[1] + p2[1]) / 2 + dx * bend;
    extra.push(`<path d="M${f(p1[0])},${f(p1[1])} Q${f(cx)},${f(cy)} ${f(p2[0])},${f(p2[1])}" stroke="${ARROW}" stroke-width="2.4" fill="none" stroke-linecap="round" marker-end="url(#${id}${ar.kind === 'fishhook' ? 'f' : 'c'})" class="arrow"/>`);
    if (ar.label) extra.push(`<text x="${f((p1[0] + p2[0]) / 2 - dy * bend * 1.35)}" y="${f((p1[1] + p2[1]) / 2 + dx * bend * 1.35)}" fill="${ARROW}" font-size="13" text-anchor="middle">${esc(ar.label)}</text>`);
  }
  for (const i of step.lone_pairs || []) {
    if (!m.pts[i]) continue;
    const [x, y] = m.pts[i];
    let vx = 0, vy = 0;
    for (const j of m.nbrs[i]) { vx += m.pts[j][0] - x; vy += m.pts[j][1] - y; }
    let nx = 0, ny = -1;
    if (m.nbrs[i].length && (vx || vy)) { const L = Math.hypot(vx, vy); nx = -vx / L; ny = -vy / L; }
    const px = x + nx * 15, py = y + ny * 15, tx = -ny * 2.9, ty = nx * 2.9;
    extra.push(`<circle cx="${f(px + tx)}" cy="${f(py + ty)}" r="2.2" fill="#ffe066"/><circle cx="${f(px - tx)}" cy="${f(py - ty)}" r="2.2" fill="#ffe066"/>`);
  }
  const defs = `<defs><marker id="${id}c" markerWidth="10" markerHeight="7" refX="8" refY="3.5" orient="auto" markerUnits="userSpaceOnUse"><polygon points="0 0, 10 3.5, 0 7" fill="${ARROW}"/></marker>`
    + `<marker id="${id}f" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto" markerUnits="userSpaceOnUse"><polyline points="0 0, 10 3.5" stroke="${ARROW}" stroke-width="1.6" fill="none"/></marker></defs>`;
  return `<svg class="mol mech" viewBox="0 0 ${f(m.w)} ${f(m.h)}" width="${f(m.w)}" height="${f(m.h)}" role="img" aria-label="${esc(step.title || 'mechanism step')}">${defs}${m.body}${extra.join('')}</svg>`;
}

// Reaction scheme: reactants + ... -> products, each fragment its own small drawing (wraps on narrow screens).
export function schemeHtml(sc, { above = '', below = '', small = true } = {}) {
  const o = small ? { bondPx: 24, maxW: 300, maxH: 220, pad: 14, fontPx: 13 } : { bondPx: 30, maxW: 380, maxH: 260 };
  const side = arr => arr.map(d => `<span class="frag">${molSvg(d, o).svg}</span>`).join('<span class="plus">+</span>');
  const mid = [above, ...(sc.agents || []).length ? [] : []].filter(Boolean).join(' ');
  const agents = (sc.agents || []).length ? `<span class="agents">${(sc.agents || []).map(d => molSvg(d, { ...o, bondPx: 18 }).svg).join(' ')}</span>` : '';
  return `<div class="scheme">${side(sc.reactants || [])}<span class="rarrow">${agents}${mid ? `<em>${esc(mid)}</em>` : ''}<b>⟶</b>${below ? `<em>${esc(below)}</em>` : ''}</span>${side(sc.products || [])}</div>`;
}
