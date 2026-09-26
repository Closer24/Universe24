"""The readings of a run, declared in the world file under `readings` and written in one format, each labelled DETECTOR (a declared detector's clicks), GAMEBOARD (a family's level, support or total, a body's centre) or HOST (the records alive); a reading reads state at the declared intervals and writes nothing into the run (ALGEBRA.md 9.115; docs/ENGINE.md, the readings by type)."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

# kind -> (label, the keys the kind takes beside name and kind)
SCHEMA: Mapping[str, tuple[str, tuple[str, ...]]] = {
    "clicks": ("DETECTOR", ("detector",)),
    "level": ("GAMEBOARD", ("family", "node", "every")),
    "support": ("GAMEBOARD", ("family", "every")),
    "total": ("GAMEBOARD", ("family", "every")),
    "centre": ("GAMEBOARD", ("body", "every")),
    "alive": ("HOST", ("every",)),
}
LABELS: tuple[str, ...] = ("DETECTOR", "GAMEBOARD", "HOST")


@dataclass(frozen=True)
class Reading:
    """One declared reading: its name, kind and label, its target (a detector, a family and a Node, a body) and its stride."""

    name: str
    kind: str
    label: str
    every: int | None = None
    detector: str | None = None
    family: str | None = None
    body: int | None = None
    node: tuple[int, int, int] | None = None

    def target(self) -> dict[str, Any]:
        """The declared target keys, echoed into the output beside the lines."""
        found: dict[str, Any] = {}
        for key in SCHEMA[self.kind][1]:
            value = getattr(self, key)
            found[key] = list(value) if key == "node" else value
        return found


def _node(value: object, where: str, shape: Sequence[int]) -> tuple[int, int, int]:
    """Three integers inside the GameBoard's shape, or a refusal by name."""
    if not (isinstance(value, list) and len(value) == 3 and all(type(v) is int for v in value)):
        raise ValueError(f"{where}.node must be three integers, not {value!r}")
    if any(not 0 <= v < s for v, s in zip(value, shape, strict=True)):
        raise ValueError(f"{where}.node {value} must lie inside the shape {list(shape)}")
    return int(value[0]), int(value[1]), int(value[2])


def declarations(
    value: object,
    shape: Sequence[int],
    detectors: Sequence[str],
    families: Sequence[str],
    bodies: Sequence[int],
) -> tuple[Reading, ...]:
    """The world file's `readings` checked against SCHEMA, kind by kind, every refusal by name."""
    if not isinstance(value, list):
        raise ValueError("readings must be a list of readings, each with a name and a kind")
    found: list[Reading] = []
    for index, item in enumerate(value):
        where = f"readings[{index}]"
        if not isinstance(item, dict):
            raise ValueError(f"{where} must be an object with a name and a kind")
        kind = item.get("kind")
        if not isinstance(kind, str) or kind not in SCHEMA:
            raise ValueError(f"{where}.kind must be one of {list(SCHEMA)}, not {kind!r}")
        label, keys = SCHEMA[kind]
        expected = {"name", "kind", *keys}
        if set(item) - expected:
            raise ValueError(f"{where} has unknown keys: {', '.join(sorted(set(item) - expected))}")
        if expected - set(item):
            raise ValueError(f"{where} lacks keys: {', '.join(sorted(expected - set(item)))}")
        name = item["name"]
        if not isinstance(name, str) or not name:
            raise ValueError(f"{where}.name must be a nonempty string")
        if any(reading.name == name for reading in found):
            raise ValueError(f"two readings named {name!r}: every reading has its own name")
        every = item.get("every")
        if "every" in keys and (type(every) is not int or every < 1):
            raise ValueError(f"{where}.every must be an integer from 1, not {every!r}")
        detector = item.get("detector")
        if "detector" in keys and detector not in detectors:
            raise ValueError(
                f"{where}.detector names no detector of the world (the detectors: {list(detectors)})"
            )
        family = item.get("family")
        if "family" in keys and family not in families:
            raise ValueError(
                f"{where}.family names no family of the universe (the families: {list(families)})"
            )
        body = item.get("body")
        if "body" in keys and body not in bodies:
            raise ValueError(
                f"{where}.body names no measured entry with a block (the bodies: {list(bodies)})"
            )
        node = _node(item["node"], where, shape) if "node" in keys else None
        found.append(Reading(name, kind, label, every, detector, family, body, node))
    return tuple(found)


