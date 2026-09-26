"""THE NINTH HARD QUESTION (records 2152, 2154, 2155): A BODY HELD BY ITS CLICKS, with no well
and no self-binding. Between clicks a body is a free record and the rule 9.57 (1) spreads it;
a click localises it again. Does its width stay bounded?

THE ENVIRONMENT (HOST, the runner's choice, stated once): every Node is a detector, the
owner's picture of record 2154 ("every Node splits like a ray; a click takes a whole quantum at
one Node"). THE CLICK is the engine's ladder (ALGEBRA.md 9.25 (2), `_ladder_click`): at every
interval the record's one-way flux into every Node through its Ports is booked, the running
total C gains it, and the click fires at the first interval at which 2 W C >= (2 u + 1) T, at
the Node whose segment of that interval's increment, laid out in Node order, holds the
threshold (Born's rule, 9.25 (3)); u the residue on the wheel W = 700, one per click, the
sequence u_{k+1} = (u_k + 397) mod W from u_0 = 350 (every residue once per 700 clicks; the
engine's residue is the record's own, here a stated sequence); T the record's norm at its
start. THE NODE OF THE CLICK: the engine lays the increment out in the ladder's declared order
and the residue's threshold picks the segment; when one interval's increment exceeds the whole
norm (a record at one Node in a bath of detectors, below) that order alone picks the Node and
Born's rule is lost, so here the point within the increment is the fraction (2 u' + 1) / (2 W)
of it, u' a second residue sequence (u'_{k+1} = (u'_k + 263) mod W from 100): Born's rule
kept, the order dropped (a HOST choice, reported to the Boss as a finding on the ladder).
THE FLUX on a Link i -> j is J = now_j before_i - now_i before_j (positive along a wave's way;
the passage of a moving packet through a plane books its whole norm, the self-check `check`).
THE NORM is the rule's own conserved form (ALGEBRA.md 9.57 (1); the record's form of the
engine): I = SUM (now^2 + before^2) - (S / w) SUM now before - (R / w) SUM before_i SUM_j now_j
over the Links, times 3 den / num (the flux's units; the passage check reads the factor).

THE FORMS OF THE CLICK, all run:
- `whole`: the record is deleted whole and re-created at the click's Node with its norm (the
  engine's click on a record: the content handed to the body at that Node, the body re-given
  there), one Node holding the form, remainders zero.
- `quantum`: the owner's picture (record 2154): a click takes ONE quantum at one Node. The M =
  2000 quanta share the record's profile until each clicks (quantum k at its own residue u_k:
  2 W C >= (2 u_k + 1) T, the same running total C, T the one-quantum norm scaled); a clicked
  quantum is a record at its click's Node and steps by the rule on its own, on a box of side 9
  about that Node (its support reaches two Links from the Node before its next click, the
  `whole` run's reading; a level reaching the box's face is counted as a leak), its next click
  by the same ladder; the body's pattern is the sum of its quanta's forms, its width the rms
  of that pattern about the start.
- `control`: no click; the free packet (item 1's control on this board).

The record: item 1's packet narrowed to the board, the kind [800, 850], width 10 (the rms of
its envelope squared 7.1 Links; width 20 wraps a 64-board's faces at 28 percent of the peak) at
the middle of 64^3 periodic, no content anywhere (no hold: no self-binding). The readings
(GAMEBOARD of the runner): the rms width about the peak Node (minimum image), the peak, the
clicks' count, the intervals between them, the rms displacement of the peak from the start
(the walk), every 50 intervals over 1500.

    PYTHONPATH=src python docs/designs/rule_alone/item9_clicks.py whole|quantum|control [intervals]
"""

from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rule_alone as R  # noqa: E402

SHAPE = (64, 64, 64)
WRAP = (True, True, True)
KIND = (800, 850)
WIDTH = 10.0
AMPLITUDE = 1 << 11  # the collapsed record's one-Node amplitude must keep the rule's total in int64
WHEEL = 700
RESIDUE_STEP = 397
RESIDUE_START = 350
POSITION_STEP = 263
POSITION_START = 100
QUANTA = 2000
BOX = 9  # the box of a clicked quantum, about its Node
VACUUM_COEFFICIENTS: dict = {}  # the kind's (R, S, w) per board shape, for the momentum reading
EVERY = 50


