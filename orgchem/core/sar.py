"""Structure-activity relationship (SAR) series — Phase 19a.

A **SAR series** is a parent scaffold + a set of variants, each
carrying one or more **activity** measurements (IC50, pKi, logP-shift,
etc.) and optional structural descriptors.

This module:

1. Defines the :class:`SARVariant` / :class:`SARSeries` dataclasses.
2. Ships two built-in teaching series:
   * **NSAIDs** — aspirin, ibuprofen, naproxen, acetaminophen.
   * **Statins** — lovastatin, simvastatin, atorvastatin.
   (A full library of benchmark SARs could be seeded later; two is
   enough to exercise the renderer and cross-check the tutor.)
3. Computes a table of descriptors (MW, logP, TPSA, QED, Lipinski
   pass, rotatable bonds) from SMILES so the matrix renderer has
   something to colour-code even without experimental activity.

Activity data for the seeded series comes from **published reviews**
(see each series' ``source`` field) — intended for teaching, not
regulatory use.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SARVariant:
    """One row in a SAR series: a structural variant + its activity value(s)."""
    name: str
    smiles: str
    #: Free-form notes about the R group / modification
    r_group_label: str = ""
    #: Activity columns: ``{metric_name: value}``.
    #: Example keys: ``"ic50_nM"``, ``"pKi"``, ``"COX-1 IC50"``, ``"LDL %"``.
    activity: Dict[str, float] = field(default_factory=dict)
    notes: str = ""


@dataclass
class SARSeries:
    id: str
    name: str
    target: str
    parent_scaffold_smiles: str
    source: str
    variants: List[SARVariant] = field(default_factory=list)
    #: The activity metric columns in preferred display order.
    activity_columns: List[str] = field(default_factory=list)

    def compute_descriptors(self) -> List[Dict[str, Any]]:
        """Return a row per variant with standard medchem descriptors."""
        from orgchem.core.druglike import drug_likeness_report
        rows: List[Dict[str, Any]] = []
        for v in self.variants:
            try:
                rep = drug_likeness_report(v.smiles)
                row = {
                    "name": v.name,
                    "r_group": v.r_group_label,
                    "smiles": v.smiles,
                    "mw": rep["lipinski"]["mw"],
                    "logp": rep["lipinski"]["logp"],
                    "tpsa": rep["veber"]["tpsa"],
                    "qed": rep["qed"],
                    "lipinski_violations": rep["lipinski"]["n_violations"],
                }
            except Exception as e:
                row = {"name": v.name, "smiles": v.smiles, "error": str(e)}
            row.update(v.activity)
            rows.append(row)
        return rows


# ---------------------------------------------------------------------
# Seeded series.
# Activity values are *approximate* literature-average numbers meant for
# teaching; drawn from the cited review for each series.

SAR_LIBRARY: List[SARSeries] = [
    SARSeries(
        id="nsaid-cox",
        name="NSAID anti-inflammatory series",
        target="Cyclooxygenase (COX-1 / COX-2)",
        parent_scaffold_smiles="OC(=O)c1ccccc1",   # benzoic-acid / salicylate core
        source="Vane & Botting 1995 *Inflamm. Res.* 44 Suppl: S1-S10",
        activity_columns=["cox1_ic50_uM", "cox2_ic50_uM",
                          "cox2_selectivity"],
        variants=[
            SARVariant(
                name="Aspirin",
                smiles="CC(=O)Oc1ccccc1C(=O)O",
                r_group_label="ortho-OAc salicylic acid",
                activity={"cox1_ic50_uM": 1.7, "cox2_ic50_uM": 280.0,
                          "cox2_selectivity": 0.006},
                notes="Irreversible covalent acetylation of Ser-530. "
                      "Non-selective; more cox1 at low dose.",
            ),
            SARVariant(
                name="Ibuprofen",
                smiles="CC(C)Cc1ccc(cc1)C(C)C(=O)O",
                r_group_label="2-phenylpropanoic acid; p-isobutyl",
                activity={"cox1_ic50_uM": 1.1, "cox2_ic50_uM": 1.8,
                          "cox2_selectivity": 0.61},
                notes="Racemic in commerce; only S enantiomer is the "
                      "COX inhibitor (R is slowly epimerised in vivo).",
            ),
            SARVariant(
                name="Naproxen",
                smiles="C[C@H](C(=O)O)c1ccc2cc(OC)ccc2c1",
                r_group_label="2-(6-methoxynaphthyl)propanoic acid",
                activity={"cox1_ic50_uM": 2.2, "cox2_ic50_uM": 3.6,
                          "cox2_selectivity": 0.61},
                notes="Sold as single S enantiomer.",
            ),
            SARVariant(
                name="Acetaminophen",
                smiles="CC(=O)Nc1ccc(O)cc1",
                r_group_label="N-acetyl-p-aminophenol (NAPAP)",
                activity={"cox1_ic50_uM": 105.0, "cox2_ic50_uM": 26.0,
                          "cox2_selectivity": 4.0},
                notes="Acts primarily on COX-3 / peroxide-poor COX-2 "
                      "in CNS. Not classed as an NSAID in strict "
                      "pharmacology.",
            ),
        ],
    ),
    SARSeries(
        id="statin-hmgcoa",
        name="Statin HMG-CoA reductase series",
        target="HMG-CoA reductase (LDL cholesterol lowering)",
        parent_scaffold_smiles="O=C1CC[C@H](O)C[C@@H]1O",  # mevalonate-like motif
        source="Istvan & Deisenhofer 2001 *Science* 292: 1160-1164",
        activity_columns=["ic50_nM", "daily_dose_mg", "ldl_pct_reduction"],
        variants=[
            SARVariant(
                name="Lovastatin",
                smiles="CC[C@@H](C)C(=O)O[C@@H]1C[C@@H](C)C=C2C=C[C@@H](C)[C@H](CC[C@@H]3C[C@H](O)CC(=O)O3)[C@@H]12",
                r_group_label="methylbutyryl side chain",
                activity={"ic50_nM": 11.0, "daily_dose_mg": 40.0,
                          "ldl_pct_reduction": 30.0},
                notes="First statin (1987). Natural product from "
                      "Aspergillus terreus.",
            ),
            SARVariant(
                name="Simvastatin",
                smiles="CCC(C)(C)C(=O)O[C@@H]1C[C@@H](C)C=C2C=C[C@@H](C)[C@H](CC[C@@H]3C[C@H](O)CC(=O)O3)[C@@H]12",
                r_group_label="dimethylbutyryl side chain",
                activity={"ic50_nM": 12.0, "daily_dose_mg": 20.0,
                          "ldl_pct_reduction": 38.0},
                notes="Semisynthetic lovastatin analogue. Higher "
                      "potency per milligram.",
            ),
            SARVariant(
                name="Atorvastatin",
                smiles="CC(C)c1c(C(=O)Nc2ccccc2)c(-c2ccccc2)c(-c2ccc(F)cc2)n1CC[C@@H](O)C[C@@H](O)CC(=O)O",
                r_group_label="pyrrole aryl-amide; synthetic",
                activity={"ic50_nM": 8.0, "daily_dose_mg": 20.0,
                          "ldl_pct_reduction": 50.0},
                notes="Fully synthetic. Lipitor — peak sales $12B/yr "
                      "(2007). 20-40 mg/day standard clinical dose.",
            ),
        ],
    ),
]


def get_series(series_id: str) -> Optional[SARSeries]:
    for s in SAR_LIBRARY:
        if s.id == series_id:
            return s
    return None


def list_series() -> List[Dict[str, Any]]:
    return [
        {"id": s.id, "name": s.name, "target": s.target,
         "n_variants": len(s.variants),
         "activity_columns": list(s.activity_columns)}
        for s in SAR_LIBRARY
    ]
