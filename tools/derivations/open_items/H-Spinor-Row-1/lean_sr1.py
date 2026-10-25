"""sr1 flagged copy of tools/derivations/open_items/H-Spinor-Row-1/toy/lean_full.py (made by make_copy.py; the flags: the shape-8 row, control.spinor_turn, control.pauli, the `at` lay's `sense` and `spin`, control.held_potential). David's local lean Node, complete (the owner's word, 04:4x: run everything, omit nothing). Every act of the law's interval at a generic Node of a fixed state, the engine's exact primitives (core.rule3, core.paces, features.phase, loader.circle), the architecture the toy's.

STATE per Node (fixed, 95 integers): volume row 16 (time line 3, three axis lines 9, four write remainders); light 3; the sign's one row 16 (time line 3, three odd lines 9, four write remainders) + its phase potential line 3; the three lifts' planes 2 senses x 2 lines x 3 = 36; per plane record standing, crossed, beats = 18; proper, closes = 2; the Link factors are read, never held.
ACTS per interval, the same at every Node: the tensions read (the axis parts from the quanta's lines), the Link factors from the two ends; Rule3 on every line at the Node's composed paces, the planes' arrivals turned by the Link phases of the sign's potential and by the odd lines' tangent (the fold); the held writes, one carried division per line (the volume from the forms, its axis lines from the tensions, the sign's time line from the Wronskians, its odd lines from the sign currents); the sign's phase potential stepped; the swap at a weak maximum of the volume's time line (every line exchanged, every remainder complemented); the close: the light's whole quanta met, the one-Link read on the frame's digit lattices, the pick and the whether, the exact take by the frame's shares' fall, the lay of a conjugate pair into the planes; the bodies' closing; the credit with the frame. The run back: every act inverted in the reverse order, the lays and takes from the log.
"""
from __future__ import annotations
import sys, os, json, math
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'src'))  # tools/derivations/open_items/H-Spinor-Row-1 -> src (the copy's place)
from event_universe.core import rule3, paces
from event_universe.core.rule3 import division_forward, carried_division, division_back, wall_of, form_term, link_factor
from event_universe.core.paces import sine_den
from event_universe.features import volume as volform, phase

AXES = ((0, 1), (0, -1), (1, 1), (1, -1), (2, 1), (2, -1))
Z = lambda shape: np.zeros(shape, dtype=object)
SR1 = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'sr1_matrices.json')))  # sr1 flag: the spinor row's matrices, derived by sr1_algebra.py (the group's 48, Gamma_a, J, G, K0, the Port turns), typed nowhere
def matvec8(M, xs):
    """sr1: an integer 8 x 8 matrix on 8 arrays, exact."""
    return [sum(M[r][c] * xs[c] for c in range(8) if M[r][c]) for r in range(8)]
def gform8(G, xs, ys):
    """sr1: the bilinear form SUM_rc G_rc x_r y_c on 8 arrays, exact."""
    found = 0
    for r in range(8):
        for c in range(8):
            if G[r][c]: found = found + G[r][c] * xs[r] * ys[c]
    return found


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
    """The stress tensor's three diagonal parts from the rows' levels, one act on every line alike: SUM over lines of weight x (gradient along the axis)^2 (the stress is the Links', decided 2026-10-23); `lines` holds (levels, weight) pairs."""
    parts = [Z(shape) for _ in range(3)]
    for levels, num in lines:
        for a in range(3):
            d = gradient(levels, a); parts[a] = parts[a] + num * d * d
    return parts


def tensor_parts(parts):
    """A tensor's trace and its traceless diagonal parts: trace = SUM_a parts_a; traceless_a = 3 parts_a - trace (the stress's trace is the time line's, the axis lines traceless)."""
    trace = parts[0] + parts[1] + parts[2]
    return trace, [3 * part - trace for part in parts]


class Row:
    """One row of the Node as the universe file names it: a shape (its count of lines), a pair (num, den) for Rule3's rule, or a wall of its own for a row with no Links (the phase row); its lines. No name and no role: every choice the acts make is by these numbers."""
    __slots__ = ('shape', 'pair', 'wall', 'lines')
    def __init__(self, shape, pair, wall, lines): self.shape, self.pair, self.wall, self.lines = shape, pair, wall, lines
    @property
    def gap(self): return None if self.pair is None else self.pair[1] - self.pair[0]


