"""Run 14, section 10: a CHECK, not a pin. The advance and the two centroids
re-derived by the engine's own kernels on the REPLAYED crowd along the
row's line, against the read -115.3 counts, 11.0 and 18.85 pixels
(docs/designs/fail_rows/RUN_14.md section 9; the reviewer's reading (1)
of 2026-09-23, the Boss's order; no world, no key, no run of a pin).

The inputs (GAMEBOARD, labelled so, never pinned): the two numbers the
law reads at a Node the row is at, captured from inside the engine's own
interval at every Node of the line y = 26, z = 20, x = 2 to 54 of the
`mass` and `light` worlds, for INTERVALS intervals:

- a_tau(x, t), the crowd's age moment the wall reads (`CrowdMoments.age_moment`,
  the rows of other numbers present at the end of the interval before,
  `nature_beam.py` about line 3238; read by `optical_walk_step`, line
  3841, through `optical_rate_and_wall`, line 3809, and the one wall
  function `core.integer.age_wall`, line 175: the rate times d against
  the wall times (d + c_f n a_tau));
- **V**(x, t), the arrival flow the push reads (`CrowdMoments.arrival_flow`,
  line 3250: sum amount x u over the rows that arrived at the Node in
  this interval, less the reader's own number's; read by `optical_turn`,
  line 3953: **W** -= n weight **V**, the weight content x (E'_D^2 + 3
  gamma p_D . p_D) // E'_D per unit, `unit_weights`, line 3770).

The kernels (COMPUTATION at rung 1, the design's closed forms with the
replayed means in place of the shell mean; the same forms as
NEWTON_FROM_CLICKS 3 (b) to (d) with k_a(x) = (n / d) a_tau(x) read and
**V**(x) read): the row advances 52 steps in x from the lamp to the
plane; its counts per Manhattan Link are its momentum's pair's, c(**P**)
= sqrt(R^2 + 3 abs(**P**)^2) / abs(**P**)_1 (`momentum_pair`, line 3697;
T / (S_1 Q)), and a step in x costs abs(**P**)_1 / P_x Manhattan Links
on **P**'s line (Bresenham), so the dwell per step in x is d(x) =
(E'(**P**) / P_x) (1 + c_f (n / d) <a_tau(x, y)>) counts with E'(**P**)
= sqrt(R^2 + 3 abs(**P**)^2); at every free Node (a Node without a
measured event: the lamp's and the receivers' excluded, `optical_turn`)
the push **W** -= n weight <**V**(x, y)> acts per interval of the dwell,
**P** = Q d content **p**_D + **W**; the transverse displacement grows
by P_y / P_x per step in x. The crowd is read on the STRAIGHT line y =
26 (the design's straight-path form) and on the BENT line, the Node (x,
round(y)) the kernel's own displacement puts the row at (the crowd
captured on the band y = 4 to 27). The advance is the sum of the dwells
less the unpushed 52 c(**P**_0); the centroid toward the mass is minus
the displacement in y at the plane. Means over the intervals WINDOW to
INTERVALS (the crowd steady from about the 60th interval).

Beside the kernel, the engine's own rows (GAMEBOARD, the store of the
lamp's family in the same replay): per x, the mean of their push
accumulator (W_x, W_y) over the label's momentum P_0, their mean y, and
their mean age at the plane x = 54 (the flight's count in ticks): the
direct comparison of the kernel's momentum profile and pace with what
the engine did, apart from the clicks (which add the two clocks' rates,
RUN_14.md 9.2).

    PYTHONPATH=src python docs/designs/fail_rows/run_14_check.py > docs/designs/fail_rows/run_14_check.out
"""

from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from event_universe.events import NatureBeamSimulation, nature_beam  # noqa: E402
from event_universe.world_loading import load_world  # noqa: E402

