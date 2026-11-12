# Conserved covectors, geodesics and what a moving clock reads

This audit uses the **same eight-channel Bianchi-I tensor and complete native
states** as `common.py`. It adds no retained particle, clock, detector or
worldline. Its exact identities and passive diagnostics describe the
test-particle geodesics of that source's interpreted metric. They are not a
claim that a material packet travels across the board.

The useful simplification is to retain a conserved **covector**, rather than
mistaking a coordinate velocity for a conserved vector. Homogeneity supplies
the three Killing symmetries. The metric converts their three conserved
momenta into the velocity and proper-time rate measured by an observer.

## Exact metric and geodesic identities

The shared sourced background has

\[
ds^2=-dt^2+\sum_i a_i(t)^2(dx^i)^2,\qquad
a_i=V^{1/3}e^{S_i I},\quad \dot I=1/V,
\]

\[
\dot V=U,\quad\dot U=3D/2,\quad
\dot P=\dot D=\dot S_i=0,\quad\sum_i S_i=0,
\qquad H_i=\dot a_i/a_i=U/(3V)+S_i/V.
\]

Here `I` is anchored by the retained reference velocity; it is not looked up
from the Engine tick. With physical particle mass \(m\ge0\), the conserved
spatial covector \(p_i\) determines

\[
E=\sqrt{m^2+\sum_i p_i^2/a_i^2},\qquad
P^\mu=(E,p_1/a_1^2,p_2/a_2^2,p_3/a_3^2).
\]

The symbolic audit independently contracts all four affine geodesic
equations. The only nonzero Christoffels needed are
\(\Gamma^0_{ii}=a_i^2H_i\) and
\(\Gamma^i_{0i}=\Gamma^i_{i0}=H_i\). Since

\[
\dot E=-\frac{1}{E}\sum_i H_i p_i^2/a_i^2,
\qquad \frac{d}{dt}(p_i/a_i^2)=-2H_i p_i/a_i^2,
\]

each component of \(P^\nu\partial_\nu P^\mu+
\Gamma^\mu_{\alpha\beta}P^\alpha P^\beta\) vanishes.
The same calculation verifies

\[
g_{\mu\nu}P^\mu P^\nu=-m^2,\qquad
\frac{dx^i}{dt}=\frac{p_i}{a_i^2 E},\qquad
\boxed{\frac{d\tau_{\rm probe}}{dt}=\frac{m}{E}}.
\]

For a nonzero spatial covector and positive mass the proper rate is strictly
between zero and one. At rest it is one. Null curves have zero proper interval;
this does not supply a photon clock. The flat control \(m=4,p=(3,0,0)\) gives
\(E=5\), coordinate speed \(3/5\) and proper rate \(4/5\).

