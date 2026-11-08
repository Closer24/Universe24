# Exact coherent sector and a controlled integer-wave limit

Status: mathematical derivation only. The p=q=1 case is a sector of the
unchanged baseline. Other positive p/q values refer only to the separately
specified [fixed-ratio candidate](fixed_ratio_candidate.md), with no variant
implementation or trajectory. No physical particle or mass claim follows.

## Exact reduction

Take a periodic cubic lattice of side L, +++ coupling, and uniform coefficients
p,q. At every spatial site x, prepare all48 channels with the same triple
`(a_x,b_x,r_x)`. Different sites may have different triples. Each directional
coupling is a channel permutation with weight+1, so every channel at x receives
the identical input `u_x=sum_{y~x} b_y`. The equality of the48 triples at each
site is therefore an exactly invariant sector of synchronous evolution.

Set `M=6q`, `alpha=p/q`, and let A be the spatial adjacency operator summing
the six neighbors. On this sector the exact scalar field update is

```text
ell_x(t), r_x(t+1) = divmod(2p*(A b(t))_x+r_x(t),6q),
a_x(t+1) = b_x(t),
b_x(t+1) = ell_x(t)-a_x(t).
```

Writing `b(-1)=a(0)` gives the exact second-order equation

```text
b(t+1) = (p/(3q))*A b(t) - b(t-1) + epsilon(t),
epsilon_x(t) = (r_x(t)-r_x(t+1))/(6q).
```

Let `g=gcd(2p,6q)`. Each site's remainder stays in a fixed residue class mod g,
so the pointwise bound is `|epsilon_x(t)| <= eta=1-g/(6q) < 1`. This term is
determined by the retained state. It is not random noise or a force added to
the board. For the baseline p=q=1, eta=2/3. Coherent preparation is a narrow
invariant family; robustness to deviations between channels is a separate test.

## Linear comparison and its dispersion

Define the real linear comparison field z using the same normalized initial
counters and the equation with epsilon omitted. With `B=A/6`, its equation is
`z(t+1)=2*alpha*B*z(t)-z(t-1)`. B is a self-adjoint contraction in the spatial
RMS norm on a periodic cube. Its Fourier eigenvalue at
`k_j=2*pi*n_j/L` is `gamma(k)=(cos(k_x)+cos(k_y)+cos(k_z))/3`.

For a mode `z_x(t)=exp(i*(k dot x-omega*t))`, direct substitution gives

```text
cos(omega) = alpha*gamma(k)
           = (p/(3q))*(cos(k_x)+cos(k_y)+cos(k_z)).
```

This equation belongs to the comparison family, with approximation error for
the integer dynamics bounded below. It is not inferred by fitting one clock.
The positive-frequency convention is `omega in[0,pi]` when the right-hand side
lies in[-1,1]; negative-frequency partners and discrete-time aliases must be
kept distinct in measurements.

For p=q=1, near k=0,

```text
omega(k)^2 = |k|^2/3 + O(|k|^4).
```

Thus the comparison has a gapless long-wavelength branch with isotropic
leading speed1/sqrt(3) in lattice spacings per update. Direction-dependent
corrections enter at higher order. This effective speed is distinct from the
strict microscopic causal bound of one lattice edge per update.

More explicitly, expanding the exact cosine relation through fourth order gives

```text
omega(k)^2 = |k|^2/3 + |k|^4/108
             - (k_x^4+k_y^4+k_z^4)/36 + O(|k|^6).
```

To obtain this, expand the spatial mean as
`1-|k|^2/6+sum_j(k_j^4)/72+O(|k|^6)` and match
`cos(omega)=1-omega^2/2+omega^4/24+O(omega^6)`. The quartic term is generally
direction-dependent, so the scalar branch is not exactly rotationally invariant
at finite wavelength.

There is also an exact group-velocity bound for this baseline comparison. Away
from the branch endpoints where sin(omega)=0,

```text
partial omega / partial k_j = sin(k_j)/(3*sin(omega)),
|grad_k omega|^2 = sum_j sin(k_j)^2 / (9*(1-gamma(k)^2)) <= 1/3.
```

The inequality follows from
`sum_j cos(k_j)^2 >= 3*gamma(k)^2`, hence
`sum_j sin(k_j)^2 <= 3*(1-gamma(k)^2)`. The endpoints are excluded from the
derivative formula because it is0/0 there; directional long-wave limits have
speed1/sqrt(3).

For the body-diagonal family k=(s,s,s), with s in[-pi,pi], the principal branch
satisfies exactly `omega=|s|`, or `omega=|k|/sqrt(3)`. Away from its endpoints,
the group-velocity norm is exactly1/sqrt(3). In contrast, on an axis
k=(s,0,0), `omega=arccos((2+cos(s))/3)`, and the group speed is strictly below
1/sqrt(3) for0<|s|<pi. Its fourth-order squared-frequency correction is
`-s^4/54`. Diagonal and axial preparations therefore give a direct finite-wave-
vector orientation test, with different predictions from merely fitting one
constant propagation speed.

