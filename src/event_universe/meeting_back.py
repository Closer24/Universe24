"""The meeting that runs back, the click that writes (ALGEBRA.md, The click is the meeting of the future with the past: backward, to the past, the click runs back along the record to its birth and writes there, the realised term's integers into the record's parts, and the board runs forward again by Rule3, so that every later side reads the realised term where it stands, which gives Bell at a distance; The meeting's reading; The births' book; the owner's words of 2026-10-19 and 2026-10-20, the click writes and nothing is in the books but the draw at the click): for every record of several parts read at N declared sides, each side draws at its own place with its own state in the order of the closes, equal closes in the declared order (`lists.readings`), on its own region's second moments with the Gram of the sides after it (`moments_booked`, `gram_of`, `coefficients_of`, `side_weights`, the Gram theorem); its realised port runs back along the record to its birth, the board stepped back by Rule3 at -1 to the birth's interval from the births' book (`run_back`, `birth_of`, `credit.Books.births`), every act from outside the Node re-presented on the way, the faces from the books' log (`take.faces_presented`) and the lays undone from the books' log of the lay lines (`logged`, `crossed`; `credit.Books.lays`, written by `lay.written`); at the birth the port's integer coefficients are written into the record's parts through the one lay act (`realised`, `lay.laid`, exact in the integers); then the board runs forward again to the close by the step at the Nodes alone (`run_forward`, `Lattice.step` with no act, the lays re-applied by their changes, the record's own later lays scaled), the sides' books taken again on the way (`booked_moments`), and the close asserted: outside the record's cone bit for bit the board the run back left, the parts written 0 at zero, the parts written alike equal (`copied`, `snapshot`, `first_difference`); N runs for N sides, the credit lines carrying the side's order and the record's scale; in the cone's reach, the default, the cone stepped alone (the owner's word of 2026-10-20, only the cone moves and the whole board steps as ever): the run back and the run forward step the record's light cone and nothing else, the ball with one ring of Nodes read from the board and asserted at frame 0, the rest of the board neither read nor written (`cone.stepped_alone`, `credit.Books.reach`); the antisymmetric sign read at other than two sides refused by name at load. The host tool's crossing of the acts from the LATTICE lines (tools/back_in_time.py: `faces_from`, `crossed` from the `face` and `lay` lines) lives here and the tool imports it; the observers' frames of the run back and forward are the lattice's (`Lattice.observers`)."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from event_universe import reports
from event_universe.records import NodeState, Record

if TYPE_CHECKING:
    from event_universe.lattice import Lattice

Snapshot = list[tuple[str, np.ndarray]]  # every array of one family's NodeState with its name, copied
Lines = list[dict[str, object]]  # output lines, as the lattice's output receives them (`reports.py`)


def named(name: str, state: NodeState) -> list[tuple[str, np.ndarray]]:
    """Every array of a family's NodeState with its name, the array itself (no copy): every line's levels now and before and its remainder, every held line's write remainder."""
    found: list[tuple[str, np.ndarray]] = []
    for index, record in enumerate(state.lines):
        found.append((f"{name}.lines[{index}].now", record.now))
        found.append((f"{name}.lines[{index}].before", record.before))
        found.append((f"{name}.lines[{index}].remainder", record.remainder))
    found += [
        (f"{name}.write_remainders[{index}]", value)
        for index, value in enumerate(state.write_remainders)
    ]
    return found


def arrays_of(name: str, state: NodeState) -> Snapshot:
    """Every array of a family's NodeState with its name, copied (`named`)."""
    return [(label, np.asarray(value).copy()) for label, value in named(name, state)]


def snapshot(board: Lattice, states: list[NodeState] | None = None) -> list[Snapshot]:
    """Every array of every family of the lattice, copied: the board at its interval (or the `states` given, frame 0 grown to the board's shape, `frame_grown`), compared bit for bit after a run back and forward (`first_difference`)."""
    return [
        arrays_of(family.name, state)
        for family, state in zip(board.families, board.states if states is None else states, strict=True)
    ]


def first_difference(
    before: list[Snapshot], after: list[Snapshot], where: np.ndarray | None = None
) -> tuple[str, list[int]] | None:
    """The first array and the first Node at which two snapshots differ, or None where they agree bit for bit (a shape that differs named with no Node); with `where`, a mask over the board, the Nodes it names alone (the box's Nodes outside the record's cone, `cone.held`)."""
    for family_before, family_after in zip(before, after, strict=True):
        for (label, was), (_label, now) in zip(family_before, family_after, strict=True):
            if was.shape != now.shape:
                return f"{label} (the shape {list(now.shape)} against {list(was.shape)})", []
            differing = np.argwhere((was != now) if where is None else (was != now) & where)
            if len(differing):
                return label, [int(i) for i in differing[0]]
    return None


