"""Rule B's runner on one board of Node-clocks: several pairs at once and a two-step loop, in exact integers.

usage: python3 -I bpasses.py (about 2 seconds; the standard library alone)

Each Node-clock on a line is doubled: a forward half (the past arriving: what was born rides out, records are
written) and a backward half (the future arriving: the settings ride back; it writes nothing). Each half has four
lanes: L (moving left), H (at rest), R (moving right), D (a detector's hold). A step is one gather per lane from a
fixed neighbour index array, and FAR counts every read farther than one site. Whole numbers; Fractions only to print
and compare laws. It stands beside the engine and imports or changes none of it. In decision 34's words the two
halves are one hand's two directions: the backward half carries the settings back as a tag, and no hand.
"""

from collections import Counter
from fractions import Fraction as F
from itertools import accumulate, product

LANES = {"L": -1, "H": 0, "R": 1, "D": 0}  # each lane's motion per tick
SIGNS = (1, -1)
RULE = {1: 0, -1: 1}  # a machine sets X (0) where the outcome it heard is +, Y (1) where it is -
GHZ_TURNS = (8, 4, 2)  # the turns of a part-by-part draw's three digits (its rows' sums)
CAUSE, REVERSED = (0, 1, 2), (2, 1, 0)
FAR, READS = [0], [0]
FA, FB = {0: (1, 0), 1: (1, 1)}, {0: (5, 2), 1: (5, -2)}  # a = 1, a' = 1 + i; b = 5 + 2i, b' = 5 - 2i
# three pairs: the birth (site, tick), A's detector (site, lateness), B's detector (site, lateness)
PAIRS = (((9, 0), (4, 2), (15, 0)), ((17, 3), (12, 0), (24, 3)), ((26, 1), (19, 4), (31, 1)))
GHZ_AT = {
    "A": (1, 1),
    "B": (6, 12),
    "C": (15, 13),
}  # each detector's (site, lateness); the birth at site 6, tick 0


def gather(reg, idx):
    """Every Node-clock i reads reg[idx[i]], one read; each read farther than one site is counted."""
    for i, j in enumerate(idx):
        FAR[0] += abs(i - j) > 1
    READS[0] += len(idx)
    return [reg[j] for j in idx]


def drawn(n, sizes):
    """The rank count: d = n mod L, the part is the number of cumulative sizes at or below d."""
    d = n % sum(sizes)
    return sum(run <= d for run in accumulate(sizes[:-1]))


def bell(sx):
    """A pair's joint sizes over ++, +-, -+, --: the squared overlap of a_s x b_t with psi = e1 x e2 - e2 x e1."""
    a, b = (
        {1: u, -1: (-u[1], u[0])} for u in (FA[sx[0]], FB[sx[1]])
    )  # u = x + iy: + along (x, y), - along (-y, x)
    return [(a[s][0] * b[t][1] - a[s][1] * b[t][0]) ** 2 for s, t in product(SIGNS, SIGNS)]


def ghz(sx):
    """GHZ's joint sizes over the eight outcomes: 1 + E sA sB sC, E = +1 at XXX, -1 at XYY, at YXY and at YYX, else 0."""
    e = {0: 1, 2: -1}.get(sum(sx), 0)
    return [1 + e * a * b * c for a, b, c in product(SIGNS, repeat=3)]


def board(n, births, dets):
    """births: (site, tick, parties, sizes); dets: party -> (site, lateness, digit, heard-from, tells, claim)."""
    lay = {"n": n, "births": [], "det": {}}
    for site, tick, parties, sizes in births:
        lanes = {p: "L" if dets[p][0] < site else "R" if dets[p][0] > site else "H" for p in parties}
        lay["births"].append(
            {"site": site, "tick": tick, "lanes": lanes, "sizes": sizes, "got": {}, "parts": {}}
        )
        for p in parties:
            s, late, digit, src, to, claim = dets[p]
            lay["det"][p] = dict(
                site=s,
                late=late,
                digit=digit,
                src=src,
                to=to,
                set=claim,
                lane=lanes[p],
                click=tick + abs(s - site) + late,
                **dict.fromkeys(("arr", "out", "act", "used", "light", "heard")),
            )
    for d in lay["det"].values():  # the way its light leaves toward the detector it tells: its wiring
        d["way"] = d["to"] and ("R" if lay["det"][d["to"]]["site"] > d["site"] else "L")
    lay["span"] = (min(b["tick"] for b in lay["births"]), max(d["click"] for d in lay["det"].values()))
    return lay


