"""p13: a wave across a step of the clock, three ways (Big Pic, 2026-10-30; the Boss's 6531810938 items 3 and 4).

A line of 400 Node-clocks, the clock's lapse N = 1 on the left half and 4/5 on the right, a right-moving packet laid at
Node 100. Nature's massless scalar under a lapse, d_t ((1/N) d_t a) = d_x (N d_x a), has its lapse on the Mesh: in one
dimension it is conformal, so the step reflects nothing, and the books of its momentum SUM (a_t / N) close exactly on
any lapse. Three forms of the act are run:
  (1) the density reading: the edge act with the dial 1/N per Node-clock and the grips N per Mesh;
  (2) the slot reading: the grips at rest and the dial rest / N^2 (one slot read for both weights);
  (3) the escapement (FWDBACK.md, section 3): one tooth per Node-clock, the dial D = L(now) + L(before) pushed by
      L_0 + L_0 a round, its 0-or-1 quotient releasing the Node-clock, which then steps at its rest teeth on its Meshes'
      now slots; here L = L_0 / N, held still.
Each is compared with its own run on a uniform clock (N = 1 everywhere): what differs on the left half after the packet
has met the step is the reflected wave. Whole numbers only; every division is Rule3's carry.
"""

from qlib import ONE, TWO, carry, report

lines = []
SITES = 400
STEP = 200
ROUNDS = 700
AMP = 1000000000
HALF = 60
CENTRE = 100
A1, B1 = 32000000, 2000000  # the rest dial and grip: the speed squared B / A = 1/16
L0 = 4  # the escapement's rest count; the right half's count 5, so N = 4/5


def pascal(m):
    row = [ONE]
    for _ in range(m):
        row = [a + b for a, b in zip([0] + row, row + [0], strict=True)]
    return row


ROW = pascal(TWO * HALF)
TOP = ROW[HALF]
lay = [0] * SITES
for k, v in enumerate(ROW):
    lay[CENTRE - HALF + k] = carry(AMP * v, TOP, 0)[0]


def right_mover(f):
    """The before slot of a right-moving packet at a quarter Mesh a round: f(x) + (f(x + 1) - f(x - 1)) / 8."""
    out = []
    for x in range(SITES):
        up = f[x + ONE] if x + ONE < SITES else 0
        down = f[x - ONE] if x > 0 else 0
        out.append(f[x] + carry(up - down, 8, 0)[0])
    return out


def pulls(a, grips):
    """The grips' pull at every Node-clock, one grip per Mesh (i, i + 1); the line's two ends are free."""
    q = [0] * SITES
    for i in range(SITES - ONE):
        d = grips[i] * (a[i + ONE] - a[i])
        q[i] += d
        q[i + ONE] -= d
    return q


def edge_run(dials, grips, rounds):
    """The edge act on a still clock: N = 2 (D (a - b) + 2 q) + s split half-open at 2 D, D = 2 A per Node-clock."""
    a, b, s = list(lay), right_mover(lay), [0] * SITES
    books = set()
    for _ in range(rounds):
        q = pulls(a, grips)
        nxt, tooth = [], []
        for i in range(SITES):
            d = TWO * dials[i]
            n = TWO * (d * (a[i] - b[i]) + TWO * q[i]) + s[i]
            v, r = carry(n + d, TWO * d, 0)
            nxt.append(a[i] + v)
            tooth.append(r - d)
        a, b, s = nxt, a, tooth
        books.add(sum(TWO * TWO * dials[i] * (a[i] - b[i]) + s[i] for i in range(SITES)))
    return a, books


def escapement_run(counts, rounds):
    """The escapement: per Node-clock one tooth tau at the dial L + L (a still clock), pushed by L0 + L0 a round; a
    release steps the Node-clock once by the edge act at the rest dial A1 on its Meshes' now slots (grip B1)."""
    a, b, s = list(lay), right_mover(lay), [0] * SITES
    tau = [carry(TWO * c, TWO, 0)[0] for c in counts]  # born at the half dial
    books = set()
    for _ in range(rounds):
        q = pulls(a, [B1] * (SITES - ONE))
        nxt_a, nxt_b, nxt_s, nxt_tau = [], [], [], []
        for i in range(SITES):
            go, t = carry(L0 + L0, counts[i] + counts[i], tau[i])
            nxt_tau.append(t)
            d = TWO * A1
            n = TWO * (d * (a[i] - b[i]) + TWO * q[i]) + s[i]
            v, r = carry(n + d, TWO * d, 0)
            nxt_a.append(a[i] + go * v)
            nxt_b.append(b[i] + go * (a[i] - b[i]))
            nxt_s.append(s[i] + go * (r - d - s[i]))
        a, b, s, tau = nxt_a, nxt_b, nxt_s, nxt_tau
        books.add(sum(TWO * TWO * A1 * (a[i] - b[i]) + s[i] for i in range(SITES)))
    return a, books


def reflected(got, ref):
    """The largest difference on the left half, in permille of the packet's height."""
    top = max(abs(got[x] - ref[x]) for x in range(STEP))
    return carry(1000 * top, AMP, 0)[0]


