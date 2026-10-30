"""Term 13, the frozen clock, on the slot form: where the strong field takes the clocks and the grips, in whole numbers.

Whole numbers alone, every division Rule3's carry, no root taken and none found by search (where a root's value is
printed, its two endpoints are stated whole numbers, checked by powers), on the act (engine/mesh.py and engine/step.py
at main 0df0e8385), with the reads laid by hand as in g2_static.py: every row's teeth W = rest + the metric family's 00
slot (term 2), every Spoke's grip = the grip + its axis's ii slot at both ends of its Mesh (term 3).

(a)  the strong field's pull on the act, at the act's own rest: on a board of 6 by 6 by 6 the 00 slot laid at 12 U and
     every ii slot at -gamma U, the grip g = 2 S and the rest 6 g = 12 S, so u = c00 / rest = U / S and
     v = c_ii / g = -(gamma / 2) u, the tie in the act's own reading, U a whole field strong enough that some Meshes'
     grips reach 0 and pass it: the 00 row's pull is exactly 12 times the Laplacian of g U - gamma U^2 (g rest times
     the Laplacian of w = u - (gamma / 2) u^2) at every Node-clock, no order dropped, for gamma 1, 2, 3 and 7, and 12
     times every ii row's pull is -gamma times the 00 row's: the tied field solves the ii rows' own equation wherever
     the 00 row's holds, at every gamma (the first text's lay, every ii slot at -7 gamma U with the grip 14,000, was
     gamma 7 and 14 against the act's rest);
(a2) the 00 slot's board mean on the act as built: a wrapped board, no notch, every grip g, every row's teeth
     W = rest + c00 (the 00 row alone: rows idle at 0 change nothing), the 00 row laid at +rest / 1000 and
     -rest / 1000 on two neighbouring sites, at rest: the mean in thousandths of rest on the ring of 8 and on the 6 by
     6 by 6 board; the identity N (rest + m) d^2 m = -SUM delta d^2 delta + SUM (r - r+) from the gear's carry, the
     pulls summing to 0 on the wrapped board (m the mean, delta = c00 - m, d^2 the second difference in rounds, r the
     fine teeth), checked at every round; and the mutant, the same lay with the teeth held at rest;
(b)  light where a grip vanishes and where it turns negative: a ring of 8 Node-clocks on one axis, light laid on four
     of them; with the Meshes at the ring's two ends of those four held at a grip of 0, the other four never move, a
     test that cannot fail, since the two Meshes split the ring; with those Meshes at a small grip, light crosses; with
     one Mesh at a negative grip, the ring runs away;
(b2) where a negative grip runs away: the effective grip the rest of the board holds between a Mesh's ends, by
     Foster's theorem, on the ring of 8 and on the wrapped 6 by 6 by 6 board, against runs with one Mesh at -g/8, -g/6
     and -g/2 on the ring and at -g/2, -2 g and -3 g on the board;
(c)  the static exterior, arithmetic alone in exact ratios, nothing run on the act (r in G M / c^2, M = 1):
     (c1) the slot form's own (the ii slots tied to the 00 slot, or pulled through grips that read them: the two agree
          at every gamma): w = u - (gamma / 2) u^2 = 2 / r, so u = (1 - x) / gamma and the grip over g is x at
          r = 4 gamma / (1 - x^2), the clocks reading N^2 = 1 / (1 + u) and light's coordinate speed squared N^2 x:
          at gamma = 1 at four x (by construction), then for gamma 1, 2 and 3 as rational functions of x, the 00 row's
          flux r^2 x du / dr = -2 by the quotient rule, and the field where the grips vanish (x = 0); the untied
          exterior, the 00 slot's mass M0 apart from the ii slots' Mi: x^2 = 1 - 4 gamma Mi / r,
          u = (M0 / Mi)(1 - x) / gamma, the 00 flux -2 M0 and the bound (M0 / Mi) 5^(-5/4) / gamma; G2's pressure
          reading, the bound 5^(-5/4) (1 + 3 p) / (1 - p) with p = P / M, and the p where it reaches the compactness
          NICER reads for PSR J0030+0451 and PSR J0740+6620, each bound and p between stated endpoints checked by
          fourth powers;
     (c2) general relativity's static field in isotropic radius: the slot form's flux r^2 (grip / g) du / dr with
          u = N^-2 - 1 and grip / g = A^-2, against general relativity's own lapse equation's flux r^2 A dN / dr, both
          by the quotient rule on N = (1 - m) / (1 + m) and A = (1 + m)^2, m = G M / (2 c^2 r);
     (c3) general relativity's horizon read in the act's terms, computed from N and A at r = 1/2: N = 0 with A = 4,
          the grip g / 16; and the slot form's u and W where its grips vanish;
     (c4) what a uniform shift of the 00 slot does to the clocks' reading of one depth: N_A^2 / N_B^2 - 1 across a
          depth of rest / 50, at a background of 0 and of plus and minus rest / 10;
     (c5) the slot form's spheres: the areal radius R = A r with A^4 = 1 / (1 - 4 gamma / r), so
          R^4 = r^5 / (r - 4 gamma): its least over a grid of r = 401/100 to 20 at gamma = 1; then
          r^5 - 3125 gamma^4 (r - 4 gamma) = (r - 5 gamma)^2 (r^3 + 10 gamma r^2 + 75 gamma^2 r + 500 gamma^3),
          coefficient by coefficient for gamma 1 to 4, so the least on r > 4 gamma is unique and global, R^4 =
          3125 gamma^4; the most compact body the exterior can hold, G M / (c^2 R) = 5^(-5/4) / gamma, against the
          compactness of two neutron stars read by NICER under general relativity's metric; R and the bound between
          stated endpoints checked by fourth powers;
     (c6) the surface where the grips vanish is never part of a static field: (1 - gamma u)^2 = 1 - 2 gamma w, so
          w <= 1 / (2 gamma) for every real u; a ball with a uniform w-source, w = a - b r^2 inside and 2 / r outside,
          has w(0) = 3 M / s, so it stands only for s >= 6 gamma M;
     (c7) light's critical impact parameter, b = A r / N at its turning point: the slot form's least b^2 = 256/3 at
          r = 16/3 and general relativity's 27 at the areal R = 3, each by a factorization; the numbers the page
          quotes, root(256/3), root 27 and 5^(5/4), between stated endpoints checked by squares and fourth powers;
     (c8) the spatial metric's second order: the series of A^2, N^2 and n^2 = A^2 / N^2 in e = G M / (c^2 r), the slot
          form's from u = 2 e + u^2 / 2 (gamma = 1) and general relativity's from m = e / 2; light's second-order
          deflection (pi / 2) times n^2's e^2 coefficient, times (G M / (c^2 b))^2, and its value at the Sun's limb,
          where pi cancels against the radian's 648000 x 10^6 / pi microarcseconds;
(d)  light at a vanishing grip, on step.tick, laid with no root (the hostile physicist's hp5): (A) 700 Node-clocks,
     every tooth at rest, a grip linear in the distance to a Mesh at grip 0: the time per Mesh goes as the root of
     W / grip, so the board time is a sum of j^(-1/2), which converges at the surface, bounded here by squares; (B) the
     slot form's exterior at gamma = 1 with its grip as the coordinate, x = m / 100 at the Mesh m, so r = 4 / (1 - x^2)
     is a ratio, the uneven gaps in r folded into the grips and the teeth, every number a ratio rounded down by a
     carry: a pulse from near x = 3/5 runs to the zero grip; the share near it and its round, the round from which
     that slope holds below 2 per cent again, and the share the line keeps;
(e)  the inspiral, read in separations, no frequency computed: two equal static slot-form bodies of 70 solar masses in
     all, touching, their surfaces at the lattice radius 4, the throat's lattice radius 5 and its areal radius 5^(5/4)
     in G m / c^2, so their centres d = k G M / c^2 apart: d exact in metres and in km at k = 4 and 5, each digit by a
     carry with its remainder shown, and at the areal radius, d^4 = 5^5 (G M / c^2)^4, between stated endpoints in
     tenths of a km checked by fourth powers; against the separation LIGO and Virgo state for GW150914, equal Newtonian
     point masses about 350 km apart at its 75 Hz orbit (PRL 116, 061102 (2016)), that separation in G M / c^2 by
     carry, which of the touching separations are wider than it, and each one's ratio to it.

Usage: python3 -I term13_frozen.py <src of main at 0df0e8385>
"""

import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import mesh, step  # noqa: E402
from tensor24.engine.state import Gearing, Layout, Plan, Read, State  # noqa: E402
from tensor24.runner.board import board  # noqa: E402
from tensor24.runner.load import geometry  # noqa: E402

