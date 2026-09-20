"""The one coupling as a signed inner product over the columns (the Beam
Law, docs/BEAM_LAW.md, section 3 step 4 and the implementation note on the
columns; the model owner, 2026-09-20, "one mechanism for all the laws on
the GameBoard"; the mathematician's verified form, scratchpad/columns/
COLUMNS.md, "correct and working"): the push a measured event A takes from
a group of a free family B's rays with the label moment V is, per axis,

    push = sum over the columns c of
           epsilon_c x sign(V n_A^c n_B^c) x by_clock(age_A, |V n_A^c n_B^c M_A|, d_A^c d_B^c),

    every column floored on its own off the reader's clock, never summed
    before the floor; gravity the built-in first column of every family
    (the value [1, 1], the sign minus, not a term in the code), `charge`
    the built-in second (the family key `charge` its value, the sign plus),
    and per family `"columns": {"<name>": {"value": n or [n, d], "sign":
    1 or -1}}` for any further column (`nature_beam.push_form`; the
    reader's side the charges the frame read from what it holds,
    `Measured.charges`, the arriving side the family's values). The
    expected integers of docs/TEST_EXPECTATIONS.md ("The columns"), written
    down before the first run; K 2^20, N 64, `suspension` 0, `release`
    [0, 1] (the rays declared in transit) and an open 5 x 5 x 1 board with
    z periodic unless said:

(a) bit-exactness: the two built-in columns are the push form as landed
    on 2026-09-20 (`M_A x (rho_A rho_B - 1) x V_B`, the electric part
    `sign x by_clock(age, |V n_A n_B M_A|, d_A d_B)`), integer by integer
    and refusal by refusal, on a grid of every input (V in -5 .. 5 on
    three axes with different signs, M_A in 0 .. 3, n_A and n_B in -2 ..
    2, d_A and d_B in 1 .. 3, the age 0 .. 4: 49 500 cases) and on 3 000
    random cases at the register's scale (V to 2^62, M_A to 2^40, n and d
    to 2^30 - 1, the age to 2^31; a refusal shared); and the replay of
    the series 7 worlds of `examples/events/coupling/` (the mathematician's
    second replay): every `read` record's push recomputed by the landed
    form from the record alone (its `reading` is V, the fixed reader's
    declared amount is M_A, its age is the tick) equals the record's push,
    every record compared and none unequal (the count, not pinned, is the
    register's 181 per world and 185 in `7_pp_m4`);
(b) a third column with the sign minus gives the design's integers (the
    physicist's DESIGN.md, test (a)): the families `a` (charge [1, 2],
    strong [3, 2]) and `b` (charge 2, strong 1) under `"strong": {"sign":
    -1}`; a reader of `a`, amount 1 (M 1, Q 1/2, G 3/2), met by one ray of
    `b` of amount 1 arriving on (1, 1, 0) (u = (45, 45, 0)) reads the push
    (-67, -67, 0) at an even age and (-68, -68, 0) at an odd one (gravity
    -45, charge +45, strong -by_clock(age, 135, 2)): two rays, one at
    (2, 1, 0) with age 1 arriving at tick 1 (the reader's age 1) and one at
    (1, 1, 0) with age 3 arriving at tick 2 (age 2), read -68 then -67; a
    reader of `c` (charge 1, strong [4, 3]) of amount 6 (M 6, Q 6, G 8,
    the charges of the held reader of `tests/test_lifetime.py`): a `b` ray
    of amount 1 on +x gives (-128, 0, 0) (-384 + 768 - 512), an `a` ray of
    amount 1 on +x (-960, 0, 0) (-384 + 192 - 768), an `a` ray of amount 3
    on -x (2880, 0, 0); a reader with no strong value (`d`, charge 0)
    reading a `b` ray on +x: gravity alone, (-64, 0, 0). The sign is a
    key: the same worlds with `"strong": {"sign": 1}` read (+67, +67, 0)
    at the even age and (+68, +68, 0) at the odd one, and (896, 0, 0) for
    the reader of `c`. A third declared column (`"extra": {"sign": 1}`,
    the value 1 on `a` and on `b`) adds +by_clock(age, 45 x 1 x 1, 1) =
    +45 per axis to the first case: -23 at the odd age, -22 at the even.
    A world without a declared column reads the parity case of the
    landed form: a reader of `q` (charge [1, 2]) of content 3 met by a
    `b` ray on (1, 1, 0) reads (0, 0, 0) at both ages (-135 + 135). The
    symmetric form: two fixed bodies at mirror Nodes on a bar, `p` (content
    3) and `q` (content 5) with the charge [1, 3] and the strong value
    [2, 3] on both families, releasing at `release` [1, 1] toward each
    other, read equal and opposite pushes at every tick (the same
    rationals floored at the same age: 320 x 1 / 3 and 320 x 4 / 3 on
    `p`, 192 x 5 / 9 and 192 x 20 / 9 on `q`), and the run's record carries
    the world's columns, every family's aligned columns and the identity
    `columns-v1` under `hypotheses` (with `bohr-v1` first when `action` is
    declared; `[]` and the two built-in columns without a declared one);
(c) the refusals, naming the key: a `sign` 0, 2, "-1" or true; a column
    named `gravity`; `charge` declared both as the key and under
    `columns`; `columns.charge` with the sign -1 (accepted with 1: the
    value is the family's charge); a nonzero value on a paid family (0
    accepted); one name with two signs on two families; a value [1, 0],
    1.5 or "1/2"; a column object with another key or without `sign`;
    `columns` that is not an object; seven declared columns (nine in
    all, beyond the eight allowed); a family without a declared column
    carries [0, 1] there, and the world's order is gravity, charge, then
    the names in the order of their first declaration;
(d) the bounds: at parsing, a reader of content 2^40 met by a family of
    the strong value 2^20 on both (|E n| = 2^80) is refused naming the
    column `strong` and the family; two columns each within the bound
    but together beyond it (a reader of content 2^30 and the strong value
    1 met by a family of content 2^25 released on one heading at
    `release` [1, 1]: gravity 2^30 x 2^31 = 2^61, strong the same, the sum
    2^62 + 2) are refused before any push is formed, naming the sum; at
    run time `push_form` refuses the product |V| x |E n| = 64 x 2^56 =
    2^62 in the column `strong` before it is formed and the partial sum
    of two columns of 2^62 - 128 each beyond the bound naming the push;
(e) the order of flooring, the mathematician's counterexample: a reader of
    content 1 met by one free unit on a heading (V = 64), rho_A = [1, 3],
    rho_B = [1, 1]: per column (the decided form) -64 + by_clock(age, 64,
    3) = -43, -43, -42, -43 at the ages 0, 1, 2, 3; the sum -128 / 3
    floored once would give -42, -43, -43, -42; on the engine the reader's
    ages 1 .. 4 read -43, -42, -43, -43.
"""

