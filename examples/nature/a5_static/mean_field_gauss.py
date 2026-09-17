"""The split table's mean field at large distance: Gauss's law, the crossover and
the time to steady state.

A computation after experiment A5s (docs/EXPERIMENTS.md), not an engine run: the
catalog's table [6, 1, 1, 1, 1, 1] over 11 as the linear map it is on average
(the remainder rule of `field-remainder-v1` realizes the split exactly on average,
so the mean field is the expectation of the engine's integers), transported on
the cubic lattice in floating point. Per-heading amounts f[j, x, y, z] hold what
arrived at a Node on heading j this interval; every interval each heading's
content is split by the table relative to its heading (forward 6/11, backward
1/11, each transverse 1/11) and walks one Link; the source releases 4096 on each
heading every interval, arriving at its six neighbours; a sink absorbs everything
that arrives at its Node and books amount x heading (the push, as the engine's
`external_body_absorbed` records book it: the push of tick t is what walked into
the sink during tick t, so the first push at distance r is at tick r); the open
boundary absorbs what walks out. A mirrored face is a symmetry plane, so a box
with the source on it holds the whole field in a half, a quarter or an octant.

Four computations (`python examples/nature/a5_static/mean_field_gauss.py`):
(1) the free-space steady state of the source alone (an octant of a box with the
boundary 2r beyond the farthest r), the net flux and the density on the axis and
on the diagonal against Gauss's S / (4 pi r^2) and the Green's function of the
lattice Laplacian (the simple walk, the table [1, 1, 1, 1, 1, 1], in the same box);
(2) a point sink at distance r, the absorbed net momentum at steady state with the
boundary at least 2r from both bodies, the exponent over r >= 12 and over the run's
r = 4 to 16; (3) the time to 90 % of that steady state at each r; (4) the split of
each push into the unscattered beam 4096 x (6/11)^(r-1) and the rest. The steady
states are the fixed points of the linear map, solved by BiCGSTAB to a relative
residual of 1e-10; the transients are stepped. Nothing is drawn: the numbers are
deterministic, and IEEE-754 doubles reproduce the printed digits.
"""

from __future__ import annotations

import argparse
import json
import math
import time

import numpy as np

HEADINGS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
SPREAD = (6, 1, 1, 1, 1, 1)
SIMPLE_WALK = (1, 1, 1, 1, 1, 1)
RELEASE = 4096
RUN_DISTANCES = (4, 6, 8, 12, 16)
SINK_DISTANCES = (4, 6, 8, 12, 16, 24, 32)


def table_weights(table) -> tuple[float, float, float, float]:
    """(forward, backward, transverse, total) of a six-entry table in Port order
    relative to the arriving heading; the four transverse weights must be equal."""
    forward, backward, *transverse = table
    if len(transverse) != 4 or len(set(transverse)) != 1:
        raise ValueError("the table needs four equal transverse weights")
    return float(forward), float(backward), float(transverse[0]), float(sum(table))


def persistence(table) -> float:
    """The cosine of the heading after one step of the table's walk."""
    forward, backward, _, total = table_weights(table)
    return (forward - backward) / total


PERSISTENCE_COSINE = persistence(SPREAD)


def diffusion(table) -> float:
    """D of the persistent walk of the table, Links^2 per interval: the cosine of
    the heading after one step is c = (forward - backward) / total, and
    D = (1 + c) / (6 (1 - c)) (the discrete Green-Kubo sum in three dimensions)."""
    c = persistence(table)
    return (1 + c) / (6 * (1 - c))


def beam(r: int, table=SPREAD, release: float = RELEASE) -> float:
    """The unscattered forward share arriving at distance r on the axis."""
    forward, _, _, total = table_weights(table)
    return release * (forward / total) ** (r - 1)


def spread(f: np.ndarray, table=SPREAD, out: np.ndarray | None = None) -> np.ndarray:
    """The departures per heading of the arrivals f (shape (6, ...)): the table applied
    to every heading's content relative to that heading and summed per Port. For Port
    j the forward share of f[j], the backward share of f[reverse j] and the transverse
    share of the other four, which with equal transverse weights is
    (forward - transverse) f[j] + (backward - transverse) f[rev j] + transverse x total."""
    forward, backward, transverse, total = table_weights(table)
    if out is None:
        out = np.empty_like(f)
    everything = f.sum(axis=0)
    for j in range(6):
        np.multiply(f[j], (forward - transverse) / total, out=out[j])
        if backward != transverse:
            out[j] += f[j ^ 1] * ((backward - transverse) / total)
        out[j] += everything * (transverse / total)
    return out


