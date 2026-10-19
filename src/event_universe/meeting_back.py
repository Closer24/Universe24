"""The meeting that runs back (ALGEBRA.md, The click is the meeting of the future with the past: backward, to the past, the click is a reading and never a write, the credit's reading through the root, which chooses which tree is the past and gives Bell at a distance; the owner's word of 2026-10-19): where the world's draw declares `meeting: back` (`loader/draw.py`), a record of several parts read at N sides is credited by N readings in the time's order in place of the one draw through the root (`lists.readings`, the root's `lists.region`): at the window's close the first side draws at its own place with its own state on its marginal; its realised port runs back along the record to its root, the whole board stepped back by Rule3 at -1 to the record's birth, the lay's interval 0 (`run_back`, `birth_of`), every act from outside the Node re-presented on the way, the faces from the books' log (`twist.faces_presented`) and the lays undone from the books' log of the lay lines (`logged`, `crossed`; `credit.Books.lays`, written by `lay.written`), and forward again to the close by the step at the Nodes alone (`run_forward`, `Lattice.step` with no act, the lays re-applied), bit for bit the board it left, asserted (`snapshot`, `first_difference`); nothing is written at the birth, the board being deterministic forward: each later side draws at its own place with its own state on its conditional from the booked joint with the realised ports fixed (`credit.conditional_of`, the chain rule), the record run back and forward again before each of them, N - 1 runs; the credit's re-weighting of the last side's parts by what the realised ports read (`credit.conditioned`, carried in the books in integers, the levels untouched) is the law's words for its conditional, its one-side share of the re-weighted record (`credit.reweighted_share`) equal to the chain's weights at the last side and at no middle side; the N readings give the one joint distribution, P(p_1) P(p_2 | p_1) ... P(p_N | p_1, ..., p_(N-1)) = J / SUM J exactly in the books' integers; the credit lines the root's with the meeting's word and the order 1 to N; in the cone's reach, the default, the record's light cone asserted after every step back and forward (`asserted`, `credit.Books.reach`); the antisymmetric sign read at other than two sides refused by name at load. The host tool's crossing of the acts from the LATTICE lines (tools/back_in_time.py: `faces_from`, `crossed` from the `face` and `lay` lines) lives here and the tool imports it; the observers' frames of the run back and forward are the lattice's (`Lattice.observers`)."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from event_universe import growth, reports
from event_universe.features import phase
from event_universe.features.click import Face
from event_universe.features.front import ball
from event_universe.loader.draw import CONE
from event_universe.loader.keys import Node
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


def snapshot(board: Lattice, states: list[NodeState] | None = None) -> list[Snapshot]:
    """Every array of every family of the lattice, copied: the board at its interval (or the `states` given, frame 0 grown to the board's shape, `frame_grown`), compared bit for bit after a run back and forward (`first_difference`)."""
    return [
        arrays_of(family.name, state)
        for family, state in zip(board.families, board.states if states is None else states, strict=True)
    ]


def first_difference(
    before: list[Snapshot], after: list[Snapshot], where: np.ndarray | None = None
) -> tuple[str, list[int]] | None:
    """The first array and the first Node at which two snapshots differ, or None where they agree bit for bit (a shape that differs named with no Node); with `where`, a mask over the board, the Nodes it names alone (the outside of the record's cone, `asserted`)."""
    for family_before, family_after in zip(before, after, strict=True):
        for (label, was), (_label, now) in zip(family_before, family_after, strict=True):
            if was.shape != now.shape:
                return f"{label} (the shape {list(now.shape)} against {list(was.shape)})", []
            differing = np.argwhere((was != now) if where is None else (was != now) & where)
            if len(differing):
                return label, [int(i) for i in differing[0]]
    return None


def support_of(board: Lattice) -> tuple[Node, ...]:
    """The lay's Nodes, S_0, the root of the record's light cone (ALGEBRA.md, The meeting's reading, root or back, the run back's reach; the interval's dependency radius is one Link): every Node where a family of quanta holds a level other than 0, now or before, on the board as laid, every record laid at the start among them (the packets' and the bodies'), at the file's coordinates; read once at the books' start (`credit.Books.support`); a kick on a holder of the content laid after the start lies outside S_0, so a back-mode world with a kick meets the run-time refusal in the cone's reach and declares `reach: board`"""
    found = np.zeros(board.shape, dtype=bool)
    for index in board.order:
        for line in board.states[index].lines:
            found |= np.asarray((line.now != 0) | (line.before != 0))
    return tuple(
        (int(at[0]) - board.offset[0], int(at[1]) - board.offset[1], int(at[2]) - board.offset[2])
        for at in np.argwhere(found)
    )


def frame_of(board: Lattice) -> list[NodeState]:
    """Frame 0, the lay's state: every family's NodeState as the start laid it, its lines, its write remainders and its phase lines (immutable records, so no array is copied), kept once at the books' start (`credit.Books.frame`) for the cone's assertion (`asserted`): outside the record's light cone the board stands at frame 0 while the laid rest is an exact fixed point of the step."""
    return [
        NodeState(list(state.lines), list(state.write_remainders), [list(row) for row in state.phases])
        for state in board.states
    ]


def frame_grown(board: Lattice) -> list[NodeState]:
    """Frame 0 over the board as grown: the lay's states (`credit.Books.frame`) grown by every growth standing (`Lattice.growths`, in their order, the layers the receding faces added before the origin and beyond the far face) as the board was grown, every grown Node at the state of a Node with no level (`growth.resized`: the vacuum's levels, the holders' rests, the remainders at their origins, the phase lines at their seed), which is frame 0's beyond the lay."""
    found = (
        frame_of(board)
        if not board.credit.frame
        else [
            NodeState(list(s.lines), list(s.write_remainders), [list(r) for r in s.phases])
            for s in board.credit.frame
        ]
    )
    seed = phase.seed(board.amplitude, board.world.node_clock)
    for _interval, axis, side, layers in board.growths:
        for index, (family, state) in enumerate(zip(board.families, found, strict=True)):
            origin, walls, half = board.origins[index], board.walls(index), board.half_wall(index)
            growth.resized(
                state, family, axis, side, layers, origin, walls, 1, board.world.kind, half, seed
            )
    return found


def radius(board: Lattice) -> int:
    """The record's light cone's radius at the board's interval t, t + 1 Links about the lay's Nodes (ALGEBRA.md, the run back's reach: the levels within t and the remainders within t + 1, a Node with a lit neighbour walking its remainder before its level leaves 0); the frames' `cone_radius`."""
    return board.interval + 1


def cone_of(board: Lattice) -> np.ndarray:
    """The record's light cone at the board's interval, G(t) = S_0 within t + 1 Links in the Link metric with the wrap as the front's shell counts it (`features/front.ball`, `radius`), cut to the board as grown: the mask of the Nodes the record can have reached, every family's arrays inside it (the holders ride along by the law's one-Link dependency radius)."""
    offset = board.offset
    origins = [(at[0] + offset[0], at[1] + offset[1], at[2] + offset[2]) for at in board.credit.support]
    return ball(board.shape, origins, radius(board), board.world.periodic)


def asserted(board: Lattice) -> None:
    """The cone asserted after one step of the run back or forward (ALGEBRA.md, The meeting's reading, root or back, the run back's reach `cone`; the owner's word of 2026-10-19): the cone's volume |G(t)| at the board's interval written into the books (`credit.Books.cone`, the look's header's list), and every array outside the cone compared bit for bit with frame 0 grown to the board (`frame_grown`, `first_difference` on the outside), the locality proved on the engine step by step; a difference refuses the run by name, since the lay's frame stands outside the cone only where the laid rest is an exact fixed point of the step (the start admits a repeat one unit off, a rounding tie), and the board's reach reads such a world."""
    inside = cone_of(board)
    board.credit.cone[board.interval] = int(inside.sum())
    found = first_difference(snapshot(board, frame_grown(board)), snapshot(board), ~inside)
    if found is not None:
        raise RuntimeError(
            f"the rest outside the record's cone moved at the interval {board.interval} (the array {found[0]} at "
            f"the Node {found[1]}): the cone's reach needs a laid rest that is an exact fixed point of the step; "
            "the board's reach reads this world"
        )


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
    """The interval a record of the family `index` was born at, the root the run back reaches: the lay's interval 0 for a record laid at the start, the one birth the loader admits for the meeting that runs back (`loader/draw.meeting_of_the_law`: a record born during the run stands in one part, the act's lays writing the first part's lines, and its lay across the parts is a declaration the law has not made); the births' book, written at the write step for every kind of lay alike with the interval and the Nodes of the lay that raised the count from 0, read here, is a later round's by name (the lay is not taken back: the run back stops at the birth and the lay stands)."""
    assert board.credit.counts[index] > 0  # a record standing in the books, laid at the start
    return 0


def run_back(board: Lattice, to: int) -> list[Snapshot]:
    """The run back from the first close to the record's birth (ALGEBRA.md, The click is the meeting of the future with the past: the backward run from the first click reaches the root): the observers called first with the board at the close as Rule3 left it (the frame of the forward run at the close, before any step back; `Lattice.observers`), the board's every array copied (`snapshot`, the inverse's exactness asserted on the return, `run_forward`), then `Lattice.step_inverse` interval by interval down to `to`, each step undoing the acts' lays of its interval from the books' log and presenting the faces from it, every array returning bit for bit (the inverse's theorem), and in the cone's reach the record's light cone asserted after every step, shrinking by one Link to the lay's Nodes at the birth (`asserted`); returns the copy."""
    board.passes, board.heading = board.passes + (board.heading < 0), 1
    for observer in board.observers:
        observer(board.interval, 1, board.passes)
    kept = snapshot(board)
    while board.interval > to:
        board.step_inverse()
        if board.credit.reach == CONE:
            asserted(board)
    return kept


def run_forward(board: Lattice, to: int, kept: list[Snapshot]) -> None:
    """The run forward from the birth to the close again (ALGEBRA.md, The click is the meeting of the future with the past: the backward run passes the root and continues forward on the partner's tree): `Lattice.step` with no act, interval by interval up to `to`, the step at the Nodes alone with the faces from the books' log and the acts' lays re-applied from it, a computation by Rule3 and no re-presentation of kept frames, in the cone's reach the cone asserted after every step as it grows by one Link (`asserted`), then every array compared bit for bit with the copy the run back took (`kept`, `first_difference`): a difference refuses the run by name, the inverse's theorem being the law's own reason for the exact inverse (the re-weighting touches no array, so the board returns whatever the conditioning)."""
    while board.interval < to:
        board.step(False)
        if board.credit.reach == CONE:
            asserted(board)
    found = first_difference(kept, snapshot(board))
    if found is not None:
        raise RuntimeError(
            f"the run back and forward of the meeting returned to the interval {board.interval} with the array "
            f"{found[0]} differing at the Node {found[1]}: the inverse is exact or the meeting is not read"
        )
