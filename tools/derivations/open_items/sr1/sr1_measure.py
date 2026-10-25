"""sr1: the measurements on the flagged copy lean_sr1.py (integers only; exact fractions in the Zeeman reading, named).

Sets (python sr1_measure.py <set> [cube] [intervals] [back]):
  zeeman : one shape-8 quantum at rest (width 2) in a held uniform curl (A_x = -B0 (y - c): Phi_z = 2 B0), laid spin up / spin down
           along z, and a plane of the same pair beside them; the reading: the exact ratio (x_next + x_before) / x_now of the row's
           lines at the centre at the intervals 1..3 (2 cos omega, a fraction), the upward crossings of the row's sum-line at the
           centre over the run, the body credits' beats; the controls with no field and with the Pauli term off.
  sg     : a neutral shape-8 packet (N quanta, both senses, the unpolarised spin up + down along z) in the held gradient
           B_z = B0 + b (z - c) (A_x = -(y - c)(B0 + b (z - c))): the credits per z by the sign of the spin density s_z, the
           centroids per spin component (credits and board), the control with no field, the second gradient along y.
  images : the 48 on the clicks: the seed (the spin vector by M(g)), the field (a polar vector) carried through each signed
           permutation; the credits compared through the image with the spin signs carried as an axial vector.
  pile   : two shape-8 quanta laid at one Node, like spins against opposite spins: the share at the centre in units.
  reach  : a change of the odd line two Links from a Node leaves that Node's interval bit for bit.
Outputs under out/<set>_*.json and the log.
"""
from __future__ import annotations
import sys, os, json, copy, itertools, hashlib
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
from lean_sr1 import Lean, SR1, gform8, matvec8, Line, wronskian
sys.set_int_max_str_digits(0)
OUT = os.path.join(HERE, 'out'); WORLDS = os.path.join(OUT, 'worlds')
UNI = json.load(open(os.path.join(WORLDS, 'universe_sr1.json')))
ROW8 = 6  # the shape-8 row's index in the universe file; the heavy lift's plane is row 2


def world(cube, intervals, seeds, control=None):
    w = {'universe': 'universe_sr1.json', 'shape': [cube] * 3, 'intervals': intervals, 'seed': [{'lay': 'sea', 'row': 0}] + seeds}
    if control: w['control'] = control
    return w


def held(line, at, B0, b, across, along):
    return {'held_potential': [{'line': line, 'at': list(at), 'field': 'sg', 'across': across, 'along': along, 'B0': B0, 'b': b}]}


def run(w, back=0, centre=None, watch=None, complement=False):
    """One world through the copy: the record (counts, credits, census, run back) and, where `watch` names a row index, the
    8 lines' levels at `centre` after every interval (for the Zeeman ratio) and the upward crossings of the sum-line there."""
    b = Lean(UNI, w); intervals = w['intervals']; hashes = []; levels = []; crossings = []; maxbits = 0
    rec = None if watch is None else b.records().index(b.by_index[watch])
    if complement and rec is not None:  # the 2 pi turn's image (-I on the lines): the symmetric lay's rule, every negated line's remainder its complement w - 1 - r (The cube's symmetry)
        for l in b.records()[rec].lines: l.rem = l.wall - 1 - l.rem
    if rec is not None: levels.append([int(l.now[centre]) for l in b.records()[rec].lines] + [int(l.before[centre]) for l in b.records()[rec].lines])
    for t in range(intervals):
        if back and t >= intervals - back: hashes.append(b.state_hash())
        b.step(); maxbits = max(maxbits, b.census()[1])
        if rec is not None:
            ls = b.records()[rec].lines
            levels.append([int(l.now[centre]) for l in ls] + [int(l.before[centre]) for l in ls])
            sn, sb = sum(int(l.now[centre]) for l in ls), sum(int(l.before[centre]) for l in ls)
            if sb < 0 <= sn: crossings.append(b.interval)
    credits = [e for e in b.log if e['event'] == 'credit']; births = [e for e in b.log if e['event'] == 'birth']
    n_int, bits = b.census()
    out = {'counts': {k: int(v) for k, v in b.counts.items()}, 'credits': credits, 'births': len(births), 'births_senses_sum': sum(sum(1 if x > 0 else -1 if x < 0 else 0 for x in e['W_children']) for e in births),
           'integers': n_int, 'max_bits_state': maxbits, 'max_transient_bits': b.max_transient, 'turns': b.counts['turns'], 'levels_at_centre': levels, 'crossings': crossings}
    if back:
        exact = 0
        for k in range(back):
            b.step_back(); exact += (b.state_hash() == hashes[back - 1 - k])
        out['run_back'] = {'intervals': back, 'exact': exact}
    return out, b


