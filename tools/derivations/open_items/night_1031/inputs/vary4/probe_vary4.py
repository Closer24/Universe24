"""VARY4's probe of node-all 4ce1aa9d7 (term 11 on the edges, plans.edging), whole numbers, Rule3's carry the one
division; the prober's loops and comparisons are the probe's, not the act's. Built from the THIRD readers' probes
(vary3_math/probe_all.py, vary3_phys/probe_all.py).
Usage: python -I probe_vary4.py <node-all src> <world dir> <setting file name> <rounds> <out.json>
Every round, at every place (a Node-clock in a round), it reads:
 the checks that hold by construction:
  - the carry's law on every side: q key_e + k' = P + k (P from step.passing and step.crossing on the same window);
  - the per-edge books: q(t,u) + q(u,t) = 0, P(t,u) + P(u,t) = 0, k(t,u) + k(u,t) = key_e - 1 (t != u);
  - the place's books: the sum of a Node-clock's sides' q is 0;
  - the sides that cannot move: P = 0 on every across side (the Mesh couplings) and on every diagonal side (t, t);
  - David's identity at each clock (a train t at a Node-clock): key_e N_t - B_t = the teeth's change, within 4 edge keys;
 the reading that can fail (the Boss's ruling, 07:5x UTC):
  - each clock's own work on its edged terms, O_t = kappa SUM over the terms with a nonzero edge weight whose leg is in
    t of W_i, W_i = J_i(a) (a+ - b) (step.passing's own work), running, against its booked total B_t = SUM_u P(t,u),
    running; M_t = O_t - B_t, the part no edge carries, held within the clock's teeth only where |M_t| < 4 key_e (its 4
    sides (t, u), u != t, the only ones that move); also O_t - key_e N_t, the work against the quanta booked;
  - the 1 : 2 share on a lay where only the held-giver ties work: 2 M_held = M_giver at every place;
  - kappa R at a Node-clock, SUM_t M_t = SUM_t O_t (B summed over the trains is 0).
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
from tensor24.runner import run as run_mod  # noqa: E402
from tensor24.runner.files import setting_departures, sites_of  # noqa: E402


def keys(v, key_e):
    """|v| in whole edge keys (Rule3's quotient) and the tooth left."""
    q, r = carry(abs(int(v)), key_e, 0)
    return [int(q), int(r)]


def main():
    world, setting_name, rounds, out = Path(sys.argv[2]), sys.argv[3], int(sys.argv[4]), Path(sys.argv[5])
    universe = json.loads(world.joinpath("universe.json").read_text(encoding="utf-8"))
    piece = json.loads(world.joinpath("piece.json").read_text(encoding="utf-8"))
    setting = json.loads(world.joinpath(setting_name).read_text(encoding="utf-8"))
    shape = piece["shape"]
    fits = setting_departures(setting, universe, piece)
    held, laid = loading.load(universe, setting, sites_of(shape), *t24.made(loading.star(len(shape))))
    lay = t24.layout(universe, shape, held)
    s = state_mod.State(*held.state)
    width = universe["integers"]["width"]
    weight, train, key_arr, across, onto = lay.click
    T = weight.shape[-1]
    key_e = int(key_arr.flat[0])
    one_key = int(np.sum(np.asarray(key_arr != key_e, dtype=bool)))
    key_f = int(universe["chosen"]["key"])
    scale, rem = carry(key_e, key_f, 0)
    senses = int(step.halves(lay))
    kappa = senses * int(scale)
    legs, factor, target = lay.plan
    sites = s.a.shape[-1]
    edged = np.asarray(np.asarray(weight != 0, dtype=bool).any(axis=1), dtype=np.int64)
    teeth_cap = (T - 1) * key_e
    bad = {"carry's law (sides x places)": 0, "q(t,u)+q(u,t) != 0": 0, "P(t,u)+P(u,t) != 0": 0,
           "k(t,u)+k(u,t) != key_e-1": 0, "place's books: Node-clock SUM q != 0": 0, "across P != 0": 0,
           "diagonal P != 0": 0, "David's identity |key_e N_t - B_t| >= 4 key_e": 0}
    moved_sides = np.zeros((T, T), dtype=np.int64)
    O = np.zeros((T, sites), dtype=object)
    B = np.zeros((T, sites), dtype=object)
    N = np.zeros((T, sites), dtype=object)
    beyond_rounds = np.zeros((T, sites), dtype=np.int64)
    first_beyond = [[None] * sites for _ in range(T)]
    peak = {"M_t = O_t - B_t at a clock": [0, None], "O_t - key_e N_t at a clock": [0, None],
            "kappa R at a Node-clock": [0, None], "|B_t| at a clock, in quanta booked |N_t|": [0, None]}
    share_off, share_places = 0, 0
    round1 = None
    promise = None
    lines = [0] * T
    for at in range(1, rounds + 1):
        got = run_mod.promised(t24.ENGINE, lay, s, width)
        if got and promise is None:
            promise = [at, got[0], len(got)]
        new, clicks = step.act(lay, s)
        own = step.passing(lay.click, lay.plan, s.b, s.a, new.a)
        cross = step.crossing(lay.click, lay.nb, s.b, s.a, new.a)
        passed = np.concatenate((own, cross))
        bad["carry's law (sides x places)"] += int(np.sum(np.asarray(clicks * key_e + new.k - s.k != passed, dtype=bool)))
        bad["across P != 0"] += int(np.sum(np.asarray(cross != 0, dtype=bool)))
        q = clicks[:T * T].reshape(T, T, sites)
        p = own.reshape(T, T, sites)
        k1 = new.k[:T * T].reshape(T, T, sites)
        bad["q(t,u)+q(u,t) != 0"] += int(np.sum(np.asarray(q + q.swapaxes(0, 1) != 0, dtype=bool)))
        bad["P(t,u)+P(u,t) != 0"] += int(np.sum(np.asarray(p + p.swapaxes(0, 1) != 0, dtype=bool)))
        off = np.asarray(k1 + k1.swapaxes(0, 1) != key_e - 1, dtype=bool)
        for t in range(T):
            off[t, t] = False
            bad["diagonal P != 0"] += int(np.sum(np.asarray(p[t, t] != 0, dtype=bool)))
        bad["k(t,u)+k(u,t) != key_e-1"] += int(np.sum(off))
        bad["place's books: Node-clock SUM q != 0"] += int(np.sum(np.asarray(q.sum(axis=(0, 1)) != 0, dtype=bool)))
        moved_sides += np.asarray(np.asarray(p != 0, dtype=bool).sum(axis=2), dtype=np.int64)
        va, vb, va1 = step.valued(s.a), step.valued(s.b), step.valued(new.a)
        first = factor[None, :, None] + 0 * va[-1:, None]
        work = np.prod(np.concatenate((first, va[legs])), axis=0) * (va1[target] - vb[target])
        mine = np.zeros((T, sites), dtype=object)
        np.add.at(mine, train, work * edged[:, None])
        O = O + kappa * mine
        B = B + p.sum(axis=1)
        N = N + q.sum(axis=1)
        M = O - B
        F = O - key_e * N
        R = M.sum(axis=0)
        teeth = key_e * N - B
        for t in range(T):
            lines[t] += int(np.sum(np.asarray(q[t].sum(axis=0) != 0, dtype=bool)))
            for x in range(sites):
                m, f, d, nq = int(M[t, x]), int(F[t, x]), int(teeth[t, x]), int(N[t, x])
                if abs(d) >= teeth_cap:
                    bad["David's identity |key_e N_t - B_t| >= 4 key_e"] += 1
                if abs(m) >= teeth_cap:
                    beyond_rounds[t, x] += 1
                    if first_beyond[t][x] is None:
                        first_beyond[t][x] = at
                if abs(m) > abs(peak["M_t = O_t - B_t at a clock"][0]):
                    peak["M_t = O_t - B_t at a clock"] = [m, [t, x, at]]
                if abs(f) > abs(peak["O_t - key_e N_t at a clock"][0]):
                    peak["O_t - key_e N_t at a clock"] = [f, [t, x, at]]
                if abs(nq) > abs(peak["|B_t| at a clock, in quanta booked |N_t|"][0]):
                    peak["|B_t| at a clock, in quanta booked |N_t|"] = [nq, [t, x, at]]
        for x in range(sites):
            r = int(R[x])
            if abs(r) > abs(peak["kappa R at a Node-clock"][0]):
                peak["kappa R at a Node-clock"] = [r, [x, at]]
            share_places += 1
            share_off += int(2 * int(M[2, x]) != int(M[3, x]))
        if at == 1:
            round1 = {"clicks by train at each Node-clock, distinct values": [sorted({int(v) for v in q[t].sum(axis=0)})
                                                                              for t in range(T)],
                      "|M_t| largest by train, edge keys": [keys(max(abs(int(v)) for v in M[t]), key_e)
                                                             for t in range(T)],
                      "O_t (own work) distinct values by train": [sorted({int(v) for v in O[t]})[:4] for t in range(T)]}
        s = new
    clocks_beyond = [int(np.sum(np.asarray(beyond_rounds[t] > 0, dtype=bool))) for t in range(T)]
    firsts = [min([r for r in first_beyond[t] if r is not None], default=None) for t in range(T)]
    in_keys = {name: v + [keys(v[0], key_e)] for name, v in peak.items()}
    end_by_train = {"M_t summed over the sites": [int(M[t].sum()) for t in range(T)],
                    "M_t summed over the sites, edge keys": [keys(int(M[t].sum()), key_e) for t in range(T)],
                    "N_t summed over the sites (quanta)": [int(N[t].sum()) for t in range(T)]}
    out.write_text(json.dumps({
        "world": world.name, "setting": setting_name, "rounds": rounds, "setting departures": fits,
        "loader departures": laid, "first promise departure": promise, "file key": key_f, "edge key": key_e,
        "sides keyed otherwise": one_key, "edge key / file key": [int(scale), int(rem)], "senses": senses,
        "kappa": kappa, "trains": T, "sides x sites": list(s.k.shape), "edged terms": int(edged.sum()),
        "terms": int(len(factor)), "teeth cap (4 sides), edge keys": T - 1,
        "checks by construction, places or sides off": bad,
        "own-reach sides that ever move (places with P != 0), row t col u": moved_sides.tolist(),
        "train lines (places with a nonzero net)": lines,
        "the reading that can fail": {
            "clocks beyond their teeth at some round, by train (of 27)": clocks_beyond,
            "first round a clock is beyond, by train": firsts,
            "clock-rounds beyond, by train": [int(beyond_rounds[t].sum()) for t in range(T)],
            "peaks [value, where, |value| in edge keys and tooth]": in_keys,
            "2 M_held = M_giver: places off / places": [share_off, share_places]},
        "round 1": round1, "end": end_by_train}, indent=1), encoding="utf-8")


main()
