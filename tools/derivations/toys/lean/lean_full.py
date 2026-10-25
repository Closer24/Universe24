"""David's local lean Node, complete (the owner's word, 04:4x: run everything, omit nothing). Every act of the law's interval at a generic Node of a fixed state, the engine's exact primitives (core.rule3, core.paces, features.phase, loader.circle), the architecture the toy's.

STATE per Node (fixed, 95 integers): volume row 16 (time line 3, three axis lines 9, four write remainders); light 3; the sign's one row 16 (time line 3, three odd lines 9, four write remainders) + its phase potential line 3; the three lifts' planes 2 senses x 2 lines x 3 = 36; per plane record standing, crossed, beats = 18; proper, closes = 2; the Link factors are read, never held.
ACTS per interval, the same at every Node: the tensions read (the axis parts from the quanta's lines), the Link factors from the two ends; Rule3 on every line at the Node's composed paces, the planes' arrivals turned by the Link phases of the sign's potential and by the odd lines' tangent (the fold); the held writes, one carried division per line (the volume from the forms, its axis lines from the tensions, the sign's time line from the Wronskians, its odd lines from the sign currents); the sign's phase potential stepped; the swap at a weak maximum of the volume's time line (every line exchanged, every remainder complemented); the close: the light's whole quanta met, the one-Link read on the frame's digit lattices, the pick and the whether, the exact take by the frame's shares' fall, the lay of a conjugate pair into the planes; the bodies' closing; the credit with the frame. The run back: every act inverted in the reverse order, the lays and takes from the log.
"""
from __future__ import annotations
import sys, os, json, math
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'src'))  # tools/derivations/toys/lean -> src
from event_universe.core import rule3, paces
from event_universe.core.rule3 import division_forward, carried_division, division_back, wall_of, form_term, link_factor
from event_universe.core.paces import sine_den
from event_universe.features import volume as volform, phase

AXES = ((0, 1), (0, -1), (1, 1), (1, -1), (2, 1), (2, -1))
Z = lambda shape: np.zeros(shape, dtype=object)


def across(a, port):
    """The one read across a Link: the array's value at the Node beyond the Port (the Node i + e_a side), the torus wrapped; every Link read of the toy passes here (the owner's word of 2026-10-25: the Link's act in one place)."""
    axis, side = AXES[port]
    return np.roll(a, -side, axis=axis)


def link(port, even=(), odd=(), frame_bits=None):
    """The Link's numbers at one Port, read the same from both ends (the owner's word: one generic atomic act of the Link, in the Node): for each `even` array the two ends' sum (symmetric), for each `odd` array the two ends' sum signed by the Port's side (antisymmetric: the other end reads the negative), and the frame sign f_ij = 1 where the two ends' frame bits agree and -1 where they differ (from `frame_bits`)."""
    axis, side = AXES[port]
    evens = [a + across(a, port) for a in even]
    odds = [side * (a + across(a, port)) for a in odd]
    f = None if frame_bits is None else 1 - 2 * (frame_bits ^ across(frame_bits, port))
    return evens, odds, f


def gradient(a, axis):
    """The centred difference of a row's line along an axis, a(i + a) - a(i - a), read through the Link's one read at the two Ports of the axis."""
    return across(a, 2 * axis) - across(a, 2 * axis + 1)


def wronskian(re, im):
    """The plane's bilinear W = re_now im_before - im_now re_before at every Node (the charge density, the sign's source)."""
    return re.now * im.before - im.now * re.before


def plane_current(re, im, frames):
    """The plane's sign current on each axis, J_a = Im(conj z (z(i + a) - z(i - a))) from the levels now, the neighbours' im read in the Node's frame; the three odd lines' source."""
    found = []
    for a in range(3):
        fp, fm = frames[2 * a], frames[2 * a + 1]
        dz_re = gradient(re.now, a); dz_im = fp * across(im.now, 2 * a) - fm * across(im.now, 2 * a + 1)
        found.append(re.now * dz_im - im.now * dz_re)
    return found


def stress_parts(lines, shape):
    """The stress tensor's three diagonal parts from the rows' levels, one act on every line alike: SUM over lines of weight x (gradient along the axis)^2 (the stress is the Links', decided 2026-10-23); `lines` holds (levels, weight) pairs. LEAN_FORMER_TENSION keeps the former reading by name: -weight h_a, h_a = a(i-a) a(i+a) - a(i)^2."""
    parts = [Z(shape) for _ in range(3)]
    for levels, num in lines:
        for a in range(3):
            if os.environ.get('LEAN_FORMER_TENSION'):
                h = across(levels, 2 * a + 1) * across(levels, 2 * a) - levels * levels; parts[a] = parts[a] - num * h
            else:
                d = gradient(levels, a); parts[a] = parts[a] + num * d * d
    return parts


def tensor_parts(parts):
    """A tensor's trace and its traceless diagonal parts: trace = SUM_a parts_a; traceless_a = 3 parts_a - trace (the stress's trace is the time line's, the axis lines traceless)."""
    trace = parts[0] + parts[1] + parts[2]
    return trace, [3 * part - trace for part in parts]


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


WIDTH = 128  # the law's one constant: every integer of the state and of every act's transient within 128 bits


def load_world(path):
    """The two files, read once: the world (shape, intervals, seed) and the universe it names (integers, rows), the universe's path relative to the world's folder."""
    world = json.load(open(path)); folder = os.path.dirname(os.path.abspath(path))
    universe = json.load(open(os.path.join(folder, world['universe'])))
    return universe, world


