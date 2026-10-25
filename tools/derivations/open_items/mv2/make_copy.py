"""mv2's flagged COPY of David's lean toy (toys-5 head, tools/derivations/mv2/toy/lean_full.py), written by this script and never by hand:
the copy is lean_full.py with the `at` lay gaining one field, `wave`, and the credit line gaining two readings; nothing else moves.
Every replacement below must match the toy's text exactly once, else the script refuses. Run: python make_copy.py  (writes lean_mv2.py beside it).

The field (the derivation in mv2_REPORT.md, item 1): "wave": [h_x, h_y, h_z], three signed integers in den's unit, h_a = den sin(k_a / 2),
the sine of the half-angle per Link along each axis; [0, 0, 0] is the former lay bit for bit; |h_a| > den is a wave number beyond the band's
edge (k = pi, the staggered mode, |h| = den), refused by name. From h the pair of the circle per axis, den cos k_a = (den^2 - 2 h^2) div den and
den sin k_a = 2 h largest_below(den^2 - h^2) div den (a Pythagorean-like point, inside den's circle to the unit, exact at h = 0 and |h| = den);
the pair composed along the offsets from the centre one Link at a time with one rounding per Link (the paces compose: the Link's pair composed);
the running rotation of the kinetic clause, den cos omega(k) = (num SUM_a den cos k_a) div (3 den), its sine by the one search; each sense's
record laid as z_s = A_i exp(i s (k . x - omega t)): re_now = A_i cos(k x), im_now = s A_i sin(k x), re_before = A_i cos(k x + omega),
im_before = s A_i sin(k x + omega), the two senses summed on the one plane (the im lines cancel: the charge 0 at every Node, the re line the
real wave 2 A_i cos(k x - omega t) moving along k at the band's group velocity)."""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'toy', 'lean_full.py')
DST = os.path.join(HERE, 'lean_mv2.py')

text = open(SRC).read()

replacements = []

# 0. the flag and the src path (the copy sits one folder above the toy's)
replacements.append((
    '"""David\'s local lean Node, complete (the owner\'s word, 04:4x: run everything, omit nothing).',
    '"""mv2\'s FLAGGED COPY (2026-10-25) of David\'s lean toy for the moving lay: the `at` lay gains the field `wave` (make_copy.py names every delta); David\'s file under toy/ is untouched.\nDavid\'s local lean Node, complete (the owner\'s word, 04:4x: run everything, omit nothing).'))
replacements.append((
    "sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'src'))  # tools/derivations/toys/lean -> src",
    "sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'src'))  # tools/derivations/mv2 -> src (mv2's copy)"))

# 1. the seed loop: the `at` lay reads `wave`; the massless row with no wave number keeps the drift lay by name
replacements.append((
    """            elif form == 'at':
                n = int(lay['quanta']); at = self.node_of(lay['centre'])
                if r_.gap == 0: z = r_.lines[0]; z.now[at] = z.now[at] + n * self.drift
                else: packets.append((self.records().index(r_), at, int(lay.get('width', 0)), n))""",
    """            elif form == 'at':
                n = int(lay['quanta']); at = self.node_of(lay['centre']); wave = self.wave_of(lay.get('wave', [0, 0, 0]))  # mv2: the one field gained, h_a = den sin(k_a / 2) per axis
                if r_.gap == 0 and wave == (0, 0, 0): z = r_.lines[0]; z.now[at] = z.now[at] + n * self.drift  # the former massless lay kept by name: the drift at one Node (the double root carries no rotation at k = 0)
                else: packets.append((self.records().index(r_), at, int(lay.get('width', 0)), n, wave))"""))
replacements.append((
    "        for s_, at, h, n in packets: self.lay_packet(s_, at, h, n)",
    "        for s_, at, h, n, wave in packets: self.lay_packet(s_, at, h, n, wave)"))

