"""The cone stepped alone (the owner's word of 2026-10-20, only the cone moves and the whole board steps as ever; ALGEBRA.md, The meeting's reading, the run back's reach `cone`; The interval's dependency radius is one Link): in the cone's reach the run back and the run forward of the meeting (`meeting_back.run_back`, `run_forward`) step the record's light cone and nothing else. The box of one step is the ball with one ring of Nodes (`box_of`: back the ball G(t), whose inverse computes the state at t - 1 on it from the neighbours' level before within one Link; forward the ball G(t + 1), one Link larger at the same interval; the bounding box cut to the board, whole on a periodic axis), every family's arrays in it as a view of the lattice (`viewed`, a shallow copy with every NodeState sliced to the box, `sliced`) stepped by the engine's own `Lattice.step` with no act and `Lattice.step_inverse`, which compute per Node what they compute, the view being which arrays they see. The ring and every box Node outside the record's cone are read from the board's own arrays as the reading left them and asserted equal to the record's reference regrown before the step (`held`; frame 0 for a record laid at the start, the board at its birth for a record born during the run, `meeting_back.frame_grown`; never substituted from the reference, which would make the premise's check empty); the computed Nodes outside the cone of the interval arrived at are asserted at frame 0 after it, but the box's edge (`edge_of`, an open face to the engine inside the board, its results discarded); the ball's Nodes are written back into the board's arrays as new arrays beside the old (`written_back`); the rest of the board is neither read nor written. The growths of the receding faces are popped on the way back as the lattice's inverse pops them and read anew on the way forward from the box's own face layer where it is the board's (`grown_at`, `growth.resize`; the write at the birth may move the interval a face is reached); the acts' logs are clipped to the ball (`acts_inside`); the Node-steps are counted per interval (`credit.Books.stepped`; `counted` for the whole-board run of the board's reach); the ball is one distance transform (`features/front.distance_map`). Nothing at the Node: core/ and flux.py untouched, the whole board stepped at its tick by the loop as ever."""

from __future__ import annotations

from dataclasses import astuple
from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe import meeting_back
from event_universe.core.ports import AXES
from event_universe.features.front import distance_map
from event_universe.loader.keys import Node
from event_universe.records import NodeState, Record

if TYPE_CHECKING:
    from event_universe.lattice import Lattice

Box = tuple[
    slice, slice, slice
]  # the box of the cone's step over the board as grown, one slice per axis


def spread(wall: Any, shape: tuple[int, int, int]) -> Any:
    """A wall as an array over the board: the per-Node array as it stands, a scalar wall spread over the shape."""
    found = np.asarray(wall, dtype=object)
    return found if found.shape == shape else np.full(shape, int(found.reshape(-1)[0]), dtype=object)


def extent_of(board: Lattice, box: Box) -> tuple[int, int, int]:
    """The shape of the box over the board as grown, the view's shape."""
    found = [len(range(*s.indices(extent))) for s, extent in zip(box, board.shape, strict=True)]
    return found[0], found[1], found[2]


def distances_of(board: Lattice, box: Box) -> np.ndarray:
    """The Link distance of every Node of the box from the lay's Nodes (`credit.Books.support`, S_0 at the file's coordinates, on the board as grown by the offset), the Link metric with the wrap as the front's shell counts it (`features/front.distance_map`), over the box alone: the box holds the ball with its ring and is whole on a periodic axis (`box_of`), so the distances within it are the board's; the record's light cone at the interval t is the Nodes at distance t + 1 or less (`radius`)."""
    lo = (int(box[0].start), int(box[1].start), int(box[2].start))
    origins = [
        (here[0] - lo[0], here[1] - lo[1], here[2] - lo[2])
        for here in [(int(at[0]), int(at[1]), int(at[2])) for at in board.credit.support]
    ]
    return distance_map(extent_of(board, box), origins, board.world.periodic)


def box_of(board: Lattice, reach: int) -> Box:
    """The box of one step of the cone stepped alone: the bounding box of the ball at `reach` Links with its ring, the Nodes one Link beyond the ball, cut to the board as grown, whole on a periodic axis (the wrap's Link stays the engine's) and on a folded axis of extent 1; the view's arrays are these slices of the board's (`viewed`)."""
    found = []
    for axis, extent in enumerate(board.shape):
        along = [at[axis] for at in board.credit.support]
        if board.world.periodic[axis] or extent == 1:
            found.append(slice(0, extent))
        else:
            found.append(slice(max(0, min(along) - reach - 1), min(extent, max(along) + reach + 2)))
    return found[0], found[1], found[2]


