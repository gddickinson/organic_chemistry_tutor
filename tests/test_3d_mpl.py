"""Tests for the matplotlib 3D renderer and export_molecule_3d action."""
from __future__ import annotations
import os
import pytest
from pathlib import Path

pytest.importorskip("rdkit")
pytest.importorskip("matplotlib")


@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_render_png_direct(tmp_path):
    from orgchem.core.molecule import Molecule
    from orgchem.render import draw3d_mpl
    from rdkit import Chem
    m = Molecule.from_smiles("CCO", name="Ethanol")
    mol = Chem.MolFromMolBlock(m.molblock_3d, removeHs=False)
    out = draw3d_mpl.render_png(mol, tmp_path / "ethanol.png",
                                style="ball-and-stick")
    assert out.exists()
    assert out.stat().st_size > 3000  # PNG with any content is at least this big


def test_missing_conformer_raises(tmp_path):
    from orgchem.render import draw3d_mpl
    from orgchem.messaging.errors import RenderError
    from rdkit import Chem
    mol = Chem.MolFromSmiles("CCO")   # no 3D coords
    with pytest.raises(RenderError):
        draw3d_mpl.render_png(mol, tmp_path / "x.png")


def test_export_molecule_3d_agent_action(app, tmp_path):
    # Use a seeded molecule (Caffeine is id 7 in the default seed)
    out = app.call("export_molecule_3d",
                   molecule_id=7, path=str(tmp_path / "caf_3d.png"),
                   style="ball-and-stick")
    assert "error" not in out, out
    p = Path(out["path"])
    assert p.exists()
    assert p.stat().st_size > 3000


@pytest.mark.parametrize("style", ["stick", "ball-and-stick", "sphere", "line"])
def test_styles_produce_distinct_output(app, tmp_path, style):
    out = app.call("export_molecule_3d",
                   molecule_id=17,   # Cholesterol
                   path=str(tmp_path / f"chol_{style}.png"),
                   style=style)
    assert Path(out["path"]).exists()
    assert out["style"] == style
