"""The fraction-free law (2026-09-20; BEAM_LAW note 41; the mathematician's
docs/designs/fraction_free/FORM.md, sections 1, 4, 6 and 7): every count of a
body is `core.integer.by_drive` on one accumulator of the body's own record,
the remainder's owner, below the count's denominator after every
self-creation, nothing at a Node; `by_clock` off the age is its constant-rate
identity. The expected integers of docs/TEST_EXPECTATIONS.md ("The
fraction-free counts"), written down first:

(a) the identity at a constant rate over 10^4 self-creations: the primitive
    on seven rates from 1 / 3 to a star's 9 736 000 000 000 /
    290 000 000 000 000 gains `by_clock(k - 1, n, d)` at the k-th
    self-creation from an empty accumulator and holds `(k n) mod d` after
    it (FORM.md section 1); on the engine, every count on its own body over
    10^4 intervals: the release of a fixed source of content 3 at `release`
    [1, 10] on +X (`acc_release` = 3 x age mod 10, the units released
    floor(3 x age / 10), 3000 after 10^4), the turn of a fixed body of
    content 3 at K = [3, 8] (`acc_turn` = 9 x age mod 8, `turned` floor(9
    x age / 8) = 11250 after 10^4), the drive of a free body of content 16
    at momentum 1 and `width` 8 (D = 8193: one Link at the self-creation
    8193, the drive 10^4 - 8193 = 1807 after), the owed count of a fixed
    probe measuring one unit per interval at `suspension` [1, 4]
    (`acc_owed` = age mod 4, the probe's age 8000 and 2000 intervals
    waited after 10^4; the probe a paid body of `light`, so it releases
    nothing back at the lamp) and a lamp's rate [1, 3] (`acc_lamp` = age
    mod 3, one unit born at every third self-creation, 3333 after 10^4);
(b) the sum over a period equal to the whole part of the sum of the
    numerators on a varying flow (stage 2, the push): `tests/test_doppler.py`
    (b), the bar as posed with rows of 64 (396672 exactly over 200 reads,
    the remainder on the body's flow accumulator below G Q at every tick;
    396673 off the clock), and `tests/test_nature_beam_push.py` (k), the
    charge accumulator at Lambda = 20 (1177 = floor(23 x 1280 / 25) over
    the 23 reads, 1178 off the clock from the age 7);
(c) the accumulators carried in `state.json` (and `run.json`) under `acc`
    by name, `owed`, `release` (per family), `lamp`, `turn`, `push` per
    column (the three axes, 0 on the built-in columns of whole charges),
    beside `drive`, `flow` per direction under `doppler` alone: on a bar
    of a source of `m` (content 3, 3 units per
    self-creation on +X), a probe of `light` (content 1) measuring them
    at `suspension` [1, 4], a turning body of `light` (content 3, K = [3,
    8]) and a mover of `light` (content 16, momentum 1000, `width` 8),
    after 20 intervals the probe's `acc` is {owed 1, turn 4} (eleven
    self-creations reading 3, 33 = 8 x 4 + 1, eight intervals waited, the
    age 12; the turn's 3 x 12 mod 8), the turner's {turn 4} (9 x 20 mod
    8), the mover's {turn 0} (48 x 20 mod 8) with the drive 1616 (20 x
    1000 mod 9192) and 2 Links; a run resumed from that `state.json`
    identical to the unbroken one at every one of the ticks 21 to 40 in
    every measured event's state and in every record; resumed with the
    accumulators emptied at that age it differs (FORM.md section 1 (i):
    the phase of every count at the age is the accumulator); the runner
    writes `acc` in both files; a declared `acc` on a measured event is
    refused as an unknown key;
(d) the per-direction split equal to the whole on a fan at rest:
    `tests/test_doppler.py` (f), the fan reader at rest under the key
    reads the same records as without it and its flow accumulators stay
    0; at w_y = 1 the third read's count is each direction's whole part
    from the empty accumulator (9787 on y; 9788 off the clock at age 2);
(e) the bound: on the worlds of (a), at every tick, `acc_owed` below 4,
    `acc_release` below 10, `acc_lamp` below 3, `acc_turn` below 8 and the
    drive's magnitude below D = Q x S x M + |p|; the push's accumulators
    below Lambda_c^2 and the flow's below G Q |v_d|^2 at every tick
    (`test_doppler` (b) and (f), `test_nature_beam_push` (k)); the
    primitive on 10^4 random rates below the denominator keeps an unsigned
    accumulator in [0, d) and a signed one in (-d, d), with `at_most` 1
    and without;
(f) the ladder at the click as the comparison of products
    (`amplitude.cell_of`, the first k with 2 T u + T <= 2 N C_k) equals
    the rungs' cell (`choose` on `rungs`) for every u on 2000 random
    ladders (up to 8 cells, weights up to 2^20 over multiplicities up to
    64, N 64 and 256; an empty ladder None) and on every gather of
    `mz_equal`, `mz_345`, `bell_0_8` and `slits_low` (the chosen cell's
    index in the gather's `cells` the comparison's);
(g) the bound of the push's denominator at load (the physics-rule review of
    the branch, docs/designs/fraction_free/REVIEW.md section 4): a world
    whose column scale Lambda_c (`world.column_scales`, the least common
    multiple of the families' value denominators in the column) has a
    square beyond the integer bound 2^62 - 1 is refused at the parse
    naming the column and the bound, before any body's table is formed;
    the run's refusal of the lifted product (`test_columns` (a)) stands
    beside it. The ceiling of Lambda_c is 2^31 - 1 = 2147483647, the
    integer root of the bound, a prime beyond one value's bound 2^30 - 1:
    the free families `m` at the value [1, 2] and `w` at [1, 2^30 - 1] in
    the column `s` load with Lambda_c = 2^31 - 2 = 2147483646, the largest
    two declared values can form under the ceiling (its square 2^62 -
    2^33 + 4, below the bound by 8589934587); `m` at [1, 2^30 - 1] alone
    loads with Lambda_c = 2^30 - 1; `m` at [1, 3] and `w` at [1,
    715827883] (3 x 715827883 = 2^31 + 1, the smallest two values can
    form above the ceiling) are refused with Lambda_c = 2147483649 (its
    square above the bound by 2^32 + 1);
(h) no remainder discarded at run time (the model owner's record 155 of
    2026-09-20; note 41 (viii)): a record row's push on a body keeps its
    remainder on the row (`share_of` with the row's accumulator, the
    columns `share_x/y/z`): on random labels, amounts and multiplicities
    the shares of a row pushed k times sum to the whole part of k x label
    x amount over m exactly and the accumulator stays below m in
    magnitude, where the floor per push alone falls short by up to k - 1
    units; on a bar of a lamp of records (K 2^20, content 2^20, one row
    per birth on +x, +y and +z, the two last leaving through the open
    faces at once) and four fixed readers of a paid family at
    x = 4 .. 7 reading `light` with the rule `read` over 30 intervals
    (three rows per record, m = 3, the +x row's label 64 leaving the
    remainder 1 per read), every row at a reader carries its accumulator
    below m, the readers' pushes are the sum of the read lines' pushes,
    and that sum is strictly between 21 and 22 units per unit read (the
    carried remainders delivered as the 22nd unit every third read; the
    floor alone gives 21); the run's state writes `share` on a row that
    holds one;
(i) a set's release over its Nodes (`place_over_nodes`): on random
    amounts over 2 to 7 Nodes, every placement sums to the amount, the
    claims sum to zero and stay within the number of Nodes, and after every
    row every Node is within one unit of its equal share of everything
    placed so far; the rows of `test_nature_beam_body` (c) re-pinned (6, 5,
    5 and 5, 6, 5 for 8, 4, 4 and 4, 8, 4; the lamp on a set at x = 1 for
    x = 2).
"""

