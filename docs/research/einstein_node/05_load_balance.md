# Computational load, local clocks and Einstein dynamics

Agent 5 of the requested eight-part investigation. Baseline main:
`4c494c1188f70eb8a677bf59765cc6e8571c6b88`. Inspected the one-system contract,
the Engine, passive metric-clock reader and the PR #50 research reports. This
report adds no runtime model and does not change any physical acceptance gate.

## Finding

The present model has no mechanism by which computer workload slows a physical
clock. `universe24/core/engine.py:361` computes every next state from the same
old integer snapshot. Its choice between int64 and Python integers changes
implementation cost, not the mathematical update. `system/runtime.py:80` measures
integer bit length; lines 152–165 record it after updates without feeding it
back. `observe/metric_clocks.py:5` instead reads a rate from an already supplied
four-metric, and explicitly does not integrate a clock or prove geodesic motion.

Four meanings of “load” should therefore be distinguished:

| Proposed meaning | What would follow |
| --- | --- |
| CPU occupancy, implementation speed or added host work | It is absent from the physical transition inputs. The exact control below confirms unchanged states and clicks. |
| Integer representation cost | It is an audited resource cost. Identifying it with proper time would require a representation-independent physical definition and a new retained coupling. Bit growth alone supplies neither. |
| Local retained activity, occupancy or oscillation rate | It can be proposed as a physical observable, then tested. Local reversibility does not make it decrease or equalize. A scalar rate alone does not determine a general metric. |
| Locally exchanged stress-energy and compatible geometry | This is a meaningful possible unification target. Its conservation identities, common metric, constraints and continuum limit must be derived from the actual tensor. Renaming it computational load would not supply those derivations. |

The host-work countercontrol does **not** disprove a theory of intrinsic physical
computation. Such a theory would concern retained microscopic states, not the
execution time of this simulator. It needs its own observable and falsifying test.

## Fresh executable evidence

Run:

```bash
python -m validation.einstein_node_audit.load_invariance
```

Output: `runs/einstein-node/load_invariance.json`. The file contains complete
tensor and seed, all 129 baseline states, every baseline click row, per-mode
state/click hashes, an independent scalar oracle and source SHA-256 hashes.
There is no timing comparison or claim about a physical clock period.

The fixed one-channel law is `u(x)=3[b(x+ex)+b(x-ex)]` on 27 periodic nodes.
Its two monomials each use one face edge, and all six remainder classes are
present. A signed nonuniform seed runs for 128 steps in three modes:

1. The unchanged Engine using its int64 evaluator.
2. A source-only subclass selecting the existing exact Python-object evaluator.
3. The unchanged Engine, with 500 discarded host multiplications before each
   step. Those calculations never enter the state, tensor or observer.

All **20,736** retained-integer backend comparisons, **10,368** independent
scalar-oracle comparisons and **256** complete click-transition comparisons
pass. The third mode performs **64,000** extra host multiplications. The object
mode really executes all 128 forward steps through the Python-integer path.
All three complete trajectories rewind exactly. The maximum retained bit length
over the baseline trace is 10. No production methods are monkeypatched.

A separate complete-state period-three orbit of that same tensor has spatial
`b` variance `2/9 → 8/9 → 2/9 → 2/9`, while retaining every remainder. Thus even
this bounded reversible local law does not monotonically equalize an amplitude
load proxy. This is a counterexample to a generic implication, not an assertion
that this variance is energy or complexity. As with any full periodic orbit,
a strictly decreasing state function cannot decrease at every step around it.

## Why a clock rate does not fix gravity

In units `c=1`, the ADM line element gives a moving clock

\[
\left(\frac{d\tau}{dt}\right)^2
=N^2-h_{ij}(v^i+\beta^i)(v^j+\beta^j).
\]

A proposed relation `N=f(load)` fixes only a normal-observer rate in a chosen
foliation. It does not specify the spatial metric, shift, stress tensor or
curvature evolution. Even a static zero-shift scalar lapse leaves all six
spatial-metric components undetermined. General reconstruction needs independent
motion and signal-direction measurements. This is an underdetermination claim
about a rate observable, not an information-capacity theorem about an unbounded
integer encoding.

Two decisive controls are a varying lapse in flat accelerated coordinates and
flat-slicing de Sitter geometry with unit lapse. The first has nonuniform
stationary rates without spacetime curvature; the second has curvature without
a varying stationary rate. The clock-geometry companion report executes these
controls. A weak, static identification of load with a Newtonian potential may
reproduce a redshift relation, but does not establish general Einstein dynamics.

