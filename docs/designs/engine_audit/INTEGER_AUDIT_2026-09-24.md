# The engine's integer audit: no float at run time, no formula in the engine, every rule one of the six verbs, every read local (the Engine Architect Auditor, 2026-09-24, docs only)

The model owner's word of 2026-09-24 02:20Z, as the Boss quoted it: an
architect is to see "that the code is clean and orderly, no formulas in the
engine, and that it is entirely algebraic with integers, as we say". This
page is that reading, docs only: no engine line, no test, no world file
changed; every violation is reported here and fixed by nobody here (the
builder owns the engine). The scope is the chief physicist's four items,
(a) to (d), one table each below, and a last section that answers the
owner's question item by item with the counts.

**Read.** `origin/main` at 324244f0f19cb4819581e4305b215fa00ba23d7e
(PR #1089), the whole of `src/event_universe/`; and, as a second pass,
the builder's branch `origin/detector-law-build-2` at
8625f81608d3ca8ce004110fb07c687d4eba3e8c (the fold of PR #1076's main into
the build, then the splitter, the matter lamp's take and the world key
`wheel`), because the GO's engine is that branch merged. On the branch
three files differ from main: `events/detector_law.py` (+329 lines),
`events/world.py` (+110), `core/phase.py` (+40); every other module of
`src/event_universe/` is byte for byte main's. Every line number below is
the branch's for those three files and main's for every other file (the
two heads agree there). The date is 2026-09-24; the auditor's session is
`session_01KqqhgDtoygptxGb9dGTVvb`.

**Not repeated.** Yesterday's audit,
[docs/designs/system_algebra/AUDIT.md](../system_algebra/AUDIT.md) (PR
#1050, read at 05e9f10), gave one row per component of the ray law's
modules. Those modules (`nature_beam.py`, `engine.py`, `measured.py`,
`meeting.py`, `amplitude.py`, `core/`) are byte for byte the same at
324244f0 as at 05e9f10 (checked with `git diff --quiet`), so their
findings are carried here at the same lines with today's verdict and are
not re-derived row by row. The new reading is `detector_law.py` (1408 lines
on main, 1737 on the branch), the world parser's additions since 05e9f10
(528 lines on main, 110 more on the branch) and `core/phase.py`'s
`nearest_phase`.

**The method.** The algebra gate `tests/test_integer_algebra.py` was run on
both heads (39 tests, all pass at both: no float literal, no true division
`/`, no forbidden import, `math` only `gcd` and `isqrt`, every numpy array
`int64`, every root in its inventory). Beyond the gate, a syntax-tree scan
of the nine physical modules listed every power `**`, every `divmod`,
`round` and `float` call, every float constant and every comparison of a
name against a family word (the scratch script is not kept: it repeats the
gate's method and adds nothing reusable). Then the reading: every function
of `detector_law.py` on the branch, the parser's additions, the phase
module's addition, and the lines yesterday's findings named. No world was
run; the one load beyond the gate's parse was a smoke load of the eleven
moving-block worlds under `examples/events/massive_record/` at the end,
to put a number on row (a)-15's severity (their walls against the bound;
no interval stepped).

**The verdicts.** CLEAN (one of the six verbs on bounded integers, local,
declared); VIOLATION (fails one of the four scope items as written, with
a severity: HIGH, a number a pin reads can change or an integer can wrap
silently; MEDIUM, a rule fails one of the three tests as written; LOW, a
declaration or a label missing, no number changed); DECLARED INPUT (a
constant of the world formed at load from declared integers, or a
load-time refusal); DIAGNOSTIC ONLY (a reading of the GameBoard labelled
so, read by no rule; or the host's reading the design admits); HISTORY (a
module the active engine does not run). "Carried" marks a finding of
yesterday's audit re-verified at the same line today.

**Notation.** N is the phase circle's number of steps; W the wheel (the
rung's denominator); Q = 64 the label scale; S the width; M a body's
content; **P** the block's momentum vector; W_d = 3 Q S M the drive's
wall; [num, den] a record kind's pair on the six-neighbour term; g = [g_n,
g_d] and G = [G_n, G_d] the coupling's two rational pairs (the receive and
the source); L the least common multiple of the blocks' G_d; C and S the
cosine and sine tables of the circle at the scale 256; k the clock's whole
step of an interval; A = 2^40 the amplitude bound of the load check; a_now,
a_before and r a record's row at a Node (its two levels and its remainder).
The six verbs are ALGEBRA.md chapter 2's: (T) the translation, (B) the
bilinear form, (G) the group-ring addition, (P) the permutation, (E) the
evaluation, (D) the division with the remainder kept and the comparison.

---

## (a) No float, root or transcendental at run time in the interval's path

