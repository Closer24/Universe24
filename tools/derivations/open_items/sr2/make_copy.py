"""sr2 (2026-10-25): makes the flagged COPY lean_sr2.py of David's toy (toy/lean_full.py, never edited in place).

Every change is a replacement listed below, each asserted to occur exactly once in the toy's text, so the copy's
departure from the toy is this file and nothing else. A world and a universe of David's (no shape-8 row, no `spin`,
no `sense`, no `control.held_potential`) run through the copy bit for bit: the state, the log and the counts equal.

The flags and the shape-8 row:
  - a row {"shape": 8, "pair": [num, den]} in the universe file is a quanta row of four planes (the spinor row): Rule3
    on its eight lines alike, each arrival turned as a plane's (the Link's pair and the odd tangent on the four
    planes alike), and the Node term -K SUM_c Phi_c sigma_c psi_now added to the numerator before the row's one
    division (K = rounded(num p^2 G^2, Gamma); Phi the curl of the six neighbours' odd lines; sigma the three Pauli
    matrices as signed permutations of the eight lines, sigma_y by i, the planes' quarter turn); its Wronskian and
    its current (the sums over its four planes) source the sign's row and its form the metric's, as a plane's do;
    its children at a birth are laid with the spin along the Link's axis, the - child the conjugate;
  - the `at` lay takes `spin` (eight integers, the lines' weights of the state) for a shape-8 row (refused by name
    without it) and an optional `sense` (sp2's flag: one record alone; else the conjugate pair);
  - `control.held_potential` (sp2's flag): hand-held lines of the shape-4 row, set at the start and restored after
    every act in either direction (the magnet as a control, no lay of the law).
Integers only.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'toy', 'lean_full.py')
OUT = os.path.join(HERE, 'lean_sr2.py')

HELPERS = '''

def pairs(lines):
    """sr2: a row's lines as its planes (re, im) in order: a plane is one pair, a shape-8 row four."""
    return [(lines[2 * k], lines[2 * k + 1]) for k in range(len(lines) // 2)]


def row_wronskian(lines):
    """sr2: a row's Wronskian, the sum over its planes of W = re_now im_before - im_now re_before (the charge density; one plane for shape 2, four for shape 8)."""
    found = 0
    for re, im in pairs(lines): found = found + wronskian(re, im)
    return found


SIGMA = (lambda v: [v[4], v[5], v[6], v[7], v[0], v[1], v[2], v[3]],
         lambda v: [v[5], -v[4], v[7], -v[6], -v[1], v[0], -v[3], v[2]],
         lambda v: [v[0], v[1], v[2], v[3], -v[4], -v[5], -v[6], -v[7]])  # sr2: the Pauli matrices on the eight lines (re Z10, im Z10, re Z11, im Z11, re Z20, ...), psi_k = Z_k0 + zeta Z_k1: sigma_x the swap of the two components, sigma_y the swap with i (the planes' quarter turn) and the sign, sigma_z the components' signs (sr2_algebra.py (2))


def spin_state(axis):
    """sr2: the spin-up state along the axis as the eight lines' weights, (1 + sigma_a) e_1 reduced by its gcd (sr2_algebra.py (8)): x (1, 0, 0, 0, 1, 0, 0, 0), y (1, 0, 0, 0, 0, 1, 0, 0), z (1, 0, 0, 0, 0, 0, 0, 0)."""
    e1 = [1, 0, 0, 0, 0, 0, 0, 0]; v = [a + b for a, b in zip(e1, SIGMA[axis](e1))]
    g = 0
    for x in v: g = math.gcd(g, abs(x))
    return [x // g for x in v]


def child_levels(A, chi, sense):
    """sr2: a child's lines at the quarter turn from its state chi (the lines' weights, (p, q) per plane) and its sense: per plane (re_now, re_before, im_now, im_before) = (A p, -sense A q, A q, sense A p), the before a quarter period behind (a plane's (A, 0, 0, sense A) at chi = (1, 0)); the - child reads the conjugate state (p, -q)."""
    out = []
    for p, q in zip(chi[0::2], chi[1::2]):
        q = sense * q if len(chi) > 2 else q
        out += [A * p, -sense * A * q, A * q, sense * A * p]
    return out
'''

PAULI = '''    def pauli_term(self, psi, odd, num, c):
        """sr2: the spinor row's Node term, one integer per line added to Rule3's numerator before the row's one division: -K SUM_c Phi_c (sigma_c psi)_l, with psi the row's eight start levels, Phi_c = gradient(A_b, a) - gradient(A_a, b) for (a, b, c) cyclic the curl of the six neighbours' odd lines (the one-Link read, twice the centred curl), and K = rounded(num p^2 G^2, Gamma) the Link's own coefficient R / (2 Gamma) at the vacuum (one rounding of an interval's coefficient, as the Link factor's; no level divided): the Chebyshev form of Dirac's evolution, 2 cos omega = 2 cos omega_0 - (nu / 3) ((k + A)^2 + sigma . B), B_c = Phi_c / (2 Gamma) radians per plaquette; g = 2 with no number (ALGEBRA.md, Spin, the g = 2 derivation)."""
        pace = paces.link_pace_of(self.gamma, c); K = paces.rounded(num * pace * pace * self.G * self.G, self.gamma)
        Phi = [gradient(odd[b], a) - gradient(odd[a], b) for (a, b) in ((1, 2), (2, 0), (0, 1))]
        turned = [S(psi) for S in SIGMA]
        return [-(K * (Phi[0] * x + Phi[1] * y + Phi[2] * z)) for x, y, z in zip(*turned)]

    def spin_at(self, lines, at):
        """sr2: the row's bilinears at a Node from its levels: W (the sum of the planes' Wronskians, the charge), s_W = psi_now^T J sigma psi_before (the Wronskian-type spin, T_0-odd as W) and s_D = psi_now^T sigma psi_before (the density-type spin, even in the sense), all three integers."""
        n = [int(l.now[at]) for l in lines]; b = [int(l.before[at]) for l in lines]
        J = lambda v: [x for k in range(len(v) // 2) for x in (-v[2 * k + 1], v[2 * k])]
        dot = lambda u, v: sum(x * y for x, y in zip(u, v))
        return {'W': dot(n, J(b)), 's_W': [dot(n, J(S(b))) for S in SIGMA], 's_D': [dot(n, S(b)) for S in SIGMA], 's_N': [dot(n, S(n)) for S in SIGMA]}  # s_N = psi_now^T sigma psi_now: the components' weights at one level (|Z_1|^2 - |Z_2|^2 for z), free of the two components' rotation phases

'''

REPLACEMENTS = [
    # 0. the head
    ('"""David\'s local lean Node, complete',
     '"""sr2 flagged copy of tools/derivations/sr2/toy/lean_full.py (made by make_copy.py; the shape-8 spinor row, the `spin` and `sense` keys of the `at` lay, `control.held_potential`). David\'s local lean Node, complete'),
    # 1. the path to src
    ("os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'src'))  # tools/derivations/toys/lean -> src",
     "os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'src'))  # tools/derivations/sr2 -> src (the copy's place)"),
    # 2. the helpers after the Wronskian
    ('''def wronskian(re, im):
    """The plane's bilinear W = re_now im_before - im_now re_before at every Node (the charge density, the sign's source)."""
    return re.now * im.before - im.now * re.before
''',
     '''def wronskian(re, im):
    """The plane's bilinear W = re_now im_before - im_now re_before at every Node (the charge density, the sign's source)."""
    return re.now * im.before - im.now * re.before
''' + HELPERS),
    # 3. the acts' order: the shape-8 row with the planes (its Wronskian and form read by the held rows after it)
    ("        order = lambda r: 0 if r.wall is not None else {2: 1 + (r.gap == 0), 4: 3, 10: 4}.get(r.shape, 5)",
     "        order = lambda r: 0 if r.wall is not None else {2: 1 + (r.gap == 0), 8: 1, 4: 3, 10: 4}.get(r.shape, 5)  # sr2: the shape-8 row acted with the planes"),
    # 4. the records: the shape-2 and shape-8 rows
    ("        return [r for r in self.rows_ if r.shape == 2]",
     "        return [r for r in self.rows_ if r.shape in (2, 8)]  # sr2: the quanta rows, the planes (shape 2) and the spinor rows (shape 8)"),
    # 5. the lay onto a quanta row
    ("            if r_ is not None and r_.shape != 2: raise ValueError('a lay is onto a plane (shape 2)')",
     "            if r_ is not None and r_.shape not in (2, 8): raise ValueError('a lay is onto a quanta row (shape 2 or 8)')  # sr2"),
    ("                else: packets.append((self.records().index(r_), at, int(lay.get('width', 0)), n))",
     "                else: packets.append((self.records().index(r_), at, int(lay.get('width', 0)), n, lay.get('sense'), lay.get('spin'), lay.get('amplitude')))  # sr2 flags: `sense` one record alone; `spin` the shape-8 state; `amplitude` the test's lay at a given amplitude (the 48 test's images)"),
    ("        for s_, at, h, n in packets: self.lay_packet(s_, at, h, n)",
     "        for s_, at, h, n, one_sense, spin, amplitude in packets: self.lay_packet(s_, at, h, n, one_sense, spin, amplitude)"),
    # 6. the packet of a quanta row: the state's weights per plane
    ("    def lay_packet(self, rec, at, h, n):",
     "    def lay_packet(self, rec, at, h, n, one_sense=None, spin=None, amplitude=None):"),
    ("        while high - low > 1:\n            middle = (low + high) // 2\n            if share_of(middle) <= target: low = middle\n            else: high = middle\n",
     "        while high - low > 1:\n            middle = (low + high) // 2\n            if share_of(middle) <= target: low = middle\n            else: high = middle\n"
     "        if amplitude is not None: low = int(amplitude)  # sr2 flag: the test's lay at the amplitude named (the 48 test lays every image at the base's amplitude)\n"),
    ("        r_ = self.records()[rec]; num = r_.pair[0]; sn = sine_den(num, self.den); w0 = weights[0] ** 3  # the pair's numbers",
     "        r_ = self.records()[rec]; num = r_.pair[0]; sn = sine_den(num, self.den); w0 = weights[0] ** 3  # the pair's numbers\n"
     "        if r_.shape == 8 and (spin is None or len(spin) != 8): raise ValueError('a shape-8 lay names its state: `spin`, eight integers, the lines\\' weights')  # sr2\n"
     "        chi = [1, 0] if r_.shape == 2 else [int(x) for x in spin]  # sr2: the state's weights (p, q) per plane; a plane's (1, 0)"),
    ('''        def record(A, sense):
            re_now = (A * envelope) // w0
            return Line(re_now, (re_now * num) // self.den, None, self.w), Line(Z(self.shape), sense * ((re_now * sn) // self.den), None, self.w)
        def share_of(A):
            re, im = record(A, 1)
            return int(sum(int(x) for x in (self.share(re, r, vacuum=True) + self.share(im, r, vacuum=True)).reshape(-1)))''',
     '''        def record(A, sense):  # sr2: every plane of the row at the band's rest rotation from its weights (p, q): now = A (p, q) env div w0, before = now turned by sense omega_0; the sense -1 record reads the conjugate state (p, -q); a plane's (1, 0) bit for bit David's
            found = []
            for p, q in zip(chi[0::2], chi[1::2]):
                q = sense * q if len(chi) > 2 else q
                re_now = (A * p * envelope) // w0; im_now = (A * q * envelope) // w0
                re_before = (re_now * num) // self.den - sense * ((im_now * sn) // self.den); im_before = sense * ((re_now * sn) // self.den) + (im_now * num) // self.den
                found += [Line(re_now, re_before, None, self.w), Line(im_now, im_before, None, self.w)]
            return found
        def share_of(A):
            total = 0
            for l in record(A, 1): total = total + self.share(l, r, vacuum=True)
            return int(sum(int(x) for x in total.reshape(-1)))'''),
    ('''        for sense in (-1, 1):  # the conjugate pair laid onto the one plane: at one Node the two senses superpose (the im lines cancel, the record neutral)
            re, im = record(low, sense); self.lay(rec, Ellipsis, (re.now, re.before, im.now, im.before))
        self.log.append({'event': 'lay', 'i': 0, 'node': list(at), 'line_pair': rec, 'width': h, 'quanta': n, 'amplitude': low, 'share': share_of(low), 'unit': self.units[rec], 'nodes': int(sum(1 for x in envelope.reshape(-1) if int(x) > 0))})''',
     '''        for sense in ((-1, 1) if one_sense is None else (int(one_sense),)):  # the conjugate pair laid onto the one row (the im lines cancel, the record neutral); sr2 flag: one sense alone where the lay names it
            self.lay(rec, Ellipsis, [x for l in record(low, sense) for x in (l.now, l.before)])
        entry = {'event': 'lay', 'i': 0, 'node': list(at), 'line_pair': rec, 'width': h, 'quanta': n, 'amplitude': low, 'share': share_of(low), 'unit': self.units[rec], 'nodes': int(sum(1 for x in envelope.reshape(-1) if int(x) > 0))}
        if one_sense is not None or spin is not None: entry.update({'sense': one_sense, 'spin': spin})  # sr2: David's log unchanged where the flags are absent
        self.log.append(entry)'''),
    # 7. the held lines of the potential (sp2's control), set at the start
    ("        self.detectors = [self.node_of(d) for d in world.get('detectors', [])]\n        self.A = rule3.largest_below(action // 2)",
     "        self.detectors = [self.node_of(d) for d in world.get('detectors', [])]\n"
     "        self.held_lines = []  # sr2 (sp2's flag): hand-held lines of the shape-4 row (a control: the magnet), each set here and restored after every act\n"
     "        for h_ in self.control.get('held_potential', []):\n"
     "            k_ = int(h_['line']); at_ = self.node_of(h_['at']); F = Z(self.shape)\n"
     "            def centred(node, a):  # the torus-centred offset along the axis a\n"
     "                d = (node[a] - at_[a]) % self.cube\n"
     "                return d - self.cube if d > self.cube // 2 else d\n"
     "            for node in np.ndindex(*self.shape):\n"
     "                if h_['field'] == 'sg': F[node] = -centred(node, int(h_['across'])) * (int(h_['B0']) + int(h_['b']) * centred(node, int(h_['along'])))  # A_line = -(d_across)(B0 + b d_along): the curl B0 + b d_along along the third axis, its gradient along `along`\n"
     "                elif h_['field'] == 'linear': F[node] = int(h_['E']) * centred(node, int(h_['along']))\n"
     "                else: raise ValueError('a held field of no form: %r' % (h_['field'],))\n"
     "            line_ = self.row(4).lines[k_]; line_.now = F.copy(); line_.before = F.copy(); self.held_lines.append(k_)\n"
     "        self.A = rule3.largest_below(action // 2)"),
    # 8. the arrivals of a row of planes turned pair by pair
    ('''        re_j, im_j = arrivals
        im_j = frames[port] * im_j
        c, s = phases[port]
        _e, (n,), _f = link(port, odd=[odd[axis]])  # the odd line on the Link: the two ends' sum signed by the Port's side (the engine's V_ij = V_a(i) + V_a(j); no division, the mirror exact)
        Wl = 4 * self.gamma; tc, ts, tw = Wl * Wl - n * n, 2 * Wl * n, Wl * Wl + n * n
        a_re = (c * re_j - s * im_j); a_im = (s * re_j + c * im_j)
        a_re, a_im = (2 * a_re + self.X) // (2 * self.X), (2 * a_im + self.X) // (2 * self.X)
        b_re = (tc * a_re - ts * a_im); b_im = (ts * a_re + tc * a_im)
        return [(2 * b_re + tw) // (2 * tw), (2 * b_im + tw) // (2 * tw)]''',
     '''        c, s = phases[port]
        _e, (n,), _f = link(port, odd=[odd[axis]])  # the odd line on the Link: the two ends' sum signed by the Port's side (the engine's V_ij = V_a(i) + V_a(j); no division, the mirror exact)
        Wl = 4 * self.gamma; tc, ts, tw = Wl * Wl - n * n, 2 * Wl * n, Wl * Wl + n * n
        found = []
        for re_j, im_j in zip(arrivals[0::2], arrivals[1::2]):  # sr2: every plane of the row alike (one for shape 2, four for shape 8), the same two roundings per Link per plane
            im_j = frames[port] * im_j
            a_re = (c * re_j - s * im_j); a_im = (s * re_j + c * im_j)
            a_re, a_im = (2 * a_re + self.X) // (2 * self.X), (2 * a_im + self.X) // (2 * self.X)
            b_re = (tc * a_re - ts * a_im); b_im = (ts * a_re + tc * a_im)
            found += [(2 * b_re + tw) // (2 * tw), (2 * b_im + tw) // (2 * tw)]
        return found'''),
    # 9. the Pauli term and the spin reading, before rotate
    ("    def rotate(self, lines, r, turn=None, direction=1, flux=None, starts=None):",
     PAULI + "    def rotate(self, lines, r, turn=None, direction=1, flux=None, starts=None):"),
    # 10. the im lines of a row of planes
    ("        return [len(row) == 2 and k == 1 for row in self.rows() for k in range(len(row))]",
     "        return [len(row) in (2, 8) and k % 2 == 1 for row in self.rows() for k in range(len(row))]  # sr2: every plane's im line, four for the shape-8 row"),
    # 11. the step of the shape-8 row: the planes' turn and the Node term
    ('''            elif r.shape == 2:
                turn = None if r.gap == 0 else (phases, odd, frames)
                if r.gap == 0: numerators = [W - W_start, None]''',
     '''            elif r.shape == 2:
                turn = None if r.gap == 0 else (phases, odd, frames)
                if r.gap == 0: numerators = [W - W_start, None]
            elif r.shape == 8:  # sr2: the spinor row: the four planes turned as a plane's, the Node term from the start levels (the before slot backward: the inverse exact)
                turn = (phases, odd, frames); flux = self.pauli_term([at(l) for l in rows[k]], odd, r.pair[0], c)'''),
    # 12. the held lines restored after the shape-4 row's act, in either direction
    ("            start, levels, out[k] = self.act(rows[k], rule, turn, numerators, direction, flux, *ends(k))\n",
     "            start, levels, out[k] = self.act(rows[k], rule, turn, numerators, direction, flux, *ends(k))\n"
     "            if r.shape == 4 and self.held_lines:  # sr2 (sp2's flag): the held lines of the potential restored to the interval's start (a constant in both directions, the bijection kept); backward the state after the turned Nodes' exchange (`kept`), so a held line's remainder returns to the pre-state's at a turned Node\n"
     "                for kk in self.held_lines: out[k][kk] = (held if direction == 1 else kept)[k][kk].copy()\n"),
    # 13. the readings of a quanta row summed over its planes
    ('''            elif r.shape == 2:  # a plane's readings for the writes after it: its Wronskian before and after the step, its current
                re, im = start; W_start = W_start + wronskian(re, im)
                after = out[k] if direction == 1 else held[k]  # the plane as the step left it
                W = W + wronskian(*after); stepped.append([l.copy() for l in after]); plane_starts.append(start)
                for a, j_a in enumerate(plane_current(re, im, frames)): J[a] = J[a] + j_a''',
     '''            elif r.shape in (2, 8):  # a quanta row's readings for the writes after it: its Wronskian before and after the step, its current, summed over its planes (sr2: four for the shape-8 row)
                W_start = W_start + row_wronskian(start)
                after = out[k] if direction == 1 else held[k]  # the row as the step left it
                W = W + row_wronskian(after); stepped.append([l.copy() for l in after]); plane_starts.append(start)
                for re, im in pairs(start):
                    for a, j_a in enumerate(plane_current(re, im, frames)): J[a] = J[a] + j_a'''),
    # 14. the lay act over every line of the row
    ('''        re, im = self.records()[rec].lines
        for line, now, before in ((re, levels[0], levels[1]), (im, levels[2], levels[3])):''',
     '''        lines = self.records()[rec].lines  # sr2: every line of the row, (now, before) per line in order; a plane's (re_now, re_before, im_now, im_before) as before
        for line, now, before in zip(lines, levels[0::2], levels[1::2]):'''),
    # 15. the births: the children of a quanta row laid in the state along the Link's axis
    ("                A = self.lay_amplitude(s_, at, c, factors, pace); re, im = self.records()[s_].lines; num = self.records()[s_].pair[0]",
     "                axis = next(a for a in range(3) if minus[a] != plus[a])  # sr2: the Link's axis, the one direction at hand\n"
     "                chi = [1, 0] if self.records()[s_].shape == 2 else spin_state(axis)  # sr2: a plane's state (1, 0); a spinor child spin-up along the Link's axis\n"
     "                A = self.lay_amplitude(s_, at, c, factors, pace, sum(x * x for x in chi)); lines_ = self.records()[s_].lines; re, im = lines_[0], lines_[1]; num = self.records()[s_].pair[0]"),
    ('''                for where, sense in ((minus, -1), (plus, 1)):  # the conjugate pair onto the one plane, one child at each end; each lay's momentum booked (the re line's now by A, the im line's before by sense A)
                    for a, d in enumerate(self.momentum_of(re.now, re.before, where, d_now=A, num=num)): dp_lay[a] += d
                    for a, d in enumerate(self.momentum_of(im.now, im.before, where, d_before=sense * A, num=num)): dp_lay[a] += d
                    self.lay(s_, where, (A, 0, 0, sense * A))
                W_children = [int(re.now[w_] * im.before[w_] - im.now[w_] * re.before[w_]) for w_ in (minus, plus)]  # each child's sense is the sign of its own Wronskian at its Node (the owner's word 3)''',
     '''                for where, sense in ((minus, -1), (plus, 1)):  # the conjugate pair onto the one row, one child at each end; each lay's momentum booked (every line's now and before moved; a plane's re now by A, im before by sense A as before)
                    lv = child_levels(A, chi, sense)
                    for l_, (dn, db) in zip(lines_, zip(lv[0::2], lv[1::2])):
                        for a, d in enumerate(self.momentum_of(l_.now, l_.before, where, d_now=dn, d_before=db, num=num)): dp_lay[a] += d
                    self.lay(s_, where, lv)
                W_children = [int(sum(int(re_.now[w_] * im_.before[w_] - im_.now[w_] * re_.before[w_]) for re_, im_ in pairs(lines_))) for w_ in (minus, plus)]  # each child's sense is the sign of its own Wronskian at its Node (the owner's word 3); sr2: summed over the row's planes'''),
    ("'amplitude': A, 'children_at_node': len(children), 'room': room, 'dP_take': dp_take, 'dP_lay': dp_lay})",
     "'amplitude': A, 'children_at_node': len(children), 'room': room, 'dP_take': dp_take, 'dP_lay': dp_lay, **({'chi': chi, 'axis': axis} if len(chi) > 2 else {})})  # sr2: the spinor child's state logged, David's log unchanged"),
    # 16. the lay's amplitude with the state's norm
    ("    def lay_amplitude(self, s_, at, c, factors, pace):",
     "    def lay_amplitude(self, s_, at, c, factors, pace, norm=1):"),
    ("        C = 2 * D + sum(int(np.asarray(x)[at]) for x in r.reaches)\n",
     "        C = (2 * D + sum(int(np.asarray(x)[at]) for x in r.reaches)) * norm  # sr2: the state's norm (the sum of its weights' squares) multiplies the share; 1 for a plane\n"),
    # 17. the standing share summed over the row's lines
    ('''            rr = self.rule_of(r, c, factors); re0, im0 = plane_starts[rec]
            owns.append(self.share(re0, rr, pace, vacuum=True) + self.share(im0, rr, pace, vacuum=True))''',
     '''            rr = self.rule_of(r, c, factors); total = 0  # sr2: the row's share summed over its lines (two for a plane, eight for the spinor row)
            for l0 in plane_starts[rec]: total = total + self.share(l0, rr, pace, vacuum=True)
            owns.append(total)'''),
    # 18. the credit of a quanta row: the first plane's frame, the row's Wronskian, the spin bilinears for shape 8
    ('''        re, im = self.records()[rec].lines; re0, im0 = plane_starts[rec]
        nodes = self.frame_nodes(at)[1:]
        W = int(re.now[at] * im.before[at] - im.now[at] * re.before[at])
        sre, sim = self.stepped[rec]''',
     '''        lines_ = self.records()[rec].lines; re, im = lines_[0], lines_[1]; re0, im0 = plane_starts[rec][0], plane_starts[rec][1]  # sr2: the first plane's frame as before; W summed over the row's planes
        nodes = self.frame_nodes(at)[1:]
        W = int(sum(int(re_.now[at] * im_.before[at] - im_.now[at] * re_.before[at]) for re_, im_ in pairs(lines_)))
        sre, sim = self.stepped[rec][0], self.stepped[rec][1]'''),
    ("'light_now_was': light_was, 'dP_take': self.last_dp, 'sign_level': int(self.row(4).lines[0].now[at]), 'turned': bool(self.turned[at])}",
     "'light_now_was': light_was, 'dP_take': self.last_dp, 'sign_level': int(self.row(4).lines[0].now[at]), 'turned': bool(self.turned[at]), **({'spin': self.spin_at(lines_, at), 'spin_start': self.spin_at(plane_starts[rec], at)} if len(lines_) == 8 else {})}  # sr2: the spinor row's bilinears on its credit (the decoder's read of the component); David's credits unchanged"),
    # 19. the unclick of a child from its logged state
    ("                self.lay(s_, tuple(entry['minus']), (A, 0, 0, -A), -1); self.lay(s_, tuple(entry['plus']), (A, 0, 0, A), -1)",
     "                chi = entry.get('chi', [1, 0])  # sr2: the child's state as logged (a plane's (1, 0))\n"
     "                self.lay(s_, tuple(entry['minus']), child_levels(A, chi, -1), -1); self.lay(s_, tuple(entry['plus']), child_levels(A, chi, 1), -1)"),
    # 20. the reader over quanta rows of any shape
    ('''    for rec, (re, im) in enumerate(planes):''',
     '''    for rec, lines_ in enumerate(planes):  # sr2: a quanta row of any shape; the weight the sum of its lines' squares
        re, im = lines_[0], lines_[1]'''),
    ("        wgt = re.now * re.now + im.now * im.now; total = int(sum(int(x) for x in wgt.reshape(-1)))",
     "        wgt = 0\n        for l_ in lines_: wgt = wgt + l_.now * l_.now\n        total = int(sum(int(x) for x in wgt.reshape(-1)))"),
    ("    for re, im in planes: W = W + wronskian(re, im)",
     "    for lines_ in planes: W = W + row_wronskian(lines_)  # sr2"),
    ("'W abs sum': int(sum(abs(int(x)) for re, im in planes for x in wronskian(re, im).reshape(-1)))",
     "'W abs sum': int(sum(abs(int(x)) for lines_ in planes for x in row_wronskian(lines_).reshape(-1)))"),
]


def main():
    text = open(SRC).read()
    for old, new in REPLACEMENTS:
        count = text.count(old)
        assert count == 1, ('replacement target found %d times, expected 1: %r' % (count, old[:100]))
        text = text.replace(old, new)
    open(OUT, 'w').write(text)
    print('wrote', OUT, 'with', len(REPLACEMENTS), 'replacements')


if __name__ == '__main__':
    main()
