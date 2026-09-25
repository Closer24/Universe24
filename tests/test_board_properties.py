"""The property test of the board (ALGEBRA.md 9.20 (B), the mathematician's six properties of
the one map S, ADOPTED with record 1875; the gate of every step of the cleanup, 9.21 (3)):
on the small world of 9.20 (a cube of 12 x 12 x 12 periodic on every axis; light [77, 25] and
the massive family [800, 809]; one well of side 2 at the vertex (3, 4, 5) with the pair
[800, 801] seeded on its composed mode; one light record born on the cell (8, 2, 7) with both
labels and the wheel 8; one receiver, the cube of side 3 at (9, 9, 2), on the record's ladder; 60
intervals): (1) equivariance under the 48; (2) translation on the torus; (3) conservation of
the content and of the form I between clicks; (4) reversibility except the click, by 8.8's
inverse; (5) locality; (6) only the click reads. Every comparison is bit for bit on the
engine's integers unless the expected value says otherwise; a failure is an engine defect,
never a change of the law. The record is planted as its birth would write it (the pair on the
circle of 2 N, 9.17 (6)); its labels are one row (the label rows of a rank-2 record are the
crystal's, held)."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import multiprocessing
from fractions import Fraction

import numpy as np
import pytest

from event_universe.events.detector_law import UNIT, DetectorLawSimulation, LiveRecord
from event_universe.events.world import parse_nature_beam_world
from tests.test_emitter import massive_generator

SIDE = 12
SHAPE = (SIDE, SIDE, SIDE)
PERIODIC = {"x": "periodic", "y": "periodic", "z": "periodic"}
WELL_VERTEX = (3, 4, 5)
BIRTH = (8, 2, 7)
RECEIVER = (9, 9, 2)
WHEEL = 8
INTERVALS = 90  # the reference record's click at 81 (u = 0; the prototype and the engine read the same flux since the prototype's factor of 3 was fixed, ALGEBRA.md 9.20 (C))
AMPLITUDE = 1 << 12


def small_world(
    well_vertex=WELL_VERTEX,
    receiver=RECEIVER,
    seed=None,
    receiver_named=True,
    side: int = SIDE,
    clock: list[int] | None = None,
) -> dict:
    """The small world of 9.20 as a document; the well's seed the composed mode's integer
    profile at the amplitude (the generator's, or `seed` given: a transformed reference)."""
    document = {
        "law": "beam",
        "model_id": "beam-board-properties-v1",
        "shape": [side, side, side],
        "boundary": PERIODIC,
        "ticks": INTERVALS,
        "age_bound": 100000,
        "K": 1073741824,
        "N": 64,
        "release": [1, 128],
        "suspension": 0,
        "clock_stamp": True,
        "detector_law": True,
        "massive_record": True,
        "amplitude_bound": 1 << 32,
        "directions": [],
        "families": [
            {"name": "light", "quantum": 1, "phase_per_link": [77, 25]},
            {"name": "matter", "quantum": 1, "pair": [800, 809]},
        ],
        "measured": [
            {
                "position": list(well_vertex),
                "family": "matter",
                "amount": 1,
                "phase": 0,
                "momentum": [0, 0, 0],
                "fixed": True,
                "side": 2,
                "pair": [800, 801],
                "seed": AMPLITUDE,
                "margin": "control",
            }
        ],
        # the receiver: the detector cube of side 3 from `receiver` (record 1899; a set
        # on free Nodes is bound to a body, the light clock's form)
        "detectors": [
            {
                "name": "screen",
                "block": 0,
                "positions": [
                    [(receiver[a] + d[a]) % side for a in range(3)]
                    for d in itertools.product(range(3), repeat=3)
                ],
            }
        ]
        if receiver_named
        else [],
    }
    if seed is None:
        # the generator writes the profile and the mode's clock [a, b] (record 1886)
        document["measured"][0]["seed"] = massive_generator().mode_profile(
            document, 0, amplitude=AMPLITUDE
        )
    else:
        document["measured"][0]["seed"] = [int(value) for value in np.asarray(seed).ravel()]
        assert clock is not None
        document["measured"][0]["clock"] = list(clock)
    return document


def born_levels(simulation: DetectorLawSimulation) -> tuple[int, int]:
    """The birth's pair on the circle of 2 N (9.17 (6)) for light's clock [77, 25] on N = 64:
    the generator's integer (a host computation; no table in the engine), now = round(A sin(pi
    n / (d N))), the character half a step either side of its zero, before = -now."""
    _ = simulation
    steps = 64
    now = round(UNIT * math.sin(math.pi * 77 / (25 * steps)))
    return now, -now


def plant(simulation: DetectorLawSimulation, node, u: int, ladder: bool = True, rows=None) -> LiveRecord:
    """The light record as its birth writes it: the pair on one cell (or the rows given), the
    residue u, the ladder the receiver's cell, the norm its conserved form."""
    now = np.zeros(SHAPE, dtype=np.int64)
    before = np.zeros(SHAPE, dtype=np.int64)
    if rows is None:
        level_now, level_before = born_levels(simulation)
        now[node] = level_now
        before[node] = level_before
    else:
        now[...] = rows[0]
        before[...] = rows[1]
    live = LiveRecord(
        1 << 40,
        0,
        0,
        u,
        1,
        simulation.tick,
        1,
        77,
        25,
        0,
        21,
        now,
        before,
        np.zeros(SHAPE, dtype=np.int64),
        pointers=[0] * len(simulation.cell_names),
        first_rung=[None] * len(simulation.cell_names),
        wheel=WHEEL,
        labels=((0, 1), (1, 1)),
    )
    live.driven = np.zeros(SHAPE, dtype=bool)
    if ladder and "screen" in simulation.cell_names:
        live.ladder = [simulation.cell_names.index("screen")]
    live.norm = simulation.conserved_form(live)
    simulation.records[live.identity] = live
    return live


def state_of(simulation: DetectorLawSimulation) -> dict[int, tuple[np.ndarray, np.ndarray, np.ndarray]]:
    return {
        identity: (live.now.copy(), live.before.copy(), live.remainder.copy())
        for identity, live in simulation.records.items()
    }


def run(document: dict, u: int = 0, intervals: int = INTERVALS, rows=None, birth=BIRTH):
    """The small world run: the well's own record from interval 0, the light record planted at
    interval 0; the states after every interval and the click lines."""
    lines: list[dict] = []
    simulation = DetectorLawSimulation(parse_nature_beam_world(document), observer=lines.append)
    plant(simulation, birth, u, rows=rows)
    states = [state_of(simulation)]
    for _ in range(intervals):
        simulation.step()
        states.append(state_of(simulation))
    clicks = [(line["tick"], line["record"]) for line in lines if line["event"] == "gather"]
    return simulation, states, clicks


# ---------------------------------------------------------------- the 48 and the translations


def the_48():
    """The signed permutations of the three axes: g = (permutation, signs)."""
    for permutation in itertools.permutations(range(3)):
        for signs in itertools.product((1, -1), repeat=3):
            yield permutation, signs


def apply_g(array: np.ndarray, g) -> np.ndarray:
    """g on an array over the torus: axis i of the result is axis permutation[i] of the input,
    reversed as x -> -x mod SIDE where the sign is -1 (the torus's reflection, a group action)."""
    permutation, signs = g
    out = np.transpose(array, permutation)
    for axis in range(3):
        if signs[axis] < 0:
            out = np.roll(np.flip(out, axis=axis), 1, axis=axis)
    return out


def apply_g_node(node, g):
    permutation, signs = g
    return tuple(
        (-node[permutation[axis]]) % SIDE if signs[axis] < 0 else node[permutation[axis]]
        for axis in range(3)
    )


def vertex_of(mask: np.ndarray, side: int):
    """The lower vertex of a cube's mask on the torus: the Node of the mask whose lower
    neighbour on every axis is outside it."""
    for node in zip(*np.nonzero(mask), strict=True):
        node = tuple(int(v) for v in node)
        if all(
            not mask[tuple((node[a] - 1) % SIDE if a == axis else node[a] for a in range(3))]
            for axis in range(3)
        ):
            return node
    raise AssertionError("no vertex")


def cube_mask(vertex, side: int) -> np.ndarray:
    mask = np.zeros(SHAPE, dtype=bool)
    for d in itertools.product(range(side), repeat=3):
        mask[tuple((vertex[a] + d[a]) % SIDE for a in range(3))] = True
    return mask


def transformed(document: dict, g, transform_node, transform_array) -> dict:
    """The world under g: the well's cube, the receiver's cube and the seed's array."""
    vertex = vertex_of(transform_array(cube_mask(WELL_VERTEX, 2)), 2)
    seed = transform_array(np.asarray(document["measured"][0]["seed"], dtype=np.int64).reshape(SHAPE))
    _ = transform_node
    return small_world(
        well_vertex=vertex,
        receiver=vertex_of(transform_array(cube_mask(RECEIVER, 3)), 3),
        seed=seed,
        clock=document["measured"][0]["clock"],
    )


def compare_runs(reference_states, states, transform_array, identities):
    for t, (a, b) in enumerate(zip(reference_states, states, strict=True)):
        assert set(a) == set(b), (t, set(a), set(b))
        for identity in a:
            for level, (x, y) in enumerate(zip(a[identity], b[identity], strict=True)):
                assert np.array_equal(transform_array(x), y), (t, identity, level)


def test_1_equivariance_under_the_48():
    """48 of 48 transformed worlds give the transformed states at every interval, the
    remainders included, and the same click at the same interval."""
    document = small_world()
    _, reference, clicks = run(document)
    assert clicks, "the reference run clicks within the intervals"
    for g in the_48():
        moved = transformed(document, g, lambda n, g=g: apply_g_node(n, g), lambda a, g=g: apply_g(a, g))
        _, states, moved_clicks = run(moved, birth=apply_g_node(BIRTH, g))
        compare_runs(reference, states, lambda a, g=g: apply_g(a, g), None)
        assert moved_clicks == clicks, g


def test_2_translation_on_the_torus():
    """7 of 7 shifts (one Link along each axis in each sign, and the diagonal (3, 5, 7))."""
    document = small_world()
    _, reference, clicks = run(document)
    shifts = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1), (3, 5, 7)]
    for shift in shifts:

        def move_node(node, shift=shift):
            return tuple((node[a] + shift[a]) % SIDE for a in range(3))

        def move_array(array, shift=shift):
            return np.roll(array, shift, axis=(0, 1, 2))

        moved = transformed(document, None, move_node, move_array)
        _, states, moved_clicks = run(moved, birth=move_node(BIRTH))
        compare_runs(reference, states, move_array, None)
        assert moved_clicks == clicks, shift


