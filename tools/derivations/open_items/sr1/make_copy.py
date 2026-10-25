"""sr1: makes the flagged COPY lean_sr1.py of David's toy (toy/lean_full.py, never edited in place).

Every change is a replacement listed below, each asserted to occur exactly once in the toy's text, so the copy's departure
from the toy is this file and nothing else. The flags (universe/world keys absent in David's files, so his worlds run bit
for bit through the copy):
  - a row {"shape": 8, "pair": [num, den]} in the universe file: the spinor row, a quanta row of 8 lines (4 planes re, im
    under J), its unit 3 T s from its pair as every quanta row's, stepped by Rule3 line by line, its arrivals turned by the
    Link's pair and the odd tangent as a plane's and then by the Port's spinor turn (control.spinor_turn: none | half | quarter,
    the integer matrices derived by sr1_algebra.py, read from out/sr1_matrices.json), its Pauli term (control.pauli: true)
    SUM_j R_j (Phi . Gamma) now in the numerator with the row's wall 12 Gamma w carrying the 1 / (2 Gamma); its share, form,
    charge, current and spin bilinears weighted by the row's Gram matrix G (derived); its credit line carrying the spin density;
  - the `at` lay takes `sense` (1 or -1, one record alone) and `spin` (a named derived vector 'spin_up_z' / 'spin_down_z' or 8 integers);
  - control.held_potential (sp2's form): hand-held lines of the shape-4 row set at the start and restored after every act in
    either direction (the magnet as a control, no lay of the law).
Integers only.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'toy', 'lean_full.py')
OUT = os.path.join(HERE, 'lean_sr1.py')

R = []
R.append(('"""David\'s local lean Node, complete',
          '"""sr1 flagged copy of tools/derivations/sr1/toy/lean_full.py (made by make_copy.py; the flags: the shape-8 row, control.spinor_turn, control.pauli, the `at` lay\'s `sense` and `spin`, control.held_potential). David\'s local lean Node, complete'))
R.append(("os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'src'))  # tools/derivations/toys/lean -> src",
          "os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'src'))  # tools/derivations/sr1 -> src (the copy's place)"))
R.append(("Z = lambda shape: np.zeros(shape, dtype=object)\n",
          "Z = lambda shape: np.zeros(shape, dtype=object)\n"
          "SR1 = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'sr1_matrices.json')))  # sr1 flag: the spinor row's matrices, derived by sr1_algebra.py (the group's 48, Gamma_a, J, G, K0, the Port turns), typed nowhere\n"
          "def matvec8(M, xs):\n"
          "    \"\"\"sr1: an integer 8 x 8 matrix on 8 arrays, exact.\"\"\"\n"
          "    return [sum(M[r][c] * xs[c] for c in range(8) if M[r][c]) for r in range(8)]\n"
          "def gform8(G, xs, ys):\n"
          "    \"\"\"sr1: the bilinear form SUM_rc G_rc x_r y_c on 8 arrays, exact.\"\"\"\n"
          "    found = 0\n"
          "    for r in range(8):\n"
          "        for c in range(8):\n"
          "            if G[r][c]: found = found + G[r][c] * xs[r] * ys[c]\n"
          "    return found\n"))
R.append(("            return [Line(Z(S), Z(S), Z(S) + self.w // 2, self.w, None if ww is None else Z(S) + ww // 2, ww) for ww in wwalls]",
          "            wall_ = self.w * 12 * gamma if shape_ == 8 else self.w  # sr1 flag: the shape-8 row's wall carries the Pauli term's 12 Gamma (the one division exact)\n"
          "            return [Line(Z(S), Z(S), Z(S) + wall_ // 2, wall_, None if ww is None else Z(S) + ww // 2, ww) for ww in wwalls]"))
R.append(("        order = lambda r: 0 if r.wall is not None else {2: 1 + (r.gap == 0), 4: 3, 10: 4}.get(r.shape, 5)",
          "        order = lambda r: 0 if r.wall is not None else {2: 1 + (r.gap == 0), 8: 1, 4: 3, 10: 4}.get(r.shape, 5)  # sr1 flag: the shape-8 row acts with the planes with a gap"))
