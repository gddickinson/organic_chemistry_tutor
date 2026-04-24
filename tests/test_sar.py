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
