"""Term 11, the whole click, measured on the draft's own act (engine/step.py, act) in whole numbers, for the
derivation's hostile mathematician's six items (the Boss's second code writer, 2026-10-30; a local draft, the keys
the probe's own and no file's). The world is Animate's: one Node-clock, T1 hands of two parts, a giver turning in its
re-im plane along x and a taker at rest, tied by term 6's vertex, each hand on its own spring; a second taker where an
item asks. What the act gives is read as it stands: the state, the clicks and the click teeth; the area a round moved
into a train is read back off its own carry, q key + k+ - k, and once against the naive cross.

Run: .venv/bin/python tools/derivations/open_items/derive/boss/term11_act/probe.py (about two minutes); its output is
probe.txt beside it.
"""

import functools
import itertools
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT / "src"))

from tensor24.algebra.carry import carry, flip  # noqa: E402
from tensor24.engine import contract, kinds, step  # noqa: E402
from tensor24.engine.state import Click, Gearing, Layout, Read, State  # noqa: E402
from tensor24.main import made  # noqa: E402
from tensor24.runner import load as loading  # noqa: E402
from tensor24.runner.board import board  # noqa: E402
from tensor24.runner.files import vocabulary  # noqa: E402

W, A = 10**20, 10**6  # the teeth at rest, and the giver's swing
F, _ = carry(W, 800, 0)  # each hand's own spring: a beat of about 126 rounds
G, _ = carry(
    F, 2, 0
)  # the vertex, five times Animate's F div 10: seven keys pass to the taker in about 250 rounds
AXES, PARTS = 3, 2
ROUNDS, SHORT, WINDOW, BEATS = 6000, 2000, 120, 10
CUBE = (3, 3, 3)


@functools.cache
def joint():
    """The kinds, the tables and the four-vector's square, once, from the Node-clock's star."""
    return made(loading.star(AXES))


def hands(count, key):
    """`count` T1 hands of two parts as the load lays them, with the loader's own click cross at the keys given."""
    held, c, square = joint()
    labels, dims, reads = vocabulary(held, square)
    t1 = labels.index("T1")
    kind, of = np.array([t1] * count, dtype=np.intp), np.arange(count, dtype=np.intp)
    trains = loading.trains_of(kind, of, np.array([PARTS] * count, dtype=object), dims, reads)
    traces, _, _ = reads
    return trains, Click(*loading.clicking(trains, c, traces, key))


def row(trains, hand, component, part):
    """A gear's row as the load lays a train's rows: the part runs fastest, then the component."""
    return int(trains.first[hand]) + component * PARTS + part


def potential(trains, f, ties):
    """V = f SUM |hand|^2 + SUM g (taker . giver) over the ties (giver, taker, g), as J's plan by the vertex law."""
    cells = list(itertools.product(range(AXES), range(PARTS)))
    own = [(f, (row(trains, h, c, p),) * 2) for h in range(len(trains)) for c, p in cells]
    vertex = [(g, (row(trains, t, c, p), row(trains, h, c, p))) for h, t, g in ties for c, p in cells]
    factor = np.array([f for f, _ in own + vertex], dtype=object)
    legs = tuple(
        np.array([(*legs, -1, -1)[i] for _, legs in own + vertex], dtype=np.intp) for i in range(4)
    )
    return contract.pushes(factor, legs)


def unread():
    """The clocks' read of no term."""
    none = np.zeros(0, dtype=np.intp)
    return Read(none, none.astype(object), none)


def node(count, key, ties):
    """Animate's Node-clock: its own neighbour through every Spoke, so no Mesh pulls it; the hands on their springs
    and the vertex between them; the keys per train, a (count, 1) array."""
    trains, click = hands(count, key)
    nb, ones = np.zeros((6, 1), dtype=np.intp), np.ones((1, 1), dtype=object)
    meshes, _ = carry(np.arange(6, dtype=np.intp)[:, None], 2, 0)
    grips, gearing = ones.repeat(AXES, axis=1), Gearing(W * ones, 1, 1, 1)
    plan = potential(trains, F, ties)
    return trains, Layout(
        nb, loading.star(AXES), meshes, grips, gearing, plan, unread(), unread(), click
    )