class Board:
    """A box of the mean field. `shape` is the stored box; `mirror[axis]` makes the
    low face of that axis a symmetry plane (index 0 on the plane); every other face is
    open. `source` is the releasing Node, `sinks` the absorbing Nodes (the source is
    one of them in every world of A5s: a body takes whatever arrives)."""

    def __init__(self, shape, mirror, source, sinks, release=RELEASE, table=SPREAD):
        self.shape = tuple(int(n) for n in shape)
        self.mirror = tuple(bool(m) for m in mirror)
        self.source = tuple(int(c) for c in source)
        self.sinks = [tuple(int(c) for c in s) for s in sinks]
        self.release = float(release)
        self.table = tuple(table)
        self._g = np.empty((6, *self.shape))
        self._out = np.empty((6, *self.shape))
        # The release lands on each neighbour on the heading toward it; a neighbour
        # behind a mirror plane is the image of the one in front of it.
        self.source_nodes = []
        for j, h in enumerate(HEADINGS):
            node = tuple(c + d for c, d in zip(self.source, h, strict=True))
            if any(node[a] < 0 and self.mirror[a] for a in range(3)):
                continue
            if any(node[a] < 0 or node[a] >= self.shape[a] for a in range(3)):
                continue
            self.source_nodes.append((j, node))

    def empty(self) -> np.ndarray:
        return np.zeros((6, *self.shape))

    def walk(self, g: np.ndarray, out: np.ndarray) -> np.ndarray:
        """Every heading's departures walk one Link; an open face loses what walks
        out, a mirrored face receives the image of what walks toward it."""
        for axis in range(3):
            jp, jm = 2 * axis, 2 * axis + 1
            plus, minus = out[jp], out[jm]
            lo = [slice(None)] * 3
            hi = [slice(None)] * 3
            lo[axis] = slice(None, -1)
            hi[axis] = slice(1, None)
            plus[tuple(hi)] = g[jp][tuple(lo)]
            minus[tuple(lo)] = g[jm][tuple(hi)]
            face0 = [slice(None)] * 3
            face0[axis] = 0
            face1 = [slice(None)] * 3
            face1[axis] = 1
            last = [slice(None)] * 3
            last[axis] = -1
            if self.mirror[axis]:
                # Arriving on +axis at the plane: the image of what left index 1 on -axis.
                plus[tuple(face0)] = g[jm][tuple(face1)]
            else:
                plus[tuple(face0)] = 0.0
            minus[tuple(last)] = 0.0
        return out

    def transport(self, f: np.ndarray, out: np.ndarray | None = None) -> np.ndarray:
        """The spread and the walk of the content f left on the board after this
        interval's absorptions: what arrives in the next interval, less the release."""
        if out is None:
            out = np.empty_like(f)
        return self.walk(spread(f, self.table, self._g), out)

    def arrivals(self, f: np.ndarray, out: np.ndarray | None = None) -> np.ndarray:
        """The transport plus the release: everything that arrives in the next interval."""
        out = self.transport(f, out)
        for j, node in self.source_nodes:
            out[(j, *node)] += self.release
        return out

    def push(self, f: np.ndarray, sink) -> np.ndarray:
        """amount x heading summed over the arrivals at the sink."""
        p = np.zeros(3)
        for j, h in enumerate(HEADINGS):
            p += f[(j, *sink)] * np.array(h, dtype=float)
        return p

    def absorb(self, f: np.ndarray) -> None:
        for sink in self.sinks:
            f[(slice(None), *sink)] = 0.0

    def step(self, f: np.ndarray) -> tuple[np.ndarray, list[np.ndarray]]:
        """One interval in place: the arrivals, the pushes read at the sinks, the
        absorptions. Returns f and the pushes in the order of `sinks`."""
        nxt = self.arrivals(f, self._out)
        pushes = [self.push(nxt, sink) for sink in self.sinks]
        self.absorb(nxt)
        f[...] = nxt
        return f, pushes

    def steady_state(self, tol: float = 1e-10, max_iter: int = 5000) -> tuple[np.ndarray, int]:
        """The fixed point f = Z (T f + s) of the interval (Z the absorptions, T the
        transport, s the release), solved as (I - Z T) f = Z s by BiCGSTAB; f is the
        content left after the absorptions, `arrivals(f)` what arrives next."""
        rhs = self.empty()
        for j, node in self.source_nodes:
            rhs[(j, *node)] = self.release
        self.absorb(rhs)

        def matvec(v):
            w = self.transport(v, np.empty_like(v))
            self.absorb(w)
            return v - w

        return bicgstab(matvec, rhs, tol, max_iter)

    def outflow(self, f: np.ndarray, r: int) -> float:
        """The net content per interval leaving the cube of half-width r about the
        source through its six faces (the Link flux, summed), for an octant board."""
        if self.mirror != (True, True, True) or self.source != (0, 0, 0):
            raise ValueError("the outflow is read on an octant board")
        g = spread(f, self.table)
        y = np.arange(r + 1)
        multiplicity = np.where(y > 0, 2.0, 1.0)
        weight = multiplicity[:, None] * multiplicity[None, :]
        face = g[0, r, : r + 1, : r + 1] - g[1, r + 1, : r + 1, : r + 1]
        return 6.0 * float((face * weight).sum())


