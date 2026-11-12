// Reaction-coordinate diagram as SVG from an energy profile (orgchem/core/energy_profile.py data): stationary points
// in order along x, a smooth curve through them (flat-topped at every point, like the desktop renderer's Bezier
// curve), transition states marked with a double dagger, and the Ea of each TS plus the overall energy change.
import { esc } from './core.js';

export function energyChartSvg(p, { w = 760, h = 360 } = {}) {
  const pts = p.points || [];
  if (pts.length < 2) return '';
  const L = 58, R = 20, T = 44, B = 50, iw = w - L - R, ih = h - T - B;
  const es = pts.map(q => q.energy), lo = Math.min(...es), hi = Math.max(...es), span = hi - lo || 1;
  const y = e => T + ih - (e - lo + span * 0.08) / (span * 1.22) * ih;
  const x = i => L + (i + 0.5) * iw / pts.length;
  const hw = iw / pts.length * 0.18; // half width of the flat plateau at each point
  let d = `M${x(0) - hw},${y(es[0])} L${x(0) + hw},${y(es[0])}`;
  for (let i = 1; i < pts.length; i++) {
    const x0 = x(i - 1) + hw, x1 = x(i) - hw, mx = (x0 + x1) / 2;
    d += ` C${mx},${y(es[i - 1])} ${mx},${y(es[i])} ${x1},${y(es[i])} L${x(i) + hw},${y(es[i])}`;
  }
  const unit = esc(p.energy_unit || 'kJ/mol');
  const ticks = niceTicks(lo, hi, 5);
  const parts = [`<line x1="${L}" y1="${T}" x2="${L}" y2="${T + ih}" stroke="#3a4670"/>`,
    `<line x1="${L}" y1="${T + ih}" x2="${L + iw}" y2="${T + ih}" stroke="#3a4670"/>`,
    ...ticks.map(t => `<line x1="${L - 4}" x2="${L + iw}" y1="${y(t)}" y2="${y(t)}" stroke="#1a2240"/><text x="${L - 8}" y="${y(t) + 4}" text-anchor="end">${t}</text>`),
    `<text x="14" y="${T + ih / 2}" transform="rotate(-90 14 ${T + ih / 2})" text-anchor="middle">energy (${unit})</text>`,
    `<text x="${L + iw / 2}" y="${h - 8}" text-anchor="middle">reaction coordinate</text>`,
    `<path d="${d}" fill="none" stroke="var(--accent)" stroke-width="2.6"/>`];
  pts.forEach((q, i) => {
    parts.push(`<circle cx="${x(i)}" cy="${y(q.energy)}" r="4.5" class="${q.is_ts ? 'ts' : 'mn'}"><title>${esc(q.label)}: ${q.energy} ${unit}${q.note ? ' - ' + esc(q.note) : ''}</title></circle>`);
    // Transition states labelled above the peak, minima below the well; energy value under the label.
    const yy = y(q.energy) + (q.is_ts ? -26 : 22);
    parts.push(`<text class="lbl" x="${x(i)}" y="${yy}" text-anchor="middle">${esc(q.label)}${q.is_ts && !q.label.includes('‡') ? '‡' : ''}</text>`,
      `<text x="${x(i)}" y="${yy + 14}" text-anchor="middle">${q.energy}</text>`);
  });
  // Ea arrows: TS minus the preceding minimum (same rule as ReactionEnergyProfile.activation_energies)
  let lastMin = null, k = 0;
  pts.forEach((q, i) => {
    if (!q.is_ts) { lastMin = i; return; }
    if (lastMin === null) return;
    const ea = (p.activation_energies || [])[k++];
    // Dashed Ea bar at the TS, from the preceding minimum's level up to the peak, value beside it.
    const xx = x(i);
    parts.push(`<line x1="${xx - hw}" x2="${xx + hw}" y1="${y(es[lastMin])}" y2="${y(es[lastMin])}" stroke="var(--accent2)" stroke-dasharray="2 3"/>`,
      `<line x1="${xx}" x2="${xx}" y1="${y(es[lastMin])}" y2="${y(q.energy) + 6}" stroke="var(--accent2)" stroke-dasharray="3 3"/>`,
      `<text x="${xx + 5}" y="${(y(es[lastMin]) + y(q.energy)) / 2 + 4}" style="fill:var(--accent2)">Ea ${ea != null ? +ea.toFixed(1) : ''}</text>`);
  });
  return `<div class="chart"><svg viewBox="0 0 ${w} ${h}" role="img" aria-label="Energy profile: ${esc(p.title || '')}">${parts.join('')}</svg></div>`;
}

function niceTicks(lo, hi, n) {
  const step0 = (hi - lo) / n || 1, mag = 10 ** Math.floor(Math.log10(step0));
  const step = [1, 2, 5, 10].map(m => m * mag).find(s => s >= step0);
  const out = [];
  for (let t = Math.ceil(lo / step) * step; t <= hi + 1e-9; t += step) out.push(+t.toFixed(6));
  return out;
}
