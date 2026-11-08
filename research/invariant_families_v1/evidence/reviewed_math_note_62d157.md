# Exact invariant families inside the unchanged Rule3

Status: mathematical derivation and static coupling checks. The primitive is
always `divmod(2*u+r,6)`, followed by `a_next=b`, `b_next=ell-a`.
All inputs come from the same previous board. No coefficient field, engine
change or runtime input is introduced. The earlier heterogeneous-ratio
proposal is not selected for this task.

An effective ratio below describes a closed **homogeneous scalar recurrence**
encoded by a fixed full-board pattern. It does not yet describe an arbitrary
spatial field, a localized body, a physical particle or a selectable route.
The constructions provide infinitely many exact preparations, not evidence
that such preparations arise generically.

## Actual coupling convention

Write F for the implemented six-input operator, with rows receiving channels
and columns sending channels. For world direction d and receiving channel g,
the code transforms d into body coordinates by `R(g)^T d`, then uses the
corresponding right action on g. The body actions are

```text
I, I, q_y, q_y^-1, q_z^3, q_z^-3,
```

with the fixed signs `(sigma_x,sigma_y,sigma_z)`. This is the existing
`universe24/core/coupling.py` convention, not a freely chosen matrix.
At spatially constant fields, summing world directions enumerates every body
direction exactly once. Thus

```text
F0 = 2 sigma_x I
   + sigma_y [T(q_y) + T(q_y^-1)]
   + sigma_z [T(q_z^3) + T(q_z^-3)],
(T(h)v)(g) = v(g h).
```

## Exact sign conjugacy, including every remainder

For `epsilon = r mod 2`, define

```text
j(r) = 4-r+2 epsilon,
J(a,b,r) = (-a,-b,j(r)).
```

The even residues are exchanged as `0 <-> 4`, with 2 fixed; the odd residues
as `1 <-> 5`, with 3 fixed. Therefore j maps `0..5` to itself and is an
involution. If `2u+r = 6 ell+r_next`, then r_next has the same parity as r,
and

```text
-2u+j(r) = -6 ell+j(r_next).
```

The last term is already the valid Euclidean remainder. Consequently the
negative-input quotient is exactly `-ell`, and

```text
Rule3(J(a,b,r), -u) = J(Rule3((a,b,r), u)).
```

This is an all-integer identity, including negative u and either remainder
parity. Keeping a common arbitrary remainder on positive and negative sites
would not give this conjugacy. For example, at `lambda=4`, `a=0,b=1,r=0`,
the positive quotient is 1, whereas a negative site incorrectly initialized
with r=0 has quotient -2. Its correct conjugate remainder is 4 and gives -1.
The special initial residues 2 and 3 are self-conjugate.

## Ternary eigenpattern theorem

Choose a fixed pattern v over every site/channel address such that

```text
v_i in {-1,0,1},       F v = lambda v.
```

For one scalar triple `(a,b,r)`, define the entire board by

| Pattern value | Stored triple |
| --- | --- |
| +1 | `(a,b,r)` |
| -1 | `J(a,b,r)` |
| 0 | `(0,0,r_bg_i)`, with any fixed `r_bg_i in 0..5` |

Then `u_i = lambda v_i b`. Positive addresses execute

```text
ell, r_next = divmod(2 lambda b+r,6),
a_next = b,
b_next = ell-a.                         (Phi_lambda)
```

Negative addresses execute its exact J conjugate. At zero-pattern addresses,
the **total** input is zero, their counters remain zero, and their chosen
remainders stay unchanged. Individual terms there may be nonzero and cancel;
these are not isolated passive halos under the stronger QuietClock contract.
This proves full-state closure for every scalar integer a,b, all six r and
every time, without a growing initial-amplitude requirement. The encoding is
injective whenever v has a nonzero entry, and it intertwines one scalar step
with one unchanged native step.

Zero-pattern remainders are retained physical state coordinates of this
mathematical model, not deleted addresses. They do not feed the current input
operator while their counters remain zero.

## Verified patterns and precise effective ratios

