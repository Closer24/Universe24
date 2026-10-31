"""Where the swept area's drift goes: into the clock's own fine teeth, and back out of them on the run back.

The two-part hand of c1 at one Node-clock under the spring D = W div 64, stepped forward 20,000 rounds by the head's
gear and then run back 20,000 rounds by the head's mirror (the slots swapped, each fine tooth flipped to W - 1 - r,
the gear stepped, mirrored again). Omega drifts on the way out and returns bit for bit on the way back, with the whole
state: the step is a bijection on (a, b, r), so no swept area leaves the clock; what Omega misses each round,
Delta q_re r_im - Delta q_im r_re, is written in the kept teeth.

Usage: python3 -I c2_held_by_the_clock.py <src of tensor24-review at 68c7245ef>   (the example files are read from
<src>/../examples/tensor24)
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
from tensor24 import main  # noqa: E402
from tensor24.runner import load as L  # noqa: E402
from tensor24.runner.files import sites_of  # noqa: E402
from tensor24.engine import step  # noqa: E402

ex = Path(sys.argv[1]).parent.joinpath("examples", "tensor24")
universe = json.loads(ex.joinpath("universe.json").read_text())
shape = json.loads(ex.joinpath("piece.json").read_text())["shape"]
loaded, _ = L.load(universe, {"version": 1, "ticks": 1, "gears": []}, sites_of(shape), *main.made(L.star(len(shape))))
W = int(main.layout(universe, shape, loaded).gearing.rest[0][0])  # the head's teeth, read through the loader
A, K = 10**6, 8
D = W // (K * K)


def omega(re, im):
    (ar, br, rr), (ai, bi, ri) = re, im
    return ar * (W * (ai - bi) + ri) - ai * (W * (ar - br) + rr)


def forward(part):
    return step.gear(*part, W, -D * part[0])


def back(part):
    a, b, r = part
    ma, mb, mr = step.gear(b, a, W - 1 - r, W, -D * b)  # the tick on the mirrored state
    return mb, ma, W - 1 - mr  # mirrored again


re0, im0 = (A, A, 0), (0, -(A // K), 0)
re, im = re0, im0
o0 = omega(re, im)
drift, drift_sum = 0, 0
for _ in range(20000):
    nre, nim = forward(re), forward(im)
    dq_re, dq_im = nre[0] - re[0], nim[0] - im[0]
    drift_sum += dq_re * nim[2] - dq_im * nre[2]
    re, im = nre, nim
    drift = max(drift, abs(omega(re, im) - o0))
out = omega(re, im)
print(f"forward 20,000 rounds: Omega from {o0} to {out}, largest drift {drift}")
print(f"the sum of Delta q_re r_im - Delta q_im r_re over the rounds equals Omega's change: {drift_sum == out - o0}")
for _ in range(20000):
    re, im = back(re), back(im)
print(f"run back 20,000 rounds: the whole state returns bit for bit: {(re, im) == (re0, im0)}; Omega returns: {omega(re, im) == o0}")
