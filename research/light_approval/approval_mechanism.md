# Reversible signal approval: mechanism and unresolved interface

Research base: `5894510ada12d22f17a70f93a41ec311aef13265`, 7 November 2026.
This note analyzes preparations and readouts under the existing Rule3 contract.
It introduces no engine operation and reports no quantum-entanglement result.

## Question and present answer

Can a board represent competing possibilities, evolve them locally, and create
a persistent detector record only after an internally generated signal approves
one possibility? A conditional local arithmetic mechanism exists. Its required
input waveform has not yet been demonstrated as an autonomous, composable
waiting/approval device in the complete board. Shared-source correlations and
the first arrival of a signal do not establish this stronger mechanism.

Here a **signal** means a specified transported counter/remainder disturbance.
Its identification with physical light remains a separate research objective.
An **approval** must be an ordinary incoming signal produced by another part of
the same closed preparation. It is not a callback, a supplied Boolean, or a
score evaluator that changes the state.

## Alternatives inside one reversible trajectory

For fixed tensor and complete initial state, the deterministic board has one
trajectory. Two candidate routes can be distinct simultaneously present state
patterns within that trajectory. A proposed internal search would likewise
need physical representations of its candidates, comparisons and workspace
in the counters and remainders. The claim that all possible futures are
explored is stronger: it requires an explicit representation, a finite declared
candidate family and a derivation of how the same rule evaluates it. The
current recipes do not provide that derivation.

An ensemble of separately prepared runs represents alternatives in an
experimenter's analysis. It is not evidence that one board evaluated those
runs. A post-run selection of the most complex trace is also distinct from an
internally generated approval signal. These distinctions remain necessary even
when both displays use clocks and gears.

## Exact local calculation

For an actual incoming signed sum `u`, Rule3 is

```text
ell, r_next = divmod(2*u + r, 6)
a_next = b
b_next = ell - a
```

The existing arithmetic observer requires `ell != 0` and an actual change of
the complete local triple for a C event. Thus a remainder change can write a
record without producing C. Conversely, later counter rotation with zero
quotient need not produce another C.

The following two-channel calculation is exact, conditional on the listed
**actual** input sequence. Each triple is `(a,b,r)`; the channels are 0 and 14.

| Stage | Incoming pair | Channel 0 | Channel 14 | Quotients | Guarded C |
|---|---|---|---|---|---|
| Initial preparation | — | `(0,0,2)` | `(0,0,4)` | — | — |
| First arrival: write pending state | `(1,-1)` | `(0,0,4)` | `(0,0,2)` | `(0,0)` | None |
| Waiting update, repeatable | `(0,0)` | `(0,0,4)` | `(0,0,2)` | `(0,0)` | None |
| Second arrival: confirmation | `(1,-1)` | `(0,1,0)` | `(0,0,0)` | `(1,0)` | Channel 0 |
| Subsequent zero-input updates | `(0,0)` | Four-cycle at `r=0`, `a²+b²=1` | `(0,0,0)` | `(0,0)` | None |

The confirmation writes a different remainder pair and a nonzero counter
magnitude. The first counter pair rotates `(0,1) -> (1,0) -> (0,-1) -> (-1,0)`
under zero actual input. The readout can remain constant while the underlying
state continues evolving. This is a precise limited realization of many board
updates occurring between recorded events; it is not a derivation of physical
time from click count.

Direct exact-integer substitution checked the write, four quiet updates,
confirmation and four subsequent zero-input updates. This arithmetic check is
not a full-board experiment: a nonzero receiver counter sends effects through
its fixed neighbors, which may return and spoil the assumed zero input.

### Necessary conditions for quiet retention

For one channel, exact stationarity implies

```text
a = b, ell = 2*a, u = 6*a.
```

Conversely, these conditions make its full triple stationary. In particular,
a stationary zero-counter remainder record requires actual input `u=0`.
This equivalence follows by substitution for every permitted integer state.
As a finite arithmetic regression, all 14,406 combinations with
`a,b in [-3,3]`, `r in [0,5]`, and `u in [-24,24]` satisfied it.

If `u=0`, the invariant local magnitude is `I=a²+b²`. In general,
`I_next-I=ell²-2*a*ell`; this is an arithmetic identity, not a physical-energy
interpretation. Persistent readout can therefore be an orbit property rather
than a frozen counter state, but feedback from the whole apparatus must still
be accounted for.

