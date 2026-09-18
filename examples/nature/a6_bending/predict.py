"""The mean field's prediction for the worlds of experiment A6 (docs/EXPERIMENTS.md),
written before the run into `predictions.json` beside the worlds.

The computation, not an engine run: the kernel of
`examples/nature/a5_static/mean_field_gauss.py` (the table [6, 1, 1, 1, 1, 1] over 11
as the linear map it is on average, the expectation of the engine's integers, which
A5s Run 2 measured to a part in a thousand), on exactly the run's boxes: the star
releasing 8192 quanta per heading per interval from tick 0 and absorbing what
returns, the launcher absorbing what reaches it, the open boundary, and the light
ray at Node x = t - LAUNCH_DELAY - 1 of its line at tick t, x = 1 .. 64 (1 .. 48 on
the cube), pushed at every Node by minus the sum of amount x heading over the field
content that arrives there in that interval (the momentum turn, ray-momentum-turn-v2,
sign -1) and sending that content back reversed (the recoil) instead of spreading
it. The push summed over the pass is the light's momentum register at the end; the
deflection is the angle of the register, alpha = atan2(|transverse|, L + p_x). The
same pass integral at the box's steady state, the unscattered beam 8192 (6/11)^(b-1)
that meets the ray at the star's x, the steady pass on deeper boards (65 x 65 x 17
and 33; the register's board is 9 deep) and in free space (an octant of half-width
FREE_HALF_WIDTH with mirrored faces, the line through the star's plane) give the
model's own exponent in b beside the run's. The delay form's prediction is not a
mean-field number: it is read from the engine's code (README, "computed before
the run").

Run:  python examples/nature/a6_bending/predict.py [--out predictions.json] [--free-half-width 96]
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "a5_static"))
import mean_field_gauss as mf  # noqa: E402


def load_make_worlds():
    spec = importlib.util.spec_from_file_location("a6_make_worlds", HERE / "make_worlds.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


mw = load_make_worlds()
HEADINGS = np.array(mf.HEADINGS, dtype=float)
RELEASE = mw.AMOUNT * mw.RELEASE[0] // mw.RELEASE[1]
DEPTHS = (9, 17, 33)
FREE_HALF_WIDTH = 96
FREE_B = (4, 6, 8, 12, 16, 24, 32)


class PassBoard(mf.Board):
    """A box with the star (the source and a sink), the launcher (a sink) and the
    light ray, whose Node returns what arrives there reversed (the recoil of the
    turn rule) instead of spreading it. `path` maps a tick to the light's Node."""

    def __init__(self, shape, star, launcher, release, path):
        super().__init__(shape, (False, False, False), star, [star, launcher], release=release)
        self.path = path
        self._recoil = None

    def transport(self, f, out=None):
        if out is None:
            out = np.empty_like(f)
        g = mf.spread(f, self.table, self._g)
        if self._recoil is not None:
            node, column = self._recoil
            for j in range(6):
                g[(j ^ 1, *node)] = column[j]
            self._recoil = None
        return self.walk(g, out)

    def step_light(self, f, tick):
        """One interval: the arrivals, the push on the light at its Node of this tick
        (minus amount x heading summed over what arrived), the absorptions."""
        arrivals = self.arrivals(f, self._out)
        node = self.path.get(tick)
        push = np.zeros(3)
        if node is not None:
            column = arrivals[(slice(None), *node)].copy()
            push = -(column[:, None] * HEADINGS).sum(axis=0)
            self._recoil = (node, column)
        self.absorb(arrivals)
        f[...] = arrivals
        return f, push


def light_path(shape, star, offset, launch_delay):
    y, z = star[1] + offset[1], star[2] + offset[2]
    return {launch_delay + 1 + x: (x, y, z) for x in range(1, shape[0])}, (0, y, z)


def transient_pass(shape, star, offset, release=RELEASE, launch_delay=mw.LAUNCH_DELAY):
    """The push on the light summed over its pass, with the field stepped from the
    empty board at tick 0 exactly as the world runs; the per-tick pushes too."""
    path, launcher = light_path(shape, star, offset, launch_delay)
    board = PassBoard(shape, star, launcher, release, path)
    f = board.empty()
    total = np.zeros(3)
    per_tick = []
    for tick in range(1, max(path) + 1):
        f, push = board.step_light(f, tick)
        if tick in path:
            per_tick.append([tick, path[tick][0], [float(v) for v in push]])
            total += push
    return total, per_tick


