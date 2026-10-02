"""A GameBoard diagnostic and no engine line (the advisor's check of problem 1, #1563 comment 5956767030): one held row stepped alone over `intervals` intervals from its laid rest with the source held, every other row and every record kept as laid; the row's level along +x from the body's centre at the start, at 1, 35, 70, 105 and 140 intervals and at the end, and the other held rows' beside it. Uses GameBoard's own acts as GameBoard.step composes them for that row (currents, stresses, rulers, stepped and hold: the row's own step by Rule3 and then the one write from the bookings) and replaces no record: the bodies' lines stay the lay's, so the form each interval books is the lay's own, and the other held rows stay at their rests.

PYTHONPATH=src python holder_alone.py <world.json> <intervals> <row name> [reach]
"""

import json
import sys
from pathlib import Path

import numpy as np

from event_universe.bookings import Bookings, booked_of
from event_universe.game_board import GameBoard
from event_universe.world_files import load_world

path, intervals, which = Path(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
reach = int(sys.argv[4]) if len(sys.argv) > 4 else 12
board = GameBoard(load_world(path))
names = [family.name for family in board.families]
held = {names[i]: i for i in board.held}
body = board.world.bodies[0]
counts = np.asarray(board.quanta(body.family)[0])
centre = tuple(int(v) for v in np.unravel_index(int(counts.argmax()), counts.shape))


def along(index: int, axis: int = 0) -> list[int]:
    array = np.asarray(board.states[index].lines[0].now)
    out = []
    for r in range(reach + 1):
        node = list(centre)
        node[axis] += r
        out.append(int(array[tuple(node)]))
    return out


start = {name: along(i) for name, i in held.items()}
quanta_start = int(counts.sum())
read_at = sorted({1, 35, 70, 105, 140, intervals})  # the gap's time 1 / omega_g = 35 intervals
along_the_way: dict[int, list[int]] = {}
for interval in range(1, intervals + 1):
    forms, turns = Bookings(), Bookings()
    currents, senses, stresses = board.currents(), board.sense_currents(), board.stresses()
    rulers = board.rulers(1)
    for family in board.order:
        _lines, bookings = board.stepped(
            family, 1
        )  # the source held: the record's lines are not replaced
        for booked, gained in zip(
            (forms, turns), booked_of(board.families, family, bookings), strict=True
        ):
            booked.update(gained)
    lines, _bookings = board.stepped(
        held[which], 1
    )  # the row's own step by Rule3, with or without a gap
    board.states[held[which]].lines = lines
    board.hold(held[which], forms, turns, 1, stresses, senses, rulers)  # the one write from the bookings
    board.tick += 1
    if interval in read_at:
        along_the_way[interval] = along(held[which])
end = {name: along(i) for name, i in held.items()}
quanta_end = int(np.asarray(board.quanta(body.family)[0]).sum())
print(
    json.dumps(
        {
            "label": "GAMEBOARD",
            "world": path.name,
            "stepped_alone": which,
            "intervals": intervals,
            "centre": list(centre),
            "body_quanta": [quanta_start, quanta_end],
            "start": start,
            "along_the_way": along_the_way,
            "end": end,
        }
    )
)
