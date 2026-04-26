"""Meta-actions — the tutor's self-introspection tools.

Round 55 bug-fix: users reported the tutor refusing to visualise
ligand binding despite the app having a full protein-binding stack.
Root cause: the LLM's training data doesn't know what OrgChem Studio
can do, and a long system prompt is easy to lose in a crowded
context. These meta-actions give the tutor a way to *ask the app*
what's available mid-conversation, grouped by topic.
"""
from __future__ import annotations
from typing import Any, Dict, List

from orgchem.agent.actions import action, registry


# Curated category summary. Keys match the ``category`` string the
# @action decorator uses; values are the one-line description the
# tutor should see when deciding whether to recurse into that area.
_CATEGORY_SUMMARIES: Dict[str, str] = {
    "molecule": "Browse / display / compare molecules from the seeded DB.",
    "tools": "Empirical-formula, IUPAC-formula, hand calculators.",
    "online": "PubChem search + download.",
    "tutorial": "Curriculum lessons (beginner → graduate).",
    "reaction": "Named reactions, 2D / 3D schemes, energy profiles, trajectories.",
    "mechanism": "Step-by-step curly-arrow playback + SVG export.",
    "synthesis": "Multi-step pathways, atom economy, green metrics, retrosynthesis.",
    "dynamics": "Conformer morphs + dihedral scans (interactive 3D HTML).",
    "orbitals": "Hückel MOs + Woodward-Hoffmann rule checks.",
    "stereo": "R/S + E/Z descriptors, wedge/dash 2D, enantiomer flip.",
    "glossary": "Searchable term dictionary (~61 entries).",
    "medchem": "Drug-likeness, SAR series, bioisostere suggestions.",
    "lab": "TLC / Rf, recrystallisation, distillation, acid-base extraction.",
    "naming": "IUPAC naming rule catalogue.",
    "spectroscopy": "IR / ¹H / ¹³C NMR / MS prediction + stick-spectrum export.",
    "session": "Save / load the user's workspace state.",
    "periodic": "118-element interactive periodic table.",
    "carbohydrate": "25-entry carbohydrates catalogue (macromolecule tab).",
    "lipid": "31-entry lipids catalogue (macromolecule tab).",
    "nucleic-acid": "33-entry nucleic-acids catalogue (macromolecule tab).",
    "protein": "PDB + AlphaFold ingestion, binding contacts, PPI, 3D viewer.",
    "export": "2D / 3D image export + screenshots.",
    "window": "Secondary-window management (Macromolecules window).",
    "meta": "Self-introspection actions (this category).",
    # Round 180 (Phase 49e) backfill — categories that shipped
    # after the round-55 baseline but never got a summary entry.
    "authoring": "Add new molecules / reactions / glossary terms / "
                 "tutorial lessons / molecule synonyms to the DB.",
    "biochem": "Major metabolic pathways (glycolysis, TCA, "
               "ox-phos, β-oxidation, …) with per-step substrates / "
               "enzymes / EC numbers / ΔG / regulators.",
    "calc": "Lab calculator solvers — molarity, dilution, "
            "stoichiometry, pH, gas law, colligative, thermo / "
            "kinetics, equilibrium (~ 30 routine bench calcs).",
    "cell": "Cell-component explorer (eukarya / bacteria / "
            "archaea — organelles, membranes, cytoskeleton, "
            "envelopes, ribosomes).",
    "centrifugation": "Centrifuge / rotor catalogue + g↔RPM "
                      "calculator + recommended-protocol lookup.",
    "chromatography": "Chromatography-method reference (TLC, "
                      "HPLC, GC-MS, FPLC, SEC, IC, SFC, …).",
    "clinical": "Clinical chemistry lab panels (BMP / CMP / "
                "Lipid / Diabetes / Thyroid / Vitamin D) with "
                "per-analyte normal ranges + clinical "
                "significance.",
    "drawing": "Headless ChemDraw-equivalent: structure ↔ SMILES, "
               "PNG / SVG / MOL export, reaction-scheme builder.",
    "instrumentation": "Major lab analyser reference catalogue "
                       "(clinical chemistry, hematology, "
                       "molecular, mass-spec, microscopy, "
                       "automation, storage).",
    "isomer": "Stereoisomer + tautomer enumeration + "
              "pairwise-relationship classifier (identical / "
              "enantiomer / diastereomer / meso / tautomer / "
              "constitutional).",
    "kingdom": "Biochemistry-by-Kingdom topics (Eukarya / "
               "Bacteria / Archaea / Viruses × Structure / "
               "Physiology / Genetics).",
    "microscopy": "Microscopy-method reference across resolution "
                  "scales (whole-organism → single-molecule), "
                  "with cross-references to lab analysers.",
    "ph": "pH + buffer explorer — pKa lookup, buffer designer "
          "(Henderson-Hasselbalch), buffer capacity, titration "
          "curve simulator.",
    "phys-org": "Physical organic chemistry — Hammett ρ-σ fits, "
                "primary kinetic isotope effects.",
    "qualitative": "Qualitative inorganic ion / gas tests (flame, "
                   "hydroxide, halide, sulfate, carbonate, NH₄⁺, "
                   "and gas tests).",
    "reagent": "Lab reagents reference (buffers, acids / bases, "
               "detergents, solvents, cell-culture media, "
               "molecular-biology enzymes).",
    "scripting": "Python script editor + 3D scene composer "
                 "workbench window.",
    "search": "Full-text search across every text-bearing column "
              "in the seeded DB (molecules, reactions, "
              "pathways, glossary, mechanism steps).",
    "spectrophotometry": "Spectrophotometry-method reference + "
                         "Beer-Lambert solver (UV-Vis, "
                         "fluorescence, IR / FTIR, NIR, Raman, "
                         "CD, AAS, ICP, NMR).",
}