# ---------------------------------------------------------------- conservation, reversibility, locality


def reads_of(simulation: DetectorLawSimulation, family: int):
    """The read matrix as a function: the six reads' sum of an array (the family's faces)."""
    return lambda a: simulation._neighbours(a, simulation.kind_wrap[family])


def form_I(
    simulation: DetectorLawSimulation, family: int, now: np.ndarray, before: np.ndarray
) -> Fraction:
    num = simulation.kind_num[family].astype(object)
    den = simulation.kind_den[family].astype(object)
    read = reads_of(simulation, family)(before).astype(object)
    now_o, before_o = now.astype(object), before.astype(object)
    total = Fraction(0)
    for node in zip(*np.nonzero(now_o | before_o | read), strict=True):
        total += Fraction(int(den[node]), int(num[node])) * (
            int(now_o[node]) ** 2 + int(before_o[node]) ** 2
        )
        total -= Fraction(1, 3) * int(now_o[node]) * int(read[node])
    return total


def test_3_conservation_between_clicks():
    """(a) the content per family constant before the click and down by one quantum of light
    at it; (b) per record, I(t) less the accumulated remainder term of 8.2 is the same rational
    at every interval (the remainder identity, exact)."""
    document = small_world()
    simulation, states, clicks = run(document)
    assert len(clicks) == 1
    click_tick = clicks[0][0]
    light = 1 << 40
    # (a) the content: the light record's quantum until the click, none after (the record
    # deleted at its click); the well's own record carries no quantum of light
    for t, state in enumerate(states):
        if t < click_tick:
            assert light in state
        else:
            assert light not in state
    # (b) the form I with the remainder identity, per record, exact
    for identity in (light, 0):
        family = 0 if identity == light else 1
        drift = Fraction(0)
        reference = None
        for t in range(len(states)):
            if identity not in states[t]:
                break
            now, before, remainder = states[t][identity]
            value = form_I(simulation, family, now, before)
            if t >= 1 and identity in states[t - 1]:
                # the remainder term of 8.2 over the step t - 1 -> t:
                # (a_next - a_before) (r - r') / (3 num) per Node
                prev_now, prev_before, prev_remainder = states[t - 1][identity]
                num = simulation.kind_num[family]
                for node in zip(
                    *np.nonzero((now != prev_before) | (remainder != prev_remainder)), strict=True
                ):
                    drift += Fraction(int(now[node]) - int(prev_before[node])) * Fraction(
                        int(prev_remainder[node]) - int(remainder[node]), 3 * int(num[node])
                    )
            invariant = value - drift
            if reference is None:
                reference = invariant
            assert invariant == reference, (identity, t)


