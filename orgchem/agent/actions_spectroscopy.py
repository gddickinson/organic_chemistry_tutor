"""Agent actions for Phase 4 — spectroscopy prediction (IR first)."""
from __future__ import annotations
import logging
from pathlib import Path
from typing import Any, Dict

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


@action(category="spectroscopy")
def predict_ir_bands(smiles: str) -> Dict[str, Any]:
    """Return the predicted IR bands for a molecule — functional-group
    SMARTS matching onto a canonical Silverstein-style correlation chart.
    Teaching-grade, not quantitative."""
    from orgchem.core.spectroscopy import predict_bands
    return predict_bands(smiles)


@action(category="spectroscopy")
def predict_nmr_shifts(smiles: str, nucleus: str = "H") -> Dict[str, Any]:
    """Predict ¹H or ¹³C NMR peaks for a molecule (Phase 4).

    ``nucleus``: ``"H"`` (default) or ``"C"``. Returns a peak list
    sorted high-to-low ppm, each with environment label, SMARTS-matched
    atom indices, chemical-shift range, and multiplicity hint (H only).
    Teaching-grade — not a GIAO / DFT calculation.
    """
    from orgchem.core.nmr import predict_shifts
    return predict_shifts(smiles, nucleus=nucleus)


@action(category="spectroscopy")
def export_nmr_spectrum(smiles: str, path: str, nucleus: str = "H",
                        width: int = 900, height: int = 400,
                        title: str = "") -> Dict[str, Any]:
    """Render a schematic stick NMR spectrum (PNG / SVG by extension)."""
    from orgchem.render.draw_nmr import export_nmr_spectrum as _export
    from orgchem.messaging.errors import RenderError
    from pathlib import Path as _P
    try:
        out = _export(smiles, path, nucleus=nucleus,
                      width=width, height=height, title=title)
    except RenderError as e:
        return {"error": str(e)}
    return {"path": str(out), "smiles": smiles, "nucleus": nucleus,
            "format": _P(out).suffix.lstrip(".").lower(),
            "size_bytes": out.stat().st_size}


@action(category="spectroscopy")
def export_ir_spectrum(smiles: str, path: str,
                       width: int = 900, height: int = 420,
                       title: str = "") -> Dict[str, Any]:
    """Render a schematic IR spectrum (PNG or SVG by file extension)."""
    from orgchem.render.draw_ir import export_ir_spectrum as _export
    from orgchem.messaging.errors import RenderError
    try:
        out = _export(smiles, path, width=width, height=height, title=title)
    except RenderError as e:
        return {"error": str(e)}
    return {"path": str(out), "smiles": smiles,
            "format": Path(out).suffix.lstrip(".").lower(),
            "size_bytes": out.stat().st_size}


@action(category="spectroscopy")
def predict_ms(smiles: str) -> Dict[str, Any]:
    """Predict monoisotopic mass + isotope pattern around M⁺ (Phase 4).

    Returns ``{"formula", "monoisotopic_mass", "peaks": [...]}``.
    Intensities are normalised so the tallest peak = 1.0 ; halogens
    (Cl, Br) and sulfur drive the classic M+2 / M+4 isotope diagnostics.
    """
    from orgchem.core.ms import isotope_pattern
    return isotope_pattern(smiles)


@action(category="spectroscopy")
def export_ms_spectrum(smiles: str, path: str,
                       width: int = 900, height: int = 380,
                       title: str = "") -> Dict[str, Any]:
    """Render a schematic MS stick spectrum (molecular-ion region)."""
    from orgchem.render.draw_ms import export_ms_spectrum as _export
    from orgchem.messaging.errors import RenderError
    try:
        out = _export(smiles, path, width=width, height=height, title=title)
    except RenderError as e:
        return {"error": str(e)}
    return {"path": str(out), "smiles": smiles,
            "format": Path(out).suffix.lstrip(".").lower(),
            "size_bytes": out.stat().st_size}
