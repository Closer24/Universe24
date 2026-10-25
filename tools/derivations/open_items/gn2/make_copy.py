"""gn2's flagged COPY of David's lean toy (toys-5 at c74322851, the fold's parent, tools/derivations/gn2/toy_former/lean_full.py: the file whose lines the brief names), written by this script and never by hand: flagged/lean_full.py. Every replacement below must match the toy's text exactly once, else the script refuses. Run: python make_copy.py

The flags (environment, read once at import; every one `off` is David's path, the state bit for bit):
  GN2_TURN  off | all | scaled   pick 1 (lines 433, 488): what turns a plane's arrivals
  GN2_EMIT  off | pair           pick 2 (434, 453, 467, 416): the row W-S1 lights, by the pairs
  GN2_CLICK off | generic        pick 3 (554, 618, 624, 637, 649, 727): the meeting over every row at its own unit
  GN2_SEA   off | named          pick 4 (150): the sea of the row named, a gapped row at its own rest
  GN2_ROWS  off | rank           section 2: the carrier and the potential found by rank, the acts' order by rising shape
  pick 5 (136, 554): unit_of(pair) one function, no flag (the same integers by construction).
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'toy_former', 'lean_full.py')
DST_DIR = os.path.join(HERE, 'flagged')
DST = os.path.join(DST_DIR, 'lean_full.py')

text = open(SRC).read()
replacements = []

# 0. the header and the flags
replacements.append((
    '"""David\'s local lean Node, complete (the owner\'s word, 04:4x: run everything, omit nothing).',
    '"""gn2\'s FLAGGED COPY (2026-10-25) of David\'s lean toy (toys-5 at c74322851) for the gap-0 picks and the picks by shape number: make_copy.py names every delta; David\'s file under toy_former/ is untouched; every flag off is David\'s path bit for bit.\nDavid\'s local lean Node, complete (the owner\'s word, 04:4x: run everything, omit nothing).'))
replacements.append((
    "from event_universe.features import volume as volform, phase\n",
    "from event_universe.features import volume as volform, phase\n\nGN2 = {k: os.environ.get('GN2_' + k, 'off') for k in ('TURN', 'EMIT', 'CLICK', 'SEA', 'ROWS')}  # gn2's flags, every one off = David's path\n"))

# 1. section 2: the acts' order under ROWS=rank (the walled row first, the pair rows by rising shape, the gap-0 plane after the gapped planes)
replacements.append((
    "        order = lambda r: 0 if r.wall is not None else {2: 1 + (r.gap == 0), 4: 3, 10: 4}.get(r.shape, 5)\n",
    "        order = (lambda r: 0 if r.wall is not None else {2: 1 + (r.gap == 0), 4: 3, 10: 4}.get(r.shape, 5)) if GN2['ROWS'] == 'off' else (lambda r: (0, 0, 0) if r.wall is not None else (1, r.shape, 1 if r.gap == 0 else 0))  # gn2 ROWS=rank: no number: the walled row first, then the pair rows by rising shape (a row of more lines is written from the rows of fewer), the gap-0 plane after the gapped planes\n"))

# 2. pick 5: the unit one function of the pair
replacements.append((
    "        self.units = [3 * action * (sine_den(r.pair[0], den) if r.gap > 0 else den) for r in self.records()]\n",
    "        self.units = [self.unit_of(r.pair) for r in self.records()]  # gn2 pick 5: one function of the pair\n"))

# 3. the couplings' table and the gapped meetings' count
replacements.append((
    "        self.orbit = [(int(seed_pair[0][0]), int(seed_pair[1][0]))]  # the table of (cos, sin) as plain integers\n",
    "        self.orbit = [(int(seed_pair[0][0]), int(seed_pair[1][0]))]  # the table of (cos, sin) as plain integers\n        self.couplings = {}  # gn2 TURN=scaled: K = omega_0 Gamma per pair, found once on the orbit\n        self.link_counts = None  # gn2: the Links' counts of the interval, for the scaled turn\n"))
