"""The board stepped in slabs by several processes with one-Link halos (the owner's word of 2026-10-24, everything local and fast, the Node steps simply with Rule3 and the click produces everything; the architect's design, rank 9 and section 7: every act of the interval reads the Node and its six Links at the interval's start, so a slab of layers along one axis with its two neighbouring layers as halos steps its own Nodes by the same Rule3 to the same integers): the board is cut along its longest axis into as many slabs as the axis has layers and the machine has cores, the fewer of the two (`slabs_of`; the count is the machine's and the board's, no file's and no law's number, and every count gives the same integers, the gate), one process forked per slab (`Slabs`, `served`), each holding a lattice over its layers and the two halo layers (`tile_of`, the state taken from the one board at the fork); every interval the parent sends each process its two halo layers as the board holds them at the interval's start, the process writes them onto its lattice (`imposed`, `rebuilt`), steps it with every act (`Lattice.step`) and sends back every array of its own layers (`arrays_of`, `layers_of`), its output lines moved to the board's frame with the key of their place in the board's order (`in_the_boards_frame`), the Nodes the fifth act turned among its own layers (`Lattice.turned`) or its refusal by name; the parent writes the returned layers onto the one board, so the board's state is the single process's bit for bit and every reading over it (tools/eras.py, the eras and the nodes lines) is the same reading, gives the output lines in the board's order (`in_the_boards_order`: the close walks the Nodes in x-major order within each of its three writes, the holes' lays, the children's lays, then the credit and birth lines, so the lines sort by their write and their Node) and logs the lays in the books as the lay act does, so the run back from the board is the single process's. The acts of the interval and what each writes beyond its Node: none writes beyond it; Rule3's step and the held write land at the Node, the hole and the born children's lays at the meeting Node (`meeting_board.closed`, `lay.laid` at the Node's own mask), the swap's exchange and complement of every line, write remainder and phase line at the turned Node (`swap.swapped`, `swap.swapped_phases`: a Link's phase pair is held at the Node of its +a Port and the far end reads it through the halo), so what crosses a slab's face is read alone, through the halo at the interval's start, and no write is routed back. A refusal in a slab is tried on the board: the halo layers' own step reads the slab's wrap in place of the true neighbour, so a slab may refuse by the amplitude bound or a reading where the board does not; the parent then steps the board itself from the same start, the board's refusal or the interval's integers are the verdict, and every slab is re-imposed whole at the next interval. When a point's records and sign rows are born at the point's first lay and nothing is allocated before (the lean board), the exchange carries the board's record set with the halos: each slab reports the points born in its own layers this interval, the parent keeps their union in the board's birth order and sends it with the halo layers, a slab lacking a record births it at the vacuum before imposing the halo's arrays (the neighbour's lay crossing the face is the record's birth on this side, at the same interval), and a record that a halo layer's own step born and the board did not is struck, so both sides hold one record set and the arrays travel keyed by the record and its line and not by their position."""

from __future__ import annotations

import os
from collections.abc import Iterator
from dataclasses import replace
from multiprocessing.connection import Connection
from multiprocessing.context import ForkContext
from multiprocessing.process import BaseProcess
from typing import TYPE_CHECKING, Any, cast

import numpy as np

from event_universe import credit, records
from event_universe.core.rule3 import division_forward
from event_universe.lattice import Lattice
from event_universe.reports import AT, CREDIT, LAY, LAY_KEYS, NODES, READINGS, REPORT_KEYS

if TYPE_CHECKING:
    from event_universe.loader.keys import Node

Line = dict[str, object]
Keyed = tuple[tuple[int, int], Line]  # a line with its place in the board's order: the write, the Node
Answer = tuple[
    bool, Any, Any, Any
]  # a slab's answer for an interval: True with its layers, its lines and its turned count, or False with its refusal's kind and words


def axis_of(shape: Node) -> int:
    """The board's longest axis, the first of equals: the slabs are cut across it."""
    return max(range(len(shape)), key=lambda axis: shape[axis])


def slabs_of(extent: int, cores: int) -> list[range]:
    """The layers of an axis of `extent` cut into as many slabs as the axis has layers and the machine has cores, the fewer, each a range of layers, the first slabs one layer longer where the division leaves a remainder: the count the machine's and the board's, every count the same integers."""
    count = max(1, min(extent, cores))
    each, longer = division_forward(extent, count, 0)
    found, start = [], 0
    for number in range(count):
        stop = start + int(each) + (number < longer)
        found.append(range(start, stop))
        start = stop
    return found


def wrapped(layer: int, extent: int) -> int:
    """A layer's index on the torus, the division act's remainder by the axis's extent."""
    return int(division_forward(layer, extent, 0)[1])


def arrays_of(board: Lattice) -> list[Any]:
    """Every array over the Nodes a lattice's state holds, in one fixed order (`rebuilt` reads the same): per family every line's two levels and remainder, the write remainders and every phase line's three arrays, then the time count and the closes."""
    found: list[Any] = []
    for state in board.states:
        for line in state.lines:
            found += [line.now, line.before, line.remainder]
        found += list(state.write_remainders)
        for row in state.phases:
            for line in row:
                found += [line.now, line.before, line.remainder]
    return found + [board.proper_count, board.closes]


