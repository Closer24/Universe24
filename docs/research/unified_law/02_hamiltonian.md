# One canonical source and dust-time interpretation

This is researcher 2/7's independent Hamiltonian check of the **selected**
`spinor_beta_mass1` candidate. The shared vector field and physical decoder are
imported from `validation/unified_law/constrained_coordinates.py`; they are not
redefined here. Run `python -m validation.unified_law.hamiltonian`. Fresh evidence
is written to `runs/unified_law/02_hamiltonian.json`.

The result is an exact continuum identity and a finite-step acceptance
obligation. It does not infer an exact discrete conserved energy from an exact
algebraic Friedmann constraint.

## 1. Canonical variables from the same metric and matter

Use the selected homogeneous isotropic metric

\[
 ds^2=-dt^2+e^{-2\beta(t)}(dx^2+dy^2+dz^2),\qquad
 B=e^\beta,\quad v=B^{-3}=e^{-3\beta}>0.
\]

Here k is the diagonal extrinsic curvature in the repository convention,
so the Hubble parameter is -k and beta-dot=k. The scalar has mass squared one,
real homogeneous value phi and normal derivative p. The signed dust amplitude
d has physical energy density d squared. The scalar charge current, spatial
gradients, Maxwell field and anisotropy vanish in this restricted sector.

In units with 8 pi G=1 and a unit comoving reference cell, the gravitational
and scalar Lagrangian in proper time is

\[
 L_0=-\frac{\dot v^2}{3v}
       +\frac v2\dot\phi^2-\frac v2\phi^2.
\]

Thus the canonical momenta and Hamiltonian are

\[
 p_v=-\frac{2\dot v}{3v}=2k,\qquad \Pi=v p,
\]

\[
 H_0(v,p_v,\phi,\Pi)
 =-\frac34v p_v^2+\frac{\Pi^2}{2v}+\frac v2\phi^2.
\]

The inverse volume occurs in this continuum canonical interpretation and
passive decoder. It is not an additional inverse operation inside the compiled
integer tensor.

Introduce comoving dust energy E and its canonical time T. On the positive
dust-energy branch the homogeneous constraint and canonical action are

\[
 H_0+E=0,\qquad
 S=\int [p_v\dot v+\Pi\dot\phi+E\dot T-N(H_0+E)]\,d\lambda.
\]

Variation gives T-prime=N and E-prime=0. With N=1, the dust time is normal proper
time. The selected spinor candidate uses that same synchronous time, not a
state-dependent time rescaling.

## 2. Exact independent check of the selected spinor dynamics

Let k,p,phi,d be the quadratic physical outputs of the shared spinor decoder.
Its identity is

\[
 C=6k^2-p^2-\phi^2-2d^2=0.
\]

With E=v d squared this implies, algebraically at every decoded state,

\[
 H_0+E=-\frac v2 C=0.
\]

The executable derives the canonical equations directly from H0:

\[
 \dot v=-\frac32vp_v,\qquad
 \dot p_v=\frac34p_v^2+\frac{\Pi^2}{2v^2}-\frac12\phi^2,
\]

\[
 \dot\phi=\frac\Pi v,\qquad \dot\Pi=-v\phi.
\]

It then differentiates the actual shared decoder along the actual shared
five-coordinate vector field and verifies all four equations exactly. This
includes the common beta evolution, which fixes volume from the same geometry
used by the matter source.

The following identities also pass as exact symbolic polynomials:

\[
 \frac d{dt}(v d^2)=0,\qquad \dot H_0=0,
\]

\[
 \rho=\frac12(p^2+\phi^2)+d^2=3k^2,\qquad
 P_{\rm matter}=\frac12(p^2-\phi^2),
\]

\[
 \dot\rho=3k(\rho+P_{\rm matter}),\qquad
 \dot k=\frac12(p^2+d^2)\ge0.
\]

These are one scalar/dust stress ledger and one metric, not a test scalar with
its stress silently removed. The seed sa=1, sb=sc=se=beta=0 has
k=-1/2, phi=1, p=0, d=1/2, v=1 and E=1/4, so the dust is nonzero.

