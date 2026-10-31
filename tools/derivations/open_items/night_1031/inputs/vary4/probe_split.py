"""VARY4's second probe of node-all 4ce1aa9d7: each clock's part no edge carries, M_t = O_t - B_t, split exactly into a
state part and a residual part; whole numbers, Rule3's carry the one division; the prober's loops are the probe's.
Usage: python -I probe_split.py <node-all src> <world dir> <setting file name> <rounds> <out.json> <site> <round>
Per term i of J's plan on an edged monomial, with J_i(y) its push at the counts y and T_i(x; y) = J_i(y) x_target:
  W_i = T_i(a+; a) - T_i(b; a)                                     (step.passing's own work over the window)
  2 G_i(n) = T_i(a+; a) + T_i(a; a+)                                (the polarized energy at the window's top)
  D_i = [T_i(a+; a) - T_i(a; a+)] + [T_i(a; b) - T_i(b; a)]          (the antisymmetric part over the two windows)
  2 W_i = 2 G_i(n) - 2 G_i(n - 1) + D_i                             (an identity, checked)
The map Lmap from a per-term array X to the clocks, Lmap[X]_t = kappa SUM_{i in t} X_i - SUM_u P[X](t, u), P[X] the
act's passing of X (step.passing's weights), gives M_t = Lmap[W] summed over the rounds; so, exactly,
  2 M_t = St_t + Res_t, St_t = Lmap[2 G(now)] - Lmap[2 G(start)] (a function of the board's counts alone),
  Res_t = SUM over the rounds of Lmap[D] (0 for every two-leg monomial: T is symmetric there).
Per place it reads the running SUM_i D_i (the residual at the Node-clock, at kappa 1), and prints it at <site> <round>.
"""
import json
import sys
from pathlib import Path

import numpy as np

SRC = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(SRC))
from tensor24 import main as t24  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import state as state_mod  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.runner import load as loading  # noqa: E402
from tensor24.runner.files import sites_of  # noqa: E402


def keys(v, key_e):
    q, r = carry(abs(int(v)), key_e, 0)
    return [int(q), int(r)]