def link_currents(now: np.ndarray, before: np.ndarray) -> list[np.ndarray]:
    """J on the Link from each Node to its +axis neighbour, per axis (x-major arrays)."""
    currents = []
    for axis in range(3):
        n_next = np.roll(now, -1, axis=axis)
        b_next = np.roll(before, -1, axis=axis)
        currents.append(n_next.astype(np.float64) * before - now.astype(np.float64) * b_next)
    return currents


def inward_flux(now: np.ndarray, before: np.ndarray) -> np.ndarray:
    """The one-way flux into every Node through its six Ports (HOST floats)."""
    total = np.zeros(now.shape, dtype=np.float64)
    for axis, j in enumerate(link_currents(now, before)):
        # j > 0 flows from the Node to its +axis neighbour: into the neighbour
        total += np.roll(np.maximum(j, 0.0), 1, axis=axis)
        # j < 0 flows from the +axis neighbour into the Node
        total += np.maximum(-j, 0.0)
    return total


def norm(
    now: np.ndarray,
    before: np.ndarray,
    read: np.ndarray,
    own: np.ndarray,
    wall: np.ndarray,
    wrap: tuple[bool, bool, bool],
    num: int,
    den: int,
) -> float:
    """The rule's conserved form I (ALGEBRA.md 9.57 (1)) in the flux's units, HOST floats."""
    n = now.astype(np.float64)
    b = before.astype(np.float64)
    s_over_w = own.astype(np.float64) / wall.astype(np.float64)
    r_over_w = read.astype(np.float64) / wall.astype(np.float64)
    form = (
        (n * n + b * b).sum()
        - (s_over_w * n * b).sum()
        - (r_over_w * b * R.neighbour_sum(now, wrap)).sum()
    )
    return float(3.0 * den / num * form)


def passage_check(cos_omega: float, num: int, den: int) -> float:
    """A moving packet on a periodic board passes a plane: the plane's one-way flux summed over
    the passage against the norm (the flux's calibration, HOST)."""
    shape = (256, 8, 8)
    wrap = (True, True, True)
    numa = np.full(shape, num, dtype=R.INT)
    dena = np.full(shape, den, dtype=R.INT)
    read, own, wall = R.coefficients(numa, dena, np.zeros(shape, dtype=R.INT))
    k = math.pi / 4
    omega = math.acos((num / den) * (math.cos(k) + 2.0) / 3.0)
    x = np.arange(shape[0], dtype=np.float64).reshape(-1, 1, 1)
    envelope = AMPLITUDE * np.exp(-((x - 64.0) ** 2) / (2.0 * 12.0**2)) * np.ones(shape)
    now = np.rint(envelope * np.cos(k * x)).astype(R.INT)
    before = np.rint(envelope * np.cos(k * x + omega)).astype(R.INT)
    remainder = np.zeros(shape, dtype=R.INT)
    total = norm(now, before, read, own, wall, wrap, num, den)
    booked = 0.0
    plane = 128
    for _ in range(400):
        j = link_currents(now, before)[0]
        booked += float(np.maximum(j[plane], 0.0).sum())
        now, before, remainder = R.step(now, before, remainder, read, own, wall, wrap)
    return booked / total


def batch_neighbour_sum(a: np.ndarray) -> np.ndarray:
    """The six neighbours' levels summed on every box of a batch [Q, BOX, BOX, BOX]; beyond a
    box's face the level is 0."""
    total = np.zeros_like(a)
    for axis in (1, 2, 3):
        for shift in (1, -1):
            rolled = np.roll(a, shift, axis=axis)
            edge = [slice(None)] * 4
            edge[axis] = slice(0, 1) if shift == 1 else slice(a.shape[axis] - 1, a.shape[axis])
            rolled[tuple(edge)] = 0
            total += rolled
    return total


def batch_step(now, before, remainder, read: int, own: int, wall: int):  # type: ignore[no-untyped-def]
    total = read * batch_neighbour_sum(now) + own * now - wall * before + remainder
    nxt = np.floor_divide(total, wall)
    return nxt, now, total - wall * nxt


