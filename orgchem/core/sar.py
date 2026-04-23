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

    # ---- Phase 31k content expansion (2026-04-23) ----------------
    SARSeries(
        id="beta-blockers",
        name="β-adrenergic blocker series",
        target="β₁ / β₂ adrenergic receptors",
        parent_scaffold_smiles="CC(C)NCC(O)COc1ccccc1",  # propranolol core
        source="Black 1988 *Br. J. Clin. Pharmacol.* 26:1-18 "
               "(Nobel 1988 lecture)",
        activity_columns=["beta1_pki", "beta2_pki",
                          "beta1_selectivity"],
        variants=[
            SARVariant(
                name="Propranolol",
                smiles="CC(C)NCC(O)COc1cccc2ccccc12",
                r_group_label="1-naphthyloxypropanolamine",
                activity={"beta1_pki": 8.2, "beta2_pki": 9.0,
                          "beta1_selectivity": 0.16},
                notes="First clinically successful β-blocker (Black, "
                      "1964). Non-selective — blocks β₁ AND β₂, so "
                      "can worsen asthma. Lipophilic (logP ~ 3), "
                      "CNS-penetrant.",
            ),
            SARVariant(
                name="Atenolol",
                smiles="CC(C)NCC(O)COc1ccc(CC(N)=O)cc1",
                r_group_label="p-acetamido aryl; hydrophilic",
                activity={"beta1_pki": 6.6, "beta2_pki": 5.5,
                          "beta1_selectivity": 13.0},
                notes="β₁-selective ('cardioselective'); safer in "
                      "asthma. Hydrophilic (logP ~ 0) → minimal "
                      "CNS side effects.",
            ),
            SARVariant(
                name="Metoprolol",
                smiles="COCCc1ccc(OCC(O)CNC(C)C)cc1",
                r_group_label="p-(2-methoxyethyl) aryl",
                activity={"beta1_pki": 7.3, "beta2_pki": 5.8,
                          "beta1_selectivity": 32.0},
                notes="β₁-selective. More lipophilic than atenolol "
                      "→ faster CNS entry + more sleep-disturbance "
                      "reports.",
            ),
            SARVariant(
                name="Bisoprolol",
                smiles="CC(C)NCC(O)COc1ccc(COCCC(C)C)cc1",
                r_group_label="p-(isopropoxymethyl) aryl",
                activity={"beta1_pki": 7.9, "beta2_pki": 5.7,
                          "beta1_selectivity": 170.0},
                notes="Most β₁-selective of this set. First-line "
                      "for chronic heart failure (MERIT-HF / CIBIS-II).",
            ),
            SARVariant(
                name="Carvedilol",
                smiles="COc1ccccc1OCCNCC(O)COc1cccc2[nH]c3ccccc3c12",
                r_group_label="carbazole-oxypropanolamine + "
                              "2-methoxyphenoxyethylamine",
                activity={"beta1_pki": 9.1, "beta2_pki": 9.0,
                          "beta1_selectivity": 1.3},
                notes="Non-selective β-blocker + α₁-antagonist + "
                      "antioxidant. Used in CHF — mortality benefit "
                      "in the COPERNICUS trial.",
            ),
        ],
    ),
    SARSeries(
        id="ace-inhibitors",
        name="ACE-inhibitor series",
        target="Angiotensin-converting enzyme (ACE)",
        parent_scaffold_smiles="O=C(N1CCCC1C(=O)O)C(C)CC",  # captopril-ish
        source="Cushman & Ondetti 1980 *Biochemistry* 19:177-184; "
               "Acharya 2003 *Nat. Rev. Drug Discov.* 2:891-902",
        activity_columns=["ic50_nM", "oral_bioavail_pct",
                          "t_half_h"],
        variants=[
            SARVariant(
                name="Captopril",
                smiles="CC(CS)C(=O)N1CCC[C@H]1C(=O)O",
                r_group_label="free thiol zinc-binder; proline",
                activity={"ic50_nM": 23.0, "oral_bioavail_pct": 75.0,
                          "t_half_h": 2.0},
                notes="First-in-class ACE-I (1981). Thiol binds the "
                      "catalytic Zn²⁺. Short half-life + sulfhydryl-"
                      "linked ADRs (rash, taste loss).",
            ),
            SARVariant(
                name="Enalaprilat",
                smiles="CCC(NC(Cc1ccccc1)C(=O)N1CCC[C@H]1C(=O)O)"
                       "C(=O)O",
                r_group_label="dicarboxylate zinc-binder; "
                              "Phe-Pro peptidomimetic",
                activity={"ic50_nM": 1.2, "oral_bioavail_pct": 10.0,
                          "t_half_h": 11.0},
                notes="Active metabolite of enalapril. Dicarboxylate "
                      "replaces thiol → longer half-life, no rash. "
                      "Prodrug (ethyl ester = enalapril) fixes oral "
                      "availability.",
            ),
            SARVariant(
                name="Lisinopril",
                smiles="NCCCC[C@H](N[C@@H](CCc1ccccc1)C(=O)O)C(=O)"
                       "N1CCC[C@H]1C(=O)O",
                r_group_label="lysyl side-chain (hydrophilic); "
                              "no prodrug needed",
                activity={"ic50_nM": 1.2, "oral_bioavail_pct": 25.0,
                          "t_half_h": 12.0},
                notes="Not a prodrug — active as-is. Polar / renally "
                      "cleared. Workhorse for hypertension + CHF.",
            ),
            SARVariant(
                name="Ramipril",
                smiles="CCC(C(=O)OCC)N[C@@H](C)C(=O)N1[C@H](C(=O)O)"
                       "C[C@H]2CCC[C@H]12",
                r_group_label="bicyclic 2-aza-bicyclic ring in "
                              "place of proline",
                activity={"ic50_nM": 7.0, "oral_bioavail_pct": 55.0,
                          "t_half_h": 17.0},
                notes="Ester prodrug → ramiprilat (active). Longer "
                      "half-life; HOPE trial showed mortality benefit "
                      "in high-CV-risk patients.",
            ),
            SARVariant(
                name="Benazepril",
                smiles="CCOC(=O)C(CCc1ccccc1)N[C@H](C)"
                       "C(=O)N1c2ccccc2CC[C@@H]1C(=O)O",
                r_group_label="benzazepine 7-membered-ring core",
                activity={"ic50_nM": 5.0, "oral_bioavail_pct": 37.0,
                          "t_half_h": 11.0},
                notes="Ester prodrug → benazeprilat. Fused-bicyclic "
                      "proline replacement tightens binding and "
                      "tunes pharmacokinetics.",
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
