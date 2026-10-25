"""Hand D3: the decoder receives the clicks as they are. The board's course with the output writer on and off, bit for bit, and the laws checked on the same run, each with an integer reading (BRIEF_d (a), (b); BRIEF_COMMON, Addition 4).

The run: the law's hole seed on the bare 3-cube of the tests' small universe (den 1,021, Gamma 1,000, T 36,000), INTERVALS intervals, twice: once with no output callable (the writer off) and once with every output line kept (the writer on). Every integer of both boards is compared at every interval: the lines (now, before, remainder), the write remainders, the phase lines, the time count `proper_count`, the closes `closes`, and the bodies' standing, crossed and beats arrays. Then on the board with the writer on: the run back to the seed (MATCH per interval), the conserved form (the linear sum of light's line, constant until the first lay), the one-Link reach (a third pair of boards, one level raised at a Node no neighbour of the hole), the cube's 48 on the credit lines themselves (the multiset of credits invariant under each signed permutation about the origin), the fixed count of integers per Node and the largest bit length of the state, the exact take on every credit and birth line, and only a bound body clicks (every light credit at a birth's Node and interval; every other credit a charged plane record's). Integers only: every reading a count, a quotient with its remainder or a bit length.

Usage: PYTHONPATH=<worktree>/src TMPDIR=/dev/shm/tmp python tools/derivations/open_items/H-Decoder-Receives-Clicks-3/d3_course.py [--intervals 40] [--out tools/derivations/open_items/H-Decoder-Receives-Clicks-3/out]
"""

from __future__ import annotations

import argparse
import itertools
import json
import os
import sys
import tempfile
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]  # the worktree's root, so that `tests` imports as the suite does
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from event_universe import bound_body, digits, seed, share, world_files  # noqa: E402
from event_universe.core.rule3 import wall_of  # noqa: E402
from event_universe.lattice import Lattice  # noqa: E402
from event_universe.world_files import load_world  # noqa: E402
from tests.laws import board_state, linear_sum, same_state  # noqa: E402
from tests.laws_universe import GAMMA, bare_torus, node_arrays  # noqa: E402

CORNER = (1, 1, 0)  # the Node raised by one level for the one-Link reach, no neighbour of the hole


def hole_board(folder: Path, output):  # type: ignore[no-untyped-def]
    folder.mkdir(parents=True, exist_ok=True)
    world_files.REPOSITORY_ROOT = folder
    return Lattice(load_world(bare_torus(folder, 3, 60)), output=output)


def full_state(board: Lattice) -> dict:
    """Every integer the board holds, as Python's integers: the arrays of every family (lines, write remainders, phase lines), the time count, the closes and the bodies' three arrays."""
    found = {("arrays", *k): tuple(np.asarray(a, dtype=object) for a in v) for k, v in node_arrays(board).items()}
    found[("proper",)] = (np.asarray(board.proper_count, dtype=object),)
    found[("closes",)] = (np.asarray(board.closes, dtype=object),)
    for name, kept in (("standing", board.standing), ("crossed", board.crossed), ("beats", board.beats)):
        for key, array in kept.items():
            found[(name, *key)] = (np.asarray(array, dtype=object),)
    return found


def same_full(a: dict, b: dict) -> tuple[bool, list]:
    if set(a) != set(b):
        return False, sorted(set(a) ^ set(b))
    apart = [k for k in a if not all(np.array_equal(x, y) for x, y in zip(a[k], b[k], strict=True))]
    return not apart, apart


def integers_of(state: dict) -> tuple[int, int]:
    """The count of integers one Node holds (every array of the board's shape counts one per Node) and the largest bit length over the state."""
    count, bits = 0, 0
    for value in state.values():
        for array in value:
            count += 1
            for x in np.asarray(array, dtype=object).reshape(-1):
                bits = max(bits, abs(int(x)).bit_length())
    return count, bits


def elements():
    """The cube's 48: a permutation of the axes and a sign per axis."""
    for permutation in itertools.permutations(range(3)):
        for signs in itertools.product((1, -1), repeat=3):
            yield permutation, signs


def carried_node(node, permutation, signs, shape):
    """A Node under one of the 48 about the origin on the torus: j_k = s_k i[perm k] mod n_k."""
    return tuple(int((signs[k] * node[permutation[k]]) % shape[k]) for k in range(3))


def carried_momentum(momentum, permutation, signs):
    if momentum is None:
        return None
    found = []
    for k in range(3):
        entry = momentum[permutation[k]]
        if entry is None:
            found.append(None)
        else:
            sign, num, den = entry
            found.append([sign * signs[k], num, den])
    return found


