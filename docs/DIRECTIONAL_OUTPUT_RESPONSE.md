# Directional computation response and independent output clocks

## Contract gap

The computation field carries direction, but the
[mass-clock-ray-v1 profile](MASS_COMPUTATION_CLOCK_CANDIDATE.md) selects only a
scalar timing response. Its frozen law sums the current local computation input
and fresh emission into `C`, then assigns `W_d = g*C` to every output face `d`.
The six clocks remain independent owners even when their sampled waits match.
This law introduces no change to a carrier's direction or a field ray's heading.
An observed zero deflection in this profile therefore does not test the intended
directional bending mechanism.

This document records an unresolved composition and numerical design alternatives.
It selects no new physical law, adds no runtime option, and does not certify a
completed bending or moving-emitter implementation. Publication of a design is
not implementation or physical acceptance.

## Trace the directional information

| Stage | Existing owner and behavior | Consequence for composition |
| --- | --- | --- |
| Field transport | `fields/rays.py` retains a heading and integer movement accumulators; `core/spatial_engine.py` delivers through the actual adjacent Port | Propagation is directional and causal |
| Local input | Spatial sampling retains six delivered travel channels; the scalar `flux` projection is defined in [spatial couplings](SPATIAL_COUPLINGS.md#inputs-and-ownership) | Direction is available before the clock adapter |
| Clock sample | `fields/output_clock.py:sample_output_clock` sums the ray amounts in all six outgoing groups; `output_delays` repeats the scalar wait six times | The current adapter discards direction for timing, as its declared scalar law requires |
| Output hold | `core/output_holds.py` stages each selected face and freezes its actual release time | The owner can hold six different waits, but does not choose their physical values |
| Carrier route | `fields/disturbances.py` reads the configured transport weights or carried direction | An unchanged cardinal direction still has exactly one eligible lane |
| Ray route | The ray's heading and accumulator choose its next lattice step | Waiting alone does not change its heading |
| Direction update | [Spatial couplings](SPATIAL_COUPLINGS.md) provide configured exchange and quarter-turn operators | These are separate selected laws; the output-clock profile rejects this composition |

For a diagonal ray, its heading, its last travel Port and its next DDA-selected
Port are different concepts. Grouping `plan.rays` by next departure Port does not
reconstruct the incoming channel that priced an old directional delay. A new
adapter must declare which local quantity it reads, including how fresh source
emission contributes. It cannot silently substitute one for another.

The older [directional delay](SPATIAL_FIELDS.md#directional-delay) modes price
departures from an `along` or `against` channel, but also defer the next carrier
cycle until the slowest departure. They cannot be enabled unchanged under the
independent-output, no-input-delay contract. Their
[least-delay router](SPATIAL_FIELDS.md#least-delay-routing) changes the order of
already eligible lanes while preserving their exact ratios. It cannot create a
transverse lane for a one-axis probe or supply a missing steering operator.

## Numerical alternatives requiring an explicit profile decision

The examples below are independent arithmetic examples for design review, not
measured results or proposed defaults. Use Port order `[+X,-X,+Y,-Y,+Z,-Z]`.
Every accepted option still requires bounded integers, causal local inputs,
unchanged fixed Link transit `H`, one owner per stock and no autonomous draw.

| Alternative | Exact example | What it can establish | Decision still required |
| --- | --- | --- | --- |
| Directional clocks only | If a profile selects channel sample `C_d=(0,0,3,0,0,0)` and `g=2`, an `along` map `W_d=g*C_d` gives `(0,0,6,0,0,0)`; an `against` map `W_d=g*C_(d xor 1)` gives `(0,0,0,6,0,0)` | A six-component input can produce different per-face release times | Channel meaning, selection of along/against, emission sampling, bounds and profile identity; neither map bends a cardinal probe |
| Explicit vector exchange | With carried `p=(4,0,0)`, signed travel flux `F=(0,2,0)`, denominator `D=2` and zero remainder, a configured exchange amount `F/D` gives `p'=(4,-1,0)` and local opposite reaction `(0,1,0)` | A supplied operator can create a transverse momentum component while preserving combined component totals | Sign, coefficient, receiving types, actual momentum owner, reaction transport, energy readout and atomic composition with output holds; this is an inserted coupling, not bending derived from clocks |
| Exact integer rotation | One existing positive Y quarter-turn takes `p=(4,0,0)` to `(0,0,-4)` and deposits `(4,0,4)` in the opposite reaction owner | Carrier norm and combined vector components can remain exact | The rotation axis and threshold are part of the law; rotation about a +Y field does not turn this probe toward -Y, so field direction alone is insufficient |
| Coherent propagation with directional timing | A selected phase advance of one step per waiting tick would accumulate two extra steps on a branch delayed by two ticks | Different face delays could produce a phase difference in a future coherent profile | Phase period/encoding, mixing operator, branch inventory, dispersion and detector readout; there is no such selected composition in mass-clock-ray-v1 |

The existing generic exchange operation can be reused for an explicitly selected
exchange profile; its arithmetic must not be copied into the engine. Admission
is more than removing `validate_output_clock` checks: the present profile allows
only plain ray fields and rejects the spatial vector reaction owner required by
exchange/rotation. Guard timing, simultaneous reaction and source debit, held
stock accounting, and reaction departure must be defined and tested together.

The first implementation decision is therefore whether the research target is
directional timing alone, a separately supplied local direction operation, or
bending emerging from a specified coherent propagation operator. The numerical
operator and its invariants belong to the family/profile. A desired attractive
trajectory is an acceptance target, not a formula selected by the scheduler.

## Independent acceptance cases for the selected composition

These are prospective tests. They must not be reported as passing until run
against an identified implementation and compared with expectations fixed first.

1. **Directional survival.** Inject the six-channel sample above and its axis
   permutations/reflections. Check the chosen local sample, six waits and output
   payloads separately. Include a diagonal ray whose incoming and next Ports
   differ, and a fresh-emission control. No sum-only adapter may satisfy a claim
   of direction-dependent response.
2. **Independent timing.** For an `along` example prepared at tick 10 with `H=1`,
   the +Y batch departs at 16 and arrives at 17; a +X batch departs at 10 and
   arrives at 11. An input arriving at 11 is admitted at 11. It cannot retime the
   existing +Y hold. Test all six faces, zero gain and integer overflow before
   any ownership change. These numbers apply only if that example map is chosen.
3. **Steering versus timing.** Preserve a cardinal probe's route under a clocks-
   only control. If a direction law is selected, test its independent vector
   arithmetic before the route and include an external transverse-field control.
   A changed arrival tick or a reordered diagonal route is not by itself bending.
4. **Joint inventory.** Account for all current records, resident fields, held
   output batches, in-flight Links, escaped stock and remainders. A coupled
   reaction must commit with the carrier or fail with all owners unchanged.
   Computation tokens are not automatically physical energy or momentum.
5. **Causality and determinism.** No receiving response before field arrival;
   departure-to-arrival always equals `H`; no same-tick multi-Link cascade;
   zero draws without an actual Detector; repeated runs preserve the same trace.
6. **Model measurement.** Only after the local cases pass, repeat paired probes
   around a source with reflected/rotated geometries, zero coupling, varied
   strength and varied distance. Keep original failed expectations. Every world
   run saves the existing HTML visualization and structured event trace.

## Delayed moving emitters and self-exclusion

The supported legacy one-Link exclusion reconstructs a departure-cycle emission
from bounded carried bookkeeping. In
`fields/spatial_coupling.py:_without_own_rays` it subtracts that reconstructed
amount on the assumption that field and emitter co-arrive. Absorption instead
matches a complete reconstructed ray key in
`fields/spatial_plan.py:_own_departed_keys`. Neither operation obtains a general
proof of provenance for independently delayed output batches.

Any proposed extension permitting a carrier and its own field to leave for the
same adjacent Node at ticks 0 and 2, respectively, with `H=1`, has a minimal
counterexample to that assumption. At tick 1 the carrier has arrived but its own
field has not; subtracting the old emission would remove absent stock and could
erase an unrelated incoming field. Reversing the holds delivers the field first.
This is a prospective unsupported-composition example, not a failing run of the
stationary-source profile. Current same-face batches prepared together use the
same sampled wait, and the moving-emitter admission guard remains necessary.
If a future profile proves same-face co-release for a restricted case, it still
needs independent tests for turn/split paths, later field delays and return.

The existing `output_clock` rejection of moving emitters and `self_exclusion`
must remain until a new bounded attribution/coarrival contract is closed. Do not
disable exclusion, skip all response, erase an entire incoming Port, read a
global source registry or add an unbounded source history to obtain a pass.
The stationary held-source sampling rule remains its separately named profile.

Required follow-up belongs jointly to field development and architecture:

- Specify when a moving source funds/emits, freezes a direction, departs and
  updates its departure metadata while its material output is held.
- Identify exactly which currently present local ray contribution is removable,
  including fields arriving before, with and after the emitter. Define the
  fixed metadata, owner, lifetime and supported path scope that prove this.
- Test isolated rest, speed `1/1000` and maximum-speed straight motion, a turn,
  reflected axes and periodic return; retain an external-source control on the
  same Port so attribution cannot remove legitimate response. Separate the
  legacy one-Link guarantee from any newly claimed wider exclusion.
- Inject late input, duplicate observations, pending completion and bound/capacity
  errors. Verify no replayed emission, double subtraction, lost reserve or
  expanded local history. Preserve current rejection tests until replacement
  acceptance is complete.

## Ownership of the unresolved work

| Owner | Concrete deliverable |
| --- | --- |
| Physics/mathematics | Select and state the local directional operator, exact units/coefficients, invariants and independent numerical predictions; distinguish a supplied force law from an emergence experiment |
| Architecture | Define bounded directional sample, reaction and self-attribution ownership; decide compatible clocks and atomic timing without changing `H` or input admission |
| Field development | Compose the selected generic arithmetic and sampling, then replace only the guards whose formerly unsupported cases have become defined and tested |
| Test/physics review | Verify the selected arithmetic, six directions, causality, external response, self-exclusion and source-identified regression evidence |

These outputs are the closure criteria for directional response and delayed
moving-emitter support. The scalar mass-clock timing experiment remains useful
evidence for its stated law and does not close either item.