from __future__ import annotations

import importlib.util
import io
import json
import random
import sys
from pathlib import Path

import numpy as np
import pytest

from event_universe.core.game_board import MAX_VALUE
from event_universe.core.integer import by_clock, by_drive
from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.amplitude import cell_of, choose, rungs
from event_universe.events.engine import count_owed, step_axis
from event_universe.events.measured import CountTable, counts_table
from event_universe.events.nature_beam import NO_ARRIVAL, place_over_nodes, share_of
from event_universe.events.run import execute_nature_beam_run
from event_universe.events.world import LABEL_SCALE, MOMENTUM_BOUND, body_nodes
from event_universe.snapshot_writer import write_snapshot

ROOT = Path(__file__).resolve().parents[1]
Q = LABEL_SCALE
INTERVALS = 10_000
RATES = [
    (1, 3),
    (3, 10),
    (7, 3),
    (32, 55),
    (100, 82),
    (1024, 8193),
    (9_736_000_000_000, 290_000_000_000_000),
]


def bar(measured: list[dict[str, object]], **keys: object) -> dict[str, object]:
    world: dict[str, object] = {
        "law": "beam",
        "model_id": "fraction-free-test",
        "shape": [4, 1, 1],
        "boundary": {"y": "periodic", "z": "periodic"},
        "ticks": 40,
        "K": [3, 8],
        "N": 64,
        "release": [1, 10],
        "suspension": [1, 4],
        "width": 8,
        "families": [{"name": "m", "quantum": 0, "phase": False}, {"name": "light", "quantum": 1}],
        "measured": measured,
    }
    world.update(keys)
    return world


