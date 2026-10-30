"""The whole click on the Node-clock's own act: what the coupling moves, what the click counts, and what it writes back."""

# The world: one Node-clock with no Mesh, two families of two parts each, a giver L and a taker M, each a T1 hand of
# three components with a re part and an im part (twelve gears). One potential, through the 24's table of T1 with T1
# onto A1 (the dot product), gives every push by the head's own contraction (engine/contract.py, term 6):
#   V = f (L.L + M.M) + g Re(conj(M) . L),   L.L = Lre . Lre + Lim . Lim,   Re(conj(M) . L) = Mre . Lre + Mim . Lim.
# f is each hand's own spring, g the vertex between them; V is unchanged when both hands turn alike in their re-im
# plane, so the two hands' swept areas move only into each other.
# A hand's swept area is Omega = SUM_i (re_i p_im,i - im_i p_re,i) through the same table, p = W (a - b) + r its
# stride with its kept tooth. On the head's step it moves each round by exactly
#   (re F_im - im F_re) + (q_re r+_im - q_im r+_re),
# the push's turn and Rule3's turn, with q the quotient and r+ the tooth kept (David's c2 identity).
# The whole click (term 11): the area the coupling moves into the taker in a round, tau, carried at the key:
#   q_c, k+ = carry(tau, key, k),
# its kept tooth k born at the half key, key div 2, as every remainder is born at the half teeth count (ALGEBRA.md, The
# one rule of the remainder, (i)).
# The strengths and the key are the probe's, set by hand (decision 35: on the act they are the law's, G3 and the
# train card).

import functools
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "src"))

from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.state import Gearing, Layout, Plan, Read, State  # noqa: E402
from tensor24.main import made  # noqa: E402
from tensor24.runner import load as loading  # noqa: E402

PLANES, ROWS = 1 + 3 + 1, 12  # the readings' planes; twelve gears
UNIT = PLANES * ROWS  # the unit, the readings' last row
LRE, LIM, MRE, MIM = 0, 3, 6, 9  # each part's first gear: three components each
W = 10**20  # the teeth at rest
F = W // 800  # each hand's own spring: a beat of about 2 pi 20 rounds
A = 10**6  # the giver's swing
ROUNDS = 6000


@functools.cache
def table() -> tuple[tuple[int, int, int], ...]:
    """The 24's table of T1 with T1 onto A1, derived once from the star: its nonzero entries (entry, j, i)."""
    kinds, tables, _ = made(loading.star(3))
    labels = [name.upper() for name in kinds._fields]
    t = tables[(labels.index("T1"), labels.index("T1"), labels.index("A1"))][0]
    return tuple((int(t[j, i]), int(j), int(i)) for j, i in np.argwhere(t))


def dot(one: int, two: int) -> list[tuple[int, int, int]]:
    """The table between two parts, as (entry, row, row)."""
    return [(e, one + j, two + i) for e, j, i in table()]


def potential(g: int) -> list[tuple[int, tuple[int, ...]]]:
    """V = f (L.L + M.M) + g (Mre . Lre + Mim . Lim), as whole factors on their legs."""
    own = [(F * e, (j, i)) for part in (LRE, LIM, MRE, MIM) for e, j, i in dot(part, part)]
    vertex = [(g * e, (j, i)) for one, two in ((MRE, LRE), (MIM, LIM)) for e, j, i in dot(one, two)]
    return own + vertex


def plan(monomials: list[tuple[int, tuple[int, ...]]]) -> Plan:
    """J's terms from one potential, as the head's test builds them: each monomial pushes every leg by minus its
    factor times its other legs, the unit standing for each leg it lacks of three."""
    terms = []
    for factor, legs in monomials:
        for p, leg in enumerate(legs):
            terms.append(((*legs[:p], *legs[p + 1 :], UNIT, UNIT, UNIT)[:3], -factor, leg))
    readings, factor, target = zip(*terms, strict=True)
    return Plan(
        *(np.array(x, dtype=np.intp) for x in zip(*readings, strict=True)),
        np.array(factor, dtype=object),
        np.array(target, dtype=np.intp),
    )


