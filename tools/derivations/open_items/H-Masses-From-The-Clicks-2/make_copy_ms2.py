"""ms2's flagged COPY of src/event_universe (engine-5.0-test af06713db), written by this script and never by hand, under
tools/derivations/open_items/H-Masses-From-The-Clicks-2/src_ms2/event_universe. Two flags, both keys of one universe-file key "ms2" (refused by the engine's loader,
so no file of David's can carry it); the key absent, every path bit for bit the engine's (the state hash compared by ms2_hash.py).
  "circle": 1  the plane rows with a gap are READ FROM den ALONE: every point (num, s) of den's circle, num^2 + s^2 = den^2, num > 0,
               s > 0, appended as a shape-2 row in the order of the leg s (the lightest first); the file names no gapped pair (MS-S2).
  "charge": 1  a born child is laid at the Wronskian T div 2 for every row: re_now = A, im_before = +-B with A B = T div 2, A the
               largest divisor of T div 2 at most largest_below(T div 2) (a search by comparisons, no number), and the walls booked
               at the take are the share the two children's lays add to their plane on the board (the exact take's letter: what the
               lay costs is taken, nothing made) (MS-S1's mending form).
Every replacement must match the engine's text exactly once, else the script refuses."""
import os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, "..", "..", "..", "src", "event_universe"))
DST = os.path.join(HERE, "src_ms2", "event_universe")

if os.path.exists(os.path.join(HERE, "src_ms2")):
    shutil.rmtree(os.path.join(HERE, "src_ms2"))
shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns("__pycache__"))

R = {}  # file -> list of (old, new)

R["loader/world.py"] = [(
    'UNIVERSE_KEYS = frozenset({"integers", "rows"})',
    'UNIVERSE_KEYS = frozenset({"integers", "rows", "ms2"})  # ms2: the hand\'s flag key, absent in every file of David\'s',
)]

R["rows.py"] = [
(
    '''    rows = sorted(by_index, key=order_of)
    walled = [r for r in rows if r.wall is not None]''',
    '''    flag = universe.get("ms2", {})  # ms2: absent, the default bit for bit
    if flag.get("circle"):
        for num, s in circle_points(den):
            pair = (num, den)
            lines = lines_of(board, PLANE, pair, None, w, write_walls(PLANE, pair, den, gamma, action))
            by_index.append(Row(PLANE, pair, None, lines))
    rows = sorted(by_index, key=order_of)
    walled = [r for r in rows if r.wall is not None]''',
),
(
    '''def row_of(rows: list[Row], shape: int, gap: int | None = None) -> Row:''',
    '''def circle_points(den: int) -> list[tuple[int, int]]:
    """ms2 (MS-S2): every point (num, s) of den's circle, num^2 + s^2 = den^2, num > 0, s > 0, found by the division act alone
    (den's primes by trial division, each prime 1 mod 4 as a^2 + b^2 by a search by comparisons, the points the Gaussian products),
    in the order of the leg s; 3^k - 1 points for k distinct primes 1 mod 4 and none where den has no such prime."""
    from event_universe.core.rule3 import largest_below

    n, primes, d = den, [], 2
    while d * d <= n:
        while n % d == 0:
            primes.append(d)
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        primes.append(n)
    pts, scale = {(1, 0)}, 1
    for p in sorted(set(primes)):
        e = primes.count(p)
        if p % 4 != 1:
            scale *= p**e
            continue
        a = 1
        while True:
            b = largest_below(p - a * a)
            if a * a + b * b == p:
                break
            a += 1
        new = set()
        for x, y in pts:
            for j in range(2 * e + 1):
                zx, zy = 1, 0
                for _ in range(j):
                    zx, zy = zx * a - zy * b, zx * b + zy * a
                for _ in range(2 * e - j):
                    zx, zy = zx * a + zy * b, zy * a - zx * b
                new.add((x * zx - y * zy, x * zy + y * zx))
        pts = new
    found = set()
    for x, y in pts:
        for u, v in ((x, y), (y, x), (-x, y), (y, -x), (x, -y), (-y, x), (-x, -y), (-y, -x)):
            if u > 0 and v > 0:
                found.add((u * scale, v * scale))
    return sorted(found, key=lambda p: p[1])


def row_of(rows: list[Row], shape: int, gap: int | None = None) -> Row:''',
),
]

