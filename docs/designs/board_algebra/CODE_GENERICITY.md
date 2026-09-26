# Code genericity review: the engine on origin/emitter-click

Reviewer: read-only code review, 2026-09-25. Nothing tracked was edited.

- Code: `origin/emitter-click` at `952f745a` ("Names in the active code ..."), checked out as a
  detached worktree in the scratchpad.
- Contract: `docs/ALGEBRA.md` 9.18 to 9.28 on `origin/lab-tools-unification` at `783e3899`;
  AGENTS.md "Change boundaries" and "Monorepo"; the three tests (generic, vector, local);
  docs/HIGHLIGHTS.md 5.4 rows 1875, 1878, 1884/1895 (moving body), 1886 and 1899.
- Method: I read `events/detector_law.py` (the one-operator engine) in full. I read the
  detector-law parts of `events/world.py` (the loader), `events/run.py`,
  `tools/run_inputs.py`, `diagnostics/massive_record_margin.py` (the generator's iteration),
  and the two generators `examples/events/massive_record/make_worlds.py` and
  `examples/events/detector_law/make_worlds.py`. I also read the 47 detector-law input files
  and `examples/events/pins.json`.
- I ran probe scripts that mutate `light_clock_60.json` and load it. I ran the one command on
  `light_clock_60.json`, and the two property-test files (section 7).

## Verdict in one paragraph

The core of the one operator is generic. The rule (`_advance`), the flux reading, the
increment ladder, the per-detector cube click, the residue read from the law, the emitter's
click rule and the loader's integer checks all read world integers only. None of them
branches on a family name, a tool name or an experiment name. The engine and the input
files are still **not completely generic**, for five reasons:

1. The law's path still branches on the family **kind** (the pair's `den > num`). This makes
   the coupling asymmetric for a matter emitter.
2. The retired ray law is the loader's **implicit default**. The loader requires ray-law keys
   in every file and silently ignores many others.
3. Three retired mechanisms still run in the law's path: `ramp` (an acceleration), `cavity`
   (a write outside the law) and the flat born pair (retired in favour of the born train).
4. The input stamp covers only the seeded profiles. The emitter's click threshold `norm` and
   the whole material and detector layout can change while the file still loads LAWFUL.
5. No body can have a name, and the momentum wall uses a hard-coded scale.

The property tests pass (18 of 18). The only pinned experiment (`light_clock_60`) misses its
pin: its first click comes at interval 42 against the pinned 214 ± 1.

Grades: **BLOCKING** means it breaks genericity or the contract; **SHOULD-FIX**; **NOTE**.

---

## 1. Branches on a family name, kind, tool name or experiment name

No branch on a family, tool or experiment **name** exists in `src/event_universe/events/detector_law.py`
or in the detector-law parts of the loader. A grep for `"light"`, `"matter"`, `"mirror"`,
`"polariser"`, `"crystal"`, `"splitter"`, `"screen"` and similar names in `src/` finds none
in a comparison. The retired tables are refused under the detector law
(`detector_law.py:349-363`), and so are lamps. The branches on the **kind** remain:

