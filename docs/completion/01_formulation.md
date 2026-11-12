# Full-frame sourced formulation: exact extensions and their boundary

Baseline: PR #50, `62202fdccdd9a40d5dbbec104de6f97d9587a999`.
Code: `validation/completion/formulation.py`.
Reproduce: `python -m validation.completion.formulation`.
Evidence: `runs/completion/01_formulation.json`.

This source-only contribution extends the earlier flat-vacuum principal-symbol
calculation to the full 44 physical fields, constructs an explicitly massive
45-channel tensor, and proves linear constraint compatibility along a nonzero
homogeneous matter family. It does not establish nonlinear discrete Einstein
constraint preservation or convergence of the integer evolution.

## 1. The equation entry point and allocation

`equations` uses the existing full 24-field Fermi-frame geometry, charged complex
scalar, Maxwell field, temporal-gauge spatial potential and signed-square dust.
It applies the PR #50 fixed additions

\[
 \dot K_{ab}\longmapsto\dot K_{ab}+\tfrac12(R_{ba}-R_{ab}),\qquad
 \dot G_{abc}\longmapsto\dot G_{abc}
 -\tfrac14(\delta_{ac}M_b-\delta_{bc}M_a).
\]

Here `M` is the **sourced** momentum constraint returned by the matter builder.
The physical parameters are explicit: by default mass squared is 1, charge
coupling is 1 and cosmological constant is 0. These are fixed equation changes,
not a state projection or a callback after an Engine step. On the full continuum
constraint surface the additions vanish.

`build45(dt=1/16, dx=1/4)` compiles these equations using the existing projective
compiler. The allocation is 24 geometry + 20 matter + 1 common denominator =
45 complete retained triples, or 135 integers per node. The three unused slots
are not an implemented apparatus. The integrator's `common45` uses the same
equation builder with its own explicit timestep and seed; fingerprints must not
be interchanged between parameter choices.

## 2. Theorem: every invertible constant frame, arbitrary matter background

Let \(A(B,n;u)\) be the frozen continuum principal symbol of the 44 physical
equations, with real spatial covector \(n\). Let \(k_a=B_a{}^i n_i\) and
\(r^2=k_a k_a\). The script differentiates the actual source equations with
respect to 44 independent derivative jets, leaving **all 44 background fields
symbolic**, and verifies the polynomial identity

\[
 A(B,n;u)=A(I,Bn;0).
\]

The right side's final argument means zero non-frame background; neither its
derivative jets nor the covector are zero. This equality shows that arbitrary
extrinsic curvature, connection, scalar, dust, potential and electromagnetic
background amplitudes enter lower-order terms only. In the actual source
ordering it also verifies

\[
 A=\operatorname{diag}(A_g,A_m),\quad
 A_m(A_m^2-r^2I)=0,
\]

and, by exact arbitrary-covector multiplication of the 24-field geometry block,

\[
 A(A^2-r^2I)(A^2-\tfrac12r^2I)(A^2-\tfrac18r^2I)=0.
\]

If \(B\) is invertible and \(n\ne0\), then \(r>0\). The annihilating
polynomial has seven distinct real roots
\(0,\pm r,\pm r/\sqrt2,\pm r/\sqrt8\), so the symbol is diagonalizable
over the reals. This is an exact identity, not a directional sample or a
numerical eigensolver tolerance.

For completeness, diagonalizability is uniform: normalize \(T=A/r\), let
\(\mathcal S=\{0,\pm1,\pm1/\sqrt2,\pm1/\sqrt8\}\), and define

\[
 P_\lambda(T)=\prod_{\mu\in\mathcal S\setminus\{\lambda\}}
       \frac{T-\mu I}{\lambda-\mu},\qquad
 H(T)=\sum_{\lambda\in\mathcal S}P_\lambda(T)^T P_\lambda(T).
\]

The projectors sum to the identity and satisfy
\(P_\lambda T=\lambda P_\lambda\). Consequently \(HT=T^TH\), while
\(v^THv\ge\|v\|^2/7\). The upper bound follows because \(T=A(I,k/r;0)\)
depends polynomially on a unit vector, a compact set. For invertible \(B\),
these projectors are smooth functions of \(n\ne0\). This provides the usual
strong-hyperbolicity certificate, locally uniformly on a nondegenerate frame
domain. It is a continuum principal-system theorem, not a stability theorem
for the projective recurrence or a metric invariant under that recurrence.

## 3. Theorem: linear constraints along a massive sourced family

Consider regular homogeneous isotropic backgrounds

\[
 B(t)=b(t)B_0,\quad K_{ab}=\kappa(t)\delta_{ab},\quad G=0,
 \quad\phi=f(t),\quad\Pi_\phi=p(t),\quad d=d(t),
\]

with constant invertible \(B_0\), positive \(b\), and every other background
matter field zero. Here \(d\) is the signed dust amplitude. The mass squared
and charge coupling are 1, and the cosmological constant is zero. The field
equations restrict to

\[
 \dot b=\kappa b,\quad \dot f=p,\quad
 \dot p=3\kappa p-f,\quad \dot d=\tfrac32\kappa d,\quad
 \dot\kappa=3\kappa^2-\tfrac12(f^2+d^2).
\]

The sole nontrivial homogeneous constraint is

\[
 H_0=6\kappa^2-p^2-f^2-2d^2=0,
 \qquad \dot H_0=6\kappa H_0.
\]

