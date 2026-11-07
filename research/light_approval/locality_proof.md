# Locality, light approval and click correlations

**Question.** Can a local Rule3 signal that approves a click, while the board continues to evolve between clicks, generate quantum entanglement?

**Scope and status.** The results below are mathematical statements about the unchanged reference engine at commit `5894510ada12d22f17a70f93a41ec311aef13265`. They apply to every permitted full integer state under their stated assumptions. They are not a derivation of physical light, quantum states or observed spacetime. A small exact enumeration checks the elementary CHSH algebra; it is not an engine experiment.

**Decision.** Light-triggered local records and correlated clicks are compatible with the model. Under a precisely separated, measurement-independent Bell experiment, however, local light approval cannot violate CHSH. A proposed mechanism that waits through many board updates can leave that separated regime, even if no click clock advances during the wait. Its physical interpretation then requires an additional account of observed locality and time.

## 1. Exact spatial dependence theorem

Let the spatial board be `V = (Z/LZ)^3`, and let `S_t(x)` denote the complete 48-channel node state, including both counters and every remainder. For representatives in `0,...,L-1`, define the toroidal Manhattan distance

`d_L(x,y) = sum_i min(|x_i-y_i|, L-|x_i-y_i|)`.

For a region `R`, let `N_t(R) = {x : d_L(x,R) <= t}`. The tensor is fixed and identical in the two evolutions being compared.

**Theorem 1.** If two complete initial states agree at every channel of every node in `N_t(R)`, their states agree on `R` after `t` updates. More generally, they agree on `N_(t-s)(R)` after each `s` updates for `0 <= s <= t`.

**Proof.** For each channel `g` at `x`, the next triple uses only its old local triple and one old `b` counter from each of the six face neighbors. The channel permutation and signs do not change those spatial distances. Thus equal complete states on `N_1(D)` give equal next states on `D`. Induct with `D = N_(t-s-1)(R)`. Integer division and nonlinearity do not affect this dependence argument. All channels read the same old snapshot, so there is no within-step cascade. This proves the result for arbitrary signed and arbitrarily large counters, for every permitted remainder, and for each of the eight fixed tensors. It requires no sampling or approximation.

Source basis: `universe24/core/engine.py:15-33,52-60`, `universe24/core/rule3.py:4-6`, and the periodic adjacency in `universe24/core/state.py:38-41`.

**Corollaries.** If two initial states differ only on spatial support `D_0`, their difference support at step `t` is contained in `N_t(D_0)`. This is an upper bound, not a claim that every possible influence actually propagates or that a recognizable signal travels at one node per step. The sparse background `(0,0,r_background)` is stationary, so support relative to that same background obeys the same bound. Remainder-only changes must be included in the support; a counter-only picture is insufficient.

**Periodic boundaries.** All separation claims must use `d_L`, not coordinate differences. A sufficient condition for an ordinary Euclidean-coordinate drawing to contain a radius-`t` causal calculation without crossing its chosen periodic seam is that the coordinate bounding box of the relevant initial support enlarged by `t` on each side lies inside `0,...,L-1`. This is sufficient, not necessary. The toroidal theorem itself needs no no-wrap assumption.

The inverse has the same radius-one dependence: reconstruct old `b` from new `a`, gather the six neighboring new `a` values, then apply the retained-remainder inverse. Its locality does not introduce a backward stage into forward evolution.

## 2. From separated readouts to local response functions

Write the complete initial preparation as `S_0(a,b,lambda)`, where `a,b in {0,1}` are two local setting labels and `lambda` contains the other trial data, including any common source, retained memory and local noise seeds. The settings may be encoded initially; no runtime intervention is required for the following mathematical comparison.

Assume all of the following:

1. Changing `a` at fixed `(b,lambda)` changes initial triples only in a declared region `U_A`; changing `b` changes them only in `U_B`. The tensor, geometry, trial pairing and readout rules are held fixed across the four setting combinations.
2. Alice's result is a deterministic function of the complete states on her declared local readout region `R_A` through a fixed horizon `T_A`. Bob uses `R_B` through `T_B`.
3. `d_L(R_A,U_B) > T_A` and `d_L(R_B,U_A) > T_B`. Thus the opposite setting lies outside each complete readout's backward cone.
4. The same preparation distribution or finite weighted ensemble `rho(lambda)` is used for all four setting combinations. In particular, `rho(lambda | a,b) = rho(lambda)`.
5. Every declared trial receives a bounded outcome. For the present check, `A,B in {-1,0,+1}`, with zero explicitly representing no qualifying click by the deadline. No context-dependent discarded trials are hidden in the denominator.

**Theorem 2.** Under these assumptions the outcomes have the form `A(a,lambda)` and `B(b,lambda)`, and the joint conditional probabilities factorize given the complete relevant `lambda`.

**Proof.** Compare the two preparations differing only in `b`. The first setting-support condition and Theorem 1 imply equality of Alice's complete local history through her horizon; her fixed local readout therefore gives the same result. The argument for Bob is identical. With deterministic response functions, conditional probabilities are indicator functions and their joint probability is their product. Probabilistic local response rules can instead be made deterministic by including their prespecified random seeds in `lambda`.

Disjoint receiver backward cones, `d_L(R_A,R_B) > T_A+T_B`, are a convenient stronger spatial condition when the settings are located at the receivers. They are not necessary for Bell locality: overlapping cones can contain an ordinary common source. Shared initial data can correlate separated outputs without enabling remote-setting dependence.

For the prospective paired-receiver experiment proposed by the computation agent, `L=97`, receiver coordinates `(32,24,48)` and `(32,72,48)`, and `T_A=T_B=16` give toroidal distance `48 > 32`. Receiver-only setting changes also satisfy `48 > 16`. This verifies the geometric conditions, not the behavior of any particular preparation. The actual support, local-setting difference and full output histories still require the computational audit.

