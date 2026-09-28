"""The recoil's folder: the turn of the body's record's phase per Link by delta k = sigma_a x (k_q div M) on the record's two time levels, the angle's remainder carried at the body so the turns over clicks sum to the exact floor, the direction of travel, the refusals and the declaration; in the loop, a giver's record turned at its window's close opposite to the given light and its momentum read from the record's current."""

import json
import sys
from math import atan, cos, pi, tan
from pathlib import Path

import numpy as np
import pytest

import event_universe.world_files as world_files
from event_universe.core.register import folder_of
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.features.recoil import (
    DECLARATION,
    GIVING,
    TAKING,
    THE_WORD,
    RecoilOwn,
    RecoilStart,
    RecoilTerm,
    RecoilWrites,
    apply,
    sign_of,
)
from event_universe.world_files import input_stamp, load_world, parse_nature_beam_world
from tests.running import lines_of
from tests.worlds import emitter_world

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from reversible import forward, reversible_row, step_back  # noqa: E402

GENERATED = ROOT / "examples" / "events" / "experiments" / "universe.json"  # the universe of record
START = ROOT / "examples" / "events" / "engine_start.json"
UNIT, CLOCK = (
    1 << 20,
    (153 * 10**6, 10**8),
)  # the test's twist unit: theta_unit = 1 / UNIT radians; 2 cos omega_b = 1.53 at a fine unit (the mode's clock is at the amplitude unit)
AMPLITUDE, NODES = 1_000_000, 9
WAVE, K_Q = (
    0.3,
    round(0.05 * UNIT),
)  # the phase per Link before the click (radians); the wave number in the twist's unit


def triple_of(angle: int, _axis: int) -> tuple[int, int, int]:  # the exact triple nearest the angle
    m = 1_000_000
    j = round(m * tan(abs(angle) / UNIT / 2))
    return (m * m - j * j, (1 if angle >= 0 else -1) * 2 * m * j, m * m + j * j)


