"""Periodic table data — Phase 27a (round 35).

Hand-curated element data for the interactive periodic-table dialog
(Phase 27). Atomic masses come from RDKit's built-in
:class:`PeriodicTable` so we don't duplicate NIST tables; the
pedagogical columns (category, common oxidation states,
electronegativity, electron configuration, group/period/block
placement) are hand-seeded for the full 1-118 set.

Kept headless (no Qt / GUI imports) so the table is usable from
agent actions, the CLI, and the future Phase 27b renderer.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from rdkit.Chem import GetPeriodicTable


# ---------------------------------------------------------------------
# Category palette (used by the renderer in Phase 27b).

CATEGORY_COLOURS: Dict[str, str] = {
    "alkali-metal":          "#ff6666",
    "alkaline-earth-metal":  "#ffb366",
    "transition-metal":      "#ffd966",
    "post-transition-metal": "#b0b0b0",
    "metalloid":             "#a0cfa0",
    "nonmetal":              "#9fd8e4",
    "halogen":               "#83c9e0",
    "noble-gas":             "#c896e0",
    "lanthanide":            "#f7b9d6",
    "actinide":              "#f097c0",
    "unknown":               "#dddddd",
}


@dataclass(frozen=True)
class Element:
    symbol: str
    name: str
    z: int                          # atomic number
    group: Optional[int]            # 1-18, None for lanthanides/actinides
    period: int
    block: str                      # "s" / "p" / "d" / "f"
    category: str                   # one of CATEGORY_COLOURS keys
    atomic_mass: float              # standard atomic weight (RDKit)
    electronegativity: Optional[float] = None   # Pauling scale
    common_oxidation_states: Tuple[int, ...] = field(default_factory=tuple)
    electron_configuration: str = ""

    def colour(self) -> str:
        return CATEGORY_COLOURS.get(self.category,
                                    CATEGORY_COLOURS["unknown"])

    def to_dict(self) -> Dict[str, object]:
        return {
            "symbol": self.symbol, "name": self.name, "z": self.z,
            "group": self.group, "period": self.period,
            "block": self.block, "category": self.category,
            "atomic_mass": round(self.atomic_mass, 4),
            "electronegativity": self.electronegativity,
            "common_oxidation_states": list(self.common_oxidation_states),
            "electron_configuration": self.electron_configuration,
            "colour": self.colour(),
        }


# ---------------------------------------------------------------------
# Hand-seeded pedagogical data. Masses come from RDKit at runtime so
# we don't need to duplicate NIST's table here. (name, group, period,
# block, category, pauling χ, oxidation states, electron config).
# Noble-gas-shell shorthand ([He], [Ne], etc.) is used where sensible.
_SEED: List[tuple] = [
    # z=1..10 — periods 1-2
    ("H",  "Hydrogen",     1,  1, "s", "nonmetal",            2.20, (-1, 1),      "1s1"),
    ("He", "Helium",       18, 1, "s", "noble-gas",           None, (0,),         "1s2"),
    ("Li", "Lithium",      1,  2, "s", "alkali-metal",        0.98, (1,),         "[He] 2s1"),
    ("Be", "Beryllium",    2,  2, "s", "alkaline-earth-metal",1.57, (2,),         "[He] 2s2"),
    ("B",  "Boron",        13, 2, "p", "metalloid",           2.04, (3,),         "[He] 2s2 2p1"),
    ("C",  "Carbon",       14, 2, "p", "nonmetal",            2.55, (-4, 2, 4),   "[He] 2s2 2p2"),
    ("N",  "Nitrogen",     15, 2, "p", "nonmetal",            3.04, (-3, 3, 5),   "[He] 2s2 2p3"),
    ("O",  "Oxygen",       16, 2, "p", "nonmetal",            3.44, (-2,),        "[He] 2s2 2p4"),
    ("F",  "Fluorine",     17, 2, "p", "halogen",             3.98, (-1,),        "[He] 2s2 2p5"),
    ("Ne", "Neon",         18, 2, "p", "noble-gas",           None, (0,),         "[He] 2s2 2p6"),
    # z=11..18 — period 3
    ("Na", "Sodium",       1,  3, "s", "alkali-metal",        0.93, (1,),         "[Ne] 3s1"),
    ("Mg", "Magnesium",    2,  3, "s", "alkaline-earth-metal",1.31, (2,),         "[Ne] 3s2"),
    ("Al", "Aluminium",    13, 3, "p", "post-transition-metal",1.61,(3,),         "[Ne] 3s2 3p1"),
    ("Si", "Silicon",      14, 3, "p", "metalloid",           1.90, (-4, 4),      "[Ne] 3s2 3p2"),
    ("P",  "Phosphorus",   15, 3, "p", "nonmetal",            2.19, (-3, 3, 5),   "[Ne] 3s2 3p3"),
    ("S",  "Sulfur",       16, 3, "p", "nonmetal",            2.58, (-2, 2, 4, 6),"[Ne] 3s2 3p4"),
    ("Cl", "Chlorine",     17, 3, "p", "halogen",             3.16, (-1, 1, 3, 5, 7), "[Ne] 3s2 3p5"),
    ("Ar", "Argon",        18, 3, "p", "noble-gas",           None, (0,),         "[Ne] 3s2 3p6"),
    # z=19..36 — period 4 (first transition row)
    ("K",  "Potassium",    1,  4, "s", "alkali-metal",        0.82, (1,),         "[Ar] 4s1"),
    ("Ca", "Calcium",      2,  4, "s", "alkaline-earth-metal",1.00, (2,),         "[Ar] 4s2"),
    ("Sc", "Scandium",     3,  4, "d", "transition-metal",    1.36, (3,),         "[Ar] 3d1 4s2"),
    ("Ti", "Titanium",     4,  4, "d", "transition-metal",    1.54, (2, 3, 4),    "[Ar] 3d2 4s2"),
    ("V",  "Vanadium",     5,  4, "d", "transition-metal",    1.63, (2, 3, 4, 5), "[Ar] 3d3 4s2"),
    ("Cr", "Chromium",     6,  4, "d", "transition-metal",    1.66, (2, 3, 6),    "[Ar] 3d5 4s1"),
    ("Mn", "Manganese",    7,  4, "d", "transition-metal",    1.55, (2, 3, 4, 7), "[Ar] 3d5 4s2"),
    ("Fe", "Iron",         8,  4, "d", "transition-metal",    1.83, (2, 3),       "[Ar] 3d6 4s2"),
    ("Co", "Cobalt",       9,  4, "d", "transition-metal",    1.88, (2, 3),       "[Ar] 3d7 4s2"),
    ("Ni", "Nickel",       10, 4, "d", "transition-metal",    1.91, (2,),         "[Ar] 3d8 4s2"),
    ("Cu", "Copper",       11, 4, "d", "transition-metal",    1.90, (1, 2),       "[Ar] 3d10 4s1"),
    ("Zn", "Zinc",         12, 4, "d", "transition-metal",    1.65, (2,),         "[Ar] 3d10 4s2"),
    ("Ga", "Gallium",      13, 4, "p", "post-transition-metal",1.81,(3,),         "[Ar] 3d10 4s2 4p1"),
    ("Ge", "Germanium",    14, 4, "p", "metalloid",           2.01, (-4, 2, 4),   "[Ar] 3d10 4s2 4p2"),
    ("As", "Arsenic",      15, 4, "p", "metalloid",           2.18, (-3, 3, 5),   "[Ar] 3d10 4s2 4p3"),
    ("Se", "Selenium",     16, 4, "p", "nonmetal",            2.55, (-2, 2, 4, 6),"[Ar] 3d10 4s2 4p4"),
    ("Br", "Bromine",      17, 4, "p", "halogen",             2.96, (-1, 1, 5),   "[Ar] 3d10 4s2 4p5"),
    ("Kr", "Krypton",      18, 4, "p", "noble-gas",           3.00, (0, 2),       "[Ar] 3d10 4s2 4p6"),
    # z=37..54 — period 5
    ("Rb", "Rubidium",     1,  5, "s", "alkali-metal",        0.82, (1,),         "[Kr] 5s1"),
    ("Sr", "Strontium",    2,  5, "s", "alkaline-earth-metal",0.95, (2,),         "[Kr] 5s2"),
    ("Y",  "Yttrium",      3,  5, "d", "transition-metal",    1.22, (3,),         "[Kr] 4d1 5s2"),
    ("Zr", "Zirconium",    4,  5, "d", "transition-metal",    1.33, (4,),         "[Kr] 4d2 5s2"),
    ("Nb", "Niobium",      5,  5, "d", "transition-metal",    1.60, (3, 5),       "[Kr] 4d4 5s1"),
    ("Mo", "Molybdenum",   6,  5, "d", "transition-metal",    2.16, (4, 6),       "[Kr] 4d5 5s1"),
    ("Tc", "Technetium",   7,  5, "d", "transition-metal",    1.90, (4, 7),       "[Kr] 4d5 5s2"),
    ("Ru", "Ruthenium",    8,  5, "d", "transition-metal",    2.20, (3, 4),       "[Kr] 4d7 5s1"),
    ("Rh", "Rhodium",      9,  5, "d", "transition-metal",    2.28, (3,),         "[Kr] 4d8 5s1"),
    ("Pd", "Palladium",    10, 5, "d", "transition-metal",    2.20, (0, 2, 4),    "[Kr] 4d10"),
    ("Ag", "Silver",       11, 5, "d", "transition-metal",    1.93, (1,),         "[Kr] 4d10 5s1"),
    ("Cd", "Cadmium",      12, 5, "d", "transition-metal",    1.69, (2,),         "[Kr] 4d10 5s2"),
    ("In", "Indium",       13, 5, "p", "post-transition-metal",1.78,(3,),         "[Kr] 4d10 5s2 5p1"),
    ("Sn", "Tin",          14, 5, "p", "post-transition-metal",1.96,(2, 4),       "[Kr] 4d10 5s2 5p2"),
    ("Sb", "Antimony",     15, 5, "p", "metalloid",           2.05, (-3, 3, 5),   "[Kr] 4d10 5s2 5p3"),
    ("Te", "Tellurium",    16, 5, "p", "metalloid",           2.10, (-2, 2, 4, 6),"[Kr] 4d10 5s2 5p4"),
    ("I",  "Iodine",       17, 5, "p", "halogen",             2.66, (-1, 1, 5, 7),"[Kr] 4d10 5s2 5p5"),
    ("Xe", "Xenon",        18, 5, "p", "noble-gas",           2.60, (0, 2, 4, 6, 8),"[Kr] 4d10 5s2 5p6"),
    # z=55..71 — period 6 s-block + lanthanides
    ("Cs", "Caesium",      1,  6, "s", "alkali-metal",        0.79, (1,),         "[Xe] 6s1"),
    ("Ba", "Barium",       2,  6, "s", "alkaline-earth-metal",0.89, (2,),         "[Xe] 6s2"),
    ("La", "Lanthanum",    None, 6, "f", "lanthanide",        1.10, (3,),         "[Xe] 5d1 6s2"),
    ("Ce", "Cerium",       None, 6, "f", "lanthanide",        1.12, (3, 4),       "[Xe] 4f1 5d1 6s2"),
    ("Pr", "Praseodymium", None, 6, "f", "lanthanide",        1.13, (3,),         "[Xe] 4f3 6s2"),
    ("Nd", "Neodymium",    None, 6, "f", "lanthanide",        1.14, (3,),         "[Xe] 4f4 6s2"),
    ("Pm", "Promethium",   None, 6, "f", "lanthanide",        1.13, (3,),         "[Xe] 4f5 6s2"),
    ("Sm", "Samarium",     None, 6, "f", "lanthanide",        1.17, (2, 3),       "[Xe] 4f6 6s2"),
    ("Eu", "Europium",     None, 6, "f", "lanthanide",        1.20, (2, 3),       "[Xe] 4f7 6s2"),
    ("Gd", "Gadolinium",   None, 6, "f", "lanthanide",        1.20, (3,),         "[Xe] 4f7 5d1 6s2"),
    ("Tb", "Terbium",      None, 6, "f", "lanthanide",        1.20, (3, 4),       "[Xe] 4f9 6s2"),
    ("Dy", "Dysprosium",   None, 6, "f", "lanthanide",        1.22, (3,),         "[Xe] 4f10 6s2"),
    ("Ho", "Holmium",      None, 6, "f", "lanthanide",        1.23, (3,),         "[Xe] 4f11 6s2"),
    ("Er", "Erbium",       None, 6, "f", "lanthanide",        1.24, (3,),         "[Xe] 4f12 6s2"),
    ("Tm", "Thulium",      None, 6, "f", "lanthanide",        1.25, (2, 3),       "[Xe] 4f13 6s2"),
    ("Yb", "Ytterbium",    None, 6, "f", "lanthanide",        1.10, (2, 3),       "[Xe] 4f14 6s2"),
    ("Lu", "Lutetium",     3,  6, "d", "lanthanide",          1.27, (3,),         "[Xe] 4f14 5d1 6s2"),
    # z=72..86 — period 6 d + p
    ("Hf", "Hafnium",      4,  6, "d", "transition-metal",    1.30, (4,),         "[Xe] 4f14 5d2 6s2"),
    ("Ta", "Tantalum",     5,  6, "d", "transition-metal",    1.50, (5,),         "[Xe] 4f14 5d3 6s2"),
    ("W",  "Tungsten",     6,  6, "d", "transition-metal",    2.36, (4, 6),       "[Xe] 4f14 5d4 6s2"),
    ("Re", "Rhenium",      7,  6, "d", "transition-metal",    1.90, (4, 7),       "[Xe] 4f14 5d5 6s2"),
    ("Os", "Osmium",       8,  6, "d", "transition-metal",    2.20, (3, 4, 6, 8), "[Xe] 4f14 5d6 6s2"),
    ("Ir", "Iridium",      9,  6, "d", "transition-metal",    2.20, (3, 4),       "[Xe] 4f14 5d7 6s2"),
    ("Pt", "Platinum",     10, 6, "d", "transition-metal",    2.28, (2, 4),       "[Xe] 4f14 5d9 6s1"),
    ("Au", "Gold",         11, 6, "d", "transition-metal",    2.54, (1, 3),       "[Xe] 4f14 5d10 6s1"),
    ("Hg", "Mercury",      12, 6, "d", "transition-metal",    2.00, (1, 2),       "[Xe] 4f14 5d10 6s2"),
    ("Tl", "Thallium",     13, 6, "p", "post-transition-metal",1.62,(1, 3),       "[Xe] 4f14 5d10 6s2 6p1"),
    ("Pb", "Lead",         14, 6, "p", "post-transition-metal",2.33,(2, 4),       "[Xe] 4f14 5d10 6s2 6p2"),
    ("Bi", "Bismuth",      15, 6, "p", "post-transition-metal",2.02,(3, 5),       "[Xe] 4f14 5d10 6s2 6p3"),
    ("Po", "Polonium",     16, 6, "p", "metalloid",           2.00, (-2, 2, 4),   "[Xe] 4f14 5d10 6s2 6p4"),
    ("At", "Astatine",     17, 6, "p", "halogen",             2.20, (-1, 1),      "[Xe] 4f14 5d10 6s2 6p5"),
    ("Rn", "Radon",        18, 6, "p", "noble-gas",           2.20, (0, 2),       "[Xe] 4f14 5d10 6s2 6p6"),
    # z=87..103 — period 7 s + actinides
    ("Fr", "Francium",     1,  7, "s", "alkali-metal",        0.70, (1,),         "[Rn] 7s1"),
    ("Ra", "Radium",       2,  7, "s", "alkaline-earth-metal",0.90, (2,),         "[Rn] 7s2"),
    ("Ac", "Actinium",     None, 7, "f", "actinide",          1.10, (3,),         "[Rn] 6d1 7s2"),
    ("Th", "Thorium",      None, 7, "f", "actinide",          1.30, (4,),         "[Rn] 6d2 7s2"),
    ("Pa", "Protactinium", None, 7, "f", "actinide",          1.50, (4, 5),       "[Rn] 5f2 6d1 7s2"),
    ("U",  "Uranium",      None, 7, "f", "actinide",          1.38, (3, 4, 5, 6), "[Rn] 5f3 6d1 7s2"),
    ("Np", "Neptunium",    None, 7, "f", "actinide",          1.36, (3, 4, 5, 6), "[Rn] 5f4 6d1 7s2"),
    ("Pu", "Plutonium",    None, 7, "f", "actinide",          1.28, (3, 4, 5, 6), "[Rn] 5f6 7s2"),
    ("Am", "Americium",    None, 7, "f", "actinide",          1.30, (3, 4, 5, 6), "[Rn] 5f7 7s2"),
    ("Cm", "Curium",       None, 7, "f", "actinide",          1.30, (3,),         "[Rn] 5f7 6d1 7s2"),
    ("Bk", "Berkelium",    None, 7, "f", "actinide",          1.30, (3, 4),       "[Rn] 5f9 7s2"),
    ("Cf", "Californium",  None, 7, "f", "actinide",          1.30, (3,),         "[Rn] 5f10 7s2"),
    ("Es", "Einsteinium",  None, 7, "f", "actinide",          1.30, (3,),         "[Rn] 5f11 7s2"),
    ("Fm", "Fermium",      None, 7, "f", "actinide",          1.30, (3,),         "[Rn] 5f12 7s2"),
    ("Md", "Mendelevium",  None, 7, "f", "actinide",          1.30, (2, 3),       "[Rn] 5f13 7s2"),
    ("No", "Nobelium",     None, 7, "f", "actinide",          1.30, (2, 3),       "[Rn] 5f14 7s2"),
    ("Lr", "Lawrencium",   3,  7, "d", "actinide",            1.30, (3,),         "[Rn] 5f14 7s2 7p1"),
    # z=104..118 — period 7 d + p
    ("Rf", "Rutherfordium",4,  7, "d", "transition-metal",    None, (4,),         "[Rn] 5f14 6d2 7s2"),
    ("Db", "Dubnium",      5,  7, "d", "transition-metal",    None, (5,),         "[Rn] 5f14 6d3 7s2"),
    ("Sg", "Seaborgium",   6,  7, "d", "transition-metal",    None, (6,),         "[Rn] 5f14 6d4 7s2"),
    ("Bh", "Bohrium",      7,  7, "d", "transition-metal",    None, (7,),         "[Rn] 5f14 6d5 7s2"),
    ("Hs", "Hassium",      8,  7, "d", "transition-metal",    None, (8,),         "[Rn] 5f14 6d6 7s2"),
    ("Mt", "Meitnerium",   9,  7, "d", "unknown",             None, (),           "[Rn] 5f14 6d7 7s2"),
    ("Ds", "Darmstadtium", 10, 7, "d", "unknown",             None, (),           "[Rn] 5f14 6d8 7s2"),
    ("Rg", "Roentgenium",  11, 7, "d", "unknown",             None, (),           "[Rn] 5f14 6d9 7s2"),
    ("Cn", "Copernicium",  12, 7, "d", "transition-metal",    None, (2,),         "[Rn] 5f14 6d10 7s2"),
    ("Nh", "Nihonium",     13, 7, "p", "unknown",             None, (1,),         "[Rn] 5f14 6d10 7s2 7p1"),
    ("Fl", "Flerovium",    14, 7, "p", "post-transition-metal",None,(2, 4),       "[Rn] 5f14 6d10 7s2 7p2"),
    ("Mc", "Moscovium",    15, 7, "p", "unknown",             None, (1, 3),       "[Rn] 5f14 6d10 7s2 7p3"),
    ("Lv", "Livermorium",  16, 7, "p", "unknown",             None, (2, 4),       "[Rn] 5f14 6d10 7s2 7p4"),
    ("Ts", "Tennessine",   17, 7, "p", "halogen",             None, (-1, 1, 5),   "[Rn] 5f14 6d10 7s2 7p5"),
    ("Og", "Oganesson",    18, 7, "p", "noble-gas",           None, (0,),         "[Rn] 5f14 6d10 7s2 7p6"),
]


def _build_elements() -> List[Element]:
    pt = GetPeriodicTable()
    out: List[Element] = []
    for z, (sym, name, group, period, block, category,
            en, oxs, cfg) in enumerate(_SEED, start=1):
        try:
            mass = pt.GetAtomicWeight(z)
        except Exception:  # noqa: BLE001
            mass = 0.0
        out.append(Element(
            symbol=sym, name=name, z=z,
            group=group, period=period, block=block,
            category=category, atomic_mass=mass,
            electronegativity=en,
            common_oxidation_states=tuple(oxs),
            electron_configuration=cfg,
        ))
    return out


ELEMENTS: List[Element] = _build_elements()
"""Full 1-118 table. Index 0 = Hydrogen."""


# ---------------------------------------------------------------------
# Lookup helpers

def list_elements() -> List[Dict[str, object]]:
    return [e.to_dict() for e in ELEMENTS]


def get_element(symbol_or_z) -> Optional[Element]:
    """Lookup by symbol (case-insensitive) or atomic number."""
    if isinstance(symbol_or_z, int) or (
            isinstance(symbol_or_z, str) and symbol_or_z.isdigit()):
        z = int(symbol_or_z)
        for e in ELEMENTS:
            if e.z == z:
                return e
        return None
    sym = str(symbol_or_z).strip()
    for e in ELEMENTS:
        if e.symbol.lower() == sym.lower() or \
                e.name.lower() == sym.lower():
            return e
    return None


def elements_by_category(category: str) -> List[Element]:
    cat = category.strip().lower()
    return [e for e in ELEMENTS if e.category == cat]


def categories() -> List[str]:
    """Ordered list of the category keys present in the table."""
    seen: List[str] = []
    for e in ELEMENTS:
        if e.category not in seen:
            seen.append(e.category)
    return seen
