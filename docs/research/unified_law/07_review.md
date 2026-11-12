# Independent review of the single six-channel candidate

The selected spinor-plus-beta construction passes the bounded claim: one
unchanged fixed-six Engine tensor, one complete prepared state, an exact
Hamiltonian-constraint decoder, a correct homogeneous Einstein–scalar–dust
continuum pushforward, and first-order convergence on the proved finite-time
family. It does not establish a general spatial universe, exact finite-step
Einstein evolution, an efficient integer representation, or an operational
clock detector.

Run the common and component audits first, then:

```sh
python -m validation.unified_law.independent_review
```

The review writes `runs/unified_law/07_review.json`. It fails on stale component
source hashes, mismatched tensors or complete seeds, missing runtime comparison,
or the promotion of an untested physical gate. It is intentionally not a
standalone replacement for the preceding audits.

## 1. What is one law here?

The retained coordinates are four real auxiliary spinor components, beta, and
one projective denominator. Every channel keeps the Engine's entire a,b,r
history. There are six channels, eighteen retained integers per node, and 58
integer monomials of degree at most three. The tensor uses only current b inputs
at the same node. No evaluation of an exponential, constraint projection, solver,
state reset, or independent continuum integrator generates its updates.

The default law and complete seed are:

| Item | Exact value |
|---|---|
| Timestep | 1/24 |
| Initial denominator | 4 |
| Coordinate seed | (sa,sb,sc,se,beta)=(1,0,0,0,0) |
| Physical seed | (k,p,phi,d,beta)=(-1/2,0,1,1/2,0) |
| Tensor SHA-256 | `8d5f0fad5d094908afd4e78d05e60710b96c95943bb7aa791e5b753ff33e9df9` |
| Complete seed SHA-256 | `61b79e0831d775508ab04086aa4f4009d89bb6df95e2357e4ee7e5ff2777097f` |

The old full45 numerator interpretation and its failed finite-step constraint
are not reclassified. This is a different discretization in fixed constrained
coordinates, with a separately checked pushforward to the same declared
homogeneous continuum equations. Its rational initial data are representable by
construction. No exact rational lift of every earlier physical seed is assumed.

## 2. Independent algebra and the actual Einstein source

The review implements its own physical decoder and force using pair arithmetic
in the algebra R[w]/(w²+3). It does not use the component's `equations` function
to generate the independent force. Two pair matrix products reproduce all four
cubic spinor velocities; beta has velocity k. Their equality to the submitted
polynomials is checked symbolically.

For z=(a,b,c,e), define U=a²+3b², V=c²+3e², p=ac+3be and y=bc-ae. The identity

\[
UV-p^2-3y^2=0
\]

gives the physical constraint under the fixed decoder

\[
k=-U/2-V/12,\qquad \phi=U-V/6-y,\qquad d=U/2-V/12+y:
\]

\[
C=6k^2-p^2-\phi^2-2d^2=0.
\]

This identity alone has no dynamical acceptance power. The independent Jacobian
calculation also proves, in normal proper time,

\[
\dot k=(p^2+d^2)/2,\quad \dot p=3kp-\phi,\quad
\dot\phi=p,\quad \dot d=3kd/2,\quad\dot\beta=k.
\]

The review then calls the existing full 44 `formulation.equations` directly with
its own symbolic decoder. All 44 velocities agree, including zero velocities
for omitted fields; all 33 declared constraints vanish. Thus this check does not
merely compare two copies of a handwritten reduced target.

For the metric `ds²=-dt²+exp(-2beta) dx·dx`, the independent pressure identity is
`2 kdot-3 k²=(p²-phi²)/2`. The metric package separately computes the full 4D
Einstein tensor, the comoving geodesic, and the proper-time normalization. Its
source, clock and metric evidence must identify the same default tensor and
complete seed as the Engine evidence.

The weighted norm N=a²+3b²+c²/6+e²/2=-2k satisfies
`Ndot=-(p²+d²)`. This proves a global future bound for the continuum spinor and
finite beta on every finite proper-time interval. It does not by itself prove
finite-step norm monotonicity.

## 3. Independent complete-state computation

The reviewer predicts every next a,b,r register using exact rational pair
arithmetic and the literal `divmod(6q+r,6)` rule. It never calls the candidate
tensor evaluator or its polynomial RHS in that oracle. The denominator follows
`Dnext=M D³-Dold`; each other numerator follows
`Pnext=M D³(x+h F(x))-Pold`. This includes the previous numerator subtraction
that invalidated earlier arguments based only on one Euler point.

Two complete homogeneous fixtures run for three actual Engine ticks on 27
nodes: the shared seed above, and the signed rational coordinates
`(-1/2,1/3,1/4,-1/5,1/7)` at denominator 420. Each fixture exercises all six
remainder classes. Across both, 2916 retained-register comparisons agree, every
immediate inverse agrees, and the final state rewinds exactly to its complete
seed. Constraint C is exactly zero at every decoded sample. Peak bit sequences
are `3,18,66,207` and `9,38,126,389`, respectively.

The common audit additionally runs the existing bundle/runtime path and compares
all saved before/after a,b,r snapshots to its independent oracle. The review
requires that check; matching only a passive decoded report would not suffice.

