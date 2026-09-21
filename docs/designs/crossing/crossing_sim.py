"""Offline check of the crossing rule on the experimenter's heading stream
(doppler_test/make_and_run.py): rows born one per interval at x = 0, the
row of age tau at m(tau) = (2 tau Q + T) // (2 T), Q 64, T 110; a body
stepping one Link per k intervals, toward (-x) or away (+x). The interval's
order is the design's: the body steps at the walk (mark e this interval),
then the reading. No engine code is used; integers only.

    python crossing_sim.py
"""

from __future__ import annotations

Q, T = 64, 110
START = 40


def m(tau: int) -> int:
    return (2 * tau * Q + T) // (2 * T) if tau >= 0 else -(10**9)


def run(k: int, sense: int, ticks: int, x0: int = START, births_from: int = -109) -> dict:
    # births: the pre-filled stream (ages 0..109 at tick 0) and the lamp's new rows.
    births = list(range(births_from, ticks + 1))
    R = {0: x0}
    mark = {0: 0}
    reads: dict[int, list[tuple[int, str]]] = {}
    ever: dict[int, list[int]] = {}
    for t in range(1, ticks + 1):
        stepped = sense if t % k == 0 else 0
        R[t] = R[t - 1] + stepped
        mark[t] = stepped
        X, origin = R[t], R[t - 1]
        got: list[tuple[int, str]] = []
        for b in births:
            if b > t:
                continue
            r1, r0 = m(t - b), m(t - 1 - b)  # now, before the walk
            u = +1  # the stream flies +x
            if stepped:
                e = stepped
                # C1: the row crossed the body's Link in the opposite sense (the swap).
                if r0 == X and r1 == origin:
                    got.append((b, "C1 swap on the Link"))
                    continue
                # C2: resident at the destination, moving against the step.
                if r1 == X and r0 == X and u * e < 0:
                    got.append((b, "C2 resident at the destination"))
                    continue
                # C3 at a step interval: an arrival at X.
                if r1 == X and r0 != X:
                    if u * e > 0 and r0 == origin:
                        continue  # came with the body from its origin: met there
                    got.append((b, "C3 arrival (the body arrived too)"))
                    continue
            else:
                if r1 == X and r0 != X:
                    # C3: an arrival at the body's Node; the leapfrog pause re-read skipped.
                    e_prev = mark[t - 1]
                    if e_prev and u * e_prev > 0 and r0 == R[t - 2] and m(t - 2 - b) == r0:
                        continue
                    got.append((b, "C3 arrival"))
        reads[t] = got
        for b, _ in got:
            ever.setdefault(b, []).append(t)
    twice = {b: ts for b, ts in ever.items() if len(ts) > 1}
    # Rows that crossed the body's world line within the run: behind at some tick
    # and ahead later (strictly), whose crossing lies inside [1, ticks].
    missed = []
    for b in births:
        if b > ticks:
            continue
        pos = [(t, m(t - b)) for t in range(max(1, b), ticks + 1)]
        behind = [t for t, p in pos if p < R[t]]
        ahead = [t for t, p in pos if p > R[t]]
        if behind and ahead and min(ahead) > min(behind) and b not in ever:
            missed.append(b)
    windows = []
    bounds = [0] + [t for t in range(1, ticks + 1) if t % k == 0]
    for lo, hi in zip(bounds[:-1], bounds[1:], strict=True):
        windows.append(sum(len(reads[t]) for t in range(lo + 1, hi + 1)))
    return {
        "R": R,
        "reads": reads,
        "twice": twice,
        "missed": missed,
        "windows": windows,
        "total": sum(len(v) for v in reads.values()),
    }


if __name__ == "__main__":
    for k, sense, ticks in ((4, -1, 32), (8, -1, 48), (4, +1, 32), (8, +1, 48)):
        out = run(k, sense, ticks)
        name = f"{'toward' if sense < 0 else 'away'}_k{k}"
        print(
            f"== {name}: windows {out['windows']} total {out['total']} / {ticks}; "
            f"read twice {out['twice']}; missed {out['missed']}"
        )
        for t in range(1, ticks + 1):
            if t % k == 0 or any(tag != "C3 arrival" for _, tag in out["reads"][t]):
                print(f"   tick {t} body {out['R'][t - 1]}->{out['R'][t]}: {out['reads'][t]}")
    # The exact sum over a period: 32 Links crossed = 32 k intervals, the body
    # started far from both ends (a long GameBoard, no face), stream pre-filled.
    for k in (4, 8):
        for sense in (-1, +1):
            ticks = 32 * k
            out = run(k, sense, ticks, x0=400, births_from=-700)
            print(
                f"period k={k} sense={sense:+d}: total {out['total']} over {ticks} "
                f"(expected {ticks + 55 if sense < 0 else ticks - 55}); twice {len(out['twice'])}; missed {out['missed']}"
            )