def edge_of(board: Lattice, box: Box) -> np.ndarray:
    """The box's edge over the box: its first and its last layer along each axis where that layer is no face of the board, the Nodes whose Link beyond the box reads the open face's fill in the view (`flux.link_fluxes`) and whose results the step discards; none on a periodic axis, where the box is whole, and none at the board's own faces, where the fill is the lawful one."""
    found = np.zeros(extent_of(board, box), dtype=bool)
    for axis, (along, extent) in enumerate(zip(box, board.shape, strict=True)):
        layer: list[slice] = [slice(None)] * AXES
        if along.start > 0:
            layer[axis] = slice(0, 1)
            found[tuple(layer)] = True
        if along.stop < extent:
            layer[axis] = slice(-1, None)
            found[tuple(layer)] = True
    return found


def sliced(state: NodeState, box: Box) -> NodeState:
    """A family's NodeState over the box alone (ALGEBRA.md, The interval's dependency radius is one Link): every array's slice over the box, a view of the board's array read and never written (the step builds new arrays), the lines, the write remainders and the phase lines."""
    return NodeState(
        [Record(r.now[box], r.before[box], r.remainder[box]) for r in state.lines],
        [array[box] for array in state.write_remainders],
        [[Record(r.now[box], r.before[box], r.remainder[box]) for r in row] for row in state.phases],
    )


def viewed(board: Lattice, box: Box, kept: np.ndarray) -> Lattice:
    """The view the cone's step sees, the lattice's own class over the box (ALGEBRA.md, The meeting's reading, the cone stepped alone; The interval's dependency radius is one Link): a shallow copy of the lattice whose every NodeState is sliced to the box (`sliced`), the shape the box's, the offset the file's coordinates into the box, the wrap's mask of the Nodes beyond the inner faces sliced with it, the world without its receding faces (`growth.grow` reads the whole board's face layers and is not run in the reading, the growths coming from the record's own history, `stepped_alone`), no growth and no observer of its own, the credit's books shared (the lays' and the faces' log); `Lattice.step` and `Lattice.step_inverse` then compute per Node what they compute, the view being which arrays they see. The box's edge inside the board is an open face to the engine, the fill read there, so the edge's results are discarded (`edge_of`, `written_back`), and two readings of the lattice are cut to the box: the mask of a body's Nodes (the cut Links, `meeting.cut`) and the amplitude bound (`Lattice.bounded`), read at the kept Nodes alone, since a face-rule level at the edge is no level of the board."""
    from event_universe.lattice import Lattice as Board  # loaded before this module is used

    class Boxed(Board):
        """The lattice over the box of the cone's step, its two readings cut to the box (`viewed`)."""

        def mask(self, nodes: tuple[Node, ...]) -> np.ndarray:
            """A set of Nodes declared at the file's coordinates over the box: the board's own mask cut to it (the cut Links of a body's region, `meeting.cut`)."""
            return np.asarray(board.mask(nodes)[box])

        def bounded(self, name: str, record: Record, carried: bool = False) -> None:
            """The amplitude bound read at the kept Nodes alone, the lattice's own check on them (`Lattice.bounded`; ALGEBRA.md, The meeting's reading): a face-rule level at the box's edge is no level of the board and its result is discarded; a time line carrying its volume read through the volume's walls (`carried`)."""
            kept_record = Record(record.now[kept], record.before[kept], record.remainder[kept])
            super().bounded(name, kept_record, carried)

    view = Boxed.__new__(Boxed)
    vars(view).update(vars(board))
    view.states = [sliced(state, box) for state in board.states]
    view.fixed_walls = {  # the carried factor's wall per Node, a constant of the lattice, cut to the box with the states
        index: [spread(wall, board.shape)[box] for wall in walls]
        for index, walls in board.fixed_walls.items()
    }
    view.shape = extent_of(board, box)
    view.observers = []
    return view


def at_file(board: Lattice, box: Box, here: list[int]) -> list[int]:
    """A Node of the box at the file's coordinates: the box's start added, the layers grown before the origin taken back (`front.declared`)."""
    return [h + int(s.start) for h, s in zip(here, box, strict=True)]


def differing(
    board: Lattice, view: Lattice, frame: list[NodeState], where: np.ndarray
) -> tuple[str, list[int]] | None:
    """The first array and the first Node of the box at which the view's arrays differ from the record's reference regrown (`frame`, frame 0 for a record laid at the start) among the Nodes `where` names, or None; the Nodes named compared alone, no array copied (the cone's assertions run at every step, `held`)."""
    if not bool(where.any()):
        return None
    nodes = np.argwhere(where)
    for family, after, was in zip(board.families, view.states, frame, strict=True):
        for (label, now), (_label, then) in zip(
            meeting_back.named(family.name, after), meeting_back.named(family.name, was), strict=True
        ):
            bad = np.flatnonzero(np.asarray(now)[where] != np.asarray(then)[where])
            if len(bad):
                return label, [int(i) for i in nodes[bad[0]]]
    return None


