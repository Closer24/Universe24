"""Probe 1: contract (the scattered sum) against the old dense form (927071a14) and a naive loop, on random plans with
repeated landings, an empty plan, huge integers and negative factors; every entry a Python int; then gears not of
dtype=object, and the caller's gears left untouched.
usage: python -I contract_equiv.py <worktree>"""

import random
import sys

sys.path[:0] = [sys.argv[1] + "/src"]
import numpy as np  # noqa: E402

from tensor24.engine.contract import Plan, contract  # noqa: E402


def dense(plan, readings, rows):
    """927071a14's form: a 0/1 scatter matrix of rows x terms, matmul'ed."""
    first, second, factor, target = plan
    scatter = np.zeros((rows, len(target)), dtype=object)
    scatter[list(target), range(len(target))] = 1
    return scatter @ (factor[:, None] * readings[first] * readings[second])


def naive(plan, readings, rows):
    first, second, factor, target = plan
    sites = readings.shape[-1]
    j = [[0] * sites for _ in range(rows)]
    for t in range(len(target)):
        for s in range(sites):
            j[target[t]][s] += factor[t] * readings[first[t]][s] * readings[second[t]][s]
    return j


rng = random.Random(11)
cases = bad = 0
kinds = {"repeated landings": 0, "empty plan": 0, "one row": 0, "huge": 0, "negative factor": 0}
for trial in range(600):
    rows, sites, planes = rng.choice((1, 2, 5, 17)), rng.choice((1, 3, 8)), rng.choice((1, 7))
    terms = rng.choice((0, 1, 2, 6, 40, 300))
    bits = rng.choice((3, 64, 200, 1000))
    first = np.array([rng.randrange(planes * rows) for _ in range(terms)], dtype=np.intp)
    second = np.array([rng.randrange(planes * rows) for _ in range(terms)], dtype=np.intp)
    mode = rng.choice(("random", "all one row", "sorted", "distinct"))
    if mode == "all one row":
        target = [rng.randrange(rows)] * terms
    elif mode == "distinct" and terms <= rows:
        target = rng.sample(range(rows), terms)
    else:
        target = sorted(rng.randrange(rows) for _ in range(terms)) if mode == "sorted" else [rng.randrange(rows) for _ in range(terms)]
    target = np.array(target, dtype=np.intp)
    factor = np.array([rng.randrange(-(1 << bits), 1 << bits) for _ in range(terms)], dtype=object)
    readings = np.array([[rng.randrange(-(1 << bits), 1 << bits) for _ in range(sites)] for _ in range(planes * rows)], dtype=object)
    plan = Plan(first, second, factor, target)
    gears = np.zeros((rows, sites), dtype=object)
    new = contract(plan, readings, gears)
    old = dense(plan, readings, rows)
    loop = naive(plan, readings, rows)
    same = new.shape == (rows, sites) and (new == old).all() and new.tolist() == loop
    ints = all(type(x) is int for x in new.ravel()) and new.dtype == object
    cases += 1
    bad += not (same and ints)
    kinds["repeated landings"] += len(set(target.tolist())) < terms
    kinds["empty plan"] += terms == 0
    kinds["one row"] += rows == 1
    kinds["huge"] += bits >= 200
    kinds["negative factor"] += any(f < 0 for f in factor)
    if not (same and ints):
        print("MISMATCH", trial, rows, sites, terms, bits, mode, same, ints)
print(f"{cases} random plans: {cases - bad} equal to the dense form and the naive loop, every entry a Python int; {bad} not")
print("covered:", kinds)

# the caller's gears are left untouched
gears = np.arange(6, dtype=object).reshape(2, 3) + (1 << 100)
before = gears.copy()
plan = Plan(np.array([0, 1], dtype=np.intp), np.array([1, 0], dtype=np.intp), np.array([2, -3], dtype=object), np.array([1, 1], dtype=np.intp))
readings = np.arange(6, dtype=object).reshape(2, 3) + (1 << 90)
j = contract(plan, readings, gears)
print("gears not zero: J independent of the gears' values:", (j == contract(plan, readings, 0 * gears)).all(), "; the caller's gears untouched:", (gears == before).all())

# gears not of dtype=object
small = Plan(np.array([0], dtype=np.intp), np.array([0], dtype=np.intp), np.array([3], dtype=object), np.array([0], dtype=np.intp))
for name, g in (("int64", np.zeros((1, 2), dtype=np.int64)), ("float64", np.zeros((1, 2))), ("bool", np.zeros((1, 2), dtype=bool)),
                ("uint8", np.zeros((1, 2), dtype=np.uint8)), ("object of np.int64", np.array([[np.int64(0), np.int64(0)]], dtype=object))):
    for label, r in (("small", np.array([[5, 7]], dtype=object)), ("2^40", np.array([[(1 << 40) + 1, 7]], dtype=object)),
                     ("2^100", np.array([[(1 << 100) + 1, 7]], dtype=object))):
        try:
            out = contract(small, r, g)
            want = [3 * int(x) * int(x) for x in r[0]]
            got = out[0].tolist()
            print(f"gears {name:<19} readings {label:<6}: J dtype {out.dtype}, entry type {type(out[0, 0]).__name__}, exact {all(type(x)(w) == x and int(x) == w for x, w in zip(got, want))}"
                  + ("" if [int(x) for x in got] == want else f" (got {int(got[0])}, want {want[0]})"))
        except Exception as error:  # noqa: BLE001
            print(f"gears {name:<19} readings {label:<6}: RAISES {type(error).__name__}: {str(error)[:80]}")
alt = np.zeros_like(np.zeros((1, 2), dtype=np.int64), dtype=object)
print("np.zeros_like(int64 gears, dtype=object): dtype", alt.dtype, "entry type", type(alt[0, 0]).__name__)