def steady_pass(shape, star, offset, release=RELEASE, tol=1e-10):
    """The same sum over the line at the box's steady state (no recoil)."""
    _, launcher = light_path(shape, star, offset, 0)
    board = mf.Board(shape, (False, False, False), star, [star, launcher], release=release)
    f, iterations = board.steady_state(tol)
    arrivals = board.arrivals(f)
    y, z = launcher[1], launcher[2]
    total = np.zeros(3)
    for x in range(1, shape[0]):
        column = arrivals[(slice(None), x, y, z)]
        total += -(column[:, None] * HEADINGS).sum(axis=0)
    return total, iterations


def free_space_pass(half_width, release=RELEASE, distances=FREE_B, tol=1e-10):
    """The steady free-space pass integral on the line (x, b, 0), x over the whole
    line (the octant holds x >= 0 and the transverse flux is even in x); the line's
    tails beyond |x| = half_width are cut, about (1 - 2 / sqrt(4 + (b / half)^2 ...))
    which the caller reports as the truncation."""
    board = mf.Board((half_width + 1,) * 3, (True,) * 3, (0, 0, 0), [(0, 0, 0)], release=release)
    f, iterations = board.steady_state(tol)
    arrivals = board.arrivals(f)
    result = {}
    for b in distances:
        if b + 4 >= half_width:
            continue
        column = arrivals[(slice(None), 0, b, 0)]
        transverse = float(column[2] - column[3])
        for x in range(1, half_width):
            column = arrivals[(slice(None), x, b, 0)]
            transverse += 2.0 * float(column[2] - column[3])
        # The transverse flux points away from the star (+y on the +b side); the
        # push is minus it, toward the star.
        result[b] = {"push_toward_star": transverse, "alpha": alpha_of((mw.LIGHT, -transverse, 0.0))}
    return result, iterations


def alpha_of(register):
    px, py, pz = (float(v) for v in register)
    return math.atan2(math.hypot(py, pz), px)


def register_of(push):
    return [mw.LIGHT + float(push[0]), float(push[1]), float(push[2])]


def fit(points):
    slope, error = mf.fit_exponent(points)
    intercept = sum(math.log(v) for _, v in points) / len(points) - slope * sum(
        math.log(r) for r, _ in points
    ) / len(points)
    return {"exponent": slope, "error": error, "intercept": intercept}


def power_law(fitted, r):
    return math.exp(fitted["intercept"]) * r ** fitted["exponent"]


def beam(b):
    forward, _, _, total = mf.table_weights(mw.SPREAD)
    return RELEASE * (forward / total) ** (b - 1)


