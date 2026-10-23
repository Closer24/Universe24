"""Matter's birth from light at the meeting of two quanta at one Node, derived under The conversion as written and found not to hold (the owner's word of 2026-10-23, derive it first; docs/FURTHER_RESEARCH.md, the item Matter's birth from light): the law's conservation at a click is the rotation's exactness, the parents' Gaussian product over their dens equal to the children's (`conversion.exact`, `conversion.rotation`), the senses entering the charge's conservation alone (`conversion.kept`) and never the point. Two quanta of a gapless family [den, den] have the point (den, 0) each, their product the identity (den^2, 0) over den^2; a list completing it needs the children's Gaussian product real and positive; two records of one gapped pair give (num + i s)^2 = num^2 - s^2 + 2 i num s, imaginary where num is above 0 and -s^2 below 0 where num is 0, and two records of different gapped pairs give a point off the real axis for every pair of this project's universes (600 + 800 i times 800 + 600 i is 1,000,000 i); so the law's own lister derives NO list for two light quanta in Universe24's three universes, the board alone (matter [666, 1000], not Pythagorean), the matter universe (matter [600, 1000], the proton [0, 1000] and the electron [800, 1000] as planes) and the birth universe (dust [0, 1000], matter [600, 1000], partner [800, 1000]), and the second quantum at a Node stays the books' deficit as The click writes on the lattice reads it. The algebra is the test; nothing is built until a conservation that conjugates the point at the sense is derived and entered."""

import json

from event_universe import conversion
from event_universe.loader.universe import universe_of
from tests.laws import ROOT

FOLDER = ROOT / "examples" / "events" / "universe24"
UNIVERSES = (
    "universe_universe24.json",
    "universe_universe24_matter.json",
    "universe_universe24_birth.json",
)


def test_two_light_quanta_have_the_identity_rotation_and_no_list_in_any_universe24_universe() -> None:
    for name in UNIVERSES:
        _integers, families = universe_of(json.loads((FOLDER / name).read_text(encoding="utf-8")))
        names = [family.name for family in families]
        light = names.index("light")
        den = families[light].pair[1]
        assert conversion.gaussian(families[light].pair) == (den, 0)  # the gapless point, no rotation
        assert conversion.rotation([families[light].pair] * 2) == (
            (den * den, 0),
            den * den,
        )  # the identity
        assert conversion.listed(families, ((light, 0), (light, 0)), {}) == [], (
            name
        )  # no child by the law's lister
        for k in conversion.candidates(families):  # two records of one gapped pair never complete it
            assert not conversion.exact([families[light].pair] * 2, [families[k].pair] * 2), names[k]


def test_the_algebra_of_the_refusal_on_the_pairs_of_the_matter_universe() -> None:
    electron, proton, matter = (800, 1000), (0, 1000), (600, 1000)
    assert conversion.gaussian(electron) == (800, 600) and conversion.gaussian(proton) == (0, 1000)
    assert conversion.rotation([electron, electron]) == (
        (800 * 800 - 600 * 600, 2 * 800 * 600),
        1000 * 1000,
    )  # imaginary part 960,000
    assert conversion.rotation([proton, proton]) == (
        (-1000 * 1000, 0),
        1000 * 1000,
    )  # the real axis, negative: not the identity
    assert conversion.rotation([matter, electron]) == (
        (0, 1000 * 1000),
        1000 * 1000,
    )  # 600 + 800 i times 800 + 600 i, pure imaginary
    assert not conversion.exact([(1000, 1000)] * 2, [electron, electron])
    assert not conversion.exact([(1000, 1000)] * 2, [proton, proton])
    assert not conversion.exact([(1000, 1000)] * 2, [matter, electron])
