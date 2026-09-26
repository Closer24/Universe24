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

THE CLICK THAT KEEPS THE MOMENTUM (the Boss's record 2160; the trailing word `keep`): the record
is re-created at the click's Node as a packet of rms KEEP_WIDTH carrying the phase gradient read
from its currents before the click, at the same norm (`Record.recreate_with_momentum`); the
displacement to the click's Node is the detector's share, booked on the click line. Run as
`moving ... keep` (one body at v), `still ... keep` (the same at v = 0: the walk alone) and
`pair ... keep` (two bodies, each reading the other's content).

    PYTHONPATH=src python docs/designs/rule_alone/item9_pair.py pair|moving|moving_control|still [intervals] [keep] [flux|density] [seed N]
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
KEEP_WIDTH = 3.0  # the re-created packet's rms (the detector's resolution, a HOST choice)
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


def run(mode: str, intervals: int, keep: bool = False, born_by: str = "flux", seed: int = 0) -> dict:
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
        width = KEEP_WIDTH if keep else None
        u0 = (C.RESIDUE_START + 97 * seed) % C.WHEEL
        p0 = (C.POSITION_START + 41 * seed) % C.WHEEL
        a = C.Record(
            *packet((X_A, middle, middle), cos_omega), 0.0, u0, p0, width, cos_omega, born_by=born_by
        )
        b = C.Record(
            *packet((X_B, middle, middle), cos_omega),
            0.0,
            (u0 + 173) % C.WHEEL,
            (p0 + 59) % C.WHEEL,
            width,
            cos_omega,
            born_by=born_by,
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
        speed = 0.0 if mode == "still" else SPEED
        k, omega_k = wave_number(speed, *KIND) if speed > 0 else (0.0, 0.0)
        now, before = packet((X_A, middle, middle), cos_omega, k, omega_k)
        record = C.Record(
            now,
            before,
            0.0,
            (C.RESIDUE_START + 97 * seed) % C.WHEEL,
            (C.POSITION_START + 41 * seed) % C.WHEEL,
            KEEP_WIDTH if keep else None,
            cos_omega,
            born_by=born_by,
        )
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
                        "expected_v_t": X_A + speed * t,
                        "peak": list(peak),
                        "clicks": len(record.clicks),
                        "centroid_x": cx,
                        "k_read": record.momentum(),
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
            "speed": speed,
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
            "keep": keep,
            "keep_width": KEEP_WIDTH if keep else None,
            "born_by": born_by,
            "seed": seed,
            "host_seconds": time.time() - t0,
        }
    )
    return result


def main() -> None:
    args = sys.argv[1:]
    # the trailing words: `keep`, then `flux` or `density` (the click's Node by Born's rule on
    # the inward flux or on the record's form), then `seed N` (the residue sequences' start)
    seed = 0
    if len(args) >= 2 and args[-2] == "seed":
        seed = int(args[-1])
        args = args[:-2]
    # `width W`: the re-created packet's rms (9.109 (3) reads a width of 1)
    if len(args) >= 2 and args[-2] == "width":
        globals()["KEEP_WIDTH"] = float(args[-1])
        args = args[:-2]
    born_by = "flux"
    if args and args[-1] in ("flux", "density"):
        born_by = args.pop()
    keep = bool(args) and args[-1] == "keep"
    if keep:
        args = args[:-1]
    mode = args[0] if args else "pair"
    intervals = int(args[1]) if len(args) > 1 else 1500
    result = run(mode, intervals, keep, born_by, seed)
    width_word = f"_w{KEEP_WIDTH:g}" if keep and KEEP_WIDTH != 3.0 else ""
    name = f"item9_pair_{mode}{'_keep' if keep else ''}{'_' + born_by if keep else ''}{width_word}{('_seed' + str(seed)) if seed else ''}"
    print(
        f"{name}: {result.get('clicks', result.get('clicks_a'))} clicks; {result['host_seconds']:.0f} s"
    )
    for r in result["readings"]:
        if r["t"] % 250 == 0:
            line = ", ".join(f"{k} {v}" for k, v in r.items() if not isinstance(v, list))
            if "k_read" in r:
                line += f", k_read x {r['k_read'][0]:.4f}"
            print("  " + line)
    (Path(__file__).resolve().parent / f"{name}.json").write_text(
        json.dumps(result, indent=1) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
