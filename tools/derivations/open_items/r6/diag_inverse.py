"""Hand R6 (2026-10-25): the candidate as the engine's inverse builds it (inside Lattice.step_inverse, on the board the
engine's inverse left), against the pre-state P: at interval t of the open standing board (U24_RIDES=2), the
candidate's arrays against P's at the forward-turned Nodes, the write walls the inverse holds against the forward's,
the candidate's triple against the forward's, and the state after the step back against P. Usage: python
diag_inverse.py <t>. Integers only; prints a JSON summary."""

import copy
import json
import os
import sys
from pathlib import Path

T_AT = int(sys.argv[1]) if len(sys.argv) > 1 else 4
os.environ["U24_RIDES"] = "2"
sys.argv[1:] = ["4", "open"]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import diag_candidate as dc  # noqa: E402  (the paths, the flag and the recording of the triples)
import ride_local as rl  # noqa: E402

import numpy as np  # noqa: E402

from event_universe import swap  # noqa: E402
from tests.laws_universe import node_arrays  # noqa: E402

SEEN = {}
original = swap.candidate_turned


def watched(board, held):
    SEEN["walls_inverse"] = {k: [int(np.asarray(w, dtype=object).reshape(-1)[0]) if np.ndim(w) else int(w) for w in v] for k, v in board.write_walls.items()}
    cand = copy.deepcopy(board)
    cand.output, cand.observers = None, []
    cand.interval = board.interval - 1
    everywhere = np.ones(board.shape, dtype=bool)
    swap.swapped(cand, held, everywhere, -1)
    if any(swap.turns(cand.families, i) for i in cand.order):
        swap.swapped_phases(cand, held, everywhere, 1)
    SEEN["candidate"] = node_arrays(cand)
    dc.TRIPLES.clear()
    cand.advanced_to_the_close()
    SEEN["triple"] = dc.TRIPLES[-1]
    SEEN["cand_turned"] = np.asarray(cand.turned, dtype=bool).copy()
    found = original(board, held)
    SEEN["returned"] = np.asarray(found, dtype=bool).copy()
    return found


swap.candidate_turned = watched

if __name__ == "__main__":
    board, _lines = rl.board_of(Path("/dev/shm/tmp/r6_diag_inv"), T_AT + 5, rl.standing_seed)
    for _ in range(T_AT - 1):
        board.advanced_to_the_close()
    p_arrays = node_arrays(board)
    dc.TRIPLES.clear()
    board.advanced_to_the_close()
    forward_triple = dc.TRIPLES[-1]
    turned = np.asarray(board.turned, dtype=bool).copy()
    walls_forward = {k: [int(np.asarray(w, dtype=object).reshape(-1)[0]) if np.ndim(w) else int(w) for w in v] for k, v in board.write_walls.items()}
    board.step_inverse()
    back = node_arrays(board)
    inside, outside = dc.nodes_differing(SEEN["candidate"], p_arrays, turned)
    after_in, after_out = dc.nodes_differing(back, p_arrays, turned)
    triples = []
    for n in np.argwhere(turned | SEEN["cand_turned"]):
        n = tuple(int(v) for v in n)
        f = tuple(int(a[n]) for a in forward_triple)
        c = tuple(int(a[n]) for a in SEEN["triple"])
        if f != c:
            triples.append({"node": n, "forward": f, "candidate": c})
    print(json.dumps({
        "t": T_AT, "forward_turned": int(turned.sum()), "candidate_turned": int(SEEN["cand_turned"].sum()),
        "returned_equal_candidate": bool((SEEN["returned"] == SEEN["cand_turned"]).all()),
        "masks_equal": bool((SEEN["cand_turned"] == turned).all()),
        "walls_equal": walls_forward == SEEN["walls_inverse"],
        "candidate_vs_P_at_turned": inside, "candidate_vs_P_elsewhere_keys": sorted(outside)[:6],
        "after_step_back_vs_P_at_turned": after_in, "after_step_back_vs_P_elsewhere": after_out,
        "differing_triples": triples[:8],
    }, indent=1, default=str))
