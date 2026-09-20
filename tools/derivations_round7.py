"""Scratch computations for DERIVATIONS.md round 7 (a thing emits; the open-GameBoard fixed point).

An iteration of the stated rules on paper, not an engine run: the mixing S = J/3 - I of
Highlights 5.4 point 24 on a cubic GameBoard with a thing at the centre that emits q quanta per
interval (R12), absorbs and re-releases what comes home (R13) and an edge through which
shares escape (R14), in the mean field (complex amplitudes) and in whole quanta (the
per-Port remainders and the phase circle of N steps). Subcommands:

  meanfield  the fixed point, the transient, the shell means and E11's Nodes (--L, --period,
             --variant recycle|absorb|rerelease|soft, --q, --ticks, --periodic)
  integer    the same in whole quanta (--variant recycle|absorb|mirror, --N)
  edge       the reflection coefficient of the open edge for a plane wave (a slab)
  home       the fraction of a released pulse absorbed at a Node at distance d
  walk       a lone quantum under the largest-remainder rule (a rotor walk)
  transit    the mean distance to a face of the cube over directions

Every number quoted in DERIVATIONS.md sections 45 to 50 comes from these subcommands with
the arguments named there. Requires numpy; seconds to a minute per run.
"""

from __future__ import annotations

import argparse
import json
import time

import numpy as np

DIRS = np.array([[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]])
AX = [0, 0, 1, 1, 2, 2]
SGN = [1, -1, 1, -1, 1, -1]


def walk(B, periodic):
    """A_new[p](x) = B[p^1](x + e_p). Returns A_new and the amount that escaped (open)."""
    A = np.empty_like(B)
    escaped = 0.0
    for p in range(6):
        src = B[p ^ 1]
        ax, s = AX[p], SGN[p]
        rolled = np.roll(src, -s, axis=ax)
        if not periodic:
            idx = [slice(None)] * 3
            idx[ax] = -1 if s == 1 else 0
            rolled[tuple(idx)] = 0.0
            # what the face cells sent outward through Port p escapes
            fidx = [slice(None)] * 3
            fidx[ax] = -1 if s == 1 else 0
            escaped += float(np.sum(np.abs(B[p][tuple(fidx)]) ** 2))
        A[p] = rolled
    return A, escaped


def mix(A):
    u = A.sum(axis=0) / 3.0
    return u[None] - A, u


def readings(A, c):
    """count n, common part u, signed flux J (3 components) per Node."""
    amt = np.abs(A) ** 2
    n = amt.sum(axis=0)
    u = A.sum(axis=0) / 3.0
    J = np.zeros((3,) + n.shape)
    for p in range(6):
        # arrival through Port p came from x + e_p, heading -e_p
        J[AX[p]] -= SGN[p] * amt[p]
    return n, u, J


def cube_flux(B, c, h):
    """Net Link current outward through the surface of the cube |x_i - c| <= h."""
    L = B.shape[1]
    lo, hi = c - h, c + h
    total = 0.0
    for ax in range(3):
        for s, face, pout, pin in ((1, hi, 2 * ax, 2 * ax + 1), (-1, lo, 2 * ax + 1, 2 * ax)):
            sl_in = [slice(lo, hi + 1)] * 3
            sl_in[ax] = face
            sl_out = [slice(lo, hi + 1)] * 3
            out_face = face + s
            if out_face < 0 or out_face >= L:
                total += float(np.sum(np.abs(B[pout][tuple(sl_in)]) ** 2))
                continue
            sl_out[ax] = out_face
            total += float(
                np.sum(np.abs(B[pout][tuple(sl_in)]) ** 2) - np.sum(np.abs(B[pin][tuple(sl_out)]) ** 2)
            )
    return total


def cube_flux_int(leave, c, h):
    L = leave.shape[1]
    lo, hi = c - h, c + h
    total = 0
    for ax in range(3):
        for s, face, pout, pin in ((1, hi, 2 * ax, 2 * ax + 1), (-1, lo, 2 * ax + 1, 2 * ax)):
            sl_in = [slice(lo, hi + 1)] * 3
            sl_in[ax] = face
            out_face = face + s
            total += int(leave[pout][tuple(sl_in)].sum())
            if 0 <= out_face < L:
                sl_out = [slice(lo, hi + 1)] * 3
                sl_out[ax] = out_face
                total -= int(leave[pin][tuple(sl_out)].sum())
    return total


