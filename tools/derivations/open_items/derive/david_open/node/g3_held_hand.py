"""G3's held hand: Big Pic's beating held quantum (thread 6525978806, item 2) read on the act, whole numbers alone.

Whole numbers alone: the head's gear step, Rule3's carry for every division, the sine and cosine by their series and
pi by Machin's formula; no float and no root. The held quantum is a hand of two parts (re, im), each a gear at teeth
W with its own spring kappa, turning round at its Node-clock; its wind D = now^2 - next times before, summed over its
parts. The constants are g3_window_and_well.py's: the head's W, n = 10^6, g = (W div 400) div n, kappa = W div 16,
grip = W div 6; s0 = kappa - g n, so that a gear tied through (g over n) (re^2 + im^2) beats at the hand's own beat
where re^2 + im^2 = n^2.

(a) one Node-clock, the held hand alone, laid on the step's own beat a quarter turn apart: re = A and im = 0 at the
    now slot, re = A cos w and im = -A sin w at the before slot, 4 W sin^2 (w over 2) = kappa, A = n; 100,000 rounds:
    re^2 + im^2 at the now slot, D_re, D_im and their sum against 2 A^2 sin^2 w, the turned momentum
    L = re_now im_before - im_now re_before, the kept teeth; the run back; the control laid in phase;
(b) a tied gear x at the same Node-clock, seeded at 1 and at 10^3, 20,000 rounds, under ties tuned to resonance,
    each with its back-reaction on the held parts: (i) Big Pic's, (g over n) (re^2 + im^2) + s0; (ii) a one-part
    count through 2 re^2, the same mean spring; (iii) the old linear tie g k, k = n + re', re' of n div 100 at twice
    x's beat, and (iii') the same with s0, x at the hand's beat; (iv) the tie through re alone, x at w over 2; and
    the controls, x alone at kappa, at g n and at kappa + W div 16 n + 1: the largest |x|, the round past 10^6,
    the growth rate against Mathieu's eps w over 4;
(c) the bound: 4 n V = 2 n kappa (re^2 + im^2) + 2 n s0 x^2 + 2 g (re^2 + im^2) x^2 + n lam x^4 on every whole
    (re, im, x) up to 2 n in steps of n div 50, at lam = 0, 1 and g^2 div kappa;
(d) a ring of 128, each held part and x pulled by its two neighbours at the grip, x tied as in (i) and seeded at 10^3
    on 16 Node-clocks, 4,000 rounds: (d1) one phase everywhere; (d2) the phase winding once around the ring, its
    winding counted by quadrants, and the whole ring's run back; (d3) the two halves at phases 0 and pi;
(e) n's unit: D at the lay over 2 sin^2 w; A^2 from a key of 2 n^2 sin^2 w, and from the shipped toy's train winding,
    read through the src's own loader;
(f) the held hand's fine teeth as G5's pointer in vacuum, the pointer and the draw ported from g5_draw.py (G5's third
    text): a ring of 128, the merge at one Node-clock and its two neighbours, both parts read as A1 rows; the teeth's
    move over W, the pointer e over 10,800 rounds, part 0 of 1:1, of 1:3 and of 3:7 with z^2, the tenths'
    chi-square, D_N, the joint tenths one round apart, the Fano factor over windows of 10 to 400 rounds; laid at one
    phase and at the phase 2 pi 37 j over 128; the controls laid in phase, and the old standing count at n, laid
    10^3 off it or at n with a tied row laid at 10^3 and at 10; the hand at kappa + 1 and at kappa + W div 16 n + 1,
    its teeth off W's lattice; every fine tooth born at H = W div 2, as G5 lays it; the run back with the draw
    read.

Usage: python3 -I g3_held_hand.py <src of tensor24-review at 9751f91c1>
"""

import json
import os
import sys

sys.path.insert(0, sys.argv[1])
from tensor24 import main as engine_main  # noqa: E402
from tensor24.algebra.carry import carry, flip  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.runner import files as engine_files  # noqa: E402
from tensor24.runner import load as engine_load  # noqa: E402

W = 6 * 15162856759112389 * 1000 * 1000
n = 10**6
g = carry(carry(W, 400, 0)[0], n, 0)[0]
gn = g * n
kappa = carry(W, 16, 0)[0]
grip = carry(W, 6, 0)[0]
s0 = kappa - gn
H = carry(W, 2, 0)[0]
SCALE = 10**40
MILLION = 10**6


def quotient(a, b):
    """a over b, the carry's quotient (the floor), b at least 1."""
    return carry(a, b, 0)[0]


def nearest(a, b):
    """a over b rounded to the nearer whole, a half away from 0 (b at least 1): one carry on the magnitude."""
    if a < 0:
        return -carry(2 * -a + b, 2 * b, 0)[0]
    return carry(2 * a + b, 2 * b, 0)[0]


def ten_to(m):
    """10 multiplied by itself m times."""
    out = 1
    for _ in range(m):
        out *= 10
    return out


def places(a, b, digits):
    """a over b (b at least 1, a of either sign) rounded to `digits` places, as text."""
    unit = ten_to(digits)
    q = nearest(a * unit, b)
    sign = "-" if q < 0 else ""
    whole, part = carry(abs(q), unit, 0)
    if digits == 0:
        return f"{sign}{whole}"
    return f"{sign}{whole}.{str(part).zfill(digits)}"


def sci(a, b, digits=4):
    """a over b (b at least 1) with `digits` significant figures, as text."""
    if a == 0:
        return "0"
    sign = "-" if a < 0 else ""
    top, bottom, power = abs(a), b, 0
    while top >= 10 * bottom:
        bottom *= 10
        power += 1
    while top < bottom:
        top *= 10
        power -= 1
    unit = ten_to(digits - 1)
    lead = nearest(top * unit, bottom)
    if lead == 10 * unit:
        lead, power = unit, power + 1
    whole, part = carry(lead, unit, 0)
    return f"{sign}{whole}.{str(part).zfill(digits - 1)} x 10^{power}"


