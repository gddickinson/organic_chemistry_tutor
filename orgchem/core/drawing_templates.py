"""Phase 36c (round 129) — ring + functional-group templates.

Pure-Python catalogue of ChemDraw-style templates for the
drawing canvas plus a single :func:`apply_template` helper that
folds a template into a live :class:`Structure` (+ a parallel
list of screen positions).  No Qt imports — fully
headless-testable.

Two template *fuse modes*:

- ``"merge"`` (rings).  The template's anchor atom is fused with
  the host atom — the anchor itself is *not* added; every other
  template atom is appended and bonds are remapped so the
  anchor's bond endpoints become the host's index.  On an empty
  canvas the anchor is placed at the click point and the ring
  is drawn around it.
- ``"attach"`` (functional groups).  The template's anchor atom
  is added as a *new* atom and a single bond
  (``attach_order``-many bonds, really) is created between host
  and anchor.  On an empty canvas the optional
  ``auto_attach_element`` (default ``"C"``) is placed first as
  the synthetic host so e.g. clicking the *COOH* button on
  empty canvas yields acetic acid, not bare ``"OC(=O)"``.

The catalogue is intentionally small and pedagogical — the ten
rings + nine FGs that undergrads + medicinal-chem students reach
for 95 % of the time.  Anything bigger goes through the SMILES
ribbon.
"""
from __future__ import annotations
import copy
import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from orgchem.core.drawing import Atom, Bond, Structure


#: Default screen distance between two bonded atoms — matches the
#: drawing panel's `_BOND_PX`.  Templates store unit-length coords
#: so the same definition works for any future zoom level.
DEFAULT_SCALE_PX = 42.0


@dataclass
class TemplateAtom:
    element: str
    x: float                # unit-length, +x → right
    y: float                # unit-length, +y → up (canvas flips)
    charge: int = 0
    aromatic: bool = False


@dataclass
class TemplateBond:
    begin_idx: int
    end_idx: int
    order: int = 1          # 1/2/3; 4 = aromatic


@dataclass
class Template:
    name: str
    label: str               # toolbar / menu label
    kind: str                # "ring" | "fg"
    atoms: List[TemplateAtom]
    bonds: List[TemplateBond]
    anchor_idx: int = 0
    fuse_mode: str = "merge"
    attach_order: int = 1
    #: Auto-place this element as the host when the user clicks
    #: empty canvas with an *attach*-mode template.  ``None``
    #: means *don't auto-place* — the FG sits on its own.
    auto_attach_element: Optional[str] = "C"

    def __post_init__(self) -> None:
        if self.fuse_mode not in ("merge", "attach"):
            self.fuse_mode = "attach"
        if self.kind not in ("ring", "fg"):
            self.kind = "fg"


# ------------------------------------------------------------------
# Geometry helpers
# ------------------------------------------------------------------

def _regular_polygon(n: int, *, anchor_at_top: bool = True
                     ) -> List[Tuple[float, float]]:
    """Return *n* unit-side polygon vertices.  Anchor (vertex 0)
    is placed at the top so a template's ``anchor_idx=0`` lines
    up with the click point.

    Side length is exactly 1.0 — the same convention every
    template uses, so :func:`apply_template` can multiply by any
    scale at placement time.
    """
    if n < 3:
        raise ValueError(f"polygon needs ≥ 3 vertices, got {n}")
    # Circumradius for a regular n-gon with side length 1.
    R = 1.0 / (2 * math.sin(math.pi / n))
    # Anchor angle: place vertex 0 at the top (90°) when anchored
    # there, else start at 0°.
    start = math.pi / 2 if anchor_at_top else 0.0
    step = 2 * math.pi / n
    return [
        (R * math.cos(start - k * step),     # clockwise from top
         R * math.sin(start - k * step))
        for k in range(n)
    ]


def _ring_template(name: str, label: str, n: int,
                   *, elements: Optional[List[str]] = None,
                   bond_orders: Optional[List[int]] = None
                   ) -> Template:
    """Build a regular n-gon ring template.

    *elements* defaults to all-carbon; *bond_orders* defaults to
    all-single.  Use :data:`bond_orders` filled with 4 for fully
    aromatic rings (benzene, pyridine, …).
    """
    coords = _regular_polygon(n)
    if elements is None:
        elements = ["C"] * n
    if bond_orders is None:
        bond_orders = [1] * n
    if len(elements) != n:
        raise ValueError(f"{name}: need {n} elements, got {len(elements)}")
    if len(bond_orders) != n:
        raise ValueError(f"{name}: need {n} bond orders, got {len(bond_orders)}")
    atoms = [
        TemplateAtom(element=el, x=x, y=y,
                     aromatic=(bond_orders[(i - 1) % n] == 4
                               or bond_orders[i] == 4))
        for i, ((x, y), el) in enumerate(zip(coords, elements))
    ]
    bonds = [
        TemplateBond(begin_idx=i, end_idx=(i + 1) % n, order=bo)
        for i, bo in enumerate(bond_orders)
    ]
    return Template(
        name=name, label=label, kind="ring",
        atoms=atoms, bonds=bonds, anchor_idx=0, fuse_mode="merge",
    )


