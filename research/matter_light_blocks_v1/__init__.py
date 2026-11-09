"""Published building blocks of the matter/light research program (data only).

Every block is an initial preparation in the official init format plus one of
the eight fixed sign triples. Nothing here evolves a state; the unchanged
engine does. See README.md.

    from research.matter_light_blocks_v1 import load, names
    engine, initial, steps, entry = load("fiber_x_packet")
"""
from .verify import load, load_catalog


def names(group: str | None = None) -> list[str]:
    return [e["name"] for e in load_catalog()["entries"] if group is None or e["group"] == group]


__all__ = ["load", "load_catalog", "names"]
