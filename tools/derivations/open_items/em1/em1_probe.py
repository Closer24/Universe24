"""em1's probe of W-S1 on the engine (2026-10-25): a READ-ONLY instrumentation of interval.Interval and close.credit.
With EM1_PROBE=1 the probe wraps two functions and reads; it writes no integer of the state, so the record is David's bit for bit
(the state hash printed with the probe on and off is the control). Readings, every one an integer:
  (a) the identity: the engine's emission numerator over the mean wall, q = emission div w_div, against the Wronskian's change over the
      step, dW = w_after - w_end, at every Node: the bound |q + dW| <= SUM over the gapped planes of (|re_now| + |im_now|) (the roundings
      of two lines, each at most one level, times the other line's level);
  (b) the board's sum of q per interval (the current's divergence sums to 0 at uniform paces) and the largest |q| of the run against T;
  (c) at the end the gap-0 line's write remainder wr against its start T div 2 (the carry of every q since the seed) and the largest |W|;
  (d) per credit and birth: the excess taken - booked in thousandths of booked and of the light quantum 3 T den; the surplus at the
      credit's Node, owns - 6 s |W| (the record's energy above the rest energy of its charge), in thousandths of the record's unit.
Usage: EM1_PROBE=1 python em1_probe.py <world.json> <out.json> [intervals N] [back N]"""
from __future__ import annotations

import json
import os
import sys
import time

import numpy as np

sys.set_int_max_str_digits(0)
from event_universe import close, interval, readings, run  # noqa: E402
from event_universe.core.paces import sine_den  # noqa: E402
from event_universe.core.rule3 import quotient  # noqa: E402
from event_universe.links import cross  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.rows import PLANE  # noqa: E402

PROBE = {
    "identity_max_mismatch": 0,
    "identity_bound_at_max": 0,
    "identity_nodes": 0,
    "identity_within_bound": 0,
    "identity_ride_within_bound": 0,
    "identity_ride_max_mismatch": 0,
    "board_sum_q_max_abs": 0,
    "q_max_abs": 0,
    "q_abs_total": 0,
    "q_nonzero_nodes": 0,
    "w_total_max_abs": 0,
    "credits": [],
    "births": [],
}

_divisions = interval.Interval.divisions
_laid_on = interval.laid_on
LAID = {"per_interval_sum": [], "per_interval_plus": [], "per_interval_minus": [], "centre_series": [], "far_series": [], "by_distance": {}}


def laid_on(node, line, levels):
    _laid_on(node, line, levels)
    laid = line.now - levels
    flat = [int(x) for x in laid.reshape(-1)]
    LAID["per_interval_sum"].append(sum(flat))
    LAID["per_interval_plus"].append(sum(1 for x in flat if x > 0))
    LAID["per_interval_minus"].append(sum(1 for x in flat if x < 0))
    c = node.cube // 2
    centre = (c, c, c)
    LAID["centre_series"].append(int(laid[centre]))
    LAID["far_series"].append(int(laid[(0, 0, 0)]))
    for idx in np.ndindex(*node.shape):
        v = int(laid[idx])
        if v != 0:
            d = sum(min(abs(idx[a] - c), node.cube - abs(idx[a] - c)) for a in range(3))
            LAID["by_distance"][d] = LAID["by_distance"].get(d, 0) + abs(v)
_credit = close.credit


