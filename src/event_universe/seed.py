"""The seed as the world file lays it: a list of lays in the four forms of the law (the owner's word of 2026-10-25; the fourth, the uniform lay, by his word of 17:57 UTC): `sea` lays the plane at the gap 0's drift v, the largest integer with v^2 <= T, at every Node; `hole` takes it back at one Node; `at` lays a packet, on the plane at the gap 0 N drifts at the centre, on a record with a gap the conjugate pair over the raised cosine's envelope of the half-width 2 or 3, at rest or, with the field `wave` [h_x, h_y, h_z] in den's unit (h_a = den sin(k_a / 2)), moving at the band's rotation at that wave number with the optional flat `top` along the wave's axis (MV-S1 to MV-S3, 2026-10-25; one path for every record row, the plane at the gap 0 with a wave among them, with none the drift by name; a quartet's lay names its `vector`, the eight integers of the lattice, and may name one `sense`; the lay refused by state where the standing row's spin density agrees with the child's at the centre, SR-S4). Refused by name: a fourth form, a field of no form (an interval key among them), a lay onto a row of no record shape, a sea of a record with a gap, a Node off the board, a packet of another width, a quartet's lay with no vector, a wave number beyond the band's edge (|h| above den), a massless packet at the wave 0, a top not fitting the board."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe import gram
from event_universe.core.paces import odd_rounded, sine_den
from event_universe.core.ports import AXES, wrap
from event_universe.core.rule3 import largest_below, quotient, remainder
from event_universe.links import turn_pair
from event_universe.rows import CARRIER, PLANE, Line, Row, zeros

if TYPE_CHECKING:
    from event_universe.node import Node

FIELDS = {  # the fields of each form of the law; a field of no form is refused by name (MV-S3)
    "sea": frozenset({"lay", "row", "quanta", "sense"}),
    "hole": frozenset({"lay", "at"}),
    "at": frozenset({"lay", "row", "centre", "quanta", "width", "vector", "sense", "wave", "top"}),
}
Pair = tuple[Any, Any]


def lay_world(node: Node, lays: list[dict[str, Any]]) -> None:
    """Every lay of the world file onto the Node's rows, the packets after the sea and the holes; a lay of no form and a field of no form refused by name (MV-S3: the loader lays the seed before the first interval and nothing after)."""
    packets = []
    for lay in lays:
        form = lay.get("lay")
        if form not in FIELDS:
            raise ValueError(f"a lay of no form of the law: {form!r}")
        beyond = sorted(set(lay) - FIELDS[form])
        if beyond:
            raise ValueError(f"a field of no form of the law in the lay {form!r}: {', '.join(beyond)}")
        row = node.by_index[int(lay["row"])] if "row" in lay else None
        if row is not None and row not in node.records():
            raise ValueError("a lay is onto a record (a plane or a quartet)")
        if form == "sea" and "quanta" not in lay:
            if row is None or row.gap != 0 or "sense" in lay:
                raise ValueError(
                    "a sea without a count is the plane at the gap 0 alone (the drift, no sense); a plane with a gap names its quanta (the fourth form)"
                )
            node.lay(node.records().index(row), Ellipsis, (node.drift, 0, 0, 0))
        elif form == "sea":
            if row is None or row.gap == 0:
                raise ValueError(
                    "the fourth form lays a plane with a gap at a count: the plane at the gap 0 alone is the drift"
                )
            lay_uniform(node, node.records().index(row), int(lay["quanta"]), int(lay.get("sense", 0)))
        elif form == "hole":
            at = node.node_of(lay["at"])
            node.lay(node.records().index(node.row(PLANE, gap=0)), at, (-node.drift, 0, 0, 0))
        else:
            n = int(lay["quanta"])
            at = node.node_of(lay["centre"])
            if row is None:
                raise ValueError("a packet names its row")
            wave = None if lay.get("wave") is None else tuple(int(x) for x in lay["wave"])
            if row.gap == 0 and wave is None:
                node.lay(node.records().index(row), at, (n * node.drift, 0, 0, 0))
            else:
                vector = lay.get("vector")
                if (vector is None) != (row.shape == PLANE):
                    raise ValueError("a quartet's lay names its vector, a plane's names none")
                packets.append(
                    (
                        node.records().index(row),
                        at,
                        int(lay.get("width", 0)),
                        n,
                        vector,
                        lay.get("sense"),
                        wave,
                        int(lay.get("top", 1)),
                    )
                )
    for rec, at, h, n, vector, sense, wave, top in packets:
        lay_packet(node, rec, at, h, n, vector, sense, wave, top)