def ratios(levels, t):
    """The exact 2 cos omega reading at the interval t: (x_(t+1) + x_(t-1)) / x_t per line (a fraction, named), the lines with x_t = 0 skipped."""
    found = []
    for k in range(8):
        a, bb, c = levels[t - 1][k], levels[t][k], levels[t + 1][k]
        if bb != 0: found.append(str(Fr(a + c, bb)))
        else: found.append(None)
    return found


def zeeman(cube, intervals, back, B0):
    c = cube // 2; cen = (c,) * 3; table = {}
    plane_lay = {'lay': 'at', 'row': 2, 'centre': list(cen), 'width': 2, 'quanta': 1, 'sense': 1}
    for name, spin, field, pauli in (('up, B, pauli', 'spin_up_z', True, True), ('down, B, pauli', 'spin_down_z', True, True), ('up, no field', 'spin_up_z', False, True), ('down, no field', 'spin_down_z', False, True),
                                     ('up, B, no pauli', 'spin_up_z', True, False), ('down, B, no pauli', 'spin_down_z', True, False)):
        control = held(1, cen, B0, 0, 1, 2) if field else {}
        control['pauli'] = pauli; control['spinor_turn'] = 'none'
        w = world(cube, intervals, [{'lay': 'at', 'row': ROW8, 'centre': list(cen), 'width': 2, 'quanta': 1, 'sense': 1, 'spin': spin}], control)
        o, b = run(w, back, cen, ROW8)
        lv = o['levels_at_centre']
        table[name] = {'ratios t=1': ratios(lv, 1), 'ratios t=2': ratios(lv, 2), 'milli 2cos (line 0 or 4) t=1..4': [str(Fr(lv[t - 1][k] + lv[t + 1][k], lv[t][k]) * 1000 // 1) if lv[t][k] else None for t in range(1, 5) for k in (0, 4) if lv[t][k]][:4],
                       'crossings of the sum-line at the centre': o['crossings'], 'crossing count': len(o['crossings']), 'credits': len(o['credits']), 'beats': sorted(set(e['beat'] for e in o['credits'])), 'run_back': o.get('run_back'), 'integers': o['integers'], 'bits': o['max_bits_state'], 'transient': o['max_transient_bits'], 'turns': o['turns']}
        print(json.dumps({name: table[name]}), flush=True)
    for name, field in (('plane, B', True), ('plane, no field', False)):
        control = held(1, cen, B0, 0, 1, 2) if field else {}
        w = world(cube, intervals, [plane_lay], control)
        o, b = run(w, back, cen, 2)
        lv = o['levels_at_centre']
        table[name] = {'ratios t=1 (re, im)': [str(Fr(lv[0][k] + lv[2][k], lv[1][k])) if lv[1][k] else None for k in range(2)], 'ratios t=2': [str(Fr(lv[1][k] + lv[3][k], lv[2][k])) if lv[2][k] else None for k in range(2)],
                       'crossings of the sum-line (re + im) at the centre': o['crossings'], 'crossing count': len(o['crossings']), 'credits': len(o['credits']), 'run_back': o.get('run_back'), 'integers': o['integers'], 'bits': o['max_bits_state']}
        print(json.dumps({name: table[name]}), flush=True)
    table['expected'] = {'2 cos omega_0 = 2 num / den': str(Fr(2 * 506298091, 1655909141)), 'Phi_z = 2 B0': 2 * B0, 'the Pauli shift of 2 cos omega, +- (nu / w) Phi = +- num Phi / (3 den Gamma)': str(Fr(506298091 * 2 * B0, 3 * 1655909141 * 1000))}
    json.dump(table, open(os.path.join(OUT, 'zeeman_c%d_i%d_B%d.json' % (cube, intervals, B0)), 'w'), indent=1)


def sg_read(o, cube, axis, spin_axis):
    """The credits per position along `axis`, by the sign of the spin density along `spin_axis`; the centroids (thousandths of a Link) per component."""
    per = {}; cen = {}
    for s in (1, -1, 0):
        cs = [e for e in o['credits'] if e.get('spin_sign', [0, 0, 0])[spin_axis] == s]
        per[s] = [sum(1 for e in cs if e['node'][axis] == z) for z in range(cube)]
        cen[s] = None if not cs else sum(e['node'][axis] for e in cs) * 1000 // len(cs)
    return {'credits': len(o['credits']), 'per position by spin sign (+1, -1, 0)': per, 'centroid milli by spin sign': cen, 'senses': {s: sum(1 for e in o['credits'] if e['sense'] == s) for s in (1, -1, 0)}, 'beats': sorted(set(e['beat'] for e in o['credits']))}


def board_read(b, axis, spin_axis):
    """The board: the row's spin density along spin_axis at every Node, its positive and negative parts' centroids along axis (thousandths)."""
    rec = b.records().index(b.by_index[ROW8]); W, s, sw = b.bilinears8(b.records()[rec].lines)
    sa = s[spin_axis]; idx = np.indices(b.shape)[axis]; out = {}
    for name, m in (('s>0', np.where(sa > 0, sa, 0)), ('s<0', np.where(sa < 0, -sa, 0))):
        tot = int(sum(int(x) for x in m.reshape(-1)))
        out[name] = None if tot == 0 else int(sum(int(w_) * int(x) for w_, x in zip(m.reshape(-1), idx.reshape(-1)))) * 1000 // tot
    out['W total'] = int(sum(int(x) for x in W.reshape(-1))); out['s total'] = [int(sum(int(x) for x in sa_.reshape(-1))) for sa_ in s]
    return out


def sg(cube, intervals, back, N, B0, bgrad):
    c = cube // 2; cen = (c,) * 3; table = {}
    unpol = [1, -1, 0, 0, 2, 0, 0, 0]  # spin up + spin down along z: s_z = 0 at every Node (the two G-orthogonal)
    for name, control, axis, spin_axis in (('control, no field', {}, 2, 2), ('gradient along z (A_x = -(y-c)(B0 + b (z-c)))', held(1, cen, B0, bgrad, 1, 2), 2, 2),
                                           ('gradient along y (A_z = -(x-c)(B0 + b (y-c)))', held(3, cen, B0, bgrad, 0, 1), 1, 1), ('uniform B (b = 0)', held(1, cen, B0, 0, 1, 2), 2, 2)):
        control = dict(control); control['pauli'] = True; control['spinor_turn'] = 'none'
        w = world(cube, intervals, [{'lay': 'at', 'row': ROW8, 'centre': list(cen), 'width': 3, 'quanta': N, 'spin': unpol}], control)
        o, b = run(w, back, cen, ROW8)
        table[name] = {'clicks': sg_read(o, cube, axis, spin_axis), 'board': board_read(b, axis, spin_axis), 'run_back': o.get('run_back'), 'counts': o['counts'], 'integers': o['integers'], 'bits': o['max_bits_state'], 'transient': o['max_transient_bits'], 'births': o['births'], 'births_senses_sum': o['births_senses_sum']}
        print(json.dumps({name: table[name]}), flush=True)
    json.dump(table, open(os.path.join(OUT, 'sg_c%d_i%d_N%d_B%d_b%d.json' % (cube, intervals, N, B0, bgrad)), 'w'), indent=1)


def signed_perms():
    return [np.array([[s[a] if pi[a] == bb else 0 for a in range(3)] for bb in range(3)]) for pi in itertools.permutations(range(3)) for s in itertools.product((1, -1), repeat=3)]


def images(cube, intervals, B0, bgrad, N=60):
    """The 48 images: g a signed permutation (det +1 a rotation, det -1 a rotation times the inversion); the seed's spin vector
    carried by M(g_rot) (the lift of the rotation part; the inversion acts as +1 on the lines), the odd line as a polar vector,
    the spin signs compared as an axial vector (det g)."""
    c = cube // 2; cen = (c,) * 3
    spin0 = [1, -1, 0, 0, 2, 0, 0, 0]
    perm_of = {k: v for k, v in SR1['perm48'].items()}
    def R_of(p):
        R = np.zeros((3, 3), dtype=int)
        for a, (bb, s) in p.items(): R['xyz'.index(bb)]['xyz'.index(a)] = s
        return R
    lifts = {}
    for key, p in perm_of.items(): lifts.setdefault(json.dumps(R_of(p).tolist()), key)
    def field_image(g):
        # A_x held as -(y - c)(B0 + b (z - c)) with the line axis 0, across 1, along 2: under g the line axis, across and along axes map to their images with signs
        la, ac, al = [int(np.nonzero(g[:, k])[0][0]) for k in range(3)]; s_la, s_ac, s_al = int(g[la, 0]), int(g[ac, 1]), int(g[al, 2])
        return {'held_potential': [{'line': 1 + la, 'at': list(cen), 'field': 'sg_image', 'across': ac, 'along': al, 'B0': B0, 'b': bgrad, 's_line': s_la, 's_across': s_ac, 's_along': s_al}]}
    base_ctrl = held(1, cen, B0, bgrad, 1, 2); base_ctrl['pauli'] = True; base_ctrl['spinor_turn'] = 'none'
    base, _ = run(world(cube, intervals, [{'lay': 'at', 'row': ROW8, 'centre': list(cen), 'width': 3, 'quanta': N, 'spin': spin0}], base_ctrl))
    def key_of(o, g, det):
        found = []
        for e in o['credits']:
            node = tuple(int(x) % cube for x in (g @ np.array(e['node'], dtype=int) - g @ np.array(cen, dtype=int) + np.array(cen, dtype=int)))
            s = np.array(e.get('spin_sign', [0, 0, 0]), dtype=int); s_img = det * (g @ s)
            found.append((e['i'], node, e['line'], e['sense'], tuple(int(x) for x in s_img)))
        return sorted(found)
    kept = 0; apart = []
    for g in signed_perms():
        det = int(round(np.linalg.det(g))); grot = g * det
        key = lifts[json.dumps(grot.tolist())]; M = SR1['M48'][key]
        spin_g = [sum(M[r][k] * spin0[k] for k in range(8)) for r in range(8)]
        ctrl = field_image(g); ctrl['pauli'] = True; ctrl['spinor_turn'] = 'none'
        o, _ = run(world(cube, intervals, [{'lay': 'at', 'row': ROW8, 'centre': list(cen), 'width': 3, 'quanta': N, 'spin': spin_g}], ctrl))
        other = sorted((e['i'], tuple(e['node']), e['line'], e['sense'], tuple(e.get('spin_sign', [0, 0, 0]))) for e in o['credits'])
        if other == key_of(base, g, det): kept += 1
        else: apart.append({'g': g.tolist(), 'det': det, 'base': len(base['credits']), 'other': len(o['credits'])})
        print(json.dumps({'g': g.tolist(), 'det': det, 'lift': key, 'credits': len(o['credits']), 'kept': other == key_of(base, g, det)}), flush=True)
    found = {'base_credits': len(base['credits']), 'images_kept': kept, 'apart': apart}
    json.dump(found, open(os.path.join(OUT, 'images48_c%d_i%d.json' % (cube, intervals)), 'w'), indent=1); print(json.dumps(found))


def pile(cube, intervals):
    c = cube // 2; cen = (c,) * 3; table = {}
    for name, seeds in (('one quantum, up', [{'lay': 'at', 'row': ROW8, 'centre': list(cen), 'width': 2, 'quanta': 1, 'sense': 1, 'spin': 'spin_up_z'}]),
                        ('two lays of one, up and up', [{'lay': 'at', 'row': ROW8, 'centre': list(cen), 'width': 2, 'quanta': 1, 'sense': 1, 'spin': 'spin_up_z'}] * 2),
                        ('two lays of one, up and down', [{'lay': 'at', 'row': ROW8, 'centre': list(cen), 'width': 2, 'quanta': 1, 'sense': 1, 'spin': 'spin_up_z'}, {'lay': 'at', 'row': ROW8, 'centre': list(cen), 'width': 2, 'quanta': 1, 'sense': 1, 'spin': 'spin_down_z'}]),
                        ('one lay of two, up', [{'lay': 'at', 'row': ROW8, 'centre': list(cen), 'width': 2, 'quanta': 2, 'sense': 1, 'spin': 'spin_up_z'}])):
      for excl in (False, True):
        b = Lean(UNI, world(cube, intervals, seeds, {'pauli': True, 'exclusion': excl}))
        rec = b.records().index(b.by_index[ROW8]); r = b.rule(b.records()[rec].pair, b.content(), b.link_factors()); b.start_content = b.content()
        name_ = name + (' [exclusion on]' if excl else ' [rule off]')
        sh = b.share8(b.records()[rec].lines, r, vacuum=True); tot = int(sum(int(x) for x in sh.reshape(-1))); W, s, sw = b.bilinears8(b.records()[rec].lines)
        table[name_] = {'share total': tot, 'units': tot // b.units[rec], 'remainder': tot % b.units[rec], 'share at centre': int(sh[cen]), 'W total': int(sum(int(x) for x in W.reshape(-1))), 's total': [int(sum(int(x) for x in sa.reshape(-1))) for sa in s], 'amplitudes': [e['amplitude'] for e in b.log if e['event'] == 'lay'], 'refused by state': [e for e in b.log if e['event'] == 'refused' and e.get('cause') == 'state']}
        print(json.dumps({name_: table[name_]}), flush=True)
    json.dump(table, open(os.path.join(OUT, 'pile_c%d.json' % cube), 'w'), indent=1)


def reach(cube):
    c = cube // 2; cen = (c,) * 3
    w = world(cube, 1, [{'lay': 'at', 'row': ROW8, 'centre': list(cen), 'width': 2, 'quanta': 1, 'sense': 1, 'spin': 'spin_up_z'}], {'pauli': True, 'spinor_turn': 'half'})
    def lines_after(change_at, delta):
        b = Lean(UNI, w)
        if change_at is not None:
            l = b.row(4).lines[1]; l.now[change_at] = l.now[change_at] + delta; l.before[change_at] = l.before[change_at] + delta
        b.step(); rec = b.records().index(b.by_index[ROW8])
        return [(int(l.now[cen]), int(l.before[cen]), int(l.rem[cen])) for l in b.records()[rec].lines]
    base = lines_after(None, 0)
    two = lines_after(((c + 2) % cube, c, c), 500); one = lines_after(((c + 1) % cube, c, c), 500)
    found = {'two Links away: the centre Node bit for bit': base == two, 'one Link away: changed': base != one}
    print(json.dumps(found)); json.dump(found, open(os.path.join(OUT, 'reach_c%d.json' % cube), 'w'))


if __name__ == '__main__':
    which = sys.argv[1]; args = [int(x) for x in sys.argv[2:]]
    if which == 'zeeman': zeeman(*args)      # cube intervals back B0
    elif which == 'sg': sg(*args)            # cube intervals back N B0 b
    elif which == 'images': images(*args)    # cube intervals B0 b
    elif which == 'pile': pile(*args)        # cube intervals
    elif which == 'reach': reach(*args)      # cube


def zeeman2(cube, N, B0):
    """The Pauli term's exact reading: the same lay (N quanta, width 2, spin up or down along z) stepped one interval with the term on and off in the held uniform curl; per line at the centre: x_now, the difference of the two x_next (the term alone), and the derived value (+-) num B0 x_now div (3 den Gamma) (g = 2: the shift of 2 cos omega by +- (nu / w) Phi, Phi = 2 B0); the two spins opposite: the doublet."""
    c = cube // 2; cen = (c,) * 3; table = {}
    for spin in ('spin_up_z', 'spin_down_z'):
        xs = {}
        for pauli in (True, False):
            control = held(1, cen, B0, 0, 1, 2); control['pauli'] = pauli; control['spinor_turn'] = 'none'
            w = world(cube, 1, [{'lay': 'at', 'row': ROW8, 'centre': list(cen), 'width': 2, 'quanta': N, 'sense': 1, 'spin': spin}], control)
            o, b = run(w, 1, cen, ROW8); xs[pauli] = o['levels_at_centre']; rb = o['run_back']
        x_now = xs[True][0][:8]; d = [xs[True][1][k] - xs[False][1][k] for k in range(8)]
        num, den, gamma = 506298091, 1655909141, 1000
        pred = [(num * B0 * x) // (3 * den * gamma) for x in x_now]
        table[spin] = {'x_now at the centre': x_now, 'x_next(pauli) - x_next(no pauli)': d, 'derived +- num B0 x_now div (3 den Gamma)': pred, 'ratio of the two as milli (d * 1000 div pred, where pred != 0)': [d[k] * 1000 // pred[k] if pred[k] else None for k in range(8)], 'run_back': rb}
        print(json.dumps({spin: table[spin]}), flush=True)
    json.dump(table, open(os.path.join(OUT, 'zeeman2_c%d_N%d_B%d.json' % (cube, N, B0)), 'w'), indent=1)


if __name__ == '__main__' and sys.argv[1] == 'zeeman2': zeeman2(*[int(x) for x in sys.argv[2:]])


def sg_pol(cube, intervals, back, N, B0, bgrad):
    """The polarised beams one at a time (sp2's reading per sense): a spin-up and a spin-down packet (one sense each) through the held gradient along z and with no field; the credits' centroid along z (all credits), the per-z counts, the board's G-weight centroid."""
    c = cube // 2; cen = (c,) * 3; table = {}
    for spin in ('spin_up_z', 'spin_down_z'):
        for name, control in (('no field', {}), ('gradient along z', held(1, cen, B0, bgrad, 1, 2))):
            control = dict(control); control['pauli'] = True; control['spinor_turn'] = 'none'
            w = world(cube, intervals, [{'lay': 'at', 'row': ROW8, 'centre': list(cen), 'width': 3, 'quanta': N, 'sense': 1, 'spin': spin}], control)
            o, b = run(w, back, cen, ROW8)
            cs = o['credits']; per = [sum(1 for e in cs if e['node'][2] == z) for z in range(cube)]
            rec = b.records().index(b.by_index[ROW8]); ls = b.records()[rec].lines; wgt = gform8(SR1['G'], [l.now for l in ls], [l.now for l in ls]); idx = np.indices(b.shape)[2]
            tot = int(sum(int(x) for x in wgt.reshape(-1))); bc = None if tot == 0 else int(sum(int(w_) * int(x) for w_, x in zip(wgt.reshape(-1), idx.reshape(-1)))) * 1000 // tot
            table[spin + ', ' + name] = {'credits': len(cs), 'per z': per, 'centroid z milli (credits)': None if not cs else sum(e['node'][2] for e in cs) * 1000 // len(cs), 'board G-weight centroid z milli': bc, 'senses': {s: sum(1 for e in cs if e['sense'] == s) for s in (1, -1, 0)}, 'spin_z sign of the credits': {s: sum(1 for e in cs if e.get('spin_sign', [0, 0, 0])[2] == s) for s in (1, -1, 0)}, 'beats': sorted(set(e['beat'] for e in cs)), 'run_back': o.get('run_back'), 'births': o['births'], 'births_senses_sum': o['births_senses_sum'], 'integers': o['integers'], 'bits': o['max_bits_state'], 'transient': o['max_transient_bits'], 'taken': o['counts']['taken'], 'booked': o['counts']['booked']}
            print(json.dumps({spin + ', ' + name: table[spin + ', ' + name]}), flush=True)
    json.dump(table, open(os.path.join(OUT, 'sg_pol_c%d_i%d_N%d_B%d_b%d.json' % (cube, intervals, N, B0, bgrad)), 'w'), indent=1)


if __name__ == '__main__' and sys.argv[1] == 'sg_pol': sg_pol(*[int(x) for x in sys.argv[2:]])
