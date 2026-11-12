# Researcher 7: a concrete hyperbolicity defect and a 45-channel repair candidate

Date: 2026-11-11. Inspected local baseline `613ea1b`, corresponding research
baseline PR #47 `621fc1f55800e50e1db5f6a30ce24bb83716a49a`. All code in this
report is source-only validation. No production equation, Engine, decoder,
metric authority or acceptance gate is changed.

## Result

The actual triangular-frame continuum reference has a defective principal
symbol in transverse and oblique directions, already about flat spacetime.
This is a specific calculation of the repository equations, not a conclusion
inferred from the name ADM. The defect is invisible to the x-directed planar
tests. A change of integer representation alone cannot fix this continuum
formulation problem.

A constructive alternative is implemented as an isolated **45-channel**
proposal: restore the full Fermi-propagated frame, symmetrize the Ricci term
in the evolution equation, and add a fixed multiple of the existing momentum
constraint to the connection evolution. These additions vanish on the
declared continuum constraint surface. The new full-frame flat principal
symbol is proved strongly hyperbolic in every direction by an exact
square-free matrix-polynomial identity. The compiled tensor fits the hard
mechanical contract and has passed three actual Engine updates with an
independent integer oracle and full rewind.

This solves a **principal-symbol gate for a changed continuum formulation**.
It does not solve nonlinear discrete constraints, metric positivity,
projective bit growth, fully discrete stability, or operational apparatus.

## Primary papers actually read

