"""OrgChem Studio — interactive organic chemistry learning & teaching environment.

Subpackages
-----------
- ``core``      : headless chemistry backend (RDKit wrappers, descriptors, formula).
- ``db``        : SQLAlchemy models + session + seeding.
- ``sources``   : pluggable online data sources (PubChem, …).
- ``render``    : stateless 2D/3D rendering helpers.
- ``gui``       : PySide6 main window, panels, widgets, dialogs.
- ``messaging`` : application-wide signal bus, errors, and logging handler.
- ``utils``     : cross-platform paths, worker-thread helpers.
- ``tutorial``  : curriculum definition and markdown loader.
"""

__version__ = "0.1.0"
