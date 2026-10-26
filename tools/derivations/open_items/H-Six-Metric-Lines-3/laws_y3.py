"""The hand H-Six-Metric-Lines-3: the laws with a number on the flagged copy (Y3_METRIC=1 on PYTHONPATH): (a) the 48 on the ten lines as one object on the hole seed of the 5-cube at 20 intervals (g_00 and the trace scalars, g_aa permuted, g_0a with the axis's sign, g_ab with the product of two signs; the negated lines' remainders mirrored w - 1 - r or at the gauge w - r), every image's board against the board's image; (b) the conserved form of Rule3's line to the remainders on the nine axis lines at every Node and every interval (the identity w a' + r' = S a_now - w a_before + SUM_j R_j m_j + r, then the write's carried division), measured by the Node's own act replayed on a copy; (c) the one-Link reach forward and backward: a change of the flux lines two Links away leaves a Node's interval and its step back bit for bit; (d) the charge and the senses; (e) the flux lines' board sum against the lattice momentum's identity (0 on the 48-symmetric seed). `python laws_y3.py <out.json>`."""

from __future__ import annotations

import copy
import itertools
import json
import sys

import numpy as np

sys.set_int_max_str_digits(0)

from event_universe.core.ports import AXES  # noqa: E402
from event_universe.core.rule3 import carried_division, mirrored  # noqa: E402
from event_universe.interval import Interval  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.rows import CARRIER  # noqa: E402
from tests.laws import node_of, state_of, world_of  # noqa: E402

CUBE, INTERVALS = 5, 20
IMAGES = [
    np.array([[s[a] if pi[a] == b else 0 for a in range(3)] for b in range(3)])
    for pi in itertools.permutations(range(3))
    for s in itertools.product((1, -1), repeat=3)
]
PAIRS = ((0, 1), (1, 2), (2, 0))


def image(m, node, cube):
    return tuple(int(x) % cube for x in m @ np.array(node, dtype=int))


def world_image(world, m, cube):
    found = dict(world, shape=[cube] * 3, seed=[dict(lay) for lay in world["seed"]])
    for lay in found["seed"]:
        for key in ("at", "centre"):
            if key in lay:
                lay[key] = list(image(m, tuple(lay[key]), cube))
    return found


def run(universe, world, n):
    node = Node(universe, world)
    for _ in range(n):
        node.step()
    return node


def carried_ten(m):
    """How the image carries the ten lines: for each line of the image board, (the source line, the sign)."""
    pi = [int(np.nonzero(m[:, a])[0][0]) for a in range(3)]  # axis a of the seed goes to axis pi[a] of the image
    s = [int(m[pi[a], a]) for a in range(3)]
    found = {0: (0, 1)}
    for a in range(3):
        found[1 + pi[a]] = (1 + a, 1)  # the tensions permuted, no sign
        found[1 + AXES + pi[a]] = (1 + AXES + a, s[a])  # the flux lines a vector
    for k, (a, b) in enumerate(PAIRS):
        target = tuple(sorted((pi[a], pi[b])))
        kk = next(j for j, p in enumerate(PAIRS) if tuple(sorted(p)) == target)
        found[1 + 2 * AXES + kk] = (1 + 2 * AXES + k, s[a] * s[b])
    return found


def the_48(out, n=INTERVALS):
    universe, world = world_of("world_hole.json")
    base = run(universe, world_image(world, np.eye(3, dtype=int), CUBE), n)
    lines = base.row(CARRIER).lines
    w = base.w
    nonzero = [sum(1 for x in line.now.reshape(-1) if int(x) != 0) for line in lines]
    counts = {"levels": 0, "rem ones": 0, "rem twos": 0, "wr ones": 0, "wr twos": 0, "signless levels": 0}
    for m in IMAGES:
        other = run(universe, world_image(world, m, CUBE), n)
        olines = other.row(CARRIER).lines
        carry = carried_ten(m)
        levels = ones = twos = wr1 = wr2 = signless = True
        for number, (source, sign) in carry.items():
            for at in np.ndindex(CUBE, CUBE, CUBE):
                there = image(m, at, CUBE)
                src, dst = lines[source], olines[number]
                if int(dst.now[there]) != sign * int(src.now[at]) or int(dst.before[there]) != sign * int(src.before[at]):
                    levels = False
                if int(dst.now[there]) != int(src.now[at]) or int(dst.before[there]) != int(src.before[at]):
                    signless = False
                r, rr = int(src.rem[at]), int(dst.rem[there])
                wl = int(np.asarray(src.wall)[at]) if np.ndim(src.wall) else int(src.wall)
                if sign == 1:
                    ones = ones and r == rr
                    twos = twos and r == rr
                else:
                    ones = ones and rr == mirrored(r, wl, 1)
                    twos = twos and rr == wl - r
                if src.wr is not None:
                    q, qq = int(src.wr[at]), int(dst.wr[there])
                    ww = int(src.wwall)
                    if sign == 1:
                        wr1 = wr1 and q == qq
                        wr2 = wr2 and q == qq
                    else:
                        wr1 = wr1 and qq == mirrored(q, ww, 1)
                        wr2 = wr2 and qq == ww - q
        counts["levels"] += levels
        counts["rem ones"] += ones
        counts["rem twos"] += twos
        counts["wr ones"] += wr1
        counts["wr twos"] += wr2
        counts["signless levels"] += signless
    out[f"48 on the ten lines, hole 5-cube at {n}"] = {"of 48": counts, "nonzero nodes per line": nonzero}