replacements.append((
    "'light_credits': 0, 'light_laid': 0, 'light_laid_nodes': 0}\n",
    "'light_credits': 0, 'light_laid': 0, 'light_laid_nodes': 0, 'met_gapped': 0}\n"))

# 4. pick 4: the sea of the row named
replacements.append((
    "                if r_.gap != 0: raise ValueError('a sea is the massless plane\\'s alone: the drift is its double root')\n                z = r_.lines[0]; z.now[:] = z.now + self.drift\n",
    "                if r_.gap != 0 and GN2['SEA'] == 'off': raise ValueError('a sea is the massless plane\\'s alone: the drift is its double root')\n                if r_.gap != 0:  # gn2 pick 4 (SEA=named): the sea of a gapped row is its drift laid at its own band's rest at every Node, both senses: the standing level A = v den div gap per sense (now - before = v at the rest rotation), re_now += 2 A, re_before += 2 (A num div den), the im lines cancelling (the charge 0): the k = 0 mode of the band, an oscillation of the whole board at omega_0, no double root\n                    re_, im_ = r_.lines; A_ = (self.drift * self.den) // r_.gap\n                    re_.now[:] = re_.now + 2 * A_; re_.before[:] = re_.before + 2 * ((A_ * r_.pair[0]) // self.den)\n                else:\n                    z = r_.lines[0]; z.now[:] = z.now + self.drift\n"))

# 5. the finders (section 2, picks 1, 2, 5) after walled()
replacements.append((
    "    def records(self):\n        \"\"\"The shape-2 rows in order: record 2 s + k of the pair s, k = 0 the sense -1 and k = 1 the sense +1 (the file's order).\"\"\"\n        return [r for r in self.rows_ if r.shape == 2]\n",
    "    def records(self):\n        \"\"\"The shape-2 rows in order: record 2 s + k of the pair s, k = 0 the sense -1 and k = 1 the sense +1 (the file's order).\"\"\"\n        return [r for r in self.rows_ if r.shape == 2]\n"
    "\n    def carrier(self):\n        \"\"\"gn2 section 2: the carrier of the wall. off: David's row(10). rank: the pair row with the most lines (the symmetric tensor's ten components), no number.\"\"\"\n        if GN2['ROWS'] == 'off': return self.row(10)\n        return max((r for r in self.rows_ if r.wall is None), key=lambda r: r.shape)\n"
    "\n    def potential(self):\n        \"\"\"gn2 section 2: the potential's row. off: David's row(4). rank: the pair row with the most lines after the carrier (the vector's four components), no number.\"\"\"\n        if GN2['ROWS'] == 'off': return self.row(4)\n        c = self.carrier()\n        return max((r for r in self.rows_ if r.wall is None and r is not c), key=lambda r: r.shape)\n"
    "\n    def unit_of(self, pair):\n        \"\"\"gn2 pick 5: the quantum of a plane as one function of its pair (row 12 of The conventions and the units): 3 T s, s the pair's sine, for a pair with a gap; 3 T den at (den, den) (W_c, the massless case by number: the owner's 1).\"\"\"\n        num, den = pair\n        return 3 * self.T * (sine_den(num, den) if num != den else den)\n"
    "\n    def coupling_of(self, pair):\n        \"\"\"gn2 pick 1 (TURN=scaled): the plane's coupling to the Link's phase, K = omega_0 Gamma in the orbit's counts (Y-S1): the least count m at which the orbit's cosine over X falls to num over den, by comparisons of integers on the one orbit table; 0 at (den, den), a theorem.\"\"\"\n        num, den = pair\n        if num >= den: return 0\n        if num in self.couplings: return self.couplings[num]\n        m = 0\n        while self.pair_angle(m)[0] * den > num * self.X: m += 1\n        self.couplings[num] = m\n        return m\n"
    "\n    def turn_of(self, r, phases, odd, frames):\n        \"\"\"gn2 pick 1: what turns a plane's arrivals. off: David's branch (the plane at the gap 0 turned by nothing, every other plane by the Link's pair and the odd tangent at the coupling 1). all: the branch removed, one turn on every plane alike at the coupling 1. scaled: one turn on every plane alike at the plane's own coupling K = omega_0 Gamma over Gamma (the count and the odd part scaled with one rounding each): K = 0 at (den, den) is the identity with no branch.\"\"\"\n        if GN2['TURN'] == 'off': return None if r.gap == 0 else (phases, odd, frames)\n        if GN2['TURN'] == 'all': return (phases, odd, frames)\n        return (phases, odd, frames, self.coupling_of(r.pair))\n"
    "\n    def emits(self, r, potential):\n        \"\"\"gn2 pick 2: whether a plane's first line takes W-S1 (the planes' Wronskian change). off: David's, the plane at the gap 0. pair: the plane whose pair is the Wronskian-writer's pair (the potential's row), a function of the pairs and no pick by the gap.\"\"\"\n        if GN2['EMIT'] == 'off': return r.gap == 0\n        return r.pair == potential.pair\n"
    "\n    def emitter(self):\n        \"\"\"gn2 pick 2: the plane W-S1 lights, by the pairs (EMIT=pair) or by the gap 0 (off).\"\"\"\n        if GN2['EMIT'] == 'off': return self.row(2, gap=0)\n        return next(r for r in self.records() if r.pair == self.potential().pair)\n"))

