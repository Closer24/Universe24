"""The window derived from the record's declared passage (the atom branch, 2026-10-19, the owner's decision with the cold reader's changes; ALGEBRA.md, The click writes on the lattice, C2: the window is the lay's passage derived at load, as the unit is derived from the pair, and no reading of the board, which shows a passing record no end a detector can read without a threshold, a wake of 2 to 7 levels standing for hundreds of intervals on every Node the record crossed, the reader's finding): a body's window is the longest passage over it of the lays, with an end, of the families its transitions read, every lay of the family on the board whoever lays it, the body's own rate among them: a packet laid along an axis (L = top + 2 edge Nodes, `packet_passage`), an emitted packet (a rate with a `width`, L the slices of its train, the length `node_detector_declaration.packet_form` holds the board to) and a source in time (a rate without one, the train's own duration, the span tau, `rate_passage`); a lay with no end (a wave filling a periodic ring, a source in time on a periodic board) or no lay at all leaves the window the declaration's, the instrument's cadence, the key required, and the key on a body whose drives' lays all have an end is refused by name with the derived W (`windowed`, the one place the key is decided). One code path for every axis and either direction, the pace by |sin k| (the group of 48 of the cube): a lay of L Nodes along its axis passes a body of b Nodes there in W = ceil((L + b - 1) / v_g) intervals at the band's group pace v_g = (num / den) sin k / (3 sin omega) of the lay's whole wave, the three axes' wave numbers (a width's transverse mode among them), in the loader's integers (`passage`)."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import replace
from typing import TYPE_CHECKING

from event_universe.core.rule3 import division_forward, largest_below
from event_universe.features.click import along_cosine, envelope, line_total, wave_cosine
from event_universe.loader.derived import FamilyRule
from event_universe.loader.draw import Draw
from event_universe.loader.faces import extent_across
from event_universe.loader.keys import Node
from event_universe.loader.node_detector_declaration import Rate
from event_universe.loader.packets import PacketRow, axes_waves

if TYPE_CHECKING:
    from event_universe.loader.world import BodyRow

Wrap = tuple[bool, ...]  # which axes wrap, the world's periodic tuple


def passage(
    length: int,
    axis: int,
    cosines: list[int],
    pair: tuple[int, int],
    nodes: tuple[Node, ...],
    shape: Node,
    periodic: Wrap,
) -> int | None:
    """The intervals a lay of `length` Nodes along `axis` takes to pass the body at `nodes`, ceil((L + b - 1) / v_g), b the body's extent along the axis (`faces.extent_across`, through the wrap on a periodic axis) and v_g = (num / den) sin k / (3 sin omega) the band's group pace of the lay's wave: `cosines` den cos k_a on the three axes by the rotation act's search (`features/click.wave_cosine`), den cos omega = (num SUM_a den cos k_a) div (3 den) the band's line as the record's unit reads it (`emission.packet_unit`; the massless family at num = den, a gapped one by its pair), the sines by the search, so W = ceil(3 den (L + b - 1) sin omega / (|num| sin k)) by the division act with the carry; |sin k| alone enters, so the opposite direction and every reflection of the lay give one W; None where the lay has no end: a lay filling a periodic ring, or one that does not move (sin k = 0 at the band's edge, a frozen pair)."""
    num, den = pair
    if periodic[axis] and length >= shape[axis]:
        return None
    omega = int(division_forward(num * sum(cosines), 3 * den, 0)[0])
    sine = largest_below(den * den - omega * omega)
    pace = abs(num) * largest_below(den * den - cosines[axis] * cosines[axis])
    if pace == 0:
        return None
    extent = extent_across([node[axis] for node in nodes], shape[axis], periodic[axis])
    return int(division_forward(3 * den * (length + extent - 1) * sine, pace, pace - 1)[0])


def packet_passage(
    packet: PacketRow,
    families: tuple[FamilyRule, ...],
    nodes: tuple[Node, ...],
    shape: Node,
    periodic: Wrap,
) -> int | None:
    """A laid packet's passage over the body (`passage`): L = top + 2 edge Nodes along its axis, its wave on the three axes the packet's `wave` and `transverse` pairs (`packets.axes_waves`)."""
    family, axis = families[packet.family], packet.along
    first, last = packet.top[axis]
    length = last - first + 1 + 2 * packet.edge[axis]
    cosines = [wave_cosine(turns, halves, family.pair[1]) for turns, halves in axes_waves(packet)]
    return passage(length, axis, cosines, family.pair, nodes, shape, periodic)


def rate_passage(
    rate: Rate, light: FamilyRule, nodes: tuple[Node, ...], shape: Node, periodic: Wrap, action: int
) -> int | None:
    """An emission's passage over the body (`passage`): a rate without a `width`, the source in time, the train's own duration, its lifetime, and no end on a board with a periodic axis above one Node (the resonance folder's ring); a rate with one, the open board's packet, the train of L slices the lay holds the board to (`features/click.envelope` on the one-line root at the lifetime, `node_detector_declaration.packet_form`) at its wave along the drawn axis (`features/click.along_cosine`, the band's line with the width's lowest transverse mode on the two axes across, `wave_cosine` at [1, width + 1]), the longest over the directions the board holds (`Rate.directions`, the body's extent along each), none where any has no end."""
    if rate.width is None:
        endless = any(wraps and extent > 1 for wraps, extent in zip(periodic, shape, strict=True))
        return None if endless else rate.lifetime
    den = light.pair[1]
    doubled = along_cosine(light.pair, rate.resonance, rate.width, den)
    assert doubled is not None  # the loader admitted the width (`packet_form`)
    along, across = int(division_forward(doubled, 2, 0)[0]), wave_cosine(1, rate.width + 1, den)
    length = len(envelope(line_total(action, rate.resonance), rate.lifetime, rate.width * rate.width))
    cosines = {
        axis: [along if a == axis else across for a in range(len(shape))] for axis, _ in rate.directions
    }
    return longest(
        passage(length, axis, found, light.pair, nodes, shape, periodic)
        for axis, found in cosines.items()
    )


def longest(passages: Iterable[int | None]) -> int | None:
    """The longest of a drive's lays' passages, the body's one window length (the law's line; the per-lay window read at the opening from the books' sources is the refinement named and not built); None where a lay has no end or none is laid: the declaration's window then."""
    found = list(passages)
    return None if not found or None in found else max(p for p in found if p is not None)


def windowed(
    bodies: tuple[BodyRow, ...],
    packets: tuple[PacketRow, ...],
    families: tuple[FamilyRule, ...],
    shape: Node,
    periodic: Wrap,
    action: int,
) -> tuple[BodyRow, ...]:
    """Every body's window as the rule derives it at the end of the load, the one place the key `window` of a body's `node_detector` is decided (`draw.body_draw_of`): for a body with a draw and no probe (a probe's window is bounded by the probe's lays, `draw.generator_of`), the lays of every family its transitions read, the world's packets of the family (`packet_passage`) and every body's rates giving to it (`rate_passage`), the body's own among them; every lay with an end: the longest passage is the window (`longest`), the generator with it the body's `Draw`, and a declared key is refused by name with the body, its drives and the derived W; any lay with no end, or none: the declared key kept and its absence refused by name; a body without a draw, a record converted whole (its window its table's), a region and the world's draw untouched."""
    rates = [rate for row in bodies if row.detector is not None for rate in row.detector.rates]
    found = []
    for number, row in enumerate(bodies):
        kind = row.detector
        if kind is None or kind.draw is None or any(t.leaves == t.enters for t in kind.transitions):
            found.append(row)
            continue
        drives = sorted({transition.drive for transition in kind.transitions})
        lays = [
            packet_passage(p, families, row.nodes, shape, periodic)
            for p in packets
            if p.family in drives
        ]
        lays += [
            rate_passage(r, families[r.light], row.nodes, shape, periodic, action)
            for r in rates
            if r.light in drives
        ]
        window, names = longest(lays), [families[drive].name for drive in drives]
        label = f"bodies[{number}].node_detector"
        if isinstance(kind.draw, Draw):
            if window is not None:
                raise ValueError(
                    f"{label} declares the window {kind.draw.window}, and the lays of its drives {names} on this "
                    f"board all have an end: the window is their passage over the body, derived at load, W = "
                    f"{window} here; remove the key (ALGEBRA.md, The click writes on the lattice, C2)"
                )
            found.append(row)
            continue
        if window is None:
            raise ValueError(
                f"{label} declares no window, and a lay of its drives {names} on this board has no end (a wave "
                "filling a periodic ring, a source in time on a periodic board) or none is laid: such a body "
                "declares its window, the instrument's cadence (ALGEBRA.md, The click writes on the lattice, C2)"
            )
        draw = Draw(kind.draw.seed, kind.draw.multiplier, kind.draw.increment, window)
        found.append(replace(row, detector=replace(kind, draw=draw)))
    return tuple(found)
