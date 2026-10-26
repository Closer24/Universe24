"""ms2: den's circle as the selection law of the pairs (candidate (a), the Pythagorean points), integers only.
Usage: python ms2_circle.py <universe.json> [more universe.json ...]
For each universe file: den factored (trial division by the division act), its primes 1 mod 4 as a^2 + b^2, every point (num, s)
of den's circle with num^2 + s^2 = den^2, num > 0, s > 0 (the Gaussian products; 3^k - 1 points for k distinct primes 1 mod 4),
each point's g = (den - num) per 10^9 of den, its leg s, whether each of the file's typed nums is a point (exact) or off the circle
(sine_den inexact: the remainder den^2 - num^2 - s^2 above 0), the ratios of the legs of the typed pairs and of every point to the
smallest leg as integers per 10^9, nature's ratios beside; the law's condition 4 a b | T per prime (K-S3's "integral lay"); the
quarter-turn lay's A and W = A^2 per row (the engine's lay_amplitude at the vacuum) against the rest lay's W = A^2 s div den at the
amplitude fitted to one unit (the seed's lay), against T div 2.
PREDICTION (before the run): universe_toy's den has three primes 1 mod 4 (617, 196,613 and a third), 26 points; the three typed
nums are 3 of the 26 (exact points); the typed legs' ratio heavy/light about 1,836,15x,xxx per 10^6 (nature 1,836,152,673);
4 a b | T fails for 617 (4 x 19 x 16 = 1,216 does not divide 36,000); the quarter-turn W: 25 / about 19,300 / 36,100; the rest-lay
W: 18,000 within a few levels for every row. The toy den 1,021 = 30^2 + 11^2: 2 points (779, 660) and (660, 779)."""
import json, sys
sys.set_int_max_str_digits(0)
from event_universe.core.paces import sine_den
from event_universe.core.rule3 import largest_below, link_unit_of, unit_of, quotient

BILLION = 10 ** 9
NATURE = {"p/e": 1836152673430, "n/e": 1838683661, "n/p": 1001378419, "mu/e": 206768283, "tau/e": 3477228,
          "pi+/e": 273132, "K+/e": 966116}  # p/e per 10^9, the rest per 10^6 (CODATA 2018 / PDG), the far reader's record

def factor(n):
    found = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            found.append(d); n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        found.append(n)
    return found

def two_squares(p):
    a = 1
    while a * a <= p:
        b2 = p - a * a
        b = largest_below(b2)
        if b * b == b2 and b >= a:
            return a, b
        a += 1
    return None

def points(den):
    """Every (x, y) with x^2 + y^2 = den^2, x > 0, y > 0, by Gaussian products over den's primes; the primes 3 mod 4 and the 2s scale."""
    primes = factor(den)
    units = [(1, 0)]
    scale = 1
    gauss = []
    for p in sorted(set(primes)):
        e = primes.count(p)
        if p % 4 == 1:
            a, b = two_squares(p)
            gauss.append(((a, b), e))
        else:
            scale *= p ** e
    # for den^2 each prime 1 mod 4 has exponent 2e; choose j in 0..2e copies of pi and 2e - j of conj(pi)
    pts = {(scale, 0)}
    for (a, b), e in gauss:
        new = set()
        for (x, y) in pts:
            for j in range(2 * e + 1):
                zx, zy = 1, 0
                for _ in range(j):
                    zx, zy = zx * a - zy * b, zx * b + zy * a
                for _ in range(2 * e - j):
                    zx, zy = zx * a + zy * b, -zx * b + zy * a
                new.add((x * zx - y * zy, x * zy + y * zx))
        pts = new
    out = set()
    for x, y in pts:
        for sx in (1, -1):
            for sy in (1, -1):
                for (u, v) in ((x, y), (y, x)):
                    if sx * u > 0 and sy * v > 0:
                        out.add((sx * u, sy * v))
    out = sorted(out)
    for x, y in out:
        assert x * x + y * y == den * den
    return primes, gauss, out

