"""The receiver by name and the click line at the rung (`detector-law-v1`,
DECLARATIONS.md section 13 item 7 and section 10 items 9 and 10; BUILD.md section 21;
Nature24's eight decisions of 2026-09-24, 12:40Z, through the Boss). On a closed chain of
200 with one emitter body and one named set 60 Links away at wheel 64: (a) exactly one
gather line per record at the set's rung, its time the rung's interval, the record deleted
whole at it; (b) the block's own cell on no ladder; (c) the loader's refusals of
`receiver`; (d) the permutation test, the detector list reordered giving byte-identical
gather lines (issue #1116); (e) a set beside the receiver books the flux into its Node and
is never chosen, its pointer on the line's `sunk` (HOST). Then the line's time, and the
registered world `sagnac_rest.json` loaded and stepped. SINCE THE FLUX READING (ALGEBRA.md
9.19 (3); BUILD.md section 26 item 14) nothing takes: every cell books the one-way flux
into its Nodes, the click is on the cumulative ladder and ends the record; the chain's
faces are closed (an open face is the receiver `face`, last on every ladder, and two
Links behind a body it clicks the half that leaves). Every number here is the engine's
reading on that head (COMPUTATION, a click line or a row's level), named so; no pin world
is run to prove the line and no pin is read."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.events.world import input_stamp, parse_nature_beam_world
from tests.test_massive_record import light_clock_world, massive_world, seed_source

SAGNAC_REST = Path(__file__).resolve().parents[1] / "examples/events/massive_record/sagnac_rest.json"
CLOSED_CHAIN = {"x": "closed", "y": "periodic", "z": "periodic"}
Spy = dict[int, tuple[list[int], list[int], int, int, int]]


def emitter(position: int, receiver: str | None, momentum: int = 0, stock: int = 4) -> dict:
    """An emitter body of side 12 at `position` on the matter kind [800, 809]: the well
    [800, 801] (W = 2403 remainder values, ALGEBRA.md 9.22 (4)), its coupling G [1, 50], g
    [1, 1000] to light (required, 9.19 (4e)), the seed 50 x 2^20 (its
    profile on the mode by `seed_source` once the world is built), its `emitter` of light
    with the stock `stock`, its `receiver` where one is named (the line at that set's
    rung)."""
    block = {
        "position": [position, 0, 0],
        "family": "matter",
        "amount": stock,
        "phase": 0,
        "momentum": [momentum, 0, 0],
        "fixed": True,
        "side": 12,
        "pair": [800, 801],
        "coupling": {"G": [1, 50], "g": [1, 1000]},
        "seed": 50 << 20,
        "emitter": {"family": "light"},
        "margin": "control",
    }
    if receiver is not None:
        block["receiver"] = receiver
    return block


def body(x: int) -> dict:
    """A receiver body of light at x (a measured event, one Node), one Node of a detector
    cube read as a set by name (record 1899)."""
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
    """The declaration's test world: a chain of 200 (x closed, mirrors), light's clock
    [1, 1], the emitter body A at [20, 32) naming `screen` (four births), the set `screen`
    the cube of side 3 at [91, 93] (60 Links from A's face at 31), and the set `beside` the
    cube at [8, 10] behind A (off A's ladder); no wheel (the record's own, 9.22 (4))."""
    document = massive_world([200, 1, 1], CLOSED_CHAIN, [800, 809], faces={"x": "open"})
    document["families"][0]["phase_per_link"] = [1, 1]
    document["ticks"] = 500
    document["clock_stamp"] = True
    document["measured"] = [emitter(20, receiver, 70), *(body(x) for x in (91, 92, 93, 8, 9, 10))]
    document["detectors"] = [
        {"name": "screen", "positions": [[91, 0, 0], [92, 0, 0], [93, 0, 0]]},
        {"name": "beside", "positions": [[8, 0, 0], [9, 0, 0], [10, 0, 0]]},
    ]
    seed_source(document, 0)
    return document


def run(
    document: dict, ticks: int, every: int = 50, seen: Spy | None = None
) -> tuple[DetectorLawSimulation, list[dict]]:
    """The world stepped `ticks` intervals with the books read every `every` intervals and at
    the end; the lines written are returned with the simulation. With `seen`, a spy on the
    engine's `_ladder_click` records per clicked record its pointers as the click read
    them, its ladder (`_ladder_of`), its residue and its norm."""
    lines: list[dict] = []
    simulation = DetectorLawSimulation(parse_nature_beam_world(document), observer=lines.append)
    if seen is not None:
        original = simulation._ladder_click

        def spy(live, increments):
            pointers = list(live.pointers)
            original(live, increments)
            if live.clicked and live.identity not in seen:
                seen[live.identity] = (
                    pointers,
                    simulation._ladder_of(live),
                    live.u,
                    live.norm,
                    live.wheel,
                )

        simulation._ladder_click = spy  # type: ignore[method-assign]
    for _ in range(ticks):
        simulation.step()
        if simulation.tick % every == 0:
            assert simulation.books()["balanced"], simulation.tick
    assert simulation.books()["balanced"], simulation.tick
    return simulation, lines


def gathers(lines: list[dict]) -> list[dict]:
    return [line for line in lines if line["event"] == "gather"]


def test_one_line_per_record_at_the_receivers_rung_the_permutation_and_the_cells_off_the_ladder():
    """(a) On the closed chain of 200 every record A emits writes EXACTLY ONE gather line, at
    `screen`'s rung (`click_at` rung, `chosen` screen, `tick` the rung's interval equal to
    `click`), more than 60 intervals after its birth (the +x half's front over 60 Links at a
    pace below one Link per interval), the ladder the one cell (the block's `receiver`, read
    through `receiver_cell`), the line carrying the quantum (`content` 1) and the record
    deleted whole at it (never in `records` after its line), the definition and
    `receiver_cell` carrying the name; (d) the detector list reversed gives byte-identical
    gather lines up to the order of the HOST listing `cells` (issue #1116: the list's order
    is no input to the click); (e) `beside` and A's own cell
    are CELLS OFF THE LADDER: they book the one-way flux into their Nodes (the -x half
    passes `beside` twelve Links behind A: its pointer above 0 as the click read it), are
    never chosen, and the line's `T` counts them with the screen (HOST); the books
    balanced. The edge case (c): the same world without
    `receiver` loads (the ladder every declared set in the declared order, `screen` then
    `beside`: the first record's line at `beside`, the set its -x half reaches first);
    `receiver` on a block that emits nothing, a name no set declares (the names listed) and
    a value that is no string are refused."""
    world = parse_nature_beam_world(chain_of_200())
    assert world.measured[0].block is not None and world.measured[0].block.receiver == "screen"
    dumps: list[list[str]] = []
    for reversed_sets in (False, True):
        document = chain_of_200()
        if reversed_sets:
            document["detectors"] = list(reversed(document["detectors"]))
        seen: Spy = {}
        simulation, lines = run(document, 500, seen=seen)
        screen = simulation.cell_names.index("screen")
        beside = simulation.cell_names.index("beside")
        own = simulation.blocks[0].cell
        assert simulation.receiver_cell == {0: screen} and simulation.has_receiver
        found = gathers(lines)
        assert len(found) >= 3, found
        assert len({g["record"] for g in found}) == len(found)  # one line per record
        for line in found:
            assert line["chosen"] == [["screen", 0, "0"]] and line["click_at"] == "rung"
            assert line["tick"] == line["click"] and line["click"] - line["birth"] > 60
            assert "ladder" not in line and line["content"] == 1
            assert line["record"] not in simulation.records and line["clock_source"] == "interval"
            pointers, ladder, u, norm, wheel = seen[line["record"]]
            assert ladder == [screen] and u == line["u"] and wheel == 2403
            # the cumulative rule on the click's own pointers (ALGEBRA.md 9.19 (3) (b))
            assert 2 * wheel * pointers[screen] >= (2 * u + 1) * norm
            # the cells off the ladder: booked, never chosen, counted in T
            assert pointers[beside] > 0 and pointers[own] >= 0
            assert line["T"] == sum(pointers) == pointers[screen] + pointers[beside] + pointers[own]
        # the line's `cells` is a HOST listing in the cells' order (the detector
        # list's, its rungs cumulative in that order); the click's fields are
        # compared without it
        dumps.append([json.dumps({k: v for k, v in g.items() if k != "cells"}) for g in found])
    assert dumps[0] == dumps[1]
    # a world with no emitter carries no receiver
    plain = light_clock_world("closed", True)
    for key in ("emitter", "receiver"):
        plain["measured"][0].pop(key)
    plain["input"] = input_stamp(plain)  # the stamp without the born pair (record 1886)
    simulation, _ = run(plain, 10)
    assert not simulation.has_receiver
    # (c) without `receiver` the ladder is every declared set in the declared order
    unnamed = parse_nature_beam_world(chain_of_200(None))
    assert unnamed.measured[0].block is not None and unnamed.measured[0].block.receiver is None
    simulation, lines = run(chain_of_200(None), 120)
    assert not simulation.has_receiver
    first = gathers(lines)[0]
    assert first["chosen"] == [["beside", 0, "0"]] and "ladder" not in first
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


def test_the_blocks_own_cell_is_on_no_ladder():
    """(b) On the closed chain of 200 the block's own cell (`measured:0`) is on no record's
    ladder: it books the one-way flux into A's cells (the -x half's return through the
    mirror at x = 0, forty Links there and back, before the +x half's rung at `screen`:
    its pointer above 0 as the click read it) and is never chosen, every line at `screen`.
    The edge case: a block naming the set that IS its own cells (the sagnac form, `block`
    without positions) on the closed chain of 600 at rest: the born record is
    written ON the set's cells and leaves them (the outward flux is booked to no cell), so
    the set reads nothing of the write itself; the record clicks at the set only once the
    mirrors return the field into the cells (the self-click of BUILD.md section 26 item 10
    retired with the take), later than the birth's next interval."""
    seen: Spy = {}
    simulation, lines = run(chain_of_200(), 400, seen=seen)
    block = simulation.blocks[0]
    own_cell = block.cell
    assert simulation.cell_names[own_cell] == "measured:0"
    found = gathers(lines)
    assert found and all(g["chosen"] == [["screen", 0, "0"]] for g in found)
    assert any(seen[g["record"]][0][own_cell] > 0 for g in found)
    assert all(seen[g["record"]][4] == 2403 for g in found)
    document = massive_world([600, 1, 1], CLOSED_CHAIN, [800, 809], faces={"x": "open"})
    document["ticks"] = 700
    document["clock_stamp"] = True
    document["measured"] = [emitter(200, "at_a", 0)]
    document["detectors"] = [{"name": "at_a", "block": 0}]
    seed_source(document, 0)
    seen = {}
    simulation, lines = run(document, 700, seen=seen)
    assert simulation.receiver_cell == {0: simulation.cell_names.index("at_a")}
    found = gathers(lines)
    assert found and all(g["chosen"] == [["at_a", 0, "0"]] for g in found)
    assert all(g["click"] > g["birth"] + 1 and g["tick"] == g["click"] for g in found)