def batch_inward_flux(now: np.ndarray, before: np.ndarray) -> np.ndarray:
    total = np.zeros(now.shape, dtype=np.float64)
    n = now.astype(np.float64)
    b = before.astype(np.float64)
    for axis in (1, 2, 3):
        n_next = np.roll(n, -1, axis=axis)
        b_next = np.roll(b, -1, axis=axis)
        edge = [slice(None)] * 4
        edge[axis] = slice(now.shape[axis] - 1, now.shape[axis])
        n_next[tuple(edge)] = 0.0
        b_next[tuple(edge)] = 0.0
        j = n_next * b - n * b_next
        total += np.roll(np.maximum(j, 0.0), 1, axis=axis)
        total += np.maximum(-j, 0.0)
    return total


def readings_of(
    now: np.ndarray, before: np.ndarray, cos_omega: float
) -> tuple[float, tuple[int, int, int], int]:
    e2 = R.envelope_squared(now, before, np.full(now.shape, cos_omega))
    peak = np.unravel_index(int(np.argmax(e2)), e2.shape)
    total = float(e2.sum())
    spread = 0.0
    for axis in range(3):
        coordinate = np.arange(SHAPE[axis], dtype=np.float64)
        d = coordinate - float(peak[axis])
        d = (d + SHAPE[axis] / 2) % SHAPE[axis] - SHAPE[axis] / 2  # the minimum image
        shape = [1, 1, 1]
        shape[axis] = SHAPE[axis]
        spread += float((e2 * (d.reshape(shape) ** 2)).sum()) / total
    return math.sqrt(spread / 3.0), (int(peak[0]), int(peak[1]), int(peak[2])), int(np.abs(now).max())


def one_node_level(t_norm: float, own: np.ndarray, wall: np.ndarray, num: int, den: int) -> int:
    """The level a at one Node with before = a whose form is T: a^2 (2 - S / w) 3 den / num = T
    (no neighbour holds a level; before the same level, the record's last two samples one)."""
    s_over_w = float(own.flat[0]) / float(wall.flat[0])
    return round(math.sqrt(t_norm * num / (3.0 * den) / (2.0 - s_over_w)))


def born_node(flux: np.ndarray, fraction: float) -> tuple[int, int, int]:
    """The Node whose segment of the increment, laid out in Node order, holds the point at
    `fraction` of the increment (Born's rule with a stated residue)."""
    cumulative = np.cumsum(flux.ravel())
    index = int(np.searchsorted(cumulative, fraction * float(cumulative[-1])))
    node = np.unravel_index(min(index, cumulative.size - 1), flux.shape)
    return (int(node[0]), int(node[1]), int(node[2]))


def walk_of(peak: tuple[int, int, int], start: tuple[int, int, int]) -> float:
    return math.sqrt(
        sum(
            ((p - s + SHAPE[a] / 2) % SHAPE[a] - SHAPE[a] / 2) ** 2
            for a, (p, s) in enumerate(zip(peak, start, strict=True))
        )
    )


