"""The meeting that runs back (ALGEBRA.md, The click is the meeting of the future with the past: backward, to the past, the click is a reading and never a write, the credit's reading through the root, which chooses which tree is the past and gives Bell at a distance; the owner's word of 2026-10-19): where the world's draw declares `meeting: back` (`loader/draw.py`), a record of several parts read at two sides is credited by two readings in the time's order in place of the one draw through the root (`lists.readings`, the root's `lists.region`): at the window's close the first side draws at its own place with its own state on its marginal; its realised port runs back along the record to its root, the whole board stepped back by Rule3 at -1 to the record's birth, the lay's interval 0 (`run_back`, `birth_of`), every act from outside the Node re-presented on the way, the faces from the books' log (`twist.faces_presented`) and the lays undone from the books' log of the lay lines (`logged`, `crossed`; `credit.Books.lays`, written by `lay.written`), and forward again to the close by the step at the Nodes alone (`run_forward`, `Lattice.step` with no act, the lays re-applied), bit for bit the board it left, asserted (`snapshot`, `first_difference`); nothing is written at the birth, the board being deterministic forward: the credit re-weights the partner's parts by what the first port read of them (`credit.conditioned`, carried in the books in integers, the levels untouched) and the partner draws at its own place with its own state on its one-side share of the re-weighted record (`credit.reweighted_share`); the two readings give the one joint distribution, P(A) P(B | A) = P(A, B) exactly in the rationals and in the books' integers; the credit lines the root's with the meeting's word and the order; two sides built, more refused by name at load. The host tool's crossing of the acts from the LATTICE lines (tools/back_in_time.py: `faces_from`, `crossed` from the `face` and `lay` lines) lives here and the tool imports it; the observers' frames of the run back and forward are the lattice's (`Lattice.observers`)."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from event_universe import reports
from event_universe.features.click import Face
from event_universe.records import NodeState, Record

if TYPE_CHECKING:
    from event_universe.lattice import Lattice

Snapshot = list[tuple[str, np.ndarray]]  # every array of one family's NodeState with its name, copied
Lines = list[dict[str, object]]  # output lines, as the lattice's output receives them (`reports.py`)


def arrays_of(name: str, state: NodeState) -> Snapshot:
    """Every array of a family's NodeState with its name, copied: every line's levels now and before and its remainder, every held line's write remainder."""
    found: list[tuple[str, np.ndarray]] = []
    for index, record in enumerate(state.lines):
        found.append((f"lines[{index}].now", record.now))
        found.append((f"lines[{index}].before", record.before))
        found.append((f"lines[{index}].remainder", record.remainder))
    found += [
        (f"write_remainders[{index}]", value) for index, value in enumerate(state.write_remainders)
    ]
    return [(f"{name}.{label}", np.asarray(value).copy()) for label, value in found]


def snapshot(board: Lattice) -> list[Snapshot]:
    """Every array of every family of the lattice, copied: the board at its interval, compared bit for bit after a run back and forward (`first_difference`)."""
    return [
        arrays_of(family.name, state) for family, state in zip(board.families, board.states, strict=True)
    ]


def first_difference(before: list[Snapshot], after: list[Snapshot]) -> tuple[str, list[int]] | None:
    """The first array and the first Node at which two snapshots differ, or None where they agree bit for bit (a shape that differs named with no Node)."""
    for family_before, family_after in zip(before, after, strict=True):
        for (label, was), (_label, now) in zip(family_before, family_after, strict=True):
            if was.shape != now.shape:
                return f"{label} (the shape {list(now.shape)} against {list(was.shape)})", []
            differing = np.argwhere(was != now)
            if len(differing):
                return label, [int(i) for i in differing[0]]
    return None


def node_of(board: Lattice, line: dict[str, object]) -> tuple[int, tuple[int, int, int]]:
    """A LATTICE line's family by its position and its Node at the file's coordinates."""
    names = [family.name for family in board.families]
    at = [int(a) for a in line[reports.LAY_KEYS[3]][reports.AT]]  # type: ignore[index]
    return names.index(str(line[reports.REPORT_KEYS[3]])), (at[0], at[1], at[2])


def faces_from(board: Lattice, lines: Lines) -> None:
    """The faces of a run rebuilt from its `face` lines into the books' log, the log emptied first: per line the family, the line, the Node, the Ports, the interval and the value, so the inverse presents what the lines carry (the host tool's way, tools/back_in_time.py; the engine's own run back presents the books' log whole)."""
    board.credit.faces = {}
    event, when = reports.REPORT_KEYS[0], reports.REPORT_KEYS[2]
    for line in [line for line in lines if line[event] == reports.FACE]:
        index, at = node_of(board, line)
        interval, value = (int(str(line[key])) for key in (when, reports.VALUE))
        ports = tuple(int(str(port)) for port in list(line[reports.PORT_SET]))  # type: ignore[call-overload]
        found = Face(index, int(str(line[reports.LINE])), at, ports, interval, value)
        board.credit.faces.setdefault(interval, []).append(found)


