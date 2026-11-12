# One constrained map: independent domain and finite-time convergence proof

This package reviews and executes the **same six-channel spinor candidate** as
`validation/unified_law/common.py`. It does not append another integrator to it.
Run `python -m validation.unified_law.invariant_map`; fresh evidence is
`runs/unified_law/04_invariant_map.json`.

The result is restricted to an expanding homogeneous isotropic universe with a
neutral massive scalar and comoving dust. It gives an exact physical constraint,
a genuine Einstein continuum pushforward, an actual complete-state Engine map,
and a finite-proper-time convergence theorem for that map. It does not supply
spatial modes, a measured clock detector or an efficient integer encoding.

## 1. Why the previous history obstruction does not apply

Write the four real spinor coordinates as z=(a,b,c,e), and retain beta separately.
These mathematical a,b are coordinate names, not the Engine's two history banks.
The common decoder defines

\[
s=(a^2+3b^2)/2,\quad t=c^2+3e^2,\quad p=ac+3be,\quad y=bc-ae,
\]
\[
k=-s-t/12,\quad \phi=2s-t/6-y,\quad d=s-t/12+y.
\]

The identity `2st=p²+3y²` implies

\[
C=6k^2-p^2-\phi^2-2d^2=2st-p^2-3y^2=0
\]

for **every** real z. Therefore every decoded current Engine state is constrained,
even when its stored previous coordinate numerator is nonzero. This is a fixed
choice of physical coordinates, not a projection or correction of an evolved
physical state. All spinor numerators, their old banks, denominator and six-valued
remainders remain retained and reversible. The decoder changes none of them.

The old obstruction concerned the different interpretation in which numerator
components were independently null physical k,p,phi,d vectors. Subtracting two
such vectors need not remain null. Here the numerator subtraction occurs before
the nonlinear physical decoder. This is not an exact conjugacy to the old
full45 **discrete** map; it is a new time discretization of the same declared
homogeneous continuum equations.

An identically zero C would be physically empty without correct dynamics. The
audit independently expands the decoder and differentiates it through the
actual candidate polynomial. It obtains, in **normal proper time with lapse1**,

\[
\dot k=(p^2+d^2)/2=3k^2-(\phi^2+d^2)/2,\quad
\dot p=3kp-\phi,\quad \dot\phi=p,\quad
\dot d=3kd/2,\quad \dot\beta=k.
\]

These are the massive scalar/dust Einstein equations used by the existing full
source, restricted to this homogeneous sector. The spatial frame is
`B=exp(beta) I`, so `B_dot=kB`. The actual source check in the coordinate package
also verifies all33 declared homogeneous constraints and zero velocities for
the omitted fields. The two checks have different purposes: this package
verifies the algebra and time map independently; the coordinate package checks
the existing full source implementation.

## 2. Global continuum bound and a useful force estimate

Use the positive matrix

\[
W=\operatorname{diag}(1,3,1/6,1/2),\quad
N=z^TWz=-2k.
\]

The pushforward immediately gives

\[
\dot N=-(p^2+d^2)\le0.
\]

For the shared initial data z=(1,0,0,0), beta=0, one has N=1,
k=-1/2, phi=1, d=1/2, p=0. Thus the continuum spinor remains bounded for all
finite forward proper times, k stays in[-1/2,0], and beta is finite on each such
interval. Since the polynomial vector field stays in a bounded spinor domain,
there is no finite-time spinor blowup. The exponential metric remains positive.

For a stronger estimate, the actual spinor force factors as

\[
F(z)=(L+G(z))z,\quad G=\tfrac32 kI+J,
\]

where the code verifies exactly

\[
L^TW+WL=0,\quad L^2=-I/4,\quad J^TW=WJ,
\quad J^2=\frac{3(d^2+2\phi^2)}{16}I.
\]

Since `12k²-d²-2phi²=2p²+3d²>=0`, the eigenvalues of J in the W inner product
lie between `-3|k|/2` and `3|k|/2`. Because k<=0, G has eigenvalues in[3k,0].
Consequently

