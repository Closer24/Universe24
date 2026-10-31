"""The sixth text's own checks: whole numbers alone, every division Rule3's carry (ratios as reduced pairs), no float,
root, log, exponential or circular function. Usage: python3 -I term13_checks.py <src of main at 0df0e8385>"""

import sys

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402


def red(num, den):
    if den < 0:
        num, den = -num, -den
    a, b = abs(num), den
    while b:
        a, b = b, carry(a, b, 0)[1]
    return (carry(num, a, 0)[0], carry(den, a, 0)[0]) if a else (0, 1)


def add(x, y):
    return red(x[0] * y[1] + y[0] * x[1], x[1] * y[1])


def sub(x, y):
    return red(x[0] * y[1] - y[0] * x[1], x[1] * y[1])


def mul(x, y):
    return red(x[0] * y[0], x[1] * y[1])


def div(x, y):
    return red(x[0] * y[1], x[1] * y[0])


def le(x, y):
    return x[0] * y[1] <= y[0] * x[1]


def ratio_text(x):
    return f"{x[0]}/{x[1]}"


one = (1, 1)

# 1. the facing point: 2 m / s + 2 m / (d - s) >= 8 m / d for 0 < s <= d / 2, equality only at d = 2 s (m = 1)
ok, eq = True, []
for d in range(2, 41):
    for s in range(1, d + 1):
        if 2 * s > d:
            continue
        w = add(red(2, s), red(2, d - s))
        if not le(red(8, d), w):
            ok = False
        if w == red(8, d):
            eq.append((d, s))
print(f"1. facing point w >= 8 m / d on 0 < s <= d / 2, d = 2 to 40: {ok}; equality exactly at d = 2 s:"
      f" {all(d == 2 * s for d, s in eq) and len(eq) == 20}")

# 2. two thin shells of radius s = 8 gamma m touching (d = 2 s): on ball 1, |p - c2|^2 >= s^2, equality at contact only
s, d, worst, hits = 8, 16, None, []
for x in range(-8, 9):
    for y in range(-8, 9):
        for z in range(-8, 9):
            if x * x + y * y + z * z > s * s:
                continue
            q = (x - d) * (x - d) + y * y + z * z
            if q < s * s:
                worst = (x, y, z)
            if q == s * s:
                hits.append((x, y, z))
print(f"2. two touching thin shells at the bound: no point of ball 1 nearer c2 than s: {worst is None};"
      f" at distance s only {hits}")

# 3. the separations at 70 solar masses, G M / c^2 = 413455/4 m
L = red(70 * 1476625, 1000)
pair = mul((8, 1), L)
gen = mul((16, 3), L)
over = div(pair, (350000, 1))
print(f"3. G M / c^2 = {ratio_text(L)} m; 8 G M / c^2 = {ratio_text(pair)} m; over 350 km: {ratio_text(over)}"
      f" (2.3626 = 23626/10000: {over == red(23626, 10000)}); (16/3) G M / c^2 = {ratio_text(gen)} m,"
      f" 551273 m rounded down: {carry(gen[0], gen[1], 0)[0] == 551273}; over 350 km in thousandths, rounded down:"
      f" {carry(gen[0] * 1000, gen[1] * 350000, 0)[0]}")

# 4. Newton's shell mean of 1 / |x - y|: (1 / (2 rho b)) ((rho + b) - |rho - b|) = 1 / max(rho, b), so at least 1 / R
ok4 = True
for rho in range(1, 13):
    for b in range(1, 13):
        lhs = mul(red(1, 2 * rho * b), ((rho + b) - abs(rho - b), 1))
        if lhs != red(1, max(rho, b)) or not le(red(1, 12), lhs):
            ok4 = False
print(f"4. the shell mean 1 / max(rho, b), at least 1 / R inside the ball (R = 12, rho and b 1 to 12): {ok4};"
      f" the bound's"
      f" sum at m = 1/2, d = 1: 2 m / (d / 2) + 2 m / (3 d / 2) = {ratio_text(add((2, 1), (2, 3)))} = 16 m / (3 d)")