class Record:
    """One record on the board with its ladder: the running total, its residues, its clicks.
    With `keep_width` set, THE CLICK THAT KEEPS THE MOMENTUM (the Boss's record 2160): the
    record is re-created at the click's Node as a packet of that rms width carrying the phase
    gradient read from its currents before the click (sin K_a = sin omega_0 SUM J_a / SUM F, the
    plane wave's relation), at the same norm; the displacement to the click's Node is booked
    as the detector's share."""

    def __init__(
        self,
        now: np.ndarray,
        before: np.ndarray,
        t_norm: float,
        u: int,
        u_position: int,
        keep_width: float | None = None,
        cos_omega: float = 0.0,
        kind: tuple[int, int] = KIND,
        born_by: str = "flux",
    ) -> None:
        self.now = now
        self.before = before
        self.remainder = np.zeros(now.shape, dtype=R.INT)
        self.t_norm = t_norm
        self.running = 0.0
        self.u = u
        self.u_position = u_position
        self.clicks: list[dict] = []
        self.keep_width = keep_width
        self.cos_omega = cos_omega
        self.kind = kind
        # THE CARRIED MOMENTUM (record 2160): the record's K as a label, set from its start and
        # changed between clicks by what the rule did (the reading now less the reading just
        # after the last re-creation); the reading alone re-imposed at every click loses a few
        # percent per click on a narrow packet (the first run: K 0.11 to 0.0000 in 50 clicks)
        self.k_label = self.momentum() if keep_width is not None else [0.0, 0.0, 0.0]
        self.k_reference = list(self.k_label)
        # THE NODE OF THE CLICK, BORN'S RULE BY THE INWARD FLUX (the engine's, 9.25 (3)) OR BY
        # THE RECORD'S FORM AT THE NODE: a Link's flux is booked to the Node it enters, so a
        # bath of Node detectors samples a moving packet one Link ahead of its density at
        # every click (the `flux` run: 0.7 Link forward per click, the body at 2.7 times its
        # speed); `density` samples the form itself, the cube detectors' limit
        self.born_by = born_by

    def momentum(self) -> list[float]:
        """K per axis read from the currents (HOST): sin K_a = sin omega_K SUM J_a / I, I the
        rule's conserved form at the kind's vacuum coefficients (both SUM J_a and I are exact
        invariants of the free rule, so the reading holds between clicks; the pair form
        now^2 + before^2 - 2 now before cos omega_0 is not invariant for a narrow packet and
        drifted 6 percent per interval in the first run); omega_K from K by two passes of the
        dispersion."""
        num, den = self.kind
        key = (self.now.shape, self.kind)
        if key not in VACUUM_COEFFICIENTS:
            numa = np.full(self.now.shape, num, dtype=R.INT)
            dena = np.full(self.now.shape, den, dtype=R.INT)
            VACUUM_COEFFICIENTS[key] = R.coefficients(numa, dena, np.zeros(self.now.shape, dtype=R.INT))
        read, own, wall = VACUUM_COEFFICIENTS[key]
        invariant = norm(self.now, self.before, read, own, wall, WRAP, num, den) * num / (3.0 * den)
        if invariant <= 0:
            return [0.0, 0.0, 0.0]
        currents = [float(j.sum()) for j in link_currents(self.now, self.before)]
        k = [0.0, 0.0, 0.0]
        for _ in range(2):
            two_cos = (num / den) * sum(2.0 * math.cos(v) for v in k) / 3.0
            omega_k = math.acos(max(-1.0, min(1.0, two_cos / 2.0)))
            k = [math.asin(max(-1.0, min(1.0, math.sin(omega_k) * c / invariant))) for c in currents]
        return k

    def recreate_with_momentum(
        self,
        node: tuple[int, int, int],
        k: list[float],
        read: np.ndarray,
        own: np.ndarray,
        wall: np.ndarray,
    ) -> None:
        shape = self.now.shape
        grids = np.meshgrid(*[np.arange(n, dtype=np.float64) for n in shape], indexing="ij")
        dx = [(g - c + s / 2) % s - s / 2 for g, c, s in zip(grids, node, shape, strict=True)]
        r2 = sum(d * d for d in dx)
        envelope = np.exp(-r2 / (2.0 * self.keep_width**2))
        num, den = self.kind
        two_cos = (num / den) * sum(2.0 * math.cos(v) for v in k) / 3.0
        omega_k = math.acos(max(-1.0, min(1.0, two_cos / 2.0)))
        phase = sum(kv * d for kv, d in zip(k, dx, strict=True))
        now = envelope * np.cos(phase - omega_k / 2.0)
        before = envelope * np.cos(phase + omega_k / 2.0)
        unit_now = np.rint(now * 1024).astype(R.INT)
        unit_before = np.rint(before * 1024).astype(R.INT)
        unit_norm = norm(unit_now, unit_before, read, own, wall, WRAP, num, den)
        scale = 1024.0 * math.sqrt(self.t_norm / unit_norm) if unit_norm > 0 else 1024.0
        self.now = np.rint(now * scale).astype(R.INT)
        self.before = np.rint(before * scale).astype(R.INT)
        self.remainder = np.zeros(shape, dtype=R.INT)

    def step(
        self, read: np.ndarray, own: np.ndarray, wall: np.ndarray, t: int, num: int, den: int
    ) -> None:
        self.now, self.before, self.remainder = R.step(
            self.now, self.before, self.remainder, read, own, wall, WRAP
        )
        flux = inward_flux(self.now, self.before)
        increment = float(flux.sum())
        threshold = (2 * self.u + 1) * self.t_norm / (2.0 * WHEEL)
        if self.running + increment >= threshold:
            if self.born_by == "density":
                weight = R.envelope_squared(
                    self.now, self.before, np.full(self.now.shape, self.cos_omega)
                )
                node = born_node(weight, (2 * self.u_position + 1) / (2.0 * WHEEL))
            else:
                node = born_node(flux, (2 * self.u_position + 1) / (2.0 * WHEEL))
            self.clicks.append(
                {
                    "t": t,
                    "node": list(node),
                    "since": t - (self.clicks[-1]["t"] if self.clicks else 0),
                    "increment_over_norm": increment / self.t_norm,
                }
            )
            if self.keep_width is not None:
                read_now = self.momentum()
                k = [
                    label + (now_value - reference)
                    for label, now_value, reference in zip(
                        self.k_label, read_now, self.k_reference, strict=True
                    )
                ]
                self.k_label = k
                e2 = R.envelope_squared(self.now, self.before, np.full(self.now.shape, self.cos_omega))
                centroid = R.centroid(e2)
                self.clicks[-1]["k_read"] = k
                self.clicks[-1]["detector_share"] = [
                    float((n - c + s / 2) % s - s / 2)
                    for n, c, s in zip(node, centroid, self.now.shape, strict=True)
                ]
                self.recreate_with_momentum(node, k, read, own, wall)
                self.k_reference = self.momentum()
            else:
                level = one_node_level(self.t_norm, own, wall, num, den)
                self.now = np.zeros(SHAPE, dtype=R.INT)
                self.before = np.zeros(SHAPE, dtype=R.INT)
                self.remainder = np.zeros(SHAPE, dtype=R.INT)
                self.now[node] = level
                self.before[node] = level
            self.running = 0.0
            self.u = (self.u + RESIDUE_STEP) % WHEEL
            self.u_position = (self.u_position + POSITION_STEP) % WHEEL
        else:
            self.running += increment


