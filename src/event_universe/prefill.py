"""The field given with the board (bit-law-v1, `initial_field`).

A thing does not emit its field: its shadows are given with the board and
circulate (the model owner's amendment of 2026-09-18). This host component
plans them before the first tick, in exact integers, with the dense region's
vectorized spread (`dense_field.DenseField`, the same integers as the spatial
law's `spread_content` at every Node), and installs them as the world's
initial content, booked on the ledger's initial line and never as a source.

`fill`: for T intervals every source, an external body of the family or a
record holding the family's stock, releases its shadow set (the whole quanta
of amount x n / d per Port heading by the family's `release`, with the
source's phase, charge sign and identity), every dense Node spreads what
arrived by the family's table, a shadow that arrives at a source is reversed
(it leaves again the way it came, as a shadow that comes home does), as is one
that arrives at a Detector mark (a mark returns it during a run): nothing is
dropped, the field is rounded to whole quanta per Node and heading and the
fractional parts are parked shadows at the Node (the model owner, 2026-09-18;
node-is-ports-v1); what walks off an open board is lost before the first tick
and not counted.
After T intervals the content that arrived at every Node is the field the
board starts with: the dense region's, when the world runs dense, or the
engine's resident and parked shadows otherwise, so that the two modes start
from the same state.

`rays`: a declared profile, each shadow placed at its Node as content that
arrived on its heading (steps 1 by default, 0 for a fresh shadow leaving at
the first tick); a shadow counts no distance from its owner (return-field-v1).
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import replace
from typing import TYPE_CHECKING

from event_universe.core.disturbance_state import Address3, InitialState, pack, unpack
from event_universe.core.spatial_state import (
    BIT_SHADOW,
    PORT_HEADINGS,
    Ray,
    Rays,
    body_release,
    merge_rays,
    release_stock,
    validate_rays,
)

if TYPE_CHECKING:
    from event_universe.core.disturbance_node import DisturbanceNode
    from event_universe.core.spatial_engine import SpatialEngine
    from event_universe.dense_field import DenseField

Placed = list[tuple[int, int, int, int, int]]


def _sources(
    initial: InitialState,
    index: int,
    carriers: Mapping[Address3, DisturbanceNode],
) -> list[tuple[Address3, Rays]]:
    """Every source of the family's shadows with the shadow set it releases per
    interval: the bodies of the family and the records holding its stock."""
    definition = initial.spatial_fields[index]
    found: list[tuple[Address3, Rays]] = []
    for body in initial.external_bodies:
        if body.family == index:
            rays = body_release(body, definition)
            if rays:
                found.append((body.position, rays))
    for position, carrier in sorted(carriers.items()):
        for record in carrier.records:
            if record is None or definition.field not in initial.disturbances[record.type_index].fields:
                continue
            stock = unpack(record.values[definition.field])[0]
            rays = release_stock(stock, definition, initial.disturbances[record.type_index].thing)
            if rays:
                found.append((position, rays))
    return found


def _fill(
    initial: InitialState,
    region: DenseField,
    index: int,
    intervals: int,
    carriers: Mapping[Address3, DisturbanceNode],
) -> dict[Address3, list[Ray]]:
    """T intervals of the split table's transient from every source, in the region;
    returns what arrived at the sources on the last interval, the shadows that
    leave them again at the first tick, fresh at their Nodes."""
    import numpy as np

    family = region.families[index]
    definition = family.definition
    sources = _sources(initial, index, carriers)
    source_positions = {position for position, _ in sources}
    # The releases as (rank, sign, port, amount, phase) per source, fixed.
    releases: dict[Address3, Placed] = {}
    for position, rays in sources:
        placed = releases.setdefault(position, [])
        for ray in rays:
            port = PORT_HEADINGS.index(definition.headings[ray.heading])
            placed.append((family.rank[ray.owner], ray.source_sign + 1, port, ray.amount, ray.phase))
    reflections: dict[Address3, Placed] = {}
    # The Nodes the region never holds: the engine's, and every source's; what
    # arrives at a source or a mark leaves again the way it came.
    engine_mask = region.owner == 1
    for position in source_positions:
        engine_mask[position] = True
    reflecting = source_positions | region.marks
    for interval in range(intervals):
        region.cycle(interval)
        for position, placed in releases.items():
            for rank, sign, port, amount, phase in placed:
                _depart(family, position, rank, sign, port, amount, phase, 0)
        for position, placed in reflections.items():
            for rank, sign, port, amount, phase in placed:
                _depart(family, position, rank, sign, port, amount, phase, 1)
        reflections = {}
        # A prefill's shares are outgoing (flow 0) and carry no momentum.
        amounts, phases, momenta = region._walk(family)
        hits = np.nonzero(engine_mask[..., None, None, None, None, None] & (amounts > 0))
        for x, y, z, rank, flow, sign, port, layer in zip(*hits, strict=True):
            position = (int(x), int(y), int(z))
            cell = (x, y, z, rank, flow, sign, port, layer)
            amount = int(amounts[cell])
            phase = int(phases[cell])
            amounts[cell] = 0
            phases[cell] = 0
            if position in reflecting:
                reflections.setdefault(position, []).append(
                    (int(rank), int(sign), int(port) ^ 1, amount, phase)
                )
        family.arr_amt += amounts
        family.arr_ph += phases
        family.arr_mom += momenta
        region.visited |= (family.arr_amt > 0).any(axis=(3, 4, 5, 6, 7))
    fresh: dict[Address3, list[Ray]] = {}
    for position, placed in reflections.items():
        for rank, sign, port, amount, phase in placed:
            fresh.setdefault(position, []).append(
                Ray(
                    definition.headings.index(PORT_HEADINGS[port]),
                    (0, 0, 0),
                    amount,
                    phase=phase,
                    detector=BIT_SHADOW,
                    source_sign=sign - 1,
                    owner=family.owners[rank],
                )
            )
    return fresh


def _depart(
    family: object,
    position: Address3,
    rank: int,
    sign: int,
    port: int,
    amount: int,
    phase: int,
    layer: int,
) -> None:
    """One departure of a source into the region's flight arrays, an outgoing share
    (flow 0), on the given layer, merged with what is there when the phases
    agree, on the other layer otherwise; a third phase on one Port of a source
    is merged by the coherence rule with the first layer's share (Highlights 5.4,
    points 24 and 25: the shares of one owner on one lane are one coherent sum,
    the amount summed and the phase the sum's), never refused (the cleanup of
    2026-09-18, on the A6 lane's finding: a fill longer than about 30 intervals
    at N = 64 refused a third phase)."""
    from event_universe.core.spatial_state import _phase_of_sum
    from event_universe.dense_field import LAYERS

    fly_amt = family.fly_amt  # type: ignore[attr-defined]
    fly_ph = family.fly_ph  # type: ignore[attr-defined]
    cell = (rank, 0, sign, port)
    slots = fly_amt[position][cell]
    for candidate in (layer, *range(LAYERS)):
        if slots[candidate] == 0:
            fly_amt[position][(*cell, candidate)] = amount
            fly_ph[position][(*cell, candidate)] = phase
            return
        if int(fly_ph[position][(*cell, candidate)]) == phase:
            fly_amt[position][(*cell, candidate)] = int(slots[candidate]) + amount
            return
    held_amount, held_phase = int(slots[layer]), int(fly_ph[position][(*cell, layer)])
    merged_phase = _phase_of_sum(
        ((held_amount, held_phase), (amount, phase)),
        tuple(int(v) for v in family.mix_cosines),  # type: ignore[attr-defined]
        tuple(int(v) for v in family.mix_sines),  # type: ignore[attr-defined]
        int(family.modulus),  # type: ignore[attr-defined]
    )
    fly_amt[position][(*cell, layer)] = held_amount + amount
    fly_ph[position][(*cell, layer)] = merged_phase


def owner_nodes(
    initial: InitialState, carriers: Mapping[Address3, DisturbanceNode]
) -> dict[int, list[Address3]]:
    """The Nodes of every thing on the board at the start: its body's, and the
    seeded records' of its type, sorted."""
    found: dict[int, set[Address3]] = {}
    for body in initial.external_bodies:
        found.setdefault(body.thing, set()).add(body.position)
    for position, carrier in carriers.items():
        for record in carrier.records:
            if record is not None:
                found.setdefault(initial.disturbances[record.type_index].thing, set()).add(position)
    return {owner: sorted(nodes) for owner, nodes in found.items()}


