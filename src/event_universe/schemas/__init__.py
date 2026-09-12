"""Packaged JSON Schema Draft 2020-12 contracts, available without a validator dependency."""

import json
from importlib.resources import files
from typing import cast

SCHEMA_BASE = "https://raw.githubusercontent.com/Closer24/Universe24/main/src/event_universe/schemas/"
SCHEMA_NAMES = (
    "runtime",
    "experiment",
    "environment",
    "definitions",
    "initial_conditions",
    "run",
    "native-events",
    "unit-system",
)


def schema_document(name: str = "runtime") -> dict[str, object]:
    """Return a fresh formal schema; canonical parsing additionally checks semantics."""
    if name not in SCHEMA_NAMES:
        raise ValueError(f"unknown schema {name!r}; choose {', '.join(SCHEMA_NAMES)}")
    source = files(__package__).joinpath(f"{name}.schema.json").read_text(encoding="utf-8")
    return cast(dict[str, object], json.loads(source))
