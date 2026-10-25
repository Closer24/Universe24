"""Hand dn1: David's lean toy (tools/derivations/open_items/H-Den-Beyond-128-Bits-1/toy, never edited) run from this hand's world and universe files, with the readings this brief asks beside the toy's own: the time per interval in integer milliseconds, the bit length of every class of integer in the state and the acts (the walls, the levels, the rotation remainders, the write remainders, the Rule3 transient, the phase, the Links' count, the credits' and births' numbers, the clock's memo), the packets' share within one Link of their lay (per mille), the run back exact bit for bit. Integers only; no float.

Run: PYTHONPATH=<worktree>/src TMPDIR=/dev/shm/tmp /home/user/Universe24/venv314/bin/python tools/derivations/open_items/H-Den-Beyond-128-Bits-1/run_toy.py <world.json> <out.json> [back N]
"""

from __future__ import annotations

import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "toy"))
sys.set_int_max_str_digits(0)

from lean_full import Lean, load_world, reading, wronskian  # the toy's own program, imported and never edited

from event_universe.core import paces


def bits_of(array) -> int:
    """The largest bit length over an array of integers."""
    flat = [abs(int(x)) for x in np.asarray(array, dtype=object).reshape(-1)]
    return max((x.bit_length() for x in flat), default=0)


def census(b: Lean) -> dict:
    """Every class of integer of the Node, its largest bit length over the board: by row shape (the volume row 10, the sign's potential row 4, the planes with a gap, the plane at the gap 0, the row with its own wall), the levels (now, before) apart from the rotation remainders and the write remainders; the walls per class; the Links' count; the paces' memo at the deepest content on the board (K-S4)."""
    out = {"walls": {}, "levels": {}, "rotation_remainders": {}, "write_remainders": {}, "write_walls": {}}
    for r in b.rows_:
        if r.wall is not None:
            name = "phase_row_wall_%d" % r.wall
        elif r.shape == 2:
            name = "plane_gap0_light" if r.gap == 0 else "plane_lift_gap_bits_%d" % r.gap.bit_length()
        else:
            name = "shape_%d" % r.shape
        out["walls"][name] = max(l.wall.bit_length() for l in r.lines)
        out["levels"][name] = max(max(bits_of(l.now), bits_of(l.before)) for l in r.lines)
        out["rotation_remainders"][name] = max(bits_of(l.rem) for l in r.lines)
        wr = [l for l in r.lines if l.wr is not None]
        if wr:
            out["write_remainders"][name] = max(bits_of(l.wr) for l in wr)
            out["write_walls"][name] = max(l.wwall.bit_length() for l in wr)
    out["counters"] = max([bits_of(a) for a in b.standing + b.crossed + b.beats] + [bits_of(b.proper), bits_of(b.closes)])
    out["phase_amplitude_X"] = int(b.X).bit_length()
    out["orbit_table_pairs"] = max(max(abs(c), abs(s)).bit_length() for c, s in b.orbit)
    out["links_count_max"] = int(b.count_max).bit_length() if hasattr(b, "count_max") else None
    out["rule3_transient_max"] = int(b.max_transient)
    c = b.content()
    cs = [int(x) for x in c.reshape(-1)]
    deepest = max(cs)
    side = paces.side_of(b.gamma, deepest)
    out["content_min_max"] = [min(cs), deepest]
    out["clock_memo_at_deepest_content"] = {"content": deepest, "clock_p0": paces.clock(b.gamma, deepest), "link_pace": paces.link_pace(b.gamma, deepest), "memo_filled_through_content": len(side.clocks) - 1, "running_fraction_numerator_bits": side.numerator.bit_length(), "running_fraction_wall_bits": side.wall.bit_length()}
    state_count, state_bits = b.census()
    out["state_arrays"] = state_count
    out["state_max_bits"] = state_bits
    return out


def log_bits(log: list) -> dict:
    """The largest bit length among the credits' frame integers and the births' numbers in the log."""
    credit = 0
    birth = 0
    for e in log:
        if e["event"] == "credit":
            f = e["frame"]
            vals = []
            for v in f.values():
                if isinstance(v, list):
                    for x in v:
                        vals += x if isinstance(x, list) else [x]
                else:
                    vals.append(v)
            credit = max([credit] + [abs(int(x)).bit_length() for x in vals] + [abs(int(e[k])).bit_length() for k in ("taken", "levels", "light_now_was", "sign_level")])
        elif e["event"] == "birth":
            birth = max([birth] + [abs(int(e[k])).bit_length() for k in ("taken", "booked", "levels", "light_now_was", "amplitude", "room")])
    return {"credit_frame_max_bits": credit, "birth_numbers_max_bits": birth}