R.append(("        return [r for r in self.rows_ if r.shape == 2]\n",
          "        return [r for r in self.rows_ if r.shape in (2, 8)]  # sr1 flag: the shape-8 quanta row is a record too\n\n"
          "    def planes(self):\n"
          "        \"\"\"sr1: the shape-2 rows alone, the draw's list (a birth lays a conjugate pair onto a plane; a shape-8 child's spin state is not derived here, so the draw names planes alone).\"\"\"\n"
          "        return [r for r in self.rows_ if r.shape == 2]\n"))
R.append(("        return rule3.Rule(tuple(0 for _ in AXES), 2 * r.wall, r.wall, 0) if r.wall is not None else self.rule(r.pair, c, factors)",
          "        if r.wall is not None: return rule3.Rule(tuple(0 for _ in AXES), 2 * r.wall, r.wall, 0)\n"
          "        ru = self.rule(r.pair, c, factors)\n"
          "        if r.shape == 8: return rule3.Rule(tuple(12 * self.gamma * x for x in ru.reaches), 12 * self.gamma * ru.self_coefficient, 12 * self.gamma * ru.wall, 12 * self.gamma * ru.mass)  # sr1 flag: the row's line scaled by 12 Gamma so that the Pauli term SUM_j R_j (Phi . Gamma) now enters as an integer\n"
          "        return ru"))
# the lay
R.append(("            if r_ is not None and r_.shape != 2: raise ValueError('a lay is onto a plane (shape 2)')",
          "            if r_ is not None and r_.shape not in (2, 8): raise ValueError('a lay is onto a quanta row (shape 2 or 8)')  # sr1 flag"))
R.append(("                else: packets.append((self.records().index(r_), at, int(lay.get('width', 0)), n))",
          "                else: packets.append((self.records().index(r_), at, int(lay.get('width', 0)), n, lay.get('sense'), lay.get('spin', 'spin_up_z')))  # sr1 flag: `sense` lays one record alone; `spin` names the spinor's vector"))
R.append(("        for s_, at, h, n in packets: self.lay_packet(s_, at, h, n)",
          "        for s_, at, h, n, sn_, sp_ in packets: self.lay_packet(s_, at, h, n, sn_, sp_)"))
R.append(("    def lay_packet(self, rec, at, h, n):",
          "    def lay_packet(self, rec, at, h, n, one_sense=None, one_spin='spin_up_z'):"))
R.append(("        def record(A, sense):\n"
          "            re_now = (A * envelope) // w0\n"
          "            return Line(re_now, (re_now * num) // self.den, None, self.w), Line(Z(self.shape), sense * ((re_now * sn) // self.den), None, self.w)\n"
          "        def share_of(A):\n"
          "            re, im = record(A, 1)\n",
          "        spin = None if r_.shape != 8 else (SR1[one_spin][0] if isinstance(one_spin, str) else [int(v) for v in one_spin])  # sr1 flag: the spinor's integer vector of the lay\n"
          "        def record(A, sense):\n"
          "            re_now = (A * envelope) // w0\n"
          "            if r_.shape == 8:  # sr1: the 8 lines at the band's rest rotation: now = re_now v, before = (num now + sense s J now) div den, one rounding per line as the plane's lay\n"
          "                nows = [re_now * v for v in spin]; jn = matvec8(SR1['J'], nows)\n"
          "                def odd(x, m):  # the law's odd rounding: the magnitude's floor with the sign after (features/phase.signed_rounded), so the -I lay is the negation and the two senses' lays sum with the J term cancelled exactly\n"
          "                    return np.where(x < 0, -((-x) * m // self.den), x * m // self.den)\n"
          "                return [Line(n_, odd(n_, num) + sense * odd(j_, sn), None, r_.lines[0].wall) for n_, j_ in zip(nows, jn)]\n"
          "            return Line(re_now, (re_now * num) // self.den, None, self.w), Line(Z(self.shape), sense * ((re_now * sn) // self.den), None, self.w)\n"
          "        def share_of(A):\n"
          "            if r_.shape == 8: return int(sum(int(x) for x in self.share8(record(A, 1), self.rule(r_.pair, c, factors), vacuum=True).reshape(-1)))\n"
          "            re, im = record(A, 1)\n"))