M, LIGHT = 0, 1
SOURCE = {"position": [3, 0, 0], "family": "m", "amount": 3, "fixed": True, "directions": [[1, 0, 0]]}
TURNER = {"position": [0, 0, 0], "family": "light", "amount": 3, "fixed": True}
MOVER = {"position": [1, 0, 0], "family": "light", "amount": 16, "momentum": [1, 0, 0]}


def counting_world() -> dict[str, object]:
    """A lamp of `light` (content 2^21 at K 2^20, the turn 2 then 1 or 2,
    never 0) at x = 0 releasing one unit per self-creation on +X, with one
    declared unit of its number already on the way, a probe of `light`
    (content 1, a paid body: it releases nothing back at the lamp) at x =
    1 measuring `light` (the presence 1 at every self-creation from the
    first), and a second lamp at rate [1, 3] at x = 2 releasing on +X
    toward the open face."""
    lamp = {
        "position": [0, 0, 0],
        "family": "light",
        "amount": 1 << 21,
        "fixed": True,
        "lamp": {"rate": [1, 1], "directions": [[1, 0, 0]]},
    }
    probe = {
        "position": [1, 0, 0],
        "family": "light",
        "amount": 1,
        "fixed": True,
        "table": {"light": "measure"},
    }
    thirds = {
        "position": [2, 0, 0],
        "family": "light",
        "amount": 1 << 21,
        "fixed": True,
        "lamp": {"rate": [1, 3], "directions": [[1, 0, 0]]},
    }
    declared = {
        "position": [0, 0, 0],
        "family": "light",
        "number": 1,
        "direction": [1, 0, 0],
        "amount": 1,
        "phase": 0,
    }
    return bar([lamp, probe, thirds], K=1 << 20, in_transit=[declared])


# -- (a) ---------------------------------------------------------------------------


@pytest.mark.parametrize(("numerator", "denominator"), RATES)
def test_the_primitive_at_a_constant_rate_is_by_clock_with_the_remainder_kept(numerator, denominator):
    """(a), the primitive."""
    accumulator = 0
    for k in range(1, INTERVALS + 1):
        count, accumulator = by_drive(accumulator, numerator, denominator)
        assert count == by_clock(k - 1, numerator, denominator), k
        assert accumulator == (k * numerator) % denominator, k


