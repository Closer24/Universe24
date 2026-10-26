"""The bodies' closing, the close's last act (ALGEBRA.md, One point and one beat): a record standing at a whole quantum of its own unit through one period of its beat clicks, one take of its unit at the Node from the gap-0 row (`bodies`), the credit logged with its frame (`credit`: a plane's levels, neighbours, phases and factors at the start, `frame_of`; a quartet's bilinears, `bilinears_of`)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe import gram
from event_universe.core import rule3
from event_universe.core.ports import AXES, PORT_SIDES, PORTS
from event_universe.links import row_current
from event_universe.merger import takes
from event_universe.rows import PLANE, Line
from event_universe.run import credit
from event_universe.take import frame_nodes, move, recoil

if TYPE_CHECKING:
    from event_universe.node import Node


def bodies(
    node: Node,
    plane_starts: list[list[Line]],
    owns: list[Any],
    born_nodes: set[tuple[int, ...]],
    frozen: Any,
    r_emitter: rule3.Rule,
) -> None:
    """The bodies' closing: a record standing at a whole quantum of its own unit through one period of its beat clicks (one take of its unit at the Node, the credit logged), a Node of a birth this interval or a frozen Node apart; EQ-S1 in cs7's letter (CS7-S1; the owner's word of 2026-10-25, 17:57 UTC, through the Boss's recommendation, 6402908585 and 6403341352): where nothing arrives at the Node, the taken row's current across its six Links summed 0 at the interval's start (links.row_current as close.meet reads it; what flows in flows out), the take is laid back on the taken line (the line the take moved, logged as `taken_line`: CS4-S2) by the one lay act in the same close, the credit written with laid_back the levels and its momentum booked 0, so a board alike at every Node returns to Gamma exactly with a body credited at every Node in every cycle, and where light accumulates the take stands (the former closing, the take alone, kept by name; eq2's reading, every one of the six currents 0, kept by name); the plane at the gap 0 is never credited as a body (the light no body, cs4's sentence through the Boss, 6402358120: light at rest is no body in nature, its quanta taken at a meeting and by a body's click alone; the former closing of the standing light, credited at every interval where its beat stood at 1, kept by name); the beat a plane's by its re line's zero crossings counted in either direction (CK-S1: the crossing read even under the negation of the line, the two levels' product below 0 or exactly one of them 0, a touch of zero a crossing from either side alike, so the closing is covariant under the conjugation and the colour exchange alike; the beat the half period; the former upward crossing, and the form `b < 0 <= n or n < 0 <= b` odd where exactly one level is 0, kept by name), a quartet's from the invariant ratio N.G.B / N.G.N along the law's orbit (gram.period)."""
    rec0 = node.records().index(node.emitter())
    net = sum((row_current(plane_starts[rec0], port) for port in range(PORTS)), start=0)
    for rec, row in enumerate(node.records()):
        if row is node.emitter():
            continue
        standing_now = np.vectorize(
            lambda v, unit=node.units[rec]: 1 if int(v) >= unit else 0, otypes=[object]
        )(owns[rec])
        node.standing[rec] = np.where(standing_now == 1, node.standing[rec] + 1, 0)
        if row.shape == PLANE:
            re = row.lines[0]
            crossing = np.vectorize(
                lambda b, n: 1 if (int(b) * int(n) < 0 or (int(b) == 0) != (int(n) == 0)) else 0,
                otypes=[object],
            )(re.before, re.now)
            counting = np.vectorize(lambda v: 1 if int(v) > 0 else 0, otypes=[object])(node.crossed[rec])
            node.beats[rec] = np.where(
                (crossing == 1) & (counting == 1), node.crossed[rec], node.beats[rec]
            )
            node.crossed[rec] = np.where(
                crossing == 1, 1, np.where(counting == 1, node.crossed[rec] + 1, 0)
            )
        else:
            node.beats[rec] = gram.period(node, row.lines, standing_now)
        closing = np.vectorize(
            lambda st, bt: 1 if (int(bt) > 0 and int(st) >= int(bt)) else 0, otypes=[object]
        )(node.standing[rec], node.beats[rec])
        for where in zip(*np.nonzero(closing == 1), strict=True):
            at = tuple(int(x) for x in where)
            if at in born_nodes or frozen[at]:
                continue
            got = takes(node, [(at, node.units[rec])], r_emitter, 1)
            node.standing[rec][at] = 0
            if got is None:
                continue
            (take,) = got
            levels, now, k = take["levels"], take["taken_now_was"], take["taken_line"]
            node.counts["body_clicks"] += 1
            frame = (
                frame_of(node, rec, at, plane_starts)
                if row.shape == PLANE
                else bilinears_of(node, rec, at)
            )
            entry = credit(node, rec, at, take, frame)
            if int(net[at]) == 0:
                move(node, rec0, k, at, now - int(node.records()[rec0].lines[k].now[at]))
                entry["laid_back"], entry["dP_take"] = levels, [0] * AXES
                back = recoil(node, at, [-x for x in node.last_dp], entry["clock"], 1)
                entry["recoil"], entry["carry"] = [0] * AXES, back["carry"]
                node.counts["laid_back"] += 1
            node.log.append(entry)


def frame_of(
    node: Node, rec: int, at: tuple[int, ...], plane_starts: list[list[Line]]
) -> dict[str, Any]:
    """A credit's frame: the record's levels at the Node now, stepped and at the start, its neighbours' at the start, the Link phases, frames, odd lines and factors the Node read at the start."""
    re, im = node.records()[rec].lines
    re0, im0 = plane_starts[rec]
    nodes = frame_nodes(node, at)[1:]
    sre, sim = node.stepped[rec]
    return {
        "re_now": int(re.now[at]),
        "im_now": int(im.now[at]),
        "re_before": int(re.before[at]),
        "im_before": int(im.before[at]),
        "re_stepped": int(sre.now[at]),
        "im_stepped": int(sim.now[at]),
        "re_start_now": int(re0.now[at]),
        "re_start_before": int(re0.before[at]),
        "im_start_now": int(im0.now[at]),
        "im_start_before": int(im0.before[at]),
        "re_neighbours_start": [int(re0.now[n]) for n in nodes],
        "im_neighbours_start": [int(im0.now[n]) for n in nodes],
        "phases": [[int(c[at]), int(sn[at])] for c, sn in node.start_phases],
        "frames": [int(f[at]) for f in node.start_frames],
        "odd": [
            int(side * (node.start_odd[axis][at] + node.start_odd[axis][n]))
            for (axis, side), n in zip(PORT_SIDES, nodes, strict=True)
        ],
        "X": node.X,
        "factors": [int(f[at]) for f in node.start_factors],
    }


def bilinears_of(node: Node, rec: int, at: tuple[int, ...]) -> dict[str, Any]:
    """A quartet's credit frame: its levels at the Node, its charge W, its spin density (the record's axial vector, signed per axis) and its axial Wronskians B.GJ Gamma_a.N (SR-S2)."""
    row = node.records()[rec]
    nows, befores = [line.now for line in row.lines], [line.before for line in row.lines]
    gj = gram.matmul(gram.gram(row.shape), gram.rotation(row.shape))
    axial = [int(s[at]) for s in gram.density(row.shape, nows)]
    return {
        "levels_now": [int(n[at]) for n in nows],
        "levels_before": [int(b[at]) for b in befores],
        "W": int(gram.charge(row.shape, row.lines)[at]),
        "axial": axial,
        "axial_sign": [(s > 0) - (s < 0) for s in axial],
        "axial_wronskian": [
            int(gram.form(gj, befores, gram.matvec(ga, nows))[at]) for ga in gram.axes(row.shape)
        ],
    }
