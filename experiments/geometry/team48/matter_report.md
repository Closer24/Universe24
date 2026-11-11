# Sourced first-order Einstein frame candidate

This research candidate closes the geometry equations with a complex classical
massive scalar, normal-comoving pressureless dust, and an optional independent
source-free Maxwell field. All evolution right-hand sides have degree at most
two and use only first spatial derivatives. It has 35 physical fields without
Maxwell and 41 with Maxwell. The team's sign encoding uses one further channel,
so these are 36- and 42-channel candidates; the independently audited triangular
frame reduction gives 32 and 38. These counts are constructive allocations,
not universal lower bounds for Einstein dynamics.

The mathematical source identities pass independent symbolic checks. The
integer encoding does not fix leapfrog's constraint drift, positivity,
nondegeneracy or the unresolved arbitrarily fine integer refinement problem.
The computational sign channel is not a proper-time clock.

## Integrated continuation after checking PR39

Fresh GitHub PR39 at `35344a1ba5c12c857404115e893911411ece7d35` already
implements the neutral scalar/dust system in 70 channels and improves dust
positivity by retaining signed `dust_amplitude=d`, with `rho_d=d^2` and
`d_dot=K*d/2`. The optional `matter_dust_square.py` adapter reproduces all 35
PR39 evolution components exactly under field renaming; its stress and common
constraints also agree symbolically. The raw-density modules remain historical
controls. The square encoding changes their discrete dust trajectories and
only directly represents square integer densities in the declared units.

A separate `matter_charged.py` extension now closes the Einstein-Maxwell
**electrically charged** classical scalar system. It replaces the six ordinary
scalar gradients by six gauge-covariant gradients Xi and adds three spatial
vector-potential components A. Temporal gauge fixes the time component to zero;
the code's A0,A1,A2 are spatial frame indices. In real two-component notation,
`J(phi,chi)=(-chi,phi)` and `D_mu=partial_mu-g A_mu J`, the extra terms are

```
Pi_dot = Div(Xi) + K Pi - m^2 Phi - g A_a J Xi_a
Xi_a_dot = D_a Pi + K_ab Xi_b - g A_a J Pi + g E_a J Phi
A_dot = K_matrix A - E
rho_e = -g (phi Pi_chi - chi Pi_phi)
current_a = g (phi Xi_chi,a - chi Xi_phi,a)
E_dot = Curl(M) + (K I-K_matrix) E - current.
```

Here the first `D_a Pi` on the displayed Xi equation means the ordinary frame
directional derivative; its gauge term is written explicitly next to it.
Gauge-covariant gradient, covariant curl, `M=Curl(A)` and electric Gauss
`Div(E)=rho_e` constraints are all measured. The rotating triangular frame
adds `Omega` to Xi and A as well as E and M. Every RHS is still degree two;
covariant Xi absorbs the terms that would otherwise require cubic A-squared
scalar expressions.

The complete charged allocation is **40 physical fields + one sign channel =
41 channels** with triangular geometry (45 unreduced). Thus seven of a
48-channel budget remain unallocated; they are not claimed to solve the
remaining physical gates. The continuum coupled energy/momentum and charge
identities pass, and an independent geometric audit checks local U(1) gauge
covariance of all 40 reduced RHS components. This is a classical charged
scalar model, not a Dirac field, pair creation or annihilation model.

Run `python -m experiments.geometry.team48.matter_charged_audit`. Its report
`runs/team48/matter/charged_square_audit.json` includes exact PR39 comparison
and an actual 41-channel Engine fixture. That fixture has initial electric
charge -5 and current_x=3; the current changes E_x by -6 in one dt=1 update.
Conjugating scalar and electromagnetic fields commutes exactly with the actual
Engine step, while stress and geometry are unchanged. The same run crosses
dust amplitude +1 to -1, keeping physical dust density at one, and reverses
exactly. This is explicitly an unconstrained interaction/encoding fixture:
its initial H=-22 and Gauss_E=5. It is not presented as a constrained Einstein
solution or as evidence of fine-grid convergence.

A second, homogeneous fixture **does satisfy every reported initial
constraint** with nonzero electric current: B=I, Gamma=0, K=diag(1,1,2),
phi=2, A_y=1, Xi_chi,y=-2, E_y=2, d=1, all other matter components zero,
and m^2=0. Its density is 5 and current_y=-4. Repeating that slice as both
time levels and taking one actual Engine step gives E_y=22 and H=-314;
reversal still succeeds. This directly demonstrates constraint drift from
constrained coupled initial slices, while explicitly leaving temporal
compatibility of the two starting slices unproved.