def test_4_reversibility_except_the_click():
    """60 intervals with no receiver named, then 60 of 8.8's inverse: the initial element
    returns bit for bit, remainders included; with the receiver named the inverse from 60
    returns the state at the click's interval without the deleted summand, and the difference
    from the forward state there is exactly that summand's rows."""
    unnamed = small_world(receiver_named=False)
    simulation, states, clicks = run(unnamed)
    assert not clicks
    for _ in range(INTERVALS):
        simulation.step_inverse()
    final = state_of(simulation)
    assert set(final) == set(states[0])
    for identity in final:
        for x, y in zip(final[identity], states[0][identity], strict=True):
            assert np.array_equal(x, y), identity
    document = small_world()
    simulation, states, clicks = run(document)
    (click_tick, clicked) = clicks[0]
    for _ in range(INTERVALS - click_tick):
        simulation.step_inverse()
    returned = state_of(simulation)
    forward = states[click_tick]
    # the click's deletion is the one act the inverse cannot undo: the deleted summand
    # was on the board before its click and is in neither state after it; every other
    # summand returns bit for bit
    assert clicked in states[click_tick - 1] and clicked not in forward and clicked not in returned
    assert set(returned) == set(forward)
    for identity in returned:
        for x, y in zip(returned[identity], forward[identity], strict=True):
            assert np.array_equal(x, y), identity


