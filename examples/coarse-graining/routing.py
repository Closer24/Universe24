"""Opt-in momentum routing using the existing balanced six-Port transport.

Momentum selects relative hop counts, not a Euclidean speed or a mass law.
Each hop uses one cardinal Link. Carried routing counters and movement credit
remain owned by the real disturbance. No diagnostic value feeds the simulator.
"""

from dataclasses import dataclass

from event_universe import Simulation
from event_universe.core.disturbance_state import Address3, DisturbanceRecord, PendingCycle
from event_universe.initialization import parse_initial_state

from .configuration import base_configuration, field

MAX_TRACE_TICKS = 4096


def build_configuration(
    momentum: tuple[int, int, int] = (5, -2, 0),
    *,
    ticks: int = 28,
    shape: Address3 = (129, 129, 3),
    link_ticks: int = 1,
    rate_denominator: int = 1,
    normal_budget: int = 1_000_000,
) -> dict[str, object]:
    """Select a candidate explicitly, with no heading separate from momentum.

    Energy is an independently owned additive quantity, not inferred from the
    route or momentum norm. Constant rate one over ``rate_denominator`` selects
    a hop rate; priced work can add the ordinary local computation delay.
    Canonical initialization validation owns all physical input bounds.
    """
    raw = base_configuration("momentum-balanced-routing-candidate-v1", ticks=ticks, shape=shape, slots=1)
    raw.update(link_ticks=link_ticks, normal_budget=normal_budget)
    raw["fields"] = [field("energy", conserved=True), field("momentum", 3, conserved=True)]
    raw["disturbance_types"] = [
        {
            "name": "carrier",
            "fields": ["energy", "momentum"],
            "defaults": {"energy": 10, "momentum": list(momentum)},
            "transport": {
                "mode": "move",
                "direction_field": "momentum",
                "routing": "balanced",
                "rate": 1,
                "rate_denominator": rate_denominator,
            },
        }
    ]
    raw["seeds"] = [{"position": [extent // 2 for extent in shape], "type": "carrier"}]
    return raw


@dataclass(frozen=True, slots=True)
class RouteEvent:
    event: str
    tick: int
    position: Address3
    port: int
    arrival_tick: int
    momentum: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class CarrierSample:
    """One actual owner, including original records during a frozen wait."""

    position: Address3
    target: Address3 | None
    arrival_tick: int | None
    record: DisturbanceRecord
    pending: PendingCycle | None


@dataclass(frozen=True, slots=True)
class RoutingTrace:
    """Finite host audit; retained memory grows with requested ticks and owners."""

    events: tuple[RouteEvent, ...]
    samples: tuple[tuple[CarrierSample, ...], ...]
    model_operations_cost: int
    local_cycles_started: int


def _sample(world: Simulation) -> tuple[CarrierSample, ...]:
    # Global enumeration is host-only evidence. It does not contribute modeled
    # local cost and must never become an input to routing or field reactions.
    residents = tuple(
        CarrierSample(position, None, None, record, node.pending)
        for position, node in world.nodes.items()
        for record in node.records
        if record is not None
    )
    traveling = tuple(
        CarrierSample(
            packet.origin,
            world.neighbor(packet.origin, packet.port),
            packet.arrival_tick,
            packet.record,
            None,
        )
        for links in world.links.values()
        for packet in links
        if packet is not None
    )
    return residents + traveling


def run_configuration(raw: dict[str, object] | None = None, ticks: int | None = None) -> RoutingTrace:
    """Run ordinary Simulation steps and retain a finite routing experiment.

    The capture limit bounds this helper's history horizon, not model time or
    physical capacity. Node/link enumeration and retained samples are host work.
    Engine errors propagate without repair or a fabricated completed trace.
    """
    initial = parse_initial_state(build_configuration() if raw is None else raw)
    count = initial.ticks if ticks is None else ticks
    if type(count) is not int or not 0 <= count <= MAX_TRACE_TICKS:
        raise ValueError(f"routing trace ticks must be from 0 through {MAX_TRACE_TICKS}")
    events = []

    def observe(event):
        if event["event"] in ("sent", "received"):
            events.append(
                RouteEvent(
                    event["event"],
                    event["tick"],
                    tuple(event["position"]),
                    event["port"],
                    event.get("arrival_tick", event["tick"]),
                    tuple(event["values"]["momentum"]),
                )
            )

    world = Simulation(initial, observer=observe)
    samples = [_sample(world)]
    for _ in range(count):
        world.step()
        samples.append(_sample(world))
    computation = world.computation_report()
    return RoutingTrace(
        tuple(events),
        tuple(samples),
        computation["model_operations_cost"],
        computation["local_cycles_started"],
    )
