"""Draft D, the closure of the split: the lattice probe (DERIVATION.md, parts 3 to 5). Integers only.

A great clock on the torus holds the twin train's four gears at every Node-clock (the up twin's three and twelve, the
down twin's three and twelve), each as (notch now, notch before, fine tooth). Every gear steps by the one formula of
law 2 with the head's own Rule3 (event_universe.core.acts.carry and mid, imported from the head, bit for bit):
    p = W (a - a-) + (r - mid W),  F = sum over the six Spokes of g (a_j - a) - D a,  p+ = p + s F,
    (a+ - a, r+) = carry(p+, W, mid W)
(flat clock: W and s constant; U_j the identity; J = 0). A fitting's two fitted hands are bobs L Meshes apart on one
axis: chi(n) K at A and chi(-n) K at B (the fitting's opposite senses), n one of the six Spoke directions. The draw is
the vernier's form: the fine teeth of the Node-clock and of its six Spokes' Node-clocks, sorted, composed by Rule3
modulo the room. A click of a split is law 6: up where c (rho + rho) rho_d < room (rho rho_d + S . m).

The models of the closure:
  M0  local:          each fitted hand clicks on its own twin pair; nothing written, nothing carried.
  M1a carriage, open: David's closure as written. The fitting stores the open reading (rho, S = 0) at both ends (a
                      reading no twin pair holds: closure24_algebra.py, 'open'); the first click writes a message
                      (rho1, m1, a) that moves one Mesh a tick; the partner reads (rho1, -a m1) once it has arrived.
  M1b carriage, own:  as M1a, with each fitted hand's own twin pair read before the message arrives.
  M2  one formula:    no message. The first click leaves its remainder (the part not taken, axis -a m1) in A's gears,
                      and the one formula carries it; the partner clicks on its own twin pair.
  M2e one formula, partner empty: as M2 with no bob at B, A clicking at its fitting; B's reading is the arrival alone.
  M3  the link's one act (L = 1): one draw over four parts sigma_ab = N(det[phi1^a, phi2^b]).
Run: python3 -I closure24_lattice.py  (it imports only the head's core.acts, which imports core.spokes)."""

import sys

HEAD_SRC = "/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/t24/src"
sys.path.insert(0, HEAD_SRC)
from event_universe.core.acts import carry, mid  # noqa: E402  the head's Rule3

MASK = (1 << 64) - 1


class Lcg:
    def __init__(self, seed):
        self.x = seed & MASK

    def next(self):
        self.x = (self.x * 6364136223846793005 + 1442695040888963407) & MASK
        return self.x >> 33

    def below(self, n):
        return self.next() % n


# ---- Gaussian integers and twin pairs (as in closure24_algebra.py) ------------------------------------------------
def gc(z):
    return (z[0], -z[1])


def gm(z, w):
    return (z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0])


def ga(z, w):
    return (z[0] + w[0], z[1] + w[1])


def gs(z, w):
    return (z[0] - w[0], z[1] - w[1])


def gn(z):
    return (-z[0], -z[1])


def nrm(z):
    return z[0] * z[0] + z[1] * z[1]


def reading(psi):
    a, b = psi
    ab = gm(gc(a), b)
    return nrm(a) + nrm(b), (ab[0] + ab[0], ab[1] + ab[1], nrm(a) - nrm(b))


def perp(phi):
    return (gn(gc(phi[1])), gc(phi[0]))


def inner(phi, psi):
    return ga(gm(gc(phi[0]), psi[0]), gm(gc(phi[1]), psi[1]))


def det(u, v):
    return gs(gm(u[0], v[1]), gm(u[1], v[0]))


def dot3(s, t):
    return s[0] * t[0] + s[1] * t[1] + s[2] * t[2]


def sense(phi, a):
    return phi if a > 0 else perp(phi)


def law6(c, room, rd, rho, s, m):
    """The click of a split (law 6): +1 (up) where c (rho + rho) rho_d < room (rho rho_d + S . m), else -1."""
    return 1 if c * (rho + rho) * rd < room * (rho * rd + dot3(s, m)) else -1


def ups(room, rd, rho, s, m):
    """How many draws c in [0, room) give up under law 6 (the exact odds of a fair draw, as a count)."""
    return sum(1 for c in range(room) if law6(c, room, rd, rho, s, m) > 0)


