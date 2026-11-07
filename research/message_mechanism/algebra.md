# Message, cancellation, and carrier algebra

Research base: `0d4c4805be67b0efc42e084416ff2204529a1e07`, 7 November 2026.
Scope: the existing one-board, 48-channel Rule3 model, with the fixed tensor
chosen before evolution. No engine changes or runtime interventions are
proposed here. “Signal” denotes a transported mathematical pattern, not yet
physical light. The results below separate exact identities, conditional local
input contracts, complete-board proofs, and finite checks.

## 1. The exact state and what a quiet record can do

For a channel with old state `(a,b,r)` and its **actual** neighbor sum `u`,

```text
ell, r_next = divmod(2*u + r, 6)
a_next = b
b_next = ell - a
```

Every address has a conserved remainder parity `epsilon = r mod 2`.
Writing `r=2*theta+epsilon`, the exact phase equation is

```text
theta_next = (theta + u) mod 3.
```

Thus the remainder provides three phase positions in each parity sector. It
is neither a click counter nor a statement that every phase change is a click.
The current passive arithmetic event C requires both `ell != 0` and a change
of the complete triple.

**Proof: quiet integration from zero counters.** Suppose `a_0=b_0=0` and no
guarded C occurs through update T. A first nonzero quotient would produce a
nonzero new `b`, changing the triple and therefore producing C. Induction
gives `ell_t=0`, `a_t=b_t=0`, and

```text
r_t = r_0 + 2*U_t,       U_t = sum(u_j, j=0,...,t-1).
```

Every prefix must satisfy `0 <= r_0+2*U_t <= 5`. For even preparations:

| Initial remainder | Permitted cumulative input while C-free |
| --- | --- |
| 0 | `U_t` in `{0,1,2}` |
| 2 | `U_t` in `{-1,0,1}` |
| 4 | `U_t` in `{-2,-1,0}` |

A complete zero-counter record is unchanged during a waiting update exactly
when its actual input is zero. The conclusion that C-free means zero quotient
depends on starting with zero counters: for example `(a,b)=(m,m)` with
`u=6m` is stationary even though `ell=2m` may be nonzero.

In general, without any quietness assumption,

```text
r_T-r_0 = 2*sum(u_t) - 6*sum(ell_t).
```

If the total signed input is zero, the endpoint remainder equals its initial
value: its difference is a multiple of six and lies between -5 and 5. The
counters can nevertheless retain a record. A receiver that must finish with
zero counters and a changed remainder cannot be written by a completed
zero-area waveform. This is an obstruction for that receiver contract, not
for every memory representation.

Remainder-only records do not emit a signal: neighbor sums read `b`, not `r`.
A quiet pending record therefore needs an incoming interrogation/approval
signal or an active surrounding apparatus to influence anything elsewhere.

## 2. Exact conditional write, wait, approve, and cancel

The following alphabet uses channels 0 and 14. Both counters start at zero.
The inputs in the table are requirements on an autonomous preparation; the
table does not supply those inputs to a running board.

| Stage, positive family | Actual input `(u0,u14)` | Channel 0 `(a,b,r)` | Channel 14 `(a,b,r)` | Quotients | C |
| --- | --- | --- | --- | --- | --- |
| Ready | — | `(0,0,2)` | `(0,0,4)` | — | — |
| Write pending | `(1,-1)` | `(0,0,4)` | `(0,0,2)` | `(0,0)` | None |
| Wait, any number of updates | `(0,0)` | `(0,0,4)` | `(0,0,2)` | `(0,0)` | None |
| Cancel, starting from pending | `(-1,1)` | `(0,0,2)` | `(0,0,4)` | `(0,0)` | None |
| Approve, starting from pending | `(1,-1)` | `(0,1,0)` | `(0,0,0)` | `(1,0)` | Channel 0 |

The equally valid negative family is obtained by exchanging the two named
channels and reversing the input pair:

| Stage, negative family | Actual input `(u0,u14)` | Remainder pair | Counter pairs `(a0,b0);(a14,b14)` | C |
| --- | --- | --- | --- | --- |
| Ready | — | `(4,2)` | `(0,0);(0,0)` | — |
| Write pending | `(-1,1)` | `(2,4)` | `(0,0);(0,0)` | None |
| Wait | `(0,0)` | `(2,4)` | `(0,0);(0,0)` | None |
| Cancel from pending | `(1,-1)` | `(4,2)` | `(0,0);(0,0)` | None |
| Approve from pending | `(-1,1)` | `(0,0)` | `(0,0);(0,1)` | Channel 14 |

These two local input contracts do not assert a symmetry that exchanges
arbitrary channels in an assembled board. Their realizability must be tested
using the actual tensor and all 48 receiver channels.

The confirmed channel, under subsequent actual zero input, follows

```text
(0,1) -> (1,0) -> (0,-1) -> (-1,0) -> (0,1),   r=0.
```

Its readout `I=a*a+b*b=1` is constant. Its full state is not stationary, and
its nonzero counters send signals to neighbors. Consequently an assumed
indefinitely zero incoming sum needs a complete-board construction; it does
not follow from this local four-cycle.

### Cancellation witnesses and resetting

Returning the receiver to Ready makes “canceled” and “never pending” locally
indistinguishable. If the application needs to distinguish them, it must
retain a witness elsewhere in the same state. For example, a third
zero-counter channel initially at `r=2` would change to `r=4` without C if
the cancellation message also supplied actual input `+1` to it. The triple
input `(-1,+1,+1)` therefore gives an exact conditional positive-family
cancellation-and-witness contract. No autonomous source for this vector is
established by that calculation.

Cancellation of a pending remainder record is different from cancellation
after approval. Immediately after positive approval, applying `(-1,+1)`
produces channel 0 `(1,-1,4)` with `I0=2` and C, and channel 14 `(0,0,2)`.
It does not restore Ready.

A stale or duplicate cancellation also has different behavior: applying
`(-1,+1)` to the positive-family Ready pair `(2,4)` produces remainder pair
`(0,0)` and channel-14 counter `(0,1)`, with C. The same waveform is therefore
not a universally safe CANCEL command. Its meaning depends on the receiver
state, its phase, and the permitted input history. A successful component
must demonstrate that its ordinary signal-producing apparatus obeys that
input contract; an observer cannot enforce it by suppressing messages.

More generally, resetting a channel `(a,b,r)` to a specified zero-counter
triple `(0,0,s)` in **one** forward update is possible exactly when

```text
b = 0,     s = r (mod 2),     u = 3*a + (s-r)/2.
```

This follows from `a_next=b=0`, `ell=a`, and `2u+r=6a+s`.
Thus a reset waveform is phase-sensitive and must be generated internally.
Negating the last message is not a general inverse operation for the full
receiver. The available inverse executor remains an audit tool only.

## 3. A minimal converter and a useful phase obstruction

Let `v=(a,b)`, `R(a,b)=(b,-a)`, and `e=(0,1)`. Exact counter evolution is

```text
v_T = R^T v_0 + sum(R^(T-1-t) e * ell_t, t=0,...,T-1).
```

This identifies the information discarded by looking only at remainders.
For actual zero input the quotient is zero, and the counter phase rotates
with period dividing four. `I=a*a+b*b` is then invariant; generally
`I_next-I = ell*ell - 2*a*ell`. This is not a physical energy claim.

**Conditional converter construction.** Consider one zero-counter address
whose first packet lobe is `q=+1` or `q=-1`. Background remainder 2 admits
that first lobe without C. Changing only the initial remainder to
`r=2+2q` gives `ell=q` and `b_next=q` at the first arrival. This is a
single-address, initial-data converter: its outgoing effect is generated by
Rule3, not by an external switch.

For the prescribed input sequence `q`, then `k` zero-input updates, then
`-q`, the two nonzero quotients are `q,-q`. The remainder returns to
`2+2q`, while

```text
v_final = q * (R^(k+1)e - e).
```

