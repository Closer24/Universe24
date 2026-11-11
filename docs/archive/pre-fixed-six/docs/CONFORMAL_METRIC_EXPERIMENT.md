# A restricted common conformal metric within rank-four Rule3

This is a new isolated construction, not a claim about the default ONE tensor and not a solution of the Einstein equations. It provides a positive example in which coherent clock, link and interaction couplings admit one continuum metric interpretation without adding a separate attraction law.

Reproduce the two experiments from the repository root:

```sh
PYTHONPATH=. python experiments/geometry/conformal_metric_probe.py
PYTHONPATH=. python experiments/geometry/conformal_nonlinear_clock.py
```

Default outputs go to ignored `runs/geometry/`. The checked results are
[conformal_metric.json](evidence/conformal_metric.json) and
[conformal_nonlinear_clock.json](evidence/conformal_nonlinear_clock.json).
The runners and their readout conventions are documented in
[experiments/geometry](../experiments/geometry/README.md).

## Primary source and what is used

Gerard 't Hooft, *The Conformal Constraint in Canonical Quantum Gravity*, https://arxiv.org/pdf/1011.0061, equations1.2 and1.5–1.10, explicitly writes the conformal metric split and the transformed scalar kinetic, mass and quartic interaction terms. Only these classical field-redefinition identities are used here. The paper's quantum proposals, anomaly conditions and predictions are not assumed. Its discussion after1.12 also distinguishes the conformal Einstein-Hilbert kinetic sign from an ordinary scalar kinetic term. The present toy uses an ordinary positive-energy scalar kinetic term for its conformal factor and therefore is not the Einstein-Hilbert action.

## 1. Exact continuum algebra: why the quartic need not gain a fifth factor

Use signature(-+++) and curvature convention

    g_mu_nu=Omega^2 eta_mu_nu,   R(g)=-6 Omega^-3 Box_eta Omega,

with Omega positive. For each scalar phi_s take conformal curvature coupling xi=1/6:

    S_m=-1/2 integral sqrt(-g)[g^mu_nu partial_mu phi_s partial_nu phi_s
                              +(m_s^2+R/6)phi_s^2]
        -lambda/2 integral sqrt(-g) phi_1^2 phi_2^2.

Define canonical variables chi_s=Omega*phi_s. Integrating the mixed derivative term by parts, the transformed kinetic term produces +(Box_eta Omega/Omega)chi_s^2 inside the bracket. The R/6 term contributes its negative. They cancel, up to the stated boundary term. Consequently

    S_m=-1/2 integral[(partial chi_s)^2+m_s^2 Omega^2 chi_s^2]
        -lambda/2 integral chi_1^2 chi_2^2.

The mass coupling has degree four. The quartic interaction is independent of Omega because sqrt(-g)=Omega^4 cancels the four scalar field weights. Its omission from the explicit Omega source is therefore consistent with this particular conformal action; it is not an arbitrary failure to couple its energy. This is a trace/conformal sector, not coupling to all components of a general metric.

For minimally coupled scalars (xi=0), the cancellation fails and an additional geometric term remains. Thus the example must not be described as a minimally coupled scalar model on an arbitrary metric. Nor does this continuum field redefinition establish an exact finite-lattice Weyl symmetry of integer states.

This also limits the earlier direct degree-five obstruction: multiplying an already chosen canonical quartic by F is indeed degree five, but that particular multiplication is not required by every geometric field convention. The conformal example avoids it without an instantaneous product auxiliary.

## 2. One fixed reciprocal integer tensor

Let H be the integer conformal-factor gear, chi_1 and chi_2 two scalar gears, and z a massless signal gear. All have field sign+1. The complete input is

    u_chi_s=D chi_s+w Delta chi_s-mu_s H^2 chi_s-gamma chi_s chi_other^2,
    u_H=D H+w Delta H-sum_s mu_s H chi_s^2,
    u_z=D z+w Delta z.

Delta is the sum of the six face-neighbor values minus six times the local value. The gamma terms may be zero for the independent-clock test. Every variable, including H, is updated by the same exact scalar Rule3. H is not held fixed externally and no source is injected during a run.