def test_the_lines_time():
    """The line's time: on the light clock's chain of 173 with the faces CLOSED and A naming
    its own bound set `A_face` (x = 112), the first record's line is written at the
    rung's interval (`tick` equal to `click`), after its birth (the set beside A's cells
    books the +x half from the first interval; the rung (2 u + 1) T / (2 W) on the record's
    own residue from the law decides how much of the record must pass, the mirrors'
    returns included), stamped with A's count (clock_source measured:0); the record is
    deleted whole at its line (not among the records, no second line within 300
    intervals). Two emitter bodies three Links apart naming
    the set on the cube of three free Nodes between them (bound to the first): both bodies'
    records write their lines there at a rung with `tick` equal to `click`, stamped with the
    bound body's count."""
    document = light_clock_world("closed", False)
    document["measured"][0]["receiver"] = "A_face"
    simulation, lines = run(document, 300)
    first = 1
    found = [g for g in gathers(lines) if g["record"] == first]
    assert len(found) == 1, found
    line = found[0]
    assert line["click_at"] == "rung" and line["tick"] == line["click"]
    assert line["chosen"] == [["A_face", 0, "0"]] and line["clock_source"] == "measured:0"
    assert 0 <= line["click"] - line["birth"] <= 300 and 0 <= line["u"] < 2403
    assert first not in simulation.records
    # two bodies three Links apart, each naming the cube between them
    document = massive_world([400, 1, 1], CLOSED_CHAIN, [800, 809], faces={"x": "open"})
    document["families"][0]["phase_per_link"] = [1, 1]
    document["ticks"] = 400
    document["clock_stamp"] = True
    document["measured"] = [emitter(100, "between"), emitter(115, "between")]
    document["detectors"] = [
        {"name": "between", "block": 0, "positions": [[112, 0, 0], [113, 0, 0], [114, 0, 0]]}
    ]
    seed_source(document, 0)
    seed_source(document, 1)
    simulation, lines = run(document, 400)
    found = gathers(lines)
    assert {line["record"] >> 32 for line in found} == {0, 1}
    for line in found:
        assert line["click_at"] == "rung" and line["click"] == line["tick"]
        assert line["chosen"] == [["between", 0, "0"]] and line["clock_source"] == "measured:0"


def test_sagnac_rest_loads_and_steps_under_the_form_without_positions():
    """The registered world `examples/events/massive_record/sagnac_rest.json` (the two
    emitter bodies at [700, 712) and [772, 784) at rest, A `receiver` at_b and B at_a, the
    sets at the bodies' cells at W 256) loads and is stepped 300 intervals as a load-and-step
    diagnostic (no pin): each body births (its excitations click at their rungs, at least
    one birth per body), and each body's records click at the OTHER body's set (A's at
    at_b, B's at at_a: the one-way flux into the other's cells over the 60 Links between
    them, the line at the rung, the record deleted at it), none at its own; the books
    balanced. The Sagnac geometry (the form without positions) is re-derived in the mirror
    item before its run; its readings are held. The edge case: the file on disk is byte for
    byte what the test read."""
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
    found = gathers(lines)
    assert {(line["record"] >> 32, line["chosen"][0][0]) for line in found} == {(0, "at_b"), (1, "at_a")}
    assert all(
        line["tick"] == line["click"] and line["record"] not in simulation.records for line in found
    )
    assert SAGNAC_REST.read_bytes() == before
