"""Every derived number of the paper recomputed from the paper's own integers and the run's data, and compared with what the text prints: the rule's integers for the two pairs, Table 1's step and step back by equation (1), the long-wave speed, the clock 5,429 and 0.905, equation (2) and 0.900, the no-click weight 0.811 and the chance 0.558 from the report's shares by the click's formulas, the wiping's ball (the layer 4t^2 + 2, N(t), the full tube 2L^2) against the run's layers, the first-order slope 1.06 and c_m = 0.50, a bound body's v < c, c_m < c, the fourth-order factor 1.69 and the two-way reading u, light near matter (c (rate/q_0)^2 on a row, the exponents 2 : 1, the frozen content) and the board's momentum P_a kept by the step, a short pattern's slowing and the tick's bound from the highest-energy light seen, the counts 18,560, 18,176 and the shells' sum 9,279, the Node's clock at 600 units (4,912, the integers 648,000,000 / 96,510,976 / 363,245,652, the angles 0.84107 and 0.75672) and the moving clock (0.92532, 0.1967, 0.9165), with the board's counts in run_clocks.json (722.5 / 803.0 and 147.5 / 160.5) against the printed 0.900 and 0.92. Usage: python3 -I check_formulas.py <run directory>."""
from __future__ import annotations
import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import plain, read_tex

GAMMA = 6000


def integers(num: int, den: int, clock: int = GAMMA, pace: int = GAMMA) -> tuple[int, int, int]:
    """(w, the neighbour weight, the own weight) as the program's coefficients: w = 6 den Gamma^2, R = 2 num pace^2, S = 12 (den Gamma^2 - (den - num) clock^2) - 6 R."""
    w = 6 * den * GAMMA * GAMMA
    r = 2 * num * pace * pace
    s = 12 * (den * GAMMA * GAMMA - (den - num) * clock * clock) - 6 * r
    return w, r, s


def step(w: int, r: int, s: int, arrivals: list[int], now: int, before: int, rem: int) -> tuple[int, int]:
    total = sum(r * a for a in arrivals) + s * now - w * before + rem
    return total // w, total % w


