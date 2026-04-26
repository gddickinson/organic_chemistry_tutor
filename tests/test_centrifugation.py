"""Phase 41 (round 144) — headless tests for the centrifugation
catalogue + g↔rpm solvers + agent actions.
"""
from __future__ import annotations
import math
import os

import pytest


# ==================================================================
# g ↔ rpm solvers
# ==================================================================

class TestRpmToG:
    def test_eppendorf_5424_data_sheet_value(self):
        """Eppendorf 5424 with FA-45-24-11 rotor: 15 000 RPM
        at 8.4 cm radius = 21 130 × g (matches the data
        sheet)."""
        from orgchem.core.centrifugation import rpm_to_g
        r = rpm_to_g(15000, 8.4)
        assert math.isclose(r["g_force"], 21130, rel_tol=1e-3)

    def test_round_trip_at_high_speed(self):
        """Beckman Optima Ti-70 rotor at 70 000 RPM, r=8.2 cm
        → ~450 000 × g.  Verify rpm→g→rpm round-trip."""
        from orgchem.core.centrifugation import rpm_to_g, g_to_rpm
        r = rpm_to_g(70000, 8.2)
        r2 = g_to_rpm(r["g_force"], 8.2)
        assert math.isclose(r2["rpm"], 70000, rel_tol=1e-6)

    def test_rejects_zero_rpm(self):
        from orgchem.core.centrifugation import rpm_to_g
        with pytest.raises(ValueError):
            rpm_to_g(0, 10.0)

    def test_rejects_zero_radius(self):
        from orgchem.core.centrifugation import rpm_to_g
        with pytest.raises(ValueError):
            rpm_to_g(1000, 0.0)


class TestGToRpm:
    def test_13000xg_on_microfuge(self):
        """A common protocol: 13 000 × g on FA-45-24-11 (r=8.4
        cm) → ~11 766 RPM."""
        from orgchem.core.centrifugation import g_to_rpm
        r = g_to_rpm(13000, 8.4)
        assert math.isclose(r["rpm"], 11765.5, rel_tol=1e-3)

    def test_rejects_zero_g(self):
        from orgchem.core.centrifugation import g_to_rpm
        with pytest.raises(ValueError):
            g_to_rpm(0, 10.0)


# ==================================================================
# Catalogue contents
# ==================================================================

class TestCentrifugesCatalogue:
    def test_size_at_least_eight(self):
        from orgchem.core.centrifugation import list_centrifuges
        assert len(list_centrifuges()) >= 8

    def test_all_classes_represented(self):
        from orgchem.core.centrifugation import (
            VALID_CENTRIFUGE_CLASSES, list_centrifuges,
        )
        seen = {c.centrifuge_class for c in list_centrifuges()}
        assert seen == set(VALID_CENTRIFUGE_CLASSES)

    def test_canonical_models_present(self):
        from orgchem.core.centrifugation import get_centrifuge
        for must in ("microfuge_5424", "benchtop_5810",
                     "hispeed_avanti", "ultra_optima_xpn"):
            assert get_centrifuge(must) is not None, must

    def test_filtered_by_class(self):
        from orgchem.core.centrifugation import list_centrifuges
        ultras = list_centrifuges(centrifuge_class="ultracentrifuge")
        assert all(c.centrifuge_class == "ultracentrifuge"
                   for c in ultras)
        assert len(ultras) >= 2

    def test_unknown_class_returns_empty(self):
        from orgchem.core.centrifugation import list_centrifuges
        assert list_centrifuges(centrifuge_class="bogus") == []

    def test_get_unknown_returns_none(self):
        from orgchem.core.centrifugation import get_centrifuge
        assert get_centrifuge("does-not-exist") is None

    def test_every_entry_required_fields(self):
        from orgchem.core.centrifugation import list_centrifuges
        for c in list_centrifuges():
            assert c.id and c.name and c.manufacturer
            assert c.max_speed_rpm > 0
            assert c.max_g_force > 0
            assert c.typical_uses

    def test_ultracentrifuge_speeds_match_class(self):
        """An ultracentrifuge MUST be > 50 000 RPM by definition."""
        from orgchem.core.centrifugation import list_centrifuges
        for c in list_centrifuges(centrifuge_class="ultracentrifuge"):
            assert c.max_speed_rpm >= 50000, c.id


class TestRotorsCatalogue:
    def test_size_at_least_eight(self):
        from orgchem.core.centrifugation import list_rotors
        assert len(list_rotors()) >= 8

    def test_all_types_represented(self):
        from orgchem.core.centrifugation import list_rotors
        seen = {r.rotor_type for r in list_rotors()}
        assert "fixed-angle" in seen
        assert "swinging-bucket" in seen
        assert "vertical" in seen

    def test_radius_positive(self):
        from orgchem.core.centrifugation import list_rotors
        for r in list_rotors():
            assert r.max_radius_cm > 0
            assert r.min_radius_cm > 0
            assert r.min_radius_cm <= r.max_radius_cm

    def test_swinging_bucket_has_variable_radius(self):
        """Swinging-bucket rotors have arms-in vs arms-out
        radius range; min < max should hold for most of them
        (bucket must rotate from rest position to horizontal)."""
        from orgchem.core.centrifugation import list_rotors
        sw = list_rotors(rotor_type="swinging-bucket")
        assert len(sw) >= 1
        # At least ONE swinging-bucket rotor should have a real
        # min < max range (some are spec'd as max-only).
        assert any(r.min_radius_cm < r.max_radius_cm for r in sw)


