"""The close, the Node's fourth act (ALGEBRA.md, The click writes on the lattice): the readings at the start (every row's rule, the gap-0 plane's share and each record's standing share at the vacuum's weight, the frozen Nodes), the Link close (`meet`: every Link once from its +a end, both ends holding a whole quantum of the record, the + child at the end the record's current flows into where the twist is right-handed, the conjugate pair's selector for a record with a gap, the one-Link read of a number at that end), the lays refused by name (`refuse`), the births taken and laid (`births`: the birth's one take per Node from the gap-0 row, the merger's one take per end from the taken row, SL-S2, every take the one act at a list of ends, merger.takes, CR-S2), the bodies' closing (bodies.py); the lay, the exact take and the momentum they book; the close undone from the log at the direction -1 (`click`). The close's one moment (CL-S2, the owner's word of 2026-10-26, 22:0x UTC by the Boss's clock, the two blind hands' cut): every reading of a record the close LOGS is read at the record's levels at the interval's start (`plane_starts`, kept on the Node as `start_lines`), the sense a credit carries, the levels a credit's frame shows and the momentum a take books at each of its ends, with the cross term of a merger's two moves booked once at the meeting's own Node; the readings the close ACTS on keep their own moment by name, the share's fall and the exact count at a take and the levels a merger takes whole, read on the board the take writes, since a take sized on a level the board no longer holds breaks the law's width; the frame's level before the swap is the one record of the state the swap replaced, read at the turned Nodes alone."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, NamedTuple

import numpy as np

from event_universe import gram, readings
from event_universe.bodies import bodies
from event_universe.core import rule3
from event_universe.core.ports import AXES, across, port_of
from event_universe.core.rule3 import quotient, remainder
from event_universe.draw import read_number
from event_universe.links import factors, row_current, row_twist
from event_universe.merger import child_levels, children_laid, light_levels, summed, takes, walls_of
from event_universe.rows import PLANE, Line, Row
from event_universe.run import birth, refused
from event_universe.take import lay, move, neighbour, recoil

if TYPE_CHECKING:
    from event_universe.node import Node


class Birth(NamedTuple):
    """A birth read at the Link close: the take's Node, the children's record, the - child's Node, the + child's Node, the draw's room and the taken record."""

    at: tuple[int, ...]
    line_pair: int
    minus: tuple[int, ...]
    plus: tuple[int, ...]
    room: int
    rec: int


def list_of(node: Node, rec: int, number: int) -> int:
    """The children's record of a meeting of the record `rec` by the pairs: where the taken row is the emitter the draw's pick among the planes (the number over the unit, modulo their count); where it is another record, the row whose pair is the product (den, den), the emitter (SL-S1: two gapped quanta meeting give light)."""
    records = node.records()
    if records[rec] is not node.emitter():
        return records.index(node.emitter())
    planes = [k for k, r in enumerate(records) if r.shape == PLANE]
    return planes[int(remainder(quotient(number, node.units[rec]), len(planes)))]


