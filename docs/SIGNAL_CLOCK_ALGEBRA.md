# Signal-triggered records and guarded clicks: algebra and limits

This note fixes the distinction between a retained remainder record, the
reference engine's guarded arithmetic C event, and a spatially realizable
device. The reference engine, tensor and six-input connectivity are unchanged.
The examples below that supply an input sequence are **scalar specifications**;
they are not experiments in which a runtime source was injected into the board.
A successful device must generate those inputs autonomously from its initial
full-board state.

The physical name *light clock* is not established here. The operational target
is a signal-triggered event clock: a specified incoming influence produces a
guarded event, leaves a record, and produces no further guarded event until a
later autonomous arrival. Clocks drawn by The Presenter are views of the same
stored integer state.

## 1. Exact remainder algebra

For any integers `a,b,u` and `r` in `{0,...,5}`, Rule3 is

```text
2u + r = 6 ell + r_next,   0 <= r_next < 6
a_next = b
b_next = ell - a.
```

Write `r=2 theta+epsilon`, with `theta` in `{0,1,2}` and `epsilon` in
`{0,1}`. Euclidean division gives the equivalent identities

```text
ell = floor((u+theta)/3)
theta_next = u+theta-3 ell
epsilon_next = epsilon.
```

**Proof.** The right-hand remainder `2 theta_next+epsilon` lies in `{0,...,5}`
and reconstructs `2u+r` with quotient `ell`. Uniqueness of Euclidean division
proves equality, including negative `u`. Reducing the defining equation modulo
two proves invariant parity. These are statements for all permitted scalar
states, not extrapolations from finite tests.

Consequently a remainder change occurs exactly when `u mod 3 != 0`.
It detects a residue of the **net signed sum**, not every individual incoming
port. Nonzero inputs can cancel, and a nonzero sum divisible by three need not
change the remainder.

## 2. The existing C guard is essential

The existing observer reports an arithmetic event only when both
`ell != 0` and the local triple changed. Its class is

```text
k = ((r_next-r)/2) mod 3 = u mod 3,
```

with the division exact because parity is conserved. The name is `Ck`.
No classification changes the state or routes a signal.

Two counterexamples prevent conflating an arbitrary remainder write with an
engine click:

| Old state | Actual net input | Next state | Consequence |
|---|---:|---|---|
| `(0,0,0)` | 1 | `(0,0,2)` | A record changes, but `ell=0`; no guarded C event |
| `(0,0,0)` | 3 | `(0,1,0)` | A guarded C0 event occurs, but the remainder is unchanged |

A protocol may separately measure remainder records, but those observations do
not satisfy a guarded-C acceptance criterion by renaming them. In particular,
the arithmetic name C2 is not a proven physical selection law.

## 3. Rest, waiting and internal rotation

If the actual net input is zero, `ell=0`, the remainder stays fixed, and

```text
(a,b) -> (b,-a) -> (-a,-b) -> (-b,a) -> (a,b).
```

A zero pair is fixed; any nonzero integer pair has exact period four. For a
nonzero pair, neither one, two nor three applications can return it to itself:
the corresponding equations imply both counters zero. Thus a nonzero pair
cannot stop under zero input. Waiting for a later **event** is compatible with
this internal rotation: the zero-input carry is zero, so there are no guarded
C events during it.

There is a sharper local limitation. If a channel starts at full local rest
`a=b=0`, an immediately successful guarded C event has `ell != 0`, hence
`b_next=ell != 0`. It cannot simultaneously leave both counters at rest.
A specification requiring immediate full counter rest after such an event is
inconsistent with Rule3. Subsequent input could cancel counters; that would be
an additional part of the autonomously generated incoming signal, not an
observer-operated stop.

If every board counter is zero, all six-input sums vanish. The entire state is
then fixed for any permitted remainder pattern and fixed tensor. This proves
source-absent quiescence for apparatus encoded entirely in remainders.

### A closed-board period-four control with zero event ticks

Choose any of the 48 channels g at one site, initialize it to `(0,1,2)`, and
put every other address at background `(0,0,2)`. Any allowed fixed sign tensor
and any allowed cube side `L>=3` work. This is a complete autonomous initial
preparation, unlike the prescribed input examples below.

**Claim.** The complete board has exact period four and no guarded arithmetic
C event at any address, for arbitrarily many forward updates.

