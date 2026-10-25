"""cs5: are the children alike at every Node? From a record's births (the log): at every birth whether the + child lies at the into-end (the take's Node) or the out-end (the twist's sign); then at the end of each named interval the children laid at every Node as a multiset of (record index, sense), the distinct multisets counted with their Node counts and the phase classes they fall on; the W of each child; the senses summed per class.
Usage: python alike.py <out.json> [i1 i2 ...]"""
import json
import sys

sys.set_int_max_str_digits(0)
rec = json.load(open(sys.argv[1]))
marks = [int(x) for x in sys.argv[2:]] or [1, 2, 3, 5, 10, 400]
log = rec["log"]
cube = int(rec["cube"])
phases = next(e for e in log if e["event"] == "lay_pattern")["phases"]


def cls(node):
    return phases[(node[0] * cube + node[1]) * cube + node[2]]


births = [e for e in log if e["event"] == "birth"]
plus_into = sum(1 for e in births if e["plus"] == e["node"])
print("births", len(births), "+ child at the into-end", plus_into, "at the out-end", len(births) - plus_into)
ws = sorted({tuple(e["W_children"]) for e in births})
print("W_children values", ws[:6])
lines = sorted({e.get("taken_line", 0) for e in births})
print("taken lines", lines, "levels", sorted({e["levels"] for e in births})[:6], "taken at or above booked on", sum(1 for e in births if e["taken"] >= e["booked"]), "of", len(births))
for m in marks:
    held = {}
    for e in births:
        if e["i"] <= m:
            for end, sense in ((tuple(e["minus"]), -1), (tuple(e["plus"]), 1)):
                held.setdefault(end, []).append((e["line_pair"], sense))
    kinds = {}
    for node, kids in held.items():
        key = tuple(sorted(kids))
        kinds.setdefault(key, []).append(node)
    print(f"through i {m}: Nodes with children {len(held)} of {cube ** 3}; distinct multisets {len(kinds)}:")
    for key, nodes in sorted(kinds.items(), key=lambda kv: -len(kv[1])):
        classes = {}
        for nd in nodes:
            classes[cls(nd)] = classes.get(cls(nd), 0) + 1
        print("   ", list(key), "at", len(nodes), "Nodes; by class", json.dumps({str(k): v for k, v in sorted(classes.items())}))
