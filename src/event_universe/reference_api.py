"""Explicit supplied-law benchmarks; these APIs are not the ordinary run path."""

from pathlib import Path

from .core.disturbance_state import InitialState
from .disturbance_api import ReferenceSimulation
from .initialization import parse_json_document, parse_reference_state

__all__ = [
    "ReferenceSimulation",
    "load_reference_state",
    "parse_reference_json",
    "parse_reference_state",
]


def parse_reference_json(source: str | bytes) -> InitialState:
    return parse_reference_state(parse_json_document(source))


def load_reference_state(path: Path) -> InitialState:
    return parse_reference_json(path.read_bytes())
