# Newtonian acceptance on saved output

[The external checker](../tools/newton_output_checks.py) reads finished output only.
It does not import the simulator, instantiate a world, evaluate initialization
expressions, select a reaction, or repair state. Its standard-library-only CLI
also runs outside the repository. Known formulas belong in this measurement
layer, not in new engine code or runtime configuration.

This is a first, deliberately bounded set of Newtonian tests, not a claim of
all classical physics or a derivation from Universe24. Source formulas:
[NASA's motion laws](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/newtons-laws-of-motion/)
and [gravitational force](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/weight-gravitational-force/).

## Three separate questions

A software test asks whether the checker correctly rejects a bad measurement.
Physical acceptance asks whether actual saved output meets an independent target.
Emergence additionally requires showing that the target was not already imposed
by the model or its initialization. These results must never share one green label.
The current collision control already configures an elastic-contact rule and
momentum/mass transport. It tests output agreement, not emergence. No physical
formula was added to those runtime rules by this work.

## Measurement contracts

| Check | External target | Measurement and limit |
| --- | --- | --- |
| First law | `x(t) = x(0) + v(0)t`, constant momentum | One isolated body; velocity comes from the first position/time window, with at least two later held-out windows |
| Momentum/velocity | `p = m dx/dt` | Velocity comes from coordinates, not the momentum register; only constant-momentum windows are compared |
| Second law | `F_independent = m d2x/dt2` | A separately calibrated nonzero constant net-force trace, constant mass and resolved acceleration are required |
| Third law | `Delta p_A = -Delta p_B` | Nonzero simultaneous impulses at a co-located direct contact, with no field or external momentum owner |
| Related elastic check | `sum(p^2 / (2m))` constant | A declared elastic, closed two-body reference only; not a universal rule for inelastic interactions |
| Gravity | `abs(F) = G m1 m2 / r^2` | A fixed-mass, radial, attractive force sweep with at least three separations; calibrate G once, then use held-out separations |

Defining force as the same target body's `m*a` or `dp/dt` and comparing it with
that expression is not an independent second-law test. Likewise, forcing an
inverse-square interaction into initialization and observing inverse-square
output is not a derivation. Missing measurements produce `not_testable`, not pass.
A force provenance declaration is a required audit record, not automatic proof
that an instrument is independent; review its calibration and measurement method.

The first adapter requires complete saved unit-tick, unit-link lattice recordings
and unique persistent body types. It reads the existing JSON in `run.html`, not
pixels or interpolated playback. Periodic positions are unwrapped across unit
links. Missing frames, unobserved in-flight positions, repeated types, particle
creation, variable mass, field ownership and native-event recordings are explicit
blockers, never silently discarded observations. Such cases need their own readout
adapter. No inventory register is renamed mass.

Coordinates are lattice links; time is the physical `tick`, never elapsed host
seconds, playback time or local computation cycles. Momentum and mass use their
saved field scales. This is not an SI calibration or a proof that lattice link
speed equals physical light speed. Motion/force controls use window speeds no
larger than 1/10 link per tick. These checks do not establish continuum or
rotational convergence.

## Resolution and verdicts

The supplied rest test allows exactly zero position and momentum drift. Moving
inertia allows one link of positional staircase error around the initially
measured line; momentum remains exact. Its measurement window is chosen in advance
to cover complete movement periods of the reference controls. For other candidates,
resolve initial-velocity uncertainty before interpreting a failure; the current
fixed line tolerance is not a general statistical error model. A nonzero momentum
with no resolved initial displacement is `not_testable`.

The momentum/velocity test allows one link of endpoint-displacement quantization
per window, multiplied by mass/window. Each tested window and its tolerance are
reported; windows containing impulses are excluded from this constant-velocity
comparison, not from contact or conservation checks. Small displacements have weak
relative precision and do not establish a calibrated mass law.

The second-law position bound is `4*m/window^2`, from the absolute coefficients
1, 2, 1 of the three-position difference. Force signals no larger than that bound
are unresolved. The first force adapter handles constant net force only; no
force uncertainty or arbitrary-force integration model is silently assumed.
The gravity comparison uses exact radial alignment and a predeclared 1/100
relative tolerance on squared-force normalization. It does not certify mass
scaling, absolute G, extended-source geometry or a weak-field limit.

CLI exit codes: 0 all reported checks pass; 1 a measured criterion fails;
2 invalid or inconsistent output; 3 incomplete evidence or an unsupported case.
A report with any missing measurement is `partial`, even when other checks pass.
A failed run, contradictory final state, changed input fingerprint or inconsistent
recording cannot pass. The checker recomputes momentum and energy from body records;
it does not treat the runner's success/conservation flags as physical proof.

## Reproduce the first output battery

The [capture helper](../tools/capture_newton_outputs.py) runs the unchanged
[canonical collision](../examples/04-unequal-mass-collision.json) and prepares
three force-free controls by removing contact and selecting existing initial
conditions, scale and duration parameters. It writes its measurement windows before
execution and checks that simulator source and the canonical reference remain
unchanged. Capture and comparison are distinct commands/processes:

```sh
python tools/capture_newton_outputs.py artifacts/newton-measurements
python tools/newton_output_checks.py artifacts/newton-measurements/free --case inertia --window 60
python tools/newton_output_checks.py artifacts/newton-measurements/rest --case inertia --window 30
python tools/newton_output_checks.py artifacts/newton-measurements/slow --case inertia --window 1000
python tools/newton_output_checks.py artifacts/newton-measurements/collision-reference --case contact --window 120
```

These first runs should return exit 3: independent second-law and gravitational
measurements have not been supplied. Do not convert that into an all-Newton pass.
Use fresh directories; retain the source/input fingerprints and recording with
each report. Output capture requests the existing HTML generator explicitly;
ordinary simulator and software-test defaults remain headless.

## Independent force and gravity output files

The checker accepts `--force-measurements` or `--gravity-measurements` JSON paths.
These are saved measurement outputs, never runtime initialization. Each needs
`source_sha256` matching the recorded simulator and a `provenance` object with
nonempty `method`, `calibration`, and `derived_from_target_kinematics: false`.
Calibration must establish the link/tick/mass units and the measurement's
independence; a self-asserted flag does not establish either.

For force use `measurement_kind: independent_net_force`, a `target_type` matching
one recorded body, and `samples` with `tick` and a three-vector `force` at every
recorded tick. Select `--case force-response` for a driven experiment. Force is
compared with acceleration measured from output positions, not from momentum.

For gravity use `measurement_kind: gravitational_force_sweep` and `samples` with
three-vectors `separation` (source to test body) and `force` (on the test body),
and positive `source_mass` and `test_mass`. Keep masses fixed across the first
sweep. All numerical measurement values are integers or exact rational strings.
Retain the producing run/configuration identities and raw observations alongside
these derived measurement files; source-code fingerprints alone cannot establish
that the samples came from the same physical experiment.

[Checker tests](../tests/test_newton_output_checks.py) use explicitly synthetic
measurement fixtures to exercise good/bad trajectories, impulse balance, energy,
independent force, inverse-square versus inverse-distance, corruption, missing
measurements, periodic wrapping and detached read-only execution. Those fixtures
are not simulator results. Physics outcomes belong to separately recorded runs.