# 6. the Links' counts kept for the scaled turn
replacements.append((
    "        found = []\n        for port in range(6):\n            n = K - frames[port] * across(K, port)\n            pairs = np.vectorize(self.pair_angle, otypes=[object, object])(n)\n            found.append((pairs[0], pairs[1]))\n        return found\n",
    "        found = []; counts = []\n        for port in range(6):\n            n = K - frames[port] * across(K, port)\n            pairs = np.vectorize(self.pair_angle, otypes=[object, object])(n)\n            found.append((pairs[0], pairs[1])); counts.append(n)\n        self.link_counts = counts  # gn2: kept for the scaled turn\n        return found\n"))

# 7. pick 1: the turn at the plane's coupling
replacements.append((
    "        if turn is None or len(arrivals) == 1: return arrivals\n        phases, odd, frames = turn; axis, side = AXES[port]\n        re_j, im_j = arrivals\n        im_j = frames[port] * im_j\n        c, s = phases[port]\n        _e, (n,), _f = link(port, odd=[odd[axis]])",
    "        if turn is None or len(arrivals) == 1: return arrivals\n        phases, odd, frames = turn[:3]; axis, side = AXES[port]\n        re_j, im_j = arrivals\n        im_j = frames[port] * im_j\n        c, s = phases[port]\n        _e, (n,), _f = link(port, odd=[odd[axis]])\n        if len(turn) == 4:  # gn2 TURN=scaled: the Link's count and the odd part at the plane's own coupling K over Gamma, one rounding each (K = 0 at the gap 0: the identity)\n            K = turn[3]; scaled = np.vectorize(lambda v: (1 if int(v) >= 0 else -1) * ((2 * abs(int(v)) * K + self.gamma) // (2 * self.gamma)), otypes=[object])\n            pairs = np.vectorize(self.pair_angle, otypes=[object, object])(scaled(self.link_counts[port])); c, s = pairs[0], pairs[1]; n = scaled(n)"))

# 8. run(): the rows by their finders; the turn and W-S1 by the finders
replacements.append((
    "        metric, walled, potential, massless, records = self.row(10), self.walled(), self.row(4), self.row(2, gap=0), self.records()\n",
    "        metric, walled, potential, massless, records = self.carrier(), self.walled(), self.potential(), self.emitter(), self.records()  # gn2: the rows by what they are (the finders), not by their numbers\n"))
replacements.append((
    "                turn = None if r.gap == 0 else (phases, odd, frames)\n                if r.gap == 0: numerators = [W - W_start, None]\n",
    "                turn = self.turn_of(r, phases, odd, frames)  # gn2 pick 1\n                if self.emits(r, potential): numerators = [W - W_start, None]  # gn2 pick 2\n"))
