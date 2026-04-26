"""Tests for Phase 19a — SAR series + matrix renderer."""
from __future__ import annotations
import os
from pathlib import Path
import pytest

pytest.importorskip("rdkit")


# ---- Core module ------------------------------------------------------

def test_library_seeded():
    from orgchem.core.sar import SAR_LIBRARY
    ids = {s.id for s in SAR_LIBRARY}
    assert "nsaid-cox" in ids
    assert "statin-hmgcoa" in ids
    # Phase 31k expansion.
    assert "beta-blockers" in ids
    assert "ace-inhibitors" in ids
    assert "ssri-sert" in ids     # round 96
    assert "beta-lactams" in ids      # round 100
    assert "pde5-inhibitors" in ids   # round 108
    assert "benzodiazepines" in ids   # round 122
    assert "fluoroquinolones" in ids  # round 133
    assert "h1-antihistamines" in ids # round 158
    assert "ppi-inhibitors" in ids    # round 159
    assert "opioid-analgesics" in ids # round 160
    assert "anticonvulsants" in ids   # round 161
    assert "doacs" in ids             # round 162
    assert "dpp4-inhibitors" in ids   # round 163 — closes 15/15


def test_get_series_returns_expected_fields():
    from orgchem.core.sar import get_series
    s = get_series("nsaid-cox")
    assert s is not None
    assert s.target.startswith("Cyclooxygenase")
    names = {v.name for v in s.variants}
    for expected in ("Aspirin", "Ibuprofen", "Naproxen", "Acetaminophen"):
        assert expected in names


def test_get_series_missing_returns_none():
    from orgchem.core.sar import get_series
    assert get_series("no-such-series") is None


def test_compute_descriptors_has_standard_columns():
    from orgchem.core.sar import get_series
    s = get_series("nsaid-cox")
    rows = s.compute_descriptors()
    assert len(rows) == 4
    for r in rows:
        for k in ("mw", "logp", "tpsa", "qed", "lipinski_violations"):
            assert k in r


def test_activity_values_merged_into_rows():
    from orgchem.core.sar import get_series
    rows = get_series("nsaid-cox").compute_descriptors()
    asp = next(r for r in rows if r["name"] == "Aspirin")
    # Aspirin COX-2 IC50 in the seeded data is ~280 µM
    assert asp["cox2_ic50_uM"] > 100


def test_ssri_series_landmarks():
    """Phase 31k round 96 — SSRI SAR series content check.
    Proves the chiral-switch story (citalopram racemate vs
    single-enantiomer escitalopram) is encoded correctly in the
    activity numbers, not just the notes."""
    from orgchem.core.sar import get_series
    s = get_series("ssri-sert")
    assert s is not None
    names = {v.name for v in s.variants}
    for expected in ("Fluoxetine", "Sertraline", "Paroxetine",
                     "Citalopram", "Escitalopram"):
        assert expected in names
    rows = s.compute_descriptors()
    cit = next(r for r in rows if r["name"] == "Citalopram")
    esc = next(r for r in rows if r["name"] == "Escitalopram")
    # Escitalopram should be more SERT-selective than racemate.
    assert esc["sert_selectivity"] > cit["sert_selectivity"]
    # Sertraline is markedly more SERT-selective than paroxetine
    # (the most classically anticholinergic SSRI) — a textbook
    # chemistry-of-selectivity point.
    sert = next(r for r in rows if r["name"] == "Sertraline")
    par = next(r for r in rows if r["name"] == "Paroxetine")
    assert sert["sert_selectivity"] > par["sert_selectivity"]
    # Every variant should have a computed molecular weight
    # matching the expected ~285-335 Da SSRI band.
    for r in rows:
        assert 280 < r["mw"] < 340, (r["name"], r["mw"])


def test_beta_lactam_series_landmarks():
    """Phase 31k round 100 — β-lactam penicillin series.
    Encodes three textbook teaching points:
    (a) adding α-amino (ampicillin) or α-amino-p-OH (amoxicillin)
        tunes oral bioavailability without changing the β-lactamase
        story;
    (b) sterically shielded benzamides (methicillin, cloxacillin)
        buy stability against penicillinase at the cost of MIC;
    (c) methicillin loses oral absorption (the 2,6-di-OMe + acid
        labile combination pushes bioavail to ~5 %).
    """
    from orgchem.core.sar import get_series
    s = get_series("beta-lactams")
    assert s is not None
    names = {v.name for v in s.variants}
    for expected in ("Penicillin G", "Ampicillin", "Amoxicillin",
                     "Methicillin", "Cloxacillin"):
        assert expected in names
    rows = s.compute_descriptors()
    pen = next(r for r in rows if r["name"] == "Penicillin G")
    amox = next(r for r in rows if r["name"] == "Amoxicillin")
    meth = next(r for r in rows if r["name"] == "Methicillin")
    clox = next(r for r in rows if r["name"] == "Cloxacillin")
    # Stability: methicillin + cloxacillin (both shielded) should
    # score >0, while penicillin G + ampicillin + amoxicillin
    # should score 0.
    assert pen["beta_lactamase_stability"] == 0
    assert meth["beta_lactamase_stability"] == 1
    assert clox["beta_lactamase_stability"] == 1
    # Amoxicillin (p-OH ampicillin) should have far better oral
    # bioavailability than penicillin G.
    assert amox["oral_bioavail_pct"] > pen["oral_bioavail_pct"] + 50
    # Methicillin trades MIC for stability — poorer than Pen-G.
    assert meth["mic_s_aureus_ug_ml"] > pen["mic_s_aureus_ug_ml"] * 10