def arctan_inverse(m):
    """arctan of 1 over m, times SCALE, by its series."""
    total, power, j, sign = 0, quotient(SCALE, m), 0, 1
    while power:
        total += sign * quotient(power, 2 * j + 1)
        power = quotient(power, m * m)
        j, sign = j + 1, -sign
    return total


def artanh_inverse(m):
    """artanh of 1 over m, times SCALE, by its series."""
    total, power, j = 0, quotient(SCALE, m), 0
    while power:
        total += quotient(power, 2 * j + 1)
        power = quotient(power, m * m)
        j += 1
    return total


PI = 16 * arctan_inverse(5) - 4 * arctan_inverse(239)  # Machin's formula, pi times SCALE
LN_TWO = 2 * artanh_inverse(3)  # ln 2 times SCALE


def ln_ratio(a, b):
    """The natural log of a over b (a, b at least 1), times SCALE: whole powers of 2, then 2 artanh of the rest."""
    k = 0
    while a >= 2 * b:
        b *= 2
        k += 1
    while a < b:
        a *= 2
        k -= 1
    t = quotient((a - b) * SCALE, a + b)
    total, power, j = 0, t, 0
    while power:
        total += quotient(power, 2 * j + 1)
        power = quotient(quotient(power * t, SCALE) * t, SCALE)
        j += 1
    return k * LN_TWO + 2 * total


def sine(x):
    """sin of x over SCALE, times SCALE, by its series at |x| with the sign put back: the carry floors a negative
    term at -1, never at 0, so the series runs on the magnitude alone."""
    if x < 0:
        return -sine(-x)
    total, term, j, sign = 0, x, 0, 1
    while term:
        total += sign * term
        j, sign = j + 1, -sign
        term = quotient(quotient(term * x, SCALE) * x, SCALE * (2 * j) * (2 * j + 1))
    return total


def cosine(x):
    """cos of x over SCALE, times SCALE, by its series at |x| (cos is even)."""
    if x < 0:
        return cosine(-x)
    total, term, j, sign = 0, SCALE, 0, 1
    while term:
        total += sign * term
        j, sign = j + 1, -sign
        term = quotient(quotient(term * x, SCALE) * x, SCALE * (2 * j - 1) * (2 * j))
    return total


def turned(theta):
    """An angle times SCALE brought into [0, 2 pi)."""
    while theta >= 2 * PI:
        theta -= 2 * PI
    while theta < 0:
        theta += 2 * PI
    return theta


def largest_angle(bound, scale_of_sine):
    """The largest angle a (times SCALE) in [0, pi over 2] with scale_of_sine sin^2 (a) <= bound (times SCALE^2)."""
    lo, hi = 0, quotient(PI, 2)
    while hi - lo > 1:
        mid = quotient(lo + hi, 2)
        s = sine(mid)
        if scale_of_sine * s * s <= bound:
            lo = mid
        else:
            hi = mid
    return lo


def beat(spring):
    """The step's beat w, times SCALE, for 4 W sin^2 (w over 2) = spring."""
    return 2 * largest_angle(spring * SCALE * SCALE, 4 * W)


def mode_beat(spring, m, size):
    """The step's beat, times SCALE, of a ring mode of wave number m: 4 W sin^2 (w over 2) = spring + 4 grip
    sin^2 (pi m over size)."""
    s = sine(quotient(PI * m, size))
    return 2 * largest_angle(spring * SCALE * SCALE + 4 * grip * s * s, 4 * W)


def laid(amplitude, phase, w):
    """A part laid at amplitude cos(phase) at the now slot and amplitude cos(phase - w) at the before slot, whole."""
    now = nearest(amplitude * cosine(turned(phase)), SCALE)
    before = nearest(amplitude * cosine(turned(phase - w)), SCALE)
    return (now, before, 0)


def mirrored(gear):
    """The mirror of a gear: its slots swapped and its fine tooth flipped, (b, a, flip(r, W))."""
    a, b, r = gear
    return (b, a, flip(r, W))


def ring_changes(values):
    """Sign changes around a ring."""
    size = len(values)
    return sum(int(values[i] * values[carry(i + 1, size, 0)[1]] < 0) for i in range(size))


w_s = beat(kappa)  # the hand's beat on the step, times SCALE
sin_w, cos_w = sine(w_s), cosine(w_s)
A = n
quarter = ((A, nearest(A * cos_w, SCALE), 0), (0, -nearest(A * sin_w, SCALE), 0))  # re and im, a quarter turn apart


# (a) one Node-clock, the held hand alone


def held_alone(re_g, im_g, rounds, marks=(1000, 10000)):
    """The held hand's two parts, each pushed by -kappa part: the least and most of re^2 + im^2 at the now slot, of
    D_re, D_im and their sum (D = now^2 - next before), and of L; the summed D's total; the kept teeth within [0, W);
    the end state; re^2 + im^2's spread at the marked rounds."""
    low = [None] * 5
    high = [None] * 5
    d_total = 0
    teeth = True
    spreads = []
    for t in range(1, rounds + 1):
        re_now, re_was, im_now, im_was = re_g[0], re_g[1], im_g[0], im_g[1]
        re_g = step.gear(*re_g, W, -kappa * re_now)
        im_g = step.gear(*im_g, W, -kappa * im_now)
        d_re = re_now * re_now - re_g[0] * re_was
        d_im = im_now * im_now - im_g[0] * im_was
        values = (re_now * re_now + im_now * im_now, d_re, d_im, d_re + d_im, re_now * im_was - im_now * re_was)
        for i, v in enumerate(values):
            low[i] = v if low[i] is None else min(low[i], v)
            high[i] = v if high[i] is None else max(high[i], v)
        d_total += d_re + d_im
        teeth = teeth and 0 <= re_g[2] < W and 0 <= im_g[2] < W
        if t in marks:
            spreads.append(high[0] - low[0])
    return low, high, d_total, teeth, (re_g, im_g), spreads


