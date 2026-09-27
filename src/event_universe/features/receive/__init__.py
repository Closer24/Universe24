"""The receive: at each Port the pair on the Link, (re, im), rotated by the Port's angle k through the twist table's triple (c, s, d), each level Rule3's read act with the coefficients (2c, -2s) and (2s, 2c) on the two arrivals, the load d over the wall 2d and the remainder not kept; the angle the read act on each twist read's vector part here and arrived; the arrivals summed per axis for the spatial step (ALGEBRA.md 9.117 the row "the receive", 9.81 (2) (b), (c), 9.96 (2) (c), 9.119 item 2)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from event_universe.core.game_board import PORT_HEADINGS
from event_universe.core.register import Declaration
from event_universe.core.rule3 import rule3

PORTS = ("+x", "-x", "+y", "-y", "+z", "-z")


def heading(port: int) -> tuple[int, int]:
    """The Port's axis and side from the six Ports' table (core.game_board.PORT_HEADINGS)."""
    return next((axis, side) for axis, side in enumerate(PORT_HEADINGS[port]) if side)


Triple = tuple[Any, Any, Any]


@dataclass(frozen=True)
class TwistRead:
    """One read with a twist of the record's family: its factor (the weight times the record's own twist for "own", else the declared twist, by q the family's charge sign) and the read family's vector part at the Node, one level per axis (now forward, before backward)."""

    factor: int
    here: tuple[Any, Any, Any]


@dataclass(frozen=True)
class Link:
    """The values on one Port's Link, put there by the other end's send: the pair (re, im) and each twist read's vector component along the Port's axis, arrived."""

    re: Any
    im: Any | None
    vectors: tuple[Any, ...]


@dataclass(frozen=True)
class ReceiveTerm:
    """The twist table as declared: the fine triples by k_0 and the coarse by k_1, three rows (c, s, d) each, None on a world without a table; the fine bits of |k| = k_1 2^bits + k_0."""

    fine: Any | None
    coarse: Any | None
    fine_bits: int


@dataclass(frozen=True)
class ReceiveStart:
    """The interval's reading at (i): the record's pair (re, im) at the Node, the twist reads of its family, and the six Ports' Links in the order +x, -x, +y, -y, +z, -z."""

    re: Any
    im: Any | None
    reads: tuple[TwistRead, ...]
    links: tuple[Link, ...]


@dataclass(frozen=True)
class ReceiveWrites:
    """The transport's writes: the angle per Port, and the arrivals summed per axis for the two levels (the second None while the record has none and no rotation writes one)."""

    angles: tuple[Any, ...]
    re: tuple[Any, Any, Any]
    im: tuple[Any, Any, Any] | None


def angle(port: int, reads: tuple[TwistRead, ...], link: Link) -> Any:
    """The Port's angle k = sigma SUM factor (V_a here + V_a arrived) over the twist reads, each read Rule3's read act on the arrived level with the Node's own level as the self term over the wall 1, loaded onto the sum (ALGEBRA.md 9.81 (2) (a), 9.96 (2))."""
    axis, sigma = heading(port)
    total: Any = 0
    for read, arrived in zip(reads, link.vectors, strict=True):
        coefficient = sigma * read.factor
        total, _ = rule3((coefficient, 0, 0), (arrived, 0, 0), coefficient, 1, read.here[axis], 0, total)
    return total


