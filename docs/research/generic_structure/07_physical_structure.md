# 7. Physical structure: one geometry, variational constraints, and an exact frame primitive

Baseline: PR #52, `8c53e69f4b466dcbd2da7dab7e3c365bd9731766`.
This review adds only a source-only audit and this report. It establishes a
prepared integer frame-domain primitive, not a gravity/matter model.

## The physical object to unify

A useful physical specification is a coframe `e`, compatible connection
`omega`, and matter, with metric `g=e^T eta e`. Matter derivatives, signal
characteristics, phase clocks, stress and curvature must use that same pair.
For a nonsingular coframe and spinless matter, the connection equation should
reduce to torsion freedom, while the coframe equation supplies Einstein's
equation with the independently derived matter stress. The metric is a common
derived object, rather than a separate authority assigned to each module.

Wise's Palatini discussion gives precisely these two distinct variations:
`D_omega(e wedge e)=0` and the coframe curvature equation. His equivalence to
the ordinary Einstein equation requires an invertible coframe. In particular,
writing an invertible frame does not establish its field equation, and writing
a connection does not establish that it is the metric's Levi-Civita connection.

## Why polynomial degree is promising, but not a completed compiler

The gravitational action has schematic terms

\[
S_g\sim\int\epsilon_{IJKL}\left[
e^I\wedge e^J\wedge(d\omega^{KL}+\omega^K{}_M\wedge\omega^{ML})
-\frac{\Lambda}{6}e^I\wedge e^J\wedge e^K\wedge e^L\right].
\]

With a linear difference replacing `d`, these are degree three or four in
independent coframe/connection components. Their algebraic variations have
degree at most three. This is a real compatibility with the allowed tensor
degree and with the new polynomial interaction compiler. A term such as
`e_i e_i (omega_j-omega_i)` can also have single-face spatial support.

It is **not** enough to place these terms in `compile_potential()` and run
`u=6b+grad(Phi)`. That routine derives reciprocal responses for a regular
mechanical force interpretation. Palatini is a spacetime, first-order,
degenerate variational system. It has mixed temporal derivatives, multipliers,
primary and secondary constraints, and gauge directions. Its discrete equations
come from varying the full spacetime action, including both neighboring time
slabs; they are not generally a regular kick/drift in every component.

A small diagnostic makes the distinction explicit: in an action
`p qdot - N C(q,p)`, variation of the multiplier `N` imposes `C=0`.
Giving N an ordinary inertial Rule3 channel with force `-d(NC)/dN=-C`
instead gives it an evolution equation. It does not impose `C=0`, and adding
that kinetic law changes the constrained physical theory. Reciprocal force
derivatives or exact rewind cannot remove this difference.

Further obligations remain:

- A gauge-covariant curvature built from a loop of group-valued links generally
  reads multiple edges. Multiplying a holonomy by two coframes also changes
  the raw polynomial degree. It cannot be treated as a free local quadratic
  symbol without accounting for its construction, relations and storage.
- Continuum gauge invariance does not automatically survive a chosen difference
  product. Kur and Glasser derive a particular discrete Palatini model with
  local Lorentz and symplectic structure; those properties belong to their
  discretization, not to every polynomial replacement of its terms.
- Matter actions can introduce inverse-coframe or volume factors. Polynomial
  first-order lifts must count their auxiliary variables and constraints.
- An unreduced four-dimensional coframe has 16 components and a Lorentz
  connection has 24. Their 40 scalar fields already leave only eight channels
  before matter, preparation representation, work and clocks. Gauge reduction
  requires its own constraint argument; it is not free storage compression.

## An executed exact frame-domain primitive

Reproduce with:

```bash
python -m validation.generic_structure.frame_primitive
```

Evidence is `runs/generic-structure/frame_primitive.json`, containing the complete
tensor, seed, trace, symbolic identities, exact checks and source hash.

Let `B` be a 3 by 3 integer inverse spatial frame and let the integers `s,t`
be retained nodewise constants. Define two elementary shears and their product:

\[
M=(I+sE_{01})(I+tE_{10})=
\begin{pmatrix}1+st&s&0\\t&1&0\\0&0&1\end{pmatrix},\qquad
M^{-1}=\begin{pmatrix}1&-s&0\\-t&1+st&0\\0&0&1\end{pmatrix}.
\]

Both matrices have integer entries and determinant one, and

\[
M+M^{-1}=\operatorname{diag}(2+st,2+st,2).
\]

Use nine frame channels and two coefficient channels, **11 complete channels /
33 retained integers per node**. Prepare the complete histories by
`a_B=M^-1 B`, `b_B=B`, `a_s=b_s=s`, `a_t=b_t=t`, with every carry independently
in `0..5`. The fixed tensor is

\[
u_{B_{ij}}=\begin{cases}6b_{B_{ij}}+3b_s b_t b_{B_{ij}},&i=0,1,\\
6b_{B_{ij}},&i=2,\end{cases}
\qquad u_s=6b_s,\quad u_t=6b_t.
\]