def lay(trains, k0):
    """The giver (hand 0) turning in its re-im plane along x, every other hand at rest, each train's click tooth at
    k0 (a whole number, or a (trains, 1) array)."""
    rows = int(trains.size.sum())
    a, b = (np.zeros((rows, 1), dtype=object) for _ in "ab")
    a[row(trains, 0, 0, 0), 0] = b[row(trains, 0, 0, 0), 0] = A
    swing, _ = carry(A, 20, 0)
    b[row(trains, 0, 0, 1), 0] = -swing
    return State(a, b, 0 * a, 0 * a, k0 + np.zeros((len(trains), 1), dtype=object))


def swept(trains, s, hand):
    """A hand's swept area through the dot product, re . p_im - im . p_re, p = W (a - b) + r its stride."""
    p = W * (s.a - s.b) + s.r
    re, im = (
        (row(trains, hand, c, 0) for c in range(AXES)),
        (row(trains, hand, c, 1) for c in range(AXES)),
    )
    return sum(s.a[x, 0] * p[y, 0] - s.a[y, 0] * p[x, 0] for x, y in zip(re, im, strict=True))


def crossed(trains, layout, s, hand):
    """The area the kick moves into a hand in a round, read naively: re . K_im - im . K_re through the dot product, K
    the source J itself at s = T_k = T_d = 1."""
    _, j = step.sources(layout, s.a)
    re, im = (
        (row(trains, hand, c, 0) for c in range(AXES)),
        (row(trains, hand, c, 1) for c in range(AXES)),
    )
    return sum(s.a[x, 0] * j[y, 0] - s.a[y, 0] * j[x, 0] for x, y in zip(re, im, strict=True))


def keyed(key, count=2):
    """Every train's key alike, a (count, 1) array."""
    return key + np.zeros((count, 1), dtype=object)


def odd_key(parts):
    """A part of the giver's swept area at the lay, made odd: the key beside Animate's."""
    trains, _ = node(1, keyed(1, 1), [])
    near, _ = carry(swept(trains, lay(trains, 0), 0), parts, 0)
    _, odd = carry(near, 2, 0)
    return near + 1 - odd


def birth(key):
    """(key - 1) div 2: the one tooth the flip leaves in place at an odd key."""
    born, _ = carry(key - 1, 2, 0)
    return born


def apart(key):
    """An even key's two births, key div 2 - 1 and key div 2, the giver's and the taker's."""
    half, _ = carry(key, 2, 0)
    return np.array([[half - 1], [half]], dtype=object)


def run(layout, s, rounds):
    """The forward run: every round's state and its clicks, each train's at the one site."""
    states, clicks = [s], []
    for _ in range(rounds):
        s, q = step.act(layout, s)
        states.append(s)
        clicks.append(q[:, 0].tolist())
    return states, clicks


def moved(layout, states, clicks):
    """The area each round moved into each train, read off the act's own carry: q key + k+ - k."""
    key = layout.click.key[:, 0].tolist()
    return [
        [q * key[t] + int(after.k[t, 0]) - int(before.k[t, 0]) for t, q in enumerate(qs)]
        for before, after, qs in zip(states[:-1], states[1:], clicks, strict=True)
    ]


def magnitude(x):
    """|x| by Rule3's sign test, [x >= 0] = 1 + x div (x x + 1): x times +1 or -1."""
    down, _ = carry(x, x * x + 1, 0)
    up = 1 + down
    return x * (up + up - 1)


def books(count, ties, key, k0, rounds):
    """A run of the world given, and its books: the rounds where the clicks' sum is not 0 (unbalanced), where the
    areas' sum is not 0 (unconserved), where the pair's teeth do not sum to key - 1 (teeth), the running total of the
    counts' range and the rounds it is not 0, and the rounds a click is seen; the run itself beside them."""
    trains, layout = node(count, keyed(key, count), ties)
    states, clicks = run(layout, lay(trains, k0), rounds)
    areas = moved(layout, states, clicks)
    totals = list(itertools.accumulate(sum(q) for q in clicks))
    return {
        "unbalanced": sum(1 for q in clicks if sum(q) != 0),
        "unconserved": sum(1 for tau in areas if sum(tau) != 0),
        "teeth": sum(1 for s in states if sum(s.k[:, 0].tolist()) != key - 1),
        "total": (min(totals), max(totals)),
        "off": sum(1 for t in totals if t != 0),
        "seen": sum(1 for q in clicks if any(q)),
        "states": states,
        "clicks": clicks,
        "areas": areas,
        "layout": layout,
        "trains": trains,
    }


