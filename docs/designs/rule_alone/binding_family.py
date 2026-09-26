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
The guard p > 0 (the content reaching Gamma) ends a run and is reported with its interval.

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

    def form(self) -> float:
        read, own, wall = self.coefficients
        return conserved(self.now, self.before, read, own, wall)


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
    num = np.full(SHAPE, KIND[0], dtype=R.INT)
    den = np.full(SHAPE, KIND[1], dtype=R.INT)
    read0, own0, wall0 = R.coefficients(num, den, np.zeros(SHAPE, dtype=R.INT))
    cos_vacuum = float(R.rest_rotation(read0, own0, wall0)[0, 0, 0])
    middle = SHAPE[1] / 2.0
    gravity, binding = Field(GRAVITY_PAIR), Field(BINDING_PAIR)
    core = Field(CORE_PAIR) if source == "core" else None
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
    e_core = max(1, int(records[0].e_s * core_scale))
    guard_interval = None
    guard_content = 0
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
        binding.step(pace_content)
        gravity.hold(support, level)
        binding.hold(support, level)
        if core is not None:
            core.step(pace_content)
            core.hold(support, level_core)
        content = gravity.now + k_m * binding.now
        if core is not None:
            content = content - k_r * core.now
        if int(content.max()) >= R.GAMMA:
            guard_interval = t
            guard_content = int(content.max())
            break
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
        "e_s": [r.e_s for r in records],
        "e_core": e_core if core is not None else None,
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
        f"; THE GUARD at interval {result['guard_interval']} (content {result['guard_content']})"
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
    (Path(__file__).resolve().parent / f"{name}.json").write_text(
        json.dumps(result, indent=1) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