def bicgstab(matvec, b, tol, max_iter):
    """Van der Vorst's BiCGSTAB, no preconditioner."""
    x = np.zeros_like(b)
    r = b.copy()
    # The shadow residual: not b itself, which is orthogonal to the residual after one
    # iteration here (the release's entries receive nothing but the source's own
    # departures, which its sink absorbs), but a fixed pseudo-random vector, the
    # same on every run.
    r0 = np.random.default_rng(0).standard_normal(b.shape)
    bnorm = float(np.sqrt(np.vdot(r, r).real))
    if bnorm == 0.0:
        return x, 0
    rho_old = alpha = omega = 1.0
    v = np.zeros_like(b)
    p = np.zeros_like(b)
    for k in range(1, max_iter + 1):
        rho = float(np.vdot(r0, r).real)
        if rho == 0.0:
            raise RuntimeError("BiCGSTAB breakdown (rho = 0)")
        beta_k = (rho / rho_old) * (alpha / omega)
        p = r + beta_k * (p - omega * v)
        v = matvec(p)
        alpha = rho / float(np.vdot(r0, v).real)
        s = r - alpha * v
        if float(np.sqrt(np.vdot(s, s).real)) / bnorm < tol:
            x += alpha * p
            return x, k
        t = matvec(s)
        omega = float(np.vdot(t, s).real) / float(np.vdot(t, t).real)
        x += alpha * p + omega * s
        r = s - omega * t
        if float(np.sqrt(np.vdot(r, r).real)) / bnorm < tol:
            return x, k
        rho_old = rho
    raise RuntimeError(f"BiCGSTAB did not converge in {max_iter} iterations")


def fit_exponent(points):
    """Log-log least squares: the exponent and its standard error (the fit of
    analyze.py); the error is nan for two points."""
    xs = [math.log(r) for r, _ in points]
    ys = [math.log(v) for _, v in points]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys, strict=True))
    slope = sxy / sxx
    intercept = my - slope * mx
    if n > 2:
        residual = sum((y - (intercept + slope * x)) ** 2 for x, y in zip(xs, ys, strict=True))
        error = math.sqrt(residual / (n - 2) / sxx)
    else:
        error = float("nan")
    return slope, error


def local_exponent(r1, v1, r2, v2) -> float:
    return math.log(v2 / v1) / math.log(r2 / r1)


def diffusion_t90(r: float, d: float, fraction: float = 0.9) -> float:
    """The continuum: a source switched on at t = 0 in three dimensions has the
    flux J(r, t) = J_inf erfc(z) + J_inf (2 z / sqrt(pi)) exp(-z^2), z = r / sqrt(4 D t);
    the first t at which J reaches the fraction is r^2 / (4 D z^2) with z from it."""

    def reached(z):
        return math.erfc(z) + 2 * z / math.sqrt(math.pi) * math.exp(-z * z)

    lo, hi = 0.0, 5.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if reached(mid) > fraction:
            lo = mid
        else:
            hi = mid
    z = (lo + hi) / 2
    return r * r / (4 * d * z * z)