def held(
    board: Lattice,
    view: Lattice,
    box: Box,
    frame: list[NodeState],
    where: np.ndarray,
    interval: int,
    edge: bool,
) -> None:
    """One assertion of the cone stepped alone over the box: the view's arrays against the record's reference regrown (`frame`, the box's slices of `credit.Books.regrown`, frame 0 for a record laid at the start and the board at its birth for a record born during the run) at the Nodes `where` names, bit for bit (`first_difference`), refused by name where they differ: at the step's start (`edge`), the ring and every box Node outside the record's cone read from the board's own arrays and found moved, the rest no exact fixed point of the step or an act outside the cone; after the step, a computed Node outside the cone of the interval arrived at not at frame 0 (back, the shell the cone left as it shrank by one Link; forward, the box's Nodes outside the grown ball), the record beyond its cone or the rest moving under the step."""
    found = differing(board, view, frame, where)
    if found is None:
        return
    label, node = found[0], at_file(board, box, found[1])
    if edge:
        raise RuntimeError(
            f"the rest at the record's cone's edge moved at the interval {interval} (the array {label} at the "
            f"Node {node}): the cone needs a laid rest that is an exact fixed point of the step and no act "
            "outside the record's cone; the board's reach, `reach: board`, reads this world"
        )
    raise RuntimeError(
        f"the record's cone did not hold at the interval {interval} (the array {label} at the Node {node}, "
        "computed outside the cone and not at frame 0): the record's levels lie within t Links of the lay "
        "and its remainders within t + 1 by the interval's dependency radius, one Link, on a laid rest that "
        "is an exact fixed point of the step; the board's reach, `reach: board`, reads this world"
    )


def acts_inside(board: Lattice, interval: int, box: Box, kept: np.ndarray) -> None:
    """The acts' logs of `interval` clipped to the box's ball (the lays, `credit.Books.lays`, re-applied or undone by `logged`; the faces, `credit.Books.faces`, presented by `take.faces_presented`, both at the file's coordinates by the view's offset): every act stands at a Node of the ball, and an act at a Node outside it at its interval contradicts the premise (an act on a Node the record never reached cannot have touched the record, and an act of another record there would move the rest), refused by name."""
    books = board.credit
    nodes = [meeting_back.node_of(board, line)[1] for line in books.lays.get(interval, [])]
    nodes += [face.at for face in books.faces.get(interval, [])]
    for at in nodes:
        here = tuple(
            h - int(s.start) for h, s in zip((int(at[0]), int(at[1]), int(at[2])), box, strict=True)
        )
        inside = all(0 <= h < extent for h, extent in zip(here, kept.shape, strict=True))
        if not inside or not bool(kept[here]):
            raise RuntimeError(
                f"an act of the interval {interval} stands at the Node {list(at)} outside the record's cone: "
                "the board's reach reads this world"
            )


def written_back(
    board: Lattice, view: Lattice, box: Box, kept: np.ndarray, before: list[NodeState]
) -> None:
    """The ball's results written back into the board's arrays after one step of the view (ALGEBRA.md, The meeting's reading, the cone stepped alone): per array a new array beside the old (no array of the board is written in place, frame 0 and the frames sharing none), the kept Nodes the view's and every other Node the board's as it stood (frame 0 outside the cone by the assertions, `held`); an array the step left as it was (the same record as `before`, the view's states before the step) kept as it is; the lines, the write remainders and the phase lines alike."""

    whole = all(s.start == 0 and s.stop == e for s, e in zip(box, board.shape, strict=True))
    filled = bool(kept.all())

    def merged(old: np.ndarray, new: np.ndarray) -> np.ndarray:
        if whole and filled:
            return np.asarray(new)
        full = np.array(old, copy=True)
        full[box] = new if filled else np.where(kept, new, full[box])
        return full

    def record(old: Record, new: Record, was: Record) -> Record:
        """One line's three arrays merged (ALGEBRA.md, The meeting's reading): the line as it was where the step left it, the kept Nodes' results beside the board's values otherwise."""
        if new is was:
            return old
        return Record(
            merged(old.now, new.now),
            merged(old.before, new.before),
            merged(old.remainder, new.remainder),
        )

    for state, after, was in zip(board.states, view.states, before, strict=True):
        state.lines = [
            record(o, n, w) for o, n, w in zip(state.lines, after.lines, was.lines, strict=True)
        ]
        state.write_remainders = [
            old if new is was_array else merged(old, new)
            for old, new, was_array in zip(
                state.write_remainders, after.write_remainders, was.write_remainders, strict=True
            )
        ]
        state.phases = [
            [record(o, n, w) for o, n, w in zip(old_row, new_row, was_row, strict=True)]
            for old_row, new_row, was_row in zip(state.phases, after.phases, was.phases, strict=True)
        ]