def _profile(
    initial: InitialState, index: int, carriers: Mapping[Address3, DisturbanceNode]
) -> dict[Address3, list[Ray]]:
    """The declared shadows of one family, per Node, as content that arrived, each
    with its declared steps (1, a Link walked, by default; a shadow counts no
    distance from its owner, return-field-v1)."""
    definition = initial.spatial_fields[index]
    entry = initial.initial_field[index]
    placed: dict[Address3, list[Ray]] = {}
    for shadow in entry.rays:
        steps = shadow.steps if shadow.steps >= 0 else 1
        placed.setdefault(shadow.position, []).append(
            Ray(
                definition.headings.index(shadow.heading),
                (0, 0, 0),
                shadow.amount,
                phase=shadow.phase,
                steps=steps,
                detector=BIT_SHADOW,
                source_sign=shadow.sign,
                polarization=shadow.polarization,
                owner=shadow.owner,
            )
        )
    return placed


def _install_node(engine: SpatialEngine, position: Address3, index: int, rays: Rays) -> None:
    """Resident shadows at an engine Node: those with a Link walked as arrivals of
    the previous interval, fresh ones (steps 0) as content leaving at the first
    tick, parked ones as they are (node-is-ports-v1)."""
    initial = engine.initial
    definition = initial.spatial_fields[index]
    node = engine._at(position)
    bundles = list(node.rays) or [() for _ in initial.spatial_fields]
    bundles[index] = merge_rays(tuple(bundles[index]) + tuple(rays))
    validate_rays(bundles[index], definition, initial.fields[definition.field])
    node.rays = tuple(bundles)
    delivered = [0] * 6
    for ray in bundles[index]:
        if ray.steps and not ray.parked:
            delivered[PORT_HEADINGS.index(definition.headings[ray.heading])] += ray.amount
    states = list(node.states)
    states[index] = replace(states[index], delivered=tuple(pack((amount,)) for amount in delivered))
    node.states = tuple(states)
    mask = list(node.arrival_mask) or [0] * 6
    for port, amount in enumerate(delivered):
        if amount:
            mask[port ^ 1] = 1
    node.arrival_mask = tuple(mask)
    node.received_count = sum(mask)
    if engine.dense is not None:
        # The Node holding the given shadows is the engine's until the region
        # takes it back at a delivery (dense-field-v1).
        engine.dense.claim(position)


