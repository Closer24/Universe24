"""A prototype of the board as one element and one operator (ALGEBRA.md 9.19), with the
property test of 9.20, on integers, outside the engine. Not engine code.

The board: a torus of N x N x N Nodes. A family: a vacuum pair [numerator, denominator] and
a clock [n, d] (steps of the phase circle per interval). The operator of a family: its pair at
every Node (the vacuum's, a body's on its cells). A record (a summand): rows per label of two
integer levels (now, before) and the rule's remainder, one family, a residue u, a norm T, a
ladder of named sets and a content. The step: at every Node, 3 den a_next + r' = num S_6 - 3
den a_before + r (S_6 the six neighbours' sum), exact integers (8.1). The reading of a set:
the one-way inward flux through its Ports, 3 G = now_i before_j - before_i now_j summed over
the Links from outside j to inside i where positive (9.19 (3)); the norm: the record's
conserved form I (8.2), both scaled to integers by the same factor. The click: 2 T u + T <=
2 W C, then the record is deleted (8.8). The birth: the emitter's excited record (the body's
seed) clicks at its centre cell and the photon is written once on the body's cells with
before = -now (9.17 (6)); the next excitation follows while the stock lasts."""

import itertools
import math

import numpy as np

N = 8
SHAPE = (N, N, N)
STEPS = 64  # the phase circle


def s6(a):
    return sum(np.roll(a, s, axis=ax) for ax in range(3) for s in (1, -1))


def cos_table(steps):
    return [int(math.floor(256 * math.cos(2 * math.pi * k / steps) + 0.5)) for k in range(steps)]


def obj(x):
    return np.array(x, dtype=object)


class Family:
    def __init__(self, name, num, den, clock):
        self.name, self.num, self.den, self.clock = name, num, den, clock


class Record:
    def __init__(self, family, rows, u, ladder, content, born=0):
        self.family = family  # a Family
        self.rows = rows  # list of [now, before, r] per label (object arrays)
        self.u = u
        self.ladder = ladder  # set of receiver names
        self.content = content
        self.C = 0
        self.T = 0
        self.born = born
        self.alive = True


