"""The conversion in the toy as a test (2026-10-21; ALGEBRA.md, The conversion, Only a click moves a quantum between families; src/event_universe/conversion.py): the exactness clause, every family's list derived from the pairs under the law's conservations with no key (the owner's word of 2026-10-21, the table's declaration deleted; the senses of a real-line parent's plane records out the one residual declaration, the row's key `senses`), the loader's refusals by name, and the chain world examples/events/conversion/neutron_chain.json run to its first conversion with the blind written before the run: no conversion before the packet reaches the target, one conversion per credited quantum at the window's close, the counts n -1, p +1, e +1, the Wronskian's sum 0 at the lay by the exact split and the rotations' identity exact in the integers."""

import copy
import json

from event_universe import conversion
from event_universe.features.click import plane_squares, two_squares
from event_universe.loader.universe import universe_of
from tests.laws import EVENTS, refused

FOLDER = EVENTS / "conversion"  # the record's universe file, read as a document of pairs and no world
UNIVERSE = json.loads((FOLDER / "nucleons_pythagorean.json").read_text(encoding="utf-8"))
NEUTRON, PROTON, ELECTRON, OLD_ELECTRON = (-4800, 6000), (0, 6000), (3600, 6000), (4000, 6000)
HALF_ACTION = 16384  # T div 2 at T = 32768, the Wronskian of one quantum at the quarter-turn lay


def universe_with(**changes):  # type: ignore[no-untyped-def]
    """The shipped universe with a family's row changed: per family name the keys to set (None deletes)."""
    document = copy.deepcopy(UNIVERSE)
    for row in document["families"]:
        for key, value in changes.get(row["name"], {}).items():
            if value is None:
                row.pop(key, None)
            else:
                row[key] = value
    return document


def wronskian(line_re: dict, line_im: dict) -> int:  # type: ignore[type-arg]
    """A plane's Wronskian from its two lay lines, re_now im_before - im_now re_before of the levels after the lay."""
    return line_re["after"][0] * line_im["after"][1] - line_im["after"][0] * line_re["after"][1]


def test_the_rotations_sum_exactly_iff_every_pair_is_pythagorean_and_the_split_carries_the_quantum_whole():
    """The exactness clause: the neutron's point (-4800, 3600) is the proton's (0, 6000) times the electron's (3600, 4800) over den, so pi/2 + arccos(3/5) = arccos(-4/5) in the integers, and no list with the old electron [4000, 6000] is exact (its sine irrational); two parents' rotations the Gaussian product of their points over their dens, p + e summing to n exactly; the lay's exact split of T div 2 over three planes is (73, 11), (57, 47), (74, 0), the sums 5450 + 5458 + 5476 = 16384 within a spread of 26 where 3 x 73^2 falls 397 short; one plane takes (128, 0)."""
    assert conversion.gaussian(NEUTRON) == (-4800, 3600) and conversion.gaussian(PROTON) == (0, 6000)
    assert conversion.gaussian(ELECTRON) == (3600, 4800) and conversion.gaussian(OLD_ELECTRON) is None
    assert conversion.exact([NEUTRON], [PROTON, ELECTRON]) and conversion.exact(
        [NEUTRON], [ELECTRON, PROTON]
    )
    assert not conversion.exact([NEUTRON], [PROTON, OLD_ELECTRON]) and not conversion.exact(
        [NEUTRON], [PROTON]
    )
    assert not conversion.exact([NEUTRON], [ELECTRON, ELECTRON]) and not conversion.exact(
        [NEUTRON], [PROTON, PROTON]
    )
    assert conversion.exact([PROTON, ELECTRON], [NEUTRON]) and conversion.rotation(
        [PROTON, ELECTRON]
    ) == (
        (-28800000, 21600000),
        36000000,
    )
    split = plane_squares(HALF_ACTION, 3)
    assert split == [(73, 11), (57, 47), (74, 0)]
    sums = [a * a + b * b for a, b in split]
    assert sum(sums) == HALF_ACTION and max(sums) - min(sums) == 26 and 3 * 73 * 73 == HALF_ACTION - 397
    assert plane_squares(HALF_ACTION, 1) == [(128, 0)] and two_squares(5461) is None
    assert plane_squares(HALF_ACTION * 2, 2) == [(128, 0), (128, 0)]


def laid_row(family: int, count: int):  # type: ignore[no-untyped-def]
    """A laid row as the loader's multiset check reads it: its family and its quanta."""
    return type("Row", (), {"family": family, "counts": (count,)})()


def table_of(document, name: str) -> list:  # type: ignore[no-untyped-def, type-arg]
    """A family's list as the loader derives it from a universe document, (family name, sense) per record out."""
    _integers, families = universe_of(document)
    return [
        (families[out].name, sense)
        for out, sense in next(f for f in families if f.name == name).converts
    ]


