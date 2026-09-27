"""The step file (law/step.json): the interval's acts in their order, each a primitive's name at its place with the words of its call, the places derived from it; one file shared by every world, read at the start, its digest in every run's output; the loop holds the interval's frame (the clock, the bodies' clocks, the deletion, the readings) and the record's fused chain, and refuses a file ordering the chain otherwise."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

STEP_FILE = "law/step.json"
# the five places of the interval (ALGEBRA.md #the-interval) and "any", the trace's read-only line
PLACES: tuple[str, ...] = ("(i)", "(ii)", "(iii)", "(iv)", "(v)", "any")
INTERVAL = "interval"
ACT_FORM = "[place, name] or [place, name, words] (words: an object of the call's words to booleans or integers)"

Words = tuple[tuple[str, object], ...]
Act = tuple[str, str, Words]


@dataclass(frozen=True)
class Step:
    """The step as the file declares it: each place to its ordered names (derived from the acts by first appearance), the file's digest, and the acts themselves as (place, name, words)."""

    places: Mapping[str, tuple[str, ...]]
    digest: str
    acts: tuple[Act, ...] = ()

    def position(self, name: str) -> tuple[str, int] | None:
        """The place and the index at which the file lists `name`, or None where it does not."""
        for place, names in self.places.items():
            if name in names:
                return place, names.index(name)
        return None


def _act(entry: object, where: str, index: int) -> Act:
    """One act of the file checked: its place, its name and the words of its call."""
    label = f"{where}.{INTERVAL}[{index}]"
    if not isinstance(entry, list) or len(entry) not in (2, 3):
        raise ValueError(f"{label} must be {ACT_FORM}")
    place, name = entry[0], entry[1]
    if not isinstance(place, str) or not isinstance(name, str) or not name:
        raise ValueError(f"{label} must be {ACT_FORM}")
    if place not in PLACES:
        raise ValueError(f"{label} names the place {place!r}, which is none of {list(PLACES)}")
    words: dict[str, object] = {}
    if len(entry) == 3:
        words = entry[2]
        if not isinstance(words, dict) or not all(
            isinstance(key, str) and type(value) in (bool, int) for key, value in words.items()
        ):
            raise ValueError(f"{label} must be {ACT_FORM}")
    return place, name, tuple(sorted(words.items()))


def read_step(document: object, digest: str, where: str = STEP_FILE) -> Step:
    """The file's form checked: an object with the one key "interval", a list of acts, a name at one place, no act twice; the places derived."""
    if not isinstance(document, dict):
        raise ValueError(
            f"{where} must be a JSON object with the key {INTERVAL!r}: the acts of one interval in their order"
        )
    unknown = sorted(str(key) for key in set(document) - {INTERVAL})
    if unknown:
        raise ValueError(f"{where} has unknown keys: {', '.join(unknown)} (the one key: {INTERVAL!r})")
    if INTERVAL not in document:
        raise ValueError(f"{where} lacks the key {INTERVAL!r}")
    entries = document[INTERVAL]
    if not isinstance(entries, list):
        raise ValueError(f"{where}.{INTERVAL} must be a list of acts, each {ACT_FORM}")
    acts: list[Act] = []
    seen: dict[str, str] = {}
    for index, entry in enumerate(entries):
        act = _act(entry, where, index)
        place, name, words = act
        if seen.get(name, place) != place:
            raise ValueError(
                f"{where} lists {name!r} at {seen[name]} and {place}: one place per primitive"
            )
        if act in acts:
            raise ValueError(
                f"{where} lists the act {name!r} at {place} with the words {dict(words)} twice: one act, one call"
            )
        seen[name] = place
        acts.append(act)
    places = {
        place: tuple(dict.fromkeys(name for p, name, _w in acts if p == place)) for place in PLACES
    }
    return Step(places, digest, tuple(acts))
