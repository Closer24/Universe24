# A bounded internal proposal–approval–cancellation protocol

Research base: `0d4c4805be67b0efc42e084416ff2204529a1e07`.
Date: 7 November 2026. Status: prospective component contracts and conditional
algebra, **not an implemented autonomous route-confirmation mechanism**.

## 1. The question and the representation

Can two simultaneously represented route candidates cause an ordinary local
signal to approve exactly one persistent record, while a different ordinary
signal cancels the other pending record, using only the present Rule3 board?

For a fixed tensor and initial state the board has one deterministic trajectory.
Here “possibilities” means a finite, declared collection of physical candidate
patterns inside that trajectory. It does not mean that every mathematical
future is already being simulated. A separate source-control run is a comparison
by the researcher, not a second possibility evaluated by the original board.

The first candidate family has exactly two spatial arms, A and B. Identity is
the initial arm region, its channel addresses, and its return-memory location.
Each arm must carry its own ordinary counter/remainder disturbance. Names in a
manifest are passive labels: no packet object, route-ID dispatcher, or callback
exists during evolution. All signals, comparisons, return messages and records
must be identified in actual full-board states.

The current body-013 model admits eight global sign triples. Every component
in a particular board must use the **same complete tensor**, chosen before
evolution. There is no independent tensor choice per component, node or channel.
A preparation-only converter changes initial triples, not local coupling.
This note adds no engine primitive or tensor family.

## 2. Existing evidence and the missing connection

