# Operational meaning of clock trials, approval and preference

Status updated2026-11-08: operational definitions, historical protocol
rationale and current evidence. This note is not evidence that an autonomous
internal selector exists. It changes no engine, coupling, click classification
or running state. The reviewed baseline is main
`ff89e2ff661c8b60af84aff738f9040ad7f15bcc`.

## Current results and the source-mask correction

- **Write–probe V1 completed:**68records,zero accepted gates. Counter-only
  removal of an absent writer left a remainder footprint that invalidated all16
  probe-only comparison inputs. The failed family is preserved in the
  [V1 audit](evidence/independent_audit/write_probe_v1_verified.json).
- **Write–probe V2 completed:**260records,4accepted clock-on gates among32
  phase/gap/size groups, with complete inverses independently checked. V2
  restores an absent packet's entire declared24-address initial footprint to
  pristine guide/background. It changes that control preparation explicitly;
  it does not relabel the V1 result. See the [V2 protocol](protocol_v2.json)
  and [audit](evidence/independent_audit/write_probe_v2.json).
- **Local-region mediation completed:**16new initial preparations,4accepted
  groups. Output carrier and C signature follow the interaction-written
  336-triple region across two exterior histories, with exact native suffix
  controls. The diagnostic swaps are initial preparation changes, not runtime
  board operations: [audit](evidence/independent_audit/clock_region_mediation.json).
- **Recurrence studies completed:**the20-run study and8-run long extension
  distinguish genuine continuous returns, lost identity and complete-board
  cycles. L48/52 joint preparations supply no later registered exact output
  after the first return through32scheduled opportunities. No autonomous
  preferred-route search was established: [initial audit](evidence/independent_audit/recurrence_v1.json),
  [long audit](evidence/independent_audit/recurrence_long_v1.json).
- **Two-clock formation study completed:**48runs demonstrate cooperative
  middle-counter activation in the equal-phase distance2 preparation, but zero
  of12geometries satisfy the frozen recurrent isolated-composite criterion:
  [results](structure_formation_results.md).
- **Baseline wave families completed:**the [16-run coherent-wave audit](evidence/independent_audit/coherent_wave_v1_summary.json)
  confirms the fixed finite-time scalar-wave comparison, and the
  [20-run internal-mode audit](evidence/independent_audit/internal_gap_v1.json)
  confirms the registered global internal oscillation family. Neither creates
  a localized particle or solves click selection. The coherent-wave producer
  exceeded its300CPU-second cap, using328.94seconds; that resource failure is
  retained separately from the verified scientific comparisons.
- **Composition and activation completed:**[OR/NO-to-clock64](route_clock_results.md)
  has eligible inputs but zero of24 quiet phase-memory successes and zero of4
  resting-apparatus retention successes. [Direct packet activation36](evidence/independent_audit/activation_v1.json)
  has zero of18 accepted on/off pairs across nine remainder preparations and
  two sizes. These audited finite negatives distinguish a first arithmetic
  activation from a persistent localized clock.
- **Conditional carrier-to-clock composition completed:**the
  [32-run result](carrier_memory_results.md) and
  [independent audit](evidence/independent_audit/carrier_memory_v1.json)
  establish zero of8 strong terminal records. At receiver phase0 on both sizes,
  a clean writer sets phase2 and a later clean conditional carrier restores
  phase0. This weak write/cancel primitive distinguishes11 from writer-only10,
  but the entire336-triple terminal region equals00 and01 throughout96..112.
  All32 terminal receivers are quiet. The native phase-0 center pauses at
  updates74/75 and restarts at76 via C2 then C1; it does not wait for a separate
  approval action. Both clocks were already active, and no unique detector
  record or autonomous selection was demonstrated.

**The demonstrated clock already rotates before the signal arrives.** The
writer changes its phase; it does not start that clock from rest. The accepted
V2 memory hold is states32..40 before the later probe. It is not a claim of
nondestructive reading or indefinite retention after that probe. In particular,
the later common clock state must not be presented as a retained history of
which writer was present.

An explicit passive comparison locates the surviving distinction. In the
audited L337,phase0,gap38,clock-on records, compare source masks01 and11. Their
complete336-triple clock regions differ at state40 but are identical at states61
and88. At each of those later states,48 triples outside the region still differ:
16 have different counter pairs and32 differ only in remainder. At88 their X
coordinates span135..241. These counts describe differences between two native
captures, not an entropy or bit count. They show why loss of this local phase
record is compatible with full-state reversibility:the distinguishing state
persists outside the clock region. This does not establish a detector's unique
permanent record or quantum collapse.
The [complete comparison receipt](evidence/phase_record_information_location.json)
retains every differing address and both triples, the336-address region and
input record hashes. A [separate independent readback](evidence/independent_audit/phase_record_information_location.json)
verifies all counts and values without executing new dynamics.

