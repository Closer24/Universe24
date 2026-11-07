# Cooperation, routing and event time

This note defines a testable cooperation measure and separates an observed
click sequence from the reversible board dynamics. It does not assert that
Rule3 prefers a high score or that the propagated signal is physical light.
The experiment protocol must freeze its addresses, times, preparations and
readouts before evaluating a routing claim.

## A bounded cooperation measure

Use an assembly with a fixed list of `m >= 2` internal memory addresses.
For each address `i`, define the initial-preparation perturbation `P_i` to
replace `r_i` by `(r_i + 2) mod 6`, leaving its counters and every other
component unchanged. These perturbations preserve remainder parity. They are
separate preparations at board step zero, never interventions during a run.
All preparations use the same fixed coupling and geometry.

Choose a calibration input preparation, a fixed set of outlet sites and a
fixed finite observation window. Let `Y(S)` be the ordered vector of **all
48 signed b counters** at those outlet sites and times, obtained by evolving
the complete preparation `S`. The order of the coordinates is fixed and no
amplitude threshold or selected visible channel enters this definition.

For each pair of distinct memory addresses define the mixed response

```text
D_ij = Y(P_i P_j S) - Y(P_i S) - Y(P_j S) + Y(S)
K(S) = number of pairs with D_ij != 0 / binomial(m, 2).
```

The vector subtraction uses exact integers. Thus `0 <= K <= 1`. The operator
order is immaterial because the two perturbations affect distinct addresses.
`K` measures pairwise non-additivity of causal response in this declared
experiment. It is not a general measure of algorithmic complexity, entropy,
disorder, regularity, period length, energy or physical cooperation.

Computing `K` needs `1 + m + m*(m-1)/2` separate calibration trajectories.
For `m=4` this is eleven runs. Calibration data, the exact perturbation list,
outlet vector and resulting score must be retained. An unchanged output can
mean either weak response or a blind observation window; that ambiguity is
not removed by giving it a low score.

There is no score in the evolution engine. The score only compares trajectories
after their preparations are fixed. The experimental preference hypothesis
would be: under **new held-out input preparations**, the outlet belonging to
the branch with greater calibration `K` more often receives the transmitted
signal according to a separate fixed routing criterion.

## Matched routing tests

The metric alone does not specify a receiver or a successful transmission.
The physics protocol must state the packet or outgoing-counter criterion
before search. A proposed comparison should include the following controls:

* The two candidate branches have the same path length, spatial geometry,
  number of prepared sites, fixed tensor and observation horizon. Initial
  counter amplitude and launch timing are the same. Only the declared memory
  preparations differ.
* The labels “higher K” and “lower K” are assigned from fixed calibration
  probes before the held-out joint-routing probes are evaluated. The same
  probes cannot both define the preferred branch and supply the claimed test.
* Swap the two memory preparations between the same physical branches and
  repeat. Also reflect the whole preparation when the fixed signed coupling
  permits a verified reflection, or use a separately characterized orientation
  control. Do not assume every geometric reflection is a symmetry.
* Include the no-source preparation, each source separately and both sources
  together. Keep outlet regions and observation times identical. An outlet
  oscillator already present without the source is not transmitted input.
* Record every retained remainder and both counters, including off-axis state
  and the branch called “cancelled.” Zero visible b at one outlet is only a
  projection result. It is not deletion of a route or of microscopic history.

A fixed exact outlet vector is preferable to a moving threshold for this
first comparison. An L1 counter total may be reported as a descriptive
amplitude, but it is not established energy and does not prove that a packet
was transmitted. Equal path length, amplitude and timing are necessary
confound controls; they are not a theorem that the only remaining cause is K.

### Concrete bounded follow-up family

The following family is specified in the separately frozen
[U24-COOPERATION-PATH-v2 protocol](../research/signal_clocks/complexity_protocol.json),
whose SHA-256 is
`0d4f7bb8d42cbaea63fddb9bc2d7a4884d56ff28c0d8cff6a5e13fd7a085bc6c`.
It was frozen before the calibration and held-out runs in this working
session; it is not externally timestamped preregistration. This definition
alone is not evidence that any branch works.

* Use `L=71`, origin `O=(35,35,35)`, tensor signs `(1,1,1)`, and uniform
  background `(a,b,r)=(0,0,2)`.
