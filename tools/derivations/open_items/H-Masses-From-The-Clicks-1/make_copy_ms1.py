"""ms1's flagged COPY of the engine's src (engine-5.0-test af06713db), written by this script and never by hand; David's src is untouched.
The copy: tools/derivations/open_items/H-Masses-From-The-Clicks-1/src_ms1/event_universe, src/event_universe with these exact text replacements, each matched once or the script refuses.
The flag is a key of ms1's OWN world copies, `ms1`: {"lay": "action", "rows": "circle"}; a world without the key runs David's path bit for bit.

Flag lay = "action" (MS-S1, the charge's universality, the law's letter: ALGEBRA.md, The charge written is the Wronskian over T div 2 for every reader; K-S2):
  take.lay_amplitude returns node.A = largest_below(T div 2) for every row (the quarter-turn lay at A^2 = T div 2, W = +-A^2 the same for every row);
  close.births books the TAKEN row's unit (the gap-0 plane's, 3 den T) per child, the lone child's share 6 den A^2 = 3 den T (2 A^2 / T) to one part in 400:
  what the lay books is light's quantum per child, the child's pair entering nowhere.
Flag rows = "circle" (MS-S2, the selection of the pairs): the universe file's gapped plane rows are replaced at the load by EVERY exact point (num, s) of den's circle,
  num^2 + s^2 = den^2, 0 < num < den, sorted by the leg s (the massless plane first, then the points, then the file's other rows in their order);
  the record's universe carries the derived rows so the decoder names them; the file's gapped pairs are read by nothing.
Run: python make_copy_ms1.py  (writes src_ms1/ beside it)."""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, "..", "..", "..", "src", "event_universe"))
DST = os.path.join(HERE, "src_ms1", "event_universe")


def replace_once(path, old, new):
    text = open(path, encoding="utf-8").read()
    if text.count(old) != 1:
        raise SystemExit(f"{path}: the text to replace matches {text.count(old)} times, not once:\n{old}")
    open(path, "w", encoding="utf-8").write(text.replace(old, new))


def main():
    if os.path.isdir(os.path.join(HERE, "src_ms1")):
        shutil.rmtree(os.path.join(HERE, "src_ms1"))
    shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns("__pycache__"))

    # 1. the world file's key `ms1`, ms1's flags (refused by David's loader; allowed in the copy alone)
    replace_once(
        os.path.join(DST, "loader", "world.py"),
        'WORLD_KEYS = frozenset({"universe", "shape", "intervals", "seed"})',
        'WORLD_KEYS = frozenset({"universe", "shape", "intervals", "seed", "ms1"})  # ms1: the flags of the hand\'s copy',
    )
    # 2. the Node reads the flags once at the load; the circle's rows replace the file's gapped planes under rows = "circle"
    replace_once(
        os.path.join(DST, "node.py"),
        "        self.T, self.G = int(ints[\"quantum_action\"]), link_unit_of(self.gamma)\n",
        "        self.T, self.G = int(ints[\"quantum_action\"]), link_unit_of(self.gamma)\n"
        "        self.ms1 = dict(world.get(\"ms1\", {}))  # ms1: the flags, {} on David's path\n"
        "        if self.ms1.get(\"rows\") == \"circle\":\n"
        "            from event_universe.circle import circle_rows  # ms1: MS-S2, the rows from den alone\n\n"
        "            universe[\"rows\"] = circle_rows(universe)\n",
    )
    # 3. the lay's amplitude: the law's A for every row under lay = "action"
    replace_once(
        os.path.join(DST, "take.py"),
        "    r = node.rule_of(node.records()[s], c, factors)\n    reaches = sum(int(np.asarray(x)[at]) for x in r.reaches)\n",
        "    if node.ms1.get(\"lay\") == \"action\":  # ms1: MS-S1, A^2 = T div 2 for every row, the charge W = A^2 universal\n"
        "        return node.A\n"
        "    r = node.rule_of(node.records()[s], c, factors)\n    reaches = sum(int(np.asarray(x)[at]) for x in r.reaches)\n",
    )
    # 4. the take books the taken row's unit per child under lay = "action"
    replace_once(
        os.path.join(DST, "close.py"),
        "        walls = sum(2 * node.units[s] for s, _m, _p, _r in by_node[at])\n",
        "        walls = sum(\n"
        "            2 * (node.unit_gap0 if node.ms1.get(\"lay\") == \"action\" else node.units[s])  # ms1: MS-S1, light's quantum per child\n"
        "            for s, _m, _p, _r in by_node[at]\n"
        "        )\n",
    )
    # 5. the circle module (ms1's own; nothing of David's)
    open(os.path.join(DST, "circle.py"), "w", encoding="utf-8").write(CIRCLE)
    print("written", DST)


