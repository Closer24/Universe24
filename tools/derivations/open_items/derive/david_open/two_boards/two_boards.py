"""Two boards on one Node-clock, shown in exact integers: the split click drawn by the product of two dials' sizes.

David's probe for the owner's words to David of 2026-10-29, 07:46 UTC ("The subtle point is the solution... the only
aim is complex clocks that create interesting clicks") and 08:28 UTC ("Show it"), on the Boss's section 10.1 of
TENSOR24-THE-BIG-PICTURE.md (two boards on one Node-clock, one forward and one backward).

usage: python3 -I two_boards.py

The forward board carries the past (the birth, the twins) and alone writes records; the backward board carries the
clicks to come back along the same worldlines; a split is drawn where the two dials meet, by the product of their
sizes. Every carry moves one Mesh a step along a twin's own worldline, so no step reads past the six neighbours.
Whole numbers throughout; fractions only to print.

  1. the product draw: d = (c + V) mod L with L = SUM sigma_f sigma_b and the rank count over the cumulative products;
     each part drawn exactly sigma_f sigma_b times over any L consecutive beats; a silent future gives law 9's draw;
  2. Bell by the zigzag on a line: each detector's setting drawn late by its own dial and carried back along its twin
     to the birth, the pair's split drawn there over the joint sizes, each outcome carried forward to its detector;
     S over full turns at three timings of the two clicks (A first, both at one tick, B first), every marginal;
  3. three parties (GHZ, each setting X or Y): every marginal of one and of two parties against the others' settings;
  4. a machine's feed-forward: B's setting chosen by A's outcome, sent by light; the histories that agree at both ends;
  5. the aim: a split whose left side leads to a composite clock and its binding click; the future's weight w carried
     back to the side that led there; the histories that agree at both ends (none, one or two) under a monotone draw,
     Born at w = 0, and the lean when the board keeps the history with the composite.
"""

from fractions import Fraction
from itertools import product


def nonneg(n: int) -> int:
    """The one whether: 1 where n is at least 0 and 0 below, the quotient of n by n n + 1, plus 1."""
    return n // (n * n + 1) + 1


def drawn(n: int, sizes: list[int]) -> int:
    """The rank count: the part whose cumulative interval holds d = n mod L, with no sort and no if."""
    total = sum(sizes)
    d = n % total
    part, run = 0, 0
    for s in sizes[:-1]:
        run += s
        part += nonneg(d - run)
    return part


def part_one() -> list[str]:
    """The product draw is exact over a full turn, and a silent future gives the fair draw of law 9."""
    out, cases, silent = [], 0, 0
    for k in range(1, 5):
        for f in product(range(0, 4), repeat=k):
            for b in product(range(0, 4), repeat=k):
                sizes = [x * y for x, y in zip(f, b, strict=True)]
                if sum(sizes) == 0:
                    continue
                counts = [0] * k
                for n in range(sum(sizes)):
                    counts[drawn(n, sizes)] += 1
                assert counts == sizes, (f, b, counts)
                cases += 1
            if sum(f):
                for level in range(1, 4):
                    sizes = [x * level for x in f]
                    counts = [0] * k
                    for n in range(sum(sizes)):
                        counts[drawn(n, sizes)] += 1
                    assert all(c * sum(f) == x * sum(counts) for c, x in zip(counts, f, strict=True))
                    silent += 1
    out.append(
        f"  each part drawn exactly sigma_f sigma_b times over a full turn: {cases} of {cases} cases (1 to 4 parts, sizes 0 to 3)"
    )
    out.append(
        f"  a silent future (sigma_b alike for every part) draws by sigma_f alone, law 9 (Born): {silent} of {silent} cases"
    )
    return out


# The plan's four axes as cosines over 29 between A's and B's settings (DAVID-TENSOR24-THE-FAIR-DRAW-AND-POSITION.md 7):
# a.b = 21/29, a.b' = 21/29, a'.b = 20/29, a'.b' = -20/29, so E = -cos and S = E(a,b) + E(a,b') + E(a',b) - E(a',b').
COS = {(0, 0): 21, (0, 1): 21, (1, 0): 20, (1, 1): -20}
SIGN = {(0, 0): 1, (0, 1): 1, (1, 0): 1, (1, 1): -1}


def joint_sizes(x: int, y: int) -> list[int]:
    """The pair's joint sizes for the settings (x, y), in the order (+,+), (+,-), (-,+), (-,-): 29 - s_A s_B k, so
    P(s_A, s_B) = (1 - s_A s_B cos) / 4 exactly, the singlet's odds, over L = 116."""
    k = COS[(x, y)]
    return [29 - k, 29 + k, 29 + k, 29 - k]


OUTCOMES = [(1, 1), (1, -1), (-1, 1), (-1, -1)]


def worldline(birth: int, end: int, start: int, step: int) -> list[tuple[int, int]]:
    """A twin's worldline from the birth's Node-clock to its detector's, one Mesh every `step` ticks: (tick, site)."""
    path, x, t = [(start, birth)], birth, start
    direction = 1 if end > birth else -1
    while x != end:
        t += step
        x += direction
        path.append((t, x))
    return path