| `k mod 4` | Final counters | Final `I` |
| --- | --- | --- |
| 0 | `(q,-q)` | 2 |
| 1 | `(0,-2q)` | 4 |
| 2 | `(-q,-q)` | 2 |
| 3 | `(0,0)` | 0 |

Balanced input can therefore leave a counter record or cancel completely
depending on lobe separation. The existing compact packet supplies opposite
lobes separated by one quiet update at an unmodified traversed address. It
motivates the `k=1` converter preparation, but once the converter becomes
active its feedback can change the actual later input. The table alone is
not an autonomous memory proof.

A concrete side-branch candidate is one transverse halo channel of the
guided packet. The tensor's port and weight determine its signed first
lobe `q`; prepare that channel with remainder `2+2q` instead of 2. At the
first arrival its nonzero counter sends a signal through the existing six
connections. Its earliest feedback to the row is one further update. It
does not add a connection or change the tensor. All other channels and
remainder-only halo changes must remain in the simulated state.

### Complementary-pair symmetry

For even remainders, if two channels have states

```text
(a,b,r),       (-a,-b,4-r)
```

and actual inputs `u,-u`, they retain that relation after the update.
Indeed, writing `2u+r=6ell+s`, the other numerator is
`4-(2u+r)=-6ell+(4-s)`, with `s` and `4-s` in `{0,2,4}`.

The prepared guide pairs `(0,4)`, `(2,2)`, and `(4,0)` lie in this
complementary sector. A converter search that needs to break this symmetry
should include `(0,0)`, `(0,2)`, `(2,0)`, `(2,4)`, `(4,2)`, and `(4,4)`.
This is a search partition, not a proof that a complementary converter
cannot scatter or retain information. Opposite inputs also have to be
verified; arbitrary neighboring defects can break their relation.

### A confined translating front cannot leave a different guide phase

**Narrow exact obstruction.** Consider an infinite identity-channel X row
under positive X coupling, with no active transverse input. Suppose its
counters have finite support, its far-left and far-right states have zero
counters and constant remainders `r_minus,r_plus`, and one update translates
the complete profile by one site in +X. Write `delta=r_plus-r_minus`.

The translation conditions imply

```text
b_x = a_(x-1)
ell_x = a_(x-2) + a_x = u_x
r_x-r_(x-1) = 4*(a_(x-2)+a_x).
```

Summing over X gives `delta=8*sum(a_x)`. Since valid endpoint remainders
differ by at most five, the only possible value is `delta=0`. In particular,
a confined unit-speed front cannot connect guide remainders 0 and 4, or 2
and 4. Applying the argument to both opposite-counter channels does not
remove it merely because their total remainder changes would cancel.

The obstruction also holds for an internally periodic profile advancing
**one site after p updates**, provided counters have finite support at every
phase and transverse input vanishes throughout the period. To see this,
let `B=sum_t,x b_t(x)` over one period. Spatial translation preserves total
endpoint a and b; summing `a_next=b` and `b_next=ell-a` gives
`sum_t,x a_t=B` and `sum_t,x ell_t=2B`. Summed row input is `2B`, whereas
the total remainder change from the one-site advance is `-delta`.
Therefore `-delta=4B-12B=-8B`, again forcing `delta=0`.

More generally, if a profile advances q sites per period and the cumulative
incoming transverse sum is W, the same calculation gives

```text
q*delta = 8*B - 2*W.
```

For one-site advance a remainder jump of magnitude two requires nonzero
transverse input area modulo four; a magnitude-four jump requires
`W = 2 (mod 4)`. These are necessary conditions, not sufficient constructions.
Other signed X couplings change the coefficient of B; they do not rescue
the confined one-site front: for X sign s it is `(12-4s)*B`.

This theorem concerns the stated row ansatz. A periodic finite board cannot
contain a single isolated kink without a second interface. The calculation
can constrain a finite-window, isolated-interface construction with stationary
far fields, but it does not rule out active transverse converters, more
general multichannel motion, multiple-site advance, extended counter tails,
or nontranslating scatterers. In particular, merely lengthening a confined
row pulse does not solve this phase-front problem.

### Reverse-designed preparations