class Lean:
    @classmethod
    def from_files(cls, path, **kw):
        universe, world = load_world(path)
        return cls(universe, world, **kw)

    def __init__(self, universe, world, swap_on=True, link_birth='current'):
        """The Node from the universe's integers and rows and the world's shape and seed, nothing else (the owner's rule: no number in the code); the rows by kind: the one shape-1 row at (den, den) the massless quanta (light), the shape-2 rows the lifts (planes); the two held rows the law's at every Node, the volume at (den - den div Gamma, den) and the sign at (den, den)."""
        self.link_birth = link_birth  # 'current': the Link close oriented by the light's current F_ij (the law's); True: the + child at the +x end (the label, the negative control of the 48); False: both children at the Node (the former toy)
        ints = universe['integers']
        den, gamma, action, unit = int(ints['den']), int(ints['node_clock']), int(ints['quantum_action']), int(ints['link_unit'])
        shape = tuple(int(x) for x in world['shape'])
        if len(set(shape)) != 1: raise ValueError('the toy runs on a cube: the shape must be [c, c, c]')
        cube = shape[0]
        self.den, self.cube, self.gamma, self.T, self.G = den, cube, gamma, action, unit
        self.shape = (cube,) * 3; S = self.shape
        rows = [(int(r['shape']), (int(r['pair'][0]), int(r['pair'][1]))) for r in universe['rows']]
        light_rows = [pair for shape_, pair in rows if shape_ == 1]
        if len(light_rows) != 1 or light_rows[0] != (den, den): raise ValueError('the universe names one massless shape-1 row at (den, den), the light')
        self.pairs = [pair for shape_, pair in rows if shape_ == 2]
        self.nl = len(self.pairs)
        if self.nl == 0: raise ValueError('the universe names no plane row')
        self.lifts = [(None, num, sine_den(num, den)) for num, _den in self.pairs]  # the legs from the pairs: T sin omega as the universe's circle gives it
        self.w = wall_of(den, gamma, unit)
        half = self.w // 2
        mk = lambda: Line(Z(S), Z(S), Z(S) + half)
        self.vol = mk(); self.vol_axes = [mk() for _ in range(3)]
        self.light = mk()
        self.sign = mk(); self.sign_axes = [mk() for _ in range(3)]
        walls = self.write_walls()  # the write remainders at the lay's gauge, half of each line's wall (the engine rounds half up: a remainder at the half wall carries the same)
        self.vol_wr = [Z(S) + walls[k] // 2 for k in range(4)]; self.sign_wr = [Z(S) + walls[4 + k] // 2 for k in range(4)]; self.light_wr = Z(S) + walls[8] // 2
        self.phi = Line(Z(S), Z(S), Z(S) + 1)  # the phase potential row: the wall 2, the write 2c
        self.planes = [[mk(), mk()] for _ in range(2 * self.nl)]  # record 2s + (0: sense -1, 1: sense +1): [re, im]
        self.standing = [Z(S) for _ in range(2 * self.nl)]; self.crossed = [Z(S) for _ in range(2 * self.nl)]; self.beats = [Z(S) for _ in range(2 * self.nl)]
        self.proper = Z(S); self.closes = Z(S)
        self.light_wr = Z(S) + action // 2  # the massless row's lay remainder at the wall T (W-S1)
        self.interval = 0; self.log = []; self.swap_on = swap_on; self.turns = []; self.stack = []
        self.vol.now[:] = gamma; self.vol.before[:] = gamma
        self.unit_light = 3 * den * action  # W_c
        self.units = [3 * action * s for _v, _n, s in self.lifts]  # one quantum of a record, 3 T s
        self.detectors = []  # the Nodes whose light the record credits (the world names them; a reading, no state)
        # the seed as the world lays it: a sea of the light row at one level with a hole; one quantum more of the light at a Node (the level v with v^2 = (1 + n) sea^2); a record of a plane row laid at a Node (one quantum of its unit at the vacuum's paces, the sense's im line); a detector Node
        plane_lays = []
        self.hold_volume = False
        for lay in world.get('seed', []):
            if 'detector' in lay: self.detectors.append(tuple(int(x) for x in lay['detector'])); continue
            if 'well' in lay:  # a hand-held well of the volume (the G hands' control): the content laid as a parabola, levels x (R^2 - r^2) div R^2 within the radius R, the volume's line at that level; held fixed where the world says so
                wl = lay['well']; at = tuple(int(x) for x in wl['at']); levels, R = int(wl['levels']), int(wl['radius']); self.hold_volume = bool(wl.get('held', False))
                for node in np.ndindex(*self.shape):
                    r2 = sum(min(abs(node[a] - at[a]), self.cube - abs(node[a] - at[a])) ** 2 for a in range(3))
                    if r2 < R * R:
                        c = levels * (R * R - r2) // (R * R)
                        self.vol.now[node] = int(np.asarray(volform.volume_of(gamma, np.array([c], dtype=object)), dtype=object).reshape(-1)[0]); self.vol.before[node] = self.vol.now[node]
                continue
            row = int(lay['row'])
            if row == 0:
                if 'sea' in lay:
                    self.light.now[:] = int(lay['sea'])
                    if 'hole' in lay: self.light.now[tuple(int(x) for x in lay['hole'])] = 0
                elif 'at' in lay:
                    at = tuple(int(x) for x in lay['at']); sea = int(self.light.now[at]); n = int(lay.get('quanta', 1))
                    self.light.now[at] = rule3.largest_below((1 + n) * sea * sea)
            else:
                plane_lays.append((row - 1, tuple(int(x) for x in lay['at']), int(lay.get('sense', 1)), int(lay.get('quanta', 1))))
        self.A = rule3.largest_below(action // 2)  # the former toy's fixed lay amplitude (the switch LEAN_FIXED_A), kept by name
        self.vol_pair = (den - den // gamma, den)
        self.X = phase.amplitude(phase.unit(gamma), WIDTH // 2 - 1)  # the phase pair's amplitude from half the law's width less one, so that a pair's product with a level stays within the width
        seed_pair = phase.seed(self.X, gamma)
        self.orbit_lines = [seed_pair]  # the last pair as lines, for the next act
        self.orbit = [(int(seed_pair[0][0]), int(seed_pair[1][0]))]  # the table of (cos, sin) as plain integers
        self.counts = {'births': 0, 'taken': 0, 'booked': 0, 'body_clicks': 0, 'refused_stop': 0, 'refused_origin': 0, 'refused_lay': 0, 'refused_orientation': 0, 'turns': 0, 'light_credits': 0, 'light_laid': 0, 'light_laid_nodes': 0}
        self.max_transient = 0
        if plane_lays:
            c = self.content(); factors = self.link_factors(); pace = paces.link_pace_of(self.gamma, c)
            for s_, at, sense, n in plane_lays:
                if not 0 <= s_ < self.nl: raise ValueError('the world lays a row the universe has not')
                A = self.lay_amplitude(s_, at, c, factors, pace); rec = 2 * s_ + (1 if sense > 0 else 0)
                re, im = self.planes[rec]; re.now[at] = re.now[at] + n * A; im.before[at] = im.before[at] + (1 if sense > 0 else -1) * n * A

    # ---- readings at the interval's start
    def content(self): return np.asarray(volform.level_of(self.gamma, self.vol.now), dtype=object)
    def pair_angle(self, n):
        """The integer (cos, sin) pair at the count n along the one orbit from the seed (features/phase), the orbit a table of the toy."""
        n = int(n); s = 1 if n >= 0 else -1; n = abs(n)  # the orbit a table built as far as the counts reach
        while len(self.orbit) <= n:
            c, sn = self.orbit_lines[-1]; c, sn = phase.act(c, self.gamma, 1), phase.act(sn, self.gamma, 1)
            self.orbit_lines = [(c, sn)]; self.orbit.append((int(c[0]), int(sn[0])))
        c, sn = self.orbit[n]
        return c, s * sn

    def tensions(self):
        """The axis parts: -num h_a(i) summed over every line of quanta, h_a = now(i-a) now(i+a) - now(i)^2; the axis lines of the volume row carry them (written below); the Link factor from the two ends' axis levels."""
        lines = [(self.light.now, self.den)] + [(l.now, self.pairs[r // 2][0]) for r in range(2 * self.nl) for l in self.planes[r]]
        return stress_parts(lines, self.shape)

    def link_factors(self):
        if os.environ.get('LEAN_FLAT_FACTORS'):  # a diagnostic switch of the toy: every Link factor G^2 (the vacuum's)
            return tuple(Z(self.shape) + self.G * self.G for _ in AXES)
        found = []
        for port, (axis, side) in enumerate(AXES):
            (summed,), _odd, _f = link(port, even=[self.vol_axes[axis].now])
            t = (summed + 1) // 2  # the Link's tension: the mean of the two ends' parts, rounded at the half (engine features/read.link_tension)
            found.append(np.vectorize(lambda tt: int(link_factor(self.gamma, self.G, min(int(tt), self.gamma))), otypes=[object])(t))  # the horizon: a tension at or past Gamma read at the wall, the factor 0 (engine features/read.link_tensions)
        return tuple(found)

    def rule(self, pair, c, factors):
        clock = paces.clock_of(self.gamma, c); pace = paces.link_pace_of(self.gamma, c)
        return rule3.rule_integers(pair[0], pair[1], self.gamma, clock, pace, factors, self.G)

    # ---- the step of one line and of one plane
    # ---- the one act of a row: Rule3 on the row's lines at the Node's paces, the arrivals turned (the owner's word of 2026-10-25: one function steps a line, inside the Node, called in one loop over the rows)
    def turned_arrival(self, arrivals, port, turn):
        """The arrivals of a row's lines at one Port, read in the Node's frame and turned by the Link's pair over X and by the odd line's tangent triple (W^2 - n^2, 2 W n, W^2 + n^2), W = 4 Gamma, one rounding per Link per part; a row of one line (a scalar) is turned by the identity; `turn` None is the identity for every shape."""
        if turn is None or len(arrivals) == 1: return arrivals
        phases, odd, frames = turn; axis, side = AXES[port]
        re_j, im_j = arrivals
        if frames is not None: im_j = frames[port] * im_j
        c, s = phases[port]
        _e, (n,), _f = link(port, odd=[odd[axis]])  # the odd line on the Link: the two ends' sum signed by the Port's side (the engine's V_ij = V_a(i) + V_a(j); no division, the mirror exact)
        Wl = 4 * self.gamma; tc, ts, tw = Wl * Wl - n * n, 2 * Wl * n, Wl * Wl + n * n
        a_re = (c * re_j - s * im_j); a_im = (s * re_j + c * im_j)
        a_re, a_im = (2 * a_re + self.X) // (2 * self.X), (2 * a_im + self.X) // (2 * self.X)
        b_re = (tc * a_re - ts * a_im); b_im = (ts * a_re + tc * a_im)
        return [(2 * b_re + tw) // (2 * tw), (2 * b_im + tw) // (2 * tw)]

    def rotate(self, lines, r, turn=None, direction=1):
        """Rule3's step of one row at every Node: for each of the row's lines the total S now - w before + SUM_j R_j m_j with m_j the row's arrivals at the Port turned as the row's shape turns them (`turned_arrival`), one carried division at the wall w per line; the rule's integers r at the Node's paces. Backward (direction -1) the same act on the before slots with the division back (`division_back`): the known part S now + SUM R m from the start levels (the before slots), the quotient next + before, before = quotient - next."""
        at = [l.now if direction == 1 else l.before for l in lines]
        totals = [r.self_coefficient * a - (r.wall * l.before if direction == 1 else 0) for l, a in zip(lines, at)]
        for port, ((axis, side), reach) in enumerate(zip(AXES, r.reaches)):
            arrivals = self.turned_arrival([across(a, port) for a in at], port, turn)
            totals = [t + reach * m for t, m in zip(totals, arrivals)]
        found = []
        if direction == 1:
            for l, t in zip(lines, totals):
                self.max_transient = max(self.max_transient, int(np.max(np.vectorize(lambda v: abs(int(v)).bit_length(), otypes=[object])(t))))
                nxt, rem = carried_division(t, r.wall, l.rem); found.append(Line(nxt, l.now, rem))
            return found
        for l, t in zip(lines, totals):
            quotient, rem = division_back(t, r.wall, l.rem); found.append(Line(l.before, quotient - l.now, rem))
        return found

    def link_current(self, line, port):
        """The light's own current on the Link at the Port, F_ij = now_i before_j - before_i now_j: odd under the exchange of the ends (the other end reads -F), read at the interval's start; the + child of a Link birth goes to the end the current flows into."""
        return line.now * across(line.before, port) - line.before * across(line.now, port)

    def frames(self, phi_rem):
        """The frame signs per Port: +1 where the two ends' frame bits (the phase row's remainder at the wall 2, complemented at every swap) agree, -1 where they differ; there the neighbour's plane is read conjugated and its count negated (ALGEBRA.md, The swap at the top, the frame clause)."""
        return [link(port, frame_bits=phi_rem)[2] for port in range(6)]

    def centred_count(self, cphi):
        """The Node's centred count K = Phi_next - Phi_before = 2 (Phi_now - Phi_before) + c, twice the trapezoid sum of the clocked potential to the triple's centre (ALGEBRA.md, The swap at the top, the phase hand's M23; the former toy read Phi_i - Phi_j, one integration too many, and pumped)."""
        return 2 * (self.phi.now - self.phi.before) + cphi

    def link_phases(self, frames=None, K=None):
        """The Link's count n_ij = K_i - f_ij K_j (the two ends' centred counts; f_ij the frame sign, the neighbour's count negated where the frames differ) and its (cos, sin) pair over X."""
        found = []
        if K is None: K = self.phi.now
        for port, (axis, side) in enumerate(AXES):
            n = K - (1 if frames is None else frames[port]) * across(K, port)
            pairs = np.vectorize(self.pair_angle, otypes=[object, object])(n)
            found.append((pairs[0], pairs[1]))
        return found

    def share(self, line, r, pace=None, vacuum=False):
        """The conserved form's term at the Node in the current's units over 2 p_i^2 G^2 (share.share without the frame's halves): [w (now^2 + before^2) - S now before - now SUM_j R_j before_j] div (2 p_i^2 G^2)."""
        reached = Z(self.shape); shared = Z(self.shape)
        for port, reach in enumerate(r.reaches):
            b_j, n_j = across(line.before, port), across(line.now, port)
            reached = reached + reach * b_j
            shared = shared + reach * (line.before - b_j) * (line.now + n_j)
        found = form_term(r.self_coefficient, r.wall, line.now, line.before) - line.now * reached
        if os.environ.get('LEAN_NODE_SHARE'):  # the former toy's reading: the Node's own term alone over 2 p^2 G^2
            pace = paces.link_pace_of(self.gamma, self.start_content) if pace is None else pace; sq = pace * pace
            return np.asarray(division_forward(found, 2 * sq * self.G * self.G + (sq == 0), 0)[0])
        found = found + found - shared  # the frame's term: the Links' products shared half and half between a Link's two ends (engine share.share, halves 2)
        if vacuum:  # the count at the vacuum's weight (V-D, the owner's sentence 7): the term over 4 Gamma^2 G^2, the Node's pace not entering, so a count rises only with a quantum gained and not with the content
            return np.asarray(division_forward(found, 4 * self.gamma * self.gamma * self.G * self.G, 0)[0])
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
        K = self.centred_count(cphi); self.count_max = max(int(abs(int(x))) for port in range(6) for x in (K - frames[port] * across(K, port)).reshape(-1))  # the Links' count's size this interval (a reading)
        phases = self.link_phases(frames, K); odd = [l.now for l in self.sign_axes]
        if os.environ.get('LEAN_NO_PHASE'):  # a diagnostic switch of the toy: the fold off (the pair (X, 0), the odd lines 0)
            phases = [(Z(self.shape) + self.X, Z(self.shape)) for _ in AXES]; odd = [Z(self.shape) for _ in range(3)]
        if os.environ.get('LEAN_NO_PHI'): phases = [(Z(self.shape) + self.X, Z(self.shape)) for _ in AXES]  # the phase pair off, the odd tangent on
        if os.environ.get('LEAN_NO_ODD'): odd = [Z(self.shape) for _ in range(3)]  # the odd tangent off, the phase pair on
        self.start_phases, self.start_odd = phases, [o.copy() for o in odd]
        parts = self.tensions()
        start = self.snapshot()
        forms = Z(self.shape); W = Z(self.shape); J = [Z(self.shape) for _ in range(3)]
        W_start = Z(self.shape)  # the planes' Wronskian at the interval's start, summed over the rows
        for re, im in self.planes: W_start = W_start + wronskian(re, im)
        new_planes = []
        for s_, pair in enumerate(self.pairs):
            r = self.rule(pair, c, factors)
            for sense in (0, 1):
                re, im = self.planes[2 * s_ + sense]
                nre, nim = self.rotate([re, im], r, (phases, odd, frames))
                forms = forms + (re.now * re.now - nre.now * re.before) + (im.now * im.now - nim.now * im.before)
                W = W + wronskian(nre, nim)
                for a, j_a in enumerate(plane_current(re, im, frames)): J[a] = J[a] + j_a  # the sign current from the start's levels, the neighbours read in the Node's frame
                new_planes.append([nre, nim])
        r_l = self.rule((self.den, self.den), c, factors)
        light = self.rotate([self.light], r_l)[0]; forms = forms + (self.light.now * self.light.now - light.now * self.light.before)
        sign = self.rotate([self.sign], r_l)[0]; sign_axes = [self.rotate([l], r_l)[0] for l in self.sign_axes]
        r_v = self.rule(self.vol_pair, c, factors)
        if self.hold_volume: vol, vol_axes = self.vol, self.vol_axes  # the control: the volume held by hand, no act on it
        else: vol = self.rotate([self.vol], r_v)[0]; vol_axes = [self.rotate([l], r_v)[0] for l in self.vol_axes]
        self.planes, self.light, self.sign, self.sign_axes, self.vol, self.vol_axes = new_planes, light, sign, sign_axes, vol, vol_axes
        self.stepped = [[l.copy() for l in r] for r in new_planes]  # the step's output as stepped, kept for the credits' frame (the swap discards it at a turned Node)
        # the held writes, one carried division per line
        trace, traceless = tensor_parts(parts)  # the stress's trace into the time line's write (the pressure term), the axis lines traceless
        p02 = p0 * p0  # the write's factor (p0 / Gamma)^2 at the power 2 on a count (engine paces.write_factor, intervals 2), Gamma^2 inside the fixed wall
        if not self.hold_volume: q, self.vol_wr[0] = carried_division(4 * start['vol_now'] * (forms * 54 * self.den * self.gamma ** 2 - trace * p0 * p0) * p0, 54 * self.den * self.gamma ** 4 * self.T, self.vol_wr[0]); self.vol.now = self.vol.now + (q if not self.hold_volume else 0)  # (d + 1) X c over Gamma E_s T, E_s 1, c the forms at the write's factor (p0 / Gamma)^1 (the holder's booking power one, engine WRONSKIAN_POWER) less the pressure, the trace times (p0 / Gamma)^2 at its wall 54 den (engine records.pressure_term: the stress parts times the pace squared over SIDES x AXES x AXES x den x Gamma^(2 + power) x clock^(3 - power)); the former toy weighed the trace 18 times more and its write vanished at every gradient
        for a in range(3):
            if self.hold_volume: break
            q, self.vol_wr[1 + a] = carried_division(traceless[a] * p02, 54 * self.den * self.T * self.gamma ** 2, self.vol_wr[1 + a]); self.vol_axes[a].now = self.vol_axes[a].now + q  # the traceless part over 6 W_c x 3 (the doubled wall 2 E_s W_c with the parts 3 and SIDES: engine held_write_of and scaled_sum; measured on the record's world, probes/write_probe.py)
        q, self.sign_wr[0] = carried_division(2 * W, self.T, self.sign_wr[0]); self.sign.now = self.sign.now + q
        for a in range(3):
            q, self.sign_wr[1 + a] = carried_division(J[a], self.T, self.sign_wr[1 + a]); self.sign_axes[a].now = self.sign_axes[a].now + q
        # W-S1 (the owner's sentence 3, 2026-10-25): a bound body's write lights the massless line: the change of the planes' Wronskian at the Node between two intervals, summed over every plane (one act over the rows), laid on the massless row's time line by the one lay act at the wall T; a static record lays nothing
        if not os.environ.get('LEAN_NO_WS1'):
            lq, self.light_wr = carried_division(W - W_start, self.T, self.light_wr); self.light.now = self.light.now + lq
            self.counts['light_laid'] += int(sum(abs(int(x)) for x in lq.reshape(-1))); self.counts['light_laid_nodes'] += int(sum(1 for x in lq.reshape(-1) if int(x) != 0))  # the emission's size: the levels laid on the light and the Nodes they were laid at (a count of the run)
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
                'held': [l.copy() for l in self.all_lines()], 'held_wr': [w.copy() for w in self.vol_wr + self.sign_wr + [self.light_wr]]}

    def is_im(self):
        """Which of all_lines() are the planes' im lines (conjugated at a turned Node)."""
        n_plain = len(self.all_lines()) - 4 * self.nl
        return [False] * n_plain + [k % 2 == 1 for k in range(4 * self.nl)]

    def floor(self):
        return int(np.asarray(volform.volume_of(self.gamma, np.array([-self.gamma], dtype=object)), dtype=object).reshape(-1)[0])

    def write_walls(self):
        return [54 * self.den * self.gamma ** 4 * self.T] + [54 * self.den * self.T * self.gamma ** 2] * 3 + [self.T] * 5  # the volume's time line, its three axis lines, the sign's four, the massless row's lay

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
        for wr, h, wall in zip(self.vol_wr + self.sign_wr + [self.light_wr], held_wr, self.write_walls()):
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
            root = rule3.largest_below(disc); s1 = (bcoef - root) // (-2 * a) if a < 0 else (-bcoef + root) // (2 * a)
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
        vac = not os.environ.get('LEAN_FRAME_WEIGHT')  # V-D, the owner's sentence 7 (2026-10-25): the birth's threshold and the lay's refusal read the share at the vacuum's weight, so a count rises only with a quantum gained; the frame's weight kept by name under the switch
        sh = self.share(start['light'], r_light, pace, vacuum=vac)
        owns = []  # each record's standing share at the interval's start (the lay's one comparison, take.below_quantum)
        for rec in range(2 * self.nl):
            r = self.rule(self.pairs[rec // 2], c, factors); re0, im0 = start['planes'][rec]
            owns.append(self.share(re0, r, pace, vacuum=vac) + self.share(im0, r, pace, vacuum=vac))
        born = []  # (the take's Node, the lift, the - child's Node, the + child's Node)
        frozen = np.asarray(pace, dtype=object) == 0 if np.ndim(pace) else np.zeros(self.shape, dtype=bool)
        if self.link_birth == 'current':
            # the Link close (Q1/Q2, the owner's sentence 1): every Link once from its +a end; a meeting where both ends hold a whole quantum; the + child at the end the light's own current F_ij = num (now_i before_j - before_i now_j) flows into, read at the interval's start; F = 0 refused by name; the lift by the one-Link read at the +a end
            currents = [self.den * self.link_current(start['light'], 2 * axis) for axis in range(3)]  # the light's own current on the +a Link of every Node, read once through the Link's function
            for at in np.ndindex(*self.shape):
                if frozen[at]: continue
                for axis in range(3):
                    j = tuple((at[a] + (1 if a == axis else 0)) % self.cube for a in range(3))
                    if frozen[j] or int(sh[at]) < self.unit_light or int(sh[j]) < self.unit_light: continue
                    F = int(currents[axis][at])
                    if F == 0:
                        self.counts['refused_orientation'] += 1; self.log.append({'event': 'refused', 'i': self.interval, 'node': list(at), 'cause': 'orientation', 'link': list(j)}); continue
                    plus, minus = (j, at) if F > 0 else (at, j)
                    number = self.read_number(plus, rules)  # the Link's one number read at the end the current flows into (no label: the end is the current's)
                    if number is None: continue
                    s_ = (number // self.unit_light) % self.nl
                    born.append((plus, s_, minus, plus))  # the take at the same end
        else:
            for at in np.ndindex(*self.shape):
                if frozen[at]: continue  # a frozen Node's share is not read (ALGEBRA.md, The horizon; engine share.frozen)
                whole, rest = divmod(int(sh[at]), self.unit_light)
                nb = ((at[0] + 1) % self.cube, at[1], at[2]) if self.link_birth else at
                if whole >= 2:
                    number = self.read_number(at, rules)
                    if number is None: continue
                    born.append((at, (number // self.unit_light) % self.nl, at, nb))
                elif whole == 1 and rest > 0:
                    number = self.read_number(at, rules)
                    if number is None: continue
                    if number % self.unit_light < rest: born.append((at, (number // self.unit_light) % self.nl, at, nb))
        # every face read before any write (meeting_board.closed): the lays refused first, then one exact take per Node of the children's walls summed, the start's light paying; the order of the Links enters no number
        kept = []
        for at, s_, minus, plus in born:
            # the lay refused by name where a child's family already stands above one quantum at its Node (ALGEBRA.md, The click writes on the lattice (b) and (d), the undepleted beam; engine take.below_quantum, meeting_board.refused_by)
            empty = not os.environ.get('LEAN_LAY_BELOW_QUANTUM')  # the lay's Wronskian is exact only at an empty Node (ALGEBRA.md, The click writes on the lattice, line 186): a child laid onto standing levels of its family adds the cross terms A x (standing levels) to W and the board's charge drifts (measured: W total 5.7e6 of 1.96e7 gross by interval 50 under the former rule); the lay is refused where the child's family stands at all; the former rule (take.below_quantum, at or below one quantum) kept by name under the switch
            bound_minus = 0 if empty else self.units[s_]; bound_plus = 0 if empty else self.units[s_]
            if int(owns[2 * s_][minus]) > bound_minus or int(owns[2 * s_ + 1][plus]) > bound_plus:
                self.counts['refused_lay'] += 1; self.log.append({'event': 'refused', 'i': self.interval, 'node': list(at), 'cause': 'lay', 'standing': int(owns[2 * s_][minus]), 'unit': self.units[s_]}); continue
            kept.append((at, s_, minus, plus))
        # one child per Node per record (the owner's sentence 1 as approved, S3): where two children of one record would land at one Node in one close, W would grow as the square (n children n^2 A^2 against n A^2: the charge made at the lay, measured 1.4e6 at one close of 31 births); every such child is refused by name, none chosen by the Links' order
        landing = {}
        for at, s_, minus, plus in kept:
            landing[(2 * s_, minus)] = landing.get((2 * s_, minus), 0) + 1; landing[(2 * s_ + 1, plus)] = landing.get((2 * s_ + 1, plus), 0) + 1
        crowded = [(at, s_, minus, plus) for at, s_, minus, plus in kept if landing[(2 * s_, minus)] > 1 or landing[(2 * s_ + 1, plus)] > 1]
        for at, s_, minus, plus in crowded:
            self.counts['refused_lay'] += 1; self.log.append({'event': 'refused', 'i': self.interval, 'node': list(at), 'cause': 'lay', 'children_at_one_node': max(landing[(2 * s_, minus)], landing[(2 * s_ + 1, plus)])})
        kept = [k for k in kept if k not in crowded]
        by_node = {}
        for at, s_, minus, plus in kept: by_node.setdefault(at, []).append((s_, minus, plus))
        taken_births = []
        for at in sorted(by_node):
            children = by_node[at]; walls = sum(2 * self.units[s_] for s_, _m, _p in children)
            levels, fall = self.take(at, walls, r_light, self.light)
            if levels is None:
                self.counts['refused_stop'] += len(children); self.log.append({'event': 'refused', 'i': self.interval, 'node': list(at), 'cause': 'stop', 'fall': fall, 'walls': walls}); continue
            taken_births.append((at, children, levels, fall, walls))
        for at, children, levels, fall, walls in taken_births:
            now = int(self.light.now[at]); before = int(self.light.before[at]); toward = 1 if before > now else -1
            self.light.now[at] = now + toward * levels
            for s_, minus, plus in children:
                A = self.lay_amplitude(s_, at, c, factors, pace)
                for sense, rec, where in ((-1, 2 * s_, minus), (1, 2 * s_ + 1, plus)):
                    re, im = self.planes[rec]; re.now[where] = re.now[where] + A; im.before[where] = im.before[where] + sense * A
                self.counts['births'] += 1; self.closes[at] += 1
                self.log.append({'event': 'birth', 'i': self.interval, 'node': list(at), 'line_pair': s_, 'senses': [-1, 1], 'minus': list(minus), 'plus': list(plus), 'taken': fall, 'booked': walls, 'levels': levels, 'light_now_was': now, 'proper': int(self.proper[at]), 'content': int(c[at]), 'amplitude': A, 'children_at_node': len(children)})
            self.counts['taken'] += fall; self.counts['booked'] += walls
        born_nodes = {at for at, _c, _l, _f, _w in taken_births} | {m for _a, ch, _l, _f, _w in taken_births for _s, m, _p in ch} | {p_ for _a, ch, _l, _f, _w in taken_births for _s, _m, p_ in ch}  # every Node of a birth taken, the take's and the children's; a refused birth pre-empts no closing (meeting_board.closed)
        # the bodies' closing: a record at a whole quantum of its own unit through one period of its re line's upward crossings
        for rec in range(2 * self.nl):
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
        # the detectors: the light's whole quanta at the Node risen over the interval (the start's share against the share as the close leaves the light), each quantum a light credit with the Node's proper count; a reading, no state
        if self.detectors:
            sh_end = self.share(self.light, r_light, pace, vacuum=True); sh_vac = self.share(start['light'], r_light, pace, vacuum=True)
            for det in self.detectors:
                rise = int(sh_end[det]) // self.unit_light - int(sh_vac[det]) // self.unit_light
                if rise > 0:
                    self.counts['light_credits'] += rise
                    self.log.append({'event': 'light', 'i': self.interval, 'node': list(det), 'quanta': rise, 'proper': int(self.proper[det]), 'content': int(c[det]), 'light_now': int(self.light.now[det]), 'light_before': int(self.light.before[det])})

    def lay_amplitude(self, s_, at, c, factors, pace):
        """The lay of one quantum: the child's record laid at the Node with the least amplitude A at which its own share reads one quantum of its unit at the Node's paces, (2 D + SUM_j R_j) A^2 >= unit x 4 p^2 G^2 (the frame share's term of a lone record with now = before = A; ALGEBRA.md, the lay of the record out whole); the former toy laid the root of T / 2 for every species."""
        if os.environ.get('LEAN_FIXED_A'): return self.A
        r = self.rule(self.pairs[s_], c, factors)
        D = 2 * int(np.asarray(r.wall)) - int(np.asarray(r.self_coefficient)[at]) - sum(int(np.asarray(x)[at]) for x in r.reaches)  # D from S = 2 w - D - SUM R
        C = 2 * D + sum(int(np.asarray(x)[at]) for x in r.reaches)
        pc = int(np.asarray(pace, dtype=object)[at]); target = self.units[s_] * 4 * pc * pc * self.G * self.G
        if C <= 0: return self.A
        A = rule3.largest_below(target // C)
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
        frame['odd'] = [int(side * (self.start_odd[axis][at] + self.start_odd[axis][n])) for (axis, side), n in zip(AXES, nodes)]
        frame['X'] = self.X
        frame['factors'] = [int(f[at]) for f in self.start_factors]
        return {'event': 'credit', 'i': self.interval, 'node': list(at), 'proper': int(self.proper[at]), 'closes': int(self.closes[at]), 'content': int(self.start_content[at]), 'line': rec, 'sense': 1 if W > 0 else -1 if W < 0 else 0,
                'beat': int(self.beats[rec][at]), 'frame': frame, 'taken': fall, 'levels': levels, 'light_now_was': light_was, 'sign_level': int(self.sign.now[at]), 'turned': bool(self.turned[at])}

    def step_back(self):
        """One interval back: the close undone from the log (the lays removed, the light restored), the swap undone at the turned Nodes (an involution), the phase row back, the writes undone by the division back from the start's levels (every start level is a before slot), Rule3 inverted on every line."""
        frame = self.stack.pop()
        # the close undone, in the reverse order of its lines
        for entry in reversed(self.log[frame['log_from']:]):
            at = tuple(entry['node'])
            if entry['event'] == 'birth':
                s_ = entry['line_pair']; minus, plus = tuple(entry['minus']), tuple(entry['plus'])
                for sense, rec, where in ((-1, 2 * s_, minus), (1, 2 * s_ + 1, plus)):
                    A = entry.get('amplitude', self.A)
                    re, im = self.planes[rec]; re.now[where] = re.now[where] - A; im.before[where] = im.before[where] - sense * A
                self.light.now[at] = entry['light_now_was']; self.closes[at] -= 1
            elif entry['event'] == 'credit':
                self.light.now[at] = entry['light_now_was']; self.closes[at] -= 1
        del self.log[frame['log_from']:]
        self.standing, self.crossed, self.beats = frame['counters']  # the readings restored
        # the swap's inverse, part one: the post-state kept; at a turned Node the before slot holds the start's now (negated on an im line), so every start level is read from the before slots after the im lines' sign is restored there
        top = frame['turned']
        post = [l.copy() for l in self.all_lines()]; post_wr = [w.copy() for w in self.vol_wr + self.sign_wr + [self.light_wr]]
        W_this = Z(self.shape)  # the planes' Wronskian as the step left it (the post state at an unturned Node)
        for rec in range(2 * self.nl): W_this = W_this + wronskian(*self.planes[rec])
        for line, im in zip(self.all_lines(), self.is_im()):
            if im: line.before = np.where(top, -line.before, line.before)
        start_bits = np.where(top, 1 - self.phi.rem, self.phi.rem)  # the frame bits at the start: complemented at the turned Nodes
        frames = self.frames(start_bits)
        # the start's readings from the before slots
        X_start = self.vol.before; c = np.asarray(volform.level_of(self.gamma, X_start), dtype=object); self.start_content = c
        p0 = paces.clock_of(self.gamma, c); p02 = p0 * p0
        self.proper = self.proper - p0
        # the phase row back: cphi from the sign's start level and p0; phi_before = 2 phi_now - phi_next + wq
        cphi = paces.rounded(self.sign.before * p0, self.gamma)
        wq, rem = division_back(2 * cphi, 2, self.phi.rem)
        phi_now = self.phi.before; phi_before = 2 * phi_now - self.phi.now + wq
        # at a turned Node the post-state is the pre-state exchanged: its before at the start is the post's now (K at the start needs it at every Node, turned neighbours included)
        phi_before = np.where(top, self.phi.now, phi_before); rem = np.where(top, 1 - self.phi.rem, rem)
        self.phi = Line(phi_now, phi_before, rem)
        # the tensions and factors at the start from the before slots
        start_lines = [(self.light.before, self.den)] + [(l.before, self.pairs[r // 2][0]) for r in range(2 * self.nl) for l in self.planes[r]]
        trace, traceless = tensor_parts(stress_parts(start_lines, self.shape))
        # the axis writes undone (their numerators from the start levels), then the factors at the start
        for a in range(3):
            q, self.vol_wr[1 + a] = division_back(traceless[a] * p02, 54 * self.den * self.T * self.gamma ** 2, self.vol_wr[1 + a]); self.vol_axes[a].now = self.vol_axes[a].now - q
        factors = self.link_factors()  # from the axis lines at the start (their now the start's now after the write undone? the factors read the axis lines' START now: the before slot)
        factors = []
        for port, (axis, side) in enumerate(AXES):
            (summed,), _odd, _f = link(port, even=[self.vol_axes[axis].before]); t = (summed + 1) // 2
            factors.append(np.vectorize(lambda tt: int(link_factor(self.gamma, self.G, min(int(tt), self.gamma))), otypes=[object])(t))
        factors = tuple(factors)
        # the sign's writes undone: W from the stepped planes at the Node (now and before slots), J from the start's levels (the before slots) in the Node's frame
        J = [Z(self.shape) for _ in range(3)]; W = Z(self.shape)
        for rec in range(2 * self.nl):
            re, im = self.planes[rec]
            W = W + wronskian(re, im)
            start_re, start_im = Line(re.before, None, None), Line(im.before, None, None)  # the start's levels in the before slots
            for a, j_a in enumerate(plane_current(start_re, start_im, frames)): J[a] = J[a] + j_a
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
                bre, bim = self.rotate([re, im], r, (phases, odd, frames), direction=-1)
                forms = forms + (bre.now * bre.now - re.now * bre.before) + (bim.now * bim.now - im.now * bim.before)
                self.planes[2 * s_ + sense] = [bre, bim]
        W_prev = Z(self.shape)
        for rec in range(2 * self.nl): W_prev = W_prev + wronskian(*self.planes[rec])
        if not os.environ.get('LEAN_NO_WS1'):
            lq, self.light_wr = division_back(W_this - W_prev, self.T, self.light_wr); self.light.now = self.light.now - lq
        r_l = self.rule((self.den, self.den), c, factors)
        light_b = self.rotate([self.light], r_l, direction=-1)[0]; forms = forms + (light_b.now * light_b.now - self.light.now * light_b.before)
        self.light = light_b
        self.sign = self.rotate([self.sign], r_l, direction=-1)[0]; self.sign_axes = [self.rotate([l], r_l, direction=-1)[0] for l in self.sign_axes]
        # the volume's write undone, then its lines inverted
        q, self.vol_wr[0] = division_back(4 * X_start * (forms * 54 * self.den * self.gamma ** 2 - trace * p0 * p0) * p0, 54 * self.den * self.gamma ** 4 * self.T, self.vol_wr[0]); self.vol.now = self.vol.now - q
        r_v = self.rule(self.vol_pair, c, factors)
        self.vol = self.rotate([self.vol], r_v, direction=-1)[0]; self.vol_axes = [self.rotate([l], r_v, direction=-1)[0] for l in self.vol_axes]
        # the swap's inverse, part two: at the turned Nodes the same act on the post-state gives the pre-state (the exchange and the complement again, the im lines' conjugation again)
        if self.swap_on and top.any(): self.exchange(top, post, post_wr)
        self.interval -= 1

    def census(self):
        arrays = [a for l in self.all_lines() for a in (l.now, l.before, l.rem)] + self.vol_wr + self.sign_wr + [self.light_wr] + self.standing + self.crossed + self.beats + [self.proper, self.closes]
        bits = max(int(np.max(np.vectorize(lambda v: abs(int(v)).bit_length(), otypes=[object])(a))) for a in arrays)
        return len(arrays), bits

    def state_bytes(self):
        return b''.join(np.asarray(a, dtype=object).astype(str).tobytes() for l in self.all_lines() for a in (l.now, l.before, l.rem)) + b''.join(np.asarray(a).astype(str).tobytes() for a in self.vol_wr + self.sign_wr + [self.light_wr])


if __name__ == '__main__':
    sys.set_int_max_str_digits(0)
    # usage: lean_full.py <world.json> <out.json> [mode: current|link|node] [back N]: the run of the world's intervals, the record dumped, then N intervals run back and compared (the arrow's reading on the record)
    world_path, out = sys.argv[1], sys.argv[2]
    mode = sys.argv[3] if len(sys.argv) > 3 else 'current'
    back = int(sys.argv[sys.argv.index('back') + 1]) if 'back' in sys.argv else 0
    birth = {'current': 'current', 'link': True, 'node': False}[mode]
    universe, world = load_world(world_path)
    intervals = int(world['intervals'])
    b = Lean(universe, world, link_birth=birth)
    rows = []; maxbits = 0
    import time, hashlib; t0 = time.monotonic_ns()
    marks = sorted({1, intervals} | {(k * intervals) // 12 for k in range(1, 12)} | {intervals // 60, intervals // 24})  # the rows' cadence: twelfths of the run and two early marks
    hashes = []
    def state_hash(): return hashlib.sha256(b.state_bytes() + str(b.interval).encode()).hexdigest()
    for t in range(intervals):
        if back and t >= intervals - back: hashes.append(state_hash())
        b.step(); n, bits = b.census(); maxbits = max(maxbits, bits)
        if b.interval in marks:
            c = b.content()
            cs = [int(x) for x in c.reshape(-1)]; vs = [int(x) for x in b.vol.now.reshape(-1)]
            energy = sum(int(x) * int(x) for rec in b.planes for l in rec for x in l.now.reshape(-1)); odd_max = max(abs(int(x)) for l in b.sign_axes for x in l.now.reshape(-1)); light_v = max(abs(int(a) - int(bb)) for a, bb in zip(b.light.now.reshape(-1), b.light.before.reshape(-1)))
            packets = {}
            for s_ in range(b.nl):
                for sense in (0, 1):
                    re, im = b.planes[2 * s_ + sense]; wgt = re.now * re.now + im.now * im.now; total = int(sum(int(x) for x in wgt.reshape(-1)))
                    if total == 0: continue
                    idx = np.indices(b.shape); cen = [int(sum(int(w) * int(x) for w, x in zip(wgt.reshape(-1), idx[a].reshape(-1)))) * 1000 // total for a in range(3)]
                    packets['row %d sense %d' % (s_ + 1, 1 if sense else -1)] = {'centroid (thousandths of a Link)': cen, 'nodes with levels': int(sum(1 for x in wgt.reshape(-1) if int(x) > 0)), 'energy bits': total.bit_length()}
            rows.append({'i': b.interval, 'packets (reader)': packets, 'content min/mean/max': [min(cs), sum(cs) // len(cs), max(cs)], 'volume mean': sum(vs) // len(vs), 'births': b.counts['births'], 'body_clicks': b.counts['body_clicks'], 'refused': b.counts['refused_stop'] + b.counts['refused_origin'] + b.counts['refused_lay'] + b.counts['refused_orientation'], 'refused_lay': b.counts['refused_lay'], 'refused_orientation': b.counts['refused_orientation'], 'turns': b.counts['turns'], 'integers': n, 'max bits': maxbits, 'max transient bits': b.max_transient, 'sign level max': max(abs(int(x)) for x in b.sign.now.reshape(-1)), 'planes energy bits': energy.bit_length(), 'tension min/max': [min(int(x) for l in b.vol_axes for x in l.now.reshape(-1)), max(int(x) for l in b.vol_axes for x in l.now.reshape(-1))], 'odd max bits': odd_max.bit_length(), 'link count max': getattr(b, 'count_max', 0), 'orbit table': len(b.orbit), 'W total': sum(int(x) for re, im in b.planes for x in (re.now * im.before - im.now * re.before).reshape(-1)), 'W abs sum': sum(abs(int(x)) for re, im in b.planes for x in (re.now * im.before - im.now * re.before).reshape(-1)), 'light velocity max': light_v, 'milliseconds': (time.monotonic_ns() - t0) // 1000000})
            print(json.dumps(rows[-1]), flush=True)
    run_back = None; kept_log = list(b.log)  # the record's log as the run left it; the run back below removes its lines as it undoes them
    if back:
        exact = 0
        for k in range(back):
            b.step_back(); exact += (state_hash() == hashes[back - 1 - k])
        run_back = {'intervals': back, 'exact': exact}
        print(json.dumps({'run back': run_back}), flush=True)
    json.dump({'world': world, 'universe': universe, 'mode': mode, 'den': den_ if (den_ := b.den) else 0, 'cube': b.cube, 'intervals': intervals, 'lifts': [(None, str(num), str(s)) for _v, num, s in b.lifts], 'T': b.T, 'gamma': b.gamma, 'G': b.G, 'counts': {k: str(v) for k, v in b.counts.items()}, 'turns': b.turns, 'rows': rows, 'run_back': run_back, 'log': kept_log}, open(out, 'w'))
    print(json.dumps({'counts': {k: str(v) for k, v in b.counts.items()}}))