| # | Where | Quote | Grade |
| --- | --- | --- | --- |
| 1.1 | `events/detector_law.py:1601-1611` (`step`) | `if self.families[live.family].massive_kind: ... if live.emitter is not None: self._advance(live)` then `continue` | **BLOCKING**. A record of a massive kind is advanced with no coupling term. Only records of light's kind (`den == num`) receive the blocks' source term and create responses (lines 1615-1631). A matter emitter's born records are therefore never coupled back. Its own record still receives from them, because `_receive` over `block.emitted` (lines 1583-1587) does not look at the kind. The coupling (g, G) becomes one-way for a matter emitter. This affects `matter_front_12`, `matter_waves_12` and `matter_waves_16` (emitter family `source`, which births `matter`). ALGEBRA 9.18 (4) item 1: "no branch on the kind exists". |
| 1.2 | `events/detector_law.py:1276` (`_advance`) | `booked = not self.families[live.family].massive_kind or live.emitter is not None` | SHOULD-FIX. Whether a record books flux and can click is decided partly by kind. The structural half is lawful: a body's own record and the responses are never on a ladder. The kind half should go. |
| 1.3 | `events/detector_law.py:1060`, `1650`, `1663` | `if self.families[live.family].massive_kind and live.emitter is None: continue` and `if not ...massive_kind: value += ...` | SHOULD-FIX (1060: the inverse step has the same asymmetry as 1.1). NOTE for 1650 and 1663: the probe and `mode_axis` readings sum light's kind only. These are GameBoard readings, not the law. |
| 1.4 | `events/world.py:1123` | `return self.pair[1] > self.pair[0]` (`massive_kind`) | NOTE. The kind is derived from integers, never declared. That is right. Everything in 1.1 to 1.3 hangs on it. |
| 1.5 | `events/world.py:2302` (`_kind_faces`), `1828-1833` (`kind_periodic`) | `if pair[1] == pair[0]: ... return None` (light reads the world's `boundary`); a massive kind is `every axis periodic by default` | **BLOCKING**. The faces are per family, and the default depends on the kind. The decision of record 1875 is "one border for every family; main's faces per family retire at regeneration" (ALGEBRA 9.18 (2)). 33 of the 47 files still declare `faces`. |
| 1.6 | `events/world.py:3467-3508` (`_block`) | `if family.massive_kind: ...well / barrier / cavity... else: ... light's kind is no gap ... clock_keys refused` | NOTE. These are load checks, not the law. "Light cannot be a body" is derived in 9.18 (1), and a load check may read the pair. |
| 1.7 | `examples/events/massive_record/make_worlds.py:153-156` | `if any(block.get("family") == "source" for block in blocks): families.append({"name": "source", ...})` | SHOULD-FIX. This branches on a family name in the generator. It is not in the law's path, but the generator should take its families from the declaration. |

## 2. Hard-coded physical numbers that should come from the input file

| # | Where | Quote | Grade |
| --- | --- | --- | --- |
| 2.1 | `events/detector_law.py:429`, `events/world.py:350,366`, `world.py:3590` | `wall = 3 * LABEL_SCALE * world.width * entry.amount`, `Q = 64`, `LABEL_SCALE = Q` | **BLOCKING**. A body's momentum wall is built from a constant Q = 64 and from the stock `amount`, which doubles as the body's mass. Record 1885 and 9.24 make the momentum an integer of every entry, and a moving body a packet carried by its character. Nothing in the file declares Q. |
| 2.2 | `events/world.py:893`, `3518` | `BLOCK_SEED = 1 << 20`, `seed = BLOCK_SEED` | **BLOCKING** (implicit default). A block with no `seed` gets a flat seed of 2^20. A flat seed is not a mode, and the loader admits it on a non-emitting well. My probe added a well of side 3 with no seed: LAWFUL. Record 1875: "nothing else nonzero", the initial state is the sum of the occupied modes. |
| 2.3 | `events/world.py:5562` | `face_depth = _integer(obj.get("face_depth", 1), ...)` | SHOULD-FIX. The face slab defaults to depth 1, while 9.25 (10) and 9.27 (B)(5) ask for "a face slab as deep as the train". All 47 files use the default. |
| 2.4 | `events/world.py:5520` | `phase_steps = _integer(obj.get("N", 64), ...)` | SHOULD-FIX. The born pair and the born clock depend on N, and N silently defaults to 64. |
| 2.5 | `events/world.py:3654` | `if residues < 500:` | SHOULD-FIX. The birth cell's richness threshold is a bare number in the loader. It is a load check, but its source should be named as a constant with its derivation. |
| 2.6 | `events/world.py:3587`, `diagnostics/massive_record_margin.py:57-58` | `margin = obj.get("margin", MARGIN_KINDS[0])`; `FACE_EXTENTS = {pin: 2.0, control: 1.0}`, `SIDE_EXTENTS = {pin: 4.0, control: 2.0}` | SHOULD-FIX. A per-world label ("pin" or "control") picks a margin threshold, with "pin" as the default. See also 5.3. |
| 2.7 | `events/detector_law.py:83`, `85` | `UNIT = 1 << 20`; `DEFAULT_TRAIN = 32` | NOTE. `UNIT` is used only as the `unit` field of the click line. `DEFAULT_TRAIN` is dead (see 3.x). |
| 2.8 | `events/world.py:856`, `5187` | `MOST_FAMILIES = 3`, `DETECTOR_SIDE = 3` | NOTE. These are the owner's decisions (records 1875 and 1899), rightly constants of the loader. |

## 3. Leftovers of retired mechanisms

| # | Where | Quote | Grade |
| --- | --- | --- | --- |
| 3.1 | `events/world.py:5569`, `events/run.py:103-106`, `events/detector_law.py:5-6` | `detector_law = obj.get("detector_law", False)`; `DetectorLawSimulation(world, ...) if world.detector_law else NatureBeamSimulation(...)`; "beside the ray law as built, which stays the default" | **BLOCKING**. The retired ray law (tables `read/measure/rerelease/pass/become`, lamps with `rate`/`wheel`/`train`/`own_grace`, the phase circle, suspension) is still the loader's and the runner's **implicit default**. 119 example worlds (64 with tables, 57 with lamps) still run on it, through `events/engine.py`, `nature_beam.py`, `measured.py`, `meeting.py` and `amplitude.py` (about 11,000 lines). ALGEBRA 9.18 and 9.21 retire the tables and the lamp form, and AGENTS.md forbids an implicit default. |
| 3.2 | `events/detector_law.py:597-607` (`_momentum_now`); `world.py:3585-3586` | `ramp = block.definition.ramp ... return [component * elapsed // ramp ...]`; `ramp = 0 if "ramp" not in obj else ...` | **BLOCKING**. `ramp` and `start` are an acceleration inside the law's path. Records 1884 and 1895 say "no acceleration during a run", with a moving body "already moving at interval 0". The loader admits `ramp` (probe: LAWFUL), and 8 example files use it (`moving_20`, `moving_28`, `sagnac_k3`, `cavity_24_moving`, `deep_well_k3_40`, `layer_pin_k3_14`, `redshift_k3`, ...). A ramp also rescales the remainder mid-run (`_advance`, line 1289-1291). |
| 3.3 | `events/detector_law.py:1591-1593` | `if block.definition.cavity: block.own.now[~block.mask] = 0; block.own.remainder[~block.mask] = 0` | **BLOCKING**. This is a write to the state every interval that is neither the law's advance nor a click or birth. ALGEBRA 9.17 says the only operation is the click. It is admitted on any massive body, including an emitter (probe: LAWFUL), and 5 example files use it. |
| 3.4 | `events/detector_law.py:893-895` (`_emit`); `world.py:3737-3760`; `massive_record/make_worlds.py:289-290` | `live.now[block.mask] = emitter.born[0]`; `born must be [now, before] ... before = -now`; `emitter["born"] = [level, -level]` | **BLOCKING**. A birth writes the flat born **pair** on every cell of the body. ALGEBRA 9.17 (6a), "THE BORN TRAIN, THE ONE FORM OF A BIRTH", retires that form: "`born` has this one form, the profile, and the two-integer form is refused with this reason". It also requires the flux-sign check along **K** and the norm T of the born record "written beside the profile and checked at load". None of that exists. This is the fault behind the light clock's MISS (section 7). |
| 3.5 | `events/detector_law.py:958-1011` (`_block_clock`) | `if block.previous_sum <= 0 < total: block.count += 1 ... "event": "click"` | SHOULD-FIX. A second "click" is written to the record: a sign crossing of the body's summed rows, not the click rule. Its count also stamps the `clock` of every click line at a set bound to a block (lines 1368-1371, 1540-1557). Under the measurement rule a click is only a detector's. This one should be renamed as a labelled GameBoard reading, or removed. |
| 3.6 | `events/detector_law.py:85, 99-148, 1014-1018, 1255-1264, 1314-1316, 1598-1600` | `DEFAULT_TRAIN = 32`; `LiveRecord.lamp`, `train`, `period`, `arms`, `mask`, `arm_done`; `_phase(...)`; `_half_space(...)` | SHOULD-FIX. This is dead machinery from lamps and arms. `_phase` and `_half_space` are never called, `arm_done` is never set, `mask` is always None, and `train` is always 0. |
| 3.7 | `events/detector_law.py:1-60, 86-97, 203, 323-327` | module docstring: "A measured event with a lamp INSERTS ... the lamp's train ... the Node's amplitude is taken"; comment "The receiver's take ... the declared pair [-15, 56]"; "the block's grace for its emitted records" | SHOULD-FIX. The code's own documentation describes the retired lamp, train, take, grace and sponge. |
| 3.8 | `events/detector_law.py:1488-1505`, `224-241` | click line `"taken_by_emitter": 0`, `"windows": []`, `"node": []`, `"momentum": [0, 0, 0]`; `Ledger.taken_by_emitter`, `closed_after_click` | NOTE. These are retired fields kept "for the readers' form". |
| 3.9 | `examples/events/detector_law/make_worlds.py:340, 659-671, 736-740` | `def lamp(...)`, `MATTER_TRAIN = 8`, `MATTER_RATE = [1, 2]`, `OWN_GRACE = 70`, `REDSHIFT_GRACE`, `SAGNAC_GRACE`, `def graced(...): "HISTORY ... nothing written"` | SHOULD-FIX. The generator still carries the retired train, rate, grace and lamp as live constants and calls (`graced(...)` at 786, 823, 857). |
| 3.10 | `events/world.py:894-962` (`LAMP_KEYS`: `rate`, `wheel`, `own_grace`, `train`, `residue_order`, `residue_seed`) | | NOTE. These are refused under the detector law (probe: a lamp is REFUSED; `emitter.wheel` is REFUSED). They live on only for the default ray law (3.1). |
| 3.11 | A declared residue, take or wheel | probes: `take` REFUSED, `emitter.wheel` REFUSED, `emitter.train` REFUSED, a top-level `residue` REFUSED | Conforms. The residue is read from the law (`residue_of`, `detector_law.py:730-742`). |

## 4. Places where composing bodies is not generic

| # | Where | Quote | Grade |
| --- | --- | --- | --- |
| 4.1 | `examples/events/massive_record/make_worlds.py:366-573`, `examples/events/detector_law/make_worlds.py:391-925` | `def worlds(): out["rest_20"] = world("rest-20", "CONTROL", [48, 48, 48], ...)`, `def two_slits()`, `def bell(...)`, `def malus(...)` | SHOULD-FIX. The worlds are hand-written per experiment in Python, with per-experiment constants (`TWO_SLITS_OPENINGS`, `SAGNAC_CHAIN`, `LIGHT_CLOCK_TICKS`, ...). There is no generic generator that takes 9.27 (B)'s list (board and families, material regions, bodies with records, detectors and faces, births, size check, stamp and pins) and writes the file. The per-body step is generic (`seed_on_the_mode`, `mode_profile`, `iterated_mode`), and bodies are generated one at a time and placed, not regenerated. |
| 4.2 | `diagnostics/massive_record_margin.py:401-411` (`iterated_mode`) | "The block alone in its medium on the world's own board (the family's pair everywhere, the block's pair on its cells)"; `num = np.where(cells, definition.pair[0], family.pair[0])` | SHOULD-FIX. 9.27 (B)(3) asks for each body to be "generated alone on the final board **with every material region in place**". The generator puts in place only the body's own pair, not the barriers or other material regions of the same family. The current files are safe only because their material regions (light's walls, mirrors) are of another family than the seeded bodies. |
| 4.3 | `examples/events/detector_law/make_worlds.py:279-296` (`wall_line`), `two_slits.json` | "A wall of the declared depth: one block per Node" | SHOULD-FIX. The slit wall is 500 one-cell bodies, although bodies with extents exist (item 23). 9.27 (B)(2) says every material region is a box with extents. Loading also costs O(B^2) because `_write_pair` loops over every other block (`detector_law.py:559-573`). |
| 4.4 | `examples/events/detector_law/make_worlds.py:264-277, 315-325`; `massive_record/make_worlds.py:576-592` | `document["measured"].append(body(position, family, [[-1, 0, 0]]))` for every detector Node | SHOULD-FIX. Every detector cube is built on top of ray-law measured events ("receiver bodies" with `directions`, `fixed`, `amount`). A click hands content to them (`detector_law.py:1480-1484`). 9.27 (B)(5) says "every detector a cube of free Nodes". two_slits carries 603 such events and matter_waves 369. |
| 4.5 | `tools/run_inputs.py:59-69` vs `events/run.py:70-84` and `tools/preflight_worlds.py` | the one command: `parse_nature_beam_world` then `DetectorLawSimulation`; the runner also runs `check_margins`, `profile_check`, `check_body_conditions` | SHOULD-FIX. Three entry points give three different LAWFUL verdicts. The one command skips the margin, composition and board-size checks of 9.27 (B)(4) and (7), which the runner makes. |
| 4.6 | `events/detector_law.py:1615-1631` | a coupled block makes one response record (a dense board array) per light record | NOTE. This is a host decomposition of the linear coupling. The coupling has no declared family: every coupled body couples to every record of light's kind. 9.18 (4) item 7 makes the families a body couples to its declared data. |
| 4.7 | `events/world.py:1309-1345` vs `3597-3610` | two ladders: the block's `receiver` (one name) and the emitter's `receiver` (a list) | NOTE. Two forms of one mechanism. |

