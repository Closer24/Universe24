# H-Readers-Unification-1: the readers Animate owns, the doubles and the folds

Head: origin/reader-5 at 8f2b67e29. Worktree $S/hands/ru1, nothing edited, nothing committed. Scripts and outputs: $S/hands/ru1/tools/derivations/open_items/H-Readers-Unification-1/ (inventory.py, inventory.json, inventory.txt, fields.py). One run of the decoder on examples/records/hole.json: the fresh reading equals the committed hole.reading.jsonl byte for byte after JSON (64 lines); the page written from it, 127874 bytes.

## The verdict line

Doubles found: (A) 16 readings computed in two or more places, (B) 3 name tables for 62 rows, (C) 1 verdict logic in 6 sites and the cut `Record.to` called 139 times for 32 distinct cuts, (D) 4 modules of one shape with 8 forms parsed again (33 sites) and 17 stub rows that are data, (E) 3 readings the page computes that the decoder owns, (F) 0 dead functions and 42 record fields no reader reads, (G) 34 asserts, 20 rows pinned by their kind alone, 1 whole-reading equality missing, 3 parsers of the reading file. Lines that fold: about 280 of 2908 (the four table modules from 1594 to about 1320), functions from 136 to about 112 (62 row functions to 41 plus 2 tables). What stays bit for bit: the three committed readings through every fold of phase 1; phase 2 (new fields: the plain name, the label, an eras row) regenerates them in the same commit with every key, number and verdict unchanged.

Scope note: src/event_universe/readings.py is the Node's readings of its own state (node.py calls it; numpy; no Record) and not a reader of the record under ENGINE.md section 4; it is left out of the table below and named under (B) for its name alone.

## (A) the same reading computed in two places

| file:line | what | the double | keep |
| --- | --- | --- | --- |
| board.py:142-144 and 182-184 | the tops (every Node turned) | recurring_bang recomputes tops' `whole` | tops computes `tops_of(record)`, 1 and 1b read it |
| board.py:145-146, 198, 263 | the exact returns | recurring_bang, returns, same_gates each filter bottoms_of for `at_gamma` | one `exact_of(record)` |
| gates.py:25-26 and predicates.py:58-59 | the torus distance | two identical nested `distance` functions | one in decoder (Record.distance) |
| decoder.py:108, board.py:42, 279, 325-328, page.py:355 | the Node's index from (x, y, z) and back | 5 sites of `cube * cube` arithmetic | Record.index(node) and Record.node(index) |
| gates.py:23, board.py:40, 169, 277, 334, predicates.py:56, decoder.py:106 | `int(record.run["cube"])` | 7 sites | Record.cube in __init__ |
| gates.py:61, 227, board.py:364, clicks.py:49, predicates.py:315 | the credits grouped by (Node, line) | 5 groupings, the count written in rows 9 (102 tracks), 8b (102), 45 (102) | one `bodies_of(record)` memoized, the count in one row |
| gates.py:223 and clicks.py:190 | the births' senses as signs | charge and conservations | charge's `signs_of`; conservations cites row 17's sum |
| gates.py:224, clicks.py:238, predicates.py:288 | taken against booked (hundredths) | written three times in the reading (rows 15, 47, the conservations: 102, 102, 102) | one `takes_of(record)` |
| gates.py:90 and predicates.py:153 | the takes (births and credits by event) | light and confinement | Record.takes in __init__ |
| clicks.py:81 and predicates.py:108 | the births by species (Counter over line_name[line_pair]) | written in rows 8 and 26 | one `born_of(record)` |
| clicks.py:191-197 and predicates.py:148-152 | the children laid where their plane stood at nothing | charge's `sizes` and confinement's `whole`/`thirds` are one zip over W_children and stood | one `laid_at_nothing(record)` |
| clicks.py:72-73 and 57-61 | tracks right | families writes [track_right, len(tracks)] and species_track writes the same two numbers | row 8b holds them, row 8 cites |
| board.py:198, 234, 263, 333 | len(record.births), len(record.credits) | written in rows 4, 8, 15, 47, 56, 57 (births 16 six times) | one row "the record" with the counts |
| gates.py:372 and events.py:93-110 | the table read twice | gates() calls verdicts(record), then first_shown calls row(record) again for all 62 rows | first_shown takes `out` |
| clicks.py:142 and predicates.py:402 | circle_of(den) | computed 11 times per gates(hole) (per cut, two rows) | record.memo["circle"] once |
| page.py:416-420, phenomena.py:73-84, tests/test_the_record.py:92-95 | the reading file parsed | 3 parsers of .reading.jsonl | one `reading_of(path)` beside gates.main's writer |

