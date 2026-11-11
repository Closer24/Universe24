# Variational and constraint-preserving routes: six-channel positive control

This investigation does not supply a general 48-channel Einstein solver.
It supplies a small exact invariant-preserving primitive and identifies what
the cited discrete-action methods still require under the current contract.

## A real invariant-preserving integer step

Run `python experiments/geometry/team48/variational_null_rotation.py`.
All updates are the unchanged Engine, degree at most three, single-edge
support (in fact onsite), and arbitrary valid retained remainders. Six gears
retain `X,Z1,Z2,Y,U1,U2`. The parameters `U1,U2` are constant prepared gears.
Define the polynomial bijection

```text
R: X' = X,
   Zi' = Zi + Ui X,
   Y' = Y + 2(U1 Z1 + U2 Z2) + (U1²+U2²)X,
   Ui' = Ui.
```

Its inverse changes the signs of the terms linear in U. It preserves
`XY-Z1²-Z2²` exactly. The Rule3 inputs are just

```text
u_X=6X, u_Zi=6Zi, u_Ui=6Ui,
u_Y=6Y+6(U1²+U2²)X.
```

Prepared `a=R^-1(b)` gives the exact map, since `u=3(R+R^-1)b` and each u is
a multiple of three. No dynamic divisor or rounding is introduced.

For any positive integer subdivision S, decode

```text
x=X, zi=Zi/S, y=Y/S²,
E=(x+y)/2, pz=(x-y)/2, px=z1, py=z2.
```

The physical null-rotation parameter per step is `Ui/S`; the tensor does not
change with S. Initial integers `(X,Z1,Z2,Y)=(m,0,0,m S²)` give exactly
`E²-px²-py²-pz²=m²`. The audit tests S=1,2,4,16,64,256 at the same endpoint,
checks the symbolic four-dimensional Lorentz matrix and exact subgroup flow,
tests 100-bit mass, and reverses every complete step. A deliberately incorrect
old history remains reversible but loses the mass-shell identity.

This is an exact kinematic Lorentz-transport primitive. The transport
parameter is not physical proper time, and there is no retained spacetime
path, stress-divergence equation, metric dynamics or gravitational source.
The E component changes under the transport; it is a frame component, not a
claim of energy creation or of separately conserved energy. It shows why
one should not infer a universal integer-refinement impossibility from the
specific uniform scaling failure of the existing frame leapfrog.

## A projective Riccati step that really evolves vacuum geometry

Run `python experiments/geometry/team48/variational_projective_milne.py`.
The three gears P,C,D have the unchanged linear inputs `u=6b`. Prepare
`P=C=1`, `D=2S` and the old history `P_old=C_old=1,D_old=2S-1`.
Thus P and C remain constant and D advances by P. Decode only for observation:

```text
B = diag(C S/D, 1, 1), K = diag(-P S/D, 0, 0), Gamma = 0.
```

For a physical proper-time step h=1/S this gives the exact Riccati subflow
`K00_next=K00/(1-h K00)`, `B00_next=B00/(1-h K00)`. The decoded metric is
`ds²=-dt²+t² dx²+dy²+dz²`, with `t=2+n/S`: a vacuum Milne coordinate patch.
The audit checks all 24 frame evolution identities symbolically, every frame
constraint at every tested integer step, and all 16 components of the spacetime
Ricci tensor in an independent coordinate calculation. The same tensor at
S=1,2,4,16,64,256 reaches exactly B00=1/3 and K00=-1/3 after one proper-time
unit. Its expanding branch stays nondegenerate. A wrong old history remains
reversible but fails the required projective slope constraint.

This is a restricted, actual vacuum geometry solution, not a sourced or
inhomogeneous solver. The rational observer does no feedback and no solve;
the physical frame and curvature variables are rational coordinates of the
integer state. Spatial derivatives, arbitrary curvature, matter and momentum
sources do not close in these three fields. Projective coordinates can remove
the reciprocal in this Riccati subflow; that fact is not a proof that a general
48-channel projective closure exists. Nondegeneracy is only established on
the D>0 expanding branch, not across the D=0 coordinate boundary.

## Independent review of the positive squared-diagonal proposal

Run `python experiments/geometry/team48/variational_amplitude_modes.py`.
For the proposed `B_aa=p²+q²`, both amplitudes obey
`p_next=p_old+h K_aa p` (and the same for q). Then
`W_n=p_n q_(n-1)-q_n p_(n-1)` satisfies `W_next=-W`; nonzero W does
indeed prohibit simultaneous zero amplitudes. This is an exact positivity
argument, including for changing K and therefore independent of its source.

