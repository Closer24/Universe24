"""The receiver by name and the click line at the rung (`detector-law-v1`,
DECLARATIONS.md section 13 item 7 and section 10 items 9 and 10; BUILD.md section 21;
Nature24's eight decisions of 2026-09-24, 12:40Z, through the Boss). On a chain of 200 with
one emitter body and one named set 60 Links away at wheel 64: (a) exactly one gather line
per record at the set's first rung, its time the rung's interval; (b) the block's own pointer
0 at every age; (c) the loader's refusals of `receiver`; (d) the permutation test, the
detector list reordered giving byte-identical gather lines (issue #1116); (e) a set beside
the receiver receives no pointer and its take appears in `escaped` (HOST). Then the line's
time and the close without a click, and the registered world `sagnac_rest.json` loaded and
stepped. SINCE THE EMITTER AS A CLICKING BODY (BUILD.md section 26) the emitter is a body
with its `emitter` on a wheel and its stock, seeded on its mode, its cells cells like every
other (no grace, no exemption, no own take); every number here is the engine's reading on
that head (COMPUTATION, a click line or a row's level), named so; no pin world is run to
prove the line and no pin is read."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import numpy as np
import pytest

from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.events.world import parse_nature_beam_world
from tests.test_massive_record import CHAIN, light_clock_world, massive_world, seed_source

SAGNAC_REST = Path(__file__).resolve().parents[1] / "examples/events/massive_record/sagnac_rest.json"


def emitter(position: int, receiver: str | None, momentum: int = 0, stock: int = 4) -> dict:
    """An emitter body of side 12 at `position` on the matter kind [800, 809]: the well
    [800, 800], the seed 50 x 2^20 (its profile on the mode by `seed_source` once the world
    is built), W 64, its `emitter` of light on the wheel [1, 64] with the stock `stock`, its
    `receiver` where one is named (the line at that set's rung)."""
    block = {
        "position": [position, 0, 0],
        "family": "matter",
        "amount": stock,
        "phase": 0,
        "momentum": [momentum, 0, 0],
        "fixed": True,
        "side": 12,
        "pair": [800, 800],
        "seed": 50 << 20,
        "wheel": 64,
        "emitter": {"family": "light", "wheel": [1, 64], "residue_order": "ordinal"},
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
    [1, 1], the emitter body A at [20, 32) naming `screen` (four births), the set `screen`
    on the body at x = 91 (60 Links from A's face at 31) at wheel 64, and the set `beside`
    on the body at x = 8 behind A at wheel 64 (a sink); the world's wheel 64."""
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
    seed_source(document, 0)
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
    below one Link per interval), the ladder the one cell (`cells` screen alone), the line
    carrying the quantum (`content` 1, the record's content 0 after it), the definition and
    `receiver_cell` carrying the name; (d) the detector list reversed gives byte-identical
    gather lines (issue #1116: the list's order is no input); (e) `beside` and the faces are
    sinks: their pointers 0 on every record at every interval, their take on the record's
    HOST `escaped` (above 0 on every line, the -x half reaching `beside` first), inside `absorbed`; the books
    balanced, the HOST count `closed_after_click` and the readings `clicked` and `escaped`
    on this world alone (a world without an emitter carries none). The edge case (c): the
    same world without `receiver` loads (the born records' ladder every cell, the line at
    completion); `receiver` on a block that emits nothing, a name no set declares (the names
    listed) and a value that is no string are refused."""
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
        assert len(found) >= 3, found
        assert len({g["record"] for g in found}) == len(found)  # one line per record
        for line in found:
            assert line["chosen"] == [["screen", 0, "0"]] and line["click_at"] == "rung"
            assert line["tick"] == line["click"] and line["click"] - line["birth"] > 60
            assert line["cells"] == [[[["screen", 0, "0"]], 64]] and line["content"] == 1
            assert "escaped" in line and line["clock_source"] == "interval"
        for live in simulation.records.values():
            if live.family != 0:
                continue
            # GAMEBOARD: the sinks on no pointer; the receiver's pointer the only one
            assert live.pointers[beside] == 0 and all(
                live.pointers[cell] == 0 for cell in range(len(simulation.cell_names)) if cell != screen
            )
            assert live.absorbed == live.pointers[screen] + live.escaped
            if live.clicked:
                assert live.content == 0
        # the -x half reaches `beside` twelve Links behind A before the line at the rung
        assert all(line["escaped"] > 0 for line in found)
        transit = simulation.books()["families"]["light"]["transit"]
        assert transit["closed_after_click"] >= 1
        state = dict(simulation.snapshot_stream())
        assert all("clicked" in entry and "escaped" in entry for entry in state["records"])
        dumps.append([json.dumps(g, sort_keys=False) for g in found])
    assert dumps[0] == dumps[1]
    # a world with no emitter carries neither reading
    plain = light_clock_world("open", True)
    for key in ("emitter", "receiver"):
        plain["measured"][0].pop(key)
    simulation, _ = run(plain, 10)
    assert not simulation.has_receiver
    assert "closed_after_click" not in simulation.books()["families"]["light"]["transit"]
    assert all("clicked" not in entry for entry in dict(simulation.snapshot_stream())["records"])
    # (c) without `receiver` the ladder is every cell
    unnamed = parse_nature_beam_world(chain_of_200(None))
    assert unnamed.measured[0].block is not None and unnamed.measured[0].block.receiver is None
    assert not DetectorLawSimulation(unnamed).has_receiver
    silent = chain_of_200()
    silent["measured"][0].pop("emitter")
    with pytest.raises(
        ValueError, match=r"measured\[0\]\.receiver is refused on a block that emits nothing"
    ):
        parse_nature_beam_world(silent)
    unknown = chain_of_200()
    unknown["measured"][0]["receiver"] = "nowhere"
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
    every record it emits at every interval (a body answers no record of its own, and its
    cells are no take Nodes in the positions form), while `screen` clicks. The edge case: a
    block naming the set that IS its own cells (the sagnac form) on the chain of 600, at rest
    and pushed at k = 3 ([64, 0, 0]) over 700 intervals: the set reads the write itself
    (BUILD.md section 26 item 10, the self-click): every own record's line at the birth's
    next interval chosen at the set, the record then closed after its click, the four of
    the stock counted on `closed_after_click`, the rows 0 at the cells, the books balanced."""
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
        document["measured"] = [emitter(200, "at_a", momentum)]
        document["detectors"] = [{"name": "at_a", "block": 0, "wheel": 256}]
        seed_source(document, 0)
        lines = []
        simulation = DetectorLawSimulation(parse_nature_beam_world(document), observer=lines.append)
        block = simulation.blocks[0]
        assert simulation.receiver_cell == {0: simulation.cell_names.index("at_a")}
        for _ in range(700):
            simulation.step()
            if simulation.tick % 50 == 0:
                assert simulation.books()["balanced"], simulation.tick
            for live in simulation.records.values():
                if live.family == 0 and live.age > 0:
                    assert not np.any(live.now[block.mask]), (simulation.tick, live.identity)
        found = gathers(lines)
        assert len(found) == 4 and all(g["chosen"] == [["at_a", 0, "0"]] for g in found)
        assert all(g["click"] == g["birth"] + 1 and g["tick"] == g["click"] for g in found)
        assert simulation.books()["families"]["light"]["transit"]["closed_after_click"] == 4
        assert block.stepped > 50 if momentum else block.stepped == 0


def test_c_the_lines_time_and_the_close_without_a_click():
    """The line's time: on the light clock's chain of 173 with the faces CLOSED and A naming
    its own bound set `A_face` (x = 112, W 64), the first record's line is written at the
    rung's interval (`tick` equal to `click`), within ten intervals of the birth (the set
    beside A's cells takes from the first interval, BUILD.md section 26 item 9), stamped
    with A's count (clock_source measured:0); the record lives on after its line (`clicked`,
    content 0, its rows on the board) with no second line within 300 intervals (it closes
    after its click at 415, section 26 item 9). Two emitter
    bodies one Link apart naming the set on the one free Node between them (bound to the
    first, W 256): both bodies' records write their lines there at a rung with `tick` equal
    to `click`, stamped with the bound body's count. The edge case: a receiver that crosses
    no rung (A naming a set on a body behind it at x = 5 on the open chain of 173 whose wheel
    is 1, the rung the whole norm, which the half arriving there cannot reach) closes with
    NO line, its content on the transit row
    `escaped` and `taken_by_emitter` 0, `closed_after_click` 0, the books balanced."""
    document = light_clock_world("closed", False)
    document["measured"][0]["receiver"] = "A_face"
    simulation, lines = run(document, 300)
    a_face = simulation.cell_names.index("A_face")
    first = 1
    found = [g for g in gathers(lines) if g["record"] == first]
    assert len(found) == 1, found
    line = found[0]
    assert line["click_at"] == "rung" and line["tick"] == line["click"]
    assert line["chosen"] == [["A_face", 0, "0"]] and line["clock_source"] == "measured:0"
    assert 0 <= line["click"] - line["birth"] <= 10
    live = simulation.records[first]
    assert live.clicked and live.content == 0 and live.first_rung[a_face] == line["click"]
    assert np.any(live.now)  # GAMEBOARD: the rows still on the board after the line
    # two bodies one Link apart, each naming the other's set
    document = massive_world([400, 1, 1], CHAIN, [800, 809], faces={"x": "open"})
    document["families"][0]["phase_per_link"] = [1, 1]
    document["ticks"] = 400
    document["clock_stamp"] = True
    document["wheel"] = 64
    document["measured"] = [emitter(100, "between"), emitter(113, "between")]
    document["detectors"] = [{"name": "between", "block": 0, "positions": [[112, 0, 0]], "wheel": 256}]
    seed_source(document, 0)
    seed_source(document, 1)
    simulation, lines = run(document, 400)
    found = gathers(lines)
    assert {line["record"] >> 32 for line in found} == {0, 1}
    for line in found:
        assert line["click_at"] == "rung" and line["click"] == line["tick"]
        assert line["chosen"] == [["between", 0, "0"]] and line["clock_source"] == "measured:0"
    # the close without a click: no line
    document = light_clock_world("open", False)
    document["measured"].append(body(5))
    document["detectors"] = [{"name": "behind", "positions": [[5, 0, 0]], "wheel": 1}]
    document["measured"][0]["receiver"] = "behind"
    simulation, lines = run(document, 500)
    assert not gathers(lines)
    # the block's own massive record lives among the records: count light's alone
    closed = simulation.layer.born - sum(1 for live in simulation.records.values() if live.family == 0)
    assert closed >= 1
    transit = simulation.books()["families"]["light"]["transit"]
    assert transit["escaped"] == closed and transit["taken_by_emitter"] == 0
    assert transit["closed_after_click"] == 0 and transit["balanced"]


def test_d_sagnac_rest_loads_and_steps_under_the_form_without_positions():
    """The registered world `examples/events/massive_record/sagnac_rest.json` (the two
    emitter bodies at [700, 712) and [772, 784) at rest, A `receiver` at_b and B at_a, the
    sets at the bodies' cells at W 256) loads and is stepped 300 intervals as a load-and-step
    diagnostic (no pin): each body births (its excitations click at their rungs, at least
    one birth per body), and under BUILD.md section 26 item 10 each body's own set, which IS
    its cells, takes its own record as it is written (a sink for it, the receiver being the
    other's set): no gather line within the 300, the records' content on `escaped`, the
    books balanced. The Sagnac geometry (the form without positions) is re-derived in the
    mirror item before its run; its readings are held. The edge case: the file on disk is
    byte for byte what the test read."""
    before = SAGNAC_REST.read_bytes()
    document = json.loads(before)
    world = parse_nature_beam_world(document)
    assert [entry.block.receiver for entry in world.measured if entry.block is not None] == [
        "at_b",
        "at_a",
    ]
    simulation, lines = run(copy.deepcopy(document), 300, every=100)
    births = [line for line in lines if line["event"] == "birth"]
    assert {line["measured"] for line in births} == {0, 1}
    assert not gathers(lines)
    for live in simulation.records.values():
        if live.family == 0:
            assert not any(live.pointers)
    assert SAGNAC_REST.read_bytes() == before