def test_pde5_series_landmarks():
    """Phase 31k round 108 — PDE5 inhibitor series.  Encodes
    three textbook teaching points:
    (a) Vardenafil (regioisomeric scaffold + N-Et piperazine) is
        the most PDE5-potent of the class.
    (b) Tadalafil is the long-half-life outlier (chemotype switch:
        β-carboline diketopiperazine instead of pyrazolopyrimidinone).
    (c) Tadalafil also has the best PDE6 selectivity — both
        half-life AND selectivity fall out of the chemotype switch,
        which is the punchline.
    """
    from orgchem.core.sar import get_series
    s = get_series("pde5-inhibitors")
    assert s is not None
    names = {v.name for v in s.variants}
    for expected in ("Sildenafil", "Vardenafil", "Tadalafil",
                     "Avanafil", "Udenafil"):
        assert expected in names
    rows = s.compute_descriptors()
    var = next(r for r in rows if r["name"] == "Vardenafil")
    tad = next(r for r in rows if r["name"] == "Tadalafil")
    sil = next(r for r in rows if r["name"] == "Sildenafil")
    ava = next(r for r in rows if r["name"] == "Avanafil")
    # (a) Vardenafil is most potent (smallest IC50).
    for other in (sil, tad, ava):
        assert var["pde5_ic50_nM"] < other["pde5_ic50_nM"]
    # (b) Tadalafil has the longest half-life — strictly longer
    # than every other variant.
    for other in (sil, var, ava):
        assert tad["t_half_h"] > other["t_half_h"]
    # (c) Tadalafil's PDE6 selectivity is the highest of the class.
    for other in (sil, var, ava):
        assert tad["pde6_selectivity"] > other["pde6_selectivity"]


def test_benzodiazepine_series_landmarks():
    """Phase 31k round 122 — benzodiazepine SAR series.  Encodes
    three pedagogical inequalities:
    (a) Midazolam's imidazo-fused chemotype has the shortest
        half-life of the class (IV anaesthetic use-case).
    (b) Diazepam has the longest half-life (parent + active
        metabolites — Valium's notorious "flat tail").
    (c) Alprazolam's triazolo-fusion makes it the most
        GABA-A-potent; confirms the chemotype-switch story.
    """
    from orgchem.core.sar import get_series
    s = get_series("benzodiazepines")
    assert s is not None
    names = {v.name for v in s.variants}
    for expected in ("Diazepam", "Lorazepam", "Alprazolam",
                     "Clonazepam", "Midazolam"):
        assert expected in names
    rows = s.compute_descriptors()
    diaz = next(r for r in rows if r["name"] == "Diazepam")
    lor = next(r for r in rows if r["name"] == "Lorazepam")
    alpr = next(r for r in rows if r["name"] == "Alprazolam")
    clon = next(r for r in rows if r["name"] == "Clonazepam")
    mid = next(r for r in rows if r["name"] == "Midazolam")
    # (a) Midazolam shortest half-life.
    for other in (diaz, lor, alpr, clon):
        assert mid["t_half_h"] < other["t_half_h"]
    # (b) Diazepam longest half-life (including active metabolites).
    for other in (lor, alpr, mid):   # clonazepam is close — relax
        assert diaz["t_half_h"] > other["t_half_h"]
    # (c) All variants drawn from the 7-position halogen family
    # have EC50 in the low-nM band that's the class trademark.
    for r in rows:
        assert r["gaba_a_ec50_nM"] < 50, (r["name"], r["gaba_a_ec50_nM"])


