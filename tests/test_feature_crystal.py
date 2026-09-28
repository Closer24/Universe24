"""THE CRYSTAL and THE PAIR RECORD (ALGEBRA.md #the-primitives, the row "the crystal"; #the-ladder, THE PAIR RECORD, THE LABELS' CLICKS and THE HALF QUANTUM): a body with the key `crystal` gives one record of rank 2 at the click of an arriving record on its set, at the arriving norm over twice its denominator with two identical labels, and each label clicks alone at its own side by its own ladder, the first click making the record rank 1 everywhere at once."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from event_universe.core.register import discover, folder_of
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.features.crystal import (
    DECLARATION,
    CrystalOwn,
    CrystalStart,
    CrystalTerm,
    apply,
    read_term,
)
from event_universe.world_files import input_digest, input_stamp, load_world

sys.path.insert(0, __file__.rsplit("/tests/", 1)[0] + "/tools")

from body_generator import generate, mode_document, split_levels  # noqa: E402

EMITTER, LEFT, CRYSTAL, RIGHT = 0, 1, 2, 3  # the bodies' numbers in the Bell world below
RECORD = Path("examples/events/experiments/bell/bell_a_b.json")  # Bell's world of record


def a_body(nodes: range | list[int], count: int, **keys: object) -> dict:
    """A body of matter in the law's form on the chain: its Nodes with one count, at rest, the phase's denominator of the worlds of record, and its keys."""
    at = [{"node": [x, 0, 0], "count": count} for x in nodes]
    rest = {"momentum": [0, 0, 0], "momentum_before": [0, 0, 0], "phase_denominator": 1024}
    signed = {"q": 1} if "emitter" in keys or "crystal" in keys else {}  # a giver's sign
    return {"family": "matter", "nodes": at, **rest, **signed, **keys}


def bell_world(right: dict | None = None) -> dict:
    """Bell's world on a chain of 80 (x closed) in the law's form on the universe of record: the emitter of three Nodes at Bell's giving count (its declaration the world of record's, one giving aimed at the crystal's set), a polariser body of one Node at 44 with its own set `left_own` and its far set `left_far` on a far body at 40, the crystal of two Nodes at Bell's giving count with the key `crystal` and its set on its Nodes, the right polariser at 58 (its card `right` where given) with `right_own` and `right_far` on a far body at 64; the givers' modes come from the generator (`bell_simulation`)."""
    record = json.loads(RECORD.read_text(encoding="utf-8"))
    emitter, window = record["measured"][EMITTER], record["measured"][1]["nodes"][0]["count"]
    giving, count = {**emitter["emitter"], "receiver": ["crystal_set"]}, emitter["nodes"][0]["count"]
    names = (("left_own", 44), ("right_own", 58), ("left_far", 40), ("right_far", 64))
    sets = [{"name": n, "positions": [[x, 0, 0]]} for n, x in names]
    bodies = [
        a_body(
            range(5, 8), count, moment=emitter["moment"], emitter=giving, stocks={giving["family"]: 1}
        ),
        a_body([44], window, polariser={"angle": [2, 1], "sets": ["left_far", "left_own"]}),
        a_body([50, 51], count, crystal={}),
        a_body([58], window, polariser=right or {"angle": [1, 0], "sets": ["right_far", "right_own"]}),
        a_body([40], window),
        a_body([64], window),
    ]
    boundary = {"x": "closed", "y": "periodic", "z": "periodic"}
    document = {"shape": [80, 1, 1], "boundary": boundary, "ticks": 400, "N": record["N"]}
    document |= {"engine": record["engine"], "universe": record["universe"], "measured": bodies}
    document["detectors"] = [sets[0], {"name": "crystal_set", "block": CRYSTAL}, *sets[1:]]
    document["stamp"] = input_stamp(document)
    return document


def bell_simulation(document: dict, folder: Path, observer=None) -> DetectorLawSimulation:
    """The world written to `folder` with its mode file beside it from the generator (the givers' modes in the world's own well, `world_digest` the world's) and loaded as the host loads a world of record."""
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "bell_chain.json"
    path.write_text(json.dumps(document), encoding="utf-8")
    reading = generate(document)
    mode = mode_document(reading, *split_levels(reading))
    mode["world_digest"] = input_digest(document)
    path.with_suffix(".mode.json").write_text(json.dumps(mode), encoding="utf-8")
    return DetectorLawSimulation(load_world(path), observer=observer)


