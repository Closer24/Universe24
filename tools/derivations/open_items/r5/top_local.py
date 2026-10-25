"""Hand r5 (2026-10-25): the fifth act at a single-Node top under the ride, the local mend measured.

Usage: python tools/derivations/r5/top_local.py <flag> <board> [forward]
FLAG: the value of U24_RIDES (0 the branch, 2 R4's form A with the two mends, 3 the same with the local backward trigger).
BOARD: open (the standing wave, every act but the close), standing (the standing wave with the close), hole (the law's
hole seed with the close), sea (the uniform sea, every act but the close).

Per interval forward: the state's arrays, a deep copy of the board, the Nodes the fifth act turned (the truth).
Then (i) the per-step inverse: from every true post-state (the copy at t) one step back, compared with the state at
t - 1 (MATCH per step), the backward mask against the forward mask: misses (turned forward, not turned back) and false
tops (turned back, not turned forward), for the mask the engine used and, under FLAG 3, for the former reading beside it
(board.bijection_turned); (ii) the chained run back from the end, MATCH per interval; (iii) the 48 of the levels at the
first single-Node turn with X0 < X1 and at the end, and of every backward mask (symmetric lays alone); (iv) the counts at
the seed, at the top and at the end, the births with their senses' sum and the takes; (v) the riding linear sum of the
light (the centred momentum's sum) per interval. Integers only. Output top_local_<FLAG>_<BOARD>.json beside the script."""

import copy
import itertools
import json
import os
import sys
from pathlib import Path

FLAG = sys.argv[1] if len(sys.argv) > 1 else "3"
BOARD = sys.argv[2] if len(sys.argv) > 2 else "open"
if FLAG != "0":
    os.environ["U24_RIDES"] = FLAG
else:
    os.environ.pop("U24_RIDES", None)
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, os.environ.get("U24_SRC", str(ROOT / "src")))  # U24_SRC: another tree's src (the pristine branch for the off-path digest)

import numpy as np  # noqa: E402

from event_universe import flux, node, readings, records, registry, seed, world_files  # noqa: E402
from event_universe.core import paces  # noqa: E402
from event_universe.core.rule3 import largest_below, wall_of  # noqa: E402
from event_universe.lattice import Lattice  # noqa: E402
from event_universe.world_files import load_world  # noqa: E402
from tests.laws_universe import CENTRE, bare_torus, carried, node_arrays, uniform_sea  # noqa: E402

AT = (0, 0, 0)
GAMMA, DEN, T = 1000, 1021, 36000
AMPLITUDE = int(os.environ.get("R5_AMPLITUDE", "576"))
ELEMENTS = [(tuple(p), tuple(s)) for p in itertools.permutations(range(3)) for s in itertools.product((1, -1), repeat=3)]


