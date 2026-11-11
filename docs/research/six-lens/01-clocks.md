# Clock and causality audit

Baseline: GitHub main `7d238e84a2167a4d3fe7bc7942da0cbf97bd29b2`,
including merged Frame48 (#36) and Bell/Born audit (#37). Current active
source/text blobs were checked against the remote tree by the parent audit.
This investigation changes no production law or initialization API.

## Result

There is one reversible update rule, but there is not yet one experimentally
validated physical clock/cone shared by all components. Three different
notions must stay distinct:

1. A global mathematical state and its update index describe the simulation.
2. Retained local processes can serve as clocks and communicate phase.
3. A physical clock must agree with the metric along its actual worldline,
   using a calibration fixed before testing other velocities and locations.

The message lanes meet local-communication requirements on their prepared
sector. The default ADM arithmetic still uses synchronized per-node clock
banks. These banks are required by that finite arithmetic construction;
removing them would disable computations. Neither fact proves or disproves
an emergent relativistic limit.

## Reproduced evidence

Run from the repository root:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python experiments/research/six_lens_clocks.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python -m unittest universe24.tests.test_metric_clocks universe24.tests.test_transported_probe -v
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python -m unittest universe24.tests.test_communication universe24.tests.test_causal_wave.CausalWaveTests.test_six_directions_exact_arrival_memory_and_rewind -v
```

The two test commands passed 8 + 8 tests. The new audit passed all assertions
and writes `runs/six-lens/01-clocks/report.json`, including source hashes.
It checks counterfactual preparations and complete rewinds rather than
substituting an observer-produced state for an Engine step.

### The compiler clock is functional scheduling state

`algebra/integer_circuit.py` assigns two microticks per arithmetic DAG level.
Its `period=ticks+3` prevents wraparound during the declared horizon.
`Compiled.prepare` copies the same clock a/b phases across every spatial node.
The clock ring advances between channel indices at each node: all its spatial
offsets are zero. Arithmetic gates read these local retained clock values.
There is no runtime scheduler callback, but initialization imposes synchronized
computational phase.

The audit compiles `x*x` with x=2: 7 channels, 5 clock channels, declared
horizon 2, clock period 5. It changes the clock phase at just one spatial node,
retaining its complete local history.

| Observation | Normal clock | Clock delayed two updates at node 0 |
| --- | ---: | ---: |
| Output at node 0, update 2 | 4 | 0 |
| Output at node 0, update 4 | 4 | 4 |
| Output at unaffected node 1, update 2 | 4 | 4 |
| Output at node 0, update 7 | 8 | 4 |

Both runs rewind exactly. Setting all clock a/b registers to zero leaves the
output at zero at the declared horizon and also rewinds exactly. Thus deleting
the pulse bank is not a behavior-preserving conversion to relational time.
After wraparound the original computation fires again, producing 8 rather
than 4. This is an intentional beyond-contract negative control, not a bug
within the declared finite horizon. A longer `Engine.run` alone cannot turn
the compiled ADM construction into an autonomous infinite-horizon universe.

### Communication cones do not yet measure the ADM light cone

`layers/communication.py` implements one-edge-per-update translation on
prepared histories. Its receiver changes only upon local arrival; the empty
network has no ticks. Six-direction signed-bigint transport, empty-network,
arrival and inverse tests pass. The causal-wave test also confirms its C2
memory arrival after three edges, followed by a four-step local memory cycle.
The number three here is the selected travel distance, not a universal third
update law. A single C2 reception can initiate a cycle without producing a new
C2 on every subsequent cycle phase.

The audit inspects the complete `UniverseProgram` tensor with communication,
transported probe and causal wave enabled. There are **zero cross-component
monomials**. This uses a small compiled arithmetic component to inspect the
same assembly constructors cheaply; it is not a replacement ADM test run.
Code inspection confirms the assembly does not add such couplings for ADM.
Consequently the wave does not read the ADM metric, and its response does not
source that metric. Its guaranteed cone is a dependency cone in board updates.

For comparison, a coordinate tangent `(1,1,0,0)` is null for
`diag(-1,1,1,1)` and timelike for `diag(-4,1,1,1)`. A fixed numerical velocity
cannot be called lightlike in both with the same coordinate calibration.
This is a metric identity, not an attempted calibration of arithmetic
microticks. A common physical interpretation requires an explicit mapping,
metric-sensitive propagation and tests in nontrivial gauges.

### Proper-time readouts and physical clock mechanisms

`observe/metric_clocks.py` correctly computes
`(d tau/dt)^2=-g_mu_nu (1,v)^mu (1,v)^nu` for a supplied tangent. The tests
cover motion, null/spacelike tangents, shifts and nonunit lapse. It is passive:
it does not propagate a clock, integrate its worldline or change the next
Engine state. An algebraically correct readout is not yet an independent
ticking apparatus.

The transported-clock experiment does contain actual moving oscillators.
The audit reran five preparations for 24 updates each with one fixed tensor
and fixed flat calibrations. All rewinds passed; the general common-metric
gate remained **false**:

| Curvature / transverse position | Metric proper-rate squared | Candidate measured rate squared | Joint metric/clock gate |
| --- | ---: | ---: | --- |
| Flat, center and displaced control | 3/4 | 3/4 | Pass |
| Curved, central axis | 3/4 | 3/4 | Restricted pass |
| Curved, x-displaced | 1/4 | 3 | Fail |
| Curved, y-displaced | 5/4 | No completed cycle | Fail |

The x-displaced measured squared rate is twelve times the target. Transport
also fails the transverse geodesic equation off axis. A separate test changes
only geometry, holding all complete nongeometric initial data fixed: the
candidate clock changes, but the marker and control clock do not. There is
real geometric response, with an incorrect general physical response.

### What the new compact models contribute

| Construction | What is retained | Clock/cone limitation |
| --- | --- | --- |
| Default ADM | Finite arithmetic history and synchronized computational clock ring | Metric rate is a passive readout; horizon expansion allocates more workspace |
| Compact FLRW | Conformal counter q, proper-time counter c6, null affine counter l30, homogeneous sources/geometry | Exact prepared homogeneous family; affine counter does not transport a photon |
| Compact null wave | Two transported profile banks | No physical clock apparatus; a chosen prepared sector |
| Frame48 | Two frame-evolution slices in 48 channels | No independent retained clock; synchronous gauge is not a general clock test |

In the new FLRW check, changing dust A from 1 to 2 leaves q=10 at update 8
in both runs, while proper time changes from 1150/3 to 2150/3 and scale factor
from 110 to 210. Both complete histories rewind and every remainder stays
fixed. Both runs produce **zero C1 and C2 events**. Therefore a retained
proper-time counter and geometry evolution do not, by themselves, supply
the proposed C2/complexity mechanism. This is a statement about these two
prepared runs, not a general absence theorem for all future clock designs.

## Four decisive next gates

1. **One operational metric.** Couple a transported signal and at least two
   independent clock mechanisms to the same evolving metric. Keep calibration
   fixed, change velocity, position, lapse and shift, and test null propagation,
   accumulated proper time and redshift. Include the already failing off-axis
   cases as held-out tests.
2. **Autonomous scheduling.** Replace the finite arithmetic compiler only with
   a declared recurrent local construction. Test local phase perturbations,
   long runs beyond prior horizons and exact complete-state inverse. Removing
   clock channels or relabeling the update counter is not this construction.
3. **Common spacetime limit.** Define the map from microsteps and board links to
   physical events. Test anisotropy, dispersion and boosted/shifted descriptions
   under refinement. A nearest-neighbor dependency bound alone does not prove
   Lorentz-invariant physical propagation.
4. **Operational complexity.** Define a structural statistic independently of
   update count, integer magnitude and the chosen click filter. A closed
   complete-state cycle has identical complexity on return; it cannot have
   strictly increasing complexity each cycle. Test an explicit local mechanism
   that preserves information and changes structure before interpreting the
   whole universe as a clock that drives complexity.

The proper-time and metric-null benchmark is the standard geometric one;
see David Tong's primary lecture notes, [Geodesics in Spacetime, section 1.2](https://www.damtp.cam.ac.uk/user/tong/gr/grhtml/S1.html)
and [Riemannian Geometry, section 3](https://www.damtp.cam.ac.uk/user/tong/gr/grhtml/S3.html).
The equations establish what must be tested. They do not establish that this
repository's clocks or computational cones meet those tests.
