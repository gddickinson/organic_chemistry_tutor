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

    # ---- Phase 31k round 96 — SSRIs -------------------------------
    SARSeries(
        id="ssri-sert",
        name="SSRI (serotonin-reuptake inhibitor) series",
        target="Serotonin transporter (SERT) vs "
               "norepinephrine (NET) / dopamine (DAT) transporters",
        parent_scaffold_smiles="c1ccccc1CCCN",  # arylalkyl-amine motif
        source="Owens, Morgan, Plott, Nemeroff 1997 *JPET* "
               "283:1305-1322; Sanchez 2004 *Basic Clin. "
               "Pharmacol. Toxicol.* 94:51-67",
        activity_columns=["sert_ki_nM", "net_ki_nM",
                          "sert_selectivity"],
        variants=[
            SARVariant(
                name="Fluoxetine",
                smiles="CNCCC(Oc1ccc(C(F)(F)F)cc1)c1ccccc1",
                r_group_label="p-(trifluoromethyl)phenyl ether; "
                              "N-methyl phenylpropylamine",
                activity={"sert_ki_nM": 0.9, "net_ki_nM": 240.0,
                          "sert_selectivity": 270.0},
                notes="Prozac — first commercial SSRI (1987, Lilly). "
                      "Racemate sold; long half-life (~2 days) and "
                      "active metabolite norfluoxetine (~7-15 days).",
            ),
            SARVariant(
                name="Sertraline",
                smiles="CN[C@H]1CC[C@@H](c2ccc(Cl)c(Cl)c2)c2ccccc21",
                r_group_label="3,4-dichlorophenyl; cis-(1S,4S) "
                              "tetrahydronaphthylamine",
                activity={"sert_ki_nM": 0.15, "net_ki_nM": 420.0,
                          "sert_selectivity": 2800.0},
                notes="Zoloft — most SERT-selective of the classic "
                      "five. Cis-(1S,4S) diastereomer only; the trans "
                      "and (1R,4R) isomers are ≥100× weaker.",
            ),
            SARVariant(
                name="Paroxetine",
                smiles="Fc1ccc([C@@H]2CCNC[C@H]2COc2ccc3OCOc3c2)cc1",
                r_group_label="3S,4R trans-disubstituted piperidine "
                              "+ p-fluorophenyl + methylenedioxyphenoxy",
                activity={"sert_ki_nM": 0.13, "net_ki_nM": 40.0,
                          "sert_selectivity": 310.0},
                notes="Paxil — sub-nanomolar SERT Ki but also the "
                      "most anticholinergic of the class (muscarinic "
                      "off-target). Short half-life → notorious "
                      "discontinuation syndrome.",
            ),
            SARVariant(
                name="Citalopram",
                smiles="CN(C)CCCC1(c2ccc(F)cc2)OCc2cc(C#N)ccc21",
                r_group_label="racemic 1,3-dihydroisobenzofuran; "
                              "p-fluorophenyl + aryl nitrile + "
                              "N,N-dimethylaminopropyl",
                activity={"sert_ki_nM": 1.1, "net_ki_nM": 4070.0,
                          "sert_selectivity": 3700.0},
                notes="Celexa — sold as racemate. The R-enantiomer "
                      "actively antagonises SSRI effect at allosteric "
                      "SERT site → motivation for the single-enantiomer "
                      "escitalopram successor.",
            ),
            SARVariant(
                name="Escitalopram",
                smiles="CN(C)CCC[C@@]1(c2ccc(F)cc2)OCc2cc(C#N)ccc21",
                r_group_label="(S)-(+)-citalopram single enantiomer",
                activity={"sert_ki_nM": 0.7, "net_ki_nM": 7841.0,
                          "sert_selectivity": 11200.0},
                notes="Lexapro — textbook example of chiral-switch "
                      "re-development. Removing the R-enantiomer "
                      "~3× boosts SERT selectivity versus NET and "
                      "reduces dose 50%.",
            ),
        ],
    ),

    # ---- Phase 31k round 100 — β-lactam antibiotics ---------------
    SARSeries(
        id="beta-lactams",
        name="β-lactam penicillin series",
        target="Bacterial D-Ala-D-Ala transpeptidase (PBP) — "
               "opposed by S. aureus β-lactamase",
        parent_scaffold_smiles="CC1(C)SC2CC(=O)N2C1C(=O)O",  # penam core
        source="Fleming 1929 *Br. J. Exp. Pathol.* 10:226; "
               "Abraham & Chain 1940 *Nature* 146:837; "
               "Rolinson 1998 *J. Antimicrob. Chemother.* 41:589",
        activity_columns=["mic_s_aureus_ug_ml",
                          "beta_lactamase_stability",
                          "oral_bioavail_pct"],
        variants=[
            SARVariant(
                name="Penicillin G",
                smiles="CC1(C)S[C@@H]2[C@H](NC(=O)Cc3ccccc3)"
                       "C(=O)N2[C@H]1C(=O)O",
                r_group_label="benzyl amide side chain",
                activity={"mic_s_aureus_ug_ml": 0.02,
                          "beta_lactamase_stability": 0.0,
                          "oral_bioavail_pct": 20.0},
                notes="Fleming's 1929 mould product, industrialised "
                      "Oxford 1941 (Florey + Chain, Nobel 1945). "
                      "Hydrolysed by gastric acid (→ low oral avail.) "
                      "AND by penicillinase — hence IV/IM only against "
                      "β-lactamase-positive S. aureus after 1948.",
            ),
            SARVariant(
                name="Ampicillin",
                smiles="CC1(C)S[C@@H]2[C@H](NC(=O)[C@H](N)c3ccccc3)"
                       "C(=O)N2[C@H]1C(=O)O",
                r_group_label="α-amino benzyl side chain",
                activity={"mic_s_aureus_ug_ml": 0.05,
                          "beta_lactamase_stability": 0.0,
                          "oral_bioavail_pct": 40.0},
                notes="Beecham 1961 — the α-amino protonates in acid "
                      "→ cation that survives stomach pH. "
                      "Broad-spectrum (Gram- coverage via porin "
                      "transit) but still β-lactamase-labile.",
            ),
            SARVariant(
                name="Amoxicillin",
                smiles="CC1(C)S[C@@H]2[C@H](NC(=O)[C@H](N)"
                       "c3ccc(O)cc3)C(=O)N2[C@H]1C(=O)O",
                r_group_label="α-amino p-hydroxybenzyl side chain",
                activity={"mic_s_aureus_ug_ml": 0.05,
                          "beta_lactamase_stability": 0.0,
                          "oral_bioavail_pct": 90.0},
                notes="Beecham 1972 — p-OH boosts oral absorption "
                      "from 40 → 90 % vs ampicillin. Still "
                      "β-lactamase-labile → usually paired with "
                      "clavulanic acid (Augmentin).",
            ),
            SARVariant(
                name="Methicillin",
                smiles="COc1cccc(OC)c1C(=O)N[C@H]1C(=O)N2"
                       "[C@@H](C(=O)O)C(C)(C)S[C@H]12",
                r_group_label="2,6-dimethoxybenzoyl side chain "
                              "(sterically shielded)",
                activity={"mic_s_aureus_ug_ml": 3.0,
                          "beta_lactamase_stability": 1.0,
                          "oral_bioavail_pct": 5.0},
                notes="Beecham 1959 — the flanking 2,6-di-OMe "
                      "blocks β-lactamase access to the C-N bond "
                      "→ first penicillinase-stable penicillin. "
                      "Intrinsically weaker (higher MIC), "
                      "acid-labile (IV only). Later selected for "
                      "MRSA resistance (~1960) which named the class.",
            ),
            SARVariant(
                name="Cloxacillin",
                smiles="Cc1onc(-c2ccccc2Cl)c1C(=O)N[C@H]1C(=O)N2"
                       "[C@@H](C(=O)O)C(C)(C)S[C@H]12",
                r_group_label="3-o-chlorophenyl-5-methyl-isoxazole-"
                              "4-carboxamide (shielded + acid-stable)",
                activity={"mic_s_aureus_ug_ml": 0.25,
                          "beta_lactamase_stability": 1.0,
                          "oral_bioavail_pct": 60.0},
                notes="Beecham 1962 — isoxazolyl steric bulk "
                      "blocks penicillinase, bulky enough to "
                      "survive gastric acid + good oral absorption. "
                      "Drug-of-choice pre-MRSA for staphylococcal "
                      "skin infections.",
            ),
        ],
    ),

    # ---- Phase 31k round 108 — PDE5 inhibitors --------------------
    SARSeries(
        id="pde5-inhibitors",
        name="PDE5 inhibitor series",
        target="cGMP-specific phosphodiesterase 5 (PDE5) — opposed "
               "by PDE6 retinal off-target",
        parent_scaffold_smiles="Cc1nn2c(nc(=O)[nH]c2=O)n1",  # pyrazolopyrimidinone
        source="Rotella 2002 *Nat. Rev. Drug Discov.* 1:674 "
               "(PDE5 structure-based SAR review)",
        activity_columns=["pde5_ic50_nM", "t_half_h",
                          "pde6_selectivity"],
        variants=[
            SARVariant(
                name="Sildenafil",
                smiles="CCCc1nn(C)c2c1nc([nH]c2=O)-c1cc("
                       "S(=O)(=O)N2CCN(C)CC2)ccc1OCC",
                r_group_label="pyrazolopyrimidinone + aryl "
                              "sulfonamide (4-methylpiperazine)",
                activity={"pde5_ic50_nM": 3.5, "t_half_h": 4.0,
                          "pde6_selectivity": 10.0},
                notes="Viagra (1998) — first-in-class (Pfizer). "
                      "Originally developed for angina. "
                      "Modest PDE6 selectivity → ~3 % of patients "
                      "report blue-tint visual disturbance.",
            ),
            SARVariant(
                name="Vardenafil",
                smiles="CCCc1nc(C)c2c(=O)[nH]c(-c3cc("
                       "S(=O)(=O)N4CCN(CC)CC4)ccc3OCC)nn12",
                r_group_label="imidazotriazinone (regioisomer of "
                              "sildenafil's pyrazolopyrimidinone) "
                              "+ N-ethyl piperazine",
                activity={"pde5_ic50_nM": 0.1, "t_half_h": 4.0,
                          "pde6_selectivity": 15.0},
                notes="Levitra (2003, Bayer) — the most potent "
                      "of the class. Ring regioisomerisation + "
                      "N-Et on piperazine doubles affinity. Same "
                      "~4 h half-life as sildenafil.",
            ),
            SARVariant(
                name="Tadalafil",
                smiles="O=C1N(C)CC(=O)N2[C@@H]1Cc1c([C@H]2c2ccc3"
                       "OCOc3c2)[nH]c2ccccc12",
                r_group_label="β-carboline-fused diketopiperazine "
                              "(completely different chemotype)",
                activity={"pde5_ic50_nM": 1.8, "t_half_h": 17.5,
                          "pde6_selectivity": 700.0},
                notes="Cialis (2003, Lilly/ICOS) — the 'weekend "
                      "pill'. 17.5-h half-life (vs 4 h for the "
                      "sildenafil family) lets single dose cover "
                      "Fri-Sun. High PDE6 selectivity → no visual "
                      "side-effects. Chemotype switch rather than "
                      "scaffold tweak.",
            ),
            SARVariant(
                name="Avanafil",
                smiles="COc1cc(CNc2ncnc(N3CCC[C@@H]3CO)c2"
                       "NC(=O)c2ncc(Cl)cn2)ccc1",
                r_group_label="pyrimidine-based third chemotype; "
                              "chloro-pyrimidine amide + prolinol",
                activity={"pde5_ic50_nM": 5.2, "t_half_h": 1.5,
                          "pde6_selectivity": 120.0},
                notes="Stendra (2012, Mitsubishi Tanabe) — fastest "
                      "onset (~15 min) due to 1.5-h half-life. "
                      "Trades potency + half-life for pharmaco-"
                      "kinetic speed. Third distinct chemotype in "
                      "the class.",
            ),
            SARVariant(
                name="Udenafil",
                smiles="CCCc1nc(C)c2c(=O)[nH]c(-c3cc("
                       "S(=O)(=O)CCCN(CC)C4CCCCC4)ccc3OCC)nn12",
                r_group_label="vardenafil core + sulfonyl-propyl-"
                              "(N-cyclohexyl, N-ethyl)amine "
                              "(replaces piperazine)",
                activity={"pde5_ic50_nM": 8.2, "t_half_h": 11.0,
                          "pde6_selectivity": 50.0},
                notes="Zydena (2005, Dong-A, S Korea approval). "
                      "Piperazine → acyclic tertiary amine tweak "
                      "on vardenafil scaffold gives ~11-h t½ with "
                      "moderate PDE6 selectivity. Regional / less "
                      "global market than the Pfizer / Lilly / "
                      "Bayer big three.",
            ),
        ],
    ),

    # ---- Phase 31k round 122 — benzodiazepines ---------------------
    SARSeries(
        id="benzodiazepines",
        name="Benzodiazepine series",
        target="GABA-A receptor (α1/α2/α3/α5 subtypes) — "
               "positive allosteric modulator site",
        parent_scaffold_smiles="O=C1CN=C(c2ccccc2)c2ccccc2N1",  # 1,4-BZD core
        source="Sternbach 1979 *J. Med. Chem.* 22:1 (Hoffmann-La "
               "Roche discovery review); Sigel & Ernst 2018 "
               "*Trends Pharmacol. Sci.* 39:659 (subtype "
               "selectivity update)",
        activity_columns=["gaba_a_ec50_nM", "t_half_h",
                          "onset_min"],
        variants=[
            SARVariant(
                name="Diazepam",
                smiles="CN1C(=O)CN=C(c2ccccc2)c2cc(Cl)ccc21",
                r_group_label="parent 1,4-benzodiazepine; 7-Cl, "
                              "N1-methyl, 2'-H phenyl",
                activity={"gaba_a_ec50_nM": 15.0, "t_half_h": 44.0,
                          "onset_min": 30.0},
                notes="Valium — Sternbach / La Roche 1963.  The "
                      "archetype of the class.  7-Cl optimises "
                      "potency; N1-methyl extends half-life (no "
                      "2-oxo removal before phase-I metabolism).  "
                      "Active metabolites (nordiazepam, oxazepam, "
                      "temazepam) extend the effective half-life "
                      "further — hence the very long t½.",
            ),
            SARVariant(
                name="Lorazepam",
                smiles="OC1N=C(c2ccccc2Cl)c2cc(Cl)ccc2NC1=O",
                r_group_label="3-OH diazepam with 2'-Cl phenyl; "
                              "N1-H (no methyl)",
                activity={"gaba_a_ec50_nM": 3.0, "t_half_h": 14.0,
                          "onset_min": 45.0},
                notes="Ativan.  3-Hydroxyl + 2'-Cl sharpen potency "
                      "~5× vs diazepam.  Crucially, the 3-OH is "
                      "glucuronidated directly (no active "
                      "metabolite), so the 14-h half-life is a "
                      "clean single-exponential — safer in "
                      "elderly / hepatic-impaired patients.",
            ),
            SARVariant(
                name="Alprazolam",
                smiles="Cc1nnc2n1-c1ccc(Cl)cc1C(c1ccccc1)=NC2",
                r_group_label="triazolo-fused benzodiazepine "
                              "(1,2,4-triazole replacing N1-methyl "
                              "+ 2-oxo)",
                activity={"gaba_a_ec50_nM": 2.5, "t_half_h": 11.0,
                          "onset_min": 60.0},
                notes="Xanax.  Triazole ring fusion in place of "
                      "diazepam's N1-CH₃ + 2-C=O is a chemotype "
                      "switch, not a substituent tweak — it "
                      "dramatically tightens the panic-disorder "
                      "efficacy profile.  Highest addictive / "
                      "withdrawal liability of the class because "
                      "of fast onset + moderate t½ + high potency.",
            ),
            SARVariant(
                name="Clonazepam",
                smiles="O=C1CN=C(c2ccccc2Cl)c2cc([N+](=O)[O-])ccc2N1",
                r_group_label="7-NO₂ in place of 7-Cl; 2'-Cl "
                              "phenyl; N1-H",
                activity={"gaba_a_ec50_nM": 1.2, "t_half_h": 35.0,
                          "onset_min": 60.0},
                notes="Klonopin.  7-NO₂ is the only common "
                      "deviation from the canonical 7-Cl — shifts "
                      "the receptor-subtype preference + prolongs "
                      "half-life.  Gold-standard anticonvulsant "
                      "in the class; the 2'-Cl boosts potency ~10× "
                      "over 7-Cl-only analogues.",
            ),
            SARVariant(
                name="Midazolam",
                smiles="Cc1ncc2CN=C(c3ccccc3F)c3cc(Cl)ccc3-n12",
                r_group_label="imidazo[1,2-a]-fused benzodiazepine; "
                              "2'-F phenyl",
                activity={"gaba_a_ec50_nM": 4.0, "t_half_h": 2.5,
                          "onset_min": 5.0},
                notes="Versed.  Imidazo-ring fusion gives pH-"
                      "dependent solubility (closed-ring at pH 4, "
                      "open-ring amino-ketone at physiological pH) "
                      "— unique among BZDs: it's water-soluble in "
                      "its ampoule, lipid-soluble in blood.  The "
                      "very short 2.5-h half-life + 5-min onset "
                      "make it the anaesthesiologist's preferred "
                      "IV induction agent.",
            ),
        ],
    ),

    # ---- Phase 31k round 133 — fluoroquinolones --------------------
    SARSeries(
        id="fluoroquinolones",
        name="Fluoroquinolone antibiotic series",
        target="Bacterial DNA gyrase + topoisomerase IV",
        # Quinolone-3-carboxylic-acid 4-oxo core (no F).
        parent_scaffold_smiles="O=c1cc2ccccc2[nH]c1C(=O)O",
        source="Andriole 2005 *Clin. Infect. Dis.* 41 Suppl 2:S113 + "
               "Bryskier 2005 *Antimicrobial Agents* (Quinolones ch.) "
               "+ Pham et al. 2019 *Front. Microbiol.* 10:2245",
        activity_columns=["mic_e_coli_ugml", "mic_s_aureus_ugml",
                          "mic_p_aeruginosa_ugml"],
        variants=[
            SARVariant(
                name="Nalidixic acid",
                smiles="CCN1C=C(C(=O)O)C(=O)c2cc(C)cnc12",
                r_group_label="1st-gen 1,8-naphthyridone (no C-6 F, "
                              "no piperazine); N-1 ethyl, C-7 methyl",
                activity={"mic_e_coli_ugml": 8.0,
                          "mic_s_aureus_ugml": 32.0,
                          "mic_p_aeruginosa_ugml": 128.0},
                notes="Lesher 1962 — the founding compound of the "
                      "class.  Naphthyridone (8-aza analogue of "
                      "quinolone), no fluorine, no piperazine.  "
                      "Narrow spectrum (Gram-negative urinary tract "
                      "only) and oral-only — but the proof of "
                      "concept that DNA-gyrase inhibition is a "
                      "viable antibacterial strategy.  Every later "
                      "-floxacin is an SAR optimisation away from "
                      "this scaffold.",
            ),
            SARVariant(
                name="Norfloxacin",
                smiles="CCN1C=C(C(=O)O)C(=O)c2cc(F)c(N3CCNCC3)cc12",
                r_group_label="2nd-gen quinolone with C-6 fluorine + "
                              "C-7 piperazinyl; N-1 ethyl",
                activity={"mic_e_coli_ugml": 0.06,
                          "mic_s_aureus_ugml": 1.0,
                          "mic_p_aeruginosa_ugml": 0.5},
                notes="Koga / Kyorin 1980 — the first true "
                      "*fluoroquinolone*.  Two SAR moves vs nalidixic "
                      "acid: (a) C-6 F adds a hydrophobic + dipole "
                      "anchor in the gyrase pocket → ~100× MIC drop "
                      "on E. coli; (b) C-7 piperazine widens activity "
                      "to Pseudomonas + Gram-positive cocci.  Still "
                      "limited to systemic UTI use; the next move "
                      "(N-1 substituent) was needed for the broad "
                      "tissue penetration of ciprofloxacin.",
            ),
            SARVariant(
                name="Ciprofloxacin",
                smiles="O=C(O)C1=CN(C2CC2)c2cc(N3CCNCC3)c(F)cc2C1=O",
                r_group_label="N-1 cyclopropyl in place of N-1 ethyl; "
                              "C-6 F + C-7 piperazinyl preserved",
                activity={"mic_e_coli_ugml": 0.015,
                          "mic_s_aureus_ugml": 0.5,
                          "mic_p_aeruginosa_ugml": 0.25},
                notes="Wise / Bayer 1983 — the workhorse of the "
                      "class.  Single SAR change (N-1 ethyl → "
                      "cyclopropyl) drops MIC ~4× across the board, "
                      "delivers oral + IV bioavailability, and gives "
                      "the best Gram-negative + anti-Pseudomonas "
                      "potency in the entire class.  Used "
                      "everywhere from anthrax post-exposure "
                      "prophylaxis to hospital pneumonia.  The "
                      "downside is rising resistance + the "
                      "tendinopathy / aortic-aneurysm class warning "
                      "that arrived with the 2010s safety reviews.",
            ),
            SARVariant(
                name="Levofloxacin",
                smiles="C[C@H]1COc2c(N3CCN(C)CC3)c(F)cc3C(=O)C(C(=O)O)"
                       "=CN1c23",
                r_group_label="3rd-gen S-isomer of ofloxacin; oxazine "
                              "ring fused at N-1/C-8 + 4'-methyl-"
                              "piperazine at C-7",
                activity={"mic_e_coli_ugml": 0.03,
                          "mic_s_aureus_ugml": 0.25,
                          "mic_p_aeruginosa_ugml": 0.5},
                notes="Hayakawa / Daiichi 1985 (ofloxacin), 1996 "
                      "(levo).  The S enantiomer of ofloxacin — the "
                      "racemate carried twice the dose for the same "
                      "effect, so the chiral switch was a 2× "
                      "potency-per-mg win.  Oxazine fusion locks the "
                      "N-1 substituent into a rigid bicyclic + the "
                      "C-7 N-methylpiperazine boosts Gram-positive "
                      "activity (S. pneumoniae especially).  Tissue "
                      "penetration to lung + prostate makes it the "
                      "go-to 'respiratory fluoroquinolone' — the "
                      "label tag that drove its 2000s adoption.",
            ),
            SARVariant(
                name="Moxifloxacin",
                smiles="COc1c(N2C[C@@H]3CCCN[C@@H]3C2)c(F)cc2C(=O)C(=CN"
                       "(C3CC3)c12)C(=O)O",
                r_group_label="4th-gen with C-8 methoxy + bicyclic "
                              "diazabicyclooctane at C-7; N-1 "
                              "cyclopropyl",
                activity={"mic_e_coli_ugml": 0.06,
                          "mic_s_aureus_ugml": 0.06,
                          "mic_p_aeruginosa_ugml": 4.0},
                notes="Petersen / Bayer 1999.  Two SAR moves on the "
                      "ciprofloxacin scaffold: (a) C-8 methoxy "
                      "(photo-stability + reduced phototoxicity); "
                      "(b) C-7 piperazine → bicyclic "
                      "diazabicyclo[2.2.1]octane (better "
                      "Gram-positive + anaerobe activity).  The "
                      "trade-off is dramatic: best-in-class "
                      "S. aureus + S. pneumoniae + anaerobe "
                      "coverage, BUT loses anti-Pseudomonas activity "
                      "(MIC jumps from 0.25 to 4 µg/mL — ~16×).  "
                      "Pulled OTC label revisions (2018 EMA) for QT "
                      "prolongation + hepatotoxicity make it a "
                      "second-line choice today.",
            ),
        ],
    ),

    # ---- Phase 31k round 163 — DPP-4 inhibitor (gliptin) series ---
    SARSeries(
        id="dpp4-inhibitors",
        name="DPP-4 inhibitor (gliptin) series — incretin-"
             "pathway antidiabetics",
        target="Dipeptidyl peptidase-4 (DPP-4 / CD26)",
        # No single shared scaffold — vildagliptin +
        # saxagliptin share a cyanopyrrolidine + adamantyl
        # template, but sitagliptin / linagliptin /
        # alogliptin diverge.  Use sitagliptin (first to
        # market + best-selling) as the parent.
        parent_scaffold_smiles="N[C@@H](CC(=O)N1CCn2c(C(F)(F)F)"
                               "nnc2C1)Cc1cc(F)c(F)cc1F",
        source="Deacon 2019 *Front. Endocrinol.* 10: 80 + "
               "Drucker 2007 *Diabetes Care* 30: 1335-1343 "
               "(canonical DPP-4-inhibitor SAR + clinical "
               "comparison reviews)",
        activity_columns=["dpp4_ic50_nM",
                          "covalent_reversible",
                          "renal_clearance_pct",
                          "half_life_h",
                          "logp"],
        variants=[
            SARVariant(
                name="Sitagliptin (Januvia)",
                smiles="N[C@@H](CC(=O)N1CCn2c(C(F)(F)F)nnc2C1)"
                       "Cc1cc(F)c(F)cc1F",
                r_group_label="(R)-β-amino-γ-(2,4,5-tri"
                              "fluorophenyl)-butanoyl + "
                              "trifluoromethyl-triazolopiperazine",
                activity={"dpp4_ic50_nM": 18.0,
                          "covalent_reversible": 0.0,
                          "renal_clearance_pct": 80.0,
                          "half_life_h": 12.0,
                          "logp": 2.0},
                notes="Merck 2006 — **first DPP-4 inhibitor "
                      "to market** + still best-selling "
                      "gliptin worldwide.  Non-covalent "
                      "competitive inhibitor — binds the "
                      "active site via the β-amino group "
                      "anchoring to Glu-205 / Glu-206 + "
                      "Tyr-662 + the trifluoromethyl-"
                      "triazolopiperazine occupying the S2 "
                      "pocket.  ~ 80% renal cleared unchanged "
                      "→ requires dose reduction in CKD.  "
                      "Once-daily dosing.  TECOS 2015 "
                      "established cardiovascular safety.",
            ),
            SARVariant(
                name="Saxagliptin (Onglyza)",
                smiles="O=C(N1C[C@@H]2C[C@@H]2[C@H]1C#N)"
                       "[C@@H](N)C12CC3CC(C1)CC(O)(C3)C2",
                r_group_label="**Cyanopyrrolidine warhead** + "
                              "(S)-3-hydroxyadamantyl + "
                              "α-amino-acyl spacer — "
                              "**covalent reversible** with "
                              "the catalytic Ser-630",
                activity={"dpp4_ic50_nM": 1.3,
                          "covalent_reversible": 1.0,
                          "renal_clearance_pct": 75.0,
                          "half_life_h": 2.5,
                          "logp": 1.0},
                notes="BMS / AstraZeneca 2009 — **covalent "
                      "reversible inhibitor** — the nitrile "
                      "(C#N) of the cyanopyrrolidine warhead "
                      "is attacked by Ser-630 of DPP-4 to form "
                      "a slowly-reversible imidate adduct.  "
                      "Result: very low IC50 (1.3 nM) but "
                      "short plasma half-life (~ 2.5 h) — the "
                      "covalent mechanism gives sustained "
                      "tissue inhibition despite rapid plasma "
                      "clearance.  Active metabolite "
                      "5-hydroxysaxagliptin contributes ~ 50% "
                      "of activity.  SAVOR-TIMI 53 2013 "
                      "raised heart-failure-hospitalisation "
                      "signal — required FDA label update.",
            ),
            SARVariant(
                name="Linagliptin (Tradjenta)",
                smiles="CC#CCn1c(N2CCC[C@@H](N)C2)nc2c1c(=O)"
                       "n(Cc1nc3ccccc3c(C)n1)c(=O)n2C",
                r_group_label="**Xanthine scaffold** — total "
                              "chemotype switch from the other "
                              "gliptins; 8-(3R-aminopiperidin-1-"
                              "yl) + 7-but-2-yn-1-yl + 3-methyl "
                              "+ 1-(4-methylquinazolinyl-methyl)",
                activity={"dpp4_ic50_nM": 1.0,
                          "covalent_reversible": 0.0,
                          "renal_clearance_pct": 5.0,
                          "half_life_h": 12.0,
                          "logp": 1.2},
                notes="Boehringer Ingelheim / Lilly 2011 — "
                      "**unique among DPP-4 inhibitors: "
                      "primarily fecal clearance** (~ 95% via "
                      "the bile, only 5% renal), so **NO "
                      "dose adjustment in CKD or ESRD** — "
                      "the only gliptin safe in haemodialysis "
                      "patients without dose modification.  "
                      "Xanthine scaffold (purine-2,6-dione "
                      "with the C8 piperidine + N1 quinazoline "
                      "+ N3 methyl + N7 but-2-ynyl) — "
                      "completely different chemotype from "
                      "the other gliptins, evolved from "
                      "natural-product xanthine pharmacology "
                      "(caffeine / theophylline).  CARMELINA "
                      "2018 trial established cardiovascular "
                      "safety + renal-protection neutrality.",
            ),
            SARVariant(
                name="Alogliptin (Nesina)",
                smiles="N[C@@H]1CCCN(c2cc(=O)n(Cc3cccc(C#N)c3)"
                       "c(=O)n2C)C1",
                r_group_label="Pyrimidine-2,4-dione + 3-"
                              "cyanobenzyl + (R)-3-amino-"
                              "piperidinyl — uracil-based "
                              "scaffold",
                activity={"dpp4_ic50_nM": 6.9,
                          "covalent_reversible": 0.0,
                          "renal_clearance_pct": 76.0,
                          "half_life_h": 21.0,
                          "logp": 0.4},
                notes="Takeda 2013 — uracil-based scaffold "
                      "with cyanobenzyl + 3-aminopiperidinyl "
                      "substituents.  Once-daily; renal "
                      "clearance ~ 76% so requires dose "
                      "reduction in CKD.  EXAMINE 2013 in "
                      "post-ACS patients showed "
                      "non-inferiority to placebo for "
                      "cardiovascular outcomes — though small "
                      "heart-failure signal also surfaced "
                      "(less robust than saxagliptin's).  "
                      "Most lipophilicity-balanced gliptin "
                      "(logP 0.4 — by far the lowest, "
                      "minimising off-target binding).",
            ),
            SARVariant(
                name="Vildagliptin (Galvus)",
                smiles="O=C(N1CCC[C@H]1C#N)CNC12CC3CC(C1)CC"
                       "(O)(C3)C2",
                r_group_label="**Cyanopyrrolidine warhead** + "
                              "3-hydroxyadamantyl-amino-acyl "
                              "spacer — **same covalent "
                              "mechanism as saxagliptin** via "
                              "different scaffold connection",
                activity={"dpp4_ic50_nM": 3.5,
                          "covalent_reversible": 1.0,
                          "renal_clearance_pct": 22.0,
                          "half_life_h": 2.0,
                          "logp": 1.2},
                notes="Novartis 2007 — **EU-approved but "
                      "NOT FDA-approved** (heart-failure "
                      "concerns + transient liver-enzyme "
                      "elevations stalled the US filing).  "
                      "Same **covalent reversible** mechanism "
                      "as saxagliptin via the cyanopyrrolidine "
                      "warhead reacting with Ser-630, but "
                      "connected to the 3-hydroxyadamantyl "
                      "anchor through a glycyl spacer instead "
                      "of an α-amino-acyl spacer.  Twice-daily "
                      "dosing because of short plasma "
                      "half-life (~ 2 h) — same compromise as "
                      "saxagliptin.  ~ 22% renal cleared, so "
                      "less dose reduction needed than "
                      "sitagliptin / saxagliptin / "
                      "alogliptin.",
            ),
        ],
    ),

    # ---- Phase 31k round 162 — direct-oral-anticoagulant (DOAC) ---
    SARSeries(
        id="doacs",
        name="Direct-oral-anticoagulant (DOAC) series — Xa "
             "vs IIa inhibitors",
        target="Coagulation cascade — factor Xa (apixaban, "
               "rivaroxaban, edoxaban) and factor IIa "
               "thrombin (dabigatran)",
        # No single shared scaffold — that's the point.  Use
        # apixaban (current best-in-class) as the parent.
        parent_scaffold_smiles="COc1ccc(-n2nc(C(N)=O)c3c2C(=O)"
                               "N(c2ccc(N4CCCCC4=O)cc2)CC3)cc1",
        source="Garcia + Crowther 2014 *N. Engl. J. Med.* "
               "370: 1281-1287 + Yeh + Eikelboom 2014 *Eur. "
               "Heart J.* 35: 2076-2087 (canonical DOAC "
               "comparison reviews)",
        activity_columns=["factor_xa",
                          "target_ki_nM",
                          "oral_bioavailability_pct",
                          "half_life_h",
                          "logp"],
        variants=[
            SARVariant(
                name="Apixaban (Eliquis)",
                smiles="COc1ccc(-n2nc(C(N)=O)c3c2C(=O)N"
                       "(c2ccc(N4CCCCC4=O)cc2)CC3)cc1",
                r_group_label="Pyrazole-3-carboxamide + "
                              "fused-bicyclic dihydropyridazinone "
                              "+ N-aryl-piperidinone tail",
                activity={"factor_xa": 1.0,
                          "target_ki_nM": 0.08,
                          "oral_bioavailability_pct": 50.0,
                          "half_life_h": 12.0,
                          "logp": 2.7},
                notes="BMS / Pfizer 2012 — direct factor-Xa "
                      "inhibitor; **most-potent DOAC on Xa "
                      "(Ki 0.08 nM)** + reversible binding to "
                      "the active site.  CYP3A4 + P-gp "
                      "substrate but only 25% renal cleared "
                      "(safest DOAC in CKD).  Twice-daily "
                      "dosing; ARISTOTLE trial 2011 showed "
                      "superiority to warfarin on stroke "
                      "prevention + reduced major bleeding "
                      "in atrial fibrillation.  Andexanet "
                      "alfa is the specific Xa-inhibitor "
                      "reversal agent.",
            ),
            SARVariant(
                name="Rivaroxaban (Xarelto)",
                smiles="O=C(NC[C@H]1CN(c2ccc(N3CCOCC3=O)cc2)"
                       "C(=O)O1)c1ccc(Cl)s1",
                r_group_label="2-Chlorothiophene + (S)-"
                              "oxazolidinone + N-aryl-"
                              "morpholinone — the chiral "
                              "oxazolidinone is the **anti-"
                              "infective scaffold reused** for "
                              "anticoagulation",
                activity={"factor_xa": 1.0,
                          "target_ki_nM": 0.4,
                          "oral_bioavailability_pct": 80.0,
                          "half_life_h": 9.0,
                          "logp": 2.5},
                notes="Bayer 2008 — first DOAC to market.  "
                      "Direct factor-Xa inhibitor.  "
                      "Once-daily dosing (15-20 mg) — the "
                      "convenience advantage that drove rapid "
                      "uptake.  Bioavailability is "
                      "**food-dependent** (66% fasting → "
                      "100% with food at 20 mg dose) so must "
                      "be taken with meals.  CYP3A4 + P-gp "
                      "substrate; 33% renal cleared.  ROCKET-"
                      "AF 2011 showed non-inferiority to "
                      "warfarin in atrial fibrillation; "
                      "EINSTEIN-DVT 2010 in venous "
                      "thromboembolism.",
            ),
            SARVariant(
                name="Edoxaban (Lixiana / Savaysa)",
                smiles="CN(C(=O)c1csc(C)n1)C(=O)N[C@@H]1CC"
                       "[C@H](NC(=O)c2cc(Cl)cnc2N)CC1",
                r_group_label="Thiazole-N-methyl-carboxamide "
                              "+ 5-chloro-2-aminonicotinamide "
                              "+ trans-cyclohexyl-1,4-diamine "
                              "spacer",
                activity={"factor_xa": 1.0,
                          "target_ki_nM": 0.6,
                          "oral_bioavailability_pct": 62.0,
                          "half_life_h": 10.0,
                          "logp": 2.6},
                notes="Daiichi Sankyo 2011 — third-to-market "
                      "factor-Xa inhibitor.  Once-daily "
                      "dosing.  Critical PK feature: "
                      "**bioavailability decreases at high "
                      "renal clearance** — paradoxically "
                      "**less effective in patients with "
                      "preserved renal function** (CrCl > "
                      "95 mL/min) than in mild-to-moderate "
                      "CKD.  Boxed warning: NOT recommended "
                      "for atrial fibrillation when CrCl > 95 "
                      "mL/min.  ENGAGE AF-TIMI 48 2013 "
                      "showed non-inferiority to warfarin.",
            ),
            SARVariant(
                name="Dabigatran (Pradaxa) — active form",
                smiles="CN1C(CNc2ccc(C(=N)N)cc2)=Nc2cc"
                       "(C(=O)N(CCC(=O)O)c3ccccn3)ccc21",
                r_group_label="Benzimidazole + amidine + "
                              "pyridinyl-N-acyl-β-alanine — "
                              "**only seeded factor-IIa "
                              "(thrombin) inhibitor**",
                activity={"factor_xa": 0.0,
                          "target_ki_nM": 4.5,
                          "oral_bioavailability_pct": 6.5,
                          "half_life_h": 14.0,
                          "logp": 3.0},
                notes="Boehringer Ingelheim 2010 — direct "
                      "factor-IIa (thrombin) inhibitor.  "
                      "**Only DOAC that targets thrombin** "
                      "(IIa) instead of factor Xa — the "
                      "amidine + carboxylate zwitterion at "
                      "physiological pH is the IIa-binding "
                      "pharmacophore.  Same zwitterion that "
                      "gives potent IIa binding **destroys "
                      "oral bioavailability** (only 6.5% as "
                      "free dabigatran) — the molecule is too "
                      "polar to cross intestinal membranes.  "
                      "Solved by the **dabigatran etexilate** "
                      "prodrug below.  Idarucizumab is the "
                      "specific IIa-inhibitor reversal agent.",
            ),
            SARVariant(
                name="Dabigatran etexilate (Pradaxa prodrug)",
                smiles="CCCCCCOC(=O)/N=C(\\N)c1ccc(NCc2nc3"
                       "cc(C(=O)N(CCC(=O)OCC)c4ccccn4)ccc3"
                       "n2C)cc1",
                r_group_label="**Prodrug** — hexyloxy-"
                              "carbamate cap on the amidine + "
                              "ethyl-ester cap on the "
                              "carboxylate; both caps "
                              "hydrolysed by esterases in the "
                              "gut wall + blood",
                activity={"factor_xa": 0.0,
                          "target_ki_nM": 9999.0,
                          "oral_bioavailability_pct": 6.5,
                          "half_life_h": 14.0,
                          "logp": 5.6},
                notes="Caps both polar groups (the amidine + "
                      "the carboxylate) of dabigatran with "
                      "lipophilic prodrug groups, raising "
                      "logP from 3.0 → 5.6 and MW from 471 "
                      "→ 628 Da.  Result: oral absorption "
                      "rises ~ 10× compared to administering "
                      "free dabigatran.  Esterases in the gut "
                      "wall + blood hydrolyse both caps in "
                      "vivo to release the active "
                      "zwitterionic dabigatran.  **Textbook "
                      "example of a 'double prodrug' / "
                      "'sequential prodrug' that masks two "
                      "polar groups simultaneously.**  The "
                      "prodrug itself has no IIa activity "
                      "(target_ki_nM ~ 10 µM, encoded as "
                      "9999 placeholder for 'inactive').",
            ),
        ],
    ),

    # ---- Phase 31k round 161 — anticonvulsant series --------------
    SARSeries(
        id="anticonvulsants",
        name="Anticonvulsant series (different scaffolds, "
             "shared indication)",
        target="Multiple — voltage-gated Na+ channels, GABA "
               "system, voltage-gated Ca++ channels, SV2A "
               "vesicular protein",
        # No single shared scaffold — that's the point.  Use
        # phenytoin (the historical anchor) as the parent.
        parent_scaffold_smiles="O=C1NC(=O)C(c2ccccc2)(c3ccccc3)N1",
        source="Brodie & Sills 2011 *Lancet Neurol.* 10: "
               "1019-1030 (anticonvulsant mechanisms + "
               "SAR review)",
        activity_columns=["na_channel_blocker",
                          "broad_spectrum",
                          "cyp_induction_score",
                          "half_life_h",
                          "logp"],
        variants=[
            SARVariant(
                name="Phenytoin (Dilantin)",
                smiles="O=C1NC(=O)C(c2ccccc2)(c3ccccc3)N1",
                r_group_label="5,5-Diphenylhydantoin — the "
                              "1908 / 1938 prototype",
                activity={"na_channel_blocker": 1.0,
                          "broad_spectrum": 0.0,
                          "cyp_induction_score": 1.0,
                          "half_life_h": 22.0,
                          "logp": 1.8},
                notes="Heinrich Biltz 1908 (synthesis), Merritt "
                      "+ Putnam 1938 (anticonvulsant activity) "
                      "— the first non-sedating anticonvulsant.  "
                      "Mechanism: voltage-gated Na+ channel "
                      "block in the inactivated state, "
                      "preferentially silencing rapidly-firing "
                      "neurons.  **Strong CYP3A4 + CYP2C9 "
                      "inducer** + autoinducer — driver of many "
                      "drug-drug interactions (warfarin, OCs, "
                      "opioids).  Non-linear (saturable) "
                      "metabolism: small dose increases at the "
                      "top of the therapeutic range cause "
                      "disproportionate plasma rises — "
                      "narrow-window classic.  Effective for "
                      "tonic-clonic + focal seizures; no use "
                      "in absence seizures.",
            ),
            SARVariant(
                name="Carbamazepine (Tegretol)",
                smiles="NC(=O)N1c2ccccc2C=Cc2ccccc21",
                r_group_label="Dibenzazepine + 5-carboxamide "
                              "(tricyclic; structurally close "
                              "to imipramine TCA)",
                activity={"na_channel_blocker": 1.0,
                          "broad_spectrum": 0.0,
                          "cyp_induction_score": 1.0,
                          "half_life_h": 25.0,
                          "logp": 3.4},
                notes="Schindler 1953 (synthesis at Geigy as "
                      "an antidepressant-analogue scaffold), "
                      "1962 EU approval as anticonvulsant.  "
                      "Same Na+-channel mechanism as phenytoin "
                      "via a totally different scaffold (TCA-"
                      "like dibenzazepine).  **Strong CYP3A4 "
                      "inducer** (similar interaction profile "
                      "to phenytoin).  HLA-B*1502 carriers (~ "
                      "10% of Han Chinese, 2-4% of South Asian) "
                      "carry markedly elevated risk of "
                      "Stevens-Johnson syndrome / toxic "
                      "epidermal necrolysis — FDA boxed warning "
                      "for HLA testing in at-risk populations.",
            ),
            SARVariant(
                name="Valproate (Depakote)",
                smiles="CCCC(CCC)C(=O)O",
                r_group_label="**Branched fatty acid** — total "
                              "chemotype switch from "
                              "phenytoin/carbamazepine; "
                              "2-propylpentanoic acid",
                activity={"na_channel_blocker": 1.0,
                          "broad_spectrum": 1.0,
                          "cyp_induction_score": -1.0,
                          "half_life_h": 13.0,
                          "logp": 2.3},
                notes="Burton 1882 (synthesis as a 'clean' "
                      "solvent), Meunier 1962 (anticonvulsant "
                      "activity discovered serendipitously when "
                      "used as a vehicle for screening).  **The "
                      "broad-spectrum anticonvulsant**: Na+-"
                      "channel block + GABA augmentation "
                      "(GABA-T inhibition + GAD activation) + "
                      "T-type Ca++-channel block + HDAC "
                      "inhibition.  Effective on tonic-clonic, "
                      "absence, and myoclonic seizures — the "
                      "only seeded entry covering all three.  "
                      "Also licensed for bipolar mania + "
                      "migraine prophylaxis.  **CYP "
                      "INHIBITOR** (opposite of "
                      "phenytoin/carbamazepine) — raises "
                      "lamotrigine + phenobarbital levels.  "
                      "Hepatotoxic + teratogenic (neural-tube "
                      "defects ~ 1-2 %); contraindicated in "
                      "women of child-bearing potential "
                      "without strict contraception.",
            ),
            SARVariant(
                name="Lamotrigine (Lamictal)",
                smiles="Nc1nnc(-c2cccc(Cl)c2Cl)c(N)n1",
                r_group_label="Phenyltriazine — third "
                              "chemotype; 6-(2,3-dichloro"
                              "phenyl)-1,2,4-triazine-3,5-"
                              "diamine",
                activity={"na_channel_blocker": 1.0,
                          "broad_spectrum": 0.5,
                          "cyp_induction_score": 0.0,
                          "half_life_h": 25.0,
                          "logp": 2.0},
                notes="Burroughs Wellcome / GSK 1990.  Same "
                      "Na+-channel inactivation mechanism as "
                      "phenytoin / carbamazepine via yet "
                      "another scaffold.  **No CYP induction** "
                      "(metabolised by glucuronidation via "
                      "UGT1A4) — clean drug-drug-interaction "
                      "profile.  Effective on focal + tonic-"
                      "clonic + Lennox-Gastaut + bipolar "
                      "depression.  Critical clinical caveat: "
                      "**Stevens-Johnson syndrome / TEN** "
                      "risk on rapid titration (~ 1-3% in "
                      "children, lower in adults) — 6-week "
                      "slow titration mandatory.  Half-life "
                      "doubles when co-administered with "
                      "valproate (UGT inhibition).",
            ),
            SARVariant(
                name="Levetiracetam (Keppra)",
                smiles="CC[C@H](N1CCCC1=O)C(N)=O",
                r_group_label="**Pyrrolidone** — fourth "
                              "chemotype; (S)-α-ethyl-2-oxo-"
                              "1-pyrrolidineacetamide",
                activity={"na_channel_blocker": 0.0,
                          "broad_spectrum": 1.0,
                          "cyp_induction_score": 0.0,
                          "half_life_h": 7.0,
                          "logp": -0.1},
                notes="UCB 1999 — totally distinct mechanism: "
                      "binds the **synaptic-vesicle protein "
                      "SV2A** (Lynch et al. 2004), modulating "
                      "neurotransmitter release without "
                      "directly blocking Na+ or Ca++ channels.  "
                      "First-in-class.  **No CYP "
                      "interactions** (66% renal-cleared "
                      "unchanged) — the cleanest interaction "
                      "profile of any seeded anticonvulsant.  "
                      "Broad-spectrum on focal + generalised "
                      "tonic-clonic + myoclonic seizures.  "
                      "Behavioural side effects (irritability, "
                      "depression) are the dose-limiting "
                      "trade-off, not hepatotoxicity or "
                      "drug interactions.  Now first-line in "
                      "many guidelines for monotherapy.",
            ),
        ],
    ),

    # ---- Phase 31k round 160 — opioid analgesic series ------------
    SARSeries(
        id="opioid-analgesics",
        name="Opioid analgesic series (μ-receptor agonists)",
        target="μ-opioid receptor (MOR)",
        # Core scaffold: morphinan / 4-anilidopiperidine
        # template that connects all 5 entries.  The morphine
        # 5-ring tetracycle is the historical anchor; fentanyl
        # is the synthetic chemotype-switch outlier.
        parent_scaffold_smiles="CN1CCC2C3CCCC2C1Cc1ccccc13",
        source="Inturrisi 2002 *Clin. J. Pain* 18 Suppl: "
               "S3-S13 + Reisine & Pasternak 1996 (Goodman & "
               "Gilman ch. 23) — canonical opioid SAR + "
               "equianalgesic-dosing reviews",
        activity_columns=["mu_ki_nM",
                          "equianalgesic_mg_iv",
                          "potency_ratio_vs_morphine",
                          "logp"],
        variants=[
            SARVariant(
                name="Morphine",
                smiles="CN1CC[C@]23c4c5ccc(O)c4O[C@H]2"
                       "[C@@H](O)C=C[C@H]3[C@H]1C5",
                r_group_label="Natural pentacyclic morphinan; "
                              "3-OH (phenol) + 6-OH "
                              "(allyl alcohol) + double bond "
                              "C7-C8",
                activity={"mu_ki_nM": 1.4,
                          "equianalgesic_mg_iv": 10.0,
                          "potency_ratio_vs_morphine": 1.0,
                          "logp": 1.2},
                notes="Sertürner 1804 — first alkaloid ever "
                      "isolated (from opium poppy *Papaver "
                      "somniferum*).  Prototype μ-opioid "
                      "receptor agonist; the reference "
                      "compound for opioid potency.  Low logP "
                      "(1.2) means slow BBB penetration — "
                      "delays peak analgesic effect ~ 20-30 "
                      "min after IV.  Glucuronidated to "
                      "morphine-6-glucuronide (M6G, the "
                      "active metabolite, more potent than "
                      "morphine itself) and morphine-3-"
                      "glucuronide (M3G, neuroexcitatory).",
            ),
            SARVariant(
                name="Codeine",
                smiles="CN1CC[C@]23c4c5ccc(OC)c4O[C@H]2"
                       "[C@@H](O)C=C[C@H]3[C@H]1C5",
                r_group_label="Morphine 3-O-methyl ether "
                              "(3-OMe instead of 3-OH)",
                activity={"mu_ki_nM": 200.0,
                          "equianalgesic_mg_iv": 120.0,
                          "potency_ratio_vs_morphine": 0.08,
                          "logp": 1.5},
                notes="Robiquet 1832 — second opium alkaloid "
                      "isolated.  **Pro-drug**: codeine's "
                      "direct μ-receptor affinity is 100× "
                      "weaker than morphine's, but CYP2D6 "
                      "demethylates ~ 5-10% of an oral dose "
                      "to morphine in vivo, which provides "
                      "essentially all of the analgesic "
                      "effect.  CYP2D6-poor metabolisers (~ "
                      "5-10% of European, 1-2% of African / "
                      "Asian populations) get little "
                      "analgesia; ultra-rapid metabolisers "
                      "get morphine overdose — opposite "
                      "extremes of the same polymorphism.  "
                      "FDA boxed-warned for paediatric use "
                      "after deaths in fast metabolisers.",
            ),
            SARVariant(
                name="Hydromorphone (Dilaudid)",
                smiles="CN1CC[C@]23c4c5ccc(O)c4O[C@H]2"
                       "C(=O)CC[C@H]3[C@H]1C5",
                r_group_label="6-keto + dihydro morphine "
                              "(7,8-saturation + 6-OH→6-=O)",
                activity={"mu_ki_nM": 0.4,
                          "equianalgesic_mg_iv": 1.5,
                          "potency_ratio_vs_morphine": 7.0,
                          "logp": 1.6},
                notes="Knoll 1924 — semi-synthetic from "
                      "morphine.  Two SAR moves: saturate "
                      "the C7-C8 double bond + oxidise the "
                      "6-OH allyl alcohol to a 6-ketone.  "
                      "**~ 7× more potent than morphine** on "
                      "weight basis with shorter onset; "
                      "lacks the active glucuronide "
                      "metabolite of morphine, so cleaner PK "
                      "in renal-failure patients (where "
                      "M6G accumulates dangerously).",
            ),
            SARVariant(
                name="Oxycodone (OxyContin)",
                smiles="CN1CC[C@@]23c4c5ccc(OC)c4O[C@H]2"
                       "C(=O)CC[C@@]3(O)[C@H]1C5",
                r_group_label="14-OH + 6-keto + 3-OMe + "
                              "dihydro semi-synthetic from "
                              "thebaine",
                activity={"mu_ki_nM": 18.0,
                          "equianalgesic_mg_iv": 5.0,
                          "potency_ratio_vs_morphine": 2.0,
                          "logp": 1.0},
                notes="Freund + Speyer 1916 — semi-synthetic "
                      "from thebaine (third major opium "
                      "alkaloid).  Direct μ-receptor "
                      "affinity is *lower* than morphine "
                      "(Ki 18 vs 1.4 nM) but the "
                      "14-OH + 6-keto + 3-OMe combination "
                      "gives oral bioavailability ~ 60-87% "
                      "(morphine PO is only ~ 25%).  Major "
                      "active metabolite oxymorphone "
                      "(CYP2D6-mediated 3-O-demethylation) "
                      "is ~ 3× more potent than morphine.  "
                      "OxyContin (1996) — controlled-release "
                      "oxycodone — is the drug at the centre "
                      "of the US opioid crisis: marketed as "
                      "low-abuse-potential; reformulated 2010 "
                      "to a tamper-resistant matrix.",
            ),
            SARVariant(
                name="Fentanyl",
                smiles="CCC(=O)N(c1ccccc1)C1CCN(CCc2ccccc2)CC1",
                r_group_label="**4-anilidopiperidine** "
                              "synthetic — total chemotype "
                              "switch from the morphinan "
                              "scaffold; phenethyl tail + "
                              "N-phenyl-propionamide cap",
                activity={"mu_ki_nM": 1.4,
                          "equianalgesic_mg_iv": 0.1,
                          "potency_ratio_vs_morphine": 100.0,
                          "logp": 4.1},
                notes="Janssen 1960 — total synthetic "
                      "chemotype switch.  Same μ-receptor "
                      "affinity as morphine (Ki 1.4 nM) but "
                      "**~ 100× more potent on weight basis** "
                      "because logP 4.1 vs morphine's 1.2 "
                      "drives 10-100× faster BBB "
                      "penetration.  This is THE textbook "
                      "example of **lipophilicity → potency** "
                      "in CNS pharmacology — same target, "
                      "same intrinsic affinity, vastly "
                      "different effective dose due to "
                      "physico-chem alone.  Onset 1-2 min IV "
                      "vs 20 min for morphine.  Carfentanil + "
                      "sufentanil push the same scaffold to "
                      "10 000× and 1000× morphine "
                      "respectively.  The lipophilicity-"
                      "drives-potency story has driven the "
                      "current illicit-fentanyl-analogue "
                      "epidemic — synthetic accessibility + "
                      "huge molar potency makes safe "
                      "trafficked-dose calibration impossible.",
            ),
        ],
    ),

    # ---- Phase 31k round 159 — PPI inhibitor series ---------------
    SARSeries(
        id="ppi-inhibitors",
        name="Proton-pump inhibitor (PPI) series",
        target="Gastric H+/K+-ATPase (Cys-813 covalent "
               "inhibition)",
        # Core scaffold: 2-(pyridinylmethyl-sulfinyl)-1H-
        # benzimidazole — every PPI is a substituted variant
        # of this template.
        parent_scaffold_smiles="O=S(Cc1ncccn1)c1nc2ccccc2[nH]1",
        source="Olbe, Carlsson & Lindberg 2003 *Nat. Rev. "
               "Drug Discov.* 2: 132-139 (the canonical PPI "
               "discovery + SAR review by the Astra team)",
        activity_columns=["onset_h", "duration_h",
                          "cyp_metabolism_dependence",
                          "logp"],
        variants=[
            SARVariant(
                name="Omeprazole (Prilosec)",
                smiles="COc1ccc2[nH]c(S(=O)Cc3ncc(C)c(OC)c3C)"
                       "nc2c1",
                r_group_label="Prototype racemate; 5-methoxy "
                              "benzimidazole + 4-methoxy / "
                              "3,5-dimethyl pyridine",
                activity={"onset_h": 1.5,
                          "duration_h": 24.0,
                          "cyp_metabolism_dependence": 1.0,
                          "logp": 2.9},
                notes="Astra 1988 — the first PPI launched + "
                      "the prototype.  Pro-drug mechanism: at "
                      "the parietal-cell secretory canaliculus "
                      "(pH ~ 1) the pyridine-N protonates, the "
                      "molecule rearranges via a sulfenamide "
                      "intermediate, and the activated species "
                      "covalently traps Cys-813 of H+/K+-"
                      "ATPase via a -S-S- bond.  Racemic "
                      "(R + S sulfoxide); both enantiomers "
                      "interconvert in vivo via CYP2C19, but "
                      "metabolism rates differ — the (R) "
                      "form clears faster, leaving the (S) "
                      "to do most of the work.  This is what "
                      "drove the chiral-switch development "
                      "below.",
            ),
            SARVariant(
                name="Esomeprazole (Nexium)",
                smiles="COc1ccc2[nH]c([S@@](=O)Cc3ncc(C)c(OC)"
                       "c3C)nc2c1",
                r_group_label="Single-enantiomer (S)-omeprazole "
                              "— **the prototypical chiral "
                              "switch drug**",
                activity={"onset_h": 1.5,
                          "duration_h": 30.0,
                          "cyp_metabolism_dependence": 0.6,
                          "logp": 2.9},
                notes="AstraZeneca 2001 — the textbook "
                      "**chiral-switch** development: take "
                      "the racemic parent (omeprazole) off-"
                      "patent, develop the more-active single "
                      "enantiomer as a new product with fresh "
                      "patent life.  Same scaffold + same "
                      "Cys-813 trapping mechanism as "
                      "omeprazole but with locked (S)-"
                      "sulfoxide chirality so the (R)-"
                      "elimination pathway is gone — net "
                      "result is reduced inter-patient "
                      "CYP2C19-polymorphism variability + "
                      "longer duration of acid suppression.  "
                      "Pairs with the SSRI series's citalopram "
                      "→ escitalopram chiral switch as the "
                      "two textbook examples of the "
                      "single-enantiomer-from-racemic "
                      "patent-extension paradigm.",
            ),
            SARVariant(
                name="Lansoprazole (Prevacid)",
                smiles="Cc1c(OCC(F)(F)F)ccnc1CS(=O)c1nc2"
                       "ccccc2[nH]1",
                r_group_label="2,2,2-Trifluoroethoxy on "
                              "pyridine; unsubstituted "
                              "benzimidazole",
                activity={"onset_h": 1.7,
                          "duration_h": 24.0,
                          "cyp_metabolism_dependence": 0.9,
                          "logp": 3.5},
                notes="Takeda 1991 — first PPI to use a "
                      "fluorinated pyridine substituent.  The "
                      "trifluoroethoxy group raises logP "
                      "(+0.6 vs omeprazole) which speeds "
                      "absorption; same Cys-813 mechanism + "
                      "similar duration.  Cleared mostly via "
                      "CYP3A4 + CYP2C19 with similar "
                      "polymorphism issues to omeprazole.",
            ),
            SARVariant(
                name="Pantoprazole (Protonix)",
                smiles="COc1ccnc(CS(=O)c2nc3cc(OC(F)F)ccc3"
                       "[nH]2)c1OC",
                r_group_label="3,4-Dimethoxy pyridine + "
                              "5-difluoromethoxy benzimidazole "
                              "— most CYP-independent",
                activity={"onset_h": 2.0,
                          "duration_h": 24.0,
                          "cyp_metabolism_dependence": 0.3,
                          "logp": 2.9},
                notes="Byk Gulden 1985 / approved 1995.  The "
                      "5-OCHF₂ + 4-OMe combination dramatically "
                      "lowers CYP-mediated clearance — "
                      "pantoprazole goes through Phase-II "
                      "sulfotransferase conjugation as the "
                      "dominant metabolic pathway.  Result: "
                      "**least drug-drug interactions** of any "
                      "PPI, no clinically-significant "
                      "interaction with warfarin / clopidogrel "
                      "/ phenytoin / theophylline.  The PPI "
                      "of choice in polypharmacy elderly + "
                      "ICU patients.",
            ),
            SARVariant(
                name="Rabeprazole (AcipHex)",
                smiles="COCCCOc1ccnc(CS(=O)c2nc3ccccc3"
                       "[nH]2)c1C",
                r_group_label="3-Methoxypropoxy on pyridine "
                              "— fastest activation",
                activity={"onset_h": 1.0,
                          "duration_h": 24.0,
                          "cyp_metabolism_dependence": 0.4,
                          "logp": 3.0},
                notes="Eisai 1999 — designed for **fastest "
                      "onset** of the class.  Higher pKa of "
                      "the benzimidazole N (5.0 vs 4.0 for "
                      "omeprazole) means rabeprazole "
                      "protonates + activates at a higher "
                      "intracellular pH — works even in "
                      "patients with chronic gastritis whose "
                      "secretory canaliculus pH is elevated.  "
                      "Like pantoprazole, mostly non-"
                      "enzymatic activation + reduction "
                      "metabolism, so few CYP interactions.  "
                      "Onset ~ 1 h vs ~ 1.5-2 h for the "
                      "rest of the class.",
            ),
        ],
    ),

    # ---- Phase 31k round 158 — H1-antihistamine series -------------
    SARSeries(
        id="h1-antihistamines",
        name="H1-antihistamine series (1st-gen → 2nd-gen → 3rd-gen)",
        target="Histamine H1 receptor",
        # Core scaffold: ethylenediamine / aminoalkyl-diaryl
        # template that connects all 3 generations.
        parent_scaffold_smiles="N(C)(C)CCC(c1ccccc1)c1ccccc1",
        source="Simons & Simons 2008 *J. Allergy Clin. "
               "Immunol.* 121: S30-S36 (the canonical H1 SAR "
               "review)",
        activity_columns=["h1_ki_nM", "sedation_score",
                          "qt_risk", "logp"],
        variants=[
            SARVariant(
                name="Diphenhydramine (Benadryl)",
                smiles="CN(C)CCOC(c1ccccc1)c1ccccc1",
                r_group_label="1st-gen ethanolamine; benzhydryl "
                              "ether + dimethylamine tail",
                activity={"h1_ki_nM": 16.0,
                          "sedation_score": 5.0,
                          "qt_risk": 0.0,
                          "logp": 3.4},
                notes="Rieveschl 1943 — the original H1 "
                      "antihistamine.  Crosses the BBB freely "
                      "(logP 3.4, low TPSA, no zwitterion); "
                      "potent muscarinic-receptor cross-"
                      "reactivity gives anticholinergic side "
                      "effects (dry mouth, urinary retention) "
                      "on top of sedation.  The OTC sleep aid "
                      "in many sleep-aid products (ZzzQuil, "
                      "Tylenol PM).",
            ),
            SARVariant(
                name="Chlorpheniramine (Chlor-Trimeton)",
                smiles="CN(C)CCC(c1ccccc1)c1ccc(Cl)cc1",
                r_group_label="1st-gen alkylamine; one aryl "
                              "halogenated (para-Cl); 3-carbon "
                              "tether (ethanolamine → propylamine)",
                activity={"h1_ki_nM": 4.6,
                          "sedation_score": 3.0,
                          "qt_risk": 0.0,
                          "logp": 3.2},
                notes="Schering 1951 — 4× more potent than "
                      "diphenhydramine because the para-Cl + "
                      "propylamine geometry better fills the "
                      "H1 receptor binding pocket.  Less "
                      "sedating than diphenhydramine but "
                      "still BBB-penetrant + still touches "
                      "muscarinic receptors.",
            ),
            SARVariant(
                name="Hydroxyzine (Atarax / Vistaril)",
                smiles="OCCOCCN1CCN(C(c2ccccc2)c2ccc(Cl)cc2)CC1",
                r_group_label="1st-gen piperazine; benzhydryl "
                              "+ 2-(2-hydroxyethoxy)ethyl tail",
                activity={"h1_ki_nM": 1.5,
                          "sedation_score": 4.0,
                          "qt_risk": 0.0,
                          "logp": 3.1},
                notes="UCB 1956 — piperazine class adds an "
                      "anxiolytic + antiemetic profile on top "
                      "of H1 antagonism.  Still sedating + "
                      "BBB-penetrant despite the polar "
                      "hydroxyethoxy tail.  The pro-drug from "
                      "which cetirizine emerges: oxidative "
                      "metabolism of the terminal -OH to "
                      "-COOH gives the zwitterionic 2nd-gen "
                      "drug below.",
            ),
            SARVariant(
                name="Loratadine (Claritin)",
                smiles="CCOC(=O)N1CCC(=C2c3ccc(Cl)cc3CCc3cccnc23)CC1",
                r_group_label="2nd-gen tricyclic; rigid "
                              "exocyclic-piperidinylidene + "
                              "ethyl-carbamate cap on N",
                activity={"h1_ki_nM": 50.0,
                          "sedation_score": 0.5,
                          "qt_risk": 0.0,
                          "logp": 4.9},
                notes="Schering-Plough 1989, OTC 2002 — the "
                      "tricyclic geometry locks the diaryl "
                      "groups in the H1-receptor-binding "
                      "conformation while the carbamate cap "
                      "prevents BBB entry (P-gp substrate).  "
                      "Loratadine itself is a pro-drug; in "
                      "vivo CYP3A4 / CYP2D6 cleaves the "
                      "carbamate to give desloratadine "
                      "(Clarinex), which is the actual H1 "
                      "antagonist (Ki ~ 0.4 nM).  No sedation, "
                      "no anticholinergic side effects, no QT "
                      "issues — the 2nd-gen template that "
                      "made non-sedating antihistamines a "
                      "$10B+ market.",
            ),
            SARVariant(
                name="Cetirizine (Zyrtec)",
                smiles="OC(=O)COCCN1CCN([C@@H](c2ccccc2)"
                       "c2ccc(Cl)cc2)CC1",
                r_group_label="2nd-gen carboxylic-acid "
                              "metabolite of hydroxyzine; "
                              "zwitterion at physiological pH",
                activity={"h1_ki_nM": 6.0,
                          "sedation_score": 1.0,
                          "qt_risk": 0.0,
                          "logp": 3.2},
                notes="UCB 1987 — direct development from "
                      "hydroxyzine: oxidise the terminal "
                      "hydroxyethyl tail to a carboxylic "
                      "acid, get a zwitterion at "
                      "physiological pH that can NOT cross "
                      "the BBB (despite having the same "
                      "diaryl-piperazine pharmacophore).  "
                      "Slightly sedating in some patients "
                      "(crosses BBB at high doses) but far "
                      "less than 1st-gen agents.  The "
                      "(R)-enantiomer levocetirizine "
                      "(Xyzal) is the active component.",
            ),
            SARVariant(
                name="Fexofenadine (Allegra)",
                smiles="CC(C)(C(=O)O)c1ccc(C(O)CCCN2CCC"
                       "(C(O)(c3ccccc3)c3ccccc3)CC2)cc1",
                r_group_label="3rd-gen carboxylic-acid "
                              "metabolite of terfenadine; "
                              "zwitterion + bulky tertiary-OH "
                              "diphenyl",
                activity={"h1_ki_nM": 10.0,
                          "sedation_score": 0.0,
                          "qt_risk": 0.0,
                          "logp": 5.5},
                notes="Hoechst Marion Roussel 1996 — the "
                      "**3rd-generation breakthrough**.  "
                      "Terfenadine (Seldane, 1985) was the "
                      "first non-sedating H1, but it blocked "
                      "the cardiac hERG K⁺ channel — sudden "
                      "deaths from torsades de pointes when "
                      "co-administered with CYP3A4 inhibitors "
                      "(grapefruit juice, ketoconazole, "
                      "erythromycin) led to 1998 withdrawal.  "
                      "Fexofenadine is the carboxylic-acid "
                      "metabolite of terfenadine (CYP3A4 "
                      "oxidation of the tert-butyl group's "
                      "methyl); the COOH adds a zwitterion "
                      "that blocks BBB entry AND eliminates "
                      "hERG affinity.  The textbook example "
                      "of an active metabolite displacing "
                      "its parent drug.",
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
