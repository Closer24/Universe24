# Universe24 — scientific research proposal (concise guide)

**Research question:** *Could reality be built from integers?*

**Project initiator:** Alon Gonen  
**Full, evolving proposal:** [Universe24 — Could a Simple Automaton Be the Logic Behind Nature?](https://docs.google.com/document/d/1NDPfeFj9vldgb0RMSSvx2lBSmOo__E-F3t2cZwfjOjI/edit?usp=drivesdk)  
**Reference implementation:** [Universe24 on GitHub](https://github.com/Closer24/Universe24)  
**Summary alignment:** baseline summary from 6 November 2026; the existing H16 discussion and methodological framing were checked against the Google Doc on 7 November 2026. This is a readable orientation, not an independent revised theory or an exact copy of every appendix.

> **Status:** This is a research proposal. The proposed integer automaton has a precise, testable mathematical implementation, but it has **not** been shown to reproduce the established laws of physics. The Google Doc is the primary evolving proposal; this summary is a guide for new readers. Access to the Google Doc is controlled by its owner.

## 1. The central idea

Universe24 asks whether diverse physical phenomena could emerge from **a single elementary local mechanism operating on exactly stored integers**. Instead of prescribing distinct microscopic algorithms for photons, electrons, atoms, clocks and detectors, the project proposes examining whether different **collective patterns of the same underlying dynamics** could account for them.

The intended distinction is between **underlying board states** (the complete integer dynamics) and **observed clicks** (declared, experimentally interpretable records of interactions). A click is not necessarily an oscillator tick or an arithmetic carry. It would become a physical detector outcome only after deriving a detector mechanism and comparing it quantitatively with measurements.

Universe24 combines science with the philosophy of science. Its methodological position is that the central question requires both: conceptual analysis clarifies what counts as a physical explanation, a clock, a measurement and a recorded outcome; mathematical derivation, reproducible computation and comparison with physical observations test the proposed account. The idea that nature favors greater joint structured complexity is a guiding philosophical conjecture to formulate and test, not an established law or a proven consequence of Rule3.

The research method works in both directions: derive constraints from existing physical experiments, then run a fixed candidate model and test its measurable predictions. A visual resemblance or an internally conserved number is insufficient.

## 2. Three levels that must not be confused

| Level | What it means | Current status |
| --- | --- | --- |
| **Foundational proposal** | Common local law, discreteness, exact arithmetic, locality, reversibility, causal structure, observable readouts and physical accounting (P1–P10 in the Google Doc) | Research postulates, not demonstrated properties of nature |
| **One mathematical candidate** | A periodic cube, one 48-channel board per site, fixed 2O-derived signed coupling and Rule3 as the sole updater | Specified and implemented as an exact computer model |
| **Physical interpretation** | Emergent clocks, propagation identified as light, stable particles, detector measurement, quantum statistics and relativistic geometry | Mostly open tests; not implied by the algebra alone |

Historical **Clockwork G** and **H9a** are distinct comparison constructions described in the proposal. They are not secretly executed by the present Rule3 engine.

## 3. The current single-board algebra

The computational space is a closed periodic cube of side `L >= 3`, with one identical node per site. Each node has **48 channels** indexed by the binary octahedral group `2O`, the double cover of the **24 proper cube rotations**. The two lifts `g` and `-g` are **not** rotation versus mirror reflection.

At each address `(x,g)`, store the complete triple `(a,b,r)` with `a,b` arbitrary-precision signed integers and `r in {0,...,5}`. Thus there are **96 integer counters and 48 remainders per spatial site**.

Every channel receives one input from each of **six distinct spatial neighbors** `(+x,-x,+y,-y,+z,-z)`; there are no within-site connections or second board. One group-based connection function picks the sender channel and a fixed sign. Its tensor `P(d,g,h) in {-1,0,+1}` is represented by **three signed 48×48 matrices and their transposes**. The sign triple is fixed before each run; it is not an evolving gate.

Let `u(x,g)` be the sum of the six signed current-counter inputs. The **only forward update** is:

```text
(ell, r_next) = divmod(2*u(x,g) + r(x,g), 6)
a_next        = b(x,g)
b_next        = ell - a(x,g)
```

All channels read one old snapshot. The retained remainder permits exact full-state inversion. Under the original all-positive signs, the graph and an algebraic signed-total account have special properties; with negative weights the same total is **not generally conserved**. Neither account has been established as physical energy.

For exact tensor definitions and mathematical qualifications, see [MODEL.md](MODEL.md). For immutable execution and read-only observation, see [ARCHITECTURE.md](ARCHITECTURE.md).

## 4. The merged ideas

The present proposal makes three structural unifications:

**Channels and couplings share one algebra.** The 48 channel labels and the fixed signed routing tensor arise from the same `2O` construction; three matrix slices are representations of one connection rule, not three arbitrary independent physical laws.

**Distinct functional roles share one board.** Previous/current counters are two time levels of one recurrence, not separately evolving boards. Different periods, phases, return signals and memory motifs may *functionally* serve different roles, but no general equivalence to two independent boards has been demonstrated.

**All physical effects must arise from one dynamics.** Rule3 is not supplemented by a dedicated clock, atom, detector, history-selection or cancellation operation. Readouts are external; a hypothetical effective veto or record must arise as an ordinary state pattern.

## 5. Proposed clicks and the unresolved selection problem

Write `r = 2*theta + epsilon`, with `theta in {0,1,2}` and invariant parity `epsilon in {0,1}`. Rule3 implies `theta_next = (theta + u) mod 3`. The reference observer labels some completed transitions `C0, C1, C2` by their shift `u mod 3`; it records an event only with nonzero quotient and an actual change to the full local triple.

These labels are **three arithmetic classes**, not three independently derived physical click species. `C2` does **not** inherently choose a winner. The source document proposes testing whether interactions with a prepared detector could create robust records and prevent later competing confirmations while preserving complete-state reversibility. No general robust mechanism has been established in this repository.

The document already contains **H16**, a candidate explanatory postulate: observed joint click histories might be the records of admissible full joint histories that maximize a pre-specified measure of *joint structured complexity*. This is a research hypothesis about possible observed behavior, not an established law or an additional engine instruction. Complexity must be defined explicitly and distinguished from entropy, disorder, periodicity and mere component count.

A finite test must register the metric, alternative routes or histories, causal comparison domain, observation window, detector/click definition, controls and tie policy before inspecting its outcomes. One testable version predicts that a uniquely largest calibrated score yields the sole observed outlet confirmation among eligible, matched alternatives. Ties and cases with no unique maximum must follow the registered policy. This conditional finite prediction does not claim a universal success rate or an instantaneous comparison of inaccessible parts of the board.

A completely specified initial state and fixed tensor have one deterministic trajectory. The metric is a read-only observable; it cannot choose the next state, change couplings during a run, delete a path or erase recorded events. Any effective competition must emerge from ordinary local Rule3 evolution. Apparent disappearance at an outlet must be reconciled with information retained in the complete invertible state, including the counters, remainders and environment. The [causal and recurrence constraints](SIGNAL_CLOCK_COMPLEXITY.md#exact-constraints-and-counterexamples) limit possible interpretations of a universal maximum or growth principle.

The registered `C_pair` test supplied **10 eligible arrival-matched comparisons, zero higher-score-only outcomes and 10 counterexamples**: six favored the lower-score route and four left both outlets quiet. This refutes that defined finite-family prediction. It does not establish that every possible structured-complexity measure fails, and changing the metric later cannot turn the original result into a success. The [protocol, result and limits](PATH_SELECTION_BLOCK.md#registered-selection-study) remain unchanged; a different metric requires a new prospective study.

The source's existing H16c/H16d discussion and its effective-collapse research target connect the idea to entanglement, detector clicks, interference and probabilities. That **quantum connection is an additional conjecture**, not a deduction from the maximum criterion or from the three arithmetic C classes. It requires a derived preparation/recording mechanism and quantitative tests of interference, Born probabilities, Bell/CHSH assumptions and no-signalling. A canceled signal or a single outlet record is not by itself quantum collapse. These physical tests remain open.

## 6. How the project would be tested against physics

The long-term goals in the proposal include:

- **Propagation and clocks:** robust propagating modes, local operational time, direction and observer comparisons, and eventually the measured properties of light including polarization.
- **Stable matter:** dynamically persistent particle-like structures; nuclear and electron properties and atomic spectra.
- **Quantum experiments:** phase-sensitive interference, entanglement correlations, Born-rule probabilities, Bell/CHSH consistency and no-signalling, including no-detection outcomes.
- **Physical conservation:** independently justified energy, momentum, charge and total angular-momentum accounts, including apparatus and detector recoil.
- **Spacetime and gravity:** effective metric, equivalence principle and quantitative general-relativistic benchmarks.
- **History and complexity hypotheses:** explicit experiments for record persistence, delayed cancellations and complexity measures, separately from ordinary entropy.

These are **targets to be derived and validated**, not outcomes reported as achieved.

## 7. What the repository currently provides

This GitHub repository implements the mathematical **reference candidate**, not the full research programme: exact group construction, fixed signed coupling, generic Rule3 execution, complete-state inverse/audits, data-only seeds, checkpoints and passive arithmetic event readouts.

The source proposal describes earlier **prepared** reference clocks and records. Their behavior depends on specific seeds and usually the positive-sign coupling; it cannot be transferred without testing to all signed tensors, all boundaries or physically interpreted detectors.

To reproduce a run, record the **Git commit SHA, side `L`, fixed signs, complete seed/background, step count, readout definition and measured diagnostics**. Keep positive and negative results, and do not redefine event labels to fit an output.

## 8. How to read and contribute

1. Start with the [main README](../README.md) for the model and commands.
2. Read the [full scientific proposal](https://docs.google.com/document/d/1NDPfeFj9vldgb0RMSSvx2lBSmOo__E-F3t2cZwfjOjI/edit?usp=drivesdk) for detailed postulates P1–P10, hypotheses H1–H17, objectives, mathematical appendix and sources.
3. Check [MODEL.md](MODEL.md), [OBSERVATION.md](OBSERVATION.md) and [RESEARCH_STATUS.md](RESEARCH_STATUS.md) before drawing scientific conclusions.
4. Run the [Quickstart](QUICKSTART.md), then read [AGENTS.md](../AGENTS.md) before editing any implementation.

**Credit:** Alon Gonen, *Universe24*. See [CITATION.cff](../CITATION.cff) for the repository citation. A research statement about the proposal and a software citation should not be mistaken for empirical validation.

**Access note:** The Google Doc may require document sharing permissions.