def test_every_count_of_a_body_at_a_constant_rate_is_the_count_off_the_clock():
    """(a), the engine: the release, the turn and the drive on one bar."""
    simulation = NatureBeamSimulation(parse_nature_beam_world(bar([SOURCE, TURNER, MOVER])))
    source, turner, mover = (simulation.measured[n] for n in (1, 2, 3))
    reach = Q * 8 * 16 + 1
    for tick in range(1, INTERVALS + 1):
        simulation.step()
        assert simulation.books()["balanced"], tick
        # The release: the source's age is the tick (it owes nothing).
        assert source.age == tick and source.acc_release[M] == (3 * tick) % 10, tick
        assert simulation.ledger.transit_released[M] == (3 * tick) // 10, tick
        # The turn at [3, 8] on the content 3: the rate 9 over 8.
        assert turner.age == tick and turner.acc_turn == (9 * tick) % 8, tick
        assert turner.turned == (9 * tick) // 8, tick
        # The drive at the momentum 1: D = 8193, one Link at 8193.
        assert mover.age == tick and mover.drive == [tick % reach, 0, 0], tick
        assert mover.steps == tick // reach and mover.position == (1 + tick // reach, 0, 0), tick
    assert simulation.ledger.transit_released[M] == 3000 and turner.turned == 11250
    assert mover.steps == 1 and mover.drive == [1807, 0, 0]


def test_the_owed_count_and_the_lamps_rate_at_a_constant_rate_are_the_counts_off_the_clock():
    """(a), the engine: the owed count under a constant presence and a
    lamp's rate."""
    records: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(counting_world()), records.append)
    probe, thirds = simulation.measured[2], simulation.measured[3]
    owed_at: list[int] = []
    for tick in range(1, INTERVALS + 1):
        simulation.step()
        assert probe.age + probe.waited == tick, tick
        if probe.creating:
            assert probe.presence == 1 and probe.counted == 1, tick
            owed_at.append(probe.owed)
        assert probe.acc_owed == probe.age % 4, tick
        assert thirds.age == tick and thirds.acc_lamp == tick % 3, tick
    assert probe.age == 8000 and probe.waited == 2000
    assert owed_at == [by_clock(k, 1, 4) for k in range(8000)]
    births = [r["tick"] for r in records if r["event"] == "birth" and r["measured"] == 3]
    assert births == [tick for tick in range(1, INTERVALS + 1) if by_clock(tick - 1, 1, 3) == 1]
    assert len(births) == 3333


# -- (c) ---------------------------------------------------------------------------


def resume_world() -> dict[str, object]:
    """A source of `m` (content 3) at x = 0 releasing 3 units per
    self-creation on +X into a probe of `light` (content 1) at x = 1 that
    measures them (so no row lingers but the newborn ones at x = 0), a
    turning body of `light` (content 3) at K = [3, 8] and a mover of
    `light` (content 16) at momentum 1000 over `width` 8 (a Link per 9192
    / 1000 self-creations)."""
    source = {
        "position": [0, 0, 0],
        "family": "m",
        "amount": 3,
        "fixed": True,
        "directions": [[1, 0, 0]],
    }
    probe = {
        "position": [1, 0, 0],
        "family": "light",
        "amount": 1,
        "fixed": True,
        "table": {"m": "measure"},
    }
    turner = {"position": [2, 0, 0], "family": "light", "amount": 3, "fixed": True}
    mover = {"position": [3, 0, 0], "family": "light", "amount": 16, "momentum": [1000, 0, 0]}
    return bar([source, probe, turner, mover], shape=[12, 1, 1], release=[1, 1])


def state_of(simulation: NatureBeamSimulation) -> dict[str, object]:
    """`state.json` as the runner writes it, parsed."""
    stream = io.StringIO()
    write_snapshot(simulation, stream)
    document: dict[str, object] = json.loads(stream.getvalue())
    return document


