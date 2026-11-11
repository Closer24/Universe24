"""CHIRAL candidate demo (declared candidate, DEFAULT OFF): clicks of the chiral block.
(a) J+ readout: the J-pure R*-fixed seed (prepare/chiral.jpure_seed) and its plain time-mirror image (Mp: the J- copy);
    the click-space J-Wronskian W_J (observe/chiral.py) per update, and the exact J-number N_J.
(b) Click-level CP: official click records of a weak-half packet run vs its CP-image run and its P-image run; the CP
    image's record equals the CP-map of the original record (kinds swapped exactly on negated gears), the P image's does
    not.
Run (repo root, one core): OMP_NUM_THREADS=1 nice -n 19 python -m universe24.demos.chiral.demo_summary
Writes runs/demos/chiral/DEMO_summary.json.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from ...core.engine import Engine, State
from ...core.reversors import GearwiseMap
from ...layers.chiral import Q_DEFAULT, chiral_algebra
from ...observe.chiral import ChiralView
from ...prepare import vacuum_state
from ...prepare.chiral import chiral_system, gear_groups, jpure_seed, standard_maps

OUT = Path("runs/demos/chiral")


def stamp():
    return datetime.now(timezone.utc).strftime("%a %b %d %H:%M:%S UTC %Y")


def click_record(E, s, T):
    out = []
    for t in range(T):
        s1 = E.step(s)
        c = E.clicks(s, s1, step=t, stream="official")
        out.append(c)
        s = s1
    return out, s


def main():
    Q, L = Q_DEFAULT, 6
    T, blocks = chiral_system(Q)
    E = Engine(T, Q)
    view = ChiralView(T, blocks[3], blocks[2])
    res = {"started": stamp(), "Q": Q, "L": L}
    # (a) J+ readout
    seed, rep = jpure_seed(T, blocks, Q, L, A=1 << 12)
    mirror = GearwiseMap(T, Q, default="Mp")(seed)          # the plain time mirror: J- copy of the same data
    rows = {}
    for nm, s0 in (("J+ seed", seed), ("J- image (Mp)", mirror)):
        hist = [s0]
        for _ in range(7):
            hist.append(E.step(hist[-1]))
        wj = [view.click_wronskian(hist[t], hist[t + 1], hist[t + 2]) for t in range(6)]
        rows[nm] = {"N_J(0)": view.j_number(hist[0]), "N_J(7)": view.j_number(hist[-1]),
                    "W_J per update": wj, "W_J sign": sorted(set(int(np.sign(w)) for w in wj))}
    res["a_J_readout"] = {"seed_report": rep, "runs": rows}
    # (b) click-level CP / P
    maps = standard_maps(T, blocks, Q, L)
    g = gear_groups(T, blocks)
    rng = np.random.default_rng(17)
    s0 = vacuum_state(T, Q, L, *blocks)
    a, b = s0.a.astype(object).copy(), s0.b.astype(object).copy()
    PiW = chiral_algebra()["PiW16"]
    mrows = [T.gear_index(n) for n in g["matter"]]
    for node in range(0, L ** 3, 7):                        # a sparse weak-half packet in the first pair
        v = PiW @ rng.integers(-(1 << 18), 1 << 18, 16)
        w = PiW @ rng.integers(-(1 << 18), 1 << 18, 16)
        for ch, gi in enumerate(mrows):
            b[gi, node] = int(v[ch]); a[gi, node] = int(w[ch])
    for k in range(3):                                         # a weak field
        for gname in g["links"][k][1:]:
            gi = T.gear_index(gname)
            b[gi] = [int(x) for x in rng.integers(-3, 4, L ** 3)]
            a[gi] = [int(x) for x in rng.integers(-3, 4, L ** 3)]
    s0 = State(L, a, b, s0.r)
    Tn = 6
    rec0, _ = click_record(E, s0, Tn)
    out = {}
    for nm in ("CP", "P"):
        X = maps[nm]
        recX, _ = click_record(E, X(s0), Tn)
        # map the original record through X: rebuild states and compare clicks of X(s_t) -> X(s_t+1)
        s, mism, total = s0, 0, 0
        for t in range(Tn):
            s1 = E.step(s)
            c_map = E.clicks(X(s), X(s1), step=t, stream="official")
            c_run = recX[t]
            ra = set(c_map.rows())
            rb = set(c_run.rows())
            mism += len(ra ^ rb)
            total += len(rb)
            s = s1
        out[nm] = {"official_clicks_in_image_run": total, "unpaired_click_entries": mism}
    res["b_click_CP_P"] = out
    res["finished"] = stamp()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "DEMO_summary.json").write_text(json.dumps(res, indent=1, default=str))
    print(json.dumps(res, indent=1, default=str))


if __name__ == "__main__":
    main()
