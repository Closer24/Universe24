"""Rule3 in one place (core/rule3.py; ALGEBRA.md #the-line, #the-direction, #the-interval): one function steps every hand in either going, the isotropic rule is the same call with equal rates, and no other file of src/ writes this arithmetic; and the generic clock is closed for building (HIGHLIGHTS.md): the clock's state is the gears and the drives' fine teeth alone, one shape for every train, one Rule3 carry per gear and one drive per held gear per tick, the readings drive nothing, the output strike and field only, ENGINE.md's table the code's."""

import ast
import random
import re
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

from event_universe import run as record
from event_universe import unspring, unwind
from event_universe.core import rates
from event_universe.core import rule3 as core
from event_universe.core.acts import flip as mirrored
from event_universe.core.rule3 import gearing, mesh_factor, rule3, spring
from event_universe.core.spokes import AXES
from event_universe.trains import REGULATOR
from tests.laws import arrivals_rule3, node_of

ROOT = Path(__file__).resolve().parents[1]
SOURCE, GAMMA = ROOT / "src" / "event_universe", 10_000


def law_line(pinion, rim, full_rate, rate, mesh_rate, factors=None, unit=1):
    square = unit * unit
    grips = tuple(2 * pinion * mesh_rate**2 * q for q in (factors or [square] * 6))
    hold = 12 * (rim * full_rate**2 - (rim - pinion) * rate**2) * square - sum(grips)
    return grips, hold, 6 * rim * full_rate**2 * square


