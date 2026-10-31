"""The form of the owner's law of 11:52 UTC ("The connection between two places comes, for certain, from the start and
from the end"; the Boss's 6543015767 and 6543120369 item 4, first on Big Pic's order of work), read under the square
form with David's cell rule (6542967229 item 3: a held hand carries one cell, h times the sum of what it ties).
Two ways to weigh the pair's two clicks under the square form, every weight the square of its cell's value:
  (one)  one cell over what the pair's source ties: the sum over the source's two states e_k of the plane of
         (a . e_k)(e_k . b), with a and b the two ends' readings (each its setting, along or across); its square, over
         the source's equal split, is the joint weight;
  (per)  one cell per state: the sum over k of the squares ((a . e_k)(e_k . b))^2, each over the same split: a hand
         born along e_k or across it, each end taking its own share of it, the local act.
Read exactly, in whole numbers and Rule3's carry, nothing drawn:
  - the identity under (one): the sum over k of (a . e_k)(e_k . b), each over (e_k . e_k), equals a . b, so the cell is
    the plane's own unit form between the two ends and holds no hand; checked on every lattice a, b and basis;
  - (one) against bellend.py's end law, the ends weighed 1 : 1: the joint counts as fractions, alike or not, at the
    triangle's settings and at the powers of z = 13 + 5 w;
  - CHSH under (one) and under (per) for every basis of the plane's lattice lines, and each wing's +1 share.
Usage: python3 -I onecell.py <src>
"""
import contextlib
import io
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
with contextlib.redirect_stdout(io.StringIO()):
    import bellend  # noqa: E402  (its law and its lattice are reused; its own readings stay in bellend.txt)

DIRS = bellend.DIRS
dot, across, direction = bellend.dot, bellend.across, bellend.direction


def reading(v, o):
    """An end's reading direction: its setting for +1, the setting turned a quarter for -1."""
    return v if o == 1 else across(v)


def one_cell(a, b):
    """Joint weights N[(oA, oB)] = (a_o . b_o)^2 over (a_o . a_o)(b_o . b_o), the source's split one each way,
    scaled to one whole denominator."""
    parts = {}
    for oa in (1, -1):
        for ob in (1, -1):
            u, v = reading(a, oa), reading(b, ob)
            parts[(oa, ob)] = (dot(u, v) * dot(u, v), dot(u, u) * dot(v, v))
    common = 1
    for _, d in parts.values():
        common *= d
    return {k: n * carry(common, d, 0)[0] for k, (n, d) in parts.items()}


def per_state(a, b, e):
    """Joint weights under one cell per state: the hand along e or across it, each end its own share of it."""
    parts = {}
    for oa in (1, -1):
        for ob in (1, -1):
            u, v = reading(a, oa), reading(b, ob)
            terms = []
            for k in (e, across(e)):
                sa_n, sa_d = bellend.share(k, u)
                sb_n, sb_d = bellend.share(k, v)
                terms.append((sa_n * sb_n, sa_d * sb_d))
            n = terms[0][0] * terms[1][1] + terms[1][0] * terms[0][1]
            parts[(oa, ob)] = (n, terms[0][1] * terms[1][1])
    common = 1
    for _, d in parts.values():
        common *= d
    return {k: n * carry(common, d, 0)[0] for k, (n, d) in parts.items()}


def same(c1, c2):
    """Two joint counts alike as fractions."""
    t1, t2 = sum(c1.values()), sum(c2.values())
    return all(c1[k] * t2 == c2[k] * t1 for k in c1)


def chsh(rule, pairs):
    num, den = 0, 1
    for (a, b), sign in pairs:
        n, d = bellend.corr(rule(a, b))
        num, den = num * d + sign * n * den, den * d
    return num, den


print("== onecell.py", flush=True)
# the identity: the cell over the source's two states is the plane's own unit form, the hand summed out
held = total = 0
lattice = [bellend.eis_vec((m, n)) for m in range(-3, 4) for n in range(-3, 4) if (m, n) != (0, 0)]
for e in DIRS:
    f = across(e)
    for a in lattice:
        for b in lattice:
            total += 1
            left = dot(a, e) * dot(e, b) * dot(f, f) + dot(a, f) * dot(f, b) * dot(e, e)
            held += left == dot(a, b) * dot(e, e) * dot(f, f)
print(f"the identity, the sum over the source's two states of (a . e_k)(e_k . b) over (e_k . e_k) = a . b: {held} of"
      f" {total} (lattice a, b with |m|, |n| at most 3; the six bases of lattice lines)", flush=True)
sets = [((direction(ua), direction(ub)), sign) for (ua, ub), sign in bellend.SETS.items()]
zs = [bellend.eis_vec(p) for p in bellend.powers]
zsets = [((zs[ka], zs[kb]), sign) for (ka, kb), sign in {(0, 1): 1, (0, 3): -1, (2, 1): 1, (2, 3): 1}.items()]
alike = sum(same(one_cell(a, b), bellend.end_law_on(a, b, 1, 1)) for (a, b), _ in sets + zsets)
print(f"the one cell against the end law (the ends weighed 1 : 1), joint counts alike as fractions: {alike} of"
      f" {len(sets) + len(zsets)} setting pairs", flush=True)
for name, group in (("the triangle's settings", sets), ("the powers of z", zsets)):
    n, d = chsh(one_cell, group)
    worst = None
    for e in DIRS:
        pn, pd = chsh(lambda a, b, e=e: per_state(a, b, e), group)
        q = bellend.per_mille(pn, pd)
        worst = q if worst is None or q > worst else worst
    print(f"{name}: CHSH under the one cell {bellend.per_mille(n, d)} per mille; under one cell per state, the largest"
          f" over the six bases {worst} per mille (2 is 2000)", flush=True)
signal = 0
for (a, b), _ in sets + zsets:
    c = one_cell(a, b)
    t = sum(c.values())
    signal += (c[(1, 1)] + c[(1, -1)]) * 2 != t or (c[(1, 1)] + c[(-1, 1)]) * 2 != t
print(f"each wing's +1 share exactly half under the one cell: {len(sets) + len(zsets) - signal} of"
      f" {len(sets) + len(zsets)} setting pairs (no signal)", flush=True)
print("exit", flush=True)
