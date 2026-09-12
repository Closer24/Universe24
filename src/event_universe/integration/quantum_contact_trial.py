"""One opt-in local contact connects the real event engine to a quantum outcome.

The fixture has two unit-mass bodies and one contact at (6,2,1), tick 4.
A supplied instrument selects identity or momentum exchange, both defined by
initialization. This is a measured classical-control experiment, not coherent
quantum scattering or a generic per-cell quantum dispatcher.
"""

import argparse
import html
import json
import platform
from collections.abc import Callable
from dataclasses import asdict, replace
from pathlib import Path

from event_universe.core.disturbance_engine import DisturbanceEngine
from event_universe.core.disturbance_state import (
    DisturbanceRecord,
    InitialState,
    LocalPlan,
    bounded,
    pack,
    unpack,
)
from event_universe.fields.disturbances import DisturbanceLaw
from event_universe.initialization import parse_initial_json
from event_universe.quantum import (
    Amplitude,
    DeferredQuantum,
    EventNetworkConfig,
    LocalInstrument,
    LocalUnitary,
    NetworkRecord,
)
from event_universe.quantum.event_network import EventNetwork
from event_universe.retention import ArtifactLease, validate_output_path
from event_universe.runner import source_fingerprint

CONTACT = (6, 2, 1)


def quantum_rules() -> tuple[LocalUnitary, LocalUnitary, LocalInstrument]:
    """Explicit demonstration matrices; no physical law is inferred from them."""
    z, o, a, b, c, d = (Amplitude(n, 0) for n in (0, 1, 3, 4, -4, 5))
    split = LocalUnitary(((d, z, z, z), (z, a, c, z), (z, b, a, z), (z, z, z, d)))
    swap = LocalUnitary(((o, z, z, z), (z, z, o, z), (z, o, z, z), (z, z, z, o)))
    instrument = LocalInstrument((((o, z), (z, z)), ((z, z), (z, o))))
    return split, swap, instrument


class ContactPlanner:
    """Fixture-only controller; the ordinary generic law never imports quantum.

    Only the two co-resident records trigger the one local instrument. All
    mechanical alternatives are validated before committing a quantum record.
    The engine then owns the chosen mechanical proposal and causal transport.
    A later engine failure stops the run, retaining the already recorded quantum
    event; this is sequential event ordering, not cross-owner rollback.
    """

    def __init__(self, initial: InitialState, space: EventNetwork, ticket: int) -> None:
        self.law = DisturbanceLaw(
            initial.fields,
            initial.disturbances,
            initial.couplings,
            initial.operation_costs,
            initial.interactions,
        )
        self.space = space
        self.ticket = ticket
        self.record: NetworkRecord | None = None
        self.instrument = quantum_rules()[2]

    def __call__(
        self,
        records: tuple[DisturbanceRecord | None, ...],
        residuals: tuple[int, ...],
        received: int,
    ) -> LocalPlan:
        if len(records) != 2:
            raise ValueError("contact fixture requires exactly two local slots")
        if self.record is not None or any(r is None for r in records):
            return self.law(records, residuals, received)
        if {r.type_index for r in records if r is not None} != {0, 1}:
            raise ValueError("contact requires the two configured body roles")
        plans = []
        for code in (1, 2):
            local = tuple(
                None if r is None else replace(r, values=(*r.values[:2], pack((code,)))) for r in records
            )
            plan = self.law(local, residuals, received)
            plans.append(replace(plan, cost=bounded(plan.cost + 1)))
        decision = self.space.prepare(1, 0, self.instrument)
        tick = self.space.tick
        self.record = self.space.commit(decision, self.ticket)
        if self.space.tick != tick:
            raise ValueError("quantum decision advanced world time")
        return plans[self.record.outcome]