ROUNDS_A = 100000
low, high, d_total, teeth, end, spreads = held_alone(*quarter, ROUNDS_A)
closed_d = 2 * A * A * sin_w * sin_w  # 2 A^2 sin^2 w, times SCALE^2
print(f"(a) one Node-clock, the held hand alone, each part a gear at teeth W pushed by -kappa part; W divisible by 16:"
      f" {carry(W, 16, 0)[1] == 0}, so cos w = {places(32 * cos_w, SCALE, 6)} over 32 and sin^2 w ="
      f" {places(1024 * sin_w * sin_w, SCALE * SCALE, 6)} over 1024 (by the series); laid re = {quarter[0][0]},"
      f" {quarter[0][1]} and im = {quarter[1][0]}, {quarter[1][1]} (now, before), A = n; {ROUNDS_A} rounds:")
print(f"    re^2 + im^2 at the now slot from {low[0]} to {high[0]}, a spread of"
      f" {places(MILLION * (high[0] - low[0]), A * A, 2)} per million of A^2 (over the first 1,000 rounds"
      f" {places(MILLION * spreads[0], A * A, 2)}, the first 10,000 {places(MILLION * spreads[1], A * A, 2)})")
print(f"    D_re from {low[1]} to {high[1]}, D_im from {low[2]} to {high[2]}; their sum from {low[3]} to {high[3]},"
      f" mean {places(d_total, ROUNDS_A, 2)}, a spread of {places(MILLION * ROUNDS_A * (high[3] - low[3]), d_total, 2)}"
      f" per million of its mean; 2 A^2 sin^2 w = {places(closed_d, SCALE * SCALE, 2)} (closed form 126 A^2 over 1024"
      f" = {quotient(126 * A * A, 1024)})")
print(f"    L = re_now im_before - im_now re_before from {low[4]} to {high[4]}, against -A^2 sin w ="
      f" {places(-A * A * sin_w, SCALE, 2)}; every kept tooth within [0, W): {teeth}")
back = held_alone(mirrored(end[0]), mirrored(end[1]), ROUNDS_A)[4]
print(f"    the run back: {ROUNDS_A} rounds forward, the mirror (b, a, flip(r, W)), {ROUNDS_A} rounds, the mirror: the"
      f" start returns bit for bit: {(mirrored(back[0]), mirrored(back[1])) == quarter}")
in_phase = held_alone(quarter[0], quarter[0], ROUNDS_A)
print(f"    the control laid in phase (im = re): re^2 + im^2 from {in_phase[0][0]} to {in_phase[1][0]}, a spread of"
      f" {places(MILLION * (in_phase[1][0] - in_phase[0][0]), A * A, 2)} per million of A^2; L from {in_phase[0][4]} to"
      f" {in_phase[1][4]}")


# (b) the ties, tuned to resonance

w0_s = beat(gn)  # the beat of the spring g n alone
spring_iii = nearest(4 * W * sine(w0_s) * sine(w0_s), SCALE * SCALE)  # its beat 2 w0
spring_iii_w = nearest(4 * W * sin_w * sin_w, SCALE * SCALE)  # its beat 2 w
sin_quarter = sine(quotient(w_s, 4))
spring_iv = nearest(4 * W * sin_quarter * sin_quarter, SCALE * SCALE)  # x's spring, its beat w over 2
small = quotient(n, 100)
OFFSET = quotient(W, 16 * n) + 1  # added to kappa it leaves W's lattice by about W div 16 a swing of n
TIES = {
    "i": "(i) Big Pic's tie, (g over n) (re^2 + im^2) + s0, the hand as in (a), x at the hand's beat w",
    "ii": "(ii) a one-part count through 2 re^2, the same mean spring, x at w, the pump at 2 w",
    "iii": "(iii) the old linear tie g k, k = n + re', re' of n div 100 at twice x's beat, x at w0, the beat of g n",
    "iii_w": "(iii') the same with s0, x at the hand's beat w, re' at 2 w",
    "iv": "(iv) the tie through re alone, (g over 2) re x^2, x's spring at w over 2, re at w",
    "alone_w": "(o) the control: x alone at the spring kappa, no held hand and no tie, the step's own rounding",
    "alone_w0": "(o') the control: x alone at the spring g n",
    "alone_off": "(o'') the control: x alone at kappa + W div 16 n + 1, a spring off W's lattice",
}


