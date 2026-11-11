# Twenty geometric fields with general spatial dependence

This experiment reduces the repository's 24-field spatial frame equations to
20 fields by choosing a rotating upper-triangular frame. It retains arbitrary
local three-dimensional spatial dependence. It is not a homogeneous or null-wave
ansatz, and it does not establish discrete constraint preservation.

The reusable implementation is `geometry_triangular.py`; run its independent
audit with:

```sh
python -m experiments.geometry.team48.geometry_triangular_audit
```

Fresh evidence, including source hashes, is in
`runs/team48/geometry/triangular_audit.json`. The baseline equations and sign
conventions are those in `universe24/algebra/frame_equations.py`.

## Gauge and equations

Let the rows of B be the inverse triad, e_a = B_a^i partial_i; retain symmetric
K_ab and Gamma_ab c = <nabla_(e_c) e_b,e_a>, antisymmetric in its first two
indices. The synchronous lapse and shift stay fixed at one and zero.

Choose the antisymmetric angular velocity

    Omega_ab = sign(b-a) K_ab.

Then Bdot = (K+Omega) B. The matrix K+Omega is upper triangular: its diagonal
is K_aa and its upper off-diagonal entries are 2 K_ab. Upper-triangular B is
therefore preserved without solving a linear system, dividing by a field,
retaining a new gauge variable, or projecting after a step.

This represents a general positive spatial metric locally: h^{-1}=B^T B is
the upper Cholesky factorization. Nonzero diagonal entries are needed, as for
the original frame chart. Constructing this gauge from an arbitrary supplied
metric can involve square roots at preparation; integer triangular B instead
defines an exact rational/integer inverse metric, and these charts can
approximate general positive metrics under a proved refinement scheme.

Add the following terms to the Fermi-frame right-hand sides:

    Bdot_ai:       Omega_ad B_di
    Kdot_ab:       Omega_ad K_db + Omega_bd K_ad
    Gammadot_abc:  Omega_ad Gamma_db c + Omega_bd Gamma_ad c
                  + Omega_cd Gamma_ab d - D_c Omega_ab

where D_c = B_c^i partial_i and repeated indices are summed. Matter scalars
and normal dust are invariant under this frame rotation. Each spatial vector,
including a scalar gradient or a Maxwell electric/magnetic field, acquires
Omega times that vector.

The coordinate yz-plane is spanned by e_1,e_2, so its Frobenius relation gives

    Gamma_02 1 = Gamma_01 2.

In repository names, G021 is the same retained value as G012. More strongly,
the unreduced rotating equations obey the exact polynomial identity

    d(G021-G012)/dt = (-K00+K11+K22) (G021-G012).

No Hamiltonian, momentum, torsion, or differential constraint was used to
derive this identity. Eliminating the field by parametrization is therefore
legitimate; it is not a numerical reset of an independently evolving value.

| Retained group | Real fields | Comments |
| --- | ---: | --- |
| Upper-triangular inverse triad B | 6 | B10=B20=B21=0 |
| Symmetric extrinsic curvature K | 6 | Includes three off-diagonal values |
| Spatial rotation connection Gamma | 8 | G021=G012 |
| Geometry total | 20 | Every RHS has degree at most two |
| Complex Klein-Gordon field | 10 | Two values, two momenta, six gradients |
| Normal-comoving dust | 1 | Energy density; no independent dust velocity |
| One-bank sign clock | 1 | Owned and audited by integer_sign_lift.py |
| Combined count | 32 | 16 of 48 registers remain available |
| Optional source-free Maxwell field | 6 | E and magnetic field vectors |
| Combined count with Maxwell | 38 | 10 of 48 registers remain available |

The combined counts are accounting, not an assertion that the spare registers
already solve normalization, constraints, generic dust motion, or refinement.
The complex scalar supports classical energy and momentum flow; these fields
do not by themselves provide a particle-antiparticle quantum theory.

## Independent checks

The audit uses four sets of arbitrary exact rational spatial two-jets of all
six upper-triangular triad entries, and spatial one-jets of all six K entries.
All three coordinate directions are present. It constructs commutators,
connection, its time derivative, and coordinate-metric Ricci independently.
It does not call the candidate equations to construct an expected answer.

All four cases give exactly zero connection evolution error, exactly zero
coordinate-versus-frame Ricci error, and exactly zero torsion and eliminated
Frobenius defects. Symbolic checks verify triangular gauge preservation,
the difference identity above, degree two, and at most one spatial derivative
factor per term. A centered coordinate derivative consequently requires only
the target and one face neighbor in each monomial.

This verifies the change of frame and variable elimination. It does not prove
well-posedness of this synchronous free-evolution formulation or stability of
its difference scheme. Hamiltonian/momentum and the remaining differential
compatibility constraints are still necessary and must be separately checked.

## Nondegeneracy and a positive polynomial primitive

The reduced continuum equations give

    d(det B)/dt = trace(K) det B.

Thus a smooth finite continuum solution cannot cross det B=0 while trace K
stays integrable. The ordinary explicit or leapfrog discretization does not
inherit this multiplicative identity. Merely adding an inverse determinant
field does not establish that its algebraic constraint stays satisfied.

A different, exact primitive shows that positive geometry clocks and the
fixed-six polynomial engine are compatible. Let

    H = [[p,q],[q,r]],  det H = pr-q^2 = 1,  p>0,
    S = [[1,s],[0,1]].