Passive inspection of the128 existing V2 clock-counter-off records found zero
unit-clock holds in the original32..40 window:every center's counters are zero
throughout that interval. A separately labeled discovery inspection of64..88
also found no constant nonzero center norm in any of those records. Those
later-window counts are not a preregistered new acceptance test or a universal
impossibility result. V2 disables its generic candidate-hold scan, so its empty
`candidate_holds` arrays must not be cited as an exhaustive search. No audited
result cited here establishes an incoming carrier creating a localized recurrent
clock from rest. That remains a separate preparation/formation target.

For reproduction of that limited passive count, use
`evidence/write_probe_v2/result.json` with SHA-256
`ff031781bb99f2b096f3af135a5b83d3925d1b5b2f622f200120aaae5963483d`.
Select cases with `stage != "pristine"` and `clock_present == false`:
32records for each source mask00/01/10/11. In each recorded observation,
`center_trace[32:41]` has a=b=0. For the later discovery count, the set
`{a*a+b*b for a,b,r in center_trace[64:89]}` is never a singleton containing
a positive integer. This checks only the declared center and windows; it is
not a search for arbitrary clocks elsewhere or for every possible period.

The counter-ablation convention below remains a separately defined mathematical
truth-table intervention and is still used where expressly registered. It is
**superseded for the V2 valid-packet comparison** by complete input-footprint
removal. Clock-counter-off controls retain their separate declared convention.
These interventions must never be mixed silently. The later synthesis links
[earlier selection failures and current follow-ups](physics_synthesis.md).

## Original discriminating question, now answered in a finite family

Can an earlier transported writer change a local clock so that an otherwise
identical later probe produces a different complete outgoing carrier?

Before V1/V2, the phase protocol recorded a signal-written relative phase; its D/X
calculation is a passive observation across two sites. It is not an internal
comparator. The existing transmission protocol demonstrates a controller prepared
before the run. Joining them must establish that the controller's relevant state
was actually written by an interaction. The existing pause bridge supplies its
restart from prepared trains and did not settle this question. V2 and the
mediation study now supply the finite answer stated above; the original design
rationale follows so its controls and limits remain reviewable.

## Fix these meanings before validation

| Term | Operational requirement |
| --- | --- |
| Clock | A declared complete counter/remainder region with a measured phase or other state; apparent dial rotation alone is insufficient. |
| Trial | A complete carrier crosses the registered incoming port and subsequently encounters the declared controller. An arbitrary board step or C event does not count as a new attempt. |
| Finds | The trial satisfies a preregistered downstream full-state output predicate. Discovery may propose the predicate; separate validation must freeze it first. |
| Approval | A state-dependent signal is produced by the interaction and physically reaches a downstream apparatus, changing its registered state. Computing a Boolean label in analysis is not approval. |
| Click type | The unchanged guarded arithmetic class at a fixed address and registered response window, retained alongside all other classes and events. |
| Preferred path | Competing, independently functional alternatives are present together; exactly one registered outlet succeeds, and the outcome follows a separately defined candidate property under reversal controls. |

For each channel, retain the exact native event definition: recover
`ell = b_next + a`; require `ell != 0` and a changed full triple; then
`kind = ((r_next-r)//2) mod 3`. A remainder change alone is not a click. A C2
label is not automatically selection, and rejected classes may not be hidden.
Raw events are mathematical readouts until a physical detector interpretation is
derived independently.

## Historical first-experiment design: write, retain, probe

The search protocol must specify geometry, tensor, all initial remainders,
incoming/outgoing templates, complete regions, horizon and response windows.
The V1 discovery scout may keep the clock present in all four writer/probe
masks; the clock-absent counterparts below are reserved for separately frozen
confirmation of a hit before attributing the effect to clock counters. A quiet
pre-probe region alone does not prove that region mediates the response: the
writer's complete wake remains part of the causal apparatus.
The original V1 recommendation was a factorial set of writer/probe/clock
counter masks with every initial remainder retained within that family. Its
failed packet-input validity led to the separately frozen V2 correction above.
The logical control roles remain:

- writer absent, probe present, clock present;
- writer present, probe present, clock present;
- writer present, probe absent, clock present;
- writer absent, probe absent, clock present;
- clock-absent counterparts for the active source combinations.

