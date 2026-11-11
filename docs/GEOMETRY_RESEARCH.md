# From local clocks and links to a candidate spacetime metric

A common metric reconstructed from clock readings and signal travel is a necessary geometric milestone. Einstein constraint equations and their preserved evolution are additional requirements. The current model has a limited slow-wave metric interpretation, explicit finite-frequency and stability limitations, and missing responses that block a general Einstein interpretation. No complete Einstein event spacetime is claimed here.

This document collects exact reconstruction algebra, checks against the actual fixed tensor, and narrowly scoped candidate corrections. The [clock research overview](CLOCK_RESEARCH.md) covers the event definition and rest-clock falsification test; the [conformal metric experiment](CONFORMAL_METRIC_EXPERIMENT.md) is a separate restricted candidate. The [integer curl-wave construction](LINEAR_SPIN2.md) and [local phase-metric experiment](PHASE_METRIC_EXPERIMENT.md) add exact prepared wave and linearized-metric identities, with an explicitly limited one-way probe. All proposed experiments remain outside the default implementation.

## A metric must be measured, not assigned by a gear name

Use signature (-,+,+,+), units c=1, and ADM convention

$$
ds^2=-N^2dt^2+\gamma_{ij}(dx^i+\beta^i dt)(dx^j+\beta^jdt).
$$

The lapse N relates coordinate time to the proper time of observers normal to the slices. A clock at a fixed board coordinate instead measures

$$
d\tau_{\rm fixed}=A_0dt,\qquad
A_0^2=N^2-\gamma_{ij}\beta^i\beta^j=-g_{00}.
$$

The two agree only for zero shift. Coordinate-fixed clock worldlines must be timelike, so this measurement requires A0^2>0. Raw cycle counts require the already-declared slow-clock and calibration controls; they cannot simply be identified with proper time.

Choose a synchronization convention and coordinate distance unit, using reference clocks and local exchanged signals. In a sufficiently small approximately stationary patch, let t+ and t- be the forward and reverse null travel times along displacement plus/minus ell n. Define

$$
B_n=g_{0i}n^i,\qquad \Gamma_n=\gamma_{ij}n^in^j.
$$

The null equations are -A0^2 t_pm^2 plus/minus 2 ell B_n t_pm + ell^2 Gamma_n=0. Their positive roots give the inverse formulas

$$
B_n=\frac{A_0^2}{2\ell}(t_+-t_-),\qquad
\Gamma_n=\frac{A_0^2}{\ell^2}t_+t_-.
$$

Once the symmetric spatial metric is known,

$$
\beta^i=\gamma^{ij}B_j,\qquad
N^2=A_0^2+B_i\gamma^{ij}B_j.
$$

These are algebraic reconstruction formulas conditional on genuinely measured local null times and clock rates; they are not quantities already derived by the automaton. One-way travel times depend on synchronization. Round-trip data alone do not remove that ambiguity. Overall time and coordinate scale are conventions; dimensionless comparisons and geometric predictions must be invariant under them.

Six directed axis measurements determine Bx,By,Bz and gamma_xx,gamma_yy,gamma_zz. With A0 this is seven independent components, leaving the three off-diagonal spatial entries undetermined. For an independent diagonal probe,

$$
\gamma_{ij}=\frac{\Gamma_{e_i+e_j}-\gamma_{ii}-\gamma_{jj}}2.
$$

A two-edge route that merely adds axis travel times supplies no new independent diagonal measurement. Suitable oblique wave propagation, polarisation or multi-path observables must be built and calibrated. Axis-only data are exactly degenerate: gamma=I plus/minus epsilon(ex ey^T+ey ex^T), beta=0, N=1 have identical axis times for |epsilon|<1, but diagonal squared intervals 2 plus/minus 2epsilon.

This audit reads gravity.MatterSpec, build_lapse, light_spec and gravity_l0c. It proposes no default/source edit. It separates exact coefficient identities, a slow-wave continuum interpretation, and physical claims still missing.

## Existing scalar coefficients and actual lattice dispersion

For a second-order scalar with bare mass coefficient mu, spatial face weight w, D=6Q and uniform F, the actual input is

$$
u=Db-\mu N^2b+wC\Delta_{\rm lat}b,\quad
N^2=1-F/P=1-2U,\quad C=1-2F/P=1-4U.
$$

The endpoint factor for a nonuniform link (x,y) is C_xy=1-(F_x+F_y)/P. Its reciprocal polynomial comes from the existing lapse potential, rather than a force added after Rule3. Define c0^2=2w/D and m0^2=2mu/D. Removing only the bounded remainder correction, Fourier modes satisfy