WORLDS = ROOT / "examples" / "events" / "newton_side"
LINE_Y, LINE_Z = 26, 20
X_FIRST, X_LAST = 2, 54
BAND = list(range(4, 28))
XS = list(range(X_FIRST, X_LAST + 1))
INTERVALS = 1000
WINDOW = 101
LAMP_NUMBER = 1
Q = 64
# The read values of RUN_14.md section 9 (DETECTOR): the advance in counts,
# the centroids in pixels toward the mass.
READ = {"mass": {"advance": -115.34, "centroid": 11.01}, "light": {"delay": 21.14, "centroid": 18.85}}


def replay(name: str) -> dict[str, object]:
    """The crowd's two readings at the band's Nodes, per interval, captured
    from inside `optical_turn` (the frame's crowd of the wall, read before
    step 1, and the arrival flow of the push, read after the walk), and
    the engine's own rows of the lamp's family: their push accumulators
    and y per x, their age at the plane."""
    path = WORLDS / f"{name}.json"
    world = load_world(path.read_bytes(), base_dir=path.parent, root=path.parent.parent).world
    simulation = NatureBeamSimulation(world)
    store = simulation.stores[0]
    nodes = np.array(
        [x * store.strides[0] + y * store.strides[1] + LINE_Z for x in XS for y in BAND], dtype=np.int64
    )
    numbers = np.full(nodes.shape[0], LAMP_NUMBER, dtype=np.int64)
    lamp = world.measured[0]
    family = lamp.family
    a_sum = np.zeros(nodes.shape[0], dtype=np.float64)
    v_sum = np.zeros((nodes.shape[0], 3), dtype=np.float64)
    counted = 0
    push_x: dict[int, list[int]] = {x: [] for x in XS}
    push_y: dict[int, list[int]] = {x: [] for x in XS}
    ys: dict[int, list[int]] = {x: [] for x in XS}
    ages_at_plane: list[int] = []
    ticks = [0]
    original = nature_beam.optical_turn

    def capturing(frame):  # type: ignore[no-untyped-def]
        nonlocal counted
        ticks[0] += 1
        if ticks[0] < WINDOW:
            return original(frame)
        assert frame.crowd is not None
        crowd = nature_beam.CrowdMoments(frame.stores, [t.flow_labels for t in frame.family_flights])
        a_sum[:] += frame.crowd.age_moment(nodes, numbers)
        v_sum[:] += crowd.arrival_flow(nodes, numbers)
        counted += 1
        rows = frame.stores[family]
        if rows.size:
            x, y, z = rows.coordinates(rows.node)
            for xi, yi, zi, wx, wy, age in zip(
                x.tolist(), y.tolist(), z.tolist(), rows.push_x.tolist(), rows.push_y.tolist(),
                rows.age.tolist(), strict=True,
            ):  # fmt: skip
                if zi != LINE_Z or xi not in push_x:
                    continue
                push_x[xi].append(int(wx))
                push_y[xi].append(int(wy))
                ys[xi].append(int(yi))
                if xi == X_LAST:
                    ages_at_plane.append(int(age))
        return original(frame)

    nature_beam.optical_turn = capturing
    started = time.perf_counter()
    try:
        for _ in range(INTERVALS):
            simulation.step()
    finally:
        nature_beam.optical_turn = original
    elapsed = time.perf_counter() - started
    table = simulation.tables.family_flights[family]
    assert lamp.lamp is not None
    direction = int(lamp.lamp.directions[0])
    a = (a_sum / counted).reshape(len(XS), len(BAND))
    v = (v_sum / counted).reshape(len(XS), len(BAND), 3)
    scale = Q * int(world.suspension[1]) * int(world.families[family].quantum)
    p0x = scale * int(table.labels[direction][0])
    profile = {
        x: (
            float(np.mean(push_x[x])) / p0x if push_x[x] else math.nan,
            float(np.mean(push_y[x])) / p0x if push_y[x] else math.nan,
            float(np.mean(ys[x])) if ys[x] else math.nan,
        )
        for x in XS
    }
    return {
        "name": name,
        "elapsed": elapsed,
        "intervals_counted": counted,
        "content": int(world.families[family].quantum),
        "label": [int(c) for c in table.labels[direction]],
        "rest": int(table.rest),
        "weight_per_unit": int(table.weight[direction]),
        "suspension": [int(world.suspension[0]), int(world.suspension[1])],
        "coefficient": 1 + int(world.optical),
        "a": a,
        "v": v,
        "profile": profile,
        "age_at_plane": (
            float(np.mean(ages_at_plane)) if ages_at_plane else math.nan,
            len(ages_at_plane),
        ),
    }


