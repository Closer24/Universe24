"""The seed as the world file lays it: a list of lays in the three forms of the law and no fourth (the owner's word of 2026-10-25): `sea` lays the massless plane's drift v, the largest integer with v^2 <= T, at every Node; `hole` takes it back at one Node; `at` lays a packet, on the massless plane N drifts at the centre, on a plane with a gap the conjugate pair at rest over the raised cosine's envelope of the half-width 2 or 3. Refused by name: a fourth form, a lay onto a row of another shape, a sea of a plane with a gap, a Node off the board, a packet of another width."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe.core.paces import sine_den
from event_universe.core.ports import AXES, wrap
from event_universe.core.rule3 import quotient
from event_universe.rows import PLANE, Line, zeros

if TYPE_CHECKING:
    from event_universe.node import Node

ENVELOPES = {2: (2, 1), 3: (4, 3, 1)}  # the raised cosine's weights by half-width, exact in integers


def lay_world(node: Node, lays: list[dict[str, Any]]) -> None:
    """Every lay of the world file onto the Node's rows, the packets after the sea and the holes."""
    packets = []
    for lay in lays:
        form = lay.get("lay")
        row = node.by_index[int(lay["row"])] if "row" in lay else None
        if row is not None and row.shape != PLANE:
            raise ValueError("a lay is onto a plane (shape 2)")
        if form == "sea":
            if row is None or row.gap != 0:
                raise ValueError("a sea is the massless plane's alone: the drift is its double root")
            z = row.lines[0]
            z.now[:] = z.now + node.drift
        elif form == "hole":
            at = node.node_of(lay["at"])
            z = node.row(PLANE, gap=0).lines[0]
            z.now[at] = z.now[at] - node.drift
        elif form == "at":
            n = int(lay["quanta"])
            at = node.node_of(lay["centre"])
            if row is None:
                raise ValueError("a packet names its row")
            if row.gap == 0:
                z = row.lines[0]
                z.now[at] = z.now[at] + n * node.drift
            else:
                packets.append((node.records().index(row), at, int(lay.get("width", 0)), n))
        else:
            raise ValueError(f"a lay of no form of the law: {form!r}")
    for rec, at, h, n in packets:
        lay_packet(node, rec, at, h, n)


def envelope_of(node: Node, at: tuple[int, ...], h: int) -> tuple[Any, int]:
    """The raised cosine's envelope of the half-width h about the Node, the product of the weights over the three axes, and the centre's weight."""
    weights = ENVELOPES.get(h)
    if weights is None:
        raise ValueError("a plane packet has the half-width 2 or 3: a body is laid over its packet")
    envelope = zeros(node.shape)
    for j in np.ndindex(*(2 * h - 1,) * AXES):
        off = [x - (h - 1) for x in j]
        where = tuple(wrap(at[a] + off[a], node.cube) for a in range(AXES))
        envelope[where] += weights[abs(off[0])] * weights[abs(off[1])] * weights[abs(off[2])]
    return envelope, weights[0] ** AXES


def lay_packet(node: Node, rec: int, at: tuple[int, ...], h: int, n: int) -> None:
    """The `at` lay of a plane with a gap: the conjugate pair (the two records at the senses -1 and 1) laid at rest over the envelope, each record at the largest amplitude A at which its share at the vacuum's weight, summed over the packet, is at most n quanta of its unit (a search by comparisons); each Node's lines at the band's rest rotation: re_now = A w_i div w_0, re_before = re_now num div den, im_now = 0, im_before = sense re_now s div den with s the pair's sine."""
    row = node.records()[rec]
    assert row.pair is not None
    num = row.pair[0]
    sn = sine_den(num, node.den)
    envelope, w0 = envelope_of(node, at, h)
    c = node.content()
    rule = node.rule_of(row, c, node.link_factors())
    node.start_content = c

    def record(amplitude: int, sense: int) -> tuple[Line, Line]:
        re_now = quotient(amplitude * envelope, w0)
        return Line(re_now, quotient(re_now * num, node.den), None, node.w), Line(
            zeros(node.shape), sense * quotient(re_now * sn, node.den), None, node.w
        )

    def share_of(amplitude: int) -> int:
        re, im = record(amplitude, 1)
        return int(
            sum(
                int(x)
                for x in (node.share(re, rule, vacuum=True) + node.share(im, rule, vacuum=True)).reshape(
                    -1
                )
            )
        )

    target = n * node.units[rec]
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
    for sense in (-1, 1):
        re, im = record(low, sense)
        node.lay(rec, Ellipsis, (re.now, re.before, im.now, im.before))
    node.log.append(
        {
            "event": "lay",
            "i": 0,
            "node": list(at),
            "line_pair": rec,
            "width": h,
            "quanta": n,
            "amplitude": low,
            "share": share_of(low),
            "unit": node.units[rec],
            "nodes": int(sum(1 for x in envelope.reshape(-1) if int(x) > 0)),
        }
    )