def resumed(
    world: dict[str, object], state: dict[str, object], keep_accumulators: bool
) -> NatureBeamSimulation:
    """A simulation of the world continued from `state.json`: the tick,
    every measured event's record (its place, what it holds, its clock,
    its drive and, with `keep_accumulators`, its accumulators) and the
    rows at the Nodes. A test's resume: the runner has none."""
    simulation = NatureBeamSimulation(parse_nature_beam_world(world))
    simulation.tick = int(state["tick"])  # type: ignore[arg-type]
    entries = state["measured"]
    assert isinstance(entries, list)
    for line in entries:
        entry = simulation.measured[int(line["number"])]
        position = tuple(int(v) for v in line["position"])
        assert len(position) == 3
        nodes = body_nodes(position, entry.span, simulation.shape, simulation.world.periodic)
        assert nodes is not None
        simulation._place(entry, nodes)
        entry.position = position
        entry.held = [int(v) for v in line["held"]]
        entry.phase = int(line["phase"])
        entry.momentum = [int(v) for v in line["momentum"]]
        entry.age, entry.owed, entry.waited = int(line["age"]), int(line["owed"]), int(line["waited"])
        entry.turned, entry.steps = int(line["phase_steps"]), int(line["steps"])
        entry.drive = [int(v) for v in line["drive"]]
        entry.axis_steps = [int(v) for v in line["axis_steps"]]
        entry.taken = [dict(t) for t in line["measured"]]
        entry.clicks = [int(v) for v in line["events"]]
        entry.pushed = [int(v) for v in line["pushed"]]
        entry.contacts = [int(v) for v in line["contacts"]]
        if keep_accumulators:
            acc = line["acc"]
            entry.acc_owed, entry.acc_lamp, entry.acc_turn = (
                int(acc["owed"]),
                int(acc["lamp"]),
                int(acc["turn"]),
            )
            entry.acc_release = [int(v) for v in acc["release"]]
    vectors = [tuple(int(v) for v in row) for row in simulation.tables.flight.vectors]
    names = [family.name for family in simulation.families]
    for node in state["nodes"]:  # type: ignore[union-attr]
        position = tuple(int(v) for v in node["position"])
        assert len(position) == 3
        for group in node["families"]:
            family = names.index(group["family"])
            store = simulation.stores[family]
            for ray in group["rays"]:
                store.append(
                    node=np.array([store.flat(position)]),
                    direction=np.array([vectors.index(tuple(int(v) for v in ray["direction"]))]),
                    age=np.array([int(ray["age"])]),
                    phase=np.array([int(ray["phase"])]),
                    number=np.array([int(ray["number"])]),
                    amount=np.array([int(ray["amount"])]),
                    content=np.array([int(ray["content"])]),
                    arrival=np.array([NO_ARRIVAL]),
                )
    for store in simulation.stores:
        store.sort()
    return simulation


def run_recording(
    simulation: NatureBeamSimulation, ticks: int
) -> tuple[list[list[dict[str, object]]], list[dict[str, object]]]:
    records: list[dict[str, object]] = []
    simulation.record = records.append
    states = []
    for _ in range(ticks):
        simulation.step()
        states.append(simulation.contents())
    return states, records


def test_the_accumulators_are_carried_in_the_state_and_a_resumed_run_is_the_unbroken_one(tmp_path: Path):
    """(c)."""
    world = resume_world()
    unbroken = NatureBeamSimulation(parse_nature_beam_world(world))
    states, records = run_recording(unbroken, 40)
    halfway = NatureBeamSimulation(parse_nature_beam_world(world))
    for _ in range(20):
        halfway.step()
    state = state_of(halfway)
    entries = state["measured"]
    assert isinstance(entries, list)
    push = {"gravity": [0, 0, 0], "charge": [0, 0, 0]}
    assert [line["acc"] for line in entries] == [
        {"owed": 0, "release": [0, 0], "lamp": 0, "turn": 0, "push": push},
        {"owed": 3 * 11 % 4, "release": [0, 0], "lamp": 0, "turn": 3 * 12 % 8, "push": push},
        {"owed": 0, "release": [0, 0], "lamp": 0, "turn": 9 * 20 % 8, "push": push},
        {"owed": 0, "release": [0, 0], "lamp": 0, "turn": 48 * 20 % 8, "push": push},
    ]
    assert entries[1]["age"] == 12 and entries[1]["waited"] == 8
    assert entries[3]["drive"] == [20 * 1000 % (Q * 8 * 16 + 1000), 0, 0] and entries[3]["steps"] == 2
    # Every count's phase at the age is its accumulator: the run resumed
    # with them is the unbroken one, tick for tick and record for record.
    continued = resumed(world, state, keep_accumulators=True)
    later, later_records = run_recording(continued, 20)
    assert later == states[20:]
    assert later_records == [r for r in records if int(r["tick"]) > 20]  # type: ignore[call-overload]
    # Emptied at the age, they are not (FORM.md section 1 (i)).
    forgetful = resumed(world, state, keep_accumulators=False)
    other, _ = run_recording(forgetful, 20)
    assert other != states[20:]
    assert [entry["acc"] for entry in other[-1]] != [entry["acc"] for entry in states[-1]]
    # The runner writes them in both files.
    source = json.dumps(world).encode("utf-8")
    out = tmp_path / "run"
    out.mkdir()
    execute_nature_beam_run(parse_nature_beam_world(world), source, out, "test", 20)
    written = json.loads((out / "state.json").read_text(encoding="utf-8"))
    record = json.loads((out / "run.json").read_text(encoding="utf-8"))
    assert [line["acc"] for line in written["measured"]] == [line["acc"] for line in entries]
    assert [line["acc"] for line in record["measured"]] == [line["acc"] for line in entries]
    # A declared accumulator is refused.
    with pytest.raises(ValueError, match="unknown keys: acc"):
        parse_nature_beam_world(bar([{**SOURCE, "acc": {"turn": 1}}]))