# 5. the frozen lay: gamma 1, a point of -1 inside a shell of 2 at r = 4; gamma 2, the shell at r = 8
rows5 = []
for gamma, shell_r in ((1, 4), (2, 8)):
    ok5 = True
    for n in range(0, 12):
        r = red(shell_r, n * n + 1)
        w = sub(red(4, shell_r), div((2, 1), r))  # 2 x 2 / shell_r from the shell, -2 / r from the point
        if sub(one, mul((2 * gamma, 1), w)) != (n * n, 1):
            ok5 = False
        u = red(1 + n, gamma)  # the plus branch
        tu = mul((gamma, 1), u)
        if mul(sub(one, tu), sub(one, tu)) != sub(one, mul((2 * gamma, 1), w)):
            ok5 = False
        if div(one, add(one, u)) != red(gamma, gamma + 1 + n):
            ok5 = False
    rows5.append(f"gamma {gamma}: 1 - 2 gamma w = n^2 at r = {shell_r} / (n^2 + 1), the plus branch"
                 f" u = (1 + n) / gamma,"
                 f" N^2 = gamma / (gamma + 1 + n), n = 0 to 11: {ok5}")
r_far = red(4, 1000 * 1000 + 1)
w_far = sub((1, 1), div((2, 1), r_far))
print("5. " + "; ".join(rows5) + f"; at r = 4/1000001 (gamma 1): 1 - 2 w = {ratio_text(sub(one, mul((2, 1), w_far)))},"
      f" N^2 = {ratio_text(div(one, add(one, (1001, 1))))}")

# 6. the clocks' floor: with t = gamma u, 1 - 2 gamma w = (1 - t)^2, so w >= 0 exactly when 0 <= t <= 2
ok6 = True
for k in range(-300, 301):
    t = red(k, 100)
    w_sign = mul(t, sub((2, 1), t))  # 2 gamma w = t (2 - t)
    inside = le((0, 1), t) and le(t, (2, 1))
    if le((0, 1), w_sign) != inside:
        ok6 = False
print(f"6. 2 gamma w = t (2 - t) >= 0 exactly when 0 <= t <= 2, t from -3 to 3 in hundredths: {ok6}; N^2 floors"
      f" gamma / (gamma + 2) at gamma 1, 2, 3: {[ratio_text(red(g, g + 2)) for g in (1, 2, 3)]};"
      f" with grips at or above 0"
      f" gamma / (gamma + 1): {[ratio_text(red(g, g + 1)) for g in (1, 2, 3)]}")

# 7. thick marginal shells: 3 (s^2 - r1^2) / (s^3 - r1^3) = 1/2 on the cavity; (grip / g)^2 = 1 - 2 w at r = 4
rows7 = []
SHELLS = ((red(10, 7), red(40, 7)), (red(18, 7), red(36, 7)), (red(22, 37), red(220, 37)), (red(130, 43), red(208, 43)))
for r1, s7 in SHELLS:
    s2, r12 = mul(s7, s7), mul(r1, r1)
    s3, r13 = mul(s2, s7), mul(r12, r1)
    k = div(one, sub(s3, r13))  # 4 pi rho / 3 at mass 1
    cavity = mul((3, 1), mul(sub(s2, r12), k))
    r = (4, 1)
    w4 = mul((2, 1), mul(k, add(div(sub(mul(mul(r, r), r), r13), r), mul((3, 2), sub(s2, mul(r, r))))))
    rows7.append(f"({ratio_text(r1)}, {ratio_text(s7)}): cavity w = {ratio_text(cavity)}, (grip / g)^2 at r = 4"
                 f" {ratio_text(sub(one, mul((2, 1), w4)))}")
print("7. " + "; ".join(rows7))