For +++ and equal values in all 48 channels, F reduces to ordinary six-neighbor
addition. With periodic boundary conditions, the following identities follow
at every address, including the zero-pattern sites.

| Preparation | Required domain | Eigenvalue lambda | Scalar coefficient alpha_eff = lambda/6 |
| --- | --- | --- | --- |
| Uniform `v=1` | Any supported periodic side | 6 | 1 |
| `v(x,y,z,g)=(1,-1,0)[x mod 3]` | +++; side divisible by 3 | 3 | 1/2 |
| `v(x,y,z,g)=(1,0,-1,0)[x mod 4]` | +++; side divisible by 4 | 4 | 2/3 |
| `v_g=R(g)[1][1]` at every site | +++ | 4 | 2/3 |
| `v_g=R(g)[2][2]` at every site | +-+ | 4 | 2/3 |
| `v_g=R(g)[0][0]` at every site | +++ | 2 | 1/3 |

The last row is an additional exact nonlinear family, not a change to the
previous finite-duration internal-mode experiment. Under +-+, the y/y pattern
has eigenvalue **0**, not 4; the z/z pattern is the stated rotated preparation.

For the period-three profile, the two x-neighbor values sum to `-v`, while
the four transverse neighbors contribute `4v`, giving `3v`. For the
period-four profile, the x pair sums to zero, leaving `4v`. These are fixed
spatial standing patterns with a shared scalar amplitude. The uniform
lambda-6 family gives `b_next=2b-a`, which includes stationary and linearly
drifting counters; it is not generally an oscillating clock. The lambda-3
family gives `b_next=b-a`, with constant r and exact minimal period 6 for
every nonzero scalar counter pair. No universal period is asserted for the
lambda-4 or lambda-2 nonlinear families.

For the internal patterns, let `v_g=(R(g)e_j)_k`. Pairing the body rotations
gives

```text
[R(q_y)+R(q_y^-1)] w = 2 e_y e_y^T w,
[R(q_z^3)+R(q_z^-3)] w = 2 e_z e_z^T w.
```

Thus every world row k has

```text
lambda_j = 2 sigma_x
         + 2 sigma_y 1{j=y} + 2 sigma_z 1{j=z}.
```

Each matrix entry takes values +1 on eight channel labels, -1 on eight and
zero on 32. The 24 proper cube rotations send a chosen body axis to each of
the six signed world axes four times; each has two lifts among the 48 labels.
This proves the counts and explains the signed-control distinction without
guessing a channel permutation.

## What equivalence to a num/den family actually means

Reduce `lambda/6=p/q` for a positive eigenvalue. The separate general scalar
rule at a **spatially homogeneous scalar state** has neighbor sum `6b` and
remainder `rho in 0..6q-1`:

```text
ell, rho_next = divmod(12 p b+rho,6q).
```

Write `rho=q*r+h`, with `0<=r<6` and `0<=h<q`. Since `12p=2 lambda q`,

```text
12 p b+rho = q(2 lambda b+r)+h,
rho_next = q*r_next+h,
ell = floor((2 lambda b+r)/6).
```

Thus Phi_lambda is exactly the homogeneous scalar p/q recurrence in each
fixed remainder coset h, not merely a fitted frequency. A native experiment
covering six base remainders with fixed background tests one such coset.
It does not, by itself, test all `6q` generalized remainder states.

The complete generalized homogeneous domain can also be encoded: when the
ternary pattern has a zero address, fix one such address in advance and store
`r_bg=2+h` there for q=2 or 3, while other zero addresses retain their declared
background. This is static spectator storage. The zero input at that address
keeps h unchanged, making the full encoding injective in `(a,b,r,h)`. It must
be declared explicitly if implemented or tested; the proof is not evidence
that an undeclared native run exercised these extra sectors. For lambda=6,
q=1 and no extra storage is required.

No primitive channel has changed ratio in any of these constructions. The
embedding relates closed full-board preparations to a two-counter homogeneous
target map. It does **not** yet intertwine an arbitrary nonuniform spatial
p/q field, establish an effective continuum equation for a packet, or provide
independently localized modules.

## Relation to the earlier internal lambda-2 result