# ---------------------------------------------------------------- (1) free space


def free_space(half_width: int, table=SPREAD, tol: float = 1e-10) -> dict:
    """The source alone at the corner of an octant of the cube of half-width L:
    the steady state, the effective source (the release less what returns to the
    source's own sink), the exact outflow through cubes, and the net flux and the
    density on the axis and on the diagonal."""
    board = Board((half_width + 1,) * 3, (True,) * 3, (0, 0, 0), [(0, 0, 0)], table=table)
    started = time.time()
    f, iterations = board.steady_state(tol)
    arrivals = board.arrivals(f)
    departures = spread(f, table)
    released = 6 * board.release
    returned = float(arrivals[(slice(None), 0, 0, 0)].sum())
    effective = released - returned

    def current(node, axis_index):
        """The Link current along one axis at a Node: the mean over its two Links of
        the departures toward the Node's far side less the departures back."""
        jp, jm = 2 * axis_index, 2 * axis_index + 1
        before = list(node)
        before[axis_index] -= 1
        after = list(node)
        after[axis_index] += 1
        into = departures[(jp, *before)] - departures[(jm, *node)]
        out_of = departures[(jp, *node)] - departures[(jm, *after)]
        return float(into + out_of) / 2

    axis = {}
    for r in range(1, half_width):
        column = arrivals[(slice(None), r, 0, 0)]
        axis[r] = {
            "flux": float(column[0] - column[1]),
            "current": current((r, 0, 0), 0),
            "density": float(column.sum()),
        }
    diagonal = {}
    for d in range(1, half_width):
        column = arrivals[(slice(None), d, d, 0)]
        jx, jy = float(column[0] - column[1]), float(column[2] - column[3])
        diagonal[d] = {
            "flux": math.hypot(jx, jy),
            "current": math.hypot(current((d, d, 0), 0), current((d, d, 0), 1)),
            "density": float(column.sum()),
        }
    body = {}
    for d in range(1, half_width):
        column = arrivals[(slice(None), d, d, d)]
        jx = float(column[0] - column[1])
        body[d] = {
            "flux": math.sqrt(3.0) * jx,
            "current": math.sqrt(3.0) * current((d, d, d), 0),
            "density": float(column.sum()),
        }
    outflow = {r: board.outflow(f, r) for r in (2, 4, 8, 16, 32, 48, 64) if r + 1 < half_width}
    return {
        "half_width": half_width,
        "table": list(table),
        "iterations": iterations,
        "seconds": time.time() - started,
        "released": released,
        "returned": returned,
        "effective": effective,
        "axis": axis,
        "diagonal": diagonal,
        "body_diagonal": body,
        "outflow": outflow,
    }


def gauss(effective: float, r: float) -> float:
    return effective / (4 * math.pi * r * r)


