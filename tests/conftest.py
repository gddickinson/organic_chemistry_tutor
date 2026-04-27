"""Session-wide pytest hooks.

Round 94: session-end teardown that wipes any ``Tutor-test-*``
rows left behind by the content-authoring action tests
(``tests/test_authoring_actions.py``).  Those tests intentionally
use unique UUID-suffixed names that survive inter-run to avoid
collisions during a single session — but prior to this hook they
also survived across runs, accumulating ~165 glossary rows in a
typical developer's local DB (round-73 demo 15 surfaced the
pollution problem explicitly).

The cleanup is scoped tightly to the `Tutor-test-` prefix every
authoring test uses — impossible to collide with real seeded
content.  Also exposed as a module-level function in
:mod:`orgchem.db.cleanup` so users can invoke it manually.
"""
from __future__ import annotations

import logging
import os

# Phase CB-1.0 — pre-import sibling life-sciences studios at the
# start of every test session so their agent-action registrations
# fire before any test inspects the registry.  Mirrors the runtime
# behaviour where `main.py` / `HeadlessApp.__init__` triggers the
# same import.  Keeps tests like
# `tests/test_feature_discovery.test_no_stale_category_summaries`
# honest (they walk the registry + complain about category
# summaries with no corresponding action).
import cellbio  # noqa: F401, E402
import biochem  # noqa: F401, E402  # Phase BC-1.0 — second sibling
import pharm    # noqa: F401, E402  # Phase PH-1.0 — third sibling
import microbio  # noqa: F401, E402  # Phase MB-1.0 — fourth sibling
import botany   # noqa: F401, E402  # Phase BT-1.0 — fifth sibling
import animal   # noqa: F401, E402  # Phase AB-1.0 — sixth sibling
import genetics  # noqa: F401, E402  # Phase GM-1.0 — seventh sibling (post -3 chain)

log = logging.getLogger(__name__)


def pytest_sessionfinish(session, exitstatus):
    """Run the pollution purge once per pytest session.

    Keyed off a sentinel env var so CI / developer runs both
    clean up, but a manually-invoked pytest that wants to
    *preserve* test data for inspection can set
    ``ORGCHEM_KEEP_TEST_POLLUTION=1`` to skip.
    """
    if os.environ.get("ORGCHEM_KEEP_TEST_POLLUTION"):
        return
    try:
        from orgchem.db.cleanup import purge_tutor_test_pollution
        counts = purge_tutor_test_pollution()
        if counts.total() > 0:
            log.info(
                "pytest session-end: purged %d Tutor-test-* rows "
                "(%s)", counts.total(), counts,
            )
    except Exception:
        # Never let a cleanup failure break a test-session's
        # exit code.  Worst case the DB stays slightly polluted,
        # which is no worse than the pre-round-94 baseline.
        log.exception("Tutor-test pollution purge failed")
