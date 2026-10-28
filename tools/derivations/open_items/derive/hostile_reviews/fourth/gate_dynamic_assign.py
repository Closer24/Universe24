"""A dynamic import written as an assignment, in each folder of tensor24 (gate.scan on the text alone).

Usage: python gate_dynamic_assign.py <worktree>
"""
import importlib.util
import sys
from pathlib import Path

wt = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("gate", wt / "tools/derivations/open_items/scribe_scan.py")
gate = importlib.util.module_from_spec(spec)
sys.modules["gate"] = gate
spec.loader.exec_module(gate)
TEXT = '"""x."""\n\nimport importlib\n\n\ndef f(z):\n    """y."""\n    np = importlib.import_module("numpy")\n    return np.sum(z)\n'
for rel in ("tensor24/algebra/x.py", "tensor24/engine/x.py", "tensor24/readings/x.py", "tensor24/runner/x.py", "tensor24/__init__.py"):
    hits = [f"{h.rule}:{h.detail[:40]}" for h in gate.scan(rel, TEXT) if h.tier == "BLOCK"]
    print(f"{rel:24s} {', '.join(hits) or 'stands'}")