def report_free_space(free: dict, simple: dict, run_distances=RUN_DISTANCES) -> dict:
    """The tables of (1) and the exponent windows; returns the summary the JSON keeps."""
    half = free["half_width"]
    far = half // 2
    effective = free["effective"]
    # The density of the simple walk in the same box, scaled to the split table's
    # source and diffusion constant: n / (D_simple / D x S / S_simple x n_simple) -> 1.
    scale = (diffusion(tuple(simple["table"])) / diffusion(tuple(free["table"]))) * (
        effective / simple["effective"]
    )
    print(f"\n== (1) free space: the source alone, octant of the cube of half-width {half}")
    print(
        f"   release {free['released']:.0f} per interval, {free['returned']:.2f} returns to the"
        f" source's sink, effective source S = {effective:.2f}; BiCGSTAB {free['iterations']}"
        f" iterations, {free['seconds']:.0f} s; the simple walk in the same box:"
        f" S = {simple['effective']:.2f}, {simple['iterations']} iterations, {simple['seconds']:.0f} s"
    )
    print("   Gauss exact on the lattice: the outflow through the cube of half-width r over S")
    print("   " + "  ".join(f"r={r}: {v / effective:.9f}" for r, v in free["outflow"].items()))
    c = PERSISTENCE_COSINE
    print(
        "\n   axis: J the net momentum arriving at the Node (amount x heading of the arrivals,"
        " what a sink\n   absorbs), Phi the Link current through the Node (the mean of its two"
        " Links), Gauss S/(4 pi r^2),\n   the beam 4096 (6/11)^(r-1), the rest J - beam over"
        " Gauss, the density n over the simple walk's\n   scaled by D_simple / D = 3/8 (the"
        " lattice Laplacian's Green's function), and the local exponent of J;\n   the arrivals"
        " sample the two neighbours' departures across the gradient, so J -> Phi x 2 / (1 + c)"
        f" = {2 / (1 + c):.4f}\n   for the table's persistence cosine c = {c:.4f} (2 for the"
        " simple walk)"
    )
    print(
        f"   {'r':>3} {'J':>10} {'J/Gauss':>8} {'Phi/Gauss':>9} {'J/Phi':>6} {'beam':>9}"
        f" {'beam/J':>7} {'rest/Gauss':>10} {'n':>10} {'n/(3/8 n_simple)':>16} {'exponent':>9}"
    )
    axis_rows = []
    for r in range(1, far + 1):
        j = free["axis"][r]["flux"]
        n = free["axis"][r]["density"]
        b = beam(r, tuple(free["table"]))
        g = gauss(effective, r)
        n_simple = simple["axis"][r]["density"] * scale
        expo = local_exponent(r, j, r + 1, free["axis"][r + 1]["flux"]) if r < far else float("nan")
        phi = free["axis"][r]["current"]
        axis_rows.append(
            {
                "r": r,
                "flux": j,
                "current": phi,
                "gauss": g,
                "beam": b,
                "rest": j - b,
                "density": n,
                "density_over_simple": n / n_simple,
                "local_exponent": expo,
            }
        )
        print(
            f"   {r:>3} {j:>10.4f} {j / g:>8.4f} {phi / g:>9.4f} {j / phi:>6.3f} {b:>9.4f}"
            f" {b / j:>7.4f} {(j - b) / g:>10.4f} {n:>10.2f} {n / n_simple:>16.4f} {expo:>9.3f}"
        )
    print("\n   windows of the axis flux, log-log least squares (exponent +- standard error):")
    windows = []
    for r0 in (2, 3, 4, 6, 8, 12, 16, 24):
        r1 = 2 * r0
        if r1 > far:
            break
        points = [(r, free["axis"][r]["flux"]) for r in range(r0, r1 + 1)]
        slope, error = fit_exponent(points)
        rest = [(r, free["axis"][r]["flux"] - beam(r)) for r in range(r0, r1 + 1)]
        # The rest is negative next to the source (the backscatter returning to it).
        slope_rest, error_rest = (
            fit_exponent(rest) if all(v > 0 for _, v in rest) else (float("nan"), float("nan"))
        )
        windows.append(
            {"from": r0, "to": r1, "exponent": slope, "error": error, "rest_exponent": slope_rest}
        )
        print(
            f"   r = {r0:>2} .. {r1:>2}: {slope:>7.3f} +- {error:.3f}   the rest alone"
            f" {slope_rest:>7.3f} +- {error_rest:.3f}"
        )
    run_points = [(r, free["axis"][r]["flux"]) for r in run_distances if r <= far]
    run_slope, run_error = fit_exponent(run_points)
    print(f"   the run's r = {list(run_distances)}: {run_slope:.3f} +- {run_error:.3f}")
    crossover = next((r for r in range(1, far) if free["axis"][r]["flux"] > 2 * beam(r)), None)
    exponents = [row["local_exponent"] for row in axis_rows if not math.isnan(row["local_exponent"])]
    within = {}
    for band in (0.2, 0.1):
        inside = [abs(e + 2) <= band for e in exponents]
        # The first r from which every local exponent to the last read stays in the band.
        start = len(inside)
        while start > 0 and inside[start - 1]:
            start -= 1
        within[band] = axis_rows[start]["r"] if start < len(inside) else None
    print(
        f"   crossover: the scattered part exceeds the beam from r = {crossover}; the local"
        f" exponent stays within -2.0 +- 0.2 from r = {within[0.2]} on and within +- 0.1 from"
        f" r = {within[0.1]} on (read to r = {far})"
    )
    diagonal_rows = {}
    for key, name, stretch in (
        ("diagonal", "the diagonal (d, d, 0), Euclidean r = d sqrt 2", math.sqrt(2)),
        ("body_diagonal", "the body diagonal (d, d, d), Euclidean r = d sqrt 3", math.sqrt(3)),
    ):
        reach = int(half / (1 + 2 * stretch))
        print(f"\n   {name}; the boundary at least 2r away for d <= {reach}")
        print(
            f"   {'d':>3} {'r':>6} {'|J|':>10} {'|J|/Gauss':>9} {'|Phi|/Gauss':>11} {'J/Phi':>6}"
            f" {'n':>10} {'n/(3/8 n_simple)':>16}"
        )
        diagonal_rows[key] = []
        for d in (2, 3, 4, 6, 8, 12, 16, 24, 32):
            if d > reach:
                break
            r = d * stretch
            j = free[key][d]["flux"]
            phi = free[key][d]["current"]
            n = free[key][d]["density"]
            n_simple = simple[key][d]["density"] * scale
            g = gauss(effective, r)
            diagonal_rows[key].append(
                {"d": d, "flux": j, "current": phi, "gauss": g, "density_over_simple": n / n_simple}
            )
            print(
                f"   {d:>3} {r:>6.2f} {j:>10.4f} {j / g:>9.4f} {phi / g:>11.4f} {j / phi:>6.3f}"
                f" {n:>10.2f} {n / n_simple:>16.4f}"
            )
    return {
        "half_width": half,
        "effective": effective,
        "returned": free["returned"],
        "outflow_over_effective": {r: v / effective for r, v in free["outflow"].items()},
        "axis": axis_rows,
        "windows": windows,
        "run_window": {"exponent": run_slope, "error": run_error},
        "crossover": crossover,
        "within_band_from": {str(k): v for k, v in within.items()},
        "diagonal": diagonal_rows["diagonal"],
        "body_diagonal": diagonal_rows["body_diagonal"],
    }


