# Dynamic links, natural states and the Einstein acceptance boundary

The candidate implements coupled node/link evolution through the existing
Engine. It does **not** complete a discrete Einstein universe. The separate
frozen-delay result cannot be pooled with this candidate to claim dynamic
length-calibrated transport.

## Construction and counted state

The periodic cube has six incident links per node and one independent state
per undirected link. Both endpoints read and affect that same state. Its
positive-axis array address is storage, not physical ownership by a node.

| Retained field | Channels per array cell |
| --- | ---: |
| Six directional node ports | 6 |
| Autonomous period-two reference | 1 |
| One link field on each positive axis | 3 |
| Total | 10 channels, 30 integers |

Every channel retains its full `(a,b,r)` triple. The tensor is fixed, degree
three, with strict single-face physical support and no old-`a` dependencies.
No external schedule, projection or extra link bank advances the state.
The period-two reference is not an elapsed proper-time apparatus. An Engine
update index is a computational ordering, not an established physical time.

The independent reversible map is `P=G S`. `S` swaps opposite ports onsite
and flips the reference bit. `G` acts on disjoint edge triplets `(x,y,q)`:

* If `q=0`, exchange the two endpoint ports; if `q=1`, keep them.
* Update the shared link to `q XOR x XOR y`.

The inverse exchanges endpoint values when the *current* `q=1`, then applies
the same XOR for the old link. When `x=y` an exchange is immaterial; otherwise
the XOR flips `q`, which recovers the forward exchange decision. The inverse
of `P` is `S^-1 G^-1`. Each output and each inverse output has a cubic or
lower polynomial representation with allowed physical support.

This is a bounded reversible scattering construction. The conserved Boolean
port population has not been identified with physical energy or stress.

## Exact positive domain

Let `z` be any complete Boolean configuration, including link and reference
bits. Prepare the raw histories as

```text
b = 1 + z
a = 1 + P^-1(z)
r = any fixed pattern in {1,2,3,4,5}
u = 6 + 3*(P(b-1) + P^-1(b-1))
```

The last expression is expanded into the fixed integer tensor before
execution. The Engine never calls the Boolean map. Since `2*u` is divisible
by6, unchanged Rule3 gives

```text
r_next = r
a_next = 1 + z
b_next = 1 + P(z)
```

Thus this declared domain is invariant for all updates, not only the finite
test horizon. It supports both endpoint-driven link changes and link-driven
routing. Raw retained histories stay in `{1,2}` and carries stay positive.
Polynomial coefficients remain signed integers and Rule3 still subtracts
`a`. This is a natural-valued state sector, **not** a rewrite using only
natural coefficients or addition-only arithmetic.

Natural initial data alone is insufficient. In the empty prepared case,
change one old `a` from 1 to 5, retaining positive `b` and `r`. The next `b`
is `-3`. The runtime preserves and rewinds this negative value; it does not
clip it. The prepared-history condition is therefore part of the model's
domain, not optional initialization advice.

## Registered native runs and failure controls

Reproduce in a new directory:

```bash
python -m validation.dynamic_link_naturals --out runs/new-dynamic-natural-links
python -m unittest universe24.tests.test_dynamic_link_naturals -v
```

The registered panel has 17 bundles: an empty case, twelve single-payload
cases covering two proposed lengths and six directions, three dense seeded
preparations, and a 64-node, 512-update run. The total is 1,504 forward updates,
plus exact replay, inverse and independent-oracle checks. All bundles use
one tensor and ordinary `system.runtime`. Complete histories, carries,
protocols, allocations, source hashes and bit growth are retained.

Every state is compared with both an independent scalar implementation of
Rule3 and the independent reversible circuit. Checks include both histories,
carry retention, strict positivity, payload count, link changes and complete
rewind. The single-payload 27-node cases recur after 24 updates; finite
recurrence is recorded, not interpreted as growth or cosmology.

| Interpretation or requirement | Disposition |
| --- | --- |
| Exact Rule3, degree/locality/budget, synchronous state and inverse | Mechanically testable; required for every saved case |
| Strictly natural retained state | Valid on the complete prepared-history domain |
| Arbitrary positive histories remain positive | Failed: explicit next value `-3` |
| Link values1/2 imply initial-length/c delays1/2 at one unit per update | Failed: measured arrivals1/3 in each of six directions |
| Physical null transport on a changing metric | Not tested: no metric/clock identification is provided |
| General Einstein/Regge equations for the coupled candidate | Not tested |
| Closeness to general Einstein spacetime | Blocked by missing physical model and failed simple interpretations |

The report's `general_length_equals_transit_time` gate refers to the tested
**initial-value divided by fixed c** prescription, with updates as the
proposed time unit. It is not a theorem about changing physical lengths:
in a time-dependent geometry, a length at emission need not equal the total
flight time times `c`. A null path, clock calibration and evolution of the
metric would have to determine that flight time. They are absent here.

A separate negative control adds endpoint-driven changes directly to the
earlier frozen-selector tensor. Its selector chart fails after one update,
so the old fixed-permutation proof no longer applies. Its reference clock
was already signed; the report separately records negative nonclock values
to avoid attributing that old oscillator property to the new feedback.
This failed direct merge is not a no-go theorem for all dynamic delay laws.