* Prepare two arms at `O +/- (j,0,0)`, `j=1,...,6`. Each arm site initially has
  channel 0 in `(0,0,4)` and channel 14 in `(0,0,0)`; other channels equal the
  background. Both X ports preserve channel 0 and channel 14 with positive
  weight. All transverse ports remain present and are simulated normally.
* The two perturbation addresses per arm are channel 0 at distances `j=2`
  and `j=3`. The three base variants set both of those remainders to `v`,
  where `v` is 0, 2 or 4. Other prepared remainders are unchanged.
* The calibration source at `O` is channel 0 `(0,1,2)` and channel 14
  `(0,-1,2)`. For each side and each base variant run the empty, first-only,
  second-only and both phase-perturbation subsets. Hold the opposite arm at
  reference variant 4. This gives 24 calibration runs and a binary K score
  for each side/variant pair.
* For calibration, `Y` contains all 48 signed b counters at that arm's outlet
  `O +/- (6,0,0)` at board steps 6, 7, 8 and 9, in time/channel order. Thus
  each Y vector has 192 exact integer coordinates.
* Test all six ordered pairs of **different** base variants on the two arms.
  Each pair gets two held-out common-source preparations: channel pairs
  `(0,2,2)/(0,-2,2)` and `(1,1,2)/(-1,-1,2)`. The total initial absolute
  counter sum is four in both held-out probes. Each pair also gets a
  no-source preparation. This adds 12 joint held-out and six no-source runs.
* Run each side/variant with each held-out source separately, replacing the
  opposite arm by the ordinary background. These twelve isolation controls
  retain the same source, tensor, output address and window. Their source-free
  baseline is exactly stationary by the quiet-state identity below.

The total is 54 runs. The 24 calibration runs use nine complete updates.
The 12 joint, twelve isolation and six no-source runs use fifteen updates.
The held-out response window is **steps 10 through 15**, with all 48 signed
b counters in time/channel order (288 entries per outlet). The earlier window
6 through 9 is reported separately as initial activation, not competitive
routing. One fixed tensor and equal arm lengths are used. The source is
prepared at step zero; there are no later injections. Ordered variant pairs
include every memory swap, and both physical orientations are simulated
rather than assumed to have identical behavior. The whole run horizon is
far shorter than a path from the preparation to a periodic image and back
to either outlet.

The total is 666 forward updates plus full inverse and rewind audits. The
experiment budget is 300 CPU seconds and 600 wall seconds; budget exhaustion
is inconclusive, with the completed prefix and stopping reason retained.

The later window is necessary for the intended comparison. A changed initial
remainder at distance two has no counter effect at step one because its
incident counters are still zero. Its first possible counter difference is
at step two. The opposite outlet is eight graph edges away, giving earliest
possible influence at step ten. The distance-three slot analogously gives
step twelve. The earlier calibration window therefore cannot by itself
demonstrate one branch cancelling the other.

After calibration, a held-out comparison with unequal scores predicts:
the higher-K outlet has at least one nonzero b coordinate in its fixed Y
window, and the lower-K outlet has none. This is deliberately a strict
selection test. Equal K supplies no ordered prediction and must be reported
as unresolved by this measure. A miss rejects that stated prediction for
that held-out case; it is not a general no-go theorem for conditional routing.
All cases, score ties and failures must remain in the report. Zero output in
steps 10 through 15 does not establish permanent extinction, absence of an
earlier record or absence of a later arrival.

Furthermore, “cancelled” requires actual simultaneous signed input terms
`v_d=w_d*b_neighbor` with `sum(v_d)=0` and `sum(abs(v_d))>0`, plus an outlet
active in its matching isolated-arm control but silent in the joint late
window. A zero outlet without both kinds of evidence is silence or suppressed
transmission, not demonstrated destructive cancellation. The local witness
must also distinguish a quiet pre-update channel from a zero b caused by
`b_next=ell-a` recurrence. A nonzero signed-input cancellation count on its
own does not prove it caused the whole branch suppression. Separate nonlinear
trajectories need not add, so subtracting independently evolved pictures is
not an interference proof.

The source-free background claim is exact: if all a and b counters vanish,
then every local input u is zero. Since `0 <= r < 6`, Rule3 gives `ell=0`,
`r_next=r` and zero next counters at every channel. Thus any such complete
remainder preparation is stationary, including an isolated source-free arm.

