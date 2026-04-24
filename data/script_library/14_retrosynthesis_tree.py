# ---------------------------------------------------------------
# Demo 14 — Multi-step retrosynthesis tree
# ---------------------------------------------------------------
# Recursively apply Phase-8d retro templates to methyl 4-phenyl-
# benzoate (ester + biaryl) and walk every discovered disconnection
# path to a terminal commercial-looking precursor.  A template for
# any retro-planning workflow.

target = "COC(=O)c1ccc(-c2ccccc2)cc1"
print(f"Target: methyl 4-phenylbenzoate")
print(f"  SMILES: {target}")
print("  (has an ester + a biaryl bond — multiple disconnection orders)\n")

tree = app.find_multi_step_retrosynthesis(
    target_smiles=target,
    max_depth=3,
    max_branches=3,
)

print(f"Routes found: {tree['n_paths_found']}")
for i, path in enumerate(tree["paths"][:4], 1):
    # A path is a list of nodes.  Non-terminal nodes carry the
    # template that disconnected them; terminal nodes are leaf
    # precursors (would be bought or made elsewhere).
    print(f"\n  Path {i}:")
    for j, node in enumerate(path):
        indent = "    " + "  " * j
        label = node.get("label", "?")
        smi = node.get("smiles", "")
        print(f"{indent}• [{label}]")
        print(f"{indent}    {smi}")

print(f"\nTree summary:")
print(f"  max_depth: {tree['max_depth']}")
print(f"  n_paths:   {tree['n_paths_found']}")
