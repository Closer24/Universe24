"""Restricted free-stream closure and counterexamples measured with Simulation.

This is a bounded research readout, not a second general physics engine. The
independent macro transition is valid only for cardinal, constant-rate, free
transport with no later incoming stock and a proved receiving-capacity bound.
Its initialization removes transverse geometry only after admitting that law.
Interacting configurations are rejected.
All microscopic evolution, including the counterexample encounter, uses the
active Simulation and ordinary initialization-defined local operations.
"""

from collections import Counter
from dataclasses import dataclass, replace
from itertools import combinations_with_replacement, product

from event_universe import Simulation
from event_universe.core.disturbance_state import bounded
from event_universe.core.integer import checked_sum, checked_work, dot_product
from event_universe.initialization import parse_initial_state

from .configuration import additive_audit, base_configuration, field, operation, reference
from .properties import Contribution, PropertySpec, aggregate_properties

DIRECTIONS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
BLOCK_SIDES = (2, 4, 8)
SCHEMA = (PropertySpec("energy", "sum"), PropertySpec("momentum", "vector_sum", 3))
FREE_LAW = "cardinal-free-boundary-v1"


@dataclass(frozen=True, slots=True)
class Wave:
    """One initialization owner; direction is derived solely from momentum."""

    position: tuple[int, int, int]
    energy: int
    momentum: tuple[int, int, int]

    def __post_init__(self):
        if type(self.position) is not tuple or len(self.position) != 3:
            raise ValueError("position requires three immutable components")
        if type(self.momentum) is not tuple or len(self.momentum) != 3:
            raise ValueError("momentum requires three immutable components")
        for value in (*self.position, self.energy, *self.momentum):
            bounded(value)
        if min(self.position) < 0 or self.energy < 0:
            raise ValueError("position and energy must be nonnegative")
        cardinal_port(self.momentum)


def cardinal_port(momentum):
    nonzero = [axis for axis, value in enumerate(momentum) if value]
    if len(nonzero) != 1:
        raise ValueError("free closure admits nonzero cardinal momentum only")
    axis = nonzero[0]
    return 2 * axis + (momentum[axis] < 0)


def stream_configuration(side, waves, *, link_ticks=1):
    """Declare the exact free law admitted by the macro proof."""
    if type(side) is not int or side not in BLOCK_SIDES:
        raise ValueError("block requires 4, 16 or 64 Nodes")
    if type(link_ticks) is not int or not 1 <= link_ticks <= 8:
        raise ValueError("link ticks must be between one and eight")
    if type(waves) is not tuple or len(waves) > 2 * side * side:
        raise ValueError("wave tuple exceeds the fixed two-slot block capacity")
    shape = (side, side, 1)
    counts = Counter()
    for wave in waves:
        if type(wave) is not Wave or any(p >= n for p, n in zip(wave.position, shape, strict=True)):
            raise ValueError("wave must be a validated owner inside the block")
        counts[wave.position] += 1
        if counts[wave.position] > 2:
            raise ValueError("initial Node capacity exceeded")
    raw = base_configuration(FREE_LAW, side * link_ticks, shape, slots=2)
    raw["link_ticks"] = link_ticks
    raw["fields"] = [field("energy", conserved=True), field("momentum", 3, conserved=True)]
    raw["disturbance_types"] = [
        {
            "name": "free_carrier",
            "fields": ["energy", "momentum"],
            "transport": {"mode": "move", "direction_field": "momentum", "rate": 1},
        }
    ]
    raw["seeds"] = [
        {
            "position": list(wave.position),
            "type": "free_carrier",
            "values": {"energy": wave.energy, "momentum": list(wave.momentum)},
        }
        for wave in waves
    ]
    raw["conservation"] = additive_audit()
    return raw


@dataclass(frozen=True, slots=True, order=True)
class ExitBin:
    """Only future-relevant free-law state; no member list or microscopic map."""

    remaining_delay: int
    direction: int
    channel: int
    energy: int
    momentum: tuple[int, int, int]

    def __post_init__(self):
        for value in (self.remaining_delay, self.direction, self.channel, self.energy):
            checked_work(value)
        if not 0 <= self.remaining_delay <= 64 or not 0 <= self.direction < 6:
            raise ValueError("exit phase or direction exceeds the fixed free contract")
        if self.channel != 0 or self.energy < 0:
            raise ValueError("free closure requires the one declared carrier channel")
        if type(self.momentum) is not tuple or len(self.momentum) != 3:
            raise ValueError("momentum must have three immutable components")
        for value in self.momentum:
            checked_work(value)
        if cardinal_port(self.momentum) != self.direction:
            raise ValueError("free exit momentum must agree with its cardinal direction")