The telescoping identity

```text
r_T-r_0 = 2*sum(u_t) - 6*sum(ell_t)
```

implies that zero integrated signed input returns the remainder to its initial
value. If the endpoint counters also return, the complete local triple returns.
Thus an unmodified location traversed by the existing exact translating packet
does not automatically become a permanent quiet remainder memory. A detector
would have to alter the actual waveform, retain a counter record, or distribute
the record over more addresses. This is a conditional obstruction, not a proof
that all detector preparations are impossible.

## What the existing full-board evidence establishes

The evidence is recorded in [the waiting/confirmation study](../../docs/CONFIRMATION_BLOCK.md)
and [the route-to-receiver study](../../docs/PATH_SELECTION_BLOCK.md).

| Claim | Evidence and scope |
|---|---|
| Source-dependent local clock/record response | Demonstrated in declared finite source/guide/receiver preparations; these remain useful components. |
| Local write–wait–confirm arithmetic | Exact conditional calculation above; it supplies a target input contract. |
| Autonomous quiet waiting/confirmation | Not established: 145 tested preparations, 580 controls, zero accepted cases. |
| Route-generated first receiver confirmation | Joined OR route supplies actual `(1,-1)` and first C at step 12 in the declared preparation. |
| Single click and retained confirmation in that joined preparation | Fails: 19 C-bearing receiver updates at `12,14,...,48`; the candidate remainder record changes at step 14. |
| Selection by highest registered cooperation score | Fails for `C_pair`: ten eligible comparisons, ten counterexamples; this is not a theorem about every complexity measure. |

A particularly useful failure is `confirmation-000-s10`: one source writes
the intended pending pair at step 8, but actual input `(-2,+2)` at old step 9
already causes C at step 10. The second source is absent. The problem is the
complete-board waveform and its feedback, not an absence of the desired
scalar threshold operation.

### New autonomous probe in this research round

The separately frozen [approval protocol](approval_protocol.json) tests the
same local latch arithmetic with actual complete-board inputs: L101, H32,
receiver `(50,50,50)`, source offsets -8 and +16 along X, two initial right
source signs, and all four on/off controls. The
[eight-run result](evidence/approval_v1/result.json) accepts neither phase
family. All 256 forward/inverse transitions and full rewinds pass.

Independent inspection of the complete left-only recording shows:

| Old board step | Actual paired input | New state at next step |
|---|---|---|
| 7 | `(1,-1)` | Step 8: zero counters and pending remainder pair `(4,2)` |
| 8 | `(0,0)` | Step 9: same pending state |
| 9 | `(-2,2)` | Step 10: remainder pair `(0,0)`, but channel-14 C and `I0=0,I14=1` |
| 11 | `(2,-2)` | Step 12: another C; the candidate record changes |

The same early sequence occurs with both sources present, before the intended
second-arrival window. Pending states last only at sampled steps 8 and 9.
Importantly, the remainder pair `(0,0)` alone would resemble the intended
confirmation, while the full counters identify the different event: the
conditional intended confirmation above has `I0=1,I14=0`. A frozen readout
must retain this distinction. These eight runs reject this declared
preparation family; they do not prove impossibility of all approval devices.

## A preparation-only development path

The next mechanism candidate should combine a compact, finite signal, a
conversion region, a pending-state receiver and a retained outgoing record.
Each must be an initial patch with the same tensor. This is a construction
target, not an implemented new library recipe. The translating guided packet
is a candidate input source, but its known passing waveform alone does not
supply the required memory transformation or guarantee compatibility with a
conversion region.

Before evaluating candidates, freeze the following stages and predicates:

1. **Write.** The first actual arrival changes the designated receiver from
   `(2,4)` to the zero-counter `(4,2)` remainder pair without any C event in
   any of its 48 channels.
2. **Wait.** For at least four complete subsequent updates the designated
   full receiver state remains fixed and its actual input sums are zero.
3. **Confirm.** A later ordinary signal causes exactly one receiver-node
   C-bearing update inside the declared arrival window. No external event
   inserts it, changes a coupling, or updates a readout into the board.
4. **Retain.** A prospectively fixed readout, for example the confirmed
   remainder pair and counter magnitude above, remains true for at least
   eight subsequent updates. Continuing counter phase motion is allowed;
   further receiver-node C events fail this strict single-event criterion.
