"""DECODE3's test: the decoder's rules for the three clicks, read on Big Pic's stage 1 records (origin/bigpic-3clicks
cf4126ff5, edgeclick.py run on node-live 1794d474b's src exported into split/nl/, its records in st1run/). A stage 1
record holds click lines (round, site, train, q) and sides (round, site, edge, c): one c per edge, booked +c to the
edge's first clock and -c to its second. It holds no tooth and no passing, and it does not name an edge's clocks; the
rules read only the record. Whole numbers; every division is Rule3's carry (tensor24.algebra.carry.carry); no float.
argv: the output name."""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.joinpath("nl", "src")))
from tensor24.algebra.carry import carry  # noqa: E402

out = []
say = out.append
RUN = HERE.joinpath("st1run")


def th(num, den):
    return carry(1000 * num, den, 0)[0] if den else 0


def load(name):
    rec = json.loads(RUN.joinpath(name).read_text(encoding="utf-8"))
    return [tuple(x) for x in rec["lines"]], [tuple(x) for x in rec["sides"]], rec["digest"]


def ends(lines, sides):
    """Each edge's two clocks, read from the places where it carried alone: the clock whose line is +c, and the one
    whose line is -c; an edge with no such place is left unread."""
    by_place = {}
    for t, x, e, c in sides:
        by_place.setdefault((t, x), []).append((e, c))
    line_at = {}
    for t, x, tr, v in lines:
        line_at.setdefault((t, x), {})[tr] = v
    found = {}
    for place, ss in by_place.items():
        if len(ss) != 1:
            continue
        e, c = ss[0]
        got = line_at.get(place, {})
        plus = sorted(tr for tr, v in got.items() if v == c)
        minus = sorted(tr for tr, v in got.items() if v == -c)
        if len(got) == 2 and len(plus) == 1 and len(minus) == 1:
            found.setdefault(e, set()).add((plus[0], minus[0]))
    named = {e: sorted(p)[0] for e, p in found.items() if len(p) == 1}
    # the structure's rule where an edge never carried alone: at a site whose lines name three clocks and whose sides
    # name three edges, two of them read, the third edge joins the pair the two read edges leave unjoined
    clocks = sorted({tr for _, _, tr, _ in lines})
    edges = sorted({e for _, _, e, _ in sides})
    left = [e for e in edges if e not in named]
    if len(left) == 1:
        joined = {tuple(sorted(p)) for p in named.values()}
        meet = sorted({c for p in named.values() for c in p})
        rest = [(a, b) for i, a in enumerate(meet) for b in meet[i + 1:] if (a, b) not in joined]
        if len(rest) == 1:
            named[left[0]] = rest[0]
    return named, {e: len(p) for e, p in found.items()}


def structure(sides, pair):
    """Per site, the clocks met through the edges that carried there; a site where three clocks are pairwise joined is
    a triangle."""
    seen = {}
    for _, x, e, _ in sides:
        seen.setdefault(x, set()).add(e)
    kinds = {}
    for x, es in seen.items():
        clocks = sorted({c for e in es if e in pair for c in pair[e]})
        kinds.setdefault((len(clocks), len(es)), []).append(x)
    return seen, kinds


def books(lines, sides, pair):
    """(1) every place's lines sum to 0; every line's q is the sum of its sides, +c at the edge's first clock, -c at
    its second."""
    by_place = {}
    for t, x, tr, v in lines:
        by_place.setdefault((t, x), {})[tr] = v
    sides_at = {}
    for t, x, e, c in sides:
        sides_at.setdefault((t, x), []).append((e, c))
    open_, wrong, unread = 0, 0, 0
    for place in set(by_place) | set(sides_at):
        got = by_place.get(place, {})
        open_ += int(sum(got.values()) != 0)
        want = {}
        for e, c in sides_at.get(place, []):
            if e not in pair:
                unread += 1
                continue
            p, m = pair[e]
            want[p] = want.get(p, 0) + c
            want[m] = want.get(m, 0) - c
        want = {k: v for k, v in want.items() if v}
        wrong += int(want != got)
    return len(set(by_place) | set(sides_at)), open_, wrong, unread