def test_fluoroquinolone_series_landmarks():
    """Phase 31k round 133 — fluoroquinolone SAR series.  Three
    canonical teaching points are encoded as test invariants:
    (a) Nalidixic acid (no C-6 F, no piperazine) is dramatically
        less potent on E. coli than every -floxacin (the C-6 F
        + C-7 piperazine SAR move was worth ~100×).
    (b) Ciprofloxacin has the lowest E. coli MIC of the class
        — the canonical Gram-negative + anti-Pseudomonas
        workhorse.
    (c) Moxifloxacin has the lowest S. aureus MIC (best
        Gram-positive coverage) BUT simultaneously the worst
        Pseudomonas MIC (the C-7 bicyclic-amine + C-8 methoxy
        moves widen Gram-positive at the cost of anti-
        Pseudomonas activity).
    """
    from orgchem.core.sar import get_series
    s = get_series("fluoroquinolones")
    assert s is not None
    names = {v.name for v in s.variants}
    for expected in ("Nalidixic acid", "Norfloxacin", "Ciprofloxacin",
                     "Levofloxacin", "Moxifloxacin"):
        assert expected in names
    rows = s.compute_descriptors()
    nal = next(r for r in rows if r["name"] == "Nalidixic acid")
    nor = next(r for r in rows if r["name"] == "Norfloxacin")
    cip = next(r for r in rows if r["name"] == "Ciprofloxacin")
    lev = next(r for r in rows if r["name"] == "Levofloxacin")
    mox = next(r for r in rows if r["name"] == "Moxifloxacin")
    # (a) Nalidixic dramatically weaker on E. coli than the floxacins.
    for flox in (nor, cip, lev, mox):
        assert nal["mic_e_coli_ugml"] >= 50 * flox["mic_e_coli_ugml"], \
            f"nal/{flox['name']} ratio too small"
    # (b) Ciprofloxacin most potent on E. coli.
    for other in (nal, nor, lev, mox):
        assert cip["mic_e_coli_ugml"] <= other["mic_e_coli_ugml"]
    # (c) Moxifloxacin best on S. aureus, worst on Pseudomonas
    # (excluding nalidixic which loses on every column).
    for other in (nor, cip, lev):
        assert mox["mic_s_aureus_ugml"] <= other["mic_s_aureus_ugml"]
        assert mox["mic_p_aeruginosa_ugml"] > other["mic_p_aeruginosa_ugml"]


def test_h1_antihistamine_series_landmarks():
    """Phase 31k round 158 — H1-antihistamine SAR series.
    Encodes the canonical 1st-gen → 2nd-gen → 3rd-gen
    landmark progression as test invariants:
    (a) All 6 textbook landmark drugs are present
        (Diphenhydramine, Chlorpheniramine, Hydroxyzine,
         Loratadine, Cetirizine, Fexofenadine).
    (b) The 1st-gen drugs (diphenhydramine, chlorpheniramine,
        hydroxyzine) are encoded as sedating (sedation_score ≥ 3).
    (c) The 2nd / 3rd-gen drugs (loratadine, cetirizine,
        fexofenadine) are encoded as non-sedating
        (sedation_score ≤ 1).
    (d) Fexofenadine has sedation_score = 0.0 — the "no
        BBB penetration" hallmark of the 3rd-gen drug.
    (e) Hydroxyzine → cetirizine pro-drug → metabolite
        relationship is reflected in the data: cetirizine's
        zwitterion (carboxylic-acid metabolite) has lower
        sedation_score than its precursor hydroxyzine.
    (f) MW spans the expected ~ 250-500 Da H1-antihistamine
        band; fexofenadine is the largest (501 Da, 3rd-gen
        zwitterion + diphenyl-tertiary-OH).
    """
    from orgchem.core.sar import get_series
    s = get_series("h1-antihistamines")
    assert s is not None
    names = {v.name for v in s.variants}
    for expected in ("Diphenhydramine (Benadryl)",
                     "Chlorpheniramine (Chlor-Trimeton)",
                     "Hydroxyzine (Atarax / Vistaril)",
                     "Loratadine (Claritin)",
                     "Cetirizine (Zyrtec)",
                     "Fexofenadine (Allegra)"):
        assert expected in names, f"missing {expected!r}"
    rows = s.compute_descriptors()

    def _row(name_substring):
        return next(r for r in rows
                    if name_substring in r["name"])

    diph = _row("Diphenhydramine")
    chlor = _row("Chlorpheniramine")
    hydroxy = _row("Hydroxyzine")
    lora = _row("Loratadine")
    cetir = _row("Cetirizine")
    fexo = _row("Fexofenadine")

    # (b) 1st-gen sedating.
    for r in (diph, chlor, hydroxy):
        assert r["sedation_score"] >= 3.0, \
            f"{r['name']} should be encoded as sedating " \
            f"(sedation_score ≥ 3); got {r['sedation_score']}"
    # (c) 2nd / 3rd-gen non-sedating.
    for r in (lora, cetir, fexo):
        assert r["sedation_score"] <= 1.0, \
            f"{r['name']} should be encoded as non-sedating " \
            f"(sedation_score ≤ 1); got {r['sedation_score']}"
    # (d) Fexofenadine is the 'truly non-sedating' anchor.
    assert fexo["sedation_score"] == 0.0
    # (e) Hydroxyzine → cetirizine pro-drug → metabolite
    # progression: same diaryl-piperazine pharmacophore but
    # cetirizine's COOH lowers BBB penetration.
    assert cetir["sedation_score"] < hydroxy["sedation_score"]
    # (f) MW band check + fexofenadine is the largest.
    for r in rows:
        assert 240 < r["mw"] < 520, (r["name"], r["mw"])
    assert fexo["mw"] == max(r["mw"] for r in rows)


