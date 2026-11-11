# Full nonlinear Einstein evolution compiled into integer Rule3

This optional construction implements the general 3+1 Einstein evolution
equations, a real Klein–Gordon field, optional cold pressureless dark matter,
and all four Einstein constraints. No homogeneity, diagonal-metric or weak-field
expansion is imposed on the equations. The tests use regular, modest fields.
Lapse and shift specify the coordinate gauge. Every numerical update runs
through the unchanged integer Engine: the RHS is not injected by an observer.

The correspondence is **equation by equation after discretization**. The
finite mesh is not exactly the continuous Einstein spacetime. Constraints have
measured truncation error; they are not projected to zero during a run. This
is a new, optional tensor, not an emergent-GR claim about default ONE or its
previous raw-click interpretation. All earlier experiments remain available.

## Run the entire pipeline

Requires Python, NumPy, and the optional validation dependency SymPy:

```bash
python -m pip install '.[validation]'
python experiments/geometry/adm_integer.py --case dark --steps 2 --dt 1/128 --out runs/geometry/adm/dark
python -m unittest universe24.tests.test_adm_integer -v
```

`--case dark` automatically prepares inhomogeneous scalar and dark-density
profiles, solves the initial discrete Hamiltonian constraint, quantizes the
seed, builds one fixed integer tensor, runs the declared horizon and verifies
complete reversal. It exports physical fields, the metric, stress, lengths,
angles, constraint errors and a lossless full-state journal. No settings or
coefficients change after preparation.

Other cases: `scalar` (homogeneous massive scalar), `massless` (an anisotropic
analytic comparison), `gauge` (quantized vacuum gauge wave), and
`inhomogeneous` (spatially varying massive scalar with harmonic lapse).
`--L` chooses the periodic board; the constrained initializer requires odd L.
`--method midpoint` selects explicit midpoint instead of Euler. `--steps`
counts physical time steps, each compiled into many Engine microticks.

## Variables and complete equation coverage

Use signature (-,+,+,+), c=kappa=1 and kappa=8*pi*G/c^4. Define

    ds^2 = -alpha^2 dt^2 + gamma_ij (dx^i+beta^i dt)(dx^j+beta^j dt),
    K_ij = -(partial_t-L_beta) gamma_ij / (2 alpha),
    Pi = n^mu partial_mu phi,    V(phi)=m^2 phi^2/2.

`g00,g01,...,g22` are the six **spatial** metric components; report keys
`metric.00,...,metric.33` are the four-dimensional spacetime metric. There are
18 physical/gauge fields: gamma(6), K(6), alpha, phi, Pi, beta(3), or 19 when
the dark rest density is enabled. Arithmetic workspace is additional.

| Einstein or matter equation | Code operation |
| --- | --- |
| Six spatial-metric equations | `dot gamma_ij = -2 alpha K_ij + L_beta gamma_ij` |
| Six extrinsic-curvature equations | Full Ricci, quadratic K, lapse Hessian, stress and optional Lambda terms |
| Hamiltonian constraint | `H = R3 + K^2 - K_ij K^ij - 2 rho_total - 2 Lambda` |
| Three momentum constraints | `M_i = D_j K^j_i - D_i K - j_i` |
| Klein–Gordon pair | Evolve phi and Pi with metric, lapse, shift, mass and spatial derivatives |
| Scalar-only lapse gauge | `dot alpha = -alpha^2 K + beta^i partial_i alpha` (harmonic slicing) |
| Dark-matter lapse gauge | Uniform positive initial lapse, `dot alpha=beta^i partial_i alpha` (geodesic slicing) |
| Shift gauge | Three prescribed time-independent shift fields, `dot beta^i=0` |
| Optional dark continuity | `dot rho_d = alpha K rho_d + beta^i partial_i rho_d` |

