"""Hand r4, round 3 (2026-10-25): the mended riding engine (U24_RIDES=2) with the owner's two approved mends (the swap's
complement at the mean wall (w / 2)(X0 + X1); the born lines' origin at (w / 2) X_before) and the standing-wave seed,
measured on one seed set with everything on, the branch beside it (argv 0) and R3's variant (U24_SIGN_RIDES=1, the
sign's holder's rows riding). (1) The uniform gapped torus, the sea on every Node, every act but the close, 80 forward
through the top and 80 back: MATCH per interval; the count per Node at the seed and at the top (the engine's, over W_c
at the frame's weight, and at the vacuum's weight), the drift as the control. (2) The hole seed with every act and the
close, 60 forward and 60 back: MATCH; the births' senses and their sum (the charge); the takes against the walls; the
books. (3) The standing-wave seed, P(x) P(y) P(z) about the centre with P = (-1/2, 1, -1/2) at A = 576 (now A P, before
A P cos omega = -A P / 2, zero-sum, symmetric under the 48), every act and the close, 60 forward and 60 back: MATCH; the
turns per interval with (X0, X1) at the turned Nodes; the 48 on the levels (every line's two levels) after the first
single-Node turn with X0 < X1 and at 60 (elements of 48 keeping every level); the currents' sum over the board and the
six Ports (the antisymmetry); the beat per proper interval at the centre over two spans; the count per Node and the
count at the mode's own unit, SUM share x 2 Gamma^2 div (3 den T sin_num) with sin_num the lattice's integer sine of
the mode at the centre's pace, at the seed and at the top. Outputs ride_round3_<flag>[_sign].json. Integers only."""

import itertools
import json
import os
import sys
from pathlib import Path

FLAG = sys.argv[1] if len(sys.argv) > 1 else "2"
os.environ["U24_RIDES"] = FLAG
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

import numpy as np  # noqa: E402

from event_universe import flux, node, readings, records, registry, seed, world_files  # noqa: E402
from event_universe.core import paces  # noqa: E402
from event_universe.core.rule3 import largest_below  # noqa: E402
from event_universe.lattice import Lattice  # noqa: E402
from event_universe.world_files import load_world  # noqa: E402
from tests.laws_universe import CENTRE, bare_torus, carried, node_arrays, uniform_sea  # noqa: E402

AT = (0, 0, 0)
GAMMA, DEN, T = 1000, 1021, 36000
AMPLITUDE = 576
TAG = FLAG + ("_sign" if os.environ.get("U24_SIGN_RIDES") == "1" else "")


def standing_seed(board, index):
    """The standing wave about the centre: now = A P(x) P(y) P(z), before = -now div 2 (cos omega = -1/2 at the vacuum), P = (-1/2, 1, -1/2)."""
    from event_universe.emission import emitted_lines
    from event_universe.lay import laid

    family = board.families[index]
    profile = {0: -1, 1: 2, 2: -1}  # 2 P
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


def counts(board):
    light = board.world.seed
    holder = board.held[0]
    time = board.states[holder].lines[0]
    quanta, _frozen = board.quanta(light)
    share, _frozen = board.share_of(light)
    x_centre, x_at = int(time.now[CENTRE]), int(time.now[AT])
    content = node.read(light, board.families, board.states, 1, board.world.node_clock, board.unit, 0)[0]
    content_centre = int(np.asarray(content)[CENTRE]) if np.ndim(content) else int(content)
    p0, pa = int(paces.clock(GAMMA, content_centre)), int(paces.link_pace(GAMMA, content_centre))
    total = int(np.asarray(share, dtype=object).sum())
    sin_num = largest_below((2 * GAMMA * GAMMA) ** 2 - (2 * GAMMA * GAMMA - 3 * pa * pa) ** 2)
    w_c = 3 * DEN * T
    return {
        "X_centre": x_centre, "X_origin": x_at, "p_0_centre": p0, "p_a_centre": pa, "eU_x10^6": GAMMA * 10 ** 6 // p0,
        "count_per_node_engine_centre": int(quanta[CENTRE]), "count_total_engine": int(np.asarray(quanta, dtype=object).sum()),
        "share_total": total, "count_total_vacuum_weight": total * pa * pa // (GAMMA * GAMMA * w_c),
        "count_total_mode_unit": (total * 2 * GAMMA * GAMMA) // (w_c * sin_num) if sin_num else None,
        "largest_level": int(max(abs(int(v)) for v in np.asarray(board.states[light].lines[0].now, dtype=object).reshape(-1))),
    }


def currents_sum(board):
    light = board.world.seed
    family = board.families[light]
    lines = board.lines_of(light, 0)
    through = readings.currents_of(family.pair[0], lines)
    return int(sum(int(np.asarray(port, dtype=object).sum()) for port in through))


def forty_eight(arrays):
    """The elements of the 48 under which every level array (every line's now and before) is invariant, and under which every array is."""
    levels = {k: v[:2] for k, v in arrays.items() if k[1] == "line"}
    kept_levels, kept_all = 0, 0
    for permutation in itertools.permutations(range(3)):
        for signs in itertools.product((1, -1), repeat=3):
            element = (tuple(permutation), tuple(signs))
            kept_levels += unequal(carried(levels, element), levels) == 0
            kept_all += unequal(carried(arrays, element), arrays) == 0
    return kept_levels, kept_all


