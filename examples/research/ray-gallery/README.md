# Ray gallery: one recorded run per ray kind

The bonded-pair and lottery panels explicitly select
`historical-autonomous-v1` under the
[sampling admission contract](../../../docs/DETECTOR_SAMPLING.md).
Their autonomous draws are historical research, not canonical external Detector
behavior. The other six panels retain the default deterministic profile. New
runner metadata records the selected profile; the dated results below retain
their original source and scope.

Exploration evidence of 2026-09-16 at commit `e5b5911`, source fingerprint
`4e0c9eeffd4a1ce1bb832c0687913c71a8c44dd4d79d100296c42e9238f50c36`
(Python 3.14.0rc2, matplotlib 3.11.2). The purpose is a picture, not a
measurement: eight small legal worlds, one for each ray form the engine
propagates at this revision, each run once through the canonical runner with
`--visualize`, read back tick by tick, and drawn as one animated panel each.
Every panel is a supplied configuration on a contract that
[spatial fields](../../../docs/SPATIAL_FIELDS.md) already names; the runner's
`run.json` records the identity it selected. Nothing here is an engine change.

**The animation is a faithful drawing of recorded state, not evidence of
physics.** One GIF frame per recorded tick; nothing interpolated, no trajectory
invented; after each tick every ray is at a Node, so nothing is in flight at
frame time. Arrows are rays resident at a Node (length by amount, hue by
Kerengonen phase), squares are records (a record emits, absorbs, reflects or
detects; it is not a ray), shaded cells are octant field stock or claims. The
bond registry and the lottery ticket have no drawing; only their recorded
consequences on the board appear.

## Replay verified against the recorded frames

The runner's `run.html` frames carry, per Node and tick, the field value,
octant populations and the ray count, but not each ray's heading, amount and
phase. `record_ticks.py` therefore replays the identical `initialization.json`
in-process (the engine is deterministic: seeded lotteries, seeded bond
registry) and, before anything is drawn, checks the replay against the recorded
frames at every tick: every record's type and values per Node, every spatial
Node's complete readout (value, directions, populations, ray count) and the
escaped totals. Result (`replay_index.json`): **0 mismatches in all eight
panels over the 226 recorded frames** (15 + 23 + 31 + 13 + 41 + 41 + 45 + 17,
one frame per tick from 0 to the run's length). The GIF has 45 frames (the
longest run, panel 7, has 44 ticks); a shorter panel holds its final recorded
frame, marked "held".

## Files and commands

| file | role |
| --- | --- |
| `worlds.py` | the eight world builders and the panel table (title, contract label, field, kind) |
| `configs/<panel>.json` | the eight documents as run (validated as schema 1 initializations; identical to what `worlds.py` builds) |
| `record_ticks.py` | replays each run in-process, verifies it against `run.html`, writes one per-tick JSON per panel and `ticks/index.json` |
| `render_rays.py` | composes the GIF and four stills from the per-tick JSON |
| `summary.json` | the recorded render summary: per panel the configuration, ticks, run flags, replay verification, derived facts, what it shows and does not show, the records on the board |
| `replay_index.json` | the recorded `ticks/index.json`: fingerprint and mismatch count per panel |

Not committed: the run directories (`run.html`, `events.jsonl`, `state.json`),
the per-tick JSON (up to 250 KB per panel), `rays.gif` and the four stills.

```sh
export PYTHONPATH=src
OUT=artifacts/research/ray-gallery
for k in 1-outward-halo 2-straight-rays 3-double-slit 4-bonded-pair 5-claim-gather 6-mirror-cavity 7-ray-delay 8-lottery-detector; do
  python -m event_universe --init examples/research/ray-gallery/configs/$k.json --output $OUT/runs/$k --visualize --frame-stride 1
done
python examples/research/ray-gallery/record_ticks.py --output $OUT     # writes $OUT/ticks/
python examples/research/ray-gallery/render_rays.py --output $OUT      # writes $OUT/rays.gif, stills, summary.json; needs the render extra
```

`python -m event_universe.configuration_validation --kind initialization examples/research/ray-gallery/configs/*.json`
reported all eight valid. Re-run at packaging (commit `d5d2427`): all eight
runs, the replay check and the render; see the packaging note at the end.

## The eight panels

