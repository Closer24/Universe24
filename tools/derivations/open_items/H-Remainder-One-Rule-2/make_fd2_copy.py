"""fd2's flagged COPY of David's lean toy (tools/derivations/open_items/H-Remainder-One-Rule-2/toy_david/lean_full.py and decoder_full.py, the toys-5 head
copied 2026-10-25, md5 b2959da3d37bc96dc0625b956a9eb240 / 4465a739008c24887b9fafad32d3ca1a), written by this script and never
by hand into tools/derivations/open_items/H-Remainder-One-Rule-2/toy_fd2/. David's files are untouched. Every replacement below must match David's text exactly
once, else the script refuses.

The copy is David's Node with the unifications of fd2_REPORT.md, section 1, each exact (the same integers by algebra, the record bit
for bit by measurement):
  U1  one bilinear `cross(x_i, y_i, x_j, y_j) = x_i y_j - y_i x_j` in place of eight spellings: the Wronskian of a plane, the current
      across a Link, the plane's sign current, the twist of two transverse currents, the form now^2 - next x before, the lattice
      momentum's change, the two children's Wronskians at a birth, the credit's Wronskian (and in the decoder the rationals' order
      and the distance of a rational to a pair).
  U2  one turn `turn_pair(re, im, c, s, X)` (one rounding half up per part) in place of three spellings: the phase pair over X and
      the odd tangent triple over its wall in `turned_arrival`, and the decoder's `solve` re-running the same turn.
  U3  one neighbour `neighbour(at, port)` in place of four spellings of the Node beyond a Port (frame_nodes, take, meet, momentum_of).
  U4  the toy's `odd_round(q, d) = (2 q + d) div (2 d)` is `paces.rounded(q, d)` to the letter: the method goes, the primitive stays.
  U5  the Link's frame sign is the parity of the Link's even part: 1 - 2 ((b_i + b_j) mod 2) in place of 1 - 2 (b_i xor b_j), equal on
      the bits 0 and 1 the phase row's wall 2 allows (its remainder is in [0, 2), its complement 1 - r).
  U6  the take is the lay at -1 on the massless record: `lay(rec, at, (toward levels, 0, 0, 0), sign)` forward in `take_at` and the
      same lay at the sign -1 in `unclick` (once per take: once per Node among a Node's birth lines, once per credit line) in place
      of the assignment of the logged level.
  U7  the decoder's `quot` is the division act's quotient (rule3.division_forward); `cmp_rat` and `nearest` read the one bilinear.
Run: python make_fd2_copy.py   (writes toy_fd2/lean_full.py and toy_fd2/decoder_full.py, copies the json files beside them)."""
import os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'toy_david')
DST = os.path.join(HERE, 'toy_fd2')
os.makedirs(DST, exist_ok=True)


def apply(text, replacements, name):
    out = text
    for old, new in replacements:
        count = out.count(old)
        if count != 1:
            sys.exit('refused (%s): a replacement matches %d times, not once: %r' % (name, count, old[:100]))
        out = out.replace(old, new)
    return out


# ---------------------------------------------------------------- lean_full.py
text = open(os.path.join(SRC, 'lean_full.py')).read()
R = []

R.append((
    '"""David\'s local lean Node, complete (the owner\'s word, 04:4x: run everything, omit nothing).',
    '"""fd2\'s FLAGGED COPY (2026-10-25) of David\'s lean toy with the code\'s unifications U1 to U7 of fd2_REPORT.md (make_fd2_copy.py names every delta); David\'s file under toy_david/ is untouched; the record bit for bit David\'s (measured: the state hash at every interval, the log, the run back, the gates).\nDavid\'s local lean Node, complete (the owner\'s word, 04:4x: run everything, omit nothing).'))

