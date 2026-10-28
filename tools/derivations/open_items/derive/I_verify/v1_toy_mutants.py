"""I_verify v1: the verifier's own mutants on draft I's toy (i1_toy.py, imported unchanged from run/).

Mutants (each must make at least one check FAIL):
  skew_nopawl   : fixAB with the pawl dropped from the skew only, m = 3 R s (V_x + V_y), the odd gear kept framed
  T_twice_plain : the turnover writes the plain exchange (no K) and does not flip the pawl (T applied zero/two times)
  T_twice_K     : the turnover writes K on the hand and flips the pawl (the head's, T twice) inside the 'fix' kind
  transverse_V  : the skew reads the flow gear's transverse component V_(a+1) (a contraction the 24 forbid)
  transverse_both : odd and flow both transverse, (a+1) and (a+2): a second transverse contraction
Also an independent recount of the gauge test C3 for fixAB with a fresh seed.
Run: python3 -I v1_toy_mutants.py
"""
import random
import sys
from fractions import Fraction as Fr

HERE = '/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/derive/I_verify/run'
sys.argv = [sys.argv[0]]
sys.path.insert(0, HERE)
import i1_toy as M  # noqa: E402

ORIG_TURN = M.turn
ORIG_TURNED = M.turned


def make_turn(kind):
    def turn(W, x, j, z, variant):
        y = M.nb(x, j)
        a, s = M.SPOKES[j]
        ex, ey = M.eps(W, x), M.eps(W, y)
        f = ex * ey
        seen = z if f == 1 else M.conj(z)
        n = W['K'][x] - f * W['K'][y]
        u_off = M.unit_of(n / W['NC'])
        ox, oy, vx, vy = W['o'][x][a], W['o'][y][a], W['V'][x][a], W['V'][y][a]
        if kind in ('transverse_V', 'transverse_both'):
            vx, vy = W['V'][x][(a + 1) % 3], W['V'][y][(a + 1) % 3]
        if kind == 'transverse_both':
            ox, oy = W['o'][x][(a + 2) % 3], W['o'][y][(a + 2) % 3]
        R = W['R']
        if variant == 'head':
            odd, m = s * (ox + oy), 3 * R * s * (vx + vy)
        elif variant == 'fixAB':
            odd, m = s * (ox + f * oy), ex * 3 * R * s * (vx + vy)
            if kind == 'skew_nopawl':
                m = 3 * R * s * (vx + vy)
        else:
            return ORIG_TURN(W, x, j, z, variant)
        return M.mul(M.mul(M.tri(odd, m, W['G']), u_off), seen)
    return turn


def make_turned(kind):
    def turned(W, st, x, k):
        a, P = st['a'][x], st['P'][x]
        ab = M.sub(a, M.scl(1 / M.teeth(W, x), P))
        if k == 'head' or kind == 'T_twice_K':
            return M.conj(ab), M.scl(-1, M.conj(P))
        return ab, M.scl(-1, P)
    return turned


def run_checks(kind):
    M.RES.clear()
    M.turn = make_turn(kind)
    M.turned = make_turned(kind)
    out = []
    import io
    import contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        if kind in ('skew_nopawl', 'transverse_V', 'transverse_both'):
            for c in (M.c1, M.c2, M.c3, M.c4):
                c()
        if kind == 'T_twice_plain':
            # the plain exchange with no pawl flip: run C6 with the pawl flip suppressed
            orig_c6 = M.c6

            def c6_noflip():
                rng = random.Random(16)
                variant = 'fixAB'
                for where in ('held', 'stepped'):
                    bad = n = 0
                    for trial in range(4):
                        W = M.world(rng)
                        st = M.new_state(rng, W)
                        q0 = M.qstar(W, st)
                        xs = [x for x in M.SITES if rng.randint(0, 3) == 0]
                        s1 = M.step(W, st, variant)
                        inflow = sum((-sum((M.current(W, st, x, j, variant) for j in range(6)), Fr(0)) for x in xs), Fr(0))
                        src = st if where == 'held' else s1
                        o = {'a': dict(s1['a']), 'P': dict(s1['P'])}
                        for x in xs:
                            o['a'][x], o['P'][x] = M.turned(W, src, x, 'fix')
                        q1 = M.qstar(W, o)            # the pawl NOT flipped: W unchanged
                        n += 1
                        bad += int(q1 - q0 != -inflow) if where == 'held' else int(q1 != q0)
                    M.report(f"C6 T_twice_plain ({where}): framed charge kept up to the inflow", bad == 0,
                             f"failures {bad} of {n}")
            c6_noflip()
        if kind == 'T_twice_K':
            M.c6()
    text = buf.getvalue()
    fails = [n for n, ok in M.RES if not ok]
    M.turn, M.turned = ORIG_TURN, ORIG_TURNED
    return text, fails


if __name__ == '__main__':
    for kind in ('skew_nopawl', 'T_twice_plain', 'T_twice_K', 'transverse_V', 'transverse_both'):
        text, fails = run_checks(kind)
        print(f"=== verifier mutant {kind}: {len(fails)} checks FAIL -> {'mutant KILLED' if fails else 'mutant SURVIVES'}")
        for line in text.splitlines():
            if line.startswith('FAIL'):
                print('   ' + line)
    # an independent recount of the gauge commutation for fixAB with a fresh seed
    rng = random.Random(9001)
    bad = n = 0
    for trial in range(3):
        W = M.world(rng)
        st = M.new_state(rng, W)
        xs = [x for x in M.SITES if rng.randint(0, 1)]
        Wg, stg = M.gauge(W, st, xs, True, False)
        lhs = M.step(Wg, stg, 'fixAB')
        rhs = M.gauge(W, M.step(W, st, 'fixAB'), xs, True, False)[1]
        for x in M.SITES:
            n += 1
            bad += int(lhs['a'][x] != rhs['a'][x] or lhs['P'][x] != rhs['P'][x])
    print(f"recount C3 fixAB (seed 9001, a and P both compared): {bad} of {n} Node-clocks differ")