CIRCLE = '''"""ms1 (MS-S2): the exact points of den\'s circle, num^2 + s^2 = den^2 with 0 < num < den and s > 0, from den\'s primes alone (every prime 1 mod 4 as a sum of two squares by a search by comparisons; the Gaussian factors composed over every exponent): the plane rows of the universe under the flag rows = "circle"."""
from __future__ import annotations

from collections import Counter
from typing import Any

from event_universe.core.rule3 import largest_below


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % a == 0:
            return n == a
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a


def rho(n: int) -> list[int]:
    if is_prime(n):
        return [n]
    c = 1
    while True:
        x = y = 2
        d = 1
        while d == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = gcd(abs(x - y), n)
        if d != n:
            return sorted(rho(d) + rho(n // d))
        c += 1


def factor(n: int) -> list[int]:
    found = []
    p = 2
    while p * p <= n and p < 2 * 10**6:
        while n % p == 0:
            found.append(p)
            n //= p
        p += 1 if p == 2 else 2
    if n > 1:
        found += rho(n)
    return sorted(found)


def two_squares(p: int) -> tuple[int, int]:
    a = largest_below(p)
    while a * a > p // 2:
        b2 = p - a * a
        b = largest_below(b2)
        if b * b == b2:
            return a, b
        a -= 1
    raise ValueError(f"{p} is no sum of two squares")


def points(den: int) -> list[tuple[int, int]]:
    """Every exact point (num, s) of den\'s circle, sorted by the leg s."""
    exps = Counter(factor(den))
    gauss, real = [], 1
    for p, e in sorted(exps.items()):
        if p == 2 or p % 4 == 3:
            real *= p**e
        else:
            a, b = two_squares(p)
            gauss.append((a, b, e))
    found: set[tuple[int, int]] = set()

    def walk(k: int, re: int, im: int) -> None:
        if k == len(gauss):
            num, s = abs(re * real), abs(im * real)
            if 0 < num < den and s > 0:
                found.add((num, s))
            return
        a, b, e = gauss[k]
        for j in range(2 * e + 1):
            r, i = re, im
            for _ in range(j):
                r, i = r * a - i * b, r * b + i * a
            for _ in range(2 * e - j):
                r, i = r * a + i * b, i * a - r * b
            walk(k + 1, r, i)

    walk(0, 1, 0)
    return sorted(found, key=lambda p: p[1])


def circle_rows(universe: dict[str, Any]) -> list[dict[str, Any]]:
    """The universe\'s rows with every gapped plane of the file replaced by den\'s exact points (sorted by leg), the massless plane first, the other rows in the file\'s order."""
    den = int(universe["integers"]["den"])
    rows = universe["rows"]
    massless = [r for r in rows if int(r["shape"]) == 2 and r.get("pair") and int(r["pair"][0]) == den]
    others = [r for r in rows if not (int(r["shape"]) == 2 and r.get("pair"))]
    return massless + [{"shape": 2, "pair": [num, den]} for num, _s in points(den)] + others
'''


if __name__ == "__main__":
    main()