R["node.py"] = [
(
    '''        self.T, self.G = int(ints["quantum_action"]), link_unit_of(self.gamma)''',
    '''        self.T, self.G = int(ints["quantum_action"]), link_unit_of(self.gamma)
        self.ms2 = universe.get("ms2", {})  # ms2: the flags; absent, the default bit for bit''',
),
(
    '''    def lay(self, rec: int, where: Any, levels: tuple[Any, Any, Any, Any], sign: int = 1) -> None:''',
    '''    def im_amplitude(self, amplitude: int) -> int:
        """ms2 (MS-S1): the im level of a child's lay: the re amplitude itself (the engine's quarter turn) with the flag off; with the
        flag "charge" the cofactor B = (T div 2) div A, so W = A B = T div 2 exactly for every row."""
        if not self.ms2.get("charge"):
            return amplitude
        return int(rule3.quotient(half(self.T), amplitude))

    def charge_amplitude(self) -> int:
        """ms2 (MS-S1): A, the largest divisor of T div 2 at most largest_below(T div 2), by a search by comparisons."""
        target = half(self.T)
        a = rule3.largest_below(target)
        while rule3.remainder(target, a):
            a -= 1
        return int(a)

    def lay_cost(self, rec: int, minus: tuple[int, ...], plus: tuple[int, ...], amplitude: int, c: Any, factors: tuple[Any, ...], pace: Any) -> int:
        """ms2 (MS-S1): the share the two children's lays add to their plane on the board at the frame's weight (the lay made, read, taken back)."""
        row = self.records()[rec]
        rr = self.rule_of(row, c, factors)
        re, im = row.lines

        def total() -> int:
            return int(sum(int(x) for x in (self.share(re, rr, pace) + self.share(im, rr, pace)).reshape(-1)))

        before = total()
        b = self.im_amplitude(amplitude)
        for where, sense in ((minus, -1), (plus, 1)):
            take.lay(self, rec, where, (amplitude, 0, 0, sense * b))
        after = total()
        for where, sense in ((minus, -1), (plus, 1)):
            take.lay(self, rec, where, (amplitude, 0, 0, sense * b), -1)
        return max(after - before, 1)

    def lay(self, rec: int, where: Any, levels: tuple[Any, Any, Any, Any], sign: int = 1) -> None:''',
),
]

R["close.py"] = [
(
    '''    taken = []
    for at in sorted(by_node):
        walls = sum(2 * node.units[s] for s, _m, _p, _r in by_node[at])
        got = take_at(node, at, walls, r_gap0, len(by_node[at]))''',
    '''    taken = []
    for at in sorted(by_node):
        walls = sum(2 * node.units[s] for s, _m, _p, _r in by_node[at])
        if node.ms2.get("charge"):  # ms2 (MS-S1): the walls the lays cost, read before the take
            a_ch = node.charge_amplitude()
            walls = sum(node.lay_cost(s, m, p, a_ch, c, factors, pace) for s, m, p, _r in by_node[at])
        got = take_at(node, at, walls, r_gap0, len(by_node[at]))''',
),
(
    '''        for a, d in enumerate(
            momentum_of(node, im.now, im.before, where, d_before=sense * amplitude, num=row.pair[0])
        ):
            dp_lay[a] += d
        lay(node, s, where, (amplitude, 0, 0, sense * amplitude))''',
    '''        for a, d in enumerate(
            momentum_of(node, im.now, im.before, where, d_before=sense * node.im_amplitude(amplitude), num=row.pair[0])
        ):
            dp_lay[a] += d
        lay(node, s, where, (amplitude, 0, 0, sense * node.im_amplitude(amplitude)))''',
),
(
    '''    for s, minus, plus, room in kids:
        amplitude = lay_amplitude(node, s, at, c, factors, pace)
        dp_lay, w_children = child_laid(node, s, minus, plus, amplitude)''',
    '''    for s, minus, plus, room in kids:
        amplitude = lay_amplitude(node, s, at, c, factors, pace)
        if node.ms2.get("charge"):  # ms2 (MS-S1): the amplitude from the charge, the same for every row
            amplitude = node.charge_amplitude()
        dp_lay, w_children = child_laid(node, s, minus, plus, amplitude)''',
),
(
    '''            lay(node, s, tuple(entry["minus"]), (amplitude, 0, 0, -amplitude), -1)
            lay(node, s, tuple(entry["plus"]), (amplitude, 0, 0, amplitude), -1)''',
    '''            lay(node, s, tuple(entry["minus"]), (amplitude, 0, 0, -node.im_amplitude(amplitude)), -1)
            lay(node, s, tuple(entry["plus"]), (amplitude, 0, 0, node.im_amplitude(amplitude)), -1)''',
),
]

R["decoder.py"] = [(
'        rows = run["universe"]["rows"]\n        planes = [\n            tuple(int(x) for x in r["pair"]) for r in rows if int(r["shape"]) == PLANE and r.get("pair")\n        ]',
'        planes = [(int(n), self.den) for n in run["planes"]]  # ms2: the decoder\'s names from the record\'s planes, not the file\'s rows',
)]

for name, pairs in R.items():
    path = os.path.join(DST, name)
    text = open(path, encoding="utf-8").read()
    for old, new in pairs:
        if text.count(old) != 1:
            print("REFUSED:", name, "matches", text.count(old), "for", old[:60].replace("\n", " "))
            sys.exit(1)
        text = text.replace(old, new)
    open(path, "w", encoding="utf-8").write(text)
    print("written", name, len(pairs), "replacements")
print("copy at", DST)