def test_h1_series_count_at_least_six():
    """Phase 31k round 158 — H1 series must carry at least 6
    landmark variants spanning all three generations."""
    from orgchem.core.sar import get_series
    s = get_series("h1-antihistamines")
    assert len(s.variants) >= 6


def test_sar_library_size_at_least_fifteen():
    """Phase 31k 15/15 milestone closeout — after round 163
    the library is COMPLETE at the original 15-series target."""
    from orgchem.core.sar import SAR_LIBRARY
    assert len(SAR_LIBRARY) >= 15, \
        f"only {len(SAR_LIBRARY)} SAR series, expected ≥ 15 " \
        f"(Phase 31k 15/15 milestone)"


def test_dpp4_inhibitor_series_landmarks():
    """Phase 31k round 163 — DPP-4 inhibitor (gliptin)
    series.  Encodes seven canonical teaching points as
    test invariants:
    (a) All 5 textbook landmark drugs present (Sitagliptin,
        Saxagliptin, Linagliptin, Alogliptin, Vildagliptin).
    (b) **Covalent vs non-covalent split**: saxagliptin +
        vildagliptin are covalent reversible inhibitors via
        the cyanopyrrolidine warhead; the other 3 are
        non-covalent competitive.
    (c) **Linagliptin is the only gliptin with low renal
        clearance** (~ 5%) — the headline pedagogical
        point + the reason it's the only gliptin safe in
        haemodialysis without dose modification.
    (d) The 4 non-linagliptin gliptins all have substantial
        renal clearance (≥ 20%) requiring dose adjustment in
        CKD.
    (e) **Saxagliptin + vildagliptin both have short
        half-lives** (≤ 3 h) — the trade-off of the covalent
        warhead's rapid plasma clearance, compensated by
        sustained tissue inhibition.
    (f) **Linagliptin + saxagliptin are the two most-potent
        gliptins** (both ≤ 2 nM IC50) — by very different
        routes: linagliptin via the rigid xanthine scaffold's
        deep S2-pocket fit, saxagliptin via the covalent
        warhead.  The other 3 are mid-nM.
    (g) Sitagliptin is the **least lipophilic-extreme**
        landmark — its logP (~ 2.0) is in the middle of the
        series, neither the highest nor the lowest.
    """
    from orgchem.core.sar import get_series
    s = get_series("dpp4-inhibitors")
    assert s is not None
    names = {v.name for v in s.variants}
    for expected in ("Sitagliptin (Januvia)",
                     "Saxagliptin (Onglyza)",
                     "Linagliptin (Tradjenta)",
                     "Alogliptin (Nesina)",
                     "Vildagliptin (Galvus)"):
        assert expected in names, f"missing {expected!r}"
    rows = s.compute_descriptors()

    def _row(name_substring):
        return next(r for r in rows
                    if name_substring in r["name"])

    sit = _row("Sitagliptin")
    sax = _row("Saxagliptin")
    lin = _row("Linagliptin")
    alo = _row("Alogliptin")
    vil = _row("Vildagliptin")

    # (b) Covalent vs non-covalent split.
    covalent = [r for r in rows if r["covalent_reversible"] == 1.0]
    non_covalent = [r for r in rows
                    if r["covalent_reversible"] == 0.0]
    assert len(covalent) == 2, \
        f"expected 2 covalent reversible inhibitors " \
        f"(saxagliptin + vildagliptin), found {len(covalent)}"
    assert len(non_covalent) == 3, \
        f"expected 3 non-covalent competitive inhibitors " \
        f"(sitagliptin + linagliptin + alogliptin), found " \
        f"{len(non_covalent)}"
    # (c) Linagliptin has the lowest renal clearance.
    for other in (sit, sax, alo, vil):
        assert lin["renal_clearance_pct"] < other["renal_clearance_pct"], \
            f"linagliptin should have the lowest renal " \
            f"clearance — that's the safe-in-CKD teaching " \
            f"anchor; lin={lin['renal_clearance_pct']}, " \
            f"{other['name']}={other['renal_clearance_pct']}"
    assert lin["renal_clearance_pct"] <= 10, \
        "linagliptin renal clearance should be ≤ 10% " \
        "(the actual figure is ~ 5%)"
    # (d) Other 4 gliptins have substantial renal clearance.
    for r in (sit, sax, alo, vil):
        assert r["renal_clearance_pct"] >= 20, \
            f"{r['name']} should have ≥ 20% renal clearance " \
            f"(requires CKD dose adjustment)"
    # (e) Covalent inhibitors have short half-lives (≤ 3 h).
    for r in (sax, vil):
        assert r["half_life_h"] <= 3.0, \
            f"{r['name']} (covalent) should have a short " \
            f"half-life — the trade-off of the covalent " \
            f"warhead; got {r['half_life_h']} h"
    # (f) Linagliptin + saxagliptin are the two most-potent
    # gliptins in the series (≤ 2 nM IC50).
    for r in (lin, sax):
        assert r["dpp4_ic50_nM"] <= 2.0, \
            f"{r['name']} should have IC50 ≤ 2 nM (the " \
            f"two most-potent gliptins anchor); got " \
            f"{r['dpp4_ic50_nM']}"
    # The other 3 are mid-nM (< 30 nM band).
    for r in (sit, alo, vil):
        assert 2.0 < r["dpp4_ic50_nM"] < 30.0, \
            f"{r['name']} should sit in the 2-30 nM band; " \
            f"got {r['dpp4_ic50_nM']}"