def divisions(self):
    _divisions(self)
    if self.direction != 1:
        return
    q = quotient(self.emission, self.w_div)
    dw = self.w_after - self.w_end
    bound = np.zeros(self.node.shape, dtype=object)
    for r in self.gap_planes:
        re_s, im_s = self.starts[self.where[id(r)]]
        bound = bound + abs(re_s) + abs(im_s)
    mism = abs(q + dw)
    w_in = self.mean_wall()
    ride = quotient(self.w_end * (w_in - self.w_div), self.w_div)
    mism2 = abs(q + dw - ride)
    PROBE["identity_ride_within_bound"] += int(sum(1 for a, b in zip(mism2.reshape(-1), bound.reshape(-1)) if int(a) <= int(b)))
    PROBE["identity_ride_max_mismatch"] = max(PROBE["identity_ride_max_mismatch"], max(int(x) for x in mism2.reshape(-1)))
    flat_m, flat_b = mism.reshape(-1), bound.reshape(-1)
    k = int(np.argmax(np.vectorize(int, otypes=[object])(flat_m)))
    if int(flat_m[k]) > PROBE["identity_max_mismatch"]:
        PROBE["identity_max_mismatch"] = int(flat_m[k])
        PROBE["identity_bound_at_max"] = int(flat_b[k])
    PROBE["identity_nodes"] += int(flat_m.size)
    PROBE["identity_within_bound"] += int(sum(1 for a, b in zip(flat_m, flat_b) if int(a) <= int(b)))
    qs = [int(x) for x in q.reshape(-1)]
    PROBE["board_sum_q_max_abs"] = max(PROBE["board_sum_q_max_abs"], abs(sum(qs)))
    PROBE["q_max_abs"] = max(PROBE["q_max_abs"], max(abs(x) for x in qs))
    PROBE["q_abs_total"] += sum(abs(x) for x in qs)
    PROBE["q_nonzero_nodes"] += sum(1 for x in qs if x != 0)
    PROBE["w_total_max_abs"] = max(PROBE["w_total_max_abs"], max(abs(int(x)) for x in self.w_end.reshape(-1)))


def credit(node, rec, at, plane_starts, fall, levels, taken_was, taken_before):
    found = _credit(node, rec, at, plane_starts, fall, levels, taken_was, taken_before)
    c = node.start_content
    frozen = readings.frozen_of(node, c)
    factors = node.link_factors(None, frozen)
    pace = readings.paces_of(node, c)[1]
    row = node.records()[rec]
    rr = node.rule_of(row, c, factors)
    re0, im0 = plane_starts[rec]
    owns = int((node.share(re0, rr, pace, vacuum=True) + node.share(im0, rr, pace, vacuum=True))[at])
    w = int(cross(re0.now[at], im0.now[at], re0.before[at], im0.before[at]))
    s = sine_den(row.pair[0], node.den) if row.gap else node.den
    unit = node.units[rec]
    walls = unit
    PROBE["credits"].append(
        {
            "i": node.interval,
            "node": list(at),
            "line": rec,
            "booked": walls,
            "taken": fall,
            "excess": fall - walls,
            "excess_per_1000_booked": quotient(1000 * (fall - walls), walls),
            "excess_per_1000_light_quantum": quotient(1000 * (fall - walls), node.unit_gap0),
            "owns": owns,
            "W": w,
            "rest_6sW": 6 * s * abs(w),
            "surplus": owns - 6 * s * abs(w),
            "surplus_per_1000_unit": quotient(1000 * (owns - 6 * s * abs(w)), unit),
            "owns_per_1000_unit": quotient(1000 * owns, unit),
            "sense": found["sense"],
            "beat": found["beat"],
        }
    )
    return found


