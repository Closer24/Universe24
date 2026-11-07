# Algebraic degrees of freedom and coupling families

**Status:** the reference engine implements the fixed body-action choice
`m=(0,1,3)` with eight sign triples. The broader axial-action family below is a
separate algebraic candidate, not an implemented or simulated extension. This
document changes no engine, coupling, preparation or recorded result.

## State, preparation and structural choices

For a periodic cube of side `L >= 3`, let `N_c=48 L^3` be the number of channel
addresses. The complete state space is

`(Z^2 × Z_6)^(N_c) ≅ Z^(96 L^3) × (Z_6)^(48 L^3)`.

Each remainder uses its representative in `{0,...,5}`. These are discrete
coordinate counts: 96 L³ unbounded integer counters and 48 L³ six-valued
remainders. They are neither continuous dimensions nor a finite bit budget.
Writing `r=2 theta+epsilon` adds no fields: `epsilon=r mod 2` is fixed by the
initial state and invariant under Rule3; `theta` has three possible values in
each parity sector.

An initial preparation chooses those triples, including source amplitudes,
phases, positions and apparatus patterns. `L` chooses the board geometry. One
global coupling tensor is a separate structural choice fixed before the run.
The observation definitions and run horizon determine what is measured and
saved; they supply no additional dynamical operation. The group `G=2O`, its 48
channel labels, six spatial directions and scalar Rule3 remain fixed here.

## Current implementation and proposed family

Let `Q_x,Q_y,Q_z` be the same chosen lifts used by the reference algebra for
positive quarter-turns about the coordinate axes. They satisfy `Q_i^4=z=-1` and `Q_i^8=1`. Introduce exponent
parameters `m=(m_x,m_y,m_z) in (Z/8Z)^3`; `m` is used instead of the wavevector
symbol `k`. For each axis `i`, define

`B_(+e_i)=Q_i^(m_i),  B_(-e_i)=B_(+e_i)^(-1)`.

Choose three signs `s_i in {-1,+1}`, shared by both orientations of their body
axis. For a receiving channel `g` and world direction `d`, set

`v=R(g)^(-1)d,  f_d(g)=g B_v,  w_d(g)=s_axis(v)`.

The full tensor is `P[d,g,h]=w_d(g)` when `h=f_d(g)`, and zero otherwise. It
contains six 48×48 signed permutation matrices, with negative directions given
by transposes. The three exponents are parameters generating that tensor, not
three tensor entries or freely adjustable weights for every channel.

| Scope | Exponents | Sign choices | Distinct labeled tensors |
| --- | --- | --- | --- |
| Current reference implementation | Fixed `(0,1,3)` | 8 | 8 signed tensors |
| Proposed axial-action family, ignoring signs | 512 triples | All positive | 512 port tensors |
| Proposed axial-action family, including signs | 512 triples | 8 per triple | 4096 signed tensors |

These counts precede any equivalence under relabeling or symmetry; they are not
counts of physically inequivalent models. This axial-action family is not an
exhaustive classification of all reciprocal six-port tensors. At `g=1` and `d=+e_i`, the destination
is `Q_i^(m_i)` and the weight is `s_i`. Since each generator has order eight,
these entries recover every exponent and sign, proving the labeled counts.

The current code hard-codes the actions and accepts only `body_signs`;
configuration accepts `coupling_signs`, not exponents or arbitrary matrices.
See [coupling.py](../universe24/core/coupling.py) and
[config.py](../universe24/experiments/config.py). Neither Rule3 nor the group
alone selects `(0,1,3)` as physically necessary.

## Why the candidate retains the stated algebraic structure

Every `B_v` rotates about its own axis, so `R(B_v)v=v`. If `h=f_d(g)=g B_v`,
the reverse body direction is

`R(h)^(-1)(-d) = R(B_v)^(-1)(-v) = -v`.

Consequently `f_(-d)(h)=h B_(-v)=g`, with the same sign. Thus `f_(-d)` is the
inverse permutation of `f_d`, proving one nonzero entry in every row and
column, reciprocity `P[-d]=P[d]^T`, and six retained spatial inputs.

For any `p in G`, simultaneously transform position by `R(p)` and channel
`g` to `p g`. Then `R(p g)^(-1)R(p)d=v`, hence
`f_(R(p)d)(p g)=p f_d(g)` with unchanged weight. This proves proper cubic
covariance for this family, not covariance under rotating positions alone.
It is a discrete algebraic symmetry, not continuous rotational invariance or
a physical spin derivation.

Full-state inversion has a more general reason. With the fixed integer input
map `u=F(b)`, recover from `(a',b',r')`:

`b=a',  u=F(a'),  r=(r'-2u) mod 6,  a=(2u+r-r')/6-b'`.

The numerator is divisible by six, giving an exact integer inverse. This
argument requires a known input map of the old `b` values; it does not require
reciprocity. The reference engine's scatter implementation and its equivalent
receiver-sum expression do use the reciprocal coupling construction.

## Central lift, scope and assembly

Exponents must not be reduced modulo four: `Q_i^(m_i+4)=z Q_i^(m_i)`. For
example, exponents 3 and 7 give the same spatial rotation but different sender
channels in the retained 48-label state. The central permutation `g -> g z`
does not negate a counter and is not interchangeable with a negative weight.

The baseline's reflection audit, graph connectivity, numerical behavior and
component performance are not inherited by this wider family. Those claims
need separate proofs or experiments. No implementation, simulation or physical
validation of the broader family is claimed here. A tensor or spinorial
representation by itself establishes no light, particle, measurement or
gravity mechanism.

An assembly must use one common, compatible tensor throughout its board.
A single shared tensor and nonconflicting initial triples establish a valid
preparation; they do not prove that assembled components retain their intended
behavior. A change of body actions belongs to an explicitly named candidate
with its own provenance and tests. The [reference contract](../AGENTS.md) and
[current model](MODEL.md) remain unchanged.