# (1) the density reading
flat1, books_flat1 = edge_run([A1] * SITES, [B1] * (SITES - ONE), ROUNDS)
a_right, b_right = carry(A1 * 5, 4, 0)[0], carry(B1 * 4, 5, 0)[0]
mid = carry(B1 + b_right, TWO, 0)[0]
got1, books1 = edge_run(
    [A1] * STEP + [a_right] * STEP, [B1] * (STEP - ONE) + [mid] + [b_right] * (STEP - ONE), ROUNDS
)
r1 = reflected(got1, flat1)
report(
    lines,
    "1. the density reading (the dial 1/N per Node-clock, the grips N per Mesh): the step N 1 to 4/5 reflects "
    f"{r1} permille (nature's one-dimensional step: 0), and the momentum's books close at every round",
    r1 <= 3 and len(books1) == ONE,
)

# (2) the slot reading
got2, books2 = edge_run([A1] * STEP + [carry(A1 * 25, 16, 0)[0]] * STEP, [B1] * (SITES - ONE), ROUNDS)
r2 = reflected(got2, flat1)
report(
    lines,
    f"2. the slot reading (the grips at rest, the dial rest / N^2): the same step reflects {r2} permille, the "
    "impedance's (N1 - N2) / (N1 + N2) = 111",
    100 <= r2 <= 120 and len(books2) == ONE,
)

# (3) the escapement
flat3, books_flat3 = escapement_run([L0] * SITES, ROUNDS)
got3, books3 = escapement_run([L0] * STEP + [5] * STEP, ROUNDS)
r3 = reflected(got3, flat3)
drift = max(books3) - min(books3)
size = sum(abs(TWO * TWO * A1 * (x - y)) for x, y in zip(lay, right_mover(lay), strict=True))
report(
    lines,
    "3. the escapement: on a uniform clock it is the act as built, state for state and its books standing; across the "
    f"step it reflects {r3} permille, near the slot reading's and not nature's, and its momentum's books move by "
    f"{carry(1000 * drift, size, 0)[0]} permille of the packet's own (the sum over the Node-clocks of |4 A v|) as the "
    "packet crosses, where the density reading's stand",
    flat3 == flat1 and len(books_flat3) == ONE and 80 <= r3 <= 120 and drift > 0,
)


def mesh_escapement_run(counts, rounds, back=False):
    """The escapement with the Mesh's own tooth: each Mesh (i, i + 1) has a tooth at the dial L(i) + L(i + 1), pushed
    by L0 + L0 a round, whose release pays the Mesh's pull into both its ends at once (the lapse on the Mesh); each
    Node-clock's own tooth releases its step, the momentum split at the rest dial (the lapse at the Node-clock). With
    back, the rounds are then undone one by one, each tooth's release read from its flip at its dial, as FWDBACK's
    mirror reads it; the state returned is then the lay's or not."""
    d = TWO * A1
    a = list(lay)
    mom = [TWO * d * (x - y) for x, y in zip(lay, right_mover(lay), strict=True)]
    tau = [carry(TWO * c, TWO, 0)[0] for c in counts]
    mu = [
        carry(counts[i] + counts[i + ONE], TWO, 0)[0] for i in range(SITES - ONE)
    ]  # born at the half dial
    start = (list(a), list(mom), list(tau), list(mu))
    books = set()
    for _ in range(rounds):
        for i in range(SITES - ONE):
            go, mu[i] = carry(L0 + L0, counts[i] + counts[i + ONE], mu[i])
            pull = TWO * TWO * B1 * (a[i + ONE] - a[i])
            mom[i] += go * pull
            mom[i + ONE] -= go * pull
        for i in range(SITES):
            go, tau[i] = carry(L0 + L0, counts[i] + counts[i], tau[i])
            v, _ = carry(mom[i] + d, TWO * d, 0)
            a[i] += go * v
        books.add(sum(mom))
    if not back:
        return a, books
    for _ in range(rounds):
        for i in range(SITES):
            dial = counts[i] + counts[i]
            go, flipped = carry(L0 + L0, dial, dial - ONE - tau[i])
            tau[i] = dial - ONE - flipped
            v, _ = carry(mom[i] + d, TWO * d, 0)
            a[i] -= go * v
        for i in range(SITES - ONE):
            dial = counts[i] + counts[i + ONE]
            go, flipped = carry(L0 + L0, dial, dial - ONE - mu[i])
            mu[i] = dial - ONE - flipped
            pull = TWO * TWO * B1 * (a[i + ONE] - a[i])
            mom[i] -= go * pull
            mom[i + ONE] += go * pull
    return (a, mom, tau, mu) == start, books


flat4, books_flat4 = mesh_escapement_run([L0] * SITES, ROUNDS)
got4, books4 = mesh_escapement_run([L0] * STEP + [5] * STEP, ROUNDS)
r4 = reflected(got4, flat4)
home, _ = mesh_escapement_run([L0] * STEP + [5] * STEP, ROUNDS, back=True)
report(
    lines,
    "4. the escapement with the Mesh's own tooth (the Mesh releases its pull into both ends at once, at the dial "
    "L(i) + L(i + 1)): on a uniform clock it is the act as built state for state; across the step it reflects "
    f"{r4} permille, its momentum's books stand at every round, and {ROUNDS} rounds undone one by one, each release "
    "read from its tooth's flip, return the lay exactly",
    flat4 == flat1 and len(books4) == ONE and r4 <= 20 and home,
)

lines.append(
    "   so the escapement keeps nature's beat at each Node-clock but carries the lapse there alone: a Mesh's two"
)
lines.append(
    "   ends take its pull at their own rates; a tooth on the Mesh carries the lapse there too, as nature does"
)

print("\n".join(lines))
print("ALL PASS" if all(line.startswith(("PASS", "   ")) for line in lines) else "SOME FAILED")