def put(regs, lane, i, item):
    assert regs[lane][i] is None, f"collision on lane {lane} at site {i}"
    regs[lane][i] = item


def sweep(lay, back):
    """One pass over the span: each step one gather per lane, then each Node-clock's own events at that tick."""
    n, (t0, t1) = lay["n"], lay["span"]
    idx = {
        ln: [min(max(i + (s if back else -s), 0), n - 1) for i in range(n)] for ln, s in LANES.items()
    }
    regs = {ln: [None] * n for ln in LANES}
    for d in lay["det"].values() if not back else ():
        d["arr"] = d["light"] = None
    ticks = range(t1, t0 - 1, -1) if back else range(t0, t1 + 1)
    for k, t in enumerate(ticks):
        if k:
            regs = {ln: gather(regs[ln], idx[ln]) for ln in LANES}
        (backward if back else forward)(lay, regs, t)
    return len(ticks) - 1


def forward(lay, regs, t):
    """Births send twins out (with part and setting once drawn); detectors take in their twin and light, then click."""
    for b in lay["births"]:
        for p, ln in b["lanes"].items() if b["tick"] == t else ():
            put(regs, ln, b["site"], ("twin", p, b["parts"].get(p), b["got"].get(p)))
    for p, d in lay["det"].items():
        i = d["site"]
        for ln in "LHR":
            it = regs[ln][i]
            if it and it[1] == p and it[0] == "light":
                regs[ln][i], d["light"], d["heard"] = None, it[2], t
            elif it and it[1] == p:
                regs[ln][i], d["arr"] = None, t
                put(regs, "D", i, it)
        if d["arr"] is not None and t == d["arr"] + d["late"]:
            (_, _, d["out"], d["used"]), regs["D"][i] = regs["D"][i], None
            d["act"] = d["digit"] % 2 if d["src"] is None else RULE.get(d["light"])
            d["set"] = d["act"] if d["set"] is None else d["set"]
            if d["way"] and d["out"] is not None:  # the outcome sent on by light
                put(regs, d["way"], i, ("light", d["to"], d["out"]))


def backward(lay, regs, t):
    """A setting enters at its click, is held back to its twin's arrival, rides back along the twin's lane to birth."""
    for p, d in lay["det"].items():
        i = d["site"]
        if t == d["arr"] + d["late"] and d["set"] is not None:
            put(regs, "D", i, ("set", p, d["set"]))
        if t == d["arr"] and regs["D"][i]:
            it, regs["D"][i] = regs["D"][i], None
            put(regs, d["lane"], i, it)
    for b in lay["births"]:
        for p, ln in b["lanes"].items() if b["tick"] == t else ():
            it = regs[ln][b["site"]]
            if it and it[:2] == ("set", p):
                regs[ln][b["site"]], b["got"][p] = None, it[2]


def draw(b, order, digits):
    """The birth's draw. order None: one joint draw, a full turn of its digit at once (each part a tuple). Else part
    by part in `order`, from its row given the parts drawn, once those settings arrived; asserted not to move else."""
    ps = list(b["lanes"])
    got, outs = [b["got"].get(p) for p in ps], list(product(SIGNS, repeat=len(ps)))
    if order is None:
        if None not in got and not b["parts"]:
            sizes = b["sizes"](got)
            parts = [drawn(n, sizes) for n in range(sum(sizes))]
            assert [
                parts.count(j) for j in range(len(sizes))
            ] == sizes  # each part exactly its size times
            b["parts"].update({p: tuple(outs[q][j] for q in parts) for j, p in enumerate(ps)})
        return
    done = {j: b["parts"][p] for j, p in enumerate(ps) if p in b["parts"]}
    while len(done) < len(ps) and None not in [got[j] for j in order[: len(done) + 1]]:
        j, rows = order[len(done)], set()
        for fill in product((0, 1), repeat=len(ps)):
            sizes = b["sizes"]([g if g is not None else f for g, f in zip(got, fill, strict=True)])
            keep = [
                (o, z)
                for o, z in zip(outs, sizes, strict=True)
                if all(o[q] == v for q, v in done.items())
            ]
            rows.add(tuple(sum(z for o, z in keep if o[j] == s) for s in SIGNS))
        assert len(rows) == 1, "the row moves with a setting not yet carried back"
        row = list(rows.pop())
        assert sum(row) == GHZ_TURNS[len(done)]
        done[j] = b["parts"][ps[j]] = SIGNS[drawn(digits[len(done)], row)]


