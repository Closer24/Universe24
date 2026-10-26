"""tw2's patch, the toy's part (tools/derivations/toys/lean, loaded by tests/test_the_quartet.py): the toy imports no
TRACE and reads the Node's trace_weight (the toy is the engine's Node); the toy's three universe files gain the key at 54.
Run by edit_apply_tw2.py's order after the engine's part (never by hand); every replacement must match exactly once."""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "apply")
TOY = os.path.join(ROOT, "tools", "derivations", "toys", "lean")
edits = [
    (
        "from event_universe.rows import CARRIER, PLANE, " + "POTENTIAL, TRACE, Line, zeros\n",
        "from event_universe.rows import CARRIER, PLANE, " + "POTENTIAL, Line, zeros\n",
    ),
    (
        "                numerators = [4 * x * (forms * TRACE * self.den * self.gamma**2 - trace * p02) * p0]\n",
        "                numerators = [\n                    4 * x * (forms * self.trace_weight * self.den * self.gamma**2 - trace * p02) * p0\n                ]  # the weight the universe file's trace_weight (TW-S1)\n",
    ),
]
path = os.path.join(TOY, "toy.py")
text = open(path, encoding="utf-8").read()
for old, new in edits:
    if text.count(old) != 1:
        print("REFUSED toy.py", repr(old[:60]), text.count(old)); sys.exit(1)
    text = text.replace(old, new)
open(path, "w", encoding="utf-8").write(text)
KEY = re.compile(r'("quantum_action":\s*)(\d+)')
for rel in ("universe_toy.json", "universe_middle.json", os.path.join("records", "universe_quartet.json")):
    path = os.path.join(TOY, rel)
    raw = open(path, encoding="utf-8").read()
    if len(KEY.findall(raw)) != 1 or "trace_weight" in raw:
        print("REFUSED", rel); sys.exit(1)
    open(path, "w", encoding="utf-8").write(KEY.sub(lambda m: m.group(0) + ', "trace_weight": 54', raw, 1))
print("toy applied")