def radial(J, c, L):
    g = np.indices((L, L, L)) - c
    r = np.sqrt((g**2).sum(axis=0))
    rs = np.where(r == 0, 1.0, r)
    return (J * g).sum(axis=0) / rs, r


NODES = {
    "axis_r4": (4, 0, 0),
    "axis_r8": (8, 0, 0),
    "axis_r12": (12, 0, 0),
    "axis_r16": (16, 0, 0),
    "110_m3": (3, 3, 0),
    "110_m6": (6, 6, 0),
    "110_m9": (9, 9, 0),
    "111_m2": (2, 2, 2),
    "111_m5": (5, 5, 5),
    "111_m7": (7, 7, 7),
}


def run_meanfield(L, periodic, period, variant, q, ticks):
    c = L // 2
    A = np.zeros((6, L, L, L), dtype=np.complex128)
    a0 = np.sqrt(q / 6.0)
    per = max(period, 1)
    # accumulators for period means
    acc_n = None
    acc_J = None
    acc_u2 = None
    acc_absu = None
    acc_cnt = 0
    snapshots = {}  # period-mean count and J_r, per period index
    escaped_hist = []
    home_hist = []
    game_board_hist = []
    flux_hist = []
    flat_hist = []
    for t in range(ticks):
        B, u = mix(A)
        home = float(np.sum(np.abs(A[:, c, c, c]) ** 2))
        phase = np.exp(2j * np.pi * t / period) if period > 0 else 1.0
        if variant == "absorb":
            B[:, c, c, c] = a0 * phase
        elif variant == "recycle":
            # home is absorbed and released again with the thing: joins the emission, six-fold, at the thing's phase
            B[:, c, c, c] = np.sqrt((home + q) / 6.0) * phase
        elif variant == "rerelease":
            arr = A[:, c, c, c]
            amt = np.abs(arr) ** 2 + q / 6.0
            ph = np.angle(arr + a0 * phase)
            B[:, c, c, c] = np.sqrt(amt) * np.exp(1j * ph)
            home = 0.0
        elif variant == "soft":
            B[:, c, c, c] = B[:, c, c, c] + a0 * phase
            home = 0.0
        else:
            raise ValueError(variant)
        cubes = [h for h in (2, 4, 8, 12, 15, 19) if h <= c - 1]
        fl = [cube_flux(B, c, h) for h in cubes]
        A, esc = walk(B, periodic)
        n, uu, J = readings(A, c)
        Jr, r = radial(J, c, L)
        game_board = float(n.sum())
        flat_hist.append(game_board - 3.0 * float(np.sum(np.abs(uu) ** 2)))
        escaped_hist.append(esc)
        home_hist.append(home)
        game_board_hist.append(game_board)
        flux_hist.append(fl)
        if acc_n is None:
            acc_n = np.zeros_like(n)
            acc_J = np.zeros_like(Jr)
            acc_u2 = np.zeros_like(n)
            acc_absu = np.zeros_like(n)
        acc_n += n
        acc_J += Jr
        acc_u2 += np.abs(uu) ** 2
        acc_absu += np.abs(uu)
        acc_cnt += 1
        if acc_cnt == per:
            snapshots[t + 1] = (acc_n / per, acc_J / per, acc_u2 / per, acc_absu / per)
            acc_n = np.zeros_like(n)
            acc_J = np.zeros_like(Jr)
            acc_u2 = np.zeros_like(n)
            acc_absu = np.zeros_like(n)
            acc_cnt = 0
    return dict(
        L=L,
        c=c,
        r=r,
        snapshots=snapshots,
        escaped=escaped_hist,
        home=home_hist,
        game_board=game_board_hist,
        flux=flux_hist,
        q=q,
        period=period,
        variant=variant,
        periodic=periodic,
        flat=flat_hist,
    )


