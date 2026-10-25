"""The interval, the Node's one program in both directions (ALGEBRA.md, The direction: every act but the click a bijection; the run back the same acts in the reverse order, each inverted), in the symmetric ride's form (R5; the owner's approved sentence 1 of 2026-10-25, the held carrier of the wall and every riding row step as one pair at the mean wall): the readings at the start, the walled row's act, every riding line's force and kick, the carrier's one division sourced by the riding momenta, every riding line's one division at the mean wall of the carrier's two levels, the riding rows' writes from numbers known before them, the swap at the top and the close."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe import readings
from event_universe.core import paces
from event_universe.core.ports import AXES, PORTS, across
from event_universe.core.rule3 import division_forward, half, quotient
from event_universe.features import volume
from event_universe.links import plane_current, stress_parts, tensor_parts, wronskian
from event_universe.rows import CARRIER, PLANE, POTENTIAL, TRACE, Line, zeros

if TYPE_CHECKING:
    from event_universe.node import Node


def odd_round(q: Any, d: Any) -> Any:
    """round(q / d) to the nearest for q odd and d even (never a half), the paces' rounding (2 q + d) div (2 d); the odd rounding of the ride's momenta."""
    return paces.rounded(q, d)


def laid_on(node: Node, line: Line, levels: Any) -> None:
    """The emission's size, a reading of the run: the levels laid on the massless line and the Nodes they were laid at."""
    laid = line.now - levels
    node.counts["light_laid"] += int(sum(abs(int(x)) for x in laid.reshape(-1)))
    node.counts["light_laid_nodes"] += int(sum(1 for x in laid.reshape(-1) if int(x) != 0))


