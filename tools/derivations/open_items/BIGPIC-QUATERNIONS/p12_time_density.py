"""p12: the time gear's own law, from above (Big Pic, 2026-10-30; the Boss's 6531004963 item 3).

Part A, the deriver's law D_in^2 + D_out^2 = 8 W^2 + 4 push + s - s+ (the out edge's tooth in [-D_out, D_out)).
The fine value F = D^2 + s with s in [-D, D) counts the out edge's states one to one (the windows [D^2 - D, D^2 + D)
tile the whole numbers), and the law reads F_out = 8 W^2 + 4 push - 1 - F_in, with the in edge read through the mirror
(s to -1 - s): a reflection of the fine value. Reading D_out from F_out is the root. On the board's range it is one carry
by 4 W and one compare. Part B, the books road: nature's law for the time density in harmonic time, the 0 row of
d_mu (sqrt(-g) g^(mu nu)) = 0 taken twice, d_t^2 A = -d_i d_j (the grips' densities). The 00 row keeps a fixed dial and
no beat of its own; the grips' row and the matter row run the edge act at the dial the 00 row produced first. A ring
toy of the mechanics, not of three-dimensional gravity. Whole numbers only; every division is Rule3's carry.
"""

from qlib import ONE, TWO, carry, report

lines = []


# ---------------------------------------------------------------- part A: the deriver's law and its root
def window_of(d_out, w):
    """The out edge's window for D_out = 2 W + d, shifted by 4 W^2: [lower, upper) for the reflected fine value."""
    return (
        4 * w * d_out + d_out * d_out - TWO * w - d_out,
        4 * w * d_out + d_out * d_out + TWO * w + d_out,
    )


def read_out(f_out, w):
    """D_out and its tooth from the out edge's fine value, by one carry by 4 W and compares; the compares counted."""
    rest = f_out - 4 * w * w
    d, _ = carry(rest + TWO * w, 4 * w, 0)
    compares = 0
    while True:
        compares += ONE
        low, high = window_of(d, w)
        if rest < low:
            d -= ONE
        elif rest >= high:
            d += ONE
        else:
            break
    d_out = TWO * w + d
    return d_out, f_out - d_out * d_out, compares


# A1. the tiling
TOP = 400
seen = {}
for big_d in range(ONE, TOP + ONE):
    for s in range(-big_d, big_d):
        seen[big_d * big_d + s] = (big_d, s)
report(
    lines,
    "A1. the out edge's states (D, s), s in [-D, D), counted by the fine value D^2 + s, tile the whole numbers one to "
    f"one: every number below {TOP}^2 + {TOP} is met exactly once",
    sorted(seen) == list(range(TOP * TOP + TOP)),
)

# A2. the law is a reflection of the fine value, and its run back is the mirror
ok_back = True
cases = 0
for w in range(8, 40):
    for push in range(-3, 4):
        for d_in in range(TWO * w - 4, TWO * w + 5):
            for s in range(-d_in, d_in):
                f_out = 8 * w * w + 4 * push + s - d_in * d_in
                d_out, s_out = seen[f_out]
                f_back = 8 * w * w + 4 * push + (-ONE - s_out) - d_out * d_out
                ok_back &= seen[f_back] == (d_in, -ONE - s)
                cases += ONE
report(
    lines,
    "A2. the deriver's law at fixed W is a bijection of the out edge's states, and the run back is the mirror: the "
    f"backward step from (D_out, -1 - s+) returns (D_in, -1 - s) in all {cases} cases (W 8 to 39, D_in within 4 of 2 W, push -3 to 3)",
    ok_back,
)

# A3. the root as one carry by 4 W and one compare, on the board's range
ok_one = True
first_two = None
for w in (100, 10000):
    for d in range(-260 if w == 10000 else -26, 261 if w == 10000 else 27):
        d_out = TWO * w + d
        for s in (-d_out, -ONE, 0, d_out - ONE):
            got, tooth, compares = read_out(d_out * d_out + s, w)
            ok_one &= got == d_out and tooth == s
            if compares > TWO and w == 10000 and (first_two is None or abs(d) < first_two):
                first_two = abs(d)