def standing_seed(board, index):
    """R4's standing wave about the centre: now = A P(x) P(y) P(z), before = -now div 2, P = (-1/2, 1, -1/2)."""
    from event_universe.emission import emitted_lines
    from event_universe.lay import laid

    family = board.families[index]
    profile = {0: -1, 1: 2, 2: -1}
    now = np.zeros(board.shape, dtype=object)
    for x in range(3):
        for y in range(3):
            for z in range(3):
                now[x, y, z] = AMPLITUDE * profile[x] * profile[y] * profile[z] // 8
    before = np.array([[[-int(v) // 2 for v in row] for row in plane] for plane in now], dtype=object)
    first = records.record_slice(family, 0).start
    for line in emitted_lines(family):
        laid(board, index, first + line, (now, before), None, None)


def board_of(folder, intervals, lay):
    folder.mkdir(parents=True, exist_ok=True)
    world_files.REPOSITORY_ROOT = folder
    lines = []
    kept = seed.uniform_seed
    if lay is not None:
        seed.uniform_seed = lay
    try:
        board = Lattice(load_world(bare_torus(folder, 3, intervals)), output=lines.append)
    finally:
        seed.uniform_seed = kept
    return board, lines


def unequal(a, b):
    total = 0
    for key in set(a) | set(b):
        if key not in a or key not in b:
            total += 1
            continue
        for x, y in zip(a[key], b[key], strict=True):
            total += int((np.asarray(x, dtype=object) != np.asarray(y, dtype=object)).sum())
    return total


def unequal_nodes(a, b):
    """The Nodes at which any array differs."""
    found = np.zeros((3, 3, 3), dtype=bool)
    for key in set(a) & set(b):
        for x, y in zip(a[key], b[key], strict=True):
            found |= np.asarray(np.asarray(x, dtype=object) != np.asarray(y, dtype=object), dtype=bool)
    return [tuple(int(v) for v in n) for n in np.argwhere(found)]


def counts(board):
    light = board.world.seed
    holder = board.held[0]
    time = board.states[holder].lines[0]
    quanta, _frozen = board.quanta(light)
    share, _frozen = board.share_of(light)
    x_centre = int(time.now[CENTRE])
    content = node.read(light, board.families, board.states, 1, board.world.node_clock, board.unit, 0)[0]
    content_centre = int(np.asarray(content)[CENTRE]) if np.ndim(content) else int(content)
    p0, pa = int(paces.clock(GAMMA, content_centre)), int(paces.link_pace(GAMMA, content_centre))
    total = int(np.asarray(share, dtype=object).sum())
    w_c = 3 * DEN * T
    vacuum = np.asarray(share, dtype=object) * pa * pa // (GAMMA * GAMMA * w_c)
    return {
        "X_centre": x_centre, "X_largest": int(max(int(v) for v in np.asarray(time.now, dtype=object).reshape(-1))),
        "eU_x10^6_centre": GAMMA * 10 ** 6 // p0,
        "count_engine_centre": int(quanta[CENTRE]), "count_engine_largest": int(np.asarray(quanta, dtype=object).max()),
        "count_engine_total": int(np.asarray(quanta, dtype=object).sum()),
        "share_total": total, "count_total_vacuum_weight": total * pa * pa // (GAMMA * GAMMA * w_c),
        "count_vacuum_weight_largest_node": int(vacuum.max()),
        "largest_level": int(max(abs(int(v)) for v in np.asarray(board.states[light].lines[0].now, dtype=object).reshape(-1))),
    }


def riding_sum(board):
    """The light's centred momentum summed over the board, SUM [w X_before (now - before) + r - (w X_before) div 2] (the ride's L);
    under the branch the plain L = SUM [w (now - before) + r]."""
    light = board.world.seed
    line = board.states[light].lines[0]
    wall = wall_of(board.families[light].pair[1], board.world.node_clock, board.unit)
    now, before, r = (np.asarray(a, dtype=object) for a in (line.now, line.before, line.remainder))
    if getattr(flux, "RIDES", False):
        time = board.states[board.held[0]].lines[0]
        xb = np.asarray(time.before, dtype=object)
        return int((wall * xb * (now - before) + r - (wall * xb) // 2).sum())
    return int((wall * (now - before) + r).sum())


def moved(a, element, about):
    """One of the 48 about the Node `about` (the centre, or the origin by a roll of the torus)."""
    permutation, signs = element
    a = np.asarray(a)
    if about == AT:
        a = np.roll(a, 1, axis=(0, 1, 2))
    a = np.transpose(a, permutation)
    a = a[tuple(slice(None, None, -1) if s < 0 else slice(None) for s in signs)]
    if about == AT:
        a = np.roll(a, -1, axis=(0, 1, 2))
    return a


def levels_48(arrays, about):
    """The elements of the 48 (about `about`) under which every line's two levels are invariant (R4's reading, the axis
    lines of the held rows permuted; the sign's odd lines carried with no sign, as tests/laws_universe.carried does)."""
    levels = {k: v[:2] for k, v in arrays.items() if k[1] == "line"}
    if about == AT:
        levels = {k: tuple(np.roll(a, 1, axis=(0, 1, 2)) for a in v) for k, v in levels.items()}
    return sum(1 for e in ELEMENTS if unequal(carried(levels, e), levels) == 0)


def mask_48(mask, about):
    return sum(1 for e in ELEMENTS if np.array_equal(moved(mask, e, about), mask))


def bits_of(arrays):
    return max(int(v).bit_length() for value in arrays.values() for x in value for v in np.asarray(x, dtype=object).reshape(-1))


def run(board_name, forward):
    base = Path(os.environ.get("TMPDIR", "/dev/shm/tmp")) / f"r5_top_{FLAG}_{board_name}"
    lay = {"open": standing_seed, "standing": standing_seed, "hole": None, "sea": uniform_sea}[board_name]
    close = board_name in ("standing", "hole")
    about = AT if board_name == "hole" else CENTRE
    board, lines = board_of(base, forward + 10, lay)
    light, holder = board.world.seed, board.held[0]
    snapshots, boards, masks, triples = [node_arrays(board)], [copy.deepcopy(board)], [None], [None]
    sums = [riding_sum(board)]
    found = {"flag": FLAG, "board": board_name, "forward": forward, "close": close, "amplitude": AMPLITUDE if lay is standing_seed else None}
    found["counts_seed"] = counts(board)
    top_x, top_counts, first_single = 0, None, None
    turns = []
    for t in range(1, forward + 1):
        pre_time = snapshots[-1][(holder, "line", 0)]
        if close:
            board.step()
        else:
            board.advanced_to_the_close()
        arrays = node_arrays(board)
        snapshots.append(arrays)
        boards.append(copy.deepcopy(board))
        mask = np.asarray(board.turned, dtype=bool).copy()
        masks.append(mask)
        sums.append(riding_sum(board))
        if mask.any():
            nodes = [tuple(int(v) for v in n) for n in np.argwhere(mask)]
            pairs = [(int(pre_time[1][n]), int(pre_time[0][n])) for n in nodes]  # (X0, X1) at the interval's start
            turns.append({"interval": t, "nodes": len(nodes), "X0_X1": pairs[:4], "at": nodes[:4]})
            if first_single is None and len(nodes) == 1 and pairs[0][0] < pairs[0][1] and lay is not None:
                first_single = {"interval": t, "node": nodes[0], "X0_X1": pairs[0], "elements_keeping_levels": levels_48(arrays, about)}
        x_now = int(np.asarray(board.states[holder].lines[0].now, dtype=object).max())
        if x_now > top_x:
            top_x, top_counts = x_now, dict(counts(board), interval=t)
    import hashlib

    digest = hashlib.sha256()
    for arrays in snapshots:
        for key in sorted(arrays, key=str):
            for a in arrays[key]:
                digest.update(repr((str(key), [int(v) for v in np.asarray(a, dtype=object).reshape(-1)])).encode())
    found["digest_of_every_forward_array"] = digest.hexdigest()
    found["turn_intervals"] = len(turns)
    found["turns"] = turns[:40]
    found["first_single_turn_48"] = first_single
    found["levels_48_at_end"] = levels_48(snapshots[-1], about)
    found["counts_top"] = top_counts
    found["counts_end"] = counts(board)
    found["largest_state_integer_bits"] = max(bits_of(a) for a in snapshots)
    births = [line for line in lines if "senses" in line]
    found["births"] = len(births)
    found["birth_intervals"] = sorted({int(line.get("interval", -1)) for line in births})
    found["charge_sum"] = sum(sum(int(x) for x in line["senses"]) for line in births)
    found["takes"] = [{k: line.get(k) for k in ("interval", "taken", "walls", "excess")} for line in births[:4]]
    found["riding_sum_changes"] = [sums[t] - sums[t - 1] for t in range(1, len(sums))]
    found["riding_sum_changes_off_turns"] = sorted({sums[t] - sums[t - 1] for t in range(1, len(sums)) if not masks[t].any()})
    # (i) the per-step inverse from every true post-state
    per_step, misses, false_tops, old_misses, old_false, mask_kept, detail = 0, 0, 0, 0, 0, 0, []
    unmatched = []
    for t in range(forward, 0, -1):
        b = copy.deepcopy(boards[t])
        b.step_inverse()
        bad = unequal(node_arrays(b), snapshots[t - 1])
        per_step += bad == 0
        truth = masks[t]
        back = np.asarray(b.turned, dtype=bool)
        miss = int((truth & ~back).sum())
        false = int((back & ~truth).sum())
        misses, false_tops = misses + miss, false_tops + false
        mask_kept += mask_48(back, about) if lay is not None else 0
        old = getattr(b, "bijection_turned", None)
        if old is not None:
            old = np.asarray(old, dtype=bool)
            old_misses += int((truth & ~old).sum())
            old_false += int((old & ~truth).sum())
        if bad:
            unmatched.append({"interval": t, "unequal": bad, "nodes": unequal_nodes(node_arrays(b), snapshots[t - 1])[:6], "miss": miss, "false": false})
        if miss or false:
            nodes = [tuple(int(v) for v in n) for n in np.argwhere(truth ^ back)]
            pre = snapshots[t - 1][(holder, "line", 0)]
            post = snapshots[t][(holder, "line", 0)]
            detail.append({"interval": t, "nodes": nodes[:4], "pre_X0_X1": [(int(pre[1][n]), int(pre[0][n])) for n in nodes[:4]], "post_now_before": [(int(post[0][n]), int(post[1][n])) for n in nodes[:4]], "miss": miss, "false": false})
    found["per_step_matched"] = per_step
    found["per_step_unmatched"] = unmatched[:12]
    found["turned_nodes_forward"] = int(sum(int(m.sum()) for m in masks[1:]))
    found["backward_misses"] = misses
    found["backward_false_tops"] = false_tops
    found["former_reading_misses"] = old_misses if FLAG == "3" else None
    found["former_reading_false_tops"] = old_false if FLAG == "3" else None
    found["mismatch_detail"] = detail[:12]
    found["backward_masks_48_elements_total"] = mask_kept if lay is not None else None
    # (ii) the chained run back
    matched, first_miss = 0, None
    for t in range(forward, 0, -1):
        board.step_inverse()
        bad = unequal(node_arrays(board), snapshots[t - 1])
        matched += bad == 0
        if bad and first_miss is None:
            first_miss = (t, bad)
    found["chained_matched"] = matched
    found["chained_first_unmatched"] = first_miss
    return found


if __name__ == "__main__":
    forward = int(sys.argv[3]) if len(sys.argv) > 3 else {"open": 80, "standing": 60, "hole": 60, "sea": 80}[BOARD]
    result = run(BOARD, forward)
    tag = "" if AMPLITUDE == 576 else f"_A{AMPLITUDE}"
    out = HERE / f"top_local_{FLAG}_{BOARD}{tag}.json"
    out.write_text(json.dumps(result, indent=1, default=str), encoding="utf-8")
    keys = ("per_step_matched", "chained_matched", "chained_first_unmatched", "turn_intervals", "turned_nodes_forward", "backward_misses", "backward_false_tops", "former_reading_misses", "former_reading_false_tops", "births", "charge_sum", "largest_state_integer_bits")
    print(json.dumps({k: result[k] for k in keys}, default=str))
