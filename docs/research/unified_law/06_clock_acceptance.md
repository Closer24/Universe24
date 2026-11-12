# Clock and source acceptance on the selected common law

The selected candidate is the five spinor/log-frame coordinates compiled into
**one six-channel projective Rule3 law**, not the alternative harmonic-time
compiler experiment. All evolution in this report uses
`validation.unified_law.common`; the clock lane does not create another tensor
builder or alter an Engine state. The scalar, geometry, dust and clock readout
are decoded from the same retained state.

Run `python -m validation.unified_law.clock_acceptance`.
Fresh evidence is `runs/unified_law/06_clock_acceptance.json`.

## Physical time, source and phase

The physical fields are beta, k, phi, p and signed dust amplitude d, with

\[
ds^2=-dt^2+e^{-2\beta}(dx^2+dy^2+dz^2),\qquad B=e^\beta.
\]

The independently written target equations are

\[
\dot\beta=k,\quad
\dot k=3k^2-\tfrac12(m^2\phi^2+d^2),\quad
\dot\phi=p,\quad
\dot p=3kp-m^2\phi,\quad
\dot d=\tfrac32kd.
\]

Here t is normal proper time in lapse one and zero shift; the selected compiler
does not change lapse. Assigning a physical timestep is a continuum numerical
interpretation, not a claim that a retained detector has recorded that interval.

With

\[
\rho=\tfrac12(p^2+m^2\phi^2)+d^2,\qquad
\mathcal P=\tfrac12(p^2-m^2\phi^2),
\]

direct differentiation gives

\[
\dot\rho=3k(\rho+\mathcal P),\qquad
D=d^2e^{-3\beta},\qquad\dot D=0.
\]

D is the conserved comoving dust mass. This condition is checked independently
of the Friedmann identity. A decoder that sets the constraint to zero could
still violate source continuity; success of one is not substituted for the other.

For a nonzero neutral radial massive scalar, define locally

\[
\theta=\operatorname{atan2}(-p,m\phi).
\]

Its exact proper-time rate is

\[
\dot\theta=m-\frac{3km\phi p}{m^2\phi^2+p^2}.
\]

The bound \(2m|\phi p|\le m^2\phi^2+p^2\) gives strict monotonicity when
\(|3k|<2m\). The phase is a matter diagnostic; a winding counter, correction
integral and autonomous readout device are not hidden in the retained state.

## A global continuum clock domain for the selected seed

The spinor decoder has k<=0 and
\(C=6k^2-p^2-m^2\phi^2-2d^2=0\) identically. On that surface,

\[
\dot k=\tfrac12(p^2+d^2)\ge0.
\]

The shared seed has k=-1/2, phi=1, p=0, d=1/2 and beta=0, with m=1.
Consequently -1/2<=k(t)<=0 forward in the continuum solution, so
\(|3k|\le3/2\) and \(\dot\theta\ge1/4\). The weighted spinor norm is
-k, which is nonincreasing, so the polynomial spinor ODE remains bounded and
extends globally forward. Beta has bounded derivative. The scalar pair cannot
vanish at a finite time, by uniqueness of its homogeneous linear equations.
Thus this is a global forward continuum phase-domain result for this seed,
not merely an initial-slice inequality.

This proof does not give a global discrete bound on k for arbitrary timestep.
The actual tested trajectories are checked sample by sample. Their minimum
observed margin \(2-|3k|\) is 1/2.

## Actual fixed-time experiment

Before running, the lane declared:

- common initial spinors `(sa,sb,sc,se)=(1,0,0,0)`, beta=0;
- D=4, zero old registers, all six remainder classes on 27 nodes;
- endpoint proper time T=1/8 and N=3,4,6 updates, h=T/N;
- decreasing field, phase and dust-mass errors across the three resolutions;
- finest phase error below 0.005 and relative dust-mass error below 5%.

