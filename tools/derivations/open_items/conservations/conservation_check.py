"""The conservation check over David's lean toy (tools/derivations/toys/lean): the toy is run from a world file for N intervals and
every law of the lattice is read on its board and in its clicks, in integers alone, each interval, from the toy's own records and
board (the toy's code is imported and never changed: the check subclasses the Node to snapshot the board before the close).

Usage: conservation_check.py <world.json> <intervals> [--toy <dir>]
  <dir> the folder of lean_full.py (default: the folder `toy` beside this script).
Prints one line per law, "LAW: held N of N" or "LAW: broken at interval k, Node (x,y,z), the numbers", with the numbers under it;
exit code 0 only when every law holds.

The laws, each by its clause of docs/ALGEBRA.md:
 1. ENERGY in the clicks (The ledger of exactness, the exact take; The conservation at the click, line by line): at every click the
    take read from the board equals the credit line's `taken`, the take is the least count of levels whose fall pays the walls, the
    fall pays the walls (taken >= booked), and taken == booked exactly (the identity of the credit lines; counted exact of all);
    the born pair carries two whole quanta (each child's record at or above one quantum of its unit at its Node after the lay).
 2. MOMENTUM (The lattice momentum): P_a = 2 num SUM_i (now_(i+a) before_i - now_i before_(i+a)) per row on the board before the
    step, after the step and after the close; the step's change against the floors' bound num SUM_i |now_(i+a) - now_(i-a)|
    (to the floor where within, named beyond where not: the paces' gradient, the force law); the close's change equal, exactly, to
    the momentum the credit lines wrote (the takes' levels and the lays' amplitudes against the board's levels at the start of the
    close); the credits' running cosine and sign current J_a per axis from the credit lines alone (a reading).
 3. CHARGE (The sign is the rotation sense; The charge written is the Wronskian over T div 2): the Wronskian's sum over the board
    before and after the step (plain and weighted by 1 / p_i^2 as an exact rational), the charge in units of T div 2; at the close
    the board's W unchanged and every birth's two children W of opposite sign summing to 0 (the pair's two senses).
 4. FLUX on the board (The flux form of Rule3; The conserved form; The tension): F_ij = -F_ji on every Link of the light's own
    current; Rule3's identity at every Node and line, w (a_next - 2 a_now + a_before) + r' - r = SUM_j R_ij (m_ij - a_now) - D a_now
    with the write's quotient w inc and its wall's book beside it, residual 0; the exchange at every turned Node; the linear sum
    L = SUM_i [w (now_i - before_i) + r_i] of the light moved by the pairing term and the write alone.
 5. COUNT from bang to bang (the owner's standing rule; The click writes on the lattice; The direction): every change of the board at
    the close is a logged take or lay and nothing else (the book exact); the quanta in whole units before and after the close
    (the light's share in W_c, the records' in their units) with the booked and the taken beside them (a reading); the run back from
    the end to the seed, the board bit for bit at every interval (the one asynchronous board test).
 6. THE 48 on the clicks (The cube's symmetry): the toy's cube48_test.py compares the births and the two rows through the 48 images;
    this check adds the credits (the body clicks) and the refusals through the image, run on the 3-cube image of the world for at
    most 30 intervals as the toy's test does. The one-Link reach forward and backward is covered by the toy's reach_test.py (both
    halves), nothing added.
"""
import sys, os, json, hashlib, itertools, copy
import numpy as np


def tot(a):
    return int(np.sum(np.asarray(a, dtype=object))) if np.ndim(a) else int(a)


def abs_tot(a):
    return int(sum(abs(int(x)) for x in np.asarray(a, dtype=object).reshape(-1)))


def snap(b):
    return [[l.copy() for l in row] for row in b.rows()]


def flat(rows):
    return [l for row in rows for l in row]


def state_hash(b):
    return hashlib.sha256(b.state_bytes() + str(b.interval).encode()).hexdigest()


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    return a * b // gcd(a, b)


class Law:
    """One law's tally: held counts and the first break with its numbers."""
    def __init__(self, name):
        self.name = name; self.held = 0; self.of = 0; self.breaks = []; self.notes = []
    def count(self, ok, interval=None, node=None, numbers=None):
        self.of += 1
        if ok: self.held += 1
        elif len(self.breaks) < 4: self.breaks.append((interval, node, numbers))
    def line(self):
        if not self.breaks: return '%s: held %d of %d' % (self.name, self.held, self.of)
        k, node, numbers = self.breaks[0]
        where = '' if node is None else ', Node %s' % (tuple(int(x) for x in node),)
        return '%s: broken at interval %s%s, %s (held %d of %d)' % (self.name, k, where, numbers, self.held, self.of)
    def ok(self): return not self.breaks


