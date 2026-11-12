# Independent review: what the new controls establish

Reviewer 8 of the requested eight-agent investigation. Main baseline:
`4c494c1188f70eb8a677bf59765cc6e8571c6b88`. No production law or accepted
physical model is changed by this work.

## Clock geometry

The exact connection/Riemann signs in `clock_geometry.py` are consistent with
signature `-+++`, units `c=1`, and
`R^a_bcd = partial_c Gamma^a_db - partial_d Gamma^a_cb + ...`.
The Rindler restriction `1+a*x>0` is necessary to identify the positive clock
rate with `1+a*x`; the metric is singular at the chart horizon. The independently
constructed coordinate transformation

```text
T = (x + 1/a) sinh(a t)
X = (x + 1/a) cosh(a t)
Y = y, Z = z
```

pulls back Minkowski to `diag(-(1+a*x)^2,1,1,1)` exactly. This independently
checks flatness without relying on the audit's Riemann algorithm.

For de Sitter, an independent review compares all 256 components against
`R^a_bcd = H^2 (delta^a_c g_bd - delta^a_d g_bc)`. It agrees with the reported
Ricci scalar `12 H^2` and tidal component `R^x_txt = -H^2`. Minkowski and this
metric both give unit stationary clock rate, but different curvature. This is
an exact continuum/Einstein-Lambda oracle, not a Universe24 Engine solution.

The ten-velocity reconstruction formulas are correct. An independently built
quadratic design matrix has rank 10; rest data alone have rank 1; removing any
one of the ten samples reduces the rank to 9. Twenty exact symmetric matrices
were reconstructed using an independent quadratic contraction, not the
production `rate_squared` helper. Those twenty matrices are algebraic controls;
they are not all Lorentzian and are not presented as physical clocks.

There is a decisive scope limitation: **ten samples identify ten metric
components only under the assumed quadratic clock law, in a known coordinate
chart and with calibrated velocities.** They do not establish that a material
mechanism obeys that law. The new independent negative control adds

```text
v_x (v_x^2 - epsilon^2), epsilon = 1/10
```

to the Minkowski squared clock rate. This term vanishes at every one of the ten
calibration velocities, so the reconstructed metric is still Minkowski. At
held-out velocity `(1/8,0,0)` it changes the squared rate by `9/12800`, and the
predicted metric law fails. All sampled and held-out rates remain positive.
Therefore held-out velocities and independent clock mechanisms are substantive
physical acceptance checks, not optional extra fitting points.

Reproduction:

```bash
python -m validation.einstein_node_audit.independent_review
```

The script saves exact, source-hashed evidence in
`runs/einstein-node/08_independent_review.json`. All eight review checks passed,
including the deliberate nonmetric counterexample.

## Node algebra, host workload and shared cones

The actual `node_algebra` audit was independently rerun: 2,430 retained triples,
2,380 paired arithmetic-click rows, all six remainders, staged old-a dependencies,
large signed integers and complete rewinds passed. Its native-coordinate and
bounded summed carry-defect identities are correct. Frozen parity is an
inactive retained label under the current tensor input contract. It does not
identify a particle, physical charge or gravitational degree of freedom.
Arithmetic content equality should be distinguished from provenance: separately
sealed parity-flipped bundles have distinct run/event identities, even when
their node/channel/quotient/class content agrees.

The `load_invariance` audit varies exact arithmetic backend and adds discarded
host work outside the Engine. Its scalar oracle and full-state comparisons
are independent of the vectorized execution. This tests implementation workload
invariance for the supplied one-channel fixture; it is not a theorem excluding
every possible representation-independent intrinsic-work theory. The explicit
period-three amplitude-variance control refutes monotone equalization as a
generic consequence of Rule3, without identifying that variance as energy.

The principal-cone script was read and rerun against exact external PR50 pin
`62202fdccdd9a40d5dbbec104de6f97d9587a999`. Its scalar/Maxwell blocks, symbolic
annihilator and nonorthogonal oblique speed comparison pass. The correct metric
gives speed squared 146; the deliberately wrong identity frame gives 14.
The published symbol and 45-channel controls also reran successfully. This is
evidence about frozen continuum derivative blocks extracted from encoded
equations. It neither derives those equations from generic Rule3 nor verifies
finite-step propagation of a localized packet along a geodesic.

## Acceptance conclusion

No blocking mathematical error was found in the inspected controls. The
important qualifications are operational rather than cosmetic: passive metric
queries are not independently ticking clocks; coordinate velocity is assumed
known; fixed-mass wave characteristics do not establish timelike material
motion; exact replay does not establish a gravitational constraint law. These
controls strengthen the falsification suite while leaving physical acceptance
unestablished.
