# Actual time-map failure and a native stable linear-wave sector

Date: 2026-11-12. Starting source: PR #50,
`62202fdccdd9a40d5dbbec104de6f97d9587a999`.

**Outcome.** The actual projective map fails a uniform wave-CFL stability
test, including its retained history. A separate, three-channel native
linear-wave tensor has a proved Fourier bound, controlled fixed-six carry
error, fixed-physical-time convergence and logarithmic retained bit growth.
The latter is a completed linear sector, **not** a nonlinear Einstein
integrator and **not** the corrected45 tensor.

Reproduce from the repository root:

```sh
python -m validation.completion.time_stability
```

Evidence: `runs/completion/time_stability.json`. The source-only executable
is `validation/completion/time_stability.py`; production Engine is unchanged.
Initial issue discussion: https://github.com/Closer24/Universe24/issues/40#issuecomment-6810761475.

## 1. Primary literature and what can be transferred

* Rein and Tamayo, [JANUS](https://arxiv.org/pdf/1704.07715), §§2.1–2.4:
  integer endpoint arithmetic can preserve exact reversal even when a
  force is rounded. Its floating-point force and per-step rounding are
  not an implementation under this project's immutable polynomial law.
* Celledoni et al., [Integrability properties of Kahan's method](https://arxiv.org/pdf/1405.3740),
  introduction, equations (1)–(4): polarization yields a rational,
  linearly implicit map, with modified invariants for specified systems.
  A matrix inverse or cancellation in a rational expression does not by
  itself supply counted integer registers or a legal fixed-six update.
* Marsden, Patrick and Shkoller,
  [Multisymplectic geometry, variational integrators, and nonlinear PDEs](https://arxiv.org/pdf/math/9807080):
  deriving a discrete field law from an action is the appropriate route
  to discrete multisymplectic and momentum identities. Exact rewind
  alone is not such a derivation. No discrete Einstein action is claimed here.

All the specific estimates below are derived for the actual map; none is
inferred merely from a paper's use of the words reversible or symplectic.

## 2. Exact instability of the PR47/50 projective memory map

Let the semidiscrete linear wave sector have one skew mode
\(\dot y=i\omega y\), put \(\theta=h\omega\), and use the existing preparation
\(P_{-1}=D_{-1}=0\), \(D_0\ge2\). For \(d\in\{2,3\}\), the actual integer law is

\[
D_{n+1}=C D_n^d-D_{n-1},\qquad
P_{n+1}=C D_n^{d-1}(1+i\theta)P_n-P_{n-1},\qquad C\ge2.
\]

Static denominators of \(\theta\) are cleared in \(C\). These are not
runtime divisions. Every tensor input is a multiple of three, so every
legal remainder is retained unchanged and this recurrence is exact.

Inductively \(0\le D_{n-1}<D_n\) and \(D_{n+1}\ge D_n^d>0\). Decoding only
the current numerator, \(y_n=P_n/D_n\), gives exactly

\[
y_{n+1}=(1+\epsilon_n)(1+i\theta)y_n-\epsilon_n y_{n-1},
\qquad \epsilon_n=D_{n-1}/D_{n+1}\ge0.
\]

The first step is \(y_1=(1+i\theta)y_0\); the zero old numerator is a memory
boundary, not an assumed physical past slice.

**Theorem.** For nonzero \(y_0\) and real \(\theta\),

\[
|y_N|\ge(1+\theta^2)^{N/2}|y_0|.
\]

**Proof.** For \(\theta>0\), start with \(R_1=y_1/y_0=1+i\theta\).
If \(R_n=x+iy\) has \(x\ge1,y\ge\theta\), then it is nonzero and

\[
R_{n+1}=(1+\epsilon_n)(1+i\theta)-\epsilon_n/R_n.
\]

Thus

\[
\Re R_{n+1}=1+\epsilon_n-\frac{\epsilon_n x}{x^2+y^2}\ge1,
\quad
\Im R_{n+1}=(1+\epsilon_n)\theta+
\frac{\epsilon_n y}{x^2+y^2}\ge\theta,
\]

using \(x^2+y^2\ge x\). Multiply the resulting bounds
\(|R_n|\ge\sqrt{1+\theta^2}\). Negative frequency follows by conjugation;
zero frequency is constant under this preparation. QED.

For a centered spatial wave eigenmode,
\(\omega=c\sin\kappa/\Delta x\). Under \(h=\nu\Delta x\), a nonzero fixed
resolved \(\kappa\) gives fixed \(\theta=c\nu\sin\kappa\). At fixed physical
time \(T\), \(N=T/h\to\infty\) and the lower bound diverges exponentially.
Consequently this frozen sector has **no uniform wave-CFL stability bound**.
This does not establish nonlinear blowup or deny a fixed-spatial-grid,
small-\(h\) limit: for fixed \(\omega\), the same lower bound tends to one.

The real two-component Engine implementation tests the mode with
\(\theta=1/3\), positive and negative seeds, all six carries and an
independent integer oracle. At degree two, ten steps reach 3,671 retained
bits; amplitude ratio is 1.69378359, versus the proved bound 1.69350878.
At degree three, six steps reach 2,036 bits and ratio 1.37174218.
Every complete state rewinds exactly.

The cost is also a theorem. Since
\(D_n^d\le D_{n+1}\le C D_n^d\),

\[
d^n\log D_0\le\log D_n\le
d^n\left(\log D_0+\frac{\log C}{d-1}\right)-\frac{\log C}{d-1}.
\]

Retained denominator bit length is \(\Theta(d^n)\). Small channel count
does not make this bounded-memory evolution.

## 3. Why an orthogonal Cayley step plus a linear denominator is insufficient

Consider the tempting repair \(D_{n+1}=C D_n-D_{n-1}\),
\(P_{n+1}=C R P_n-P_{n-1}\), where \(R\) is a rational rotation with
eigenvalue \(e^{i\phi}\), \(C>2\), and \(CR\) has integer entries. Its
first decoded step is exactly the norm-preserving rotation.

Write \(\rho+\rho^{-1}=C\), \(\rho>1\). The denominator grows like
\(\rho^n\); numerator eigenvalues satisfy
\(\lambda+\lambda^{-1}=C e^{i\phi}\). For the larger root \(r=|\lambda|\ge1\),

\[
|\lambda+\lambda^{-1}|^2
=(r+r^{-1})^2\cos^2\psi+(r-r^{-1})^2\sin^2\psi.
\]

If \(r\le\rho\), this is at most \(C^2\), with equality only when
\(r=\rho\) and \(\psi=0\) or \(\pi\). A non-real rotation therefore forces
\(r>\rho\); with the zero-old preparation the growing coefficient is
nonzero, so decoded amplitudes grow as \((r/\rho)^n\). Linear bit growth
fixes one cost problem but not the retained-history stability problem.

The executable checks the exact Cayley example
\(R=\frac15\begin{pmatrix}3&-4\\4&3\end{pmatrix}\), \(C=5\), for 120 Engine
steps, all carries and exact rewind. This is a failed proposed repair,
not a general impossibility theorem about every rational encoding. At step
120 its decoded amplitude is 753.439864 while maximum retained bit length
is 282; the first-step amplitude is exactly one.

## 4. A legal three-channel native bidirectional wave

Use three retained channels: one shared sign \(s\), and fields \(b_+,b_-\).
There are **nine retained integers per node**, including all old slices and
remainders, with no denominator, auxiliary history or runtime callback.
The immutable polynomial inputs are

\[
u_s=0,\qquad
u_\sigma(x)=\sigma s_a(x)s_b(x)
\bigl[b_\sigma(x+e_x)-b_\sigma(x-e_x)\bigr],\qquad \sigma\in\{+1,-1\}.
\]

Each summand has degree three and touches one face edge. The only old-\(a\)
dependency is from the sign to a wave field, an acyclic graph. The sign
starts uniformly with \(s_a=s_b=1\), evolves by
\((s_a,s_b)\mapsto(s_b,-s_a)\), and keeps every legal sign remainder.

The tensor explicitly marks these sign-to-wave terms as one-way
computational control. The phase is fully counted but is neither a proper
clock nor a demonstrated reciprocal source or detector. This designation
does not waive the reciprocity obligations of a future physical model.

For a preparation/readout amplitude \(S\), define

\[
y_{n-1}=-s_b a_\sigma/S,\qquad y_n=s_a b_\sigma/S.
\]

No division by \(S\) occurs inside the Engine. Its sole quotient remains
\(\operatorname{divmod}(2u+r,6)\). Because
\(\ell=u/3+(r-r')/6\), the exact decoded recurrence is

\[
y_{n+1}(x)=y_{n-1}(x)+\frac{\sigma}{3}
\bigl[y_n(x+e_x)-y_n(x-e_x)\bigr]+\eta_n(x),
\quad \eta_n=\frac{s_b(r_n-r_{n+1})}{6S}.
\]

In particular \(|\eta_n|\le5/(6S)\), for every allowed carry. Carries are
**not assumed zero or discarded**. With \(h=\Delta x/3\), the limiting PDE is
\(\partial_t y_\pm=\pm\partial_x y_\pm\). Their sum and difference give
\(q_t=v_x\), \(v_t=q_x\), hence \(q_{tt}=q_{xx}\). This is a nontrivial
flat, massless, one-spatial-direction wave sector on the periodic cube.

## 5. Uniform Fourier bound and fixed-time refinement proof

For the ideal recurrence without \(\eta\), a mode \(e^{i\kappa x}\) evolves
its two-time vector by

\[
M=\begin{pmatrix}2ia&1\\1&0\end{pmatrix},\qquad
a=\frac{\sigma\sin\kappa}{3}.
\]

Define

\[
H=\begin{pmatrix}1&-ia\\ia&1\end{pmatrix}.
\]

Direct multiplication gives \(M^*HM=H\), verified symbolically in the
executable. The eigenvalues of \(H\) are \(1\pm a\), within \([2/3,4/3]\).
Therefore \(\|M^n\|_2\le\sqrt2\), uniformly in mode, mesh and step count.
This includes the computational branch, zero mode and Nyquist mode.
Parseval gives the same bound on the full spatial two-slice norm.

Compare the quantized Engine output with the ideal scheme from the same
decoded initial pair. Variation of constants and the carry bound give

\[
\|e_N\|_{2,\mathrm{pair}}
\le\sqrt2\,\frac{5N}{6S}.
\]

Here spatial/field means are normalized, and the two time-slice squares
are summed. No independence, randomness or cancellation of carries is used.

For a smooth periodic solution, Taylor expansion gives a per-step
consistency defect \(O(h^3+h\Delta x^2)\). At \(h=\Delta x/3\), fixed
\(T=Nh\), and a second-order prepared past slice, stability therefore gives

\[
\|y_N-y(T)\|_2
\le C_T\Delta x^2+C/S+\sqrt2\,5N/(6S).
\]

Take \(\Delta x=1/L\), \(S=L^3\). Since \(N=O(L)\), both truncation and
worst-case carry error are \(O(L^{-2})\). The integer-amplitude choice is
made once during preparation; the tensor is identical at all resolutions.

For bounded initial physical data, the norm bound also controls every
retained integer by a polynomial in \(S,N,L\): for instance the normalized
cube norm yields a peak bound of order \(L^{3/2}(S+N)\), up to fixed
constants. Thus maximum retained bit length is
\(O(\log S+\log N+\log L)\), and specifically \(O(\log L)\) at fixed \(T\)
with \(S=L^3\). The total lattice storage still grows with the number of
nodes, as it must. No all-time bounded-energy claim is made for arbitrary
carry forcing at fixed \(S\).

## 6. Executed evidence and negative controls

The native tensor fingerprint is
`fc12313fdbe2110e55d26c64cf4eb5ffe6c3a3b4ab4486fdc827eeb7205900d4`.

Independent scalar address arithmetic agrees with the actual Engine for
180 steps on signed, spatially varying seeds: **43,740 register
comparisons**, **6,485 changed carry entries**, all six initial remainders,
complete rewind and maximum eight retained bits. The exact decoded carry
identity is checked after clearing its factor of six.

Fixed physical time \(T=1/3\), two smooth opposite waves, second-order
backward Taylor preparation from initial data and derivatives:

| L | Steps | S | Continuum RMS error | Observed order | Maximum bits |
|---:|---:|---:|---:|---:|---:|
| 12 | 12 | 1,728 | 0.055487916 | — | 11 |
| 24 | 24 | 13,824 | 0.013432057 | 2.046 | 14 |
| 48 | 48 | 110,592 | 0.003300177 | 2.025 | 17 |

All three runs use the same tensor, include nonzero carries and rewind the
complete state. Passive floating-point comparisons with the continuum and
the ideal linear scheme do not feed state evolution; the separate scalar
integer oracle establishes exact mechanics. The measured carry-pair RMS
errors are 0.000828714, 0.000143022 and 0.0000264044, below the respective
proved bounds 0.00818411, 0.00204603 and 0.000511507.

Multiplying the native stencil coefficient by three changes the Courant
number to one. At \(\kappa=\pi/2\), \(M\) has a repeated unit eigenvalue
with a Jordan block. An actual integer seed grows from amplitude one to
40 after 40 steps. Coefficient four gives \(\nu=4/3\) and amplitude
43,201,214,264,023 after 40 steps. Both still rewind exactly. These negative
controls distinguish stability from reversibility and show why a strict
Courant margin is part of the proved construction.

## 7. Scope and handoff

| Gate | Status |
|---|---|
| Actual projective frozen-mode amplification theorem | passed |
| Projective uniform wave-CFL stability | failed |
| Naive Cayley plus linear-D history repair | failed |
| Native fixed-six linear-wave scalar oracle and complete rewind | passed |
| Uniform ideal Fourier bound and controlled carry forcing | passed |
| Fixed-time second-order native linear-wave refinement | passed |
| Logarithmic per-integer bit growth for the proved refinement family | passed |
| General nonlinear Einstein time integration within 48 channels | blocked |
| Same corrected45 tensor, source constraints, proper material clock | not_tested |
| Nonlinear energy/Noether identities or full Einstein acceptance | not_tested |

The native sign factors already consume degree three for a linear
spatial derivative. Arbitrary fractional nonlinear coefficients and
variable geometry require a new counted construction; this proof does not
provide one. Kahan polarization remains a rational candidate, not a legal
runtime inverse. The native compiler agent's separate potential-shear
primitive is a possible dependency, not an integrated drift-kick proof.
Similarly, preserving a metric determinant does not alter the projective
amplification theorem or its bit-growth bound. These gates must not be
combined across different tensors into a claim of complete Einstein dynamics.
