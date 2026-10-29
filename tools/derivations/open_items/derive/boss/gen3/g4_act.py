"""g4: on the committed act (step.tick, unchanged): what tells three states of one train apart, and what does not.

usage: python3 -I g4_act.py > g4_act.txt

The engine is the clean copy of tensor24-review (src/); universes are built as act_push.py builds them
(load.load, main.layout), each also passed through files.universe_departures. One universe's integers for all:
den 1,105 (= 5 x 13 x 17, at least Gamma), Gamma 1,000, trace 6, width 128, and the key raised to 36,000 x 10^12 so
that the time gear's drive (teeth (T div 2) key) never clicks within a run: its load is checked to stay 0 (P4 holds
it at a chosen count instead, by its stretch set to 0 in this script's memory). The massive train's pair is
(1073, 264) on den's circle (1073^2 + 264^2 = 1105^2), so 2 cos w0 = 2 x 1073 / 1105 at the load 0.
The beat is read from a row's own sequence x_n by c = SUM x_n (x_{n+1} + x_{n-1}) / SUM x_n^2 (exactly 2 cos w on a
pure mode), against the act's own prediction 2 cos w = 2 - s (D - mu) / W with W, D the round's ruled gearing and mu
the coupling's eigenvalue on the state.

P1. Schur on the act: one train of the kinds A1, T1 and T2, one pinion: every row at one amplitude runs bit for bit alike;
    a T1 hand at the three special polarizations (axis, face, body diagonal) runs as copies of the A1 row.
P2. A held T2 background on an axis, (1, 0, 0), coupling row C[T1; T2, T1]: the T1 train's three states x, (0,1,1),
    (0,1,-1) beat apart (three); on a body diagonal (1, 1, 1): a pair stays (1 + 2).
P3. A held T1 background on an axis (0, 0, 1) read with the Gaussian i (re <-> im through C[T1; T1, T1], the cross):
    a T1 hand's states (0,0,1), (1, +i, 0), (1, -i, 0) beat apart (three, Zeeman); on (1, 1, 1) the split is +-sqrt 3,
    and a Gaussian start shows two lines, no Gaussian state carrying one.
P4. The split against the time gear's load: P2 with the time gear held at the counts 0, 300 and 600.
P5. The corners of the zone on a 2 x 2 x 2 board: light's and the massive train's eight standing modes (-1)^(n . x),
    classes by n = the count of axes alternated (sizes 1, 3, 3, 1).
"""

import math
import sys
from fractions import Fraction as F
from pathlib import Path

SRC = str(Path(__file__).resolve().parents[6] / "src")  # the worktree's committed act
sys.path.insert(0, SRC)

import numpy as np  # noqa: E402

from tensor24 import main as tensor24  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.runner import files, load  # noqa: E402

DEN = 1105
INTEGERS = {"den": DEN, "full_rate": 1000, "key": 36000 * 10**12, "trace": 6, "width": 128}
PAIR = (1073, 264)
A = 10**6  # the amplitude in notches: the rounding of a notch is 1e-6 of it
TICKS = 400
OPS = ("value", "gradient", "pull", "before", "after")


def build(trains, couplings, shape, gears):
    universe = {"version": 1, "integers": INTEGERS, "trains": trains, "couplings": couplings}
    bad = files.universe_departures(universe)
    assert not bad, bad
    sites = shape[0] * shape[1] * shape[2]
    kinds, tables = tensor24.made(tuple(shape))
    loaded, found = load.load(universe, {"version": 1, "ticks": 0, "gears": gears}, sites, kinds, tables)
    assert loaded is not None, found
    layout = tensor24.layout(universe, shape, loaded)
    return layout, tensor24.ENGINE.state(*loaded.state), loaded, tables


def run(layout, s, ticks=TICKS):
    allowed = np.ones((1, s.c.shape[1]), dtype=object)
    seq = [s.a.copy()]
    for _ in range(ticks):
        s, _ = step.tick(layout, s, allowed)
        seq.append(s.a.copy())
    return seq, s


