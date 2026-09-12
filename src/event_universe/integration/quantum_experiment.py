"""Run a declared finite coherent experiment using the existing quantum owner.

No rule branches on entity names. The schedule is fixed input, not selected from
remote amplitudes. Mode reservations supply fixed local waits and link arrivals;
all actual amplitudes and sampled records have exactly one quantum owner.
"""

import argparse
import json
import platform
import time
from dataclasses import asdict
from fractions import Fraction
from pathlib import Path

from event_universe.core.event_space import CausalEventSpace
from event_universe.initialization import parse_json_document
from event_universe.quantum import DeferredQuantum
from event_universe.retention import ArtifactLease, validate_output_path
from event_universe.runner import source_fingerprint

from .quantum_initialization import Action, QuantumInitialization, parse_quantum_initialization
from .quantum_observations import occupation_probability, rational, reduced_state, sector_distribution


class QuantumExperiment:
    """Local clock/controller adapter, with no duplicate physical payloads."""

    def __init__(self, initial: QuantumInitialization) -> None:
        self.initial = initial
        self.owner = DeferredQuantum()
        self.event_space = CausalEventSpace(
            shape=initial.network.shape,
            boundary=initial.network.boundary,
            link_ticks=initial.link_ticks,
        )
        self.network = self.owner.bind_event_network(initial.network, event_space=self.event_space)

    @property
    def tick(self) -> int:
        return self.network.tick

    def step(self) -> tuple[dict[str, object], ...]:
        if self.tick >= self.initial.ticks:
            raise ValueError("experiment duration exhausted")
        due = tuple((i, a) for i, a in enumerate(self.initial.actions) if a.end == self.tick + 1)
        operations = tuple((a.matrix, a.sites) for _, a in due if a.matrix is not None)
        observations = tuple(
            (i, a.sites[0], a.instrument, a.ticket) for i, a in due if a.instrument is not None
        )
        transfers = tuple((a.sites[0], a.destination) for _, a in due if a.destination is not None)
        self.network.advance(operations, observations, transfers)
        return tuple(
            {
                "event": action.kind,
                "tick": self.tick,
                "id": i,
                "start": action.start,
                "departure": action.departure,
                "arrival": action.end,
                "modes": [self.initial.modes[q].name for q in action.sites],
                "cost": action.cost,
                "port": action.port,
                "origins": action.origins,
                "destination": action.destination,
            }
            for i, action in due
        )

    def _ownership(self, site: int) -> tuple[str, Action | None]:
        for action in self.initial.actions:
            if site not in action.sites:
                continue
            if action.kind == "escape" and action.end <= self.tick:
                return "escaped", action
            if action.start <= self.tick < action.end:
                if action.kind in ("link", "escape") and action.departure <= self.tick:
                    return "in_flight", action
                return "waiting", action
        return "resident", None

    def snapshot(self) -> dict[str, object]:
        """Exact diagnostics including conditional escaped inventories.

        These values may depend on earlier observations. They are host reports,
        never remotely available registers or a routing/measurement trigger.
        """
        state = self.network.joint_state()
        modes = []
        escaped = [Fraction(0) for _ in self.initial.quantity_names]
        retained = [Fraction(0) for _ in self.initial.quantity_names]
        for site, mode in enumerate(self.initial.modes):
            status, action = self._ownership(site)
            probability = occupation_probability(state, site)
            totals = escaped if status == "escaped" else retained
            for i, value in enumerate(mode.quantities):
                totals[i] += value * probability
            modes.append(
                {
                    "name": mode.name,
                    "position": self.network.addresses[site],
                    "ownership": status,
                    "probability": rational(probability),
                    "arrival": None if action is None else action.end,
                }
            )
        return {
            "tick": self.tick,
            "modes": modes,
            "groups": {name: reduced_state(state, sites) for name, sites in self.initial.groups},
            "sectors": sector_distribution(state, tuple(m.quantities for m in self.initial.modes)),
            "retained": dict(zip(self.initial.quantity_names, map(rational, retained), strict=True)),
            "escaped": dict(zip(self.initial.quantity_names, map(rational, escaped), strict=True)),
            "records": [asdict(record) for record in self.network.records],
        }


def run_experiment(
    initialization: Path, output: Path, *, checkpoint_every: int = 0
) -> dict[str, object]:
    if type(checkpoint_every) is not int or checkpoint_every < 0:
        raise ValueError("checkpoint interval must be nonnegative")
    validate_output_path(output)
    if output.exists() and any(output.iterdir()):
        raise ValueError("use a new or empty output directory")
    if initialization.resolve().is_relative_to(output.resolve()):
        raise ValueError("original initialization must be outside the output directory")
    source = initialization.read_bytes()
    fingerprint = source_fingerprint()
    output.mkdir(parents=True, exist_ok=True)
    start = time.perf_counter_ns()
    with ArtifactLease(output.parent, [output.resolve()]):
        (output / "initialization.json").write_bytes(source)
        world = None
        try:
            initial = parse_quantum_initialization(parse_json_document(source))
            world = QuantumExperiment(initial)
            with (
                (output / "observations.jsonl").open("w", encoding="utf-8") as reports,
                (output / "events.jsonl").open("w", encoding="utf-8") as events,
            ):
                reports.write(json.dumps(world.snapshot()) + "\n")
                for _ in range(initial.ticks):
                    for event in world.step():
                        events.write(json.dumps(event) + "\n")
                    if checkpoint_every and world.tick % checkpoint_every == 0:
                        world.network.checkpoint(0)
                    reports.write(json.dumps(world.snapshot()) + "\n")
            if fingerprint != source_fingerprint():
                raise RuntimeError("simulation source changed during the run")
            result: dict[str, object] = {
                "status": "completed",
                "model": initial.model_id,
                "python": platform.python_version(),
                "source_sha256": fingerprint,
                "schema": "local-coherent-modes-v1",
                "ticks": world.tick,
                "link_ticks": initial.link_ticks,
                "shape": initial.network.shape,
                "boundary": initial.network.boundary,
                "configured_operation_cost": sum(a.cost for a in initial.actions),
                "successful_queries": world.network.successful_queries,
                "host_evaluated_nodes": world.network.host_evaluated_nodes,
                "host_elapsed_ns": time.perf_counter_ns() - start,
                "checkpoint_every": checkpoint_every,
                "visualization": False,
                "final": world.snapshot(),
            }
            (output / "result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
            return result
        except Exception as error:
            failure = {
                "status": "failed",
                "error": str(error),
                "python": platform.python_version(),
                "source_sha256": fingerprint,
                "last_committed_tick": None if world is None else world.tick,
            }
            (output / "failure.json").write_text(json.dumps(failure, indent=2), encoding="utf-8")
            raise
        finally:
            if world is not None:
                with (output / "causal-events.jsonl").open("w", encoding="utf-8") as causal_stream:
                    for entry in world.event_space.events:
                        causal_stream.write(json.dumps(asdict(entry)) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--init", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--checkpoint-every", type=int, default=0)
    args = parser.parse_args()
    result = run_experiment(args.init, args.output, checkpoint_every=args.checkpoint_every)
    print(json.dumps({k: v for k, v in result.items() if k != "final"}, indent=2))


if __name__ == "__main__":
    main()
