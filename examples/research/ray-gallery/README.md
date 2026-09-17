# Ray gallery: one recorded run per ray kind

Exploration evidence of 2026-09-16 at commit `e5b5911`, source fingerprint
`4e0c9eeffd4a1ce1bb832c0687913c71a8c44dd4d79d100296c42e9238f50c36`
(Python 3.14.0rc2, matplotlib 3.11.2). The purpose is a picture, not a
measurement: small legal worlds, one for each ray form the engine propagated
at that revision, each run once through the canonical runner with
`--visualize`, read back tick by tick, and drawn as one animated panel each.
Every panel is a supplied configuration on a contract that
[spatial fields](../../../docs/SPATIAL_FIELDS.md) already names; the runner's
`run.json` records the identity it selected. Nothing here is an engine change.

On 2026-09-17 three of the eight recorded panels were deleted with the rules
they drew (issue #164, bucket B.5, under [Highlights](../../../docs/HIGHLIGHTS.md)
3.18 deleted, 3.19, 3.20, 5.1 and 5.4): panel 4 (bonded rays and the bond
registry), panel 5 (claim and gather) and panel 8 (the lottery capture at a
detector). Their configurations, builders and recorded rows are gone; the five
remaining panels keep their numbers, configurations and recorded results
unchanged, so the counts below are those of the five panels.

**The animation is a faithful drawing of recorded state, not evidence of
physics.** One GIF frame per recorded tick; nothing interpolated, no trajectory
invented; after each tick every ray is at a Node, so nothing is in flight at
frame time. Arrows are rays resident at a Node (length by amount, hue by
Kerengonen phase), squares are records (a record emits, absorbs or reflects;
it is not a ray), shaded cells are octant field stock.

## Replay verified against the recorded frames

The runner's `run.html` frames carry, per Node and tick, the field value,
octant populations and the ray count, but not each ray's heading, amount and
phase. `record_ticks.py` therefore replays the identical `initialization.json`
in-process (the engine is deterministic) and, before anything is drawn, checks
the replay against the recorded frames at every tick: every record's type and
values per Node, every spatial Node's complete readout (value, directions,
populations, ray count) and the escaped totals. Result (`replay_index.json`):
**0 mismatches in all five panels over the 155 recorded frames** (15 + 23 +
31 + 41 + 45, one frame per tick from 0 to the run's length; the 2026-09-16
recording had 226 frames over eight panels). The GIF has 45 frames (the
longest run, panel 7, has 44 ticks); a shorter panel holds its final recorded
frame, marked "held".

## Files and commands

| file | role |
| --- | --- |
| `worlds.py` | the five world builders and the panel table (title, contract label, field, kind) |
| `configs/<panel>.json` | the five documents as run (validated as schema 1 initializations; identical to what `worlds.py` builds) |
| `record_ticks.py` | replays each run in-process, verifies it against `run.html`, writes one per-tick JSON per panel and `ticks/index.json` |
| `render_rays.py` | composes the GIF and four stills from the per-tick JSON |
| `summary.json` | the recorded render summary: per panel the configuration, ticks, run flags, replay verification, derived facts, what it shows and does not show, the records on the board |
| `replay_index.json` | the recorded `ticks/index.json`: fingerprint and mismatch count per panel |

Not committed: the run directories (`run.html`, `events.jsonl`, `state.json`),
the per-tick JSON (up to 250 KB per panel), `rays.gif` and the four stills.

```sh
export PYTHONPATH=src
OUT=artifacts/research/ray-gallery
for k in 1-outward-halo 2-straight-rays 3-double-slit 6-mirror-cavity 7-ray-delay; do
  python -m event_universe --init examples/research/ray-gallery/configs/$k.json --output $OUT/runs/$k --visualize --frame-stride 1
done
python examples/research/ray-gallery/record_ticks.py --output $OUT     # writes $OUT/ticks/
python examples/research/ray-gallery/render_rays.py --output $OUT      # writes $OUT/rays.gif, stills, summary.json; needs the render extra
```

`python -m event_universe.configuration_validation --kind initialization examples/research/ray-gallery/configs/*.json`
reported every committed configuration valid. Re-run at packaging (commit
`d5d2427`): the runs, the replay check and the render; see the packaging note
at the end.

## The five panels