def report_meanfield(res):
    L, c, r, q = res["L"], res["c"], res["r"], res["q"]
    snaps = res["snapshots"]
    keys = sorted(snaps)
    tf = keys[-1]
    n_f, J_f, u2_f, au_f = snaps[tf]
    out = {}
    out["config"] = dict(
        L=L, periodic=res["periodic"], period=res["period"], variant=res["variant"], q=q, ticks=tf
    )
    out["final_game_board_over_q"] = res["game_board"][-1] / q
    out["final_escaped_over_q"] = float(np.mean(res["escaped"][-16:])) / q
    out["final_home_over_q"] = float(np.mean(res["home"][-16:])) / q
    cubes = [h for h in (2, 4, 8, 12, 15, 19) if h <= c - 1]
    out["flux_over_q_last"] = [
        float(np.mean([f[i] for f in res["flux"][-16:]])) / q for i in range(len(cubes))
    ]
    out["flux_cubes"] = cubes
    out["flux_over_q_samples"] = {
        t: [round(v / q, 4) for v in res["flux"][t - 1]]
        for t in (16, 32, 48, 64, 96, 128, 192, 256, 320, 400, 480)
        if t <= len(res["flux"])
    }
    per_node = {}
    for name, (x, y, z) in NODES.items():
        if max(abs(x), abs(y), abs(z)) > c - 1:
            continue
        i, j, k = c + x, c + y, c + z
        rr = float(r[i, j, k])
        nn = float(n_f[i, j, k])
        jj = float(J_f[i, j, k])
        uu2 = float(u2_f[i, j, k])
        au = float(au_f[i, j, k])
        per_node[name] = dict(
            r=round(rr, 2),
            n=nn,
            Jr=jj,
            absu=au,
            wave_fraction=3 * uu2 / nn if nn else None,
            n_r2_over_q=nn * rr * rr / q,
            Jr_4pir2_over_q=jj * 4 * np.pi * rr * rr / q,
            absu_r_over_sqrtq=au * rr / np.sqrt(q),
        )
    out["nodes"] = per_node
    # shells in L2 radius bins
    shells = {}
    for R in (2, 4, 6, 8, 10, 12, 14, 16, 18, 20):
        m = np.abs(r - R) < 0.5
        if m.sum() == 0:
            continue
        shells[R] = dict(
            nodes=int(m.sum()),
            n=float(n_f[m].mean()),
            Jr=float(J_f[m].mean()),
            absu=float(au_f[m].mean()),
            Jr_4pir2_over_q=float(J_f[m].mean()) * 4 * np.pi * R * R / q,
            n_r2_over_q=float(n_f[m].mean()) * R * R / q,
            absu_r_over_sqrtq=float(au_f[m].mean()) * R / np.sqrt(q),
        )
    out["shells"] = shells
    # settling: first period end after which the period-mean count within R stays within 1 % (and 5 %) of final
    settle = {}
    for R in (4, 8, 12, 16):
        m = (r <= R) & (r > 0)
        if m.sum() == 0 or R > c - 1:
            continue
        for tol in (0.05, 0.01):
            ok_from = None
            for t in keys:
                nn = snaps[t][0][m]
                dev = np.max(np.abs(nn - n_f[m]) / np.maximum(n_f[m], 1e-12))
                if dev <= tol:
                    if ok_from is None:
                        ok_from = t
                else:
                    ok_from = None
            settle[f"R{R}_tol{tol}"] = ok_from
        # J settling within R (relative to the mean |J| in the shell)
        ok_from = None
        for t in keys:
            jj = snaps[t][1][m]
            dev = np.max(np.abs(jj - J_f[m])) / np.mean(np.abs(J_f[m]))
            if dev <= 0.05:
                if ok_from is None:
                    ok_from = t
            else:
                ok_from = None
        settle[f"R{R}_J_tol0.05"] = ok_from
    out["settle"] = settle
    # GameBoard total history samples
    TS = (
        8,
        16,
        32,
        48,
        64,
        96,
        128,
        192,
        256,
        320,
        400,
        512,
        640,
        800,
        1000,
        1200,
        1600,
        2000,
        2400,
        3000,
    )
    out["game_board_over_q_samples"] = {
        t: res["game_board"][t - 1] / q for t in TS if t <= len(res["game_board"])
    }
    out["flat_over_q_samples"] = {t: res["flat"][t - 1] / q for t in TS if t <= len(res["flat"])}
    out["home_over_q_samples"] = {t: res["home"][t - 1] / q for t in TS if t <= len(res["home"])}
    # path sums along lines parallel to x at impact parameter b (y = b, z = 0), x over the GameBoard
    S = q * out["flux_over_q_last"][2] if len(out["flux_over_q_last"]) > 2 else q
    paths = {}
    H = c
    for b in (3, 4, 5, 6, 8, 10, 12):
        if b > c - 1:
            continue
        line_u = au_f[:, c + b, c]
        # transverse push: J_y at (x, b, 0): from the period-mean J we only kept J_r; recompute J_perp from J_r * (b / r)
        rr = r[:, c + b, c]
        line_Jperp = J_f[:, c + b, c] * b / rr
        su = float(line_u.sum())
        sj = float(line_Jperp.sum())
        pred_u = 0.2143 * np.sqrt(S) * 2 * np.arcsinh(H / b)
        pred_j = (S / (4 * np.pi)) * (2 / b) * (H / np.sqrt(b * b + H * H))
        paths[b] = dict(
            sum_absu=su,
            pred_absu=float(pred_u),
            ratio_u=su / pred_u,
            sum_Jperp=sj,
            pred_Jperp=float(pred_j),
            ratio_j=sj / pred_j,
        )
    out["paths"] = paths
    out["S_over_q_used"] = S / q
    out["escaped_over_q_samples"] = {
        t: res["escaped"][t - 1] / q for t in TS if t <= len(res["escaped"])
    }
    return out


