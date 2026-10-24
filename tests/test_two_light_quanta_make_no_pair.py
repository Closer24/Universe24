"""Matter's birth from light at the meeting of two quanta at one Node, derived on the owner's word of 2026-10-23 and entered as the gapless meeting's own clause (`conversion.birth_of`; ALGEBRA.md, Matter's birth from light; docs/FURTHER_RESEARCH.md): (1) The former reading, the law as written to 2026-10-23, named and dated: the click's conservation is the rotation's exactness, the parents' Gaussian product over their dens equal to the children's (`conversion.exact`, `conversion.rotation`), the senses entering the charge's sum alone (`conversion.kept`) and never the point; two quanta of a gapless family [den, den] have the point (den, 0) each and the identity as their product, and no list of this project's pairs completes it ((num + i s)^2 imaginary or negative, two different pairs off the real axis), so the lister derived no list for two light quanta, and the second quantum at a Node stayed the books' deficit; that lister stands unchanged, with the sense the charge's sign and the point the same at both senses, the neutron's chain resting on it. (2) The sentence: where the parents' own list is empty, two quanta of a gapless family make the conjugate pair of a plane family, `birth_of`, every plane family with a gap and a Pythagorean pair at the senses -1 and 1, the lightest first: in Universe24's universe the electron pair then the proton pair (the former variants' universes, read on them: the birth universe of real lines none, the first board's matter [666, 1000], not Pythagorean, none). (3) No list changes: the one universe file loads and its derived list is the law's as written (the 27 shipped universes' lists stood here by name to 2026-10-24, when every world but Universe24 was cancelled)."""

import json
from pathlib import Path

from event_universe import conversion
from event_universe.loader.universe import universe_of
from tests.laws import ROOT

FOLDER = ROOT / "examples" / "events" / "universe24"
UNIVERSES = (
    "universe_universe24.json",
)  # the one world's universe at nature's den (2026-10-24): gravity, the sign holder, matter, light, the proton and electron planes


def families_of(path: Path):  # type: ignore[no-untyped-def]
    _integers, families = universe_of(json.loads(path.read_text(encoding="utf-8")))
    return families, [family.name for family in families]


def test_the_former_reading_two_light_quanta_have_the_identity_rotation_and_no_list() -> None:
    for name in UNIVERSES:
        families, names = families_of(FOLDER / name)
        light = names.index("light")
        den = families[light].pair[1]
        assert conversion.gaussian(families[light].pair) == (den, 0)  # the gapless point, no rotation
        assert conversion.rotation([families[light].pair] * 2) == (
            (den * den, 0),
            den * den,
        )  # the identity
        for k in conversion.candidates(families):
            assert not conversion.exact([families[light].pair] * 2, [families[k].pair] * 2), names[k]


def test_the_algebra_of_the_former_reading_on_the_pairs_of_the_matter_universe() -> None:
    electron, proton, matter = (800, 1000), (0, 1000), (600, 1000)
    assert conversion.gaussian(electron) == (800, 600) and conversion.gaussian(proton) == (0, 1000)
    assert conversion.rotation([electron, electron]) == (
        (800 * 800 - 600 * 600, 2 * 800 * 600),
        1000 * 1000,
    )
    assert conversion.rotation([proton, proton]) == ((-1000 * 1000, 0), 1000 * 1000)
    assert conversion.rotation([matter, electron]) == ((0, 1000 * 1000), 1000 * 1000)


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
        conversion.birth_of(families, names.index("matter")) == []
    )  # a family with a gap births nothing: its own list is the conversion's
