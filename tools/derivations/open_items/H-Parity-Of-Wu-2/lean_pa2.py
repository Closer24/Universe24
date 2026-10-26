"""Hand pa2's copy of David's lean toy with one flag: the orientation of the Link birth (ALGEBRA.md, The conversion; The click's parity; the Q comparison's S1).

The class LeanPa2 subclasses David's Lean (tools/derivations/open_items/H-Parity-Of-Wu-2/toy/lean_full.py, a copy of origin/toys-5, untouched) and replaces one method, `close`, with a copy of his that differs at one line, the choice of the end the + child goes to, behind `orientation`:
  'current' (the default): the + child at the end the light's own current F_ij = num (now_i before_j - before_i now_j) flows into; F = 0 refused by the name 'orientation' (David's path, bit for bit: checked by the state hash in pa2_48.py).
  'twist': the + child at the end the current flows into where the twist of the light's transverse current between the two ends is right-handed, at the end it flows from where left-handed: h = e_ij . (u(i) x u(j)), u_b(k) = F(k, k - b) - F(k, k + b) the light's net current along b at the end k (the two ends' four transverse Links each: one Link's reach at each end); h is a pseudoscalar on the Link (even under the 24 rotations, odd under the 24 reflections, symmetric under the exchange of the ends), so the end named by sign(F) x sign(h) is P-odd; h = 0 refused by the name 'twist'; F = 0 refused as before.
  'label': the + child at the +a end (the lattice label; the negative control, David's `link` switch).
The second reading, no state: at every turned Node the sign of every plane record's Wronskian before and after the swap's exchange, counted kept or exchanged (`sense_at_swap`).
Integers only; no float; no number of a universe in this file."""
from __future__ import annotations
import sys, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'toy'))
from lean_full import Lean, load_world, AXES, across, wronskian, paces  # David's toy, the copy under toy/

CYCLIC = ((0, 1, 2), (1, 2, 0), (2, 0, 1))  # (a, b, c) with e_a = e_b x e_c