def rebuilt(board: Lattice, arrays: list[Any]) -> None:
    """The lattice's state set from arrays in the order of `arrays_of`, every record a new one (an act replaces a record and never writes one in place: the reads memoized on the records stand on the objects)."""
    given: Iterator[Any] = iter(arrays)

    def record() -> records.Record:
        return records.Record(next(given), next(given), next(given))

    for state in board.states:
        state.lines = [record() for _ in state.lines]
        state.write_remainders = [next(given) for _ in state.write_remainders]
        state.phases = [[record() for _ in row] for row in state.phases]
    board.proper_count, board.closes = next(given), next(given)


def selection(axis: int, layers: list[int]) -> tuple[Any, ...]:
    """The index that names some layers of an array along one axis."""
    return (slice(None),) * axis + (list(layers),)


def layers_of(arrays: list[Any], axis: int, layers: list[int]) -> list[Any]:
    """Some layers of every array along one axis, each a copy, in the layers' order."""
    where = selection(axis, layers)
    return [np.asarray(array)[where] for array in arrays]


def imposed(arrays: list[Any], axis: int, layers: list[int], pieces: list[Any]) -> list[Any]:
    """Every array with some of its layers along one axis replaced by the pieces given, each a new array."""
    where, found = selection(axis, layers), []
    for array, piece in zip(arrays, pieces, strict=True):
        copy = np.array(array, copy=True)
        copy[where] = piece
        found.append(copy)
    return found


def tile_layers(slab: range, extent: int) -> list[int]:
    """The board's layers a slab's lattice holds, in the lattice's order: the halo before, the slab's own layers, the halo after, on the torus."""
    return [wrapped(slab.start - 1, extent), *slab, wrapped(slab.stop, extent)]


def tile_of(board: Lattice, axis: int, slab: range) -> Lattice:
    """A slab's lattice: the board's world over the slab's layers and its two halos, every array over the Nodes and the fixed walls taken from the board's layers, the board's clocks, its origins and its amplitude; its own books (the counts and the births' book are readings, no act's input)."""
    extent, shape = board.shape[axis], list(board.shape)
    shape[axis] = len(slab) + 2
    tile = Lattice(replace(board.world, shape=(shape[0], shape[1], shape[2])))
    layers = tile_layers(slab, extent)
    rebuilt(tile, layers_of(arrays_of(board), axis, layers))
    where = selection(axis, layers)
    tile.fixed_walls = {
        index: [np.asarray(wall)[where] if np.shape(wall) == board.shape else wall for wall in walls]
        for index, walls in board.fixed_walls.items()
    }
    tile.origins, tile.laid, tile.amplitude = list(board.origins), dict(board.laid), board.amplitude
    tile.interval, tile.tick, tile.passes, tile.heading = (
        board.interval,
        board.tick,
        board.passes,
        board.heading,
    )
    return tile


def in_the_boards_frame(
    line: Line, axis: int, slab: range, shape: Node, tile: Node, seed: str | None
) -> Keyed | None:
    """An output line of a slab's lattice moved to the board's frame: its Node's coordinate along the slabs' axis from the lattice's layer to the board's (the credit line's x-major index and its support, the birth line's Nodes, the lay line's Node), with the key of its place in the board's order, the close's write (0 the holes' lays of the seed family, 1 the children's lays, 2 the credit and birth lines) and the Node's x-major index on the board; None for a line at a halo Node, which the slab owning the Node writes."""
    extent = shape[axis]

    def moved(node: list[int]) -> list[int] | None:
        found = [int(c) for c in node]
        if found[axis] == 0 or found[axis] == tile[axis] - 1:
            return None
        found[axis] = wrapped(slab.start + found[axis] - 1, extent)
        return found

    event, family = str(line[REPORT_KEYS[0]]), str(line[REPORT_KEYS[3]])
    if event == LAY:
        written = cast(dict[str, object], line[LAY_KEYS[3]])
        at = moved(cast(list[int], written[AT]))
        if at is None:
            return None
        line[LAY_KEYS[3]] = {**written, AT: at}
        return (0 if family == seed else 1, int(np.ravel_multi_index(at, shape))), line
    if event == CREDIT:
        place = np.unravel_index(int(str(line[REPORT_KEYS[-1]])), tile)
        at = moved([int(c) for c in place])
        if at is None:
            return None
        line[REPORT_KEYS[-1]], line[READINGS[3]] = int(np.ravel_multi_index(at, shape)), at
        return (2, int(np.ravel_multi_index(at, shape))), line
    nodes = [moved(node) for node in cast(list[list[int]], line[NODES])]
    if nodes[0] is None:
        return None
    line[NODES] = nodes
    return (2, int(np.ravel_multi_index(nodes[0], shape))), line


def in_the_boards_order(answers: list[Answer]) -> list[Line]:
    """The slabs' output lines of one interval in the board's order, by their keys (the close's write, then the Node's x-major index; within a Node the slab's own order stands)."""
    keyed: list[Keyed] = [pair for answer in answers for pair in answer[2]]
    return [line for _key, line in sorted(keyed, key=lambda pair: pair[0])]


