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


def main() -> None:
    g = (
        F // 10
    )  # the vertex: the two hands' beats part by about a twentieth, a whole exchange in about 2,500 rounds
    start = lay()
    om0 = swept(LRE, LIM, start.a[:, 0], stride(start))
    key = om0 // 7  # the probe's key: the giver holds seven keys and a little more
    print(f"W = {W}, f = {F} (a beat of about 2 pi 20 rounds), g = {g}, the giver's swing A = {A}")
    print(f"the giver's swept area at the lay {om0}, the key {key} ({om0 / key:.4f} keys)")
    rec = run(g, start, key)
    n = len(rec["q"])

    print("\n1. The coupling moves the swept area between the two hands and nowhere else.")
    bad = [
        t
        for t in range(n)
        if (rec["om_l"][t + 1] - rec["om_l"][t]) + (rec["om_m"][t + 1] - rec["om_m"][t])
        != rec["t_l"][t] + rec["t_m"][t]
    ]
    each = [t for t in range(n) if rec["om_m"][t + 1] - rec["om_m"][t] != rec["tau"][t] + rec["t_m"][t]]
    print(f"   rounds where the two areas' change is not Rule3's two turns: {len(bad)} of {n}")
    print(
        f"   rounds where the taker's change is not the area moved plus its Rule3 turn: {len(each)} of {n}"
    )
    print(
        f"   Rule3's turn on both hands: largest in a round {max(abs(a + b) for a, b in zip(rec['t_l'], rec['t_m'], strict=True))}, "
        f"summed over the run {sum(rec['t_l']) + sum(rec['t_m'])} ({(sum(rec['t_l']) + sum(rec['t_m'])) / key:.2e} keys)"
    )

    print("\n2. The click: the area moved into the taker, carried at the key.")
    books = [key * sum(rec["q"][: t + 1]) + rec["k"][t] - key // 2 for t in range(n)]
    board = [sum(rec["tau"][: t + 1]) for t in range(n)]
    print(
        f"   rounds where key x clicks + (kept - key div 2) != the area moved: "
        f"{sum(1 for x, y in zip(books, board, strict=True) if x != y)} of {n}"
    )
    held = [rec["om_m"][t + 1] - rec["om_m"][0] - sum(rec["t_m"][: t + 1]) for t in range(n)]
    print(
        f"   rounds where key x clicks + (kept - key div 2) != the taker's area less its Rule3 turns: "
        f"{sum(1 for x, y in zip(books, held, strict=True) if x != y)} of {n}"
    )
    clicks = [(t, q) for t, q in enumerate(rec["q"]) if q]
    print(
        f"   clicks: {len(clicks)}, {sum(1 for _, q in clicks if q > 0)} taken (+1) and {sum(1 for _, q in clicks if q < 0)} given back (-1)"
    )
    print(f"   the rounds and signs: {clicks}")
    count = np.cumsum(rec["q"])
    print(
        f"   the taker's area at its most: {max(rec['om_m']) / key:.4f} keys; the clicks' count from {min(count)} to "
        f"{max(count)}; |the area moved, in keys, less the count| at most "
        f"{max(abs(x / key - c) for x, c in zip(board, count, strict=True)):.4f}"
    )

    print("\n3. The energy a click carries: the key times the hand's own beat (E = n h nu per mode).")

    def energy(s: State, re: int) -> int:
        """2 W times a hand's energy: its strides squared and its spring, f a^2 per gear, times 2 W."""
        p = stride(s)
        return sum(p[x] * p[x] for x in range(re, re + 6)) + 2 * W * F * sum(
            s.a[x, 0] ** 2 for x in range(re, re + 6)
        )

    e0 = energy(start, MRE)
    ratios = [(t, (energy(rec["states"][t + 1], MRE) - e0) / (2 * W * board[t])) for t, _ in clicks[:7]]
    print(
        "   the taker's energy gained over its area gained, at each of its first seven clicks: "
        + ", ".join(f"{r:.5f}" for _, r in ratios)
        + f"; its beat sqrt(2 f / W) = {(2 * F / W) ** 0.5:.5f}. So a quantum, one key of area, carries key x beat."
    )

    print("\n4. The click writes nothing into the gears, so the run back is the act's own.")
    s = rec["states"][-1]
    y = node(g)
    back, k = [], rec["k"][-1]
    for t in range(n - 1, -1, -1):
        s = step.untick(y, s)
        _, j = step.sources(y, s.a)
        tau = moved(s, list(j[:, 0]), MRE)
        k = k + key * rec["q"][t] - tau
        back.append(same(s, rec["states"][t]))
    print(
        f"   rounds run back to their way out's state: {sum(back)} of {n}; the click's kept tooth back at its birth, "
        f"key div 2: {k == key // 2}"
    )

    print(
        "\n5. The 24: every turn of the cube on the lay, the run turned state for state, the clicks alike."
    )
    import itertools

    turns = []
    for order, signs in itertools.product(
        itertools.permutations(range(3)), itertools.product((1, -1), repeat=3)
    ):
        m = np.zeros((3, 3), dtype=int)
        m[range(3), order] = signs
        if round(np.linalg.det(m)) == 1:
            turns.append(m)
    alike_states = alike_clicks = 0
    for m in turns:
        other = run(g, turn(start, m), key, rounds=1500)
        alike_states += all(
            same(x, turn(y, m)) for x, y in zip(other["states"], rec["states"][:1501], strict=True)
        )
        alike_clicks += other["q"] == rec["q"][:1500] and other["k"] == rec["k"][:1500]
    print(
        f"   turns: {len(turns)}; runs turned state for state over 1,500 rounds: {alike_states}; "
        f"clicks and kept teeth alike in every round: {alike_clicks}"
    )

    print("\n6. Free light: no vertex, so no area moves and nothing clicks (The light no bob).")
    free = run(0, start, key)
    print(
        f"   area moved over the run: {sum(free['tau'])}; clicks: {sum(1 for q in free['q'] if q)}; the giver's area "
        f"moved by {free['om_l'][-1] - free['om_l'][0]} = its Rule3 turns {sum(free['t_l'])}"
    )

    print("\n7. Mutants.")
    take = run(g, start, key, mutant="take")
    held_sum = [
        take["om_l"][t] + take["om_m"][t] - sum(take["t_l"][:t]) - sum(take["t_m"][:t])
        for t in range(len(take["q"]) + 1)
    ]
    jumps = [
        (t, take["q"][t], (held_sum[t + 1] - held_sum[t]) / key)
        for t in range(len(take["q"]))
        if take["q"][t]
    ][:3]
    print(
        "   a write at the click (the giver shrunk along itself by the clicked keys, way (b)'s write beside the vertex):"
    )
    print(
        "     at its first clicks (round, quanta, the two hands' area less Rule3's turns moved, in keys): "
        + ", ".join(f"({t}, {q}, {d:+.4f})" for t, q, d in jumps)
        + "; 0 at every click without the write: each quantum taken twice, once by the vertex and once by the write"
    )
    zero = run(g, start, key, mutant="zero")
    zc = [(t, q) for t, q in enumerate(zero["q"]) if q]
    dips = sum(1 for c in np.cumsum(zero["tau"]) if c < 0)
    print(
        f"   the click's tooth born at 0: clicks {len(zc)} against {len(clicks)}, the count from {min(np.cumsum(zero['q']))}; "
        f"the area moved into the taker dips below 0 in {dips} rounds, by at most "
        f"{-min(np.cumsum(zero['tau'])) / key:.4f} keys, and the record shows a click and its return there: "
        + ", ".join(f"({t}, {q:+d})" for t, q in zc if 2400 < t < 2600 or 1200 < t < 1300)
    )
    diag = run(g, lay((0, 1)), key)
    rows = [sum(c) for c in diag["rows"]]
    print(
        f"   a gear's click (each component carried alone), laid along x and y at once: the train's clicks "
        f"{sum(1 for q in diag['q'] if q)} (net {sum(diag['q'])}), the gears' {sum(1 for c in diag['rows'] for q in c if q)} "
        f"(net {sum(rows)}); rounds where they part: {sum(1 for x, y in zip(diag['q'], rows, strict=True) if x != y)}"
    )


if __name__ == "__main__":
    main()
