"""The great clock's source by the force form against the books' stress tensor, on one gear with a cubic coupling.

phi'' = F = -D phi - g phi^2, V = D phi^2 / 2 + g phi^3 / 3 (the spring and the coupling's energy V_c = g phi^3 / 3).
The books' rho + 3p for one gear is 2 phi'^2 - 2V (exact); the force form is J = -2 phi F - D phi^2. Averaged over one
beat, the two differ by 2 <V_c>: the force form weighs a coupling's energy wrongly, so binding would gravitate wrongly.
Floats, by name: a leapfrog at dt = 1e-5 over one beat.

Usage: python3 -I virial.py
"""

D, g = 1.0, 0.3
phi, v, dt = 0.8, 0.0, 1e-5
n, s_exact, s_force, s_vc, crossings = 0, 0.0, 0.0, 0.0, 0
while crossings < 2:
    f = -D * phi - g * phi * phi
    vc = g * phi ** 3 / 3
    s_exact += 2 * v * v - 2 * (D * phi * phi / 2 + vc)
    s_force += -2 * phi * f - D * phi * phi
    s_vc += vc
    n += 1
    v_new = v + f * dt
    phi += v_new * dt
    if (v_new > 0) != (v > 0) and n > 10:
        crossings += 1
    v = v_new
print(f"over one beat: books' rho + 3p {s_exact / n:+.6f}; force form {s_force / n:+.6f}; "
      f"difference {s_force / n - s_exact / n:+.6f}; 2 <V_c> {2 * s_vc / n:+.6f}")