# -- (e) ---------------------------------------------------------------------------


def test_every_accumulator_stays_below_its_denominator():
    """(e)."""
    simulation = NatureBeamSimulation(parse_nature_beam_world(bar([SOURCE, TURNER, MOVER])))
    counting = NatureBeamSimulation(parse_nature_beam_world(counting_world()))
    for tick in range(1, 2001):
        simulation.step()
        counting.step()
        for entry in [*simulation.measured.values(), *counting.measured.values()]:
            assert 0 <= entry.acc_owed < 4, (tick, entry.number)
            assert all(0 <= acc < 10 for acc in entry.acc_release), (tick, entry.number)
            assert 0 <= entry.acc_lamp < 3, (tick, entry.number)
            assert 0 <= entry.acc_turn < (8 if entry in simulation.measured.values() else 1 << 20), tick
            for axis in range(3):
                reach = Q * 8 * entry.content + abs(entry.momentum[axis])
                assert abs(entry.drive[axis]) < reach, (tick, entry.number, axis)
    # The primitive: an unsigned accumulator in [0, d), a signed one in
    # (-d, d), with the step's cap and without, under random rates.
    draw = random.Random(41)
    for denominator in (3, 1000, 1 << 20):
        unsigned = signed = capped = 0
        owed = 0
        for _ in range(INTERVALS):
            rate = draw.randrange(denominator)
            count, unsigned = by_drive(unsigned, rate, denominator)
            assert 0 <= unsigned < denominator and count >= 0
            signed_rate = rate if draw.random() < 0.5 else -rate
            count, signed = by_drive(signed, signed_rate, denominator)
            assert -denominator < signed < denominator and count in (-1, 0, 1)
            count, capped = by_drive(capped, signed_rate, denominator, at_most=1)
            assert -denominator < capped < denominator and count in (-1, 0, 1)
            count, owed = count_owed(owed, draw.randrange(1 << 10), (1, denominator))
            assert 0 <= owed < denominator
    # The step's drive: a momentum reversing at random keeps the drive
    # within D on a body of content 16 at width 8.
    drive = 0
    for _ in range(INTERVALS):
        momentum = draw.choice((-1024, -7, 7, 1024))
        _, drive = step_axis(drive, momentum, 16, 8)
        assert abs(drive) < Q * 8 * 16 + abs(momentum)