def main():
    world, setting_name, rounds, out = Path(sys.argv[2]), sys.argv[3], int(sys.argv[4]), Path(sys.argv[5])
    at_site, at_round = int(sys.argv[6]), int(sys.argv[7])
    universe = json.loads(world.joinpath("universe.json").read_text(encoding="utf-8"))
    shape = json.loads(world.joinpath("piece.json").read_text(encoding="utf-8"))["shape"]
    setting = json.loads(world.joinpath(setting_name).read_text(encoding="utf-8"))
    held, laid = loading.load(universe, setting, sites_of(shape), *t24.made(loading.star(len(shape))))
    lay = t24.layout(universe, shape, held)
    s = state_mod.State(*held.state)
    weight, train, key_arr, _, _ = lay.click
    T = weight.shape[-1]
    key_e = int(key_arr.flat[0])
    scale, _ = carry(key_e, int(universe["chosen"]["key"]), 0)
    kappa = int(step.halves(lay)) * int(scale)
    legs, factor, target = lay.plan
    sites = s.a.shape[-1]
    edged = np.asarray(np.asarray(weight != 0, dtype=bool).any(axis=1), dtype=np.int64)[:, None]

    def push(vy):
        first = factor[None, :, None] + 0 * vy[-1:, None]
        return np.prod(np.concatenate((first, vy[legs])), axis=0) * edged

    def lmap(x):
        mine = np.zeros((T, sites), dtype=object)
        np.add.at(mine, train, x)
        given = np.zeros((T, T, sites), dtype=object)
        np.add.at(given, train, weight[:, :, None] * x[:, None, :])
        return kappa * mine - (given - given.swapaxes(0, 1)).sum(axis=1)

    off = {"2 W = 2 G(n) - 2 G(n-1) + D (terms x places)": 0, "Lmap[W] running = O - B (clocks x rounds)": 0,
           "2 M = St + Res (clocks x rounds)": 0}
    M = np.zeros((T, sites), dtype=object)
    O = np.zeros((T, sites), dtype=object)
    B = np.zeros((T, sites), dtype=object)
    Res = np.zeros((T, sites), dtype=object)
    Dplace = np.zeros(sites, dtype=object)
    base = None
    peak = {"Res_t / 2 at a clock (the residual's share)": [0, None], "St_t / 2 at a clock (the state part)": [0, None],
            "SUM_i D_i running at a Node-clock (kappa 1)": [0, None]}
    beyond = {"Res": [[None] * sites for _ in range(T)], "St": [[None] * sites for _ in range(T)]}
    at_value = None
    for at in range(1, rounds + 1):
        new, _ = step.act(lay, s)
        va, vb, va1 = step.valued(s.a), step.valued(s.b), step.valued(new.a)
        ja, jb, ja1 = push(va), push(vb), push(va1)
        t_up, t_down = ja * va1[target], ja1 * va[target]  # T(a+; a), T(a; a+)
        t_ab, t_ba = jb * va[target], ja * vb[target]  # T(a; b), T(b; a)
        w = t_up - t_ba
        g_now, g_before, d = t_up + t_down, t_ab + t_ba, (t_up - t_down) + (t_ab - t_ba)
        off["2 W = 2 G(n) - 2 G(n-1) + D (terms x places)"] += int(np.sum(np.asarray(
            w + w != g_now - g_before + d, dtype=bool)))
        if base is None:
            base = lmap(g_before)
        own = step.passing(lay.click, lay.plan, s.b, s.a, new.a).reshape(T, T, sites)
        mine = np.zeros((T, sites), dtype=object)
        np.add.at(mine, train, w)
        O, B = O + kappa * mine, B + own.sum(axis=1)
        M = M + lmap(w)
        off["Lmap[W] running = O - B (clocks x rounds)"] += int(np.sum(np.asarray(M != O - B, dtype=bool)))
        Res = Res + lmap(d)
        St = lmap(g_now) - base
        off["2 M = St + Res (clocks x rounds)"] += int(np.sum(np.asarray(M + M != St + Res, dtype=bool)))
        Dplace = Dplace + d.sum(axis=0)
        if at == at_round:
            at_value = int(Dplace[at_site])
        for t in range(T):
            for x in range(sites):
                r2, s2 = int(Res[t, x]), int(St[t, x])
                if abs(r2) > abs(2 * peak["Res_t / 2 at a clock (the residual's share)"][0]):
                    peak["Res_t / 2 at a clock (the residual's share)"] = [carry(r2, 2, 0)[0], [t, x, at], r2]
                if abs(s2) > abs(2 * peak["St_t / 2 at a clock (the state part)"][0]):
                    peak["St_t / 2 at a clock (the state part)"] = [carry(s2, 2, 0)[0], [t, x, at], s2]
                for name, v in (("Res", r2), ("St", s2)):
                    if abs(v) >= 2 * (T - 1) * key_e and beyond[name][t][x] is None:
                        beyond[name][t][x] = at
        for x in range(sites):
            v = int(Dplace[x])
            if abs(v) > abs(peak["SUM_i D_i running at a Node-clock (kappa 1)"][0]):
                peak["SUM_i D_i running at a Node-clock (kappa 1)"] = [v, [x, at]]
        s = new
    summary = {}
    for name in ("Res", "St"):
        summary[name + ": clocks beyond 4 edge keys at some round, by train"] = [
            sum(1 for r in beyond[name][t] if r is not None) for t in range(T)]
        summary[name + ": first round beyond, by train"] = [
            min([r for r in beyond[name][t] if r is not None], default=None) for t in range(T)]
    out.write_text(json.dumps({
        "setting": setting_name, "rounds": rounds, "loader departures": laid, "kappa": kappa, "edge key": key_e,
        "identities, off": off, "peaks [value, where, (2x value)] and |value| in edge keys":
        {k: v + [keys(v[0], key_e)] for k, v in peak.items()}, "beyond": summary,
        "Res_t / 2 summed over the sites at the end, by train": [int(carry(int(Res[t].sum()), 2, 0)[0]) for t in range(T)],
        "SUM_i D_i running at the site and round asked": [at_site, at_round, at_value]}, indent=1), encoding="utf-8")


main()
