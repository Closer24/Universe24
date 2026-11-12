# A source-coupled Einstein chart on the same local board

This construction gives one exact, restricted physical bridge: the retained
record/carrier rails source a spatially varying plane-symmetric metric that
satisfies every Einstein component, covariant source conservation and the
affine null-geodesic equations on a certified finite causal chart. The
metric coefficients evolve inside the same twelve-channel integer tensor and
the unchanged Engine. This is not a global periodic Einstein universe,
massive matter, a proper-time clock or general relativity in arbitrary
geometry.

## What is retained and what actually couples

The first eight channels are the two banks of the four-rail collision in
[01_native.md](01_native.md): each bank contains
(record+, record−, carrier+, carrier−). The gate exchanges 1001 and 0110.
Writing its input as (a,b,c,d), its polynomial is

\[
 \delta=ad(1-b-c)-bc(1-a-d),\qquad
 G(a,b,c,d)=(a-\delta,b+\delta,c+\delta,d-\delta).
\]

The gate preserves the two directional counts q+=a+c and q−=b+d at each
site. Record and carrier can exchange momentum while their summed stress
stays identical. Both species stream at the corresponding signed velocity.

Four appended channels retain spline coefficients F_A, H_A, F_B, H_B
(indices 8,9,10,11). Every channel retains the full (a,b,r) history. There
are twelve channels and 36 retained integers per node; no state is discarded.
The geometry coefficients are physical-chart data, not extra positive-energy
particles. Packet counts are not identified with orthonormal energy density
without the metric normalization below.

Let d denote the declared unit lattice direction. The initial chart
constraint is

\[
 \Delta_d^2 F=F(x+d)-2F(x)+F(x-d)=-q_+,\qquad
 \Delta_d^2 H=-q_-.
\]

The geometry rows of the actual tensor are

\[
\begin{aligned}
 u_{F_A}&=3(3F_B-F_B(x-d)-q_{+,B}),\\
 u_{H_A}&=3(3H_B-H_B(x+d)-q_{-,B}),\\
 u_{F_B}&=3(3F_A-F_A(x+d)-q_{+,A}),\\
 u_{H_B}&=3(3H_A-H_A(x-d)-q_{-,A}).
\end{aligned}
\]

These are literal source terms in the same tensor that scatters the records.
All geometry terms are linear, the collision terms are cubic, and every
monomial has strict onsite/single-face support. The Engine still executes
its original fixed-six carry law:

