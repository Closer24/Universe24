"""tw1's patch maker: the spec's edits applied to the detached tree patch_tree/ (HEAD 435af1631) and never by hand: the trace's
weight out of rows.py into the universe file's integers under the key `trace_weight`, read by the loader with the file's own
refusal by name when absent (the loader's one refusal of keys), carried by the Node as its fourth integer beside den, Gamma and T,
and passed to held_wall and held_numerator from there; the four universe files of the tests and the examples carry the key at
the record's 54; the three committed records' universe dicts the same; the literal 54 struck from the tests' allowed set.
Run: python make_patch_tw1.py; then git -C patch_tree diff > tw1.patch."""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TREE = os.path.join(HERE, "patch_tree")


def replace(name: str, old: str, new: str) -> None:
    path = os.path.join(TREE, name)
    text = open(path, encoding="utf-8").read()
    if text.count(old) != 1:
        print("REFUSED", name, repr(old[:90]), "matches", text.count(old))
        sys.exit(1)
    open(path, "w", encoding="utf-8").write(text.replace(old, new))


replace(
    "src/event_universe/loader/world.py",
    '    {"den", "node_clock", "quantum_action"}\n)  # the Link unit G is derived from Gamma (K-S1), no key\n',
    '    {"den", "node_clock", "quantum_action", "trace_weight"}\n)  # the Link unit G is derived from Gamma (K-S1), no key; the trace\'s weight the file\'s (TW-S1)\n',
)
replace(
    "src/event_universe/rows.py",
    "TRACE = 54  # the trace's weight of the held walls and the carrier's write, 2 x 27 (ALGEBRA.md, the held write)\n",
    "",
)
replace(
    "src/event_universe/rows.py",
    "def write_walls(\n    shape: int, pair: tuple[int, int] | None, den: int, gamma: int, action: int\n) -> list[Any]:",
    "def write_walls(\n    shape: int, pair: tuple[int, int] | None, den: int, gamma: int, action: int, weight: int\n) -> list[Any]:",
)
replace(
    "src/event_universe/rows.py",
    "    \"\"\"The write walls of a row's lines by its shape: the carrier's time line and its other lines the held walls (rule3.held_wall at the powers 4 and 2)",
    "    \"\"\"The write walls of a row's lines by its shape: the carrier's time line and its other lines the held walls (rule3.held_wall at the powers 4 and 2 with the trace's weight, the universe file's integer, TW-S1)",
)
replace(
    "src/event_universe/rows.py",
    "        return [held_wall(TRACE, den, gamma, action, p) for p in (4, *[2] * (shape - 1))]",
    "        return [held_wall(weight, den, gamma, action, p) for p in (4, *[2] * (shape - 1))]",
)
replace(
    "src/event_universe/rows.py",
    '    den, gamma, action = int(ints["den"]), int(ints["node_clock"]), int(ints["quantum_action"])\n',
    '    den, gamma, action = int(ints["den"]), int(ints["node_clock"]), int(ints["quantum_action"])\n    weight = int(ints["trace_weight"])\n',
)
replace(
    "src/event_universe/rows.py",
    "        lines = lines_of(board, shape, pair, wall, w, write_walls(shape, pair, den, gamma, action))",
    "        lines = lines_of(board, shape, pair, wall, w, write_walls(shape, pair, den, gamma, action, weight))",
)
replace(
    "src/event_universe/node.py",
    '        self.T, self.G = int(ints["quantum_action"]), link_unit_of(self.gamma)\n',
    '        self.T, self.G = int(ints["quantum_action"]), link_unit_of(self.gamma)\n        self.weight = int(ints["trace_weight"])  # the trace\'s weight of the held write, the file\'s integer (TW-S1)\n',
)
replace(
    "src/event_universe/interval.py",
    "from event_universe.rows import CARRIER, PLANE, " + "POTENTIAL, TRACE, Line, Row, zeros\n",
    "from event_universe.rows import CARRIER, PLANE, " + "POTENTIAL, Line, Row, zeros\n",
)
replace(
    "src/event_universe/interval.py",
    "            held_numerator(TRACE, self.x_now, self.forms, self.trace, self.p0, node.den, node.gamma)\n",
    "            held_numerator(node.weight, self.x_now, self.forms, self.trace, self.p0, node.den, node.gamma)\n",
)
replace(
    "src/event_universe/interval.py",
    "its one division with the write sourced by the riding rows' momenta, 4 X (forms 54 den Gamma^2 - trace p_0^2) p_0 on its time line",
    "its one division with the write sourced by the riding rows' momenta, 4 X (forms K den Gamma^2 - trace p_0^2) p_0 on its time line, K the trace's weight of the universe file (TW-S1)",
)
replace(
    "src/event_universe/core/rule3.py",
    "weight den Gamma^power T with the trace's weight 54 (rows.TRACE), the time line's at the power 4 and the nine lines' at 2.",
    "weight den Gamma^power T with the trace's weight the universe file's integer (TW-S1; 54 on the record), the time line's at the power 4 and the nine lines' at 2.",
)
replace(
    "src/event_universe/core/rule3.py",
    "4 X (forms 54 den Gamma^2 - trace p_0^2) p_0 with the trace's weight 54 (rows.TRACE).",
    "4 X (forms K den Gamma^2 - trace p_0^2) p_0 with the trace's weight K the universe file's integer (TW-S1; 54 on the record).",
)
replace(
    "tests/test_rule3.py",
    "ROW_INTEGERS = frozenset({8, 10, 54, 64})",
    "ROW_INTEGERS = frozenset({8, 10, 64})",
)
# the universe files of the law's form (integers and rows) and the committed records' universe dicts
for root in ("tests/worlds", "examples"):
    for folder, _dirs, files in os.walk(os.path.join(TREE, root)):
        for name in sorted(files):
            if not name.endswith(".json"):
                continue
            path = os.path.join(folder, name)
            text = open(path, encoding="utf-8").read()
            try:
                data = json.loads(text)
            except ValueError:
                continue
            if isinstance(data, dict) and set(data) == {"integers", "rows"} and "node_clock" in data["integers"]:
                data["integers"]["trace_weight"] = 54
                sep = (",", ":") if '":' in text and '": ' not in text else (", ", ": ")
                open(path, "w", encoding="utf-8").write(json.dumps(data, separators=sep) + ("\n" if text.endswith("\n") else ""))
                print("universe file", os.path.relpath(path, TREE))
            elif isinstance(data, dict) and "universe" in data and "rows" in data and "nodes" in data:
                data["universe"]["integers"]["trace_weight"] = 54
                open(path, "w", encoding="utf-8").write(json.dumps(data))
                print("record", os.path.relpath(path, TREE))
