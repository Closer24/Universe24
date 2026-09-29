"""A check of the shape theorem: the top mode of Rule3's operator for a one-Node well on a 3D lattice, its symmetry under the 48, and its decay along the axis and the diagonals against the support function of the evanescent surface."""

import itertools
import math

import numpy as np

NUM, DEN, GAMMA, COUNT, N = 2, 3, 12000, 4000, 41
c = N // 2
level = np.zeros((N, N, N))
level[c, c, c] = COUNT  # the well: the count at one Node (divisor 1)
p0 = GAMMA - level  # the clock's pace: the level once
pa = p0 - level  # the Link's pace: the level twice
w = 6 * DEN * GAMMA**2
R = 2 * NUM * pa**2 / w  # the same on the three axes (isotropic well)
S = (12 * DEN * GAMMA**2 - 12 * (DEN - NUM) * p0**2 - 4 * NUM * 3 * pa**2) / w


def M(a):
    out = S * a
    for axis in range(3):
        up = np.roll(a, 1, axis)
        up[(slice(None),) * axis + (0,)] = 0  # open faces: 0 beyond
        dn = np.roll(a, -1, axis)
        dn[(slice(None),) * axis + (N - 1,)] = 0
        out += R * (up + dn)
    return out


rng = np.random.default_rng(7)
a = rng.random((N, N, N)) + 0.1  # an asymmetric random seed
shift = 3.0
for _ in range(600):
    b = M(a) + shift * a
    a = b / np.abs(b).max()
lam = (M(a) * a).sum() / (a * a).sum()
cosw = lam / 2
Lam = 3 * DEN / NUM * cosw
print(
    f"top eigenvalue 2cos w_b = {lam:.5f}, cos w_b = {cosw:.5f}, w_b = {math.acos(cosw):.4f}, Lambda = {Lam:.4f}"
)
print(f"positive everywhere: {bool((a > 0).all())}")
# symmetry under the 48: every signed permutation of the axes about the centre
worst = 0.0
for perm in itertools.permutations(range(3)):
    for signs in itertools.product((1, -1), repeat=3):
        g = np.transpose(a, perm)
        for ax, sgn in enumerate(signs):
            if sgn < 0:
                g = np.flip(g, ax)
        worst = max(worst, float(np.abs(g - a).max() / a.max()))
print(f"largest asymmetry under the 48 (relative to the peak): {worst:.2e}")
# the decay rates measured far from the well, against the support function
kx_pred = math.acosh(Lam - 2)
q_face = math.acosh((Lam - 1) / 2)
q_body = math.acosh(Lam / 3)
d = 12
ax_meas = -math.log(a[c + d + 1, c, c] / a[c + d, c, c])
face_meas = -math.log(
    a[c + d + 1, c + d + 1, c] / a[c + d, c + d, c]
)  # one diagonal step: two axis steps
body_meas = -math.log(a[c + d + 1, c + d + 1, c + d + 1] / a[c + d, c + d, c + d])
print(
    f"axis:          measured kappa {ax_meas:.4f}   predicted acosh(Lambda-2) = {kx_pred:.4f}   law's table at 4,000: 1.016"
)
print(
    f"face diagonal: measured per step {face_meas:.4f}   predicted 2 acosh((Lambda-1)/2) = {2 * q_face:.4f}   L1 seed would give 2 kappa = {2 * kx_pred:.4f}"
)
print(
    f"body diagonal: measured per step {body_meas:.4f}   predicted 3 acosh(Lambda/3) = {3 * q_body:.4f}   L1 seed would give 3 kappa = {3 * kx_pred:.4f}"
)
print(
    f"per unit length: axis {kx_pred:.4f}, face {math.sqrt(2) * q_face:.4f}, body {math.sqrt(3) * q_body:.4f}"
)


# the shape of a level set: the distance along the axis and along the body diagonal at which the mode falls to 1e-4 of the peak
def dist_to(frac, direction):
    for k in range(1, c):
        i = tuple(c + k * s for s in direction)
        if a[i] / a[c, c, c] < frac:
            return k * math.sqrt(sum(s * s for s in direction))
    return None


print(
    f"level set 1e-4: along the axis {dist_to(1e-4, (1, 0, 0)):.2f} Links, along the body diagonal {dist_to(1e-4, (1, 1, 1)):.2f} Links (a sphere would be equal; an L1 octahedron would give the ratio 1/sqrt3 = {1 / math.sqrt(3):.2f})"
)

# the far field carries the prefactor 1/r beside e^{-kappa r}: the rate per step corrected by ln((d+1)/d)
print("--- with the 1/r prefactor of the three-dimensional far field removed ---")
for d in (8, 12, 16):
    corr = math.log((d + 1) / d)
    ax_m = -math.log(a[c + d + 1, c, c] / a[c + d, c, c]) - corr
    fa_m = -math.log(a[c + d + 1, c + d + 1, c] / a[c + d, c + d, c]) - corr
    bo_m = -math.log(a[c + d + 1, c + d + 1, c + d + 1] / a[c + d, c + d, c + d]) - corr
    print(
        f"d = {d}: axis {ax_m:.4f} (pred {kx_pred:.4f}), face {fa_m:.4f} (pred {2 * q_face:.4f}), body {bo_m:.4f} (pred {3 * q_body:.4f})"
    )
print(
    "r * a(r) along the axis (constant if the prefactor is 1/r):",
    [f"{(k * a[c + k, c, c] * math.exp(kx_pred * k)):.3e}" for k in (6, 9, 12, 15)],
)