def tie_run(kind, seed, rounds=20000, window=500):
    """x laid at rest at the seed; the held parts laid per tie; the back-reaction on the held parts from the same V.
    Returns x's largest |x|, the first round past 10^6, the largest |x| per window, and the held swing's least and
    most re^2 + im^2 (tie (i))."""
    x = (seed, seed, 0)
    if kind == "i":
        held = list(quarter)
    elif kind in ("ii", "iv"):
        held = [quarter[0]]
    elif kind == "iii":
        held = [(small, nearest(small * cosine(2 * w0_s), SCALE), 0)]
    elif kind == "iii_w":
        held = [(small, nearest(small * cosine(2 * w_s), SCALE), 0)]
    else:
        held = []
    most, first, envelope, top, rho_low, rho_high = 0, None, [], 0, None, None
    for t in range(1, rounds + 1):
        xx, c = x[0], x[0] * x[0]
        parts = [h[0] for h in held]
        if kind == "i":
            rho = parts[0] * parts[0] + parts[1] * parts[1]
            rho_low = rho if rho_low is None else min(rho_low, rho)
            rho_high = rho if rho_high is None else max(rho_high, rho)
            px = -quotient(g * rho * xx, n) - s0 * xx
            pushes = [-kappa * p - quotient(g * p * c, n) for p in parts]
        elif kind == "ii":
            px = -quotient(2 * g * parts[0] * parts[0] * xx, n) - s0 * xx
            pushes = [-kappa * parts[0] - quotient(2 * g * parts[0] * c, n)]
        elif kind == "iii":
            px = -g * (n + parts[0]) * xx
            pushes = [-spring_iii * parts[0] - quotient(g * c, 2)]
        elif kind == "iii_w":
            px = -(g * (n + parts[0]) + s0) * xx
            pushes = [-spring_iii_w * parts[0] - quotient(g * c, 2)]
        elif kind == "iv":
            px = -(spring_iv + g * parts[0]) * xx
            pushes = [-kappa * parts[0] - quotient(g * c, 2)]
        else:
            px = -{"alone_w": kappa, "alone_w0": gn, "alone_off": kappa + OFFSET}[kind] * xx
            pushes = []
        x = step.gear(*x, W, px)
        held = [step.gear(*h, W, p) for h, p in zip(held, pushes, strict=True)]
        top = max(top, abs(x[0]))
        if first is None and abs(x[0]) > MILLION:
            first = t
        if carry(t, window, 0)[1] == 0:
            envelope.append(top)
            most, top = max(most, top), 0
    return most, first, envelope, rho_low, rho_high


def mathieu(kind, rho_spread):
    """eps, the tie's relative swing of x's spring, as a fraction, and x's beat times SCALE."""
    if kind == "i":
        return (g * rho_spread, 2 * n * kappa), w_s
    if kind == "ii":
        return (gn, kappa), w_s
    if kind == "iii":
        return (g * small, gn), w0_s
    if kind == "iii_w":
        return (g * small, kappa), w_s
    if kind == "iv":
        return (gn, spring_iv), quotient(w_s, 2)
    return (0, 1), (w0_s if kind == "alone_w0" else w_s)


print(f"(b) a tied gear x at teeth W, laid at rest, 20,000 rounds; s0 = kappa - g n = {s0}; x's beat w ="
      f" {places(w_s, SCALE, 5)}, w0 = {places(w0_s, SCALE, 5)} a round; the largest |x| per window of 500 rounds"
      f" gives the growth rate, ln of the window reaching 10^5 (else the last) over the first, per round:")
for kind, label in TIES.items():
    print(f"    {label}:")
    for seed in (1, 1000):
        most, first, envelope, rho_low, rho_high = tie_run(kind, seed)
        last = next((i for i, v in enumerate(envelope) if v >= 10**5), len(envelope) - 1)
        rate = nearest(MILLION * ln_ratio(max(envelope[last], 1), max(envelope[0], 1)), 500 * last * SCALE)
        (e_num, e_den), beat_x = mathieu(kind, (rho_high - rho_low) if kind == "i" else 0)
        predicted = nearest(MILLION * e_num * beat_x, 4 * e_den * SCALE)
        print(f"      seed {seed}: the largest |x| {most}; past 10^6 at round {first}; the first and last windows"
              f" {envelope[0]} and {envelope[last]} (window {last + 1}); the growth rate {places(rate, MILLION, 6)} a"
              f" round against Mathieu's eps w over 4 = {places(predicted, MILLION, 6)}, eps = {sci(e_num, e_den)}")


# (c) the bound

steps = [quotient(n, 50) * j for j in range(-100, 101)]
rhos = sorted({re * re + im * im for re in steps for im in steps})
print(f"(c) 4 n V = 2 n kappa (re^2 + im^2) + 2 n s0 x^2 + 2 g (re^2 + im^2) x^2 + n lam x^4 on every whole (re, im, x)"
      f" with each from -2 n to 2 n in steps of n div 50 ({len(steps)}^3 points; {len(rhos)} values of re^2 + im^2):")
for lam in (0, 1, quotient(g * g, kappa)):
    pairs = [(2 * n * kappa + 2 * g * x * x, 2 * n * s0 * x * x + n * lam * x**4) for x in steps]
    least_v = min(r * a + b for r in rhos for a, b in pairs)
    print(f"    lam = {lam}: the least 4 n V {least_v}, at or above 0: {least_v >= 0}")
print(f"    every term is at or above 0 wherever kappa, s0, g and lam are: no bound on lam for any g and lam at or"
      f" above 0 (s0 = {s0} > 0), against the sixth text's least lam 4548858; the least of V is 0, at the hand at"
      f" rest at 0")


# (d) a ring of 128

SIZE, SEEDED = 128, 16


def hand_ring_round(res, ims, xs):
    """One ring round: each held part pulled by its two neighbours at the grip, its spring and the tie's back-reaction;
    x by its two neighbours, the tie (g over n) (re^2 + im^2) and s0."""
    size = len(res)
    ra, ia, xa = [s[0] for s in res], [s[0] for s in ims], [s[0] for s in xs]
    nr, ni, nx = [], [], []
    for i in range(size):
        right = carry(i + 1, size, 0)[1]
        c = xa[i] * xa[i]
        rho = ra[i] * ra[i] + ia[i] * ia[i]
        nr.append(step.gear(*res[i], W, grip * (ra[i - 1] + ra[right] - 2 * ra[i]) - kappa * ra[i]
                            - quotient(g * ra[i] * c, n)))
        ni.append(step.gear(*ims[i], W, grip * (ia[i - 1] + ia[right] - 2 * ia[i]) - kappa * ia[i]
                            - quotient(g * ia[i] * c, n)))
        nx.append(step.gear(*xs[i], W, grip * (xa[i - 1] + xa[right] - 2 * xa[i]) - quotient(g * rho * xa[i], n)
                            - s0 * xa[i]))
    return nr, ni, nx


