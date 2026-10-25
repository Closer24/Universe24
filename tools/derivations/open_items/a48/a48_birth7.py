"""a48: the first parting birth read line by line: the seed and its image under m (the diagonal given, default -1 1 1) run to
the interval named; every log line of that interval printed for both runs (the births with their plane and children, the
refusals with their cause), and every draw of that interval through the image: the Node, the number and the room in both
runs, the plane each number picks ((number div unit_gap0) mod the records' count), the count of digits that differ.
Usage: python a48_birth7.py <world.json> <cube> <interval> [mx my mz]; integers only."""
import json
import sys

import numpy as np

sys.set_int_max_str_digits(0)
from event_universe import close  # noqa: E402
from event_universe.core.rule3 import quotient, remainder  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402

from a48_48 import image, world_image  # noqa: E402
from a48_parting import DRAWS, wrapped_read  # noqa: E402


def main(argv):
    universe, world = load_world(argv[1])
    cube, last = int(argv[2]), int(argv[3])
    diag = [int(x) for x in argv[4:7]] if len(argv) >= 7 else [-1, 1, 1]
    m = np.diag(diag).astype(int)
    eye = np.eye(3, dtype=int)
    base = Node(json.loads(json.dumps(universe)), world_image(world, eye, cube, last))
    img = Node(json.loads(json.dumps(universe)), world_image(world, m, cube, last))
    for _ in range(last):
        close.read_number = wrapped_read("base")
        base.step()
        close.read_number = wrapped_read("image")
        img.step()
    n_rec = len(base.records())
    for tag, node in (("base", base), ("image", img)):
        print(f"--- {tag}: the log at interval {last}")
        for e in node.log:
            if e["i"] != last:
                continue
            if e["event"] == "birth":
                print(json.dumps({k: e[k] for k in ("event", "node", "line_pair", "minus", "plus", "W_children", "taken", "booked", "room")}))
            else:
                print(json.dumps({k: v for k, v in e.items() if k != "i"}))
    print(f"--- the draws at interval {last} through the image (base Node -> image Node)")
    di = {d[1]: d for d in DRAWS.get("image", []) if d[0] == last}
    for d in [d for d in DRAWS.get("base", []) if d[0] == last]:
        there = image(m, d[1], cube)
        e = di.get(there)
        sb = sorted((x[5], x[6]) for x in d[2])
        row = {"node": list(d[1]), "image node": list(there), "base (number, room)": d[3]}
        if d[3] is not None:
            row["base plane"] = int(remainder(quotient(d[3][0], base.unit_gap0), n_rec))
        if e is None:
            row["image"] = "no draw at the image Node"
        else:
            si = sorted((x[5], x[6]) for x in e[2])
            row["image (number, room)"] = e[3]
            if e[3] is not None:
                row["image plane"] = int(remainder(quotient(e[3][0], img.unit_gap0), n_rec))
            row["digits that differ"] = sum(1 for a, b in zip(sb, si) if a != b) if len(sb) == len(si) else "counts differ"
        print(json.dumps(row))


if __name__ == "__main__":
    main(sys.argv)
