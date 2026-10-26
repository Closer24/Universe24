"""cs3: den's circle (MS-S2's finding: the rows with a gap are the exact points num^2 + s^2 = den^2 of den's circle), integers only: den factored by trial division, its primes 1 mod 4 as a^2 + b^2, every point by the Gaussian products, and the universe files written: universe_c5.json (universe_toy's rows plus the two circle neighbours of the typed heavy row 2458210083751875) and universe_c14.json (universe_toy's rows plus every other point of the circle with num below s, the heavy half, and the typed light lift's mirror).
Usage: python circle.py <universe_toy.json> <out_dir>"""
import json
import sys

from event_universe.core.rule3 import largest_below


def factor(n):
    found, d = [], 2
    while d * d <= n:
        while n % d == 0:
            found.append(d)
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        found.append(n)
    return found


def two_squares(p):
    a = 1
    while a * a <= p:
        b2 = p - a * a
        b = largest_below(b2)
        if b * b == b2:
            return a, b
        a += 1
    return None


def gmul(u, v):
    return (u[0] * v[0] - u[1] * v[1], u[0] * v[1] + u[1] * v[0])


def gpow(u, k):
    r = (1, 0)
    for _ in range(k):
        r = gmul(r, u)
    return r


def points(den):
    """Every (num, s) with num^2 + s^2 = den^2, num > 0, s > 0: the Gaussian integers of norm den^2, pi^j conj(pi)^(2e - j) over den's primes 1 mod 4 (the primes 3 mod 4 scale), integers only."""
    primes = factor(den)
    pts = {(1, 0)}
    scale = 1
    for p in sorted(set(primes)):
        e = primes.count(p)
        if p % 4 != 1:
            scale *= p ** e
            continue
        a, b = two_squares(p)
        pi, conj = (a, b), (a, -b)
        new = set()
        for pt in pts:
            for j in range(2 * e + 1):
                new.add(gmul(pt, gmul(gpow(pi, j), gpow(conj, 2 * e - j))))
        pts = new
    found = set()
    for x, y in pts:
        x, y = abs(x) * scale, abs(y) * scale
        if x > 0 and y > 0:
            found.add((x, y))
            found.add((y, x))
    found = sorted(found)
    assert all(x * x + y * y == den * den for x, y in found)
    return found


def main(argv):
    sys.set_int_max_str_digits(0)
    with open(argv[1], encoding="utf-8") as f:
        toy = json.load(f)
    den = int(toy["integers"]["den"])
    pts = points(den)
    typed = [int(r["pair"][0]) for r in toy["rows"] if r["shape"] == 2 and r["pair"][0] != r["pair"][1]]
    lines = [f"den {den} = {' x '.join(str(p) for p in factor(den))}; points with num > 0, s > 0: {len(pts)} ({len(pts) // 2} unordered pairs)"]
    for num, s in pts:
        g = (den - num) * 1000 // den
        lines.append(f"  num {num} s {s} g per mille {g} {'TYPED' if num in typed else ''}")
    heavy = [num for num, s in pts if num < s]
    nbrs = sorted(heavy, key=lambda n: abs(n - 2458210083751875))[1:3]
    lines.append(f"the heavy half (num < s): {len(heavy)}; the typed heavy row's two circle neighbours: {nbrs}")
    for name, extra in (("universe_c5.json", nbrs), ("universe_c14.json", [n for n in heavy if n not in typed])):
        u = {"integers": dict(toy["integers"]), "rows": list(toy["rows"])}
        rows = list(toy["rows"])
        head, tail = rows[:4], rows[4:]
        for n in extra:
            head.append({"shape": 2, "pair": [n, den]})
        u["rows"] = head + tail
        with open(f"{argv[2]}/{name}", "w", encoding="utf-8") as f:
            json.dump(u, f)
        lines.append(f"{name}: gapped rows {sum(1 for r in u['rows'] if r['shape'] == 2 and r['pair'][0] != r['pair'][1])}, records {sum(1 for r in u['rows'] if r['shape'] == 2)}; added {extra}")
    text = "\n".join(lines)
    print(text)
    with open(f"{argv[2]}/circle.txt", "w", encoding="utf-8") as f:
        f.write(text + "\n")


if __name__ == "__main__":
    main(sys.argv)