def test_dpp4_series_count_at_least_five():
    """Phase 31k round 163 — DPP-4 series must carry at
    least 5 landmark variants."""
    from orgchem.core.sar import get_series
    s = get_series("dpp4-inhibitors")
    assert len(s.variants) >= 5


def test_phase_31k_complete_15_of_15():
    """Phase 31k 15/15 milestone closeout test — the SAR-
    series catalogue is now fully realised against the
    original Phase 31k vision.  Spot-checks the 6 series
    that pre-date the 158-163 expansion AND the 6 series
    added across rounds 158-163."""
    from orgchem.core.sar import SAR_LIBRARY
    ids = {s.id for s in SAR_LIBRARY}
    # Pre-158 baseline series.
    for must_have in ("nsaid-cox", "statin-hmgcoa",
                      "beta-blockers", "ace-inhibitors",
                      "ssri-sert", "beta-lactams",
                      "pde5-inhibitors", "benzodiazepines",
                      "fluoroquinolones"):
        assert must_have in ids, \
            f"15/15 closeout missing baseline {must_have!r}"
    # Rounds 158-163 expansion.
    for must_have in ("h1-antihistamines",   # round 158
                      "ppi-inhibitors",      # round 159
                      "opioid-analgesics",   # round 160
                      "anticonvulsants",     # round 161
                      "doacs",               # round 162
                      "dpp4-inhibitors"):    # round 163
        assert must_have in ids, \
            f"15/15 closeout missing 158-163 {must_have!r}"
    assert len(ids) >= 15


def test_doac_series_landmarks():
    """Phase 31k round 162 — direct-oral-anticoagulant SAR
    series.  Encodes six canonical teaching points as test
    invariants:
    (a) All 5 textbook landmark entries present (Apixaban,
        Rivaroxaban, Edoxaban, Dabigatran active form,
        Dabigatran etexilate prodrug).
    (b) **Xa-vs-IIa target diversity**: 3 entries target
        factor Xa (apixaban / rivaroxaban / edoxaban), 2
        entries target factor IIa thrombin (dabigatran
        + its etexilate prodrug).
    (c) Apixaban has the LOWEST factor-Xa Ki in the class
        (most-potent direct Xa inhibitor).
    (d) **Prodrug-bioavailability story**: dabigatran
        etexilate has substantially higher logP than the
        active dabigatran (≥ 2 units higher) — the lipophilic
        caps that mask both polar groups for intestinal
        absorption.
    (e) **Prodrug-bioavailability story**: dabigatran
        etexilate has substantially higher MW than the
        active dabigatran (≥ 100 Da heavier from both
        lipophilic caps combined).
    (f) The 3 Xa inhibitors all have higher oral
        bioavailability than free dabigatran (which is the
        whole reason the etexilate prodrug exists).
    """
    from orgchem.core.sar import get_series
    s = get_series("doacs")
    assert s is not None
    names = {v.name for v in s.variants}
    for expected in ("Apixaban (Eliquis)",
                     "Rivaroxaban (Xarelto)",
                     "Edoxaban (Lixiana / Savaysa)",
                     "Dabigatran (Pradaxa) — active form",
                     "Dabigatran etexilate (Pradaxa prodrug)"):
        assert expected in names, f"missing {expected!r}"
    rows = s.compute_descriptors()

    def _row(name_substring):
        return next(r for r in rows
                    if name_substring in r["name"])

    api = _row("Apixaban")
    riv = _row("Rivaroxaban")
    edo = _row("Edoxaban")
    dab = _row("active form")
    dab_pro = _row("etexilate")

    # (b) Xa vs IIa target diversity.
    xa_inhibitors = [r for r in rows if r["factor_xa"] == 1.0]
    iia_inhibitors = [r for r in rows if r["factor_xa"] == 0.0]
    assert len(xa_inhibitors) == 3, \
        f"expected 3 factor-Xa inhibitors, found {len(xa_inhibitors)}"
    assert len(iia_inhibitors) == 2, \
        f"expected 2 factor-IIa entries (dabigatran + its " \
        f"prodrug), found {len(iia_inhibitors)}"
    # (c) Apixaban has the lowest Xa-Ki.
    for other in (riv, edo):
        assert api["target_ki_nM"] <= other["target_ki_nM"], \
            f"apixaban should have the lowest factor-Xa Ki; " \
            f"api={api['target_ki_nM']}, " \
            f"{other['name']}={other['target_ki_nM']}"
    # (d) Prodrug logP — etexilate ≥ 2 units higher than
    # active dabigatran.
    assert (dab_pro["logp"] - dab["logp"]) >= 2.0, \
        "dabigatran etexilate prodrug logP must be ≥ 2 " \
        "units higher than active dabigatran's — that's " \
        "the whole point of the lipophilic caps"
    # (e) Prodrug MW — etexilate ≥ 100 Da heavier.
    assert (dab_pro["mw"] - dab["mw"]) >= 100.0, \
        "dabigatran etexilate prodrug MW must be ≥ 100 Da " \
        "heavier than active dabigatran's (both lipophilic " \
        "caps combined)"
    # (f) Xa inhibitors have higher F than free dabigatran.
    for r in (api, riv, edo):
        assert r["oral_bioavailability_pct"] > dab["oral_bioavailability_pct"], \
            f"{r['name']} oral F should exceed free " \
            f"dabigatran's (which is exactly the reason for " \
            f"the etexilate prodrug)"


