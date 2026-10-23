"""Matter's birth from light at the meeting of two quanta at one Node, derived on the owner's word of 2026-10-23 and entered as the gapless meeting's own clause (`conversion.birth_of`; ALGEBRA.md, Matter's birth from light; docs/FURTHER_RESEARCH.md): (1) The former reading, the law as written to 2026-10-23, named and dated: the click's conservation is the rotation's exactness, the parents' Gaussian product over their dens equal to the children's (`conversion.exact`, `conversion.rotation`), the senses entering the charge's sum alone (`conversion.kept`) and never the point; two quanta of a gapless family [den, den] have the point (den, 0) each and the identity as their product, and no list of this project's pairs completes it ((num + i s)^2 imaginary or negative, two different pairs off the real axis), so the lister derived no list for two light quanta, and the second quantum at a Node stayed the books' deficit; that lister stands unchanged, with the sense the charge's sign and the point the same at both senses, the neutron's chain resting on it. (2) The sentence: where the parents' own list is empty, two quanta of a gapless family make the conjugate pair of a plane family, `birth_of`, every plane family with a gap and a Pythagorean pair at the senses -1 and 1, the lightest first: in the matter universe the electron pair then the proton pair, in the birth universe (real lines) none, on the board alone (matter not Pythagorean, no plane) none. (3) No shipped list changes: every universe file the shipped worlds name loads and its derived lists are the law's as written, the neutron's chain among them (the 27 universes' lists, frozen here by name)."""

import glob
import json
from pathlib import Path

from event_universe import conversion
from event_universe.loader.universe import universe_of
from tests.laws import ROOT

FOLDER = ROOT / "examples" / "events" / "universe24"
UNIVERSES = (
    "universe_universe24.json",
    "universe_universe24_matter.json",
    "universe_universe24_birth.json",
)
LISTS_AS_WRITTEN = {  # every shipped universe with a list, its lists by name (the parent: the records out and their senses)
    "nucleons_box.json": {"neutron": [("proton", 1), ("electron", -1)]},
    "nucleons_light.json": {"neutron": [("proton", 1), ("electron", -1)]},
    "nucleons_pythagorean.json": {"neutron": [("proton", 1), ("electron", -1)]},
    "universe_universe24_matter.json": {"proton": [("matter", 0), ("electron", 1)]},
    "universe_universe24_birth.json": {"dust": [("matter", 0), ("partner", 0)]},
}


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
        assert conversion.listed(families, ((light, 0), (light, 0)), {}) == [], (
            name
        )  # the lister as written: no list at any size searched
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
    families, names = families_of(FOLDER / "universe_universe24_matter.json")
    light = names.index("light")
    born = [[(names[k], sense) for k, sense in table] for table in conversion.birth_of(families, light)]
    assert born == [
        [("electron", -1), ("electron", 1)],
        [("proton", -1), ("proton", 1)],
    ]  # the lightest first: 3,600 T then 6,000 T
    for name in ("universe_universe24_birth.json", "universe_universe24.json"):
        families, names = families_of(FOLDER / name)
        assert conversion.birth_of(families, names.index("light")) == [], (
            name
        )  # real lines and a pair that is not Pythagorean: no child
    assert (
        conversion.birth_of(families, names.index("matter")) == []
    )  # a family with a gap births nothing: its own list is the conversion's


def test_no_shipped_universes_list_changes_under_the_sentence() -> None:
    universes = set()
    for world in glob.glob(str(ROOT / "examples" / "events" / "*" / "*.json")):
        document = json.loads(Path(world).read_text(encoding="utf-8"))
        if isinstance(document, dict) and isinstance(document.get("universe"), str):
            universes.add(document["universe"])
    assert len(universes) >= 27, len(universes)
    for relative in sorted(universes):
        families, names = families_of(ROOT / relative)  # every shipped universe loads
        lists = {
            family.name: [(names[k], sense) for k, sense in family.converts]
            for family in families
            if family.converts
        }
        assert lists == LISTS_AS_WRITTEN.get(Path(relative).name, {}), relative
