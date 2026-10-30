"""The closed list in algebra/ on ring.py's own text, and dynamic imports in each folder, through gate.scan(rel, source).

Usage: python gate_closed_list.py <worktree>. Each case is ring.py with one change; BLOCK hits are the refusals.
"""

import importlib.util
import sys
from pathlib import Path

wt = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("gate", wt / "tools/derivations/open_items/scribe_scan.py")
gate = importlib.util.module_from_spec(spec)
sys.modules["gate"] = gate
spec.loader.exec_module(gate)
RING = (wt / "src/tensor24/algebra/ring.py").read_text()
REL = "tensor24/algebra/ring.py"
MUL = "    a, b = z\n    c, d = w\n    return a * c - b * d, a * d + b * c\n"


def blocks(rel, text):
    return [f"{h.rule}:{h.detail[:40]}" for h in gate.scan(rel, text) if h.tier == "BLOCK"]


assert RING.count(MUL) == 1
print("ring.py as committed:", blocks(REL, RING) or "no refusal", "| notes:", [h.rule for h in gate.scan(REL, RING) if h.tier != "BLOCK"])
CASES = {
    "nested tuple unpacking": "    (a, b), (c, d) = z, w\n    return a * c - b * d, a * d + b * c\n",
    "a number 2": "    a, b = z\n    c, d = w\n    return 2 * a * c - b * d, a * d + b * c\n",
    "a number -1 (as -1 *)": "    a, b = z\n    c, d = w\n    return a * c + -1 * b * d, a * d + b * c\n",
    "a power a ** 2": "    a, b = z\n    c, d = w\n    return a ** 2 - b * d, a * d + b * c\n",
    "a float": "    a, b = z\n    c, d = w\n    return a * c - b * d * 1.0, a * d + b * c\n",
    "a comparison": "    a, b = z\n    c, d = w\n    return a * c - b * d, (a < d) + b * c\n",
    "an if": "    a, b = z\n    c, d = w\n    if a:\n        return a, b\n    return a * c - b * d, a * d + b * c\n",
    "an if expression": "    a, b = z\n    c, d = w\n    return (a if b else c), a * d + b * c\n",
    "a floor division": "    a, b = z\n    c, d = w\n    return a * c // d, a * d + b * c\n",
    "abs()": "    a, b = z\n    c, d = w\n    return abs(a) * c - b * d, a * d + b * c\n",
    "a list display": "    a, b = z\n    c, d = w\n    return [a * c - b * d, a * d + b * c]\n",
    "a for loop": "    a, b = z\n    c, d = w\n    for _ in z:\n        pass\n    return a * c - b * d, a * d + b * c\n",
    "a generator": "    a, b = z\n    c, d = w\n    return tuple(x for x in z)\n",
    "a starred unpacking": "    a, *b = z\n    c, d = w\n    return a * c, a * d\n",
    "an and": "    a, b = z\n    c, d = w\n    return (a and c) - b * d, a * d + b * c\n",
    "a lambda": "    a, b = z\n    c, d = w\n    f = lambda x: x\n    return f(a) * c - b * d, a * d + b * c\n",
    "an import of numpy": "    import numpy\n    a, b = z\n    c, d = w\n    return a * c - b * d, a * d + b * c\n",
    "importlib in algebra": "    import importlib\n    importlib.import_module('numpy')\n    a, b = z\n    c, d = w\n    return a * c - b * d, a * d + b * c\n",
    "a True": "    a, b = z\n    c, d = w\n    return a * c - b * d * True, a * d + b * c\n",
    "a walrus": "    a, b = z\n    c, d = w\n    return (t := a * c) - b * d, a * d + b * c\n",
    "an augmented add": "    a, b = z\n    c, d = w\n    a += c\n    return a * c - b * d, a * d + b * c\n",
    "a subscript chain": "    a, b = z[0], z[1]\n    c, d = w\n    return a * c - b * d, a * d + b * c\n",
}
for name, body in CASES.items():
    print(f"{name:28s} {'REFUSED ' + ', '.join(blocks(REL, RING.replace(MUL, body))) if blocks(REL, RING.replace(MUL, body)) else 'stands'}")

DYN = "import importlib\n\nimportlib.import_module('tensor24.engine.step')\n__import__('numpy')\n"
for rel in ("tensor24/__init__.py", "tensor24/main.py", "tensor24/runner/x.py", "tensor24/record/x.py",
            "tensor24/decoder/x.py", "tensor24/readings/x.py", "tensor24/engine/x.py", "tensor24/algebra/x.py"):
    print(f"dynamic imports in {rel:24s} {', '.join(blocks(rel, DYN)) or 'stand'}")
