"""Section 12c of DERIVATIONS_BEAM.md: the mover's counter under the
crossing count and the owed count (route C).

Host arithmetic on the derivation's own formulas and on registered
integers; no run of the engine. Every count below is a ratio to the rest
count of the same reader in the same crowd.

(A) The isotropic crowd at rest: the mean over the sphere of four
    per-direction counts of a reader moving at beta (its speed over c):
    the Euclidean sweep |n - beta| (a sphere reader sweeping point rows),
    the Manhattan sweep (a cube reader sweeping point rows), the Euclidean
    crossing count 1 - n . beta (fronts crossed) and the lattice's
    crossing rule 1 - sgn(n_e) beta / |n|_1 per step on the axis e
    (section 2.4's Manhattan flux, the limit of record 158's count).
(B) The same on the registered 290-direction fan of series E with the
    integer T_d, for a body stepping on x at 1 / 8 and 1 / 4 Link per
    self-creation.
(C) The co-moving pair's counts (section 12's exchange rates) and the two
    counters of a moving pair.
(D) The muon of J4: the bound on route C's lengthening of a lifetime.
(E) The pins: series E's +x axis probe thrown outward and inward.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

Q = 64
C = 32 / 55  # a row's pace on a heading, Links per interval (T_d = 110)
BETAS = (0.2148, 0.4297, 0.8594, 1.0)  # 1/8, 1/4, 1/2 Link per interval over c, and the cap


def isqrt3(d: tuple[int, int, int]) -> int:
    return math.isqrt(3 * (d[0] ** 2 + d[1] ** 2 + d[2] ** 2) * Q * Q)


def gauss_legendre(n: int) -> tuple[list[float], list[float]]:
    """Nodes and weights on [-1, 1] by Newton on the Legendre polynomial."""
    xs, ws = [], []
    for i in range(1, n + 1):
        x = math.cos(math.pi * (i - 0.25) / (n + 0.5))
        for _ in range(100):
            p0, p1 = 1.0, x
            for k in range(2, n + 1):
                p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
            dp = n * (x * p1 - p0) / (x * x - 1)
            dx = p1 / dp
            x -= dx
            if abs(dx) < 1e-15:
                break
        xs.append(x)
        ws.append(2 / ((1 - x * x) * dp * dp))
    return xs, ws


def sphere_grid(n_mu: int = 200, n_phi: int = 400) -> list[tuple[float, float, float, float]]:
    """(n_x, n_y, n_z, weight) with the weights summing to 1."""
    mus, ws = gauss_legendre(n_mu)
    grid = []
    for mu, w in zip(mus, ws, strict=True):
        s = math.sqrt(1 - mu * mu)
        for j in range(n_phi):
            phi = 2 * math.pi * (j + 0.5) / n_phi
            grid.append((mu, s * math.cos(phi), s * math.sin(phi), w / (2 * n_phi)))
    return grid


def l1(v: tuple[float, ...]) -> float:
    return sum(abs(c) for c in v)


def sphere_means(beta: float, v_dir: tuple[float, float, float]) -> dict[str, float]:
    """The four counts of a reader at velocity beta v_dir (|v_dir| = 1),
    each as a ratio to the rest count, averaged over an isotropic crowd."""
    grid = sphere_grid()
    bv = tuple(beta * c for c in v_dir)
    sweep_e = sweep_m = rest_m = rule_e = rule_m = 0.0
    fwd_rule_m = fwd_w = 0.0
    for nx, ny, nz, w in grid:
        n = (nx, ny, nz)
        sweep_e += w * math.sqrt(sum((a - b) ** 2 for a, b in zip(n, bv, strict=True)))
        sweep_m += w * sum(abs(a - b) for a, b in zip(n, bv, strict=True))
        rest_m += w * l1(n)
        rule_e += w * (1 - sum(a * b for a, b in zip(n, bv, strict=True)))
        # The lattice's rule: a body stepping on the axis e at v_e meets
        # the rows of direction n at 1 - sgn(n_e) v_e / c_1(n), with
        # c_1(n) = c |n|_1 the direction's Manhattan pace; the steps on
        # the axes are shared as |v_e| / |v|_1.
        f = 0.0
        for e in range(3):
            if bv[e] == 0:
                continue
            share = abs(bv[e]) / l1(bv)
            f += share * (1 - math.copysign(1, n[e] * bv[e]) * abs(bv[e]) / l1(n)) if n[e] else share
        rule_m += w * f
        if nx * bv[0] + ny * bv[1] + nz * bv[2] < 0:  # the rows coming toward the reader
            fwd_rule_m += w * f
            fwd_w += w
    return {
        "sweep_euclid": sweep_e,
        "sweep_manhattan": sweep_m / rest_m,
        "rule_euclid": rule_e,
        "rule_manhattan": rule_m,
        "rule_manhattan_toward_hemisphere": fwd_rule_m / fwd_w,
    }


def fan_means(directions: list[tuple[int, int, int]], v: float) -> dict[str, float]:
    """The crossing rule's factor on the registered fan for a body stepping
    on +x at v Links per self-creation: 1 - sgn(D_x) v T_d / (Q S_1)
    (section 2.4), and the cube sweep's on the same fan."""
    rule, sweep, rest = 0.0, 0.0, 0.0
    lo, hi = math.inf, -math.inf
    for d in directions:
        t = isqrt3(d)
        s1 = l1(d)
        f = 1 - (0 if d[0] == 0 else math.copysign(1, d[0]) * v * t / (Q * s1))
        rule += f
        lo, hi = min(lo, f), max(hi, f)
        pace = [c * Q / t for c in d]  # Links per interval per axis
        sweep += abs(pace[0] - v) + abs(pace[1]) + abs(pace[2])
        rest += sum(abs(p) for p in pace)
    n = len(directions)
    return {"rule": rule / n, "rule_min": lo, "rule_max": hi, "sweep": sweep / rest}