# --------------------------------------------------------------------- (2) sink


def sink_board(r: int, boundary: int, table=SPREAD) -> Board:
    """The source at the origin and the sink at (r, 0, 0), the open boundary at
    `boundary` Links from both (the cube [-b, r + b] x [-b, b]^2), stored as a quarter
    by the y and z mirrors."""
    shape = (2 * boundary + r + 1, boundary + 1, boundary + 1)
    sinks = [(boundary, 0, 0), (boundary + r, 0, 0)]
    return Board(shape, (False, True, True), (boundary, 0, 0), sinks, table=table)


def sink_steady(r: int, boundary: int, tol: float = 1e-10) -> dict:
    board = sink_board(r, boundary)
    started = time.time()
    f, iterations = board.steady_state(tol)
    arrivals = board.arrivals(f)
    push = board.push(arrivals, board.sinks[1])
    return {
        "r": r,
        "boundary": boundary,
        "shape": board.shape,
        "push": float(push[0]),
        "iterations": iterations,
        "seconds": time.time() - started,
    }


def sink_transient(r: int, boundary: int, steady: float, cap: int) -> dict:
    """Step the sink world from the empty board: the first ticks at which the push on
    the sink reaches 50, 90 and 99 % of its steady state (None when not within the
    cap), and the push at the run's 2r + 32 and the plan's 2r + 64 ticks."""
    board = sink_board(r, boundary)
    f = board.empty()
    reached = {0.5: None, 0.9: None, 0.99: None}
    marks = {2 * r + 32: "run", 2 * r + 64: "plan"}
    at = {}
    started = time.time()
    t = 0
    for t in range(1, cap + 1):
        f, pushes = board.step(f)
        push = float(pushes[1][0])
        for fraction in reached:
            if reached[fraction] is None and push >= fraction * steady:
                reached[fraction] = t
        if t in marks:
            at[marks[t]] = push
        if reached[0.99] is not None and t >= max(marks):
            break
    return {
        "r": r,
        "t50": reached[0.5],
        "t90": reached[0.9],
        "t99": reached[0.99],
        "ticks": t,
        "run_push": at.get("run"),
        "plan_push": at.get("plan"),
        "seconds": time.time() - started,
    }


