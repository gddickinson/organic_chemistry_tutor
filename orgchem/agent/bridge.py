"""JSON-over-stdio bridge for external LLMs (incl. Claude Code sessions).

Run ``python main.py --agent-stdio`` and the app enters a loop that reads
newline-delimited JSON commands from stdin and writes JSON results to stdout.

Protocol (line-oriented, one JSON object per line):
    request :  {"id": "1", "method": "show_molecule", "params": {"name_or_id": "Caffeine"}}
    response:  {"id": "1", "result": {...}}
    error   :  {"id": "1", "error": "..."}

Special methods:
    list_actions        — return every action's JSON schema
    quit                — clean shutdown
"""
from __future__ import annotations
import json
import logging
import sys
from typing import Any, Dict

from orgchem.agent.actions import invoke, tool_schemas

log = logging.getLogger(__name__)


def _handle(req: Dict[str, Any]) -> Dict[str, Any]:
    rid = req.get("id")
    method = req.get("method", "")
    params = req.get("params") or {}

    if method == "list_actions":
        return {"id": rid, "result": tool_schemas()}
    if method == "quit":
        return {"id": rid, "result": "bye"}

    try:
        out = invoke(method, **params)
    except Exception as e:
        log.exception("Action %s failed", method)
        return {"id": rid, "error": f"{type(e).__name__}: {e}"}
    return {"id": rid, "result": out}


def run(show: bool = False) -> int:
    """Enter the JSON-stdio loop. Blocks until ``quit`` or EOF."""
    from orgchem.agent.headless import HeadlessApp

    with HeadlessApp(show=show) as app:
        log.info("Agent stdio bridge ready — send newline-delimited JSON requests")
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                req = json.loads(line)
            except json.JSONDecodeError as e:
                sys.stdout.write(json.dumps({"error": f"bad JSON: {e}"}) + "\n")
                sys.stdout.flush()
                continue

            resp = _handle(req)
            sys.stdout.write(json.dumps(resp, default=str) + "\n")
            sys.stdout.flush()

            if req.get("method") == "quit":
                break
            app.pump(3)
    return 0
