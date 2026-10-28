"""The head's light act, tick by tick, against its formula in Tensor24's terms (stage 4's probe, BRIEF_HEAD_LIGHT.md).

The head is src/event_universe at 67b765312; Tensor24's gear is src/tensor24/engine/step.py:gear on tensor24-review
(0970b0deb), read from a copy made by `git archive` (never the Boss's clone). Every number below is a Python integer.

The formula checked, for the light (the unsprung hand, ratio (rim, rim), gears three and twelve) at a clock i, forward:
    W   = (T div 2)(X_b + X_n)                 T = 6 rim Gamma^2 G^2, (X_b, X_n) the regulator's time gear at the start
    s   = X_n                                  the stretch at the start
    p_i = mesh_rate(max(load_of(X_n), 0))      the clock's own mesh rate at its load
    Q_ij from the regulator's tension gears    (G^2 (Gamma - t)^2 + Gamma^2 div 2) div Gamma^2, t = (N_a(i) + N_a(j) + 1) div 2
                                               clipped to [0, Gamma]; 0 where an end is stopped
    R_ij = 2 rim p_i^2 Q_ij                    the six grips; D = 12 (rim - rim) p_0^2 G^2 = 0 the spring
    F    = SUM_j R_ij (a_j - a) - D a          a_j the neighbour's now slot as it is (coupling 0: the turn is the identity)
    P    = W (a - b) + (r - W div 2)           W div 2 = mid(W) = Tensor24's home(W, 0)
    W+   = (T div 2)(X_n + X_n')               X_n' the time gear after the regulator's act (W where that is <= 0)
    (q, r+) = divmod(P + going s F + W+ div 2, W+),  a+ = a + q,  b+ = a     (going = 1, no kick K)
i.e. Tensor24's gear(a, b, r, go=0, w=W, wp=W+, push=s F) with grip_j = s R_ij.
After the gear act the head can still change the light at a clock: the release's advance on the three gear (Tick.advances),
the stopped clocks' restore, the turnover at the top (the held pre-state exchanged: three (b, a, (2 mid W - r) mod W),
twelve (-b, -a, r)) and the click's unwinds; the probe checks the end of every tick against these and counts each.

Run: TMPDIR=/dev/shm/tmp PYTHONDONTWRITEBYTECODE=1 python -I probe.py <head worktree> <tensor24 copy's src> [records dir]
with the head:     git -C /home/user/Universe24 worktree add --detach <head worktree> 67b765312
and Tensor24:      git -C /home/user/Universe24 archive origin/tensor24-review src/tensor24 | tar -x -C <dir>
                   (then <tensor24 copy's src> is <dir>/src); python is /home/user/Universe24/venv314/bin/python.
"""

import gzip
import json
import sys
from collections import Counter

import numpy as np

WT, T24 = sys.argv[1], sys.argv[2]
RECORDS = sys.argv[3] if len(sys.argv) > 3 else "/dev/shm/tmp"
sys.path[:0] = [WT + "/src", WT, T24]

from event_universe import readings  # noqa: E402
from event_universe import tick as T  # noqa: E402
from event_universe.clock import Clock  # noqa: E402
from event_universe.core import rates  # noqa: E402
from event_universe.core.spokes import SPOKE_SIDES  # noqa: E402
from event_universe.features import stretch  # noqa: E402
from event_universe.trains import REGULATOR  # noqa: E402
from tensor24.algebra.carry import home as t24_home  # noqa: E402
from tensor24.engine.step import gear as t24_gear  # noqa: E402
from tests.laws import world_of  # noqa: E402

GEARS = ("three", "twelve")


def nbr(a, spoke):
    """The array at the clock beyond the spoke, out[i] = a[i + side] on the torus (core/spokes.across), written anew."""
    axis, side = SPOKE_SIDES[spoke]
    return np.roll(a, -side, axis=axis)


