"""gn2's FLAGGED COPY (2026-10-25) of David's lean toy (toys-5 at c74322851) for the gap-0 picks and the picks by shape number: make_copy.py names every delta; David's file under toy_former/ is untouched; every flag off is David's path bit for bit.
David's local lean Node, complete (the owner's word, 04:4x: run everything, omit nothing). Every act of the law's interval at a generic Node of a fixed state, the engine's exact primitives (core.rule3, core.paces, features.phase, loader.circle), the architecture the toy's.

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

GN2 = {k: os.environ.get('GN2_' + k, 'off') for k in ('TURN', 'EMIT', 'CLICK', 'SEA', 'ROWS')}  # gn2's flags, every one off = David's path

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
            return [Line(Z(S), Z(S), Z(S) + self.w // 2, self.w, None if ww is None else Z(S) + ww // 2, ww) for ww in wwalls]
        self.rows_ = []; self.by_index = []  # the rows in the file's order (a lay names a row by its index in the file)
        for r in universe['rows']:
            shape_ = int(r['shape']); pair = None if r.get('pair') is None else (int(r['pair'][0]), int(r['pair'][1])); wall = None if r.get('wall') is None else int(r['wall'])
            if shape_ == 1 and wall is None: raise ValueError('a shape-1 row with a pair: light is the plane whose pair is (den, den) (U-S2, the owner\'s word of 2026-10-25), no fourth shape')
            self.rows_.append(Row(shape_, pair, wall, lines_of(shape_, pair, wall))); self.by_index.append(self.rows_[-1])
        # the acts' order: a row whose write reads other rows comes after them: the row with its own wall, the planes with a gap, the plane at the gap 0 (its lay reads the planes' Wronskian), the shape-4 row, the shape-10 row
        order = (lambda r: 0 if r.wall is not None else {2: 1 + (r.gap == 0), 4: 3, 10: 4}.get(r.shape, 5)) if GN2['ROWS'] == 'off' else (lambda r: (0, 0, 0) if r.wall is not None else (1, r.shape, 1 if r.gap == 0 else 0))  # gn2 ROWS=rank: no number: the walled row first, then the pair rows by rising shape (a row of more lines is written from the rows of fewer), the gap-0 plane after the gapped planes
        self.rows_.sort(key=order)
        if sum(1 for r in self.rows_ if r.wall is not None) != 1 or len([r for r in self.rows_ if r.shape == 2 and r.gap == 0]) != 1 or len([r for r in self.rows_ if r.shape == 10]) != 1 or len([r for r in self.rows_ if r.shape == 4]) != 1:
            raise ValueError('the universe names one row with its own wall, one massless plane (shape 2 at the gap 0), one shape-10 row and one shape-4 row')
        if self.carrier().pair != (den - den // gamma, den): raise ValueError('the shape-10 row is the clock\'s one level: its pair (den - den div Gamma, den)')
        if self.potential().pair != (den, den): raise ValueError('the shape-4 row stands at (den, den)')
        # the planes (shape 2): every one a record of two lines; the massless plane among them; the lifts the planes with a gap, in the file's order (the draw's list); each plane's quantum its unit: 3 T s for a plane with a gap (s the pair's sine), 3 T den for the plane at the gap 0 (the drift's double root)
        self.lifts = [r for r in self.records() if r.gap > 0]
        self.pairs = [r.pair for r in self.lifts]
        self.nl = len(self.pairs)
        if self.nl == 0: raise ValueError('the universe names no plane row with a gap')
        self.units = [self.unit_of(r.pair) for r in self.records()]  # gn2 pick 5: one function of the pair
        nr = len(self.records()); self.standing = [Z(S) for _ in range(nr)]; self.crossed = [Z(S) for _ in range(nr)]; self.beats = [Z(S) for _ in range(nr)]
        self.proper = Z(S); self.closes = Z(S)
        self.interval = 0; self.log = []; self.turns = []; self.stack = []
        for l in self.carrier().lines[:1]: l.now[:] = gamma; l.before[:] = gamma  # the metric's time line at the vacuum's level
        self.unit_gap0 = self.units[self.records().index(self.row(2, gap=0))]  # the massless plane's quantum, W_c = 3 den T
        self.detectors = []  # the Nodes whose light the record credits (the world names them; a reading, no state)
        # the seed as the world lays it: a list of lays in the three forms of the law and no fourth (the owner's word of 2026-10-25, "2, 3, 4 approved"; the Z hands' form): `sea` lays the massless row's drift v, the largest integer with v^2 <= T, at every Node; `hole` takes it back at one Node; `at` lays a packet: on the massless row N drifts at the centre, on a plane row the conjugate pair, N quanta each record, over the raised cosine's envelope of the half-width 2 or 3 (exact in integers there and at no other width below 6). Refused by name: a fourth form, a row no pair of the universe carries, a sea of a plane row, a Node off the board, a plane packet of another width (a body is laid over its packet, never one Node)
        self.drift = rule3.largest_below(action)
        packets = []
        for lay in world.get('seed', []):
            form = lay.get('lay'); r_ = self.by_index[int(lay['row'])] if 'row' in lay else None  # the row by its index in the universe file (the Boss's ruling of 2026-10-25: the index names it, not the pair)
            if r_ is not None and r_.shape != 2: raise ValueError('a lay is onto a plane (shape 2)')
            if form == 'sea':
                if r_.gap != 0 and GN2['SEA'] == 'off': raise ValueError('a sea is the massless plane\'s alone: the drift is its double root')
                if r_.gap != 0:  # gn2 pick 4 (SEA=named): the sea of a gapped row is its drift laid at its own band's rest at every Node, both senses: the standing level A = v den div gap per sense (now - before = v at the rest rotation), re_now += 2 A, re_before += 2 (A num div den), the im lines cancelling (the charge 0): the k = 0 mode of the band, an oscillation of the whole board at omega_0, no double root
                    re_, im_ = r_.lines; A_ = (self.drift * self.den) // r_.gap
                    re_.now[:] = re_.now + 2 * A_; re_.before[:] = re_.before + 2 * ((A_ * r_.pair[0]) // self.den)
                else:
                    z = r_.lines[0]; z.now[:] = z.now + self.drift
            elif form == 'hole':
                at = self.node_of(lay['at']); z = self.row(2, gap=0).lines[0]; z.now[at] = z.now[at] - self.drift
            elif form == 'at':
                n = int(lay['quanta']); at = self.node_of(lay['centre'])
                if r_.gap == 0: z = r_.lines[0]; z.now[at] = z.now[at] + n * self.drift
                else: packets.append((self.records().index(r_), at, int(lay.get('width', 0)), n))
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
                    m = self.carrier().lines[0]; m.now[node] = int(np.asarray(volform.volume_of(gamma, np.array([c], dtype=object)), dtype=object).reshape(-1)[0]); m.before[node] = m.now[node]
        self.detectors = [self.node_of(d) for d in world.get('detectors', [])]
        self.A = rule3.largest_below(action // 2)  # the lay's amplitude where the rule's form has no positive term (a lone record's share cannot be read there)
        self.X = phase.amplitude(phase.unit(gamma), WIDTH // 2 - 1)  # the phase pair's amplitude from half the law's width less one, so that a pair's product with a level stays within the width
        seed_pair = phase.seed(self.X, gamma)
        self.orbit_lines = [seed_pair]  # the last pair as lines, for the next act
        self.orbit = [(int(seed_pair[0][0]), int(seed_pair[1][0]))]  # the table of (cos, sin) as plain integers
        self.couplings = {}  # gn2 TURN=scaled: K = omega_0 Gamma per pair, found once on the orbit
        self.link_counts = None  # gn2: the Links' counts of the interval, for the scaled turn
        self.counts = {'births': 0, 'taken': 0, 'booked': 0, 'body_clicks': 0, 'refused_stop': 0, 'refused_origin': 0, 'refused_lay': 0, 'refused_orientation': 0, 'refused_twist': 0, 'turns': 0, 'light_credits': 0, 'light_laid': 0, 'light_laid_nodes': 0, 'met_gapped': 0}
        self.max_transient = 0
        for s_, at, h, n in packets: self.lay_packet(s_, at, h, n)
        if self.control.get('ride') == 'symmetric':  # the symmetric ride: a riding line's remainder lives at the mean wall (w div 2)(X_before + X_now) of the carrier's two levels at its Node, half of it at the seed
            W0 = (self.w // 2) * (self.carrier().lines[0].before + self.carrier().lines[0].now)
            for r in self.rows_:
                if r.wall is None and r is not self.carrier():
                    for l in r.lines: l.wall = W0; l.rem = W0 // 2

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
        return [r for r in self.rows_ if r.shape == 2]

    def carrier(self):
        """gn2 section 2: the carrier of the wall. off: David's row(10). rank: the pair row with the most lines (the symmetric tensor's ten components), no number."""
        if GN2['ROWS'] == 'off': return self.row(10)
        return max((r for r in self.rows_ if r.wall is None), key=lambda r: r.shape)

    def potential(self):
        """gn2 section 2: the potential's row. off: David's row(4). rank: the pair row with the most lines after the carrier (the vector's four components), no number."""
        if GN2['ROWS'] == 'off': return self.row(4)
        c = self.carrier()
        return max((r for r in self.rows_ if r.wall is None and r is not c), key=lambda r: r.shape)

    def unit_of(self, pair):
        """gn2 pick 5: the quantum of a plane as one function of its pair (row 12 of The conventions and the units): 3 T s, s the pair's sine, for a pair with a gap; 3 T den at (den, den) (W_c, the massless case by number: the owner's 1)."""
        num, den = pair
        return 3 * self.T * (sine_den(num, den) if num != den else den)

    def coupling_of(self, pair):
        """gn2 pick 1 (TURN=scaled): the plane's coupling to the Link's phase, K = omega_0 Gamma in the orbit's counts (Y-S1): the least count m at which the orbit's cosine over X falls to num over den, by comparisons of integers on the one orbit table; 0 at (den, den), a theorem."""
        num, den = pair
        if num >= den: return 0
        if num in self.couplings: return self.couplings[num]
        m = 0
        while self.pair_angle(m)[0] * den > num * self.X: m += 1
        self.couplings[num] = m
        return m

    def turn_of(self, r, phases, odd, frames):
        """gn2 pick 1: what turns a plane's arrivals. off: David's branch (the plane at the gap 0 turned by nothing, every other plane by the Link's pair and the odd tangent at the coupling 1). all: the branch removed, one turn on every plane alike at the coupling 1. scaled: one turn on every plane alike at the plane's own coupling K = omega_0 Gamma over Gamma (the count and the odd part scaled with one rounding each): K = 0 at (den, den) is the identity with no branch."""
        if GN2['TURN'] == 'off': return None if r.gap == 0 else (phases, odd, frames)
        if GN2['TURN'] == 'all': return (phases, odd, frames)
        return (phases, odd, frames, self.coupling_of(r.pair))

    def emits(self, r, potential):
        """gn2 pick 2: whether a plane's first line takes W-S1 (the planes' Wronskian change). off: David's, the plane at the gap 0. pair: the plane whose pair is the Wronskian-writer's pair (the potential's row), a function of the pairs and no pick by the gap."""
        if GN2['EMIT'] == 'off': return r.gap == 0
        return r.pair == potential.pair

    def emitter(self):
        """gn2 pick 2: the plane W-S1 lights, by the pairs (EMIT=pair) or by the gap 0 (off)."""
        if GN2['EMIT'] == 'off': return self.row(2, gap=0)
        return next(r for r in self.records() if r.pair == self.potential().pair)

    def rule_of(self, r, c, factors):
        """A row's rule: Rule3's integers at its pair and the Node's paces, or, for the row with its own wall, no Links and the own weight 2 w (next = 2 now - before + the write inside the division)."""
        return rule3.Rule(tuple(0 for _ in AXES), 2 * r.wall, r.wall, 0) if r.wall is not None else self.rule(r.pair, c, factors)

    def lay_packet(self, rec, at, h, n):
        """The `at` lay of a plane row: the conjugate pair (the two records at the senses -1 and 1) laid at rest over the raised cosine's envelope of the half-width h (the weights 2, 1 at h = 2; 4, 3, 1 at h = 3; the product over the three axes), each record at the largest amplitude A at which its share at the vacuum's weight, summed over the packet, is at most n quanta of its unit (a search by comparisons); each Node's lines at the band's rest rotation: re_now = A w_i div w_0, re_before = re_now num div den, im_now = 0, im_before = sense re_now s div den with s the pair's sine (Z1's form)."""
        weights = {2: (2, 1), 3: (4, 3, 1)}.get(h)
        if weights is None: raise ValueError('a plane packet has the half-width 2 or 3: a body is laid over its packet')
        r_ = self.records()[rec]; num = r_.pair[0]; sn = sine_den(num, self.den); w0 = weights[0] ** 3  # the pair's numbers
        envelope = Z(self.shape)
        for j in np.ndindex(*(2 * h - 1,) * 3):
            off = [x - (h - 1) for x in j]
            envelope[tuple((at[a] + off[a]) % self.cube for a in range(3))] += weights[abs(off[0])] * weights[abs(off[1])] * weights[abs(off[2])]
        c = self.content(); factors = self.link_factors(); r = self.rule_of(r_, c, factors); self.start_content = c
        def record(A, sense):
            re_now = (A * envelope) // w0
            return Line(re_now, (re_now * num) // self.den, None, self.w), Line(Z(self.shape), sense * ((re_now * sn) // self.den), None, self.w)
        def share_of(A):
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
        for sense in (-1, 1):  # the conjugate pair laid onto the one plane: at one Node the two senses superpose (the im lines cancel, the record neutral)
            re, im = record(low, sense); self.lay(rec, Ellipsis, (re.now, re.before, im.now, im.before))
        self.log.append({'event': 'lay', 'i': 0, 'node': list(at), 'line_pair': rec, 'width': h, 'quanta': n, 'amplitude': low, 'share': share_of(low), 'unit': self.units[rec], 'nodes': int(sum(1 for x in envelope.reshape(-1) if int(x) > 0))})

    # ---- the readings at the interval's start
    def content(self): return np.asarray(volform.level_of(self.gamma, self.carrier().lines[0].now), dtype=object)
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
        axis_levels = [l.now for l in self.carrier().lines[1:4]] if axis_levels is None else axis_levels
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
        found = []; counts = []
        for port in range(6):
            n = K - frames[port] * across(K, port)
            pairs = np.vectorize(self.pair_angle, otypes=[object, object])(n)
            found.append((pairs[0], pairs[1])); counts.append(n)
        self.link_counts = counts  # gn2: kept for the scaled turn
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
        phases, odd, frames = turn[:3]; axis, side = AXES[port]
        re_j, im_j = arrivals
        im_j = frames[port] * im_j
        c, s = phases[port]
        _e, (n,), _f = link(port, odd=[odd[axis]])
        if len(turn) == 4:  # gn2 TURN=scaled: the Link's count and the odd part at the plane's own coupling K over Gamma, one rounding each (K = 0 at the gap 0: the identity)
            K = turn[3]; scaled = np.vectorize(lambda v: (1 if int(v) >= 0 else -1) * ((2 * abs(int(v)) * K + self.gamma) // (2 * self.gamma)), otypes=[object])
            pairs = np.vectorize(self.pair_angle, otypes=[object, object])(scaled(self.link_counts[port])); c, s = pairs[0], pairs[1]; n = scaled(n)  # the odd line on the Link: the two ends' sum signed by the Port's side (the engine's V_ij = V_a(i) + V_a(j); no division, the mirror exact)
        Wl = 4 * self.gamma; tc, ts, tw = Wl * Wl - n * n, 2 * Wl * n, Wl * Wl + n * n
        a_re = (c * re_j - s * im_j); a_im = (s * re_j + c * im_j)
        a_re, a_im = (2 * a_re + self.X) // (2 * self.X), (2 * a_im + self.X) // (2 * self.X)
        b_re = (tc * a_re - ts * a_im); b_im = (ts * a_re + tc * a_im)
        return [(2 * b_re + tw) // (2 * tw), (2 * b_im + tw) // (2 * tw)]

    def rotate(self, lines, r, turn=None, direction=1, flux=None, starts=None):
        """Rule3's step of one row at every Node, the one function of a line: for each line the total S now - w before + SUM_j R_j m_j (+ the line's flux where the row carries its write inside the division, the phase row) with m_j the row's arrivals at the Port turned as the row's shape turns them (`turned_arrival`), one carried division at the wall w per line; the rule's integers r at the Node's paces. Backward (direction -1) the same act on the before slots with the division's direction -1: the known part S now + SUM R m from the start levels, the quotient next + before, before = quotient - next."""
        at = [l.now if direction == 1 else l.before for l in lines] if starts is None else starts  # the start level: forward the now slot; backward the before slot (or the start levels given: at a turned Node the pre-state's now)
        totals = [r.self_coefficient * a - (r.wall * l.before if direction == 1 else 0) + (0 if flux is None else f) + m for l, a, f, m in zip(lines, at, flux or [0] * len(lines), self.arrivals(at, r, turn))]
        found = []
        for l, a, t in zip(lines, at, totals):
            if direction == 1: self.max_transient = max(self.max_transient, int(np.max(np.vectorize(lambda v: abs(int(v)).bit_length(), otypes=[object])(t))))
            quotient, rem = carried_division(t, r.wall, l.rem, direction)
            found.append(Line(quotient, l.now, rem, l.wall, l.wr, l.wwall) if direction == 1 else Line(a, quotient - l.now, rem, l.wall, l.wr, l.wwall))
        return found

    def arrivals(self, at, r, turn):
        """The Links' part of Rule3's total for a row's lines at every Node, SUM_j R_j m_j, the arrivals at each Port turned as the row's shape turns them."""
        totals = [0] * len(at)
        for port, reach in enumerate(r.reaches):
            found = self.turned_arrival([across(a, port) for a in at], port, turn)
            totals = [t + reach * m for t, m in zip(totals, found)]
        return totals

    def odd_round(self, q, d):
        """round(q / d) to the nearest for q odd and d even (never a half): (2 q + d) div (2 d); the odd rounding of the ride's momenta (R5)."""
        return (2 * q + d) // (2 * d)

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
            self.restore(start, kept, top)
        return start, levels, start

    def restore(self, lines, kept, top):
        """Backward at the turned Nodes `top`: the row set to `kept`, the pre-state the exchange returned (the inverse at a turned Node is no act)."""
        for l, k in zip(lines, kept):
            l.now, l.before, l.rem = np.where(top, k.now, l.now), np.where(top, k.before, l.before), np.where(top, k.rem, l.rem)
            if np.ndim(k.wall): l.wall = np.where(top, k.wall, l.wall)
            if l.wr is not None: l.wr = np.where(top, k.wr, l.wr)

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
        for line, h, im in zip(self.all_lines(), [l for row in held for l in row], self.is_im()):
            sgn = -1 if im else 1
            line.now, line.before, line.rem = np.where(top, sgn * h.before, line.now), np.where(top, sgn * h.now, line.before), np.where(top, h.rem if im else h.wall - 1 - h.rem, line.rem)
            if np.ndim(h.wall): line.wall = np.where(top, h.wall, line.wall)  # the riding remainder's own wall, the Node's (symmetric in the two levels, so the exchange keeps it)
            if line.wr is not None: line.wr = np.where(top, line.wwall - 1 - h.wr, line.wr)

    def swap(self, held):
        """The swap at the top (ALGEBRA.md, the fifth act): the weak maximum X0 <= X1 >= X2 with one strict (the held before, the held now, the now after the writes), or the floor (X0 or X2 below X_f); the turned Node ends the interval at the state it started from, exchanged and complemented, the step's output discarded there."""
        k = self.rows_.index(self.carrier()); x0, x1, x2 = held[k][0].before, held[k][0].now, self.carrier().lines[0].now
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
        metric, walled, potential, massless, records = self.carrier(), self.walled(), self.potential(), self.emitter(), self.records()  # gn2: the rows by what they are (the finders), not by their numbers
        # the readings at the start
        c = np.asarray(volform.level_of(self.gamma, at(metric.lines[0])), dtype=object); self.start_content = c
        p0 = paces.clock_of(self.gamma, c); self.proper = self.proper + direction * p0
        factors = self.link_factors([at(l) for l in metric.lines[1:4]]); self.start_factors = factors
        frames = self.frames(walled.lines[0].rem); self.start_frames = frames
        cphi = paces.rounded(at(potential.lines[0]) * p0, self.gamma)  # the clocked potential at the potential's start level
        out = [None] * len(rows); ends = lambda k: (top, None if kept is None else kept[k])
        if self.control.get('ride') == 'symmetric': return self.ride(direction, top, held, kept, at, c, p0, factors, frames, cphi, rows, where, out, ends)
        riding = records + ([potential] if self.control.get('metric_sources') == 'every riding row' else [])  # the rows whose form and tensions source the metric's write: the planes alone, or every row that divides at the carrier's wall (the shape-4 row too; the Boss's 2(a), measured against the planes alone)
        trace, traceless = tensor_parts(stress_parts([(at(l), r.pair[0]) for r in riding for l in r.lines], self.shape))
        forms = Z(self.shape); W_start = Z(self.shape); W = Z(self.shape); J = [Z(self.shape) for _ in range(3)]; plane_starts = []; stepped = []; phases = odd = None
        # one loop over the rows in the acts' order, one act on every row alike; what a row's write reads and what turns its arrivals is a function of its shape and its pair (the law's table): the walled row carries its write 2 c_phi inside its division and gives the Links' count; a plane with a gap is turned by the Link's pair and the odd tangent, the plane at the gap 0 by nothing (K = omega_0 Gamma = 0) and its first line takes W-S1 (the planes' Wronskian change, the planes acted before it); the shape-4 row's time line takes 2 W and its other lines the planes' current; the shape-10 row's time line takes every riding row's form less the pressure and its axis lines the traceless stress, its other lines nothing
        for r in self.rows_:
            k = where(r); rule = self.rule_of(r, c, factors); turn = None; flux = None; numerators = [None] * r.shape
            if r.wall is not None: flux = [2 * cphi]
            elif r.shape == 2:
                turn = self.turn_of(r, phases, odd, frames)  # gn2 pick 1
                if self.emits(r, potential): numerators = [W - W_start, None]  # gn2 pick 2
            elif r.shape == 4: numerators = [2 * W, *J]
            elif r.shape == 10:
                if self.hold_volume: out[k] = rows[k]; continue  # the control: the metric's row held by hand, no act on it in either direction
                X = at(r.lines[0]); p02 = p0 * p0
                numerators = [4 * X * (forms * 54 * self.den * self.gamma ** 2 - trace * p02) * p0] + [traceless[a] * p02 for a in range(3)] + [None] * (r.shape - 4)
            start, levels, out[k] = self.act(rows[k], rule, turn, numerators, direction, flux, *ends(k))
            if r in riding:  # the form of every line that rides the carrier, read for the metric's write
                for l0, lv in zip(start, levels): forms = forms + (l0.now * l0.now - lv * l0.before)
            if r.wall is not None:  # the Links' count from the walled row at the start, the phase pair and the odd tangent for the planes' turn
                K = self.centred_count(cphi, start[0])
                self.count_max = max(int(abs(int(x))) for port in range(6) for x in (K - frames[port] * across(K, port)).reshape(-1))  # the Links' count's size this interval (a reading)
                phases = self.link_phases(frames, K); odd = [at(l) for l in potential.lines[1:4]]
                self.start_phases, self.start_odd = phases, [o.copy() for o in odd]
            elif r.shape == 2:  # a plane's readings for the writes after it: its Wronskian before and after the step, its current
                re, im = start; W_start = W_start + wronskian(re, im)
                after = out[k] if direction == 1 else held[k]  # the plane as the step left it
                W = W + wronskian(*after); stepped.append([l.copy() for l in after]); plane_starts.append(start)
                for a, j_a in enumerate(plane_current(re, im, frames)): J[a] = J[a] + j_a
                if self.emits(r, potential) and direction == 1:  # the emission's size, a reading of the run: the levels laid on the massless line and the Nodes they were laid at (gn2 pick 2)
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

    def ride(self, direction, top, held, kept, at, c, p0, factors, frames, cphi, rows, where, out, ends):
        """The symmetric ride (R5's form; the owner's approved sentence 1 of 2026-10-25, "the held carrier of the wall and EVERY riding row step as one pair at the mean wall"), behind the world file's key `ride`: the one row that does not ride is the carrier of the wall (the shape-10 row, whose first line is X); every other row with a pair rides. A riding line's momentum lives at the mean wall W_in = (w div 2)(X_before + X_now): P_in = W_in (a_now - a_before) + r - W_in div 2; the kick P_out = P_in + X_now F with F = SUM_j R_j (m_j - a_now) - D a_now (no division); the carrier's write is sourced by every riding line alike, u_in u_out + (a (D a + SUM R (a - m))) div w with u = round(Q / (2 w X_now)), Q = 2 P + 1 (the odd rounding), in place of the form now^2 - next x before; the carrier steps by its one division; then every riding line divides once at W_out = (w div 2)(X_now + X_next), its remainder kept in [0, W_out) at that wall. The riding rows' writes come after the divisions, sourced by numbers known before them: the shape-4 row's time line 2 W of the planes after the step and its odd lines the current at the start, the plane at the gap 0 the Wronskian's change read from the kick, X_now SUM (re F_im - im F_re) over the planes with a gap, div W_out. Backward the same acts in the reverse order (the writes undone from the post state, the kick back, the carrier back, the division back at W_in): no cycle, every line one carried division."""
        carrier, potential, walled, massless = self.carrier(), self.potential(), self.walled(), self.emitter()  # gn2: the finders
        riders = [r for r in self.rows_ if r.wall is None and r is not carrier]
        gap_planes = [r for r in riders if r.shape == 2 and r.gap > 0]
        X_now = at(carrier.lines[0]); W_div_post = (self.w // 2) * (carrier.lines[0].before + carrier.lines[0].now) if direction == -1 else None
        stress = stress_parts([(at(l), r.pair[0]) for r in self.records() for l in r.lines], self.shape)
        trace, traceless = tensor_parts(stress)
        # the walled row first (its act carries its own write; the Links' count from it)
        k = where(walled); (phi_start,), _l, out[k] = self.act(rows[k], self.rule_of(walled, c, factors), None, [None], direction, [2 * cphi], *ends(k))
        K = self.centred_count(cphi, phi_start)
        self.count_max = max(int(abs(int(x))) for port in range(6) for x in (K - frames[port] * across(K, port)).reshape(-1))
        phases = self.link_phases(frames, K); odd = [at(l) for l in potential.lines[1:4]]
        self.start_phases, self.start_odd = phases, [o.copy() for o in odd]
        # backward: the riding rows' writes come off first, from the post state (the planes after the step unwritten, the start levels in the before slots)
        W_post = Z(self.shape)
        for r in gap_planes: W_post = W_post + wronskian(*rows[where(r)])
        J = [Z(self.shape) for _ in range(3)]
        for r in gap_planes:
            re_s, im_s = [Line(at(l), None, None, l.wall) for l in rows[where(r)]]
            for a_, j_a in enumerate(plane_current(re_s, im_s, frames)): J[a_] = J[a_] + j_a
        forces = {}
        for r in riders:  # every riding line's force at the start, SUM_j R_j (m_j - a) - D a
            rule = self.rule_of(r, c, factors); turn = None if r.shape != 2 else self.turn_of(r, phases, odd, frames)  # gn2 pick 1
            starts = [at(l) for l in rows[where(r)]]
            forces[where(r)] = (starts, [m - (2 * rule.wall - rule.self_coefficient) * a for a, m in zip(starts, self.arrivals(starts, rule, turn))], rule)
        emission = Z(self.shape)  # the Wronskian's change over the interval read from the kick: X_now SUM over the planes with a gap of (re F_im - im F_re)
        for r in gap_planes:
            (re_s, im_s), (f_re, f_im), _rule = forces[where(r)]
            emission = emission + X_now * (re_s * f_im - im_s * f_re)
        if direction == -1:
            self.write(rows[where(massless)][0], emission // W_div_post, -1)
            for l, n in zip(rows[where(potential)], [2 * W_post, *J]): self.write(l, n, -1)
        # the kicks: every riding line's momentum in and out, and the carrier's source
        forms = Z(self.shape); kicks = {}
        for r in riders:
            k = where(r); lines = rows[k]; starts, force, rule = forces[k]
            W_side = (self.w // 2) * (carrier.lines[0].before + carrier.lines[0].now)  # forward W_in from the pre carrier; backward W_out from the post carrier (the same expression at the other end)
            P_side = [W_side * (l.now - l.before) + l.rem - W_side // 2 for l in lines]
            P_other = [p + direction * X_now * f for p, f in zip(P_side, force)]
            d = 2 * self.w * X_now
            for a, f, p1, p2 in zip(starts, force, P_side, P_other):
                forms = forms + self.odd_round(2 * p1 + 1, d) * self.odd_round(2 * p2 + 1, d) + (-a * f) // self.w
            kicks[k] = (starts, P_other)
        # the carrier: its one division with the write sourced by the riding rows' momenta
        k = where(carrier)
        if self.hold_volume: out[k] = rows[k]
        else:
            p02 = p0 * p0
            numerators = [4 * X_now * (forms * 54 * self.den * self.gamma ** 2 - trace * p02) * p0] + [traceless[a] * p02 for a in range(3)] + [None] * (carrier.shape - 4)
            _s, _l, out[k] = self.act(rows[k], self.rule_of(carrier, c, factors), None, numerators, direction, None, *ends(k))
        Xc = out[k][0]; W_div = (self.w // 2) * (Xc.before + Xc.now)  # forward (w div 2)(X_now + X_next); backward (w div 2)(X_before + X_now)
        # every riding line divides once at the mean wall of the carrier's two levels at its end
        plane_starts = []; stepped = []; W = Z(self.shape); W_start = Z(self.shape)
        for r in riders:
            k = where(r); lines = rows[k]; starts, P = kicks[k]; new = []
            for a, p, l in zip(starts, P, lines):
                u = p + W_div // 2; v = u // W_div; rem = u - v * W_div  # the one division of the riding line at the mean wall
                new.append(Line(a + v, a, rem, W_div, l.wr, l.wwall) if direction == 1 else Line(a, a - v, rem, W_div, l.wr, l.wwall))
            if direction == -1 and kept is not None: self.restore(new, kept[k], top)
            out[k] = new
            if r.shape == 2:
                start = lines if direction == 1 else new; after = new if direction == 1 else held[k]
                plane_starts.append(list(start)); stepped.append([l.copy() for l in after])
                if r.gap > 0: W_start = W_start + wronskian(*start); W = W + wronskian(*after)
        self.stepped = stepped
        if direction == 1:  # the riding rows' writes after the divisions: the shape-4 row 2 W and the current; the plane at the gap 0 the Wronskian's change from the kick (W-S1)
            laid_line = out[where(massless)][0]; before_write = laid_line.now
            self.write(laid_line, emission // W_div, 1)
            laid = laid_line.now - before_write
            self.counts['light_laid'] += int(sum(abs(int(x)) for x in laid.reshape(-1))); self.counts['light_laid_nodes'] += int(sum(1 for x in laid.reshape(-1) if int(x) != 0))
            for l, n in zip(out[where(potential)], [2 * W, *J]): self.write(l, n, 1)
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

    def read_number(self, at, rules, unit=None):
        """The one-Link read: every line's remainder at the Node on the Node's own lattice F_i = gcd(w, D_i, R_i1..R_i6) and at each neighbour on the Link's lattice gcd(w, R_ji), the digit r div F, the base w div F + 1, sorted by value, composed modulo M = unit x 3 (the carry); the three refusals by name."""
        M = (self.unit_gap0 if unit is None else unit) * len(self.records())  # the draw composed modulo the planes' count times the TAKEN row's unit (gn2 pick 5): the quotient names the plane, over every plane alike
        nodes = self.frame_nodes(at); digits = []; origin = True; coarse = True
        half = self.w // 2
        for line, r in rules:
            at_node = lambda x, node: int(np.asarray(x)[node]) if np.ndim(x) else int(x)  # a rule's integer at a Node (a walled row's reaches are the one integer 0)
            F0 = math.gcd(at_node(line.wall, at), at_node(r.mass, at), *[at_node(x, at) for x in r.reaches])
            for k, n in enumerate(nodes):
                wl = at_node(line.wall, n)  # the line's own wall at that Node (the rule's w, or the ride's mean wall)
                F = F0 if k == 0 else math.gcd(wl, at_node(r.reaches[k - 1], n))
                rem = int(line.rem[n]); values = wl // F
                if self.control.get('digits') == 'folded': rem = min(rem, wl - rem); values = values // 2 + 1  # the Boss's mend of 10:1x for the twist's CP: every line's remainder folded to its wall, min(r, w - r), the distance to the nearer edge, conjugation-even on every line alike
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

    def momentum_of(self, line_now, line_before, at, d_now=0, d_before=0, num=1):
        """The change of the lattice momentum P_a = 2 num SUM_i (now_(i+a) before_i - now_i before_(i+a)) when a line's level now at the Node moves by d_now and its level before by d_before (co1's reading of the close): 2 num [d_now (before_(i-a) - before_(i+a)) + d_before (now_(i+a) - now_(i-a))] per axis."""
        found = []
        for a in range(3):
            up = tuple((at[k] + (1 if k == a else 0)) % self.cube for k in range(3)); down = tuple((at[k] - (1 if k == a else 0)) % self.cube for k in range(3))
            found.append(2 * num * (d_now * (int(line_before[down]) - int(line_before[up])) + d_before * (int(line_now[up]) - int(line_now[down]))))
        return found

    def take_at(self, at, walls, r_gap0, cause, rec=None):
        """One exact take at a Node of the walls booked: the light's level now moved toward its before by the least count of levels at which the Node's share falls by the walls (`take`); refused by name where the fall cannot reach the walls (the stop). Returns (levels, fall, the light's now before the take) or None."""
        z = (self.row(2, gap=0) if rec is None else self.records()[rec]).lines[0]  # gn2 pick 3: the taken row's first line (the gap-0 row where none is named: the bodies' closing)
        levels, fall = self.take(at, walls, r_gap0, z)
        if levels is None:
            self.counts['refused_stop'] += cause; self.log.append({'event': 'refused', 'i': self.interval, 'node': list(at), 'cause': 'stop', 'fall': fall, 'walls': walls}); return None
        now = int(z.now[at]); before = int(z.before[at]); toward = 1 if before > now else -1
        z.now[at] = now + toward * levels; self.closes[at] += 1
        self.last_dp = self.momentum_of(z.now, z.before, at, d_now=toward * levels, num=(self.row(2, gap=0) if rec is None else self.records()[rec]).pair[0])  # the take's momentum, booked on the click's line (N-S3's reading); gn2: the taken row's num
        return levels, fall, now

    def meet(self, gap0_start, sh, rules, frozen, rec=None, unit=None):
        """The Link close (Q1/Q2, the owner's sentence 1): every Link once from its +a end; a meeting where both ends hold a whole quantum of light at the vacuum's weight and neither end is frozen; the + child at the end the light's own current F_ij = num (now_i before_j - before_i now_j) flows into, read at the interval's start (F = 0 refused by name: no orientation); the Link's one number read at that end gives the lift. Returns the births as (the take's Node, the lift, the - child's Node, the + child's Node)."""
        born = []; unit = self.unit_gap0 if unit is None else unit  # gn2 pick 3: the taken row's unit
        taken = gap0_start[0]  # the row the click takes: the row whose quanta meet (David's: the massless plane's first line); its current orients the Link, its twist gives the handedness
        currents = [self.den * self.link_current(taken, 2 * axis) for axis in range(3)]
        twists = [self.twist(taken, axis) for axis in range(3)]
        for at in np.ndindex(*self.shape):
            if frozen[at]: continue
            for axis in range(3):
                j = tuple((at[a] + (1 if a == axis else 0)) % self.cube for a in range(3))
                if frozen[j] or int(sh[at]) < unit or int(sh[j]) < unit: continue
                if rec is not None and self.records()[rec].gap != 0:  # gn2 pick 3: two whole quanta of a gapped row meeting: the children by the exact list of its pair (none built here): refused by name `list`, counted, the first 20 logged
                    self.counts['met_gapped'] += 1
                    if self.counts['met_gapped'] <= 20: self.log.append({'event': 'refused', 'i': self.interval, 'node': list(at), 'cause': 'list', 'link': list(j), 'row': rec, 'share': [int(sh[at]), int(sh[j])], 'unit': unit})
                    continue
                F = int(currents[axis][at])
                if F == 0:
                    self.counts['refused_orientation'] += 1; self.log.append({'event': 'refused', 'i': self.interval, 'node': list(at), 'cause': 'orientation', 'link': list(j)}); continue
                into, outof = (j, at) if F > 0 else (at, j)  # the end the current flows into: the draw and the take stay there
                h = int(twists[axis][at])
                if h == 0:
                    self.counts['refused_twist'] += 1; self.log.append({'event': 'refused', 'i': self.interval, 'node': list(at), 'cause': 'twist', 'link': list(j)}); continue
                plus, minus = (into, outof) if h > 0 else (outof, into)  # the + child at the end the current flows into where the twist is right-handed, at the other end where left-handed (the owner's sentence 4, PA2's form)
                drawn = self.read_number(into, rules, unit)
                if drawn is None: continue
                number, room = drawn
                born.append((into, (number // unit) % len(self.records()), minus, plus, room, rec))  # the plane drawn, over every plane alike (the massless plane among them); the take at the current's end; gn2: the taken row carried
        return born

    def refuse(self, born, owns):
        """The lay refused by name (ALGEBRA.md, The click writes on the lattice, line 186: the lay's Wronskian is exact only at an empty Node): where any of the child's family already stands at its Node, and where two children of one record would land at one Node in one close (the charge made at a crowded lay, W = n^2 A^2; a rule that reaches two Links, named open under the locality law). Returns the births kept."""
        kept = []
        for at, s_, minus, plus, room, rec in born:
            if int(owns[s_][minus]) > 0 or int(owns[s_][plus]) > 0:
                self.counts['refused_lay'] += 1; self.log.append({'event': 'refused', 'i': self.interval, 'node': list(at), 'cause': 'lay', 'standing': int(owns[s_][minus]), 'unit': self.units[s_]}); continue
            kept.append((at, s_, minus, plus, room, rec))
        landing = {}
        for at, s_, minus, plus, room, rec in kept:
            landing[(s_, minus)] = landing.get((s_, minus), 0) + 1; landing[(s_, plus)] = landing.get((s_, plus), 0) + 1
        crowded = [k for k in kept if landing[(k[1], k[2])] > 1 or landing[(k[1], k[3])] > 1]
        for at, s_, minus, plus, room, rec in crowded:
            self.counts['refused_lay'] += 1; self.log.append({'event': 'refused', 'i': self.interval, 'node': list(at), 'cause': 'lay', 'children_at_one_node': max(landing[(s_, minus)], landing[(s_, plus)])})
        return [k for k in kept if k not in crowded]

    def births(self, kept, r_gap0, c, factors, pace):
        """The births kept, every face read before any write: one exact take per Node of its children's walls summed, the start's light paying; then each child laid as one quantum of its record at the quarter turn (re_now A at the - end, im_before -A; re_now A at the + end, im_before +A), the birth logged with its numbers. Returns every Node a taken birth touched."""
        by_node = {}
        for at, s_, minus, plus, room, rec in kept: by_node.setdefault((at, rec), []).append((s_, minus, plus, room))
        taken = []
        for at, rec in sorted(by_node, key=lambda k_: (k_[0], -1 if k_[1] is None else k_[1])):
            children = by_node[(at, rec)]; walls = sum(2 * self.units[s_] for s_, _m, _p, _r in children)
            got = self.take_at(at, walls, r_gap0 if rec is None else self.rules_at[rec], len(children), rec)  # gn2 pick 3: the take from the taken row at its rule
            if got is not None: taken.append((at, children, walls, got, rec))
        for at, children, walls, (levels, fall, now), rec in taken:
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
                self.log.append({'event': 'birth', 'i': self.interval, 'node': list(at), 'line_pair': s_, 'senses': [-1, 1], 'W_children': W_children, 'minus': list(minus), 'plus': list(plus), 'taken': fall, 'booked': walls, 'levels': levels, 'light_now_was': now, 'proper': int(self.proper[at]), 'content': int(c[at]), 'amplitude': A, 'children_at_node': len(children), 'room': room, 'dP_take': dp_take, 'dP_lay': dp_lay, **({'taken_row': rec} if rec is not None and self.records()[rec].gap != 0 else {})})
            self.counts['taken'] += fall; self.counts['booked'] += walls
        return {at for at, _c, _w, _g, _rec in taken} | {m for _a, ch, _w, _g, _rec in taken for _s, m, _p, _r in ch} | {p_ for _a, ch, _w, _g, _rec in taken for _s, _m, p_, _r in ch}

    def bodies(self, gap0_start, plane_starts, owns, born_nodes, frozen, r_gap0):
        """The bodies' closing: a record standing at a whole quantum of its own unit through one period of its re line's upward crossings clicks (one take of its unit at the Node, the credit logged), a Node of a birth this interval or a frozen Node apart."""
        for rec in range(len(self.records())):
            s_ = rec
            standing_now = np.vectorize(lambda v: 1 if int(v) >= self.units[s_] else 0, otypes=[object])(owns[rec])
            self.standing[rec] = np.where(standing_now == 1, self.standing[rec] + 1, 0)
            re = self.records()[rec].lines[0]
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
            rules = [(r.lines[0], self.rule_of(r, c, factors)) for r in (self.potential(), self.carrier())]
            for rec, r in enumerate(self.records()):
                rules += [(l, self.rule_of(r, c, factors)) for l in plane_starts[rec]]
        else:  # A2, the default (the owner's word of 2026-10-25, "go with A if it is generic and solves"; the Boss's ruling of 10:1x): the one-Link read takes every line of every row at the interval's start, alike
            rules = [(l, self.rule_of(r, c, factors)) for r, lines in zip(self.rows_, held) for l in lines]
        pace = paces.link_pace_of(self.gamma, c)
        owns = []; self.rules_at = []  # every plane's standing share at the interval's start at the vacuum's weight (V-D, the owner's sentence 7): the meeting's threshold on the massless plane, the lay's refusal on the lift's; gn2: every record's rule kept for the take
        for rec, r in enumerate(self.records()):
            rr = self.rule_of(r, c, factors); re0, im0 = plane_starts[rec]; self.rules_at.append(rr)
            owns.append(self.share(re0, rr, pace, vacuum=True) + self.share(im0, rr, pace, vacuum=True))
        sh = owns[self.records().index(massless)]
        frozen = np.asarray(pace, dtype=object) == 0 if np.ndim(pace) else np.zeros(self.shape, dtype=bool)
        if GN2['CLICK'] == 'off': born = self.meet(gap0_start, sh, rules, frozen)
        else:  # gn2 pick 3 (CLICK=generic): the meeting over every row alike, each at its own unit; the taken row is the row whose quanta meet
            born = []
            for rec_, _r in enumerate(self.records()): born += self.meet(plane_starts[rec_], owns[rec_], rules, frozen, rec_, self.units[rec_])
        born_nodes = self.births(self.refuse(born, owns), r_gap0, c, factors, pace)
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

    def credit(self, rec, at, plane_starts, fall, levels, light_was):
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
                'beat': int(self.beats[rec][at]), 'frame': frame, 'taken': fall, 'levels': levels, 'light_now_was': light_was, 'dP_take': self.last_dp, 'sign_level': int(self.potential().lines[0].now[at]), 'turned': bool(self.turned[at])}


    def unclick(self, frame):
        """The close undone from the log, in the reverse order of its lines: the lays removed, the light restored, the readings' counters restored."""
        z = self.row(2, gap=0).lines[0]
        for entry in reversed(self.log[frame['log_from']:]):
            at = tuple(entry['node'])
            if entry['event'] == 'birth':
                s_ = entry['line_pair']; A = entry['amplitude']
                self.lay(s_, tuple(entry['minus']), (A, 0, 0, -A), -1); self.lay(s_, tuple(entry['plus']), (A, 0, 0, A), -1)
                zz = z if 'taken_row' not in entry else self.records()[entry['taken_row']].lines[0]  # gn2 pick 3
                zz.now[at] = entry['light_now_was']; self.closes[at] -= 1
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
    metric, potential, massless, planes = b.carrier(), b.potential(), b.emitter().lines[0], [r.lines for r in b.records()]
    c = b.content(); cs = [int(x) for x in c.reshape(-1)]; vs = [int(x) for x in metric.lines[0].now.reshape(-1)]
    energy = sum(int(x) * int(x) for rec in planes for l in rec for x in l.now.reshape(-1)); odd_max = max(abs(int(x)) for l in potential.lines[1:4] for x in l.now.reshape(-1))
    light_v = max(abs(int(a) - int(bb)) for a, bb in zip(massless.now.reshape(-1), massless.before.reshape(-1)))
    packets = {}
    for rec, (re, im) in enumerate(planes):
        if b.records()[rec].gap == 0: continue  # the reader skips the massless plane (the sea fills the board)
        wgt = re.now * re.now + im.now * im.now; total = int(sum(int(x) for x in wgt.reshape(-1)))
        if total == 0: continue
        idx = np.indices(b.shape); cen = [int(sum(int(w) * int(x) for w, x in zip(wgt.reshape(-1), idx[a].reshape(-1)))) * 1000 // total for a in range(3)]
        if True:
            packets['plane %d' % rec] = {'centroid (thousandths of a Link)': cen, 'nodes with levels': int(sum(1 for x in wgt.reshape(-1) if int(x) > 0)), 'energy bits': total.bit_length()}
    W = Z(b.shape)
    for re, im in planes: W = W + wronskian(re, im)
    n, _bits = b.census(); tens = [int(x) for l in metric.lines[1:4] for x in l.now.reshape(-1)]
    return {'i': b.interval, 'packets (reader)': packets, 'content min/mean/max': [min(cs), sum(cs) // len(cs), max(cs)], 'volume mean': sum(vs) // len(vs), 'births': b.counts['births'], 'body_clicks': b.counts['body_clicks'],
            'refused': b.counts['refused_stop'] + b.counts['refused_origin'] + b.counts['refused_lay'] + b.counts['refused_orientation'] + b.counts['refused_twist'], 'refused_lay': b.counts['refused_lay'], 'refused_orientation': b.counts['refused_orientation'], 'turns': b.counts['turns'],
            'integers': n, 'max bits': maxbits, 'max transient bits': b.max_transient, 'sign level max': max(abs(int(x)) for x in potential.lines[0].now.reshape(-1)), 'planes energy bits': energy.bit_length(),
            'links at the wall': int(sum(1 for f in b.link_factors()[0::2] for x in f.reshape(-1) if int(x) == 0)), 'tension min/max': [min(tens), max(tens)], 'odd max bits': odd_max.bit_length(), 'link count max': b.count_max, 'orbit table': len(b.orbit),
            'massless W abs max': int(max(abs(int(x)) for x in wronskian(*b.row(2, gap=0).lines).reshape(-1))), 'W total': int(sum(int(x) for x in W.reshape(-1))), 'W abs sum': int(sum(abs(int(x)) for re, im in planes for x in wronskian(re, im).reshape(-1))), 'light velocity max': light_v}


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
