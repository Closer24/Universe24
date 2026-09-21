"""c in the vector law: the integer map beside FORM.md (read-only, the
mathematician, 2026-09-21). (A) The bound of the flight table: the largest
Manhattan pace over every primitive direction within the table's bound is
exactly 1 at the cube diagonals, so c = 1 / sqrt 3 is the largest isotropic
speed at which no direction crosses two Links in one interval. (B) The
dispersion v(p) of today's per-axis step rule against the two directional
forms that insert c into matter and against relativity. (C) The registered
worlds' moving bodies against c at their declared momenta. (D) One flight
primitive for light and matter: the Manhattan accumulator at a fraction,
light the fraction 1, and the first interval at which the directional
drive parts from today's per-axis drive on the register's readers. (E)
lorentz-v1 in integers on the muon of series J4: the fraction at a grain,
the root, the trigger tick and the range, against the exchange clock of
the derivation's section 10.

Run from the repository root with PYTHONPATH=src:

    python docs/designs/light_speed/light_speed_map.py > docs/designs/light_speed/light_speed_map.out
"""

from __future__ import annotations

import glob
import json
import math
from pathlib import Path

from event_universe.core.integer import by_drive
from event_universe.world_loading import load_world

Q = 64
BOUND = 64
C_AXIS = 32 / 55
GRAIN = 1 << 20


def resolution(v: tuple[int, int, int]) -> int:
    return math.isqrt(3 * (v[0] ** 2 + v[1] ** 2 + v[2] ** 2) * Q * Q)


def bresenham(vector: tuple[int, int, int]) -> list[tuple[int, int, int]]:
    s1 = sum(abs(c) for c in vector)
    line = []
    position = [0, 0, 0]
    for j in range(s1):
        best = max(range(3), key=lambda i: (abs(vector[i]) * (j + 1) - s1 * abs(position[i]), -i))
        step = [0, 0, 0]
        step[best] = 1 if vector[best] > 0 else -1
        position[best] += step[best]
        line.append((step[0], step[1], step[2]))
    return line


def walk(vector: tuple[int, int, int], rate: int, wall: int, intervals: int) -> tuple[int, ...]:
    """The Manhattan accumulator on the digital line of `vector` at the
    rate over the wall (by_drive, one Link per interval at most): the
    position after `intervals`."""
    line = bresenham(vector)
    s1 = len(line)
    drive = 0
    made = 0
    position = [0, 0, 0]
    for _ in range(intervals):
        fired, drive = by_drive(drive, rate, wall, at_most=1)
        if fired:
            step = line[made % s1]
            made += 1
            for a in range(3):
                position[a] += step[a]
    return tuple(position)