report(
    lines,
    "A3. D_out read from its fine value by one carry by 4 W and compares is exact; at W = 10,000 one compare after the "
    f"carry places it while |D_out - 2 W| < {first_two} (twice the root of W is 200), and a second compare is needed "
    "only beyond",
    ok_one and first_two is not None and 190 < first_two < 210,
)

# A4. what the law keeps: W v^2 (sqrt(W) v squared) as W triples, with no push
w_b, w_now, s = 1000000, 1000000 + 3000, 0
kept0 = w_now * (w_now - w_b) ** TWO
rounds = 0
while w_now < 3000000:
    d_in = w_b + w_now
    d_out, s_out, _ = read_out(8 * w_now * w_now + s - d_in * d_in, w_now)
    w_b, w_now, s = w_now, d_out - w_now, s_out
    rounds += ONE
kept1 = w_now * (w_now - w_b) ** TWO
permille, _ = carry(1000 * kept1, kept0, 0)
report(
    lines,
    f"A4. with no push the law keeps W v^2, sqrt(W) v squared: {permille} permille of the start after {rounds} rounds, "
    "as W triples (the deriver's sqrt(W) v kept to within 14 permille)",
    985 <= permille <= 1030,
)

# ---------------------------------------------------------------- part B: the books road on a ring
SITES = 64
REST_A, REST_G = 4000000, 250000


def ring(i):
    return carry(i, SITES, 0)[1]


def pascal(m):
    row = [ONE]
    for _ in range(m):
        row = [a + b for a, b in zip([0] + row, row + [0], strict=True)]
    return row


def bump(centre, half, scale):
    row = pascal(TWO * half)
    f = [0] * SITES
    for k, v in enumerate(row):
        f[ring(centre - half + k)] = v * scale
    return f


def second(f, i):
    return f[ring(i + ONE)] - TWO * f[i] + f[ring(i - ONE)]


def act(x, x_b, s, d_in, d_out, grips):
    """The edge act on one row: N = 2 (D_in (x - x_b) + 2 q) + s split half-open at 2 D_out; D per Node, grips per Mesh."""
    nxt, tooth = [], []
    for i in range(SITES):
        j, h = ring(i + ONE), ring(i - ONE)
        q = grips[i] * (x[j] - x[i]) - grips[h] * (x[i] - x[h])
        n = TWO * (d_in[i] * (x[i] - x_b[i]) + TWO * q) + s[i]
        v, r = carry(n + d_out[i], TWO * d_out[i], 0)
        nxt.append(x[i] + v)
        tooth.append(r - d_out[i])
    return nxt, tooth


def step(state):
    """One round: the 00 row first (the books, a fixed dial, no carry), then the grips' row and the matter row at the
    dial it produced, both gripped by the grips' row at now (the Mesh's two ends)."""
    a_b, a, g_b, g, sg, p_b, p, sp = state
    a_next = [TWO * a[i] - a_b[i] - second(g, i) for i in range(SITES)]
    d_in = [TWO * (a_b[i] + a[i]) for i in range(SITES)]
    d_out = [TWO * (a[i] + a_next[i]) for i in range(SITES)]
    grips = [g[i] + g[ring(i + ONE)] for i in range(SITES)]
    g_next, sg_next = act(g, g_b, sg, d_in, d_out, grips)
    p_next, sp_next = act(p, p_b, sp, d_in, d_out, grips)
    return (a, a_next, g, g_next, sg_next, p, p_next, sp_next)


def mirror(state):
    a_b, a, g_b, g, sg, p_b, p, sp = state
    return (a, a_b, g, g_b, [-ONE - t for t in sg], p, p_b, [-ONE - t for t in sp])


def run(state, rounds):
    for _ in range(rounds):
        state = step(state)
    return state


zeros = [0] * SITES
rest_a = [REST_A] * SITES
g_lay = [REST_G + v for v in bump(20, 6, 20)]
p_lay = bump(44, 6, 1000)
lay = (rest_a, list(rest_a), g_lay, list(g_lay), zeros, p_lay, list(p_lay), zeros)