def walk(reading: dict[str, object], bent: bool) -> dict[str, object]:
    """The row's 52 steps in x by the kernels at rung 1 on the replayed
    means, the crowd read on the straight line (y = 26) or on the bent one
    (the Node the kernel's own displacement puts the row at)."""
    n, d = reading["suspension"]  # type: ignore[misc]
    c_f = int(reading["coefficient"])
    content = int(reading["content"])
    label = np.array(reading["label"], dtype=np.float64)
    scale = Q * d * content
    p = scale * label
    rest = scale * int(reading["rest"])
    weight = content * int(reading["weight_per_unit"])
    a = reading["a"]
    v = reading["v"]

    def energy(momentum: np.ndarray) -> float:
        return math.sqrt(rest * rest + 3.0 * float(momentum @ momentum))

    c0 = energy(p) / float(np.abs(p).sum())
    counts = 0.0
    wall_only = 0.0
    dy = 0.0
    momentum = p.copy()
    path: list[tuple[int, int, float, float]] = []
    for k, x in enumerate(XS[:-1]):
        y = int(round(LINE_Y + dy)) if bent else LINE_Y
        y = min(max(y, BAND[0]), BAND[-1])
        j = BAND.index(y)
        k_a = n * float(a[k, j]) / d  # type: ignore[index]
        dwell = energy(momentum) / float(momentum[0]) * (1.0 + c_f * k_a)
        wall_only += c0 * c_f * k_a
        if X_FIRST < x < X_LAST:
            momentum = momentum - n * weight * dwell * v[k, j]  # type: ignore[index]
        counts += dwell
        dy += float(momentum[1] / momentum[0])
        path.append((x, y, float(momentum[0] / p[0]), float(momentum[1] / p[0])))
    return {
        "counts_per_link_unpushed": c0,
        "counts": counts,
        "advance": counts - 52 * c0,
        "wall_delay_alone": wall_only,
        "push_part": counts - 52 * c0 - wall_only,
        "centroid_toward_mass": -dy,
        "momentum_end_over_start": float(np.abs(momentum).sum() / np.abs(p).sum()),
        "path": path,
    }


