"""gn1: build the flagged copy lean_generic.py from David's lean_full.py at toys-5 adc2049 (the file untouched; this script writes a new file beside it).
Every replacement names its old text exactly once. With both flags at their default the copy runs David's path bit for bit (checked by the record's counts, log and state hash).
Flags (environment): GN1_READ = david | quanta | all_start (the digit set of the one-Link read); GN1_CLOSE = david | all (the shape-1 row of gap 0 closes as a record does)."""
import os, sys
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, 'toy_adc2049', 'lean_full.py')).read()


def once(text, old, new):
    n = text.count(old)
    if n != 1: raise SystemExit('old text found %d times: %r' % (n, old[:80]))
    return text.replace(old, new)


# the path to src from tools/derivations/gn1 (three steps up, not four)
src = once(src, "'..', '..', '..', '..', 'src'))  # tools/derivations/toys/lean -> src", "'..', '..', '..', 'src'))  # tools/derivations/gn1 -> src (gn1's flagged copy)")

# the flags
src = once(src, "WIDTH = 128  # the law's one constant: every integer of the state and of every act's transient within 128 bits\n",
           "WIDTH = 128  # the law's one constant: every integer of the state and of every act's transient within 128 bits\n"
           "GN1_READ = os.environ.get('GN1_READ', 'david')  # gn1's flag: david = the toy's digit set bit for bit; quanta = every line of every row of shape 1 or 2 with a pair, at the start; all_start = every line of every row, at the start\n"
           "GN1_CLOSE = os.environ.get('GN1_CLOSE', 'david')  # gn1's flag: david = the shape-2 records close; all = the shape-1 row of gap 0 closes too, at its unit W_c, the take from its own line\n")

# the start's rows kept for the read (the pre-state copies, already made)
src = once(src, "        held = [[l.copy() for l in row] for row in self.rows()]  # the state at this end of the interval: the pre-state forward, the post-state backward\n",
           "        held = [[l.copy() for l in row] for row in self.rows()]  # the state at this end of the interval: the pre-state forward, the post-state backward\n"
           "        if direction == 1: self.start_rows = held  # gn1: the start's lines of every row, for the read under the flag\n")

# the digit set
src = once(src, "        rules = [(light_start, r_light)] + [(r.lines[0], self.rule_of(r, c, factors)) for r in (self.row(4), self.row(10))]\n"
           "        for rec, r in enumerate(self.records()):\n"
           "            rules += [(l, self.rule_of(r, c, factors)) for l in plane_starts[rec]]\n",
           "        if GN1_READ == 'david':\n"
           "            rules = [(light_start, r_light)] + [(r.lines[0], self.rule_of(r, c, factors)) for r in (self.row(4), self.row(10))]\n"
           "            for rec, r in enumerate(self.records()):\n"
           "                rules += [(l, self.rule_of(r, c, factors)) for l in plane_starts[rec]]\n"
           "        elif GN1_READ == 'quanta':  # gn1: every line of every row of quanta (shape 1 or 2 with a pair) at the start, ALGEBRA.md The click writes on the lattice (every line of every record of quanta)\n"
           "            rules = [(l, self.rule_of(r, c, factors)) for r, lines in zip(self.rows_, self.start_rows) for l in lines if r.wall is None and r.shape in (1, 2)]\n"
           "        else:  # gn1: every line of every row at the start, the holders and the walled row included\n"
           "            rules = [(l, self.rule_of(r, c, factors)) for r, lines in zip(self.rows_, self.start_rows) for l in lines]\n")

# the close of the shape-1 row of gap 0 as a record's
src = once(src, "        self.proper = Z(S); self.closes = Z(S)\n",
           "        self.proper = Z(S); self.closes = Z(S)\n"
           "        self.standing_z, self.crossed_z, self.beats_z = Z(S), Z(S), Z(S)  # gn1: the shape-1 row's counters under GN1_CLOSE = all (three integers more per Node)\n")