@dataclass(frozen=True, slots=True)
class FreeMacro:
    """Closed autonomous countdown, valid only after free-law admission."""

    bins: tuple[ExitBin, ...]

    def __post_init__(self):
        if type(self.bins) is not tuple or len(self.bins) > 128:
            raise ValueError("macro state exceeds the fixed block capacity")
        if any(type(item) is not ExitBin or item.remaining_delay < 1 for item in self.bins):
            raise ValueError("macro state retains only unreleased validated bins")

    def advance(self):
        """Advance without a Simulation, configuration, callback or micro owner."""
        pending, outgoing = [], []
        for item in self.bins:
            advanced = replace(item, remaining_delay=item.remaining_delay - 1)
            (outgoing if advanced.remaining_delay == 0 else pending).append(advanced)
        return FreeMacro(tuple(pending)), tuple(outgoing)

    def inventory(self):
        return (
            checked_sum(item.energy for item in self.bins),
            tuple(checked_sum(item.momentum[axis] for item in self.bins) for axis in range(3)),
        )


def compress_free(raw):
    """Read initial owners once and reject any law outside the proved family.

    Exact configuration equality intentionally makes admission conservative. This
    experiment is not a validator for arbitrary equivalent expressions or models.
    E/P are owned additive values; neither is reconstructed from an amplitude.
    """
    initial = parse_initial_state(raw)
    if any(set(seed.get("values", {})) != {"energy", "momentum"} for seed in raw["seeds"]):
        raise ValueError("free closure requires explicit energy and momentum on every seed")
    waves = tuple(
        Wave(tuple(seed["position"]), seed["values"]["energy"], tuple(seed["values"]["momentum"]))
        for seed in raw["seeds"]
    )
    side = initial.shape[0]
    expected = stream_configuration(side, waves, link_ticks=initial.link_ticks)
    if raw != expected:
        raise ValueError("macro closure requires the exact admitted free-stream configuration")
    ports = {cardinal_port(wave.momentum) for wave in waves}
    if len(waves) > 2 and len(ports) > 1:
        raise ValueError("free closure has no receiving-capacity proof for this mixed-direction block")
    # At most two global owners cannot exceed K=2. Alternatively one common
    # port translates every occupied Node injectively; its initial K persists.
    contributions = []
    for index, wave in enumerate(waves):
        port = cardinal_port(wave.momentum)
        axis = port // 2
        links = initial.shape[axis] - wave.position[axis] if port % 2 == 0 else wave.position[axis] + 1
        contributions.append(
            Contribution(
                (index,),
                FREE_LAW,
                0,
                port,
                links * initial.link_ticks,
                ((wave.energy,), wave.momentum),
            )
        )
    bins = aggregate_properties(SCHEMA, tuple(contributions), capacity=2 * side * side)
    # The admitted free law never reads identities or transverse coordinates.
    # Member diagnostics stay outside the evolving macro owner.
    return FreeMacro(
        tuple(
            sorted(
                ExitBin(
                    item.remaining_delay, item.direction, item.channel, item.values[0][0], item.values[1]
                )
                for item in bins
            )
        )
    )


def flux_signature(bins):
    totals = {}
    for item in bins:
        key = (item.direction, item.channel)
        old = totals.get(key, (0, (0, 0, 0)))
        totals[key] = (
            checked_work(old[0] + item.energy),
            tuple(checked_work(a + b) for a, b in zip(old[1], item.momentum, strict=True)),
        )
    return tuple(
        (direction, channel, energy, momentum)
        for (direction, channel), (energy, momentum) in sorted(totals.items())
    )


def escaped_flux(events):
    return flux_signature(
        tuple(
            ExitBin(0, event["port"], 0, event["values"]["energy"][0], event["values"]["momentum"])
            for event in events
            if event["event"] == "escaped"
        )
    )


def compare_free(side, waves, *, link_ticks=1):
    """Measure completed boundary links and still-owned stock at every tick."""
    raw = stream_configuration(side, waves, link_ticks=link_ticks)
    macro = compress_free(raw)
    initial_bins = len(macro.bins)
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    rows = []
    for tick in range(1, raw["ticks"] + 1):
        events.clear()
        world.step()
        macro, outgoing = macro.advance()
        measured = escaped_flux(events)
        predicted = flux_signature(outgoing)
        if measured != predicted:
            raise AssertionError(("boundary flux mismatch", tick, measured, predicted))
        totals = world.totals()
        if macro.inventory() != (totals["energy"][0], totals["momentum"]):
            raise AssertionError(("owned inventory mismatch", tick))
        if world.conservation_report()["status"] != "passed":
            raise AssertionError("microscopic local accounting failed")
        rows.append({"tick": tick, "flux": measured, "inventory": macro.inventory()})
    return {"nodes": side * side, "owners": len(waves), "initial_bins": initial_bins, "rows": rows}


def encounter_rule():
    """Configured local quarter-turn when a pair has zero summed momentum."""
    total = operation("add", reference("momentum"), reference("momentum", "right"))
    return {
        "name": "opposite_pair_turn",
        "left_requires": ["energy", "momentum"],
        "right_requires": ["energy", "momentum"],
        "when": operation("eq", operation("dot", total, total), 0),
        "assignments": [
            {
                "side": side,
                "field": "momentum",
                "expression": {
                    "op": "transform",
                    "args": [reference("momentum", side)],
                    "matrix": [[0, -1, 0], [1, 0, 0], [0, 0, 1]],
                },
            }
            for side in ("left", "right")
        ],
        "invariants": [
            {
                "name": "additive_energy",
                "expression": operation("add", reference("energy"), reference("energy", "right")),
            }
        ],
    }


