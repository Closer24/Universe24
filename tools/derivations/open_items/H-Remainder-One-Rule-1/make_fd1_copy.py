"""fd1's flagged COPY of David's lean toy (tools/derivations/open_items/H-Remainder-One-Rule-1/toy/lean_full.py at c74322851, md5 b2959da3d37bc96dc0625b956a9eb240), written by this script and never by hand:
the copy is lean_full.py with ONE bilinear in place of the eight places that write a_now b_before - b_now a_before, and the take, the undo and the seed's drift lays routed through the one lay act; nothing else moves.
The flag: the world file's key control.fd1 = "unify"; off the flag every line of David's path stands as he wrote it (the copy holds both, the state hash shows them equal).
Every replacement below must match the toy's text exactly once, else the script refuses. Run: python make_fd1_copy.py  (writes toy_fd1/lean_full.py beside it, the same depth as David's toy so the src path stands)."""
import os, sys, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'toy', 'lean_full.py')
DST_DIR = os.path.join(HERE, 'toy_fd1')
DST = os.path.join(DST_DIR, 'lean_full.py')
os.makedirs(DST_DIR, exist_ok=True)
text = open(SRC).read()
replacements = []

# 0. the head: the copy named
replacements.append((
    '"""David\'s local lean Node, complete (the owner\'s word, 04:4x: run everything, omit nothing).',
    '"""fd1\'s FLAGGED COPY (2026-10-25) of David\'s lean toy for the unifications: one bilinear (W, the current, the twist, the sign current, the form, the momentum\'s change) and one lay (the lay, the take, the undo, the seed\'s drifts) under the world file\'s key control.fd1 = "unify" (make_fd1_copy.py names every delta); David\'s file under toy/ is untouched.\nDavid\'s local lean Node, complete (the owner\'s word, 04:4x: run everything, omit nothing).'))

# 1. the flag at module level, beside Z
replacements.append((
    "Z = lambda shape: np.zeros(shape, dtype=object)\n",
    "Z = lambda shape: np.zeros(shape, dtype=object)\nUNIFY = [False]  # fd1: the flag, set once at the load from the world file's control.fd1; off, David's path line for line\n"))

# 2. the one bilinear beside the Wronskian
replacements.append((
    '''def wronskian(re, im):
    """The plane's bilinear W = re_now im_before - im_now re_before at every Node (the charge density, the sign's source)."""
    return re.now * im.before - im.now * re.before
''',
    '''def bilinear(a_now, a_before, b_now, b_before):
    """fd1: THE one bilinear of two (now, before) pairs, W(a, b) = a_now b_before - b_now a_before, antisymmetric (W(b, a) = -W(a, b)): two lines at one Node give the plane's Wronskian (the charge); one line at the two ends of a Link gives the Link's current F_ij (odd under the ends' exchange with no label); the pair (u_b, u_c) at the two ends gives the twist; (re, im) at the two ends gives the sign current; a line against its own next gives the form now^2 - next x before; the increment against the two neighbours gives the lattice momentum's change."""
    return a_now * b_before - b_now * a_before


def wronskian(re, im):
    """The plane's bilinear W = re_now im_before - im_now re_before at every Node (the charge density, the sign's source)."""
    return bilinear(re.now, re.before, im.now, im.before) if UNIFY[0] else re.now * im.before - im.now * re.before
'''))

# 3. the sign current J_a: the bilinear of (re, im) at the Node against the framed gradient
replacements.append((
    "        found.append(re.now * dz_im - im.now * dz_re)\n",
    "        found.append(bilinear(re.now, im.now, dz_re, dz_im) if UNIFY[0] else re.now * dz_im - im.now * dz_re)  # fd1: W((re, im)_i, (re, im)_j) summed with the Ports' signs\n"))

# 4. the Link's current: the bilinear of one line at the two ends
replacements.append((
    "    return line.now * across(line.before, port) - line.before * across(line.now, port)\n",
    "    return bilinear(line.now, line.before, across(line.now, port), across(line.before, port)) if UNIFY[0] else line.now * across(line.before, port) - line.before * across(line.now, port)  # fd1\n"))

# 5. the twist: the bilinear of the pair (u_b, u_c) at the two ends
replacements.append((
    "    return ub * across(uc, 2 * a) - uc * across(ub, 2 * a)\n",
    "    return bilinear(ub, uc, across(ub, 2 * a), across(uc, 2 * a)) if UNIFY[0] else ub * across(uc, 2 * a) - uc * across(ub, 2 * a)  # fd1\n"))

