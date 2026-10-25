"""em1's one-Node tests (2026-10-25), integers only, each prediction printed before its measurement:
 (1) the beat of a uniform body (k = 0) at a held content c is the rule's rational, 2 cos omega_c = (2 w - D(c)) / w, D = 12 (den - num) p_0(c)^2 G^2:
     measured from three consecutive re levels at one Node: |w (a_next + a_before) - (2 w - D) a_now| < w at every Node (one rounding);
 (2) the redshift of the body's line between two contents: (1 - cos omega_c1) / (1 - cos omega_c2) = p_0(c1)^2 / p_0(c2)^2 and
     sin(omega_c1 / 2) / sin(omega_c2 / 2) = p_0(c1) / p_0(c2) (PC-S3), per 10^9, from the rule's integers (the measured levels' rational beside);
 (3) a lone light quantum at the vacuum: a_next = -a_before at the lone Node (S = 0: 6 R = 2 w for num = den), the period 4; the front reaches
     the distance d first at the interval d (the one-Link reach);
 (4) the band: the content past which a row's beat is above the local light band, g > 2 (p_0 / Gamma)^2 (no k carries the line), and the
     one-axis condition g <= (2 / 3)(p_0 / Gamma)^2, by a search by comparisons on the clock's table.
Usage: python em1_beat.py <universe.json>"""
from __future__ import annotations

import json
import sys

import numpy as np

sys.set_int_max_str_digits(0)
from event_universe import run  # noqa: E402
from event_universe.core import paces, rule3  # noqa: E402
from event_universe.core.paces import sine_den  # noqa: E402
from event_universe.core.rule3 import quotient  # noqa: E402
from event_universe.features import volume  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.rows import CARRIER, PLANE  # noqa: E402


class Held(Node):
    """The carrier held by hand at a uniform content (the toy's `well held`, uniform): `carried` returns the lines unchanged."""

    content_held = 0

    def __init__(self, universe, world):
        super().__init__(universe, world)
        m = self.row(CARRIER).lines[0]
        level = int(np.asarray(volume.volume_of(self.gamma, np.array([self.content_held], dtype=object)), dtype=object).reshape(-1)[0])
        m.now[:] = level
        m.before[:] = level
        self.ride_walls()

    def carried(self, lines, r, numerators, direction, top, kept):
        return lines