The existing prepared guided carrier translates by one lattice edge per update,
and the exact local dependence cone also permits one edge per update. Neither
equals this scalar comparison branch's maximal group speed1/sqrt(3). These
are different defined behaviors and bounds, not two independently established
values of one physical light constant. A unique observed c requires a common
internally defined distance/time calibration and detector-click relation; none
is supplied by identifying lattice steps with physical time or by camera motion.

There is an exact integer corollary along the diagonal, stronger than the
large-amplitude approximation. Let f be ANY integer-valued periodic function
of `s=x+y+z mod L`. Initialize every channel at each site by
`b_x=f(s)`, `a_x=f(s+1)`, and r2. The six-neighbor sum is exactly
`u_x=3*(f(s-1)+f(s+1))`. Therefore ell equals `f(s-1)+f(s+1)`, the remainder
stays2, and the next pair is `(a_x,b_x)=(f(s),f(s-1))`. Induction gives the
exact translated profile `b_x(t)=f(s-t)`, `a_x(t)=f(s-t+1)` for every t.
The complete board returns after L updates; its minimal period may divide L.
No large-amplitude limit, smooth profile or floating-point approximation is
needed for this integer theorem.

These are dense planar profiles rather than compact three-dimensional objects.
The same state change can be represented by a one-edge translation in +X, +Y
or +Z, since each changes s by1. That nonunique translation does not identify
a localized object's velocity of one edge per update. The plane's normal
coordinate is s/sqrt(3), so its front advances at1/sqrt(3) along the body
diagonal, consistent with the exact diagonal dispersion. The n=(1,1,1)
sinusoidal preparations are a special case when their rounded a and b values
form these shifted samples; a nonsinusoidal f is also allowed by the theorem.

For 0<alpha<1, the zero-wave-vector frequency is
`omega_0=arccos(alpha)>0`. At fixed alpha and small k,

```text
omega(k) = omega_0 + alpha*|k|^2/(6*sin(omega_0)) + O(|k|^4),
omega(k)^2 = omega_0^2
             + alpha*omega_0*|k|^2/(3*sin(omega_0)) + O(|k|^4).
```

In the additional small-gap regime alpha close to1, expansion of both cosines
gives `omega^2 = 2*(1-alpha)+(alpha/3)*|k|^2`
to leading order in the joint small quantities. The latter is an additional
approximation; it must not replace the exact cosine dispersion at general
alpha. A classical frequency gap is not a physical mass. Identifying mass
would require independently justified energy/momentum observables and their
transformation and collision laws.

For alpha>1 the uniform mode has a linearly unstable characteristic equation
`lambda^2-2*alpha*lambda+1=0`, with one root exceeding1. This is not merely a
linearization artifact for the concrete proposed p=2,q=1 uniform field:
there `u=6b`, `ell=4b`, and r is exactly unchanged, so the integer recurrence
is exactly `b(t+1)=4*b(t)-b(t-1)`. Initial a=b=1 yields b values1,3,11,41,...,
with roots `2+sqrt(3)` and `2-sqrt(3)`. This is an exact algebraic example,
not an executed variant run and not a claim that every state grows.

## Finite-time error bound for every mode together

Let N be a positive normalization amplitude. Compare `x(t)=b(t)/N` to the
linear solution z with exactly matched initial values
`z(-1)=a(0)/N`, `z(0)=b(0)/N`. Let `e(t)=x(t)-z(t)`. Then e(-1)=e(0)=0 and

```text
e(T) = (1/N)*sum_{s=0}^{T-1} U_{T-1-s}(alpha*B)*epsilon(s),
```

where U_n is the second-kind Chebyshev polynomial, defined by
`U_0=1`, `U_1=2x`, `U_{n+1}=2x*U_n-U_{n-1}`. This follows by substitution
in the forced second-order recurrence; for T1 it gives e(1)=epsilon(0)/N.

For 0<alpha<=1, the spectral theorem and
`|U_n(x)|<=n+1` on[-1,1] give the uniform finite-time bound

```text
||e(T)||_RMS <= eta*T*(T+1)/(2*N).
```

Here `||v||_RMS=(L^-3 * sum_x |v_x|^2)^(1/2)`. The bound includes all Fourier
modes simultaneously, arbitrary sitewise initial remainders in their valid
domains, and every integer initial counter field. It is independent of L.
It is an RMS estimate, not a pointwise estimate of the same size. A pointwise
estimate follows with the additional factor L^(3/2), or requires a separate
sharper analysis.

