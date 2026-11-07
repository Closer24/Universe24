# Physics gates and a falsifiable cooperation hypothesis

Status: prospective research protocol, 2026-11-07. No experiment in this file has been run. Base implementation: `ed1556e202eb0f3cc60342c75d44012c2eeb71c3`. This protocol adds no forward operation. Every counterfactual below is a separate initial preparation evolved by the unchanged Rule3; none is an intervention during a run.

## Common acceptance contract

Fix the coupling signs, complete seed generator, parameter ranges, readout, regions, trial window, thresholds and exclusions in a versioned JSON protocol before validation. Use separate discovery and validation seed sets. A failed search means failure within its enumerated domain, not impossibility. Exact identities have zero tolerance. Approximation errors have explicit norms, horizons and held-out domains. Report every trial, including no arrival, no record and numerical/resource failure. A result outside the registered domain is exploratory.

Maintain four ledgers: mathematical proofs; finite computational observations; hypotheses; future targets. A physics gate needs operational click predictions in addition to board diagnostics. Full-state inversion and local accounting are prerequisites, not empirical validation. The arithmetic observer `C0/C1/C2` is not itself a detector or a selection law.

## G0: propagation, interactions and effective laws

For two preparations equal outside region S, prove by induction that their states agree outside the graph-distance-t neighborhood of S after t updates. The six-neighbor graph therefore gives an exact microscopic influence bound. For a periodic cube, use shortest torus distance; for an infinite-space interpretation require a causal neighborhood that does not wrap. This does not establish an isotropic physical light cone.

Predefine a receiver record predicate and measure arrival time against local clock phase as well as simulator update number. Compare axes, face diagonals, body diagonals and at least six generic rational directions; report first influence, first record and packet centroid separately. Finite cube covariance does not imply continuous rotational symmetry. A fit to long-wavelength motion does not remove anisotropy of the earliest causal front.

An effective law must specify an observation map O, state domain D, evolution F, horizon H and error norm. For example, validate `max(t<=H) ||O(W^t X)-F^t(O(X))|| <= epsilon` for held-out X, and report the worst case, not just the average. Use detector-event timing and output errors alongside field errors. Compare at least two simpler alternatives, such as constant velocity and a dispersive linear recurrence. Fit once on discovery data; freeze coefficients for validation.

For an exact effective coefficient alpha=num/den, require an injective encoding E_alpha, a declared spatial correspondence and fixed positive integer m with `W_1,1^m E_alpha(X)=E_alpha W_alpha(X)` for every X in the stated family, plus invariance of the encoded domain. Preserve all remainder information. A finite table verifies only that table. A homogeneous oscillator family does not establish a spatial field family; a matching frequency establishes neither. An approximate encoding needs a quantified residual and accumulated-error bound.

## G1–G4: separate physical targets

| Gate | Required operational evidence | Rejection or limitation |
| --- | --- | --- |
| G1 light | Reproducible mobile modes, receiver clicks, direction-dependent speed/dispersion and attenuation curves; two independently controllable polarization preparations with a fixed analyzer response; local clock calibration shared across directions | Speed alone is insufficient. Fail a claimed regime when directional, frequency or amplitude errors exceed its registered tolerance; report narrower domains honestly. Lorentz/observer comparisons remain a further obligation. |
| G2 matter | Localized persistent structure, reproducible response to momentum-carrying preparations, two-body interactions and detector recoil accounted by independently justified balances; internal transition frequencies predicting held-out click spectra | A periodic pattern or spinor label alone does not identify mass, spin or a particle. Dispersal, dependence on wraparound, or failure under the stated perturbations falsifies the claimed component domain. |
| G3 quantum measurement | An internal record-writing apparatus, exhaustive outcome probabilities including no detection, repeatability, interference with a fixed phase-to-click map, calibrated Born-rule targets and the Bell audit below | One retained record, cancellation, or reversible information spreading is not quantum collapse. Conditioning away failures cannot establish exclusivity or quantum statistics. |
| G4 gravity | Operational distance/time from exchanges between internal apparatuses; a declared effective metric; common free-fall and clock-rate predictions across different prepared bodies; independently identified source accounts; quantitative weak-field and eventually dynamical tests | Tensor notation is insufficient. No gravity claim before metric, source and observable correspondence are specified. A fitted attractive trajectory cannot alone establish equivalence or Einstein dynamics. |

