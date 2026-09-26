"""THE RUNS OF ALGEBRA.md 9.98 (11) AND 9.108 (the Boss's records 2157 and 2163): THE BINDING AS A
FAMILY, the mathematician's generic line (c) and its two corrected forms, in Nature24's runner
of the rule 9.57 (1) in integers.

THE LINE, as run (HOST choices stated once):
- every record writes at every Node of its support its local count s_i into the t part of
  gravity and of the binding family (and of the core family in the two-family form). F_i is
  the record's form at the Node from its own pair, F_i = now^2 + before^2 - 2 now before cos
  omega_i, cos omega_i the Node's rest rotation at the content read there in the interval
  before. E_s is the level's: F_peak(0) div s, the peak Node reading s = 2000 at the start.
- the hold: at every interval, after the held families' step, both levels of every held family
  at the support (s_i > 0) are written to s_i (the engine's hold, the order of 9.85 (2)).
- gravity's pair [1, 1]; the binding family's pair [1000, 1019] (cosh kappa = 3 den / num - 2,
  the range 1 / kappa = 3 Links); the core family's pair [1000, 1181] (the range 1 Link).
- the record's pace at a Node p_0,i = Gamma - g_i - K_m b_i + K_r h_i (the weights 1, +K_m and
  -K_r: a hollow, a hollow and a hill, 9.108 (7), (8)); the record steps by the rule with these
  coefficients; no pair well anywhere, the kind [800, 850] on every Node, no hop, no tally.
- the held families step by the plain rule at the pace Gamma (`pace=0`) or at the Node's pace,
  the same coefficients as the record's (`pace=1`, 9.108 (5): every field instance at the pace).
- the board 48^3 with open faces (a level 0 beyond a face; the runner's face reflects); the
  record starts as a standing Gaussian of sigma = side / 2 at amplitude 2^17 (a start, not the
  mode; the mode is what the run settles to).

THE FORMS OF THE SOURCE (`source=`):
- `level`: s_i = F_i div E_s (9.98 (11) (c) as written).
- `count`: E_s = SUM F_i(0) div s, the counts summing to s.
- `cap`: `level` with s_i cut at s.
- `table`: s_i = s_cap F_i div (s_cap E_s + F_i), the saturating divide of 9.108 (3), `scap=`.
- `core`: `level` into the binding family and, scaled by `corescale=a/b` (E_core = E_s a / b),
  into the core family read with -K_r (`kr=`), 9.108 (7).
- `sourced`: the binding and the core SOURCED, not held (9.108 (10) (a) to (d)): each interval
  the record's local count s_i = F_i div E_s is ADDED into each family's now level at its Nodes,
  and each family steps by the rule at the Node's pace with its own pair; gravity stays the
  hold. The fields start at the static response to the start's source (the screened Poisson
  solution of the plain rule, (2 - M) a = s, by relaxation, HOST), and E_s is set by that
  response so that K_m b - K_r h at the start's peak is 1500 (`floor=`). The conserved total
  of 9.108 (10) (c), the record's form plus the two fields' forms over E_s plus the coupling
  K_m SUM b_i s_i - K_r SUM h_i s_i, is read beside its pieces. `wrap=1` puts the run on a
  periodic board of 64 (the start a Gaussian, as (b) allows).
The guard p > 0 (the content reaching Gamma) ends a run and is reported with its interval.
THE FOUR CORRECTIONS OF 9.108 item 12 (the mathematician, 2026-09-26), each an option so the
earlier runs stand unchanged:
- (i) the guard is two-sided: a content below 0 (a pace above Gamma) ends the run as well, with
  the side named (`guard_side`).
- (ii) `passes=N` (0 off): THE STATIONARY START AT THE PACE. The record's ground mode and the
  fields' static levels are iterated together N times: the record's standing mode is the
  eigenvector of the rule's step operator M(content) with the largest 2 cos omega (a power
  iteration shifted by 2, HOST floats, `MODE_SWEEPS` sweeps), the sources are its counts, the
  fields' static response (or the held fields' exterior, relaxed with the support's levels held)
  at the pace of the content gives the next content. The passes' report is in the output.
- (iii) `sponge=L` (0 off): ABSORBING FACES as a layer of L Nodes at every face where every
  stepping level is damped each interval by (1 - d), d = SPONGE_STRENGTH x ((L - distance) / L)^2,
  in integers (the damped part rounded); a HOST device standing in for the receiver faces the
  engine will declare; it touches the record's tails too and the leak reading shows it.
- (iv) the adiabatic condition is a choice of v (v / w against the fields' rotations).
- THE RINGING READING: the level of each sourced field at the start's peak Node every interval;
  per window of 300 the amplitude (max - min) / (2 |mean|) (`ringing_300`); under 5 percent is the
  reading that decides (9.108 item 12).
- `n=` the side of the open board (48 by default).

THE READINGS (GAMEBOARD of the runner) every 25 intervals: the centroid of F, the rms width about
it, the peak level and Node, the count SUM s_i and the peak's s_i, the content at the peak, the
rotation (the time average of 2 SUM now before / SUM (now^2 + before^2) over the window), the
bound share (F within 12 Links of the centroid over the total), the record's form at the current
coefficients over its start, and the binding family's own form at its coefficients (9.108 (4):
the record's form and the field's in antiphase; the mean of the record's form over windows of
300 intervals, no drift).

    PYTHONPATH=src python docs/designs/rule_alone/binding_family.py rest side=9 km=2 source=table scap=4000
    PYTHONPATH=src python docs/designs/rule_alone/binding_family.py moving side=9 km=2 v=0.05 source=core kr=1 corescale=3/2
    PYTHONPATH=src python docs/designs/rule_alone/binding_family.py pair side=9 km=2 source=table scap=4000 pace=1
"""

