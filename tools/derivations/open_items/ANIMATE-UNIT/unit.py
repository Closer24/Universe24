"""n's unit and the click's key (G3's open item 3) on the Node-clock's own act, in whole numbers alone.

Animate, 2026-10-30, for David's G3 list (DAVID-TENSOR24-G3.md, section 4, item (3)) and the Boss's term 11 (its key's
value OPEN at G3), on the owner's words to Animate: "Check with David which pieces you can complete" and "every step
from the clocks to the algebra to the physics in the clicks; think of the 24 operations". README.md beside it reads it.
Every division is Rule3's carry; nothing here holds a float, a root, a circular call, a random draw or a fraction.

Run: python3 tools/derivations/open_items/ANIMATE-UNIT/unit.py (about twenty seconds); its output is unit.txt.
"""

import importlib.util
import itertools
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "src"))

from tensor24.algebra.carry import carry, flip  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.state import Gearing, Layout, Plan, Read, State  # noqa: E402
from tensor24.main import made  # noqa: E402
from tensor24.runner import load as loading  # noqa: E402

SPEC = importlib.util.spec_from_file_location(
    "click", ROOT / "tools/derivations/open_items/ANIMATE-CLICK/click.py"
)
click = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(click)

KINDS, TABLES, _ = made(loading.star(3))
LABELS = [name.upper() for name in KINDS._fields]
ON = [g for g in range(KINDS.a1.shape[0]) if KINDS.a1[g, 0, 0] == 1]  # the 24, weighed 1 by Rule3
PLANES = 1 + 3 + 1  # the readings: the value, the three gradients, the force; the unit after them

# The two worlds' numbers. The teeth W = 13 Q and each count's own spring 2 F with F = Q, so that the step's
# 2 - 2 F / W is 2 x 12 / 13: a hand laid at (13 P, 0) now and (12 P, -5 P) before turns on a circle, the whole
# triple 5, 12, 13 standing for the beat's cosine and sine (no circular call is made). The tied family's spring
# 2 M R^2 is W / 400, its beat about a fifth of the held hand's own; the held count of G3 stands at n = R^2 with the
# same strength, G = M, so that both worlds give the tied family the one spring.
Q = 104 * 10**18
W = 13 * Q
F = Q
P = 1000
R = 13 * P
M = 10**10
G = M
N = R * R
A = 1000  # the tied family's swing, far below where it would move the held hand by a count
ROUNDS = 4000


def table(one: str, two: str) -> list[tuple[int, int, int]]:
    """The 24's table of two kinds onto A1, from the engine's own star: its nonzero entries (entry, j, i)."""
    t = TABLES[(LABELS.index(one), LABELS.index(two), LABELS.index("A1"))][0]
    return [(int(t[j, i]), int(j), int(i)) for j, i in np.argwhere(t)]


def plan(monomials: list[tuple[int, tuple[int, ...]]], unit: int) -> Plan:
    """Each monomial pushes every leg by minus its factor times its other legs, the unit for each leg it lacks of three."""
    terms = []
    for factor, legs in monomials:
        for p, leg in enumerate(legs):
            terms.append(((*legs[:p], *legs[p + 1 :], unit, unit, unit)[:3], -factor, leg))
    readings, factor, target = zip(*terms, strict=True)
    return Plan(
        *(np.array(x, dtype=np.intp) for x in zip(*readings, strict=True)),
        np.array(factor, dtype=object),
        np.array(target, dtype=np.intp),
    )


def node(monomials: list[tuple[int, tuple[int, ...]]], rows: int, teeth: int) -> Layout:
    """One Node-clock whose neighbours are itself, so no Mesh pulls it; the push is J from the one potential."""
    nb = np.zeros((6, 1), dtype=np.intp)
    spokes = np.array([s * axis for axis in np.eye(3, dtype=int) for s in (1, -1)], dtype=object)
    meshes, _ = carry(np.arange(6), 2, 0)
    meshes = meshes[:, None]
    none = np.zeros(0, dtype=np.intp)
    unread = Read(none, none.astype(object), none)
    ones = np.ones((1, 1), dtype=object)
    return Layout(
        nb,
        spokes,
        meshes,
        ones.repeat(3, axis=1),
        Gearing(teeth * ones, 1, 1, 1),
        plan(monomials, PLANES * rows),
        unread,
        unread,
    )