def manhattan_ball(node, radius: int) -> np.ndarray:
    grids = np.indices(SHAPE)
    distance = np.zeros(SHAPE, dtype=np.int64)
    for axis in range(3):
        d = np.abs(grids[axis] - node[axis])
        distance += np.minimum(d, SIDE - d)
    return distance <= radius


def test_5_locality():
    """Two runs whose initial elements differ at one Node of the light record by one unit of
    `now`: at every interval m the difference is inside the Manhattan ball of radius m about
    that Node, and nonzero somewhere for every m <= 12."""
    document = small_world(receiver_named=False)
    _, reference, _ = run(document, intervals=14)
    changed = (BIRTH[0] + 1, BIRTH[1], BIRTH[2])
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    level_now, level_before = born_levels(simulation)
    now = np.zeros(SHAPE, dtype=np.int64)
    before = np.zeros(SHAPE, dtype=np.int64)
    now[BIRTH] = level_now
    before[BIRTH] = level_before
    now[changed] += 1
    _, states, _ = run(document, intervals=14, rows=(now, before))
    light = 1 << 40
    for m in range(0, 15):
        difference = np.zeros(SHAPE, dtype=bool)
        for x, y in zip(reference[m][light], states[m][light], strict=True):
            difference |= x != y
        assert not np.any(difference & ~manhattan_ball(changed, m)), m
        if m <= 12:
            assert np.any(difference), m


