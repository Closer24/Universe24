# The fourth hostile code reader on b1a50bb33..49e97c992 (node-live, C5), 2026-10-31

(Written by the Boss from the reader's hand-back, the reader's harness having refused the write; the text is the
reader's. The evidence is in this folder: gate.log, fullcheck.log, runs/, mut/ and probes/ (each probe with its .out).
The reader's worktree hcr4/tree is removed; to rerun a probe, re-add a worktree at 49e97c992. scanZ and live/.venv are
untouched, and nothing was committed or pushed.)

VERDICT on b1a50bb33..49e97c992: NOT PASSED

There is one BLOCKING item and five MINOR ones. The BLOCKING item is D8 on the shipped click world; the fix is small.
The rest holds:
- The laws hold.
- The gate and the full check give what the Boss's runs gave.
- The five records decode as FRAMES 13's table says.
- The four named mutants fail the test.

WHAT I RAN
I worked in my own detached worktree at 49e97c992 under hcr4/, with .venv linked to live/.venv, removed when done.
- The gate (gate5, --base origin/main --summary): no refusal, no note.
- The full check (CHECK_BASE=origin/main tools/check.py --full): exit 0, 28 passed.
- The decode tool on the five records. Each exits 0 with no stderr. Run with its ledger, each output is byte for byte
  writer C's (nightC_work/blocks/).
  - tensor24, -live, -well and -mesh: NO CLICK on all four, with the refusal line.
  - tensor24-click: the books SHOWN, 0 at 2106 of 2106 places. Trains 2, 3 and 4 match the table. D6 and D7 are NOT
    READ, and D8 is SHOWN at 4212 of 4212.
- Mutants as text edits in my tree. Each was run on the decoder test file and on the whole suite (mut/run.py,
  mut/more.py). mut/same.py and mut/world.py decode the click world under a mutant.
- Probes in whole numbers: probes/p1 to p7. Each was run twice and gave the same output.

=== BLOCKING ===

1. D8's SHOWN on the click world cannot fail, its line does not say so, and no test checks how the lay is read.
   Writer C.
   - Where:
     - src/tensor24/decoder/shadow.py:94, the SHOWN cause.
     - tests/test_the_tensor24_decoder.py:580, the ring's one gear, laid at site 0.
   - Evidence:
     - All 27 sites are laid. So each line has a laid site 0 Meshes away, its own, and the check is vacuous from
       round 0 (as the brief says).
     - It is vacuous a second way. The first click line comes at round 91, and the board's diameter is 3 Meshes. So
       the cone of one laid site would hold every line.
       - p1, with site 0 alone laid: SHOWN, 4212 of 4212.
       - p1, with lines that no run could write (round 1, at every one of the 27 sites): SHOWN.
     - The line reads "one Mesh a round from the 27 sites laid: 4212 of 4212 lines". It says neither that those 27 are
       the whole board nor that no line could stand outside the cone. FRAMES 13's own table asks for "every site
       laid".
     - Where nothing can be compared, the decoder's own tools read NOT READ (measure.py:183, "no setting outside a
       click's past cone drew two frames"; measure.py:257).
     - The test's one gear stands at site 0, which is also the cone's origin. So three mutants pass all 28 tests and
       leave the click world's whole output byte for byte the same:
       - the cone taken from site 0, whatever the setting lays;
       - the cone of the first laid site alone;
       - `all` in place of `any` over the laid sites.
   - Fix:
     - Count the lines that could stand outside the lay's cone. A line at a laid site cannot, and neither can a line
       at or past the board's diameter in rounds.
     - Where no line could, read NOT READ with a cause such as "the lay's cone covers the board's 27 sites from round
       0, before the first click line at round 91: no line could stand outside it". If the Boss keeps SHOWN, that
       sentence goes into the line instead.
     - In the test, lay the ring's gears at two sites, neither of them site 0. Add one line inside one cone only and
       one line outside both.

=== MINOR ===

