# A typed interaction-to-execution contract

The concrete unifying structure is **one local interaction specification,
one complete retained-state encoding, one compiled temporal map and one passive
observation boundary**. It is not a union of independently passing tensors.
The same Rule3 can implement many such specifications; its coefficient array
does not become a spacetime tensor merely because both are called tensors.

This report inspects PR52 at `8c53e69f4b466dcbd2da7dab7e3c365bd9731766`,
PR51 at `ff21c878cc2e6e9d0969c3538e0c676fcdab616f`, PR53 at
`73b24b788d5d3aa3c969a08ca5af16bfe532c4a4`, and the newly published PR54 at
`d4f281c0839887ac7af8c050c406b2081f7c9baf`. The checkout for this work is PR52.
The other branches were read with `git show`, not merged or silently imported.
Fresh [#40](https://github.com/Closer24/Universe24/issues/40),
[#41](https://github.com/Closer24/Universe24/issues/41) and
[#45](https://github.com/Closer24/Universe24/issues/45) discussions supply current
handoffs. Their reported runs are distinguished below from this audit's runs.

## Five objects with different responsibilities

| Object | Concrete input/output | Required checks | Existing implementation or gap |
|---|---|---|---|
| `PhysicalStateSpec` | Named fields, units, gauge, lattice, encoding and complete `(a,b,r)` preparation; one metric readout | Every field maps to owned retained entries; chart and physical/microtick relation explicit; both histories and remainders belong to the domain | `completion/common45.py` gives a specific projective full-frame instance |
| `InteractionSpec` | Onsite or single-face polynomial potential/kinetic/source terms, differentiated into all declared response ports | Degree after expansion; strict face support; reciprocal endpoint responses; all geometric/source responses counted | Generic gradient construction is possible for appropriate polynomial potentials; arbitrary Einstein dynamics is not established by it |
| `TemporalCompilation` | Immutable tensor, complete workspace/scheduler preparation, physical macrostep decoder and step ratio | Exact macro identity with carries and old histories; inverse; workspace restoration; degree/locality; coefficient/scale conditions; stability and cost separately | Projective45, native three-tick potential and native nine-tick drift/kick are distinct implementations with distinct domains |
| `DomainAndConstraintEvidence` | Predicates and identities tied to exact law/encoding; independently executable algebra or counterexample | Preparation, invariance, nondegeneracy, constraint propagation and refinement are separate obligations | PR52 proves some restricted identities and refutes several transfers; no general compatible set exists |
| `ObservationSpec` | Verified saved transitions or canonical records plus one declared interpretation and window | Input authority, before/after convention, units, law/seed/trace identity, readout domain and passivity | Existing bundle/runtime/decoder remain authoritative; the new research receipt checker binds additional interpretation/window information |

An observation specification may contain a state diagnostic or a records-only
measurement protocol. These inputs are different types. A function using hidden
`D`, frame or field values cannot be made records-only by changing a label. A
canonical arithmetic event is neither a particle nor a material clock tick
without a separately implemented and tested apparatus interpretation.

## One physical-state and metric authority

The current full45 allocation is exact:

| Retained content | Channels | Register meaning |
|---|---:|---|
| Full frame `B_ai` | 9 | Projective numerators; all nine spatial frame components |
| Symmetric `K_ab` | 6 | Extrinsic curvature components |
| Antisymmetric spatial connection `G_ab,c` | 9 | Three antisymmetric pairs times three directions |
| Charged scalar `phi,chi`, two momenta and six covariant gradients | 10 | Matter using the same frame |
| Electric/magnetic fields | 6 | Three of each |
| Spatial gauge potential | 3 | Temporal gauge is specified separately |
| Signed normal dust amplitude | 1 | Density is the decoded amplitude squared |
| Shared projective denominator | 1 | Retained arithmetic scale and history, not proper time |
| **Total** | **45** | **135 integers per node, including every `a,b,r`** |

For the present synchronous gauge,

\[
f=P_f/D,\qquad \gamma^{ij}=\sum_a B_{ai}B_{aj},\qquad
g=-dt^2+\gamma_{ij}dx^i dx^j.
\]

The rational readout needs its stated positive, spatially uniform denominator
domain. An inverse or square root used by a diagnostic is not an uncounted
runtime channel, but it cannot feed the Engine. `D_old=0` in the standard seed
is encoding boundary memory, not an earlier singular physical metric.

The PR51 and PR52 builders compile equal tensors at matched physical parameters,
as reported in the [cross-team join](https://github.com/Closer24/Universe24/issues/40#issuecomment-6811115398).
Their default strong/weak seeds and step sizes differ. Equality of the equation
builder is therefore weaker than equality of a complete run. Matching fields or
channel names alone does not permit transferring a clock, constraint or source
claim between these preparations.

## What a local interaction can establish

Let a discrete polynomial potential be a sum of onsite and single-face terms,
`V=sum_e V_e`, with responses `F_j=-dV/dq_j`. Static differentiation and expansion
can generate both endpoint forces and the response of any retained mediator.
The compiler must reject any resulting monomial that violates degree or support;
it cannot retain only the convenient endpoint and call that reciprocal.

For a shift-invariant potential, simultaneous `q_j -> q_j+c` gives
`sum_j F_j=0`. If an admissible native temporal compiler establishes the exact
macro map `P'_j=P_j+2F_j(S)` with all carry/work registers included, then

\[
\sum_j P'_j=\sum_j P_j.
\]

This is an exact native shift charge of that map. It is not automatically the
physical spatial momentum of curved spacetime, an exact discrete energy, or an
Einstein constraint. The geometric response and matter work identity must be
derived in the same representation. Even a reciprocal polynomial can have an
unbounded potential or an unstable discrete time map.

A useful machine-readable interaction declaration therefore needs: ordered
field/port roles; oriented physical edge; potential coefficient table; every
derivative response; source/stress entries; coefficient units; and the static
map from symbols to actual retained factors. A degree or reciprocity certificate
must be recomputed from those polynomials. A string saying `reciprocal=true`
is not such a certificate.

## The temporal and channel bottleneck

| Construction | Actual or proposed total | What fits | What does not follow |
|---|---:|---|---|
| PR52 common projective law | 45 | Geometry + charged matter + dust + scale; three slots unused | Stable waves, constraint closure or autonomous apparatus |
| Common45 plus passive `I/S` and metric diagnostics | 45 | No new retained state | A physical clock/readout interaction |
| PR54 sourced homogeneous oscillator | 47 | Shared45 plus two neutral `q,p` fields | General spatial apparatus momentum or stability |
| PR54 raw feedback record | 48 | Sourced47 plus one retained mechanical history channel | Record stress, calibrated detector or general source closure |
| Covariant real-scalar apparatus in this first-order representation | 50 before record; 51 with record | Requires `q,p` and three spatial gradients | The present 48-channel contract; this count is representation-specific |
| PR52 native nonlinear drift/kick | 7 | Two data + two quotient-work + three scheduler channels | A replacement of all full45 dynamics |
| Direct full-rank native extension to 44 data channels | 91 | `44 data +44 quotient work +3 scheduler` | A 48-channel fit |
| New low-rank scheduling proposal | `n+r+3` | At `n=44,r=1`, arithmetic count is 48 | Rank-one kinetic motion cannot be relabelled full-rank44 dynamics; encoding/symmetry/constraint checks still needed |
| PR52 native stable wave | 3 | Two chiral data fields and one sign scheduler | Full geometry or operational clock |
| Homogeneous isotropic reduction | 6 | `D,B,K,phi,Pi,d` in an explicitly constrained representation domain | Generic 3D, anisotropic, charged or Maxwell perturbations |

The low-rank row is a proposed generalization being tested in this research
round, not an imported PR52 result. Rank is the kinetic update rank in the
specified field coordinates, not the number of spatial directions. A physical
reduction must preserve the intended dynamics on an invariant domain; a cheap
rank-one replacement simply changes the dynamics unless that proof is supplied.

The seven-channel primitive's workspace is restored after nine ticks, but its
registers exist at every intermediate tick. Restoration does not remove them
from the channel budget. Conversely, replacing a denominator encoding is a new
representation and temporal compiler, not a `45+7` attachment. No shared-register
credit is valid without an explicit common encoding/inverse/domain proof.

PR54 supplies a real source interaction
`W=omega²*q²/2+g*q*(phi²+chi²)`, including reciprocal carrier forces and
homogeneous stress. Its exact energy-exchange identity is continuum and
homogeneous. Three missing gradients prevent a general covariant spatial source;
the raw48 pointer is an additional perturbation with no supplied record stress.
This is the current compatibility bottleneck in concrete form: **the desired
source/kinetic/constraint structure and the admissible temporal compiler do not
yet share one proved, budgeted retained representation**.

## Certificates that can actually be checked

The following are obligations for a common schema, not a claim that a general
proof checker already exists:

| Evidence kind | Machine-checkable object | Scope and refusal condition |
|---|---|---|
| Mechanical law | Actual coefficient/factor table, degree/support graph and full channel manifest | Delegate to `Tensor`, `SystemBundle` and existing runtime; do not duplicate them |
| Macro compilation | Exact map/decoder, number of ticks, preparation predicates, residual polynomial identities including remainders | Prove identity symbolically on its domain or publish finite verified cases; tests are not a universal proof |
| Invariant sector | Embedding `E`, extraction `R`, domain predicate and `T_full E=E T_reduced`, `R E=id` | Both histories and all carries included; no interpolation of general states into the sector |
| Constraint closure | Constraint expressions `C`, exact update and an identity such as `C(T(s))=A(s)C(s)` | Denominator/nonzero assumptions explicit; continuum tangency alone is insufficient |
| Positivity/nondegeneracy | Initial inequalities, inductive bounds, exact exceptional-domain controls | A finite positive trace cannot establish all-time invariance |
| Noether-type charge | Explicit charge and exact one/macrostep difference | Do not substitute naive point energy for a two-time charge or vice versa |
| Physical observation | Same law, complete seed, trace/window, representation, metric/gauge, units and typed input authority | Arithmetic, state-diagnostic and operational claims remain distinct |

An external proof artifact needs the exact proposition, quantified variables,
domain assumptions, actual symbolic residual or proof steps, checker/source hash
and result. Merely storing a theorem name or a `passed` string does not certify
anything. Algebraic identities can be exact; a simulation result must retain its
finite horizon, configurations and negative controls.

The new `validation/generic_structure/contracts.py` implements only the last
row's **compatibility boundary** and an append-budget ledger. It first calls the
existing `verify_run` and loads the actual bundled inputs. Its receipts bind
tensor, full seed, bundle/run, trace files, comparison interval and a declared
representation/metric/time/domain interpretation. It permits comparing different
quantities on that same authority; it does not require a metric to equal a phase.
It refuses a records-only port that lists hidden retained dependencies.

These hashes detect mismatches, not authorship or truth of the interpretation.
The checker does not execute arbitrary readout code or prove that an actual
reader obeys its dependency declaration. A separately audited reader must do
that. In-memory receipts are not authenticated certificates and may not be used
as imported proof authority. A different implementation/readout can be joined
only after a separate equivalence adapter establishes the required relation;
this checker does not guess that equivalence.

## Executed controls and status

`python -m validation.generic_structure.contracts --out runs/generic_structure/contracts`
ran the actual common45 for two updates through the ordinary runtime, bound
metric and scalar `I/S` observations to the same saved trace, and accepted that
comparison. It separately executed and verified a massless tensor and a
one-carry-changed complete preparation, then rejected both joins. Eight further
controls reject changed physical tick scale, scheduler-as-clock interpretation,
frame ordering, invariant-domain assertion, comparison window, hidden-state
access under a records-only label, `45+4` slots and duplicate ownership.
The `45+3` ledger is accepted **only arithmetically**, with no constructed coupled
tensor asserted. All ten rejection controls passed. The evidence is
`runs/generic_structure/contracts/06_contracts.json` with the three actual saved
runtime directories referenced inside it.

| Statement | Status at this checkpoint |
|---|---|
| Same verified trace + explicit meaning/window is a usable observation join boundary | Accepted as an implemented compatibility check |
| One local polynomial can generate reciprocal responses and, conditionally on its exact macro map, a shift charge | Accepted algebraic pattern; actual scope belongs to the interaction/temporal audits |
| Full45, native7, wave3 and raw48 results form one physical solution | Refuted as an evidence join; they are distinct laws/domains |
| A restored workspace costs zero channels | Refuted under the retained-state contract |
| A scalar clock, host load or canonical click label determines the full metric | Refuted in PR53 controls; no new rerun claimed here |
| A typed common interaction/compiler/domain/observer schema can guide integration | Proposed architecture with one implemented compatibility component |
| Generic stable, constraint-preserving Einstein dynamics plus operational records within48 | Blocked; no accepted model supplied |

The immediate integration target is one exact primitive-to-macro compilation
with a stated kinetic rank, source response and invariant/constraint relation,
followed by the same metric/phase/record comparison on its own trace. Existing
counterexamples and already failed physical gates must stay attached to their
exact laws throughout that process.
