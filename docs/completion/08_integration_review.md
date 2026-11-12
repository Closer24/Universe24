# Independent integration review

Baseline: PR #50, `62202fdccdd9a40d5dbbec104de6f97d9587a999`.
Run **after the component audits**:

```sh
python -m validation.completion.integration_review
```

Source: `validation/completion/integration_review.py`.
Fresh evidence: `runs/completion/08_integration_review.json`.
The review reads exact component evidence and rejects stale source hashes.
It also executes independent Engine controls; it does not simply count green
component reports. The supported runtime and physical acceptance remain unchanged.

## 1. Which results really belong to the same run

The common runtime, massive clock and signal audits agree on:

- mass squared 1, h=1/64, dx=1/4;
- 45 total channels, 135 retained integers per node;
- tensor `6ea453fa77a5a9d74af5bd4fc626cfcdc8f92942b10c301d2d00814bf4d05ba0`;
- complete seed `b53909631f3e14e3c09905275fe7b50a0dad2ecdec9ac431db2306127abd3b7c`.

The seed includes every old/current numerator and all remainder registers.
Sharing only the decoded physical initial values is not enough for a same-run
claim. This review rebuilds the tensor/seed and compares both identities to the
runtime, clock, signal and constraint evidence records. Ownership remains exhaustive; no clock or particle
position bank is hidden in the passive diagnostic code.

Seven deliberately false joins are rejected: the coarse h=1/4 clock law,
massless control, cubic metric repair, native potential lift, native wave,
seven-channel joint compiler and reduced constraint history lift.
Copying the true seed hash into one of these claims does not make its tensor
the same. A changed complete seed under the true tensor is rejected as well.

The real bundle boundary rejects 49 channels. The actual common-bundle helper
also rejects a massless tensor under massive metadata and a changed remainder
under its exact prepared-seed metadata. There are **three jointly unallocated
slots**, not three independent allowances for every proposed subsystem.
Although 45+3 fits the numerical budget, a flat three-channel wave appended to
the 45-channel law would not by itself become a same-metric coupled sector.

## 2. Mathematical review

### Metric nondegeneracy

For symmetric K, the complete-square identity

\[
I+hK+h^2K^2=(hK+I/2)^2+3I/4
\]

is valid for arbitrary real amplitudes, not only small K. With the stated
zero-old preparation, the projective denominator gives
\(0\le\epsilon\le1/7\). If
\(X=B_{n-1}B_n^{-1}\) has norm at most two, then

\[
\sigma_{\min}((1+\epsilon)R-\epsilon X)
\ge3(1+\epsilon)/4-2\epsilon\ge4/7.
\]

Because \(B_{n+1}=A B_n\), the next history matrix is exactly
\(B_nB_{n+1}^{-1}=A^{-1}\); noncommutativity does not invalidate this step.
Its norm is at most 7/4, so the induction closes. The continuous path from
\((1+\epsilon)R\) to A stays nonsingular, preserving determinant sign.
The proof is therefore sound on its declared domain.

It proves finite-tick nondegeneracy, not a uniform continuum-limit condition
number or arbitrary-history positivity. More importantly, the repair changes
the finite-h dynamics. The sourced TT torsion defect in the metric audit is
retained as a **failed** constraint gate, and the linear constraint theorem for
the original formulation is not transferred to the repaired law.

### Native wave stability and a sharper carry estimate

Independent multiplication verifies \(M^*HM=H\) for

\[
M=\begin{pmatrix}2i\alpha&1\\1&0\end{pmatrix},\qquad
H=\begin{pmatrix}1&-i\alpha\\i\alpha&1\end{pmatrix}.
\]

For \(|\alpha|\le1/3\), the eigenvalues of H lie between 2/3 and 4/3,
so the stated Euclidean power bound \(\sqrt2\) follows, including both
time branches. The component's \(5/(6S)\) carry bound is correct but can
be sharpened. The unchanged fixed-six law implies

\[
r_{n+1}-r_n=2u_n-6\ell_n\equiv0\pmod2.
\]

Legal remainders with the same parity differ by at most four. Hence

\[
|\eta_n|\le\frac{2}{3S},\qquad
\|e_N\|_{2,\mathrm{pair}}\le\sqrt2\frac{2N}{3S}.
\]

This conclusion uses no statistical cancellation. The weaker original bound
still proves second-order fixed-time convergence when S=L cubed and N=O(L).
The bit argument controls integers by a polynomial in L, S and N, hence their
individual bit lengths logarithmically. Total storage still includes all
L cubed sites. This theorem remains a linear, flat, one-direction wave result;
it neither supplies a variable metric coupling nor repairs projective45.

### Native nonlinear lifting

The three-tick compiler has a counted scheduler and homogeneous quadratic
forces. The middle-stage sign is harmless precisely because the force has
even degree: F(-q)=F(q). A general nonhomogeneous force would need its own
proof. The independent review sums each positive face edge once, derives both
endpoint forces directly from
\(V_{ij}=\lambda(g_i+g_j)(\phi_j-\phi_i)^2\), and executes the actual
compiled tensor for three ticks with new signed coupling/drift values.

It verifies

\[
P'=P+2F(q),\quad q'=q+\ell a',\quad P=6a+r,
\]

full scheduler restoration, the scalar shift charge and complete rewind.
No component `forces`, macro oracle or inverse oracle is called in this
independent control. The potential-only refinement is a real subflow result;
the integer-drift scaling obstruction remains a scoped limitation of this
ansatz. Neither g nor the scheduler is a proven Einstein metric or physical clock.