def cmd_meanfield(args):
    t0 = time.time()
    res = run_meanfield(args.L, args.periodic, args.period, args.variant, args.q, args.ticks)
    out = report_meanfield(res)
    out["seconds"] = round(time.time() - t0, 1)
    print(json.dumps(out, indent=1, default=float))


def cmd_edge(args):
    """Reflection of the open edge: a slab periodic in y, z, a plane source at x = 2, the open edge at x = L-1.
    Fit the +x and -x moving Port amplitudes' time-harmonic components in the interior."""
    L, T = args.L, args.ticks
    period = args.period
    A = np.zeros((6, L, 4, 4), dtype=np.complex128)
    om = 2 * np.pi / period
    rec = []
    for t in range(T):
        B, u = mix(A)
        # a plane source: force the +x Port of the source plane x = 2 (toward +x) with unit amplitude and absorb what returns
        B[0, 2] = np.exp(-1j * om * t)
        B[1, 2] = 0.0
        # left edge at x = 0 absorbing too (open)
        A, esc = walk(B, periodic=False)
        # periodic transverse: re-wrap y,z
        for p in (2, 3, 4, 5):
            src = B[p ^ 1]
            A[p] = np.roll(src, -SGN[p], axis=AX[p])
        if t >= T - 4 * period:
            rec.append(A[:, :, 0, 0].copy())
    rec = np.array(rec)  # time, port, x
    # time-harmonic component at om
    tt = np.arange(rec.shape[0])
    ph = np.exp(1j * om * tt)[:, None, None]
    H = (rec * ph).mean(axis=0)  # port, x
    ux = H.sum(axis=0) / 3.0
    k = np.arccos(3 * np.cos(om) - 2)
    xs = np.arange(L)
    inner = slice(8, L - 3)
    M = np.stack([np.exp(1j * k * xs[inner]), np.exp(-1j * k * xs[inner])], axis=1)
    coef, *_ = np.linalg.lstsq(M, ux[inner], rcond=None)
    resid = np.abs(M @ coef - ux[inner]).max() / np.abs(ux[inner]).max()
    R = abs(coef[1] / coef[0])
    print(
        json.dumps(
            dict(
                L=L,
                period=period,
                k=float(k),
                u_forward=float(abs(coef[0])),
                u_backward=float(abs(coef[1])),
                R_amplitude=float(R),
                R_amount=float(R * R),
                fit_residual=float(resid),
                candidate_sqrt3=float((np.sqrt(3) - 1) / (np.sqrt(3) + 1)),
            ),
            indent=1,
        )
    )