R.append(("        for sense in (-1, 1):  # the conjugate pair laid onto the one plane: at one Node the two senses superpose (the im lines cancel, the record neutral)\n"
          "            re, im = record(low, sense); self.lay(rec, Ellipsis, (re.now, re.before, im.now, im.before))",
          "        for sense in ((-1, 1) if one_sense is None else (int(one_sense),)):  # sr1 flag: one sense where the lay names it; else the conjugate pair (the im lines cancel, the record neutral)\n"
          "            lines_ = record(low, sense)\n"
          "            if r_.shape == 8 and self.control.get('exclusion'):  # sr1 flag: the lay's rule per full state (SP-S3): at the lay's Node the standing row's spin density s against the child's: the child laid whole where they oppose (or nothing stands), passing in the books where they agree\n"
          "                W0, s0, _ = self.bilinears8(r_.lines); _, s1, _ = self.bilinears8(lines_)\n"
          "                dot = sum(int(s0[a_][at]) * int(s1[a_][at]) for a_ in range(3))\n"
          "                if dot > 0:\n"
          "                    self.counts['refused_lay'] += 1; self.log.append({'event': 'refused', 'i': 0, 'node': list(at), 'cause': 'state', 'dot': dot, 'standing_spin': [int(x[at]) for x in s0], 'child_spin': [int(x[at]) for x in s1]}); continue\n"
          "            if r_.shape == 8: self.lay8(rec, lines_)\n"
          "            else: re, im = lines_; self.lay(rec, Ellipsis, (re.now, re.before, im.now, im.before))"))
R.append(("        self.log.append({'event': 'lay', 'i': 0, 'node': list(at), 'line_pair': rec, 'width': h, 'quanta': n, 'amplitude': low, 'share': share_of(low), 'unit': self.units[rec], 'nodes': int(sum(1 for x in envelope.reshape(-1) if int(x) > 0))})",
          "        self.log.append({'event': 'lay', 'i': 0, 'node': list(at), 'line_pair': rec, 'width': h, 'quanta': n, 'amplitude': low, 'share': share_of(low), 'unit': self.units[rec], 'nodes': int(sum(1 for x in envelope.reshape(-1) if int(x) > 0)), 'sense': one_sense, 'spin': spin})"))
# the held potential (sp2's control) and the frames of ones
R.append(("        self.detectors = [self.node_of(d) for d in world.get('detectors', [])]\n        self.A = rule3.largest_below(action // 2)",
          "        self.detectors = [self.node_of(d) for d in world.get('detectors', [])]\n"
          "        self.ones_frames = [1] * 6  # sr1: the plane turn of the spinor row's planes reads no frame sign (the row's conjugation is K0, applied before)\n"
          "        self.held_lines = []  # sr1 flag (sp2's form): hand-held lines of the shape-4 row (a control: the magnet), each set here and restored after every act\n"
          "        for h_ in self.control.get('held_potential', []):\n"
          "            k_ = int(h_['line']); at_ = self.node_of(h_['at']); F = Z(self.shape)\n"
          "            def centred(node, a):  # the torus-centred offset along the axis a\n"
          "                d = (node[a] - at_[a]) % self.cube\n"
          "                return d - self.cube if d > self.cube // 2 else d\n"
          "            for node in np.ndindex(*self.shape):\n"
          "                if h_['field'] == 'sg': F[node] = -centred(node, int(h_['across'])) * (int(h_['B0']) + int(h_['b']) * centred(node, int(h_['along'])))  # A_line = -(d_across)(B0 + b d_along): the curl B0 + b d_along along the third axis, its gradient along `along`\n"
          "                elif h_['field'] == 'linear': F[node] = int(h_['E']) * centred(node, int(h_['along']))\n"
          "                elif h_['field'] == 'sg_image': F[node] = int(h_['s_line']) * (-(int(h_['s_across']) * centred(node, int(h_['across'])))) * (int(h_['B0']) + int(h_['b']) * int(h_['s_along']) * centred(node, int(h_['along'])))  # the sg field carried through a signed permutation as a polar vector, A'_a'(g x) = s_a A_a(x)\n"
          "                else: raise ValueError('a held field of no form: %r' % (h_['field'],))\n"
          "            line_ = self.row(4).lines[k_]; line_.now = F.copy(); line_.before = F.copy(); self.held_lines.append(k_)\n"
          "        self.A = rule3.largest_below(action // 2)"))