def plane_wave(k: float, phase: float) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """The two time levels of A cos(k x - phase) about the centre Node, before one rotation omega_b earlier."""
    omega = 2 * atan(((4 * CLOCK[1] ** 2 - CLOCK[0] ** 2) ** 0.5) / (CLOCK[0] + 2 * CLOCK[1]))
    now = tuple(round(AMPLITUDE * cos(k * (x - NODES // 2) - phase)) for x in range(NODES))
    before = tuple(round(AMPLITUDE * cos(k * (x - NODES // 2) - phase + omega)) for x in range(NODES))
    return now, before


OFFSETS = (tuple(x - NODES // 2 for x in range(NODES)), (0,) * NODES, (0,) * NODES)


def current(
    levels: tuple[tuple[int, ...], tuple[int, ...]],
) -> int:  # the count's line's current along +x
    now, before = levels
    return sum(now[i + 1] * before[i] - before[i + 1] * now[i] for i in range(NODES - 1))


TERM = RecoilTerm(K_Q, 1, CLOCK, TAKING, triple_of)
GIVER = {"family": "charge", "weight": 1, "norm": 100, "norm_denominator": 1, "receiver": ["strip"]}
NODES_OF_THE_GIVER = [{"node": [1, 0, 0], "count": 1}, {"node": [2, 0, 0], "count": 1}]
FACES = {"x": "closed", "y": "periodic", "z": "periodic"}
STRIP = {"name": "strip", "positions": [[2, 0, 0]]}  # the set on the body's own Node


def test_the_turn_moves_the_records_phase_per_link_by_delta_k_on_both_time_levels():
    """A record A cos(k x - phase) with before one rotation earlier, turned at M = 1 by k_q along +x: every Node's two levels are those of the same wave at k + delta k, delta k = k_q theta_unit, to the rounding of the table's triple and the nearest unit (the quad level from the two time levels and the clock, the determinant one); a taking at sigma_x = +1 turns by +delta k, a giving by -delta k, the centre Node (the offset 0) untouched."""
    now, before = plane_wave(WAVE, 0.7)
    for sense, sign in ((TAKING, 1), (GIVING, -1)):
        term = RecoilTerm(K_Q, 1, CLOCK, sense, triple_of)
        writes = apply(term, RecoilStart((5, 0, 0), (now, before), OFFSETS), RecoilOwn({}, {}))
        expected_now, expected_before = plane_wave(WAVE + sign * K_Q / UNIT, 0.7)
        assert writes.turn == (sign * K_Q, 0, 0)
        assert all(abs(a - b) <= 3 for a, b in zip(writes.levels[0], expected_now, strict=True))
        assert all(abs(a - b) <= 3 for a, b in zip(writes.levels[1], expected_before, strict=True))
        centre = NODES // 2
        assert writes.levels[0][centre] == now[centre] and writes.levels[1][centre] == before[centre]
        # the record's current along +x (the count's line's booking) grows with the phase per Link and shrinks against it: the velocity moves with the turn
        assert sign * (current(writes.levels) - current((now, before))) > 0


def test_the_angles_remainder_carried_at_the_body_makes_the_turns_the_exact_floor():
    """delta k = (sense sigma k_q + r) div M with r carried at the body under the axis's key: at k_q = 7 and M = 3 three takings turn by 2, 2 and 3 (the exact floors of 7 / 3, 14 / 3 and 21 / 3); a giving after a taking returns the remainder to 0 and the turns cancel; sigma is the tally's sign and never its size; an axis without a tally turns by nothing."""
    now, before = plane_wave(WAVE, 0.0)

    def turn(sense: int, tally: tuple[int, int, int], own: RecoilOwn) -> RecoilWrites:
        term = RecoilTerm(7, 3, CLOCK, sense, triple_of)
        return apply(term, RecoilStart(tally, (now, before), OFFSETS), own)

    own, turns = RecoilOwn({}, {}), []
    for _ in range(3):
        writes = turn(TAKING, (1, 0, 0), own)
        own, turns = writes.own, [*turns, writes.turn[0]]
    assert turns == [2, 2, 3] and own.carries[(0,)] == 0 and own.values[(0,)] == 3
    take = turn(TAKING, (10**6, 0, 0), RecoilOwn({}, {}))
    give = turn(GIVING, (1, 0, 0), take.own)
    assert take.turn == (2, 0, 0) and give.turn == (-2, 0, 0) and give.own.carries[(0,)] == 0
    still = apply(TERM, RecoilStart((0, 0, 0), (now, before), OFFSETS), RecoilOwn({}, {}))
    assert still.turn == (0, 0, 0) and still.levels == (now, before)
    assert [sign_of(v) for v in (-3, 0, 5)] == [-1, 0, 1] and TAKING == 1 and GIVING == -1


def test_the_bounds_and_the_terms_are_refused_by_name():
    """The wave number from 0 and the count from 1; the sense +1 or -1; a clock that is no rotation (the sine from 1 on one); the levels and the offsets over the same Nodes."""
    now, before = plane_wave(WAVE, 0.0)
    start = RecoilStart((1, 0, 0), (now, before), OFFSETS)
    with pytest.raises(ValueError, match="got k_q = -1, M = 1"):
        apply(RecoilTerm(-1, 1, CLOCK, TAKING, triple_of), start, RecoilOwn({}, {}))
    with pytest.raises(ValueError, match="count from 1, got k_q = 7, M = 0"):
        apply(RecoilTerm(7, 0, CLOCK, TAKING, triple_of), start, RecoilOwn({}, {}))
    with pytest.raises(ValueError, match=r"sense is \+1 \(a taking\) or -1 \(a giving\), got 2"):
        apply(RecoilTerm(7, 1, CLOCK, 2, triple_of), start, RecoilOwn({}, {}))
    with pytest.raises(ValueError, match=r"clock \[2000, 1000\] is no rotation"):
        apply(RecoilTerm(7, 1, (2000, 1000), TAKING, triple_of), start, RecoilOwn({}, {}))
    with pytest.raises(ValueError, match="over the body's Nodes alike, got 9, 8"):
        apply(TERM, RecoilStart((1, 0, 0), (now, before[:-1]), OFFSETS), RecoilOwn({}, {}))


def giver_world(tmp_path: Path, monkeypatch, wave_number: int) -> Path:
    """A giving body of two Nodes one Node off the closed -x face (its light's tally one way along x within the window) in the law's form on the generated universe (its twist table), its mode file beside it with the quantum's `wave_number`, the strip on its own Node."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    (tmp_path / "universe.json").write_text(GENERATED.read_text(encoding="utf-8"), encoding="utf-8")
    (tmp_path / "start.json").write_text(START.read_text(encoding="utf-8"), encoding="utf-8")
    body = {"family": "matter", "moment": [0, 0, 1], "stocks": {"charge": 4}, "emitter": GIVER, "q": 1}
    body.update(nodes=NODES_OF_THE_GIVER, momentum=[0, 0, 0], momentum_before=[0, 0, 0])
    world = {"shape": [16, 1, 1], "boundary": FACES, "ticks": 400, "N": 1024, "measured": [body]}
    world.update(universe="universe.json", engine="start.json", detectors=[STRIP])
    world["stamp"] = input_stamp(world)
    (tmp_path / "giver.json").write_text(json.dumps(world), encoding="utf-8")
    entry = {"family": "matter", "pair": [800, 1200], "profile": [0, 1000, 1000] + [0] * 13}
    entry.update(clock=list(CLOCK), twist=45875, wavelength=7, wave_number=wave_number)
    mode = {"world_digest": world["stamp"]["hash"], "bodies": [entry]}
    (tmp_path / "giver.mode.json").write_text(json.dumps(mode), encoding="utf-8")
    return tmp_path / "giver.json"


def test_in_the_loop_the_givers_record_turns_at_the_close_opposite_to_the_light_and_n_is_a_reading(
    tmp_path, monkeypatch
):
    """The loop: the giver's mode carries `wave_number`; at its window's close the `recoil` line names the body at the sense -1, the giving's tally along x and the turn (-sigma_x k_q) div M along the light's axis (opposite to the given light), the books summing the turns per body and the angle's remainder on the body under the recoil's key; the body's momentum is the reading of its record's current at every interval, W x the current over the form to the nearest unit (recomputed here from the record's levels), both levels one reading; across the close the host undoes the turn from the copy on the recoil's line (the click keeps the click): the body's own record returns bit for bit, and the reversible row's reading is the same with the turn and without it."""
    unit = json.loads(GENERATED.read_text(encoding="utf-8"))["integers"]["twist_table"]["unit"]
    wave_number = round(unit * 2 * pi / 7) // 100  # a slow quantum: the turn inside the table's angles
    world = load_world(path := giver_world(tmp_path, monkeypatch, wave_number))
    simulation = DetectorLawSimulation(world, observer=(lines := []).append)
    block, quanta = simulation.blocks[0], sum(world.measured[0].block.counts)  # M the body's count
    while not lines_of(lines, "recoil") and simulation.tick < world.ticks:
        wall = simulation.wall_of(block)  # W as the interval starts, before the giving's open
        simulation.step()
        live, weight = block.own, simulation.kind_wall(block.family, block.definition.pair)
        flow = sum(
            int(live.now[x + 1, 0, 0]) * int(live.before[x, 0, 0])
            - int(live.before[x + 1, 0, 0]) * int(live.now[x, 0, 0])
            for x in range(world.shape[0] - 1)
        )
        reading = round(wall * weight * flow / (block.count_norm * quanta))
        assert abs(block.momentum[0] - reading) <= 1 and block.momentum[1:] == [0, 0]
        assert block.momentum_before == block.momentum
    (recoil,), (giving,) = lines_of(lines, "recoil"), lines_of(lines, "giving")
    assert (recoil["sense"], recoil["measured"], recoil["tick"]) == (GIVING, 0, giving["tick"])
    sigma = giving["momentum"][0]  # the light's direction along x, the tally's sign
    assert sigma != 0 and recoil["turn"] == [(-sigma * wave_number) // quanta, 0, 0]
    assert simulation.recoil_turns == {0: recoil["turn"]} and recoil["tally"][0] * sigma > 0
    assert block.hold_carry[("recoil", 0)] == (-sigma * wave_number) % quanta

    def build() -> tuple[DetectorLawSimulation, list[dict]]:
        found: list[dict] = []
        return DetectorLawSimulation(load_world(path), observer=found.append), found

    row = reversible_row(build, recoil["tick"])
    back, lines = build()
    step_back(back, lines, *forward(back, lines, recoil["tick"])[1:], recoil["tick"])
    fresh, _ = build()
    for _ in range(recoil["tick"] - 1):
        fresh.step()
    own, then = back.blocks[0].own, fresh.blocks[0].own
    assert all(np.array_equal(getattr(own, k), getattr(then, k)) for k in ("now", "before", "remainder"))
    mode = json.loads((tmp_path / "giver.mode.json").read_text(encoding="utf-8"))
    mode["bodies"][0].pop("wave_number")  # the same world without the turn
    (tmp_path / "giver.mode.json").write_text(json.dumps(mode), encoding="utf-8")
    assert reversible_row(build, recoil["tick"])["read"] == row["read"]


def test_the_declaration_is_the_ledgers_row():
    """The folder declares the row of ALGEBRA.md #the-primitives: "the recoil" at (iv), writing a family's level at a Node (the body's own record) and a body's remainders, its function `apply`, its section; the engine's register finds it; a giver off the mode (no wave number) takes no recoil."""
    assert DECLARATION.name == "the recoil" and DECLARATION.place == "(iv)"
    assert DECLARATION.writes == ("a family's level at a Node", "a body's remainders")
    assert (
        DECLARATION.function is apply and DECLARATION.built and folder_of(DECLARATION.name) == "recoil"
    )
    assert DECLARATION.section.startswith(THE_WORD) and DECLARATION.word == "after the step"
    simulation = DetectorLawSimulation(parse_nature_beam_world(emitter_world(stock=1, ticks=2)))
    registered = simulation.register.declarations["the recoil"]
    assert registered.reads == DECLARATION.reads and registered.function is apply
    assert registered.place_of("a family's level at a Node") == "(iv)"
    assert "the twist table" in DECLARATION.reads
    # a giver whose mode carries no wave number takes no recoil (the fixture off the mode, tests/worlds.py)
    off_mode = simulation.world.measured[0].block
    assert off_mode is not None and off_mode.emitter is not None and off_mode.emitter.wave_number is None
    assert simulation.recoil_turns == {}