def raised_cosine(h: int) -> tuple[int, ...]:
    """The raised cosine's weights over the half-width h, w_k = 2 + 2 cos(pi k / h) for k = 0 .. h - 1, exact in integers where 2 cos(pi / h) is an integer, at h = 2 (0) and h = 3 (1) and at no other width: the doubled cosines by the Chebyshev recurrence t_(k+1) = t_1 t_k - t_(k-1) from t_0 = 2 (the weights 2, 1 and 4, 3, 1); another width refused by name."""
    if h not in (2, 3):
        raise ValueError("a plane packet has the half-width 2 or 3: a body is laid over its packet")
    doubled = [2, h - 2]
    while len(doubled) < h:
        doubled.append(doubled[1] * doubled[-1] - doubled[-2])
    return tuple(2 + t for t in doubled[:h])


def offsets(h: int, half_tops: tuple[int, ...]) -> list[tuple[int, ...]]:
    """Every offset of the envelope about the centre, along each axis from -(h - 1 + its half top) to h - 1 + its half top."""
    reach = [h - 1 + t for t in half_tops]
    return [tuple(j[a] - reach[a] for a in range(AXES)) for j in np.ndindex(*(2 * r + 1 for r in reach))]


def envelope_of(
    node: Node, at: tuple[int, ...], h: int, half_tops: tuple[int, ...] = (0,) * AXES
) -> tuple[Any, int]:
    """The raised cosine's envelope of the half-width h about the Node, the product of the weights over the three axes, flat at the centre's weight over the half top of each axis given one (MV-S1's `top`, 0 the former envelope), and the centre's weight."""
    weights = raised_cosine(h)
    envelope = zeros(node.shape)
    for off in offsets(h, half_tops):
        where = tuple(wrap(at[a] + off[a], node.cube) for a in range(AXES))
        weight = 1
        for a in range(AXES):
            weight *= weights[max(abs(off[a]) - half_tops[a], 0)]
        envelope[where] += weight
    return envelope, weights[0] ** AXES


def circle_point(den: int, h: int) -> tuple[int, int]:
    """The point of den's circle at the half-angle sine h (MV-S1, the wave number's unit): den cos k = (den^2 - 2 h^2) over den and den sin k = 2 h largest_below(den^2 - h^2) over den, each rounded once with the sign after (paces.odd_rounded), so the point at -h is the conjugate; (den, 0) at h = 0, (-den, 0) at |h| = den, the band's edge (MV-S2); beyond it refused by name."""
    if abs(h) > den:
        raise ValueError(f"a wave number beyond the band's edge: |h| {abs(h)} above den {den}")
    return (
        int(odd_rounded(den * den - 2 * h * h, den)),
        int(odd_rounded(2 * h * largest_below(den * den - h * h), den)),
    )


def axis_pairs(den: int, point: tuple[int, int], reach: int) -> dict[int, tuple[int, int]]:
    """The pair over den at every offset from -reach to reach along one axis: from (den, 0) at the centre, the axis's point composed one Link at a time (links.turn_pair, one odd rounding per part per Link), the conjugate point for a negative offset, so the pair at -n is the conjugate of the pair at n."""
    found = {0: (den, 0)}
    for side in (1, -1):
        for n in range(1, reach + 1):
            re, im = found[side * (n - 1)]
            pair = turn_pair(re, im, point[0], side * point[1], den)
            found[side * n] = (int(pair[0]), int(pair[1]))
    return found


def phase_of(den: int, pairs: list[tuple[int, int]]) -> tuple[int, int]:
    """The pair over den at a Node from its three axes' pairs, composed in their sorted order (two turns, one odd rounding per part each): the same integers at every image of the Node under the 48, the axes' pairs permuted with the axes and each one even under its axis's reflection with the wave."""
    first, second, third = sorted(pairs)
    re, im = turn_pair(first[0], first[1], second[0], second[1], den)
    re, im = turn_pair(re, im, third[0], third[1], den)
    return int(re), int(im)


def phases_of(
    node: Node,
    at: tuple[int, ...],
    h: int,
    half_tops: tuple[int, ...],
    points: list[tuple[int, int]],
) -> Pair:
    """The phase pair (C, S) over den at every Node of the envelope, the three axes' pairs at the Node's offsets (axis_pairs) composed (phase_of); (den, 0) beyond the envelope and everywhere at the wave 0."""
    den = node.den
    along = [axis_pairs(den, points[a], h - 1 + half_tops[a]) for a in range(AXES)]
    cosine, sine = zeros(node.shape) + den, zeros(node.shape)
    for off in offsets(h, half_tops):
        where = tuple(wrap(at[a] + off[a], node.cube) for a in range(AXES))
        cosine[where], sine[where] = phase_of(den, [along[a][off[a]] for a in range(AXES)])
    return cosine, sine