# U1, U2: the two primitives after `across`
R.append((
    '''def link(port, even=(), odd=(), frame_bits=None):''',
    '''def cross(x_i, y_i, x_j, y_j):
    """The one bilinear of the law (fd2, U1): x_i y_j - y_i x_j, the 2 x 2 determinant of two readings (x, y) at two places (i, j), odd under the exchange of the places and under the exchange of the readings. The Wronskian of a plane is cross(re_now, im_now, re_before, im_before) (two lines, two slots); the current across a Link is cross(now_i, before_i, now_j, before_j) (one line, two Nodes); the plane's sign current is cross(re_i, im_i, re_j, im_j) differenced over the axis's two Ports; the twist is cross(u_b(i), u_c(i), u_b(j), u_c(j)); the form now^2 - next x before is cross(now, before, next, now), the line with itself one interval on; the lattice momentum's change is 2 num cross(d_now, d_before, now_down - now_up, before_down - before_up)."""
    return x_i * y_j - y_i * x_j


def turn_pair(re, im, c, s, X):
    """The pair (re, im) turned by the pair (c, s) over X, one rounding half up per part (fd2, U2): ((2 (c re - s im) + X) div (2 X), (2 (s re + c im) + X) div (2 X)); the phase pair over the amplitude X and the odd tangent triple over its wall W^2 + n^2 are the same turn, and the decoder's solve re-runs this one."""
    a_re = (c * re - s * im); a_im = (s * re + c * im)
    return (2 * a_re + X) // (2 * X), (2 * a_im + X) // (2 * X)


def link(port, even=(), odd=(), frame_bits=None):'''))

# U5: the frame sign the parity of the even part
R.append((
    "    f = None if frame_bits is None else 1 - 2 * (frame_bits ^ across(frame_bits, port))\n    return evens, odds, f",
    "    f = None if frame_bits is None else 1 - 2 * ((frame_bits + across(frame_bits, port)) % 2)  # fd2 U5: the frame sign is the parity of the Link's even part (the bits 0 and 1 of the wall 2: b_i xor b_j = (b_i + b_j) mod 2)\n    return evens, odds, f"))

# U1: the Wronskian
R.append((
    '    return re.now * im.before - im.now * re.before\n',
    '    return cross(re.now, im.now, re.before, im.before)  # fd2 U1\n'))

# U1: the plane's sign current
R.append((
    '        found.append(re.now * dz_im - im.now * dz_re)\n',
    '        found.append(cross(re.now, im.now, dz_re, dz_im))  # fd2 U1\n'))

# U1: the current across a Link
R.append((
    '        return line.now * across(line.before, port) - line.before * across(line.now, port)\n',
    '        return cross(line.now, line.before, across(line.now, port), across(line.before, port))  # fd2 U1\n'))

# U1: the twist
R.append((
    '        return ub * across(uc, 2 * a) - uc * across(ub, 2 * a)\n',
    '        return cross(ub, uc, across(ub, 2 * a), across(uc, 2 * a))  # fd2 U1\n'))

# U1: the form
R.append((
    '                for l0, lv in zip(start, levels): forms = forms + (l0.now * l0.now - lv * l0.before)\n',
    '                for l0, lv in zip(start, levels): forms = forms + cross(l0.now, l0.before, lv, l0.now)  # fd2 U1: the form is the line\'s Wronskian with itself one interval on\n'))

# U2: the turn
R.append((
    '''        a_re = (c * re_j - s * im_j); a_im = (s * re_j + c * im_j)
        a_re, a_im = (2 * a_re + self.X) // (2 * self.X), (2 * a_im + self.X) // (2 * self.X)
        b_re = (tc * a_re - ts * a_im); b_im = (ts * a_re + tc * a_im)
        return [(2 * b_re + tw) // (2 * tw), (2 * b_im + tw) // (2 * tw)]''',
    '''        a_re, a_im = turn_pair(re_j, im_j, c, s, self.X)  # fd2 U2: the one turn, by the phase pair over X
        return list(turn_pair(a_re, a_im, tc, ts, tw))  # and by the odd tangent triple over its wall'''))

# U4: odd_round is paces.rounded
R.append((
    '''    def odd_round(self, q, d):
        """round(q / d) to the nearest for q odd and d even (never a half): (2 q + d) div (2 d); the odd rounding of the ride's momenta (R5)."""
        return (2 * q + d) // (2 * d)

''',
    ''))