def seeded_x():
    return [(1000, 1000, 0)] * SEEDED + [(0, 0, 0)] * (SIZE - SEEDED)


def quadrant(re, im):
    """0 to 3 counterclockwise from the positive re axis; None at the origin."""
    if re > 0 and im >= 0:
        return 0
    if re <= 0 and im > 0:
        return 1
    if re < 0 and im <= 0:
        return 2
    if re >= 0 and im < 0:
        return 3
    return None


def winding(res, ims):
    """The winding number around the ring counted by quadrants, or None where a step is ambiguous or a hand at 0."""
    qs = [quadrant(r[0], i[0]) for r, i in zip(res, ims, strict=True)]
    if None in qs:
        return None
    total = 0
    for j in range(len(qs)):
        d = carry(qs[carry(j + 1, len(qs), 0)[1]] - qs[j], 4, 0)[1]
        if d == 2:
            return None
        total += 1 if d == 1 else (-1 if d == 3 else 0)
    whole, rest = carry(total, 4, 0)
    return whole if rest == 0 else None


res, ims, xs = [quarter[0]] * SIZE, [quarter[1]] * SIZE, seeded_x()
rho_low = rho_high = None
most_changes = 0
for t in range(1, 4001):
    res, ims, xs = hand_ring_round(res, ims, xs)
    rho_now = [r[0] * r[0] + i[0] * i[0] for r, i in zip(res, ims, strict=True)]
    rho_low = min(rho_now) if rho_low is None else min(rho_low, min(rho_now))
    rho_high = max(rho_now) if rho_high is None else max(rho_high, max(rho_now))
    most_changes = max(most_changes, ring_changes([r[0] for r in res]))
print(f"(d) a ring of 128, each held part and x pulled by its two neighbours at the grip, x tied as in (i), x laid at"
      f" 10^3 at rest on 16 Node-clocks; 4,000 rounds:")
print(f"    (d1) one phase everywhere, laid as in (a): re^2 + im^2 over the ring and the rounds from {rho_low} to"
      f" {rho_high} ({places(MILLION * (rho_high - rho_low), A * A, 2)} per million of A^2); re's sign changes around"
      f" the ring at most {most_changes} in any round, {ring_changes([r[0] for r in res])} at round 4,000; the largest"
      f" |x| at round 4,000 {max(abs(s[0]) for s in xs)} (the old hat flipped 114 to 126 of 128)")

w1_s = mode_beat(kappa, 1, SIZE)
start2 = ([laid(A, quotient(2 * PI * j, SIZE), w1_s) for j in range(SIZE)],
          [laid(A, quotient(2 * PI * j, SIZE) - quotient(PI, 2), w1_s) for j in range(SIZE)], seeded_x())
res, ims, xs = start2
windings, rho_low = set(), None
for t in range(1, 4001):
    res, ims, xs = hand_ring_round(res, ims, xs)
    windings.add(winding(res, ims))
    rho_now = min(r[0] * r[0] + i[0] * i[0] for r, i in zip(res, ims, strict=True))
    rho_low = rho_now if rho_low is None else min(rho_low, rho_now)
end2 = (res, ims, xs)
res, ims, xs = ([mirrored(s) for s in part] for part in end2)
for t in range(1, 4001):
    res, ims, xs = hand_ring_round(res, ims, xs)
back2 = tuple([mirrored(s) for s in part] for part in (res, ims, xs))
print(f"    (d2) the phase 2 pi j over 128 at Node-clock j (re = A cos, im = A sin, the before slot on the mode's own"
      f" beat {places(w1_s, SCALE, 6)} against {places(w_s, SCALE, 6)}): the winding over every round"
      f" {sorted(windings, key=str)} (at the lay {winding(start2[0], start2[1])}); the least re^2 + im^2 anywhere"
      f" {rho_low}"
      f" ({places(MILLION * rho_low, A * A, 0)} per million of A^2); the whole ring's run back, 4,000 rounds, the"
      f" mirror, 4,000 rounds, the mirror: bit for bit {back2 == start2}")

half_ring = quotient(SIZE, 2)
res = [quarter[0]] * half_ring + [tuple(-v for v in quarter[0][:2]) + (0,)] * half_ring
ims = [quarter[1]] * half_ring + [tuple(-v for v in quarter[1][:2]) + (0,)] * half_ring
xs = seeded_x()
seams = (half_ring - 1, half_ring, SIZE - 1, 0)


def seam_energy(res, ims):
    """Twice the grip's energy on the two seam bonds: grip times the squared differences across them."""
    total = 0
    for i, j in ((half_ring - 1, half_ring), (SIZE - 1, 0)):
        total += (res[j][0] - res[i][0]) ** 2 + (ims[j][0] - ims[i][0]) ** 2
    return grip * total


def bond_energy(res, ims):
    """Twice the grip's energy on every bond of the ring."""
    size = len(res)
    return grip * sum((res[carry(i + 1, size, 0)[1]][0] - res[i][0]) ** 2
                      + (ims[carry(i + 1, size, 0)[1]][0] - ims[i][0]) ** 2 for i in range(size))


