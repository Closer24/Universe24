"""fd1's FOLDED copy of David's lean toy (no flag): the same deltas as make_fd1_copy.py written unconditionally, so that the count of lines and functions of the folded Node is read on a file that runs; written by this script and never by hand, every replacement matched exactly once. Run: python make_fd1_folded.py (writes toy_fd1_folded/lean_full.py)."""
import os, sys, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'toy', 'lean_full.py'); DST_DIR = os.path.join(HERE, 'toy_fd1_folded'); DST = os.path.join(DST_DIR, 'lean_full.py')
os.makedirs(DST_DIR, exist_ok=True)
text = open(SRC).read(); R = []
R.append(('"""David\'s local lean Node, complete (the owner\'s word, 04:4x: run everything, omit nothing).', '"""fd1\'s FOLDED COPY (2026-10-25) of David\'s lean toy: one bilinear and one lay, no flag (make_fd1_folded.py names every delta); David\'s file under toy/ is untouched.\nDavid\'s local lean Node, complete (the owner\'s word, 04:4x: run everything, omit nothing).'))
R.append(('''def wronskian(re, im):
    """The plane's bilinear W = re_now im_before - im_now re_before at every Node (the charge density, the sign's source)."""
    return re.now * im.before - im.now * re.before
''', '''def bilinear(a_now, a_before, b_now, b_before):
    """THE one bilinear of two (now, before) pairs, W(a, b) = a_now b_before - b_now a_before, antisymmetric: two lines at one Node the plane's Wronskian (the charge); one line at a Link's two ends the current F_ij; (u_b, u_c) at the two ends the twist; (re, im) at the two ends the sign current; a line against its own next the form now^2 - next x before; the increment against the two neighbours the lattice momentum's change."""
    return a_now * b_before - b_now * a_before


def wronskian(re, im):
    """The plane's bilinear W = re_now im_before - im_now re_before at every Node (the charge density, the sign's source)."""
    return bilinear(re.now, re.before, im.now, im.before)
'''))
R.append(("        found.append(re.now * dz_im - im.now * dz_re)\n", "        found.append(bilinear(re.now, im.now, dz_re, dz_im))\n"))
R.append(("    return line.now * across(line.before, port) - line.before * across(line.now, port)\n", "    return bilinear(line.now, line.before, across(line.now, port), across(line.before, port))\n"))
R.append(("    return ub * across(uc, 2 * a) - uc * across(ub, 2 * a)\n", "    return bilinear(ub, uc, across(ub, 2 * a), across(uc, 2 * a))\n"))
R.append(("                for l0, lv in zip(start, levels): forms = forms + (l0.now * l0.now - lv * l0.before)\n", "                for l0, lv in zip(start, levels): forms = forms + bilinear(l0.now, l0.before, lv, l0.now)\n"))
R.append(("            found.append(2 * num * (d_now * (int(line_before[down]) - int(line_before[up])) + d_before * (int(line_now[up]) - int(line_now[down]))))\n", "            found.append(2 * num * (bilinear(d_now, d_before, int(line_now[down]), int(line_before[down])) - bilinear(d_now, d_before, int(line_now[up]), int(line_before[up]))))\n"))
R.append(("                W_children = [int(re.now[w_] * im.before[w_] - im.now[w_] * re.before[w_]) for w_ in (minus, plus)]", "                W_children = [int(bilinear(re.now[w_], re.before[w_], im.now[w_], im.before[w_])) for w_ in (minus, plus)]"))
R.append(("        W = int(re.now[at] * im.before[at] - im.now[at] * re.before[at])\n", "        W = int(bilinear(re.now[at], re.before[at], im.now[at], im.before[at]))\n"))
R.append(("                z = r_.lines[0]; z.now[:] = z.now + self.drift\n", "                self.lay(self.records().index(r_), Ellipsis, (self.drift, 0, 0, 0))\n"))
R.append(("                at = self.node_of(lay['at']); z = self.row(2, gap=0).lines[0]; z.now[at] = z.now[at] - self.drift\n", "                at = self.node_of(lay['at']); self.lay(self.records().index(self.row(2, gap=0)), at, (self.drift, 0, 0, 0), -1)\n"))
R.append(("                if r_.gap == 0: z = r_.lines[0]; z.now[at] = z.now[at] + n * self.drift\n", "                if r_.gap == 0: self.lay(self.records().index(r_), at, (n * self.drift, 0, 0, 0))\n"))
R.append(("        z.now[at] = now + toward * levels; self.closes[at] += 1\n", "        self.lay(self.records().index(self.row(2, gap=0)), at, (toward * levels, 0, 0, 0)); self.closes[at] += 1\n"))
R.append(("""                z.now[at] = entry['light_now_was']; self.closes[at] -= 1
            elif entry['event'] == 'credit':
                z.now[at] = entry['light_now_was']; self.closes[at] -= 1
""", """                self.lay(self.records().index(self.row(2, gap=0)), at, (int(z.now[at]) - entry['light_now_was'], 0, 0, 0), -1); self.closes[at] -= 1
            elif entry['event'] == 'credit':
                self.lay(self.records().index(self.row(2, gap=0)), at, (int(z.now[at]) - entry['light_now_was'], 0, 0, 0), -1); self.closes[at] -= 1
"""))
out = text
for old, new in R:
    c = out.count(old)
    if c != 1: sys.exit('refused: a replacement matches %d times, not once: %r' % (c, old[:90]))
    out = out.replace(old, new)
open(DST, 'w').write(out)
for name in ('universe_toy.json', 'universe_middle.json'): shutil.copyfile(os.path.join(HERE, 'toy', name), os.path.join(DST_DIR, name))
print('written', DST, len(out), 'bytes;', len(R), 'replacements')