from __future__ import annotations

import itertools
import json
import random
from fractions import Fraction
from pathlib import Path
from types import SimpleNamespace

import pytest

from event_universe.core.integer import by_clock
from event_universe.events import RaySimulation, parse_ray_world
from event_universe.events.measured import column_charges
from event_universe.events.nature_beam import push_form
from event_universe.events.world import COLUMNS_RULE, MOMENTUM_BOUND, Column
from event_universe.runner import run_initialization

ROOT = Path(__file__).resolve().parents[1]
GRAVITY = ("gravity", -1)
CHARGE = ("charge", 1)
ENTRY = SimpleNamespace(number=1, position=(2, 2, 0))
DIAGONAL = [1, 1, 0]
PLUS_X = [1, 0, 0]
MINUS_X = [-1, 0, 0]
Charge = int | list[int]


# -- the landed form, the reference of (a) ----------------------------------------


def landed_bounded(value: int) -> int:
    if not -MOMENTUM_BOUND <= value <= MOMENTUM_BOUND:
        raise OverflowError("refused")
    return value


def landed_push_form(
    free: bool,
    moment: list[int],
    content: int,
    reader: tuple[int, int],
    emitter: tuple[int, int],
    age: int,
) -> list[int]:
    """`nature_beam.push_form` as landed on 2026-09-20 (the charge per unit
    of content): the gravity -M_A V plus the electric part off the
    reader's clock by the declared pairs, its products bounded."""
    if not free:
        return [landed_bounded(v) for v in moment]
    push = [landed_bounded(-moment[axis] * content) for axis in range(3)]
    n_a, d_a = reader
    n_b, d_b = emitter
    if n_a and n_b:
        denominator = d_a * d_b
        for axis in range(3):
            total = landed_bounded(moment[axis] * n_a * n_b * content)
            whole = by_clock(age, abs(total), denominator)
            push[axis] = landed_bounded(push[axis] + (-whole if total < 0 else whole))
    return push