Every input is onsite, degree at most three, and reads only old b. The general
`3(Phi+Phi^-1)` embedding from the constraint review applies with
`Phi(B,s,t)=(MB,s,t)`. Since all coefficients in u are divisible by three,
the quotient is exactly `u/3` and all carries remain unchanged. One actual
Engine step gives

\[
(a_B,b_B,r_B)\longmapsto(B,MB,r_B).
\]

The new old slice equals `M^-1(MB)`, so the **complete prepared history graph
is invariant forward and backward**. For every finite positive or negative
tick, `B_n=M^n B_0`, hence `det B_n=det B_0`. An initially nonsingular B stays
nonsingular; `gamma_inverse=B^T B` stays positive definite. This is an exact
domain theorem, not just a finite observed determinant.

The real Engine ran 12 steps on 27 varied, nonorthogonal integer frames and
signed coefficient preparations. All six carries appeared. The independent
scalar update made **10,692 complete integer-entry comparisons**; the matrix
power oracle, complete old-history relation, determinants, exact Sylvester
minors, every inverse and full rewind passed. Maximum retained bit lengths
were `5,7,9,12,14,17,20,22,25,27,30,32`.

### Limits are part of the result

1. **It is a prepared kinematic map.** The two shear coefficients are frozen;
   they do not respond to matter or connection evolution. It is not the
   reciprocal gravity/matter potential, nor a dynamically chosen sequence of
   shears. Composing distinct shears needs a new complete-state/scheduler
   proof, especially if their parameters change.
2. **Off the history graph it can fail immediately.** The actual audit starts
   with `B=I`, `s=t=1`, but `a_B=diag(3,3,2)`. One valid Rule3 update gives
   `B_next=0`, while the complete state still rewinds exactly. The prepared
   relation is essential.
3. **Volume is fixed.** Any product of these determinant-one left shears leaves
   `det B` fixed. For this inverse-frame convention,
   `sqrt(det gamma)=1/abs(det B)`. Such shears alone cannot represent isotropic
   expansion; `B -> 2B` changes its determinant by eight. A separately proved
   nonzero scale degree and its conjugate/history are required.
4. **Nondegeneracy is not conditioning.** With `s=t=1`, `B0=I`, let
   `lambda=(3+sqrt(5))/2`. The condition number of `B_n^T B_n` is exactly
   `lambda^(4n)` despite determinant one. The audit retains this counterexample.
5. **These are not Lorentz gauge transformations.** A generic shear does not
   preserve the internal metric; it changes the decoded spatial metric. No
   torsion, Einstein constraint, geodesic or conservation claim follows.

## Recommended generic architecture

The useful design is a **certificate-first physical compiler**:

| Layer | Concrete responsibility | Current evidence |
| --- | --- | --- |
| Common geometry and matter specification | Declare coframe/connection, one metric, matter kinetic/action terms, units and gauge | Specification proposal; existing common45 supplies a separate equation-level candidate |
| Discrete physical map | Derive a constrained variational or otherwise certified map, with torsion/Gauss/Einstein identities and a nonsingular domain | Not established for the coupled Einstein law; reduced lift retains its tick-two failure |
| Complete integer embedding | Prove `T^m E=E Phi`, including all carries, old histories, work and scheduler state | Generic certificate and exact positive fixtures exist; this frame map is one additional instance |
| Local compilation and budget | Certify integer coefficients, cubic/single-face support and all retained ownership | Interaction and native-schedule compilers prove particular classes; `44+1+3=48` only supplies rank-one drift in that schedule, not 44 independent kinetic directions |
| Operational readout | Compare actual matter packets, phase and signals against the same saved metric with fixed calibration | New chiral packet is restricted transport; no universal proper-clock relation follows |

The next useful composition is a **small reciprocal matter/frame sector** with
an explicit gravitational constraint and variable volume, then an exact
embedding certificate. It should retain both the shear off-sector failure and
the existing Einstein tick-two counterexample. Passing such a sector can
justify an ingredient; it cannot promote the unrepaired full45 law. An action
label, same-run receipt or combined channel count cannot substitute for the
missing map and constraint proofs.

## Primary sources and scope of inspection

- Derek K. Wise, [*MacDowell–Mansouri Gravity and Cartan Geometry*](https://arxiv.org/pdf/gr-qc/0611154),
  section 5.1, equations 10–12: inspected coframe metric, connection, Palatini
  action and separate torsion/Einstein variations, including nondegeneracy.
- Eugene Kur and Alexander S. Glasser,
  [*Discrete Gravity with Local Lorentz Invariance*](https://arxiv.org/abs/2202.02486):
  inspected the primary article's abstract and model claim. It motivates an
  exact discrete symmetry requirement; no uninspected implementation is imported.
- Cayetano Di Bartolo, Rodolfo Gambini, Rafael Porto and Jorge Pullin,
  [*Dirac-like approach for consistent discretizations of classical constrained theories*](https://arxiv.org/abs/gr-qc/0405131):
  inspected the primary abstract's conditions: discrete constraint preservation
  can fix multipliers and change constraint classification. No runtime multiplier
  solve is authorized by citing this work.

The shear theorem, actual Engine results, counterexamples and compiler architecture
are this review's derivations and recommendations, not results attributed to
those papers. General Einstein acceptance remains open.
