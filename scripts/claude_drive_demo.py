"""Demonstrate driving OrgChem Studio from an external LLM / Python session.

Two approaches are shown:

1. **Direct** — import :class:`HeadlessApp` and call actions as Python functions.
   Simplest; recommended when the driver is a Python program.

2. **Stdio bridge** — spawn ``python main.py --agent-stdio`` and exchange
   newline-delimited JSON. This is what Claude Code (or any external process)
   uses when it can't import the package directly.
"""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


# ---------------------------------------------------------------------
def demo_direct() -> None:
    sys.path.insert(0, str(REPO))
    from orgchem.agent.headless import HeadlessApp

    with HeadlessApp() as app:
        print("\n--- list_all_molecules (first 5) ---")
        rows = app.call("list_all_molecules")
        for r in rows[:5]:
            print(f"  {r['id']:>3}  {r['name']:<18}  {r.get('formula', '')}")

        print("\n--- show_molecule: Caffeine ---")
        print(json.dumps(app.call("show_molecule", name_or_id="Caffeine"), indent=2, default=str))

        print("\n--- calculate_empirical_formula (nicotine sample) ---")
        print(json.dumps(app.call(
            "calculate_empirical_formula",
            percentages={"C": 74.00, "H": 8.70, "N": 17.27},
            molar_mass=162.0,
        ), indent=2))


# ---------------------------------------------------------------------
def demo_stdio() -> None:
    cmd = [sys.executable, str(REPO / "main.py"), "--agent-stdio"]
    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        text=True, bufsize=1,
    )
    assert proc.stdin and proc.stdout

    def send(obj):
        proc.stdin.write(json.dumps(obj) + "\n")
        proc.stdin.flush()
        return json.loads(proc.stdout.readline())

    print("\n--- list_actions (first 3 tools) ---")
    resp = send({"id": "1", "method": "list_actions"})
    for t in resp["result"][:3]:
        print(f"  {t['name']}: {t.get('description', '')[:72]}")

    print("\n--- show_molecule: Cholesterol ---")
    resp = send({"id": "2", "method": "show_molecule", "params": {"name_or_id": "Cholesterol"}})
    print(json.dumps(resp, indent=2, default=str))

    send({"id": "3", "method": "quit"})
    proc.wait(timeout=5)


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "direct"
    (demo_stdio if which == "stdio" else demo_direct)()