def two_columns(
    free: bool,
    moment: list[int],
    content: int,
    reader: tuple[int, int],
    emitter: tuple[int, int],
    age: int,
    *,
    reduce: bool = True,
) -> list[int]:
    """The engine's form with the two built-in columns: the reader's
    charges (M_A, 1) and rho_A x M_A as the frame reads them from what it
    holds (`column_charges`, the reduced pair; a charge beyond the
    register refuses), or the same rational unreduced, the emitter's
    values (1, 1) and rho_B."""
    if not free:
        # A paid family carries no charge: the frame reads (M, 1) and (0, 1).
        charges = [(content, 1), (0, 1)]
    elif reduce:
        charges = column_charges([(((1, 1), reader), content)], 2, 1, ENTRY.position)
    else:
        charges = [(content, 1), (reader[0] * content, reader[1])]
    return push_form(free, list(moment), charges, ((1, 1), emitter), (GRAVITY, CHARGE), age, ENTRY)


def outcome(form, *arguments, **keys) -> object:
    try:
        return form(*arguments, **keys)
    except OverflowError:
        return "refused"


def test_the_two_built_in_columns_are_the_landed_form_integer_by_integer():
    """(a), the grid and the register's scale."""
    total = 0
    for v, m, n_a, n_b, d_a, d_b, age in itertools.product(
        range(-5, 6), range(4), range(-2, 3), range(-2, 3), range(1, 4), range(1, 4), range(5)
    ):
        moment = [v, -v, 2 * v + 1]
        expected = landed_push_form(True, moment, m, (n_a, d_a), (n_b, d_b), age)
        assert two_columns(True, moment, m, (n_a, d_a), (n_b, d_b), age) == expected
        assert two_columns(True, moment, m, (n_a, d_a), (n_b, d_b), age, reduce=False) == expected
        total += 1
    assert total == 49500
    rng = random.Random(20260920)
    refused = beyond = 0
    for _ in range(3000):
        moment = [rng.choice([-1, 1]) * rng.randrange(0, 1 << rng.randrange(1, 63)) for _ in range(3)]
        m = rng.randrange(0, 1 << rng.randrange(1, 41))
        n_a = rng.choice([-1, 0, 1]) * rng.randrange(1, 1 << rng.randrange(1, 31))
        n_b = rng.choice([-1, 0, 1]) * rng.randrange(1, 1 << rng.randrange(1, 31))
        d_a, d_b = (
            rng.randrange(1, 1 << rng.randrange(1, 31)),
            rng.randrange(1, 1 << rng.randrange(1, 31)),
        )
        age = rng.randrange(0, 1 << 31)
        free = rng.random() < 0.9
        expected = outcome(landed_push_form, free, list(moment), m, (n_a, d_a), (n_b, d_b), age)
        # The unreduced pair forms the landed product exactly, so the two
        # forms refuse together; the reduced pair, the frame's, refuses
        # at most where the landed form refused and never elsewhere.
        assert (
            outcome(two_columns, free, moment, m, (n_a, d_a), (n_b, d_b), age, reduce=False) == expected
        )
        found = outcome(two_columns, free, moment, m, (n_a, d_a), (n_b, d_b), age)
        # The frame's reduced pair refuses a charge rho_A M_A beyond the
        # register on its own (the landed form never formed it alone) and
        # otherwise at most where the landed form refused, never elsewhere,
        # with the same integers where both accept.
        if free and m and abs(n_a) > MOMENTUM_BOUND // m:
            assert found == "refused"
            beyond += 1
        else:
            assert found == expected or (expected == "refused" and found != "refused")
        refused += expected == "refused"
    assert 0 < beyond < refused < 3000
    assert push_form(False, [5, -7, 9], [], (), (), 3, ENTRY) == [5, -7, 9]