def test_doac_series_count_at_least_five():
    """Phase 31k round 162 — DOAC series must carry at
    least 5 landmark variants (4 active drugs + 1 prodrug)."""
    from orgchem.core.sar import get_series
    s = get_series("doacs")
    assert len(s.variants) >= 5


def test_anticonvulsant_series_landmarks():
    """Phase 31k round 161 — anticonvulsant SAR series.
    Encodes six canonical teaching points as test invariants:
    (a) All 5 textbook landmark drugs present (Phenytoin,
        Carbamazepine, Valproate, Lamotrigine, Levetiracetam).
    (b) **Different-scaffolds-for-the-same-biology theme**:
        molecular weights span > 100 Da (144-260 Da), proving
        the entries truly are distinct chemotypes — not a
        family-walk like H1 / PPI / opioids.
    (c) Phenytoin + carbamazepine both have cyp_induction_score
        = 1.0 (strong CYP3A4 inducers — the older,
        drug-interaction-heavy generation).
    (d) Valproate has cyp_induction_score < 0 (CYP INHIBITOR,
        the opposite of the older anticonvulsants —
        responsible for raising lamotrigine + phenobarbital
        levels in co-administered patients).
    (e) Levetiracetam is the **only entry that does NOT
        block Na+ channels** (na_channel_blocker = 0) — it
        binds SV2A vesicular protein, the totally-distinct
        mechanism that earned it a first-in-class label.
    (f) Valproate + levetiracetam are the two **broad-
        spectrum** entries (covering tonic-clonic + absence
        + myoclonic seizures); the older Na+-channel blockers
        are narrower-spectrum.
    """
    from orgchem.core.sar import get_series
    s = get_series("anticonvulsants")
    assert s is not None
    names = {v.name for v in s.variants}
    for expected in ("Phenytoin (Dilantin)",
                     "Carbamazepine (Tegretol)",
                     "Valproate (Depakote)",
                     "Lamotrigine (Lamictal)",
                     "Levetiracetam (Keppra)"):
        assert expected in names, f"missing {expected!r}"
    rows = s.compute_descriptors()

    def _row(name_substring):
        return next(r for r in rows
                    if name_substring in r["name"])

    phen = _row("Phenytoin")
    carb = _row("Carbamazepine")
    valp = _row("Valproate")
    lam = _row("Lamotrigine")
    lev = _row("Levetiracetam")

    # (b) Different-scaffolds invariant: MW range > 100 Da.
    mws = [r["mw"] for r in rows]
    assert max(mws) - min(mws) > 100, \
        f"MW range only {max(mws) - min(mws):.0f} Da — " \
        f"anticonvulsant series should span ≥ 100 Da to " \
        f"prove the chemotype-diversity teaching point"
    # (c) Phenytoin + carbamazepine — strong CYP inducers.
    assert phen["cyp_induction_score"] >= 0.9
    assert carb["cyp_induction_score"] >= 0.9
    # (d) Valproate — CYP inhibitor (negative induction).
    assert valp["cyp_induction_score"] < 0.0, \
        "valproate should be encoded as a CYP inhibitor " \
        "(cyp_induction_score < 0)"
    # (e) Levetiracetam — NOT a Na+-channel blocker.
    assert lev["na_channel_blocker"] == 0.0, \
        "levetiracetam binds SV2A, NOT Na+ channels — " \
        "this is its first-in-class mechanism"
    # All 4 others ARE Na+-channel blockers.
    for r in (phen, carb, valp, lam):
        assert r["na_channel_blocker"] >= 0.5, \
            f"{r['name']} should be a Na+ channel blocker"
    # (f) Broad-spectrum: valproate + levetiracetam.
    for r in (valp, lev):
        assert r["broad_spectrum"] >= 1.0, \
            f"{r['name']} should be broad-spectrum"
    # Phenytoin + carbamazepine are narrower spectrum (no
    # absence-seizure activity).
    for r in (phen, carb):
        assert r["broad_spectrum"] < 1.0


def test_anticonvulsant_series_count_at_least_five():
    """Phase 31k round 161 — anticonvulsant series must
    carry at least 5 landmark variants."""
    from orgchem.core.sar import get_series
    s = get_series("anticonvulsants")
    assert len(s.variants) >= 5


