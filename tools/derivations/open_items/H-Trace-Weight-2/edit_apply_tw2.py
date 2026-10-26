"""tw2's patch, applied by this script to the scratch checkout apply/ (never by hand): the trace's weight leaves the code
and enters the universe file as the integer `trace_weight` (the loader's INTEGERS, read by the Node, refused by name
when absent), rows.TRACE deleted, the held primitives' docstrings naming the file's key; every universe file of the
tests and the examples and the three committed records' embedded universe gain the key at the head's 54, so every
record stands bit for bit. Every replacement must match exactly once, else the script refuses."""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "apply")
SRC = os.path.join(ROOT, "src", "event_universe")

edits = {
    "loader/world.py": [
        (
            'INTEGERS = frozenset(\n    {"den", "node_clock", "quantum_action"}\n)  # the Link unit G is derived from Gamma (K-S1), no key\n',
            'INTEGERS = frozenset(\n    {"den", "node_clock", "quantum_action", "trace_weight"}\n)  # the Link unit G is derived from Gamma (K-S1), no key; trace_weight the held write\'s weight (TW-S1)\n',
        ),
        (
            "the universe's four integers, every row's shape",
            "the universe's four integers (den, node_clock, quantum_action, trace_weight), every row's shape",
        ),
    ],
    "rows.py": [
        (
            "TRACE = 54  # the trace's weight of the held walls and the carrier's write, 2 x 27 (ALGEBRA.md, the held write)\n",
            "",
        ),
        (
            "def write_walls(\n    shape: int, pair: tuple[int, int] | None, den: int, gamma: int, action: int\n) -> list[Any]:\n",
            "def write_walls(\n    shape: int, pair: tuple[int, int] | None, den: int, gamma: int, action: int, weight: int\n) -> list[Any]:\n",
        ),
        (
            "        return [held_wall(TRACE, den, gamma, action, p) for p in (4, *[2] * (shape - 1))]\n",
            "        return [held_wall(weight, den, gamma, action, p) for p in (4, *[2] * (shape - 1))]\n",
        ),
        (
            '    den, gamma, action = int(ints["den"]), int(ints["node_clock"]), int(ints["quantum_action"])\n    by_index: list[Row] = []\n',
            '    den, gamma, action = int(ints["den"]), int(ints["node_clock"]), int(ints["quantum_action"])\n    weight = trace_weight_of(ints)\n    by_index: list[Row] = []\n',
        ),
        (
            "        lines = lines_of(board, shape, pair, wall, w, write_walls(shape, pair, den, gamma, action))\n",
            "        lines = lines_of(board, shape, pair, wall, w, write_walls(shape, pair, den, gamma, action, weight))\n",
        ),
        (
            "def rows_of(universe: dict[str, Any], board: tuple[int, ...], w: int) -> tuple[list[Row], list[Row]]:\n",
            'def trace_weight_of(ints: dict[str, Any]) -> int:\n    """The held write\'s weight from the universe file\'s integers (TW-S1, 2026-10-26): the weight of the forms\' term against the stress\'s trace in the carrier\'s time line write and the held walls, in the unit den Gamma^2 (the trace\'s term enters at one part in trace_weight of the forms\' at the vacuum); a universe integer beside den, node_clock and quantum_action, refused by name when absent; the former literal 54 of rows.TRACE kept by name."""\n    if ints.get("trace_weight") is None:\n        raise ValueError("the universe names no trace_weight: the held write\'s weight of the forms\' term against the stress\'s trace")\n    return int(ints["trace_weight"])\n\n\ndef rows_of(universe: dict[str, Any], board: tuple[int, ...], w: int) -> tuple[list[Row], list[Row]]:\n',
        ),
        (
            "    \"\"\"The rows from the universe file's list, each a shape with a pair or a wall of its own, in the acts' order, and the same rows in the file's order (a lay names a row by its index); the file's shapes refused by name:",
            "    \"\"\"The rows from the universe file's list, each a shape with a pair or a wall of its own, in the acts' order, and the same rows in the file's order (a lay names a row by its index), the held walls at the file's trace_weight; the file's shapes refused by name:",
        ),
    ],
    "node.py": [
        (
            '        self.T, self.G = int(ints["quantum_action"]), link_unit_of(self.gamma)\n',
            '        self.T, self.G = int(ints["quantum_action"]), link_unit_of(self.gamma)\n        self.trace_weight = trace_weight_of(ints)\n',
        ),
    ],
    "interval.py": [
        (
            "from event_universe.rows import CARRIER, PLANE, " + "POTENTIAL, TRACE, Line, Row, zeros\n",
            "from event_universe.rows import CARRIER, PLANE, " + "POTENTIAL, Line, Row, zeros\n",
        ),
        (
            "            held_numerator(TRACE, self.x_now, self.forms, self.trace, self.p0, node.den, node.gamma)\n",
            "            held_numerator(\n                node.trace_weight, self.x_now, self.forms, self.trace, self.p0, node.den, node.gamma\n            )\n",
        ),
        (
            "4 X (forms 54 den Gamma^2 - trace p_0^2) p_0 on its time line",
            "4 X (forms trace_weight den Gamma^2 - trace p_0^2) p_0 on its time line (the weight the universe file's, TW-S1)",
        ),
    ],
    "core/rule3.py": [
        (
            "weight den Gamma^power T with the trace's weight 54 (rows.TRACE), the time line's at the power 4 and the nine lines' at 2.",
            "weight den Gamma^power T with the trace's weight the universe file's trace_weight (TW-S1; the former literal 54 of rows.TRACE kept by name), the time line's at the power 4 and the nine lines' at 2.",
        ),
        (
            "4 X (forms 54 den Gamma^2 - trace p_0^2) p_0 with the trace's weight 54 (rows.TRACE).",
            "4 X (forms weight den Gamma^2 - trace p_0^2) p_0 with the trace's weight the universe file's trace_weight (TW-S1; the former literal 54 of rows.TRACE kept by name).",
        ),
    ],
}
for name, pairs in edits.items():
    path = os.path.join(SRC, name)
    text = open(path, encoding="utf-8").read()
    for old, new in pairs:
        if text.count(old) != 1:
            print("REFUSED", name, repr(old[:70]), text.count(old))
            sys.exit(1)
        text = text.replace(old, new)
    open(path, "w", encoding="utf-8").write(text)
