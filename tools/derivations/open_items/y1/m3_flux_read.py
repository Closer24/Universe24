"""m3 (hand y1): the flux lines' read. (1) K = omega_0 Gamma to the unit for the two points of den 1,021 by the search on the phase line's orbit (plane.rotation_unit), the float acos beside it as a check and not a reading. (2) Gravity's fold pair on a vacuum Link, X_ij = 2 num G^2, at V_ij = -50..50 with the sign's pair at n = 0, and composed with the sign's pair at n = 200: the integers (X^c, X^s). (3) On the flagged engine (U24_METRIC=1) at the interval 5 of the bare 3-cube hole seed, the volume row's flux lines fed by hand (uniform, then random within 60), every born plane record's Link pairs read through flux.pairs_of: the odd part through the -a Port at the Node i + a against minus the odd part through the +a Port at i (X^s_ji = -X^s_ij), the even parts equal, on every Link; light's pairs None (a real line reads no fold). (4) The theorem for a one-part real line: a ring of 24 Nodes, light's pair at the vacuum, Rule3 in integers with an odd Link coefficient e on the +x reach and -e on the -x reach: the largest level over 300 intervals at e = 0, R div 100 and R div 10 (growth), against the plane (re, im) with the Peierls pair (R cos, R sin) at the same angle, bounded. Integers only; the one float is the check in (1)."""
from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import y1lib  # noqa: E402

assert os.environ.get("U24_METRIC") == "1"
from event_universe import flux, plane, records  # noqa: E402
from event_universe.core import paces, rule3  # noqa: E402
from event_universe.core.paces import rounded  # noqa: E402
from event_universe.features.phase import signed_rounded  # noqa: E402

GAMMA, DEN, G = 1000, 1021, 16
out: dict = {}

# (1) K
out["K"] = {}
for num in (779, 660, 1021):
    k = plane.rotation_unit((num, DEN), GAMMA)
    out["K"][str(num)] = {"K_integer": k, "float_check_acos_times_Gamma": round(math.acos(num / DEN) * GAMMA, 3)}
print("K", out["K"])

# (2) the fold pair on a vacuum Link
x = 2 * 779 * G * G
k = plane.rotation_unit((779, DEN), GAMMA)
table = []
for v in (-50, -5, -1, 0, 1, 5, 50):
    odd = int(signed_rounded(6 * x * k * v, GAMMA * GAMMA))
    e0, o0 = plane.fold_pairs((779, DEN), GAMMA, (G * G,), (v,), (x,), (0,))
    n = 200
    wall = plane.link_wall(GAMMA)
    circle = wall * wall + n * n
    xc, xs = int(rounded(x * (wall * wall - n * n), circle)), int(signed_rounded(x * 2 * wall * n, circle))
    e1, o1 = plane.fold_pairs((779, DEN), GAMMA, (G * G,), (v,), (xc,), (xs,))
    table.append({"V_ij": v, "X_ij": x, "Xs_gravity": odd, "composed_with_sign_n0": [int(e0[0]), int(o0[0])], "sign_pair_n200": [xc, xs], "composed_with_sign_n200": [int(e1[0]), int(o1[0])]})
out["fold_pairs"] = table
print("fold", json.dumps(table))

# (3) the two ends on the engine
board = y1lib.board_of(Path("/dev/shm/tmp/y1_m3"))
for _ in range(5):
    board.step()