The remainder of this report documents the initial neutral/raw-density controls
and their independent validation. Their scope restrictions remain accurate for
those constructors; the charged and square-dust adapters are separate opt-ins.

## State and conventions

Use signature (-,+,+,+), c=8 pi G=1, lapse 1, shift 0 and
K_ab=-<nabla_(e_a)n,e_b>. The orthonormal frame is e_a=B_a^i partial_i,
with Gamma^a_bc=<nabla_(e_c)e_b,e_a>. Spatial frame derivatives are D_a.
The triad determines the inverse spatial metric algebraically:
gamma^ij=sum_a B_a^i B_a^j. Reading gamma_ij requires an invertible B.

| Sector | Physical fields | Count |
| --- | --- | ---: |
| Unreduced geometry | B_a^i, symmetric K_ab, antisymmetric Gamma_ab c | 24 |
| Two real scalar components | phi, Pi_phi, Psi_phi,a; chi, Pi_chi, Psi_chi,a | 10 |
| Normal-comoving dust | rho_d | 1 |
| Optional independent Maxwell | E_a, M_a | 6 |

Here Pi_A=n(phi_A), Psi_Aa=D_a phi_A and
V=m^2(phi^2+chi^2)/2. M denotes the magnetic field, avoiding a name collision
with the frame B. A fixed cosmological constant needs no extra state field.

## Stress and Einstein sources

Summing A over phi and chi, the scalar-plus-dust projections are

```
rho = (sum_A Pi_A^2 + sum_A,a Psi_Aa^2)/2 + V + rho_d
j_a = -sum_A Pi_A Psi_Aa
S_ab = sum_A Psi_Aa Psi_Ab
       + delta_ab [(sum_A Pi_A^2 - sum_A,c Psi_Ac^2)/2 - V].
```

Dust has j_a=S_ab=0 in this synchronous normal-comoving model. Maxwell adds

```
rho_EM = (E.E + M.M)/2
j_EM = E cross M
S_EM,ab = delta_ab rho_EM - E_a E_b - M_a M_b.
```

The complete projected Einstein equations add the same combined stress to
both dynamics and constraints:

```
Kdot_ab = Ric_ab + K K_ab - S_ab + delta_ab (S-rho)/2 - Lambda delta_ab
H = R + K^2 - K_ab K_ab - 2 rho - 2 Lambda = 0
M_a = nabla_b K_ab - D_a K - j_a = 0.
```

Kdot is for orthonormal components; the two quadratic K terms in coordinate
ADM cancel against the evolving frame. For scalar-plus-dust alone its matter
source simplifies to `-sum_A Psi_Aa Psi_Ab-delta_ab(V+rho_d/2)`.
No metric inverse or square root enters these polynomial evolution equations.

## Closed matter dynamics

```
phi_A_dot = Pi_A
Pi_A_dot = Div(Psi_A) + K Pi_A - m^2 phi_A
Psi_Aa_dot = D_a Pi_A + K_ab Psi_Ab
rho_d_dot = K rho_d
E_dot = Curl(M) + (K I-K_matrix) E
M_dot = -Curl(E) + (K I-K_matrix) M.
```

Here `Div(X)=sum_a[D_a X_a-Gamma^b_aa X_b]` and
`Curl(X)_a=epsilon_abc[D_b X_c-Gamma^d_cb X_d]`.
The scalar gradient and curl constraints, the Maxwell Gauss constraints,
frame torsion/connection constraints and Einstein H/M constraints must hold.
The triangular rotating frame adds `Omega X` to every spatial vector equation,
where Omega_ab=sign(b-a)K_ab. Its geometry already includes the corresponding
rotation terms.

These equations imply the continuum identities

```
rho_dot + Div(j) - K rho - K_ab S_ab = 0
j_a_dot + Div(S)_a - K j_a - K_ab j_b = 0.
```

The second assumes scalar curl compatibility and Maxwell Gauss constraints.
These are local covariant energy/momentum conservation, not a claim of a
globally conserved coordinate energy in an arbitrary curved spacetime.

The global scalar U(1) charge has
`q=phi Pi_chi-chi Pi_phi`, `J_a=chi Psi_phi,a-phi Psi_chi,a`, and
`q_dot=K q-Div(J)`. Conjugation changes the signs of chi and its derivatives,
reverses q and J, and preserves the stress-energy tensor. This realizes
opposite classical global-U(1) charge sectors with identical gravitational
coupling. It does not implement a quantum particle/antiparticle theory or
electromagnetically charged scalar interactions. The Maxwell sector is
source-free and interacts with the scalar through gravity only.