def test_the_series_7_read_records_replay_under_the_landed_form():
    """(a), the replay from the record alone: every `read` record's push of
    the six series 7 worlds equals the landed two-column form recomputed
    from the record and the world file (no wrapper in the engine)."""
    compared = equal = 0
    for path in sorted((ROOT / "examples" / "events" / "coupling").glob("7_*.json")):
        document = json.loads(path.read_text(encoding="utf-8"))
        world = parse_ray_world(document)
        assert world.suspension[0] == 0 and world.declared_columns == ()
        records: list[dict[str, object]] = []
        simulation = RaySimulation(world, records.append)
        for _ in range(world.ticks):
            simulation.step()
        family_of = {family.name: family for family in world.families}
        for event in records:
            if event["event"] != "read":
                continue
            reader = world.measured[int(str(event["measured"])) - 1]
            assert reader.fixed
            arriving = family_of[str(event["family"])]
            push = landed_push_form(
                True,
                [int(v) for v in event["reading"]],  # type: ignore[union-attr]
                reader.amount,
                world.families[reader.family].charge,
                arriving.charge,
                int(str(event["tick"])),
            )
            compared += 1
            equal += push == event["push"]
    assert compared == equal > 0


# -- the worlds of (b) ----------------------------------------------------------------


def family(
    name: str, charge: Charge | None = 0, columns: dict[str, object] | None = None
) -> dict[str, object]:
    """A free family without a phase circle; `charge` None leaves the key out."""
    found: dict[str, object] = {"name": name, "quantum": 0, "phase": False}
    if charge is not None:
        found["charge"] = charge
    if columns is not None:
        found["columns"] = columns
    return found


def strong(value: Charge, sign: int = -1) -> dict[str, object]:
    return {"value": value, "sign": sign}


def families(sign: int = -1, extra: bool = False) -> list[dict[str, object]]:
    a = family("a", [1, 2], {"strong": strong([3, 2], sign)})
    b = family("b", 2, {"strong": strong(1, sign)})
    if extra:
        a["columns"]["extra"] = {"value": 1, "sign": 1}  # type: ignore[index]
        b["columns"]["extra"] = {"value": 1, "sign": 1}  # type: ignore[index]
    return [a, b, family("c", 1, {"strong": strong([4, 3], sign)}), family("d"), family("q", [1, 2])]


def world(
    reader: str,
    amount: int,
    rays: list[dict[str, object]],
    *,
    sign: int = -1,
    extra: bool = False,
    ticks: int = 2,
    **keys: object,
) -> dict[str, object]:
    document: dict[str, object] = {
        "law": "rays",
        "model_id": "columns-test",
        "shape": [5, 5, 1],
        "boundary": {"z": "periodic"},
        "ticks": ticks,
        "K": 1 << 20,
        "N": 64,
        "release": [0, 1],
        "suspension": 0,
        "directions": [DIAGONAL],
        "families": families(sign, extra),
        "measured": [
            {"position": [2, 2, 0], "family": reader, "amount": amount, "fixed": True},
            {"position": [0, 4, 0], "family": "b", "amount": 1, "fixed": True},
        ],
        "in_transit": rays,
    }
    document.update(keys)
    return document


def ray(
    position: list[int], name: str, direction: list[int], amount: int = 1, age: int = 0
) -> dict[str, object]:
    return {
        "position": position,
        "family": name,
        "number": 2,
        "direction": direction,
        "amount": amount,
        "phase": 0,
        "age": age,
    }


def pushes(document: dict[str, object]) -> list[tuple[int, list[int]]]:
    records: list[dict[str, object]] = []
    simulation = RaySimulation(parse_ray_world(document), records.append)
    for _ in range(int(str(document["ticks"]))):
        simulation.step()
        assert simulation.books()["balanced"]
    return [
        (int(str(r["tick"])), list(r["push"]))
        for r in records
        if r["event"] == "read" and r["measured"] == 1
    ]  # type: ignore[arg-type]


PARITY = [ray([2, 1, 0], "b", DIAGONAL, age=1), ray([1, 1, 0], "b", DIAGONAL, age=3)]