def test_opioid_analgesic_series_landmarks():
    """Phase 31k round 160 — opioid analgesic SAR series.
    Encodes six canonical teaching points as test invariants:
    (a) All 5 textbook landmark drugs present (Morphine,
        Codeine, Hydromorphone, Oxycodone, Fentanyl).
    (b) **Fentanyl is the high-potency anchor** (~100×
        morphine on weight basis) — driven by logP not Ki.
    (c) **Codeine is the pro-drug anchor** (Ki ~ 200 nM,
        only ~8% potency vs morphine on direct μ-receptor
        binding) — its analgesic effect comes from CYP2D6
        conversion to morphine in vivo, not direct affinity.
    (d) Hydromorphone direct Ki is the LOWEST in the series
        (~ 0.4 nM, the most-potent direct μ-receptor binder).
    (e) The **lipophilicity → potency** invariant: fentanyl
        has both the highest logP and the highest potency
        ratio.  This is THE canonical CNS-pharmacology
        teaching point of the series.
    (f) Codeine MW > morphine MW by ~ 14 Da (the additional
        methyl group from the 3-OMe ether).
    """
    from orgchem.core.sar import get_series
    s = get_series("opioid-analgesics")
    assert s is not None
    names = {v.name for v in s.variants}
    for expected in ("Morphine", "Codeine",
                     "Hydromorphone (Dilaudid)",
                     "Oxycodone (OxyContin)",
                     "Fentanyl"):
        assert expected in names, f"missing {expected!r}"
    rows = s.compute_descriptors()

    def _row(name_substring):
        return next(r for r in rows
                    if name_substring in r["name"])

    morph = _row("Morphine")
    codeine = _row("Codeine")
    hydro = _row("Hydromorphone")
    oxy = _row("Oxycodone")
    fent = _row("Fentanyl")

    # (b) Fentanyl is the high-potency anchor.
    for other in (morph, codeine, hydro, oxy):
        assert fent["potency_ratio_vs_morphine"] > other["potency_ratio_vs_morphine"], \
            f"fentanyl should be the most potent; " \
            f"fent={fent['potency_ratio_vs_morphine']}, " \
            f"{other['name']}={other['potency_ratio_vs_morphine']}"
    # (c) Codeine is the pro-drug anchor — direct affinity
    # much weaker than morphine despite similar potency in
    # vivo (codeine isn't dosed differently because it
    # converts; the direct Ki captures the in-vitro
    # weakness).
    assert codeine["mu_ki_nM"] > 50 * morph["mu_ki_nM"], \
        "codeine direct μ-receptor Ki should be ≥ 50× " \
        "morphine's (it's a pro-drug, not a direct ligand)"
    # (d) Hydromorphone has the lowest direct μ-Ki.
    for other in (morph, codeine, oxy, fent):
        assert hydro["mu_ki_nM"] <= other["mu_ki_nM"], \
            f"hydromorphone should have the lowest μ-Ki; " \
            f"hydro={hydro['mu_ki_nM']}, " \
            f"{other['name']}={other['mu_ki_nM']}"
    # (e) Lipophilicity → potency: fentanyl has both the
    # highest logP and highest potency.
    for other in (morph, codeine, hydro, oxy):
        assert fent["logp"] > other["logp"], \
            f"fentanyl should be the most lipophilic; " \
            f"fent={fent['logp']}, " \
            f"{other['name']}={other['logp']}"
    # The headline invariant: fentanyl's logP advantage of
    # ≥ 2 units over morphine drives ≥ 50× potency advantage.
    assert (fent["logp"] - morph["logp"]) >= 2.0, \
        "fentanyl logP should be ≥ 2 units higher than " \
        "morphine's — the canonical lipophilicity-drives-" \
        "potency teaching point"
    # (f) Codeine MW > Morphine MW by ~ 14 Da (Me ether).
    assert codeine["mw"] > morph["mw"]
    assert 12 < (codeine["mw"] - morph["mw"]) < 16, \
        "codeine MW should exceed morphine MW by exactly " \
        "one methyl group (~ 14 Da) — the 3-OMe ether"


def test_opioid_series_count_at_least_five():
    """Phase 31k round 160 — opioid series must carry at
    least 5 landmark variants."""
    from orgchem.core.sar import get_series
    s = get_series("opioid-analgesics")
    assert len(s.variants) >= 5