R.append(("            start, levels, out[k] = self.act(rows[k], rule, turn, numerators, direction, flux, *ends(k))\n",
          "            start, levels, out[k] = self.act(rows[k], rule, turn, numerators, direction, flux, *ends(k))\n"
          "            if r.shape == 4 and self.held_lines:  # sr1 flag (sp2's form): the held lines restored to the interval's start (a constant in both directions, the bijection kept)\n"
          "                for kk in self.held_lines: out[k][kk] = held[k][kk].copy()\n"))
# the methods of the row: lay8, share8, bilinears8, current8, curl_odd, spinor_turn_matrix
R.append(("    def momentum_of(self, line_now, line_before, at, d_now=0, d_before=0, num=1):",
          "    def lay8(self, rec, lines_, sign=1):\n"
          "        \"\"\"sr1: the lay of a shape-8 record's 8 lines over the board (the two levels added; sign -1 takes them back).\"\"\"\n"
          "        for line, l_ in zip(self.records()[rec].lines, lines_):\n"
          "            line.now = line.now + sign * l_.now; line.before = line.before + sign * l_.before\n\n"
          "    def share8(self, lines, r, pace=None, vacuum=False):\n"
          "        \"\"\"sr1: the conserved form's term of a shape-8 row at the Node: the plane's share with the Gram matrix G of the row's invariant form (derived) weighting the lines pairwise, 2 [w N.G.N + w B.G.B - S N.G.B - N.G.(SUM_j R_j B_j)] - SUM_j R_j (B - B_j).G.(N + N_j), over 4 p^2 G^2 (the plane's share is the case G = I); at the unscaled rule.\"\"\"\n"
          "        G = SR1['G']; N = [l.now for l in lines]; B = [l.before for l in lines]\n"
          "        reached = [Z(self.shape) for _ in range(8)]; shared = Z(self.shape)\n"
          "        for port, reach in enumerate(r.reaches):\n"
          "            Bj = [across(b, port) for b in B]; Nj = [across(n, port) for n in N]\n"
          "            reached = [x + reach * bj for x, bj in zip(reached, Bj)]\n"
          "            shared = shared + reach * gform8(G, [b - bj for b, bj in zip(B, Bj)], [n + nj for n, nj in zip(N, Nj)])\n"
          "        found = r.wall * (gform8(G, N, N) + gform8(G, B, B)) - r.self_coefficient * gform8(G, N, B) - gform8(G, N, reached)\n"
          "        found = found + found - shared\n"
          "        pace = paces.link_pace_of(self.gamma, self.start_content) if pace is None else pace\n"
          "        sq = (self.gamma * self.gamma) if vacuum else pace * pace\n"
          "        wall = 4 * sq * self.G * self.G + (sq == 0)\n"
          "        return np.asarray(division_forward(found, wall, 0)[0])\n\n"
          "    def period8(self, lines, standing_now):\n"
          "        \"\"\"sr1: the row's rotation period at the Nodes where it stands: cos omega = N.G.B / N.G.N exactly (a fraction, named), c_0 = 1, c_1 = cos, c_(k+1) = 2 cos c_k - c_(k-1); P the first k >= 2 at which c_k is a maximum (c_k >= c_(k-1) and c_k >= c_(k+1)), the first return; 0 where the row stands at no quantum or the ratio is degenerate.\"\"\"\n"
          "        from fractions import Fraction as Fr_\n"
          "        G = SR1['G']; N = [l.now for l in lines]; B = [l.before for l in lines]\n"
          "        nn = gform8(G, N, N); nb = gform8(G, N, B); found = Z(self.shape)\n"
          "        for at in zip(*np.nonzero(np.asarray(standing_now, dtype=object) == 1)):\n"
          "            at = tuple(int(x) for x in at); d = int(nn[at])\n"
          "            if d == 0: continue\n"
          "            cs = Fr_(int(nb[at]), d)\n"
          "            if cs >= 1 or cs <= -1: continue\n"
          "            c0, c1 = Fr_(1), cs; k = 1\n"
          "            while k < 200:\n"
          "                c2 = 2 * cs * c1 - c0\n"
          "                if k >= 2 and c1 >= c0 and c1 >= c2: found[at] = k; break\n"
          "                c0, c1 = c1, c2; k += 1\n"
          "        return found\n\n"
          "    def gj(self):\n"
          "        G, J = SR1['G'], SR1['J']\n"
          "        return [[sum(G[r][k] * J[k][c] for k in range(8)) for c in range(8)] for r in range(8)]\n\n"
          "    def bilinears8(self, lines):\n"
          "        \"\"\"sr1: the row's bilinears at every Node: the charge W = B.(G J).N (the G-weighted sum of the 4 planes' Wronskians re_now im_before - im_now re_before), the spin density s_a = N.(G Gamma_a).N, the spin Wronskians B.(G J Gamma_a).N.\"\"\"\n"
          "        G = SR1['G']; GJ = self.gj(); N = [l.now for l in lines]; B = [l.before for l in lines]\n"
          "        W = gform8(GJ, B, N)\n"
          "        s = [gform8(G, N, matvec8(SR1['Gamma'][a], N)) for a in 'xyz']\n"
          "        sw = [gform8(GJ, B, matvec8(SR1['Gamma'][a], N)) for a in 'xyz']\n"
          "        return W, s, sw\n\n"
          "    def current8(self, lines):\n"
          "        \"\"\"sr1: the row's sign current on each axis, J_a = dN_a.(G J).N with dN_a the centred difference of the levels now (the plane's re dim - im dre with G = I), the odd lines' source.\"\"\"\n"
          "        GJ = self.gj(); N = [l.now for l in lines]\n"
          "        return [gform8(GJ, [gradient(n, a) for n in N], N) for a in range(3)]\n\n"
          "    def curl_odd(self, odd):\n"
          "        \"\"\"sr1: the one-Link curl of the odd lines at the Node, Phi_a = d_b A_c - d_c A_b, d_b the centred difference through the two Ports of the axis b (the six neighbours' odd lines and nothing further).\"\"\"\n"
          "        return [gradient(odd[(a + 2) % 3], (a + 1) % 3) - gradient(odd[(a + 1) % 3], (a + 2) % 3) for a in range(3)]\n\n"
          "    def spinor_turn_matrix(self, axis, side):\n"
          "        \"\"\"sr1 flag control.spinor_turn: the Port's spinor turn, 'none' (the identity: the row four planes under the turn), 'half' (J Gamma_a, the half turn's lift) or 'quarter' (u_a, the quarter turn's lift); the -a Port the inverse.\"\"\"\n"
          "        kind = self.control.get('spinor_turn', 'none')\n"
          "        if kind == 'none': return None\n"
          "        key = {'half': 'S_half', 'quarter': 'S_quarter'}[kind]\n"
          "        return SR1[key if side == 1 else key + '_inv']['xyz'[axis]]\n\n"
          "    def momentum_of(self, line_now, line_before, at, d_now=0, d_before=0, num=1):"))
