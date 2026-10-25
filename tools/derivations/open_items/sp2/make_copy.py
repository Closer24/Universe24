"""sp2: makes the flagged COPY lean_sp2.py of David's toy (toy/lean_full.py, never edited in place).

Every change is a replacement listed below, each asserted to occur exactly once in the toy's text, so the
copy's departure from the toy is this file and nothing else. The flags (world-file keys, absent in David's
worlds, so a world of his runs bit for bit through the copy):
  - the `at` lay takes an optional `sense` (1 or -1): one record of one sense laid alone (David's lay lays the
    conjugate pair, the two senses superposed on the one plane, a neutral record);
  - `control.held_potential`: a list of hand-held lines of the shape-4 row (the potential): each entry names the
    line (0 the time line A_0, 1..3 the odd lines A_x, A_y, A_z), the field's form and its integers; the line is
    set at the start and restored after every act in either direction (a constant, as the toy's held well of the
    volume is; the Stern-Gerlach magnet as a control, no lay of the law).
Integers only.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'toy', 'lean_full.py')
OUT = os.path.join(HERE, 'lean_sp2.py')

REPLACEMENTS = [
    # 0. the head: the copy named
    ('"""David\'s local lean Node, complete',
     '"""sp2 flagged copy of tools/derivations/sp2/toy/lean_full.py (made by make_copy.py; the flags: the `at` lay\'s `sense`, `control.held_potential`). David\'s local lean Node, complete'),
    # 1. the path to src: this copy sits one folder shallower than David's toy
    ("os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'src'))  # tools/derivations/toys/lean -> src",
     "os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'src'))  # tools/derivations/sp2 -> src (the copy's place)"),
    # 2. the `at` lay carries an optional sense
    ("                else: packets.append((self.records().index(r_), at, int(lay.get('width', 0)), n))",
     "                else: packets.append((self.records().index(r_), at, int(lay.get('width', 0)), n, lay.get('sense')))  # sp2 flag: `sense` lays one record alone"),
    ("        for s_, at, h, n in packets: self.lay_packet(s_, at, h, n)",
     "        for s_, at, h, n, one_sense in packets: self.lay_packet(s_, at, h, n, one_sense)"),
    ("    def lay_packet(self, rec, at, h, n):",
     "    def lay_packet(self, rec, at, h, n, one_sense=None):"),
    ("        for sense in (-1, 1):  # the conjugate pair laid onto the one plane: at one Node the two senses superpose (the im lines cancel, the record neutral)",
     "        for sense in ((-1, 1) if one_sense is None else (int(one_sense),)):  # sp2 flag: one sense alone where the lay names it; else David's conjugate pair (the im lines cancel, the record neutral)"),
    ("        self.log.append({'event': 'lay', 'i': 0, 'node': list(at), 'line_pair': rec, 'width': h, 'quanta': n, 'amplitude': low, 'share': share_of(low), 'unit': self.units[rec], 'nodes': int(sum(1 for x in envelope.reshape(-1) if int(x) > 0))})",
     "        self.log.append({'event': 'lay', 'i': 0, 'node': list(at), 'line_pair': rec, 'width': h, 'quanta': n, 'amplitude': low, 'share': share_of(low), 'unit': self.units[rec], 'nodes': int(sum(1 for x in envelope.reshape(-1) if int(x) > 0)), 'sense': one_sense})"),
    # 3. the held lines of the potential (the magnet): set at the start
    ("        self.detectors = [self.node_of(d) for d in world.get('detectors', [])]\n        self.A = rule3.largest_below(action // 2)",
     "        self.detectors = [self.node_of(d) for d in world.get('detectors', [])]\n"
     "        self.held_lines = []  # sp2 flag: hand-held lines of the shape-4 row (a control: the Stern-Gerlach magnet), each set here and restored after every act\n"
     "        for h_ in self.control.get('held_potential', []):\n"
     "            k_ = int(h_['line']); at_ = self.node_of(h_['at']); F = Z(self.shape)\n"
     "            def centred(node, a):  # the torus-centred offset along the axis a\n"
     "                d = (node[a] - at_[a]) % self.cube\n"
     "                return d - self.cube if d > self.cube // 2 else d\n"
     "            for node in np.ndindex(*self.shape):\n"
     "                if h_['field'] == 'sg': F[node] = -centred(node, int(h_['across'])) * (int(h_['B0']) + int(h_['b']) * centred(node, int(h_['along'])))  # A_axis = -(d_across)(B0 + b d_along): B_along = B0 + b d_along, its gradient along `along`\n"
     "                elif h_['field'] == 'linear': F[node] = int(h_['E']) * centred(node, int(h_['along']))  # a uniform gradient E of the line along `along`\n"
     "                else: raise ValueError('a held field of no form: %r' % (h_['field'],))\n"
     "            line_ = self.row(4).lines[k_]; line_.now = F.copy(); line_.before = F.copy(); self.held_lines.append(k_)\n"
     "        self.A = rule3.largest_below(action // 2)"),
    # 4. the held lines restored after the shape-4 row's act, in either direction
    ("            start, levels, out[k] = self.act(rows[k], rule, turn, numerators, direction, flux, *ends(k))\n",
     "            start, levels, out[k] = self.act(rows[k], rule, turn, numerators, direction, flux, *ends(k))\n"
     "            if r.shape == 4 and self.held_lines:  # sp2 flag: the held lines of the potential restored to the interval's start (a constant in both directions, the bijection kept)\n"
     "                for kk in self.held_lines: out[k][kk] = held[k][kk].copy()\n"),
]


def main():
    text = open(SRC).read()
    for old, new in REPLACEMENTS:
        count = text.count(old)
        assert count == 1, ('replacement target found %d times, expected 1: %r' % (count, old[:80]))
        text = text.replace(old, new)
    open(OUT, 'w').write(text)
    print('wrote', OUT, 'with', len(REPLACEMENTS), 'replacements')


if __name__ == '__main__':
    main()