These are research gates, not claims that the target phenomena occur. Numerical accuracy targets for comparison to physical experiments must be chosen from a named dataset and its uncertainty before that experiment begins; no physical fit is performed here.

## Early Bell obstruction audit

For binary outcomes A(x,lambda), B(y,lambda), local dependence and one setting-independent distribution rho(lambda) imply `|E00+E01+E10-E11|<=2`: for each lambda, `A0(B0+B1)+A1(B0-B1)` is +2 or -2, and averaging preserves the bound. This is an analytic obstruction, not a simulation challenge. Determinism alone neither establishes nor invalidates setting independence.

Before seeking a violation, specify how operationally separated setting choices and records map to lattice events. Check whether a lattice path can connect a remote setting to an outcome before its registration. Disclose setting-source correlations, communication, postselection and trial pairing. Record no detections under a fixed exhaustive protocol; use a justified inequality or a prespecified binary assignment without dropping trials. Test no-signalling separately. An apparent violation must first trigger an assumption and implementation audit; it cannot refute the proven bound under its premises.

Background: [Preskill, Quantum Entanglement, sections 4.3.1–4.3.2 and 4.3.6](https://www.preskill.caltech.edu/ph229/notes/chap4_01.pdf); original [CHSH (1969)](https://doi.org/10.1103/PhysRevLett.23.880). This project-specific obstruction follows from the displayed algebra, not from an empirical result for Universe24.

## A measurable cooperation statistic

Use **nonadditive joint response**, not an unspecified universal complexity. Fix two disjoint preparation regions A and B, a receiver region R, a time window I, and four valid initial states X00, X10, X01, X11. X10 adds the A preparation, X01 adds B, and X11 adds both to X00; this is initial-state construction only. All four use the same fixed coupling and exact engine. Any remainder preparation must lie in 0..5; do not introduce an unrecorded modulo convention.

Flatten the complete triples in R into an integer vector Yij(t). Set `Dij=Yij-Y00` and `J=D11-D10-D01`. Define

`C_R,I = sum(t in I)||J(t)||_1 / [sum(t in I)(||D11(t)||_1+||D10(t)||_1+||D01(t)||_1)]`,

with C=0 when the denominator is zero. The triangle inequality gives 0<=C<=1. It detects failure of additive superposition in the declared apparatus and window; it is not causal integration, semantic complexity, computational universality or thermodynamic entropy. Quotient thresholds alone can produce C>0. Report the denominator and unnormalized numerator to expose tiny-response artifacts. Remainder coordinates have their fixed integer representation; the score is representation dependent.

Report separately: exact period/translation tests on the full state (order/periodicity); click-symbol entropy estimated across the registered preparation ensemble with a declared estimator (statistical diversity); and C (joint response). These quantities must not be substituted for one another. Time-scrambled and phase-scrambled controls are generated before a run or applied to passive analysis records, never written into an evolving state.

## Test H16 without an external selector

H16-C is a restricted prediction: a two-receiver preparation with a higher independently measured C on one branch produces an exclusive persistent record on that branch more often than a matched lower-C branch. It is not yet a claim about preference for all future histories. A complete seed has exactly one trajectory; probabilities here concern a declared ensemble of seeds.

First characterize isolated branch preparations with the four-run assay, freeze their C values, and match baseline click rate, response size, path length and memory lifetime as closely as possible. Freeze a non-overlapping validation ensemble of 256 seeds and its permutation/mirror controls. Predict a high-C selection fraction >=0.65, a two-sided exact 95% binomial interval excluding 0.5, and the same directional effect after swapping branch locations. Treat nonexclusive/no-record outcomes as failures of the selection prediction in the primary 256-trial denominator; report a conditional fraction only as secondary. Require the effect to survive controls matched on baseline activity and response size. Failure to construct matched branches blocks this test rather than licensing a new metric.

Alternative explanations are geometric path advantage, threshold sensitivity, activity magnitude and seed bias. Run lower/higher-C branches in both positions, equal-C branch pairs, and phase-scrambled initial preparations with matched register-value inventories. Preregister one primary score/window; additional scores are exploratory. Neither C nor any ranking enters Rule3.

When a projected path vanishes, compare the two full states including remainders and apparatus. Display where their difference resides, then invert both trajectories to recover their distinct preparations. A bijection cannot map distinct complete states to one complete state. A projection may map them to the same observed record; that alone is not physical collapse.

## Bounded work packages and decisions

Budgets below are prospective full-package ceilings, not current authorizations to run them. The 600-CPU-second pilot ceilings in PROJECT_PLAN.md apply first; a recorded decision is needed to launch the larger package. Stop at the first limit and exclude already completed baseline audits. A channel update means one Rule3 application; count the four-run cooperation assay and controls against the total. Do not silently enlarge a budget or relabel an exhausted search as a mathematical impossibility.

| ID / owner | One question and deliverable | Budget | Success / failure / continue |
| --- | --- | --- | --- |
| PG0 / algebra | Does the candidate imply the graph-cone and Bell conditional bounds? Proof note with premises and counterexample checks | 2 reviewer-hours; <=10^6 channel updates | Success: checked proofs and explicit operational map obligations. Failure: a concrete invalid step. Continue to numerical claims only after correction. |
| PG1 / physics | Is a prepared signal's measured transport described by one frozen effective law? Protocol, traces and error table | <=10^8 channel updates or 2 CPU-hours | Success: all held-out cases satisfy registered error (initial engineering target: <=5% arrival-time error with a one-tick floor) and no hidden wraparound. Failure: a violating case. Continue by narrowing a declared domain or collecting a genuinely new model. |
| PG2 / algebra | Does one proposed alpha encoding close under Rule3? Encoding, inverse and identity proof or counterexample | 4 reviewer-hours; <=10^7 channel updates | Success: all-state proof on a named family. Failure: closure/injectivity counterexample. Continue only with a separate restricted family; finite checks remain finite. |
| PG3 / search | Do matched branch motifs with different C exist? Complete preparations and four-run scores | <=10^8 channel updates or 2 CPU-hours | Success: frozen motifs satisfy matching tolerances fixed before search. Failure: domain exhausted or matching fails. Continue H16 only if comparability is established. |
| PG4 / physics | Does H16-C predict independent selection trials? 256-seed primary result and matched controls | <=3*10^8 channel updates or 4 CPU-hours | Success: all stated statistical and control criteria. Failure: any primary criterion fails. Continue replication, never alter scoring retrospectively. |
| PG5 / independent review | Can another implementation/reader reproduce one claimed gate result? Reproduction report and discrepancies | 2 reviewer-hours; <=10^8 channel updates | Success: exact full-state agreement and identical decisions. Failure: mismatch with minimal counterexample. Continue only after resolving it. |

G2–G4 remain blocked until an internal signal–clock–memory apparatus and relevant operational correspondences pass their own gates. This prevents expenditure on fitting physical names to unvalidated arithmetic behavior. A structural escape from a proved obstruction must receive a new candidate identifier, preserved predecessor, explicit minimal change and fresh inversion/locality tests.

## Source map

- Repository contract: `AGENTS.md`, `docs/MODEL.md`, `docs/OBSERVATION.md`, `docs/RESEARCH_STATUS.md`, at the pinned base revision.
- Research document: [Universe24 research proposal](https://docs.google.com/document/d/1NDPfeFj9vldgb0RMSSvx2lBSmOo__E-F3t2cZwfjOjI), H1a, H6–H9, H15–H17, Section 6 and A11. The protocol above is a new proposal, not an already established result from that document.