def running_rotation(num: int, den: int, points: list[tuple[int, int]]) -> tuple[int, int]:
    """The band's rotation at the wave number (the kinetic clause): den cos omega(k) = (num SUM_a den cos k_a) div (3 den) and its sine by the one search (paces.sine_den's form); the row's own pair (num, s) at the wave 0, (den, 0) for the massless row there, the double root with no rotation."""
    cosine = int(quotient(num * sum(c for c, _s in points), 3 * den))
    return cosine, sine_den(cosine, den)


def rest_record(
    node: Node,
    row: Row,
    envelope: Any,
    w0: int,
    amplitude: int,
    sense: int,
    vector: list[int],
    pairs: tuple[Pair, Pair] | None = None,
) -> list[Line]:
    """A record over the envelope at an amplitude, base = A w_i div w_0 along the lay's vector: at rest (gram.rest) the plane's re_now = base, re_before = base num div den, im_now = 0, im_before = sense base s div den with s the pair's sine; at a wave number (gram.moving) the base at the Node's phase pair now and at that pair turned by the band's rotation before."""
    assert row.pair is not None
    num = row.pair[0]
    base = quotient(amplitude * envelope, w0)
    if pairs is None:
        return gram.rest(row.shape, base, vector, num, node.den, sine_den(num, node.den), sense)
    return gram.moving(row.shape, base, vector, pairs[0], pairs[1], node.den, sense)


def uniform_levels(node: Node, row: Row, amplitude: int, sense: int) -> list[Line]:
    """The fourth form's levels at an amplitude (MA-S1, ma2's spelling): one record at rest at every Node (rest_record with the envelope 1 and the centre's weight 1) at the sense -1 or 1, or the conjugate pair at 0 (both senses summed, the im lines cancelling)."""
    if sense == 0:
        a = uniform_levels(node, row, amplitude, 1)
        b = uniform_levels(node, row, amplitude, -1)
        return [Line(x.now + y.now, x.before + y.before, None, None) for x, y in zip(a, b, strict=True)]
    return rest_record(node, row, zeros(node.shape) + 1, 1, amplitude, sense, [1, 0])


def share_at_node(node: Node, row: Row, lines: list[Line], rule: Any) -> int:
    """A record's share at the vacuum's weight at the Node of the board's first index, the uniform lay's share at every Node alike."""
    return int(node.share(lines, rule).reshape(-1)[0])


def lay_uniform(node: Node, rec: int, n: int, sense: int) -> None:
    """The fourth form laid: the plane with a gap at every Node alike at the least amplitude whose share at the vacuum's weight is at or above n quanta of its unit at every Node (ma2's fitted_uniform: the search by comparisons, doubling then halving, its answer plus one), at the sense -1 or 1 or the conjugate pair at 0; the lay logged."""
    row = node.records()[rec]
    assert row.pair is not None
    node.start_content, node.start_x = node.content(), node.row(CARRIER).lines[0].now
    rule = node.rule(row.pair, node.start_content, node.link_factors())
    target = n * node.units[rec]
    high = 1
    while share_at_node(node, row, uniform_levels(node, row, high, sense), rule) <= target:
        high = high + high
    low = 0
    while high - low > 1:
        middle = int(quotient(low + high, 2))
        if share_at_node(node, row, uniform_levels(node, row, middle, sense), rule) <= target:
            low = middle
        else:
            high = middle
    amplitude = low + 1
    lines = uniform_levels(node, row, amplitude, sense)
    node.lay(rec, Ellipsis, tuple(x for line in lines for x in (line.now, line.before)))
    node.log.append(
        {
            "event": "lay",
            "i": 0,
            "node": None,
            "line_pair": rec,
            "quanta": n,
            "amplitude": amplitude,
            "share": share_at_node(node, row, lines, rule),
            "unit": node.units[rec],
            "nodes": int(node.cube) ** AXES,
            "sense": sense,
        }
    )


def packet_share(node: Node, row: Row, lines: list[Line], rule: Any) -> int:
    """A record's share at the vacuum's weight summed over the board."""
    return int(sum(int(x) for x in node.share(lines, rule).reshape(-1)))


def fitted(
    node: Node,
    row: Row,
    envelope: Any,
    w0: int,
    target: int,
    vector: list[int],
    pairs: tuple[Pair, Pair] | None = None,
) -> int:
    """The largest amplitude at which the record's share at the vacuum's weight, summed over the packet, is at most the target (a search by comparisons, doubling then halving)."""
    assert row.pair is not None
    rule = node.rule(row.pair, node.content(), node.link_factors())

    def share_of(amplitude: int) -> int:
        lines = rest_record(node, row, envelope, w0, amplitude, 1, vector, pairs)
        return packet_share(node, row, lines, rule)

    high = 1
    while share_of(high) <= target:
        high = high + high
    low = 0
    while high - low > 1:
        middle = int(quotient(low + high, 2))
        if share_of(middle) <= target:
            low = middle
        else:
            high = middle
    return low