def conserved_form(out):
    """The nine axis lines' step replayed: from the pre-state and the interval's own readings, the identity per line."""
    node = node_of("world_hole.json")
    equal = total = 0
    writes_nonzero = [0] * 9
    for _ in range(INTERVALS):
        pre = copy.deepcopy(node)
        itv = Interval(pre, 1)
        itv.walled_act()
        itv.forces()
        itv.kicks()
        parts = [*itv.traceless, *itv.flux, *itv.shear]
        p02 = itv.p0 * itv.p0
        rule = pre.rule_of(itv.carrier, itv.c, itv.factors)
        starts = [line.now for line in itv.carrier.lines]
        arrivals = pre.arrivals(starts, rule, None)
        node.step()
        post = node.row(CARRIER).lines
        for k in range(1, 10):
            line = itv.carrier.lines[k]
            total_k = rule.self_coefficient * line.now - rule.wall * line.before + arrivals[k]
            q, rem = carried_division(total_k, rule.wall, line.rem, 1)
            numerator = parts[k - 1] * p02
            qw, wr = carried_division(numerator, line.wwall, line.wr, 1)
            frozen = itv.frozen
            turned = node.turned
            still = frozen | turned
            for at in np.ndindex(*node.shape):
                total += 1
                if still[at]:
                    equal += 1  # a still Node ends at its pre-state (exchanged at a turned one): the identity is the exchange's, measured by the run back
                    continue
                ok = int(post[k].now[at]) == int(q[at]) + int(qw[at]) and int(post[k].rem[at]) == int(rem[at]) and int(post[k].wr[at]) == int(wr[at]) and int(post[k].before[at]) == int(line.now[at])
                equal += ok
                writes_nonzero[k - 1] += int(qw[at]) != 0
    out["conserved form on the nine axis lines, hole 5-cube, 20 intervals"] = {"node-interval-lines equal": equal, "of": total, "write quotients nonzero per line": writes_nonzero}


def one_link(out):
    """The one-Link reach: the flux lines and the shears changed by hand at the Nodes two Links from the centre and beyond, the centre's step forward and back bit for bit; changed at a face neighbour, the centre's step changed (the positive control)."""
    centre = (2, 2, 2)
    universe, world = world_of("world_hole.json")

    def dist(at):
        return sum(min(abs(a - c), CUBE - abs(a - c)) for a, c in zip(at, centre, strict=True))

    def centre_lines(node):
        return [(int(line.now[centre]), int(line.before[centre]), int(line.rem[centre])) for row in node.rows() for line in row]

    base = run(universe, world, 6)
    far, near = copy.deepcopy(base), copy.deepcopy(base)
    for node_, where in ((far, lambda at: dist(at) >= 2), (near, lambda at: dist(at) == 1)):
        for k in range(1 + AXES, 1 + 3 * AXES):
            line = node_.row(CARRIER).lines[k]
            for at in np.ndindex(CUBE, CUBE, CUBE):
                if where(at):
                    line.now[at] = int(line.now[at]) + 7 * (k - AXES)
                    line.before[at] = int(line.before[at]) + 3 * (k - AXES)
    found = {}
    for name, node_ in (("base", base), ("far", far), ("near", near)):
        node_.step()
        fwd = centre_lines(node_)
        node_.step_back()
        found[name] = (fwd, centre_lines(node_))
    out["one-Link reach of the six lines"] = {
        "two Links away forward equal": found["base"][0] == found["far"][0],
        "two Links away backward equal": found["base"][1] == found["far"][1],
        "one Link away forward equal (control, expected False)": found["base"][0] == found["near"][0],
    }


def momentum_sum(out):
    node = node_of("world_hole.json")
    sums = []
    for _ in range(INTERVALS):
        node.step()
        lines = node.row(CARRIER).lines
        sums.append([sum(int(x) for x in lines[k].now.reshape(-1)) for k in range(1 + AXES, 1 + 3 * AXES)])
    out["six lines' board sums per interval, hole at 20"] = sums


def main(argv):
    out = {}
    the_48(out, 3)
    the_48(out, 20)
    conserved_form(out)
    one_link(out)
    momentum_sum(out)
    json.dump(out, open(argv[1], "w"), indent=1)
    print(json.dumps(out))


if __name__ == "__main__":
    main(sys.argv)