def pair(key, k0, rounds=ROUNDS, g=G):
    """One giver and one taker at the key, born at k0, tied at g."""
    return books(2, [(0, 1, g)], key, k0, rounds)


def permutation(m, count):
    """The turn on every row of `count` hands of two parts: m on each hand's components, the part carried along."""
    block = np.kron(m, np.eye(PARTS, dtype=object))
    return np.kron(np.eye(count, dtype=object), block)


def signs(p):
    """The two halves of a signed permutation: its + entries and its - entries, each a 0 or 1 matrix."""
    plus, _ = carry(p * p + p, 2, 0)
    return plus, p * p - plus


def turned(s, p, site, w, flipped=True):
    """The state turned: rows by p, sites by site, each tooth of a row whose sign p flips taken to w - 1 - r; the
    click teeth moved by site alone; with flipped False, the teeth only moved (the mutant)."""
    plus, minus = signs(p)
    r = plus @ s.r + minus @ (flip(s.r, w) if flipped else s.r)
    out = []
    for x in (p @ s.a, p @ s.b, r, s.rd, s.k):
        y = np.empty_like(x)
        y[:, site] = x
        out.append(y)
    return State(*out)


def same(s, t):
    """Every slot equal, gear by gear."""
    return all(bool(np.array_equal(x, y)) for x, y in zip(s, t, strict=True))


def recurrence(seed):
    """An endless row of whole numbers from a fixed recurrence, each step one carry: no random module."""
    v = seed
    while True:
        _, v = carry(v * 6364136223846793005 + 1442695040888963407, 1 << 64, 0)
        yield v


def drawn(source, low, high):
    """A whole number in [low, high] from the recurrence's high bits."""
    _, x = carry(next(source) >> 33, high - low + 1, 0)
    return low + x


def board_turns(group, key, shape, rounds, s0=None):
    """On a board of the shape with Meshes (one site: Animate's Node-clock), the two hands laid turning at every site
    from a recurrence, or from the lay given: the turns for which the turned run is the run turned with its clicks
    and click teeth in every round, the mutant's (the fine teeth not flipped), the clicks seen, and the turns that
    flip no sign."""
    trains, click = hands(2, keyed(key))
    nb = board(shape)
    n = nb.shape[1]
    spokes, meshes = loading.geometry(nb, AXES)
    ones = np.ones((1, n), dtype=object)
    grip, _ = carry(W, 100, 0)
    grips, gearing = np.full((1, AXES * n), grip, dtype=object), Gearing(W * ones, 1, 1, 1)
    plan = potential(trains, F, [(0, 1, G)])
    layout = Layout(nb, spokes, meshes, grips, gearing, plan, unread(), unread(), click)
    if s0 is None:
        source = recurrence(11)
        rows = int(trains.size.sum())
        a, b, r = (np.zeros((rows, n), dtype=object) for _ in "abr")
        for hand, c, x in itertools.product(range(2), range(AXES), range(n)):
            re, im = row(trains, hand, c, 0), row(trains, hand, c, 1)
            a[re, x], a[im, x] = drawn(source, -A, A), drawn(source, -A, A)
            twentieth_im, _ = carry(a[im, x], 20, 0)
            twentieth_re, _ = carry(a[re, x], 20, 0)
            b[re, x], b[im, x] = a[re, x] + twentieth_im, a[im, x] - twentieth_re  # a turning hand
            r[re, x], r[im, x] = drawn(source, 0, 5), drawn(source, 0, 5)
        s0 = State(a, b, r, 0 * a, birth(key) + np.zeros((2, n), dtype=object))
    xyz, sides = np.indices(shape).reshape(AXES, -1), np.array(shape, dtype=object)[:, None]
    states, clicks = [s0], []
    for _ in range(rounds):
        s, q = step.act(layout, states[-1])
        states.append(s)
        clicks.append(q)
    held, flips = [0, 0], 0
    for m in group:
        p = permutation(m, 2)
        flips += not bool((p < 0).any())
        _, wrapped = carry(m @ xyz, sides, 0)
        site = np.ravel_multi_index(tuple(wrapped.astype(np.intp)), shape)
        for which, flipped in enumerate((True, False)):
            s, good = turned(s0, p, site, W, flipped), True
            for t in range(rounds):
                s, q = step.act(layout, s)
                moved_q = np.empty_like(q)
                moved_q[:, site] = clicks[t]
                alike = same(s, turned(states[t + 1], p, site, W, flipped))
                good = good and alike and bool(np.array_equal(q, moved_q))
            held[which] += good
    return held[0], held[1], sum(int((q != 0).sum()) for q in clicks), flips