# 8. the dumbbell: two uniform balls, m = 1/2, radius 4, centres 14 apart: w <= 3 m / s + 2 m / 10 inside a ball
print(f"8. the dumbbell's bound inside a ball: 3 m / s + 2 m / (14 - 4) = {ratio_text(add(red(3, 8), red(1, 10)))};"
      f" outside both at most 2 m / 4 + 2 m / 10 = {ratio_text(add(red(1, 4), red(1, 10)))}; the nearest surface point"
      f" to the centre of mass at 14 / 2 - 4 = 3")

# 9. the closed form: SUM_i (SUM over i's Meshes of d_j - d_i) / W_i = SUM over Meshes (d_i - d_j)^2 / (W_i W_j)
ok9, seed = True, 12345
for trial in range(50):
    n = 8
    dvals = []
    for i in range(n):
        seed = carry(seed * 1103515245 + 12345, 2 ** 31, 0)[1]
        dvals.append(carry(seed, 41, 0)[1] - 20)
    w0 = 1000
    lhs, rhs = (0, 1), (0, 1)
    for i in range(n):
        lap = dvals[carry(i + 1, n, 0)[1]] + dvals[carry(i + n - 1, n, 0)[1]] - 2 * dvals[i]
        lhs = add(lhs, red(lap, w0 + dvals[i]))
        j = carry(i + 1, n, 0)[1]
        rhs = add(rhs, red((dvals[i] - dvals[j]) ** 2, (w0 + dvals[i]) * (w0 + dvals[j])))
    if lhs != rhs:
        ok9 = False
print(f"9. the closed form on 50 rings of 8 (whole swings within 20, W0 = 1000): {ok9}")

# 10. z: (1 + z)^2 <= 2 at gamma 1, and 1.4142^2 < 2 < 1.4143^2
print(f"10. 14142^2 < 2 x 10^8 < 14143^2: {14142 * 14142 < 2 * 10 ** 8 < 14143 * 14143}")

# 11. light's three-dimensional s-wave form: r^2 (2 - x) J = 128 x (2 - x) / (1 - x^2)^4, r^2 p = 2
ok11 = True
for k in range(1, 20):
    x = red(k, 20)
    q = sub(one, mul(x, x))
    r = div((4, 1), q)
    jac = div(mul((8, 1), x), mul(q, q))
    p = div(mul(q, q), (8, 1))
    weight = mul(mul(mul(r, r), sub((2, 1), x)), jac)
    if weight != div(mul(mul((128, 1), x), sub((2, 1), x)), mul(mul(q, q), mul(q, q))) or mul(mul(r, r), p) != (2, 1):
        ok11 = False
print(f"11. the s-wave weight and p = 2 at x = k / 20, k = 1 to 19: {ok11}")

# 12. general relativity in isotropic radius: R = r (1 + M / (2 r))^2, 4 r (R - 2 M) = (2 r - M)^2
ok12 = True
for rr in range(1, 30):
    for mm in range(1, 8):
        r, m = red(rr, 3), (mm, 1)
        big_r = mul(r, mul(add(one, div(m, mul((2, 1), r))), add(one, div(m, mul((2, 1), r)))))
        left = mul(mul((4, 1), r), sub(big_r, mul((2, 1), m)))
        right = mul(sub(mul((2, 1), r), m), sub(mul((2, 1), r), m))
        if left != right:
            ok12 = False
print(f"12. 4 r (R - 2 M) = (2 r - M)^2 on a grid: {ok12}")

# 13. the double pulsar: the excess 3/7 and 3/4 against 0.0034 and 0.0084, rounded down
print(f"13. 3/7 over 0.0034: {carry(3 * 10000, 7 * 34, 0)[0]}; 3/4 over 0.0034: {carry(3 * 10000, 4 * 34, 0)[0]};"
      f" 3/7 over 0.0084: {carry(3 * 10000, 7 * 84, 0)[0]}; 3/4 over 0.0084: {carry(3 * 10000, 4 * 84, 0)[0]}")