def install_initial_field(
    initial: InitialState, engine: SpatialEngine, carriers: Mapping[Address3, DisturbanceNode]
) -> None:
    """Plan and install the field given with the board, before the first tick."""
    from event_universe.dense_field import DenseField

    fills = {index: entry.fill for index, entry in initial.initial_field.items() if entry.fill}
    if fills:
        region = engine.dense if engine.dense is not None else DenseField(initial, engine)
        assert isinstance(region, DenseField)
        fresh: list[tuple[int, Address3, list[Ray]]] = []
        for index, intervals in sorted(fills.items()):
            if index not in region.families:
                raise ValueError("an initial_field fill requires a spreading family (bit-law-v1)")
            for position, rays in sorted(_fill(initial, region, index, intervals, carriers).items()):
                fresh.append((index, position, rays))
        # What walked off the board during the fill is lost before the first tick.
        for values in (engine.escaped, engine.shadow_escaped):
            for line in values:
                for component in range(len(line)):
                    line[component] = 0
        if engine.dense is None:
            # A sparse run: the region's content, the parked shadows included,
            # becomes the engine's Nodes.
            for position, node in sorted(region.materialized_nodes({}).items()):
                for index in region.families:
                    if node.rays[index]:
                        _install_node(engine, position, index, node.rays[index])
        for index, position, rays in fresh:
            _install_node(engine, position, index, tuple(rays))
    for index, entry in sorted(initial.initial_field.items()):
        if not entry.rays:
            continue
        for position, rays in sorted(_profile(initial, index, carriers).items()):
            _install_node(engine, position, index, tuple(rays))
    engine.invalidate_totals()