The probe preparation and incoming full carrier must agree between the first
two runs up to its encounter with the controller. Verify that the writer arrives
and changes the declared controller region, and that the changed state survives
a registered interval before probing. Preserve the whole earlier writer output:
a later match at the probe outlet must be distinguished by space-time windows
and source controls from an earlier packet merely passing through.

That paragraph states the original design target. The completed V2 operational
contract uses full early incoming templates and a later near-input template
that explicitly excludes the seven clock-region nodes. Its pass must not be
described as equality of every possible later causal input. The separate
crossed-region mediation study supplies the stronger, finite local-state
comparison across its two declared exterior histories.

An accepted result requires a difference at the registered complete outgoing
carrier or downstream receiver, with unchanged later probe input. Record local
inputs, every raw C, retained record and complete-board inverse. Test more than
one probe separation and an unseen board size before promoting a reusable block.
No long run, end-time scan or favorable output window can retroactively replace
the frozen response criterion.

The accepted V2 groups establish **interaction-written conditional transmission**
within their registered finite domains.
If a downstream receiver also responds with the frozen event/record predicate,
it establishes that narrower acknowledgment interface. It does not establish
two-path preference or internally generated alternatives.

## Repeated trials and stopping

A prepared finite train can perform repeated probing without outside
intervention. Call it finite autonomous probing and declare the number of
individually valid arrivals. It is not an indefinitely renewable source or an
evolutionary process merely because it is long.

A "tries until success" claim additionally requires several registered trials,
earlier failures, a success dependent on the evolving internal state, and a
measured change in subsequent behavior. If later packets still propagate after
the selected click, retain them. Do not stop the engine or discard later clicks
to manufacture a stopping mechanism. Feedback must itself travel through Rule3
states. Full-state reversibility requires information outside the retained local
record, even if an observed output disappears.

## A limited cooperation proxy

For a preregistered binary success predicate Y and n independently addressable
candidate source groups, run every initial counter-ablation mask S while keeping
the complete common remainder field fixed. When `Y(full)=1`, define

`K = min{|S| : Y(S)=1}`.

Report the complete truth table and every minimal sufficient set, not just K.
If `Y(empty)=1`, K is zero and success needs no candidate source in that family.
If `Y(full)=0`, K is undefined for the full candidate. Restrict the first study
to n <= 3 so that all masks can be checked. K measures **minimum sufficient
source cooperation for this fixed output**, not entropy, algorithmic complexity,
periodicity, biological fitness, physical energy or a universal ranking of
histories. Its mask experiments are independent preparations, never runtime
ablations. The board never receives K as an instruction.

The V1 absent-writer remainder footprint illustrates why mask validity matters.
Counter ablation can leave an apparatus that damages an otherwise supplied
probe. Such a truth table still describes that frozen mathematical preparation,
but cannot rank cooperation among independently functional packet inputs.
Report input eligibility for every mask. A later complete-input-footprint
removal convention is a different preregistered intervention family; it must
not be substituted silently for the counter-ablation definition above.

Multi-source dependence alone is vulnerable to dose and timing explanations.
Retain initial `sum(|a|+|b|)`, packet count, path lengths, arrival times and actual
six-term input histories. Add separately registered controls with equal packet
count and counter budget but disrupted relative phase or disconnected delivery.
Validate every such preparation as a genuine carrier; an invalid amplified
packet is not an amplitude control. The counter budget is not physical energy.
Identical complete channel input histories and initial triples necessarily give
identical scalar trajectories, regardless of which description calls them more
cooperative.

K can be reported for a demonstrated component without a preference claim. A
preference study needs two independently functional alternatives, a single
simultaneous-input outcome, and property-reversal controls: change which
alternative has the larger premeasured K while holding designated nuisance
variables fixed, then test whether the winning outlet reverses. Also swap path
labels/placements through actually valid preparations. A persistent fixed-port,
phase, intensity or earliest-arrival bias does not establish K preference. If
the controls cannot be constructed, the claim remains relational discrimination.

## Historical recurrence proposal, now completed

The following was the proposal for the subsequently completed20-run study.
Its original predictions are retained here; the current outcomes and the
separate long extension are linked at the top of this note.
Use one initial packet at `x=c-16`, a p2/r0 controller, and the existing periodic
X guide. Suggested discovery sizes are L48 and L50, followed by unseen L52 and
L54, with `H=2L+40`. Four packet/clock counter masks per size retain the full
common remainder field. A separate pristine guide-carrier preparation at each
size supplies a positive transport control; its different complete guide is
not silently substituted for a matched clock-absent control. Total: 20 runs.

