"""Hand R6 (2026-10-25): why the candidate pre-state's forward act does or does not reproduce the forward trigger. On
the open standing board (U24_RIDES=2), forward to t - 1 (P, the pre-state, kept), one interval to t with the fifth
act's triple recorded at every Node (Z the post-state); the candidate built from Z as swap.candidate_turned builds it
(every Node swapped and complemented), compared with P array by array at every Node (where the forward turned and
where it did not); then the candidate stepped forward to the fifth act and its triple compared with the forward's.
Usage: python diag_candidate.py <t> [seed open|hole|sea]. Integers only; prints a JSON summary."""

import copy
import json
import os
import sys
from pathlib import Path

T_AT = int(sys.argv[1]) if len(sys.argv) > 1 else 4
SEED = sys.argv[2] if len(sys.argv) > 2 else "open"
os.environ["U24_RIDES"] = "2"
sys.argv[1:] = ["2"]  # ride_local reads its flag from the arguments: the flag 2, the mended engine
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ride_local as rl  # noqa: E402  (the paths and the flag)

import numpy as np  # noqa: E402

from event_universe import swap  # noqa: E402
from tests.laws_universe import node_arrays, uniform_sea  # noqa: E402

from event_universe import flux  # noqa: E402

assert flux.RIDES and flux.MENDED, "the diagnostic runs the mended engine"
TRIPLES = []
original_acted = swap.acted


def recording_acted(board, held, direction):
    holder = rl.holder_of(board)
    if direction == 1:
        t_held, t_now = held[0][holder][0], board.states[holder].lines[0]
        TRIPLES.append(tuple(np.asarray(a, dtype=object).copy() for a in (t_held.before, t_held.now, t_now.now)))
    return original_acted(board, held, direction)


swap.acted = recording_acted


def nodes_differing(a, b, mask):
    """Per array key the count of Nodes inside `mask` and outside it where the two states differ."""
    inside, outside = {}, {}
    for key in a:
        for part, (x, y) in enumerate(zip(a[key], b[key], strict=True)):
            d = np.asarray(x, dtype=object) != np.asarray(y, dtype=object)
            n_in, n_out = int((d & mask).sum()), int((d & ~mask).sum())
            if n_in:
                inside[str((key, part))] = n_in
            if n_out:
                outside[str((key, part))] = n_out
    return inside, outside


if __name__ == "__main__":
    lay = {"open": rl.standing_seed, "hole": None, "sea": uniform_sea}[SEED]
    close = SEED == "hole"
    board, _lines = rl.board_of(Path("/dev/shm/tmp/r6_diag") / SEED, T_AT + 5, lay)
    for _ in range(T_AT - 1):
        board.step() if close else board.advanced_to_the_close()
    p_arrays = node_arrays(board)
    TRIPLES.clear()
    board.step() if close else board.advanced_to_the_close()
    x0, x1, x2 = TRIPLES[-1]
    turned = np.asarray(board.turned, dtype=bool).copy()
    held = swap.kept(board)
    cand = copy.deepcopy(board)
    cand.output, cand.observers = None, []
    cand.interval = board.interval - 1
    everywhere = np.ones(board.shape, dtype=bool)
    swap.swapped(cand, held, everywhere, -1)
    if any(swap.turns(cand.families, i) for i in cand.order):
        swap.swapped_phases(cand, held, everywhere, 1)
    c_arrays = node_arrays(cand)
    inside, outside = nodes_differing(c_arrays, p_arrays, turned)
    TRIPLES.clear()
    cand.advanced_to_the_close()
    y0, y1, y2 = TRIPLES[-1]
    cand_turned = np.asarray(cand.turned, dtype=bool)
    report = {
        "seed": SEED, "t": T_AT, "forward_turned": [tuple(int(v) for v in n) for n in np.argwhere(turned)],
        "candidate_turned": [tuple(int(v) for v in n) for n in np.argwhere(cand_turned)],
        "candidate_vs_P_differing_at_turned_nodes": inside, "candidate_vs_P_differing_elsewhere_count": len(outside),
        "triples": [],
    }
    for n in np.argwhere(turned | cand_turned):
        n = tuple(int(v) for v in n)
        report["triples"].append({"node": n, "forward": (int(x0[n]), int(x1[n]), int(x2[n])), "candidate": (int(y0[n]), int(y1[n]), int(y2[n]))})
    print(json.dumps(report, indent=1))
