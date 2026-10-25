"""cs4's one-Node test of the stop's condition (integers only): the cycle board laid at n quanta on a universe file, then at the seed (interval 0) for every gapped plane the walls a birth books (close.lay_cost at the two ends of one passing Link) and, at one Node of every phase class, the full fall of the light's re line (take.fall_of with walls 1: the fall at the full move, or None with the fall below 1), the fall at one, two and three levels (3 den (2 A k - k^2) by the algebra, checked against fall_of's least root at those walls), the share and the slack above the unit. The pass predicate (this head, MS-S1: the lay (A, B) with A B = T div 2 the same for every row): walls = 6 den (A^2 + B^2) X / Gamma for every plane alike (218,166 den at T 36,000: 125^2 + 144^2 = 36,361), whatever its s; the full fall = 3 den A^2 at the classes with p even and negative at the classes with p odd; the slack 6 den (A^2 - n 18,000).
Usage: python one_node_test.py <world.json> <pattern.json>"""
import json
import sys

import numpy as np

import cs4_run
from event_universe import close, readings, take
from event_universe.core.paces import sine_den
from event_universe.loader.world import load_world
from event_universe.rows import PLANE


def main(argv):
    sys.set_int_max_str_digits(0)
    universe, world = load_world(argv[1])
    pattern = json.load(open(argv[2], encoding="utf-8"))
    node = cs4_run.CsNode(universe, world, pattern)
    A = node.lay_line["amplitude"]
    den, T = node.den, node.T
    print("A", A, "unit of the light", node.unit_gap0, "= 3 T den", 3 * T * den == node.unit_gap0)
    c = node.start_content
    frozen = readings.frozen_of(node, c)
    factors = node.link_factors(None, frozen)
    gap0 = node.row(PLANE, gap=0)
    r0 = node.rule_of(gap0, c, factors)
    re = gap0.lines[0]
    share = node.share(gap0.lines, r0)
    sh = cs4_run.ints(share)
    print("share min/max", min(sh), max(sh), "6 den A^2", 6 * den * A * A, "slack min", min(sh) - node.unit_gap0, "6 den (A^2 - n 18000)", 6 * den * (A * A - int(pattern.get("quanta", 1)) * 18000))
    # the walls per plane at one Link's ends (0,0,0) and (1,0,0)
    minus, plus = (0, 0, 0), (1, 0, 0)
    ok = True
    for s, row in enumerate(node.records()):
        if row.gap == 0:
            continue
        walls = close.lay_cost(node, s, minus, plus, c, factors)
        sine = sine_den(row.pair[0], den)
        lay_walls = 6 * den * (node.A * node.A + node.B * node.B)
        print("plane", s, "num", row.pair[0], "s", sine, "walls", walls, "6 den (A^2 + B^2) with (A, B)", (node.A, node.B), lay_walls, "equal", walls == lay_walls, "walls over den", walls // den, "6 T s (the former lay's two units)", 6 * T * sine)
        ok = ok and walls == lay_walls
    # the fall per phase class
    phases = cs4_run.PHASES
    seen = set()
    for n, at in enumerate(np.ndindex(*node.shape)):
        p = phases[n]
        if p in seen:
            continue
        seen.add(p)
        now, before = int(re.now[at]), int(re.before[at])
        levels, fall = take.fall_of(node, at, 1, r0, re)
        full = take.fall_of(node, at, 3 * den * A * A, r0, re)
        line = f"class p {p} at {at}: re now {now} before {before}: least take {fall} (levels {levels}); the full fall asked at 3 den A^2 {3 * den * A * A}: {full}"
        for k in (1, 2, 3):
            algebra = 3 * den * (2 * A * k - k * k)
            got = take.fall_of(node, at, algebra, r0, re)
            line += f"; k {k}: algebra {algebra} fall_of {got}"
        print(line)
        if p % 2 == 0:
            ok = ok and levels == 1 and fall == 3 * den * (2 * A - 1) and full == (A, 3 * den * A * A)
        else:
            ok = ok and levels is None and fall < 0
    lay_walls = 6 * den * (node.A * node.A + node.B * node.B)
    print("the stop's condition: a birth needs the full fall 3 den A^2 at or above the walls", lay_walls // den, "den: A at least", min(a for a in range(1, 100000) if 3 * a * a >= 6 * (node.A * node.A + node.B * node.B)), "; this lay's A", A, "pays" if 3 * den * A * A >= lay_walls else "does not pay", "; the least k with 3 den (2 A k - k^2) at or above the walls:", next((k for k in range(1, A + 1) if 3 * den * (2 * A * k - k * k) >= lay_walls), None))
    print("PASS" if ok else "FAIL")


if __name__ == "__main__":
    main(sys.argv)
