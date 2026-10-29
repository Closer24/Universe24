"""Probe 4: the checks this review asks the load's tests to make, run on a src tree (the worktree's, a mutant copy's or
the fixed copy's). a: contract on gears not 0 gives the J of gears at 0 and leaves the caller's gears as they were;
b: contract on int64 gears still gives Python integers (holds only once the source is made with dtype=object);
c: every laid array of dtype=object, and a gear whose a, b and tooth pass 64 bits laid exactly; d: b's laid entries
counted; e: a gear at the last train's last component laid; f: a strength past 64 bits loads and contracts as the naive sum.
usage: python -I proposed_checks.py <root holding src/ and tests/>"""

import sys

ROOT = sys.argv[1]
sys.path[:0] = [ROOT + "/src", ROOT]
import numpy as np  # noqa: E402

from tensor24.engine.contract import Plan, contract  # noqa: E402
from tests.test_the_tensor24_load import COUPLINGS, D, OPERANDS, ROWS, SITES, TRAINS, joint, load, naive, universe  # noqa: E402

ks, c = joint((SITES, 1, 1))
labels = tuple(name.upper() for name in ks._fields)
results = {}


def check(name, fn):
    try:
        results[name] = bool(fn())
    except Exception as error:  # noqa: BLE001
        results[name] = f"raised {type(error).__name__}: {str(error)[:60]}"


def a():
    held, _ = load(universe(), {"gears": []}, SITES, ks, c)
    readings = np.random.default_rng(1).integers(-1 << 30, 1 << 30, ((len(OPERANDS) + D - 1) * ROWS, SITES)).astype(object)
    gears = np.random.default_rng(2).integers(1, 1 << 30, (ROWS, SITES)).astype(object) << 80
    kept = gears.copy()
    return (contract(Plan(*held.plan), readings, gears) == naive(universe(), c, readings, labels)).all() and (gears == kept).all()


def b():
    held, _ = load(universe(), {"gears": []}, SITES, ks, c)
    readings = np.ones(((len(OPERANDS) + D - 1) * ROWS, SITES), dtype=object) << 70
    j = contract(Plan(*held.plan), readings, np.zeros((ROWS, SITES), dtype=np.int64))
    return j.dtype == object and all(type(x) is int for x in j.ravel()) and (j == naive(universe(), c, readings, labels)).all()


big = 1 << 70


def c_():
    held, found = load(universe(), {"gears": [[0, 1, 3, big, big + 1, big + 2]]}, SITES, ks, c)
    arrays = held.state
    return (found == [] and all(x.dtype == object for x in arrays)
            and (arrays[0][1, 3], arrays[1][1, 3], arrays[2][1, 3]) == (big, big + 1, big + 2)
            and all(type(x) is int for x in np.concatenate([y.ravel() for y in arrays])))


def d():
    laid = [[0, 1, 3, 5, 6, 4], [len(TRAINS) - 1, 1, 3, 6, 5, 0]]
    held, _ = load(universe(), {"gears": laid}, SITES, ks, c)
    return (held.state[1] != 0).sum() == len(laid)


def e():
    last = len(TRAINS) - 1
    held, found = load(universe(), {"gears": [[last, 3, 2, 5, 6, 0]]}, SITES, ks, c)
    return found == [] and held.state[0][ROWS - 1, 2] == 5


def f():
    couplings = [[*x[:-1], x[-1] << 70] for x in COUPLINGS]
    u = universe(couplings=couplings)
    held, found = load(u, {"gears": []}, SITES, ks, c)
    readings = np.random.default_rng(3).integers(-1 << 30, 1 << 30, ((len(OPERANDS) + D - 1) * ROWS, SITES)).astype(object)
    return found == [] and (contract(Plan(*held.plan), readings, 0 * held.state[0]) == naive(u, c, readings, labels)).all()


for name, fn in (("a gears not 0", a), ("b int64 gears", b), ("c the lay's dtype and 2^70", c_), ("d b counted", d),
                 ("e the last train's last component", e), ("f a strength of 2^70", f)):
    check(name, fn)
print("; ".join(f"{k}: {v}" for k, v in results.items()))