class World:
    def __init__(self):
        self.families = {}
        self.num = {}  # family name -> array of numerators per Node
        self.den = {}
        self.receivers = {}  # name -> boolean mask
        self.W = 8
        self.emitter = None  # dict: body mask, family, born family, stock, centre mask, norm
        self.residues = []  # the declared permutation of Z_W
        self.next_residue = 0
        self.records = []
        self.tick = 0
        self.clicks = []
        self.log = []

    def add_family(self, f):
        self.families[f.name] = f
        self.num[f.name] = np.full(SHAPE, f.num, dtype=object)
        self.den[f.name] = np.full(SHAPE, f.den, dtype=object)

    # ---- the operator of a family and its modes (the generator's computation, float)
    def operator(self, fam):
        num, den = self.num[fam].astype(float), self.den[fam].astype(float)
        ratio = den / num
        sc = 1 / np.sqrt(ratio)
        n = N**3
        A = np.zeros((n, n))
        idx = np.arange(n).reshape(SHAPE)
        for ax in range(3):
            for s in (1, -1):
                nb = np.roll(idx, s, axis=ax)
                A[idx.ravel(), nb.ravel()] += 1
        M = (sc.ravel()[:, None] * A * sc.ravel()[None, :]) / 3
        return M, sc

    def bound_mode(self, fam):
        M, sc = self.operator(fam)
        w, v = np.linalg.eigh(M)
        lam = w[-1]
        mode = (v[:, -1] * sc.ravel()).reshape(SHAPE)
        mode = mode / np.abs(mode).max()
        if mode.ravel()[np.argmax(np.abs(mode))] < 0:
            mode = -mode
        return lam, mode

    # ---- the rule
    def step_record(self, rec, inverse=False):
        num, den = self.num[rec.family.name], self.den[rec.family.name]
        wall = 3 * den
        for row in rec.rows:
            now, before, r = row
            if not inverse:
                m = num * s6(now) - wall * before + r
                nxt = m // wall
                r2 = m % wall
                row[0], row[1], row[2] = nxt, now, r2
            else:
                # 8.8's inverse: from (now = a_next, before = a_now, r' ) recover (a_before, r)
                a_next, a_now, r_next = now, before, r
                m = num * s6(a_now) - wall * a_next - r_next  # = 3 den a_before - r
                a_before = -((-m) // wall)  # ceil(m / wall)
                r_prev = wall * a_before - m
                row[0], row[1], row[2] = a_now, a_before, r_prev

    def form_I(self, rec):
        """The conserved form 8.2, scaled by 3 x the family's vacuum numerator to an integer."""
        num, den = self.num[rec.family.name], self.den[rec.family.name]
        L = rec.family.num
        total = 0
        for now, before, _ in rec.rows:
            # I = sum D_i (now_i^2 + before_i^2) - (1/3) now . A before, D_i = den_i / num_i
            d_term = (3 * L * den * (now * now + before * before)) // num  # exact where num | L
            total += int(np.sum(d_term)) - L * int(np.sum(now * s6(before)))
        return total

    def flux_into(self, rec, mask):
        """3 x the one-way inward flux into the set `mask` through its Ports this interval."""
        L = rec.family.num
        total = 0
        outside = ~mask
        for now, before, _ in rec.rows:
            for ax in range(3):
                for s in (1, -1):
                    nb_now = np.roll(now, s, axis=ax)
                    nb_before = np.roll(before, s, axis=ax)
                    nb_out = np.roll(outside, s, axis=ax)
                    g = now * nb_before - before * nb_now
                    g = np.where(mask & nb_out, g, 0)
                    g = np.where(g > 0, g, 0)
                    total += int(np.sum(g))
        return 3 * L * total

    # ---- births
    def written_pair(self, fam):
        """9.17 (6): the character half a step either side of its zero, on the circle of 2 N."""
        n, d = fam.clock
        s = n // d
        table = cos_table(2 * STEPS)
        now = table[(3 * STEPS // 2 + s) % (2 * STEPS)]
        return now, -now

    def birth_photon(self, mask, amplitude):
        em = self.emitter
        fam = self.families[em["born"]]
        now_v, before_v = self.written_pair(fam)
        rows = []
        for _ in range(2):  # two labels, equal rows (the branches [[0, 1], [1, 1]])
            now = np.zeros(SHAPE, dtype=object)
            before = np.zeros(SHAPE, dtype=object)
            now[mask] = amplitude * now_v
            before[mask] = amplitude * before_v
            rows.append([now, before, np.zeros(SHAPE, dtype=object)])
        u = self.residues[self.next_residue % len(self.residues)]
        self.next_residue += 1
        rec = Record(fam, rows, u, em["ladder"], 1, born=self.tick)
        rec.T = self.form_I(rec)
        return rec

    def excite(self):
        em = self.emitter
        fam = self.families[em["family"]]
        seed = em["seed"]
        rows = [[seed.copy(), seed.copy(), np.zeros(SHAPE, dtype=object)]]
        u = self.residues[self.next_residue % len(self.residues)]
        self.next_residue += 1
        rec = Record(fam, rows, u, set(), 1)
        rec.T = em["norm"]
        rec.excited = True
        return rec

    # ---- one interval of the whole element
    def step(self):
        for rec in self.records:
            self.step_record(rec)
        self.tick += 1
        # the readings and the clicks
        births = []
        for rec in self.records:
            if not rec.alive:
                continue
            if getattr(rec, "excited", False):
                em = self.emitter
                rec.C += self.flux_into(rec, em["centre"])
                if 2 * rec.T * rec.u + rec.T <= 2 * self.W * rec.C:
                    rec.alive = False
                    self.clicks.append(("emitter", self.tick, rec.u))
                    births.append(("photon", em["body"]))
                    em["stock"] -= 1
                    if em["stock"] > 0:
                        births.append(("excite", None))
            else:
                for name in rec.ladder:
                    rec.C += self.flux_into(rec, self.receivers[name])
                if rec.ladder and 2 * rec.T * rec.u + rec.T <= 2 * self.W * rec.C:
                    rec.alive = False
                    self.clicks.append(("receiver", self.tick, rec.u, rec.born, rec.C, rec.T))
        self.records = [r for r in self.records if r.alive]
        for kind, mask in births:
            if kind == "photon":
                self.records.append(self.birth_photon(mask, self.emitter["amplitude"]))
            else:
                self.records.append(self.excite())

    def state(self):
        """The one element: every record's rows, in order, as one tuple of arrays."""
        return [
            (rec.family.name, rec.u, [tuple(a.copy() for a in row) for row in rec.rows])
            for rec in self.records
        ]


# ---------------------------------------------------------------- the small world of 9.20
def cube_mask(vertex, side):
    m = np.zeros(SHAPE, dtype=bool)
    for dx in range(side):
        for dy in range(side):
            for dz in range(side):
                m[(vertex[0] + dx) % N, (vertex[1] + dy) % N, (vertex[2] + dz) % N] = True
    return m


def build(
    with_receiver=True,
    well_pair=(800, 801),
    receiver_cell=(6, 6, 1),
    well_vertex=(1, 2, 3),
    side=2,
    amplitude=1 << 12,
    residues=None,
    W=8,
):
    w = World()
    w.W = W
    w.add_family(Family("light", 1, 1, (77, 25)))
    w.add_family(Family("matter", 800, 809, (0, 1)))
    body = cube_mask(well_vertex, side)
    w.num["matter"][body] = well_pair[0]
    w.den["matter"][body] = well_pair[1]
    centre = np.zeros(SHAPE, dtype=bool)
    centre[well_vertex] = True
    lam, mode = w.bound_mode("matter")
    seed = obj(np.rint(mode * amplitude).astype(np.int64))
    if with_receiver:
        w.receivers["screen"] = cube_mask(receiver_cell, 1)
    w.residues = list(residues) if residues is not None else [(3 * k) % W for k in range(W)]
    w.emitter = {
        "body": body,
        "centre": centre,
        "family": "matter",
        "born": "light",
        "stock": 3,
        "seed": seed,
        "amplitude": 200,
        "ladder": {"screen"} if with_receiver else set(),
        "norm": 0,
    }
    # the excited record's norm: the one-way flux into the centre over one period of the mode (the generator's integer)
    omega = math.acos(lam / 2)
    period = int(round(2 * math.pi / omega))
    probe = World()
    probe.add_family(Family("matter", 800, 809, (0, 1)))
    probe.num["matter"][body] = well_pair[0]
    probe.den["matter"][body] = well_pair[1]
    rec = Record(
        probe.families["matter"],
        [[seed.copy(), seed.copy(), np.zeros(SHAPE, dtype=object)]],
        0,
        set(),
        1,
    )
    total = 0
    for _ in range(period):
        probe.step_record(rec)
        total += probe.flux_into(rec, centre)
    w.emitter["norm"] = total
    w.emitter["period"] = period
    w.emitter["lambda"] = lam
    w.records.append(w.excite())
    return w


def transform_index(g):
    """g = (perm, signs): x -> (s_0 x_perm0, ...) mod N; returns the index map new <- old."""
    perm, signs = g
    src = np.indices(SHAPE).reshape(3, -1)
    dst = np.empty_like(src)
    for k in range(3):
        dst[k] = (signs[k] * src[perm[k]]) % N
    return src, dst


def apply_g(arr, g):
    src, dst = transform_index(g)
    out = np.empty_like(arr)
    out[dst[0], dst[1], dst[2]] = arr[src[0], src[1], src[2]]
    return out


def det(g):
    perm, signs = g
    p = np.zeros((3, 3))
    for k in range(3):
        p[k, perm[k]] = signs[k]
    return int(round(np.linalg.det(p)))


def transform_world(w, g):
    """The world's declared data and its element carried by g (positions; the hand's sign on the labels)."""
    t = World()
    t.W = w.W
    for f in w.families.values():
        t.add_family(Family(f.name, f.num, f.den, f.clock))
        t.num[f.name] = apply_g(w.num[f.name], g)
        t.den[f.name] = apply_g(w.den[f.name], g)
    t.receivers = {k: apply_g(m, g) for k, m in w.receivers.items()}
    t.residues = list(w.residues)
    t.next_residue = w.next_residue
    t.tick = w.tick
    em = w.emitter
    t.emitter = dict(
        em, body=apply_g(em["body"], g), centre=apply_g(em["centre"], g), seed=apply_g(em["seed"], g)
    )
    for rec in w.records:
        rows = [[apply_g(a, g) for a in row] for row in rec.rows]
        if det(g) < 0 and len(rows) == 2:
            rows = [rows[1], rows[0]]  # a reflection exchanges the two hands
        nr = Record(t.families[rec.family.name], rows, rec.u, set(rec.ladder), rec.content, rec.born)
        nr.T, nr.C = rec.T, rec.C
        if getattr(rec, "excited", False):
            nr.excited = True
        t.records.append(nr)
    return t


def same(w1, w2):
    s1, s2 = w1.state(), w2.state()
    if len(s1) != len(s2):
        return False
    for (f1, u1, r1), (f2, u2, r2) in zip(s1, s2, strict=True):
        if f1 != f2 or u1 != u2 or len(r1) != len(r2):
            return False
        for a, b in zip(r1, r2, strict=True):
            for x, y in zip(a, b, strict=True):
                if not np.array_equal(x, y):
                    return False
    return True


def run(w, intervals):
    for _ in range(intervals):
        w.step()
    return w


def all_48():
    out = []
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product((1, -1), repeat=3):
            out.append((perm, signs))
    return out


def main():
    print(f"the board: {N}^3 torus, N = {STEPS} phase steps")
    # ---- the initial state given by the algebra: the composed operator's bound mode
    w0 = build()
    lam = w0.emitter["lambda"]
    omega = math.acos(lam / 2)
    print(
        f"the well [800, 801] on [800, 809], side 2: largest eigenvalue {lam:.6f} (< 2: stable), omega_b {omega:.5f}, "
        f"the vacuum's omega_0 {math.acos(800 / 809):.5f} (bound: omega_b < omega_0), period {w0.emitter['period']}; "
        f"the excited record's norm T (one period's one-way flux into the centre) = {w0.emitter['norm']}"
    )
    # the standing start: the seed alone stays the mode (relative change of I over one period)
    probe = build(with_receiver=False)
    probe.emitter["stock"] = 1
    rec = probe.records[0]
    I0 = probe.form_I(rec)
    centre_now = [int(rec.rows[0][0][1, 2, 3])]
    for _ in range(probe.emitter["period"]):
        probe.step_record(rec)
        centre_now.append(int(rec.rows[0][0][1, 2, 3]))
    I1 = probe.form_I(rec)
    crossings = sum(1 for a, b in zip(centre_now, centre_now[1:], strict=False) if (a < 0) != (b < 0))
    print(
        f"the seed alone over one period: I {I0} -> {I1} (relative change {abs(I1 - I0) / I0:.2e}); "
        f"sign changes at the centre {crossings} (a rotation at omega_b gives 2)"
    )

    # ---- the emitter clicks, the photon is born and clicks at the screen
    w = build()
    run(w, 400)
    em_clicks = [c for c in w.clicks if c[0] == "emitter"]
    rc_clicks = [c for c in w.clicks if c[0] == "receiver"]
    print(
        f"emitter clicks (interval, u): {[(c[1], c[2]) for c in em_clicks]}; the wait for u over W = {w.W}: "
        f"expected about (2u+1)/(2W) x period = {[round((2 * c[2] + 1) / (2 * w.W) * w.emitter['period']) for c in em_clicks]}"
    )
    print(
        f"receiver clicks (interval, u, born, C, T): {[(c[1], c[2], c[3], c[4], c[5]) for c in rc_clicks]}; "
        f"the Manhattan distance body->screen is {abs(6 - 1) + abs(6 - 2) + abs(1 - 3)} Links"
    )

    # ---- 9.20 (1) equivariance under the 48
    ref = build()
    run(ref, 40)
    ok = 0
    fails = []
    for g in all_48():
        tw = transform_world(build(), g)
        run(tw, 40)
        if same(tw, transform_world(ref, g)) and tw.clicks == ref.clicks:
            ok += 1
        else:
            fails.append(g)
    print(
        f"(1) equivariance under the 48 over 40 intervals: {ok} of 48 identical bit for bit"
        + (f"; failing {fails[:3]}" if fails else "")
    )

    # ---- 9.20 (2) translation
    ok = 0
    shifts = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1), (3, 5, 7)]
    for sh in shifts:
        tw = build(
            receiver_cell=tuple((np.array((6, 6, 1)) + sh) % N),
            well_vertex=tuple((np.array((1, 2, 3)) + sh) % N),
        )
        run(tw, 40)
        moved = ref.state()
        good = len(tw.state()) == len(moved)
        for (_f1, _u1, r1), (_f2, _u2, r2) in zip(tw.state(), moved, strict=False):
            for a, b in zip(r1, r2, strict=True):
                for x, y in zip(a, b, strict=True):
                    good = good and np.array_equal(x, np.roll(y, sh, axis=(0, 1, 2)))
        ok += good and tw.clicks == ref.clicks
    print(f"(2) translation on the torus, 7 shifts: {ok} of 7 identical")

    # ---- 9.20 (3) conservation between clicks: content and I per record
    w = build()
    w.emitter["stock"] = 1
    w.emitter["stock"] = 3
    contents = []
    for _t in range(200):
        w.step()
        photons = [r for r in w.records if not getattr(r, "excited", False)]
        contents.append(
            len(photons) + len([c for c in w.clicks if c[0] == "receiver"]) + w.emitter["stock"]
        )
    print(
        f"(3a) content: photons alive + photons clicked + the stock's excitations, constant at every interval: {len(set(contents)) == 1} (value {contents[0]}, {len(w.clicks)} clicks)"
    )
    for amp in (1 << 12, 1 << 16):
        w = build(with_receiver=False, amplitude=amp)
        w.emitter["stock"] = 1
        rec = w.records[0]
        I0 = w.form_I(rec)
        drift = 0.0
        for _t in range(120):
            w.step_record(rec)
            drift = max(drift, abs(w.form_I(rec) - I0) / I0)
        print(
            f"(3b) the form I of the seed over 120 intervals at the amplitude {amp}: largest relative drift {drift:.2e}"
        )
    # (3c) momentum on the homogeneous board: a plane wave along x keeps its wave number
    hw = World()
    hw.add_family(Family("light", 1, 1, (77, 25)))
    k = 2 * math.pi / N
    x = np.indices(SHAPE)[0]
    omega_k = math.acos((math.cos(k) + 2) / 3)
    now = obj(np.rint(4096 * np.cos(k * x)).astype(np.int64))
    before = obj(np.rint(4096 * np.cos(k * x + omega_k)).astype(np.int64))
    rec = Record(hw.families["light"], [[now, before, np.zeros(SHAPE, dtype=object)]], 0, set(), 1)
    peaks = []
    for _ in range(60):
        hw.step_record(rec)
        spec = np.abs(np.fft.fftn(rec.rows[0][0].astype(float)))
        spec[0, 0, 0] = 0
        peaks.append(np.unravel_index(np.argmax(spec), SHAPE))
    print(
        f"(3c) a plane wave's wave number on the homogeneous board over 60 intervals: the spectral peak stays at {peaks[0]}: {len(set(peaks)) == 1}"
    )

    # ---- 9.20 (4) reversibility except the click
    w = build(with_receiver=False)
    w.emitter["stock"] = 1
    start = w.state()
    for _ in range(40):
        for rec in w.records:
            w.step_record(rec)
    for _ in range(40):
        for rec in w.records:
            w.step_record(rec, inverse=True)
    back = w.state()
    rev = all(
        np.array_equal(x, y)
        for (_, _, r1), (_, _, r2) in zip(start, back, strict=True)
        for a, b in zip(r1, r2, strict=True)
        for x, y in zip(a, b, strict=True)
    )
    print(
        f"(4) reversibility: 40 steps forward then 40 of 8.8's inverse return the element bit for bit, remainders included: {rev}"
    )
    # with a click: everything but the deleted summand returns
    w = build()
    run(w, 400)
    n_after = len(w.records)
    print(
        f"    with clicks: {len(w.clicks)} clicks deleted {len(w.clicks)} summands; {n_after} summands remain; the deleted rows are not recoverable by the inverse (the one deletion)"
    )

    # ---- 9.20 (5) locality
    w1 = build(with_receiver=False)
    w2 = build(with_receiver=False)
    w1.emitter["stock"] = w2.emitter["stock"] = 1
    w2.records[0].rows[0][0][4, 4, 4] += 1
    inside = True
    nonzero = True
    for m in range(1, 8):
        for rec in (w1.records[0], w2.records[0]):
            (w1 if rec is w1.records[0] else w2).step_record(rec)
        diff = (w2.records[0].rows[0][0] != w1.records[0].rows[0][0]) | (
            w2.records[0].rows[0][2] != w1.records[0].rows[0][2]
        )
        ix = np.indices(SHAPE)
        dist = sum(np.minimum((ix[a] - 4) % N, (4 - ix[a]) % N) for a in range(3))
        inside = inside and not np.any(diff & (dist > m))
        nonzero = nonzero and np.any(diff)
    print(
        f"(5) locality: a one-unit change at one Node stays inside the Manhattan ball of radius m at interval m (m = 1..7): {inside}; nonzero at every m: {nonzero}"
    )

    # ---- 9.20 (6) only the click reads: residue blindness
    wa = build(residues=[0] * 8)
    wb = build(residues=[7] * 8)
    identical = True
    first_click = None
    for t in range(200):
        wa.step()
        wb.step()
        if wa.clicks or wb.clicks:
            first_click = t + 1
            break
        rows_a = [row for rec in wa.records for row in rec.rows]
        rows_b = [row for rec in wb.records for row in rec.rows]
        identical = (
            identical
            and len(rows_a) == len(rows_b)
            and all(
                np.array_equal(x, y)
                for a, b in zip(rows_a, rows_b, strict=True)
                for x, y in zip(a, b, strict=True)
            )
        )
    print(
        f"(6c) two runs differing only in their residues are identical bit for bit until the first click (at interval {first_click}): {identical}"
    )
    # equal inputs give equal outputs: the step at a Node is a function of its seven inputs
    rng = np.random.default_rng(0)
    w = build(with_receiver=False)
    ok = 0
    for _ in range(1000):
        now = obj(rng.integers(-1000, 1000, SHAPE))
        before = obj(rng.integers(-1000, 1000, SHAPE))
        r = obj(rng.integers(0, 3 * 809, SHAPE))
        # make Node (2,2,2) and Node (5,5,5) have equal inputs: same pair (vacuum), same self and neighbours, same r
        for arr in (now, before):
            for d in [(0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
                arr[(5 + d[0]) % N, (5 + d[1]) % N, (5 + d[2]) % N] = arr[
                    (2 + d[0]) % N, (2 + d[1]) % N, (2 + d[2]) % N
                ]
        r[5, 5, 5] = r[2, 2, 2]
        rec = Record(w.families["matter"], [[now, before, r]], 0, set(), 1)
        w.step_record(rec)
        ok += (
            rec.rows[0][0][2, 2, 2] == rec.rows[0][0][5, 5, 5]
            and rec.rows[0][2][2, 2, 2] == rec.rows[0][2][5, 5, 5]
        )
    print(f"(6b) equal seven inputs give equal outputs at two Nodes: {ok} of 1000")


if __name__ == "__main__":
    main()