GRIP = 15162856759112389 * 1000 * 1000
REST = 6 * GRIP
matter_row, light_row, slot00, slot_xx = 0, 1, 2, 6  # rows as in g2_static.py: matter, light, the 00 slot, xx (yy, zz)
ROWS = 12
no_plan = Plan(*(np.zeros(0, dtype=np.intp),) * 3, np.zeros(0, dtype=object), np.zeros(0, dtype=np.intp))
no_read = Read(np.zeros(0, dtype=np.intp), np.zeros(0, dtype=object), np.zeros(0, dtype=np.intp))
reads_ii = Read(np.array([slot_xx, slot_xx, slot_xx + 1, slot_xx + 1, slot_xx + 2, slot_xx + 2], dtype=np.intp),
                np.ones(6, dtype=object), np.arange(6, dtype=np.intp))


def fraction(num, den):
    """A ratio in lowest terms, by Euclid's steps in carries, as num/den with den above 0."""
    if den < 0:
        num, den = -num, -den
    a, b = abs(num), den
    while b:
        a, b = b, carry(a, b, 0)[1]
    return f"{carry(num, a, 0)[0]}/{carry(den, a, 0)[0]}" if a else "0/1"


# whole-number tools: ratios as pairs, polynomials as lists of whole coefficients (lowest power first), rational
# functions as pairs of polynomials, power series as lists of ratios, and stated endpoints checked by powers
def quo(num, den):
    """num over den rounded down: the quotient of Rule3's carry."""
    return carry(num, den, 0)[0]


def red(num, den):
    """A ratio as a pair in lowest terms, den above 0, by Euclid's steps in carries."""
    if den < 0:
        num, den = -num, -den
    a, b = abs(num), den
    while b:
        a, b = b, carry(a, b, 0)[1]
    return (quo(num, a), quo(den, a)) if a else (0, 1)


def radd(x, y):
    return red(x[0] * y[1] + y[0] * x[1], x[1] * y[1])


def rsub(x, y):
    return red(x[0] * y[1] - y[0] * x[1], x[1] * y[1])


def rmul(x, y):
    return red(x[0] * y[0], x[1] * y[1])


def rdiv(x, y):
    return red(x[0] * y[1], x[1] * y[0])


def show(x):
    """A ratio pair as num/den."""
    return fraction(x[0], x[1])


def plain(x):
    """A ratio pair as a whole number where it is one, else as num/den."""
    return str(x[0]) if x[1] == 1 else fraction(x[0], x[1])


def below(x, y):
    """x < y for two ratio pairs."""
    return x[0] * y[1] < y[0] * x[1]


def trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def padd(p, q):
    size = max(len(p), len(q))
    return trim([(p[i] if i < len(p) else 0) + (q[i] if i < len(q) else 0) for i in range(size)])


def pscale(p, c):
    return trim([c * x for x in p])


def psub(p, q):
    return padd(p, pscale(q, -1))


def pmul(p, q):
    out = [0] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            out[i + j] += x * y
    return trim(out)


def pder(p):
    return trim([i * p[i] for i in range(1, len(p))] or [0])


def peval(p, x):
    """p at the ratio x = (n, d) by Horner's steps on whole numbers: (c_k n + c_(k-1) d) n + c_(k-2) d^2 ..."""
    acc, power = p[-1], 1
    for c in reversed(p[:-1]):
        power = power * x[1]
        acc = acc * x[0] + c * power
    return red(acc, power)


def const(c, d=1):
    return ([c], [d])


def fmul(f, h):
    return (pmul(f[0], h[0]), pmul(f[1], h[1]))


def fdiv(f, h):
    return (pmul(f[0], h[1]), pmul(f[1], h[0]))


def fsub(f, h):
    return (psub(pmul(f[0], h[1]), pmul(h[0], f[1])), pmul(f[1], h[1]))


def fder(f):
    """The quotient rule: (n / d)' = (n' d - n d') / d^2."""
    return (psub(pmul(pder(f[0]), f[1]), pmul(f[0], pder(f[1]))), pmul(f[1], f[1]))


def feq(f, h):
    """f = h as rational functions: the cross products equal coefficient by coefficient."""
    return pmul(f[0], h[1]) == pmul(h[0], f[1])


def feval(f, x):
    return rdiv(peval(f[0], x), peval(f[1], x))


def square(s):
    return s * s


def fourth(s):
    return square(square(s))


def within(power, low, high, n, d):
    """Two stated endpoints checked by powers, no root found and none searched for:
    power(low) d <= n < power(high) d."""
    return power(low) * d <= n < power(high) * d


def decimal(num, den, scale):
    """num / den rounded down to the digits of scale, a power of 10, as text: the whole part, then each digit by a
    carry."""
    sign = "-" if (num < 0) != (den < 0) and num else ""
    whole, part = carry(quo(abs(num) * scale, abs(den)), scale, 0)
    digits, place = "", scale
    while place > 1:
        place = quo(place, 10)
        digit, part = carry(part, place, 0)
        digits += str(digit)
    return f"{sign}{whole}.{digits}"


def between(low, high, scale):
    """Two stated endpoints, low / scale and high / scale, as text."""
    return f"between {decimal(low, scale, scale)} and {decimal(high, scale, scale)}"


TERMS = 5  # power series kept to e^4


def s_sum(xs):
    total = (0, 1)
    for x in xs:
        total = radd(total, x)
    return total


def s_add(p, q):
    return [radd(p[k], q[k]) for k in range(TERMS)]


def s_scale(p, c):
    return [rmul(x, c) for x in p]


def s_mul(p, q):
    return [s_sum([rmul(p[i], q[k - i]) for i in range(k + 1)]) for k in range(TERMS)]


def s_inv(p):
    """1 / p for a series with p[0] = 1, coefficient by coefficient."""
    out = [(1, 1)]
    for k in range(1, TERMS):
        out.append(rsub((0, 1), s_sum([rmul(p[i], out[k - i]) for i in range(1, k + 1)])))
    return out


def s_const(c):
    return [(c, 1)] + [(0, 1)] * (TERMS - 1)


def s_text(p, last=TERMS):
    """A series as 1 + 2 e + (3/2) e^2 ..., to e^(last - 1)."""
    out = ""
    for k in range(last):
        num, den = p[k]
        if num == 0:
            continue
        size = plain((abs(num), den))
        size = f"({size})" if den != 1 else size
        size = "" if (abs(num), den) == (1, 1) and k else size
        name = "" if k == 0 else (" e" if k == 1 else f" e^{k}")
        sign = ("-" if num < 0 else "") if not out else (" - " if num < 0 else " + ")
        out += sign + (size + name).strip()
    return out


# (a) the strong field's pull on the act, at the act's rest = 6 g
nb6 = board((6, 6, 6))
sites6 = nb6.shape[1]
spokes6, meshes6 = geometry(nb6, 3)
S, K = 1000, 12
g = 2 * S
rest6 = 6 * g  # = K S, so u = c00 / rest = U / S
seq = 20261030
U = []
for _ in range(sites6):
    _, seq = carry(1103515245 * seq + 12345, 2147483648, 0)
    U.append(carry(seq, 2 * S + 1, 0)[1])  # 0 to 2 S: u = U / S from 0 to 2, the grips 1 - (gamma / 2)(u_i + u_j)
lay6 = Layout(nb6, spokes6, meshes6, np.full((1, 3 * sites6), g, dtype=object),
              Gearing(*(np.ones((ROWS, 1), dtype=object),) * 4), no_plan, no_read, reads_ii)
lines_a = []
for gamma in (1, 2, 3, 7):
    a_f = np.zeros((ROWS, sites6), dtype=object)
    a_f[slot00, :] = [K * x for x in U]
    for d in range(3):
        a_f[slot_xx + d, :] = [-gamma * x for x in U]
    # the tie in the act's own reading, v = c_ii / g = -(gamma / 2) c00 / rest: 2 rest c_ii = -gamma g c00
    tie = all(2 * rest6 * int(a_f[slot_xx + d, i]) == -gamma * g * int(a_f[slot00, i])
              for d in range(3) for i in range(sites6))
    pulled = mesh.pull(lay6, a_f)
    f00 = pulled[slot00]
    w = [g * x - gamma * x * x for x in U]
    exact = all(int(f00[i]) == K * sum(w[int(nb6[k, i])] - w[i] for k in range(6)) for i in range(sites6))
    # g rest Lap(w) with w = u - (gamma / 2) u^2 and u = c00 / rest: 2 rest pull = g Lap(2 rest c00 - gamma c00^2)
    c = [K * x for x in U]
    w2 = [2 * rest6 * x - gamma * x * x for x in c]
    in_w = all(2 * rest6 * int(f00[i]) == g * sum(w2[int(nb6[k, i])] - w2[i] for k in range(6)) for i in range(sites6))
    ii = all(K * int(pulled[slot_xx + d, i]) == -gamma * int(f00[i]) for d in range(3) for i in range(sites6))
    grips = [g - gamma * (U[i] + U[int(nb6[k, i])]) for i in range(sites6) for k in range(0, 6, 2)]
    lines_a.append(f"gamma {gamma}: the tie v = -(gamma / 2) u: {tie}; the pull equals 12 Lap(g U - gamma U^2) at all"
                   f" {sites6} Node-clocks: {exact}, that is g rest Lap(w): {in_w}; 12 pull_ii = -gamma pull_00 on"
                   f" xx, yy and zz at all {sites6}: {ii}; of the {len(grips)} Meshes, {sum(int(x > 0) for x in grips)}"
                   f" with a grip above 0, {sum(int(x == 0) for x in grips)} at 0 and"
                   f" {sum(int(x < 0) for x in grips)} below it")
