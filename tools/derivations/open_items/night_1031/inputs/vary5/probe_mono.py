"""VARY5's probe of node-all 4ce1aa9d7: D per term and per monomial, whole numbers, no division; the prober's loops are
the probe's. D_i = [T_i(a+; a) - T_i(a; a+)] + [T_i(a; b) - T_i(b; a)], T_i(x; y) = J_i(y) x_target (VARY4 2.2). A
monomial is read from the plan's structure: its terms are those whose rows (the target and the non-unit legs, as a
multiset) agree. Per round and place it counts the two-leg terms whose own D_i is not 0, the two-leg monomials whose
summed D is not 0, and the monomials of four legs whose summed D is not 0; and it keeps the place's running SUM_i D_i.
Usage: python3 -I -B probe_mono.py <node-all src> <world dir> <setting> <rounds> <out.json>
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(sys.argv[1]).resolve()))
from tensor24 import main as t24  # noqa: E402
from tensor24.engine import state as state_mod  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.runner import load as loading  # noqa: E402
from tensor24.runner.files import sites_of  # noqa: E402

world, setting_name, rounds, out = Path(sys.argv[2]), sys.argv[3], int(sys.argv[4]), Path(sys.argv[5])
universe = json.loads(world.joinpath("universe.json").read_text(encoding="utf-8"))
shape = json.loads(world.joinpath("piece.json").read_text(encoding="utf-8"))["shape"]
setting = json.loads(world.joinpath(setting_name).read_text(encoding="utf-8"))
held, laid = loading.load(universe, setting, sites_of(shape), *t24.made(loading.star(len(shape))))
lay = t24.layout(universe, shape, held)
s = state_mod.State(*held.state)
weight, train, _, _, _ = lay.click
legs, factor, target = lay.plan
edged = [int(i) for i in np.nonzero(np.asarray(np.asarray(weight != 0, dtype=bool).any(axis=1), dtype=bool))[0]]
groups = {}
for i in edged:
    rows = tuple(sorted([int(target[i])] + [int(r) for r in legs[:, i] if int(r) >= 0]))
    groups.setdefault(rows, []).append(i)
by_legs = {}
for rows, members in groups.items():
    by_legs.setdefault(len(rows), []).append(members)
two_terms = [i for members in by_legs.get(2, []) for i in members]


def push(vy):
    first = factor[None, :, None] + 0 * vy[-1:, None]
    return np.prod(np.concatenate((first, vy[legs])), axis=0)


count = {"two-leg terms with D_i != 0 (term x place x round)": 0,
         "two-leg monomials with SUM D != 0 (monomial x place x round)": 0,
         "four-leg monomials with SUM D != 0 (monomial x place x round)": 0}
first_two_term = None
place = np.zeros(s.a.shape[-1], dtype=object)
peak = [0, None]
for at in range(1, rounds + 1):
    new, _ = step.act(lay, s)
    va, vb, va1 = step.valued(s.a), step.valued(s.b), step.valued(new.a)
    ja, jb, ja1 = push(va), push(vb), push(va1)
    d = (ja * va1[target] - ja1 * va[target]) + (jb * va[target] - ja * vb[target])
    nz = int(np.sum(np.asarray(d[two_terms] != 0, dtype=bool))) if two_terms else 0
    count["two-leg terms with D_i != 0 (term x place x round)"] += nz
    if nz and first_two_term is None:
        first_two_term = at
    for k, name in ((2, "two-leg monomials with SUM D != 0 (monomial x place x round)"),
                    (4, "four-leg monomials with SUM D != 0 (monomial x place x round)")):
        for members in by_legs.get(k, []):
            count[name] += int(np.sum(np.asarray(d[members].sum(axis=0) != 0, dtype=bool)))
    place = place + d[edged].sum(axis=0)
    for x in range(len(place)):
        if abs(int(place[x])) > abs(peak[0]):
            peak = [int(place[x]), [x, at]]
    s = new
out.write_text(json.dumps({
    "setting": setting_name, "rounds": rounds, "loader departures": laid, "edged terms": len(edged),
    "monomials by legs (rows in the multiset): count, terms": {str(k): [len(v), sum(len(m) for m in v)]
                                                            for k, v in sorted(by_legs.items())},
    "counts": count, "first round a two-leg term's D_i is not 0": first_two_term,
    "the place's running SUM_i D_i, largest [value, (site, round)]": peak}, indent=1), encoding="utf-8")
