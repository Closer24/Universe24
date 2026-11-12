# Quantum handoff for the one-system geodesic board

## Result and scope

The geodesic board can display metric-derived trajectories from one retained
run without thereby implementing quantum mechanics. This review adds a passive
complete-trial validator and executable counterexamples; it does not add a second
runtime, quantum sampler, or retained channel. Its exact arithmetic uses Python
integers and `Fraction`. `python -m validation.geodesic_board.quantum_audit`
writes fresh evidence under `runs/geodesic_board/quantum.json`.

The checked upstream handoff is [PR #49 at a3013a9](https://github.com/Closer24/Universe24/pull/49):
44 carrier channels plus four one-way observer records. That report explicitly
states that 9:1 intensity produces 36:36 binary events and 36 double outcomes,
despite 324:36 quotient weights; it has no Engine Bell apparatus. These are
published upstream findings, not re-executed #49 results in this audit.
The corrected full-frame proposal is 45 channels, so appending those four
recorders would require 49. A shared field name cannot establish a compatible
coupling or justify reusing the old 44-channel decoder.

## Exact obstruction, with assumptions stated

If each trial has a common hidden preparation `lambda`, local responses
`A(x,lambda), B(y,lambda)` in [-1,1], and the **same distribution of lambda for
each independently chosen setting pair**, then

\[
|A_0(B_0+B_1)+A_1(B_0-B_1)|\le 2,
\qquad |E_{00}+E_{01}+E_{10}-E_{11}|\le2.
\]

For a reversible deterministic local board, lambda can include all relevant
initial retained state and apparatus history. Local coarse-grained clicks remain
functions of that state. An information-losing passive decoder alone does not
remove the bound. This conclusion requires that the remote setting cannot enter
the local outcome's causal past before the measurement and that preparation is
setting-independent; strict face support alone does not establish the physical
spacetime arrangement or statistical independence.

The audit enumerates all 81 local response vertices in {-1,0,1}^4 (0 represents
no detection), attaining maximum absolute CHSH 2. Convex common weights preserve
the bound. It also constructs a strictly local acceptance example with
coincidence-selected S=4 but complete-emission S=1. Selection changes the hidden
ensemble for each setting. Neither S=4 nor a selected C2 stream is evidence of
quantum nonlocality in that control.

This is an exact ensemble/algebra result. A finite empirical CHSH estimate can
exceed 2 through sampling fluctuation even for a local model. The validator
reports no p-value and cannot establish a statistically significant Bell test.
For a real trial sequence, predeclare the setting schedule/generator, stopping
rule and memory-robust statistical analysis. The emission manifest must exist
before outcomes, include no detections, and have source/run/window provenance.

## Why reversibility is not enough

There is a useful exact mathematical embedding: a reversible map F on a
countable state set defines a permutation unitary on the formal basis,
`U|s> = |F(s)>`. But a single classical seed stays a single basis state. A
classical mixture plus diagonal coarse-grained measurements reproduces classical
probability, not interference of amplitudes or a nonclassical Bell correlation.
Choosing coherent superpositions, noncommuting measurement operators and a Born
measure supplies additional physical structure. It is not derived by naming the
integer inverse map “unitary.” This embedding is an algebra observation here,
not a proposed additional runtime or an inherited QCA theorem.

Likewise, classical complex waves can interfere. The equality of a detector's
quotient with intensity is weaker than exclusive outcomes with the normalized
Born frequency. Reversible detector memory, source feedback and an appropriate
state/observable algebra still require construction. A quantum-cellular-automaton
approach can be local without contradicting Bell: it has a quantum state algebra
and entanglement, not the factorized local hidden-variable response assumptions
above. Such a change would require a separate derivation and a complete retained
representation/locality/cost ledger; it is not implemented by this patch.

## Concrete next handoff

| Required connection | Falsifying acceptance test | Current status |
| --- | --- | --- |
| One source, phase transport and apparatus on the same corrected tensor | Intervention changes actual retained apparatus records, with strict face causality and full rewind | Not implemented here |
| Apparatus interaction and source stress in the joint <=48 ledger | Degree <=3 including interaction energy and all feedback; no discarded pointer branch | Open; #49 quartic pointer source fails |
| One exclusive outcome or explicit no-detection for every emission | Predeclared two-port protocol; reject doubles; amplitude and phase held-out controls | #49 reported failure retained |
| Born response from actual detector trials | Frequencies versus normalized intensities with uncertainty and fixed calibration; no quotient weighting substituted for trials | Not established |
| Bell assumptions and physical separation | Source/settings provenance, remote-setting interventions, same-metric spacelike separation and complete trials | No Engine Bell apparatus |
| Quantum state/observable interpretation | Derive the necessary nonclassical operational structure, or explicitly state which Bell assumption a proposal changes | Unresolved theoretical choice |

The immediate useful implementation target is a **physically accounted detector
interaction within the existing three spare slots**, then a complete-trial
two-port measurement protocol. A quadratic interaction/source is worth testing
before another quartic bistable pointer. This is a research direction, not an
existence claim or a promise to evade Bell's theorem. The same-run geodesic
renderer can supply separation diagnostics when its geometry is valid; it cannot
certify an independent clock or quantum measurement merely by plotting a path.

## Executable interface

`complete_trial_summary(trials, manifest)` accepts immutable `Trial` records with
ID, two settings and each side's tuple of signed detection outcomes. It rejects
missing, duplicate, unknown and setting-inconsistent trials and noninteger
outcomes. Empty tuples remain explicit no detections and receive outcome 0.
Multiple outcomes at either side invalidate the exclusive-outcome contract and
suppress CHSH rather than silently choosing a winner. All four setting pairs
must have emitted trials. The report uses exact rational correlations and keeps
causal provenance, measurement independence and statistical significance marked
as requiring separate evidence.

`audit()` returns a JSON-compatible report suitable for the common board report.
All its fixtures are labelled protocol/algebra controls, not Engine runs. The
physical-gate section remains open even when the validator's software controls
pass. No hidden retained-state reads or update callbacks occur.

## Primary sources consulted

1. J. S. Bell, *On the Einstein Podolsky Rosen paradox* (1964),
   [doi:10.1103/PhysicsPhysiqueFizika.1.195](https://doi.org/10.1103/PhysicsPhysiqueFizika.1.195).
   Establishes the incompatibility between the specified local hidden-variable
   account and all quantum predictions; it does not imply that locality alone
   excludes quantum field theory.
2. J. F. Clauser, M. A. Horne, A. Shimony and R. A. Holt, *Proposed Experiment to
   Test Local Hidden-Variable Theories* (1969),
   [doi:10.1103/PhysRevLett.23.880](https://doi.org/10.1103/PhysRevLett.23.880).
   Basis for the CHSH correlation test used above. The algebraic inequality is
   reproduced explicitly rather than inferred from an empirical score.
3. P. Arrighi, V. Nesme and R. Werner, *Unitarity plus causality implies
   localizability*, [arXiv:0711.3975v3](https://arxiv.org/abs/0711.3975v3).
   Starts with unitary quantum dynamics and bounded-speed causality to derive a
   local circuit representation. It does not derive quantum amplitudes or the
   Born rule from a classical reversible integer seed.
4. B. Hensen et al., *Experimental loophole-free violation of a Bell inequality
   using entangled electron spins separated by 1.3 km* (2015),
   [arXiv:1508.05949](https://arxiv.org/abs/1508.05949).
   Illustrates event-ready trial definition, detection/locality controls and
   an explicit finite-sample hypothesis test. These requirements motivate the
   provenance and significance gates; their experimental conclusion is not
   borrowed as evidence for Universe24.