\[
\|F(z)\|_W\le(1/2+3N/2)\sqrt N.
\]

The forward Euler point `E_h(z)=z+hF(z)` therefore satisfies

\[
N(E_hz)=N(z)-h(p^2+d^2)+h^2\|F(z)\|_W^2
\le N(z)\{1+h^2(1/2+3N(z)/2)^2\}.
\]

The continuum N monotonicity is **not** asserted for every finite Engine step.
The last inequality is the finite-step bound actually used below.

## 3. The actual complete-history recurrence

There are five physical coordinates and one projective denominator, hence six
complete channels and18 retained integers per node. The common tensor has58
cubic-or-lower terms and uses exactly the unchanged fixed-six Engine. All u
coefficients are multiples of3, so every valid remainder is retained unchanged.
For the standard zero-old preparation, the exact numerator equations are

\[
D_{n+1}=M D_n^3-D_{n-1},\qquad
P_{n+1}=M\{D_n^2P_n+hF_{\rm hom}(P_n,D_n)\}-P_{n-1}.
\]

M is a static coefficient-clearing integer, not the Engine divisor. For h=1/m,
the compiler gives M=144m in the tested family; the proof only needs M>=m. The
linear `-a` term in the coordinate RHS already forces the coefficient-clearing
integer to be a multiple of m. There is no runtime division by m.

For `x_n=P_n/D_n`, including beta, the actual decoded map is

\[
x_{n+1}=E_h(x_n)+\epsilon_n\{E_h(x_n)-x_{n-1}\},\quad
\epsilon_n=D_{n-1}/D_{n+1}.
\]

The first step is exactly Euler because the old denominator/numerators are zero.
This zero memory is not an earlier physical Einstein slice. Later old physical
coordinates in the displayed formula are well defined. The executable checks
this recurrence with exact Fractions against every actual default Engine step.

Assume D0>=2. Induction gives `0<=D_(n-1)<D_n` and positive increasing D. After
the first step, `D_n>=M D0³`, hence

\[
0\le\epsilon_n\le\frac1{M D_n^2-1}
\le\frac1{M^3D_0^6-1}\le\frac{h^3}{63},\quad n\ge1.
\]

The first epsilon is zero. This uniform estimate is deliberately loose; no
rounding, cancellation or observed smallness is needed for it.

## 4. A proved finite-time domain for the actual map

Assume the shared sa=1 seed, h=1/m<=1/16, D0>=2 and nh<=T<=1/8. Set eta=h³/63.
While N<=2, the Euler estimate gives

\[
\|E_h(z)\|_W\le\sqrt{1+49h^2/4}\,\|z\|_W.
\]

For the running maximum of the two retained physical spinor norms, the exact
history formula therefore gives a per-step multiplier at most

\[
(1+\eta)\sqrt{1+49h^2/4}+\eta\le1+7h^2.
\]

For example, use `sqrt(1+x)<=1+x/2`, `eta<=h²/1008`, and
`49/8+1/336<7`. The bound is also valid for the first step with epsilon=0.
Thus the running maximum is bounded by `exp(7Th)`. With the stated T,h,

\[
\exp(7Th)\le\exp(7/128)\le128/121<\sqrt2.
\]

The first-crossing argument closes the bootstrap, proving **N_n<=2** for every
actual tick in this interval, independently of the number of ticks and all six
prepared remainder classes.

Beta obeys the same history law with RHS k<=0. Its increments satisfy

\[
\Delta\beta_{n+1}=(1+\epsilon_n)hk_n+\epsilon_n\Delta\beta_n.
\]

They are nonpositive from the zero-beta preparation. Since |k|<=1 on the
proved spinor domain, each increment has magnitude at most
`h(1+eta)/(1-eta)`. Summing gives `-2T<=beta_n<=0`. In particular,

\[
-1/4\le\beta_n\le0,\qquad e^{-1/4}\le B_n\le1.
\]

The metric is read passively; no exponential is evaluated to generate a tensor
update. This is a uniform finite-proper-time domain bound, stronger than a
numerical determinant check. It is not a long-time conditioning theorem.

