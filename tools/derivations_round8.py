"""Scratch computations for DERIVATIONS.md round 8 (the law of the shadow).

An iteration of the stated rules on paper, not an engine run: the mixing S = J/3 - I
(Highlights 5.4 point 24) on a cubic board, a held content that emits q units per interval
(R12) and absorbs and re-releases every unit that reaches its Node (R13, section 46 (viii)),
in the mean field (complex amplitudes), with the held content moving one Link every k
intervals along +x. The board's faces carry a sponge (a smooth damping of the amplitudes over
the outer `sponge` layers) so that what is measured at the source is the source's own near
field and not the edge's 7 % mirror (section 46 (i)). Subcommands:

  selfpush   one held content moving at v = 1/k: the amount and the momentum it absorbs of its
             own field per interval, against the emission weights (1 + alpha v e_p . x) per Port
             (--k, --alpha, --period, --ticks, --L, --W)
  pair       two held contents A (ahead) and B (behind) at separation d on the x axis, both
             moving at v = 1/k, two fields (two numbers): the momentum each absorbs of the
             other's field per interval, and their sum (--d, --k, --alpha, --theta, ...);
             --theta is a phase lead theta v on the +x Port of every release (and a lag on -x),
             0 for the law as written
  scan       selfpush over k in (0, 8, 4, 2) and alpha in a list, one table

Every number quoted in DERIVATIONS.md sections 52 to 54 comes from these subcommands with
the arguments named there. Requires numpy; 10 to 60 s per run.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from derivations_round7 import mix, walk  # noqa: E402

DIRS = np.array([[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]])


def sponge_mask(shape, width):
    """A smooth damping factor per Node: 1 inside, falling toward the faces over `width` layers."""
    m = np.ones(shape)
    for ax, L in enumerate(shape):
        idx = np.arange(L)
        d = np.minimum(idx, L - 1 - idx)
        f = np.ones(L)
        inside = d < width
        f[inside] = 1.0 - 0.6 * ((width - d[inside]) / width) ** 2
        sh = [1, 1, 1]
        sh[ax] = L
        m = m * f.reshape(sh)
    return m


PORT_X = np.array([1.0, -1.0, 0.0, 0.0, 0.0, 0.0])


def release(amount, weights, phase, lead=0.0):
    """Six Port amplitudes releasing `amount`, shared by `weights` (sum 1), at the holder's
    phase, the +x Port leading and the -x Port lagging by `lead` radians (a phase gradient
    along the motion; 0 for the law as written)."""
    return np.sqrt(amount * weights) * phase * np.exp(1j * lead * PORT_X)


def emission_weights(alpha, v):
    w = np.ones(6)
    w[0] = 1.0 + alpha * v
    w[1] = 1.0 - alpha * v
    w = np.maximum(w, 0.0)
    return w / w.sum()


def absorbed(A, pos):
    """The amount and the x-momentum (amount x heading) of the six arrivals at a Node."""
    a = np.abs(A[:, pos[0], pos[1], pos[2]]) ** 2
    amount = float(a.sum())
    mom = float(sum(a[p] * (-DIRS[p][0]) for p in range(6)))
    return amount, mom, a


def run_selfpush(L, W, k, alpha, period, q, ticks, sponge, measure, theta=0.0):
    """One held content moving +x one Link every k intervals (k = 0: at rest)."""
    shape = (L, W, W)
    A = np.zeros((6,) + shape, dtype=np.complex128)
    mask = sponge_mask(shape, sponge)
    v = 0.0 if k == 0 else 1.0 / k
    weights = emission_weights(alpha, v)
    lead = theta * v
    x0, cy = sponge + 4, W // 2
    hist = []
    t0 = time.time()
    for t in range(ticks):
        xs = x0 + (t // k if k else 0)
        if xs >= L - sponge - 2:
            raise SystemExit("board too short for the run")
        B, u = mix(A)
        home, mom, ports = absorbed(A, (xs, cy, cy))
        phase = np.exp(2j * np.pi * t / period) if period > 0 else 1.0
        B[:, xs, cy, cy] = release(home + q, weights, phase, lead)
        A, _ = walk(B, periodic=False)
        A *= mask
        hist.append((home, mom, ports))
    last = hist[-measure:]
    home_m = float(np.mean([h for h, _, _ in last]))
    mom_m = float(np.mean([m for _, m, _ in last]))
    ports_m = np.mean([p for _, _, p in last], axis=0)
    out = dict(
        L=L,
        W=W,
        k=k,
        v=v,
        alpha=alpha,
        theta=theta,
        period=period,
        q=q,
        ticks=ticks,
        measure=measure,
        home_over_q=home_m / q,
        absorbed_momentum_x_over_q=mom_m / q,
        ports_over_q={
            n: float(ports_m[i]) / q for i, n in enumerate(("+x", "-x", "+y", "-y", "+z", "-z"))
        },
        seconds=round(time.time() - t0, 1),
    )
    if v > 0:
        out["c1_momentum_over_v_home"] = mom_m / (v * home_m)
        out["momentum_over_v_q"] = mom_m / (v * q)
    # the drift of the window mean: first and second half of the measured window
    h1 = float(np.mean([m for _, m, _ in last[: measure // 2]]))
    h2 = float(np.mean([m for _, m, _ in last[measure // 2 :]]))
    out["momentum_halves_over_q"] = [h1 / q, h2 / q]
    return out


def run_pair(L, W, d, k, alpha, period, q, ticks, sponge, measure, theta=0.0):
    """Two held contents, A ahead at x_A and B behind at x_A - d, both moving +x at v = 1/k.
    Two fields (numbers). Each Node absorbs both fields; its own is recycled (R13) and the other's
    is re-released with its own number (S2.3, S2.4), so the absorbed cross amount joins its release."""
    shape = (L, W, W)
    FA = np.zeros((6,) + shape, dtype=np.complex128)
    FB = np.zeros((6,) + shape, dtype=np.complex128)
    mask = sponge_mask(shape, sponge)
    v = 0.0 if k == 0 else 1.0 / k
    weights = emission_weights(alpha, v)
    lead = theta * v
    xb0, cy = sponge + 4, W // 2
    hist = []
    t0 = time.time()
    for t in range(ticks):
        xb = xb0 + (t // k if k else 0)
        xa = xb + d
        if xa >= L - sponge - 2:
            raise SystemExit("board too short for the run")
        pa, pb = (xa, cy, cy), (xb, cy, cy)
        BA, _ = mix(FA)
        BB, _ = mix(FB)
        hA, _, _ = absorbed(FA, pa)  # A's own field at A: recycled
        hB, _, _ = absorbed(FB, pb)  # B's own field at B: recycled
        cAB, mAB, _ = absorbed(FB, pa)  # B's field absorbed at A: the push on A
        cBA, mBA, _ = absorbed(FA, pb)  # A's field absorbed at B: the push on B
        phase = np.exp(2j * np.pi * t / period) if period > 0 else 1.0
        # A releases its own number: q + home + what it absorbed of B (re-released as A's)
        BA[:, xa, cy, cy] = release(q + hA + cAB, weights, phase, lead)
        BB[:, xa, cy, cy] = 0.0  # B's field is absorbed at A, nothing of it leaves A
        BB[:, xb, cy, cy] = release(q + hB + cBA, weights, phase, lead)
        BA[:, xb, cy, cy] = 0.0
        FA, _ = walk(BA, periodic=False)
        FB, _ = walk(BB, periodic=False)
        FA *= mask
        FB *= mask
        hist.append((hA, hB, cAB, cBA, mAB, mBA))
    last = np.array(hist[-measure:])
    m = last.mean(axis=0)
    J = q / (4 * np.pi * d * d)
    out = dict(
        L=L,
        W=W,
        d=d,
        k=k,
        v=v,
        alpha=alpha,
        theta=theta,
        period=period,
        q=q,
        ticks=ticks,
        measure=measure,
        home_A_over_q=m[0] / q,
        home_B_over_q=m[1] / q,
        cross_amount_at_A_over_q=m[2] / q,
        cross_amount_at_B_over_q=m[3] / q,
        cross_momentum_at_A_over_J=m[4] / J,
        cross_momentum_at_B_over_J=m[5] / J,
        pair_sum_over_J=(m[4] + m[5]) / J,
        J_over_q=J / q,
        count_law_over_q=0.1378 / (d * d),
        seconds=round(time.time() - t0, 1),
    )
    if v > 0:
        out["pair_sum_over_v_J"] = (m[4] + m[5]) / (v * J)
    h1 = last[: measure // 2].mean(axis=0)
    h2 = last[measure // 2 :].mean(axis=0)
    out["pair_sum_halves_over_J"] = [float((h1[4] + h1[5]) / J), float((h2[4] + h2[5]) / J)]
    return out


def cmd_selfpush(args):
    print(
        json.dumps(
            run_selfpush(
                args.L,
                args.W,
                args.k,
                args.alpha,
                args.period,
                args.q,
                args.ticks,
                args.sponge,
                args.measure,
                args.theta,
            ),
            indent=1,
        )
    )


def cmd_pair(args):
    print(
        json.dumps(
            run_pair(
                args.L,
                args.W,
                args.d,
                args.k,
                args.alpha,
                args.period,
                args.q,
                args.ticks,
                args.sponge,
                args.measure,
                args.theta,
            ),
            indent=1,
        )
    )


def cmd_scan(args):
    rows = []
    for k in args.ks:
        for alpha in args.alphas:
            r = run_selfpush(
                args.L,
                args.W,
                k,
                alpha,
                args.period,
                args.q,
                args.ticks,
                args.sponge,
                args.measure,
                args.theta,
            )
            rows.append(
                dict(
                    k=k,
                    v=r["v"],
                    alpha=alpha,
                    home_over_q=round(r["home_over_q"], 4),
                    mom_over_q=round(r["absorbed_momentum_x_over_q"], 5),
                    c1=round(r.get("c1_momentum_over_v_home", 0.0), 4),
                    halves=[round(x, 5) for x in r["momentum_halves_over_q"]],
                    s=r["seconds"],
                )
            )
            print(json.dumps(rows[-1]), flush=True)
            if k == 0:
                break
    print(json.dumps(rows, indent=1))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("selfpush", "pair", "scan"):
        a = sub.add_parser(name)
        a.add_argument("--L", type=int, default=129)
        a.add_argument("--W", type=int, default=41)
        a.add_argument("--k", type=int, default=4)
        a.add_argument("--alpha", type=float, default=0.0)
        a.add_argument("--theta", type=float, default=0.0)
        a.add_argument("--period", type=int, default=16)
        a.add_argument("--q", type=float, default=6.0)
        a.add_argument("--ticks", type=int, default=400)
        a.add_argument("--sponge", type=int, default=8)
        a.add_argument("--measure", type=int, default=128)
        if name == "pair":
            a.add_argument("--d", type=int, default=4)
        if name == "scan":
            a.add_argument("--ks", type=int, nargs="+", default=[0, 8, 4, 2])
            a.add_argument("--alphas", type=float, nargs="+", default=[0.0])
    args = ap.parse_args()
    {"selfpush": cmd_selfpush, "pair": cmd_pair, "scan": cmd_scan}[args.cmd](args)


if __name__ == "__main__":
    main()