These are three separately fingerprinted immutable tensors in the same equation
and physical-decoder family. The default h=1/24 tensor is
`8d5f0fad5d094908afd4e78d05e60710b96c95943bb7aa791e5b753ff33e9df9`;
the complete common seed is
`61b79e0831d775508ab04086aa4f4009d89bb6df95e2357e4ee7e5ff2777097f`.
The other exact fingerprints are stored in the evidence. No history or remainder
is discarded when changing preparation between separate runs.

Each actual tick passes the independent scalar integer oracle, local inverse and
complete rewind. The physical constraint is exactly zero at every sample.
All sampled B are positive, scalar phi and d are positive, and the measured
scalar phase strictly increases. The passive physical-coordinate RK4 reference
uses 4096 steps and agrees with its 2048-step check to 1.12e-15 at the endpoint.
It imports no spinor RHS and never feeds an Engine update.

| N | h | Largest physical-field error | Phase error | Dust-mass error | Peak retained bits |
|---:|---:|---:|---:|---:|---:|
|3|1/24|0.0034242880|0.0033019708|0.0000566967|207|
|4|1/32|0.0025445299|0.0024540889|0.0000415093|649|
|6|1/48|0.0016808920|0.0016214385|0.0000270201|6101|

Observed field orders are 1.032 and 1.023; phase orders are 1.032 and 1.022;
dust-mass orders are 1.084 and 1.059. This is actual fixed-time first-order
convergence evidence, not an efficient-storage or arbitrary-spatial-resolution
theorem. The cubic projective denominator cost is explicit and remains severe.

## Two exact negative controls survive the new constraint identity

**Dust mass is not exactly conserved by the finite map.** At the three endpoints
the value is strictly greater than 1/4. This is certified with rational bounds,
not decided only by floating-point differences. For rational x=-3beta>=0,
sum the exponential Taylor series through degree 14. All omitted-term ratios are
at most x/16, so

\[
\sum_{j=0}^{14}\frac{x^j}{j!}
\le e^x\le
\sum_{j=0}^{14}\frac{x^j}{j!}
+\frac{x^{15}/15!}{1-x/16}.
\]

Multiplying by the exact rational d squared gives a strictly positive lower
bound for D-1/4 in every run. The drift decreases under the declared refinement;
it is not silently relabeled as exact discrete source conservation.

**Phase divided by mass is not proper time.** At every tested endpoint the exact
rational inequality \(0<-p/\phi<1/8\), together with atan(x)<x for x>0, proves
\(\theta<T\). The independent continuum reference likewise gives
\(\theta(1/8)=0.11423226109711956\), whereas T=0.125. Refinement approaches
this expansion-corrected physical phase rather than an ideal flat-clock value.
The endpoint target fields are approximately

\[
(\beta,k,\phi,p,d)=
(-0.0615722011,-0.4854564312,0.9926565377,-0.1138892128,0.4558891996).
\]

An accepted operational clock would still need a retained measurement mechanism,
calibration, signal transport and appropriate moving-clock controls. The current
homogeneous sector contains no spatial packet or apparatus.

## Literature and scope

[Husain and Pawlowski, 1108.1145](https://arxiv.org/pdf/1108.1145), equations (1),
(5),(10)–(13), derive an irrotational dust time variable and show that propagation
of the gauge T=t fixes lapse one. Their framework motivates treating dust time
as a physical gauge with a source, not equating every computational scheduler to
a clock. [Their cosmology paper,1108.1147](https://arxiv.org/pdf/1108.1147), §2,
discusses homogeneous matter with that time gauge. [Brown and Kuchar,
gr-qc/9409001](https://arxiv.org/pdf/gr-qc/9409001), introduction, distinguishes
physical reference dust from coordinate conditions whose backreaction is omitted.

Those sources do not provide this Rule3 construction or the measured results.
The scalar-phase/source identities above and the exact rational certificates
are derived in this lane for the same selected candidate. General Einstein
evolution, spatial geodesic transport, efficient refinement and operational
clock acceptance remain outside this result.
