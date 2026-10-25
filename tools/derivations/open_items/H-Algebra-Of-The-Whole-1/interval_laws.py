"""ag1, items (3) to (5) and (7) on the engine's interval: the laws read inside every interval of a record, integers only.
Usage: interval_laws.py <world.json> <intervals> [back N]
The interval is driven act by act as interval.run drives it (the same calls in the same order; nothing of src changed), so the
state between the acts can be read:
 A. the riding line's momentum form (the kick and the division at the mean wall): for every riding line at every Node,
    W_out (a_next - a_now) - W_in (a_now - a_before) + r' - r - (W_out - W_in) div 2 == X_now F, F the force of the start
    (SUM_j R_j (m_j - a) - D a plus the Node term by shape) scaled by the row's scale; counted exact of all Node-lines.
 B. LC-S1: SUM over the Links of 2 num Q_ij G^2 (X_j - X_i) == 0 at every interval (the pace-weighted Links' sum); the plain sum
    SUM_i SUM_j R_ij (X_j - X_i) (the lift) per interval: its first, least and largest value.
 C. the charge: the records' Wronskian summed over the board at the start, after the acts, after the swap and after the close;
    at every turned Node W after the exchange equals W before (W even under C T_0); every birth's W_children sum 0.
 D. the transients' bits: the rotate's (node.max_transient), the carrier's held numerator, the kick's products u_in (G u_out),
    the share's numerator (o + o - s) X at the close, the emission; the state's census (count, bits).
 E. the swap is an involution: at the first turn, the exchange applied twice returns the rows bit for bit.
 F. the close: on every birth and credit line taken >= booked (the stop refused where not), the count with taken == booked, the
    sum of taken - booked (the excess no line credits); laid-back credits: the taken line's level restored; the gap-0 record
    credited never; the births' taken_row and children's record.
 G. the run back over the last N intervals: the state hash equal at each.
"""

from __future__ import annotations

import json
import sys
import time

import numpy as np
from typing import Any

sys.set_int_max_str_digits(0)

from event_universe import gram  # noqa: E402
from event_universe.core.ports import PORTS, across  # noqa: E402
from event_universe.core.rule3 import half  # noqa: E402
from event_universe.interval import Interval  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402


def bits_of(a: Any) -> int:
    """The largest bit length of an integer array's values (the hand's own reader; the loop's stays the loop's)."""
    return int(np.max(np.vectorize(lambda v: abs(int(v)).bit_length(), otypes=[object])(a)))
from event_universe.rows import CARRIER, PLANE  # noqa: E402


def total(a) -> int:
    return int(np.sum(np.asarray(a, dtype=object)))


def charge_total(node: Node) -> tuple[int, ...]:
    """The Wronskian summed over the board, one integer per record."""
    return tuple(total(gram.charge(r.shape, r.lines)) for r in node.records())