def run(lay, order=None, digits=None):
    """The runner: forward; then backward, the births' draws, forward again; until every detector has recorded."""
    passes, steps, seen = 0, 0, None
    while True:
        steps, passes = steps + sweep(lay, False), passes + 1
        if all(d["out"] is not None for d in lay["det"].values()):
            return passes, steps
        steps, passes = steps + sweep(lay, True), passes + 1
        for b in lay["births"]:
            draw(b, order, digits)
        now = [d["set"] for d in lay["det"].values()] + [len(b["parts"]) for b in lay["births"]]
        if now == seen:
            return passes, None  # stuck: no new setting chosen and no new part drawn
        seen = now


def pair_board(xs, only=None):
    """The pairs on one board of 36 Node-clocks; xs holds the six detectors' digits; only: one pair alone."""
    births, dets = [], {}
    for q, ((b, tb), (sa, la), (sb, lb)) in enumerate(PAIRS):
        if only in (None, q):
            births.append((b, tb, [f"A{q}", f"B{q}"], bell))
            dets[f"A{q}"], dets[f"B{q}"] = (
                (sa, la, xs[2 * q], *[None] * 3),
                (sb, lb, xs[2 * q + 1], *[None] * 3),
            )
    return board(36, births, dets)


def shortcut(xs):
    """Deliberately broken: after pass 1, each A detector reads its partner's setting straight from B's site and draws
    the pair there; each B detector reads its part straight from A's site. Two reads across the board per pair."""
    lay = pair_board(xs)
    sweep(lay, False)
    n, outs = lay["n"], list(product(SIGNS, SIGNS))
    for q in range(3):
        a, b = lay["det"][f"A{q}"], lay["det"][f"B{q}"]
        idx, there = list(range(n)), [None] * n
        idx[a["site"]], there[b["site"]] = b["site"], b["set"]
        sizes = bell((a["set"], gather(there, idx)[a["site"]]))
        parts = [outs[drawn(m, sizes)] for m in range(sum(sizes))]
        idx, there = list(range(n)), [None] * n
        idx[b["site"]], there[a["site"]] = a["site"], tuple(o[1] for o in parts)
        a["out"], b["out"] = tuple(o[0] for o in parts), gather(there, idx)[b["site"]]
    return lay


def bell_report(laws):
    """S, the four E's and both marginals of one pair, from its law at each of its four setting pairs."""
    tot = {k: sum(v.values()) for k, v in laws.items()}
    e = {k: F(sum(s * t * c for (s, t), c in v.items()), tot[k]) for k, v in laws.items()}
    ma, mb = (
        {k: F(sum(c for o, c in v.items() if o[j] == 1), tot[k]) for k, v in laws.items()}
        for j in (0, 1)
    )
    return e[0, 0] + e[0, 1] + e[1, 0] - e[1, 1], e, ma, mb


