# Integration audit: one Engine, several physical and experimental systems

Baseline: GitHub `Closer24/Universe24` main
`7d238e84a2167a4d3fe7bc7942da0cbf97bd29b2`, including Frame48 (#36) and
Bell/Born references (#37). The local reconstructed snapshot was `467b685`;
it is not GitHub ancestry. Current active source and text files were checked
against remote blob hashes. Pre-fixed-six archives are outside this audit.

## Finding

The project already has a coupled classical gravity/matter model in ADM.
Its scalar and dust sources influence geometry, and geometry influences the
scalar. That positive result is distinct from the integration gap:
communication, the causal-click wave and the transported probe are independent
components. Sharing the same fixed-six Engine and storage cube does not make
their propagation, detection or energy obey the ADM geometry.

The new graph audit counted **zero cross-owner factor edges** in the actual
four-component assembly. This is intentional in `core/channels.py`, which
rejects undeclared cross-owner terms. It prevents accidental claims that an
experimental detector or external Born draw contributes to physical stress.

| Component | Retained channels in this construction | Established role | Relationship to ADM |
| --- | ---: | --- | --- |
| Einstein | 4,771 | Spatially varying discretized classical ADM, complex scalar and comoving pressureless dust | Owns physical metric and stress; internal two-way coupling |
| Communication | 54 | Transport lanes and reference receivers | Independent audit state; no metric read or stress source |
| Transported probe | 26 | Probe with its own test chart | Independent; general common-metric gate remains false |
| Causal wave | 9 | Computational-cone arrival, C2 memory, response | Independent; no metric read or stress source |
| Frame48 | 48, standalone | Reversible nonlinear vacuum-frame candidate | Not assembled; several general GR gates fail |
| Compact FLRW | 8, standalone | Prepared homogeneous isotropic flat dust/radiation family | Separate restricted model with retained prepared counters |
| Compact null wave | 2, standalone | Transported prepared pp-wave profile and exact geometric readout | Separate restricted model; no clock apparatus |
| Joint Born reference | External Python data/sampler | Explicit assumed quantum reference | No Engine or stress-energy feedback |

All four assembled owners together have 4,860 channels. The factor-edge
occurrence counts are 19,784 Einstein-to-Einstein, 306 communication-to-
communication, 60 probe-to-probe and 32 causal-wave-to-causal-wave. They count
factor occurrences, not physical interactions or unique graph edges.

## Executed evidence

Runs are under `runs/six-lens/06-integration/`. Set
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1` for each command below.

| Command | Fresh result |
| --- | --- |
| `python experiments/research/six_lens_integration.py` | Zero cross-owner factors; three preparations, six updates each; exact counterfactual equalities and full rewind |
| `python experiments/geometry/frame48_audit.py --out runs/six-lens/06-integration/frame48` | All five audit cases completed, exact lifts/inverses, failed physical gates retained |
| `python -m unittest universe24.tests.test_frame48 -v` | 10 passed, 9.708 s |
| `python -m unittest universe24.tests.test_channels -v` | 5 passed, 34.951 s, including actual ADM output preservation and complete C2 trace replay |
| Five physical ADM tests listed below | 5 passed, 43.082 s |

The new counterfactual experiment uses the real compiled complex-scalar/dust
ADM component with communication and causal wave, L=3. At preparation only:

1. Double both retained histories of the existing positive-x wave lane,
   keeping every Einstein channel fixed.
2. Independently prepare spatial `g00` four times larger, keeping the causal
   wave preparation fixed.

For every complete snapshot at microticks 0 through 6, experiment 1 leaves
the entire Einstein `(a,b,r)` state unchanged, while experiment 2 leaves the
entire causal-wave state unchanged. All three preparations rewind exactly.
The saved tensor and all 21 complete snapshots are in
`wiring/counterfactuals.jsonl.gz`; the report records source and artifact hashes.
The absence of cross-owner factors establishes isolation for subsequent
updates too; the six-step execution is a concrete check, not the sole reason.

## What the ADM work has established

The freshly rerun tests are:

- `TestFullADM.test_matter_sources_geometry_with_correct_coefficient`: the
  sourced-minus-unsourced difference in each diagonal K is independently
  predicted as `-1/8192`. This control deliberately changes the initial constraint and
  isolates the source coefficient.
- `TestFullADM.test_geometry_feeds_back_on_scalar`: changing K00 changes Pi
  by the independently expected `3/65536`.
- `TestIndependentPhysics.test_massless_anisotropic_solution_with_full_4D_einstein_tensor`:
  an independent four-metric calculation gives the full Einstein tensor
  `diag(1,1,1,1)/128` for the specified scalar solution; the ADM RHS and
  constraints match the analytic initial slice.
- `TestIndependentPhysics.test_spatial_discretization_converges_on_nonlinear_metric`:
  Ricci error decreases by more than a factor three on each L=9,17,33
  refinement of the specified nonuniform conformal metric.
- `TestDarkMatter.test_independent_full_einstein_dust_solution`: an independent
  four-metric calculation gives `diag(3/256,0,0,0)` for the stated dust FLRW
  slice. This is an analytic equation check, not a long dynamical run.

These are meaningful internal physical-equation and numerical-consistency
checks. They are not comparisons with measured laboratory data. The Engine
exactly evaluates the **chosen discrete** Euler/midpoint update, including
rational inverse-metric expressions. Spatial centered differences, time
truncation and initial quantization still approximate the continuum problem.
Constraints are monitored, not maintained by an exact discrete Bianchi
identity. Finite compiler workspace grows with the predeclared horizon;
indefinite bounded-memory gravity, generic strong-field stability and a
continuum limit for all observables remain unestablished.

The complex ADM scalar is a classical U(1) field with a current and stress
tensor. Opposite charge signs are useful classical controls; their existence
does not establish quantized particles, spin, quantum annihilation or a
many-particle Hilbert space. Similarly, an affine counter named `light` in the
FLRW sector does not constitute an emitted, detected photon.

## What changed with Frame48, and what did not

The fresh Frame48 run confirms 48 channels, 762 monomials, degree two and
strict single-edge support. It has no compiler clock ring or growing
finite-horizon circuit. Flat data stayed stationary for 120 updates. Generic
spatial data and nonlinear integer data updated and rewound exactly.

The same run retains decisive limitations:

- Two individually constrained retained slices yield H=4 after one update;
  compatible time-pair initialization and constraint propagation are absent.
- An initially invertible pair yields singular frames at all 27 nodes after
  one update. Exact inversion of the register dynamics does not preserve an
  invertible physical metric.
- `dt=1/2` or `1/16` at fixed dx=1 is rejected because coefficients cease to
  be integral. A special joint dt/dx refinement exists, but is not arbitrary
  precision at fixed geometry.
- The nonlinear six-update control reaches 172-bit integers and 1,890 C0
  events, with zero C1/C2. This is evidence of nonlinear reversible arithmetic,
  not particle complexity, physical-clock validation or growing structure.
- Matter coupling and retained operational clocks remain absent. Its decreasing
  floating Kasner reference errors are explicitly outside the integer Engine.

Thus Frame48 is a useful candidate toward a fixed-budget gravitational law.
Its failed gates do not invalidate the separate ADM discretization and its
passing scalar/dust checks. Neither construction currently supplies a shared
quantum detector, photon propagation and gravity experiment.

## Decisive next integration gates

1. **One operational geometry experiment.** Use one declared metric authority.
   Start with the existing ADM massless scalar as a controlled *classical wave
   analogue*, not a photon claim. On that same geometry, compare propagation
   times, phases and two independently evolving clock apparatuses across
   lapse/shift changes and spatial/time refinement. Reading metric rates alone
   is insufficient. Do not attach an independently timed audit cone by label.
2. **Declared detector interaction.** Couple an explicitly represented detector
   to that carrier and retain its memory/environment. Test no early response,
   stable records, repeated preparations, one-versus-two outcomes, recoil or
   backreaction and an appropriate conservation balance. A test-field limit
   may neglect backreaction only as a stated controlled approximation.
3. **Quantum gate after common dynamics.** Specify what represents coherent
   alternatives, joint states and local measurement operations. Test the
   Born/detector and full-emission Bell requirements identified by agents 3/4.
   Reversible classical state retention, adding |psi|² as a force, and a
   separate joint random sampler do not by themselves supply this structure.
4. **Common empirical protocol.** Calibrate units and preparation once; predict
   phase-, setting-, distance- and geometry-dependent observables on held-out
   conditions, with detector inefficiency and uncertainty explicit. A passing
   internal test suite verifies the implemented law, not agreement with nature.

This is a tractable route from separate successful pieces to a single tested
experiment. 'One universe as one clock' can mean one interacting retained
system of relational events. It still requires these interaction terms and
observable clock relations. A desire for complexity is not yet a specified
equation, state function or empirically tested selection principle.

## Sources and scope

Code paths inspected: `core/channels.py`, `layers/universe.py`,
`layers/adm.py`, `layers/frame48.py`, `layers/conformal_flrw.py`,
`layers/null_wave.py`, `observe/metric_clocks.py`, the corresponding tests,
and the standalone Bell/Born experiment. Primary literature consulted:

- [Gourgoulhon, 3+1 Formalism and Bases of Numerical Relativity](https://arxiv.org/abs/gr-qc/0703035):
  reference framework for separating Einstein evolution, constraints, matter
  equations and choices of foliation. This supports the stated validation
  categories, not the correctness of this implementation.
- [Schlosshauer, Decoherence, the measurement problem, and interpretations of
  quantum mechanics](https://arxiv.org/abs/quant-ph/0312059): distinguishes the
  decoherence program and its interpretive/measurement questions. No claim
  that the present reversible record is an implemented decoherence model.

No production dynamics were edited. The added helper only assembles existing
components, prepares controls, measures them and writes reproducible evidence.
