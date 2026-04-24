# ---------------------------------------------------------------
# Demo 15 — Glossary catalogue tour
# ---------------------------------------------------------------
# Enumerate every seeded glossary term, bucket by category, and
# show the top entries per category.  Plus a sample ``define``
# call that returns the full markdown definition of one term —
# demonstrates how a tutorial or a tutor can surface glossary
# cross-references programmatically.

from collections import defaultdict

terms = app.list_glossary()
print(f"Glossary catalogue: {len(terms)} terms\n")

by_cat = defaultdict(list)
for t in terms:
    by_cat[t.get("category", "—")].append(t["term"])

print(f"  {'Category':22s}  terms")
print("  " + "-" * 40)
for cat in sorted(by_cat):
    entries = sorted(by_cat[cat])
    print(f"  {cat:22s}  {len(entries)}")

print("\nSample entries per category (first 3):")
for cat in sorted(by_cat):
    entries = sorted(by_cat[cat])
    preview = ", ".join(entries[:3])
    if len(entries) > 3:
        preview += f", … (+{len(entries) - 3} more)"
    print(f"  {cat}:  {preview}")

# Pull the full definition of one well-known term so the
# demo closes with a concrete markdown payload.
demo_term = "Bürgi-Dunitz angle"
try:
    d = app.define(term=demo_term)
except Exception:
    d = None

if d and "definition_md" in d:
    print(f"\n=== define('{demo_term}') ===")
    print(f"category: {d.get('category')}")
    print(f"aliases:  {', '.join(d.get('aliases', []))}")
    print(f"see_also: {', '.join(d.get('see_also', []))}")
    print(f"\n{d['definition_md']}")