def case_rows():
    """(name, shape, star, offset, kind) for every turn-form case whose field the
    mean field predicts; the N scan, the slow ray and 2M share the b = 8 field."""
    for b in mw.AXIS_B:
        yield f"b{b}", mw.SLAB, mw.SLAB_STAR, (0, b, 0), "axis"
    for b in mw.AXIS_B:
        yield f"m{b}", mw.SLAB, mw.SLAB_STAR, (0, -b, 0), "other_side"
    for b in mw.CUBE_AXIS_B:
        yield f"c_b{b}", mw.CUBE, mw.CUBE_STAR, (0, b, 0), "cube_axis"
    for d in mw.CUBE_DIAGONAL_D:
        yield f"c_d{d}", mw.CUBE, mw.CUBE_STAR, (0, d, d), "cube_diagonal"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=HERE / "predictions.json")
    parser.add_argument("--free-half-width", type=int, default=FREE_HALF_WIDTH)
    args = parser.parse_args(argv)
    started = time.time()
    cases = {}
    for name, shape, star, offset, kind in case_rows():
        t0 = time.time()
        total, per_tick = transient_pass(shape, star, offset)
        steady, iterations = steady_pass(shape, star, offset)
        b = math.hypot(offset[1], offset[2])
        register = register_of(total)
        cases[name] = {
            "kind": kind,
            "shape": list(shape),
            "star": list(star),
            "offset": list(offset),
            "b": b,
            "push": [float(v) for v in total],
            "register": register,
            "alpha": alpha_of(register),
            "steady_push": [float(v) for v in steady],
            "steady_alpha": alpha_of(register_of(steady)),
            "beam": beam(round(b)) if kind in ("axis", "other_side", "cube_axis") else 0.0,
            "per_tick": per_tick,
            "seconds": time.time() - t0,
        }
        print(
            name,
            kind,
            "b",
            round(b, 3),
            "push",
            np.round(total, 2),
            "alpha",
            round(cases[name]["alpha"], 7),
            "steady alpha",
            round(cases[name]["steady_alpha"], 7),
            flush=True,
        )
    # The cases that share a field: the N scan (the light's width is read nowhere
    # in the mean field), the slow ray (the same push on the same content), 2M
    # (the field doubled, the mean field linear), the control (no field).
    shared = {
        "n8": ("b8", 1.0),
        "n10": ("b8", 1.0),
        "n14": ("b8", 1.0),
        "n16": ("b8", 1.0),
        "slow": ("b8", 1.0),
        "2m": ("b8", 2.0),
    }
    for name, (source, factor) in shared.items():
        base = cases[source]
        push = [factor * v for v in base["push"]]
        register = register_of(push)
        cases[name] = {
            "kind": "shared",
            "same_field_as": source,
            "factor": factor,
            "b": base["b"],
            "push": push,
            "register": register,
            "alpha": alpha_of(register),
            "steady_alpha": alpha_of(register_of([factor * v for v in base["steady_push"]])),
        }
    cases["control"] = {
        "kind": "control",
        "b": float(mw.SCAN_B),
        "push": [0.0, 0.0, 0.0],
        "register": [float(mw.LIGHT), 0.0, 0.0],
        "alpha": 0.0,
        "steady_alpha": 0.0,
    }
    axis_points = [(cases[f"b{b}"]["b"], cases[f"b{b}"]["alpha"]) for b in mw.AXIS_B]
    axis_steady = [(cases[f"b{b}"]["b"], cases[f"b{b}"]["steady_alpha"]) for b in mw.AXIS_B]
    cube_points = [(cases[f"c_b{b}"]["b"], cases[f"c_b{b}"]["alpha"]) for b in mw.CUBE_AXIS_B]
    cube_fit = fit(cube_points)
    diagonal = {}
    for d in mw.CUBE_DIAGONAL_D:
        row = cases[f"c_d{d}"]
        axial = power_law(cube_fit, row["b"])
        diagonal[f"c_d{d}"] = {
            "b": row["b"],
            "alpha": row["alpha"],
            "axis_fit": axial,
            "ratio": row["alpha"] / axial,
        }
    depth = {}
    for z in DEPTHS:
        shape = [mw.SLAB[0], mw.SLAB[1], z]
        star = (mw.SLAB_STAR[0], mw.SLAB_STAR[1], z // 2)
        points = []
        for b in mw.AXIS_B:
            steady, _ = steady_pass(shape, star, (0, b, 0))
            points.append((float(b), alpha_of(register_of(steady))))
        depth[str(z)] = {"alphas": dict((str(int(b)), a) for b, a in points), "fit": fit(points)}
        print("depth", z, depth[str(z)]["fit"], flush=True)
    free, iterations = free_space_pass(args.free_half_width)
    free_points = [(float(b), row["alpha"]) for b, row in free.items()]
    free_fits = {
        "4-16": fit([p for p in free_points if p[0] <= 16]),
        "8-32": fit([p for p in free_points if p[0] >= 8]),
        "local": {
            f"{free_points[i][0]:g}-{free_points[i + 1][0]:g}": mf.local_exponent(
                *free_points[i], *free_points[i + 1]
            )
            for i in range(len(free_points) - 1)
        },
    }
    print(
        "free space",
        {b: round(row["alpha"], 7) for b, row in free.items()},
        free_fits["4-16"],
        free_fits["8-32"],
        flush=True,
    )
    result = {
        "release_per_heading": RELEASE,
        "light": mw.LIGHT,
        "launch_delay": mw.LAUNCH_DELAY,
        "ticks": mw.LAUNCH_DELAY + mw.EXTRA_TICKS,
        "table": list(mw.SPREAD),
        "cases": cases,
        "axis_fit": fit(axis_points),
        "axis_steady_fit": fit(axis_steady),
        "cube_axis_fit": cube_fit,
        "diagonal": diagonal,
        "depth": depth,
        "free_space": {
            "half_width": args.free_half_width,
            "iterations": iterations,
            "alphas": {str(b): row for b, row in free.items()},
            "fits": free_fits,
        },
        "seconds": time.time() - started,
    }
    args.out.write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")
    print(
        "axis fit",
        result["axis_fit"],
        "steady",
        result["axis_steady_fit"],
        "cube",
        cube_fit,
        "diagonal",
        diagonal,
    )
    print("written", args.out, "in", round(time.time() - started), "s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
