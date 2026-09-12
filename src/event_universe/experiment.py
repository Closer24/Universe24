"""Assemble bounded local experiment packages into the canonical runtime input.

This is host-side JSON composition. It adds neither runtime imports nor laws.
"""

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import cast

from event_universe.core.disturbance_state import InitialState
from event_universe.initialization import parse_initial_json, parse_json_document

MAX_EXPERIMENT_FILES = 64
MAX_EXPERIMENT_DEPTH = 16
MAX_EXPERIMENT_BYTES = 16 * 1024 * 1024

PART_KEYS = {
    "environment": {
        "shape",
        "boundary",
        "topology",
        "slots_per_cell",
        "link_ticks",
        "normal_budget",
        "operation_costs",
        "unit_system",
        "directional_delay",
    },
    "definitions": {
        "fields",
        "disturbance_types",
        "couplings",
        "interactions",
        "spatial_fields",
        "emissions",
        "spatial_couplings",
        "field_groups",
        "field_rules",
        "spatial_interactions",
        "event_program",
    },
    "initial_conditions": {"seeds", "spatial_seeds"},
    "run": {"ticks", "visualize", "frame_stride"},
}
_NAMED = {
    "fields": ("name",),
    "disturbance_types": ("name",),
    "couplings": ("name",),
    "interactions": ("name",),
    "spatial_fields": ("field",),
    "emissions": ("type", "field"),
    "spatial_couplings": ("name",),
    "field_groups": ("name",),
    "field_rules": ("name",),
    "spatial_interactions": ("name",),
}
_REUSABLE = {"fields", "disturbance_types"}


def _json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _object(value: object, label: str, allowed: set[str], required: set[str]) -> dict[str, object]:
    if not isinstance(value, dict) or any(not isinstance(key, str) for key in value):
        raise ValueError(f"{label} must be an object")
    result = cast(dict[str, object], value)
    if result.keys() - allowed:
        raise ValueError(f"{label} has unknown keys: {', '.join(sorted(result.keys() - allowed))}")
    if required - result.keys():
        raise ValueError(f"{label} is missing keys: {', '.join(sorted(required - result.keys()))}")
    return result


def _version(value: object, label: str, accepted: tuple[int, ...] = (1,)) -> None:
    if type(value) is not int or value not in accepted:
        raise ValueError(f"unsupported {label}; expected {accepted}")


def _paths(value: object, label: str, minimum: int = 0) -> list[str]:
    if not isinstance(value, list) or not minimum <= len(value) <= MAX_EXPERIMENT_FILES:
        raise ValueError(f"{label} must contain {minimum} through {MAX_EXPERIMENT_FILES} paths")
    if any(not isinstance(item, str) for item in value):
        raise ValueError(f"{label} must contain relative JSON paths")
    paths = cast(list[str], value)
    if len(set(paths)) != len(paths):
        raise ValueError(f"{label} contains duplicate paths")
    return paths


@dataclass(frozen=True, slots=True)
class ExperimentSource:
    """Exact source bytes captured once, under a package-relative portable path."""

    path: str
    content: bytes
    sha256: str


@dataclass(frozen=True, slots=True)
class ExperimentPackage:
    """Frozen run input and source evidence; mapping properties return fresh data."""

    runtime_json: bytes
    initial: InitialState
    sources: tuple[ExperimentSource, ...]
    run_json: bytes
    provenance_json: bytes

    @property
    def run_controls(self) -> dict[str, object]:
        return cast(dict[str, object], json.loads(self.run_json))

    @property
    def provenance(self) -> dict[str, object]:
        return cast(dict[str, object], json.loads(self.provenance_json))