def packet_shares(b: Lean, centres: list) -> dict:
    """For every plane with a gap that holds levels: the weight re^2 + im^2 summed over the board, the share within one Link (L1 distance at most 1 on the torus) of each lay centre, per mille; the weighted centroid in thousandths of a Link (the toy's reader's form)."""
    out = {}
    for rec, r in enumerate(b.records()):
        if r.gap == 0:
            continue
        re, im = r.lines
        wgt = re.now * re.now + im.now * im.now
        total = int(sum(int(x) for x in wgt.reshape(-1)))
        if total == 0:
            continue
        shares = []
        for at in centres:
            within = 0
            for node in np.ndindex(*b.shape):
                d = sum(min(abs(node[a] - at[a]), b.cube - abs(node[a] - at[a])) for a in range(3))
                if d <= 1:
                    within += int(wgt[node])
            shares.append((within * 1000) // total)
        nodes = int(sum(1 for x in wgt.reshape(-1) if int(x) > 0))
        out["plane_%d" % rec] = {"weight_bits": total.bit_length(), "nodes_with_levels": nodes, "share_within_one_link_of_each_centre_per_mille": shares}
    return out


def main() -> None:
    world_path, out_path = sys.argv[1], sys.argv[2]
    back = int(sys.argv[sys.argv.index("back") + 1]) if "back" in sys.argv else 0
    universe, world = load_world(world_path)
    paces.clear_memo()
    t_load = time.monotonic_ns()
    b = Lean(universe, world)
    load_ms = (time.monotonic_ns() - t_load) // 10**6
    intervals = int(world["intervals"])
    centres = [tuple(int(x) for x in lay["centre"]) for lay in world.get("seed", []) if lay.get("lay") == "at" and tuple(int(x) for x in lay["row"]) != (b.den, b.den)]
    marks = sorted({1, 2, 5, 10, 20, 30, 40, 60, 80, 100, 120, intervals} & set(range(1, intervals + 1)))
    per_interval_ms = []
    rows = []
    hashes = []
    maxbits = 0
    for t in range(intervals):
        if back and t >= intervals - back:
            hashes.append(b.state_hash())
        t0 = time.monotonic_ns()
        b.step()
        per_interval_ms.append((time.monotonic_ns() - t0) // 10**6)
        maxbits = max(maxbits, b.census()[1])
        if b.interval in marks:
            row = dict(reading(b, maxbits), census=census(b), log_bits=log_bits(b.log), interval_ms=per_interval_ms[-1], total_ms=sum(per_interval_ms))
            if centres:
                row["packets_within_one_link"] = packet_shares(b, centres)
            rows.append(row)
            print(json.dumps({k: v for k, v in row.items() if k in ("i", "births", "body_clicks", "turns", "refused", "max bits", "max transient bits", "interval_ms", "total_ms", "content min/mean/max", "packets_within_one_link")}), flush=True)
    kept_log = list(b.log)
    run_back = None
    if back:
        t0 = time.monotonic_ns()
        exact = 0
        first_bad = None
        for k in range(back):
            b.step_back()
            if b.state_hash() == hashes[back - 1 - k]:
                exact += 1
            elif first_bad is None:
                first_bad = back - 1 - k
        run_back = {"intervals": back, "exact": exact, "first_mismatch_at_interval": first_bad, "ms": (time.monotonic_ns() - t0) // 10**6}
        print(json.dumps({"run back": run_back}), flush=True)
    ms = sorted(per_interval_ms)
    timing = {"load_ms": load_ms, "intervals": intervals, "total_ms": sum(per_interval_ms), "per_interval_ms_min_median_max": [ms[0], ms[len(ms) // 2], ms[-1]], "per_interval_ms_mean": sum(per_interval_ms) // len(per_interval_ms), "nodes": b.cube**3, "ms_per_node_interval_milli": (sum(per_interval_ms) * 1000) // (len(per_interval_ms) * b.cube**3)}
    senses = sum(s for e in kept_log if e["event"] == "birth" for s in e["senses"])
    found = {"world": world, "universe_integers": universe["integers"], "den_bits": b.den.bit_length(), "timing": timing, "counts": {k: str(v) for k, v in b.counts.items()}, "senses_sum_over_births": senses, "rows": rows, "run_back": run_back, "final_census": census(b), "log_bits": log_bits(kept_log), "log": kept_log, "lifts": [(None, str(r.pair[0]), None) for r in b.lifts], "planes": [str(r.pair[0]) for r in b.records()], "den": str(b.den), "cube": b.cube, "intervals": intervals, "T": b.T, "gamma": b.gamma, "G": b.G, "turns": b.turns}
    text = json.dumps(found, default=str)
    if len(text) > 1400000:  # the file's cap: the log kept to its counts and its first lines; the whole record written outside the worktree, under TMPDIR, for the clicks' reader
        whole = os.path.join(os.environ.get("TMPDIR", "/dev/shm/tmp"), "dn1_" + os.path.basename(out_path))
        open(whole, "w").write(text)
        found["log_dropped"] = {"lines": len(kept_log), "kept": 200, "whole_record_at": whole}
        found["log"] = kept_log[:200]
        text = json.dumps(found, default=str)
    open(out_path, "w").write(text)
    print(json.dumps({"timing": timing, "counts": found["counts"], "senses_sum_over_births": senses, "final_census": found["final_census"], "log_bits": found["log_bits"]}, default=str), flush=True)


if __name__ == "__main__":
    main()
