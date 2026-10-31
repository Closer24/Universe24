"""Term 11's quantum per mode, on the head's own gear step, whole numbers alone.

A two-part hand (re, im) at one Node-clock under a spring D: each part steps by step.gear. With p = W (a - b) + r the
part's stride and kept fine tooth, the gear is p+ = p + push and a+ = a + (p+ div W) exactly. The hand's swept area is
Omega = re p_im - im p_re (= W (b_re a_im - a_re b_im) + a_re r_im - a_im r_re in the stored state): the symplectic
product, the adiabatic invariant, the wind over the frequency.
(a) at equal energy, Omega grows as 1 / omega, so counting the click on Omega gives E = n h nu per mode; the wind does not;
(b) Omega's drift under the carries over 20,000 rounds;
(c) the opposite sense gives Omega of the other sign, and carry(Omega, key, r) a negative quotient with no if.

Usage: python3 -I c1_quantum_per_mode.py <src of tensor24-review at 68c7245ef>   (the example files are read from
<src>/../examples/tensor24)
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
from tensor24 import main  # noqa: E402
from tensor24.runner import load as L  # noqa: E402
from tensor24.runner.files import sites_of  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import step  # noqa: E402

ex = Path(sys.argv[1]).parent.joinpath("examples", "tensor24")
universe = json.loads(ex.joinpath("universe.json").read_text())
shape = json.loads(ex.joinpath("piece.json").read_text())["shape"]
loaded, _ = L.load(universe, {"version": 1, "ticks": 1, "gears": []}, sites_of(shape), *main.made(L.star(len(shape))))
W = int(main.layout(universe, shape, loaded).gearing.rest[0][0])  # the head's teeth, read through the loader
A = 10**6


def omega(re, im):
    (ar, br, rr), (ai, bi, ri) = re, im
    return ar * (W * (ai - bi) + ri) - ai * (W * (ar - br) + rr)


def energy(part, d):
    a, b, r = part
    p = W * (a - b) + r
    return p * p + d * W * a * a  # W times (p^2 / W + D a^2): the wind of the rational step, scaled whole


rows = []
for k in (8, 16, 32, 64):
    d = W // (k * k)
    re, im = (A, A, 0), (0, -(A // k), 0)  # one part at rest at A, the other moving by A div k: equal energies
    o0, e0 = omega(re, im), energy(re, d) + energy(im, d)
    drift = 0
    for _ in range(20000):
        re = step.gear(*re, W, -d * re[0])
        im = step.gear(*im, W, -d * im[0])
        drift = max(drift, abs(omega(re, im) - o0))
    rows.append((k, o0, e0, drift))
    print(f"(a, b) k = {k:2}: D = W div {k * k}; Omega = {o0}; wind = {e0}; Omega's largest drift in 20,000 rounds = {drift}")
k0, o00, e00, _ = rows[0]
print("(a) at the same wind, Omega over the k = 8 one:",
      [f"k {k}: {o * e00 // (o00 * e) if e else 0} (k / 8 = {k // 8})" for k, o, e, _ in rows])
key = 36000
for sense in (1, -1):
    re, im = (A, A, 0), (0, -sense * (A // 8), 0)
    q, r = carry(omega(re, im), key * W, 0)
    print(f"(c) sense {sense:+d}: Omega {omega(re, im)}; carry by the quantum key W gives q = {q}, kept {r} (0 <= kept < key W: {0 <= r < key * W})")