def cmd_home(args):
    """A pulse released at (d,0,0) (six Ports in one phase, amount 1) with an absorbing Node at the origin
    (B = 0 there; the arrivals booked). Open GameBoard. Fraction absorbed at the origin by tick T."""
    L = args.L
    c = L // 2
    out = {}
    for d in (2, 4, 8, 12):
        for kind in ("six", "one"):
            A = np.zeros((6, L, L, L), dtype=np.complex128)
            if kind == "six":
                A[:, c + d, c, c] = np.sqrt(1 / 6.0)
            else:
                A[1, c + d, c, c] = (
                    1.0  # a lone share heading -x (toward the origin), arrived through Port +x
                )
            absorbed = 0.0
            esc_total = 0.0
            series = {}
            for t in range(args.ticks):
                B, u = mix(A)
                absorbed += float(np.sum(np.abs(A[:, c, c, c]) ** 2)) if t > 0 else 0.0
                B[:, c, c, c] = 0.0
                A, esc = walk(B, periodic=False)
                esc_total += esc
                if t + 1 in (20, 40, 80, 160, 300):
                    series[t + 1] = absorbed
            out[f"d{d}_{kind}"] = dict(
                absorbed=absorbed,
                escaped=esc_total,
                on_game_board=float(np.sum(np.abs(A) ** 2)),
                series=series,
                geometric_1_over_4pid2=1 / (4 * np.pi * d * d),
            )
    print(json.dumps(out, indent=1))