All 44 fields may be perturbed, including the second charged-scalar component,
Maxwell field, frame and torsion modes. This is not a restriction of perturbations
to homogeneous or scalar modes. For each Fourier covector let \(L(t,n)\) be
the **full** linearized evolution matrix, including lower-order terms, and let
\(C(t,n)\) be the linearization of all 33 declared constraints: Hamiltonian,
momentum, torsion, antisymmetric Ricci, scalar gradient/curl, electromagnetic
Gauss and magnetic-potential constraints. Then

\[
 \delta c=C\delta u,\qquad
 \partial_t\delta c=(\dot C+CL)\delta u.
\]

The code constructs \(\dot C\) by differentiating the constraint map along the
actual homogeneous field drift. Freezing this term to zero would test a
different background that does not solve the equations.

For symbolic \(\kappa,f,p,d,q\), the script computes an exact basis \(N\)
of \(\ker C\). Every entry of \((\dot C+CL)N\) outside the Hamiltonian row
vanishes identically. Every remaining numerator is divisible by \(H_0\).
For example, on the generic nonzero-frequency branch the only nonzero
off-background-constraint entries are \(H_0\) times

\[
 iq/\kappa,\ iq/\kappa,\ p/\kappa,
 -if/(\kappa q),\ 2d/\kappa.
\]

The code separately checks all four zero/nonzero combinations of \(f,p\),
each at symbolic \(n=(0,0,q)\), \(q\ne0\), and at \(n=0\). Each basis
denominator is checked nonzero on its declared branch. Dust may vanish in
every branch. For real constrained fields, \(\kappa=0\) forces
\(f=p=d=0\); that vacuum branch is checked separately. Thus no division by a
vanishing scalar amplitude is hidden.

For \(q\ne0\), constraint rank is 23 and the tangent space has dimension 21.
For \(q=0\), a nontrivial scalar has rank 20, pure dust has rank 19, and the
vacuum has rank 18. The formulas are rotationally covariant: both the Ricci
symmetrization and momentum addition use frame tensors, with no triangular
alias. A proper spatial rotation maps any nonzero physical covector to the
tested axis. A constant affine coordinate change maps an invertible background
frame to the identity at the instant being tested. The background drift is
transformed as well. This extends the identity to every Fourier direction and
every constant invertible \(B_0\).

It follows that the time-dependent linearized constraint kernel is invariant
along these regular homogeneous solutions. On each fixed Fourier mode this is
an ordinary linear differential equation and its zero-constraint solution is
unique. The nontrivial scalar pair cannot both vanish at an isolated time by
uniqueness of its background ODE; separate charts cover its individual turning
points. The pure-dust and vacuum strata are invariant as well. This establishes
continuous-time **linear** constraint propagation on this sourced family.

It does not cover arbitrary inhomogeneous backgrounds, nonzero background
charge/flux, nonlinear perturbations, boundaries, or exact constraint
preservation by finite integer steps. Matter perturbations interact with the
nonzero scalar background, so this is more than the earlier vacuum test.

## 4. Executed integer compiler and negative control

At `dt=1/16`, `dx=1/4`, mass squared 1, the actual tensor fingerprint is
`02c1aa0ecd76f242c3bfb02233d59e6c873275b5f5b78392bf1a00b5e8ab145b`.
It contains 889 degree-two monomials, static multiplier 64, strict single-face
support and no old-a input reads. A 27-node, three-update run agrees exactly
with an independent scalar monomial/divmod oracle, exercises all six remainder
classes, and rewinds the complete state. Maximum retained integer size in this
specific run is 77 bits. This audit seed is a mechanical stress fixture, not
constraint-consistent physical initial data. The broader projective bit-growth
obstruction remains.

A separate exact negative control removes only the three lower-triangular B
fields while retaining **all nine G fields**, then applies the existing
triangular frame rotation and the same constraint additions. This 21-field
geometry passes the three axial zero-Jordan rank checks but fails directions
`(1,1,0)` and `(1,2,3)`: rank(A)=11 while rank(A squared)=10. Merely restoring
the previously aliased ninth connection field therefore does not fix the
oblique triangular-gauge defect. No such reduced tensor is adopted.

Changing the frame evolution to `K B + h K squared B`, as explored in the
separate metric-domain work, preserves the principal symbol but changes the
lower-order constraint calculation above. The theorem here must not be copied
to that modified law. A sourced transverse-traceless perturbation already
exposes an order-h torsion source; the metric-domain owner tracks that result.

## 5. Primary sources inspected

- [Buchman and Bardeen, gr-qc/0301072v2](https://arxiv.org/abs/gr-qc/0301072),
  §§ IV–V, especially equations 53–59: expressing frame principal matrices in
  coordinate directions introduces the frame contraction with the covector.
  Their WEBB formulation has its own constraint/gauge choices; the present
  equations are not claimed to be a transcription of it.
- [Gundlach and Martín-García, gr-qc/0604035v2](https://arxiv.org/abs/gr-qc/0604035),
  § II.A and the introduction: well-posedness and formulation equivalence must
  be assessed off the constraint surface; a constrained physical subset alone
  is insufficient for numerical free evolution.
- [Garfinkle and Gundlach, gr-qc/0501031v2](https://arxiv.org/abs/gr-qc/0501031),
  § IV, equations 44–56: the subsidiary constraint system is a separate
  compatibility calculation. Their argument motivates retaining all necessary
  lower-order terms in the constraint map and proving closure, rather than
  inferring it from the principal eigenvalues.

The polynomial identities and tensor fingerprints reported here are newly
computed from the pinned Universe24 source. The papers support the analytical
criteria, not the correctness of this particular implementation.