class Line:
    """One line of a row: its two levels, its rotation remainder at the rule's wall `wall`, and where the row writes it, its write remainder `wr` at the write wall `wwall`."""
    __slots__ = ('now', 'before', 'rem', 'wall', 'wr', 'wwall')
    def __init__(self, now, before, rem, wall, wr=None, wwall=None): self.now, self.before, self.rem, self.wall, self.wr, self.wwall = now, before, rem, wall, wr, wwall
    def copy(self): return Line(self.now.copy(), self.before.copy(), self.rem.copy(), self.wall, None if self.wr is None else self.wr.copy(), self.wwall)


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

    def __init__(self, universe, world):
        """The Node from the universe's integers and rows and the world's shape and seed, nothing else (the owner's rule: no number in the code); the rows by kind: the one shape-1 row at (den, den) the massless quanta (light), the shape-2 rows the lifts (planes); the two held rows the law's at every Node, the volume at (den - den div Gamma, den) and the sign at (den, den)."""
        ints = universe['integers']
        den, gamma, action, unit = int(ints['den']), int(ints['node_clock']), int(ints['quantum_action']), int(ints['link_unit'])
        shape = tuple(int(x) for x in world['shape'])
        if len(set(shape)) != 1: raise ValueError('the toy runs on a cube: the shape must be [c, c, c]')
        cube = shape[0]
        self.den, self.cube, self.gamma, self.T, self.G = den, cube, gamma, action, unit
        self.shape = (cube,) * 3; S = self.shape
        self.w = wall_of(den, gamma, unit)
        # the rows as the file has them, each a shape (its lines' count) with a pair or a wall of its own; the Node holds them with no name: the massless row is the shape-1 row whose pair has the gap 0, the metric's row the shape-10 row, the potential's the shape-4 row, a plane row (shape 2) the conjugate pair of records, the row with its own wall the phase row (no Links)
        # every remainder starts at half its wall (the engine rounds half up); the write walls by shape: the metric's time line 54 den Gamma^4 T and its other lines 54 den T Gamma^2, the potential's four lines and the massless row T, a plane none
        def lines_of(shape_, pair, wall):
            if wall is not None: return [Line(Z(S), Z(S), Z(S) + wall // 2, wall)]
            if shape_ == 10: wwalls = [54 * den * gamma ** 4 * action] + [54 * den * action * gamma ** 2] * 9
            elif shape_ == 4: wwalls = [action] * 4
            elif shape_ == 2 and pair is not None and pair[0] == pair[1]: wwalls = [action, None]  # the massless plane's first line takes the lay of W-S1 at the wall T
            else: wwalls = [None] * shape_
            wall_ = self.w * 12 * gamma if shape_ == 8 else self.w  # sr1 flag: the shape-8 row's wall carries the Pauli term's 12 Gamma (the one division exact)
            return [Line(Z(S), Z(S), Z(S) + wall_ // 2, wall_, None if ww is None else Z(S) + ww // 2, ww) for ww in wwalls]
        self.rows_ = []; self.by_index = []  # the rows in the file's order (a lay names a row by its index in the file)
        for r in universe['rows']:
            shape_ = int(r['shape']); pair = None if r.get('pair') is None else (int(r['pair'][0]), int(r['pair'][1])); wall = None if r.get('wall') is None else int(r['wall'])
            if shape_ == 1 and wall is None: raise ValueError('a shape-1 row with a pair: light is the plane whose pair is (den, den) (U-S2, the owner\'s word of 2026-10-25), no fourth shape')
            self.rows_.append(Row(shape_, pair, wall, lines_of(shape_, pair, wall))); self.by_index.append(self.rows_[-1])
        # the acts' order: a row whose write reads other rows comes after them: the row with its own wall, the planes with a gap, the plane at the gap 0 (its lay reads the planes' Wronskian), the shape-4 row, the shape-10 row
        order = lambda r: 0 if r.wall is not None else {2: 1 + (r.gap == 0), 8: 1, 4: 3, 10: 4}.get(r.shape, 5)  # sr1 flag: the shape-8 row acts with the planes with a gap
        self.rows_.sort(key=order)
        if sum(1 for r in self.rows_ if r.wall is not None) != 1 or len([r for r in self.rows_ if r.shape == 2 and r.gap == 0]) != 1 or len([r for r in self.rows_ if r.shape == 10]) != 1 or len([r for r in self.rows_ if r.shape == 4]) != 1:
            raise ValueError('the universe names one row with its own wall, one massless plane (shape 2 at the gap 0), one shape-10 row and one shape-4 row')
        if self.row(10).pair != (den - den // gamma, den): raise ValueError('the shape-10 row is the clock\'s one level: its pair (den - den div Gamma, den)')
        if self.row(4).pair != (den, den): raise ValueError('the shape-4 row stands at (den, den)')
        # the planes (shape 2): every one a record of two lines; the massless plane among them; the lifts the planes with a gap, in the file's order (the draw's list); each plane's quantum its unit: 3 T s for a plane with a gap (s the pair's sine), 3 T den for the plane at the gap 0 (the drift's double root)
        self.lifts = [r for r in self.records() if r.gap > 0]
        self.pairs = [r.pair for r in self.lifts]
        self.nl = len(self.pairs)
        if self.nl == 0: raise ValueError('the universe names no plane row with a gap')
        self.units = [3 * action * (sine_den(r.pair[0], den) if r.gap > 0 else den) for r in self.records()]
        nr = len(self.records()); self.standing = [Z(S) for _ in range(nr)]; self.crossed = [Z(S) for _ in range(nr)]; self.beats = [Z(S) for _ in range(nr)]
        self.proper = Z(S); self.closes = Z(S)
        self.interval = 0; self.log = []; self.turns = []; self.stack = []
        for l in self.row(10).lines[:1]: l.now[:] = gamma; l.before[:] = gamma  # the metric's time line at the vacuum's level
        self.unit_gap0 = self.units[self.records().index(self.row(2, gap=0))]  # the massless plane's quantum, W_c = 3 den T
        self.detectors = []  # the Nodes whose light the record credits (the world names them; a reading, no state)
        # the seed as the world lays it: a list of lays in the three forms of the law and no fourth (the owner's word of 2026-10-25, "2, 3, 4 approved"; the Z hands' form): `sea` lays the massless row's drift v, the largest integer with v^2 <= T, at every Node; `hole` takes it back at one Node; `at` lays a packet: on the massless row N drifts at the centre, on a plane row the conjugate pair, N quanta each record, over the raised cosine's envelope of the half-width 2 or 3 (exact in integers there and at no other width below 6). Refused by name: a fourth form, a row no pair of the universe carries, a sea of a plane row, a Node off the board, a plane packet of another width (a body is laid over its packet, never one Node)
        self.drift = rule3.largest_below(action)
        packets = []
        for lay in world.get('seed', []):
            form = lay.get('lay'); r_ = self.by_index[int(lay['row'])] if 'row' in lay else None  # the row by its index in the universe file (the Boss's ruling of 2026-10-25: the index names it, not the pair)
            if r_ is not None and r_.shape not in (2, 8): raise ValueError('a lay is onto a quanta row (shape 2 or 8)')  # sr1 flag
            if form == 'sea':
                if r_.gap != 0: raise ValueError('a sea is the massless plane\'s alone: the drift is its double root')
                z = r_.lines[0]; z.now[:] = z.now + self.drift
            elif form == 'hole':
                at = self.node_of(lay['at']); z = self.row(2, gap=0).lines[0]; z.now[at] = z.now[at] - self.drift
            elif form == 'at':
                n = int(lay['quanta']); at = self.node_of(lay['centre'])
                if r_.gap == 0: z = r_.lines[0]; z.now[at] = z.now[at] + n * self.drift
                else: packets.append((self.records().index(r_), at, int(lay.get('width', 0)), n, lay.get('sense'), lay.get('spin', 'spin_up_z')))  # sr1 flag: `sense` lays one record alone; `spin` names the spinor's vector
            else: raise ValueError('a lay of no form of the law: %r' % (form,))
        # the toy's controls and readings, no lay of the law (named open for the owner's word): `control.well` a hand-held well of the volume (the content laid as a parabola within the radius, held fixed where the file says so), `detectors` the Nodes whose light credits the record reads
        self.control = world.get('control', {}); self.hold_volume = False
        well = self.control.get('well')
        if well:
            at = self.node_of(well['at']); levels, R = int(well['levels']), int(well['radius']); self.hold_volume = bool(well.get('held', False))
            for node in np.ndindex(*self.shape):
                r2 = sum(min(abs(node[a] - at[a]), self.cube - abs(node[a] - at[a])) ** 2 for a in range(3))
                if r2 < R * R:
                    c = levels * (R * R - r2) // (R * R)
                    m = self.row(10).lines[0]; m.now[node] = int(np.asarray(volform.volume_of(gamma, np.array([c], dtype=object)), dtype=object).reshape(-1)[0]); m.before[node] = m.now[node]
        self.detectors = [self.node_of(d) for d in world.get('detectors', [])]
        self.ones_frames = [1] * 6  # sr1: the plane turn of the spinor row's planes reads no frame sign (the row's conjugation is K0, applied before)
        self.held_lines = []  # sr1 flag (sp2's form): hand-held lines of the shape-4 row (a control: the magnet), each set here and restored after every act
        for h_ in self.control.get('held_potential', []):
            k_ = int(h_['line']); at_ = self.node_of(h_['at']); F = Z(self.shape)
            def centred(node, a):  # the torus-centred offset along the axis a
                d = (node[a] - at_[a]) % self.cube
                return d - self.cube if d > self.cube // 2 else d
            for node in np.ndindex(*self.shape):
                if h_['field'] == 'sg': F[node] = -centred(node, int(h_['across'])) * (int(h_['B0']) + int(h_['b']) * centred(node, int(h_['along'])))  # A_line = -(d_across)(B0 + b d_along): the curl B0 + b d_along along the third axis, its gradient along `along`
                elif h_['field'] == 'linear': F[node] = int(h_['E']) * centred(node, int(h_['along']))
                elif h_['field'] == 'sg_image': F[node] = int(h_['s_line']) * (-(int(h_['s_across']) * centred(node, int(h_['across'])))) * (int(h_['B0']) + int(h_['b']) * int(h_['s_along']) * centred(node, int(h_['along'])))  # the sg field carried through a signed permutation as a polar vector, A'_a'(g x) = s_a A_a(x)
                else: raise ValueError('a held field of no form: %r' % (h_['field'],))
            line_ = self.row(4).lines[k_]; line_.now = F.copy(); line_.before = F.copy(); self.held_lines.append(k_)
        self.A = rule3.largest_below(action // 2)  # the lay's amplitude where the rule's form has no positive term (a lone record's share cannot be read there)
        self.X = phase.amplitude(phase.unit(gamma), WIDTH // 2 - 1)  # the phase pair's amplitude from half the law's width less one, so that a pair's product with a level stays within the width
        seed_pair = phase.seed(self.X, gamma)
        self.orbit_lines = [seed_pair]  # the last pair as lines, for the next act
        self.orbit = [(int(seed_pair[0][0]), int(seed_pair[1][0]))]  # the table of (cos, sin) as plain integers
        self.counts = {'births': 0, 'taken': 0, 'booked': 0, 'body_clicks': 0, 'refused_stop': 0, 'refused_origin': 0, 'refused_lay': 0, 'refused_orientation': 0, 'refused_twist': 0, 'turns': 0, 'light_credits': 0, 'light_laid': 0, 'light_laid_nodes': 0}
        self.max_transient = 0
        for s_, at, h, n, sn_, sp_ in packets: self.lay_packet(s_, at, h, n, sn_, sp_)

    def node_of(self, xyz):
        """A Node named by the world file: three integers on the board; a Node off the board is refused by name."""
        at = tuple(int(x) for x in xyz)
        if len(at) != 3 or any(not 0 <= x < self.cube for x in at): raise ValueError('a Node off the board: %r' % (at,))
        return at

    def row(self, shape, gap=None):
        """The one row of the shape (and of the gap den - num where given), chosen by the numbers alone."""
        return next(r for r in self.rows_ if r.shape == shape and r.wall is None and (gap is None or r.gap == gap))

    def walled(self):
        """The one row with a wall of its own and no Links (the phase row)."""
        return next(r for r in self.rows_ if r.wall is not None)

    def records(self):
        """The shape-2 rows in order: record 2 s + k of the pair s, k = 0 the sense -1 and k = 1 the sense +1 (the file's order)."""
        return [r for r in self.rows_ if r.shape in (2, 8)]  # sr1 flag: the shape-8 quanta row is a record too

    def planes(self):
        """sr1: the shape-2 rows alone, the draw's list (a birth lays a conjugate pair onto a plane; a shape-8 child's spin state is not derived here, so the draw names planes alone)."""
        return [r for r in self.rows_ if r.shape == 2]

    def rule_of(self, r, c, factors):
        """A row's rule: Rule3's integers at its pair and the Node's paces, or, for the row with its own wall, no Links and the own weight 2 w (next = 2 now - before + the write inside the division)."""
        if r.wall is not None: return rule3.Rule(tuple(0 for _ in AXES), 2 * r.wall, r.wall, 0)
        ru = self.rule(r.pair, c, factors)
        if r.shape == 8: return rule3.Rule(tuple(12 * self.gamma * x for x in ru.reaches), 12 * self.gamma * ru.self_coefficient, 12 * self.gamma * ru.wall, 12 * self.gamma * ru.mass)  # sr1 flag: the row's line scaled by 12 Gamma so that the Pauli term SUM_j R_j (Phi . Gamma) now enters as an integer
        return ru

    def lay_packet(self, rec, at, h, n, one_sense=None, one_spin='spin_up_z'):
        """The `at` lay of a plane row: the conjugate pair (the two records at the senses -1 and 1) laid at rest over the raised cosine's envelope of the half-width h (the weights 2, 1 at h = 2; 4, 3, 1 at h = 3; the product over the three axes), each record at the largest amplitude A at which its share at the vacuum's weight, summed over the packet, is at most n quanta of its unit (a search by comparisons); each Node's lines at the band's rest rotation: re_now = A w_i div w_0, re_before = re_now num div den, im_now = 0, im_before = sense re_now s div den with s the pair's sine (Z1's form)."""
        weights = {2: (2, 1), 3: (4, 3, 1)}.get(h)
        if weights is None: raise ValueError('a plane packet has the half-width 2 or 3: a body is laid over its packet')
        r_ = self.records()[rec]; num = r_.pair[0]; sn = sine_den(num, self.den); w0 = weights[0] ** 3  # the pair's numbers
        envelope = Z(self.shape)
        for j in np.ndindex(*(2 * h - 1,) * 3):
            off = [x - (h - 1) for x in j]
            envelope[tuple((at[a] + off[a]) % self.cube for a in range(3))] += weights[abs(off[0])] * weights[abs(off[1])] * weights[abs(off[2])]
        c = self.content(); factors = self.link_factors(); r = self.rule_of(r_, c, factors); self.start_content = c
        spin = None if r_.shape != 8 else (SR1[one_spin][0] if isinstance(one_spin, str) else [int(v) for v in one_spin])  # sr1 flag: the spinor's integer vector of the lay
        def record(A, sense):
            re_now = (A * envelope) // w0
            if r_.shape == 8:  # sr1: the 8 lines at the band's rest rotation: now = re_now v, before = (num now + sense s J now) div den, one rounding per line as the plane's lay
                nows = [re_now * v for v in spin]; jn = matvec8(SR1['J'], nows)
                def odd(x, m):  # the law's odd rounding: the magnitude's floor with the sign after (features/phase.signed_rounded), so the -I lay is the negation and the two senses' lays sum with the J term cancelled exactly
                    return np.where(x < 0, -((-x) * m // self.den), x * m // self.den)
                return [Line(n_, odd(n_, num) + sense * odd(j_, sn), None, r_.lines[0].wall) for n_, j_ in zip(nows, jn)]
            return Line(re_now, (re_now * num) // self.den, None, self.w), Line(Z(self.shape), sense * ((re_now * sn) // self.den), None, self.w)
        def share_of(A):
            if r_.shape == 8: return int(sum(int(x) for x in self.share8(record(A, 1), self.rule(r_.pair, c, factors), vacuum=True).reshape(-1)))
            re, im = record(A, 1)
            return int(sum(int(x) for x in (self.share(re, r, vacuum=True) + self.share(im, r, vacuum=True)).reshape(-1)))
        target = n * self.units[rec]
        high = 1
        while share_of(high) <= target: high = high + high
        low = 0
        while high - low > 1:
            middle = (low + high) // 2
            if share_of(middle) <= target: low = middle
            else: high = middle
        for sense in ((-1, 1) if one_sense is None else (int(one_sense),)):  # sr1 flag: one sense where the lay names it; else the conjugate pair (the im lines cancel, the record neutral)
            lines_ = record(low, sense)
            if r_.shape == 8 and self.control.get('exclusion'):  # sr1 flag: the lay's rule per full state (SP-S3): at the lay's Node the standing row's spin density s against the child's: the child laid whole where they oppose (or nothing stands), passing in the books where they agree
                W0, s0, _ = self.bilinears8(r_.lines); _, s1, _ = self.bilinears8(lines_)
                dot = sum(int(s0[a_][at]) * int(s1[a_][at]) for a_ in range(3))
                if dot > 0:
                    self.counts['refused_lay'] += 1; self.log.append({'event': 'refused', 'i': 0, 'node': list(at), 'cause': 'state', 'dot': dot, 'standing_spin': [int(x[at]) for x in s0], 'child_spin': [int(x[at]) for x in s1]}); continue
            if r_.shape == 8: self.lay8(rec, lines_)
            else: re, im = lines_; self.lay(rec, Ellipsis, (re.now, re.before, im.now, im.before))
        self.log.append({'event': 'lay', 'i': 0, 'node': list(at), 'line_pair': rec, 'width': h, 'quanta': n, 'amplitude': low, 'share': share_of(low), 'unit': self.units[rec], 'nodes': int(sum(1 for x in envelope.reshape(-1) if int(x) > 0)), 'sense': one_sense, 'spin': spin})

    # ---- the readings at the interval's start
    def content(self): return np.asarray(volform.level_of(self.gamma, self.row(10).lines[0].now), dtype=object)
    def pair_angle(self, n):
        """The integer (cos, sin) pair at the count n along the one orbit from the seed (features/phase), the orbit a table of the toy."""
        n = int(n); s = 1 if n >= 0 else -1; n = abs(n)  # the orbit a table built as far as the counts reach
        while len(self.orbit) <= n:
            c, sn = self.orbit_lines[-1]; c, sn = phase.act(c, self.gamma, 1), phase.act(sn, self.gamma, 1)
            self.orbit_lines = [(c, sn)]; self.orbit.append((int(c[0]), int(sn[0])))
        c, sn = self.orbit[n]
        return c, s * sn

    def link_factors(self, axis_levels=None):
        """The Link factor at each Port from the two ends' axis parts of the volume row: the tension the mean of the two ends' levels rounded at the half (engine features/read.link_tension), a tension at or past Gamma read at the wall, the factor 0 (the horizon)."""
        axis_levels = [l.now for l in self.row(10).lines[1:4]] if axis_levels is None else axis_levels
        found = []
        for port, (axis, side) in enumerate(AXES):
            (summed,), _odd, _f = link(port, even=[axis_levels[axis]])
            t = (summed + 1) // 2
            found.append(np.vectorize(lambda tt: int(link_factor(self.gamma, self.G, min(int(tt), self.gamma))), otypes=[object])(t))
        return tuple(found)

    def rule(self, pair, c, factors):
        clock = paces.clock_of(self.gamma, c); pace = paces.link_pace_of(self.gamma, c)
        return rule3.rule_integers(pair[0], pair[1], self.gamma, clock, pace, factors, self.G)

    def frames(self, phi_rem):
        """The frame signs per Port: +1 where the two ends' frame bits (the phase row's remainder at the wall 2, complemented at every swap) agree, -1 where they differ; there the neighbour's plane is read conjugated and its count negated (ALGEBRA.md, The swap at the top, the frame clause)."""
        return [link(port, frame_bits=phi_rem)[2] for port in range(6)]

    def centred_count(self, cphi, phi):
        """The Node's centred count K = Phi_next - Phi_before = 2 (Phi_now - Phi_before) + c from the phase row at the start, twice the trapezoid sum of the clocked potential to the triple's centre (ALGEBRA.md, The swap at the top, the phase hand's M23)."""
        return 2 * (phi.now - phi.before) + cphi

    def link_phases(self, frames, K):
        """The Link's count n_ij = K_i - f_ij K_j (the two ends' centred counts; f_ij the frame sign, the neighbour's count negated where the frames differ) and its (cos, sin) pair over X."""
        found = []
        for port in range(6):
            n = K - frames[port] * across(K, port)
            pairs = np.vectorize(self.pair_angle, otypes=[object, object])(n)
            found.append((pairs[0], pairs[1]))
        return found

    def share(self, line, r, pace=None, vacuum=False):
        """The conserved form's term at the Node in the current's units over the weight (share.share with the frame's halves): [w (now^2 + before^2) - S now before - now SUM_j R_j before_j], doubled, less the Links' products shared half and half between a Link's two ends; over 4 p^2 G^2 at the frame's weight, over 4 Gamma^2 G^2 at the vacuum's (V-D, the owner's sentence 7: a count rises only with a quantum gained and not with the content)."""
        reached = Z(self.shape); shared = Z(self.shape)
        for port, reach in enumerate(r.reaches):
            b_j, n_j = across(line.before, port), across(line.now, port)
            reached = reached + reach * b_j
            shared = shared + reach * (line.before - b_j) * (line.now + n_j)
        found = form_term(r.self_coefficient, r.wall, line.now, line.before) - line.now * reached
        found = found + found - shared
        pace = paces.link_pace_of(self.gamma, self.start_content) if pace is None else pace
        sq = (self.gamma * self.gamma) if vacuum else pace * pace
        wall = 4 * sq * self.G * self.G + (sq == 0)
        return np.asarray(division_forward(found, wall, 0)[0])

    # ---- the four acts of the Node on a row: rotate, write, swap (the exchange), click (the close); the one Link act `link`
    def turned_arrival(self, arrivals, port, turn):
        """The arrivals of a row's lines at one Port, read in the Node's frame and turned by the Link's pair over X and by the odd line's tangent triple (W^2 - n^2, 2 W n, W^2 + n^2), W = 4 Gamma, one rounding per Link per part; a row of one line (a scalar) is turned by the identity; `turn` None is the identity for every shape."""
        if turn is None or len(arrivals) == 1: return arrivals
        phases, odd, frames = turn; axis, side = AXES[port]
        if len(arrivals) == 8:  # sr1 flag: the shape-8 row's arrival: the frame's conjugation K0 where the frames differ, its 4 planes turned by the Link's pair and the odd tangent as a plane's (one rounding per Link per line), then the Port's spinor turn (exact, an integer matrix)
            xs = list(arrivals); fr = frames[port]
            if not isinstance(fr, int) and bool((np.asarray(fr) == -1).any()): xs = [np.where(fr == -1, k_, x_) for k_, x_ in zip(matvec8(SR1['K0'], xs), xs)]
            turned = []
            for k in range(4): turned += self.turned_arrival([xs[2 * k], xs[2 * k + 1]], port, (phases, odd, self.ones_frames))
            S = self.spinor_turn_matrix(axis, side)
            return turned if S is None else matvec8(S, turned)
        re_j, im_j = arrivals
        im_j = frames[port] * im_j
        c, s = phases[port]
        _e, (n,), _f = link(port, odd=[odd[axis]])  # the odd line on the Link: the two ends' sum signed by the Port's side (the engine's V_ij = V_a(i) + V_a(j); no division, the mirror exact)
        Wl = 4 * self.gamma; tc, ts, tw = Wl * Wl - n * n, 2 * Wl * n, Wl * Wl + n * n
        a_re = (c * re_j - s * im_j); a_im = (s * re_j + c * im_j)
        a_re, a_im = (2 * a_re + self.X) // (2 * self.X), (2 * a_im + self.X) // (2 * self.X)
        b_re = (tc * a_re - ts * a_im); b_im = (ts * a_re + tc * a_im)
        return [(2 * b_re + tw) // (2 * tw), (2 * b_im + tw) // (2 * tw)]

    def rotate(self, lines, r, turn=None, direction=1, flux=None, starts=None):
        """Rule3's step of one row at every Node, the one function of a line: for each line the total S now - w before + SUM_j R_j m_j (+ the line's flux where the row carries its write inside the division, the phase row) with m_j the row's arrivals at the Port turned as the row's shape turns them (`turned_arrival`), one carried division at the wall w per line; the rule's integers r at the Node's paces. Backward (direction -1) the same act on the before slots with the division's direction -1: the known part S now + SUM R m from the start levels, the quotient next + before, before = quotient - next."""
        at = [l.now if direction == 1 else l.before for l in lines] if starts is None else starts  # the start level: forward the now slot; backward the before slot (or the start levels given: at a turned Node the pre-state's now)
        totals = [r.self_coefficient * a - (r.wall * l.before if direction == 1 else 0) + (0 if flux is None else f) for l, a, f in zip(lines, at, flux or [0] * len(lines))]
        if len(lines) == 8 and turn is not None and self.control.get('pauli'):  # sr1 flag: the Pauli term nu (Phi . Gamma) now in the numerator, nu = R / (2 Gamma) derived from g = 2; with the row's line scaled by 12 Gamma it is SUM_j R_j (Phi . Gamma) now, R_j the unscaled reaches; Phi the one-Link curl of the odd lines at the start; read from the start levels so the inverse reads the same term
            phi = self.curl_odd(turn[1]); coef = sum(r.reaches) // (12 * self.gamma)
            for a_, ax in enumerate('xyz'):
                gx = matvec8(SR1['Gamma'][ax], at)
                totals = [t + coef * phi[a_] * g for t, g in zip(totals, gx)]
        for port, reach in enumerate(r.reaches):
            arrivals = self.turned_arrival([across(a, port) for a in at], port, turn)
            totals = [t + reach * m for t, m in zip(totals, arrivals)]
        found = []
        for l, a, t in zip(lines, at, totals):
            if direction == 1: self.max_transient = max(self.max_transient, int(np.max(np.vectorize(lambda v: abs(int(v)).bit_length(), otypes=[object])(t))))
            quotient, rem = carried_division(t, r.wall, l.rem, direction)
            found.append(Line(quotient, l.now, rem, l.wall, l.wr, l.wwall) if direction == 1 else Line(a, quotient - l.now, rem, l.wall, l.wr, l.wwall))
        return found

    def link_current(self, line, port):
        """The light's own current on the Link at the Port, F_ij = now_i before_j - before_i now_j: odd under the exchange of the ends (the other end reads -F), read at the interval's start; the + child of a Link birth goes to the end the current flows into."""
        return line.now * across(line.before, port) - line.before * across(line.now, port)

    def net_current(self, line, axis):
        """A line's net transverse current at every Node along an axis, u_b(k) = F(k, k - b) - F(k, k + b): the current into the Node from the -b Link less the current out along the +b Link, read from the Node's own two Links of that axis."""
        return self.link_current(line, 2 * axis + 1) - self.link_current(line, 2 * axis)

    def twist(self, line, axis):
        """The twist of a line's transverse current along the +axis Link of every Node (PA2's form, the owner's sentence 4): h(k, k + e_a) = u_b(k) u_c(k + e_a) - u_c(k) u_b(k + e_a) with (a, b, c) cyclic, e_a . (u(k) x u(k + e_a)), the cross product of the two ends' transverse currents read at each end from its own Links; a pseudoscalar of the unoriented Link, the handedness of the born pair."""
        a, b, c = axis, (axis + 1) % 3, (axis + 2) % 3
        ub, uc = self.net_current(line, b), self.net_current(line, c)
        return ub * across(uc, 2 * a) - uc * across(ub, 2 * a)

    def write(self, line, numerator, direction):
        """The one write act on a line: the numerator's carried division at the line's write wall, the quotient added to the level now (forward) or taken back (backward), the remainder carried in the line."""
        q, line.wr = carried_division(numerator, line.wwall, line.wr, direction); line.now = line.now + direction * q

    def act(self, lines, r, turn, numerators, direction, flux=None, top=None, kept=None):
        """The Node's act on one row in the direction: Rule3's rotate of the row then its lines' writes (forward); the writes undone then the rotate inverted (backward), the same two acts in the reverse order. Returns the row at the start, the stepped levels before the write, and the row as the act leaves it. Backward, at the turned Nodes `top` the row is set to `kept`, the pre-state the exchange returned (the inverse at a turned Node is no act: the turned Node ended the interval at its pre-state exchanged)."""
        if direction == 1:
            stepped = self.rotate(lines, r, turn, 1, flux); levels = [l.now for l in stepped]
            for line, n in zip(stepped, numerators):
                if n is not None: self.write(line, n, 1)
            return lines, levels, stepped
        starts = None if kept is None else [np.where(top, l.now, l.before) for l in lines]  # the start levels read before the writes are undone: the before slot, the pre-state's now at a turned Node
        for line, n in zip(lines, numerators):
            if n is not None: self.write(line, n, -1)
        levels = [l.now for l in lines]; start = self.rotate(lines, r, turn, -1, flux, starts)
        if kept is not None:
            for l, k in zip(start, kept):
                l.now, l.before, l.rem = np.where(top, k.now, l.now), np.where(top, k.before, l.before), np.where(top, k.rem, l.rem)
                if l.wr is not None: l.wr = np.where(top, k.wr, l.wr)
        return start, levels, start

    def rows(self):
        """The Node's rows' lines in the acts' order (the row with its own wall, the planes, the massless row, the potential's row, the metric's row: a row whose write reads other rows comes after them)."""
        return [r.lines for r in self.rows_]

    def set_rows(self, rows):
        for r, lines in zip(self.rows_, rows): r.lines = list(lines)

    def all_lines(self): return [l for row in self.rows() for l in row]

    def is_im(self):
        """Which lines are a plane's im line (the second line of a shape-2 row), conjugated at a turned Node."""
        return [len(row) == 2 and k == 1 for row in self.rows() for k in range(len(row))]

    def floor(self):
        return int(np.asarray(volform.volume_of(self.gamma, np.array([-self.gamma], dtype=object)), dtype=object).reshape(-1)[0])

    def exchange(self, top, held):
        """The swap's act at the Nodes `top`: every line set to the held line exchanged and complemented (the two levels exchanged, an im line conjugated, every remainder complemented at its wall, an im line's rotation remainder kept); an involution with the state it leaves, so the same act on the post-state gives the pre-state (ALGEBRA.md, the fifth act)."""
        for row, hrow in zip(self.rows(), held):  # sr1 flag: a shape-8 row exchanged as a whole: the levels exchanged and conjugated by K0 (the lattice's conjugation, derived), every remainder complemented (named open: K0 is no signed permutation; no turn fires in the measured runs)
            if len(row) == 8:
                kb = matvec8(SR1['K0'], [h.before for h in hrow]); kn = matvec8(SR1['K0'], [h.now for h in hrow])
                for line, h, b_, n_ in zip(row, hrow, kb, kn):
                    line.now, line.before, line.rem = np.where(top, b_, line.now), np.where(top, n_, line.before), np.where(top, line.wall - 1 - h.rem, line.rem)
        eights = [id(l_) for row in self.rows() if len(row) == 8 for l_ in row]
        for line, h, im in zip(self.all_lines(), [l for row in held for l in row], self.is_im()):
            if id(line) in eights: continue
            sgn = -1 if im else 1
            line.now, line.before, line.rem = np.where(top, sgn * h.before, line.now), np.where(top, sgn * h.now, line.before), np.where(top, h.rem if im else line.wall - 1 - h.rem, line.rem)
            if line.wr is not None: line.wr = np.where(top, line.wwall - 1 - h.wr, line.wr)

    def swap(self, held):
        """The swap at the top (ALGEBRA.md, the fifth act): the weak maximum X0 <= X1 >= X2 with one strict (the held before, the held now, the now after the writes), or the floor (X0 or X2 below X_f); the turned Node ends the interval at the state it started from, exchanged and complemented, the step's output discarded there."""
        k = self.rows_.index(self.row(10)); x0, x1, x2 = held[k][0].before, held[k][0].now, self.row(10).lines[0].now
        top = np.vectorize(lambda a, b, c: 1 if (int(a) <= int(b) and int(c) <= int(b) and (int(a) < int(b) or int(c) < int(b))) else 0, otypes=[object])(x0, x1, x2) == 1
        xf = self.floor()
        top = top | (np.vectorize(lambda a, c: 1 if (int(a) < xf or int(c) < xf) else 0, otypes=[object])(x0, x2) == 1)
        self.turned = top
        if top.any():
            self.counts['turns'] += int(top.sum()); self.turns.append((self.interval, int(top.sum())))
            self.exchange(top, held)
        return top

    # ---- the interval: the Node's one program in both directions
    def run(self, direction=1):
        """One interval of the Node's program in the direction (ALGEBRA.md, The direction: every act but the click a bijection; the run back the same acts in the reverse order, each inverted). The readings at the start (the content, the paces, the Link factors, the frames, the sign's clocked potential, the stress), then one act on every row in the rows' order, then the swap at the top and the close (forward); backward the close is undone from the log first, the turned Nodes are returned to their pre-state by the same exchange, and the rows' acts are inverted in the same order. Every start level is read from the slot the direction names: forward the now slot; backward the before slot, which the forward act left holding the start's now, and the now slot at a turned Node."""
        if direction == 1: self.interval += 1; top = np.zeros(self.shape, dtype=bool); kept = None
        else: frame = self.stack.pop(); self.unclick(frame); top = frame['turned']
        held = [[l.copy() for l in row] for row in self.rows()]  # the state at this end of the interval: the pre-state forward, the post-state backward
        if direction == -1:
            if top.any(): self.exchange(top, held)
            kept = [[l.copy() for l in row] for row in self.rows()]
        at = (lambda l: l.now) if direction == 1 else (lambda l: np.where(top, l.now, l.before))
        # the rows by their numbers: the metric's (shape 10: its time line the content, its axis lines the tensions), the row with its own wall (the frames and the Links' count), the potential's (shape 4: the clocked potential and the odd tangent), the planes (shape 2), the massless row (shape 1 at the gap 0)
        rows = self.rows(); idx = {id(r): k for k, r in enumerate(self.rows_)}; where = lambda r: idx[id(r)]
        metric, walled, potential, massless, records = self.row(10), self.walled(), self.row(4), self.row(2, gap=0), self.records()
        # the readings at the start
        c = np.asarray(volform.level_of(self.gamma, at(metric.lines[0])), dtype=object); self.start_content = c
        p0 = paces.clock_of(self.gamma, c); self.proper = self.proper + direction * p0
        factors = self.link_factors([at(l) for l in metric.lines[1:4]]); self.start_factors = factors
        frames = self.frames(walled.lines[0].rem); self.start_frames = frames
        cphi = paces.rounded(at(potential.lines[0]) * p0, self.gamma)  # the clocked potential at the potential's start level
        out = [None] * len(rows); ends = lambda k: (top, None if kept is None else kept[k])
        riding = records + ([potential] if self.control.get('metric_sources') == 'every riding row' else [])  # the rows whose form and tensions source the metric's write: the planes alone, or every row that divides at the carrier's wall (the shape-4 row too; the Boss's 2(a), measured against the planes alone)
        parts_ = stress_parts([(at(l), r.pair[0]) for r in riding if r.shape != 8 for l in r.lines], self.shape)
        for r in riding:  # sr1 flag: a shape-8 row's stress G-weighted, SUM_a num d_a N . G . d_a N
            if r.shape == 8:
                for a in range(3):
                    d = [gradient(at(l), a) for l in r.lines]; parts_[a] = parts_[a] + r.pair[0] * gform8(SR1['G'], d, d)
        trace, traceless = tensor_parts(parts_)
        forms = Z(self.shape); W_start = Z(self.shape); W = Z(self.shape); J = [Z(self.shape) for _ in range(3)]; plane_starts = []; stepped = []; phases = odd = None
        # one loop over the rows in the acts' order, one act on every row alike; what a row's write reads and what turns its arrivals is a function of its shape and its pair (the law's table): the walled row carries its write 2 c_phi inside its division and gives the Links' count; a plane with a gap is turned by the Link's pair and the odd tangent, the plane at the gap 0 by nothing (K = omega_0 Gamma = 0) and its first line takes W-S1 (the planes' Wronskian change, the planes acted before it); the shape-4 row's time line takes 2 W and its other lines the planes' current; the shape-10 row's time line takes every riding row's form less the pressure and its axis lines the traceless stress, its other lines nothing
        for r in self.rows_:
            k = where(r); rule = self.rule_of(r, c, factors); turn = None; flux = None; numerators = [None] * r.shape
            if r.wall is not None: flux = [2 * cphi]
            elif r.shape == 2:
                turn = None if r.gap == 0 else (phases, odd, frames)
                if r.gap == 0: numerators = [W - W_start, None]
            elif r.shape == 8: turn = (phases, odd, frames)  # sr1 flag: the spinor row turned as a plane with a gap; its Port turn and Pauli term inside rotate
            elif r.shape == 4: numerators = [2 * W, *J]
            elif r.shape == 10:
                if self.hold_volume: out[k] = rows[k]; continue  # the control: the metric's row held by hand, no act on it in either direction
                X = at(r.lines[0]); p02 = p0 * p0
                numerators = [4 * X * (forms * 54 * self.den * self.gamma ** 2 - trace * p02) * p0] + [traceless[a] * p02 for a in range(3)] + [None] * (r.shape - 4)
            start, levels, out[k] = self.act(rows[k], rule, turn, numerators, direction, flux, *ends(k))
            if r.shape == 4 and self.held_lines:  # sr1 flag (sp2's form): the held lines restored to the interval's start (a constant in both directions, the bijection kept)
                for kk in self.held_lines: out[k][kk] = held[k][kk].copy()
            if r in riding:  # the form of every line that rides the carrier, read for the metric's write
                if r.shape == 8: forms = forms + gform8(SR1['G'], [l0.now for l0 in start], [l0.now for l0 in start]) - gform8(SR1['G'], levels, [l0.before for l0 in start])  # sr1 flag: the row's form G-weighted
                else:
                    for l0, lv in zip(start, levels): forms = forms + (l0.now * l0.now - lv * l0.before)
            if r.wall is not None:  # the Links' count from the walled row at the start, the phase pair and the odd tangent for the planes' turn
                K = self.centred_count(cphi, start[0])
                self.count_max = max(int(abs(int(x))) for port in range(6) for x in (K - frames[port] * across(K, port)).reshape(-1))  # the Links' count's size this interval (a reading)
                phases = self.link_phases(frames, K); odd = [at(l) for l in potential.lines[1:4]]
                self.start_phases, self.start_odd = phases, [o.copy() for o in odd]
            elif r.shape == 8:  # sr1 flag: the spinor row's readings: its charge W before and after the step, its current, its lines for the click
                W_start = W_start + self.bilinears8(start)[0]
                after = out[k] if direction == 1 else held[k]
                W = W + self.bilinears8(after)[0]; stepped.append([l.copy() for l in after]); plane_starts.append(start)
                for a, j_a in enumerate(self.current8(start)): J[a] = J[a] + j_a
            elif r.shape == 2:  # a plane's readings for the writes after it: its Wronskian before and after the step, its current
                re, im = start; W_start = W_start + wronskian(re, im)
                after = out[k] if direction == 1 else held[k]  # the plane as the step left it
                W = W + wronskian(*after); stepped.append([l.copy() for l in after]); plane_starts.append(start)
                for a, j_a in enumerate(plane_current(re, im, frames)): J[a] = J[a] + j_a
                if r.gap == 0 and direction == 1:  # the emission's size, a reading of the run: the levels laid on the massless line and the Nodes they were laid at
                    laid = out[k][0].now - levels[0]
                    self.counts['light_laid'] += int(sum(abs(int(x)) for x in laid.reshape(-1))); self.counts['light_laid_nodes'] += int(sum(1 for x in laid.reshape(-1) if int(x) != 0))
        self.stepped = stepped  # kept for the credits' frame (the swap discards it at a turned Node)
        self.set_rows(out)
        if direction == -1: self.interval -= 1; return
        counters = ([a.copy() for a in self.standing], [a.copy() for a in self.crossed], [a.copy() for a in self.beats])
        top = self.swap(held)
        log_from = len(self.log)
        self.click(plane_starts, held)
        self.stack.append({'turned': top, 'counters': counters, 'log_from': log_from})

    def step(self): return self.run(1)
    def step_back(self): return self.run(-1)

    # ---- the close
    def frame_nodes(self, at):
        return [at] + [tuple((at[a] + (side if a == axis else 0)) % self.cube for a in range(3)) for axis, side in AXES]

    def read_number(self, at, rules):
        """The one-Link read: every line's remainder at the Node on the Node's own lattice F_i = gcd(w, D_i, R_i1..R_i6) and at each neighbour on the Link's lattice gcd(w, R_ji), the digit r div F, the base w div F + 1, sorted by value, composed modulo M = unit x 3 (the carry); the three refusals by name."""
        M = self.unit_gap0 * len(self.planes())  # the draw composed modulo the planes' count times the massless unit: the quotient names the plane, over every plane alike (sr1: the shape-2 rows; a shape-8 child's spin state is not derived here)
        nodes = self.frame_nodes(at); digits = []; origin = True; coarse = True
        half = self.w // 2
        for line, r in rules:
            at_node = lambda x, node: int(np.asarray(x)[node]) if np.ndim(x) else int(x)  # a rule's integer at a Node (a walled row's reaches are the one integer 0)
            F0 = math.gcd(int(r.wall), at_node(r.mass, at), *[at_node(x, at) for x in r.reaches])
            for k, n in enumerate(nodes):
                F = F0 if k == 0 else math.gcd(int(r.wall), at_node(r.reaches[k - 1], n))
                rem = int(line.rem[n]); values = int(r.wall) // F
                if self.control.get('digits') == 'folded': rem = min(rem, int(r.wall) - rem); values = values // 2 + 1  # the Boss's mend of 10:1x for the twist's CP: every line's remainder folded to its wall, min(r, w - r), the distance to the nearer edge, conjugation-even on every line alike
                origin = origin and rem in (half - 1, half); coarse = coarse and values <= 3
                digits.append((rem // F, values + 1))
        if origin: self.counts['refused_origin'] += 1; return None
        if coarse: return None
        digits.sort(); carry = 0; room = 1
        for d, b in digits: carry = (carry * b + d) % M; room = min(room * b, M)
        return carry, room  # the number drawn and the draw's room: the count of numbers the read could give (the digits' bases' product, at most M), the click's entropy its bit length

    def take(self, at, walls, r_gap0, line):
        """The exact take at the Node: the light's now moved toward its before by the least count of levels at which the Node's share falls by the walls. The share's term at the Node is w (now^2 + before^2) - S now before - now L, L = SUM_j R_j before_j, over W_i = 2 p_i^2 G^2; moving now by t s (t the direction) its fall is f(s) = [w (now^2 - (now + t s)^2) - t s (S before + L)] div W_i, an exact quadratic in s: the least s with f(s) >= walls by one integer root (largest_below), checked exactly at s - 1, s, s + 1; refused by name where the full move cannot pay."""
        now, before = int(line.now[at]), int(line.before[at])
        if now == before: return None, 0
        t = 1 if before > now else -1
        S = int(np.asarray(r_gap0.self_coefficient)[at]); w = int(r_gap0.wall)
        L = 0
        for (axis, side), reach in zip(AXES, r_gap0.reaches):
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

    def lay(self, rec, where, levels, sign=1):
        """The one lay act: a record's four levels (re_now, re_before, im_now, im_before) added at the Node `where` (or over the board where `where` is the whole), taken back with sign -1 (the inverse of the lay is the same act)."""
        re, im = self.records()[rec].lines
        for line, now, before in ((re, levels[0], levels[1]), (im, levels[2], levels[3])):
            line.now[where] = line.now[where] + sign * now; line.before[where] = line.before[where] + sign * before

    def lay8(self, rec, lines_, sign=1):
        """sr1: the lay of a shape-8 record's 8 lines over the board (the two levels added; sign -1 takes them back)."""
        for line, l_ in zip(self.records()[rec].lines, lines_):
            line.now = line.now + sign * l_.now; line.before = line.before + sign * l_.before

    def share8(self, lines, r, pace=None, vacuum=False):
        """sr1: the conserved form's term of a shape-8 row at the Node: the plane's share with the Gram matrix G of the row's invariant form (derived) weighting the lines pairwise, 2 [w N.G.N + w B.G.B - S N.G.B - N.G.(SUM_j R_j B_j)] - SUM_j R_j (B - B_j).G.(N + N_j), over 4 p^2 G^2 (the plane's share is the case G = I); at the unscaled rule."""
        G = SR1['G']; N = [l.now for l in lines]; B = [l.before for l in lines]
        reached = [Z(self.shape) for _ in range(8)]; shared = Z(self.shape)
        for port, reach in enumerate(r.reaches):
            Bj = [across(b, port) for b in B]; Nj = [across(n, port) for n in N]
            reached = [x + reach * bj for x, bj in zip(reached, Bj)]
            shared = shared + reach * gform8(G, [b - bj for b, bj in zip(B, Bj)], [n + nj for n, nj in zip(N, Nj)])
        found = r.wall * (gform8(G, N, N) + gform8(G, B, B)) - r.self_coefficient * gform8(G, N, B) - gform8(G, N, reached)
        found = found + found - shared
        pace = paces.link_pace_of(self.gamma, self.start_content) if pace is None else pace
        sq = (self.gamma * self.gamma) if vacuum else pace * pace
        wall = 4 * sq * self.G * self.G + (sq == 0)
        return np.asarray(division_forward(found, wall, 0)[0])

    def period8(self, lines, standing_now):
        """sr1: the row's rotation period at the Nodes where it stands: cos omega = N.G.B / N.G.N exactly (a fraction, named), c_0 = 1, c_1 = cos, c_(k+1) = 2 cos c_k - c_(k-1); P the first k >= 2 at which c_k is a maximum (c_k >= c_(k-1) and c_k >= c_(k+1)), the first return; 0 where the row stands at no quantum or the ratio is degenerate."""
        from fractions import Fraction as Fr_
        G = SR1['G']; N = [l.now for l in lines]; B = [l.before for l in lines]
        nn = gform8(G, N, N); nb = gform8(G, N, B); found = Z(self.shape)
        for at in zip(*np.nonzero(np.asarray(standing_now, dtype=object) == 1)):
            at = tuple(int(x) for x in at); d = int(nn[at])
            if d == 0: continue
            cs = Fr_(int(nb[at]), d)
            if cs >= 1 or cs <= -1: continue
            c0, c1 = Fr_(1), cs; k = 1
            while k < 200:
                c2 = 2 * cs * c1 - c0
                if k >= 2 and c1 >= c0 and c1 >= c2: found[at] = k; break
                c0, c1 = c1, c2; k += 1
        return found

    def gj(self):
        G, J = SR1['G'], SR1['J']
        return [[sum(G[r][k] * J[k][c] for k in range(8)) for c in range(8)] for r in range(8)]

    def bilinears8(self, lines):
        """sr1: the row's bilinears at every Node: the charge W = B.(G J).N (the G-weighted sum of the 4 planes' Wronskians re_now im_before - im_now re_before), the spin density s_a = N.(G Gamma_a).N, the spin Wronskians B.(G J Gamma_a).N."""
        G = SR1['G']; GJ = self.gj(); N = [l.now for l in lines]; B = [l.before for l in lines]
        W = gform8(GJ, B, N)
        s = [gform8(G, N, matvec8(SR1['Gamma'][a], N)) for a in 'xyz']
        sw = [gform8(GJ, B, matvec8(SR1['Gamma'][a], N)) for a in 'xyz']
        return W, s, sw

    def current8(self, lines):
        """sr1: the row's sign current on each axis, J_a = dN_a.(G J).N with dN_a the centred difference of the levels now (the plane's re dim - im dre with G = I), the odd lines' source."""
        GJ = self.gj(); N = [l.now for l in lines]
        return [gform8(GJ, [gradient(n, a) for n in N], N) for a in range(3)]

    def curl_odd(self, odd):
        """sr1: the one-Link curl of the odd lines at the Node, Phi_a = d_b A_c - d_c A_b, d_b the centred difference through the two Ports of the axis b (the six neighbours' odd lines and nothing further)."""
        return [gradient(odd[(a + 2) % 3], (a + 1) % 3) - gradient(odd[(a + 1) % 3], (a + 2) % 3) for a in range(3)]

    def spinor_turn_matrix(self, axis, side):
        """sr1 flag control.spinor_turn: the Port's spinor turn, 'none' (the identity: the row four planes under the turn), 'half' (J Gamma_a, the half turn's lift) or 'quarter' (u_a, the quarter turn's lift); the -a Port the inverse."""
        kind = self.control.get('spinor_turn', 'none')
        if kind == 'none': return None
        key = {'half': 'S_half', 'quarter': 'S_quarter'}[kind]
        return SR1[key if side == 1 else key + '_inv']['xyz'[axis]]

    def momentum_of(self, line_now, line_before, at, d_now=0, d_before=0, num=1):
        """The change of the lattice momentum P_a = 2 num SUM_i (now_(i+a) before_i - now_i before_(i+a)) when a line's level now at the Node moves by d_now and its level before by d_before (co1's reading of the close): 2 num [d_now (before_(i-a) - before_(i+a)) + d_before (now_(i+a) - now_(i-a))] per axis."""
        found = []
        for a in range(3):
            up = tuple((at[k] + (1 if k == a else 0)) % self.cube for k in range(3)); down = tuple((at[k] - (1 if k == a else 0)) % self.cube for k in range(3))
            found.append(2 * num * (d_now * (int(line_before[down]) - int(line_before[up])) + d_before * (int(line_now[up]) - int(line_now[down]))))
        return found

    def take_at(self, at, walls, r_gap0, cause):
        """One exact take at a Node of the walls booked: the light's level now moved toward its before by the least count of levels at which the Node's share falls by the walls (`take`); refused by name where the fall cannot reach the walls (the stop). Returns (levels, fall, the light's now before the take) or None."""
        z = self.row(2, gap=0).lines[0]
        levels, fall = self.take(at, walls, r_gap0, z)
        if levels is None:
            self.counts['refused_stop'] += cause; self.log.append({'event': 'refused', 'i': self.interval, 'node': list(at), 'cause': 'stop', 'fall': fall, 'walls': walls}); return None
        now = int(z.now[at]); before = int(z.before[at]); toward = 1 if before > now else -1
        z.now[at] = now + toward * levels; self.closes[at] += 1
        self.last_dp = self.momentum_of(z.now, z.before, at, d_now=toward * levels, num=self.row(2, gap=0).pair[0])  # the take's momentum, booked on the click's line (N-S3's reading)
        return levels, fall, now

    def meet(self, gap0_start, sh, rules, frozen):
        """The Link close (Q1/Q2, the owner's sentence 1): every Link once from its +a end; a meeting where both ends hold a whole quantum of light at the vacuum's weight and neither end is frozen; the + child at the end the light's own current F_ij = num (now_i before_j - before_i now_j) flows into, read at the interval's start (F = 0 refused by name: no orientation); the Link's one number read at that end gives the lift. Returns the births as (the take's Node, the lift, the - child's Node, the + child's Node)."""
        born = []
        taken = gap0_start[0]  # the row the click takes: the massless plane's first line; its current orients the Link, its twist gives the handedness
        currents = [self.den * self.link_current(taken, 2 * axis) for axis in range(3)]
        twists = [self.twist(taken, axis) for axis in range(3)]
        for at in np.ndindex(*self.shape):
            if frozen[at]: continue
            for axis in range(3):
                j = tuple((at[a] + (1 if a == axis else 0)) % self.cube for a in range(3))
                if frozen[j] or int(sh[at]) < self.unit_gap0 or int(sh[j]) < self.unit_gap0: continue
                F = int(currents[axis][at])
                if F == 0:
                    self.counts['refused_orientation'] += 1; self.log.append({'event': 'refused', 'i': self.interval, 'node': list(at), 'cause': 'orientation', 'link': list(j)}); continue
                into, outof = (j, at) if F > 0 else (at, j)  # the end the current flows into: the draw and the take stay there
                h = int(twists[axis][at])
                if h == 0:
                    self.counts['refused_twist'] += 1; self.log.append({'event': 'refused', 'i': self.interval, 'node': list(at), 'cause': 'twist', 'link': list(j)}); continue
                plus, minus = (into, outof) if h > 0 else (outof, into)  # the + child at the end the current flows into where the twist is right-handed, at the other end where left-handed (the owner's sentence 4, PA2's form)
                drawn = self.read_number(into, rules)
                if drawn is None: continue
                number, room = drawn
                born.append((into, self.records().index(self.planes()[(number // self.unit_gap0) % len(self.planes())]), minus, plus, room))  # sr1: the plane drawn, as a record index  # the plane drawn, over every plane alike (the massless plane among them); the take at the current's end
        return born

    def refuse(self, born, owns):
        """The lay refused by name (ALGEBRA.md, The click writes on the lattice, line 186: the lay's Wronskian is exact only at an empty Node): where any of the child's family already stands at its Node, and where two children of one record would land at one Node in one close (the charge made at a crowded lay, W = n^2 A^2; a rule that reaches two Links, named open under the locality law). Returns the births kept."""
        kept = []
        for at, s_, minus, plus, room in born:
            if int(owns[s_][minus]) > 0 or int(owns[s_][plus]) > 0:
                self.counts['refused_lay'] += 1; self.log.append({'event': 'refused', 'i': self.interval, 'node': list(at), 'cause': 'lay', 'standing': int(owns[s_][minus]), 'unit': self.units[s_]}); continue
            kept.append((at, s_, minus, plus, room))
        landing = {}
        for at, s_, minus, plus, room in kept:
            landing[(s_, minus)] = landing.get((s_, minus), 0) + 1; landing[(s_, plus)] = landing.get((s_, plus), 0) + 1
        crowded = [k for k in kept if landing[(k[1], k[2])] > 1 or landing[(k[1], k[3])] > 1]
        for at, s_, minus, plus, room in crowded:
            self.counts['refused_lay'] += 1; self.log.append({'event': 'refused', 'i': self.interval, 'node': list(at), 'cause': 'lay', 'children_at_one_node': max(landing[(s_, minus)], landing[(s_, plus)])})
        return [k for k in kept if k not in crowded]

    def births(self, kept, r_gap0, c, factors, pace):
        """The births kept, every face read before any write: one exact take per Node of its children's walls summed, the start's light paying; then each child laid as one quantum of its record at the quarter turn (re_now A at the - end, im_before -A; re_now A at the + end, im_before +A), the birth logged with its numbers. Returns every Node a taken birth touched."""
        by_node = {}
        for at, s_, minus, plus, room in kept: by_node.setdefault(at, []).append((s_, minus, plus, room))
        taken = []
        for at in sorted(by_node):
            children = by_node[at]; walls = sum(2 * self.units[s_] for s_, _m, _p, _r in children)
            got = self.take_at(at, walls, r_gap0, len(children))
            if got is not None: taken.append((at, children, walls, got))
        for at, children, walls, (levels, fall, now) in taken:
            self.closes[at] -= 1  # the take counted once per child below
            dp_take = self.last_dp
            for s_, minus, plus, room in children:
                A = self.lay_amplitude(s_, at, c, factors, pace); re, im = self.records()[s_].lines; num = self.records()[s_].pair[0]
                dp_lay = [0, 0, 0]
                for where, sense in ((minus, -1), (plus, 1)):  # the conjugate pair onto the one plane, one child at each end; each lay's momentum booked (the re line's now by A, the im line's before by sense A)
                    for a, d in enumerate(self.momentum_of(re.now, re.before, where, d_now=A, num=num)): dp_lay[a] += d
                    for a, d in enumerate(self.momentum_of(im.now, im.before, where, d_before=sense * A, num=num)): dp_lay[a] += d
                    self.lay(s_, where, (A, 0, 0, sense * A))
                W_children = [int(re.now[w_] * im.before[w_] - im.now[w_] * re.before[w_]) for w_ in (minus, plus)]  # each child's sense is the sign of its own Wronskian at its Node (the owner's word 3)
                self.counts['births'] += 1; self.closes[at] += 1
                self.log.append({'event': 'birth', 'i': self.interval, 'node': list(at), 'line_pair': s_, 'senses': [-1, 1], 'W_children': W_children, 'minus': list(minus), 'plus': list(plus), 'taken': fall, 'booked': walls, 'levels': levels, 'light_now_was': now, 'proper': int(self.proper[at]), 'content': int(c[at]), 'amplitude': A, 'children_at_node': len(children), 'room': room, 'dP_take': dp_take, 'dP_lay': dp_lay})
            self.counts['taken'] += fall; self.counts['booked'] += walls
        return {at for at, _c, _w, _g in taken} | {m for _a, ch, _w, _g in taken for _s, m, _p, _r in ch} | {p_ for _a, ch, _w, _g in taken for _s, _m, p_, _r in ch}

    def bodies(self, gap0_start, plane_starts, owns, born_nodes, frozen, r_gap0):
        """The bodies' closing: a record standing at a whole quantum of its own unit through one period of its re line's upward crossings clicks (one take of its unit at the Node, the credit logged), a Node of a birth this interval or a frozen Node apart."""
        for rec in range(len(self.records())):
            s_ = rec
            standing_now = np.vectorize(lambda v: 1 if int(v) >= self.units[s_] else 0, otypes=[object])(owns[rec])
            self.standing[rec] = np.where(standing_now == 1, self.standing[rec] + 1, 0)
            re = self.records()[rec].lines[0]
            if self.records()[rec].shape == 8:  # sr1 flag: the row's beat is read covariantly, from the invariant ratio cos omega = N.G.B / N.G.N at the Node (no line of a spinor is a scalar under the 48, so no crossing line is covariant; the plane's re crossing is the case of scalar lines): the period P in intervals by Chebyshev's recurrence on the exact ratio, the first return of cos(k omega) to its maximum; the click when the record has stood one period
                self.beats[rec] = self.period8(self.records()[rec].lines, standing_now)
                closing = np.vectorize(lambda st, bt: 1 if (int(bt) > 0 and int(st) >= int(bt)) else 0, otypes=[object])(self.standing[rec], self.beats[rec])
                for at in zip(*np.nonzero(closing == 1)):
                    at = tuple(int(x) for x in at)
                    if at in born_nodes or frozen[at]: continue
                    got = self.take_at(at, self.units[s_], r_gap0, 1)
                    self.standing[rec][at] = 0
                    if got is None: continue
                    levels, fall, now = got
                    self.counts['body_clicks'] += 1
                    self.log.append(self.credit(rec, at, plane_starts, fall, levels, now))
                continue
            upward = np.vectorize(lambda b, n: 1 if (int(b) < 0 <= int(n)) else 0, otypes=[object])(re.before, re.now)
            counting = np.vectorize(lambda v: 1 if int(v) > 0 else 0, otypes=[object])(self.crossed[rec])
            self.beats[rec] = np.where((upward == 1) & (counting == 1), self.crossed[rec], self.beats[rec])
            self.crossed[rec] = np.where(upward == 1, 1, np.where(counting == 1, self.crossed[rec] + 1, 0))
            closing = np.vectorize(lambda st, bt: 1 if (int(bt) > 0 and int(st) >= int(bt)) else 0, otypes=[object])(self.standing[rec], self.beats[rec])
            for at in zip(*np.nonzero(closing == 1)):
                at = tuple(int(x) for x in at)
                if at in born_nodes or frozen[at]: continue
                got = self.take_at(at, self.units[s_], r_gap0, 1)
                self.standing[rec][at] = 0
                if got is None: continue
                levels, fall, now = got
                self.counts['body_clicks'] += 1
                self.log.append(self.credit(rec, at, plane_starts, fall, levels, now))

    def detect(self, gap0_start, r_gap0, pace, c):
        """The detectors, a reading and no act: the light's whole quanta at the Node risen over the interval (the start's share against the share as the click leaves the light), each quantum a light credit with the Node's proper count."""
        if not self.detectors: return
        z = self.row(2, gap=0).lines[0]; sh_end = self.share(z, r_gap0, pace, vacuum=True); sh_vac = self.share(gap0_start[0], r_gap0, pace, vacuum=True)
        for det in self.detectors:
            rise = int(sh_end[det]) // self.unit_gap0 - int(sh_vac[det]) // self.unit_gap0
            if rise > 0:
                self.counts['light_credits'] += rise
                self.log.append({'event': 'detector', 'i': self.interval, 'node': list(det), 'line': self.records().index(self.row(2, gap=0)), 'quanta': rise, 'proper': int(self.proper[det]), 'content': int(c[det]), 'light_now': int(z.now[det]), 'light_before': int(z.before[det])})

    def click(self, plane_starts, held):
        """The click (ALGEBRA.md, The click writes on the lattice), the Node's fourth act: the readings at the start (the rules of every row, the massless row's share and each record's standing share at the vacuum's weight, the frozen Nodes), the Link close (`meet`), the lays refused by name (`refuse`), the births taken and laid (`births`), the bodies' closing (`bodies`), the detectors' credits (`detect`); `gap0_start` and `plane_starts` the massless row's line and the planes' lines at the interval's start. The one-Link read of a number takes every row's first line and a plane's both (the former toy's digit set, kept until the Boss's word on reading every line)."""
        c = self.start_content; factors = self.link_factors()
        massless = self.row(2, gap=0); r_gap0 = self.rule_of(massless, c, factors); gap0_start = plane_starts[self.records().index(massless)]
        if self.control.get('digits') == 'former':  # the former digit set, kept by name under the key: the shape-4 and shape-10 rows' first lines after the step, the planes' lines at the start
            rules = [(r.lines[0], self.rule_of(r, c, factors)) for r in (self.row(4), self.row(10))]
            for rec, r in enumerate(self.records()):
                rules += [(l, self.rule_of(r, c, factors)) for l in plane_starts[rec]]
        else:  # A2, the default (the owner's word of 2026-10-25, "go with A if it is generic and solves"; the Boss's ruling of 10:1x): the one-Link read takes every line of every row at the interval's start, alike
            rules = [(l, self.rule_of(r, c, factors)) for r, lines in zip(self.rows_, held) for l in lines]
        pace = paces.link_pace_of(self.gamma, c)
        owns = []  # every plane's standing share at the interval's start at the vacuum's weight (V-D, the owner's sentence 7): the meeting's threshold on the massless plane, the lay's refusal on the lift's
        for rec, r in enumerate(self.records()):
            rr = self.rule_of(r, c, factors)
            if r.shape == 8: owns.append(self.share8(plane_starts[rec], self.rule(r.pair, c, factors), pace, vacuum=True)); continue  # sr1 flag: the row's share G-weighted at the unscaled rule
            re0, im0 = plane_starts[rec]
            owns.append(self.share(re0, rr, pace, vacuum=True) + self.share(im0, rr, pace, vacuum=True))
        sh = owns[self.records().index(massless)]
        frozen = np.asarray(pace, dtype=object) == 0 if np.ndim(pace) else np.zeros(self.shape, dtype=bool)
        born_nodes = self.births(self.refuse(self.meet(gap0_start, sh, rules, frozen), owns), r_gap0, c, factors, pace)
        self.bodies(gap0_start, plane_starts, owns, born_nodes, frozen, r_gap0)
        self.detect(gap0_start, r_gap0, pace, c)

    def lay_amplitude(self, s_, at, c, factors, pace):
        """The lay of one quantum: the child's record laid at the Node with the least amplitude A at which its own share reads one quantum of its unit at the Node's paces, (2 D + SUM_j R_j) A^2 >= unit x 4 p^2 G^2 (the frame share's term of a lone record with now = before = A; ALGEBRA.md, the lay of the record out whole); the former toy laid the root of T / 2 for every species."""
        r = self.rule_of(self.records()[s_], c, factors)  # the record's pair
        D = 2 * int(np.asarray(r.wall)) - int(np.asarray(r.self_coefficient)[at]) - sum(int(np.asarray(x)[at]) for x in r.reaches)  # D from S = 2 w - D - SUM R
        C = 2 * D + sum(int(np.asarray(x)[at]) for x in r.reaches)
        pc = int(np.asarray(pace, dtype=object)[at]); target = self.units[s_] * 4 * pc * pc * self.G * self.G
        if C <= 0: return self.A
        A = rule3.largest_below(target // C)
        while C * A * A < target: A += 1
        return A

    def credit8(self, rec, at, plane_starts, fall, levels, light_was):
        """sr1: the credit line of a shape-8 record: the Node, the proper count, the beat, the row's charge W (its sense), its spin density s (the axial vector, signed per axis) and spin Wronskians at the Node, the take."""
        lines = self.records()[rec].lines
        W, s, sw = self.bilinears8(lines)
        Wn = int(W[at]); sn_ = [int(x[at]) for x in s]; swn = [int(x[at]) for x in sw]
        return {'event': 'credit', 'i': self.interval, 'node': list(at), 'proper': int(self.proper[at]), 'closes': int(self.closes[at]), 'content': int(self.start_content[at]), 'line': rec, 'sense': 1 if Wn > 0 else -1 if Wn < 0 else 0,
                'beat': int(self.beats[rec][at]), 'W': Wn, 'spin': sn_, 'spin_sign': [1 if x > 0 else -1 if x < 0 else 0 for x in sn_], 'spin_wronskian': swn, 'levels8': [int(l.now[at]) for l in lines], 'taken': fall, 'levels': levels, 'light_now_was': light_was, 'dP_take': self.last_dp, 'sign_level': int(self.row(4).lines[0].now[at]), 'turned': bool(self.turned[at])}

    def credit(self, rec, at, plane_starts, fall, levels, light_was):
        if self.records()[rec].shape == 8: return self.credit8(rec, at, plane_starts, fall, levels, light_was)  # sr1 flag
        re, im = self.records()[rec].lines; re0, im0 = plane_starts[rec]
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
                'beat': int(self.beats[rec][at]), 'frame': frame, 'taken': fall, 'levels': levels, 'light_now_was': light_was, 'dP_take': self.last_dp, 'sign_level': int(self.row(4).lines[0].now[at]), 'turned': bool(self.turned[at])}


    def unclick(self, frame):
        """The close undone from the log, in the reverse order of its lines: the lays removed, the light restored, the readings' counters restored."""
        z = self.row(2, gap=0).lines[0]
        for entry in reversed(self.log[frame['log_from']:]):
            at = tuple(entry['node'])
            if entry['event'] == 'birth':
                s_ = entry['line_pair']; A = entry['amplitude']
                self.lay(s_, tuple(entry['minus']), (A, 0, 0, -A), -1); self.lay(s_, tuple(entry['plus']), (A, 0, 0, A), -1)
                z.now[at] = entry['light_now_was']; self.closes[at] -= 1
            elif entry['event'] == 'credit':
                z.now[at] = entry['light_now_was']; self.closes[at] -= 1
        del self.log[frame['log_from']:]
        self.standing, self.crossed, self.beats = frame['counters']

    def census(self):
        arrays = [a for l in self.all_lines() for a in (l.now, l.before, l.rem)] + [l.wr for l in self.all_lines() if l.wr is not None] + self.standing + self.crossed + self.beats + [self.proper, self.closes]
        bits = max(int(np.max(np.vectorize(lambda v: abs(int(v)).bit_length(), otypes=[object])(a))) for a in arrays)
        return len(arrays), bits

    def state_hash(self):
        """The state's hash with the interval, the run back's bit-for-bit comparison."""
        import hashlib
        return hashlib.sha256(self.state_bytes() + str(self.interval).encode()).hexdigest()

    def state_bytes(self):
        return b''.join(np.asarray(a, dtype=object).astype(str).tobytes() for l in self.all_lines() for a in (l.now, l.before, l.rem)) + b''.join(np.asarray(l.wr).astype(str).tobytes() for l in self.all_lines() if l.wr is not None)


def reading(b, maxbits):
    """The reader's row of the record at an interval: the readings a reader takes of the whole board (no act): the packets' centroids and spreads, the content's and the volume's ranges, the counts, the integers and bits, the sign's level, the planes' energy, the tensions' range, the Links at the wall, the Links' count, the orbit table's size, the board's Wronskian, the light's velocity."""
    metric, potential, massless, planes = b.row(10), b.row(4), b.row(2, gap=0).lines[0], [r.lines for r in b.records()]
    c = b.content(); cs = [int(x) for x in c.reshape(-1)]; vs = [int(x) for x in metric.lines[0].now.reshape(-1)]
    energy = sum(int(x) * int(x) for rec in planes for l in rec for x in l.now.reshape(-1)); odd_max = max(abs(int(x)) for l in potential.lines[1:4] for x in l.now.reshape(-1))
    light_v = max(abs(int(a) - int(bb)) for a, bb in zip(massless.now.reshape(-1), massless.before.reshape(-1)))
    packets = {}
    for rec, lines_ in enumerate(planes):
        if b.records()[rec].gap == 0: continue  # the reader skips the massless plane (the sea fills the board)
        if len(lines_) == 8: wgt = gform8(SR1['G'], [l.now for l in lines_], [l.now for l in lines_])  # sr1 flag: the row's weight G-weighted
        else: re, im = lines_; wgt = re.now * re.now + im.now * im.now
        total = int(sum(int(x) for x in wgt.reshape(-1)))
        if total == 0: continue
        idx = np.indices(b.shape); cen = [int(sum(int(w) * int(x) for w, x in zip(wgt.reshape(-1), idx[a].reshape(-1)))) * 1000 // total for a in range(3)]
        if True:
            packets['plane %d' % rec] = {'centroid (thousandths of a Link)': cen, 'nodes with levels': int(sum(1 for x in wgt.reshape(-1) if int(x) > 0)), 'energy bits': total.bit_length()}
    W = Z(b.shape)
    for lines_ in planes: W = W + (b.bilinears8(lines_)[0] if len(lines_) == 8 else wronskian(*lines_))  # sr1 flag
    n, _bits = b.census(); tens = [int(x) for l in metric.lines[1:4] for x in l.now.reshape(-1)]
    return {'i': b.interval, 'packets (reader)': packets, 'content min/mean/max': [min(cs), sum(cs) // len(cs), max(cs)], 'volume mean': sum(vs) // len(vs), 'births': b.counts['births'], 'body_clicks': b.counts['body_clicks'],
            'refused': b.counts['refused_stop'] + b.counts['refused_origin'] + b.counts['refused_lay'] + b.counts['refused_orientation'] + b.counts['refused_twist'], 'refused_lay': b.counts['refused_lay'], 'refused_orientation': b.counts['refused_orientation'], 'turns': b.counts['turns'],
            'integers': n, 'max bits': maxbits, 'max transient bits': b.max_transient, 'sign level max': max(abs(int(x)) for x in potential.lines[0].now.reshape(-1)), 'planes energy bits': energy.bit_length(),
            'links at the wall': int(sum(1 for f in b.link_factors()[0::2] for x in f.reshape(-1) if int(x) == 0)), 'tension min/max': [min(tens), max(tens)], 'odd max bits': odd_max.bit_length(), 'link count max': b.count_max, 'orbit table': len(b.orbit),
            'massless W abs max': int(max(abs(int(x)) for x in wronskian(*b.row(2, gap=0).lines).reshape(-1))), 'W total': int(sum(int(x) for x in W.reshape(-1))), 'W abs sum': int(sum(abs(int(x)) for lines_ in planes for x in (b.bilinears8(lines_)[0] if len(lines_) == 8 else wronskian(*lines_)).reshape(-1))), 'light velocity max': light_v}


def record(universe, world, back=0, out=print):
    """The writer: the world's intervals run, a reader's row at every twelfth and two early marks, then N intervals run back and compared bit for bit by the state's hash (the arrow's reading on the record); returns the record (the two files, the constants, the counts, the turns, the rows, the run back and the log as the run left it)."""
    import time
    b = Lean(universe, world); intervals = int(world['intervals']); t0 = time.monotonic_ns()
    marks = sorted({1, intervals} | {(k * intervals) // 12 for k in range(1, 12)} | {intervals // 60, intervals // 24})
    rows = []; hashes = []; maxbits = 0
    for t in range(intervals):
        if back and t >= intervals - back: hashes.append(b.state_hash())
        b.step(); maxbits = max(maxbits, b.census()[1])  # the largest integer of the state over the whole run
        if b.interval in marks:
            rows.append(dict(reading(b, maxbits), milliseconds=(time.monotonic_ns() - t0) // 1000000)); out(json.dumps(rows[-1]))
    kept_log = list(b.log)  # the record's log as the run left it; the run back below removes its lines as it undoes them
    run_back = None
    if back:
        exact = 0
        for k in range(back):
            b.step_back(); exact += (b.state_hash() == hashes[back - 1 - k])
        run_back = {'intervals': back, 'exact': exact}; out(json.dumps({'run back': run_back}))
    out(json.dumps({'counts': {k: str(v) for k, v in b.counts.items()}}))
    return {'world': world, 'universe': universe, 'den': b.den, 'cube': b.cube, 'intervals': intervals, 'lifts': [(None, str(r.pair[0]), str(sine_den(r.pair[0], b.den))) for r in b.lifts], 'planes': [str(r.pair[0]) for r in b.records()], 'T': b.T, 'gamma': b.gamma, 'G': b.G,
            'counts': {k: str(v) for k, v in b.counts.items()}, 'turns': b.turns, 'rows': rows, 'run_back': run_back, 'log': kept_log}


if __name__ == '__main__':
    sys.set_int_max_str_digits(0)
    # usage: lean_full.py <world.json> <out.json> [back N]
    universe, world = load_world(sys.argv[1])
    found = record(universe, world, int(sys.argv[sys.argv.index('back') + 1]) if 'back' in sys.argv else 0, lambda line: print(line, flush=True))
    json.dump(found, open(sys.argv[2], 'w'))
