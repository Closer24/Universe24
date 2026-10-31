"""David's probe for the owner's question of 01:3x UTC: does the metric's whole block follow from the tensor act?

usage: python3 -I p16_metric_channels.py <worktree>/src
The Spokes are T1. A metric is a symmetric tensor of two Spokes, so its kinds are the channels of T1 x T1 that are
symmetric in their two inputs. This reads them from the head's own tables C (main.made, stage 6), exactly:
  (1) for each channel T1 x T1 -> X, whether C[x, a, b] is symmetric or antisymmetric in (a, b);
  (2) the symmetric channels' dimensions, against the six of a symmetric tensor of three axes;
  (3) the two polarizations of a wave along an axis, h_xx - h_yy and h_xy: which kind each lies in.
"""
import sys

sys.path.insert(0, sys.argv[1])
import numpy as np  # noqa: E402

from tensor24 import main  # noqa: E402

shape = (3, 3, 3)
held, tables = main.made(shape)
names = [f.upper() for f in held._fields]
t1 = names.index("T1")
symmetric_dims = 0
for x, name in enumerate(names):
    c = np.asarray(tables[(t1, t1, x)])
    if not c.any():
        print(f"T1 x T1 -> {name}: no channel")
        continue
    swapped = np.swapaxes(c, 1, 2)
    kind = "symmetric" if np.array_equal(c, swapped) else "antisymmetric" if np.array_equal(c, -swapped) else "neither"
    print(f"T1 x T1 -> {name}: {kind} in its two Spokes ({c.shape[0]} components)")
    symmetric_dims += c.shape[0] if kind == "symmetric" else 0
axes = len(shape)
slots = [(a, b) for a in range(axes) for b in range(a, axes)]  # a symmetric tensor's slots, one per pair a <= b
print(f"the symmetric channels hold {symmetric_dims} components; a symmetric tensor of {axes} axes holds {len(slots)}")

# a wave along z: h_xx - h_yy and h_xy, as symmetric tensors of two Spokes, read through each channel
plus = np.zeros((3, 3), dtype=int)
plus[0, 0], plus[1, 1] = 1, -1
cross = np.zeros((3, 3), dtype=int)
cross[0, 1] = cross[1, 0] = 1
for label, h in (("h_xx - h_yy", plus), ("h_xy", cross)):
    lands = [names[x] for x in range(len(names)) if np.asarray(tables[(t1, t1, x)]).any()
             and np.einsum("xab,ab->x", np.asarray(tables[(t1, t1, x)]), h).any()]
    print(f"a wave along z, {label}: lands in {lands}")