from __future__ import annotations

import json
import math
import sys
import time
from fractions import Fraction
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rule_alone as R  # noqa: E402

SHAPE = (48, 48, 48)
WRAP = (False, False, False)
PERIODIC_SHAPE = (64, 64, 64)
KIND = (800, 850)
GRAVITY_PAIR = (1, 1)
BINDING_PAIR = (1000, 1019)  # cosh kappa = 3 den / num - 2 = 1.057: the range 3 Links
CORE_PAIR = (1000, 1181)  # cosh kappa = 1.543: the range 1 Link
COUNT = 2000
AMPLITUDE = 1 << 17
EVERY = 25
BOUND_RADIUS = 12
PAIR_SEPARATION = 20
WINDOW = 300
MODE_SWEEPS = 1200
MODE_SWEEPS_WARM = 400
SPONGE_STRENGTH = 0.12


def wave_number(speed: float, num: int, den: int) -> tuple[float, float]:
    def pace(k: float) -> float:
        omega = math.acos((num / den) * (2.0 * math.cos(k) + 4.0) / 6.0)
        return (num / (3.0 * den)) * math.sin(k) / math.sin(omega)

    low, high = 0.0, 1.5
    for _ in range(80):
        mid = 0.5 * (low + high)
        if pace(mid) < speed:
            low = mid
        else:
            high = mid
    k = 0.5 * (low + high)
    return k, math.acos((num / den) * (2.0 * math.cos(k) + 4.0) / 6.0)


