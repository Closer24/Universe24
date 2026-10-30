# The 7b act at rest on every row: W (a+ - 2a + b) = s F, F = grip SUM_spokes (a_nb - a) - D a, s grip / W = 1/6.
# Dispersion: sin^2(w/2) = (1/6) SUM_i sin^2(k_i/2) + s D / (4 W). Group speed |grad_k w| over the whole zone.
import numpy as np
cone = 1 / 6
n = 121
k = np.linspace(-np.pi, np.pi, n)
kx, ky, kz = np.meshgrid(k, k, k, indexing="ij")
def speeds(mass):
    s2 = cone * (np.sin(kx / 2) ** 2 + np.sin(ky / 2) ** 2 + np.sin(kz / 2) ** 2) + mass
    w = 2 * np.arcsin(np.sqrt(s2))
    denom = np.sin(w / 2) * np.cos(w / 2)
    g = [cone * np.sin(q / 2) * np.cos(q / 2) / np.where(denom == 0, np.inf, denom) for q in (kx, ky, kz)]
    return np.sqrt(g[0] ** 2 + g[1] ** 2 + g[2] ** 2), w
for mass in (0.0, 0.001, 0.05):
    v, w = speeds(mass)
    print(f"mass term {mass}: the fastest group speed {v.max():.6f} against light's 1/sqrt 6 = {np.sqrt(cone):.6f}; stable: {np.isfinite(w).all()}")
# the long-wave speed along an axis and along the body diagonal (isotropy)
for name, d in (("axis", (1, 0, 0)), ("diagonal", (1, 1, 1))):
    d = np.array(d) / np.linalg.norm(d)
    for kk in (0.01, 0.5, 1.0):
        q = kk * d
        w = 2 * np.arcsin(np.sqrt(cone * np.sum(np.sin(q / 2) ** 2)))
        print(f"  {name}, k = {kk}: phase speed {w / kk:.6f}")