$$
4\sin^2(\omega/2)
=m_0^2N^2+4c_0^2C\sum_i\sin^2(k_i/2).
$$

The slow, long-wave limit is omega^2=m0^2 N^2+c0^2 C |k|^2. Slow rest clocks read N and massless signals travel at c0 sqrt(C). They therefore fit the same static isotropic metric

$$
ds^2=-N^2c_0^2dt^2+A^2d\mathbf x^2,\qquad
A^2=N^2/C=\frac{1-2U}{1-4U}.
$$

This is a kinematic, weak-field candidate when N^2,C>0. To first order it has N^2=1-2U and A^2=1+2U. These coefficients are selected by the construction; this calculation does not derive their values from unconstrained Rule3.

The exact cellular dependency cone remains at most one face edge per update and is not this low-energy null cone. For finite wave number the group velocity is

$$
v_i=\frac{c_0^2C\sin k_i}{\sin\omega}.
$$

It is dispersive and generally anisotropic. Use a dimensionless clock-calibrated comparison
[v_g(U)/v_g(0)]/[omega_clock(U)/omega_clock(0)].
In the common slow limit it tends to 1/A. The exact remainder-free calculation in [link-metric evidence](evidence/link_metric_check.json) shows, at U=1/64, relative departures from 1/A of about -2.58e-5 for |k|=0.1, -4.16e-4 for axis |k|=0.4, and -1.66e-3 for axis |k|=0.8. The diagonal direction differs too. These are symbol calculations, not measured packet arrivals. The rest-clock part was separately measured through actual official records in [rest-clock evidence](evidence/metric_clock_gate.json).

## A spatial instability that rest clocks alone cannot detect

For massless uniform-background light, the checkerboard eigenvalue is beta_corner=D-12wC. An all-mode oscillatory band requires wC<=Q. With the current w=Q-1,

$$
U\ge-\frac1{4(Q-1)}.
$$

Thus the current near-CFL stencil has virtually no room for negative U: at Q=2^33+1 the boundary is about -2.91e-11. The negative-U on-site clock experiment has no spatial transport and does not certify this spatial regime. A low-k dispersion branch can look healthy while the corner mode is unstable.

A mathematically permissible pre-run choice w=(Q-1)/2 supplies an actual margin: C<=2Q/(Q-1), or approximately U>=-1/4 before mass and other couplings. Set the carrier to D-6w so the free input remains Db+w Delta b. Choose w/(2P) integral to keep the existing lapse potential integral. This is a different declared candidate tensor, with a smaller flat coordinate wave speed; every proposed common-cone sector must be treated consistently.

For a massive scalar the uniform sufficient spectral endpoint conditions also include mu N^2+12wC<=2D and nonnegative mu N^2, wC. For variable fields, the weighted graph Laplacian gives corresponding operator bounds. Nothing here proves that a dynamically evolving unbounded F remains in the permitted interval. The exact resolution lift scales w,D together and leaves these relative margins unchanged.

These band statements concern the remainder-free linear recurrence. The [exact metric-source audit](METRIC_SOURCE_AUDIT.md) constructs an integer carry phase with a linearly growing checkerboard amplitude for over a billion allowed updates even though its remainder-free eigenvalue is inside the band. It also derives the uniform source ledger. Neither a spectral margin nor a slowly changing uniform metric register proves bounded exact dynamics, curvature or cosmological expansion. A time-dependent lapse alone can be removed by a time reparametrization when the spatial metric is unchanged.

## Matching the cone is weaker than matching a covariant wave equation

For static N,A, a minimally coupled scalar satisfies, in units c0=1,

$$
\phi_{tt}=\frac{N}{A^3}\nabla\cdot(NA\nabla\phi)-N^2m^2\phi.
$$

The actual slow-wave divergence-form operator is instead

$$
b_{tt}=\nabla\cdot(C\nabla b)-N^2m^2b.
$$

Both have principal coefficient C=N^2/A^2, but their first-derivative terms differ:
metric KG has C grad log(NA), whereas the existing recurrence has grad C.
At first order in the chosen U, NA=1+O(U^2), so the first term vanishes to first order while grad C=-4 grad U. This is a real distinction in wave transport beyond the eikonal cone.

A declared canonical field convention can reconcile the fixed time-kinetic coefficient. Set chi=z phi with z=sqrt(A^3/N), for a static background. Direct differentiation gives

$$
\chi_{tt}=\nabla\cdot(C\nabla\chi)
-\left[\nabla\cdot(C\nabla\log z)+C|\nabla\log z|^2+N^2m^2\right]\chi.
$$