def meet(
    node: Node, rec: int, start: list[Line], sh: Any, rules: list[tuple[Line, rule3.Rule]], frozen: Any
) -> list[Birth]:
    """The Link close of one record, the same for every record (SL-S1, the generic close): every Link once from its +a end; a meeting where both ends hold a whole quantum of the record at the interval's start and neither end is frozen (counted as `met`); the + child at the end the record's own current flows into where the twist of its transverse currents is right-handed, at the other end where left-handed (F = 0 and h = 0 refused by name); a record with a gap meets as the conjugate pair alone, the two ends' charges of opposite sign (SL-S2's selector with no name, W_minus W_plus < 0; refused by name `sense` where not), and at rest, no current across the Link, as the pair at rest (MG-S1: the + child at the end whose charge is positive, the birth's orientation read at -1, the twist not read, its number read after the stop in `births`); the Link's one number read at the current's end names the children's record (`list_of`; one read per Node and record in a close). Returns the births as (the take's Node, the children's record, the - child's Node, the + child's Node, the draw's room, the taken record)."""
    born: list[Birth] = []
    row, unit = node.records()[rec], node.units[rec]
    standing = np.vectorize(lambda v: int(v) >= unit, otypes=[bool])(sh) & ~frozen
    currents = [node.den * row_current(start, port_of(axis, 0)) for axis in range(AXES)]
    twists = [row_twist(start, axis) for axis in range(AXES)]
    charges = gram.charge(row.shape, start) if row is not node.emitter() else None
    for axis in range(AXES):
        both = standing & across(standing, port_of(axis, 0))
        for where in zip(*np.nonzero(both), strict=True):
            at = tuple(int(x) for x in where)
            j = neighbour(node, at, port_of(axis, 0))
            node.counts["met"] += 1
            flow, h = int(currents[axis][at]), int(twists[axis][at])
            w = [0, 0] if charges is None else [int(charges[at]), int(charges[j])]
            rest = flow == 0 and w[0] * w[1] < 0
            if (flow == 0 or h == 0) and not rest:
                refused(node, at, "orientation" if flow == 0 else "twist", link=list(j), row=rec)
                continue
            if charges is not None and w[0] * w[1] >= 0:
                refused(node, at, "sense", link=list(j), row=rec, charges=w)
                continue
            if rest:
                into, outof = (at, j) if w[0] > 0 else (j, at)
            else:
                into, outof = (j, at) if flow > 0 else (at, j)
            plus, minus = (into, outof) if rest or h > 0 else (outof, into)
            if rest:
                born.append(Birth(into, list_of(node, rec, 0), minus, plus, 0, rec))
                continue
            if (into, rec) not in node.drawn:
                node.drawn[(into, rec)] = read_number(node, into, rules, unit)
            drawn = node.drawn[(into, rec)]
            if drawn is None:
                continue
            number, room = drawn
            born.append(Birth(into, list_of(node, rec, number), minus, plus, room, rec))
    return born


def refuse(node: Node, born: list[Birth], owns: list[Any]) -> list[Birth]:
    """The lay refused by name: where any of the child's plane already stands at its Node, and where two children of one plane would land at one Node in one close (the charge made at a crowded lay); a merger's light children (the taken record with a gap, the children the gap-0 row) pass both and read their bound on their own quantum at the take, the light's unit at the end as MG-S1's share reads it, the light a sea the merger pays into (the Boss's word of 2026-10-26, 11:33 UTC, 6414995372; the standing-light bound of 4ad484eb9, which ended every merger of the record, kept by name; the birth read at -1, MG-S1). Returns the births kept."""
    records = node.records()
    inverse = [k for k in born if records[k.line_pair] is node.emitter() is not records[k.rec]]
    kept = []
    for at, s, minus, plus, room, rec in [k for k in born if k not in inverse]:
        if int(owns[s][minus]) > 0 or int(owns[s][plus]) > 0:
            refused(node, at, "lay", standing=int(owns[s][minus]), unit=node.units[s], row=rec)
            continue
        kept.append(Birth(at, s, minus, plus, room, rec))
    landing: dict[tuple[int, tuple[int, ...]], int] = {}
    for _at, s, minus, plus, _room, _rec in kept:
        landing[(s, minus)] = landing.get((s, minus), 0) + 1
        landing[(s, plus)] = landing.get((s, plus), 0) + 1
    crowded = [
        k for k in kept if landing[(k.line_pair, k.minus)] > 1 or landing[(k.line_pair, k.plus)] > 1
    ]
    for at, s, minus, plus, _room, rec in crowded:
        refused(
            node, at, "lay", children_at_one_node=max(landing[(s, minus)], landing[(s, plus)]), row=rec
        )
    return [k for k in kept if k not in crowded] + inverse


