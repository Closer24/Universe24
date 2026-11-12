# Eight-researcher continuation: clocks, geometry and native arithmetic

This is a source-only continuation of PR50 at
`62202fdccdd9a40d5dbbec104de6f97d9587a999`, coordinated in
[issue40](https://github.com/Closer24/Universe24/issues/40) and
[issue41](https://github.com/Closer24/Universe24/issues/41).
The source is published in [PR52](https://github.com/Closer24/Universe24/pull/52).
It contains new proofs and executable constructions, not an accepted general
Einstein universe. The installed Engine and supported runtime are unchanged.

## Shared handoff

The prior full-frame symbol repair and massive-clock audit used different
tensors. `validation/completion/common45.py` closes that identity gap: its
explicitly massive full45 law, weak constrained seed, complete ownership and
ordinary system bundle are shared by clock and signal audits.

| Property | Common handoff |
|---|---|
| Channels | 24 geometry + 20 matter + 1 denominator =45 |
| Retained integers per node | 135, including all a,b,r registers |
| Parameters | mass squared1, coupling1, cosmological constant0, h=1/64, dx=1/4 |
| Tensor SHA256 | `6ea453fa77a5a9d74af5bd4fc626cfcdc8f92942b10c301d2d00814bf4d05ba0` |
| Complete seed SHA256 | `b53909631f3e14e3c09905275fe7b50a0dad2ecdec9ac431db2306127abd3b7c` |
| Seed | B=I, Kdiag=-1/10, phi=1/5, dust amplitude1/10, other fields0, D=100, old registers0 |
| Mechanics | 889 quadratic integer monomials, strict face support, all six carry values |
| Executed handoff | 27 nodes, three steps, independent scalar oracle, saved runtime trace, verify and full rewind |
| Peak bits | 7 at preparation, then22,51,110 |
| Added operational apparatus | None; three unused slots are not implemented clocks or detectors |

The current B, scalar, dust and electromagnetic fields all enter the same source
equations and metric. The source-removal control changes geometry. Arithmetic
clicks remain the existing passive protocol; scalar phase and ray formulas are
separate research observations, not an autonomous measured clock or particle.

## Eight proof and implementation packages

| Researcher | Report | Concrete result and boundary |
|---|---|---|
| 1 | [Formulation](01_formulation.md) | Exact arbitrary-frame full44 principal theorem and continuous linear constraint propagation along a massive homogeneous family; finite integer steps remain separate |
| 2 | [Native compiler](02_native_compiler.md) | Actual nine-tick nonlinear quotient drift/kick: 2 data + 2 workspace + 3 scheduler channels, all workspace restored; direct extension to 44 data fields would cost 91 channels |
| 3 | [Metric domain](03_metric_domain.md) | Distinct cubic45 law preserves full B nondegeneracy for every finite tick on its prepared domain; finite-h torsion failure is retained |
| 4 | [Matter clock](04_matter_clock.md) | Same-law I/S, stress and phase covariance; exact expansion correction to clock phase; separate coarse run resolves a sampled oscillation |
| 5 | [Signals and geodesics](05_geodesic_signals.md) | Actual scalar/Maxwell characteristic cones use the same B; conditional geodesic/phase oracles do not establish moving matter packets |
| 6 | [Time stability](06_time_stability.md) | Exact projective instability theorem and a distinct3-channel native wave with controlled carries, second-order fixed-time refinement and logarithmic per-integer bit growth |
| 7 | [Constraint closure](07_constraint_closure.md) | Cubic rational target preserves the reduced homogeneous constraint; its actual five-channel history lift fails at tick two, with an exact cross-history identity |
| 8 | [Independent integration review](08_integration_review.md) | Independent three/nine-tick force oracles, sharper carry bound, same-law/seed joins, actual budget and wrong-law rejection |

Each researcher inspected primary literature and coordinated dependencies in the
issues. Source-specific theorems are derived explicitly; they are not attributed
to papers merely because those papers discuss similar numerical methods.

## What the positive results do not combine into

| Law or claim | Status | Evidence boundary |
|---|---|---|
| Common massive45 mechanics and existing-runtime handoff | passed | Exact complete state, not physical acceptance |
| Corrected continuum principal system on invertible frames | passed | Does not give discrete time stability |
| Original projective wave-CFL stability | failed | Actual history-dependent amplification theorem |
| Original full45 metric preservation | failed | Constrained vacuum seed becomes singular in one tick |
| Cubic45 metric nondegeneracy | passed | Prepared memory domain; no uniform long-time conditioning claim |
| Cubic45 exact finite-h constraint propagation | failed | Explicit sourced transverse torsion control |
| Native linear-wave refinement | passed | Separate tensor; flat one-direction linear sector |
| Nonlinear native Einstein integration | blocked | Arithmetic, constraints, geometry and matter not yet joined |
| Common fine-step clock period | blocked | Projective bit growth prevents a useful resolved-period run |
| Coarse sampled massive oscillation | passed | Different h=1/4 tensor;14 steps,174385 bits, nonzero constraint defect |
| Operational proper-clock and moving wavepacket trajectories | not_tested | No counted autonomous detector/packet experiment |
| General coupled Einstein acceptance | blocked | Cannot be inferred by combining proofs for different laws |

The main constructive direction is to join the native arithmetic and stable wave
results with a discrete sourced constraint identity, then allocate geometry and
actual clock/detector state in one immutable law of at most48 channels. The cubic
metric theorem supplies one domain-preservation building block; its worsening
projective storage cost and torsion defect are explicit obligations.

## Reproduction

```sh
python -m validation.completion.run_all
python -m unittest discover -s universe24/tests -t . -v
python -m validation.system_smoke --out runs/completion-smoke
python -m universe24 verify --run runs/completion-smoke/run
```

The runner executes the common runtime handoff and all eight research audits.
Fresh evidence and source hashes are written to `runs/completion/`; the archived
integration snapshot is `docs/evidence/completion_nov12.json`. A successful
counterexample test deliberately leaves the corresponding physical gate failed.
The CI workflow repeats the full research runner on Python3.11 and3.12.

All inputs are prepared before evolution. Only Engine advances the retained
state. Norms, matrix inverses, rational readouts, continuum solutions and symbolic
algebra occur in preparation or passive validation and never feed a state update.