\[
 (\ell,r')=\operatorname{divmod}(2u+r,6),\qquad
 a'=b,\quad b'=\ell-a.
\]

On the constraint surface, the geometry rows are exactly the paired-bank
characteristic compiler u=3(F+F^{-1}). The forward first-order geometry law
is (A,B) ↦ (B,S A), where S shifts plus in +d and minus in −d. The prepared
old history is F^{-1}(b). Legal carries 0,…,5 are retained and frozen on
this orbit. Off the constraint surface the full Engine remains invertible;
the characteristic interpretation need not hold.

After two Engine ticks, each bank's directional count and matching profile
translate one site. Physical macrotime is therefore one half the Engine
tick count. At even ticks the physical source and profile add both banks;
omitting a bank would omit matter and change the metric.

## Exact interpolation, rather than a finite-difference approximation

The centered linear and cubic cardinal splines satisfy

\[
 B_1(s)=\max(0,1-|s|),\qquad
 B_3(s)=
 \begin{cases}
 (4-6|s|^2+3|s|^3)/6,& |s|<1,\\
 (2-|s|)^3/6,&1\le |s|<2,\\
 0,&|s|\ge2,
 \end{cases}
\]

and the exact identity

\[
 B_3''(s)=B_1(s+1)-2B_1(s)+B_1(s-1).
\]

Consequently, in the interior where the coefficient constraints hold,

\[
 {\cal F}(s)=\sum_j F_jB_3(s-j),\qquad
 {\cal F}''(s)=\sum_j\Delta^2F_j B_1(s-j)
             =-\sum_jq_jB_1(s-j)=-n(s).
\]

The retained F_j are spline coefficients; they are not asserted to be point
samples of the metric. The reconstruction is C², its source is continuous
and nonnegative, and rational evaluation is exact. The code rejects floats
and booleans at this boundary. There is no runtime interpolation solver or
feedback from this passive readout.

Let x be the coordinate along d, t macrotime, u=t−x and v=t+x. If the initial
summed plus/minus coefficient reconstructions are \({\cal F}_0,{\cal H}_0\),
set

\[
 f(u)={\cal F}_0(-u),\qquad
 g(v)={\cal H}_0(v),\qquad R=f(u)+g(v)>0.
\]

Then n+(u)=−f''(u), n−(v)=−g''(v). This orientation is essential: with
u=t−x and v=t+x, plus packets move toward increasing x.

## The exact restricted Einstein solution

In units 8πG=c=1, define

\[
 ds^2=-2R^{-1/2}\,du\,dv+R(dy^2+dz^2).
\]

Direct differentiation of the metric, inverse, Christoffel symbols and Ricci
tensor gives

\[
 G_{uu}=-f''/R=n_+/R,\qquad
 G_{vv}=-g''/R=n_-/R,
\]

with all other fourteen Einstein components and the Ricci scalar zero.
Thus the complete source is the sum of the two null streams,

\[
 T_{ab}=\frac{n_+}{R}(du)_a(du)_b
       +\frac{n_-}{R}(dv)_a(dv)_b.
\]

Both species, both banks and both velocities contribute. There is no
discarded apparatus momentum or unnamed rest-mass reservoir.

The future-directed affine rays
\(k_+=\sqrt R\,\partial_v\) and
\(k_-=\sqrt R\,\partial_u\) are null and obey
\(k^a\nabla_a k^b=0\). The four components of
\(\nabla_aT^{ab}\) vanish. The symbolic certificate computes all sixteen
Einstein residuals, four divergence residuals and eight affine-acceleration
residuals, rather than checking only one Friedmann equation.

For the orthonormal observer at fixed x,y,z,

\[
 \rho=\frac{n_++n_-}{2\sqrt R},\qquad
 j_x=\frac{n_+-n_-}{2\sqrt R},\qquad
 p_x=\rho,\quad p_y=p_z=0.
\]

Hence \(\rho\ge |j_x|\). The raw packet count is the source numerator; the
physical normalization depends on R. The coordinate null speed is exactly
one in this chart. Metric-dependent affine parameters and physical energy
do not require changing that coordinate speed. This exact sector does not
supply a massive-body proper-time clock.

Two-null-fluid Einstein solutions have an established physical context; see
P. S. Letelier, “Anisotropic fluids with two-perfect-fluid components,”
[Physical Review D 22, 807 (1980)](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.22.807),
which includes plane-symmetric two-null-fluid solutions. The local integer
compiler and the spline identification here are explicit constructions
verified by the repository certificates; that citation is not a substitute
for their proof.

## The finite causal chart and the obstruction at the seam

Static preparation obtains integer coefficients by

\[
 F_0=F_1=8L^2,\qquad F_{j+1}=2F_j-F_{j-1}-q_j
 \quad(1\le j\le L-2).
\]

It plane-tiles the repeated record/carrier encounter and places its receiver
at L//2. This uses finite initial work only. No solve, injection or repair
occurs during evolution. Coefficients are positive for the declared fixture.
The nonnegative spline basis and partition of unity then certify R>0
throughout the retained interior support.

A nonzero nonnegative source cannot obey this discrete Poisson constraint
everywhere on a periodic direction:

\[
 \sum_j\Delta^2F_j=0,\qquad
 \sum_jq_j>0.
\]

The complete periodic runtime therefore has seam constraint violations.
They are retained, serialized, measured and excluded from the physical chart;
they are not described as negative physical matter. This is an exact
obstruction to this ansatz on the closed board, not a no-go theorem for all
Einstein constructions.

The initial constraints hold at coefficients 1,…,L−2. The full Engine
depends on at most one neighboring face per microtick, including the
prepared old history. By induction, after tick k its coefficients agree
with the characteristic-shift solution throughout

\[
 k+1\le j\le L-2-k.
\]

The induction uses equality of current and old histories in the preceding
causal interior; the characteristic source constraints there give the same
tensor input. The source and ideal coefficients translate by at most one
site per two ticks, so their original interior constraints remain valid on
this more conservative domain. The cubic spline support has radius two.
Therefore the public readout admits only

\[
 k+3\le x\le L-1-(k+3),
\]

at even k within the declared horizon. Preparation rejects unsafe L/horizon
pairs. The default L=19 and six microticks retain the receiver x=9 and all
required support; L=11 with two microticks is the smaller unit-test chart.
Transverse plane symmetry and exact state types are checked before readout.

A source/curvature residual from one snapshot alone is insufficient to
certify a spacetime trajectory. The saved-run replay, full retained history,
constraint/causal-interior checks, even-tick characteristic anchoring and
symbolic identities must be combined. The independent geometry reviewer
checks the serialized same-tensor trajectory rather than trusting this
module's ideal-step helper.

## Controls and reproducibility

Run the actual twelve-channel audit and unit tests:

~~~bash
python -m validation.local_unification.geometry --out runs/local-unification/geometry
python -m unittest universe24.tests.test_local_unification_geometry
~~~

The audit writes an ordinary runtime bundle and complete trace, verifies
replay and full inverse reconstruction, and records the physical protocol
and exact rational readouts in geometry.json. All full states, including
seams, remain available.

The controls distinguish four different statements:

1. Removing the geometry source coefficients from the tensor preserves
   invertibility but produces a nonzero source/curvature defect. Structural
   reversibility alone does not establish the Einstein relation.
2. Removing one initial record and re-preparing its compatible profiles
   changes the physical source and metric. This is a different valid
   preparation, not matter changed while holding a valid metric fixed.
3. Holding all geometry histories fixed while changing that source is an
   explicitly off-constraint mechanical control: the next geometry state
   changes through the literal source terms and the complete state rewinds.
4. Disabling the collision keeps total directional source and the complete
   geometry history identical while changing carrier/record labels. This is
   the correct response to a species exchange with identical summed stress.

The complete coupled tensor fingerprint is
109a254ecfe53a42785a9a5a545b2eee928c4857402e38a41bf39c388dc6b5cd.
The original construction's full runtime replay/rewind, symbolic certificate
and five initial tests were executed before loss of the local executor.
The recovered revision adds stricter input/protocol validation and the
additional controls; those changes require fresh CI results. Repository
status must report those final CI results separately instead of carrying
the earlier validation claim forward.

## What this closes and what remains open

The previously missing bridge is a constraint-compatible common source:
the same retained directional matter counts occur in the local geometry
update, in the continuous stress tensor and in the exact Einstein residual.
The record gate can be physically active while its species-blind stress is
unchanged. The relation is more specific than an increase of a generic
complexity measure.

This closes a constructive finite plane-symmetric null-matter sector with
actual source dependence, local scattering and exact full-state reversal.
It leaves a global periodic positive-source sector, massive matter,
operational proper-time clocks, general gravitational scattering and a
universal monotonic complexity law unproved. Those are separate
mathematical obligations; none follows from this chart's exact identities.