# node.py imports trace_weight_of from rows (the multiline import block)
path = os.path.join(SRC, "node.py")
text = open(path, encoding="utf-8").read()
old = "    rows_of,\n    walled_of,\n"
if text.count(old) != 1:
    print("REFUSED node.py rows import", text.count(old)); sys.exit(1)
text = text.replace(old, "    rows_of,\n    trace_weight_of,\n    walled_of,\n", 1)
open(path, "w", encoding="utf-8").write(text)

# the universe files and the records' embedded universe
universes = [
    "tests/worlds/universe_toy.json", "tests/worlds/universe_quartet.json", "tests/worlds/universe_middle.json",
    "examples/events/universe24/universe_universe24.json",
    "examples/events/pixel/universe_pixel_absorption.json", "examples/events/m20/universe_m19_lay3_g1000.json",
    "examples/events/big_bang/universe_big_bang.json", "examples/events/cycle/universe_three_clumps.json",
    "examples/events/cycle/universe_cycle.json", "examples/events/conserve/universe_conserve.json",
]
WEIGHT = 54
KEY = re.compile(r'("quantum_action":\s*)(\d+)')


def with_weight(raw: str, what: str) -> str:
    """The integers block with the key trace_weight added after quantum_action, the file's spacing kept."""
    found = KEY.findall(raw)
    if len(found) != 1:
        print("REFUSED", what, len(found)); sys.exit(1)
    return KEY.sub(lambda m: m.group(0) + ', "trace_weight": %d' % WEIGHT, raw, 1)


for rel in universes:
    path = os.path.join(ROOT, rel)
    raw = open(path, encoding="utf-8").read()
    if "trace_weight" in raw:
        continue
    raw = with_weight(raw, rel)
    json.loads(raw)
    open(path, "w", encoding="utf-8").write(raw)
for rec in ("hole", "chiral", "bodies"):
    path = os.path.join(ROOT, "examples", "records", rec + ".json")
    raw = open(path, encoding="utf-8").read()
    if "trace_weight" in raw:
        continue
    raw = with_weight(raw, rec)
    open(path, "w", encoding="utf-8").write(raw)
print("applied")

# the toy's part, the same order
import runpy
runpy.run_path(os.path.join(HERE, "toy_edits_tw2.py"))
