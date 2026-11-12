// Minimal WebGL ball-and-stick viewer (no libraries). Input: the API's 3D molecule JSON (orgchem/web/depict.py
// coords_3d: RDKit ETKDG + MMFF conformer with explicit hydrogens). Drag to rotate, wheel / pinch to zoom.
import { color } from './draw2d.js';

// Covalent-ish display radii (A) for ball sizes; van der Waals radii for space-filling.
const RCOV = { H: 0.31, C: 0.76, N: 0.71, O: 0.66, F: 0.57, P: 1.07, S: 1.05, Cl: 1.02, Br: 1.2, I: 1.39, B: 0.84 };
const RVDW = { H: 1.2, C: 1.7, N: 1.55, O: 1.52, F: 1.47, P: 1.8, S: 1.8, Cl: 1.75, Br: 1.85, I: 1.98, B: 1.92 };

const VS = `attribute vec3 p; attribute vec3 n; uniform mat4 mv, pr; uniform mat3 nm;
varying vec3 vn; varying vec3 vp;
void main(){ vec4 q = mv * vec4(p,1.0); vp = q.xyz; vn = normalize(nm * n); gl_Position = pr * q; }`;
const FS = `precision mediump float; varying vec3 vn; varying vec3 vp; uniform vec3 col;
void main(){ vec3 L = normalize(vec3(0.4,0.6,1.0)); vec3 N = normalize(vn);
 float d = max(dot(N,L),0.0); vec3 V = normalize(-vp); float s = pow(max(dot(reflect(-L,N),V),0.0), 30.0);
 gl_FragColor = vec4(col*(0.28+0.72*d) + vec3(0.35)*s, 1.0); }`;

function sphere(seg = 16) {
  const p = [], idx = [];
  for (let i = 0; i <= seg; i++) for (let j = 0; j <= seg; j++) {
    const t = i / seg * Math.PI, ph = j / seg * 2 * Math.PI;
    p.push(Math.sin(t) * Math.cos(ph), Math.cos(t), Math.sin(t) * Math.sin(ph));
  }
  for (let i = 0; i < seg; i++) for (let j = 0; j < seg; j++) {
    const a = i * (seg + 1) + j, b = a + seg + 1;
    idx.push(a, b, a + 1, b, b + 1, a + 1);
  }
  return { p, n: p, idx };
}
function cylinder(seg = 14) { // unit cylinder along +z from 0 to 1, radius 1
  const p = [], n = [], idx = [];
  for (let j = 0; j <= seg; j++) {
    const a = j / seg * 2 * Math.PI, x = Math.cos(a), y = Math.sin(a);
    p.push(x, y, 0, x, y, 1); n.push(x, y, 0, x, y, 0);
  }
  for (let j = 0; j < seg; j++) { const a = 2 * j; idx.push(a, a + 1, a + 2, a + 1, a + 3, a + 2); }
  return { p, n, idx };
}

// --- tiny matrix helpers (column-major 4x4) ---
const ident = () => [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1];
function mul(a, b) {
  const o = new Array(16).fill(0);
  for (let c = 0; c < 4; c++) for (let r = 0; r < 4; r++) for (let k = 0; k < 4; k++) o[c * 4 + r] += a[k * 4 + r] * b[c * 4 + k];
  return o;
}
const rotX = t => [1, 0, 0, 0, 0, Math.cos(t), Math.sin(t), 0, 0, -Math.sin(t), Math.cos(t), 0, 0, 0, 0, 1];
const rotY = t => [Math.cos(t), 0, -Math.sin(t), 0, 0, 1, 0, 0, Math.sin(t), 0, Math.cos(t), 0, 0, 0, 0, 1];
const persp = (fov, asp, n, fr) => { const f = 1 / Math.tan(fov / 2); return [f / asp, 0, 0, 0, 0, f, 0, 0, 0, 0, (fr + n) / (n - fr), -1, 0, 0, 2 * fr * n / (n - fr), 0]; };
const hex = h => { const v = parseInt(h.slice(1), 16); return [(v >> 16 & 255) / 255, (v >> 8 & 255) / 255, (v & 255) / 255]; };