Here z=1+2U+O(U^2), so the missing geometric potential is 2 Delta U at first order. This is a construction-level field normalization and operator correction, not an outcome-dependent reinterpretation of raw click periods. It does not remove the finite-frequency clock discrepancy.

A legal fixed polynomial for that weak-static correction is

$$
\Phi_{\rm corr}
=-\frac{w}{2P}\sum_x F_x\Delta_{\rm lat}(\chi_x^2)
=-\frac{w}{2P}\sum_x\chi_x^2\Delta_{\rm lat}F_x
$$

on a periodic board. Its exact signed-plus derivatives are

$$
\Delta u_\chi=-\frac{w}{P}\chi\,\Delta_{\rm lat}F,\qquad
\Delta u_F=-\frac{w}{2P}\Delta_{\rm lat}(\chi^2).
$$

The first contributes -2c0^2(Delta U)chi to the slow equation. Every monomial occupies one node or one edge. The potential has degree three, hence tensor order three, below the allowed four. Coefficients are integer when w/(2P) is integer. [link-metric audit](../experiments/geometry/link_metric_check.py) verified both full polynomial inputs on an arbitrary nonuniform integer state, strict support, reciprocity and a 20-step exact rewind using the existing engine. No observer feeds a correction into a run.

This is a limited new scalar candidate. It does not yet supply the nonlinear metric coefficients, time-dependent normalization terms, all matter representations, constraints or a full Einstein source. Differentiating a candidate potential supplies reciprocal source terms; it does not prove they equal the conserved stress tensor required by Einstein's equations.

## Geodesics and field equations still need independent tests

A slowly varying common principal symbol can produce geometric-optics rays governed by a Hamiltonian proportional to g^{mu nu}p_mu p_nu. That supports a geodesic interpretation in the corresponding approximation. To establish it for this automaton, actual packet emission/arrival and trajectories must come from fixed official-click detectors, agree with the inferred geometry across species and directions, and control lattice, bandwidth, remainder and background-gradient errors. A board-energy centroid or an algebraic dispersion identity alone is insufficient.

The default/optional Einstein code still has absent mixed and off-diagonal matter response, a nonzero source-divergence diagnostic, and a harmonic constraint imposed in a polarisation count rather than enforced by the full interacting evolution. There is no derivation here of G_mu_nu+Lambda g_mu_nu=8piG T_mu_nu. This kinematic candidate is therefore not an Einstein spacetime solution.

A separate conformal construction g=Omega^2 eta can keep massless transport flat while clock mass terms scale as Omega^2. With conformal scalar curvature coupling in four dimensions, canonical chi=Omega phi keeps dimensionless quartic interactions independent of Omega. That can avoid a naive rank-five dressing for that particular field convention. It cannot give general Weyl curvature or light bending and remains distinct from the nonconformal N,A candidate above.

## Next defensible experiment

Use one declared scalar tensor with positive spatial headroom and the same slow-clock/transport metric coupling for two scalar species. Prepare a weak, spatially varying background and local signal detectors once. Compare relational clock rates and pulse arrival/trajectory predictions from one fitted metric; retain the zero-field control and a refinement family. If canonical normalization is claimed, include its derived geometric operator term in the tensor beforehand. Then test complete reciprocal sources and constraints separately. Do not add an unrelated attractive force or call a fitted cone Einstein's equations.

Relevant primary/author sources: Carroll, Lecture Notes on General Relativity, https://arxiv.org/abs/gr-qc/9712019 ; Will, The Confrontation between General Relativity and Experiment, https://arxiv.org/abs/1403.7377 . The coefficient, canonical-normalization and discrete-band calculations above are explicit derivations for this code, not results imported from those sources.

## What Einstein dynamics additionally requires

Let K_ij=-(partial_t gamma_ij-L_beta gamma_ij)/(2N), D_i be the spatial metric derivative, and rho,j_i,S_ij the normal energy, momentum and spatial stress projections of an independently defined physical T_mu_nu. With S=gamma^ij S_ij and Einstein convention G_mu_nu+Lambda g_mu_nu=8piG T_mu_nu, initial data must satisfy

$$
{}^{(3)}R+K^2-K_{ij}K^{ij}-16\pi G\rho-2\Lambda=0,
$$

$$
D_j(K^{ij}-\gamma^{ij}K)-8\pi G j^i=0.
$$

These are the Hamiltonian constraint and three momentum constraints. Evolution also requires

$$
(\partial_t-\mathcal L_\beta)\gamma_{ij}=-2NK_{ij},
$$

