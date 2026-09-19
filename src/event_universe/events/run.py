"""A run of the law of the ray: the artifacts the runner writes for it.

`execute_ray_run` steps a parsed world and preserves the input
(`initialization.json`), the events (`events.jsonl`: the measurements per
measured event, family and number with the push taken, the clicks with their
phase and content, the detectors' records per interval, the steps, the clicks
on the open faces), the final state (`state.json`, the measured events, the
detectors with the face detectors and every Node with rays, written Node by
Node through `snapshot_writer`) and the record (`run.json`: the law's marker
`rays-v1`, the world's keys, the books per completed tick with the
conservation flag, the per-tick lines of the measured content, the content in
transit and the momentum, the measured events' final states, the detectors'
measurements with their records and the face detectors', and the escapes).
`tools/run_series.py` reads the same keys of `run.json` as for any run
(`status`, `completed_ticks`, `elapsed_seconds`, `audit`,
`conserved_at_every_completed_tick`).
"""

from __future__ import annotations

import copy
import hashlib
import json
import time
from pathlib import Path

from event_universe import __version__
from event_universe.events.engine import RaySimulation
from event_universe.events.world import RAYS_LAW, RayWorld
from event_universe.snapshot_writer import write_snapshot


def execute_ray_run(
    world: RayWorld,
    source: bytes,
    output: Path,
    fingerprint: str,
    count: int,
    *,
    initialization_record: dict[str, object] | None = None,
) -> Path:
    """Run `count` intervals of the world into the empty directory `output`;
    returns the path of `run.json`. A failing interval is recorded and raised.
    Optional initialization provenance is copied for output only, never physics.
    """
    initialization_metadata = copy.deepcopy(initialization_record)
    (output / "initialization.json").write_bytes(source)
    audit: list[dict[str, object]] = []
    measured_content: list[list[int]] = []
    transit_content: list[list[int]] = []
    momentum: list[dict[str, object]] = []
    failure: Exception | None = None
    completed = 0
    started = time.perf_counter()
    with (output / "events.jsonl").open("w", encoding="utf-8") as stream:

        def record(event: dict[str, object]) -> None:
            stream.write(json.dumps(event) + "\n")

        simulation = RaySimulation(world, observer=record)
        try:
            for _ in range(count):
                simulation.step()
                books = simulation.books()
                audit.append(books)
                families = books["families"]
                assert isinstance(families, dict)
                measured_content.append(
                    [int(families[family.name]["measured"]["current"]) for family in world.families]
                )
                transit_content.append(
                    [int(families[family.name]["transit"]["current"]) for family in world.families]
                )
                momentum.append(dict(books["momentum"]))  # type: ignore[call-overload]
                if not books["balanced"]:
                    raise ValueError(f"{RAYS_LAW}: the books do not close at tick {simulation.tick}")
                completed += 1
        except Exception as error:  # noqa: BLE001 - recorded, then raised
            failure = error
        with (output / "state.json").open("w", encoding="utf-8") as state_stream:
            write_snapshot(simulation, state_stream)
            state_stream.write("\n")
    metadata: dict[str, object] = {
        "package_version": __version__,
        "source_sha256": fingerprint,
        "initialization_sha256": hashlib.sha256(source).hexdigest(),
        "law": RAYS_LAW,
        "model": world.model_id,
        "shape": list(world.shape),
        "boundary": world.boundary,
        "K": world.clock,
        "N": world.phase_steps,
        "release": list(world.release),
        "suspension": list(world.suspension),
        "directions": [list(vector) for vector in world.directions],
        "families": [
            {
                "name": family.name,
                "kind": family.kind,
                "charge": family.charge,
                "quantum": family.quantum,
                "phase": family.phase,
                "phase_per_link": family.phase_per_link,
            }
            for family in world.families
        ],
        "numbers": {
            str(index + 1): {
                "position": list(entry.position),
                "family": world.families[entry.family].name,
            }
            for index, entry in enumerate(world.measured)
        },
        "status": "failed" if failure else "completed",
        "error": str(failure) if failure else None,
        "requested_ticks": count,
        "completed_ticks": completed,
        "tick": simulation.tick,
        "elapsed_seconds": time.perf_counter() - started,
        "conserved_at_every_completed_tick": all(bool(entry["balanced"]) for entry in audit),
        "audit": audit,
        "measured_content": measured_content,
        "transit_content": transit_content,
        "momentum": momentum,
        "measured": simulation.contents(),
        "detectors": simulation.detectors(),
        "escaped": [
            {
                "family": family.name,
                "amount": simulation.ledger.escaped_units(index),
                "content": simulation.ledger.escaped_content(index),
                "momentum": simulation.ledger.escaped_momentum() if index == 0 else None,
            }
            for index, family in enumerate(world.families)
        ],
        "display": "none",
    }
    if initialization_metadata is not None:
        metadata["initialization_resolution"] = initialization_metadata
    path = output / "run.json"
    path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    if failure is not None:
        raise failure
    return path