def main():
    args = sys.argv[1:]
    here = os.path.dirname(os.path.abspath(__file__))
    toy = os.path.join(here, 'toy')
    if '--toy' in args:
        i = args.index('--toy'); toy = args[i + 1]; del args[i:i + 2]
    if len(args) != 2:
        print(__doc__.split('\n')[4]); return 2
    world_path, n = args[0], int(args[1])
    sys.path.insert(0, os.path.abspath(toy))
    sys.set_int_max_str_digits(0)
    import lean_full as LF
    from event_universe.core import rule3, paces
    from event_universe.features import volume as volform

    class Checked(LF.Lean):
        """The toy's Node with the board snapshotted before its click (the state after the step and the swap), nothing else; the click's act is named close on the toy's heads before 437ff73d8 and click from it on."""
        def close(self, start):
            self.pre_close = snap(self); self.close_start = start
            super().close(start)
        def click(self, start):
            self.pre_close = snap(self); self.close_start = start
            super().click(start)
    if not hasattr(LF.Lean, 'close'): del Checked.close
    if not hasattr(LF.Lean, 'click'): del Checked.click

    universe, world = LF.load_world(world_path)
    b = Checked(universe, world)
    den, gamma, T, G, w = b.den, b.gamma, b.T, b.G, b.w
    AX = LF.AXES; across = LF.across
    n_rec = 2 * b.nl
    row_names = ['phase'] + ['plane %d' % k for k in range(n_rec)] + ['light', 'sign', 'volume']
    row_nums = [None] + [b.pairs[k // 2][0] for k in range(n_rec)] + [den, den, b.vol_pair[0]]
    row_pairs = [None] + [b.pairs[k // 2] for k in range(n_rec)] + [(den, den), (den, den), b.vol_pair]
    print(json.dumps({'world': os.path.basename(world_path), 'cube': b.cube, 'intervals': n, 'den': den, 'Gamma': gamma, 'T': T, 'G': G, 'planes': n_rec, 'W_c': b.unit_light, 'units': b.units}))

    L = {k: Law(k) for k in ('ENERGY the take read from the board equals the credit line', 'ENERGY the take is the least count paying the walls', 'ENERGY taken pays booked (taken >= booked)', 'ENERGY the exact take (taken == booked)', 'ENERGY the born pair carries two whole quanta (one per child, the book)',
                              'MOMENTUM the rotate to the floor, exact at uniform plain paces (dP_a w = 2 num SUM (r\' - r)(now(i+a) - now(i-a)))', 'MOMENTUM the close wrote what the credit lines book (dP_a exact)',
                              'CHARGE the board W unchanged at the close', 'CHARGE every birth W(-) + W(+) = 0', 'CHARGE the rotate keeps the weighted W within the remainders and the turn roundings',
                              'FLUX F_ij = -F_ji on every Link', 'FLUX Rule3 identity per Node and line, residual 0', 'FLUX the write book per Node and line', 'FLUX the exchange at every turned Node', 'FLUX the light L moved by the pairing and the write alone',
                              'COUNT the close book exact (every change a logged take or lay)', 'COUNT the run back exact (the board bit for bit)')}
    readings = {'momentum written by the clicks per axis (light, planes)': [[0, 0, 0], [0, 0, 0]], 'credits J_a sum per axis': [0, 0, 0], 'credits running cosine 2cos k_a sum (numerator, denominator) per axis': [[0, 1], [0, 1], [0, 1]],
                'momentum moved by the step: rotate, write (W-S1 and the held writes), exchange at the turns (abs sums per axis)': [[0, 0, 0], [0, 0, 0], [0, 0, 0]], 'momentum at varying paces or folded Links: rows within / beyond the floors bound (the force law)': [0, 0], 'momentum first row beyond the floors bound': None,
                'W drift per step (abs sum, the rotate)': 0, 'W weighted drift (abs sum of numerators over the lcm wall, the rotate)': 0, 'charge in T div 2 units (quotient, remainder) start/end': [None, None],
                'excess taken - booked (share units)': 0, 'excess in W_c (quotient, remainder of the sum)': None, 'children laid at 1 / 2 / more quanta of their unit': [0, 0, 0],
                'clicks': {'births': 0, 'credits': 0, 'refused': 0, 'turns': 0}, 'light quanta (W_c) start/end': [None, None], 'records quanta start/end': [None, None], 'momentum P_a per row start/end': {}}
    intervals_with_clicks = []
    hashes = [state_hash(b)]
    frozen_level = paces.frozen_content(gamma)

    def shares_in_quanta(rows_snapshot, c, factors, pace):
        """The light's share over the board in W_c and each record's share in its unit, whole quanta (the frame's weight at the start pace, as the take reads it): [light quanta, [record quanta...]] with the raw share sums beside."""
        light = rows_snapshot[1 + n_rec][0]
        r_l = b.rule((den, den), c, factors)
        s_light = tot(b.share(light, r_l, pace))
        recs = []
        for rec in range(n_rec):
            r = b.rule(b.pairs[rec // 2], c, factors); re, im = rows_snapshot[1 + rec]
            recs.append(tot(b.share(re, r, pace)) + tot(b.share(im, r, pace)))
        return s_light // b.unit_light, [s // b.units[rec // 2] for rec, s in enumerate(recs)], s_light, recs

    def momentum(lines, num):
        found = []
        for a in range(3):
            p = 0
            for l in lines:
                p += tot(across(l.now, 2 * a) * l.before - l.now * across(l.before, 2 * a))
            found.append(2 * num * p)
        return found

    def floor_bound(lines, num):
        return [num * sum(abs_tot(across(l.now, 2 * a) - across(l.now, 2 * a + 1)) for l in lines) for a in range(3)]

    def wronskian_total(rows_snapshot):
        return sum(tot(LF.wronskian(re, im)) for re, im in rows_snapshot[1:1 + n_rec])

    def weighted_wronskian(rows_snapshot, pace):
        """SUM_i W_i / p_i^2 as the exact rational (numerator, common wall), the wall the lcm of the distinct p_i^2 (p_i the Link pace at the start content; a frozen pace 0 reads the wall 1 as the share does)."""
        p2 = np.vectorize(lambda p: int(p) * int(p) + (1 if int(p) == 0 else 0), otypes=[object])(np.asarray(pace, dtype=object))
        wall = 1
        for v in set(int(x) for x in p2.reshape(-1)): wall = lcm(wall, v)
        weights = np.vectorize(lambda v: wall // int(v), otypes=[object])(p2)
        numer = sum(tot(LF.wronskian(re, im) * weights) for re, im in rows_snapshot[1:1 + n_rec])
        return numer, wall

    def charge_units(W):
        half = T // 2
        return [W // half, W - half * (W // half)]

    def frame_momentum(e):
        """The credit line's sign current J_a = Im(conj z (z(+a) - z(-a))) at the Node from the frame alone (the neighbours' im read in the Node's frame) and the running cosine 2 cos k_a = Re((z(+a) + z(-a)) / z) as a rational."""
        f = e['frame']; re_i, im_i = f['re_start_now'], f['im_start_now']
        J = []; cosines = []
        for a in range(3):
            rp, rm = f['re_neighbours_start'][2 * a], f['re_neighbours_start'][2 * a + 1]
            ip, im_ = f['frames'][2 * a] * f['im_neighbours_start'][2 * a], f['frames'][2 * a + 1] * f['im_neighbours_start'][2 * a + 1]
            J.append(re_i * (ip - im_) - im_i * (rp - rm))
            cosines.append((re_i * (rp + rm) + im_i * (ip + im_), re_i * re_i + im_i * im_i))
        return J, cosines

    def add_rational(acc, q):
        num, d = acc; qn, qd = q
        if qd == 0: return acc
        num, d = num * qd + qn * d, d * qd
        g = gcd(abs(num), d) or 1
        return [num // g, d // g]

    for t in range(n):
        pre = snap(b)
        b.step()
        post = snap(b); mid = b.pre_close; turned = np.asarray(b.turned, dtype=bool)
        log_new = b.log[b.stack[-1]['log_from']:]
        births = [e for e in log_new if e['event'] == 'birth']; credits = [e for e in log_new if e['event'] == 'credit']; refused = [e for e in log_new if e['event'] == 'refused']
        readings['clicks']['births'] += len(births); readings['clicks']['credits'] += len(credits); readings['clicks']['refused'] += len(refused); readings['clicks']['turns'] += int(turned.sum())
        c = b.start_content; factors = b.start_factors; pace = paces.link_pace_of(gamma, c); p0 = paces.clock_of(gamma, c)
        k = b.interval
        # ---- 4. FLUX: Rule3's identity per Node and line on every row, from the pre-state and the state after the step (before the close)
        phases, odd, frames = b.start_phases, b.start_odd, b.start_frames
        W_start = sum(tot(LF.wronskian(re, im)) for re, im in pre[1:1 + n_rec])
        W_step_arr = sum(LF.wronskian(re, im) for re, im in b.stepped) if b.stepped else LF.Z(b.shape)
        W_start_arr = sum(LF.wronskian(re, im) for re, im in pre[1:1 + n_rec])
        J = [LF.Z(b.shape) for _ in range(3)]
        for re, im in pre[1:1 + n_rec]:
            for a, j_a in enumerate(LF.plane_current(re, im, frames)): J[a] = J[a] + j_a
        stress = LF.stress_parts([(pre[1 + n_rec][0].now, den)] + [(l.now, b.pairs[kk // 2][0]) for kk in range(n_rec) for l in pre[1 + kk]], b.shape)
        trace, traceless = LF.tensor_parts(stress)
        cphi = paces.rounded(pre[2 + n_rec][0].now * p0, gamma)
        forms = LF.Z(b.shape)
        for kk in range(n_rec):
            (re, im), (sre, sim) = pre[1 + kk], b.stepped[kk]
            forms = forms + (re.now * re.now - sre.now * re.before) + (im.now * im.now - sim.now * im.before)
        not_turned = ~turned
        rotate_ok = 0; rotate_of = 0; write_ok = 0; write_of = 0; first_bad = None
        light_q = None; rotated = {}  # per row: the lines' levels and remainders as the rotate alone leaves them (before the write and the swap)
        uniform = bool(int(c.min()) == int(c.max())) and all(bool(np.asarray(f == f.reshape(-1)[0]).all()) for f in factors)
        plain_turn = all(bool(np.asarray(sn == 0).all()) and bool(np.asarray(co == b.X).all()) for co, sn in phases) and all(bool(np.asarray(o == 0).all()) for o in odd) and all(bool(np.asarray(f == 1).all()) for f in frames)
        # the rows in the order of their writes' dependence: the light's rotate first (its stepped level enters the volume's form), then every row
        order = [1 + n_rec] + [ridx for ridx in range(len(pre)) if ridx != 1 + n_rec]
        for ridx in order:
            row = pre[ridx]
            if ridx == 3 + n_rec and b.hold_volume: continue
            pair = row_pairs[ridx]
            if ridx == 0: r = b.rule_phi; turn = None; flux = [2 * cphi]
            else: r = b.rule(pair, c, factors); turn = (phases, odd, frames) if 1 <= ridx <= n_rec else None; flux = None
            # the rotate: Rule3's totals from the pre-state levels and the turned arrivals (the toy's turn function on the toy's own start readings)
            totals = [r.self_coefficient * l.now - r.wall * l.before + (0 if flux is None else flux[j]) for j, l in enumerate(row)]
            links = [LF.Z(b.shape) for _ in row]
            for port, reach in enumerate(r.reaches):
                m = b.turned_arrival([across(l.now, port) for l in row], port, turn)
                totals = [tt + reach * mm for tt, mm in zip(totals, m)]
                links = [ll + reach * (mm - l.now) for ll, mm, l in zip(links, m, row)]
            mass = r.mass
            rotated[ridx] = []
            for j, l in enumerate(row):
                q = (totals[j] + l.rem) // r.wall; rem_after = totals[j] + l.rem - r.wall * q
                rotated[ridx].append((q, rem_after))
                after = mid[ridx][j]
                inc = after.now - q  # the write's quotient as the step left the level (0 where the line is not written)
                resid = r.wall * (after.now - inc - 2 * l.now + l.before) + (after.rem - l.rem) - (links[j] - mass * l.now) - (0 if flux is None else flux[j])
                good = np.asarray(resid == 0) & np.asarray(after.before == l.now) & np.asarray(after.rem == rem_after)
                rotate_of += int(not_turned.sum()); rotate_ok += int((good & not_turned).sum())
                if ridx == 1 + n_rec:
                    light_q = q; light_pre_line = pre[1 + n_rec][0]
                    forms = forms + (light_pre_line.now * light_pre_line.now - light_q * light_pre_line.before)  # the light's form at its stepped level, the toy's line
                if l.wr is not None:
                    if ridx == 1 + n_rec: numer = W_step_arr - W_start_arr
                    elif ridx == 2 + n_rec: numer = 2 * W_step_arr if j == 0 else J[j - 1]
                    elif ridx == 3 + n_rec: numer = (4 * pre[3 + n_rec][0].now * (forms * 54 * den * gamma ** 2 - trace * p0 * p0) * p0) if j == 0 else (traceless[j - 1] * p0 * p0 if j <= 3 else LF.Z(b.shape))
                    else: numer = LF.Z(b.shape)
                    wok = np.asarray(l.wwall * inc + after.wr - l.wr == numer)
                    write_of += int(not_turned.sum()); write_ok += int((wok & not_turned).sum())
                    if first_bad is None and not bool((wok | turned).all()):
                        bad = tuple(int(x) for x in next(zip(*np.nonzero(~wok & not_turned)))); first_bad = (bad, 'write %s line %d' % (row_names[ridx], j))
                else:
                    wok = np.asarray(inc == 0); write_of += int(not_turned.sum()); write_ok += int((wok & not_turned).sum())
                if first_bad is None and not bool((good | turned).all()):
                    bad = tuple(int(x) for x in next(zip(*np.nonzero(~good & not_turned)))); first_bad = (bad, 'rotate %s line %d, residual %d' % (row_names[ridx], j, int(resid[bad])))
        L['FLUX Rule3 identity per Node and line, residual 0'].count(rotate_ok == rotate_of, k, None if first_bad is None else first_bad[0], 'residual not 0 at %d of %d (Node, line): %s' % (rotate_of - rotate_ok, rotate_of, first_bad))
        L['FLUX the write book per Node and line'].count(write_ok == write_of, k, None if first_bad is None else first_bad[0], 'the write book off at %d of %d (Node, line): %s' % (write_of - write_ok, write_of, first_bad))
        # the exchange at the turned Nodes: every line the pre-state exchanged and complemented
        ex_ok = True; ex_bad = None
        if turned.any():
            for l_pre, l_mid, im in zip(flat(pre), flat(mid), b.is_im()):
                sgn = -1 if im else 1
                good = np.asarray(l_mid.now == sgn * l_pre.before) & np.asarray(l_mid.before == sgn * l_pre.now) & np.asarray(l_mid.rem == (l_pre.rem if im else l_pre.wall - 1 - l_pre.rem))
                if l_pre.wr is not None: good = good & np.asarray(l_mid.wr == l_pre.wwall - 1 - l_pre.wr)
                if not bool((good | ~turned).all()):
                    ex_ok = False; ex_bad = tuple(int(x) for x in next(zip(*np.nonzero(~good & turned)))); break
        L['FLUX the exchange at every turned Node'].count(ex_ok, k, ex_bad, 'turned Nodes %d, a line not the pre-state exchanged' % int(turned.sum()))
        # the light's own current antisymmetric on every Link, and its linear sum L moved by the pairing term and the write alone
        light_pre = pre[1 + n_rec][0]; light_mid = mid[1 + n_rec][0]
        anti = True
        for a in range(3):
            Fp = b.link_current(light_pre, 2 * a); Fm = b.link_current(light_pre, 2 * a + 1)
            # F(i, +a) read at i and F(j, -a) read at j = i + a: the same Link from its two ends
            if not bool(np.asarray(Fp + across(Fm, 2 * a) == 0).all()): anti = False
        L['FLUX F_ij = -F_ji on every Link'].count(anti, k, None, 'the light current not antisymmetric on a Link')
        r_l = b.rule((den, den), c, factors)
        # L per Node, w (now - before) + r, summed over the untouched Nodes (a turned Node ends at its pre-state exchanged, the step's output discarded there)
        L_node_pre = w * (light_pre.now - light_pre.before) + light_pre.rem; L_node_mid = w * (light_mid.now - light_mid.before) + light_mid.rem
        pairing_node = LF.Z(b.shape)
        for port, reach in enumerate(r_l.reaches): pairing_node = pairing_node + reach * (across(light_pre.now, port) - light_pre.now)
        inc_light = light_mid.now - light_q
        dL = tot(np.where(not_turned, L_node_mid - L_node_pre, 0)); pairing = tot(np.where(not_turned, pairing_node, 0)); written = tot(np.where(not_turned, w * inc_light, 0))
        L['FLUX the light L moved by the pairing and the write alone'].count(dL == pairing + written, k, None, 'dL %d against pairing %d + write %d (turned Nodes %d left out)' % (dL, pairing, written, int(turned.sum())))
        # ---- 2. MOMENTUM on the board: the rotate to the floor (exactly, at uniform plain paces: dP_a w = 2 num SUM (r' - r)(now(i+a) - now(i-a)); within the floors' bound otherwise, the paces' gradient named), the write's and the exchange's momentum read, the close exact against the credit lines
        for ridx in [1 + n_rec] + list(range(1, 1 + n_rec)):
            num = row_nums[ridx]
            P_pre, P_mid, P_post = momentum(pre[ridx], num), momentum(mid[ridx], num), momentum(post[ridx], num)
            rot_lines = [LF.Line(q, l.now, rem_after, l.wall) for (q, rem_after), l in zip(rotated[ridx], pre[ridx])]
            P_rot = momentum(rot_lines, num)
            floors = [2 * num * sum(tot((rem_after - l.rem) * (across(l.now, 2 * a) - across(l.now, 2 * a + 1))) for (q, rem_after), l in zip(rotated[ridx], pre[ridx])) for a in range(3)]
            bound = floor_bound(pre[ridx], num)
            exact_floor = uniform and (ridx > n_rec or plain_turn)
            if exact_floor:
                held_ = all((P_rot[a] - P_pre[a]) * w == floors[a] for a in range(3))
                L['MOMENTUM the rotate to the floor, exact at uniform plain paces (dP_a w = 2 num SUM (r\' - r)(now(i+a) - now(i-a)))'].count(held_, k, None, '%s dP_rotate x w %s against the floors identity %s' % (row_names[ridx], [(P_rot[a] - P_pre[a]) * w for a in range(3)], floors))
            else:
                # at varying paces the law's change is the paces' gradient (the force law), at a folded Link the turn's work: a reading, no break; counted within or beyond the floors' bound
                within = all(abs(P_rot[a] - P_pre[a]) <= bound[a] for a in range(3))
                readings['momentum at varying paces or folded Links: rows within / beyond the floors bound (the force law)'][0 if within else 1] += 1
                if not within and readings['momentum first row beyond the floors bound'] is None:
                    readings['momentum first row beyond the floors bound'] = {'interval': k, 'row': row_names[ridx], 'dP_rotate': [P_rot[a] - P_pre[a] for a in range(3)], 'floors bound': bound, 'paces': 'uniform' if uniform else 'varying', 'turn': 'plain' if plain_turn else 'folded'}
            readings['momentum moved by the step: rotate, write (W-S1 and the held writes), exchange at the turns (abs sums per axis)'][0] = [x + abs(P_rot[a] - P_pre[a]) for a, x in enumerate(readings['momentum moved by the step: rotate, write (W-S1 and the held writes), exchange at the turns (abs sums per axis)'][0])]
            if turned.any():
                # at a turned Node the state is the pre-state exchanged, not the rotate's output: the exchange's move read as the rest
                written_lines = [LF.Line(np.where(turned, q, mid_l.now), l.now, rem_after, l.wall) for (q, rem_after), l, mid_l in zip(rotated[ridx], pre[ridx], mid[ridx])]
            else: written_lines = mid[ridx]
            P_written = momentum(written_lines, num)
            readings['momentum moved by the step: rotate, write (W-S1 and the held writes), exchange at the turns (abs sums per axis)'][1] = [x + abs(P_written[a] - P_rot[a]) for a, x in enumerate(readings['momentum moved by the step: rotate, write (W-S1 and the held writes), exchange at the turns (abs sums per axis)'][1])]
            readings['momentum moved by the step: rotate, write (W-S1 and the held writes), exchange at the turns (abs sums per axis)'][2] = [x + abs(P_mid[a] - P_written[a]) for a, x in enumerate(readings['momentum moved by the step: rotate, write (W-S1 and the held writes), exchange at the turns (abs sums per axis)'][2])]
            if t == 0: readings['momentum P_a per row start/end'][row_names[ridx]] = [P_pre, None]
            readings['momentum P_a per row start/end'][row_names[ridx]][1] = P_post
            if ridx == 1 + n_rec and (births or credits):
                for a in range(3): readings['momentum written by the clicks per axis (light, planes)'][0][a] += P_post[a] - P_mid[a]
            if ridx <= n_rec and births:
                for a in range(3): readings['momentum written by the clicks per axis (light, planes)'][1][a] += P_post[a] - P_mid[a]
        # the close's momentum from the credit lines alone: a take of d levels at i moves P_a by 2 num d (before_(i-a) - before_(i+a)); a lay of A on re.now the same, of s A on im.before by 2 num s A (now_(i+a) - now_(i-a))
        if births or credits:
            expected = {ridx: [0, 0, 0] for ridx in [1 + n_rec] + list(range(1, 1 + n_rec))}
            takes = {}
            for e in births + credits:
                at = tuple(e['node']); now_was = e['light_now_was']; before = int(light_mid.before[at]); toward = 1 if before > now_was else -1
                takes[at] = toward * e['levels']
            for at, d in takes.items():
                for a in range(3):
                    minus = tuple((at[x] - (1 if x == a else 0)) % b.cube for x in range(3)); plus = tuple((at[x] + (1 if x == a else 0)) % b.cube for x in range(3))
                    expected[1 + n_rec][a] += 2 * den * d * (int(light_mid.before[minus]) - int(light_mid.before[plus]))
            for e in births:
                s_ = e['line_pair']; A = e['amplitude']; num = b.pairs[s_][0]
                for sense, rec, where in ((-1, 2 * s_, tuple(e['minus'])), (1, 2 * s_ + 1, tuple(e['plus']))):
                    re, im = mid[1 + rec]
                    for a in range(3):
                        minus = tuple((where[x] - (1 if x == a else 0)) % b.cube for x in range(3)); plus = tuple((where[x] + (1 if x == a else 0)) % b.cube for x in range(3))
                        expected[1 + rec][a] += 2 * num * A * (int(re.before[minus]) - int(re.before[plus]))
                        expected[1 + rec][a] += 2 * num * sense * A * (int(im.now[plus]) - int(im.now[minus]))
            exact = True; bad = None
            for ridx, exp in expected.items():
                got = [momentum(post[ridx], row_nums[ridx])[a] - momentum(mid[ridx], row_nums[ridx])[a] for a in range(3)]
                if got != exp: exact = False; bad = (row_names[ridx], got, exp); break
            L['MOMENTUM the close wrote what the credit lines book (dP_a exact)'].count(exact, k, None, 'row %s: the board dP %s against the credit lines %s' % bad if bad else '')
            for e in credits:
                Jc, cosines = frame_momentum(e)
                for a in range(3):
                    readings['credits J_a sum per axis'][a] += Jc[a]
                    readings['credits running cosine 2cos k_a sum (numerator, denominator) per axis'][a] = add_rational(readings['credits running cosine 2cos k_a sum (numerator, denominator) per axis'][a], cosines[a])
        # ---- 3. CHARGE: the Wronskian over the board, the step's drift within the remainders' and the turn's roundings (the rotate alone, at the start's weights 1 / p_i^2), the close's exactness, the births' pairs
        W_pre, W_mid, W_post = W_start, wronskian_total(mid), wronskian_total(post)
        rot_planes = [[LF.Line(q, l.now, rem_after, l.wall) for (q, rem_after), l in zip(rotated[1 + kk], pre[1 + kk])] for kk in range(n_rec)]
        W_rot = sum(tot(LF.wronskian(re, im)) for re, im in rot_planes)
        wn_pre, wall_pre = weighted_wronskian(pre, pace); wn_rot, wall_rot = weighted_wronskian([None] + rot_planes, pace)
        # every rotated level is the rational step's within 3 levels (the carried remainder below one, the two turned-arrival roundings at most one each over the six Links), so |dW_i| <= 3 (|re_now_i| + |im_now_i|)
        p2 = np.vectorize(lambda p: int(p) * int(p) + (1 if int(p) == 0 else 0), otypes=[object])(np.asarray(pace, dtype=object))
        weights = np.vectorize(lambda v: wall_pre // int(v), otypes=[object])(p2)
        bound_w = sum(tot(3 * (np.vectorize(abs, otypes=[object])(re.now) + np.vectorize(abs, otypes=[object])(im.now)) * weights) for re, im in pre[1:1 + n_rec])
        readings['W drift per step (abs sum, the rotate)'] += abs(W_rot - W_pre)
        readings['W weighted drift (abs sum of numerators over the lcm wall, the rotate)'] += abs(wn_rot - wn_pre)
        L['CHARGE the rotate keeps the weighted W within the remainders and the turn roundings'].count(abs(wn_rot - wn_pre) <= bound_w, k, None, 'weighted dW numerator %d against the bound %d over the wall %d; plain W %d -> %d (in T div 2 units %s -> %s)' % (wn_rot - wn_pre, bound_w, wall_pre, W_pre, W_rot, charge_units(W_pre), charge_units(W_rot)))
        readings['charge in T div 2 units (quotient, remainder) start/end'][1] = charge_units(W_post)
        if t == 0: readings['charge in T div 2 units (quotient, remainder) start/end'][0] = charge_units(W_pre)
        L['CHARGE the board W unchanged at the close'].count(W_post == W_mid, k, None, 'W after the step %d, after the close %d, births %d' % (W_mid, W_post, len(births)))
        for e in births:
            s_ = e['line_pair']; minus, plus = tuple(e['minus']), tuple(e['plus'])
            dW = 0; parts = []
            for rec, where in ((2 * s_, minus), (2 * s_ + 1, plus)):
                re0, im0 = mid[1 + rec]; re1, im1 = post[1 + rec]
                d = int(LF.wronskian(re1, im1)[where]) - int(LF.wronskian(re0, im0)[where]); dW += d; parts.append(d)
            L['CHARGE every birth W(-) + W(+) = 0'].count(dW == 0 and sum(e['senses']) == 0, k, e['node'], 'the two children W %s, senses %s, amplitude %d' % (parts, e['senses'], e['amplitude']))
        # ---- 1. ENERGY in the clicks: the take read from the board, the least count, taken >= booked, taken == booked, the pair's two quanta
        r_light_close = b.rule((den, den), c, b.link_factors())  # the close reads the factors as the step left the axis lines (the toy's close)
        taken_sum = 0
        last_click = {}  # several records may click at one Node in one close, each take from the light as the one before left it: the board's level is the last click's
        for e in births + credits: last_click[tuple(e['node'])] = e
        for e in births + credits:
            at = tuple(e['node']); now = e['light_now_was']; before = int(light_mid.before[at]); t_ = 1 if before > now else -1
            S = int(np.asarray(r_light_close.self_coefficient)[at]); Lsum = 0
            for (axis, side), reach in zip(AX, r_light_close.reaches):
                nb = tuple((at[x] + (side if x == axis else 0)) % b.cube for x in range(3)); Lsum += int(np.asarray(reach)[at]) * int(light_mid.before[nb])
            pc = int(np.asarray(pace, dtype=object)[at]); Wi = 2 * pc * pc * G * G + (1 if pc == 0 else 0)
            def fall(s_): return (w * (now * now - (now + t_ * s_) ** 2) - t_ * s_ * (S * before + Lsum)) // Wi
            levels = e['levels']; booked = e['booked'] if e['event'] == 'birth' else b.units[e['line'] // 2]
            if e['event'] == 'birth' and e['children_at_node'] > 1: booked = e['booked']  # the walls summed over the children at the Node, logged on each
            read = fall(levels); taken = e['taken']
            level_ok = int(post[1 + n_rec][0].now[at]) == now + t_ * levels if last_click[at] is e else True
            L['ENERGY the take read from the board equals the credit line'].count(read == taken and level_ok, k, at, 'fall read %d, credit line taken %d, light now %d -> %d by %d levels' % (read, taken, now, int(post[1 + n_rec][0].now[at]), levels))
            L['ENERGY the take is the least count paying the walls'].count(levels >= 1 and (levels == 1 or fall(levels - 1) < booked) and read >= booked, k, at, 'levels %d, fall at levels - 1 %d, walls %d' % (levels, fall(levels - 1) if levels > 1 else 0, booked))
            L['ENERGY taken pays booked (taken >= booked)'].count(taken >= booked, k, at, 'taken %d, booked %d' % (taken, booked))
            L['ENERGY the exact take (taken == booked)'].count(taken == booked, k, at, 'taken %d, booked %d, excess %d (%s of W_c)' % (taken, booked, taken - booked, [(taken - booked) // b.unit_light, (taken - booked) % b.unit_light]))
            if e['event'] == 'birth': taken_sum += taken if e['children_at_node'] == 1 else 0
            else: taken_sum += taken
            readings['excess taken - booked (share units)'] += (taken - booked) if (e['event'] == 'credit' or e['children_at_node'] == 1) else 0
        seen_nodes = set()
        for e in births:
            at = tuple(e['node'])
            if e['children_at_node'] > 1 and at not in seen_nodes:
                seen_nodes.add(at); taken_sum += e['taken']; readings['excess taken - booked (share units)'] += e['taken'] - e['booked']
        for e in births:
            s_ = e['line_pair']; r = b.rule(b.pairs[s_], c, factors); quanta = []
            for rec, where in ((2 * s_, tuple(e['minus'])), (2 * s_ + 1, tuple(e['plus']))):
                re0, im0 = mid[1 + rec]; re1, im1 = post[1 + rec]
                s1 = int(b.share(re1, r, pace)[where]) + int(b.share(im1, r, pace)[where]); s0 = int(b.share(re0, r, pace)[where]) + int(b.share(im0, r, pace)[where])
                quanta.append((s1 - s0) // b.units[s_])
                readings['children laid at 1 / 2 / more quanta of their unit'][0 if (s1 - s0) // b.units[s_] == 1 else 1 if (s1 - s0) // b.units[s_] == 2 else 2] += 1
            L['ENERGY the born pair carries two whole quanta (one per child, the book)'].count(all(q == 1 for q in quanta), k, e['node'], 'the two children laid %s whole quanta of the unit %d where the book is 1 and 1 (amplitude %d)' % (quanta, b.units[s_], e['amplitude']))
        # ---- 5. COUNT: the close's book exact, the quanta before and after
        book_ok = True; book_bad = None
        expected_rows = [[l.copy() for l in row] for row in mid]
        light_exp = expected_rows[1 + n_rec][0]
        for e in births + credits:
            at = tuple(e['node']); now = e['light_now_was']; before = int(light_mid.before[at]); t_ = 1 if before > now else -1
            light_exp.now[at] = now + t_ * e['levels']
        for e in births:
            s_ = e['line_pair']; A = e['amplitude']
            for sense, rec, where in ((-1, 2 * s_, tuple(e['minus'])), (1, 2 * s_ + 1, tuple(e['plus']))):
                re, im = expected_rows[1 + rec]; re.now[where] = re.now[where] + A; im.before[where] = im.before[where] + sense * A
        for ridx, (row_e, row_p) in enumerate(zip(expected_rows, post)):
            for j, (le, lp) in enumerate(zip(row_e, row_p)):
                for slot in ('now', 'before', 'rem', 'wr'):
                    xe, xp = getattr(le, slot), getattr(lp, slot)
                    if xe is None: continue
                    if not bool(np.asarray(xe == xp).all()):
                        book_ok = False; book_bad = (row_names[ridx], j, slot, tuple(int(x) for x in next(zip(*np.nonzero(np.asarray(xe != xp)))))); break
                if not book_ok: break
            if not book_ok: break
        L['COUNT the close book exact (every change a logged take or lay)'].count(book_ok, k, None if book_bad is None else book_bad[3], 'a change not in the log: %s' % (book_bad,))
        if births or credits or t == 0 or t == n - 1:
            lq_mid, rq_mid, sl_mid, sr_mid = shares_in_quanta(mid, c, factors, pace); lq_post, rq_post, sl_post, sr_post = shares_in_quanta(post, c, factors, pace)
            if t == 0: lq_pre, rq_pre, _a, _b = shares_in_quanta(pre, c, factors, pace); readings['light quanta (W_c) start/end'][0] = lq_pre; readings['records quanta start/end'][0] = rq_pre
            readings['light quanta (W_c) start/end'][1] = lq_post; readings['records quanta start/end'][1] = rq_post
            if births or credits:
                intervals_with_clicks.append({'i': k, 'births': len(births), 'credits': len(credits), 'light quanta before/after the close': [lq_mid, lq_post], 'light share fall at the close': sl_mid - sl_post, 'taken sum (credit lines)': taken_sum, 'records quanta before/after the close': [rq_mid, rq_post], 'records share rise at the close': [s1 - s0 for s0, s1 in zip(sr_mid, sr_post)], 'booked (births x 2 units + credits x 1 unit)': sum(e['booked'] for e in births if e['children_at_node'] == 1) + sum(b.units[e['line'] // 2] for e in credits), 'turned': int(turned.sum())})
        hashes.append(state_hash(b))
    # ---- 5. the run back from the end to the seed
    exact = 0; first_bad = None
    for kk in range(n):
        b.step_back()
        if state_hash(b) == hashes[n - 1 - kk]: exact += 1
        elif first_bad is None: first_bad = n - 1 - kk
    L['COUNT the run back exact (the board bit for bit)'].count(exact == n, first_bad, None, 'exact %d of %d, first mismatch at interval %s' % (exact, n, first_bad))
    L['COUNT the run back exact (the board bit for bit)'].held = exact; L['COUNT the run back exact (the board bit for bit)'].of = n
    excess = readings['excess taken - booked (share units)']
    readings['excess in W_c (quotient, remainder of the sum)'] = [excess // b.unit_light, excess % b.unit_light]
    # ---- 6. THE 48 on the clicks: the credits and the refusals through the image (the births the toy's cube48_test covers), on the 3-cube image
    law48 = Law('THE 48 on the clicks (births, credits, refusals through the image; the 3-cube image of the world, %d intervals)' % min(n, 30))
    cube = 3; n48 = min(n, 30)

    def signed_permutations():
        axes = range(3)
        return [np.array([[s[a] if pi[a] == bb else 0 for a in axes] for bb in axes]) for pi in itertools.permutations(axes) for s in itertools.product((1, -1), repeat=3)]

    def image(m, node):
        v = m @ np.array(node, dtype=int); return tuple(int(x) % cube for x in v)

    def world_image(wd, m):
        w2 = copy.deepcopy(wd); w2['shape'] = [cube, cube, cube]
        for lay in w2.get('seed', []):
            for key in ('at', 'centre'):
                if key in lay: lay[key] = list(image(m, tuple(lay[key])))
        if 'well' in w2.get('control', {}): w2['control']['well']['at'] = list(image(m, tuple(w2['control']['well']['at'])))
        w2['detectors'] = [list(image(m, tuple(d))) for d in w2.get('detectors', [])]
        return w2

    def clicks_of(bb, m):
        births = sorted((e['i'], image(m, e['node']), e['line_pair'], image(m, e['minus']), image(m, e['plus']), e['taken'], e['booked'], e['levels'], e['amplitude']) for e in bb.log if e['event'] == 'birth')
        credits = sorted((e['i'], image(m, e['node']), e['line'], e['taken'], e['levels'], e['beat'], e['proper'], e['sense']) for e in bb.log if e['event'] == 'credit')
        # an orientation refusal names its Link from the lower end (the toy's loop over the +a Links): compared as the Link, the two ends unordered
        refused = sorted((e['i'], tuple(sorted((image(m, e['node']), image(m, e['link'])))) if 'link' in e else (image(m, e['node']),), e['cause']) for e in bb.log if e['event'] == 'refused')
        return births, credits, refused

    def run48(wd):
        bb = LF.Lean(universe, wd)
        for _ in range(n48): bb.step()
        return bb
    try:
        base = run48(world_image(world, np.eye(3, dtype=int)))
        base_clicks = clicks_of(base, np.eye(3, dtype=int))
        counts48 = {'births': len(base_clicks[0]), 'credits': len(base_clicks[1]), 'refused': len(base_clicks[2]), 'images holding births/credits/refusals': [0, 0, 0]}
        for m in signed_permutations():
            other = run48(world_image(world, m))
            # the image's clicks read back through the inverse image equal the base's clicks; a signed permutation's inverse is its transpose (integers alone)
            inv = np.array(m.T, dtype=int)
            L48 = clicks_of(other, inv)
            same = [L48[q] == base_clicks[q] for q in range(3)]
            for q in range(3): counts48['images holding births/credits/refusals'][q] += int(same[q])
            law48.count(all(same), None, None, 'image %s apart in %s' % (m.tolist(), [nm for nm, s in zip(('births', 'credits', 'refused'), same) if not s]))
        law48.notes.append(counts48)
    except ValueError as err:
        law48.count(False, None, None, 'the 3-cube image refused: %s' % err)
    # ---- the report
    all_ok = True
    for name in L:
        print(L[name].line()); all_ok = all_ok and L[name].ok()
        for brk in L[name].breaks[1:]:
            print('  also at interval %s, Node %s: %s' % (brk[0], None if brk[1] is None else tuple(int(x) for x in brk[1]), brk[2]))
    print(law48.line() + ('  clicks of the base run %s' % law48.notes[0] if law48.notes else '')); all_ok = all_ok and law48.ok()
    print('REACH forward and backward: covered by the toy\'s reach_test.py (both halves), nothing added here')
    print(json.dumps({'readings': readings}))
    for row in intervals_with_clicks[:12]: print(json.dumps({'interval with clicks': row}))
    if len(intervals_with_clicks) > 12: print(json.dumps({'intervals with clicks': len(intervals_with_clicks), 'shown': 12}))
    print('VERDICT: %s' % ('every law holds' if all_ok else 'a law is broken (named above)'))
    return 0 if all_ok else 1


if __name__ == '__main__':
    sys.exit(main())
