"""A reader of the sign writes its charge per quantum by its count unit, exact for a Pythagorean pair alone; a reader with an irrational sine is refused by name, as the conversion refuses it from every exact list (ALGEBRA.md, The conversion, 180; The constants; the owner's word of 2026-10-24, (ii), "closed"; the rounded count unit and the lcm of 236e74ed0 the former behaviour, kept by name as its defect: the hydrogen electron [4000, 6000]'s count unit 482,990,683,139 against the proton's 648,000,000,000, their lcm of order 10^23, the holder's wall above 2^63). The shipped worlds whose electron is [4000, 6000] stay as files, the records of the law as it stood to 2026-10-23, refused at load since 2026-10-24 (the owner's word: no re-lay of the record worlds), each named here with the sentence matched."""

from __future__ import annotations

import json

import pytest

from event_universe.loader.universe import universe_of
from event_universe.world_files import load_world
from tests.laws import ROOT, refused

IRRATIONAL = "a reader of the sign writes its charge per quantum by its count unit"
REFUSED = (
    "the read weight is one for every reader|" + IRRATIONAL
)  # the record worlds on hydrogen_read3.json (the electron's read 3) meet the read weight's sentence first, the others the sine's
EVENTS = ROOT / "examples" / "events"
REFUSED_WORLDS = (
    "atom/atom.json",
    "atom/atom_free.json",
    "atom/atom_1s.json",
    "atom/atom_2p.json",
    "atom/atom_line.json",
    "atom/hydrogen_1s.json",
    "atom/hydrogen_line.json",
    "conserve/beat_c11.json",
    "conserve/box_c15.json",
    "conserve/giver_c5.json",
    "conserve/mixed_c11.json",
    "conserve/pure_c11.json",
    "conserve/sum_c11.json",
    "conserve/taker_c5.json",
    "clicks/clicks_tube.json",
)


def test_a_sign_reader_with_an_irrational_sine_is_refused_by_name_and_a_pythagorean_one_admitted():
    sign = {"name": "charge", "pair": [1000, 1000]}  # the holder of the sign, the held massless row
    universe = {
        "integers": {"node_clock": 1000, "quantum_action": 36_000, "width": 92, "link_unit": 16},
        "families": [
            sign,
            {"name": "proton", "pair": [0, 1000], "dimension": 2},
            {"name": "electron", "pair": [800, 1000], "dimension": 2},
        ],
    }
    universe_of(universe)  # [800, 1000]: the sine 600, Pythagorean, admitted
    universe["families"][2]["pair"] = [666, 1000]  # 1,000,000 - 443,556 = 556,444, no square
    refusal = refused(IRRATIONAL, universe_of, universe)
    assert "'electron'" in str(refusal) and "556444" in str(refusal) and "2026-10-24" in str(refusal)


@pytest.mark.parametrize("world", REFUSED_WORLDS)
def test_the_shipped_worlds_with_the_electron_at_4000_over_6000_are_refused_at_load_by_name(world):  # type: ignore[no-untyped-def]
    path = EVENTS / world
    universe = json.loads(path.read_text(encoding="utf-8"))["universe"]
    electron = next(
        f
        for f in json.loads((ROOT / universe).read_text(encoding="utf-8"))["families"]
        if f["name"] == "electron"
    )
    assert electron["pair"] == [
        4000,
        6000,
    ]  # the pair kept: the world stands as the record of the law to 2026-10-23
    refusal = refused(REFUSED, load_world, path)
    assert "'electron'" in str(refusal) and ("[4000, 6000]" in str(refusal) or "is 3" in str(refusal))