# 2. lay_packet with the wave number (the derivation's form), David's form bit for bit at wave (0, 0, 0)
old_lay = text[text.index("    def lay_packet(self, rec, at, h, n):"):text.index("    # ---- the readings at the interval's start")]
new_lay = '''    def wave_of(self, h):
        """mv2: the wave number as the world file carries it, three signed integers h_a = den sin(k_a / 2) (the sine of the half-angle per Link, in den's unit); |h_a| above den is a wave number beyond the band's edge (the staggered mode k = pi at |h| = den), refused by name."""
        h = tuple(int(x) for x in h)
        if len(h) != 3: raise ValueError('a wave number is three integers, one per axis: %r' % (h,))
        if any(abs(x) > self.den for x in h): raise ValueError('a wave number beyond the band\\'s edge: |h| = %d above den = %d (|h| = den is the edge, k = pi)' % (max(abs(x) for x in h), self.den))
        return h

    def circle_point(self, h):
        """mv2: the point of den's circle at the half-angle sine h: den cos k = (den^2 - 2 h^2) div den, den sin k = (2 h largest_below(den^2 - h^2)) div den; exact at h = 0 (den, 0) and |h| = den (-den, 0), inside the circle to the unit elsewhere (Pythagorean-like)."""
        den = self.den
        c = (den * den - 2 * h * h) // den
        s = (2 * h * rule3.largest_below(den * den - h * h)) // den
        return c, s

    def turned_by(self, C, S, c, s):
        """mv2: the pair (C, S) over den rotated by the pair (c, s) over den, one rounding (half up) per part: the Link's pair composed one Link at a time (The paces compose: the orbit of the phase)."""
        den = self.den
        return (2 * (C * c - S * s) + den) // (2 * den), (2 * (S * c + C * s) + den) // (2 * den)

    def lay_packet(self, rec, at, h, n, wave=(0, 0, 0)):
        """The `at` lay of a plane row: the conjugate pair (the two records at the senses -1 and 1) laid over the raised cosine's envelope of the half-width h (the weights 2, 1 at h = 2; 4, 3, 1 at h = 3; the product over the three axes), each record at the largest amplitude A at which its share at the vacuum's weight, summed over the packet, is at most n quanta of its unit (a search by comparisons); each Node's lines at the band's rotation at the wave number (mv2, the one field gained): with (c_a, s_a) the circle's point per axis from h_a and (C_i, S_i) their composition along the offsets from the centre (one rounding per Link), den cos omega(k) = (num SUM_a c_a) div (3 den) the kinetic clause's running rotation and (C'_i, S'_i) = (C_i, S_i) turned by (c_w, s_w): re_now = (A w_i div w_0) C_i div den, im_now = sense (A w_i div w_0) S_i div den, re_before = (A w_i div w_0) C'_i div den, im_before = sense (A w_i div w_0) S'_i div den; at wave (0, 0, 0) this is David's rest lay bit for bit (C = den, S = 0, c_w = num, s_w = the pair's sine: re_now = A w_i div w_0, re_before = re_now num div den, im_now = 0, im_before = sense re_now s div den, Z1's form)."""
        weights = {2: (2, 1), 3: (4, 3, 1)}.get(h)
        if weights is None: raise ValueError('a plane packet has the half-width 2 or 3: a body is laid over its packet')
        r_ = self.records()[rec]; num = r_.pair[0]; w0 = weights[0] ** 3  # the pair's numbers
        den = self.den
        points = [self.circle_point(x) for x in wave]  # the circle's point per axis, (den cos k_a, den sin k_a)
        c_w = (num * sum(c for c, _s in points)) // (3 * den)  # the running rotation's cosine over den (the kinetic clause: den cos omega(k) = (num SUM_a den cos k_a) div (3 den))
        s_w = rule3.largest_below(den * den - c_w * c_w)  # its sine by the one search (sine_den's form at the running cosine)
        envelope = Z(self.shape); C = Z(self.shape) + den; S = Z(self.shape); Cb = Z(self.shape) + den; Sb = Z(self.shape)
        for j in np.ndindex(*(2 * h - 1,) * 3):
            off = [x - (h - 1) for x in j]
            node = tuple((at[a] + off[a]) % self.cube for a in range(3))
            envelope[node] += weights[abs(off[0])] * weights[abs(off[1])] * weights[abs(off[2])]
            Ci, Si = den, 0  # the phase at the offset: the pair composed along each axis |off_a| times, the conjugate pair for a negative offset (the 48: the pair at -n the conjugate of the pair at +n)
            for a in range(3):
                c, s = points[a]
                for _ in range(abs(off[a])): Ci, Si = self.turned_by(Ci, Si, c, s if off[a] > 0 else -s)
            C[node], S[node] = Ci, Si
            Cb[node], Sb[node] = self.turned_by(Ci, Si, c_w, s_w)  # the level before: the phase turned forward by the running rotation (z_before = A exp(i (k x + omega)))
        c_ = self.content(); factors = self.link_factors(); r = self.rule_of(r_, c_, factors); self.start_content = c_
        def record(A, sense):
            base = (A * envelope) // w0
            re = Line((base * C) // den, (base * Cb) // den, None, self.w)
            im = Line(sense * ((base * S) // den), sense * ((base * Sb) // den), None, self.w)
            return re, im
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
        s_k = [s for _c, s in points]
        velocity_milli = [0 if s_w == 0 else (1000 * num * s) // (3 * den * s_w) for s in s_k]  # the band's group velocity per axis in milli-Links per interval, (num sin k_a) / (3 den sin omega(k)), an integer reading (the quotient)
        self.log.append({'event': 'lay', 'i': 0, 'node': list(at), 'line_pair': rec, 'width': h, 'quanta': n, 'amplitude': low, 'share': share_of(low), 'unit': self.units[rec], 'nodes': int(sum(1 for x in envelope.reshape(-1) if int(x) > 0)),
                         'wave': list(wave), 'den_cos_k': [c for c, _s in points], 'den_sin_k': s_k, 'den_cos_omega': c_w, 'den_sin_omega': s_w, 'group_velocity_milli': velocity_milli})

'''
replacements.append((old_lay, new_lay))