def run(mode: str, intervals: int) -> dict:
    num = np.full(SHAPE, KIND[0], dtype=R.INT)
    den = np.full(SHAPE, KIND[1], dtype=R.INT)
    read, own, wall = R.coefficients(num, den, np.zeros(SHAPE, dtype=R.INT))
    cos_omega = float(R.rest_rotation(read, own, wall)[0, 0, 0])
    middle = SHAPE[0] // 2
    now, before = R.gaussian_packet(SHAPE, (middle, middle, middle), WIDTH, AMPLITUDE, cos_omega)
    t_norm = norm(now, before, read, own, wall, WRAP, *KIND)
    start = (middle, middle, middle)
    records = [Record(now, before, t_norm, RESIDUE_START, POSITION_START)]
    # the quantum form: the shared profile's quanta, each with its own residue, leave it one
    # by one at their thresholds and become records of their own on a box about their Node
    shared_u = np.array([(RESIDUE_START + k * RESIDUE_STEP) % WHEEL for k in range(QUANTA)])
    shared_position = np.array([(POSITION_START + k * POSITION_STEP) % WHEEL for k in range(QUANTA)])
    shared_running = 0.0
    left = QUANTA
    q_now = np.zeros((QUANTA, BOX, BOX, BOX), dtype=R.INT)
    q_before = np.zeros_like(q_now)
    q_rem = np.zeros_like(q_now)
    q_position = np.zeros((QUANTA, 3), dtype=np.int64)  # the box's centre Node on the board
    q_running = np.zeros(QUANTA)
    q_u = np.zeros(QUANTA, dtype=np.int64)
    q_upos = np.zeros(QUANTA, dtype=np.int64)
    q_out = np.zeros(QUANTA, dtype=bool)  # the quantum has left the shared profile
    q_clicks = np.zeros(QUANTA, dtype=np.int64)
    q_leaks = 0
    q_norm = t_norm / QUANTA
    q_level = one_node_level(q_norm, own, wall, *KIND)
    centre = BOX // 2
    read0, own0, wall0 = int(read.flat[0]), int(own.flat[0]), int(wall.flat[0])
    readings: list[dict] = []
    t0 = time.time()
    for t in range(intervals + 1):
        if t % EVERY == 0:
            if mode == "quantum":
                # the pattern's rms about the start: the shared profile's part and the quanta's
                spread = 0.0
                weight_total = 0.0
                if left > 0:
                    e2 = R.envelope_squared(records[0].now, records[0].before, np.full(SHAPE, cos_omega))
                    total = float(e2.sum())
                    if total > 0:
                        share = left / QUANTA
                        for axis in range(3):
                            d = np.arange(SHAPE[axis], dtype=np.float64) - float(start[axis])
                            d = (d + SHAPE[axis] / 2) % SHAPE[axis] - SHAPE[axis] / 2
                            shape = [1, 1, 1]
                            shape[axis] = SHAPE[axis]
                            spread += share * float((e2 * (d.reshape(shape) ** 2)).sum()) / total
                        weight_total += share
                if q_out.any():
                    e2q = R.envelope_squared(
                        q_now[q_out], q_before[q_out], np.full((1, 1, 1, 1), cos_omega)
                    )
                    offsets = np.arange(BOX, dtype=np.float64) - centre
                    for axis in range(3):
                        pos = q_position[q_out, axis].astype(np.float64)
                        shape = [1, 1, 1, 1]
                        shape[axis + 1] = BOX
                        d = pos.reshape(-1, 1, 1, 1) + offsets.reshape(shape) - float(start[axis])
                        d = (d + SHAPE[axis] / 2) % SHAPE[axis] - SHAPE[axis] / 2
                        totals = e2q.sum(axis=(1, 2, 3))
                        totals[totals == 0] = 1.0
                        spread += float(((e2q * d * d).sum(axis=(1, 2, 3)) / totals).sum()) / QUANTA
                    weight_total += int(q_out.sum()) / QUANTA
                width = math.sqrt(spread / (3.0 * max(weight_total, 1e-12)))
                readings.append(
                    {
                        "t": t,
                        "width_rms": width,
                        "peak_node": [int(v) for v in np.rint(q_position[q_out].mean(axis=0))]
                        if q_out.any()
                        else list(start),
                        "peak": 0,
                        "walk": float(
                            np.sqrt(((q_position[q_out] - np.array(start)) ** 2).sum(axis=1).mean())
                        )
                        if q_out.any()
                        else 0.0,
                        "clicks": int(q_clicks.sum()),
                        "quanta_out": QUANTA - left,
                        "leaks": q_leaks,
                        "norm_ratio": float("nan"),
                    }
                )
            else:
                width, peak, peak_level = readings_of(records[0].now, records[0].before, cos_omega)
                readings.append(
                    {
                        "t": t,
                        "width_rms": width,
                        "peak_node": list(peak),
                        "peak": peak_level,
                        "walk": walk_of(peak, start),
                        "clicks": len(records[0].clicks),
                        "norm_ratio": norm(
                            records[0].now, records[0].before, read, own, wall, WRAP, *KIND
                        )
                        / t_norm,
                    }
                )
        if t == intervals:
            break
        if mode == "control":
            records[0].now, records[0].before, records[0].remainder = R.step(
                records[0].now, records[0].before, records[0].remainder, read, own, wall, WRAP
            )
        elif mode == "whole":
            records[0].step(read, own, wall, t + 1, *KIND)
        else:
            shared = records[0]
            if left > 0:
                shared.now, shared.before, shared.remainder = R.step(
                    shared.now, shared.before, shared.remainder, read, own, wall, WRAP
                )
                flux = inward_flux(shared.now, shared.before)
                shared_running += float(flux.sum())
                leaving = np.where(~q_out & (2 * WHEEL * shared_running >= (2 * shared_u + 1) * t_norm))[
                    0
                ]
                for k in leaving:
                    node = born_node(flux, (2 * int(shared_position[k]) + 1) / (2.0 * WHEEL))
                    q_position[k] = node
                    q_now[k] = 0
                    q_before[k] = 0
                    q_rem[k] = 0
                    q_now[k, centre, centre, centre] = q_level
                    q_before[k, centre, centre, centre] = q_level
                    q_u[k] = (int(shared_u[k]) + RESIDUE_STEP) % WHEEL
                    q_upos[k] = (int(shared_position[k]) + POSITION_STEP) % WHEEL
                    q_out[k] = True
                    q_clicks[k] += 1
                if len(leaving):
                    keep = (left - len(leaving)) / left
                    left -= len(leaving)
                    shared.now = np.rint(shared.now * keep).astype(R.INT)
                    shared.before = np.rint(shared.before * keep).astype(R.INT)
            if q_out.any():
                idx = np.where(q_out)[0]
                n, b, r = batch_step(q_now[idx], q_before[idx], q_rem[idx], read0, own0, wall0)
                # a level on a box's face is a leak (the record reached the box's edge)
                faces = np.zeros((BOX, BOX, BOX), dtype=bool)
                faces[0, :, :] = faces[-1, :, :] = faces[:, 0, :] = faces[:, -1, :] = faces[
                    :, :, 0
                ] = faces[:, :, -1] = True
                q_leaks += int((np.abs(n[:, faces]) > 0).any(axis=1).sum())
                flux_q = batch_inward_flux(n, b)
                increments = flux_q.sum(axis=(1, 2, 3))
                thresholds = (2 * q_u[idx] + 1) * q_norm / (2.0 * WHEEL)
                fires = q_running[idx] + increments >= thresholds
                q_running[idx] += increments
                for local, k in enumerate(idx):
                    if not fires[local]:
                        continue
                    cumulative = np.cumsum(flux_q[local].ravel())
                    point = (2 * int(q_upos[k]) + 1) / (2.0 * WHEEL) * float(cumulative[-1])
                    node = np.unravel_index(
                        min(int(np.searchsorted(cumulative, point)), cumulative.size - 1),
                        (BOX, BOX, BOX),
                    )
                    q_position[k] = (q_position[k] + np.array(node) - centre) % np.array(SHAPE)
                    n[local] = 0
                    b[local] = 0
                    r[local] = 0
                    n[local, centre, centre, centre] = q_level
                    b[local, centre, centre, centre] = q_level
                    q_running[k] = 0.0
                    q_u[k] = (int(q_u[k]) + RESIDUE_STEP) % WHEEL
                    q_upos[k] = (int(q_upos[k]) + POSITION_STEP) % WHEEL
                    q_clicks[k] += 1
                q_now[idx], q_before[idx], q_rem[idx] = n, b, r
    clicks = records[0].clicks if mode != "quantum" else []
    since = [c["since"] for c in clicks][1:]
    quantum_clicks = int(q_clicks.sum()) if mode == "quantum" else None
    return {
        "mode": mode,
        "intervals": intervals,
        "shape": SHAPE,
        "kind": KIND,
        "width": WIDTH,
        "amplitude": AMPLITUDE,
        "wheel": WHEEL,
        "quanta": QUANTA if mode == "quantum" else 1,
        "cos_omega": cos_omega,
        "norm_at_start": t_norm,
        "one_node_amplitude": one_node_level(t_norm, own, wall, *KIND),
        "clicks_total": len(clicks) if mode != "quantum" else quantum_clicks,
        "quanta_leaks": q_leaks if mode == "quantum" else None,
        "mean_interval_between_clicks_per_quantum": (intervals * QUANTA / quantum_clicks)
        if quantum_clicks
        else None,
        "first_click": min((c["t"] for c in clicks), default=None),
        "mean_interval_between_clicks": (sum(since) / len(since)) if since else None,
        "increment_over_norm_at_first_step_after_a_click": [
            c["increment_over_norm"] for c in clicks[1:6]
        ],
        "clicks": clicks[:200],
        "readings": readings,
        "host_seconds": time.time() - t0,
    }


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "whole"
    intervals = int(sys.argv[2]) if len(sys.argv) > 2 else 1500
    if mode == "check":
        print(
            f"HOST the passage check: a moving packet books {passage_check(0.0, *KIND):.4f} of its norm through a plane"
        )
        return
    result = run(mode, intervals)
    print(
        f"{mode}: {result['clicks_total']} clicks, the first at {result['first_click']}, mean interval between clicks {result['mean_interval_between_clicks']}; one-Node amplitude {result['one_node_amplitude']}; {result['host_seconds']:.0f} s"
    )
    print(
        f"  increment over norm at the first step after a click: {result['increment_over_norm_at_first_step_after_a_click']}"
    )
    for r in result["readings"]:
        if r["t"] % 250 == 0:
            print(
                f"  t {r['t']:5d}: width rms {r['width_rms']:6.2f}, peak {r['peak']:9d} at {r['peak_node']}, walk {r['walk']:6.2f}, clicks {r['clicks']}, norm {r['norm_ratio']:.4f}"
            )
    (Path(__file__).resolve().parent / f"item9_clicks_{mode}.json").write_text(
        json.dumps(result, indent=1) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