src = once(src, "                self.log.append(self.credit(rec, at, plane_starts, fall, levels, now))\n",
           "                self.log.append(self.credit(rec, at, plane_starts, fall, levels, now))\n"
           "        if GN1_CLOSE == 'all':  # gn1: the same close on the shape-1 row of gap 0, its unit W_c, the take from its own line\n"
           "            z = self.row(1, gap=0).lines[0]; sh = self.share(light_start, r_light, vacuum=True)\n"
           "            standing_now = np.vectorize(lambda v: 1 if int(v) >= self.unit_light else 0, otypes=[object])(sh)\n"
           "            self.standing_z = np.where(standing_now == 1, self.standing_z + 1, 0)\n"
           "            upward = np.vectorize(lambda b, n: 1 if (int(b) < 0 <= int(n)) else 0, otypes=[object])(z.before, z.now)\n"
           "            counting = np.vectorize(lambda v: 1 if int(v) > 0 else 0, otypes=[object])(self.crossed_z)\n"
           "            self.beats_z = np.where((upward == 1) & (counting == 1), self.crossed_z, self.beats_z)\n"
           "            self.crossed_z = np.where(upward == 1, 1, np.where(counting == 1, self.crossed_z + 1, 0))\n"
           "            closing = np.vectorize(lambda st, bt: 1 if (int(bt) > 0 and int(st) >= int(bt)) else 0, otypes=[object])(self.standing_z, self.beats_z)\n"
           "            self.counts['z_standing_nodes'] = self.counts.get('z_standing_nodes', 0) + int(standing_now.sum()); self.counts['z_upward'] = self.counts.get('z_upward', 0) + int(upward.sum())\n"
           "            for at in zip(*np.nonzero(closing == 1)):\n"
           "                at = tuple(int(x) for x in at)\n"
           "                if at in born_nodes or frozen[at]: continue\n"
           "                got = self.take_at(at, self.unit_light, r_light, 1)\n"
           "                self.standing_z[at] = 0\n"
           "                if got is None: continue\n"
           "                levels, fall, now = got\n"
           "                self.counts['light_credits'] += 1\n"
           "                self.log.append({'event': 'light', 'i': self.interval, 'node': list(at), 'quanta': 1, 'proper': int(self.proper[at]), 'content': int(self.start_content[at]), 'beat': int(self.beats_z[at]), 'taken': fall, 'levels': levels, 'light_now_was': now})\n")
src = once(src, "        counters = ([a.copy() for a in self.standing], [a.copy() for a in self.crossed], [a.copy() for a in self.beats])\n",
           "        counters = ([a.copy() for a in self.standing], [a.copy() for a in self.crossed], [a.copy() for a in self.beats]) + ((self.standing_z.copy(), self.crossed_z.copy(), self.beats_z.copy()) if GN1_CLOSE == 'all' else ())\n")
src = once(src, "            elif entry['event'] == 'credit':\n"
           "                z.now[at] = entry['light_now_was']; self.closes[at] -= 1\n"
           "        del self.log[frame['log_from']:]\n"
           "        self.standing, self.crossed, self.beats = frame['counters']\n",
           "            elif entry['event'] == 'credit' or (entry['event'] == 'light' and 'light_now_was' in entry):\n"
           "                z.now[at] = entry['light_now_was']; self.closes[at] -= 1\n"
           "        del self.log[frame['log_from']:]\n"
           "        self.standing, self.crossed, self.beats = frame['counters'][:3]\n"
           "        if GN1_CLOSE == 'all': self.standing_z, self.crossed_z, self.beats_z = frame['counters'][3:]\n")

# the one-Link read's lattice of a rule whose reaches are plain integers (the walled row: no Links, the reaches 0): the same values for an array
src = once(src, "            F0 = math.gcd(self.w, int(r.mass[at]) if np.ndim(r.mass) else int(r.mass), *[int(np.asarray(x)[at]) for x in r.reaches])\n"
           "            for k, n in enumerate(nodes):\n"
           "                F = F0 if k == 0 else math.gcd(self.w, int(np.asarray(r.reaches[k - 1])[n]))\n",
           "            F0 = math.gcd(self.w, int(r.mass[at]) if np.ndim(r.mass) else int(r.mass), *[int(np.asarray(x)[at]) if np.ndim(x) else int(x) for x in r.reaches])  # gn1: a plain reach (the walled row's 0) read as it is\n"
           "            for k, n in enumerate(nodes):\n"
           "                F = F0 if k == 0 else math.gcd(self.w, int(np.asarray(r.reaches[k - 1])[n]) if np.ndim(r.reaches[k - 1]) else int(r.reaches[k - 1]))\n")

out = os.path.join(here, 'lean_generic.py')
open(out, 'w').write(src)
print('written', out, len(src.splitlines()), 'lines')
