"""Probe 2: the click count of a moving mode, the momentum density's sign, the bang's light pattern."""
import cmath
import math

# (a) A plane wave of the vacuum leapfrog a+ + a- = 2 c0 (1/6) sum_j a_j, cos w(k) = c0 (cos kx + cos ky + cos kz)/3.
# The conserved form (hold 0 at the vacuum): E = w (|n|^2 + |b|^2) - Re(conj(n) sum_j R b_j), R = w c0 / 3.
# The sweep (the charge) Im(conj(b) n). The plan's quantum: w_c fixed per train (3 key s, s = rim sin w0).
def mode(c0, k):
    cw = c0 * sum(math.cos(x) for x in k) / 3
    w = math.acos(cw)
    return w

for name, c0 in [("electron", 0.999999855991), ("neutron", 0.162120510851), ("light", 1.0)]:
    w0 = math.acos(c0)
    for kx in [0.0, 0.05, 0.3, 1.0, math.pi / 2]:
        k = (kx, 0.0, 0.0)
        w = mode(c0, k)
        if w == 0:
            continue
        A = 1.0
        n = A  # now at a site (phase 0)
        b = A * cmath.exp(1j * w)  # before: z(t-1) = z(t) e^{+iw} for z ~ e^{-iwt}
        # neighbours' before: b_j = b e^{i k.e_j}
        nb_sum = sum(b * cmath.exp(1j * s * kk) for kk in k for s in (1, -1))
        E = (abs(n) ** 2 + abs(b) ** 2) - (c0 / 3) * (n.conjugate() * nb_sum).real
        sweep = (b.conjugate() * n).imag
        # quanta by the charge: |sweep| / (sweep of one rest quantum at the same amplitude scale)
        # the plan's q = E / w_c with w_c chosen so a rest quantum gives q = sweep units: q/N = (E/|sweep|)/(E0/|sweep0|)
        ratio_E_per_charge = E / abs(sweep)
        s_ref = math.sin(w0) if w0 > 0 else 1.0  # light: the head's rim (sin = 1)
        print(f"{name:8s} kx={kx:.3f} w(k)={w:.5f} E/|sweep|={ratio_E_per_charge:.5f} = 2 sin w = {2*math.sin(w):.5f};"
              f" clicks per quantum q/N = sin w / s_ref = {math.sin(w)/s_ref:.4f}")

# (b) momentum density sign: z = exp(i(kx - wt)) moves toward +x for k, w > 0.
k, w = 0.3, 0.2
def z(x, t):
    return cmath.exp(1j * (k * x - w * t))
d0 = z(0, 0) - z(0, -1)
da = (z(1, 0) - z(-1, 0)) / 2
print("\nRe(conj(d0 z) da z) for a wave moving to +x:", (d0.conjugate() * da).real, "(negative: the plan's P_a has the wrong sign)")
print("Im(conj(z) (z_up - z_down)) (the lead):", (z(0, 0).conjugate() * (z(1, 0) - z(-1, 0))).imag,
      " Im(conj(z-) z) (the sweep):", (z(0, -1).conjugate() * z(0, 0)).imag)

# (c) the bang's light pattern: p(x,y,z) = (p1[4 (x mod 4) + (y mod 4)] + cz z) mod 4, hand = i^p, quarter turn per tick.
p1 = [0, 0, 1, 1, 2, 2, 3, 3, 1, 1, 0, 0, 3, 3, 2, 2]
cz = 1
L = 4
def p(x, y, zz):
    return (p1[4 * (x % 4) + (y % 4)] + cz * zz) % 4
def hand(x, y, zz, t):
    return 1j ** ((p(x, y, zz) + t) % 4)  # z(t+1) = i z(t)
bad = 0
for x in range(L):
    for y in range(L):
        for zz in range(L):
            s = sum(hand(x + dx, y + dy, zz + dz, 0) for dx, dy, dz in
                    [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)])
            # light: a+ + a- = (1/3) sum_j a_j; a quarter turn needs a+ + a- = i a + (-i) a = 0
            if abs(s) > 1e-12:
                bad += 1
print("\nbang pattern: sites where the six neighbours do not sum to 0:", bad, "of", L ** 3)
# momentum density (velocity = now - before) and stress on each axis, per the plan's formulas
Pd = [0.0, 0.0, 0.0]
Td = [0.0, 0.0, 0.0]
Toff = [0.0, 0.0, 0.0]
for x in range(L):
    for y in range(L):
        for zz in range(L):
            now = hand(x, y, zz, 0)
            vel = now - hand(x, y, zz, -1)
            grads = []
            for a, e in enumerate([(1, 0, 0), (0, 1, 0), (0, 0, 1)]):
                up = hand(x + e[0], y + e[1], zz + e[2], 0)
                dn = hand(x - e[0], y - e[1], zz - e[2], 0)
                grads.append((up - dn) / 2)
            for a in range(3):
                Pd[a] += (vel.conjugate() * grads[a]).real
                Td[a] += abs(grads[a]) ** 2
            Toff[0] += (grads[0].conjugate() * grads[1]).real
            Toff[1] += (grads[1].conjugate() * grads[2]).real
            Toff[2] += (grads[2].conjugate() * grads[0]).real
print("total momentum per axis (plan's Re(conj(d0 z) da z)):", [round(v, 6) for v in Pd])
print("stress diagonal totals T_xx, T_yy, T_zz:", [round(v, 6) for v in Td], " off-diagonal xy, yz, zx:", [round(v, 6) for v in Toff])
