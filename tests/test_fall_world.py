"""THE FALL's chain world (ALGEBRA.md #the-rows-against-nature (i); the owner's order of 17:08Z): the world in the law's form beside its mode file (the tool's, the world file's digest inside) and its expectation file in two sections, DETECTOR (the records' clicks at the falling body) and GAMEBOARD (the momentum growing by the feed, the centre), written before any run; the loader's word on the giving body in the law's form decides whether the frame takes it today."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from event_universe.core.register import discover
from event_universe.core.schema import Context
from event_universe.loader import frame

ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / "examples" / "events" / "generated" / "fall.json"


def test_the_falls_world_its_mode_file_and_its_expectation_agree():
    """The world: one universe file in the law's form, two bodies by their Nodes with their counts, momentum and phase_denominator, a detector on each, the readings of the momentum and the centre; the mode file carries the world's digest, the giver's mode with its period by the one-Node rule and the light body's own reading; the expectation file's two sections name the row and carry the DETECTOR pins and the GAMEBOARD pins apart; the frame takes the resting body and names the giving body's key where it refuses it today."""
    sys.set_int_max_str_digits(0)  # the mode file's rotation is an exact fraction of hundreds of digits
    document = json.loads(WORLD.read_text(encoding="utf-8"))
    universe = json.loads((ROOT / document["universe"]).read_text(encoding="utf-8"))
    rows = {row["name"]: row for row in universe["families"]}
    assert rows["matter"]["pair"] == [800, 1200] and rows["charge"]["clock"] == [512, 1]
    heavy, light = document["measured"]
    assert "emitter" in heavy and "stocks" in heavy and "emitter" not in light
    assert all("phase_denominator" in body and "fixed" not in body for body in (heavy, light))
    assert [reading["kind"] for reading in document["readings"]] == ["momentum", "centre", "momentum"]
    assert [detector["block"] for detector in document["detectors"]] == [1, 0]
    try:
        assert (
            len(frame.bodies(frame.world(document)["measured"], Context(tuple(rows)), discover())) == 2
        )
    except ValueError as refusal:  # the giving body in the law's form waits on the loader's item 3
        assert "emitter" in str(refusal) or "phase_denominator" in str(refusal)
    mode = json.loads(WORLD.with_suffix(".mode.json").read_text(encoding="utf-8"))
    assert mode["world_digest"] == hashlib.sha256(WORLD.read_bytes()).hexdigest()
    assert mode["rest"]["gravity"]["at_bodies"] == 3000 and mode["bodies"][0]["period"] >= 1
    assert mode["bodies"][0]["moving"]["phase_pair"] == [1024, 0]
    expectation = json.loads(WORLD.with_suffix(".expectation.json").read_text(encoding="utf-8"))
    assert "(i) THE FALL" in expectation["row"] and set(expectation) >= {"DETECTOR", "GAMEBOARD"}
    assert all(pin["detector"] == "at_fall" for pin in expectation["DETECTOR"])
    assert all(pin["body"] == 1 and "interval" in pin for pin in expectation["GAMEBOARD"])
