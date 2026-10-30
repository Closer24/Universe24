"""David's correction of p10: which lattice coupling is general relativity's wave operator on the head's own metric.

usage: python3 -I p13_grip_on_the_head_metric.py
The head's time gear is the stretch X = Gamma (Gamma / p_0)^4 (features/stretch: the proper volume per proper tick,
d = 3), and its grip per end is R_i = 2 pinion p_i^2 Q with the mesh rate p_i = p_0^2 / Gamma (core/rule3.gearing), so
with N = p_0 / Gamma the grip per end goes as N_i^4 and the stretch as 1 / N^4. That is the metric
ds^2 = -N^2 dt^2 + A^2 dx^2 with N A = 1 (the exponential metric: Schwarzschild's to first order, PPN gamma = 1).
A massless field there obeys (A^3 / N) phi_tt = d(N A d phi), so phi_tt = N^4 phi'' (one axis shows it).
p10 compared the forms with phi_tt = N d(N d phi), the operator of a lapse on a flat space (A = 1), and read the head's
grip as N^2 per end. Here the three forms of p10, the head's read as it is (N^4 per end), are compared with both
operators at h = 2 pi / n, n from 64 to 1,024; the error of a form that is the operator falls as h^2. Then the
coordinate speed of light in a uniform N under each form, against N / A = N^2 on the head's metric. Floats, a
continuum statement read on its lattice; no engine is run.
"""
import math


def lapse(x):
    return 1 + 0.3 * math.sin(x)


def dlapse(x):
    return 0.3 * math.cos(x)


def field(x):
    return math.cos(2 * x)


def dfield(x):
    return -2 * math.sin(2 * x)


def ddfield(x):
    return -4 * math.cos(2 * x)


def on_the_head_metric(x):  # (N / A^3) (N A phi')' with A = 1 / N: N^4 phi''
    return lapse(x) ** 4 * ddfield(x)


def on_a_flat_space(x):  # N (N phi')', A = 1
    return lapse(x) * (dlapse(x) * dfield(x) + lapse(x) * ddfield(x))


FORMS = {
    "the head's, a grip per end N_i^4 (p_i^2 with the mesh rate)": lambda ni, mesh: ni**4,
    "p10's per Mesh at the clock's own rate, N_i N_ij": lambda ni, mesh: ni * mesh,
    "per Mesh at the full rate, N_ij^4": lambda ni, mesh: mesh**4,
}

for target_name, target in (("the head's metric, N A = 1", on_the_head_metric), ("a flat space, A = 1", on_a_flat_space)):
    print(f"against the operator on {target_name}:")
    for name, coefficient in FORMS.items():
        errors = []
        for n in (64, 256, 1024):
            h = 2 * math.pi / n
            worst = 0.0
            for i in range(n):
                x = i * h
                ni = lapse(x)
                value = sum(
                    coefficient(ni, (ni + lapse(y)) / 2) * (field(y) - field(x)) for y in (x + h, x - h)
                ) / h**2
                worst = max(worst, abs(value - target(x)))
            errors.append(worst)
        print(f"  {name}: largest error {errors[0]:.2e} at n = 64, {errors[1]:.2e} at 256, {errors[2]:.2e} at 1,024")

print("the coordinate speed of light in a uniform N (the long-wave limit of each form), against N^2 on the head's metric:")
for n_value in (0.9, 0.99):
    head, own_rate = n_value**2, n_value
    print(f"  N = {n_value}: the head's {head:.4f}; p10's per Mesh at the own rate {own_rate:.4f}; N^2 = {n_value**2:.4f}")
print("so in a weak well N = 1 + Phi light's coordinate speed is 1 + 2 Phi under the head's form and 1 + Phi under p10's:")
print("the bending of light by the head's form is general relativity's, and by p10's form half of it")
