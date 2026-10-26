"""vf11: the plasma run to N by the test's method (test_the_board.py, PL-S1): the tops, X = Gamma where, the credits and the laid back, the run back 10 through the top, the retrace at every k."""
import json
import sys
from typing import Any

import numpy as np

sys.set_int_max_str_digits(0)
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.rows import CARRIER, POTENTIAL  # noqa: E402


def state_of(node):
    return node.state_bytes().decode() + f" {node.interval}"


def main(argv):
    universe, world = load_world(argv[1])
    n = int(argv[2])
    node = Node(universe, dict(world, intervals=n))
    states, kept, exact, tops, bits = [], [], [], [], 0
    wr_time = []
    for _ in range(n):
        states.append([[line.copy() for line in row] for row in node.rows()])
        kept.append(state_of(node))
        node.step()
        bits = max(bits, node.census()[1])
        x = node.row(CARRIER).lines[0].now
        exact.append(int(x.min()) == int(x.max()) == node.gamma)
        wr_time.append(int(node.row(POTENTIAL).lines[0].wr.reshape(-1)[0]))
        if node.turned.any():
            tops.append((node.interval, int(node.turned.sum())))
    states.append([[line.copy() for line in row] for row in node.rows()])
    credits = [e for e in node.log if e["event"] == "credit"]
    top = tops[0][0]
    out: dict[str, Any] = {
        "world": argv[1], "intervals": n, "tops": tops, "top": top,
        "x_equals_gamma_at": [i + 1 for i, e in enumerate(exact) if e],
        "credits": len(credits),
        "laid_back": sum(1 for c in credits if "laid_back" in c),
        "credits_in_rise": sum(1 for c in credits if c["i"] < top),
        "births": node.counts["births"], "laid": node.counts["laid"],
        "census_integers": node.census()[0], "max_bits_seen": bits,
        "max_transient_bits": node.max_transient,
        "counts": {k: int(v) for k, v in node.counts.items()},
        "time_line_wr_node0_first_12_after_top": wr_time[top - 2 : top + 10],
    }
    # the run back 10 through the top: back to top + 6, then 10 compared down to top - 4
    window = list(range(top - 4, top + 6))
    for _ in range(n - (top + 6)):
        node.step_back()
    assert node.interval == top + 6
    hits = 0
    for k in range(10):
        node.step_back()
        hits += state_of(node) == kept[window[9 - k]]
    out["run_back_through_top"] = {"window": [window[0], window[-1]], "exact": hits, "of": 10}
    everywhere = np.ones(node.shape, dtype=bool)

    def text(rows, exchanged):
        node.set_rows([[line.copy() for line in row] for row in rows])
        if exchanged:
            node.exchange(everywhere, rows)
        return node.state_bytes()

    out["retrace"] = []
    for t, _count in tops:
        ks = range(1, min(t, n - t + 1))
        hits = [k for k in ks if text(states[t + k], False) == text(states[t - 1 - k], True)]
        parted = [k for k in ks if k not in hits]
        out["retrace"].append({"top": t, "equal": len(hits), "of": len(ks), "first_parted_k": parted[:5]})
    with open(argv[3], "w", encoding="utf-8") as f:
        json.dump(out, f)
    print(json.dumps(out))


if __name__ == "__main__":
    main(sys.argv)