def triple(term: ReceiveTerm, k: Any, port: int) -> Triple:
    """The rotation's triple at the Port from |k| = k_1 2^bits + k_0: the fine triple of k_0 and the coarse of k_1 composed by two of Rule3's read acts over the wall 1, the coefficients (c_1, -s_1) and (s_1, c_1) on (c_0, s_0), the denominator d_1 d_0 a product of two declared integers, the sine by k's sign; refused naming the Port beyond the coarse table or without one (ALGEBRA.md 9.96 (2) (c))."""
    magnitude = np.abs(k)
    coarse_index = magnitude >> term.fine_bits
    if term.fine is None or term.coarse is None or int(np.max(coarse_index)) >= term.coarse.shape[1]:
        raise ValueError(
            f"the twist on the Port toward {PORTS[port]} reaches |k| = {int(np.max(magnitude))}, "
            f"beyond the twist table ({'no table' if term.coarse is None else f'{term.coarse.shape[1]} coarse triples'}; "
            "ALGEBRA.md 9.96 (2) (c))"
        )
    c0, s0, d0 = term.fine[:, magnitude & ((1 << term.fine_bits) - 1)]
    c1, s1, d1 = term.coarse[:, coarse_index]
    cosine, _ = rule3((c1, -s1, 0), (c0, s0, 0), 0, 1, 0, 0, 0)
    sine, _ = rule3((s1, c1, 0), (c0, s0, 0), 0, 1, 0, 0, 0)
    return cosine, np.sign(k) * sine, d1 * d0


def rotated(found: Triple, re: Any, im: Any) -> tuple[Any, Any]:
    """The pair on the Link rotated by the triple: each level Rule3's read act with the coefficients (2c, -2s) and (2s, 2c) on the two arrivals, the load d over the wall 2d (the nearest unit), the remainder not kept (ALGEBRA.md 9.81 (2) (c))."""
    c, s, d = found
    t_re, _ = rule3((2 * c, -2 * s, 0), (re, im, 0), 0, 2 * d, 0, 0, d)
    t_im, _ = rule3((2 * s, 2 * c, 0), (re, im, 0), 0, 2 * d, 0, 0, d)
    return t_re, t_im


def check(start: ReceiveStart) -> None:
    """The refusals by name: six Links, each with one arrived vector per twist read."""
    if len(start.links) != 6:
        raise ValueError(f"the receive reads six Links, one per Port, got {len(start.links)}")
    for port, link in enumerate(start.links):
        if len(link.vectors) != len(start.reads):
            raise ValueError(
                f"the Link toward {PORTS[port]} carries {len(link.vectors)} vector parts for "
                f"{len(start.reads)} twist reads"
            )


def apply(term: ReceiveTerm, start: ReceiveStart, own: None = None) -> ReceiveWrites:
    """The primitive at (i), `apply(term, start, own)` with no own record: the angle per Port, the Link's pair rotated by its triple where the angle is not zero (the pair itself where it is), then Rule3's input per axis, arr_a = the arrival through +a plus the arrival through -a, for the two levels (ALGEBRA.md 9.117 the row "the receive")."""
    check(start)
    angles = []
    re_sums = [np.zeros_like(start.re) for _ in range(3)]  # Rule3's arr_a on the first level
    im_sums = (
        None if start.im is None else [np.zeros_like(start.re) for _ in range(3)]
    )  # and on the second
    for port, link in enumerate(start.links):
        k = angle(port, start.reads, link)
        angles.append(k)
        axis, _ = heading(port)
        if not np.any(k):
            re_sums[axis] = re_sums[axis] + link.re
            if im_sums is not None and link.im is not None:
                im_sums[axis] = im_sums[axis] + link.im
            continue
        t_re, t_im = rotated(triple(term, k, port), link.re, 0 if link.im is None else link.im)
        re_sums[axis] = re_sums[axis] + t_re
        if im_sums is None and np.any(t_im):
            im_sums = [np.zeros_like(start.re) for _ in range(3)]
        if im_sums is not None:
            im_sums[axis] = im_sums[axis] + t_im
    return ReceiveWrites(
        tuple(angles),
        (re_sums[0], re_sums[1], re_sums[2]),
        None if im_sums is None else (im_sums[0], im_sums[1], im_sums[2]),
    )


DECLARATION = Declaration(
    name="the receive",
    place="(i)",
    reads=("the Link's value", "a Port's accumulator", "the twist table"),
    writes=("the arrivals",),
    function=apply,
    section="9.112 item 1; 9.96 (2) (e); 9.117 item 3; 9.119 item 2, the row 'the receive'",
    word="the step",
)