def test_a_third_column_with_the_sign_minus_gives_the_designs_integers():
    """(b)."""
    assert pushes(world("a", 1, PARITY)) == [(1, [-68, -68, 0]), (2, [-67, -67, 0])]
    assert pushes(world("a", 1, PARITY, sign=1)) == [(1, [68, 68, 0]), (2, [67, 67, 0])]
    assert pushes(world("a", 1, PARITY, extra=True)) == [(1, [-23, -23, 0]), (2, [-22, -22, 0])]
    assert pushes(world("q", 3, PARITY)) == [(1, [0, 0, 0]), (2, [0, 0, 0])]
    for name, direction, position, amount, push, plus in (
        ("b", PLUS_X, [1, 2, 0], 1, [-128, 0, 0], [896, 0, 0]),
        ("a", PLUS_X, [1, 2, 0], 1, [-960, 0, 0], [576, 0, 0]),
        ("a", MINUS_X, [3, 2, 0], 3, [2880, 0, 0], [-1728, 0, 0]),
    ):
        assert pushes(world("c", 6, [ray(position, name, direction, amount)], ticks=1)) == [(1, push)]
        assert pushes(world("c", 6, [ray(position, name, direction, amount)], ticks=1, sign=1)) == [
            (1, plus)
        ]
    assert pushes(world("d", 1, [ray([1, 2, 0], "b", PLUS_X)], ticks=1)) == [(1, [-64, 0, 0])]
    simulation = RaySimulation(parse_ray_world(world("c", 6, [])))
    assert simulation.measured[1].charges() == [(6, 1), (6, 1), (8, 1)]
    assert simulation.measured[1].state()["charges"] == {
        "gravity": [6, 1],
        "charge": [6, 1],
        "strong": [8, 1],
    }
    assert simulation.world.columns == (GRAVITY, CHARGE, ("strong", -1))


def test_two_bodies_at_mirror_nodes_read_equal_and_opposite_pushes(tmp_path):
    """(b), the symmetric form and the record."""
    document = {
        "law": "rays",
        "model_id": "columns-mirror-test",
        "shape": [4, 1, 1],
        "boundary": {"y": "periodic", "z": "periodic"},
        "ticks": 12,
        "K": 1 << 20,
        "N": 64,
        "release": [1, 1],
        "suspension": 0,
        "families": [
            family("p", [1, 3], {"strong": strong([2, 3])}),
            family("q", [1, 3], {"strong": strong([2, 3])}),
        ],
        "measured": [
            {"position": [0, 0, 0], "family": "p", "amount": 3, "fixed": True, "directions": [PLUS_X]},
            {"position": [3, 0, 0], "family": "q", "amount": 5, "fixed": True, "directions": [MINUS_X]},
        ],
    }
    records: list[dict[str, object]] = []
    simulation = RaySimulation(parse_ray_world(document), records.append)
    for _ in range(12):
        simulation.step()
        assert simulation.books()["balanced"]
    on_p = {r["tick"]: r["push"] for r in records if r["event"] == "read" and r["measured"] == 1}
    on_q = {r["tick"]: r["push"] for r in records if r["event"] == "read" and r["measured"] == 2}
    assert sorted(on_p) == sorted(on_q) == list(range(6, 13))
    for tick in on_p:
        push = on_p[tick]
        assert push == [-v for v in on_q[tick]] and push[0] > 0 and push[1:] == [0, 0]  # type: ignore[union-attr]
        # p: gravity 3 x 320 = 960, charge -(320 / 3 floored), strong +(1280 / 3 floored).
        assert push[0] == 960 - by_clock(tick, 320, 3) + by_clock(tick, 1280, 3)  # type: ignore[index]
    assert simulation.measured[1].pushed == [-v for v in simulation.measured[2].pushed]
    path = tmp_path / "world.json"
    path.write_text(json.dumps({**document, "ticks": 1}), encoding="utf-8")
    record = json.loads(run_initialization(path, tmp_path / "run").read_text(encoding="utf-8"))
    assert record["hypotheses"] == [COLUMNS_RULE] and record["status"] == "completed"
    assert record["columns"] == [
        {"name": "gravity", "sign": -1},
        {"name": "charge", "sign": 1},
        {"name": "strong", "sign": -1},
    ]
    assert record["families"][1]["columns"] == [
        {"name": "gravity", "value": [1, 1], "sign": -1},
        {"name": "charge", "value": [1, 3], "sign": 1},
        {"name": "strong", "value": [2, 3], "sign": -1},
    ]
    assert record["measured"][0]["charges"] == {"gravity": [3, 1], "charge": [1, 1], "strong": [2, 1]}
    plain = {**document, "ticks": 1, "families": [family("p", [1, 3]), family("q")]}
    path.write_text(json.dumps(plain), encoding="utf-8")
    record = json.loads(run_initialization(path, tmp_path / "plain").read_text(encoding="utf-8"))
    assert record["hypotheses"] == [] and len(record["columns"]) == 2
    both = parse_ray_world({**document, "action": 64})
    assert both.hypotheses == ["bohr-v1", COLUMNS_RULE]