| Original source and inspected content | What is relevant here |
| --- | --- |
| Buchman–Bardeen, [gr-qc/0301072v2](https://arxiv.org/pdf/gr-qc/0301072), introduction and §§IV–V, equations (53)–(66); [erratum](https://journals.aps.org/prd/pdf/10.1103/PhysRevD.72.049903) | WEBB obtains its hyperbolic connection system through specific constraint additions and gauge choices. Its proof uses real complete eigensystems and a positive symmetrizer under a timelike-domain condition. The erratum changes signs in (59), (B3)–(B5); the arXiv v2 includes this correction. Our repository explicitly says its original frame equations are not that constraint-added WEBB system, so the paper's theorem cannot simply be inherited. |
| Gundlach–Martín-García, [gr-qc/0604035](https://arxiv.org/pdf/gr-qc/0604035), §II.A and principal-symbol/gauge discussion | Well-posedness requires a perturbation estimate with a constant independent of initial frequency. Formulation and gauge matter, including the behavior away from the constraint surface. This supplies the criterion used below; the matrix result is our independent code calculation. |
| Gundlach–Calabrese–Hinder–Martín-García, [gr-qc/0504114](https://arxiv.org/pdf/gr-qc/0504114), §§II–III, equations (1)–(12) and mode analysis | Z4 adds four constraint variables and lower-order damping. It changes the off-constraint system; the linear result excludes undamped constant modes. It is not a proof of exact nonlinear discrete constraint preservation. A lower-order damping term cannot by itself change the high-frequency principal symbol of an already defective system. |

These original texts were opened at the stated equations, including the
one-page erratum. No numerical-relativity theorem is attributed to the
integer compiler or inferred from a paper abstract.

## Actual-code principal-symbol extraction

Set the background to `B=I`, `K=G=0`. For each direction `n`, replace
`partial(field,i)` by `n_i v_field` in the actual equation builder, then take
the Jacobian of the resulting right-hand sides with respect to the jet `v`.
The matrix convention is `partial_t delta_y = A(n) partial_n delta_y`.
The same calculation is performed for the original 24-field Fermi frame and
its 20-field triangular reduction, with exact symbolic arithmetic.

For every tested direction, the original 24-field characteristic polynomial is
`lambda^18 (lambda²-|n|²)^3`; the triangular one's is
`lambda^14 (lambda²-|n|²)^3`. Real eigenvalues are not enough:

| Direction | Full24 zero eigenspace dimension (multiplicity 18) | Triangular20 zero eigenspace dimension (multiplicity 14) |
| --- | ---: | ---: |
| (1,0,0) | 16 | 14 |
| (0,1,0) | 15 | 12 |
| (0,0,1) | 14 | 10 |
| (1,1,0) | 15 | 12 |
| (1,2,3) | 14 | 10 |

One explicit transverse Jordan chain needs no eigensolver. In the triangular
system with dependence only on z, the principal equations include

```
partial_t G010 = 0
partial_t K12 = -partial_z G010
partial_t G122 = -2 partial_z K12.
```

Thus `e_G010 -> -e_K12 -> 2e_G122 -> 0` under `A(e_z)`.
Starting with a unit-amplitude Fourier mode in `G010` produces a term of
magnitude `k² t²` in `G122`. The initial connection perturbation violates the
torsion constraints; this is a finding about the full off-constraint
evolution, not an assertion that a physical Einstein wave grows this way.
The script explicitly checks that torsion defect and a separate transverse
traceless principal control. Finite precision or discretization errors can
populate such off-constraint directions, which is why their behavior matters.

This is a continuum frozen-coefficient statement. It is not an independently
proved instability exponent of every nonlinear integer Engine trajectory.

## A concrete constraint addition and its exact all-direction identity

Let `M_a` denote the existing sourced momentum constraint and `R_ab` the
retained spatial connection Ricci tensor. Before compilation, change the RHS by

```
Delta(K_ab dot) = (R_ba-R_ab)/2
Delta(G_abc dot) = -(delta_ac M_b-delta_bc M_a)/4.
```

The first line makes the Ricci contribution symmetric. It is a fixed algebraic
RHS term, not a state projection, clipping or post-step repair. The second
line uses the same matter momentum included in the original constraint. Both
vanish for continuum Einstein data with the declared torsion-free connection.
Their product degree is at most two; derivative terms use one face after
discretization.

In the full 24-field Fermi formulation the corrected flat symbol satisfies,
**symbolically for arbitrary real `(nx,ny,nz)`**, with `r²=nx²+ny²+nz²`,

```
A (A²-r² I) (A²-r² I/2) (A²-r² I/8) = 0.
```

For nonzero n the seven roots of this annihilating polynomial are distinct
and real. Therefore A is diagonalizable, with possible speeds
`0, ±r, ±r/sqrt(2), ±r/sqrt(8)`. On the unit sphere the spectral projectors
are polynomials in A with fixed nonzero denominators, so they are continuous
and uniformly bounded. This supplies the uniform strong-hyperbolicity
criterion for this flat frozen symbol, beyond checking a few eigenvalues.
The characteristic polynomial checked independently in the listed directions
is `lambda^14 (lambda²-r²)^2 (lambda²-r²/2) (lambda²-r²/8)^2`.

Applying the same additions to triangular20 **does not suffice**. It gives
complete real eigensystems along the three axes, but the oblique `(1,1,0)` and
`(1,2,3)` directions have zero eigenvalue multiplicity 10 and eigenspace
dimension 9. This negative control prevents promoting an axis-only repair.
Restoring four fields is one successful construction for the audited symbol,
not a theorem that four extra fields are the minimum for every formulation.

These coefficients were explored after observing the original failure; this
is an exploratory algebraic repair, not a preregistered physical validation.
The failed triangular version remains in the output.

## Actual integer compiler and Engine evidence

The isolated `build45()` uses the full-frame charged scalar, Maxwell and
squared-dust equations, the fixed constraint additions above, and the existing
projective compiler. There are 24 geometric and 20 matter/potential fields,
plus one retained projective denominator: **45 channels / 135 integers per
node**, leaving three unimplemented slots. No new apparatus is supplied.

At `dt=1/16`, `dx=1/4`, mass-squared zero, coupling one, the compiled tensor
has **881 monomials, degree two, strict single-face support, no old-a input**,
and static multiplier 64. The Engine divisor remains six.

Three updates on 27 nodes with mixed remainder values 0–5 agree exactly with
an independent literal integer-monomial/divmod evaluator. Every transition
inverts and complete rewind returns the seed, including remainders. The
largest retained integer uses 77 bits. This random source preparation is a
mechanical fixture, not constrained physical data.

A separate nonlinear homogeneous source control has `B=I`, `K=-I`, scalar
momentum 2 and dust amplitude 1. Its original H/M constraints vanish, and the
original and corrected physical RHS agree exactly. A transverse-traceless
linear control also has unchanged principal evolution. These checks are
scope controls, not proof of nonlinear discrete constraint propagation.

The protected44 determinant theorem depends on its triangular frame and
cannot be transferred to a general 3x3 B merely by protecting the diagonal.
Adding three diagonal pairs to full45 would count 48 but would **not** by
itself prove a nonzero determinant. The present proposal remains unprotected45.

## Remaining time discretization and bit-cost barriers

The existing projective encoding still has its exponential denominator
growth. Changing the continuum RHS does not alter that recurrence.

There is also a separate fully discrete issue: the leading decoded Euler
map for a Fourier frequency omega has amplification `1+i h omega`, whose
squared modulus is `1+h² omega²`. Under a fixed wave CFL ratio `h proportional
to dx`, high-frequency amplification is not uniformly controlled over a fixed
physical duration as resolution increases. A more restrictive scaling or a
different time map needs a proof. The retained projective-history term means
this Euler calculation is a warning and a target for a complete amplification
analysis, not a finished theorem for the full projective recurrence.

Researcher 1's native reversible lattice coordinates may support a different
time map; their stability and nonlinear refinement require their own proof.
Symplecticity, reversible replay and strong continuum hyperbolicity are
different gates.

Z4 is a second possible formulation route, but appending four variables to
protected44 fills 48 before apparatus or extra gauge/workspace. Damping cannot
be imported as unrecorded information loss. Effective damping in a reversible
extended model is not categorically impossible, but its retained partner
states, arithmetic, inverse and total count must be exhibited. The current
constraint-addition proposal avoids those four new Z4 variables.

## Reproduction and next falsifying tests

```
python -m validation.research_eight.07_hyperbolic_symbol
```

Source hashes, exact eigenspace results, all-direction polynomial proof,
negative triangular results, tensor hash and Engine checks are written to
`runs/research_eight/07_hyperbolic_symbol.json`.

Before promoting this candidate, test its coupled principal symbol on
nontrivial backgrounds; derive constraint propagation including torsion and
matter gradients; independently reconstruct the metric curvature; establish
nondegeneracy and fully discrete stability; then conduct fixed-domain
refinement with transverse and oblique sourced preparations. Predeclare the
tests and retain the old negative controls. None of those general physical
gates is closed by the present 45-channel mechanical run.