# B1. the run back
there = run(lay, 300)
back = run(mirror(there), 300)
report(
    lines,
    "B1. the books road runs back exactly: 300 rounds, the mirror, 300 rounds give the mirrored lay, every row and tooth",
    mirror(back) == lay,
)

# B2. the 00 row's step holds no carry; the dial's total stands
state, totals = lay, set()
for _ in range(300):
    state = step(state)
    totals.add(sum(state[ONE]))
report(
    lines,
    "B2. the 00 row's own step divides nothing and keeps no tooth, and the dial's total over the ring stands at every "
    "round (the grips' double divergence sums to 0)",
    totals == {SITES * REST_A},
)

# B3. a uniform rest stands, at several rests: a change of units
ok_uniform = True
for ra, rg in ((REST_A, REST_G), (TWO * REST_A, REST_G), (REST_A, 3 * REST_G), (5 * REST_A, 7 * REST_G)):
    flat = ([ra] * SITES, [ra] * SITES, [rg] * SITES, [rg] * SITES, zeros, zeros, zeros, zeros)
    ok_uniform &= run(flat, 200) == flat
report(
    lines, "B3. a uniform rest of the dial and the grips stands exactly at every rest tried", ok_uniform
)

# B4. the 00 row has no beat of its own: a bump in the dial alone stands
a_bump = [REST_A + v for v in bump(32, 6, 200)]
lone = (a_bump, list(a_bump), [REST_G] * SITES, [REST_G] * SITES, zeros, zeros, zeros, zeros)
report(
    lines,
    "B4. a bump in the dial alone, with the grips at rest, stands exactly for 300 rounds: the 00 row carries no wave of "
    "its own, so it has no second cone",
    run(lone, 300) == lone,
)

# B5. the 00 row moves only inside the grips' reach
state, g_reach, a_reach = lay, set(), set()
for _ in range(60):
    state = step(state)
    g_reach |= {i for i in range(SITES) if state[3][i] != g_lay[i]}
    a_reach |= {i for i in range(SITES) if state[ONE][i] != REST_A}
widened = {ring(i + k) for i in g_reach for k in (-ONE, 0, ONE)} | {
    ring(i + k) for i in range(14, 27) for k in (-1, 0, 1)
}
report(
    lines,
    "B5. over 60 rounds the dial moves only where the grips' row has moved (one Mesh wider, the double divergence's "
    f"reach): the dial moved at {len(a_reach)} Nodes, the grips at {len(g_reach)}",
    a_reach <= widened and len(a_reach) > 0,
)

# B6. one cone: the grips' row and the matter row read one dial and one set of grips
g_lay2 = [REST_G + v for v in bump(32, 6, 20)]
twin = (rest_a, list(rest_a), g_lay2, list(g_lay2), zeros, g_lay2, list(g_lay2), zeros)
moved = run(twin, 200)
report(
    lines,
    "B6. one cone: a matter lay equal to the grips' lay moves equal to it, Node for Node and tooth for tooth, for 200 "
    "rounds, the dial moving under both",
    moved[3] == moved[6] and moved[4] == moved[7] and moved[ONE] != rest_a,
)


# B7. the dial as the slowdown: a matter packet crossing a dial bump arrives later
def arrival(a_row, rounds):
    p0 = bump(10, 4, 1000)
    st = (a_row, list(a_row), [REST_G] * SITES, [REST_G] * SITES, zeros, p0, list(p0), zeros)
    peak = []
    for _ in range(rounds):
        st = step(st)
        peak.append(abs(st[6][40]))
    best = max(peak)
    return [k for k, v in enumerate(peak) if v == best][0]


slow = [REST_A + v for v in bump(26, 10, 200)]
t_flat, t_slow = arrival(rest_a, 200), arrival(slow, 200)
report(
    lines,
    f"B7. the dial is the slowdown: a matter packet's peak reaches Node 40 at round {t_flat} over a flat dial and at "
    f"round {t_slow} across a raised dial between",
    t_slow > t_flat,
)

print("\n".join(lines))
print("ALL PASS" if all(line.startswith("PASS") for line in lines) else "SOME FAILED")