def step_back(w: int, r: int, s: int, arrivals: list[int], now: int, nxt: int, rem_new: int) -> tuple[int, int]:
    left = w * nxt + rem_new - sum(r * a for a in arrivals) - s * now
    return -(left // w), left % w


def fmt(n: int) -> str:
    return f"{n:,}"


def main(argv: list[str]) -> int:
    run_dir = Path(argv[1]) if len(argv) > 1 else Path(".")
    source = read_tex()
    text = plain(source)
    rows = re.sub(r"(?<=\d),(?=\d{3}\b)", "", re.sub(r"(?<!\\)%.*", "", source))
    text_n = re.sub(r"(?<=\d),(?=\d{3}\b)", "", text)
    problems = []

    def check(name: str, ok: bool, detail: str = "") -> None:
        print(("ok       " if ok else "MISMATCH ") + name + (": " + detail if detail else ""))
        if not ok:
            problems.append(name)

    # (a) the rule's integers for the two pairs, as printed
    for num, den, label in ((1, 1, "light's pair 1 and 1"), (2, 3, "matter's pair 2 and 3")):
        w, r, s = integers(num, den)
        check(f"{label}: w, neighbour weight, own weight", all(str(v) in text_n for v in (w, r)) and s == 0, f"{fmt(w)}, {fmt(r)}, {s}")
    # (b) Table 1's step and step back by equation (1)
    arrivals = [3, 3, 2, 2, 1, 1]
    for num, den, want in ((1, 1, (3, 0)), (2, 3, (1, 432000000))):
        w, r, s = integers(num, den)
        nxt, rem = step(w, r, s, arrivals, 4, 1, 0)
        back = step_back(w, r, s, arrivals, 4, nxt, rem)
        row = f"& {sum(arrivals) * r} & {w * 1} & {sum(arrivals) * r - w * 1} & {nxt} & {rem} \\\\"
        check(f"Table 1 step for the pair {num} and {den}", (nxt, rem) == want and row in rows, f"total {fmt(sum(arrivals) * r - w)} -> next {nxt}, remainder {fmt(rem)}")
        check(f"the step back for the pair {num} and {den}", back == (1, 0), f"before {back[0]}, remainder {back[1]}")
    # (c) the long-wave speed from R / w = 1/3
    w, r, s = integers(1, 1)
    c = math.sqrt(r / w)
    check("the long-wave speed 0.58 from R/w = 1/3", abs(r / w - 1 / 3) < 1e-12 and f"{c:.2f}" == "0.58" and "0.58" in text, f"c = {c:.4f}")
    if "0.577" in text:
        check("0.577 along a row", f"{c:.3f}" == "0.577")
    # (d) the clock 5,429 and 0.905
    clock = round(GAMMA * (1 - 1 / GAMMA) ** 600)
    check("5,429 = round(6,000 (1 - 1/6,000)^600)", clock == 5429 and "5429" in text_n, str(clock))
    check("0.905 = 5,429 / 6,000", f"{clock / GAMMA:.3f}" == "0.905" and "0.905" in text, f"{clock / GAMMA:.4f}")
    # (e) equation (2) and the ratio of the turn rates at the pair 2 and 3
    def angle(num: int, den: int, clk: int) -> float:
        return math.acos(1 - (1 - num / den) * (clk / GAMMA) ** 2)
    ratio = angle(2, 3, clock) / angle(2, 3, GAMMA)
    check("equation (2): the turn rate at 5,429 over the one at 6,000, 0.900 at the pair 2 and 3", f"{ratio:.3f}" == "0.900" and "0.900" in text, f"{ratio:.4f}")
    # (h) the Node's clock at 600 units: the Link's pace 4,912, the integers at the pair 2 and 3, the two angles and their ratio
    pace = round(clock * clock / GAMMA)
    check("4,912 = round(5,429^2 / 6,000) (computed; the paper no longer prints it)", pace == 4912, str(pace))
    w6, r6, s6 = integers(2, 3, clock=clock, pace=pace)
    check("the integers at the pair 2 and 3 with the clock 5,429: w, neighbour weight, own weight", (w6, r6, s6) == (648000000, 96510976, 363245652), f"{fmt(w6)}, {fmt(r6)}, {fmt(s6)} (computed; the paper no longer prints them)")
    cos6 = (6 * r6 + s6) / (2 * w6)
    check("equation (2) from the integers: (6 R + S) / (2 w) = 1 - (1 - 2/3)(5,429/6,000)^2", abs(cos6 - (1 - (1 - 2 / 3) * (clock / GAMMA) ** 2)) < 1e-12, f"{cos6:.6f}")
    turn0, turn6 = angle(2, 3, GAMMA), angle(2, 3, clock)
    check("the angle per tick 0.84107 at 6,000 and 0.75672 at 5,429, ratio 0.8997", f"{turn0:.5f}" == "0.84107" and f"{turn6:.5f}" == "0.75672" and f"{turn6 / turn0:.4f}" == "0.8997", f"{turn0:.5f}, {turn6:.5f}, {turn6 / turn0:.4f}")
    # (i) the moving clock from the same integers, each Node an eighth of a swing behind the one before (crest to crest 8 Nodes)
    w0, r0, s0 = integers(2, 3)
    part = 2 * math.pi / 8
    cos_m = (s0 + 4 * r0 + 2 * r0 * math.cos(part)) / (2 * w0)
    turn_m = math.acos(cos_m)
    speed = (2 * r0 * math.sin(part) / (2 * w0)) / math.sin(turn_m)
    middle = turn_m - part * speed
    check("the moving form: a fixed Node's angle per tick 0.92532 (1.100 of rest)", f"{turn_m:.5f}" == "0.92532" and f"{turn_m / turn0:.3f}" == "1.100", f"{turn_m:.5f}, {turn_m / turn0:.4f}")
    check("the middle's speed 0.1967 Node per tick, printed 0.1967", f"{speed:.4f}" == "0.1967" and "0.1967" in text, f"{speed:.4f}")
    check("the middle's swings 0.916481 of rest, printed 0.916", f"{middle / turn0:.6f}" == "0.916481" and "0.916" in text and "0.917" not in text, f"{middle / turn0:.6f}")
    # (k) the first-order forms beside the known formulas: the slope 2 tan(turn_0/2)/turn_0 and c_m^2 = turn_0 cot(turn_0)/3
    slope = 2 * math.tan(turn0 / 2) / turn0
    check("the first-order slope 2 tan(turn_0/2)/turn_0 = 1.06 at the pair 2 and 3", f"{slope:.2f}" == "1.06" and "1.06" in text, f"{slope:.4f}")
    cm2 = turn0 * math.cos(turn0) / math.sin(turn0) / 3
    check("c_m^2 = turn_0 cot(turn_0)/3 = 0.251, c_m = 0.50", f"{cm2:.3f}" == "0.251" and f"{math.sqrt(cm2):.2f}" == "0.50" and "0.251" in text and "0.50" in text, f"{cm2:.4f}, {math.sqrt(cm2):.4f}")
    check("the moving form's first order 1 - v^2/(2 c_m^2) matches turn - p v at small p", abs((1 - speed * speed / (2 * cm2)) - (middle / turn0)) < 0.03, f"{1 - speed * speed / (2 * cm2):.4f} against {middle / turn0:.4f} at an eighth")
    # the crossing of the moving clock: the middle's count exceeds the rest's from p = 2.22 at the pair 2 and 3 (v = 0.32 c), 1.99 at top/bottom 0.9, 1.50 at 0.99, 0.35 at 0.999999, 0.08 at 1 - 1e-10 (v near c)
    def crossing(ratio: float) -> tuple[float, float]:
        turn_at = lambda q: math.acos(ratio * (1 - (1 - math.cos(q)) / 3))
        rest_turn = turn_at(0.0)
        lo, hi = 1e-4, math.pi - 1e-4
        f_ = lambda q: turn_at(q) - q * (turn_at(q + 1e-6) - turn_at(q - 1e-6)) / 2e-6 - rest_turn
        for _ in range(200):
            mid = (lo + hi) / 2
            if f_(mid) < 0:
                lo = mid
            else:
                hi = mid
        q = (lo + hi) / 2
        return q, (turn_at(q + 1e-6) - turn_at(q - 1e-6)) / 2e-6 / math.sqrt(1 / 3)
    crossings = {r_: crossing(r_) for r_ in (2 / 3, 0.9, 0.99, 0.999999, 1 - 1e-10)}
    check("the crossing: p = 2.22 at the pair 2 and 3 (v = 0.32 c), 1.99 at 0.9, 1.50 at 0.99, 0.35 at 0.999999, 0.08 at 1 - 1e-10 (v near c)", [round(crossings[r_][0], 2) for r_ in (2 / 3, 0.9, 0.99, 0.999999, 1 - 1e-10)] == [2.22, 1.99, 1.5, 0.35, 0.08] and f"{crossings[2 / 3][1]:.2f}" == "0.32" and crossings[1 - 1e-10][1] > 0.99 and "0.32c" in source and "about two at the worked pair" in text, ", ".join(f"{r_}: p {q_:.2f}, v {v_:.2f} c" for r_, (q_, v_) in crossings.items()))
    # light's cut-off Node: with the reach 0, S = 2w exactly, so next = 2 now - before; the resonance's cosine 5,414/6,000 is light's turn per tick at eight Nodes crest to crest, equation (9) with top equal to bottom
    s_light_cut = 12 * (1 * GAMMA * GAMMA - (1 - 1) * 54 * 54) - 6 * 0
    check("light's cut-off Node: S = 2w at the reach 0, next = 2 now - before; the resonance's cosine 5,414/6,000 = light's turn at p = 2 pi / 8", s_light_cut == 2 * 6 * 1 * GAMMA * GAMMA and "next $= 2\\,\\mathrm{now} - \\mathrm{before}$" in source and abs((1 - (1 - math.cos(2 * math.pi / 8)) / 3) - 5414 / 6000) < 1e-4 and "5,414/6,000" in source, f"S/w = {s_light_cut / (6 * GAMMA * GAMMA):.1f}, cos = {1 - (1 - math.cos(math.pi / 4)) / 3:.4f} against {5414 / 6000:.4f}")
    # (n) a body's own frame: from equation (7) v^2 = r^2 (1 - x^2)/(9 - r^2 (2 + x)^2) with r = top/bottom and x = cos p stays below 1/3 for every r < 1 (a sweep), c_m^2 = turn_0/(3 tan turn_0) < 1/3, the fourth-order factor 2 turn_0/sin(2 turn_0) = 1.69, and the two-way reading u = (v_B - v_A)/(1 - v_A v_B/c^2) below c, equal to the count ratio's reading
    vsq = lambda r_, x_: r_ * r_ * (1 - x_ * x_) / (9 - r_ * r_ * (2 + x_) ** 2)
    sweep = max(vsq(r_ / 100, x_ / 100) for r_ in range(1, 100) for x_ in range(-100, 101))
    check("a bound body's speed squared stays below 1/3 for every top below bottom (r and x swept)", sweep < 1 / 3 and abs(math.sqrt(vsq(2 / 3, math.cos(part))) - speed) < 1e-9, f"the largest {sweep:.4f}; at the pair 2 and 3 and an eighth {math.sqrt(vsq(2 / 3, math.cos(part))):.4f}")
    check("c_m^2 = turn_0/(3 tan turn_0) is below light's 1/3", abs(cm2 - turn0 / (3 * math.tan(turn0))) < 1e-12 and cm2 < 1 / 3, f"{cm2:.4f}")
    fourth = 2 * turn0 / math.sin(2 * turn0)
    check("the fourth-order factor 2 turn_0/sin(2 turn_0) = 1.69 at the pair 2 and 3", f"{fourth:.2f}" == "1.69" and "1.69" in text, f"{fourth:.4f}")
    c_light = math.sqrt(1 / 3)
    va, vb = 0.10, 0.25
    k_ratio = (c_light - va) * (c_light + vb) / ((c_light - vb) * (c_light + va))
    u_count = c_light * (k_ratio - 1) / (k_ratio + 1)
    u_form = (vb - va) / (1 - va * vb / (c_light * c_light))
    check("the two-way reading u = (v_B - v_A)/(1 - v_A v_B/c^2) equals the count ratio's reading and stays below c", abs(u_count - u_form) < 1e-12 and abs(u_form) < c_light and abs((0.25 + 0.25) / (1 + 0.25 * 0.25 / (1 / 3))) < c_light, f"{u_form:.4f} at v_A = {va}, v_B = {vb}; two bodies at 0.25 each way read {(0.25 + 0.25) / (1 + 0.25 * 0.25 / (1 / 3)):.4f} < {c_light:.4f}")
    # (o) light near matter: c(n) = c (rate/q_0)^2 from light's integers at the content 600, the exponent 2 against the rate's 1, the frozen content (q_0/2) ln(2 q_0); the speed counted on a row of 4,000 Nodes with the paper's integers
    import numpy as np
    def light_row(content: int, ticks: int = 1500, row: int = 4000, start: float = 800.0, crest: float = 40.0, width: float = 60.0) -> tuple[float, float]:
        rate = round(GAMMA * (1 - 1 / GAMMA) ** content)
        pace = round(rate * rate / GAMMA)
        w_, r_, s_ = integers(1, 1, clock=rate, pace=pace)
        c_form = math.sqrt(r_ / w_)
        x = np.arange(row, dtype=float)
        kk = 2 * math.pi / crest
        pk = lambda t: np.rint(1e7 * np.exp(-((x - start - c_form * t) ** 2) / (2 * width ** 2)) * np.cos(kk * (x - start - c_form * t))).astype(np.int64)
        now, bef, rem = pk(0), pk(-1), np.zeros(row, dtype=np.int64)
        centre = lambda a_: float(((a_.astype(float) ** 2) * x).sum() / (a_.astype(float) ** 2).sum())
        c0 = centre(now)
        for _ in range(ticks):
            nb = np.zeros(row, dtype=np.int64)
            nb[1:] += now[:-1]
            nb[:-1] += now[1:]
            tot = r_ * nb + (s_ + 4 * r_) * now - w_ * bef + rem
            nxt = tot // w_
            rem = tot - w_ * nxt
            bef, now = now, nxt
        return c_form, (centre(now) - c0) / ticks
    c_form0, c_row0 = light_row(0)
    c_form6, c_row6 = light_row(600)
    rho2 = (1 - 1 / GAMMA) ** 1200
    check("light's speed at 600 units: c (rate/q_0)^2 = 0.819 c by the form, 0.818 c counted on a row, as printed in Section 4", abs(c_form6 / c_form0 - round(5429 * 5429 / GAMMA) / GAMMA) < 1e-3 and f"{c_form6 / c_form0:.3f}" == "0.819" and f"{c_row6 / c_row0:.3f}" == "0.818" and "0.818" in text and "0.819" in text, f"form {c_form6 / c_form0:.4f} (exact (1 - 1/q_0)^(2n) = {rho2:.4f}), row {c_row6 / c_row0:.4f}; empty-board row speed {c_row0:.4f} against {c_form0:.4f}")
    check("light's exponent 2n/q_0 against the rate's n/q_0: the ratio 2 : 1 exactly", abs(math.log(rho2) / math.log((1 - 1 / GAMMA) ** 600) - 2) < 1e-12, "2.0000")
    frozen = GAMMA / 2 * math.log(2 * GAMMA)
    n_pace0 = next(n_ for n_ in range(20000, 40000) if round(round(GAMMA * (1 - 1 / GAMMA) ** n_) ** 2 / GAMMA) == 0)
    half_up = lambda x_, y_: (2 * x_ + y_) // (2 * y_)  # x over y rounded half up, in whole numbers
    rate_exact = lambda n_: half_up(GAMMA * (GAMMA - 1) ** n_, GAMMA ** n_)
    reach_exact = lambda n_: half_up(rate_exact(n_) ** 2, GAMMA)
    n_reach0 = next(n_ for n_ in range(20000, 40000) if reach_exact(n_) == 0)
    check("the rule's rounding: the rate 5,429 and the reach 4,912 at 600 units are the exact fractions rounded half up once; the rate is within a half of q_0 (1 - 1/q_0)^n at every content tried", rate_exact(600) == 5429 and reach_exact(600) == 4912 and all(abs(rate_exact(n_) - GAMMA * (1 - 1 / GAMMA) ** n_) <= 0.5 for n_ in range(0, 30000, 97)) and "rounded half up once" in text, f"{rate_exact(600)}, {reach_exact(600)}")
    check("the reach rounds to zero once the rate falls below sqrt(q_0/2), near n = (q_0/2) ln(2 q_0)", abs(n_reach0 - frozen) < 60 and rate_exact(n_reach0) < math.sqrt(GAMMA / 2) <= rate_exact(n_reach0 - 1) and "below $\\sqrt{q_0/2}$" in source, f"the form {frozen:.0f}, the rounding {n_reach0} at the rate {rate_exact(n_reach0)}")
    # (p) the board's momentum P_a of equation (9) kept by the step on a periodic row of 24 Nodes: exactly in the rationals, within the floors' bound in whole numbers, with the program's own currents.momentum_terms
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
        from fractions import Fraction
        from event_universe.features.currents import momentum_terms
        from event_universe.core.ports import Wrap
        wrap, row_n = Wrap(True, False, False), 24
        p_of = lambda now_, bef_: momentum_terms(np.asarray(now_, dtype=object).reshape(row_n, 1, 1), np.asarray(bef_, dtype=object).reshape(row_n, 1, 1), 0, wrap, 1).sum(dtype=object)
        for num_, den_, label in ((1, 1, "light"), (2, 3, "matter")):
            w_, r_, s_ = integers(num_, den_)
            lam = ((s_ + 4 * r_) + 2 * r_ * math.cos(part)) / w_
            om = math.acos(lam / 2)
            now0 = [round(20 * math.cos(part * i_)) for i_ in range(row_n)]
            bef0 = [round(20 * math.cos(part * i_ + om)) for i_ in range(row_n)]
            a_, b_ = [Fraction(v) for v in now0], [Fraction(v) for v in bef0]
            p0 = p_of(a_, b_)
            exact = True
            for _ in range(200):
                a2 = [(r_ * (a_[i_ - 1] + a_[(i_ + 1) % row_n]) + (s_ + 4 * r_) * a_[i_] - w_ * b_[i_]) / w_ for i_ in range(row_n)]
                a_, b_ = a2, a_
                exact &= p_of(a_, b_) == p0
            a_, b_, rm = list(now0), list(bef0), [0] * row_n
            pv, within = p_of(a_, b_), True
            for _ in range(200):
                bound = 2 * sum(abs(a_[i_ - 1] - a_[(i_ + 1) % row_n]) for i_ in range(row_n))
                tot = [r_ * (a_[i_ - 1] + a_[(i_ + 1) % row_n]) + (s_ + 4 * r_) * a_[i_] - w_ * b_[i_] + rm[i_] for i_ in range(row_n)]
                a2 = [t_ // w_ for t_ in tot]
                rm = [t_ - w_ * q_ for t_, q_ in zip(tot, a2)]
                a_, b_ = a2, a_
                p2 = p_of(a_, b_)
                within &= abs(p2 - pv) <= bound
                pv = p2
            check(f"P_a of equation (9) kept by the step for {label} on a periodic row: exact in the rationals, within the floors' bound in whole numbers (200 ticks)", exact and within and p0 != 0, f"P_a = {p0}")
    except Exception as exc:  # the program's package not beside the paper
        check("P_a's conservation with the program's currents.momentum_terms (the package at ../../src)", False, str(exc)[:80])
    # (q) the tick's bound: a short pattern of light slows by (3 sum d_a^4 - 1)/24 p^2 (1/12 on an axis, 1/48 on a face diagonal, 0 on a body diagonal, 1/30 averaged), from cos(turn) = (sum_a cos(p d_a))/3; the closed forms 3 sqrt2 hbar c / E_QG2 and sqrt6 hbar / E_QG2 and the four numbers at E_QG2 = 6.3e10 GeV
    def slowing(d: tuple[float, float, float], p_: float = 0.02) -> float:
        turn_at = lambda q: math.acos(sum(math.cos(q * di) for di in d) / 3)
        v_ = (turn_at(p_ + 1e-6) - turn_at(p_ - 1e-6)) / 2e-6
        return (1 - v_ / math.sqrt(1 / 3)) / (p_ * p_)
    r3, r2 = 1 / math.sqrt(3), 1 / math.sqrt(2)
    coeff = lambda d: (3 * sum(di ** 4 for di in d) - 1) / 24
    dirs = {"axis": (1.0, 0.0, 0.0), "face diagonal": (r2, r2, 0.0), "body diagonal": (r3, r3, r3)}
    ok_dirs = all(abs(slowing(d) - coeff(d)) < 2e-4 for d in dirs.values()) and abs(coeff(dirs["axis"]) - 1 / 12) < 1e-12 and abs(coeff(dirs["face diagonal"]) - 1 / 48) < 1e-12 and abs(coeff(dirs["body diagonal"])) < 1e-12
    mean_d4 = 3 / 5  # <sum_a d_a^4> over the sphere: each <d_a^4> = 1/5
    check("a short pattern's slowing (3 sum d_a^4 - 1)/24 p^2: 1/12 axis, 1/48 face diagonal, 0 body diagonal, 1/30 averaged", ok_dirs and abs((3 * mean_d4 - 1) / 24 - 1 / 30) < 1e-12 and "p^2}{12}" in source and "p^2/48" in source and "1/30" in text, ", ".join(f"{k} {slowing(d):.5f}" for k, d in dirs.items()))
    hbar_c, hbar, e_qg, e_tev = 1.97327e-16, 6.58212e-25, 6.3e10, 1000.0  # GeV m, GeV s, GeV, GeV
    bound_dv = 1.5 * (e_tev / e_qg) ** 2
    lam = 2 * math.pi * hbar_c / e_tev
    step_axis = 3 * math.sqrt(2) * hbar_c / e_qg
    tick_axis = math.sqrt(6) * hbar / e_qg
    p_axis = math.sqrt(12 * bound_dv)
    check("the measured bound |dv/v| = (3/2)(E/E_QG2)^2 = 3.8e-16 at 1 TeV, the wavelength 1.24e-18 m", f"{bound_dv:.1e}" == "3.8e-16" and f"{lam:.2e}" == "1.24e-18" and "3.8 \\times 10^{-16}" in source and "1.24 \\times 10^{-18}" in source, f"{bound_dv:.2e}, {lam:.3e} m")
    check("the second burst's bound 1.3e11 GeV halves the lengths (the ratio 2.1); the third, 6.9e11 GeV, is eleven times the first and gives 2e-36 s on an axis", 1.9 < 1.3e11 / e_qg < 2.2 and "1.3 \\times 10^{11}" in source and 10.5 < 6.9e11 / e_qg < 11.5 and f"{math.sqrt(6) * hbar / 6.9e11:.0e}" == "2e-36" and "6.9 \\times 10^{11}" in source and "2 \\times 10^{-36}" in source, f"{1.3e11 / e_qg:.2f}, {6.9e11 / e_qg:.2f}, {math.sqrt(6) * hbar / 6.9e11:.2e} s")
    # the three bursts on the sky (GRB 090510, GRB 190114C, GRB 221009A, right ascension and declination in degrees): their separations, and that no turn of the board puts all three within five degrees of its body diagonals, two of which are 70.5 or 109.5 degrees apart
    sky = {"090510": (333.55, -26.58), "190114C": (54.51, -26.95), "221009A": (288.26, 19.77)}
    def apart(a_, b_):
        ra1, d1 = math.radians(sky[a_][0]), math.radians(sky[a_][1])
        ra2, d2 = math.radians(sky[b_][0]), math.radians(sky[b_][1])
        return math.degrees(math.acos(max(-1.0, min(1.0, math.sin(d1) * math.sin(d2) + math.cos(d1) * math.cos(d2) * math.cos(ra1 - ra2)))))
    seps = [apart("090510", "190114C"), apart("090510", "221009A"), apart("190114C", "221009A")]
    diag = math.degrees(math.acos(1 / 3))  # 70.53 degrees between two body diagonals' directions, else 109.47 or 180
    allowed = (0.0, diag, 180 - diag, 180.0)
    hidden_all = all(min(abs(s_ - a_) for a_ in allowed) <= 10 for s_ in seps)  # two directions each within 5 degrees of a diagonal are within 10 degrees of an allowed angle
    check("the three bursts 64 to 130 degrees apart on the sky; no turn of the board hides all three within five degrees of its body diagonals", 60 < min(seps) < 66 and 125 < max(seps) < 135 and not hidden_all and "64^\\circ" in source and "71^\\circ" in source and "130^\\circ" in source and "180^\\circ" in source, ", ".join(f"{s_:.0f}" for s_ in seps) + " degrees")
    # the direction: the slowing's coefficient at a given angle from a body diagonal, the smallest over the directions at that angle; the bound on the distance and the tick weakens by the square root of 1/12 over it
    def coef_at(deg: float) -> float:
        nrm = (r3, r3, r3)
        u_ = (r2, -r2, 0.0)
        v_ = (1 / math.sqrt(6), 1 / math.sqrt(6), -2 / math.sqrt(6))
        th = math.radians(deg)
        best = None
        for k_ in range(3600):
            ph = 2 * math.pi * k_ / 3600
            d_ = tuple(math.cos(th) * nrm[i_] + math.sin(th) * (math.cos(ph) * u_[i_] + math.sin(ph) * v_[i_]) for i_ in range(3))
            c_ = coeff(d_)
            best = c_ if best is None else min(best, c_)
        return best
    factor5, factor1 = math.sqrt((1 / 12) / coef_at(5.0)), math.sqrt((1 / 12) / coef_at(1.0))
    step_5, tick_5 = step_axis * factor5, tick_axis * factor5
    check("the distance between Nodes below 3 sqrt2 hbar c/E_QG2 = 1.3e-26 m on an axis (p lambda / 2 pi agrees), below 1.1e-25 m (to rounding) more than five degrees from a body diagonal (the bound eightfold weaker at 5 degrees, fortyfold at 1 degree)", abs(p_axis * lam / (2 * math.pi) - step_axis) < 1e-30 and f"{step_axis:.1e}" == "1.3e-26" and abs(step_5 - 1.1e-25) < 0.05 * 1.1e-25 and 7.5 < factor5 < 8.5 and 35 < factor1 < 45 and "1.3 \\times 10^{-26}" in source and "1.1 \\times 10^{-25}" in source and "eightfold" in text and "fortyfold" in text, f"{step_axis:.2e} m, {step_5:.2e} m; factors {factor5:.2f}, {factor1:.1f}")
    check("the tick below sqrt6 hbar/E_QG2 = 2.6e-35 s on an axis (light at 1/sqrt3 of the distance per tick), below 2.2e-34 s more than five degrees from a body diagonal, about 2e-34 in the Conclusion", abs(step_axis / (math.sqrt(3) * 2.99792458e8) - tick_axis) < 1e-40 and f"{tick_axis:.1e}" == "2.6e-35" and 2.2e-34 >= tick_5 > 0.9 * 2.2e-34 and "2.6 \\times 10^{-35}" in source and "2.2 \\times 10^{-34}" in source and "2 \\times 10^{-34}" in source and "10^{-25}" in source, f"{tick_axis:.2e} s, {tick_5:.2e} s")
    # (r) the bound reaching back to the clocks at the printed tick 2.2e-34 s: the electron's rest rate m c^2/h = 1.24e20 per second (the inner clock), turn_0 = 2 pi nu tau under 1.8e-13, 1 - cos = turn_0^2/2 within 2e-26, s - 1 = turn_0^2/12 within 3e-27, 1/3 - c_m^2 = turn_0^2/9 within 4e-27, the bottom above 1/(1 - cos) = 6e25, the proton 1,836 times faster within 6e-20, 1e-20 and 2e-20 (the series' coefficients checked at a small turn)
    nu_e = 0.51099895e-3 / (2 * math.pi * hbar)  # GeV over GeV s: the rest rate, swings per second
    turn_e = 2 * math.pi * 1.24e20 * 2.2e-34
    turn_p = turn_e * 1836
    small = 1e-3
    series_s = (2 * math.tan(small / 2) / small - 1) / small ** 2
    series_cm = (1 / 3 - small / (3 * math.tan(small))) / small ** 2
    ok_e = turn_e < 1.8e-13 and turn_e ** 2 / 2 < 2e-26 and turn_e ** 2 * series_s < 3e-27 and turn_e ** 2 * series_cm < 4e-27 and 1 / (turn_e ** 2 / 2) > 6e25
    ok_p = turn_p ** 2 / 2 < 6e-20 and turn_p ** 2 * series_s < 1e-20 and turn_p ** 2 * series_cm < 2e-20 and abs(1836 - 938.272 / 0.51099895) < 1
    printed = all(s_ in source for s_ in ("1.24 \\times 10^{20}", "1.8 \\times 10^{-13}", "2 \\times 10^{-26}", "3 \\times 10^{-27}", "4 \\times 10^{-27}", "6 \\times 10^{25}", "6 \\times 10^{-20}", "2 \\times 10^{-20}", "1,836"))
    # the clocks by kind at the printed tick: s - 1 = turn_0^2/12 for a body swinging at its rest rate m c^2/h, the electron, the proton, the iron nucleus of the measured shift (Fe-57) and a caesium atom; every atom up to the heaviest (U-238) within 5e-16; a single pattern heavier than h/(4 c^2 tau) turns past a quarter swing per tick
    def s_minus_1(mass_mev: float) -> float:
        turn = 2 * math.pi * (mass_mev * 1e-3 / (2 * math.pi * hbar)) * 2.2e-34
        return turn ** 2 / 12
    u_mev = 931.49410242
    kinds = {"electron": 0.51099895, "proton": 938.27208816, "iron nucleus": 56.9353928 * u_mev, "caesium atom": 132.905452 * u_mev, "uranium atom": 238.050788 * u_mev}
    s1 = {k_: s_minus_1(m_) for k_, m_ in kinds.items()}
    mass_limit = 6.62607015e-34 / (4 * 2.99792458e8 ** 2 * 2.2e-34)
    turn_u = math.sqrt(12 * s1["uranium atom"])
    check("the clocks by kind: s - 1 = turn_0^2/12 within 3e-27 (electron), 1e-20 (proton), 3e-17 (iron nucleus), 2e-16 (caesium), 5e-16 (uranium, 238 u); at uranium's rate c_m within turn_0^2/6 < 1e-15 of c and the moving coefficient within turn_0^2/3 < 2e-15, four times s - 1; a single pattern above about 1e-17 kg past a quarter swing", s1["electron"] < 3e-27 and s1["proton"] < 1e-20 and 2e-17 < s1["iron nucleus"] < 3e-17 and 1e-16 < s1["caesium atom"] < 2e-16 and 4e-16 < s1["uranium atom"] < 5e-16 and turn_u ** 2 / 6 < 1e-15 and turn_u ** 2 / 3 < 2e-15 and 5e-18 < mass_limit < 1e-17 and all(s_ in source for s_ in ("5 \\times 10^{-16}", "3 \\times 10^{-17}", "2 \\times 10^{-16}", "10^{-17}", "2 \\times 10^{-15}", "10^{-15}")), ", ".join(f"{k_} {v_:.1e}" for k_, v_ in s1.items()) + f"; uranium turn_0 {turn_u:.1e}, c_m {turn_u ** 2 / 6:.1e}, the coefficient {turn_u ** 2 / 3:.1e}; the mass limit {mass_limit:.1e} kg")
    check("the electron's rest rate 1.24e20 per second; at the tick 2.2e-34 s turn_0 < 1.8e-13, 1 - cos within 2e-26, s within 3e-27 of 1, c_m^2 within 4e-27 of 1/3, the bottom above 6e25; the proton within 6e-20, 1e-20 and 2e-20", f"{nu_e:.2e}" == "1.24e+20" and abs(series_s - 1 / 12) < 1e-4 and abs(series_cm - 1 / 9) < 1e-4 and ok_e and ok_p and printed, f"nu {nu_e:.3e}, turn_0 {turn_e:.2e}, 1 - cos {turn_e ** 2 / 2:.2e}, s - 1 {turn_e ** 2 * series_s:.1e}, 1/3 - c_m^2 {turn_e ** 2 * series_cm:.1e}, bottom > {1 / (turn_e ** 2 / 2):.1e}; proton {turn_p ** 2 / 2:.1e}, {turn_p ** 2 * series_s:.1e}, {turn_p ** 2 * series_cm:.1e}")
    # (l) the wiping's ball counted in steps: the layer 4t^2 + 2, N(t) = (4t^3 + 6t^2 + 8t + 3)/3, the full tube 2L^2
    layer = lambda t: 1 if t == 0 else 4 * t * t + 2
    ball = lambda t: sum(layer(k) for k in range(t + 1))
    closed = lambda t: (4 * t ** 3 + 6 * t ** 2 + 8 * t + 3) // 3
    brute = lambda t: sum(1 for x in range(-t, t + 1) for y in range(-t, t + 1) for z in range(-t, t + 1) if abs(x) + abs(y) + abs(z) <= t)
    check("the layer at t steps holds 4t^2 + 2 Nodes and the ball N(t) = (4t^3 + 6t^2 + 8t + 3)/3: 1, 7, 25, 63, 129", all(ball(t) == closed(t) == brute(t) and (4 * t ** 3 + 6 * t ** 2 + 8 * t + 3) % 3 == 0 for t in range(8)) and [closed(t) for t in range(5)] == [1, 7, 25, 63, 129] and "4t^3 + 6t^2 + 8t + 3" in source and "4t^2 + 2" in source and "1,\\ 7,\\ 25,\\ 63,\\ 129" in source, str([closed(t) for t in range(5)]))
    # (f) the shares of the report
    clocks_file = Path(__file__).resolve().parent.parent / "run_clocks.json"
    if clocks_file.exists():
        rc = json.load(open(clocks_file))
        rest0, rest6 = rc["rest"]["content_0"]["swings"], rc["rest"]["content_600"]["swings"]
        mv, rs = rc["moving"]["swings_moving"], rc["moving"]["swings_rest"]
        check("on the board at rest: 722.5 / 803.0 swings -> 0.900 as printed", (rest6, rest0) == (722.5, 803.0) and f"{rest6 / rest0:.3f}" == "0.900" and "722.5" in text and "803.0" in text, f"{rest6} / {rest0} = {rest6 / rest0:.4f}")
        check("on the board moving: 147.5 / 160.5 swings -> 0.92 as printed, the middle at 0.197 Node per tick", (mv, rs) == (147.5, 160.5) and f"{mv / rs:.2f}" == "0.92" and "147.5" in text and "160.5" in text and re.search(r"0\.92\b(?!\d)", text) and abs(rc["moving"]["middle_speed"] - speed) < 0.001, f"{mv} / {rs} = {mv / rs:.4f}; speed {rc['moving']['middle_speed']}")
        lt = rc.get("light")
        check("the light row in run_clocks.json: 0.818 counted against 0.819 by the form, as here", lt is not None and lt["ratio_counted"] == 0.818 and lt["ratio_form"] == 0.819 and abs(lt["content_600"]["speed_counted"] / lt["content_0"]["speed_counted"] - c_row6 / c_row0) < 1e-3, f"{lt and lt['ratio_counted']} counted, {lt and lt['ratio_form']} form")
    else:
        check("run_clocks.json present (tools/run_clocks.py writes it)", False)
    # (f) the shares of the report
    rep_file = run_dir / "report_e4.json"
    if rep_file.exists():
        rep = json.load(open(rep_file))
        closes = rep["iv_two_detectors"]["c_closes"]
        s48 = [closes["48"]["shares"][k]["share_over_unit"][0] for k in ("body 0", "body 1")]
        s96 = [closes["96"]["shares"][k]["share_over_unit"][0] for k in ("body 0", "body 1")]
        no_click = 1 - sum(s48)
        chance = s96[1] / sum(s96)
        chance_printed = round(s96[1], 3) / (round(s96[0], 3) + round(s96[1], 3))
        check("0.811 = 1 - 0.080 - 0.109 at tick 48", f"{no_click:.3f}" == "0.811" and "0.811" in text, f"{no_click:.4f}")
        check("0.558 = 0.678 / (0.536 + 0.678), printed 0.56", f"{chance_printed:.3f}" == "0.558" and f"{chance:.2f}" == "0.56" and "0.56" in text, f"{chance:.4f} (from the printed shares {chance_printed:.4f})")
        # (m) the toss's numbers at the two closes from the formulas W_0 = max(min(U, 1) - sum W, 0), P_i = W_i / (W_0 + sum W)
        u48 = max(min(1.0, 1) - sum(s48), 0)
        u96 = max(min(u48, 1) - sum(s96), 0)
        check("W_0 at the first close = 0.811, at the second 0 (the weights exceed what is left), P = 0.558", f"{u48:.3f}" == "0.811" and u96 == 0 and abs(s96[1] / (u96 + sum(s96)) - 0.5585) < 0.001, f"{u48:.4f}, {u96}, {s96[1] / (u96 + sum(s96)):.4f}")
        # (g) the counts
        shells = [row[2] for row in rep["a_erased_nodes_per_shell"]]
        L = rep["world"]["shape"][1]
        taker = rep["iv_two_detectors"]["hole_nodes_file_coordinates"][0]
        tube = []
        for t in range(1, 12):
            n = 0
            for y in range(L):
                for z in range(L):
                    d = abs(y - taker[1]) + abs(z - taker[2])
                    n += 2 if d < t else (1 if d == t else 0)
            tube.append(n)
        check(f"the tube's layers from the taker at ({taker[1]}, {taker[2]}) in a width of {L}: 6, 18, 38, 64, 90, 110, 122, 127, 128 then 2L^2 = {2 * L * L}", tube[:9] == shells[:9] and tube[9] == 2 * L * L == shells[9] and "2L^2" in source and ", ".join(str(x) for x in shells[:9]) in text, str(tube[:10]))
        wiped = rep["a_erased_nodes_total_to_end"]
        named = rep["b_faces"]["count"]
        written = rep["b_faces"]["count_keyed_to_%d" % rep["world"]["intervals"]]
        check("9,279 = the sum of the shells", sum(shells) == wiped == 9279 and shells[:9] == [6, 18, 38, 64, 90, 110, 122, 127, 128] and all(v == 128 for v in shells[9:]), f"{len(shells)} shells, {fmt(sum(shells))}")
        check("18,560 = 2 x 9,279 + 2", named == 2 * wiped + 2 == 18560 and "18560" in text_n, fmt(named))
        check("18,176 = 18,560 - 256 - 128, the 384 named and not yet written", written == named - 256 - 128 == 18176 and named - written == 384 and "18176" in text_n and "384 named" in text, fmt(written))
        # (t) the momentum at the click: the quarter turn 9,424 = floor(q_0 pi/2) acts of the angle 1/q_0, the twist; the taker carried 31,560 of the piece's 33,812 along the board, 2,252 left (run_momentum.json, read on the board by tools/run_momentum.py)
        mom_file = Path(__file__).resolve().parent.parent / "run_momentum.json"
        if mom_file.exists():
            rm = json.load(open(mom_file))
            q0 = rm["q_0"]
            check("the quarter turn: 9,424 acts of 1/q_0 is the largest count under pi/2, the twist along the board", rm["quarter_turn_acts"] == math.floor(q0 * math.pi / 2) == rm["twist"][0] == 9424 and rm["piece_momentum_read_at_the_taker"] == rep["iv_two_detectors"]["credit_lines"][0]["momentum"] and "9,424" in source, f"{rm['quarter_turn_acts']} against {q0 * math.pi / 2:.2f}")
            light_sum = rm["light_along_board"]
            check("equation (5) over the board: the light 3,480 at tick 0, 4,280 at tick 96 (the credit line's fan), -26,406 at tick 120 and -46,774 at the end with the click, 872 at the end without; the taker's two lines 15,780 each; light and atoms together -14,842 at the end", light_sum["0"] == 3480 and light_sum["96"] == 4280 == rm["fan"][0] and light_sum["120"] == -26406 and light_sum["172"] == -46774 and rm["twin_light_along_board"]["172"] == 872 and sorted(rm["taker_lines_along_board"]) == [0, 0, 15780, 15780] and rm["light_and_atoms_along_board_at_end"] == -14842 and all(s_ in source for s_ in ("4,280", "3,480", "872", "26{,}406", "46{,}774", "14{,}842")), f"{light_sum}, twin {rm['twin_light_along_board']}, atoms {rm['atoms_along_board']}, together {rm['light_and_atoms_along_board_at_end']}")
            hv = rm["halves_alone_along_board"]
            tk, ot = hv[rm["taken_half"]], hv[[k_ for k_ in hv if k_ != rm["taken_half"]][0]]
            check("each half alone: the taken half 37,952 at the start and 39,272 at tick 96, the other -36,640 and -38,584; the taker's 31,560 0.80 of its half's; light and taker 5,154 at tick 120 against 2,936 without a click, within 2,218; the references' scale 2^12", tk["0"] == 37952 and tk["96"] == 39272 and ot["0"] == -36640 and ot["96"] == -38584 and 0.78 < rm["taker_along_board"] / tk["96"] < 0.82 and rm["light_and_taker_at_120"] == 5154 == light_sum["120"] + rm["taker_along_board"] and rm["twin_light_along_board"]["120"] == 2936 and rm["light_and_taker_at_120"] - rm["twin_light_along_board"]["120"] == 2218 and rm["reference_scale"] == 4096 and all(s_ in source for s_ in ("39,272", "37,952", "38{,}584", "36{,}640", "5,154", "2,936", "2,218", "4{,}096", "0.80 of")), f"{tk}, {ot}, the taker {rm['taker_along_board'] / tk['96']:.3f} of its half; {rm['light_and_taker_at_120']} against {rm['twin_light_along_board']['120']}; scale {rm['reference_scale']}")
            lin = rm["linear_form_along_board"]
            cross = rm["cross_terms_at_start"]
            check("the linear form keeps equation (5): 3,480 on the whole board and 37,952 / -36,640 for the halves at ticks 0, 48 and 96; the halves' cross terms 2,168 (3,480 less their sum 1,312); the gap at tick 96, 3,592, is the cross terms plus about 1,400 of the remainder's drift (+800, +1,320, -1,944 on the three boards); the taker 0.80 of its half, the two-Node reading 0.86 of it; the whole light -1,124 and 0 across the tube", all(abs(v_ - 3480) < 0.5 for v_ in lin["both"].values()) and all(abs(v_ - tk["0"]) < 0.5 for v_ in lin["half 0"].values()) and all(abs(v_ - ot["0"]) < 0.5 for v_ in lin["half 1"].values()) and cross == 3480 - 37952 + 36640 == 2168 and tk["0"] + ot["0"] == 1312 and rm["gap_at_click_tick"] == 3592 and abs(rm["gap_at_click_tick"] - cross - 1400) < 60 and (4280 - 3480, 39272 - 37952, -38584 + 36640) == (800, 1320, -1944) and f"{rm['taker_along_board'] / tk['96']:.2f}" == "0.80" and f"{abs(rm['piece_momentum_read_at_the_taker'][0]) / tk['96']:.2f}" == "0.86" and rm["fan"][1:] == [-1124, 0] and all(s_ in source for s_ in ("2,168", "1,400", "1,312", "0.80 of", "0.86 of", "1{,}124")), f"linear {lin}; cross {cross}; gap {rm['gap_at_click_tick']}")
            check("31,560 carried of the piece's 33,812 along the board, 2,252 left", rm["gained_along_board"] == 31560 and rm["short_of_the_piece"] == abs(rm["piece_momentum_read_at_the_taker"][0]) - rm["gained_along_board"] == 2252 and rm["gained_along_board"] < abs(rm["piece_momentum_read_at_the_taker"][0]) and "31,560" in source and "2,252" in source and "34,349" in source and "13,418" in source, f"{rm['gained_along_board']} of {rm['piece_momentum_read_at_the_taker'][0]}, {rm['short_of_the_piece']} left; across {rm['piece_momentum_read_at_the_taker'][1:]}")
        else:
            check("run_momentum.json present (tools/run_momentum.py writes it)", False)
        # (u) the ensemble over seeds (run3d_fixed/ensemble/summary.json): the frequencies as counts over 400 with the binomial uncertainty, equation (3) chained over the closes from the weights read, the far share at tick 96, the two weights at tick 96 against what was left, light's 83 ticks across 48 Nodes
        ens_file = run_dir / "ensemble" / "summary.json"
        if ens_file.exists():
            es = json.load(open(ens_file))["summary"]
            both, ea, eb = es["both"], es["A"], es["B"]
            n_ = both["seeds"]
            binom = lambda k_: (k_ / n_, math.sqrt(k_ / n_ * (1 - k_ / n_) / n_))
            fa, fb = binom(both["A_clicks"]), binom(both["B_clicks"])
            check("both present: 174 and 226 of 400, 0.435 +- 0.025 and 0.565 +- 0.025, no run with two clicks or none", both["A_clicks"] == 174 and both["B_clicks"] == 226 and n_ == 400 and f"{fa[0]:.3f}" == "0.435" and f"{fb[0]:.3f}" == "0.565" and f"{fa[1]:.3f}" == "0.025" and both["two_clicks_in_one_run"] == 0 and both["no_click"] == 0, f"{fa[0]:.4f} +- {fa[1]:.4f}, {fb[0]:.4f} +- {fb[1]:.4f}")
            def chained(weights: dict, names: tuple) -> dict:
                U, alive, p = 1.0, 1.0, {k_: 0.0 for k_ in names}
                for t_ in sorted(weights, key=int):
                    w_ = weights[t_]
                    s_ = sum(w_.values())
                    w0 = max(min(U, 1.0) - s_, 0.0)
                    for k_ in w_:
                        p[k_] += alive * w_[k_] / (w0 + s_)
                    alive *= w0 / (w0 + s_)
                    U -= s_
                return p
            pb = chained(both["prediction_from_the_weights"]["weights_read"], ("A", "B"))
            pa_alone = chained(ea["prediction_from_the_weights"]["weights_read"], ("A",))
            pb_alone = chained(eb["prediction_from_the_weights"]["weights_read"], ("B",))
            check("equation (3) chained over the closes: 0.438 and 0.562 with both, 0.658 alone near, 0.812 alone far", f"{pb['A']:.3f}" == "0.438" and f"{pb['B']:.3f}" == "0.562" and f"{pa_alone['A']:.3f}" == "0.658" and f"{pb_alone['B']:.3f}" == "0.812", f"{pb['A']:.4f}, {pb['B']:.4f}; {pa_alone['A']:.4f}; {pb_alone['B']:.4f}")
            at96 = both["clicks_by_detector_and_tick"]
            w96 = both["prediction_from_the_weights"]["weights_read"]["96"]
            check("at tick 96: 182 of 324 clicks the far detector's, 0.562; the weights 0.536 + 0.678 = 1.21 above the 0.81 left, so W_0 = 0", at96["B at 96"] == 182 and at96["A at 96"] + at96["B at 96"] == 324 and f"{182 / 324:.3f}" == "0.562" and f"{sum(w96.values()):.2f}" == "1.21" and f"{1 - sum(both['prediction_from_the_weights']['weights_read']['48'].values()):.2f}" == "0.81" and sum(w96.values()) > 1 - sum(both['prediction_from_the_weights']['weights_read']['48'].values()), f"{at96}, {sum(w96.values()):.4f}")
            fa1, fb1 = (ea["A_clicks"] / ea["seeds"], math.sqrt(ea["A_clicks"] / ea["seeds"] * (1 - ea["A_clicks"] / ea["seeds"]) / ea["seeds"])), (eb["B_clicks"] / eb["seeds"], math.sqrt(eb["B_clicks"] / eb["seeds"] * (1 - eb["B_clicks"] / eb["seeds"]) / eb["seeds"]))
            check("alone: the far detector 326 of 400, 0.815 +- 0.019; the near 263 of 400, 0.658 +- 0.024", eb["B_clicks"] == 326 and ea["A_clicks"] == 263 and f"{fb1[0]:.3f}" == "0.815" and f"{fb1[1]:.3f}" == "0.019" and abs(fa1[0] - 0.658) < 0.00051 and f"{fa1[1]:.3f}" == "0.024", f"{fb1[0]:.4f} +- {fb1[1]:.4f}; {fa1[0]:.4f} +- {fa1[1]:.4f}")
            dets = rep["iv_two_detectors"]["takers"]
            apart = abs(dets[1][0][0] - dets[0][0][0])
            check("the detectors 48 Nodes apart, which light at 0.577 Node per tick crosses in 83 ticks", apart == 48 and round(apart / math.sqrt(1 / 3)) == 83 and "83 ticks" in text, f"{apart} Nodes, {apart / math.sqrt(1 / 3):.1f} ticks")
        else:
            check("run3d_fixed/ensemble/summary.json present", False)
        # (s) the stretch after the click: the other detector's weight 0.039 at tick 144 and no toss, the count 0; at the run's end the light's other half with its crest at Node 119 (the profile at the last tick), the ball's edge at Node 148 = taker - (last tick - click tick - 1), reached into its tail, most of it outside
        close3 = closes["144"]
        w144 = close3["shares"]["body 0"]["share_over_unit"][0]
        check("the other detector's weight 0.039 at tick 144, no toss (the count 0)", f"{w144:.3f}" == "0.039" and close3["shares"]["body 0"]["counts"] == [1, 0] and close3["shares"]["no_click_weight_over_unit_as_engine"] == "no draw: the count is 0" and "0.039 at tick 144" in text, f"{w144:.6f}, {close3['shares']['no_click_weight_over_unit_as_engine']}")
        last = rep["world"]["intervals"]
        prof = rep["e_motion_0_to_48"]["profiles"][str(last)]
        click_tick = rep["iv_two_detectors"]["click_tick"]
        edge = taker[0] - (last - click_tick - 1)
        fig = run_dir / "figure_data.json"
        edge_data = json.load(open(fig))["i_erased_set_after_click"][-1] if fig.exists() else [last, [edge]]
        check("at the run's end the light's other half: crest at Node 119, the ball's edge at Node 148, the tail inside, most outside", prof["peak_minus_x"][0] == 119 and edge == 148 and edge_data[0] == last and edge_data[1][0] == edge and prof["x_min"] < edge <= prof["x_max"] and edge - prof["x_min"] > prof["x_max"] - edge and "crest at Node 119" in text and "edge at Node 148" in text, f"crest {prof['peak_minus_x'][0]}, the half over {prof['x_min']}..{prof['x_max']}, edge {edge}")
    else:
        problems.append("no report_e4.json in " + str(run_dir))
        print("MISMATCH no report to read the shares and the counts from")
    if problems:
        print("the formulas FAIL: " + ", ".join(problems))
        return 1
    print("the formulas pass")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