## (B) two names for one thing

Three tables for the 62 rows: the decoder's keys (f"{number} {title}", 60 numbered plus the conservations and the three constants, spread over the four modules), events.LABELS (62, events.py:11-74), phenomena.PHENOMENA (57, tools/phenomena.py:14-72; lacks 1b, 1c, 8b). Row by row in inventory.txt under "(B) the three name tables". Examples of three names for one row: 8 "families forming (whole view)" / "a body clicks" / "the families forming"; 17 "charge conservation" / "a pair born" / "charge conservation"; 28 "the conversion list" / "a conversion" / "the neutron's conversion"; 56 "Bell" / "Bell's bound holds" / "Bell's correlation". The units live in the keys ("19 mass ratios (parts per million)", "16 uncertainty floor (one click)") and in the field names too. The fold: one NAMES table in events.py (or a names.py of the readers), 62 rows of (number, title, label, plain name), read by gates.py (the key), events.py (the label), phenomena.py (the plain name, which then imports it or reads a "phenomenon" field the decoder writes), tests (the key). The key stays f"{number} {title}" so the readings stay bit for bit. Lines: 57 + 62 + the titles in 62 row functions fold to about 66; about 55 go. Also: "readings.py" (the Node's) against "the reading" (the decoder's file): one word for two things; a rename of the module is David's, named here only.

## (C) a verdict's logic repeated

| file:line | what |
| --- | --- |
| gates.py:349-363 kind_of (15 lines) and phenomena.py:88-91 kind_of (4) and 94-101 cause_of (8) | two readers of the kind from the words, two parsers of the "as gate N: " prefix |
| events.py:81-83 shown | a third: `startswith("SHOWN")` |
| events.py:115 | "numbers" = verdict.split(";")[0].split(" (")[0]: the field named numbers holds the verdict's first clause |
| tests/test_the_record.py:81, 83 | `kind.startswith("SHOWN")`, `verdict.startswith(words)` |
| gates 26, board 37, clicks 30, predicates 31 verdict literals | 124 string literals in 268 lines of conditional chains; the qualifiers after SHOWN in 7 forms ("at the board", "in the reader's view", "as silence", "as the identity", "as nature", "as the law's floor", "(every credit...") and two verdicts in one string in rows 2, 10, 15, 17 ("; NOT READ in the one-place view", "; the magnitude SHOWN") |
| the hand-written "NOT READ: why; the predicate: ..." outside predicates.unread | 17 sites: gates.py:104, 184; board.py:111, 143, 158, 305, 349, 375; clicks.py:335; predicates.py:93, 125, 158, 232, 268, 293, 328, 479 |
| events.py:86-94 first_interval with decoder.py:80-90 Record.to | 139 cuts for 32 distinct intervals on hole; every row function called more than once (max 11); decoded_credits 13 times, tracks_of 20, marks 15, volumes 12 |