replacements.append((
    "                if r.gap == 0 and direction == 1:  # the emission's size, a reading of the run: the levels laid on the massless line and the Nodes they were laid at\n",
    "                if self.emits(r, potential) and direction == 1:  # the emission's size, a reading of the run: the levels laid on the massless line and the Nodes they were laid at (gn2 pick 2)\n"))

# 9. ride(): the same finders
replacements.append((
    "        carrier, potential, walled, massless = self.row(10), self.row(4), self.walled(), self.row(2, gap=0)\n",
    "        carrier, potential, walled, massless = self.carrier(), self.potential(), self.walled(), self.emitter()  # gn2: the finders\n"))
replacements.append((
    "            rule = self.rule_of(r, c, factors); turn = None if r.shape != 2 or r.gap == 0 else (phases, odd, frames)\n",
    "            rule = self.rule_of(r, c, factors); turn = None if r.shape != 2 else self.turn_of(r, phases, odd, frames)  # gn2 pick 1\n"))
replacements.append((
    "                if r.wall is None and r.shape != 10:\n",
    "                if r.wall is None and r is not self.carrier():\n"))

# 10. pick 5 / pick 3: the draw's modulus the taken row's unit times the count
replacements.append((
    "    def read_number(self, at, rules):\n",
    "    def read_number(self, at, rules, unit=None):\n"))
replacements.append((
    "        M = self.unit_gap0 * len(self.records())  # the draw composed modulo the planes' count times the massless unit: the quotient names the plane, over every plane alike\n",
    "        M = (self.unit_gap0 if unit is None else unit) * len(self.records())  # the draw composed modulo the planes' count times the TAKEN row's unit (gn2 pick 5): the quotient names the plane, over every plane alike\n"))

# 11. pick 3: the take from the taken row
replacements.append((
    "    def take_at(self, at, walls, r_gap0, cause):\n",
    "    def take_at(self, at, walls, r_gap0, cause, rec=None):\n"))
replacements.append((
    "        z = self.row(2, gap=0).lines[0]\n        levels, fall = self.take(at, walls, r_gap0, z)\n",
    "        z = (self.row(2, gap=0) if rec is None else self.records()[rec]).lines[0]  # gn2 pick 3: the taken row's first line (the gap-0 row where none is named: the bodies' closing)\n        levels, fall = self.take(at, walls, r_gap0, z)\n"))
replacements.append((
    "        self.last_dp = self.momentum_of(z.now, z.before, at, d_now=toward * levels, num=self.row(2, gap=0).pair[0])  # the take's momentum, booked on the click's line (N-S3's reading)\n",
    "        self.last_dp = self.momentum_of(z.now, z.before, at, d_now=toward * levels, num=(self.row(2, gap=0) if rec is None else self.records()[rec]).pair[0])  # the take's momentum, booked on the click's line (N-S3's reading); gn2: the taken row's num\n"))

# 12. pick 3: the meeting of any row at its own unit
replacements.append((
    "    def meet(self, gap0_start, sh, rules, frozen):\n",
    "    def meet(self, gap0_start, sh, rules, frozen, rec=None, unit=None):\n"))
replacements.append((
    "        born = []\n        taken = gap0_start[0]  # the row the click takes: the massless plane's first line; its current orients the Link, its twist gives the handedness\n",
    "        born = []; unit = self.unit_gap0 if unit is None else unit  # gn2 pick 3: the taken row's unit\n        taken = gap0_start[0]  # the row the click takes: the row whose quanta meet (David's: the massless plane's first line); its current orients the Link, its twist gives the handedness\n"))
replacements.append((
    "                if frozen[j] or int(sh[at]) < self.unit_gap0 or int(sh[j]) < self.unit_gap0: continue\n",
    "                if frozen[j] or int(sh[at]) < unit or int(sh[j]) < unit: continue\n                if rec is not None and self.records()[rec].gap != 0:  # gn2 pick 3: two whole quanta of a gapped row meeting: the children by the exact list of its pair (none built here): refused by name `list`, counted, the first 20 logged\n                    self.counts['met_gapped'] += 1\n                    if self.counts['met_gapped'] <= 20: self.log.append({'event': 'refused', 'i': self.interval, 'node': list(at), 'cause': 'list', 'link': list(j), 'row': rec, 'share': [int(sh[at]), int(sh[j])], 'unit': unit})\n                    continue\n"))
