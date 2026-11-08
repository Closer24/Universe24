# Collective activity and exact Rule3 balance

This is a fresh reconstruction of the mathematical argument discussed before
the earlier scratch files became unavailable. The proof below is self-contained;
the accompanying audit creates new evidence. It does not recover or certify the
unavailable historical run receipts.

## Contract and notation

An address is `nu=(x,g)`, where `g` ranges over the existing 48 channels. Each
address has six signed spatial donors. Let `A` denote their fixed reciprocal
adjacency, so `(Ab)_nu=u_nu`, `A=A^T`, and every edge weight is `+1` or `-1`.
There is one periodic board and one synchronous update:

\[
(\ell,r')=\operatorname{divmod}(2Ab+r,6),\qquad
a'=b,\quad b'=\ell-a.
\]

All operations on vectors are componentwise unless stated otherwise. The
reciprocity assumption is essential to the gradient and quadratic identities.
No metric, force, additional state or callback is introduced.

## Exact complete coordinates

Write `r=2 theta+epsilon`, where `theta` is 0, 1 or 2 and `epsilon` is 0 or 1.
Since the numerator changes by an even integer, `epsilon'=epsilon`. For every
integer input, including negative inputs,

\[
\ell=\left\lfloor\frac{Ab+\theta}{3}\right\rfloor,
\qquad \theta'=(Ab+\theta)\bmod3.
\]

Define

\[
p=3(b-a)+\theta-1.
\]

The coordinates `(b,p,epsilon)` contain the complete original state:

\[
\theta=(p+1)\bmod3,\qquad
a=b-\left\lfloor\frac{p+1}{3}\right\rfloor,
\qquad r=2\theta+\epsilon.
\]

Direct substitution, without a continuum approximation, gives

\[
\boxed{p'=p+(A-6I)b},\qquad
\boxed{b'=b+\left\lfloor\frac{p'+1}{3}\right\rfloor},\qquad
\boxed{\epsilon'=\epsilon}.
\]

This is a coordinate rewriting of Rule3. The letter `p` names a balance
coordinate; it does not establish momentum, clock phase or elapsed time.

## The activity tensor and its quadratic sum

For a direction vector `d` equal to a signed lattice unit vector, define

\[
S_{ij}(x)=\frac14\sum_{g,d}
\left(b_{x,g}-w_d(g)b_{x+d,h_d(g)}\right)^2d_i d_j.
\]

This diagnostic is positive semidefinite. In the lattice-axis frame it is
diagonal, since every `d` has only one nonzero coordinate. It is not a general
spatial metric or an Einstein tensor.

Each undirected reciprocal edge is counted twice. Consequently

\[
V(b):=\sum_x\operatorname{tr}S(x)
=\frac14\sum_{\nu,d}(b_\nu-w_{\nu\eta}b_\eta)^2
=\frac12 b^T(6I-A)b.
\]

Extend this quadratic polynomial to real `b` solely to take its ordinary
gradient, then evaluate at the integer state:

\[
\nabla_bV=(6I-A)b,\qquad
\boxed{p'=p-\nabla_bV}.
\]

The gradient is calculated from the dependence of `V` on the complete `b`
vector. Knowing a numerical value of `V`, or numerical values of `S(x)`, does
not supply that derivative. This notation inserts no continuous dynamics.

There is also a local bound. Put
`delta_(g,d)=b_(x,g)-w_d(g)b_(x+d,h_d(g))`. Since
`Delta p_(x,g)=-sum_d delta_(g,d)`, Cauchy--Schwarz gives

\[
\boxed{\sum_g(\Delta p_{x,g})^2\le24\operatorname{tr}S(x)}.
\]

This bounds the size of a balance-coordinate change. It fixes neither its
sign nor an oscillation frequency.

## Exact counterexamples to stronger interpretations

All examples below use `+++`, background `(0,0,2)`, and a side-three board.

1. **Identical activity and identical initial p do not determine next p.** At
   a single channel address prepare `(a,b,r)=(1,1,2)` in one board and
   `(-1,-1,2)` in another. Every other address remains background. Both have
   `p=0` everywhere and identical `S(x)`, since all signed mismatches change
   sign. At the prepared address the next `p` is respectively `-6` and `+6`.
   All next triples are computed by Rule3. This is not a counterexample to
   deterministic full-state evolution: the complete initial states differ.
2. **V is not conserved.** A single channel `(0,1,2)` has `V=3`. One update
   sets every current counter `b` to zero, giving `V'=0`. Its information
   remains in previous counters and remainders and the complete state rewinds.
   Therefore this quadratic cannot simply be called conserved physical energy.
3. **p is not automatically a clock phase.** Prepare every address uniformly
   as `(0,1,2)`. The exact state at integer time `t>=0` is `(t,t+1,2)` at every
   address. The board keeps changing while `p=3` and `S=0` throughout. This
   drifting solution is not a periodic clock.

## What remains to be derived

A clock needs a fixed, operational readout with repeatable cycles and a usable
record. A measured normalized cycle rate is a separate observable, for example
`N=f_local/f_reference` after calibration. None of the identities above derives
a general relation `N=F(S)` or universal gravitational slowing.

The current repository separately demonstrates a restricted rate coincidence:
two prepared all-48 probes change from period four to period five under the
same neighboring source. Its `4/5` recurrence-rate ratio is valuable finite
evidence. It is not universal across arbitrary clock preparations, and no
Einstein metric or stress-energy source follows from it. The fresh independent
replay in this package checks that existing result without changing its scope.

To test emergent gravity, clock and signal records would have to support one
common predictive geometry across distinct apparatus preparations and unused
observations, and physical source quantities would need an independent
identification. A metric would describe the derived measurements; it would not
be an extra input to Rule3.