# 3. the credit line gains the record's momentum terms at the Node (the pair per axis from the one-Link frame: the Node's and its neighbours' two start levels) and the running cosine per axis
replacements.append((
    "        frame['factors'] = [int(f[at]) for f in self.start_factors]\n        return {'event': 'credit',",
    """        frame['factors'] = [int(f[at]) for f in self.start_factors]
        num = self.records()[rec].pair[0]; p_record = []; running = []  # mv2: the record's lattice momentum term at the Node per axis, F_(i,i-a) - F_(i,i+a) summed over its two lines with F_ij = num (now_i before_j - before_i now_j) (The lattice momentum: the board's sum of these terms is P_a = 2 num SUM_i (now_(i+a) before_i - now_i before_(i+a))), from the start levels; and the running cosine per axis den (now_(i+a) + now_(i-a)) div (2 now_i) on the re line (0 where now_i = 0)
        for a in range(3):
            up, down = nodes[2 * a], nodes[2 * a + 1]
            p = 0
            for l0 in (re0, im0):
                p += int(l0.now[at]) * int(l0.before[down]) - int(l0.before[at]) * int(l0.now[down]) - (int(l0.now[at]) * int(l0.before[up]) - int(l0.before[at]) * int(l0.now[up]))
            p_record.append(num * p)
            running.append(0 if int(re0.now[at]) == 0 else (self.den * (int(re0.now[up]) + int(re0.now[down]))) // (2 * int(re0.now[at])))
        frame['p_record'] = p_record; frame['running_cosine'] = running
        return {'event': 'credit',"""))

out = text
for old, new in replacements:
    count = out.count(old)
    if count != 1:
        sys.exit('refused: a replacement matches %d times, not once: %r' % (count, old[:80]))
    out = out.replace(old, new)
open(DST, 'w').write(out)
print('written', DST, len(out), 'bytes;', len(replacements), 'replacements')
