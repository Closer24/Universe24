"""Exact, data-only checkpoints of the canonical Simulation assembly.

This host IO boundary stores state, never executable callbacks or replay recipes.
A restore is private until configuration, source identity and all state validate.
"""

import hashlib
import json
import os
import platform
import sys
import time
from pathlib import Path
from typing import Any
from uuid import uuid4

from event_universe.checkpoint_codec import canonical, decode, encode
from event_universe.checkpoint_quantum import (
    capture_events,
    capture_quantum,
    restore_events,
    restore_quantum,
)
from event_universe.checkpoint_validation import (
    SPATIAL_FIELDS,
    WORLD_FIELDS,
    validate_balance,
    validate_world,
)
from event_universe.core.disturbance_engine import EventSink
from event_universe.core.disturbance_state import InitialState
from event_universe.disturbance_api import Simulation
from event_universe.initialization import parse_initial_json
from event_universe.retention import ArtifactLease, adopt_artifacts, validate_output_path

FORMAT = "event-universe-checkpoint"
VERSION = 1
MAX_BYTES = 64 * 1024 * 1024


def _source_identity() -> str:
    """Bind state to the exact installed runtime sources, including codec schema."""
    root = Path(__file__).resolve().parent
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*.py")):
        name, content = path.relative_to(root).as_posix().encode(), path.read_bytes()
        digest.update(len(name).to_bytes(8, "big"))
        digest.update(name)
        digest.update(len(content).to_bytes(8, "big"))
        digest.update(content)
    return digest.hexdigest()


def _runtime() -> dict[str, Any]:
    return {
        "source_sha256": _source_identity(),
        "python": list(sys.version_info[:3]),
        "implementation": platform.python_implementation(),
    }


def _components(world: Simulation) -> tuple[Any, ...]:
    spatial = world._spatial
    return (
        world._planner,
        world._record_policy,
        spatial,
        spatial.planner if spatial else None,
        spatial.coupler if spatial else None,
        spatial.decayer if spatial else None,
        spatial.port_waiter if spatial else None,
        world.event_space,
        world._resolver,
    )


def _canonical(world: Simulation, fresh: Simulation) -> None:
    if type(world) is not Simulation or set(vars(world)) != set(vars(fresh)):
        raise ValueError("checkpoint requires the canonical Simulation with no injected state")
    if any(
        current is not original
        for current, original in zip(_components(world), world._checkpoint_components, strict=True)
    ):
        raise ValueError("checkpoint cannot serialize replaced runtime components")
    for name in ("_planner", "_record_policy", "_coupled_types"):
        if getattr(world, name) != getattr(fresh, name):
            raise ValueError("checkpoint law composition differs from initialization")
    spatial, baseline = world._spatial, fresh._spatial
    if (spatial is None) != (baseline is None):
        raise ValueError("checkpoint spatial composition differs from initialization")
    if spatial is not None and baseline is not None:
        if type(spatial) is not type(baseline) or set(vars(spatial)) != set(vars(baseline)):
            raise ValueError("checkpoint spatial engine contains unknown mutable state")
        for name in (
            "initial",
            "port_count",
            "planner",
            "coupler",
            "decayer",
            "port_waiter",
            "_initial_totals",
        ):
            if getattr(spatial, name) != getattr(baseline, name):
                raise ValueError("checkpoint spatial law composition was changed")
        if spatial.observer != world._observer:
            raise ValueError("checkpoint spatial observer differs from the public observer")
    if world.event_space is not None and fresh.event_space is not None:
        for name in ("capacity", "shape", "boundary", "link_ticks"):
            if getattr(world.event_space, name) != getattr(fresh.event_space, name):
                raise ValueError("checkpoint event ledger configuration was changed")


def _initialization(world: Simulation, supplied: str | bytes | None) -> str:
    source = supplied if supplied is not None else world.initial.source_json
    if source is None:
        raise ValueError("checkpoint requires the original validated initialization JSON")
    parsed = parse_initial_json(source)
    if parsed != world.initial or parsed.source_json is None:
        raise ValueError("checkpoint initialization does not describe this world")
    return parsed.source_json


def _capture(world: Simulation, source: str) -> dict[str, Any]:
    fresh = Simulation(parse_initial_json(source))
    _canonical(world, fresh)
    validate_world(world)
    validate_balance(world, fresh)
    state = {
        "initial": world.initial,
        "world": {name: getattr(world, name) for name in WORLD_FIELDS},
        "spatial": (
            {name: getattr(world._spatial, name) for name in SPATIAL_FIELDS} if world._spatial else None
        ),
        "events": capture_events(world),
        "quantum": capture_quantum(world, fresh),
    }
    return {
        "format": FORMAT,
        "version": VERSION,
        "runtime": _runtime(),
        "initialization": source,
        "config_sha256": hashlib.sha256(source.encode()).hexdigest(),
        "state": encode(state),
    }


def _object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("checkpoint JSON contains a duplicate key")
        result[key] = value
    return result


def _reject_constant(value: str) -> None:
    raise ValueError(f"checkpoint JSON forbids numeric constant {value}")