def validate_fixture(initial: InitialState) -> None:
    """The positional role mapping is scoped to this one experiment, not general JSON."""
    if (
        initial.shape != (13, 5, 3)
        or initial.slots_per_cell != 2
        or initial.link_ticks != 1
        or initial.normal_budget != 10000
        or initial.ticks != 8
        or initial.boundary != "open"
        or len(initial.fields) != 3
        or len(initial.disturbances) != 2
        or tuple(s.position for s in initial.seeds) != ((2, 2, 1), (10, 2, 1))
        or tuple(s.record.type_index for s in initial.seeds) != (0, 1)
        or initial.spatial_fields
        or initial.couplings
    ):
        raise ValueError("initialization is outside the single-contact fixture contract")
    expected = (((1,), (1, 0, 0), (0,)), ((1,), (-1, 0, 0), (0,)))
    if tuple(tuple(unpack(v) for v in s.record.values) for s in initial.seeds) != expected:
        raise ValueError("fixture requires two unit masses, opposite momenta and no prior decision")


def mechanics(world: DisturbanceEngine) -> dict[str, object]:
    """Read-only balances include records in flight exactly once."""
    records = [r for c in world.cells.values() for r in c.records if r is not None]
    records += [p.record for link in world.links.values() for p in link if p is not None]
    momentum = tuple(sum(unpack(r.values[1])[a] for r in records) for a in range(3))
    twice_energy = sum(sum(p * p for p in unpack(r.values[1])) for r in records)
    mass = sum(unpack(r.values[0])[0] for r in records)
    if len(records) != 2 or momentum != (0, 0, 0) or twice_energy != 2 or mass != 2:
        raise ValueError("unit-mass body balance failed; no repair is applied")
    return {
        "momentum": momentum,
        "twice_kinetic_energy": twice_energy,
        "mass": mass,
        "body_momenta": {
            world.initial.disturbances[r.type_index].name: unpack(r.values[1]) for r in records
        },
    }


