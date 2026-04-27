"""Phase PH-1.0 (round 214) — 30-entry drug-class catalogue.

Spans 11 therapeutic areas + 9 molecular-target classes.
Cross-references resolve to:
- ``cross_reference_molecule_names`` → orgchem ``Molecule.name``
- ``cross_reference_enzyme_ids`` → ``biochem.core.enzymes`` ids
- ``cross_reference_signaling_pathway_ids`` →
  ``cellbio.core.cell_signaling`` ids
"""
from __future__ import annotations
from typing import List

from pharm.core.drug_classes import DrugClass


DRUG_CLASSES: List[DrugClass] = [

    # ============================================================
    # Cardiovascular
    # ============================================================
    DrugClass(
        id="beta-blockers",
        name="β-adrenergic receptor blockers (β-blockers)",
        target_class="GPCR",
        therapeutic_areas=("cardiovascular",),
        mechanism="Competitive antagonism of β-adrenergic "
                  "receptors → reduced cAMP → reduced heart "
                  "rate, contractility, renin release.",
        molecular_target="β1 ± β2 ± β3 adrenergic GPCRs",
        typical_agents=("Metoprolol (β1-selective)",
                        "Atenolol (β1-selective)",
                        "Bisoprolol (β1-selective)",
                        "Propranolol (non-selective)",
                        "Carvedilol (α1 + β non-selective)"),
        clinical_use=("Hypertension", "Heart failure (carvedilol, "
                      "bisoprolol, metoprolol succinate)",
                      "Post-MI", "Angina",
                      "Tachyarrhythmias", "Migraine prophylaxis",
                      "Performance anxiety"),
        side_effects=("Bradycardia", "Hypotension", "Fatigue",
                      "Bronchospasm (non-selective)",
                      "Cold extremities", "Sleep disturbance"),
        contraindications=("Severe bradycardia / heart block "
                           "(without pacemaker)",
                           "Severe asthma (relative for "
                           "non-selective)",
                           "Decompensated heart failure"),
        monitoring=("Heart rate", "Blood pressure",
                    "Symptoms of HF decompensation"),
        cross_reference_molecule_names=("Propranolol",
                                        "Metoprolol"),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(
            "gpcr-camp-pka",),
        notes="The Black + Stephenson β-receptor work won the "
              "1988 Nobel.  Carvedilol's α1 + antioxidant "
              "effects make it preferred in heart failure.",
    ),
    DrugClass(
        id="ace-inhibitors",
        name="Angiotensin-converting enzyme (ACE) inhibitors",
        target_class="enzyme",
        therapeutic_areas=("cardiovascular",),
        mechanism="Inhibit ACE → reduced angiotensin II + "
                  "increased bradykinin → vasodilation, "
                  "natriuresis, RAAS suppression.",
        molecular_target="Angiotensin-converting enzyme (ACE; "
                         "Zn²⁺ metallopeptidase)",
        typical_agents=("Lisinopril", "Ramipril", "Enalapril "
                        "(prodrug)", "Captopril (first ACEi)"),
        clinical_use=("Hypertension",
                      "Heart failure with reduced EF",
                      "Post-MI",
                      "Diabetic nephropathy / proteinuria"),
        side_effects=("Dry cough (bradykinin-mediated, ~ 10 %)",
                      "Hyperkalaemia", "Acute kidney injury "
                      "(esp. bilateral renal artery stenosis)",
                      "Angioedema (rare but life-threatening)"),
        contraindications=("Pregnancy (teratogenic)",
                           "Bilateral renal artery stenosis",
                           "Prior angioedema",
                           "Hyperkalaemia"),
        monitoring=("Creatinine + K⁺ at baseline + 1-2 weeks "
                    "after start", "Blood pressure"),
        cross_reference_molecule_names=("Captopril",
                                        "Lisinopril",
                                        "Ramipril",
                                        "Enalapril"),
        cross_reference_enzyme_ids=("ace",),
        cross_reference_signaling_pathway_ids=(
            "gpcr-ip3-ca",),
        notes="Captopril (1981) was the first structure-based "
              "drug (modelled on snake-venom peptide BPP9a).",
    ),
    DrugClass(
        id="arbs",
        name="Angiotensin II receptor blockers (ARBs / sartans)",
        target_class="GPCR",
        therapeutic_areas=("cardiovascular",),
        mechanism="Competitive antagonism at AT1 receptor → "
                  "blocks angiotensin II vasoconstriction + "
                  "aldosterone release WITHOUT bradykinin "
                  "accumulation.",
        molecular_target="Angiotensin II type-1 (AT1) GPCR",
        typical_agents=("Losartan", "Valsartan", "Olmesartan",
                        "Candesartan", "Telmisartan", "Irbesartan"),
        clinical_use=("Hypertension",
                      "Heart failure with reduced EF "
                      "(especially if ACEi-intolerant)",
                      "Diabetic nephropathy"),
        side_effects=("Hyperkalaemia", "Acute kidney injury",
                      "Dizziness", "Angioedema (rare; lower "
                      "than ACEi)"),
        contraindications=("Pregnancy",
                           "Bilateral renal artery stenosis",
                           "Hyperkalaemia"),
        monitoring=("Creatinine + K⁺", "Blood pressure"),
        cross_reference_molecule_names=("Losartan",),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(
            "gpcr-ip3-ca",),
        notes="Often preferred over ACEi when cough is the "
              "dose-limiting side effect.",
    ),
    DrugClass(
        id="ccbs",
        name="Calcium-channel blockers (CCBs)",
        target_class="ion-channel",
        therapeutic_areas=("cardiovascular",),
        mechanism="Block L-type voltage-gated Ca²⁺ channels → "
                  "vasodilation (DHPs) or reduced cardiac "
                  "rate / conduction (non-DHPs).",
        molecular_target="L-type voltage-gated Ca²⁺ channels "
                         "(Cav1.x family)",
        typical_agents=("Amlodipine (DHP)",
                        "Nifedipine (DHP)",
                        "Felodipine (DHP)",
                        "Verapamil (non-DHP)",
                        "Diltiazem (non-DHP)"),
        clinical_use=("Hypertension", "Stable angina",
                      "Vasospastic angina (Prinzmetal)",
                      "Atrial fibrillation rate control "
                      "(non-DHPs)",
                      "Raynaud phenomenon"),
        side_effects=("Peripheral oedema (DHPs)",
                      "Flushing", "Headache",
                      "Constipation (verapamil)",
                      "Bradycardia / heart block (non-DHPs)"),
        contraindications=("Decompensated heart failure with "
                           "non-DHPs",
                           "Severe AV block (non-DHPs)",
                           "Combination of non-DHP CCB with "
                           "β-blocker → high block risk"),
        monitoring=("Blood pressure", "Heart rate "
                    "(non-DHPs)"),
        cross_reference_molecule_names=(),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(
            "gpcr-ip3-ca", "camkii"),
        notes="DHPs (-dipines) are vasoselective; non-DHPs "
              "are cardioselective.  Don't combine non-DHP "
              "CCB with β-blocker without expert input.",
    ),
    DrugClass(
        id="loop-diuretics",
        name="Loop diuretics",
        target_class="transporter",
        therapeutic_areas=("cardiovascular",),
        mechanism="Block Na⁺-K⁺-2Cl⁻ co-transporter (NKCC2) "
                  "in the thick ascending limb of Henle → "
                  "powerful natriuresis + diuresis.",
        molecular_target="NKCC2 (SLC12A1) co-transporter",
        typical_agents=("Furosemide", "Torsemide", "Bumetanide",
                        "Ethacrynic acid (sulfa-allergy "
                        "alternative)"),
        clinical_use=("Acute pulmonary oedema",
                      "Decompensated heart failure",
                      "Cirrhotic ascites",
                      "Severe hypertension with volume "
                      "overload"),
        side_effects=("Hypokalaemia",
                      "Hypomagnesaemia",
                      "Hyponatraemia (less than thiazides)",
                      "Hyperuricaemia / gout",
                      "Ototoxicity (esp. high-dose IV)",
                      "Pre-renal AKI from over-diuresis"),
        contraindications=("Severe volume depletion",
                           "Anuria",
                           "Sulfa allergy (relative — "
                           "ethacrynic acid is alternative)"),
        monitoring=("Electrolytes (K⁺, Mg²⁺, Na⁺)",
                    "Creatinine", "Body weight + symptoms"),
        cross_reference_molecule_names=(),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes="Ceiling effect at Loop sites; switch to "
              "combination diuresis (loop + thiazide) for "
              "diuretic-resistant heart failure.",
    ),
    DrugClass(
        id="thiazide-diuretics",
        name="Thiazide + thiazide-like diuretics",
        target_class="transporter",
        therapeutic_areas=("cardiovascular",),
        mechanism="Block Na⁺-Cl⁻ co-transporter (NCC) in "
                  "distal convoluted tubule → moderate "
                  "natriuresis + paradoxical Ca²⁺ "
                  "reabsorption.",
        molecular_target="NCC (SLC12A3) co-transporter",
        typical_agents=("Hydrochlorothiazide",
                        "Chlorthalidone",
                        "Indapamide",
                        "Metolazone"),
        clinical_use=("Hypertension (first-line)",
                      "Mild heart failure",
                      "Calcium nephrolithiasis "
                      "(reduces urinary Ca²⁺)",
                      "Nephrogenic diabetes insipidus "
                      "(paradoxical)"),
        side_effects=("Hypokalaemia",
                      "Hyponatraemia",
                      "Hyperuricaemia / gout",
                      "Hyperglycaemia", "Hypercalcaemia",
                      "Hyperlipidaemia",
                      "Erectile dysfunction"),
        contraindications=("Severe renal impairment "
                           "(eGFR < 30 — limited efficacy)",
                           "Severe hyponatraemia",
                           "Sulfa allergy (relative)"),
        monitoring=("Electrolytes", "Glucose", "Uric acid"),
        cross_reference_molecule_names=(),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes="Chlorthalidone has longer half-life + better "
              "outcome data than HCTZ for hypertension.",
    ),
    DrugClass(
        id="statins",
        name="HMG-CoA reductase inhibitors (statins)",
        target_class="enzyme",
        therapeutic_areas=("cardiovascular", "metabolic"),
        mechanism="Competitive inhibition of HMG-CoA "
                  "reductase → reduced cholesterol "
                  "biosynthesis → upregulation of hepatic "
                  "LDL-receptor → lower serum LDL-C.",
        molecular_target="HMG-CoA reductase (rate-limiting "
                         "step of cholesterol biosynthesis)",
        typical_agents=("Atorvastatin",
                        "Rosuvastatin",
                        "Simvastatin",
                        "Pravastatin",
                        "Pitavastatin"),
        clinical_use=("ASCVD primary + secondary prevention",
                      "Hyperlipidaemia",
                      "Diabetes ≥ 40 years (primary "
                      "prevention)"),
        side_effects=("Myalgia (~ 5-10 %)",
                      "Rare rhabdomyolysis",
                      "Mild transaminitis",
                      "Hyperglycaemia / new-onset diabetes",
                      "Cognitive concerns (controversial)"),
        contraindications=("Active liver disease",
                           "Pregnancy",
                           "Concomitant strong CYP3A4 "
                           "inhibitors with simva / atorva"),
        monitoring=("Baseline lipids + LFTs",
                    "Repeat lipids 6-12 weeks after start "
                    "or dose change",
                    "CK if symptoms"),
        cross_reference_molecule_names=("Cholesterol",),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes="Rosuvastatin + atorvastatin are 'high-"
              "intensity' (≥ 50 % LDL-C lowering).  Renal "
              "dose adjustment for rosuvastatin.",
    ),
    DrugClass(
        id="anticoagulants",
        name="Anticoagulants (warfarin / DOACs / heparin)",
        target_class="enzyme",
        therapeutic_areas=("cardiovascular", "haematology"),
        mechanism="Warfarin: vitamin-K epoxide reductase "
                  "inhibition → reduced functional II / VII / "
                  "IX / X.  DOACs: direct factor Xa or "
                  "thrombin inhibition.  Heparins: enhance "
                  "antithrombin → factor IIa + Xa "
                  "inactivation.",
        molecular_target="VKORC1 (warfarin); "
                         "FXa or FIIa (DOACs); "
                         "antithrombin III (heparins)",
        typical_agents=("Warfarin",
                        "Apixaban (FXa inhibitor)",
                        "Rivaroxaban (FXa inhibitor)",
                        "Dabigatran (direct thrombin "
                        "inhibitor)",
                        "Enoxaparin (LMWH)",
                        "Heparin (UFH)"),
        clinical_use=("Atrial fibrillation stroke prophylaxis",
                      "Venous thromboembolism (DVT / PE) "
                      "treatment + prevention",
                      "Mechanical heart valves (warfarin "
                      "still preferred)",
                      "Acute coronary syndrome bridging"),
        side_effects=("Major bleeding",
                      "Heparin-induced thrombocytopenia (HIT)",
                      "Warfarin-induced skin necrosis "
                      "(early protein-C drop)"),
        contraindications=("Active major bleeding",
                           "Severe thrombocytopenia",
                           "Recent intracranial bleed",
                           "Pregnancy (warfarin teratogenic)"),
        monitoring=("Warfarin: INR target 2-3 (3-4 for "
                    "mech valves)",
                    "DOACs: renal function, no routine INR",
                    "UFH: aPTT or anti-Xa",
                    "LMWH: anti-Xa in renal impairment / "
                    "obesity / pregnancy"),
        cross_reference_molecule_names=(),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes="DOACs have largely supplanted warfarin "
              "except for mechanical valves + severe "
              "renal disease + pregnancy.",
    ),
    DrugClass(
        id="antiplatelets",
        name="Antiplatelets",
        target_class="enzyme",
        therapeutic_areas=("cardiovascular", "haematology"),
        mechanism="Aspirin: irreversible COX-1 acetylation "
                  "→ reduced TXA2 synthesis.  P2Y12 "
                  "inhibitors: block ADP-mediated platelet "
                  "activation.  GP IIb/IIIa antagonists: "
                  "block fibrinogen binding.",
        molecular_target="COX-1 (aspirin); P2Y12 GPCR "
                         "(clopidogrel et al); GP IIb/IIIa "
                         "integrin (eptifibatide et al)",
        typical_agents=("Aspirin (low-dose 75-100 mg)",
                        "Clopidogrel",
                        "Ticagrelor",
                        "Prasugrel",
                        "Eptifibatide (GP IIb/IIIa)"),
        clinical_use=("Secondary prevention of MI / stroke",
                      "Acute coronary syndrome",
                      "Coronary stenting (DAPT — dual "
                      "antiplatelet therapy)"),
        side_effects=("Bleeding (especially GI)",
                      "Dyspnoea (ticagrelor)",
                      "TTP / neutropenia (clopidogrel — rare)"),
        contraindications=("Active bleeding",
                           "Known hypersensitivity",
                           "Severe thrombocytopenia"),
        monitoring=("Bleeding signs",
                    "CBC if dual therapy"),
        cross_reference_molecule_names=("Aspirin",
                                        "Clopidogrel"),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes="Aspirin acetylates COX-1 for the platelet's "
              "lifespan (~ 10 days) since platelets lack "
              "nuclei + can't resynthesise the enzyme.",
    ),

    # ============================================================
    # Pulmonology
    # ============================================================
    DrugClass(
        id="beta2-agonists",
        name="β2-adrenergic agonists",
        target_class="GPCR",
        therapeutic_areas=("pulmonology",),
        mechanism="Activate β2-AR → Gαs → cAMP → PKA → "
                  "MLCK inactivation → bronchial smooth-"
                  "muscle relaxation.",
        molecular_target="β2-adrenergic GPCR",
        typical_agents=("Salbutamol / albuterol (SABA)",
                        "Terbutaline (SABA)",
                        "Salmeterol (LABA)",
                        "Formoterol (LABA)",
                        "Vilanterol (ultra-LABA)"),
        clinical_use=("Asthma rescue (SABA)",
                      "Asthma controller (LABA + ICS)",
                      "COPD bronchodilation",
                      "Acute hyperkalaemia (drives K⁺ "
                      "intracellular)"),
        side_effects=("Tachycardia + tremor",
                      "Hypokalaemia",
                      "Hyperglycaemia",
                      "QT prolongation (rare)"),
        contraindications=("LABA monotherapy in asthma "
                           "(black-box — mortality)",
                           "Tachyarrhythmia"),
        monitoring=("Symptom control",
                    "Inhaler technique",
                    "K⁺ if frequent dosing"),
        cross_reference_molecule_names=("Salbutamol",),
        cross_reference_enzyme_ids=("adenylate-cyclase",),
        cross_reference_signaling_pathway_ids=(
            "gpcr-camp-pka",),
        notes="LABA monotherapy in asthma was associated "
              "with mortality (SMART trial) — must be paired "
              "with inhaled corticosteroid.",
    ),

    # ============================================================
    # Pain + inflammation
    # ============================================================
    DrugClass(
        id="nsaids",
        name="Non-steroidal anti-inflammatory drugs (NSAIDs)",
        target_class="enzyme",
        therapeutic_areas=("pain", "inflammation-immunology"),
        mechanism="Inhibit COX-1 ± COX-2 → reduced "
                  "prostaglandin synthesis → analgesia + "
                  "anti-inflammatory + antipyretic effects.",
        molecular_target="COX-1 + COX-2 (PTGS1, PTGS2)",
        typical_agents=("Ibuprofen", "Naproxen", "Diclofenac",
                        "Celecoxib (COX-2 selective)",
                        "Ketorolac (potent IV)",
                        "Aspirin (anti-inflammatory dose)"),
        clinical_use=("Mild-moderate pain",
                      "Osteoarthritis",
                      "Rheumatoid arthritis",
                      "Dysmenorrhoea",
                      "Fever",
                      "Acute gout"),
        side_effects=("GI ulceration / bleeding",
                      "Renal impairment (acute + chronic)",
                      "Hypertension worsening",
                      "Cardiovascular events (especially "
                      "COX-2 selective)",
                      "Hyperkalaemia",
                      "Hepatotoxicity (rare)"),
        contraindications=("Active peptic ulcer disease",
                           "Severe renal impairment",
                           "Severe heart failure",
                           "Pregnancy (esp. third trimester)",
                           "NSAID allergy / asthma triad"),
        monitoring=("Renal function + BP if chronic",
                    "GI symptoms",
                    "Consider PPI co-prescription"),
        cross_reference_molecule_names=("Ibuprofen",
                                        "Aspirin",
                                        "Naproxen"),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes="Selective COX-2 inhibitors (rofecoxib) were "
              "withdrawn for cardiovascular events; "
              "celecoxib retains use with cardiovascular "
              "warning.",
    ),
    DrugClass(
        id="opioids",
        name="Opioid analgesics",
        target_class="GPCR",
        therapeutic_areas=("pain",),
        mechanism="Agonism at μ-opioid receptor (Gαi-"
                  "coupled) → reduced cAMP, K⁺ efflux, "
                  "reduced Ca²⁺ influx → reduced "
                  "neurotransmitter release → analgesia.",
        molecular_target="μ-opioid receptor (MOR; OPRM1)",
        typical_agents=("Morphine",
                        "Oxycodone",
                        "Hydromorphone",
                        "Fentanyl (transdermal / IV)",
                        "Buprenorphine (partial agonist; "
                        "OUD treatment)",
                        "Tramadol (weak μ + SNRI)"),
        clinical_use=("Severe acute pain",
                      "Cancer / palliative pain",
                      "Anaesthesia (intra-op)",
                      "Opioid use disorder "
                      "(buprenorphine, methadone)"),
        side_effects=("Respiratory depression "
                      "(dose-limiting)",
                      "Constipation (does not tolerate)",
                      "Sedation",
                      "Nausea",
                      "Pruritus",
                      "Tolerance + physical dependence + "
                      "addiction risk"),
        contraindications=("Significant respiratory "
                           "compromise",
                           "Paralytic ileus",
                           "Concurrent monoamine oxidase "
                           "inhibitors (esp. tramadol, "
                           "meperidine)"),
        monitoring=("Pain score + functional response",
                    "Respiratory rate + sedation level",
                    "PDMP review",
                    "Naloxone co-prescription"),
        cross_reference_molecule_names=("Morphine",),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(
            "gpcr-camp-pka",),
        notes="Naloxone reverses opioid overdose by "
              "competitive μ-receptor antagonism; "
              "co-prescribe with chronic opioid therapy.",
    ),

    # ============================================================
    # Neurology / psychiatry
    # ============================================================
    DrugClass(
        id="ssris",
        name="Selective serotonin reuptake inhibitors (SSRIs)",
        target_class="transporter",
        therapeutic_areas=("neurology-psychiatry",),
        mechanism="Block serotonin reuptake transporter "
                  "(SERT) → increased synaptic 5-HT → "
                  "long-term receptor desensitisation + "
                  "neuroplastic changes.",
        molecular_target="Serotonin transporter (SERT; "
                         "SLC6A4)",
        typical_agents=("Sertraline", "Escitalopram",
                        "Citalopram", "Fluoxetine",
                        "Paroxetine", "Fluvoxamine"),
        clinical_use=("Major depressive disorder",
                      "Generalised anxiety disorder",
                      "Panic disorder", "OCD", "PTSD",
                      "Premenstrual dysphoric disorder"),
        side_effects=("GI upset / nausea (early)",
                      "Sexual dysfunction",
                      "Weight gain (paroxetine)",
                      "Hyponatraemia (SIADH, esp. elderly)",
                      "Increased bleeding risk",
                      "Discontinuation syndrome",
                      "Black-box: suicidality in young adults"),
        contraindications=("Concurrent MAOI use (serotonin "
                           "syndrome)",
                           "Linezolid co-administration",
                           "Caution in pregnancy"),
        monitoring=("Mood + suicidality (especially first "
                    "weeks)",
                    "Sodium in elderly",
                    "Bleeding signs"),
        cross_reference_molecule_names=(),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes="Onset of antidepressant effect 4-6 weeks; "
              "side effects often appear days 1-7 + "
              "improve with time.",
    ),
    DrugClass(
        id="benzodiazepines",
        name="Benzodiazepines",
        target_class="ion-channel",
        therapeutic_areas=("neurology-psychiatry",),
        mechanism="Allosteric modulation of GABA-A receptor "
                  "→ increased Cl⁻ influx → CNS inhibition.",
        molecular_target="GABA-A receptor (γ-subunit "
                         "benzodiazepine binding site)",
        typical_agents=("Diazepam (long-acting)",
                        "Lorazepam (intermediate)",
                        "Alprazolam (short)",
                        "Midazolam (procedural)",
                        "Clonazepam"),
        clinical_use=("Acute anxiety / panic",
                      "Insomnia (short-term)",
                      "Status epilepticus (lorazepam IV)",
                      "Alcohol withdrawal",
                      "Procedural sedation",
                      "Muscle spasm"),
        side_effects=("Sedation",
                      "Anterograde amnesia",
                      "Falls + fractures (elderly)",
                      "Tolerance + dependence + withdrawal "
                      "(seizures!)",
                      "Respiratory depression "
                      "(with opioids)"),
        contraindications=("Severe respiratory insufficiency",
                           "Acute narrow-angle glaucoma",
                           "Untreated obstructive sleep "
                           "apnoea",
                           "Pregnancy + breastfeeding"),
        monitoring=("Sedation + cognitive status",
                    "PDMP",
                    "Withdrawal plan if chronic use"),
        cross_reference_molecule_names=(),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes="Flumazenil is the GABA-A benzo-site antagonist "
              "for overdose reversal — use cautiously as it "
              "can precipitate seizures in chronic users.",
    ),
    DrugClass(
        id="atypical-antipsychotics",
        name="Atypical (second-generation) antipsychotics",
        target_class="GPCR",
        therapeutic_areas=("neurology-psychiatry",),
        mechanism="Combined D2 + 5-HT2A antagonism (varying "
                  "5-HT2A:D2 ratios); some have α1, H1, M1 "
                  "activity.",
        molecular_target="Dopamine D2 + serotonin 5-HT2A "
                         "GPCRs",
        typical_agents=("Risperidone", "Olanzapine",
                        "Quetiapine", "Aripiprazole "
                        "(partial D2 agonist)",
                        "Clozapine (refractory)",
                        "Lurasidone"),
        clinical_use=("Schizophrenia",
                      "Bipolar disorder (acute mania + "
                      "maintenance)",
                      "Adjunct in major depression",
                      "Behavioural symptoms in dementia "
                      "(black-box mortality warning)"),
        side_effects=("Metabolic syndrome (esp. olanzapine, "
                      "clozapine — weight gain, T2DM, "
                      "dyslipidaemia)",
                      "Extrapyramidal symptoms (risperidone)",
                      "Hyperprolactinaemia (risperidone)",
                      "QT prolongation",
                      "Clozapine: agranulocytosis, "
                      "myocarditis, seizures"),
        contraindications=("Clozapine: WBC < 3500 / mm³",
                           "QT-prolonging drug interactions"),
        monitoring=("Weight + BMI + waist circumference",
                    "Fasting glucose + lipids",
                    "ECG baseline if QT risk",
                    "Clozapine: weekly CBC × 6 months, "
                    "then less frequent"),
        cross_reference_molecule_names=(),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes="Aripiprazole's D2 partial agonism explains "
              "lower EPS + prolactin effects.",
    ),
    DrugClass(
        id="antiepileptics",
        name="Anti-seizure medications",
        target_class="ion-channel",
        therapeutic_areas=("neurology-psychiatry",),
        mechanism="Heterogeneous: Na⁺ channel blockade "
                  "(phenytoin, carbamazepine, lamotrigine), "
                  "Ca²⁺ channel modulation (gabapentinoids), "
                  "GABA enhancement (valproate, "
                  "benzodiazepines), SV2A binding "
                  "(levetiracetam).",
        molecular_target="Voltage-gated Na⁺ channels, "
                         "T-type Ca²⁺ channels, GABA-A, "
                         "SV2A vesicle protein, others",
        typical_agents=("Levetiracetam",
                        "Lamotrigine",
                        "Valproate",
                        "Carbamazepine",
                        "Phenytoin",
                        "Gabapentin / pregabalin"),
        clinical_use=("Epilepsy (focal + generalised)",
                      "Status epilepticus",
                      "Bipolar mania (valproate, "
                      "lamotrigine)",
                      "Migraine prophylaxis",
                      "Neuropathic pain (gabapentinoids, "
                      "carbamazepine for trigeminal "
                      "neuralgia)"),
        side_effects=("Sedation, dizziness, ataxia",
                      "Stevens-Johnson syndrome "
                      "(lamotrigine, carbamazepine — "
                      "HLA-B*1502 in Asians)",
                      "Hepatotoxicity (valproate)",
                      "Pancreatitis (valproate)",
                      "Hyperammonaemia (valproate)",
                      "Teratogenicity (esp. valproate)"),
        contraindications=("Valproate in women of "
                           "childbearing potential without "
                           "REMS",
                           "Carbamazepine + lamotrigine in "
                           "HLA-B*1502 carriers"),
        monitoring=("Serum levels for narrow-TI agents "
                    "(phenytoin, valproate, carbamazepine)",
                    "LFTs + CBC",
                    "Bone density (long-term enzyme inducers)"),
        cross_reference_molecule_names=(),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes="Levetiracetam is now first-line for many "
              "indications because of clean PK + minimal "
              "drug-drug interactions.",
    ),

    # ============================================================
    # Endocrinology / metabolic
    # ============================================================
    DrugClass(
        id="insulin",
        name="Insulin (rapid / long / mixed analogues)",
        target_class="other",
        therapeutic_areas=("endocrinology", "metabolic"),
        mechanism="Agonist at the insulin receptor (RTK) → "
                  "PI3K-Akt → GLUT4 translocation + glycogen "
                  "synthesis + lipogenesis + protein "
                  "synthesis.",
        molecular_target="Insulin receptor (RTK)",
        typical_agents=("Insulin lispro / aspart / glulisine "
                        "(rapid)",
                        "Insulin regular (short)",
                        "Insulin NPH (intermediate)",
                        "Insulin glargine / detemir / "
                        "degludec (long, basal)"),
        clinical_use=("Type 1 diabetes (essential)",
                      "Type 2 diabetes (advanced / "
                      "uncontrolled)",
                      "Diabetic ketoacidosis / HHS",
                      "Gestational diabetes "
                      "(when oral / GLP-1 insufficient)"),
        side_effects=("Hypoglycaemia (life-threatening)",
                      "Weight gain",
                      "Lipohypertrophy at injection sites",
                      "Hypokalaemia (drives K⁺ "
                      "intracellular — deliberate use in "
                      "DKA)"),
        contraindications=("Hypoglycaemia",
                           "Hypokalaemia (relative — must "
                           "replace K⁺ first in DKA)"),
        monitoring=("Glucose (CGM ideal)",
                    "HbA1c",
                    "Hypoglycaemia awareness",
                    "Injection technique"),
        cross_reference_molecule_names=("Insulin",
                                        "Glucose"),
        cross_reference_enzyme_ids=("hexokinase",),
        cross_reference_signaling_pathway_ids=("insulin",
                                               "pi3k-akt-mtor"),
        notes="Glargine / degludec → near-flat 24 h profile, "
              "lower nocturnal hypos than NPH.",
    ),
    DrugClass(
        id="glp1-agonists",
        name="GLP-1 receptor agonists (incretin mimetics)",
        target_class="GPCR",
        therapeutic_areas=("endocrinology", "metabolic"),
        mechanism="Activate GLP-1 receptor (Gαs-coupled) → "
                  "glucose-dependent insulin secretion + "
                  "glucagon suppression + delayed gastric "
                  "emptying + central appetite suppression.",
        molecular_target="GLP-1 receptor (GPCR)",
        typical_agents=("Semaglutide (oral + injectable "
                        "weekly)",
                        "Liraglutide (daily)",
                        "Dulaglutide (weekly)",
                        "Tirzepatide (dual GIP / GLP-1)",
                        "Exenatide"),
        clinical_use=("Type 2 diabetes",
                      "Obesity (semaglutide, liraglutide, "
                      "tirzepatide)",
                      "ASCVD risk reduction in T2DM "
                      "(semaglutide, liraglutide, "
                      "dulaglutide)",
                      "MASH (in development)"),
        side_effects=("Nausea + vomiting (early; titrate)",
                      "Diarrhoea",
                      "Pancreatitis (rare)",
                      "Gallbladder disease",
                      "Black-box: medullary thyroid carcinoma "
                      "in MEN-2 (rodent finding)"),
        contraindications=("Personal / family history of "
                           "medullary thyroid cancer",
                           "MEN-2",
                           "History of pancreatitis "
                           "(relative)"),
        monitoring=("HbA1c",
                    "Weight + waist",
                    "GI tolerability"),
        cross_reference_molecule_names=(),
        cross_reference_enzyme_ids=("adenylate-cyclase",),
        cross_reference_signaling_pathway_ids=(
            "gpcr-camp-pka", "insulin"),
        notes="Tirzepatide's dual GIP / GLP-1 agonism gives "
              "the largest weight loss of any FDA-approved "
              "agent (~ 22 % at 72 weeks).",
    ),
    DrugClass(
        id="sglt2-inhibitors",
        name="SGLT2 inhibitors (gliflozins)",
        target_class="transporter",
        therapeutic_areas=("endocrinology", "cardiovascular",
                           "metabolic"),
        mechanism="Block sodium-glucose co-transporter 2 in "
                  "the proximal tubule → glucosuria + mild "
                  "natriuresis + caloric loss + intratubular "
                  "haemodynamic effects.",
        molecular_target="SGLT2 (SLC5A2) transporter",
        typical_agents=("Empagliflozin",
                        "Dapagliflozin",
                        "Canagliflozin",
                        "Ertugliflozin"),
        clinical_use=("Type 2 diabetes",
                      "Heart failure (reduced + preserved "
                      "EF)",
                      "Chronic kidney disease "
                      "(albuminuric)",
                      "Cardiovascular risk reduction in "
                      "T2DM"),
        side_effects=("Genital mycotic infections",
                      "UTIs",
                      "Volume depletion / orthostasis",
                      "Euglycaemic DKA (rare but "
                      "important)",
                      "Fournier gangrene (very rare)",
                      "Lower-limb amputation signal "
                      "(canagliflozin — historical)"),
        contraindications=("Type 1 diabetes (DKA risk)",
                           "Severe renal impairment "
                           "(eGFR < 20 — varies by agent)",
                           "Active genital infection"),
        monitoring=("Renal function",
                    "Volume status",
                    "Symptoms of UTI / DKA",
                    "Foot exam"),
        cross_reference_molecule_names=("Glucose",),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes="Cardiovascular + renal benefits are "
              "independent of glucose lowering — now "
              "indicated even in non-diabetic HF + CKD.",
    ),

    # ============================================================
    # Gastrointestinal
    # ============================================================
    DrugClass(
        id="ppis",
        name="Proton-pump inhibitors (PPIs)",
        target_class="enzyme",
        therapeutic_areas=("gastrointestinal",),
        mechanism="Irreversibly inhibit the gastric "
                  "H⁺/K⁺-ATPase in parietal cells → "
                  "profound acid suppression.",
        molecular_target="Gastric H⁺/K⁺-ATPase",
        typical_agents=("Omeprazole", "Esomeprazole",
                        "Pantoprazole", "Lansoprazole",
                        "Rabeprazole"),
        clinical_use=("GORD / erosive oesophagitis",
                      "Peptic ulcer disease",
                      "H. pylori eradication regimens",
                      "Stress-ulcer prophylaxis (ICU)",
                      "Zollinger-Ellison syndrome"),
        side_effects=("Long-term: B12 + Mg²⁺ deficiency, "
                      "osteoporosis-related fractures, "
                      "C. difficile risk, pneumonia, "
                      "interstitial nephritis, possible "
                      "dementia association",
                      "Drug interactions (clopidogrel via "
                      "CYP2C19)"),
        contraindications=("Known hypersensitivity",),
        monitoring=("De-prescribe when indication ends",
                    "B12 + Mg²⁺ + bone density on "
                    "long-term therapy"),
        cross_reference_molecule_names=(),
        cross_reference_enzyme_ids=("na-k-atpase",),
        # ↑ structurally analogous P-type ATPase
        cross_reference_signaling_pathway_ids=(),
        notes="Omeprazole's discovery was a paradigm shift "
              "for GORD treatment (1988 launch; >90 % healing "
              "of erosive oesophagitis).",
    ),

    # ============================================================
    # Infectious disease
    # ============================================================
    DrugClass(
        id="beta-lactams",
        name="β-lactam antibiotics (penicillins / "
             "cephalosporins / carbapenems)",
        target_class="enzyme",
        therapeutic_areas=("infectious",),
        mechanism="Acylate penicillin-binding proteins "
                  "(transpeptidases) → block bacterial cell-"
                  "wall cross-linking → bacterial lysis.",
        molecular_target="Bacterial PBPs (transpeptidases)",
        typical_agents=("Amoxicillin / clavulanate",
                        "Piperacillin / tazobactam",
                        "Ceftriaxone (3rd-gen ceph)",
                        "Cefepime (4th-gen)",
                        "Meropenem (carbapenem)",
                        "Aztreonam (monobactam)"),
        clinical_use=("Wide spectrum — community-acquired "
                      "infections (amoxicillin)",
                      "Hospital-acquired (piperacillin-"
                      "tazobactam)",
                      "Meningitis (ceftriaxone)",
                      "Resistant gram-negatives "
                      "(carbapenems)"),
        side_effects=("Hypersensitivity (1-10 %; <1 % "
                      "anaphylaxis)",
                      "Diarrhoea + C. difficile risk",
                      "Interstitial nephritis",
                      "Seizures (cefepime, imipenem in "
                      "renal failure)",
                      "Cytopenias"),
        contraindications=("Documented severe hypersensitivity "
                           "(varies by structure)",),
        monitoring=("Renal function + dose adjustment",
                    "Allergy history clarification"),
        cross_reference_molecule_names=(),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes="β-lactamase inhibitors (clavulanic acid, "
              "tazobactam, avibactam, vaborbactam) restore "
              "activity against ESBL / AmpC / KPC enzymes.",
    ),
    DrugClass(
        id="macrolides",
        name="Macrolide antibiotics",
        target_class="nucleic-acid",
        therapeutic_areas=("infectious",),
        mechanism="Bind 50S ribosomal subunit (23S rRNA) → "
                  "block peptide-chain elongation → "
                  "bacteriostatic.",
        molecular_target="Bacterial 50S ribosomal subunit",
        typical_agents=("Azithromycin",
                        "Clarithromycin",
                        "Erythromycin",
                        "Fidaxomicin (C. difficile)"),
        clinical_use=("Community-acquired pneumonia",
                      "Atypical pathogens (Mycoplasma, "
                      "Legionella, Chlamydophila)",
                      "STIs (azithromycin for chlamydia)",
                      "Pertussis treatment / prophylaxis",
                      "H. pylori (clarithromycin)"),
        side_effects=("GI motility (motilin agonism — "
                      "erythromycin)",
                      "QT prolongation (azithromycin, "
                      "clarithromycin)",
                      "Hepatotoxicity",
                      "CYP3A4 inhibition "
                      "(clarithromycin >> azithromycin)"),
        contraindications=("Macrolide allergy",
                           "Concurrent QT-prolonging drug + "
                           "risk factors"),
        monitoring=("ECG if QT-risk co-meds",
                    "LFTs if prolonged use"),
        cross_reference_molecule_names=(),
        cross_reference_enzyme_ids=("cyp3a4",),
        cross_reference_signaling_pathway_ids=(),
        notes="Azithromycin's tissue half-life (~ 68 h) "
              "allows a 5-day course or single 1 g dose for "
              "uncomplicated chlamydia.",
    ),
    DrugClass(
        id="fluoroquinolones",
        name="Fluoroquinolones",
        target_class="enzyme",
        therapeutic_areas=("infectious",),
        mechanism="Inhibit bacterial DNA gyrase (gram-) + "
                  "topoisomerase IV (gram+) → DNA damage + "
                  "bacterial death.",
        molecular_target="Bacterial gyrase (gyrA/gyrB) + "
                         "topo IV (parC/parE)",
        typical_agents=("Ciprofloxacin",
                        "Levofloxacin",
                        "Moxifloxacin",
                        "Delafloxacin"),
        clinical_use=("Complicated UTI / pyelonephritis",
                      "Pseudomonas pneumonia "
                      "(ciprofloxacin)",
                      "Atypical pneumonia "
                      "(levofloxacin, moxifloxacin)",
                      "Bone + joint infections",
                      "Anthrax post-exposure"),
        side_effects=("Tendinopathy + tendon rupture "
                      "(black-box; especially elderly + "
                      "concomitant steroids)",
                      "Aortic dissection / aneurysm signal",
                      "QT prolongation",
                      "Peripheral neuropathy",
                      "C. difficile",
                      "CNS effects (seizures)",
                      "Hypoglycaemia (esp. diabetic with "
                      "sulfonylurea)"),
        contraindications=("Pregnancy + paediatrics "
                           "(relative)",
                           "Myasthenia gravis",
                           "QT prolongation"),
        monitoring=("Tendon symptoms",
                    "Glucose if diabetic"),
        cross_reference_molecule_names=(),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes="FDA black-box warns against use for "
              "uncomplicated UTI, sinusitis, bronchitis "
              "when alternatives exist.",
    ),
    DrugClass(
        id="aminoglycosides",
        name="Aminoglycoside antibiotics",
        target_class="nucleic-acid",
        therapeutic_areas=("infectious",),
        mechanism="Bind 30S ribosomal subunit → "
                  "mistranslation + premature termination → "
                  "rapid bactericidal action against gram-"
                  "negatives + synergy with cell-wall agents.",
        molecular_target="Bacterial 30S ribosomal subunit",
        typical_agents=("Gentamicin",
                        "Tobramycin",
                        "Amikacin",
                        "Streptomycin (TB)"),
        clinical_use=("Severe gram-negative infections "
                      "(combined with β-lactam)",
                      "Endocarditis synergy",
                      "Tuberculosis (streptomycin / "
                      "amikacin)",
                      "Inhaled tobramycin for CF"),
        side_effects=("Nephrotoxicity (acute tubular "
                      "necrosis — reversible)",
                      "Ototoxicity — vestibular + cochlear "
                      "(often irreversible)",
                      "Neuromuscular blockade",
                      "Hypomagnesaemia"),
        contraindications=("Pre-existing renal impairment "
                           "(use cautiously)",
                           "Myasthenia gravis",
                           "Pregnancy"),
        monitoring=("Trough levels (avoid accumulation)",
                    "Daily creatinine",
                    "Audiometry on prolonged courses"),
        cross_reference_molecule_names=(),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes="Once-daily extended-interval dosing exploits "
              "post-antibiotic effect + reduces nephro / "
              "ototoxicity vs traditional q8h dosing.",
    ),
    DrugClass(
        id="hiv-pis",
        name="HIV protease inhibitors",
        target_class="enzyme",
        therapeutic_areas=("infectious",),
        mechanism="Competitive inhibition of HIV-1 protease "
                  "→ blocks Gag-Pol polyprotein cleavage → "
                  "non-infectious immature virions.",
        molecular_target="HIV-1 protease (aspartic homodimer)",
        typical_agents=("Darunavir / cobicistat",
                        "Atazanavir / ritonavir",
                        "Lopinavir / ritonavir",
                        "Ritonavir (also used as "
                        "pharmacokinetic booster via CYP3A4 "
                        "inhibition)"),
        clinical_use=("HIV-1 treatment (combination ART)",
                      "Post-exposure prophylaxis (some "
                      "regimens)"),
        side_effects=("Hyperlipidaemia",
                      "Hyperglycaemia",
                      "Lipodystrophy",
                      "GI upset",
                      "Atazanavir → indirect "
                      "hyperbilirubinaemia",
                      "Many drug interactions via CYP3A4"),
        contraindications=("Concurrent strong CYP3A4 "
                           "substrates with narrow TI "
                           "(midazolam, simvastatin)",),
        monitoring=("Viral load + CD4",
                    "Lipids + glucose",
                    "LFTs"),
        cross_reference_molecule_names=("Ritonavir",
                                        "Darunavir",
                                        "Lopinavir"),
        cross_reference_enzyme_ids=("hiv-protease",
                                    "cyp3a4"),
        cross_reference_signaling_pathway_ids=(),
        notes="Modern ART regimens have largely shifted to "
              "integrase strand-transfer inhibitors (INSTIs) "
              "as first-line; PIs reserved for resistance + "
              "pregnancy.",
    ),
    DrugClass(
        id="nrtis",
        name="Nucleoside reverse transcriptase inhibitors "
             "(NRTIs)",
        target_class="nucleic-acid",
        therapeutic_areas=("infectious",),
        mechanism="Phosphorylated to triphosphates → "
                  "incorporated into nascent viral DNA → "
                  "chain termination (lack 3'-OH).",
        molecular_target="HIV / HBV reverse transcriptase",
        typical_agents=("Tenofovir disoproxil + tenofovir "
                        "alafenamide (TDF / TAF)",
                        "Emtricitabine (FTC)",
                        "Abacavir",
                        "Lamivudine (3TC)",
                        "Zidovudine (AZT — historical)"),
        clinical_use=("HIV-1 treatment (backbone of ART)",
                      "Hepatitis B (TDF / TAF + FTC / 3TC)",
                      "HIV pre-exposure prophylaxis (PrEP)"),
        side_effects=("Renal dysfunction (TDF > TAF)",
                      "Bone density loss (TDF)",
                      "Lactic acidosis + steatosis (rare; "
                      "older agents)",
                      "Abacavir hypersensitivity "
                      "(HLA-B*5701)"),
        contraindications=("Abacavir in HLA-B*5701 carriers",
                           "Severe renal impairment (TDF)"),
        monitoring=("Renal function + bone density (TDF)",
                    "HLA-B*5701 testing before abacavir",
                    "HBV reactivation if discontinuing in "
                    "co-infected patients"),
        cross_reference_molecule_names=(),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes="HIV PrEP with TDF / FTC reduces sexual "
              "acquisition by > 90 %.",
    ),

    # ============================================================
    # Oncology
    # ============================================================
    DrugClass(
        id="platinum-chemotherapy",
        name="Platinum chemotherapy",
        target_class="nucleic-acid",
        therapeutic_areas=("oncology",),
        mechanism="DNA cross-linker — forms intra- + "
                  "inter-strand adducts at GpG → DNA "
                  "damage → apoptosis.",
        molecular_target="DNA (covalent adducts)",
        typical_agents=("Cisplatin",
                        "Carboplatin",
                        "Oxaliplatin"),
        clinical_use=("Testicular cancer (cisplatin — "
                      "curative)",
                      "Ovarian cancer (carboplatin)",
                      "Lung cancer",
                      "Colorectal cancer (oxaliplatin)",
                      "Head + neck cancer"),
        side_effects=("Nephrotoxicity (cisplatin >> "
                      "carboplatin)",
                      "Ototoxicity (cisplatin)",
                      "Peripheral neuropathy "
                      "(oxaliplatin: cold-induced acute; "
                      "cisplatin: cumulative)",
                      "Myelosuppression "
                      "(carboplatin > cisplatin)",
                      "Severe nausea + vomiting",
                      "Magnesium wasting"),
        contraindications=("Severe renal impairment "
                           "(cisplatin)",
                           "Pre-existing severe neuropathy"),
        monitoring=("Renal function + electrolytes "
                    "(esp. Mg²⁺)",
                    "Audiometry (cisplatin)",
                    "Neuropathy assessment",
                    "CBC"),
        cross_reference_molecule_names=(),
        cross_reference_enzyme_ids=("p-glycoprotein",),
        # ↑ MDR efflux can mediate resistance
        cross_reference_signaling_pathway_ids=("p53",
                                               "intrinsic-apoptosis"),
        notes="Cisplatin discovered serendipitously by "
              "Rosenberg (1965) — cured testicular cancer + "
              "transformed it from uniformly fatal to > 95 % "
              "curable.",
    ),
    DrugClass(
        id="taxanes",
        name="Taxane chemotherapy",
        target_class="nucleic-acid",
        therapeutic_areas=("oncology",),
        mechanism="Bind β-tubulin → stabilise microtubules "
                  "→ block mitotic spindle disassembly → "
                  "G2/M arrest → apoptosis.",
        molecular_target="β-tubulin (microtubule "
                         "stabiliser)",
        typical_agents=("Paclitaxel",
                        "Docetaxel",
                        "Cabazitaxel",
                        "Nab-paclitaxel"),
        clinical_use=("Breast cancer (adjuvant + metastatic)",
                      "Ovarian cancer",
                      "Non-small-cell lung cancer",
                      "Prostate cancer (docetaxel, "
                      "cabazitaxel)"),
        side_effects=("Hypersensitivity reactions "
                      "(Cremophor vehicle for paclitaxel)",
                      "Myelosuppression",
                      "Peripheral neuropathy",
                      "Fluid retention (docetaxel)",
                      "Alopecia",
                      "Mucositis"),
        contraindications=("Severe hypersensitivity to "
                           "taxane / vehicle",
                           "Severe neutropenia"),
        monitoring=("CBC",
                    "Neuropathy",
                    "Pre-medication for hypersensitivity"),
        cross_reference_molecule_names=("Paclitaxel",),
        cross_reference_enzyme_ids=("p-glycoprotein",),
        cross_reference_signaling_pathway_ids=("p53",
                                               "intrinsic-apoptosis"),
        notes="Original paclitaxel sourced from Pacific yew "
              "bark (limited supply); modern semi-synthetic "
              "production from yew needles via baccatin III.",
    ),
    DrugClass(
        id="kinase-inhibitors",
        name="Tyrosine-kinase inhibitors (TKIs)",
        target_class="RTK",
        therapeutic_areas=("oncology",),
        mechanism="Compete with ATP at the kinase active "
                  "site → block phosphorylation of "
                  "downstream signalling proteins.",
        molecular_target="Specific oncogenic kinase (BCR-"
                         "ABL, EGFR, ALK, ROS1, BRAF, HER2, "
                         "JAK, BTK, etc.)",
        typical_agents=("Imatinib (BCR-ABL — CML)",
                        "Osimertinib (EGFR T790M)",
                        "Crizotinib + alectinib (ALK)",
                        "Trastuzumab deruxtecan (HER2 — "
                        "ADC)",
                        "Ibrutinib (BTK)",
                        "Sotorasib (KRAS G12C)"),
        clinical_use=("CML (imatinib first-line)",
                      "EGFR-mutant NSCLC",
                      "ALK / ROS1-rearranged NSCLC",
                      "HER2+ breast cancer",
                      "CLL + mantle-cell lymphoma "
                      "(ibrutinib)",
                      "Melanoma (BRAF + MEK inhibitor "
                      "combos)"),
        side_effects=("Class-specific: rash, diarrhoea "
                      "(EGFR)",
                      "QT prolongation",
                      "Hypothyroidism (sunitinib, "
                      "sorafenib)",
                      "Cardiotoxicity (trastuzumab)",
                      "Hepatotoxicity",
                      "Pneumonitis (osimertinib, "
                      "crizotinib)"),
        contraindications=("Severe hepatic impairment "
                           "(varies)",
                           "QT-risk drug interactions",
                           "Pregnancy (most)"),
        monitoring=("Class-specific tox screening",
                    "Drug levels (rare)",
                    "Resistance mutation testing on "
                    "progression"),
        cross_reference_molecule_names=("Gefitinib",
                                        "Erlotinib",
                                        "Osimertinib",
                                        "Sotorasib",
                                        "Vemurafenib",
                                        "Trametinib"),
        cross_reference_enzyme_ids=("egfr-tk",),
        cross_reference_signaling_pathway_ids=("egfr-ras-raf",
                                               "mapk-erk",
                                               "pi3k-akt-mtor"),
        notes="Imatinib (2001) was the first targeted "
              "cancer therapy approved + transformed CML "
              "into a chronic disease.",
    ),
    DrugClass(
        id="checkpoint-inhibitors",
        name="Immune-checkpoint inhibitors (anti-PD-1 / "
             "anti-PD-L1 / anti-CTLA-4)",
        target_class="antibody-target",
        therapeutic_areas=("oncology",),
        mechanism="Monoclonal antibodies blocking PD-1 / "
                  "PD-L1 (release T-cell exhaustion) or "
                  "CTLA-4 (release lymphocyte priming "
                  "checkpoint) → restored anti-tumour "
                  "immunity.",
        molecular_target="PD-1, PD-L1, or CTLA-4 surface "
                         "receptors",
        typical_agents=("Pembrolizumab (anti-PD-1)",
                        "Nivolumab (anti-PD-1)",
                        "Atezolizumab (anti-PD-L1)",
                        "Durvalumab (anti-PD-L1)",
                        "Ipilimumab (anti-CTLA-4)"),
        clinical_use=("Melanoma",
                      "NSCLC",
                      "Renal cell carcinoma",
                      "Bladder cancer",
                      "MSI-high colorectal cancer",
                      "Hodgkin lymphoma",
                      "Head + neck cancer"),
        side_effects=("Immune-related adverse events "
                      "(irAEs): pneumonitis, colitis, "
                      "hepatitis, endocrinopathies "
                      "(thyroiditis, hypophysitis, "
                      "adrenalitis, T1DM), dermatitis, "
                      "myocarditis (rare but life-"
                      "threatening)",
                      "Infusion reactions"),
        contraindications=("Active autoimmune disease "
                           "(relative)",
                           "Solid-organ transplant "
                           "(rejection risk)"),
        monitoring=("Endocrine panel (TSH + cortisol)",
                    "LFTs + creatinine",
                    "Symptom screen for irAEs at every "
                    "visit",
                    "Early steroid taper for severe "
                    "irAEs"),
        cross_reference_molecule_names=(),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=("tcr",
                                               "jak-stat"),
        notes="2018 Nobel (Allison + Honjo) for PD-1 / "
              "CTLA-4 discovery.  Combination ipilimumab + "
              "nivolumab gives higher response rates but "
              "much higher irAE incidence.",
    ),
    DrugClass(
        id="anti-cd20",
        name="Anti-CD20 monoclonal antibodies",
        target_class="antibody-target",
        therapeutic_areas=("oncology",
                           "inflammation-immunology"),
        mechanism="Bind CD20 on B cells → "
                  "complement-dependent + ADCC + direct "
                  "apoptosis induction → B-cell depletion.",
        molecular_target="CD20 (membrane B-cell antigen)",
        typical_agents=("Rituximab",
                        "Obinutuzumab",
                        "Ofatumumab",
                        "Ocrelizumab"),
        clinical_use=("CD20+ B-cell lymphomas (NHL, CLL)",
                      "Rheumatoid arthritis",
                      "Granulomatosis with polyangiitis "
                      "(GPA / MPA)",
                      "Multiple sclerosis (ocrelizumab)",
                      "Pemphigus vulgaris"),
        side_effects=("Infusion reactions (cytokine "
                      "release; pre-medicate)",
                      "Hepatitis B reactivation (screen + "
                      "treat)",
                      "Late-onset neutropenia",
                      "PML (rare; rituximab in immune-"
                      "compromised hosts)",
                      "Hypogammaglobulinaemia (chronic "
                      "use)"),
        contraindications=("Active severe infection",
                           "Untreated chronic HBV"),
        monitoring=("HBV serology before start",
                    "CBC + Ig levels long-term",
                    "Vaccination optimisation pre-therapy"),
        cross_reference_molecule_names=(),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes="Rituximab (1997) was the first FDA-approved "
              "monoclonal antibody for cancer + spawned "
              "the modern mAb-therapeutic era.",
    ),
]
