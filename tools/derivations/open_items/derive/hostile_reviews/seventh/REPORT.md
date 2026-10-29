# The seventh hostile review: 814fe5c45, 8469170ad, 823690afc

Verdict: approve with changes (a fresh reader, 22:3x UTC 2026-10-28). 814fe5c45 and 8469170ad stand as they are, with
one wording follow-up on 8469170ad. 823690afc needs four changes, all in the decoder: two of row 15's readings can be
fooled, the tests miss half of the new guards, and the ticks reading takes a k that is not a bit. Every claim stands
on a probe the reader ran on a worktree of 823690afc; the probes cited here stand beside this report.

## Required (the decoder's, Animate's)

1. **Row 15's second reading sums only the trains the ledger happens to list** (decoder/books.py:60-75, the verdict
   at :104-114), where the plan reads the wind over every train (TENSOR24.md 837 and 1676; row 15 in part C). On a
   record whose header names trains 0 and 1 and whose one click moves wind from train 1 to train 0
   (decoder_readings.py):
   - a ledger that holds only train 7, which is in no record, reads SHOWN;
   - a ledger that leaves out train 0 reads SHOWN;
   - a ledger that leaves out train 1 reads NOT SHOWN on a lawful record;
   - each time the cause says "the wind over every train agrees", and the tool prints the same.

   The fix: read a round only where its step lines and its clicks lines hold every train of the header's trains; a
   header that names no train reads NOT READ, the cause named. The tests' header then needs its trains.
2. **The first reading cannot fail on a click that books nothing** (books.py:26-57): it sums the holdings and never
   reads the click's own q or train. Each of these reads SHOWN with an agreeing ledger (decoder_readings.py):
   - a whole click with q 5 and no books at all;
   - a take whose windings rise from 4 to 8;
   - a click of train 1 that takes only from train 0.

   The fix: a part with an empty taken reads open; taken windings fall and laid windings rise; where q is given, the
   windings that left equal q; the click's own train is among those taken. The tests' take fixture stands at train 0
   while its windings leave train 1, so it needs the same fix.
3. **The tests miss half of the new guards** (tests/test_the_tensor24_decoder.py): 17 of 18 mutants of the new text
   survive the 46 tests (decoder_mutants_s8.py):
   - raises in place of a named cause: an event without its round, a ledger line without its round or train, a
     holding without its windings, a laid holding without its kept, a clicks line without its wind (KeyError or
     TypeError); the tool raises AttributeError on a record it does not read;
   - wrong readings: SHOWN for a pair booked a second time in the click's laid, SHOWN for one open click out of two,
     SHOWN for clicks lines holding a train the step lacks, and a click with three ends read;
   - removing any whole guard from its tuple fails a test (14 of 14), so the commit's claim holds guard by guard, but
     not for each guard's parts.

   The fix: the 13 tests of part A of decoder_tests_s8.py, which pass on the head and kill all 18 mutants
   (decoder_tests_s8_run.py). Its part B (8 tests) pins items 1, 2 and 4 and fails on the head, as it should.
4. **The ticks reading takes a k that is not a bit** (decoder/clocks.py:24-37): with k = 2 it reads 8 ticks over 4
   beats, with k = -1 it reads -4 (decoder_readings.py), where its own comment counts the beats whose k is 1 and the
   engine's Layout makes k a bit. The fix: unread() names a rate line whose k is not 0 or 1; the schema's Rate line
   says that k is a bit (the Boss's file).

## Follow-ups, none blocking

- **Unchecked value rules (Animate):** an event at site 99 of a one-site board or at site -1, at round 5 of a
  one-round record or at round -3; a float, NaN, true or null in a field the schema does not name; the end's digest
  "", which the tests' own end uses; a whole click at count 0 reading 0 ticks; a rate line that repeats its k. Each
  reads SHOWN.
- **Row 15's order of decision (Animate):** a click that lacks a field, beside a click whose books open, reads NOT
  READ, and the cause hides the open books, where the docstring says a failure at a part read gives NOT SHOWN, as the
  ledger has it (decoder_precedence.py).
- **To settle (Animate):** row 15 in part C compares the two readings ("the change equals the booked"), and the
  decoder holds each against zero and joins them. And "the plan's (section 8, the books)" (books.py:7, the commit
  message, the README) points at TENSOR24_PLAN.md's section on the bang; the books are its section 5, item 8.
- **Quadratic ticks (Animate):** the tool walks a Node-clock's rate lines again for every click: one clock at half
  the full rate over 16,000 rounds takes 39 s, four times longer at each doubling. One pass per Node-clock mends it.
- **Small causes (Animate):** without the tool's lift, the library calls a lawful line of 4,301 digits "no JSON
  object with its kind", where the cause should name the digits; records.read raises ValueError on a path holding a
  NUL, which the tool's arguments cannot carry, but lines_of should catch it.
- **The plan's wording (the Boss):** TENSOR24_PLAN.md's width line says the index tables count "sites below N",
  true of nb; meshes counts Meshes below 3N (its largest value is 80 at N = 27).
- **Notes:** under the lift a number of 10^7 digits takes 17 s, the interpreter's own conversion; the tool's literal
  2 and 3 (tools/tensor24_decode.py:36, 38, 44) stand outside decoder/, where no rule covers them.

## What holds

- **814fe5c45:** both files are scribe-5's blobs, at cceb76371 and at its tip, scribe_scan.py unchanged; the
  self-test is a ratchet of tools/check.py, 808 cases, 0 parted; the lines the fourth review named are gone (runs
  of three capitals 3 to 0, the barred phrase 2 to 0; the two words left are the owner's own, quoted).
- **8469170ad:** the light test's comment counts reproduce, 9,713 of 17,910 and 9,147 for the head's R alone; the
  probe's pin holds, 40 of 40 and 0 of 40 at a5b992c73, and it cannot run at the head; the head_light README's
  mutants and six worlds are the test's own; the stage 2 row and the reviews' README are true.
- **823690afc:** the decoder files are byte for byte reader-5's 5ee08a381 and 4028d0f02; Animate's 50 mutants all
  die and her engine_rates output reproduces byte for byte; in the fifth review's raise probe every case is read or
  named; 6,000 broken records and ledgers and 305 extremes raise nothing, none above 2 s, and 612 runs of the tool
  exit 0 with nothing on stderr; the digits' lift stays inside the tool's own process; decoder/ keeps its folder
  rules read as code (the standard library and record/ alone; no number beyond 0 and 1, no float, raise, clamp,
  operation beyond Rule3's or module state); the decoder's tests went from 15 to 46.
- **The checks:** every fast check passes, and 193 of Tensor24's tests pass; the full check at 823690afc reads 311
  passed, exit 0, the gate's refusals 0 and notes 1.

Each probe runs as `python3 -I <probe> <a worktree of 823690afc> <a scratch folder>`; its output stands beside it.
