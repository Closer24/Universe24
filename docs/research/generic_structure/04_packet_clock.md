# A native massive packet with phase and motion in three retained channels

Baseline: `8c53e69f4b466dcbd2da7dab7e3c365bd9731766` (PR #52).
Executable: `validation/generic_structure/packet_clock.py`. Fresh evidence:
`runs/generic-structure/packet_clock.json`.

This source-only construction extends the existing native three-channel wave
control by a skew on-site mass term. An actual Engine packet now moves through
the board while its two retained real fields supply a measurable spectral
phase. No new retained field is added: one computational sign plus two real
wave fields occupy three channels, nine integers per node. The sign remains
computational scheduling, not physical proper time.

The demonstrated packet is localized in one coordinate and uniform in the
other two before carry perturbations. It is a classical linear field control
on a fixed flat lattice, not a three-dimensionally localized particle, a
quantum spinor, a detector, or the common45 Einstein–matter law. Rotating the
selected lattice axis constructs a separately fingerprinted permutation of
the law; no single isotropic three-dimensional tensor is claimed.

## 1. One fixed-six law, including a massive gap

Let the sign channel have old slices `s_a,s_b`, initially both one. It evolves
by `(s_a,s_b) -> (s_b,-s_a)` under `u_s=0`. For retained wave values `b_1,b_2`
and one selected face direction `e`, set

\[
u_1=s_as_b\,[b_1(x+e)-b_1(x-e)+\mu b_2(x)],
\qquad
u_2=s_as_b\,[-b_2(x+e)+b_2(x-e)-\mu b_1(x)].
\]

Every summand has degree three, reads one old snapshot and occupies the target
and at most one face edge. The only old-`a` dependency is sign-to-wave, hence
acyclic. `mu` is a fixed exact integer tensor coefficient. The actual Engine
still performs only

\[
\ell,r'=\operatorname{divmod}(2u+r,6),\quad a'=b,\quad b'=\ell-a.
\]

Prepare and decode physical amplitudes with a static scale `S`:

\[
Y_{n-1}=-s_ba/S,\quad Y_n=s_ab/S.
\]

With \(\sigma_3=\operatorname{diag}(1,-1)\) and
\(J=\begin{pmatrix}0&1\\-1&0\end{pmatrix}\), the exact decoded identity is

\[
Y_{n+1}=Y_{n-1}+
\tfrac13(\sigma_3\Delta_e+\mu J)Y_n+\eta_n,
\qquad
\eta_n=\frac{s_b(r_n-r_{n+1})}{6S}.
\]

Carries are retained. Their parity is invariant because the numerator adds
`2u`, so `r-r_next` belongs to `{-4,-2,0,2,4}` and
\(|\eta_n|\le2/(3S)\). This is deterministic forcing, not noise assumed to
average away. No floating-point arithmetic occurs in state evolution.

With physical `dt=dx/3`, the formal low-frequency equations are

\[
\partial_tY=\sigma_3\partial_xY+mJY,\qquad m=\mu/(2\,dx).
\]

Since \(\sigma_3J+J\sigma_3=0\), each real component obeys the massive
Klein–Gordon equation \(Y_{tt}=Y_{xx}-m^2Y\). This factorization explains the
mass gap and dispersive motion; it does not infer quantum statistics.

## 2. Independent discrete dispersion and a stability bound

For the ideal recurrence with the carry term removed, a spatial mode
\(e^{ikx}\) has positive-frequency branch

\[
\sin^2\omega=\frac{4\sin^2k+\mu^2}{36},\qquad
\omega(k)=\arcsin\frac{\sqrt{4\sin^2k+\mu^2}}6.
\]

Here `omega` is radians per Engine tick and `k` radians per node. Its group
velocity and phase derivative along its central ray are

\[
v_g=\frac{d\omega}{dk}
=\frac{\sin k\cos k}{9\sin\omega\cos\omega},
\qquad
\frac{d\theta}{dn}\bigg|_{x=v_gn}=\omega-kv_g.
\]

The field's rest angular frequency is \(\omega_0=\arcsin(|\mu|/6)\).
The computational branch of this two-time scheme is retained rather than
erased; two-slice eigenmode preparation suppresses it in the ideal initial
data, and carry/quantization errors can excite it.

For a Fourier mode, define the Hermitian matrix

\[
B=\begin{pmatrix}-\sin k/3&i\mu/6\\-i\mu/6&\sin k/3\end{pmatrix},
\quad M=\begin{pmatrix}-2iB&I\\I&0\end{pmatrix},
\quad H=\begin{pmatrix}I&iB\\-iB&I\end{pmatrix}.
\]

The executable proves symbolically `M* H M = H` and
\(B^2=(4\sin^2k+\mu^2)I/36\). Therefore the ideal scheme is uniformly
stable if \(\sqrt{4+\mu^2}<6\). At `mu=1`, with
\(r_*=\sqrt5/6\),

\[
\|M^n\|_2\le C=\sqrt{(1+r_*)/(1-r_*)}.
\]

Parseval and variation of constants bound the normalized two-slice RMS error
from carries by \(2CN/(3S)\). Rounding each prepared slice contributes at
most \(C\sqrt2/(2S)\). The reported bound is their sum; the Engine output is
compared with the independent ideal spectral prediction, not assumed to have
an exactly linear dispersion despite its carries.

## 3. Actual localized packet, then held-out checks

The packet is a finite-band Gaussian-weighted superposition of seven modes
around mode 4 on `L=32`. Only the initial two real slices are prepared. The
Engine advances all 32,768 nodes; no future packet coordinates, callback or
Fourier update feeds the retained state. All six initial carry classes occur.
Passively extracting the occupied Fourier band supplies an envelope and phase.

At `mu=1`, `S=2^24`, 64 actual updates:

| Quantity | Positive packet on x | Negative packet on y |
|---|---:|---:|
| Actual displacement in nodes | 12.61347819 | -12.61347780 |
| Measured circular-centroid velocity | 0.1970830853 | -0.1970830836 |
| Independent finite-band centroid prediction | 0.1970830812 | -0.1970830812 |
| Spectral weighted group prediction | 0.1987628124 | -0.1987628124 |
| Central phase frequency measured | 0.2928427714 | 0.2928427720 |
| Central phase frequency predicted | 0.2928427717 | 0.2928427717 |
| Final field RMS error | 7.88e-8 | 8.71e-8 |
| Deterministic error upper bound | 3.83e-6 | 3.83e-6 |
| Changed carry entries | 2,752,544 | 2,772,324 |
| Maximum retained bits | 25 | 25 |
| Complete rewind | exact | exact |

The finite bandwidth and circular centroid explain the difference between
the weighted derivative-of-dispersion estimate and the full finite-band
prediction. These are reported separately. The exact spectral prediction
does not get fitted to the Engine trajectory.

An independent scalar-coordinate oracle, without Tensor evaluation or its
neighbor-index map, checks 24 updates on random signed states along each
coordinate axis: 17,496 register comparisons and 2,633 changed carry entries.
Each state inverts exactly. Initial and final complete-state hashes and law
fingerprints are in the report.

Separate plane-wave runs check rest, low wave number, intermediate wave
number, the opposite direction and a high-frequency case. All use the same
mass coefficient and no frequency recalibration. The rest field's actual
upward zero crossings occur at ticks 10 and 47 in an 80-tick observation;
the predicted period is about 37.52 ticks. These are sampled field crossings,
not operational detector clicks. The phase fit gives rest frequency
0.1674480777 against the independent 0.1674480792 prediction.

## 4. Failed claims and negative controls remain visible

1. **A lattice phase is not already proper time.** At the packet's central
   `k=pi/4`, `(omega-k*v_g)/omega0` is 0.806051652 while the continuum SR
   clock factor using low-frequency speed `c=1/3` is 0.797724035. At
   `k=pi/2`, group speed is zero but the phase rate is over 2.28 times the
   rest rate. Calling every zero-group-speed pattern the same physical clock
   would fail. No exact finite-spacing Lorentz invariance is asserted.
2. **Central-difference doubling is present.** The actual Nyquist mode has
   the same frequency gap as the zero mode. This is preserved as a failure
   control, not identified as a new particle species.
3. **Massless uniform data do not tick.** With `mu=0`, a spatially constant
   physical field remains constant for 24 actual updates, with exact rewind.
4. **Reversibility is not stability.** With `mu=7`, outside the proved margin,
   a uniform control amplifies by over 1.27 million in 24 updates and still
   rewinds exactly.
5. **Fixed-mass refinement remains blocked for this primitive.** Because
   `m=mu/(2*dx)`, refining `dx` while holding physical `m` fixed requires
   `mu=2*m*dx`. This cannot remain a nonzero integer coefficient at arbitrary
   refinement. A counted schedule/quotient construction or a different
   encoding is needed. Raising amplitude scale `S` controls carries but does
   not fix this coefficient obstruction.

The spectrum is a useful necessary clock/transport test. A true proper-time
clock additionally needs an independently ticking material mechanism, a
worldline, universal calibration, and a local record/readout. The FFT and
transverse average here are passive global diagnostics, not such an apparatus.

## 5. Relation to common45 and the next integration gate

The script builds common45 and compares its actual tensor fingerprint with
this primitive's fingerprint: they differ. The common45 shared massive field
does source geometry, but its previous phase audit had only a few fine steps
and a separate coarse oscillation; this new stable long packet does not
transfer that source or curved geometry into its own tensor.

Simply adding these three channels to common45's 45 would total 48 but would
still create an uncoupled additional field and a second calibration. Adding
the new stencil to common45 also cannot directly reuse its projective
coordinates as native chiral variables. Multiplying this already cubic
sign-controlled derivative by a dynamic geometric factor would exceed the
degree bound. Thus budget arithmetic is not an integration proof.

The concrete next gate is a counted native schedule that supports refinable
mass and shared frame-dependent propagation while preserving the complete
state and a stability bound. That same law must then pass sourced Einstein
constraints, curved packet motion and material-clock calibration. No supported
runtime mode or accepted physical model was added by this audit.

Reproduce with:

```bash
python -m validation.generic_structure.packet_clock
```