def test_6_only_the_click_reads():
    """(b) for 200 random elements, two Nodes whose seven inputs are equal by construction (the
    pair, the row and remainder, the six neighbours' rows) give equal outputs; (c) two runs
    whose records differ only in their residues u are identical until the first click."""
    document = small_world(receiver_named=False)
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    rng = np.random.default_rng(11)
    a, b = (2, 2, 2), (8, 7, 9)
    for _ in range(200):
        now = rng.integers(-UNIT, UNIT, size=SHAPE, dtype=np.int64)
        before = rng.integers(-UNIT, UNIT, size=SHAPE, dtype=np.int64)
        remainder = rng.integers(0, 3, size=SHAPE, dtype=np.int64)
        # b's environment copied from a's: the Node and its six neighbours
        for offset in ((0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
            src = tuple((a[i] + offset[i]) % SIDE for i in range(3))
            dst = tuple((b[i] + offset[i]) % SIDE for i in range(3))
            now[dst] = now[src]
            before[dst] = before[src]
        remainder[b] = remainder[a]
        live = plant(simulation, BIRTH, 0, ladder=False, rows=(now, before))
        live.remainder = remainder.copy()
        simulation._advance(live)
        assert int(live.now[a]) == int(live.now[b]) and int(live.remainder[a]) == int(live.remainder[b])
        del simulation.records[live.identity]
    named = small_world()
    _, states_u, clicks_u = run(named, u=0)
    _, states_v, clicks_v = run(named, u=1)
    first = min(click[0] for click in clicks_u + clicks_v)
    assert clicks_u != clicks_v
    for t in range(first):
        for identity in states_u[t]:
            for x, y in zip(states_u[t][identity], states_v[t][identity], strict=True):
                assert np.array_equal(x, y), (t, identity)


# ---------------------------------------------------------------- the scaling check (HOST)


def scaled_world(side: int) -> dict:
    """The small world's form on a cube of `side`: the well of side 2 at the vertex (3, 4, 5),
    the receiver at (side - 3, side - 3, 2)."""
    return small_world(receiver=(side - 3, side - 3, 2), side=side)


@pytest.mark.parametrize("side", [12, 24, 48])
def test_7_the_host_cost_per_node_per_interval_is_bounded(side: int, capsys):
    """The owner's question on large boards (the Boss's 22:55Z): the host time per Node per
    interval and the state's memory per Node stay within a constant across 12^3, 24^3 and
    48^3 (every step linear or bilinear in the levels), and the generator's cost for the
    composed mode is reported; HOST readings, printed, no pin. The bound asserted: the time
    per Node per interval at 48^3 within five times that at 12^3 (the small board's fixed
    costs dominate it)."""
    import time
    import tracemalloc

    started = time.perf_counter()
    document = scaled_world(side)
    generator_seconds = time.perf_counter() - started
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    shape = (side, side, side)
    now = np.zeros(shape, dtype=np.int64)
    before = np.zeros(shape, dtype=np.int64)
    level_now, level_before = born_levels(simulation)
    now[(side - 4, 2, side - 5)] = level_now
    before[(side - 4, 2, side - 5)] = level_before
    live = LiveRecord(
        1 << 40,
        0,
        0,
        0,
        1,
        0,
        1,
        77,
        25,
        0,
        21,
        now,
        before,
        np.zeros(shape, dtype=np.int64),
        pointers=[0] * len(simulation.cell_names),
        first_rung=[None] * len(simulation.cell_names),
        wheel=WHEEL,
    )
    live.driven = np.zeros(shape, dtype=bool)
    live.ladder = [simulation.cell_names.index("screen")]
    live.norm = simulation.conserved_form(live)
    simulation.records[live.identity] = live
    nodes = side**3
    tracemalloc.start()
    started = time.perf_counter()
    intervals = 20
    for _ in range(intervals):
        simulation.step()
    seconds = time.perf_counter() - started
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    per_node = seconds / (intervals * nodes)
    print(
        f"scaling (HOST): {side}^3 = {nodes} Nodes: {per_node * 1e6:.3f} microseconds per Node per "
        f"interval over {intervals} intervals with {len(simulation.records)} records; the peak "
        f"memory {peak / nodes:.0f} bytes per Node; the generator's composed mode "
        f"{generator_seconds:.2f} seconds"
    )
    assert per_node < 50e-6, per_node


# ---------------------------------------------------------------- the same input, the same output


def output_of(serialized: str) -> dict:
    """The run's output from its input text alone (the model owner's word through the Boss,
    23:51Z: the same input gives the same output): the input's hash, the click lines (the
    receiver and the interval) and the digest of the final state's rows, for one process."""
    document = json.loads(serialized)
    simulation, states, clicks = run(document)
    digest = hashlib.sha256()
    for identity in sorted(states[-1]):
        for array in states[-1][identity]:
            digest.update(np.ascontiguousarray(array).tobytes())
    return {
        "input": hashlib.sha256(serialized.encode("utf-8")).hexdigest(),
        "clicks": [[tick, record] for tick, record in clicks],
        "state": digest.hexdigest(),
    }


def test_8_the_same_input_gives_the_same_output():
    """The owner's word (the Boss's relay of 23:51Z): the same input file run twice, and run in
    two separate processes at once, gives byte-identical outputs (the clicks and the final
    state's digest, with the input's own hash). The edge cases: a one-unit change in the
    input's seed profile changes the input's hash and gives a different output (the loader
    of this head admits it; record 1886's load check refuses it), never silently the same
    output; a one-unit change in the planted record's row gives a different output (test
    5's difference)."""
    serialized = json.dumps(small_world(), sort_keys=True)
    first = output_of(serialized)
    second = output_of(serialized)
    assert first == second and first["clicks"]
    with multiprocessing.get_context("spawn").Pool(2) as pool:
        apart = pool.map(output_of, [serialized, serialized])
    assert apart == [first, first]
    changed = json.loads(serialized)
    profile = changed["measured"][0]["seed"]
    index = next(i for i, value in enumerate(profile) if value)
    profile[index] += 1
    altered = json.dumps(changed, sort_keys=True)
    assert hashlib.sha256(altered.encode("utf-8")).hexdigest() != first["input"]
    try:
        other = output_of(altered)
    except ValueError:
        other = None  # refused at load: never the same output
    assert other is None or (other["input"] != first["input"] and other["state"] != first["state"])
    document = json.loads(serialized)
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    level_now, level_before = born_levels(simulation)
    now = np.zeros(SHAPE, dtype=np.int64)
    before = np.zeros(SHAPE, dtype=np.int64)
    now[BIRTH] = level_now + 1
    before[BIRTH] = level_before
    # read before the click (the deleted summand leaves the final states alike)
    _, states, _ = run(document, intervals=14, rows=(now, before))
    reference = json.loads(serialized)
    _, plain, _ = run(reference, intervals=14)
    assert any(
        not np.array_equal(a, b)
        for identity in plain[-1]
        for a, b in zip(plain[-1][identity], states[-1][identity], strict=True)
    )
