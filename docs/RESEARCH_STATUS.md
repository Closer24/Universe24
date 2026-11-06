# Research status, boundaries and acceptance criteria

## Present implementation

This repository specifies a **single-board mathematical dynamical system**, with exact integer state, 48 group-labelled channels per node, fixed signed six-spatial-neighbor coupling and one Rule3 recurrence. It includes a pure executor, explicit algebraic inverse, seed/checkpoint loading, external arithmetic event readouts, and automated contract tests.

The algebraic law and the static coupling definition are reproducible. Passing tests is evidence of **implementation consistency**, not of empirical physical correctness.

## Results within the scope of this repository

| Property | Scope |
| --- | --- |
| Full-state invertibility | Exact constructive inverse, with complete state and same fixed coupling |
| Six spatial connections | One signed input per face direction, per channel, by construction |
| Finite cube covariance | Group-derived 24 proper spatial rotations with 48 double-cover channel labels |
| Three remainder classes | Algebraic `C0,C1,C2` transition classification, passive readout |
| Local balance identity | Exact arithmetic residual of Rule3 |
| Signed account `Q` | Conserved in the positive reference case on the periodic graph; may change with frustrated signed coupling |
| Clock/packet preparations | Candidate examples and research testbeds, not identified physical particles |

These results should not be conflated with claims from other prototype graphs or prior experimental variants. In particular, a previous prototype with two on-site and four spatial contacts **is not** the topology implemented here.

## Not yet demonstrated

- A physical detector click, detector readiness and irreversible-looking yet full-state-reversible records.
- A universal choice/selection rule based on a specified complexity functional.
- Self-generated, addressed cancellation signals that enforce exclusive outcomes against late competitors.
- An autonomous physical clock independent of the simulator's synchronized reference updates.
- Physical identification and exact balance of **energy**, **momentum**, **charge** and **total angular momentum**, including detector recoil and interaction contributions.
- Derivation of physical mirror/parity violation in a particular interaction. Signed/frustrated loops do not suffice.
- Photons, electromagnetic polarization, stable atoms/nuclei/electrons, spin-1/2 measurement, Bell statistics, the Born rule, Lorentz covariance, gravity or Einstein's field equations.

The ordinary double-cover labels `g,-g` represent the **same proper spatial cube rotation**, not 24 rotations plus 24 literal mirror reflections. A signed link is **not automatically a chiral interaction**.

## Explicit research tests

1. Compare fixed `[1,1,1]` and `[1,-1,1]` couplings with the same seed and measure full-state behavior, not only projected `b` patterns.
2. Search for reproducible spatially extended oscillators and wave packets with exact periods/shifts including remainders. Report dependence on boundary size `L`.
3. Propose **one readout fixed before testing** and distinguish ordinary atomic-like events from detector confirmations. Do not redefine `C2` after seeing data.
4. Implement, if possible, a spatially propagating confirmation/cancellation protocol **inside the generic state**, then test delayed signals, simultaneous candidates, ties and full inverse.
5. Define a quantitative structured-complexity functional (normalization, domain, tie rule) and test whether measured selection actually follows it; raw number of oscillators is not enough.
6. Search for physical candidate invariants with explicit local storage/flux and correct detector accounting. A mathematical `Q` is not energy.
7. Check the physical mirror transformation on both spatial positions and internal observables before claiming parity breaking.
8. Quantitatively compare with independent physical data, including null detections, timing and correlations, using one fixed protocol.

## Failure reporting

Failures are first-class results. Report the exact seed, coupling signs, cube side, full time interval, initial state, any diagnostic tolerance (normally **zero** for exact integer identities), and a counterexample when a conjecture fails.

Do not turn an externally observed event into an internal command. If a new physics hypothesis requires changing the transition law, publish it as a **clearly named variant** with a separate implementation and fresh correctness tests; do not overwrite the generic Rule3 model.