print("patched", TREE)

# the refusal by name of an integer the file lacks (the brief: a refusal by name when absent), one check for the four alike
replace(
    "src/event_universe/loader/world.py",
    '    refused_keys(universe["integers"], INTEGERS, "universe\'s integers")\n    for row in universe["rows"]:',
    '    refused_keys(universe["integers"], INTEGERS, "universe\'s integers")\n    lacking = sorted(INTEGERS - set(universe["integers"]))\n    if lacking:\n        raise ValueError(f"the universe\'s integers lack the law\'s: {\', \'.join(lacking)}")\n    for row in universe["rows"]:',
)

# the lean toy (a Node subclass the suite loads) reads the Node's weight
replace(
    "tools/derivations/toys/lean/toy.py",
    "from event_universe.rows import CARRIER, PLANE, " + "POTENTIAL, TRACE, Line, zeros\n",
    "from event_universe.rows import CARRIER, PLANE, " + "POTENTIAL, Line, zeros\n",
)
replace(
    "tools/derivations/toys/lean/toy.py",
    "                numerators = [4 * x * (forms * TRACE * self.den * self.gamma**2 - trace * p02) * p0]\n",
    "                numerators = [4 * x * (forms * self.weight * self.den * self.gamma**2 - trace * p02) * p0]\n",
)