It is also a physical-mode preparation obligation. For constant K, let
`r_plus=h K/2+sqrt(1+(h K/2)²)` and
`r_minus=h K/2-sqrt(1+(h K/2)²)`. Their product is -1. The two amplitude
vectors decompose as `A r_plus^n + D r_minus^n`; a nonzero W requires
linearly independent A,D. Therefore

```text
B_n = |A|² r_plus^(2n) + |D|² r_minus^(2n) + 2(A dot D)(-1)^n.
```

For negative K, the second root grows in magnitude even while the intended
continuum frame contracts. The exact rational example hK=-3/2 has roots
1/2 and -2; with orthogonal amplitude vectors and second-root amplitude
1/1024, its positive metric component eventually grows although the
physical-root contribution decays. This is an independent recurrence audit,
not an Engine compilation or a self-consistent Einstein counterexample.

This does not rule out the proposal. The physical Wronskian can shrink with
refinement: integer amplitudes calibrated by M give `W_physical=W_integer/M²`.
A separate floating example with second-root amplitude h² converges at fixed
time for the constant-K test. A successful integer refinement family must
demonstrate that suppression with its actual fixed tensor, source dynamics,
and prepared histories. Positivity by itself supplies none of those results.

## What a variational replacement would have to do

The following primary sources were consulted directly, with these limited
conclusions:

1. Di Bartolo, Gambini and Pullin, *Consistent and mimetic discretizations in
   general relativity*, [arXiv:gr-qc/0404052](https://arxiv.org/abs/gr-qc/0404052).
   Their abstract explicitly distinguishes a consistent simultaneous solution
   from mimetic constraint preservation: multipliers are determined by the
   discrete equations. The mimetic result is demonstrated for linearized GR;
   their Ashtekar calculation is restricted to Euclidean signature. Four spare
   lapse/shift registers alone do not implement this nonlinear solve.
2. Gambini, Ponce and Pullin, *Consistent discretizations: the Gowdy spacetimes*,
   [DOI:10.1103/PhysRevD.72.024031](https://doi.org/10.1103/PhysRevD.72.024031).
   The stated numerical result is convergence and approximate constraint
   preservation, with substantial computational cost. It is not exact integer
   preservation by a small explicit local update.
3. Kur and Glasser, *Discrete Gravity with Local Lorentz Invariance*,
   [arXiv:2202.02486](https://arxiv.org/abs/2202.02486).
   Their vacuum Palatini discretization preserves Lorentz gauge and symplectic
   structure. This does not directly establish the present sourced integer,
   single-edge recurrence; plaquette data and implicit equations still have
   to be represented and solved honestly.
4. Gonzalez, *Time Integration and Discrete Hamiltonian Systems* (1996),
   [author PDF](https://web.ma.utexas.edu/users/og/PUBLICATIONS/paper_DisHamSys.pdf),
   and McLachlan, Quispel, Robidoux, *Geometric integration using discrete
   gradients* (1999), [DOI:10.1098/rsta.1999.0363](https://doi.org/10.1098/rsta.1999.0363).
   Discrete gradients can preserve prescribed first integrals exactly, but
   the general construction entails implicit updates; the solve must not be
   hidden in an observer or a post-step projection.

For example, midpoint evolution of the unit harmonic oscillator from (1,0)
at h=1/2 gives `(15/17,-8/17)`. Its energy is exact, but the integer state is
not closed without another representation. This exact small calculation is
included in the audit. It is not a theorem against projective, prepared or
multi-microtick encodings.

## A narrow algebraic obstruction, not a GR no-go theorem

Suppose a real polynomial map P on all of R^n preserves the positive norm
exactly: `sum_i P_i(x)^2=sum_i x_i^2`. Its top homogeneous terms have a sum
of squares that cannot cancel, so its degree is at most one. Its constant
term vanishes by evaluation at zero; its linear matrix is orthogonal. If
its coefficients are integers, it is a signed permutation matrix. Thus a
single globally polynomial integer map preserving ordinary oscillator energy
has no generic small-angle family near the identity.

This statement does NOT cover indefinite GR constraints, retained histories,
modular/remainder logic, restricted prepared manifolds, projective encodings,
or multiple microsteps. The six-channel Lorentz null rotation above is a
concrete reason those qualifications matter: indefinite forms admit
nontrivial unipotent polynomial transformations.

## Actionable consequence for the 36-plus-12 proposal

A reduced channel count frees working state but does not itself repair the
constraints. The next useful construction is a discrete invariant manifold
for the *sourced* Hamiltonian, momentum, frame-compatibility and matter-gradient
conditions, with an update tangent to it in the discrete sense. Candidate
routes are a factorization into constraint-preserving local moves, or an
explicitly budgeted iterative solve of a discrete action. Every retained
multiplier, work field, residual, phase and discarded remainder has to be
counted. Until one of these is implemented and independently checked, the
general physical gate stays false even if the arithmetic fits 48 channels.
