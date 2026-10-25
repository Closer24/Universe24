"""Hand R6 (2026-10-25): the fifth act's two backward readings along the true forward trajectory, and the collisions
of the forward interval under the ride. At every interval t of a board (U24_RIDES=2, R4's variant with the local
mend), with the forward's turned Nodes as the truth: the candidate reading (the forward act on the post-state swapped
and complemented at every Node, swap.candidate_turned) and the base reading (R4's: the triple (Y.before, Z.before,
Z.now) with Y the engine's inverse), both read inside one step back on a copy of the post-state. A Node where the
candidate fires and the base does not holds two pre-images of the one post-state (the swapped post-state, which
turns, and the engine's inverse, which steps to it without a turn): a collision of the forward interval; the
candidate errs there where the truth did not turn (a false top), the base where it did (R4's miss). The first
collision of each kind is verified explicitly: the pre-state with the Node's arrays replaced by the other pre-image,
stepped forward, against the post-state, every array. Usage: python collisions.py <seed open|hole|sea|wave>
<intervals>; output collisions_<seed>.json beside the script. Integers only."""

import copy
import json
import os
import sys
from pathlib import Path

SEED = sys.argv[1] if len(sys.argv) > 1 else "open"
INTERVALS = int(sys.argv[2]) if len(sys.argv) > 2 else 80
os.environ["U24_RIDES"] = "2"
sys.argv[1:] = ["2"]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ride_local as rl  # noqa: E402

import numpy as np  # noqa: E402

from event_universe import flux, records, swap  # noqa: E402
from tests.laws_universe import node_arrays, uniform_sea  # noqa: E402

assert flux.RIDES and flux.MENDED
SEEN = {}
original = swap.candidate_turned


def watched(board, held):
    holder = rl.holder_of(board)
    y_time, z_time = board.states[holder].lines[0], held[0][holder][0]
    floor = swap.floor_of(board.world.node_clock)
    SEEN["base"] = np.asarray(swap.at_top(y_time.before, z_time.before, z_time.now) | swap.at_floor(y_time.before, z_time.now, floor), dtype=bool)
    cand = copy.deepcopy(board)
    cand.output, cand.observers = None, []
    cand.interval = board.interval - 1
    everywhere = np.ones(board.shape, dtype=bool)
    swap.swapped(cand, held, everywhere, -1)
    if any(swap.turns(cand.families, i) for i in cand.order):
        swap.swapped_phases(cand, held, everywhere, 1)
    SEEN["cand_board"] = copy.deepcopy(cand)
    cand.advanced_to_the_close()
    SEEN["cand"] = np.asarray(cand.turned, dtype=bool).copy()
    SEEN["y_board"] = copy.deepcopy(board)
    return SEEN["cand"]


swap.candidate_turned = watched


def node_replaced(target, source, at):
    """`target` with every array's value at the Node `at` taken from `source` (new records, nothing in place)."""
    for state, other in zip(target.states, source.states, strict=True):
        lines = []
        for line, src in zip(state.lines, other.lines, strict=True):
            parts = []
            for mine, theirs in zip((line.now, line.before, line.remainder), (src.now, src.before, src.remainder), strict=True):
                a = np.array(mine, dtype=object, copy=True)
                a[at] = np.asarray(theirs, dtype=object)[at]
                parts.append(np.asarray(a, dtype=np.asarray(mine).dtype))
            lines.append(records.Record(*parts))
        state.lines = lines
        writes = []
        for mine, theirs in zip(state.write_remainders, other.write_remainders, strict=True):
            a = np.array(mine, dtype=object, copy=True)
            a[at] = np.asarray(theirs, dtype=object)[at]
            writes.append(a)
        state.write_remainders = writes
        rows = []
        for row, src_row in zip(state.phases, other.phases, strict=True):
            new_row = []
            for line, src in zip(row, src_row, strict=True):
                parts = []
                for mine, theirs in zip((line.now, line.before, line.remainder), (src.now, src.before, src.remainder), strict=True):
                    a = np.array(mine, dtype=object, copy=True)
                    a[at] = np.asarray(theirs, dtype=object)[at]
                    parts.append(np.asarray(a, dtype=np.asarray(mine).dtype))
                new_row.append(records.Record(*parts))
            rows.append(new_row)
        state.phases = rows
    return target


def verified(p_board, other_board, at, z_arrays, close):
    """Whether the pre-state with the Node `at` replaced by the other pre-image steps to the same post-state (every array), with the count of unequal entries and the difference from the true pre-state."""
    alt = node_replaced(copy.deepcopy(p_board), other_board, at)
    differs = rl.unequal(node_arrays(alt), node_arrays(p_board))
    alt.output, alt.observers = None, []
    alt.step() if close else alt.advanced_to_the_close()
    bad = rl.unequal(node_arrays(alt), z_arrays)
    return {"node": at, "pre_images_differ_in_entries": differs, "post_states_unequal_entries": bad, "collision": differs > 0 and bad == 0}


if __name__ == "__main__":
    lay = {"open": rl.standing_seed, "hole": None, "sea": uniform_sea, "wave": rl.standing_seed}[SEED]
    close = SEED in ("hole", "wave")
    board, _lines = rl.board_of(Path(os.environ.get("TMPDIR", "/dev/shm/tmp")) / f"r6_collisions_{SEED}", INTERVALS + 5, lay)
    totals = {"turned": 0, "cand_false": 0, "cand_missed": 0, "base_missed": 0, "base_false": 0, "ambiguous": 0, "neither": 0}
    per_interval, checks = [], {}
    for t in range(1, INTERVALS + 1):
        p_board = copy.deepcopy(board)
        board.step() if close else board.advanced_to_the_close()
        truth = np.asarray(board.turned, dtype=bool).copy()
        z_arrays = node_arrays(board)
        probe = copy.deepcopy(board)
        probe.output, probe.observers = None, []
        probe.step_inverse()
        cand, base = SEEN["cand"], SEEN["base"]
        row = {
            "interval": t, "turned": int(truth.sum()), "cand_false": int((cand & ~truth).sum()), "cand_missed": int((truth & ~cand).sum()),
            "base_missed": int((truth & ~base).sum()), "base_false": int((base & ~truth).sum()), "ambiguous": int((cand & ~base).sum()), "neither": int((~cand & base).sum()),
        }
        for key in totals:
            totals[key] += row[key]
        if any(row[k] for k in ("cand_false", "cand_missed", "base_missed", "base_false")):
            row["cand_false_at"] = [tuple(int(v) for v in n) for n in np.argwhere(cand & ~truth)][:3]
            row["base_missed_at"] = [tuple(int(v) for v in n) for n in np.argwhere(truth & ~base)][:3]
            per_interval.append(row)
        if row["cand_false"] and "false_top_collision" not in checks:
            at = tuple(int(v) for v in np.argwhere(cand & ~truth)[0])
            checks["false_top_collision"] = dict(verified(p_board, SEEN["cand_board"], at, z_arrays, close), interval=t)
        if row["base_missed"] and "missed_top_collision" not in checks:
            at = tuple(int(v) for v in np.argwhere(truth & ~base)[0])
            checks["missed_top_collision"] = dict(verified(p_board, SEEN["y_board"], at, z_arrays, close), interval=t)
        rl.say(f"{SEED} t {t}: {row}")
    out = {"seed": SEED, "intervals": INTERVALS, "close": close, "totals": totals, "checks": checks, "per_interval": per_interval}
    (HERE / f"collisions_{SEED}.json").write_text(json.dumps(out, indent=1, default=str), encoding="utf-8")
    print(json.dumps({"totals": totals, "checks": checks}, indent=1, default=str))
