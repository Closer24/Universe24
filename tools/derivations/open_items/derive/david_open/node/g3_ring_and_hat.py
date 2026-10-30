"""G3 on a ring with Meshes, and 4.2's hat for the held count: what one Node-clock's uniform swing does not show.

Whole numbers alone (the head's gear step, Rule3's carry for every division; no float). Every run of g3_strengths.py
is one Node-clock, the uniform mode alone. Here the tied family's row x and the held count k stand at every Node-clock
of a ring on one axis, each pulled by its two neighbours (the grip W div 6, term 4), with term 6 as in g3_strengths.py
(n = 10^6, g = (W div 400) div n, the held hand's spring kappa and its own least lam):

(m1) the held boson's decay: k laid at n + n / 2 at rest at every Node-clock and x laid 10^6 at one, on a ring of 512;
     per window of 500 rounds the largest |k - n| (the held boson's swing) and the largest |x| (the tied waves), at
     kappa = 25 g n (above 4 g n: twice the band's beat meets the held boson's at a wave number p*, so k -> x x is open),
     at 2 g n (below 4 g n: closed), and on one Node-clock (no Meshes); at round 3,000, x's sign changes around the ring
     against L p* / pi, with p* from 4 sin^2 (w / 2) = (g n + 4 grip sin^2 (p / 2)) / W at twice w equal to the held
     boson's beat (4 sin^2 (w_k / 2) = kappa / W), computed in whole numbers (the sine by its series, pi by Machin's);
(m2) a large uniform swing on a ring of 128 at 25 g n: every x laid at A (one Node-clock 1,000 counts more), every k on
     its valley n - g A^2 / (2 kappa), all at rest; per window of 500 rounds the spread of the Node-clocks' largest |x|
     (the most less the least) in per mille of their mean, at A = 2 x 10^7, where the beat falls as the swing grows, and
     at A = 10^5;
(m3) 4.2's hat for the held count, -(mu / 2) k^2 + (nu / 4) k^4 with mu = W div 32 and nu = mu div n^2 (its wells at
     +-n, its spring there 2 mu, W div 16 to a count), one tied family at the least lam, one Node-clock: the clock's
     state; the mirror well, k laid at -n; the mirror condensate, the least of V at k*^2 = (mu + g^2 / (2 lam)) / nu and
     c* = g |k*| / lam, and the beat about it; two rows laid on the condensate's circle.

Usage: python3 -I g3_ring_and_hat.py <src of tensor24-review at 9751f91c1>
"""

import sys

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import step  # noqa: E402

W = 6 * 15162856759112389 * 1000 * 1000
n = 10**6
g = carry(carry(W, 400, 0)[0], n, 0)[0]
grip = carry(W, 6, 0)[0]


def ceiling(a, b):
    return carry(a + b - 1, b, 0)[0]


def ring_step(xs, ks, spring, lam):
    """One round on the ring: x pushed by its two neighbours, the held count's spring and the four-leg term; k by its two
    neighbours, the tie's -(g / 2) c and its spring. A ring of one Node-clock has no Meshes (its neighbours are itself)."""
    size = len(xs)
    a = [s[0] for s in xs]
    kk = [s[0] for s in ks]
    nx, nk = [], []
    for i in range(size):
        right = carry(i + 1, size, 0)[1]
        c = a[i] * a[i]
        half, _ = carry(g * c, 2, 0)
        nx.append(step.gear(*xs[i], W, grip * (a[i - 1] + a[right] - 2 * a[i]) - g * kk[i] * a[i] - lam * c * a[i]))
        nk.append(step.gear(*ks[i], W, grip * (kk[i - 1] + kk[right] - 2 * kk[i]) - half - spring * (kk[i] - n)))
    return nx, nk


SCALE = 10**40


def arctan_inverse(m):
    total, power, j = 0, carry(SCALE, m, 0)[0], 0
    while power:
        term = carry(power, 2 * j + 1, 0)[0]
        total += -term if j % 2 else term
        power = carry(power, m * m, 0)[0]
        j += 1
    return total


