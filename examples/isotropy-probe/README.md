# Isotropy probe: a known number the model does not give

A point source in nature radiates the same intensity in every direction at
the same distance; the expected ratio between any two directions is 1. This
probe asks what each of the repository's two spreading rules gives instead,
on recorded runs of the canonical runner, and what it costs to close the gap.
No engine law is added or changed. The analytic references are computed
independently of the update code.

```sh
PYTHONPATH=src python examples/isotropy-probe/run_experiments.py --output artifacts/isotropy-probe
```

`--headings 256 1024` restricts the ray sweeps. `tests/test_isotropy_probe.py`
checks the path-count identity, the derived inputs, the outward shell and one
small ray sweep in the fast gate.

## Outward field: exact, and far from isotropic

Source: [moving_source.json](../moving_source.json) with the carrier held and
the emission raised to `8 x 3^9 = 157,464` units per tick, so that octant
splitting stays exact through the Manhattan shell `R = 9`. The stock at an
offset is predicted by the multinomial path count of the
[inverse-square derivation](../inverse-square/EMERGENCE_VALIDATION.md).

Recorded at tick 9 on the shell `R = 9` (326 Nodes): mean stock 483.02, equal
to `157,464 / (4 x 81 + 2)`; every sampled point equals its path count.

| Offset | Euclidean r | Measured | Path count | Isotropic 1/r^2, normalized at (3, 3, 3) | Measured / isotropic |
| --- | --- | --- | --- | --- | --- |
| (9, 0, 0) | 9.00 | 4 | 4 | 560 | 0.007 |
| (8, 1, 0) | 8.06 | 18 | 18 | 698 | 0.026 |
| (7, 2, 0) | 7.28 | 72 | 72 | 856 | 0.084 |
| (6, 3, 0) | 6.71 | 168 | 168 | 1008 | 0.167 |
| (5, 4, 0) | 6.40 | 252 | 252 | 1106 | 0.228 |
| (7, 1, 1) | 7.14 | 72 | 72 | 889 | 0.081 |
| (5, 2, 2) | 5.74 | 756 | 756 | 1375 | 0.550 |
| (4, 4, 1) | 5.74 | 630 | 630 | 1375 | 0.458 |
| (3, 3, 3) | 5.20 | 1680 | 1680 | 1680 | 1.000 |

At the same Euclidean distance of about 5, the axis Node (5, 0, 0) holds 324
and the body diagonal (3, 3, 3) holds 1680: a ratio of 5.2 where nature gives
1. Along an axis the stock falls as `1 / 3^R`, exponentially, because only one
hop ordering reaches it; the inverse square holds for the shell mean only.
This is a property of any splitting into cardinal neighbors, not of the
weights: the multinomial concentrates near the octant diagonal. The rule is
an exact bookkeeping of dilution, and it is falsified as a pointwise field law
by the measured isotropy of real radiation.

## Straight rays: isotropic on average, with counting spread

Source: [isotropic_rays.json](../isotropic_rays.json) with the source held,
`N` golden-spiral headings at scale 24, 64 rays per tick of 16 units each, and
a run of 12 warm-up ticks plus one full sweep of `N / 64` ticks. Every Node
within half a unit of Euclidean radius 8 (762 Nodes) sums its field over the
sweep; the sum over 16 is the number of rays that crossed it.

| Headings | Sweep ticks | Rays per Node, mean | Solid-angle estimate | Relative spread between Nodes | Counting spread for that mean | Nodes never reached | Axis mean | Near-diagonal mean | Host seconds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 256 | 4 | 0.45 | 0.32 | 1.11 | 1.49 | 421 of 762 | 0.33 | 0.46 | 2.6 |
| 1024 | 16 | 1.92 | 1.27 | 0.37 | 0.72 | 3 | 1.50 | 2.23 | 10.9 |
| 4096 | 64 | 10.13 | 5.09 | 0.20 | 0.31 | 0 | 9.50 | 11.25 | 257.9 |
| 16384 | 256 | run in progress at the time of this commit; the row is filled by the follow-up commit |  |  |  |  |  |  |  |

Each fourfold increase in headings halves the spread between Nodes: the
spread follows the square root of the rays per Node, as counting does, and
sits below the Poisson value because the golden spiral is more regular than
random directions. The mean per Node is about twice the solid-angle estimate
because a ray crosses about two Nodes of a shell one unit thick. A residual
directional bias remains: near-diagonal Nodes see about one fifth more rays
than axis Nodes at 4096 headings, the integer-heading and digital-line effect
also seen in the [gravity probe](../gravity-probe/README.md). Host time grows
faster than the number of rays alive.

## What this establishes

- A known number, the directional ratio 1, and the model's numbers in its
  place: 5.2 (and 140 at r = 9 on the axis) for the outward rule; 1.2 with a
  counting spread of 0.2 at 4096 headings for the ray rule.
- The outward rule cannot be repaired by weights; it is the right tool for
  conserved dilution and accounting, not for a field read at a point.
- The ray rule approaches isotropy at a cost: the spread at radius `r` and
  precision `e` needs of order `r^2 / e^2` headings per sweep, and the host
  time grows with the rays alive. Reaching one percent at radius 8 would need
  of order a million headings per sweep.
- Nothing here is a new prediction about nature; it is a measured limit of
  the model, with the number that a laboratory would use to reject or keep
  each rule.