Six equations for K plus four constraints are the ten independent Einstein
equations in 3+1 form; the six gamma equations define K as the rate of metric
change. Lapse and shift are gauge choices, not missing Einstein equations.
All nonlinear terms are retained. A nonzero cosmological constant is supported
by the construction API and independently checked with de Sitter data; the CLI
preparations use Lambda=0.

The full curvature update is

    (partial_t-L_beta) K_ij = -D_i D_j alpha
        + alpha (R3_ij + K K_ij - 2 K_ik K^k_j)
        - alpha [S_ij - gamma_ij (S-rho_total)/2]
        - alpha Lambda gamma_ij.

For the real scalar,

    rho_phi = (Pi^2 + gamma^ij partial_i phi partial_j phi)/2 + V,
    j_i = -Pi partial_i phi,
    S_ij = partial_i phi partial_j phi
         + gamma_ij [(Pi^2-grad(phi)^2)/2 - V],
    (partial_t-beta^i partial_i) phi = alpha Pi,
    (partial_t-beta^i partial_i) Pi = alpha (D^i D_i phi + K Pi - m^2 phi)
                                    + D^i alpha D_i phi.

The source in the K equation simplifies exactly to
`partial_i phi partial_j phi + (V+rho_d/2) gamma_ij`. This is an algebraic
identity for the declared matter models. Full T is also constructed separately
from the scalar gradient, metric and dark fluid; T is never defined as G.
The matter changes K, K changes the metric, and the metric/lapse/curvature feed
back into matter. Tests isolate both directions of that response.

## Dark matter gravitates

Within GR, dark matter contributes to the same stress-energy source as other
matter. Its microscopic identity is unknown. This implementation chooses a
specific macroscopic cold model:

    T_dark(mu,nu) = rho_d n_mu n_nu,
    pressure_dark=0,   j_dark=0,   S_dark=0.

The density is a retained evolving field, not a fixed background profile.
It enters the Hamiltonian constraint, the K update and spacetime T_00. Normal
comoving pressureless flow is geodesic when D_i alpha=0; therefore the dark
option selects geodesic slicing and rejects a nonuniform initial lapse. The
coordinate velocity of the normal flow is -beta. Scalar matter can still be
inhomogeneous and exchange influence with the geometry.

This is irrotational, single-stream dust before caustics. It does not model
velocity dispersion, intersecting streams or virialized halos; those require
a kinetic/particle or more general fluid matter module. It does not identify
dark matter with the scalar, infer its particle type, or confuse it with dark
energy. Lambda is a separate optional source parameter.

## Exact integer arithmetic inside the original Engine

`integer_circuit.py` constructs a DAG of integer addition, multiplication and
face shifts. Rational physical values are pairs of retained integer
expressions. Division swaps numerator/denominator expressions and multiplies;
there is no floating-point division in evolution. Symbolic cancellation and
common subexpressions are resolved before building the tensor. No numerical
future state is computed into the seed.

Each arithmetic output z starts with a_z=b_z=0. Once its parents are stable,
its retained clock c takes values +1,-1 on two consecutive updates. Its fixed
input is

    u_z = D*b_z + (D/2)*c*F(parents),    D=6, Q=1.

Rule3 gives `z_next=2*z-z_previous+c*F`, with unchanged remainder. The two
updates take (a,b) from (0,0) to (0,F) to (F,F); z then remains stationary
until the end of the declared horizon. A linear register ring supplies the
clock pulses under the same Rule3:

    u_clock,j = (D/2) (b_clock,j-1+b_clock,j+1),
    b_clock,j(0)=pulse(j),  a_clock,j(0)=pulse(j-1).

Thus `b_clock,j(t)=pulse(j+t)`; there is no runtime scheduler or callback.
Parent readiness sets each gate's pulse phase at construction. The period
exceeds the entire run, so pulses do not repeat during the declared horizon.