def wave_of(
    node: Node, row: Row, h: int, wave: tuple[int, ...], top: int
) -> tuple[tuple[int, ...], list[tuple[int, int]], tuple[int, int]]:
    """The moving lay's integers from its two fields: the half top per axis (the flat top of `top` Nodes along the axes of the wave's largest |h|, refused by name where the top is not an odd count or does not fit the board with the raised cosine's edges), the circle's point per axis (circle_point, |h| above den refused there) and the band's rotation (running_rotation, the row at the gap 0 at the wave 0 refused by name: its sine 0, the drift its lay)."""
    assert row.pair is not None
    if len(wave) != AXES:
        raise ValueError("a wave number is three integers, one per axis")
    if top < 1 or remainder(top, 2) == 0 or top + 2 * (h - 1) > node.cube:
        raise ValueError(
            "a top is an odd count of Nodes about the centre that fits the board with its edges"
        )
    largest = max(abs(x) for x in wave)
    half_tops = tuple(int(quotient(top - 1, 2)) if abs(x) == largest else 0 for x in wave)
    points = [circle_point(node.den, int(x)) for x in wave]
    rotation = running_rotation(row.pair[0], node.den, points)
    if rotation[1] == 0:
        raise ValueError("a packet of the gap-0 row at the wave 0 has no rotation: the drift is its lay")
    return half_tops, points, rotation


def lay_packet(
    node: Node,
    rec: int,
    at: tuple[int, ...],
    h: int,
    n: int,
    vector: list[int] | None = None,
    one_sense: int | None = None,
    wave: tuple[int, ...] | None = None,
    top: int = 1,
) -> None:
    """The `at` lay of a record with a gap (or of the plane at the gap 0 at a wave number): the conjugate pair (the two records at the senses -1 and 1 where the lay names no sense or the sense 0, EM-S2; the one record at the sense -1 or 1 named) laid over the envelope along the vector (a plane's (1, 0)), at rest where the lay names no wave (`rest_record`, the former lay by name) or at the wave number (MV-S1: the phase pair composed one Link at a time from the circle's point per axis, the level before at the band's rotation, `wave_of`, `phases_of`; the wave 0 the rest lay bit for bit) with the flat `top` (1 the former envelope), each record at the largest amplitude whose share, summed over the packet, is at most n quanta of its unit (`fitted`); a record refused by state where the standing row and the child agree at the centre in their full state, the sense (the charges' product above 0) and the spin (the spin densities' dot above 0; SR-S4: the exclusion the lay's rule per full state), laid whole where either opposes or nothing stands; the lay logged."""
    row = node.records()[rec]
    assert row.pair is not None
    named = {"sense": int(one_sense or 0)} | (
        {} if vector is None else {"vector": [int(v) for v in vector]}
    )
    vector = [1, 0] if vector is None else [int(v) for v in vector]
    half_tops: tuple[int, ...] = (0,) * AXES
    pairs = None
    if wave is not None:
        half_tops, points, rotation = wave_of(node, row, h, wave, top)
        named |= {"wave": [int(x) for x in wave], "top": int(top)}
    envelope, w0 = envelope_of(node, at, h, half_tops)
    if wave is not None:
        phases = phases_of(node, at, h, half_tops, points)
        pairs = (phases, turn_pair(phases[0], phases[1], rotation[0], rotation[1], node.den))
    node.start_content, node.start_x = node.content(), node.row(CARRIER).lines[0].now
    amplitude = fitted(node, row, envelope, w0, n * node.units[rec], vector, pairs)
    for sense in (-1, 1) if not one_sense else (int(one_sense),):
        lines = rest_record(node, row, envelope, w0, amplitude, sense, vector, pairs)
        standing = gram.density(row.shape, [line.now for line in row.lines])
        child = gram.density(row.shape, [line.now for line in lines])
        dot = sum(int(s[at]) * int(c[at]) for s, c in zip(standing, child, strict=True))
        charges = int(gram.charge(row.shape, row.lines)[at]) * int(gram.charge(row.shape, lines)[at])
        if dot > 0 and charges > 0:
            node.counts["refused_lay"] += 1
            node.log.append({"event": "refused", "i": 0, "node": list(at), "cause": "state", "dot": dot})
            continue
        node.lay(rec, Ellipsis, tuple(x for line in lines for x in (line.now, line.before)))
    lines = rest_record(node, row, envelope, w0, amplitude, 1, vector, pairs)
    rule = node.rule(row.pair, node.start_content, node.link_factors())
    node.log.append(
        {
            "event": "lay",
            "i": 0,
            "node": list(at),
            "line_pair": rec,
            "width": h,
            "quanta": n,
            "amplitude": amplitude,
            "share": packet_share(node, row, lines, rule),
            "unit": node.units[rec],
            "nodes": int(sum(1 for x in envelope.reshape(-1) if int(x) > 0)),
            **named,
        }
    )