Under a constant diagonal coordinate change \(x'^i=\lambda_i x^i\),
\(a'_i=a_i/\lambda_i\), \(p'_i=p_i/\lambda_i\), and
\(P'^i=\lambda_iP^i\). The energy and mass shell are unchanged. The audit
verifies this dual transformation explicitly. Holding contravariant momentum
constant instead produces a spatial geodesic residual
\(2EH_iP^i\); a simple control gives the exact nonzero value 30.

For null rays the comoving measured energy is
\(E_\gamma=\sqrt{\sum_i p_i^2/a_i^2}\). Therefore
\(1+z=E_\gamma(t_{\rm emission})/E_\gamma(t_{\rm reception})\)
depends on direction. Spatial covector conservation does **not** imply energy
conservation in this time-dependent metric.

## Actual native states and passive quadrature

The default source seed is
\(D=1,P=2,S=(1,-1,0),V_0=7/3,U_0=4\). Its initial directional expansion
rates are \((1,1/7,4/7)\), so the anisotropy is physical and nonzero. All three
resolutions use tensor
`a51595cb6b4facd289fc40334527dc9ad4126c4f3244f70f8d5fcba53585231b`;
the default complete seed is
`d1fcbb9266b7c9cb06ce10a33e900068ade4f83a01f7507c3f894efff103e1cc`.

Only the unchanged Engine advances the background. Every step is compared
with a separate scalar Rule3 oracle and immediately inverted, and the complete
state is rewound. Constraint and shear charges are exact in every sampled
state. At background proper time \(T=1/8\), the exact source endpoint is
\(V=2185/768,U=67/16\) at every resolution.

For the diagnostic probe \(m=4,p=(3,0,0)\), composite trapezoids use the
metric values read from those actual states. A separately written exact
continuum solution supplies only the passive high-precision reference.
No quadrature result is written back to Engine.

| N | Engine steps | Proper-time quadrature error | x1 quadrature error | Peak retained bits |
|---:|---:|---:|---:|---:|
| 24 | 3 | 8.45436e-6 | 2.80702e-5 | 13 |
| 48 | 6 | 2.11437e-6 | 7.02078e-6 | 15 |
| 96 | 12 | 5.28642e-7 | 1.75540e-6 | 17 |

Observed orders are 1.9995/1.9999 for proper time and 1.9993/1.9998 for
position. This is **diagnostic quadrature convergence**, not error in the
exact native source solution or proof of retained probe transport. Reference
proper time is approximately `0.1102867902487182`, strictly below `0.125`;
the instantaneous proper rate increases from `0.8704721431` to `0.8929038173`.
The independent metric formula agrees below `2e-70`, and repeating reference
quadrature at 90 rather than 70 decimal digits changes the result below `1e-60`.
These precision comparisons are numerical checks, not interval certificates.

There is also an analytic error bound. On this declared interval,
\(V\ge7/3\), \(4\le U\le67/16\), \(I\ge0\), hence for axis one
\(a_1>1\), \(0<q=9/a_1^2\le9\), \(0<H_1<2\), and
\(|\dot H_1|<4\). Differentiating the proper rate and coordinate velocity
gives the conservative bounds

\[
\sup| (4/\sqrt{16+q})''|\le675/64,\qquad
\sup| (q/(3\sqrt{16+q}))''|\le8361/256.
\]

The composite-trapezoid theorem then bounds each error by
\(T h^2\sup|f''|/12\). Every reported error lies below its corresponding
explicit rational bound in the evidence. The metric is smooth on the entire
interval, so the theorem's regularity hypothesis is satisfied.

For axis-aligned null rays the endpoint redshifts are approximately
`(0.1213875898, 0.01777835794, 0.06832767434)` in axes `(1,2,3)`.
All three resolutions give the same values because the sourced endpoints are
exact. Replacing the anisotropic metric by one common scale factor loses this
direction-dependent prediction.

## A narrow encoding obstruction and remaining obligation

An exact generic worldline extension cannot simply give position and moving
proper time fixed rational scales. Already in flat space, the rational data
\(m=1,p=(1,0,0)\) require velocity and proper-time rate \(1/\sqrt2\).
For any positive rational time step the exact increments are irrational.
A rational decoder of integer registers can only produce rational values.
The executable witness checks that \(2z^2-1\) is irreducible over \(\mathbb Q\).

This excludes **only** the direct exact rational-coordinate encoding. It is
not a no-go theorem for approximate, implicit, algebraic or nonlinear
encodings. Retaining three conserved covector constants is cheap, but does
not itself retain a moving position, accumulated proper time, detector or
reaction on the source. No such extension is claimed here. A subsequent
implementation must count those channels and prove their joint Engine map;
the present passive geodesic formulas cannot be substituted for that work.

## Sources and reproduction

- Fleury, Pitrou and Uzan, [Light propagation in a homogeneous and anisotropic
  universe](https://arxiv.org/pdf/1410.8473), sections II and IV, especially
  equations (4.1)–(4.7): homogeneous covector constants, null energy and
  direction-dependent redshift, and the timelike extension. The metric/source
  specialization and native-state checks above are derived in this project.
- Hughes, [MIT 8.962 Lecture 9](https://web.mit.edu/sahughes/www/8.962/lec09.pdf),
  sections 9.3–9.4, equations (9.24)–(9.31): covariant geodesic momentum and
  Killing-vector conservation. The distinction between covector, raised vector
  and measured energy is used explicitly in the negative controls.

```sh
python -m validation.conservation_closure.covector_geodesics
```

Evidence: `runs/conservation_closure/covector_geodesics.json`. The evidence
records exact tensor/complete-seed identities, all three resolutions, source
hashes, the analytic quadrature bounds and the unimplemented transport gate.