def snap(train):
    return [
        (g.now.copy(), g.before.copy(), g.fine.copy(), g.teeth.copy() if np.ndim(g.teeth) else g.teeth,
         None if g.dfine is None else g.dfine.copy())
        for g in train.gears
    ]


def eq(x, y):
    return np.asarray(x == y, dtype=bool)


def ints(a):
    return [int(v) for v in np.asarray(a).reshape(-1)]


class Probe:
    """The hooks on the head's acts for one clock, and the formula's check at every clock and tick."""

    def __init__(self, clock, records):
        self.clock, self.records, self.stats, self.cur = clock, records, Counter(), {}
        self.light = clock.unsprung()
        self.reg = clock.train(REGULATOR)
        c = clock
        self.T6 = 6 * c.rim * c.full_rate**2 * c.G**2
        assert self.T6 == c.teeth, "the teeth T differ from clock.teeth"
        self.H6 = self.T6 // 2
        self.W0 = self.H6 * (c.full_rate + c.full_rate)  # the vacuum's W, X_b = X_n = Gamma
        self.grip0 = c.full_rate * 2 * c.rim * c.full_rate**2 * c.G**2  # s R_ij at the vacuum: Gamma 2 rim Gamma^2 G^2
        self.ticks = 0
        self.lo, self.hi = {}, {}

    def note_range(self, name, arr):
        vals = ints(arr)
        lo, hi = min(vals), max(vals)
        self.lo[name] = min(self.lo.get(name, lo), lo)
        self.hi[name] = max(self.hi.get(name, hi), hi)

    # ---- the hooks -------------------------------------------------------------------------------------------
    def impulse(self, tick, orig):
        c, cur = self.clock, {}
        k = tick.where[id(self.light)]
        cur["going"] = tick.going
        cur["start"] = snap(self.light)
        tg = self.reg.gears[0]
        cur["Xb"], cur["Xn"] = tg.before.copy(), tg.now.copy()
        cur["N"] = [g.now.copy() for g in self.reg.gears[1:4]]
        cur["head_s"], cur["head_load"] = tick.stretch_now, tick.load
        cur["head_factors"], cur["head_stopped"] = tick.factors, tick.stopped
        cur["head_pull"] = [p.copy() for p in tick.pull[k]]
        cur["head_spring_train"] = tick.train_spring[k]
        cur["head_gearing"] = readings.gearing_of(c, self.light, tick.load, tick.factors)
        cur["head_w_side"] = readings.mean_teeth(c, tg)
        cur["held_load"] = c.start_held
        orig(tick)
        cur["head_impelled"] = [p.copy() for p in tick.impelled[k]]
        self.cur = cur

    def advances(self, tick, orig):
        cur = self.cur
        cur["gear"] = snap(self.light)
        tg = self.reg.gears[0]
        cur["Xn1"], cur["Xb1"] = tg.now.copy(), tg.before.copy()
        cur["head_wdiv"] = tick.end_teeth(tg)
        orig(tick)
        cur["advanced"] = snap(self.light)

    def carry(self, tick, orig):
        orig(tick)
        self.cur["restored"] = snap(self.light)
        self.cur["stopped_final"] = tick.stopped.copy()

    def turnover(self, tick, orig):
        self.cur["x2"] = self.reg.gears[0].now.copy()  # the time gear's now after the drives, the trigger's third notch
        orig(tick)
        self.cur["turned"] = snap(self.light)
        self.cur["top"] = np.asarray(tick.top, dtype=bool).copy()

    def click(self, tick, orig):
        births = self.clock.counts["births"]
        orig(tick)
        self.cur["end"] = snap(self.light)
        self.cur["births"] = self.clock.counts["births"] - births
        self.ticks += 1
        self.check(self.ticks, self.cur)

    # ---- the check -------------------------------------------------------------------------------------------
    def check(self, t, cur):
        c, st = self.clock, self.stats
        G, rim, Gamma = c.G, c.rim, c.full_rate
        size = int(np.prod(c.size))
        going = cur["going"]
        Xb, Xn, Xn1 = cur["Xb"], cur["Xn"], cur["Xn1"]

        # W, s, W+ from the regulator's time gear
        W = self.H6 * (Xb + Xn)
        s = Xn.copy()
        Wp = self.H6 * (Xn + Xn1)
        fallback = np.asarray(Wp <= 0, dtype=bool)
        Wp = np.where(fallback, W, Wp)
        st["W: (T div 2)(X_b + X_n) = the head's mean teeth at the impulse, sites"] += int(eq(W, cur["head_w_side"]).sum())
        st["W: = the light gear's own teeth at the tick's start (both gears), gear-sites"] += sum(
            int(eq(W, g[3]).sum()) for g in cur["start"])
        st["s: X_n = the head's stretch_now, sites"] += int(eq(s, cur["head_s"]).sum())
        st["W+: (T div 2)(X_n + X_n') = the head's end teeth, sites"] += int(eq(Wp, cur["head_wdiv"]).sum())
        st["W+: X_b after the act = X_n at the start, sites"] += int(eq(cur["Xb1"], Xn).sum())
        st["W+: fallback to W (X_n + X_n' <= 0), sites"] += int(fallback.sum())
        st["W+ = W, sites (the stretch's two notches summed unchanged)"] += int(eq(Wp, W).sum())
        st["home: W div 2 = Tensor24's home(W, 0), sites"] += int(eq(W // 2, t24_home(W, 0)).sum())

        # the grips from the load and the tensions
        load = stretch.load_of(Gamma, Xn)
        st["load: load_of(X_n) = the head's load, sites"] += int(eq(load, cur["head_load"]).sum())
        pm = rates.mesh_rate_of(Gamma, np.maximum(load, 0))
        stopped = np.asarray(pm == 0, dtype=bool)
        st["stopped: mesh rate 0 at the load = the head's mask, sites"] += int(eq(stopped, cur["head_stopped"]).sum())
        st["stopped clocks, sites"] += int(stopped.sum())
        grips = []
        for j, (axis, _side) in enumerate(SPOKE_SIDES):
            n = cur["N"][axis]
            t_ = (n + nbr(n, j) + 1) // 2
            tc = np.minimum(np.maximum(t_, 0), Gamma)
            Q = (G * G * (Gamma - tc) ** 2 + (Gamma * Gamma) // 2) // (Gamma * Gamma)
            Q = np.where(stopped | nbr(stopped, j), 0, Q)
            st["Q: the mesh factor = the head's factors, spoke-sites"] += int(eq(Q, cur["head_factors"][j]).sum())
            R = 2 * rim * pm * pm * Q
            st["R: 2 rim p_i^2 Q_ij = the head's light grip, spoke-sites"] += int(eq(R, cur["head_gearing"].grips[j]).sum())
            grips.append(R)
        # symmetry of a mesh read from its two ends (the clock beyond +a reads the mesh through its -a spoke)
        for j in range(0, 6, 2):
            st["R: meshes read alike from both ends (R_ij = R_ji), meshes"] += int(eq(grips[j], nbr(grips[j + 1], j)).sum())
            st["R: meshes where Q_ij = Q_ji, meshes"] += int(eq(cur["head_factors"][j], nbr(cur["head_factors"][j + 1], j)).sum())
            st["R: meshes where p_i = p_j (the two ends' mesh rates), meshes"] += int(eq(pm, nbr(pm, j)).sum())
            st["R: meshes where s R_ij = s R_ji (Tensor24's grip), meshes"] += int(
                eq(s * grips[j], nbr(s * grips[j + 1], j)).sum())
            st["R: meshes, read"] += size
        uniform = all(len(set(ints(R))) == 1 for R in grips) and len({ints(R)[0] for R in grips}) == 1
        st["R: ticks with one grip on every spoke of every clock"] += int(uniform)
        p0 = rates.rate_of(Gamma, np.maximum(cur["held_load"], 0))
        D = 12 * (rim - self.light.ratio[0]) * p0 * p0 * G * G
        st["D: 12 (rim - pinion) p_0^2 G^2 = the head's spring, sites"] += int(eq(D, cur["head_gearing"].spring).sum())
        st["D: = 0, sites"] += int(eq(D, 0).sum())
        st["D: the head's spring per train = 0, sites"] += int(eq(cur["head_spring_train"], 0).sum())
        for name, arr in (("X_n", Xn), ("W", W), ("W+", Wp), ("grip R", np.concatenate([np.asarray(R).reshape(-1) for R in grips])),
                          ("load", load), ("mesh rate p_i", pm)):
            self.note_range(name, arr)

        start, gear_h = cur["start"], cur["gear"]
        rec = {"tick": t, "going": going, "W": ints(W), "Wp": ints(Wp), "s": ints(s), "spring": ints(D),
               "grips": [ints(R) for R in grips], "top": [int(x) for x in cur["top"].reshape(-1)]}
        for gi, name in enumerate(GEARS):
            a, b, r = start[gi][0], start[gi][1], start[gi][2]
            st[f"{name}: fine tooth r in [0, W) at the start, sites"] += int(((r >= 0) & (r < W)).sum())
            F = sum(R * (nbr(a, j) - a) for j, R in enumerate(grips)) - D * a
            st[f"{name}: F = SUM_j R_ij (a_j - a) - D a = the head's pull, sites"] += int(eq(F, cur["head_pull"][gi]).sum())
            P = W * (a - b) + (r - W // 2)
            push = going * s * F
            K = cur["head_impelled"][gi] - (P + push)
            st[f"{name}: the head's impelled = P + going s F (kick K = 0), sites"] += int(eq(K, 0).sum())
            u = P + push + Wp // 2
            q, rp = u // Wp, u % Wp
            a1, b1, r1 = a + q, a, rp
            ah, bh, rh, wh = gear_h[gi][0], gear_h[gi][1], gear_h[gi][2], gear_h[gi][3]
            ok = eq(ah, a1) & eq(bh, b1) & eq(rh, r1)
            st[f"{name}: GEAR ACT (a+, b+, r+) = the formula, sites"] += int(ok.sum())
            st[f"{name}: gear act, the gear's teeth set to W+, sites"] += int(eq(wh, Wp).sum())
            ta, tb, tr = t24_gear(a, b, r, 0, W, Wp, push)
            st[f"{name}: GEAR ACT = Tensor24's gear(a, b, r, 0, W, W+, s F), sites"] += int(
                (eq(ah, ta) & eq(bh, tb) & eq(rh, tr)).sum())
            # M1's one act from the head's own state: W+ = W = W_0 and every grip g_0, no regulator
            ma, mb, mr = t24_gear(a, b, r, 0, self.W0, self.W0, sum(self.grip0 * (nbr(a, j) - a) for j in range(6)))
            st[f"{name}: M1's act from the head's state, notches (a+, b+) = the head's gear act, sites"] += int(
                (eq(ah, ma) & eq(bh, mb)).sum())
            st[f"{name}: M1's act from the head's state, (a+, b+, r+) = the head's gear act, sites"] += int(
                (eq(ah, ma) & eq(bh, mb) & eq(rh, mr)).sum())
            st[f"{name}: sites read"] += size
            self.note_range(f"{name} F", F)
            self.note_range(f"{name} q (a+ - a)", q)

            # what the other acts did to the gear act at each clock
            def same(x, y):
                return eq(x[gi][0], y[gi][0]) & eq(x[gi][1], y[gi][1]) & eq(x[gi][2], y[gi][2])

            released = ~same(cur["advanced"], gear_h)
            if gear_h[gi][4] is not None:  # the three gear's drive fine tooth at the drive teeth T_d
                released |= ~eq(cur["advanced"][gi][4], gear_h[gi][4])
            restored = ~same(cur["restored"], cur["advanced"])
            turned = ~same(cur["turned"], cur["restored"])
            clicked = ~same(cur["end"], cur["turned"])
            st[f"{name}: the release's advance moved the gear, sites"] += int(released.sum())
            st[f"{name}: the stopped restore moved the gear, sites"] += int(restored.sum())
            st[f"{name}: the click moved the gear, sites"] += int(clicked.sum())
            top = cur["top"]
            # the turnover's formula from the held pre-state
            sign = 1 if gi == 0 else -1
            mid_w = W // 2
            r_t = (2 * mid_w - r) % W if gi == 0 else r
            e = cur["end"][gi]
            at_top_ok = eq(e[0], sign * b) & eq(e[1], sign * a) & eq(e[2], r_t) & eq(e[3], W)
            if start[gi][4] is not None:  # the drive fine tooth mirrored at the drive teeth T_d
                td = self.light.gears[gi].dteeth
                at_top_ok &= eq(e[4], (2 * (td // 2) - start[gi][4]) % td)
            st[f"{name}: turned-over clocks, sites"] += int(top.sum())
            st[f"{name}: turned-over clocks where the end = the turnover's formula (b, a, mirror r) / (-b, -a, r), sites"] += int(
                (at_top_ok & top).sum())
            st[f"{name}: turned-over clocks where the turnover changed the gear act, sites"] += int((turned & top).sum())
            st[f"{name}: the turnover changed the gear off the top, sites"] += int((turned & ~top).sum())
            end_is_gear = eq(e[0], a1) & eq(e[1], b1) & eq(e[2], r1)
            st[f"{name}: the end of tick = the gear act (off the top), sites"] += int((end_is_gear & ~top).sum())
            st[f"{name}: the end of tick, off the top, sites"] += int((~top).sum())
            rec[name] = {"start": [ints(a), ints(b), ints(r)], "F": ints(F),
                         "gear": [ints(ah), ints(bh), ints(rh)], "end": [ints(e[0]), ints(e[1]), ints(e[2])]}
        # the turnover's trigger, recomputed from the time gear's three notches (clock.turnover): the weak maximum
        # X_b <= X_n >= X_n'' with one strict, or a notch below the bottom X_f (the stretch at the load -Gamma)
        xf = readings.bottom(c)
        x0, x1, x2 = Xb, Xn, cur["x2"]
        top_mine = ((x0 <= x1) & (x2 <= x1) & ((x0 < x1) | (x2 < x1))) | (x0 < xf) | (x2 < xf)
        st["top: the weak maximum of (X_b, X_n, X_n'') or below the bottom = the head's top, sites"] += int(
            eq(np.asarray(top_mine, dtype=bool), cur["top"]).sum())
        st["top: X_n'' (after the drives and the restore) = X_n' (after the act), sites"] += int(eq(x2, Xn1).sum())
        st["births in the click"] += cur["births"]
        self.records.write(json.dumps(rec) + "\n")
        self.cur = {}


def hook(probe):
    o_imp, o_adv, o_car, o_turn, o_click = T.Tick.impulse, T.Tick.advances, T.Tick.carry, T.Tick.turnover, T.Tick.click
    T.Tick.impulse = lambda self: probe.impulse(self, o_imp)
    T.Tick.advances = lambda self: probe.advances(self, o_adv)
    T.Tick.carry = lambda self: probe.carry(self, o_car)
    T.Tick.turnover = lambda self: probe.turnover(self, o_turn)
    T.Tick.click = lambda self: probe.click(self, o_click)
    return o_imp, o_adv, o_car, o_turn, o_click


def unhook(origs):
    T.Tick.impulse, T.Tick.advances, T.Tick.carry, T.Tick.turnover, T.Tick.click = origs


def m1_run(probe, start, ticks_end):
    """David's M1 beside the head, run on its own: Tensor24's gear on the light from the head's state at the setting,
    no regulator, W+ = W = W_0 = (T div 2) 2 Gamma, every grip g_0 = Gamma 2 rim Gamma^2 G^2 (the head's s R_ij at the
    vacuum, one grip on every Mesh). Per tick: the sites where both gears' notches (a, b) equal the head's at the end of
    the tick, and where (a, b, r) do."""
    W0, grip0 = probe.W0, probe.grip0
    state = [(g[0].copy(), g[1].copy(), g[2].copy()) for g in start]
    notches, whole = [], []
    for end in ticks_end:
        state = [t24_gear(a, b, r, 0, W0, W0, sum(grip0 * (nbr(a, j) - a) for j in range(6))) for (a, b, r) in state]
        ok_n = np.ones(probe.clock.size, dtype=bool)
        ok_w = np.ones(probe.clock.size, dtype=bool)
        for (a, b, r), e in zip(state, end):
            ok_n &= eq(a, e[0]) & eq(b, e[1])
            ok_w &= eq(a, e[0]) & eq(b, e[1]) & eq(r, e[2])
        notches.append(int(ok_n.sum()))
        whole.append(int(ok_w.sum()))
    return W0, grip0, notches, whole


def run_world(label, calibre, piece, ticks):
    path = f"{RECORDS}/head_light_records_{label}.jsonl.gz"
    with gzip.open(path, "wt") as records:
        clock = Clock(calibre, piece)
        probe = Probe(clock, records)
        start0 = snap(probe.light)
        records.write(json.dumps({"world": label, "shape": list(clock.size), "sites": [list(x) for x in np.ndindex(clock.size)],
                                  "rim": clock.rim, "Gamma": clock.full_rate, "key": clock.key, "G": clock.G, "T": clock.teeth,
                                  "seed": piece.get("seed", []),
                                  "setting": {name: [ints(g[0]), ints(g[1]), ints(g[2])] for name, g in zip(GEARS, start0)},
                                  "per tick": "W, Wp (W+), s, spring D per site; grips[spoke][site] R_ij in spoke order "
                                              "+x -x +y -y +z -z; top the turned-over clocks; per gear: start [a, b, r], "
                                              "F the pull, gear [a+, b+, r+] after the gear act, end [now, before, fine] "
                                              "at the tick's end"}) + "\n")
        origs = hook(probe)
        ends = []
        try:
            for _ in range(ticks):
                clock.tick()
                ends.append([(g.now.copy(), g.before.copy(), g.fine.copy()) for g in probe.light.gears])
        finally:
            unhook(origs)
    W0, grip0, m1_notches, m1_whole = m1_run(probe, start0, ends)
    size = int(np.prod(clock.size))
    print(f"== {label}: shape {list(clock.size)} ({size} sites), {ticks} ticks, records {path}")
    print(f"   integers: rim {clock.rim}, Gamma {clock.full_rate}, key T_d {clock.key}, G {clock.G}, T = 6 rim Gamma^2 G^2 = {clock.teeth}")
    print(f"   the setting's light: three now {sorted(set(ints(start0[0][0])))}, three before {sorted(set(ints(start0[0][1])))}, "
          f"twelve now {sorted(set(ints(start0[1][0])))[:9]}{' ...' if len(set(ints(start0[1][0]))) > 9 else ''}")
    for name in probe.lo:
        print(f"   range {name}: [{probe.lo[name]}, {probe.hi[name]}]")
    refused = Counter(e.get("why", e.get("reason", "?")) for e in clock.log if e.get("event") == "refused")
    print(f"   the click: meshes engaged (both ends a whole winding) {clock.counts['met']}, refused by name "
          f"{sum(refused.values())}, births {clock.counts['births']}, unwinds taken {clock.counts['taken']}; "
          f"turnovers {clock.counts['turns']}")
    for key in sorted(probe.stats):
        print(f"   {key}: {probe.stats[key]}")
    first_off = next((t + 1 for t, n in enumerate(m1_notches) if n != size), None)
    print(f"   M1 run on its own beside the head (W+ = W = W_0 = {W0}, every grip g_0 = {grip0}, no regulator, no "
          f"turnover), sites equal to the head's end of tick, per tick:")
    print(f"     notches (a, b) of both gears: {m1_notches}")
    print(f"     (a, b, r) of both gears:      {m1_whole}")
    print(f"     first tick with a site's notches apart: {first_off}")
    return probe.stats, size, ticks, first_off


def main():
    cal_node, piece_node = world_of("world_node.json")
    cal_sea, piece_sea = world_of("world_sea_3.json")
    rim = int(cal_node["integers"]["den"])
    packet = {"lay": "at", "row": 0, "centre": [1, 1, 1], "width": 2, "quanta": 1, "sense": 1, "wave": [rim // 2, 0, 0]}
    worlds = [
        ("node3", cal_node, piece_node, 40),  # the head's smallest test piece: sea, hole and packet on the light
        ("sea3", cal_sea, piece_sea, 30),  # the light's drift alike at every clock
        ("sea_packet3", cal_node, {**piece_node, "seed": [{"lay": "sea", "row": 0}, packet]}, 30),  # both gears
        ("packet3", cal_node, {**piece_node, "seed": [packet]}, 30),  # a weak light alone: under one winding in all
        ("node4", cal_node, {**piece_node, "shape": [4, 4, 4]}, 30),  # the test piece at side 4
        ("vacuum3", cal_node, {**piece_node, "seed": []}, 20),  # nothing laid: the stretch held at Gamma by the turnover
    ]
    print(__doc__.split("Run:")[0].strip())
    print()
    total, rows = Counter(), []
    for label, cal, piece, ticks in worlds:
        stats, size, n, m1_off = run_world(label, cal, piece, ticks)
        rows.append((label, size, n, stats, m1_off))
        for key, v in stats.items():
            total[key] += v
    print("== all worlds")
    for key in sorted(total):
        print(f"   {key}: {total[key]}")
    print()
    print("== the counts, per world (three / twelve where two; every count of sites is site-ticks)")
    head = ("world", "sites", "ticks", "read", "act=formula", "act=T24 gear", "end=act, off top", "end=turnover, top",
            "release/restore/click", "W+=W", "R_ij=R_ji meshes", "M1 apart at tick")
    print("   " + " | ".join(head))

    def two(st, key):
        return f"{st['three: ' + key]}/{st['twelve: ' + key]}"

    for label, size, n, st, m1_off in rows + [("all", "", "", total, "")]:
        other = sum(st[f"{g}: the {w} moved the gear, sites"] for g in GEARS
                    for w in ("release's advance", "stopped restore", "click"))
        cells = (label, size, n, two(st, "sites read"), two(st, "GEAR ACT (a+, b+, r+) = the formula, sites"),
                 two(st, "GEAR ACT = Tensor24's gear(a, b, r, 0, W, W+, s F), sites"),
                 f"{two(st, 'the end of tick = the gear act (off the top), sites')} of {st['three: the end of tick, off the top, sites']}",
                 f"{two(st, 'turned-over clocks where the end = the turnover' + chr(39) + 's formula (b, a, mirror r) / (-b, -a, r), sites')}"
                 f" of {st['three: turned-over clocks, sites']}",
                 other, st["W+ = W, sites (the stretch's two notches summed unchanged)"],
                 f"{st['R: meshes read alike from both ends (R_ij = R_ji), meshes']} of {st['R: meshes, read']}", m1_off)
        print("   " + " | ".join(str(c) for c in cells))


if __name__ == "__main__":
    main()
