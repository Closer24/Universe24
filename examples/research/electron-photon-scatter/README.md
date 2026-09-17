# Electron-photon scatter: a catalog electron meets directional quanta

Exploration evidence of 2026-09-16 at commit `e5b5911`, source fingerprint
`4e0c9eeffd4a1ce1bb832c0687913c71a8c44dd4d79d100296c42e9238f50c36`
(Python 3.14.0rc2). This is the one study that asked for visualization: the
run was recorded with `--visualize` and rendered from the recorded frames.
The GIF, stills, `run.html`, event trace and state dump are not committed;
the commands below regenerate them.

## Configuration

`build_viz_config.py` derives `electron-photon-scatter.json` from the
checked-in [radiation-scattering adapter](../../radiation-scattering/build.py)
and binds the carrier's charge and mass to the
[entity catalog](../../known-entities/catalog.json) through the shared
reference-unit encoder, as the catalog contact example (`examples/catalog-contact`,
deleted on 2026-09-17) did. Everything physical is catalog data, a supplied rule or an exact
accounting invariant; the bindings file lists them:

| item | value |
| --- | --- |
| `model_id` | `viz-catalog-electron-directional-quanta-scattering-v1`, schema 1, open 17 x 7 x 7 lattice, 16 ticks |
| electron charge | -3 thirds of e, exact (catalog `electric_charge`, PDG lepton table) |
| electron mass | 511 keV/c^2 from 0.51099895069 MeV/c^2, rounding error 0.00105 keV (the published uncertainty is 1.6e-7 keV) |
| photon stream | six pulses of 10 quanta at x = 1..6 heading +x, 1 momentum unit each, no charge, mass or energy register |
| supplied rules | presence marker `exact_div(charge^2, 9)` per interval; hold fraction `min(rad_px, presence * 2)`; scatter: held quanta become `rad_mx` (-x) and the electron gains 2 x held along +x; electron moves along its momentum at `sum(abs(p)) / 48` hops per interval; `electric_signal` halo emitted outward at `charge * 72 = -216` per interval; family selection by carried properties (`requires: [charge]`, `requires: [charge, momentum]`), no type-name dispatch |
| dependency fingerprints | `build.py` `e13044cb...`, `catalog.json` `bbe8d5c0...`, `physical-units.json` `2357d218...` (all three unchanged at packaging) |
| initialization SHA-256 | `1afb3a08f648c4fbb1f0978a7635a61e7361ef95f17224d47a507cbc32adf8cf` |

## Commands

```sh
export PYTHONPATH=src
OUT=artifacts/research/electron-photon-scatter
python examples/research/electron-photon-scatter/build_viz_config.py --output $OUT       # writes $OUT/electron-photon-scatter{,.bindings}.json
python -m event_universe --init examples/research/electron-photon-scatter/electron-photon-scatter.json --output $OUT/run --visualize   # 11 s
python examples/research/electron-photon-scatter/render_scatter.py --run $OUT/run --output $OUT/render    # 19 s; needs the render extra (matplotlib, Pillow)
```

Re-run at packaging (commit `d5d2427`): the rebuilt configuration and bindings
are byte-identical to the committed files; the visualized run and the render
give the same per-tick facts as `render_summary.json` (scatter, hold and hop
ticks, first contact, every per-tick row, every run flag except the source
fingerprint).

## Recorded run (`render_summary.json`)

The renderer asserts, before drawing, that the frames embedded in `run.html`
agree with `events.jsonl` and `run.json`: resident plus escaped quanta equal
the 60 seeded, the electron's momentum plus the direction-weighted quanta
(escaped included) equal (60, 0, 0) at every frame, no quanta leave the x axis,
and the final electron momentum is twice the sum of scattered quanta.