# the first text's lay, c00 = 12 U and c_ii = -7 gamma U at the grip 14,000, read against the act's rest 6 x 14,000
first_text = [plain(red(2 * 6 * 14000 * 7 * gamma, 14000 * K)) for gamma in (1, 2)]
print(f"(a) the 00 slot laid at {K} U and each ii slot at -gamma U, the grip g = 2 S = {g} and the act's rest 6 g ="
      f" {rest6} = {K} S, so u = c00 / rest = U / S and v = c_ii / g = -(gamma / 2) u, U from 0 to 2 S (S = {S}),"
      f" w = u - (gamma / 2) u^2: " + "; ".join(lines_a) + f"; the first text's lay (each ii slot at -7 gamma U, the"
      f" grip 14000) read against the act's rest: gamma {first_text[0]} and {first_text[1]}")


# (a2) the 00 slot's board mean on the act as built
def drift(shape, rounds, held):
    """The 00 row alone on a wrapped board, every grip g, laid at +rest / 1000 on site 0 and -rest / 1000 on its +x
    neighbour, at rest, its teeth W = rest + c00 (or held at rest): per 2,000 rounds the board's sum T and the largest
    |N c00 - T|; at every round the identity N (N rest + T) d^2 T + SUM D d^2 D = N^2 SUM (r - r+), D = N c00 - T
    (N^2 times N (rest + m) d^2 m = -SUM delta d^2 delta + SUM (r - r+)); the rounds where the swing's part
    -SUM D d^2 D stands above 0 and its sum over the run; N^2 N W, the most the fine teeth's part can add over the run
    (it telescopes to N^2 times the fine teeth's first sum less their last, each below N W); the largest |c00|."""
    nb = board(shape)
    n = nb.shape[1]
    spokes, meshes = geometry(nb, 3)
    one = np.ones((1, 1), dtype=object)
    self_read = Read(np.zeros(1, dtype=np.intp), np.ones(1, dtype=object), np.zeros(1, dtype=np.intp))
    lay = Layout(nb, spokes, meshes, np.full((1, 3 * n), GRIP, dtype=object),
                 Gearing(REST * one, one, one.copy(), one.copy()), no_plan, no_read if held else self_read, no_read)
    a = np.zeros((1, n), dtype=object)
    a[0, 0], a[0, int(nb[0, 0])] = quo(REST, 1000), -quo(REST, 1000)
    s = State(a, a.copy(), np.full((1, n), quo(REST, 2), dtype=object), np.zeros((1, n), dtype=object))
    marks, holds, above, swing_sum, top, w_top = [], True, 0, 0, 0, REST
    for t in range(1, rounds + 1):
        before, s = s, step.tick(lay, s)
        now, past, after = before.a[0], before.b[0], s.a[0]
        total = int(now.sum())
        d2t = int(after.sum()) - 2 * total + int(past.sum())
        swing = int(((n * now - total) * (n * (after - 2 * now + past) - d2t)).sum())
        teeth = int(before.r[0].sum()) - int(s.r[0].sum())
        holds = holds and (held or n * (n * REST + total) * d2t + swing == n * n * teeth)
        above += int(swing < 0)
        swing_sum -= swing
        top = max(top, max(abs(int(x)) for x in after))
        w_top = max(w_top, REST + max(int(x) for x in after))
        if carry(t, 2000, 0)[1] == 0:
            new_total = int(after.sum())
            marks.append((new_total, max(abs(n * int(x) - new_total) for x in after)))
    return n, marks, holds, above, swing_sum, n * n * n * w_top, top


def means(n, marks):
    return ", ".join(decimal(total * 1000, n * REST, 10) for total, _ in marks)


n8, marks8, holds8, above8, swing8, most8, _ = drift((8, 1, 1), 16000, False)
n216, marks216, holds216, above216, swing216, most216, _ = drift((6, 6, 6), 6000, False)
n8h, marks8h, _, _, _, _, top8h = drift((8, 1, 1), 16000, True)
# the swing's sum against the most the fine teeth can add: the stated powers of ten, checked by products
tens8 = 10**19 * most8 <= swing8 < 10**20 * most8
tens216 = 10**18 * most216 <= swing216 < 10**19 * most216
print(f"(a2) the 00 slot's board mean on the act as built (a wrapped board, no notch, every grip g, every row's teeth"
      f" W = rest + c00, the 00 row alone), the 00 row laid at +rest / 1000 and -rest / 1000 on two neighbouring sites,"
      f" at rest: on the ring of 8 the mean in thousandths of rest at rounds 2,000 to 16,000: {means(n8, marks8)} (the"
      f" swing about it at most {max(quo(sw * 10**6, n8 * REST) for _, sw in marks8)} millionths of rest); on the 6 by"
      f" 6 by 6 board at rounds 2,000, 4,000 and 6,000: {means(n216, marks216)}; the gear's carry, the pulls summing to"
      f" 0 on the wrapped board, gives N (rest + m) d^2 m = -SUM delta d^2 delta + SUM (r - r+) (m the mean,"
      f" delta = c00 - m, r the fine teeth), exactly at every round: {holds8} on the ring, {holds216} on the board; the"
      f" swing's part -SUM delta d^2 delta stands above 0 at {above8:,} of the ring's 16,000 rounds and {above216:,} of"
      f" the board's 6,000, and summed over them it is above 10^19 and 10^18 times the most the fine teeth's part can"
      f" add (N W: it telescopes to the fine teeth's first sum less their last), the powers stated and checked by"
      f" products, 10^19 <= the ring's ratio < 10^20: {tens8}, 10^18 <= the board's < 10^19: {tens216}; the mutant, the"
      f" same lay with the teeth held at rest, on the ring: the mean at rounds 2,000 to 16,000:"
      f" {means(n8h, marks8h)} thousandths of rest, the largest |c00| over the 16,000 rounds"
      f" {decimal(top8h * 1000, REST, 10)} thousandths of rest")

# (b) light where a grip vanishes and where it turns negative: a ring of 8 on the x axis
nb8 = board((8, 1, 1))
sites8 = nb8.shape[1]
spokes8, meshes8 = geometry(nb8, 3)
ones = np.ones((ROWS, 1), dtype=object)
clock = Read(np.full(ROWS, slot00, dtype=np.intp), np.ones(ROWS, dtype=object), np.arange(ROWS, dtype=np.intp))


def ring(cut_grip, negative=None):
    """The ring's grips: GRIP on every +x Mesh but those from site 3 and site 7 (to sites 4 and 0), which carry
    cut_grip; with negative, the +x Mesh from site 1 carries that grip instead of GRIP."""
    grips = np.full((1, 3 * sites8), GRIP, dtype=object)
    grips[0, 3], grips[0, 7] = cut_grip, cut_grip
    if negative is not None:
        grips[0, 1] = negative
    return Layout(nb8, spokes8, meshes8, grips, Gearing(REST * ones, ones, ones.copy(), ones.copy()), no_plan, clock,
                  no_read)


def light_lay():
    a = np.zeros((ROWS, sites8), dtype=object)
    a[light_row, :4] = [10**6, -(10**6), 10**6, -(10**6)]
    return State(a, a.copy(), np.full((ROWS, sites8), carry(REST, 2, 0)[0], dtype=object),
                 np.zeros((ROWS, sites8), dtype=object))


def far_side(lay, rounds=4000):
    """The largest |light| on sites 4 to 7 over the rounds, and the round light first passes 10^60 (or 0)."""
    s, top, gone = light_lay(), 0, 0
    for t in range(1, rounds + 1):
        s = step.tick(lay, s)
        top = max(top, max(abs(int(v)) for v in s.a[light_row, 4:]))
        if max(abs(int(v)) for v in s.a[light_row]) > 10**60:
            gone = t
            break
    return top, gone


def pieces(lay):
    """The sites the Meshes with a grip other than 0 hold together: each Mesh joins its site to the site's + neighbour
    on its axis (load.geometry), the pieces grown site by site."""
    nb, grips = lay.nb, lay.grip
    n = nb.shape[1]
    piece = list(range(n))
    for axis in range(3):
        for i in range(n):
            j = int(nb[2 * axis, i])
            if int(grips[0, axis * n + i]) != 0 and piece[i] != piece[j]:
                old, new = max(piece[i], piece[j]), min(piece[i], piece[j])
                piece = [new if p == old else p for p in piece]
    return [[i for i in range(n) if piece[i] == p] for p in sorted(set(piece))]