def world_readings(
    obj: Mapping[str, Any],
    shape: Sequence[int],
    detectors: Sequence[Any],
    families: Sequence[Any],
    measured: Sequence[Any],
) -> tuple[Reading, ...]:
    """The world file's readings as declarations, an empty tuple where the file declares none; the detectors', families' names and the bodies' numbers resolved from the loaded definitions."""
    if "readings" not in obj:
        return ()
    bodies = [number for number, entry in enumerate(measured) if entry.block is not None]
    return declarations(
        obj["readings"], shape, [d.name for d in detectors], [f.name for f in families], bodies
    )


class Readings:
    """The declared readings of one run: read at the declared intervals, the clicks after the run, written once."""

    def __init__(self, declared: Sequence[Reading]) -> None:
        self.declared = tuple(declared)
        self.lines: dict[str, list[dict[str, Any]]] = {reading.name: [] for reading in self.declared}

    def read(self, simulation: Any) -> None:
        """One interval's periodic readings at their stride, the interval 0 the loaded state."""
        for reading in self.declared:
            if reading.every is not None and simulation.tick % reading.every == 0:
                self.lines[reading.name].append(
                    {"interval": int(simulation.tick), **_read(reading, simulation)}
                )

    def clicks(self, gathers: Sequence[Mapping[str, Any]], detectors: Sequence[Any]) -> None:
        """A declared detector's clicks as its DETECTOR lines: the interval, the record, its giving, content, momentum and the detector's Nodes."""
        positions = {
            detector.name: [list(node) for node in detector.positions] for detector in detectors
        }
        for reading in self.declared:
            if reading.kind != "clicks":
                continue
            for gather in gathers:
                chosen = gather["chosen"]
                if not (isinstance(chosen, list) and chosen and chosen[0][0] == reading.detector):
                    continue
                self.lines[reading.name].append(
                    {
                        "interval": int(gather["click"]),
                        "record": gather["record"],
                        "giving": gather["giving"],
                        "content": gather["content"],
                        "momentum": [int(part) for part in gather["momentum"]],
                        "node": positions[reading.detector],
                    }
                )

    def output(self) -> list[dict[str, Any]]:
        """The readings in the declared order: name, kind, label, the target, the stride and the lines."""
        return [
            {"name": r.name, "kind": r.kind, "label": r.label, **r.target(), "lines": self.lines[r.name]}
            for r in self.declared
        ]


def _family_level(reading: Reading, simulation: Any) -> Any:
    """The family's level array now, the held record's and every live record's summed; None where none."""
    index = [family.name for family in simulation.families].index(reading.family)
    level = None
    arrays = [simulation.held_records[index].now] if index in simulation.held_records else []
    arrays += [live.now for live in simulation.records.values() if live.family == index]
    for array in arrays:
        level = array if level is None else level + array
    return level


def _read(reading: Reading, simulation: Any) -> dict[str, Any]:
    """One reading's numbers at this interval, by its kind."""
    if reading.kind == "alive":
        return {"alive": len(simulation.records)}
    if reading.kind == "centre":
        block = simulation.block_by_number[reading.body]
        extents = block.definition.extents
        return {"node": [(block.corner[a] + extents[a] // 2) % simulation.shape[a] for a in range(3)]}
    level = _family_level(reading, simulation)
    if reading.kind == "level":
        return {"level": 0 if level is None else int(level[reading.node])}
    if reading.kind == "support":
        return {"support": 0 if level is None else int((level != 0).sum())}
    return {"total": 0 if level is None else int(abs(level).astype(object).sum())}