# -- (c) ---------------------------------------------------------------------------


def refused(document: dict[str, object], text: str) -> None:
    with pytest.raises(ValueError, match=text):
        parse_ray_world(document)


def test_the_refusals_and_the_alignment():
    """(c)."""
    base = world("a", 1, [])

    def with_families(*declared: dict[str, object]) -> dict[str, object]:
        reader = {"position": [2, 2, 0], "family": "b", "amount": 1, "fixed": True}
        return {**base, "families": [*declared, family("b", 2)], "measured": [reader]}

    for sign in (0, 2, "-1", True):
        refused(with_families(family("a", 0, {"s": {"value": 1, "sign": sign}})), "sign must be 1")
    refused(with_families(family("a", 0, {"gravity": strong(1)})), "built-in column 'gravity'")
    refused(
        with_families(family("a", 1, {"charge": {"value": 1, "sign": 1}})),
        "declare the column 'charge' twice",
    )
    refused(
        with_families(family("a", None, {"charge": {"value": 1, "sign": -1}})),
        "columns\\['charge'\\].sign must be 1",
    )
    shorthand = parse_ray_world(
        with_families(family("a", None, {"charge": {"value": [3, 4], "sign": 1}}))
    )
    assert shorthand.families[0].charge == (3, 4) and shorthand.columns == (GRAVITY, CHARGE)
    paid = {"name": "light", "quantum": 1, "columns": {"s": strong(1)}}
    refused(
        with_families(paid),
        "a paid family \\(quantum 1\\) carries no column value \\(light, the column 's'",
    )
    zero = parse_ray_world(with_families({**paid, "columns": {"s": strong(0)}}))
    assert zero.families[0].values == ((1, 1), (0, 1), (0, 1))
    refused(
        with_families(family("a", 0, {"s": strong(1, -1)}), family("e", 0, {"s": strong(1, 1)})),
        "families\\[1\\].columns\\['s'\\].sign 1 differs from the sign -1 families\\[0\\] declared",
    )
    for value, text in (
        ([1, 0], "columns\\['s'\\].value denominator must be an integer from 1"),
        (1.5, "columns\\['s'\\].value must be an integer"),
        ("1/2", "columns\\['s'\\].value must be an integer or \\[numerator, denominator\\]"),
    ):
        refused(with_families(family("a", 0, {"s": strong(value)})), text)
    refused(
        with_families(family("a", 0, {"s": {"value": 1, "sign": 1, "range": 3}})), "unknown keys: range"
    )
    refused(with_families(family("a", 0, {"s": {"value": 1}})), "lacks keys: sign")
    refused(with_families({**family("a"), "columns": [1]}), "columns must be an object of column name")
    many = {f"c{k}": strong(1) for k in range(7)}
    refused(
        with_families(family("a", 0, many)), "declares 7 columns beyond gravity and charge; at most 8"
    )
    # The alignment: a family without a column carries [0, 1] there; the
    # order is gravity, charge, then the names as first declared.
    parsed = parse_ray_world(
        with_families(
            family("a", 0, {"s": strong(1), "t": {"value": [2, 5], "sign": 1}}),
            family("e", 0, {"t": strong([1, 7], 1)}),
        )
    )
    assert parsed.columns == (GRAVITY, CHARGE, ("s", -1), ("t", 1)) and parsed.declared_columns == (
        "s",
        "t",
    )
    assert parsed.families[1].columns == (
        Column("gravity", (1, 1), -1),
        Column("charge", (0, 1), 1),
        Column("s", (0, 1), -1),
        Column("t", (1, 7), 1),
    )
    assert parsed.families[2].values == ((1, 1), (2, 1), (0, 1), (0, 1))


# -- (d) ---------------------------------------------------------------------------