def laid(rows: int, gears: dict[int, tuple[int, int]]) -> State:
    """A state with the gears given at (now, before), every fine tooth at 0."""
    a = np.zeros((rows, 1), dtype=object)
    b = np.zeros((rows, 1), dtype=object)
    for row, (now, before) in gears.items():
        a[row, 0], b[row, 0] = now, before
    return State(a, b, 0 * a, 0 * a)


def area(s: State, re: list[int], im: list[int], tab: list[tuple[int, int, int]], teeth: int) -> int:
    """A two-part hand's swept area through the table: SUM t (re_j p_im,i - im_j p_re,i), p = W (a - b) + r."""
    a, b, r = s.a[:, 0], s.b[:, 0], s.r[:, 0]

    def p(x: int) -> int:
        return teeth * (a[x] - b[x]) + r[x]

    return sum(e * (a[re[j]] * p(im[i]) - a[im[j]] * p(re[i])) for e, j, i in tab)


def crossed(s: State, re: list[int], im: list[int], tab: list[tuple[int, int, int]]) -> int:
    """The counts' own cross of before and now through the table, X = SUM t (im_j re_b,i - re_j im_b,i): the area
    in whole counts, W X + (the fine teeth's cross) being the swept area."""
    a, b = s.a[:, 0], s.b[:, 0]
    return sum(e * (a[im[j]] * b[re[i]] - a[re[j]] * b[im[i]]) for e, j, i in tab)


def moved(s: State, j: list[int], re: list[int], im: list[int], tab: list[tuple[int, int, int]]) -> int:
    """The area the act's push moves into a hand in a round: SUM t (re_j J_im,i - im_j J_re,i), read at the now slot."""
    a = s.a[:, 0]
    return sum(e * (a[re[x]] * j[im[i]] - a[im[x]] * j[re[i]]) for e, x, i in tab)


def turned_rule3(before: State, after: State, re: list[int], im: list[int], tab) -> int:
    """Rule3's turn on a hand in a round: SUM t (q_re r+_im - q_im r+_re), q the quotient and r+ the tooth kept."""
    q = [x - y for x, y in zip(after.a[:, 0], before.a[:, 0], strict=True)]
    r = after.r[:, 0]
    return sum(e * (q[re[x]] * r[im[i]] - q[im[x]] * r[re[i]]) for e, x, i in tab)


def same(x: State, y: State) -> bool:
    return all(np.array_equal(u, v) for u, v in zip(x, y, strict=True))


def changes(xs: list[int]) -> int:
    """How often a count changes its sign, zeros skipped."""
    signs = [1 if x > 0 else -1 for x in xs if x != 0]
    return sum(1 for u, v in zip(signs, signs[1:], strict=False) if u != v)


def in_billionths(x: int, unit: int) -> str:
    """x over the unit in billionths, by one carry, with its sign."""
    q, _ = carry(abs(x) * 10**9, unit, 0)
    return f"{'-' if x < 0 else ''}{q} billionths"


# The standing count (G3's operation, 2.1): k one part of kind A1 at row 0; a tied family X of kind T1, two parts
#   V = G k (X . X) + H (k - n)^2, the constant H n^2 left out, H = F.
S_K, S_RE, S_IM, S_ROWS = 0, [1, 2, 3], [4, 5, 6], 7
# The turning count: K two parts of kind A1 at rows 0 and 1; the same tied family
#   V = F (K . K) + M (K . K)(X . X).
T_RE, T_IM, T_XRE, T_XIM, T_ROWS = [0], [1], [2, 3, 4], [5, 6, 7], 8


def standing() -> list[tuple[int, tuple[int, ...]]]:
    dot = table("T1", "T1")
    tied = [(G * e, (S_K, x[j], x[i])) for x in (S_RE, S_IM) for e, j, i in dot]
    return [*tied, (F, (S_K, S_K)), (-2 * F * N, (S_K,))]


