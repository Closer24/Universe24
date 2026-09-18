"""Anisotropy of the split table's mean field on six link sets of Z^3.

A computation (2026-09-18), not an engine run, made to settle the question of the
board's link set (docs/EXPERIMENTS.md, section F). The kernel follows
examples/nature/a5_static/mean_field_gauss.py: the source alone at the corner of an
octant of a cube of half-width L, the three low faces mirror planes, the high faces
open, the source's own Node a sink, the steady state the fixed point of the linear
map solved by BiCGSTAB. It is generalized to any set of link vectors on Z^3, one hop
per interval on every link (the pace a longer link would carry is not applied: the
steady flows do not depend on it, only the resident density would scale per heading).

Link sets: cubic6 (today), corners8, edges12, fc14 (faces + corners), fe18 (faces +
edges), all26. Two walks per set: `simple`, every arrival shared over all headings by
the set's isotropic weights (faces 8 and corners 1 on fc14, faces 2 and edges 1 on fe18, faces 16, edges 4 and corners 1 on all26: the weights that cancel the
fourth-order term on the two-shell sets; uniform on a single shell), and `persistent`,
today's forward share 6/11 kept on the continuation of the arriving heading and the
other 5/11 shared over the other headings by the same weights (on cubic6 this is
exactly [6, 1, 1, 1, 1, 1] over 11). The source releases 24576 per interval in total,
split over its headings by the same weights (4096 per heading on cubic6).

Read: the density n (arrivals summed over headings) and the net momentum J (arrivals
times unit heading) along six lines through the source, interpolated in r to common
radii, and the spread between the lines, max / min - 1.
"""

from __future__ import annotations

import argparse
import itertools
import json
import time

import numpy as np

TOTAL_RELEASE = 6 * 4096.0
FORWARD = 6.0 / 11.0
LINES = {
    "axis (1,0,0)": (1, 0, 0),
    "face diagonal (1,1,0)": (1, 1, 0),
    "body diagonal (1,1,1)": (1, 1, 1),
    "oblique (2,1,0)": (2, 1, 0),
    "oblique (2,1,1)": (2, 1, 1),
    "oblique (3,2,1)": (3, 2, 1),
}
RADII = (4, 6, 8, 12, 16, 24)


def link_set(name: str):
    by_class = {1: [], 2: [], 3: []}
    for v in itertools.product((-1, 0, 1), repeat=3):
        k = sum(abs(c) for c in v)
        if k:
            by_class[k].append(v)
    faces, edges, corners = by_class[1], by_class[2], by_class[3]
    sets = {
        "cubic6": (faces, {1: 1.0}),
        "corners8": (corners, {3: 1.0}),
        "edges12": (edges, {2: 1.0}),
        "fc14": (faces + corners, {1: 8.0, 3: 1.0}),
        "fe18": (faces + edges, {1: 2.0, 2: 1.0}),
        "all26": (faces + edges + corners, {1: 16.0, 2: 4.0, 3: 1.0}),
    }
    links, weight_of = sets[name]
    weights = np.array([weight_of[sum(abs(c) for c in v)] for v in links], dtype=float)
    return [tuple(v) for v in links], weights


