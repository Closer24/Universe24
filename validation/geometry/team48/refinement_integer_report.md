# Integer refinement by a retained projective denominator

This is a new research integrator, **not** a claim that the old sign-leapfrog
was corrected without changing trajectories. It removes the old compiler's
fractional-coefficient obstruction. Full nonlinear Einstein convergence,
constraint preservation and an efficient long run remain separate tests.

## Exact construction and readout identity

Let the spatially discretized, rational-coefficient field equations be
`dy/dt = f(y)`, of polynomial degree at most `d=2` or `d=3`. Neighbor terms
must satisfy the existing single-face support rule. For a rational step `h`,
homogenize each monomial to degree `d` using **one retained uniform channel**
`D`: `F(P,D)=D^d f(P/D)`. Choose the positive static integer `C>=2` clearing
every coefficient of `h F`. The immutable tensor is

```
u_D   = 3 C D^d
u_P_i = 3 C (D^(d-1) P_i + h F_i(P,D)).
```

These are integer polynomials of degree at most `d`; no tensor reads `r`
or old `a`, and no new Engine operation is introduced. The factor `C` is a
coefficient multiplier, **not** a change to the Engine divisor six. The
denominator channel is counted. There is no extra phase channel. For the
actual charged triangular model the count is 40 physical numerator channels
plus one denominator: **41 channels, 123 retained integers per node**.

Since every `u` is divisible by three, for **each of all six core remainder
values** the exact unchanged Engine gives `ell=u/3` and `r_next=r`. Therefore

```
D_next = C D^d - D_old
P_next = C (D^(d-1) P + h F(P,D)) - P_old.
```

All nodes initialize both denominator slices identically; the onsite
denominator recurrence then proves spatial uniformity inductively. Its exact
inverse recovers `D_old=C D^d-D_next`, preserving uniformity on every rewind
of the prepared forward orbit. No neighbor reads a denominator at a remote
node; adding a local D factor to an existing one-edge monomial keeps its
support local. One metric is reconstructed from the decoded physical fields.

Prepare any exact rational physical initial data with one common `D0>=2`,
`P0=D0*y0`, and **all previous registers zero**. Thus there is no future
answer or incompatible previous physical history in preparation. The
previous zero denominator is an arithmetic memory boundary; no physical
ratio is evaluated there. The first physical update is exactly explicit
Euler. Subsequently `0<=D_old<D` and

```
D_next >= 2 D^d - D > D > 0.
```

The current ratio is therefore defined throughout the forward orbit and
rewind back to the prepared initial state. Let `E=y+h f(y)`. At every later
step, the following identity is exact:

```
y_next = E + epsilon*(E-y_old),   epsilon=D_old/D_next.
```

At the first step `D_old=P_old=0`, so `y_next=E` exactly and `y_old` is not
needed. This is a proved passive ratio chart, not an arbitrary denominator
asserted to satisfy the original differential equation. The error term is
retained explicitly; no projection, truncation, normalization or hidden
numerical solve is used in evolution. Independent validation may use
rational or floating calculations, but these cannot feed the Engine.

## What refinement is established algebraically

For a **fixed spatial discretization**, a fixed nonzero rational polynomial
`f` and `h=1/S`, coefficient clearing gives `C >= c*S` for some fixed `c>0`:
choose any nonzero coefficient `a/b` in lowest terms, and use
`denominator(a/(b*S)) >= b*S/abs(a)`. If `f=0`, the decoded solution is
constant exactly. This is why static field scaling alone was insufficient,
whereas a retained denominator removes the obstruction.

For `n>=1`, `D_n >= C D0^d`, so
`epsilon_n <= 1/(C D_n^(d-1)-1) = O(h^d)` uniformly. On a compact domain
where the polynomial vector field is Lipschitz and the corresponding exact
solution remains regular, the ratio recurrence is a consistent explicit
Euler perturbation. Bounded solutions give a per-step memory perturbation
`O(h^d)` directly and the usual increment induction strengthens this to
`O(h^(d+1))`; the accumulated memory error is `O(h^d)`. Standard finite-time
Euler stability then gives `O(h)` temporal convergence. This is a local
finite-time **semidiscrete ODE** argument, not a proof of stable continuum
Einstein PDE evolution, spatial consistency, constraint conservation, metric
positivity, or a global synchronous coordinate chart. Those gates need
independent physical tests and joint space/time/seed refinement.

