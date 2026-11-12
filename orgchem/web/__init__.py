"""Web interface for OrgChem Studio (FastAPI app + static front end; see INTERFACE.md "web/").

- app.py        FastAPI routes under /api and STATIC_ENDPOINTS for the GitHub Pages export
- chemdata.py   seeds a private temporary DB with the app's seeders and keeps plain-dict rows
- depict.py     RDKit 2D / 3D coordinates as compact atom/bond JSON for the browser renderers
- lessons.py    curriculum index + lesson HTML (same Markdown pipeline as the Tutorial panel)
- quiz.py       quiz bank generated from seeded content
- static/       ES-module front end (pages, draw2d.js SVG drawing, viewer3d.js WebGL, chem_engine.js / smarts.js /
                formula_calc.js chemistry ported to JS with node tests)
"""
