# The decoder, first slice (Animate)

The owner's word to the Boss, 16:1x UTC (6474211874): "Approved, build it. You on the engine. Animate on the decoder." His word to Animate, 16:4x UTC (Hebrew, translated): "Are you building the decoder or waiting?" His order of 16:3x UTC, through the Boss: "I will be back in 12 hours. Sync everyone, build everything and check it. Push when ready."

The decoder's modules moved out of this folder into src/tensor24/decoder (reader-5 c94ecaa9), to the record's schema 1.0 (src/tensor24/record/schema.py). They carry the fifth hostile review's three changes, its follow-ups and Sofer's G1 to G3 since reader-5 5ee08a38 (#2187, 6479895768 and 6478265426). This folder keeps the first slice's run on the committed records, the engine's own beats read back, and the decoder's mutants.

## The files

- **src/tensor24/decoder/records.py,** the record reader. The file is split at the line feed alone, so U+2028, U+0085 and U+2029 stand inside a label. The schema's rules are its guards, checked in order:
  - every line is a JSON object with its kind, each key once; a line nested past the interpreter's depth, or holding a whole number past its digits, is no JSON object to the reader (the tool lifts the digits' bound);
  - the record holds a header and an end;
  - the header comes first, with a whole major version that is known;
  - the end comes last;
  - every event is of a known kind and stands at a whole round and site;
  - every field a line holds has its shape in the schema's record of its kind: a whole number, a label, a row of the schema's length, or a record of the schema, so a float, a truth value, NaN or a row of another length is seen (Sofer's G1 and G2);
  - a whole click with ends books in its two ends alone, and one that takes at one end holds no end (G3);
  - the events keep the schema's order.

  A record that breaks a rule is not read, with the cause named; nothing is raised. A field may stand absent where its writer lacks it, and a reading that needs it reads not read, the cause named. The ledger has its own guards: every line a JSON object, at a whole round and train, after the step or the clicks, with its fields of their shape, each place once.
- **src/tensor24/decoder/books.py,** row 15's two readings:
  - the books at every whole click: windings and kept together gain nothing over its holdings, at its two ends where it takes at both; a whole click that lacks a field its books are read from reads the row not read, the click named;
  - the plan's second reading (section 8): the wind over every train after the clicks against after the step, at every round with a click, whole or split, read where the round's two lines hold the same trains with their whole wind.

  Shown where both hold everywhere; not shown where either fails at a part read; not read with no whole click, with the ledger absent or not read, or with the ledger read at no round with a click or at some alone.
- **src/tensor24/decoder/clocks.py,** each Node-clock's ticks counted from its rate lines, read where the lines stand from its first beat with whole counts and k, the counts rising; else not read, the cause named.
- **tools/tensor24_decode.py,** the decoder's tool: the usage line with no argument (exit 2), the digits' bound lifted, row 15's verdict, and the whole clicks' ticks with the first not read named. **tests/test_the_tensor24_decoder.py,** 46 tests: each broken record and ledger not read with its own cause and read or raising without its own guard, each reading's law failing on its own mutant, the tool run as a program.
- **tools/tensor24_convert.py,** the converter (Animate's tool, outside src/tensor24): a head record in the schema 1.0. The head's proper time is written as rate lines that give its ticks exactly at each of its clicks, its books as holdings of the amounts it moved, and its winds as the ledger at "clicks" alone.
- **first_slice.py and first_slice.txt:** the three committed records (examples/records: bodies, chiral and hole) converted, read back by the package, counted against the head's own counts, read for row 15 beside the head's reader, and their whole clicks' ticks read against the head's own proper time.
- **engine_rates.py and engine_rates.txt:** the engine's own beats under random masks (the Mesh test's parted layouts), written as rate lines in a record, read back by the package at every beat.
- **mutants.py and mutants.txt:** 50 source mutants of the decoder and its tool, the fifth review's sixteen among them on the new text, each run against the tests.
- **review_raises.txt:** the fifth review's own probe (derive/hostile_reviews/fifth/decoder_raises.py, its interpreter's path set to this bench's) on tensor24-review at 13672be1e with 5ee08a38 picked onto it: every case read or named, nothing raised, the tool's every run exit 0.

## What it reads

- **Every converted record reads under the schema's rules,** the new guards included, and its counts match the head's: whole clicks 138, 2,745 and 1,327; books 116, 54 and 71; turnovers 1,934, 861 and 1,073.
- **The ticks at the whole clicks,** read from the rate lines, are the head's own at every click: 138, 2,745 and 1,327 of as many.
- **Row 15 reads NOT READ on all three:** the books close at every whole click (4,210 of 4,210), and the converted ledger, the head's winds once a round at "clicks" alone, is read at 0 of 25, 54 and 47 rounds with a click.
- **The step's change, a reading of its own:** the wind over every train moved on every round with no click (94 of 94, 5 of 5 and 12 of 12).
- **The engine's beats** (engine_rates.txt): the ticks read back right at 1,349, 1,358 and 1,414 beats of as many on three seeds; a Node-clock's lines with the first dropped, and a site with no rate line, read not read with the cause named.
- **The mutants** (mutants.txt): 50, none surviving.

## Next

- The rows' readings by part C (ANIMATE-TENSOR24-READINGS.md, K1 to K8), each row with its two readings' fields disjoint, and a control record that reads SHOWN and one that reads NOT SHOWN.
- For stage 9's writer: the first reading sums a click's windings and kept across its trains as one unit, and the second reads the kept inside its train's wind; the writer's test pins both or names the unit.

---
Animate, reader-5.
