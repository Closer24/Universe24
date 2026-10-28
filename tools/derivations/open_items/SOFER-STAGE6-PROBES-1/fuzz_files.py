"""Sofer's hostile probe of stage 6: the three files mutated at random (a value replaced, a key or a row dropped, one added or
doubled, the text cut or made not JSON), each variant through the checker and, where it holds, the load and the contraction.
A raise anywhere is a finding: the checker and the load name every departure, they raise none.
usage: python -I fuzz_files.py <worktree> <variants> <seed>"""
import copy, json, random, sys, tempfile, traceback
from collections import Counter
from pathlib import Path

WT, N, SEED = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
sys.path[:0] = [WT + "/src", WT]
import numpy as np  # noqa: E402

from tensor24.engine.contract import Plan, contract  # noqa: E402
from tensor24.main import made  # noqa: E402
from tensor24.runner.files import departures, sites_of  # noqa: E402
from tensor24.runner.load import load  # noqa: E402
from tests.test_the_tensor24_load import COUPLINGS, TRAINS  # noqa: E402

held, c = made((3, 3, 3))
trains = []
for t in TRAINS:
    t = dict(t)
    t["pinion"] = 2 if t["part"] == 1 else 3
    if t["part"] > 1:
        t["sine"] = 4
    trains.append(t)
U = {"version": 1, "integers": {"den": 5, "full_rate": 1000, "key": 36000, "trace": 6, "width": 128}, "trains": trains,
     "couplings": copy.deepcopy(COUPLINGS)}
P = {"version": 1, "shape": [2, 2, 2]}
S = {"version": 1, "ticks": 3, "gears": [[0, 1, 3, 5, 6, 0], [1, 0, 2, 7, 8, 0], [4, 2, 5, -9, 10, 1]]}

POOL = [None, True, False, -1, 0, 1, 2, 3, 4, 5, 7, 10**30, -(10**30), 1.5, 0.0, "x", "", [], {}, [1], [[1]], {"a": 1},
        float("nan"), 2**200, -2, 99, "A1", "T1"]


def paths(node, prefix=()):
    out = [prefix]
    if isinstance(node, dict):
        for k, v in node.items():
            out += paths(v, prefix + (k,))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            out += paths(v, prefix + (i,))
    return out


def get(root, path):
    for p in path:
        root = root[p]
    return root


def mutate(doc, rng):
    doc = copy.deepcopy(doc)
    for _ in range(rng.choice((1, 1, 1, 2, 3))):
        ps = [p for p in paths(doc) if p]
        if not ps:
            break
        p = rng.choice(ps)
        parent, key = get(doc, p[:-1]), p[-1]
        op = rng.choice(("set", "set", "set", "del", "dup", "add"))
        if op == "set":
            parent[key] = copy.deepcopy(rng.choice(POOL))
        elif op == "del":
            del parent[key]
        elif op == "dup" and isinstance(parent, list):
            parent.insert(key, copy.deepcopy(parent[key]))
        elif op == "add" and isinstance(parent, dict):
            parent["extra"] = copy.deepcopy(rng.choice(POOL))
        elif op == "add" and isinstance(parent, list):
            parent.append(copy.deepcopy(rng.choice(POOL)))
    return doc


def text_of(doc, rng):
    s = json.dumps(doc)
    r = rng.random()
    if r < 0.03:
        return s[: rng.randrange(1, len(s))]
    if r < 0.05:
        return s.replace("1", "1, 1", 1)
    if r < 0.06:
        return "[" * 100000 + "]" * 100000
    if r < 0.07:
        return s.replace("}", ', "version": 1}', 1)
    if r < 0.08:
        return s[:-1] + ', "big": ' + "9" * 5000 + "}"
    return s


rng = random.Random(SEED)
raised_check, raised_load, raised_contract = Counter(), Counter(), Counter()
accepted = refused_load = loaded_ok = 0
samples = {}
with tempfile.TemporaryDirectory() as d:
    d = Path(d)
    for n in range(N):
        docs = {"universe": U, "piece": P, "setting": S}
        which = rng.choice(("universe", "universe", "setting", "piece"))
        docs = {k: (mutate(v, rng) if k == which else v) for k, v in docs.items()}
        paths_ = {}
        for k, v in docs.items():
            f = d / f"{k}.json"
            f.write_text(text_of(v, rng) if k == which else json.dumps(v), encoding="utf-8")
            paths_[k] = f
        try:
            found = departures(paths_["universe"], paths_["piece"], paths_["setting"])
        except BaseException as e:  # noqa: BLE001
            key = f"{type(e).__name__}: {str(e)[:90]}"
            raised_check[key] += 1
            samples.setdefault(("check", key), (which, traceback.format_exc().splitlines()[-4:]))
            continue
        if found:
            continue
        accepted += 1
        u, p, s = (json.loads(paths_[k].read_text(encoding="utf-8")) for k in ("universe", "piece", "setting"))
        try:
            got, named = load(u, s, sites_of(p["shape"]), held, c)
        except BaseException as e:  # noqa: BLE001
            key = f"{type(e).__name__}: {str(e)[:90]}"
            raised_load[key] += 1
            samples.setdefault(("load", key), (which, traceback.format_exc().splitlines()[-4:]))
            continue
        if named or got is None:
            refused_load += 1
            continue
        loaded_ok += 1
        try:
            rows = sum(t.rows() for t in got.trains)
            readings = np.arange(7 * rows * sites_of(p["shape"]), dtype=object).reshape(7 * rows, -1)
            contract(Plan(*got.plan), readings)
        except BaseException as e:  # noqa: BLE001
            key = f"{type(e).__name__}: {str(e)[:90]}"
            raised_contract[key] += 1
            samples.setdefault(("contract", key), (which, traceback.format_exc().splitlines()[-4:]))

print(f"variants {N}: held by the checker {accepted}; of those the load named a departure in {refused_load} and loaded {loaded_ok}")
print("raised in the checker:", dict(raised_check))
print("raised in the load:", dict(raised_load))
print("raised in the contraction:", dict(raised_contract))
for k, v in samples.items():
    print("sample", k, v)