Two actual wrong tensors demonstrate why C=0 cannot certify the dynamics:

| Alteration | Still passes | Independently rejected by |
|---|---|---|
| Set sc velocity to zero | Three reversible Engine ticks and C=0 | At the seed, pdot=0 instead of the required -1 |
| Set beta velocity to zero | Three reversible Engine ticks and C=0 | The frozen flat metric has zero Einstein tensor while matter density is positive |

These tests retain the same physical interpretation and expose inconsistent
forces; they do not feed a correction into either trajectory.

## 4. Review of the finite-time theorem

The proof in [04_invariant_map.md](04_invariant_map.md) applies to the actual
two-history map, not only its continuum or Euler limit. Its stated hypotheses
are essential: the shared sa=1 seed, D0>=2, h=1/m<=1/16 and nh<=T<=1/8.

The denominator induction is positive and increasing. With M>=m, its history
coefficient satisfies epsilon0=0 and epsilon_n<=h³/63 thereafter. The weighted
force estimate `||F(z)||W<=(1/2+3N/2)sqrt(N)` follows from a W-skew linear part
and a W-selfadjoint cubic part whose eigenvalues lie between 3k and 0. While N<=2,
the running maximum norm grows by at most `1+7h²` per step. The estimate
`exp(7Th)<=128/121<sqrt(2)` closes the first-crossing bootstrap. It also yields
`-1/4<=beta_n<=0` and a positive metric bound over this whole family.

The polynomial box and coefficient bounds give L=4745/64 and
A=5085391/8192. The memory perturbation has norm at most 10h³/63, so discrete
Gronwall proves

\[
e_N\le\frac{e^{LT}-1}{L}\left(\frac{Ah}{2}+\frac{10h^2}{63}\right).
\]

The constants are conservative, but the bound is a genuine first-order
convergence theorem on the stated finite interval. The physical decoder and
metric are Lipschitz on the proved domain. It is valid to transfer convergence
to those observables; it is not valid to infer exact finite-step conservation.

The independent physical-ODE reference and the clock component agree within
1e-12 on the three field errors. The review joins the h=1/24,1/32,1/48 tensors
explicitly, with 3, 4, 6 steps to the same T=1/8. Their maximum field errors are
approximately 0.00342429,0.00254453,0.00168089. These are distinct prepared
tensors in one refinement family, not one identical tensor at three step sizes.

## 5. Source, clock and cost boundaries

The continuum comoving dust amount `d² exp(-3beta)` is conserved. It is not
exactly conserved by the finite-step map: positive drift certificates and errors
about 5.67e-5,4.15e-5,2.70e-5 remain recorded as failed exact conservation. The
scalar phase is monotone in the proved continuum seed domain, but it is not
equal to proper time. A decoded phase is not an autonomous material clock,
signal path, detector record or calibration experiment.

Refinement peak bits grow from 207 to 649 to 6101. The projective denominator
recurrence has exponential bit growth in tick count; fewer channels do not
remove that cost. No spatial packet coupling is present in this onsite tensor.
Generic runtime acceptance gates C–F remain `not_tested`.

The native scheduler is a separate research bridge with its own tensor and
decoder. Its mechanical reversibility or channel budget cannot inherit this
spinor decoder's constraint identity, convergence theorem or clock results.
Its finalized 21-channel sourced run passes its mechanical oracle and complete
rewind over 54 ticks, but the first decoded constraint is already -4/9. The
review recomputes that rational residual and retains the failed exact-constraint
and untested refinement statuses. Any alternative must pass those physical
checks on its own complete trajectory.

## 6. Provenance and one repaired defect

The review compares component source hashes to the current files, records the
evidence hashes, and rejects joins with a different timestep tensor or even one
changed carry in the complete seed. It also records its direct Engine,
projective compiler and full-source dependencies. Regenerate the evidence after
any relevant source edit; an old passing JSON is not acceptance of new code.

Review found that a type guard inside an untyped `lru_cache` could be skipped:
after caching Fraction(1,32), float 0.03125 compared equal; after Fraction(1),
True compared equal. The public guard now runs before cache lookup. The review
warms both cache entries and confirms both inexact requests raise TypeError.
This repairs input discipline without changing the selected tensor or seed.

## 7. Primary sources actually consulted

Larsson and Larsson, [The Lorentz group and the Kronecker product of matrices](https://arxiv.org/pdf/2110.15118),
section 3.1, explains the 2×2 Hermitian representation of the Minkowski quadratic
form and its Lorentz action. It provides context for the rank-one cone identity;
it does not establish the specific force or any quantum interpretation here.

Brown and Kuchar, [Dust as a Standard of Space and Time in Canonical Quantum Gravity](https://arxiv.org/pdf/gr-qc/9409001),
section II, derives the dust normalization, continuity equation and proper-time
field along dust worldlines. Those distinctions motivate checking source
continuity and time interpretation separately. The present six-channel map
does not retain their independent dust reference fields or an apparatus.

The new algebraic identities, complete-state comparisons, domain theorem and
numerical errors are evidence from this implementation. They are not claims
borrowed from those papers.