def report_sinks(distances, boundary_factor, box_checks, cap_factor, free_axis) -> dict:
    """The tables of (2), (3) and (4); returns the summary the JSON keeps."""
    rs = list(distances)
    print(f"\n== (2) the point sink at distance r, the boundary {boundary_factor}r from both bodies")
    steadies = {r: sink_steady(r, boundary_factor * r) for r in rs}
    checks = {(r, factor): sink_steady(r, factor * r) for r, factor in box_checks}
    free_flux = {row["r"]: row["flux"] for row in free_axis}
    print(
        "   F the net momentum absorbed per interval at steady state, the beam"
        " 4096 (6/11)^(r-1), the rest\n   F - beam, J_free the net flux through the same Node"
        " with no sink there (table (1)), the local exponent"
    )
    print(
        f"   {'r':>3} {'box':>14} {'F':>10} {'beam':>9} {'beam/F':>7} {'F-beam':>9}"
        f" {'(F-beam) r^2':>12} {'F/J_free':>8} {'exponent':>9} {'iters':>5} {'s':>4}"
    )
    rows = []
    for i, r in enumerate(rs):
        s = steadies[r]
        b = beam(r)
        expo = (
            local_exponent(r, s["push"], rs[i + 1], steadies[rs[i + 1]]["push"])
            if i + 1 < len(rs)
            else float("nan")
        )
        j = free_flux.get(r)
        rows.append(
            {
                "r": r,
                "push": s["push"],
                "beam": b,
                "rest": s["push"] - b,
                "over_free_flux": (s["push"] / j) if j else None,
                "local_exponent": expo,
            }
        )
        print(
            f"   {r:>3} {str(s['shape']):>14} {s['push']:>10.4f} {b:>9.4f} {b / s['push']:>7.4f}"
            f" {s['push'] - b:>9.4f} {(s['push'] - b) * r * r:>12.1f}"
            f" {(s['push'] / j if j else float('nan')):>8.4f} {expo:>9.3f} {s['iterations']:>5}"
            f" {s['seconds']:>4.0f}"
        )
    print("   the box: the steady push with the boundary farther out, the same r")
    for (r, factor), s in checks.items():
        base = steadies[r]["push"] if r in steadies else None
        rel = f"{100 * (s['push'] / base - 1):+.3f} % against {boundary_factor}r" if base else ""
        print(f"   r = {r:>2}, boundary {factor}r, box {s['shape']}: F = {s['push']:.4f}  {rel}")
    fits = {}
    for label, subset in (
        ("r >= 12", [r for r in rs if r >= 12]),
        ("r >= 16", [r for r in rs if r >= 16]),
        ("the run's 4..16", [r for r in rs if r in RUN_DISTANCES]),
    ):
        if len(subset) >= 2:
            slope, error = fit_exponent([(r, steadies[r]["push"]) for r in subset])
            rest_points = [(r, steadies[r]["push"] - beam(r)) for r in subset]
            rest = (
                fit_exponent(rest_points)
                if all(v > 0 for _, v in rest_points)
                else (float("nan"), float("nan"))
            )
            fits[label] = {"exponent": slope, "error": error, "rest_exponent": rest[0]}
            print(
                f"   fit over {label}: {slope:.3f} +- {error:.3f} (the rest alone"
                f" {rest[0]:.3f} +- {rest[1]:.3f})"
            )
    print(f"\n== (3) the transient in the same boxes, stepped to at most {cap_factor} r^2 + 64 ticks")
    print(
        "   t50, t90, t99 the first tick at which the push reaches that fraction of the"
        " box's steady state;\n   'diffusion' the continuum's t90 for D = 4/9; F at the run's"
        " 2r + 32 and the plan's 2r + 64 ticks"
    )
    print(
        f"   {'r':>3} {'F_steady':>10} {'t50':>5} {'t90':>5} {'t99':>6} {'t90/r^2':>7}"
        f" {'diffusion':>9} {'F(2r+32)':>9} {'%':>5} {'F(2r+64)':>9} {'%':>5} {'ticks':>5} {'s':>4}"
    )
    transients = {}
    for r in rs:
        cap = cap_factor * r * r + 64
        tr = sink_transient(r, boundary_factor * r, steadies[r]["push"], cap)
        transients[r] = tr
        steady = steadies[r]["push"]
        t90 = tr["t90"]
        plan = tr["plan_push"] if tr["plan_push"] is not None else float("nan")
        print(
            f"   {r:>3} {steady:>10.4f} {tr['t50'] or '-':>5} {t90 or '-':>5} {tr['t99'] or '-':>6}"
            f" {(t90 / r / r if t90 else float('nan')):>7.3f}"
            f" {diffusion_t90(r, diffusion(SPREAD)):>9.1f}"
            f" {tr['run_push']:>9.3f} {100 * tr['run_push'] / steady:>5.1f}"
            f" {plan:>9.3f} {100 * plan / steady:>5.1f} {tr['ticks']:>5} {tr['seconds']:>4.0f}"
        )
    scalings = {}
    for label, subset in (("all r", rs), ("r >= 12", [r for r in rs if r >= 12])):
        points = [(r, transients[r]["t90"]) for r in subset if transients[r]["t90"]]
        if len(points) >= 2:
            slope, error = fit_exponent(points)
            scalings[label] = {"exponent": slope, "error": error}
            print(f"   t90 over {label}: t90 ~ r^k with k = {slope:.3f} +- {error:.3f}")
    coefficient = diffusion_t90(1, diffusion(SPREAD))
    print(f"   the continuum's t90 = {coefficient:.3f} r^2 with D = {diffusion(SPREAD):.4f}")
    return {
        "boundary_factor": boundary_factor,
        "rows": rows,
        "box_checks": [
            {"r": r, "factor": factor, "push": s["push"], "shape": list(s["shape"])}
            for (r, factor), s in checks.items()
        ],
        "fits": fits,
        "transients": [transients[r] for r in rs],
        "t90_scaling": scalings,
        "diffusion_t90_coefficient": coefficient,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--free-half-width", type=int, default=96, help="octant half-width L")
    parser.add_argument(
        "--free-check", type=int, default=64, help="a second half-width for the box dependence"
    )
    parser.add_argument("--sink", type=int, nargs="*", default=list(SINK_DISTANCES))
    parser.add_argument("--boundary", type=int, default=2, help="boundary at this multiple of r")
    parser.add_argument("--cap", type=int, default=3, help="step the transient to cap r^2 + 64")
    parser.add_argument("--only-free", action="store_true", help="computation (1) alone")
    parser.add_argument("--out", help="write the tables as JSON")
    args = parser.parse_args(argv)
    started = time.process_time()
    wall = time.time()
    print(f"table {list(SPREAD)} over {sum(SPREAD)}, D = {diffusion(SPREAD):.4f} Links^2 per interval")
    free = free_space(args.free_half_width)
    simple = free_space(args.free_half_width, table=SIMPLE_WALK)
    summary = {"free": report_free_space(free, simple)}
    if args.free_check and args.free_check < args.free_half_width:
        check = free_space(args.free_check)
        ratios = {
            r: check["axis"][r]["flux"] / free["axis"][r]["flux"]
            for r in (4, 8, 16, 24, 32)
            if r <= args.free_check // 2
        }
        print(
            f"\n   the box: the axis flux at half-width {args.free_check} over half-width"
            f" {args.free_half_width}: " + "  ".join(f"r={r}: {v:.4f}" for r, v in ratios.items())
        )
        summary["free_box"] = ratios
    if not args.only_free:
        box_checks = [(r, factor) for r in (8, 12, 16) for factor in (3, 4) if r in args.sink]
        summary["sink"] = report_sinks(
            args.sink, args.boundary, box_checks, args.cap, summary["free"]["axis"]
        )
    cpu = time.process_time() - started
    print(f"\nCPU {cpu:.0f} s, wall {time.time() - wall:.0f} s")
    summary["cpu_seconds"] = cpu
    if args.out:
        with open(args.out, "w", encoding="utf-8") as handle:
            json.dump(summary, handle, indent=1)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
