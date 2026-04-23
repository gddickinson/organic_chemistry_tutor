"""Agent actions for Phase 19a — SAR series exploration."""
from __future__ import annotations
import logging
from pathlib import Path
from typing import Any, Dict, List

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


@action(category="medchem")
def list_sar_series() -> List[Dict[str, Any]]:
    """Enumerate the seeded SAR series (NSAIDs, statins, …)."""
    from orgchem.core.sar import list_series
    return list_series()


@action(category="medchem")
def get_sar_series(series_id: str) -> Dict[str, Any]:
    """Return variants + computed medchem descriptors + activity values
    for one seeded SAR series."""
    from orgchem.core.sar import get_series
    s = get_series(series_id)
    if s is None:
        return {"error": f"Unknown SAR series {series_id!r}"}
    return {
        "id": s.id, "name": s.name, "target": s.target,
        "source": s.source,
        "activity_columns": list(s.activity_columns),
        "rows": s.compute_descriptors(),
    }


@action(category="medchem")
def export_sar_matrix(series_id: str, path: str,
                      width: int = 1100, height: int = 460) -> Dict[str, Any]:
    """Render a SAR series as a colour-coded descriptor + activity matrix.
    PNG or SVG by file extension."""
    from orgchem.core.sar import get_series
    from orgchem.render.draw_sar import export_sar_matrix as _export
    from orgchem.messaging.errors import RenderError
    s = get_series(series_id)
    if s is None:
        return {"error": f"Unknown SAR series {series_id!r}"}
    try:
        out = _export(s, path, width=width, height=height)
    except RenderError as e:
        return {"error": str(e)}
    return {"path": str(out), "series_id": series_id,
            "n_variants": len(s.variants),
            "format": Path(out).suffix.lstrip(".").lower(),
            "size_bytes": out.stat().st_size}
