"""Headless tutor-driver test.

Exercises the same Conversation + tool-loop the GUI Tutor panel
uses, against the local Ollama qwen2.5:14b backend, with a
variety of prompts that should hit different agent actions.
Captures tool calls + errors so we can diagnose tutor bugs
without watching the GUI.
"""
from __future__ import annotations
import json
import os
import sys
import traceback

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


def main() -> None:
    from orgchem.agent.headless import HeadlessApp
    from orgchem.agent.conversation import Conversation
    from orgchem.agent.llm.ollama_backend import OllamaBackend

    # Start the headless app + seeded DB.
    print("=" * 70)
    print("Booting HeadlessApp (offscreen Qt + seeded DB)…")
    with HeadlessApp() as h:
        h.pump(5)
        print("  ready.")
        print()

        backend = OllamaBackend(model="qwen2.5:14b")
        convo = Conversation(backend=backend)

        prompts = [
            # The original bug-repro the user reported
            "Show me caffeine and explain why it is a stimulant.",
            # Molecule lookup by SMILES / synonym
            "What is the structure of glucose?",
            # Reaction lookup
            "Show me the Diels-Alder reaction.",
            # Mechanism playback
            "Open the chymotrypsin mechanism.",
            # Glossary / definition
            "Define photoredox catalysis.",
            # Periodic table opener
            "Open the periodic table.",
            # Process simulator (Phase 38d)
            "Run a simulation of simple distillation.",
            # Metabolic pathway lookup
            "What molecules does glycolysis touch?",
            # Spectroscopy prediction
            "Predict the IR spectrum of acetone.",
            # Comparison
            "Compare aspirin and ibuprofen by their drug-likeness.",
        ]

        report = []
        for i, prompt in enumerate(prompts, 1):
            print("=" * 70)
            print(f"[{i}/{len(prompts)}]  USER: {prompt}")
            print("-" * 70)
            tool_calls = []
            errors = []
            final_text = ""
            try:
                for assistant in convo.send(prompt):
                    if assistant.tool_calls:
                        for tc in assistant.tool_calls:
                            tool_calls.append({
                                "name": tc.name,
                                "args": tc.arguments,
                            })
                            print(f"  TOOL: {tc.name}({json.dumps(tc.arguments, default=str)[:140]})")
                    if assistant.text:
                        final_text = assistant.text
                # Look at the most-recent tool_results in history
                # for any is_error rows.
                if convo.history and convo.history[-1].tool_results:
                    for tr in convo.history[-1].tool_results:
                        if tr.is_error:
                            errors.append(tr.content)
                # Also walk all of history's tool_results for errors
                for msg in convo.history:
                    if msg.tool_results:
                        for tr in msg.tool_results:
                            if tr.is_error:
                                errors.append(tr.content)
            except Exception as e:
                errors.append({"runtime": f"{type(e).__name__}: {e}"})
                traceback.print_exc()

            # Dedupe errors per prompt
            unique_errors = []
            seen = set()
            for e in errors:
                key = json.dumps(e, default=str)
                if key in seen:
                    continue
                seen.add(key)
                unique_errors.append(e)

            print(f"  → final text: {(final_text or '<empty>')[:200]}")
            if unique_errors:
                print(f"  ⚠ ERRORS: {len(unique_errors)}")
                for e in unique_errors[:3]:
                    print(f"     {json.dumps(e, default=str)[:200]}")
            else:
                print(f"  ✓ no tool errors")
            report.append({
                "prompt": prompt,
                "n_tools": len(tool_calls),
                "tools": tool_calls,
                "errors": unique_errors,
                "final_text": (final_text or "")[:300],
            })
            print()

        # Summary
        print("=" * 70)
        print("SUMMARY")
        print("=" * 70)
        n_clean = sum(1 for r in report if not r["errors"])
        n_with_err = len(report) - n_clean
        print(f"Prompts: {len(report)}")
        print(f"Clean (no tool errors): {n_clean}")
        print(f"With at least one tool error: {n_with_err}")
        print()
        # Print error-bearing prompts
        for r in report:
            if r["errors"]:
                print(f"ERROR in: {r['prompt']!r}")
                for e in r["errors"]:
                    print(f"  - {json.dumps(e, default=str)[:300]}")


if __name__ == "__main__":
    main()