The fold: one verdict type in decoder.py, Verdict(kind, view, cause, restates) with kind one of the five, view one of (board, reader, one-place, none), rendered once by `words(verdict)` into the string the readings carry (the same words, so bit for bit), the row writing `"verdict": words(v)` and the reading carrying beside it `"kind"` only when phase 2 adds fields; kind_of in gates and phenomena, events.shown and the two test reads fold to the field or to one `kind_of` in decoder.py (about 30 lines go); the 17 hand-written predicate clauses call `unread` (about 17 lines go). One cut: `Record.to` memoized by i in record.memo (139 to 32 cuts), and the per-cut memos (solved, lift, circle) keyed by the cut id.

## (D) the four modules against one shape

Signature shared by all 62 row functions: Record -> {key: {numbers..., "at"?: Node, "verdict": str}}. Functions: gates 21 (14 rows, approach, distance, restated, verdicts, kind_of, gates, main), board 18 (12 rows, marks, volumes, bottoms_of, returns_of, lift_of, neighbours), clicks 13 (9 rows, solved, tracks_of, leg_of, halves), predicates 31 (27 rows, unread, wave_lay, distance, course). Lines in functions: 265 / 322 / 286 / 411. What each parses again: the forms of (A) (33 sites over 8 forms). What is data and not a function: 17 stubs in predicates.py returning unread (141 lines: twist, conversion, perihelion, dragging, shears, aharonov_bohm, zeeman, two_beats, stern_gerlach, velocity, black_body, light_on_light, casimir, neutrino, binds, scattering, two_slits) and 4 restated rows in gates.py (12 lines plus restated, 4). The generic fold: one module per view is the law's own line and the modules nearly are it already (board.py the Node lines and the rows; clicks.py the log; the one-place view inside clicks 8b and the dilation's clause), so the fold is not a re-cut by row group but: (1) an UNREAD table of 17 entries (key, why or a function of the record for the 5 conditional whys, predicate) iterated by one row function, about 95 lines and 17 functions go; (2) a RESTATED table of 4 (key, gate function), about 10 lines and 4 functions go; (3) the shared reads of (A) into Record, about 45 lines go; predicates.py then holds the 10 read rows (21, 22, 26, 27, 40, 43, 47, 49, 56, 57) and the two tables, about 230 lines. Count after the fold: 41 row functions and 2 tables, the four modules about 1320 lines from 1594.

## (E) readings the page or phenomena.py keeps that the decoder should write

| file:line | what | the fold |
| --- | --- | --- |
| page.py:88 (SCRIPT), 161-166 | wholeTurn: the page decides "every Node turns at once" by its own rule (half the Nodes turned within 12 lines back), not row 1b's (every Node turned) | the page reads events with gate "1b"; the rule goes |
| page.py:30 | bangs = events whose key matches /^1c / | read e.gate == "1c" from the NAMES fold; the regex on the key goes |
| page.py:207-211 | eras = events whose key matches /^(1|4|5|46) / with a colour by the number | the decoder writes an "eras" row (interval from, interval to, the gate) in the reading; the page draws bands |
| page.py:360-371 | the clicks from the record with the take's source by taken_row == -1 | stays in the page (the record is the page's input and the list is 793 long); the source bit is row 24's rule, so the page should name the gap-0 row by the record's planes and not by -1 |
| phenomena.py:88-101 | the kind and the cause re-derived from the verdict's words | read the fields of (C) once the decoder writes them |
| page.py:26-28 (SCRIPT) | length(X) = (X / G)^(1/4) in floats, the drawn stretch | a drawing, not a reading; named for the owner: the readers' rule says no float, the page is a reader module |

## (F) dead or unreachable reader code

By grep over src, tests and tools: 0 functions named once only. By the traced run of gates(hole) (sys.setprofile; the venv has no coverage module): every function of decoder, gates, events, board, clicks, predicates and circle entered. Record fields no reader reads (fields.py): run: counts, gapped, turns; credit: closes, sign_level, taken_line, taken_now_was, taker; frame: re_before, im_before; birth: amplitude, senses, taken_line, taken_now_was, taker; refused: link; row: 16 of 25 fields (W abs sum, W total, body_clicks, gap-0 W abs max, gap-0 velocity max, link count max, links at the wall, milliseconds, odd max bits, orbit table, packets (reader), planes energy bits, refused_lay, refused_orientation, sign level max, tension min/max); counts: 12 of 15. The record's "counts" row and the rows' refused counts are the writer's and the readers never read them: either a row reads them (the conservations could cite counts.booked and counts.taken) or they are David's to drop; named, not decided here.