PI = 16 * arctan_inverse(5) - 4 * arctan_inverse(239)


def sine(x):
    total, term, j = 0, x, 0
    while term:
        total += -term if j % 2 else term
        j += 1
        term = carry(carry(term * x, SCALE, 0)[0] * x, SCALE * (2 * j) * (2 * j + 1), 0)[0]
    return total


def largest_angle(bound, scale_of_sine):
    """The largest angle a (times SCALE) in [0, pi / 2] with scale_of_sine * sin^2 (a) <= bound (times SCALE^2)."""
    lo, hi = 0, carry(PI, 2, 0)[0]
    while hi - lo > 1:
        mid = carry(lo + hi, 2, 0)[0]
        s = sine(mid)
        if scale_of_sine * s * s <= bound:
            lo = mid
        else:
            hi = mid
    return lo


def predicted_changes(spring, size):
    """x's sign changes around a ring of size at the decay's wave number p*, in tenths: size p* / pi."""
    half_wk = largest_angle(spring * SCALE * SCALE, 4 * W)  # w_k / 2
    s = sine(carry(half_wk, 2, 0)[0])  # sin (w / 2), w = w_k / 2
    target = 4 * W * s * s - g * n * SCALE * SCALE  # 4 grip sin^2 (p / 2), times SCALE^2
    half_p = largest_angle(target, 4 * grip)
    return carry(10 * size * 2 * half_p, PI, 0)[0]


def decay(spring, size, rounds=4000, window=500):
    lam = ceiling(g * g, 2 * spring)
    xs = [(10**6, 10**6, 0)] + [(0, 0, 0)] * (size - 1)
    ks = [(n + carry(n, 2, 0)[0],) * 2 + (0,)] * size
    rows, most_k, most_x, changes = [], 0, 0, None
    for t in range(1, rounds + 1):
        xs, ks = ring_step(xs, ks, spring, lam)
        most_k = max(most_k, max(abs(s[0] - n) for s in ks))
        most_x = max(most_x, max(abs(s[0]) for s in xs))
        if t == 3000:
            v = [s[0] for s in xs]
            changes = sum(int(v[i] * v[carry(i + 1, size, 0)[1]] < 0) for i in range(size))
        if carry(t, window, 0)[1] == 0:
            rows.append(f"{t}: {most_k}, {most_x}")
            most_k = most_x = 0
    return rows, changes


print("(m1) the held boson laid at n + n / 2 at every Node-clock, x laid 10^6 at one; per window of 500 rounds the largest"
      " |k - n| and the largest |x|:")
for label, times, size in (("kappa 25 g n, a ring of 512", 25, 512), ("kappa 2 g n, a ring of 512", 2, 512),
                           ("kappa 25 g n, one Node-clock", 25, 1)):
    rows, changes = decay(times * g * n, size)
    print(f"    {label}: " + "; ".join(rows))
    if size > 1 and times > 4:
        whole, tenth = carry(predicted_changes(times * g * n, size), 10, 0)
        print(f"      at round 3,000 x changes sign {changes} times around the ring; the decay's wave number p* gives"
              f" {whole}.{tenth}")


def clumps(swing, size=128, rounds=4000, window=500):
    spring = 25 * g * n
    lam = ceiling(g * g, 2 * spring)
    valley = n - carry(g * swing * swing, 2 * spring, 0)[0]
    xs = [(swing + 1000, swing + 1000, 0)] + [(swing, swing, 0)] * (size - 1)
    ks = [(valley, valley, 0)] * size
    most = [0] * size
    rows = []
    for t in range(1, rounds + 1):
        xs, ks = ring_step(xs, ks, spring, lam)
        most = [max(m, abs(s[0])) for m, s in zip(most, xs, strict=True)]
        if carry(t, window, 0)[1] == 0:
            mean = carry(sum(most), size, 0)[0]
            rows.append(f"{t}: {carry(1000 * (max(most) - min(most)), mean, 0)[0]} ({min(most)} to {max(most)})")
            most = [0] * size
    return rows