def main(paths):
    for path in paths:
        uni = json.load(open(path))
        ints = uni["integers"]
        den, gamma, T = int(ints["den"]), int(ints["node_clock"]), int(ints["quantum_action"])
        G = link_unit_of(gamma)
        print("=" * 60)
        print(path, "den", den, "bits", den.bit_length(), "Gamma", gamma, "T", T, "G", G)
        primes, gauss, pts = points(den)
        print("primes", primes, "as a^2 + b^2:", gauss)
        print("points of den's circle (num > 0, s > 0):", len(pts), "(3^k - 1 for k primes 1 mod 4)")
        typed = [tuple(r["pair"]) for r in uni["rows"] if r.get("pair") and int(r["shape"]) == 2 and r["pair"][0] != r["pair"][1]]
        typed_nums = [int(p[0]) for p in typed]
        legs = {}
        print("  num | g per 10^9 | leg s | leg/den per 10^9 | typed?")
        for num, s in sorted(pts, key=lambda p: p[1]):
            legs[num] = s
            print(f"  {num} | {(den - num) * BILLION // den} | {s} | {s * BILLION // den} | {'TYPED' if num in typed_nums else ''}")
        for num in typed_nums:
            s = sine_den(num, den)
            rem = den * den - num * num - s * s
            print(f"typed num {num}: sine_den {s}, remainder den^2 - num^2 - s^2 = {rem} ({'ON the circle' if rem == 0 else 'OFF the circle'})")
        # ratios
        least = min(legs.values())
        ratios = sorted(set(s * BILLION // least for s in legs.values()))
        print("every point's leg over the least leg, per 10^9:", ratios)
        if len(typed_nums) >= 2:
            tl = sorted(sine_den(n, den) for n in typed_nums)
            print("typed legs ratios over the least typed leg per 10^9:", [s * BILLION // tl[0] for s in tl[1:]],
                  "| heaviest over second per 10^9:", tl[-1] * BILLION // tl[-2] if len(tl) > 2 else None)
            # the gaps' ratios (the Rule3 mass D is 12 (den - num) p0^2 G^2)
            tg = sorted(den - n for n in typed_nums)
            print("typed gaps (den - num) ratios over the least per 10^9:", [g * BILLION // tg[0] for g in tg[1:]])
        print("nature (the far reader): p/e", NATURE["p/e"], "per 10^9; n/p", NATURE["n/p"], "per 10^9; mu/e", NATURE["mu/e"], "per 10^6")
        # the law's T condition
        for (a, b), e in gauss:
            print(f"  prime {a * a + b * b} = {a}^2 + {b}^2: 4ab = {4 * a * b}, T mod 4ab = {T % (4 * a * b)} ({'divides' if T % (4 * a * b) == 0 else 'DOES NOT divide'})")
        # the quarter-turn lay's W against the rest lay's W, per row (at the vacuum, lone record)
        print("  row num | unit 3Ts | quarter-turn A, W = A^2 | rest-lay A (share <= unit), W = A^2 s div den | T div 2 =", T // 2)
        for num in typed_nums + [den]:
            s = sine_den(num, den) if num != den else den
            unit = unit_of(s, T)
            weight = 12 * gamma * gamma * G * G * (2 * den - num)
            target = unit * 4 * gamma * gamma * G * G
            A = largest_below(quotient(target, weight))
            while weight * A * A < target:
                A += 1
            # the rest lay (seed.rest_record) of a lone record: re (A, A num div den), im (0, A s div den); the share at the vacuum
            # for a lone record: [w (now^2 + before^2) - S now before] doubled over 4 Gamma^2 G^2 per line (no neighbours)
            w = 6 * den * gamma * gamma * G * G
            D = 12 * (den - num) * gamma * gamma * G * G
            R = 6 * 2 * num * gamma * gamma * G * G
            S = 2 * w - D - R
            def share(a):
                rn, rb, inw, ib = a, quotient(a * num, den), 0, quotient(a * s, den)
                f = 0
                for n_, b_ in ((rn, rb), (inw, ib)):
                    f += 2 * (w * (n_ * n_ + b_ * b_) - S * n_ * b_)
                return quotient(f, 4 * gamma * gamma * G * G)
            hi = 1
            while share(hi) <= unit:
                hi *= 2
            lo = 0
            while hi - lo > 1:
                mid = (lo + hi) // 2
                if share(mid) <= unit:
                    lo = mid
                else:
                    hi = mid
            Ar = lo
            Wr = Ar * quotient(Ar * s, den)
            print(f"  {num} | {unit} | {A}, {A * A} | {Ar}, {Wr} (share {share(Ar)} of unit {unit}) | W per (T div 2) per 10^9: quarter {A * A * BILLION // (T // 2)}, rest {Wr * BILLION // (T // 2)}")

if __name__ == "__main__":
    main(sys.argv[1:])