An allowed external search can specify a complete endpoint containing an
outgoing proved packet and a spatially separated zero-counter remainder
record, then use exact inverse evolution to propose an initial preparation.
Only the proposed initial state is supplied to the actual forward experiment.
Source-off controls retain all its remainders and remove the declared initial
source counters. The receiver, its desired record, source region, exclusion
distance, and acceptance window must be fixed before evaluating candidates.

At the specified endpoint, the remainder defect alone is stationary. If it
does not intersect the outgoing packet's complete row/halo influence during
the next eight updates, the defect stays quiet throughout those updates by
locality and the proved translation identity. The full state must still be
verified: this argument cannot omit a halo address or ignore periodic return.
What remains uncertain is whether backward scattering produces an earlier
admissible idle receiver with a different remainder and suitably localized
source counters. An inverse-designed endpoint is a search constraint, not
evidence that that earlier interface exists.

## 4. Exact full-board phase and time-reversal symmetries

These identities apply to every state under each of the eight fixed signed
tensors. At each address let `c=4+2*(r mod 2)` and define

```text
K(a,b,r) = (-a,-b,c-r)
J(a,b,r) = (b,a,c-r).
```

Both are involutions and preserve valid remainders. If F is the complete
synchronous forward map, then

```text
F K = K F,             F J F = J,             F J = J F^-1.
```

**Proof for K.** Its counter negation negates every actual signed neighbor
sum. If `2u+r=6ell+s`, then the transformed numerator is
`c-(2u+r)=-6ell+(c-s)` with valid remainder `c-s`. The new counters and
remainder are exactly K of the original new triple.

**Proof for J.** In `J F(S)`, the b-counter at every address equals the
original b-counter of S. Consequently its actual neighbor sum is again u.
If the first update has remainder s and quotient ell, its next numerator is
`2u+c-s=6ell+c-r`. The next quotient is ell and its next state is
`(b,a,c-r)=J(S)`. This uses the same complete old snapshot at every step.
The identity is already represented by
[`time_reverse`](../../universe24/observation/diagnostics.py); it introduces
no new runtime primitive.

If an exact prepared pattern satisfies `F(S)=T_x(S)`, J commutes with spatial
translation and therefore `F(J(S))=T_x^-1(J(S))`. An opposite-moving packet
can be prepared by applying J to **all** its initial counters, guide
remainders, and retained halo. Its subsequent evolution uses forward F only.

For the [proved positive-X packet](../component_review/packet_proof_review.md),
the channel-0 preparation transforms as follows:

| Local X | Original `(a,b,r)` | J-transformed `(a,b,r)` |
| --- | --- | --- |
| 0 | `(1,0,4)` | `(0,1,0)` |
| 1 | `(0,1,4)` | `(1,0,0)` |
| 2 | `(-1,0,4)` | `(0,-1,0)` |
| 3 | `(0,-1,4)` | `(-1,0,0)` |
| Other guide positions | `(0,0,0)` | `(0,0,4)` |

The full guide pair becomes `(4,0)`, and every even halo remainder becomes
`4-r`; background 2 remains 2. Channel 14 must also be transformed. This
proves the translated carrier on the full complementary guide for the same
scope as the original packet, signs `(+,+,+)` and every `L>=5`. Joining
positive and negative guides at a seam is a new interaction preparation;
neither packet proof establishes the seam's behavior.

## 5. Information accounting and exact impossibility statements

### No global absorption into a fixed state or an existing finite cycle

**Proof.** The complete Rule3 map F is invertible. If a full state P is fixed
and `F^T(S)=P`, then `S=F^-T(P)=P`. A different whole-board state cannot
arrive at P in finite time. More generally, if P belongs to a finite cycle,
every predecessor is on that same cycle. There is no attracting basin into
that exact full-state cycle from outside it.

This permits a local region to become quiet while information travels or
continues evolving elsewhere. It also permits two different global states
to have identical receiver readouts. It forbids interpreting local
cancellation as deletion of the distinction from the entire closed state.
Unbounded counters mean this argument should not be replaced by an
unsupported assertion that every trajectory eventually recurs.

### Signed account