@action(category="meta")
def list_capabilities(category: str = "") -> Dict[str, Any]:
    """Return the tutor's capability inventory.

    Without a ``category`` argument, returns the list of known
    categories with a one-line description each plus the count of
    agent actions in each. Pass a category to drill in — you get
    every action in that bucket with its docstring's first line.

    Use this whenever a student asks about a topic you're unsure
    the app supports. It's faster and more reliable than guessing
    from memory.

    Examples of useful drill-ins:
    - ``list_capabilities(category="protein")`` — every PDB /
      binding-contact / interaction-map action.
    - ``list_capabilities(category="spectroscopy")`` — every IR /
      NMR / MS tool.
    - ``list_capabilities(category="synthesis")`` — pathways,
      retrosynthesis, atom economy.
    """
    all_actions = registry()
    by_cat: Dict[str, List[Dict[str, str]]] = {}
    for name, spec in all_actions.items():
        cat = getattr(spec, "category", "") or "(uncategorised)"
        fn = getattr(spec, "fn", None) or getattr(spec, "func", None)
        doc = (fn.__doc__ if fn is not None else "") or ""
        doc = doc.strip()
        first_line = doc.splitlines()[0] if doc else ""
        by_cat.setdefault(cat, []).append({
            "name": name, "summary": first_line,
        })
    if not category:
        return {
            "total_actions": len(all_actions),
            "categories": [
                {
                    "category": c,
                    "description": _CATEGORY_SUMMARIES.get(c, ""),
                    "action_count": len(actions),
                    "example_actions": [a["name"] for a in actions[:3]],
                }
                for c, actions in sorted(by_cat.items())
            ],
        }
    key = category.strip().lower()
    match = next(
        (c for c in by_cat if c.lower() == key), None,
    )
    if match is None:
        return {
            "error": f"Unknown category {category!r}. "
                     f"Known: {sorted(by_cat)}",
        }
    return {
        "category": match,
        "description": _CATEGORY_SUMMARIES.get(match, ""),
        "actions": sorted(by_cat[match], key=lambda a: a["name"]),
    }