Normal-comoving dust is a legitimate pressureless gravitating component and
can serve as a restricted cold-dark-matter model. It does not represent
arbitrary tilted dust, collisionless velocity distributions or shell crossing.
General tilted dust introduces transport velocity/normalization constraints;
this report does not assert a polynomial closure for that extension.

## Exact nonzero-momentum integer initial data

On a periodic lattice with centered unit-spacing derivative, choose integer
phi(x)=4 f(x), Psi=D_x phi, k=phi+C with C sufficiently large, and

```
B=I, Gamma=0, K=diag(0,k,k)
Pi_phi=4, chi=1, Pi_chi=Psi_chi=0
Psi_phi=(Psi,0,0)
E=(0,2,0), M=(0,0,Psi)
rho_d=k^2-10-Psi^2; m^2=Lambda=0.
```

Then rho=k^2, j_x=-4 Psi+2 Psi=-2 Psi, with nonzero scalar flux and Maxwell
Poynting flux. The geometric momentum is `-2 D_x k=-2 Psi`, so H=M_a=0
exactly. Scalar gradient, curl, frame torsion and both Gauss constraints also
vanish. All modeled sectors are active and q=-4. Conjugating chi reverses q
without changing stress or constraints. A valid single slice does not provide
a consistent previous slice for a second-order time recurrence; using repeated
slices is an encoding/constraint-drift test, not a solved Einstein history.

## Checks and remaining gates

Run `python -m experiments.geometry.team48.matter_audit`. Its JSON output is
`runs/team48/matter/symbolic_audit.json`. The audit independently constructs
covariant T_mu_nu, verifies its projections, checks degree two, checks the
charge-conjugation rule, and verifies the continuum energy/momentum/charge
identities with symbolic derivatives. It substitutes two independent exact
flat-FLRW solutions into every evolution equation and returned constraint:
normal dust with a=t^(2/3), rho=4/(3t^2); and massless scalar with a=t^(1/3),
phi=sqrt(2/3) log(t). All tested residuals vanish identically.

The actual fixed-divisor Engine compiler is tested independently by the integer
agent, and actual constraint/metric drift by the numerical agent. Those results
must be read alongside these continuum checks. Exact reversibility does not
imply Einstein constraint preservation. A finite successful tensor compilation
does not establish an arbitrarily fine family of integer time steps. No
production engine or channel allocation is changed by these files.

## Primary sources and convention mapping

- [Einstein Toolkit ScalarEvolve documentation](https://einsteintoolkit.org/thornguide/Scalar/ScalarEvolve/documentation.html)
  gives the Einstein-Klein-Gordon system, source projections and ADM signs.
  Its K_Phi is -Pi/2, and its complex scalar normalization differs from the
  two canonically normalized real components used here.
- [Gourgoulhon, 3+1 Formalism and Bases of Numerical Relativity](https://arxiv.org/html/gr-qc/0703035v1)
  gives the Einstein constraints and matter conservation equations, especially
  sections 4.3 and 5.2. Its energy and momentum projections convert to the frame
  identities above. The version's Maxwell section is unwritten; it is not used
  as a source for the Maxwell evolution equations.
- [Petri, General-relativistic electromagnetic fields around a slowly rotating neutron star](https://academic.oup.com/mnras/article/439/1/1071/1749409)
  section 2.2 gives source-free Maxwell divergence/curl evolution with the
  spatial volume factor. Set lapse to one, shift to zero, use
  d(log sqrt(gamma))/dt=-K, and convert coordinate vectors to Fermi frame
  components to obtain the K I-K_matrix terms above. The covariant Maxwell
  stress projection and local conservation identity are also checked directly
  by the independent symbolic audit.
- [Pugliese and Valiente Kroon, On the evolution equations for a self-gravitating charged scalar field](https://arxiv.org/abs/1301.0461)
  develops a tetrad Einstein-Maxwell-Klein-Gordon system with a symmetric
  hyperbolicity result. That formulation retains additional derivative tensors.
  This compact candidate does not inherit its hyperbolicity or well-posedness
  theorem merely by using first-order variables.
- [Baake and Rinne, Superradiance of a charged scalar field coupled to the Einstein-Maxwell equations](https://arxiv.org/abs/1610.08352)
  numerically evolves a coupled charged scalar and gravity in spherical
  symmetry. It provides a relevant implemented physical comparison, not a
  fixed-integer channel encoding or a validation of this discretization.