R.append((
    '                forms = forms + self.odd_round(2 * p1 + 1, d) * self.odd_round(2 * p2 + 1, d) + (-a * f) // self.w\n',
    '                forms = forms + paces.rounded(2 * p1 + 1, d) * paces.rounded(2 * p2 + 1, d) + (-a * f) // self.w  # fd2 U4: the odd rounding of an odd numerator over an even wall is the one rounding half up, paces.rounded, to the letter\n'))

# U3: the neighbour
R.append((
    '''    def frame_nodes(self, at):
        return [at] + [tuple((at[a] + (side if a == axis else 0)) % self.cube for a in range(3)) for axis, side in AXES]
''',
    '''    def neighbour(self, at, port):
        """The Node beyond the Port of the Node `at`, on the torus (fd2, U3): the one spelling of a neighbour's place, as `across` is the one read of a neighbour's array."""
        axis, side = AXES[port]
        return tuple((at[a] + (side if a == axis else 0)) % self.cube for a in range(3))

    def frame_nodes(self, at):
        return [at] + [self.neighbour(at, port) for port in range(6)]
'''))
R.append((
    '''        for (axis, side), reach in zip(AXES, r_gap0.reaches):
            n = tuple((at[a] + (side if a == axis else 0)) % self.cube for a in range(3))
            L += int(np.asarray(reach)[at]) * int(line.before[n])''',
    '''        for port, reach in enumerate(r_gap0.reaches):
            n = self.neighbour(at, port)  # fd2 U3
            L += int(np.asarray(reach)[at]) * int(line.before[n])'''))
R.append((
    '''                j = tuple((at[a] + (1 if a == axis else 0)) % self.cube for a in range(3))
                if frozen[j]''',
    '''                j = self.neighbour(at, 2 * axis)  # fd2 U3: the +a end
                if frozen[j]'''))
R.append((
    '''            up = tuple((at[k] + (1 if k == a else 0)) % self.cube for k in range(3)); down = tuple((at[k] - (1 if k == a else 0)) % self.cube for k in range(3))
            found.append(2 * num * (d_now * (int(line_before[down]) - int(line_before[up])) + d_before * (int(line_now[up]) - int(line_now[down]))))''',
    '''            up, down = self.neighbour(at, 2 * a), self.neighbour(at, 2 * a + 1)  # fd2 U3
            found.append(2 * num * cross(d_now, d_before, int(line_now[down]) - int(line_now[up]), int(line_before[down]) - int(line_before[up])))  # fd2 U1: the change of the momentum is the one bilinear of the move against the neighbours' difference'''))

# U1: the children's Wronskians and the credit's
R.append((
    "                W_children = [int(re.now[w_] * im.before[w_] - im.now[w_] * re.before[w_]) for w_ in (minus, plus)]",
    "                W_children = [int(cross(re.now[w_], im.now[w_], re.before[w_], im.before[w_])) for w_ in (minus, plus)]  # fd2 U1"))
R.append((
    "        W = int(re.now[at] * im.before[at] - im.now[at] * re.before[at])\n        sre, sim = self.stepped[rec]",
    "        W = int(cross(re.now[at], im.now[at], re.before[at], im.before[at]))  # fd2 U1\n        sre, sim = self.stepped[rec]"))

# U6: the take is the lay at the massless record
R.append((
    "        z.now[at] = now + toward * levels; self.closes[at] += 1\n",
    "        self.lay(self.records().index(self.row(2, gap=0)), at, (toward * levels, 0, 0, 0)); self.closes[at] += 1  # fd2 U6: the take is the lay of -toward x levels toward the level before, the same act\n"))
