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
        rows = [(int(r['shape']), (int(r['pair'][0]), int(r['pair'][1]))) for r in universe['rows']]
        light_rows = [pair for shape_, pair in rows if shape_ == 1]
        if len(light_rows) != 1 or light_rows[0] != (den, den): raise ValueError('the universe names one massless shape-1 row at (den, den), the light')
        self.pairs = [pair for shape_, pair in rows if shape_ == 2]
        self.nl = len(self.pairs)
        if self.nl == 0: raise ValueError('the universe names no plane row')
        self.lifts = [(None, num, sine_den(num, den)) for num, _den in self.pairs]  # the legs from the pairs: T sin omega as the universe's circle gives it
        self.w = wall_of(den, gamma, unit)
        # every remainder starts at half its wall (the engine rounds half up: a remainder at the half wall carries the same); the write walls: the volume's time line 54 den Gamma^4 T, its axis lines 54 den T Gamma^2, the sign's four and the massless row's lay T
        mk = lambda wwall=None: Line(Z(S), Z(S), Z(S) + self.w // 2, self.w, None if wwall is None else Z(S) + wwall // 2, wwall)
        self.vol = mk(54 * den * gamma ** 4 * action); self.vol_axes = [mk(54 * den * action * gamma ** 2) for _ in range(3)]
        self.vol_more = [mk(54 * den * action * gamma ** 2) for _ in range(6)]  # the metric's six other lines (the three flux g_0a, the three shears g_ab): standing at zero, rotated with the row, written by nothing and read by nothing until the derivation of their write and read lands (the owner's question of 2026-10-25, the 10, 4, 2 in the code); then one input more of act and link, no new function
        self.light = mk(action)
        self.sign = mk(action); self.sign_axes = [mk(action) for _ in range(3)]
        self.phi = Line(Z(S), Z(S), Z(S) + 1, 2)  # the phase potential row: the wall 2, the write 2 c_phi inside its division
        self.rule_phi = rule3.Rule(tuple(0 for _ in AXES), 4, 2, 0)  # the phase row's rule: no Links, the wall 2, the own weight 2 w (phi_next = 2 phi_now - phi_before + the write)
        self.planes = [[mk(), mk()] for _ in range(2 * self.nl)]  # record 2s + (0: sense -1, 1: sense +1): [re, im]
        self.standing = [Z(S) for _ in range(2 * self.nl)]; self.crossed = [Z(S) for _ in range(2 * self.nl)]; self.beats = [Z(S) for _ in range(2 * self.nl)]
        self.proper = Z(S); self.closes = Z(S)
        self.interval = 0; self.log = []; self.turns = []; self.stack = []
        self.vol.now[:] = gamma; self.vol.before[:] = gamma
        self.unit_light = 3 * den * action  # W_c
        self.units = [3 * action * s for _v, _n, s in self.lifts]  # one quantum of a record, 3 T s
        self.detectors = []  # the Nodes whose light the record credits (the world names them; a reading, no state)
        # the seed as the world lays it: a list of lays in the three forms of the law and no fourth (the owner's word of 2026-10-25, "2, 3, 4 approved"; the Z hands' form): `sea` lays the massless row's drift v, the largest integer with v^2 <= T, at every Node; `hole` takes it back at one Node; `at` lays a packet: on the massless row N drifts at the centre, on a plane row the conjugate pair, N quanta each record, over the raised cosine's envelope of the half-width 2 or 3 (exact in integers there and at no other width below 6). Refused by name: a fourth form, a row no pair of the universe carries, a sea of a plane row, a Node off the board, a plane packet of another width (a body is laid over its packet, never one Node)
        self.drift = rule3.largest_below(action)
        packets = []
        for lay in world.get('seed', []):
            form = lay.get('lay'); row = tuple(int(x) for x in lay['row']) if 'row' in lay else None
            if form == 'sea':
                if row != (den, den): raise ValueError('a sea is the massless row\'s alone: the drift is its double root')
                self.light.now[:] = self.light.now + self.drift
            elif form == 'hole':
                at = self.node_of(lay['at']); self.light.now[at] = self.light.now[at] - self.drift
            elif form == 'at':
                n = int(lay['quanta']); at = self.node_of(lay['centre'])
                if row == (den, den): self.light.now[at] = self.light.now[at] + n * self.drift
                elif row in self.pairs: packets.append((self.pairs.index(row), at, int(lay.get('width', 0)), n))
                else: raise ValueError('the world lays a row the universe has not')
            else: raise ValueError('a lay of no form of the law: %r' % (form,))
        # the toy's controls and readings, no lay of the law (named open for the owner's word): `control.well` a hand-held well of the volume (the content laid as a parabola within the radius, held fixed where the file says so), `detectors` the Nodes whose light credits the record reads
        self.hold_volume = False
        well = world.get('control', {}).get('well')
        if well:
            at = self.node_of(well['at']); levels, R = int(well['levels']), int(well['radius']); self.hold_volume = bool(well.get('held', False))
            for node in np.ndindex(*self.shape):
                r2 = sum(min(abs(node[a] - at[a]), self.cube - abs(node[a] - at[a])) ** 2 for a in range(3))
                if r2 < R * R:
                    c = levels * (R * R - r2) // (R * R)
                    self.vol.now[node] = int(np.asarray(volform.volume_of(gamma, np.array([c], dtype=object)), dtype=object).reshape(-1)[0]); self.vol.before[node] = self.vol.now[node]
        self.detectors = [self.node_of(d) for d in world.get('detectors', [])]
        self.A = rule3.largest_below(action // 2)  # the lay's amplitude where the rule's form has no positive term (a lone record's share cannot be read there)
        self.vol_pair = (den - den // gamma, den)
        self.X = phase.amplitude(phase.unit(gamma), WIDTH // 2 - 1)  # the phase pair's amplitude from half the law's width less one, so that a pair's product with a level stays within the width
        seed_pair = phase.seed(self.X, gamma)
        self.orbit_lines = [seed_pair]  # the last pair as lines, for the next act
        self.orbit = [(int(seed_pair[0][0]), int(seed_pair[1][0]))]  # the table of (cos, sin) as plain integers
        self.counts = {'births': 0, 'taken': 0, 'booked': 0, 'body_clicks': 0, 'refused_stop': 0, 'refused_origin': 0, 'refused_lay': 0, 'refused_orientation': 0, 'turns': 0, 'light_credits': 0, 'light_laid': 0, 'light_laid_nodes': 0}
        self.max_transient = 0
        for s_, at, h, n in packets: self.lay_packet(s_, at, h, n)

    def node_of(self, xyz):
        """A Node named by the world file: three integers on the board; a Node off the board is refused by name."""
        at = tuple(int(x) for x in xyz)
        if len(at) != 3 or any(not 0 <= x < self.cube for x in at): raise ValueError('a Node off the board: %r' % (at,))
        return at

    def lay_packet(self, s_, at, h, n):
        """The `at` lay of a plane row: the conjugate pair (the two records at the senses -1 and 1) laid at rest over the raised cosine's envelope of the half-width h (the weights 2, 1 at h = 2; 4, 3, 1 at h = 3; the product over the three axes), each record at the largest amplitude A at which its share at the vacuum's weight, summed over the packet, is at most n quanta of its unit (a search by comparisons); each Node's lines at the band's rest rotation: re_now = A w_i div w_0, re_before = re_now num div den, im_now = 0, im_before = sense re_now s div den with s the pair's sine (Z1's form)."""
        weights = {2: (2, 1), 3: (4, 3, 1)}.get(h)
        if weights is None: raise ValueError('a plane packet has the half-width 2 or 3: a body is laid over its packet')
        num = self.pairs[s_][0]; sn = self.lifts[s_][2]; w0 = weights[0] ** 3
        envelope = Z(self.shape)
        for j in np.ndindex(*(2 * h - 1,) * 3):
            off = [x - (h - 1) for x in j]
            envelope[tuple((at[a] + off[a]) % self.cube for a in range(3))] += weights[abs(off[0])] * weights[abs(off[1])] * weights[abs(off[2])]
        c = self.content(); factors = self.link_factors(); r = self.rule(self.pairs[s_], c, factors); self.start_content = c
        def record(A, sense):
            re_now = (A * envelope) // w0
            return Line(re_now, (re_now * num) // self.den, None, self.w), Line(Z(self.shape), sense * ((re_now * sn) // self.den), None, self.w)
        def share_of(A):
            re, im = record(A, 1)
            return int(sum(int(x) for x in (self.share(re, r, vacuum=True) + self.share(im, r, vacuum=True)).reshape(-1)))
        target = n * self.units[s_]
        high = 1
        while share_of(high) <= target: high = high + high
        low = 0
        while high - low > 1:
            middle = (low + high) // 2
            if share_of(middle) <= target: low = middle
            else: high = middle
        for sense in (-1, 1):
            re, im = record(low, sense); self.lay(2 * s_ + (1 if sense > 0 else 0), Ellipsis, (re.now, re.before, im.now, im.before))
        self.log.append({'event': 'lay', 'i': 0, 'node': list(at), 'line_pair': s_, 'width': h, 'quanta': n, 'amplitude': low, 'share': share_of(low), 'unit': self.units[s_], 'nodes': int(sum(1 for x in envelope.reshape(-1) if int(x) > 0))})

    # ---- the readings at the interval's start
    def content(self): return np.asarray(volform.level_of(self.gamma, self.vol.now), dtype=object)
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
        axis_levels = [l.now for l in self.vol_axes] if axis_levels is None else axis_levels
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
        """The Node's rows in the order their writes depend on each other: the phase row (its count read by every plane), the planes (no write), the massless row (W-S1 from the planes' Wronskian), the sign's row (its time line from the Wronskian, its odd lines from the planes' current), the volume's row (its time line from every form, its axis lines from the stress)."""
        return [[self.phi], *self.planes, [self.light], [self.sign, *self.sign_axes], [self.vol, *self.vol_axes, *self.vol_more]]

    def set_rows(self, rows):
        n = 2 * self.nl
        (self.phi,) = rows[0]; self.planes = [list(r) for r in rows[1:1 + n]]; (self.light,) = rows[1 + n]; self.sign, *self.sign_axes = rows[2 + n]; self.vol, *self.vol_axes = rows[3 + n][:4]; self.vol_more = list(rows[3 + n][4:])

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
            line.now, line.before, line.rem = np.where(top, sgn * h.before, line.now), np.where(top, sgn * h.now, line.before), np.where(top, h.rem if im else line.wall - 1 - h.rem, line.rem)
            if line.wr is not None: line.wr = np.where(top, line.wwall - 1 - h.wr, line.wr)

    def swap(self, held):
        """The swap at the top (ALGEBRA.md, the fifth act): the weak maximum X0 <= X1 >= X2 with one strict (the held before, the held now, the now after the writes), or the floor (X0 or X2 below X_f); the turned Node ends the interval at the state it started from, exchanged and complemented, the step's output discarded there."""
        x0, x1, x2 = held[-1][0].before, held[-1][0].now, self.vol.now
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
        # the readings at the start
        c = np.asarray(volform.level_of(self.gamma, at(self.vol)), dtype=object); self.start_content = c
        p0 = paces.clock_of(self.gamma, c); self.proper = self.proper + direction * p0
        factors = self.link_factors([at(l) for l in self.vol_axes]); self.start_factors = factors
        frames = self.frames(self.phi.rem); self.start_frames = frames
        cphi = paces.rounded(at(self.sign) * p0, self.gamma)  # the clocked potential at the sign's start level
        rows = self.rows(); n = 2 * self.nl; out = [None] * len(rows); ends = lambda k: (top, None if kept is None else kept[k])
        # the phase row: its write 2 c_phi inside its division at the wall 2 (the row 2 phi_now - phi_before + c_phi); the Links' count from the row at the start
        (phi_start,), _l, out[0] = self.act(rows[0], self.rule_phi, None, [None], direction, [2 * cphi], *ends(0))
        K = self.centred_count(cphi, phi_start)
        self.count_max = max(int(abs(int(x))) for port in range(6) for x in (K - frames[port] * across(K, port)).reshape(-1))  # the Links' count's size this interval (a reading)
        phases = self.link_phases(frames, K); odd = [at(l) for l in self.sign_axes]
        self.start_phases, self.start_odd = phases, [o.copy() for o in odd]
        stress = stress_parts([(at(self.light), self.den)] + [(at(l), self.pairs[k // 2][0]) for k in range(n) for l in self.planes[k]], self.shape)
        trace, traceless = tensor_parts(stress)
        # the planes: no write; their forms, Wronskians and currents feed the other rows' writes
        forms = Z(self.shape); W_start = Z(self.shape); W = Z(self.shape); J = [Z(self.shape) for _ in range(3)]; plane_starts = []; stepped = []
        for k in range(n):
            r = self.rule(self.pairs[k // 2], c, factors)
            start, levels, out[1 + k] = self.act(rows[1 + k], r, (phases, odd, frames), [None, None], direction, None, *ends(1 + k))
            re, im = start
            forms = forms + (re.now * re.now - levels[0] * re.before) + (im.now * im.now - levels[1] * im.before)
            W_start = W_start + wronskian(re, im)
            after = out[1 + k] if direction == 1 else held[1 + k]  # the planes as the step left them
            W = W + wronskian(*after); stepped.append([l.copy() for l in after])
            for a, j_a in enumerate(plane_current(re, im, frames)): J[a] = J[a] + j_a
            plane_starts.append(start)
        self.stepped = stepped  # kept for the credits' frame (the swap discards it at a turned Node)
        # the massless row: W-S1 (the owner's sentence 3): the change of the planes' Wronskian over the interval, summed over every plane, laid on the time line at the wall T; a steady rotation lays nothing
        r_l = self.rule((self.den, self.den), c, factors)
        (light_start,), levels, out[1 + n] = self.act(rows[1 + n], r_l, None, [W - W_start], direction, None, *ends(1 + n))
        forms = forms + (light_start.now * light_start.now - levels[0] * light_start.before)
        if direction == 1:  # the emission's size, a reading of the run: the levels laid on the massless line and the Nodes they were laid at
            laid = out[1 + n][0].now - levels[0]
            self.counts['light_laid'] += int(sum(abs(int(x)) for x in laid.reshape(-1))); self.counts['light_laid_nodes'] += int(sum(1 for x in laid.reshape(-1) if int(x) != 0))
        # the sign's row: its time line written 2 W, its odd lines the planes' current, at the wall T
        _s, _l, out[2 + n] = self.act(rows[2 + n], r_l, None, [2 * W, *J], direction, None, *ends(2 + n))
        # the volume's row: its time line written (d + 1) X c over Gamma E_s T less the pressure (the stress's trace at the pace squared, engine records.pressure_term), its axis lines the traceless stress at the write's factor (p0 / Gamma)^2 (engine held_write_of)
        if self.hold_volume: out[3 + n] = rows[3 + n]  # the control: the volume held by hand, no act on it in either direction
        else:
            X = at(self.vol); p02 = p0 * p0
            numerators = [4 * X * (forms * 54 * self.den * self.gamma ** 2 - trace * p02) * p0] + [traceless[a] * p02 for a in range(3)] + [None] * len(self.vol_more)
            _s, _l, out[3 + n] = self.act(rows[3 + n], self.rule(self.vol_pair, c, factors), None, numerators, direction, None, *ends(3 + n))
        self.set_rows(out)
        if direction == -1: self.interval -= 1; return
        counters = ([a.copy() for a in self.standing], [a.copy() for a in self.crossed], [a.copy() for a in self.beats])
        top = self.swap(held)
        log_from = len(self.log)
        self.click({'light': light_start, 'planes': plane_starts})
        self.stack.append({'turned': top, 'counters': counters, 'log_from': log_from})

    def step(self): return self.run(1)
    def step_back(self): return self.run(-1)

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
        digits.sort(); carry = 0; room = 1
        for d, b in digits: carry = (carry * b + d) % M; room = min(room * b, M)
        return carry, room  # the number drawn and the draw's room: the count of numbers the read could give (the digits' bases' product, at most M), the click's entropy its bit length

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

    def lay(self, rec, where, levels, sign=1):
        """The one lay act: a record's four levels (re_now, re_before, im_now, im_before) added at the Node `where` (or over the board where `where` is the whole), taken back with sign -1 (the inverse of the lay is the same act)."""
        re, im = self.planes[rec]
        for line, now, before in ((re, levels[0], levels[1]), (im, levels[2], levels[3])):
            line.now[where] = line.now[where] + sign * now; line.before[where] = line.before[where] + sign * before

    def take_at(self, at, walls, r_light, cause):
        """One exact take at a Node of the walls booked: the light's level now moved toward its before by the least count of levels at which the Node's share falls by the walls (`take`); refused by name where the fall cannot reach the walls (the stop). Returns (levels, fall, the light's now before the take) or None."""
        levels, fall = self.take(at, walls, r_light, self.light)
        if levels is None:
            self.counts['refused_stop'] += cause; self.log.append({'event': 'refused', 'i': self.interval, 'node': list(at), 'cause': 'stop', 'fall': fall, 'walls': walls}); return None
        now = int(self.light.now[at]); before = int(self.light.before[at]); toward = 1 if before > now else -1
        self.light.now[at] = now + toward * levels; self.closes[at] += 1
        return levels, fall, now

    def meet(self, start, sh, rules, frozen):
        """The Link close (Q1/Q2, the owner's sentence 1): every Link once from its +a end; a meeting where both ends hold a whole quantum of light at the vacuum's weight and neither end is frozen; the + child at the end the light's own current F_ij = num (now_i before_j - before_i now_j) flows into, read at the interval's start (F = 0 refused by name: no orientation); the Link's one number read at that end gives the lift. Returns the births as (the take's Node, the lift, the - child's Node, the + child's Node)."""
        born = []
        currents = [self.den * self.link_current(start['light'], 2 * axis) for axis in range(3)]
        for at in np.ndindex(*self.shape):
            if frozen[at]: continue
            for axis in range(3):
                j = tuple((at[a] + (1 if a == axis else 0)) % self.cube for a in range(3))
                if frozen[j] or int(sh[at]) < self.unit_light or int(sh[j]) < self.unit_light: continue
                F = int(currents[axis][at])
                if F == 0:
                    self.counts['refused_orientation'] += 1; self.log.append({'event': 'refused', 'i': self.interval, 'node': list(at), 'cause': 'orientation', 'link': list(j)}); continue
                plus, minus = (j, at) if F > 0 else (at, j)
                drawn = self.read_number(plus, rules)
                if drawn is None: continue
                number, room = drawn
                born.append((plus, (number // self.unit_light) % self.nl, minus, plus, room))
        return born

    def refuse(self, born, owns):
        """The lay refused by name (ALGEBRA.md, The click writes on the lattice, line 186: the lay's Wronskian is exact only at an empty Node): where any of the child's family already stands at its Node, and where two children of one record would land at one Node in one close (the charge made at a crowded lay, W = n^2 A^2; a rule that reaches two Links, named open under the locality law). Returns the births kept."""
        kept = []
        for at, s_, minus, plus, room in born:
            if int(owns[2 * s_][minus]) > 0 or int(owns[2 * s_ + 1][plus]) > 0:
                self.counts['refused_lay'] += 1; self.log.append({'event': 'refused', 'i': self.interval, 'node': list(at), 'cause': 'lay', 'standing': int(owns[2 * s_][minus]), 'unit': self.units[s_]}); continue
            kept.append((at, s_, minus, plus, room))
        landing = {}
        for at, s_, minus, plus, room in kept:
            landing[(2 * s_, minus)] = landing.get((2 * s_, minus), 0) + 1; landing[(2 * s_ + 1, plus)] = landing.get((2 * s_ + 1, plus), 0) + 1
        crowded = [k for k in kept if landing[(2 * k[1], k[2])] > 1 or landing[(2 * k[1] + 1, k[3])] > 1]
        for at, s_, minus, plus, room in crowded:
            self.counts['refused_lay'] += 1; self.log.append({'event': 'refused', 'i': self.interval, 'node': list(at), 'cause': 'lay', 'children_at_one_node': max(landing[(2 * s_, minus)], landing[(2 * s_ + 1, plus)])})
        return [k for k in kept if k not in crowded]

    def births(self, kept, r_light, c, factors, pace):
        """The births kept, every face read before any write: one exact take per Node of its children's walls summed, the start's light paying; then each child laid as one quantum of its record at the quarter turn (re_now A at the - end, im_before -A; re_now A at the + end, im_before +A), the birth logged with its numbers. Returns every Node a taken birth touched."""
        by_node = {}
        for at, s_, minus, plus, room in kept: by_node.setdefault(at, []).append((s_, minus, plus, room))
        taken = []
        for at in sorted(by_node):
            children = by_node[at]; walls = sum(2 * self.units[s_] for s_, _m, _p, _r in children)
            got = self.take_at(at, walls, r_light, len(children))
            if got is not None: taken.append((at, children, walls, got))
        for at, children, walls, (levels, fall, now) in taken:
            self.closes[at] -= 1  # the take counted once per child below
            for s_, minus, plus, room in children:
                A = self.lay_amplitude(s_, at, c, factors, pace)
                self.lay(2 * s_, minus, (A, 0, 0, -A)); self.lay(2 * s_ + 1, plus, (A, 0, 0, A))
                self.counts['births'] += 1; self.closes[at] += 1
                self.log.append({'event': 'birth', 'i': self.interval, 'node': list(at), 'line_pair': s_, 'senses': [-1, 1], 'minus': list(minus), 'plus': list(plus), 'taken': fall, 'booked': walls, 'levels': levels, 'light_now_was': now, 'proper': int(self.proper[at]), 'content': int(c[at]), 'amplitude': A, 'children_at_node': len(children), 'room': room})
            self.counts['taken'] += fall; self.counts['booked'] += walls
        return {at for at, _c, _w, _g in taken} | {m for _a, ch, _w, _g in taken for _s, m, _p, _r in ch} | {p_ for _a, ch, _w, _g in taken for _s, _m, p_, _r in ch}

    def bodies(self, start, owns, born_nodes, frozen, r_light):
        """The bodies' closing: a record standing at a whole quantum of its own unit through one period of its re line's upward crossings clicks (one take of its unit at the Node, the credit logged), a Node of a birth this interval or a frozen Node apart."""
        for rec in range(2 * self.nl):
            s_ = rec // 2
            standing_now = np.vectorize(lambda v: 1 if int(v) >= self.units[s_] else 0, otypes=[object])(owns[rec])
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
                got = self.take_at(at, self.units[s_], r_light, 1)
                self.standing[rec][at] = 0
                if got is None: continue
                levels, fall, now = got
                self.counts['body_clicks'] += 1
                self.log.append(self.credit(rec, at, start, fall, levels, now))

    def detect(self, start, r_light, pace, c):
        """The detectors, a reading and no act: the light's whole quanta at the Node risen over the interval (the start's share against the share as the click leaves the light), each quantum a light credit with the Node's proper count."""
        if not self.detectors: return
        sh_end = self.share(self.light, r_light, pace, vacuum=True); sh_vac = self.share(start['light'], r_light, pace, vacuum=True)
        for det in self.detectors:
            rise = int(sh_end[det]) // self.unit_light - int(sh_vac[det]) // self.unit_light
            if rise > 0:
                self.counts['light_credits'] += rise
                self.log.append({'event': 'light', 'i': self.interval, 'node': list(det), 'quanta': rise, 'proper': int(self.proper[det]), 'content': int(c[det]), 'light_now': int(self.light.now[det]), 'light_before': int(self.light.before[det])})

    def click(self, start):
        """The click (ALGEBRA.md, The click writes on the lattice), the Node's fourth act: the readings at the start (the rules of every row, the light's share and each record's standing share at the vacuum's weight, the frozen Nodes), the Link close (`meet`), the lays refused by name (`refuse`), the births taken and laid (`births`), the bodies' closing (`bodies`), the detectors' credits (`detect`); `start` holds the massless row's and the planes' lines at the interval's start."""
        c = self.start_content; factors = self.link_factors()
        r_light = self.rule((self.den, self.den), c, factors)
        rules = [(start['light'], r_light), (self.sign, r_light), (self.vol, self.rule(self.vol_pair, c, factors))]
        for s_, pair in enumerate(self.pairs):
            r = self.rule(pair, c, factors)
            for sense in (0, 1):
                rules += [(start['planes'][2 * s_ + sense][0], r), (start['planes'][2 * s_ + sense][1], r)]
        pace = paces.link_pace_of(self.gamma, c)
        sh = self.share(start['light'], r_light, pace, vacuum=True)  # V-D, the owner's sentence 7: the birth's threshold and the lay's refusal read the share at the vacuum's weight
        owns = []
        for rec in range(2 * self.nl):
            r = self.rule(self.pairs[rec // 2], c, factors); re0, im0 = start['planes'][rec]
            owns.append(self.share(re0, r, pace, vacuum=True) + self.share(im0, r, pace, vacuum=True))
        frozen = np.asarray(pace, dtype=object) == 0 if np.ndim(pace) else np.zeros(self.shape, dtype=bool)
        born_nodes = self.births(self.refuse(self.meet(start, sh, rules, frozen), owns), r_light, c, factors, pace)
        self.bodies(start, owns, born_nodes, frozen, r_light)
        self.detect(start, r_light, pace, c)

    def lay_amplitude(self, s_, at, c, factors, pace):
        """The lay of one quantum: the child's record laid at the Node with the least amplitude A at which its own share reads one quantum of its unit at the Node's paces, (2 D + SUM_j R_j) A^2 >= unit x 4 p^2 G^2 (the frame share's term of a lone record with now = before = A; ALGEBRA.md, the lay of the record out whole); the former toy laid the root of T / 2 for every species."""
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


    def unclick(self, frame):
        """The close undone from the log, in the reverse order of its lines: the lays removed, the light restored, the readings' counters restored."""
        for entry in reversed(self.log[frame['log_from']:]):
            at = tuple(entry['node'])
            if entry['event'] == 'birth':
                s_ = entry['line_pair']; A = entry['amplitude']
                self.lay(2 * s_, tuple(entry['minus']), (A, 0, 0, -A), -1); self.lay(2 * s_ + 1, tuple(entry['plus']), (A, 0, 0, A), -1)
                self.light.now[at] = entry['light_now_was']; self.closes[at] -= 1
            elif entry['event'] == 'credit':
                self.light.now[at] = entry['light_now_was']; self.closes[at] -= 1
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
    c = b.content(); cs = [int(x) for x in c.reshape(-1)]; vs = [int(x) for x in b.vol.now.reshape(-1)]
    energy = sum(int(x) * int(x) for rec in b.planes for l in rec for x in l.now.reshape(-1)); odd_max = max(abs(int(x)) for l in b.sign_axes for x in l.now.reshape(-1))
    light_v = max(abs(int(a) - int(bb)) for a, bb in zip(b.light.now.reshape(-1), b.light.before.reshape(-1)))
    packets = {}
    for s_ in range(b.nl):
        for sense in (0, 1):
            re, im = b.planes[2 * s_ + sense]; wgt = re.now * re.now + im.now * im.now; total = int(sum(int(x) for x in wgt.reshape(-1)))
            if total == 0: continue
            idx = np.indices(b.shape); cen = [int(sum(int(w) * int(x) for w, x in zip(wgt.reshape(-1), idx[a].reshape(-1)))) * 1000 // total for a in range(3)]
            packets['row %d sense %d' % (s_ + 1, 1 if sense else -1)] = {'centroid (thousandths of a Link)': cen, 'nodes with levels': int(sum(1 for x in wgt.reshape(-1) if int(x) > 0)), 'energy bits': total.bit_length()}
    W = Z(b.shape)
    for re, im in b.planes: W = W + wronskian(re, im)
    n, _bits = b.census(); tens = [int(x) for l in b.vol_axes for x in l.now.reshape(-1)]
    return {'i': b.interval, 'packets (reader)': packets, 'content min/mean/max': [min(cs), sum(cs) // len(cs), max(cs)], 'volume mean': sum(vs) // len(vs), 'births': b.counts['births'], 'body_clicks': b.counts['body_clicks'],
            'refused': b.counts['refused_stop'] + b.counts['refused_origin'] + b.counts['refused_lay'] + b.counts['refused_orientation'], 'refused_lay': b.counts['refused_lay'], 'refused_orientation': b.counts['refused_orientation'], 'turns': b.counts['turns'],
            'integers': n, 'max bits': maxbits, 'max transient bits': b.max_transient, 'sign level max': max(abs(int(x)) for x in b.sign.now.reshape(-1)), 'planes energy bits': energy.bit_length(),
            'links at the wall': int(sum(1 for f in b.link_factors()[0::2] for x in f.reshape(-1) if int(x) == 0)), 'tension min/max': [min(tens), max(tens)], 'odd max bits': odd_max.bit_length(), 'link count max': b.count_max, 'orbit table': len(b.orbit),
            'W total': int(sum(int(x) for x in W.reshape(-1))), 'W abs sum': int(sum(abs(int(x)) for re, im in b.planes for x in wronskian(re, im).reshape(-1))), 'light velocity max': light_v}


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
    return {'world': world, 'universe': universe, 'den': b.den, 'cube': b.cube, 'intervals': intervals, 'lifts': [(None, str(num), str(s)) for _v, num, s in b.lifts], 'T': b.T, 'gamma': b.gamma, 'G': b.G,
            'counts': {k: str(v) for k, v in b.counts.items()}, 'turns': b.turns, 'rows': rows, 'run_back': run_back, 'log': kept_log}


if __name__ == '__main__':
    sys.set_int_max_str_digits(0)
    # usage: lean_full.py <world.json> <out.json> [back N]
    universe, world = load_world(sys.argv[1])
    found = record(universe, world, int(sys.argv[sys.argv.index('back') + 1]) if 'back' in sys.argv else 0, lambda line: print(line, flush=True))
    json.dump(found, open(sys.argv[2], 'w'))
