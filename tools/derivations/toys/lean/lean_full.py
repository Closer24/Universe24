"""David's local lean Node, complete (the owner's word, 04:4x: run everything, omit nothing). Every act of the law's interval at a generic Node of a fixed state, the engine's exact primitives (core.rule3, core.paces, features.phase, loader.circle), the architecture the toy's.

STATE per Node (fixed, 94 integers): volume row 16 (time line 3, three axis lines 9, four write remainders); light 3; the sign's one row 16 (time line 3, three odd lines 9, four write remainders) + its phase potential line 3; the three lifts' planes 2 senses x 2 lines x 3 = 36; per plane record standing, crossed, beats = 18; proper, closes = 2; the Link factors are read, never held.
ACTS per interval, the same at every Node: the tensions read (the axis parts from the quanta's lines), the Link factors from the two ends; Rule3 on every line at the Node's composed paces, the planes' arrivals turned by the Link phases of the sign's potential and by the odd lines' tangent (the fold); the held writes, one carried division per line (the volume from the forms, its axis lines from the tensions, the sign's time line from the Wronskians, its odd lines from the sign currents); the sign's phase potential stepped; the swap at a weak maximum of the volume's time line (every line exchanged, every remainder complemented); the close: the light's whole quanta met, the one-Link read on the frame's digit lattices, the pick and the whether, the exact take by the frame's shares' fall, the lay of a conjugate pair into the planes; the bodies' closing; the credit with the frame. The run back: every act inverted in the reverse order, the lays and takes from the log.
"""
from __future__ import annotations
import sys, os, json, math
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'src'))  # tools/derivations/toys/lean -> src
from event_universe.core import rule3, paces
from event_universe.core.rule3 import division_forward, carried_division, division_back, wall_of, form_term, link_factor
from event_universe.core.paces import sine_den
from event_universe.loader import circle
from event_universe.features import volume as volform, phase

AXES = ((0, 1), (0, -1), (1, 1), (1, -1), (2, 1), (2, -1))
Z = lambda shape: np.zeros(shape, dtype=object)


def roll(a, axis, side):
    return np.roll(a, -side, axis=axis)  # a[i + side]


def gcd_arr(*arrays):
    out = None
    for a in arrays:
        a = np.asarray(a, dtype=object)
        out = a if out is None else np.vectorize(math.gcd, otypes=[object])(out, a)
    return out


class Line:
    __slots__ = ('now', 'before', 'rem')
    def __init__(self, now, before, rem): self.now, self.before, self.rem = now, before, rem
    def copy(self): return Line(self.now.copy(), self.before.copy(), self.rem.copy())


