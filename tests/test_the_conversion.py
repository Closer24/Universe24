"""The conversion in the toy as a test (2026-10-21; ALGEBRA.md, The conversion, Only a click moves a quantum between families; src/event_universe/conversion.py): the exactness clause, every family's list derived from the pairs under the law's conservations with no key (the owner's word of 2026-10-21, the table's declaration deleted; the senses of a real-line parent's plane records out the one residual declaration, the row's key `senses`), the loader's refusals by name, and the chain world examples/events/conversion/neutron_chain.json run to its first conversion with the blind written before the run: no conversion before the packet reaches the target, one conversion per credited quantum at the window's close, the counts n -1, p +1, e +1, the Wronskian's sum 0 at the lay by the exact split and the rotations' identity exact in the integers."""

import copy
import json

from event_universe import conversion
from event_universe.features.click import plane_squares, two_squares
from event_universe.lattice import Lattice
from event_universe.loader.universe import universe_of
from tests.laws import EVENTS, family, refused
from tests.laws_read import load_shipped

FOLDER = EVENTS / "conversion"
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


def table_of(document, name: str) -> list:  # type: ignore[no-untyped-def, type-arg]
    """A family's list as the loader derives it from a universe document, (family name, sense) per record out."""
    _integers, families = universe_of(document)
    return [
        (families[out].name, sense)
        for out, sense in next(f for f in families if f.name == name).converts
    ]


def test_the_loader_derives_every_familys_list_from_the_pairs_under_the_laws_conservations_and_refuses_by_name():
    """The shipped universe derives n -> p + e from the pairs, the electron's -1 the sum's from the proton's declared 1 and nothing else typed, and no other family has a list, the proton's stability by the baryon and the electron's by having no lighter charged family; a plane at [4800, 6000] or a real line at the electron's pair adds a list exact in rotation that the charge cuts, a second plane at the electron's pair a second list keeping both, refused; the old electron's universe is lawful with no key and nothing converts, and refused where the neutron declares senses for no list; the deleted key `converts`, a non-Pythagorean parent, a held row's and a plane parent's senses, a stray name, a contradiction of the sum and the missing declaration are refused by name; the flipped declaration is the anti-list; two parents' lists: the capture p + e -> n irreducible, two neutrons' and a neutron with an electron's lists reducible to the quanta's own clicks, no list for two like senses."""
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
    for row in (muon, neutral):
        added = universe_with()
        added["families"].append(row)
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
    refused("'converts', deleted", universe_of, universe_with(neutron={"senses": None, "converts": {}}))
    refused("a held row converts nothing", universe_of, universe_with(binding={"senses": {"proton": 1}}))
    refused(
        "a plane parent's records out", universe_of, universe_with(proton={"senses": {"electron": 1}})
    )
    refused("names 'antineutrino'", universe_of, universe_with(neutron={"senses": {"antineutrino": 1}}))
    stray = universe_with(neutron={"senses": {"proton": 1, "muon": 1}})
    stray["families"].append(muon)
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