// Model matrix placing the unit cylinder between points a and b with radius r.
function cylMatrix(a, b, r) {
  const d = [b[0] - a[0], b[1] - a[1], b[2] - a[2]], L = Math.hypot(...d) || 1, z = d.map(v => v / L);
  const up = Math.abs(z[2]) < 0.9 ? [0, 0, 1] : [1, 0, 0];
  let x = [up[1] * z[2] - up[2] * z[1], up[2] * z[0] - up[0] * z[2], up[0] * z[1] - up[1] * z[0]];
  const xl = Math.hypot(...x); x = x.map(v => v / xl);
  const y = [z[1] * x[2] - z[2] * x[1], z[2] * x[0] - z[0] * x[2], z[0] * x[1] - z[1] * x[0]];
  return [x[0] * r, x[1] * r, x[2] * r, 0, y[0] * r, y[1] * r, y[2] * r, 0, z[0] * L, z[1] * L, z[2] * L, 0, a[0], a[1], a[2], 1];
}

export function viewer3d(canvas, mol, opts = {}) {
  const gl = canvas.getContext('webgl', { antialias: true });
  if (!gl || !mol || !mol.a) return null;
  const sh = (type, src) => { const s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s); return s; };
  const prog = gl.createProgram();
  gl.attachShader(prog, sh(gl.VERTEX_SHADER, VS)); gl.attachShader(prog, sh(gl.FRAGMENT_SHADER, FS)); gl.linkProgram(prog);
  gl.useProgram(prog);
  const loc = n => gl.getUniformLocation(prog, n), aP = gl.getAttribLocation(prog, 'p'), aN = gl.getAttribLocation(prog, 'n');
  const mesh = m => {
    const pb = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, pb); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(m.p), gl.STATIC_DRAW);
    const nb = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, nb); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(m.n), gl.STATIC_DRAW);
    const ib = gl.createBuffer(); gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, ib); gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint16Array(m.idx), gl.STATIC_DRAW);
    return { pb, nb, ib, count: m.idx.length };
  };
  const SPH = mesh(sphere()), CYL = mesh(cylinder());
  const bind = m => {
    gl.bindBuffer(gl.ARRAY_BUFFER, m.pb); gl.enableVertexAttribArray(aP); gl.vertexAttribPointer(aP, 3, gl.FLOAT, false, 0, 0);
    gl.bindBuffer(gl.ARRAY_BUFFER, m.nb); gl.enableVertexAttribArray(aN); gl.vertexAttribPointer(aN, 3, gl.FLOAT, false, 0, 0);
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, m.ib);
  };
  // Centre the molecule
  const P = mol.a.map(a => [a[1], a[2], a[3]]);
  const c = [0, 1, 2].map(k => P.reduce((s, p) => s + p[k], 0) / P.length);
  P.forEach(p => { p[0] -= c[0]; p[1] -= c[1]; p[2] -= c[2]; });
  const radius = Math.max(2, ...P.map(p => Math.hypot(...p)));
  const state = { rx: 0.35, ry: 0.5, dist: radius * 2.4 + 2.5, style: opts.style || 'ball', showH: true, spin: !matchMedia('(prefers-reduced-motion: reduce)').matches };
  const cols = mol.a.map(a => hex(color(a[0])));

  function draw() {
    const w = canvas.clientWidth, h = canvas.clientHeight, dpr = Math.min(devicePixelRatio || 1, 2);
    if (canvas.width !== Math.round(w * dpr) || canvas.height !== Math.round(h * dpr)) { canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr); }
    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.clearColor(0.03, 0.04, 0.07, 1); gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT); gl.enable(gl.DEPTH_TEST);
    gl.uniformMatrix4fv(loc('pr'), false, persp(0.7, w / Math.max(h, 1), 0.5, 500));
    const view = mul([1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, -state.dist, 1], mul(rotX(state.rx), rotY(state.ry)));
    const drawWith = (m, model) => {
      const mv = mul(view, model);
      // normal matrix: upper 3x3 of the rotation part (model scale is uniform for spheres; cylinders use direction)
      const r = mul(rotX(state.rx), rotY(state.ry));
      gl.uniformMatrix4fv(loc('mv'), false, mv);
      gl.uniformMatrix3fv(loc('nm'), false, [r[0], r[1], r[2], r[4], r[5], r[6], r[8], r[9], r[10]]);
      gl.drawElements(gl.TRIANGLES, m.count, gl.UNSIGNED_SHORT, 0);
    };
    const hidden = i => !state.showH && mol.a[i][0] === 'H';
    bind(SPH);
    mol.a.forEach((a, i) => {
      if (hidden(i)) return;
      const el = a[0], r = state.style === 'space' ? (RVDW[el] || 1.8) : state.style === 'stick' ? 0.16 : 0.32 * (RCOV[el] || 1.1) + 0.12;
      gl.uniform3fv(loc('col'), cols[i]);
      drawWith(SPH, [r, 0, 0, 0, 0, r, 0, 0, 0, 0, r, 0, P[i][0], P[i][1], P[i][2], 1]);
    });
    if (state.style !== 'space') {
      bind(CYL);
      for (const [i, j] of mol.b) {
        if (hidden(i) || hidden(j)) continue;
        const mid = [0, 1, 2].map(k => (P[i][k] + P[j][k]) / 2);
        gl.uniform3fv(loc('col'), cols[i]); drawWith(CYL, cylMatrix(P[i], mid, 0.16));
        gl.uniform3fv(loc('col'), cols[j]); drawWith(CYL, cylMatrix(mid, P[j], 0.16));
      }
    }
  }
  // Interaction
  let drag = null, pinch = null, raf = 0, alive = true;
  canvas.addEventListener('pointerdown', e => { drag = [e.clientX, e.clientY]; state.spin = false; canvas.setPointerCapture(e.pointerId); });
  canvas.addEventListener('pointermove', e => {
    if (!drag || pinch) return;
    state.ry += (e.clientX - drag[0]) * 0.01; state.rx += (e.clientY - drag[1]) * 0.01; drag = [e.clientX, e.clientY]; draw();
  });
  canvas.addEventListener('pointerup', () => { drag = null; });
  canvas.addEventListener('wheel', e => { e.preventDefault(); state.dist = Math.min(300, Math.max(3, state.dist * (1 + Math.sign(e.deltaY) * 0.1))); draw(); }, { passive: false });
  canvas.addEventListener('touchmove', e => {
    if (e.touches.length !== 2) return;
    const d = Math.hypot(e.touches[0].clientX - e.touches[1].clientX, e.touches[0].clientY - e.touches[1].clientY);
    if (pinch) state.dist = Math.min(300, Math.max(3, state.dist * pinch / d));
    pinch = d; draw(); e.preventDefault();
  }, { passive: false });
  canvas.addEventListener('touchend', () => { pinch = null; });
  canvas.addEventListener('keydown', e => {
    const k = { ArrowLeft: [0, -0.15], ArrowRight: [0, 0.15], ArrowUp: [-0.15, 0], ArrowDown: [0.15, 0] }[e.key];
    if (k) { state.rx += k[0]; state.ry += k[1]; state.spin = false; draw(); e.preventDefault(); }
    if (e.key === '+' || e.key === '=') { state.dist *= 0.9; draw(); }
    if (e.key === '-') { state.dist *= 1.1; draw(); }
  });
  const loop = () => { if (!alive) return; if (state.spin && !document.hidden) { state.ry += 0.006; draw(); } raf = requestAnimationFrame(loop); };
  draw(); loop();
  return {
    set(k, v) { state[k] = v; draw(); },
    get: k => state[k],
    stop() { alive = false; cancelAnimationFrame(raf); },
  };
}
