# Geometry audit: the shared kinetic metric already present

Inspected main: `4c494c1188f70eb8a677bf59765cc6e8571c6b88`.
Executed proposal: PR50 `62202fdccdd9a40d5dbbec104de6f97d9587a999`.
This report distinguishes a new independent principal-block calculation from
reruns of published audits and from unimplemented packet/clock tests.

## A concrete generic connection

The charged scalar and Maxwell equations already use the same inverse spatial
frame `B` in their derivative operator:

\[
e_a=B_a{}^i\partial_i,\qquad g^{\mu\nu}=\operatorname{diag}(-1,B^TB).
\]

This is visible in PR50's
`validation/geometry/team48/matter_equations.py` (`direction`, `divergence`,
`curl` and the scalar/Maxwell RHS) and `matter_charged.py`. The readout
`universe24/observe/frame48.py:31` uses the same metric. Nonzero determinant
is required for its spacetime interpretation. The lapse is one and the shift
is zero in this frame formulation; arbitrary clock-rate differences have not
been introduced as a separate gravitational field.

Our new script extracts the actual scalar and Maxwell principal derivative
blocks from `matter_charged.equations`. For an arbitrary real full frame `B`
and covector `n`, it verifies symbolically

\[
A_s^3-|Bn|^2A_s=0,\quad A_M^3-|Bn|^2A_M=0,
\quad\mathrm{tr}(A_s^2)=2|Bn|^2,\quad
\mathrm{tr}(A_M^2)=4|Bn|^2.
\]

The nonzero characteristic speeds therefore belong to the same metric null
cone, `omega^2=n^T B^T B n`. The scalar block has five variables: field,
momentum and three gradient variables. Maxwell has six: electric and magnetic
components. Zero principal speeds include auxiliary/constraint directions;
they should not be identified as additional kinds of light. The extraction
sets non-frame background fields to zero and tests derivative blocks only.
It does not establish the full coupled symbol on arbitrary matter backgrounds.

A held-fixed nonorthogonal frame and oblique direction prevent an accidental
axis-only or identity-metric result:

\[
B=\begin{pmatrix}2&1&0\\0&3&1\\1&0&2\end{pmatrix},
\quad n=(1,2,3),\quad\det B=13,\quad |Bn|^2=146.
\]

The actual symbolic characteristic polynomials are
`lambda^3 (lambda^2-146)` and `lambda^2 (lambda^2-146)^2`.
The deliberate identity-frame substitution instead gives speed squared 14
and fails the metric comparison. Nonzero declared mass squared 7 and charge
coupling 5 do not change these principal derivative blocks.

This is a useful existing unification: one geometric kinetic contraction
controls two matter sectors. It is **encoded in the selected continuum law**,
not derived from fixed-six Rule3, integer arithmetic or load balancing.

## From that cone to geodesics: the missing limit

Harte's original paper, [arXiv:1808.06203v2](https://arxiv.org/pdf/1808.06203),
section 2.1, equations (2)–(6), derives the high-frequency eikonal relation
`g^{mu nu} k_mu k_nu=0` and the null-geodesic transport of its rays from the
scalar wave equation. The introduction and section 2 distinguish this limit
from finite-frequency wave propagation, including corrections and tails.
The result does not assert that every wavepacket center is exactly geodesic.

Applied to Universe24, the following is a proposed inference, not an executed
physical result: if actual refined Engine matter solutions converge to these
wave equations, and there is a window
`grid spacing << wavelength << curvature scale`, their appropriate geometric
optics rays should approach null geodesics of the same reconstructed metric.
The principal-block identity is one prerequisite. It supplies neither that
convergence nor a bound on the two limiting errors.

The centered spatial difference in the present compiler replaces a Fourier
covector component by `sin(k_i dx)/dx`. This differs from `k_i` at finite
resolution and vanishes at Nyquist. Therefore equality of continuum cones is
not an equality of finite-lattice packet trajectories. A face-neighbor causal
bound alone does not supply the metric cone. Timelike massive packets and
charged packets need separately stated limits; electromagnetic forces need
not produce geodesic motion.