def test_the_bounds_at_parsing_and_at_the_push():
    """(d)."""
    big = {
        **world("a", 1, []),
        "shape": [4, 1, 1],
        "boundary": {"y": "periodic", "z": "periodic"},
        "release": [1, 1],
        "directions": [],
        "families": [
            family("a", 0, {"strong": strong(1 << 20)}),
            family("b", 0, {"strong": strong(1 << 20)}),
        ],
        "measured": [
            {
                "position": [0, 0, 0],
                "family": "a",
                "amount": 1 << 40,
                "fixed": True,
                "directions": [PLUS_X],
            },
            {"position": [3, 0, 0], "family": "b", "amount": 1, "fixed": True, "directions": [MINUS_X]},
        ],
    }
    refused(big, "measured\\[0\\]: the push over the column 'strong' from the rays of the family 'b'")
    together = {
        **big,
        "families": [family("a", 0, {"strong": strong(1)}), family("b", 0, {"strong": strong(1)})],
        "measured": [
            {
                "position": [0, 0, 0],
                "family": "a",
                "amount": 1 << 30,
                "fixed": True,
                "directions": [PLUS_X],
            },
            {
                "position": [3, 0, 0],
                "family": "b",
                "amount": 1 << 25,
                "fixed": True,
                "directions": [MINUS_X],
            },
        ],
    }
    refused(
        together,
        f"the pushes over the 3 columns from the rays of the family 'b' could sum to {(1 << 62) + 2}",
    )
    apart = {**together, "families": [family("a", 0, {"strong": strong(1)}), family("b")]}
    assert parse_ray_world(apart).declared_columns == ("strong",)
    columns = (GRAVITY, CHARGE, ("strong", -1))
    with pytest.raises(
        OverflowError, match="the push of measured event 1 at \\[2, 2, 0\\] .* in the column 'strong'"
    ):
        push_form(
            True, [64, 0, 0], [(1, 1), (0, 1), (1 << 56, 1)], ((1, 1), (0, 1), (1, 1)), columns, 0, ENTRY
        )
    within = (1 << 56) - 2
    assert push_form(
        True, [64, 0, 0], [(within, 1), (0, 1), (0, 1)], ((1, 1), (0, 1), (1, 1)), columns, 0, ENTRY
    ) == [
        -(within * 64),
        0,
        0,
    ]
    with pytest.raises(
        OverflowError, match="the push of measured event 1 at \\[2, 2, 0\\] exceeds the integer bound"
    ):
        push_form(
            True,
            [64, 0, 0],
            [(within, 1), (0, 1), (within, 1)],
            ((1, 1), (0, 1), (1, 1)),
            columns,
            0,
            ENTRY,
        )


# -- (e) ---------------------------------------------------------------------------


def summed_then_floored(moment: int, content: int, terms: list[tuple[int, Fraction]], age: int) -> int:
    """The rejected alternative: the columns' rationals summed, one whole
    part off the clock with the sign restored."""
    kappa = sum((Fraction(sign) * value for sign, value in terms), Fraction(0))
    total = moment * content * kappa
    whole = by_clock(age, abs(total.numerator), total.denominator)
    return whole if total > 0 else -whole


def test_every_column_is_floored_on_its_own():
    """(e)."""
    per_column = [two_columns(True, [64, 0, 0], 1, (1, 3), (1, 1), age)[0] for age in range(4)]
    assert per_column == [-43, -43, -42, -43]
    assert per_column == [-64 + by_clock(age, 64, 3) for age in range(4)]
    summed = [
        summed_then_floored(64, 1, [(-1, Fraction(1)), (1, Fraction(1, 3))], age) for age in range(4)
    ]
    assert summed == [-42, -43, -43, -42] and summed != per_column
    document = {
        **world("a", 1, [], ticks=4),
        "families": [family("r", [1, 3]), family("b", 1)],
        "measured": [
            {"position": [2, 2, 0], "family": "r", "amount": 1, "fixed": True},
            {"position": [0, 4, 0], "family": "b", "amount": 1, "fixed": True},
        ],
        "in_transit": [ray([x, 2, 0], "b", PLUS_X, age=a) for x in (1, 0) for a in (0, 1)],
    }
    found = {tick: push[0] for tick, push in pushes(document)}
    assert found == {1: -43, 2: -42, 3: -43, 4: -43}
