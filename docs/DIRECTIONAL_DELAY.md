# Directional origin waiting

This optional timing hypothesis delays both carriers and every spatial field bundle
at their origin. It does not modify momentum or choose a different routing port.
Configure it in the runtime document or the environment part:

```json
"directional_delay": {
  "model_id": "positive-projection-origin-wait-v1",
  "field": "load",
  "divisor": 2
}
```

The named field must be a three-component spatial field. At a field phase, before
fresh emission or forwarding, sample its baseline plus owned populations as L.
For configured port offset d, additional wait is
`ceil(max(0, dot(L,d)) / divisor) * link_ticks`.
The divisor is a positive integer. Signed sums use bounded working registers;
final components and wait timestamps must fit the physical integer bound.
Offsets are integer affinities, not normalized Euclidean unit vectors. Thus
noncardinal topologies use their declared offsets without hidden normalization.
For L=(6,-4,0), divisor=2, the six waits are (3,0,0,2,0,0) link intervals.
Reversing L reverses the slowed directions. This is an explicit new law, not a
formula derived from previously measured scalar computation cost or real gravity.

The same local sample supplies field reservations and carrier proposals begun in
that phase. A carrier first completes its ordinary uniform computation delay,
then its frozen directional wait. Field packets wait from their field commit.
The timing calculation itself costs 9 reads, 24 updates and 5 evaluations per port
under the configured operation tariff; zero directional wait is not zero work.
A later incoming field never reschedules an existing reservation.

Waiting payloads occupy fixed origin departure buffers and are counted once in
inventory. Snapshots include phase=waiting and dispatch_tick; playback labels them
as origin buffers. Upon dispatch, phase becomes transit and actual sent events are
emitted. Arrival is always dispatch_tick + link_ticks. Decay and open escape happen
only at completed arrival. Checkpoints retain the phase and frozen schedule.
The current batch policy waits until all outgoing slots of an origin are empty
before starting another batch. A slow port can therefore hold up later fast-port
batches. Held emitters pause their injection while their field batch is occupied.

This first version rejects moving emitters, spatial responses (couplings and
joint interactions), native event programs and formal SI calibration. These need
separate composition contracts. Existing configurations that omit the option keep
the previous scheduling law. Ordinary configured momentum updates are independent
features; omit them for a timing-only experiment.

`tests/test_directional_delay.py` checks exact port times, signs, fixed transit,
unchanged oblique carrier port sequence, ownership, checkpoint restoration,
cancellation bounds, later arrivals, finite sources and decay/escape timing.
Timing can change field distributions because field transport branches; a whole
carrier with unchanged momentum follows the same port sequence at equal hop count.
No orbital-motion or physical-energy conservation claim follows from these tests.