def interaction_counterexample():
    """Equal free summaries hide collision versus separate transverse lanes."""
    summaries, traces = [], []
    for right_y in (1, 2):
        waves = (Wave((0, 1, 0), 1, (1, 0, 0)), Wave((2, right_y, 0), 1, (-1, 0, 0)))
        raw = stream_configuration(4, waves)
        summaries.append(compress_free(raw))
        raw["model_id"] = "opposite-pair-geometry-counterexample-v1"
        raw["interactions"] = [encounter_rule()]
        events = []
        world = Simulation(parse_initial_state(raw), observer=events.append)
        rows = []
        for tick in range(1, 5):
            events.clear()
            world.step()
            if world.conservation_report()["status"] != "passed":
                raise AssertionError("encounter accounting failed")
            rows.append({"tick": tick, "flux": escaped_flux(events)})
        traces.append(rows)
    if summaries[0] != summaries[1] or traces[0] == traces[1]:
        raise AssertionError("interaction counterexample did not separate equal summaries")
    return {"initial_summary": summaries[0], "collision": traces[0], "parallel": traces[1]}


def _projection(macro, candidate):
    groups = {}
    for item in macro.bins:
        key = (
            ()
            if candidate == "totals"
            else (
                (item.direction,) if candidate == "direction" else (item.remaining_delay, item.direction)
            )
        )
        old = groups.get(key, (0, (0, 0, 0)))
        groups[key] = (
            checked_work(old[0] + item.energy),
            tuple(checked_work(a + b) for a, b in zip(old[1], item.momentum, strict=True)),
        )
    return tuple(sorted(groups.items()))


def closure_search():
    """Exhaust the declared finite family, not all possible coarse theories.

    Domain: zero, one or two unit owners at the four Nodes of a 2x2x1 open
    block, each with one of six unit momenta, link time one and no interactions.
    At most two owners globally prevent any receiving-capacity failure. Three
    nested candidate summaries retain totals; direction; then direction/phase.
    A transition is closed only if its projected next state AND directional flux
    are single-valued. Micro runs supply measurements, never macro predictions.
    """
    launches = tuple(
        Wave((x, y, 0), 1, momentum) for x, y, momentum in product(range(2), range(2), DIRECTIONS)
    )
    cases = (
        ((),) + tuple((wave,) for wave in launches) + tuple(combinations_with_replacement(launches, 2))
    )
    candidates = ("totals", "direction", "direction_phase")
    maps = {name: {} for name in candidates}
    conflicts = {name: 0 for name in candidates}
    witnesses = {}
    checked = 0
    for waves in cases:
        raw = stream_configuration(2, waves)
        macro = compress_free(raw)
        events = []
        world = Simulation(parse_initial_state(raw), observer=events.append)
        for _ in range(2):
            before = macro
            macro, outgoing = macro.advance()
            events.clear()
            world.step()
            measured = escaped_flux(events)
            if measured != flux_signature(outgoing):
                raise AssertionError("finite family macro prediction failed")
            # link_ticks=1 leaves only resident owners at these clock boundaries.
            remaining = tuple(
                Wave(
                    position,
                    world.record_values(record)["energy"][0],
                    world.record_values(record)["momentum"],
                )
                for position, node in world.nodes.items()
                for record in node.records
                if record is not None
            )
            observed = compress_free(stream_configuration(2, remaining))
            if observed != macro:
                raise AssertionError("macro next state differs from independently observed micro")
            for name in candidates:
                current = _projection(before, name)
                result = (_projection(observed, name), measured)
                previous = maps[name].setdefault(current, result)
                if previous != result:
                    conflicts[name] += 1
                    witnesses.setdefault(name, {"state": current, "first": previous, "second": result})
            checked += 1
    closed = [name for name in candidates if not conflicts[name]]
    if closed != ["direction_phase"]:
        raise AssertionError(("unexpected finite closure result", conflicts))
    return {
        "domain_configurations": len(cases),
        "transitions": checked,
        "candidates": candidates,
        "conflicts": conflicts,
        "witnesses": witnesses,
        "smallest_in_declared_family": closed[0],
        "scope": "exhaustive finite free domain; no interacting closure claimed",
    }


def invariant_mass_squared(energy, momentum):
    """Read-only normalized c=1 system candidate, never a physical update."""
    checked_work(energy)
    if energy < 0 or type(momentum) is not tuple or len(momentum) != 3:
        raise ValueError("nonnegative energy and three immutable momentum components required")
    for value in momentum:
        checked_work(value)
    return checked_work(checked_work(energy * energy) - dot_product(momentum, momentum))