class Field:
    """A held family stepping by the rule with its own pair, at the pace Gamma or the Node's."""

    def __init__(self, pair: tuple[int, int]) -> None:
        self.num = np.full(SHAPE, pair[0], dtype=R.INT)
        self.den = np.full(SHAPE, pair[1], dtype=R.INT)
        self.plain = R.coefficients(self.num, self.den, np.zeros(SHAPE, dtype=R.INT))
        self.coefficients = self.plain
        self.now = np.zeros(SHAPE, dtype=R.INT)
        self.before = np.zeros(SHAPE, dtype=R.INT)
        self.remainder = np.zeros(SHAPE, dtype=R.INT)

    def step(self, content: np.ndarray | None) -> None:
        self.coefficients = (
            self.plain if content is None else R.coefficients(self.num, self.den, content)
        )
        read, own, wall = self.coefficients
        self.now, self.before, self.remainder = R.step(
            self.now, self.before, self.remainder, read, own, wall, WRAP
        )

    def hold(self, support: np.ndarray, level: np.ndarray) -> None:
        self.now[support] = level[support]
        self.before[support] = level[support]

    def inject(self, level: np.ndarray) -> None:
        """The source: the count added into the now level at the record's Nodes."""
        self.now = self.now + level

    def static_response(
        self,
        source: np.ndarray,
        sweeps: int = 4000,
        coefficients: tuple[np.ndarray, np.ndarray, np.ndarray] | None = None,
    ) -> np.ndarray:
        """The steady level of the sourced field, (2 - M) a = s with M the rule's operator
        at the given coefficients (a_next = M a - a_before + s): Jacobi relaxation, HOST floats."""
        read, own, wall = self.plain if coefficients is None else coefficients
        r = read.astype(np.float64) / wall.astype(np.float64)
        s_over_w = own.astype(np.float64) / wall.astype(np.float64)
        a = np.zeros(SHAPE, dtype=np.float64)
        src = source.astype(np.float64)
        for _ in range(sweeps):
            a = 0.5 * (r * R.neighbour_sum(a, WRAP) + s_over_w * a) + 0.5 * src
        return a

    def start_static(self, source: np.ndarray, content: np.ndarray | None = None) -> None:
        coefficients = None if content is None else R.coefficients(self.num, self.den, content)
        level = np.rint(self.static_response(source, coefficients=coefficients)).astype(R.INT)
        self.coefficients = self.plain if coefficients is None else coefficients
        self.now = level.copy()
        self.before = level.copy()
        self.remainder = np.zeros(SHAPE, dtype=R.INT)

    def static_hold(
        self,
        support: np.ndarray,
        level: np.ndarray,
        content: np.ndarray | None = None,
        sweeps: int = 4000,
    ) -> None:
        """The steady exterior of a held field: (2 - M) a = 0 outside the support with a held
        at the support's levels, by relaxation (HOST floats); the start of a held family."""
        coefficients = None if content is None else R.coefficients(self.num, self.den, content)
        read, own, wall = self.plain if coefficients is None else coefficients
        r = read.astype(np.float64) / wall.astype(np.float64)
        s_over_w = own.astype(np.float64) / wall.astype(np.float64)
        a = np.zeros(SHAPE, dtype=np.float64)
        held = level.astype(np.float64)
        for _ in range(sweeps):
            a = 0.5 * (r * R.neighbour_sum(a, WRAP) + s_over_w * a)
            a[support] = held[support]
        self.coefficients = self.plain if coefficients is None else coefficients
        self.now = np.rint(a).astype(R.INT)
        self.before = self.now.copy()
        self.remainder = np.zeros(SHAPE, dtype=R.INT)

    def sponge(self, damping: np.ndarray | None) -> None:
        if damping is not None:
            self.now = self.now - np.rint(self.now * damping).astype(R.INT)
            self.before = self.before - np.rint(self.before * damping).astype(R.INT)

    def form(self) -> float:
        read, own, wall = self.coefficients
        return conserved(self.now, self.before, read, own, wall)


def damping_profile(layer: int) -> np.ndarray | None:
    """The sponge of 9.108 item 12 (iii): d = SPONGE_STRENGTH ((L - distance) / L)^2 within L
    Nodes of an open face, 0 elsewhere (HOST)."""
    if layer <= 0:
        return None
    grids = np.meshgrid(*[np.arange(n, dtype=np.float64) for n in SHAPE], indexing="ij")
    distance = np.full(SHAPE, np.inf)
    for axis, g in enumerate(grids):
        if not WRAP[axis]:
            distance = np.minimum(distance, np.minimum(g, SHAPE[axis] - 1 - g))
    inside = np.clip((layer - distance) / layer, 0.0, 1.0)
    return SPONGE_STRENGTH * inside * inside


def ground_mode(
    coefficients: tuple[np.ndarray, np.ndarray, np.ndarray],
    warm: np.ndarray,
    sweeps: int,
) -> tuple[np.ndarray, float, float]:
    """The record's standing mode under the content: the eigenvector of M = (R N + S) / w with
    the largest eigenvalue 2 cos omega, by a power iteration on M + 2 (the shift puts the K = pi
    modes, 2 cos omega near -2, at the bottom); HOST floats. Returns (phi with max 1, 2 cos omega,
    the residual |(M + 2) phi - (lambda + 2) phi| over |phi|)."""
    read, own, wall = coefficients
    r = read.astype(np.float64) / wall.astype(np.float64)
    s_over_w = own.astype(np.float64) / wall.astype(np.float64)
    phi = warm.astype(np.float64)
    phi = phi / np.sqrt((phi * phi).sum())
    lam = 0.0
    for _ in range(sweeps):
        m_phi = r * R.neighbour_sum(phi, WRAP) + s_over_w * phi + 2.0 * phi
        norm = float(np.sqrt((m_phi * m_phi).sum()))
        phi = m_phi / norm
    m_phi = r * R.neighbour_sum(phi, WRAP) + s_over_w * phi
    lam = float((phi * m_phi).sum())
    residual = float(np.sqrt(((m_phi - lam * phi) ** 2).sum()))
    return phi / phi.max(), lam, residual