def carried(path: list[tuple[int, int]]) -> int:
    """Checks that a carry along a worldline moves at most one Mesh a step, and returns its steps."""
    for (t0, x0), (t1, x1) in zip(path, path[1:], strict=False):
        assert abs(x1 - x0) <= 1 and t1 != t0
    return len(path) - 1


def part_two() -> list[str]:
    """Bell by the zigzag: the settings ride back to the birth, the split is drawn there, the outcomes ride forward."""
    out = []
    half, birth, start, step = 6, 6, 0, 2
    a_site, b_site = 0, 2 * half
    to_a = worldline(birth, a_site, start, step)
    to_b = worldline(birth, b_site, start, step)
    arrive = to_a[-1][0]
    for name, (late_a, late_b) in (
        ("A first", (0, 5)),
        ("both at one tick", (3, 3)),
        ("B first", (5, 0)),
    ):
        t_a, t_b = arrive + late_a, arrive + late_b
        hits = {(x, y): [0, 0, 0, 0] for x in (0, 1) for y in (0, 1)}
        steps, reads_across = 0, 0
        histories = 0
        # each detector's own dial at its click, a full turn each
        for dial_a, dial_b in product(range(2), repeat=2):
            x, y = dial_a % 2, dial_b % 2  # the settings, drawn late, at t_a and t_b
            # the backward board: each setting rides back along its twin's worldline, from the click to the birth
            back_a = list(reversed(to_a + [(t, a_site) for t in range(arrive + 1, t_a + 1)]))
            back_b = list(reversed(to_b + [(t, b_site) for t in range(arrive + 1, t_b + 1)]))
            steps += carried(list(reversed(back_a))) + carried(list(reversed(back_b)))
            sizes = joint_sizes(x, y)
            # the birth's own dial, a full turn: the split where the dials meet
            for n in range(sum(sizes)):
                s_a, s_b = OUTCOMES[drawn(n, sizes)]
                # the forward board: each outcome rides out along its twin to its detector, which reads it there
                steps += carried(to_a) + carried(to_b)
                # the history agrees at both ends when the settings read at the clicks are the ones carried back;
                # the settings are the detectors' own dials, which the twins do not touch, so one sweep closes it
                histories += 1
                hits[(x, y)][OUTCOMES.index((s_a, s_b))] += 1
        expect = {
            k: Fraction(sum(s_a * s_b * h for (s_a, s_b), h in zip(OUTCOMES, v, strict=True)), sum(v))
            for k, v in hits.items()
        }
        s_value = sum(SIGN[k] * expect[k] for k in expect)
        margin_a = {k: Fraction(v[0] + v[1], sum(v)) for k, v in hits.items()}
        margin_b = {k: Fraction(v[0] + v[2], sum(v)) for k, v in hits.items()}
        out.append(
            f"  {name} (A clicks at tick {t_a}, B at {t_b}): S = {s_value} = {float(s_value):.5f}"
        )
        out.append(
            "    E(a,b), E(a,b'), E(a',b), E(a',b') = "
            + ", ".join(str(expect[k]) for k in ((0, 0), (0, 1), (1, 0), (1, 1)))
        )
        out.append(
            "    A's marginal at every setting pair: "
            + ", ".join(str(margin_a[k]) for k in sorted(margin_a))
            + "; B's: "
            + ", ".join(str(margin_b[k]) for k in sorted(margin_b))
        )
        out.append(
            f"    histories agreeing at both ends: {histories} of {histories}, one per draw; carries one Mesh a step: {steps}; reads across space: {reads_across}"
        )
    out.append(
        "  the board's cone closure at one tick reads S = 0 there (l4); the zigzag needs no window"
    )
    return out


def ghz_sizes(settings: tuple[int, int, int]) -> list[int]:
    """GHZ's joint sizes over the eight outcomes for settings X (0) or Y (1): 1 + E s_A s_B s_C over L = 8, E = +1 at
    XXX, -1 at XYY, YXY and YYX, 0 otherwise."""
    ys = sum(settings)
    e = 1 if ys == 0 else (-1 if ys == 2 else 0)
    return [1 + e * sa * sb * sc for sa, sb, sc in product((1, -1), repeat=3)]


