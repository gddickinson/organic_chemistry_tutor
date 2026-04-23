"""Woodward-Hoffmann selection rules — Phase 14b.

The orbital-symmetry rules that govern pericyclic reactions. Three
families:

- **Cycloadditions** `[m+n]`: thermal suprafacial-suprafacial allowed
  iff ``(m + n) / 2`` is **odd** (photochemical flips the parity).
- **Electrocyclic** ring closures: thermal is **disrotatory** for
  (4n+2)-electron systems, **conrotatory** for 4n-electron systems
  (photochemical flips each).
- **Sigmatropic** `[i,j]` shifts: 6-electron (i+j = 6) thermal sup-sup
  allowed (the Cope / Claisen family).

Canonical teaching references: Fleming (*Molecular Orbitals and Organic
Chemical Reactions*, 2010) and Woodward-Hoffmann (*The Conservation of
Orbital Symmetry*, 1970).

The catalogue mirrors the shape of :mod:`orgchem.naming.rules` so the
LLM tutor can reason about pericyclic allowed-ness with the same
``list_wh_rules`` / ``get_wh_rule`` / ``check_wh_allowed`` pattern.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------

@dataclass(frozen=True)
class WHRule:
    """A single Woodward-Hoffmann entry."""
    id: str
    family: str                  # cycloaddition / electrocyclic / sigmatropic / general
    title: str
    description_md: str
    #: "thermal" or "photochemical" — which regime the rule applies to
    regime: str = "thermal"
    #: "allowed" / "forbidden" / "conrotatory" / "disrotatory" / "sup-sup" / "sup-ant"
    outcome: str = ""
    example: str = ""
    example_smiles: str = ""

    def to_dict(self) -> Dict[str, str]:
        return {
            "id": self.id, "family": self.family, "title": self.title,
            "description_md": self.description_md,
            "regime": self.regime, "outcome": self.outcome,
            "example": self.example, "example_smiles": self.example_smiles,
        }


# ---------------------------------------------------------------------

RULES: List[WHRule] = [
    # ==== Cycloadditions ===============================================
    WHRule(
        id="cyclo-4plus2-thermal",
        family="cycloaddition",
        title="[4+2] cycloaddition — thermal, sup-sup: allowed",
        description_md=(
            "Diene (4 π e⁻) + dienophile (2 π e⁻). `(4+2)/2 = 3` is odd "
            "→ thermally allowed as suprafacial-suprafacial. This is the "
            "**Diels-Alder reaction** — the most-used pericyclic step in "
            "synthesis. Endo adduct kinetically favoured via secondary "
            "orbital interactions."
        ),
        regime="thermal",
        outcome="allowed (suprafacial-suprafacial)",
        example="Diels-Alder: butadiene + ethene → cyclohexene",
        example_smiles="C=CC=C.C=C>>C1=CCCCC1",
    ),
    WHRule(
        id="cyclo-2plus2-thermal",
        family="cycloaddition",
        title="[2+2] cycloaddition — thermal, sup-sup: forbidden",
        description_md=(
            "Alkene + alkene. `(2+2)/2 = 2` is even → thermally forbidden "
            "as suprafacial-suprafacial. Thermal [2+2]s don't happen with "
            "normal alkenes. Photochemical [2+2] works (see `cyclo-2plus2-"
            "photochemical`) because UV flips one end's phase. Ketene + "
            "alkene is the classic *thermal* exception via an antarafacial "
            "pathway enabled by ketene's orthogonal π systems."
        ),
        regime="thermal",
        outcome="forbidden (suprafacial-suprafacial)",
        example="Ethene + ethene ⇏ cyclobutane (thermally)",
        example_smiles="C=C.C=C>>C1CCC1",
    ),
    WHRule(
        id="cyclo-2plus2-photochemical",
        family="cycloaddition",
        title="[2+2] cycloaddition — photochemical: allowed",
        description_md=(
            "Photochemical excitation promotes one π electron, inverting "
            "the effective symmetry. `(2+2)/2 = 2` even → photochemically "
            "allowed. Basis of photo-dimerisation of cinnamic acids "
            "(Liebermann 1877) and of the thymine-dimer DNA lesion from "
            "UV exposure."
        ),
        regime="photochemical",
        outcome="allowed (suprafacial-suprafacial)",
        example="Photodimerisation of 2 × cinnamic acid → truxillic/truxinic acids",
        example_smiles="",
    ),
    WHRule(
        id="cyclo-4plus4-thermal",
        family="cycloaddition",
        title="[4+4] cycloaddition — thermal: forbidden; photochemical: allowed",
        description_md=(
            "Diene + diene. `(4+4)/2 = 4` even → thermally forbidden, "
            "photochemically allowed. Naphthalene photodimerisation is "
            "an example."
        ),
        regime="thermal",
        outcome="forbidden (suprafacial-suprafacial)",
        example="Anthracene [4+4] photo-dimer",
        example_smiles="",
    ),
    WHRule(
        id="cyclo-8plus2-thermal",
        family="cycloaddition",
        title="[8+2] cycloaddition — thermal, sup-sup: allowed",
        description_md=(
            "Larger cycloadditions follow the same (m+n)/2-odd rule. "
            "`(8+2)/2 = 5` odd → thermally allowed. Used with "
            "heptafulvenes + dienophiles to make bicyclic 10-membered "
            "rings."
        ),
        regime="thermal",
        outcome="allowed (suprafacial-suprafacial)",
        example="Heptafulvene + dienophile",
        example_smiles="",
    ),
    WHRule(
        id="cyclo-1plus3-dipolar-thermal",
        family="cycloaddition",
        title="1,3-Dipolar cycloaddition — thermal, sup-sup: allowed",
        description_md=(
            "A 1,3-dipole (ozone, azide, diazoalkane, nitrile oxide, "
            "azomethine ylide) + dipolarophile. Counts as a [3+2] with "
            "4 π electrons on the dipole + 2 on the alkene = 6 total; "
            "(4+2)/2 = 3 odd → thermally allowed. Powers the "
            "copper-catalysed azide-alkyne \"click\" reaction."
        ),
        regime="thermal",
        outcome="allowed (suprafacial-suprafacial)",
        example="CuAAC azide-alkyne click",
        example_smiles="[N-]=[N+]=NCC.C#CC>>Cn1cc(C)nn1",
    ),

    # ==== Electrocyclic ================================================
    WHRule(
        id="electro-4pi-thermal",
        family="electrocyclic",
        title="4π electrocyclic — thermal: conrotatory",
        description_md=(
            "4 π electrons → thermal closure is **conrotatory** (both "
            "ends rotate the same sense). The HOMO has C₂-symmetric "
            "phases at the termini; conrotation aligns like-phase lobes "
            "for σ-bond formation. Example: thermal butadiene → "
            "cyclobutene (retro direction more common)."
        ),
        regime="thermal",
        outcome="conrotatory",
        example="Thermal butadiene ↔ cyclobutene",
        example_smiles="C=CC=C>>C1=CCC1",
    ),
    WHRule(
        id="electro-4pi-photochemical",
        family="electrocyclic",
        title="4π electrocyclic — photochemical: disrotatory",
        description_md=(
            "Photoexcitation promotes an electron to the LUMO, which has "
            "the **opposite** end-phase symmetry to the ground-state HOMO. "
            "So 4π photo closure is **disrotatory**. Important in "
            "vitamin D photo-synthesis from 7-dehydrocholesterol."
        ),
        regime="photochemical",
        outcome="disrotatory",
        example="Vitamin D pre-ring-opening of 7-dehydrocholesterol",
        example_smiles="",
    ),
    WHRule(
        id="electro-6pi-thermal",
        family="electrocyclic",
        title="6π electrocyclic — thermal: disrotatory",
        description_md=(
            "6 π electrons (4n+2, n=1) → thermal closure is "
            "**disrotatory**. Our seeded reaction `6π electrocyclic: "
            "hexatriene → cyclohexadiene` is the textbook case; "
            "vitamin-D biosynthesis also goes through a disrotatory 6π "
            "opening of a cyclohexadiene."
        ),
        regime="thermal",
        outcome="disrotatory",
        example="1,3,5-hexatriene → 1,3-cyclohexadiene",
        example_smiles="C=CC=CC=C>>C1=CC=CCC1",
    ),
    WHRule(
        id="electro-6pi-photochemical",
        family="electrocyclic",
        title="6π electrocyclic — photochemical: conrotatory",
        description_md=(
            "Photochemical 6π closure is **conrotatory**. Ring closure "
            "of Z-1,3,5-hexatriene gives cis-5,6-disubstituted-1,3-"
            "cyclohexadiene thermally (disrotatory) but the trans isomer "
            "photochemically (conrotatory)."
        ),
        regime="photochemical",
        outcome="conrotatory",
        example="Nazarov-like trienes, stereospecific photo-closures",
        example_smiles="",
    ),
    WHRule(
        id="electro-general",
        family="electrocyclic",
        title="Electrocyclic general rule",
        description_md=(
            "For 2n π electrons: thermal mode is **conrotatory** when "
            "2n = 4k, **disrotatory** when 2n = 4k+2. Photochemical "
            "flips each. Memorise the two 4π and 6π cases and extrapolate."
        ),
        regime="general",
        outcome="",
        example="",
        example_smiles="",
    ),

    # ==== Sigmatropic ==================================================
    WHRule(
        id="sigma-1-5-h-thermal",
        family="sigmatropic",
        title="[1,5]-H shift — thermal: allowed (suprafacial)",
        description_md=(
            "A [1,5]-hydrogen shift has 6 electrons in the TS (the H and "
            "the 4 π electrons of the diene). Thermally allowed as "
            "suprafacial on the π system (1,3-cyclopentadiene equilibrates "
            "its deuterium label at room temperature via this shift)."
        ),
        regime="thermal",
        outcome="allowed (suprafacial-suprafacial)",
        example="Cyclopentadiene H-scrambling",
        example_smiles="",
    ),
    WHRule(
        id="sigma-1-3-h-thermal",
        family="sigmatropic",
        title="[1,3]-H shift — thermal: forbidden (sup-sup)",
        description_md=(
            "A [1,3]-H shift has 4 electrons in the TS. Thermally "
            "forbidden as suprafacial-suprafacial. Can happen antarafacial "
            "but geometry makes it vanishingly rare, so [1,3]-H shifts are "
            "effectively thermally dead."
        ),
        regime="thermal",
        outcome="forbidden (suprafacial-suprafacial)",
        example="Allyl radical doesn't rearrange via H-migration",
        example_smiles="",
    ),
    WHRule(
        id="sigma-3-3-cope-claisen",
        family="sigmatropic",
        title="[3,3]-sigmatropic (Cope / Claisen) — thermal: allowed",
        description_md=(
            "6-electron TS, suprafacial on both ends → thermally allowed. "
            "**Cope** (1,5-hexadiene → 1,5-hexadiene, degenerate). "
            "**Claisen** (allyl vinyl ether → 4-pentenal). Low-barrier, "
            "widely used in synthesis."
        ),
        regime="thermal",
        outcome="allowed (suprafacial-suprafacial)",
        example="Claisen: allyl vinyl ether → 4-pentenal",
        example_smiles="C=CCOC=C>>C=CCCC=O",
    ),
    WHRule(
        id="sigma-2-3-wittig",
        family="sigmatropic",
        title="[2,3]-sigmatropic (Wittig rearrangement) — thermal: allowed",
        description_md=(
            "6 electrons in the TS via a 5-membered arrangement. The "
            "[2,3]-Wittig rearrangement of an allyl ether anion to a "
            "homoallyl alcohol is allowed thermally. Related: [2,3]-Meisenheimer "
            "and Stevens rearrangements."
        ),
        regime="thermal",
        outcome="allowed (suprafacial-suprafacial)",
        example="[2,3]-Wittig allyl ether → alcohol",
        example_smiles="",
    ),

    # ==== General master rule ==========================================
    WHRule(
        id="general-electron-count",
        family="general",
        title="Master rule: electron-count parity",
        description_md=(
            "For any pericyclic step, classify the TS as a sum of "
            "suprafacial (s) and antarafacial (a) components. Count: "
            "$N = \\Sigma \\,(4q + 2)_s + \\Sigma \\,(4r)_a$. "
            "Thermally allowed iff $N$ is odd; photochemically allowed iff "
            "$N$ is even. This single rule subsumes all the cycloaddition, "
            "electrocyclic, and sigmatropic rules as special cases."
        ),
        regime="general",
        outcome="",
        example="Any pericyclic reaction",
        example_smiles="",
    ),
    WHRule(
        id="general-photo-flip",
        family="general",
        title="Photochemical inversion of thermal rules",
        description_md=(
            "Every Woodward-Hoffmann statement has a photochemical "
            "counterpart with the outcome **flipped**. The mechanism: UV "
            "photons promote one electron to the LUMO, inverting the "
            "relevant phase-symmetry element. A useful check on any "
            "answer: write the thermal rule, then mentally flip it for "
            "UV conditions."
        ),
        regime="general",
        outcome="",
        example="",
        example_smiles="",
    ),
]


# ---------------------------------------------------------------------

def list_rules(family: str = "") -> List[Dict[str, str]]:
    """Return summary dicts for WH rules, optionally filtered by family."""
    if family:
        rows = [r for r in RULES if r.family == family]
    else:
        rows = list(RULES)
    return [
        {"id": r.id, "family": r.family, "title": r.title,
         "regime": r.regime, "outcome": r.outcome}
        for r in rows
    ]


def get_rule(rule_id: str) -> Dict[str, str]:
    """Return a full rule dict by id, or an error."""
    for r in RULES:
        if r.id == rule_id:
            return r.to_dict()
    return {"error": f"No WH rule with id {rule_id!r}"}


def rule_families() -> List[str]:
    """Distinct families in the catalogue, in first-seen order."""
    seen: List[str] = []
    for r in RULES:
        if r.family not in seen:
            seen.append(r.family)
    return seen


# ---------------------------------------------------------------------
# Allowed-ness lookup for the common teaching cases.

def check_allowed(kind: str, electron_count: int,
                  regime: str = "thermal") -> Dict[str, Any]:
    """Is a pericyclic step thermally / photochemically allowed?

    ``kind``: one of ``"cycloaddition"``, ``"electrocyclic"``, ``"sigmatropic"``.
    ``electron_count``: total number of electrons participating in the TS.

    Returns a dict with ``allowed`` (bool), ``geometry`` (string, e.g.
    ``"suprafacial-suprafacial"`` or ``"disrotatory"``), and ``reason``.
    """
    kind = kind.strip().lower()
    regime = regime.strip().lower()
    if regime not in ("thermal", "photochemical"):
        return {"error": f"regime must be 'thermal' or 'photochemical', got {regime!r}"}
    if electron_count < 2:
        return {"error": "electron_count must be ≥ 2"}

    if kind == "cycloaddition":
        odd = (electron_count // 2) % 2 == 1
        # Thermal: allowed iff electron_count / 2 is odd.
        thermal_allowed = odd
        allowed = thermal_allowed if regime == "thermal" else not thermal_allowed
        return {
            "allowed": allowed,
            "geometry": "suprafacial-suprafacial",
            "reason": f"(n/2 = {electron_count // 2}) "
                      f"{'odd' if odd else 'even'}; "
                      f"{regime} sup-sup "
                      f"{'allowed' if allowed else 'forbidden'}",
        }

    if kind == "electrocyclic":
        # 4n: thermal conrotatory, photo disrotatory
        # 4n+2: thermal disrotatory, photo conrotatory
        is_4n_plus_2 = (electron_count - 2) % 4 == 0
        if regime == "thermal":
            geom = "disrotatory" if is_4n_plus_2 else "conrotatory"
        else:
            geom = "conrotatory" if is_4n_plus_2 else "disrotatory"
        return {
            "allowed": True,
            "geometry": geom,
            "reason": f"{electron_count} π e⁻ "
                      f"({'4n+2' if is_4n_plus_2 else '4n'}); "
                      f"{regime} → {geom}",
        }

    if kind == "sigmatropic":
        # Treat as a cycloaddition-like electron count: thermal allowed
        # iff n/2 is odd (6-electron [3,3] allowed, 4-electron [1,3]
        # forbidden, etc.)
        odd = (electron_count // 2) % 2 == 1
        thermal_allowed = odd
        allowed = thermal_allowed if regime == "thermal" else not thermal_allowed
        return {
            "allowed": allowed,
            "geometry": "suprafacial-suprafacial",
            "reason": f"(n/2 = {electron_count // 2}) "
                      f"{'odd' if odd else 'even'}; "
                      f"{regime} sup-sup "
                      f"{'allowed' if allowed else 'forbidden'}",
        }

    return {"error": f"Unknown pericyclic kind {kind!r} "
                     "(use cycloaddition / electrocyclic / sigmatropic)"}