# 14. the pair bound's general form (Big Pic, 6536901666 item 1), the seventh text's check. Each spherical body with a
#     source at or above 0 holds w = 2 m / r outside it, the fields add, and the contact point of two touching bodies
#     must keep w at or below 1 / (2 gamma): 4 gamma (m1 s2 + m2 s1) <= s1 s2. Then d = s1 + s2 meets the bound
#     d >= 4 gamma (sqrt m1 + sqrt m2)^2, written with no root: with D = d / (4 gamma), D >= M and (D - M)^2 >= 4 m1 m2.
def pair_bound(m1, m2, s1, s2, gamma):
    d, big = s1 + s2, m1 + m2
    lawful = 4 * gamma * (m1 * s2 + m2 * s1) <= s1 * s2
    held = d >= 4 * gamma * big and (d - 4 * gamma * big) ** 2 >= 16 * gamma * gamma * 4 * m1 * m2
    exact = d >= 4 * gamma * big and (d - 4 * gamma * big) ** 2 == 16 * gamma * gamma * 4 * m1 * m2
    return lawful, held, exact


lays = broken = 0
for gamma in (1, 2):
    for m1, m2 in ((1, 1), (2, 1), (3, 2), (10, 1), (49, 1), (36, 29)):
        for s1 in range(1, 701):
            for s2 in range(1, 701):
                lawful, held, _ = pair_bound(m1, m2, s1, s2, gamma)
                lays += lawful
                broken += lawful and not held
w49 = add(red(2 * 49, 224), red(2 * 1, 32))
w10 = add(red(2 * 10, 53), red(2 * 1, 17))
w11 = add(red(2 * 1, 8), red(2 * 1, 8))
wrong = add(red(2 * 49, 128), red(2 * 1, 128))
k_rows = [ratio_text(red(4 * (k + 1) ** 2, k * k + 1)) for k in (1, 7, 1000)]
# 10:1, the bound over M between 6.299 and 6.300: D = 6.299 x 11 / 4 lies below it, 6.300 x 11 / 4 on or above it
low10 = (6299 * 11 - 4000 * 11) ** 2 < 4 * 10 * 1 * 4000 ** 2
high10 = (6300 * 11 - 4000 * 11) ** 2 >= 4 * 10 * 1 * 4000 ** 2
# 36:29, D in thousandths of the mass unit between 129.621 and 129.622, and in metres at 70 solar masses (413455 / 65 m
# a unit)
low36 = (129621 - 65000) ** 2 < 4 * 36 * 29 * 1000 ** 2
high36 = (129622 - 65000) ** 2 >= 4 * 36 * 29 * 1000 ** 2
km_low, km_high = carry(129621 * 413455, 65 * 1000, 0)[0], carry(129622 * 413455, 65 * 1000, 0)[0]
print(f"14. the pair bound's general form, (D - M)^2 >= 4 m1 m2 with D = d / (4 gamma) >= M, on every pair of touching"
      f" shells of whole radii 1 to 700 whose contact keeps w at or below 1 / (2 gamma), gamma 1 and 2, masses 1:1, 2:1,"
      f" 3:2, 10:1, 49:1 and 36:29: {lays} lays, {broken} below the bound; reached at 49:1 by radii 224 and 32"
      f" (contact w {ratio_text(w49)}, {pair_bound(49, 1, 224, 32, 1)[2]}) and at 1:1 by 8 and 8 (contact w"
      f" {ratio_text(w11)}, {pair_bound(1, 1, 8, 8, 1)[2]}); 10:1 at 53 and 17, contact w {ratio_text(w10)}, above the"
      f" bound, which lies between 6.299 and 6.300 M: {low10 and high10}; 49:1 at 128 and 128 breaks the ceiling (contact"
      f" w {ratio_text(wrong)}); the bound over M at k^2:1 for k = 1, 7, 1000: {k_rows}, falling toward 4; at 36:29 D lies"
      f" between 129.621 and 129.622 of the mass unit: {low36 and high36}, d between {km_low} and {km_high + 1} m at 70"
      f" solar masses")
