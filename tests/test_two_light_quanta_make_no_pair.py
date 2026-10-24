"""Matter's birth from light, the gapless meeting's own clause (conversion.birth_of; ALGEBRA.md, Matter's birth from light): on the one universe file two quanta of light make the conjugate pair of a plane family with a gap and a Pythagorean pair at the senses -1 and 1, the lists the lightest first, and a family with a gap births nothing."""

import json
from pathlib import Path

from event_universe import conversion
from event_universe.loader.universe import universe_of
from tests.laws import ROOT

FOLDER = ROOT / "examples" / "events" / "universe24"
UNIVERSES = (
    "universe_universe24.json",
)  # the one world's universe at nature's den (2026-10-24): gravity, the sign holder, light, the proton and electron planes (matter's row left the same day)


def families_of(path: Path):  # type: ignore[no-untyped-def]
    _integers, families = universe_of(json.loads(path.read_text(encoding="utf-8")))
    return families, [family.name for family in families]


def test_the_sentence_births_the_conjugate_pair_of_a_plane_family_lightest_first() -> None:
    families, names = families_of(FOLDER / "universe_universe24.json")
    light = names.index("light")
    born = [[(names[k], sense) for k, sense in table] for table in conversion.birth_of(families, light)]
    assert (
        born
        == [
            [("electron", -1), ("electron", 1)],
            [("proton", -1), ("proton", 1)],
        ]
    )  # the lister's order, the lightest first: the electron's gap 29,276^2 before the proton's; the one born the heaviest within the two quanta's energy (act.born_table, 2026-10-24)
    assert (
        conversion.birth_of(families, names.index("proton")) == []
    )  # a family with a gap births nothing: its own list is the conversion's