def run_integer(L, periodic, period, q, ticks, N=64, m=None, K=None, rerelease=True, variant=None):
    """The integer form: whole quanta per Port, phases on the circle of N, per-Port remainders."""
    c = L // 2
    amt = np.zeros((6, L, L, L), dtype=np.int64)
    ph = np.zeros((6, L, L, L), dtype=np.int64)
    reg = np.zeros((6, L, L, L), dtype=np.float64)
    two_pi_N = 2 * np.pi / N
    hist_game_board, hist_esc, hist_home, hist_flux, hist_reg, hist_flat = [], [], [], [], [], []
    per = max(period, 1)
    acc_n = np.zeros((L, L, L))
    acc_J = np.zeros((3, L, L, L))
    acc_u = np.zeros((L, L, L))
    acc_cnt = 0
    snaps = {}
    g = np.indices((L, L, L)) - c
    r = np.sqrt((g**2).sum(axis=0))
    for t in range(ticks):
        Aamp = np.sqrt(amt) * np.exp(1j * two_pi_N * ph)
        u = Aamp.sum(axis=0) / 3.0
        B = u[None] - Aamp
        n_in = amt.sum(axis=0)
        w2 = np.abs(B) ** 2
        tot = w2.sum(axis=0)
        share = np.where(tot[None] > 0, w2 / np.maximum(tot[None], 1e-300) * n_in[None], 0.0)
        leave = np.floor(share + reg).astype(np.int64)
        reg = reg + share - leave
        # conservation check: sum leave + sum reg change == n_in (registers hold the rest)
        lph = np.round(np.angle(B) / two_pi_N).astype(np.int64) % N
        # source Node
        home = int(amt[:, c, c, c].sum())
        src_phase = (
            (m * t // K) % N
            if (m is not None and K is not None)
            else (int(round(t * N / period)) % N if period > 0 else 0)
        )
        emit_share = q / 6.0
        # per-Port emission remainder (six registers on the thing)
        if t == 0:
            src_regs = np.zeros(6)
        src_regs_prev = src_regs.copy()
        e = np.floor(emit_share + src_regs).astype(np.int64)
        src_regs = src_regs + emit_share - e
        int(e.sum())
        if variant == "recycle":
            # R13: home joins the emission, (home + q) shared six-fold in whole quanta, the fractions
            # kept in the thing's six per-Port registers (its parked shadows), at the thing's phase.
            emit_share2 = (home + q) / 6.0
            e = np.floor(emit_share2 + src_regs_prev).astype(np.int64)
            src_regs = src_regs_prev + emit_share2 - e
            leave[:, c, c, c] = e
            lph[:, c, c, c] = src_phase
            reg[:, c, c, c] = 0.0
            int(e.sum())
        elif rerelease:
            # the returned share on lane p (the arrival through Port p) leaves again through Port p, merged with the emission
            arr_amt = amt[:, c, c, c]
            arr_ph = ph[:, c, c, c]
            merged = np.sqrt(arr_amt) * np.exp(1j * two_pi_N * arr_ph) + np.sqrt(e) * np.exp(
                1j * two_pi_N * src_phase
            )
            leave[:, c, c, c] = arr_amt + e
            lph[:, c, c, c] = np.round(np.angle(merged) / two_pi_N).astype(np.int64) % N
            reg[:, c, c, c] = 0.0
            home = 0
        else:
            leave[:, c, c, c] = e
            lph[:, c, c, c] = src_phase
            reg[:, c, c, c] = 0.0
        cubes = [h for h in (2, 4, 8, 12, 15, 19) if h <= c - 1]
        fl = [cube_flux_int(leave, c, h) for h in cubes]
        hist_flux.append(fl)
        # walk
        new_amt = np.zeros_like(amt)
        new_ph = np.zeros_like(ph)
        esc = 0
        for p in range(6):
            ax, s = AX[p], SGN[p]
            ra = np.roll(leave[p ^ 1], -s, axis=ax)
            rp = np.roll(lph[p ^ 1], -s, axis=ax)
            if not periodic:
                idx = [slice(None)] * 3
                idx[ax] = -1 if s == 1 else 0
                ra[tuple(idx)] = 0
                fidx = [slice(None)] * 3
                fidx[ax] = -1 if s == 1 else 0
                esc += int(leave[p][tuple(fidx)].sum())
            new_amt[p] = ra
            new_ph[p] = rp
        amt, ph = new_amt, new_ph
        hist_game_board.append(int(amt.sum()))
        hist_esc.append(esc)
        hist_home.append(home)
        hist_reg.append(float(reg.sum()))
        # readings
        n = amt.sum(axis=0)
        J = np.zeros((3, L, L, L))
        for p in range(6):
            J[AX[p]] -= SGN[p] * amt[p]
        Aamp2 = np.sqrt(amt) * np.exp(1j * two_pi_N * ph)
        uu = np.abs(Aamp2.sum(axis=0) / 3.0)
        hist_flat.append(float(n.sum() - 3.0 * np.sum(uu**2)))
        acc_n += n
        acc_J += J
        acc_u += uu
        acc_cnt += 1
        if acc_cnt == per:
            snaps[t + 1] = (acc_n / per, acc_J / per, acc_u / per)
            acc_n = np.zeros((L, L, L))
            acc_J = np.zeros((3, L, L, L))
            acc_u = np.zeros((L, L, L))
            acc_cnt = 0
    return dict(
        L=L,
        c=c,
        r=r,
        snaps=snaps,
        game_board=hist_game_board,
        esc=hist_esc,
        home=hist_home,
        q=q,
        period=period,
        g=g,
        flux=hist_flux,
        regs=hist_reg,
        flat=hist_flat,
    )


def cmd_integer(args):
    t0 = time.time()
    res = run_integer(
        args.L,
        args.periodic,
        args.period,
        args.q,
        args.ticks,
        N=args.N,
        rerelease=(args.variant == "mirror"),
        variant=args.variant,
    )
    L, c, r, q, g = res["L"], res["c"], res["r"], res["q"], res["g"]
    snaps = res["snaps"]
    keys = sorted(snaps)
    # average the last W period snapshots
    W = args.window
    lastk = keys[-W:]
    n_f = np.mean([snaps[k][0] for k in lastk], axis=0)
    J_f = np.mean([snaps[k][1] for k in lastk], axis=0)
    u_f = np.mean([snaps[k][2] for k in lastk], axis=0)
    rs = np.where(r == 0, 1, r)
    Jr = (J_f * g).sum(axis=0) / rs
    out = dict(
        config=dict(
            L=L,
            periodic=args.periodic,
            period=args.period,
            q=q,
            ticks=args.ticks,
            window_periods=W,
            variant=args.variant,
        ),
        game_board_over_q=res["game_board"][-1] / q,
        escaped_over_q=float(np.mean(res["esc"][-32:])) / q,
        home_over_q=float(np.mean(res["home"][-32:])) / q,
        seconds=round(time.time() - t0, 1),
    )
    per = {}
    for name, (x, y, z) in NODES.items():
        if max(abs(x), abs(y), abs(z)) > c - 1:
            continue
        i, j, k = c + x, c + y, c + z
        rr = float(r[i, j, k])
        per[name] = dict(
            r=round(rr, 2),
            n=float(n_f[i, j, k]),
            Jr=float(Jr[i, j, k]),
            absu=float(u_f[i, j, k]),
            n_r2_over_q=float(n_f[i, j, k]) * rr * rr / q,
            Jr_4pir2_over_q=float(Jr[i, j, k]) * 4 * np.pi * rr * rr / q,
            absu_r_over_sqrtq=float(u_f[i, j, k]) * rr / np.sqrt(q),
        )
    out["nodes"] = per
    shells = {}
    for R in (2, 4, 6, 8, 10, 12, 14, 16, 18, 20):
        m = np.abs(r - R) < 0.5
        if m.sum() == 0 or R > c - 1:
            continue
        shells[R] = dict(
            nodes=int(m.sum()),
            n=float(n_f[m].mean()),
            Jr=float(Jr[m].mean()),
            Jr_4pir2_over_q=float(Jr[m].mean()) * 4 * np.pi * R * R / q,
            n_r2_over_q=float(n_f[m].mean()) * R * R / q,
            absu_r_over_sqrtq=float(u_f[m].mean()) * R / np.sqrt(q),
        )
    out["shells"] = shells
    # per-tick fluctuation at the axis Nodes over the last window: std of the per-period J_r
    fl = {}
    for name in ("axis_r4", "axis_r8", "axis_r12"):
        x = NODES[name][0]
        if x > c - 1:
            continue
        vals = [(snaps[k][1] * g).sum(axis=0)[c + x, c, c] / x for k in lastk]
        fl[name] = dict(mean=float(np.mean(vals)), std_over_periods=float(np.std(vals)))
    out["period_fluctuation_Jr"] = fl
    TS = (16, 32, 64, 96, 128, 192, 256, 320, 400, 600, 800, 1000, 1200, 1600, 2000)
    out["game_board_samples"] = {
        t: res["game_board"][t - 1] / q for t in TS if t <= len(res["game_board"])
    }
    out["flat_samples"] = {t: res["flat"][t - 1] / q for t in TS if t <= len(res["flat"])}
    out["reg_samples"] = {t: res["regs"][t - 1] / q for t in TS if t <= len(res["regs"])}
    # probe J_r per 100-tick window on the axis and the diagonal
    win = {}
    for name in ("axis_r4", "axis_r8", "axis_r12", "111_m5", "111_m7"):
        x, y, z = NODES[name]
        if max(x, y, z) > c - 1:
            continue
        rr = float(r[c + x, c + y, c + z])
        vals = {}
        for t0 in range(0, args.ticks, 100):
            ks = [k for k in keys if t0 < k <= t0 + 100]
            if not ks:
                continue
            Jm = np.mean([snaps[k][1] for k in ks], axis=0)
            jr = float((Jm * g).sum(axis=0)[c + x, c + y, c + z] / rr)
            nm = float(np.mean([snaps[k][0][c + x, c + y, c + z] for k in ks]))
            vals[t0 + 100] = (round(jr * 4 * np.pi * rr * rr / q, 3), round(nm * rr * rr / q, 4))
        win[name] = vals
    out["probe_windows_Jr4pir2_over_q_and_nr2_over_q"] = win
    cubes = [h for h in (2, 4, 8, 12, 15, 19) if h <= c - 1]
    out["flux_cubes"] = cubes
    ww = max(32, args.window * max(args.period, 1))
    out["flux_over_q_mean_last_window"] = [
        float(np.mean([f[i] for f in res["flux"][-ww:]])) / q for i in range(len(cubes))
    ]
    out["flux_over_q_samples"] = {
        t: [round(v / q, 4) for v in res["flux"][t - 1]]
        for t in (32, 64, 128, 256, 400, 600, 800, 1000, 1200)
        if t <= len(res["flux"])
    }
    print(json.dumps(out, indent=1, default=float))


def cmd_walk(args):
    """A lone quantum's path under the integer rule with per-Node per-Port registers (a rotor-router):
    mean square displacement against t, and the fraction sent back at each Node."""
    rng = np.random.default_rng(0)
    c = 40
    T = args.ticks
    msd = np.zeros(T)
    back = 0
    steps = 0
    for _trial in range(args.trials):
        reg = {}
        x = np.array([c, c, c])
        p_in = 0  # arrived through Port 0 (from +x), heading -x
        # random initial heading
        p_in = int(rng.integers(6))
        for t in range(T):
            key = tuple(x)
            R = reg.setdefault(key, np.zeros(6))
            share = np.full(6, 1 / 9.0)
            share[p_in] = 4 / 9.0
            R += share
            p_out = int(np.argmax(R))
            R[p_out] -= 1.0
            if p_out == p_in:
                back += 1
            steps += 1
            x = x + DIRS[p_out]
            p_in = p_out ^ 1
            msd[t] += float(((x - c) ** 2).sum())
    msd /= args.trials
    D = msd[-1] / (6 * T)
    print(
        json.dumps(
            dict(
                T=T,
                trials=args.trials,
                back_fraction=back / steps,
                msd_samples={t: float(msd[t - 1]) for t in (4, 16, 64, 256, 1024) if t <= T},
                D_est=float(D),
            ),
            indent=1,
        )
    )


def cmd_transit(args):
    """Mean distance to the face of a cube of half-width H over directions, and the mean-field GameBoard total."""
    n = 200000
    rng = np.random.default_rng(1)
    v = rng.normal(size=(n, 3))
    v /= np.linalg.norm(v, axis=1)[:, None]
    dist = 1.0 / np.max(np.abs(v), axis=1)
    print(
        json.dumps(
            dict(
                mean_distance_to_face_over_H=float(dist.mean()),
                sqrt3_times=float(np.sqrt(3) * dist.mean()),
            ),
            indent=1,
        )
    )


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    a = sub.add_parser("meanfield")
    a.add_argument("--L", type=int, default=33)
    a.add_argument("--periodic", action="store_true")
    a.add_argument("--period", type=int, default=16)
    a.add_argument("--variant", default="rerelease")
    a.add_argument("--q", type=float, default=786432.0)
    a.add_argument("--ticks", type=int, default=400)
    a = sub.add_parser("edge")
    a.add_argument("--L", type=int, default=64)
    a.add_argument("--period", type=int, default=16)
    a.add_argument("--ticks", type=int, default=400)
    a = sub.add_parser("home")
    a.add_argument("--L", type=int, default=41)
    a.add_argument("--ticks", type=int, default=300)
    a = sub.add_parser("integer")
    a.add_argument("--L", type=int, default=33)
    a.add_argument("--periodic", action="store_true")
    a.add_argument("--period", type=int, default=16)
    a.add_argument("--q", type=float, default=786432.0)
    a.add_argument("--ticks", type=int, default=320)
    a.add_argument("--window", type=int, default=4)
    a.add_argument("--variant", default="recycle")
    a.add_argument("--N", type=int, default=64)
    a = sub.add_parser("walk")
    a.add_argument("--ticks", type=int, default=1024)
    a.add_argument("--trials", type=int, default=200)
    a = sub.add_parser("transit")
    args = ap.parse_args()
    {
        "meanfield": cmd_meanfield,
        "edge": cmd_edge,
        "home": cmd_home,
        "integer": cmd_integer,
        "walk": cmd_walk,
        "transit": cmd_transit,
    }[args.cmd](args)


if __name__ == "__main__":
    main()
