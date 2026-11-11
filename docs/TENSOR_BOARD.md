# Full tensor readout on the prepared board

`experiments/geometry/tensor_board.py` is a passive observer for the recorded
vacuum and Einstein-Maxwell wave experiments. It does not add a metric update
or claim that general Einstein dynamics now follows from ONE.

It reads the complete n=2 histories (L=6) for a mixed vacuum wave, linear and
circular electromagnetic waves, and flat space. At every board site and tick
it supplies the metric, its inverse, all 256 covariant Riemann components,
Ricci, the curvature scalar, Einstein, independently computed Maxwell stress,
the electromagnetic field tensor, Weyl and the Einstein-minus-stress residual.
All components use exact rational arithmetic; rounded display values do not
replace the exact values.

## Coordinate and field conventions

The coordinate order is (u,v,x,y), signature (-,+,+,+), kappa=1 and Lambda=0.
For computational site (i,j,k), the declared chart is

```
x = 3*(2*i-(L-1))/L,
y = 3*(2*j-(L-1))/L,
u = (tick+2*k)/n.
```

These are chosen local-chart samples. A computational board slice is not
established as a physical simultaneous spacetime slice. The chart is not
periodically glued in x or y and is not calibrated by clock measurements.

The vacuum profile decodes p.X/P and q.X/P as A,B. The electromagnetic profile
decodes those registers as E1,E2, with rho=E1^2+E2^2 and C=-rho/2. The combined
pointwise formula supported by the observer is

```
H = (A+C)*x^2 + 2*B*x*y + (-A+C)*y^2,
ds^2 = -2du dv + dx^2 + dy^2 + H du^2.
```

The underlying update tensor, the metric g, the Einstein tensor G and the
stress tensor T are different objects. G and T are computed separately.
Setting C=0 while retaining E1=1/8 gives the deliberately incorrect-metric
control `Guu-Tuu=-1/64`, which the observer detects.

## All components and their matrix representation

Rank-two tensors appear as 4x4 arrays. Riemann and Weyl appear as 6x6 arrays
indexed by the antisymmetric pairs (uv,ux,uy,vx,vy,xy). This is a complete
representation: reversing either pair changes the sign, and a repeated index
within either pair gives zero. Tests reconstruct all 256 entries. It is not
a claim that Riemann is a rank-two tensor.

The curvature formula is checked independently against differentiation of the
metric, with arbitrary functions A(u), B(u), C(u). Ricci is contracted from
Riemann using the inverse metric, and stress is computed from F and g. Weyl
is obtained by subtracting the Ricci traces. The pure vacuum example has
nonzero Weyl and zero Ricci; pure electromagnetic plane waves have zero Weyl
and nonzero Ricci. Both have R=0, so a zero scalar curvature does not certify
flatness.

The four stored histories supply 11,232 exact site/time checks (4*13*6^3).
Every one has all 16 Einstein-minus-stress components zero. This verifies
the selected decoder on those histories, not a general constrained evolution
theorem for arbitrary board states.

## Reproduce

```sh
python experiments/geometry/pp_wave_solution.py --refinements 2
python experiments/geometry/electrovac_solution.py --refinements 2
python experiments/geometry/tensor_board.py
python -m unittest universe24.tests.test_tensor_board universe24.tests.test_electrovac_solution universe24.tests.test_pp_wave_solution -v
```

The observer writes `runs/geometry/tensor_board/board.json` and `audit.json`.
The compact board data stores each phase column once because the curvature
and electromagnetic field are transversely homogeneous. The metric's x,y
dependence is reconstructed from the exact declared H formula. The export
records source trace hashes and the chart convention.