## A more precise unifying principle to investigate

**Local conserved exchange, plus consistency of different spacetime slicing
descriptions, is a stronger target than equalizing a scalar workload.** This is
a proposed research direction, not a new theorem about Universe24.

The continuum hypersurface-deformation relation has the schematic smeared form

\[
\{H[N],H[M]\}
=D\!\left[h^{ij}(N\partial_jM-M\partial_jN)\right],
\]

up to the convention for bracket and deformation signs. Two different local
normal advances compose to a spatial deformation determined by the same metric.
Reordering evaluations that all read one immutable old snapshot is much weaker;
it does not test this geometric relation. A discrete/refined counterpart is an
explicit future target, not a property already supplied by Rule3.

The existing reciprocal face-flux and native-coordinate work in PR #50 supplies
possible algebraic ingredients. It should not be reintroduced as another
independent physical universe. An exact balance can be formulated as
`Q_x(next)-Q_x(old) = sum_y J_yx`, with antisymmetric edge transfers and complete
retained interaction state. In curved spacetime, the corresponding physical
claim must use covariant stress conservation and account for geometric work;
a universal conserved global gravitational-energy sum is not assumed.

## Primary sources actually inspected

| Source and inspected material | Contribution and limit |
| --- | --- |
| Teitelboim (1973), [How Commutators of Constraints Reflect the Spacetime Structure](https://www.fis.uc.cl/~mbanados/Cursos/TopicosRelatividadAvanzada/Teitelboim.pdf), pp. 542–546, especially equations (4)–(6) and the path-independence assumptions | Derives the geometric constraint commutators from consistency of evolution between hypersurfaces. It is not a derivation from processor load, nor an existing integer update algorithm. |
| Jacobson (1995), [Thermodynamics of Spacetime](https://arxiv.org/html/gr-qc/9504004v2), opening derivation through heat flux and local horizon construction | Derives Einstein's equation using horizon-area entropy, Unruh temperature, local equilibrium and heat flux for all local Rindler horizons. These are substantial physical assumptions. It does not identify entropy or energy with an integer bit length or click count. |
| Bahr and Dittrich (2009), [Breaking and restoring of diffeomorphism symmetry in discrete gravity](https://arxiv.org/html/0909.5688v1), section 0.2, equations (1)–(6) | Shows how discretization can destroy reparametrization freedom; the discrete time variation need not follow automatically from the configuration variation. Symmetry requires its own construction or continuum recovery. A reversible step is insufficient. |
| Bombelli, Henson and Sorkin (2006/2009), [Discreteness without symmetry breaking](https://arxiv.org/abs/gr-qc/0605006), abstract/theorem statement only | Their result concerns Lorentz-invariant Poisson sprinklings and excludes an equivariantly assigned finite-valency graph in that setting. It does not prove every finite-neighbor cellular model impossible. A cubic lattice's continuum Lorentz limit remains a separate test. |

Hojman–Kuchar–Teitelboim's 1976 article was located bibliographically but its
publisher full text was unavailable in this session; no stronger uniqueness
claim from that article is used here.

## Falsifying tests for an intrinsic-load proposal

1. Define a retained, local load observable and its units before fitting clocks.
   State whether it is invariant under permitted physical-state re-encodings.
   Preserve the host-backend invariance demonstrated here.
2. Prepare two independently constructed physical clocks in one metric. Change
   load, velocity and orientation separately. Require a single calibration to
   predict both clocks, signal delays and free-fall trajectories, with explicit
   clock/apparatus stress or a justified test approximation.
3. Include accelerated flat-coordinate and unit-lapse curved controls. Declare
   a failure if a rate-only construction conflates their curvature or tidal data.
4. Prove a constraint propagation identity for the actual compiled map, for
   example `C(F(z))=A(z)C(z)` on its declared domain, then check refinement against
   independent Einstein residuals. An arbitrary new quantity called a constraint
   is insufficient without its continuum relation.
5. When the candidate can represent changes of slicing, compare the two ordered
   normal deformations against the spatial deformation generated by the same
   metric. This requires an explicit discrete implementation; it cannot be
   certified by the current synchronous host loop alone.

Any local scheduling or gating state must fit the shared 48-channel budget,
preserve the degree-three single-face tensor contract and retain the complete
inverse. No external load-dependent delay, normalization or solver may become
an uncounted physical input.