# ------------------------------------------------------------------
# Catalogue
# ------------------------------------------------------------------

def _build_catalogue() -> Dict[str, Template]:
    out: Dict[str, Template] = {}

    # ---- rings ---------------------------------------------------
    rings = [
        ("cyclopropane", "△ C3", 3),
        ("cyclobutane", "▢ C4", 4),
        ("cyclopentane", "⬠ C5", 5),
        ("cyclohexane", "⬡ C6", 6),
    ]
    for name, label, n in rings:
        out[name] = _ring_template(name, label, n)

    # Aromatic six-membered rings.
    out["benzene"] = _ring_template(
        "benzene", "⬡ Bz", 6,
        bond_orders=[4, 4, 4, 4, 4, 4],
    )
    # Pyridine: N at top so anchor falls on a C across the ring.
    # Conventional drawing: N at vertex 3 (bottom), anchor C at top.
    out["pyridine"] = _ring_template(
        "pyridine", "⬡ Py", 6,
        elements=["C", "C", "C", "N", "C", "C"],
        bond_orders=[4, 4, 4, 4, 4, 4],
    )
    # Pyrimidine: N at vertices 1 and 5 (1,3-diazine pattern,
    # anchor at C-2).
    out["pyrimidine"] = _ring_template(
        "pyrimidine", "⬡ Pm", 6,
        elements=["C", "N", "C", "C", "C", "N"],
        bond_orders=[4, 4, 4, 4, 4, 4],
    )

    # 5-membered aromatic heterocycles.
    out["furan"] = _ring_template(
        "furan", "⬠ Fu", 5,
        elements=["O", "C", "C", "C", "C"],
        bond_orders=[4, 4, 4, 4, 4],
    )
    out["thiophene"] = _ring_template(
        "thiophene", "⬠ Th", 5,
        elements=["S", "C", "C", "C", "C"],
        bond_orders=[4, 4, 4, 4, 4],
    )
    out["pyrrole"] = _ring_template(
        "pyrrole", "⬠ Pr", 5,
        elements=["N", "C", "C", "C", "C"],
        bond_orders=[4, 4, 4, 4, 4],
    )

    # ---- functional groups --------------------------------------
    # OH — single oxygen, attaches via single bond to host.
    out["oh"] = Template(
        name="oh", label="OH", kind="fg",
        atoms=[TemplateAtom(element="O", x=0.0, y=1.0)],
        bonds=[],
        anchor_idx=0, fuse_mode="attach", attach_order=1,
    )
    # NH2 — single nitrogen.
    out["nh2"] = Template(
        name="nh2", label="NH₂", kind="fg",
        atoms=[TemplateAtom(element="N", x=0.0, y=1.0)],
        bonds=[],
        anchor_idx=0, fuse_mode="attach", attach_order=1,
    )
    # Methyl — single carbon (use for CH3 caps or C atoms in
    # branching).
    out["me"] = Template(
        name="me", label="Me", kind="fg",
        atoms=[TemplateAtom(element="C", x=0.0, y=1.0)],
        bonds=[],
        anchor_idx=0, fuse_mode="attach", attach_order=1,
    )
    # COOH — carboxyl C with =O and -OH.  Anchor = carboxyl C.
    out["cooh"] = Template(
        name="cooh", label="COOH", kind="fg",
        atoms=[
            TemplateAtom(element="C", x=0.0, y=1.0),
            TemplateAtom(element="O", x=0.866, y=1.5),    # =O
            TemplateAtom(element="O", x=-0.866, y=1.5),   # -OH
        ],
        bonds=[
            TemplateBond(0, 1, 2),
            TemplateBond(0, 2, 1),
        ],
        anchor_idx=0, fuse_mode="attach", attach_order=1,
    )
    # CHO — aldehyde C with =O.
    out["cho"] = Template(
        name="cho", label="CHO", kind="fg",
        atoms=[
            TemplateAtom(element="C", x=0.0, y=1.0),
            TemplateAtom(element="O", x=0.866, y=1.5),
        ],
        bonds=[TemplateBond(0, 1, 2)],
        anchor_idx=0, fuse_mode="attach", attach_order=1,
    )
    # C=O — bare carbonyl O double-bonded to host.  Anchor IS the
    # O; attach with order 2.
    out["co"] = Template(
        name="co", label="C=O", kind="fg",
        atoms=[TemplateAtom(element="O", x=0.0, y=1.0)],
        bonds=[],
        anchor_idx=0, fuse_mode="attach", attach_order=2,
    )
    # NO2 — nitro group as zwitterion (N+, one =O, one -O−).
    # RDKit insists on the charged form for valence sanity.
    out["no2"] = Template(
        name="no2", label="NO₂", kind="fg",
        atoms=[
            TemplateAtom(element="N", x=0.0, y=1.0, charge=1),
            TemplateAtom(element="O", x=0.866, y=1.5),
            TemplateAtom(element="O", x=-0.866, y=1.5, charge=-1),
        ],
        bonds=[
            TemplateBond(0, 1, 2),
            TemplateBond(0, 2, 1),
        ],
        anchor_idx=0, fuse_mode="attach", attach_order=1,
    )
    # CN — nitrile carbon, triple-bonded to N.
    out["cn"] = Template(
        name="cn", label="CN", kind="fg",
        atoms=[
            TemplateAtom(element="C", x=0.0, y=1.0),
            TemplateAtom(element="N", x=0.0, y=2.0),
        ],
        bonds=[TemplateBond(0, 1, 3)],
        anchor_idx=0, fuse_mode="attach", attach_order=1,
    )
    # OMe — O-CH3.
    out["ome"] = Template(
        name="ome", label="OMe", kind="fg",
        atoms=[
            TemplateAtom(element="O", x=0.0, y=1.0),
            TemplateAtom(element="C", x=0.866, y=1.5),
        ],
        bonds=[TemplateBond(0, 1, 1)],
        anchor_idx=0, fuse_mode="attach", attach_order=1,
    )
    # CF3 — trifluoromethyl.
    out["cf3"] = Template(
        name="cf3", label="CF₃", kind="fg",
        atoms=[
            TemplateAtom(element="C", x=0.0, y=1.0),
            TemplateAtom(element="F", x=0.866, y=1.5),
            TemplateAtom(element="F", x=0.0, y=2.0),
            TemplateAtom(element="F", x=-0.866, y=1.5),
        ],
        bonds=[
            TemplateBond(0, 1, 1),
            TemplateBond(0, 2, 1),
            TemplateBond(0, 3, 1),
        ],
        anchor_idx=0, fuse_mode="attach", attach_order=1,
    )
    return out