def main(argv: list[str]) -> None:
    t0 = time.monotonic_ns()
    universe, world = load_world(argv[1])
    n = int(argv[2])
    back = int(argv[argv.index("back") + 1]) if "back" in argv else 0
    node = Node(universe, world)
    rec0 = node.records().index(node.row(PLANE, gap=0))
    a_total = a_exact = 0
    b_zero = b_total = 0
    lifts: list[int] = []
    w_course: list[tuple[int, int, int, int, int]] = []
    turned_even = turned_total = 0
    bits = {"rotate": 0, "held numerator": 0, "kick products": 0, "share numerator": 0, "emission": 0, "state": 0}
    involution = None
    frozen_total = 0
    hashes = []
    for _ in range(n):
        if back and node.interval >= n - back:
            hashes.append(node.state_hash())
        w_start = charge_total(node)
        iv = Interval(node, 1)
        frozen_total += int(iv.frozen.sum())
        iv.walled_act()
        iv.forces()
        iv.kicks()
        # D: the kick's products and the held numerator
        for k in iv.kicked:
            pass
        iv.carrier_act()
        p02 = iv.p0 * iv.p0
        from event_universe.core.rule3 import held_numerator
        from event_universe.rows import TRACE

        held_num = held_numerator(TRACE, iv.x_now, iv.forms, iv.trace, iv.p0, node.den, node.gamma)
        bits["held numerator"] = max(bits["held numerator"], bits_of(held_num), bits_of(iv.traceless[0] * p02))
        bits["emission"] = max(bits["emission"], bits_of(iv.emission))
        iv.divisions()
        # A: the momentum form on every riding line
        w_in = iv.w_half * (iv.held[iv.where[id(iv.carrier)]][0].before + iv.held[iv.where[id(iv.carrier)]][0].now)
        w_out = iv.w_div
        for r in iv.riders:
            k = iv.where[id(r)]
            s = iv.scales[k]
            for a0, line_held, line_new, f in zip(iv.starts[k], iv.held[k], iv.out[k], iv.force[k], strict=True):
                left = (
                    s * w_out * (line_new.now - a0)
                    - s * w_in * (a0 - line_held.before)
                    + line_new.rem
                    - line_held.rem
                    - half(s * w_out)
                    + half(s * w_in)
                )
                right = iv.x_now * f
                a_total += left.size
                a_exact += int(np.sum(left == right))
                # the kick's products' bits
                pin = s * w_in * (a0 - line_held.before) + line_held.rem - half(s * w_in)
                bits["kick products"] = max(bits["kick products"], bits_of(2 * pin + 1), bits_of(2 * (pin + right) + 1))
        bits["kick products"] = max(bits["kick products"], bits_of(iv.forms))
        # B: LC-S1 and the lift on the carrier's time line at the start
        x = iv.x_now
        rule = node.rule_of(node.row(CARRIER), iv.c, iv.factors)
        weighted = lift = 0
        pi2 = iv.pi * iv.pi
        for port, reach in enumerate(rule.reaches):
            d = across(x, port) - x
            lift += total(reach * d)
            # reach = 2 num p_i^2 Q G^2: divide the pace squared out exactly
            q = reach // pi2
            assert bool(np.all(q * pi2 == reach))
            weighted += total(q * d)
        b_total += 1
        b_zero += weighted == 0
        lifts.append(lift)
        iv.writes()
        node.set_rows(iv.out)
        iv.rest()
        w_stepped = charge_total(node)
        # the swap and the close, as interval.close() does them, with the readings between
        counters = ([a.copy() for a in node.standing], [a.copy() for a in node.crossed], [a.copy() for a in node.beats])
        before_swap = [[line.copy() for line in row] for row in node.rows()]
        top = node.swap(iv.held, iv.frozen)
        w_swapped = charge_total(node)
        if top.any():
            for rec, r in enumerate(node.records()):
                # W even under C T_0: the exchanged pre-state's Wronskian against the pre-state's (iv.held), at the turned Nodes
                wb = gram.charge(r.shape, iv.held[node.rows_.index(r)])
                wa = gram.charge(r.shape, r.lines)
                turned_total += int(top.sum())
                turned_even += int(np.sum((wb == wa) & top))
            if involution is None:
                probe = Node.__new__(Node)
                probe.rows_ = node.rows_
                probe.rows = node.rows
                once = [[line.copy() for line in row] for row in node.rows()]
                # the exchange applied again with the rows as they stand as the held rows
                saved = [[line.copy() for line in row] for row in node.rows()]
                node.exchange(top, once)
                twice_ok = all(
                    bool(np.all(a.now[top] == b.now[top]))
                    and bool(np.all(a.before[top] == b.before[top]))
                    and bool(np.all(a.rem[top] == b.rem[top]))
                    and (a.wr is None or bool(np.all(a.wr[top] == b.wr[top])))
                    for a, b in zip(node.all_lines(), [l for row in iv.held for l in row], strict=True)
                )
                involution = twice_ok
                # restore the swapped state
                node.set_rows([[line.copy() for line in row] for row in saved])
        log_from = len(node.log)
        # D: the share's numerator at the close (gram.share's (o + o - s) X): read the share's largest term by the census of owns
        node.click(iv.plane_starts, iv.held)
        node.stack.append({"turned": top, "counters": counters, "log_from": log_from, "frozen": iv.frozen})
        w_closed = charge_total(node)
        w_course.append((node.interval, w_start, w_stepped, w_swapped, w_closed))
        count, state_bits = node.census()
        bits["state"] = max(bits["state"], state_bits)
        bits["rotate"] = node.max_transient
    # the share's numerator bits: the largest (o + o - s) X over the board at the end, from the share's own terms
    for r in node.records():
        rule = node.rule(r.pair, node.start_content, node.link_factors())
        nows = [line.now for line in r.lines]
        o = rule.wall * (nows[0] * nows[0] + nows[0] * nows[0]) * 2
        bits["share numerator"] = max(bits["share numerator"], bits_of(o * node.start_x))
    # F: the close's lines
    births = [e for e in node.log if e["event"] == "birth"]
    credits = [e for e in node.log if e["event"] == "credit"]
    # a credit's booked is its record's unit (bodies.bodies takes node.units[rec]); a birth's the children's walls
    takes = [(e["taken"], e["booked"]) for e in births] + [(e["taken"], node.units[e["line"]]) for e in credits]
    at_least = sum(1 for taken, booked in takes if taken >= booked)
    exact = sum(1 for taken, booked in takes if taken == booked)
    excess = sum(taken - booked for taken, booked in takes)
    excess_credits = sum(taken - booked for taken, booked in takes[len(births):])
    laid_back = [e for e in credits if "laid_back" in e]
    light_credits = sum(1 for e in credits if e["line"] == rec0)
    w_children = [sum(e["W_children"]) for e in births]
    taken_rows = sorted({e["taken_row"] for e in births})
    children_rows = sorted({e["line_pair"] for e in births})
    # G: the run back
    kept = list(node.log)
    exact_back = 0
    for k in range(len(hashes)):
        node.step_back()
        exact_back += node.state_hash() == hashes[len(hashes) - 1 - k]
    print(json.dumps({
        "world": argv[1], "intervals": n, "cube": node.cube,
        "A momentum form exact of Node-lines": [a_exact, a_total],
        "B LC-S1 weighted Links' sum 0 of intervals": [b_zero, b_total],
        "B lift first/least/largest": [lifts[0], min(lifts), max(lifts)],
        "C W total (interval, start, stepped, swapped, closed) first/last": [w_course[0], w_course[-1]],
        "C W drift by the step, intervals with a change": sum(1 for c in w_course if c[2] != c[1]),
        "C W drift by the swap, intervals with a change": sum(1 for c in w_course if c[3] != c[2]),
        "C W drift by the close, intervals with a change": sum(1 for c in w_course if c[4] != c[3]),
        "C W even at turned Nodes (records x Nodes)": [turned_even, turned_total],
        "C births' W_children sums": sorted(set(w_children)),
        "D bits": bits, "D census count": node.census()[0],
        "E the exchange twice is the identity": involution,
        "F takes: taken >= booked, taken == booked, of": [at_least, exact, len(takes)],
        "F excess taken - booked summed": excess,
        "F excess at the credits alone": excess_credits,
        "F credits' units": sorted({node.units[e["line"]] for e in credits}),
        "F credits laid back, of credits": [len(laid_back), len(credits)],
        "F credits of the gap-0 record": light_credits,
        "F births: taken rows, children's rows, count": [taken_rows, children_rows, len(births)],
        "F refused stop": node.counts["refused_stop"],
        "frozen Node-intervals": frozen_total,
        "G run back exact of": [exact_back, len(hashes)],
        "seconds": (time.monotonic_ns() - t0) // 10**9,
    }))


if __name__ == "__main__":
    main(sys.argv)