## 5. Finite-time convergence of the actual map

Both the exact solution and the actual discrete points lie in the convex box

`|a|<=3/2, |b|<=1, |c|<=7/2, |e|<=2, |beta|<=1/4`.

Exact sums of absolute polynomial coefficients, with these radii, give

\[
\|DF\|_\infty\le L=4745/64,\quad
\|DF\,F\|_\infty\le A=5085391/8192,\quad
\|F\|_\infty\le15625/384.
\]

These conservative bounds are computed symbolically, not fitted to trajectories.
The additional complete-history term has norm at most `10 epsilon_n`, hence at
most `10h³/63`. Taylor's theorem bounds the exact solution's one-step Euler
defect by `Ah²/2`. If e_n is the infinity-norm coordinate error, then

\[
e_{n+1}\le(1+hL)e_n+Ah^2/2+10h^3/63.
\]

Since e0=0, discrete Gronwall gives

\[
\boxed{e_N\le\frac{e^{LT}-1}{L}
       \left(\frac{Ah}{2}+\frac{10h^2}{63}\right)}.
\]

Thus the **actual retained-history map converges with first order** on this
finite-proper-time family. The physical decoder is polynomial on the same
bounded box, and `exp(beta)` is Lipschitz there; the Einstein physical fields
and metric therefore converge as well. Constraint C remains exactly zero at
every discrete point, independently of the convergence estimate.

This is not an assertion that finite steps exactly satisfy every differential
Einstein equation or a discrete dust-volume conservation law. Those evolution
errors converge to zero. The very conservative rigorous bound establishes the
order and domain, while the independent experiment below measures useful errors.

## 6. Executed same-law evidence

Default identity, matching the common runtime/clock handoff:

- Tensor: `8d5f0fad5d094908afd4e78d05e60710b96c95943bb7aa791e5b753ff33e9df9`.
- Complete seed: `61b79e0831d775508ab04086aa4f4009d89bb6df95e2357e4ee7e5ff2777097f`.
- h=1/24, D0=4,27 nodes, three actual ticks, all six carries retained.
- Exact decoded history identity, every physical C=0, domain checks, immediate
  inverse and complete rewind pass. Maximum bits:3,18,66,207.

For fixed T=1/8, a separate60-digit RK4 integration of the **physical Einstein
ODE** supplies the reference; it is not used for seeds or Engine feedback.
Changing its step count from1024 to2048 changes the answer by less than
`2.47e-18`.

| Engine steps | h | Maximum physical-field error | Observed order | Peak bits |
|---:|---:|---:|---:|---:|
| 3 | 1/24 | 0.00342428804 | — | 207 |
| 4 | 1/32 | 0.00254452989 | 1.0322 | 649 |
| 6 | 1/48 | 0.00168089196 | 1.0226 | 6101 |

The physical error compares k,p,phi,d,beta. All three runs retain C=0 exactly,
use the same physical initial data and unchanged Engine, and completely rewind.
Their different h values produce explicitly different prepared tensors.

The bit growth remains the severe projective limitation: denominator bit length
grows exponentially in the number of updates. This proof does not turn the
six-channel construction into a bounded-cost general universe. No spatial
packet, arbitrary anisotropic frame, charged field, detector record or quantum
claim is added.

## 7. Primary reading and attribution

Celledoni, McLachlan, McLaren, Owren and Quispel,
[Discretization of polynomial vector fields by polarization](https://arxiv.org/pdf/1506.03855),
Definition1 and Propositions4–5, provides genuine examples of complete-history
modified invariants for polynomial Hamiltonian flows. It also requires a
rational linear solve and distinguishes its polar map from ordinary leapfrog.
That method has **not** been inserted into the Engine. The weighted norm,
projective domain and Gronwall estimates here are derived for the actual selected
spinor map; they are not attributed to that paper.

The constructive change is the physical coordinate interpretation together with
its exact Einstein pushforward and a checked complete-state evolution. Neither
the words “spinor” nor “constraint identity” establish quantum mechanics or a
general physical model.