def node_of(board: Lattice, line: dict[str, object]) -> tuple[int, tuple[int, int, int]]:
    """A LATTICE line's family by its position and its Node at the file's coordinates."""
    names = [family.name for family in board.families]
    at = [int(a) for a in line[reports.LAY_KEYS[3]][reports.AT]]  # type: ignore[index]
    return names.index(str(line[reports.REPORT_KEYS[3]])), (at[0], at[1], at[2])


def same_lay(line: dict[str, object], kept: dict[str, object]) -> bool:
    """Whether a lay line from a run's output names the lay the books' log holds: the same family, line and Node at the same interval (the log's line is the output's own object where both are kept, and its equal where the lines come from a file)."""
    return all(
        line[key] == kept[key] for key in (reports.REPORT_KEYS[2], reports.REPORT_KEYS[3], reports.LINE)
    ) and list(line[reports.LAY_KEYS[3]][reports.AT]) == list(kept[reports.LAY_KEYS[3]][reports.AT])  # type: ignore[index]


def crossed(board: Lattice, lines: Lines, direction: int = -1, log: bool = False) -> None:
    """The lays of the lattice's interval crossed from their `lay` lines by their changes (ALGEBRA.md, The click is the meeting of the future with the past: the backward run brings no new number along the realised orbit, the board is reversible, and the lay is not taken back; the mathematician's hand: the face's part of the inverse; the one write site of the engine beside the lay act's write step, Rule3's step and the cone's write-back of Rule3's own results into the board (`cone.written_back`, the fourth site the writers gate admits)): per line of the interval, in the lines' order forward and reversed back, the Node at the file's coordinates, the line's levels now and before changed by the lay's own change, after less before, added forward and subtracted back, and the remainder: a lay without an origin changes no remainder and the inverse recovers it; a lay with an origin sets it forward and restores the history's own backward, the board's remainder before the setting logged into the line's `before` on the way forward, so that the log holds the history it is replayed in and the next run back restores it (the reader's fix of 2026-10-20, the residual's root: the source's increments carried pass 1's remainders into the rewritten history); so a lay the click's write scaled at the birth (`realised`, the log's copies carrying the scaled levels) replays scaled, and every other lay replays as it was, the board's value equal to the line's at the line's turn by the inverse's theorem; a copy of each array written, nothing in place. The host tool reads the lines from the run's output (tools/back_in_time.py), the engine from the books' log (`logged`)."""
    event, when = reports.REPORT_KEYS[0], reports.REPORT_KEYS[2]
    held = [] if log else board.credit.lays.get(board.interval, [])
    own = [
        line
        for line in lines
        if line[event] == reports.LAY
        and line[when] == board.interval
        and not any(line is kept or same_lay(line, kept) for kept in held)
    ]  # a host's line naming a lay the books' log holds is skipped: the loop crosses the log itself (`logged`, `log` True), once, so nothing is crossed twice
    for line in own if direction > 0 else reversed(own):
        index, at = node_of(board, line)
        here = (int(at[0]), int(at[1]), int(at[2]))
        number = int(str(line[reports.LINE]))
        record = board.states[index].lines[number]
        was, after = line[reports.BEFORE], line[reports.AFTER]
        arrays = [np.array(a, copy=True) for a in (record.now, record.before, record.remainder)]
        for array, before_value, after_value in zip(arrays[:2], was[:2], after[:2], strict=True):  # type: ignore[index]
            array[here] += direction * (after_value - before_value)
        if was[2] != after[2]:  # type: ignore[index]  # a lay with an origin: set forward, the history's own back
            if direction > 0:
                line[reports.BEFORE] = [was[0], was[1], int(arrays[2][here])]  # type: ignore[index]
            arrays[2][here] = after[2] if direction > 0 else line[reports.BEFORE][2]  # type: ignore[index]
        board.states[index].lines[number] = Record(arrays[0], arrays[1], arrays[2])


def logged(board: Lattice, direction: int) -> None:
    """The lays the books' log holds at the board's interval, crossed in `direction` (`crossed`; `credit.Books.lays`, filled by `lay.written` where the world's draw runs back): the step at the Nodes alone re-applies them after its Rule3 and the inverse undoes them before its own, so the engine's run back and forward re-present every act from outside the Node from the books; nothing where the log is empty, a world with no record of several parts at declared sides, where the host tool crosses from the lines."""
    crossed(board, board.credit.lays.get(board.interval, []), direction, log=True)
