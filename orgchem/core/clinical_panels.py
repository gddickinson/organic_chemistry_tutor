"""Phase 37b (round 137) — clinical-chemistry lab-panel catalogue.

Headless reference data for the *Tools → Clinical lab panels…*
dialog.  Three primary panels — Basic Metabolic Panel (BMP),
Comprehensive Metabolic Panel (CMP), Lipid Panel — plus a few
commonly bundled "extended" tests (HbA1c, TSH, free T4, vitamin
D 25-OH).

Each :class:`LabAnalyte` carries the name (long + abbreviation),
its category (electrolyte / kidney / liver / lipid / metabolic /
hormone / vitamin), units, a normal-range string, the clinical
significance, and interpretation notes (typical abnormal patterns,
common confounders).

Each :class:`LabPanel` carries the panel's clinical purpose, the
sample type + procedure, fasting requirements, and the list of
:class:`LabAnalyte` objects that the panel measures.  CMP shares
its first 8 analytes with BMP — they're literally the same
:class:`LabAnalyte` instances since the dataclass is frozen.

This is **reference data for teaching**, not a clinical
decision-support tool.  Normal-range values are
literature-typical (US adult, fasting where applicable); real
labs publish their own reference ranges with method-specific
calibration.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass(frozen=True)
class LabAnalyte:
    id: str
    name: str
    abbreviation: str
    category: str          # "electrolyte" / "kidney" / "liver" / "lipid" /
                           # "metabolic" / "hormone" / "vitamin"
    units: str
    normal_range: str
    clinical_significance: str
    notes: str = ""


@dataclass(frozen=True)
class LabPanel:
    id: str
    name: str
    short_name: str
    purpose: str
    sample: str
    procedure: str
    fasting: str            # e.g. "8-12 h" / "not required"
    analytes: List[LabAnalyte] = field(default_factory=list)
    notes: str = ""


VALID_CATEGORIES: tuple = (
    "metabolic", "electrolyte", "kidney",
    "liver", "lipid", "hormone", "vitamin",
)


# ------------------------------------------------------------------
# Analyte definitions (shared across panels)
# ------------------------------------------------------------------

# ---- BMP analytes (also reused by CMP) ---------------------------

GLUCOSE = LabAnalyte(
    id="glucose",
    name="Glucose",
    abbreviation="GLU",
    category="metabolic",
    units="mg/dL",
    normal_range="70-99 (fasting); <140 (2-h post-prandial)",
    clinical_significance=(
        "Blood-sugar level — the primary screen for diabetes "
        "and its acute complications.  Hyperglycaemia "
        "(>126 fasting on two separate days = diabetes); "
        "hypoglycaemia (<70 in a fasting adult) is symptomatic "
        "and dangerous below ~55."
    ),
    notes=(
        "Fasting for 8 h is required for the diagnostic "
        "threshold to apply; random glucose ≥ 200 mg/dL with "
        "symptoms is also diagnostic.  Stress, steroids, and "
        "many endocrine disorders also raise glucose; "
        "haemolysis falsely lowers the measured value."
    ),
)

CALCIUM = LabAnalyte(
    id="calcium",
    name="Calcium (total)",
    abbreviation="Ca",
    category="electrolyte",
    units="mg/dL",
    normal_range="8.6-10.3",
    clinical_significance=(
        "Total serum calcium — important for nerve "
        "transmission, muscle contraction, cardiac rhythm, "
        "and bone mineralisation.  Hypercalcaemia common "
        "causes: hyperparathyroidism, malignancy, vitamin-D "
        "toxicity.  Hypocalcaemia: hypoparathyroidism, "
        "vitamin-D deficiency, chronic kidney disease."
    ),
    notes=(
        "Total Ca is bound ~50 % to albumin — correct for "
        "albumin (add 0.8 mg/dL per 1 g/dL the albumin is "
        "below 4.0) or order ionised calcium directly when "
        "a precise free fraction is needed."
    ),
)

SODIUM = LabAnalyte(
    id="sodium",
    name="Sodium",
    abbreviation="Na",
    category="electrolyte",
    units="mEq/L",
    normal_range="136-145",
    clinical_significance=(
        "Major extracellular cation — the primary determinant "
        "of plasma osmolality + extracellular fluid volume.  "
        "Hyponatraemia (most common electrolyte abnormality "
        "in hospitalised patients): SIADH, heart failure, "
        "cirrhosis, thiazide diuretics.  Hypernatraemia: "
        "free-water deficit (dehydration, diabetes insipidus)."
    ),
    notes=(
        "Pseudo-hyponatraemia (lab artefact) can occur with "
        "very high triglycerides or paraproteins.  Acute Na "
        "changes (>0.5 mEq/L per hour) are dangerous — fix "
        "slowly to avoid central pontine myelinolysis."
    ),
)

POTASSIUM = LabAnalyte(
    id="potassium",
    name="Potassium",
    abbreviation="K",
    category="electrolyte",
    units="mEq/L",
    normal_range="3.5-5.0",
    clinical_significance=(
        "Major intracellular cation — critical for "
        "cardiac + skeletal muscle excitability.  "
        "Hyperkalaemia (common: renal failure, ACE "
        "inhibitors, K-sparing diuretics, rhabdomyolysis) "
        "causes peaked T waves → wide QRS → fatal "
        "arrhythmia.  Hypokalaemia (loop / thiazide "
        "diuretics, GI losses) causes weakness + "
        "U waves + arrhythmia."
    ),
    notes=(
        "Haemolysis from a difficult venipuncture falsely "
        "raises K — repeat the draw before treating an "
        "isolated mild hyperkalaemia.  Prolonged "
        "tourniquet + fist-clenching also raise K."
    ),
)

CHLORIDE = LabAnalyte(
    id="chloride",
    name="Chloride",
    abbreviation="Cl",
    category="electrolyte",
    units="mEq/L",
    normal_range="98-107",
    clinical_significance=(
        "Major extracellular anion — tracks Na in most "
        "states.  Useful primarily for the anion gap "
        "calculation: AG = Na − (Cl + HCO₃), normal 8-12.  "
        "High AG metabolic acidosis = MUDPILES (methanol, "
        "uraemia, DKA, paraldehyde, isoniazid, lactate, "
        "ethylene glycol, salicylates)."
    ),
    notes=(
        "Hyperchloraemic non-AG acidosis is the classic "
        "result of large-volume normal saline resuscitation "
        "(0.9 % NaCl = 154 mEq/L Cl, much higher than "
        "plasma)."
    ),
)

BICARBONATE = LabAnalyte(
    id="bicarbonate",
    name="Bicarbonate (CO₂)",
    abbreviation="HCO₃ / CO₂",
    category="electrolyte",
    units="mEq/L",
    normal_range="22-29",
    clinical_significance=(
        "Total CO₂ = HCO₃ + dissolved CO₂; primary marker "
        "of metabolic acid-base status.  Low = metabolic "
        "acidosis (DKA, lactic acidosis, renal tubular "
        "acidosis, diarrhoea).  High = metabolic alkalosis "
        "(vomiting, diuretics, hyperaldosteronism)."
    ),
    notes=(
        "Reported as 'CO₂' on most chemistry panels but the "
        "value is essentially HCO₃ in adult plasma at "
        "physiological pH.  Pair with arterial blood-gas "
        "pH + pCO₂ for full acid-base interpretation."
    ),
)

BUN = LabAnalyte(
    id="bun",
    name="Blood Urea Nitrogen",
    abbreviation="BUN",
    category="kidney",
    units="mg/dL",
    normal_range="7-20",
    clinical_significance=(
        "Urea (byproduct of hepatic protein metabolism) "
        "filtered by glomeruli + variably reabsorbed by "
        "tubules.  Elevated in renal dysfunction, "
        "dehydration (pre-renal), GI bleed (digested blood "
        "= protein load), high-protein diet, catabolic "
        "states."
    ),
    notes=(
        "BUN/Creatinine ratio: >20:1 suggests pre-renal "
        "(dehydration, GI bleed); 10-15:1 normal; <10:1 "
        "suggests intrinsic renal disease or low protein "
        "intake / liver failure."
    ),
)

CREATININE = LabAnalyte(
    id="creatinine",
    name="Creatinine",
    abbreviation="Cr",
    category="kidney",
    units="mg/dL",
    normal_range="0.6-1.3 (M); 0.5-1.1 (F)",
    clinical_significance=(
        "Byproduct of muscle creatine breakdown — "
        "produced at a near-constant daily rate, freely "
        "filtered, minimally secreted.  The standard "
        "marker of glomerular filtration rate (GFR).  "
        "Doubling of Cr ≈ halving of GFR."
    ),
    notes=(
        "Affected by muscle mass (low in elderly women + "
        "amputees, high in body-builders), so eGFR "
        "calculations (CKD-EPI, MDRD) correct for age + "
        "sex.  Trimethoprim + cimetidine raise serum Cr "
        "without changing true GFR (block tubular "
        "secretion)."
    ),
)

# ---- CMP-only (additional liver / protein analytes) -------------

ALT = LabAnalyte(
    id="alt",
    name="Alanine aminotransferase",
    abbreviation="ALT",
    category="liver",
    units="U/L",
    normal_range="7-56",
    clinical_significance=(
        "Hepatocellular enzyme — the most specific routine "
        "marker of liver-cell injury.  Elevated in viral "
        "hepatitis, drug-induced liver injury (especially "
        "acetaminophen overdose: ALT often >1000), NAFLD, "
        "ischaemic hepatitis."
    ),
    notes=(
        "ALT > AST in most chronic liver disease.  Reverse "
        "(AST > ALT, ratio > 2) is the alcoholic-hepatitis "
        "fingerprint.  Mild persistent elevation (40-100) "
        "with elevated BMI = NAFLD until proven otherwise."
    ),
)

AST = LabAnalyte(
    id="ast",
    name="Aspartate aminotransferase",
    abbreviation="AST",
    category="liver",
    units="U/L",
    normal_range="8-48",
    clinical_significance=(
        "Hepatocellular + skeletal-muscle + cardiac enzyme.  "
        "Less liver-specific than ALT — also elevated in "
        "rhabdomyolysis, MI (historical), haemolysis."
    ),
    notes=(
        "AST/ALT ratio > 2 with elevated GGT suggests "
        "alcoholic liver disease.  Marked elevation (>1000) "
        "with low ALT suggests muscle-source (CK should be "
        "checked)."
    ),
)

ALP = LabAnalyte(
    id="alp",
    name="Alkaline phosphatase",
    abbreviation="ALP",
    category="liver",
    units="U/L",
    normal_range="44-147",
    clinical_significance=(
        "Hepatic biliary enzyme + bone osteoblast enzyme.  "
        "Elevated in cholestasis (biliary obstruction, "
        "primary biliary cholangitis, drug-induced "
        "cholestasis) AND in bone activity (Paget's "
        "disease, healing fracture, growing children, "
        "metastatic bone disease)."
    ),
    notes=(
        "Pair with GGT to distinguish liver vs bone source: "
        "GGT elevated → liver; GGT normal → bone.  "
        "Pregnancy raises ALP (placental isoform) — "
        "physiological, not pathological."
    ),
)

BILIRUBIN_TOTAL = LabAnalyte(
    id="bilirubin_total",
    name="Total bilirubin",
    abbreviation="T-Bili",
    category="liver",
    units="mg/dL",
    normal_range="0.1-1.2",
    clinical_significance=(
        "End-product of haem catabolism.  Elevated in "
        "haemolysis (unconjugated), hepatocellular injury "
        "(mixed), and cholestasis (conjugated).  Visible "
        "jaundice usually appears at total bilirubin "
        "> 2.5-3.0 mg/dL."
    ),
    notes=(
        "Direct (conjugated) vs indirect (unconjugated) "
        "fractionation distinguishes pre-hepatic / hepatic / "
        "post-hepatic causes.  Gilbert syndrome (benign "
        "indirect hyperbilirubinaemia from UGT1A1 "
        "polymorphism) affects ~5 % of the population."
    ),
)

ALBUMIN = LabAnalyte(
    id="albumin",
    name="Albumin",
    abbreviation="ALB",
    category="liver",
    units="g/dL",
    normal_range="3.5-5.0",
    clinical_significance=(
        "Major plasma protein — synthesised by the liver, "
        "long half-life (~21 days).  Low albumin reflects "
        "chronic liver disease, nephrotic syndrome (urinary "
        "loss), malnutrition, or chronic inflammation "
        "(negative acute-phase reactant)."
    ),
    notes=(
        "Half-life makes albumin a poor acute marker — "
        "won't move in days.  Pre-albumin (transthyretin, "
        "half-life ~2 days) is the better short-term "
        "nutritional marker."
    ),
)

TOTAL_PROTEIN = LabAnalyte(
    id="total_protein",
    name="Total protein",
    abbreviation="TP",
    category="liver",
    units="g/dL",
    normal_range="6.0-8.3",
    clinical_significance=(
        "Sum of albumin + globulins.  Elevated total "
        "protein with normal albumin → high globulin "
        "(multiple myeloma, chronic infection, "
        "autoimmune disease — confirm with serum protein "
        "electrophoresis)."
    ),
    notes=(
        "Calculated A:G ratio (albumin / globulins) is "
        "normally 1.0-2.5; reversed ratio (<1) suggests "
        "either low albumin or high globulin, both "
        "pathological in different ways."
    ),
)

# ---- Lipid Panel analytes ---------------------------------------

TOTAL_CHOLESTEROL = LabAnalyte(
    id="total_chol",
    name="Total cholesterol",
    abbreviation="TC",
    category="lipid",
    units="mg/dL",
    normal_range="<200 desirable; 200-239 borderline; "
                 "≥240 high",
    clinical_significance=(
        "Sum of cholesterol in all lipoprotein fractions.  "
        "Cardiovascular-risk screen; the workhorse "
        "first-line lipid measure."
    ),
    notes=(
        "Total cholesterol alone is a coarse risk marker — "
        "the LDL / HDL fractions matter more for individual "
        "risk stratification."
    ),
)

LDL_CHOLESTEROL = LabAnalyte(
    id="ldl_chol",
    name="LDL cholesterol",
    abbreviation="LDL-C",
    category="lipid",
    units="mg/dL",
    normal_range="<100 optimal; 100-129 near optimal; "
                 "130-159 borderline; 160-189 high; "
                 "≥190 very high",
    clinical_significance=(
        "'Bad' cholesterol — atherogenic.  The primary "
        "target for statin therapy.  ASCVD-risk "
        "calculation drives the LDL goal: <70 mg/dL for "
        "very high-risk patients (post-MI, recurrent "
        "events)."
    ),
    notes=(
        "Friedewald-calculated when triglycerides < 400; "
        "directly measured (LDL-D) preferred when "
        "triglycerides are elevated.  Non-HDL = TC - HDL "
        "is a useful alternative when LDL is unreliable."
    ),
)

HDL_CHOLESTEROL = LabAnalyte(
    id="hdl_chol",
    name="HDL cholesterol",
    abbreviation="HDL-C",
    category="lipid",
    units="mg/dL",
    normal_range=">40 (M), >50 (F) protective; "
                 ">60 strongly protective",
    clinical_significance=(
        "'Good' cholesterol — reverse cholesterol "
        "transport from periphery back to liver.  Inverse "
        "relationship with cardiovascular risk; HDL is a "
        "negative risk factor in the Framingham score."
    ),
    notes=(
        "Pharmacologically raising HDL (CETP inhibitors, "
        "niacin) does NOT reduce CV events in trials — HDL "
        "is a marker, not a modifiable target."
    ),
)

TRIGLYCERIDES = LabAnalyte(
    id="triglycerides",
    name="Triglycerides",
    abbreviation="TG",
    category="lipid",
    units="mg/dL",
    normal_range="<150 normal; 150-199 borderline; "
                 "200-499 high; ≥500 very high",
    clinical_significance=(
        "Serum triglycerides — primarily from chylomicrons "
        "(post-prandial) + VLDL.  Very high (>500 mg/dL) "
        "carries pancreatitis risk; severe (>1000) is an "
        "indication for fibrate / omega-3 therapy."
    ),
    notes=(
        "Fasting (12 h) for accurate baseline.  "
        "Non-fasting elevation up to 200 is acceptable in "
        "most adults.  Alcohol + simple sugars + obesity "
        "are the main lifestyle drivers."
    ),
)

# ---- Extended / commonly bundled tests --------------------------

HBA1C = LabAnalyte(
    id="hba1c",
    name="Haemoglobin A1c",
    abbreviation="HbA1c",
    category="metabolic",
    units="%",
    normal_range="<5.7 normal; 5.7-6.4 prediabetes; "
                 "≥6.5 diabetes",
    clinical_significance=(
        "Fraction of haemoglobin with non-enzymatic "
        "glycation at the N-terminal valine of the β-chain — "
        "reflects average plasma glucose over the prior "
        "~3 months (RBC lifespan).  The standard long-term "
        "diabetes-control marker."
    ),
    notes=(
        "Falsely low in conditions that shorten RBC "
        "lifespan (haemolytic anaemia, recent transfusion); "
        "falsely high in iron-deficiency anaemia (longer "
        "RBC survival).  Conversion: HbA1c % × 28.7 - 46.7 "
        "≈ average glucose mg/dL."
    ),
)

TSH = LabAnalyte(
    id="tsh",
    name="Thyroid-stimulating hormone",
    abbreviation="TSH",
    category="hormone",
    units="mU/L",
    normal_range="0.4-4.0",
    clinical_significance=(
        "Pituitary anterior-lobe hormone that stimulates "
        "thyroid T4 / T3 production.  Low TSH (suppressed) "
        "= hyperthyroidism; high TSH = primary "
        "hypothyroidism (negative feedback failure to shut "
        "off the pituitary)."
    ),
    notes=(
        "TSH is the single best screening test for thyroid "
        "function — much more sensitive than free T4 alone.  "
        "Subclinical hypothyroidism (TSH 5-10 with normal "
        "free T4) is common and often watched, not treated."
    ),
)

FREE_T4 = LabAnalyte(
    id="free_t4",
    name="Free thyroxine",
    abbreviation="Free T4",
    category="hormone",
    units="ng/dL",
    normal_range="0.8-1.8",
    clinical_significance=(
        "Free (unbound) T4 — the bioactive thyroid "
        "hormone that crosses cell membranes.  Used to "
        "confirm thyroid status when TSH is abnormal or "
        "when central (pituitary / hypothalamic) thyroid "
        "disease is suspected (TSH unreliable)."
    ),
    notes=(
        "Total T4 is mostly bound to TBG and varies with "
        "TBG levels (oestrogen, pregnancy raise TBG).  "
        "Free T4 is the modern standard; rT3 (reverse T3) "
        "is rarely needed clinically."
    ),
)

VITAMIN_D = LabAnalyte(
    id="vitamin_d",
    name="25-hydroxyvitamin D",
    abbreviation="25(OH)D",
    category="vitamin",
    units="ng/mL",
    normal_range="30-100 sufficient; 20-29 insufficient; "
                 "<20 deficient",
    clinical_significance=(
        "Major circulating vitamin-D metabolite + the best "
        "indicator of body stores.  Deficiency is common "
        "in northern latitudes / dark-skinned individuals / "
        "elderly / institutionalised patients.  Severe "
        "deficiency causes osteomalacia (adults) and "
        "rickets (children)."
    ),
    notes=(
        "1,25-(OH)₂D (calcitriol) is the active form but "
        "has a short half-life and tightly regulated "
        "levels — not useful as a stores marker.  "
        "Optimal levels for non-skeletal benefits "
        "(immune / cardiovascular) are debated."
    ),
)


# ------------------------------------------------------------------
# Panel definitions
# ------------------------------------------------------------------

_BMP_ANALYTES: List[LabAnalyte] = [
    GLUCOSE, CALCIUM, SODIUM, POTASSIUM,
    CHLORIDE, BICARBONATE, BUN, CREATININE,
]

_CMP_ANALYTES: List[LabAnalyte] = list(_BMP_ANALYTES) + [
    ALT, AST, ALP, BILIRUBIN_TOTAL, ALBUMIN, TOTAL_PROTEIN,
]

_LIPID_ANALYTES: List[LabAnalyte] = [
    TOTAL_CHOLESTEROL, LDL_CHOLESTEROL,
    HDL_CHOLESTEROL, TRIGLYCERIDES,
]

_DIABETES_FOLLOWUP: List[LabAnalyte] = [HBA1C, GLUCOSE]

_THYROID_PANEL: List[LabAnalyte] = [TSH, FREE_T4]

_VITAMIN_D_PANEL: List[LabAnalyte] = [VITAMIN_D, CALCIUM]


_PANELS: List[LabPanel] = [
    LabPanel(
        id="bmp",
        name="Basic Metabolic Panel",
        short_name="BMP",
        purpose=(
            "Screen for diabetes, kidney disease, "
            "electrolyte / acid-base disorders.  Routine "
            "outpatient + admission lab work-up."
        ),
        sample="Venous blood, serum or plasma",
        procedure=(
            "Phlebotomy from an antecubital vein into a "
            "lithium-heparin or SST tube; centrifuge; run "
            "on a chemistry analyzer (e.g. Roche cobas, "
            "Siemens Atellica).  Total turnaround usually "
            "< 1 hour."
        ),
        fasting="8-12 h preferred for glucose interpretation",
        analytes=_BMP_ANALYTES,
        notes=(
            "Sometimes called Chem 7 (8 analytes total in US "
            "practice — historically excluded calcium).  "
            "Bedside iSTAT cartridges report a similar "
            "panel from a fingerstick in ~2 min."
        ),
    ),
    LabPanel(
        id="cmp",
        name="Comprehensive Metabolic Panel",
        short_name="CMP",
        purpose=(
            "BMP + liver-function + protein panel.  "
            "Standard for general medical evaluation, "
            "monitoring chronic disease + drug toxicity."
        ),
        sample="Venous blood, serum",
        procedure=(
            "Same phlebotomy / processing as BMP; the "
            "CMP analytes ride on the same sample tube "
            "and chemistry analyzer."
        ),
        fasting="8-12 h preferred",
        analytes=_CMP_ANALYTES,
        notes=(
            "14 analytes total (sometimes called Chem 14).  "
            "Strict cost-conscious lab algorithms reflex "
            "from BMP to CMP only when liver evaluation "
            "is needed."
        ),
    ),
    LabPanel(
        id="lipid",
        name="Lipid Panel",
        short_name="Lipid",
        purpose=(
            "Cardiovascular-risk screening + monitoring "
            "lipid-lowering therapy (statin, ezetimibe, "
            "PCSK9 inhibitor).  Recommended at age 40+ in "
            "most guidelines and earlier with risk "
            "factors / family history."
        ),
        sample="Venous blood, serum",
        procedure=(
            "Same phlebotomy / processing as BMP.  "
            "Friedewald-calculated LDL = TC - HDL - TG/5 "
            "when TG < 400; direct LDL when TG ≥ 400."
        ),
        fasting=(
            "12 h preferred for accurate triglycerides + "
            "Friedewald LDL; non-fasting acceptable for "
            "screening per 2018 AHA / ACC guidelines."
        ),
        analytes=_LIPID_ANALYTES,
        notes=(
            "Non-HDL cholesterol (TC - HDL) is increasingly "
            "used as a primary target — captures all "
            "atherogenic apoB-containing lipoproteins, "
            "including remnant particles that direct LDL "
            "misses."
        ),
    ),
    LabPanel(
        id="diabetes_followup",
        name="Diabetes follow-up",
        short_name="DM follow-up",
        purpose=(
            "Long-term glycaemic-control monitoring in "
            "established diabetes (HbA1c target usually "
            "<7.0 % for most non-pregnant adults)."
        ),
        sample="Venous blood, EDTA tube for HbA1c",
        procedure=(
            "HbA1c by HPLC, immunoassay, or boronate-"
            "affinity chromatography.  Glucose may be "
            "fasting / random / 2-h post-prandial as the "
            "clinical question dictates."
        ),
        fasting="Not required for HbA1c",
        analytes=_DIABETES_FOLLOWUP,
        notes=(
            "ADA recommends HbA1c every 6 months in "
            "stable patients, every 3 months when "
            "treatment changes or control is poor."
        ),
    ),
    LabPanel(
        id="vitamin_d",
        name="Vitamin D screening",
        short_name="Vit D",
        purpose=(
            "Diagnose + monitor vitamin-D status (skeletal "
            "+ extra-skeletal effects).  Calcium is paired "
            "to flag hypercalcaemia from over-supplementation "
            "or PTH-driven secondary effects."
        ),
        sample="Venous blood, serum",
        procedure=(
            "25-(OH)D measured by LC-MS/MS or "
            "immunoassay; calcium on the chemistry "
            "analyzer alongside."
        ),
        fasting="Not required",
        analytes=_VITAMIN_D_PANEL,
        notes=(
            "Routine population screening NOT recommended "
            "(USPSTF I-statement); test in symptomatic "
            "patients (osteomalacia, bone pain, malabsorption, "
            "CKD, on chronic steroids / antiepileptics)."
        ),
    ),
    LabPanel(
        id="thyroid",
        name="Thyroid function panel",
        short_name="Thyroid",
        purpose=(
            "Screen + diagnose thyroid disorders "
            "(hyperthyroidism / hypothyroidism); monitor "
            "levothyroxine therapy."
        ),
        sample="Venous blood, serum",
        procedure=(
            "TSH measured first as the screening test; "
            "free T4 added when TSH is abnormal or central "
            "thyroid disease is suspected."
        ),
        fasting="Not required",
        analytes=_THYROID_PANEL,
        notes=(
            "Reflex strategy: TSH alone if normal; add "
            "free T4 + free T3 if TSH < 0.4 or > 4.0.  "
            "For levothyroxine titration, recheck TSH "
            "≥ 6 weeks after a dose change (T4 half-life "
            "~7 days, steady-state ≥ 5 half-lives)."
        ),
    ),
]


# ------------------------------------------------------------------
# Public lookup helpers
# ------------------------------------------------------------------

def list_panels() -> List[LabPanel]:
    return list(_PANELS)


def get_panel(panel_id: str) -> Optional[LabPanel]:
    for p in _PANELS:
        if p.id == panel_id:
            return p
    return None


def list_analytes(category: Optional[str] = None
                  ) -> List[LabAnalyte]:
    """Return every catalogued analyte, optionally filtered by
    ``category`` (one of :data:`VALID_CATEGORIES`).  Order
    matches the BMP → CMP → Lipid → extended-tests panel
    walk."""
    seen: Dict[str, LabAnalyte] = {}
    for p in _PANELS:
        for a in p.analytes:
            seen[a.id] = a
    rows = list(seen.values())
    if category is None:
        return rows
    if category not in VALID_CATEGORIES:
        return []
    return [a for a in rows if a.category == category]


def get_analyte(analyte_id: str) -> Optional[LabAnalyte]:
    for a in list_analytes():
        if a.id == analyte_id:
            return a
    return None


def find_analyte(needle: str) -> List[LabAnalyte]:
    """Return every analyte whose id / name / abbreviation
    matches the (case-insensitive) needle.  Useful for the
    agent action — the user types ``"BUN"`` or ``"sodium"``
    and we surface the right rows."""
    if not needle:
        return []
    n = needle.lower().strip()
    out: List[LabAnalyte] = []
    for a in list_analytes():
        if (n == a.id.lower()
                or n in a.name.lower()
                or n == a.abbreviation.lower()):
            out.append(a)
    return out


def categories() -> List[str]:
    return list(VALID_CATEGORIES)


def analyte_to_dict(a: LabAnalyte) -> Dict[str, str]:
    return {
        "id": a.id,
        "name": a.name,
        "abbreviation": a.abbreviation,
        "category": a.category,
        "units": a.units,
        "normal_range": a.normal_range,
        "clinical_significance": a.clinical_significance,
        "notes": a.notes,
    }


def panel_to_dict(p: LabPanel) -> Dict[str, object]:
    return {
        "id": p.id,
        "name": p.name,
        "short_name": p.short_name,
        "purpose": p.purpose,
        "sample": p.sample,
        "procedure": p.procedure,
        "fasting": p.fasting,
        "notes": p.notes,
        "analytes": [analyte_to_dict(a) for a in p.analytes],
    }