def births(
    node: Node, kept: list[Birth], c: Any, factors: tuple[Any, ...], reads: list[tuple[Line, rule3.Rule]]
) -> set[tuple[int, ...]]:
    """The births kept, every face read before any write: every child's wall first (`walls_of`, MS-S1: what is taken is what the lay books and nothing made; the rules once per record), then the takes by the taken pair's case, the taken row's line by the fall's sign paying at its rule (take.fall_of's choice, CS4-S2; the former first line kept by name): at the gap 0 one exact take per Node and taken record of its children's walls summed (the birth's case, kept by name); with a gap each child's wall paid at its own end by the record's levels taken whole (MG-S1: the birth read at -1, the share's fall read at the end's Node and its six neighbours, where alone the lay changes it, the standing shares kept per close until a merger writes; the Link's number read at the take's Node after the stop, the draw's refusal counted there); every take the close's one act at a list of ends, read whole before any write (merger.read_ends, write_ends, takes; CR-S2, the owner's word of 2026-10-26, 06:1x UTC; the former take_at, take_line and merger_take kept by name); then each child laid at the charge T div 2 (`children`). Returns every Node a taken birth touched."""
    by_node: dict[tuple[tuple[int, ...], int], list[Birth]] = {}
    for k in kept:
        by_node.setdefault((k.at, k.rec), []).append(k)
    records = node.records()
    rules = {}
    for r in {k.line_pair for k in kept} | {k.rec for k in kept}:
        pair = records[r].pair
        assert pair is not None
        rules[r] = readings.rule(node, pair, c, factors)
    own: dict[tuple[int, int, tuple[int, ...]], int] = {}
    walls = {k: walls_of(node, k.line_pair, k.minus, k.plus, rules[k.line_pair], own) for k in kept}
    taken: list[tuple[tuple[int, ...], int, list[Birth], dict[str, Any]]] = []
    shares: dict[tuple[int, tuple[int, ...]], int] = {}
    for at, rec in sorted(by_node):
        kids = by_node[(at, rec)]
        row, rule = records[rec], rules[rec]
        if row is not node.emitter():
            for kid in kids:
                ends = list(zip((kid.minus, kid.plus), walls[kid], strict=True))
                drawn: list[Any] = []

                def draw(
                    at: tuple[int, ...] = at, unit: int = node.units[rec], into: list[Any] = drawn
                ) -> Any:
                    into.append(read_number(node, at, reads, unit))
                    return into[-1]

                got = takes(node, ends, rule, 1, rec, draw, shares, at)
                if got is None:
                    continue
                taken.append((at, rec, [kid._replace(room=drawn[-1][1])], summed(got)))
                shares.clear()
            continue
        got = takes(node, [(at, sum(sum(walls[kid]) for kid in kids))], rule, len(kids), rec)
        if got is None:
            continue
        node.closes[at] -= 1
        taken.append((at, rec, kids, summed(got)))
    touched: set[tuple[int, ...]] = set()
    for at, rec, kids, take in taken:
        touched |= children(node, at, kids, take, rec, c, factors)
        node.counts["taken"] += take["taken"]
        node.counts["booked"] += take["booked"]
    return touched


def children(
    node: Node,
    at: tuple[int, ...],
    kids: list[Birth],
    take: dict[str, Any],
    rec: int,
    c: Any,
    factors: tuple[Any, ...],
) -> set[tuple[int, ...]]:
    """One take's children laid by the one lay act (merger.children_laid: the charged children at the charge T div 2, a merger's light children as the exact take at -1, merger.light_levels, MG-S1, each end's wall found by its Node and not by its place in the take's list, so the lay is order-free under the ends' naming, the comparison's bug of close.py:166-169, CL-S2), each birth logged with its numbers, its take's own momentum among them (the Boss's 6399718139: every take's dP on its line, not the close's last), a merger's two ends' takes under `takes` and its lays under `exact_lay`. Returns the Nodes touched."""
    touched = {at}
    for _at, s, minus, plus, room, _rec in kids:
        exact: list[list[int] | None] = []
        row = node.records()[s]
        assert row.pair is not None
        if "takes" in take:
            walls = {
                sense: t["booked"]
                for t in take["takes"]
                for sense, where in ((-1, minus), (1, plus))
                if t["node"] == list(where)
            }
            levels_of = light_levels(node, s, walls, readings.rule(node, row.pair, c, factors), exact)
        else:

            def levels_of(_where: tuple[int, ...], sense: int, row: Row = row) -> tuple[int, ...]:
                return child_levels(row, sense, node.A, node.B)

        laid = children_laid(node, s, minus, plus, levels_of)
        touched |= {minus, plus}
        written = [
            recoil(node, where, dp, int(node.start_clock[where]), 1)
            for where, dp in zip((minus, plus), laid[-1], strict=True)
        ]
        node.counts["births"] += 1
        node.closes[at] += 1
        birth(node, at, s, (minus, plus), take, rec, laid, written, len(kids), room, exact)
    return touched