# 6. the form: the bilinear of a line against its own next
replacements.append((
    "                for l0, lv in zip(start, levels): forms = forms + (l0.now * l0.now - lv * l0.before)\n",
    "                for l0, lv in zip(start, levels): forms = forms + (bilinear(l0.now, l0.before, lv, l0.now) if UNIFY[0] else (l0.now * l0.now - lv * l0.before))  # fd1: D = W((now, before), (next, now))\n"))

# 7. the lattice momentum's change at a lay: the bilinear of the increment against the two neighbours
replacements.append((
    "            found.append(2 * num * (d_now * (int(line_before[down]) - int(line_before[up])) + d_before * (int(line_now[up]) - int(line_now[down]))))\n",
    "            found.append(2 * num * (bilinear(d_now, d_before, int(line_now[down]), int(line_before[down])) - bilinear(d_now, d_before, int(line_now[up]), int(line_before[up]))) if UNIFY[0] else 2 * num * (d_now * (int(line_before[down]) - int(line_before[up])) + d_before * (int(line_now[up]) - int(line_now[down]))))  # fd1\n"))

# 8. the children's Wronskians at the birth
replacements.append((
    "                W_children = [int(re.now[w_] * im.before[w_] - im.now[w_] * re.before[w_]) for w_ in (minus, plus)]",
    "                W_children = [int(bilinear(re.now[w_], re.before[w_], im.now[w_], im.before[w_]) if UNIFY[0] else re.now[w_] * im.before[w_] - im.now[w_] * re.before[w_]) for w_ in (minus, plus)]"))

# 9. the credit's Wronskian
replacements.append((
    "        W = int(re.now[at] * im.before[at] - im.now[at] * re.before[at])\n",
    "        W = int(bilinear(re.now[at], re.before[at], im.now[at], im.before[at]) if UNIFY[0] else re.now[at] * im.before[at] - im.now[at] * re.before[at])  # fd1\n"))

# 10. the flag read once at the load
replacements.append((
    "        ints = universe['integers']\n",
    "        ints = universe['integers']\n        UNIFY[0] = world.get('control', {}).get('fd1') == 'unify'  # fd1: the flag, a control key outside the law as the toy's control is\n"))

# 11. the seed's drift lays through the one lay act (the sea, the hole, the at)
replacements.append((
    "                z = r_.lines[0]; z.now[:] = z.now + self.drift\n",
    "                if UNIFY[0]: self.lay(self.records().index(r_), Ellipsis, (self.drift, 0, 0, 0))  # fd1: the sea is the lay act over the board\n                else: z = r_.lines[0]; z.now[:] = z.now + self.drift\n"))
replacements.append((
    "                at = self.node_of(lay['at']); z = self.row(2, gap=0).lines[0]; z.now[at] = z.now[at] - self.drift\n",
    "                at = self.node_of(lay['at']); z = self.row(2, gap=0).lines[0]\n                if UNIFY[0]: self.lay(self.records().index(self.row(2, gap=0)), at, (self.drift, 0, 0, 0), -1)  # fd1: the hole is the lay act at -1\n                else: z.now[at] = z.now[at] - self.drift\n"))
replacements.append((
    "                if r_.gap == 0: z = r_.lines[0]; z.now[at] = z.now[at] + n * self.drift\n",
    "                if r_.gap == 0 and UNIFY[0]: self.lay(self.records().index(r_), at, (n * self.drift, 0, 0, 0))  # fd1: the at lay of the massless row is the lay act\n                elif r_.gap == 0: z = r_.lines[0]; z.now[at] = z.now[at] + n * self.drift\n"))

# 12. the take is the lay act at the count moved toward before (the same act, the levels (t s, 0, 0, 0))
replacements.append((
    "        z.now[at] = now + toward * levels; self.closes[at] += 1\n",
    "        if UNIFY[0]: self.lay(self.records().index(self.row(2, gap=0)), at, (toward * levels, 0, 0, 0))  # fd1: the take is the one lay act\n        else: z.now[at] = now + toward * levels\n        self.closes[at] += 1\n"))

# 13. the undo of a take is the lay act at -1 of the levels the take moved
replacements.append((
    """                z.now[at] = entry['light_now_was']; self.closes[at] -= 1
            elif entry['event'] == 'credit':
                z.now[at] = entry['light_now_was']; self.closes[at] -= 1
""",
    """                if UNIFY[0]: self.lay(self.records().index(self.row(2, gap=0)), at, (int(z.now[at]) - entry['light_now_was'], 0, 0, 0), -1)  # fd1: the take undone is the lay act at -1
                else: z.now[at] = entry['light_now_was']
                self.closes[at] -= 1
            elif entry['event'] == 'credit':
                if UNIFY[0]: self.lay(self.records().index(self.row(2, gap=0)), at, (int(z.now[at]) - entry['light_now_was'], 0, 0, 0), -1)  # fd1
                else: z.now[at] = entry['light_now_was']
                self.closes[at] -= 1
"""))