# the arrival of the row
R.append(("        if turn is None or len(arrivals) == 1: return arrivals\n        phases, odd, frames = turn; axis, side = AXES[port]\n        re_j, im_j = arrivals",
          "        if turn is None or len(arrivals) == 1: return arrivals\n        phases, odd, frames = turn; axis, side = AXES[port]\n"
          "        if len(arrivals) == 8:  # sr1 flag: the shape-8 row's arrival: the frame's conjugation K0 where the frames differ, its 4 planes turned by the Link's pair and the odd tangent as a plane's (one rounding per Link per line), then the Port's spinor turn (exact, an integer matrix)\n"
          "            xs = list(arrivals); fr = frames[port]\n"
          "            if not isinstance(fr, int) and bool((np.asarray(fr) == -1).any()): xs = [np.where(fr == -1, k_, x_) for k_, x_ in zip(matvec8(SR1['K0'], xs), xs)]\n"
          "            turned = []\n"
          "            for k in range(4): turned += self.turned_arrival([xs[2 * k], xs[2 * k + 1]], port, (phases, odd, self.ones_frames))\n"
          "            S = self.spinor_turn_matrix(axis, side)\n"
          "            return turned if S is None else matvec8(S, turned)\n"
          "        re_j, im_j = arrivals"))
# the Pauli term inside rotate (from the start levels, so the inverse reads the same term)
R.append(("        totals = [r.self_coefficient * a - (r.wall * l.before if direction == 1 else 0) + (0 if flux is None else f) for l, a, f in zip(lines, at, flux or [0] * len(lines))]\n",
          "        totals = [r.self_coefficient * a - (r.wall * l.before if direction == 1 else 0) + (0 if flux is None else f) for l, a, f in zip(lines, at, flux or [0] * len(lines))]\n"
          "        if len(lines) == 8 and turn is not None and self.control.get('pauli'):  # sr1 flag: the Pauli term nu (Phi . Gamma) now in the numerator, nu = R / (2 Gamma) derived from g = 2; with the row's line scaled by 12 Gamma it is SUM_j R_j (Phi . Gamma) now, R_j the unscaled reaches; Phi the one-Link curl of the odd lines at the start; read from the start levels so the inverse reads the same term\n"
          "            phi = self.curl_odd(turn[1]); coef = sum(r.reaches) // (12 * self.gamma)\n"
          "            for a_, ax in enumerate('xyz'):\n"
          "                gx = matvec8(SR1['Gamma'][ax], at)\n"
          "                totals = [t + coef * phi[a_] * g for t, g in zip(totals, gx)]\n"))
