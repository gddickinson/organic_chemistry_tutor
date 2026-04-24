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
