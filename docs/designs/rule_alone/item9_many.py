"""THE PAIR IN THE MANY-RECORD FORM (the Boss's record 2167; ALGEBRA.md 9.109 (3), 9.98 (10) (i)):
two bodies held by clicks that keep the momentum, each a body of M records (one per quantum),
20 Links apart, each record reading the other body's content; do the bodies fall together?

AS RUN (HOST choices stated once). Each body is M records, each a packet of rms KEEP_WIDTH at
the body's centre at the start, at rest, on its own box of side BOX about its centre (the
record's levels beyond the box are 0). Every Node
is a detector; each record's ladder is the engine's (2 W C >= (2 u + 1) T on its one-way flux
into the Nodes of its box), its residues its own sequence. At a click the record is re-created
at the click's Node (Born's rule on the record's form) as a packet of the same rms carrying its
momentum K, carried as a label from the start and changed between clicks by the rule's reading
(the reading now less the reading just after the last re-creation), at the same norm; the box
is re-centred at that Node. Each record reads the OTHER body's content: the gravity time part's
static level of item 2's body, s = 2000 on a cube of side 5 about the other body's centroid
Node (relaxed once and rolled to the Node each interval; no self-field; a one-Node source is
125 times weaker and its fall is unreadable in 1500 intervals: the first run). The body's position is the mean of its
records' centroids (GAMEBOARD of the runner); the walk of one record is divided by sqrt M. The
leak is the records' form against their norm, what left through the boxes' faces.

THE CONTROL: `null`, the clicks with no content (no approach expected). `free`, the same
bodies with no click, is no control on boxes: the free packets leave their boxes within tens of
intervals; item 1's fall stands for it.

    PYTHONPATH=src python docs/designs/rule_alone/item9_many.py pair|free|null [M] [intervals]
"""

from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bodies as B  # noqa: E402
import item9_clicks as C  # noqa: E402
import rule_alone as R  # noqa: E402

SHAPE = (96, 48, 48)
WRAP = (True, True, True)
KIND = (800, 850)
AMOUNT = 2000
X_A, X_B = 38, 58
KEEP_WIDTH = 3.5
BOX = 25  # the packet's level at the box's face is 0.3 percent of its peak
WHEEL = C.WHEEL
EVERY = 50
AMPLITUDE = 1 << 11