def part_pairs():
    def joint(lay, q):  # a pair's law: the count of each joint part recorded at its two detectors
        return Counter(zip(lay["det"][f"A{q}"]["out"], lay["det"][f"B{q}"]["out"], strict=True))

    laws, shapes, agree, keys = {}, Counter(), 0, list(product((0, 1), repeat=2))
    FAR[0] = READS[0] = 0
    for xs in product(
        (0, 1), repeat=6
    ):  # a full turn of every detector's digit; each birth's digit turns inside
        lay = pair_board(xs)
        shapes[run(lay)] += 1
        agree += all(d["act"] == d["used"] for d in lay["det"].values())
        for q in range(3):
            laws.setdefault((q,) + xs[2 * q : 2 * q + 2], []).append(joint(lay, q))
    print(
        f"  64 runs (each detector's digit over its turn; each birth's digit over its full turn inside a run);"
        f" (passes, steps) per run: {dict(shapes)}\n  reads {READS[0]}, reads farther than one site: {FAR[0]};"
        f" runs where every setting read at a click equals the one the birth drew with: {agree} of 64"
    )
    for q, ((b, tb), (sa, la), (sb, lb)) in enumerate(PAIRS):
        first = {k: laws[(q,) + k][0] for k in keys}
        s, e, ma, mb = bell_report(first)
        same = all(v == first[k] for k in keys for v in laws[(q,) + k])
        lone = all(
            joint(lay, q) == first[k]
            for k in keys  # the pair alone on the board, at its settings k
            for lay in [pair_board([0] * (2 * q) + list(k) + [0] * (4 - 2 * q), only=q)]
            if run(lay)
        )
        moves = any(ma[x, 0] != ma[x, 1] or mb[0, x] != mb[1, x] for x in (0, 1))

        def show(m):
            return ", ".join(str(m[k]) for k in keys)

        print(
            f"  pair {q}: born at site {b}, tick {tb}; A at {sa} clicks at tick {tb + abs(b - sa) + la}, B at {sb}"
            f" at {tb + abs(sb - b) + lb}; birth turns {show({k: sum(first[k].values()) for k in keys})}\n"
            f"    S = {s}, S^2 = {s * s} (4 < S^2: {4 < s * s}, S^2 < 8: {s * s < 8}); E at 00, 01, 10, 11:"
            f" {show(e)}\n"
            f"    A's marginal at 00, 01, 10, 11: {show(ma)}; B's: {show(mb)}; one moves with the other's setting:"
            f" {moves}\n    its law is the same under all 16 settings of the other pairs: {same}; alone: {lone}\n"
            f"    carries back and forward: A's {abs(b - sa) + la} steps each ({abs(b - sa)} sites, {la} held), B's"
            f" {abs(sb - b) + lb} ({abs(sb - b)} sites, {lb} held)"
        )
    FAR[0], broken = 0, {}
    for xs in product((0, 1), repeat=6):
        lay = shortcut(xs)
        for q in range(3):
            broken.setdefault(q, {})[xs[2 * q : 2 * q + 2]] = joint(lay, q)
    print(
        f"  the broken runner (A reads B's setting at B's site and draws there, B reads its part at A's site):"
        f" S = {', '.join(str(bell_report(broken[q])[0]) for q in range(3))}; reads farther than one site:"
        f" {FAR[0]} (2 per pair per run)"
    )


def ghz_board(xs, loop, claims=(None, None, None)):
    """One birth of three twins on 17 Node-clocks: A's to the left, B's at rest, C's to the right. In the loop, B's
    setting is chosen by A's outcome, heard by light, and C's by B's; else each setting is its own detector's digit."""
    src, to = (None, "A", "B"), ("B", "C", None)
    dets = {
        p: GHZ_AT[p] + (xs[j], src[j] if loop else None, to[j] if loop else None, claims[j])
        for j, p in enumerate("ABC")
    }
    return board(17, [(6, 0, ["A", "B", "C"], ghz)], dets)