SPOKE_DIRS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
SIX = {
    (0, 0, 1): ((1, 0), (0, 0)), (0, 0, -1): ((0, 0), (1, 0)),
    (1, 0, 0): ((1, 0), (1, 0)), (-1, 0, 0): ((1, 0), (-1, 0)),
    (0, 1, 0): ((1, 0), (0, 1)), (0, -1, 0): ((1, 0), (0, -1)),
}
SIX_KEYS = sorted(SIX)
SETTINGS = {"a": ((1, 0), (0, 0)), "a'": ((1, 0), (1, 0)), "b": ((5, 0), (2, 0)), "b'": ((5, 0), (-2, 0))}
PAIRS = [("a", "b", 1), ("a", "b'", 1), ("a'", "b", 1), ("a'", "b'", -1)]
OTHER_A = {"a": "a'", "a'": "a"}


class Lattice:
    """The twin train on a torus of the given extent, every gear (notch now, notch before, fine tooth)."""

    def __init__(self, shape, teeth, stretch, grip, spring):
        self.shape = shape
        nx, ny, nz = shape
        self.sites = [(x, y, z) for x in range(nx) for y in range(ny) for z in range(nz)]
        index = {p: i for i, p in enumerate(self.sites)}
        self.spokes = [[index[((x + dx) % nx, (y + dy) % ny, (z + dz) % nz)] for dx, dy, dz in SPOKE_DIRS] for x, y, z in self.sites]
        # a folded axis' Spokes read the Node-clock itself, where g (a - a) = 0 exactly: the pull sums the others alone
        self.pulled = [[j for j in row if j != i] for i, row in enumerate(self.spokes)]
        self.W, self.s, self.g, self.D, self.mid = teeth, stretch, grip, spring, mid(teeth)
        n = len(self.sites)
        self.now = [[0] * 4 for _ in range(n)]
        self.before = [[0] * 4 for _ in range(n)]
        self.fine = [[self.mid] * 4 for _ in range(n)]
        self.index = index

    def copy(self):
        other = Lattice.__new__(Lattice)
        other.__dict__.update(self.__dict__)
        other.now = [row[:] for row in self.now]
        other.before = [row[:] for row in self.before]
        other.fine = [row[:] for row in self.fine]
        return other

    def pull(self, slot, i, k):
        a = slot[i][k]
        return sum(slot[j][k] - a for j in self.pulled[i]) * self.g - self.D * a

    def step(self):
        """Law 2 at every gear, every read before any write."""
        W, s, m = self.W, self.s, self.mid
        now, before, fine = self.now, self.before, self.fine
        new_now, new_fine = [], []
        for i in range(len(now)):
            rn, rf = [], []
            for k in range(4):
                a = now[i][k]
                q, f = carry(W * (a - before[i][k]) + fine[i][k] - m + s * self.pull(now, i, k), W, m)
                rn.append(a + q)
                rf.append(f)
            new_now.append(rn)
            new_fine.append(rf)
        self.before, self.now, self.fine = now, new_now, new_fine

    def unstep(self):
        """Law 3, the rewind: p+ = W (a+ - a) + r+ - mid, p = p+ - s F(a), then (a - a-, r) = carry(p, W, mid)."""
        W, s, m = self.W, self.s, self.mid
        now, before, fine = self.now, self.before, self.fine
        new_before, new_fine = [], []
        for i in range(len(now)):
            rb, rf = [], []
            for k in range(4):
                a = before[i][k]
                p = W * (now[i][k] - a) + fine[i][k] - m - s * self.pull(before, i, k)
                q, f = carry(p, W, m)
                rb.append(a - q)
                rf.append(f)
            new_before.append(rb)
            new_fine.append(rf)
        self.now, self.before, self.fine = before, new_before, new_fine

    def twin(self, i, slot=None):
        row = (self.now if slot is None else slot)[i]
        return ((row[0], row[1]), (row[2], row[3]))

    def set_twin(self, i, psi, slot):
        slot[i][0], slot[i][1], slot[i][2], slot[i][3] = psi[0][0], psi[0][1], psi[1][0], psi[1][1]

    def draw(self, i, room):
        """The vernier's form: every gear's fine tooth at the Node-clock and its six Spokes' Node-clocks, sorted,
        composed as a mixed-radix number by Rule3 modulo the room (W^28 > room, so the room is the modulus)."""
        digits = sorted(self.fine[j][k] for j in [i] + self.spokes[i] for k in range(4))
        c = 0
        for d in digits:
            c = carry(c * self.W + d, room, 0)[1]
        return c

    def leave_remainder(self, i, phi, a):
        """M2's write: the split's quotient leaves and its remainder stays. At both slots the twin pair becomes the part
        not taken, <eta, psi> eta div N(eta) with eta = phi^(-a), coefficient by coefficient by Rule3; the Rule3
        remainders and the replaced gears are the note the rewind reads (the click's books)."""
        eta = sense(phi, -a)
        rd = nrm(eta[0]) + nrm(eta[1])
        note = (i, [row[:] for row in (self.now[i], self.before[i])])
        for slot in (self.now, self.before):
            c = inner(eta, self.twin(i, slot))
            part = (gm(c, eta[0]), gm(c, eta[1]))
            kept = tuple(tuple(carry(x, rd, 0)[0] for x in z) for z in part)
            self.set_twin(i, kept, slot)
        return note

    def undo(self, note):
        i, (now_row, before_row) = note
        self.now[i], self.before[i] = now_row[:], before_row[:]