top0, gone0 = far_side(ring(0))
top_small, gone_small = far_side(ring(carry(GRIP, 100, 0)[0]))
top_neg, gone_neg = far_side(ring(GRIP, negative=-carry(GRIP, 2, 0)[0]))
split = pieces(ring(0))
print(f"(b) a ring of 8, light laid on sites 0 to 3 at 10^6 (alternating), 4,000 rounds: with the Meshes 3-4 and 7-0"
      f" at a grip of 0, the largest |light| on sites 4 to 7 is {top0} (runs away: {bool(gone0)}), a test that cannot"
      f" fail: the Meshes left with a grip hold the ring in {len(split)} pieces, sites {split[0]} and {split[1]}; at a"
      f" grip of g / 100, {top_small} (runs away: {bool(gone_small)}); with every grip g but the Mesh 1-2 at -g / 2,"
      f" light passes 10^60 at round {gone_neg}")

# (b2) where a negative grip runs away: Foster's theorem, and runs on the act
two = np.ones((2, 1), dtype=object)
clock2 = Read(np.zeros(2, dtype=np.intp), np.ones(2, dtype=object), np.arange(2, dtype=np.intp))  # row 0 the 00 slot


def foster(nb):
    """The grip the rest of a wrapped board holds between one Mesh's ends, over g: by Foster's theorem the Meshes'
    effective resistances sum to the sites less 1, alike on every Mesh, so each Mesh's is (sites - 1) / Meshes in 1 / g,
    its effective grip Meshes / (sites - 1) g, of which the Mesh itself holds g. Meshes joining a site to itself (an
    axis of side 1) are no Meshes here."""
    n = nb.shape[1]
    joined = sum(int(int(nb[2 * axis, i]) != i) for axis in range(3) for i in range(n))
    return red(joined - (n - 1), n - 1), joined, n


def runaway(shape, num, den, rounds=4000):
    """Light (row 1) laid at +-10^6 across the +x Mesh of site 0, that Mesh at num g / den and every other grip g, the
    teeth reading the 00 slot (row 0, idle at 0): the largest |light| over the rounds, and the round it passes 10^60
    (0 if never)."""
    nb = board(shape)
    n = nb.shape[1]
    spokes, meshes = geometry(nb, 3)
    grips = np.full((1, 3 * n), GRIP, dtype=object)
    grips[0, 0] = quo(num * GRIP, den)
    lay = Layout(nb, spokes, meshes, grips, Gearing(REST * two, two, two.copy(), two.copy()), no_plan, clock2, no_read)
    a = np.zeros((2, n), dtype=object)
    a[1, 0], a[1, int(nb[0, 0])] = 10**6, -(10**6)
    s = State(a, a.copy(), np.full((2, n), quo(REST, 2), dtype=object), np.zeros((2, n), dtype=object))
    top = 0
    for t in range(1, rounds + 1):
        s = step.tick(lay, s)
        big = max(abs(int(v)) for v in s.a[1])
        if big > 10**60:
            return top, t
        top = max(top, big)
    return top, 0


rows_b2, agree = [], True
for shape, name in (((8, 1, 1), "the ring of 8"), ((6, 6, 6), "the 6 by 6 by 6 board")):
    eff, joined, n = foster(board(shape))
    runs = []
    for num, den in (((-1, 8), (-1, 6), (-1, 2)) if shape[1] == 1 else ((-1, 2), (-2, 1), (-3, 1))):
        top, gone = runaway(shape, num, den)
        agree = agree and bool(gone) == below(eff, (-num, den))
        label = f"{num}/{den} g" if den != 1 else f"{num} g"
        runs.append(f"{label}: passes 10^60 at round {gone}" if gone else f"{label}: never, the largest |light| {top}")
    rows_b2.append(f"{name} ({n} sites, {joined} Meshes), the rest's effective grip {show(eff)} g: " + "; ".join(runs))
print("(b2) where a negative grip runs away, light laid at +-10^6 across one Mesh at a negative grip, every other grip"
      " g, 4,000 rounds, against the grip the rest of the board holds between that Mesh's ends by Foster's theorem (the"
      " Meshes' effective resistances sum to the sites less 1, alike on every Mesh of a wrapped board): "
      + "; ".join(rows_b2) + f"; each runs away exactly where its size is past the rest's effective grip: {agree}")

# (c1) the slot form's own exterior, gamma = 1: x = p / q, r = 4 q^2 / (q^2 - p^2), u = 1 - x
xs = ((1, 2), (1, 10), (1, 100), (1, 1000))
rows_c1 = []
for p, q in xs:
    r_num, r_den = 4 * q * q, q * q - p * p
    u_num, u_den = q - p, q
    w_ok = (u_num * 2 * u_den - u_num * u_num) * r_num == 2 * 2 * u_den * u_den * r_den  # u - u^2 / 2 = 2 / r
    n2_num, n2_den = q, 2 * q - p  # N^2 = 1 / (2 - x)
    rows_c1.append(f"x = {fraction(p, q)}: r = {fraction(r_num, r_den)}, u = {fraction(u_num, u_den)}, grip / g ="
                   f" {fraction(p, q)}, N^2 = {fraction(n2_num, n2_den)}, light's speed squared"
                   f" {fraction(n2_num * p, n2_den * q)}; u - u^2 / 2 = 2 / r: {w_ok}")


def tied(gamma, m0=1, mi=1):
    """The exterior as rational functions of x = grip / g: r = 4 gamma Mi / (1 - x^2), u = (M0 / Mi)(1 - x) / gamma."""
    return ([4 * gamma * mi], [1, 0, -1]), ([m0, -m0], [gamma * mi])


def flux00(r_x, u_x):
    """The 00 row's flux through the grips, r^2 x du / dr, du / dr = (du / dx) / (dr / dx) by the quotient rule."""
    return fmul(fmul(fmul(r_x, r_x), ([0, 1], [1])), fdiv(fder(u_x), fder(r_x)))


rows_g, rows_c1g, rows_c1z = [], [], []
for gamma in (1, 2, 3):
    r_x, u_x = tied(gamma)
    r0, u0 = feval(r_x, (0, 1)), feval(u_x, (0, 1))  # where the grips vanish, x = 0
    n2_0 = rdiv((1, 1), radd((1, 1), u0))
    if gamma < 3:
        rows_g.append(f"gamma {gamma}: the grips vanish at r = {plain(r0)}, u = {show(u0)}, N^2 = {show(n2_0)}")
    w_x = fsub(u_x, fmul(([gamma], [2]), fmul(u_x, u_x)))
    flux = flux00(r_x, u_x)
    rows_c1g.append(f"gamma {gamma}: w = 2 / r: {feq(w_x, fdiv(const(2), r_x))}; the flux equals -2:"
                    f" {feq(flux, const(-2))}; at x = " + ", ".join(fraction(p, q) for p, q in xs) + ": "
                    + ", ".join(plain(feval(flux, (p, q))) for p, q in xs))
    rows_c1z.append(f"gamma {gamma}: r = {plain(r0)}, u = {show(u0)}, N^2 = {show(n2_0)}, W ="
                    f" {show(radd((1, 1), u0))} rest")
print("(c1) arithmetic alone, the slot form's exterior at gamma = 1, w = u - u^2 / 2 = 2 / r (r and u built from"
      " x = grip / g, so this holds by construction): " + "; ".join(rows_c1) + "; " + "; ".join(rows_g))
print("(c1) arithmetic alone, at gamma 1, 2 and 3, as rational functions of x = grip / g with r = 4 gamma / (1 - x^2)"
      " and u = (1 - x) / gamma: w = u - (gamma / 2) u^2 against 2 / r, and the 00 row's flux r^2 x du / dr by the"
      " quotient rule against -2: " + "; ".join(rows_c1g) + "; where the grips vanish (x = 0): " + "; ".join(rows_c1z))

rows_un = []
for m0, mi, low, high in ((23, 19, 161905, 161906), (5, 4, 167185, 167186)):  # the bound's stated ends, in millionths
    r_x, u_x = tied(1, m0, mi)
    h_x = ([-1, 0, 1], [4])  # the ii slots' own field v + v^2 with 1 + 2 v = x
    k = mi  # gamma Mi, gamma = 1: the spheres R^4 = r^5 / (r - 4 k)
    least = padd([0, 0, 0, 0, 0, 1], pscale([-4 * k, 1], -3125 * k**4)) == pmul(
        pmul([-5 * k, 1], [-5 * k, 1]), [500 * k**3, 75 * k**2, 10 * k, 1])
    ends = within(fourth, low, high, m0**4 * 10**24, 3125 * mi**4)
    rows_un.append(f"M0 / Mi = {m0}/{mi}: the 00 flux r^2 x du / dr = -2 M0: {feq(flux00(r_x, u_x), const(-2 * m0))};"
                   f" the ii field v + v^2 = -gamma Mi / r: {feq(h_x, fdiv(const(-mi), r_x))}; the least sphere at"
                   f" r = 5 gamma Mi, R^4 = 3125 (gamma Mi)^4, factorized: {least}; the bound G M0 / (c^2 R)"
                   f" {between(low, high, 10**6)} ({low}^4 x 3125 x {mi}^4 <= {m0}^4 x 10^24 < {high}^4 x 3125 x"
                   f" {mi}^4: {ends})")
