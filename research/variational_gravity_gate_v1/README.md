# Exact variational Rule3 and Einstein clock–signal consistency gate

**Date:** 2026-11-08. **Evidence status:** exact all-channel mechanics and an Einstein-specific *necessary-condition/no-go* test; **no emergent gravity, physical metric, photon, mass, stress-energy, or Einstein field equation has been derived**.

The immutable model is one 48-channel `2O` board per site, six face neighbors, one fixed signed reciprocal coupling chosen before the run, exactly two unbounded integers `a,b` and remainder `r in 0..5` per channel, and one synchronous Rule3. This study adds **only read-only analysis and test code**. It links the previously established strain gradient and restricted clock-rate measurements to a genuinely local discrete action, then states what a viable Einstein interpretation must additionally predict.

## 1. Exact coordinate chart on the original state

At every full address `nu=(x,g)`, set `theta=floor(r/2)`, `epsilon=r mod 2`, and

```
p = 3*(b-a) + theta - 1.
```

The triple `(b,p,epsilon)` is an **exact bijective coordinate description** of `(a,b,r)`:

```
theta = (p+1) mod 3
k     = (p+1-theta)//3
a     = b-k
r     = 2*theta+epsilon.
```

The parity `epsilon` remains invariant; no state information is lost and no additional register is added. Let `A_sigma` be the *actual* symmetric all-48 signed neighbor operator and `L_sigma=6I-A_sigma`. The **complete original Rule3** now reads

\[
\boxed{p_{n+1}=p_n-L_\sigma b_n,\qquad
b_{n+1}=b_n+\lfloor(p_{n+1}+1)/3\rfloor,\qquad
\epsilon_{n+1}=\epsilon_n.}
\]

This holds for every integer state and all eight fixed body-sign triples.

## 2. Exact local potential and a discrete phase-space action

Because every directional connection is reciprocal and has weight `w=±1`,

\[
V_\sigma(b)=\tfrac12 b^T L_\sigma b
=\tfrac14\sum_{\nu}\sum_{\eta\sim\nu}(b_\nu-w_{\nu\eta}b_\eta)^2\ge0,
\qquad \partial V_\sigma/\partial b=L_\sigma b.
\]

The sum is over **all 48 channels at every site**, and over all six directed ports; a physical `T_{mu nu}` or energy is *not* assigned.

To obtain an explicit differentiable generating function, extend the integer tooth function to real values as follows. Set `k=floor(p/3)` and `s=p-3k in [0,3)`, then

\[
D(p)=\begin{cases}
 k,&0\le s\le1,\\
 k+3(s-1)^2-2(s-1)^3,&1\le s\le2,\\
 k+1,&2\le s<3.
\end{cases}
\]

This is a continuously differentiable nondecreasing function with **exact integer values** `D(m)=floor((m+1)/3)` for every integer `m`. Define `K(p)=int_0^p D(v) dv`. This is convex and `K'(m)=floor((m+1)/3)`. At integer `m=3k+s`, `s=0,1,2`,

\[
K(3k)=\tfrac32 k^2,\quad K(3k+1)=\tfrac32 k^2+k,\quad
K(3k+2)=\tfrac32 k^2+2k+\tfrac12.
\]

Now define the **auxiliary real phase-space action** on paths `(b_n,p_n)`:

\[
\boxed{\mathcal S=\sum_n \Big[
 p_{n+1}\cdot(b_{n+1}-b_n)
 -\sum_\nu K(p_{n+1,\nu})-V_\sigma(b_n)\Big].}
\]

Variations of `p_{n+1}` yield `b_{n+1}-b_n=D(p_{n+1})`; variations of interior `b_n` give `p_{n+1}-p_n=-L_sigma b_n`. When the initial state is integer-valued, this is **exactly native Rule3**, including every `r` reconstructed from `p` and the inert parity label. It is not a new evolution rule or a physical continuous spacetime.

Equivalently, this is a Type-II generating function `F_2(b_n,p_{n+1})=b_n.p_{n+1}+V(b_n)+sum K(p_{n+1})`. The auxiliary real map is a composition of two canonical shears and preserves `sum_nu db_nu ∧ dp_nu`: its Jacobian is `J=J_d J_k`, with `J_k=[[I,0],[-L,I]]` and `J_d=[[I,M],[0,I]]`, `M=diag(K''(p'))`. Both `L` and `M` are symmetric. **On the integer lattice, the map is exactly the original invertible update**; the arbitrarily chosen smooth interpolation between integers is not a physical claim.

**Essential caution:** the expression `H=V(b)+sum K(p)` is **not conserved** by the finite kick–drift step. Exact reversibility and a variational/symplectic embedding do not establish a physical stress-energy tensor, covariant conservation, Einstein dynamics, or an emergent metric.