def chi_k(n, k):
    return tuple(tuple(k * x for x in z) for z in SIX[n])


def neg(n):
    return tuple(-x for x in n)


def set_bob(lat, i, psi):
    lat.set_twin(i, psi, lat.now)
    lat.set_twin(i, psi, lat.before)


def tenk(n, d):
    q = (abs(n) * 10000) // d
    return -q if n < 0 else q


def fmt(n, d):
    v = tenk(n, d)
    sign = "-" if v < 0 else " "
    v = abs(v)
    return f"{sign}{v // 10000}.{v % 10000:04d}"


# ---- the world's integers (a piece of the probe; no number of the engine) -----------------------------------------
W = 3 << 19  # the teeth count, even
STRETCH = 1
LIGHT = (W // 3, W // 24)  # (grip, spring): the light's own grip ratio s g / W = 1/3, a light twin train
HEAVY = (W // 96, W // 6)  # a heavy twin train, a bob that stays
K = 1 << 12  # a bob's notches
ROOM = 5800  # a room every 2 rho rho_d of the settings divides
L = 6
T_A = 2
DELTAS = list(range(0, L + 7))


def classify(delta):
    return "spacelike" if delta <= L - 2 else ("edge" if delta == L - 1 else "timelike")


# ---- part A: many draws on a ring of extent (2L + 2, 1, 1), the draws read from the fine teeth --------------------
def ring_runs(params, runs_per_pair, seed):
    """Every run: a fitting with hidden n and fine teeth lambda from the LCG, one setting pair by the run's index. One
    evolution serves M0, M1a, M1b (their clicks write no gear); M2 has its own evolution with A's write, and a third
    with A's other setting for the bit-for-bit locality count. B's click is read at every delta of DELTAS."""
    grip, spring = params
    shape = (2 * L + 2, 1, 1)
    models = ("M0", "M1a", "M1b", "M2")
    tally = {(mo, d, p): [0, 0, 0] for mo in models for d in DELTAS for p in range(4)}  # (sum of a b, count, sum of b)
    changed = {(mo, d): [0, 0, 0] for mo in models for d in DELTAS}  # runs where B's answer, draw, reading moved with A's setting
    checked = dict.fromkeys(DELTAS, 0)
    rng = Lcg(seed)
    for run in range(4 * runs_per_pair):
        pidx = run % 4
        x, y, _sgn = PAIRS[pidx]
        phi1, phi2, phi1o = SETTINGS[x], SETTINGS[y], SETTINGS[OTHER_A[x]]
        (rd1, m1), (rd2, m2), (rd1o, m1o) = reading(phi1), reading(phi2), reading(phi1o)
        n = SIX_KEYS[rng.below(6)]
        base = Lattice(shape, W, STRETCH, grip, spring)
        for row in base.fine:
            for k in range(4):
                row[k] = rng.below(W)
        ia, ib = base.index[(0, 0, 0)], base.index[(L, 0, 0)]
        set_bob(base, ia, chi_k(n, K))
        set_bob(base, ib, chi_k(neg(n), K))
        rho_open_a = reading(base.twin(ia))[0]
        rho_open_b = reading(base.twin(ib))[0]
        for _ in range(T_A):
            base.step()
        ca = base.draw(ia, ROOM)
        rho_a, s_a = reading(base.twin(ia))
        a_own = law6(ca, ROOM, rd1, rho_a, s_a, m1)
        a_own_o = law6(ca, ROOM, rd1o, rho_a, s_a, m1o)
        a_open = law6(ca, ROOM, rd1, rho_open_a, (0, 0, 0), m1)
        a_open_o = law6(ca, ROOM, rd1o, rho_open_a, (0, 0, 0), m1o)
        two = base.copy()
        note = two.leave_remainder(ia, phi1, a_own)
        three = base.copy()
        three.leave_remainder(ia, phi1o, a_own_o)
        del note
        for t in range(T_A, T_A + DELTAS[-1] + 1):
            delta = t - T_A
            if t > T_A:
                base.step()
                two.step()
                three.step()
            arrived = delta >= L  # the message has moved L Meshes, one a tick
            cb = base.draw(ib, ROOM)
            rho_b, s_b = reading(base.twin(ib))
            b0 = law6(cb, ROOM, rd2, rho_b, s_b, m2)
            if arrived:
                b1a = law6(cb, ROOM, rd2, rd1, tuple(-a_open * v for v in m1), m2)
                b1a_o = law6(cb, ROOM, rd2, rd1o, tuple(-a_open_o * v for v in m1o), m2)
                b1b = law6(cb, ROOM, rd2, rd1, tuple(-a_own * v for v in m1), m2)
                b1b_o = law6(cb, ROOM, rd2, rd1o, tuple(-a_own_o * v for v in m1o), m2)
            else:
                b1a = b1a_o = law6(cb, ROOM, rd2, rho_open_b, (0, 0, 0), m2)
                b1b = b1b_o = b0
            cb2 = two.draw(ib, ROOM)
            rho2, s2 = reading(two.twin(ib))
            b2 = law6(cb2, ROOM, rd2, rho2, s2, m2)
            cb3 = three.draw(ib, ROOM)
            rho3, s3 = reading(three.twin(ib))
            b2_o = law6(cb3, ROOM, rd2, rho3, s3, m2)
            for mo, aa, bb in (("M0", a_own, b0), ("M1a", a_open, b1a), ("M1b", a_own, b1b), ("M2", a_own, b2)):
                cell = tally[(mo, delta, pidx)]
                cell[0] += aa * bb
                cell[1] += 1
                cell[2] += bb
            # M0's B reads its own Node-clock of the one lattice, which no click writes: nothing of A's setting reaches it
            changed[("M1a", delta)][0] += b1a != b1a_o
            changed[("M1b", delta)][0] += b1b != b1b_o
            changed[("M1a", delta)][2] += arrived and (rd1, m1) != (rd1o, m1o)
            changed[("M1b", delta)][2] += arrived and (rd1, m1) != (rd1o, m1o)
            moved = changed[("M2", delta)]
            moved[0] += b2 != b2_o
            moved[1] += cb2 != cb3
            moved[2] += (rho2, s2) != (rho3, s3)
            checked[delta] += 1
    return tally, changed, checked


def s_of(tally, model, delta):
    """S = E(a,b) + E(a,b') + E(a',b) - E(a',b') as an integer ratio, each E = (sum of a b) / count."""
    num, den = 0, 1
    es = []
    for p, (_x, _y, sgn) in enumerate(PAIRS):
        e_num, e_den = tally[(model, delta, p)][:2]
        es.append((e_num, e_den))
        num, den = num * e_den + sgn * e_num * den, den * e_den
    return (num, den), es


# ---- part B: exact odds (every draw c in [0, room) counted) on the one formula's own carriage, 1D and 3D -----------
def exact_one_formula(params, shape, deltas, empty_partner=False, t_a=T_A):
    """For every n of the six, every setting pair and both answers a, the lattice from the fitting with A's remainder
    left at t_a; the partner's exact odds read at every delta. Returns E per (delta, pair) averaged over n, as ratios,
    and, for the empty partner, the arrival's alignment with -a m1 and its rho against the fitted hand's."""
    grip, spring = params
    out = {}
    align = {}
    for n in SIX_KEYS:
        for p, (x, y, _sgn) in enumerate(PAIRS):
            phi1, phi2 = SETTINGS[x], SETTINGS[y]
            (rd1, m1), (rd2, m2) = reading(phi1), reading(phi2)
            lat = Lattice(shape, W, STRETCH, grip, spring)
            ia, ib = lat.index[(0, 0, 0)], lat.index[(L, 0, 0)]
            set_bob(lat, ia, chi_k(n, K))
            if not empty_partner:
                set_bob(lat, ib, chi_k(neg(n), K))
            rho_child = reading(lat.twin(ia))[0]
            for _ in range(t_a):
                lat.step()
            rho_a, s_a = reading(lat.twin(ia))
            count_up = ups(ROOM, rd1, rho_a, s_a, m1)
            p_a = {1: count_up, -1: ROOM - count_up}
            runs = {a: lat.copy() for a in (1, -1)}
            for a in (1, -1):
                runs[a].leave_remainder(ia, phi1, a)
            for t in range(t_a, t_a + max(deltas) + 1):
                delta = t - t_a
                if t > t_a:
                    for a in (1, -1):
                        runs[a].step()
                if delta not in deltas:
                    continue
                num = marg = 0
                for a in (1, -1):
                    rho_b, s_b = reading(runs[a].twin(ib))
                    if rho_b == 0:
                        up_b = ROOM // 2  # nothing at B: no axis; counted as half (the fair draw on no parts)
                    else:
                        up_b = ups(ROOM, rd2, rho_b, s_b, m2)
                    num += p_a[a] * a * (up_b - (ROOM - up_b))
                    marg += p_a[a] * (up_b - (ROOM - up_b))
                    if empty_partner:
                        key = (delta, a)
                        tgt = tuple(-a * v for v in m1)
                        cell = align.setdefault(key, [0, 0, 0, 0, 0, 0])
                        cell[5] += rho_b == 0
                        # alignment: (rho_b rho1 + S_b . (-a m1)) against 2 rho_b rho1; and rho_b against the child's rho
                        cell[0] += rho_b * rd1 + dot3(s_b, tgt)
                        cell[1] += 2 * rho_b * rd1
                        cell[2] += rho_b
                        cell[3] += rho_child
                        cell[4] += 1
                acc = out.setdefault((delta, p), [0, 0, 0])
                acc[0] += num
                acc[1] += ROOM * ROOM
                acc[2] += marg
    return out, align


def signal_gap(cells):
    """B's marginal <b> under A's setting a against a', at each of B's settings: the largest gap, as a ratio.
    cells[p] = (sum or numerator of b, count or denominator); PAIRS 0 and 2 share B's b, 1 and 3 share b'."""
    best = (0, 1)
    for p, q in ((0, 2), (1, 3)):
        (n1, d1), (n2, d2) = cells[p], cells[q]
        gap = (abs(n1 * d2 - n2 * d1), d1 * d2)
        if gap[0] * best[1] > best[0] * gap[1]:
            best = gap
    return best


def s_exact(out, delta):
    num, den = 0, 1
    es = []
    for p, (_x, _y, sgn) in enumerate(PAIRS):
        e_num, e_den = out[(delta, p)][:2]
        es.append((e_num, e_den))
        num, den = num * e_den + sgn * e_num * den, den * e_den
    return (num, den), es


# ---- part C: the rewind across the remainder's write --------------------------------------------------------------
def rewind_check(params, shape, ticks, trials, seed):
    grip, spring = params
    rng = Lcg(seed)
    fails = 0
    for _ in range(trials):
        lat = Lattice(shape, W, STRETCH, grip, spring)
        for row in lat.fine:
            for k in range(4):
                row[k] = rng.below(W)
        n = SIX_KEYS[rng.below(6)]
        ia, ib = lat.index[(0, 0, 0)], lat.index[(L % shape[0], 0, 0)]
        set_bob(lat, ia, chi_k(n, K))
        set_bob(lat, ib, chi_k(neg(n), K))
        start = (([r[:] for r in lat.now]), [r[:] for r in lat.before], [r[:] for r in lat.fine])
        for _ in range(T_A):
            lat.step()
        note = lat.leave_remainder(ia, SETTINGS["a'"], 1 if rng.below(2) else -1)
        for _ in range(ticks):
            lat.step()
        for _ in range(ticks):
            lat.unstep()
        lat.undo(note)
        for _ in range(T_A):
            lat.unstep()
        fails += (lat.now, lat.before, lat.fine) != start
    return trials, fails


# ---- part D: the link's one act at L = 1 (the pair at both ends of one Mesh) --------------------------------------
def link_act(runs_per_pair, seed):
    """One draw at the - end (A) over the four parts sigma_ab = N(det[phi1^a, phi2^b]) (Rule3: c total = t room + r,
    the part where t falls), exact by counting every c, and measured with the vernier's draws on a ring."""
    order = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    exact = []
    for x, y, _sgn in PAIRS:
        phi1, phi2 = SETTINGS[x], SETTINGS[y]
        sig = {k: nrm(det(sense(phi1, k[0]), sense(phi2, k[1]))) for k in order}
        total = sum(sig.values())
        num = 0
        for c in range(ROOM):
            t = carry(c * total, ROOM, 0)[0]
            acc = 0
            for k in order:
                acc += sig[k]
                if t < acc:
                    num += k[0] * k[1]
                    break
        exact.append((num, ROOM))
    rng = Lcg(seed)
    meas = [[0, 0] for _ in PAIRS]
    for run in range(4 * runs_per_pair):
        p = run % 4
        x, y, _sgn = PAIRS[p]
        phi1, phi2 = SETTINGS[x], SETTINGS[y]
        lat = Lattice((8, 1, 1), W, STRETCH, LIGHT[0], LIGHT[1])
        for row in lat.fine:
            for k in range(4):
                row[k] = rng.below(W)
        n = SIX_KEYS[rng.below(6)]
        set_bob(lat, 0, chi_k(n, K))
        set_bob(lat, 1, chi_k(neg(n), K))
        for _ in range(T_A):
            lat.step()
        sig = {k: nrm(det(sense(phi1, k[0]), sense(phi2, k[1]))) for k in order}
        total = sum(sig.values())
        t = carry(lat.draw(0, ROOM) * total, ROOM, 0)[0]
        acc = 0
        for k in order:
            acc += sig[k]
            if t < acc:
                meas[p][0] += k[0] * k[1]
                meas[p][1] += 1
                break
    return exact, meas


def s_from(es):
    num, den = 0, 1
    for (e_num, e_den), (_x, _y, sgn) in zip(es, PAIRS):
        num, den = num * e_den + sgn * e_num * den, den * e_den
    return num, den


if __name__ == "__main__":
    lines = []

    def out(s=""):
        print(s)
        lines.append(s)

    out("closure24_lattice.py: draft D's lattice probe, integers only, the head's carry and mid (core/acts.py) for Rule3")
    out(f"world: W {W}, s {STRETCH}, light (g, D) {LIGHT}, heavy (g, D) {HEAVY}, bob notches K {K}, room {ROOM}, L {L} Meshes, first click at tick {T_A}")
    out("settings: a = (1, 0) axis z rho 1; a' = (1, 1) axis x rho 2; b = (5, 2) axis (20, 0, 21) rho 29; b' = (5, -2) axis (-20, 0, 21) rho 29")
    out(f"S = E(a,b) + E(a,b') + E(a',b) - E(a',b'); singlet S = -82/29 = {fmt(-82, 29)}; local isotropic S = -82/87 = {fmt(-82, 87)}; Bell's bound |S| <= 2")
    out("delta = the partner's click tick less the first click's; spacelike delta <= L - 2 (neither the partner's reading nor its draw can read the first click), edge delta = L - 1 (its draw can), timelike delta >= L (the message has arrived)")
    out()

    tr, fl = rewind_check(LIGHT, (2 * L + 2, 1, 1), 12, 40, 7)
    out(f"[rewind] the one formula forward and back across the remainder's write, ring (14,1,1), 12 ticks: {tr} trials, failures {fl}")
    tr3, fl3 = rewind_check(LIGHT, (2 * L + 2, 3, 3), 8, 8, 8)
    out(f"[rewind] the same on a torus (14,3,3), 8 ticks: {tr3} trials, failures {fl3}")
    out()

    RUNS = 2000
    summary = {}
    for label, params, seed in (("light", LIGHT, 2026), ("heavy", HEAVY, 2027)):
        tally, changed, checked = ring_runs(params, RUNS, seed)
        out(f"[A] many draws, {label} twin train, ring (14,1,1), {4 * RUNS} runs (2,000 per setting pair), hidden n and fine teeth from the LCG")
        out("    model delta kind       E(a,b)   E(a,b')  E(a',b)  E(a',b')  S         |S|>2  with A's other setting, runs where B's answer / draw / reading moved; <b> gap = |<b> under a - <b> under a'| (signalling)")
        for model in ("M0", "M1a", "M1b", "M2"):
            for delta in DELTAS:
                (sn, sd), es = s_of(tally, model, delta)
                beyond = "yes" if 4 * sd * sd < sn * sn else "no"
                gap = signal_gap([(tally[(model, delta, q)][2], tally[(model, delta, q)][1]) for q in range(4)])
                out(f"    {model:4s} {delta:3d}  {classify(delta):9s} " + " ".join(f"{fmt(*e):>8s}" for e in es) + f"  {fmt(sn, sd):>8s}  {beyond:5s}  " + " / ".join(str(v) for v in changed[(model, delta)]) + f" of {checked[delta]}   <b> gap {fmt(*gap)}")
                cell = summary.setdefault((label, model, classify(delta)), [None, None, 0, 0])
                v = tenk(sn, sd)
                cell[0] = v if cell[0] is None else min(cell[0], v)
                cell[1] = v if cell[1] is None else max(cell[1], v)
                cell[2] += changed[(model, delta)][0]
                cell[3] += checked[delta]
        out()
    out("[A summary] S x 10^4 over the deltas of each kind (lowest, highest), and the runs where B's answer moved with A's setting")
    for (label, model, kind), (lo, hi, moved_n, of_n) in sorted(summary.items()):
        out(f"    {label:5s} {model:4s} {kind:9s} S from {lo:6d} to {hi:6d}   B's answer moved in {moved_n} of {of_n}")
    out()

    for label, params in (("light", LIGHT), ("heavy", HEAVY)):
        for shape in ((2 * L + 2, 1, 1), (2 * L + 2, 3, 3)):
            deltas = [0, L - 2, L - 1, L, L + 2, L + 6, L + 14, L + 30]
            res, _ = exact_one_formula(params, shape, deltas)
            out(f"[B] exact odds (every c in [0, room) counted), M2 the one formula's own carriage, {label} train, torus {shape}, averaged over the six n")
            for delta in deltas:
                (sn, sd), es = s_exact(res, delta)
                gap = signal_gap([(res[(delta, q)][2], res[(delta, q)][1]) for q in range(4)])
                out(f"    M2  {delta:3d}  {classify(delta):9s} " + " ".join(f"{fmt(*e):>8s}" for e in es) + f"  S {fmt(sn, sd):>8s}   B's marginal gap between A's settings {fmt(*gap)}")
    out()

    for label, params in (("light", LIGHT), ("heavy", HEAVY)):
        for shape in ((2 * L + 2, 1, 1), (2 * L + 2, 3, 3)):
            deltas = [L, L + 2, L + 6, L + 14, L + 30]
            res, align = exact_one_formula(params, shape, deltas, empty_partner=True, t_a=0)
            out(f"[B'] M2e: no bob at B, A's remainder left at its fitting (tick 0); {label} train, torus {shape}")
            for delta in deltas:
                (sn, sd), es = s_exact(res, delta)
                al = [align[(delta, a)] for a in (1, -1)]
                a_num = sum(c[0] for c in al)
                a_den = sum(c[1] for c in al)
                r_b = sum(c[2] for c in al)
                r_child = sum(c[3] for c in al)
                share = f"{fmt(r_b, r_child)}" if r_child else "-"
                aligned = fmt(a_num, a_den) if a_den else "  (nothing arrived)"
                empty = sum(c[5] for c in al)
                cases = sum(c[4] for c in al)
                out(f"    M2e {delta:3d}  " + " ".join(f"{fmt(*e):>8s}" for e in es) + f"  S {fmt(sn, sd):>8s}  along -a m1: {aligned:>8s}  rho at B over a fitted hand's: {share}  nothing at B in {empty} of {cases}")
    out()

    exact, meas = link_act(RUNS, 99)
    out(f"[D] the link's one act at L = 1 (one draw at the - end over the four parts N(det[phi1^a, phi2^b])): exact over every c, and {4 * RUNS} vernier draws")
    out("    exact    " + " ".join(f"{fmt(*e):>8s}" for e in exact) + f"  S {fmt(*s_from(exact)):>8s}")
    out("    measured " + " ".join(f"{fmt(*e):>8s}" for e in meas) + f"  S {fmt(*s_from(meas)):>8s}")