_TEMPLATES: Dict[str, Template] = _build_catalogue()


def list_template_names() -> List[str]:
    return list(_TEMPLATES)


def list_templates(kind: Optional[str] = None) -> List[Template]:
    """Return every template, optionally filtered by ``kind``
    (``"ring"`` or ``"fg"``)."""
    if kind is None:
        return list(_TEMPLATES.values())
    return [t for t in _TEMPLATES.values() if t.kind == kind]


def get_template(name: str) -> Optional[Template]:
    return _TEMPLATES.get(name)


# ------------------------------------------------------------------
# Application
# ------------------------------------------------------------------

def apply_template(
    structure: Structure,
    positions: List[Tuple[float, float]],
    template: Template,
    anchor_pos: Tuple[float, float],
    *,
    host_atom_idx: Optional[int] = None,
    scale: float = DEFAULT_SCALE_PX,
) -> Tuple[Structure, List[Tuple[float, float]]]:
    """Fold *template* into *structure* + return the updated
    structure and parallel positions list.

    *positions* are screen coords (pixels); *anchor_pos* is the
    click point (also pixels).  Template-internal coords are unit
    bond-length and get multiplied by ``scale`` here; the canvas
    convention flips y, so we negate the template y at placement.

    The input ``structure`` and ``positions`` are NOT mutated —
    callers receive a fresh copy.  This is what lets the
    DrawingPanel's snapshot-based undo stack work without extra
    bookkeeping.
    """
    s = copy.deepcopy(structure)
    pos = list(positions)
    if not template.atoms:
        return s, pos
    n_existing = len(s.atoms)

    if template.fuse_mode == "merge":
        return _apply_merge(s, pos, template, anchor_pos,
                            host_atom_idx, scale)
    return _apply_attach(s, pos, template, anchor_pos,
                         host_atom_idx, scale)