volume = board.held[0]
gamma, unit = board.world.node_clock, board.unit
checks = []
rng = np.random.default_rng(17)
for label, fed in (("uniform_20", [np.full(board.shape, 20, dtype=object)] * 3), ("random_60", [np.asarray(rng.integers(-60, 61, board.shape), dtype=object) for _ in range(3)])):
    lines = list(board.states[volume].lines)
    for a in range(3):
        lines[4 + a] = records.Record(fed[a], fed[a].copy(), lines[4 + a].remainder)
    board.states[volume].lines = lines
    equal_even = opposite_odd = links = 0
    for index in board.turning:
        fam = board.families[index]
        for record in range(len(board.states[index].lines) // (fam.parts * fam.width)):
            content, factors = board.read(index, 1, record)
            pairs = flux.pairs_of(index, board.families, board.states, 1, gamma, content, factors, record, board.amplitude)
            assert pairs is not None
            evens, odds = pairs
            square = np.asarray(paces.link_pace_of(gamma, content), dtype=object) ** 2  # the pair in the Link unit, R / p_i^2, exact
            for axis in range(3):
                plus, minus = np.asarray(evens[2 * axis], dtype=object) // square, np.asarray(evens[2 * axis + 1], dtype=object) // square
                oplus, ominus = np.asarray(odds[2 * axis], dtype=object) // square, np.asarray(odds[2 * axis + 1], dtype=object) // square
                far_minus = np.roll(minus, -1, axis=axis)  # the -a Port's read at the Node i + a
                far_ominus = np.roll(ominus, -1, axis=axis)
                links += plus.size
                equal_even += int(np.sum(plus == far_minus))
                opposite_odd += int(np.sum(oplus == -far_ominus))
    light_pairs = flux.pairs_of(board.world.seed, board.families, board.states, 1, gamma, *board.read(board.world.seed, 1, 0), 0, board.amplitude)
    checks.append({"fed": label, "links": links, "even_equal_from_both_ends": equal_even, "odd_opposite_from_both_ends": opposite_odd, "nonzero_odd_parts": int(sum(int(np.count_nonzero(np.asarray(o, dtype=object))) for index in board.turning if len(board.states[index].lines) for o in flux.pairs_of(index, board.families, board.states, 1, gamma, *board.read(index, 1, 0), 0, board.amplitude)[1])), "light_pairs_is_None": int(light_pairs is None)})
out["two_ends"] = checks
print("two ends", json.dumps(checks))

# (4) the ring theorem
N = 24
w = rule3.wall_of(DEN, GAMMA, G)
R = 2 * DEN * GAMMA * GAMMA * G * G  # light's reach at the vacuum, Q = G^2, p = Gamma
shape = (N, 1, 1)


def ring_real(e: int, intervals: int) -> dict:
    now = np.zeros(shape, dtype=object)
    now[0, 0, 0] = 1000
    before = now.copy()
    r = np.full(shape, w // 2, dtype=object)
    reaches = (R + e, R - e, R, R, R, R)
    largest = []
    for t in range(1, intervals + 1):
        f = flux.link_fluxes(now, reaches)
        nxt, r = rule3.rule3(f, 0, w, now, before, r)
        now, before = np.asarray(nxt, dtype=object), now
        if t in (50, 100, 200, 300):
            largest.append((t, int(np.abs(now).max())))
    return {"e": e, "largest_level_at": largest, "bits_at_end": int(np.abs(now).max()).bit_length()}


def ring_plane(e: int, intervals: int) -> dict:
    """The plane with the Peierls pair at tan theta = e / R on the x Links: (R^c, R^s) = (R, e) on +x and (R, -e) on -x (the two ends' odd parts opposite)."""
    re = np.zeros(shape, dtype=object)
    re[0, 0, 0] = 1000
    im = np.zeros(shape, dtype=object)
    re_b, im_b = re.copy(), im.copy()
    r_re, r_im = np.full(shape, w // 2, dtype=object), np.full(shape, w // 2, dtype=object)
    reaches = (R, R, R, R, R, R)
    evens = (R, R, R, R, R, R)
    odds = (e, -e, 0, 0, 0, 0)
    largest = []
    for t in range(1, intervals + 1):
        f_re, f_im = flux.turned_link_fluxes((re, im), reaches, (evens, odds))
        n_re, r_re = rule3.rule3(f_re, 0, w, re, re_b, r_re)
        n_im, r_im = rule3.rule3(f_im, 0, w, im, im_b, r_im)
        re, re_b = np.asarray(n_re, dtype=object), re
        im, im_b = np.asarray(n_im, dtype=object), im
        if t in (50, 100, 200, 300):
            largest.append((t, int(max(np.abs(re).max(), np.abs(im).max()))))
    return {"e": e, "largest_level_at": largest, "bits_at_end": int(max(np.abs(re).max(), np.abs(im).max())).bit_length()}


out["ring"] = {"N": N, "R": R, "w": w, "real_line": [ring_real(e, 300) for e in (0, R // 100, R // 10)], "plane_peierls": [ring_plane(e, 300) for e in (0, R // 100, R // 10)]}
print("ring", json.dumps(out["ring"]))
(HERE / "m3_flux_read.json").write_text(json.dumps(out, indent=1, default=str))
