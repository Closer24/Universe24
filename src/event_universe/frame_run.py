"""The frame's run inside the engine, the law's own measurement of a bound body's rate (ALGEBRA.md, The click writes on the lattice (5), CHANGED 2026-10-22, the reader's ruling under the owner's word that the law may change where a derivation needs it: the hazard of a bound body in its upper part is A times the upper level's share, A the power of its two levels beating each at one quantum, read by the law's run of that beat in its well over one period through the near zone's shell, over the transition's quantum): once per bound body, at the first close of its window at which its own-light row falls due (`lists.own_light_weights`; the run reads the declaration and no live line, so its number is the same at whichever close it is made, and it is made there and not at the lay because the copy's run costs the period's steps, 31 and 46 s on the conserve 5-cubes where the shell has no Port on the board and the book reads 0, beyond a test's bound), the body's own well is copied (`copy_world`: the world with the body's row laid beating, the two levels' profiles the frame tool typed under `profiles` summed into the part carrying its count, each at one quantum's charge so the record carries W = T, the other bodies' rows with no draw, no packet, no reader, no draw of the world), the copy is built as a board of its own and stepped one period of the transition's resonance by Rule3 alone (`loader/window.period_of`), and the holder's light through the body's own shell is booked at every step by the very function the live book uses (`reports.shell_outflow` through `reports.booked_light`, a book of the copy's with no draw and no click), the sums per shell Node the frame run's outflow F_k, F = SUM_k F_k floored at 0 the full beat's power over one period in the unit G^2, A's own measure (`full_beat`); beside it the two profiles' charge densities per Node, W_i = re_now im_before - im_now re_before of each level's lay, the sign holder's own read (`densities`), the two levels' shapes the upper level's share of the record is read against; the two kept on the body's books (`FrameRun`, `node_detector.NodeBooks.frame_stream`), no line of the copy reaching the main board but them. The copy is built from the declaration alone and from nothing read off the live board (the reader's condition of 2026-10-22, 06:20): the universe's integers, the world's start shape, boundary and declared largest, the declared bodies' Nodes and counts, the holder's static rows as the declaration sources them (the frozen proton's row from its declared Node, written by the engine's own act on the copy), the mode file's two profiles at one quantum each, the derived shell and period; not the live holder's rows, which carry the body's own wave, and not the grown shape or offset of a receding board at the close; so built, F is a function of the file, the same at every close, and the hour of its computation is bookkeeping and no act. A shell with no Port on the declared board books nothing at any step, so its F is the zeros before any step and the copy is not stepped (the reader's word (2): the declared geometry's reading, the cavity's word on a body at the face). The copy is a measurement and no world; the two one-part rows of the design give way to the one plane's sum because the sign holder's source is the sum of each plane's own Wronskian with no cross term between two parts (`records.wronskian`), so only one plane beats. The engine evaluates no formula: it runs the beat and reads the number; the only numbers of the hand are the two profiles the frame tool typed from Rule3's standing line, the engine having no solver of levels."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, replace
from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe import records, reports
from event_universe.core.rule3 import division_forward
from event_universe.loader.mode import Levels
from event_universe.loader.node_detector_declaration import Transition
from event_universe.loader.window import period_of
from event_universe.loader.world import BodyRow, World
from event_universe.node_detector import NodeBooks

if TYPE_CHECKING:
    from event_universe.lattice import Lattice


@dataclass(frozen=True)
class FrameRun:
    """The frame run's two readings kept on a body's books: the full beat's outflow per shell Node over one period in the unit G^2 (`full_beat`) and per part its level's charge density over the board (`densities`), the body's two profiles as laid at one quantum each."""

    outflow: tuple[int, ...]
    densities: tuple[Any, ...]


def summed(levels: Iterable[Levels]) -> Levels:
    """Several levels over the lattice summed Node by Node, as their nonzero Nodes in x-major order: the two profiles' lay in one plane, the beat the record's shape and no fraction of its quantum."""
    found: dict[int, int] = {}
    for laid in levels:
        for at, level in laid:
            found[at] = found.get(at, 0) + level
    return tuple(sorted((at, level) for at, level in found.items() if level))