replacements.append((
    "                drawn = self.read_number(into, rules)\n                if drawn is None: continue\n                number, room = drawn\n                born.append((into, (number // self.unit_gap0) % len(self.records()), minus, plus, room))  # the plane drawn, over every plane alike (the massless plane among them); the take at the current's end\n",
    "                drawn = self.read_number(into, rules, unit)\n                if drawn is None: continue\n                number, room = drawn\n                born.append((into, (number // unit) % len(self.records()), minus, plus, room, rec))  # the plane drawn, over every plane alike (the massless plane among them); the take at the current's end; gn2: the taken row carried\n"))

# 13. pick 3: refuse and births carry the taken row
replacements.append((
    "        for at, s_, minus, plus, room in born:\n            if int(owns[s_][minus]) > 0 or int(owns[s_][plus]) > 0:\n",
    "        for at, s_, minus, plus, room, rec in born:\n            if int(owns[s_][minus]) > 0 or int(owns[s_][plus]) > 0:\n"))
replacements.append((
    "            kept.append((at, s_, minus, plus, room))\n        landing = {}\n        for at, s_, minus, plus, room in kept:\n",
    "            kept.append((at, s_, minus, plus, room, rec))\n        landing = {}\n        for at, s_, minus, plus, room, rec in kept:\n"))
replacements.append((
    "        for at, s_, minus, plus, room in crowded:\n",
    "        for at, s_, minus, plus, room, rec in crowded:\n"))
replacements.append((
    "        by_node = {}\n        for at, s_, minus, plus, room in kept: by_node.setdefault(at, []).append((s_, minus, plus, room))\n        taken = []\n        for at in sorted(by_node):\n            children = by_node[at]; walls = sum(2 * self.units[s_] for s_, _m, _p, _r in children)\n            got = self.take_at(at, walls, r_gap0, len(children))\n            if got is not None: taken.append((at, children, walls, got))\n        for at, children, walls, (levels, fall, now) in taken:\n",
    "        by_node = {}\n        for at, s_, minus, plus, room, rec in kept: by_node.setdefault((at, rec), []).append((s_, minus, plus, room))\n        taken = []\n        for at, rec in sorted(by_node, key=lambda k_: (k_[0], -1 if k_[1] is None else k_[1])):\n            children = by_node[(at, rec)]; walls = sum(2 * self.units[s_] for s_, _m, _p, _r in children)\n            got = self.take_at(at, walls, r_gap0 if rec is None else self.rules_at[rec], len(children), rec)  # gn2 pick 3: the take from the taken row at its rule\n            if got is not None: taken.append((at, children, walls, got, rec))\n        for at, children, walls, (levels, fall, now), rec in taken:\n"))
replacements.append((
    "'children_at_node': len(children), 'room': room, 'dP_take': dp_take, 'dP_lay': dp_lay})\n",
    "'children_at_node': len(children), 'room': room, 'dP_take': dp_take, 'dP_lay': dp_lay, **({'taken_row': rec} if rec is not None and self.records()[rec].gap != 0 else {})})\n"))
replacements.append((
    "        return {at for at, _c, _w, _g in taken} | {m for _a, ch, _w, _g in taken for _s, m, _p, _r in ch} | {p_ for _a, ch, _w, _g in taken for _s, _m, p_, _r in ch}\n",
    "        return {at for at, _c, _w, _g, _rec in taken} | {m for _a, ch, _w, _g, _rec in taken for _s, m, _p, _r in ch} | {p_ for _a, ch, _w, _g, _rec in taken for _s, _m, p_, _r in ch}\n"))