# run(): the row's turn, its readings, its form and stress
R.append(("            elif r.shape == 2:\n                turn = None if r.gap == 0 else (phases, odd, frames)\n                if r.gap == 0: numerators = [W - W_start, None]",
          "            elif r.shape == 2:\n                turn = None if r.gap == 0 else (phases, odd, frames)\n                if r.gap == 0: numerators = [W - W_start, None]\n"
          "            elif r.shape == 8: turn = (phases, odd, frames)  # sr1 flag: the spinor row turned as a plane with a gap; its Port turn and Pauli term inside rotate"))
R.append(("            elif r.shape == 2:  # a plane's readings for the writes after it: its Wronskian before and after the step, its current\n",
          "            elif r.shape == 8:  # sr1 flag: the spinor row's readings: its charge W before and after the step, its current, its lines for the click\n"
          "                W_start = W_start + self.bilinears8(start)[0]\n"
          "                after = out[k] if direction == 1 else held[k]\n"
          "                W = W + self.bilinears8(after)[0]; stepped.append([l.copy() for l in after]); plane_starts.append(start)\n"
          "                for a, j_a in enumerate(self.current8(start)): J[a] = J[a] + j_a\n"
          "            elif r.shape == 2:  # a plane's readings for the writes after it: its Wronskian before and after the step, its current\n"))
R.append(("                for l0, lv in zip(start, levels): forms = forms + (l0.now * l0.now - lv * l0.before)",
          "                if r.shape == 8: forms = forms + gform8(SR1['G'], [l0.now for l0 in start], [l0.now for l0 in start]) - gform8(SR1['G'], levels, [l0.before for l0 in start])  # sr1 flag: the row's form G-weighted\n"
          "                else:\n"
          "                    for l0, lv in zip(start, levels): forms = forms + (l0.now * l0.now - lv * l0.before)"))