def main() -> None:
    out = []
    out.append("(A) The isotropic crowd at rest: the mover's count over the rest count, sphere means")
    out.append(
        "beta      dir     sweep_E   sweep_M   rule_E    rule_M    rule_M toward-hemisphere   1+beta^2/3"
    )
    for beta in BETAS:
        for name, vd in (
            ("x", (1, 0, 0)),
            ("xy", (1 / 2**0.5, 1 / 2**0.5, 0)),
            ("xyz", (1 / 3**0.5,) * 3),
        ):
            m = sphere_means(beta, vd)
            out.append(
                f"{beta:<9.4f} {name:<7} {m['sweep_euclid']:<9.4f} {m['sweep_manhattan']:<9.4f} "
                f"{m['rule_euclid']:<9.4f} {m['rule_manhattan']:<9.4f} "
                f"{m['rule_manhattan_toward_hemisphere']:<26.4f} {1 + beta * beta / 3:.4f}"
            )
    out.append("the sweep minus the rule, Euclidean, from the rows with |n_x| < beta: beta^2/3 x rest;")
    out.append("the rule's mean is 1 by the reflection n_e -> -n_e; the sweep's 1 + beta^2/3 on the")
    out.append("sphere or the cube alike (mean |n_x - beta| = (1 + beta^2) / 2, mean |n_x| = 1 / 2).")

    out.append("")
    out.append("(B) The registered fan (series E's 290 directions, integer T_d), a body stepping on +x")
    world = json.loads(
        (Path(__file__).resolve().parents[3] / "examples/events/redshift/scalar.json").read_text()
    )
    fan = [tuple(d) for d in world["measured"][0]["directions"]]
    assert len(fan) == 290
    for v, label in ((1 / 8, "1/8"), (1 / 4, "1/4"), (C, "c = 32/55 (the cap)")):
        m = fan_means(fan, v)
        out.append(
            f"v = {label}: rule mean {m['rule']:.6f} (min {m['rule_min']:.4f} on the co-moving heading,"
            f" max {m['rule_max']:.4f} head-on); cube sweep mean {m['sweep']:.4f}"
        )
    c1 = sorted({l1(d) * Q / isqrt3(d) for d in fan})
    out.append(
        f"the fan's Manhattan paces c_1 = S_1 Q / T_d from {c1[0]:.4f} (headings) to {c1[-1]:.4f}"
    )

    out.append("")
    out.append("(C) The co-moving pair (section 12's exchange rates as counts at the partner)")
    out.append(
        "beta     leading (1-b)^2  trailing (1+b)^2  mean   aberrated (1-b^2)^2  transverse 1-b^2"
    )
    for beta in BETAS[:3]:
        out.append(
            f"{beta:<8.4f} {(1 - beta) ** 2:<16.4f} {(1 + beta) ** 2:<17.4f} {1 + beta**2:<6.4f} "
            f"{(1 - beta**2) ** 2:<20.4f} {1 - beta**2:.4f}"
        )
    out.append("the counters of a pair at the partner's count k_p (n / d = 1): rate 1 / (1 + k_p f)")
    for beta in BETAS[:2]:
        for k in (1.0, 0.1):
            lead = 1 / (1 + k * (1 - beta) ** 2)
            trail = 1 / (1 + k * (1 + beta) ** 2)
            ab = 1 / (1 + k * (1 - beta**2) ** 2)
            rest = 1 / (1 + k)
            out.append(
                f"beta {beta:.4f}, k_p {k}: rest {rest:.4f}, leading {lead:.4f} ({lead / rest:.3f} x rest), "
                f"trailing {trail:.4f} ({trail / rest:.3f}), aberrated both {ab:.4f} ({ab / rest:.3f});"
                f" Lorentz 1 / gamma = {math.sqrt(1 - beta**2):.4f}"
            )

    out.append("")
    out.append(
        "(D) The muon of J4 (become at 64; v = 1/4 and 1/2 Link per interval = 0.43 c and 0.86 c)"
    )
    for beta in (0.4297, 0.8594):
        g = 1 / math.sqrt(1 - beta**2)
        out.append(
            f"beta {beta:.4f}: gamma {g:.3f}, lorentz-v1's tick {64 * g:.0f}; route C in J4's empty bar: 64;"
            f" in a crowd at k n / d = 1: rest 128, with the crowd's rows {64 * (1 + (1 - beta)):.0f},"
            f" against them {64 * (1 + (1 + beta)):.0f}; the isotropic mean 128"
        )
    out.append(
        "the bound: (1 + k (n/d) (1 + beta)) / (1 + k n/d) < 1 + beta <= 2 for every crowd and direction;"
        " nature's CERN muon 29.3"
    )

    out.append("")
    out.append("(E) The pins: series E's scalar world, the +x axis probe thrown along x under form B")
    S, M = 1, 1
    for v_target, label in ((1 / 8, "1/8"), (1 / 4, "1/4")):
        p = round(v_target * Q * Q * S * M / (Q - 110 * v_target))
        v = p * Q / (Q * Q * S * M + 110 * p)
        f = v * 110 / (Q * 1)
        out.append(
            f"v {label}: p = {p} label units, v = {v:.4f} Link per self-creation, v T_d / (Q S_1) = {f:.4f}"
        )
        for rest_k, where in (
            (2.03, "r = 6 .. 12 (the registered 2.03)"),
            (55 / 32, "the path mean 55/32"),
        ):
            for sense, sign in (("outward", -1), ("inward", +1)):
                k = rest_k * (1 + sign * f)
                out.append(
                    f"  {sense:<8} at {where}: count {k:.3f} of rest {rest_k:.3f}; "
                    f"self-creations per 1000 intervals {1000 / (1 + k):.0f} against {1000 / (1 + rest_k):.0f}"
                    f" at rest; the 10 Links r = 4 .. 14 in {round(10 / v * (1 + k)):d} intervals"
                    f" ({round(10 / v):d} self-creations) against {round(10 / v * (1 + rest_k)):d}"
                )
    Path(__file__).with_suffix(".out").write_text("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
