"""Hand R3 (2026-10-25): the riding line as a standalone stepper of the lines, integers only, the volume X set by hand.

The line (V1's candidate, the brief): w [X_now (a_next - a_now) - X_before (a_now - a_before)] + r' - r = X_now F,
F = SUM over the six Links of R_ij (m_j - a_now) - D a_now (Rule3's flux form), one carried division at the wall w X_now.
Written as the momentum: P_in = w X_before (a_now - a_before) + r with r in [0, w X_before), P_out = P_in + X_now F,
(a_next - a_now, r') = divmod(P_out, w X_now). The inverse: P_out = w X_now (a_next - a_now) + r', P_in = P_out - X_now F,
(a_now - a_before, r) = divmod(P_in, w X_before). Rule3's line bit for bit at X_now = X_before (every term divided by X).

Parts (the command's first word):
  bijection  (a) the forward act and its inverse on random states and random volume pairs (rising and falling), the
             return bit for bit counted; the two other ways of carrying r counted for their collisions: r rescaled to the
             new wall, and r as it is with the velocity term at the new wall (Rule3 times X).
  seed       (c, d) the uniform sea's velocity under the ride at X set by hand, v = P div (w X), integer readings.
  adiabatic | sudden | rule3  (c) the standing wave of V2's lay on the torus [12, 3, 3] (k = pi / 2, A = 400), the
             plateaus 0, 500, 1000, 1500, 2000 held 240 intervals, 2 units of content per interval between them (sudden:
             the jump; rule3: the branch's line on the same lay as the control): per plateau the crossings, the proper
             count, the amplitude, J_rule3 = A^2 sin omega and J_ride = A^2 sin omega X / Gamma as integer roots, the
             proper frequency and E e^U.
  gapped     (e) a one-Node record of the gapped pair (779, 1021) on the 3-cube, X raised by hand: the beat, the
             amplitude, the share at the Node, under the ride and under Rule3.
Command: PYTHONPATH=src TMPDIR=/dev/shm/tmp /home/user/Universe24/venv314/bin/python tools/derivations/r3/ride_lines.py <part>
Floats stand only as named checks (check_*).
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
for path in (ROOT / "src", ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from event_universe.core import paces  # noqa: E402
from event_universe.core.ports import LINK_UNIT, PORTS  # noqa: E402
from event_universe.core.rule3 import coefficients, division_forward, form_term, largest_below, wall_of  # noqa: E402
from event_universe.features import volume  # noqa: E402
from event_universe.flux import link_fluxes  # noqa: E402
from event_universe.readings import ports  # noqa: E402

DEN, GAMMA, ACTION, G = 1021, 1000, 36000, LINK_UNIT
W = wall_of(DEN, GAMMA, G)
SCALE = 10**6
OUT = HERE.parent


def volume_at(level: int) -> int:
    return int(np.asarray(volume.volume_of(GAMMA, np.array([level], dtype=object)), dtype=object).reshape(-1)[0])


def paces_at(level: int) -> tuple[int, int]:
    p_0, p_a = paces.node_paces(GAMMA, level)
    return int(p_0), int(p_a)


def coeffs(num: int, level: int) -> tuple[int, int]:
    p_0, p_a = paces_at(level)
    return 2 * num * p_a * p_a * G * G, 12 * (DEN - num) * p_0 * p_0 * G * G


def flux_of(now: np.ndarray, num: int, level: int) -> np.ndarray:
    reach, mass = coeffs(num, level)
    return link_fluxes(now, (reach,) * PORTS) - mass * now


def half_move(x_now, x_before):  # type: ignore[no-untyped-def]
    """The half wall's move, w (X_now - X_before) div 2 (w even): the remainder born at half the wall w X_before stands at half the wall w X_now entered, the law's birth at the half wall carried across the wall's change (the shear's momentum has the same term, flux.step_momentum); without it the floor's bias at every wall change is a velocity kick of the uniform mode, which the double root keeps (measured: the board's mean -27 at the interval 250 and -19,359 at 720 on 108 Nodes)."""
    return division_forward(W * (x_now - x_before), 2, 0)[0]


def ride_forward(now, before, r, x_now, x_before, num, level, centred=True):  # type: ignore[no-untyped-def]
    """The riding act forward: (now, before, r) -> (next, now, r'), the walls w X_before (born) and w X_now (entered); `centred` carries the half wall's move (the law's form), False the letter of V1's line with no move (the control of the drift)."""
    p_in = W * x_before * (now - before) + r
    p_out = p_in + x_now * flux_of(now, num, level)
    if centred:
        p_out = p_out + half_move(x_now, x_before)
    v, kept = division_forward(p_out, W * x_now, 0)
    return now + v, now, kept


def ride_back(next_, now, kept, x_now, x_before, num, level, centred=True):  # type: ignore[no-untyped-def]
    """The same act at -1: (next, now, r') -> (now, before, r), the one division at the born wall w X_before."""
    p_out = W * x_now * (next_ - now) + kept
    p_in = p_out - x_now * flux_of(now, num, level)
    if centred:
        p_in = p_in - half_move(x_now, x_before)
    v_in, r = division_forward(p_in, W * x_before, 0)
    return now, now - v_in, r


def rule3_forward(now, before, r, num, level):  # type: ignore[no-untyped-def]
    """The branch's line (core/rule3.rule3): w a_next + r' = w (2 a_now - a_before) + F + r at the wall w."""
    total = W * (now + now - before) + flux_of(now, num, level) + r
    found, kept = division_forward(total, W, 0)
    return found, now, kept


def arrays(shape, draw, levels, wall):  # type: ignore[no-untyped-def]
    now = draw.integers(-levels, levels + 1, shape).astype(object)
    before = draw.integers(-levels, levels + 1, shape).astype(object)
    r = np.array([int(draw.integers(0, int(wall))) for _ in range(int(np.prod(shape)))], dtype=object).reshape(shape)
    return now, before, r


def same(a, b) -> bool:  # type: ignore[no-untyped-def]
    return bool(np.all(np.asarray(a, dtype=object) == np.asarray(b, dtype=object)))


def bijection() -> dict:
    """(a) The forward act and its inverse on random states: every trial back bit for bit, or the first miss named."""
    draw = np.random.default_rng(3)
    shape = (4, 3, 3)
    levels_of_content = (0, 300, 700, 1200, 2000)
    trials, returned, rising, falling = 0, 0, 0, 0
    for _ in range(400):
        a_b, a_n = (int(x) for x in draw.choice(levels_of_content, 2))
        x_before, x_now = volume_at(a_b), volume_at(a_n)
        for num in (DEN, 779):
            now, before, r = arrays(shape, draw, 600, W * x_before)
            post = ride_forward(now, before, r, x_now, x_before, num, a_n)
            back = ride_back(*post, x_now, x_before, num, a_n)
            trials += 1
            ok = same(back[0], now) and same(back[1], before) and same(back[2], r)
            returned += ok
            rising += ok and x_now > x_before
            falling += ok and x_now < x_before
            assert 0 <= int(np.min(post[2])) and int(np.max(post[2])) < W * x_now
    # the two other ways of carrying r, counted at one Node for their collisions on the remainder alone
    x_before, x_now = volume_at(700), volume_at(300)  # a falling volume: X_before > X_now
    lost_rescaled = W * x_before - W * x_now  # the rescaled remainder r X_now div X_before maps [0, w X_before) onto [0, w X_now)
    # r as it is at the new wall with the velocity term at the new wall: the inverse's divmod at w X_now folds r >= w X_now
    folded = W * x_before - W * x_now
    # a sampled check of the rescaled map's collisions
    sample = [int(x) for x in draw.integers(0, W * x_before, 20000)]
    images = {int(division_forward(s * x_now, x_before, 0)[0]) for s in sample}
    return {
        "trials": trials,
        "returned_bit_for_bit": returned,
        "returned_rising": rising,
        "returned_falling": falling,
        "x_pair_for_collisions": [x_before, x_now],
        "rescaled_r_states_lost_per_node_interval": lost_rescaled,
        "rescaled_r_sampled": {"drawn": len(sample), "distinct_images": len(images)},
        "r_as_is_at_new_wall_states_folded_per_node_interval": folded,
    }


def seed() -> dict:
    """(c, d) The uniform sea's velocity under the ride at X set by hand: P = w Gamma v_0 + r_0 conserved (F = 0 on the sea)."""
    v_0, r_0 = largest_below(ACTION), int(division_forward(W * GAMMA, 2, 0)[0])
    momentum = W * GAMMA * v_0  # the centred momentum, P less half its wall, conserved on the sea (F = 0)
    rows = []
    for level in (0, 108, 173, 346, 500, 509, 1000, 1500, 2000, 2500):
        x = volume_at(level)
        p_0, p_a = paces_at(level)
        v, r = division_forward(momentum + division_forward(W * x, 2, 0)[0], W * x, 0)
        share = int(division_forward(3 * DEN * int(v) * int(v) * GAMMA * GAMMA, p_a * p_a, 0)[0])
        quanta = int(division_forward(share + 3 * DEN * ACTION // 2, 3 * DEN * ACTION, 0)[0])
        rule3_quanta = int(
            division_forward(3 * DEN * v_0 * v_0 * GAMMA * GAMMA + (3 * DEN * ACTION // 2) * p_a * p_a, p_a * p_a * 3 * DEN * ACTION, 0)[0]
        )
        rows.append(
            {
                "level": level,
                "X": x,
                "X_over_Gamma_scaled": int(division_forward(x * SCALE, GAMMA, 0)[0]),
                "p_0": p_0,
                "p_a": p_a,
                "e_U_scaled": int(division_forward(GAMMA * SCALE, p_0, 0)[0]),
                "v_ride": int(v),
                "r_ride": int(r),
                "v_x_over_gamma_scaled": int(division_forward(int(v) * x * SCALE, GAMMA, 0)[0]),
                "share_ride_frame_weight": share,
                "quanta_ride_frame_weight": quanta,
                "quanta_rule3_frame_weight": rule3_quanta,
                "push_ride_scaled": int(division_forward(4 * int(v) * int(v) * SCALE, ACTION, 0)[0]),
                "pull_scaled": int(division_forward(12 * (DEN - 1020) * p_0 * p_0 * G * G * x * SCALE, W, 0)[0]),
            }
        )
        print(
            f"seed level {level:5d} X {x:9d} e^U x1e6 {rows[-1]['e_U_scaled']:9d} v {int(v):4d} r {int(r)} v X / Gamma x1e6 {rows[-1]['v_x_over_gamma_scaled']} "
            f"quanta ride {quanta} (rule3 {rule3_quanta}) push x1e6 {rows[-1]['push_ride_scaled']} pull x1e6 {rows[-1]['pull_scaled']}"
        )
    return {"v_0": v_0, "r_0": r_0, "P": momentum, "rows": rows}


SHAPE, WAVES, AMPLITUDE = (12, 3, 3), 3, 400
PLATEAUS, SPAN, RAMP = (0, 500, 1000, 1500, 2000), 240, 2


def wave_lay() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """V2's lay: the standing wave A cos(k x) at the vacuum's rotation, now and before alike at cos(omega / 2), the remainder at the half wall (w Gamma div 2, the wall at the start under the ride; w div 2 under Rule3 is the same line, the remainder a value)."""
    k = 2 * math.pi * WAVES / SHAPE[0]
    p_a = paces_at(0)[1]
    omega = math.acos(1 - p_a**2 / (3 * GAMMA**2))  # the lay alone, a float of the lay as V2's
    x = np.arange(SHAPE[0]).reshape(SHAPE[0], 1, 1)
    profile = np.rint(AMPLITUDE * np.cos(k * x) * math.cos(omega / 2)) * np.ones(SHAPE)
    now = profile.astype(int).astype(object)
    return now, now.copy(), np.full(SHAPE, int(division_forward(W * GAMMA, 2, 0)[0]), dtype=object)


def schedule(sudden: bool) -> list[int]:
    found: list[int] = []
    for number, level in enumerate(PLATEAUS):
        if number and not sudden:
            found += list(range(PLATEAUS[number - 1] + RAMP, level + 1, RAMP))
        found += [level] * SPAN
    return found


def plateau_reading(level: int, trace: list[int], proper: list[int]) -> dict:
    p_0, p_a = paces_at(level)
    x = volume_at(level)
    crossings = [t for t in range(1, len(trace)) if trace[t - 1] < 0 <= trace[t]]
    n = len(crossings)
    amplitude = max(abs(a) for a in trace)
    j2_rule3 = int(division_forward(amplitude**4 * p_a * p_a * (6 * GAMMA * GAMMA - p_a * p_a), 9 * GAMMA**4, 0)[0])
    j2_ride = int(
        division_forward(amplitude**4 * x * x * p_a * p_a * (6 * GAMMA * GAMMA - p_a * p_a), 9 * GAMMA**6, 0)[0]
    )
    c_num = sum(trace[t] * (trace[t + 1] + trace[t - 1]) for t in range(1, len(trace) - 1))
    c_den = 2 * sum(trace[t] * trace[t] for t in range(1, len(trace) - 1))
    row = {
        "level": level,
        "X": x,
        "p_0": p_0,
        "p_a": p_a,
        "e_U_scaled": int(division_forward(GAMMA * SCALE, p_0, 0)[0]),
        "span": len(trace) - 1,
        "crossings": n,
        "amplitude": amplitude,
        "amplitude_e_U_scaled": int(division_forward(amplitude * GAMMA * 1000, p_0, 0)[0]),
        "J_rule3": largest_below(j2_rule3),
        "J_ride": largest_below(j2_ride),
        "cosine_residual_scaled": (
            int(division_forward((c_num * 3 * GAMMA * GAMMA - c_den * (3 * GAMMA * GAMMA - p_a * p_a)) * SCALE, c_den * 3 * GAMMA * GAMMA, 0)[0])
            if c_den
            else None
        ),
    }
    if n >= 2:
        first, last = crossings[0], crossings[-1]
        between = sum(proper[first:last])
        row["period_board"] = [int(q) for q in division_forward(last - first, n - 1, 0)]
        row["proper_between"] = between
        row["K_board"] = int(division_forward((n - 1) * GAMMA * GAMMA * SCALE, (last - first) * p_0 * p_0, 0)[0])
        row["K_proper"] = int(division_forward((n - 1) * GAMMA * GAMMA * SCALE, between * p_0, 0)[0])
        row["E_proper_scaled"] = int(division_forward((n - 1) * GAMMA * SCALE, between, 0)[0])
    return row


def wave(mode: str) -> dict:
    """(c) The standing wave under the ride (adiabatic or sudden; uncentred: V1's letter with no half-wall move, the control of the drift) or under Rule3 (rule3) on the same lay and schedule."""
    now, before, r = wave_lay()
    if mode == "rule3":
        r = np.full(SHAPE, int(division_forward(W, 2, 0)[0]), dtype=object)  # Rule3's half wall, w div 2
    contents = schedule(mode == "sudden")
    centred = mode != "uncentred"
    traces: dict[int, list[int]] = {}
    propers: dict[int, list[int]] = {}
    x_before = volume_at(contents[0])
    for t, level in enumerate(contents):
        x_now = volume_at(level)
        if level in PLATEAUS:
            traces.setdefault(level, []).append(int(now[0, 0, 0]))
            propers.setdefault(level, []).append(paces_at(level)[0])
        if mode == "rule3":
            now, before, r = rule3_forward(now, before, r, DEN, level)
        else:
            now, before, r = ride_forward(now, before, r, x_now, x_before, DEN, level, centred)
        x_before = x_now
        if t % 300 == 0:
            print(f"{mode}: interval {t} of {len(contents)} at the level {level}", flush=True)
    rows = []
    for level in PLATEAUS:
        row = plateau_reading(level, traces[level], propers[level])
        row["mean_level_sum"] = int(sum(int(a) for a in traces[level]) // len(traces[level]))  # the antinode's mean over the span: the uniform mode's drift
        rows.append(row)
        print(
            f"{mode} plateau {level:5d} X {row['X']:8d} e^U x1e6 {row['e_U_scaled']:8d} mean {row['mean_level_sum']:6d} crossings {row['crossings']:3d} "
            f"period {row.get('period_board')} A {row['amplitude']:5d} A e^U x1e3 {row['amplitude_e_U_scaled']:8d} "
            f"J_rule3 {row['J_rule3']:8d} J_ride {row['J_ride']:8d} K_board {row.get('K_board')} K_proper {row.get('K_proper')} "
            f"E_proper x1e6 {row.get('E_proper_scaled')} cos residual x1e6 {row['cosine_residual_scaled']}"
        )
    return {"mode": mode, "shape": SHAPE, "A": AMPLITUDE, "plateaus": rows}


def share_at(num: int, now, before, level: int):  # type: ignore[no-untyped-def]
    """The share at every Node (share.share's plain form, the frame's term halved as the engine has it), in the current's units."""
    p_0, p_a = paces_at(level)
    reads, self_coefficient, wall = coefficients(num, DEN, GAMMA, p_0, p_a, None, G)
    arrived = tuple(np.asarray(v, dtype=object) for v in ports(before))
    arrived_now = tuple(np.asarray(v, dtype=object) for v in ports(now))
    link = sum(read * arrival for read, arrival in zip(reads, arrived, strict=True))
    found = form_term(self_coefficient, wall, now, before) - now * link
    shared = sum(read * (before - b_j) * (now + n_j) for read, b_j, n_j in zip(reads, arrived, arrived_now, strict=True))
    found = found + found - shared
    return np.asarray(division_forward(found, 4 * p_a * p_a * G * G, 0)[0], dtype=object)


def gapped() -> dict:
    """(e) A one-Node record of the gapped pair (779, 1021), g = 242 / 1021, laid at the centre of the 3-cube at its rest rotation, X raised by hand 0 -> 1000 over 500 intervals and held, under the ride and under Rule3: per window of 50 the crossings, the largest level, the share at the Node over the board's share."""
    num = 779
    shape, centre = (3, 3, 3), (1, 1, 1)
    results = {}
    for mode in ("ride", "rule3"):
        a = 20000
        now = np.zeros(shape, dtype=object)
        before = np.zeros(shape, dtype=object)
        now[centre] = a
        before[centre] = int(division_forward(a * num, DEN, 0)[0])  # A cos omega_0, the rest rotation
        r = np.full(shape, int(division_forward(W * GAMMA if mode == "ride" else W, 2, 0)[0]), dtype=object)
        levels = [min(1000, 2 * t) for t in range(800)]
        x_before = volume_at(0)
        windows = []
        trace: list[int] = []
        shares: list[tuple[int, int]] = []
        for t, level in enumerate(levels):
            x_now = volume_at(level)
            trace.append(int(now[centre]))
            s = share_at(num, now, before, level)
            shares.append((int(s[centre]), int(s.sum())))
            if mode == "ride":
                now, before, r = ride_forward(now, before, r, x_now, x_before, num, level)
            else:
                now, before, r = rule3_forward(now, before, r, num, level)
            x_before = x_now
            if (t + 1) % 50 == 0:
                window = trace[t + 1 - 50 : t + 1]
                n = sum(1 for u in range(1, len(window)) if window[u - 1] < 0 <= window[u])
                amplitude = max(abs(v) for v in window)
                p_0, p_a = paces_at(level)
                x = volume_at(level)
                centre_share, total = shares[t]
                windows.append(
                    {
                        "end": t + 1,
                        "level": level,
                        "X": x,
                        "e_U_scaled": int(division_forward(GAMMA * SCALE, p_0, 0)[0]),
                        "crossings": n,
                        "amplitude": amplitude,
                        "share_centre_over_total_scaled": int(division_forward(centre_share * SCALE, total, 0)[0]) if total else None,
                        "share_centre_in_W_c_scaled": int(division_forward(centre_share * SCALE, 3 * DEN * ACTION, 0)[0]),
                        "A2_X_over_Gamma_scaled": int(division_forward(amplitude * amplitude * x, GAMMA, 0)[0]),
                    }
                )
                print(
                    f"gapped {mode} end {t + 1:4d} level {level:4d} X {x:6d} e^U x1e6 {windows[-1]['e_U_scaled']} crossings {n:2d} A {amplitude:6d} "
                    f"A^2 X / Gamma {windows[-1]['A2_X_over_Gamma_scaled']} share centre/total x1e6 {windows[-1]['share_centre_over_total_scaled']} "
                    f"centre share in W_c x1e6 {windows[-1]['share_centre_in_W_c_scaled']}"
                )
        results[mode] = windows
    return {"pair": [num, DEN], "windows": results}


def main() -> None:
    part = sys.argv[1] if len(sys.argv) > 1 else "bijection"
    if part == "bijection":
        found = bijection()
    elif part == "seed":
        found = seed()
    elif part in ("adiabatic", "sudden", "rule3", "uncentred"):
        found = wave(part)
    elif part == "gapped":
        found = gapped()
    else:
        raise SystemExit(f"unknown part {part}")
    print(json.dumps(found, indent=1, default=str) if part == "bijection" else "")
    (OUT / f"ride_lines_{part}.json").write_text(json.dumps(found, indent=1, default=str), encoding="utf-8")
    print("written", OUT / f"ride_lines_{part}.json")


if __name__ == "__main__":
    main()
