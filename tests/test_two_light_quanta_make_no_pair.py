"""Matter's birth from light, the gapless meeting's own clause (conversion.birth_of; ALGEBRA.md, Matter's birth from light; the birth's selector, 2026-10-24, 13:xx UTC): on the one universe file two quanta of the massless point make the conjugate pair of a plane at a LIFT of den's primes (loader/circle.lift_points), the lists the lightest first by the gap den^2 - num^2, three at the den of three primes, the electron's, the proton's and the neutron's by mass; the swaps and the composed points are rows and no lists (the former list over every point of the circle, 26, kept by name); the massless point and the holders no record out; a family with a gap births nothing."""

import json

from event_universe import conversion
from event_universe.loader.circle import lift_points, vector_of
from event_universe.loader.universe import MASSLESS, universe_of
from tests.laws import ROOT, resolved

UNIVERSE = ROOT / "examples" / "events" / "universe24" / "universe_universe24.json"


def test_the_sentence_births_the_conjugate_pair_of_a_plane_family_lightest_first() -> None:
    _integers, families = universe_of(json.loads(UNIVERSE.read_text(encoding="utf-8")))
    names = [family.name for family in families]
    light = names.index(MASSLESS)
    born = conversion.birth_of(families, light)
    gap = lambda k: families[k].pair[1] ** 2 - families[k].pair[0] ** 2  # noqa: E731
    planes = sorted((k for k, f in enumerate(families) if f.plane), key=gap)
    lifts = {num for _vector, num, _sine in lift_points(families[light].pair[1])}
    assert born == [((k, -1), (k, 1)) for k in planes if families[k].pair[0] in lifts] and len(born) == 3
    assert (
        [names[k] for (k, _sense), _other in born]
        == [
            "point 0 0 2",
            "point 2 0 0",
            "point 0 2 0",
        ]
        and all(vector_of(names[k]) for k in planes)
    )  # the lifts alone, the least leg first (the selector, 2026-10-24; point 0 2 0, 0 0 2, 2 0 0 at the top tier); 26 lists before it
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
