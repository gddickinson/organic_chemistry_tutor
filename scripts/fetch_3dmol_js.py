"""Download 3Dmol.js for offline use — Phase 20a.

Run once (``python scripts/fetch_3dmol_js.py``); the JS bundle lands
under ``orgchem/gui/assets/3Dmol-min.js`` and every future
``build_3dmol_html`` call inlines it so the app works offline.
"""
from __future__ import annotations
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from orgchem.render.draw3d import _3DMOL_CDN, local_3dmol_path  # noqa: E402


def main() -> int:
    dest = local_3dmol_path()
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 1000:
        print(f"3Dmol.js already bundled → {dest} "
              f"({dest.stat().st_size} bytes)")
        return 0
    print(f"Downloading 3Dmol.js from {_3DMOL_CDN} ...")
    try:
        with urllib.request.urlopen(_3DMOL_CDN, timeout=60) as resp:
            data = resp.read()
    except urllib.error.URLError as e:
        print(f"ERROR: {e}")
        return 1
    dest.write_bytes(data)
    print(f"Bundled 3Dmol.js → {dest} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
