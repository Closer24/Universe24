"""Matter's birth from light, the gapless meeting's own clause (conversion.birth_of; ALGEBRA.md, Matter's birth from light): on the one universe file two quanta of the massless point make the conjugate pair of a plane with a gap and a Pythagorean pair at the senses -1 and 1, the lists the lightest first by the gap den^2 - num^2, every point of den's circle a list since the file carries no row (2026-10-24, the owner's word: declaring a family is forbidden; the loader derives every point as a plane until the kind sentence lands); a family with a gap births nothing, its own list the conversion's; and no list for two light quanta under The conversion as written (a massless family is no record out)."""

import json

from event_universe import conversion
from event_universe.loader.circle import vector_of
from event_universe.loader.universe import MASSLESS, universe_of
from tests.laws import resolved


def test_the_sentence_births_the_conjugate_pair_of_a_plane_family_lightest_first() -> None:
    _integers, families = universe_of(
        json.loads(
            '{"integers": {"den": 1166991900949580266237, "node_clock": 1000, "quantum_action": 36000}}'
        )
    )  # the top tier's den, the sentence the law's at every den
    names = [family.name for family in families]
    light = names.index(MASSLESS)
    born = conversion.birth_of(families, light)
    planes = sorted(
        (k for k, f in enumerate(families) if f.plane),
        key=lambda k: families[k].pair[1] ** 2 - families[k].pair[0] ** 2,
    )
    assert (
        born == [((k, -1), (k, 1)) for k in planes] and len(born) == 3**3 - 1
    )  # every point, the lightest first
    assert names[born[0][0][0]] == "point 0 2 0" and all(
        vector_of(names[k]) for k in planes
    )  # the least leg first (point 0 0 2 at the PeV den, the loader's circle test)
    assert sorted(conversion.candidates(families)) == sorted(
        planes
    )  # the massless point and the holders no record out
    gapped = resolved(
        {"name": "charge", "pair": [6000, 6000]},
        {"name": "matter", "pair": [4000, 6000], "dimension": 1},
        {"name": "light", "pair": [6000, 6000], "dimension": 1},
    )
    assert (
        conversion.birth_of(gapped, 1) == []
    )  # a family with a gap births nothing: its own list is the conversion's
    assert conversion.birth_of(gapped, 2) == []  # two light quanta with no plane under the sign: no list