def test_the_ladders_cell_is_the_comparison_of_products():
    """(f)."""
    draw = random.Random(2026_09_20)
    for _ in range(2000):
        steps = draw.choice((64, 256))
        weights = [
            (draw.randrange(0, 1 << 20), draw.randrange(1, 65)) for _ in range(draw.randrange(1, 9))
        ]
        ladder, total = rungs(weights, steps)
        for u in range(steps):
            assert cell_of(weights, steps, u) == choose(ladder, u) if total[0] else None
    assert cell_of([(0, 1), (0, 3)], 64, 5) is None and rungs([(0, 1), (0, 3)], 64)[1] == (0, 1)
    spec = importlib.util.spec_from_file_location(
        "amplitude_make_worlds_ff", ROOT / "examples" / "events" / "amplitude" / "make_worlds.py"
    )
    assert spec is not None and spec.loader is not None
    generator = importlib.util.module_from_spec(spec)
    sys.modules["amplitude_make_worlds_ff"] = generator
    spec.loader.exec_module(generator)
    worlds = {
        "mz_equal": generator.mach_zehnder("mz_equal"),
        "mz_345": generator.mach_zehnder("mz_345", splitter=generator.PYTHAGOREAN_5),
        "bell_0_8": generator.pair_worlds()["bell_0_8"],
        "slits_low": generator.two_slits_low(),
    }
    for name, world in worlds.items():
        simulation = NatureBeamSimulation(parse_nature_beam_world(world))
        for _ in range(int(world["ticks"])):
            simulation.step()
        assert simulation.layer is not None
        gathers = simulation.layer.gathers
        assert gathers, name
        # The layer chose the cell by the comparison (`cell_of`); the
        # gather reports the rungs: the rungs' cell of u is the chosen one.
        for gather in gathers:
            cells = gather["cells"]
            assert isinstance(cells, list) and gather["chosen"] is not None, name
            ladder = [int(cell[1]) for cell in cells]
            chosen = [k for k, cell in enumerate(cells) if cell[0] == gather["chosen"]]
            assert len(chosen) == 1, (name, gather["record"])
            assert choose(ladder, int(gather["u"])) == chosen[0], (name, gather["record"])


# -- (g) ---------------------------------------------------------------------------


def scaled_world(m_value: list[int], w_value: list[int] | None) -> dict[str, object]:
    """The bar with the column `s` on the free family `m` at `m_value` and,
    when given, on a second free family `w` at `w_value` (a paid family
    carries no column value); the source of `m` its one measured event."""
    families: list[dict[str, object]] = [
        {"name": "m", "quantum": 0, "phase": False, "columns": {"s": {"value": m_value, "sign": -1}}},
        {"name": "light", "quantum": 1},
    ]
    if w_value is not None:
        families.append(
            {"name": "w", "quantum": 0, "phase": False, "columns": {"s": {"value": w_value, "sign": -1}}}
        )
    return bar([SOURCE], families=families)


def test_a_column_whose_lifted_denominator_leaves_the_register_is_refused_at_load():
    """(g)."""
    assert MOMENTUM_BOUND == (1 << 62) - 1 and MAX_VALUE == (1 << 30) - 1
    # The largest Lambda_c two declared values can form under the ceiling
    # 2^31 - 1 (the integer root of the bound, a prime beyond one value's
    # bound): 2 x (2^30 - 1), its square below the bound, loads.
    ceiling = (1 << 31) - 1
    assert ceiling * ceiling <= MOMENTUM_BOUND < (ceiling + 1) * (ceiling + 1)
    largest = ceiling - 1
    loaded = parse_nature_beam_world(scaled_world([1, 2], [1, MAX_VALUE]))
    assert loaded.column_scales == (1, 1, largest)
    # One value at the register's bound alone.
    alone = parse_nature_beam_world(scaled_world([1, MAX_VALUE], None))
    assert alone.column_scales == (1, 1, MAX_VALUE)
    # The smallest Lambda_c two values can form above the ceiling, 2^31 + 1
    # = 3 x 715827883 (2^31 itself is beyond one value's bound): refused at
    # the parse, naming the column and the bound, with no body's table formed.
    above = (1 << 31) + 1
    assert 3 * 715827883 == above and above * above > MOMENTUM_BOUND
    with pytest.raises(ValueError) as refusal:
        parse_nature_beam_world(scaled_world([1, 3], [1, 715827883]))
    message = str(refusal.value)
    assert f"the column 's': Lambda_c = {above}," in message
    assert f"beyond the integer bound {MOMENTUM_BOUND}" in message
    assert f"at most {(1 << 31) - 1}" in message


