"""Probe 5: files the checker holds, at the load's edges, through the checker and the load as tools/tensor24_files.py runs
them, under a 6 GB address-space cap: (1) every coupling row over trains of every kind the load takes (each of the four on a
hand, and all four on one gear in another order) with every operand and every target, in one universe: no raise, each refusal one of
the load's named kinds, and the rows it takes contracted equal to the load test's naive sum at huge readings and a
strength past 64 bits; (2) boards of 2^31 to 2^1000 sites: named, no raise; (3) a gear and a strength of 2^1000: laid and
planned exactly, Python integers throughout.
usage: python -I load_edges.py <worktree>"""

import itertools
import json
import resource
import sys
import tempfile
from collections import Counter
from pathlib import Path

WT = sys.argv[1]
sys.path[:0] = [WT + "/src", WT]
resource.setrlimit(resource.RLIMIT_AS, (6 << 30, 6 << 30))
import numpy as np  # noqa: E402

from tensor24.engine.contract import Plan, contract  # noqa: E402
from tensor24.main import made  # noqa: E402
from tensor24.runner.files import OPERANDS, departures, sites_of  # noqa: E402
from tensor24.runner.load import load  # noqa: E402
from tests.test_the_tensor24_load import naive  # noqa: E402

TRAINS = [{"name": k.lower(), "kinds": [k], "part": 2, "pinion": 3, "sine": 4} for k in ("A1", "A2", "T1", "T2")]
TRAINS.append({"name": "mixed", "kinds": ["T2", "A1", "T1", "A2"], "part": 1, "pinion": 2})
INTEGERS = {"den": 5, "full_rate": 1000, "key": 36000, "trace": 6, "width": 1100}


def files(d, trains, couplings, shape, gears):
    docs = {"universe": {"version": 1, "integers": INTEGERS, "trains": trains, "couplings": couplings},
            "piece": {"version": 1, "shape": shape}, "setting": {"version": 1, "ticks": 1, "gears": gears}}
    paths = []
    for name, doc in docs.items():
        (d / f"{name}.json").write_text(json.dumps(doc), encoding="utf-8")
        paths.append(d / f"{name}.json")
    return paths


def run(paths):
    """The tool's two steps: the checker, then the load on the board's kinds; a raise is reported, never swallowed."""
    found = departures(*paths)
    if found:
        return "checker", found, None
    u, p, s = (json.loads(x.read_text(encoding="utf-8")) for x in paths)
    try:
        held, named = load(u, s, sites_of(p["shape"]), *made(tuple(p["shape"])))
    except BaseException as error:  # noqa: BLE001
        return "RAISED", [f"{type(error).__name__}: {error}"], None
    return "load", named, held


sides = [(t, k, p, o) for t, train in enumerate(TRAINS) for k in range(len(train["kinds"])) for p in range(train["part"]) for o in range(len(OPERANDS))]
targets = [(t, k, p) for t, train in enumerate(TRAINS) for k in range(len(train["kinds"])) for p in range(train["part"])]
couplings = [[*x, *y, *z, 3] for x, y, z in itertools.product(sides, sides, targets)]
with tempfile.TemporaryDirectory(dir="/dev/shm/tmp") as d:
    d = Path(d)
    where, found, held = run(files(d, TRAINS, couplings, [2, 2, 1], []))
    kinds = Counter(line.split(": ", 1)[1].split(",")[0][:40] for line in found)
    print(f"(1) {len(couplings)} coupling rows: {where}; refusals by kind {dict(kinds)}")
    refused = {int(line.split("[")[1].split("]")[0]) for line in found}
    taken = [row for at, row in enumerate(couplings) if at not in refused]
    taken = [[*row[:-1], (1 << 70) + at] for at, row in enumerate(taken)]
    where, found, held = run(files(d, TRAINS, taken, [2, 2, 1], []))
    rows = sum(t.rows() for t in held.trains)
    readings = np.random.default_rng(9).integers(-1 << 40, 1 << 40, ((len(OPERANDS) + 2) * rows, 4)).astype(object) << 70
    ks, c = made((2, 2, 1))
    labels = tuple(name.upper() for name in ks._fields)
    j = contract(Plan(*held.plan), readings, held.state[0])
    same = (j == naive({"trains": TRAINS, "couplings": taken}, c, readings, labels)).all()
    print(f"    the {len(taken)} rows it takes: {where}, named {found[:1]}; terms {len(held.plan[0])}; J equals the naive sum: {bool(same)};"
          f" every entry a Python int: {all(type(x) is int for x in j.ravel())}; J not all 0: {bool(j.any())}")
    for e in (31, 32, 40, 62, 63, 64, 100, 1000):
        where, found, _ = run(files(d, TRAINS[:1], [], [1 << e, 1, 1], []))
        print(f"(2) a board of 2^{e} sites: {where}: {[line[:110] for line in found]}")
    huge = 1 << 1000
    where, found, held = run(files(d, TRAINS[:1], [[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, huge]], [3, 1, 1], [[0, 1, 2, huge, -huge, huge - 1]]))
    a, b, r = held.state[:3]
    print(f"(3) a gear and a strength of 2^1000: {where}, named {found}; laid exactly {(a[1, 2], b[1, 2], r[1, 2]) == (huge, -huge, huge - 1)};"
          f" factor {held.plan[2].tolist() == [huge]} of {held.plan[2].dtype}; state dtypes {sorted({x.dtype.str for x in held.state})}")
