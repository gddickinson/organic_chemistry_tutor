"""Drive the app through canonical states and save a PNG gallery.

Uses the agent action registry — the same path any external LLM (including
a Claude Code session) would use. Output lands under ``screenshots/tour/``.

Gallery contents:
  00_initial           — fresh app, nothing selected
  01–04_<molecule>     — main workspace after selecting each of 4 molecules
  05_viewer_2d         — standalone 2D panel (Porphyrin)
  06_viewer_3d_3dmol   — 3D panel with 3Dmol backend (blank in headless — WebGL)
  07_properties        — right-dock property table
  08_browser           — left-dock molecule list
  09_session_log       — bottom-dock log
  10_reactions         — full Reactions tab
  11_compare           — Compare tab with 4 molecules side-by-side
  export_caffeine.png/.svg — File → Export current molecule (2D)
  reaction_*.svg       — File → Export reaction exports
  3d_*_mpl.png         — matplotlib-backend 3D renderings
  energy_*.png         — Phase 13 reaction-coordinate energy profiles
  mo_*.png             — Phase 14a Hückel MO level diagrams
  stereo_*.png         — R/S + E/Z 2D renders with wedge/dash
  13_glossary.png      — Phase 11b Glossary tab
"""
from __future__ import annotations
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

OUT = ROOT / "screenshots" / "tour"

_MOLECULES = [
    ("Caffeine",    1200),
    ("Cholesterol",  900),
    ("Nicotine",     900),
    ("Porphyrin",    900),
]

_REACTIONS_TO_EXPORT = [
    ("Fischer esterification", "reaction_fischer.svg"),
    ("SN2: methyl bromide",    "reaction_sn2.svg"),
    ("Diels-Alder",            "reaction_diels_alder.svg"),
    ("Friedel-Crafts alkylation", "reaction_fc_alkylation.svg"),
]

_MPL_3D_MOLECULES = [
    (7,  "caffeine",    "ball-and-stick"),
    (17, "cholesterol", "ball-and-stick"),
    (17, "cholesterol", "sphere"),
    (14, "porphyrin",   "stick"),
]

_COMPARE_IDS = [6, 7, 17, 15]  # Nicotine, Caffeine, Cholesterol, Thiamine