print("(c1) arithmetic alone, the untied exterior at gamma = 1, M0 the 00 slot's mass and Mi the ii slots' (both in"
      " one unit, r in G / c^2 times it): x^2 = 1 - 4 gamma Mi / r, u = (M0 / Mi)(1 - x) / gamma, the bound"
      " (M0 / Mi) 5^(-5/4) / gamma between stated endpoints, checked by fourth powers, no root found: "
      + "; ".join(rows_un))

nicer = ((156, f"PSR J0030+0451, {decimal(134, 100, 100)} solar masses at {decimal(1271, 100, 100)} km (Riley and"
               f" others 2019)"),
         (247, f"PSR J0740+6620, {decimal(2072, 1000, 1000)} solar masses at {decimal(1239, 100, 100)} km (Riley and"
               f" others 2021)"))
rows_p = []
# p = k / 100 and the bound's stated ends, in ten-thousandths
for k, low, high in ((1, 1391, 1392), (2, 1446, 1447), (3, 1502, 1503), (4, 1560, 1561)):
    ends = within(fourth, low, high, (100 + 3 * k) ** 4 * 10**16, 3125 * (100 - k) ** 4)
    rows_p.append(f"p = {k}/100: {between(low, high, 10**4)} ({ends})")
reach = []
for (c, name), (low, high) in zip(nicer, ((399, 400), (1747, 1748))):  # p = j / 10^4 at the stated ends
    short = (10**4 + 3 * low) ** 4 * 1000**4 < c**4 * 3125 * (10**4 - low) ** 4  # the bound below c at low
    there = (10**4 + 3 * high) ** 4 * 1000**4 >= c**4 * 3125 * (10**4 - high) ** 4  # at c or above at high
    reach.append(f"{decimal(c, 1000, 1000)} ({name.split(',')[0]}) at p {between(low, high, 10**4)}"
                 f" ({short and there})")
print("(c1) arithmetic alone, G2's pressure reading (the 1/r terms M + 3 P and M - P, so M0 / Mi = (1 + 3 p) / (1 - p),"
      " p = P / M, gamma = 1): the bound 5^(-5/4) (1 + 3 p) / (1 - p) between stated endpoints B and B', checked by"
      " fourth powers, B^4 3125 (1 - p)^4 <= (1 + 3 p)^4 < B'^4 3125 (1 - p)^4, no root found: " + "; ".join(rows_p)
      + "; it reaches, the bound below it at the first stated p and at it or above at the second, by fourth powers: "
      + " and ".join(reach))

# (c2) general relativity in isotropic radius as rational functions of m = 1 / (2 r): N = (1 - m) / (1 + m),
# A = (1 + m)^2, r = 1 / (2 m), dm / dr = -2 m^2; the slot form's flux r^2 A^-2 du / dr with u = N^-2 - 1 against
# general relativity's lapse flux r^2 A dN / dr, both by the quotient rule
n_gr, a_gr, r_m, dm_dr = ([1, -1], [1, 1]), ([1, 2, 1], [1]), ([1], [0, 2]), ([0, 0, -2], [1])
u_gr = fsub(fdiv(const(1), fmul(n_gr, n_gr)), const(1))
grip_gr = fdiv(const(1), fmul(a_gr, a_gr))
slot_flux = fmul(fmul(fmul(r_m, r_m), grip_gr), fmul(fder(u_gr), dm_dr))
gr_flux = fmul(fmul(fmul(r_m, r_m), a_gr), fmul(fder(n_gr), dm_dr))
rows_c2 = []
for r_num, r_den in ((1, 1), (2, 1), (4, 1), (10, 1)):
    m_at = red(r_den, 2 * r_num)  # m = 1 / (2 r)
    rows_c2.append(f"r = {fraction(r_num, r_den)}: the slot form's flux {show(feval(slot_flux, m_at))}, general"
                   f" relativity's {show(feval(gr_flux, m_at))}")
closed = feq(slot_flux, ([-2], pmul(pmul([1, 0, -1], [1, 0, -1]), [1, 0, -1])))
print("(c2) arithmetic alone, general relativity's static field in isotropic radius: the slot form's flux"
      " r^2 (grip / g) du / dr (constant where the slot form's 00 equation holds) against general relativity's"
      " r^2 A dN / dr, both by the quotient rule on N = (1 - m) / (1 + m) and A = (1 + m)^2 with m = G M / (2 c^2 r),"
      " u = N^-2 - 1 and grip / g = A^-2: " + "; ".join(rows_c2) + f"; as rational functions of m, the slot form's"
      f" flux equals -2 / (1 - m^2)^3: {closed}, general relativity's equals 1: {feq(gr_flux, const(1))}")

# (c3) the horizon in the act's terms: r = 1/2, m = 1
n_h, a_h = feval(n_gr, (1, 1)), feval(a_gr, (1, 1))
rows_c3 = []
for gamma in (1, 2, 3):
    u0 = feval(tied(gamma)[1], (0, 1))
    rows_c3.append(f"gamma {gamma}: u = {show(u0)}, W = {show(radd((1, 1), u0))} rest")
grip_h = rdiv((1, 1), rmul(a_h, a_h))
print(f"(c3) arithmetic alone, general relativity's horizon at r = 1/2 (m = 1), from N = (1 - m) / (1 + m) and"
      f" A = (1 + m)^2: N = {show(n_h)}, A = {show(a_h)}, the grip over g = A^-2 = {show(grip_h)}; N^2 ="
      f" {show(rmul(n_h, n_h))}, so the clocks' teeth W = rest / N^2 have no bound at a finite grip; the slot form's"
      f" field reaches u = 1 / gamma, W = (1 + 1 / gamma) rest, where its grips vanish (x = 0): " + "; ".join(rows_c3))

# (c4) the reading of one depth against a uniform background
rows_c4 = []
for c_bar_num, label in ((0, "0"), (1, "+rest / 10"), (-1, "-rest / 10")):
    # W_A = rest + c_bar + rest / 50, W_B = rest + c_bar; N_A^2 / N_B^2 = W_B / W_A; the depth read: W_A / W_B - 1
    wb = 50 * (10 + c_bar_num)  # in units of rest / 500
    wa = wb + 10
    rows_c4.append(f"background {label}: W_A / W_B - 1 = {fraction(wa - wb, wb)}")
print("(c4) arithmetic alone, no clock run: one depth of rest / 50 read by two clocks, W_A / W_B - 1 (the square of"
      " their rate's ratio, less 1): " + "; ".join(rows_c4) + " (a first-order dependence on the uniform part)")

# (c5) the least sphere of the slot form's exterior: R^4 = r^5 / (r - 4), r = k / 100
least = None
for k in range(401, 2001):
    num, den = k**5, 10**8 * (k - 400)  # (k / 100)^5 / (k / 100 - 4) = k^5 / (10^8 (k - 400))
    if least is None or num * least[2] < least[1] * den:
        least = (k, num, den)
k0, r4_num, r4_den = least
# the most compact body: (G M / (c^2 R))^4 = r4_den / r4_num, against NICER's 156 and 247 thousandths (fourth powers)
rows_c5 = [f"{fraction(c, 1000)} for {name}: reachable {c**4 * r4_num <= r4_den * 1000**4}" for c, name in nicer]
bound_ends = within(fourth, 133748, 133749, r4_den * 10**24, r4_num)  # the stated ends, in millionths
print(f"(c5) arithmetic alone, the slot form's spheres at gamma = 1, R^4 = r^5 / (r - 4): the least over a grid of"
      f" r = 401/100 to 20 in steps of 1/100 at r = {fraction(k0, 100)}, R^4 = {fraction(r4_num, r4_den)}"
      f" (G M / c^2)^4, so no body more compact than (G M / (c^2 R))^4 = {fraction(r4_den, r4_num)}, G M / (c^2 R)"
      f" {between(133748, 133749, 10**6)} (the endpoints stated, checked by fourth powers, no root found:"
      f" {bound_ends}); the compactness G M / (c^2 R) " + "; ".join(rows_c5))
