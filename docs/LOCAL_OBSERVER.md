# Local reception observer

`local-reception-observer-v1` is an optional passive probe at one configured node.
It records what has actually arrived through the six links. This operational
observation layer does not establish human optics, proper time, an emergent
spacetime, Maxwell equations or a new Gauss constraint.

## Run and view

Generate an initialization and separate probe placement, then use the ordinary
runner and existing HTML generator:

```bash
python examples/observer/configuration.py --size 9 --output artifacts/observer-input
python -m event_universe --init artifacts/observer-input/initialization.json --observer artifacts/observer-input/observer.json --output artifacts/observer-run --visualize
```

Keep reusable inputs outside the disposable run output directory. The placement
file contains `{"position": [4, 4, 4], "max_receipts": 100000}`. Choose another
in-bounds integer position and rerun to move the probe; no rebuild is needed.
The API accepts `run_initialization(..., observer=Path("observer.json"))`.
Without `--visualize`, the same observer produces JSON without physical frame
capture. No GIF is required.

The runner saves normalized `observer.json`, local `observations.json` and the
ordinary initialization, event trace, state and run metadata. HTML defaults to
**Local observer** when observation data exists. **World audit** explicitly opens
the global recording for comparison; that view is not local probe knowledge.

## Inputs, clock and exact history

- Completed `received` events contribute configured disturbance labels, carried
  integer values and receiver-facing ports.
- Completed `spatial_received` events contribute per-port field component sums
  after the configured receiver decay and ownership commit. Travel ports are
  reversed once: +X travel arrives through the receiver's -X side. A used port
  with a zero reading remains distinct from a port with no arrival.
- Local `cycle_committed` events increment a completed whole-node carrier-cycle
  counter. This is not a count of host seconds, scheduler ticks, individual
  operations or particles. A configured held record supplies a repeated process;
  absent local cycles, the counter stays zero. Field forwarding is not a clock.
- The ideal probe records delivery even while the carrier cycle waits. This
  does not mean a material detector or human has processed the input. Such a
  detector needs an explicitly priced local response law.

Receipt sequence numbers are archive order, not elapsed time. Several arrivals
can share one clock reading; the counter cannot distinguish simultaneity from
arrivals between completions. Changing global timestamps while preserving the
local event sequence leaves these readings unchanged.

Remote events, origins, scheduled arrival times, global causal IDs/parents,
totals and quantum controller information are excluded from the local whitelist.
Each sampled frame stores its clock and exact receipt prefix at capture time.
Global timestamp filtering alone is unsafe: the initial tick-zero frame can
precede a later commit also stamped tick zero. Rewinding uses the captured prefix
and never reveals later records. Frame stride changes sampling, not receptions.

## Interpretation and limits

The six panels identify the last incoming link, not a remote source location
after turns. They do not infer distance, emission time or current source state.
Signed scalar/vector payloads retain configured labels and units; labels do not
supply color, intensity, photons or electromagnetic meaning. Field summaries
aggregate populations on each port; their sum does not reconstruct microscopic
population information.

This is a reception probe, not periodic sampling of static fields or resident
records. No signal is different from zero signal and from a resident field.
Observing a static field through a material response requires a configured local
coupling. Radar distance would require a sender, causal reflection/response and
returned signal measured with a defined clock; it is not inferred from addresses.

Physical updates keep their integer operations, costs, ownership and link times.
The archive never feeds a planner or repairs conservation. Its host memory grows
with local receptions and samples; it is not physical cell memory or an O(1)
physical algorithm. `max_receipts` bounds the receipt archive. Exhaustion reports
a failed run with retained partial evidence, not silent loss. Completed physical
commits stay committed if diagnostic output later fails.

## Acceptance and demonstration

`tests/test_local_observer.py` checks remote withholding until delivery, two-tick
periodic transit, signed post-decay readings, zero versus absence, atomic archive
overflow, copied payloads, exact capture prefixes, clock independence from global
timestamps, frame-stride independence and unchanged physical results/costs.
`tests/test_observer_playback.py` checks backward seeking, paused-clock samples,
safe labels, zero versus unknown and explicit global audit access.

The example uses the same simple rules in 9-cubed and 15-cubed worlds. Two
conserved fields and one configured disturbance approach a held phase-toggle
process. Expected arrivals are audit ticks 4, 6 and 8 for link time 2, through
receiver ports -X, +Y and +Z respectively. Local field computation can delay the
clock while signals arrive. This follows the selected scheduling law; it does
not prove relativistic time dilation or emergent electromagnetism.

### Recorded finite results

On 2026-09-12, both default worlds completed eight ticks with nine frames each,
using runtime SHA256
`c45f9ee8d8696965414cea77b4d2c13fec0fc9f1b412ff2d7047470176c1b935`
after integrating main `b8941d97545e9ab8c35fbff5391288ccffa447bd`.
Their receipt journals and sampled clock/count histories matched exactly after
translating probe placement. Conservation and accounting passed every completed
tick. The ordinary event trace, final state, all frames and observer journal also
matched the pre-integration experiments.

| Audit arrival tick | Receiver side | Nonzero received content | Local cycle counter |
| --- | --- | --- | --- |
| 4 | -X | `pulse_inventory: 7` | 2 |
| 6 | +Y | `pulse_vector: [3, -2, 1]` | 2 |
| 8 | +Z | `message_inventory: 11`, `message_vector: [2, -3, 1]` | 2 |

The held process committed at audit ticks 0 and 2. Its next cycle began at tick
4 with configured cost 288 and scheduled completion 74, beyond this run. The
probe recorded inputs during that wait. The initial frame contains zero
completed cycles because it preceded the tick-zero commit. Desktop/mobile
playback, initial/final frames, rewind and the audit switch were inspected.
These finite results verify the observation mechanism, not perceived time.