def beat_test(universe, c, rec, amplitude, cube=3, steps=3):
    Held.content_held = c
    world = {"universe": "x", "shape": [cube] * 3, "intervals": steps, "seed": []}
    node = Held(universe, world)
    row = node.records()[rec]
    num, den = row.pair
    s = sine_den(num, den)
    re_before = quotient(amplitude * num, den)
    im_before = quotient(amplitude * s, den)
    node.lay(rec, Ellipsis, (amplitude, re_before, 0, im_before))
    content = node.content()
    clock = int(np.asarray(paces.clock_of(node.gamma, content), dtype=object).reshape(-1)[0])
    rule = node.rule_of(row, content, node.link_factors())
    w, d = int(rule.wall), int(np.asarray(rule.mass).reshape(-1)[0])
    at = (cube // 2,) * 3
    levels = [int(row.lines[0].now[at])]
    for _ in range(steps):
        node.step()
        levels.append(int(row.lines[0].now[at]))
    # the Wronskian at the Node and the share, for the identity share = 6 s W
    re, im = row.lines
    wr = int(re.now[at] * im.before[at] - im.now[at] * re.before[at])
    rr = node.rule_of(row, node.content(), node.link_factors())
    owns = int((node.share(re, rr, vacuum=True) + node.share(im, rr, vacuum=True))[at])
    residuals = []
    for k in range(1, len(levels) - 1):
        a_b, a_n, a_x = levels[k - 1], levels[k], levels[k + 1]
        residuals.append(w * (a_x + a_b) - (2 * w - d) * a_n)
    return {
        "content": int(content[at]),
        "clock_p0": clock,
        "w": w,
        "D": d,
        "levels": levels,
        "residual_w_(a_next+a_before)-(2w-D)a_now": residuals,
        "residual_within_w": all(abs(x) < w for x in residuals),
        "one_minus_cos_per_1e9_rule": quotient(10**9 * d, 2 * w),
        "one_minus_cos_per_1e9_levels": None
        if levels[1] == 0
        else quotient(10**9 * (2 * levels[1] - levels[2] - levels[0]), 2 * levels[1]),
        "W_at_node": wr,
        "owns_at_node": owns,
        "owns_over_6sW_per_1000": None if wr == 0 else quotient(1000 * owns, 6 * s * abs(wr)),
        "run_back_hash_check": None,
    }


def light_test(universe, cube=5, steps=8):
    Held.content_held = 0
    world = {"universe": "x", "shape": [cube] * 3, "intervals": steps, "seed": []}
    node = Held(universe, world)
    gap0 = node.row(PLANE, gap=0)
    rec = node.records().index(gap0)
    c = cube // 2
    centre = (c, c, c)
    node.lay(rec, centre, (5 * node.drift, 0, 0, 0))
    series = [int(gap0.lines[0].now[centre])]
    first_nonzero = {}
    for t in range(1, steps + 1):
        node.step()
        re = gap0.lines[0]  # the row's lines are replaced by every interval: read the row, never a kept Line
        series.append(int(re.now[centre]))
        for idx in np.ndindex(*node.shape):
            if int(re.now[idx]) != 0:
                d = sum(min(abs(idx[a] - c), cube - abs(idx[a] - c)) for a in range(3))
                first_nonzero.setdefault(d, t)
    rule = node.rule_of(gap0, node.content(), node.link_factors())
    return {
        "S_lone_light": int(np.asarray(rule.self_coefficient).reshape(-1)[0]),
        "six_R_minus_2w": int(sum(int(np.asarray(x).reshape(-1)[0]) for x in rule.reaches) - 2 * int(rule.wall)),
        "centre_series": series,
        "period_4_check_a[t+2]==-a[t]": [series[k + 2] == -series[k] for k in range(0, 3)],
        "first_nonzero_interval_by_distance": dict(sorted(first_nonzero.items())),
        "reach_one_link_per_interval": all(first_nonzero[d] == d for d in first_nonzero if d > 0),
    }


def band_test(universe):
    ints = universe["integers"]
    den, gamma = int(ints["den"]), int(ints["node_clock"])
    found = []
    for r in universe["rows"]:
        if int(r["shape"]) != 2 or r["pair"][0] == r["pair"][1]:
            continue
        num = int(r["pair"][0])
        g_num = den - num  # g = g_num / den
        # the beat above the local band where g Gamma^2 > 2 p_0(c)^2: the least such content by a search by comparisons
        c_trap = None
        c_axis = None
        for c in range(0, paces.frozen_content(gamma) + 1):
            p0 = paces.clock(gamma, c)
            if c_trap is None and g_num * gamma * gamma > 2 * p0 * p0 * den:
                c_trap = c
            if c_axis is None and 3 * g_num * gamma * gamma > 2 * p0 * p0 * den:
                c_axis = c
            if c_trap is not None and c_axis is not None:
                break
        found.append(
            {
                "num": num,
                "g_per_1e9": quotient(10**9 * g_num, den),
                "content_where_line_leaves_light_band": c_trap,
                "content_where_line_leaves_one_axis_band": c_axis,
                "frozen_content": paces.frozen_content(gamma),
            }
        )
    return found


def main(argv):
    universe = json.load(open(argv[1]))
    gamma = int(universe["integers"]["node_clock"])
    out = {}
    print("PREDICTION (1): residual within w at every step for rows 1 and 2 at c = 0 and c = 300; (2) rows records()[0] (the light lift) and [1] (the heavy lift); the ratio per 1e9 equals clock(300)^2 / Gamma^2 =", quotient(10**9 * paces.clock(gamma, 300) ** 2, gamma * gamma), "and the half-sine ratio clock(300) / Gamma per 1e9 =", quotient(10**9 * paces.clock(gamma, 300), gamma))
    for rec, amp in ((0, 10**7), (1, 10**4)):
        for c in (0, 300):
            out[f"beat_row{rec}_c{c}"] = beat_test(universe, c, rec, amp)
    for k, v in out.items():
        print(k, json.dumps(v))
    b0, b3 = out["beat_row1_c0"], out["beat_row1_c300"]
    print("redshift row1 (the heavy lift, records()[1]) (1-cos) ratio per 1e9 from the rule:", quotient(10**9 * b3["D"], b0["D"]), " from the levels:", None if not b0["one_minus_cos_per_1e9_levels"] else quotient(10**9 * b3["one_minus_cos_per_1e9_levels"], b0["one_minus_cos_per_1e9_levels"]))
    print("PREDICTION (3): S_lone_light 0, period 4 (a[t+2] == -a[t]) true x3, first nonzero at distance d at interval d")
    print("light", json.dumps(light_test(universe)))
    print("PREDICTION (4): row 2 of the middle den (g 0.694) leaves the one-axis band at the vacuum (content 0) and the light band near content 529; row 1 (g 1.7e-5) never before the frozen content")
    print("band", json.dumps(band_test(universe)))


if __name__ == "__main__":
    main(sys.argv)