def _read(path: Path) -> dict[str, Any]:
    with path.open("rb") as stream:
        data = stream.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError("checkpoint file exceeds byte capacity")
    try:
        result = json.loads(data, object_pairs_hook=_object, parse_constant=_reject_constant)
    except (UnicodeError, json.JSONDecodeError, RecursionError) as error:
        raise ValueError("invalid checkpoint JSON") from error
    if type(result) is not dict or set(result) != {"payload", "sha256"}:
        raise ValueError("checkpoint envelope is incomplete")
    body = result["payload"]
    if type(body) is not dict or set(body) != {
        "format",
        "version",
        "runtime",
        "initialization",
        "config_sha256",
        "state",
    }:
        raise ValueError("checkpoint payload schema is incompatible")
    if body["format"] != FORMAT or type(body["version"]) is not int or body["version"] != VERSION:
        raise ValueError("unsupported checkpoint format or version")
    if (
        type(result["sha256"]) is not str
        or hashlib.sha256(canonical(body)).hexdigest() != result["sha256"]
    ):
        raise ValueError("checkpoint checksum mismatch")
    return body


def _restore(body: dict[str, Any], observer: EventSink | None) -> Simulation:
    if body["runtime"] != _runtime():
        raise ValueError("checkpoint runtime source or Python identity differs")
    source = body["initialization"]
    if type(source) is not str or hashlib.sha256(source.encode()).hexdigest() != body["config_sha256"]:
        raise ValueError("checkpoint configuration identity mismatch")
    initial = parse_initial_json(source)
    state = decode(body["state"])
    if type(state) is not dict or set(state) != {"initial", "world", "spatial", "events", "quantum"}:
        raise ValueError("checkpoint state sections are incomplete")
    if type(state["initial"]) is not InitialState or state["initial"] != initial:
        raise ValueError("checkpoint typed initialization disagrees with validated source")
    world = Simulation(initial)
    data = state["world"]
    if type(data) is not dict or set(data) != set(WORLD_FIELDS):
        raise ValueError("checkpoint physical state fields are incomplete")
    for name in WORLD_FIELDS:
        setattr(world, name, data[name])
    spatial = state["spatial"]
    if world._spatial is None:
        if spatial is not None:
            raise ValueError("checkpoint includes unconfigured spatial fields")
    else:
        if type(spatial) is not dict or set(spatial) != set(SPATIAL_FIELDS):
            raise ValueError("checkpoint spatial state fields are incomplete")
        if spatial["_initial_totals"] != world._spatial._initial_totals:
            raise ValueError("checkpoint original spatial totals disagree with configuration")
        for name in SPATIAL_FIELDS:
            setattr(world._spatial, name, spatial[name])
    restore_events(world, state["events"])
    restore_quantum(world, state["quantum"])
    validate_world(world)
    validate_balance(world, Simulation(initial))
    world._observer = observer
    if world._spatial is not None:
        world._spatial.observer = observer
    return world


def load_checkpoint(path: Path, *, observer: EventSink | None = None) -> Simulation:
    """Restore privately and return only a completely validated canonical world."""
    try:
        return _restore(_read(Path(path)), observer)
    except (TypeError, KeyError, IndexError, AttributeError, OverflowError, RecursionError) as error:
        raise ValueError("checkpoint contains corrupt or incompatible state") from error


def _leased_directory(lease: ArtifactLease, path: Path) -> None:
    if type(lease) is not ArtifactLease or lease._closed or not lease._lock.held:
        raise ValueError("checkpoint requires a live artifact directory lease")
    entry = json.loads(lease.path.read_text(encoding="utf-8"))
    for item in entry["targets"]:
        directory = lease.root / item["path"]
        if item["directory"] and path.is_relative_to(directory):
            info = directory.stat()
            if (info.st_dev, info.st_ino) == (item["device"], item["inode"]):
                return
    raise ValueError("checkpoint target is outside the supplied artifact directory lease")


def _write_atomic(path: Path, data: bytes, lease: ArtifactLease | None) -> None:
    validate_output_path(path)
    path = path.resolve()
    if lease is not None:
        _leased_directory(lease, path)
    if path.exists():
        # Never overwrite an unrelated JSON document or original initialization.
        _read(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{uuid4().hex}.tmp")
    temporary.touch(exist_ok=False)
    try:
        owned = ArtifactLease(path.parent, [temporary]) if lease is None else None
        try:
            with temporary.open("wb") as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, path)
            if lease is None:
                adopt_artifacts(path.parent, [path], time.time())
        finally:
            if owned is not None:
                owned.finish()
    finally:
        temporary.unlink(missing_ok=True)


def save_checkpoint(
    world: Simulation,
    path: Path,
    *,
    initialization: str | bytes | None = None,
    lease: ArtifactLease | None = None,
) -> Path:
    """Atomically save complete state at a completed step boundary, under retention.

    Pass the runner's active directory lease for checkpoints inside its output.
    Other destinations are enrolled independently with the standard expiry.
    """
    if type(world) is not Simulation:
        raise ValueError("checkpoint requires the canonical Simulation class")
    source = _initialization(world, initialization)
    body = _capture(world, source)
    # Validate the exact codec round trip before any filesystem mutation.
    _restore(body, None)
    data = canonical({"payload": body, "sha256": hashlib.sha256(canonical(body)).hexdigest()})
    if len(data) > MAX_BYTES:
        raise ValueError("checkpoint file exceeds byte capacity")
    target = Path(path)
    _write_atomic(target, data, lease)
    return target.resolve()