| tick | electron at | electron p | quanta resident + escaped | held quanta (Node) | scatter committed this tick | halo stock |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | (8,3,3) | (0,0,0) | 60 + 0 | - | - | 0 |
| 1 | (8,3,3) | (0,0,0) | 60 + 0 | - | - | -216 |
| 2 | (8,3,3) | (0,0,0) | 60 + 0 | - (first contact: hold rule keeps 2) | - | -432 |
| 3 | (8,3,3) | (0,0,0) | 60 + 0 | 2 at (8,3,3) | 2 | -648 |
| 4 | (8,3,3) | (4,0,0) | 60 + 0 | 2 at (8,3,3) | 2 | -848 |
| 5 | (8,3,3) | (8,0,0) | 60 + 0 | 2 at (8,3,3) | 2 | -1016 |
| 6 | (8,3,3) | (12,0,0) | 60 + 0 | 2 at (8,3,3) | 2 | -1144 |
| 7 | (8,3,3) | (16,0,0) | 60 + 0 | 2 at (8,3,3) | 2; hop sent, arrives tick 8 | -1240 |
| 8 | (9,3,3) | (20,0,0) | 60 + 0 | 2 at (8,3,3) (electron gone) | - | -1312 |
| 9 | (9,3,3) | (20,0,0) | 60 + 0 | 2 at (8,3,3), 2 at (9,3,3) | 2; hop sent | -1368 |
| 10 | (10,3,3) | (24,0,0) | 60 + 0 | 2 at (8,3,3) | - | -1408 |
| 11 | (10,3,3) | (24,0,0) | 52 + 8 | 2 at (8,3,3) | -; hop sent | -1432 |
| 12 | (11,3,3) | (24,0,0) | 44 + 16 | 2 at (8,3,3) | - | -1448 |
| 13 | (11,3,3) | (24,0,0) | 34 + 26 | 2 at (8,3,3) | -; hop sent | -1464 |
| 14 | (12,3,3) | (24,0,0) | 24 + 36 | 2 at (8,3,3) | - | -1480 |
| 15 | (12,3,3) | (24,0,0) | 14 + 46 | 2 at (8,3,3) | -; hop sent | -1496 |
| 16 | (13,3,3) | (24,0,0) | 6 + 54 | 2 at (8,3,3) | - | -1504 |

Run flags: status `completed`, 16 ticks, `accounting_balanced_at_every_completed_tick`
true, `conserved_at_every_completed_tick` false (the `electric_signal` field is
sourced: source total -3456, escaped -1952, final stock -1504; mass 511 and
charge -3 unchanged).

## Findings

1. **Exact accounting.** 60 quanta and total momentum (60, 0, 0) at all 17
   frames, escaped quanta included; six scatters of 2 quanta at ticks 3, 4,
   5, 6, 7 and 9 give the electron p = 24 = 2 x 12 exactly; hops at ticks 7,
   9, 11, 13, 15 follow the supplied rate `|p| / 48`.
2. **Two quanta stranded.** The hold rule (a field rule) keeps 2 quanta at
   the electron's Node in one phase and the scatter (a joint transaction)
   needs the electron resident in the next; when the electron's hop sent at
   tick 7 intervenes, the 2 quanta held at (8,3,3) stay there for the rest of
   the run (`held_px` current stock 2 in `run.json`). Recorded as a defect of
   the two-phase hold/scatter composition of the configured rules.
3. **The halo never decays.** The `electric_signal` stock grows monotonically
   from -216 to -1504 while it spreads and escapes: the configuration is
   schema 1, which dilutes only through redistribution; the explicit
   completed-link decay is a schema 2 option, and the configuration's hold
   and scatter rules were built on the schema 1 adapter.

## Limits and what is not established

- Not reproduced, by construction: the photon energy or frequency shift
  (Compton formula), the Klein-Nishina or any derived cross section,
  relativistic kinematics (the 511 keV/c^2 mass is inert inventory in this
  rule), a Coulomb 1/r^2 field (the halo is a configured outward signal), and
  any energy-family law (no declared relation between the quanta's energy or
  momentum and the electron family's response; the hold fraction is fixed).
- The scattering fraction `presence * 2` is a supplied rule, not a measurement.
- One configuration, one seed-free deterministic run of 16 ticks.
- The rendered GIF is a display of recorded values (one frame per recorded
  tick, nothing interpolated); it establishes nothing the tables above do not.