def turning() -> list[tuple[int, tuple[int, ...]]]:
    own = [(F * e, (p[j], p[i])) for p in (T_RE, T_IM) for e, j, i in table("A1", "A1")]
    tied = [
        (M * e * f, (p[u], p[v], x[j], x[i]))
        for p in (T_RE, T_IM)
        for f, u, v in table("A1", "A1")
        for x in (T_XRE, T_XIM)
        for e, j, i in table("T1", "T1")
    ]
    return own + tied


def run(layout: Layout, start: State, rounds: int) -> list[State]:
    states, s = [start], start
    for _ in range(rounds):
        s = step.tick(layout, s)
        states.append(s)
    return states


def turn_t1(s: State, m: list[list[int]], parts: list[list[int]], teeth: int) -> State:
    """A turn of the 24 on a T1 hand's parts: a gear sent to minus a gear has its fine tooth flipped in its teeth."""
    a, b, r = s.a.copy(), s.b.copy(), s.r.copy()
    for rows in parts:
        for i in range(3):
            j = next(c for c in range(3) if m[i][c] != 0)
            sign = m[i][j]
            a[rows[i], 0], b[rows[i], 0] = sign * s.a[rows[j], 0], sign * s.b[rows[j], 0]
            r[rows[i], 0] = s.r[rows[j], 0] if sign > 0 else flip(s.r[rows[j], 0], teeth)
    return State(a, b, r, s.rd)


def part_one() -> None:
    print("1. A count and a turn: what the mirror and the 24 keep, exactly and up to the grain.")
    dot = table("T1", "T1")
    layout = node(turning(), T_ROWS, W)
    start = laid(T_ROWS, {0: (R, 12 * P), 1: (0, -5 * P), 2: (A, A)})
    states = run(layout, start, 600)
    odd = 0
    for s in states:
        m = State(s.b, s.a, flip(s.r, W), s.rd)  # the act's own mirror at fixed teeth
        odd += crossed(m, T_XRE, T_XIM, dot) == -crossed(s, T_XRE, T_XIM, dot) and crossed(
            m, T_RE, T_IM, table("A1", "A1")
        ) == -crossed(s, T_RE, T_IM, table("A1", "A1"))
    print(
        "   the mirror sends the counts' cross of before and now to minus itself (an identity wherever the table is "
        f"symmetric; checked on the 601 states of a run, both hands): {odd} of 601"
    )
    tables = {kind: table(kind, kind) for kind in LABELS}
    kept, symmetric = 0, True
    for tab in tables.values():
        symmetric &= sorted((e, j, i) for e, j, i in tab) == sorted((e, i, j) for e, j, i in tab)
    for g in ON:
        mats = {
            "A1": KINDS.a1[g],
            "A2": KINDS.a2[g],
            "E": KINDS.e[g],
            "T1": KINDS.t1[g],
            "T2": KINDS.t2[g],
        }
        ok = True
        for kind, tab in tables.items():
            mat = [[int(v) for v in row] for row in mats[kind]]
            dim = len(mat)
            c = [[0] * dim for _ in range(dim)]
            for e, j, i in tab:
                c[j][i] = e
            for j in range(dim):
                for i in range(dim):
                    ok &= (
                        sum(mat[u][j] * c[u][v] * mat[v][i] for u in range(dim) for v in range(dim))
                        == c[j][i]
                    )
        kept += ok
    print(
        f"   the five kinds' tables onto A1 are symmetric: {symmetric}; turns of the 24 that keep every one "
        f"(D^T C D = C): {kept} of {len(ON)}"
    )