def main() -> None:
    print(
        "CHECK (RUN_14.md section 10): the advance and the centroids by the kernels on the replayed "
        f"crowd along the row's line (y = {LINE_Y} straight, or bent by the kernel's own displacement), "
        f"z = {LINE_Z}, x = {X_FIRST}..{X_LAST}; means over the intervals {WINDOW}..{INTERVALS}; every "
        "input GAMEBOARD, every output COMPUTATION, the read values DETECTOR"
    )
    for name in ("mass", "light"):
        reading = replay(name)
        a = reading["a"]
        v = reading["v"]
        j26 = BAND.index(LINE_Y)
        print(
            f"\n{name}: HOST {reading['elapsed']:.1f} s for {INTERVALS} intervals ({reading['intervals_counted']} "
            f"counted); the family's content {reading['content']}, label {reading['label']}, rest {reading['rest']}, "
            f"weight per unit {reading['weight_per_unit']}, the pair {reading['suspension']}, c_f {reading['coefficient']}"
        )
        print(
            f"  GAMEBOARD the replayed means on the straight line y = {LINE_Y}, per Node x: a_tau, V = (V_x, V_y, V_z):"
        )
        for k, x in enumerate(XS):
            print(
                f"    x = {x:2d}: a_tau {a[k, j26]:8.2f}  V ({v[k, j26][0]:8.2f}, {v[k, j26][1]:8.2f}, {v[k, j26][2]:8.2f})"  # type: ignore[index]
            )
        p0x = Q * reading["suspension"][1] * reading["content"] * reading["label"][0]  # type: ignore[index]
        print(
            f"  GAMEBOARD the engine's own rows per x: the mean y, the mean push accumulator W_x / P_0 and W_y / P_0 "
            f"(P_0 = {p0x}, the label's momentum; W_y jumps at the label's turns, where P is conserved and W is not):"
        )
        for x in XS[::4]:
            wx, wy, ym = reading["profile"][x]  # type: ignore[index]
            print(f"    x = {x:2d}: y {ym:6.2f}  W_x / P_0 {wx:+.4f}  W_y / P_0 {wy:+.4f}")
        age, count = reading["age_at_plane"]  # type: ignore[misc]
        print(
            f"  GAMEBOARD the engine's rows' mean age at the plane x = {X_LAST}: {age:.2f} ticks over {count} row-intervals"
        )
        results = {}
        for bent in (False, True):
            result = walk(reading, bent)
            results[bent] = result
            print(
                f"  COMPUTATION the kernel on the {'bent' if bent else 'straight'} line: counts per Link unpushed "
                f"{result['counts_per_link_unpushed']:.4f}; the 52 steps {result['counts']:.2f} counts; the advance "
                f"{result['advance']:+.2f} counts (the wall alone {result['wall_delay_alone']:+.2f}, the push "
                f"{result['push_part']:+.2f}); the centroid toward the mass {result['centroid_toward_mass']:.2f} pixels; "
                f"abs(P)_1 at the end over the start {result['momentum_end_over_start']:.4f}"
            )
            if bent:
                for x, y, px, py in result["path"][::8]:  # type: ignore[union-attr]
                    print(f"    kernel at x = {x:2d}: y {y:2d}  P_x / P_0 {px:.4f}  P_y / P_0 {py:+.4f}")
        result = results[True]
        read = READ[name]
        unpushed = 52 * result["counts_per_link_unpushed"]
        if name == "mass":
            print(
                f"  CHECK against the read (DETECTOR): the advance {result['advance']:+.2f} against {read['advance']:+.2f} "
                f"(the ratio {result['advance'] / read['advance']:.2f}); the centroid {result['centroid_toward_mass']:.2f} "
                f"against {read['centroid']:.2f} (the ratio {result['centroid_toward_mass'] / read['centroid']:.2f}); "
                f"and against the engine's rows' age at the plane (GAMEBOARD): the kernel's flight {result['counts']:.1f} "
                f"against {age:.1f} ticks (the unpushed {unpushed:.1f})"
            )
        else:
            print(
                f"  CHECK against the read (DETECTOR): the delay {result['advance']:+.2f} against the read T's excess "
                f"{read['delay']:+.2f} (the two clocks' rates in the read, section 9.2; the ratio "
                f"{result['advance'] / read['delay']:.2f}); the centroid {result['centroid_toward_mass']:.2f} against "
                f"{read['centroid']:.2f} (the ratio {result['centroid_toward_mass'] / read['centroid']:.2f}); "
                f"and against the engine's rows' age at the plane (GAMEBOARD): the kernel's flight {result['counts']:.1f} "
                f"against {age:.1f} ticks (the unpushed {unpushed:.1f})"
            )
        json.dump(
            {
                "name": name,
                "straight": {k: val for k, val in results[False].items() if k != "path"},
                "bent": {k: val for k, val in results[True].items() if k != "path"},
                "bent_path": results[True]["path"],
                "rows_profile": {str(x): list(reading["profile"][x]) for x in XS},  # type: ignore[index]
                "age_at_plane": list(reading["age_at_plane"]),  # type: ignore[arg-type]
            },
            (Path(__file__).parent / f"run_14_check_{name}.json").open("w", encoding="utf-8"),
            indent=1,
        )


if __name__ == "__main__":
    main()
