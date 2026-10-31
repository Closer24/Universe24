"""STOP1 section 2's structure probe: what plans.holding's one quartic rule lays, read on the tree's own loader.
(1) Each train's character flags as trains_of reads them: square, held, kept under the sign kind's twist, tied =
    kept x lit(apart) (apart: the gap to the held character).
(2) holding()'s live monomials grouped by the trains of their first pair (legs 1-2) and second pair (legs 3-4).
(3) The same line with the held hand's exemption lifted (tied' = kept): the monomials it adds, and their sum at whole
    points against hold f |k|^4 (the held hand's own quartic at HAT1's e = hold f).
(4) Every own square c_X c_X the tie's line could reach: the second pair is always a held row, so a tied train's
    own square is never laid; the held hand's own is cut by lit(apart) alone.
Usage: python -I structure.py <tree> <files dir>. Whole numbers only; Rule3's carry the one division.
"""

import json
import sys
from pathlib import Path

TREE, FILES = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(TREE.joinpath("src")))
import numpy as np  # noqa: E402

from tensor24 import main as tmain  # noqa: E402
from tensor24.algebra.carry import carry, lit  # noqa: E402
from tensor24.runner import load as loadmod  # noqa: E402
from tensor24.runner import plans  # noqa: E402
from tensor24.runner.files import sites_of, star  # noqa: E402

universe, piece, setting = (json.loads(FILES.joinpath(n + ".json").read_text(encoding="utf-8")) for n in ("universe", "piece", "setting"))
shape = piece["shape"]
kinds, c, square = tmain.made(star(len(shape)))
loaded, found = loadmod.load(universe, setting, sites_of(shape), kinds, c, square)
assert not found, found
trains = loaded.trains
labels, dims, reads = loadmod.vocabulary(kinds, square)
traces, _, squared, hand, twist = reads
kind, of, part = loadmod.entries(universe["trains"], labels)
member = np.eye(len(part), dtype=object)[of]
character = part[:, None] * (member.T @ traces[kind])
twisted = character * twist[None, :] - character
kept, _ = carry(1, (twisted * twisted).sum(axis=-1) + 1, 0)
off = character - hand
apart = (off * off).sum(axis=-1)
names = [t["name"] for t in universe["trains"]]
print("(1) the trains' flags (trains_of's lines):")
for t, n in enumerate(names):
    print(f"    {n}: kinds {universe['trains'][t]['kinds']} part {universe['trains'][t]['part']}; square {int(trains.square[t])}, "
          f"held {int(trains.held[t])}, kept under the twist {int(kept[t])}, gap to the held character {int(apart[t])}, "
          f"tied = kept x lit(gap) {int(trains.tied[t])}")
row, rof, _, _, _ = plans.rows_of(trains)
train_of = {int(r): int(t) for r, t in zip(row, rof)}
_, rest = loadmod.teeth(universe, star(len(shape)))
hold, gamma, spring = universe["chosen"]["hold"], universe["integers"]["full_rate"], universe["chosen"]["spring"]
f, _ = carry(rest, gamma, 0)


def groups(potential):
    factor, legs = potential
    out = {}
    for x, a, b, cc, d in zip(factor, *legs):
        if int(x) == 0:
            continue
        key = (tuple(sorted(set(names[train_of[int(y)]] for y in (a, b) if int(y) >= 0))) or ("unit",),
               tuple(sorted(set(names[train_of[int(y)]] for y in (cc, d) if int(y) >= 0))) or ("unit",))
        out.setdefault(key, []).append((int(x), (int(a), int(b), int(cc), int(d))))
    return out


built = plans.holding(trains, c, traces, rest, hold, gamma, spring)
print(f"(2) plans.holding's live monomials as built (hold {hold}, f = rest div Gamma = {f}, hold f = {hold * f}):")
for key, mons in sorted(groups(built).items()):
    print(f"    first pair on {key[0]}, second pair on {key[1]}: {len(mons)} monomials, factors {sorted(set(m[0] for m in mons))}")
import dataclasses  # noqa: E402
lifted = dataclasses.replace(trains, tied=kept)
more = plans.holding(lifted, c, traces, rest, hold, gamma, spring)
gb, gm = groups(built), groups(more)
print("(3) the same line with the held hand's exemption lifted (tied' = kept):")
for key in sorted(gm):
    if key not in gb or len(gm[key]) != len(gb[key]):
        print(f"    added: first pair on {key[0]}, second pair on {key[1]}: {len(gm[key]) - len(gb.get(key, []))} monomials, factors {sorted(set(m[0] for m in gm[key]))}")
# the added block's value at whole points against hold f |k|^4, the held rows read off the held flag
hrows = [r for r in sorted(train_of) if int(trains.held[train_of[r]])]
added = [m for key in gm for m in gm[key] if key not in gb]
for point in ((1, 1), (2, 3), (5, -7), (40, 0)):
    v = {r: p for r, p in zip(hrows, point)}
    total = sum(x * v[a] * v[b] * v[cc] * v[d] for x, (a, b, cc, d) in added)
    k2 = sum(p * p for p in point)
    print(f"    at k = {point}: the added monomials sum to {total}; hold f |k|^4 = {hold * f * k2 * k2}; alike {total == hold * f * k2 * k2}")
# (4) every own square the line reaches
own = [key for key in gb if key[0] == key[1]]
print("(4) own squares the line lays as built (first and second pair on one train):", own if own else "none")
print("    the second pair of every tie monomial is a held row:",
      all(int(trains.held[train_of[m[1][2]]]) and m[1][2] == m[1][3] for key, mons in gb.items() if key[1] != ("unit",) for m in mons))
