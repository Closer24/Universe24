"""COMPUTATION on the algebra (no engine run, no box): the cube's own
binding threshold on the INFINITE board for the well of the pair, in the stable
massive form 3 den(x)(a_next + a_before) = num SUM6, D(x) = den/num = 1 + mu_in(x)^2/2.

At the band's top (2 cos omega = 2/D_out) the mode obeys (2 - L/3) a = (2/D_out) delta a,
delta = (mu^2 - mu_in^2)/2 = g/2 on the cube, so a bound mode exists iff the largest
eigenvalue of (g/D_out) G_0 restricted to the cube exceeds 1, G_0 = (2 - L/3)^-1 the
massless lattice Green's function, G_0(r) = INT_0^inf PROD_i ive(r_i, 2t/3) dt
(the Bessel representation; G_0(0) = W_3 / 2 with W_3 = 1.516386 Watson's integral for the
simple cubic walk, since 2 - (2/3) SUM cos k = 2 (1 - (1/3) SUM cos k)). With
Lambda(s) the largest eigenvalue of G_0 on the s-cube (uniform well):
    g_c(s) = D_out / Lambda(s)                      (binding)
    g_tach(s) = mu^2 + 1 / Lambda(s)                (the mode's omega reaches 0: growth;
                                                     by the checkerboard symmetry S L S = -L
                                                     the corner mode leaves the band at the
                                                     same g, so this is the one ceiling)
The reversed-mass window of a cube: g_c(s) < g < g_tach(s), of width about mu^2.
Light in an index lump (D >= 1 inside, D = 1 outside) binds never: the operator's
norm is bounded by the continuum's top, checked once on a box at the end.

    PYTHONPATH=src python docs/designs/detector_law/massive_cube_threshold.py
"""

import time

import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import LinearOperator, eigsh
from scipy.special import erf, ive

S = 60
t0 = time.time()
# the Green's function table G(a, b, c), 0 <= a, b, c <= S-1
T = 4.0e4
grid = np.concatenate([np.linspace(0, 1, 201)[:-1], np.exp(np.linspace(0, np.log(T), 6000))])
x = 2 * grid / 3
w = np.zeros_like(grid)
w[1:-1] = (grid[2:] - grid[:-2]) / 2
w[0] = (grid[1] - grid[0]) / 2
w[-1] = (grid[-1] - grid[-2]) / 2
R = np.arange(S)
IV = np.array([ive(r, x) for r in R])  # (S, n)
IVw = IV * w
G = np.einsum("ai,bi,ci->abc", IVw, IV, IV, optimize=True)
# the tail beyond T from the asymptotic PROD ive ~ (2 pi x)^-3/2 exp(-rho^2/(2x)), dt = (3/2) dx
X = 2 * T / 3
A, B, C = np.meshgrid(R, R, R, indexing="ij")
rho = np.sqrt(A**2 + B**2 + C**2).astype(float)
tail = np.where(
    rho > 0,
    (3 / 2)
    * (2 * np.pi) ** -1.5
    * np.sqrt(2 * np.pi)
    / np.maximum(rho, 1e-12)
    * erf(rho / np.sqrt(2 * X)),
    (3 / 2) * (2 * np.pi) ** -1.5 * 2 / np.sqrt(X),
)
G = G + tail
W3 = 1.516386059151978
print(
    f"G_0(0) = {G[0, 0, 0]:.6f} against W_3 / 2 = {W3 / 2:.6f}; G_0(1,0,0) = {G[1, 0, 0]:.6f} (the identity (2 - L/3) G = delta at 0: 2 G(0) - 2 G(1) = {2 * G[0, 0, 0] - 2 * G[1, 0, 0]:.6f}); table in {time.time() - t0:.0f} s"
)


def lambda_cube(s):
    """The largest eigenvalue of G_0 restricted to the s-cube (FFT convolution)."""
    idx = np.abs(np.arange(-(s - 1), s))
    K = G[np.ix_(idx, idx, idx)]
    n = 2 * s - 1
    Kf = np.fft.rfftn(np.roll(K, -(s - 1), axis=(0, 1, 2)), s=(n, n, n), axes=(0, 1, 2))

    def mv(v):
        V = np.zeros((n, n, n))
        V[:s, :s, :s] = v.reshape(s, s, s)
        return np.fft.irfftn(np.fft.rfftn(V) * Kf, s=(n, n, n), axes=(0, 1, 2))[:s, :s, :s].ravel()

    if s == 1:
        return G[0, 0, 0]
    op = LinearOperator((s**3, s**3), matvec=mv, dtype=float)
    return eigsh(op, k=1, which="LA", tol=1e-7, ncv=20, return_eigenvectors=False)[0]


