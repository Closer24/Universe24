"""THE COUNT'S LINE, its own folder (ALGEBRA.md #the-counts-line): Rule3 for the family of clicks with the record's current as its read; a body at rest keeps its count in place; a moving record carries its count at the group velocity; the count conserved exactly; the inverse; the int64 bound; the refusals; the declaration, bound."""

import json
import math
from pathlib import Path

import numpy as np
import pytest

from event_universe.core.integer import MAX_WORK_INT
from event_universe.core.register import folder_of
from event_universe.core.rule3 import coefficients
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.features.counts_line import (
    DECLARATION,
    CountStart,
    CountTerm,
    Levels,
    apply,
    bound,
    current,
)
from event_universe.world_files import input_digest, load_world, parse_world_document, world_files

TOWARD = Path(__file__).resolve().parents[1] / "tests"  # the rule tests' own small worlds


def links_of(levels: Levels, periodic: bool | tuple[bool, bool, bool] = True) -> tuple[Levels, ...]:
    """The neighbour's levels across each Port as the send puts them on the Link: the wrap on a periodic axis, 0 beyond an open face, the Node itself on an axis of one layer."""
    wrap = (periodic,) * 3 if isinstance(periodic, bool) else periodic
    found = []
    for axis in range(3):
        for sigma in (1, -1):
            found.append(
                Levels(
                    *(
                        None if a is None else across(a, axis, sigma, wrap[axis])
                        for a in (levels.now, levels.before, levels.im_now, levels.im_before)
                    )
                )
            )
    return tuple(found)


def shipped_world(name: str) -> DetectorLawSimulation:
    document = json.loads((TOWARD / name).read_text(encoding="utf-8"))
    return DetectorLawSimulation(
        parse_world_document(document, world_files(document), input_digest(document))
    )


def levels_of(live) -> Levels:
    return Levels(live.now, live.before, live.im_now, live.im_before)


def centroid(weights: np.ndarray) -> float:
    """The centroid along x of a non-negative weight over the board, exact in Python integers."""
    x = np.arange(weights.shape[0]).reshape(-1, 1, 1)
    found = weights.astype(object)
    return int((x * found).sum()) / int(found.sum())


def across(a: np.ndarray, axis: int, sigma: int, periodic: bool) -> np.ndarray:
    if a.shape[axis] == 1:
        return a
    rolled = np.roll(a, -sigma, axis=axis)
    if not periodic:
        index = [slice(None)] * 3
        index[axis] = -1 if sigma > 0 else 0
        rolled[tuple(index)] = 0
    return rolled


