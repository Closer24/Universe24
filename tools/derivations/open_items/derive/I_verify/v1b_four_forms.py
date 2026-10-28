"""I_verify v1b: the four pawl placements of the triple (each T1 gear read with the near pawl e_x or the far pawl f)
against the four framings of the gauge flip (o framed or not, V framed or not), on draft I's toy (i1 imported).
For each form: C1 antisymmetry (Meshes off), C2 Q* over 20 exact ticks, C3 the gauge commutation per framing."""
import random
import sys
HERE = '/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/derive/I_verify/run'
sys.argv = [sys.argv[0]]
sys.path.insert(0, HERE)
import i1_toy as M  # noqa: E402

FORMS = {'odd far, V near (fixAB)': ('far', 'near'), 'odd far, V far (fixA)': ('far', 'far'),
         'odd near, V near (fixB)': ('near', 'near'), 'odd near, V far (fixBA, not in the draft)': ('near', 'far')}
ORIG = M.turn

def make(po, pv):
    def turn(W, x, j, z, variant):
        y = M.nb(x, j)
        a, s = M.SPOKES[j]
        ex, ey = M.eps(W, x), M.eps(W, y)
        f = ex * ey
        seen = z if f == 1 else M.conj(z)
        n = W['K'][x] - f * W['K'][y]
        u_off = M.unit_of(n / W['NC'])
        ox, oy, vx, vy = W['o'][x][a], W['o'][y][a], W['V'][x][a], W['V'][y][a]
        R = W['R']
        odd = s * (ox + f * oy) if po == 'far' else ex * s * (ox + oy)
        m = 3 * R * s * (vx + f * vy) if pv == 'far' else ex * 3 * R * s * (vx + vy)
        return M.mul(M.mul(M.tri(odd, m, W['G']), u_off), seen)
    return turn

for name, (po, pv) in FORMS.items():
    M.turn = make(po, pv)
    rng = random.Random(4242)
    off = n = 0
    for trial in range(4):
        W = M.world(rng)
        st = M.new_state(rng, W)
        for x in M.SITES:
            for j in range(6):
                if M.SPOKES[j][1] != 1:
                    continue
                y = M.nb(x, j)
                n += 1
                off += int(M.current(W, st, x, j, 'fixAB') + M.current(W, st, y, M.back(j), 'fixAB') != 0)
    W = M.world(rng)
    st = M.new_state(rng, W)
    q0 = M.qstar(W, st)
    moved = 0
    for _ in range(20):
        st = M.step(W, st, 'fixAB')
        moved += int(M.qstar(W, st) != q0)
    comm = {}
    for fo in (True, False):
        for fv in (True, False):
            bad = cnt = 0
            for trial in range(2):
                W = M.world(rng)
                st = M.new_state(rng, W)
                xs = [x for x in M.SITES if rng.randint(0, 1)]
                Wg, stg = M.gauge(W, st, xs, fo, fv)
                lhs = M.step(Wg, stg, 'fixAB')
                rhs = M.gauge(W, M.step(W, st, 'fixAB'), xs, fo, fv)[1]
                for x in M.SITES:
                    cnt += 1
                    bad += int(lhs['a'][x] != rhs['a'][x])
            comm[f"o {'framed' if fo else 'unframed'}, V {'framed' if fv else 'unframed'}"] = f"{bad} of {cnt}"
    print(f"{name}: antisymmetry off at {off} of {n} Meshes; Q* moved at {moved} of 20 ticks; G-commutation failures: {comm}")
M.turn = ORIG