## 5. The input-file schema

The engine **reads** a small generic set: `shape`, `boundary` (per axis `open`, `periodic`
or `closed`), `families` (`name`, `quantum`, `pair`, `phase_per_link`, and `faces`, see 1.5),
`measured` (per body `position`, `family`, `amount`, `momentum`, `side` or `extents`, `pair`,
`coupling`, `seed` with `clock`, `emitter`, `receiver`, `cavity`, `ramp`, `start`, `margin`),
`detectors` (`name`, `positions`, `block`), `face_depth`, `width`, `N`, `amplitude_bound`,
`ticks`, `input`, and the diagnostics `probes` and `mode_axis`
(`grep world\.` in `detector_law.py`). The schema has no per-experiment key such as
`bell_setting` or `slit_width`. It is not the contract's one schema, for these reasons:

| # | Finding | Evidence | Grade |
| --- | --- | --- | --- |
| 5.1 | Ray-law keys are **required** in every detector-law file although the engine never reads them | probes: without `law` REFUSED ("declares `law`: `beam`"), without `K` REFUSED, without `release` REFUSED, without `model_id` REFUSED; every file carries `K: 1073741824`, `release`, `suspension`, `directions: []`, `age_bound`, and per body `phase`, `fixed` | **BLOCKING** (see 3.1): the file format is the ray law's. |
| 5.2 | Keys of other models are **admitted and silently ignored** | probes: `optical: 1`, `atom_level`, `meeting`, `drive_b`, `flow_link`, `centred_step`, `massive_rows`, `action`, `suspension` all LAWFUL, and `DetectorLawSimulation` reads none of them; detector `threshold: 999` LAWFUL and unread; `fixed: true` with `momentum [64, 0, 0]` (sagnac_k3) moves anyway | SHOULD-FIX. What a file declares is not what the run does. The detector law should refuse every key it does not read. |
| 5.3 | A per-world label changes the checks | `margin: "pin"` or `"control"` picks the margin extents (2.6); a profile seed is admitted "only with margin declared" (`world.py:3525`) | SHOULD-FIX. |
| 5.4 | A body has **no name** | probe: `measured[0].name` REFUSED "unknown keys: name"; bodies are `measured[<n>]` | SHOULD-FIX. The contract's tool is "material integers, momentum K, an optional birth and a name" (record 1875; 9.27 row "What a lab tool is"). |
| 5.5 | Tools the contract lists but the schema cannot express | no label matrix or polariser axis; no birth triggered by an arriving record (crystal); no rank-2 record; no push with declared pushing families (9.18 (4) item 7); no `hypotheses` key (9.27 (D)) | NOTE. These are owed, not non-generic. |
| 5.6 | Two keys for one thing | `momentum` (per body) plus `ramp`/`start`; `side` or `extents` | NOTE. |
| 5.7 | Pins | `examples/events/pins.json` holds one pin (`light_clock_60`, `first_click` 214 ± 1). The reader in `run_inputs.py:83-106` knows only `count` and `first_click`, not the fringe, centroid, ratio or visibility pins of 9.22 (8). None of the 18 placed experiments of 9.22 (8) exists as a detector-law input file, and `two_slits.json` is not the table's placement. | NOTE. |