This family tests routing by **prepared** memory states and the predictive
use of calibration K. It does not by itself show that an earlier signal
autonomously writes those states. That stronger assembly needs the earlier
source history, residual-wave controls and a later probe all prepared at
step zero and evolved together.

## Exact constraints and counterexamples

**A local event cannot compare causally inaccessible complexity.** Use graph
distance on the periodic cube, including its wrap edges. After `T` updates,
the state in a detector region `D` depends only on the preparation within
distance `T` of `D` and on the fixed tensor. At `T=0` this is immediate. If
it holds for `T`, each next local update reads only the preceding site and
its six neighbors, so its initial dependence extends by at most one edge.
Induction proves the claim. The same bound covers a click read from two
consecutive local snapshots. Therefore preparations agreeing on that entire
initial causal region have identical detector histories through `T`, however
different their states elsewhere. A universal instantaneous rule favoring a
branch because of arbitrary complexity outside that region is incompatible
with the local update. This does not prevent a delayed influence after a
signal from the changed region reaches the detector. The K measure must be
interpreted within its declared causal input/output experiment, not as a
global complexity oracle.

**Non-additivity is not a direction of preference.** For a quiet scalar
channel write `r=2*theta+epsilon`, with `theta in {0,1,2}`. The carry is
`q(u)=floor((theta+u)/3)`. For two hypothetical unit input increments define
`d=q(2)-q(1)-q(1)+q(0)`. Then:

| theta | q(0) | q(1) | q(2) | d |
|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 1 | 1 |
| 2 | 0 | 1 | 1 | -1 |

The last two cases have the same binary non-additivity score but opposite
mixed-response signs. Therefore the magnitude-only fact “non-additive” does
not determine a routing direction or a preference for transmission over
suppression. This is an exact local algebraic example, **not** a closed-board
construction of two arriving packets or of the phase-perturbation K above.

**No strictly increasing universal score on a finite recurrent set.** Let
`F` be the complete reversible update and `A` a finite invariant set on which
`F` is bijective. For any real-valued score `H` on `A`,

```text
sum_{s in A} (H(F(s)) - H(s)) = 0.
```

This follows by reindexing the first sum with the permutation `F`. Hence if
all increments are nonnegative, every increment is zero. In particular a
score cannot increase weakly at every point of a periodic orbit and strictly
at any point on that orbit. This rules out a universal strict complexity
ascent on such a set. It does **not** rule out conditional ensemble trends,
finite transient increases, preparation bias or growth on unbounded orbits.
Universe24 has unbounded integer counters, so the entire state space is not
asserted to be finite.

**Information under a finite preparation ensemble.** A deterministic
bijective full-state map permutes the probabilities of a finite discrete
ensemble. Its Shannon entropy is unchanged. A projected outlet distribution
or coarse readout can change entropy because many full states can have the
same projection. This is a statement about ensemble probabilities and a
bijection, not a claim of physical thermodynamic entropy or a Born law.

## Board steps, observed clicks and internal records

Let a protocol define a local transition event `C_t in {0,1}` from the two
complete snapshots around board update `t`. Define the observer's event index

```text
N(0) = 0
N(t) = sum_{s=1}^t C_s.
```

Then `N(t+1)-N(t)=C_(t+1)` is nonnegative by definition. During any interval
with no clicks, the event index stays fixed even while the board advances
through many updates. This captures the requested distinction between board
updates and observed event ticks. It does not by itself establish time
dilation, a physical arrow of time, or a stored internal clock. Computing
`N` from an external history retains information outside the automaton.
Reversibility here means exact recovery of the previous complete state;
it is not, by itself, a proof of invariance under a particular time-reversal
transformation. The declared forward Rule3 iteration and the observer's
event count remain separate mathematical objects.

The stricter internal construction needs a fixed local state readout with
distinct record values `M0`, `M1` and `M2`: the first arriving signal changes
`M0` to `M1`; a declared waiting interval keeps `M1` without a new click; the
second arrival changes it to `M2`. The no-source and single-source controls
must exclude an autonomous scheduled second transition. A clock that starts
periodic counter motion after one arrival does not satisfy this condition
merely because its drawn hand keeps moving.

For a record using only `k` quiet channels and their remainders, each
channel's invariant parity leaves exactly three possible remainder values.
There are therefore at most `3**k` distinct such records within the fixed
parity sector. A nonwrapping count of `n` clicks represented by distinct
records including the zero record requires `n+1 <= 3**k`. This is a finite
capacity bound on that chosen record architecture, not on the full model.
Unbounded counters or a growing spatial record change the bound and require
their own construction. A remainder cycle returning to the same record does
not by itself encode the number of completed cycles.

