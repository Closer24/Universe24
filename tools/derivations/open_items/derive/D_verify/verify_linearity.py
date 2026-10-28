"""Verifier's attack on draft D part 4.1-4.4: how linear is the one formula once the carries act?
Own code: law 2 on a flat clock with floor-divmod as Rule3 (cross-checked against the head's carry), integers only.
Two runs of the twin train (with and without the first click's remainder write at A), and the write delta alone
propagated by the same step with every gear scaled by M = 2^80 (the exact linear map to 1/M of a notch).
Run: python3 -I -B verify_linearity.py"""

import sys

sys.path.insert(0, "/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/t24/src")
from event_universe.core.acts import carry as head_carry, mid as head_mid  # noqa: E402  (cross-check only)

W = 3 << 19
S_STRETCH = 1
LIGHT = (W // 3, W // 24)
HEAVY = (W // 96, W // 6)
MID = W // 2
M = 1 << 80


def rule3(total, d):
    return total // d, total % d


# cross-check the head's carry and mid against floor-divmod (the head's act at going +1)
bad = int(head_mid(W) != MID)
x = 12345678901234567
for _ in range(20000):
    x = (x * 6364136223846793005 + 1442695040888963407) % (1 << 64)
    tot = (x >> 3) - (1 << 59)
    f = x % W
    bad += head_carry(tot, W, f) != rule3(tot + f, W)
print(f"head carry/mid = floor-divmod on 20,000 values: failures {bad}")


class Ring:
    def __init__(self, shape, grip, spring):
        nx, ny, nz = shape
        self.sites = [(i, j, k) for i in range(nx) for j in range(ny) for k in range(nz)]
        ix = {p: n for n, p in enumerate(self.sites)}
        self.nb = []
        for (i, j, k) in self.sites:
            row = []
            for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
                q = ix[((i + d[0]) % nx, (j + d[1]) % ny, (k + d[2]) % nz)]
                if q != ix[(i, j, k)]:
                    row.append(q)
            self.nb.append(row)
        self.ix = ix
        self.g, self.D = grip, spring
        n = len(self.sites)
        self.a = [[0] * 4 for _ in range(n)]
        self.b = [[0] * 4 for _ in range(n)]
        self.r = [[MID] * 4 for _ in range(n)]

    def clone(self):
        o = Ring.__new__(Ring)
        o.__dict__.update(self.__dict__)
        o.a = [row[:] for row in self.a]
        o.b = [row[:] for row in self.b]
        o.r = [row[:] for row in self.r]
        return o

    def step(self, wd=W, md=MID):
        na, nr = [], []
        for i in range(len(self.a)):
            ra, rr = [], []
            for k in range(4):
                ai = self.a[i][k]
                force = self.g * sum(self.a[j][k] - ai for j in self.nb[i]) - self.D * ai
                p_next = wd * (ai - self.b[i][k]) + (self.r[i][k] - md) + S_STRETCH * force
                q, rem = rule3(p_next + md, wd)
                ra.append(ai + q)
                rr.append(rem)
            na.append(ra)
            nr.append(rr)
        self.b, self.a, self.r = self.a, na, nr


def gm(z, w):
    return (z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0])


def gc(z):
    return (z[0], -z[1])


def twin(row):
    return ((row[0], row[1]), (row[2], row[3]))


def set_bob(lat, i, psi):
    v = [psi[0][0], psi[0][1], psi[1][0], psi[1][1]]
    lat.a[i] = v[:]
    lat.b[i] = v[:]


def leave_remainder(lat, i, eta):
    """The draft's M2 write: both slots become <eta, psi> eta div N(eta), coefficient by coefficient."""
    rd = eta[0][0] ** 2 + eta[0][1] ** 2 + eta[1][0] ** 2 + eta[1][1] ** 2
    for slot in (lat.a, lat.b):
        psi = twin(slot[i])
        c = tuple(x + y for x, y in zip(gm(gc(eta[0]), psi[0]), gm(gc(eta[1]), psi[1])))
        part = (gm(c, eta[0]), gm(c, eta[1]))
        slot[i] = [part[0][0] // rd, part[0][1] // rd, part[1][0] // rd, part[1][1] // rd]


def reading(row):
    (x1, y1), (x2, y2) = twin(row)
    return x1 * x1 + y1 * y1 + x2 * x2 + y2 * y2, (2 * (x1 * x2 + y1 * y2), 2 * (x1 * y2 - y1 * x2), x1 * x1 + y1 * y1 - x2 * x2 - y2 * y2)


CHI = {"+z": ((1, 0), (0, 0)), "-z": ((0, 0), (1, 0)), "+x": ((1, 0), (1, 0)), "-x": ((1, 0), (-1, 0)),
       "+y": ((1, 0), (0, 1)), "-y": ((1, 0), (0, -1))}
OPP = {"+z": "-z", "-z": "+z", "+x": "-x", "-x": "+x", "+y": "-y", "-y": "+y"}
A_SET = ((1, 0), (1, 0))  # a' = (1, 1), axis x
A_PERP = ((-1, 0), (1, 0))  # its perp (-conj 1, conj 1)


def experiment(shape, params, kbob, n, ans, deltas, t_a=2, L=6, partner=True):
    base = Ring(shape, *params)
    ia, ib = base.ix[(0, 0, 0)], base.ix[(L, 0, 0)]
    set_bob(base, ia, tuple(tuple(kbob * v for v in z) for z in CHI[n]))
    if partner:
        set_bob(base, ib, tuple(tuple(kbob * v for v in z) for z in CHI[OPP[n]]))
    for _ in range(t_a):
        base.step()
    hit = base.clone()
    eta = A_PERP if ans == 1 else A_SET  # the part not taken when the answer is ans
    leave_remainder(hit, ia, eta)
    # the write delta alone, scaled by M, its fine teeth at the mid tooth (r - mid = 0): the linear map
    lin = Ring(shape, *params)
    lin.a[ia] = [M * (x - y) for x, y in zip(hit.a[ia], base.a[ia])]
    lin.b[ia] = [M * (x - y) for x, y in zip(hit.b[ia], base.b[ia])]
    out = []
    for t in range(1, max(deltas) + 1):
        base.step()
        hit.step()
        lin.step()
        if t in deltas:
            d_int = [x - y for x, y in zip(hit.a[ib], base.a[ib])]
            d_lin_scaled = lin.a[ib]
            dev = [abs(di * M - dl) for di, dl in zip(d_int, d_lin_scaled)]  # in units of 1/M notch
            size = max(abs(dl) for dl in d_lin_scaled)
            beta = max(abs(v) for v in base.a[ib])
            out.append((t, max(abs(v) for v in d_int), size // M, max(dev) // M, (max(dev) * 1000) // max(size, 1), beta,
                        reading(hit.a[ib])))
    return out


if __name__ == "__main__":
    deltas = (6, 8, 12, 20, 36)
    for label, shape, params, kbob in (
        ("light ring K=4096", (14, 1, 1), LIGHT, 4096),
        ("light torus K=4096", (14, 3, 3), LIGHT, 4096),
        ("heavy ring K=4096", (14, 1, 1), HEAVY, 4096),
        ("light ring K=8", (14, 1, 1), LIGHT, 8),
        ("light ring K=2", (14, 1, 1), LIGHT, 2),
    ):
        print(f"[{label}] n = +z, A's setting a' (x), answer +1: at B, max |d_int| (notches), max |G delta| (linear), max |d_int - G delta|, per mille of |G delta|, max |beta|")
        for t, dint, dlin, dev, pm, beta, _rd in experiment(shape, params, kbob, "+z", 1, deltas):
            print(f"    Delta {t:3d}: |d_int| {dint:6d}  |G delta| {dlin:6d}  deviation {dev:4d}  ({pm} per mille)  |beta| {beta}")
