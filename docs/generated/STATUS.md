<!-- rendered by tools/render_documents.py from the tree; do not edit by hand -->

# The state of the engine

## The primitives

25 folders under `src/event_universe/features/`: 15 built, 6 of them running their own code; 10 not built. The register reads every card at load; a term of the files naming an unbuilt primitive is refused.

| primitive | place | word | how it runs | its keys of the files | its line in ALGEBRA.md |
| --- | --- | --- | --- | --- | --- |
| **the clicks** | (ii) | after the step | bound through the loop's `bind` | `clicks` (a family's entry) | 9.25 (2), (3); 9.111 items 1, 2 and 6; 9.117 items 2 and 3 |
| **the clicks list** | (ii) | after the step | not built |  | 9.88 (4) |
| **the count's line** | (ii) | after the step | not built |  | 9.121 item 3; 9.119 item 1; 9.57 (1) |
| **the degree** | (i) | the step | bound through the loop's `bind` | `parts` (a family's entry) | 9.86 (2); 9.91 (2) |
| **the feed** | (v) | after the step | not built |  | 9.117 item 2; 9.78 (4); 9.91 (8) (v) |
| **the giving** | (ii) | after the step | its own `apply` |  | the close of the count the click's inverse, the bulk share from the rule 9.57 (1), the window's write beyond (H) (9.117 item 5); 9.117 item 2, the row 'the giving'; 9.107; 9.71 (1); 9.116 item 5; 9.86 (1) |
| **the hand** | (ii) | after the step | not built |  | 9.88 (5) |
| **the hold** | (iv) | the right side | its own `apply` | `held` (a family's entry) | 9.45 (2); 9.91 (3); 9.111 item 3; 9.117 item 3; 9.119 item 2, the row 'the hold' |
| **the hop** | (v) | after the step | bound through the loop's `bind` |  | 9.117 item 2; 9.52; 9.104 item 6 |
| **the induction** | (v) | after the step | not built |  | 9.117 item 2; 9.78 (4); 9.91 (8) (v) |
| **the internal representation** | (i) | the right side | not built |  | 9.88 (7) (i); 9.101; 9.117 item 3 |
| **the lifetime** | (ii) | after the step | not built |  | 9.88 (3); 9.117 item 3 |
| **the operation** | (i) | the step | bound through the loop's `bind` |  | 9.57 (1); 9.112 items 1 and 2 |
| **the pair** | (i) | the step | bound through the loop's `bind` | `pair` (a family's entry) | 9.57 (1); 9.111 item 7 row 1 |
| **the phase** | (i) | the step | bound through the loop's `bind` | `phase` (a family's entry) | 9.91 (2) |
| **the receive** | (i) | the step | its own `apply` |  | 9.112 item 1; 9.96 (2) (e); 9.117 item 3; 9.119 item 2, the row 'the receive' |
| **the recoil** | (iv) | after the step | its own `apply` |  | from the rule 9.57 (1) and the click, the store a remainder of the division on the record (9.117 item 5); 9.117 item 2, the row 'the recoil'; 9.84 (2); 9.91 (4); 9.111 items 1 and 2 |
| **the recoil's accumulator** | (v) | after the step | not built |  | 9.117 item 2; 9.109 item 2 (b); 9.96 (2) (e) |
| **the self-source** | (i) | the right side | its own `apply` | `self_source` (a family's entry) | 9.78 (3); 9.88 (2); 9.91 (5); 9.119 item 2, the row 'the self-source' |
| **the send** | (i) | the step | bound through the loop's `bind` |  | 9.112 item 1 |
| **the signed read** | (i) | the right side | bound through the loop's `bind`; its own `apply` waits | `sign` (a family's entry), `reads` (a family's entry) | from the rule 9.57 (1) and the click (9.117 item 5); 9.117 item 2, the first row; 9.78 (4); 9.108 items 8, 11, 12, 13; 9.116 items 4a and 4c |
| **the source** | (iv) | the right side | not built | `sourced` (a family's entry) | the field's shape from the rule 9.57 (1), the write beyond (H) (9.113 item 2; 9.117 item 5); 9.117 item 2; 9.108 items 3, 10, 11, 13; 9.116 item 4b |
| **the spin's step** | (v) | after the step | its own `apply` | `spins_step` (a family's entry) | 9.117 item 2, the row 'the spin's step'; 9.78 (5); 9.104 (2); 9.119 item 2 |
| **the trace** | any | any | not built |  | 9.112 item 5; 9.117 item 2 |
| **the wait** | (i) | the step | bound through the loop's `bind` |  | 9.112 item 1 |


## The step file's acts

`law/step.json`, digest `777bbb80bd0456a004e4f3d8260dc2e6c3f28d0d82ce51ae8540cabd9c81c275` (written into every output as `step.hash`): 25 acts, of which 16 are built and walked.

| # | place | primitive | words | built |
| --- | --- | --- | --- | --- |
| 0 | (v) | the hop |  | yes |
| 1 | (iv) | the hold | {"advance": false} | yes |
| 2 | (i) | the pair |  | yes |
| 3 | (i) | the degree |  | yes |
| 4 | (i) | the signed read |  | yes |
| 5 | (i) | the send |  | yes |
| 6 | (i) | the wait |  | yes |
| 7 | (i) | the receive |  | yes |
| 8 | (i) | the internal representation |  | no |
| 9 | (i) | the self-source |  | yes |
| 10 | (i) | the phase |  | yes |
| 11 | (i) | the operation |  | yes |
| 12 | (ii) | the clicks |  | yes |
| 13 | (ii) | the lifetime |  | no |
| 14 | (ii) | the giving |  | yes |
| 15 | (ii) | the clicks list |  | no |
| 16 | (ii) | the hand |  | no |
| 17 | (iv) | the hold | {"advance": true} | yes |
| 18 | (iv) | the source |  | no |
| 19 | (iv) | the recoil |  | yes |
| 20 | (v) | the feed |  | no |
| 21 | (v) | the induction |  | no |
| 22 | (v) | the spin's step |  | yes |
| 23 | (v) | the recoil's accumulator |  | no |
| 24 | any | the trace |  | no |


## The expected failures

Each mark names what the tree does not do yet; it comes off when the cut lands.

| test | reason |
| --- | --- |
| `tests/test_engine_acceptance.py:166` | the ledger's item 'a signed read weight' (ALGEBRA.md 9.108 (8)): the loader bounds the weight from 1; when the support lands this passes and the mark comes off |
| `tests/test_engine_acceptance.py:267` | the ledger's item 'no flag, family name or number in the code' (records 2172 to 2174): the loader still writes defaults for keys of the files; the review aft... |
| `tests/test_genericity.py:139` |  |
| `tests/test_ledger_items.py:94` | item 2 of record 2199: the loader admits `reads`, not the term form [kind, target, of, degree, weight, table] |
| `tests/test_ledger_items.py:123` | item 2 of record 2199: the step's four declarations (send, receive, wait, operation) are not read from universe.json |
| `tests/test_ledger_items.py:166` | item 3 of record 2199: no record adds its count into a family's level; the loader refuses `sourced` |
| `tests/test_ledger_items.py:195` | item 3 of record 2199: the guard is the load's alone, from below; a pace above Gamma at run time is not refused |
| `tests/test_ledger_items.py:218` | item 4 of record 2199: the recoil is not built; a body's held momentum does not move at a click |
| `tests/test_ledger_items.py:245` | item 5 of record 2199: the trace that shows the interval's order is not built |
| `tests/test_ledger_items.py:287` | item 7 of record 2199: the start file's `trace` is not read; nothing is traced |
| `tests/test_ledger_items.py:316` | item 8 of record 2199: no parallel or active path; the start file's keys are refused |
| `tests/test_loader_acceptance.py:127` | ALGEBRA.md 9.120 item 1 with record 2226: the frame reads the body's form (#1221) and the loop still reads N, age_bound, clock_stamp and the flags massive_re... |
| `tests/test_loader_acceptance.py:147` | ALGEBRA.md 9.117 row 'the source' with record 2226: the frame reads `sourced` from the source folder's card (#1206) and `world.py` carries it as the family's... |
| `tests/test_loader_acceptance.py:169` | record 2199 item 1 with record 2226: K, release and width are gone (#1236); the source worlds still carry none of N, age_bound, clock_stamp, massive_record a... |
| `tests/test_loader_acceptance.py:208` | record 2226 (1) and (2): every key of a shipped family's entry is one folder's card (#1206, #1236) but `spins_step`, the frame's until #1203's card lands; `w... |
| `tests/test_source_worlds.py:196` | the loader reads `readings`, reads no `sourced` and requires the residue keys K, N, release (record 2199 items 2 and 3; the ledger's source row); LAWFUL when... |
| `tests/test_toward_nature.py:109` | the Boss's records 2204 and 2206 (2026-09-26): a giving lowers the live M in the wall W = 3 Q M while n stays, so the moving emitter speeds up and the mirror... |


## The owners

One owner per area (`tools/owners.json`); the arbiter is Boss.

| owner | areas |
| --- | --- |
| Nature24 | `src/event_universe/loader/`, `docs/ENGINE.md` |
| Main Loop | `src/event_universe/core/`, `src/event_universe/events/detector_law.py`, `law/step.json`, `src/event_universe/retention.py`, `tools/run_inputs.py`, `tools/record_shipped_worlds.py` |
| Mathematician | `docs/ALGEBRA.md`, `tools/body_generator.py`, `src/event_universe/features/feed/`, `src/event_universe/features/induction/`, `src/event_universe/features/recoil/` |
| Mathematician 2 | `src/event_universe/features/counts_line/`, `src/event_universe/features/hold/`, `src/event_universe/features/spins_step/`, `src/event_universe/features/receive/`, `src/event_universe/features/self_source/` |
| Paper Writer | `paper/`, `tools/check.py`, `tools/every_pull_request.txt`, `tools/engine_gates.py`, `tools/merge_base.py`, `tools/owners.json`, `tools/ownership.py`, `tools/record_code_shape.py`, `tools/tests_shape.py`, `tests/bodies.py`, `tests/running.py`, `tests/worlds.py`, `tests/shipped_worlds.json` |
| Boss | `docs/HIGHLIGHTS.md`, `skills/`, `AGENTS.md`, `README.md`, `CONTRIBUTING.md` |


## The shipped worlds

22 worlds under `examples/events/`, each replayed bit for bit on every pull request that runs a world (`tests/shipped_worlds.json`).

| world | ticks | intervals recorded |
| --- | --- | --- |
| `examples/events/dark_body/bright.json` | 15156 | 200 |
| `examples/events/dark_body/dark.json` | 2400 | 200 |
| `examples/events/massive_record/boxed_clock_side_20_at_rest.json` | 3000 | 200 |
| `examples/events/massive_record/boxed_clock_side_20_moving.json` | 9500 | 200 |
| `examples/events/massive_record/boxed_clock_side_28_at_rest.json` | 3000 | 200 |
| `examples/events/massive_record/boxed_clock_side_28_moving.json` | 9500 | 200 |
| `examples/events/massive_record/deep_well_clock_at_rest_40.json` | 3500 | 200 |
| `examples/events/massive_record/deep_well_clock_speed_third_40.json` | 9500 | 200 |
| `examples/events/massive_record/light_clock.json` | 4800 | 1500 |
| `examples/events/massive_record/muon_moving_clock_at_rest_14.json` | 20500 | 200 |
| `examples/events/massive_record/muon_moving_clock_speed_third_14.json` | 20500 | 200 |
| `examples/events/point_emitter/point_chain.json` | 70992 | 200 |
| `examples/events/point_emitter/point_light_clock.json` | 35304 | 3000 |
| `examples/events/toward_nature/bending.json` | 5600 | 200 |
| `examples/events/toward_nature/lorentz_moving.json` | 3600 | 200 |
| `examples/events/toward_nature/lorentz_moving_long.json` | 5966 | 200 |
| `examples/events/toward_nature/lorentz_rest.json` | 3600 | 1500 |
| `examples/events/toward_nature/lorentz_rest_long.json` | 8206 | 200 |
| `examples/events/toward_nature/redshift_bottom.json` | 6534 | 200 |
| `examples/events/toward_nature/redshift_bottom_long.json` | 10558 | 200 |
| `examples/events/toward_nature/redshift_top.json` | 6150 | 200 |
| `examples/events/toward_nature/redshift_top_long.json` | 9598 | 200 |