def _apply_merge(
    s: Structure,
    pos: List[Tuple[float, float]],
    template: Template,
    anchor_pos: Tuple[float, float],
    host_atom_idx: Optional[int],
    scale: float,
) -> Tuple[Structure, List[Tuple[float, float]]]:
    anchor = template.atoms[template.anchor_idx]
    # Pixel offset = template coord * scale, with y flipped to
    # match canvas.
    if host_atom_idx is not None:
        anchor_screen = pos[host_atom_idx]
    else:
        anchor_screen = (anchor_pos[0], anchor_pos[1])
    # Map every template atom index to its *new* structure index.
    # Anchor maps to host (when fusing) or to a freshly added atom
    # (when free-standing).
    idx_map: Dict[int, int] = {}
    if host_atom_idx is None:
        # Add anchor as a new atom too.
        new_idx = s.add_atom(anchor.element)
        s.atoms[new_idx].charge = anchor.charge
        s.atoms[new_idx].aromatic = anchor.aromatic
        pos.append(anchor_screen)
        idx_map[template.anchor_idx] = new_idx
    else:
        idx_map[template.anchor_idx] = host_atom_idx
    # Add every non-anchor atom.
    for ti, ta in enumerate(template.atoms):
        if ti == template.anchor_idx:
            continue
        new_idx = s.add_atom(ta.element)
        s.atoms[new_idx].charge = ta.charge
        s.atoms[new_idx].aromatic = ta.aromatic
        # Position relative to the anchor, scaled to pixels, y flipped.
        dx = (ta.x - anchor.x) * scale
        dy = -(ta.y - anchor.y) * scale
        pos.append((anchor_screen[0] + dx, anchor_screen[1] + dy))
        idx_map[ti] = new_idx
    # Add bonds with remapped endpoints — skip any bond that
    # collapses to a self-loop (shouldn't happen for valid
    # templates, but be defensive).
    for tb in template.bonds:
        a = idx_map[tb.begin_idx]
        b = idx_map[tb.end_idx]
        if a == b:
            continue
        # Skip duplicate bonds — when fusing, the anchor's bonds
        # might already exist on the host; preserving them as-is
        # is fine since the new bonds connect host to new atoms.
        if _bond_exists(s, a, b):
            continue
        s.add_bond(a, b, order=tb.order)
    return s, pos


def _apply_attach(
    s: Structure,
    pos: List[Tuple[float, float]],
    template: Template,
    anchor_pos: Tuple[float, float],
    host_atom_idx: Optional[int],
    scale: float,
) -> Tuple[Structure, List[Tuple[float, float]]]:
    # Empty-canvas attach: optionally synthesise a host atom first.
    if host_atom_idx is None and template.auto_attach_element:
        host_atom_idx = s.add_atom(template.auto_attach_element)
        pos.append((anchor_pos[0], anchor_pos[1]))
    # Add every template atom (no skipping; attach mode adds
    # them all, then connects host ↔ anchor).
    anchor = template.atoms[template.anchor_idx]
    if host_atom_idx is not None:
        anchor_screen = pos[host_atom_idx]
        # Offset template so the anchor lands at one bond above
        # the host (template y origin is the host).
        anchor_origin_x = anchor_screen[0]
        anchor_origin_y = anchor_screen[1]
    else:
        anchor_origin_x, anchor_origin_y = anchor_pos
    idx_map: Dict[int, int] = {}
    for ti, ta in enumerate(template.atoms):
        new_idx = s.add_atom(ta.element)
        s.atoms[new_idx].charge = ta.charge
        s.atoms[new_idx].aromatic = ta.aromatic
        dx = ta.x * scale
        dy = -ta.y * scale
        pos.append((anchor_origin_x + dx, anchor_origin_y + dy))
        idx_map[ti] = new_idx
    # Internal template bonds.
    for tb in template.bonds:
        a = idx_map[tb.begin_idx]
        b = idx_map[tb.end_idx]
        if a == b:
            continue
        s.add_bond(a, b, order=tb.order)
    # Host-to-anchor connection.
    if host_atom_idx is not None:
        anchor_struct_idx = idx_map[template.anchor_idx]
        if not _bond_exists(s, host_atom_idx, anchor_struct_idx):
            s.add_bond(host_atom_idx, anchor_struct_idx,
                       order=template.attach_order)
    return s, pos


def _bond_exists(s: Structure, a: int, b: int) -> bool:
    for bond in s.bonds:
        if {bond.begin_idx, bond.end_idx} == {a, b}:
            return True
    return False
