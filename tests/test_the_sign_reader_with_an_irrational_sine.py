"""A reader of the sign writes its charge per quantum by its count unit, exact for a Pythagorean pair alone; a reader with an irrational sine is refused by name, as the conversion refuses it from every exact list (ALGEBRA.md, The conversion, 180; The constants; the owner's word of 2026-10-24, (ii), "closed"; the rounded count unit and the lcm of 236e74ed0 the former behaviour, kept by name as its defect: the hydrogen electron [4000, 6000]'s count unit 482,990,683,139 against the proton's 648,000,000,000, their lcm of order 10^23, the holder's wall above 2^63). The shipped worlds whose electron is [4000, 6000] stay as files, the records of the law as it stood to 2026-10-23, refused at load since 2026-10-24 (the owner's word: no re-lay of the record worlds), each named here with the sentence matched."""

from __future__ import annotations

import json

from event_universe import world_files
from event_universe.loader.universe import universe_of
from event_universe.world_files import load_world
from tests.laws import ROOT, refused

IRRATIONAL = "a reader of the sign writes its charge per quantum by its count unit"
WEIGHT = "the read weight is one for every reader"
UNIVERSE = ROOT / "examples" / "events" / "universe24" / "universe_universe24.json"


def test_a_sign_reader_with_an_irrational_sine_is_refused_by_name_and_a_pythagorean_one_admitted():
    sign = {
        "name": "charge",
        "pair": [1000, 1000],
        "reads": {},
        "held": {"sources": ["wronskian"], "level_weight": 1},
    }
    universe = {
        "integers": {"node_clock": 1000, "quantum_action": 36_000, "width": 92, "link_unit": 16},
        "families": [
            sign,
            {"name": "proton", "pair": [0, 1000], "reads": {"charge": 1}, "dimension": 2},
            {"name": "electron", "pair": [800, 1000], "reads": {"charge": 1}, "dimension": 2},
        ],
    }
    universe_of(universe)  # [800, 1000]: the sine 600, Pythagorean, admitted
    universe["families"][2]["pair"] = [666, 1000]  # 1,000,000 - 443,556 = 556,444, no square
    refusal = refused(IRRATIONAL, universe_of, universe)
    assert "'electron'" in str(refusal) and "556444" in str(refusal) and "2026-10-24" in str(refusal)


def test_the_one_universe_with_the_electron_reading_the_charge_at_3_is_refused_by_name(
    tmp_path, monkeypatch
):  # type: ignore[no-untyped-def]
    """The one universe file copied and changed in tmp_path, the electron's read of the charge 3 (the folded record's declaration to 2026-10-24), on the bare 3-cube torus: refused at load by the read weight's sentence (the owner's word of 2026-10-24, like nature; the cancelled worlds posed it to that day)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    universe = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    electron = next(f for f in universe["families"] if f["name"] == "electron")
    electron["reads"]["charge"] = 3
    (tmp_path / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    world = {"universe": "u.json", "shape": [3, 3, 3], "intervals": 1}
    (path := tmp_path / "bare.json").write_text(json.dumps(world), encoding="utf-8")
    refusal = refused(WEIGHT, load_world, path)
    assert "'electron'" in str(refusal) and "is 3" in str(refusal)