R.append(("        trace, traceless = tensor_parts(stress_parts([(at(l), r.pair[0]) for r in riding for l in r.lines], self.shape))",
          "        parts_ = stress_parts([(at(l), r.pair[0]) for r in riding if r.shape != 8 for l in r.lines], self.shape)\n"
          "        for r in riding:  # sr1 flag: a shape-8 row's stress G-weighted, SUM_a num d_a N . G . d_a N\n"
          "            if r.shape == 8:\n"
          "                for a in range(3):\n"
          "                    d = [gradient(at(l), a) for l in r.lines]; parts_[a] = parts_[a] + r.pair[0] * gform8(SR1['G'], d, d)\n"
          "        trace, traceless = tensor_parts(parts_)"))
# the close: the draw over the planes alone; the owns of the row; the credit
R.append(("        M = self.unit_gap0 * len(self.records())  # the draw composed modulo the planes' count times the massless unit: the quotient names the plane, over every plane alike",
          "        M = self.unit_gap0 * len(self.planes())  # the draw composed modulo the planes' count times the massless unit: the quotient names the plane, over every plane alike (sr1: the shape-2 rows; a shape-8 child's spin state is not derived here)"))
R.append(("                born.append((into, (number // self.unit_gap0) % len(self.records()), minus, plus, room))",
          "                born.append((into, self.records().index(self.planes()[(number // self.unit_gap0) % len(self.planes())]), minus, plus, room))  # sr1: the plane drawn, as a record index"))
R.append(("            rr = self.rule_of(r, c, factors); re0, im0 = plane_starts[rec]\n",
          "            rr = self.rule_of(r, c, factors)\n"
          "            if r.shape == 8: owns.append(self.share8(plane_starts[rec], self.rule(r.pair, c, factors), pace, vacuum=True)); continue  # sr1 flag: the row's share G-weighted at the unscaled rule\n"
          "            re0, im0 = plane_starts[rec]\n"))
R.append(("            re = self.records()[rec].lines[0]\n            upward = np.vectorize(lambda b, n: 1 if (int(b) < 0 <= int(n)) else 0, otypes=[object])(re.before, re.now)",
          "            re = self.records()[rec].lines[0]\n"
          "            if self.records()[rec].shape == 8:  # sr1 flag: the row's beat is read covariantly, from the invariant ratio cos omega = N.G.B / N.G.N at the Node (no line of a spinor is a scalar under the 48, so no crossing line is covariant; the plane's re crossing is the case of scalar lines): the period P in intervals by Chebyshev's recurrence on the exact ratio, the first return of cos(k omega) to its maximum; the click when the record has stood one period\n"
          "                self.beats[rec] = self.period8(self.records()[rec].lines, standing_now)\n"
          "                closing = np.vectorize(lambda st, bt: 1 if (int(bt) > 0 and int(st) >= int(bt)) else 0, otypes=[object])(self.standing[rec], self.beats[rec])\n"
          "                for at in zip(*np.nonzero(closing == 1)):\n"
          "                    at = tuple(int(x) for x in at)\n"
          "                    if at in born_nodes or frozen[at]: continue\n"
          "                    got = self.take_at(at, self.units[s_], r_gap0, 1)\n"
          "                    self.standing[rec][at] = 0\n"
          "                    if got is None: continue\n"
          "                    levels, fall, now = got\n"
          "                    self.counts['body_clicks'] += 1\n"
          "                    self.log.append(self.credit(rec, at, plane_starts, fall, levels, now))\n"
          "                continue\n"
          "            upward = np.vectorize(lambda b, n: 1 if (int(b) < 0 <= int(n)) else 0, otypes=[object])(re.before, re.now)"))