**Proof.** The source's six receiving addresses occupy its six distinct face
neighbors. They therefore do not coincide with each other or with the source
when `L>=3`. Only the source counter b is nonzero. If its recipients keep zero
counters, the source input is zero, and its `(a,b)` sequence is
`(0,1),(1,0),(0,-1),(-1,0),(0,1)`. Each recipient has one signed incoming
contribution with weight w in `{-1,+1}`. Its actual input sequence is therefore
`w*(1,0,-1,0)`. Starting at phase 1, its successive phases are

```text
1 -> 1+w -> 1+w -> 1 -> 1.
```

All phases remain in `{0,1,2}`, so every recipient carry is zero and its
counters indeed stay zero. Every other address has zero input and stays at
background. This closes induction over the complete board. Source and
recipient carries are all zero, so the existing C guard always fails. The
source returns first after four steps, and its six retained remainder changes
return at that time too; hence the complete state has exact period four.

The regression test covers all eight tensors, all 48 source channels and
`L=3,5`: 768 complete preparations, eight updates each, or 6,144 full-state
transitions with one-step inversion and no-C checks. This is positive evidence
for a precise limited component: board updates and visible counter rotation
can occur while the chosen arithmetic event count remains zero. It is not a
signal-arrival clock, physical light or a source-free apparatus awakening.

## 4. Two distinct scalar component specifications

Let two channels initially have triples `(0,0,2)` and `(0,0,2)`. Their memory
readout is the ordered pair of retained remainders. In each specification there
are two equal paired arrivals separated by six updates with zero net inputs,
followed by eight more zero-input updates. The first arrival is the transition
to sampled state 1; the second is the transition to sampled state 8.

### A. Silent priming followed by activation

Prescribe paired net inputs `(1,-1)` at those two arrivals. Exact states are:

| Sample | Remainder pair | Counter pairs `(a,b)` | Guarded events |
|---|---|---|---|
| 0 | `(2,2)` | `(0,0)` / `(0,0)` | None |
| 1 through 7 | `(4,0)` | `(0,0)` / `(0,0)` | None |
| 8 | `(0,4)` | `(0,1)` / `(0,-1)` | C1 / C2 |

The first arrival writes a persistent resting record. It is **not** a guarded
click. The second activates counters, followed by their internal rotation if
the net inputs remain zero. This truth table supplies an arming interface;
it does not pass a requirement for two genuine guarded clicks.

### B. Two genuine guarded events with a waiting interval

Instead prescribe paired inputs `(4,-4)` at both arrivals:

| Sample | Remainder pair | Counter pairs `(a,b)` | Carries | Guarded events |
|---|---|---|---|---|
| 0 | `(2,2)` | `(0,0)` / `(0,0)` | — | None |
| 1 | `(4,0)` | `(0,1)` / `(0,-1)` | `1,-1` | C1 / C2 |
| 2 through 7 | `(4,0)` | Internal period-four rotation | `0,0` | None |
| 8 | `(0,4)` | `(-1,2)` / `(1,-2)` | `2,-2` | C1 / C2 |
| 9 through 16 | `(0,4)` | Internal period-four rotation | `0,0` | None |

All three memory values are distinct. The two prescribed arrivals produce
authentic existing C events, and the waiting intervals contain none. This is
an exact feasible local interface. It says nothing yet about whether a spatial
preparation can deliver precisely those sums without extra events.

The former guide source reverses its counter phase and can send later inputs.
An experiment must retain such returns and reflections. Discarding them or
stopping observation before an unwanted reset would not establish a reusable
component. Source-only and source-absent controls must use the same fixed
readout and observation horizon.

### C. Two unit arrivals using asymmetric initial memory

The code owner proposed a lower-amplitude alternative, independently checked
against the reference primitive and its actual `classify` function. Start at
rest with remainder pair `(4,2)`, use paired inputs `(1,-1)` at states 1 and 8,
and zero input otherwise. The first event is C1 on the first channel only;
the second is C2 on the second channel only:

| Sample | Remainder pair | Counter pairs `(a,b)` | Guarded events |
|---|---|---|---|
| 0 | `(4,2)` | `(0,0)` / `(0,0)` | None |
| 1 | `(0,0)` | `(0,1)` / `(0,0)` | C1 / none |
| 7 | `(0,0)` | `(0,-1)` / `(0,0)` | None |
| 8 | `(2,4)` | `(-1,0)` / `(0,-1)` | None / C2 |

There are no other guarded events through state 16 under the specified input
sequence. This qualifies as two events at the two-channel apparatus, not two
events at each individual channel. The asymmetric initial memory breaks the
usual opposite-channel symmetry, so a full-board experiment must include its
actual off-axis states and later feedback. It remains a prescribed-input
interface, not an autonomous source construction.

