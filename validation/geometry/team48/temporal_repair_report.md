# Projective positive frame: temporal and nondegeneracy repair

This is new model algebra and independent evidence for the proposal in issue
40, based on PR 42. It does not preserve the old sign-leapfrog trajectory and
is not an accepted production Einstein model. The generic implementation is
`refinement_integer_projective.py`; this review owns the independent sourced
control in `temporal_repair_projective.py`.

## Retained update and unchanged Engine

Use the 43 physical positive-frame fields and one common denominator channel:
44 channels, 132 integer entries per node, no computational phase. Write
`P_i/D = y_i`, and let `F_i(P,D)` be the degree-three homogenization of the
existing physical polynomial `f_i(y)`. The fixed integer multiplier `C`
clears coefficients of `h*f`; it is not an Engine divisor. The immutable
polynomial tensor implements

```
D_next   = C D^3 - D_old
P_i_next = C D^2 P_i + C h F_i(P,D) - P_i_old
```

by taking `u = 3*(the indicated polynomial before -old)`. Therefore the
Engine remains exactly `divmod(2*u+r,6)`, and all six remainder values remain
unchanged. Every monomial retains degree at most three and one-face support.
No old-a reads enter the tensor. The current uniform `D` is retained at each
node; its update is on-site, with no global reduction.

For prepared `D_old=0`, `D>=2` and `C>=2`, induction gives positive strictly
increasing denominators. Readout only uses the proved current `P/D` chart.
`D_old=0` is a declared memory boundary, not an earlier physical metric. This
is permissible initial retained data and requires no runtime reset.

## Positive diagonal theorem survives, with a controlled small memory seed

The three diagonal frames are `B_aa=(Pp_a²+Pq_a²)/D²`. The two numerator
updates use the same coefficient,

```
A_a = C D² + (C h/2) D PK_aa
Pp_next = A_a Pp - Pp_old
Pq_next = A_a Pq - Pq_old
```

so `W=Pp*Pq_old-Pq*Pp_old` is **constant**. Unlike the previous plus-old
physical leapfrog, its sign does not alternate. This identity holds for
arbitrary time-dependent `K` and all couplings in the existing full equation
builder. If each initial W is nonzero, neither pair can vanish, hence every
`B_aa>0` and the triangular spatial frame has `det(B)>0` for every finite
integer update. This is an invariant, not clipping or post-step repair.

Take current `Pp=D`, `Pq=0`, initial memory `Pp_old=0`, `Pq_old=1`, and
`D_old=0`. Then `W=D_initial!=0`, whereas the first decoded q is only
`-1/(C D_initial^3)`. Nonzero retained W therefore does **not** require an
order-one physical computational mode. The normalized two-level area is
`W/(D_n D_(n-1))` wherever both denominators are positive and falls rapidly.
The previous Wronskian obstruction was specific to keeping a fixed physical
scale while using the sign-leapfrog recurrence.

## Finite-time consistency argument and limits

After the first update, the exact passive identity is

`y_next = E_h(y) + eta*(E_h(y)-y_old)`,

where `E_h(y)=y+h*f(y)` and `eta=D_old/D_next`. This is a perturbed explicit
Euler method, not exact Euler and not the old leapfrog. The first-step q
memory contributes the explicitly bounded extra `-1/(C D_initial^3)`.
For m=3, positivity and monotonic D give
`eta <= 1/((C-1)*D_initial^2)`. Choosing `D_initial >= h^-2` makes this
coefficient O(h^4). On a compact nonsingular domain with bounded/Lipschitz
semidiscrete f, ordinary finite-time error propagation therefore leaves the
Euler O(h) temporal error dominant. This conditional consistency argument
is not spatial stability or a general-Einstein convergence theorem.

In particular, the p/q memory may be made small as h tends to zero while the
exact nonzero-W protection survives. No dissipative filter or runtime
reinitialization is needed. Euler has its own stability restrictions, and
the original spatial constraint/product-rule defects are not repaired by
this observation.

## Independent actual Engine experiment

Run:

```
python -m validation.geometry.team48.temporal_repair_projective
```

The current seed has flat homogeneous B=I, K_aa=-1, Pi_phi=2 and dust amplitude
1. Thus rho=3, Hamiltonian H=0 and momentum/gradient/Gauss constraints vanish.
Charged current and Maxwell fields are zero in this control. Both scalar
and dust source the same geometry. In units c=8piG=1, the independent exact
solution has volume `v(t)=1+3t+3t²/4`, `K=-v'/(3v)`, `Pi=2/v`, dust amplitude
`1/sqrt(v)` and `B=v^(-1/3)`.

At the same proper-time endpoint T=1/4:

| Updates | h | Peak absolute H | Peak field error | Maximum retained bits |
|---:|---:|---:|---:|---:|
| 2 | 1/8 | 0.046875 | 0.192253521127 | 70 |
| 4 | 1/16 | 0.0146591607104 | 0.0795938827091 | 849 |
| 8 | 1/32 | 0.00629406021889 | 0.0370767520785 | 85,291 |

Initial denominators are 64, 256 and 1024 (the square of each h denominator).
The corresponding protected endpoint |q| values decrease from 2.28174e-7 to
1.73549e-9 to 1.33768e-11. At four steps every non-q retained component in the
protected and unprotected control agrees exactly; the positive metric difference
is exactly q², approximately 3.01194e-18. Direct float64 subtraction rounds that
difference to zero, which is not an equality claim. The report includes exact
Fraction numerator/denominator bit counts and signed-integer-pair hashes for H
and q, in addition to passive floating diagnostics.

A separate heterogeneous off-constraint initial seed activates scalar, charged,
Maxwell and dust fields. All 81 Wronskians remain exactly 8 over three actual
Engine updates on 27 nodes; every diagonal stays positive and complete rewind
passes. This tests the coupled algebraic domain invariant and makes no claim
that these deliberately unconstrained data solve Einstein's equations.

The field error is the maximum over B, K, scalar momentum, dust amplitude
and scalar value, across all sampled times. A separately coded reduced
integer polynomial checks every complete Engine state on all 27 nodes;
it does not call the production RHS. All six remainder classes, each
inverse step and complete rewind are checked. Every diagonal remains
positive with exact constant W. A four-step zero-W control approaches the
same physical solution; the nonzero-W memory is a domain safeguard, not an
additional physical source.

These are finite-time homogeneous sourced results. Hamiltonian error is
nonzero; no spatial refinement, full charged test, clock apparatus, or
click-only decoder claim is made. Raw evidence is under
`runs/team48/temporal_repair/projective44.json`.

## Cost and source boundaries

The denominator's bit length grows asymptotically like 3^N. At eight steps
the maximum is already 85,291 bits. Compact channel count therefore does not
imply a practical long-duration solver. This cost must remain prominent.

Primary paper consulted: C. L. Ellison, J. W. Burby, J. M. Finn, H. Qin and
W. M. Tang, *Initializing and stabilizing variational multistep algorithms
for modeling dynamical systems*, https://arxiv.org/abs/1403.0890 (PPPL-4976,
https://bp-pub.pppl.gov/pub_report/2014/PPPL-4976.pdf). The paper motivates
separate analysis of smooth and parasitic modes and preparation; its
runtime reinitialization proposal is not used. Its theorems do not certify
this new projective encoding. The identity and experiment above are
separate derivations and tests.