## 3. All-trial CHSH bound, including absent clicks

Define `E_ab = sum_lambda rho(lambda) A(a,lambda) B(b,lambda)` and

`S = |E_00 + E_01 + E_10 - E_11|`.

For a fixed `lambda`, abbreviate the four responses as `A_0,A_1,B_0,B_1`. Since every response lies in `[-1,1]`,

`|A_0(B_0+B_1) + A_1(B_0-B_1)|`

`<= |B_0+B_1| + |B_0-B_1|`

`= 2 max(|B_0|,|B_1|) <= 2`.

Averaging with the same nonnegative normalized weights and using the triangle inequality proves `S <= 2`. This is a proof for every such response model. It applies to no-click `0` outcomes without a fair-sampling assumption. A prespecified assignment of no-clicks to one binary value also remains bounded; changing the normalization by dropping trials is a different statistic.

**Exact finite algebra check.** Exhaustive Python enumeration of all `2^4=16` binary response tables gave eight tables with CHSH expression `-2` and eight with `+2`. Enumeration of all `3^4=81` ternary tables gave counts `{ -2:16, -1:8, 0:33, 1:8, 2:16 }`. Maximum absolute value was exactly `2` in each case. The enumeration is a sanity check on the proof, not empirical evidence of physical correlations.

## 4. First clicks, event-ready approval and selection

Selecting the first qualifying local click within a fixed horizon is still a local function of a bounded history. If none occurs, its output must be recorded as the declared no-click value. A frozen local stopping rule with no fixed upper bound remains a local functional of its accessible history, but the finite-cone separation test above no longer applies without a bound on its stopping time.

Conditioning on both detectors eventually clicking generally changes the sampled hidden-variable distribution to `rho(lambda | a,b,accepted)`. Likewise, pairing events after the run by a setting-dependent coincidence window can compare different subsets in different settings. The all-trial CHSH proof cannot be applied to four correlations formed from four different selected ensembles. This can create an apparent violation with entirely local deterministic response tables; it is not a proof of quantum entanglement.

A valid heralded/event-ready trial is different. A sufficient condition is an acceptance indicator `H` for which `rho(lambda | a,b,H=1) = rho(lambda | H=1)`, together with local response functions in that accepted ensemble. The same proof then gives `S_H <= 2`. A herald established before fresh independent setting choices is a useful sufficient arrangement, not a necessary absolute time ordering. A herald spacelike separated from the setting choices can also meet the independence condition. Actual causal geometry and statistical independence must be checked rather than inferred from the word "approval".

If approval is a signal that carries information about both settings to the outcomes, the separated-response premise may fail. That is causal communication in the board, not a counterexample to Theorem 2. If a global read-only observer chooses which clicks to retain using both outcomes or settings, that is an analysis selection rule, not a detector mechanism implemented by Rule3.

## 5. Why zero click-time does not settle the causal question

Define a candidate local click clock by `tau_A(t) = number of selected A clicks through board step t`. It can remain constant during many board updates. During those updates, signals and ordinary state changes can still propagate within the expanding board cone. A small or zero difference in `tau_A` is therefore not evidence that two events were separated in the board's causal geometry.

In particular, a detector may wait for a message from another apparatus and still register only one eventual click. To test whether this reproduces quantum experiments, the model must independently derive how click-clock readings, spatial distances, measurement-setting events and communication speed correspond to observable spacetime. It must then reproduce the relevant correlations and no-signalling constraints in that operational description. Merely suppressing clock ticks does not establish that correspondence.

Conversely, a board-locality proof alone is not a universal proof against every possible emergent spacetime interpretation. If the model's board causal order differs from measured locality, that relation is an additional physical hypothesis requiring quantitative tests. One must state exactly which Bell premise the proposed interpretation changes. An unexplained mapping cannot serve as evidence that the mechanism succeeds.

## 6. What can be investigated without altering Rule3

| Candidate interpretation | What can be studied now | Decisive requirement or limit |
| --- | --- | --- |
| Prepared common-source correlation | Shared source variables, two separated receiver records, source-absent controls | Correlated clicks alone do not demonstrate entanglement; full-trial CHSH obeys the bound under the stated assumptions |
| Signal-triggered local record | Arrival-conditioned record creation and finite persistence using ordinary counters/remainders | Show the internal record, its lifetime and full-state inversion; an external first-click log is not itself that record |
| Event-ready light approval | Define accepted trials through an internally produced herald and test independent local settings | Check independence of the accepted ensemble, then retain no-click outcomes within it |
| Delayed common approval | Let local signals reach a common region and return to detector regions before their clicks | Explicit board communication and delay must be included; this is not a board-separated Bell test |
| Setting-dependent preparation ensemble | Declare a different relation between hidden preparation and settings | This changes measurement independence, an additional physical assumption; post-hoc seed fitting is not a prediction |
| Emergent observed locality | Derive operational clock and distance measurements from records | Demonstrate their mapping, no-signalling and quantum statistics; hiding board elapsed time does not suffice |

The proof does not establish that every quantum-entangled state must violate CHSH. It excludes the claimed Bell-nonlocal statistics only under the listed assumptions. A positive claim of entanglement also needs an explicit operational correspondence to quantum states and measurements, or another justified entanglement witness. The current record-approval concept has not supplied that derivation.

**Next decisive test.** First verify the full-trial, fixed-horizon paired-receiver protocol and all remote-setting counterfactuals. If a conditioned statistic exceeds its all-trial bound, identify the accepted subensembles exactly before interpreting it. If the mechanism requires long waits, measure the board-causal paths and derive the proposed observed-time mapping as a separate research claim.