seam0 = seam_energy(res, ims)
seam_rho, trail = None, []
for t in range(1, 4001):
    res, ims, xs = hand_ring_round(res, ims, xs)
    here = min(res[i][0] * res[i][0] + ims[i][0] * ims[i][0] for i in seams)
    seam_rho = here if seam_rho is None else min(seam_rho, here)
    if carry(t, 500, 0)[1] == 0:
        trail.append(places(1000 * seam_energy(res, ims), seam0, 0))
left, right = quotient(SIZE, 4), quotient(3 * SIZE, 4)
facing = res[left][0] * res[right][0] + ims[left][0] * ims[right][0]
print(f"    (d3) the left half at phase 0 and the right half at phase pi: the least re^2 + im^2 at the seams' four"
      f" Node-clocks over the rounds {seam_rho} ({places(MILLION * seam_rho, A * A, 0)} per million of A^2); the seams'"
      f" bond energy per mille of its lay at rounds 500 to 4,000: {', '.join(trail)}; every bond's energy at round"
      f" 4,000 per mille of the seams' at the lay {places(1000 * bond_energy(res, ims), seam0, 0)}; at round 4,000 the"
      f" halves' middles (Node-clocks {left} and {right}) hold re^2 + im^2 of"
      f" {places(1000 * (res[left][0] ** 2 + ims[left][0] ** 2), A * A, 0)} and"
      f" {places(1000 * (res[right][0] ** 2 + ims[right][0] ** 2), A * A, 0)} per mille of A^2, their hands opposed"
      f" (re re' + im im' below 0): {facing < 0}")


# (e) n's unit

toy = os.path.join(sys.argv[1], os.pardir, "examples", "tensor24")
universe, setting, piece = (json.loads(open(os.path.join(toy, name), encoding="utf-8").read())
                            for name in ("universe.json", "setting.json", "piece.json"))
kinds, tables, square = engine_main.made(engine_load.star(len(piece["shape"])))
loaded, _ = engine_load.load(universe, setting, engine_files.sites_of(piece["shape"]), kinds, tables, square)
layout = engine_main.layout(universe, piece["shape"], loaded)
windings_toy = [layout.gearing.drive[first, 0] for first in loaded.trains.first.tolist()]
re_g, im_g = quarter
d_first = (re_g[0] * re_g[0] - step.gear(*re_g, W, -kappa * re_g[0])[0] * re_g[1]
           + im_g[0] * im_g[0] - step.gear(*im_g, W, -kappa * im_g[0])[0] * im_g[1])
two_sin2 = 2 * sin_w * sin_w  # 2 sin^2 w times SCALE^2
key_n = nearest(n * n * two_sin2, SCALE * SCALE)
print(f"(e) n's unit: D at the lay, summed over the parts, {d_first}; D over 2 sin^2 w ="
      f" {places(d_first * SCALE * SCALE, two_sin2, 2)}, against A^2 = {A * A}")
print(f"    one winding = D sets A^2 = key over (2 sin^2 w), the key the law's quantum of D: a key of 2 n^2 sin^2 w ="
      f" {key_n} gives A^2 = key times 512 over 63 (2 sin^2 w = 63 over 512 exactly, kappa being W over 16) ="
      f" {quotient(key_n * 512, 63)}, n^2 exactly: {key_n * 512 == 63 * n * n}")
print(f"    the src carries no quantum of D; it lays each train card's winding as the drive's teeth T_d, 1 on the"
      f" force's path: the shipped toy's trains {[t['name'] for t in universe['trains']]} read {windings_toy}; read as"
      f" the key, T = {windings_toy[0]} gives A^2 = {places(windings_toy[0] * SCALE * SCALE, two_sin2, 3)} counts^2")


# (f) the held hand's fine teeth as G5's pointer in vacuum: the pointer, the draw and the statistics are g5_draw.py's
# (G5's third text, read and not written), ported line for line onto the ring


def ppm(part, whole):
    return carry(MILLION * part, whole, 0)[0]


def shown(thousandths):
    whole, rest = carry(thousandths, 1000, 0)
    return f"{whole}.{str(rest).zfill(3)}"


def hundredths(value):
    whole, rest = carry(value, 100, 0)
    return f"{whole}.{str(rest).zfill(2)}"


def nonneg(value):
    """The law's one whether: 1 where the value is at least 0 and 0 below, by one carry, v div (v v + 1) 0 or -1."""
    return carry(value, value * value + 1, 0)[0] + 1


def placing(sizes):
    """The law's rank count, with no sort and no if: one sign bit per pair of parts; each part's place is the count of
    parts placed before it. Returns the sizes placed before each part, whether each closes the last interval (the
    last placed part of nonzero size), and the total."""
    count = len(sizes)
    place = [0] * count
    for j in range(count):
        for k in range(j + 1, count):
            first = nonneg(sizes[j] - sizes[k])
            place[k] += first
            place[j] += 1 - first
    total = sum(sizes)
    before = tuple(sum(sizes[j] * nonneg(place[k] - place[j] - 1) for j in range(count)) for k in range(count))
    closing = tuple(nonneg(before[k] + sizes[k] - total) * nonneg(sizes[k] - 1) for k in range(count))
    return before, closing, total


PLACED = {sizes: placing(sizes) for sizes in ((1, 1), (1, 3), (3, 7))}


def law_drawn(e, h, sizes):
    """The part whose interval, from B times H up to (B + S) times H, holds e times L; closed at the last placed part
    of nonzero size, which so takes e = H."""
    before, closing, total = PLACED[sizes]
    part = 0
    for k, size in enumerate(sizes):
        part += k * nonneg(e * total - before[k] * h) * nonneg((before[k] + size) * h - 1 + closing[k] - e * total)
    return part


def tenth(e, h):
    return min(carry(10 * e, h, 0)[0], 9)