def copied(board: Lattice) -> list[NodeState]:
    """Every family's NodeState with every array copied, the lines, the write remainders and the phase lines (`dataclasses.astuple`, a deep copy of each line's three arrays): the close the run back takes (`run_back`), read and never written into the board, resized at the return as the board was resized by the growths the run forward found anew (`grown`, `growth.resized`) and compared bit for bit outside the record's cone (`run_forward`, `first_difference`; ALGEBRA.md, The click is the meeting of the future with the past)."""
    return [
        NodeState(
            [Record(*astuple(r)) for r in state.lines],
            [np.asarray(a).copy() for a in state.write_remainders],
            [[Record(*astuple(r)) for r in row] for row in state.phases],
        )
        for state in board.states
    ]


def stepped_alone(board: Lattice, direction: int) -> None:
    """One step of the cone stepped alone, back (-1) or forward (+1) (ALGEBRA.md, The meeting's reading, the run back's reach `cone`; The interval's dependency radius is one Link; the owner's word of 2026-10-20, only the cone moves): forward, the receding faces are read first from the box's own layer where it is the board's face (`grown_at`, `growth.resize` at +1 on the board and frame 0 regrown with it, nothing outside the box read); the box of the step is the ball with its ring (`box_of`: back the ball G(t), whose inverse computes the state at t - 1 on it from the neighbours' level before within one Link; forward the ball G(t + 1), one Link larger at the same interval), every family's arrays in it (`viewed`); the ring and every box Node outside the support G(t) are read from the board's own arrays as the reading left them and asserted equal to frame 0 regrown (`held`), never substituted from it, which would make the premise's check empty; the acts of the interval clipped to the ball (`acts_inside`); the Node-steps counted in the books (`credit.Books.stepped`, the box with its ring, per interval arrived at); then `Lattice.step` with no act or `Lattice.step_inverse` on the view, the engine's own step over the box's arrays; after it every computed Node outside the ball of the interval arrived at but the box's edge (`edge_of`, its results discarded) is asserted at frame 0 (back, the shell G(t) less G(t - 1) returned to the lay's frame as the cone shrinks by one Link per step; forward, the box's Nodes outside G(t + 1), the ball holding the record), the ball's Nodes written back into the board's arrays (`written_back`) and the cone's volume |G| at the interval arrived at, the Nodes within arrived - birth + 1 Links of the birth's Nodes (`meeting_back.radius`'s rule; the reader's F5 of 2026-10-20: a born record's radius counts from its birth, 2 r + 1 on the chain), written into the books (`credit.Books.cone`); back, the growths that served the interval left are popped as `Lattice.step_inverse` pops them and kept on the record's history; the board's interval, passes and heading are the view's, and the observers are called as the lattice calls them; no Node beyond the box is read or written."""
    books, interval = board.credit, board.interval
    arrived = interval + direction
    reach = meeting_back.radius(board) + (1 if direction > 0 else 0)
    box = box_of(board, reach)
    distance = distances_of(board, box)
    kept, live = np.asarray(distance <= reach), np.asarray(distance <= meeting_back.radius(board))
    frame = [sliced(state, box) for state in books.regrown]
    view = viewed(board, box, kept)
    before = [
        NodeState(list(s.lines), list(s.write_remainders), [list(r) for r in s.phases])
        for s in view.states
    ]
    held(board, view, box, frame, ~live, interval, True)
    acts_inside(board, arrived if direction > 0 else interval, box, kept)
    books.stepped[arrived] = books.stepped.get(arrived, 0) + int(np.prod(view.shape))
    if direction > 0:
        view.step(False)
    else:
        view.step_inverse()
    after = np.asarray(distance <= arrived - books.birth + 1)  # |G(arrived)|, the radius from the birth
    held(board, view, box, frame, ~after & ~edge_of(board, box), arrived, False)
    books.cone[arrived] = int(after.sum())
    written_back(board, view, box, kept, before)
    board.interval, board.passes, board.heading = view.interval, view.passes, view.heading
    for observer in board.observers:
        observer(board.interval, direction, board.passes)


def counted(board: Lattice, volume: int) -> None:
    """The Node-steps of one step of the whole-board run written into the books (`credit.Books.stepped`, per interval arrived at): the board's `volume` as the step read it, before a step back that takes a growth's layers off and after a step forward that grows them; the cost the cone stepped alone is read against (the box with its ring, `stepped_alone`)."""
    books = board.credit
    books.stepped[board.interval] = books.stepped.get(board.interval, 0) + volume