For `q_i=6*(b_i-a_i)+r_i-r_background`, direct substitution gives

```text
q_i(next)-q_i = 2*u_i - 12*b_i.
```

Each source has signed degree `2*(s_x+s_y+s_z)`, so on the periodic board

```text
Q_next-Q = 4*(s_x+s_y+s_z-3)*sum(b_i),     Q=sum(q_i).
```

Thus Q is conserved for the `(+,+,+)` tensor. It is generally not conserved
for the other signed tensors. This restates the existing diagnostic account;
it is useful for complete-board converter audits and is not established
physical energy. A local converter's changing account must be reconciled
with the environment, even during zero incoming sums: nonzero local b can
continue to send outgoing influence.

## 6. Search decisions implied by the algebra

| Candidate or observation | Decision before attributing a mechanism |
| --- | --- |
| Zero-counter, C-free receiver with desired changed remainder | Require the exact nonzero signed input area and every prefix within the quiet interval. |
| Completed bipolar packet with zero area and zero endpoint counters | It cannot leave a changed remainder at that address; search a converter or a different record. |
| Boundary-remainder side branch | Permit C in the converter, retain every affected channel, and measure its actual outgoing waveform and feedback. |
| Two-lobe converter with separation `k=3 mod 4` | The conditional isolated response cancels; prioritize other phases when seeking a counter record. |
| Confirmed remainder pair `(0,0)` | Also require the intended full counter signature; channel-14 excitation is not channel-0 approval. |
| Restored Ready pair after cancellation | Require an independently specified witness if canceled and never-pending histories must be distinguished. |
| Two opposite-moving carriers | Transform the entire packet and its guide/halo; test their seam as a separate preparation. |
| Long locally quiet interval | Check full-state inversion and where the difference from controls remains; do not infer global erasure. |

The current baseline prospectively tests state 13 as the pending write and
states 14 through 21 as eight quiet retention updates. Its acceptance is a
pending-record result only. A complete approval/cancellation component also
needs distinct ordinary messages, a fixed response window, full receiver
predicates, retained records, and source-off controls in one autonomous
preparation. A complexity score cannot perform that selection from outside
the board. These calculations do not establish maximum-complexity selection,
physical light, wave-function collapse, entanglement, or a physical time arrow.

## 7. Finite regression evidence

An exact-integer inline check was run against the research-base engine with
Python's standard library; all assertions passed. No engine or model file
was changed. The all-state claims above rely on their algebraic proofs,
not on the finite ranges below.

| Check | Declared finite domain | Cases |
| --- | --- | --- |
| Scalar K, J, parity, and stationary-state equivalence | `a,b=-3..3`, `r=0..5`, `u=-12..12` | 7,350 |
| Quiet integration and balanced-input remainder return | Every length-six input word over `{-1,0,1}`, every initial remainder, zero counters | 4,374; 1,154 fully quiet words |
| Converter phase formula | `q` in `{-1,1}`, `k=0..15` | 32 |
| Complementary pair identity | `a,b=-3..3`, even remainder, `u=-12..12` | 3,675 |
| One-update reset equivalence | `a,b=-3..3`, old/target remainder `0..5`, `u=-12..12` | 44,100 |
| Write/wait/cancel/approve tables | Both signed input families, eight quiet waiting updates and eight approved phase updates | 2 families |
| Full-board K, J, and inverse round-trip | All eight sign triples, backgrounds `r=0..5`, L3, four updates per preparation | 192 transitions |

The full-board regression used `Random(240711)`. For each sign/background
combination it drew 48 addresses independently and counters in `-4..4`,
remainders in `0..5`; coincident draws overwrite earlier draws, exactly as
ordinary dictionary construction. Transformations applied to both sparse
cells and the background. No incomplete-state projection was compared.

The following reproduces the scalar and converter assertions from the
repository root; the full-board test is a supplementary finite check of
the proved identities and is specified below it.

