"""Hand R6 (2026-10-25), the fourth round of the riding line: the fifth act at a single-Node top under the ride, measured
on R4's seed set (the standing wave with every act but the close, 80 intervals; the hole seed with every act and the
close, 60; the uniform sea with every act but the close, 80 through its top) under the flag U24_RIDES=2 (R4's
variant_src.diff applied, form A, the mean-wall complement, the half-wall origin), before the local mend (tag base)
and with it (tag mend). Per board: the run back MATCH per interval; the backward trigger against the forward turns at
every interval (the false tops, fired back where the forward did not turn; the missed tops, the forward turn the
inverse did not fire); the turns with (X0, X1) at the turned Nodes; the 48 on the levels and on every array at the
first single-Node turn with X0 < X1, at every interval of the first 20 and at the end; the currents' sum over the
board and the six Ports; the counts at the seed, the top and the end (the engine's, the vacuum's weight, the mode's
unit); the births, their senses' sum (the charge) and the takes against the walls (the clicks); the centred momenta's
sum L_ride and its exact identity per interval with no turn (L_out - L_in = SUM X_now F); the widest integer in bits.
Integers only, no float. Usage: python ride_local.py <flag> <parts> <tag>, parts among open,hole,sea; outputs
ride_local_<flag>_<tag>.json and .log beside the script."""

import hashlib
import itertools
import json
import os
import sys
from pathlib import Path

FLAG = sys.argv[1] if len(sys.argv) > 1 else "2"
PARTS = sys.argv[2].split(",") if len(sys.argv) > 2 else ["open", "hole", "sea"]
TAG = sys.argv[3] if len(sys.argv) > 3 else "base"
FORWARD = int(sys.argv[4]) if len(sys.argv) > 4 else 0  # a shorter run for a smoke check, 0 the boards' own lengths
if FLAG == "0":
    os.environ.pop("U24_RIDES", None)
else:
    os.environ["U24_RIDES"] = FLAG
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

import numpy as np  # noqa: E402

from event_universe import flux, node, readings, records, registry, seed, world_files  # noqa: E402
from event_universe.core import paces  # noqa: E402
from event_universe.core.rule3 import largest_below, wall_of  # noqa: E402
from event_universe.emission import emitted_lines  # noqa: E402
from event_universe.lattice import Lattice  # noqa: E402
from event_universe.lay import laid  # noqa: E402
from event_universe.world_files import load_world  # noqa: E402
from tests.laws_universe import CENTRE, bare_torus, carried, node_arrays, uniform_sea  # noqa: E402

AT = (0, 0, 0)
GAMMA, DEN, T = 1000, 1021, 36000
AMPLITUDE = 576  # R4's standing wave, the owner's seed of the third round
LOG = []


def say(text):
    LOG.append(text)
    print(text, flush=True)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()[:16]


def standing_seed(board, index, amplitude=AMPLITUDE):
    """R4's standing wave about the centre: now = A P(x) P(y) P(z), before = -now div 2, P = (-1/2, 1, -1/2)."""
    family = board.families[index]
    profile = {0: -1, 1: 2, 2: -1}  # 2 P
    now = np.zeros(board.shape, dtype=object)
    for x in range(3):
        for y in range(3):
            for z in range(3):
                now[x, y, z] = amplitude * profile[x] * profile[y] * profile[z] // 8
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


def holder_of(board):
    return [i for i in board.held if board.families[i].motion_volume][0]


def counts(board):
    light = board.world.seed
    time = board.states[holder_of(board)].lines[0]
    quanta, _frozen = board.quanta(light)
    share, _frozen = board.share_of(light)
    content = node.read(light, board.families, board.states, 1, board.world.node_clock, board.unit, 0)[0]
    content_centre = int(np.asarray(content)[CENTRE]) if np.ndim(content) else int(content)
    p0, pa = int(paces.clock(GAMMA, content_centre)), int(paces.link_pace(GAMMA, content_centre))
    total = int(np.asarray(share, dtype=object).sum())
    sin_num = largest_below((2 * GAMMA * GAMMA) ** 2 - (2 * GAMMA * GAMMA - 3 * pa * pa) ** 2)
    w_c = 3 * DEN * T
    per_node = [int(v) for v in np.asarray(quanta, dtype=object).reshape(-1)]
    return {
        "X_centre": int(time.now[CENTRE]), "X_origin": int(time.now[AT]), "X_max": int(max(int(v) for v in np.asarray(time.now, dtype=object).reshape(-1))),
        "p_0_centre": p0, "eU_x10^6_centre": GAMMA * 10 ** 6 // p0,
        "count_per_node_engine_centre": int(quanta[CENTRE]), "count_total_engine": sum(per_node),
        "nodes_at_one_or_more_quanta": sum(1 for v in per_node if v >= 1),
        "share_total": total, "count_total_vacuum_weight": total * pa * pa // (GAMMA * GAMMA * w_c),
        "count_total_mode_unit": (total * 2 * GAMMA * GAMMA) // (w_c * sin_num) if sin_num else None,
        "largest_level": int(max(abs(int(v)) for v in np.asarray(board.states[light].lines[0].now, dtype=object).reshape(-1))),
    }