## 2b. Exact all-48 scalar spatial mode and a Newtonian `1/r` kernel — with a decisive source caveat

The `+++` 2O coupling has a rigorously invariant **channel-uniform sector**: if the complete triples are the same for all 48 labels at each site, their future triples remain channel-uniform. For the counter profile `b_(x,g)=B_x` at an instant,

\[
(L_+ b)_{x,g}=6 B_x-\sum_{d=\pm e_i}B_{x+d}
=:(L_\mathrm{sc}B)_x,\qquad \text{for every }g=0,\dots,47.
\]

This is precisely the standard 3D positive cubic **scalar lattice Laplacian**, with no independently inserted gravitational field and no selected subset of channels. Its infinite-volume Green kernel is

\[
G_\infty(x)=\frac{1}{(2\pi)^3}\int_{[-\pi,\pi]^3}
\frac{e^{ik\cdot x}d^3k}{6-2(\cos k_x+\cos k_y+\cos k_z)}
=\frac{1}{4\pi|x|}+O(|x|^{-3})
\]

for large spatial separations (direction-dependent higher corrections). Thus the **linear spatial operator itself** has the same leading inverse-distance kernel used by Newtonian potential theory. On a periodic finite board, the zero mode is removed:

\[
L_\mathrm{sc}G_L=\delta_{x0}-1/L^3,\quad \sum_xG_L(x)=0.
\]

The optional `newtonian_kernel.py` checked the 48-channel stencil at 3,072 receiver addresses, solved the finite Fourier problem on sides 64/96/128 with maximum residual below `4e-16`, and fitted `G_L(r)=a/r+b` over a short axial window. The fitted `a` values were `0.0811905`, `0.0808166`, `0.0806307`, approaching the infinite-volume `1/(4pi)=0.0795775`. The fit is *illustrative*: finite-volume constants and lattice corrections matter.

**Crucial distinction between an operator and its realization by Rule3:** at every integer trajectory,

\[
L_\sigma\overline b_T=-\frac{p_T-p_0}{T},
\qquad \overline b_T=T^{-1}\sum_{n=0}^{T-1} b_n.
\]

This is exact by telescoping. In an exact periodic configuration, `p_T=p_0`, so `L_sigma mean(b)=0`; on a connected `+++` lattice the static mean counter is spatially uniform. Therefore a genuine persistent `1/r` profile **has not been produced**. It would require a separately identified, self-consistent nonperiodic phase-drift source, with proper compensation for the finite torus zero mode. Defining the “mass density” as `-Delta p` merely restates the identity and is **not** an independent matter-source derivation. The scalar Laplacian and Green kernel are mathematical Newtonian-limit substrates, not gravitational attraction or the Einstein field equations.

The frozen-remainder *comparison* `b_(n+1)+b_(n-1)≈(A/3)b_n` has a channel-uniform Fourier branch `cos(omega)=(cos kx+cos ky+cos kz)/3`, with leading isotropic small-k speed `1/sqrt(3)` in lattice units. This is **not** established as a family of full nonlinear, integer, physically calibrated light waves; the integer quotient and changing remainders must not be dropped when making physical claims.

## 3. Why clocks plus an unchanged event front do not solve Einstein's vacuum equations

For a stationary zero-shift metric and **independently calibrated physical null propagation**, let a clock rate relative to a chosen time coordinate be `N(x)`, and an isotropic spatial length factor be `H(x)`:

\[
ds^2=-N(x)^2 c^2dt^2+H(x)^2 \delta_{ij}dx^i dx^j,
\qquad v_\mathrm{null}(x)/c=N(x)/H(x).
\]

The special *physical* hypothesis `v_null(x)=c` in all directions forces `H=N`. The metric is then conformally Minkowski, `g_{mu nu}=Omega(x)^2 eta_{mu nu}` with `Omega=N`, **not** necessarily flat. For `omega=ln Omega` static, direct 4D curvature calculation gives

\[
G_{00}=-2\Delta\omega-|\nabla\omega|^2,\qquad
\sum_{i=1}^3 G_{ii}=4\Delta\omega+5|\nabla\omega|^2.
\]

Consequently,

\[
\boxed{\sum_i G_{ii}+2G_{00}=3|\nabla\omega|^2.}
\]

In **vacuum with `Lambda=0`**, `G_mu nu=0` would force `grad Omega=0`. Thus a *nonconstant* static gravitational lapse with the same calibrated coordinate null cone as Minkowski is **not an exterior-vacuum Einstein solution under this conformal/zero-shift ansatz**. A nontrivial conformal metric can still be curved and correspond to a nonzero stress-energy source; no inference about Universe24's actual stress-energy follows.