For a pristine carrier, incoming template windows recur at `4..7+nL` and the
forward outlet at `24..27+nL`, for n=0,1,2. Each purported return must independently
pass its complete incoming template. A missing or damaged return cannot count
as a controller rejecting a valid trial. Record all other disturbances and raw
C events; no copies, injections, resets, rewinds or filtered wake are allowed.

Conditionally, if the first encounter writes global clock phase zero and the
complete interface is restored before the return, the next relative encounter
phase is `L mod 4`. The existing isolated-encounter comparison motivates
suppression for residue zero and transmission for residue two. The first pair
of sizes explores this prediction and the second pair can validate it. Actual
wake recirculation may invalidate either assumption. The result is explicitly
boundary-dependent and supplies no nonperiodic or physical-space claim.

Even a successful recurrence test establishes only repeated genuine encounters
and state-dependent persistence. The first p2 encounter already transmits; this
does not constitute unsuccessful trials followed by a discovered solution. A
p0 preparation may destroy the first valid carrier and leave no further trial.
Preferred routing, a distinct terminal success, a restartable source and
internally generated alternatives remain separate targets. Suggested budget:
at most 20 runs and 600 CPU seconds, plus preregistered storage/state caps and
complete-group stopping; independent replay time must be reserved separately.

## Attraction, binding, repulsion and dissociation

The earlier `research/building_blocks/structure_protocol_v2.json` tested 128
isolated/adjacent clock preparations and reported 72 radius-one recurrent
clusters in `structure_results_v2.json`. Its all-state return periods range
from three to seven. It explicitly excludes physical binding, source-created
attachment and motion. Those finite results must not be promoted merely by
renaming an adjacent pair a molecule.

Separate these two levels in every new pair result:

| Level | Required evidence | Permitted interpretation |
| --- | --- | --- |
| State coupling | Complete joint-region trajectories differ from matched singleton controls, with the same fixed tensor and full shared remainder preparation. | Causal interaction of prepared clock states. |
| Interacting localized recurrence | A preregistered complete region repeats while support stays within the fixed bound; the interaction condition also passes. | Prepared recurrent composite, not an attractive force. |
| Signal-created reconfiguration | A transported signal changes the pair into a different registered local state/recurrence; the matched source-off preparation does not. | Interaction-induced structure change, with the complete wake retained. |
| Motion-based attraction or repulsion | Identifiable full-template objects change their relative displacement or velocity compared with free singleton trajectories, under registered incoming/outgoing windows. | A finite effective kinematic interaction in that object family. |
| Attachment and dissociation | Initially identifiable separated objects approach and remain as an interacting bounded composite; or a composite produces identifiable separating products under a registered perturbing signal. | Finite attachment or breakup, separately from a physical force law. |

An intensity centroid can move when amplitudes change between fixed sites.
Neither this centroid nor `a*a+b*b` has been established as a particle position
or physical energy. Use a preregistered full-state template/phase atlas to track
an object; report ambiguous matches or a lost template as lost identity. During
an overlap, identities may be unavailable, so compare independently valid
pre- and post-interaction objects rather than inventing continuous trajectories.

A stationary cluster losing its recurrence is disruption, not evidence that
two bodies repel. Two preloaded fixed clocks remaining adjacent is not evidence
that they attract. Source-induced local capture is compatible with reversibility
only while the full board retains distinctions outside the retained region;
local convergence is not deletion. No new force, coupling update, template
correction or hidden position variable may drive the board.

For the current short pair study, state coupling and signal-induced
reconfiguration are realistic first targets. A claimed force requires the
additional motion measurements above. A positive coupling result can become a
candidate internal resource for later approval/route studies, but it does not
establish a preference for higher cooperation or complexity by itself.

## The skin-clock and three-class hypothesis

Treat the proposed division into two spontaneous click types and a third
selection-associated type as a hypothesis. Do not implement that division as a
new event classifier or as behavior in the engine. Test all three candidate
assignments under the existing guard and report every registered comparison.

For a valid channel, `u=0` gives `ell=0` and therefore no native C event. This
does not forbid an autonomous cluster from producing events: its neighbors
inside the cluster can provide nonzero inputs with no new arriving external
source. "Source absent", "no external term entering the declared body region"
and "zero input to this channel" are three different predicates. Cancellation
of nonzero external terms also differs from no individual external input.

The exact identity `r_next-r=2*u-6*ell` gives `kind=u mod 3` whenever the native
event guard passes. It does not assign a physical interaction or selection
role to any class. In particular, C0 can occur without a remainder change;
its guarded counter transition still matters. Quiet rotation with zero
quotients is not a raw click.

