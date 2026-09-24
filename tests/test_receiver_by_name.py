"""The receiver by name and the click line at the rung (`detector-law-v1`,
DECLARATIONS.md section 13 item 7 and section 10 items 9 and 10; BUILD.md section 21;
Nature24's eight decisions of 2026-09-24, 12:40Z, through the Boss). On a chain of 200 with
one emitting block and one named set 60 Links away at wheel 64: (a) exactly one gather line
per record at the set's first rung, its time the rung's interval; (b) the block's own pointer
0 at every age; (c) the loader refuses the same world without `receiver`; (d) the permutation
test, the detector list reordered giving byte-identical gather lines (issue #1116); (e) a
set beside the receiver receives no pointer and its take appears in `escaped` (HOST). Then
the line's time against the train and the close without a click, and the registered world
`sagnac_rest.json` loaded and stepped, each block's click read on the other's record. Every
number here is DETECTOR (a click line) or GAMEBOARD (a row's level, a pointer), named so; no
pin world is run to prove the line and no pin is read."""

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
    [800, 800], the seed 50 x 2^20, G = [1, 50], g = [1, 1000], W 64, `emits` light, its
    `receiver` where one is named."""
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


def body(x: int) -> dict:
    """A receiver body of light at x (a measured event, one Node), read as a set by name."""
    return {
        "position": [x, 0, 0],
        "family": "light",
        "amount": 1,
        "phase": 0,
        "momentum": [0, 0, 0],
        "fixed": True,
        "directions": [[-1, 0, 0]],
    }


def chain_of_200(receiver: str | None = "screen") -> dict:
    """The declaration's test world: a chain of 200 (x open, the sponges), light's clock
    [1, 1], the emitting block A at [20, 32) with own_grace 70 naming `screen`, the set
    `screen` on the body at x = 91 (60 Links from A's face at 31) at wheel 64, and the set
    `beside` on the body at x = 8 behind A at wheel 64 (a sink); the world's wheel 64."""
    document = massive_world([200, 1, 1], CHAIN, [800, 809], faces={"x": "open"})
    document["families"][0]["phase_per_link"] = [1, 1]
    document["ticks"] = 500
    document["clock_stamp"] = True
    document["wheel"] = 64
    document["measured"] = [emitter(20, receiver, 70), body(91), body(8)]
    document["detectors"] = [
        {"name": "screen", "positions": [[91, 0, 0]], "wheel": 64},
        {"name": "beside", "positions": [[8, 0, 0]], "wheel": 64},
    ]
    return document


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


def test_a_one_line_per_record_at_the_receivers_first_rung_the_permutation_and_the_sinks():
    """(a) On the chain of 200 every record A emits writes EXACTLY ONE gather line, at
    `screen`'s first rung (`click_at` rung, `chosen` screen, `tick` the rung's interval equal
    to `click`), more than 60 intervals after its birth (the transit of 60 Links at a pace
    below one Link per interval), the ladder the one cell (`cells` screen alone), the
    definition and `receiver_cell` carrying the name; (d) the detector list reversed gives
    byte-identical gather lines (issue #1116: the list's order is no input); (e) `beside` and
    the faces are sinks: their pointers 0 on every record at every interval, their take on
    the record's HOST `escaped` (above 0 on the records `beside` reached), inside `absorbed`;
    the books balanced, the HOST count `closed_after_click` and the readings `clicked` and
    `escaped` on this world alone (a world without an emitter carries none). The edge case
    (c): the same world without `receiver` is refused naming the key; `receiver` on a block
    that emits nothing, a name no set declares (the names listed) and a value that is no
    string are refused."""
    world = parse_nature_beam_world(chain_of_200())
    assert world.measured[0].block is not None and world.measured[0].block.receiver == "screen"
    dumps: list[list[str]] = []
    for reversed_sets in (False, True):
        document = chain_of_200()
        if reversed_sets:
            document["detectors"] = list(reversed(document["detectors"]))
        simulation, lines = run(document, 500)
        screen = simulation.cell_names.index("screen")
        beside = simulation.cell_names.index("beside")
        assert simulation.receiver_cell == {0: screen} and simulation.has_receiver
        found = gathers(lines)
        assert len(found) >= 4, found
        assert len({g["record"] for g in found}) == len(found)  # one line per record
        for line in found:
            assert line["chosen"] == [["screen", 0, "0"]] and line["click_at"] == "rung"
            assert line["tick"] == line["click"] and line["click"] - line["birth"] > 60  # DETECTOR
            assert line["cells"] == [[[["screen", 0, "0"]], 64]] and line["content"] == 0
            assert "escaped" in line and line["clock_source"] == "interval"
        reached_beside = 0
        for live in simulation.records.values():
            if live.family != 0:
                continue
            # GAMEBOARD: the sinks on no pointer; the receiver's pointer the only one
            assert live.pointers[beside] == 0 and all(
                live.pointers[cell] == 0 for cell in range(len(simulation.cell_names)) if cell != screen
            )
            assert live.absorbed == live.pointers[screen] + live.escaped
            reached_beside += int(live.escaped > 0)
            if live.clicked:
                assert live.content == 0
        assert reached_beside >= 2
        transit = simulation.books()["families"]["light"]["transit"]
        assert transit["closed_after_click"] >= 1 and transit["escaped"] == 0
        state = dict(simulation.snapshot_stream())
        assert all("clicked" in entry and "escaped" in entry for entry in state["records"])
        dumps.append([json.dumps(g, sort_keys=False) for g in found])
    assert dumps[0] == dumps[1]
    # a world with no emitter carries neither reading (a lamp world's books byte for byte)
    plain = light_clock_world("open", True)
    for key in ("emits", "own_grace", "receiver"):
        plain["measured"][0].pop(key)
    simulation, _ = run(plain, 10)
    assert not simulation.has_receiver
    assert "closed_after_click" not in simulation.books()["families"]["light"]["transit"]
    assert all("clicked" not in entry for entry in dict(simulation.snapshot_stream())["records"])
    # (c) the refusals
    with pytest.raises(ValueError, match=r"measured\[0\] emits 'light' and declares no `receiver`"):
        parse_nature_beam_world(chain_of_200(None))
    silent = chain_of_200()
    silent["measured"][0].pop("emits")
    silent["measured"][0].pop("own_grace")
    with pytest.raises(
        ValueError, match=r"measured\[0\]\.receiver is refused on a block that emits nothing"
    ):
        parse_nature_beam_world(silent)
    unknown = chain_of_200("nowhere")
    with pytest.raises(
        ValueError, match=r"'nowhere' names no declared detector set.*'screen', 'beside'"
    ):
        parse_nature_beam_world(unknown)
    number = chain_of_200()
    number["measured"][0]["receiver"] = 3
    with pytest.raises(
        ValueError, match=r"measured\[0\]\.receiver must be the name of a declared detector set"
    ):
        parse_nature_beam_world(number)


def test_b_the_blocks_own_pointer_is_0_at_every_age():
    """(b) On the chain of 200 the block's own cell (`measured:0`) holds a pointer of 0 on
    every record it emits at every interval (no self-share after own_grace: its own take on
    no pointer, item 10 at T = 0 as merged), while `screen` clicks. The edge case: a block
    naming the set that IS its own cells (the sagnac form) on the chain of 600, own_grace 70,
    at rest and pushed at k = 3 ([64, 0, 0], the hops onto its own records' remnants) over
    700 intervals: every own record's pointers are 0 at every cell at every interval, no
    record is clicked and no line is written, the row nonzero at the cells while the block
    sources it (line B) and 0 at the current cells from the first interval after the train,
    the books balanced."""
    simulation, lines = run(chain_of_200(), 400)
    block = simulation.blocks[0]
    own_cell = block.cell
    assert simulation.cell_names[own_cell] == "measured:0"
    assert gathers(lines)
    lines.clear()
    simulation.step()
    for live in simulation.records.values():
        if live.family == 0:
            assert live.pointers[own_cell] == 0 and live.first_rung[own_cell] is None
    for momentum in (0, 64):
        document = massive_world([600, 1, 1], CHAIN, [800, 809], faces={"x": "open"})
        document["ticks"] = 700
        document["clock_stamp"] = True
        document["wheel"] = 64
        document["measured"] = [emitter(200, "at_a", 70, momentum)]
        document["detectors"] = [{"name": "at_a", "block": 0, "wheel": 256}]
        lines = []
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
        assert not gathers(lines)
        assert block.stepped > 100 if momentum else block.stepped == 0


def test_c_the_lines_time_against_the_train_and_the_close_without_a_click():
    """The line's time: on the light clock's chain of 173 with the faces CLOSED and A naming
    its own bound set `A_face` (x = 112, W 64), the first record's line is written at the
    rung's interval (`tick` equal to `click`), after the grace of 140 (the set free during
    it), stamped with A's count (clock_source measured:0); the record lives on after its line
    (`clicked`, content 0, its rows on the board) with no second line within 600 intervals.
    A rung crossed INSIDE the train (two blocks one Link apart naming each other's sets,
    own_grace 3000, W 256) writes its line at the first interval after the train (`click`
    below `tick`, `tick` the birth plus the train), never while the block sources it. The
    edge case: a receiver that crosses no rung (A naming the set at its own cells on the
    open chain of 173) closes with NO line, the content rows `escaped` and `taken_by_emitter`
    0 (a block's record is born at content 0), `closed_after_click` 0, the books balanced."""
    document = light_clock_world("closed", False)
    document["measured"][0]["receiver"] = "A_face"
    simulation, lines = run(document, 600)
    a_face = simulation.cell_names.index("A_face")
    first = 1
    found = [g for g in gathers(lines) if g["record"] == first]
    assert len(found) == 1, found
    line = found[0]
    assert line["click_at"] == "rung" and line["tick"] == line["click"]
    assert line["chosen"] == [["A_face", 0, "0"]] and line["clock_source"] == "measured:0"
    assert line["click"] - line["birth"] > 140  # DETECTOR: after the grace of train + own_grace
    live = simulation.records[first]
    assert live.clicked and live.content == 0 and live.first_rung[a_face] == line["click"]
    assert np.any(live.now)  # GAMEBOARD: the rows still on the board after the line
    # the rung inside the train
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
        live = simulation.records[line["record"]]
        assert live.clicked and line["tick"] >= line["birth"] + live.train
        if line["click"] < line["tick"]:
            inside += 1
            assert line["tick"] == line["birth"] + live.train
    assert inside >= 1, gathers(lines)
    # the close without a click: no line
    document = light_clock_world("open", False)
    document["detectors"] = [{"name": "at_a", "block": 0, "wheel": 64}]
    document["measured"][0]["receiver"] = "at_a"
    simulation, lines = run(document, 500)
    assert not gathers(lines)
    # the block's own massive record lives among the records: count light's alone
    closed = simulation.layer.born - sum(1 for live in simulation.records.values() if live.family == 0)
    assert closed >= 1
    transit = simulation.books()["families"]["light"]["transit"]
    assert transit["escaped"] == 0 and transit["taken_by_emitter"] == 0
    assert transit["closed_after_click"] == 0 and transit["balanced"]


def test_d_sagnac_rest_loads_and_steps_and_reads_each_blocks_click_on_the_others_record():
    """The registered world `examples/events/massive_record/sagnac_rest.json` (the two
    blocks at [700, 712) and [772, 784) at rest, own_grace 3000, A `receiver` at_b and B
    at_a, the sets at the blocks' cells at W 256) loads and is stepped 300 intervals as a
    load-and-step diagnostic (no pin): each block's own click lines on its own massive record
    (its clock) number at least three; every gather line is B's record's click at `at_a` or
    A's at `at_b`, at the set's first rung (`tick` equal to `click`, click_at rung), more
    than 60 intervals after the birth (the transit of L = 60 Links; the interval itself is
    the pin run's reading, not read here), stamped with the receiving block's count, the
    records living on with content 0, both directions the same interval at rest, the books
    balanced. The edge case: the file on disk is byte for byte what the test read."""
    before = SAGNAC_REST.read_bytes()
    document = json.loads(before)
    world = parse_nature_beam_world(document)
    assert [entry.block.receiver for entry in world.measured if entry.block is not None] == [
        "at_b",
        "at_a",
    ]
    simulation, lines = run(copy.deepcopy(document), 300, every=100)
    for block in simulation.blocks:
        own = [
            line
            for line in lines
            if line["event"] == "click"
            and line["measured"] == block.number
            and line["record"] == block.own.identity
        ]
        assert len(own) >= 3 and own[-1]["clock"] == block.count, own
    found = gathers(lines)
    assert len(found) >= 2, found
    by_birth: dict[int, list[dict]] = {}
    for line in found:
        emitter_number = line["record"] >> 32
        other = 1 - emitter_number
        assert line["chosen"] == [[("at_b", "at_a")[emitter_number], 0, "0"]]
        assert line["click_at"] == "rung" and line["tick"] == line["click"]
        assert line["clock_source"] == f"measured:{other}"
        assert line["click"] - line["birth"] > 60  # DETECTOR: after the transit of 60 Links
        live = simulation.records[line["record"]]
        assert live.clicked and live.content == 0
        by_birth.setdefault(line["birth"], []).append(line)
    for pair in by_birth.values():
        assert len(pair) == 2 and pair[0]["click"] == pair[1]["click"]
    assert SAGNAC_REST.read_bytes() == before
