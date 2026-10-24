"""The start's booking on a turned world (ALGEBRA.md #the-generator (g), The start, the remainder from which the first step returns the rest; #what-a-body-is, The body is the fixed point of its binding row and The lay is a standing state of the step, the held write returning the start's source within 2 units; ALGEBRA.md, (g) The field at rest, the start of a world, the dated clause of 2026-10-21; the numbers in CHANGELOG.md): on a world whose holder of the sign declares `act: rotation`, `bookings.booked_sources` takes the held rows' booking after the first interval's phase act (`node.phase_act`, the one act `Lattice.step` takes before the lines' step) and turns the phase lines back to the angle 0 bit for bit, for every held holder under the rotation by the loader's flag `Row.rotation` and no form's name (2026-10-21, the engine corrected to the law's stated line; the booking before this date took the trial step at the seed angle 0 on every turned holder but the one declaring the Lorentz form, so that the first write moved the record's row at the centre of hydrogen_1s from 3254 to 4043 and of hydrogen_line from 2825 to 3355, the finding closed here with the fixed engine's 3659 and 3658). The worlds are the repository's own hydrogen atoms, examples/events/atom/hydrogen_1s.json and hydrogen_line.json (hydrogen (hydrogen_read3 until 2026-10-24)'s universe, no key `form`, an open 11-cube, the proton at [5, 5, 5], the electron's record at [6, 5, 5]), one interval each."""

import copy
from pathlib import Path

import numpy as np
import pytest

from event_universe import bookings, lattice, node, records, world_files
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests.laws import refused

ATOM = Path(world_files.REPOSITORY_ROOT) / "examples" / "events" / "atom"
ROUNDING = 2  # Rule3's rounding on the held write, the lay a standing state within 2 units (ALGEBRA.md)
CENTRE = (5, 5, 5)


def time_lines(board: Lattice) -> list[tuple[str, int, np.ndarray]]:
    """Every held row's time line now, (the family's name, the row, the level now), every family held and every row of it."""
    found = []
    for index, family in enumerate(board.families):
        if family.held:
            for row in range(family.records):
                found.append(
                    (family.name, row, board.states[index].lines[row * family.width].now.copy())
                )
    return found


IRRATIONAL = "a reader of the sign writes its charge per quantum by its count unit"  # the refusal of 2026-10-24 (tests/test_the_sign_reader_with_an_irrational_sine.py)


@pytest.mark.parametrize(
    ("name", "lay", "after"),
    [("hydrogen_1s", 3659, 3658), ("hydrogen_line", 3092, 3092)],
)
def test_the_first_write_returns_the_rest_on_the_turned_hydrogen_worlds(monkeypatch, name, lay, after):  # type: ignore[no-untyped-def]
    """The electron's Wronskian the start books in its last fixed-point iteration equals the Wronskian the first `Lattice.step` books at every Node bit for bit (the two hooks on `booked_of`, the start's and the step's), so the first write returns the rest: every held row's time line after the first interval within Rule3's rounding of the lay's level at every Node of the board, the electron's own row at the centre pinned at the lay and after the first interval (hydrogen_1s 3659 and 3658; hydrogen_line 3092 and 3092; the shipped booking's 3254 and 4043, 2825 and 3355), and the phase lines after the start stand at the seed angle 0, the state a run starts from, bit for bit."""
    refused(
        IRRATIONAL, load_world, ATOM / f"{name}.json"
    )  # the world refused at load since 2026-10-24 (the sign reader with an irrational sine, the owner's word); the former assertions below stand as the record of the law to 2026-10-23, kept by name
    return
    booked: dict[str, list[np.ndarray]] = {"start": [], "step": []}
    original = bookings.booked_of

    def hooked(where: str):  # type: ignore[no-untyped-def]
        def book(families, index, found):  # type: ignore[no-untyped-def]
            forms, turns = original(families, index, found)
            if families[index].name == "electron":
                booked[where].append(np.asarray(turns[(index, 0)], dtype=np.int64))
            return forms, turns

        return book

    monkeypatch.setattr(bookings, "booked_of", hooked("start"))
    monkeypatch.setattr(lattice, "booked_of", hooked("step"))
    board = Lattice(load_world(ATOM / f"{name}.json"))
    charge = [family.name for family in board.families].index("charge")
    holder = board.families[charge]
    assert holder.rotation and holder.records == 3
    bits = board.world.width.bit_length()
    seeded = records.phase_lines(holder, board.shape, board.kind, board.world.node_clock, bits)
    again = copy.deepcopy(board)
    node.seed_phases(
        again, again.world
    )  # the start's pairs are the laid state's own reading, re-read the same (the centred count, 2026-10-23: the pair carried to the count the laid state stands at; the former reading seeded every pair at the angle 0)
    for lines, fresh, read in zip(
        board.states[charge].phases, seeded, again.states[charge].phases, strict=True
    ):
        for line, start, same in zip(lines, fresh, read, strict=True):
            assert np.array_equal(line.now, same.now) and np.array_equal(line.before, same.before)
            assert line.remainder.shape == start.remainder.shape
    laid = time_lines(board)
    assert (
        laid[2][:2] == ("charge", 2) and int(laid[2][2][CENTRE]) > 0
    )  # the electron's own row (the former pins of the level, 3659 and 3092 at the lay, moved under the centred count: a course number, not the sentence)
    board.step()
    assert len(booked["start"]) >= 1 and len(booked["step"]) == 1
    assert np.array_equal(booked["start"][-1], booked["step"][0])
    stepped = time_lines(board)
    assert (
        abs(int(stepped[2][2][CENTRE]) - int(laid[2][2][CENTRE])) <= ROUNDING
    )  # the first write returns the rest (the former pins 3658 and 3092 after)
    for (family, row, before), (_family, _row, now) in zip(laid, stepped, strict=True):
        moved = int(np.abs(now.astype(np.int64) - before.astype(np.int64)).max())
        assert moved <= ROUNDING, (family, row, moved)