Declare core, halo/skin and exterior addresses before inspecting event counts.
For moving bodies, register the complete identity/tracking rule first and mark
lost identity instead of redefining the surface around favorable activity.
Register coincidence directions and lag windows; retain the full count table,
all three classes, source-off controls and exact six-term inputs. Periodic
coincidence can be a kinematic consequence of a common oscillator rather than
evidence of information being accepted.

A proposed selection association must additionally predict actual full-state
outgoing carriers or retained records under valid-input counterfactuals. The C
label is a passive marker of the very Rule3 transition being measured, not a
second causal operation. One cannot remove or invoke the label during a run to
test its effect. Instead vary complete initial preparations and follow the
resulting internal state changes and outputs. Neither coincidence nor a single
record derives quantum collapse, a preferred route, or an arrow of time.

## Effective ratios are measured component laws, not new Rule3 parameters

The primitive remains `ell,r_next=divmod(2*u+r,6)` with the existing fixed
couplings. Each channel retains a state; it does not select a new numerator or
denominator. Its exact balance over T updates is

`6*sum(ell) = 2*sum(u) + r_0 - r_T`.

Because remainder parity is fixed and valid remainders are in 0..5,
`abs(sum(ell)-sum(u)/3) <= 2/3`. For nonzero accumulated signed input, the ratio
error is at most `2/(3*abs(sum(u)))`. Approaching 1/3 requires growing absolute
accumulated signed input, not merely a long run: alternating inputs can sum to
zero forever. Raw event counts are not the signed sum of quotients. A claimed
new scalar gain must not overlook this exact existing constraint.

A different, emergent ratio must name different operational quantities. For
example, preregister counts of complete carrier crossings at fixed input and
output ports, or accumulated cycles of identifiable internal clock states. A
four-frame template match is one declared crossing, not four particles. Clock
phase alone is modulo its period; accumulated cycles are initially a passive
analysis observable unless an internal counter/record has also been realized.

To test a candidate component ratio `rho=p/q`, freeze a relation such as
`abs(N_out(t)-rho*N_in(t-tau)) <= B` after a declared transient, where the
crossing rule, latency tau, residual bound B, state family and time interval
are all specified before validation. Output-only background events need a
separate source-off measurement and an explicit fixed treatment; do not erase
them. One finite rational count ratio or fitted frequency provides no evidence
that the same law predicts another input.

| Variation | What must stay fixed or be checked |
| --- | --- |
| Initial clock phase and retained state | Test every phase in the declared family; a state-dependent law must identify its state variable before validation. |
| Input spacing and phase | Compare multiple spacings, irregular but initially prepared finite sequences, and separated repeated encounters; distinguish resonance, latency and a true count law. |
| Amplitude and polarity | Validate every complete incoming variant under Rule3 first; scaling a seed does not guarantee that it remains the same carrier. |
| Input duration and number | Test several lengths and independent longer holdouts, retaining no-output and saturation cases. |
| Environment and composition | Join compatible components, preserve complete halos, and compare source masks using their explicitly registered full-preparation convention. |
| Geometry and boundaries | Use new sizes and directions; isolate intentional periodic returns from claims about unrestricted propagation. |

Use one training family to propose p/q and a disjoint validation family to
test it. Compare alternatives such as a fixed delay, a one-time phase write,
phase-dependent filtering, finite storage saturation and a periodic echo.
Report the entire registered family and error curve; do not select a new ratio
for each outcome. If the internal state changes during a run, an effective
state-dependent response is possible, but its state and transition laws must
also be measured or derived rather than supplied by an observer.

These requirements apply equally to proposed "non-light" components. Different
ratios or division/remainder patterns do not identify gravity, charge,
electromagnetism, strong/weak interactions or electronic binding. Those names
require the separately specified record families in `physics_targets/`.

## Claim ladder and budget decision

1. Prepared state controls a later carrier: existing baseline.
2. An incoming writer controls a later carrier: first new target.
3. That carrier writes a downstream acknowledgment and affects later trials.
4. Two competing alternatives yield one registered output under reversal controls.
5. The winner tracks a frozen cooperation measure beyond nuisance controls.
6. The board generates and retains new alternatives through an internal feedback
   process: a distinct stronger target, not supplied by the earlier stages.

Complete and independently review each stage before using its name in the next.
Within the three-hour research budget, reserve time for independent replay and
generic Presenter packaging. Exhaustion or a failed finite family is a recorded
limit; it is neither universal impossibility nor permission to alter Rule3.