def crossings(levels_at_centre):
    return sum(1 for a, b in zip(levels_at_centre, levels_at_centre[1:]) if a <= 0 < b)


def run(folder, lay, close, forward):
    board, lines = board_of(folder, forward + 10, lay)
    light, holder = board.world.seed, board.held[0]
    snapshots = [node_arrays(board)]
    first = counts(board)
    currents0 = currents_sum(board)
    turns, levels_centre, proper_centre, tops = [], [int(board.states[light].lines[0].now[CENTRE])], [0], []
    first_turn_48 = None
    top_counts, top_x, bits = None, 0, 0
    for t in range(1, forward + 1):
        before_time = snapshots[-1][(holder, "line", 0)]
        if close:
            board.step()
        else:
            board.advanced_to_the_close()
        snapshots.append(node_arrays(board))
        bits = max(bits, max(int(v).bit_length() for value in snapshots[-1].values() for x in value for v in np.asarray(x, dtype=object).reshape(-1)))
        if board.turned.any():
            nodes = [tuple(int(v) for v in n) for n in np.argwhere(board.turned)]
            pairs = [(int(before_time[1][n]), int(before_time[0][n])) for n in nodes]  # (X0, X1) at the start of the interval
            turns.append({"interval": t, "nodes": len(nodes), "X0_X1": pairs[:3]})
            if first_turn_48 is None and len(nodes) == 1 and pairs[0][0] < pairs[0][1]:
                kept_levels, kept_all = forty_eight(snapshots[-1])
                first_turn_48 = {"interval": t, "node": nodes[0], "X0_X1": pairs[0], "elements_keeping_levels": kept_levels, "elements_keeping_all": kept_all}
        x_now = int(board.states[holder].lines[0].now[CENTRE])
        if x_now > top_x:
            top_x, top_counts = x_now, dict(counts(board), interval=t)
        levels_centre.append(int(board.states[light].lines[0].now[CENTRE]))
        proper_centre.append(int(board.proper_count[CENTRE]))
    kept_levels_end, kept_all_end = forty_eight(snapshots[-1])
    half = forward // 2
    n1, n2 = crossings(levels_centre[: half + 1]), crossings(levels_centre[half:])
    p1, p2 = proper_centre[half] - proper_centre[0], proper_centre[forward] - proper_centre[half]
    beat = {
        "span": half, "crossings_first": n1, "crossings_second": n2, "proper_first": p1, "proper_second": p2,
        "K_first": n1 * GAMMA * 10 ** 6 // p1 if p1 else None, "K_second": n2 * GAMMA * 10 ** 6 // p2 if p2 else None,
    }
    births = [line for line in lines if "senses" in line]
    senses = [[int(x) for x in line["senses"]] for line in births]
    takes = [{k: line.get(k) for k in ("interval", "taken", "walls", "excess")} for line in births[:4]]
    books = {}
    for i in board.order:
        name = board.families[i].name
        standing = registry.records_of(board.families[i], board.states[i].lines)
        books[name] = {"records": int(standing), "quanta_on_board": int(board.quanta(i)[0].sum()) if standing else 0, "count_in_books": int(board.credit.counts[i]), "deficit": int(board.credit.deficits.get(i, 0))}
    end = counts(board)
    currents_end = currents_sum(board)
    matched, first_miss = 0, None
    for t in range(forward, 0, -1):
        board.step_inverse()
        bad = unequal(node_arrays(board), snapshots[t - 1])
        matched += bad == 0
        if bad and first_miss is None:
            first_miss = (t, bad)
    return {
        "forward": forward, "close": close, "intervals_matched_back": matched, "first_unmatched": first_miss,
        "turns": turns[:12], "turn_intervals": len(turns), "first_single_turn_48": first_turn_48,
        "elements_keeping_levels_at_end": kept_levels_end, "elements_keeping_all_at_end": kept_all_end,
        "currents_sum_seed": currents0, "currents_sum_end": currents_end, "beat": beat,
        "counts_seed": first, "counts_top": top_counts, "counts_end": end,
        "births": len(births), "charge_sum": sum(sum(s) for s in senses), "takes": takes, "books": books,
        "largest_state_integer_bits": bits,
    }


if __name__ == "__main__":
    base = Path(os.environ.get("TMPDIR", "/dev/shm/tmp")) / f"r4_round3_{TAG}"
    found = {"flag": FLAG, "sign_rides": os.environ.get("U24_SIGN_RIDES") == "1", "rides": flux.RIDES, "mended": getattr(flux, "MENDED", None)}
    out = HERE / f"ride_round3_{TAG}.json"
    for name, part in (
        ("sea", lambda: run(base / "sea", uniform_sea, False, 80)),
        ("hole", lambda: run(base / "hole", None, True, 60)),
        ("standing", lambda: run(base / "standing", standing_seed, True, 60)),
    ):
        found[name] = part()
        out.write_text(json.dumps(found, indent=1, default=str), encoding="utf-8")
    print(json.dumps(found, indent=1, default=str))
