# Fixed per-channel rational coefficients: separate candidate specification

Status: mathematical proposal only. No variant engine, preparation, recording or
Presenter support has been implemented. No baseline source or experiment changes.

Selection decision, 2026-11-08: this alternative is **unselected**. The project
continues with `num=den=1` in every channel. Effective ratios must be derived
from baseline patterns; no per-channel coefficient field is authorized for
implementation. The specification below is preserved as a mathematical
comparison, not as the next implementation step.

The current `universe24/core/rule3.py` exposes `forward(old, neighbor_sum)` and
hardcodes `divmod(2*neighbor_sum+old.r,6)`. The independent reference implements
the same arithmetic. Neither has a general num/den parameter. The proposal below
must therefore not be described as an existing configurable baseline option.

The linked research document already specifies the general normalized Rule3
formula in sections H1/A2: the numerator is `2*num*Sum6+r`, the denominator and
remainder modulus are `6*den`, and the old counter is subtracted after taking
the quotient. Its H1 comparison uses spatially uniform ratios in separate
scalar systems. The strict H1a/A2 appendix fixes `num=den=1` and explicitly says
that no channel chooses a different ratio. The live document was checked on
2026-11-08; its reported modification time was 2026-11-07T13:47:08.362Z.

Thus the algebraic placement below agrees with the document's existing general
scalar rule. The new proposal is a heterogeneous, fixed per-channel coefficient
field on the 48-channel model, outside the implemented strict baseline. The
document's older 8192-site, 600-step, eight-run comparison table has not been
replayed or independently verified in this session and is not evidence for
this proposed extension. Source: [Universe24 research document](https://docs.google.com/document/d/1NDPfeFj9vldgb0RMSSvx2lBSmOo__E-F3t2cZwfjOjI/edit),
sections H1, H1a and A2; live document identity and section alignment are recorded
in the [source alignment](document_alignment.md) and its
[read-only receipt](evidence/document_alignment/receipt.json), separately from
computational evidence.

## A precise candidate

Index a channel at a lattice site by i. Before evolution fix positive integers
`p_i,q_i`, preferably coprime to remove representational redundancy. The pair is
attached to that channel's entire `(a_i,b_i,r_i)` update, not independently to
the two quarter-turn coordinates a and b. Fix the same six-neighbor signed
coupling F and the complete coefficient field before the first update.

Define `M_i=6*q_i`, with channel state space
`a_i,b_i in Z` and `0 <= r_i < M_i`. Extending the document's normalized scalar
rule to this declared fixed field gives

```text
u_i = F(b)_i,
ell_i,r_i_next = divmod(2*p_i*u_i+r_i, 6*q_i),
a_i_next = b_i,
b_i_next = ell_i-a_i.
```

All channels read the same old snapshot. The heterogeneous field is a proposed
model extension; it is not an existing baseline API. There are other
inequivalent ways to insert a ratio, which are not the document's stated rule.
For example, multiplying
the full numerator including r, or rounding p*u/q before applying the baseline
formula, defines a different map and needs a separate invertibility analysis.

Setting every p_i=q_i=1 gives the existing scalar update and state domain
exactly. Holding p_i,q_i fixed at initialization avoids runtime coefficient
changes, but still changes the current mathematical contract when any differs
from1. The extra immutable field and enlarged remainder domains are essential
parts of this candidate's specification and checkpoint identity.

For q_i=1, an integer p_i can algebraically be absorbed into the recipient
row weights of a different coupling map: define `F_tilde_ij=p_i*F_ij`, then
the scalar expression is again `divmod(2*(F_tilde*b)_i+r_i,6)`. This does not
make it an allowed option in the current eight signed-unit templates, whose
weights are only+1 or−1. A heterogeneous row scaling also generally breaks
reciprocal weights. Such weighted couplings would be another explicitly
authorized coupling family, not a reinterpretation of the present TensorSpec.
For q_i>1 the proposed modulus6q_i changes the remainder domain itself; it
cannot be hidden as a choice within the current r0..5 state representation.

Effective period or transport ratios assembled from baseline clocks are a
separate behavioral question. They may change without changing any primitive
coefficient. They must be demonstrated across a declared family and must not
be reported as evidence that an individual baseline counter selected p_i/q_i.

## Exact inverse and locality

Given the complete new state and the same fixed coefficient/coupling fields,
the old b field is the new a field. Therefore calculate

```text
u_i_old = F(a_next)_i,
k_i = 2*p_i*u_i_old,
r_i_old = (r_i_next-k_i) mod M_i,
ell_i = (k_i+r_i_old-r_i_next)/M_i,
a_i_old = ell_i-b_i_next,
b_i_old = a_i_next.
```

The quotient is an integer because of the modular reconstruction. Euclidean
uniqueness puts the recovered r in its declared range, and substituting back
recovers the new triple. Conversely applying this formula to a forward update
recovers the exact old triple. This proves a full-board bijection for every
state in the product of these channel domains. No invertibility of F is needed:
the old b values are already available as new a. The inverse and forward maps
both use only the fixed six-neighbor field and the local coefficient.

As in the baseline, a disturbance cannot affect a site beyond one lattice edge
per synchronous update. This causal upper bound does not establish a physical
light cone, a universal observed speed, a mass or Lorentz symmetry.

## Residue sectors and measured gains

The identity `r_i_next-r_i = 2*p_i*u_i-6*q_i*ell_i` implies invariance of
`r_i mod gcd(2*p_i,6*q_i)`. Let this gcd be g_i. Writing `r_i=g_i*s_i+h_i`
with `0 <= h_i < g_i` removes h_i from the quotient and s evolution, so h_i
is a spectator sector. It must remain in the reversible full state, but does
not by itself define an observable physical property or a new behavior.

If a common factor c divides both p and q, writing r=c*r_bar+h similarly
shows that the unreduced ratio is the reduced dynamics plus c spectator sectors.
Thus equal rational values represented by different integer pairs are not
literally identical full state spaces. Requiring coprime pairs gives a canonical
specification; it does not remove the baseline's own parity spectator.

For a fixed channel over T updates, exact telescoping gives

```text
6*q_i * sum(ell_i) = 2*p_i * sum(u_i) + r_i_initial-r_i_final,
|sum(ell_i) - p_i/(3*q_i)*sum(u_i)| <= 1 - g_i/(6*q_i).
```

The endpoint difference bound uses the fixed residue sector: its largest
possible absolute remainder difference is M_i-g_i. If summed input is nonzero,
divide this bound by its absolute value to bound the signed accumulated gain.
The measured gain approaches p_i/(3*q_i) only when that absolute accumulated
input becomes unbounded. Long duration with canceling input is insufficient.
Counts of C events, component periods, packet velocities and detection rates
are different observables and do not follow from this gain identity.

The baseline's simple global algebraic account also does not automatically
survive. Define the corresponding local account
`A_i=6*q_i*(b_i-a_i)+(r_i-r_i_background)`. Its exact update is
`Delta A_i=2*p_i*u_i-12*q_i*b_i`. Even for uniform p,q with +++ reciprocal
coupling, summing gives `Delta sum(A)=12*(p-q)*sum(b)`, generally nonzero.
For a weighted account `sum_i lambda_i*A_i`, conservation for all states
requires `sum_i lambda_i*p_i*F_ij=6*lambda_j*q_j` at every j. This is a
new algebraic condition to prove or disprove, not a physical conservation law.

The silent-quarter-turn obstruction remains unchanged: if every quotient on
the complete board is zero for four consecutive updates, the two counters
return by their quarter-turn rotation, every fixed linear input sums to zero
over those updates, and each remainder changes by `2*p_i*sum_t u_i=0`.
The complete state therefore recurs after four updates. Static p/q fields do
not allow prolonged exploration with all quotients zero. Absence of guarded
C alone remains a different, weaker condition.

The old arithmetic class formula, if separately retained for this candidate,
would give `((r_next-r)//2) mod3 = p_i*u_i mod3` under the same nonzero-quotient
and changed-triple guard. In particular, p_i divisible by3 forces every guarded
event into class0. That change in label frequencies would be arithmetic, not
evidence of unique-route choice. Baseline observers and Presenter validation
currently assume remainders0..5 and the baseline rule; their compatibility with
this candidate must not be asserted or silently bypassed.

## Fixed lattice medium versus a transported object

Two exact uniform-field examples illustrate the candidate's consequences
without implementing it. If every site and channel has the same a,b and valid
r, then +++ input is u=6b. For p/q=1/2 the proposed modulus is12, so ell=b,
the remainder stays fixed, and `(a,b)->(b,b-a)`. The third iterate negates the
pair and the sixth is the identity; every nonzero integer pair has minimal
period6. For p/q=2/1, ell=4b and `(a,b)->(b,4b-a)` instead has characteristic
roots `2+sqrt(3)` and `2-sqrt(3)` and permits exponential growth. Both examples
are statements about the proposed spatially uniform full-field candidate,
not native baseline runs, localized clocks, or identifications of mass.

By contrast, a genuinely zero-input center still has ell0 for every valid
p,q and remainder, so it follows the same quarter-turn period4. Assigning a
different fixed ratio does not by itself change that isolated free clock's
period. The period6 example above is a uniformly interacting whole field with
u=6b, not a disconnected scalar clock whose rate was independently set.

Here p_i,q_i are attached to lattice addresses. A moving pattern encounters
different coefficients as it moves through an inhomogeneous field. This is a
prepared medium and may introduce preferred locations and directions. Generic
heterogeneous fields break translation symmetry. Channel-dependent fields can
also break rotation symmetry unless their transformation is included in the
symmetry statement. A uniform field is a cleaner first mathematical comparison.

Attaching coefficients to a moving object instead would require an additional
transport law or a derivation of a pattern-dependent effective response within
unchanged dynamics. Neither is supplied by this fixed-field proposal. In
particular, setting p/q is not a definition of mass. Massless/massive claims
require independently identified propagating patterns, dispersion and invariant
relations across preparations and motion, with fixed detector readouts and
quantified error. Different periods or speeds in a prepared medium are not
sufficient.

## Required review decisions before implementation

1. Accept or reject this exact placement of p and q in the arithmetic, separately
   from the all1 baseline. Specify coefficient bounds, full remainder domains,
   coefficient-field storage, and whether only uniform fields are first allowed.
2. Test exact all1 equivalence, signed/large-integer scalar inverses, mixed-field
   synchronous full-board inverse, residue sectors and full-state checkpoints.
   An independent oracle must reconstruct the proposal rather than import its
   scalar function or generated coupling tables as expected answers.
3. Register homogeneous ratios first, with matched initial preparations and
   multiple sizes, then heterogeneous interfaces if justified. Preserve all
   failures and complete states. Fix response observables and controls before
   evolution; do not tune labels after seeing the output.
4. Treat internally increasing complexity as another hypothesis. No term above
   selects a high-complexity branch, erases alternatives, produces quantum
   probabilities or supplies an evolutionary fitness function. Any such claim
   needs a fixed measurable mechanism and null comparisons, including information
   retained elsewhere in the invertible state.

This candidate remains outside all frozen baseline studies in this session.