def beating(row: BodyRow) -> BodyRow:
    """The body's row laid beating for the copy (ALGEBRA.md, The click writes on the lattice (5); the lay the engine's own, `Lattice.lay`, no write of the hand): the two levels' profiles summed into the part carrying the declared count (`laid_parts` lays the one part with the count; the declaration's counts and not the live books', the copy being the file's), each at one quantum's charge, the record carrying W = T, its declaration with no draw, so that the copy makes no books of it, draws nothing and clicks nothing; its region kept, so the copy lays it as the live body is laid and cuts no Link (`meeting.cut`)."""
    assert row.detector is not None  # a bound body declared through the mode file
    now, before, im_now, im_before = (summed(levels) for levels in zip(*row.profiles, strict=True))
    declaration = replace(row.detector, draw=None)
    return replace(
        row, now=now, before=before, second_now=im_now, second_before=im_before, detector=declaration
    )


def copy_world(world: World, number: int) -> World:
    """The copy's world: the world `world` with the body `number` laid beating (`beating`), every other body's declaration with no draw (no books, no draw and no click on the copy; a body laid in its parts by the engine's own act is laid as on the main board), no packet, no packet laid whole, no reader and no draw of the world; the holder's rows are then the start's under the proton's and the body's own sources, the same well the live world has, the live world's own first period had the body been laid beating."""
    bodies = []
    for n, row in enumerate(world.bodies):
        if n == number:
            bodies.append(beating(row))
        elif row.detector is not None:
            bodies.append(replace(row, detector=replace(row.detector, draw=None)))
        else:
            bodies.append(row)
    return replace(world, bodies=tuple(bodies), packets=(), wholes=(), node_detectors=(), draw=None)


def full_beat(board: Lattice, books: NodeBooks) -> tuple[int, ...]:
    """The full beat's outflow per shell Node over one period on the copy (the frame's run, cost (ii) of the reader's ruling): the copy built as a board of its own from `copy_world` (its start the live start under the beating lay, by the same code), a book of the copy's with the body's shell and zone and no transition appended to its bodies, so that `reports.booked_light` books the shell's outflow at the step's own point, the same as the live book's (inside the reports, before the holder's write), and no draw and no click follow it (no declaration's draw); the copy stepped the period of the transition's resonance (`loader/window.period_of`, the live body's window where it declares no rate) and the book read: F_k per shell Node, outward positive, in the unit G^2, bit for bit the first-window book of a live world laid the same; a shell with no Port on the declared board (`reports.front` of the near zone's ball on the copy at its start, the same geometry the booking reads) books nothing at any step, so its zeros are returned before any step; () for a body with no profiles or no shell (no transition); a copy whose run ends within the period (a receding face reaching its largest) is refused by name, the period's reading having no board."""
    row = board.world.bodies[books.number]
    if not row.profiles or books.zone is None:
        return ()
    transition = books.declared.transitions[0]
    copy = type(board)(copy_world(board.world, books.number), None)
    centre, radius = books.zone
    ball = reports.ball(copy.shape, centre, radius, copy.wrap)  # the copy at its start, the offset 0
    if not any(side.any() for side in reports.front(ball, copy.wrap, ball, copy.declared_board())):
        return (0,) * len(
            books.shell
        )  # no Port on the declared board: nothing books, F the zeros, no step
    declared = replace(books.declared, transitions=(), rates=(), draw=None)
    book = NodeBooks(
        books.number,
        books.index,
        books.record,
        books.nodes,
        books.weights,
        declared,
        next((p for p, c in enumerate(declared.counts) if c), 0),
        list(declared.counts),
        [],
        0,
        [],
        bound=True,
        shell=books.shell,
        zone=books.zone,
    )
    copy.credit.bodies.append(book)
    period = period_of(transition.resonance)
    for _ in range(period):
        copy.step()
        if copy.ended is not None:
            raise RuntimeError(
                f"the frame's run of the body {books.number} ({board.families[books.index].name!r}) ends at the "
                f"interval {copy.interval} before the period {period} of its transition: {copy.ended}; the law's "
                "reading of the full beat has one period on one board; declare the receding face's `largest` "
                "beyond the period's growth or a closed face"
            )
    return tuple(book.light)


def laid(shape: tuple[int, int, int], kind: type, levels: Levels) -> Any:
    """A level over the lattice from its nonzero Nodes, in Python's integers (`Lattice.board_array`'s form, read without a board)."""
    found = records.zeros(shape, kind).reshape(-1).astype(object)
    for at, level in levels:
        found[at] += level
    return found.reshape(shape)


