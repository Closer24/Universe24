# Run performance

## Active engine: default Focus and exact plan reuse

Measured on Linux with Python 3.14.7 on 2026-09-15. Baseline:
`4796cb256cbdbd830aa29cc3038fea98087de58b`, with its original default Focus off.
The proposed default enables certified empty-carrier scheduling and pure plan
reuse; both transport engines additionally index occupied output banks.

| Input | Ticks | Baseline median | Optimized median | Elapsed time change |
| --- | ---: | ---: | ---: | ---: |
| One moving carrier leaving an empty trail | 240 | 0.2041 s | 0.0849 s | 58.4% shorter |
| 32 repeated moving carriers, periodic domain | 120 | 1.1858 s | 0.8199 s | 30.9% shorter |
| 16 repeated local two-field configurations | 48 | 6.7063 s | 4.5271 s | 32.5% shorter |
| Existing finite-field example | 16 | 0.1898 s | 0.1960 s | 3.3% longer |

Each value is the median of three fresh processes. Variant order alternates.
Timers include `step()` and the same ordered event serialization, while excluding
initialization, imports, per-tick comparison reads and HTML export. CPU time is
recorded separately. These are small input-specific benchmarks, not universal
speed guarantees. The low-repetition finite-field input showed no benefit;
cache lookup and index maintenance can outweigh savings in such a short world.

For repeated carriers, 3840 local planning requests required only two actual law
evaluations. The 16 repeated field configurations required 47 spatial evaluations
for 752 requests and one carrier evaluation for 736 requests. Every Node still
performed its own guarded commits, event publication and modeled cost accounting;
reducing planner work by more than 90% does not reduce whole-run time by 90%.

Across all 24 measured runs, the cumulative hashes of every completed tick's
snapshot, actual inventory and computation report matched within each input.
Full ordered event trace hashes and final accounting also matched. Every run
produced HTML using the existing `render_disturbances` generator. Browser visual
inspection was unavailable because the browser policy blocked local-file access;
HTML generation and embedded recording integrity were checked separately.

Baseline source fingerprint:
`c70c279be058f8730358a9110a9a51a1c201e91f5f0d884641cbfc3ef263fb14`.
Optimized source fingerprint:
`7c5375d1731082a27cb9f50fd2fe5e87c0bad761d8a67b6c679b469d2f83b346`.
The fingerprint covers active Python source, not generated outputs or this text.

A subsequent constructor correction preserves the original spatial planner object
for direct law inspection while passing the same reuse adapter to execution.
Its source fingerprint is
`4e0c9eeffd4a1ce1bb832c0687913c71a8c44dd4d79d100296c42e9238f50c36`.
All four inputs were replayed on this corrected source and matched the recorded
state, event, cost and accounting evidence exactly. The table remains the earlier
isolated timing measurement: constructor setup is outside its timer, the stepping
callback is unchanged, and timings from the extra acceptance replays are not used.

Reproduce with the same environment and `tools/benchmark_focus.py`, setting
`PYTHONPATH` to each chosen checkout's `src`. Select `--case trail`, `repeated`,
`fields` or `finite`, provide that checkout with `--source`, and use a fresh
`--output` directory. `--focus true` or `--focus false` provides an explicit
control. Run each comparison at least three times. Inputs, events, result JSON
and canonical HTML are written together; generated outputs stay outside commits.
See [Local Focus](LOCAL_FOCUS.md) for eligibility, bounds and supercell limits.

## Active engine: one validation per crossing and undecoded checks

Measured on Linux with Python 3.14.0rc2 on 2026-09-16 with the same
`tools/benchmark_focus.py` inputs. Baseline: `e5b5911` (merged Focus default).
Profiling that baseline showed `node_boundary.validate_record` at about half
of the repeated-carrier step time, with each delivered record validated by the
transport loop, by `DisturbanceNode.receive` and again by `validate_records`
over the received records. In the two-field input, `decode` and `unpack`
took more than half of the step time, reached from conservation readouts,
field guard validation and spatial-state validation.

Three host-only changes follow, each with identical physical outputs:

- A delivered record is validated once, by the receiving Node. `receive`
  passes its validated arrivals to `validate_records` as verified objects, so
  only new records such as merges are checked again; transport validates only
  records escaping through an open boundary. Malformed records raise the same
  errors at the same boundary.
- `FieldDefinition.validate` and `SpatialState.validate` inspect codes without
  decoding: a valid code is an integer in `1..2*MAX_VALUE+1` and an even code
  is exactly a negative value. Messages and their order are unchanged.