def part_three() -> list[str]:
    """Three parties: the three settings ride back to the birth, the split is drawn there jointly."""
    out = []
    triples = list(product((1, -1), repeat=3))
    one_party, two_party = set(), {}
    mermin = {}
    for settings in product((0, 1), repeat=3):
        sizes = ghz_sizes(settings)
        counts = [0] * 8
        for n in range(sum(sizes)):
            counts[drawn(n, sizes)] += 1
        total = sum(counts)
        for who in range(3):
            plus = sum(c for t, c in zip(triples, counts, strict=True) if t[who] == 1)
            one_party.add(Fraction(plus, total))
        for pair in ((1, 2), (0, 2), (0, 1)):
            other = ({0, 1, 2} - set(pair)).pop()
            for sp in product((1, -1), repeat=2):
                c = sum(
                    n for t, n in zip(triples, counts, strict=True) if (t[pair[0]], t[pair[1]]) == sp
                )
                key = (pair, settings[pair[0]], settings[pair[1]], sp)
                two_party.setdefault(key, set()).add((settings[other], Fraction(c, total)))
        if sum(settings) in (0, 2):
            products_seen = {t[0] * t[1] * t[2] for t, c in zip(triples, counts, strict=True) if c}
            mermin[settings] = products_seen
    out.append(f"  every one-party marginal at every setting: {sorted(one_party)}")
    moved = [k for k, v in two_party.items() if len({p for _, p in v}) > 1]
    out.append(
        f"  two-party marginals that move with the third party's setting: {len(moved)} of {len(two_party)}"
    )
    out.append(
        "  Mermin's products: "
        + "; ".join(f"{''.join('XY'[s] for s in k)} -> {sorted(v)}" for k, v in sorted(mermin.items()))
    )
    out.append(
        "  the carried closure in a window moved B and C's joint law by up to 1/2 (l5); the zigzag has no window"
    )
    return out


def part_four() -> list[str]:
    """A machine's feed-forward: B's setting is chosen by A's outcome, sent by light before B clicks."""
    out = []
    rule = {1: 0, -1: 1}  # B's machine sets b where A read +, b' where A read -
    hits = {}
    histories, sweeps = 0, 0
    for x in (0, 1):
        # stage 1: A's setting rides back; A's marginal over the joint sizes does not depend on b, so s_A is drawn first
        for n_a in range(2 * 58):
            first = [58, 58]  # A's sizes (+, -): 29 - k + 29 + k for either b
            s_a = (1, -1)[drawn(n_a, first)]
            # light carries s_A to B's machine, which sets y; y rides back along B's twin to the birth
            y = rule[s_a]
            sizes = joint_sizes(x, y)
            row = sizes[0:2] if s_a == 1 else sizes[2:4]
            for n_b in range(sum(row)):
                s_b = (1, -1)[drawn(n_b, row)]
                hits.setdefault((x, y), [0, 0])
                hits[(x, y)][0] += s_a * s_b
                hits[(x, y)][1] += 1
                histories += 1
            sweeps += 2
    expect = {k: Fraction(v[0], v[1]) for k, v in hits.items()}
    out.append(
        f"  E at each setting pair the machine reaches: {', '.join(f'{k}: {v}' for k, v in sorted(expect.items()))}"
    )
    out.append(
        f"  histories agreeing at both ends: {histories} of {histories} (one per pair of digits); sweeps per pair: 2"
    )
    out.append(
        "  a loop with no history needs each setting to depend on the other's outcome, so each in the other's past: no light can carry both"
    )
    return out


def part_five() -> list[str]:
    """The aim: a split whose left side leads to a composite clock; the future's weight w rides back to that side."""
    out = []
    big = 60060  # the forward dial's fine digit u runs over a full turn of `big` values, a multiple of every share's denominator
    for f_left, f_right in ((1, 1), (1, 3)):
        out.append(
            f"  forward sizes (left, right) = ({f_left}, {f_right}); left lays a hand that meets a partner and binds"
        )
        for w in (0, 1, 3, 9):
            none = one = two = 0
            kept_aim = kept_least = 0
            for u in range(big):
                # a history assumes a side; the backward board carries w to the left only where the composite forms
                # the future holds the composite's binding click
                left_sizes = [f_left * (1 + w), f_right]
                right_sizes = [f_left, f_right]  # the future is silent on it
                # the monotone draw: left where u lands below the left share of the products
                left_ok = nonneg(left_sizes[0] * big - 1 - u * sum(left_sizes))
                right_ok = 1 - nonneg(right_sizes[0] * big - 1 - u * sum(right_sizes))
                found = left_ok + right_ok
                none += 1 - nonneg(found - 1)
                one += nonneg(found - 1) * (1 - nonneg(found - 2))
                two += nonneg(found - 2)
                kept_aim += left_ok  # the board keeps the history with the composite where two agree
                kept_least += left_ok * (1 - right_ok)  # the history with fewer composites kept instead
            born = Fraction(f_left, f_left + f_right)
            lean = Fraction(f_left * (1 + w), f_left * (1 + w) + f_right)
            out.append(
                f"    w = {w}: histories none {none}, one {one}, two {two} of {big}; "
                f"left kept {Fraction(kept_aim, big)} (the composite's lean {lean}), "
                f"{Fraction(kept_least, big)} with the fewer kept (Born {born})"
            )
    return out


def main() -> None:
    lines = ["Two boards on one Node-clock, in exact integers (David, 2026-10-29)", ""]
    for title, part in (
        ("1. The product draw", part_one),
        ("2. Bell by the zigzag through the birth", part_two),
        ("3. Three parties (GHZ, settings X or Y)", part_three),
        ("4. A machine's feed-forward", part_four),
        ("5. The aim: a split whose one side leads to a composite clock", part_five),
    ):
        lines.append(title)
        lines.extend(part())
        lines.append("")
    print("\n".join(lines).rstrip())


if __name__ == "__main__":
    main()
