"""The receiver by name and the click line at the rung (`detector-law-v1`,
DECLARATIONS.md section 13 item 7 and section 10 item 9; BUILD.md section 19): (a) the
world key `receiver` on an emitting block names the detector set whose one cell is the
ladder of every record the block emits, the faces and every other set sinks for it; (b) the
gather line is written at the receiver's first rung after the record's train (`tick` the
line's interval, `click` the rung), the record living on with content 0 and closing with no
second line; (c) the emitter's own cells take on no pointer at every age in the receiver
form (item 10, the hop fix of PR 1115 read through the key); (d) the registered world
`sagnac_rest.json` loads as it is (no key: the ladder every cell, as before) and, keyed in
memory as section 13 item 7 names it, reads each block's click on the other's record at
the rung. Every number here is DETECTOR (a click line) or GAMEBOARD (a row's level, a
pointer), named so; no pin is read."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import numpy as np
import pytest

from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.events.world import parse_nature_beam_world
from tests.test_massive_record import CHAIN, light_clock_world, massive_world

SAGNAC_REST = Path(__file__).resolve().parents[1] / "examples/events/massive_record/sagnac_rest.json"


def emitter(position: int, receiver: str | None, own_grace: int, momentum: int = 0) -> dict:
    """An emitting block of side 12 at `position` on the matter kind [800, 809]: the well
    [800, 800], the seed 50 x 2^20, G = [1, 50], g = [1, 1000], W 64, `emits` light."""
    block = {
        "position": [position, 0, 0],
        "family": "matter",
        "amount": 1,
        "phase": 0,
        "momentum": [momentum, 0, 0],
        "fixed": True,
        "side": 12,
        "pair": [800, 800],
        "seed": 50 << 20,
        "coupling": {"G": [1, 50], "g": [1, 1000]},
        "wheel": 64,
        "emits": "light",
        "own_grace": own_grace,
        "margin": "control",
    }
    if receiver is not None:
        block["receiver"] = receiver
    return block


def run(document: dict, ticks: int, every: int = 50) -> tuple[DetectorLawSimulation, list[dict]]:
    """The world stepped `ticks` intervals with the books read every `every` intervals and at
    the end; the lines written are returned with the simulation."""
    lines: list[dict] = []
    simulation = DetectorLawSimulation(parse_nature_beam_world(document), observer=lines.append)
    for _ in range(ticks):
        simulation.step()
        if simulation.tick % every == 0:
            assert simulation.books()["balanced"], simulation.tick
    assert simulation.books()["balanced"], simulation.tick
    return simulation, lines


def gathers(lines: list[dict]) -> list[dict]:
    return [line for line in lines if line["event"] == "gather"]


def test_a_the_receiver_by_name_is_the_one_cell_of_the_blocks_ladder():
    """(a) The key `receiver` on an emitting block (the light clock's chain of 173, open faces,
    A at [100, 112) with own_grace 70, the sets `A_face` at x = 112 and `far` on the body at
    x = 160, both at W 64): A naming `far` makes `far` the one cell of every record's ladder:
    every gather line chooses `far` at its first rung (click_at rung), `A_face` and the two
    faces are SINKS for A's records (their pointers 0 on every record at every interval,
    their take in `absorbed` alone, `absorbed` above the receiver's pointer), the books
    balanced; the loader carries the name on the definition and the engine on `receiver_cell`;
    the state reading carries `clicked` and the books `closed_after_click` on this world alone.
    The permutation: the detector list reversed gives the same lines by name (record, birth,
    tick, click, chosen, clock). The edge cases: `receiver` on a block that emits nothing is
    refused, a name no set declares is refused listing the declared names, a value that is no
    string is refused."""
    document = light_clock_world("open", True)
    document["measured"][0]["receiver"] = "far"
    world = parse_nature_beam_world(document)
    assert world.measured[0].block is not None and world.measured[0].block.receiver == "far"
    by_order: list[list[tuple]] = []
    for reversed_sets in (False, True):
        trial = copy.deepcopy(document)
        if reversed_sets:
            trial["detectors"] = list(reversed(trial["detectors"]))
        simulation, lines = run(trial, 500)
        far = simulation.cell_names.index("far")
        a_face = simulation.cell_names.index("A_face")
        assert simulation.receiver_cell == {0: far} and simulation.has_receiver
        found = gathers(lines)
        assert len(found) >= 3, found
        sinks_took = 0
        for line in found:
            assert line["chosen"][0][0] == "far" and line["click_at"] == "rung"
            assert line["cells"] == [[[["far", 0, "0"]], 64]]
        for live in simulation.records.values():
            if live.family != 0:
                continue
            # GAMEBOARD: the sinks' pointers 0; the receiver's the only one
            assert live.pointers[a_face] == 0
            assert all(
                live.pointers[cell] == 0 for cell in range(len(simulation.cell_names)) if cell != far
            )
            if live.clicked:
                # `absorbed` carries the sinks' take beside the receiver's pointer
                assert live.content == 0 and live.absorbed >= live.pointers[far] > 0
                sinks_took += int(live.absorbed > live.pointers[far])
        assert sinks_took >= 1
        books = simulation.books()["families"]["light"]["transit"]
        assert "closed_after_click" in books and books["closed_after_click"] >= 1
        state = dict(simulation.snapshot_stream())
        assert all("clicked" in entry for entry in state["records"])
        by_order.append(
            [
                (g["record"], g["birth"], g["tick"], g["click"], g["chosen"][0][0], g["clock"], g["T"])
                for g in found
            ]
        )
    assert by_order[0] == by_order[1]
    # a world without the key carries neither reading (a lamp world's books byte for byte)
    plain = light_clock_world("open", True)
    simulation, _ = run(plain, 10)
    assert not simulation.has_receiver
    assert "closed_after_click" not in simulation.books()["families"]["light"]["transit"]
    assert all("clicked" not in entry for entry in dict(simulation.snapshot_stream())["records"])
    # the refusals
    silent = light_clock_world("open", True)
    silent["measured"][0].pop("emits")
    silent["measured"][0].pop("own_grace")
    silent["measured"][0]["receiver"] = "far"
    with pytest.raises(
        ValueError, match=r"measured\[0\]\.receiver is refused on a block that emits nothing"
    ):
        parse_nature_beam_world(silent)
    unknown = light_clock_world("open", True)
    unknown["measured"][0]["receiver"] = "nowhere"
    with pytest.raises(ValueError, match=r"'nowhere' names no declared detector set.*'A_face', 'far'"):
        parse_nature_beam_world(unknown)
    number = light_clock_world("open", True)
    number["measured"][0]["receiver"] = 3
    with pytest.raises(
        ValueError, match=r"measured\[0\]\.receiver must be the name of a declared detector set"
    ):
        parse_nature_beam_world(number)


def test_b_the_click_line_at_the_rung_for_a_one_cell_ladder():
    """(b) The light clock's chain of 173 with the faces CLOSED, A naming its own bound set
    `A_face` (the free Node at x = 112, W 64): the first record's line is written at the
    interval of `A_face`'s first rung (`tick` equal to `click`, click_at rung), after the
    record's grace of 140 (the set free during it: no rung before), stamped with A's own
    count (clock_source measured:0); the record lives on after its line (`clicked`, its
    content 0, its rows still on the board) and no second line is written for it within 600
    intervals; on the open chain with the body `far` as the receiver, records close after
    their line with no second line, counted on the books' HOST row `closed_after_click`, one
    gather line per record. The edge case: two blocks one Link apart naming each other's
    sets (A at [100, 112) and B at [113, 125), own_grace 3000, the sets at W 256): a rung
    crossed INSIDE the record's train writes its line at the first interval after the train
    (Reviewer 3's precondition: `click` the rung, `tick` the birth plus the train), never
    while the block sources it."""
    document = light_clock_world("closed", False)
    document["measured"][0]["receiver"] = "A_face"
    simulation, lines = run(document, 600)
    a_face = simulation.cell_names.index("A_face")
    first = 1
    found = [g for g in gathers(lines) if g["record"] == first]
    assert len(found) == 1, found
    line = found[0]
    assert line["click_at"] == "rung" and line["tick"] == line["click"]
    assert line["chosen"][0][0] == "A_face" and line["clock_source"] == "measured:0"
    assert line["click"] - line["birth"] > 140  # DETECTOR: after the grace of train + own_grace
    assert line["content"] == 0 and line["taken_by_emitter"] == 0
    live = simulation.records[first]
    assert live.clicked and live.content == 0 and live.first_rung[a_face] == line["click"]
    assert np.any(live.now)  # GAMEBOARD: the rows still on the board after the line
    assert sum(1 for g in gathers(lines) if g["record"] == first) == 1
    # the close after the line: no second line, the HOST count
    document = light_clock_world("open", True)
    document["measured"][0]["receiver"] = "far"
    simulation, lines = run(document, 600)
    records = [g["record"] for g in gathers(lines)]
    assert len(records) == len(set(records)) >= 3
    closed = simulation.books()["families"]["light"]["transit"]["closed_after_click"]
    assert closed >= 1
    open_clicked = [live for live in simulation.records.values() if live.family == 0 and live.clicked]
    assert closed + len(open_clicked) == len(records)
    # the edge case: the rung inside the train
    document = massive_world([400, 1, 1], CHAIN, [800, 809], faces={"x": "open"})
    document["families"][0]["phase_per_link"] = [1, 1]
    document["ticks"] = 400
    document["clock_stamp"] = True
    document["wheel"] = 64
    document["measured"] = [emitter(100, "at_b", 3000), emitter(113, "at_a", 3000)]
    document["detectors"] = [
        {"name": "at_a", "block": 0, "wheel": 256},
        {"name": "at_b", "block": 1, "wheel": 256},
    ]
    simulation, lines = run(document, 400)
    inside = 0
    for line in gathers(lines):
        assert line["click_at"] == "rung" and line["click"] <= line["tick"]
        live = simulation.records.get(line["record"])
        assert live is not None and live.clicked
        assert line["tick"] >= line["birth"] + live.train
        if line["click"] < line["tick"]:
            inside += 1
            assert line["tick"] == line["birth"] + live.train
    assert inside >= 1, gathers(lines)


def test_c_the_emitters_own_cells_take_on_no_pointer_at_every_age_in_the_receiver_form():
    """(c) An emitting block whose receiver is the set that IS its own cells (`at_a` without
    positions, the sagnac form) on the chain of 600, own_grace 70, at rest and pushed at k = 3
    ([64, 0, 0]) over 700 intervals: every own record's pointers are 0 at every cell at every
    interval (the own take on no pointer, item 10, at every age: during the train the cells
    insert and the row is nonzero there, from the first interval after the train the row at
    the current cells is 0 and the block's hops book nothing), no record's line is ever
    written at a rung (`clicked` false on every record, no gather line with a chosen cell),
    the books balanced. The edge case: on the open chain of 173 a record whose receiver
    crosses no rung completes with NO click (its line with `chosen` null, click_at
    completion, `taken_by_emitter` 0 as its content is 0), `closed_after_click` 0."""
    for momentum in (0, 64):
        document = massive_world([600, 1, 1], CHAIN, [800, 809], faces={"x": "open"})
        document["ticks"] = 700
        document["clock_stamp"] = True
        document["wheel"] = 64
        document["measured"] = [emitter(200, "at_a", 70, momentum)]
        document["detectors"] = [{"name": "at_a", "block": 0, "wheel": 256}]
        lines: list[dict] = []
        simulation = DetectorLawSimulation(parse_nature_beam_world(document), observer=lines.append)
        block = simulation.blocks[0]
        assert simulation.receiver_cell == {0: simulation.cell_names.index("at_a")}
        sourcing_seen = taken_seen = 0
        for _ in range(700):
            simulation.step()
            if simulation.tick % 50 == 0:
                assert simulation.books()["balanced"], simulation.tick
            for live in simulation.records.values():
                if live.family != 0:
                    continue
                assert not any(live.pointers) and not live.clicked, (simulation.tick, live.identity)
                if live.sourcing:
                    sourcing_seen += int(np.any(live.now[block.mask]))
                elif live.age >= live.train:
                    taken_seen += 1
                    assert not np.any(live.now[block.mask]), (simulation.tick, live.identity)
        assert sourcing_seen > 50 and taken_seen > 300
        assert not [g for g in gathers(lines) if g["chosen"] is not None]
        assert block.stepped > 100 if momentum else block.stepped == 0
    # the edge case: the close with no click
    document = light_clock_world("open", False)
    document["detectors"] = [{"name": "at_a", "block": 0, "wheel": 64}]
    document["measured"][0]["receiver"] = "at_a"
    simulation, lines = run(document, 500)
    found = gathers(lines)
    assert len(found) >= 1, found
    for line in found:
        assert line["chosen"] is None and line["click_at"] == "completion"
        assert line["taken_by_emitter"] == 0 and line["content"] == 0 and line["cells"] == []
        assert line["record"] not in simulation.records
    transit = simulation.books()["families"]["light"]["transit"]
    assert transit["closed_after_click"] == 0 and transit["balanced"]


def test_d_sagnac_rest_loads_as_it_is_and_keyed_reads_each_blocks_click_on_the_others_record():
    """(d) The registered world `examples/events/massive_record/sagnac_rest.json` (the two
    blocks at [700, 712) and [772, 784) at rest, own_grace 3000, the sets `at_a` and `at_b`
    at the blocks' cells at W 256; the file byte for byte, no key) loads with no receiver on
    either block; stepped 300 intervals each block's own click lines (its clock's count on
    its own massive record, DETECTOR) number at least three, B's first record crosses `at_a`'s
    first rung and yet no gather line is written (the ladder every cell, the line at the
    close, as before the key). Keyed in memory as DECLARATIONS.md section 13 item 7 names
    it (A `receiver` at_b, B at_a) and stepped 420 intervals: every gather line is written
    at the other block's set at its first rung (`tick` equal to `click`, click_at rung), more
    than 60 intervals after the birth (the front's transit of L = 60 Links at a pace below
    one Link per interval; the interval itself is the pin run's reading, not read here),
    stamped with the receiving block's count (clock_source), the records living on with
    content 0, both directions the same interval at rest, the books balanced. The edge case:
    the file on disk is unchanged by the keyed run."""
    before = SAGNAC_REST.read_bytes()
    document = json.loads(before)
    world = parse_nature_beam_world(document)
    assert all(entry.block is not None and entry.block.receiver is None for entry in world.measured)
    simulation, lines = run(copy.deepcopy(document), 300, every=100)
    assert not simulation.has_receiver
    for block in simulation.blocks:
        own = [
            line
            for line in lines
            if line["event"] == "click"
            and line["measured"] == block.number
            and line["record"] == block.own.identity
        ]
        assert len(own) >= 3 and own[-1]["clock"] == block.count, own
    at_a = simulation.cell_names.index("at_a")
    b_first = simulation.records[1 * (1 << 32) + 1]
    assert b_first.first_rung[at_a] is not None and not gathers(lines)
    keyed = copy.deepcopy(document)
    keyed["measured"][0]["receiver"] = "at_b"
    keyed["measured"][1]["receiver"] = "at_a"
    simulation, lines = run(keyed, 420, every=100)
    found = gathers(lines)
    assert len(found) >= 4, found
    by_birth: dict[int, list[dict]] = {}
    for line in found:
        emitter_number = line["record"] >> 32
        other = 1 - emitter_number
        assert line["chosen"][0][0] == ("at_b", "at_a")[emitter_number]
        assert line["click_at"] == "rung" and line["tick"] == line["click"]
        assert line["clock_source"] == f"measured:{other}"
        assert line["click"] - line["birth"] > 60  # DETECTOR: after the transit of 60 Links
        live = simulation.records[line["record"]]
        assert live.clicked and live.content == 0
        by_birth.setdefault(line["birth"], []).append(line)
    for pair in by_birth.values():
        assert len(pair) == 2 and pair[0]["click"] == pair[1]["click"]
    assert simulation.books()["families"]["light"]["transit"]["closed_after_click"] == 0
    assert SAGNAC_REST.read_bytes() == before
