# H-Confirm-Page-1: a cold read of reader-5 at 4d8009f37 (tools/page.py and reader/) for the merge into engine-5.0-test

REFUSED 4d8009f37 for the merge: one breach, ranked alone.

1. The header drops a lone lay's centre (item 3c), the mend the Boss held reader-5 for. `lays_of` at tools/page.py lines 279 to 285 strips `centre` from every lay's key before counting, and returns the bare key when the count is 1, so the centre of a lone `at` lay never reaches the header. Measured on the pages: the hole's seed `{"lay": "at", "row": 0, "centre": [1, 0, 0], "quanta": 1}` reads on the page as `{"lay": "at", "row": 0, "quanta": 1}`; the packet's `{"lay": "at", "row": 2, "centre": [6, 4, 4], "width": 3, "quanta": 218}` reads as `{"lay": "at", "row": 2, "width": 3, "quanta": 218}`. Centres in the seed 1, centres shown in the header 0, on both. The fold itself holds: 8 alike `at` lays read as `{"lay": "at", "row": 0, "quanta": 1} at 8 centres`. No commit on the branch names the lone centre; 3b16f3702 folds, 4d8009f37 and the rest touch the drawing. What it breaks: the header is the page's one line from the two files as they are, and the owner reads a world's seed from it without its place on the board.

Everything else measured holds: the branch touches tools/page.py and reader/ alone; the suite passes 73 of 73; the tools' gates all exit 0; nothing of a universe is typed; the floats stay in the drawing; the clicks read back field by field; both pages run headless with no error, their readouts equal to the record's integers; both pages under 5 MB.

Worktree: /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/pg1 (S = /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad), HEAD 4d8009f37, merge base with origin/engine-5.0-test bb9deff70. Scripts and outputs: /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/pg1/tools/derivations/open_items/H-Confirm-Page-1/ (headers.py, clicks_check.py, intervals.py, dom.js, frames.js copied, make_records.sh, worlds/, out/, frames/, pytest_all.txt, make_records.log). Every run under nice -n 19 with PYTHONPATH=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/pg1/src and the venv314 python.

## 1. What the branch changes against engine-5.0-test

Commands: `git log --oneline $(git merge-base HEAD origin/engine-5.0-test)..HEAD`; `git diff --stat $(git merge-base HEAD origin/engine-5.0-test) HEAD`; `git diff --name-only ... | grep -vE '^(tools/page\.py|reader/)'`.

- 14 commits above the merge base: 3b16f3702 (the fold of the lays), d3a69d5ec, a467cf437 (merge of 44abf08), 3e5a5d95b, 88bf4b9d3 (merge of bb9deff), 3e3022e9c, d89c89759, 4ae142ccc, eb34768d8, 4f6fdf65d, 23a836a70, ae4df436e (mend of an apostrophe), 5e53d8aa4 (the clicks as short lists), 516d1ced5 (mend of the clicks' read), 4d8009f37.
- 149 files changed, 5373 insertions, 27 deletions: tools/page.py (164 lines changed) and 148 files under reader/ (reader/f4a210a, reader/44abf08, reader/bb9deff: pages, readings, frames, one mp4).
- Files outside tools/page.py and reader/: none (the grep found 0). No change under src/, tests/ or docs/.

## 2. The repository's checks on the branch

| check | command | result | exit |
| --- | --- | --- | --- |
| the record's tests, the page's own among them | `nice -n 19 $PY -m pytest -q tests/test_the_record.py` | 11 passed in 9 s | 0 |
| the whole suite | `nice -n 19 $PY -m pytest -q tests/` | 73 passed in 104 s, no failure | 0 |
| lint | `ruff check tools/page.py` | All checks passed | 0 |
| format | `ruff format --check tools/page.py` | 1 file already formatted | 0 |
| the code's shape | `$PY tools/record_code_shape.py` | the shape of the code holds against the merge base | 0 |
| the documents' gates | `$PY tools/documents_gates.py` | the documents' six gates hold | 0 |
| the engine's gates | `$PY tools/engine_gates.py` | the engine gates hold against the merge base | 0 |
| the tests' shape | `$PY tools/tests_shape.py` | the shape of tests/ holds against the merge base | 0 |

The page's own test, test_the_page_is_one_html_from_the_record_and_the_reading_with_nothing_typed, asserts `den` and `shape` in the page and every event's label in it; it does not read the seed's centre, so it passes with the breach above.

## 3. tools/page.py cold-read (410 lines; lines 1 to 36 the docstring and tokens, 38 to 263 the script, 264 to 410 the Python)

(a) Nothing of a universe typed. `grep -niE "electron|proton|neutron|photon|quark|[0-9]{4,}" tools/page.py` hits 8 lines, none a family's name or a world's constant: line 1 (the docstring: the date 2026-10-25 and two message numbers 6397241917 and 6397272516, the owner's words through the Boss); line 10 (`BOUND = 4 * 1024 * 1024`, the page's byte bound); line 12 (the base-36 digits string); lines 15, 17, 100, 180 (hex colours of the tokens and the canvas); line 239 (`1000 / speed`, milliseconds per tick). The words electron, proton, neutron, photon, quark: 0 hits. The test's own grep (den's digits, "electron", "light" absent from the source) passes.