class TestApplicationsCatalogue:
    def test_size_at_least_six(self):
        from orgchem.core.centrifugation import list_applications
        assert len(list_applications()) >= 6

    def test_canonical_protocols_present(self):
        from orgchem.core.centrifugation import get_application
        for must in ("cell_pellet_mammalian", "cell_pellet_ecoli",
                     "differential_organelle",
                     "density_gradient_sucrose",
                     "density_gradient_cscl_plasmid",
                     "exosome_isolation"):
            assert get_application(must) is not None, must

    def test_filtered_by_protocol_class(self):
        from orgchem.core.centrifugation import list_applications
        diff = list_applications(protocol_class="differential")
        assert all(a.protocol_class == "differential" for a in diff)


# ==================================================================
# to_dict serialisation
# ==================================================================

class TestSerialisation:
    def test_centrifuge_to_dict_keys(self):
        from orgchem.core.centrifugation import (
            centrifuge_to_dict, get_centrifuge,
        )
        d = centrifuge_to_dict(get_centrifuge("microfuge_5424"))
        for k in ("id", "name", "manufacturer", "centrifuge_class",
                  "max_speed_rpm", "max_g_force",
                  "typical_capacity", "refrigerated",
                  "typical_uses", "notes"):
            assert k in d

    def test_rotor_to_dict_keys(self):
        from orgchem.core.centrifugation import (
            get_rotor, rotor_to_dict,
        )
        d = rotor_to_dict(get_rotor("rotor_fa_45_24_11"))
        for k in ("id", "name", "rotor_type",
                  "max_radius_cm", "min_radius_cm",
                  "max_speed_rpm", "typical_tubes", "notes"):
            assert k in d

    def test_application_to_dict_keys(self):
        from orgchem.core.centrifugation import (
            application_to_dict, get_application,
        )
        d = application_to_dict(get_application(
            "differential_organelle"))
        for k in ("id", "name", "protocol_class",
                  "recommended_g_force",
                  "recommended_duration",
                  "recommended_rotor_type",
                  "description", "notes"):
            assert k in d


# ==================================================================
# Agent actions
# ==================================================================

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(5)
        yield h


def test_action_list_centrifuges(app):
    rows = app.call("list_centrifuges_action")
    assert len(rows) >= 8


def test_action_list_centrifuges_filtered(app):
    rows = app.call("list_centrifuges_action",
                    centrifuge_class="microfuge")
    assert all(r["centrifuge_class"] == "microfuge" for r in rows)


def test_action_list_centrifuges_unknown_class(app):
    rows = app.call("list_centrifuges_action",
                    centrifuge_class="bogus")
    assert "error" in rows[0]


def test_action_get_centrifuge(app):
    r = app.call("get_centrifuge_action",
                 centrifuge_id="microfuge_5424")
    assert "error" not in r
    assert r["manufacturer"] == "Eppendorf"


def test_action_get_unknown_centrifuge(app):
    r = app.call("get_centrifuge_action",
                 centrifuge_id="bogus")
    assert "error" in r


def test_action_list_rotors(app):
    rows = app.call("list_rotors_action")
    assert len(rows) >= 8


def test_action_list_rotors_filtered(app):
    rows = app.call("list_rotors_action",
                    rotor_type="vertical")
    assert all(r["rotor_type"] == "vertical" for r in rows)


def test_action_get_rotor(app):
    r = app.call("get_rotor_action",
                 rotor_id="rotor_fa_45_24_11")
    assert "error" not in r
    assert r["max_radius_cm"] == 8.4


def test_action_list_applications(app):
    rows = app.call("list_centrifugation_applications")
    assert len(rows) >= 6


def test_action_list_applications_filtered(app):
    rows = app.call("list_centrifugation_applications",
                    protocol_class="density-gradient")
    assert all(r["protocol_class"] == "density-gradient"
               for r in rows)


def test_action_rpm_to_g(app):
    r = app.call("rpm_to_g_action", rpm=15000, radius_cm=8.4)
    assert "error" not in r
    assert math.isclose(r["g_force"], 21130, rel_tol=1e-3)


def test_action_g_to_rpm(app):
    r = app.call("g_to_rpm_action", g_force=13000, radius_cm=8.4)
    assert "error" not in r
    assert math.isclose(r["rpm"], 11765.5, rel_tol=1e-3)


def test_action_rpm_to_g_error_path(app):
    r = app.call("rpm_to_g_action", rpm=0, radius_cm=8.4)
    assert "error" in r