$$
\begin{aligned}
(\partial_t-\mathcal L_\beta)K_{ij}
={}&-D_iD_jN+N[{}^{(3)}R_{ij}+KK_{ij}-2K_{ik}K^k{}_j]\\
&-8\pi GN[S_{ij}-\tfrac12\gamma_{ij}(S-\rho)]
-\Lambda N\gamma_{ij}.
\end{aligned}
$$

A consistent matter evolution supplies covariant source conservation. The contracted Bianchi identity links that conservation to propagation of the constraints. The continuum equations here specify a target; copying them into a document does not derive them from Rule3.

A discrete claim must define its actual curvature, source, constraints and update and prove preservation with the actual lattice difference operators and integer remainders. A useful exact certificate would be a nonempty prepared invariant set

$$
\mathcal S_{\rm geom}=\{s:\mathcal C(s)=0,\ \gamma(s)>0,\ N(s)>0\},
\qquad W(\mathcal S_{\rm geom})=\mathcal S_{\rm geom},
$$

together with local reconstruction and a well-defined encoded geometric evolution. An identity of the form C_i(Ws)=sum_j M_ij(s)C_j(s) suffices for forward preservation of the equality constraints. Inverse preservation and positivity of the lapse and spatial metric must also be proved; they do not follow from that identity alone. It need not be the only proof route. An approximate claim instead needs explicit residuals and convergence bounds through a declared refinement family. Dropping the carry ledger is not an exact constraint proof.

The current named metric fields do not meet this target. In the optional Einstein tensor all three h0i and all three spatial off-diagonal hij gears have zero external readers and only seven free stencil monomials each. An arbitrary change in those sectors therefore cannot change any other register. A spatially varying hxy counterfactual on the L4 prepared package produced exactly the same 25,006 official records over 20 updates, with exact rewind in both histories. The proof is the absent dependency; the run is a reproducible illustration. A generic metric perturbation cannot be encoded operationally in a field invisible to every detector and matter sector.

Separately, a uniform ref.R00 b=32, a=0 preparation gives implemented time-component source divergence 18,382,848, versus maximum source magnitude 33,554,432; its spatial divergence components are zero. This is an exact counterexample to universal conservation of the current declared source, not an identification of that source with a physical stress tensor. Additional ledger terms or a restricted sector would have to be explicitly constructed and proved. A polarisation count with harmonic constraints imposed does not do that.

## An exact prepared linear TT sector does exist

There is a constructive result inside the actual optional Einstein tensor, without adding a rule or changing its coefficients. In its stored DeWitt basis, prepare only

$$
\texttt{metric.a1}=p(z),\qquad \texttt{metric.hxy}=q(z),
$$

with both previous and current counters and both remainders depending on z alone. Set every other counter to zero. Their remainders may be fixed allowed values. This is a vacuum preparation, not the ordinary matter-containing package seed.

The exact stored-to-metric map gives

$$
P h_{xx}=p,\quad P h_{yy}=-p,\quad P h_{xy}=q,
\qquad h_{00}=h_{0i}=h_{zz}=h_{xz}=h_{yz}=0.
$$

Here the trace-reversed field equals h. The opposite hxx and hyy values are projections of one stored counter, so there is no independent rounding mismatch between them.

The proof has three steps. First, set every inactive a,b to zero in the tensor polynomial. A complete monomial audit leaves exactly fourteen terms: the independent seven-term free stencil for each of the two active gears. Every inactive input vanishes. Therefore the inactive counters stay zero and their remainders stay fixed. Second, the remaining input for either planar field f is

$$
u_f(z)=(4Q+2)f(z)+(Q-1)[f(z+1)+f(z-1)].
$$

Coordinatewise integer division preserves dependence on z alone, including the carry phase. The same argument applies to the exact inverse, so this set is invariant in both time directions. Third, the metric trace vanishes algebraically, and every potentially nonzero term in the harmonic divergence differentiates p or q along x or y. Those differences vanish exactly. The time components are zero, so their time differences vanish too. Thus the discrete linear transverse-traceless and harmonic constraints hold for every state of this prepared sector, not just at initialization.

The exact wave equation remains

$$
D(f_{t+1}-2f_t+f_{t-1})-2(Q-1)\Delta_z f_t
=r_t-r_{t+1},\qquad |r_t-r_{t+1}|\le D-1.
$$

The remainder residual is retained. It need not vanish or be negligible for small-amplitude data. The proof establishes a constrained two-polarisation board sector; it does not establish the continuum vacuum wave equation at every scale.

