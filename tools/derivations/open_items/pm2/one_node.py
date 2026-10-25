"""pm2's one-Node test (section 2): two Nodes stepped side by side on one world, the flag off and on (the copy src_pm2), N intervals; at every interval the state bytes compared (which integers change, at which interval first), the readings at every Node of every record under the three weights (the vacuum's 4 Gamma^2 G^2, the carrier's 4 Gamma^3 G^2 / X, the frame's 4 p^2 G^2) with the carrier's factor X / Gamma in thousandths, the run back, the census (count, bits), the current's antisymmetry F_ij + F_ji on every Link of every line, and the conserved form's share summed over the board. Usage: python one_node.py <world.json> <intervals> [weight_kind]"""
import json
import sys

sys.set_int_max_str_digits(0)
import numpy as np

from event_universe.core import paces
from event_universe.core.ports import PORTS, across
from event_universe.core.rule3 import division_forward
from event_universe.links import link_current
from event_universe.loader.world import load_world
from event_universe.node import Node
from event_universe.rows import CARRIER, PLANE


def shares(node):
    """Every record's share at the start levels under the three weights, summed re + im, at every Node."""
    c = node.start_content
    factors = node.start_factors
    pace = paces.link_pace_of(node.gamma, c)
    x = node.start_x if getattr(node, "start_x", None) is not None else node.row(CARRIER).lines[0].now
    out = []
    for rec, r in enumerate(node.records()):
        rr = node.rule_of(r, c, factors)
        kind = getattr(node, "weight_kind", None)
        node.weight_kind = None
        vac = sum(node.share(line, rr, pace, vacuum=True) for line in node.stepped[rec]) if False else None
        found = []
        for line in r.lines:
            # the form's numerator as readings.share builds it, by the vacuum call times 4 Gamma^2 G^2 (exact: the division is by the weight alone)
            pass
        node.weight_kind = kind
        out.append(rr)
    return out


def numerators(node, line, r):
    """readings.share's numerator at every Node (the doubled form less the shared Link products), rebuilt here to read it under the three weights."""
    from event_universe.core.rule3 import form_term
    from event_universe.rows import zeros

    reached, shared = zeros(node.shape), zeros(node.shape)
    for port, reach in enumerate(r.reaches):
        b_j, n_j = across(line.before, port), across(line.now, port)
        reached = reached + reach * b_j
        shared = shared + reach * (line.before - b_j) * (line.now + n_j)
    found = form_term(r.self_coefficient, r.wall, line.now, line.before) - line.now * reached
    return found + found - shared


def main(argv):
    universe, world = load_world(argv[1])
    n = int(argv[2])
    kind = argv[3] if len(argv) > 3 else "carrier"
    off = Node(universe, dict(world))
    on = Node(universe, dict(world, pm2_weight=kind))
    gamma, g2 = off.gamma, off.G * off.G
    first_diff = None
    hashes_off, hashes_on = [], []
    for t in range(n):
        hashes_off.append(off.state_hash())
        hashes_on.append(on.state_hash())
        off.step()
        on.step()
        same = off.state_bytes() == on.state_bytes()
        if not same and first_diff is None:
            first_diff = off.interval
            lines_off, lines_on = off.all_lines(), on.all_lines()
            changed = [k for k, (a, b) in enumerate(zip(lines_off, lines_on)) if not (np.array_equal(a.now, b.now) and np.array_equal(a.before, b.before) and np.array_equal(a.rem, b.rem))]
            print(json.dumps({"first interval the states part": first_diff, "lines changed (acts' order index)": changed, "counts off": off.counts, "counts on": on.counts}))
        if off.interval in (1, 2, 5, 10, 20, 40, 60, 100, 150, 200, 300) or off.interval == n:
            # the readings at the start of the NEXT interval: the state now; X and content per Node
            x = off.row(CARRIER).lines[0].now
            c = off.content()
            pace = paces.link_pace_of(gamma, c)
            factors = off.link_factors()
            ratio = [int(division_forward(int(v) * 1000, gamma, 0)[0]) for v in x.reshape(-1)]
            row = {"i": off.interval, "same state": same, "X/Gamma thousandths min/max": [min(ratio), max(ratio)], "content min/max": [int(c.min()), int(c.max())]}
            for rec, r in enumerate(off.records()):
                rr = off.rule_of(r, c, factors)
                num = sum(numerators(off, line, rr) for line in r.lines)
                vac = [int(v) for v in np.asarray(division_forward(num, 4 * gamma * gamma * g2, 0)[0]).reshape(-1)]
                car = [int(v) for v in np.asarray(division_forward(num * x, 4 * gamma**3 * g2, 0)[0]).reshape(-1)]
                sq = pace * pace
                frm = [int(v) for v in np.asarray(division_forward(num, 4 * sq * g2 + (sq == 0), 0)[0]).reshape(-1)]
                unit = off.units[rec]
                row[f"rec {rec} (pair {str(r.pair[0])[:6]}..)"] = {
                    "unit": unit,
                    "share max vacuum/carrier/frame (units, thousandths)": [max(vac) * 1000 // unit, max(car) * 1000 // unit, max(frm) * 1000 // unit],
                    "nodes at or above one unit vacuum/carrier/frame": [sum(1 for v in vac if v >= unit), sum(1 for v in car if v >= unit), sum(1 for v in frm if v >= unit)],
                    "carrier against frame: nodes equal / carrier larger / frame larger": [sum(1 for a, b in zip(car, frm) if a == b), sum(1 for a, b in zip(car, frm) if a > b), sum(1 for a, b in zip(car, frm) if a < b)],
                }
            # the current's antisymmetry on every Link of every plane line (the state now)
            anti = 0
            for r in off.records():
                for line in r.lines:
                    for axis in range(3):
                        f = link_current(line, 2 * axis)
                        fb = across(link_current(line, 2 * axis + 1), 2 * axis)  # the other end's read of the same Link
                        anti += int(sum(1 for v in (f + fb).reshape(-1) if int(v) != 0))
            row["F_ij + F_ji != 0 (count over Links x lines)"] = anti
            row["census off (arrays, bits) / on"] = [list(off.census()), list(on.census())]
            row["transient bits off / on"] = [off.max_transient, on.max_transient]
            print(json.dumps(row))
    back_off = back_on = 0
    for k in range(min(10, n)):
        off.step_back()
        on.step_back()
        back_off += off.state_hash() == hashes_off[n - 1 - k]
        back_on += on.state_hash() == hashes_on[n - 1 - k]
    print(json.dumps({"run back off": back_off, "run back on": back_on, "of": min(10, n), "first interval the states part": first_diff, "counts off": off.counts, "counts on": on.counts}))


if __name__ == "__main__":
    main(sys.argv)