class LeanPa2(Lean):
    def __init__(self, universe, world, orientation='current'):
        self.orientation = orientation
        self.sense_at_swap = {'kept': 0, 'exchanged': 0, 'zero': 0}
        self.counts_twist = {'refused_twist': 0, 'plus_downstream': 0, 'plus_upstream': 0}
        super().__init__(universe, world)

    def net_current(self, line, axis):
        """The light's net current along +axis at every Node, u_a(k) = F(k, k - a) - F(k, k + a) (ALGEBRA.md, The lattice momentum: P_a = SUM_k (F_(k,k-a) - F_(k,k+a))), each F the Link's own read `link_current`."""
        return self.link_current(line, 2 * axis + 1) - self.link_current(line, 2 * axis)

    def twist(self, line, axis):
        """The twist of the light's transverse current along the +axis Link of every Node, h(k, k + e_a) = u_b(k) u_c(k + e_a) - u_c(k) u_b(k + e_a) with (a, b, c) cyclic: e_a . (u(k) x u(k + e_a)); the cross product of the two ends' transverse currents, read at the two ends from their own transverse Links (one Link's reach at each end)."""
        a, b, c = CYCLIC[axis]
        ub, uc = self.net_current(line, b), self.net_current(line, c)
        return ub * across(uc, 2 * a) - uc * across(ub, 2 * a)

    def exchange(self, top, held):
        """David's exchange, with a reading before and after: the sign of every plane record's W at the turned Nodes."""
        before = [np.sign(wronskian(*held[1 + k])) for k in range(2 * self.nl)]  # the held pre-state's planes (rows 1..2 nl), the state the exchange acts on
        super().exchange(top, held)
        after = [np.sign(wronskian(*rec)) for rec in self.planes]
        for wb, wa in zip(before, after):
            for at in zip(*np.nonzero(top)):
                sb, sa = int(wb[at]), int(wa[at])
                if sb == 0: self.sense_at_swap['zero'] += 1
                elif sb == sa: self.sense_at_swap['kept'] += 1
                else: self.sense_at_swap['exchanged'] += 1

    def close(self, start):
        """David's close, copied, one line changed (marked PA2): the end the + child goes to."""
        c = self.start_content; factors = self.link_factors()
        r_light = self.rule((self.den, self.den), c, factors)
        rules = [(start['light'], r_light), (self.sign, r_light), (self.vol, self.rule(self.vol_pair, c, factors))]
        for s_, pair in enumerate(self.pairs):
            r = self.rule(pair, c, factors)
            for sense in (0, 1):
                rules += [(start['planes'][2 * s_ + sense][0], r), (start['planes'][2 * s_ + sense][1], r)]
        pace = paces.link_pace_of(self.gamma, c)
        sh = self.share(start['light'], r_light, pace, vacuum=True)
        owns = []
        for rec in range(2 * self.nl):
            r = self.rule(self.pairs[rec // 2], c, factors); re0, im0 = start['planes'][rec]
            owns.append(self.share(re0, r, pace, vacuum=True) + self.share(im0, r, pace, vacuum=True))
        born = []
        frozen = np.asarray(pace, dtype=object) == 0 if np.ndim(pace) else np.zeros(self.shape, dtype=bool)
        currents = [self.den * self.link_current(start['light'], 2 * axis) for axis in range(3)]
        twists = [self.twist(start['light'], axis) for axis in range(3)] if self.orientation == 'twist' else None  # PA2: the twist of the light's transverse current on the +a Link of every Node, read once
        for at in np.ndindex(*self.shape):
            if frozen[at]: continue
            for axis in range(3):
                j = tuple((at[a] + (1 if a == axis else 0)) % self.cube for a in range(3))
                if frozen[j] or int(sh[at]) < self.unit_light or int(sh[j]) < self.unit_light: continue
                F = int(currents[axis][at])
                if F == 0:
                    self.counts['refused_orientation'] += 1; self.log.append({'event': 'refused', 'i': self.interval, 'node': list(at), 'cause': 'orientation', 'link': list(j)}); continue
                # PA2: the changed lines. David: plus, minus = (j, at) if F > 0 else (at, j); the number read and the take at plus
                into, outof = ((j, at) if F > 0 else (at, j))  # the end the current flows into, the end it flows from: a scalar reading of the oriented Link under the 48
                if self.orientation == 'current':
                    plus, minus = into, outof; read_at = plus; rules_read = rules
                elif self.orientation == 'label':
                    plus, minus = j, at; read_at = plus; rules_read = rules
                else:
                    h = int(twists[axis][at])
                    if h == 0:
                        self.counts_twist['refused_twist'] += 1; self.log.append({'event': 'refused', 'i': self.interval, 'node': list(at), 'cause': 'twist', 'link': list(j)}); continue
                    plus, minus = (into, outof) if h > 0 else (outof, into)
                    self.counts_twist['plus_downstream' if h > 0 else 'plus_upstream'] += 1
                    # the Link's one number and the take stay at the current's end (even under the 48 and under the conjugation); the number is read from the rows even under the conjugation alone (the light's and the volume's: the planes' and the sign's remainders are complemented by the conjugation, ALGEBRA.md The swap at the top, and would make the lift Conj-odd)
                    read_at = into; rules_read = [rules[0], rules[2]]
                number = self.read_number(read_at, rules_read)
                if number is None: continue
                s_ = (number // self.unit_light) % self.nl
                born.append((read_at, s_, minus, plus, F))
        kept = []
        for at, s_, minus, plus, F in born:
            if int(owns[2 * s_][minus]) > 0 or int(owns[2 * s_ + 1][plus]) > 0:
                self.counts['refused_lay'] += 1; self.log.append({'event': 'refused', 'i': self.interval, 'node': list(at), 'cause': 'lay', 'standing': int(owns[2 * s_][minus]), 'unit': self.units[s_]}); continue
            kept.append((at, s_, minus, plus, F))
        landing = {}
        for at, s_, minus, plus, F in kept:
            landing[(2 * s_, minus)] = landing.get((2 * s_, minus), 0) + 1; landing[(2 * s_ + 1, plus)] = landing.get((2 * s_ + 1, plus), 0) + 1
        crowded = [(at, s_, minus, plus, F) for at, s_, minus, plus, F in kept if landing[(2 * s_, minus)] > 1 or landing[(2 * s_ + 1, plus)] > 1]
        for at, s_, minus, plus, F in crowded:
            self.counts['refused_lay'] += 1; self.log.append({'event': 'refused', 'i': self.interval, 'node': list(at), 'cause': 'lay', 'children_at_one_node': max(landing[(2 * s_, minus)], landing[(2 * s_ + 1, plus)])})
        kept = [k for k in kept if k not in crowded]
        by_node = {}
        for at, s_, minus, plus, F in kept: by_node.setdefault(at, []).append((s_, minus, plus, F))
        taken_births = []
        for at in sorted(by_node):
            children = by_node[at]; walls = sum(2 * self.units[s_] for s_, _m, _p, _F in children)
            levels, fall = self.take(at, walls, r_light, self.light)
            if levels is None:
                self.counts['refused_stop'] += len(children); self.log.append({'event': 'refused', 'i': self.interval, 'node': list(at), 'cause': 'stop', 'fall': fall, 'walls': walls}); continue
            taken_births.append((at, children, levels, fall, walls))
        for at, children, levels, fall, walls in taken_births:
            now = int(self.light.now[at]); before = int(self.light.before[at]); toward = 1 if before > now else -1
            self.light.now[at] = now + toward * levels
            for s_, minus, plus, F in children:
                A = self.lay_amplitude(s_, at, c, factors, pace)
                W_pair = 0
                for sense, rec, where in ((-1, 2 * s_, minus), (1, 2 * s_ + 1, plus)):
                    re, im = self.planes[rec]; re.now[where] = re.now[where] + A; im.before[where] = im.before[where] + sense * A
                    W_pair += int(re.now[where] * im.before[where] - im.now[where] * re.before[where])
                self.counts['births'] += 1; self.closes[at] += 1
                # PA2: the birth's line carries the current's sign on the Link from minus to plus (plus_downstream 1 where the + child sits at the end the current flows into) and the pair's Wronskian at the lay (the charge made, 0 at empty Nodes)
                downstream = 1 if ((plus == tuple((minus[a] + (1 if a == axis_of(minus, plus, self.cube) else 0)) % self.cube for a in range(3))) == (F > 0)) else -1
                self.log.append({'event': 'birth', 'i': self.interval, 'node': list(at), 'line_pair': s_, 'senses': [-1, 1], 'minus': list(minus), 'plus': list(plus), 'taken': fall, 'booked': walls, 'levels': levels, 'light_now_was': now, 'proper': int(self.proper[at]), 'content': int(c[at]), 'amplitude': A, 'children_at_node': len(children), 'plus_downstream': downstream, 'W_pair': W_pair})
            self.counts['taken'] += fall; self.counts['booked'] += walls
        born_nodes = {at for at, _c, _l, _f, _w in taken_births} | {m for _a, ch, _l, _f, _w in taken_births for _s, m, _p, _F in ch} | {p_ for _a, ch, _l, _f, _w in taken_births for _s, _m, p_, _F in ch}
        for rec in range(2 * self.nl):
            s_ = rec // 2; r = self.rule(self.pairs[s_], c, factors)
            own = owns[rec]
            standing_now = np.vectorize(lambda v: 1 if int(v) >= self.units[s_] else 0, otypes=[object])(own)
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
                levels, fall = self.take(at, self.units[s_], r_light, self.light)
                if levels is None:
                    self.counts['refused_stop'] += 1; self.standing[rec][at] = 0; continue
                now = int(self.light.now[at]); before = int(self.light.before[at]); toward = 1 if before > now else -1
                self.light.now[at] = now + toward * levels
                self.counts['body_clicks'] += 1; self.closes[at] += 1; self.standing[rec][at] = 0
                self.log.append(self.credit(rec, at, start, fall, levels, now))
        if self.detectors:
            sh_end = self.share(self.light, r_light, pace, vacuum=True); sh_vac = self.share(start['light'], r_light, pace, vacuum=True)
            for det in self.detectors:
                rise = int(sh_end[det]) // self.unit_light - int(sh_vac[det]) // self.unit_light
                if rise > 0:
                    self.counts['light_credits'] += rise
                    self.log.append({'event': 'light', 'i': self.interval, 'node': list(det), 'quanta': rise, 'proper': int(self.proper[det]), 'content': int(c[det]), 'light_now': int(self.light.now[det]), 'light_before': int(self.light.before[det])})


def axis_of(minus, plus, cube):
    """The axis of the Link between the two children's Nodes (they differ on one axis by one Link, the torus wrapped)."""
    for a in range(3):
        if (minus[a] - plus[a]) % cube != 0: return a
    raise ValueError('the two children at one Node')
