# Universe24: one Einstein event board

The default entry point is `python -m universe24`. Einstein evolution is in the
installed package, not an optional observer added to a separate default model.
The fixed tensor evolves a spatial metric, extrinsic curvature, complex scalar
matter and dark dust together. Preparation solves initial constraints; the
Engine computes all subsequent states with integer Rule3.

## Matter and antimatter convention

Use a canonical complex scalar `Phi=(phi+i chi)/sqrt(2)` and its two normal
momenta `Pi=n(phi)` and `Pi_chi=n(chi)`. The Lagrangian is

    L = -1/2 sum_A [g^{mu nu} d_mu phi_A d_nu phi_A + m^2 phi_A^2].

The contraction uses the inverse metric; the two real fields are phi and chi. The code sums the two canonical real-scalar
stress tensors. Both charge signs have positive energy density for m^2 >= 0.
There is no negative gravitational mass switch for antimatter.

The exact classical charge conjugation is

    C: (phi,Pi,chi,Pi_chi) -> (phi,Pi,-chi,-Pi_chi).

It leaves `T_mu_nu`, initial Einstein constraints and subsequent geometry
unchanged, and reverses the Noether current. Tests check this through the
actual integer Engine, not only in the passive field formulas. The default
initializer puts positive and negative local charge regions on the same board.
Its initial scalar momentum density is zero because chi=Pi=0, even though
Pi_chi varies spatially. Both signs enter the initial Hamiltonian solve through
the same positive energy.

The source is constructed independently from matter; it is never defined as
the measured Einstein tensor. The complex field feels the metric through its
inverse, covariant Laplacian, lapse, shift and extrinsic curvature. Its stress
sources the curvature equation and constraints. Dark density adds to the same
source and evolves with the local expansion. This is mutual coupling in one
fixed tensor.

This is a **classical scalar matter/antimatter charge model**. The current is
associated with a global U(1) symmetry. It is not electromagnetic charge coupled
to a Maxwell field in this implementation. It is not a quantum particle counter,
Dirac fermion model, Standard Model, or particle-antiparticle annihilation model.
Einstein's equations alone do not specify those matter dynamics. The older
Dirac, gauge and clock builders remain named research components; their names
do not establish a generally covariant source and they are not silently added
to the default stress tensor.

## Two levels of events, with an explicit connection

1. **Integer Engine events.** Rule3 changes retained triples. Physical
   numerator/denominator registers have the `official` readout label. Clock and
   computational workspace registers have the `audit` label. Labels only affect
   readout; they never change an update. `official_events.jsonl.gz` contains the
   actual `Engine.clicks(...).select('official')` records: microtick, register,
   cube node, exact quotient and click kind. A nonzero quotient in an unchanged
   triple is not exported as a click.
2. **Physical mesh events.** A physical snapshot at node `(ix,iy,iz)` has chart
   `(step*dt,ix*dx,iy*dx,iz*dx)`. Its fields are read only after all their
   arithmetic dependencies are stable. `event_board.json` records numerator and
   denominator register names, coefficients and readiness microticks for every
   physical field. Constant terms explicitly have no source register.

The full integer journal preserves every state, including audit workspace.
The board exports exact metric and stress tensors at every physical event in
`event_tensors_N.json.gz`. The interactive HTML displays numerical conversions
of those same values. It does not run another simulation in JavaScript.

Metric reconstruction, shared spatial lengths and local angles use the evolved
metric. The square grid in the display is a coordinate diagram. Its pixels are
not a Euclidean embedding of curved spacetime. Finite link lengths use the
declared metric approximation; they are not exact finite geodesic distances.

## Error reporting and scope

The four Einstein constraints are measured at each snapshot. The complex
current is computed separately and its spatial balance defect is recorded.
Volume-weighted charge uses floating-point quadrature of `sqrt(det gamma)`
only as an observer. Its finite-step drift is reported; exact arithmetic does
not imply exact discrete stress/current conservation or a discrete Bianchi
identity. Spatial differences and Euler/midpoint integration have truncation
errors.

The compiled physical horizon is fixed before the run. Workspace and integers
grow with its length. Running beyond the declared clock horizon is not a valid
continuation. Dust assumes a single geodesic flow before caustics. Long-time,
strong-field, halo and quantum physics are not validated.

## Measured integration checks

All 141 tests on the integrated fixed-six main pass. The 25 focused
Einstein/compiler/conjugation/fixed-divisor checks also pass. Package version
0.4.0 builds and imports outside the checkout without any experiment-module
dependency. The full one-step integer trace and physical event outputs match
the pre-port implementation exactly. Main's Engine source is unchanged.
See [integration evidence](evidence/universe24_integration.json).

| Same final coordinate time 1/64, L=3 | One Euler step | Two half steps |
| --- | --- | --- |
| Engine microticks | 96 | 164 |
| Registers per node | 4,771 | 11,111 |
| Official physical-register clicks | 1,134 | 2,268 |
| Maximum Hamiltonian residual | 1.14456e-5 | 6.02292e-6 |
| Maximum momentum residual | 2.25880e-5 | 2.25357e-5 |
| Complete retained-state rewind | exact | exact |

The Hamiltonian error decreases while the momentum error has a spatial/discrete
floor in this comparison. Neither is claimed zero. The two-step retained
integers reach 97,980 bits. See [machine-readable evidence](evidence/universe24_integration.json).

The HTML payload and JavaScript control logic were checked. Browser visual
verification was blocked by this workspace's browser/socket restrictions; no
visual browser pass is claimed.

## Naming and migration

The package, CLI, CI and active module paths use Universe24. The fixed-six reference
construction has explicit `reference_model` / `reference_system` / `reference_seed`
names; the retired unified matter module is `unified_matter`. Main retains its
archived pre-migration records. Reference state and oracle checks continue under
the new paths. No old-name
import aliases are installed. Historical research records retain original
evidence identifiers, names and timestamps.

The old `experiments/geometry/adm_*` entry points delegate to package modules
for reproducibility. The installed runtime imports no experiment code. The
shared Engine and its scalar recurrence are unchanged.

## Sources

- [Gourgoulhon, 3+1 formalism](https://arxiv.org/abs/gr-qc/0703035): Einstein evolution and constraints.
- [Einstein Toolkit ScalarEvolve](https://einsteintoolkit.org/thornguide/Scalar/ScalarEvolve/documentation.html): complex Einstein–Klein–Gordon formulation; its field normalization and momentum convention differ from those explicitly defined above.
- [Liebling and Palenzuela, Dynamical boson stars](https://doi.org/10.1007/s41114-023-00043-4): complex scalar stress and conserved U(1) current.
- [CERN ALPHA-g result](https://home.cern/alpha-experiment-at-cern-observes-the-influence-of-gravity-on-antimatter/): experimental antihydrogen gravitational attraction, consistent with treating antimatter gravitationally as matter. This does not validate the scalar approximation to atomic antimatter.