# 14. The one rule of the remainder (the owner's word through the Boss, 13:1x UTC): the keys that read a coefficient's division by the one rule (a negative numerator mirrors the carry: half away from zero) and the digits' fold under the ones' complement; and the tie counters (readings, no act)
replacements.append((
    "        cphi = paces.rounded(at(potential.lines[0]) * p0, self.gamma)  # the clocked potential at the potential's start level\n",
    "        cphi = (paces.odd_rounded if self.control.get('fd1_round') == 'odd' else paces.rounded)(at(potential.lines[0]) * p0, self.gamma)  # the clocked potential at the potential's start level; fd1: under the key the one rule's rounding of a signed coefficient (the carry mirrored for a negative numerator)\n"))
replacements.append((
    "            t = (summed + 1) // 2\n",
    "            t = paces.odd_rounded(summed, 2) if self.control.get('fd1_tension') == 'odd' else (summed + 1) // 2  # fd1: under the key the one rule's rounding of the signed sum\n            self.ties['tension sums negative and odd'] += int(sum(1 for v in np.asarray(summed, dtype=object).reshape(-1) if int(v) < 0 and int(v) % 2 == 1))\n"))
replacements.append((
    "                if self.control.get('digits') == 'folded': rem = min(rem, wl - rem); values = values // 2 + 1  # the Boss's mend of 10:1x for the twist's CP: every line's remainder folded to its wall, min(r, w - r), the distance to the nearer edge, conjugation-even on every line alike\n",
    "                if self.control.get('digits') == 'folded': rem = min(rem, wl - rem); values = values // 2 + 1  # the Boss's mend of 10:1x for the twist's CP: every line's remainder folded to its wall, min(r, w - r), the distance to the nearer edge, conjugation-even on every line alike\n                elif self.control.get('digits') == 'folded1': rem = min(rem, wl - 1 - rem); values = values // 2 + 1  # fd1: the fold under the one rule's mirror w - 1 - r, the distance to the nearer edge of [0, w - 1]\n"))
replacements.append((
    "        a_re, a_im = (2 * a_re + self.X) // (2 * self.X), (2 * a_im + self.X) // (2 * self.X)\n",
    "        for v in (a_re, a_im): self.ties['arrival ties at X (first rounding)'] += int(sum(1 for q in np.asarray(v, dtype=object).reshape(-1) if (2 * int(q)) % (2 * self.X) == self.X)); self.ties['arrival roundings at X'] += int(np.asarray(v).size)\n        a_re, a_im = (2 * a_re + self.X) // (2 * self.X), (2 * a_im + self.X) // (2 * self.X)\n"))
replacements.append((
    "        return [(2 * b_re + tw) // (2 * tw), (2 * b_im + tw) // (2 * tw)]\n",
    "        for v in (b_re, b_im): self.ties['arrival ties at the tangent wall (second rounding)'] += int(sum(1 for q, t_ in zip(np.asarray(v, dtype=object).reshape(-1), np.asarray(tw, dtype=object).reshape(-1)) if (2 * int(q)) % (2 * int(t_)) == int(t_)))\n        return [(2 * b_re + tw) // (2 * tw), (2 * b_im + tw) // (2 * tw)]\n"))
replacements.append((
    "        self.max_transient = 0\n",
    "        self.max_transient = 0\n        self.ties = {'arrival ties at X (first rounding)': 0, 'arrival roundings at X': 0, 'arrival ties at the tangent wall (second rounding)': 0, 'tension sums negative and odd': 0}  # fd1: readings of the one rule's ties, no act\n"))

out = text
for old, new in replacements:
    count = out.count(old)
    if count != 1:
        sys.exit('refused: a replacement matches %d times, not once: %r' % (count, old[:90]))
    out = out.replace(old, new)
open(DST, 'w').write(out)
for name in ('decoder_full.py', 'cube48_test.py', 'reach_test.py', 'universe_toy.json', 'universe_middle.json'):
    shutil.copyfile(os.path.join(HERE, 'toy', name), os.path.join(DST_DIR, name))  # David's own files, unchanged, so the tests import the copy from their folder
print('written', DST, len(out), 'bytes;', len(replacements), 'replacements')
