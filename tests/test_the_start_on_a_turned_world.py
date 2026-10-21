"""The start's booking on a turned world (ALGEBRA.md #the-generator (g), The start, the remainder from which the first step returns the rest; #what-a-body-is, The body is the fixed point of its binding row and The lay is a standing state of the step, the held write returning the start's source within 2 units; docs/FURTHER_RESEARCH.md, The start's booking kick on every turned world): on a world whose holder of the sign declares `act: rotation`, `bookings.booked_sources` takes the held rows' booking after the first interval's phase act (`node.phase_act`, the one act `Lattice.step` takes before the lines' step) and turns the phase lines back to the angle 0 bit for bit, for every held holder under the rotation by the loader's flag `Row.rotation` and no form's name (2026-10-21, the engine corrected to the law's stated line; the booking before this date took the trial step at the seed angle 0 on every turned holder but the one declaring the Lorentz form, so that the first write moved the record's row at the centre of hydrogen_1s from 3254 to 4043 and of hydrogen_line from 2825 to 3355, the finding closed here with the fixed engine's 3659 and 3658). The worlds are the repository's own hydrogen atoms, examples/events/atom/hydrogen_1s.json and hydrogen_line.json (hydrogen_read3's universe, no key `form`, an open 11-cube, the proton at [5, 5, 5], the electron's record at [6, 5, 5]), one interval each."""

from pathlib import Path

import numpy as np
import pytest

from event_universe import bookings, lattice, records, world_files
from event_universe.lattice import Lattice
from event_universe.world_files import load_world

ATOM = Path(world_files.REPOSITORY_ROOT) / "examples" / "events" / "atom"
ROUNDING = 2  # Rule3's rounding on the held write, the lay a standing state within 2 units (ALGEBRA.md)
CENTRE = (5, 5, 5)


def time_lines(board: Lattice) -> list[tuple[str, int, np.ndarray]]:
    """Every held row's time line as it stands, (the family's name, the row, the level now), every family held and every row of it."""
    found = []
    for index, family in enumerate(board.families):
        if family.held:
            for row in range(family.records):
                found.append(
                    (family.name, row, board.states[index].lines[row * family.width].now.copy())
                )
    return found


@pytest.mark.parametrize(
    ("name", "lay", "after"),
    [("hydrogen_1s", 3659, 3658), ("hydrogen_line", 3092, 3092)],
)
def test_the_first_write_returns_the_rest_on_the_turned_hydrogen_worlds(monkeypatch, name, lay, after):  # type: ignore[no-untyped-def]
    """The electron's Wronskian the start books in its last fixed-point iteration equals the Wronskian the first `Lattice.step` books at every Node bit for bit (the two hooks on `booked_of`, the start's and the step's), so the first write returns the rest: every held row's time line after the first interval within Rule3's rounding of the lay's level at every Node of the board, the electron's own row at the centre pinned at the lay and after the first interval (hydrogen_1s 3659 and 3658; hydrogen_line 3092 and 3092; the shipped booking's 3254 and 4043, 2825 and 3355), and the phase lines after the start stand at the seed angle 0, the state a run starts from, bit for bit."""
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
    assert holder.rotation and not holder.lorentz and holder.records == 3
    bits = board.world.width.bit_length()
    seeded = records.phase_lines(holder, board.shape, board.kind, board.world.node_clock, bits)
    for lines, fresh in zip(board.states[charge].phases, seeded, strict=True):
        for line, start in zip(lines, fresh, strict=True):
            assert np.array_equal(line.now, start.now) and np.array_equal(line.before, start.before)
    laid = time_lines(board)
    assert laid[2][:2] == ("charge", 2) and int(laid[2][2][CENTRE]) == lay  # the electron's own row
    board.step()
    assert len(booked["start"]) >= 1 and len(booked["step"]) == 1
    assert np.array_equal(booked["start"][-1], booked["step"][0])
    stepped = time_lines(board)
    assert int(stepped[2][2][CENTRE]) == after
    for (family, row, before), (_family, _row, now) in zip(laid, stepped, strict=True):
        moved = int(np.abs(now.astype(np.int64) - before.astype(np.int64)).max())
        assert moved <= ROUNDING, (family, row, moved)