## Current scope and next decision

The frozen 54-run family has now been executed. The
[cooperation result](../research/signal_clocks/evidence/cooperation/result.json)
retains its full traces and fixed-window vectors. An independent
[vector readback](../research/signal_clocks/complexity_readback_results.json)
parsed all 54 native traces, reconstructed the calibration and held-out
vectors directly, recomputed K both directly and with the passive helper,
and checked the isolated-arm comparisons and signed-input witnesses.
The outcomes are:

| Quantity | Observed result |
|---|---:|
| K for variant 0, either side | 0 |
| K for variants 2 and 4, either side | 1 |
| Held-out comparisons with unequal K | 8 |
| Higher-K-only selection among those comparisons | 0 |
| Both outlets active in those comparisons | 8 |
| Tied-score comparisons, with no ordered prediction | 4 |
| Isolated-active to joint-silent suppression | 0 |
| Qualifying input-cancellation witnesses | 0 |

All twelve held-out runs had activity at both outlets in the declared late
window. The specific finite prediction that the higher-K branch alone
transmits is therefore refuted by this family. This does not show that every
possible cooperation measure or preparation fails to influence routing.

There is a concrete observed obstruction. Memory changes in this family
touch only channel 0, but the source carries channel 14 as well. At **both**
outlets and for **all six ordered variant pairs**, the joint channel-14
b vector in steps 10 through 15 was:

| Probe | b14 at steps 10, 11, 12, 13, 14, 15 |
|---|---|
| P1 | `(-2, 0, 1, 0, 0, 0)` |
| P2 | `(-1, 1, 0, 0, 0, 0)` |

Thus the nominal lower-K branch retains a nonzero output through an unchanged
signal channel. The first concrete counterexample, `joint-0-2-P1`, has
K-left=0 and K-right=1 but identical late outlet vectors: channel 14 is -2 at
step 10 and +1 at step 12 on both sides, with all other late outlet entries
zero. An animation displaying only channel 0 would hide this failure; the
registered all-48-channel criterion correctly preserves it. This is measured
persistence for the specified preparations and horizon, not a theorem that
channel 14 is independent of channel 0 in all states of the full 3D model.

The score does not even order descriptive output amplitude in this family.
For P2, the late absolute-b total of a variant-0 outlet is 10, versus 2 for
variant 2 and 4 for variant 4. These are finite counter totals, not physical
energy. They do not rescue the failed exclusive-selection prediction.

The subsequent preparation varies **both** members of the paired signal at
each memory site, using remainder pairs `(4,0)`, `(2,2)` and `(0,4)` for
channels `(0,14)`. A paired perturbation
`(r0,r14) -> ((r0+2) mod 6,(r14-2) mod 6)` preserves both parities and cycles
these phases. It changes the preparation and the perturbation definition,
so it was tested under a **separate frozen transmission protocol**, with no
new K ranking. The failed complexity-selection result above is unchanged.
This follow-up establishes prepared-memory transfer within its finite domain.
A signal writing that memory and a later signal using it still require their
own closed trajectory and residual-wave controls.

### Conditional algebra for a paired memory barrier

For this follow-up, suppose a pair begins with both counters zero,
remainder phases `(theta, 2-theta)`, and opposite net inputs `(u,-u)` at each
update. Define `S_t` as the cumulative signed input to the first member
through update t. Both members remain counter-quiet through T exactly while

```text
-theta <= S_t <= 2-theta    for every t=1,...,T.
```

Within that interval their phases are `(theta+S_t, 2-theta-S_t)`. This follows
by induction: the two phase numerators stay in `{0,1,2}`, so both quotient
carries vanish and both zero counter pairs stay zero. If the interval is
first left while the previous counters are zero, a nonzero carry produces
a nonzero next b counter. The three preparations therefore give:

| Remainder pair | Quiet cumulative-input interval | First positive unit input |
|---|---|---|
| `(4,0)` | `[-2,0]` | Nonzero opposite carries |
| `(2,2)` | `[-1,1]` | Stored phase change, zero carries |
| `(0,4)` | `[0,2]` | Stored phase change, zero carries |