## 5. A retained state can change transmission without a switch

Two resting remainder states respond differently to the same paired input:

| Initial remainder pair | Input sums | Next counter b pair |
|---|---|---|
| `(2,2)` | `(1,-1)` | `(0,0)` |
| `(4,0)` | `(1,-1)` | `(1,-1)` |

This follows directly from the quotient thresholds. The first input can prime
the memory from the first row to the second row; the same later input can then
produce nonzero outgoing counter values. The weights and channel maps do not
change. A neighboring receiver reads those counters on the next synchronous
update, as always.

This is **local state-conditioned output**, not a certificate for route
selection. A route-selection claim additionally requires a complete prepared
network, two fixed output regions, causal controls, a declared measurement
window and reproducibility under held-out preparations. Competing ports,
off-axis remainder changes and later leakage must remain in the evidence.
No untested complexity score may be substituted for the actual integer state.

### Paired preparation and channel leakage

For the current 2O channel indexing, channel 14 is the central negative of
channel 0. More generally let J send quaternion g to `-g`. These have identical
spatial rotations, so for every direction the fixed port map P and weight w
satisfy `P(Jg)=J(P(g))` and `w(Jg)=w(g)`. Right multiplication by each fixed body
action commutes with the central sign; this proves the port identity.

Consequently the following full-board subspace is invariant:

```text
a[Jg] = -a[g],  b[Jg] = -b[g],  r[Jg] = 4-r[g],
r[g] in {0,2,4}.
```

The signed input at Jg is the negative of that at g. If `z=u+theta`, its paired
phase numerator is `2-z`; the integer identity
`floor((2-z)/3)=-floor(z/3)` makes the paired carries opposite, and the paired
new phases sum to two. This proves invariance under every update. Background
remainder 2 and the guide pair `(4,0)` satisfy the condition.

A memory edit made only to channel 0 generally breaks this symmetry. Suppressing
that channel therefore does not establish suppression of channel 14 or the
other 46 channels. A separate paired-memory preparation can vary the pairs
`(4,0),(2,2),(0,4)` together, preserving opposite counters in the paired channels.
This fixes one specific leakage mechanism; it does not prove complete output
suppression or routing. Pair-valued preparation variables are a new calibration
family if the original complexity protocol varied individual channel addresses.
Existing results cannot be relabeled using that later definition.

For an initially resting paired phase `(theta,2-theta)`, let `S(t)` be the
cumulative **actual** first-channel net input since initialization, with the
companion receiving the opposite input. The pair stays at counter rest through
T exactly when every prefix satisfies `-theta <= S(t) <= 2-theta`. Indeed,
remaining at rest forces every carry to zero, so its phases are
`theta+S(t)` and `2-theta-S(t)`; conversely these bounded phases force zero
quotient at every step. The first exit produces nonzero opposite carries.
This conditional barrier identity is independently checked on all 625
four-input sequences from `[-2,2]`, each at three starting phases (1,875 cases). It does not assert
that a chosen closed-board guide realizes a bounded input sequence. The
separate cooperation study specifies paired-memory experiments and their
actual causal inputs.

### A phase-dependent internal amplitude record

Define the integer observable `I=a*a+b*b`. The exact counter update gives

```text
I_next = b*b+(ell-a)*(ell-a) = I+ell*ell-2*a*ell.
```

Thus `I` is constant throughout any interval with `ell=0`, in particular any
zero-net-input waiting interval. It is a counter-amplitude record, not an
established physical energy or a generally conserved quantity. For example,
at phase `(a,b)=(A,0)` with carry `ell=-1`, the next pair is `(0,-A-1)` and
`I` increases from `A*A` to `(A+1)*(A+1)`. With the opposite old phase
`(-A,0)` and the same carry, it decreases to `(A-1)*(A-1)`. Generic arrivals do
not impose monotonic growth.

In the already recorded endpoint-064 both-source trajectory, the per-channel
I values are 0 before step 12, 1 from steps 12 through 21, and 4 from steps 22
through 32. The first event has `a=0,ell=1`; the second channel-0 event has
`a=1,ell=-1`. The identity explains both increments exactly. The remainder pair
returns to its initial value at the second event, but the local full counter
state retains a distinction. This is a **post-hoc observation** of that retained
trajectory, not a passing result for its frozen three-remainder-symbol test.
A future amplitude-record criterion requires its own fixed preparation,
readout, retention and phase-sensitivity tests before new cases are inspected.

