"""Lorentz from the delay field, the arithmetic (read-only, the derivation
mathematician, 2026-09-21; DERIVATIONS_BEAM.md section 12): (1) the age
moment of a uniformly moving source is the Lienard-Wiechert potential,
kappa R_ret = sqrt(x_par^2 + (1 - beta^2) x_perp^2), Heaviside's ellipsoid;
(2) the exchange rates between co-moving bodies in the continuum limit of
the law's push, without and with the Galilean aberration of the released
fan, against the classical field; (3) the same on the register's
deuteron fan with the engine's own flight table at k = 4 and 8 (the pins
of section 10 reproduced, then with the aberration rule), and the
recoil the aberrated fan gives a lamp.

Run from the repository root with PYTHONPATH=src:

    python docs/designs/derivations_beam/lorentz_field.py > docs/designs/derivations_beam/lorentz_field.out

A host computation on the engine's flight table; no engine run.
"""

from __future__ import annotations

import math
import random
from pathlib import Path

import numpy as np

from event_universe.events.nature_beam import Q, nature_beam_tables
from event_universe.world_loading import load_world

# 1. The potential of a moving source.
print("1. THE AGE MOMENT OF A MOVING SOURCE: kappa R_ret against sqrt(x_par^2 + (1 - beta^2) x_perp^2)")
random.seed(3)
worst = 0.0
for _ in range(1000):
    beta = random.uniform(0, 0.95)
    x = np.array([random.uniform(-5, 5) for _ in range(3)])
    # the source at the origin now, moving along +x at beta (c = 1): the retarded time tau > 0 with
    # |x + beta tau x_hat| = tau
    b = x[0] * beta
    tau = (b + math.sqrt(b * b + (1 - beta * beta) * x @ x)) / (1 - beta * beta)
    r_ret = np.array([x[0] + beta * tau, x[1], x[2]])
    n = r_ret / tau
    kappa = 1 - beta * n[0]
    lhs = kappa * tau
    rhs = math.sqrt(x[0] ** 2 + (1 - beta * beta) * (x[1] ** 2 + x[2] ** 2))
    worst = max(worst, abs(lhs - rhs) / rhs)
print(
    f"  1000 random points and speeds: the identity holds to {worst:.1e}; the age moment A = q dwell / (4 pi c kappa R_ret)"
)
print(
    "  has the level sets x_par^2 + (1 - beta^2) x_perp^2 = const, ellipsoids contracted along the motion by sqrt(1 - beta^2);"
)
print("  the presence P = q dwell / (4 pi kappa R_ret^2) has not (kappa R_ret^2 is no quadric).")


# 2. The co-moving exchange in the continuum limit.
def jacobian(beta: float, theta_prime: float) -> float:
    """dOmega / dOmega' of the Galilean aberration n -> (n + beta x_hat) / |n + beta x_hat| at the
    arrival direction theta' (from +x): the fan's density per steradian there over the rest density,
    (1 + 2 beta cos theta + beta^2)^(3/2) / (1 + beta cos theta) at the fan angle theta that maps to theta'."""

    def forward(theta: float) -> float:
        return math.atan2(math.sin(theta), math.cos(theta) + beta)

    lo, hi = 0.0, math.pi
    for _ in range(200):
        mid = (lo + hi) / 2
        if forward(mid) < theta_prime:
            lo = mid
        else:
            hi = mid
    c = math.cos((lo + hi) / 2)
    return (1 + 2 * beta * c + beta * beta) ** 1.5 / (1 + beta * c)


print(
    "\n2. THE EXCHANGE BETWEEN CO-MOVING BODIES, THE CONTINUUM LIMIT (rows received per interval over the rest rate)"
)
print(
    "  beta | forward, no aberration (1-b)^2 | backward (1+b)^2 | transverse (1-b^2) | Galilean aberration: forward | backward | transverse (J (1-b^2)) | classical E: longitudinal (1-b^2) | transverse 1/gamma | transverse drag component beta"
)
for beta in (0.2148, 0.4297):
    gamma = 1 / math.sqrt(1 - beta * beta)
    j_fwd = jacobian(beta, 0.0)
    j_back = jacobian(beta, math.pi)
    theta_t = math.acos(beta)  # the arrival direction of a transverse target
    j_t = jacobian(beta, theta_t)
    print(
        f"  {beta:.4f} | {(1 - beta) ** 2:.3f} | {(1 + beta) ** 2:.3f} | {1 - beta * beta:.3f} | {j_fwd * (1 - beta) ** 2:.3f} | {j_back * (1 + beta) ** 2:.3f} | {j_t * (1 - beta * beta):.3f} | {1 - beta * beta:.3f} | {1 / gamma:.3f} | {beta:.3f}"
    )
print(
    "  the round trips of the exchange (transit forward + back, over the rest 2 d / c): longitudinal d/(c-v) + d/(c+v) = gamma^2 x rest, transverse 2 gamma d / c = gamma x rest, with or without aberration;"
)
for beta in (0.2148, 0.4297):
    gamma = 1 / math.sqrt(1 - beta * beta)
    print(f"    beta {beta:.4f}: gamma {gamma:.3f}, gamma^2 {gamma * gamma:.3f}")