class Lattice:
    def __init__(self, name: str, walk: str, half_width: int):
        self.name, self.walk, self.L = name, walk, int(half_width)
        self.links, self.weights = link_set(name)
        self.H = len(self.links)
        index = {v: i for i, v in enumerate(self.links)}
        self.reverse = np.array([index[tuple(-c for c in v)] for v in self.links])
        self.reflect = []
        for axis in range(3):
            perm = []
            for v in self.links:
                w = list(v)
                w[axis] = -w[axis]
                perm.append(index[tuple(w)])
            self.reflect.append(np.array(perm))
        self.unit = np.array(self.links, dtype=float)
        self.unit /= np.linalg.norm(self.unit, axis=1)[:, None]
        self.W = float(self.weights.sum())
        self.release = TOTAL_RELEASE * self.weights / self.W
        n = self.L + 1
        self.shape = (n, n, n)
        # The release lands on the neighbour in the box; images are the symmetric state.
        self.source_nodes = []
        for j, v in enumerate(self.links):
            if all(c >= 0 for c in v):
                self.source_nodes.append((j, v))
        self._g = np.empty((self.H, *self.shape))
        self._out = np.empty((self.H, *self.shape))

    # -- the split ---------------------------------------------------------------
    def spread(self, f: np.ndarray, out: np.ndarray) -> np.ndarray:
        w = self.weights
        if self.walk == "simple":
            everything = f.sum(axis=0)
            for j in range(self.H):
                np.multiply(everything, w[j] / self.W, out=out[j])
            return out
        # persistent: F on the continuation, (1 - F) w_out / (W - w_in) elsewhere
        inv = 1.0 / (self.W - w)
        shared = np.tensordot(inv, f, axes=(0, 0))  # sum_in f_in / (W - w_in)
        for j in range(self.H):
            np.multiply(f[j], FORWARD - (1 - FORWARD) * w[j] * inv[j], out=out[j])
            out[j] += shared * ((1 - FORWARD) * w[j])
        return out

    # -- the walk ----------------------------------------------------------------
    def walk_links(self, g: np.ndarray, out: np.ndarray) -> np.ndarray:
        """Departures g walk one link. Low faces are mirrors: a ghost layer at index
        -1 holds index 1 of the reflected heading (applied axis by axis so a ghost
        corner is the double reflection); high faces are open (nothing comes in)."""
        padded = g
        for axis in range(3):
            ghost = np.take(padded, self.reflect[axis], axis=0)
            sl = [slice(None)] * 4
            sl[axis + 1] = slice(1, 2)
            ghost = ghost[tuple(sl)]
            padded = np.concatenate([ghost, padded], axis=axis + 1)
        n = self.L + 1
        out[...] = 0.0
        for j, v in enumerate(self.links):
            dst = [j]
            src = [j]
            for c in v:
                if c == 1:
                    dst.append(slice(0, n))
                    src.append(slice(0, n))
                elif c == -1:
                    dst.append(slice(0, n - 1))
                    src.append(slice(2, n + 1))
                else:
                    dst.append(slice(0, n))
                    src.append(slice(1, n + 1))
            out[tuple(dst)] = padded[tuple(src)]
        return out

    def transport(self, f: np.ndarray, out: np.ndarray) -> np.ndarray:
        return self.walk_links(self.spread(f, self._g), out)

    def arrivals(self, f: np.ndarray) -> np.ndarray:
        out = self.transport(f, np.empty_like(f))
        for j, v in self.source_nodes:
            out[(j, *v)] += self.release[j]
        return out

    def absorb(self, f: np.ndarray) -> None:
        f[(slice(None), 0, 0, 0)] = 0.0

    def steady_state(self, tol=1e-10, max_iter=5000):
        rhs = np.zeros((self.H, *self.shape))
        for j, v in self.source_nodes:
            rhs[(j, *v)] = self.release[j]

        def matvec(x):
            w = self.transport(x, np.empty_like(x))
            self.absorb(w)
            return x - w

        return bicgstab(matvec, rhs, tol, max_iter)


def bicgstab(matvec, b, tol, max_iter):
    x = np.zeros_like(b)
    r = b.copy()
    r0 = np.random.default_rng(0).standard_normal(b.shape)
    bnorm = float(np.sqrt(np.vdot(r, r).real))
    rho_old = alpha = omega = 1.0
    v = np.zeros_like(b)
    p = np.zeros_like(b)
    for k in range(1, max_iter + 1):
        rho = float(np.vdot(r0, r).real)
        if rho == 0.0:
            raise RuntimeError("BiCGSTAB breakdown")
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


def interpolate(points, R):
    """Linear interpolation in r of the values at the line's nodes; None outside."""
    pts = [(r, v) for r, v in points if v is not None]
    for (r1, v1), (r2, v2) in zip(pts, pts[1:], strict=False):
        if r1 <= R <= r2:
            return v1 + (v2 - v1) * (R - r1) / (r2 - r1)
    return None