def chi_tenths(values):
    """Chi-square of the tenths of e within H on 9, in thousandths."""
    counts = [0] * 10
    for e in values:
        counts[tenth(e, H)] += 1
    total = sum(counts)
    return carry(1000 * sum((10 * c - total) ** 2 for c in counts), 10 * total, 0)[0]


def chi_joint(pairs):
    """Chi-square of a 10 by 10 table of tenths against the product of its margins, in thousandths, with its degrees of
    freedom, (filled rows - 1) (filled columns - 1)."""
    table = [[0] * 10 for _ in range(10)]
    for i, j in pairs:
        table[i][j] += 1
    count = len(pairs)
    rows = [sum(line) for line in table]
    cols = [sum(table[i][j] for i in range(10)) for j in range(10)]
    total = 0
    for i in range(10):
        for j in range(10):
            den = count * rows[i] * cols[j]
            if den:
                total += carry(10**9 * (count * table[i][j] - rows[i] * cols[j]) ** 2, den, 0)[0]
    filled = (sum(int(r > 0) for r in rows) - 1) * (sum(int(c > 0) for c in cols) - 1)
    return carry(total, MILLION, 0)[0], filled


def z2_fixed(zero, total, s1, s2):
    """z^2 of part 0's count at fixed sizes, (L zero - total s1)^2 over total s1 s2, in thousandths."""
    return carry(1000 * ((s1 + s2) * zero - total * s1) ** 2, total * s1 * s2, 0)[0]


def odds(num, den):
    """A z^2 of one degree, num over den, in its odds class: below 384 hundredths, up to 663, or above."""
    labels = (f"below {hundredths(384)}", f"{hundredths(384)} to {hundredths(663)}", f"above {hundredths(663)}")
    return labels[nonneg(100 * num - 384 * den) + nonneg(100 * num - 663 * den - 1)]


def discrepancy(values):
    """The star discrepancy's numerator over N H: the largest of j H - e_(j) N and e_(j) N - (j - 1) H."""
    count, top = len(values), 0
    for j, e in enumerate(sorted(values), start=1):
        top = max(top, j * H - e * count, e * count - (j - 1) * H)
    return top


def fano(marks, sp, lsum, m):
    """A part's count in windows of m rounds, pooled over the Node-clocks: F in thousandths, the windows, and F's z^2
    against its own binomial spread as a fraction."""
    windows = acc = 0
    for k in range(len(marks[0])):
        for t0 in range(0, len(marks) - m + 1, m):
            count = sum(marks[t][k] for t in range(t0, t0 + m))
            acc += (lsum * count - m * sp) ** 2
            windows += 1
    q = m * sp * (lsum - sp)
    num, den = (acc - windows * q) ** 2, windows * q * (2 * q + lsum * lsum - 6 * sp * (lsum - sp))
    return carry(1000 * acc, windows * q, 0)[0], windows, num, den


WINDOWS = (10, 40, 100, 200, 400)
MERGE = (SIZE - 1, 0, 1)  # the merge on the ring: Node-clock 0 and its two neighbours
ROUNDS_F, MOVES_F = 10800, 10000


def pointer(rows_in, rows_out):
    """G5's pointer at the merge: P, the sum of c(r_in) + c(r_out), c(r) = 2 r + 1 - W, over the merge's Node-clocks
    and every read row; u = P mod W; e = min(u, W - u), between 0 and H."""
    total = 0
    for row_in, row_out in zip(rows_in, rows_out, strict=True):
        for y in MERGE:
            total += (2 * row_in[y][2] + 1 - W) + (2 * row_out[y][2] + 1 - W)
    u = carry(total, W, 0)[1]
    return min(u, W - u)


def pointer_round(rows, kind, spring):
    """A ring round in vacuum. kind "hand": rows re and im, each pulled by its two neighbours and pushed by -spring
    part; "count": the old standing count, -spring (k - n); "tied": the old count with a tied row x, the old linear
    tie, k pushed by -(g over 2) x^2 - spring (k - n) and x by -g k x."""
    size = len(rows[0])
    nows = [[s[0] for s in row] for row in rows]
    out = [[] for _ in rows]
    for i in range(size):
        right = carry(i + 1, size, 0)[1]
        laps = [now[i - 1] + now[right] - 2 * now[i] for now in nows]
        if kind == "hand":
            pushes = [grip * laps[p] - spring * nows[p][i] for p in range(2)]
        elif kind == "count":
            pushes = [grip * laps[0] - spring * (nows[0][i] - n)]
        else:
            k_i, x_i = nows[0][i], nows[1][i]
            pushes = [grip * laps[0] - quotient(g * x_i * x_i, 2) - spring * (k_i - n), grip * laps[1] - g * k_i * x_i]
        for p, push in enumerate(pushes):
            out[p].append(step.gear(*rows[p][i], W, push))
    return out


def pointer_run(rows, kind, spring, read, rounds):
    """The pointer each round at the merge from the read rows, and each read row's fine-tooth move at Node-clock 0."""
    es, moves = [], [[] for _ in read]
    for _ in range(rounds):
        out = pointer_round(rows, kind, spring)
        es.append(pointer([rows[p] for p in read], [out[p] for p in read]))
        for j, p in enumerate(read):
            moves[j].append(abs(out[p][0][2] - rows[p][0][2]))
        rows = out
    return es, moves, rows


def gcd(a, b):
    a, b = abs(a), abs(b)
    while b:
        a, b = b, carry(a, b, 0)[1]
    return a


def born_at_h(rows, born=H):
    """Every fine tooth born at H, as G5 lays its gears (or at the birth given)."""
    return [[(a, b, born) for a, b, _ in row] for row in rows]


