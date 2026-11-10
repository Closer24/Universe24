"""TC.19 (pre-registration 10): F7 with the front on the round-cone headroom light, time-difference source,
amplitude below Bob's clock, one-shot Bob via the verified arc law; no full history kept (memory)."""
from __future__ import annotations

import itertools
import math
from collections import defaultdict
from fractions import Fraction as Fr

from ...core import Engine, check_reciprocity, compose
from ...layers.choice_round import build_f7_round, round_gamma
from ...observe.choice import quotient, values
from ...prepare.choice import Prep, ring_b, ring_state, yz_lines


def exp_f7_round(A, d=5, steps=50, L=32, rho0=0.9, settings=range(6)):
    Q = -(-8 * A * A // 6)
    if Q % 2 == 0:
        Q += 1
    D = 6 * Q
    gamma = round_gamma(Q, rho0)
    base, extra = build_f7_round(Q=Q, kappa=1, gamma=gamma)
    T = compose(base, extra)
    rep = check_reciprocity(T)
    eng = Engine(T, Q)
    xA, xB, tA = 2, 2 + d, 1
    allyz = yz_lines(L, L * L)
    num, den = defaultdict(Fr), defaultdict(Fr)
    rew = True
    for a in settings:
        Cs = ring_b(A, a, tA)
        wts = {}
        for phi in range(6):
            ph = ring_b(A, phi)
            X = sum(p * c for p, c in zip(ph, Cs))
            n2 = sum(p * p for p in ph)
            wts[phi] = (Fr(min(max(2 * (n2 + X), 0), D), D), Fr(min(max(2 * (n2 - X), 0), D), D))
        phi_rep = (a + tA + 1) % 6
        for q, lamA in ((1, D - 1), (-1, 0)):
            pr = Prep(T, Q, L, base, extra)
            nA = pr.nodes_x(xA, allyz)
            c = ring_b(A, phi_rep)
            for j in range(3):
                pr.set(f"f7.PH{j}", pr.nodes_x(xA + 1, allyz), b=c[j])
                pr.set(f"f7.PH{j}", pr.nodes_x(xA + 2, allyz), a=c[j])
            pr.set("f7.PG", pr.nodes_x(xA + 1, allyz), b=1)
            pr.set("f7.PG", pr.nodes_x(xA + 2, allyz), a=1)
            for j, (aa, bb) in enumerate(ring_state(A, a)):
                pr.set(f"f7.C{j}", nA, a=aa, b=bb)
            pr.set("f7.dAp", nA, r=lamA)
            pr.set("f7.dAm", nA, r=lamA)
            s0 = pr.state()
            nB0 = pr.node(xB, 0, 0)
            gP = [T.gear_index(f"f7.P{j}") for j in range(3)]
            st = s0
            for t in range(steps + 1):
                if t == tA + 1:
                    qa = set((quotient(T, prev, st, "f7.dAp", nA) + quotient(T, prev, st, "f7.dAm", nA)).tolist())
                    if qa != {q}:
                        raise AssertionError("representative token did not give q")
                P = [int(st.b[g][nB0]) for g in gP]
                for b in settings:
                    Bv = ring_b(A, b, t)
                    X = sum(x * y for x, y in zip(Bv, P))
                    n2 = sum(x * x for x in Bv)
                    Pp, Pm = Fr(min(max(2 * (n2 + X), 0), D), D), Fr(min(max(2 * (n2 - X), 0), D), D)
                    for phi in range(6):
                        w = wts[phi][0] if q == 1 else wts[phi][1]
                        num[(a, b, t)] += w * q * (Pp - Pm)
                        den[(a, b, t)] += w * (Pp + Pm)
                if t < steps:
                    prev, st = st, eng.step(st)
            rew &= eng.rewind(st, steps).same_as(s0)
    cosk = 1 - 3 * Q / (2 * (Q - 1))
    theta_cw = (-90 - math.degrees(math.acos(cosk)) * d + 60) % 360
    out = {"A": A, "Q": Q, "odd": Q % 2 == 1, "D": D, "gamma": gamma, "rho0": rho0, "theta_CW_pred_deg": round(theta_cw, 2),
           "round_first_snapshot": tA + 1 + d * math.sqrt(3 * Q / (Q - 1)), "per_tB": {}, "rewind_all_runs": rew,
           "recip_ok": rep.ok, "designated": len(rep.designated)}
    for t in range(steps + 1):
        Et = {(a, b): (num[(a, b, t)] / den[(a, b, t)]) if den[(a, b, t)] else Fr(0) for a in settings for b in settings}
        S = max(abs(Et[(a, b)] + Et[(a, b2)] + Et[(a2, b)] - Et[(a2, b2)])
                for a, a2, b, b2 in itertools.product(settings, repeat=4))
        cs = sum(float(Et[(a, b)]) * math.cos(math.radians(60 * (a - b))) for a in settings for b in settings)
        sn = sum(float(Et[(a, b)]) * math.sin(math.radians(60 * (a - b))) for a in settings for b in settings)
        rho = 2 * math.hypot(cs, sn) / 36
        theta = math.degrees(math.atan2(-sn, cs)) % 360
        resid = max(abs(float(Et[(a, b)]) - rho * math.cos(math.radians(60 * (a - b) + theta)))
                    for a in settings for b in settings)
        out["per_tB"][str(t)] = {"maxS": round(float(S), 6), "max|E|": round(max(abs(float(v)) for v in Et.values()), 6),
                                 "rho": round(rho, 4), "theta_deg": round(theta, 2), "fit_resid": round(resid, 5),
                                 "E": {f"{a},{b}": str(v) for (a, b), v in Et.items()} if t in (40, 45) else None}
    return out
