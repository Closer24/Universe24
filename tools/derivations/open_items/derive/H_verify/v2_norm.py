"""H_verify v2: F-H5 (the six grips normalised by their A1 sum) against the head's grips, pure integers, python3 -I.

Q(t) = (G^2 (Gamma - t)^2 + Gamma^2 div 2) div Gamma^2 (rule3.mesh_factor); head grip 2 pinion p^2 Q_j;
F-H5 grip (2 pinion p^2 C Q_j) div S, C = 6 G^2, S = SUM Q_j. Grips printed in the unit 2 pinion p^2 (pinion = p = 1).
"""

import random

GAMMA, G = 1000, 16
C = 6 * G * G


def q(t):
    return (G * G * (GAMMA - t) ** 2 + GAMMA * GAMMA // 2) // (GAMMA * GAMMA)


def head(ts):
    return [q(t) for t in ts]


def fh5(ts):
    qs = head(ts)
    s = sum(qs)
    if s == 0:
        return None  # F-H5's formula has no value at S = 0: the probe's np.where guard
    return [(C * x) // s for x in qs]


def show(name, ts):
    h, f = head(ts), fh5(ts)
    print(f"{name:40s} tensions {ts}: head {h} (sum {sum(h)}), F-H5 {f} (sum {None if f is None else sum(f)})")


def main():
    print(f"Gamma {GAMMA}, G {G}, C = 6 G^2 = {C}")
    show("vacuum", [0] * 6)
    for t in (10, 100, 300, 600):
        show(f"uniform t = {t} (pure trace)", [t] * 6)
    show("one Mesh at t = 100", [100, 0, 0, 0, 0, 0])
    show("one axis at t = 100 (both sides)", [100, 100, 0, 0, 0, 0])
    show("traceless (100, 100, -100, -100, 0, 0)", [100, 100, -100, -100, 0, 0])
    show("traceless (10, 10, -10, -10, 0, 0)", [10, 10, -10, -10, 0, 0])
    show("five at the horizon band, one open", [960, 960, 960, 960, 960, 0])
    band = [t for t in range(800, 1201) if q(t) == 0]
    print(f"Q(t) = 0 exactly on t in [{band[0]}, {band[-1]}] ({len(band)} tensions): S = 0 when all six lie there")
    # first-order departure: relative change of the grip sum, head against F-H5, over random tensions in [0, 200]
    rng = random.Random(24)
    worst_first = 0
    for _ in range(2000):
        ts = [rng.randint(0, 200) for _ in range(6)]
        h, f = head(ts), fh5(ts)
        worst_first = max(worst_first, sum(f) - sum(h))
    print(f"tensions in [0, 200] (the head's own range, no clamp acting), 2000 draws: the grip sum F-H5 minus head up to {worst_first} of {C}")
    # the cone with F-H5: D + 2 SUM R <= 4 w needs p <= Gamma (F-H4 or F5); at a hill p > Gamma it fails
    rim, pinion = 1, 1
    for p0, p in ((GAMMA, GAMMA), (GAMMA + 50, (GAMMA + 50) ** 2 // GAMMA)):
        w = 6 * rim * GAMMA * GAMMA * G * G
        d = 12 * (rim - pinion) * p0 * p0 * G * G
        ts = [rng.randint(-300, 900) for _ in range(6)]
        qs = head(ts)
        s = sum(qs)
        grips = [(2 * pinion * p * p * C * x) // s for x in qs]
        print(f"rate p0 {p0}, mesh rate {p}: D + 2 SUM R - 4 w = {d + 2 * sum(grips) - 4 * w} (<= 0 inside the cone)")


if __name__ == "__main__":
    main()