For 0<alpha<1, the identity
`U_n(cos(theta))=sin((n+1)*theta)/sin(theta)` also yields
`||U_n(alpha*B)|| <= 1/sqrt(1-alpha^2)`. Therefore one may use

```text
||e(T)||_RMS <= (eta/N)*sum_{j=1}^T min(j,1/sqrt(1-alpha^2))
             <= eta*T/(N*sqrt(1-alpha^2)).
```

The quadratic bound remains useful near alpha1, where the latter constant
diverges. Neither estimate assumes independent remainder errors or their
cancellation. For any fixed T the integer normalized trajectory converges to
the linear comparison as N grows. The baseline estimate controls growing T
only when T^2/N is small; it is not an unqualified infinite-time limit.

To approximate a predeclared real initial mode or smooth profile, round each
of its scaled a and b values to the nearest integer. The initial normalized
RMS error for each field is at most1/(2N). Linear propagation contributes at
most `(2*T+1)/(2*N)` for alpha<=1. Combining this with the forced bound gives

```text
||b(T)/N-z_target(T)||_RMS
    <= (2*T+1)/(2*N) + eta*T*(T+1)/(2*N).
```

For fixed alpha<1 the initial-error term can instead be bounded by
`1/(N*sqrt(1-alpha^2))`. The initial rounding rule and the linear target are
external preparation/analysis definitions; the board thereafter evolves with
its own integer rule alone.

The same finite-time RMS bound extends beyond the coherent sector. On the
complete channel-address space, a fixed reciprocal signed coupling F is a
real symmetric matrix with absolute row and column sums6. Thus `||F/6||_2<=1`.
For uniform p/q<=1, replace B by F/6 and use RMS over all48L^3 addresses in
the same proof. This covers arbitrary channel fields and the baseline's fixed
sign choices. Coherence and +++ are needed for the simple scalar spatial
dispersion above, not for this full-board linear-comparison error bound. A
channel-asymmetric perturbation generally excites other linear modes; this
extension does not assign them the scalar branch's physical interpretation.

An exact growth corollary follows for the unchanged baseline on any fixed
finite board and any allowed fixed sign tensor. Take N=1 and write the
homogeneous linear solution as
`U_t(F/6)*b(0)-U_(t-1)(F/6)*a(0)`. The same norm bounds give

```text
||b(t)||_RMS <= (t+1)*||b(0)||_RMS + t*||a(0)||_RMS + t*(t+1)/3,
a(t)=b(t-1) for t>=1.
```

The last term uses the baseline remainder endpoint bound eta=2/3. For fixed
finite initial data and board, the full counter norm therefore has a polynomial
upper bound, excluding asymptotic exponential growth of that norm in this
reciprocal baseline family. It does not assert conservation of physical energy,
absence of complicated patterns, or a bound on every proposed complexity
observable. The separately proposed p/q>1 family is outside the contraction
assumption and its exponential example does not contradict this baseline bound.

For a native baseline experiment, even the rounded-initial linear comparator
can be evaluated exactly with integer arithmetic. Set `w_0=b(0)` and
`w_1=A*b(0)-3*a(0)`, then use
`w_(t+1)=A*w_t-9*w_(t-1)` for t>=1. The normalized linear field is
`z(t)=w_t/(N*3^t)`. For every t>=1 the RMS bound can therefore be tested without
floating-point rounding by the integer inequality

```text
sum_x (3^t*b_x(t)-w_x(t))^2
    <= L^3 * t^2*(t+1)^2 * 3^(2*t-2).
```

This is the eta=2/3 bound after squaring and clearing denominators. It compares
against the linear solution with the actual rounded initial counters. Comparing
against an ideal real sinusoid additionally requires the declared initial
rounding bound and an explicit numerical or interval evaluation policy.

## Prospective falsifiable comparison

A small future baseline protocol can specify several admissible wave vectors,
orientations, phases and amplitudes N, with initial remainder2 and all48 channels
equal at every site. Compare complete integer trajectories against the exact
linear solution, using the formula above as a fixed RMS envelope and the
cosine dispersion as the predicted mode family. Include superposed modes to
test the common linear regime, larger amplitudes to test the1/N error scaling,
and new lattice sizes. Do not retune frequency or tolerance for each run.

The sector reduction is an exact theorem; finite-amplitude frequency estimates
and any stronger empirical error scaling remain computational questions.
Observe all native clicks if desired, but the RMS theorem does not by itself
control threshold event times: a small normalized field error can cross an
integer quotient boundary. A clock-to-click prediction needs its own frozen
detector and distance-to-threshold error analysis.

Other uniform p/q values would require explicit authorization and a separately
validated candidate implementation. Heterogeneous coefficients are a prepared
lattice medium and do not have the translation-invariant Fourier law derived
here. Neither the baseline gapless branch nor a candidate gapped branch proves
photon/matter identity, quantum probabilities or complexity selection.
