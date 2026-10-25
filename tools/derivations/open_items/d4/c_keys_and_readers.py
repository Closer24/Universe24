"""(c) The credit line's keys on the hole run (from hole_N.lines.jsonl), each classed: the Node's own readings (allowed to the decoder), the Node's position, the board's (the interval and its window, the labels), the loader's names (strings), the constants of the board's own click; and the readers' use of the board's `interval` by name, counted per function by the AST of tools/clicks_read.py, tools/record_gates.py, tools/back_in_time.py, tools/look/*.py (every string literal "interval" and every attribute/name `interval`).
Command: cd <worktree> && PYTHONPATH=src TMPDIR=/dev/shm/tmp /home/user/Universe24/venv314/bin/python tools/derivations/d4/c_keys_and_readers.py 120"""

from __future__ import annotations

import ast
import json
import sys

from d4lib import HERE, ROOT, dump

N = int(sys.argv[1]) if len(sys.argv) > 1 else 120
lines = [json.loads(x) for x in (HERE / f"hole_{N}.lines.jsonl").read_text(encoding="utf-8").splitlines()]
credits = [l for l in lines if l["event"] == "credit"]
OWN = ("point", "kind", "sense", "beat", "identity", "momentum", "proper", "windows", "taken", "walls", "excess", "step")
POSITION = ("support", "node_detector")
BOARD = ("interval", "window", "event", "label")
NAMES = ("family", "realised", "absorbed", "emitted", "source", "before")
CONSTANT = ("kept", "count", "left", "lost")
keys: dict[str, dict] = {}
for c in credits:
    for k, v in c.items():
        entry = keys.setdefault(k, {"on_credits": 0, "types": {}, "distinct": set()})
        entry["on_credits"] += 1
        t = type(v).__name__
        entry["types"][t] = entry["types"].get(t, 0) + 1
        if len(entry["distinct"]) < 6:
            entry["distinct"].add(json.dumps(v))
table = []
for k, e in keys.items():
    cls = "own" if k in OWN else "position" if k in POSITION else "board" if k in BOARD else "name" if k in NAMES else "constant" if k in CONSTANT else "unclassed"
    table.append({"key": k, "class": cls, "on_credits": e["on_credits"], "types": e["types"], "sample": sorted(e["distinct"])[:4]})
# node_detector against support: the x-major index unravelled equals the support on every credit
shape = (3, 3, 3)
same = sum(1 for c in credits if [c["node_detector"] // 9, (c["node_detector"] // 3) % 3, c["node_detector"] % 3] == c["support"])
# window against interval
win = sum(1 for c in credits if c["window"] == [c["interval"], c["interval"]])
strings = sum(1 for c in credits for v in c.values() if isinstance(v, str))

def interval_uses(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    found = {}
    def visit(node, owner):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            owner = node.name
        if isinstance(node, ast.Constant) and node.value == "interval":
            found[owner] = found.get(owner, 0) + 1
        elif isinstance(node, ast.Attribute) and node.attr == "interval":
            found[owner] = found.get(owner, 0) + 1
        for child in ast.iter_child_nodes(node):
            visit(child, owner)
    visit(tree, "<module>")
    return found
readers = {}
for rel in ("tools/clicks_read.py", "tools/record_gates.py", "tools/back_in_time.py", "tools/look/captions.py", "tools/look/eras_page.py", "tools/look/torus_page.py"):
    uses = interval_uses(ROOT / rel)
    readers[rel] = {"total": sum(uses.values()), "per_function": uses}
result = {
    "intervals": N,
    "credits": len(credits),
    "keys": table,
    "node_detector_unravels_to_support_on": same,
    "window_equals_[interval, interval]_on": win,
    "string_values_on_credits": strings,
    "readers_interval_uses": readers,
}
dump(HERE / f"c_keys_and_readers_{N}.json", result)
print(json.dumps({k: v for k, v in result.items() if k != "keys"}, indent=1))
for row in table:
    print(row["class"], row["key"], row["on_credits"], row["types"], row["sample"])