Two inherited independent controls expose other missing pieces:

* Equal-length face-only shortest paths give distance 2 for displacement
  `(1,1,0)` instead of `sqrt(2)` under the tested refinement. The 41.421%
  error does not decrease. This tests that graph-distance interpretation,
  not every possible effective wave dynamics on a cubic lattice.
* A flat Rindler metric has equal spatial edge lengths but unequal stationary
  clock rates. Independent symbolic Einstein residuals vanish, while spatial
  lengths alone do not identify those observer clocks or null flight times.
  Extra clock information might emerge from additional retained dynamics;
  it has not emerged in this candidate.

The source-only central acceptance command separately runs the repository's
existing homogeneous massless, anisotropic, massive, finite null-source and
gauge constructions. These are distinct tensors and physical domains.
Their restricted Einstein successes cannot validate this new scatterer or
certify one combined model.

Evidence from this execution belongs under
`runs/dynamic-link-naturals-20261113/`,
`runs/full-acceptance-20261113/` and
`runs/dynamic-link-review-20261113/`.

## Completed execution, 2026-11-13

* All 17 new coupled bundles passed, totaling 1,504 forward updates. Peak
  retained integer size was 3 bits. Source fingerprints still match.
* Central acceptance completed 20 saved trajectories, totaling 145 forward
  transitions, with software execution passed and general physical
  acceptance blocked. Restricted physical successes retain their own laws.
* A passive scan of every serialized before/after retained entry found
  negative values in 13 of the 20 central trajectories. The other seven
  contain zero; none is strictly positive throughout. All 17 new candidate
  trajectories were strictly positive. See `natural_state_audit.json` in
  the review evidence directory, including a first offending entry per run.
* Full discovery passed 533 tests in 193.825 seconds. The generic mechanical
  smoke, supported CLI replay and whitespace check also passed. Historical
  oversized models exercised by tests do not become budget-approved models.

### Rest-length-one spring control

The repository already has reciprocal spring terms in
`universe24/layers/clock_network.py` and `strict_edge.py`. They are fixed
tensor terms; naming a retained channel `length` does not install them.

A new isolated control uses `u=3*b+3` on each link channel. With all retained
carries unchanged, exact Rule3 gives

```text
L_next - 2*L + L_previous = -(L-1).
```

The preparation `a=b=1` is an exact fixed point. With old length 1,
the measured current-length sequences were:

| Initial length | Current length over six updates |
| --- | --- |
| 1 | 1,1,1,1,1,1,1 |
| 2 | 2,2,1,0,0,1,2 |
| 3 | 3,3,1,-1,-1,1,3 |

All three isolated bundles passed scalar-oracle, saved replay and inverse
checks. This shows why an ordinary linear restoring term does not
guarantee positive geometric lengths. Rest length 1 is a declared reference,
not a derived universal Einstein-vacuum condition. Oscillation has not been
identified as a cosmological bang, bounce or matter-producing event.

### Geometry representation comparison

The existing passive `observe.simplex_metric` reconstructs a local Lorentzian
metric exactly from ten signed squared tangent-simplex intervals. A new
rational comparison uses spatial matrices `I` and
`[[1,1/2,0],[1/2,1,0],[0,0,1]]`, both with time component `g00=-1`.
All six axial squared lengths are 1 for both, but the xy angle is 90 versus 60
degrees and the `(1,1,0)` squared distance is 2 versus 3. Both ten-interval
roundtrips recover the original metric exactly. These are flat cell shapes,
not a curvature experiment or an evolution law. See
`geometry_representation.json` in the review evidence directory.

The design implication is recorded in
[the geometry/signal plan](proposals/LINK_GEOMETRY_SIGNAL_PLAN.md#einstein-representation-target-after-the-dynamic-and-spring-controls).

### Passage-ticks-first follow-up

The user's proposed primary quantity is now the positive integer passage
cost N, with operational length `c*tau0*N` in a declared static clock chart.
An exact affine recoding of the prior frozen-delay tensor also makes its
payloads, selectors and reference-clock histories strictly positive.
The fixed law is `u_new(A,B)=u_old(A-K,B-K)+6K`, with a,b both shifted by K
and r unchanged. K=1 for all channels except the reference clock, where K=2.
There is no mutation or state projection during execution.

The completed panel in `runs/dynamic-link-review-20261113/time-link-naturals/`
contains 21 saved runs and 204 forward updates, all with 31 channels, degree
two, no support violations and at most 3 retained bits. The 18 axial cases
measure 1,2,4-update arrival in each direction. Two mixed-delay paths and
a 128-update case also pass scalar/permutation oracles, full replay and rewind.
Delays are represented by two selector registers, not an unbounded single
integer countdown. In-flight stages are retained and counted.

This is successful static natural-valued transport. Dynamic delays, arbitrary
unbounded N, material proper-clock calibration, isotropic effective geometry
and Einstein source equations remain untested for this tensor. It cannot
inherit dynamic feedback from the separate ten-channel experiment. The
existing full-suite count remains 533; this follow-up is a separate replayed
validation script and introduces no production-source change.