(b) Floats. The Python side (lines 264 to 410) has no float: `word` and `letters` divide with `//`, `kept` takes the ceiling as `-(-total // BOUND)`, every value written into the embedded JSON is an integer, a string of base-36 digits or a letter. The script's float literals, each named with where it stands and what it touches:
- yaw 62/100 and pitch 42/100, the 9/10 on the y axis, the `c + 3/2` divisor in `place`: the projection of the board; pixels alone.
- `Math.pow(X / G, 1/4)` in `length`, `stretch`, `meanStretch`, `Math.sqrt(mean / most)` in `lay`, the 1/10^9 floors on `most` and `lenSpan`, `touch = 5 / full`: the Links' drawn lengths and the board's size; pixels alone. The JavaScript `bangs` from the minima of these stretches (with the 10 times test) name the "Big Bang" labels' intervals: those intervals are the record's own integers `lines[k].i`, the floats pick which, and the label says "the board at its zero and rising", the page's own reading of the X lines, not a number from the reading file.
- `1/5 + 7/10 * rel` and `1 + 5 * rel` (the Links' alpha and width), `35/100 + 65/100 * size`, `h * 1/2`, `4 + 10 * size` (the current's marks), `18/100 + 3/100 * total`, `5/2`, `3/2` (halos, rings, leaders), `1/5 * PI` and `17/10 * PI` (the turned arc), `8/100 + 5/100 * age`, `35/100 + 15/100 * (r % 2)`, `age / 10` (the burst), `22/100 + 2/100 * wholeTurn` (the dashed ring), `24/100`, `1/10`, `14/100`, `16/100` of the canvas width (label places), `1 - age / 4`, `1 - back / 8`, `1 - wholeTurn / 12` (fades), `11/10 * PI`, `1/2`, `9/10` in `glyph` (the glyphs' strokes), `82/100` in the label's background: every one a pixel, an alpha or an angle.
- The percentages `100 * (i - 1) / (N - 1)` on the bar and the cursor: positions of the record's integer intervals; the tick's title and the era's title carry `e.label`, `e.numbers` and `e.gate` as strings from the reading.
- The readout: `up`, `down` and `line.X.length - up - down` are counts of integer comparisons of the X words parsed by `parseInt(w, 36)`; `line.i`, `N`, `D.stride` integers. The labels: `e.label + e.numbers` from the reading file as strings, the intervals `b` and `lines[...].i` integers. So no float reaches a number shown as a reading. One bound: `parseInt` holds an integer exactly under 2^53 = 9007199254740992; the largest X in the committed records is 60594 (bodies), 26624 (hole), 25196 (chiral), and 26624 and 6063 in the two records run here, so the bound is not reached; a record whose X passed 2^53 would compare X as doubles in the readout.

(c) The header's lone lay: the breach above. Command: `$PY headers.py out hole_60 packet_6 universe_6 many_4 plasma_3_170`, each page made as the test makes one (the record by `event_universe.run`, the reading by `event_universe.gates`, the page by `tools/page.py <record> <reading> <out>`). The lines read:
- hole_60: `world: shape [5, 5, 5], 60 intervals, seed {"lay": "sea", "row": 0}; {"lay": "hole", "at": [0, 0, 0]}; {"lay": "at", "row": 0, "quanta": 1}`: the centre [1, 0, 0] absent (the hole lay's `at` stands, its key is not `centre`).
- packet_6 (world_packet.json cut to 6 intervals, the header reads the seed alone): `seed {"lay": "at", "row": 2, "width": 3, "quanta": 218}`: the centre [6, 4, 4] absent.
- universe_6 (world_universe.json cut to 6): three sea lays, no centre in the seed, the line as the seed is.
- many_4 (a built world: a sea and 8 `at` lays alike but for their centre, 5-cube, 4 intervals): `{"lay": "at", "row": 0, "quanta": 1} at 8 centres`: the fold with its count holds.
- plasma_3_170: three sea lays, as the seed is.

(d) The clicks folded to short lists. Command: `$PY clicks_check.py out hole_60` and `... plasma_3_170`, reading the page's embedded JSON (`<script id="data">`) against the record's `log` lines of event birth or credit, field by field in the page's order [interval, the Node's index x*c*c + y*c + z, the row (`line`, else `line_pair`), the levels taken, the taken row else -1, a birth's two children's indices else 0]:
- hole 60: record lines 249 (births 16, credits 233), page clicks 249; mismatches per field 0, 0, 0, 0, 0, 0; the intervals in order; every credit carries `levels` (233 of 233) and none `taken_row` (so the page's -1 for a credit is the record's absence, read as blue from the gap-0 row); every birth carries `line_pair` (16) and `taken_row`. The page's `bangs` [9, 19, 24] equal the births' intervals. Stride 1, 60 of 60 Node lines kept.
- plasma_3 at 170: record lines 135 (credits 135, births 0), page clicks 135, mismatches 0 on every field, bangs [], stride 1, 170 of 170 lines kept.
- The script reads the lists back in the same order (line 50: `i: k[0], at: k[1], node: unravel(k[1]), line: k[2], levels: k[3], from: k[4] < 0 ? null : k[4], children: k[5] ? k[5] : null`), confirmed in the browser: the hole's first click reads `i 9, at 32, node [1, 1, 2], line 1, levels 16, from 3, children [7, 32]`, and the record's first birth is at interval 9, Node [1, 1, 2], line_pair 1, levels 16, taken_row 3, minus [0, 1, 2] (index 7), plus [1, 1, 2] (index 32).

## 4. The pages run headless (Playwright, Chromium, viewport 1280 by 960)

Records (make_records.sh): world_hole.json to 60 in 4 s; world_plasma_3.json to 170 in 3 s; both readings by `event_universe.gates`. Pages: hole_60.html 113191 bytes, plasma_3_170.html 90205 bytes, both under 5 MB (5242880); the largest committed page, reader/bb9deff/chiral.html, 4121445 bytes. Command: `node dom.js <page> frames/<name> <intervals>`, evaluating `playing = false; t = seek(k); draw()` per interval, reading `#where`, the `#labels .label` divs, the bar's `.name`, `.era` and `.tick`, collecting `page.on('console')` (errors and warnings) and `page.on('pageerror')`, one PNG per interval under frames/ and one JSON per page (frames/<name>.dom.json).

Intervals: `intervals.py` picks the first local maximum of the sum of X and the first minimum after it. The plasma record has them: 83 (top) and 167 (bottom). The hole's sum of X rises through all 60 intervals with no top, so its frames are 1, 9 (the first bang and first click), 19, 24 (the other two bangs), 30 and 60; said here as asked.

Hole 60 (frames hole_60_001, 009, 019, 024, 030, 060.png): page errors 0, console errors 0.
| interval | readout | record's integers (rising, falling, rest) | labels shown |
| --- | --- | --- | --- |
| 1 | interval 1 of 60; the seed | 0, 0, 125 | 2: Big Bang (interval 1), the three constants hold |
| 9 | interval 9 of 60; 75 rising, 50 falling, 0 at rest | 75, 50, 0 | 11 (the bang label, then 10 events through interval 9: one Link per interval, the exclusion holds, the lengthening quickens, the take pays the walls, a pair born, births of both hands, the entropy rises, no third alone, light absorbed at a take) |
| 19 | interval 19 of 60; 111 rising, 14 falling, 0 at rest | 111, 14, 0 | 15 (adds the floor holds, a body clicks, the clicks conserve, the clocks run slow, the era of matter) |
| 24 | interval 24 of 60; 118 rising, 7 falling, 0 at rest | 118, 7, 0 | 17 (adds the mass ratio read; three lifts, the beats ordered) |
| 30 | interval 30 of 60; 120 rising, 5 falling, 0 at rest | 120, 5, 0 | 18 (adds the Links lengthen) |
| 60 | interval 60 of 60; 115 rising, 10 falling, 0 at rest | 115, 10, 0 | 21 (adds two bodies meet, a body stands in its well, unlike attract, like repel) |
Every label's second line is the reading's verdict text as the file has it (for instance "a body clicks | SHOWN in part: every credit within the floor, tracks right 32 of 40"). The bar: 16 names, 22 ticks, 3 eras titled "1 bang", "5 acceleration (the lengthening quickens)", "4 an era of matter"; the numbered bang marks at 9, 19, 24. Every label stays 60 intervals by the commit's design, so on a 60-interval record all 21 stand at the end and pile below the board (seen on hole_60_060.png and 024.png: the labels without a Node stack at the foot and overlap those with a Node).

Plasma_3 at 170 (frames plasma_3_170_001, 083, 167, 170.png): page errors 0, console errors 0.
| interval | readout | record's integers | labels shown |
| --- | --- | --- | --- |
| 1 | interval 1 of 170; the seed | 0, 0, 27 | 2: Big Bang (interval 1), the three constants hold |
| 83 | interval 83 of 170; every clock's volume rising | 27, 0, 0 | 0 (the last event before is at 13, over 60 back) |
| 167 | interval 167 of 170; every clock's volume falling | 0, 27, 0 | 0 (the events at 99 are 68 back) |
| 170 | interval 170 of 170; every clock's volume rising | 27, 0, 0 | 0 |
The bar: 8 names (the three constants hold, the floor holds, light absorbed at a take, a body clicks, a track read right, two bodies meet, the board shortens then lengthens, the board contracts), 12 ticks, 1 era "1 bang". The single turn at interval 84 is not among the frames.

The readout's counts equal the record's integers at all 10 framed intervals.

One observation, not a breach of the rule given: the word "bang" names two things on the page. The embedded `D.bangs` are the births' intervals (hole: 9, 19, 24), drawn as the numbered marks 1, 2, 3 on the bar; the script's own `bangs` (hole: [1]) from the stretches' minima draw the burst and the "Big Bang" label and the orange ticks. Both stand by the docstring's words; a reader of the bar sees "Big Bang at 1" beside a mark "1" at 9.

## Missing by name

- The hole 60 record has no top and no bottom of the board within 60 intervals; the frames stand at 1, 9, 19, 24, 30, 60 in their place.
- No reader test asserts a lone lay's centre in the header; tests/ is outside the branch's allowed files, so the assertion is for engine-5.0-test to carry, by whoever owns tests/.
- The pages under reader/ were not re-run here beyond the largest's byte count (4121445, reader/bb9deff/chiral.html); their headers carry the same `lays_of`, so every committed page of a world with a lone `at` lay (hole, packet, bodies, chiral) lacks the centre too.
- Playwright was run on two pages at ten intervals; the play's hold of three seconds per new label and the speed buttons were not timed.