The [actual-engine experiment](../experiments/geometry/planar_tt_sector.py) used L4 and deliberately unequal planar carries for 256 updates. All trace, divergence, planarity, inactive-sector and wave-ledger identities passed at every step, and all counters and remainders rewound exactly. It recorded 32,224 audit-labelled arithmetic events and zero official-labelled events. These fields therefore have board dynamics but no demonstrated official gravitational-wave detector. See [exact evidence](evidence/planar_tt_sector.json).

This result does not solve the nonlinear vacuum constraints. For example, at an instant with spatially uniform p=0 and nonzero time derivative, the continuum candidate gamma=diag(1+p/P,1-p/P,1) has zero spatial curvature and K=0 but positive Kij K^ij. Its vacuum Hamiltonian constraint fails at quadratic order unless further backreaction is supplied. The exact linear sector is a useful restricted construction, not a nonlinear Einstein solution, a generic attractor or an all-time amplitude bound.

## Why a quartic Palatini expression does not close the proof

A tetrad and connection allow the polynomial Einstein-Palatini action schematically epsilon e e (d omega+omega omega) plus a cosmological epsilon e e e e term. Its degree is compatible with four in a formal field expression, and g_mu_nu=eta_IJ e_mu^I e_nu^J is quadratic. This is a possible inverse-design starting point.

However, its first-order evolution is degenerate and constrained. A b-only reciprocal remainder-free Rule3 recurrence has a regular mixed discrete kinetic Hessian proportional to -D I. Even with validated old-a dependencies, the derivative of b' with respect to a is triangular with diagonal -1 in dependency order. The full unrestricted Rule3 state does not thereby acquire Palatini's primary constraints or gauge freedom. A gauge-fixed, constrained invariant encoding may still be possible; it is an additional construction, not a consequence of polynomial degree.

Connection components carried by honest links in different directions, and holonomy around a plaquette, also occupy more than one edge. Low degree does not imply the repository's strict single-edge physical support. Staged relay fields can be considered, but their consistency, delays and constraint preservation must be proved. Enforcing a positive spatial metric, nondegenerate tetrad, time orientation and admissible clock states is another invariant-sector requirement.

The [Palatini target and executable controls](PALATINI_TARGET.md) give the exact next encoding criterion and two counterexamples. A local reciprocal multiplier gear can leave its initially satisfied constraint after one Rule3 step while retaining exact reversibility; a cross-axis connection product can fail strict physical support despite its allowed degree. The same note gives an involution construction showing why a known reversible constrained target could, in principle, be retimed into Rule3 if locality, degree and retained information are proved. This is a missing-construction statement, not a general impossibility theorem.

There is no established minimum new gear count or tensor that fulfills these requirements. The smallest defensible next step is a restricted weak-field sector with complete observable metric response and an exact local constraint-propagation certificate, followed by increasingly general sources and geometries. A conformal scalar construction is a useful narrower sector but has no general Weyl curvature or light bending.

## Primary references and scope

- Arnowitt, Deser and Misner, The Dynamics of General Relativity: https://arxiv.org/abs/gr-qc/0405109 .
- Gourgoulhon, 3+1 Formalism and Bases of Numerical Relativity: https://arxiv.org/abs/gr-qc/0703035 .
- Bahr and Dittrich, (Broken) Gauge Symmetries and Constraints in Regge Calculus: https://arxiv.org/abs/0905.1670 . This analyzes broken symmetries and pseudo-constraints in the studied curved Regge constructions; it is not a no-go theorem for every discrete gravity model.
- Dittrich and Hoehn, From covariant to canonical formulations of discrete gravity: https://arxiv.org/abs/0912.1817 . Its linearized flat-background first-class constraints illustrate that the action, symmetry and constraint propagation must be studied together; higher-order results are specific to that construction.
- Dittrich and Hoehn, Canonical simplicial gravity: https://arxiv.org/abs/1108.1974 . It derives canonical evolution from a discrete action, not from reversibility alone.

## Reproducing the isolated checks

Run the exact derivative, support and rewind check with:

    python experiments/geometry/link_metric_check.py --out runs/geometry/link_metric_check.json

The result also tabulates the remainder-free signal dispersion. It does not measure a propagated packet.

Run the named-metric invisibility and declared-source counterexamples with:

    python experiments/geometry/metric_obstruction_check.py --out runs/geometry/metric_obstruction_check.json

The [committed obstruction evidence](evidence/metric_obstruction_check.json) includes the tensor fingerprint, reader census, official-record comparison and exact source defect. Both commands write only their requested report; neither edits a source tensor during evolution.

Run the actual optional tensor's exact prepared linear TT check with:

    python experiments/geometry/planar_tt_sector.py --out runs/geometry/planar_tt_sector.json

This checks a vacuum board sector and keeps the existing audit labels. It does not relabel its metric activity as official observations.
