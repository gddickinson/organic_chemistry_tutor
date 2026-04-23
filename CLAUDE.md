# OrgChem Studio — Claude Code Instructions

@INTERFACE.md

**Always consult `INTERFACE.md` before opening any source file.** It is the
top-level navigation map and is kept in sync with the project structure.

Two more living docs you must keep current:
- `PROJECT_STATUS.md` — what works today + metrics + known issues. Update
  at the end of any session that makes meaningful progress.
- `ROADMAP.md` — phased plan. Tick items as you finish them and move them
  into `PROJECT_STATUS.md`'s "What works today" list.

## Project summary
An interactive PySide6 desktop application for learning and teaching organic
chemistry: molecule database, 2D/3D viewers, descriptors, online download
(PubChem, extensible), curriculum-based tutorials, and a session-log panel for
messaging. Built on RDKit + 3Dmol.js + SQLAlchemy/SQLite.

Reference paper reimplemented & superseded:
Verma, Singh, Passey (2024), *Rasayan J. Chem.* 17(4):1460–1472.
Their empirical→molecular formula calculation lives in `orgchem/core/formula.py`
and is exposed via `Tools → Empirical / Molecular Formula Calculator…`.
Their 15 reference compounds seed the database (`orgchem/db/seed.py`).

## Coding rules (project)
- **Max 500 lines per file** (per global rule). If a file is growing, split into
  a new module and update `INTERFACE.md`.
- **No GUI imports inside `core/`** — the chemistry back-end must be headless-testable.
- **All cross-panel communication goes through `messaging/bus.py`.**
  Do not wire one panel directly into another.
- **All logging via `logging`** — never `print()`. The bus handler routes
  records to the `SessionLogPanel`.
- **Long-running work on a worker thread** (`utils/threading.py`) — never
  block the UI.
- **Update `INTERFACE.md` and `SESSION_LOG.md`** whenever the layout changes or
  a session makes meaningful progress.

## How to run
```
pip install -r requirements.txt
python main.py
```

## Running tests
```
pytest tests/
```

## Where each concern lives (quick)
- A new molecule descriptor  → `orgchem/core/descriptors.py`
- A new online data source   → `orgchem/sources/` + register in `search_panel.py`
- A new 2D rendering option  → `orgchem/render/draw2d.py` + `viewer_2d.py`
- A new 3D style             → `orgchem/render/draw3d.py` (`_style_spec`) + `viewer_3d.py`
- A new lesson               → markdown in `orgchem/tutorial/content/<level>/` + entry in `curriculum.py`
- A new panel                → `orgchem/gui/panels/` + register in `main_window.py`