def part_two() -> tuple[int, list[State], list[State]]:
    print("\n2. The standing count of G3 and the turning count, one Node-clock, the same tied family.")
    one = table("A1", "A1")
    s_states = run(node(standing(), S_ROWS, W), laid(S_ROWS, {S_K: (N, N), S_RE[0]: (A, A)}), ROUNDS)
    t_layout = node(turning(), T_ROWS, W)
    t_start = laid(T_ROWS, {0: (R, 12 * P), 1: (0, -5 * P), T_XRE[0]: (A, A)})
    t_states = run(t_layout, t_start, ROUNDS)
    key = area(t_start, T_RE, T_IM, one, W)
    print(f"   W = {W}, F = {F}, M = G = {M}, R = {R}, n = R^2 = {N}, the tied swing {A}")
    off = max(abs(s.a[S_K, 0] - N) for s in s_states)
    print(f"   the standing count's largest move off n over {ROUNDS} rounds: {off} counts")
    birth, _ = carry(key - 1, 2, 0)
    _, parity = carry(key, 2, 0)
    print(
        f"   the turning count's area at the lay, the key it sets here: {key} (W R^2 x 5 / 13 = "
        f"{carry(W * R * R * 5, 13, 0)[0]}); odd: {parity == 1} (no click fires here, so its parity reads nothing)"
    )
    pushed = held = 0
    worst = 0
    radius = 0
    windings = set()
    for t in range(ROUNDS):
        s, nxt = t_states[t], t_states[t + 1]
        _, j = step.sources(t_layout, s.a)
        jj = list(j[:, 0])
        pushed += moved(s, jj, T_RE, T_IM, one) != 0
        change = area(nxt, T_RE, T_IM, one, W) - area(s, T_RE, T_IM, one, W)
        held += change != turned_rule3(s, nxt, T_RE, T_IM, one)
        worst = max(worst, abs(area(nxt, T_RE, T_IM, one, W) - key))
        radius = max(radius, abs(nxt.a[0, 0] ** 2 + nxt.a[1, 0] ** 2 - N))
        q, _ = carry(area(nxt, T_RE, T_IM, one, W), key, birth)
        windings.add(q)
    print(
        f"   rounds where the act's push moves area into the turning count (tau, what term 11's click carries): "
        f"{pushed} of {ROUNDS}, so its clicks: 0; rounds where its area moves by anything but Rule3's turn: "
        f"{held} of {ROUNDS}"
    )
    print(
        f"   its area off the key at most: {worst} grains ({in_billionths(worst, key)} of a key); its windings at "
        f"the key (its swept area carried at the key from the birth), in every round: {sorted(windings)}"
    )
    print(f"   its radius squared off R^2 at most: {radius} counts squared (R^2 = {N})")
    xs = [s.a[S_RE[0], 0] for s in s_states]
    xt = [s.a[T_XRE[0], 0] for s in t_states]
    print(
        f"   the tied family's sign changes in {ROUNDS} rounds: {changes(xs)} beside the standing count, {changes(xt)} "
        f"beside the turning one; their counts part by at most {max(abs(u - v) for u, v in zip(xs, xt, strict=True))} "
        f"of its swing {A}"
    )
    return key, t_states, s_states


def part_three() -> None:
    print(
        "\n3. The 24 on the click world (ANIMATE-CLICK/click.py, the giver and the taker turning): what every turn "
        "keeps exactly, and what only up to the grain."
    )
    g = carry(click.F, 10, 0)[0]
    layout = click_node(click.potential(g))
    base = lay_click(click.A)
    key = carry(click.swept(click.LRE, click.LIM, base.a[:, 0], click.stride(base)), 7, 0)[0]
    rounds = 600
    found, states = clicks_of(layout, base, key, rounds)
    dot = table("T1", "T1")
    gre, gim = [click.LRE + c for c in range(3)], [click.LIM + c for c in range(3)]
    tre, tim = [click.MRE + c for c in range(3)], [click.MIM + c for c in range(3)]
    parts = [gre, gim, tre, tim]

    def tau(s: State) -> int:
        _, j = step.sources(layout, s.a)
        return moved(s, list(j[:, 0]), tre, tim, dot)

    taus = [tau(s) for s in states]
    count = {"state": 0, "cross": 0, "tau": 0, "area": 0, "clicks": 0}
    worst = 0
    for g24 in ON:
        m = [[int(v) for v in row] for row in KINDS.t1[g24]]
        other_found, other = clicks_of(layout, turn_t1(base, m, parts, click.W), key, rounds)
        pairs = list(zip(other, states, strict=True))
        count["state"] += all(same(x, turn_t1(y, m, parts, click.W)) for x, y in pairs)
        count["cross"] += all(
            crossed(x, gre, gim, dot) == crossed(y, gre, gim, dot)
            and crossed(x, tre, tim, dot) == crossed(y, tre, tim, dot)
            for x, y in pairs
        )
        count["tau"] += [tau(x) for x in other] == taus
        diffs = [area(x, gre, gim, dot, click.W) - area(y, gre, gim, dot, click.W) for x, y in pairs]
        count["area"] += all(d == 0 for d in diffs)
        worst = max(worst, max(abs(d) for d in diffs))
        count["clicks"] += other_found == found
    grains, _ = carry(worst, click.W - 1, 0)
    print(
        f"   turns: {len(ON)}; runs turned state for state over {rounds} rounds: {count['state']}; the counts' cross "
        f"of both hands alike in every round: {count['cross']}; tau, the area the push moves into the taker, alike: "
        f"{count['tau']}; the clicks alike: {count['clicks']}"
    )
    print(
        f"   the giver's swept area with its fine teeth alike in every round: {count['area']} of {len(ON)}; under the "
        f"others it moves by up to {grains} times W - 1 (a flipped tooth turns a stride p into -p + W - 1)"
    )