sides = list(range(1, 25)) + list(range(26, 61, 2))
Lam = {}
print(
    "s | Lambda(s) | g_c(s) at mu = 0.05 | g_c s^2 | the sphere's pi^2 c^2 / (s/2)^2 = 3.290 / s^2 -> g s^2"
)
for s in sides:
    Lam[s] = lambda_cube(s)
    gc = (1 + 0.05**2 / 2) / Lam[s]
    print(f"{s:2d} | {Lam[s]:9.4f} | {gc:.5f} | {gc * s * s:.3f} | 3.290")
print(f"(the table took {time.time() - t0:.0f} s)")

print(
    f"\nReviewer 3's one-Node well (11.6): g_c = 1.319; this table's g_c(1) = D_out / G_0(0) = {(1 + 0.05**2 / 2) / Lam[1]:.4f} = D_out x 2 / W_3 ({2 / W3:.4f}): the same number"
)

for mu in (0.05, 0.15):
    D_out = 1 + mu**2 / 2
    for name, g in (("mu^2 / 2", mu**2 / 2), ("mu^2", mu**2)):
        s_min = next((s for s in sides if D_out / Lam[s] <= g), None)
        sphere = 2 * np.sqrt(0.8225 / g)
        print(
            f"mu = {mu}: g = {name} = {g:.5f}: the smallest side that binds on the infinite board: s = {s_min}"
            f" (g_c({s_min}) = {D_out / Lam[s_min]:.5f}; the previous side {D_out / Lam[sides[sides.index(s_min) - 1]]:.5f}); the sphere's side 2 sqrt(0.8225/g) = {sphere:.1f}"
        )

mu = 0.05
s = 12
gc, gt = (1 + mu**2 / 2) / Lam[s], mu**2 + 1 / Lam[s]
print(
    f"\nthe reversed-mass window of a 12-cube at mu = {mu}: bound for g > {gc:.5f} (mu_in^2 = mu^2 - g = {mu**2 - gc:+.5f}, reversed),"
    f" growth for g > {gt:.5f} (the mode's omega_0 -> 0; the corner leaves the band at the same g by S L S = -L); the window's width {gt - gc:.5f} = mu^2 (1 - 1/(2 Lambda)) = {mu**2 * (1 - 1 / (2 * Lam[s])):.5f}"
)
print(
    f"a scratch box scaling (zero faces, boxes to 96^3, HISTORY) read side 36 near threshold and 44 bound at g = mu^2 = 0.0025; this exact table gives g_c(36) = {(1 + mu**2 / 2) / Lam[36]:.5f} and g_c(44) = {(1 + mu**2 / 2) / Lam[44]:.5f}: side 36 IS bound, weakly, and the box's confinement hid it; the box is superseded by this table"
)
print(
    f"the cube's constant: g_c(s) s^2 -> {(1 + mu**2 / 2) / Lam[60] * 3600:.3f} (the sphere with R = s/2 gives 3.290, the equal-volume sphere 2.14)"
)


# light in an index lump binds never: ||D^-1/2 (L/3) D^-1/2|| <= ||L/3|| = 2 = the continuum's top
# when D >= 1 inside and D = 1 outside; checked once on a 32^3 box with zero faces (n^2 = 2 in a 12-cube)
nb = 32
o = np.ones(nb - 1)
S1 = sp.diags([o, o], [-1, 1], shape=(nb, nb))
I1 = sp.identity(nb)
Lb = (sp.kron(sp.kron(S1, I1), I1) + sp.kron(sp.kron(I1, S1), I1) + sp.kron(sp.kron(I1, I1), S1)).tocsr()
xb = np.arange(nb) - (nb - 1) / 2
Xb, Yb, Zb = np.meshgrid(xb, xb, xb, indexing="ij")
lump = ((np.abs(Xb) < 6) & (np.abs(Yb) < 6) & (np.abs(Zb) < 6)).ravel()
Dl = np.where(lump, 2.0, 1.0)
dl = 1 / np.sqrt(Dl)
lam_light = eigsh(sp.diags(dl) @ (Lb / 3) @ sp.diags(dl), k=1, which="LA", return_eigenvectors=False)[0]
print(
    f"\nLIGHT in an index lump (n^2 = 2 in a 12-cube, a 32^3 box): lambda_max = {lam_light:.6f} against the continuum's top 2: bound = {lam_light > 2}; the norm bound is exact"
)
