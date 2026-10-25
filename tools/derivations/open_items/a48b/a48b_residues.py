"""a48b: the residues of every digit's remainder on its lattice, per line and per slot (the Node, the six neighbours), over every draw of one run: 0, F - 1, or other; and the lattice F against the wall (W div F) per line. Usage: PYTHONPATH=<src> python a48b_residues.py <world.json> <intervals>"""
import json
import sys

sys.set_int_max_str_digits(0)
from a48b_48 import wrap_read_number
from event_universe.loader.world import load_world
from event_universe.node import Node


def main(argv):
    universe, world = load_world(argv[1])
    n = int(argv[2])
    node = Node(universe, world)
    wrap_read_number(node)
    for _ in range(n):
        node.step()
    tags = []
    for r in node.rows_:
        for k in range(len(r.lines)):
            tags.append(f"shape{r.shape}{'' if r.pair is None else ('_gap' + str(r.gap)) if r.gap is not None else ''}_line{k}")
    table = {}
    for e in node.draws:
        for d, b, li, k, rem, wl, F in e["digits"]:
            key = (tags[li], "node" if k == 0 else "neighbour")
            s = rem % F
            kind = "zero" if s == 0 else "F-1" if s == F - 1 else "other"
            row = table.setdefault(key, {"zero": 0, "F-1": 0, "other": 0, "F_bits": 0, "W_over_F_bits": 0})
            row[kind] += 1
            row["F_bits"] = max(row["F_bits"], F.bit_length())
            row["W_over_F_bits"] = max(row["W_over_F_bits"], (wl // F).bit_length())
    for key in sorted(table):
        print(json.dumps({"line": key[0], "slot": key[1], **table[key]}))
    print(json.dumps({"draws": len(node.draws), "births": node.counts["births"]}))


if __name__ == "__main__":
    main(sys.argv)