class _PackageReader:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.sources: dict[Path, ExperimentSource] = {}
        self.documents: dict[Path, object] = {}
        self.total_bytes = 0
        self.visited: set[Path] = set()
        self.active: set[Path] = set()

    def reference(self, value: object, parent: Path) -> Path:
        if not isinstance(value, str) or not value or len(value) > 1024:
            raise ValueError("experiment reference must be a relative JSON path")
        portable = PurePosixPath(value)
        if (
            "\\" in value
            or ":" in value
            or "\x00" in value
            or portable.is_absolute()
            or any(part in (".", "..", "") for part in value.split("/"))
            or portable.suffix != ".json"
        ):
            raise ValueError(
                "experiment references require local relative .json paths without traversal"
            )
        lexical = parent / Path(*portable.parts)
        candidate = lexical.resolve()
        if not candidate.is_relative_to(self.root):
            raise ValueError("experiment reference escapes the package directory")
        component = self.root
        for segment in lexical.relative_to(self.root).parts:
            component = component / segment
            if component.is_symlink() or component.is_junction():
                raise ValueError("experiment references must not use symbolic links or junctions")
        return candidate

    def read(self, path: Path) -> object:
        if path in self.documents:
            return self.documents[path]
        if len(self.sources) >= MAX_EXPERIMENT_FILES:
            raise ValueError("experiment exceeds the file limit")
        with path.open("rb") as stream:
            content = stream.read(MAX_EXPERIMENT_BYTES - self.total_bytes + 1)
        self.total_bytes += len(content)
        if self.total_bytes > MAX_EXPERIMENT_BYTES:
            raise ValueError("experiment exceeds the source byte limit")
        document = parse_json_document(content)
        self.sources[path] = ExperimentSource(
            path.relative_to(self.root).as_posix(), content, hashlib.sha256(content).hexdigest()
        )
        self.documents[path] = document
        return document

    def part(self, path: Path, kind: str, result: dict[str, object], depth: int = 1) -> None:
        if depth > MAX_EXPERIMENT_DEPTH:
            raise ValueError("experiment includes exceed the depth limit")
        if path in self.active:
            raise ValueError("experiment include cycle")
        raw = _object(
            self.read(path),
            "experiment part",
            {"part_version", "part_kind", "includes", "data"},
            {"part_version", "part_kind", "data"},
        )
        _version(raw["part_version"], "part_version")
        if raw["part_kind"] != kind:
            raise ValueError(f"experiment requires a {kind} part")
        if path in self.visited:
            return
        data = _object(raw["data"], f"{kind} data", PART_KEYS[kind], set())
        self.active.add(path)
        for reference in _paths(raw.get("includes", []), "includes"):
            self.part(self.reference(reference, path.parent), kind, result, depth + 1)
        self.active.remove(path)
        self._merge(result, data)
        self.visited.add(path)

    @staticmethod
    def _merge(result: dict[str, object], data: dict[str, object]) -> None:
        for key, value in data.items():
            if key in _NAMED:
                if not isinstance(value, list):
                    raise ValueError(f"{key} must be an array")
                rows = cast(list[object], result.setdefault(key, []))
                identities: dict[tuple[str, ...], object] = {}
                local: set[tuple[str, ...]] = set()
                for index, row in enumerate([*rows, *value]):
                    if not isinstance(row, dict):
                        raise ValueError(f"{key} declarations must be objects")
                    identity = tuple(row.get(name) for name in _NAMED[key])
                    if any(not isinstance(name, str) or not name.strip() for name in identity):
                        raise ValueError(f"{key} declaration requires a nonempty identity")
                    identity = cast(tuple[str, ...], identity)
                    if index >= len(rows):
                        if identity in local:
                            raise ValueError(f"duplicate {key} declaration within a part: {identity}")
                        local.add(identity)
                    if identity in identities:
                        if key not in _REUSABLE or _json_bytes(identities[identity]) != _json_bytes(row):
                            raise ValueError(f"conflicting or duplicate {key} declaration: {identity}")
                    else:
                        identities[identity] = row
                result[key] = list(identities.values())
            elif key in ("seeds", "spatial_seeds"):
                if not isinstance(value, list):
                    raise ValueError(f"{key} must be an array")
                old = cast(list[object], result.setdefault(key, []))
                result[key] = [*old, *value]
            elif key in result and _json_bytes(result[key]) != _json_bytes(value):
                raise ValueError(f"conflicting experiment member: {key}")
            else:
                result[key] = value


def load_experiment(path: Path) -> ExperimentPackage:
    """Load one local package, preserving exact sources and the validated merged input."""
    manifest_path = path.resolve()
    reader = _PackageReader(manifest_path.parent)
    keys = {
        "experiment_version",
        "schema_version",
        "model_id",
        "environment",
        "definitions",
        "initial_conditions",
        "run",
    }
    manifest = _object(reader.read(manifest_path), "experiment manifest", keys, keys)
    _version(manifest["experiment_version"], "experiment_version")
    _version(manifest["schema_version"], "schema_version", (1, 2))
    runtime = {key: manifest[key] for key in ("schema_version", "model_id")}
    controls: dict[str, object] = {}
    for kind in PART_KEYS:
        references = (
            _paths(manifest[kind], "definitions", 1) if kind == "definitions" else [manifest[kind]]
        )
        target = controls if kind == "run" else runtime
        for reference in references:
            reader.part(reader.reference(reference, manifest_path.parent), kind, target)
    if "ticks" not in controls:
        raise ValueError("experiment run data requires ticks")
    runtime["ticks"] = controls["ticks"]
    if "visualize" in controls and type(controls["visualize"]) is not bool:
        raise ValueError("run visualize must be a boolean")
    stride = controls.get("frame_stride", 1)
    if type(stride) is not int or not 1 <= stride <= 2**31 - 1:
        raise ValueError("run frame_stride must be a positive bounded integer")
    controls.setdefault("visualize", False)
    controls.setdefault("frame_stride", 1)
    runtime_json = _json_bytes(runtime)
    initial = parse_initial_json(runtime_json)
    sources = tuple(reader.sources.values())
    provenance = {
        "experiment_version": 1,
        "manifest": manifest_path.name,
        "sources": [{"path": source.path, "sha256": source.sha256} for source in sources],
        "runtime_sha256": hashlib.sha256(runtime_json).hexdigest(),
        "run_controls_sha256": hashlib.sha256(_json_bytes(controls)).hexdigest(),
    }
    return ExperimentPackage(
        runtime_json, initial, sources, _json_bytes(controls), _json_bytes(provenance)
    )