The later nine-tick joint compiler is a distinct, stronger result and is
reviewed separately. Its seven channels comprise two data, two workspace and
three scheduler channels. With workspace carries prepared as 0 or 1 it realizes

\[
S^*=S+\lfloor P/18\rfloor,\qquad
P'=P+2F(S^*),\qquad S'=S^*.
\]

The independent audit uses new signed coupling values -3 and 2, mixed signed
data, both admitted workspace remainder values and all six data/clock
remainder classes. It obtains F from its own once-per-edge potential loop,
then compares the macro identity with nine actual Engine steps. Every
workspace/scheduler triple returns exactly; each microstep inverts, and the
full seed rewinds. Observed maxima are 13 and 12 bits in these two short tests.
This closes one concrete nonlinear drift-and-kick compilation problem, with
an actual quotient computed and uncomputed inside the tensor. Arbitrary
division depth, continuum refinement and full45 coupling are still absent.

### Reduced constraint target and retained history

The seventh researcher's decomposition \(F(z)=3kz+A(z)z\), with
\(A^TJ+JA=0\), yields a valid frozen Cayley preservation identity.
Multiplying its common denominator by \(1-3hk\) gives
\(C(z')=C(z)/(1-3hk)^2\). The reported sparse cancellations really leave
cubic numerators and a cubic denominator, and the excluded denominator-zero
domain is explicit. State dependence of A is not itself a global
invertibility proof; none is claimed.

The mandatory Rule3 subtraction of the retained old numerator adds
\(-2cN_{\mathrm{hom}}^TJP_{\mathrm{old}}\) to the quadratic constraint.
Two separately null vectors need not have null difference. The reviewed
five-channel lift therefore correctly reports exact zero at its first tick
and exact nonzero at its second. The tiny second-step value is compared as a
rational, not hidden under a floating tolerance. Its matching common45
first-step evidence and source hash are included in the integration guard.

### Massive clock and geodesics

The neutral scalar phase can also be derived directly from
\(\operatorname{atan2}(-p,mx)\), using
\(\dot x=p,\ \dot p=kp-m^2x\):

\[
\dot\theta=m-\frac{k m x p}{m^2x^2+p^2}.
\]

The inequality \(2|mxp|\le m^2x^2+p^2\) proves monotonicity for
\(|k|<2m\) on the nonzero radial sector. It does not make phase/m equal
proper time when k is nonzero. The actual coarse oscillation is on a different
tensor, is not exactly recurrent and has nonzero constraint drift. The fine
common run has no resolved period or operational detector.

The signal work differentiates the actual same-law matter equations and uses
the retained full B for its cones. Fixed-mass Klein–Gordon characteristics
remain null; the timelike eikonal/geodesic argument requires its stated
controlled limit. Analytic FLRW/Milne/Lorentz-force examples are independent
references and are not Engine-propagated localized packets. The reports retain
this boundary correctly.

## 3. Acceptance and source provenance

There is also an independently checked failure on the **exact shared weak
seed**, not just another tensor's counterexample. In the homogeneous neutral
sector write
\(C=6k^2-p^2-\phi^2-2d^2\). From the independently written reduced
velocities, \(\dot C=6kC\), whereas the first prepared projective step is
exactly Euler and obeys

\[
C_+=(1+6hk)C+h^2(6v_k^2-v_p^2-v_\phi^2-2v_d^2).
\]

At the common initial slice \(k=-1/10,\phi=1/5,p=0,d=1/10\), the
coefficient of \(h^2\) is exactly \(-403/10000\). Thus the shared
\(h=1/64\) tensor gives

\[
C_+=-403/40960000\ne0.
\]

The actual Engine reproduces this rational value and its complete state
still reverses. This proves a failed exact discrete-constraint gate on the
same law and same seed used for the clock/cone handoff. It does not rule out
controlled constraint convergence or a different legal temporal compiler.

The executable review verifies that the generic runtime still marks C–F
`not_tested`, that the coarse clock's constraint gate remains `failed`, and
that the metric repair's finite-h constraint failure remains visible.
Source hashes in component records must match the present reviewed files;
otherwise the review fails and requests that component's audit be rerun.

The current collection establishes useful mathematical and implementation
pieces, with one genuine shared massive45 runtime/clock/cone handoff. It does
not establish one nonlinear, stable, constraint-preserving Einstein model
with operational clocks within the budget. Exact reversal, constraint closure,
metric domain, continuum stability, calibration and bit cost are separate
obligations and cannot be combined across different tensors.

## 4. Primary reading

- [Rein and Tamayo, JANUS, arXiv:1704.07715](https://arxiv.org/pdf/1704.07715),
  §2: its exact reversible integer endpoint updates coexist with rounded
  floating-point force evaluations. The present contract requires the whole
  update to fit its immutable polynomial tensor, so reversibility literature
  alone does not provide that compilation or a physical acceptance theorem.
- [Celledoni et al., Integrability properties of Kahan's method,
  arXiv:1405.3740](https://arxiv.org/pdf/1405.3740), introduction, equations
  (1)–(4): polarization yields a rational map, and preserved modified
  invariants depend on the system. Its rational algebra/cancellation must not
  be confused with an admissible reversible retained-integer implementation.

The sharpened carry estimate and selected identities here were independently
derived from the fixed-six rule and actual candidate equations, not attributed
to either paper.