def run(name: str, walk: str, L: int, tol: float) -> dict:
    lat = Lattice(name, walk, L)
    started = time.time()
    f, iterations = lat.steady_state(tol)
    arrivals = lat.arrivals(f)
    returned = float(arrivals[(slice(None), 0, 0, 0)].sum())
    effective = TOTAL_RELEASE - returned
    # The check: f is the fixed point f = Z(T f + s), the arrivals less the absorption.
    g = arrivals.copy()
    lat.absorb(g)
    residual = float(np.abs(g - f).max() / max(1.0, np.abs(f).max()))
    density = arrivals.sum(axis=0)
    J = np.tensordot(lat.unit, arrivals, axes=(0, 0))  # (3, x, y, z)
    Jmag = np.sqrt((J * J).sum(axis=0))
    lines = {}
    for label, d in LINES.items():
        dv = np.array(d, dtype=float)
        norm = float(np.linalg.norm(dv))
        kmax = int(L / (max(d) + 2 * norm))
        is_link = tuple(d) in {tuple(int(c) for c in v) for v in lat.links}
        j_link = None
        if is_link:
            j_link = lat.links.index(tuple(d))
        rows = []
        for k in range(1, kmax + 1):
            node = tuple(k * c for c in d)
            r = k * norm
            n_here = float(density[node])
            if n_here <= 0.0:
                rows.append({"k": k, "r": r, "n": None, "J": None, "n_rest": None, "J_rest": None})
                continue
            jm = float(Jmag[node])
            beam = 0.0
            if is_link and walk == "persistent":
                beam = float(lat.release[j_link]) * FORWARD ** (k - 1)
            rows.append(
                {"k": k, "r": r, "n": n_here, "J": jm, "n_rest": n_here - beam, "J_rest": jm - beam}
            )
        lines[label] = rows
    summary = {}
    for R in RADII:
        entry = {}
        for key, power in (("n", 1), ("J", 2), ("n_rest", 1), ("J_rest", 2)):
            values = {}
            for label, rows in lines.items():
                pts = [
                    (row["r"], row[key] * row["r"] ** power if row[key] is not None else None)
                    for row in rows
                ]
                val = interpolate(pts, R)
                if val is not None:
                    values[label] = val
            if len(values) >= 2:
                vmax, vmin = max(values.values()), min(values.values())
                entry[key] = {
                    "spread": vmax / vmin - 1.0 if vmin > 0 else None,
                    "over_axis": {
                        lab: (v / values["axis (1,0,0)"] if "axis (1,0,0)" in values else None)
                        for lab, v in values.items()
                    },
                }
        summary[R] = entry
    return {
        "lattice": name,
        "walk": walk,
        "half_width": L,
        "headings": lat.H,
        "iterations": iterations,
        "seconds": time.time() - started,
        "released": TOTAL_RELEASE,
        "returned": returned,
        "effective": effective,
        "fixed_point_residual": residual,
        "lines": lines,
        "summary": summary,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--lattices", nargs="*", default=["cubic6", "corners8", "edges12", "fc14", "fe18", "all26"]
    )
    parser.add_argument("--walks", nargs="*", default=["simple", "persistent"])
    parser.add_argument("--half-width", type=int, default=48)
    parser.add_argument("--tol", type=float, default=1e-10)
    parser.add_argument("--out")
    args = parser.parse_args(argv)
    results = []
    for name in args.lattices:
        for walk in args.walks:
            res = run(name, walk, args.half_width, args.tol)
            results.append(res)
            print(
                f"\n== {name} ({res['headings']} headings), {walk} walk, L = {args.half_width}:"
                f" S = {res['effective']:.2f} (returned {res['returned']:.2f}),"
                f" BiCGSTAB {res['iterations']} it, {res['seconds']:.0f} s,"
                f" residual {res['fixed_point_residual']:.1e}"
            )
            print(
                "   axis: "
                + "  ".join(
                    f"r={row['k']}: n={row['n']:.2f} J={row['J']:.3f}"
                    for row in res["lines"]["axis (1,0,0)"]
                    if row["n"] is not None and row["k"] in (4, 6, 8, 12, 16, 24)
                )
            )
            for key in ("n", "J", "n_rest", "J_rest"):
                if walk == "simple" and key.endswith("rest"):
                    continue
                print(
                    f"   {key:>6}: spread max/min-1 at r = "
                    + "  ".join(
                        f"{R}: {100 * res['summary'][R][key]['spread']:.1f}%"
                        for R in RADII
                        if key in res["summary"][R] and res["summary"][R][key]["spread"] is not None
                    )
                )
    if args.out:
        with open(args.out, "w", encoding="utf-8") as handle:
            json.dump(results, handle, indent=1)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
