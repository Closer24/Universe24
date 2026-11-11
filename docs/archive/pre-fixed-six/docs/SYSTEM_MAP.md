# What the executable system establishes

The default construction is a generic exact local automaton with a fixed rank-four polynomial input tensor and a complete initial state. It is **not yet a model in which all the intended physical phenomena have been derived**. The tensor defines several independent subsystems; putting them in one array does not create interactions between them.

This document separates the algebra, the executable dependency graph and the interpretation. The current equations are in [MODEL](MODEL.md); [VALIDATION](VALIDATION.md) records actual executions. Historical experiments remain evidence about their stated configurations, not certificates for the current default.

## One generic transition

For gear type i at node x, the retained state is (a,b,r), with integer a,b and 0 ≤ r < D. The default has 382 gear types, Q=8,589,934,593 and D=6Q. Its 48-type binary-octahedral block is only one component.

The fixed input tensor evaluates

    u_i(x) = sum_m c_m product_f v_f(x + d_f),   v_f in {a_j,b_j}.

There are at most three input factors per monomial. Including its output index gives tensor rank at most four; constants and lower-degree terms are included using a fixed unit coordinate. Here rank means tensor order (number of indices), not matrix rank, decomposition rank or the dimension of spacetime.

Every gear applies the same transition:

    ell, r_next = divmod(2*u + r, D)
    a_next = b
    b_next = ell - a

`core/engine.py` has no update branch on a physical name, observer label, block, link axis or field sign. It gathers indexed old-state values, multiplies by fixed integer coefficients and evaluates Rule3. All outputs read the same old snapshot. A regression changes names, labels, link metadata and field signs while retaining the indexed polynomial, and compares the complete forward and inverse histories.

The default `jpure` preparation uses floating-point projection and norm matching to choose an integer seed. Once prepared, every retained register and every forward update is exact. Replaying the exported complete seed avoids depending on cross-version floating-point preparation reproducibility; a random-seed number alone is not the whole initial condition.

There is one common divisor, not an independently chosen num/den at each gear. The coefficients, number of gears and field content are choices of construction; Rule3 alone does not uniquely derive them. The old-a field is retained state, not an extra clock or a second forward update.

The int64 implementation uses conservative exact bounds and switches to Python integers before unsafe arithmetic. Serialization retains integer values. Passive click extraction and mirror maps must obey the same exactness requirement; large-divisor reload and mirror regressions cover cases in which small arrays were compacted back to int64.

## Why the algebra is reversible and local

From a new state, old b is a_next. If u contains only old-b values, its exact old input is immediately known. Otherwise the constructor requires an acyclic dependency graph for old-a reads, so old-a values are recovered in a validated order. At each recovered gear:

    r_old = (r_next - 2*u_old) mod D
    a_old = (2*u_old + r_old - r_next)//D - b_next

The numerator is divisible by D, and Euclidean division fixes the unique r_old. Induction through the dependency stages gives both W_inverse W = id and W W_inverse = id. The inverse stages are recovery steps, not additional forward laws. This does not prove bounded trajectories, positive physical energy or a time-mirror symmetry.

Each tensor monomial reads its target storage node and at most one face neighbor. By induction, after n updates a register can depend only on initial storage sites within n lattice edges. The periodic cube, its boundary condition and update schedule are specified before the run; they are not emergent Einstein spacetime.

A physical link is stored at its base node, but geometrically has two endpoints. The default has 3,300 monomials whose geometric support fails the stronger single-physical-edge condition. The [optional mediator construction](SINGLE_EDGE_IMPLEMENTATION.md) removes this violation with the same Rule3 and rank bound. It changes the dynamics, adds 90 gear types and is not a proven physics-preserving replacement. Neither implementation should be reported as satisfying both all physical goals and all locality goals.

For b-only inputs the map M(a,b,r)=(b,a,D−1−r) is a reversor. This result does not extend to arbitrary old-a inputs. Termwise divisibility of coefficients by Q is sufficient to preserve the remainder class modulo Q, but is not necessary: integer-valued polynomials can have divisible values without divisible coefficients. Divisibility alone does not establish a reversor for old-a couplings.

## What actually communicates

Run the passive census from the repository root:

```bash
python -m universe24.tools.system_inventory --out runs/system-inventory.json
```

It reads the canonical, merged tensor, so canceled terms do not become fictitious edges. An input read defines a directed edge from the input gear type to the output gear type. Forgetting spatial offsets overestimates possible influence. Therefore **absence of a path proves that changing only the source gears' initial registers cannot change the target history, for every seed and horizon**; presence of a path only permits influence and does not prove an excited signal or a physical interaction.

The current default has these six independent namespace groups:

| Group | Namespaces | Interpretation of the construction |
|---|---|---|
| Proposed interacting core | ref, metric, beta, bgk, matter, matter2, em, wsu2, chiral | L0, metric/load, electromagnetic and weak/matter couplings; incomplete gravitational clock response |
| Choice experiment | arm1, arm2, router, gate, exit | Prepared clock arms and routing experiment; isolated from proposed matter |
| Cosmic experiment | cosmic | Hand, readers, loads and recording gears; isolated from all other groups |
| Separate SU(2) experiment | su2 | Gauge block with its own internal matter |
| Separate SU(3) experiment | su3 | Gauge block with its own internal matter |
| Separate U(1) experiment | u1 | Gauge block with its own internal matter |

No live monomial crosses between these groups in either direction, so their full state updates factorize. This does not imply statistical independence when the initial seeds are correlated. Namespace aggregation is coarse: the gear-type graph has 15 weak components, including nine isolated metric gears. The report lists the precise members and directed reachability. It does not assert that every gear within a namespace group is dynamically coupled to every other one.

The checked-in [inventory](evidence/system_inventory.json) identifies the exact tensor by its fingerprints. Its 22 builder blocks have 382 declared types in total. Blocks such as ehop, gwb and lapseL0 add coefficients to existing gears without adding new gear types; the empty lapse block adds neither. Raw builder term counts must not be confused with 18,592 live monomials after cancellation and merging.

The optional [connected-clock preset](CLOCK_RESEARCH.md) changes that construction before evolution. Seven additional local clocks, complete-multiplet ports and a recording-sum bridge join the 389 gear types into one weak dependency component. Paired controls demonstrate transfer in both directions; a zero-bridge control removes it. The original 382-type default and this inventory remain unchanged. Connectivity is not a stability or shared-metric theorem: zero unforced multiplets can remain dormant, randomized clock phases do not spontaneously align in the tested preparation, and metric growth remains visible.

## A precise obstruction to the current choice interpretation

For the cosmic preparation let c be its fixed pair coefficient and I=b_M1²+b_M2². In each preparation require a_L=b_L for both loads (so they remain static), Lp+Lm=D/(2c), and r_dp=r_dm. Between the two compared preparations require equal complete hand/reader states (a,b,r) and equal Delta_a,Delta_b; the load split and shared token may differ. The pair inputs are u_dp=c I Lp and u_dm=−c I Lm. Equal initial pair remainders remain equal because their inputs differ by a multiple of D. Exact Euclidean division then gives

    ell_dp - ell_dm = I,
    Delta_a_next = Delta_b,
    Delta_b_next = I - Delta_a,

where Delta means the dp−dm difference. These equations do not depend on the load split or the shared token remainder.

The hand's input from the recording pair depends only on this difference; its other inputs are hand values. M1 and M2 read the hand and neighboring reader values. Hence, for preparations with equal initial hand/readers/Delta and the declared static loads, induction proves the entire future hand/reader/Delta history is independent of the load split and token. Individual recording-gear quotients and click classes can still differ. `test_one.TestOne.test_O8_history_independent_of_outcomes` checks this same cosmic mechanism in the explicitly rejected coupled comparison. A separate 12-update default control is recorded in the integration evidence; neither run replaces the induction proof.

This is a conditional exact obstruction, not a claim about all possible seeds or tensors. In the current preparation the different detector records do **not** select different future hand/matter trajectories. A preference for complexity, collapse or irreversible removal of alternative complete states has not been derived. Fixing that requires a newly specified coupling with its own algebra and tests, not relabeling the third click class.

## Claims and their evidence boundaries

| Claim | Evidence | What it does not establish |
|---|---|---|
| Same exact scalar law for all gears | `Engine.step`, independent scalar receiver audit, metadata invariance regression | Uniqueness of the chosen tensor or emergence of its coefficients |
| Full-state reversibility | Constructive inverse above; core, migration and strict-edge tests | Boundedness, thermodynamic energy, CPT or arbitrary proposed mirror |
| Local storage influence | Constructor validation; finite-cone induction; perturbation audit | Single-physical-edge support for the default; Lorentz invariance |
| 24 cube rotations and their 48-element double cover | Exact quaternion/group construction in `algebra/group_2o.py` and coupling checks | Continuous spacetime symmetry or reflection symmetry of the complete tensor |
| Field representations | Explicit matrices, quaternion operations and scoped covariance tests in matter/gauge/chiral modules | Identification of an excitation as an observed particle |
| Official click stream | Nonzero quotient, changed triple and official label; saved-event decoder agrees with online readout | Wavefunction collapse, general quantum measurement statistics or physical detection efficiency |
| Quotient ledger and remainder parity | Exact identities, tested including large integers | A positive conserved energy or decreasing thermodynamic entropy |
| Carry-weight proportions | Declared matched-remainder/load preparation and telescoping quotient identity | Born probabilities for counts of official records, independent repeated measurements or a complexity optimizer |
| Electromagnetic identities | Scoped `test_em`, system balance checks and the explicit strict-edge observation map | General electrodynamics inferred solely from official clicks |
| Complete weak gauge symmetry | Standalone identities pass, but E1 breaks composed t1/t2 balances; t3 survives the stated test | Full interacting electroweak gauge symmetry of the default |
| Clock universality | Reconstructed-input identity is checked; recorded raw site-frequency criterion fails | Independently observed universal clock response |
| Einstein candidates | Optional imposed ansatz and scoped algebra/response tests | Full Einstein equations, universal proper time or spacetime emergent in the default |
| Cosmic clocks respond to the metric | Fails structurally: no dependency path; paired seeds give identical clock records | Cannot be claimed as universal gravitational clock response |
| Stability | Only declared seeds, parameters and horizons; long gauge negative controls remain failures | Stability for all preparations, or for arbitrary long runs |
| Bell-style route | TC.15 remains a recorded expected failure of the proposed physical criterion | A derived Bell-consistent quantum model |

