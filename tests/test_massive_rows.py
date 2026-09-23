"""The massive rows (`massive-rows-v1`; the model owner's yes of 2026-09-21,
record 332 of docs/LOG_2026-09-20.md; the mathematician's design
docs/designs/massive_rows/DESIGN.md, ADMISSIBLE in the physics-rule
review's three rounds; the worlds and the register of
`examples/events/massive_rows/`). The expected integers of
docs/TEST_EXPECTATIONS.md ("The massive rows"), written down before the
first run; every number of a shipped world read from its register:

(a) the gate: every lamp-free world of the gate set reads at its cap the
    three digests `gate_set.json` registers (as `test_amplitude_click` (d)
    reads them), and the amplitude worlds `mz_345`, `bell_0_8` and
    `slits_low` read at their ticks the digests registered from the base
    tree before the build (`expectations.json` under `byte_identity`):
    state, books and events byte identical without the key; on every one
    of them and on every world of the gate set the pair (f_F, q_F) is
    (1, 0) on every family, `massive_rows` is false, the identity is not
    under `hypotheses`, and no row of `state.json` carries `acc_turn`;
(b) the tables by value: on a small world of a massive family `matter`
    (quantum 4, p 400, S 1, h 1024, N 64) beside the paid family `wall`,
    the wall's table is Flight's (the rate 2 S_1 Q, the wall 2 T_D, the
    start T_D, the labels u_D, the turn `phase_per_link` on every
    direction and axis over 1, the pair (1, 0)) and the massive table is
    the host's computation of the design's section 1 (p_D by the scaled
    unit rule, E'_0 = Q S M, E'_D = isqrt(E'_0^2 + 3 p_D . p_D), the rate
    2 abs(p_D)_1, the wall 2 E'_D, the start E'_D, the turn abs(p_{D,a}) N
    over h, the pair (0, M)); the primitive's identity on the pin world's
    table: at E'_0 = 0 with the flight vector Q D the massive triple is
    Flight's on every one of its 1332 directions, and with the label u_D
    in its place on the six headings alone; `scaled_label` at the scale Q
    is `unit_label` on every direction;
(c) the edges: the primitive at p = 0 (the labels zero) has the rate 0 and
    the turn 0 on every direction, so a row never moves and never turns;
    `momentum_magnitude` 0 is refused at load; a massive record of two
    rows through the open faces +x and -x completes at one face: that
    face's lines gain one unit, the content M and the label M p_D, the
    `gather` line carries them, the other face's waiting goes to the
    cancelled lines (one unit, M, the other label) and the books balance;
(d) the refusals, naming the key: `massive` without `massive_rows`, with
    `phase_per_link` in either form, on a free family, on a family without
    a phase circle, without `action`; `momentum_magnitude` on a lamp of a
    family that is not massive, absent on a massive lamp, below 1, two
    values on two lamps of one family, a massive family without a lamp;
    `age_bound` absent with the key; the domain: a rest energy whose
    square passes 2^62 - 1 and a turn's rate abs(p_a) N beyond it; at the
    birth, a massive lamp whose turn is 2 (held 2 K), naming the lamp;
    the inverse interval on a world that declares the key;
(e) the books' identity at every step on a small massive world (a lamp
    toward a screen of `sum` pixels, no re-emitter): the books balanced;
    the content line's `absorbed` the measured line's `measured` plus the
    `waiting` sub-line; the momentum lines measured + transit + escaped +
    cancelled + remainder + waiting zero on every axis; at a completion
    the chosen pixel's `held` grows by M, its `clicks` by one, its
    momentum by M p_D of a direction of the table, the `gather` line's
    `content` M and `momentum` that label, and the rest of the record's
    waiting moves to the cancelled lines; the turn: the heading's row
    holds after k Links the phase floor(k p N / h) plus its birth phase
    mod N with the remainder k p N mod h on `acc_turn`, the plane wave to
    one remainder; two rows of different remainders never merge;
(f) the small massive two-slit world `slits_matter_small` (8 births read,
    48 intervals) replayed bit-exact through the runner: the digests of
    state, books and events, the gathers of the records 1 .. 8 (the tick,
    the chosen set, the Node, the content M and the one label), the books
    at the end, the identity under `hypotheses`, as `tools/click_readings/massive_rows_replay.py`
    wrote them;
(g) the pin derived from the world and the engine's tables (the round-2
    map's B on the engine's own Bresenham lines by the family's triple):
    E' = 4113 on every direction of the pin's table, the lamp leg 139 (the
    photon's 13 by Flight's triple), the first fan row at the centre pixel
    815 intervals after the re-release and at the first-fringe pixels 876,
    the longest row 1468, the diagonal's table entry (624, 8226, 4113), as
    registered.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import re
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.nature_beam import (
    IDENTITY_FIELDS,
    FamilyFlight,
    NatureBeamStore,
    direction_flight,
    flight_triple,
    unit_label,
)
from event_universe.events.run import execute_nature_beam_run
from event_universe.events.world import MASSIVE_ROWS_RULE, Q, scaled_label
from event_universe.world_loading import load_world

ROOT = Path(__file__).resolve().parents[1]
WORLDS = ROOT / "examples" / "events" / "massive_rows"
GATE_SET = ROOT / "examples" / "events" / "gate_set.json"
EXPECTATIONS = json.loads((WORLDS / "expectations.json").read_text("utf-8"))
INTEGERS = EXPECTATIONS["integers"]
BASE = 1 << 32
N = 64
H = 1024
# The small worlds' family: the content M of one row and the label's
# magnitude p (E'_0 = 256, E' = 738 on a heading, the pace 400 / 738).
M = 4
P = 400


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


AMPLITUDE = load(
    "amplitude_make_worlds_massive_test", ROOT / "examples" / "events" / "amplitude" / "make_worlds.py"
)
GENERATOR = load("massive_rows_make_worlds_test", WORLDS / "make_worlds.py")


def small_world(
    *,
    massive: bool = True,
    p: int | None = P,
    m: int = M,
    faces: bool = False,
    key: bool = True,
    action: int | None = H,
    family_extra: dict[str, object] | None = None,
    age_bound: int | None = 4000,
    amount: int = 1 << 20,
    clock: int = 1 << 20,
) -> dict[str, object]:
    """A lamp of `matter` on a plane of 11 x 11 x 1 (z periodic): at (1, 5,
    0) on +x and the two diagonals toward a screen of `sum` pixels at x =
    9 (`faces` False), or at (5, 5, 0) on +x and -x toward the open faces
    with no detector (`faces` True)."""
    family: dict[str, object] = {"name": "matter", "quantum": m}
    if massive:
        family["massive"] = True
    family.update(family_extra or {})
    lamp: dict[str, object] = {
        "rate": [1, 1],
        "wheel": [1, 8],
        "directions": [[1, 0, 0], [-1, 0, 0]] if faces else [[1, 0, 0], [1, 1, 0], [1, -1, 0]],
    }
    if p is not None:
        lamp["momentum_magnitude"] = p
    measured: list[dict[str, object]] = [
        {
            "position": [5 if faces else 1, 5, 0],
            "family": "matter",
            "amount": amount,
            "fixed": True,
            "lamp": lamp,
        }
    ]
    if not faces:
        measured.extend(
            {"position": [9, y, 0], "family": "wall", "amount": 1, "fixed": True} for y in range(11)
        )
    document: dict[str, object] = {
        "law": "beam",
        "model_id": "massive-rows-test",
        "shape": [11, 11, 1],
        "boundary": {"z": "periodic"},
        "ticks": 60,
        "K": clock,
        "N": N,
        "release": [1, 128],
        "suspension": 0,
        "width": 1,
        "directions": [[1, 1, 0], [1, -1, 0]],
        "families": [family, {"name": "wall", "quantum": 1}],
        "measured": measured,
        "detectors": (
            []
            if faces
            else [{"name": f"screen_{y}", "positions": [[9, y, 0]], "reading": "sum"} for y in range(11)]
        ),
    }
    if action is not None:
        document["action"] = action
    if age_bound is not None:
        document["age_bound"] = age_bound
    if key:
        document["massive_rows"] = True
    return document


def run(
    world: dict[str, object], ticks: int | None = None
) -> tuple[NatureBeamSimulation, list[dict[str, object]]]:
    lines: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(world), observer=lines.append)
    for _ in range(int(world["ticks"]) if ticks is None else ticks):  # type: ignore[call-overload]
        simulation.step()
    return simulation, lines


def host_label(vector: tuple[int, int, int], scale: int) -> tuple[int, int, int]:
    """The design's rule on the host: the integer vector nearest scale D / |D|."""
    n = sum(c * c for c in vector)
    if n == 0 or scale == 0:
        return (0, 0, 0)
    found = []
    for a in vector:
        t = 2 * scale * abs(a)
        k = (math.isqrt(t * t // n) + 1) // 2
        found.append(k if a >= 0 else -k)
    return found[0], found[1], found[2]


def digests_of(out: Path) -> dict[str, str]:
    record = json.loads((out / "run.json").read_text(encoding="utf-8"))
    return {
        "state_sha256": hashlib.sha256((out / "state.json").read_bytes()).hexdigest(),
        "audit_sha256": hashlib.sha256(json.dumps(record["audit"]).encode("utf-8")).hexdigest(),
        "events_sha256": hashlib.sha256((out / "events.jsonl").read_bytes()).hexdigest(),
    }


def gathers_of(lines: list[dict[str, object]], tick: int | None = None) -> list[dict[str, object]]:
    return [
        line for line in lines if line["event"] == "gather" and (tick is None or line["tick"] == tick)
    ]


# -- (a) ---------------------------------------------------------------------------


def gate_worlds_without_a_lamp() -> list[tuple[str, int]]:
    document = json.loads(GATE_SET.read_text(encoding="utf-8"))
    found = []
    for entry in document["worlds"]:
        path = GATE_SET.parent / entry["path"]
        loaded = load_world(path.read_bytes(), base_dir=path.parent)
        if all(event.lamp is None for event in loaded.world.measured):
            found.append((entry["path"], int(entry["cap"])))
    return found


@pytest.mark.parametrize(("path", "cap"), gate_worlds_without_a_lamp())
def test_a_gate_world_without_a_lamp_reads_as_it_did(tmp_path: Path, path: str, cap: int):
    """(a): the gate set's lamp-free worlds at their caps."""
    source = (GATE_SET.parent / path).read_bytes()
    world = load_world(source, base_dir=(GATE_SET.parent / path).parent).world
    assert world.massive_rows is False and MASSIVE_ROWS_RULE not in world.hypotheses
    out = tmp_path / "run"
    out.mkdir()
    entry = next(
        e for e in json.loads(GATE_SET.read_text(encoding="utf-8"))["worlds"] if e["path"] == path
    )
    if "refusal" in entry:
        # The world refuses before its cap under the law as it stands (the
        # gate set's `refusal`, the generic entry of the bending): the
        # digests beside it are the base tree's before the entry.
        with pytest.raises(OverflowError, match=entry["refusal"]["match"]):
            execute_nature_beam_run(world, source, out, "test", cap)
        return
    execute_nature_beam_run(world, source, out, "test", cap)
    assert digests_of(out) == entry["digests"], path
    assert b'"acc_turn"' not in (out / "state.json").read_bytes()
    record = json.loads((out / "run.json").read_text(encoding="utf-8"))
    assert record["massive_rows"] is False and MASSIVE_ROWS_RULE not in record["hypotheses"]


def test_every_gate_world_carries_the_pair_one_zero_on_every_family():
    """(a): (f_F, q_F) = (1, 0) by value on every family of every gate world."""
    for entry in json.loads(GATE_SET.read_text(encoding="utf-8"))["worlds"]:
        path = GATE_SET.parent / entry["path"]
        world = load_world(path.read_bytes(), base_dir=path.parent).world
        tables = NatureBeamSimulation(world).tables
        for definition, table in zip(world.families, tables.family_flights, strict=True):
            assert definition.massive is False, entry["path"]
            assert (table.placed, table.quantum, table.content) == (1, 0, 0), entry["path"]
            assert table.turn_denominator == 1
            assert (table.turn == definition.phase_per_link).all()


@pytest.mark.parametrize("name", ["mz_345", "bell_0_8", "slits_low"])
def test_an_amplitude_world_reads_as_it_did_before_the_identity(tmp_path: Path, name: str):
    """(a): mz_345, bell_0_8 and slits_low against the base tree's digests."""
    worlds = {
        "mz_345": lambda: AMPLITUDE.mach_zehnder("mz_345", splitter=AMPLITUDE.PYTHAGOREAN_5),
        "bell_0_8": lambda: AMPLITUDE.pair_worlds()["bell_0_8"],
        "slits_low": AMPLITUDE.two_slits_low,
    }
    world = worlds[name]()
    registered = EXPECTATIONS["byte_identity"]["worlds"][name]
    source = (json.dumps(world) + "\n").encode("utf-8")
    assert hashlib.sha256(source).hexdigest() == registered["source_sha256"]
    parsed = parse_nature_beam_world(world)
    assert parsed.massive_rows is False and MASSIVE_ROWS_RULE not in parsed.hypotheses
    simulation = NatureBeamSimulation(parsed)
    assert all((t.placed, t.quantum) == (1, 0) for t in simulation.tables.family_flights)
    out = tmp_path / "run"
    out.mkdir()
    execute_nature_beam_run(parsed, source, out, "test", int(registered["ticks"]))
    found = digests_of(out)
    assert found == {key: registered[key] for key in found}, name
    assert b'"acc_turn"' not in (out / "state.json").read_bytes()
    record = json.loads((out / "run.json").read_text(encoding="utf-8"))
    assert len(record["world"]) == registered["gathers"]
    assert "waiting" not in record["audit"][-1]["momentum"]
    assert all("waiting" not in lines["content"] for lines in record["audit"][-1]["families"].values())


# -- (b) ---------------------------------------------------------------------------


def test_the_tables_are_the_host_computation_of_the_design():
    """(b)."""
    world = parse_nature_beam_world(small_world())
    simulation = NatureBeamSimulation(world)
    flight = simulation.tables.flight
    matter, wall = simulation.tables.family_flights
    vectors = [tuple(int(v) for v in row) for row in flight.vectors]
    # The wall's table: Flight's numbers by value and the pair (1, 0).
    assert wall.rate.tolist() == (2 * flight.manhattan * Q).tolist()
    assert wall.wall.tolist() == (2 * flight.resolution).tolist()
    assert wall.start.tolist() == flight.resolution.tolist()
    assert wall.labels.tolist() == flight.labels.tolist()
    assert wall.turn.tolist() == [[0, 0, 0]] * len(vectors) and wall.turn_denominator == 1
    assert (wall.placed, wall.quantum, wall.content) == (1, 0, 0)
    # The massive table: the design's section 1 on the host.
    rest = Q * 1 * M
    for index, vector in enumerate(vectors):
        label = host_label(vector, P)
        energy = math.isqrt(rest * rest + 3 * sum(c * c for c in label))
        assert matter.labels[index].tolist() == list(label), vector
        assert int(matter.rate[index]) == 2 * sum(abs(c) for c in label)
        assert int(matter.wall[index]) == 2 * energy and int(matter.start[index]) == energy
        assert matter.turn[index].tolist() == [abs(c) * N for c in label]
        assert int(matter.rate[index]) <= int(matter.wall[index])
    assert matter.turn_denominator == H
    assert (matter.placed, matter.quantum, matter.content) == (0, M, M)
    heading = vectors.index((1, 0, 0))
    assert int(matter.wall[heading]) == 2 * 738 and matter.labels[heading].tolist() == [P, 0, 0]
    # The walk on the heading: one Link per E' / p intervals in the mean by
    # the same verb (the count 0 or 1), 4 p Links in 4 E' intervals.
    ages = np.arange(738 * 4, dtype=np.int64)
    steps = matter.walk_step(np.full(ages.shape, heading), ages)
    assert set(steps[:, 0].tolist()) == {0, 1} and int(steps[:, 0].sum()) == 4 * P
    # The wall's walk is Flight's, integer for integer.
    ages = np.arange(500, dtype=np.int64)
    for index in range(len(vectors)):
        directions = np.full(ages.shape, index)
        assert (wall.walk_step(directions, ages) == flight.walk_step(directions, ages)).all()


def test_the_primitive_is_flights_at_zero_rest_energy_on_the_pin_worlds_table():
    """(b): 1332 of 1332 with Q D, 6 of 1332 with u_D; `scaled_label` at Q is `unit_label`."""
    path = ROOT / "examples" / "events" / "amplitude" / "slits_huygens.json"
    world = load_world(path.read_bytes(), base_dir=path.parent).world
    flight = direction_flight(world.directions)
    vectors = np.array(world.directions, dtype=np.int64)
    moving = [i for i, v in enumerate(world.directions) if any(v)]
    assert len(moving) == 1332
    rate, wall, start = flight_triple(Q * vectors, 0)
    same = [
        i
        for i in moving
        if (int(rate[i]), int(wall[i]), int(start[i]))
        == (2 * int(flight.manhattan[i]) * Q, 2 * int(flight.resolution[i]), int(flight.resolution[i]))
    ]
    assert len(same) == 1332
    rate_u, wall_u, _ = flight_triple(flight.labels, 0)
    same_u = [
        i
        for i in moving
        if (int(rate_u[i]), int(wall_u[i]))
        == (2 * int(flight.manhattan[i]) * Q, 2 * int(flight.resolution[i]))
    ]
    assert len(same_u) == 6 and all(sum(abs(c) for c in world.directions[i]) == 1 for i in same_u)
    for vector in world.directions:
        assert scaled_label(vector, Q) == unit_label(vector)
        assert scaled_label(vector, INTEGERS["p"]) == host_label(vector, INTEGERS["p"])
    # The pin's integers: E' = 4113 on every direction, abs(p_D) within
    # 0.29 percent of p.
    labels = np.array([scaled_label(v, INTEGERS["p"]) for v in world.directions], dtype=np.int64)
    _, wall_m, start_m = flight_triple(labels, INTEGERS["rest_energy"])
    assert {int(start_m[i]) for i in moving} == {INTEGERS["energy"]}
    assert {int(wall_m[i]) for i in moving} == {2 * INTEGERS["energy"]}
    norms = [math.sqrt(sum(c * c for c in labels[i].tolist())) for i in moving]
    assert 219.3 < min(norms) and max(norms) < 220.7


# -- (c) ---------------------------------------------------------------------------


def test_the_primitive_at_p_zero_never_moves_and_never_turns():
    """(c)."""
    flight = direction_flight(((0, 0, 0), (0, 0, 0), (1, 0, 0), (1, 1, 0), (2, 1, 0)))
    zero = np.zeros((5, 3), dtype=np.int64)
    rate, wall, start = flight_triple(zero, 256)
    assert rate.tolist() == [0] * 5 and wall.tolist() == [512] * 5 and start.tolist() == [256] * 5
    table = FamilyFlight(
        rate, wall, start, flight.manhattan, flight.lines, zero, np.abs(zero) * N, H, 0, M, M
    )
    ages = np.arange(2000, dtype=np.int64)
    for index in range(5):
        assert not table.walk_step(np.full(2000, index), ages).any()
    count, after = table.turned(np.zeros(3, dtype=np.int64), np.array([2, 3, 4]), np.array([0, 1, 0]))
    assert count.tolist() == [0, 0, 0] and after.tolist() == [0, 0, 0]
    with pytest.raises(ValueError, match="momentum_magnitude must be an integer from 1"):
        parse_nature_beam_world(small_world(p=0))


def test_a_massive_record_through_the_open_faces_completes_at_one_face():
    """(c)."""
    simulation, lines = run(small_world(faces=True), ticks=40)
    gathers = gathers_of(lines)
    assert gathers, "no completion"
    faces = {d["name"]: d["families"]["matter"] for d in simulation.face_detectors()}
    books = simulation.books()
    assert books["balanced"]
    matter = books["families"]["matter"]
    assert faces["face:+x"]["clicks"] + faces["face:-x"]["clicks"] == len(gathers)
    assert faces["face:+x"]["content"] + faces["face:-x"]["content"] == M * len(gathers)
    # Every gather chose a face, took M and the one label M p_D there, and
    # cancelled the other row's unit, content and label.
    for gather in gathers:
        name = gather["chosen"][0][0]
        assert name in ("face:+x", "face:-x") and gather["content"] == M
        assert gather["momentum"] == [(1 if name == "face:+x" else -1) * M * P, 0, 0]
    assert faces["face:+x"]["momentum"] == [M * P * faces["face:+x"]["clicks"], 0, 0]
    assert faces["face:-x"]["momentum"] == [-M * P * faces["face:-x"]["clicks"], 0, 0]
    assert matter["transit"]["cancelled"] == len(gathers)
    assert matter["content"]["cancelled"] == M * len(gathers)
    assert matter["cancelled"] == [
        M * P * (faces["face:-x"]["clicks"] - faces["face:+x"]["clicks"]),
        0,
        0,
    ]
    # The face's click lines are what arrived (both rows of every record);
    # the value says where it went: nothing measured, the placed content
    # escaped, the rest waiting until its completion.
    face_clicks = [
        line for line in lines if line["event"] == "click" and str(line["detector"]).startswith("face:")
    ]
    assert len(face_clicks) == 2 * len(gathers)
    assert all(line["content"] == M for line in face_clicks)
    assert matter["measured"]["measured"] == 0 and matter["content"]["escaped"] == M * len(gathers)
    # The two rows of a record escape in one interval (one pace, one age)
    # and the record completes in it: nothing waits at the end of an
    # interval, and `absorbed` holds the waiting alone.
    assert matter["content"]["absorbed"] == matter["content"]["waiting"] == 0
    assert matter["transit"]["waiting"] == 0 and simulation.layer.born > len(gathers)


# -- (d) ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("world", "message"),
    [
        (small_world(key=False), "massive is refused without the world key"),
        (small_world(family_extra={"phase_per_link": 3}), "refused with phase_per_link"),
        (small_world(family_extra={"phase_per_link": [8, 1]}), "refused with phase_per_link"),
        (small_world(family_extra={"phase": False}), "without a phase circle"),
        (small_world(action=None), "needs the world's `action`"),
        (small_world(massive=False), "momentum_magnitude belongs to the lamp of a massive family"),
        (small_world(p=None), "lacks keys: momentum_magnitude"),
        (small_world(age_bound=None), "age_bound is required with the world key"),
        (small_world(m=1 << 29, clock=1 << 40, amount=1 << 40), "has a square beyond the integer bound"),
        # The square E'_D^2 = E'_0^2 + 3 p_D . p_D passes the bound before
        # the turn's rate abs(p_a) N can (3 p^2 > p N for every p beyond N /
        # 3), so the ceiling that fires is the energy's, naming the direction
        # (p = 1.4 x 10^9: 3 p^2 = 5.9 x 10^18 beyond 2^62 - 1); beyond that
        # the label's rounding itself leaves the working bound, refused
        # naming the key before any root is formed.
        (small_world(p=1_400_000_000), "E'_D^2 = E'_0^2 + 3 p_D . p_D ="),
        (small_world(p=1 << 57), "beyond the working bound"),
    ],
)
def test_the_keys_are_refused_at_load_naming_them(world: dict[str, object], message: str):
    """(d)."""
    with pytest.raises(ValueError, match=re.escape(message)):
        parse_nature_beam_world(world)


def test_a_massive_free_family_and_a_massive_family_without_a_lamp_are_refused():
    """(d)."""
    world = small_world()
    world["families"][0]["quantum"] = 0  # type: ignore[index]
    with pytest.raises(ValueError, match="refused on the free family"):
        parse_nature_beam_world(world)
    world = small_world()
    del world["measured"][0]["lamp"]  # type: ignore[index]
    with pytest.raises(ValueError, match="has no lamp"):
        parse_nature_beam_world(world)
    world = small_world()
    second = json.loads(json.dumps(world["measured"][0]))  # type: ignore[index]
    second["position"] = [1, 2, 0]
    second["lamp"]["momentum_magnitude"] = 300
    world["measured"].append(second)  # type: ignore[union-attr]
    with pytest.raises(ValueError, match="declare two momentum_magnitude values"):
        parse_nature_beam_world(world)
    world = small_world()
    world["massive_rows"] = 1
    with pytest.raises(ValueError, match="massive_rows must be true or false"):
        parse_nature_beam_world(world)
    world = small_world()
    world["families"][0]["massive"] = "yes"  # type: ignore[index]
    with pytest.raises(ValueError, match="massive must be true or false"):
        parse_nature_beam_world(world)


def test_a_massive_birth_at_a_turn_other_than_one_is_refused_naming_the_lamp():
    """(d)."""
    simulation = NatureBeamSimulation(parse_nature_beam_world(small_world(amount=1 << 21)))
    with pytest.raises(
        ValueError,
        match=re.escape("measured event 1 at [1, 5, 0] births rows of 'matter' at the turn 2"),
    ):
        simulation.step()


def test_the_inverse_interval_is_refused_on_a_world_with_the_key():
    """(d)."""
    world = {
        "law": "beam",
        "model_id": "massive-inverse",
        "shape": [8, 1, 1],
        "boundary": {"y": "periodic", "z": "periodic"},
        "ticks": 4,
        "K": 64,
        "release": [1, 128],
        "age_bound": 64,
        "massive_rows": True,
        "families": [{"name": "light", "quantum": 1}],
        "measured": [],
        "in_transit": [
            {"position": [2, 0, 0], "family": "light", "number": 1, "direction": [1, 0, 0], "amount": 1}
        ],
    }
    parsed = parse_nature_beam_world(world)
    assert parsed.massive_rows and parsed.hypotheses == [MASSIVE_ROWS_RULE]
    simulation = NatureBeamSimulation(parsed)
    simulation.step()
    with pytest.raises(ValueError, match="inverse interval is refused on a world that declares"):
        simulation.inverse_step()


# -- (e) ---------------------------------------------------------------------------


def momentum_total(books: dict[str, object]) -> list[int]:
    momentum = books["momentum"]
    assert isinstance(momentum, dict)
    return [
        sum(v)
        for v in zip(
            momentum["measured"],
            momentum["transit"],
            momentum["escaped"],
            momentum["cancelled"],
            momentum["remainder"],
            momentum["waiting"],
            strict=True,
        )
    ]


def test_the_books_identities_hold_at_every_step_and_a_completion_places_one_quantum():
    """(e)."""
    lines: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(small_world()), observer=lines.append)
    table = simulation.tables.family_flights[0]
    labels = {tuple(row.tolist()) for row in table.labels}
    completions = 0
    for tick in range(1, 61):
        held_before = {
            n: (e.held[0], e.clicks[0], list(e.momentum)) for n, e in simulation.measured.items()
        }
        waiting_before = simulation.ledger.waiting_content[0]
        cancelled_before = simulation.ledger.cancelled_content[0]
        simulation.step()
        books = simulation.books()
        assert books["balanced"], tick
        matter = books["families"]["matter"]
        assert (
            matter["content"]["absorbed"]
            == matter["measured"]["measured"] + matter["content"]["waiting"]
        )
        clicked = sum(e.clicks[0] for e in simulation.measured.values())
        assert matter["transit"]["absorbed"] == clicked + matter["transit"]["waiting"], tick
        assert momentum_total(books) == [0, 0, 0], tick
        gathers = gathers_of(lines, tick)
        for gather in gathers:
            completions += 1
            assert gather["content"] == M and tuple(v // M for v in gather["momentum"]) in labels
            node = tuple(gather["node"][0])
            name = gather["chosen"][0][0]
            if not name.startswith("screen_"):
                # The diagonals leave the plane through a y face before the
                # screen: a face's completion, its lines the test of (c).
                assert name in ("face:+y", "face:-y")
                continue
            assert name == f"screen_{node[1]}"
            holder = next(e for e in simulation.measured.values() if e.position == node)
            here = sum(1 for g in gathers if tuple(g["node"][0]) == node)
            before = held_before[holder.number]
            assert holder.held[0] - before[0] == M * here and holder.clicks[0] - before[1] == here
            assert holder.momentum != before[2]
        if gathers:
            arrived = sum(
                int(line["content"])
                for line in lines
                if line["event"] == "click" and line["tick"] == tick and line["family"] == "matter"
            )
            waiting_moved = waiting_before - simulation.ledger.waiting_content[0]
            cancelled_moved = simulation.ledger.cancelled_content[0] - cancelled_before
            assert cancelled_moved == waiting_moved + arrived - M * len(gathers)
    assert completions >= 8
    clicks = [line for line in lines if line["event"] == "click" and line["family"] == "matter"]
    # Every click line (a pixel's `push`, a face's `momentum`) carries the
    # row's content M and its label, what arrived; the value said where it
    # went.
    assert clicks and all(line["content"] == M for line in clicks)
    assert all(line.get("push", line.get("momentum")) != [0, 0, 0] for line in clicks)


def test_the_turn_is_the_plane_wave_to_one_remainder():
    """(e): the heading's row after k Links."""
    simulation = NatureBeamSimulation(parse_nature_beam_world(small_world()))
    heading = list(simulation.world.directions).index((1, 0, 0))
    seen = 0
    for tick in range(1, 12):
        simulation.step()
        store = simulation.stores[0]
        for i in np.flatnonzero((store.direction == heading) & (store.record == BASE + 1)).tolist():
            links = int(store.node[i] // store.strides[0]) - 1
            assert int(store.phase[i]) == (links * P * N // H + int(store.birth[i])) % N, tick
            assert int(store.acc_turn[i]) == (links * P * N) % H, tick
            seen += links
    assert seen > 0


def test_two_rows_of_different_remainders_never_merge():
    """(e): `acc_turn` is an identity field of the merge."""
    # `acc_turn` is followed by one identity field, `turn`, the row's own
    # phase rate of atom-level-v1 (2026-09-22), constant 0 without the key
    # `atom_level`; the last field of the massive rows' own is `acc_turn`.
    assert IDENTITY_FIELDS[-2:] == ("acc_turn", "turn")
    store = NatureBeamStore((4, 1, 1))
    one = np.array([1, 1])
    store.append(
        node=one,
        direction=np.array([2, 2]),
        age=one,
        phase=one,
        number=one,
        amount=one,
        content=one,
        arrival=np.array([0, 0]),
        acc_turn=np.array([3, 5]),
    )
    store.merge()
    assert store.size == 2 and store.acc_turn.tolist() == [3, 5]
    store.append(
        node=one[:1],
        direction=np.array([2]),
        age=one[:1],
        phase=one[:1],
        number=one[:1],
        amount=one[:1],
        content=one[:1],
        arrival=np.array([0]),
        acc_turn=np.array([3]),
    )
    store.merge()
    assert store.size == 2
    assert sorted(zip(store.acc_turn.tolist(), store.amount.tolist(), strict=True)) == [(3, 2), (5, 1)]


# -- (f) ---------------------------------------------------------------------------


def test_the_small_two_slit_world_replays_bit_exact(tmp_path: Path):
    """(f)."""
    block = EXPECTATIONS["slits_matter_small"]
    registered = block["replay"]
    path = WORLDS / "slits_matter_small.json"
    source = path.read_bytes()
    assert hashlib.sha256(source).hexdigest() == registered["source_sha256"]
    shipped = GENERATOR.families_by_definition(
        GENERATOR.two_slits_matter_small(), GENERATOR.FAMILY_DEFINITIONS, GENERATOR.DEFINITIONS_SOURCE
    )
    assert source == (json.dumps(shipped) + "\n").encode("utf-8")
    loaded = load_world(source, base_dir=path.parent)
    assert loaded.world.ticks == block["intervals"]
    out = tmp_path / "run"
    out.mkdir()
    execute_nature_beam_run(loaded.world, source, out, "test", loaded.world.ticks)
    assert digests_of(out) == registered["digests"]
    record = json.loads((out / "run.json").read_text(encoding="utf-8"))
    assert record["hypotheses"] == registered["hypotheses"] and MASSIVE_ROWS_RULE in record["hypotheses"]
    assert (
        record["conserved_at_every_completed_tick"]
        and record["completed_ticks"] == registered["intervals"]
    )
    assert record["layer"] == registered["layer"]
    gathers = [
        {
            "record": int(g["record"]) - BASE,
            "tick": g["tick"],
            "u": g["u"],
            "chosen": None if g["chosen"] is None else g["chosen"][0][0],
            "node": g["node"],
            "content": g["content"],
            "momentum": g["momentum"],
        }
        for g in record["world"]
        if BASE + 1 <= int(g["record"]) <= BASE + int(block["births"])
    ]
    assert gathers == registered["gathers"] and len(gathers) == block["births"]
    assert all(g["content"] == M for g in gathers)
    assert record["audit"][-1]["families"]["matter"] == registered["books_at_end"]
    assert record["audit"][-1]["momentum"] == registered["momentum_at_end"]
    assert b'"acc_turn"' in (out / "state.json").read_bytes()


# -- (g) ---------------------------------------------------------------------------


def walk(flight, index: int, start: tuple[int, int], stop):
    """The engine's Bresenham line of a direction from a Node until `stop`
    names an end: (the end, the Node, the Manhattan Links made)."""
    s1 = int(flight.manhattan[index])
    line = flight.lines[index, :s1]
    x, y = start
    made = 0
    while True:
        step = line[made % s1]
        x += int(step[0])
        y += int(step[1])
        made += 1
        end = stop((x, y))
        if end:
            return end, (x, y), made


def age_of(table: FamilyFlight, index: int, made: int) -> int:
    """The first age at which the family's accumulator count reaches `made` Links."""
    rate, wall, start = int(table.rate[index]), int(table.wall[index]), int(table.start[index])
    return max(0, -(-(made * wall - start) // rate))


def test_the_pin_is_derived_from_the_world_and_the_tables():
    """(g)."""
    pin = EXPECTATIONS["slits_matter"]
    path = WORLDS / "slits_matter.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    world = load_world(path.read_bytes(), base_dir=path.parent).world
    assert world.massive_rows and world.hypotheses == ["bohr-v1", "amplitude-v1", MASSIVE_ROWS_RULE]
    assert world.ticks == pin["intervals"] and document["massive_rows"] is True
    assert document["width"] == INTEGERS["S"] and document["action"] == INTEGERS["h"]
    shipped = GENERATOR.families_by_definition(
        GENERATOR.two_slits_matter(), GENERATOR.FAMILY_DEFINITIONS, GENERATOR.DEFINITIONS_SOURCE
    )
    assert path.read_bytes() == (json.dumps(shipped) + "\n").encode("utf-8")
    simulation = NatureBeamSimulation(world)
    flight = simulation.tables.flight
    tables = simulation.tables.family_flights
    matter = next(t for t, f in zip(tables, world.families, strict=True) if f.massive)
    photon = next(t for t, f in zip(tables, world.families, strict=True) if not f.massive)
    assert (matter.placed, matter.quantum) == tuple(INTEGERS["pair"]["matter"])
    assert (photon.placed, photon.quantum) == tuple(INTEGERS["pair"]["wall"])
    directions = list(world.directions)
    diagonal = INTEGERS["flight_table_diagonal"]
    i = directions.index(tuple(diagonal["direction"]))
    assert (int(matter.rate[i]), int(matter.wall[i]), int(matter.start[i])) == (
        diagonal["rate"],
        diagonal["wall"],
        diagonal["start"],
    )
    assert matter.labels[i].tolist() == diagonal["label"] and matter.turn[i].tolist() == diagonal["turn"]
    assert matter.turn_denominator == diagonal["denominator"]
    moving = [k for k, v in enumerate(directions) if any(v)]
    assert {int(matter.start[k]) for k in moving} == {INTEGERS["energy"]}
    assert Fraction(INTEGERS["p"] * N, H) == Fraction(INTEGERS["turn_per_axis_link"])
    assert Fraction(H, INTEGERS["p"]) == Fraction(INTEGERS["wavelength"])
    assert Fraction(INTEGERS["pace"]) == Fraction(INTEGERS["p"], INTEGERS["energy"])
    lamp = next(m for m in document["measured"] if "lamp" in m)
    assert lamp["lamp"]["momentum_magnitude"] == INTEGERS["p"] and lamp["lamp"]["wheel"] == pin["wheel"]
    openings = {
        tuple(m["position"][:2]) for m in document["measured"] if isinstance(m.get("table"), dict)
    }
    walls = {
        tuple(m["position"][:2])
        for m in document["measured"]
        if m["family"] == "wall" and not m.get("table")
    }
    shape = document["shape"]
    screen_x = max(m["position"][0] for m in document["measured"])
    assert screen_x == 52 and sorted(openings) == [(8, 55), (8, 65)]

    def inside(node: tuple[int, int]) -> bool:
        return 0 <= node[0] < shape[0] and 0 <= node[1] < shape[1]

    def stop_lamp(node: tuple[int, int]) -> str:
        if node in walls:
            return "wall"
        if node in openings:
            return "opening"
        return "" if inside(node) else "face"

    def stop_fan(node: tuple[int, int]) -> str:
        if node[0] == screen_x:
            return "screen"
        if not inside(node):
            return "face"
        return "wall" if node in walls else ""

    lamp_xy = tuple(lamp["position"][:2])
    legs = {}
    for vector in lamp["lamp"]["directions"]:
        index = directions.index(tuple(vector))
        end, node, made = walk(flight, index, lamp_xy, stop_lamp)
        legs[tuple(vector)] = (end, made, age_of(matter, index, made), age_of(photon, index, made))
    reaching = {d: v for d, v in legs.items() if v[0] == "opening"}
    assert sorted(reaching) == [(1, -1, 0), (1, 1, 0)] and all(v[1] == 11 for v in reaching.values())
    assert max(v[2] for v in reaching.values()) == pin["lamp_leg"]["value"] == 139
    assert max(v[3] for v in reaching.values()) == 13
    assert (
        legs[(1, 0, 0)][0] == "wall" and legs[(2, 1, 0)][0] == "wall" and legs[(2, -1, 0)][0] == "wall"
    )
    fan_entry = next(m for m in document["measured"] if isinstance(m.get("table"), dict))
    fan = [tuple(v) for v in fan_entry["directions"]]
    assert len(fan) == 1327 and "matter" in fan_entry["table"] and "light" not in fan_entry["table"]
    first: dict[int, int] = {}
    longest = 0
    for opening in openings:
        for vector in fan:
            index = directions.index(vector)
            end, node, made = walk(flight, index, opening, stop_fan)
            tau = age_of(matter, index, made)
            longest = max(longest, tau)
            if end == "screen":
                first[node[1]] = min(first.get(node[1], 10**9), tau)
    rerelease = 1 + pin["lamp_leg"]["value"]
    assert rerelease == pin["first_rerelease_tick"]
    for name, entry in pin["first_click_tick"].items():
        assert rerelease + first[int(name.split("_")[1])] == entry["value"], name
    # The pace in the row's own clock (2026-09-22): the row's `age` on its
    # first `click` line at the pixel, the first fan row's flight by the
    # accumulator rule; the click's tick is the re-release plus this age.
    for name, entry in pin["first_click_age"].items():
        assert first[int(name.split("_")[1])] == entry["value"], name
        assert entry["value"] + rerelease == pin["first_click_tick"][name]["value"]
    assert longest == pin["longest_row"]["value"]
    assert pin["births"] + pin["lamp_leg"]["value"] + longest <= pin["intervals"]
    small = EXPECTATIONS["slits_matter_1024"]
    assert small["intervals"] >= small["births"] + small["lamp_leg"] + longest
    other = json.loads((WORLDS / "slits_matter_1024.json").read_text(encoding="utf-8"))
    assert (
        other["measured"][0]["lamp"]["wheel"] == small["wheel"] and other["ticks"] == small["intervals"]
    )