In the weak-field, asymptotically Cartesian isotropic PPN gauge, write `N=1-U/c²+O(U²)` and `H=1+gamma U/c²+O(U²)`. Then

\[
\frac{v_\mathrm{null}}c=1-(1+\gamma)\frac U{c^2}+O(U^2),
\quad \alpha=\frac{d\ln(v_\mathrm{null}/c)}{d\ln N}\to 1+\gamma.
\]

Einstein gravity has `gamma=1`, so its leading requirement is **`alpha=2`**, whereas unchanged calibrated coordinate null speed would imply **`alpha=0` / `gamma=-1`**. This is a falsifiable common-metric **benchmark**, not an extracted PPN parameter for the automaton. Assumptions: true physical photons, calibrated spatial coordinates, a weak-field sequence of source strengths, a source-free exterior, and an applicable stationary gauge. See the PPN review: https://doi.org/10.12942/lrr-2014-4 .

## 4. Actual Rule3 clock-plus-pulse audit: do not apply the PPN equation prematurely

The separate all-48 preparations from earlier local work contain six phase-matched face clocks around one J-paired source. Each face clock has exact full-state period **5** with the source, **4** without it. A matched distant clock stays at period **4**. An initially balanced 48-channel difference is seeded at the midpoint, three lattice steps from a near and a far clock.

The fresh **self-contained** `signal_gate.py` rebuilds this configuration from the pinned native core. Twelve source on/off × six-face runs for pulse amplitude 6 reproduce earliest complete-state differences at update `3` at *both* receiver nodes when the source is present. Four amplitude controls show that **earliest differences are not universal**:

| Balanced 48-channel amplitude | Near first full-state difference | Far first full-state difference |
|---:|---:|---:|
| +1 | none in 16 steps | none in 16 steps |
| +3 | 3 | 4 |
| -3 | 5 | 4 |
| +6 | 3 | 3 |

For nonzero differences, the prepared clock may be disturbed by the signal; source and oscillator strongly interact. These are not repeated calibrated photon arrival times. **Do not claim that equal update-index arrival proves conformal geometry, or that these measurements extract `gamma=-1` or refute Einstein.** The theorem in §3 is a conditional test to use *after* an operational photon-like carrier and fixed clock readouts exist.

## 5. Reproduce, provenance and falsification gates

From the repository root:

```sh
python -m research.variational_gravity_gate_v1.audit
python -m research.variational_gravity_gate_v1.signal_gate
# optional: finite-volume Green kernel via numpy
python -m research.variational_gravity_gate_v1.newtonian_kernel
# optional: independent 4D curvature with sympy
python -m research.variational_gravity_gate_v1.check_einstein_symbolic
python -m unittest discover -s tests -p 'test_variational_gravity_gate.py' -v
```

In this standalone local archive, run the files directly; the `source/` copy contains pinned exact core blobs. The scripts regenerate `results/audit.json`, `results/signal_gate.json`, `results/einstein_symbolic.json` only upon explicit execution; **no engine/core file is modified**. The JSON receipt pins the five core Git blobs from commit `c5a23743d96936190210dd510105ed470d4a0b23`; this pins the immutable law even if the documentation gets newer commits. The core action audit requires only Python's standard library; the optional curvature check uses SymPy.

Exact tests: 5,000 random huge-integer coordinate inversions; 601 integer interpolation values; 16 signed/dimension full-board snapshots with **34,944 complete channel updates** and inverse checks; 240 centered exact `V` gradients; one exact rational noncommuting symplectic Jacobian; 1,000 rational tensor-jet identities; 16 independently rebuilt clock/pulse runs, 3,072 explicitly checked scalar-channel spatial stencil values, three periodic Fourier kernels, and a separate symbolic Einstein-tensor computation. Seven regression tests passed in a clean mocked repository tree.

### What would actually count as progress to general relativity?

* Identify an **independently calibrated** family of clocks and minimally invasive probes, not only prepared recurrence periods.
* Obtain physical signals with a reproducible amplitude- and phase-independent long-wavelength light cone; measure `N`, spatial scale and PPN gamma on **held-out** cases.
* Obtain a localized source with measurable propagation outside its near halo, and independent energy/momentum/stress definitions; derive covariant balance in a coarse-grained limit.
* Only then construct a nondegenerate metric from operational measurements and test Einstein constraints and dynamics without defining `T_mu nu` as whatever makes the equation true.

This report is **a genuine exact variational structure an exact inverse-distance spatial Green kernel, and a precise Einstein-facing falsification test, not a derivation of Einstein gravity**. Its negative and limited cases are part of the evidence and must not be dropped.