def test_the_loader_derives_every_familys_list_from_the_pairs_under_the_laws_conservations_and_refuses_by_name():
    """The shipped universe derives n -> p + e from the pairs, the electron's -1 the sum's from the proton's declared 1 and nothing else typed, and no other family has a list, the proton's stability by the baryon and the electron's by having no lighter charged family; a plane at [4800, 6000] or a real line at the electron's pair adds a list exact in rotation that the charge cuts, a second plane at the electron's pair a second list keeping both, refused; the old electron's universe is lawful with no key and nothing converts, and refused where the neutron declares senses for no list; the deleted key `converts` (refused since 2026-10-23 as every key the one-Node loader does not read, "unknown key", where the former loader named it deleted), a non-Pythagorean parent, a held row's and a plane parent's senses, a stray name (its plane reading no sign holder since 2026-10-23, so the stray is met before the one Node's alpha gate of one ratio per holder), a contradiction of the sum and the missing declaration are refused by name; the flipped declaration is the anti-list; two parents' lists: the capture p + e -> n irreducible, two neutrons' and a neutron with an electron's lists reducible to the quanta's own clicks, no list for two like senses."""
    assert table_of(UNIVERSE, "neutron") == [("proton", 1), ("electron", -1)]
    _integers, families = universe_of(UNIVERSE)
    assert all(not f.converts for f in families if f.name != "neutron")
    reads = {"gravity": 1, "binding": 1, "charge": 1}  # a plane's reads, the sign among them
    muon = {"name": "muon", "pair": [4800, 6000], "dimension": 2, "reads": reads}
    neutral = {
        "name": "neutral",
        "pair": [3600, 6000],
        "dimension": 1,
        "reads": {"gravity": 1, "binding": 1},
    }
    added = universe_with()
    added["families"].append(muon)
    _integers, with_muon = universe_of(
        added
    )  # a second pair reading the sign loads: one alpha per holder with any pairs under it, the charge the Wronskian per quantum (The constants, 2026-10-24; the refusal "one ratio per holder" of 2026-10-23 kept by name)
    assert not next(
        f for f in with_muon if f.name == "muon"
    ).converts  # the muon [4800, 6000]: no list of the shipped pairs sums to it
    added = universe_with()
    added["families"].append(neutral)
    assert table_of(added, "neutron") == [
        ("proton", 1),
        ("electron", -1),
    ]  # the charge cuts the second list
    added["families"].append({"name": "twin", "pair": [3600, 6000], "dimension": 2, "reads": reads})
    refused("several exact lists keep the charge and the baryon", universe_of, added)
    old = universe_with(electron={"pair": [4000, 6000]}, neutron={"senses": None})
    assert all(not f.converts for f in universe_of(old)[1])  # no exact split: nothing converts
    refused(
        "no square: its sine is irrational", universe_of, universe_with(electron={"pair": [4000, 6000]})
    )
    refused("no list sums to it exactly", universe_of, universe_with(neutron={"pair": [-4000, 6000]}))
    refused(
        "unknown key 'converts'", universe_of, universe_with(neutron={"senses": None, "converts": {}})
    )
    refused("a held row converts nothing", universe_of, universe_with(binding={"senses": {"proton": 1}}))
    refused(
        "a plane parent's records out", universe_of, universe_with(proton={"senses": {"electron": 1}})
    )
    refused("names 'antineutrino'", universe_of, universe_with(neutron={"senses": {"antineutrino": 1}}))
    stray = universe_with(neutron={"senses": {"proton": 1, "muon": 1}})
    stray["families"].append({**muon, "reads": neutral["reads"]})  # no sign holder read: the stray first
    refused("no record out of its one list", universe_of, stray)
    refused(
        "contradicts the Wronskian's sum",
        universe_of,
        universe_with(neutron={"senses": {"proton": 1, "electron": 1}}),
    )
    refused("is required", universe_of, universe_with(neutron={"senses": None}))
    assert table_of(universe_with(neutron={"senses": {"electron": 1}}), "neutron") == [
        ("proton", -1),
        ("electron", 1),
    ]
    assert table_of(
        universe_with(neutron={"senses": {"proton": 1, "electron": -1}}), "neutron"
    ) == table_of(UNIVERSE, "neutron")
    n, p, e = (
        next(k for k, f in enumerate(families) if f.name == name)
        for name in ("neutron", "proton", "electron")
    )
    senses = dict(families[n].senses)
    assert conversion.listed(families, ((p, 1), (e, -1)), senses) == [
        ((n, 0),)
    ]  # the capture, irreducible
    assert conversion.listed(families, ((p, 1), (e, 1)), senses) == []  # the senses' sum 2 keeps no list
    assert (
        conversion.listed(families, ((n, 0), (n, 0)), senses) == []
    )  # {n, p, e} and {p, p, e, e} reducible
    assert (
        conversion.listed(families, ((n, 0), (e, 1)), senses) == []
    )  # {p, e, e} is n's list beside e passing
    assert conversion.reducible(families, ((n, 0), (n, 0)), ((n, 0), (p, 1), (e, -1)))
    assert conversion.together(families, [laid_row(n, 2), laid_row(e, 1)]) is None  # no several lists