def part_ghz():
    free, shapes, triples = {}, Counter(), list(product((0, 1), repeat=3))
    FAR[0] = 0
    digits = list(
        product(*(range(t) for t in GHZ_TURNS))
    )  # the birth's three digits, each over its full turn
    for order, xs, digs in product((CAUSE, REVERSED), triples, digits):
        lay = ghz_board(xs, False)
        shapes[run(lay, order, digs)] += 1
        free.setdefault((order, xs), Counter())[tuple(lay["det"][p]["out"] for p in "ABC")] += 1
    one = {
        F(sum(c for o, c in free[CAUSE, xs].items() if o[j] == 1), 64)
        for xs in triples
        for j in range(3)
    }
    two = {}  # each two-party marginal, by the third party's setting
    for (j, k), xs, sj, sk in product(((0, 1), (0, 2), (1, 2)), triples, SIGNS, SIGNS):
        c = sum(c for o, c in free[CAUSE, xs].items() if (o[j], o[k]) == (sj, sk))
        two.setdefault((j, k, xs[j], xs[k], sj, sk), set()).add(c)
    mermin = "; ".join(
        f"{''.join('XY'[s] for s in xs)} -> {sorted({o[0] * o[1] * o[2] for o in free[CAUSE, xs]})}"
        for xs in triples
        if sum(xs) in (0, 2)
    )
    print(
        f"  free settings, 8 settings x 64 digits in each order; (passes, steps) per run: {dict(shapes)}\n"
        f"    one-party marginals at every setting triple: {', '.join(map(str, sorted(one)))}; two-party marginals"
        f" that move with the third party's setting: {sum(len(v) > 1 for v in two.values())} of {len(two)}\n"
        f"    Mermin's products: {mermin}; the two orders give one joint law at every setting:"
        f" {all(free[CAUSE, x] == free[REVERSED, x] for x in triples)}"
    )
    hist, kept = {o: Counter() for o in (CAUSE, REVERSED)}, {o: Counter() for o in (CAUSE, REVERSED)}
    shapes, built, match = Counter(), Counter(), 0
    for xa, digs, order in product((0, 1), digits, (CAUSE, REVERSED)):
        good = []
        for cand in product(
            (0, 1), repeat=2
        ):  # the settings B and C carry back, checked at their clicks
            lay = ghz_board((xa, 0, 0), True, (None,) + cand)
            shapes[run(lay, order, digs)] += 1
            if all(
                d["act"] == d["used"] for d in lay["det"].values()
            ):  # each detector's own check at its click
                good.append((xa,) + cand + tuple(lay["det"][p]["out"] for p in "ABC"))
        hist[order][len(good)] += 1
        kept[order].update(good)
        if order == CAUSE:  # the runner building the history pass by pass, with no candidates
            lay = ghz_board((xa, 0, 0), True)
            built[run(lay, CAUSE, digs)] += 1
            match += [(xa, lay["det"]["B"]["set"], lay["det"]["C"]["set"])] == [g[:3] for g in good]
    ticks = {p: (d["click"], d["heard"]) for p, d in lay["det"].items()}
    lay = ghz_board((0, 0, 0), True)
    stuck = run(lay, REVERSED, digits[0]) + (len(lay["births"][0]["parts"]),)
    marg = ", ".join(
        f"{'ABC'[j]}'s {F(sum(c for g, c in kept[CAUSE].items() if g[0] == xa and g[3 + j] == 1), 64)}"
        for j in range(3)
        for xa in (0, 1)
    )
    print(
        f"  the loop: B's setting from A's outcome by light, C's from B's; (click, light heard) ticks {ticks}\n"
        f"    2 x 64 digits (A's, the birth's three), 4 candidate settings carried back at each; (passes, steps) per"
        f" run: {dict(shapes)}\n    digits by the number of histories agreeing at both ends: cause's order (A from"
        f" its marginal, B from its row given A, C last) {dict(hist[CAUSE])}; reversed order (C, then B given C, A"
        f" last) {dict(sorted(hist[REVERSED].items()))}\n    histories over all digits: {sum(kept[CAUSE].values())}"
        f" and {sum(kept[REVERSED].values())}; the same multiset of (settings, parts) in both orders:"
        f" {kept[CAUSE] == kept[REVERSED]}\n    the runner building it in the cause's order: (passes, steps)"
        f" {dict(built)}; it finds the one history at {match} of 128 digits; in the reversed order it stops at"
        f" (passes, steps, parts drawn) {stuck}\n    marginals over the histories, at A's setting X then Y: {marg}\n"
        f"  reads farther than one site in all the GHZ runs: {FAR[0]}"
    )


if __name__ == "__main__":
    print("Rule B's three passes on one board of Node-clocks, in exact integers\n")
    print("1-2. Three pairs at once (frames a = 1, a' = 1 + i; b = 5 + 2i, b' = 5 - 2i)")
    part_pairs()
    print("\n3. GHZ on one birth: free settings, and a loop of two steps")
    part_ghz()
