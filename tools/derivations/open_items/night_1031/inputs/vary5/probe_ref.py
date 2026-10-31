"""The reader's check of VARY4's split (probe_split.py's quantities, recomputed), whole numbers, Rule3's carry the one
division: does the residual's share depend on the reference energy? VARY4's reference per term is the polarized
2 G_i = T_i(a+; a) + T_i(a; a+), which at rest is -k H for a k-leg monomial (Euler), so to first order in the counts'
step v, 2 dG = -2 k f v.P against 2 W = -4 f v.P: D = 2 W - 2 dG = 2 (k - 2) f v.P, 0 for two legs and about -dG for
the four-leg tie. The reference that matches the work at first order for every k is G' = (2 / k) G (at rest -2 H for
every monomial, the two-leg staggered energy unchanged). Doubled to stay whole: 4 M = St' + Res', St' = Lmap[(4 / k) 2 G]
now less at the start, Res' = 4 M - St'. Prints, beside VARY4's, the residual's share Res'/4 and the state part St'/4:
their largest at a clock, the clocks past 4 edge keys and the first round; and the place's residual at kappa 1 under
both references, running. Usage: python3 -I -B probe_ref.py <node-all src> <world dir> <setting> <rounds>"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(sys.argv[1]).resolve()))
from tensor24 import main as t24  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import state as state_mod  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.runner import load as loading  # noqa: E402
from tensor24.runner.files import sites_of  # noqa: E402

world, setting_name, rounds = Path(sys.argv[2]), sys.argv[3], int(sys.argv[4])
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
# each term's monomial's value legs: its own target plus its non-unit legs
k_legs = 1 + np.asarray(np.asarray(legs >= 0, dtype=bool).sum(axis=0), dtype=np.int64)
four_over_k = np.asarray([carry(4, int(k), 0)[0] for k in k_legs], dtype=object)[:, None]  # 2 for two legs, 1 for four
ks = sorted({int(k) for k, e in zip(k_legs, edged[:, 0]) if e})
print(f"{world.name}/{setting_name}: edge key {key_e}, kappa {kappa}, departures {laid}; edged terms by legs:"
      f" {[(k, int(sum(1 for kk, e in zip(k_legs, edged[:, 0]) if e and kk == k))) for k in ks]}")


def push(vy):
    first = factor[None, :, None] + 0 * vy[-1:, None]
    return np.prod(np.concatenate((first, vy[legs])), axis=0) * edged


def lmap(x):
    mine = np.zeros((T, sites), dtype=object)
    np.add.at(mine, train, x)
    given = np.zeros((T, T, sites), dtype=object)
    np.add.at(given, train, weight[:, :, None] * x[:, None, :])
    return kappa * mine - (given - given.swapaxes(0, 1)).sum(axis=1)


M = np.zeros((T, sites), dtype=object)
Res = np.zeros((T, sites), dtype=object)
D_place = np.zeros(sites, dtype=object)
W_place = np.zeros(sites, dtype=object)
Dn_place = np.zeros(sites, dtype=object)
base = base_n = g0_place = None
peak = {"VARY4 Res/2": (0, None), "VARY4 St/2": (0, None), "normalized Res'/4": (0, None),
        "normalized St'/4": (0, None), "place D (VARY4), kappa 1": (0, None), "place D' (normalized), kappa 1": (0, None)}
first = {name: [None] * T for name in ("VARY4 Res/2", "normalized Res'/4")}
count = {name: [set() for _ in range(T)] for name in ("VARY4 Res/2", "normalized Res'/4")}
off = 0
for at in range(1, rounds + 1):
    new, _ = step.act(lay, s)
    va, vb, va1 = step.valued(s.a), step.valued(s.b), step.valued(new.a)
    ja, jb, ja1 = push(va), push(vb), push(va1)
    t_up, t_down, t_ab, t_ba = ja * va1[target], ja1 * va[target], jb * va[target], ja * vb[target]
    w = t_up - t_ba
    g_now, g_before, d = t_up + t_down, t_ab + t_ba, (t_up - t_down) + (t_ab - t_ba)
    if base is None:
        base, base_n = lmap(g_before), lmap(four_over_k * g_before)
        g0_place = (four_over_k * g_before).sum(axis=0)
    M = M + lmap(w)
    Res = Res + lmap(d)
    St = lmap(g_now) - base
    off += int(np.sum(np.asarray(M + M != St + Res, dtype=bool)))
    St_n = lmap(four_over_k * g_now) - base_n
    Res_n = 4 * M - St_n
    D_place = D_place + d.sum(axis=0)
    W_place = W_place + w.sum(axis=0)
    # the place's residual under G' at kappa 1, doubled: 2 (2 SUM W) - (4/k) 2 G (now less start)
    Dn_place = 4 * W_place - ((four_over_k * g_now).sum(axis=0) - g0_place)
    for t in range(T):
        for x in range(sites):
            for name, v, div in (("VARY4 Res/2", Res[t, x], 2), ("VARY4 St/2", St[t, x], 2),
                                 ("normalized Res'/4", Res_n[t, x], 4), ("normalized St'/4", St_n[t, x], 4)):
                h, _ = carry(int(v), div, 0)
                if abs(h) > abs(peak[name][0]):
                    peak[name] = (int(h), (t, x, at))
                if name in first and abs(h) >= (T - 1) * key_e:
                    count[name][t].add(x)
                    if first[name][t] is None:
                        first[name][t] = at
    for x in range(sites):
        if abs(int(D_place[x])) > abs(peak["place D (VARY4), kappa 1"][0]):
            peak["place D (VARY4), kappa 1"] = (int(D_place[x]), (x, at))
        h, _ = carry(int(Dn_place[x]), 2, 0)
        if abs(h) > abs(peak["place D' (normalized), kappa 1"][0]):
            peak["place D' (normalized), kappa 1"] = (int(h), (x, at))
    if at == 170:
        print(f"  round 170, site 17: place D (VARY4) {int(D_place[17])}; place D' (normalized) "
              f"{carry(int(Dn_place[17]), 2, 0)[0]}; giver Res/2 {carry(int(Res[3, 17]), 2, 0)[0]}, Res'/4"
              f" {carry(int(Res_n[3, 17]), 4, 0)[0]}; giver St/2 {carry(int(St[3, 17]), 2, 0)[0]}, St'/4"
              f" {carry(int(St_n[3, 17]), 4, 0)[0]}; giver M {int(M[3, 17])}")
    s = new
print(f"  2 M = St + Res off at {off} clock-rounds (VARY4's identity, recomputed)")
for name, (v, where) in peak.items():
    if where is not None:
        print(f"  {name}: largest {v} at {where}, {carry(abs(v), key_e, 0)[0]} edge keys")
for name in first:
    print(f"  {name}: clocks past 4 edge keys by train {[len(c) for c in count[name]]}; first round {first[name]}")
