"""Data-only variant init files and full-state checkpoints.

A variant init file is the official init format plus the complete coupling
table and its fingerprint::

    {"format": "universe24-variant-init-v1",
     "side": 9, "background": [0, 0, 2], "steps": 12,
     "coupling": {"format": "universe24-variant-coupling-v1", "name": "...",
                  "construction": {...optional...}, "fingerprint": "<sha256>",
                  "ports": [[48 ints] x 6], "weights": [[48 ints] x 6]},
     "seed_changes": [{"position": [4, 4, 4], "channel": 0, "state": [0, 2, 2]}]}

The cube, background, steps and seed changes are parsed by the official
loader ``universe24.experiments.from_dict``. The coupling is rebuilt from its
tables, validated, and must reproduce the recorded fingerprint (and its
declared construction, if any). The reference loader rejects these files
("Unsupported keys"), so a variant can never be run as a reference experiment
by mistake.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from universe24.core.state import State
from universe24.experiments import from_dict as reference_from_dict

from .coupling import VariantCoupling
from .engine import VariantEngine

INIT_FORMAT = "universe24-variant-init-v1"
CHECKPOINT_FORMAT = "universe24-variant-checkpoint-v1"
_STATE_KEYS = ("side", "background", "steps", "seed_changes")


def _keys(data, allowed, required):
    if not isinstance(data, dict):
        raise TypeError("Expected JSON object")
    if set(data) - allowed:
        raise ValueError(f"Unsupported keys: {sorted(set(data) - allowed)}")
    if required - set(data):
        raise ValueError(f"Missing keys: {sorted(required - set(data))}")


@dataclass(frozen=True, slots=True)
class VariantExperiment:
    engine: VariantEngine
    initial: State
    steps: int

    def __post_init__(self):
        if not isinstance(self.engine, VariantEngine) or not isinstance(self.initial, State):
            raise TypeError("Expected VariantEngine and State")
        if type(self.steps) is not int or self.steps < 0:
            raise ValueError("steps must be nonnegative")

    @property
    def label(self) -> str:
        return self.engine.coupling.label


def init_data(coupling: VariantCoupling, state: State, steps: int = 0) -> dict[str, Any]:
    """The variant init dictionary (cells sorted, as in the official checkpoint)."""
    if not isinstance(coupling, VariantCoupling) or not isinstance(state, State):
        raise TypeError("Expected VariantCoupling and State")
    if type(steps) is not int or steps < 0:
        raise ValueError("steps must be nonnegative")
    return {"format": INIT_FORMAT, "side": state.cube.side, "background": list(state.background),
            "steps": steps, "coupling": coupling.to_json(),
            "seed_changes": [{"position": list(address[:3]), "channel": address[3], "state": list(value)}
                             for address, value in sorted(state.cells.items())]}


def from_dict(data: dict[str, Any]) -> VariantExperiment:
    _keys(data, {"format", *_STATE_KEYS, "coupling"}, {"format", "side", "coupling"})
    if data["format"] != INIT_FORMAT:
        raise ValueError("Bad variant init format")
    coupling = VariantCoupling.from_json(data["coupling"])
    reference = reference_from_dict({k: data[k] for k in _STATE_KEYS if k in data})
    return VariantExperiment(VariantEngine(coupling), reference.initial, reference.steps)


def load(path: str | Path) -> VariantExperiment:
    with Path(path).open(encoding="utf-8") as handle:
        return from_dict(json.load(handle))


def dumps(data: dict[str, Any]) -> str:
    """Compact, line-oriented JSON: one table row or seed change per line."""
    def line(value):
        return json.dumps(value, separators=(",", ":"))

    parts = []
    for key, value in data.items():
        if key == "coupling":
            inner = []
            for k, v in value.items():
                if k in ("ports", "weights"):
                    rows = ",\n".join("   " + line(row) for row in v)
                    inner.append(f'  {json.dumps(k)}: [\n{rows}\n  ]')
                else:
                    inner.append(f"  {json.dumps(k)}: {line(v)}")
            parts.append(f' {json.dumps(key)}: {{\n' + ",\n".join(inner) + "\n }")
        elif key == "seed_changes":
            rows = ",\n".join("  " + line(change) for change in value)
            parts.append(f' {json.dumps(key)}: [\n{rows}\n ]' if value else f' {json.dumps(key)}: []')
        else:
            parts.append(f" {json.dumps(key)}: {line(value)}")
    text = "{\n" + ",\n".join(parts) + "\n}\n"
    if json.loads(text) != json.loads(json.dumps(data)):
        raise AssertionError("compact writer changed the data")
    return text


def write_init(path: str | Path, coupling: VariantCoupling, state: State, steps: int = 0) -> Path:
    """Write a variant init file (never overwrites) and check that it reloads exactly."""
    path = Path(path)
    data = init_data(coupling, state, steps)
    text = dumps(data)
    reloaded = from_dict(json.loads(text))
    if (reloaded.initial != state or reloaded.steps != steps
            or reloaded.engine.coupling.fingerprint != coupling.fingerprint):
        raise AssertionError("init file does not reproduce the preparation")
    with path.open("x", encoding="utf-8") as handle:
        handle.write(text)
    return path


def checkpoint_data(state: State, engine: VariantEngine, completed_steps: int) -> dict[str, Any]:
    if type(completed_steps) is not int or completed_steps < 0:
        raise ValueError("Invalid steps")
    if not isinstance(engine, VariantEngine):
        raise TypeError("Expected VariantEngine")
    return {"format": CHECKPOINT_FORMAT, "completed_steps": completed_steps,
            "coupling_label": engine.coupling.label,
            "variant_fingerprint": engine.coupling.fingerprint,
            "experiment": init_data(engine.coupling, state, 0)}


def read_checkpoint(path: str | Path):
    with Path(path).open(encoding="utf-8") as handle:
        data = json.load(handle)
    _keys(data, {"format", "completed_steps", "coupling_label", "variant_fingerprint", "experiment"},
          {"format", "completed_steps", "coupling_label", "variant_fingerprint", "experiment"})
    if data["format"] != CHECKPOINT_FORMAT:
        raise ValueError("Bad variant checkpoint format")
    experiment = from_dict(data["experiment"])
    coupling = experiment.engine.coupling
    if data["variant_fingerprint"] != coupling.fingerprint or data["coupling_label"] != coupling.label:
        raise ValueError("Variant coupling fingerprint mismatch")
    n = data["completed_steps"]
    if type(n) is not int or n < 0:
        raise ValueError("Bad step index")
    return experiment.engine, experiment.initial, n