def currents_sum(board):
    light = board.world.seed
    through = readings.currents_of(board.families[light].pair[0], board.lines_of(light, 0))
    return int(sum(int(np.asarray(port, dtype=object).sum()) for port in through))


def forty_eight(arrays):
    """The elements of the 48 under which every level array is invariant, and under which every array is."""
    levels = {k: v[:2] for k, v in arrays.items() if k[1] == "line"}
    kept_levels, kept_all = 0, 0
    for permutation in itertools.permutations(range(3)):
        for signs in itertools.product((1, -1), repeat=3):
            element = (tuple(permutation), tuple(signs))
            kept_levels += unequal(carried(levels, element), levels) == 0
            kept_all += unequal(carried(arrays, element), arrays) == 0
    return kept_levels, kept_all


def momenta(board):
    """The light line's centred riding momentum summed over the board, L_ride = SUM [w X_before (now - before) + r - (w X_before) div 2], and the branch's L = SUM [w (now - before) + r]; and SUM over the Nodes of X_now F with F the Links' sum of the level now (the drift of L_ride over the interval, the identity L_out = L_in + SUM X_now F)."""
    light = board.world.seed
    time = board.states[holder_of(board)].lines[0]
    line = board.states[light].lines[0]
    w = wall_of(DEN, GAMMA, board.unit)
    now, before, r = (np.asarray(x, dtype=object) for x in (line.now, line.before, line.remainder))
    x_before, x_now = np.asarray(time.before, dtype=object), np.asarray(time.now, dtype=object)
    rho = w * x_before * (now - before) + r - (w * x_before) // 2
    plain = w * (now - before) + r
    content, factors = node.read(light, board.families, board.states, 1, GAMMA, board.unit, 0)
    rule = node.rule_of(board.families[light], GAMMA, content, factors, board.unit)
    force = np.asarray(flux.link_fluxes(now, rule.reaches), dtype=object) - rule.mass * now
    return int(rho.sum()), int(plain.sum()), int((x_now * force).sum())


def bits_of(arrays):
    return max(int(v).bit_length() for value in arrays.values() for x in value for v in np.asarray(x, dtype=object).reshape(-1))