R.append(("    def credit(self, rec, at, plane_starts, fall, levels, light_was):\n        re, im = self.records()[rec].lines; re0, im0 = plane_starts[rec]",
          "    def credit8(self, rec, at, plane_starts, fall, levels, light_was):\n"
          "        \"\"\"sr1: the credit line of a shape-8 record: the Node, the proper count, the beat, the row's charge W (its sense), its spin density s (the axial vector, signed per axis) and spin Wronskians at the Node, the take.\"\"\"\n"
          "        lines = self.records()[rec].lines\n"
          "        W, s, sw = self.bilinears8(lines)\n"
          "        Wn = int(W[at]); sn_ = [int(x[at]) for x in s]; swn = [int(x[at]) for x in sw]\n"
          "        return {'event': 'credit', 'i': self.interval, 'node': list(at), 'proper': int(self.proper[at]), 'closes': int(self.closes[at]), 'content': int(self.start_content[at]), 'line': rec, 'sense': 1 if Wn > 0 else -1 if Wn < 0 else 0,\n"
          "                'beat': int(self.beats[rec][at]), 'W': Wn, 'spin': sn_, 'spin_sign': [1 if x > 0 else -1 if x < 0 else 0 for x in sn_], 'spin_wronskian': swn, 'levels8': [int(l.now[at]) for l in lines], 'taken': fall, 'levels': levels, 'light_now_was': light_was, 'dP_take': self.last_dp, 'sign_level': int(self.row(4).lines[0].now[at]), 'turned': bool(self.turned[at])}\n\n"
          "    def credit(self, rec, at, plane_starts, fall, levels, light_was):\n"
          "        if self.records()[rec].shape == 8: return self.credit8(rec, at, plane_starts, fall, levels, light_was)  # sr1 flag\n"
          "        re, im = self.records()[rec].lines; re0, im0 = plane_starts[rec]"))
# the swap on the row
R.append(("        for line, h, im in zip(self.all_lines(), [l for row in held for l in row], self.is_im()):\n            sgn = -1 if im else 1",
          "        for row, hrow in zip(self.rows(), held):  # sr1 flag: a shape-8 row exchanged as a whole: the levels exchanged and conjugated by K0 (the lattice's conjugation, derived), every remainder complemented (named open: K0 is no signed permutation; no turn fires in the measured runs)\n"
          "            if len(row) == 8:\n"
          "                kb = matvec8(SR1['K0'], [h.before for h in hrow]); kn = matvec8(SR1['K0'], [h.now for h in hrow])\n"
          "                for line, h, b_, n_ in zip(row, hrow, kb, kn):\n"
          "                    line.now, line.before, line.rem = np.where(top, b_, line.now), np.where(top, n_, line.before), np.where(top, line.wall - 1 - h.rem, line.rem)\n"
          "        eights = [id(l_) for row in self.rows() if len(row) == 8 for l_ in row]\n"
          "        for line, h, im in zip(self.all_lines(), [l for row in held for l in row], self.is_im()):\n"
          "            if id(line) in eights: continue\n"
          "            sgn = -1 if im else 1"))
# the reader
R.append(("    for rec, (re, im) in enumerate(planes):\n        if b.records()[rec].gap == 0: continue  # the reader skips the massless plane (the sea fills the board)\n        wgt = re.now * re.now + im.now * im.now; total = int(sum(int(x) for x in wgt.reshape(-1)))",
          "    for rec, lines_ in enumerate(planes):\n        if b.records()[rec].gap == 0: continue  # the reader skips the massless plane (the sea fills the board)\n"
          "        if len(lines_) == 8: wgt = gform8(SR1['G'], [l.now for l in lines_], [l.now for l in lines_])  # sr1 flag: the row's weight G-weighted\n"
          "        else: re, im = lines_; wgt = re.now * re.now + im.now * im.now\n"
          "        total = int(sum(int(x) for x in wgt.reshape(-1)))"))
R.append(("    for re, im in planes: W = W + wronskian(re, im)",
          "    for lines_ in planes: W = W + (b.bilinears8(lines_)[0] if len(lines_) == 8 else wronskian(*lines_))  # sr1 flag"))
R.append(("'W abs sum': int(sum(abs(int(x)) for re, im in planes for x in wronskian(re, im).reshape(-1)))",
          "'W abs sum': int(sum(abs(int(x)) for lines_ in planes for x in (b.bilinears8(lines_)[0] if len(lines_) == 8 else wronskian(*lines_)).reshape(-1)))"))


def main():
    text = open(SRC).read()
    for old, new in R:
        count = text.count(old)
        assert count == 1, ('replacement target found %d times, expected 1: %r' % (count, old[:90]))
        text = text.replace(old, new)
    open(OUT, 'w').write(text)
    print('wrote', OUT, 'with', len(R), 'replacements')


if __name__ == '__main__':
    main()