def run(node: Node, direction: int) -> None:
    """One interval in the direction: forward the start's readings, the acts, the swap and the close, the frame pushed; backward the close undone from the log first, the turned Nodes returned to their pre-state by the same exchange, every act inverted in the reverse order."""
    if direction == 1:
        node.interval += 1
        top: Any = np.zeros(node.shape, dtype=bool)
        kept = None
    else:
        frame = node.stack.pop()
        node.unclick(frame)
        top = frame["turned"]
    held = [[line.copy() for line in row] for row in node.rows()]
    if direction == -1:
        if top.any():
            node.exchange(top, held)
        kept = [[line.copy() for line in row] for row in node.rows()]

    def at(line: Line) -> Any:
        return line.now if direction == 1 else np.where(top, line.now, line.before)

    rows = node.rows()
    where = {id(r): k for k, r in enumerate(node.rows_)}
    carrier, walled, potential, massless = (
        node.row(CARRIER),
        node.walled(),
        node.row(POTENTIAL),
        node.row(PLANE, gap=0),
    )
    c = np.asarray(volume.level_of(node.gamma, at(carrier.lines[0])), dtype=object)
    node.start_content = c
    p0 = paces.clock_of(node.gamma, c)
    node.proper = node.proper + direction * p0
    factors = node.link_factors([at(line) for line in carrier.lines[1 : 1 + AXES]])
    node.start_factors = factors
    frames = readings.frames(node, walled.lines[0].rem)
    node.start_frames = frames
    cphi = paces.rounded(at(potential.lines[0]) * p0, node.gamma)
    out: list[list[Line]] = [[] for _ in rows]

    def ends(k: int) -> tuple[Any, list[Line] | None]:
        return top, None if kept is None else kept[k]

    riders = [r for r in node.rows_ if r.wall is None and r is not carrier]
    gap_planes = [r for r in riders if r.shape == PLANE and r.gap]
    x_now = at(carrier.lines[0])
    w_half = half(node.w)
    trace, traceless = tensor_parts(
        stress_parts(
            [(at(line), r.pair[0]) for r in node.records() if r.pair for line in r.lines], node.shape
        )
    )
    # the walled row first: its act carries its own write, the Links' count comes from it
    k = where[id(walled)]
    (phi_start,), _levels, out[k] = node.act(
        rows[k], node.rule_of(walled, c, factors), None, [None], direction, [2 * cphi], *ends(k)
    )
    count = readings.centred_count(node, cphi, phi_start)
    node.count_max = max(
        int(abs(int(x)))
        for port in range(PORTS)
        for x in (count - frames[port] * across(count, port)).reshape(-1)
    )
    phases = readings.link_phases(node, frames, count)
    odd = [at(line) for line in potential.lines[1 : 1 + AXES]]
    node.start_phases, node.start_odd = phases, [o.copy() for o in odd]
    # the planes' Wronskian and current at this end, for the writes
    w_post = zeros(node.shape)
    for r in gap_planes:
        w_post = w_post + wronskian(*rows[where[id(r)]])
    current = [zeros(node.shape) for _ in range(AXES)]
    for r in gap_planes:
        re_s, im_s = [Line(at(line), None, None, line.wall) for line in rows[where[id(r)]]]
        for a, j_a in enumerate(plane_current(re_s, im_s, frames)):
            current[a] = current[a] + j_a
    forces: dict[int, tuple[list[Any], list[Any]]] = {}
    for r in riders:  # every riding line's force at the start, SUM_j R_j (m_j - a) - D a
        rule = node.rule_of(r, c, factors)
        turn = (phases, odd, frames) if r.shape == PLANE and r.gap else None
        starts = [at(line) for line in rows[where[id(r)]]]
        forces[where[id(r)]] = (
            starts,
            [
                m - (2 * rule.wall - rule.self_coefficient) * a
                for a, m in zip(starts, node.arrivals(starts, rule, turn), strict=True)
            ],
        )
    emission = zeros(
        node.shape
    )  # the Wronskian's change read from the kick: X_now SUM over the planes with a gap of (re F_im - im F_re)
    for r in gap_planes:
        (re_s, im_s), (f_re, f_im) = forces[where[id(r)]]
        emission = emission + x_now * (re_s * f_im - im_s * f_re)
    if direction == -1:  # the riding rows' writes come off first, from the post state
        node.write(
            rows[where[id(massless)]][0],
            quotient(emission, w_half * (carrier.lines[0].before + carrier.lines[0].now)),
            -1,
        )
        for line, n in zip(rows[where[id(potential)]], [2 * w_post, *current], strict=True):
            node.write(line, n, -1)
    # the kicks: every riding line's momentum in and out, and the carrier's source
    forms = zeros(node.shape)
    kicks: dict[int, list[Any]] = {}
    d = 2 * node.w * x_now
    for r in riders:
        k = where[id(r)]
        starts, force = forces[k]
        w_side = w_half * (carrier.lines[0].before + carrier.lines[0].now)
        p_side = [w_side * (line.now - line.before) + line.rem - half(w_side) for line in rows[k]]
        p_other = [p + direction * x_now * f for p, f in zip(p_side, force, strict=True)]
        for a, f, p1, p2 in zip(starts, force, p_side, p_other, strict=True):
            forms = (
                forms + odd_round(2 * p1 + 1, d) * odd_round(2 * p2 + 1, d) + quotient(-a * f, node.w)
            )
        kicks[k] = p_other
    # the carrier: its one division with the write sourced by the riding rows' momenta
    k = where[id(carrier)]
    p02 = p0 * p0
    numerators = [4 * x_now * (forms * TRACE * node.den * node.gamma**2 - trace * p02) * p0]
    numerators += [traceless[a] * p02 for a in range(AXES)] + [None] * (carrier.shape - 1 - AXES)
    out[k] = node.carried(rows[k], node.rule_of(carrier, c, factors), numerators, direction, *ends(k))
    xc = out[k][0]
    w_div = w_half * (xc.before + xc.now)
    # every riding line divides once at the mean wall of the carrier's two levels at its end
    plane_starts: list[list[Line]] = []
    stepped: list[list[Line]] = []
    w_after = zeros(node.shape)
    for r in riders:
        k = where[id(r)]
        new = []
        for a, p, line in zip(forces[k][0], kicks[k], rows[k], strict=True):
            v, rem = division_forward(p, w_div, half(w_div))
            new.append(
                Line(a + v, a, rem, w_div, line.wr, line.wwall)
                if direction == 1
                else Line(a, a - v, rem, w_div, line.wr, line.wwall)
            )
        if direction == -1 and kept is not None:
            node.restore(new, kept[k], top)
        out[k] = new
        if r.shape == PLANE:
            start = rows[k] if direction == 1 else new
            after = new if direction == 1 else held[k]
            plane_starts.append(list(start))
            stepped.append([line.copy() for line in after])
            if r.gap:
                w_after = w_after + wronskian(*after)
    node.stepped = stepped
    if direction == 1:  # the riding rows' writes after the divisions, from numbers known before them
        laid_line = out[where[id(massless)]][0]
        before_write = laid_line.now
        node.write(laid_line, quotient(emission, w_div), 1)
        laid_on(node, laid_line, before_write)
        for line, n in zip(out[where[id(potential)]], [2 * w_after, *current], strict=True):
            node.write(line, n, 1)
    node.set_rows(out)
    if direction == -1:
        node.interval -= 1
        return
    counters = (
        [a.copy() for a in node.standing],
        [a.copy() for a in node.crossed],
        [a.copy() for a in node.beats],
    )
    top = node.swap(held)
    log_from = len(node.log)
    node.click(plane_starts, held)
    node.stack.append({"turned": top, "counters": counters, "log_from": log_from})
