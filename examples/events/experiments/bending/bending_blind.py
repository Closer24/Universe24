"""THE BENDING's blind expectation for the world `bending.json` (COMPUTED, no run of the engine): a light packet of the charge family
([1, 1], wavelength 5 Links, k = 2 pi / 5 along +x) moves by the geometric optics of its band, x' = d omega / d k, k' = - d omega / d x,
with 2 cos omega = 2 - (2/3) SUM_a P_a^2 (1 - cos k_a) at the paces P_0 = 1 - U + U^2 / 2, P_a = 1 - 2U (the law's line) or P_a = P_0
(the Link once, main today), U = c(x, y) / Gamma with c the plane's rest of the world's bodies (the discrete Poisson, SUM (phi_j - phi_i)
= -3 count_i / E_s, phi = 0 beyond the open faces); the shift at the screen x = 260 against the twin (a straight line), and its
ratio F to the row's 4 U_b L with U_b = c(60, 83) / Gamma and L = 200."""

import json
from pathlib import Path

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spl
from scipy.integrate import solve_ivp
from scipy.interpolate import RegularGridInterpolator

HERE = Path(__file__).resolve().parent
GAMMA = 10000.0


def plane_rest(divisor):
    """The plane's rest of the world's bodies: SUM over the four plane neighbours (phi_j - phi_i) = -3 count_i / E_s, phi = 0 beyond the open faces."""
    world = json.load(open(HERE / "bending.json", encoding="utf-8"))
    nx, ny, _ = world["shape"]
    source = np.zeros((nx, ny))
    for body in world["measured"]:
        for node in body["nodes"]:
            x, y, _ = node["node"]
            source[x, y] += node["count"]
    rows, cols, vals = [], [], []
    for x in range(nx):
        for y in range(ny):
            i = x * ny + y
            rows.append(i)
            cols.append(i)
            vals.append(-4.0)
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                xx, yy = x + dx, y + dy
                if 0 <= xx < nx and 0 <= yy < ny:
                    rows.append(i)
                    cols.append(xx * ny + yy)
                    vals.append(1.0)
    matrix = sp.csr_matrix((vals, (rows, cols)), shape=(nx * ny, nx * ny))
    return spl.spsolve(matrix, -3.0 * source.reshape(-1) / divisor).reshape(nx, ny)


K0 = 2 * np.pi / 5
X0, Y0, XS = 15.0, 83.0, 260.0
L = 200.0


def run(phi, link_twice, second_order, scale=1.0):
    nx, ny = phi.shape
    interp = RegularGridInterpolator(
        (np.arange(nx), np.arange(ny)), phi * scale / GAMMA, bounds_error=False, fill_value=0.0
    )

    def U(x, y):
        return float(interp((x, y)))

    def omega(kx, ky, u):
        P0 = 1 - u + u * u / 2 if second_order else 1 - u
        Pa = 1 - 2 * u if link_twice else P0
        c2 = 2 - (2.0 / 3.0) * Pa * Pa * ((1 - np.cos(kx)) + (1 - np.cos(ky)))
        return np.arccos(c2 / 2)

    def rhs(t, s):
        x, y, kx, ky = s
        h = 1e-4
        u = U(x, y)
        dwdkx = (omega(kx + h, ky, u) - omega(kx - h, ky, u)) / (2 * h)
        dwdky = (omega(kx, ky + h, u) - omega(kx, ky - h, u)) / (2 * h)
        d = 0.05
        dwdx = (omega(kx, ky, U(x + d, y)) - omega(kx, ky, U(x - d, y))) / (2 * d)
        dwdy = (omega(kx, ky, U(x, y + d)) - omega(kx, ky, U(x, y - d))) / (2 * d)
        return [dwdkx, dwdky, -dwdx, -dwdy]

    def hit(t, s):
        return s[0] - XS

    hit.terminal = True
    sol = solve_ivp(rhs, (0, 4000), [X0, Y0, K0, 0.0], events=hit, rtol=1e-10, atol=1e-12, max_step=0.5)
    y_end = sol.y_events[0][0][1]
    return y_end - Y0


for Es in (100000, 40000):
    phi = plane_rest(Es)
    Ub = phi[60, 83] / GAMMA
    row = 4 * Ub * L
    print(f"E_s {Es}: c(60, 83) = {phi[60, 83]:.1f}, U_b = {Ub:.5f}, the row 4 U_b L = {row:.2f} Links")
    for twice, second, name in (
        (False, False, "the Link once, the clock first order (main today)"),
        (True, False, "the Link twice, the clock first order"),
        (True, True, "the Link twice, the clock second order (the law)"),
    ):
        s = run(phi, twice, second)
        print(f"   {name:52}: shift {s:+.2f} Links = {s / row:+.3f} x the row")
# the band's factor at the small-k limit for the same field, as a check of the wavelength's part
phi = plane_rest(100000)
Ub = phi[60, 83] / GAMMA
K0 = 0.05
s = run(phi, True, True)
print(
    f"the same field at k = 0.05 (the isotropic limit): shift {s:+.2f} = {s / (4 * Ub * L):+.3f} x the row"
)
