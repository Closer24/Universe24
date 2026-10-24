"""A reader of the sign writes its charge per quantum by its count unit, exact for a Pythagorean pair alone; a reader with an irrational sine is refused by name (ALGEBRA.md, The constants; the owner's word of 2026-10-24, (ii), "closed"): posed on rows by hand, since the file carries no row (the same day's later word, declaring a family is forbidden) and every plane row the loader derives from den is a point of den's circle, Pythagorean by construction; and the one universe file with a family row written back into it is refused by name with the derivation's sentence."""

import json

from event_universe import world_files
from event_universe.conversion import sine_of
from event_universe.loader.universe import universe_of
from event_universe.world_files import load_world
from tests.laws import ROOT, refused, resolved

IRRATIONAL = "a reader of the sign writes its charge per quantum by its count unit"
UNIVERSE = ROOT / "examples" / "events" / "universe24" / "universe_universe24.json"


def test_a_sign_reader_with_an_irrational_sine_is_refused_by_name_and_a_pythagorean_one_admitted():
    sign = {"name": "charge", "pair": [1000, 1000]}  # the holder of the sign, the held massless row
    proton, electron = (
        {"name": "proton", "pair": [0, 1000], "dimension": 2},
        {"name": "electron", "pair": [800, 1000], "dimension": 2},
    )
    resolved(
        sign, proton, electron, node_clock=1000, quantum_action=36_000
    )  # [800, 1000]: the sine 600, Pythagorean, admitted
    electron["pair"] = [666, 1000]  # 1,000,000 - 443,556 = 556,444, no square
    refusal = refused(
        IRRATIONAL, resolved, sign, proton, electron, node_clock=1000, quantum_action=36_000
    )
    assert "'electron'" in str(refusal) and "556444" in str(refusal) and "2026-10-24" in str(refusal)
    _integers, families = universe_of(
        json.loads(
            '{"integers": {"den": 1166991900949580266237, "node_clock": 1000, "quantum_action": 36000}}'
        )
    )
    assert all(
        sine_of(f.pair) is not None for f in families if f.plane
    )  # every derived plane Pythagorean (the top tier's 26 points; the PeV den's in the loader's circle test)


def test_the_one_universe_with_a_family_row_written_back_is_refused_by_name(tmp_path, monkeypatch):  # type: ignore[no-untyped-def]
    """The one universe file copied and changed in tmp_path, the electron's row of the file to 2026-10-24 written back under `families`, on the bare 3-cube torus: refused at load by the gone key's sentence (the owner's word of 2026-10-24: declaring a family is forbidden), the derivation that replaced it named."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    universe = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    den = universe["integers"]["den"]
    universe["families"] = [{"name": "electron", "pair": [den - 8, den], "dimension": 2}]
    (tmp_path / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    world = {"universe": "u.json", "shape": [3, 3, 3], "intervals": 1}
    (path := tmp_path / "bare.json").write_text(json.dumps(world), encoding="utf-8")
    refusal = refused("holds the key 'families', a declaration no file carries", load_world, path)
    assert "every Pythagorean point of den's circle" in str(refusal) and "kept by name" in str(refusal)