def test_the_coefficients_are_the_laws_line_and_the_isotropic_ones_at_zero_axis_contents():
    """With no meshes' factors the even notch's six grips (R,) x 6, S, w term for term at the composed rates of a load (the rate and the mesh rate the module's two functions, core/rates.py), at the mesh unit G the integers G^2 times the unit's; with the six meshes' factors the six spokes' grips, each the mesh rate squared times its mesh's factor, the same factor read from either end; the vacuum's rates 2 Gamma^2 times the plain rule; the mesh's factor Q = (G^2 (Gamma - t)^2 + Gamma^2 div 2) div Gamma^2, G^2 at no tension, 0 at the tension Gamma, 264 at G = 16 and the tension -153 at Gamma 10,000 (a hill above G^2), resolved to Gamma / (2 G^2); the band's rotation at k = 0 carries the rate's square and the unsprung band on a chain the mesh rate squared, the notch entering the mesh twice, exact in rationals. The vacuum's rates give 2 Gamma^2 times the plain rule, the notches bit for bit; a factor on the +x mesh alone changes that spoke's grip and the own term by 2 pinion p^2 (Q - 1); the band at k = 0 is 2 cos omega = (6 R + S) / w = 2 - 2 f (1 - pinion / rim) with f = p_0^2 / Gamma^2 the rate's square (the mesh rate cancels at k = 0), and the unsprung hand on a chain cos omega = 1 - f_a (1 - cos k) / 3 with f_a = p_i^2 / Gamma^2, p_i = p_0^2 / Gamma to the unit, at cos k = 1, 0 and -1 (ALGEBRA.md #the-paces)."""
    rng = random.Random(3)
    for _ in range(500):
        pinion, rim, full_rate = rng.randint(1, 1000), rng.randint(1, 1000), rng.choice([1, 100, GAMMA])
        load, unit = rng.randint(-full_rate + 1, full_rate - 1), rng.choice([1, 2, 16])
        factors = tuple(unit * unit + rng.randint(-50, 50) for _ in range(6))
        rate, p = rates.rate(full_rate, load), rates.mesh_rate(full_rate, load)
        assert gearing(pinion, rim, full_rate, rate, p)[:3] == law_line(pinion, rim, full_rate, rate, p)
        found = gearing(pinion, rim, full_rate, rate, p, factors, unit)[:3]
        assert found == law_line(pinion, rim, full_rate, rate, p, factors, unit)
        plain = gearing(pinion, rim, full_rate, rate, p, None, unit)[:3]
        assert gearing(pinion, rim, full_rate, rate, p, (unit * unit,) * 6, unit)[:3] == plain
        (grip, *_), hold_iso, teeth = gearing(pinion, rim, full_rate, rate, p)[:3]
        assert plain == ((grip * unit * unit,) * 6, hold_iso * unit * unit, teeth * unit * unit)
        vacuum = ((2 * full_rate**2 * pinion,) * 6, 0, 6 * rim * full_rate**2)
        assert gearing(pinion, rim, full_rate, full_rate, full_rate)[:3] == vacuum
        q = factors[0]
        along = (2 * q * p**2 * pinion,) + (grip,) * 5, hold_iso - 2 * pinion * p**2 * (q - 1), teeth
        assert gearing(pinion, rim, full_rate, rate, p, (q,) + (1,) * 5)[:3] == along
    assert (mesh_factor(GAMMA, 16, 0), mesh_factor(GAMMA, 16, GAMMA)) == (256, 0)
    assert mesh_factor(GAMMA, 16, -153) == 264 and mesh_factor(GAMMA, 16, GAMMA // 512) == 255
    for pinion, rim, c in ((800, 809, 500), (3200, 3227, 2000), (1, 1, 0), (1, 1, 2000)):
        p_0, p_i = rates.rate(GAMMA, c), rates.mesh_rate(GAMMA, c)
        (grip, *_), hold, teeth = gearing(pinion, rim, GAMMA, p_0, p_i)[:3]
        rate, mesh = Fraction(p_0 * p_0, GAMMA**2), Fraction(p_i * p_i, GAMMA**2)
        assert Fraction(6 * grip + hold, teeth) == 2 - 2 * rate * (1 - Fraction(pinion, rim))
        for cosine in (1, 0, -1):
            band = Fraction(grip * (2 * cosine + 4) + hold, 2 * teeth)
            assert pinion != rim or band == 1 - mesh * (1 - cosine) / 3


def test_the_one_rule_steps_forward_and_back_exactly_on_integers_and_int64_arrays():
    """w a_next + r' = SUM over the six spokes of R_ij arr_j + S a_now - w a_before + r with 0 <= r' < w, the inverse exact; on int64 arrays at an even notch the sum over the spokes equals R times the six-sum bit for bit, the dtype kept. The form's clock term w (now^2 + before^2) - S now before and the magnitude bound 6 A R + A |S| + w (A + 1) are read from the one function's integers."""
    rng = random.Random(5)
    for _ in range(500):
        pinion, rim, full_rate = rng.randint(1, 1000), rng.randint(1, 1000), rng.choice([1, GAMMA])
        load = rng.randint(-full_rate + 1, full_rate - 1)
        factors = tuple(16 * 16 - rng.randint(0, 30) for _ in range(6))
        rate, mesh_rate = rates.rate(full_rate, load), rates.mesh_rate(full_rate, load)
        grips, hold, teeth = gearing(pinion, rim, full_rate, rate, mesh_rate, factors, 16)[:3]
        *pulls, now, before = (rng.randint(-(10**6), 10**6) for _ in range(8))
        fine = rng.randint(0, teeth - 1)
        total = sum(grip * pull for grip, pull in zip(grips, pulls, strict=True))
        total += hold * now - teeth * before + fine
        flows = sum(grip * (pull - now) for grip, pull in zip(grips, pulls, strict=True))
        own = spring(pinion, rim, rate, 16)
        assert own == 2 * teeth - hold - sum(grips)  # the spring, the identity of the two forms
        nxt, carried = rule3(flows, own, teeth, now, before, fine)
        assert (nxt, carried) == (total // teeth, total % teeth) and 0 <= carried < teeth
        assert arrivals_rule3(grips, pulls, hold, teeth, now, before, fine) == (
            nxt,
            carried,
        )
        back = rule3(flows, own, teeth, now, nxt, carried, -1)
        assert back == (before, fine)
    generator, shape = np.random.default_rng(9), (4, 3, 2)
    pinion, rim = np.full(shape, 800, dtype=np.int64), np.full(shape, 809, dtype=np.int64)
    load = generator.integers(-3000, 3000, shape, dtype=np.int64)
    pulls = tuple(generator.integers(-(10**6), 10**6, shape, dtype=np.int64) for _ in range(6))
    now, before = (generator.integers(-(10**6), 10**6, shape, dtype=np.int64) for _ in range(2))
    grips, hold, teeth = gearing(
        pinion, rim, GAMMA, rates.rate_of(GAMMA, load), rates.mesh_rate_of(GAMMA, load)
    )[:3]
    fine = generator.integers(0, 10**9, shape, dtype=np.int64) % teeth
    flows = grips[0] * sum(pull - now for pull in pulls)
    own = 2 * teeth - hold - sum(grips)
    nxt, carried = rule3(flows, own, teeth, now, before, fine)
    total = grips[0] * sum(pulls) + hold * now - teeth * before + fine
    assert nxt.dtype == np.int64 and np.array_equal(nxt, np.floor_divide(total, teeth))
    assert np.array_equal(carried, total - teeth * nxt)
    back = rule3(flows, own, teeth, now, nxt, carried, -1)
    assert np.array_equal(back, (before, fine))


LAW_INTEGERS, TOOL_INTEGERS = frozenset({0, 1}), frozenset({0, 1, 2, 3, 4, 6})
# what the fold leaves by file (H-No-Numbers-In-Code-1 item 17, 2026-10-26): the spokes and the axes; Rule3's own gear;
# the gear counts, the powers and the width (the trace's 54 the file's key); the mesh teeth's 4; the half widths; the quarters;
# the writer's marks; quartet.py's item 7 (the NamedTuples) deferred, its three as they stand
FILE_INTEGERS = {
    "spokes.py": frozenset({2, 3}),
    "rule3.py": frozenset({2, 3, 4}),
    "trains.py": frozenset({2, 4, 8, 10}),
    "meshes.py": frozenset({4}),
    "setting.py": frozenset({2, 3}),
    "cycle.py": frozenset({4}),
    "run.py": frozenset({12, 24, 60}),
    "acts.py": frozenset(
        {2}
    ),  # the mid tooth at the half teeth by the carry on 2 (core/acts.mid, the halving's own 2 as rule3.half's)
}
# the chart's readers, Animate's since 00:42 UTC (their constants named at the module's top on reader-5), no act of the clock;
# the writer run.py reads the inventory and not the names gate (its chart keys are the files' words)
READERS = tuple(
    f"{n}.py"
    for n in "reckoner gates events rim great_clock swings strikes predicates symmetries".split()
)
WRITER = ("run.py",)
NAMED_CALLS = {
    "jammed",
    "logged",
    "get",
    "join",
}  # a jam's cause by name; a log entry's event by name; a file's key read by name; a separator


def test_no_integer_beyond_the_laws_own_enters_the_engine_or_the_tools():
    """No integer literal in src/event_universe or in any tool that touches the engine's arrays (the owner, 2026-09-30: every coordinate, gap, wavelength, width, amplitude, count and window comes from the piece's files) beyond the law's own (LAW_INTEGERS: 0 and 1, the identity and the going, -1 the inverse and the hole; 2, the halves, W_c div 2, the half teeth, the axis loads' rounding, two notches; 3, the three axes, 3 rim; 6, the six spokes, 6 rim; and in Rule3's own gear, core/rule3.py alone, 4 and 12 of S = 12 rim Gamma^2 - 12 (rim - pinion) p_0^2 - 4 pinion SUM p_a^2, RULE_LINE_INTEGERS): every other number is a file's key or the rule's own act, so a number cannot enter the engine again. The root leaves everywhere (the owner, 2026-09-30): no file of src/ or tools/ imports `isqrt` or `math`, or calls a name `isqrt` or `sqrt`; the assembly and the generator read the fixed point of the carry, and the run reads no root. The names gate (HIGHLIGHTS.md **The engine works only with families of dimension one**; the owner, 2026-10-01, 03:25): no string literal stands in src/event_universe outside docstrings, the packets of `raise` and `assert` and f-strings, but in the assembly (the files' key tables), in reports.py (the output's words), in world_files.py (the host's files) and in the package's version; so no act or reading of the engine names a train, a key or a kind, and a train's name cannot enter the engine again."""
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
            imported = (
                [a.name for a in item.names] + [getattr(item, "module", None) or ""] if importing else []
            )
            callee = item.func if isinstance(item, ast.Call) else None
            called = callee.id if isinstance(callee, ast.Name) else getattr(callee, "attr", "")
            if "math" in imported or any("sqrt" in name for name in imported) or "sqrt" in called:
                found.append(f"{path.relative_to(ROOT)}:{item.lineno} {imported or called}")
    assert not found, found
    found = []
    for path in sorted(SOURCE.rglob("*.py")):
        name = path.relative_to(SOURCE).as_posix()
        if name.startswith("assembly/") or name == "__init__.py" or name in READERS + WRITER:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        spoken = {id(item.value) for item in ast.walk(tree) if isinstance(item, ast.Expr)}
        for item in ast.walk(
            tree
        ):  # a message, a key of the chart's log or of a file, a comparison with a file's word
            if isinstance(item, ast.Raise | ast.Assert | ast.JoinedStr | ast.Compare):
                spoken |= {id(part) for part in ast.walk(item)}
            elif isinstance(item, ast.Dict):  # a line of the chart's log: its keys and its words
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
    """PC-S1 (K-S4 in pc1's form, 2026-10-25): the rate by one carry per load at the resolution Gamma^2, N_0 = Gamma^3 with the fine tooth Gamma div 2, N(c + 1) Gamma + r(c + 1) = N(c) (Gamma - 1) + r(c), the rate rounded(N, Gamma^2) half up, equal to the exact power Gamma (1 - 1 / Gamma)^c rounded half up at every load to the edge at Gamma 1,000 and 1,021 and on the hills -1 to -300; the mesh rate the rate's square over Gamma rounded once; the assembly's certificate finds no undecided load; the stopped load 3,793 at Gamma 1,000 where the mesh rate first reads 0 and the rate 22; the table's largest integer below 2^60; the vectorised entries the table's own integers in the array's kind."""
    half = Fraction(1, 2)
    for full_rate in (1_000, 1_021):
        stopped = rates.certified(full_rate)
        assert rates.mesh_rate(full_rate, stopped) == 0 and rates.mesh_rate(full_rate, stopped - 1) > 0
        for c in range(-300, 2 * stopped):
            exact = int(Fraction(full_rate) * Fraction(full_rate - 1, full_rate) ** c + half)
            assert rates.rate(full_rate, c) == exact, (full_rate, c)
            assert rates.mesh_rate(full_rate, c) == int(Fraction(exact * exact, full_rate) + half)
        sides = rates.sides(full_rate)
        assert max(abs(side.scaled) for side in sides) < 2**60 and all(
            0 <= side.carry < side.teeth for side in sides
        )
    full_rate = 1_000
    assert (
        rates.stopped_load(full_rate) == 3_793
        and rates.rate(full_rate, 3_793) == 22
        and rates.rate(full_rate, 0) == full_rate
    )
    plain, entries = (rates.rate, rates.mesh_rate), (rates.rate_of, rates.mesh_rate_of)
    narrow, sparse = (
        np.arange(-7, 53).reshape(5, 4, 3),
        np.array(list(range(7_000, 7_600, 10))).reshape(5, 4, 3),
    )
    for held in (narrow, sparse, narrow.astype(object), sparse.astype(object)):
        found, flat = [f(full_rate, held) for f in entries], held.ravel().tolist()
        assert all(a.dtype == held.dtype for a in found)
        assert [a.ravel().tolist() for a in found] == [[f(full_rate, c) for c in flat] for f in plain]


def test_the_one_rule_of_the_remainder_is_one_primitive_and_every_rounding_odd():
    """The one rule of the fine tooth (fd1's form, the owner's word of 2026-10-25): the flip r -> w - 1 - r once per reversal and the identity for an even count (core/acts.flip), the coefficient's rounding the carry from the half teeth with the carry flipped for a negative numerator, so the one rounding is sign(x) times the magnitude's half-up rounding, (2 |x| + w) div 2 w, odd at every integer; the offset pair and the driven gears' impulses odd with no tie (a skew), the origin pair the half teeth and its flip."""
    rng = random.Random(11)
    for _ in range(2_000):
        teeth, r = rng.randint(2, 10**6), rng.randint(0, 10**6)
        r = r % teeth
        assert mirrored(r, teeth, 1) == teeth - 1 - r and mirrored(mirrored(r, teeth, 1), teeth, 1) == r
        assert mirrored(r, teeth, 2) == r and mirrored(r, teeth, 0) == r
        x = rng.randint(-(10**9), 10**9)
        sign = (x > 0) - (x < 0)
        assert rates.rounded(x, teeth) == sign * ((2 * abs(x) + teeth) // (2 * teeth))
        assert rates.rounded(-x, teeth) == -rates.rounded(x, teeth)
        q, wx = 2 * rng.randint(-(10**6), 10**6) + 1, 2 * rng.randint(1, 10**6)
        assert rates.rounded(q, wx) == (2 * q + wx) // (2 * wx)
    half = 1_000 // 2
    assert (half, mirrored(half, 1_000, 1)) == (500, 499)


def test_the_take_count_is_one_carried_division_of_the_walls_by_the_price_tc_s1():
    """TC-S1 (the owner's word of 2026-10-26, 08:3x UTC, "approved"; both hands' one finding, The-Take-Count-As-Rule3-Division_COMPARISON.md section 3, H-Take-Count-As-Rule3-Division-1's one-clock test): on the hole setting's first unwinds the fall is the count times a price linear in the count, f(s) = s (price - X w s) over the wind's weight with the price X times Rule3's backward numerator read at the now slot, -t (2 w now + pull), exactly to the carry's fine tooth; the count unwound is the least count paying the windings due, the carry of the windings due by the price at the start lies at most one below it and below it exactly where the fall at those carries is short of the windings due by the moved notches' own square: one carry iterated from below, no root. Under 15 s."""
    clock, seen = node_of("world_hole.json", intervals=12), []
    orig = unwind.fall_of

    def wrapped(clock_, at, windings, r, train):
        got = orig(clock_, at, windings, r, train)
        if sys._getframe(1).f_code.co_name == "read_ends" and got[0]:
            s, _fall, k = got
            gear = train.gears[k]
            now, before = int(gear.now[at]), int(gear.before[at])
            w, gripped = int(r.teeth), 0
            for spoke, grip in enumerate(r.grips):
                gripped += unwind.at_clock(grip, at) * int(
                    gear.before[unwind.neighbour(clock_, at, spoke)]
                )
            pull = unwind.at_clock(r.hold, at) * before + gripped
            t = 1 if before > now else -1
            x, weight = int(clock_.start_stretch[at]), core.wind_weight(clock_.full_rate, clock_.G)
            seen.append((now, t, w, pull, x, weight, windings, s, -t * ((w + w) * now + pull) * x))
        return got

    unwind.fall_of = wrapped
    try:
        for _ in range(12):
            clock.tick()
    finally:
        unwind.fall_of = orig
    assert unspring.unwind.fall_of is orig and len(seen) == 47
    below = short = 0
    for now, t, w, pull, x, weight, windings, s, price in seen:
        moved = now + t * s
        fall = x * (w * (now * now - moved * moved) - t * s * pull)
        assert fall == s * (price - x * w * s) and price > 0
        assert (
            core.carries(fall, weight)
            >= windings
            > core.carries((s - 1) * (price - x * w * (s - 1)), weight)
        )
        first = -core.carries(-windings * weight, price)
        assert first <= s <= first + 1
        below += first < s
        short += core.carries(first * (price - x * w * first), weight) < windings
    assert below == short > 0


def test_every_move_of_the_close_books_its_momentum_on_the_flux_line_as_an_identity_lt_s1():
    """LT-S1 (the owner's word of 2026-10-26, 08:4x UTC, "approve"; The-Lay-As-The-Take-Reversed_COMPARISON.md section 3, H-Lay-As-The-Take-Reversed-1's one-clock test): on the hole setting every move of the striking drives its tally into the regulator's flow gear of its axis at its clock by the clock's one drive act, so at every strike the mesh's chart identity holds per axis at every end, -dP p_0^2 + carry before - carry after = advanced x (K rim Gamma^2 T), the gear gaining what the moved quantum lost (the Boss's sign of 10:18 UTC), read on the clock's own gears and not the log alone; the clock's carry after the tick is the last tally's at that clock; the rewind exact through 14 ticks with the tallies undone. Under 15 s."""
    clock = node_of("world_hole.json", intervals=14)
    teeth = clock.trace * clock.rim * clock.full_rate * clock.full_rate * clock.key
    flow = slice(1 + AXES, 1 + AXES + AXES)
    hashes, checked = [], 0
    for _ in range(14):
        hashes.append(record.state_hash(clock))
        from_log = len(clock.log)
        clock.tick()
        last = {}
        for e in clock.log[from_log:]:
            if e["event"] not in ("birth", "credit"):
                continue
            tallies = [(tuple(t["node"]), t["dP_take"], t) for t in e.get("takes", [e])]
            if e["event"] == "birth":
                tallies += [
                    (
                        tuple(where),
                        push,
                        {k: e[k + "_ends"][j] for k in ("clock", "recoil", "carry_was", "carry")},
                    )
                    for j, (where, push) in enumerate(
                        zip((e["minus"], e["plus"]), e["dP_lay_ends"], strict=True)
                    )
                ]
            for where, push, t in tallies:
                for a in range(AXES):
                    assert (
                        t["carry_was"][a] - t["carry"][a] - push[a] * t["clock"] ** 2
                        == t["recoil"][a] * teeth
                    )
                last[where], checked = t["carry"], checked + 1
        gears = clock.train(REGULATOR).gears[flow]
        assert all(carry == [int(gear.dfine[at]) for gear in gears] for at, carry in last.items())
    assert checked == 193
    for h in reversed(hashes):
        clock.tick(-1)
        assert record.state_hash(clock) == h
