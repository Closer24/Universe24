"""The twin hands under the cube's turns, in integers: Z[zeta8] as four coefficients (a + b z + c z^2 + d z^3, z^4 = -1)."""
import itertools
import numpy as np
def mul(x, y):  # product in Z[zeta8], coefficients (a, b, c, d)
    out = [0] * 8
    for i, a in enumerate(x):
        for j, b in enumerate(y):
            out[i + j] += a * b
    return tuple(out[k] - out[k + 4] for k in range(4))
zeta, one = (0, 1, 0, 0), (1, 0, 0, 0)
inv = (0, 0, 0, -1)  # zeta^-1 = -zeta^3
assert mul(zeta, inv) == one
print("the multiplication by zeta is a shift with one sign:", mul(zeta, (5, 7, 11, 13)), "from (5, 7, 11, 13)")
# the spinor quarter turn about z: diag(zeta^-1, zeta); four of them give -1, eight give +1
p = [one, one]
for k in range(1, 9):
    p = [mul(inv, p[0]), mul(zeta, p[1])]
    if k in (4, 8):
        print(f"{k} quarter turns about z: diag =", p)
# the quarter turn about x: (1 - i sigma_x) / sqrt 2 has the entry 1 / sqrt 2; is 1/sqrt 2 in Z[zeta8]?
# sqrt 2 = zeta - zeta^3; an element u with u * sqrt2 = 1 would make sqrt 2 a unit: its norm (the product of its four conjugates) is 4, not 1
s2 = (0, 1, 0, -1)
def as_complex(x):
    w = np.exp(1j * np.pi / 4)
    return sum(c * w ** k for k, c in enumerate(x))
print("sqrt 2 as (0, 1, 0, -1):", np.round(as_complex(s2), 12))
conj = [as_complex(tuple(c * (1 if k == 0 else 0) for k, c in enumerate(s2)))]  # placeholder
norm = 1
for g in (1, 3, 5, 7):  # the Galois conjugates zeta -> zeta^g
    w = np.exp(1j * np.pi * g / 4)
    norm *= sum(c * w ** k for k, c in enumerate(s2))
print("the norm of sqrt 2 in Z[zeta8]:", np.round(norm, 9), "-> not a unit, so 1/sqrt 2 is no integer of Z[zeta8]")
# with an integer scale exponent e (the value psi / sqrt2^e) every turn of the double cover is an integer matrix over Z[i]:
turns = {
    "quarter about z": (np.array([[1 - 1j, 0], [0, 1 + 1j]]), 1),
    "quarter about x": (np.array([[1, -1j], [-1j, 1]]), 1),
    "three-fold about (1,1,1)": (np.array([[1 - 1j, -1j - 1], [-1j + 1, 1 + 1j]]), 2),
    "half about x": (np.array([[0, -1j], [-1j, 0]]), 0),
}
for name, (m, e) in turns.items():
    u = m / np.sqrt(2) ** e
    print(f"{name:26s} integer matrix over Z[i], exponent +{e}: unitary", np.allclose(u.conj().T @ u, np.eye(2)), " det", np.round(np.linalg.det(u), 9))