class Record:
    def __init__(self, now: np.ndarray, before: np.ndarray) -> None:
        self.now = now
        self.before = before
        self.remainder = np.zeros(SHAPE, dtype=R.INT)
        self.cos_omega = np.full(SHAPE, 0.0)
        self.e_s = 1
        self.form_window: list[float] = []
        self.form_means: list[float] = []


def packet(
    centre: tuple[float, float, float],
    sigma: float,
    cos_omega: float,
    k: float = 0.0,
    omega_k: float = 0.0,
) -> tuple[np.ndarray, np.ndarray]:
    grids = np.meshgrid(*[np.arange(n, dtype=np.float64) for n in SHAPE], indexing="ij")
    r2 = sum((g - c) ** 2 for g, c in zip(grids, centre, strict=True))
    envelope = AMPLITUDE * np.exp(-r2 / (2.0 * sigma * sigma))
    if k == 0.0:
        return np.rint(envelope).astype(R.INT), np.rint(envelope * cos_omega).astype(R.INT)
    dx = grids[0] - centre[0]
    return (
        np.rint(envelope * np.cos(k * dx - omega_k / 2.0)).astype(R.INT),
        np.rint(envelope * np.cos(k * dx + omega_k / 2.0)).astype(R.INT),
    )


def form_of(record: Record) -> np.ndarray:
    n = record.now.astype(np.float64)
    b = record.before.astype(np.float64)
    return np.maximum(n * n + b * b - 2.0 * n * b * record.cos_omega, 0.0)


def conserved(
    now: np.ndarray, before: np.ndarray, read: np.ndarray, own: np.ndarray, wall: np.ndarray
) -> float:
    n = now.astype(np.float64)
    b = before.astype(np.float64)
    return float(
        (n * n + b * b).sum()
        - (own / wall * n * b).sum()
        - (read / wall * b * R.neighbour_sum(now, WRAP)).sum()
    )


def source_counts(form: np.ndarray, e_s: int, source: str, s_cap: int) -> np.ndarray:
    integer = form.astype(np.int64)
    if source == "table":
        # the saturating divide of 9.108 (3), in integers
        return (s_cap * integer) // (s_cap * e_s + integer)
    count = integer // e_s
    if source == "cap":
        count = np.minimum(count, COUNT)
    return count.astype(R.INT)


def readings_of(
    record: Record, form: np.ndarray, content: np.ndarray, count: np.ndarray, window: list[float]
) -> dict:
    total = float(form.sum())
    cx, cy, cz = R.centroid(form)
    grids = np.meshgrid(*[np.arange(n, dtype=np.float64) for n in SHAPE], indexing="ij")
    r2 = (grids[0] - cx) ** 2 + (grids[1] - cy) ** 2 + (grids[2] - cz) ** 2
    width = math.sqrt(float((form * r2).sum()) / total / 3.0) if total > 0 else float("nan")
    peak = np.unravel_index(int(np.argmax(form)), SHAPE)
    bound = float(form[r2 <= BOUND_RADIUS**2].sum()) / total if total > 0 else float("nan")
    xs = np.arange(SHAPE[0])
    line = form[:, int(round(cy)) % SHAPE[1], int(round(cz)) % SHAPE[2]]
    r_line = xs - cx
    inside = (r_line >= 6) & (r_line <= 12) & (line > 0)
    tail = float("nan")
    if inside.sum() >= 3:
        slope = np.polyfit(r_line[inside], np.log(line[inside]), 1)[0]
        tail = -2.0 / slope if slope < 0 else float("inf")
    cos_eff = float(np.mean(window)) if window else float("nan")
    return {
        "centroid": [cx, cy, cz],
        "width_rms": width,
        "peak": int(form.max() ** 0.5),
        "peak_node": [int(v) for v in peak],
        "count_sum": int(count.sum()),
        "count_peak": int(count[peak]),
        "content_peak": int(content[peak]),
        "bound_share_12": bound,
        "tail_links": tail,
        "cos_omega_eff": cos_eff,
        "omega_eff": math.acos(max(-1.0, min(1.0, cos_eff))) if window else float("nan"),
    }