def pointer_report(label, rows, kind, spring, read, born=H):
    es, moves, _ = pointer_run(born_at_h(rows, born), kind, spring, read, ROUNDS_F)
    count = len(es)
    teeth = []
    for j in range(len(read)):
        ordered = sorted(moves[j][:MOVES_F])
        teeth.append(f"median {quotient(1000 * ordered[quotient(MOVES_F, 2)], W)}, least"
                     f" {quotient(1000 * ordered[0], W)}")
    chi, free = chi_joint([(tenth(es[t], H), tenth(es[t + 1], H)) for t in range(count - 1)])
    print(f"    {label}: the fine tooth's move over W at Node-clock 0, rounds 1 to 10,000, in thousandths:"
          f" {'; '.join(teeth)}; {len(set(es))} distinct e of {count}; chi-square of the tenths on 9"
          f" {shown(chi_tenths(es))}; D_N {ppm(discrepancy(es), count * H)} ppm; the joint tenths one round apart"
          f" {shown(chi)} on {free}")
    draws = []
    for s1, s2 in ((1, 1), (1, 3), (3, 7)):
        zero = sum(int(law_drawn(e, H, (s1, s2)) == 0) for e in es)
        lsum = s1 + s2
        odds_class = odds((lsum * zero - count * s1) ** 2, count * s1 * s2)
        draws.append(f"at {s1}:{s2} part 0 in {zero} (expected {quotient(count * s1, lsum)}), z^2"
                     f" {shown(z2_fixed(zero, count, s1, s2))}, {odds_class}")
    print("      " + "; ".join(draws) + f" (of {count})")
    lines = []
    for sizes, lsum in (((1, 1), 2), ((1, 3), 4)):
        marks = [[int(law_drawn(e, H, sizes) == 0)] for e in es]
        cells = []
        for m in WINDOWS:
            f_value, windows, num, den = fano(marks, 1, lsum, m)
            cells.append(f"M {m}: {shown(f_value)} ({windows}, z^2 {shown(carry(1000 * num, den, 0)[0])})")
        lines.append(f"{sizes[0]}:{sizes[1]} " + ", ".join(cells))
    print("      the Fano factor of part 0 (windows, its z^2): " + "; ".join(lines))


w37_s = mode_beat(kappa, 37, SIZE)
phase37 = [quotient(2 * PI * 37 * j, SIZE) for j in range(SIZE)]
turning_37 = [[laid(A, p, w37_s) for p in phase37], [laid(A, p - quotient(PI, 2), w37_s) for p in phase37]]
offset = OFFSET
print(f"(f) G5's pointer in vacuum, ported from g5_draw.py: a ring of 128 (each part pulled by its two neighbours at"
      f" the grip), the merge at Node-clock 0 and its two neighbours on the ring, the read rows' fine teeth, every"
      f" fine tooth born at H = W div 2 as G5 lays it; {ROUNDS_F} rounds; the 37-wave's beat"
      f" {places(w37_s, SCALE, 5)} against {places(w_s, SCALE, 5)}; a fine tooth moves by its push mod W, and W over"
      f" gcd(W, kappa) = {quotient(W, gcd(W, kappa))}, W over gcd(W, kappa, the grip) ="
      f" {quotient(W, gcd(gcd(W, kappa), grip))}:")
pointer_report("the turning hand at one phase, re and im read", [[quarter[0]] * SIZE, [quarter[1]] * SIZE],
               "hand", kappa, (0, 1))
pointer_report("the turning hand at the phase 2 pi 37 j over 128", turning_37, "hand", kappa, (0, 1))
pointer_report("the turning hand at the phase 2 pi 37 j over 128, its fine teeth born at 0", turning_37, "hand",
               kappa, (0, 1), 0)
pointer_report("the control laid in phase (im = re), one phase", [[quarter[0]] * SIZE, [quarter[0]] * SIZE],
               "hand", kappa, (0, 1))
pointer_report("the control laid in phase, the phase 2 pi 37 j over 128", [turning_37[0], list(turning_37[0])],
               "hand", kappa, (0, 1))
pointer_report("the old standing count at n, laid 10^3 off it, read alone",
               [[(n + 1000, n + 1000, 0)] * SIZE], "count", kappa, (0,))
pointer_report("the old standing count at n, a tied row laid at 10^3 (the old linear tie), the count read alone",
               [[(n, n, 0)] * SIZE, [(1000, 1000, 0)] * SIZE], "tied", kappa, (0,))
pointer_report("the old standing count at n, a tied row laid at 10 (its tooth's move near G5's 10^16), read alone",
               [[(n, n, 0)] * SIZE, [(10, 10, 0)] * SIZE], "tied", kappa, (0,))
pointer_report("the turning hand at kappa + 1, one phase", [[quarter[0]] * SIZE, [quarter[1]] * SIZE],
               "hand", kappa + 1, (0, 1))
pointer_report(f"the turning hand at kappa + {offset}, one phase, its teeth off W's lattice",
               [[quarter[0]] * SIZE, [quarter[1]] * SIZE], "hand", kappa + offset, (0, 1))
es_forward, _, end_f = pointer_run(born_at_h(turning_37), "hand", kappa, (0, 1), 1000)
es_back, _, back_f = pointer_run([[mirrored(s) for s in row] for row in end_f], "hand", kappa, (0, 1), 1000)
returned = [[mirrored(s) for s in row] for row in back_f] == born_at_h(turning_37)
print(f"    the run back with the draw read, the turning hand at the phase 2 pi 37 j over 128: 1,000 rounds, the"
      f" mirror, 1,000 rounds, the mirror: bit for bit {returned};"
      f" the pointer read on the way back is the forward one reversed: {es_back == es_forward[::-1]}")