def undo(node: Node, frame: dict[str, Any]) -> None:
    """The click at -1 (X2): the log since the interval's frame read backward, every birth's recoils and lays and every take undone by the same acts at -1, the log cut back and the counters set to the frame's."""
    rec0 = node.records().index(node.emitter())
    unbooked: set[tuple[Any, ...]] = set()
    for entry in reversed(node.log[frame["log_from"] :]):
        at = tuple(entry["node"])
        if entry["event"] == "birth":
            s, (a, b) = entry["line_pair"], entry["amplitude"]
            for where, dp, clock in zip(
                (entry["plus"], entry["minus"]),
                entry["dP_lay_ends"][::-1],
                entry["clock_ends"][::-1],
                strict=True,
            ):
                recoil(node, tuple(where), dp, clock, -1)
            exact = entry.get("exact_lay", [None, None])
            for where, sense, laid in zip((entry["minus"], entry["plus"]), (-1, 1), exact, strict=True):
                if laid is None:
                    lay(node, s, tuple(where), child_levels(node.records()[s], sense, a, b), -1)
                else:
                    move(node, s, laid[0], tuple(where), -laid[1])
            if "cross" in entry:
                cross = entry["cross"]
                recoil(node, tuple(cross["node"]), cross["dP"], cross["clock"], -1)
        if entry["event"] in ("birth", "credit"):
            row = entry.get("taken_row", rec0)
            for take in entry.get("takes", [entry]):
                where = tuple(take["node"])
                if entry["event"] == "credit" or (where, row, at) not in unbooked:
                    unbooked.add((where, row, at))
                    recoil(node, where, take["dP_take"], take["clock"], -1)
                if "taken_levels" in take:
                    lay(node, row, where, tuple(take["taken_levels"]))
                    node.closes[where] += 1
                    continue
                toward = 1 if take["taker"][1] > take["taker"][0] else -1
                count = 0 if "laid_back" in take else toward * take["levels"]
                move(node, row, take["taken_line"], where, -count)
                node.take_rem[where] = take["remainder_was"]
            node.closes[at] -= 1
    del node.log[frame["log_from"] :]
    node.standing, node.crossed, node.beats = frame["counters"]


def click(
    node: Node,
    plane_starts: list[list[Line]],
    held: list[list[Line]],
    direction: int = 1,
    frame: dict[str, Any] | None = None,
) -> None:
    """The click in the direction (X2: the undo is the click at -1): forward the readings at the start (each record's standing share at its unscaled rule in the carrier's unit, PM-S1), the Link close of every record alike (SL-S1), the lays refused by name, the births taken and laid, the bodies' closing; backward the close undone from the log's frame in the reverse order of its lines: the lays removed, a merger's cross term unbooked at the meeting's Node, the taken line moved back by the take's own count at every take's Node (`taken_line`, CS4-S2; the former restore to the level that was, which read a line another lay of the same close had moved and undid that lay twice, struck 2026-10-26 under CL-S2's run back on the fed horizon world; a merger's two ends under `takes`, their levels laid back whole, MG-S1, and its exact lays removed), the take's remainder, the closes at every end and the readings' counters restored (a merger's ends count their close back, left uncounted by the former undo and met by the run back once the state's counters are compared, 2026-10-26) (RW-S1: one function with the direction, the former `unclick` kept by name). `plane_starts` the records' lines at the interval's start, `held` every row's."""
    if direction == -1:
        assert frame is not None
        undo(node, frame)
        return
    c = node.start_content
    node.start_lines = plane_starts
    node.lattices, node.drawn = {}, {}
    frozen = readings.frozen_of(node, c)
    read = factors(node, None, frozen)
    r_emitter = readings.rule_of(node, node.emitter(), c, read)
    rules = node.read_lines(held, c, read)
    owns = []
    for rec, r in enumerate(node.records()):
        assert r.pair is not None
        owns.append(gram.share(node, plane_starts[rec], readings.rule(node, r.pair, c, read)))
    born = [
        b
        for rec in range(len(node.records()))
        for b in meet(node, rec, plane_starts[rec], owns[rec], rules, frozen)
    ]
    born_nodes = births(node, refuse(node, born, owns), c, read, rules)
    bodies(node, plane_starts, owns, born_nodes, frozen, r_emitter)