def served(board: Lattice, axis: int, slab: range, pipe: Connection) -> None:
    """One slab's process: its lattice made from the board at the fork, then per interval the layers the parent names imposed with the board's clocks, the lattice stepped with every act, and the answer sent, its own layers' arrays with its lines in the board's frame and its count of turned Nodes, or its refusal by name; None ends it."""
    tile, lines, shape = tile_of(board, axis, slab), list[Line](), board.shape
    tile.output = lines.append
    seed = board.families[board.world.seed].name if board.world.seed is not None else None
    own = list(range(1, len(slab) + 1))
    while (message := pipe.recv()) is not None:
        layers, pieces, interval, tick = message
        rebuilt(tile, imposed(arrays_of(tile), axis, layers, pieces))
        tile.interval, tile.tick = interval, tick
        lines.clear()
        try:
            tile.step()
        except (ValueError, RuntimeError) as refusal:
            pipe.send((False, type(refusal).__name__, str(refusal), None))
            continue
        moved = [in_the_boards_frame(line, axis, slab, shape, tile.shape, seed) for line in lines]
        turned = int(np.asarray(tile.turned)[selection(axis, own)].sum())
        pipe.send((True, layers_of(arrays_of(tile), axis, own), [m for m in moved if m], turned))


class Slabs:
    """The board stepped by slabs in processes (the module's sentence): the slabs along the longest axis, the count the fewer of the axis's layers and the machine's cores (`processes` where a caller names the count, the tests of the gate), one process per slab forked from the board at the call; `advanced` is one interval of the board with every act, the same integers and the same lines as `Lattice.step` (the step's act list is the lattice's one list, so the runner's interval bears another name); `close` ends the processes."""

    def __init__(self, board: Lattice, processes: int | None = None) -> None:
        self.board, self.axis = board, axis_of(board.shape)
        cores = processes if processes is not None else os.process_cpu_count() or 1
        self.slabs = slabs_of(board.shape[self.axis], cores)
        self.whole = False  # every slab re-imposed whole at the next interval, after a refusal tried
        self.pipes: list[Connection] = []
        self.processes: list[BaseProcess] = []
        if len(self.slabs) == 1:
            return  # one slab is the board: the single process steps it, nothing forked
        context = (
            ForkContext()
        )  # the fork: the slabs' lattices made from the board in the parent's memory
        for slab in self.slabs:
            parent, child = context.Pipe()
            process = context.Process(target=served, args=(board, self.axis, slab, child), daemon=True)
            process.start()
            child.close()
            self.pipes.append(parent)
            self.processes.append(process)

    @property
    def count(self) -> int:
        """The slabs' count, the processes' where above one."""
        return len(self.slabs)

    def advanced(self) -> None:
        """One interval of the board through the slabs: the halo layers (or every layer after a refusal tried) sent to every slab, the answers gathered, the slabs' layers written onto the board, the board's clocks advanced as `Lattice.step` advances them, the swaps' count logged, the lines given in the board's order and the lays logged in the books, the seed's count read, the observers called; a refusal in any slab tried on the board itself; the one slab stepped by the board itself."""
        board, extent = self.board, self.board.shape[self.axis]
        if not self.pipes:
            board.step()
            return
        arrays = arrays_of(board)
        for slab, pipe in zip(self.slabs, self.pipes, strict=True):
            layers = tile_layers(slab, extent)
            kept = list(range(len(layers))) if self.whole else [0, len(layers) - 1]
            pieces = layers_of(arrays, self.axis, [layers[k] for k in kept])
            pipe.send((kept, pieces, board.interval, board.tick))
        answers: list[Answer] = [pipe.recv() for pipe in self.pipes]
        self.whole = any(not answer[0] for answer in answers)
        if self.whole:
            board.step()
            return
        for slab, answer in zip(self.slabs, answers, strict=True):
            arrays = imposed(arrays, self.axis, list(slab), answer[1])
        rebuilt(board, arrays)
        board.interval, board.tick = board.interval + 1, board.tick + 1
        turned = sum(int(answer[3]) for answer in answers)
        if turned:
            board.swaps.append((board.interval, 1, turned))
        for line in in_the_boards_order(answers):
            if board.output is not None:
                board.output(line)
            if line[REPORT_KEYS[0]] == LAY:
                board.credit.lays.setdefault(board.interval, []).append(line)
        if board.world.seed is not None:
            counted = credit.count_of(board, board.world.seed)
            if counted is not None:
                board.credit.counts[board.world.seed] = counted
        board.passes, board.heading = board.passes + (board.heading < 0), 1
        for observer in board.observers:
            observer(board.interval, 1, board.passes)

    def close(self) -> None:
        """The processes ended and joined."""
        for pipe in self.pipes:
            pipe.send(None)
        for process, pipe in zip(self.processes, self.pipes, strict=True):
            process.join()
            pipe.close()
        self.pipes, self.processes = [], []