class Lean:
    def __init__(self, den, cube, gamma=1000, action=36000, unit=16, seed_hole=(0, 0, 0), swap_on=True, link_birth=False):
        self.link_birth = link_birth
        self.den, self.cube, self.gamma, self.T, self.G = den, cube, gamma, action, unit
        self.shape = (cube,) * 3; S = self.shape
        self.lifts = [(p[0], p[1], sine_den(p[1], den)) for p in circle.lift_points(den)]
        self.pairs = [(num, den) for _v, num, _s in self.lifts]
        self.w = wall_of(den, gamma, unit)
        half = self.w // 2
        mk = lambda: Line(Z(S), Z(S), Z(S) + half)
        self.vol = mk(); self.vol_axes = [mk() for _ in range(3)]; self.vol_wr = [Z(S) + action // 2] + [Z(S) + (3 * den * action) // 2 for _ in range(3)]  # the lay's gauge, the half of the wall's lowest factor
        self.light = mk()
        self.sign = mk(); self.sign_axes = [mk() for _ in range(3)]; self.sign_wr = [Z(S) + action // 2 for _ in range(4)]
        self.phi = Line(Z(S), Z(S), Z(S) + 1)  # the phase potential row: the wall 2, the write 2c
        self.planes = [[mk(), mk()] for _ in range(6)]  # record 2s + (0: sense -1, 1: sense +1): [re, im]
        self.standing = [Z(S) for _ in range(6)]; self.crossed = [Z(S) for _ in range(6)]; self.beats = [Z(S) for _ in range(6)]
        self.proper = Z(S); self.closes = Z(S)
        self.interval = 0; self.log = []; self.swap_on = swap_on; self.turns = []; self.stack = []
        drift = math.isqrt(action)
        self.light.now[:] = drift; self.light.now[seed_hole] = 0
        self.vol.now[:] = gamma; self.vol.before[:] = gamma
        self.unit_light = 3 * den * action  # W_c
        self.units = [3 * action * s for _v, _n, s in self.lifts]  # one quantum of a record, 3 T s
        self.A = math.isqrt(action // 2)
        self.vol_pair = (den - den // gamma, den)
        self.X = phase.amplitude(gamma, 63)  # the phase pair's amplitude from the width 63
        seed_pair = phase.seed(self.X, gamma)
        self.orbit_lines = [seed_pair]  # the last pair as lines, for the next act
        self.orbit = [(int(seed_pair[0][0]), int(seed_pair[1][0]))]  # the table of (cos, sin) as plain integers
        self.counts = {'births': 0, 'taken': 0, 'booked': 0, 'body_clicks': 0, 'refused_stop': 0, 'refused_origin': 0, 'refused_lay': 0, 'turns': 0}
        self.max_transient = 0

    # ---- readings at the interval's start
    def content(self): return np.asarray(volform.level_of(self.gamma, self.vol.now), dtype=object)
    def pair_angle(self, n):
        """The integer (cos, sin) pair at the count n along the one orbit from the seed (features/phase), the orbit a table of the toy."""
        n = int(n); s = 1 if n >= 0 else -1; n = abs(n) % 65536  # the toy's orbit capped at 2^16 acts, named
        while len(self.orbit) <= n:
            c, sn = self.orbit_lines[-1]; c, sn = phase.act(c, self.gamma, 1), phase.act(sn, self.gamma, 1)
            self.orbit_lines = [(c, sn)]; self.orbit.append((int(c[0]), int(sn[0])))
        c, sn = self.orbit[n]
        return c, s * sn

    def tensions(self):
        """The axis parts: -num h_a(i) summed over every line of quanta, h_a = now(i-a) now(i+a) - now(i)^2; the axis lines of the volume row carry them (written below); the Link factor from the two ends' axis levels."""
        parts = [Z(self.shape) for _ in range(3)]
        lines = [(self.light, self.den)] + [(l, self.pairs[r // 2][0]) for r in range(6) for l in self.planes[r]]
        for line, num in lines:
            for a in range(3):
                if os.environ.get('LEAN_FORMER_TENSION'):  # the former reading, kept by name: -weight h_a, h_a = now(i-a) now(i+a) - now(i)^2
                    h = roll(line.now, a, -1) * roll(line.now, a, 1) - line.now * line.now; parts[a] = parts[a] - num * h
                else:  # The stress is the Links' (decided 2026-10-23): weight x (now(i+a) - now(i-a))^2, read at the doubled wall
                    d = roll(line.now, a, 1) - roll(line.now, a, -1); parts[a] = parts[a] + num * d * d
        return parts

    def link_factors(self):
        if os.environ.get('LEAN_FLAT_FACTORS'):  # a diagnostic switch of the toy: every Link factor G^2 (the vacuum's)
            return tuple(Z(self.shape) + self.G * self.G for _ in AXES)
        found = []
        for axis, side in AXES:
            aa_i = self.vol_axes[axis].now; aa_j = roll(aa_i, axis, side)
            t = (aa_i + aa_j + 1) // 2
            found.append(np.vectorize(lambda tt: int(link_factor(self.gamma, self.G, min(int(tt), self.gamma))), otypes=[object])(t))  # the horizon: a tension at or past Gamma read at the wall, the factor 0 (engine features/read.link_tensions)
        return tuple(found)

    def rule(self, pair, c, factors):
        clock = paces.clock_of(self.gamma, c); pace = paces.link_pace_of(self.gamma, c)
        return rule3.rule_integers(pair[0], pair[1], self.gamma, clock, pace, factors, self.G)

    # ---- the step of one line and of one plane
    def step_line(self, line, r, direction=1):
        total = r.self_coefficient * line.now - r.wall * line.before
        for (axis, side), reach in zip(AXES, r.reaches):
            total = total + reach * roll(line.now, axis, side)
        self.max_transient = max(self.max_transient, int(np.max(np.vectorize(lambda v: abs(int(v)).bit_length(), otypes=[object])(total))))
        nxt, rem = carried_division(total, r.wall, line.rem, direction)
        return Line(nxt, line.now, rem), total

    def frames(self, phi_rem):
        """The frame signs per Port: +1 where the two ends' frame bits (the phase row's remainder at the wall 2, complemented at every swap) agree, -1 where they differ; there the neighbour's plane is read conjugated and its count negated (ALGEBRA.md, The swap at the top, the frame clause)."""
        return [1 - 2 * (phi_rem ^ roll(phi_rem, axis, side)) for axis, side in AXES]

    def step_plane(self, re, im, r, phases, odd, frames=None):
        """The fold: each Port's arrival (read in the Node's frame) turned by the Link's phase (cos, sin) over X and by the odd line's tangent triple (W^2 - n^2, 2 W n) over (W^2 + n^2), W = 4 Gamma, one rounding per Link per part."""
        Wl = 4 * self.gamma
        tot_re = r.self_coefficient * re.now - r.wall * re.before
        tot_im = r.self_coefficient * im.now - r.wall * im.before
        for port, ((axis, side), reach) in enumerate(zip(AXES, r.reaches)):
            re_j, im_j = roll(re.now, axis, side), roll(im.now, axis, side)
            if frames is not None: im_j = frames[port] * im_j
            c, s = phases[port]  # arrays of (cos, sin) over X per Node
            n = odd[axis]  # the odd line on the Link: the two ends' mean floored once, signed by the Port's side (antisymmetric: one number read from both ends)
            n = side * ((n + roll(n, axis, side)) // 2)
            tc, ts, tw = Wl * Wl - n * n, 2 * Wl * n, Wl * Wl + n * n
            # the turned arrival z' = z e^{i theta} e^{i phi}: first the phase pair over X, then the tangent triple over tw
            a_re = (c * re_j - s * im_j); a_im = (s * re_j + c * im_j)
            a_re, a_im = (2 * a_re + self.X) // (2 * self.X), (2 * a_im + self.X) // (2 * self.X)
            b_re = (tc * a_re - ts * a_im); b_im = (ts * a_re + tc * a_im)
            b_re, b_im = (2 * b_re + tw) // (2 * tw), (2 * b_im + tw) // (2 * tw)
            tot_re = tot_re + reach * b_re; tot_im = tot_im + reach * b_im
        nre, rre = carried_division(tot_re, r.wall, re.rem); nim, rim = carried_division(tot_im, r.wall, im.rem)
        return Line(nre, re.now, rre), Line(nim, im.now, rim)

    def centred_count(self, cphi):
        """The Node's centred count K = Phi_next - Phi_before = 2 (Phi_now - Phi_before) + c, twice the trapezoid sum of the clocked potential to the triple's centre (ALGEBRA.md, The swap at the top, the phase hand's M23; the former toy read Phi_i - Phi_j, one integration too many, and pumped)."""
        return 2 * (self.phi.now - self.phi.before) + cphi

    def link_phases(self, frames=None, K=None):
        """The Link's count n_ij = K_i - f_ij K_j (the two ends' centred counts; f_ij the frame sign, the neighbour's count negated where the frames differ) and its (cos, sin) pair over X."""
        found = []
        if K is None: K = self.phi.now
        for port, (axis, side) in enumerate(AXES):
            n = K - (1 if frames is None else frames[port]) * roll(K, axis, side)
            pairs = np.vectorize(self.pair_angle, otypes=[object, object])(n)
            found.append((pairs[0], pairs[1]))
        return found

    def share(self, line, r, pace=None):
        """The conserved form's term at the Node in the current's units over 2 p_i^2 G^2 (share.share without the frame's halves): [w (now^2 + before^2) - S now before - now SUM_j R_j before_j] div (2 p_i^2 G^2)."""
        link = Z(self.shape); shared = Z(self.shape)
        for (axis, side), reach in zip(AXES, r.reaches):
            b_j, n_j = roll(line.before, axis, side), roll(line.now, axis, side)
            link = link + reach * b_j
            shared = shared + reach * (line.before - b_j) * (line.now + n_j)
        found = form_term(r.self_coefficient, r.wall, line.now, line.before) - line.now * link
        if os.environ.get('LEAN_NODE_SHARE'):  # the former toy's reading: the Node's own term alone over 2 p^2 G^2
            pace = paces.link_pace_of(self.gamma, self.start_content) if pace is None else pace; sq = pace * pace
            return np.asarray(division_forward(found, 2 * sq * self.G * self.G + (sq == 0), 0)[0])
        found = found + found - shared  # the frame's term: the Links' products shared half and half between a Link's two ends (engine share.share, halves 2)
        pace = paces.link_pace_of(self.gamma, self.start_content) if pace is None else pace; sq = pace * pace
        wall = 4 * sq * self.G * self.G + (sq == 0)
        return np.asarray(division_forward(found, wall, 0)[0])

    # ---- one interval forward
    def step(self):
        self.interval += 1
        c = self.content(); self.start_content = c
        p0 = paces.clock_of(self.gamma, c)
        self.proper = self.proper + p0
        factors = self.link_factors(); self.start_factors = factors
        frames = self.frames(self.phi.rem); self.start_frames = frames
        cphi = paces.rounded(self.sign.now * p0, self.gamma)  # the clocked potential at the level now
        phases = self.link_phases(frames, self.centred_count(cphi)); odd = [l.now for l in self.sign_axes]
        if os.environ.get('LEAN_NO_PHASE'):  # a diagnostic switch of the toy: the fold off (the pair (X, 0), the odd lines 0)
            phases = [(Z(self.shape) + self.X, Z(self.shape)) for _ in AXES]; odd = [Z(self.shape) for _ in range(3)]
        if os.environ.get('LEAN_NO_PHI'): phases = [(Z(self.shape) + self.X, Z(self.shape)) for _ in AXES]  # the phase pair off, the odd tangent on
        if os.environ.get('LEAN_NO_ODD'): odd = [Z(self.shape) for _ in range(3)]  # the odd tangent off, the phase pair on
        self.start_phases, self.start_odd = phases, [o.copy() for o in odd]
        parts = self.tensions()
        start = self.snapshot()
        forms = Z(self.shape); W = Z(self.shape); J = [Z(self.shape) for _ in range(3)]
        new_planes = []
        for s_, pair in enumerate(self.pairs):
            r = self.rule(pair, c, factors)
            for sense in (0, 1):
                re, im = self.planes[2 * s_ + sense]
                nre, nim = self.step_plane(re, im, r, phases, odd, frames)
                forms = forms + (re.now * re.now - nre.now * re.before) + (im.now * im.now - nim.now * im.before)
                W = W + (nre.now * nim.before - nim.now * nre.before)
                for a in range(3):  # the sign current J_a = Im(conj z (z_{+a} - z_{-a})) from the start's levels, the neighbours read in the Node's frame
                    fp, fm = frames[2 * a], frames[2 * a + 1]
                    dz_re = roll(re.now, a, 1) - roll(re.now, a, -1); dz_im = fp * roll(im.now, a, 1) - fm * roll(im.now, a, -1)
                    J[a] = J[a] + (re.now * dz_im - im.now * dz_re)
                new_planes.append([nre, nim])
        r_l = self.rule((self.den, self.den), c, factors)
        light, _ = self.step_line(self.light, r_l); forms = forms + (self.light.now * self.light.now - light.now * self.light.before)
        sign, _ = self.step_line(self.sign, r_l); sign_axes = [self.step_line(l, r_l)[0] for l in self.sign_axes]
        r_v = self.rule(self.vol_pair, c, factors)
        vol, _ = self.step_line(self.vol, r_v); vol_axes = [self.step_line(l, r_v)[0] for l in self.vol_axes]
        self.planes, self.light, self.sign, self.sign_axes, self.vol, self.vol_axes = new_planes, light, sign, sign_axes, vol, vol_axes
        self.stepped = [[l.copy() for l in r] for r in new_planes]  # the step's output as stepped, kept for the credits' frame (the swap discards it at a turned Node)
        # the held writes, one carried division per line
        trace = (parts[0] + parts[1] + parts[2])  # the stress's trace into the time line's write (the pressure term), the axis lines traceless
        p04 = p0 * p0 * p0 * p0
        q, self.vol_wr[0] = carried_division(4 * start['vol_now'] * (forms * 3 * self.den - trace) * p04, 3 * self.den * self.gamma ** 5 * self.T, self.vol_wr[0]); self.vol.now = self.vol.now + q
        for a in range(3):
            q, self.vol_wr[1 + a] = carried_division((3 * parts[a] - trace) * p04, 2 * self.gamma ** 4 * 3 * self.den * self.T, self.vol_wr[1 + a]); self.vol_axes[a].now = self.vol_axes[a].now + q  # the traceless part at the doubled wall 2 E_s W_c, per proper volume and interval
        q, self.sign_wr[0] = carried_division(2 * W, self.T, self.sign_wr[0]); self.sign.now = self.sign.now + q
        for a in range(3):
            q, self.sign_wr[1 + a] = carried_division(J[a], self.T, self.sign_wr[1 + a]); self.sign_axes[a].now = self.sign_axes[a].now + q
        # the phase potential: c_phi = rounded(L p0 / Gamma) per Node, the row stepped 2 phi_now - phi_before + write (the wall 2)
        wq, rem = carried_division(2 * cphi, 2, self.phi.rem)
        self.phi = Line(2 * self.phi.now - self.phi.before + wq, self.phi.now, rem)
        counters = ([a.copy() for a in self.standing], [a.copy() for a in self.crossed], [a.copy() for a in self.beats])
        # the swap at the top
        self.swap(start)
        # the close
        log_from = len(self.log)
        self.close(start)
        self.start = start
        self.stack.append({'turned': self.turned.copy(), 'counters': counters, 'log_from': log_from, 'p0': p0})

    def snapshot(self):
        return {'vol_now': self.vol.now.copy(), 'vol_before': self.vol.before.copy(), 'sign_now': self.sign.now.copy(),
                'planes': [[l.copy() for l in r] for r in self.planes], 'light': self.light.copy(), 'content': self.start_content,
                'held': [l.copy() for l in self.all_lines()], 'held_wr': [w.copy() for w in self.vol_wr + self.sign_wr]}

    def is_im(self):
        """Which of all_lines() are the planes' im lines (conjugated at a turned Node)."""
        n_plain = len(self.all_lines()) - 12
        return [False] * n_plain + [k % 2 == 1 for k in range(12)]

    def floor(self):
        return int(np.asarray(volform.volume_of(self.gamma, np.array([-self.gamma], dtype=object)), dtype=object).reshape(-1)[0])

    def write_walls(self):
        return [3 * self.den * self.gamma ** 5 * self.T] + [2 * self.gamma ** 4 * 3 * self.den * self.T] * 3 + [self.T] * 4

    def all_lines(self):
        return [self.vol, *self.vol_axes, self.light, self.sign, *self.sign_axes, self.phi, *[l for r in self.planes for l in r]]

    def swap(self, start):
        """The swap at the top (ALGEBRA.md, the fifth act): the weak maximum X0 <= X1 >= X2 with one strict on (the held before, the held now, the now after the writes), or the floor (X0 or X2 below X_f); the turned Node ends the interval at the state it started from with every line's two levels exchanged and every remainder complemented at its wall, the step's output discarded; the planes' im lines conjugated (im to -im, the remainder complemented again); the write remainders complemented from the held ones."""
        x0, x1, x2 = start['vol_before'], start['vol_now'], self.vol.now
        top = np.vectorize(lambda a, b, c: 1 if (int(a) <= int(b) and int(c) <= int(b) and (int(a) < int(b) or int(c) < int(b))) else 0, otypes=[object])(x0, x1, x2) == 1
        xf = self.floor()
        top = top | (np.vectorize(lambda a, c: 1 if (int(a) < xf or int(c) < xf) else 0, otypes=[object])(x0, x2) == 1)
        self.turned = top
        if not self.swap_on or not top.any(): return
        self.counts['turns'] += int(top.sum()); self.turns.append((self.interval, int(top.sum())))
        self.exchange(top, start['held'], start['held_wr'])

    def exchange(self, top, held, held_wr):
        """The act at the Nodes `top`: every line set to the held (pre-state) line exchanged and complemented; an involution with the state it leaves (the same act on the post-state gives the pre-state)."""
        for line, h, im in zip(self.all_lines(), held, self.is_im()):
            wall = 2 if line is self.phi else self.w
            sgn = -1 if im else 1
            line.now, line.before, line.rem = np.where(top, sgn * h.before, line.now), np.where(top, sgn * h.now, line.before), np.where(top, h.rem if im else wall - 1 - h.rem, line.rem)
        for wr, h, wall in zip(self.vol_wr + self.sign_wr, held_wr, self.write_walls()):
            wr[:] = np.where(top, wall - 1 - h, wr)

    # ---- the close
    def frame_nodes(self, at):
        return [at] + [tuple((at[a] + (side if a == axis else 0)) % self.cube for a in range(3)) for axis, side in AXES]

    def read_number(self, at, rules):
        """The one-Link read: every line's remainder at the Node on the Node's own lattice F_i = gcd(w, D_i, R_i1..R_i6) and at each neighbour on the Link's lattice gcd(w, R_ji), the digit r div F, the base w div F + 1, sorted by value, composed modulo M = unit x 3 (the carry); the three refusals by name."""
        M = self.unit_light * 3
        nodes = self.frame_nodes(at); digits = []; origin = True; coarse = True
        half = self.w // 2
        for line, r in rules:
            F0 = math.gcd(self.w, int(r.mass[at]) if np.ndim(r.mass) else int(r.mass), *[int(np.asarray(x)[at]) for x in r.reaches])
            for k, n in enumerate(nodes):
                F = F0 if k == 0 else math.gcd(self.w, int(np.asarray(r.reaches[k - 1])[n]))
                rem = int(line.rem[n]); values = self.w // F
                origin = origin and rem in (half - 1, half); coarse = coarse and values <= 3
                digits.append((rem // F, values + 1))
        if origin: self.counts['refused_origin'] += 1; return None
        if coarse: return None
        digits.sort(); carry = 0
        for d, b in digits: carry = (carry * b + d) % M
        return carry

    def take(self, at, walls, r_light, line):
        """The exact take at the Node: the light's now moved toward its before by the least count of levels at which the Node's share falls by the walls. The share's term at the Node is w (now^2 + before^2) - S now before - now L, L = SUM_j R_j before_j, over W_i = 2 p_i^2 G^2; moving now by t s (t the direction) its fall is f(s) = [w (now^2 - (now + t s)^2) - t s (S before + L)] div W_i, an exact quadratic in s: the least s with f(s) >= walls by one integer root (largest_below), checked exactly at s - 1, s, s + 1; refused by name where the full move cannot pay."""
        now, before = int(line.now[at]), int(line.before[at])
        if now == before: return None, 0
        t = 1 if before > now else -1
        S = int(np.asarray(r_light.self_coefficient)[at]); w = int(r_light.wall)
        L = 0
        for (axis, side), reach in zip(AXES, r_light.reaches):
            n = tuple((at[a] + (side if a == axis else 0)) % self.cube for a in range(3))
            L += int(np.asarray(reach)[at]) * int(line.before[n])
        pace = int(np.asarray(paces.link_pace_of(self.gamma, self.start_content), dtype=object)[at]); Wi = 2 * pace * pace * self.G * self.G + (1 if pace == 0 else 0)
        def fall(s_):
            return (w * (now * now - (now + t * s_) ** 2) - t * s_ * (S * before + L)) // Wi
        dist = abs(now - before)
        full = fall(dist)
        if full < walls: return None, full
        # f(s) Wi = -w s^2 - s (2 w now t + t (S before + L)) =: a s^2 + b s, a = -w, b = -(2 w now + S before + L) t; least s with a s^2 + b s >= walls Wi
        a = -w; bcoef = -(2 * w * now + S * before + L) * t; target = walls * Wi
        disc = bcoef * bcoef + 4 * a * target
        if disc < 0: cands = [dist]
        else:
            root = math.isqrt(disc); s1 = (bcoef - root) // (-2 * a) if a < 0 else (-bcoef + root) // (2 * a)
            cands = sorted({max(1, s1 - 1), max(1, s1), max(1, s1 + 1), max(1, s1 + 2)})
        for s_ in cands:
            if s_ <= dist and fall(s_) >= walls: return s_, fall(s_)
        for s_ in range(1, dist + 1):  # the exact guard, reached only where the root misses
            if fall(s_) >= walls: return s_, fall(s_)
        return dist, full

    def close(self, start):
        c = self.start_content; factors = self.link_factors()
        r_light = self.rule((self.den, self.den), c, factors)
        rules = [(start['light'], r_light), (self.sign, r_light), (self.vol, self.rule(self.vol_pair, c, factors))]
        for s_, pair in enumerate(self.pairs):
            r = self.rule(pair, c, factors)
            for sense in (0, 1):
                rules += [(start['planes'][2 * s_ + sense][0], r), (start['planes'][2 * s_ + sense][1], r)]
        pace = paces.link_pace_of(self.gamma, c)
        sh = self.share(start['light'], r_light, pace)
        owns = []  # each record's standing share at the interval's start (the lay's one comparison, take.below_quantum)
        for rec in range(6):
            r = self.rule(self.pairs[rec // 2], c, factors); re0, im0 = start['planes'][rec]
            owns.append(self.share(re0, r, pace) + self.share(im0, r, pace))
        born = []
        frozen = np.asarray(pace, dtype=object) == 0 if np.ndim(pace) else np.zeros(self.shape, dtype=bool)
        for at in np.ndindex(*self.shape):
            if frozen[at]: continue  # a frozen Node's share is not read (ALGEBRA.md, The horizon; engine share.frozen)
            whole, rest = divmod(int(sh[at]), self.unit_light)
            if whole >= 2:
                number = self.read_number(at, rules)
                if number is None: continue
                born.append((at, (number // self.unit_light) % 3))
            elif whole == 1 and rest > 0:
                number = self.read_number(at, rules)
                if number is None: continue
                if number % self.unit_light < rest: born.append((at, (number // self.unit_light) % 3))
        for at, s_ in born:
            walls = 2 * self.units[s_]
            nb = ((at[0] + 1) % self.cube, at[1], at[2]) if self.link_birth else at
            # the lay refused by name where a child's family already stands above one quantum at its Node (ALGEBRA.md, The click writes on the lattice (b) and (d), the undepleted beam; engine take.below_quantum, meeting_board.refused_by)
            if int(owns[2 * s_][at]) > self.units[s_] or int(owns[2 * s_ + 1][nb]) > self.units[s_]:
                self.counts['refused_lay'] += 1; self.log.append({'event': 'refused', 'i': self.interval, 'node': list(at), 'cause': 'lay', 'standing': int(owns[2 * s_][at]), 'unit': self.units[s_]}); continue
            levels, fall = self.take(at, walls, r_light, self.light)
            if levels is None:
                self.counts['refused_stop'] += 1; self.log.append({'event': 'refused', 'i': self.interval, 'node': list(at), 'cause': 'stop', 'fall': fall, 'walls': walls}); continue
            now = int(self.light.now[at]); before = int(self.light.before[at]); toward = 1 if before > now else -1
            self.light.now[at] = now + toward * levels
            A = self.lay_amplitude(s_, at, c, factors, pace)
            for sense, rec, where in ((-1, 2 * s_, at), (1, 2 * s_ + 1, nb)):
                re, im = self.planes[rec]; re.now[where] = re.now[where] + A; im.before[where] = im.before[where] + sense * A
            self.counts['births'] += 1; self.counts['taken'] += fall; self.counts['booked'] += walls; self.closes[at] += 1
            self.log.append({'event': 'birth', 'i': self.interval, 'node': list(at), 'line_pair': s_, 'senses': [-1, 1], 'taken': fall, 'booked': walls, 'levels': levels, 'light_now_was': now, 'proper': int(self.proper[at]), 'content': int(c[at]), 'amplitude': A})
        born_nodes = {at for at, _ in born}
        if self.link_birth:  # both ends of a Link birth are the birth's Nodes
            born_nodes |= {((at[0] + 1) % self.cube, at[1], at[2]) for at, _ in born}
        # the bodies' closing: a record at a whole quantum of its own unit through one period of its re line's upward crossings
        for rec in range(6):
            s_ = rec // 2; r = self.rule(self.pairs[s_], c, factors)
            own = owns[rec]
            standing_now = np.vectorize(lambda v: 1 if int(v) >= self.units[s_] else 0, otypes=[object])(own)
            self.standing[rec] = np.where(standing_now == 1, self.standing[rec] + 1, 0)
            re = self.planes[rec][0]
            upward = np.vectorize(lambda b, n: 1 if (int(b) < 0 <= int(n)) else 0, otypes=[object])(re.before, re.now)
            counting = np.vectorize(lambda v: 1 if int(v) > 0 else 0, otypes=[object])(self.crossed[rec])
            self.beats[rec] = np.where((upward == 1) & (counting == 1), self.crossed[rec], self.beats[rec])
            self.crossed[rec] = np.where(upward == 1, 1, np.where(counting == 1, self.crossed[rec] + 1, 0))
            closing = np.vectorize(lambda st, bt: 1 if (int(bt) > 0 and int(st) >= int(bt)) else 0, otypes=[object])(self.standing[rec], self.beats[rec])
            for at in zip(*np.nonzero(closing == 1)):
                at = tuple(int(x) for x in at)
                if at in born_nodes or frozen[at]: continue
                levels, fall = self.take(at, self.units[s_], r_light, self.light)
                if levels is None:
                    self.counts['refused_stop'] += 1; self.standing[rec][at] = 0; continue
                now = int(self.light.now[at]); before = int(self.light.before[at]); toward = 1 if before > now else -1
                self.light.now[at] = now + toward * levels
                self.counts['body_clicks'] += 1; self.closes[at] += 1; self.standing[rec][at] = 0
                self.log.append(self.credit(rec, at, start, fall, levels, now))

    def lay_amplitude(self, s_, at, c, factors, pace):
        """The lay of one quantum: the child's record laid at the Node with the least amplitude A at which its own share reads one quantum of its unit at the Node's paces, (2 D + SUM_j R_j) A^2 >= unit x 4 p^2 G^2 (the frame share's term of a lone record with now = before = A; ALGEBRA.md, the lay of the record out whole); the former toy laid isqrt(T / 2) for every species."""
        if os.environ.get('LEAN_FIXED_A'): return self.A
        r = self.rule(self.pairs[s_], c, factors)
        D = 2 * int(np.asarray(r.wall)) - int(np.asarray(r.self_coefficient)[at]) - sum(int(np.asarray(x)[at]) for x in r.reaches)  # D from S = 2 w - D - SUM R
        C = 2 * D + sum(int(np.asarray(x)[at]) for x in r.reaches)
        pc = int(np.asarray(pace, dtype=object)[at]); target = self.units[s_] * 4 * pc * pc * self.G * self.G
        if C <= 0: return self.A
        A = math.isqrt(target // C)
        while C * A * A < target: A += 1
        return A

    def credit(self, rec, at, start, fall, levels, light_was):
        re, im = self.planes[rec]; re0, im0 = start['planes'][rec]
        nodes = self.frame_nodes(at)[1:]
        W = int(re.now[at] * im.before[at] - im.now[at] * re.before[at])
        sre, sim = self.stepped[rec]
        frame = {'re_now': int(re.now[at]), 'im_now': int(im.now[at]), 're_before': int(re.before[at]), 'im_before': int(im.before[at]), 're_stepped': int(sre.now[at]), 'im_stepped': int(sim.now[at]), 're_start_now': int(re0.now[at]), 're_start_before': int(re0.before[at]), 'im_start_now': int(im0.now[at]), 'im_start_before': int(im0.before[at]),
                 're_neighbours_start': [int(re0.now[n]) for n in nodes], 'im_neighbours_start': [int(im0.now[n]) for n in nodes]}
        frame['phases'] = [[int(c[at]), int(sn[at])] for c, sn in self.start_phases]
        frame['frames'] = [int(f[at]) for f in self.start_frames]
        frame['odd'] = [int(side * ((self.start_odd[axis][at] + self.start_odd[axis][n]) // 2)) for (axis, side), n in zip(AXES, nodes)]
        frame['X'] = self.X
        frame['factors'] = [int(f[at]) for f in self.start_factors]
        return {'event': 'credit', 'i': self.interval, 'node': list(at), 'proper': int(self.proper[at]), 'closes': int(self.closes[at]), 'content': int(self.start_content[at]), 'line': rec, 'sense': 1 if W > 0 else -1 if W < 0 else 0,
                'beat': int(self.beats[rec][at]), 'frame': frame, 'taken': fall, 'levels': levels, 'light_now_was': light_was, 'sign_level': int(self.sign.now[at]), 'turned': bool(self.turned[at])}

    def back_line(self, st, r):
        """Rule3's inverse by the division back (core.rule3.division_back): the known part S now + SUM R m, with the remainder after, gives the quotient next + before and the remainder before (the -w before term an exact multiple of the wall); before = quotient - next."""
        known = r.self_coefficient * st.before
        for (axis, side), reach in zip(AXES, r.reaches):
            known = known + reach * roll(st.before, axis, side)
        quotient, rem = division_back(known, r.wall, st.rem)
        return Line(st.before, quotient - st.now, rem), known

    def back_plane(self, re, im, r, phases, odd, frames=None):
        """The fold's inverse by the same division back: the known part with the turned arrivals from the start's levels (the before slots), the neighbours read in the Node's frame."""
        Wl = 4 * self.gamma
        k_re = r.self_coefficient * re.before; k_im = r.self_coefficient * im.before
        for port, ((axis, side), reach) in enumerate(zip(AXES, r.reaches)):
            re_j, im_j = roll(re.before, axis, side), roll(im.before, axis, side)
            if frames is not None: im_j = frames[port] * im_j
            c, s_ = phases[port]; n = odd[axis]; n = side * ((n + roll(n, axis, side)) // 2)
            tc, ts, tw = Wl * Wl - n * n, 2 * Wl * n, Wl * Wl + n * n
            a_re = (c * re_j - s_ * im_j); a_im = (s_ * re_j + c * im_j)
            a_re, a_im = (2 * a_re + self.X) // (2 * self.X), (2 * a_im + self.X) // (2 * self.X)
            b_re = (tc * a_re - ts * a_im); b_im = (ts * a_re + tc * a_im)
            b_re, b_im = (2 * b_re + tw) // (2 * tw), (2 * b_im + tw) // (2 * tw)
            k_re = k_re + reach * b_re; k_im = k_im + reach * b_im
        q_re, r_re = division_back(k_re, r.wall, re.rem); q_im, r_im = division_back(k_im, r.wall, im.rem)
        return Line(re.before, q_re - re.now, r_re), Line(im.before, q_im - im.now, r_im)

    def step_back(self):
        """One interval back: the close undone from the log (the lays removed, the light restored), the swap undone at the turned Nodes (an involution), the phase row back, the writes undone by the division back from the start's levels (every start level is a before slot), Rule3 inverted on every line."""
        frame = self.stack.pop()
        # the close undone, in the reverse order of its lines
        for entry in reversed(self.log[frame['log_from']:]):
            at = tuple(entry['node'])
            if entry['event'] == 'birth':
                s_ = entry['line_pair']; nb = ((at[0] + 1) % self.cube, at[1], at[2]) if self.link_birth else at
                for sense, rec, where in ((-1, 2 * s_, at), (1, 2 * s_ + 1, nb)):
                    A = entry.get('amplitude', self.A)
                    re, im = self.planes[rec]; re.now[where] = re.now[where] - A; im.before[where] = im.before[where] - sense * A
                self.light.now[at] = entry['light_now_was']; self.closes[at] -= 1
            elif entry['event'] == 'credit':
                self.light.now[at] = entry['light_now_was']; self.closes[at] -= 1
        del self.log[frame['log_from']:]
        self.standing, self.crossed, self.beats = frame['counters']  # the readings restored
        # the swap's inverse, part one: the post-state kept; at a turned Node the before slot holds the start's now (negated on an im line), so every start level is read from the before slots after the im lines' sign is restored there
        top = frame['turned']
        post = [l.copy() for l in self.all_lines()]; post_wr = [w.copy() for w in self.vol_wr + self.sign_wr]
        for line, im in zip(self.all_lines(), self.is_im()):
            if im: line.before = np.where(top, -line.before, line.before)
        start_bits = np.where(top, 1 - self.phi.rem, self.phi.rem)  # the frame bits at the start: complemented at the turned Nodes
        frames = self.frames(start_bits)
        # the start's readings from the before slots
        X_start = self.vol.before; c = np.asarray(volform.level_of(self.gamma, X_start), dtype=object); self.start_content = c
        p0 = paces.clock_of(self.gamma, c); p04 = p0 * p0 * p0 * p0
        self.proper = self.proper - p0
        # the phase row back: cphi from the sign's start level and p0; phi_before = 2 phi_now - phi_next + wq
        cphi = paces.rounded(self.sign.before * p0, self.gamma)
        wq, rem = division_back(2 * cphi, 2, self.phi.rem)
        phi_now = self.phi.before; phi_before = 2 * phi_now - self.phi.now + wq
        # at a turned Node the post-state is the pre-state exchanged: its before at the start is the post's now (K at the start needs it at every Node, turned neighbours included)
        phi_before = np.where(top, self.phi.now, phi_before); rem = np.where(top, 1 - self.phi.rem, rem)
        self.phi = Line(phi_now, phi_before, rem)
        # the tensions and factors at the start from the before slots
        start_lines = [(Line(self.light.before, None, None), self.den)] + [(Line(l.before, None, None), self.pairs[r // 2][0]) for r in range(6) for l in self.planes[r]]
        parts = [Z(self.shape) for _ in range(3)]
        for line, num in start_lines:
            for a in range(3):
                if os.environ.get('LEAN_FORMER_TENSION'):
                    h = roll(line.now, a, -1) * roll(line.now, a, 1) - line.now * line.now; parts[a] = parts[a] - num * h
                else:
                    d = roll(line.now, a, 1) - roll(line.now, a, -1); parts[a] = parts[a] + num * d * d
        trace = parts[0] + parts[1] + parts[2]
        # the axis writes undone (their numerators from the start levels), then the factors at the start
        for a in range(3):
            q, self.vol_wr[1 + a] = division_back((3 * parts[a] - trace) * p04, 2 * self.gamma ** 4 * 3 * self.den * self.T, self.vol_wr[1 + a]); self.vol_axes[a].now = self.vol_axes[a].now - q
        factors = self.link_factors()  # from the axis lines at the start (their now the start's now after the write undone? the factors read the axis lines' START now: the before slot)
        factors = []
        for axis, side in AXES:
            aa_i = self.vol_axes[axis].before; aa_j = roll(aa_i, axis, side); t = (aa_i + aa_j + 1) // 2
            factors.append(np.vectorize(lambda tt: int(link_factor(self.gamma, self.G, min(int(tt), self.gamma))), otypes=[object])(t))
        factors = tuple(factors)
        # the sign's writes undone: W from the stepped planes at the Node (now and before slots), J from the start's levels (the before slots) in the Node's frame
        J = [Z(self.shape) for _ in range(3)]; W = Z(self.shape)
        for rec in range(6):
            re, im = self.planes[rec]
            W = W + (re.now * im.before - im.now * re.before)
            for a in range(3):
                fp, fm = frames[2 * a], frames[2 * a + 1]
                dz_re = roll(re.before, a, 1) - roll(re.before, a, -1); dz_im = fp * roll(im.before, a, 1) - fm * roll(im.before, a, -1)
                J[a] = J[a] + (re.before * dz_im - im.before * dz_re)
        for a in range(3):
            q, self.sign_wr[1 + a] = division_back(J[a], self.T, self.sign_wr[1 + a]); self.sign_axes[a].now = self.sign_axes[a].now - q
        q, self.sign_wr[0] = division_back(2 * W, self.T, self.sign_wr[0]); self.sign.now = self.sign.now - q
        # the planes inverted at the start's rule, phases (phi restored) and odd lines (the sign axes' start now = their before slots)
        phases = self.link_phases(frames, self.centred_count(cphi))
        odd = [l.before for l in self.sign_axes]
        forms = Z(self.shape)
        for s_, pair in enumerate(self.pairs):
            r = self.rule(pair, c, factors)
            for sense in (0, 1):
                re, im = self.planes[2 * s_ + sense]
                bre, bim = self.back_plane(re, im, r, phases, odd, frames)
                forms = forms + (bre.now * bre.now - re.now * bre.before) + (bim.now * bim.now - im.now * bim.before)
                self.planes[2 * s_ + sense] = [bre, bim]
        r_l = self.rule((self.den, self.den), c, factors)
        light_b, _ = self.back_line(self.light, r_l); forms = forms + (light_b.now * light_b.now - self.light.now * light_b.before)
        self.light = light_b
        self.sign, _ = self.back_line(self.sign, r_l); self.sign_axes = [self.back_line(l, r_l)[0] for l in self.sign_axes]
        # the volume's write undone, then its lines inverted
        q, self.vol_wr[0] = division_back(4 * X_start * (forms * 3 * self.den - trace) * p04, 3 * self.den * self.gamma ** 5 * self.T, self.vol_wr[0]); self.vol.now = self.vol.now - q
        r_v = self.rule(self.vol_pair, c, factors)
        self.vol, _ = self.back_line(self.vol, r_v); self.vol_axes = [self.back_line(l, r_v)[0] for l in self.vol_axes]
        # the swap's inverse, part two: at the turned Nodes the same act on the post-state gives the pre-state (the exchange and the complement again, the im lines' conjugation again)
        if self.swap_on and top.any(): self.exchange(top, post, post_wr)
        self.interval -= 1

    def census(self):
        arrays = [a for l in self.all_lines() for a in (l.now, l.before, l.rem)] + self.vol_wr + self.sign_wr + self.standing + self.crossed + self.beats + [self.proper, self.closes]
        bits = max(int(np.max(np.vectorize(lambda v: abs(int(v)).bit_length(), otypes=[object])(a))) for a in arrays)
        return len(arrays), bits

    def state_bytes(self):
        return b''.join(np.asarray(a, dtype=object).astype(str).tobytes() for l in self.all_lines() for a in (l.now, l.before, l.rem)) + b''.join(np.asarray(a).astype(str).tobytes() for a in self.vol_wr + self.sign_wr)


if __name__ == '__main__':
    sys.set_int_max_str_digits(0)
    den, cube, intervals, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    link = len(sys.argv) > 5 and sys.argv[5] == 'link'
    b = Lean(den, cube, link_birth=link)
    rows = []; maxbits = 0
    import time; t0 = time.monotonic_ns()
    for t in range(intervals):
        b.step(); n, bits = b.census(); maxbits = max(maxbits, bits)
        if b.interval in (1, 5, 10, 25, 50, 100, 150, 200, 300, 400, 600, 800, 1000, 1200, 1600, 2000, 2400) or b.interval == intervals:
            c = b.content()
            cs = [int(x) for x in c.reshape(-1)]; vs = [int(x) for x in b.vol.now.reshape(-1)]
            energy = sum(int(x) * int(x) for rec in b.planes for l in rec for x in l.now.reshape(-1)); odd_max = max(abs(int(x)) for l in b.sign_axes for x in l.now.reshape(-1)); light_v = max(abs(int(a) - int(bb)) for a, bb in zip(b.light.now.reshape(-1), b.light.before.reshape(-1)))
            # integers only (the owner's word of 05:08): the means as quotients, the clock in milliseconds
            rows.append({'i': b.interval, 'content min/mean/max': [min(cs), sum(cs) // len(cs), max(cs)], 'volume mean': sum(vs) // len(vs), 'births': b.counts['births'], 'body_clicks': b.counts['body_clicks'], 'refused': b.counts['refused_stop'] + b.counts['refused_origin'] + b.counts['refused_lay'], 'refused_lay': b.counts['refused_lay'], 'turns': b.counts['turns'], 'integers': n, 'max bits': maxbits, 'max transient bits': b.max_transient, 'sign level max': max(abs(int(x)) for x in b.sign.now.reshape(-1)), 'planes energy bits': energy.bit_length(), 'tension min/max': [min(int(x) for l in b.vol_axes for x in l.now.reshape(-1)), max(int(x) for l in b.vol_axes for x in l.now.reshape(-1))], 'odd max bits': odd_max.bit_length(), 'light velocity max': light_v, 'milliseconds': (time.monotonic_ns() - t0) // 1000000})
            print(json.dumps(rows[-1]), flush=True)
    json.dump({'den': den, 'cube': cube, 'intervals': intervals, 'lifts': [(list(v), str(num), str(s)) for v, num, s in b.lifts], 'T': b.T, 'gamma': b.gamma, 'G': b.G, 'counts': {k: str(v) for k, v in b.counts.items()}, 'turns': b.turns, 'rows': rows, 'log': b.log}, open(out, 'w'))
    print(json.dumps({'counts': {k: str(v) for k, v in b.counts.items()}}))
