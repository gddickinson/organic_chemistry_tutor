"""IUPAC nomenclature rule catalogue — Phase 12a.

A structured rule set for teaching organic nomenclature. Each rule has
a canonical id, a short title, a markdown explanation, a worked example
(SMILES + IUPAC name + common name where applicable), and a "common
pitfalls" field. The catalogue feeds:

- The (future) Phase 12b quiz engine ("name this structure"),
- The (future) `intermediate/04_nomenclature` cheat-sheet lesson,
- Agent actions `list_naming_rules` / `get_naming_rule` so an LLM tutor
  can pull exactly the right rule for a student question.

Rules are organised by substrate class. The list is explicit (no
dict-lookup magic) so the order in this file is the order students see.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(frozen=True)
class NamingRule:
    id: str
    category: str
    title: str
    description_md: str
    example_smiles: str = ""
    example_iupac: str = ""
    example_common: str = ""
    pitfalls: str = ""

    def to_dict(self) -> Dict[str, str]:
        return {
            "id": self.id, "category": self.category, "title": self.title,
            "description_md": self.description_md,
            "example_smiles": self.example_smiles,
            "example_iupac": self.example_iupac,
            "example_common": self.example_common,
            "pitfalls": self.pitfalls,
        }


# ---------------------------------------------------------------------

RULES: List[NamingRule] = [
    # ---- Alkanes --------------------------------------------------
    NamingRule(
        id="alkane-parent",
        category="alkanes",
        title="Pick the longest continuous carbon chain",
        description_md=(
            "The **parent** name is based on the longest continuous chain "
            "of carbons that passes through the molecule. Count atoms, not "
            "bonds; branches don't count as part of the chain. The parent "
            "suffix is **-ane** for a saturated hydrocarbon."
        ),
        example_smiles="CCCCC(C)C",
        example_iupac="2-methylhexane",
        pitfalls=(
            "Students often count the drawn-left-to-right chain. If the "
            "molecule has an angle, follow the bonds — the parent chain "
            "may wander up/down/left/right on the page."
        ),
    ),
    NamingRule(
        id="alkane-locants",
        category="alkanes",
        title="Number to give substituents the lowest locants",
        description_md=(
            "Number the parent chain from whichever end gives the **lowest "
            "set of locants** for the substituents (compare element-by-"
            "element, like decimals). Ties are broken by alphabetical order "
            "of the substituent name."
        ),
        example_smiles="CC(C)C(C)CCC",
        example_iupac="2,3-dimethylhexane",
        pitfalls=(
            "If you number from the wrong end you'll get e.g. '3,4-dimethyl' "
            "when '2,3-dimethyl' is correct — same molecule, wrong name."
        ),
    ),
    NamingRule(
        id="alkane-substituent-order",
        category="alkanes",
        title="Alphabetise substituent prefixes (ignoring multipliers)",
        description_md=(
            "Substituents are listed **alphabetically** in the final name, "
            "ignoring prefixes like *di-*, *tri-*, and *sec-* / *tert-*. "
            "The *n-* prefix (for straight chains) is **not** italicised in "
            "the alphabetisation either."
        ),
        example_smiles="CCC(CC)C(C)C",
        example_iupac="3-ethyl-2-methylpentane",
        pitfalls=(
            "'diethyl' is alphabetised under 'e', not 'd'. So 'ethyl' "
            "precedes 'methyl' regardless of multiplicity."
        ),
    ),
    NamingRule(
        id="cycloalkane",
        category="alkanes",
        title="Cycloalkanes use the **cyclo-** prefix",
        description_md=(
            "A ring of n carbons is **cyclo-***(parent)***ane**: "
            "cyclopropane (3), cyclobutane (4), cyclopentane (5), "
            "cyclohexane (6), etc. If the ring has substituents, number "
            "to give them the lowest locants — the ring atoms all count "
            "toward the parent."
        ),
        example_smiles="CC1CCCCC1",
        example_iupac="methylcyclohexane",
        pitfalls="",
    ),

    # ---- Alkenes / alkynes ---------------------------------------
    NamingRule(
        id="alkene-suffix",
        category="alkenes",
        title="Alkenes use the **-ene** suffix; alkynes use **-yne**",
        description_md=(
            "The suffix changes from *-ane* to **-ene** for a C=C double "
            "bond, or **-yne** for a C≡C triple bond. The locant goes "
            "immediately before the suffix — e.g. *but-2-ene*, not "
            "*2-butene* in IUPAC 2013 recommendations (older texts use the "
            "latter; both are common)."
        ),
        example_smiles="CCC=CC",
        example_iupac="pent-2-ene",
        pitfalls=(
            "Choose the parent chain that **contains** the double/triple "
            "bond, even if a longer alkyl chain exists without it."
        ),
    ),
    NamingRule(
        id="alkene-ez",
        category="alkenes",
        title="Double-bond stereo: E / Z",
        description_md=(
            "For a disubstituted alkene, apply the CIP priority rules on "
            "each side of the double bond. If the two high-priority "
            "substituents are on **opposite** sides the isomer is *(E)-* "
            "(*entgegen*, German 'opposite'); on the **same** side it's "
            "*(Z)-* (*zusammen*, 'together'). Older `cis-`/`trans-` usually "
            "agree but can disagree when priorities aren't obvious."
        ),
        example_smiles="C/C=C/C(=O)O",
        example_iupac="(2E)-but-2-enoic acid",
        example_common="trans-crotonic acid",
        pitfalls=(
            "(E) does not always mean the two carbons look symmetric. "
            "Always rank substituents via CIP."
        ),
    ),

    # ---- Alcohols ------------------------------------------------
    NamingRule(
        id="alcohol-suffix",
        category="alcohols",
        title="Alcohols use the **-ol** suffix",
        description_md=(
            "Replace the terminal *-e* of the parent with **-ol**. Give "
            "the OH the lowest possible locant (it outranks alkyl "
            "substituents but not multiple bonds)."
        ),
        example_smiles="CCCO",
        example_iupac="propan-1-ol",
        example_common="n-propanol",
        pitfalls=(
            "`propan-1-ol` (preferred IUPAC) is the same compound as "
            "`1-propanol` (older style). Either is usually accepted."
        ),
    ),
    NamingRule(
        id="alcohol-diol",
        category="alcohols",
        title="Two hydroxyls → **-diol**",
        description_md=(
            "Two OH groups give a **diol**. Retain the parent's final *e* "
            "(unlike single `-ol`): **ethane-1,2-diol**, not *ethan-diol*. "
            "Three OHs → triol, four → tetraol."
        ),
        example_smiles="OCCO",
        example_iupac="ethane-1,2-diol",
        example_common="ethylene glycol",
        pitfalls="Remember to keep the trailing 'e' before 'diol'.",
    ),

    # ---- Ethers --------------------------------------------------
    NamingRule(
        id="ether-common",
        category="ethers",
        title="Ethers: alkyl-alkyl ether (common) or **alkoxy** prefix (IUPAC)",
        description_md=(
            "Common names list the two alkyl groups alphabetically + "
            "'ether': *diethyl ether*, *methyl tert-butyl ether*. IUPAC "
            "names the smaller group as an **alkoxy-** substituent on the "
            "larger chain."
        ),
        example_smiles="CCOCC",
        example_iupac="ethoxyethane",
        example_common="diethyl ether",
        pitfalls="",
    ),

    # ---- Aldehydes / ketones ------------------------------------
    NamingRule(
        id="aldehyde-suffix",
        category="carbonyls",
        title="Aldehydes use the **-al** suffix; the C=O is C1",
        description_md=(
            "Replace the terminal *-e* with **-al**. The CHO carbon is "
            "always C1; no locant needed in the suffix. Aldehydes take "
            "priority over alcohols for the principal chain."
        ),
        example_smiles="CCC=O",
        example_iupac="propanal",
        example_common="propionaldehyde",
        pitfalls="",
    ),
    NamingRule(
        id="ketone-suffix",
        category="carbonyls",
        title="Ketones use **-one**",
        description_md=(
            "Replace *-e* with **-one** and give the carbonyl carbon the "
            "lowest possible locant. Ketones outrank alcohols and alkenes."
        ),
        example_smiles="CC(=O)CC",
        example_iupac="butan-2-one",
        example_common="methyl ethyl ketone (MEK)",
        pitfalls=(
            "`butan-2-one` and `2-butanone` are the same compound. The "
            "common name MEK is still widely used in lab speech."
        ),
    ),

    # ---- Carboxylic acids & derivatives -------------------------
    NamingRule(
        id="acid-suffix",
        category="acids",
        title="Carboxylic acids use **-oic acid** (or **-carboxylic acid**)",
        description_md=(
            "Replace *-e* with **-oic acid**; COOH is always C1. For a "
            "ring with a pendant COOH (e.g. cyclohexane-COOH), use "
            "**-carboxylic acid** appended to the ring parent."
        ),
        example_smiles="CCC(=O)O",
        example_iupac="propanoic acid",
        example_common="propionic acid",
        pitfalls="",
    ),
    NamingRule(
        id="ester-suffix",
        category="acids",
        title="Esters: 'alkyl **-oate**'",
        description_md=(
            "Name the alkyl group on oxygen first, then the acid parent "
            "with *-oic acid* replaced by **-oate**. Ethyl acetate = "
            "ethyl ethanoate."
        ),
        example_smiles="CCOC(C)=O",
        example_iupac="ethyl ethanoate",
        example_common="ethyl acetate",
        pitfalls="",
    ),
    NamingRule(
        id="amide-suffix",
        category="acids",
        title="Amides: **-amide**",
        description_md=(
            "Replace *-oic acid* with **-amide**. N-substituents are "
            "prefixed with *N-* (for each nitrogen). DMF = "
            "N,N-dimethylformamide."
        ),
        example_smiles="CC(=O)N",
        example_iupac="ethanamide",
        example_common="acetamide",
        pitfalls="",
    ),

    # ---- Amines --------------------------------------------------
    NamingRule(
        id="amine-suffix",
        category="amines",
        title="Amines: **-amine** (IUPAC) or alkyl-*amine* (common)",
        description_md=(
            "Replace *-e* with **-amine** and give the N the lowest "
            "locant. Common names juxtapose the alkyl groups ("
            "*methylamine*, *ethylamine*). Secondary and tertiary amines "
            "get N-substituent prefixes (*N-methylethanamine*)."
        ),
        example_smiles="CCN",
        example_iupac="ethan-1-amine",
        example_common="ethylamine",
        pitfalls="",
    ),

    # ---- Aromatics ----------------------------------------------
    NamingRule(
        id="aromatic-benzene-substituted",
        category="aromatics",
        title="Monosubstituted benzenes: many have retained common names",
        description_md=(
            "IUPAC allows retained names for very common substituted "
            "benzenes: **toluene** (methylbenzene), **phenol** "
            "(hydroxybenzene), **aniline** (aminobenzene), **anisole** "
            "(methoxybenzene), **styrene** (vinylbenzene), **benzaldehyde**, "
            "**benzoic acid**. For others, use 'X-benzene' with X as the "
            "substituent prefix."
        ),
        example_smiles="Cc1ccccc1",
        example_iupac="methylbenzene",
        example_common="toluene",
        pitfalls="",
    ),
    NamingRule(
        id="aromatic-disubst-locants",
        category="aromatics",
        title="Disubstituted benzenes: ortho / meta / para",
        description_md=(
            "The three positional isomers of a disubstituted benzene get "
            "the prefixes **o-** (1,2-), **m-** (1,3-), **p-** (1,4-). "
            "IUPAC now prefers the numerical locants (1,2-, 1,3-, 1,4-) "
            "but the o/m/p shorthand is still everywhere in the literature."
        ),
        example_smiles="Cc1ccc(C)cc1",
        example_iupac="1,4-dimethylbenzene",
        example_common="p-xylene",
        pitfalls="",
    ),

    # ---- Heterocycles -------------------------------------------
    NamingRule(
        id="heterocycle-retained",
        category="heterocycles",
        title="Heterocycles: retained names dominate",
        description_md=(
            "IUPAC retains the trivial names for common heterocycles: "
            "**pyridine**, **pyrrole**, **furan**, **thiophene**, "
            "**imidazole**, **pyrazole**, **oxazole**, **thiazole**, "
            "**pyrimidine**, **piperidine**, **morpholine**, **indole**, "
            "**quinoline**, **isoquinoline**, **purine**, **pyrazine**. "
            "Heteroatom numbering starts from the heteroatom and proceeds "
            "to give substituents the lowest locants."
        ),
        example_smiles="c1ccncc1",
        example_iupac="pyridine",
        example_common="azine",
        pitfalls="",
    ),
    NamingRule(
        id="heterocycle-hantzsch-widman",
        category="heterocycles",
        title="New heterocycles: Hantzsch-Widman nomenclature",
        description_md=(
            "For heterocycles without a retained name, combine "
            "**heteroatom 'a' prefix** (*oxa-* O, *aza-* N, *thia-* S, "
            "*phospha-* P) with a ring-size suffix: *-irine* (3, "
            "unsaturated), *-irane* (3, saturated), *-ete* (4 unsat), "
            "*-etane* (4 sat), etc. Harder to use; rarely needed for "
            "teaching beyond 5- and 6-rings."
        ),
        example_smiles="C1CN1",
        example_iupac="aziridine",
        pitfalls="",
    ),

    # ---- Stereodescriptors --------------------------------------
    NamingRule(
        id="stereo-rs",
        category="stereochemistry",
        title="R/S descriptors at stereocentres",
        description_md=(
            "CIP rules: rank the four substituents by atomic number with "
            "standard tie-breakers. View with the lowest-priority group "
            "pointing away; 1→2→3 clockwise is **R**, anticlockwise is "
            "**S**. The descriptor is prefixed to the name in parentheses "
            "with a locant: *(R)-2-butanol*."
        ),
        example_smiles="C[C@H](O)CC",
        example_iupac="(2R)-butan-2-ol",
        pitfalls=(
            "The descriptor depends on *priority*, not handedness of the "
            "drawn wedge. Always walk the CIP priorities."
        ),
    ),

    # ---- Multiple functional groups -----------------------------
    NamingRule(
        id="functional-group-priority",
        category="general",
        title="Functional-group priority (for picking the principal chain)",
        description_md=(
            "When multiple FGs are present, one is the **principal** "
            "(suffix) and others become **prefix** substituents. Priority "
            "order (highest → lowest): cations > carboxylic acid > "
            "anhydride > ester > acid halide > amide > nitrile > "
            "aldehyde > ketone > alcohol > amine > ether > alkene > "
            "alkyne > alkane."
        ),
        example_smiles="OC(=O)CCC(=O)C",
        example_iupac="5-oxohexanoic acid",
        pitfalls=(
            "Every group beneath the principal becomes a prefix (-oxo- for "
            "a ketone → -oxo-). Only one gets the suffix."
        ),
    ),
    NamingRule(
        id="locants-minimum",
        category="general",
        title="Numbering: minimise locants for the principal characteristic group first",
        description_md=(
            "When you number the parent chain, always give the **principal "
            "characteristic group** (the one that sets the suffix) the "
            "**lowest possible locant**. If there's still a choice, "
            "minimise the locants for the other substituents in the order "
            "they appear in the name."
        ),
        example_smiles="CC(=O)CCC(O)C",
        example_iupac="5-hydroxyhexan-2-one",
        pitfalls=(
            "A common error is to give the OH (prefix) locant 2, thereby "
            "assigning the C=O locant 5, when naming should minimise the "
            "C=O (principal) locant."
        ),
    ),
]


def list_rules(category: str = "") -> List[Dict[str, str]]:
    """Return summary dicts for rules, optionally filtered by ``category``."""
    if category:
        rows = [r for r in RULES if r.category == category]
    else:
        rows = list(RULES)
    return [
        {"id": r.id, "category": r.category, "title": r.title}
        for r in rows
    ]


def get_rule(rule_id: str) -> Dict[str, str]:
    """Return a full rule dict by id, or an error."""
    for r in RULES:
        if r.id == rule_id:
            return r.to_dict()
    return {"error": f"No naming rule with id {rule_id!r}"}


def rule_categories() -> List[str]:
    """Distinct ``category`` values in the catalogue, in first-seen order."""
    seen: List[str] = []
    for r in RULES:
        if r.category not in seen:
            seen.append(r.category)
    return seen