print("(m2) a ring of 128 at 25 g n, every x laid at A (one 1,000 counts more), every k on its valley; per window of 500"
      " rounds the spread of the Node-clocks' largest |x| in per mille of their mean (the least to the most):")
for swing in (10**5, 2 * 10**7):
    print(f"    A = {swing}: " + "; ".join(clumps(swing)))

mu = carry(W, 32, 0)[0]
nu = carry(mu, n * n, 0)[0]
lam_hat = ceiling(g * g, 2 * 2 * mu)


def hat_run(lays, k_laid, rounds, centre=0):
    """One Node-clock, tied rows laid at lays (one summed four-leg term), the held count under the hat: the largest |x|
    and |k|, and each row's sign changes about centre (the first row) and about 0 (the rest)."""
    xs, k = [(v, v, 0) for v in lays], (k_laid, k_laid, 0)
    most_x = most_k = 0
    changes = [0] * len(lays)
    last = [lays[0] - centre] + list(lays[1:])
    for _ in range(rounds):
        a = [s[0] for s in xs]
        kk = k[0]
        total = sum(v * v for v in a)
        half, _ = carry(g * total, 2, 0)
        xs = [step.gear(*s, W, -g * kk * v - lam_hat * total * v) for s, v in zip(xs, a, strict=True)]
        k = step.gear(*k, W, mu * kk - nu * kk * kk * kk - half)
        most_x = max(most_x, max(abs(s[0]) for s in xs))
        most_k = max(most_k, abs(k[0]))
        for i, s in enumerate(xs):
            now = s[0] - (centre if i == 0 else 0)
            changes[i] += int(now * last[i] < 0)
            last[i] = now if now else last[i]
    return most_x, most_k, changes


def root(m):
    """The largest r with r^2 <= m, by bisection."""
    lo, hi = 0, m + 1
    while hi - lo > 1:
        mid = carry(lo + hi, 2, 0)[0]
        if mid * mid <= m:
            lo = mid
        else:
            hi = mid
    return lo


print(f"(m3) the hat, mu = W div 32 and nu = mu div n^2: its spring at the wells 2 mu = {2 * mu} (W div 16 less"
      f" {carry(W, 16, 0)[0] - 2 * mu}); the least lam {lam_hat}; one Node-clock")
most_x, most_k, changes = hat_run([10**5], n, 4000)
print(f"    the clock's state, x laid 10^5: the largest |x| {most_x}, |k| {most_k}; sign changes {changes[0]} in 4,000 rounds")
most_x, most_k, changes = hat_run([10**3], -n, 20000)
print(f"    the mirror well, k laid at -n and x at 10^3: over 20,000 rounds the largest |x| {most_x}, |k| {most_k}: bounded")
k_star = -root(carry(mu + carry(g * g, 2 * lam_hat, 0)[0], nu, 0)[0])
c_star = carry(g * -k_star, lam_hat, 0)[0]
x_star = root(c_star)
most_x, most_k, changes = hat_run([x_star + 10**5], k_star, 4000, centre=x_star)
print(f"    the mirror condensate k* = {k_star} ({carry(-1000 * k_star, n, 0)[0]} thousandths of n), x* = {x_star}: laid 10^5"
      f" off it, sign changes of x - x* in 4,000 rounds {changes[0]} (the largest |x| {most_x}, |k| {most_k})")
second = 10**5
first = root(c_star - second * second)
most_x, most_k, changes = hat_run([first, second], k_star, 4000, centre=x_star)
print(f"    two rows on the condensate's circle, ({first}, {second}): sign changes of the first about x* and of the second"
      f" about 0 in 4,000 rounds {changes}; the largest |x| {most_x}, |k| {most_k}")