| panel | contract (run.json identity) | ticks | run flags | rays versus records |
| --- | --- | --- | --- | --- |
| 1. Outward octant field | `conservative-outward-v1`, transport `outward-octants`, allocation `carried-straight-phase-v1` | 14 | completed, balanced; conserved false (external source: 3024 injected, 1680 in field + 1344 escaped) | no rays exist in this panel: octant populations are this contract's ray form. Records (not rays): the charge |
| 2. Straight directional rays | `isotropic-ray-field-v1`, transport `straight-rays` (funded, directed headings [1,0,0] [0,1,0] [2,1,0]) | 22 | completed, balanced; conserved false (104 of 144 quanta escaped the open boundary) | rays cross at a Node without responding, one link per tick along an integer line. Records (not rays): the three lamps |
| 3. Kerengonen phased rays | `kerengonen-ray-field-v1` (share capture), 8 phase steps advancing 2 per link | 30 | completed, balanced; conserved false (696 escaped) | two lamps in phase, a screen of nine absorbers ten links on. Records (not rays): lamps A and B, the nine screen absorbers |
| 6. Mirror reflection | `kerengonen-ray-field-v1` (`kerengonen_mirror` x, carried phase) | 40 | completed, balanced, conserved (16 quanta) | one parcel each way; a mirror absorbs a ray for one tick and re-emits it along the mirrored heading at the carried phase; there is no ray-to-ray reflection rule. Records (not rays): lamp, two mirrors |
| 7. Ray delay under a computation field | `kerengonen-ray-field-v1` + `ray_delay` + `directional-departure-delay-along-v1`, phase `per-link` | 44 | completed, balanced; conserved false (computation field sourced) | a lamp's ray train crosses Nodes loaded by a mass record's outward computation field; `ray_wait` registers hold rays k cycles; the wait is the configured local delay law, not a gravitational one. Records (not rays): lamp, screen, mass body |

All five: status `completed`, `accounting_balanced_at_every_completed_tick`
true (final = initial + sources - escaped). `conserved_at_every_completed_tick`
is false exactly where quanta escape the open boundary or are injected by a
`source: true` rule, by design.

## Recorded facts per panel (from the replay, never from a model)

| panel | recorded fact |
| --- | --- |
| 1 | radiation stock at the end: 1680 in the field, 1344 escaped, 3024 injected (216 per tick for 14 ticks) |
| 2 | 104 of 144 quanta escaped by tick 22; final momentum in records (-64, -56, 0) against escaped (64, 56, 0) |
| 3 | screen stock by y = 0..8 at tick 30: 128 132 136 72 144 72 136 132 128; y = 3 and 5 are the half-turn Manhattan path difference |
| 6 | mirrors hold stock at ticks 5, 14, 23 and 32 (both mirrors each time): a 9-tick round trip of 8 links plus one tick in the record |
| 7 | first screen click at tick 23 against 11 in the same world without load (an in-process tuning run, not a recorded panel); largest `ray_wait` per column x = 3..11: 1 2 2 2 3 2 2 2 1 |

A note recorded in `summary.json`: panel 7 was first run with budget 100 and
emission 2400 and stopped at tick 7 with `funded ray emission or absorption
does not support a delayed carrier cycle` (the load reaching the held lamp and
screen plus their cycle cost exceeded the budget); the recorded panel uses
budget 1000 and emission 28000, the scale of `tests/test_ray_delay.py`.

## What is not established

- Nothing physical: no light speed (only the configured link clock), no
  wavelength unit, no cross section, no gravitational law, no rate.
- The double-slit profile is a single short run, drawn as recorded; it is not
  a statistic.
- The mirror cavity shows that reflection passes through a record; the engine
  has no rule by which two rays reflect each other (see
  [ray form](../ray-form/README.md)).

## Packaging note

At packaging (commit `d5d2427`, a later engine than the recorded
`e5b5911`, fingerprint `39a611dd...`) the eight runs of the 2026-09-16
recording, the replay check and the render were repeated from the committed
configurations: 0 mismatches over the same 226 frames, and every panel's
ticks, verification, derived facts, record list and run flags identical to
`summary.json` (only `source_sha256` differs). The deletion of panels 4, 5 and
8 on 2026-09-17 removed their rows from `summary.json` and
`replay_index.json` and left the five remaining rows as recorded.
