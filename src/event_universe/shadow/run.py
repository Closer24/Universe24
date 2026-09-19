"""A run of the law of the shadow: the artifacts the runner writes for it.

`execute_shadow_run` steps a parsed world and preserves, as the old engine's
runner does, the input (`initialization.json`), the events (`events.jsonl`:
the absorptions per held content, family and number with the momentum carried
and the push taken, the steps, the merges, the escapes), the final state
(`state.json`, the held contents and every Node with content, written Node by
Node through `snapshot_writer`) and the record (`run.json`: the law's marker,
the world's keys, the books per completed tick with the conservation flag,
the per-tick lines of the held content, the shadows and the momentum, the
held contents' final states and the escapes). `tools/run_series.py` reads the
same keys of `run.json` as for any run (`status`, `completed_ticks`,
`elapsed_seconds`, `audit`, `conserved_at_every_completed_tick`).
"""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

from event_universe import __version__
from event_universe.shadow.engine import ShadowSimulation
from event_universe.shadow.world import SHADOW_LAW, ShadowWorld
from event_universe.snapshot_writer import write_snapshot


def execute_shadow_run(
    world: ShadowWorld, source: bytes, output: Path, fingerprint: str, count: int
) -> Path:
    """Run `count` intervals of the world into the empty directory `output`;
    returns the path of `run.json`. A failing interval is recorded and raised."""
    (output / "initialization.json").write_bytes(source)
    audit: list[dict[str, object]] = []
    held_content: list[list[int]] = []
    shadow_content: list[list[int]] = []
    momentum: list[dict[str, object]] = []
    failure: Exception | None = None
    completed = 0
    started = time.perf_counter()
    with (output / "events.jsonl").open("w", encoding="utf-8") as stream:

        def record(event: dict[str, object]) -> None:
            stream.write(json.dumps(event) + "\n")

        simulation = ShadowSimulation(world, observer=record)
        try:
            for _ in range(count):
                simulation.step()
                books = simulation.books()
                audit.append(books)
                families = books["families"]
                assert isinstance(families, dict)
                held_content.append(
                    [int(families[family.name]["held"]["current"]) for family in world.families]
                )
                shadow_content.append(
                    [int(families[family.name]["shadows"]["current"]) for family in world.families]
                )
                momentum.append(dict(books["momentum"]))  # type: ignore[call-overload]
                if not books["balanced"]:
                    raise ValueError(f"{SHADOW_LAW}: the books do not close at tick {simulation.tick}")
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
        "law": SHADOW_LAW,
        "model": world.model_id,
        "shape": list(world.shape),
        "boundary": "open",
        "K": world.clock,
        "N": world.phase_steps,
        "release": list(world.release),
        "wait_per_quantum": list(world.wait),
        "families": [
            {
                "name": family.name,
                "kind": family.kind,
                "charge": family.charge,
                "turns_in_flight": family.turns,
                "quantum": family.quantum,
            }
            for family in world.families
        ],
        "numbers": {
            str(index + 1): {
                "position": list(content.position),
                "family": world.families[content.family].name,
            }
            for index, content in enumerate(world.contents)
        },
        "status": "failed" if failure else "completed",
        "error": str(failure) if failure else None,
        "requested_ticks": count,
        "completed_ticks": completed,
        "tick": simulation.tick,
        "elapsed_seconds": time.perf_counter() - started,
        "conserved_at_every_completed_tick": all(bool(entry["balanced"]) for entry in audit),
        "audit": audit,
        "held_content": held_content,
        "shadow_content": shadow_content,
        "momentum": momentum,
        "contents": simulation.contents(),
        "escaped": [
            {
                "family": family.name,
                "amount": layer.escaped,
                "momentum": [int(v) for v in layer.escaped_momentum],
            }
            for family, layer in zip(world.families, simulation.layers, strict=True)
        ],
        "display": "none",
    }
    path = output / "run.json"
    path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    if failure is not None:
        raise failure
    return path
