"""The fair draw on the dial, exact: the rule, its distribution over a full turn, and the head's sorted draw beside it.

usage: python3 -I p1_fair_draw_exact.py
The rule (David's proposal for stage 9's split click):
  the number  d = (c + V) mod L, one carry: c the Node-clock's own beat count (its dial, one step per due beat),
              V the sum of the A1 rows' fine teeth over the Node-clock and its six neighbours (24-invariant), and
              L = sigma_1 + ... + sigma_k the parts' sizes' total;
  the part    the rank count of d among the cumulative sizes S_i = sigma_1 + ... + sigma_i: part = SUM_i nonneg(d - S_i),
              i = 1 .. k - 1, no sort and no if;
  the twins   on a hand's twins against a detector, sigma_up = N(<phi, psi>) = (rho rho_d + S . m) / 2 (Fierz, exact on
              Gaussian integers), L = rho rho_d, and down = (2 d - S . m + L) div (2 L), one carry.
Checked here by enumeration, exact integers: (1) over every full turn of the dial (L consecutive beats) each part is
drawn exactly sigma_i times; (2) the same over L consecutive values of any one of the seven digits, the others fixed;
(3) the twin form gives sigma_up exactly, and sigma_up / L = cos^2(theta / 2); (4) the head's draw, the digits sorted
and composed by Horner modulo M (draw.py, vernier), over every combination of its digits: equal parts drawn 7/8 and
15/16 where a fair draw gives 1/2 (the plan's M2 figures), and the own digit framed o + |r - o| on the whole base.
"""
import random
from fractions import Fraction


def nonneg(n):
    return (n // (n * n + 1)) + 1  # the algebra's one whether: 1 where n >= 0, 0 below


def part_of(d, sizes):
    s, rank = 0, 0
    for sigma in sizes[:-1]:
        s += sigma
        rank += nonneg(d - s)
    return rank


def draw(c, digits, sizes):
    L = sum(sizes)
    return part_of((c + sum(digits)) % L, sizes)


rng = random.Random(29)
cases = exact = 0
for L in range(1, 121):
    for _ in range(12):
        k = rng.randint(1, min(L, 6))
        cuts = sorted(rng.sample(range(1, L), k - 1)) if k > 1 else []
        sizes = [b - a for a, b in zip([0] + cuts, cuts + [L])]
        if rng.random() < 0.3 and k > 1:  # a part of size 0 among them, which must never be drawn
            sizes.insert(rng.randrange(len(sizes)), 0)
        digits = [rng.randrange(10**30) for _ in range(7)]
        c0 = rng.randrange(10**12)
        counts = [0] * len(sizes)
        for c in range(c0, c0 + L):
            counts[draw(c, digits, sizes)] += 1
        cases += 1
        exact += counts == sizes
        # (2) one digit's full turn, the dial fixed
        j = rng.randrange(7)
        counts2 = [0] * len(sizes)
        for v in range(digits[j], digits[j] + L):
            dd = digits[:j] + [v] + digits[j + 1:]
            counts2[draw(c0, dd, sizes)] += 1
        cases += 1
        exact += counts2 == sizes
print(f"(1, 2) the rank count over a full turn: {exact} of {cases} cases drew each part exactly sigma_i times "
      f"(L from 1 to 120, 1 to 6 parts, parts of size 0 included, the dial's turn and one digit's turn)")


def gauss_norm(z):
    return z.real * z.real + z.imag * z.imag


def spin(p):  # S = (2 Re(p1* p2), 2 Im(p1* p2), |p1|^2 - |p2|^2), integers for Gaussian-integer spinors
    a, b = p
    x = a.conjugate() * b
    return (int(2 * x.real), int(2 * x.imag), int(gauss_norm(a) - gauss_norm(b)))


def gi(r):
    return complex(rng.randint(-r, r), rng.randint(-r, r))


ok_fierz = ok_draw = n = 0
worst = Fraction(0)
for _ in range(400):
    psi, phi = (gi(4), gi(4)), (gi(4), gi(4))
    rho, rho_d = int(gauss_norm(psi[0]) + gauss_norm(psi[1])), int(gauss_norm(phi[0]) + gauss_norm(phi[1]))
    if rho == 0 or rho_d == 0:
        continue
    n += 1
    S, m = spin(psi), spin(phi)
    sm = sum(x * y for x, y in zip(S, m))
    inner = phi[0].conjugate() * psi[0] + phi[1].conjugate() * psi[1]
    sigma_up = int(gauss_norm(inner))
    ok_fierz += 2 * sigma_up == rho * rho_d + sm
    L = rho * rho_d
    V = rng.randrange(10**20)
    ups = 0
    for c in range(L):
        d = (c + V) % L
        down = (2 * d - sm + L) // (2 * L)
        ups += 1 - down
    ok_draw += ups == sigma_up
    cos = Fraction(sm, rho * rho_d)  # cos theta, exact, since |S| = rho and |m| = rho_d
    worst = max(worst, abs(Fraction(ups, L) - (1 + cos) / 2))
print(f"(3) the twins: Fierz sigma_up = (rho rho_d + S . m) / 2 exact in {ok_fierz} of {n}; the carry's side drew up "
      f"exactly sigma_up times over the full turn in {ok_draw} of {n}; the largest |ups / L - cos^2(theta / 2)| = {worst}")


def head_compose(digits_with_bases, M):
    carry, room = 0, 1
    for d, b in sorted(digits_with_bases):
        carry = (carry * b + d) % M
        room = min(room * b, M)
    return carry, room


def head_equal_parts(n_digits, base, M):
    """P(up) on equal parts (up where 2 c < room) over every combination of the digits, each over its whole base."""
    import itertools
    ups = total = 0
    for combo in itertools.product(range(base), repeat=n_digits):
        c, room = head_compose([(d, base) for d in combo], M)
        ups += 2 * c < room
        total += 1
    return Fraction(ups, total)


print("(4) the head's draw (the digits sorted, then composed by Horner modulo M; up where 2 c < room), over every "
      "combination of its digits, on equal parts where a fair draw gives 1/2:")
for nd, base, M in ((2, 2, 64), (3, 2, 64), (4, 2, 64), (3, 3, 64), (3, 4, 64), (4, 3, 81), (3, 6, 1000), (7, 2, 1000)):
    p = head_equal_parts(nd, base, M)
    print(f"    {nd} digits of base {base}, M {M}: P(up) = {p} = {float(p):.4f}")


def sum_equal_parts(n_digits, base, L):
    import itertools
    ups = total = 0
    for combo in itertools.product(range(base), repeat=n_digits):
        d = sum(combo) % L
        ups += 2 * d < L
        total += 1
    return Fraction(ups, total)


print("    beside it, the sum modulo L over the same combinations, up where 2 d < L:")
for nd, base, L in ((3, 2, 2), (4, 2, 2), (3, 4, 2), (3, 4, 4), (3, 6, 6), (7, 2, 2)):
    p = sum_equal_parts(nd, base, L)
    print(f"    {nd} digits of base {base}, L {L}: P(up) = {p}")
print("      (exact wherever the base is a multiple of L: one digit's full turn then covers each residue alike;"
      " the dial c supplies that turn for every L)")

# the own digit framed o + |r - o| on the whole base w (the head's 42d5448b7 frame), over the digit's full turn
w = 17
o = (w - 1) // 2
framed = [o + abs(r - o) for r in range(w)]
upper = sum(1 for x in framed if 2 * x >= w)
print(f"(4') the head's own digit framed o + |r - o| on the whole base {w}: {upper} of {w} values in the upper half "
      f"(a fair digit puts {w // 2} or {w // 2 + 1} there)")
