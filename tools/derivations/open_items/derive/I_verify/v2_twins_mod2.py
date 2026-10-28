"""I_verify v2: the twin hands' frame count, mod 4 against mod 2 (draft I's i2_twins.py imported unchanged).

D5 (new): the stored twins with turnovers against the physical twins with turnovers, tick by tick.
  physical: frame c = 0 everywhere, the turnover applies T once to the physical slots (Z_now' = T Z_before,
            P' = -T P), the bare hop h;
  stored  : the count c and the read K^(c_x)(h) T^(c_y - c_x) psi_y (i2's `read`), the slots exchanged with no T.
  The test: Z_phys == T^c psi_stored at every Node-clock and tick, and the charge kept.
Variants of the stored count:
  mod4      : c -> c + 1 modulo 4 (draft I's change 2)
  mod2      : c -> c + 1 modulo 2, no sign (a mod-2 count, the verifier's mutant)
  mod2_sign : c -> c + 1 modulo 2, and the slots negated where c wraps from 1 to 0 (T T = -1 written in the gears)
  twice     : T in the slots and the count advanced modulo 4 (T applied twice)
Run: python3 -I v2_twins_mod2.py
"""
import random
import sys
from fractions import Fraction as Fr

HERE = '/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/derive/I_verify/run'
sys.argv = [sys.argv[0]]
sys.path.insert(0, HERE)
import i2_twins as M  # noqa: E402


def stored_turn(W, st, xs, how):
    W2 = dict(W)
    W2['c'] = dict(W['c'])
    out = {'psi': dict(st['psi']), 'P': dict(st['P'])}
    for x in xs:
        psi, P = st['psi'][x], st['P'][x]
        before = M.vsub(psi, M.vscl(1 / (W['T'] * W['X'][x]), P))
        c = W['c'][x]
        if how == 'twice':
            out['psi'][x], out['P'][x] = M.T(before), M.vscl(-1, M.T(P))
            W2['c'][x] = (c + 1) % 4
        elif how == 'mod4':
            out['psi'][x], out['P'][x] = before, M.vscl(-1, P)
            W2['c'][x] = (c + 1) % 4
        elif how == 'mod2':
            out['psi'][x], out['P'][x] = before, M.vscl(-1, P)
            W2['c'][x] = (c + 1) % 2
        elif how == 'mod2_sign':
            sgn = -1 if c == 1 else 1
            out['psi'][x], out['P'][x] = M.vscl(sgn, before), M.vscl(-sgn, P)
            W2['c'][x] = (c + 1) % 2
    return W2, out


def phys_turn(W, st, xs):
    out = {'psi': dict(st['psi']), 'P': dict(st['P'])}
    for x in xs:
        psi, P = st['psi'][x], st['P'][x]
        before = M.vsub(psi, M.vscl(1 / (W['T'] * W['X'][x]), P))
        out['psi'][x], out['P'][x] = M.T(before), M.vscl(-1, M.T(P))
    return out


def d5(how, seed):
    rng = random.Random(seed)
    W = M.world(rng)
    W['c'] = {x: 0 for x in M.SITES}           # start in one frame: the stored and the physical state equal
    W['B'] = {x: [Fr(0)] * 3 for x in M.SITES}  # no spin field: the bare hop alone (the frame test)
    st = M.new_state(rng, W)
    Wp = dict(W)
    Wp['c'] = {x: 0 for x in M.SITES}
    ph = {'psi': dict(st['psi']), 'P': dict(st['P'])}
    q0 = M.charge(W, st)
    differ = moved = turns = 0
    for t in range(24):
        st = M.step(W, st)
        ph = M.step(Wp, ph)
        if t % 2 == 1:
            xs = [x for x in M.SITES if rng.randint(0, 1) == 0]
            turns += len(xs)
            W, st = stored_turn(W, st, xs, how)
            ph = phys_turn(Wp, ph, xs)
        bad = any(M.Tpow(W['c'][x], st['psi'][x]) != ph['psi'][x] for x in M.SITES)
        differ += int(bad)
        moved += int(M.charge(W, st) != q0)
    return differ, moved, turns


if __name__ == '__main__':
    for how in ('mod4', 'mod2', 'mod2_sign', 'twice'):
        tot_d = tot_m = tot_t = 0
        for seed in (51, 52):
            d, m, t = d5(how, seed)
            tot_d += d
            tot_m += m
            tot_t += t
        print(f"D5 {how}: stored != physical at {tot_d} of 48 ticks; the stored charge moved at {tot_m} of 48 ticks;"
              f" {tot_t} Node-clock turnovers")
    # D1 on a mod-2 assignment read with the integer difference (T^-1 = -T): antisymmetry
    rng = random.Random(53)
    bad = n = 0
    for trial in range(6):
        W = M.world(rng)
        W['c'] = {x: rng.randint(0, 1) for x in M.SITES}
        st = M.new_state(rng, W)
        for x in M.SITES:
            for j in range(6):
                if M.SPOKES[j][1] != 1:
                    continue
                y = M.nb(x, j)
                n += 1
                bad += int(M.cur(W, st, x, j) + M.cur(W, st, y, M.back(j)) != 0)
    print(f"D1 on pawl-only frames (c in {{0,1}}, read T^(c_y - c_x) with T^-1 = -T): {bad} of {n} Meshes not antisymmetric")