These inputs are the gradient of the fixed unit-cell/edge potential

    Phi=D/2 sum_i b_i^2-w/2 sum_edges,i (b_i(y)-b_i(x))^2
        -1/2 sum_s mu_s H^2 chi_s^2-gamma/2 chi_1^2 chi_2^2.

Potential halves need not be integers; all differentiated input coefficients are integers. The input degree is at most three and tensor order at most four. All nonlinear terms are on site, each spatial term occupies one physical edge, and all inputs read old b. Reciprocity, strict support and staged inversion are checked by the repository's existing validators. This is chosen tensor data, not a derivation of its coefficients from Rule3.

## 3. Controlled scales and the role of remainders

The executable tests use an even refinement integer N and

    h=dt=1/N, A=N^6, P=A^2, Q=P^2 N^2, D=6Q, w=D/12,
    mu_s=3 m_s^2,   m_1=1,m_2=2,
    f_s=chi_s/A,   Omega=H/P.

If the quartic interaction is enabled, gamma=3A^2 gives continuum canonical coupling lambda=1. Otherwise gamma=0. Each N defines a separate fixed tensor and explicit seed; the divisor and coefficients never change during a run.

For homogeneous clocks the exact normalized recurrence is

    Delta_t^2 f_s/h^2=-m_s^2 Omega^2 f_s-lambda f_s f_other^2+eta_s/(A h^2),
    Delta_t^2 Omega/h^2=-(A/P)^2 Omega sum_s m_s^2 f_s^2+eta_H/(P h^2),

where eta=(r-r_next)/D and |eta|<1. Hence the integer-rounding acceleration error is bounded by N^-4 for probe fields and N^-10 for Omega. The reciprocal metric backreaction coefficient is (A/P)^2=N^-12. It tends to zero in this declared probe limit; it is not discarded by an update branch.

On a fixed finite time interval, the smooth continuum ODE has a bounded positive-Omega neighborhood for sufficiently small probe ratio and the prepared zero metric velocity. The positive scalar kinetic and nonnegative matter potential give finite energy bounds. Consistency plus a discrete Gronwall estimate then yields convergence on that interval: truncation errors are O(h^2), rounded-force errors are O(N^-4), and background motion is controlled by the small N^-12 source. The uncorrected a=b clock preparation has an O(h) phase offset; the independent-clock rate comparison does not pretend otherwise. The nonlinear trajectory test uses the second-order Taylor preparation instead.

More explicitly, an error sequence obeys a bound of the form

    |e_n| <= initial errors + sum_(j<n)(n-j)[h^2 L|e_j|+C h^4+1/A].

For nh<=T this gives a finite-T bound with factor depending on T and the bounded-region Lipschitz constant, and error contributions O(h^2+1/(A h^2)) in addition to preparation error. It is not an all-time bound for arbitrary integer seeds.

The spatial coefficient2w/D=1/6 lies inside the cubic wave stability band. With dx=sqrt(6)h, the long-wavelength signal speed is one. A full spatial continuum study would also enlarge the lattice to hold a physical domain fixed. The present runs use L=3 and therefore test temporal refinement of homogeneous clocks plus a finite-grid signal identity, not spatial continuum convergence.

## 4. Operational metric and the measured observables

In the continuum constant patch, the metric is

    ds^2=Omega^2(-dt^2+d x^2),   d tau=Omega dt.

Massive clocks oscillate at coordinate frequency m_s Omega and at proper frequency m_s. The massless canonical signal follows the same coordinate null cone for every Omega. Consequently a received signal frequency compared with the local clock has the corresponding conformal redshift as a continuum prediction. An emitter-to-receiver redshift experiment was not executed here; the actual signal check is equality of canonical histories across homogeneous backgrounds. Raw event counts do not define this proper time.

The tested clock observable is the period between positive zero crossings of the signed quotient values recorded in the official click stream at node0. No board values are substituted into that decoder. Linear interpolation of successive recorded samples estimates the crossing; the complete definition and trace hashes are stored in the JSON evidence.