The selected parameterization covers the expanding branch k<=0. Its redundant
spinor phase remains part of the complete retained state; it cannot be deleted
merely because these physical observables are phase independent.

## 3. What the actual finite-step map must additionally satisfy

The passive decoder ensures C=0 for every real spinor, even for the wrong
spinor dynamics. As an exact negative control, double every spinor coordinate
and leave beta unchanged. The quadratic outputs k,p,phi,d all multiply by four.
Consequently C stays zero while

\[
 E_{\rm after}=16 E_{\rm before}.
\]

This transformation is only a counterexample in the decoder's domain; it is
not described as a candidate Engine step. It proves that an algebraic source
identity alone cannot certify the intended dust conservation or trajectory.

The shared Engine audit must therefore report, on its exact tensor and seed:

- complete-state oracle/inverse and rewind;
- the exact rational C residual from decoded spinors;
- comoving dust mass M=d squared times exp(-3 beta), relative to its initial
  value, at fixed physical endpoint and at three prepared resolutions;
- fixed-time errors in the scalar, momentum, curvature and log-frame against
  an independent continuum reference;
- retained integer bit growth and the exact same metric used in the clock
  comparison.

Finite-step M need not be exactly constant for an approximate consistent
integrator, but its drift must be measured and shown to converge under a stated
protocol. Setting E := -H0 afresh in a passive readout would make the Friedmann
identity tautological while allowing a physically changing dust mass. This
report does not use that operation as an acceptance shortcut.

A dust-time gauge is also distinct from an operational clock record. The
five physical coordinates plus a projective denominator contain no separately
retained T or detector pointer. If a retained T is added, its actual compiled
recurrence and channel ownership must be checked. Engine step number alone
does not establish a material recorded tick. Likewise, a scalar phase requires
the expansion correction and calibration checked by the clock researcher.

## 4. Quadratic harmonic-lapse interface for future native compilation

This appendix is an **unselected interface derivation**, not a competing
executed candidate and not an extra set of passed gates for the spinor law.
It records a possible bridge if native quadratic first-order dynamics can be
compiled more cheaply than the current cubic spinor dynamics.

Choose lapse N=v and harmonic parameter lambda. Set

\[
 P=v p_v=2vk,\quad \Pi=vp,\quad r=v\phi,
 \quad E=vd^2=\hbox{constant}.
\]

The closed four-coordinate system is quadratic:

\[
 v'=-\frac32vP,\qquad P'=-r^2-Ev,\qquad
 \Pi'=-vr,\qquad r'=v\Pi-\frac32Pr.
\]

Its quadratic Hamiltonian constraint and proper-time rate are

\[
 C_H=-\frac34P^2+\frac12\Pi^2+\frac12r^2+Ev,
 \qquad C_H'=0,\qquad T'=v.
\]

No independent phi register is required: phi=r/v. Direct differentiation
reproduces the homogeneous physical equations after division by T-prime=v.
The physical Friedmann constraint equals -2 C_H/v squared. The physical domain
requires v>0, E>=0 and C_H=0; the vector field alone does not provide a legal
native complete-state map preserving that domain. Thus its low degree is useful
compiler information, not evidence that this alternative has already solved
the remaining temporal implementation problem.

## 5. Primary reading and provenance

- Brown and Kuchař, [Dust as a Standard of Space and Time in Canonical Quantum
  Gravity](https://arxiv.org/pdf/gr-qc/9409001), introduction and sections II–III:
  dust proper time is a material canonical variable, and its stress is part of
  the gravitational system.
- Husain and Pawlowski, [Dust reference frame in quantum
  cosmology](https://arxiv.org/pdf/1108.1147), section 2, equations 1–3:
  the dust-time gauge gives a physical Hamiltonian without a square root of the
  remaining Hamiltonian in the stated dust model.

The normalization, canonical transformation, selected-spinor pushforward,
quadratic harmonic interface and counterexample above were derived explicitly
for this repository. No quantum, inhomogeneous, global gauge or operational
detector conclusion is inferred from those papers.

Initial coordination:
[issue 40](https://github.com/Closer24/Universe24/issues/40#issuecomment-6811710808).