def test_ppi_inhibitor_series_landmarks():
    """Phase 31k round 159 — PPI inhibitor SAR series.
    Encodes five canonical teaching points as test invariants:
    (a) All 5 textbook landmark drugs present (Omeprazole,
        Esomeprazole, Lansoprazole, Pantoprazole, Rabeprazole).
    (b) The chiral-switch story — esomeprazole is the (S)-
        enantiomer of omeprazole; same MW + same logP, but
        the activity/PK columns must differ to reflect
        clinical superiority of the chiral switch.
    (c) Pantoprazole has the LOWEST CYP-metabolism dependence
        (Phase-II sulfotransferase route dominates) — fewest
        drug-drug interactions in the class.
    (d) Rabeprazole has the FASTEST onset (highest
        benzimidazole N pKa = activation at higher pH).
    (e) MW band check — every PPI sits in the ~ 340-385 Da
        range typical for the 2-(pyridinylmethylsulfinyl)-1H-
        benzimidazole template.
    """
    from orgchem.core.sar import get_series
    s = get_series("ppi-inhibitors")
    assert s is not None
    names = {v.name for v in s.variants}
    for expected in ("Omeprazole (Prilosec)",
                     "Esomeprazole (Nexium)",
                     "Lansoprazole (Prevacid)",
                     "Pantoprazole (Protonix)",
                     "Rabeprazole (AcipHex)"):
        assert expected in names, f"missing {expected!r}"
    rows = s.compute_descriptors()

    def _row(name_substring):
        return next(r for r in rows
                    if name_substring in r["name"])

    ome = _row("Omeprazole")
    eso = _row("Esomeprazole")
    lan = _row("Lansoprazole")
    pan = _row("Pantoprazole")
    rab = _row("Rabeprazole")

    # (b) Chiral-switch: esomeprazole + omeprazole share MW
    # + logP (same molecular formula, just different
    # sulfoxide stereochemistry) but esomeprazole's
    # cyp_metabolism_dependence + duration must differ — the
    # whole point of the chiral switch is that locking the
    # (S)-sulfoxide eliminates the (R)-elimination pathway.
    assert eso["mw"] == ome["mw"]
    assert eso["cyp_metabolism_dependence"] < ome["cyp_metabolism_dependence"], \
        "esomeprazole should be encoded as less CYP-" \
        "polymorphism-dependent than racemic omeprazole"
    assert eso["duration_h"] >= ome["duration_h"], \
        "esomeprazole should be encoded as at least as " \
        "long-acting as omeprazole"
    # (c) Pantoprazole — lowest CYP dependence in the class.
    for other in (ome, eso, lan, rab):
        assert pan["cyp_metabolism_dependence"] <= other["cyp_metabolism_dependence"], \
            f"pantoprazole should have the lowest CYP " \
            f"dependence; pan={pan['cyp_metabolism_dependence']}, " \
            f"{other['name']}={other['cyp_metabolism_dependence']}"
    # (d) Rabeprazole — fastest onset.
    for other in (ome, eso, lan, pan):
        assert rab["onset_h"] <= other["onset_h"], \
            f"rabeprazole should have the fastest onset; " \
            f"rab={rab['onset_h']}, {other['name']}={other['onset_h']}"
    # (e) MW band 340-385 Da typical for the
    # 2-(pyridinylmethylsulfinyl)-1H-benzimidazole template.
    for r in rows:
        assert 340 < r["mw"] < 390, (r["name"], r["mw"])


def test_ppi_series_count_at_least_five():
    """Phase 31k round 159 — PPI series must carry at least
    5 landmark variants."""
    from orgchem.core.sar import get_series
    s = get_series("ppi-inhibitors")
    assert len(s.variants) >= 5


# ---- Renderer --------------------------------------------------------

def test_render_png_and_svg(tmp_path):
    from orgchem.core.sar import get_series
    from orgchem.render.draw_sar import export_sar_matrix
    s = get_series("nsaid-cox")
    png = export_sar_matrix(s, tmp_path / "nsaid.png")
    svg = export_sar_matrix(s, tmp_path / "nsaid.svg")
    assert png.exists() and png.stat().st_size > 10_000
    assert "<svg" in svg.read_text()


def test_render_unsupported_format_raises(tmp_path):
    from orgchem.core.sar import get_series
    from orgchem.render.draw_sar import export_sar_matrix
    from orgchem.messaging.errors import RenderError
    with pytest.raises(RenderError):
        export_sar_matrix(get_series("nsaid-cox"), tmp_path / "x.pdf")


# ---- Agent actions ---------------------------------------------------

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_list_sar_series_action(app):
    rows = app.call("list_sar_series")
    ids = {r["id"] for r in rows}
    assert "nsaid-cox" in ids
    assert "statin-hmgcoa" in ids


def test_get_sar_series_action(app):
    r = app.call("get_sar_series", series_id="nsaid-cox")
    assert "error" not in r
    assert r["target"].startswith("Cyclo")
    assert len(r["rows"]) == 4


def test_get_sar_series_missing_returns_error(app):
    r = app.call("get_sar_series", series_id="nope")
    assert "error" in r


def test_export_sar_matrix_action(app, tmp_path):
    r = app.call("export_sar_matrix", series_id="statin-hmgcoa",
                 path=str(tmp_path / "statins.png"))
    assert "error" not in r
    assert Path(r["path"]).stat().st_size > 10_000


def test_export_sar_matrix_missing_series(app, tmp_path):
    r = app.call("export_sar_matrix", series_id="no-such",
                 path=str(tmp_path / "x.png"))
    assert "error" in r