def main() -> None:
    # A. The bound of the flight table.
    print("A. THE FLIGHT TABLE'S BOUND")
    fastest = 0.0
    slowest = 1.0
    at_one = 0
    count = 0
    for a in range(-BOUND, BOUND + 1):
        for b in range(-BOUND, BOUND + 1):
            for c in range(-BOUND, BOUND + 1):
                if (a, b, c) == (0, 0, 0) or math.gcd(math.gcd(abs(a), abs(b)), abs(c)) != 1:
                    continue
                s1 = abs(a) + abs(b) + abs(c)
                t = resolution((a, b, c))
                assert s1 * Q <= t  # the Manhattan pace S_1 Q / T_D is at most one Link per interval
                euclid = Q * math.sqrt(a * a + b * b + c * c) / t
                count += 1
                fastest = max(fastest, euclid)
                slowest = min(slowest, euclid)
                if s1 * Q == t:
                    at_one += 1
                assert s1 * Q <= t, (a, b, c)
    print(
        f"  primitive directions with components within {BOUND}: {count}; Manhattan pace S_1 Q / T_D <= 1 on every one (checked), equal to 1 on {at_one} (the cube diagonals (+-1, +-1, +-1): T = 192 = 3 x 64)"
    )
    print(
        f"  the Euclidean pace Q |D| / T_D over the table: {slowest:.4f} to {fastest:.4f} Links per interval (1 / sqrt 3 = {1 / math.sqrt(3):.4f}; the heading 64 / 110 = {C_AXIS:.4f}): isotropic within isqrt's rounding"
    )
    print(
        "  so c = 1 / sqrt 3 is the largest isotropic speed with at most one Link per interval in every direction: the meeting of the L1 walk with the Euclidean flight (1 / sqrt n in n dimensions)"
    )

    # B. The dispersion.
    print("\nB. THE DISPERSION v(p) IN UNITS OF c, m = Q S M, on a heading (c = 32 / 55 there)")
    print(
        "  p / m | today p / (m + p), in c | form A c p / (m + p) | form B p / (m + p / c) | relativity p / sqrt(m^2 c^2 + p^2)"
    )
    for num, den in ((1, 16), (1, 4), (1, 1), (3, 1), (9, 1)):
        x = num / den
        today = x / (1 + x) / C_AXIS
        form_a = x / (1 + x)
        form_b = (x / (1 + x / C_AXIS)) / C_AXIS
        rel = x / math.sqrt(C_AXIS**2 + x * x)
        print(f"  {num}/{den:<3d} | {today:.3f} | {form_a:.3f} | {form_b:.3f} | {rel:.3f}")
    print(
        "  today caps at 1 Link per interval = 1.72 c (a body outruns light above p = 1.39 m); both forms cap at c; form A rescales every speed by c (Newton's limit v = c p / m), form B keeps Newton's limit v = p / m and bends to c"
    )

    # Isotropy of the directional drive: a fixed fraction f on four directions.
    print(
        "\n  the directional drive at one fraction on four directions (form B, p / m = 1, 600 intervals): the Euclidean distance made, isotropic within the flight table's rounding"
    )
    m = 1 << 20
    p = m
    for vector in ((1, 0, 0), (1, 1, 0), (1, 1, 1), (3, 1, 0)):
        s1, t = sum(map(abs, vector)), resolution(vector)
        rate, wall = p * s1 * Q, m * s1 * Q + p * t
        pos = walk(vector, rate, wall, 600)
        dist = math.sqrt(sum(x * x for x in pos))
        print(
            f"    {vector}: position {pos}, Euclidean {dist:.1f} Links in 600 intervals = {dist / 600:.4f} per interval (c x p / (c m + p) on this direction = {(Q * math.sqrt(sum(x * x for x in vector)) / t) * p / (p + m * s1 * Q / t):.4f})"
        )

    # C. The registered worlds' moving bodies.
    print(
        "\nC. THE REGISTERED WORLDS' MOVING BODIES AT THEIR DECLARED MOMENTA (content = amount + held)"
    )
    rows = []
    for path_name in sorted(glob.glob("examples/events/**/*.json", recursive=True)):
        path = Path(path_name)
        try:
            doc = json.loads(load_world(path.read_bytes(), base_dir=path.parent).expanded_source)
        except Exception:
            continue
        if "measured" not in doc:
            continue
        width = doc.get("width", 1)
        best = 0.0
        moving = 0
        for entry in doc["measured"]:
            if entry.get("fixed", False):
                continue
            momentum = entry.get("momentum")
            if not momentum or not any(momentum):
                continue
            held = entry.get("held", {})
            content = entry.get("amount", 0) + (sum(held.values()) if isinstance(held, dict) else 0)
            if content <= 0:
                continue
            moving += 1
            best = max(best, max(abs(pa) / (Q * width * content + abs(pa)) for pa in momentum))
        if moving:
            rows.append((path_name[16:], width, moving, best))
    above = [r for r in rows if r[3] > C_AXIS]
    print(
        f"  worlds with moving bodies: {len(rows)}; bodies above c on an axis at the declared momenta: {len(above)} worlds"
    )
    for name, width, moving, best in sorted(rows, key=lambda r: -r[3])[:8]:
        print(
            f"    {name:38s} S = {width:<10d} bodies {moving:2d}  fastest axis speed {best:.4f} Links per interval = {best / C_AXIS:.3f} c; under form B {best / (1 + best * (1 / C_AXIS - 1)):.4f} ({best / (1 + best * (1 / C_AXIS - 1)) / best:.3f} of today)"
        )
    print(
        "  the run-time momenta: G2's stars reach 1.14 x 10^14 at Q S M = 2.8 x 10^14 (GRAIN.md), v = 0.289 = 0.50 c; the fastest coasting star reads z = 0.2636 (the derivation's 4.5); the only body above c on the register is the doppler bar's outrunning body at 0.75 (FORM.md's map and test_doppler (b)), a test fixture and not a world file"
    )

    # D. One primitive: light as the fraction 1; the first interval where form B parts from today.
    print("\nD. ONE FLIGHT PRIMITIVE: light is the directional drive at the fraction 1")
    for vector in ((1, 0, 0), (1, 1, 0), (5, -3, 2)):
        s1, t = sum(map(abs, vector)), resolution(vector)
        light = walk(vector, s1 * Q, t, 300)
        body = walk(vector, (1 << 40) * s1 * Q, 0 * s1 * Q + (1 << 40) * t, 300)  # m = 0: the fraction 1
        print(
            f"  {vector}: the flight table's row after 300 intervals {light}; the directional drive at m = 0 {body}; identical {light == body}"
        )
    print(
        "  the register's readers (record 153: M = 21 x 2^16, S = 1, |p| = 7 x 2^22, v = 1 / 4 today) and G2's fastest star, today's per-axis drive against form B on the axis:"
    )
    for label, m_qsm, p in (
        ("the k = 4 reader", 21 << 22, 7 << 22),
        ("the k = 8 reader", 21 << 22, 3 << 22),
        ("G2's fastest star", 2817 * 10**11, 114 * 10**12),
    ):
        s1, t = 1, resolution((1, 0, 0))
        today_pos = walk((1, 0, 0), p, m_qsm + p, 400)[0]
        b_pos = walk((1, 0, 0), p * s1 * Q, m_qsm * s1 * Q + p * t, 400)[0]
        # the first differing interval
        first = None
        d1 = d2 = 0
        x1 = x2 = 0
        for k in range(1, 4001):
            f1, d1 = by_drive(d1, p, m_qsm + p, at_most=1)
            f2, d2 = by_drive(d2, p * s1 * Q, m_qsm * s1 * Q + p * t, at_most=1)
            x1 += f1
            x2 += f2
            if x1 != x2 and first is None:
                first = k
        print(
            f"    {label}: today {today_pos} Links in 400 intervals (v = {p / (m_qsm + p):.4f}), form B {b_pos} (v = {p * Q / (m_qsm * Q + p * t):.4f}, {b_pos / today_pos:.3f} of today); the first interval at which the two part: {first}"
        )

    # E. lorentz-v1 on the muon.
    print(
        "\nE. LORENTZ-V1 ON THE MUON OF SERIES J4 (M = 207, S = 1, Q S M = 13248; the trigger at 64 turns of the clock at rate [1, 1])"
    )
    m_qsm = Q * 1 * 207
    t = resolution((1, 0, 0))
    print(
        "  the fraction of c from the drive's own numbers, f_c = |p| T_D / (Q S M S_1 Q + |p| T_D) (the drive's rate over light's rate on the same line); the rate of the clock multiplied by isqrt(G^2 - f_hat^2) / G at G = 2^20 (one root per interval)"
    )
    for target in (0.43, 0.86):
        # form B: f_c = p t / (m Q + p t) = target  ->  p = target m Q / ((1 - target) t)
        p = round(target * m_qsm * Q / ((1 - target) * t))
        f_hat = (p * t * GRAIN) // (m_qsm * Q + p * t)
        gamma_inv = math.isqrt(GRAIN * GRAIN - f_hat * f_hat)
        acc = 0
        turns = 0
        tick = 0
        while turns < 64:
            tick += 1
            fired, acc = by_drive(acc, gamma_inv, GRAIN)
            turns += fired
        f = f_hat / GRAIN
        range_v1 = walk((1, 0, 0), p * Q, m_qsm * Q + p * t, tick)[0]
        range_today = walk((1, 0, 0), p * Q, m_qsm * Q + p * t, 64)[0]
        print(
            f"  f_c = {f:.4f} (p = {p}, v = {p * Q / (m_qsm * Q + p * t):.4f} Links per interval under form B): gamma = {1 / math.sqrt(1 - f * f):.3f}, the 64th turn at tick {tick} (today: tick 64 at every speed), the range {range_v1} Links against {range_today} at tick 64"
        )
    print(
        "  the derivation's exchange clock (section 10.2): the bond's round trip 1.383 x rest at v / c = 0.43 (k = 4) and 1.173 at 0.21 (k = 8), against gamma 1.107 and 1.024: a slowing larger than gamma and lossy; lorentz-v1 and the exchange clock cannot both be the body's clock (a body with both slows twice)"
    )
    print("\n  the orbit worlds' body at S = 1:")
    for name in ("orbit/s1_r12.json", "orbit/s8_r12.json"):
        path = Path("examples/events") / name
        doc = json.loads(load_world(path.read_bytes(), base_dir=path.parent).expanded_source)
        body = next(
            e for e in doc["measured"] if not e.get("fixed", False) and any(e.get("momentum", [0]))
        )
        v = max(abs(x) for x in body["momentum"]) / (
            Q * doc["width"] * body["amount"] + max(abs(x) for x in body["momentum"])
        )
        print(
            f"    {name}: amount {body['amount']}, momentum {body['momentum']}, S = {doc['width']}: v = {v:.4f} Links per interval = {v / C_AXIS:.3f} c"
        )


if __name__ == "__main__":
    main()