## 6. Anything kept at a Node beyond its events

| What | Where | Allowed? |
| --- | --- | --- |
| Each record's `now`, `before` and the rule's own `remainder` per Node | `LiveRecord`, `_advance` | Yes: the record's rows and the rule's remainder. |
| The pair arrays `kind_num` and `kind_den` per family per Node | `detector_law.py:397-402`, `_write_pair` | Yes: a tool's material integers. They move only with a body's hop. |
| `cell_index` per Node (detector, body or face membership) | `detector_law.py:305` onward | Yes as HOST bookkeeping. The law never reads a Node's value through it; it chooses the Ports of a cube. |
| Per record, per cell: `pointers`, `absorbed`, `total`; per body: `drive` accumulators with remainder, `offer` (C), `residue_pending` | `LiveRecord`, `Block` | Yes. They are per record or per body, not per Node. `total` and `offer` are the click rule's own C, and `drive` is the push's accumulator with its remainder (9.18 (4) item 7). |
| `Block.count`, `previous_sum`, `cycle_*`, `new_cycle`, `rung_counts` | `detector_law.py:188-222, 958-1011` | NOTE: a per-body register of the retired block clock (3.5). It is not per Node, but it is state the law does not need. |
| `cavity`'s zero write outside the body | `detector_law.py:1591-1593` | **Not allowed**: an act on Nodes that is not the law (3.3). |
| The per-record dense arrays | whole board per record, plus one response per (light record, coupled body) | NOTE (host cost). The model's storage per Node grows with the number of live records crossing it, which is inherent to records. The host keeps every record over the whole board, and the property test bounds the host cost only on its small world. |

