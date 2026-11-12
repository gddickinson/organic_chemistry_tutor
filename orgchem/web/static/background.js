// Subtle animated background: faint hexagonal rings drifting upward. Skipped under prefers-reduced-motion.
export function background(canvas) {
  if (!canvas || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const ctx = canvas.getContext('2d');
  const rings = Array.from({ length: 16 }, (_, i) => ({ x: Math.random(), y: Math.random(), s: 0.00008 + Math.random() * 0.00018,
    r: 14 + Math.random() * 26, a: Math.random() * Math.PI, p: i }));
  const size = () => { canvas.width = innerWidth; canvas.height = innerHeight; };
  size();
  addEventListener('resize', size);
  const tick = t => {
    const { width: w, height: h } = canvas;
    ctx.clearRect(0, 0, w, h);
    ctx.lineWidth = 1.4;
    for (const k of rings) {
      k.y -= k.s; if (k.y < -0.1) { k.y = 1.1; k.x = Math.random(); }
      const x = k.x * w + Math.sin(t / 3000 + k.p) * 30, y = k.y * h, rot = k.a + t / 9000;
      ctx.strokeStyle = k.p % 3 === 0 ? 'rgba(255,94,168,.35)' : k.p % 3 === 1 ? 'rgba(56,242,216,.35)' : 'rgba(255,209,102,.3)';
      ctx.beginPath();
      for (let i = 0; i <= 6; i++) { const a = rot + i * Math.PI / 3; ctx[i ? 'lineTo' : 'moveTo'](x + k.r * Math.cos(a), y + k.r * Math.sin(a)); }
      ctx.stroke();
    }
    if (!document.hidden) requestAnimationFrame(tick); else setTimeout(() => requestAnimationFrame(tick), 500);
  };
  requestAnimationFrame(tick);
}
