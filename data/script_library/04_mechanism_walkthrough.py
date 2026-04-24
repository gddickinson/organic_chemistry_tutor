# ---------------------------------------------------------------
# Demo 04 — Mechanism walkthrough
# ---------------------------------------------------------------
# Enumerate every seeded mechanism, bucket by category, and then
# drill into the Diels-Alder entry — printing every curly-arrow
# and every lone-pair-dot decoration in every step.  Uses the
# Phase-32e ``get_mechanism_details`` action (round 81) that
# returns the full JSON blob, not just the summary.

ms = app.list_mechanisms()

# Bucket by category so the report reads as a teaching index.
by_cat: dict[str, list[dict]] = {}
for m in ms:
    by_cat.setdefault(m.get("category", "Other"), []).append(m)

print(f"Seeded mechanisms: {len(ms)} across "
      f"{len(by_cat)} categories\n")
for cat, items in sorted(by_cat.items()):
    print(f"  {cat} ({len(items)})")
    for m in sorted(items, key=lambda x: x["name"]):
        print(f"    • {m['name']:42s}  {m['steps']} steps")

# ---------- Arrow-by-arrow drill-down ----------
target = next((m for m in ms if "Diels" in m["name"]), None)
if target:
    detail = app.get_mechanism_details(name_or_id=str(target["id"]))
    if "error" in detail:
        print(f"\n[{detail['error']}]")
    else:
        mech = detail["mechanism"]
        print(f"\n=== {detail['name']} — full arrow walkthrough ===")
        print(f"  category: {detail['category']}")
        print(f"  description: {detail['description'][:120]}…\n")
        for i, step in enumerate(mech.get("steps", []), 1):
            arrows = step.get("arrows", [])
            lps = step.get("lone_pairs", [])
            print(f"  Step {i}: {step.get('title')}")
            print(f"    smiles: {step.get('smiles')}")
            if arrows:
                print(f"    arrows ({len(arrows)}):")
                for a in arrows:
                    src = a.get("from_atom")
                    dst = a.get("to_atom")
                    kind = a.get("kind", "curly")
                    lab = a.get("label") or ""
                    fb = a.get("from_bond")
                    tb = a.get("to_bond")
                    src_repr = f"bond{tuple(fb)}" if fb else f"atom{src}"
                    dst_repr = f"bond{tuple(tb)}" if tb else f"atom{dst}"
                    tag = f"  — {lab}" if lab else ""
                    print(f"      {src_repr} → {dst_repr}  [{kind}]{tag}")
            if lps:
                print(f"    lone-pair dots on atoms: {lps}")
            print()