A passive state diagnostic is not an official-event-only observable. Tests using field arrays are labeled as such; only the event decoder and explicitly declared event analyses can support claims about information available in the clicks alone.

## Module responsibilities and experimental scope

| Files or directory under `universe24/` | Responsibility and scope |
|---|---|
| `core/engine.py`, `tensor.py`, `lattice.py` | Generic arithmetic, validated fixed polynomial and prescribed periodic geometry |
| `core/reciprocity.py`, `reversors.py` | Passive algebraic checks and audit maps; not extra evolution |
| `algebra/group_2o.py`, `coupling.py` | Exact finite group and reference coupling construction |
| `layers/one.py`, `system.py`, `reference.py` | Active construction and composition; selected coefficients fixed before a run |
| `layers/matter.py`, `gauge.py`, `links.py` | Field and link building blocks; link metadata alone is not a force |
| `layers/em.py`, `em_dressed.py`, `chiral.py`, `electroweak.py` | Current electromagnetic/weak construction and its explicitly limited identities |
| `layers/gravity.py`, `gravity_select.py`, `gravity_l0.py`, `gravity_l0c.py`, `gravity_beta_fix.py`, `matter_lapse_c.py` | Metric/lapse candidates and composition helpers; actual enabled coefficients govern the claims |
| `layers/choice.py`, `choice_oddq.py`, `choice_round.py` | Prepared choice/router variants; using the same recurrence does not prove quantum measurement |
| `layers/strict_edge.py` | Optional locality experiment, not default physical equivalence |
| `layers/clock_network.py`, `clock_bridge.py` | Optional complete-multiplet clock ports and record-sum feedback, compiled into a fixed tensor |
| `layers/resolution.py`, `prepare/resolution.py` | Exact coefficient/divisor/seed embedding; preserves source trajectories rather than stabilizing them |
| `layers/involution_clock.py` | Bounded Boolean routing sector compiled from two local involutions; distinct from the default field tensor |
| `layers/einstein.py`, `gravity_hybrid.py`, `clockgen.py`, `onematter.py`, `em_compact.py`, `electroweak_b.py`, `universality.py`, `c2_zq8.py` | Optional or comparison constructions; their conclusions apply only to their stated tensor and preparation |
| `prepare/` | Complete initial states, selected backgrounds, packets and ensembles; no mutation during forward evolution |
| `observe/` | Passive state/event diagnostics for the named construction; no feedback into the forward rule |
| `tools/audit_contract.py`, `physics_gate.py`, `system_inventory.py` | Reproducible audit, physical negative controls and structural census |
| `tools/connected_clocks.py`, `clock_epochs.py`, `metric_clock_gate.py` | Declared candidate and paired controls, passive epoch diagnostics, and raw-clock universality gate |
| `demos/one/run_one.py`, package `__main__.py` | Default executable run and reports |
| Other `demos/` | Scoped research experiments, sometimes expensive; new output goes under `runs/` |
| `tests/` | Exact checks and declared numerical regressions, including known negative physical findings |
| `results/`, `full_picture_2026-11-10/`, `NOTES*`, manifests | Historical evidence and interpretations, retained with original configuration/provenance; not current guarantees |

`prepare/seed.py:pplus_seed_hook` is an explicit unsupported preparation. `one_system(families != 1)` and combining the rejected doublet coupling with route B are unsupported. The base `StateMap` is abstract. These are not used by the default run. Optional Einstein time-derivative completion, full electroweak beta dressing, universal gravitational clock response and an autonomous trajectory-selection mechanism remain research tasks; this audit does not silently fill them with externally selected outcomes.

The demos `demos/gravity/census.py` and `demos/system/dirac_formc_check.py` use test helpers and require a source checkout. Several historical EM experiment scripts execute their experiment when imported; run them explicitly instead of importing every demo as a library. Module and direct-file execution are supported for the EM scripts; their fresh outputs are separate from checked-in historical inputs.