def main() -> int:
    from orgchem.agent.headless import HeadlessApp

    OUT.mkdir(parents=True, exist_ok=True)
    print(f"Writing screenshots to {OUT}")

    with HeadlessApp(show=False) as app:
        app.window.resize(1500, 950)
        app.pump(15)
        time.sleep(0.5)

        # 00 – initial empty state
        app.call("screenshot_window",
                 path=str(OUT / "00_initial.png"), settle_ms=300)

        # 01–04 – four reference molecules in the main workspace
        for idx, (name, settle) in enumerate(_MOLECULES, start=1):
            app.call("show_molecule", name_or_id=name)
            app.pump(20)
            time.sleep(settle / 1000.0)
            app.call("screenshot_window",
                     path=str(OUT / f"{idx:02d}_{name.lower()}.png"),
                     settle_ms=300)

        # 05 – 2D panel only
        app.call("screenshot_panel", panel_name="viewer_2d",
                 path=str(OUT / "05_viewer_2d.png"), settle_ms=200)
        # 06 – 3D panel (3Dmol backend; blank under offscreen WebGL)
        app.call("screenshot_panel", panel_name="viewer_3d",
                 path=str(OUT / "06_viewer_3d_3dmol.png"), settle_ms=400)
        # 07–09 – property / browser / log
        app.call("screenshot_panel", panel_name="props",
                 path=str(OUT / "07_properties.png"), settle_ms=100)
        app.call("screenshot_panel", panel_name="browser",
                 path=str(OUT / "08_browser.png"), settle_ms=100)
        app.call("screenshot_panel", panel_name="session_log",
                 path=str(OUT / "09_session_log.png"), settle_ms=100)

        # 10 – Reactions tab after selecting Diels-Alder
        app.call("show_reaction", name_or_id="Diels-Alder")
        app.pump(15)
        time.sleep(0.4)
        app.call("screenshot_window",
                 path=str(OUT / "10_reactions.png"), settle_ms=300)

        # 11 – Compare tab with 4 molecules
        app.call("compare_molecules", molecule_ids=_COMPARE_IDS)
        app.pump(15)
        time.sleep(0.3)
        app.call("screenshot_window",
                 path=str(OUT / "11_compare.png"), settle_ms=300)

        # ---- Exports (no screenshots, produced directly by agent actions) ----

        # 2D molecule exports
        app.call("export_molecule_2d_by_id", molecule_id=7,
                 path=str(OUT / "export_caffeine.png"),
                 width=800, height=600)
        app.call("export_molecule_2d_by_id", molecule_id=7,
                 path=str(OUT / "export_caffeine.svg"),
                 width=800, height=600)

        # Reaction exports
        for substr, fname in _REACTIONS_TO_EXPORT:
            rows = app.call("list_reactions", filter=substr)
            if rows:
                app.call("export_reaction_by_id",
                         reaction_id=rows[0]["id"],
                         path=str(OUT / fname))

        # Matplotlib 3D exports
        for mid, name, style in _MPL_3D_MOLECULES:
            app.call("export_molecule_3d",
                     molecule_id=mid,
                     path=str(OUT / f"3d_{name}_{style}_mpl.png"),
                     style=style, width=800, height=600)

        # Mechanism step SVGs — one per step of each textbook mechanism
        mechs = app.call("list_mechanisms")
        for m in mechs:
            safe = (m["name"].split(":")[0]
                    .replace(" ", "_").replace("/", "_").replace("(", "").replace(")", ""))
            for step_idx in range(m["steps"]):
                app.call("export_mechanism_step",
                         reaction_id=m["id"], step_index=step_idx,
                         path=str(OUT / f"mech_{safe}_step{step_idx + 1}.svg"))

        # Static 3D side-by-side renders (Phase 2c.1) — only reactions with
        # mapped SMARTS; action returns error dict for the others which we skip.
        for substr, fname in [("SN2: methyl bromide", "rxn3d_sn2.png"),
                               ("SN1: tert-butyl", "rxn3d_sn1.png"),
                               ("PCC oxidation", "rxn3d_pcc.png"),
                               ("NaBH4 reduction", "rxn3d_nabh4.png"),
                               ("Catalytic hydrogenation", "rxn3d_h2.png")]:
            rxns = app.call("list_reactions", filter=substr)
            if rxns:
                app.call("export_reaction_3d",
                         reaction_id=rxns[0]["id"],
                         path=str(OUT / fname))

        # 3D trajectory HTML (Phase 2c.2) — open in a browser to play the animation.
        for substr, fname in [("SN2: methyl bromide", "trajectory_sn2.html"),
                               ("SN1: tert-butyl", "trajectory_sn1.html"),
                               ("Catalytic hydrogenation", "trajectory_h2.html")]:
            rxns = app.call("list_reactions", filter=substr)
            if rxns:
                app.call("export_reaction_trajectory_html",
                         reaction_id=rxns[0]["id"],
                         path=str(OUT / fname),
                         n_frames=24)

        # Synthesis pathways (Phase 8) — vertical schemes.
        for substr, fname in [
            ("Aspirin (acet",            "pathway_aspirin.png"),
            ("Paracetamol (acet",        "pathway_paracetamol.png"),
            ("BHC",                      "pathway_ibuprofen_bhc.png"),
            ("Wöhler",                   "pathway_wohler.png"),
            ("Caffeine by N-methylation","pathway_caffeine.png"),
            ("Phenacetin",               "pathway_phenacetin.png"),
            ("Paracetamol from phenol",  "pathway_paracetamol_3step.png"),
            ("Kolbe-Schmitt",            "pathway_aspirin_kolbe.png"),
            ("Vanillin from eugenol",    "pathway_vanillin.png"),
            ("Aniline from benzene",     "pathway_aniline.png"),
            ("2-Methyl-2-butanol",       "pathway_grignard_tamyl.png"),
            ("SPPS",                     "pathway_spps_enkephalin.png"),
        ]:
            paths = app.call("list_pathways", filter=substr)
            if paths:
                app.call("export_pathway",
                         pathway_id=paths[0]["id"],
                         path=str(OUT / fname))

        # Phase 10a — conformational-dynamics demos (open each HTML in a browser).
        for demo, fname in [("butane", "dynamics_butane.html"),
                             ("ethane", "dynamics_ethane.html"),
                             ("cyclohexane", "dynamics_cyclohexane.html")]:
            app.call("run_dihedral_scan_demo", demo=demo,
                     path=str(OUT / fname), n_frames=36)

        # Phase 13 — reaction-coordinate energy profiles (one per seeded profile).
        for row in app.call("list_energy_profiles"):
            safe = (row["name"].split(":")[0]
                    .replace(" ", "_").replace("/", "_").lower())
            app.call("export_energy_profile",
                     reaction_id=row["id"],
                     path=str(OUT / f"energy_{safe}.png"))

        # Phase 14a — Hückel MO level diagrams for canonical teaching cases.
        for label, smi in [("ethene", "C=C"),
                            ("butadiene", "C=CC=C"),
                            ("benzene", "c1ccccc1"),
                            ("allyl_cation", "[CH2+]C=C"),
                            ("cyclopentadienide", "[cH-]1cccc1"),
                            ("pyrrole", "c1cc[nH]c1")]:
            app.call("export_mo_diagram", smiles=smi,
                     path=str(OUT / f"mo_{label}.png"))

        # Stereo: R vs S ibuprofen side-by-side (wedge bonds + CIP labels).
        for label, smi in [("R_ibuprofen", "CC(C)Cc1ccc(cc1)[C@@H](C)C(=O)O"),
                            ("S_ibuprofen", "CC(C)Cc1ccc(cc1)[C@H](C)C(=O)O"),
                            ("trans_2_butene", "C/C=C/C"),
                            ("cis_2_butene",  r"C/C=C\C")]:
            app.call("export_molecule_2d_stereo", smiles=smi,
                     path=str(OUT / f"stereo_{label}.png"))

        # Phase 11b — Glossary tab screenshot.
        app.call("show_term", term="SN2")
        app.pump(15)
        time.sleep(0.3)
        app.call("screenshot_window", path=str(OUT / "13_glossary.png"),
                 settle_ms=300)

        # Screenshot the Synthesis tab itself for the gallery.
        app.call("show_pathway", name_or_id="Aspirin")
        app.pump(15)
        time.sleep(0.3)
        app.call("screenshot_window", path=str(OUT / "12_synthesis.png"),
                 settle_ms=300)

    print()
    print("Gallery contents:")
    for p in sorted(OUT.iterdir()):
        print(f"  {p.name:<38}  {p.stat().st_size:>9,} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
