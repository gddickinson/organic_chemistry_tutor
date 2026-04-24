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