The exact frozen, remainder-free discrete clock frequency is

    omega_s(N,Omega)=2 asin(m_s Omega/(2N)).

It is not universally proportional to Omega at finite N. The ratio for Omega2/Omega1=2 has expansion

    omega_s(N,2)/omega_s(N,1)=2[1+m_s^2/(8N^2)+O(N^-4)].

The measured convergence is thus a controlled limited result, not a claim of exact Einstein clock behavior on the finite lattice.

## 5. Executed independent-clock and signal tests

[conformal_metric_probe.py](../experiments/geometry/conformal_metric_probe.py) constructs the complete tensor and seed, evolves only through Engine.step, extracts official clicks and rewinds every complete state. The tensor has four gear types and32 monomials. A nonconstant massless signal is seeded across neighboring nodes. All scalar clocks and H are initially homogeneous.

| N | Clock1 rate ratio | Clock2 rate ratio | Maximum normalized H drift |
|---:|---:|---:|---:|
|8|2.0039360930|2.0161122146|3.91e-7|
|16|2.0009798845|2.0039379150|9.11e-11|
|32|2.0002442034|2.0009787158|2.20e-14|
|64|2.0000610411|2.0002442689|5.36e-18|

Both target rate ratios are2. Every complete H history stays positive in these runs. The massless gear's complete a,b,r history and official quotient trace are exactly identical between the two backgrounds. This is equality of the canonical signal variable, not a claim that every detector amplitude or physical scalar phi=z/Omega is unchanged. All eight runs rewind exactly.

## 6. Nonlinear clocks without an extra Omega dressing

For a constant conformal factor and the quartic interaction, continuum solutions obey

    f_s(t;Omega)=Omega f_s(Omega t;1)

when the physical initial preparation is the same, including appropriately scaled velocities. This follows directly because the acceleration, mass term and cubic interaction all scale as Omega^3. It provides one proper-time history for an interacting clock assembly.

The second experiment enables the reciprocal quartic terms. It prepares f_s(0)=Omega and zero velocity to second order, including the nonlinear acceleration. It compares the official signed quotient history in the Omega2 run at update n with the Omega1 run at update2n-1, dividing out the canonical amplitude factor. With b_n denoting the current counter after update n, that update's quotient is ell_n=b_n+b_(n-2), centered at time n-1. The offset follows this centering, not a fitted shift. This uses nominal constant-background proper-time matching, not an integral of the slightly evolving Omega. Over a comparison at coordinate times t and2t, the accumulated mismatch is bounded by t*drift_2+2t*drift_1, using the recorded maximum normalized background drifts.

| N | Maximum matched trace error, clock1 | clock2 |
|---:|---:|---:|
|8|0.0513659|0.1944733|
|16|0.0135139|0.0516224|
|32|0.00342540|0.0130907|
|64|0.000859034|0.00328224|

Errors decrease by approximately four per doubling, consistent with the second-order temporal limit. All eight additional full histories rewind exactly. The checked nonlinear proper-time drift bounds at N=8,16,32,64 are respectively9.75e-8,2.34e-11,5.74e-15,1.12e-18. No trace was retimed using those bounds. The runner is [conformal_nonlinear_clock.py](../experiments/geometry/conformal_nonlinear_clock.py), and its evidence is linked above. This is a finite prepared nonlinear clock example, not an all-seed stability result.

## 7. What this does not establish

The conformal restriction forces the Weyl tensor to vanish and preserves unparametrized null curves relative to the background Minkowski metric. It cannot supply a general Schwarzschild-type light-deflection field or arbitrary Einstein geometry. Varying a single Omega gives only a scalar/trace equation; it does not impose the full metric, momentum and Hamiltonian constraints of general relativity. The chosen positive-sign Omega kinetic term is not the conformal Einstein-Hilbert kinetic term. No quantum statistics or particles are derived.

The useful conclusion is narrower: fixed reciprocal rank-four couplings can support a coherent, explicitly limited common metric interpretation of interacting clocks and links in a controlled continuum/probe regime. This construction changes the proposed algebra; it is not evidence that the current default repository already realizes that geometry.
