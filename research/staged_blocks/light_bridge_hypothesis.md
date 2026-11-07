# Light as a proposed bridge between board dynamics and recorded events

**Status: bridging hypothesis, not an established physical result.** This note
changes no model, preparation, observer or accepted experiment. The contract remains fixed
Rule3, one board, 48 channels per node and six spatial neighbors.

## The candidate claim

A **board carrier** is a specified transported counter/remainder pattern.
An **observed photon** would be a separately defined pattern of detector records
under a fixed observation map. One record need not identify a unique microscopic
pattern, and an arithmetic C event
has not yet been derived as a photon detection.

The hypothesis has three separable parts:

1. A fixed map from board states to local clock and detector records supports
   an operational signal speed `c` that agrees for a declared family of observers
   moving relative to the board.
2. A realized branching component sends its accepted outgoing light signals at
   that same operational speed. Branch production, propagation and final record
   formation are distinct measurements.
3. A stronger **uniqueness extension** proposes that light supplies the sole
   independent invariant linking the two descriptions. Specify the observables,
   observer changes and meaning of independence before testing this. Functions
   of the same invariant are not separate discoveries. Present data establish no
   universal uniqueness claim.

## What locality proves

For cube coordinates in `0..L-1`, define

`d1(x,y) = sum_i min(|x_i-y_i|, L-|x_i-y_i|)`.

Every new node state depends only on its old state and its six old neighbors.
Under the same fixed tensor, induction gives an exact bound: agreement of all
48 triples at every initial node `y` with `d1(x,y)<=t` implies agreement at node
`x` after `t` updates.
An influence cannot cross more than one spatial edge per update. Channel
permutations and signed sums do not create additional spatial links.

This is an L1 causal cone in board coordinates. It proves neither isotropy nor
Lorentz symmetry, operational observer independence or identification of one
edge per update with physical `c`. It also does not construct a fork: permission
for influence to reach two regions is not evidence for two usable outgoing
carriers. The [prepared guided packet](../../docs/CONFIRMATION_BLOCK.md) realizes
one exact translation within its specified guide environment.

## Fix the observation and calibration first

Declare clocks, detectors, signals, observer identities, lengths, time readings,
trial boundaries and no-click outcomes before a run. Preserve every arithmetic
C0/C1/C2 event alongside the proposed physical readout. Keep the same definitions
across directions, velocities and controls.

An operational model observer must be represented by Rule3 states and
records. A moving sampling window is useful analysis, but
does not establish a moving physical observer. A clock phase modulo four also
does not by itself provide an accumulated elapsed-time record.

Choosing units in which a measured speed equals one is not evidence that all
observers measure the same speed. Register independent preparation/calibration
procedures and dimensionless comparison ratios before measuring the tested
carrier. Do not redefine distance, clock rate or detector response separately
for each trajectory to enforce the desired result.

## Independent ways the hypothesis could fail

1. **Motion relative to the board.** Prepare stationary and moving model
   observers with the same registered clock/detector roles. Compare signal
   round-trip readings over a fixed range of relative velocities. A reproducible
   velocity dependence outside the declared error bound refutes that domain.
2. **Direction and scale.** Test rotated paths, several non-axis directions,
   distances and cube sizes. Separate propagation delay from interface latency
   and periodic returns. Direction dependence cannot be removed by refitting
   the observation map afterward.
3. **Round trips and synchronization.** Start with departure and return recorded
   by one local apparatus. Separately register a procedure for synchronizing
   distant clocks and test its predictions. Agreement cannot be assumed in the
   synchronization procedure and then counted again as a result.
4. **Detector calibration and branching.** Include source-off, delayed-arrival,
   duplicate-message and independently functional output controls. Measure
   detection latency and missed records. A usable two-output fork must first
   exist before its propagation speed can be compared with the parent carrier.
5. **Uniqueness.** Seek a second independent invariant in the declared observable
   class. Finding one rejects the uniqueness extension without necessarily
   rejecting an invariant light-speed hypothesis.

## Present evidence and limits

The [phase study](phase_protocol.json) and its
[independent audit](evidence/independent_audit/phase.json) support finite
synchronization of a prepared clock against a same-board reference. D/X remains
a passive calculation; aligned arrivals can leave its value unchanged. These
results do not yet provide calibrated photon detectors, moving measuring
apparatus or an operational observer-independent `c`.

The board already has mathematical invariants: `r_next-r=2u-6ell` preserves
parity at each fixed node/channel. Writing `r=2s+p` gives
`ell=floor((u+s)/3)`, `s_next=(u+s) mod 3`, `p_next=p`. Consequently, matching
initial `(a,b,s)` fields with different parity fields produce identical counters
and guarded C records. A passive full-state reader can inspect parity, but these
internal responses cannot distinguish it. Thus a mathematical invariant need not
be an observable physical invariant. Whether light is the sole invariant in the
declared observation class remains a separate hypothesis.