5. **Account.** Retain all 48 channel triples at every node, actual inputs,
   source controls and exact inverses. Locate where the candidate and
   comparison information survives; a quiet visible outlet is not deletion.

Null, first-only, second-only and both-source preparations must share their
apparatus and initial remainders, varying only registered initial source
counters. Each single-source control must be checked through the complete
fixed horizon, not only before the intended second arrival. Two preloaded
sources can demonstrate a two-arrival component, but they do not demonstrate
that a path-selection mechanism computed the second arrival.

To establish **unique-path approval**, the confirming disturbance must instead
originate from a specified internal interaction in the competing-route
apparatus. Every competitor relevant to the decision must lie in the decision
region's declared causal past. A finite local device cannot certify the
absence of an unbounded remote future signal. A bounded route family with
predeclared travel limits, and locally generated return information, is a
meaningful prospective target. No external maximum-complexity calculation is
permitted to supply its outcome.

Repeated use is an additional milestone. Returning the entire apparatus and
all its environment to one reset state while forgetting its input history
would contradict injectivity. Reusable visible states may coexist with
retained history elsewhere, but that storage and its growing requirements
must be included in the complete model. No indefinite-reuse claim follows
from two successful arrivals.

### Bounded next task — proposed, not executed

Question: can the existing exact compact guided packet write a quiet pending
record when it meets a prepared receiver defect? It is a useful next input
primitive because it has a finite waveform, rather than an indefinitely
emitting oscillator. However, its opposite lobes cancel at an unmodified
guide location, and its exact translation proof assumes the unmodified guide.
That proof cannot be extended through a receiver defect without checking the
interaction. Reflections and transverse feedback involve the complete 48
channels and retained halo.

A minimal next protocol could use L129, H24, a complete periodic `(0,4)` X-row
guide at Y=Z=64, the existing packet initially at X=32..35 and a receiver at
X=48. The disturbance has no time to reach a periodic boundary in this window.
Use all nine even receiver-remainder pairs with zero counters, each with
source-present and source-absent controls: 18 runs, at most 60 CPU seconds.
The unmodified receiver pair is an exact-translation control. Freeze all
preparations and predicted record predicates before evolution.

The packet's leading channel-0 current has negative sign, so its first direct
paired input at the receiver is expected at update 13 as `(-1,+1)` in the
unperturbed propagation region. The two-arrival scalar table has a sign-dual
version: `(4,2) -> (2,4) -> (0,0)`, with channel-14 confirmation on the second
identical input. Its trailing opposite lobe and the defect's own backreaction
can undo this record; both must be included rather than filtered from the
readout.

This first interface study should require a declared changed remainder
record, zero receiver counters, no receiver-node C, and at least eight
subsequent complete quiet updates within the fixed horizon. Candidate-specific
record targets and time windows must be registered in advance, not selected
from whichever plateau appears. It tests a pending record only. A successful
candidate would then need a new prospective second-arrival protocol and
fresh controls for confirmation and retention. Internal route-generated
approval remains a subsequent task. No such packet/receiver study was run
as part of this note.

## Relation to the current two-party computation

The new L97, H16 experiment uses two separated receivers, four shared source
phases and two local remainder preparations. Its first-C sign outcome can
test local signal response and shared-initial-data correlations. It does not
implement the write–wait–confirm contract above. All no-click outcomes,
actual input traces, all 48 receiver channels and later C events must remain
visible; a first-event statistic alone does not demonstrate a lasting record.

The recorded `shared-0-00` case illustrates the distinction: both receivers
have C-bearing times 8 and 10; channel-0 magnitude changes from 1 at steps 8–9
to 4 at steps 10–16, with rotating phase. That later finite plateau is a real
observation. It does not rescue the failed criterion that the first click
write the final unchanged record, nor does the first-click failure establish
that every form of local memory is absent.

Approvals in a common past can correlate subsequent local records. Approvals
that depend on both measurement settings after communication describe a
different causal arrangement. Selection of only jointly approved clicks can
also change the sampled ensemble. These possibilities must be distinguished
before interpreting any click correlation as quantum entanglement. The
independent [locality analysis](locality_proof.md) and
[physics review](physics_review.md) specify the separate Bell, no-signalling
and quantum-state obligations. An approval mechanism would be a useful
building block even if it only produces classical correlations.