def credit_key(line, permutation, signs, shape):
    support = carried_node(tuple(line["support"]), permutation, signs, shape)
    point = json.dumps(line["point"])
    momentum = json.dumps(carried_momentum(line["momentum"], permutation, signs))
    return (line["interval"], support, tuple(line["identity"]), point, line["kind"], line["sense"], line["beat"], line["proper"], line["windows"], momentum)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--intervals", type=int, default=40)
    parser.add_argument("--out", type=Path, default=HERE.parent / "out")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix="d3_", dir=os.environ.get("TMPDIR", "/dev/shm/tmp")))
    n = args.intervals

    lines: list[dict] = []
    off = hole_board(tmp / "off", None)
    on = hole_board(tmp / "on", lines.append)
    light = on.world.seed
    assert light is not None
    wall = wall_of(on.families[light].pair[1], GAMMA, on.unit)
    equal_intervals, first_apart, kept, sums, counts, bits = 0, None, [full_state(on)], [], [], []
    count0, bits0 = integers_of(kept[0])
    sums.append(linear_sum(wall, on.states[light].lines[0]))
    for _ in range(n):
        off.step()
        on.step()
        same, apart = same_full(full_state(off), full_state(on))
        if same:
            equal_intervals += 1
        elif first_apart is None:
            first_apart = (on.interval, [str(k) for k in apart[:5]])
        kept.append(full_state(on))
        sums.append(linear_sum(wall, on.states[light].lines[0]))
        c, b = integers_of(kept[-1])
        counts.append(c)
        bits.append(b)
    credits = [x for x in lines if x["event"] == "credit"]
    births = [x for x in lines if x["event"] == "birth"]
    lays = [x for x in lines if x["event"] == "lay"]
    refused = [x for x in lines if x["event"] == "refused"]
    first_lay = min((x["interval"] for x in lays), default=None)
    first_birth = min((x["interval"] for x in births), default=None)
    constant_until = 0
    while constant_until + 1 < len(sums) and sums[constant_until + 1] == sums[0]:
        constant_until += 1
    # the run back, the writer on: every interval back compared to the kept state bit for bit
    match, counters_kept = 0, 0
    for k in range(n):
        on.step_inverse()
        now_state, was = full_state(on), kept[n - 1 - k]
        arrays = {key for key in was if key[0] == "arrays"}  # the state: the lines, the write remainders, the phase lines
        same = all(np.array_equal(x, y) for key in arrays for x, y in zip(now_state[key], was[key], strict=True))
        match += same
        others = {key for key in was if key[0] != "arrays"}  # the readings kept beside the state (the time count, the closes, the bodies' arrays): the run back reads none of them, the law's letter
        counters_kept += all(np.array_equal(x, y) for key in others for x, y in zip(now_state[key], now_state[key], strict=True)) and not all(np.array_equal(x, y) for key in others if key in now_state for x, y in zip(now_state[key], was[key], strict=True))
    # the one-Link reach on a third pair
    a = hole_board(tmp / "a", None)
    b = hole_board(tmp / "b", None)
    line0, now = b.states[light].lines[0], np.asarray(b.states[light].lines[0].now, dtype=object).copy()
    now[CORNER] += 1
    b.states[light].lines[0] = line0.__class__(now, line0.before, line0.remainder)
    frame = {tuple(int(i) for i in node) for node in digits.frame_of(CORNER, b.shape, b.world.periodic)}
    a.step()
    b.step()

    def apart_nodes(x, y):
        found = set()
        for (la, wa), (lb, wb) in zip(x, y, strict=True):
            pairs = [(u, v) for p, q in zip(la, lb, strict=True) for u, v in zip(p, q, strict=True)]
            for u, v in pairs + list(zip(wa, wb, strict=True)):
                found |= {tuple(int(i) for i in d) for d in np.argwhere(np.asarray(u != v, dtype=bool))}
        return found

    reach_forward = apart_nodes(board_state(a), board_state(b))
    a.step_inverse()
    b.step_inverse()
    reach_back = apart_nodes(board_state(a), board_state(b))
    # the cube's 48 on the credit lines: the multiset of credits invariant under each element about the origin
    shape = tuple(on.shape)
    plain = sorted(credit_key(x, (0, 1, 2), (1, 1, 1), shape) for x in credits)
    invariant = sum(1 for p, s in elements() if sorted(credit_key(x, p, s, shape) for x in credits) == plain)
    # the exact take on every credit and birth line
    takes = [x for x in credits + births if x.get("taken") is not None]
    identity = sum(1 for x in takes if x["taken"] == x["walls"] + x["excess"])
    exact = sum(1 for x in takes if x["excess"] == 0)
    # only a bound body clicks
    born_at = {(x["interval"], tuple(node)) for x in births for node in x["nodes"]}
    light_credits = [x for x in credits if x["identity"][0] == light]
    body_credits = [x for x in credits if x["identity"][0] != light]
    light_at_births = sum(1 for x in light_credits if (x["interval"], tuple(x["support"])) in born_at)
    bodies_charged_plane = sum(
        1 for x in body_credits if share.charged(on.families[x["identity"][0]]) and on.families[x["identity"][0]].plane and x["kind"] == on.families[x["identity"][0]].width
    )
    massless_is_body = light in {k for k, _r in bound_body.body_records(on)}
    body_point_pair_of_pairs = sum(1 for x in body_credits if isinstance(x["point"], list) and x["point"] and isinstance(x["point"][0], list))
    body_beat_none = sum(1 for x in body_credits if x["beat"] is None)
    body_beat_zero = sum(1 for x in body_credits if x["beat"] == 0)
    light_beat = sum(1 for x in light_credits if x["beat"])
    names = sorted({str(x.get(k)) for x in credits for k in ("family", "before", "realised", "absorbed", "emitted") if x.get(k) is not None})
    window_is_interval = sum(1 for x in credits if x["window"] == [x["interval"], x["interval"]])
    detector_is_support = sum(1 for x in credits if x["node_detector"] == int(np.ravel_multi_index(tuple(x["support"]), shape)))
    found = {
        "universe": {"den": 1021, "node_clock": GAMMA, "quantum_action": 36000, "shape": list(shape), "intervals": n, "seed": "the law's hole seed (light at one quantum on every Node but the origin)"},
        "a_output_on_off": {"intervals_equal_bit_for_bit": equal_intervals, "of": n, "first_apart": first_apart, "lines_written_on": len(lines), "lines_written_off": 0, "credits": len(credits), "births": len(births), "lays": len(lays), "refused": len(refused)},
        "run_back_match_intervals": [match, n],
        "run_back_counters_beside_the_state_not_run_back": [counters_kept, n],
        "conserved_form": {"linear_sum_of_light_at_start": sums[0], "constant_through_interval": constant_until, "first_lay_interval": first_lay, "first_birth_interval": first_birth, "sums_first_six": sums[:6]},
        "one_link_reach": {"nodes_apart_after_one_interval": len(reach_forward), "frame_size": len(frame), "apart_is_frame": reach_forward == frame, "nodes_apart_after_step_back": sorted(reach_back)},
        "cube_48_on_credit_lines": {"elements_invariant": invariant, "of": 48, "credits": len(credits)},
        "fixed_count_and_bits": {"integers_per_node_at_start": count0, "integers_per_node_per_interval": sorted(set(counts)), "integers_per_node_at_end": counts[-1], "largest_bit_length_at_start": bits0, "largest_bit_length_over_run": max(bits)},
        "exact_take": {"lines_with_a_take": len(takes), "taken_equals_walls_plus_excess": identity, "excess_zero": exact},
        "b_only_a_bound_body_clicks": {"credits": len(credits), "light_credits": len(light_credits), "light_credits_at_a_birth": light_at_births, "light_credits_not_at_a_birth": len(light_credits) - light_at_births, "body_credits": len(body_credits), "body_credits_charged_plane_kind_is_width": bodies_charged_plane, "massless_record_is_a_body": massless_is_body, "body_credit_point_pair_of_pairs": body_point_pair_of_pairs, "body_credit_beat_none": body_beat_none, "body_credit_beat_zero": body_beat_zero, "light_credits_with_a_beat": light_beat},
        "c_board_keys_on_the_credit": {"window_equals_interval_twice": [window_is_interval, len(credits)], "node_detector_equals_ravelled_support": [detector_is_support, len(credits)], "names_carried": names},
    }
    (args.out / "course.json").write_text(json.dumps(found, indent=1, default=str) + "\n", encoding="utf-8")
    with (args.out / "clicks.jsonl").open("w", encoding="utf-8") as handle:
        for line in lines:
            handle.write(json.dumps(line, default=str) + "\n")
    print(json.dumps(found, indent=1, default=str))


if __name__ == "__main__":
    main()