```python
from itertools import product
from universe24.core.state import Channel
from universe24.core.rule3 import forward

def c(r): return 4 + 2 * (r % 2)
def K(s): return Channel(-s.a, -s.b, c(s.r) - s.r)
def J(s): return Channel(s.b, s.a, c(s.r) - s.r)
def event(s, u):
    return bool((2*u+s.r)//6 and forward(s, u) != s)

for a, b, r, u in product(range(-3,4), range(-3,4), range(6), range(-12,13)):
    s = Channel(a,b,r)
    n = forward(s,u)
    assert forward(K(s),-u) == K(n)
    assert forward(J(n),u) == J(s)
    assert (n == s) == (a == b and u == 6*a)
    assert n.r % 2 == r % 2

for r, seq in product(range(6), product((-1,0,1), repeat=6)):
    s, area, quiet = Channel(0,0,r), 0, True
    for u in seq:
        quiet = quiet and not event(s,u)
        s, area = forward(s,u), area + u
        if quiet:
            assert s == Channel(0,0,r+2*area)
    if area == 0:
        assert s.r == r

for q, k in product((-1,1), range(16)):
    s = Channel(0,0,2+2*q)
    for u in (q,) + (0,)*k + (-q,):
        s = forward(s,u)
    expected = ((q,-q),(0,-2*q),(-q,-q),(0,0))[k % 4]
    assert s == Channel(*expected,2+2*q)

for a, b, r, u in product(range(-3,4), range(-3,4), (0,2,4), range(-12,13)):
    s, t = Channel(a,b,r), Channel(-a,-b,4-r)
    assert forward(t,-u) == K(forward(s,u))

for a,b,r,s,u in product(range(-3,4),range(-3,4),range(6),range(6),range(-12,13)):
    actual = forward(Channel(a,b,r),u) == Channel(0,0,s)
    condition = b == 0 and (s-r)%2 == 0 and 2*u == 6*a+s-r
    assert actual == condition

for remainders, inputs in (((2,4),(1,-1)),((4,2),(-1,1))):
    ready = tuple(Channel(0,0,r) for r in remainders)
    pending = tuple(forward(s,u) for s,u in zip(ready,inputs))
    assert tuple(s.r for s in pending) == tuple(reversed(remainders))
    assert all(s.a == s.b == 0 for s in pending)
    for _ in range(8):
        assert tuple(forward(s,0) for s in pending) == pending
    assert tuple(forward(s,-u) for s,u in zip(pending,inputs)) == ready
    approved = tuple(forward(s,u) for s,u in zip(pending,inputs))
    assert tuple(s.r for s in approved) == (0,0)
    expected = tuple(1 if u == 1 else 0 for u in inputs)
    assert tuple(s.b for s in approved) == expected
    for _ in range(8):
        assert tuple(s.a*s.a+s.b*s.b for s in approved) == expected
        approved = tuple(forward(s,0) for s in approved)
```

```python
from random import Random
from universe24.core.state import Cube, State
from universe24.core.coupling import Coupling
from universe24.core.engine import Engine

rng = Random(240711)
def transform(s, fun):
    return State(s.cube, fun(s.background),
                 {address: fun(value) for address, value in s.cells.items()})
def same(s,t):
    return (s.cube == t.cube and s.background == t.background
            and s.cells == t.cells)

for signs, bg in product(product((-1,1),repeat=3), range(6)):
    engine, cube = Engine(Coupling(signs)), Cube(3)
    cells = {
        (rng.randrange(3),rng.randrange(3),rng.randrange(3),rng.randrange(48)):
        Channel(rng.randrange(-4,5),rng.randrange(-4,5),rng.randrange(6))
        for _ in range(48)
    }
    state = State(cube, Channel(0,0,bg), cells)
    for _ in range(4):
        after = engine.advance(state)
        assert same(engine.advance(transform(state,K)),transform(after,K))
        assert same(engine.advance(transform(after,J)),transform(state,J))
        assert same(engine.rewind(after),state)
        state = after
```

Historical unsuccessful preparations and their retained evidence are
described in [the prior approval analysis](../light_approval/approval_mechanism.md).
The new computational studies must report their own frozen protocols and
complete-board results; this algebra note does not turn a proposed input
sequence into an observed device.