def run(folder, lay, close, forward, name):
    board, lines = board_of(folder, forward + 10, lay)
    light, holder = board.world.seed, holder_of(board)
    snapshots = [node_arrays(board)]
    forward_turned = [None]
    first = counts(board)
    currents0 = currents_sum(board)
    turns, tops_x, bits = [], [], bits_of(snapshots[0])
    first_turn_48, top_counts, top_x = None, None, 0
    per_interval_48 = []
    l_identity = []  # per interval with no turned Node: (L_in, L_out, SUM X F, residual)
    l_turn_intervals = 0
    for t in range(1, forward + 1):
        before_time = snapshots[-1][(holder, "line", 0)]
        l_in, plain_in, drift = momenta(board)
        if close:
            board.step()
        else:
            board.advanced_to_the_close()
        snapshots.append(node_arrays(board))
        forward_turned.append(np.asarray(board.turned, dtype=bool).copy())
        bits = max(bits, bits_of(snapshots[-1]))
        if board.turned.any():
            l_turn_intervals += 1
            nodes = [tuple(int(v) for v in n) for n in np.argwhere(board.turned)]
            pairs = [(int(before_time[1][n]), int(before_time[0][n])) for n in nodes]  # (X0, X1) at the interval's start
            turns.append({"interval": t, "nodes": len(nodes), "X0_X1": pairs[:3], "at": nodes[:3]})
            if first_turn_48 is None and len(nodes) == 1 and pairs[0][0] < pairs[0][1]:
                kept_levels, kept_all = forty_eight(snapshots[-1])
                first_turn_48 = {"interval": t, "node": nodes[0], "X0_X1": pairs[0], "elements_keeping_levels": kept_levels, "elements_keeping_all": kept_all}
        else:
            l_out, plain_out, _drift_out = momenta(board)
            l_identity.append({"interval": t, "L_in": l_in, "L_out": l_out, "sum_X_F": drift, "residual": l_out - l_in - drift, "plain_L_change": plain_out - plain_in})
        if t <= 20:
            kept_levels, kept_all = forty_eight(snapshots[-1])
            per_interval_48.append({"interval": t, "levels": kept_levels, "all": kept_all, "turned": int(board.turned.sum())})
        x_now = int(board.states[holder].lines[0].now[CENTRE])
        if x_now > top_x:
            top_x, top_counts = x_now, dict(counts(board), interval=t)
    kept_levels_end, kept_all_end = forty_eight(snapshots[-1])
    births = [line for line in lines if "senses" in line]
    senses = [[int(x) for x in line["senses"]] for line in births]
    takes = [{k: line.get(k) for k in ("interval", "taken", "walls", "excess")} for line in births]
    exact_takes = sum(1 for line in births if int(line["taken"]) == int(line["walls"]) + int(line["excess"]))
    credits = [line for line in lines if line.get("event") == "credit"]
    books = {}
    for i in board.order:
        fam = board.families[i]
        standing = registry.records_of(fam, board.states[i].lines)
        books[fam.name] = {"records": int(standing), "quanta_on_board": int(board.quanta(i)[0].sum()) if standing else 0, "count_in_books": int(board.credit.counts[i]), "deficit": int(board.credit.deficits.get(i, 0))}
    end = counts(board)
    currents_end = currents_sum(board)
    matched, first_miss, false_tops, missed_tops, back_turn_intervals = 0, None, 0, 0, 0
    false_top_places, missed_places = [], []
    for t in range(forward, 0, -1):
        board.step_inverse()
        back = np.asarray(board.turned, dtype=bool)
        fwd = forward_turned[t]
        back_turn_intervals += int(back.any())
        false_here, missed_here = int((back & ~fwd).sum()), int((~back & fwd).sum())
        false_tops += false_here
        missed_tops += missed_here
        if false_here and len(false_top_places) < 12:
            false_top_places.append({"interval": t, "nodes": [tuple(int(v) for v in n) for n in np.argwhere(back & ~fwd)][:3]})
        if missed_here and len(missed_places) < 12:
            missed_places.append({"interval": t, "nodes": [tuple(int(v) for v in n) for n in np.argwhere(~back & fwd)][:3]})
        bad = unequal(node_arrays(board), snapshots[t - 1])
        matched += bad == 0
        if bad and first_miss is None:
            first_miss = (t, bad)
    found = {
        "board": name, "forward": forward, "close": close, "intervals_matched_back": matched, "first_unmatched": first_miss,
        "turn_intervals_forward": len(turns), "turn_intervals_back": back_turn_intervals, "turns": turns[:40],
        "false_tops": false_tops, "false_top_places": false_top_places, "missed_tops": missed_tops, "missed_places": missed_places,
        "first_single_turn_48": first_turn_48, "per_interval_48": per_interval_48,
        "elements_keeping_levels_at_end": kept_levels_end, "elements_keeping_all_at_end": kept_all_end,
        "currents_sum_seed": currents0, "currents_sum_end": currents_end,
        "counts_seed": first, "counts_top": top_counts, "counts_end": end,
        "births": len(births), "charge_sum": sum(sum(s) for s in senses), "takes": takes[:6], "exact_takes": exact_takes,
        "credits": len(credits), "books": books, "largest_state_integer_bits": bits,
        "L_identity_intervals": len(l_identity), "L_identity_residual_zero": sum(1 for d in l_identity if d["residual"] == 0),
        "L_identity_drift_nonzero": sum(1 for d in l_identity if d["sum_X_F"] != 0), "L_plain_changed": sum(1 for d in l_identity if d["plain_L_change"] != 0),
        "L_identity_first": l_identity[:4], "L_identity_last": l_identity[-2:],
    }
    say(f"{name}: MATCH {matched} of {forward}, first unmatched {first_miss}; turns forward {len(turns)} intervals, back {back_turn_intervals}; false tops {false_tops}, missed tops {missed_tops}; 48 at end levels {kept_levels_end} all {kept_all_end}; bits {bits}; births {len(births)} charge sum {found['charge_sum']} exact takes {exact_takes} of {len(births)}")
    return found


if __name__ == "__main__":
    base = Path(os.environ.get("TMPDIR", "/dev/shm/tmp")) / f"r6_ride_local_{FLAG}_{TAG}"
    found = {"flag": FLAG, "tag": TAG, "rides": flux.RIDES, "mended": getattr(flux, "MENDED", None),
             "swap_py_sha256_16": digest(ROOT / "src/event_universe/swap.py"), "lattice_py_sha256_16": digest(ROOT / "src/event_universe/lattice.py"),
             "flux_py_sha256_16": digest(ROOT / "src/event_universe/flux.py")}
    say(f"flag {FLAG} tag {TAG} rides {flux.RIDES} mended {found['mended']} swap.py {found['swap_py_sha256_16']}")
    out = HERE / f"ride_local_{FLAG}_{TAG}.json"
    parts = {
        "open": lambda: run(base / "open", standing_seed, False, FORWARD or 80, "standing wave, open (no close)"),
        "hole": lambda: run(base / "hole", None, True, FORWARD or 60, "hole seed, every act and the close"),
        "sea": lambda: run(base / "sea", uniform_sea, False, FORWARD or 80, "uniform sea, open (no close)"),
        "wave": lambda: run(base / "wave", standing_seed, True, FORWARD or 60, "standing wave A 576, every act and the close"),
    }
    for name in PARTS:
        found[name] = parts[name]()
        out.write_text(json.dumps(found, indent=1, default=str), encoding="utf-8")
        (HERE / f"ride_local_{FLAG}_{TAG}.log").write_text("\n".join(LOG) + "\n", encoding="utf-8")
    say("done")
