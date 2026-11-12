# Exact physical domain and retained-bit cost

This audit applies to the selected **massless**, homogeneous, isotropic,
neutral scalar-plus-dust construction. It does not establish massive-scalar,
spatial or general Einstein closure. The validator reads a trajectory; it never
clips, projects or vetoes an Engine update.

## Physical variables and exact invariant

Write the physical volume as `V=B^(-3)`, its proper-time derivative as `U`, the
conserved scalar charge as `P=Pi*V`, and the conserved nonnegative dust source
as `D=d^2*V`. Then

\[
\dot V=U,\qquad \dot U=\tfrac32D,\qquad
I=U^2-3DV-\tfrac32P^2.
\]

The actual physical fields are

\[
k=-\frac{U}{3V},\quad p=\frac P V,\quad d^2=\frac D V,
\quad B=V^{-1/3}.
\]

Their Hamiltonian constraint satisfies the exact identity

\[
6k^2-p^2-2d^2=\frac{2I}{3V^2}.
\]

Consequently the nonzero source terms are not omitted by this coordinate
choice. Differentiation gives `kdot=3k^2-d^2/2`, `pdot=3kp`,
`(d^2)dot=3k*d^2` and `Bdot=kB`. The scalar value is recovered by its
declared integration coordinate in the physical-map report; `P` alone is not
the scalar's absolute initial value.

The exact finite-time map is

\[
V'=V+hU+\tfrac34Dh^2,\qquad U'=U+\tfrac32Dh.
\]

Direct polynomial expansion proves `I'=I`. Replacing `h` by `-h` gives the
inverse. These statements are algebraic; they do not say every interval of the
polynomial continuation remains physically admissible.

## Physical domain is an interval condition

For `D>0` and `I=0`, positive volume requires

\[
U^2>\tfrac32P^2.
\]

There are two disconnected branches. The selected expanding-volume branch has
`U>0` and is forward invariant: for every `h>=0`, `V(h)>=V(0)>0` and `U(h)>0`.
Thus the inverse frame and positive spatial metric remain nonsingular for all
finite forward times on this branch. The positive dust-amplitude branch is an
explicit interpretation choice; squared density does not retain an arbitrary
initial amplitude sign.

For a nonzero source the physical past ends at finite zero volume. Native
integer reversibility can hold beyond that boundary, but physical decoding
cannot justify a continuation through the singularity. The roots are

\[
t_\pm=\frac{-U\pm\sqrt{3/2}\,|P|}{(3/2)D}.
\]

The interval checker uses exact rational comparisons, without evaluating these
square roots. It evaluates `V(t)` at both endpoints and at its vertex
`t=-2U/(3D)` if that vertex lies inside the interval. Strict positivity of the
minimum is necessary and sufficient for the polynomial trajectory to remain
inside the positive-volume domain throughout the requested interval.

**Executed counterexample:** start from `V=1,U=-3,D=1,P=2`. At `h=4`, the final
point has `V=1,U=3` and exactly the same zero constraint. Both endpoints are
positive. But the intervening minimum is **V=-2 at t=2**, so the physical
interval is invalid. The inverse example starts on the selected expanding
branch and integrates backward four time units. Checking only the endpoint
decoder would miss the intervening singularities. A pure-dust control touches
`V=0` without becoming negative and is also rejected.

These are passive validation failures. No running state is reset and no
forbidden runtime singularity veto is introduced.

## Retained integers and bit growth

The selected native volume scaling is `h=1/N`, `V=Q/(4N^2)`. Its recurrence is

\[
Q_{n+1}=2Q_n-Q_{n-1}+6D,
\quad Q_n=b+n(b-a)+3Dn(n+1).
\]

For every integer `|n|<=R`,

\[
|Q_n|\le |b|+R|b-a|+3|D|R(R+1).
\]

Use `R+1` to cover the retained previous slice as well. Frozen source/reference
channels remain bounded by their initial integers; the proper-tick channel is
linear; all legal carries remain explicit retained integers in `0..5`.
Therefore the construction's retained-bit growth is logarithmic in elapsed
tick count for a fixed preparation. At fixed physical time, refinement increases
the initial volume numerator as `N^2`; this cost is also counted.

The allocation includes six channels, hence **18 retained integers per node**:
volume, dust charge, scalar charge, reference velocity, scalar offset and proper
tick. The frozen reference and scalar offset are necessary physical preparation
data, not free readout constants outside the state. Decoder evaluation of cube
roots/logarithms has its own output-precision cost; it does not make those
values exact rational numbers.

## Executed independent checks

`python -m validation.sourced_map.domain` writes
`runs/sourced-map/domain.json` and verifies:

- Symbolic finite-map invariant, exact inverse and physical-source identities.
- **915** exact rational constrained forward-domain cases.
- Whole-interval negatives, including crossing and returning to positive
  volume, touching the singularity, and the finite physical-past boundary.
- Rejection of floating, Boolean, zero-volume, negative-density and unconstrained
  inputs.
- **960** signed integer comparisons against the quadratic bit bound, including
  100-bit initial histories and both time directions.

The companion native audit establishes that the unchanged Engine implements
the recurrence and retains the declared carries. Passing a recurrence bound
alone cannot establish that implementation or repair an incompatible history.