def thousandths(x, key):
    """x in thousandths of the key, Rule3's quotient."""
    q, _ = carry(1000 * x, key, 0)
    return q


def report():
    k7 = odd_key(7)
    k8 = k7 + 1
    born = birth(k7)
    trains0, _ = node(1, keyed(1, 1), [])
    print(
        "Term 11 on the draft's act (step.act), whole numbers: the hostile mathematician's six items and the 24"
    )
    print(f"the giver's swept area at the lay {swept(trains0, lay(trains0, 0), 0)}")
    print(f"the odd key K {k7}, its birth (K - 1) div 2 = {born}; the even key beside it K + 1 = {k8}")

    print(
        f"\n1. The books, {ROUNDS} rounds, the clicks pushing nothing (the gears' run is the same at every key):"
    )
    one = pair(k7, born)
    print(
        f"   one giver and one taker at K: rounds where the clicks' sum is not 0: {one['unbalanced']} of {ROUNDS};"
        f" where the areas' sum is not 0: {one['unconserved']} of {ROUNDS}; a click seen in {one['seen']} rounds"
    )
    naive = sum(
        1
        for s, tau in zip(one["states"][:-1], one["areas"], strict=True)
        if [crossed(one["trains"], one["layout"], s, h) for h in range(2)] != tau
    )
    print(
        f"   the area read off the act's carry (q key + k+ - k) against the naive cross: {naive} rounds differ"
    )
    halved, _ = carry(G, 2, 0)
    for name, ties in (
        ("G and G", [(0, 1, G), (0, 2, G)]),
        ("G and G div 2", [(0, 1, G), (0, 2, halved)]),
    ):
        two = books(3, ties, k7, born, ROUNDS)
        print(
            f"   one giver and two takers, tied at {name}: rounds where the clicks' sum is not 0:"
            f" {two['unbalanced']} of {ROUNDS}; where the areas' sum is not 0: {two['unconserved']} of {ROUNDS};"
            f" the running total of the three counts from {two['total'][0]} to {two['total'][1]}, not 0 in"
            f" {two['off']} rounds; a click seen in {two['seen']} rounds"
        )
    his = [carry(x, 7, 3)[0] for x in (-8, 4, 4)]
    print(
        f"   his arithmetic, the key 7 born at 3, the areas (-8, +4, +4): the clicks {his}, their sum {sum(his)}"
    )

    print(f"\n2. The invariant k_giver + k_taker = key - 1, one giver and one taker, {ROUNDS} rounds:")
    print(
        f"   K (odd), both born at (K - 1) div 2: rounds where the teeth's sum is not K - 1: {one['teeth']} of"
        f" {ROUNDS + 1}"
    )
    even = pair(k8, birth(k8))
    print(
        f"   K + 1 (even), both born at (K + 1 - 1) div 2 = {birth(k8)}: rounds where the teeth's sum is not"
        f" K + 1 - 1: {even['teeth']} of {ROUNDS + 1} (it stands at K + 1 - 2); the books' misses:"
        f" {even['unbalanced']} of {ROUNDS}"
    )
    split = pair(k8, apart(k8))
    low, high = apart(k8)[:, 0].tolist()
    print(
        f"   K + 1 (even), born at (K + 1) div 2 - 1 and (K + 1) div 2: the teeth's sum not K + 1 - 1:"
        f" {split['teeth']} of {ROUNDS + 1}; the books' misses: {split['unbalanced']} of {ROUNDS}; the mirror takes"
        f" each birth to the other's: {flip(low, k8) == high and flip(high, k8) == low}"
    )
    print(
        f"   small keys on the same act, {SHORT} rounds, the area a round moves far above the key, the vertex at G + 1:"
        " at G every area moved is a multiple of 2^14 5^18 (2F's and G's common factor), so an even key's tooth"
        " keeps its parity and never lands on key - 1"
    )
    for small in (7, 6, 8):
        alike = pair(small, birth(small), SHORT, G + 1)
        parted = pair(small, apart(small), SHORT, G + 1)
        _, odd = carry(small, 2, 0)
        low, high = apart(small)[:, 0].tolist()
        print(
            f"   key {small} ({'odd' if odd else 'even'}): born alike at {birth(small)}: the books' misses"
            f" {alike['unbalanced']} of {SHORT}, the teeth's sum not key - 1 in {alike['teeth']} of {SHORT + 1};"
            f" born at {low} and {high}: the books' misses {parted['unbalanced']} of {SHORT}, the teeth's sum not"
            f" key - 1 in {parted['teeth']} of {SHORT + 1}"
        )

    print(
        "\n3. The beat read against the key (the free giver, no vertex): E the hand's energy, P its period in rounds,"
        " Omega its swept area:"
    )
    trains, layout = node(1, keyed(1, 1), [])
    s0 = lay(trains, 0)
    states, _ = run(layout, s0, 1400)
    re = [int(s.a[row(trains, 0, 0, 0), 0]) for s in states]
    crossings = [t for t in range(1, len(re)) if (re[t - 1] >= 0) != (re[t] >= 0)]
    span = crossings[2 * BEATS] - crossings[0]
    p = W * (s0.a - s0.b) + s0.r
    twice_w_e = int((p * p).sum() + 2 * W * F * (s0.a * s0.a).sum())  # 2 W E, a whole number
    omega = swept(trains, s0, 0)
    ratio, _ = carry(1000 * twice_w_e * span, 2 * W * omega * BEATS, 0)
    print(f"   {BEATS} beats take {span} rounds; 2 W E = {twice_w_e}; Omega = {omega}")
    print(
        f"   1000 E P div Omega = {ratio}: E P = 2 pi Omega within the lattice's rounding, so E = Omega omega with"
        " omega the angular beat 2 pi / P;"
    )
    print(
        "   one key of area carries key x omega (E = n key omega): the key is h-bar; E = key / P (h) would read 1000"
    )

    print(
        f"\n4. One click per round holds only while |tau| <= key, one giver and one taker, {ROUNDS} rounds:"
    )
    k350 = odd_key(350)
    for name, held in (("K", one), ("K div 50 made odd", pair(k350, birth(k350)))):
        key = held["layout"].click.key[1, 0]
        big = [magnitude(t[1]) for t in held["areas"]]
        qs = [magnitude(q[1]) for q in held["clicks"]]
        many = [(t, q) for t, q in zip(big, qs, strict=True) if q >= 2]
        over = sum(1 for t in big if t > key)
        within = sum(1 for t, q in zip(big, qs, strict=True) if t <= key and q >= 2)
        more = (
            f", their |tau| from {thousandths(min(t for t, _ in many), key)} to"
            f" {thousandths(max(t for t, _ in many), key)} thousandths of the key, |q| at most"
            f" {max(q for _, q in many)}"
            if many
            else ""
        )
        print(
            f"   key {name} = {key}: the most |tau| in a round is {thousandths(max(big), key)} thousandths of the"
            f" key; rounds with |tau| > key: {over} of {ROUNDS}; rounds with |q| >= 2: {len(many)} of {ROUNDS}{more};"
            f" rounds with |tau| <= key and |q| >= 2: {within}"
        )

    print(
        "\n5. The flip, k to key - 1 - k, as the area's negation about the birth, flip(k) - birth = -(k - birth):"
    )
    for name, key in (("K (odd)", k7), ("K + 1 (even)", k8)):
        b = birth(key)
        print(f"   {name}: flip(birth) - birth = {flip(b, key) - b}")
    for key in (7, 8):
        b = birth(key)
        held = sum(1 for k in range(key) if flip(k, key) - b == -(k - b))
        off = sorted({flip(k, key) - b + (k - b) for k in range(key)})
        print(
            f"   key {key}: teeth whose flip is the negation about the birth: {held} of {key};"
            f" flip(k) - birth + (k - birth) takes the values {off}"
        )
    for name, held in (("K", one), ("K + 1", even)):
        key = held["layout"].click.key[1, 0]
        b = birth(key)
        rounds = sum(1 for s in held["states"] if flip(s.k[1, 0], key) - b == -(s.k[1, 0] - b))
        print(
            f"   on the act at {name}: rounds where the mirrored taker's tooth is its tooth negated about the birth:"
            f" {rounds} of {ROUNDS + 1}"
        )

    print(
        f"\n6. The run back by the act alone, the click teeth flipped in the key by the mirror, no log read,"
        f" {ROUNDS} rounds:"
    )
    for name, held in (("K", one), ("K + 1", even), ("K + 1 born apart", split)):
        layout, states, clicks = held["layout"], held["states"], held["clicks"]
        s = states[-1]
        gears = teeth = quotients = 0
        for t in range(ROUNDS - 1, -1, -1):
            _, q = step.act(layout, step.mirror(layout, s))
            s = step.untick(layout, s)
            gears += all(np.array_equal(x, y) for x, y in zip(s[:-1], states[t][:-1], strict=True))
            teeth += np.array_equal(s.k, states[t].k)
            quotients += q[:, 0].tolist() == clicks[t]
        print(
            f"   {name}: rounds whose gears return: {gears} of {ROUNDS}; whose click teeth return: {teeth} of"
            f" {ROUNDS}; whose mirrored quotients are the way out's: {quotients} of {ROUNDS}; at the start the teeth"
            f" are the births: {np.array_equal(s.k, states[0].k)}"
        )
    layout, states = one["layout"], one["states"]
    s, unflipped = states[-1], 0
    for t in range(ROUNDS - 1, -1, -1):
        m = step.mirror(layout, s)._replace(k=s.k)  # the mutant: the click teeth left as they are
        n = step.tick(layout, m)
        s = step.mirror(layout, n)._replace(k=n.k)
        unflipped += np.array_equal(s.k, states[t].k)
    print(
        f"   the mutant at K, the click teeth not flipped by the mirror: rounds whose teeth return: {unflipped} of {ROUNDS}"
    )

    print(
        "\n7. The 24 by the act's own turn (kinds.turns on the star, T1 the turn itself, a negated row's fine tooth"
        " flipped in its teeth), the click teeth unmoved:"
    )
    matrix, weight = kinds.turns(loading.star(AXES))
    group = [matrix[g] for g in np.nonzero(weight)[0]]
    trains, _ = node(2, keyed(k7), [(0, 1, G)])
    alike, mutant, seen, flips = board_turns(group, k7, (1, 1, 1), WINDOW, lay(trains, birth(k7)))
    print(
        f"   one Node-clock, Animate's lay at K, {WINDOW} rounds: the turned run equals the run turned, its clicks"
        f" and click teeth alike in every round, for {alike} of the {len(group)} turns; the mutant (the fine teeth"
        f" not flipped) for {mutant}: the {flips} that flip no sign and the {mutant - flips} whose flips fall on the y"
        f" and z rows, which this lay keeps at 0; clicks seen: {seen}"
    )
    alike, mutant, seen, flips = board_turns(group, k350, (1, 1, 1), WINDOW)
    print(
        f"   one Node-clock, both hands turning on every axis from a recurrence, {WINDOW} rounds at K div 50 made odd:"
        f" for {alike} of the {len(group)} turns; the mutant for {mutant}; clicks seen: {seen}"
    )
    alike, mutant, seen, flips = board_turns(group, k350, CUBE, 6)
    print(
        f"   a cube of side 3 with Meshes, the hands turning at every site, 6 rounds at K div 50 made odd: for {alike}"
        f" of the {len(group)} turns; the mutant for {mutant} (the {flips} turns that flip no sign); clicks seen:"
        f" {seen}"
    )


if __name__ == "__main__":
    report()