def quartic(lam: int, g: int) -> list[tuple[int, tuple[int, ...]]]:
    """Animate's click world with a stop on the giver: V = f (L.L + M.M) + g Re(conj(M) . L) + lam (L.L)^2."""
    giver = [click.LRE + c for c in range(3)] + [click.LIM + c for c in range(3)]
    return click.potential(g) + [(lam, (j, j, i, i)) for j in giver for i in giver]


def clicks_of(
    layout: Layout, start: State, key: int, rounds: int
) -> tuple[list[tuple[int, int]], list[State]]:
    """The whole click on the taker: the area the push moves into it, carried at the key from the Boss's birth."""
    s, k = start, carry(key - 1, 2, 0)[0]
    out, states = [], [start]
    for t in range(rounds):
        _, j = step.sources(layout, s.a)
        tau = click.moved(s, list(j[:, 0]), click.MRE)
        s = step.tick(layout, s)
        q, k = carry(tau, key, k)
        if q:
            out.append((t, q))
        states.append(s)
    return out, states


def lay_click(swing: int) -> State:
    a = np.zeros((click.ROWS, 1), dtype=object)
    b = np.zeros((click.ROWS, 1), dtype=object)
    a[click.LRE, 0], b[click.LRE, 0] = swing, swing
    a[click.LIM, 0], b[click.LIM, 0] = 0, -carry(swing, 20, 0)[0]
    return State(a, b, 0 * a, 0 * a)


def click_node(monomials: list[tuple[int, tuple[int, ...]]]) -> Layout:
    return node(monomials, click.ROWS, click.W)


def part_four() -> None:
    print(
        "\n4. The key is no law of the act: the click writes nothing; by homogeneity the clicks read a four-leg "
        "strength times the key, in the continuum, and on the act up to Rule3's grain."
    )
    g, lam = (
        carry(click.F, 10, 0)[0],
        1251,
    )  # 1251 = 9 x 139; at the giver's swing the stop stiffens it by 2 per cent
    base = lay_click(click.A)
    key, _ = carry(click.swept(click.LRE, click.LIM, base.a[:, 0], click.stride(base)), 7, 0)
    rounds = 6000
    one, s1 = clicks_of(click_node(quartic(lam, g)), base, key, rounds)
    three, s3 = clicks_of(click_node(quartic(lam, g)), base, 3 * key, rounds)
    gears = sum(1 for x, y in zip(s1, s3, strict=True) if same(x, y))
    print(
        f"   the click world with a stop lam = {lam} on the giver, the key a seventh of its area at the lay ({key}): "
        f"{len(one)} clicks, net {sum(q for _, q in one)}"
    )
    print(
        f"   the same at three times the key: gears alike in {gears} of {rounds + 1} rounds; {len(three)} clicks, net "
        f"{sum(q for _, q in three)}"
    )
    scaled, sc = clicks_of(
        click_node(quartic(carry(lam, 9, 0)[0], g)), lay_click(3 * click.A), 9 * key, rounds
    )
    exact = sum(
        1
        for x, y in zip(sc, s1, strict=True)
        if all(u == 3 * v for u, v in zip(x.a[:, 0], y.a[:, 0], strict=True))
    )
    print(
        f"   every swing x 3, the key x 9 and the stop / 9 (lam key kept): {len(scaled)} clicks; clicks in one run and "
        f"not the other: {len(set(scaled) ^ set(one))}; rounds whose counts are exactly 3 times the first run's: "
        f"{exact} of {rounds + 1} (Rule3's grain does not scale)"
    )
    unscaled, _ = clicks_of(click_node(quartic(lam, g)), lay_click(3 * click.A), 9 * key, rounds)
    print(
        f"   every swing x 3 and the key x 9 with the stop kept (lam key x 9): {len(unscaled)} clicks; clicks in one run "
        f"and not the other: {len(set(unscaled) ^ set(one))}"
    )
    lam2 = 1296  # 6^4: the stop over s^2 is whole at every s that divides 36
    first, _ = clicks_of(click_node(quartic(lam2, g)), base, key, rounds)
    moved_by = []
    for s in (2, 3, 4, 6, 9):
        sq = s * s
        other, _ = clicks_of(
            click_node(quartic(carry(lam2, sq, 0)[0], g)), lay_click(s * click.A), sq * key, rounds
        )
        moved_by.append((s, len(set(other) ^ set(first))))
    print(
        f"   with the stop lam = {lam2}: {len(first)} clicks; every swing x s, the key x s^2 and the stop / s^2: "
        f"(s, clicks in one run and not the other): {moved_by}"
    )