## 6. Information retention and event time

An invertible full-board update cannot settle into a complete fixed state after
a nontrivial history. If `F(S*)=S*` and `F^T(S)=S*`, applying the unique inverse
T times gives `S=S*`. Local records can become stationary while their history
remains in the rest of the board. A signal disappearing from a selected channel
or a readout becoming zero does not show microscopic information loss.

Likewise, on a finite invariant set K where F is a bijection, a real-valued
complexity score cannot satisfy `C(F(s))>=C(s)` for every state and a strict
increase at any state. Summing all differences over K gives zero because F
permutes K. On a periodic orbit this reduces to a telescoping sum. This does
not exclude complexity growth over a selected transient, conditional ensemble
or an unbounded orbit. Any proposed preference needs a specified score,
initial ensemble and comparison; reversibility alone supplies no such bias.

For a declared event observer, `n(t)` can count guarded arrivals through board
step t. It is constant between arrivals even while counters rotate. This is a
coarse event index, not an independently derived physical time metric. Its
monotonicity is part of the counting convention; it is not a microscopic arrow
of time or evidence that every possible observer sees nothing between events.
The order and retention of actual internal records need separate testing.

## 7. Finite verification and reproduction

[algebra_checks.py](../research/signal_clocks/algebra_checks.py) compares the
reference scalar primitive to the independently written three-phase formula.
The [retained result](../research/signal_clocks/algebra_results.json) contains:

- 7,950 signed scalar cases: all `a,b` in `[-3,3]`, four additional pairs with
  5,001-digit integers, all six remainders and inputs `[-12,12]`;
- 318 zero-input cycle cases;
- five silent-priming waiting intervals and five genuine-C waiting intervals;
- exact prescribed-input trajectories, source hashes and measured CPU time.

The separate [regression tests](../tests/test_signal_clock_algebra.py) contain
eleven passing tests, including the distinction between quiet writes and guarded
events. These finite checks support the implementation of the displayed
identities; the algebraic proofs above establish their stated all-state scope.
Neither collection certifies a closed-board device.

```bash
python -m unittest tests.test_signal_clock_algebra -v
python -m research.signal_clocks.algebra_checks --output runs/new-signal-clock-algebra.json
```

The script refuses to overwrite evidence and rejects its result if the completed
fixed-size check exceeded 180 CPU seconds; this is not a preemptive timeout.
No random sampling, model changes or runtime interventions are used in these
checks. The next decisive computation is a full-board preparation producing
separated authentic C events and a retained state that changes subsequent
transmission, under the separately frozen spatial experiment protocol.

## 8. A separate bounded synthesis strategy

If a registered guide family fails, a future preparation family can use exact
integer constraints to design the complete causal environment. Introduce
integer variables `a[i,t], b[i,t], theta[i,t]` and retain the fixed parity and
tensor. The equations

```text
a[i,t+1] = b[i,t]
3*(b[i,t+1]+a[i,t]) + theta[i,t+1]-theta[i,t]
    = sum_j w[i,j]*b[j,t]
0 <= theta[i,t] <= 2
```

are exactly equivalent to Rule3: `ell=b[i,t+1]+a[i,t]`, and the bounded next
phase makes it the unique Euclidean quotient. They are linear integer
constraints for each prescribed space-time location. Fixed finite counter
bounds `|a|,|b|<=B`, a finite horizon and finitely many source addresses turn
the search into a finite bounded feasibility problem. A guarded C requirement
adds the finite disjunction `ell!=0` and a changed local triple.

At t=0 every apparatus counter must remain zero; only the protocol's specified
source regions may carry nonzero counters. The solver can choose allowed
initial phases and source counters. Several source-present/absent trajectories
can share one apparatus preparation while satisfying their own fixed readout
constraints. This searches for initial conditions; it does not apply those
constraints as runtime forces.

A design must include every initial degree of freedom in the relevant causal
cones and fix the omitted state to the declared background. A complete initial
checkpoint is then advanced and rewound with the reference engine. A solver
certificate alone is not the full-board engine certificate. Reversing an
arbitrarily chosen final state without the initial-rest constraints is not
sufficient: it generally puts unintended counters inside the apparatus.

This section proposes a future candidate family only. It does not change a
completed protocol or claim that such a source has been found. Unsatisfiability
at one bound B, horizon and source geometry would exclude only that finite
search domain, not all initial states of Universe24.