def node(g: int) -> Layout:
    """One Node-clock whose neighbours are itself, so no Mesh pulls it, on the force's path, J from the potential."""
    nb = np.zeros((6, 1), dtype=np.intp)
    spokes = np.array([s * axis for axis in np.eye(3, dtype=int) for s in (1, -1)], dtype=object)
    meshes = (np.arange(6) // 2)[:, None]
    none = np.zeros(0, dtype=np.intp)
    unread = Read(none, none.astype(object), none)
    ones = np.ones((1, 1), dtype=object)
    return Layout(
        nb,
        spokes,
        meshes,
        ones.repeat(3, axis=1),
        Gearing(W * ones, 1, 1, 1),
        plan(potential(g)),
        unread,
        unread,
    )


def swept(re: int, im: int, a, p) -> int:
    """A hand's swept area through the table: SUM re_j p_im,i - im_j p_re,i."""
    return sum(e * (a[j] * p[im + i - re] - a[im + j - re] * p[i]) for e, j, i in dot(re, re))


def stride(s: State) -> list[int]:
    """Every gear's stride with its kept tooth, p = W (a - b) + r."""
    return [W * (x - y) + r for x, y, r in zip(s.a[:, 0], s.b[:, 0], s.r[:, 0], strict=True)]


def moved(s: State, j: list[int], re: int) -> int:
    """The area the push moves into a hand in a round: SUM re_j J_im,i - im_j J_re,i through the table."""
    a = s.a[:, 0]
    return sum(e * (a[x] * j[re + 3 + i - re] - a[re + 3 + x - re] * j[i]) for e, x, i in dot(re, re))


def turned_rule3(before: State, after: State, re: int) -> int:
    """Rule3's turn on a hand in a round: SUM q_re r+_im - q_im r+_re, q the quotient, r+ the tooth kept."""
    q = [x - y for x, y in zip(after.a[:, 0], before.a[:, 0], strict=True)]
    r = after.r[:, 0]
    return sum(e * (q[x] * r[re + 3 + i - re] - q[re + 3 + x - re] * r[i]) for e, x, i in dot(re, re))


def lay(axes: tuple[int, ...] = (0,)) -> State:
    """The giver turning in its re-im plane along the axes given, the taker at rest: re at the swing, im moving."""
    a = np.zeros((ROWS, 1), dtype=object)
    b = np.zeros((ROWS, 1), dtype=object)
    for axis in axes:
        a[LRE + axis, 0], b[LRE + axis, 0] = A, A
        a[LIM + axis, 0], b[LIM + axis, 0] = 0, -A // 20
    return State(a, b, 0 * a, 0 * a)


def turn(s: State, m: np.ndarray) -> State:
    """A turn of the 24 on every part's three components: a gear sent to minus a gear has its fine tooth flipped in its
    teeth (W - 1 - r), as the mirror flips it, so that the carry of the negated sum is the negated carry."""
    a, b, r = s.a.copy(), s.b.copy(), s.r.copy()
    for part in (LRE, LIM, MRE, MIM):
        for i in range(3):
            j = int(np.flatnonzero(m[i])[0])
            sign = int(m[i, j])
            a[part + i, 0], b[part + i, 0] = sign * s.a[part + j, 0], sign * s.b[part + j, 0]
            r[part + i, 0] = s.r[part + j, 0] if sign > 0 else W - 1 - s.r[part + j, 0]
    return State(a, b, r, s.rd)


def run(g: int, start: State, key: int, rounds: int = ROUNDS, mutant: str = "") -> dict:
    """Step the act and read the click each round: the area moved into the taker carried at the key.

    mutant "take": the click also shrinks the giver along itself by the clicked keys (a write at the click);
    mutant "zero": the click's tooth born at 0 and not at the half key.
    Beside the train's click, each component's own area carried alone (a gear's click, the rows' record)."""
    y, s = node(g), start
    half = 0 if mutant == "zero" else key // 2
    k, krow = half, [half, half, half]
    rec = {
        "q": [],
        "k": [],
        "tau": [],
        "om_l": [],
        "om_m": [],
        "t_l": [],
        "t_m": [],
        "rows": [],
        "states": [s],
    }
    for _ in range(rounds):
        _, j = step.sources(y, s.a)
        jj = list(j[:, 0])
        p = stride(s)
        om_l, om_m = swept(LRE, LIM, s.a[:, 0], p), swept(MRE, MIM, s.a[:, 0], p)
        tau = moved(s, jj, MRE)
        nxt = step.tick(y, s)
        q, k = carry(tau, key, k)
        per = [
            e * (s.a[x, 0] * jj[MIM + i - MRE] - s.a[MIM + x - MRE, 0] * jj[i])
            for e, x, i in dot(MRE, MRE)
        ]
        qs = []
        for c in range(3):
            qr, krow[c] = carry(per[c], key, krow[c])
            qs.append(qr)
        if mutant == "take" and q:
            # the giver's now and before shrink along themselves so its swept area drops by q keys more
            pn = stride(nxt)
            om = swept(LRE, LIM, nxt.a[:, 0], pn)
            a, b = nxt.a.copy(), nxt.b.copy()
            for row in range(LRE, LIM + 3):
                a[row, 0] -= (a[row, 0] * q * key) // (2 * om)
                b[row, 0] -= (b[row, 0] * q * key) // (2 * om)
            nxt = State(a, b, nxt.r, nxt.rd)
        rec["q"].append(q)
        rec["k"].append(k)
        rec["tau"].append(tau)
        rec["om_l"].append(om_l)
        rec["om_m"].append(om_m)
        rec["t_l"].append(turned_rule3(s, nxt, LRE))
        rec["t_m"].append(turned_rule3(s, nxt, MRE))
        rec["rows"].append(qs)
        s = nxt
        rec["states"].append(s)
    p = stride(s)
    rec["om_l"].append(swept(LRE, LIM, s.a[:, 0], p))
    rec["om_m"].append(swept(MRE, MIM, s.a[:, 0], p))
    return rec


def same(x: State, y: State) -> bool:
    return all(np.array_equal(u, v) for u, v in zip(x, y, strict=True))