rows_f, rows_b = [], []
# the stated ends: R = 5^(5/4) gamma in thousandths, and the bound 5^(-5/4) / gamma in millionths (gamma 1 to 3)
ends_r = ((7476, 7477), (14953, 14954), (22430, 22431), (29906, 29907))
ends_b = ((133748, 133749), (66874, 66875), (44582, 44583))
for gamma in (1, 2, 3, 4):
    left = padd([0, 0, 0, 0, 0, 1], pscale([-4 * gamma, 1], -3125 * gamma**4))
    cubic = [500 * gamma**3, 75 * gamma**2, 10 * gamma, 1]
    right = pmul(pmul([-5 * gamma, 1], [-5 * gamma, 1]), cubic)
    r_low, r_high = ends_r[gamma - 1]
    r_ends = within(fourth, r_low, r_high, 3125 * gamma**4 * 10**12, 1)
    rows_f.append(f"gamma {gamma}: {left == right}, the cubic's coefficients above 0: {all(c > 0 for c in cubic)};"
                  f" R = 5^(5/4) gamma {between(r_low, r_high, 1000)} ({r_low}^4 <= {3125 * gamma**4} x 10^12 <"
                  f" {r_high}^4: {r_ends})")
    if gamma < 4:
        b_low, b_high = ends_b[gamma - 1]
        b_ends = within(fourth, b_low, b_high, 10**24, 3125 * gamma**4)
        rows_b.append(f"gamma {gamma}: {between(b_low, b_high, 10**6)} ({b_low}^4 x {3125 * gamma**4} <= 10^24 <"
                      f" {b_high}^4 x {3125 * gamma**4}: {b_ends})")
print("(c5) arithmetic alone, r^5 - 3125 gamma^4 (r - 4 gamma) = (r - 5 gamma)^2 (r^3 + 10 gamma r^2 + 75 gamma^2 r"
      " + 500 gamma^3) as polynomials in r, coefficient by coefficient, so R^4 - 3125 gamma^4 = (r - 5 gamma)^2 times"
      " the cubic over r - 4 gamma stands above 0 on r > 4 gamma except at r = 5 gamma, the least there unique and"
      " global; R and the bound between stated endpoints, checked by fourth powers, no root found: " + "; ".join(rows_f)
      + "; the bound G M / (c^2 R) = 5^(-5/4) / gamma: " + "; ".join(rows_b))

# (c6) the surface of vanishing grip is never part of a static field
rows_c6 = []
for gamma in (1, 2, 3, 5):
    # 2 w = 2 u - gamma u^2, so 1 - 2 gamma w = 1 - gamma (2 u - gamma u^2)
    rows_c6.append(f"gamma {gamma}: {pmul([1, -gamma], [1, -gamma]) == padd([1], pscale([0, 2, -gamma], -gamma))}")
rows_ball = []
for radius in (5, 6, 7):
    # w = a - b r^2 inside, 2 / r outside (M = 1): the value and the slope agree at r = s
    b_s = rdiv((2, radius * radius), (2 * radius, 1))  # -2 b s = -2 / s^2
    a_s = radd((2, radius), rmul(b_s, (radius * radius, 1)))  # a - b s^2 = 2 / s
    side = "above" if below((1, 2), a_s) else ("at" if a_s == (1, 2) else "below")
    rows_ball.append(f"s = {radius}: b = {show(b_s)}, w(0) = a = {show(a_s)}, {side} 1/2, 1 - 2 w(0) ="
                     f" {show(rsub((1, 1), rmul((2, 1), a_s)))}, at the surface w = {show(red(2, radius))}")
print("(c6) arithmetic alone, the surface of vanishing grip is never part of a static field: (1 - gamma u)^2 ="
      " 1 - 2 gamma w with w = u - (gamma / 2) u^2, as polynomials in u, coefficient by coefficient: "
      + "; ".join(rows_c6) + ", so 1 - 2 gamma w >= 0 and w <= 1 / (2 gamma) for every real u, on either branch:"
      " inside r = 4 gamma, where w = 2 / r passes 1 / (2 gamma), no real u stands at all; a ball of radius s with a"
      " uniform w-source (M = 1, gamma = 1), w = a - b r^2 inside matched to 2 / r at r = s: " + "; ".join(rows_ball)
      + ": the field is largest at the centre, w(0) = 3 M / s, so such a ball stands only for s >= 6 gamma M, and"
      " outside it w < 1 / (2 gamma): every grip there stands above 0")

# (c7) light's critical impact parameter, b = A r / N at the turning point
r_x, u_x = tied(1)
b2_slot = fmul(fmul(r_x, r_x), ([2, -1], [0, 1]))  # A^2 r^2 / N^2 = r^2 (2 - x) / x at gamma = 1
cubic7 = [6, 5, -4, -4]
slot_least = feq(fsub(b2_slot, const(256, 3)), (pscale(pmul(pmul([-1, 2], [-1, 2]), cubic7), 16),
                                                 pscale(pmul([0, 1], pmul([1, 0, -1], [1, 0, -1])), 3)))
cubic_floor = cubic7 == padd([6, -3], pmul(pmul([0, 4], [1, -1]), [2, 1]))  # 6 - 3 x + 4 x (1 - x)(2 + x)
b2_gr = fdiv(([0, 0, 1], [1]), ([-2, 1], [0, 1]))  # R^2 / N^2 with N^2 = (R - 2) / R
gr_least = feq(fsub(b2_gr, const(27)), (pmul(pmul([-3, 1], [-3, 1]), [6, 1]), [-2, 1]))
ratio7 = rdiv(feval(b2_slot, (1, 2)), feval(b2_gr, (3, 1)))
# the stated ends, in ten-thousandths: root(256/3), root 27 and 5^(5/4)
b_slot, b_gr, r_min = (92376, 92377), (51961, 51962), (74767, 74768)
b_slot_ends = within(square, b_slot[0], b_slot[1], 256 * 10**8, 3)
b_gr_ends = within(square, b_gr[0], b_gr[1], 27 * 10**8, 1)
r_min_ends = within(fourth, r_min[0], r_min[1], 3125 * 10**16, 1)
print(f"(c7) arithmetic alone, light's critical impact parameter b = A r / N: the slot form's b^2 = r^2 (2 - x) / x"
      f" with r = 4 / (1 - x^2) (gamma = 1): b^2 - 256/3 = 16 (2 x - 1)^2 (6 + 5 x - 4 x^2 - 4 x^3) /"
      f" (3 x (1 - x^2)^2): {slot_least}, and 6 + 5 x - 4 x^2 - 4 x^3 = 6 - 3 x + 4 x (1 - x)(2 + x): {cubic_floor},"
      f" at least 3 on 0 <= x <= 1, so the least b^2 = {show(feval(b2_slot, (1, 2)))} at x = 1/2, r ="
      f" {show(feval(r_x, (1, 2)))}; general relativity's b^2 = R^3 / (R - 2) in the areal R: b^2 - 27 ="
      f" (R - 3)^2 (R + 6) / (R - 2): {gr_least}, the least {plain(feval(b2_gr, (3, 1)))} at R = 3; their ratio"
      f" {show(ratio7)} = (16/9)^2: {ratio7 == (256, 81)}; between stated endpoints, checked by powers, no root"
      f" found: root(256/3) {between(b_slot[0], b_slot[1], 10**4)} ({b_slot[0]}^2 x 3 <= 256 x 10^8 <"
      f" {b_slot[1]}^2 x 3: {b_slot_ends}), root 27 {between(b_gr[0], b_gr[1], 10**4)} ({b_gr[0]}^2 <= 27 x 10^8 <"
      f" {b_gr[1]}^2: {b_gr_ends}), the areal least 5^(5/4) {between(r_min[0], r_min[1], 10**4)} ({r_min[0]}^4 <="
      f" 3125 x 10^16 < {r_min[1]}^4: {r_min_ends})")

# (c8) the spatial metric's second order, e = G M / (c^2 r)
u_s = s_const(0)
for _ in range(TERMS):  # u - u^2 / 2 = 2 e by u = 2 e + u^2 / 2, one order more each pass
    u_s = s_add([(0, 1), (2, 1)] + [(0, 1)] * (TERMS - 2), s_scale(s_mul(u_s, u_s), (1, 2)))
one_u = s_add(s_const(1), u_s)
a2_slot = s_inv(s_add(s_const(1), s_scale(u_s, (-1, 1))))  # A^2 = 1 / x, x = 1 - u
n2_slot = s_inv(one_u)  # N^2 = 1 / (1 + u)
ind_slot = s_mul(a2_slot, one_u)  # n^2 = A^2 / N^2
solved = s_add(u_s, s_scale(s_mul(u_s, u_s), (-1, 2))) == [(0, 1), (2, 1)] + [(0, 1)] * (TERMS - 2)
four_e = s_mul(s_mul(a2_slot, a2_slot), [(1, 1), (-4, 1)] + [(0, 1)] * (TERMS - 2)) == s_const(1)  # A^4 (1 - 4 e) = 1
one_p = [(1, 1), (1, 2)] + [(0, 1)] * (TERMS - 2)  # 1 + m, m = e / 2
one_m = [(1, 1), (-1, 2)] + [(0, 1)] * (TERMS - 2)
a2_gr = s_mul(s_mul(one_p, one_p), s_mul(one_p, one_p))  # A^2 = (1 + m)^4
n_gr_s = s_mul(one_m, s_inv(one_p))
n2_gr = s_mul(n_gr_s, n_gr_s)
ind_gr = s_mul(a2_gr, s_inv(n2_gr))
defl_slot, defl_gr = rmul(ind_slot[2], (1, 2)), rmul(ind_gr[2], (1, 2))  # (pi / 2) c2, in units of pi


