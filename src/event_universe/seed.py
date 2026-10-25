"""The seed as the world file lays it: a list of lays in the three forms of the law and no fourth (the owner's word of 2026-10-25): `sea` lays the plane at the gap 0's drift v, the largest integer with v^2 <= T, at every Node; `hole` takes it back at one Node; `at` lays a packet, on the plane at the gap 0 N drifts at the centre, on a record with a gap the conjugate pair at rest over the raised cosine's envelope of the half-width 2 or 3 (a quartet's lay names its `vector`, the eight integers of the lattice, and may name one `sense`; the lay refused by state where the standing row's spin density agrees with the child's at the centre, SR-S4). Refused by name: a fourth form, a lay onto a row of no record shape, a sea of a record with a gap, a Node off the board, a packet of another width, a quartet's lay with no vector."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe import gram
from event_universe.core.paces import sine_den
from event_universe.core.ports import AXES, wrap
from event_universe.core.rule3 import quotient
from event_universe.rows import PLANE, Line, Row, zeros

if TYPE_CHECKING:
    from event_universe.node import Node


def lay_world(node: Node, lays: list[dict[str, Any]]) -> None:
    """Every lay of the world file onto the Node's rows, the packets after the sea and the holes."""
    packets = []
    for lay in lays:
        form = lay.get("lay")
        row = node.by_index[int(lay["row"])] if "row" in lay else None
        if row is not None and row not in node.records():
            raise ValueError("a lay is onto a record (a plane or a quartet)")
        if form == "sea":
            if row is None or row.gap != 0:
                raise ValueError("a sea is the plane at the gap 0 alone: the drift is its double root")
            node.lay(node.records().index(row), Ellipsis, (node.drift, 0, 0, 0))
        elif form == "hole":
            at = node.node_of(lay["at"])
            node.lay(node.records().index(node.row(PLANE, gap=0)), at, (-node.drift, 0, 0, 0))
        elif form == "at":
            n = int(lay["quanta"])
            at = node.node_of(lay["centre"])
            if row is None:
                raise ValueError("a packet names its row")
            if row.gap == 0:
                node.lay(node.records().index(row), at, (n * node.drift, 0, 0, 0))
            else:
                vector = lay.get("vector")
                if (vector is None) != (row.shape == PLANE):
                    raise ValueError("a quartet's lay names its vector, a plane's names none")
                sense = lay.get("sense")
                packets.append(
                    (node.records().index(row), at, int(lay.get("width", 0)), n, vector, sense)
                )
        else:
            raise ValueError(f"a lay of no form of the law: {form!r}")
    for rec, at, h, n, vector, sense in packets:
        lay_packet(node, rec, at, h, n, vector, sense)


def raised_cosine(h: int) -> tuple[int, ...]:
    """The raised cosine's weights over the half-width h, w_k = 2 + 2 cos(pi k / h) for k = 0 .. h - 1, exact in integers where 2 cos(pi / h) is an integer, at h = 2 (0) and h = 3 (1) and at no other width: the doubled cosines by the Chebyshev recurrence t_(k+1) = t_1 t_k - t_(k-1) from t_0 = 2 (the weights 2, 1 and 4, 3, 1); another width refused by name."""
    if h not in (2, 3):
        raise ValueError("a plane packet has the half-width 2 or 3: a body is laid over its packet")
    doubled = [2, h - 2]
    while len(doubled) < h:
        doubled.append(doubled[1] * doubled[-1] - doubled[-2])
    return tuple(2 + t for t in doubled[:h])


def envelope_of(node: Node, at: tuple[int, ...], h: int) -> tuple[Any, int]:
    """The raised cosine's envelope of the half-width h about the Node, the product of the weights over the three axes, and the centre's weight."""
    weights = raised_cosine(h)
    envelope = zeros(node.shape)
    for j in np.ndindex(*(2 * h - 1,) * AXES):
        off = [x - (h - 1) for x in j]
        where = tuple(wrap(at[a] + off[a], node.cube) for a in range(AXES))
        envelope[where] += weights[abs(off[0])] * weights[abs(off[1])] * weights[abs(off[2])]
    return envelope, weights[0] ** AXES


def rest_record(
    node: Node, row: Row, envelope: Any, w0: int, amplitude: int, sense: int, vector: list[int]
) -> list[Line]:
    """A record at rest over the envelope at an amplitude (gram.rest): re_now = A w_i div w_0 along the lay's vector, before = num now div den + sense s (J now) div den with s the pair's sine, the plane's re_before = re_now num div den, im_now = 0, im_before = sense re_now s div den as the case v = (1, 0)."""
    assert row.pair is not None
    num = row.pair[0]
    re_now = quotient(amplitude * envelope, w0)
    return gram.rest(row.shape, re_now, vector, num, node.den, sine_den(num, node.den), sense)


def packet_share(node: Node, row: Row, lines: list[Line], rule: Any) -> int:
    """A record's share at the vacuum's weight summed over the board."""
    return int(sum(int(x) for x in node.share(lines, rule, vacuum=True).reshape(-1)))


def fitted(node: Node, row: Row, envelope: Any, w0: int, target: int, vector: list[int]) -> int:
    """The largest amplitude at which the record's share at the vacuum's weight, summed over the packet, is at most the target (a search by comparisons, doubling then halving)."""
    assert row.pair is not None
    rule = node.rule(row.pair, node.content(), node.link_factors())

    def share_of(amplitude: int) -> int:
        return packet_share(node, row, rest_record(node, row, envelope, w0, amplitude, 1, vector), rule)

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


def lay_packet(
    node: Node,
    rec: int,
    at: tuple[int, ...],
    h: int,
    n: int,
    vector: list[int] | None = None,
    one_sense: int | None = None,
) -> None:
    """The `at` lay of a record with a gap: the conjugate pair (the two records at the senses -1 and 1, or the one sense named) laid at rest over the envelope (`rest_record`) along the vector (a plane's (1, 0)), each record at the largest amplitude whose share, summed over the packet, is at most n quanta of its unit (`fitted`); a record refused by state where the standing row and the child agree at the centre in their full state, the sense (the charges' product above 0) and the spin (the spin densities' dot above 0; SR-S4: the exclusion the lay's rule per full state), laid whole where either opposes or nothing stands; the lay logged."""
    row = node.records()[rec]
    assert row.pair is not None
    named = None if vector is None else {"vector": [int(v) for v in vector], "sense": one_sense}
    vector = [1, 0] if vector is None else [int(v) for v in vector]
    envelope, w0 = envelope_of(node, at, h)
    node.start_content = node.content()
    amplitude = fitted(node, row, envelope, w0, n * node.units[rec], vector)
    for sense in (-1, 1) if one_sense is None else (int(one_sense),):
        lines = rest_record(node, row, envelope, w0, amplitude, sense, vector)
        standing = gram.density(row.shape, [line.now for line in row.lines])
        child = gram.density(row.shape, [line.now for line in lines])
        dot = sum(int(s[at]) * int(c[at]) for s, c in zip(standing, child, strict=True))
        charges = int(gram.charge(row.shape, row.lines)[at]) * int(gram.charge(row.shape, lines)[at])
        if dot > 0 and charges > 0:
            node.counts["refused_lay"] += 1
            node.log.append({"event": "refused", "i": 0, "node": list(at), "cause": "state", "dot": dot})
            continue
        node.lay(rec, Ellipsis, tuple(x for line in lines for x in (line.now, line.before)))
    lines = rest_record(node, row, envelope, w0, amplitude, 1, vector)
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
            **(named or {}),
        }
    )