def test_the_chain_converts_an_arriving_neutron_at_the_windows_close_exactly():
    """The blind on examples/events/conversion/neutron_chain.json over its first 40 intervals (the packet of two quanta laid at 24..36 travelling +x, the target 40..60, the window 12): no credit and no conversion line at the closes before the packet's share reaches the target; at the first crediting close one conversion line per credited neutron quantum with the same window, into proton and electron at the senses 1 and -1; the books move n -1, p +1, e +1 per quantum; the lay lines at the credited Node carry the proton's three planes at the exact split with Wronskians summing to 16384 and the electron's one plane at -16384, the sum 0; the identity of the rotations holds in the integers."""
    lines: list[dict] = []  # type: ignore[type-arg]
    board = Lattice(load_shipped(FOLDER / "neutron_chain.json"), lines.append)
    neutron, proton, electron = (family(board, name) for name in ("neutron", "proton", "electron"))
    assert board.families[neutron].converts == ((proton, 1), (electron, -1))
    counts = {k: board.credit.counts[k] for k in (neutron, proton, electron)}
    assert counts == {neutron: 2, proton: 0, electron: 0}
    first = None
    for _ in range(40):
        board.step()
        credits = [c for c in lines if c["event"] == "credit"]
        if credits and first is None:
            first = board.interval
    assert first is not None and first % board.world.draw.window == 0  # the when: a window's close
    credits = [c for c in lines if c["event"] == "credit" and c["interval"] <= first]
    conversions = [c for c in lines if c["event"] == "conversion"]
    assert [c["interval"] for c in conversions] == [first] * len(credits) and len(credits) >= 1
    for credit, converted in zip(credits, conversions, strict=True):
        assert credit["family"] == converted["family"] == "neutron"
        assert credit["window"] == converted["window"] == [first - board.world.draw.window + 1, first]
        assert converted["into"] == ["proton", "electron"] and converted["senses"] == [1, -1]
        assert converted["node_detector"] == credit["node_detector"] == "target"
    moved = len(credits)
    assert board.credit.counts[neutron] == 2 - moved  # the count by whole units, the write's own
    assert board.credit.counts[proton] == moved and board.credit.counts[electron] == moved
    lays = [line for line in lines if line["event"] == "lay" and line["interval"] == first]
    at = {tuple(line["node"]["at"]) for line in lays}
    assert len(at) == 1 and next(iter(at)) in {tuple(n) for n in board.world.node_detectors[0].positions}
    of = {
        name: sorted((row for row in lays if row["family"] == name), key=lambda row: row["line"])
        for name in ("proton", "electron")
    }
    proton_w = [wronskian(of["proton"][k], of["proton"][k + 1]) for k in range(0, 6, 2)]
    assert (
        sorted(proton_w) == [5450, 5458, 5476] and sum(proton_w) == HALF_ACTION
    )  # the exact split, the sense 1
    assert wronskian(of["electron"][0], of["electron"][1]) == -HALF_ACTION  # the sense -1
    assert (
        sum(proton_w) + wronskian(of["electron"][0], of["electron"][1]) == 0
    )  # the charge kept exactly
    assert conversion.exact(
        [board.families[neutron].pair], [board.families[k].pair for k in (proton, electron)]
    )
    assert not any(c["event"] == "conversion" and c["interval"] < first for c in lines)


def test_two_families_laid_toward_one_target_convert_by_their_own_lists_under_the_whether():
    """The world examples/events/conversion/neutron_electron_chain.json re-read under the floor and the remainder's draw (its blind's third round, written for the half-up count, and the re-read beneath it): the neutron's credit at 48 by the remainder's draw with its conversion alone into proton and electron at the senses 1 and -1, the electron's credit at 84 by the draw, each at its own close with no meeting (their one list {p, e, e} is reducible, the neutron's own beside the electron passing, asserted in the loader test), the books n 0, p 1, e 1 with no deficit, the erasing front the neutron's alone; deterministic per file."""
    lines: list[dict] = []  # type: ignore[type-arg]
    board = Lattice(load_shipped(FOLDER / "neutron_electron_chain.json"), lines.append)
    for _ in range(84):
        board.step()
    found = [
        (c["interval"], c["event"], c["family"], c.get("into"), c.get("senses"))
        for c in lines
        if c["event"] in ("credit", "conversion")
    ]
    assert found == [
        (48, "credit", "neutron", None, None),
        (48, "conversion", "neutron", ["proton", "electron"], [1, -1]),
        (84, "credit", "electron", None, None),
    ]
    counts = {board.families[i].name: board.credit.counts[i] for i in board.order}
    assert (counts["neutron"], counts["proton"], counts["electron"]) == (0, 1, 1)
    assert not any(board.credit.deficits.values())
    assert {e["family"] for e in lines if e["event"] == "erasure"} == {"neutron"}