F is linear or a two-input product, making each clocked monomial degree at
most three (tensor rank four). A shift reads one face neighbor plus its
on-site clock. Cross-axis products use on-site intermediates populated by
earlier legal shifts. There are no old-a reads in the tensor, so its inverse
dependencies are acyclic. Every source and coefficient is fixed before run.

This addresses the earlier DIRECT one-step obstacles: inverse metrics are
exact rational arithmetic, and mixed spatial stencils use retained relays.
The numerical integrator is compiled into Rule3, not evaluated outside the
Engine and inserted as a time-dependent input. Initial-data Newton solves and
plotting may use floats; the actual state updates use only exact integers.

## The mesh geometry and event map

A physical mesh event has label `(physical step,node)` and coordinates
`(step*dt, ix*dx, iy*dx, iz*dx)`. The report records when each physical snapshot
has become stable in Engine microticks. All four-metric entries follow from
evolved gamma, alpha and beta. At every checked node the spatial metric is
positive definite, lapse is positive, and signature is Lorentzian.

Ten signed squared tangent-simplex edges use coordinate basis
`diag(dt,dx,dx,dx)` and recover the entire metric by polarization. Shared
spatial edges use one symmetric endpoint-average metric. Local angle cosines
are stored by exact sign and cosine-squared rational data. The geometry files
therefore reflect the same evolved state as the field equations; no separate
drawn surface, imposed time-varying metric or fitted expansion is substituted.

These finite edge lengths are discretized geometric measurements, not exact
finite geodesic distances in a smooth curved manifold. Raw arithmetic
microtick clicks are not asserted to be all continuum spacetime events. The
explicit numerical event chart is the implemented mapping. Default ONE's
other event/particle sectors have not been automatically coupled to this
new tensor or operationally calibrated to it.

## Discretization, constraints and finite horizon

Spatial differentiation uses centered first differences and their compositions
throughout, including Hessians. Ricci comes from centered derivatives of the
connection plus its full quadratic products, then is symmetrized to remove an
O(dx^2) antisymmetric finite-product-rule defect. This is a consistent
second-order spatial approximation, not an exact discrete Bianchi identity.
Composed central differences have checkerboard null modes on even boards;
odd grids are preferred and required by the constrained initializer.

Time integration is Euler or explicit midpoint. Every chosen discrete update
is evaluated **exactly** by integer arithmetic, including its rational inverse
metric. The approximation is to continuous Einstein evolution. Initial-data
quantization and spatial/time truncation remain. Four constraints are
calculated in retained circuit registers at every physical snapshot. They are
initially solved/checked and monitored, not silently repaired or claimed zero.

The circuit retains all workspace and past physical states. A chosen finite
horizon is compiled before running; requesting more physical steps grows the
tensor and integer sizes. Continuing beyond its declared microtick horizon is
not a valid next physical step. This is not yet a bounded-memory perpetual
automaton. Exact computational rewind uses the retained history; it does not
make Euler physically time-symmetric or symplectic. Long-time ADM stability,
strong fields, singularities and production astrophysics are not validated.

## Initial data and evidence

The inhomogeneous initializer uses gamma=psi^4 C with a fixed non-diagonal
positive matrix C, K_ij=-k gamma_ij, Pi=0, nonuniform phi and optional nonuniform
rho_d. Newton solves the actual discrete Hamiltonian residual and a conformal
normalization for psi and k. Quantization preserves K's proportionality to
gamma using a common integer denominator, keeping the discrete momentum
constraint exact initially. The remaining Hamiltonian quantization error is
reported. Preparation never injects subsequent states.

Tests cover every arithmetic register against a passive integer-DAG oracle,
exact complete rewind, full trace replay, strict support, off-diagonal and
spatially varying data, both directions of matter/geometry feedback, dark
density sourcing/evolution, compatible gauge, nonzero Lambda, independent full
4D Einstein checks of massless Bianchi and dust FLRW solutions, and analytic
spatial-curvature refinement.

Measured controls include:

| Control | Result |
| --- | --- |
| Massive scalar, one Euler step dt=1/64 | final max Hamiltonian residual 7.00136e-6 |
| Same final time, two Euler steps dt=1/128 | final max Hamiltonian residual 3.49777e-6 |
| Massless analytic solution, midpoint dt=1/8 | local maximum field error 1.77127e-6 |
| Same analytic family, midpoint dt=1/16 | local maximum field error 2.20911e-7 |
| Inhomogeneous scalar, L=3, dt=1/64 | initial H 6.83854e-7; final H 1.19756e-5 |
| Same initial data, dt=1/128 | final H 3.35433e-6 (different final time) |
| Inhomogeneous scalar plus dark matter, L=3, dt=1/64 | initial H 7.36557e-7; final H 1.12933e-5; max momentum residual 3.16227e-6 |
| Same dark initial data and final time, two steps dt=1/128 | final H 5.77058e-6; max momentum residual 3.17397e-6 |

The midpoint comparison is a one-step/local-error comparison at different
end times, not a fixed-end-time global convergence measurement. A separate
analytic nonuniform metric test refines L=9,17,33 and verifies the expected
spatial error reduction. Increasing L in a different constrained preparation
alone is not a monotone-error certificate.
The dark run's Hamiltonian error approximately halves at fixed final time;
its momentum error does not, exposing remaining spatial/discrete error rather
than hiding it behind exact arithmetic.

One generic scalar Euler step uses 4,171 gears and 9,596 monomials over 98
Engine ticks. The dark option's geodesic gauge uses 4,061 gears and 9,392
monomials over 96 ticks. These are arithmetic registers per node, not thousands
of new physical fields. Arbitrary-precision paths are exercised. The earlier
50 checks and 16 ADM/compiler/dark-matter checks pass; no core/default change
is involved.
The completed two-step inhomogeneous dark run uses 9,727 gears, 21,372
monomials and 164 Engine microticks; full reversal passes. Retained workspace
integers reach 97,980 bits and the lossless trace is about 157 MB, illustrating
the current cost of exact unreduced arithmetic and a retained history.

## Output and provenance

- `tensor.json`: complete fixed law and fingerprint.
- `full_trace.jsonl.gz`: seed plus lossless hexadecimal b changes for every
  microtick. Since a_next=b and r stays fixed, this reconstructs every complete
  retained triple. `replay_trace` verifies the format without pickle.
- `physical_N.json.gz`: every physical field at every node, as exact integer
  numerator/denominator pairs in hexadecimal.
- `geometry_N.json.gz`: shared spatial squared lengths and exact local angle
  data derived from that snapshot.
- `report.json`: parameters, event chart, readiness ticks, exact geometry
  sample, constraint errors, forward/reverse audit, sizes and source hashes.

## Primary sources

- [Gourgoulhon, 3+1 Formalism and Bases of Numerical Relativity](https://arxiv.org/abs/gr-qc/0703035): ADM evolution, constraints, matter and gauge conventions.
- [Einstein Toolkit, ScalarEvolve](https://einsteintoolkit.org/thornguide/Scalar/ScalarEvolve/documentation.html): coupled Einstein–Klein–Gordon equations. Its scalar momentum and complex-field normalization differ; this implementation explicitly uses a canonical real scalar and Pi=n(phi).
- [Einstein Toolkit, FLRWSolver](https://einsteintoolkit.org/thornguide/EinsteinInitialData/FLRWSolver/documentation.html): dust cosmological initial data and Einstein–de Sitter reference. This is an initial-data module, not the solver implemented here.
- [ESA, The dark Universe](https://www.esa.int/Science_Exploration/Space_Science/Euclid/The_dark_Universe): gravitational evidence for dark matter and the unresolved particle identity.

The integer compiler is this repository's construction. No cited source is
claimed to have supplied this Rule3 encoding or established its unlimited
stability or physical equivalence to the default event model.
