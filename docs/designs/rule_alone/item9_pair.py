"""THE NINTH HARD QUESTION, part (b) (record 2152): two bodies held by their clicks, 20 Links
apart, and one put in motion at v = 0.1; the click as in `item9_clicks.py` (every Node a
detector, the engine's ladder, the record deleted whole and re-created at the click's Node).

`pair`: two records of s = 2000 quanta each, the packets of width 6 at x = 38 and x = 58 on
[96, 48, 48] periodic; each reads the gravity time part's static level of the OTHER body's
content, s at that body's peak Node (a one-Node source relaxed once and rolled to the Node at
every interval; the own level left out: no self-binding, record 2152); the reading (GAMEBOARD
of the runner) the separation of the two peaks over 1500 intervals. The algebra's number
beside: two point sources of s = 2000 from rest at 20 Links meet at 249 intervals (item 2's
Newton integration, `item2_algebra.py`); a body whose record is one Node between clicks falls
1 / 2 g tau^2 per click interval tau and forgets the fall's pace at the click.

`moving`: one record put in motion along +x at the group pace v = 0.1 (now = p cos(K dx -
omega_K / 2), before = p cos(K dx + omega_K / 2), ALGEBRA.md 9.98 (9) (b)), no content anywhere;
the reading the peak's x over 1500 intervals (unwrapped), against v t; `moving_control` the same
record with no click.

    PYTHONPATH=src python docs/designs/rule_alone/item9_pair.py pair|moving|moving_control [intervals]
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
WIDTH = 6.0
X_A, X_B = 38, 58
SPEED = 0.1
EVERY = 50
C.SHAPE = SHAPE
C.WRAP = WRAP


def wave_number(speed: float, num: int, den: int) -> tuple[float, float]:
    """K and omega_K of the kind at the group pace `speed` (HOST, bisection on the dispersion
    2 cos omega = (num / den) (2 cos K + 4) / 3)."""

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


def packet(
    centre: tuple[float, float, float], cos_omega: float, k: float = 0.0, omega_k: float = 0.0
) -> tuple[np.ndarray, np.ndarray]:
    grids = np.meshgrid(*[np.arange(n, dtype=np.float64) for n in SHAPE], indexing="ij")
    r2 = sum((g - c) ** 2 for g, c in zip(grids, centre, strict=True))
    envelope = C.AMPLITUDE * np.exp(-r2 / (2.0 * WIDTH * WIDTH))
    if k == 0.0:
        return np.rint(envelope).astype(R.INT), np.rint(envelope * cos_omega).astype(R.INT)
    dx = grids[0] - centre[0]
    now = np.rint(envelope * np.cos(k * dx - omega_k / 2.0)).astype(R.INT)
    before = np.rint(envelope * np.cos(k * dx + omega_k / 2.0)).astype(R.INT)
    return now, before


def peak_of(record: C.Record, cos_omega: float) -> tuple[int, int, int]:
    e2 = R.envelope_squared(record.now, record.before, np.full(SHAPE, cos_omega))
    p = np.unravel_index(int(np.argmax(e2)), SHAPE)
    return (int(p[0]), int(p[1]), int(p[2]))


def unwrap(previous: int, current: int, extent: int) -> int:
    d = (current - previous + extent // 2) % extent - extent // 2
    return d


def run(mode: str, intervals: int) -> dict:
    num = np.full(SHAPE, KIND[0], dtype=R.INT)
    den = np.full(SHAPE, KIND[1], dtype=R.INT)
    zero = np.zeros(SHAPE, dtype=R.INT)
    read0, own0, wall0 = R.coefficients(num, den, zero)
    cos_omega = float(R.rest_rotation(read0, own0, wall0)[0, 0, 0])
    middle = SHAPE[1] // 2
    t0 = time.time()
    readings: list[dict] = []
    if mode == "pair":
        lone = B.lone_static_field(
            SHAPE, WRAP, B.Body([SHAPE[0] // 2, middle, middle], AMOUNT, side=1, kind=KIND, well=KIND)
        )
        a = C.Record(*packet((X_A, middle, middle), cos_omega), 0.0, C.RESIDUE_START, C.POSITION_START)
        b = C.Record(
            *packet((X_B, middle, middle), cos_omega),
            0.0,
            (C.RESIDUE_START + 173) % C.WHEEL,
            (C.POSITION_START + 59) % C.WHEEL,
        )
        a.t_norm = C.norm(a.now, a.before, read0, own0, wall0, WRAP, *KIND)
        b.t_norm = C.norm(b.now, b.before, read0, own0, wall0, WRAP, *KIND)
        peaks = [peak_of(a, cos_omega), peak_of(b, cos_omega)]
        xa, xb = float(peaks[0][0]), float(peaks[1][0])
        for t in range(intervals + 1):
            if t % EVERY == 0:
                readings.append(
                    {
                        "t": t,
                        "x_a": xa,
                        "x_b": xb,
                        "separation": xb - xa,
                        "peak_a": list(peaks[0]),
                        "peak_b": list(peaks[1]),
                        "clicks_a": len(a.clicks),
                        "clicks_b": len(b.clicks),
                    }
                )
            if t == intervals:
                break
            # each record reads the other's static level at the other's peak Node
            content_a = np.roll(lone, [peaks[1][i] - SHAPE[i] // 2 for i in range(3)], axis=(0, 1, 2))
            content_b = np.roll(lone, [peaks[0][i] - SHAPE[i] // 2 for i in range(3)], axis=(0, 1, 2))
            a.step(*R.coefficients(num, den, content_a), t + 1, *KIND)
            b.step(*R.coefficients(num, den, content_b), t + 1, *KIND)
            new_peaks = [peak_of(a, cos_omega), peak_of(b, cos_omega)]
            xa += unwrap(peaks[0][0], new_peaks[0][0], SHAPE[0])
            xb += unwrap(peaks[1][0], new_peaks[1][0], SHAPE[0])
            peaks = new_peaks
        result = {
            "mode": mode,
            "readings": readings,
            "clicks_a": len(a.clicks),
            "clicks_b": len(b.clicks),
            "clicks_a_first": a.clicks[:50],
            "clicks_b_first": b.clicks[:50],
        }
    else:
        k, omega_k = wave_number(SPEED, *KIND)
        now, before = packet((X_A, middle, middle), cos_omega, k, omega_k)
        record = C.Record(now, before, 0.0, C.RESIDUE_START, C.POSITION_START)
        record.t_norm = C.norm(now, before, read0, own0, wall0, WRAP, *KIND)
        peak = peak_of(record, cos_omega)
        x = float(peak[0])
        for t in range(intervals + 1):
            if t % EVERY == 0:
                e2 = R.envelope_squared(record.now, record.before, np.full(SHAPE, cos_omega))
                cx = R.centroid(e2)[0] if mode == "moving_control" else float("nan")
                readings.append(
                    {
                        "t": t,
                        "x_peak": x,
                        "expected_v_t": X_A + SPEED * t,
                        "peak": list(peak),
                        "clicks": len(record.clicks),
                        "centroid_x": cx,
                    }
                )
            if t == intervals:
                break
            if mode == "moving_control":
                record.now, record.before, record.remainder = R.step(
                    record.now, record.before, record.remainder, read0, own0, wall0, WRAP
                )
            else:
                record.step(read0, own0, wall0, t + 1, *KIND)
            new_peak = peak_of(record, cos_omega)
            x += unwrap(peak[0], new_peak[0], SHAPE[0])
            peak = new_peak
        result = {
            "mode": mode,
            "K": k,
            "omega_K": omega_k,
            "speed": SPEED,
            "readings": readings,
            "clicks": len(record.clicks),
            "clicks_first": record.clicks[:50],
        }
    result.update(
        {
            "intervals": intervals,
            "shape": SHAPE,
            "kind": KIND,
            "amount": AMOUNT,
            "width": WIDTH,
            "host_seconds": time.time() - t0,
        }
    )
    return result


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "pair"
    intervals = int(sys.argv[2]) if len(sys.argv) > 2 else 1500
    result = run(mode, intervals)
    print(
        f"{mode}: {result.get('clicks', result.get('clicks_a'))} clicks; {result['host_seconds']:.0f} s"
    )
    for r in result["readings"]:
        if r["t"] % 250 == 0:
            print("  " + ", ".join(f"{k} {v}" for k, v in r.items() if not isinstance(v, list)))
    (Path(__file__).resolve().parent / f"item9_pair_{mode}.json").write_text(
        json.dumps(result, indent=1) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