def test_the_shipped_resting_body_keeps_its_count_under_the_loops_own_record():
    """lorentz_rest.json: the body's own standing record on its nine Nodes stepped by the loop for 200 intervals; nine quanta, one per Node, T the record's norm over nine; the count stays in place to the bit, none negative, the total conserved exactly, the accumulated swing far below T / 2."""
    simulation = shipped_world("lorentz_rest.json")
    block = simulation.blocks[0]
    weight = simulation.kind_wall(block.family, block.definition.pair)
    wrap = simulation.kind_wrap[block.family]
    count = block.mask.astype(np.int64)
    quanta = int(count.sum())
    norm = int(block.own.norm) // quanta
    term = CountTerm(norm, weight, simulation.world.amplitude_bound, quanta)
    remainder = np.full_like(count, norm // 2)
    origin = norm * count.astype(object) + remainder.astype(object)
    total = int(origin.sum())
    swing = 0
    for _ in range(200):
        simulation.step()
        here = levels_of(block.own)
        writes = apply(term, CountStart(count, remainder, here, links_of(here, wrap), 1))
        count, remainder = writes.count, writes.remainder
        found = norm * count.astype(object) + remainder.astype(object)
        assert int(found.sum()) == total and np.array_equal(count, block.mask.astype(np.int64))
        swing = max(swing, int(np.abs(found - origin).max()))
    assert 0 < swing < norm // 2


def test_the_hold_sources_the_well_where_the_lines_quanta_are_and_no_corner_follows():
    """A body has no law of motion of its own (ALGEBRA.md #the-primitives, #the-counts-line): the hold's sources are the count's line's quanta at their Nodes once laid (the well follows the record's current), the declared counts before; the corner and the mask never move."""
    world = load_world(
        TOWARD.parent / "examples" / "events" / "experiments" / "bell" / "bell_a_b.json"
    )  # bodies by their Nodes
    simulation = DetectorLawSimulation(world)
    block = next(b for b in simulation.blocks if b.own is not None and b.definition.counts)
    declared = sorted(simulation.node_sources(block.number, "content"))
    assert declared == sorted(zip(block.definition.nodes, block.definition.counts, strict=True))
    assert declared
    simulation.step()
    assert block.counts is not None
    assert sorted(simulation.node_sources(block.number, "content")) == declared
    corner, mask = list(block.corner), block.mask.copy()
    block.counts = np.roll(
        block.counts, 1, axis=0
    )  # the quanta one Link along x, as the line would move them
    moved = simulation.node_sources(block.number, "content")
    width = simulation.shape[0]
    assert sorted(moved) == sorted((((x + 1) % width, y, z), c) for (x, y, z), c in declared)
    simulation.step()
    assert list(block.corner) == corner and np.array_equal(block.mask, mask)
    assert not hasattr(simulation, "_follow_count")


def test_a_moving_record_on_the_shipped_moving_world_carries_its_count_at_the_group_velocity():
    """lorentz_moving.json's GameBoard, families and pair: a record of two levels with the phase k per Link along x (a packet of width 30 Links at x = 900, far from the world's bodies) stepped by the loop's own advance for 600 intervals; T the record's form over 9000 quanta, the count and its remainder at every Node laid from the Node's share of the form plus the origin's T / 2. The count is conserved exactly, none negative, and its centroid moves with the record's, which moves at Rule3's group velocity R 2 sin k / (2 w sin omega) at the vacuum's pair, each within one Node."""
    simulation = shipped_world("lorentz_moving.json")
    block = simulation.blocks[0]
    family, (num, den) = block.family, block.definition.kind
    weight = simulation.kind_wall(family, block.definition.pair)
    wrap = simulation.kind_wrap[family]
    reads, self_coefficient, wall = coefficients(num, den, simulation.world.node_clock, 0)
    k = 2 * math.pi / 8
    omega = math.acos((reads[0] * (2 * math.cos(k) + 4) + self_coefficient) / (2 * wall))
    group_velocity = reads[0] * 2 * math.sin(k) / (2 * wall * math.sin(omega))
    x = np.arange(simulation.shape[0]).reshape(-1, 1, 1)
    envelope = (1 << 16) * np.exp(-((x - 900) ** 2) / (2 * 30 * 30)) * np.ones(simulation.shape)
    now, before = (np.rint(envelope * np.cos(k * x - omega * t)).astype(np.int64) for t in (0, -1))
    im_now, im_before = (np.rint(envelope * np.sin(k * x - omega * t)).astype(np.int64) for t in (0, -1))
    live = simulation.planted_record(family, now, before, pair=(num, den))
    live.im_now, live.im_before = im_now, im_before
    live.im_remainder = np.zeros(simulation.shape, dtype=np.int64)
    live.standing = True
    numerator, denominator = simulation.conserved_form(live)
    quanta = 9000
    norm = numerator // denominator // quanta
    # the count and its remainder from the record's norm at the Node: T c + r is the Node's share of the conserved form plus the origin's T / 2 (the nine Nodes of a slab alike)
    laid = np.full(simulation.shape, norm // 2, dtype=np.int64)
    for slab in range(750, 1051):
        mask = np.zeros(simulation.shape, dtype=bool)
        mask[slab] = True
        share_numerator, share_denominator = simulation.form_share(live, mask)
        laid[slab] += share_numerator // (share_denominator * int(mask.sum()))
    count, remainder = np.floor_divide(laid, norm), np.remainder(laid, norm)
    term = CountTerm(norm, weight, simulation.world.amplitude_bound, quanta)
    total = int((norm * count.astype(object) + remainder.astype(object)).sum())
    count_start = centroid(count)
    record_start = centroid(now.astype(object) ** 2 + im_now.astype(object) ** 2)
    intervals = 600
    for _ in range(intervals):
        simulation._advance(live)
        here = levels_of(live)
        writes = apply(term, CountStart(count, remainder, here, links_of(here, wrap), 1))
        count, remainder = writes.count, writes.remainder
        assert int((norm * count.astype(object) + remainder.astype(object)).sum()) == total
        assert not np.any(count < 0)
    record_moved = (
        centroid(live.now.astype(object) ** 2 + live.im_now.astype(object) ** 2) - record_start
    )
    count_moved = centroid(count) - count_start
    assert abs(record_moved - group_velocity * intervals) < 1 and abs(count_moved - record_moved) < 1


def test_the_count_is_conserved_exactly_and_the_inverse_undoes_the_line():
    generator = np.random.default_rng(3)
    shape = (4, 3, 2)
    amplitude = 1 << 8
    norm, weight = 5000, 7
    term = CountTerm(norm, weight, amplitude, 1 << 21)  # each Node holds what it gives:
    count = generator.integers(1 << 20, 1 << 21, size=shape).astype(np.int64)
    remainder = generator.integers(0, norm, size=shape).astype(np.int64)
    for periodic in (True, False):
        for _ in range(50):
            bounds = (-amplitude, amplitude + 1)
            levels = [generator.integers(*bounds, size=shape).astype(np.int64) for _ in range(4)]
            here = Levels(*levels)
            links = links_of(here, periodic)
            forward = apply(term, CountStart(count, remainder, here, links, 1))
            total = norm * count + remainder
            assert int((norm * forward.count + forward.remainder).sum()) == int(total.sum())
            assert np.all(forward.remainder >= 0) and np.all(forward.remainder < norm)
            assert np.array_equal(sum(forward.net), (norm * forward.count + forward.remainder) - total)
            back = apply(term, CountStart(forward.count, forward.remainder, here, links, -1))
            assert np.array_equal(back.count, count) and np.array_equal(back.remainder, remainder)
            count, remainder = forward.count, forward.remainder


def test_the_current_is_the_booking_and_its_bound_holds_within_int64():
    here = Levels(np.array([3]), np.array([-2]), np.array([5]), np.array([1]))
    there = Levels(np.array([7]), np.array([4]), np.array([-1]), np.array([6]))
    assert int(current(3, here, there)[0]) == 3 * ((3 * 4 - (-2) * 7) + (5 * 6 - 1 * (-1)))
    assert int(current(3, there, here)[0]) == -int(current(3, here, there)[0])
    within = CountTerm(1 << 40, 1000, 1 << 20, 1 << 10)
    assert bound(within) <= MAX_WORK_INT
    beyond = CountTerm(1 << 40, 1000, 1 << 28, 1 << 10)
    assert bound(beyond) > MAX_WORK_INT
    level = np.zeros((1, 1, 1), dtype=np.int64)
    here = Levels(level, level, None, None)
    with pytest.raises(ValueError, match="beyond int64"):
        apply(beyond, CountStart(level, level, here, links_of(here), 1))
    with pytest.raises(ValueError, match="six Links"):
        apply(within, CountStart(level, level, here, links_of(here)[:5], 1))
    with pytest.raises(ValueError, match="direction"):
        apply(within, CountStart(level, level, here, links_of(here), 2))
    with pytest.raises(ValueError, match="from 1"):
        apply(CountTerm(0, 1, 1, 1), CountStart(level, level, here, links_of(here), 1))


def test_the_declaration_is_the_registers_row():
    assert DECLARATION.name == "the count's line" and folder_of(DECLARATION.name) == "counts_line"
    assert DECLARATION.place == "(ii)" and DECLARATION.word == "after the step"
    assert DECLARATION.function is apply and DECLARATION.built  # bound: the loop calls apply
    assert DECLARATION.writes == ("the count at a Node", "the count's remainder", "a body's position")


def test_a_node_at_0_gives_nothing_and_a_node_giving_more_than_it_holds_is_refused_by_name():
    """Two Nodes on a periodic axis of two, the record's levels (1, 0) now and (0, 1) before: the current into the first Node through each of its two x Ports is the weight, the second Node gives twice the weight. Holding exactly that it ends at 0 and the first holds it all; holding one less the line is refused by name with the quanta and the count where no arrivals are handed (the guard behind the block, never a clamp); with the Ports' arrivals handed a Node holding nothing or one less than it would give is starved, its Ports' currents are blocked at both ends and nothing moves."""
    weight, now = 7, np.array([[[1]], [[0]]], dtype=np.int64)
    here, term = Levels(now, 1 - now, None, None), CountTerm(1, weight, 1, 2 * weight)
    count = np.array([[[0]], [[2 * weight]]], dtype=np.int64)
    line = lambda p=None: apply(term, CountStart(count, count * 0, here, links_of(here), 1, p))  # noqa: E731
    assert line().count.ravel().tolist() == [2 * weight, 0]
    count[1] = 2 * weight - 1
    with pytest.raises(ValueError, match=f"a Node holding {count[1, 0, 0]} < {2 * weight}"):
        line()
    ports = lambda a: tuple(across(a, x, s, True) for x in range(3) for s in (1, -1))  # noqa: E731
    for holding in (0, 2 * weight - 1):
        count[1] = holding
        moved = line(ports)
        assert moved.count.ravel().tolist() == [0, holding] and not sum(moved.net).any()