# 3. The register's deuteron fan with the engine's flight table.
print(
    "\n3. THE DEUTERON FAN (deuteron_1_kick, 290 directions) AT k = 4 AND 8: section 10.2's counts, then with the aberration rule"
)
path = Path(__file__).resolve().parents[3] / "examples" / "events" / "nucleus" / "deuteron_1_kick.json"
world = load_world(path.read_bytes(), base_dir=path.parent).world
flight = nature_beam_tables(world).flight
vectors = [tuple(int(c) for c in v) for v in flight.vectors]
fan = list(world.measured[0].directions) if hasattr(world.measured[0], "directions") else None
if fan is None:
    fan = [i for i, v in enumerate(vectors) if any(v) and i >= 2]
fan = [i for i in fan if any(vectors[i])]
print(f"  fan of {len(fan)} directions; T_D of the heading {int(flight.resolution[fan[0]])}")


def walk(direction: int, ages: int) -> list[tuple[int, int, int]]:
    """The positions of a row of this direction after 1 .. ages walks from the origin."""
    pos = np.zeros(3, dtype=np.int64)
    out = []
    period = int(flight.period[direction])
    for age in range(ages):
        pos = pos + flight.steps[direction, age % period]
        out.append(tuple(int(c) for c in pos))
    return out


def nearest(w: tuple[int, int, int]) -> int:
    """The table's direction nearest to the integer vector w by the exact comparison
    (w . D)^2 |D'|^2 >= (w . D')^2 |D|^2 with w . D > 0 (light_speed/FORM.md section 3), among the fan."""
    best = None
    for i in fan:
        d = vectors[i]
        dot = sum(a * b for a, b in zip(w, d, strict=True))
        if dot <= 0:
            continue
        key = (dot * dot, sum(c * c for c in d))
        if best is None or key[0] * best[1][1] > best[1][0] * key[1]:
            best = (i, key)
    assert best is not None
    return best[0]


def exchange(k: int, aberrated: bool, axis_target: bool):
    """Rows received per cycle by the partner and their transits, on the axis (the front body,
    forward) or transverse, as section 10.2 counts them; and the backward exchange on the axis."""
    v_num = 1  # the body's speed 1 / k Links per interval: w = k Q D + T_D x_hat
    dirs = {}
    for i in fan:
        if aberrated:
            d = vectors[i]
            w = (k * Q * d[0] + int(flight.resolution[i]) * v_num, k * Q * d[1], k * Q * d[2])
            dirs[i] = nearest(w)
        else:
            dirs[i] = i
    target2 = (2, 0, 0) if axis_target else (1, 1, 0)
    first = (1, 0, 0) if axis_target else (0, 1, 0)
    n2 = {2: 0, 3: 0}
    f_first = 0
    f_back = 0
    for i in fan:
        p = walk(dirs[i], 3)
        if p[0] == first:
            f_first += 1
        if p[0] == (-1, 0, 0):
            f_back += 1
        if p[0] != first:
            continue  # a first Link elsewhere: on the axis it cannot reach Node 2 in time; transverse it lands on its emitter's new Node and goes home
        if p[1] == target2:
            n2[2] += 1
        elif p[2] == target2:
            n2[3] += 1
    n2_total = n2[2] + n2[3]
    received = n2_total + f_first * (k - 1)
    if axis_target:
        transit = (
            (2 * n2[2] + 3 * n2[3] + 3 * f_first + f_first * (k - 2)) / received
            if received
            else float("nan")
        )
    else:
        transit = (2 * n2[2] + 3 * n2[3] + f_first * (k - 1)) / received if received else float("nan")
    return f_first, n2, received, transit, f_back


for k in (4, 8):
    beta = (1 / k) / (32 / 55)
    gamma = 1 / math.sqrt(1 - beta * beta)
    for aberrated in (False, True):
        f1, n2, rec, tr, fb = exchange(k, aberrated, True)
        ft, n2t, rect, trt, _ = exchange(k, aberrated, False)
        label = "aberrated" if aberrated else "as built "
        back = fb * k
        round_trip = tr + 1.0
        print(
            f"  k = {k} (v / c = {beta:.4f}, gamma {gamma:.3f}, gamma^2 {gamma * gamma:.3f}), {label}: first-Link +x directions {f1}, reaching Node 2 at age 2 / 3: {n2[2]} / {n2[3]}; forward received per cycle {rec} of {57 * k}, mean forward transit {tr:.3f}, round trip {round_trip:.3f} = {round_trip / 2:.3f} x rest; backward received {back} of {57 * k} (first-Link -x directions {fb}); transverse: first-Link +y {ft}, reaching (1, 1, 0) at age 2 / 3: {n2t[2]} / {n2t[3]}, received {rect} of {47 * k}, mean transit {trt:.3f}"
        )

# 4. The aberrated fan's recoil on a lamp (label units per unit of amount born).
print(
    "\n4. THE RECOIL OF THE ABERRATED FAN (the labels' sum over the fan, per unit of amount on each direction)"
)
for k in (4, 8):
    rest = np.zeros(3, dtype=np.int64)
    moved = np.zeros(3, dtype=np.int64)
    for i in fan:
        d = vectors[i]
        rest += flight.labels[i]
        w = (k * Q * d[0] + int(flight.resolution[i]), k * Q * d[1], k * Q * d[2])
        moved += flight.labels[nearest(w)]
    beta = (1 / k) / (32 / 55)
    print(
        f"  k = {k}: the fan's labels sum at rest {rest.tolist()}, aberrated {moved.tolist()} (label units; the continuum estimate (2/3) K beta Q = {2 / 3 * len(fan) * beta * Q:.0f} on x): a lamp in motion takes the recoil {(-moved).tolist()} per unit of amount per direction born"
    )