def epstein_shapiro(a2, n2):
    """pi (2 + 2 gamma - beta + 3 eps / 4) over pi, with A^2 = 1 + 2 gamma e + (3/2) eps e^2 and
    N^2 = 1 - 2 e + 2 beta e^2; and eps."""
    gamma_p, beta_p, eps_p = rmul(a2[1], (1, 2)), rmul(n2[2], (1, 2)), rmul(a2[2], (2, 3))
    return radd(rsub(radd((2, 1), rmul((2, 1), gamma_p)), beta_p), rmul((3, 4), eps_p)), eps_p


es_slot, eps_slot = epstein_shapiro(a2_slot, n2_slot)
es_gr, eps_gr = epstein_shapiro(a2_gr, n2_gr)
sun_l, sun_b = (1476625, 1000), (695700 * 1000, 1)  # G M_sun / c^2 and the Sun's radius, in m
sun_text = decimal(sun_l[0], sun_l[1], 1000)
# (pi / 2) c2 (L / b)^2 radians, times 648000 x 10^6 / pi microarcseconds a radian: c2 x 324000 x 10^6 (L / b)^2
limb = rmul((324000 * 10**6, 1), rmul(rdiv(sun_l, sun_b), rdiv(sun_l, sun_b)))
uas_slot, uas_gr = rmul(limb, ind_slot[2]), rmul(limb, ind_gr[2])
print(f"(c8) arithmetic alone, the spatial metric's second order in e = G M / (c^2 r), the slot form at gamma = 1 from"
      f" u = 2 e + u^2 / 2 (u - u^2 / 2 = 2 e to e^4: {solved}; A^4 (1 - 4 e) = 1 to e^4: {four_e}): A^2 ="
      f" {s_text(a2_slot)}, against general relativity's isotropic A^2 = (1 + e / 2)^4 = {s_text(a2_gr)}; N^2 ="
      f" {s_text(n2_slot, 4)} against {s_text(n2_gr, 4)}; n^2 = A^2 / N^2 = {s_text(ind_slot, 3)} against"
      f" {s_text(ind_gr, 3)}; the second-order spatial parameter eps (A^2's e^2 coefficient over 3/2)"
      f" {plain(eps_slot)} against {plain(eps_gr)}; light's second-order deflection, (pi / 2) times n^2's e^2"
      f" coefficient times (G M / (c^2 b))^2: {plain(defl_slot)} pi against {plain(defl_gr)} pi, the ratio"
      f" {show(rdiv(defl_slot, defl_gr))} (Epstein and Shapiro's pi (2 + 2 gamma - beta + 3 eps / 4) agrees:"
      f" {es_slot == defl_slot and es_gr == defl_gr}); at the Sun's limb (G M / c^2 = {sun_text} m, b = 695,700 km, pi"
      f" cancelling against the radian's 648000 x 10^6 / pi microarcseconds): {decimal(uas_slot[0], uas_slot[1], 1000)}"
      f" against {decimal(uas_gr[0], uas_gr[1], 1000)} microarcseconds, each rounded down")

# (d) light at a vanishing grip, on step.tick, laid with no root (the hostile physicist's hp5): every tooth and grip a
# ratio rounded down by a carry
def wall_energy(s, teeth, grips, first, last):
    """The leapfrog's own energy of the light row (row 1) in the sites first to last: W (a - b)^2, and
    grip (a_j - a_i)(b_j - b_i) over the Meshes inside."""
    a, b = s.a[1], s.b[1]
    e = 0
    for i in range(first, last + 1):
        d = int(a[i]) - int(b[i])
        e += int(teeth[1, i]) * d * d
    for k in range(first, last):
        e += int(grips[0, k]) * (int(a[k + 1]) - int(a[k])) * (int(b[k + 1]) - int(b[k]))
    return e


def wall_run(grips, teeth, centre, half, rounds, windows, every):
    """A pulse of 10^15 laid at rest at the site centre (it parts in two) on step.tick, the teeth laid by hand: every
    `every` rounds each window's energy. The start's energy over the last window (the whole line), each other window's
    largest and its round, the first round after the first window's largest where it holds below 2 per cent, and the
    line's energy at the end."""
    n = teeth.shape[1]
    nb = board((n, 1, 1))
    spokes, meshes = geometry(nb, 3)
    lay = Layout(nb, spokes, meshes, grips, Gearing(teeth, two, two.copy(), two.copy()), no_plan, no_read, no_read)
    a = np.zeros((2, n), dtype=object)
    r = np.zeros((2, n), dtype=object)
    for i in range(n):
        d = i - centre
        a[1, i] = quo(10**15 * (half * half - d * d) ** 3, half**6) if d * d < half * half else 0
        r[:, i] = quo(int(teeth[0, i]), 2)
    s = State(a, a.copy(), r, np.zeros((2, n), dtype=object))
    e0 = wall_energy(s, teeth, grips, *windows[-1])
    best, empty = [(0, 0) for _ in windows[:-1]], 0
    for t in range(1, rounds + 1):
        s = step.tick(lay, s)
        if carry(t, every, 0)[1] == 0:
            for w, (first, last) in enumerate(windows[:-1]):
                e = wall_energy(s, teeth, grips, first, last)
                if e > best[w][0]:
                    best[w] = (e, t)
            if best[0][1] and not empty and t > best[0][1] and wall_energy(s, teeth, grips, *windows[0]) * 50 < e0:
                empty = t
    return e0, best, empty, wall_energy(s, teeth, grips, *windows[-1])


def mille(e, e0):
    return decimal(e * 1000, e0, 10)


# (A) a grip linear in the distance: 700 Node-clocks, every tooth at rest, the Meshes 500 to 599 at g (600 - k) / 100,
# the Mesh 600 (the surface) and the wrap's at 0
grips_a = np.full((1, 3 * 700), GRIP, dtype=object)
for k in range(500, 600):
    grips_a[0, k] = quo(GRIP * (600 - k), 100)
grips_a[0, 600], grips_a[0, 699] = 0, 0
teeth_a = np.full((2, 700), REST, dtype=object)
e0_a, best_a, empty_a, end_a = wall_run(grips_a, teeth_a, 300, 30, 2400, ((500, 600), (590, 600), (0, 600)), 10)
# the board time, the sum over the Meshes of root(W / grip), bounded with no root taken: on the slope W / grip = 600 / j
# and j^(-1/2) < 2 (root j - root(j - 1)), as (2 j - 1)^2 - 4 j (j - 1) = 1, so its time is below 2 root(600 x 100);
# the flat run from the site 300 to 500 takes 200 root 6
term_bound = psub(pmul([-1, 2], [-1, 2]), pmul([0, 4], [-1, 1])) == [1]
print(f"(d) light at a vanishing grip, on step.tick, laid with no root (the hostile physicist's hp5); (A) a grip linear"
      f" in the distance: 700 Node-clocks, every tooth at rest, the Meshes 500 to 599 at g (600 - k) / 100, the Mesh"
      f" 600 (the surface) and the wrap's at 0, a pulse of 10^15 laid at rest at site 300; the time per Mesh goes as"
      f" the root of W / grip, so a grip linear in the distance j gives a sum of j^(-1/2), which converges at the"
      f" surface (its continuum, the integral of d^(-1/2), is finite there, where a grip in j^2 would give the harmonic"
      f" sum, which is not): each j^(-1/2) < 2 (root j - root(j - 1)), as (2 j - 1)^2 - 4 j (j - 1) = 1: {term_bound},"
      f" so the slope's time is below 2 root(600 x 100), its square 240,000 < 490^2: {2 * 2 * 600 * 100 < 490 * 490},"
      f" and the flat run's 200 root 6, its square 240,000 < 490^2: {200 * 200 * 6 < 490 * 490}: the board time to the"
      f" surface below 980 rounds; on the act: the slope (sites 500 to 600) holds at most {mille(best_a[0][0], e0_a)}"
      f" per mille of the pulse's energy, at round {best_a[0][1]}; the last 11 sites (590 to 600) at most"
      f" {mille(best_a[1][0], e0_a)} per mille, at round {best_a[1][1]}; the slope holds below 20 per mille again from"
      f" round {empty_a}; the line keeps {mille(end_a, e0_a)} per mille at round 2,400")