def run_trial(
    initialization: Path,
    ticket: int,
    *,
    visualize: bool = False,
    event_sink: Callable[[dict[str, object]], None] | None = None,
) -> dict[str, object]:
    """Execute actual engine ticks; visualization never supplies physical inputs."""
    initial = parse_initial_json(initialization.read_bytes())
    validate_fixture(initial)
    if type(ticket) is not int or not 0 <= ticket < 25:
        raise ValueError("demonstration ticket must be an integer from 0 to 24")
    owner = DeferredQuantum()
    space = owner.bind_event_network(EventNetworkConfig((CONTACT, (6, 3, 1), (6, 4, 1)), (0,)))
    split, swap, _ = quantum_rules()
    planner = ContactPlanner(initial, space, ticket)
    events: list[dict[str, object]] = []

    def record(event: dict[str, object]) -> None:
        events.append(event)
        if event_sink is not None:
            event_sink(event)

    world = DisturbanceEngine(initial, planner, record)
    frames = [world.snapshot()] if visualize else []
    balances = [mechanics(world)]
    query_counts = [owner.query_stats.successful_queries]
    for _ in range(initial.ticks):
        if world.tick != space.tick:
            raise ValueError("physical and quantum recipe clocks disagree")
        previous = planner.record
        world.step()
        if previous is None and planner.record is not None:
            decision = planner.record.decision
            if decision.tick != 4:
                raise ValueError("fixture contact occurred at an unexpected tick")
            record(
                {
                    "event": "quantum_contact",
                    "tick": decision.tick,
                    "position": CONTACT,
                    "outcome": planner.record.outcome,
                    "weights": decision.weights,
                    "model_cost": 1,
                    "extra_world_ticks": 0,
                }
            )
        layer: tuple[tuple[LocalUnitary, tuple[int, ...]], ...] = ()
        if world.tick == 1:
            layer = ((split, (0, 1)),)
        elif world.tick == 5:
            layer = ((swap, (0, 1)),)
        elif world.tick == 6:
            layer = ((swap, (1, 2)),)
        space.step(layer)
        balances.append(mechanics(world))
        query_counts.append(owner.query_stats.successful_queries)
        if visualize:
            frames.append(world.snapshot())
    if planner.record is None:
        raise ValueError("no quantum contact occurred")
    contact_sends = [e for e in events if e["event"] == "sent" and e["tick"] == 4]
    if len(contact_sends) != 2 or any(e["position"] != CONTACT for e in contact_sends):
        raise ValueError("physical contact and quantum record disagree")
    return {
        "model": initial.model_id,
        "status": "completed",
        "shape": initial.shape,
        "boundary": initial.boundary,
        "link_ticks": initial.link_ticks,
        "python": platform.python_version(),
        "source_sha256": source_fingerprint(),
        "ticket": ticket,
        "outcome": planner.record.outcome,
        "branch": "reflection" if planner.record.outcome else "transmission",
        "contact_tick": 4,
        "contact_address": CONTACT,
        "weights_transmission_reflection": planner.record.decision.weights,
        "physical_tick": world.tick,
        "quantum_tick": space.tick,
        "extra_world_ticks": 0,
        "query_counts_after_each_tick": query_counts,
        "host_evaluated_nodes": owner.query_stats.host_evaluated_nodes,
        "final_quantum_state": space.joint_state(),
        "quantum_events": [asdict(e) for e in space.events],
        "balances": balances,
        "final_state": world.snapshot(),
        "frames": frames,
        "events": sorted(events, key=lambda e: int(str(e["tick"]))),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--init", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--ticket", type=int, default=24)
    parser.add_argument("--visualize", action="store_true")
    args = parser.parse_args()
    validate_output_path(args.output)
    if args.output.exists() and any(args.output.iterdir()):
        raise ValueError("use a new or empty output directory")
    if args.init.resolve().is_relative_to(args.output.resolve()):
        raise ValueError("original initialization must be outside the output directory")
    args.output.mkdir(parents=True, exist_ok=True)
    with ArtifactLease(args.output.parent, [args.output.resolve()]):
        (args.output / "initialization.json").write_bytes(args.init.read_bytes())
        try:
            with (args.output / "events.jsonl").open("w", encoding="utf-8") as stream:

                def record(event: dict[str, object]) -> None:
                    stream.write(json.dumps(event) + "\n")

                result = run_trial(args.init, args.ticket, visualize=args.visualize, event_sink=record)
        except Exception as error:
            (args.output / "failure.json").write_text(
                json.dumps({"status": "failed", "error": str(error)})
            )
            raise
        (args.output / "result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
        if args.visualize:
            from typing import cast

            from event_universe.diagnostics.disturbance_render import render_disturbances

            page = render_disturbances(
                cast(list[dict[str, object]], result["frames"]), args.output / "playback.html", result
            )
            note = (
                "<section><h2>Local event + quantum decision</h2>"
                f"<p>Contact: tick 4 at (6, 2, 1). Recorded branch: <b>{result['branch']}</b>. "
                "Born weights: transmission 16/25, reflection 9/25. One oracle call, zero extra ticks.</p>"
                "<p>At event tick 4 the outcome selects the engine's outgoing packets; "
                "the change is first visible in completed frame 5. XYZ world; both bodies lie in z=1.</p>"
                "<p>Body momentum (0,0,0), mass 2 and twice kinetic energy 2 at every tick. "
                "These are measured-control toy laws, not derived quantum scattering.</p>"
                "<details><summary>Quantum event trace and continuation</summary><pre>"
                + html.escape(
                    json.dumps(
                        {k: result[k] for k in ("quantum_events", "final_quantum_state")}, indent=2
                    )
                )
                + "</pre></details></section>"
            )
            page.write_text(
                page.read_text(encoding="utf-8").replace(
                    '<div class="stage">', note + '<div class="stage">', 1
                ),
                encoding="utf-8",
            )
        print(
            json.dumps(
                {
                    k: v
                    for k, v in result.items()
                    if k not in {"frames", "events", "quantum_events", "final_state"}
                },
                indent=2,
            )
        )


if __name__ == "__main__":
    main()
