"""lr1: the 48 on the clicks of the chiral 3-cube to N through the reflected FILES (every signed permutation of the axes on the seed's Nodes) and through the C P mirror STATE (the base laid, then every level by the sign table and every odd line's remainder W - 1 - r, stepped beside), on a named src with the flags from the environment: rotations equal, reflections the conjugate (children exchanged, senses negated), the first apart interval. Usage: run_48_lr1.py <src> <worktree> <N> <out.json> [world.json cube]"""
import itertools
import json
import os
import sys
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, sys.argv[1])
sys.set_int_max_str_digits(0)
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.rows import CARRIER, PLANE, POTENTIAL  # noqa: E402

root, N = sys.argv[2], int(sys.argv[3])
if len(sys.argv) > 5:
    universe, world = load_world(sys.argv[5])
    CUBE = int(sys.argv[6])
    world = dict(world, intervals=N)
else:
    universe, world = load_world(root + "/tests/worlds/world_node.json")
    lays = [{"lay": "sea", "row": 0}, {"lay": "hole", "at": [0, 0, 0]}]
    lays += [{"lay": "at", "row": 0, "centre": c, "quanta": 1} for c in ([1, 0, 0], [0, 2, 1], [2, 1, 0])]
    world = dict(world, shape=[3, 3, 3], intervals=N, seed=lays)
    CUBE = 3
IMAGES = [np.array([[s[a] if pi[a] == b else 0 for a in range(3)] for b in range(3)]) for pi in itertools.permutations(range(3)) for s in itertools.product((1, -1), repeat=3)]


def det_of(m):
    pi = [int(np.nonzero(m[:, a])[0][0]) for a in range(3)]
    signs = [int(m[pi[a], a]) for a in range(3)]
    inv = sum(1 for a in range(3) for b in range(a + 1, 3) if pi[a] > pi[b])
    return (-1) ** inv * signs[0] * signs[1] * signs[2]


def image(m, node):
    return tuple(int(x) % CUBE for x in m @ np.array(node, dtype=int))


def world_image(w, m):
    found = dict(w, seed=[dict(lay) for lay in w["seed"]])
    for lay in found["seed"]:
        for key in ("at", "centre"):
            if key in lay:
                lay[key] = list(image(m, lay[key]))
    return found


def line_signs(node, m):
    """Every line's image line and sign under m (a48b's sign table): the shape-4 row's lines 1..3 an axial vector (det s_a, permuted), the carrier's axis lines permuted even, a plane's im line and the shape-4 row's time line det, every other line even."""
    pi = [int(np.nonzero(m[:, a])[0][0]) for a in range(3)]
    signs = [int(m[pi[a], a]) for a in range(3)]
    det = det_of(m)
    found = []
    li = 0
    for r in node.rows_:
        for k in range(len(r.lines)):
            if r.shape == POTENTIAL and 1 <= k <= 3:
                found.append((li - (k - 1) + pi[k - 1], det * signs[k - 1]))
            elif r.shape == CARRIER and 1 <= k <= 3:
                found.append((li - (k - 1) + pi[k - 1], 1))
            elif (r.shape == PLANE and k == 1) or (r.shape == POTENTIAL and k == 0):
                found.append((li, det))
            elif r.shape == 1 and os.environ.get("LR1_WALLED_ODD") == "1":
                found.append((li, det))  # the walled row's level odd (its flux the time line's), its remainder (the turn parity bit) kept
            else:
                found.append((li, 1))
            li += 1
    return found


def mirror_state(base, m):
    """The C P image of a laid state: out[g x] = s * level[x]; the odd line's remainder W - 1 - r (and its write remainder), the even line's kept."""
    img = Node(json.loads(json.dumps(universe)), world_image(world, m))
    lb, li_ = base.all_lines(), img.all_lines()
    table = line_signs(base, m)
    for li, (lj, s) in enumerate(table):
        src, dst = lb[li], li_[lj]
        for name in ("now", "before", "rem", "wr"):
            a = getattr(src, name)
            if a is None:
                continue
            wall = src.wall if name == "rem" else src.wwall
            out = np.array(getattr(dst, name), dtype=object)
            for x in np.ndindex(*base.shape):
                v = int(a[x])
                if name in ("now", "before"):
                    out[image(m, x)] = s * v
                else:
                    w = int(wall[x]) if isinstance(wall, np.ndarray) else int(wall)
                    out[image(m, x)] = (w - 1 - v) if s == -1 and w != 2 else v
            setattr(dst, name, out)
    return img


def clicks(log, m, conj):
    births = sorted((e["i"], image(m, e["node"]), e["line_pair"]) + ((image(m, e["plus"]), image(m, e["minus"])) if conj else (image(m, e["minus"]), image(m, e["plus"]))) for e in log if e["event"] == "birth")
    credits = sorted((e["i"], image(m, e["node"]), e["line"], -e["sense"] if conj else e["sense"], e["beat"]) for e in log if e["event"] == "credit")
    return births, credits


def first_apart(a, b):
    apart = sorted((set(a[0]) ^ set(b[0])) | (set(a[1]) ^ set(b[1])), key=lambda x: x[0])
    return None if not apart else apart[0][0]


def run_node(node):
    for _ in range(N):
        node.step()
    return node.log


def one(k):
    try:
        return one_(k)
    except Exception as err:  # the failing image named, the rest measured
        return {"k": k, "m": IMAGES[k].tolist(), "det": det_of(IMAGES[k]), "file_apart": "error " + repr(err)[:80], "state_apart": "error", "births": 0, "credits": 0}


def one_(k):
    m = IMAGES[k]
    det = det_of(m)
    eye = np.eye(3, dtype=int)
    base = Node(json.loads(json.dumps(universe)), world)
    want = clicks(run_node(Node(json.loads(json.dumps(universe)), world)), m, det == -1)
    by_file = clicks(run_node(Node(json.loads(json.dumps(universe)), world_image(world, m))), eye, False)
    by_state = clicks(run_node(mirror_state(base, m)), eye, False)
    return {"k": k, "m": m.tolist(), "det": det, "file_apart": first_apart(by_file, want), "state_apart": first_apart(by_state, want), "births": len(want[0]), "credits": len(want[1])}


if __name__ == "__main__":
    os.nice(19)
    with Pool(int(os.environ.get("LR1_POOL", "8"))) as pool:
        rows = pool.map(one, range(len(IMAGES)))
    summary = {"N": N, "cube": CUBE, "flags": {k: os.environ.get(k) for k in ("LR1_PICK", "LR1_LAY")}}
    for way in ("file", "state"):
        rot = [r for r in rows if r["det"] == 1]
        ref = [r for r in rows if r["det"] == -1]
        summary[way] = {
            "rotations equal": sum(1 for r in rot if r[way + "_apart"] is None),
            "reflections conjugate": sum(1 for r in ref if r[way + "_apart"] is None),
            "apart": sum(1 for r in rows if r[way + "_apart"] is not None),
            "first apart intervals": sorted({r[way + "_apart"] for r in rows if isinstance(r[way + "_apart"], int)}),
        }
    print(json.dumps(summary)); print("errors", [r["k"] for r in rows if isinstance(r["file_apart"], str)])
    with open(sys.argv[4], "w", encoding="utf-8") as f:
        json.dump({"summary": summary, "rows": rows}, f)