1. More mutants pass all 28 tests, and the decoder file alone as well.
   - Where the books open only at a sum above 0, a lone give reads "SHOWN: the sum of q over the trains is 0 at 2 of
     2 places" (p4 under the mutant). The test's no case has its first open place at +1, and it never reads the count.
   - The books summed per site over the whole run, with the first round named. A give and its take at one site in two
     rounds would then close.
   - laid() treating every gear as laid, 0 or not; or reading the count alone and not the tooth.
   - ABSENT spelt "NOT READ", or NO_LINE changed. The test compares each with itself (:593).
   - The refusal line printed on every record (tools/tensor24_decode.py:61). The click world then prints "the record
     holds no click line" under its 4212 lines.
   - The books' per-train readings dropped, or the tool's train lines under the books dropped.
   - The cone's NOT READ for a header with no sides removed (the reading then raises TypeError), and for one with no
     setting (it then reads NOT SHOWN, every line outside; p7).
   - Fix, in the test (the file stands at 597 lines of the Boss's 600):
     - assert the books' cause whole, or add a lone give;
     - assert the literal "NO CLICK" and the owner's phrase;
     - assert there is no refusal line on a record with click lines;
     - assert one train's tally;
     - add one record with no sides.

2. The books' order is not row 15's.
   - Where: shadow.py:31, which returns NOT READ before it looks at the open places.
   - Evidence:
     - Take a record with a closed place, a lone give at round 2 and a line with no q at round 3. It reads NOT READ,
       naming round 3, and the open place is never named (p4).
     - Row 15 reads NOT SHOWN first, "with every gap named beside it, since law 8 breaks on the first reading alone"
       (books.py:24, :232).
     - Only a hand-built record lacks q, since the runner writes q on every line.
   - Fix: read NOT SHOWN at the first open place among those where every line holds q, with the gap named beside it;
     else NOT READ; else SHOWN.

3. Called on their own, books() and cone() read SHOWN on a record with no click line.
   - Evidence: the causes read "is 0 at 0 of 0 places" and "0 of 0 lines" (p1). The NO CLICK check lives in shadow()
     alone, and the test calls shadow.books directly (:592).
   - Fix: put the NO CLICK check in each reading.

4. laid() reads the setting without the runner's checks.
   - A gear at site 7 or site -3 on a ring of five is read as site 2, through meshes' carry. The cone then reads
     SHOWN, where the same line read from site 0 is NOT SHOWN (p2). The runner refuses such a site (files.py:225).
   - A setting.json whose text is not JSON reads "the header holds no setting file" (p6).
   - Fix:
     - read NOT READ for a gear whose site is off the board, naming it as the guards name a line's;
     - find the setting file by its name, and say when it is not read.

5. Wording.
   - (a) One output names the twins as both D6 (tools/tensor24_decode.py:83, an unchanged line) and D7 (the new
     block). measure.py's own docstring orders them D6 duration, D7 twins, D8 cone.
   - (b) On the test's own record of a whole click, given its ledger, row 15 prints SHOWN. The refusal line below it
     says "no claim of physics is shown on it" (p5).
   - (c) shadow.py's Clock and Board lines say the record's end is read and list the click line's tooth, but the
     module reads neither. The Board line also says "no gear's count", yet laid() reads every setting gear's counts.
   - Fix:
     - label the 1.2 line D7;
     - print the refusal only where the record holds no click of either kind;
     - make the docstring name only what the module reads.

THE LAWS: they hold.
- shadow.py uses whole numbers only, with no division, float, root, search, sine or cosine.
- shadow.py and the tool's new lines have no number beyond 0 and 1, and no 1 + 1. The tool's one slash is the old
  Path / "src" join at :21.
- The commit's files are all ASCII, and the import wall holds.
- The new test line tmp_path / "record.jsonl" joins by the slash, as the file's other eleven joins do.
- The cone docstring's two reasons stand. meshes is the torus's L1 metric, so the triangle inequality holds. The click
  tooth enters only its own carry, so the clicks push nothing back into the gears (step.py:143-144).

=== THE BOSS'S RULINGS (00:5x UTC) ===
- BLOCKING 1: NOT READ, with the cause naming why no line could stand outside the lay's cone (the decoder's own
  precedent, measure.py:183 and :257; the owner's ban on a claim that cannot fail). The test lays two gears, neither at
  site 0, with one line inside one cone only and one line outside both.
- The fold rides C6 (FRAMES 13b). Its new tests go in the second click-world test file with its own room (decision
  26); the decoder test file stays at 597.