def windows(sides, e, x, rounds, w):
    counts = [0] * (rounds // w)
    for t, xx, ee, c in sides:
        if ee == e and xx == x and t < (rounds // w) * w:
            q, _ = carry(t, w, 0)
            counts[q] += c
    return counts


def draw_noise(first, third, pair, sites, rounds, w):
    """The third click's draw against the first's, from the two records of one lay: the board runs alike in both (the
    click pushes nothing into the gears), so the first record's quanta per window are the passing's, and the
    difference is the turn's. Per edge: var(difference) over the mean quanta passed, and the two giver edges'
    co-movement (r^2 with its sign)."""
    res = {}
    for e in sorted(pair):
        diffs, mass = [], 0
        for x in range(sites):
            a = windows(first, e, x, rounds, w)
            b = windows(third, e, x, rounds, w)
            diffs += [q - p for p, q in zip(a, b)]
            mass += sum(abs(p) for p in a)
        n, s1, s2 = len(diffs), sum(diffs), sum(d * d for d in diffs)
        var_n2 = n * s2 - s1 * s1
        res[e] = (diffs, th(var_n2, n * mass), n)
    return res


def corr(xs, ys):
    n, sx, sy = len(xs), sum(xs), sum(ys)
    vx = n * sum(a * a for a in xs) - sx * sx
    vy = n * sum(b * b for b in ys) - sy * sy
    cv = n * sum(a * b for a, b in zip(xs, ys)) - sx * sy
    sign = "+" if cv > 0 else ("-" if cv < 0 else "0")
    return sign, th(cv * cv, vx * vy) if vx * vy else 0


def lives(sides, e, sites):
    gaps = []
    for x in range(sites):
        ts = sorted(t for t, xx, ee, c in sides if ee == e and xx == x and c != 0)
        gaps += [b - a for a, b in zip(ts, ts[1:])]
    n, s1, s2 = len(gaps), sum(gaps), sum(g * g for g in gaps)
    return n, th(s1, n), th(n * s2 - s1 * s1, s1 * s1)


first_l, first_s, first_d = load("edge_tensor24-click_200_0.json")
third_l, third_s, third_d = load("edge_tensor24-click_200_1.json")
swf_l, swf_s, swf_d = load("edge_tensor24-clickswap_200_0.json")
swt_l, swt_s, swt_d = load("edge_tensor24-clickswap_200_1.json")
SITES, ROUNDS = 27, 200
BP = {"first": "1d221a1be329f42a3df07eb1a235aa671e5f2bad7228bc60c6926dc4285dd47c",
      "third": "59d3a811329522ce1cde9dc4750a6fee6d98fd8f3fc6f2fcaa4225908edca18e"}
say(f"R1, one lay run twice, one record: this run's digests against Big Pic's stage 1 (edge_click_first.txt,"
    f" edge_click_third.txt): first {first_d == BP['first']}, third {third_d == BP['third']}")

for name, lines, sides in (("first", first_l, first_s), ("third", third_l, third_s)):
    pair, counts = ends(lines, sides)
    seen, kinds = structure(sides, pair)
    say(f"({name}) the edges' clocks read from the places where one edge carried alone: {pair} (each read one way"
        f" at {counts} such pairs)")
    say(f"    the sites by (clocks met, edges carried): {[(k, len(v)) for k, v in sorted(kinds.items())]}")
    n, open_, wrong, unread = books(lines, sides, pair)
    say(f"    (1) the books: {n} places; a place's lines not summing to 0: {open_}; a line's q not its sides' sum: {wrong};"
        f" sides on an unread edge: {unread}")

pair, _ = ends(first_l, first_s)
for w in (5, 10, 20, 40):
    res = draw_noise(first_s, third_s, pair, SITES, ROUNDS, w)
    fano = {pair[e]: res[e][1] for e in res}
    giver_edges = [e for e in sorted(pair) if 2 in pair[e]]
    sign, r2 = corr(res[giver_edges[0]][0], res[giver_edges[1]][0]) if len(giver_edges) == 2 else ("0", 0)
    say(f"(3) windows of {w} rounds ({res[min(res)][2]} per edge): the third click's quanta less the first's, var over the"
        f" quanta passed, per edge {fano} thousandths (independent landings about 1,000, a carried form 0); the held"
        f" clock's two edges' differences: cov {sign}, r^2 {r2} thousandths")
for name, sides in (("first", first_s), ("third", third_s)):
    say(f"(3) lives, {name}: per edge (gaps, mean gap in thousandths of a round, var over mean^2 in thousandths; the"
        f" exponential law about 1,000): {[(pair[e], lives(sides, e, SITES)) for e in sorted(pair)]}")

# the swap: trains 3 and 4 exchanged in the files; the edges (2, 3) and (2, 4) exchange and (3, 4) reverses
SW = {3: 4, 4: 3}
spair, _ = ends(swf_l, swf_s)
say(f"(3) the swapped files' edges, read from their own record: {spair}")
for name, a_l, b_l in (("first", first_l, swf_l), ("third", third_l, swt_l)):
    mapped = sorted((t, x, SW.get(tr, tr), v) for t, x, tr, v in b_l)
    orig = sorted(a_l)
    same = len(set(mapped) & set(orig))
    diff_rounds = sorted({t for t, x, tr, v in set(mapped) ^ set(orig)})
    say(f"    {name}: the swapped record relabelled back equals the original at {same} of {len(orig)} lines"
        f" ({len(mapped)} in the swapped); first round apart {diff_rounds[0] if diff_rounds else None}; rounds apart"
        f" {len(diff_rounds)}")

HERE.joinpath(sys.argv[1] if len(sys.argv) > 1 else "decode3.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
