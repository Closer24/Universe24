"""sl1's runner: a world run on the engine's package named by `src` (the repository's src, or the flagged copy src_sl1), the state's hash printed at the end of the forward run (the bit-for-bit comparison between the two packages and between the flag on and off), then the run back and the record written.
Usage: python run_record.py <src|copy> <world.json> <out.json> [back N] [generic]
`generic` sets SL1_CLOSE=generic before the import (the copy's flag); `src` runs the repository's src bit for bit."""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
which = sys.argv[1]
if "generic" in sys.argv[4:]:
    os.environ["SL1_CLOSE"] = "generic"
if which == "copy":
    sys.path.insert(0, os.path.join(HERE, "src_sl1"))
else:
    sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "src")))

from event_universe import close, run  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402


def main() -> None:
    sys.set_int_max_str_digits(0)
    print("package:", os.path.dirname(os.path.abspath(close.__file__)), "flag:", os.environ.get("SL1_CLOSE"))
    universe, world = load_world(sys.argv[2])
    back = int(sys.argv[sys.argv.index("back") + 1]) if "back" in sys.argv else 0
    node = Node(universe, world)
    intervals = int(world["intervals"])
    rows, nodes, hashes = run.forward(node, intervals, back, lambda line: None)
    n_ints, bits = node.census()
    final = {"state_hash": node.state_hash(), "integers": n_ints, "state_bits": bits, "transient_bits": node.max_transient, "intervals": intervals}
    print(json.dumps(final))
    kept_log = list(node.log)
    returned = run.run_back(node, hashes) if back else None
    print(json.dumps({"run back": returned}))
    counts = {k: str(v) for k, v in node.counts.items()}
    print(json.dumps({"counts": counts}))
    found = {
        "world": world,
        "universe": universe,
        "den": node.den,
        "cube": node.cube,
        "intervals": intervals,
        "units": [str(u) for u in node.units],
        "planes": [str(r.pair[0]) for r in node.records() if r.pair],
        "T": node.T,
        "gamma": node.gamma,
        "G": node.G,
        "counts": counts,
        "turns": node.turns,
        "rows": rows,
        "final": final,
        "run_back": returned,
        "log": kept_log,
    }
    with open(sys.argv[3], "w", encoding="utf-8") as out:
        json.dump(found, out)


if __name__ == "__main__":
    main()