def test_the_card_is_built_at_ii_and_the_pair_is_declared_at_the_half_quantum():
    """The card: "the crystal" at (ii) after the step, the function `apply`, the body's key `crystal` (an empty object, declaring nothing) through the cards, no write of its own (the giving's act writes for it); `apply` declares the pair's two labels, the arriving record's twice, its norm over twice the denominator (THE HALF QUANTUM) and its clock at half the arriving rotation ([p, 2 q]); a norm or a clock below 1 is refused by name; a body with no key gives nothing."""
    assert DECLARATION.name == "the crystal" and folder_of(DECLARATION.name) == "crystal"
    assert (DECLARATION.place, DECLARATION.word, DECLARATION.writes) == ("(ii)", "after the step", ())
    registered = discover().declarations["the crystal"]
    assert registered.built and registered.function is apply
    assert registered.schema is not None and "crystal" in registered.schema.places["a body"].keys
    writes = apply(CrystalTerm(), CrystalStart(7, 3, (0, 1), (512, 1)), CrystalOwn())
    expected = (((0, 1), (0, 1)), 7, 6, (512, 2))
    assert (writes.labels, writes.norm, writes.denominator, writes.clock) == expected
    with pytest.raises(ValueError, match="clock is a pair of integers from 1"):
        apply(CrystalTerm(), CrystalStart(7, 3, (0, 1), (0, 1)), CrystalOwn())
    with pytest.raises(ValueError, match="norm is from 1"):
        apply(CrystalTerm(), CrystalStart(0, 3, (0, 1), (512, 1)), CrystalOwn())
    assert read_term({"family": "matter"}) is None and read_term({"crystal": {}}) == CrystalTerm()


def test_the_crystal_gives_the_pair_at_the_click_and_each_label_clicks_alone_at_its_side(tmp_path):
    """The loop on Bell's world in the law's form (the givers' modes from the generator, the crystal a giver with the key `crystal`), the main loop's audit admitting every act: the emitter's record clicks at the crystal's set and in the same interval the crystal gives the pair through the giving's open and window, named at the window's close (after the click, the intervals in this order and never the run's numbers) with the two identical labels, the arriving norm over twice its denominator and a residue of its own (the crystal's, read at its Node); the rows' label clicks alone at the left polariser's own set on the first row's line with the pair's one quantum, the columns' label alone at the right polariser's own set on the second row's line with the arriving record's residue (the second residue of the crystal's Node) and the content 0 (the half in the family's unit), whichever first; after the second click no row is alive. The refusals by name: a crystal on a body with an emitter, a world with one polariser body."""
    lines: list[dict] = []
    simulation = bell_simulation(bell_world(), tmp_path, lines.append)
    assert (f"measured[{CRYSTAL}].crystal", "the crystal") in simulation.family_terms()
    for _ in range(400):
        simulation.step()
    givings = [line for line in lines if line["event"] == "giving"]
    gathers = [line for line in lines if line["event"] == "gather"]
    arriving, pair = givings
    labels = [(line["measured"], line["labels"]) for line in givings]
    assert labels == [(EMITTER, [[0, 1]]), (CRYSTAL, [[0, 1], [0, 1]])]
    assert (pair["norm"], pair["pace"]) == (arriving["norm"], 2 * arriving["pace"])
    assert pair["u"] != arriving["u"]  # the crystal's own residue, read at its Node
    chosen = [(g["record"], g["chosen"][0][0], g["u"], g["content"]) for g in gathers]
    assert chosen[0] == (arriving["record"], "crystal_set", arriving["u"], 1) and len(chosen) == 3
    # the two labels' clicks in either order (whichever first)
    assert {chosen[1], chosen[2]} == {
        (pair["record"], "left_own", pair["u"], 1),
        (pair["record"] + 1, "right_own", arriving["u"], 0),
    }
    ticks = [arriving["tick"], gathers[0]["tick"], pair["tick"], gathers[1]["tick"], gathers[2]["tick"]]
    assert ticks == sorted(ticks) and ticks[0] < ticks[1] < ticks[2] < ticks[3]  # the order alone
    assert not [live for live in simulation.records.values() if live.pair_record is not None]
    simulation.crystals = {EMITTER: CrystalTerm()}
    with pytest.raises(ValueError, match="declares nothing else"):
        simulation.family_terms()
    one_sided = bell_world()
    del one_sided["measured"][RIGHT]["polariser"]
    one_sided["stamp"] = input_stamp(one_sided)
    with pytest.raises(ValueError, match="needs two polariser bodies"):
        bell_simulation(one_sided, tmp_path / "one_sided")