No register, draw or residue is kept at a Node beyond the rule's own remainder. The one
violation is `cavity`.

## 7. The property tests and the one command

- `.venv` of the repository lacks `scipy`, a declared dependency in `pyproject.toml:14`.
  `tests/test_initial_state.py` then fails at collection (`ModuleNotFoundError: scipy`, through
  `diagnostics/massive_record_margin.py:44`). I ran the tests in a scratch venv with
  numpy 2.5.3, scipy 1.18.1 and pytest:
  `pytest tests/test_board_properties.py tests/test_initial_state.py` → **18 passed in 25.0 s**:
  - 10 board-property tests (8 functions, the host-cost test parametrized by side): equivalence under the cube group, translation on the torus,
    conservation between clicks, reversibility except the click, locality, only the click
    reads, bounded host cost per Node, the same input gives the same output.
  - 8 initial-state tests: lawful generated world, refusal off the mode, clock refusals,
    at most three families, bodies whole and disjoint, the six-neighbour read, the stamp,
    the iterated generator.
  - Coverage NOTE: the property world plants one light record and has one well at rest. It
    exercises no birth, no moving body, no matter emitter (1.1) and no cavity or ramp.
- The one command on `light_clock_60.json`
  (`PYTHONPATH=src python tools/run_inputs.py --pins examples/events/pins.json ...`):
  - LAWFUL, 64 clicks at `at_a`.
  - The first click comes at interval **42** against the pin 214 ± 1: **MISS**. The next
    clicks are at 69, 75, 91, 107, ..., so records click on the outgoing pass, before any
    return from the mirror 60 Links away.
  - This is the born-pair fault of 3.4, which ALGEBRA 9.17 (6a) already diagnosed. The
    engine "works" only in the sense of running. The one registered experiment does not
    match.
