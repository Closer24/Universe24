"""Hand r5 (2026-10-25): the twins of the interval under the ride (U24_RIDES=3; the forward acts are U24_RIDES=2's).

Usage: python tools/derivations/open_items/H-Fifth-Act-Under-The-Ride-5/twin.py BOARD (open | standing | hole | sea)

(1) Every per-step inverse that does not return the true pre-state is stepped forward again (every act before the close,
the close too on a closed board): where the forward act from the wrong pre-state gives the true post-state bit for bit,
two pre-states have one post-state, a twin, and no reading of the post-state can return both. Read under the local
trigger (flux.LOCAL_TOP, the false tops) and under the former reading (flux.LOCAL_TOP off, the missed tops).
(2) The reversal error at every Node and interval: delta = X2' - X0, X2' the volume's step of the swapped post-state (the
candidate the local trigger reads, the fifth act left out) and X0 the true pre-state's level before; 0 under an exact
time symmetry; with the volume's last step X0 - X1, the Node-intervals where a false top is possible by the integers
(X2 <= X1 and X2' <= X1 with the truth unturned) and where a missed top is possible (the turned Node's inverse reading
above X1). Output twin_<BOARD>.json."""

import copy
import json
import os
import sys
from pathlib import Path

BOARD = sys.argv[1] if len(sys.argv) > 1 else "open"
TWIN_FLAG = sys.argv[2] if len(sys.argv) > 2 else "3"  # 3 the ride with the local trigger; 0 the branch (the control)
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.argv = [sys.argv[0], TWIN_FLAG, BOARD]
import top_local as tl  # noqa: E402  (the paths, the seeds and the helpers; reads the flag from argv)

import numpy as np  # noqa: E402

from event_universe import flux, swap  # noqa: E402
from tests.laws_universe import node_arrays, uniform_sea  # noqa: E402



def candidate_step(board_after):
    """X2' at every Node: the swapped post-state's own step before the fifth act, captured inside the engine's own
    swap.forward_turned (the scratch board's forward act, swap.stepped wrapped to read the volume's level before it acts)."""
    captured = {}
    kept_stepped = swap.stepped

    def recording(board, kept):
        captured["x2p"] = np.asarray(board.states[board.held[0]].lines[0].now, dtype=object).copy()
        kept_stepped(board, kept)

    b = copy.deepcopy(board_after)
    swap.stepped = recording
    try:
        b.step_inverse()
    finally:
        swap.stepped = kept_stepped
    return captured["x2p"]


def main():
    lay = {"open": tl.standing_seed, "standing": tl.standing_seed, "hole": None, "sea": uniform_sea}[BOARD]
    close = BOARD in ("standing", "hole")
    forward = {"open": 80, "standing": 60, "hole": 60, "sea": 80}[BOARD]
    base = Path(os.environ.get("TMPDIR", "/dev/shm/tmp")) / f"r5_twin_{BOARD}"
    board, _lines = tl.board_of(base, forward + 10, lay)
    holder = board.held[0]
    snapshots, boards, masks = [node_arrays(board)], [copy.deepcopy(board)], [None]
    for _ in range(forward):
        if close:
            board.step()
        else:
            board.advanced_to_the_close()
        snapshots.append(node_arrays(board))
        boards.append(copy.deepcopy(board))
        masks.append(np.asarray(board.turned, dtype=bool).copy())
    found = {"board": BOARD, "forward": forward}
    for reading, local in (("local_trigger", True), ("former_reading", False)):
        flux.LOCAL_TOP = local and TWIN_FLAG == "3"
        twins = []
        for t in range(forward, 0, -1):
            b = copy.deepcopy(boards[t])
            b.step_inverse()
            if tl.unequal(node_arrays(b), snapshots[t - 1]) == 0:
                continue
            wrong = node_arrays(b)
            nodes = tl.unequal_nodes(wrong, snapshots[t - 1])
            again = copy.deepcopy(b)
            again.step() if close else again.advanced_to_the_close()
            twins.append({"interval": t, "differs_from_truth_at": nodes, "forward_of_wrong_equals_post_state": tl.unequal(node_arrays(again), snapshots[t]) == 0, "unequal_after_forward": tl.unequal(node_arrays(again), snapshots[t])})
        found[reading] = twins
    flux.LOCAL_TOP = True  # the candidate step is read through swap.forward_turned, under the branch too (the control)
    deltas, possible_false, met_false = {}, 0, 0
    largest = 0
    rows = []
    for t in range(1, forward + 1):
        x2p = candidate_step(boards[t])
        pre, post = snapshots[t - 1][(holder, "line", 0)], snapshots[t][(holder, "line", 0)]
        for n in np.ndindex(*board.shape):
            if masks[t][n]:
                continue
            x0, x1, x2, xp = int(pre[1][n]), int(pre[0][n]), int(post[0][n]), int(x2p[n])
            d = xp - x0
            deltas[d] = deltas.get(d, 0) + 1
            largest = max(largest, abs(d))
            if x2 <= x1 and x0 > x1 and x0 - x1 <= max(0, -d):
                possible_false += 1
                rows.append({"interval": t, "node": list(n), "X0": x0, "X1": x1, "X2": x2, "X2_candidate": xp})
            if bool(swap.at_top(x2, x1, xp)):
                met_false += 1
    found["delta_histogram"] = {str(k): v for k, v in sorted(deltas.items())}
    found["delta_largest_abs"] = largest
    found["false_top_conditions_met"] = possible_false
    found["false_tops_by_the_candidate_trigger"] = met_false
    found["false_top_rows"] = rows[:12]
    out = HERE / f"twin_{TWIN_FLAG}_{BOARD}.json"
    out.write_text(json.dumps(found, indent=1, default=str), encoding="utf-8")
    print(json.dumps({k: v for k, v in found.items() if k != "delta_histogram"}, default=str)[:3000])
    print("delta histogram:", json.dumps(found["delta_histogram"])[:1500])


if __name__ == "__main__":
    main()
