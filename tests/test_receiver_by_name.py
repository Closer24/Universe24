"""The receiver by name and the click line at the rung: one gather line per record at the set's rung,
the block's own detector on no ladder, the loader's refusals, and a reordered detector list byte for byte."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import input_stamp, parse_nature_beam_world
from tests.bodies import CLOSED_CHAIN, emitter, light_clock_world, massive_world, seed_source
from tests.worlds import lawful_wheel

LIGHT_CLOCK = Path(__file__).resolve().parents[1] / "examples/events/massive_record/light_clock.json"
Spy = dict[int, tuple[list[int], list[int], int, int, int]]


def body(x: int) -> dict:
    """A receiver body of light at x (a measured event, one Node), one Node of a detector
    cube read as a set by name (record 1899)."""
    return {
        "position": [x, 0, 0],
        "family": "light",
        "amount": 1,
        "stocks": {},
        "momentum": [0, 0, 0],
        "momentum_before": [0, 0, 0],
    }


def chain_of_200(receiver: str | None = "screen") -> dict:
    """The declaration's test world: a chain of 200 (x closed, mirrors), light on the given
    clock [512, 1] of N = 1024, the emitter body A at [20, 52) naming `screen` (four givings,
    the train along +x), the set `screen` the cube of side 3 at [91, 93] (40 Links from A's
    head at 51), and the set `beside` the cube at [60, 62] between A and the screen (off
    A's ladder); no wheel (the record's own, ALGEBRA.md #a-familys-declaration)."""
    document = massive_world([200, 1, 1], CLOSED_CHAIN, [800, 809])
    document["ticks"] = 500
    document["measured"] = [emitter(20, receiver, 70), *(body(x) for x in (91, 92, 93, 60, 61, 62))]
    document["detectors"] = [
        {"name": "screen", "positions": [[91, 0, 0], [92, 0, 0], [93, 0, 0]]},
        {"name": "beside", "positions": [[60, 0, 0], [61, 0, 0], [62, 0, 0]]},
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
                    live.pace,
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
    """(a) On the closed chain of 200 every record A emits writes EXACTLY ONE gather line, at `screen`'s rung (`click_at` rung, `chosen` screen, `tick` the rung's interval equal to `click`), never before the lattice's cone allows (one Link per interval from the body's head at its giving to the screen's nearest Node at 91; the body steps toward the screen at the momentum 70, so the later givings are nearer: the fourth's head 18 Links away, its click 51 intervals after its giving on this head's residue 114 of 2403 before the Node clock, COMPUTATION; SINCE THE NODE CLOCK, BUILD.md section 26 item 31, the wheel at the body's Nodes is the rule's with its content and the residues moved; SINCE THE REMAINDER KEPT, BUILD.md section 26 item 29, the residues spread from the kept remainder), the ladder the one detector (the block's `receiver`, read through `receiver_detector`), the line carrying the quantum (`content` 1) and the record deleted whole at it (never in `records` after its line), the definition and `receiver_detector` carrying the name; (d) the detector list reversed gives byte-identical gather lines up to the order of the HOST listing `detectors` (issue #1116: the list's order is no input to the click); (e) `beside` and A's own detector are DETECTORS OFF THE LADDER: they book the one-way flux into their Nodes (the train passes `beside` between A and the screen: its pointer above 0 as the click read it; A's own detector books nothing of its outgoing train, the outward flux negative), are never chosen, and the line's `T` counts them with the screen (HOST); the books balanced. The edge case (c): the same world without `receiver` loads (the ladder every declared set in the declared order, `screen` then `beside`: the first record's line at `beside`, the set the train reaches first); `receiver` on a block that emits nothing, a name no set declares (the names listed) and a value that is no string are refused."""
    world = parse_nature_beam_world(chain_of_200())
    assert world.measured[0].block is not None and world.measured[0].block.receiver == "screen"
    dumps: list[list[str]] = []
    for reversed_sets in (False, True):
        document = chain_of_200()
        if reversed_sets:
            document["detectors"] = list(reversed(document["detectors"]))
            document["stamp"] = input_stamp(document)  # the stamp over the whole file (item 28)
        seen: Spy = {}
        simulation, lines = run(document, 500, seen=seen)
        screen = simulation.detector_names.index("screen")
        beside = simulation.detector_names.index("beside")
        own = simulation.blocks[0].detector
        assert simulation.receiver_detector == {0: screen} and simulation.has_receiver
        found = gathers(lines)
        assert len(found) >= 3, found
        assert len({g["record"] for g in found}) == len(found)  # one line per record
        givings = {line["record"]: line for line in lines if line["event"] == "giving"}
        for line in found:
            assert line["chosen"] == [["screen", 0, "0"]] and line["click_at"] == "rung"
            head = givings[line["record"]]["node"][0] + 31  # the body's head at the giving
            assert line["tick"] == line["click"] and line["click"] - line["giving"] >= 91 - head
            assert "ladder" not in line and line["content"] == 1
            assert line["record"] not in simulation.records and line["clock_source"] == "interval"
            pointers, ladder, u, norm, wheel, pace = seen[line["record"]]
            assert ladder == [screen] and u == line["u"] and wheel == givings[line["record"]]["W"]
            assert lawful_wheel(simulation.world, givings[line["record"]])
            # the cumulative rule on the click's own pointers (ALGEBRA.md #rule3), the
            # plain flux against the norm's rational norm / pace (item 36)
            assert pace == givings[line["record"]]["pace"]
            assert 2 * wheel * pace * pointers[screen] >= (2 * u + 1) * norm
            # the detectors off the ladder: booked, never chosen, counted in T; `beside` books
            # while its Nodes are its own (SINCE item 48 the Ports are re-read at every hop, so
            # once the stepping body covers [60, 62] the set has no Node and no Port)
            assert pointers[own] >= 0
            if head < 60:
                assert pointers[beside] > 0
            assert line["T"] == sum(pointers) == pointers[screen] + pointers[beside] + pointers[own]
        # the line's `detectors` is a HOST listing in the detectors' order (the detector
        # list's, its rungs cumulative in that order); the click's fields are
        # compared without it
        dumps.append([json.dumps({k: v for k, v in g.items() if k != "detectors"}) for g in found])
    assert dumps[0] == dumps[1]
    # a world with no emitter carries no receiver
    plain = light_clock_world("closed", True)
    for key in ("emitter", "receiver"):
        plain["measured"][0].pop(key)
    plain["stamp"] = input_stamp(plain)  # the stamp without the given pair (record 1886)
    simulation, _ = run(plain, 10)
    assert not simulation.has_receiver
    # (c) without `receiver` the ladder is every declared set in the declared order; the
    # emitter at rest here (SINCE item 48 a stepping body covering the set at [60, 62] takes
    # its Nodes and its Ports, so the set books nothing from then on)
    resting = chain_of_200(None)
    resting["measured"][0]["momentum"] = [0, 0, 0]
    resting["stamp"] = input_stamp(resting)
    unnamed = parse_nature_beam_world(resting)
    assert unnamed.measured[0].block is not None and unnamed.measured[0].block.receiver is None
    simulation, lines = run(resting, 300)  # the first gather past 120 at the seed 50 x 2^12 (item 44)
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
    unknown["stamp"] = input_stamp(unknown)  # the stamp over the whole file (item 28)
    with pytest.raises(
        ValueError, match=r"'nowhere' names no declared detector set.*'screen', 'beside'"
    ):
        parse_nature_beam_world(unknown)
    number = chain_of_200()
    number["measured"][0]["receiver"] = 3
    number["stamp"] = input_stamp(number)
    with pytest.raises(ValueError, match=r"measured\[0\]\.receiver must be a word, not 3"):
        parse_nature_beam_world(number)


def test_the_blocks_own_cell_is_on_no_ladder():
    """(b) On the closed chain of 200 the block's own detector (`measured:0`) is on no record's
    ladder: the outgoing train leaves A's Nodes through their Ports (the outward flux
    negative, booked nowhere; what the detector books is the tapers' dispersion returned off
    the mirror at x = 0, below a hundredth of the norm as the click read it) and A's detector
    is never chosen, every line at `screen`. The edge case: a block naming the set that IS its own
    Nodes (the light clock's form, `block` without positions) on the closed chain of 400 at
    rest, A at [300, 332): the given train is written ON the set's Nodes and leaves them
    toward +x (the outward flux is booked to no detector), so the set reads nothing of the
    write itself; the record clicks at the set only once the mirror at x = 399 returns
    the train into the Nodes (the round trip 2 x 67 Links at v_g = 0.447, about 300
    intervals; the self-click of BUILD.md section 26 item 10 retired with the take), later
    than the giving's next interval."""
    seen: Spy = {}
    simulation, lines = run(chain_of_200(), 400, seen=seen)
    block = simulation.blocks[0]
    own_detector = block.detector
    assert simulation.detector_names[own_detector] == "measured:0"
    found = gathers(lines)
    assert found and all(g["chosen"] == [["screen", 0, "0"]] for g in found)
    # A's own detector books nothing of the light leaving A's Nodes (the outward flux is
    # negative); SINCE COMMIT 7 (the window, ALGEBRA.md #the-primitives) the light leaves both ways
    # and the half toward x = 0 returns off the mirror into A's Nodes and books there
    # (COMPUTATION), off every ladder by name: never chosen
    assert all(own_detector not in seen[g["record"]][1] for g in found)
    givings = {line["record"]: line for line in lines if line["event"] == "giving"}
    assert all(seen[g["record"]][4] == givings[g["record"]]["W"] for g in found)
    assert all(lawful_wheel(simulation.world, givings[g["record"]]) for g in found)
    document = massive_world([400, 1, 1], CLOSED_CHAIN, [800, 809])
    document["ticks"] = 700
    document["measured"] = [emitter(300, "at_well", 0)]
    document["detectors"] = [{"name": "at_well", "block": 0}]
    seed_source(document, 0)
    seen = {}
    simulation, lines = run(document, 700, seen=seen)
    assert simulation.receiver_detector == {0: simulation.detector_names.index("at_well")}
    found = gathers(lines)
    assert found and all(g["chosen"] == [["at_well", 0, "0"]] for g in found)
    # SINCE COMMIT 7 (the window at every Node of the 32-Node body) the set at A's own Nodes
    # books the light leaving A's faces as it piles up inside them, so a record may click at
    # A before the mirror's return (COMPUTATION; the one-Node body's Node of the shipped light clock
    # clicks on the return alone, tests/test_receiver_by_name.py's light clock test)
    assert all(g["tick"] == g["click"] > g["giving"] for g in found)


def test_the_lines_time():
    """The line's time: on the light clock's chain of 173 with the faces CLOSED and A naming
    its own bound set `A_face` (x in [132, 134]), the first record's line is written at the
    rung's interval (`tick` equal to `click`), after its giving (the set beside A's head
    books the train from the first interval; the rung (2 u + 1) T / (2 W) on the record's
    own residue from the law decides how much of the record must pass, the mirrors'
    returns included), stamped with A's count (clock_source measured:0); the record is
    deleted whole at its line (not among the records, no second line within 300
    intervals). Two emitter bodies a hundred Links apart (A at [100, 132), B at [232, 264):
    A's mode at 50 x 2^20 ends 63 Links beyond its head, and the loader refuses a body's
    profile that is not 0 at another body of its family, BUILD.md section 26 item 28), the
    first's train along +x and the second's along -x, naming the set on the cube of three
    free Nodes beside the first (bound to it): both bodies' records write their lines there
    at a rung with `tick` equal to `click`, stamped with the bound body's count."""
    document = light_clock_world("closed", False)
    document["measured"][0]["receiver"] = "A_face"
    simulation, lines = run(document, 300)
    first = 1
    found = [g for g in gathers(lines) if g["record"] == first]
    assert len(found) == 1, found
    line = found[0]
    assert line["click_at"] == "rung" and line["tick"] == line["click"]
    assert line["chosen"] == [["A_face", 0, "0"]] and line["clock_source"] == "measured:0"
    given = next(b for b in lines if b["event"] == "giving" and b["record"] == first)
    assert 0 <= line["click"] - line["giving"] <= 300 and 0 <= line["u"] < given["W"]
    assert lawful_wheel(simulation.world, given)
    assert first not in simulation.records
    # two bodies a hundred Links apart, each naming the cube beside the first
    document = massive_world([400, 1, 1], CLOSED_CHAIN, [800, 809])
    document["ticks"] = 600
    document["measured"] = [emitter(100, "between"), emitter(232, "between", direction=[-1, 0, 0])]
    document["detectors"] = [
        {"name": "between", "block": 0, "positions": [[132, 0, 0], [133, 0, 0], [134, 0, 0]]}
    ]
    seed_source(document, 0)
    seed_source(document, 1)
    simulation, lines = run(document, 600)
    found = gathers(lines)
    assert {line["record"] >> 32 for line in found} == {0, 1}
    for line in found:
        assert line["click_at"] == "rung" and line["click"] == line["tick"]
        assert line["chosen"] == [["between", 0, "0"]] and line["clock_source"] == "measured:0"


def test_the_light_clock_loads_and_steps_under_the_form_without_positions():
    """The registered world `examples/events/massive_record/light_clock.json` (the one table's
    form: [760, 3, 3] with the face slabs 32 deep, A the chain's point extruded, [1, 3, 3] at
    x = 631, giving by the window (commit 7) with its stock of 64, the mirror at [690, 694)
    and the mirror behind A at [629, 631), A's `receiver` at_well the set at its own
    Nodes) loads and is stepped 700 intervals as a load-and-step diagnostic (no pin): A
    givings (its excitations click at their rungs), and its records click at at_well when
    the mirror returns them into A's Nodes (the line at the rung, the record deleted at it;
    at least one within the 700, the round trip about 300 intervals after the giving; under
    the row's floor, ALGEBRA.md #the-paces, one record given at 402 reaches its rung at A's own
    Nodes at 426, before any round trip), none at the faces; the books balanced. The edge case: the file on disk is byte for byte what
    the test read."""
    before = LIGHT_CLOCK.read_bytes()
    document = json.loads(before)
    world = parse_nature_beam_world(document)
    assert [entry.block.receiver for entry in world.measured if entry.block is not None] == [
        "at_well",
        None,
        None,
    ]
    simulation, lines = run(copy.deepcopy(document), 700, every=100)
    givings = [line for line in lines if line["event"] == "giving"]
    assert givings and {line["measured"] for line in givings} == {0}
    found = gathers(lines)
    assert found and {line["chosen"][0][0] for line in found} == {"at_well"}
    assert all(
        line["tick"] == line["click"] and line["record"] not in simulation.records for line in found
    )
    trips = [line["click"] - line["giving"] for line in found]
    assert sum(trip > 200 for trip in trips) == len(trips) - 1 and min(trips) == 24
    assert LIGHT_CLOCK.read_bytes() == before