## What the existing geodesic and clock tests actually show

| Construction | Established result | Boundary |
| --- | --- | --- |
| `observe/metric_clocks.py:5` | Exact contraction of metric with supplied tangent gives instantaneous proper-time rate | No worldline integration or independently ticking apparatus |
| `tests/test_conformal_flrw.py:15` | Metric-derived Einstein tensor and two symbolic timelike/null geodesic families agree with the prepared FLRW sector | Actual retained proper-time and affine counters follow prepared polynomials; the null test does not transport a packet across board nodes |
| `validation/geometry/ppwave_geodesic_clock.py:30` | Actual fixed-six test-worldline registers respond to a neighboring geometric input and rewind | One-axis phase-space position stays inside one computational node; explicit one-way terms, preparation/calibration and restricted curvature sectors |
| Main 44-channel adapter/readout | Exact replay and passive metric/source reconstruction from the pinned old sign law | Unconstrained mechanical seed; arithmetic clicks are not operational spacetime events |
| PR50 corrected 45-channel proposal | Shared sourced frame, fixed local quadratic tensor, corrected flat continuum symbol and exact mechanical replay | No nonlinear discrete-constraint proof, nondegeneracy theorem, packet geodesics or material clock |

Fresh main verification:

```bash
python -m unittest universe24.tests.test_conformal_flrw \
  universe24.tests.test_metric_clocks \
  universe24.tests.test_ppwave_geodesic_clock -v
```

All **14 tests passed** (1.504 seconds). This includes tests whose success
consists of retaining a known physical failure or decoder limitation.

## Latest published geometry audit independently rerun

The new runner also reexecutes PR50's existing `symbol_audit` and
`compile_audit`; these are reported separately from our new matter calculation.
The original full and triangular frame formulations have off-constraint
Jordan chains. The corrected full-frame flat symbol satisfies the exact
all-direction square-free annihilator

\[
A(A^2-|n|^2I)(A^2-|n|^2I/2)(A^2-|n|^2I/8)=0.
\]

The corrected triangular shortcut still fails oblique directions. The 45-channel
candidate compiles to 881 degree-two monomials, with strict face support,
135 retained integers per node and static multiplier 64. Three updates on
27 nodes agree with its independent scalar evaluator; all six remainder
classes and complete rewind pass. Maximum retained size is 77 bits in this
short mechanical fixture. The source report's positive metric, nonlinear
constraint, bit-growth and operational-apparatus blockers remain explicit.

PR47's earlier sourced refinement evidence is mixed: time refinement and an
exploratory joint sequence improve its reported defects, while several
original spatial/joint series fail. The 44-channel protecting theorem applies
to its triangular amplitude construction and does not automatically transfer
to PR50's full 3-by-3 frame. Reported source changes in newer issue comments
must be pinned and rerun before becoming evidence for this audit.

## Next falsifying test

Use one declared source law and same metric to generate massless scalar and
Maxwell packets on a nontrivial slowly varying background. Predeclare oblique
directions, both signs, boundaries, geometry-disconnection controls, endpoint
and wavelength/grid refinement. Independently reconstruct Christoffels from
the saved metric and compare the measured phase/ray transport to null
geodesics. Do not feed that reference trajectory into the Engine. Record the
full constraint residuals and bit cost alongside the trajectory discrepancy.

Start with a test-field limit explicitly, then test source backreaction and
material clock records within the same 48-channel allocation. A successful
geodesic limit is still distinct from deriving Einstein's source equations.

Reproduction of this report's new symbolic check and published PR50 reruns:

```bash
git worktree add --detach ../geometry-pr50 62202fdccdd9a40d5dbbec104de6f97d9587a999
python -m validation.einstein_node_audit.principal_cones \
  --source ../geometry-pr50 --out runs/einstein-node/04_geometry.json
```

The runner requires the exact clean source pin, imports it only in an isolated
Python process, and records source hashes and limitations in the JSON report.
It changes no production Engine, tensor, decoder or physical acceptance gate.
