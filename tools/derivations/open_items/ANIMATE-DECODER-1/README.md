# The decoder, first slice (Animate)

The owner's word to the Boss, 16:1x UTC (6474211874): "Approved, build it. You on the engine. Animate on the decoder." His word to Animate, 16:4x UTC (Hebrew, translated): "Are you building the decoder or waiting?" His order of 16:3x UTC, through the Boss: "I will be back in 12 hours. Sync everyone, build everything and check it. Push when ready."

The decoder's modules moved out of this folder into src/tensor24/decoder (reader-5 c94ecaa9), to the record's schema, now 1.1 (src/tensor24/record/schema.py). They carry:
- the fifth hostile review's three changes, its follow-ups and Sofer's G1 to G3 (reader-5 5ee08a38; #2187, 6479895768 and 6478265426);
- the seventh hostile review's four changes and its follow-ups (#2187, 6482763700; derive/hostile_reviews/seventh/REPORT.md).

This folder keeps the first slice's run on the committed records, the engine's own beats read back, the decoder's mutants and the reviews' probes as run here.

## The files

- **src/tensor24/decoder/records.py,** the record reader. The file is split at the line feed alone, so U+2028, U+0085 and U+2029 stand inside a label. A line that is no JSON object is named with its cause: no JSON, nested past the interpreter's depth, or holding a whole number past its digits (the tool lifts the digits' bound); a path that cannot be opened, a NUL in it among them, is named too. The schema's rules are its guards, checked in order:
  - every line is a JSON object with its kind, each key once;
  - the record holds a header and an end;
  - the header comes first, with a whole major version that is known;
  - the end comes last;
  - every event is of a known kind and stands at a whole round and site;
  - every field a line holds has its shape in the schema's record of its kind (a whole number, a label, a row of the schema's length, or a record of the schema), and a field the schema does not name holds whole numbers and labels alone, the schema's first line: a float, a truth value, NaN, null or a row of another length is seen (Sofer's G1 and G2);
  - every value stands on the record: a round from 1 to the end's rounds, a site on the board the header's sides make (the click's, its ends' and its children's), a Spoke among the board's, a count from the first beat. The digests are the runner's, which the decoder never reads (TENSOR24.md);
  - a whole click with ends books in its two ends alone, and one that takes at one end holds no end (G3);
  - the events keep the schema's order.

  A record that breaks a rule is not read, with the cause named; nothing is raised. A field may stand absent where its writer lacks it, and a reading that needs it reads not read, the cause named. The ledger has its own guards: every line a JSON object, at a whole round and train, after the step or the clicks, with its fields of their shape, each place once.
- **src/tensor24/decoder/books.py,** row 15's two readings:
  - **the books at every whole click** (K3): each part takes (its taken holds a holding), each taken holding loses and each laid one gains, its windings and kept together, and over the part's holdings the windings and the kept together gain nothing; the click's own train is among those it takes from; where it holds its q, q whole windings left. A take paid from its remainder alone moves no whole winding (the head's credits do so: 2,557 on the chiral and 1,047 on the hole), so a holding is read by its windings and kept together. A whole click that lacks a field its books are read from (its ends, a part's books, a holding's train, windings and kept) is named;
  - **the plan's second reading** (TENSOR24.md section 19, item 8; TENSOR24_PLAN.md section 5, item 8): the wind over every train of the header after the clicks against after the step, at every round with a click, whole or split. A round is read where its step lines and its clicks lines hold the header's trains and no other, each with its whole wind; a header that names no train is named.

  The verdict: not read with no whole click, with the ledger absent or not read, or with a header that names no train; not shown where a part read fails, the books at a whole click read or the wind at a round read, with the rest named beside it; else not read where a whole click lacks a field or a round with a click is not read; else shown. Part C's "the change equals the booked" is each reading held against 0: a click keeps its remainder in the train it took from, so the change over every train is what it booked, 0 where its books close.
- **src/tensor24/decoder/clocks.py,** each Node-clock's ticks counted from its rate lines, read where the lines stand from its first beat with whole counts, each k a bit (the schema's Rate line under the second promise), the counts rising and no k repeated; else not read, the cause named. A Node-clock's lines are read once for all its counts, the ticks before each stretch summed once and each count found by bisection.
- **tools/tensor24_decode.py,** the decoder's tool: the usage line with no argument or more than two (exit 1 + 1), the digits' bound lifted, row 15's verdict, and the whole clicks' ticks with the first not read named, each Node-clock's lines read once. Its numbers are spelt from 0 and 1, as the files' tool spells them.
- **tests/test_the_tensor24_decoder.py,** 75 tests: each broken record and ledger not read with its own cause and read or raising without its own guard, the clicks whose books do not hold them, the wind over the header's trains, the precedence of a failure over a gap, each reading's law failing on its own mutant, the tool run as a program.
- **tools/tensor24_convert.py,** the converter (Animate's tool, outside src/tensor24): a head record in the schema 1.1. The head's proper time is written as rate lines that give its ticks exactly at each of its clicks, its books as holdings of the amounts it moved, and its winds as the ledger at "clicks" alone. A whole click's train is the train its windings left; its q is left out, the head counting its levels where its books count amounts. Its numbers are spelt from 0 and 1, as the decoder's tool spells them (Sofer's gate reads both tools under its amendment 4).
- **first_slice.py and first_slice.txt:** the three committed records (examples/records: bodies, chiral and hole) converted, read back by the package, counted against the head's own counts, read for row 15 beside the head's reader, and their whole clicks' ticks read against the head's own proper time.
- **engine_rates.py and engine_rates.txt:** the engine's own beats under random masks (the Mesh test's parted layouts), written as rate lines in a record, read back by the package at every beat.
- **mutants.py and mutants.txt:** 114 source mutants of the decoder and its tool: each guard dropped, each part of each rule, reading and verdict changed, the fifth review's sixteen and the seventh's eighteen among them on this text.
- **review_raises.txt** and **review_readings.txt:** the fifth review's decoder_raises.py and the seventh's decoder_readings.py, as run here on this text.

## What it reads

- **Every converted record reads under the schema's rules,** every new guard included, and its counts match the head's: whole clicks 138, 2,745 and 1,327; books 116, 54 and 71; turnovers 1,934, 861 and 1,073.
- **The books hold every converted click:** 4,210 of 4,210 close under the new rules.
- **The ticks at the whole clicks,** read from the rate lines, are the head's own at every click: 138, 2,745 and 1,327 of as many.
- **Row 15 reads NOT READ on all three:** the converted ledger, the head's winds once a round at "clicks" alone, is read at 0 of 25, 54 and 47 rounds with a click.
- **The step's change, a reading of its own:** the wind over every train moved on every round with no click (94 of 94, 5 of 5 and 12 of 12).
- **The engine's beats** (engine_rates.txt): the ticks read back right at 1,349, 1,358 and 1,414 beats of as many on three seeds; a Node-clock's lines with the first dropped, and a site with no rate line, read not read with the cause named.
- **The mutants** (mutants.txt): 114, none surviving.
- **The ticks in one pass:** one Node-clock at half the full rate with a whole click at every round reads in 0.30 s at 4,000 rounds and 1.12 s at 16,000, where the walk per click took 7.4 s at 4,000.

## Next

- The rows' readings by part C (ANIMATE-TENSOR24-READINGS.md, K1 to K8), each row with its two readings' fields disjoint, and a control record that reads SHOWN and one that reads NOT SHOWN.
- For stage 9's writer: the first reading sums a click's windings and kept across its trains as one unit, and the second reads the kept inside the wind of the train it was taken from; the writer's test pins both or names the unit.

---
Animate, reader-5.