The shear H' = S H S^T has

    p' = p+2s q+s^2 r,   q'=q+s r,   r'=r,   s'=s.

It preserves determinant and positive definiteness exactly and has the
polynomial inverse obtained by changing s to -s. Its degree is three. With
prepared a=R^{-1}(b) and zero remainder, the unchanged Rule3 reproduces this
map with

    u_p=6p+6s^2 r,  u_q=6q,  u_r=6r,  u_s=6s.

The audit runs seven forward and seven inverse steps for each of four integer
shear values, checking the fixed-six arithmetic, determinant one, positivity,
and exact recovery. This is a geometric/kinematic control, not Einstein
evolution. Matching the shear rate to the Einstein extrinsic curvature and
matter equations without division, while composing a polynomial reversible
map within the degree and stencil limits, remains unsolved here. Volume-
preserving row shears of the three-dimensional triad alone cannot represent
general expansion, so they are not a replacement for the trace-K equation.

## Alternatives considered

| Representation | Actual accounting or obstruction in this engine |
| --- | --- |
| Symmetric triad gauge | Six triad entries, but keeping B symmetric requires solving Omega B+B Omega=BK-KB; the generic solution divides by field-dependent eigenvalue sums. The triangular gauge avoids this. |
| Derive Gamma from B | Removes stored connection values but uses B inverse and spatial derivatives. Curvature then introduces second derivatives and products of derivatives. A direct substitution has denominators and generally violates the one-face monomial stencil. |
| Metric and momentum alone | Twelve familiar continuum variables; inverse metrics, determinants, and second spatial derivatives remain to encode. The small count alone does not fit the fixed polynomial law. |
| Self-dual connection | Nine complex connection components are 18 real registers, not nine. With a real nine-component densitized triad this is already 27 real values before clocks and matter; real connection/triad compatibility must still be enforced. If both canonical arrays are stored as unrestricted complex arrays the count is 36. No imaginary unit is a free integer channel. |
| Palatini/tetrad independent connection | Polynomial action is promising, but storing all spacetime tetrad/connection components and their algebraic constraints is not a demonstrated reduction here. |
| Regge edge lengths | Can encode general piecewise-flat geometry; areas, deficit angles and derivatives are not supplied by the current degree-three integer tensor. A different geometric representation needs a concrete polynomial encoding, not just an edge count. |

Primary-source context: [Alekseenko and Arnold, 2003](https://arxiv.org/abs/gr-qc/0210071)
also reduce the first-order spatial derivative data to eight combinations;
their linearized system has fourteen evolution variables with the metric
recovered by integration. The present triangular construction is derived and
audited independently; no equivalence to their formulation is asserted.
[Iriondo, Leguizamon and Reula, 1997](https://arxiv.org/abs/gr-qc/9710004)
obtain a symmetric hyperbolic Ashtekar formulation by adding constraints.
That result does not make complex reality conditions or discrete constraints
disappear, and is not a proof of hyperbolicity for the equations used here.

## Charged extension and positive diagonal pairs

The later charged-source cross-review is in `geometry_charged_audit.py`. It
independently differentiates the coordinate definition Xi=D Phi, checks the
rotating spatial potential, and checks every RHS under a spatially varying
infinitesimal U(1) gauge transformation. These identities, degree two, and
one-face support pass for 40 physical fields plus one sign clock. The matter
agent's optional squared-dust adapter retains the same count and treats its
signed amplitude as a frame scalar.

The isolated `geometry_positive_pairs.py` instead parametrizes each diagonal
as B_aa=p_a²+q_a² and evolves both amplitudes with K_aa/2. This adds three
physical fields. For equal-coefficient leapfrogs, the exact two-slice area

    W_a[n] = p_a[n] q_a[n-1] - q_a[n] p_a[n-1]

changes sign each step. A nonzero initial value therefore prevents p_a,q_a
from both vanishing, so all three B diagonals and det(B) stay strictly
positive. This is a genuine invariant for arbitrary evolving K, not a step
veto or an after-the-fact projection.

The physical RHS becomes cubic. The original common-phase compiler would
produce degree five and is unsuitable. Opposite staggered phase offsets for
K/Gamma, Pi/Xi and E/M, and for off-diagonal B/K, remove those extra phase
factors. All 120 cubic physical monomials pass the required odd parity check
in `geometry_positive_audit.py`. The separate integer agent's
`integer_staggered_audit.py` actually compiles and evolves the charged,
squared-dust candidate in 44 channels (43 physical plus one phase clock).
Its Engine evidence is `runs/team48/integer/staggered_audit.json`; the geometry
audit explicitly does not substitute its symbolic check for that evidence.

There are two separate limitations. First, exactly sampled continuum
amplitudes have constant q/p and zero W. A nonzero integer W introduces a
second discrete mode; its physical normalization must tend to zero under
a validated refinement family. Positivity does not prove this. Second,
centered differences do not obey the analytic chain rule for B=p²+q².
The builder's returned constraints are explicitly continuum-jet expressions.
Use its passive `sampled_constraints` helper, or reconstruct the full B
snapshot independently, before taking literal finite differences. The audit
includes a case where the chain-rule torsion defect is zero but the literal
sampled defect is -2. No discrete Hamiltonian/momentum, source continuity,
or convergence claim is closed by the 44-channel construction.