- `LocalBalanceGuard` keeps two bounded caches (4096 entries each, least
  recently used eviction) of successful readouts keyed by quantity index and
  the immutable record values or spatial bundle. Failures are never retained;
  the discarded validation meter charges nothing observable. The caches are
  bounded at 2 x 4096 entries, belong to one guard instance (a derived guard
  starts empty), assume the boundary validation that precedes every readout,
  and are deliberately absent from `execution_report()` so that execution
  reports stay identical to the baseline.

| Input | Ticks | Baseline median | Optimized median | Elapsed time change |
| --- | ---: | ---: | ---: | ---: |
| One moving carrier leaving an empty trail | 240 | 0.0478 s | 0.0362 s | 24.1% shorter |
| 32 repeated moving carriers, periodic domain | 120 | 0.4590 s | 0.3755 s | 18.2% shorter |
| 16 repeated local two-field configurations | 48 | 2.3308 s | 0.9181 s | 60.6% shorter |
| Existing finite-field example | 16 | 0.1028 s | 0.0977 s | 4.9% shorter |

Each value is the median of three fresh processes per stage; the same
timer as the earlier table is used. Intermediate stages measured 18.3%
(repeated) after the first change and 25.7% (two-field) after the second; the
readout cache contributes most of the two-field gain, while the small
carrier-only inputs vary by a few milliseconds between stages. These are
small input-specific measurements on a shared host, not speed guarantees.

Across all 48 measured runs (baseline plus three stages, four inputs, three
runs each), `state_sha256`, `events_sha256`, the computation report, final
totals, spatial accounting and the execution report matched the baseline
exactly within each input. Modeled operation cost and world time are
unchanged; only host work was removed. HTML export ran through the existing
generator without visual inspection.

Baseline source fingerprint:
`4e0c9eeffd4a1ce1bb832c0687913c71a8c44dd4d79d100296c42e9238f50c36`.
After the first change:
`1ebe5f5f00f8a87003e97d9d1bc8a3eb12f5a334b4ec24305d28f4a71b3e9bb5`;
after the second:
`fa966dd12f3527be137217fe5de0a55c9a9f0730bbd5706f83a1762653d005b2`;
optimized source fingerprint:
`39a611ddd1df3f549566a233417c3cb2c28cb953fc52cd388b96f5cbde04a516`.
The fingerprint covers active Python source, not generated outputs or this text.

`validate_field_guards` in `fields/local_field_rules.py` still decodes its
stock and outgoing payloads on every commit; reusing its result would need a
cache keyed by the complete spatial state and plan, threaded through the
spatial Node services, and was left for a separate change.

## Historical renderer measurements

These are dated measurements of the historical scalar/particle renderer, which
was deleted together with its runner and scenarios on 2026-09-17 (issue #164,
bucket A). They cannot be reproduced on the current tree and do not measure the
active initialization-defined disturbance engine. Current runs are headless
unless visualization is explicitly requested.

## Measured contact run

Measured on the same Windows host on 2026-09-11, using Python 3.14.7,
Matplotlib 3.11.1, Pillow 12.3.0 and NumPy 2.5.3 in one existing environment.
The baseline was commit `1168463ae7d211f86274200dd75c5e03c556c8f3`.
Each measurement used the historical contact scenario: 48 physical ticks, 49 saved
frames, stride 1, and enhanced 1500x1275 3D GIF and standalone HTML.

| Measured phase | Before | After |
| --- | ---: | ---: |
| Simulation, capture and metadata before rendering | 0.724 s | 0.697 s |
| Rendering and GIF/HTML export | 44.106 s | 20.349 s |
| Total run after imports | 44.831 s | 21.046 s |

This run completed **2.13 times faster**, with a **53.1% shorter elapsed time**.
These are single before/after wall-clock measurements, not a cross-platform
guarantee or a statistical benchmark. Setup, dependency installation and imports
are excluded. Larger fields or longer runs can have different bottlenecks.

The baseline source fingerprint is
`c7696ccccad62080363a35673f9e6be053c3f5461909160de8792abc8b621256`;
the optimized source fingerprint is
`49c8e8fe8401f038d463ab20ab331392ae8a41c723bd25309a9af571eb2be506`.
Fingerprints identify the active Python source, independently of documentation.

## Validation environment

The Windows validation environment enables UTF-8 mode (`$env:PYTHONUTF8 = '1'`
in PowerShell) before the unchanged gate. Some existing tests read UTF-8 source
and HTML through the platform default encoding; a legacy Windows code page
cannot decode those files. This setting does not change simulation arithmetic.

Generated GIFs, HTML, event traces and timing records belong in run outputs,
outside source commits. Their comparison and the executed gate results are
recorded in the implementation PR.
