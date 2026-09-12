"""Validate passive probe placement independently of physical state and recording."""

from dataclasses import dataclass
from pathlib import Path

from event_universe.core.disturbance_state import Address3
from event_universe.json_documents import parse_json_document


@dataclass(frozen=True)
class ObserverDefinition:
    """Placement and host archive capacity; neither changes a physical law."""

    position: Address3
    max_receipts: int = 100000

    @classmethod
    def load(cls, path: Path, shape: Address3) -> ObserverDefinition:
        return cls.parse(parse_json_document(path.read_bytes()), shape)

    @classmethod
    def parse(cls, raw: object, shape: Address3) -> ObserverDefinition:
        if not isinstance(raw, dict) or set(raw) - {"position", "max_receipts"}:
            raise ValueError("observer configuration accepts position and max_receipts only")
        position = raw.get("position")
        if (
            not isinstance(position, list)
            or len(position) != 3
            or any(
                type(v) is not int or not 0 <= v < size for v, size in zip(position, shape, strict=True)
            )
        ):
            raise ValueError("observer position must be three integer coordinates inside the world")
        capacity = raw.get("max_receipts", 100000)
        if type(capacity) is not int or not 1 <= capacity <= 1000000:
            raise ValueError("observer max_receipts must be an integer from 1 to 1000000")
        return cls((position[0], position[1], position[2]), capacity)