def main(argv):
    universe, world = load_world(argv[1])
    if "intervals" in argv:
        world = dict(world, intervals=int(argv[argv.index("intervals") + 1]))
    back = int(argv[argv.index("back") + 1]) if "back" in argv else 0
    probe = os.environ.get("EM1_PROBE") == "1"
    if probe:
        interval.Interval.divisions = divisions
        interval.laid_on = laid_on
        close.credit = credit
    t0 = time.monotonic_ns()
    node = Node(universe, world)
    intervals = int(world["intervals"])
    rows, nodes, hashes = run.forward(node, intervals, back, lambda line: None)
    final_hash = node.state_hash()
    census = node.census()
    gap0 = node.row(PLANE, gap=0).lines[0]
    wr = [int(x) for x in gap0.wr.reshape(-1)]
    half_t = node.T // 2
    out = {
        "world": argv[1],
        "probe": probe,
        "intervals": intervals,
        "final_hash": final_hash,
        "counts": dict(node.counts),
        "census_arrays": census[0],
        "census_bits": census[1],
        "max_transient_bits": node.max_transient,
        "T": node.T,
        "unit_gap0": node.unit_gap0,
        "units": node.units,
        "wr_minus_half_T_max_abs": max(abs(x - half_t) for x in wr),
        "wr_off_half_T_nodes": sum(1 for x in wr if x != half_t),
        "seconds": (time.monotonic_ns() - t0) // 10**9,
    }
    for entry in node.log:
        if entry["event"] == "birth":
            PROBE["births"].append(
                {
                    "i": entry["i"],
                    "booked": entry["booked"],
                    "taken": entry["taken"],
                    "excess_per_1000_booked": quotient(1000 * (entry["taken"] - entry["booked"]), entry["booked"]),
                    "excess_per_1000_light_quantum": quotient(1000 * (entry["taken"] - entry["booked"]), node.unit_gap0),
                    "W_children": entry["W_children"],
                }
            )
    if back:
        out["run_back"] = run.run_back(node, hashes)
    if probe:
        out["probe_readings"] = {k: v for k, v in PROBE.items() if k not in ("credits", "births")}
        cr = PROBE["credits"]
        out["credits_n"] = len(cr)
        if cr:
            out["credits_excess_per_1000_booked_min_max"] = [min(c["excess_per_1000_booked"] for c in cr), max(c["excess_per_1000_booked"] for c in cr)]
            out["credits_excess_light_quanta_per_1000_total"] = sum(c["excess_per_1000_light_quantum"] for c in cr)
            out["credits_excess_positive"] = sum(1 for c in cr if c["excess"] > 0)
            out["credits_surplus_per_1000_unit_min_max"] = [min(c["surplus_per_1000_unit"] for c in cr), max(c["surplus_per_1000_unit"] for c in cr)]
            out["credits_owns_per_1000_unit_min_max"] = [min(c["owns_per_1000_unit"] for c in cr), max(c["owns_per_1000_unit"] for c in cr)]
            out["credits_W_zero"] = sum(1 for c in cr if c["W"] == 0)
            out["credits_W_max_abs"] = max(abs(c["W"]) for c in cr)
            out["credits_senses_sum"] = sum(c["sense"] for c in cr)
        bi = PROBE["births"]
        out["births_n"] = len(bi)
        if bi:
            out["births_excess_per_1000_booked_min_max"] = [min(b["excess_per_1000_booked"] for b in bi), max(b["excess_per_1000_booked"] for b in bi)]
            out["births_excess_light_quanta_per_1000_total"] = sum(b["excess_per_1000_light_quantum"] for b in bi)
            out["births_charge_sum"] = sum(sum(b["W_children"]) for b in bi)
            out["births_charge_zero"] = sum(1 for b in bi if sum(b["W_children"]) == 0)
        out["credits"] = cr[:400]
        out["laid_board_sum_total"] = sum(LAID["per_interval_sum"])
        out["laid_board_sum_max_abs"] = max([abs(x) for x in LAID["per_interval_sum"]] or [0])
        out["laid_intervals_with_lay"] = sum(1 for a, b in zip(LAID["per_interval_plus"], LAID["per_interval_minus"]) if a + b > 0)
        out["laid_plus_nodes_total"] = sum(LAID["per_interval_plus"])
        out["laid_minus_nodes_total"] = sum(LAID["per_interval_minus"])
        out["laid_first_interval"] = next((k + 1 for k, (a, b) in enumerate(zip(LAID["per_interval_plus"], LAID["per_interval_minus"])) if a + b > 0), 0)
        out["laid_by_distance"] = LAID["by_distance"]
        out["laid_centre_series_nonzero"] = [(k + 1, v) for k, v in enumerate(LAID["centre_series"]) if v != 0][:60]
        out["laid_board_sum_series"] = LAID["per_interval_sum"][:120]
        out["births"] = bi
    print(json.dumps({k: v for k, v in out.items() if k not in ("credits", "births")}, default=str))
    with open(argv[2], "w", encoding="utf-8") as f:
        json.dump(out, f, default=str)


if __name__ == "__main__":
    main(sys.argv)
