"""Rule3 in one place (core/rule3.py; ALGEBRA.md #the-line, #the-direction, #the-interval): one function steps every record in either direction, the isotropic rule is the same call with equal paces, and no other file of src/ writes this arithmetic; and the generic Node is closed for building (HIGHLIGHTS.md): the NodeState is the lines and the writes' remainders alone, one shape for every family, one Rule3 division per line and one write per held line per interval, the readings write nothing, the output click and field only, ENGINE.md's table the code's."""

import ast
import random
import re
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

from event_universe import merger, take
from event_universe.core import paces
from event_universe.core import rule3 as core
from event_universe.core.rule3 import form_term, link_factor, mass, mirrored, rule3, rule_integers
from tests.laws import arrivals_rule3, node_of

ROOT = Path(__file__).resolve().parents[1]
SOURCE, GAMMA = ROOT / "src" / "event_universe", 10_000


def law_line(num, den, gamma, clock, pace, factors=None, unit=1):
    square = unit * unit
    reads = tuple(2 * num * pace**2 * q for q in (factors or [square] * 6))
    self_coefficient = 12 * (den * gamma**2 - (den - num) * clock**2) * square - sum(reads)
    return reads, self_coefficient, 6 * den * gamma**2 * square


def test_the_coefficients_are_the_laws_line_and_the_isotropic_ones_at_zero_axis_contents():
    """With no Links' factors the uniform level's six reads (R,) x 6, S, w term for term at the composed paces of a content (the clock and the Node's pace the module's two functions, core/paces.py), at the Link unit G the integers G^2 times the unit's; with the six Links' factors the six Ports' reads, each the Node's pace squared times its Link's factor, the same factor read from either end; the vacuum's paces 2 Gamma^2 times the plain rule; the Link's factor Q = (G^2 (Gamma - t)^2 + Gamma^2 div 2) div Gamma^2, G^2 at no tension, 0 at the tension Gamma, 264 at G = 16 and the tension -153 at Gamma 10,000 (a hill above G^2), resolved to Gamma / (2 G^2); the band's rotation at k = 0 carries the clock's square and light's band on a chain the Node's pace squared, the level entering the Link twice, exact in rationals. The vacuum's paces give 2 Gamma^2 times the plain rule, the levels bit for bit; a factor on the +x Link alone changes that Port's read and the own term by 2 num p^2 (Q - 1); the band at k = 0 is 2 cos omega = (6 R + S) / w = 2 - 2 f (1 - num / den) with f = p_0^2 / Gamma^2 the clock's square (the Link's pace cancels at k = 0), and light on a chain cos omega = 1 - f_a (1 - cos k) / 3 with f_a = p_i^2 / Gamma^2, p_i = p_0^2 / Gamma to the unit, at cos k = 1, 0 and -1 (ALGEBRA.md #the-paces)."""
    rng = random.Random(3)
    for _ in range(500):
        num, den, gamma = rng.randint(1, 1000), rng.randint(1, 1000), rng.choice([1, 100, GAMMA])
        content, unit = rng.randint(-gamma + 1, gamma - 1), rng.choice([1, 2, 16])
        factors = tuple(unit * unit + rng.randint(-50, 50) for _ in range(6))
        clock, p = paces.clock(gamma, content), paces.link_pace(gamma, content)
        assert rule_integers(num, den, gamma, clock, p)[:3] == law_line(num, den, gamma, clock, p)
        found = rule_integers(num, den, gamma, clock, p, factors, unit)[:3]
        assert found == law_line(num, den, gamma, clock, p, factors, unit)
        plain = rule_integers(num, den, gamma, clock, p, None, unit)[:3]
        assert rule_integers(num, den, gamma, clock, p, (unit * unit,) * 6, unit)[:3] == plain
        (read, *_), self_iso, wall = rule_integers(num, den, gamma, clock, p)[:3]
        assert plain == ((read * unit * unit,) * 6, self_iso * unit * unit, wall * unit * unit)
        vacuum = ((2 * gamma**2 * num,) * 6, 0, 6 * den * gamma**2)
        assert rule_integers(num, den, gamma, gamma, gamma)[:3] == vacuum
        q = factors[0]
        along = (2 * q * p**2 * num,) + (read,) * 5, self_iso - 2 * num * p**2 * (q - 1), wall
        assert rule_integers(num, den, gamma, clock, p, (q,) + (1,) * 5)[:3] == along
    assert (link_factor(GAMMA, 16, 0), link_factor(GAMMA, 16, GAMMA)) == (256, 0)
    assert link_factor(GAMMA, 16, -153) == 264 and link_factor(GAMMA, 16, GAMMA // 512) == 255
    for num, den, c in ((800, 809, 500), (3200, 3227, 2000), (1, 1, 0), (1, 1, 2000)):
        p_0, p_i = paces.clock(GAMMA, c), paces.link_pace(GAMMA, c)
        (read, *_), self_coefficient, wall = rule_integers(num, den, GAMMA, p_0, p_i)[:3]
        clock, link = Fraction(p_0 * p_0, GAMMA**2), Fraction(p_i * p_i, GAMMA**2)
        assert Fraction(6 * read + self_coefficient, wall) == 2 - 2 * clock * (1 - Fraction(num, den))
        for cosine in (1, 0, -1):
            band = Fraction(read * (2 * cosine + 4) + self_coefficient, 2 * wall)
            assert num != den or band == 1 - link * (1 - cosine) / 3


def test_the_one_rule_steps_forward_and_back_exactly_on_integers_and_int64_arrays():
    """w a_next + r' = SUM over the six Ports of R_ij arr_j + S a_now - w a_before + r with 0 <= r' < w, the inverse exact; on int64 arrays at a uniform level the sum over the Ports equals R times the six-sum bit for bit, the dtype kept. The form's Node term w (now^2 + before^2) - S now before and the load bound 6 A R + A |S| + w (A + 1) are read from the one function's integers."""
    rng = random.Random(5)
    for _ in range(500):
        num, den, gamma = rng.randint(1, 1000), rng.randint(1, 1000), rng.choice([1, GAMMA])
        content = rng.randint(-gamma + 1, gamma - 1)
        factors = tuple(16 * 16 - rng.randint(0, 30) for _ in range(6))
        clock, pace = paces.clock(gamma, content), paces.link_pace(gamma, content)
        reads, self_coefficient, wall = rule_integers(num, den, gamma, clock, pace, factors, 16)[:3]
        *arrivals, now, before = (rng.randint(-(10**6), 10**6) for _ in range(8))
        remainder = rng.randint(0, wall - 1)
        total = sum(read * arrival for read, arrival in zip(reads, arrivals, strict=True))
        total += self_coefficient * now - wall * before + remainder
        fluxes = sum(read * (arrival - now) for read, arrival in zip(reads, arrivals, strict=True))
        own = mass(num, den, clock, 16)
        assert own == 2 * wall - self_coefficient - sum(reads)  # the mass, the identity of the two forms
        nxt, carried = rule3(fluxes, own, wall, now, before, remainder)
        assert (nxt, carried) == (total // wall, total % wall) and 0 <= carried < wall
        assert arrivals_rule3(reads, arrivals, self_coefficient, wall, now, before, remainder) == (
            nxt,
            carried,
        )
        back = rule3(fluxes, own, wall, now, nxt, carried, -1)
        assert back == (before, remainder)
    generator, shape = np.random.default_rng(9), (4, 3, 2)
    num, den = np.full(shape, 800, dtype=np.int64), np.full(shape, 809, dtype=np.int64)
    content = generator.integers(-3000, 3000, shape, dtype=np.int64)
    arrivals = tuple(generator.integers(-(10**6), 10**6, shape, dtype=np.int64) for _ in range(6))
    now, before = (generator.integers(-(10**6), 10**6, shape, dtype=np.int64) for _ in range(2))
    reads, self_coefficient, wall = rule_integers(
        num, den, GAMMA, paces.clock_of(GAMMA, content), paces.link_pace_of(GAMMA, content)
    )[:3]
    remainder = generator.integers(0, 10**9, shape, dtype=np.int64) % wall
    fluxes = reads[0] * sum(arrival - now for arrival in arrivals)
    own = 2 * wall - self_coefficient - sum(reads)
    nxt, carried = rule3(fluxes, own, wall, now, before, remainder)
    total = reads[0] * sum(arrivals) + self_coefficient * now - wall * before + remainder
    assert nxt.dtype == np.int64 and np.array_equal(nxt, np.floor_divide(total, wall))
    assert np.array_equal(carried, total - wall * nxt)
    back = rule3(fluxes, own, wall, now, nxt, carried, -1)
    assert np.array_equal(back, (before, remainder))
    _reads, self_coefficient, wall = rule_integers(
        800, 809, GAMMA, paces.clock(GAMMA, 250), paces.link_pace(GAMMA, 250)
    )[:3]
    assert form_term(self_coefficient, wall, 7, -3) == wall * (49 + 9) + self_coefficient * 21


LAW_INTEGERS, TOOL_INTEGERS = frozenset({0, 1}), frozenset({0, 1, 2, 3, 4, 6})
# the fold's remainder by file (H-No-Numbers-In-Code-1 item 17, 2026-10-26): the Ports and the axes; Rule3's own line;
# the shapes, the powers and the width (the trace's 54 the file's key); the Link wall's 4; the half widths; the turns;
# the writer's marks; quartet.py's item 7 (the NamedTuples) deferred, its three as they stand
FILE_INTEGERS = {
    "ports.py": frozenset({2, 3}),
    "rule3.py": frozenset({2, 3, 4}),
    "rows.py": frozenset({2, 4, 8, 10, 128}),
    "links.py": frozenset({4}),
    "seed.py": frozenset({2, 3}),
    "wave.py": frozenset({4}),
    "run.py": frozenset({12, 24, 60}),
    "quartet.py": frozenset({2, 3, 4}),
}
# the record's readers, Animate's since 00:42 UTC (their constants named at the module's top on reader-5), no act of the Node;
# the writer run.py reads the inventory and not the names gate (its record keys are the files' words)
READERS = tuple(f"{n}.py" for n in "decoder gates events circle board clicks predicates".split())
WRITER = ("run.py",)
NAMED_CALLS = {
    "refused",
    "get",
    "join",
}  # a refusal's cause by name; a file's key read by name; a separator


def test_no_integer_beyond_the_laws_own_enters_the_engine_or_the_tools():
    """No integer literal in src/event_universe or in any tool that touches the engine's arrays (the owner, 2026-09-30: every coordinate, gap, wavelength, width, amplitude, count and window comes from the world's files) beyond the law's own (LAW_INTEGERS: 0 and 1, the identity and the direction, -1 the inverse and the hole; 2, the halves, W_c div 2, the half wall, the axis contents' rounding, two levels; 3, the three axes, 3 den; 6, the six Ports, 6 den; and in Rule3's own line, core/rule3.py alone, 4 and 12 of S = 12 den Gamma^2 - 12 (den - num) p_0^2 - 4 num SUM p_a^2, RULE_LINE_INTEGERS): every other number is a file's key or the rule's own act, so a number cannot enter the engine again. The root leaves everywhere (the owner, 2026-09-30): no file of src/ or tools/ imports `isqrt` or `math`, or calls a name `isqrt` or `sqrt`; the loader and the generator read the fixed point of the division act, and the run reads no root. The names gate (HIGHLIGHTS.md **The engine works only with families of dimension one**; the owner, 2026-10-01, 03:25): no string literal stands in src/event_universe outside docstrings, the packets of `raise` and `assert` and f-strings, but in the loader (the files' key tables), in reports.py (the output's words), in world_files.py (the host's files) and in the package's version; so no act or reading of the engine names a family, a key or a kind, and a family name cannot enter the engine again."""
    texts = {p: p.read_text(encoding="utf-8") for p in sorted((ROOT / "tools").glob("*.py"))}
    tools = [p for p, text in texts.items() if re.search(r"^(from|import) event_universe\b", text, re.M)]
    found = []
    for path in [*sorted(SOURCE.rglob("*.py")), *tools]:
        if path.name in READERS:
            continue
        allowed = (
            TOOL_INTEGERS if path in tools else LAW_INTEGERS | FILE_INTEGERS.get(path.name, frozenset())
        )
        for item in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(item, ast.Constant) and type(item.value) in (int, float, complex):
                if item.value not in allowed or type(item.value) is not int:
                    found.append(f"{path.relative_to(ROOT)}:{item.lineno} {item.value!r}")
    assert not found, found
    found = []
    for path in sorted([*SOURCE.rglob("*.py"), *(ROOT / "tools").glob("*.py")]):
        for item in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            importing = isinstance(item, ast.Import | ast.ImportFrom)
            imported = [a.name for a in item.names] if importing else []
            callee = item.func if isinstance(item, ast.Call) else None
            called = callee.id if isinstance(callee, ast.Name) else getattr(callee, "attr", "")
            if "math" in imported or any("sqrt" in name for name in imported) or "sqrt" in called:
                found.append(f"{path.relative_to(ROOT)}:{item.lineno} {imported or called}")
    assert not found, found
    found = []
    for path in sorted(SOURCE.rglob("*.py")):
        name = path.relative_to(SOURCE).as_posix()
        if name.startswith("loader/") or name == "__init__.py" or name in READERS + WRITER:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        spoken = {id(item.value) for item in ast.walk(tree) if isinstance(item, ast.Expr)}
        for item in ast.walk(
            tree
        ):  # a message, a key of the record's log or of a file, a comparison with a file's word
            if isinstance(item, ast.Raise | ast.Assert | ast.JoinedStr | ast.Compare):
                spoken |= {id(part) for part in ast.walk(item)}
            elif isinstance(item, ast.Dict):  # a line of the record's log: its keys and its words
                spoken |= {id(part) for part in ast.walk(item)}
            elif isinstance(item, ast.Assign) and any(
                getattr(target, "id", "") == "__slots__" for target in item.targets
            ):
                spoken |= {id(part) for part in ast.walk(item.value)}
            elif isinstance(item, ast.Subscript):
                spoken |= {id(part) for part in ast.walk(item.slice)}
            elif (
                isinstance(item, ast.Call)
                and getattr(item.func, "attr", getattr(item.func, "id", "")) in NAMED_CALLS
            ):
                spoken |= {id(part) for arg in item.args for part in ast.walk(arg)}
                spoken |= {id(part) for part in ast.walk(item.func)}
        for item in ast.walk(tree):
            if isinstance(item, ast.Constant) and isinstance(item.value, str) and id(item) not in spoken:
                found.append(f"{path.relative_to(ROOT)}:{item.lineno} {item.value!r}")
    assert not found, found


def test_the_composed_paces_are_the_laws_carried_division_at_gamma_squared_bit_for_bit_the_power():
    """PC-S1 (K-S4 in pc1's form, 2026-10-25): the clock by one carried division per content at the resolution Gamma^2, N_0 = Gamma^3 with the remainder Gamma div 2, N(c + 1) Gamma + r(c + 1) = N(c) (Gamma - 1) + r(c), the pace rounded(N, Gamma^2) half up, equal to the exact power Gamma (1 - 1 / Gamma)^c rounded half up at every content to the edge at Gamma 1,000 and 1,021 and on the hills -1 to -300; the Link's pace the clock's square over Gamma rounded once; the loader's certificate finds no undecided content; the frozen content 3,793 at Gamma 1,000 where the Link's pace first reads 0 and the clock 22; the table's largest integer below 2^60; the vectorised entries the table's own integers in the array's kind."""
    half = Fraction(1, 2)
    for gamma in (1_000, 1_021):
        frozen = paces.certified(gamma)
        assert paces.link_pace(gamma, frozen) == 0 and paces.link_pace(gamma, frozen - 1) > 0
        for c in range(-300, 2 * frozen):
            exact = int(Fraction(gamma) * Fraction(gamma - 1, gamma) ** c + half)
            assert paces.clock(gamma, c) == exact, (gamma, c)
            assert paces.link_pace(gamma, c) == int(Fraction(exact * exact, gamma) + half)
        sides = paces.sides(gamma)
        assert max(abs(side.scaled) for side in sides) < 2**60 and all(
            0 <= side.carry < side.wall for side in sides
        )
    gamma = 1_000
    assert (
        paces.frozen_content(gamma) == 3_793
        and paces.clock(gamma, 3_793) == 22
        and paces.clock(gamma, 0) == gamma
    )
    plain, entries = (paces.clock, paces.link_pace), (paces.clock_of, paces.link_pace_of)
    narrow, sparse = (
        np.arange(-7, 53).reshape(5, 4, 3),
        np.array(list(range(7_000, 7_600, 10))).reshape(5, 4, 3),
    )
    for held in (narrow, sparse, narrow.astype(object), sparse.astype(object)):
        found, flat = [f(gamma, held) for f in entries], held.ravel().tolist()
        assert all(a.dtype == held.dtype for a in found)
        assert [a.ravel().tolist() for a in found] == [[f(gamma, c) for c in flat] for f in plain]


def test_the_one_rule_of_the_remainder_is_one_primitive_and_every_rounding_odd():
    """The one rule of the remainder (fd1's form, the owner's word of 2026-10-25): the mirror r -> w - 1 - r once per reversal and the identity for an even count (rule3.mirrored), the coefficient's rounding the carried division from the half wall with the carry mirrored for a negative numerator, so odd_rounded(x, w) = sign(x) rounded(|x|, w) and odd at every integer; the turn's pair and the ride's kicks odd with no tie (a fold), the origin pair the half wall and its mirror."""
    rng = random.Random(11)
    for _ in range(2_000):
        wall, r = rng.randint(2, 10**6), rng.randint(0, 10**6)
        r = r % wall
        assert mirrored(r, wall, 1) == wall - 1 - r and mirrored(mirrored(r, wall, 1), wall, 1) == r
        assert mirrored(r, wall, 2) == r and mirrored(r, wall, 0) == r
        x = rng.randint(-(10**9), 10**9)
        sign = (x > 0) - (x < 0)
        assert paces.odd_rounded(x, wall) == sign * paces.rounded(abs(x), wall)
        assert paces.odd_rounded(-x, wall) == -paces.odd_rounded(x, wall)
        q, wx = 2 * rng.randint(-(10**6), 10**6) + 1, 2 * rng.randint(1, 10**6)
        assert paces.odd_rounded(q, wx) == paces.rounded(q, wx)
    half = 1_000 // 2
    assert (half, mirrored(half, 1_000, 1)) == (500, 499)


def test_the_take_count_is_one_carried_division_of_the_walls_by_the_price_tc_s1():
    """TC-S1 (the owner's word of 2026-10-26, 08:3x UTC, "approved"; both hands' one finding, The-Take-Count-As-Rule3-Division_COMPARISON.md section 3, H-Take-Count-As-Rule3-Division-1's one-Node test): on the hole seed's first takes the fall is the count times a price linear in the count, f(s) = s (price - X w s) over the share's weight with the price X times Rule3's backward numerator read at the now slot, -t (2 w now + pull), exactly to the division's remainder; the count taken is the least count paying the walls, the carried division of the walls by the price at the start lies at most one below it and below it exactly where that quotient's fall is short of the walls by the moved levels' own square: one carried division iterated from below, no root. Under 15 s."""
    node, seen = node_of("world_hole.json", intervals=12), []
    orig = take.fall_of

    def wrapped(node_, at, walls, r, row):
        got = orig(node_, at, walls, r, row)
        if sys._getframe(1).f_code.co_name == "read_ends" and got[0]:
            s, _fall, k = got
            line = row.lines[k]
            now, before = int(line.now[at]), int(line.before[at])
            w, reached = int(r.wall), 0
            for port, reach in enumerate(r.reaches):
                reached += take.at_node(reach, at) * int(line.before[take.neighbour(node_, at, port)])
            pull = take.at_node(r.self_coefficient, at) * before + reached
            t = 1 if before > now else -1
            x, weight = int(node_.start_x[at]), core.share_weight(node_.gamma, node_.G)
            seen.append((now, t, w, pull, x, weight, walls, s, -t * ((w + w) * now + pull) * x))
        return got

    take.fall_of = wrapped
    try:
        for _ in range(12):
            node.step()
    finally:
        take.fall_of = orig
    assert merger.take.fall_of is orig and len(seen) == 47
    below = short = 0
    for now, t, w, pull, x, weight, walls, s, price in seen:
        moved = now + t * s
        fall = x * (w * (now * now - moved * moved) - t * s * pull)
        assert fall == s * (price - x * w * s) and price > 0
        assert (
            core.quotient(fall, weight)
            >= walls
            > core.quotient((s - 1) * (price - x * w * (s - 1)), weight)
        )
        first = -core.quotient(-walls * weight, price)
        assert first <= s <= first + 1
        below += first < s
        short += core.quotient(first * (price - x * w * first), weight) < walls
    assert below == short > 0