- Loader probes on `light_clock_60.json` (each loads **LAWFUL** with the file's original
  `input` stamp):
  - the emitter's `norm` divided by 1000 (the excited record's click threshold T);
  - `period` set to 5 (unread);
  - the mirror moved from x = 672 to 640;
  - the mirror's pair changed to [1, 9];
  - the coupling changed;
  - the stock set to 1;
  - light's `phase_per_link` changed, so the born pair no longer matches the born clock;
  - `ramp` and `momentum` added;
  - `cavity: true` on the emitter;
  - a flat-seed well added.

  The stamp (`world.py:4984-5058`) hashes only the seeded profiles, their clocks and the
  born pair. **BLOCKING** for "the input file is checked LAWFUL/REFUSED" (record 1886):
  the integers that set the click's cadence (`norm`) are neither hashed nor recomputed nor
  checked. Changing the material or detector layout needs regeneration but is not caught.
  REFUSED as expected: 4 families; a lamp; a changed `born`; a declared `take`, `wheel`,
  `train` or top-level residue.

## Summary of grades

- **BLOCKING (9)**:
  - 1.1: the kind branch that makes a matter emitter's coupling one-way.
  - 1.5: faces per family, contrary to one border.
  - 2.1: the Q = 64 wall, with the stock as mass.
  - 2.2: the implicit flat seed 2^20.
  - 3.1: the retired ray law as the implicit default, whose keys are required (5.1).
  - 3.2: `ramp` (acceleration).
  - 3.3: `cavity` (a write outside the law).
  - 3.4: the flat born pair instead of the born train.
  - The stamp and load check leave `norm` and the layout unchecked (section 7).
- **SHOULD-FIX**: 1.2, 1.3, 1.7, 2.3 to 2.6, 3.5 to 3.7, 3.9, 4.1 to 4.5, 5.2 to 5.4, and
  the missing `scipy` in `.venv`.
- **NOTE**: 1.4, 1.6, 2.7, 2.8, 3.8, 3.10, 4.6, 4.7, 5.5 to 5.7, the host cost of the dense
  records, and the property test's coverage.
- **Conforms**: the rule `_advance` (G, then D with the remainder kept, then T, one division
  per row per interval); the flux reading and the per-detector cube click through outer
  Ports (`_flux_ports`); the increment ladder (`_ladder_click`, 9.25 (2)); the residue and
  wheel from the law (`residue_of`); the emitter's click rule (`_excitation_rung`, 9.17 (7)
  (f)); the one deletion at a click; tables, lamps, take, grace and declared wheel refused;
  at most three families; bodies whole and disjoint; the profile's residual checked in
  integers; the generator as the operator iterated with its stop; one output file per input.