# (B) the slot form's exterior itself at gamma = 1, its grip as the coordinate: x = m / 100 at the Mesh m (m = 0 the
# surface, at grip 0), each site between two Meshes at x = (2 m - 1) / 200, r = 4 / (1 - x^2) a ratio everywhere; the
# gaps in r folded into the act's two numbers, grip_m = g x_m / (the gap in r across the Mesh m) and
# W_i = 6 g (2 - x_i)(the gap in r across the site i) lambda: the finite volumes of light's equation
# (1 / N^2) d_t^2 phi = d_r (A^-2 d_r phi), N^2 = 1 / (2 - x), A^-2 = x; a far wall (grip 0) at the Mesh 90
STEPS, FAR = 100, 90


def radius(x):
    """r = 4 / (1 - x^2) at the ratio x, a ratio."""
    return red(4 * x[1] * x[1], x[1] * x[1] - x[0] * x[0])


x_mesh = [red(m, STEPS) for m in range(FAR + 1)]
x_site = [None] + [red(2 * m - 1, 2 * STEPS) for m in range(1, FAR + 1)]  # the site m, between the Meshes m - 1 and m
cell = [None] + [rsub(radius(x_mesh[m]), radius(x_mesh[m - 1])) for m in range(1, FAR + 1)]  # the site's gap in r
gap = [None] + [rsub(radius(x_site[m + 1]), radius(x_site[m])) for m in range(1, FAR)]  # the Mesh's gap in r
grip_x = [(0, 1)] + [rdiv(x_mesh[m], gap[m]) for m in range(1, FAR)] + [(0, 1)]  # grip / g, 0 at both walls
# lambda: the largest over the 90 sites of (grip_left + grip_right) / (6 (2 - x) cell), exact ratios compared, so that
# every site's (grip_left + grip_right) / W is at most 1, as on the loader's flat board (six grips g against 6 g)
lam = (0, 1)
for m in range(1, FAR + 1):
    ratio = rdiv(radd(grip_x[m - 1], grip_x[m]), rmul((6, 1), rmul(rsub((2, 1), x_site[m]), cell[m])))
    if below(lam, ratio):
        lam = ratio
lam_up = rmul(lam, (10**6 + 1, 10**6))  # a millionth above, so the carries' rounding keeps every ratio below 1
grips_b = np.full((1, 3 * (FAR + 2)), GRIP, dtype=object)
teeth_b = np.full((2, FAR + 2), REST, dtype=object)
grips_b[0, 0], grips_b[0, FAR], grips_b[0, FAR + 1] = 0, 0, 0  # the surface, the far wall and the wrap
for m in range(1, FAR):
    grips_b[0, m] = quo(grip_x[m][0] * GRIP, grip_x[m][1])
for m in range(1, FAR + 1):
    w_over_g = rmul((6, 1), rmul(rsub((2, 1), x_site[m]), rmul(cell[m], lam_up)))
    teeth_b[:, m] = quo(w_over_g[0] * GRIP, w_over_g[1])
flat_bound = all(int(grips_b[0, m - 1]) + int(grips_b[0, m]) <= int(teeth_b[0, m]) for m in range(1, FAR + 1))
e0_b, best_b, empty_b, end_b = wall_run(grips_b, teeth_b, 60, 10, 2000, ((1, 30), (1, 3), (1, FAR)), 5)
print(f"(d) (B) the slot form's exterior itself at gamma = 1, laid with no root, its grip as the coordinate:"
      f" x = m / 100 at the Mesh m (m = 0 the surface, at grip 0; a far wall at x = {decimal(FAR, STEPS, 10)}), each"
      f" site between two Meshes at x = (2 m - 1) / 200, so the lattice radius r = 4 / (1 - x^2) is a ratio everywhere;"
      f" the gaps in r folded into the act's two numbers, grip_m = g x_m / (the gap in r across the Mesh m) and"
      f" W_i = 6 g (2 - x_i)(the gap in r across the site i) lambda, the finite volumes of light's equation"
      f" (1 / N^2) d_t^2 phi = d_r (A^-2 d_r phi) with N^2 = 1 / (2 - x) and A^-2 = x, every number a ratio rounded"
      f" down by a carry; lambda = {show(lam)}, the largest over the sites of (grip_left + grip_right) /"
      f" (6 g (2 - x) gap),"
      f" raised by a millionth: every site's (grip_left + grip_right) / W at most 1: {flat_bound}; a pulse of 10^15"
      f" laid at rest at x near {decimal(60, STEPS, 10)} (site 60): the sites 1 to 30 (x below"
      f" {decimal(30, STEPS, 100)}) hold at most {mille(best_b[0][0], e0_b)} per mille of its energy, at round"
      f" {best_b[0][1]}; the sites 1 to 3 (x below {decimal(3, STEPS, 100)}, beside the zero grip) at most"
      f" {mille(best_b[1][0], e0_b)} per mille, at round {best_b[1][1]}; the sites 1 to 30 hold below 20 per mille"
      f" again from round {empty_b}; the line keeps {mille(end_b, e0_b)} per mille at round 2,000: light reaches the"
      f" zero grip in a finite board time and is turned back")


# (e) the inspiral, read in separations, no frequency computed: two equal static slot-form bodies touching, their
# centres d = k G M / c^2 apart, against the separation LIGO and Virgo state for GW150914 at its 75 Hz orbit
def in_digits(x, scale):
    """A ratio pair rounded down to the digits of scale, a power of 10, each digit by a carry (a whole number at scale
    1), and the remainder Rule3's carry leaves on num x scale over den: 0 where the digits are exact."""
    whole, left = carry(x[0] * scale, x[1], 0)
    return (str(whole) if scale == 1 else decimal(x[0], x[1], scale)), left


L_M = red(70 * 1476625, 1000)  # G M / c^2 for 70 solar masses, in m
GW_KM = 350  # GW150914: equal Newtonian point masses orbiting at 75 Hz would be about 350 km apart (PRL 116, 061102)
gw = (GW_KM * 1000, 1)  # in m
rows_e, wide = [], []
# per row the digits shown: d in m, d in km, and d over GW150914's separation
for k, name, at_m, at_km, at_ratio in ((4, "the lattice radius 4, where the grips vanish", 1, 1000, 10**4),
                                       (5, "the throat's lattice radius 5", 100, 10**5, 10**6)):
    d = rmul((k, 1), L_M)  # in m
    (m_text, m_left), (km_text, km_left) = in_digits(d, at_m), in_digits(rdiv(d, (1000, 1)), at_km)
    ratio, left = in_digits(rdiv(d, gw), at_ratio)
    rows_e.append(f"at {name}, d = {k} G M / c^2 = {m_text} m = {km_text} km (the carries' remainders {m_left} and"
                  f" {km_left})")
    wide.append((below(gw, d), f"at {name.split(',')[0]}, by a ratio of {ratio} (the carry's remainder {left})"))
# at the areal radius, d^4 = 5^5 (G M / c^2)^4: d's stated ends in tenths of a km and its ratio's to GW150914's
# separation in thousandths, checked by fourth powers, no root found
d_low, d_high, q_low, q_high = 7728, 7729, 2208, 2209
d_ends = within(fourth, d_low, d_high, 3125 * fourth(L_M[0]), fourth(100 * L_M[1]))
q_ends = within(fourth, q_low, q_high, 3125 * fourth(1000 * L_M[0]), fourth(gw[0] * L_M[1]))
wide.append((fourth(gw[0] * L_M[1]) < 3125 * fourth(L_M[0]), f"at its areal radius, by a ratio"
             f" {between(q_low, q_high, 1000)} ({q_low}^4 x {gw[0] * L_M[1]}^4 <= 3125 x {1000 * L_M[0]}^4 <"
             f" {q_high}^4 x {gw[0] * L_M[1]}^4: {q_ends})"))
print(f"(e) arithmetic alone, the inspiral, read in separations, no frequency computed: two equal static slot-form"
      f" bodies of 70 solar masses in all (G M / c^2 = 70 x {sun_text} m = {decimal(L_M[0], L_M[1], 100)} m), touching"
      f" at d = k G M / c^2 with their surfaces at k G m / c^2 (m = M / 2): " + "; ".join(rows_e) + f"; at its areal"
      f" radius 5^(5/4), d^4 = 5^5 (G M / c^2)^4, d {between(d_low, d_high, 10)} km ({d_low}^4 x {100 * L_M[1]}^4 <="
      f" 3125 x {L_M[0]}^4 < {d_high}^4 x {100 * L_M[1]}^4: {d_ends}), the endpoints stated and checked by fourth"
      f" powers, no root found; against GW150914 as LIGO and Virgo state it (PRL 116, 061102 (2016)): equal Newtonian"
      f" point masses orbiting at 75 Hz, half the waves' frequency, would be only about {GW_KM} km apart,"
      f" {decimal(gw[0] * L_M[1], L_M[0], 1000)} G M / c^2 (rounded down, each digit by a carry); the touching"
      f" separations wider than GW150914's: " + "; ".join(text for wider, text in wide if wider) + "; narrower: "
      + ("; ".join(text for wider, text in wide if not wider) or "none"))