# 14. pick 3: the click's meeting over every row
replacements.append((
    "        owns = []  # every plane's standing share at the interval's start at the vacuum's weight (V-D, the owner's sentence 7): the meeting's threshold on the massless plane, the lay's refusal on the lift's\n        for rec, r in enumerate(self.records()):\n            rr = self.rule_of(r, c, factors); re0, im0 = plane_starts[rec]\n",
    "        owns = []; self.rules_at = []  # every plane's standing share at the interval's start at the vacuum's weight (V-D, the owner's sentence 7): the meeting's threshold on the massless plane, the lay's refusal on the lift's; gn2: every record's rule kept for the take\n        for rec, r in enumerate(self.records()):\n            rr = self.rule_of(r, c, factors); re0, im0 = plane_starts[rec]; self.rules_at.append(rr)\n"))
replacements.append((
    "        born_nodes = self.births(self.refuse(self.meet(gap0_start, sh, rules, frozen), owns), r_gap0, c, factors, pace)\n",
    "        if GN2['CLICK'] == 'off': born = self.meet(gap0_start, sh, rules, frozen)\n        else:  # gn2 pick 3 (CLICK=generic): the meeting over every row alike, each at its own unit; the taken row is the row whose quanta meet\n            born = []\n            for rec_, _r in enumerate(self.records()): born += self.meet(plane_starts[rec_], owns[rec_], rules, frozen, rec_, self.units[rec_])\n        born_nodes = self.births(self.refuse(born, owns), r_gap0, c, factors, pace)\n"))

# 15. unclick: the taken row's line restored
replacements.append((
    "                self.lay(s_, tuple(entry['minus']), (A, 0, 0, -A), -1); self.lay(s_, tuple(entry['plus']), (A, 0, 0, A), -1)\n                z.now[at] = entry['light_now_was']; self.closes[at] -= 1\n",
    "                self.lay(s_, tuple(entry['minus']), (A, 0, 0, -A), -1); self.lay(s_, tuple(entry['plus']), (A, 0, 0, A), -1)\n                zz = z if 'taken_row' not in entry else self.records()[entry['taken_row']].lines[0]  # gn2 pick 3\n                zz.now[at] = entry['light_now_was']; self.closes[at] -= 1\n"))

# 16. the credit's sign level and the reader's rows by the finders
replacements.append((
    "'sign_level': int(self.row(4).lines[0].now[at]), 'turned': bool(self.turned[at])}\n",
    "'sign_level': int(self.potential().lines[0].now[at]), 'turned': bool(self.turned[at])}\n"))
replacements.append((
    "    metric, potential, massless, planes = b.row(10), b.row(4), b.row(2, gap=0).lines[0], [r.lines for r in b.records()]\n",
    "    metric, potential, massless, planes = b.carrier(), b.potential(), b.emitter().lines[0], [r.lines for r in b.records()]\n"))

for old, new in replacements:
    n = text.count(old)
    if n != 1:
        sys.exit('refused: the text below matches %d times, not once:\n%s' % (n, old[:300]))
    text = text.replace(old, new)

# 17. every remaining pick of the carrier and the potential by number -> the finders (section 2); the count asserted
for old, new, want in (('self.row(10)', 'self.carrier()', 11), ('self.row(4)', 'self.potential()', 3)):
    n = text.count(old)
    if n != want:
        sys.exit('refused: %s found %d times, expected %d' % (old, n, want))
    text = text.replace(old, new)
# the finders' own bodies must keep the numbers (the off path): put them back there
text = text.replace("        if GN2['ROWS'] == 'off': return self.carrier()\n        return max((r for r in self.rows_ if r.wall is None), key=lambda r: r.shape)", "        if GN2['ROWS'] == 'off': return self.row(10)\n        return max((r for r in self.rows_ if r.wall is None), key=lambda r: r.shape)")
text = text.replace("        if GN2['ROWS'] == 'off': return self.potential()\n        c = self.carrier()", "        if GN2['ROWS'] == 'off': return self.row(4)\n        c = self.carrier()")
assert text.count('self.row(10)') == 1 and text.count('self.row(4)') == 1, 'the finders alone hold the numbers'

os.makedirs(DST_DIR, exist_ok=True)
open(DST, 'w').write(text)
print('written', DST, len(replacements) + 2, 'replacements;', 'self.row(2, gap=0) left:', text.count('row(2, gap=0)'))
