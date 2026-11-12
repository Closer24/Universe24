# Bounded local comparison under Rule3

Reviewed base: `621fc1f55800e50e1db5f6a30ce24bb83716a49a` (PR #47).
This is a source-only algebra/control study for issue #45. It does not replace
the other team's phase-link motif definition or burst protocol and does not
append another mechanism to the physical model.

## Constructive result: a prepared comparison response

Let `x` be one retained Boolean score at the target node and `y` one retained
Boolean score at its positive-x neighbor. Declare four channel types:

| Channel | Input polynomial `u` | Responsibility |
| --- | --- | --- |
| score_left | `6 b_left` | Retain the left argument |
| score_right | `6 b_right` | Retain the right argument |
| prefer_left | `3 x - 3 x y` | Response to strict Boolean preference |
| preferred_score | `3 x + 3 y - 3 x y` | Response to the Boolean maximum |

All terms have degree at most two and lie on the target or one physical face
edge. There are no old-`a` reads. All four channels retain their complete
`(a,b,r)`, totaling twelve integers per node. All are audit-labelled. Preparing
each score with `a=b` leaves it constant under `b_next=2b-a`, for every carry
`0<=r<6`. Preparing both response channels with `a=b=0` gives, after one step,

`prefer_left.b = x(1-y)` and `preferred_score.b = x+y-xy`.

For Boolean arguments these equal `1[x>y]` and `max(x,y)`. The input pair stays
retained: no losing input, branch or history is erased. This is an actual
Universe24 `Tensor` executed by its unchanged `Engine`, not a host-side `max`
callback. Python `max` occurs only in the independent expected-value check.

The generic receiver identity is

`u=3F => ell=F, r_next=r, a_next=b, b_next=F-a`.

Consequently the inverse is exact even outside the Boolean domain and with
nonzero response history. That inverse success does **not** imply a valid
comparison outside its prepared domain. For example `(x,y)=(2,1)` gives
preference zero and preferred response one, although `x>y` and `max(x,y)=2`.
With `(x,y)=(1,0)` and older response `a=2`, the new response is `-1`, not one.

The positive prepared response also does not accumulate: with constant `F=1`
and initial response `(a,b)=(0,0)`, its states are
`(0,1), (1,1), (1,0), (0,0)` and then repeat. The executable control checks two
full cycles. Selecting the first two updates after examining the output would
not establish recurrent growth.

## Restricted obstruction: arbitrary integer thresholds in one update

Fix the other retained channels, the old response `a`, and carry `r`. If a
polynomial `P(x)` were to implement an exact arbitrary-integer threshold in one
Rule3 quotient, then

`floor((2P(x)+r)/6)=1[x>0]`.

On all nonpositive integers the right side is zero, so `0<=2P(x)+r<6` there.
A nonconstant polynomial is unbounded on that infinite half-line. Thus `P`
would have to be constant, contradicting the positive half-line. The same
argument rules out a one-update exact positive part `max(x,0)`: it too is zero
on an infinite half-line but nonconstant elsewhere. Setting the other score
to zero reduces an arbitrary-integer max comparator to this case.

This is a new elementary argument for this **restricted one-update,
fixed-auxiliary-state interface**. It is not a no-go theorem for Rule3,
multi-step reversible circuits, bounded encodings, input-dependent auxiliary
preparation, variable-time digit comparison, or physically emergent preference.
The floor/carry operation is included in the argument; it was not silently
replaced by a polynomial update.

## Executed checks and acceptance boundary

Run:

```bash
python -m validation.synthesis.complexity_selection --out runs/synthesis/complexity_selection.json
```

The script checks all four Boolean input pairs against **all 1,296 independent
four-channel carry assignments**, for 5,184 prepared comparisons. It also
checks all 625 four-channel signed values in `[-2,2]` at each of six uniform
carries (3,750 cases), six large-integer cases, six unprepared inhomogeneous
states, the two cycles, the two negative examples and a real periodic face
seam. Every complete state is compared to independent explicit scalar
equations and passed through `Engine.inverse_step`. The seam perturbation at
`x=0` affects the declared receiver at `x=2`, without cross-axis influence.
The output JSON records actual counts, source hash and the reviewed base.

| Claim | Status |
| --- | --- |
| Integer/local/budget-compliant four-channel test tensor and exact inverse | Passed |
| First-update Boolean preference with supplied prepared bits | Passed |
| Arbitrary integer comparator from this polynomial | Failed; explicit `(2,1)` counterexample |
| Monotone repeated selection from this preparation | Failed; exact period four |
| Computation of a structural score from the 44-channel physical state | Not implemented |
| Feedback into matter/geometry and shared stress accounting | Not implemented |
| Recurrent burst-to-burst structural growth | Not tested by this control |

The four score/response slots would fill all remaining capacity in a 44+4
allocation. They therefore **compete with**, rather than augment, the other
team's four intensity apparatus slots. No ownership reservation or physical
integration is made. A scalar amplitude, bit, integer magnitude or supplied
flag is not a demonstrated structural complexity score.

## Primary literature and next admissible handoff

1. C. H. Bennett, *Logical Reversibility of Computation*, IBM Journal of
   Research and Development 17, 525–532 (1973),
   [original paper transcription](https://www.cs.princeton.edu/courses/archive/fall06/cos576/papers/bennett73.html),
   DOI `10.1147/rd.176.0525`. Bennett constructs reversible computation by
   retaining intermediate information and later reversing the computation
   while preserving its result and original input. This supports retaining
   the losing alternative; it does not supply a four-slot Universe24 compiler.
2. E. Fredkin and T. Toffoli, *Conservative Logic*, International Journal of
   Theoretical Physics 21, 219–253 (1982),
   [original paper](https://www.cs.princeton.edu/courses/archive/fall06/cos576/papers/fredkin_toffoli82.pdf).
   The paper constructs reversible conservative logic and analyzes auxiliary
   storage and reusable computation. Its circuit universality is not a proof
   of an invariant Boolean encoding or scheduler under this fixed Rule3 tensor.

A concrete next target is a **shared bounded local feature encoding**: identify
which existing retained matter/apparatus variables encode the candidate
features, prove their domain survives evolution, and compile reversible
comparison/routing with explicit timing and history. A proposal must retain
the loser and show a causal effect on later local structure. It must also
share the existing ledger rather than append these four experimental slots.
Its first negative controls should be out-of-domain input, nonzero retained
history, ties, disconnected feedback and periodic recurrence. General
irreversible `argmax`, host clipping or resetting a response after a useful
sample is not an admissible solution.