| Ingredient | Current status and source |
| --- | --- |
| Guided compact transported disturbance | Exact complete-state translation on the specified periodic guide; [proof and domain](../../docs/CONFIRMATION_BLOCK.md#complete-state-translation-proof), [independent review](../component_review/packet_proof_review.md). |
| Spatial route competition | Prepared OR/NO competition has finite source-phase, length and horizon evidence; [study](../../docs/PATH_SELECTION_BLOCK.md). Its transmitted output has multiple C events. |
| Quiet write–wait–confirm arithmetic | Exact only conditional on specified actual incoming sums; [existing calculation](../light_approval/approval_mechanism.md#exact-local-calculation). |
| Autonomous packet-to-pending conversion | Research target. The known translating packet has opposite lobes; its quiet passage through an unmodified site does not leave permanent remainder memory. |
| Internal unique approval and cancellation | Research target. An independently preloaded second source would establish two-arrival response, not a route-computed acknowledgment. |
| Preference for maximum complexity | Not established. The registered `C_pair` prediction had ten eligible comparisons and ten counterexamples; [evidence](../../docs/PATH_SELECTION_BLOCK.md#results). |

The immediate bottleneck is a complete-board input converter, followed by
retention in the presence of backreaction. A scalar threshold identity is useful
for designing this search but is not an autonomous gate specification proved to
work in this lattice.

## 3. Exact local state vocabulary

For one channel let `F((a,b,r),u)=(b,ell-a,r_next)`, where
`(ell,r_next)=divmod(2*u+r,6)`. The arithmetic observer records C only when
`ell != 0` and the full triple changes. Its class is `u mod 3`; that class is
not a selection instruction. Define `I_g=a_g^2+b_g^2` only as a counter
magnitude, with no physical-energy interpretation.

The following positive-orientation interface uses channels 0 and 14 with
zero initial counters. The negative-orientation version exchanges the two
channels and reverses the input signs. Every listed input must be produced by
the six actual spatial inputs in a composed board.

| Readout or transition | Required local state or actual incoming pair |
| --- | --- |
| Ready | Zero counters; `(r0,r14)=(2,4)` |
| Write pending | Input `(1,-1)` produces zero counters and `(4,2)`, with no C |
| Pending | Zero counters; `(r0,r14)=(4,2)` |
| Wait | Repeated input `(0,0)` retains this exact pending state |
| Approve pending | A second input `(1,-1)` produces channel 0 `(0,1,0)` and channel 14 `(0,0,0)`; one channel-0 C |
| Approved readout | `(r0,r14)=(0,0)`, `I0=1`, `I14=0`; quiet-input rotation may continue |
| Cancel pending | Input `(-1,1)` restores zero counters and `(2,4)`, with no C |

“Canceled” and “never requested” are therefore indistinguishable at these two
channels alone. If a distinct cancellation record is required, it must have
physical storage. One conditional target adds an ordinary third channel `g`,
distinct from 0 and 14, initially `(0,0,2)`. At cancellation the actual input
vector `(-1,1,1)` on `(0,14,g)` yields remainders `(2,4,4)` and zero counters,
with no C. Ready has witness remainder 2; canceled has witness remainder 4.
The witness must also retain its record against later inputs. This is an exact
input contract, not proof that the present coupling generates this vector or
that an arbitrary third channel composes with the paired guide.

For a strict whole-node test, all other receiver channels must remain in their
registered null states during pending, and every C on all 48 channels must be
counted. Approved retention must include the witness and all registered record
clauses. Merely observing `(r0,r14)=(0,0)` is insufficient: the previous failed
source preparation reached that pair with `I0=0,I14=1`, the wrong record.

### Cancellation after an approved record is a different transition

Immediately after the intended approval, applying `(-1,1)` gives channel 0
`(1,-1,4)` and channel 14 `(0,0,2)`. Channel 0 has `I0=2` and a new C.
It does not quietly return to pending or ready. Later phases require their own
calculation. A cancellation after an accepted click must be represented as a
new retraction/correction record if supported, while the earlier event remains
in the complete trace. It cannot retroactively remove that event.

Likewise, an immediate duplicate approval `(1,-1)` gives `(1,0,2)` and
`(0,-1,4)`: the second channel clicks and the approved predicate fails.
Duplicate handling is not already idempotent. The first protocol is therefore
one-shot: no reset, retransmission, stale acknowledgment or automatic retry is
assumed. Arrival of an undeclared extra message is a failed case, not an event
to filter out. Repeated use would require a separately realized state machine
and explicit retained history. Fresh spatial memory slots can identify finitely
many epochs, but they must be present initially and their routing must also
arise from Rule3.

These entries were checked by direct exact substitution (12 scalar assertions).
They hold conditional on the inputs; full-board source and receiver traces are
the required next evidence.

## 4. Two concrete converter targets

### A. Release a transverse packet disturbance

The exact guided packet has transverse channels whose incoming pulse is
`q=+1` or `q=-1` and whose carefully prepared remainders keep their quotient
zero. A stationary remainder-only defect at such a channel can release a
counter signal at its first arrival:

| Initial quiet channel | Actual input | New triple | Quotient |
| --- | --- | --- | --- |
| `(0,0,4)` | `+1` | `(0,1,0)` | `+1` |
| `(0,0,0)` | `-1` | `(0,-1,4)` | `-1` |

For the packet study geometry, inspect one transverse neighbor of row sites
45, 46 or 47, using the actual `tensor.ports[direction][source_channel]` and
`tensor.weights[direction][source_channel]`. Enumerate its initial remainder
and the companion channel's remainder in `{0,2,4}`. Also inspect two or three
on-row remainder-pair defects immediately before the receiver. These are finite
initial-patch searches. All source-off preparations remain stationary because
their counters are zero. The actual first incoming sign and all later feedback
must be measured, not supplied by this table.

A useful discovery would separate the leading write contribution from the
opposite trailing contribution, retain the latter elsewhere, or emit a bounded
side signal. No absorber may erase the trailing contribution from the full
state. A defect that merely creates a long pulse train does not pass the pending
contract. Modifying the halo also invalidates use of the unmodified translation
proof at the interaction site.

### B. A first-update coincidence target

A quiet channel at remainder 2 has the following exact response to two unit
contributions arriving from two ordinary spatial ports:

| Combined actual input | New triple | C at this update |
| --- | --- | --- |
| `0` | `(0,0,2)` | No |
| `1` | `(0,0,4)` | No |
| `2` | `(0,1,0)` | Yes |

The negative dual has `u=-1 -> (0,0,0)` without C and
`u=-2 -> (0,-1,4)` with C. Thus simultaneous contributions can cross a quotient
threshold even when either contribution alone does not. This supplies a small
collision/conversion target. It proves neither a durable AND gate nor exclusivity:
successive single arrivals can also accumulate remainder, and outgoing counters
feed the rest of the board. Search complete prepared branch/collision geometries
and keep the null, each-single-source and joint controls. Agreement at the first
update alone is not acceptance.

### C. Search initial preparations by the exact inverse

Using the inverse externally to search for an initial preparation is allowed;
using it as a stage of the advertised forward evolution is not. For a desired
terminal state T, `F^n(F^(-n)(T))=T` follows from reversibility. Endpoint recovery
alone therefore establishes no new detector mechanism. The nontrivial search
question is whether the preimage belongs to a useful, independently specified
initial-source family and produces the entire required forward behavior.

Before computing preimages, freeze the terminal family, rewind count, initial
source box, separation bound, receiver-ready state and all forward predicates.
For the current candidate, require the complete initial 48-channel receiver to
have zero counters, pair `(4,2)`, and all other remainders 2. Every nonzero
initial `a` **or** `b` must lie in the predeclared source box and be at least
eight toroidal Manhattan steps from the receiver. Reject out-of-box activity;
do not expand the box after inspecting a preimage. Keep every initial remainder,
including distant and transverse ones, as an explicit part of the apparatus.

Construct the source-off control from that same reconstructed initial state
by zeroing only source-box counters, preserving all remainders and the rest of
the apparatus. Independently reversing a different source-off terminal state
would change the apparatus and is not the matched control. Require the same
whole-node quiet write/retention predicates throughout the forward window,
not only the chosen endpoint. Exact forward/inverse replay audits the run;
fresh forward preparations and geometry/perturbation controls are needed before
promoting an inverse-engineered instance to a reusable component. Acceptance
would establish a prepared pending-write example, not route selection or
internally computed approval.

Periodicity must also be bounded prospectively. For receiver `(48,64,64)` and
a forward horizon 40, its unwrapped dependency cone lies inside X8..88 and
Y/Z24..104. This bounds boundary dependence of that receiver readout if the
initial cone is preserved. It does not prove that no activity anywhere on the
complete board crossed a periodic boundary.

## 5. A minimum two-route experiment

The following is a dependency-ordered experimental target, to be frozen as a
separate protocol once the relevant initial patches exist. It is not a claim
that the current library already implements each role.

1. **Input interface.** Run the separately registered 18-case compact-packet
   interface study: L129, H24, source at X32..35, receiver X48, Y=Z=64,
   all nine even receiver-remainder pairs with source on/off. Freeze the target
   write and eight-update pending retention before evaluation. Failures identify
   whether the first write, silence, or subsequent retention fails.
2. **Two-arrival latch.** For any new converter candidate, freeze a new study
   before validation. Prepare two finite source packets at time zero. Compare
   null, first-only, second-only and both-source runs with identical apparatus
   remainders. Require a four-update quiet pending interval, one receiver-node
   C-bearing update in a predeclared second-arrival window, and eight subsequent
   updates of the full approved predicate with no further receiver-node C.
   Reject a single-source premature record through the entire horizon. This
   tests a latch, not internal route approval.
3. **Internal source of the return message.** Replace the independent second
   source by a declared decision region reached by A and B. Its outgoing signal
   must change when the competitor input changes, with all initially prepared
   output-source counters held fixed. No runtime replacement is allowed.
   Record the complete causal path from incoming routes through interaction to
   return disturbance. Initially use a fixed finite predicate, not complexity.
4. **Unique route record.** Require both isolated arms to be functional. In the
   joint case require exactly one approved route, the other route pending or
   explicitly canceled according to a frozen contract, no premature winner,
   and the full retention interval. Swap spatial arms and repeat. A quiet outlet
   alone is not evidence of a cancellation message; locate an actual incoming
   disturbance and an internal witness or demonstrate its effect by matched
   controls. Report first passage, every later C, actual sums and all six terms.

A prospective comparator uses the following deliberately modest truth table.
A is one fixed spatial input port of the prepared comparator; the label itself
does not change its evolution.

| Valid candidate data `(A,B)` | Required final record |
| --- | --- |
| `(0,0)` | No approval |
| `(1,0)` | A approved only |
| `(0,1)` | B approved only |
| `(1,1)` | A approved; B canceled with its witness retained |

This fixed-port priority is a construction target, not a Python branch allowed
during evolution and not a law favoring complexity. Swapping input data alone
keeps the priority port fixed; rotating the whole prepared apparatus rotates
that port and its expected output. Both are separate controls. Before claiming
a comparator, all four cases must be represented by initial candidate data on
the same apparatus.
An invalid/absent candidate needs either an internally transmitted completion
state or a proved deadline mechanism; its absence cannot simply be announced
by the experiment runner.

For an eventual complexity comparison, define a bounded measure on a finite
represented candidate object, specify how the board itself encodes and compares
the values, and test against equal-length/arrival controls. A score computed by
the observer remains diagnostic. It cannot choose the returning approval signal.
The failed `C_pair` prediction is retained as evidence; changing the measure
starts a new prospectively specified hypothesis.

## 6. Causal completion and the deadline obligation

Let candidate i supply a required new terminal datum at location `c_i` and board
time `tau_i`. Assume that datum is not already duplicated or inferable from
registered information at the decision location: matched inputs must permit
different candidate values while agreeing on the earlier decision past. Let
one decision location `d` emit the return message at `tau_D`, and let the final
record be at `m`. With toroidal Manhattan distance `dist`, locality gives the
necessary bounds for this message-dependent architecture

```text
tau_D >= max_i [tau_i + dist(c_i,d)]
tau_click >= tau_D + dist(d,m).
```

These are causal lower bounds. They are not guarantees of transmission or upper
bounds on latency. For a finite decision region, use the actual emission site
and include all internal communication needed to combine the candidate data.
The proof is the radius-one dependency of every full-node update: by induction,
after t updates a node depends only on initial sites within distance t. If one
candidate remains outside that past, two preparations differing only in that
candidate give the same decision state. Therefore a correct decision that may
depend on it cannot yet have been made. If the winner was separately encoded in
the decision apparatus at time zero, this indistinguishability premise fails;
an early matching output would not demonstrate that the apparatus evaluated
the arriving competitors.

If validated route and processing upper bounds are `T_i`, `delta_D`, and
`T_return`, a safe prospective schedule has

```text
decision not before max_i(tau_i + T_i) + delta_D
record window ending by that scheduled decision time + T_return + delta_write.
```

This schedule must be implemented by initial spatial distances, counter phases,
retained completion marks and ordinary signal collisions. A wall-clock timeout,
loop index, observer flag or missing-packet callback cannot trigger the board.
A preloaded deadline packet is a possible timing source only after its complete
input/output interaction has been realized; it certifies absence solely within
the declared finite source family and proved arrival bounds. If a legal source
may send an arbitrarily delayed message, no finite local timeout can establish
that all relevant competitors are finished.

Freeze arrival windows and the sample convention (`old state t` to `new state
t+1`) before a run. Use the entire registered horizon for single-source and null
controls. Keep the toroidal distances explicit; enlarging the cube must preserve
the local preparation and leave possible periodic returns outside the window.
Guide background that wraps around the board is part of the preparation even
when the moving disturbance cannot yet reach the periodic boundary.

## 7. Information retained by cancellation and a visible winner

Let M distinct complete initial alternatives have the same eventual visible
winner record at the same comparison time. Injectivity of the full evolution
requires M distinct compatible full final states. The unobserved degrees of
freedom must distinguish these alternatives; if assigned a finite encoding they
need at least `ceil(log2 M)` bits of distinguishability. This is an information
counting requirement, not a thermodynamic entropy or fixed number of nodes.
Counters are unbounded integers; any storage-resource claim must bound both
the addresses used and the magnitude/precision allowed.

For example, k independent binary candidate data bits admit `2^k` inputs. If
the visible output only names one of k routes or “none,” at least one output
class contains `ceil(2^k/(k+1))` distinguishable inputs. Their distinctions must
survive elsewhere. Declaring rejected paths canceled cannot remove them from the
full inverse audit. Local reset is possible with exported information; resetting
the entire apparatus and environment to one common state while forgetting
different inputs is incompatible with invertibility.

This also limits claims about click time. A fixed observer may assign no new
event count during a quiet interval while the board performs many updates.
Such coarse observation does not make full-board time stop, prove an intrinsic
arrow of time, or make approval quantum collapse. Establishing observed light,
entanglement, Born probabilities or a physical temporal order remains a separate
set of tests.

## 8. Generic component interface and composition

The existing [immutable API](../components/spec.py) and
[finalizer](../components/compose.py) implement preparation and ownership checks.
They do not promise that a valid assembly has the desired dynamics. A candidate
role should be documented with the following data, using ordinary `Patch`
metadata plus a research manifest where the current API has no field.

| Field | Required content |
| --- | --- |
| Initial patch | Every explicit `(x,y,z,channel,a,b,r)` assignment; stationary background; source-on/off substitutions; raw ownership |
| Tensor | Model ID, all ports and signs, fingerprint; identical for all placements |
| Ports | Named existing input/output address sets; polarity, channel and spatial orientation; no added links |
| Environment | Required guide, halo, reserved sockets, allowed neighboring initial patterns, excluded interference domain |
| Input family | Complete permitted transported state patterns, phases, amplitudes, arrival separations and source controls |
| Output/readout | Exact triples or predeclared orbit predicates, all-channel C observer, cancellation witness, forbidden early records |
| Latency | Earliest influence and measured/proved latest response; update indexing convention |
| Retention/range | Exact number of quiet updates, finite horizon, cube sizes, route lengths, boundary-return exclusions |
| Evidence | Source commit/hashes, protocol hash, seed if used, complete preparation, recordings, inverse results, pass/fail cases |
| Composition status | Isolated evidence versus joined evidence; precise conditions inherited from each |

The finalizer rejects inconsistent initial assignments, tensor conflicts,
unfilled sockets, aliasing sources and incompatible backgrounds. Identical
shared assignments may be allowed with their owners retained. One may not add
two overlapping packet states as if the nonlinear update were superposition,
or silently overwrite a guide remainder to resolve a conflict. A changed joint
patch must be declared and revalidated. Counterpropagating packet recipes can
also require different guide remainder backgrounds; opposite propagation alone
does not establish that they can occupy the same lane.

The present passive patch readouts support `all_equal` clauses, not an arbitrary
runtime protocol interpreter. Orbit invariants such as `I0=1` belong in the
research observer unless a separate passive schema extension is reviewed.
The Presenter should render the recorded cube, actual clocks/gears and declared
readouts, retaining every event and all channels. Animation cannot provide an
approval that the recorded engine state does not contain.

## 9. Decision rule for this research stage

**Success:** an independently audited, initially prepared full-board mechanism
meets its frozen pending/return/unique-record contract over the declared domain,
including matched controls, swaps and fresh validation cases.

**Failure:** any premature C, incorrect full record, lost retention, duplicate
record, unaccounted input, incompatible initial overlap or missing causal
completion. Keep the earliest divergent full state and six incoming terms.

**Continue:** use a failure to constrain a new bounded initial-patch family and
freeze a new validation protocol. A verified converter is worth retaining even
if a complete comparator fails. Do not rename a weaker plateau as the original
strict success. If the required behavior cannot be constructed in the current
budget, report the exact unresolved interface; the present evidence is not a
global impossibility proof. Structural changes, if later considered, belong to
a separately named model candidate and require an explicit decision.
