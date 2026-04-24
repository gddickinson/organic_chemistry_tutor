# ---------------------------------------------------------------
# Demo 11 — NSAID SAR series: COX inhibition table
# ---------------------------------------------------------------
# Pull the seeded NSAID SAR series, tabulate each variant's
# drug-likeness + COX-1 / COX-2 potency + selectivity index,
# and flag which variants are COX-2-selective enough to dodge
# the classical NSAID gastric-side-effect risk.  A template for
# any SAR-driven medicinal-chemistry lesson.

series_list = app.list_sar_series()
print(f"Seeded SAR series ({len(series_list)}):")
for s in series_list:
    print(f"  • {s['name']:36s} target: {s.get('target', '—')}")

# The NSAID / COX series is seeded with id 'nsaid-cox'.
series = app.get_sar_series(series_id="nsaid-cox")

print(f"\n=== {series['name']} ===")
print(f"  target:   {series.get('target', '—')}")
# SARSeries exposes its variants under `rows` (each row =
# one analogue), with its assay columns listed in
# `activity_columns`.
rows = series.get("rows", [])
print(f"  variants: {len(rows)}\n")

print(f"  {'Name':14s} {'MW':>7s} {'logP':>6s} {'QED':>6s} "
      f"{'COX1 IC50':>10s} {'COX2 IC50':>10s} {'COX2 sel':>9s}  verdict")
print("  " + "-" * 76)
for v in rows:
    c1 = v.get("cox1_ic50_uM")
    c2 = v.get("cox2_ic50_uM")
    sel = v.get("cox2_selectivity")
    # Flag: a variant is COX-2-selective if sel > 1 (COX-1 IC50
    # / COX-2 IC50 > 1, i.e. it inhibits COX-2 at lower
    # concentration than COX-1).  Classical NSAIDs ~0.5; coxibs > 10.
    verdict = "—"
    if sel is not None:
        if sel >= 10:
            verdict = "coxib-like"
        elif sel >= 1.5:
            verdict = "preferential"
        else:
            verdict = "non-selective"
    print(f"  {v['name'][:14]:14s} "
          f"{v.get('mw', 0):7.1f} "
          f"{v.get('logp', 0):6.2f} "
          f"{v.get('qed', 0):6.3f} "
          f"{c1 if c1 is not None else '—':>10} "
          f"{c2 if c2 is not None else '—':>10} "
          f"{sel if sel is not None else '—':>9}  {verdict}")