The construction also supports arbitrary rational `dx` by clearing the
resulting construction-time coefficients. Every desired `h,dx` pair has a
finite immutable tensor. No extra runtime state is required as h decreases.
This is a family of laws with declared parameters, not one fixed tensor
whose step is silently reinterpreted.

## Cost and limits

The denominator satisfies `D_next~C D^d`, so its **bit length grows roughly
as d^n**. The numerator bit lengths are of the same order while the decoded
physical fields stay bounded. State dimension remains 41, but memory and
execution cost rapidly become prohibitive. This method trades the previous
integer-coefficient obstruction for enormous integer precision. It cannot
be described as an efficient complete solution. Reducing this bit growth
autonomously without losing reversible information or violating the total
budget is still open.

## Positive 44-channel extension with declared protecting memory

The positive-pair geometry has 43 physical fields, including three pairs
`p_a,q_a`, and fits **44 total channels** after adding D and removing the
old phase. Its homogenization degree is three. At every node and for each
axis the numerator pair has the exact common-coefficient recurrence

```
Pp_next = A_n Pp - Pp_old
Pq_next = A_n Pq - Pq_old
A_n = C D^2 + (C h/2) D PK_aa.
```

`A_n` is an integer on the compiled coefficient domain. It may vary with
node and time; spatially varying K does not affect the argument. Therefore

```
W_n = Pp_n Pq_(n-1) - Pq_n Pp_(n-1)
W_next = W_n.
```

This is **constant**, unlike the sign-flipping W of the superseded
plus-previous leapfrog. All six legal core carries remain unchanged because
every u is divisible by three, so they do not add a hidden pair force.
If `W0!=0`, the current pair cannot both vanish. With the already proved
`D>0`, `B_aa=(Pp_a^2+Pq_a^2)/D^2>0`; hence the triangular inverse triad has
positive determinant and its spatial metric is positive definite at every
finite step. This protects nondegeneracy, not a uniform lower bound or small
condition number, and not the Einstein constraints.

For the physical initial diagonal `B_aa=1`, choose current `Pp=D0,Pq=0`,
old `Pp=0,Pq=1`, and `D_old=0`. All other old numerators are zero. The
initial W is D0. This is retained arithmetic memory, not a claimed earlier
physical slice. The first ratio identity becomes

```
y1 = y0 + h f(y0) - m/(C D0^3),
```

where m is the declared old-numerator vector, with unit entries on the
three q channels. Later steps obey the previous exact epsilon identity.
At fixed D0 and bounded m, the first perturbation is O(h); it occurs once,
so the finite-time first-order convergence argument is preserved. Choosing
`D0=S^2` for `h=1/S` makes it O(h^7) (because C grows proportionally to S).
The protecting memory thus survives exactly in the full integers while its
physical amplitude vanishes with refinement. No runtime reset or projection
is needed. A general rational seed needs the same explicitly checked
nonzero-area preparation; arbitrary unprepared data are not covered.

The actual `temporal_repair_projective.py` independent homogeneous run uses
this preparation and an independently derived flat FLRW scalar+dust
solution. The integer audit additionally checks a nonuniform spatial K and
signed-field fixture, every remainder class and exact W at every node.

## Literature boundary

- Rein and Tamayo, *JANUS: A bit-wise reversible integrator for N-body
  dynamics*, MNRAS 473 (2018), [arXiv:1704.07715](https://arxiv.org/abs/1704.07715).
  Their force evaluation uses floating arithmetic and rounding. It is
  evidence that reversible arithmetic and numerical stability are different
  requirements; that force evaluator does not satisfy our fixed tensor law.
- Petrera, Smirin and Suris, *Geometry of the Kahan discretizations of planar
  quadratic Hamiltonian systems*, Proc. R. Soc. A 475 (2019),
  [primary full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC6451985/).
  A Kahan step is a rational map from a linear implicit solve. It suggests
  projective coordinates, but no Kahan invariant or integrability theorem
  is claimed for the different explicit homogenized-memory map above.

The construction and ratio identity above are proved directly for the
actual tensor. The primary papers do not certify this proposal's GR gates.

## Reproduction

`python -m validation.geometry.team48.refinement_integer_audit` checks
signed initial values, all remainder classes, actual charged tensor
construction, exact first-step Euler agreement, subsequent ratio identity,
strict support, arbitrary-precision fallback and complete-state rewind.
Fresh evidence is written to `runs/team48/refinement_integer/`.