def densities(shape: tuple[int, int, int], kind: type, row: BodyRow) -> tuple[Any, ...]:
    """Per part its level's charge density at every Node from the typed profile, W_i = re_now im_before - im_now re_before (`records.wronskian`, the sign holder's own read of a plane; ALGEBRA.md, The click writes on the lattice (5)), in Python's integers over the declared `shape`, the start's, in the run's `kind`: a reading of the typed levels and no record of the board; () where the body has no profiles."""
    found = []
    for now, before, im_now, im_before in row.profiles:
        re, im = (
            records.Record(laid(shape, kind, a), laid(shape, kind, b), records.zeros(shape, object))
            for a, b in ((now, before), (im_now, im_before))
        )
        found.append(np.asarray(records.wronskian([re, im], True), dtype=object))
    return tuple(found)


def measured(board: Lattice, books: NodeBooks) -> FrameRun:
    """The frame's run of one body, once, at the first close at which its own-light row falls due: its full beat's outflow (`full_beat`) and its two levels' charge densities (`densities`), kept on its books (`NodeBooks.frame_stream`); refused by name where the body's `instrument` declares no `profiles`, the row then having no A to be weighed by (the two levels are the frame tool's, tools/frame_of.py)."""
    row = board.world.bodies[books.number]
    if not row.profiles:
        raise RuntimeError(
            f"the own-light row of the body {books.number} ({board.families[books.index].name!r}) falls due at "
            f"the interval {board.interval} with no `profiles` under its `instrument`: the two levels the frame "
            "tool types, each at one quantum's charge, are the A the row is weighed by; run tools/frame_of.py "
            "on the world"
        )
    return FrameRun(full_beat(board, books), densities(board.world.shape, board.kind, row))


def upper_share(board: Lattice, books: NodeBooks, transition: Transition) -> tuple[int, int]:
    """The upper level's share of the record as the board holds it, rho, as a quotient of integers (numerator, denominator), the one division the weight takes (`hazard`): the record's charge density at every Node, W_i over its planes (`records.wronskian`, the count's own read, standing for a level and invariant under the record's turn at every Node, so that the reading stands at any interval), fitted on the frame run's two level densities (`densities`) by the normal equations: with S_e = SUM_i W_i E_i and S_g = SUM_i W_i G_i against the levels' three Gram sums G_ee, G_eg and G_gg, the upper coefficient over the two coefficients' sum, the determinant cancelled, rho = (G_gg S_e - G_eg S_g) / ((G_gg - G_eg) S_e + (G_ee - G_eg) S_g); the two levels' beat is odd about a symmetric well and enters neither sum, so rho reads 1 on the pure upper level, 1 / 2 on the equal superposition and the upper share of any mix, to the lay's rounding; the record read within the declared board's window on a lattice grown at a receding face (the typed levels stand on the start's board); integers throughout, no division here."""
    stream = books.frame_stream
    assert stream is not None and stream.densities  # the frame's run made (`measured`)
    window = tuple(slice(f, f + e) for f, e in zip(board.offset, board.world.shape, strict=True))
    record = np.asarray(records.wronskian(board.lines_of(books.index, books.record), True), dtype=object)
    record, upper, lower = (
        record[window],
        stream.densities[transition.enters],
        stream.densities[transition.leaves],
    )
    s_e, s_g = int((record * upper).sum()), int((record * lower).sum())
    g_ee, g_eg, g_gg = int((upper * upper).sum()), int((upper * lower).sum()), int((lower * lower).sum())
    return g_gg * s_e - g_eg * s_g, (g_gg - g_eg) * s_e + (g_ee - g_eg) * s_g


def hazard(stream: FrameRun, numerator: int, denominator: int) -> int:
    """The own-light row's weight at a close, A rho in the unit G^2 (ALGEBRA.md, The click writes on the lattice (5), CHANGED 2026-10-22, the reader's ruling): the frame run's F, the full beat's outflow summed over the shell and floored at 0 (a closed board whose walls return the wave within the period reads a cavity's F below 0: the pure level does not decay there, the floor the law's own word on it), times the upper level's share (`upper_share`; the numerator held within [0, denominator], a level's share of a record at most), by one division act, F x num div den, the acts table's row; 0 where no share stands (the denominator 0)."""
    if denominator <= 0:
        return 0
    share = max(0, min(numerator, denominator))
    return int(division_forward(max(sum(stream.outflow), 0) * share, denominator, 0)[0])