The earlier [internal-gap proof](internal_gap_algebra.md) used integer
quaternion-coordinate eigenvectors, including entries of magnitude 2. It
made every division exact for a declared finite horizon using amplitudes
proportional to `3^H`, obtaining a specified linear cosine recurrence.

The new rotation-entry eigenvector is ternary. It therefore closes under
Phi_2 with the J-encoded evolving remainders for all times and arbitrary
scalar amplitudes. Its finite-amplitude recurrence is generally nonlinear
because of Euclidean division. These are different statements: an exact
nonlinear scalar encoding does not imply an eternal unrounded cosine mode.
Naively multiplying the scalar counter pair by eigenvector entries of
magnitude 2 while retaining a common r=2 fails: with lambda=2 and b=1, the
v=1 quotient is 1 but the v=2 quotient is also 1, not 2. This example does not
rule out a different remainder encoding. The stated ternary and divisibility
hypotheses matter.

## Exact coexistence that is not an interaction

Let P be a counter-field solution satisfying `u_P=F b_P` divisible by 3 at
every address and every time, and

```text
a_P_next=b_P,       b_P_next=u_P/3-a_P.
```

For **any** native trajectory S under the same fixed coupling, prepare only
the initial sum of its counters with P and retain S's remainders:

```text
a_joint=a_S+a_P,    b_joint=b_S+b_P,    r_joint=r_S.
```

Since `2u_P` is divisible by 6, native divmod adds exactly `u_P/3` to S's
quotient and leaves S's remainder unchanged. Induction proves these identities
for every time. Nothing is added during evolution. This is an exact additive
solution symmetry, not a superposition principle for arbitrary Rule3 states.

The integer diagonal planar profiles in [the wave proof](coherent_wave_algebra.md)
have `u_P=3[f(s-1-t)+f(s+1-t)]` and satisfy this condition under +++.
The lambda-3 period-six counter families and uniform lambda-6 families also
qualify. Adding any of these to an internal pattern gives zero counter and
remainder interaction defect identically. Such a demonstration establishes
coexistence, but cannot establish signal activation of the residual S.
The arithmetic potential class `u mod 3` is unchanged by the added input;
actual guarded C presence can change through the quotient or changed-triple
guard. A changed passive event list alone would not contradict decoupling.

## A prospective interaction test with a known first-step prediction

Two lambda-4 preparations need not have that additive property. Choose two
verified ternary eigenpatterns under the same +++ tensor, prepare four masks
with initial a=0, b equal to neither/first/second/both patterns, and set every
initial remainder to 2. Because j(2)=2, each singleton is a valid invariant
preparation and all four masks have identical remainders.

At an address with both pattern values +1, each singleton has `u=4`, quotient
1 and next remainder 4; their joint input is 8, giving quotient 3 and next
remainder 0. The first-step counter-additivity defect is therefore +1. At a
double -1 address it is -1. Spatial x/y period-four modes, or internal and
spatial lambda-4 modes, provide explicit such overlaps. This predicts a native
nonlinear carry from immutable initial data, not an added force or gate.

Counter addition is an explicitly declared preparation of one joint board,
not permission to overwrite conflicting full-state component patches. A
generic constructor must either produce the complete joint preparation under
this declared operation or reject incompatible assignments. Two opposite
patterns whose counters cancel already in the initial state do not encode
two recoverable source labels there; that is not dynamical information erasure.

No new trajectory is claimed by this proposed test. If implemented, it needs
a frozen complete-state observer, all four controls, full inverses and stated
boundaries. A nonzero defect would establish interaction in this prepared
family, not preferred complexity, binding, unique selection or physical mass.
Cutting these global patterns into local patches, placing arbitrary modules
alongside them, or summing arbitrary invariant families generally violates the
eigenpattern or remainder conditions. Those composition problems remain open.

## Verification identity

The source-only arithmetic and coupling checks are recorded separately under
`evidence/invariant_families_algebra/`. They contain no native forward or
inverse trajectories and do not modify the earlier frozen evidence. An
independent exact-matrix review is required alongside any later native
demonstration. The alleged earlier 48-run result has not been assumed here.