def run(options: dict) -> dict:
    mode = options["mode"]
    side = int(options.get("side", 9))
    k_m = int(options.get("km", 2))
    k_r = int(options.get("kr", 0))
    speed = float(options.get("v", 0.0))
    intervals = int(options.get("t", 1500))
    source = options.get("source", "level")
    s_cap = int(options.get("scap", 4000))
    core_scale = Fraction(options.get("corescale", "1"))
    at_pace = options.get("pace", "0") == "1"
    floor = int(options.get("floor", 1500))
    passes = int(options.get("passes", 0))
    sponge_layer = int(options.get("sponge", 0))
    global SHAPE, WRAP
    if options.get("wrap", "0") == "1":
        SHAPE, WRAP = PERIODIC_SHAPE, (True, True, True)
    elif "n" in options:
        SHAPE, WRAP = (int(options["n"]),) * 3, (False, False, False)
    damping = damping_profile(sponge_layer)
    num = np.full(SHAPE, KIND[0], dtype=R.INT)
    den = np.full(SHAPE, KIND[1], dtype=R.INT)
    read0, own0, wall0 = R.coefficients(num, den, np.zeros(SHAPE, dtype=R.INT))
    cos_vacuum = float(R.rest_rotation(read0, own0, wall0)[0, 0, 0])
    middle = SHAPE[1] / 2.0
    gravity, binding = Field(GRAVITY_PAIR), Field(BINDING_PAIR)
    core = Field(CORE_PAIR) if source in ("core", "sourced") else None
    sourced = source == "sourced"
    static_peak = None
    sigma = side / 2.0
    records: list[Record] = []
    x_start = SHAPE[0] / 2.0 - 8 if mode == "moving" else SHAPE[0] / 2.0
    if mode == "pair":
        for x in (SHAPE[0] / 2.0 - PAIR_SEPARATION / 2.0, SHAPE[0] / 2.0 + PAIR_SEPARATION / 2.0):
            records.append(Record(*packet((x, middle, middle), sigma, cos_vacuum)))
    elif mode == "moving":
        k, omega_k = wave_number(speed, *KIND)
        records.append(Record(*packet((x_start, middle, middle), sigma, cos_vacuum, k, omega_k)))
    else:
        records.append(Record(*packet((x_start, middle, middle), sigma, cos_vacuum)))
    for record in records:
        record.cos_omega = np.full(SHAPE, cos_vacuum)
        form = form_of(record)
        record.e_s = (
            max(1, int(form.sum()) // COUNT) if source == "count" else max(1, int(form.max()) // COUNT)
        )
    if sourced and core is not None:
        # E_s by the static response (9.108 (10) (b)): the unit source is the start's form over
        # its peak; the peak's count makes K_m b - K_r h at the peak equal to the floor
        unit = sum(form_of(r) for r in records)
        unit = unit / unit.max()
        b_unit = binding.static_response(unit)
        h_unit = core.static_response(unit)
        peak = np.unravel_index(int(np.argmax(unit)), SHAPE)
        per_count = k_m * float(b_unit[peak]) - k_r * float(h_unit[peak])
        if per_count <= 0:
            raise ValueError(f"the net well per unit count at the peak is {per_count:.3f}: no hollow")
        s_peak = floor / per_count
        for record in records:
            record.e_s = max(1, int(form_of(record).max() / s_peak))
        start_source = np.zeros(SHAPE, dtype=R.INT)
        for record in records:
            start_source += (form_of(record).astype(np.int64) // record.e_s).astype(R.INT)
        # two passes: the plain static response gives the content, and the fields' static
        # response at the Node's pace of that content is the start (the paced step's own
        # stationary state, else the well falls fourfold in 25 intervals: the first run)
        binding.start_static(start_source)
        core.start_static(start_source)
        if at_pace:
            gravity_start = np.zeros(SHAPE, dtype=R.INT)
            gravity_start[start_source > 0] = start_source[start_source > 0]
            start_content = gravity_start + k_m * binding.now - k_r * core.now
            binding.start_static(start_source, start_content)
            core.start_static(start_source, start_content)
        static_peak = k_m * int(binding.now[peak]) - k_r * int(core.now[peak])
    e_core = max(1, int(records[0].e_s * core_scale))
    passes_report: list[dict] = []
    if passes > 0:
        # 9.108 item 12 (ii): the record's mode and the fields' static levels iterated together
        # under the pace the fields make; E_s as set above (the floor rule at the Gaussian)
        start_content = np.zeros(SHAPE, dtype=R.INT)
        modes: list[np.ndarray] = [form_of(r) ** 0.5 for r in records]
        grids = np.meshgrid(*[np.arange(n, dtype=np.float64) for n in SHAPE], indexing="ij")
        for index_pass in range(passes):
            # the fields' static levels from the records as they stand (the Gaussian at the
            # first pass), at the pace of the content of the pass before
            level_start = np.zeros(SHAPE, dtype=R.INT)
            level_core_start = np.zeros(SHAPE, dtype=R.INT)
            for record in records:
                form = form_of(record)
                level_start += source_counts(form, record.e_s, source, s_cap)
                if core is not None:
                    level_core_start += (form.astype(np.int64) // e_core).astype(R.INT)
            support_start = level_start > 0
            pace_start = start_content if (at_pace and index_pass > 0) else None
            gravity.static_hold(support_start, level_start, pace_start)
            if sourced and core is not None:
                binding.start_static(level_start, pace_start)
                core.start_static(level_start, pace_start)
            else:
                binding.static_hold(support_start, level_start, pace_start)
                if core is not None:
                    core.static_hold(support_start, level_core_start, pace_start)
            new_content = gravity.now + k_m * binding.now
            if core is not None:
                new_content = new_content - k_r * core.now
            excess_nodes = int((new_content < 0).sum())
            excess_max = int(-new_content.min()) if excess_nodes else 0
            new_content = np.maximum(new_content, 0)
            change = int(np.abs(new_content - start_content).max())
            start_content = new_content
            peak_now = np.unravel_index(int(np.argmax(level_start)), SHAPE)
            # the record's standing mode under that content
            coefficients = R.coefficients(num, den, start_content)
            cos_local_start = R.rest_rotation(*coefficients)
            omegas, residuals = [], []
            for index, record in enumerate(records):
                phi, lam, residual = ground_mode(
                    coefficients, modes[index], MODE_SWEEPS if index_pass == 0 else MODE_SWEEPS_WARM
                )
                modes[index] = phi
                omegas.append(math.acos(max(-1.0, min(1.0, lam / 2.0))))
                residuals.append(residual)
                envelope = AMPLITUDE * phi
                if mode == "moving":
                    k, omega_k = wave_number(speed, *KIND)
                    centre_x = R.centroid(phi * phi)[0]
                    dx = grids[0] - centre_x
                    record.now = np.rint(envelope * np.cos(k * dx - omega_k / 2.0)).astype(R.INT)
                    record.before = np.rint(envelope * np.cos(k * dx + omega_k / 2.0)).astype(R.INT)
                else:
                    record.now = np.rint(envelope).astype(R.INT)
                    record.before = np.rint(envelope * (lam / 2.0)).astype(R.INT)
                record.remainder = np.zeros(SHAPE, dtype=R.INT)
                record.cos_omega = cos_local_start
            passes_report.append(
                {
                    "pass": index_pass,
                    "omega_mode": omegas,
                    "mode_residual": residuals,
                    "content_peak": int(start_content[peak_now]),
                    "content_max": int(start_content.max()),
                    "hill_excess_nodes": excess_nodes,
                    "hill_excess_max": excess_max,
                    "count_sum": int(level_start.sum()),
                    "count_peak": int(level_start[peak_now]),
                    "content_change_max": change,
                }
            )
        static_peak = int(start_content[peak_now])
    guard_interval = None
    guard_content = 0
    guard_side = None
    ring_node = np.unravel_index(int(np.argmax(sum(form_of(r) for r in records))), SHAPE)
    ring_levels: dict[str, list[int]] = {"binding": [], "core": []}
    ringing: dict[str, list[float]] = {"binding": [], "core": []}
    i_start: list[float] | None = None
    windows: list[list[float]] = [[] for _ in records]
    readings: list[dict] = []
    t0 = time.time()
    content = np.zeros(SHAPE, dtype=R.INT)
    for t in range(intervals + 1):
        counts = []
        support = np.zeros(SHAPE, dtype=bool)
        level = np.zeros(SHAPE, dtype=R.INT)
        level_core = np.zeros(SHAPE, dtype=R.INT)
        for record in records:
            form = form_of(record)
            count = source_counts(form, record.e_s, source, s_cap)
            counts.append(count)
            support |= count > 0
            level += count
            if core is not None:
                level_core += (form.astype(np.int64) // e_core).astype(R.INT)
        pace_content = content if at_pace and t > 0 else None
        gravity.step(pace_content)
        gravity.hold(support, level)
        if sourced and core is not None:
            # the sourced fields: the step at the Node's pace, then the count added (the
            # static start makes a constant source stationary: a = M a - a + s)
            binding.step(pace_content)
            binding.inject(level)
            core.step(pace_content)
            core.inject(level)
        else:
            binding.step(pace_content)
            binding.hold(support, level)
            if core is not None:
                core.step(pace_content)
                core.hold(support, level_core)
        binding.sponge(damping)
        if core is not None:
            core.sponge(damping)
        content = gravity.now + k_m * binding.now
        if core is not None:
            content = content - k_r * core.now
        # 9.108 item 12 (i): the pace bounded on both sides, 0 < p <= Gamma: a content below 0 (a
        # hill exceeding the hollow, here by the integer tails) is cut at 0 and counted; a content
        # at or above Gamma ends the run
        hill_excess_nodes = int((content < 0).sum())
        hill_excess_max = int(-content.min()) if hill_excess_nodes else 0
        content = np.maximum(content, 0)
        if int(content.max()) >= R.GAMMA:
            guard_interval = t
            guard_side = "pace at or below 0"
            guard_content = int(content.max())
            break
        for name, field in (("binding", binding), ("core", core)):
            if field is not None:
                ring_levels[name].append(int(field.now[ring_node]))
                if len(ring_levels[name]) == WINDOW:
                    values = np.array(ring_levels[name], dtype=np.float64)
                    mean = abs(float(values.mean()))
                    ringing[name].append(
                        float((values.max() - values.min()) / (2.0 * mean)) if mean > 0 else float("inf")
                    )
                    ring_levels[name] = []
        read, own, wall = R.coefficients(num, den, content)
        cos_local = R.rest_rotation(read, own, wall)
        forms = [conserved(r.now, r.before, read, own, wall) for r in records]
        if t == 0:
            i_start = forms
        for index, record in enumerate(records):
            record.form_window.append(
                forms[index] / i_start[index] if i_start and i_start[index] else float("nan")
            )
            if len(record.form_window) == WINDOW:
                record.form_means.append(float(np.mean(record.form_window)))
                record.form_window = []
        if t % EVERY == 0:
            row: dict = {"t": t, "binding_form": binding.form()}
            if core is not None:
                row["core_form"] = core.form()
            if sourced and core is not None:
                # the conserved total of 9.108 (10) (c): the record's form, the fields' forms
                # over E_s, the coupling K_m SUM b s - K_r SUM h s, counted once
                s_total = level.astype(np.float64)
                coupling = k_m * float((binding.now * s_total).sum()) - k_r * float(
                    (core.now * s_total).sum()
                )
                e_s = records[0].e_s
                row["coupling"] = coupling
                row["total"] = sum(forms) + (row["binding_form"] + row["core_form"]) / e_s + coupling
                row["content_max"] = int(content.max())
                row["content_min"] = int(content.min())
            row["hill_excess_nodes"] = hill_excess_nodes
            row["hill_excess_max"] = hill_excess_max
            for index, record in enumerate(records):
                reading = readings_of(record, form_of(record), content, counts[index], windows[index])
                reading["leak"] = (
                    forms[index] / i_start[index] if i_start and i_start[index] else float("nan")
                )
                row[f"record_{index}"] = reading
                windows[index] = []
            if mode == "pair":
                row["separation"] = row["record_1"]["centroid"][0] - row["record_0"]["centroid"][0]
            if mode == "moving":
                row["expected_x"] = x_start + speed * t
            readings.append(row)
        if t == intervals:
            break
        for index, record in enumerate(records):
            n = record.now.astype(np.float64)
            b = record.before.astype(np.float64)
            denominator = float((n * n + b * b).sum())
            if denominator > 0:
                windows[index].append(2.0 * float((n * b).sum()) / denominator)
            record.now, record.before, record.remainder = R.step(
                record.now, record.before, record.remainder, read, own, wall, WRAP
            )
            if damping is not None:
                record.now = record.now - np.rint(record.now * damping).astype(R.INT)
                record.before = record.before - np.rint(record.before * damping).astype(R.INT)
            record.cos_omega = cos_local
    return {
        "options": options,
        "mode": mode,
        "side": side,
        "k_m": k_m,
        "k_r": k_r,
        "speed": speed,
        "intervals": intervals,
        "source": source,
        "s_cap": s_cap if source == "table" else None,
        "core_scale": str(core_scale) if core is not None else None,
        "fields_at_pace": at_pace,
        "shape": SHAPE,
        "kind": KIND,
        "binding_pair": BINDING_PAIR,
        "core_pair": CORE_PAIR if core is not None else None,
        "count": COUNT,
        "amplitude": AMPLITUDE,
        "guard_interval": guard_interval,
        "guard_content": guard_content if guard_interval is not None else None,
        "guard_side": guard_side,
        "passes": passes,
        "passes_report": passes_report,
        "sponge_layer": sponge_layer,
        "sponge_strength": SPONGE_STRENGTH if sponge_layer > 0 else None,
        "ringing_300": ringing,
        "ring_node": [int(v) for v in ring_node],
        "e_s": [r.e_s for r in records],
        "e_core": e_core if core is not None else None,
        "static_floor_at_peak": static_peak,
        "floor_asked": floor if sourced else None,
        "wrap": WRAP,
        "cos_omega_vacuum": cos_vacuum,
        "omega_vacuum": math.acos(cos_vacuum),
        "form_means_300": [r.form_means for r in records],
        "readings": readings,
        "host_seconds": time.time() - t0,
    }


def main() -> None:
    options: dict = {"mode": sys.argv[1]}
    for item in sys.argv[2:]:
        key, _, value = item.partition("=")
        options[key] = value
    result = run(options)
    name = "binding_" + "_".join(f"{k}{v}".replace("/", "over") for k, v in options.items())
    guard = (
        f"; THE GUARD at interval {result['guard_interval']} ({result['guard_side']}, content {result['guard_content']})"
        if result["guard_interval"] is not None
        else ""
    )
    print(
        f"{name}: E_s {result['e_s']}, E_core {result['e_core']}, omega_vacuum {result['omega_vacuum']:.4f}; {result['host_seconds']:.0f} s{guard}"
    )
    for row in result["readings"]:
        if row["t"] % 250 == 0 or row["t"] == 25:
            r = row["record_0"]
            extra = f", separation {row['separation']:.2f}" if "separation" in row else ""
            extra += f", expected x {row['expected_x']:.1f}" if "expected_x" in row else ""
            print(
                f"  t {row['t']:5d}: centroid x {r['centroid'][0]:6.2f}, width {r['width_rms']:5.2f}, tail {r['tail_links']:5.1f}, "
                f"peak {r['peak']:7d}, count sum {r['count_sum']:7d} peak {r['count_peak']:5d}, content {r['content_peak']:5d}, "
                f"omega {r['omega_eff']:.4f}, bound {r['bound_share_12']:.3f}, form {r['leak']:.4f}, field form {row['binding_form']:.3e}{extra}"
            )
    print(
        f"  the record's form's means over windows of {WINDOW}: {[round(v, 4) for v in result['form_means_300'][0]]}"
    )
    for row in result["passes_report"]:
        print(
            f"  pass {row['pass']}: omega_mode {[round(v, 4) for v in row['omega_mode']]}, residual {[f'{v:.1e}' for v in row['mode_residual']]}, "
            f"content peak {row['content_peak']} max {row['content_max']}, the hill's excess at {row['hill_excess_nodes']} Nodes (max {row['hill_excess_max']}), "
            f"count sum {row['count_sum']} peak {row['count_peak']}, change {row['content_change_max']}"
        )
    if result["sponge_layer"]:
        print(
            f"  the sponge: {result['sponge_layer']} Nodes at strength {result['sponge_strength']} (HOST)"
        )
    for family_name, values in result["ringing_300"].items():
        if values:
            print(
                f"  the ringing of {family_name} at the peak Node {result['ring_node']}, per 300: {[round(v, 4) for v in values]}"
            )
    if result["source"] == "sourced":
        print(
            f"  the static floor at the peak {result['static_floor_at_peak']} (asked {result['floor_asked']}); E_s {result['e_s']}"
        )
        for row in result["readings"]:
            if row["t"] % 250 == 0:
                print(
                    f"  t {row['t']:5d}: total {row['total']:.4e}, coupling {row['coupling']:.4e}, content max {row['content_max']}, "
                    f"the hill's excess at {row['hill_excess_nodes']} Nodes (max {row['hill_excess_max']})"
                )
    (Path(__file__).resolve().parent / f"{name}.json").write_text(
        json.dumps(result, indent=1) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