def keeps(stack, v: tuple[int, ...]) -> int:
    """How many of the 24 send the steady count v of a kind to itself, by the kind's own matrices."""
    dim = len(v)
    return sum(
        1
        for g in ON
        if all(sum(int(stack[g][i][j]) * v[j] for j in range(dim)) == v[i] for i in range(dim))
    )


def part_five() -> None:
    print(
        "\n5. The 24 on a steady count, by its kind: how many turns keep it, every count with entries -2 to 2."
    )
    mats = {"A1": KINDS.a1, "A2": KINDS.a2, "E": KINDS.e, "T1": KINDS.t1, "T2": KINDS.t2}
    for kind, stack in mats.items():
        dim = stack.shape[-1]
        sizes: dict[int, int] = {}
        multiples = True
        for c in itertools.product(range(-2, 3), repeat=dim):
            if not any(c):
                continue
            k = keeps(stack, c)
            sizes[k] = sizes.get(k, 0) + 1
            multiples &= all(keeps(stack, tuple(f * x for x in c)) == k for f in (2, 3, -1))
        row = ", ".join(f"{k}: {n}" for k, n in sorted(sizes.items(), reverse=True))
        print(
            f"   {kind}: the turns that keep it (counts with that many): {row}; the same for 2, 3 and -1 times "
            f"every count: {multiples}"
        )


def part_six() -> None:
    print(
        "\n6. A quantum carries the key times its beat (E = n hbar omega, the key as hbar), on the click world with no stop."
    )
    g = carry(click.F, 10, 0)[0]
    base = lay_click(click.A)
    key = carry(click.swept(click.LRE, click.LIM, base.a[:, 0], click.stride(base)), 7, 0)[0]
    found, states = clicks_of(click_node(click.potential(g)), base, key, click.ROUNDS)

    def doubled(s: State) -> int:
        """2 W times the taker's energy: its strides squared, and its spring F a^2 on each of its six gears times 2 W."""
        p = click.stride(s)
        taker = range(click.MRE, click.MRE + 6)
        return sum(p[x] * p[x] for x in taker) + 2 * click.W * click.F * sum(
            s.a[x, 0] ** 2 for x in taker
        )

    def taken(s: State) -> int:
        return click.swept(click.MRE, click.MIM, s.a[:, 0], click.stride(s))

    ratios = []
    for t, _ in found[:7]:
        x, om = doubled(states[t + 1]) - doubled(base), taken(states[t + 1]) - taken(base)
        ratios.append(carry(x * x * 10**9, 8 * click.F * click.W * om * om, 0)[0])
    print(
        "   the square of the taker's energy gained over its area gained, over its beat squared 2 F / W, at its first "
        f"seven clicks, in billionths: {ratios}"
    )


def main() -> None:
    part_one()
    part_two()
    part_three()
    part_four()
    part_five()
    part_six()


if __name__ == "__main__":
    main()