def crossed(board: Lattice, lines: Lines, direction: int = -1) -> None:
    """The lays of the lattice's interval crossed from their `lay` lines (ALGEBRA.md, The click is the meeting of the future with the past: the backward run brings no new number along the realised orbit, the board is reversible, and the lay is not taken back; the mathematician's hand: the face's part crossed by Rule3's inverse, the lay's part from its line): backward (`direction` -1, before the step back, the host tool's way) every line a lay changed at a Node set back to its levels [now, before, remainder] before the lay, the interval's lines in reverse order (two lays on one Node in one interval are two lines, the second's `before` the first's `after`); forward (+1, after the step at the Nodes alone, the run forward of the meeting that runs back) every such line set to its levels after the lay, the lines in their order; every other Node untouched; the same absolute values set twice set once (the tool's crossing and the engine's own on one board agree); the lay act's own values and no new number, the one write site of the engine beside the lay act's write step and Rule3's step."""
    event, when = reports.REPORT_KEYS[0], reports.REPORT_KEYS[2]
    own = [line for line in lines if line[event] == reports.LAY and line[when] == board.interval]
    key = reports.BEFORE if direction < 0 else reports.AFTER
    for line in own if direction > 0 else reversed(own):
        index, at = node_of(board, line)
        here = (at[0] + board.offset[0], at[1] + board.offset[1], at[2] + board.offset[2])
        number = int(str(line[reports.LINE]))
        record = board.states[index].lines[number]
        arrays = [np.array(a, copy=True) for a in (record.now, record.before, record.remainder)]
        for array, value in zip(arrays, line[key], strict=True):  # type: ignore[call-overload]
            array[here] = value
        board.states[index].lines[number] = Record(arrays[0], arrays[1], arrays[2])


def logged(board: Lattice, direction: int) -> None:
    """The lays the books' log holds at the board's interval, crossed in `direction` (`crossed`; `credit.Books.lays`, filled by `lay.written` where the world's draw runs back): the step at the Nodes alone re-applies them after its Rule3 and the inverse undoes them before its own, so the engine's run back and forward re-present every act from outside the Node from the books; nothing where the log is empty, the root's worlds, whose host tool crosses from the lines."""
    crossed(board, board.credit.lays.get(board.interval, []), direction)


def birth_of(board: Lattice, index: int) -> int:
    """The interval a record of the family `index` was born at, the root the run back reaches: the lay's interval 0 for a record laid at the start, the one birth the loader admits for the meeting that runs back (`loader/draw.meeting_of_the_law`); a record born of an emission would read the emitters' book, which holds no interval, a later round's by name (the lay is not taken back: the run back stops at the birth and the lay stands)."""
    assert board.credit.counts[index] > 0  # a record standing in the books, laid at the start
    return 0


def run_back(board: Lattice, to: int) -> list[Snapshot]:
    """The run back from the first close to the record's birth (ALGEBRA.md, The click is the meeting of the future with the past: the backward run from the first click reaches the root): the observers called first with the board at the close as Rule3 left it (the frame of the forward run at the close, before any step back; `Lattice.observers`), the board's every array copied (`snapshot`, the inverse's exactness asserted on the return, `run_forward`), then `Lattice.step_inverse` interval by interval down to `to`, each step undoing the acts' lays of its interval from the books' log and presenting the faces from it, every array returning bit for bit (the inverse's theorem); returns the copy."""
    board.passes, board.heading = board.passes + (board.heading < 0), 1
    for observer in board.observers:
        observer(board.interval, 1, board.passes)
    kept = snapshot(board)
    while board.interval > to:
        board.step_inverse()
    return kept


def run_forward(board: Lattice, to: int, kept: list[Snapshot]) -> None:
    """The run forward from the birth to the close again (ALGEBRA.md, The click is the meeting of the future with the past: the backward run passes the root and continues forward on the partner's tree): `Lattice.step` with no act, interval by interval up to `to`, the step at the Nodes alone with the faces from the books' log and the acts' lays re-applied from it, then every array compared bit for bit with the copy the run back took (`kept`, `first_difference`): a difference refuses the run by name, the inverse's theorem being the law's own reason for the exact inverse (the re-weighting touches no array, so the board returns whatever the conditioning)."""
    while board.interval < to:
        board.step(False)
    found = first_difference(kept, snapshot(board))
    if found is not None:
        raise RuntimeError(
            f"the run back and forward of the meeting returned to the interval {board.interval} with the array "
            f"{found[0]} differing at the Node {found[1]}: the inverse is exact or the meeting is not read"
        )