# -- (h), (i) ----------------------------------------------------------------------


def test_a_record_rows_push_keeps_its_remainder_on_the_row():
    """(h)."""
    draw = random.Random(155)
    for _ in range(2000):
        label = draw.choice((-1, 1)) * draw.randrange(0, 1 << 30)
        amount, m, pushes = draw.randrange(1, 64), draw.randrange(1, 500), draw.randrange(1, 12)
        accumulator, delivered, floors = 0, 0, 0
        for _ in range(pushes):
            share, accumulator = share_of(label, amount, m, accumulator)
            delivered += share
            floors += share_of(label, amount, m)[0]
            assert abs(accumulator) < m
        total = pushes * label * amount
        exact = -(abs(total) // m) if total < 0 else abs(total) // m
        assert delivered == exact and 0 <= abs(exact) - abs(floors) <= pushes - 1
    world = {
        "law": "beam",
        "model_id": "share-accumulator-test",
        "shape": [12, 2, 2],
        "boundary": "open",
        "ticks": 30,
        "K": 1 << 20,
        "N": 64,
        "release": [0, 1],
        "suspension": 0,
        "families": [
            {"name": "light", "quantum": 1, "charge": 0},
            {"name": "reader", "quantum": 1, "charge": 0},
        ],
        "measured": [
            {
                "position": [0, 0, 0],
                "family": "light",
                "amount": 1 << 20,
                "fixed": True,
                "lamp": {"rate": [1, 1], "directions": [[1, 0, 0], [0, 1, 0], [0, 0, 1]]},
            },
            *(
                {
                    "position": [x, 0, 0],
                    "family": "reader",
                    "amount": 3,
                    "fixed": True,
                    "table": {"light": "read"},
                }
                for x in (4, 5, 6, 7)
            ),
        ],
    }
    lines: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(world), observer=lines.append)
    store = simulation.stores[0]
    readers = [store.flat((x, 0, 0)) for x in (4, 5, 6, 7)]
    for tick in range(1, 31):
        simulation.step()
        assert simulation.books()["balanced"], tick
        # A row read keeps the part of its push not yet delivered, below m.
        at_readers = np.isin(store.node, readers) & (store.record != 0)
        for i in np.flatnonzero(at_readers).tolist():
            assert abs(int(store.share_x[i])) < int(store.multiplicity[i])
    reads = [line for line in lines if line["event"] == "read"]
    units = sum(int(str(line["amount"])) for line in reads)
    pushed = sum(int(line["push"][0]) for line in reads)  # type: ignore[index]
    assert reads and pushed == sum(simulation.measured[n].pushed[0] for n in (2, 3, 4, 5))
    # The +x row's label is 64 over m = 3: 21 per read with the remainder
    # 1 carried on the row from reader to reader, delivered as the 22nd
    # unit every third read (the floor alone would give 21 x units).
    assert 21 * units < pushed < 22 * units
    written = state_of(simulation)["nodes"]
    assert isinstance(written, list)
    rows_with_share = [
        ray for node in written for group in node["families"] for ray in group["rays"] if "share" in ray
    ]
    assert rows_with_share and all(len(ray["share"]) == 3 for ray in rows_with_share)


def test_a_sets_release_is_placed_by_the_nodes_claims():
    """(i)."""
    draw = random.Random(155)
    for _ in range(300):
        ways = draw.randrange(2, 8)
        counts = counts_table((1, 1), (0, 1), (0, 1), (True,), None, (1,), None, 1, ways)
        assert isinstance(counts, CountTable)
        placed = [0] * ways
        total = 0
        for _ in range(40):
            amount = draw.randrange(0, 50)
            shares = place_over_nodes(counts, amount, ways)
            assert sum(shares) == amount and all(share >= 0 for share in shares)
            total += amount
            placed = [a + b for a, b in zip(placed, shares, strict=True)]
            claims = counts.values("place")
            assert sum(claims) == 0 and all(abs(claim) < ways for claim in claims)
            assert all(abs(ways * got - total) < ways for got in placed)