This is a conditional exact channel-pair statement, not a proof that a whole
board supplies the required input history or blocks every other channel.
Upstream feedback can drive S outside the interval and cause a later leak.
Consequently the follow-up must retain the actual input sequence, first
leak time, all 48 outlet channels and their remainders. Counter silence alone
is weaker than equality of the complete outlet state with its no-source
control. A remainder-only arrival can still leave a record.

### Measured paired-memory transfer

The [paired-blocker protocol](../research/signal_clocks/paired_blocker_protocol.json),
SHA-256 `de584e9dc4ee628b0913ad7bb6d0c523f61ebdcfd3095b5fe7ded7648fea9709`,
was frozen before this follow-up. It uses `L=101`, origin `(50,50,50)`, the
same six-site arms and memory positions 2 and 3. The fixed source preparation
is `(0,1,2)/(0,-1,2)` in channels `(0,14)`. Variant O is `(4,0)`, N is
`(2,2)` and R is `(0,4)` at both memory sites. Nine ordered joint pairs with
source, nine matching no-source controls and six isolated-arm preparations
were run for 40 complete updates: 24 runs and 960 forward updates, plus the
recorded inverse audits. The initial boundary margin is 44, greater than the
40-update horizon.

The [recorded result](../research/signal_clocks/evidence/paired_blocker/result.json)
passes both predeclared nominal conditions. In each direction, isolated O
transmits while isolated N preserves **all 48 complete outlet triples** over
steps 6 through 40. The composed O/N and N/O preparations preserve the same
distinction: the O outlet first changes at step 6; the N outlet is exactly
equal to its matching no-source control throughout the observation window.
Every no-source preparation is stationary. This is prepared state-dependent
transmission and blocking with unchanged Rule3 and coupling, not an external
switch.

The independent [paired readback](../research/signal_clocks/paired_blocker_readback_results.json)
reconstructs these outlet comparisons from all 24 native traces. It also
checks 41,162 stored channel/central-partner entries and 48 actual memory-site
input histories. In this even-parity family the central partner J obeys
`a_J=-a`, `b_J=-b`, `r_J=4-r`; the fixed coupling commutes with J and preserves
its weights. The paired initial preparations therefore keep the two signal
members matched. This addresses the earlier channel-14 bypass, while the
strong outlet test still checks all other channel pairs and all remainders.

The measured cumulative inputs explain why two memory sites matter:

| Preparation and memory site | Initial quiet S interval | Observed behavior through step 40 |
|---|---|---|
| Joint O/N, N site 2 | `[-1,1]` | S stays in `[0,1]`; no counter activation |
| Joint O/N, N site 3 | `[-1,1]` | S remains 0; no counter activation |
| Isolated N, site 2 | `[-1,1]` | S first reaches 2 at step 6; this first site activates |
| Isolated N, site 3 | `[-1,1]` | S stays in `[-1,1]`; the second site still blocks the outlet |

The opposite nominal orientation has the same measured statements; both were
explicitly simulated. An isolated neutral **first** site is therefore not
claimed to remain quiet. The declared two-site assembly is the verified
finite blocker.

There are also six R-branch observations that are active in isolation but
have unchanged outlets when the other prepared arm is present. These are
counterfactual suppression observations, not demonstrated destructive-input
cancellations: **zero** cases satisfy the registered nonzero-term zero-sum
witness. The local difference is concrete. At R site 2, the isolated input
at step 4 is -2, taking S from 1 to -1 and out of its permitted `[0,2]`
interval. That site activates at step 4 and its isolated outlet first changes
at step 10. In the corresponding joint preparations the step-4 input is -1,
taking S to 0; S stays in `[0,1]` and the site remains counter-quiet through
40. The companion arm changes the incident waveform under the same initial
source preparation. It is not an additional selection instruction and does
not prove that opposing input terms cancelled at the outlet.

These measurements establish a finite prepared-memory building block. They
do not establish indefinite blocking, robustness to arbitrary probes, an
autonomously written routing memory, physical light, or a preference for
greater K. No observation window or failed earlier score was changed to
obtain this separate result.

The definitions and proofs above remain model-level constraints. A successful
signal-driven waiting record, controlled routing or high-K preference needs
its own complete-state evidence. Failure of a selected family is failure of
that family and declared budget, not a proof that every permitted preparation
is impossible. No modification of Rule3, fixed connectivity or coupling is
proposed by this note.