| panel | contract (run.json identity) | ticks | run flags | rays versus records |
| --- | --- | --- | --- | --- |
| 1. Outward octant field | `conservative-outward-v1`, transport `outward-octants`, allocation `carried-straight-phase-v1` | 14 | completed, balanced; conserved false (external source: 3024 injected, 1680 in field + 1344 escaped) | no rays exist in this panel: octant populations are this contract's ray form. Records (not rays): the charge |
| 2. Straight directional rays | `isotropic-ray-field-v1`, transport `straight-rays` (funded, directed headings [1,0,0] [0,1,0] [2,1,0]) | 22 | completed, balanced; conserved false (104 of 144 quanta escaped the open boundary) | rays cross at a Node without responding, one link per tick along an integer line. Records (not rays): the three lamps |
| 3. Kerengonen phased rays | `kerengonen-ray-field-v1` (share capture), 8 phase steps advancing 2 per link | 30 | completed, balanced; conserved false (696 escaped) | two lamps in phase, a screen of nine absorbers ten links on. Records (not rays): lamps A and B, the nine screen absorbers |
| 4. Bonded rays | `kerengonen-ray-field-v1` with bonds `bonded-ray-field-v1` (`bond_field` origin, `bond_setting`) | 12 | completed, balanced, conserved (8 quanta) | one Node births a pair per tick with one bond code (dashed link = equal code, not a ray or signal); plus detectors ask the registry, minus detectors take what walks on. Records (not rays): sources, four detectors |
| 5. Claim and gather | `isotropic-ray-field-v1` with claims `claim-gather-ray-field-v1` (pace 1/4, dissolve) | 40 | completed, balanced, conserved (64 matter) | a particle dissolves into eight planar rays; the screen's click opens a claim that floods the Nodes (knowledge, not stock); free rays turn homing and walk home. Records (not rays): particle, screen |
| 6. Mirror reflection | `kerengonen-ray-field-v1` (`kerengonen_mirror` x, carried phase) | 40 | completed, balanced, conserved (16 quanta) | one parcel each way; a mirror absorbs a ray for one tick and re-emits it along the mirrored heading at the carried phase; there is no ray-to-ray reflection rule. Records (not rays): lamp, two mirrors |
| 7. Ray delay under a computation field | `kerengonen-ray-field-v1` + `ray_delay` + `directional-departure-delay-along-v1`, phase `per-link` | 44 | completed, balanced; conserved false (computation field sourced) | a lamp's ray train crosses Nodes loaded by a mass record's outward computation field; `ray_wait` registers hold rays k cycles; the wait is the configured local delay law, not a gravitational one. Records (not rays): lamp, screen, mass body |
| 8. Lottery capture at a detector | `kerengonen-ray-field-v1` (capture lottery, `capture_salt`) | 16 | completed, balanced; conserved false (6 reference quanta escaped) | a reference lamp lands a quantum per tick at each plus detector at the setting phase (coherence one half); the lottery takes or passes each whole ray; the minus detector takes what passed. Records (not rays): sources, reference lamps, four detectors |

All eight: status `completed`, `accounting_balanced_at_every_completed_tick`
true (final = initial + sources - escaped). `conserved_at_every_completed_tick`
is false exactly where quanta escape the open boundary or are injected by a
`source: true` rule, by design.

## Recorded facts per panel (from the replay, never from a model)

| panel | recorded fact |
| --- | --- |
| 1 | radiation stock at the end: 1680 in the field, 1344 escaped, 3024 injected (216 per tick for 14 ticks) |
| 2 | 104 of 144 quanta escaped by tick 22; final momentum in records (-64, -56, 0) against escaped (64, 56, 0) |
| 3 | screen stock by y = 0..8 at tick 30: 128 132 136 72 144 72 136 132 128; y = 3 and 5 are the half-turn Manhattan path difference |
| 4 | four pairs, registry answers (Alice, Bob): (-, +), (-, +), (+, +), (+, -); taken at +A 2, passed to -A 2; taken at +B 3, passed to -B 1; four pairs are not a statistic |
| 5 | first claim at tick 11, the whole 64 gathered at the screen by tick 21 |
| 6 | mirrors hold stock at ticks 5, 14, 23 and 32 (both mirrors each time): a 9-tick round trip of 8 links plus one tick in the record |
| 7 | first screen click at tick 23 against 11 in the same world without load (an in-process tuning run, not a recorded panel); largest `ray_wait` per column x = 3..11: 1 2 2 2 3 2 2 2 1 |
| 8 | eight quanta per side: taken at +A 5, passed to -A 3; taken at +B 6, passed to -B 2; not a rate measurement |

A note recorded in `summary.json`: panel 7 was first run with budget 100 and
emission 2400 and stopped at tick 7 with `funded ray emission or absorption
does not support a delayed carrier cycle` (the load reaching the held lamp and
screen plus their cycle cost exceeded the budget); the recorded panel uses
budget 1000 and emission 28000, the scale of `tests/test_ray_delay.py`.

## What is not established

- Nothing physical: no light speed (only the configured link clock), no
  wavelength unit, no cross section, no gravitational law, no rate.
- The double-slit profile, the bonded outcomes and the lottery outcomes are
  single short runs, drawn as recorded; they are not statistics.
- The mirror cavity shows that reflection passes through a record; the engine
  has no rule by which two rays reflect each other (see
  [ray form](../ray-form/README.md)).

## Packaging note

At packaging (commit `d5d2427`, a later engine than the recorded
`e5b5911`, fingerprint `39a611dd...`) the eight runs, the replay check and the
render were repeated from the committed configurations: 0 mismatches over the
same 226 frames, and every panel's ticks, verification, derived facts, record
list and run flags identical to `summary.json` (only `source_sha256` differs).