R.append((
    '''        z = self.row(2, gap=0).lines[0]
        for entry in reversed(self.log[frame['log_from']:]):
            at = tuple(entry['node'])
            if entry['event'] == 'birth':
                s_ = entry['line_pair']; A = entry['amplitude']
                self.lay(s_, tuple(entry['minus']), (A, 0, 0, -A), -1); self.lay(s_, tuple(entry['plus']), (A, 0, 0, A), -1)
                z.now[at] = entry['light_now_was']; self.closes[at] -= 1
            elif entry['event'] == 'credit':
                z.now[at] = entry['light_now_was']; self.closes[at] -= 1''',
    '''        z = self.row(2, gap=0).lines[0]; gap0 = self.records().index(self.row(2, gap=0)); taken_back = set()
        def take_back(entry):  # fd2 U6: the take undone is the same lay at -1: toward read from the level before (unmoved by the close) against the logged level, the levels the logged count
            toward = 1 if int(z.before[at]) > entry['light_now_was'] else -1
            self.lay(gap0, at, (toward * entry['levels'], 0, 0, 0), -1)
        for entry in reversed(self.log[frame['log_from']:]):
            at = tuple(entry['node'])
            if entry['event'] == 'birth':
                s_ = entry['line_pair']; A = entry['amplitude']
                self.lay(s_, tuple(entry['minus']), (A, 0, 0, -A), -1); self.lay(s_, tuple(entry['plus']), (A, 0, 0, A), -1)
                if at not in taken_back: take_back(entry); taken_back.add(at)  # one take per Node of the births, its children's walls summed
                self.closes[at] -= 1
            elif entry['event'] == 'credit':
                take_back(entry); self.closes[at] -= 1'''))

out = apply(text, R, 'lean_full.py')
open(os.path.join(DST, 'lean_full.py'), 'w').write(out)
print('written', os.path.join(DST, 'lean_full.py'), len(out), 'bytes;', len(R), 'replacements')

# ---------------------------------------------------------------- decoder_full.py
text = open(os.path.join(SRC, 'decoder_full.py')).read()
R = []
R.append((
    '"""The decoder of the full lean toy, integers only',
    '"""fd2\'s FLAGGED COPY (2026-10-25) of David\'s decoder with U1, U2 and U7 of fd2_REPORT.md (make_fd2_copy.py names every delta); the gates\' output bit for bit David\'s (measured).\nThe decoder of the full lean toy, integers only'))
R.append((
    "from event_universe.core.paces import sine_den\nMIL = 1000000",
    "from event_universe.core.paces import sine_den\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\nfrom lean_full import cross, turn_pair  # fd2: the Node's one bilinear and one turn, read by the decoder from the same primitive\nMIL = 1000000"))
R.append((
    '    return None if b == 0 else (a * scale) // b\n',
    '    return None if b == 0 else rule3.division_forward(a * scale, b, 0)[0]  # fd2 U7: the division act\'s quotient\n'))
R.append((
    '    s = p[0] * q[1] - q[0] * p[1]\n',
    '    s = cross(p[0], p[1], q[0], q[1])  # fd2 U1: the order of two rationals is the sign of the one bilinear\n'))
R.append((
    '    return min(R.NAMES.items(), key=lambda kv: abs(N * R.den - kv[0] * D))[1][0]\n',
    '    return min(R.NAMES.items(), key=lambda kv: abs(cross(N, D, kv[0], R.den)))[1][0]  # fd2 U1: the distance of a rational to a pair is the one bilinear\n'))
R.append((
    '''            m = ((2 * (c_ * m[0] - s_ * m[1]) + X) // (2 * X), (2 * (s_ * m[0] + c_ * m[1]) + X) // (2 * X))
            n = odd[port]; tc, ts, tw = Wl * Wl - n * n, 2 * Wl * n, Wl * Wl + n * n
            m = ((2 * (tc * m[0] - ts * m[1]) + tw) // (2 * tw), (2 * (ts * m[0] + tc * m[1]) + tw) // (2 * tw))''',
    '''            m = turn_pair(m[0], m[1], c_, s_, X)  # fd2 U2: the Node's one turn, re-run by the decoder
            n = odd[port]; tc, ts, tw = Wl * Wl - n * n, 2 * Wl * n, Wl * Wl + n * n
            m = turn_pair(m[0], m[1], tc, ts, tw)'''))
out = apply(text, R, 'decoder_full.py')
open(os.path.join(DST, 'decoder_full.py'), 'w').write(out)
print('written', os.path.join(DST, 'decoder_full.py'), len(out), 'bytes;', len(R), 'replacements')

for name in os.listdir(SRC):
    if name.endswith('.json') or name in ('runback_test.py', 'reach_test.py', 'cube48_test.py', 'one_node_test.py'):
        shutil.copy(os.path.join(SRC, name), os.path.join(DST, name))
print('json files and David\'s four tests copied beside the copy')
