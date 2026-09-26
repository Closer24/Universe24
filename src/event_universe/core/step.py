"""The step file (law/step.json): the interval's places and, within each, the ordered names of the primitives the loop calls; one file shared by every world, read at the start, its digest in every run's output; the loop holds no order and no name of its own."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

STEP_FILE = "law/step.json"
# the five places of the interval (ALGEBRA.md 9.91 (8)) and "any", the trace's read-only line
PLACES: tuple[str, ...] = ("(i)", "(ii)", "(iii)", "(iv)", "(v)", "any")


@dataclass(frozen=True)
class Step:
    """The step as the file declares it: each place to its ordered names, and the file's digest."""

    places: Mapping[str, tuple[str, ...]]
    digest: str

    def position(self, name: str) -> tuple[str, int] | None:
        """The place and the index at which the file lists `name`, or None where it does not."""
        for place, names in self.places.items():
            if name in names:
                return place, names.index(name)
        return None


def read_step(document: object, digest: str, where: str = STEP_FILE) -> Step:
    """The file's form checked: an object with exactly the places, each a list of names, no name twice."""
    if not isinstance(document, dict):
        raise ValueError(f"{where} must be a JSON object with the places {list(PLACES)}")
    unknown = sorted(str(key) for key in set(document) - set(PLACES))
    if unknown:
        raise ValueError(f"{where} has unknown keys: {', '.join(unknown)} (the places: {list(PLACES)})")
    missing = [place for place in PLACES if place not in document]
    if missing:
        raise ValueError(f"{where} lacks the places: {', '.join(missing)}")
    seen: dict[str, str] = {}
    places: dict[str, tuple[str, ...]] = {}
    for place in PLACES:
        names = document[place]
        if not isinstance(names, list) or not all(isinstance(name, str) and name for name in names):
            raise ValueError(f"{where}.{place} must be a list of primitive names")
        for name in names:
            if name in seen:
                raise ValueError(
                    f"{where} lists {name!r} twice, at {seen[name]} and {place}: one place per primitive"
                )
            seen[name] = place
        places[place] = tuple(names)
    return Step(places, digest)