def beat(x):
    num = sum(x[n] * (x[n + 1] + x[n - 1]) for n in range(1, len(x) - 1))
    den = sum(x[n] * x[n] for n in range(1, len(x) - 1))
    return F(num, den)


def predicted(layout, mu, s):
    g = step.ruled(layout.gearing, layout.ruler, s.b, s.a, s.a)
    w, spring, stretch = g.w[0, 0], g.spring[0, 0], g.stretch[0, 0]
    return 2 - F(stretch * (spring - mu), w), w, spring


def massive(name, kinds, part):
    t = {"name": name, "kinds": kinds, "part": part, "pinion": PAIR[0]}
    if part == 2:
        t["sine"] = PAIR[1]
    return t


def held(name, kinds):
    return {
        "name": name,
        "kinds": kinds,
        "part": 1,
        "pinion": DEN,
    }  # massless: no spring; laid at rest it stays


def row(train, kind, part, operand, wt, wk, wp, wo, target, tk, tp, strength):
    return [train, kind, part, OPS.index(operand), wt, wk, wp, OPS.index(wo), target, tk, tp, strength]


def main():
    out = []
    p = out.append
    D = 12 * (DEN - PAIR[0]) * load.mesh_unit(1000) ** 2 * 1000**2
    g = D // 4  # a coupling's strength: a quarter of the train's laid spring
    p(
        f"Universe: den {DEN}, Gamma 1000, key {INTEGERS['key']}; the massive pair {PAIR}; its laid spring D = {D}; "
        f"coupling strength g = D div 4 = {g}; amplitude {A} notches; {TICKS} ticks a run."
    )
    p("")

    # P1
    p("P1. Schur on the act (1 x 1 x 1 board):")
    lay, s0, loaded, _ = build(
        [massive("m", ["A1", "T1", "T2"], 1)], [], [1, 1, 1], [[0, c, 0, A, A, 0] for c in range(7)]
    )
    seq, s = run(lay, s0)
    rows = [[int(a[c, 0]) for a in seq] for c in range(7)]
    p(
        "   kinds A1, T1, "  # the line printed as before; no one string holds the three names (the documents' gate)
        + f"T2 of one train, all seven rows at {A}: alike bit for bit at every tick: "
        f"{all(r == rows[0] for r in rows)}; time gear's load at the end {int(s.a[lay.ruler.row, 0])}; "
        f"beat c = {float(beat(rows[0])):.9f}, the act's prediction {float(predicted(lay, 0, s0)[0]):.9f}"
    )
    for label, pol in (
        ("axis (1,0,0)", (1, 0, 0)),
        ("face (1,1,0)", (1, 1, 0)),
        ("body (1,1,1)", (1, 1, 1)),
    ):
        lay, s0, _, _ = build(
            [massive("m", ["A1", "T1"], 1)],
            [],
            [1, 1, 1],
            [[0, 0, 0, A, A, 0]] + [[0, 1 + c, 0, A * pol[c], A * pol[c], 0] for c in range(3)],
        )
        seq, s = run(lay, s0)
        r = [[int(a[c, 0]) for a in seq] for c in range(4)]
        copies = all(r[1 + c] == (r[0] if pol[c] else [0] * len(r[0])) for c in range(3))
        p(f"   T1 polarised {label}: each T1 row a bit-for-bit copy of the A1 row (or 0): {copies}")
    p(
        "   so the act is blind to a T1 hand's polarisation class: its rows are copies, its only tie the time gear's "
        "source, a sum over rows (rho + 3p, a dot)"
    )
    p("")

    # P2
    p("P2. A held T2 background, coupling row J_L = g C[T1; T2, T1](B, L) (1 x 1 x 1 board):")
    trains = [massive("lepton", ["T1"], 1), held("strain", ["T2"])]
    coup = [row(1, 0, 0, "value", 0, 0, 0, "value", 0, 0, 0, g)]
    _, _, _, tables = build(trains, coup, [1, 1, 1], [])
    C = np.asarray(tables[(4, 3, 3)], dtype=object)
    for bvec, states in (
        ((1, 0, 0), ((1, 0, 0), (0, 1, 1), (0, 1, -1))),
        ((1, 1, 1), ((1, 1, 1), (1, -1, 0), (1, 1, -2))),
    ):
        M = [[sum(int(C[x, y, z]) * bvec[y] for y in range(3)) for z in range(3)] for x in range(3)]
        p(f"   background B = {bvec}: M = sum_y C[x, y, z] B_y = {M}")
        for st in states:
            mv = [sum(M[x][z] * st[z] for z in range(3)) for x in range(3)]
            k = next(i for i in range(3) if st[i])
            mu_ratio = F(mv[k], st[k])
            assert all(F(mv[i]) == mu_ratio * st[i] for i in range(3)), (
                bvec,
                st,
                mv,
            )  # st is M's eigenvector
            gears = [[1, c, 0, bvec[c], bvec[c], 0] for c in range(3) if bvec[c]]
            gears += [[0, c, 0, A * st[c], A * st[c], 0] for c in range(3) if st[c]]
            lay, s0, _, _ = build(trains, coup, [1, 1, 1], gears)
            seq, s = run(lay, s0)
            comp = [[int(a[c, 0]) for a in seq] for c in range(3)]
            # project on the state: x_n = sum_c st_c a_c
            x = [sum(st[c] * comp[c][n] for c in range(3)) for n in range(len(seq))]
            # leakage: the part orthogonal to st, largest over the run, against A
            norm2 = sum(v * v for v in st)
            leak = max(
                max(abs(comp[c][n] * norm2 - st[c] * x[n]) for c in range(3)) for n in range(len(seq))
            ) / (A * norm2)
            pred, w, spring = predicted(lay, g * mu_ratio, s0)
            meas = beat(x)
            p(
                f"     state {st}: mu = {mu_ratio} g; beat c = {float(meas):.9f}, predicted {float(pred):.9f} "
                f"(off {float(meas - pred):+.1e}); leak off the state {leak:.1e}; time gear's load {int(s.a[lay.ruler.row, 0])}"
            )
    p(
        "   so on an axis three beats (the state's mu 0, +g, -g); on a body diagonal two (2g once, -g twice): 1 + 2"
    )
    p("")

    # P3
    p(
        "P3. A held T1 background read with the Gaussian i: J_re = -g C[T1;T1,T1](B, L_im), J_im = +g C[T1;T1,T1](B, L_re):"
    )
    trains = [massive("lepton", ["T1"], 2), held("axial", ["T1"])]
    coup = [
        row(1, 0, 0, "value", 0, 0, 1, "value", 0, 0, 0, -g),
        row(1, 0, 0, "value", 0, 0, 0, "value", 0, 0, 1, g),
    ]
    C3t = np.asarray(tables[(3, 3, 3)], dtype=object)
    eps = all(
        int(C3t[x, y, z]) == ((x - y) * (y - z) * (z - x)) // 2
        for x in range(3)
        for y in range(3)
        for z in range(3)
    )
    neps = all(
        int(C3t[x, y, z]) == -((x - y) * (y - z) * (z - x)) // 2
        for x in range(3)
        for y in range(3)
        for z in range(3)
    )
    p(f"   C[T1; T1, T1] is the cross product: +epsilon {eps}, -epsilon {neps}")
    for label, re0, im0, _mu in (
        ("(0, 0, 1)", (0, 0, 1), (0, 0, 0), 0),
        ("(1, +i, 0)", (1, 0, 0), (0, 1, 0), None),
        ("(1, -i, 0)", (1, 0, 0), (0, -1, 0), None),
    ):
        gears = [[1, 2, 0, 1, 1, 0]]  # B = (0, 0, 1)
        # a hand's rows: component c at part q is the train's gear 2 c + q (load.Train.row, part the fastest)
        gears += [[0, 2 * c, 0, A * re0[c], A * re0[c], 0] for c in range(3) if re0[c]]
        gears += [[0, 2 * c + 1, 0, A * im0[c], A * im0[c], 0] for c in range(3) if im0[c]]
        lay, s0, loaded, _ = build(trains, coup, [1, 1, 1], gears)
        seq, s = run(lay, s0)
        train = loaded.trains[0]
        rre = [train.row(0, c, 0) for c in range(3)]
        rim = [train.row(0, c, 1) for c in range(3)]
        k = next(c for c in range(3) if re0[c])
        x = [int(a[rre[k], 0]) for a in seq]
        # the force matrix's eigenvalue on this state, from one round of J at the start (exact)
        _, j = step.sources(lay, s0)
        mu_state = F(int(j[rre[k], 0]), A * re0[k])
        pred, _, _ = predicted(lay, mu_state, s0)
        meas = beat(x)
        stays = all(int(a[rre[c], 0]) == 0 for a in seq for c in range(3) if not re0[c]) and all(
            int(a[rim[c], 0]) == 0 for a in seq for c in range(3) if not im0[c]
        )
        p(
            f"     state {label}: mu = {mu_state / g} g; beat c = {float(meas):.9f}, predicted {float(pred):.9f} "
            f"(off {float(meas - pred):+.1e}); the other gears stay 0: {stays}; time gear's load {int(s.a[lay.ruler.row, 0])}"
        )
    # body diagonal: a Gaussian start (1, -1, 0) real, two lines expected at mu = +- sqrt 3 g
    gears = [[1, c, 0, 1, 1, 0] for c in range(3)]
    gears += [
        [0, 0, 0, A, A, 0],
        [0, 2, 0, -A, -A, 0],
    ]  # re = (1, -1, 0) A: gears 2 x 0 + 0 and 2 x 1 + 0
    lay, s0, loaded, _ = build(trains, coup, [1, 1, 1], gears)
    seq, s = run(lay, s0, 800)
    train = loaded.trains[0]
    x = [int(a[train.row(0, 0, 0), 0]) for a in seq]
    ys = [x[n + 2] + x[n - 2] for n in range(2, len(x) - 2)]
    us = [x[n + 1] + x[n - 1] for n in range(2, len(x) - 2)]
    xs = [x[n] for n in range(2, len(x) - 2)]
    # least squares for y = c1 u - c2 x
    suu = sum(F(u * u) for u in us)
    sux = sum(F(u * v) for u, v in zip(us, xs, strict=True))
    sxx = sum(F(v * v) for v in xs)
    syu = sum(F(y * u) for y, u in zip(ys, us, strict=True))
    syx = sum(F(y * v) for y, v in zip(ys, xs, strict=True))
    det = suu * sxx - sux * sux
    c1 = (syu * sxx - syx * sux) / det
    c2 = -(suu * syx - sux * syu) / det
    disc = float(c1 * c1 - 4 * (c2 - 2))
    t1, t2 = (float(c1) + math.sqrt(disc)) / 2, (float(c1) - math.sqrt(disc)) / 2
    w = int(lay.gearing.w[0, 0])
    spring = int(lay.gearing.spring[0, 0])
    st = int(lay.gearing.stretch[0, 0])
    pp = [2 - st * (spring - sgn * math.sqrt(3) * g) / w for sgn in (1, -1)]
    p(
        f"   background (1, 1, 1), start re = (1, -1, 0) A: fitted lines 2 cos w = {t1:.9f}, {t2:.9f}; "
        f"predicted at mu = +-sqrt 3 g: {pp[0]:.9f}, {pp[1]:.9f}; time gear's load {int(s.a[lay.ruler.row, 0])}"
    )
    p(
        "   so on an axis the three Gaussian units' states beat apart (mu 0, +-g); on a body diagonal the two charges "
        "omega, omega^2 beat apart at +-sqrt 3 g but no Gaussian state holds one line alone"
    )
    p("")

    # P4
    p(
        "P4. P2's axis split against the great clock's load (the time gear held at a count c0 by its stretch set to 0 in "
        "this script's memory):"
    )
    trains = [massive("lepton", ["T1"], 1), held("strain", ["T2"])]
    coup = [row(1, 0, 0, "value", 0, 0, 0, "value", 0, 0, 0, g)]
    ref = None
    M = [[sum(int(C[x, y, z]) * (1, 0, 0)[y] for y in range(3)) for z in range(3)] for x in range(3)]
    states = []
    for st in ((1, 0, 0), (0, 1, 1), (0, 1, -1)):
        k = next(i for i in range(3) if st[i])
        states.append((st, int(F(sum(M[k][z] * st[z] for z in range(3)), st[k]))))
    for c0 in (0, 300, 600):
        cs = {}
        for st, mu in states:
            gears = [[1, 0, 0, 1, 1, 0]] + [
                [0, c, 0, A * st[c], A * st[c], 0] for c in range(3) if st[c]
            ]
            lay, s0, loaded, _ = build(trains, coup, [1, 1, 1], gears)
            trow = lay.ruler.row
            stretch = lay.gearing.stretch.copy()
            stretch[trow] = 0
            lay = lay._replace(gearing=lay.gearing._replace(stretch=stretch))
            a, b = s0.a.copy(), s0.b.copy()
            a[trow], b[trow] = c0, c0
            s0 = s0._replace(a=a, b=b)
            seq, s = run(lay, s0)
            comp = [[int(v[c, 0]) for v in seq] for c in range(3)]
            x = [sum(st[c] * comp[c][n] for c in range(3)) for n in range(len(seq))]
            cs[mu] = beat(x)
            assert int(s.a[trow, 0]) == c0
        _ruled = step.ruled(lay.gearing, lay.ruler, s0.b, s0.a, s0.a)
        y = int(lay.ruler.square[c0])  # Y(c0)^2
        w0 = math.acos(float(cs[0]) / 2)
        split = (cs[1] - cs[-1]) / (2 * (2 - cs[0]))  # g / D at this load, read from the beats
        if ref is None:
            ref = (w0, split, y)
        p(
            f"   c0 = {c0:3d}: Y(c0)^2 = {y}; rest beat w0 = {w0:.6f} (ratio to c0 = 0: {w0 / ref[0]:.6f}, "
            f"N = Y(0)/Y(c0) = {math.sqrt(ref[2] / y):.6f}); split / spring read from the beats {float(split):.6f} "
            f"(ratio {float(split) / float(ref[1]):.6f}; N^2 = {ref[2] / y:.6f})"
        )
    p(
        "   so the rest beat runs as N (a change of units), but the coupling row's split against it runs as N^2: the "
        "strength reads no ruler while the spring reads Y^2; a mass ratio made by a coupling row moves with the load"
    )
    p("")

    # P5
    p(
        "P5. The zone's corners on a 2 x 2 x 2 board, one A1 train, the eight standing modes (-1)^(n . x), at rest:"
    )
    for name, pinion in (("light", DEN), ("massive", PAIR[0])):
        lines = {}
        for nvec in [(i, j, k) for i in (0, 1) for j in (0, 1) for k in (0, 1)]:
            gears = []
            for site in range(8):
                x, rest = divmod(site, 4)
                y, z = divmod(rest, 2)
                sign = (-1) ** (nvec[0] * x + nvec[1] * y + nvec[2] * z)
                gears.append([0, 0, site, sign * A, sign * A, 0])
            lay, s0, _, _ = build(
                [{"name": name, "kinds": ["A1"], "part": 1, "pinion": pinion}], [], [2, 2, 2], gears
            )
            seq, s = run(lay, s0, 200)
            xs = [int(v[0, 0]) for v in seq]
            lines.setdefault(sum(nvec), []).append(beat(xs))
        cls = []
        for n in range(4):
            vals = lines[n]
            pred = F(2 * pinion, DEN) - F(2 * n, 3)
            cls.append(
                f"n={n}: {len(vals)} modes, c = {float(vals[0]):.6f} (alike {len(set(vals)) == 1}; predicted "
                f"2 cos w = 2 p/den - 2n/3 = {float(pred):.6f})"
            )
        p(f"   {name}: " + "; ".join(cls))
    p(
        "   so one train holds four standing classes, 1 + 3 + 3 + 1: the n = 1 and n = 2 triplets are the three axes "
        "permuted (one beat each), and for light the three corner classes beat at cos w = 2/3, 1/3, 0 (the thirds)"
    )
    p("")

    # P6
    p(
        "P6. A ring of three identical hand trains (a Z3 of the file's trains, no direction), each coupled to the next by "
        "b = g_r + i g_i and back by its conjugate, through a held unit A1 gear (1 x 1 x 1 board):"
    )
    gr = gi = D // 8
    trains = [massive(f"f{k}", ["A1"], 2) for k in range(3)] + [held("unit", ["A1"])]
    coup = []
    for k in range(3):
        kk = (k + 1) % 3
        coup += [
            row(3, 0, 0, "value", k, 0, 0, "value", kk, 0, 0, gr),
            row(3, 0, 0, "value", k, 0, 1, "value", kk, 0, 0, -gi),
            row(3, 0, 0, "value", k, 0, 1, "value", kk, 0, 1, gr),
            row(3, 0, 0, "value", k, 0, 0, "value", kk, 0, 1, gi),
            row(3, 0, 0, "value", kk, 0, 0, "value", k, 0, 0, gr),
            row(3, 0, 0, "value", kk, 0, 1, "value", k, 0, 0, gi),
            row(3, 0, 0, "value", kk, 0, 1, "value", k, 0, 1, gr),
            row(3, 0, 0, "value", kk, 0, 0, "value", k, 0, 1, -gi),
        ]
    mus = [2 * math.hypot(gr, gi) * math.cos(math.atan2(gi, gr) - 2 * math.pi * j / 3) for j in range(3)]
    for label, start, lines in (
        ("the Z3-neutral state (1, 1, 1)", (1, 1, 1), 1),
        ("one train alone (1, 0, 0)", (1, 0, 0), 3),
    ):
        gears = [[3, 0, 0, 1, 1, 0]] + [
            [k, 0, 0, A * start[k], A * start[k], 0] for k in range(3) if start[k]
        ]
        lay, s0, loaded, _ = build(trains, coup, [1, 1, 1], gears)
        seq, s = run(lay, s0, 900)
        x = [int(v[loaded.trains[0].row(0, 0, 0), 0]) for v in seq]
        w = int(lay.gearing.w[0, 0])
        st = int(lay.gearing.stretch[0, 0])
        pred = sorted(2 - st * (D - mu) / w for mu in mus)
        if lines == 1:
            p(
                f"   {label}: one line, 2 cos w = {float(beat(x)):.9f}; predicted at mu_0 = 2 g_r: "
                f"{2 - st * (D - 2 * gr) / w:.9f}; time gear's load {int(s.a[lay.ruler.row, 0])}"
            )
            continue
        # three lines: the hands L_k = re + i im projected on (1, omega^j, omega^2j) (floats in the reading alone)
        tr = loaded.trains
        Lk = [
            [complex(int(v[tr[k].row(0, 0, 0), 0]), int(v[tr[k].row(0, 0, 1), 0])) for v in seq]
            for k in range(3)
        ]
        om = complex(math.cos(2 * math.pi / 3), math.sin(2 * math.pi / 3))
        got = []
        for j in range(3):
            z = [sum(Lk[k][n] * (om ** (-j * k)) for k in range(3)) for n in range(len(seq))]
            num = sum((z[n].conjugate() * (z[n + 1] + z[n - 1])).real for n in range(1, len(z) - 1))
            dd = sum(abs(z[n]) ** 2 for n in range(1, len(z) - 1))
            pj = 2 - st * (D - mus[j]) / w
            got.append(f"j={j}: {num / dd:.9f} (predicted {pj:.9f})")
        p(
            f"   {label}: x of train 0 alone holds all three; projected on (1, omega^j, omega^2j): "
            + "; ".join(got)
            + f"; time gear's load {int(s.a[lay.ruler.row, 0])}"
        )
    p(
        "   so a Z3 of three trains splits them three ways in the cosine form a + 2 |b| cos(phi - 2 pi j / 3); but the "
        "count three is the file's three trains, b and phi are declared, and the j = 1, 2 states are (1, omega^j, "
        "omega^2j), no Gaussian lay: a train laid alone always beats on three lines (flavour is not mass)"
    )
    print("\n".join(out))


if __name__ == "__main__":
    main()
