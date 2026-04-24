# ---------------------------------------------------------------
# Demo 04 — Mechanism walkthrough
# ---------------------------------------------------------------
# Enumerate every seeded mechanism and, for each one, report:
#   * the category (Substitution / Addition / Pericyclic / Enzyme / …)
#   * how many curly-arrow steps it carries
#
# Then launch the mechanism player for the Diels-Alder entry.
# The player dialog runs on the main thread — if you're in the
# GUI it'll pop up for Prev / Next navigation; headless it just
# returns the metadata.

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

# Open the Diels-Alder player (no-op if no main window).
target = next((m for m in ms if "Diels" in m["name"]), None)
if target:
    info = app.open_mechanism(name_or_id=str(target["id"]))
    print(f"\nopen_mechanism → {info}")