| Row | File and lines | What the line does | Verdict | The fix, if a violation |
| --- | --- | --- | --- | --- |
| (a)-1 | `tests/test_integer_algebra.py`, the gate, run at 324244f0 and at 8625f816 | no float token, no `/`, no `random`, `fractions`, `decimal`, `cmath`, `statistics`; `math` only `gcd` and `isqrt`; every numpy dtype `int64`, `bool` or `object`; no `np.sqrt`, `mean`, `sin`, `cos`, `linalg`; a root only where the inventory names it | CLEAN at both heads (39 passed, 39 passed) | none |
| (a)-2 | `nature_beam.py:856-877` (`unit_label`), `:911-1005` (`direction_flight`), `:1007-1247` (`flight_triple`, `unit_energies`); `world.py:478` (`T_HEADING`), `scaled_label`, `column_scales`, `flight_bound`, `_covariant`, `_massive_families`; `meeting.py:arc_shift`; `engine.py:__init__` | twelve roots of the gate's inventory, each at load: the unit label, the flight table's T_D = isqrt(3 abs(**D**)^2 Q^2), a massive family's E'_D, the heading's resolution, the parser's bounds, the covariant identity's E' once | DECLARED INPUT (a declared rounding at load, ARCHITECTURE.md "The tables the engine carries") | none |
| (a)-3 | `amplitude.py:223-239` (`common_denominator`, `math.isqrt` at `:235`); `world.py:4041-4046` (`_same_class`, `math.isqrt(product) ** 2 == product` at `:4045`) | two predicates: is a ratio, is a product a perfect square; the root squared back and compared, no rounded number enters a reading | CLEAN (a comparison, verb D) | none |
| (a)-4 | `meeting.py:355-363` (`meet`) | `norm[index] = integer_root(t . t)` per met row per interval under the world key `meeting` (5 worlds under `examples/events/`) | VIOLATION, MEDIUM, carried (ALGEBRA.md 2.7's first run-time root, "the seventh verb, not admitted"; the gate lists it "AT RUN TIME"; HISTORY for the GO: no `detector_law` world declares `meeting`) | replace the norm by the square's ladder of comparisons on abs(**t**)^2 against the register's squares, as `split_ladder` does for the pushed row, or state the meeting under its own identity outside the law |
| (a)-5 | `nature_beam.py:3643-3701` (`square_ladder`, `split_ladder`), called at `:3770` in `momentum_pair` | the pushed row's wall T(**P**) = floor(sqrt((R^2 + 3 abs(**P**)^2) Q^2)) by two ladders of comparisons from the high bit down, per pushed row when **P** changes, under the key `optical` (53 worlds) | VIOLATION, MEDIUM, carried: no root primitive is called, but the floor of a square root is formed at run time by iteration (the docstring says "the same floor as the integer root, reached by comparisons alone"); ALGEBRA.md 2.7 names it the second run-time root; HISTORY for the GO (no `detector_law` world declares `optical`) | form T(**P**) at load for every momentum the world declares and every push the family table admits (a table per family, as the flight table), or declare the ladder as the rounding of the key `optical` in ALGEBRA.md 2.7 with its grain |
| (a)-6 | `world.py:568-602` (`body_weight`, `energy = integer_root(square)` at `:600`), called at `engine.py:693` in `_frame_all` | the moving body's gravity charge (w, Q S) with w = (E'^2 + 3 gamma **p** . **p**) // E', E' = isqrt((Q S M)^2 + 3 **p** . **p**), every interval for every moving body under `drive_b` (18 worlds) | VIOLATION, MEDIUM, carried (the third run-time root of yesterday's audit); and LOW, new: the gate's inventory reason for `("events/world.py", "body_weight")` says "at load", while `engine.py:693` calls it in the frame each interval, so the inventory's reason is wrong; HISTORY for the GO (no `detector_law` world declares `drive_b`) | form E' once when the momentum changes (a push) by the ladder, or read w from the covariant identity's E' kept on the record (`covariant_square`), and correct the inventory's reason line to "AT RUN TIME under `drive_b`" |
| (a)-7 | `detector_law.py:337` (`__init__`, the splitter's rows) | `root = integer_root(norm)` on the split's weights, refused unless `root * root == norm` (21, 20 against 29) | DECLARED INPUT (at load, a perfect-square predicate; in the gate's inventory) | none |
| (a)-8 | `core/phase.py:30-116` (`_fixed_cosine`, `_fixed_sine`, `phase_cosines`, `phase_sines`) | the tables C and S at the scale 256 by a fixed-point series at load, cached per N | DECLARED INPUT (the circle's tables, ARCHITECTURE.md) | none |
| (a)-9 | `core/phase.py:164-201` (`nearest_phase`, branch only) | the phase nearest to the pair (a_before, a_now) at an amplitude by the least residual over 2 N table entries, integer comparisons only | DIAGNOSTIC ONLY (DECLARATIONS.md section 14 item 5: "the phase reading of component 1 stays as a diagnostic (GAMEBOARD, the nearest angle) and is not the tables' input"; called by no rule: its callers are `detector_law.read_phase` and two tests) | none; keep it out of every rule (row (c)-19) |
| (a)-10 | `detector_law.py:839-856` (`_sine_table`, `_cosine_table`) | the tables S and C as `int64` arrays, C scaled to the amplitude unit 2^20 by the exact factor 2^20 / 256 | DECLARED INPUT (formed once) | none |
| (a)-11 | `nature_beam.py:502`, `:1291`, `:1304`, `:1323`, `:2593`; `detector_law.py:964`; `world.py:4110` (`_same_class`), `:4316` (`_massive_families`); `amplitude.py:129` | every `**` of the nine modules: integer squares (a bound's square, the driven steps' squares of the norm at birth, the reach's square) and the slot code's powers 3^k at load | CLEAN (a whole exponent on integers; no negative exponent, so no float) | none |
| (a)-12 | `nature_beam.py:699`, `:712` (`exact_phase`), `:1786` (`place_over_nodes`); `detector_law.py:1215` (`_split`) | every `divmod` of the nine modules: a Euclidean division with the remainder kept | CLEAN (verb D) | none |
| (a)-13 | `world.py:624`, `nature_beam.py:778`, `amplitude.py:228-229` | "sqrt" in prose only (docstrings) | CLEAN | none |
| (a)-14 | `diagnostics/massive_record_margin.py` (the whole module, 370 lines; `import math`, `RITZ_TOLERANCE = 1e-9`, a Lanczos iteration), called at `run.py:61` before the world runs | the margin rule of the massive record kind: the block's bound mode by a floating-point eigenvalue, the extent 1 / kappa, the margin per axis; a declaration below the margin refuses the run; every number printed and written into the run's record | DIAGNOSTIC ONLY (a HOST module at load, outside the interval's path, read by no state; the module says so) with one line to note: the refusal of a world, a load-time decision, depends on a floating computation with a tolerance, so whether a GO world runs is decided by a float; the state never reads it | none required; if the owner wants the load path integer too, declare the margin in Links per world (an integer the pins script prints) and let the module print its reading beside the declaration instead of refusing on it |
| (a)-15 | `detector_law.py` (no call of `checked_work` in the module: 0 hits); `world.py:2054-2066` (`_pair_bound`, at load: num x scale x 6 x A + 3 x den x scale x (A + 1) < 2^63 with A = 2^40), called at `:2089` for the kind's pair and at `:3214` for the block's pair with `receive[1]` as the scale | the rule's rows are `int64` arrays and the wall at run time is 3 x den x scale with scale = g_d x pair_d (`receive_scale`, `:657-661`), pair_d = W_d^2 - 3 **P** . **P** (`motion_pair`, `:567-578`); numpy's `int64` arithmetic wraps on overflow without an error; the load bound covers g_d but not pair_d (up to W_d^2 = (3 Q S M)^2), and no run-time comparison of a row against A exists | VIOLATION, MEDIUM (ARCHITECTURE.md: "check intermediates ... do not ... wrap overflow"; the working bound is the host's, TERMINOLOGY.md). Not HIGH: the smoke load of the eleven moving-block worlds under `massive_record/` (W_d = 192 at M = 1, pair_d = 2 or 13 after the gcd, g_d = 1 or 200) gives the rule's total at A = 2^40 between 54 and 63 bits, below the 64-bit bound in every one (the two `index_moving_k4` worlds at 63 bits, one bit under), and 19 to 36 bits at the declared seed; no GO world wraps today, and nothing checks the next one | extend `_pair_bound`'s scale at `:3214` to g_d x (W_d^2 - 3 **P** . **P**) at the block's declared momentum (and at the ramp's end, the same number), and add in `_advance` one host comparison per record per interval, `abs(nxt).max() <= AMPLITUDE_BOUND`, raising `OverflowError` naming the rule (the gate's `checked_work` for arrays) |

**(a) in one line.** No float, root or transcendental enters the interval's
path of the GO's engine (`detector_law.py`): 0 violations there. The ray
law carries its three known run-time roots (rows 4 to 6, MEDIUM, all under
keys no `detector_law` world declares). One new finding: the integer
bound of the dense rows is not checked at run time (row 15).

---

## (b) No physical formula in the engine: the rates and walls declared data, the engine branching on no family name or kind

| Row | File and lines | What the line does | Verdict | The fix, if a violation |
| --- | --- | --- | --- | --- |
| (b)-1 | `engine.py` (14 sites of `world.optical`, `world.drive_b`, `world.meeting`, `world.covariant_readings`, `world.centred_step`, `world.massive`, `world.atom_level`); `nature_beam.py` (6 sites); `run.py:93` (`world.detector_law`) | the engine branches on declared world keys (a value of the world file), never on a family's name; the syntax-tree scan found no comparison of a name against a family word in the nine modules (the three hits, `world.py:2298`, `:3536`, `:4666`, are `"massive" not in obj` and `"lamp" in obj`, key presence in the parser) | CLEAN, carried (ARCHITECTURE.md: "names must not select hidden physical equations") | none |
| (b)-2 | `world.py:2069-2113` (`_kind_pair`), `:2054-2066` (`_pair_bound`), `:3122-3290` (`_block`: `side`, `pair`, `coupling` {G, g}, `wheel`, `seed`, `absorbing`, `cavity`, `ramp`, `start`, `margin`, `emits`), `:3274` (the pace bound 3 **P** . **P** < W_d^2, a comparison) | the massive record kind's declarations: a family's pair, a block's well, the coupling's two pairs, the block's wheel, the pushing agent's ramp and start; each refused by name when malformed | DECLARED INPUT (the rule's rates and walls as data) | none |
| (b)-3 | `world.py:3758-3830` (`_detector_law_load_checks`, branch: the fan refused, the splitter's clock refused where S[k] = 0 at `:3799`, the arm's half-space refused on a periodic axis, the matter lamp's clock required); `:4640-4646` (the world key `wheel`) | load-time refusals under `detector_law`; W of the detector sets where no lamp declares a larger birth wheel | DECLARED INPUT | none |
| (b)-4 | `detector_law.py:86` (`DEFAULT_TRAIN = 32`), read at `:895` (`lamp.train if lamp.train is not None else DEFAULT_TRAIN`) | a lamp that declares no `train` inserts for 32 periods: a physical number supplied by the engine where the file names none | VIOLATION, LOW (AGENTS.md: "do not ... reintroduce an implicit default"; the same class as yesterday's parser defaults, row 1.7 there) | refuse a `detector_law` lamp without `train` in `_detector_law_load_checks`, one line naming the key, and delete the constant |
| (b)-5 | `detector_law.py:97-98` (`TAKE_NUMERATOR = -15`, `TAKE_DENOMINATOR = 56`), read at `:1142-1144` | the receiver's take, g(t + 1) = a_f(t) + k (a_f(t + 1) - g(t)) with k = [-15, 56] (the rounding of sqrt 3 - 2 at load), a rate of the law held as a module constant of the engine and applied to every receiver Node and every open face of every world | VIOLATION, LOW (the scope's (b) names "the take's pair" among the rates to be declared data; DESIGN.md section 5 names four receiver forms per object, "the world file names the form per object", and the engine carries one, applied everywhere; the number itself is right and a declared rounding) | move the pair to `world.py` beside `LIGHT_PAIR` as a named constant of the law read by the parser into a `take` field of the measured event and the world's faces (the same value for every object today, so no pin moves), and let a later declaration per object select the form |
| (b)-6 | `detector_law.py:1074-1081` (`_advance`: `grace = live.train + 2 * live.period`) | the cycle sentence's N_s, the intervals after the train during which the lamp's own Nodes take nothing of the record, is 2 periods, a constant of the engine | VIOLATION, MEDIUM (DESIGN.md section 5, "the cycle sentence": "N_s is the object's declaration (1.1; the build's 'grace' of two periods is a module constant to become it), not a constant of the law"; the design itself marks it as the number to become a declaration, and the code's comment says "the first build's grace") | add the key `grace` (or the design's name N_s, in periods) to the lamp's declaration in `world._lamp` (`:2461`), refused when absent under `detector_law`, and read `live.grace` in `_advance` |
| (b)-7 | `detector_law.py:567-578` (`motion_pair`), read at `:661` (`receive_scale`) and `:673` (`_receive`) every interval per block | the index in motion: the coupling's g carried as [W_d^2, W_d^2 - 3 **P** . **P**] reduced by the gcd, computed by the engine from the block's momentum each interval | VIOLATION, MEDIUM: a physical formula (the square of the Lorentz factor, gamma^2 = W_d^2 / (W_d^2 - 3 **P** . **P**)) owned by the engine and computed at run time, not declared data; ALGEBRA.md 8.5 admits it as "a COMPUTATION from the drive's count ... nothing new declared in motion", and 8.9's prediction 3 says the reading is "not covariant under either declaration": a hypothesis's number, formed in the engine; the generic test ("its special cases are values, not branches") is met, the "declared data" clause of (b) is not | form the pair once at load per block from its declared momentum (and once per ramp interval, a table of `ramp` entries, since the ramp is a declared schedule), stored on `BlockDefinition`, so that the engine reads a declared integer and computes no gamma; if the owner keeps it as the engine's, name it in ALGEBRA.md 8.5 as the one formula the engine forms in motion |
| (b)-8 | `detector_law.py:1090`, `:1279`, `:1394`, `:1435`, `:1445`, `:1458`, `:1484` (`self.families[live.family].massive_kind`, with `live.driven is None` at four of them) | the engine branches on the record's KIND (a block's massive record: taken by nothing, reads no Port, never completes, not probed, not read) at seven sites | VIOLATION, MEDIUM (the three tests, "Generic": "no family name or kind ... its special cases are values, not branches; the engine branches on no name"; ALGEBRA.md 2.8; the scope's (b) names "kind" explicitly). The branch is the same one everywhere: "is this record a block's own or a block's response"; `massive_kind` is derived from the pair (den > num), a kind | replace the seven branches by one boolean on `LiveRecord`, `taken` (true for a lamp's record of either kind, false for a block's own and a block's response), set once where the record is made (`_massive_record` `:533`, `_births` `:858`, `_block_births` `:687`), so the rule reads a value of the record and no kind; the probes and the mode reading select on the same value |
| (b)-9 | `detector_law.py:989-992` (`_phase`: (3 N / 4 + floor(age n / d)) mod N); `:895-907` (the train's ceiling of periods and its extension to the next zero crossing of the clock) | the clock's zero at 3 N / 4 (cosine 0 and rising) and the train's end at a zero, from the declared pair [n, d], N and `train` | CLEAN (a constant of the law's clock, DESIGN.md section 5; formed at the birth from declared integers) | none |
| (b)-10 | `detector_law.py:449-452` (`light_scale`: L, the least common multiple of the blocks' G_d, by `gcd` at load) | light's wall 3 L under the coupling, so that every light row divides once per interval | DECLARED INPUT (at load; ALGEBRA.md 8.5, "the one division") | none |
| (b)-11 | `detector_law.py:1032-1061` (`_neighbours`: on an axis of one layer the row itself twice, `total += 2 * a`) | the six-neighbour sum with the declared reading of a one-layer axis | CLEAN (DESIGN.md section 2's declared reading; verb G) | none |
| (b)-12 | `detector_law.py:517-531` (`_write_pair`), `world.py:3122-3200` (`_block` on light's kind: den > num, the (M) wall, no clock keys) | the block of light's kind: a lowered pair written at its cells and nothing else | DECLARED INPUT (a value at the cells, the same primitive) | none |
| (b)-13 | `detector_law.py:1006-1030` (`_shift`, `fill=0` beyond an open face of a massive kind), `:1021` (the wrap per kind, `kind_wrap`), `:384-393` (light's open face: the face's layer absorbing with the take) | the closed face: a massive kind's open face is a zero face (a mirror, the row beyond held at 0); light's open face is the sponge that does not read (booked as escaped) | DECLARED INPUT (the kind's `faces`, the world's `boundary`; DESIGN.md section 5, "a face of the board is one of the three forms too, declared") | none |
| (b)-14 | the rotation on the pair (the polariser's U_s acting on (a_before, a_now) by the linear form) | not present at 8625f816: `detector_law.py` holds no rotation, polariser or bar; the only action of a table on the pair is the splitter's turn t_ij per input (row (c)-6), which is the same linear form with one phase shift | not a verdict (nothing to read); noted for Reviewer 3 so that the component list of the order is complete | none |
| (b)-15 | `detector_law.py:1268-1285` (`_complete`: `energy * self.wheel < live.absorbed`, the record's motion left on the board below one rung of what the receivers hold) | the completion rule from W and the record's ledger | CLEAN as data (W declared) and the host's reading (row (d)-8) | none |

**(b) in one line.** The rule's rates and walls are declared data
(the pair, the coupling's two pairs with g_d folded into the wall, the
wheel, the clock's step) except three numbers the engine holds (rows 4 to
6) and one it computes from the state in motion (row 7); the engine
branches on no family name, and on the record's kind at seven sites (row
8). 5 violations: 3 MEDIUM, 2 LOW.

---

## (c) Every rule one of the six verbs, with its declared integers and its one division with the remainder kept

| Row | File and lines | What the line does | Verdict | The fix, if a violation |
| --- | --- | --- | --- | --- |
| (c)-1 | `detector_law.py:1074-1127` (`_advance`, the rule: `total = num x scale x S_6 - wall x a_before + r (+ the coupling's term)`, `nxt = floor_divide(total, wall)`, `r' = total - wall x nxt`, wall = 3 x den x scale) | the six-neighbour rule with the kind's pair: (G) the sum over the six neighbours, (T) the translation by minus 3 den a_before and by the remainder, (D) one Euclidean division by the wall with the remainder kept on the row, 0 <= r' < wall | CLEAN (ALGEBRA.md 8.1 and 8.5: one (D) per row per interval, g_d and G_d folded into the wall) | none |
| (c)-2 | `detector_law.py:1101-1104` (`_advance`: `live.remainder = live.remainder * scale // live.scale` when the wall's scale changes) | under a ramp the coupling's pair changes every interval (row (b)-7), and the row's remainder is rescaled to the new wall by a whole part, the sub-wall part dropped | VIOLATION, MEDIUM (TERMINOLOGY.md "Remainder: never discarded at run time"; the same class as `optical_turn`'s residue, row (c)-13; the vector test's "the remainder kept") | with row (b)-7's table the wall is a declared integer per ramp interval and the rescale is still needed unless the wall is one number for the ramp: declare the coupling's pair at the ramp's END for the whole ramp (one wall, the remainder never rescaled), the ramp acting on the momentum alone; if the owner wants the pair to follow the momentum, keep r on the old wall as a pair (r, wall_old) and add it to the next total as r x wall_new // wall_old with ITS remainder kept on the row |
| (c)-3 | `detector_law.py:1134-1156` (`_advance`, the take: `ghost = floor_divide(56 x a_f(t) + (-15) x (a_f(t + 1) - g(t)), 56)`, then `motion = ghost - g(t)`, `g(t) <- ghost`, `offer += motion x motion`) | the receiver's Port amplitude follows the free neighbour one way ((T) and (D) by 56); the offer arriving by the Port is the Port's motion squared ((B) with the identity matrix); but the division by 56 keeps no remainder: the Port holds g(t) only, and the part of the numerator below 56 is dropped every interval at every receiver Port and every open face | VIOLATION, MEDIUM (DESIGN.md section 5, "the Port's take": "the remainder of the Port's division by 56 stays on the Port as the rule keeps r (the vector test)"; the code drops it; the vector test as written fails, and the number the screens read, the offer, is the floor's) | keep one remainder array per take mask beside `live.ports[index]` (the Port's r, in [0, 56)), add it to the numerator before the division and store the new remainder after it, as `_advance` does for the row (the pins may move by the grain of 1 / 56 per Port per interval: to be re-read by the pins script before any run) |
| (c)-4 | `detector_law.py:1157-1176` (the pointer per cell: `live.pointers[cell] += offer`, `live.absorbed += offer`, the first rung `pointers[cell] x W >= norm`) | (G) the offers summed into the cell's pointer, (D)'s comparison on the wheel for the first rung; Python integers (`astype(object)`) | CLEAN (ALGEBRA.md 8.6: "the comparison W x (the pointer) >= (the record's norm), integers both") | none |
| (c)-5 | `detector_law.py:1178-1217` (`_split`: k = `by_clock(age - 1, n, d)`; per input Node the term w_ij x (L / R_i) x (a_now S[k + t_ij] - a_before S[t_ij]); per output `divmod(total + r_j, S[k] x L)`, the quotient added to the output Node's a_now, the remainder kept per output per record) | the splitter of the TABLE form: (T) the clock's whole step, (B) the integer matrix on the record's two columns with the sine table's entries, (D) one division per output per interval by the wall S[k] x L with the remainder kept, (G) the term added to the rule's value | CLEAN as verbs (DECLARATIONS.md section 14 items 1 to 3, the linear form, additive, the remainder carried); its reach is row (d)-4 | none here |
| (c)-6 | `detector_law.py:1195-1198` (`_split`: `common`, the least common multiple of the rows' roots, recomputed per record per interval) | the wall's factor L of the splitter, a constant of the declaration formed inside the interval's loop | CLEAN (an integer of the declaration; a host cost, not a physical one) | none required; form it once in `__init__` on the `Splitter` (a tidiness line for the builder) |
| (c)-7 | `detector_law.py:646-685` (`_coupled_term`, `_receive`, `_source`: the term 3 den x numerator x delta at the cells, delta the other record's first difference a_now - a_before; the massive row gains g_n x pair_n, light's row gains -G_n x (L / G_d)) | the coupling of ALGEBRA.md 8.5: (B) one entry of the declared matrix over the other record's two columns, both first differences, undivided; the one (D) is the rule's in `_advance` | CLEAN (8.5's "one division", g_d and G_d in the wall; the column order massive first then light, `step` `:1380-1424`, is 8.5's) | none |
| (c)-8 | `detector_law.py:580-631` (`_move_block`: per axis `by_drive(drive, P_a, W_d, at_most=1)`, x before y before z, a second Link in one interval lost to the earlier axis) | the block's step: (T) the accumulator gains P_a, (D) the count against the wall W_d with the remainder kept, at most one Link | CLEAN as verbs; LOW, carried: the per-axis tie of `engine._move` (yesterday's row 1.5, "a later axis whose drive reaches its D in the interval" loses its Link to the earlier axis) is built here too (`:589-595`), a declared tie in TERMINOLOGY.md "The cube group" but a Link lost, not a Link carried | none beyond yesterday's: carry the later axis's count to the next interval by leaving its accumulator uncounted (the count taken only on the first axis that fires, the others' accumulators untouched), which the code already does (`if count and not stepped`), so the only loss is the interval, not the Link: state that in the docstring |
| (c)-9 | `detector_law.py:555-565` (`_momentum_now`: P x elapsed // ramp until the ramp ends) | the ramp's momentum, the closed form floor(P t / ramp) of a constant rate | CLEAN ((T)'s closed form s(t) = floor(s_0 + r t), ALGEBRA.md chapter 2, the linear block) | none |
| (c)-10 | `detector_law.py:765-815` (`_block_clock`: the total record over the cells R, one count at the sum's crossing from at most 0 to above 0) | the block's clock: (G) over R, (D)'s comparison | CLEAN (MASSIVE_RECORD.md sections 4 and 6; the centre's value a diagnostic, written on the `block` line) | none |
| (c)-11 | `detector_law.py:817-837` (`_book_response`: the response's motion squared over the cells into light's pointer, the first rung at W stamped with the block's count) | the click of a body at W: (B) the motion's square on the cells, (G) into the pointer, (D)'s comparison on the wheel | CLEAN (ALGEBRA.md 8.6) | none |
| (c)-12 | `detector_law.py:858-987` (`_births`: the lamp's accumulator against its rate's denominator `:866-871`; u = (ordinal - 1) x wheel_n mod wheel_d `:875`; the norm as the sum of the driven steps' squares over the train `:958-966`) and `:994-1003` (`_drive`: the level C[phi] at the lamp's Nodes) | the birth: (T) and (D) the lamp's count, (T) on Z_W the birth's coordinate, (B) the norm at birth from the table's values, (E) the table entry at the clock's phase | CLEAN (a declared rounding at load in the table, evaluated) | none |
| (c)-13 | `nature_beam.py:3529-3552` (`reseed_flight`: "the crowd's carry on the old line dropped with the old line") and `:3972-4206` (`optical_turn`: the residue rescaled at every push, s' = s S_1(**P**') // S_1(**P**), "the sub-unit remainder dropped") | two remainders discarded at run time in the ray law, under `optical` | VIOLATION, MEDIUM, carried (yesterday's rows for both; HISTORY for the GO) | yesterday's: keep the carry as a pair on the row and add it at the new rate with its own remainder |
| (c)-14 | `meeting.py:234-246` (`register`: adv = (abs(**t**) + Q / 2) // Q) | the meeting's rounding at run time each interval | VIOLATION, LOW, carried (ALGEBRA.md 2.7: "NOT a torus operation ... its exact form acc += abs(t) on Z_(N Q)"); HISTORY for the GO | the exact form ALGEBRA.md names |
| (c)-15 | `nature_beam.py:1249-1327` (`collision_table`, the tie of the cyclic shift in Port order) | the collision's permutation (P) with an undeclared tie | VIOLATION, LOW, carried | declare the tie in ALGEBRA.md 2.4's line and TERMINOLOGY.md |
| (c)-16 | `detector_law.py:1409-1415` (`step`: for a record a block sources, `added = floor_divide(term, 3 den L)` and `live.norm += sum(added^2)`) | the sourced record's norm grows by the whole part of the source term squared: a second division of the same term, made for the ledger with its remainder dropped, beside the rule's one division in `_advance` (which keeps it) | VIOLATION, LOW (a second (D) on the same term, the remainder not kept; the norm sets the first rung, a click's time) | take the norm's increment from the rule's own quotient: record the part of `nxt` the source term contributed by advancing the row once without the term on the host's copy, or declare the norm of a sourced record as the block's own ledger (the sum of its emitted quanta's squares in I's units, ALGEBRA.md 8.6) and drop the second division |
| (c)-17 | `detector_law.py:1219-1266` (`record_form`, the conserved form I with the weights 3 den x (L / num) and L on the Links) | (B) and (G) over the whole board, a GAMEBOARD diagnostic read by the books | DIAGNOSTIC ONLY (labelled so in the docstring and in `books`) | none |
| (c)-18 | `detector_law.py:1287-1367` (`_click`: `cell_of` and `rungs` of `amplitude.py:241-329` on the pointers, the ledger's lines) | the click's choice by the ladder of rungs on the wheel (D), the content handed once | CLEAN, carried (yesterday's rows on `amplitude.py`) | none |
| (c)-19 | `core/phase.py:164-201` (`nearest_phase`: `for phi in range(N)` with two steps, the least residual) | a minimisation by iteration over 2 N entries: not one of the six verbs (an iteration inside a step, "no iteration inside it" of workflow.md's why) | DIAGNOSTIC ONLY (row (a)-9; read by no rule) with one line: it must stay so; the tables act on the pair by the linear form (row (c)-5) and never through this reading | none; the builder's docstring already says it |
| (c)-20 | `engine.py:122-154` (`step_axis`), `:157-182` (`count_owed`), `:773-1052` (`_move`), `:1299-1375` (`_give`); `measured.py:100-152`, `:404-930` (`counts_table`, the push's denominators); `nature_beam.py:3037-3125` (`push_form`), `:587-637` (`by_clock_rows`, `by_drive_rows`), `:639-714` (`exact_phase`), `:1475-1661` (the merge), `:2420-2530` (`transform`), `:6494-6561` (`_merge`) | the ray law's rules, one row each in yesterday's audit, all one of the six verbs on `core.integer`'s primitives | CLEAN, carried (unchanged files; yesterday's 89 ALGEBRAIC rows) | none |

**(c) in one line.** Every rule of the GO's engine is one of the six verbs
on bounded integers with its declared integers and its one division,
except the take (its remainder dropped, row 3), the ramp's rescale of the
remainder (row 2) and the sourced norm's second division (row 16): 3
violations new (2 MEDIUM, 1 LOW), 4 carried from the ray law (2 MEDIUM,
2 LOW, all under keys the GO does not run).

---

## (d) Locality: each Node's interval reads its own record and the six neighbours; nothing kept at a Node beyond the events there

| Row | File and lines | What the line does | Verdict | The fix, if a violation |
| --- | --- | --- | --- | --- |
| (d)-1 | `detector_law.py:1006-1061` (`_shift` by one Node per axis with the wrap or the fill; `_neighbours`, the six shifts summed; a receiver neighbour read through its Port amplitude `ports[index]`) | the rule's inputs at a Node: its own row (a_now, a_before, r) and the six neighbours' a_now, a receiver's by the Port that faces the Node | CLEAN (LOCALITY-1: one Link, six neighbours, fixed work per Node) | none |
| (d)-2 | `detector_law.py:1134-1145` (the take reads `free_now` and `free_next`, the free neighbour's level before and after this interval's step) | the receiver's Port reads its one free neighbour's new amplitude: one Link, under a declared order within the interval (the free Nodes' step, then the Ports) | CLEAN (DESIGN.md section 5, "the Port's take": "one Link under a declared order within the interval") | none; the order is to be written into ENGINE.md's interval steps when the design lands (the design's own line) |
| (d)-3 | `detector_law.py:1128-1131` (`nxt[self.absorbing] = 0`; `nxt[~live.mask] = 0`) | a receiver's own row held at 0; an arm's row held at 0 outside its half-space | CLEAN for the receiver (its own row); the mask is row (d)-6 | none |
| (d)-4 | `detector_law.py:1178-1217` (`_split`: reads `live.now[source]` and `live.before[source]` at each INPUT Node, a neighbour of the splitter's Node, and adds the quotient to `live.now[output]` at each OUTPUT Node, another neighbour) | the table's action carries the input Node's pair to the output Node within one interval: input to splitter to output is two Links, and the splitter's own row (held at 0, `splitter_mask`) carries nothing of it | VIOLATION, MEDIUM (LOCALITY-1: a Node's new level depends on a Node two Links away at the previous interval; every other rule of the module moves one Link per interval, and the splitter's reach is the one exception, undeclared in DECLARATIONS.md section 14 and in the `Splitter` docstring) | let the splitter act as the receiver does: the table's Node reads its inputs' pairs (its neighbours, one Link) and writes ITS OWN Port amplitudes toward the outputs (one per output direction, as `live.ports` holds one per take mask), which the output Nodes read as their neighbour's level at the next interval through `_neighbours` (one Link): the same numbers one interval later, the remainder kept per Port as today per output; re-read row 2b's pin (the visibility) before any run, since the arm's length changes by one interval |
| (d)-5 | `detector_law.py:1200` (`splitter.remainders.setdefault(live.identity, ...)`), never removed in `_click` (`:1287-1367` pops `block.responses`, `emitted`, `rung_counts`, not the splitters' remainders) | the splitter's remainders per output per record, the declared remainder of the division, kept on the splitter for every record ever born | VIOLATION, LOW (the storage grows with the records born, not fixed for a fixed K; the remainder itself is the declared one the scope admits) | pop `splitter.remainders[live.identity]` for every splitter in `_click` beside `rung_counts` |
| (d)-6 | `detector_law.py:1063-1072` (`_half_space`: `np.indices` over the board, (node - origin) . vector >= 0), formed once per arm at the birth (`:945`), applied every interval (`:1131`) | the pair's arms: each arm's row confined to its own side of the lamp's Node by a mask formed from the lamp's declared position and the arm's first direction | DECLARED INPUT (world data per Node, as `absorbing` is: a Node's membership in the arm's side is a constant of the declaration, not a reading of another Node; formed on the host at the birth, a host cost of the board's size per birth, to be counted with the host's costs) | none; the label "a declared set of Nodes, as a detector set" in the docstring would close the question |
| (d)-7 | `detector_law.py:1379-1424` (`step`: the blocks' massive records advanced before light's; the source term of every block into every light record; a response record per (block, light record) made on first contact `:1418-1424`) | the coupling's inputs at a block's cell: light's first difference at the same cell (`_receive` `:663-674`, or the block's own Ports' motion `port_motion` for an absorbing block), the massive current at the same cell (`_source` `:676-685`) | CLEAN (same-Node reads; ALGEBRA.md 8.5 "both local to the cell"); the responses' count grows with the live light records reaching the block (bounded by the records present, released at the click `:1349-1354`) | none |
| (d)-8 | `detector_law.py:1268-1285` (`_complete`: `np.sum(motion x motion)` over the WHOLE board), `:1287-1300` (`_click`: `cell_of` over the pointers of every cell) | the completion of a record and the choice of its click: the host's reading over every Node and every cell, one non-local step per record | DIAGNOSTIC ONLY in the scope's words ("the completion the host's reading"; DESIGN.md section 5, "the click's one non-local step, the host's, as today"; ALGEBRA.md 8.6 "not a dependency of any Node") with one LOW line: the code's docstrings do not say HOST at either function, while the design and the order require every host reading labelled host (workflow.md, the local test: "every host reading labelled host") | write "HOST: the completion is the host's reading over the board, not a dependency of any Node" in the two docstrings; no code change |
| (d)-9 | `nature_beam.py:6563-6734` (`gather_records`, `_place_completion`) with `amplitude.py:901-1003` (`Layer.complete`) | the ray law's completion reads every detector's offer across the board | the same host reading, carried (yesterday's row, FINDING; DIAGNOSTIC ONLY under the scope's admission; HISTORY for the GO) | the same label |
| (d)-10 | `detector_law.py:765-815` (`_block_clock`, the sum over R), `:817-837` (`_book_response`, over R), `:498-515` (`_cube`, R the cube of `side` at the corner) | the block reads its own record across its own cells, a declared set of side^3 Nodes | CLEAN (ALGEBRA.md 8.6 "local, the body's own record across its own cells"; fixed work for a declared side) | none |
| (d)-11 | `detector_law.py:517-531` (`_write_pair`, the kind's pair arrays over the board rewritten at every hop `:602`), `:596-631` (the take masks re-formed at every hop of an absorbing block) | world data at the cells moved with the block: the host's bookkeeping of the declaration, of the board's size per hop | DECLARED INPUT (a value per Node; a host cost) | none; count the hop's host cost in the run's HOST line |
| (d)-12 | `detector_law.py:132-147` (`LiveRecord.now`, `before`, `remainder`, dense over the board; `ports`, one array per take mask; `port_motion`), `:255-480` (`__init__`) | what is kept at a Node: the record's two levels and its remainder, and at a receiver its Port amplitudes (one per Port facing a free Node, DESIGN.md section 5, "one amplitude per Port") | CLEAN (nothing beyond the events there and the declared remainder; the Port amplitude is the design's declared state of the Port). The dense build keeps a row at every Node for every live record (zeros included): the host's storage is the board's size times the records live, and the host's work per interval the same; not a locality finding (each Node's update reads six neighbours), a HOST cost to be reported separately, as the module's docstring says ("the first build") | none; the run's HOST line reports it |
| (d)-13 | `detector_law.py:1441-1468` (the probes' sum of light's levels at declared Nodes; the mode's three residue sums along an axis), `:765-815` (the block's `centre` value), `:1469-1492` (`read_phase`) | readings of the GameBoard written on their own lines, read by no rule | DIAGNOSTIC ONLY (each labelled GAMEBOARD in its comment or docstring) | none |
| (d)-14 | `detector_law.py:567-578` (`motion_pair` reads `block.momentum` and `block.wall`, the object's own) and `:555-565` (`_momentum_now` reads `self.tick` against the block's declared `start` and `ramp`) | the coupling's pair in motion from the block's own declared numbers and the interval's count | CLEAN as a read (the object's own); the formula is row (b)-7 | none here |
| (d)-15 | `engine.py:664-736` (`_frame_all`), `:1418-1608` (`books`, `recount`) | the ray law's frame reads every measured event's content once per interval for the push and the books; the books a diagnostic | CLEAN, carried (yesterday's rows: the frame's reads are the bodies' own records; the books read-only) | none |

**(d) in one line.** Each Node's interval reads its own record and the
six neighbours, the completion is the host's reading, and nothing is kept
at a Node beyond the events there and the declared remainder, except the
splitter's two-Link reach (row 4, MEDIUM) and its remainders never
released (row 5, LOW); the host readings lack the word HOST in two
docstrings (row 8, LOW).

---

## What the owner asked, answered

"Is the code clean and orderly, no formulas in the engine, entirely
algebraic with integers?" Per item, for the GO's engine (the branch
8625f816 merged; the ray law's carried findings are counted apart, since
no `detector_law` world declares the keys they run under):

| Item | Yes or no | Violations in the GO's engine (new today) | Carried from the ray law (yesterday's, re-verified, under keys the GO does not run) |
| --- | --- | --- | --- |
| (a) no float, root or transcendental at run time | YES for the interval's path: the gate passes at both heads, no float, no true division, no root at run time in `detector_law.py`, the tables and the one root at load declared | 1: the integer bound unchecked on the dense rows (row (a)-15, MEDIUM; no GO world wraps today) | 3 MEDIUM (the meeting's root, the pushed row's ladder root, the body's weight's root); and, new, 1 LOW label line (the inventory's reason for `body_weight`, row (a)-6) |
| (b) no physical formula in the engine, the rates and walls declared data, no branch on a name or kind | NO, not yet: the rates and walls are data except three numbers held by the engine and one computed in motion; no branch on a name; seven branches on the kind | 5: MEDIUM the grace (row (b)-6), MEDIUM the index in motion (row (b)-7), MEDIUM the kind branches (row (b)-8); LOW the train's default (row (b)-4), LOW the take's pair as a module constant (row (b)-5) | 0 (yesterday's LOW on the parser's defaults and `boundary` open by default stands, `world.py:4516-4800`, unchanged) |
| (c) every rule one of the six verbs with its declared integers and its one division with the remainder kept | MOSTLY: the rule, the coupling, the click, the block's clock, the drive, the birth and the splitter's form are the verbs with one division each and the remainder kept; three places drop or rescale a remainder | 3: MEDIUM the take's remainder dropped (row (c)-3), MEDIUM the remainder rescaled under a ramp (row (c)-2); LOW the sourced norm's second division (row (c)-16) | 4: MEDIUM `reseed_flight` and `optical_turn` (two remainders dropped), LOW the meeting's `register` rounding, LOW the collision's tie; and LOW the per-axis tie, present in `_move_block` too (row (c)-8) |
| (d) locality: own record and six neighbours; the completion the host's; nothing kept at a Node beyond the events there | YES for every rule but one: the splitter reaches two Links in one interval | 2: MEDIUM the splitter's reach (row (d)-4), LOW its remainders never released (row (d)-5); and LOW the missing HOST label on the completion and the click (row (d)-8) | 1: the ray law's completion, the same host reading (row (d)-9), the same label |

**The counts.** New today, in the GO's engine: 11 violations and 2 label
lines: 7 MEDIUM (the bound among them), 4 LOW, 2 labels; nothing HIGH. Carried
from the ray law, unchanged since yesterday and under keys the GO does not
run: 8 (5 MEDIUM, 3 LOW). Rows read: (a) 15, (b) 15, (c) 20, (d) 15; 65
rows, 40 CLEAN or DECLARED INPUT, 7 DIAGNOSTIC ONLY, 17 VIOLATION (11 new,
6 carried rows holding 8 findings with the per-axis tie of row (c)-8), 1 noted absence (the rotation on the
pair, not built at 8625f816). No number of any pin was moved or
recomputed here.

**The answer in one sentence.** The GO's engine is integer and algebraic
in its path (no float, no root, no true division at run time; every rule
one of the six verbs), it is local except at the splitter, and it is not
yet clean of formulas: one physical formula is computed in the engine in
motion, three physical numbers live in the engine as constants, the
engine branches on the record's kind, and three remainders are dropped or
rescaled against the law's own rule; the integer bound of the dense rows
is unchecked at run time.

### The proposed fixes, by severity, each bounded, NONE APPLIED

1. **MEDIUM, the bound (first because a wrap is silent).** `world.py:3214` and
   `detector_law.py:1074-1127`: extend `_pair_bound`'s scale to g_d x
   (W_d^2 - 3 **P** . **P**) at the block's declared momentum, and add one
   host comparison per record per interval in `_advance`,
   `abs(nxt).max() <= AMPLITUDE_BOUND`, raising `OverflowError` naming the
   rule (row (a)-15); the eleven moving worlds' walls today sit at 54 to
   63 bits under the load's A, so the check refuses nothing that runs now.
2. **MEDIUM, the take's remainder.** `detector_law.py:1134-1156`: one
   remainder array per take mask beside `live.ports[index]`, added to the
   numerator before the division by 56 and stored after it; the pins
   re-read by the pins script before any run (row (c)-3).
3. **MEDIUM, the splitter's reach.** `detector_law.py:1178-1217`: the
   table's Node writes its own Port amplitudes toward the outputs, read by
   the outputs one interval later through `_neighbours`; the remainder
   kept per Port; row 2b's pin re-read (row (d)-4).
4. **MEDIUM, the kind branches.** `detector_law.py:1090`, `:1279`,
   `:1394`, `:1435`, `:1445`, `:1458`, `:1484`: one boolean `taken` on
   `LiveRecord`, set where the record is made, read in place of
   `massive_kind` (row (b)-8).
5. **MEDIUM, the index in motion.** `detector_law.py:567-578`,
   `world.py:3122-3290`: the coupling's pair in motion formed at load per
   block from its declared momentum (a table of `ramp` entries under a
   ramp) on `BlockDefinition`, the engine reading it (row (b)-7); or the
   formula named in ALGEBRA.md 8.5 as the engine's one, by the owner.
6. **MEDIUM, the remainder rescaled.** `detector_law.py:1101-1104`: with
   fix 5, one wall for the ramp (the pair at the ramp's end) and no
   rescale; else the old remainder carried as a pair and divided with its
   own remainder kept (row (c)-2).
7. **MEDIUM, the grace.** `world.py:2461` (`_lamp`) and
   `detector_law.py:1080`: the lamp's key for N_s in periods, refused when
   absent under `detector_law`, read from the record (row (b)-6).
8. **LOW, the take's pair.** `detector_law.py:97-98` to `world.py` beside
   `LIGHT_PAIR`, read into the measured event's and the faces' `take`
   (row (b)-5).
9. **LOW, the train's default.** `detector_law.py:86`, `:895`: refuse a
   lamp without `train` under `detector_law` in
   `_detector_law_load_checks`; delete the constant (row (b)-4).
10. **LOW, the sourced norm.** `detector_law.py:1409-1415`: the norm's
    increment from the rule's own quotient or from the block's ledger, no
    second division (row (c)-16).
11. **LOW, the splitter's remainders.** `detector_law.py:1287-1367`: pop
    `splitter.remainders[live.identity]` at the click (row (d)-5).
12. **LOW, the labels.** `detector_law.py:1268` and `:1287`: the word
    HOST in the two docstrings (row (d)-8); `tests/test_integer_algebra.py`
    line 144-146: the reason of `("events/world.py", "body_weight")` to
    "AT RUN TIME under `drive_b`" (row (a)-6).
13. **Carried, the ray law (under keys the GO does not run).** The three
    run-time roots (rows (a)-4 to (a)-6), the two dropped remainders (row
    (c)-13), the meeting's rounding (row (c)-14), the collision's tie (row
    (c)-15), the completion's label (row (d)-9): yesterday's proposals
    stand, in AUDIT.md section 5.2, unchanged.

Every fix above is the builder's to make on the owner's word through the
physics-rule reviewer; the pins that fixes 2 and 3 may move are named at
their rows and are to be re-read by the pins script before any run. No
law changes by this page; nothing here is a decision of the model owner.
