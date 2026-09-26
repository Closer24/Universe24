"""THE FOUR RUNS OF ALGEBRA.md 9.98 (11) (the Boss's record 2157): THE BINDING AS A FAMILY, the
mathematician's generic line (c), in Nature24's runner of the rule 9.57 (1) in integers.

THE LINE, as run here (HOST choices stated once):
- every record writes at every Node of its support its local count s_i = F_i div E_s into the
  t part of gravity and of the binding family. F_i is the record's form at the Node from its
  own pair alone, F_i = now^2 + before^2 - 2 now before cos omega_i, cos omega_i the Node's rest
  rotation at the content read there in the interval before (the stationary envelope; the
  mathematician's six-differences form is its neighbour form); E_s is fixed at the start so that
  the record's peak Node reads s = 2000 (today's hold writes s at the body's Nodes; the source
  writes s_i as the form says, more at the centre): E_s = F_peak(0) div 2000, a universe integer
  in the design, here read from the start.
- the hold: at every interval, after the held families' plain step, both levels of gravity and
  of the binding family at the support (s_i > 0) are written to s_i (the engine's hold, the
  order of 9.85 (2)).
- gravity's pair [1, 1] (long range); the binding family's pair [54, 55]: the static equation
  of a held level is SUM_neighbours a = 6 (den / num) a at p = Gamma, so its level decays as
  exp(-kappa r) with kappa^2 = 6 (den / num - 1) = 1 / 9: the range of 3 Links asked.
- the record's pace at a Node p_0,i = Gamma - g_i - K_m b_i (weights 1 and K_m, 9.91 (2)); the
  record steps by the rule with these coefficients; no pair well anywhere, the kind [800, 850]
  on every Node, no hop, no tally.
- the board 48^3 with open faces (a level 0 beyond a face; the runner's face reflects); the
  record starts as a standing Gaussian of sigma = side / 2 at amplitude 2^17 (a start, not the
  mode; the mode is what the run settles to).

THE RUNS: (1) `rest SIDE K_M`: bound or not, at what width and rotation; (2) `moving SIDE K_M
V`: a phase gradient at the group pace V; does it move freely, from what width; (3) the leak,
read in every run: the rule's conserved form I at the current coefficients over its start; (4)
`pair K_M`: two bodies 20 Links apart, each sourcing both families and reading both.

THE READINGS (GAMEBOARD of the runner) every 25 intervals: the centroid of F, the rms width
about it, the peak level and Node, the count SUM s_i and the peak's s_i, the content at the peak,
the rotation (the time average of 2 SUM now before / SUM (now^2 + before^2) over the window,
cos omega_eff), the bound share (F within 12 Links of the centroid over the total), the leak.

THE THREE READINGS OF E_s (the source's scale), all run, the first the line as written:
- `level`: E_s = F_peak(0) div s, the peak Node reads s at the start (the engine's hold today
  writes the level s at every Node of the body; the mathematician's table of 9.98 (10) (h) binds
  at the level K_m s); the level then follows the form.
- `count`: E_s = SUM F_i(0) div s, the counts sum to s (one count's form, the conserved
  reading; the level at a Node is then s times the Node's share of the form).
- `cap`: `level` with s_i cut at s (a saturation: not the line, a reading of what the cut does).
The guard p > 0 (the content reaching Gamma) ends a run and is reported with its interval.

    PYTHONPATH=src python docs/designs/rule_alone/binding_family.py rest 5 2 [intervals] [level|count|cap]
    PYTHONPATH=src python docs/designs/rule_alone/binding_family.py moving 5 2 0.05 [intervals] [source]
    PYTHONPATH=src python docs/designs/rule_alone/binding_family.py pair 9 2 [intervals] [source]
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

SHAPE = (48, 48, 48)
WRAP = (False, False, False)
KIND = (800, 850)
GRAVITY_PAIR = (1, 1)
BINDING_PAIR = (54, 55)  # kappa^2 = 6 (55 / 54 - 1) = 1 / 9, the range 3 Links
COUNT = 2000
AMPLITUDE = 1 << 17
EVERY = 25
BOUND_RADIUS = 12
PAIR_SEPARATION = 20


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
    """A held family stepping by the plain rule at the pace Gamma with its own pair."""

    def __init__(self, pair: tuple[int, int]) -> None:
        num = np.full(SHAPE, pair[0], dtype=R.INT)
        den = np.full(SHAPE, pair[1], dtype=R.INT)
        self.read, self.own, self.wall = R.coefficients(num, den, np.zeros(SHAPE, dtype=R.INT))
        self.now = np.zeros(SHAPE, dtype=R.INT)
        self.before = np.zeros(SHAPE, dtype=R.INT)
        self.remainder = np.zeros(SHAPE, dtype=R.INT)

    def step(self) -> None:
        self.now, self.before, self.remainder = R.step(
            self.now, self.before, self.remainder, self.read, self.own, self.wall, WRAP
        )

    def hold(self, support: np.ndarray, level: np.ndarray) -> None:
        self.now[support] = level[support]
        self.before[support] = level[support]


class Record:
    def __init__(self, now: np.ndarray, before: np.ndarray) -> None:
        self.now = now
        self.before = before
        self.remainder = np.zeros(SHAPE, dtype=R.INT)
        self.cos_omega = np.full(SHAPE, 0.0)
        self.e_s = 1


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


def conserved(record: Record, read: np.ndarray, own: np.ndarray, wall: np.ndarray) -> float:
    n = record.now.astype(np.float64)
    b = record.before.astype(np.float64)
    return float(
        (n * n + b * b).sum()
        - (own / wall * n * b).sum()
        - (read / wall * b * R.neighbour_sum(record.now, WRAP)).sum()
    )


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
    # the tail: the log slope of the form along +x from the centroid between 6 and 12 Links
    xs = np.arange(SHAPE[0])
    line = form[:, int(round(cy)), int(round(cz))]
    r_line = xs - cx
    inside = (r_line >= 6) & (r_line <= 12) & (line > 0)
    tail = float("nan")
    if inside.sum() >= 3:
        slope = np.polyfit(r_line[inside], np.log(line[inside]), 1)[0]
        tail = (
            -2.0 / slope if slope < 0 else float("inf")
        )  # the envelope's 1 / kappa (the form is the envelope squared)
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


def run(mode: str, side: int, k_m: int, speed: float, intervals: int, source: str) -> dict:
    num = np.full(SHAPE, KIND[0], dtype=R.INT)
    den = np.full(SHAPE, KIND[1], dtype=R.INT)
    read0, own0, wall0 = R.coefficients(num, den, np.zeros(SHAPE, dtype=R.INT))
    cos_vacuum = float(R.rest_rotation(read0, own0, wall0)[0, 0, 0])
    middle = SHAPE[1] / 2.0
    gravity, binding = Field(GRAVITY_PAIR), Field(BINDING_PAIR)
    sigma = side / 2.0
    records: list[Record] = []
    if mode == "pair":
        for x in (SHAPE[0] / 2.0 - PAIR_SEPARATION / 2.0, SHAPE[0] / 2.0 + PAIR_SEPARATION / 2.0):
            records.append(Record(*packet((x, middle, middle), sigma, cos_vacuum)))
    elif mode == "moving":
        k, omega_k = wave_number(speed, *KIND)
        records.append(
            Record(*packet((SHAPE[0] / 2.0 - 8, middle, middle), sigma, cos_vacuum, k, omega_k))
        )
    else:
        records.append(Record(*packet((SHAPE[0] / 2.0, middle, middle), sigma, cos_vacuum)))
    for record in records:
        record.cos_omega = np.full(SHAPE, cos_vacuum)
        form = form_of(record)
        if source == "count":
            record.e_s = max(1, int(form.sum()) // COUNT)
        else:
            record.e_s = max(1, int(form.max()) // COUNT)
    guard_interval = None
    i_start = None
    windows: list[list[float]] = [[] for _ in records]
    readings: list[dict] = []
    t0 = time.time()
    content = np.zeros(SHAPE, dtype=R.INT)
    guard_content = 0
    for t in range(intervals + 1):
        # the sources: each record's local count from its own form
        counts = []
        support = np.zeros(SHAPE, dtype=bool)
        level = np.zeros(SHAPE, dtype=R.INT)
        for record in records:
            form = form_of(record)
            count = (form // record.e_s).astype(R.INT)
            if source == "cap":
                count = np.minimum(count, COUNT)
            counts.append(count)
            support |= count > 0
            level += count
        # the held families' step, then the hold (9.85 (2))
        gravity.step()
        binding.step()
        gravity.hold(support, level)
        binding.hold(support, level)
        content = gravity.now + k_m * binding.now
        if int(content.max()) >= R.GAMMA:
            guard_interval = t
            guard_content = int(content.max())
            break
        read, own, wall = R.coefficients(num, den, content)
        cos_local = R.rest_rotation(read, own, wall)
        if t == 0:
            i_start = [conserved(r, read, own, wall) for r in records]
        if t % EVERY == 0:
            row: dict = {"t": t}
            for index, record in enumerate(records):
                reading = readings_of(record, form_of(record), content, counts[index], windows[index])
                reading["leak"] = (
                    conserved(record, read, own, wall) / i_start[index]
                    if i_start and i_start[index]
                    else float("nan")
                )
                row[f"record_{index}"] = reading
                windows[index] = []
            if mode == "pair":
                row["separation"] = row["record_1"]["centroid"][0] - row["record_0"]["centroid"][0]
            if mode == "moving":
                row["expected_x"] = SHAPE[0] / 2.0 - 8 + speed * t
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
        "mode": mode,
        "side": side,
        "k_m": k_m,
        "speed": speed,
        "intervals": intervals,
        "shape": SHAPE,
        "kind": KIND,
        "binding_pair": BINDING_PAIR,
        "count": COUNT,
        "amplitude": AMPLITUDE,
        "source": source,
        "guard_interval": guard_interval,
        "guard_content": guard_content if guard_interval is not None else None,
        "e_s": [r.e_s for r in records],
        "cos_omega_vacuum": cos_vacuum,
        "omega_vacuum": math.acos(cos_vacuum),
        "readings": readings,
        "host_seconds": time.time() - t0,
    }


def main() -> None:
    mode = sys.argv[1]
    args = sys.argv[2:]
    source = "level"
    if args and args[-1] in ("level", "count", "cap"):
        source = args.pop()
    if mode == "pair":
        side, k_m, speed = int(args[0]), int(args[1]), 0.0
        intervals = int(args[2]) if len(args) > 2 else 1500
        name = f"binding_pair_s{side}_k{k_m}_{source}"
    elif mode == "moving":
        side, k_m, speed = int(args[0]), int(args[1]), float(args[2])
        intervals = int(args[3]) if len(args) > 3 else 1500
        name = f"binding_moving_s{side}_k{k_m}_v{speed}_{source}"
    else:
        side, k_m, speed = int(args[0]), int(args[1]), 0.0
        intervals = int(args[2]) if len(args) > 2 else 1500
        name = f"binding_rest_s{side}_k{k_m}_{source}"
    result = run(mode, side, k_m, speed, intervals, source)
    guard = (
        f"; THE GUARD at interval {result['guard_interval']} (content {result['guard_content']})"
        if result["guard_interval"] is not None
        else ""
    )
    print(
        f"{name}: E_s {result['e_s']}, omega_vacuum {result['omega_vacuum']:.4f}; {result['host_seconds']:.0f} s{guard}"
    )
    for row in result["readings"]:
        if row["t"] % 250 == 0 or row["t"] == 25:
            r = row["record_0"]
            extra = (
                f", separation {row['separation']:.2f}"
                if "separation" in row
                else (f", expected x {row['expected_x']:.1f}" if "expected_x" in row else "")
            )
            print(
                f"  t {row['t']:5d}: centroid x {r['centroid'][0]:6.2f}, width {r['width_rms']:5.2f}, tail {r['tail_links']:5.1f}, peak {r['peak']:7d}, count sum {r['count_sum']:6d} peak {r['count_peak']:5d}, content {r['content_peak']:5d}, omega {r['omega_eff']:.4f}, bound {r['bound_share_12']:.3f}, leak {r['leak']:.4f}{extra}"
            )
    (Path(__file__).resolve().parent / f"{name}.json").write_text(
        json.dumps(result, indent=1) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
