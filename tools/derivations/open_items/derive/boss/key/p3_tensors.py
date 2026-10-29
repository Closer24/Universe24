"""Probe 3: the tensors.  Do the 24, the kinds or the tables hold the key, or put any condition on it?

Derivation: runner/load.py builds the 24's kinds and the 125 tables from the board's axes alone (main.made(shape)
takes no file integer), the coupling plan from the tables and the file's strengths, and every coefficient in geared;
the key is read once there, in the time gear's drive teeth (T div 2) key.  A swept area Q = SUM Im(conj(a) b) is kept
by every signed permutation of sites and components, so the count n = 2 Q div key is a 24-invariant whole number at
every key.  So the tensors can put no condition on the key; the probe can fail if any other entry of the layout moves
with the key, or if the act's images under the 24 part at some key (odd, prime, 1, 2).

Checks, exact on the committed act:
  1. two layouts of one world at key 36,000 and at 72,000 (and 35,999, a prime, and 1): every array compared;
  2. the 24's images: for each of the 24 turns g (kinds.turns, weight 1), g acts on the board's sites (x -> g x mod 4)
     and on nothing else (A1 trains); tick(g s) = g tick(s) bit for bit for 6 rounds, on a world of light and matter
     with random strides and a time gear already moving, at the keys 36,000, 35,999, 36,001, 2 and 1.

usage: python3 -I p3_tensors.py   (about 30 s)
"""

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # this folder's rig.py
import numpy as np  # noqa: E402
import rig  # noqa: E402

from tensor24.engine import kinds as kinds_mod  # noqa: E402
from tensor24.engine.state import State  # noqa: E402

SHAPE = (4, 4, 4)
SITES = 64


def flat(x):
    """Every array of a nested record, as (path, array) pairs."""
    out = []
    if hasattr(x, "_fields"):
        for name, v in zip(x._fields, x, strict=True):
            out += [(f"{name}.{p}" if p else name, a) for p, a in flat(v)]
    elif isinstance(x, (tuple, list)):
        for i, v in enumerate(x):
            out += [(f"[{i}].{p}" if p else f"[{i}]", a) for p, a in flat(v)]
    else:
        out.append(("", np.asarray(x, dtype=object)))
    return out


def world(key, seed=1):
    rnd = random.Random(seed)
    laid = {}
    for site in range(SITES):
        a = rnd.randint(-900, 900)
        laid[(0, 0, site)] = (a, a - rnd.randint(-40, 40))
        m = rnd.randint(-900, 900)
        laid[(1, 0, site)] = (m, m - rnd.randint(-40, 40))
    return rig.built([rig.light(), rig.matter()], laid, SHAPE, rig.integers(key=key), drive_home=False)


def turns():
    matrix, weight = kinds_mod.turns(kinds_mod.axes(3))
    return [np.array(m, dtype=int) for m, w in zip(matrix, weight, strict=True) if w == 1]


def site_map(g):
    """The site each site goes to under g: (x, y, z) -> g (x, y, z) mod 4, site = (x sy + y) sz + z."""
    sx, sy, sz = SHAPE
    out = np.zeros(SITES, dtype=np.intp)
    for x in range(sx):
        for y in range(sy):
            for z in range(sz):
                v = g @ np.array([x, y, z])
                gx, gy, gz = (int(v[0]) % sx, int(v[1]) % sy, int(v[2]) % sz)
                out[(x * sy + y) * sz + z] = (gx * sy + gy) * sz + gz
    return out


def image(s, where):
    """The state turned: every per-site array moved along the site axis, value at site i landing at where[i]."""
    out = []
    for arr in s:
        new = np.empty_like(arr)
        new[:, where] = arr
        out.append(new)
    return State(*out)


def same(x, y):
    return all(
        np.array_equal(np.asarray(p, dtype=object), np.asarray(q, dtype=object))
        for p, q in zip(x, y, strict=True)
    )


def main():
    out = ["Probe 3: the tensors and the key (committed 7b act, 4 x 4 x 4)", ""]
    kinds, tables = rig.made(SHAPE)
    nonzero = sum(1 for t in tables.values() if t.any())
    out.append(
        f"1. the tables: {len(tables)} built from the axes alone (main.made takes no file integer), {nonzero} not zero"
    )
    base, _ = world(36000)
    for key in (72000, 35999, 1):
        other, _ = world(key)
        diffs = []
        for (p, a), (_, b) in zip(flat(base), flat(other), strict=True):
            if a.shape != b.shape or not np.array_equal(a, b):
                where = np.argwhere(a != b) if a.shape == b.shape else "shape"
                diffs.append(f"{p} at {where.tolist() if hasattr(where, 'tolist') else where}")
        out.append(f"   the layout at key {key} against 36,000: the entries that differ: {diffs}")
    td = int(base.gearing.drive[base.ruler.row, 0])
    out.append(
        f"   (the time gear's row is {base.ruler.row}; its drive teeth at 36,000: {td} = (T div 2) 36,000: {td == (rig.teeth() // 2) * 36000})"
    )
    out.append("")
    gs = turns()
    out.append(
        f"2. the 24's images: {len(gs)} turns; tick(g s) = g tick(s) for 6 rounds, light + matter + a moving time gear"
    )
    for key in (36000, 35999, 36001, 2, 1):
        L, s0 = world(key)
        for _ in range(3):  # let the time gear move off rest first
            s0 = rig.tick(L, s0)
        held = 0
        for g in gs:
            where = site_map(g)
            s, t = s0, image(s0, where)
            ok = True
            for _ in range(6):
                s, t = rig.tick(L, s), rig.tick(L, t)
                if not same(image(s, where), t):
                    ok = False
                    break
            held += ok
        out.append(
            f"   key {key}: {held} of {len(gs)} turns bit for bit (the time gear's count at the start {[int(x) for x in s0.a[L.ruler.row][:4]]}...)"
        )
    out.append("")
    out.append(
        "So the 24, the kinds and the tables hold no key and ask nothing of it: the key is one divisor, the great"
    )
    out.append("clock's drive teeth, and the images hold at every key, odd, prime and 1.")
    print("\n".join(out))


if __name__ == "__main__":
    main()
