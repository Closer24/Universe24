"""Rule3 in one place (core/rule3.py; ALGEBRA.md #the-line, #the-direction, #the-interval): one function steps every hand in either going, the isotropic rule is the same call with equal rates, and no other file of src/ writes this arithmetic; and the generic clock is closed for building (HIGHLIGHTS.md): the clock's state is the gears and the drives' fine teeth alone, one shape for every train, one Rule3 carry per gear and one drive per held gear per tick, the readings drive nothing, the output strike and field only, ENGINE.md's table the code's."""

import ast
import random
import re
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from event_universe import bobs, hands, readings, unwind
from event_universe import run as record
from event_universe.assembly import setting
from event_universe.core import rates
from event_universe.core.acts import flip as mirrored
from event_universe.core.rule3 import gearing, mesh_factor, rule3, spring
from event_universe.core.spokes import AXES, SPOKES
from event_universe.meshes import factors
from event_universe.trains import REGULATOR
from tests.laws import arrivals_rule3, node_of, world_of

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
# what the fold leaves by file (H-No-Numbers-In-Code-1 item 17, 2026-10-26; the generic folds of David's DAVID-GENERIC-ENGINE.md
# part A, 2026-10-27: every two the signs' count, the hand and the halving SIDES, the time gear's power AXES + 1, the quarters
# the order of i, the half spans the half turn's closure): the dimension alone, and the writer's marks
FILE_INTEGERS = {"spokes.py": frozenset({3}), "run.py": frozenset({12, 24, 60})}
# the chart's readers, Animate's since 00:42 UTC (their constants named at the module's top on reader-5), no act of the clock;
# the writer run.py reads the inventory and not the names gate (its chart keys are the files' words)
READERS = tuple(
    f"{n}.py"
    for n in "reckoner gates events rim great_clock swings strikes predicates symmetries phenomena".split()
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


def test_the_take_is_the_least_count_whose_window_wind_falls_by_the_windings_tc_s1(monkeypatch) -> None:
    """TC-S1 as the wave amends it (the owner's word of 2026-10-27, 15:5x UTC, "yes to all, by your recommendation": the take's fall is the wind's own fall; David's DAVID-CLOSE-LAW.md item 1; the closed form's price, which carried the pull's sign reversed against the wind's fall at 47 of 47 takes on the head, the Reader's finding 1, struck and kept by name): at every chime of the chiral setting over 14 ticks (31 under the great clock's bounds, 101 at the wave, each one a take: light arrives at every one, so none is a still chime, bobs.still_chime, which takes nothing) the light's gear moves by the least count at which the window's wind falls by what is owed, the windings less the slack the earlier takes left (17 owe nothing and move no notch, 57 at the wave), the fall booked is the window's wind before less after to the integer, one count fewer falls short, and the excess stands in the slack (EX-S1)."""
    clock, seen = node_of("world_nature.json", intervals=14), []
    real = bobs.unwinds

    def wrapped(clock_: Any, ends: Any, gearing_: Any, cause: int, *args: Any, **keys: Any) -> Any:
        (at, windings), light = ends[0], clock_.unsprung()
        window = unwind.window_clocks(clock_, at)

        def wind() -> int:
            return sum(int(v) for v in hands.wind(clock_, light.gears, gearing_, window))

        before, got = wind(), real(clock_, ends, gearing_, cause, *args, **keys)
        if got is not None:
            (take,) = got
            gear, (now, was, _s) = light.gears[take["taken_line"]], take["taker"]
            after, back = wind(), 1 if was > now else -1
            gear.now[at] -= back
            short = wind()
            gear.now[at] += back
            seen.append((before - after, before - short, take, windings))
        return got

    monkeypatch.setattr(bobs, "unwinds", wrapped)
    for _ in range(14):
        clock.tick()
    chimes = (len(seen), clock.counts["body_clicks"], clock.counts["laid_back"])  # takes, chimes, still
    assert chimes == (31, 31, 0) and sum(take["levels"] == 0 for _f, _s, take, _w in seen) == 17
    for fall, short, take, windings in seen:
        assert fall == take["taken"] >= take["owed"] and take["booked"] == windings
        assert take["levels"] == 0 or short < take["owed"]  # the least count: one fewer falls short
        assert take["taken"] + take["remainder_was"] - take["remainder"] == windings  # EX-S1


def test_every_move_of_the_close_books_its_momentum_on_the_flux_line_as_an_identity_lt_s1():
    """LT-S1 (the owner's word of 2026-10-26, 08:4x UTC, "approve"; The-Lay-As-The-Take-Reversed_COMPARISON.md section 3, H-Lay-As-The-Take-Reversed-1's one-clock test): on the chiral setting with its three bobs at 6 quanta (the hole's first fittings stand at its tick 53 under the wave's light; at the world file's 2 quanta no booking of the 14 ticks advances a notch under the great clock's bounds, 4 did at the wave) every move of the striking drives its tally into the regulator's flow gear of its axis at its clock by the clock's one drive act, so at every strike the mesh's chart identity holds per axis at every end, -dP p_0^2 + carry before - carry after = advanced x (K rim Gamma^2 T), seen in both of its cases, the carry below one level of the line and an advance of the gear's notch, the gear gaining what the moved quantum lost (the Boss's sign of 10:18 UTC), read on the clock's own gears and not the log alone; the clock's carry after the tick is the last tally's at that clock; the rewind exact through 14 ticks with the tallies undone. Under 15 s."""
    seed = [s | {"quanta": 6} if "quanta" in s else s for s in world_of("world_nature.json")[1]["seed"]]
    clock = node_of("world_nature.json", intervals=14, seed=seed)
    teeth = clock.trace * clock.rim * clock.full_rate * clock.full_rate * clock.key
    flow = slice(1 + AXES, 1 + AXES + AXES)
    hashes, checked, pushed, advanced = [], 0, 0, 0
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
                for was, now, p, q in zip(t["carry_was"], t["carry"], push, t["recoil"], strict=True):
                    assert was - now - p * t["clock"] ** 2 == q * teeth  # per axis, every booking
                last[where], checked = t["carry"], checked + 1
                pushed, advanced = pushed + any(push), advanced + any(t["recoil"])
        gears = clock.train(REGULATOR).gears[flow]
        assert all(carry == [int(gear.dfine[at]) for gear in gears] for at, carry in last.items())
    # every booking, those with a push, those advancing the flow gear's notch, the still chimes (push 0),
    # under the great clock's bounds (116, 49, 4 and 0 at the wave at 2 quanta)
    assert (checked, pushed, advanced, clock.counts["laid_back"]) == (142, 58, 2, 0)
    for h in reversed(hashes):
        clock.tick(-1)
        assert record.state_hash(clock) == h


def test_a_hands_wind_is_a_gaussian_norm_and_its_quanta_are_its_sweep() -> None:
    """The amplitudes on the great clock as the hand's norms (David's DAVID-AMPLITUDES.md sections 1 and 5, toys-5 6415deeb0, on the owner's word of 2026-10-27, 12:4x UTC; the owner's rule of 14:5x UTC, a push's test sees what it was pushed for): on every sprung hand of the toy and the middle calibres laid even at rest on an empty 3-cube at the vacuum, the wind is the Gaussian form 3 [rim (|z_now|^2 + |z_before|^2) - 2 pinion Re(conj(z_now) z_before)] exactly; at rest it is SPOKES s |W| + 3 (r1^2 + r2^2) div rim, so a rest hand's quanta are its sweep in e; and the winding is 3 T s."""
    for name in ("world_node.json", "world_bodies.json"):
        clock = node_of(name, shape=[3] * 3, seed=[])
        clock.start_load, clock.start_stretch = readings.load(clock), clock.train(REGULATOR).gears[0].now
        for k, train in enumerate(clock.hands()):
            if train is clock.unsprung() or train.ratio is None:
                continue
            pinion, rim = train.ratio
            s = rates.sine_rim(pinion, rim)
            assert clock.windings[k] == AXES * clock.key * s
            gearing_ = readings.gearing(clock, train.ratio, clock.start_load, factors(clock))
            for sense, a in ((1, 1), (-1, 7), (1, 135), (-1, 5690), (1, 10**6 + 7)):
                gears = setting.even_notches(clock, train, a, sense)
                wind = setting.wind_at_clock(clock, train, gears, gearing_)
                (n0, b0), (n1, b1) = ((int(g.now.flat[0]), int(g.before.flat[0])) for g in gears)
                assert wind == 3 * (
                    rim * (n0 * n0 + n1 * n1 + b0 * b0 + b1 * b1) - 2 * pinion * (n0 * b0 + n1 * b1)
                )
                r1, r2 = a * pinion % rim, a * s % rim
                assert wind == SPOKES * s * abs(n0 * b1 - n1 * b0) + AXES * (r1 * r1 + r2 * r2) // rim