## (G) the readers' tests

tests/test_the_record.py: 34 asserts in 6 tests. Pinned: 57 numbered rows; the set of rows SHOWN per record (kind alone); NOT REACHED exactly {14, 34}; 4 verdicts by words per record (rows 9, 22, 45, 56 on hole; 9, 1b, 1c, 56 on chiral; 37, 55, 56, 57 on bodies); the constants SHOWN; the circle's count; the events line equal to a fresh gates(run); labels of six words at most; the page's text. No test pins the numbers of rows 1, 3, 5, 6, 8, 8b, 10, 13, 16, 19 (beyond the circle), 21, 23, 24, 25, 26, 27, 40, 43, 47, 49 (20 rows pinned by kind alone). Missing: one assert that the whole fresh reading equals the committed file after JSON (fields.py shows it holds on hole; the test asserts it for the events line only, line 118). Asserted twice: test_the_conservations_hold_on_the_record (lines 64-73) recomputes from the record what rows 17, 15, the constants and 18 read, and the first test asserts their kinds (one is the readers' logic repeated in the test; keep one as the independent check and say so, or fold to the reading). The test's reading_of (92-95) is the third parser of the reading file (A).

## The spec for Animate, in order

1. The verdict type and the cut (C): Verdict in decoder.py rendered to the same words; `kind_of` once; `Record.to` memoized by i; events.first_shown takes the verdicts already read. About 50 lines go; 139 cuts to 32; readings bit for bit.
2. The two tables (D): UNREAD of 17 and RESTATED of 4 in predicates.py and gates.py; the 17 hand-written predicate clauses through `unread`. About 120 lines and 21 functions go; readings bit for bit.
3. The shared reads into Record (A): cube, index/node, distance, takes, bodies_of, signs_of, takes_of, born_of, laid_at_nothing, tops_of, exact_of, the circle memo; the doubled numbers (tracks 102, births 16, taken per booked 102) written once and cited by key. About 45 lines go; readings bit for bit (the doubled fields stay in this phase, the code behind them folds).
4. One name table (B): NAMES of 62 in events.py; LABELS and PHENOMENA go; the keys unchanged. About 55 lines go; readings bit for bit.
5. Phase 2, the readings regenerated in the same commit: the decoder writes "phenomenon" and "label" per row, an "eras" row, and "kind" per row; phenomena.py and the page read fields and hold no rule (the page's wholeTurn and the two regexes go, about 10 lines); the doubled fields of step 3 go from rows 8, 9, 15, 45, 56, 57 and the conservations. Every existing key, number and verdict unchanged, checked by the old rows a subset of the new.
6. The tests (G): the whole-reading equality on the three records (one assert); the kinds read from the field; the conservations test named as the independent check; one reading_of.
After the fold: about 2630 lines from 2908 over the eleven files, 112 functions from 136, 41 row functions and 2 tables; the committed readings identical through steps 1 to 4.

## Missing by name

- No coverage module in venv314 (sys.setprofile used instead; function level, not line level).
- The test suite not run in the 30 minutes; the decoder and the page run on hole only (not chiral, not bodies).
- The three rows to come (57 to 60) unknown here; the counts above are for 62 rows (57 numbered, 1b, 1c, 8b, the conservations, the three constants).
- readings.py (the Node's) read but not inventoried as a reader of the record; its name collision named under (B).
- ALGEBRA.md's readers' clauses read by grep (lines 37, 39) and ENGINE.md section 4 read whole; no clause found that forbids a field beside the verdict in a row.