def box_indices(centre: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    half = BOX // 2
    return tuple((centre[a] - half + np.arange(BOX)) % SHAPE[a] for a in range(3))  # type: ignore[return-value]


def batch_coefficients(content: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    num = np.full(content.shape, KIND[0], dtype=R.INT)
    den = np.full(content.shape, KIND[1], dtype=R.INT)
    return R.coefficients(num, den, content)


def batch_form(
    now: np.ndarray, before: np.ndarray, read: np.ndarray, own: np.ndarray, wall: np.ndarray
) -> np.ndarray:
    """The rule's conserved form per box, in the flux's units (3 den / num)."""
    n = now.astype(np.float64)
    b = before.astype(np.float64)
    inner = (n * n + b * b).sum(axis=(1, 2, 3)) - (own / wall * n * b).sum(axis=(1, 2, 3))
    inner -= (read / wall * b * C.batch_neighbour_sum(now)).sum(axis=(1, 2, 3))
    return 3.0 * KIND[1] / KIND[0] * inner


def batch_currents(now: np.ndarray, before: np.ndarray) -> list[np.ndarray]:
    n = now.astype(np.float64)
    b = before.astype(np.float64)
    out = []
    for axis in (1, 2, 3):
        n_next = np.roll(n, -1, axis=axis)
        b_next = np.roll(b, -1, axis=axis)
        edge = [slice(None)] * 4
        edge[axis] = slice(now.shape[axis] - 1, now.shape[axis])
        n_next[tuple(edge)] = 0.0
        b_next[tuple(edge)] = 0.0
        out.append((n_next * b - n * b_next).sum(axis=(1, 2, 3)))
    return out


def batch_momentum(
    now: np.ndarray, before: np.ndarray, read: np.ndarray, own: np.ndarray, wall: np.ndarray
) -> np.ndarray:
    """K per axis per record: sin K_a = sin omega_K SUM J_a / I, two passes of the dispersion."""
    invariant = batch_form(now, before, read, own, wall) * KIND[0] / (3.0 * KIND[1])
    invariant = np.where(invariant > 0, invariant, np.inf)
    currents = np.stack(batch_currents(now, before), axis=1)
    k = np.zeros_like(currents)
    num, den = KIND
    for _ in range(2):
        two_cos = (num / den) * (2.0 * np.cos(k)).sum(axis=1) / 3.0
        omega_k = np.arccos(np.clip(two_cos / 2.0, -1.0, 1.0))
        k = np.arcsin(np.clip(np.sin(omega_k)[:, None] * currents / invariant[:, None], -1.0, 1.0))
    return k


def packet_box(k: np.ndarray, cos_omega: float) -> tuple[np.ndarray, np.ndarray]:
    """A packet of rms KEEP_WIDTH at the box's centre with the momentum k (unit amplitude)."""
    grids = np.meshgrid(*[np.arange(BOX, dtype=np.float64) - BOX // 2 for _ in range(3)], indexing="ij")
    r2 = sum(g * g for g in grids)
    envelope = np.exp(-r2 / (2.0 * KEEP_WIDTH**2))
    num, den = KIND
    two_cos = (num / den) * sum(2.0 * math.cos(float(v)) for v in k) / 3.0
    omega_k = math.acos(max(-1.0, min(1.0, two_cos / 2.0)))
    phase = sum(float(kv) * g for kv, g in zip(k, grids, strict=True))
    return envelope * np.cos(phase - omega_k / 2.0), envelope * np.cos(phase + omega_k / 2.0)


class Body:
    def __init__(self, centre: tuple[int, int, int], count: int, cos_omega: float, seed: int) -> None:
        self.count = count
        self.centres = np.array([centre] * count, dtype=np.int64)  # each record's box centre
        self.now = np.zeros((count, BOX, BOX, BOX), dtype=R.INT)
        self.before = np.zeros_like(self.now)
        self.remainder = np.zeros_like(self.now)
        unit_now, unit_before = packet_box(np.zeros(3), cos_omega)
        self.now[:] = np.rint(unit_now * AMPLITUDE).astype(R.INT)
        self.before[:] = np.rint(unit_before * AMPLITUDE).astype(R.INT)
        self.u = (C.RESIDUE_START + 97 * seed + C.RESIDUE_STEP * np.arange(count)) % WHEEL
        self.u_position = (C.POSITION_START + 41 * seed + C.POSITION_STEP * np.arange(count)) % WHEEL
        self.running = np.zeros(count)
        self.k_label = np.zeros((count, 3))
        self.k_reference = np.zeros((count, 3))
        self.norm = np.zeros(count)
        self.clicks = 0
        self.leaks = 1.0
        self.cos_omega = cos_omega

    def content_boxes(self, field: np.ndarray) -> np.ndarray:
        out = np.zeros(self.now.shape, dtype=R.INT)
        for q in range(self.count):
            ix, iy, iz = box_indices(self.centres[q])
            out[q] = field[np.ix_(ix, iy, iz)]
        return out

    def centroid(self) -> np.ndarray:
        """The mean over the records of each record's centroid (its box's centre plus the
        offset of its form's centroid within the box), unwrapped about the first record."""
        e2 = R.envelope_squared(self.now, self.before, np.full((1, 1, 1, 1), self.cos_omega))
        totals = e2.sum(axis=(1, 2, 3))
        totals[totals == 0] = 1.0
        offsets = np.arange(BOX, dtype=np.float64) - BOX // 2
        positions = np.zeros((self.count, 3))
        for axis in range(3):
            shape = [1, 1, 1, 1]
            shape[axis + 1] = BOX
            positions[:, axis] = (
                self.centres[:, axis] + (e2 * offsets.reshape(shape)).sum(axis=(1, 2, 3)) / totals
            )
        reference = positions[0]
        for axis in range(3):
            positions[:, axis] = reference[axis] + (
                (positions[:, axis] - reference[axis] + SHAPE[axis] / 2) % SHAPE[axis] - SHAPE[axis] / 2
            )
        return positions.mean(axis=0)

    def step(self, content: np.ndarray, click: bool) -> None:
        read, own, wall = batch_coefficients(content)
        if not self.norm.any():
            self.norm = batch_form(self.now, self.before, read, own, wall)
            self.k_reference = batch_momentum(self.now, self.before, read, own, wall)
            self.k_label = self.k_reference.copy()
        self.now, self.before, self.remainder = C.batch_step(
            self.now, self.before, self.remainder, read, own, wall
        )
        # the leak: the records' form against their norm (what left through the boxes' faces)
        self.leaks = float(np.mean(batch_form(self.now, self.before, read, own, wall) / self.norm))
        if not click:
            return
        flux = C.batch_inward_flux(self.now, self.before)
        increments = flux.sum(axis=(1, 2, 3))
        thresholds = (2 * self.u + 1) * self.norm / (2.0 * WHEEL)
        fires = self.running + increments >= thresholds
        self.running += increments
        if not fires.any():
            return
        cos_local = R.rest_rotation(read, own, wall)
        k_now = batch_momentum(self.now, self.before, read, own, wall)
        for q in np.where(fires)[0]:
            weight = R.envelope_squared(self.now[q], self.before[q], cos_local[q])
            cumulative = np.cumsum(weight.ravel())
            point = (2 * int(self.u_position[q]) + 1) / (2.0 * WHEEL) * float(cumulative[-1])
            node = np.unravel_index(
                min(int(np.searchsorted(cumulative, point)), cumulative.size - 1), (BOX, BOX, BOX)
            )
            self.centres[q] = (self.centres[q] + np.array(node) - BOX // 2) % np.array(SHAPE)
            self.k_label[q] = self.k_label[q] + (k_now[q] - self.k_reference[q])
            unit_now, unit_before = packet_box(self.k_label[q], self.cos_omega)
            trial_now = np.rint(unit_now * 1024).astype(R.INT)[None]
            trial_before = np.rint(unit_before * 1024).astype(R.INT)[None]
            unit_norm = batch_form(
                trial_now, trial_before, read[q : q + 1], own[q : q + 1], wall[q : q + 1]
            )[0]
            scale = 1024.0 * math.sqrt(self.norm[q] / unit_norm) if unit_norm > 0 else 1024.0
            self.now[q] = np.rint(unit_now * scale).astype(R.INT)
            self.before[q] = np.rint(unit_before * scale).astype(R.INT)
            self.remainder[q] = 0
            self.k_reference[q] = batch_momentum(
                self.now[q : q + 1],
                self.before[q : q + 1],
                read[q : q + 1],
                own[q : q + 1],
                wall[q : q + 1],
            )[0]
            self.running[q] = 0.0
            self.u[q] = (self.u[q] + C.RESIDUE_STEP) % WHEEL
            self.u_position[q] = (self.u_position[q] + C.POSITION_STEP) % WHEEL
            self.clicks += 1


def run(mode: str, count: int, intervals: int) -> dict:
    num = np.full(SHAPE, KIND[0], dtype=R.INT)
    den = np.full(SHAPE, KIND[1], dtype=R.INT)
    read0, own0, wall0 = R.coefficients(num, den, np.zeros(SHAPE, dtype=R.INT))
    cos_omega = float(R.rest_rotation(read0, own0, wall0)[0, 0, 0])
    middle = SHAPE[1] // 2
    lone = B.lone_static_field(
        SHAPE, WRAP, B.Body([SHAPE[0] // 2, middle, middle], AMOUNT, side=5, kind=KIND, well=KIND)
    )
    a = Body((X_A, middle, middle), count, cos_omega, 0)
    b = Body((X_B, middle, middle), count, cos_omega, 1)
    click = mode != "free"
    with_content = mode != "null"
    zero = np.zeros(SHAPE, dtype=R.INT)
    readings: list[dict] = []
    t0 = time.time()
    xa, xb = float(X_A), float(X_B)
    ca, cb = a.centroid(), b.centroid()
    for t in range(intervals + 1):
        if t % EVERY == 0:
            readings.append(
                {
                    "t": t,
                    "x_a": xa,
                    "x_b": xb,
                    "separation": xb - xa,
                    "clicks_a": a.clicks,
                    "clicks_b": b.clicks,
                    "leaks_a": a.leaks,
                    "leaks_b": b.leaks,
                    "k_a_mean": a.k_label.mean(axis=0).tolist(),
                    "k_b_mean": b.k_label.mean(axis=0).tolist(),
                }
            )
        if t == intervals:
            break
        if with_content:
            node_a = np.rint(ca).astype(int) % np.array(SHAPE)
            node_b = np.rint(cb).astype(int) % np.array(SHAPE)
            field_for_a = np.roll(
                lone, [int(node_b[i]) - SHAPE[i] // 2 for i in range(3)], axis=(0, 1, 2)
            )
            field_for_b = np.roll(
                lone, [int(node_a[i]) - SHAPE[i] // 2 for i in range(3)], axis=(0, 1, 2)
            )
        else:
            field_for_a = field_for_b = zero
        a.step(a.content_boxes(field_for_a), click)
        b.step(b.content_boxes(field_for_b), click)
        new_a, new_b = a.centroid(), b.centroid()
        xa += (new_a[0] - ca[0] + SHAPE[0] / 2) % SHAPE[0] - SHAPE[0] / 2
        xb += (new_b[0] - cb[0] + SHAPE[0] / 2) % SHAPE[0] - SHAPE[0] / 2
        ca, cb = new_a, new_b
    return {
        "mode": mode,
        "records_per_body": count,
        "intervals": intervals,
        "shape": SHAPE,
        "kind": KIND,
        "amount": AMOUNT,
        "keep_width": KEEP_WIDTH,
        "box": BOX,
        "readings": readings,
        "clicks": [a.clicks, b.clicks],
        "leaks": [a.leaks, b.leaks],
        "host_seconds": time.time() - t0,
    }


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "pair"
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    intervals = int(sys.argv[3]) if len(sys.argv) > 3 else 1500
    result = run(mode, count, intervals)
    print(
        f"item9_many_{mode}_m{count}: clicks {result['clicks']}, leaks {result['leaks']}; {result['host_seconds']:.0f} s"
    )
    for r in result["readings"]:
        if r["t"] % 250 == 0:
            print(
                f"  t {r['t']:5d}: x_a {r['x_a']:6.2f}, x_b {r['x_b']:6.2f}, separation {r['separation']:6.2f}, clicks {r['clicks_a']} {r['clicks_b']}, k_a x {r['k_a_mean'][0]:+.4f}, k_b x {r['k_b_mean'][0]:+.4f}"
            )
    (Path(__file__).resolve().parent / f"item9_many_{mode}_m{count}.json").write_text(
        json.dumps(result, indent=1) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
