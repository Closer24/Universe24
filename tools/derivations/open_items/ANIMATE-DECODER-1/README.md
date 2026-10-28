# The decoder, first slice (Animate)

The owner's word to the Boss, 16:1x UTC (6474211874): "Approved, build it. You on the engine. Animate on the decoder." His word to Animate, 16:4x UTC (Hebrew, translated): "Are you building the decoder or waiting?" His order of 16:3x UTC, through the Boss: "I will be back in 12 hours. Sync everyone, build everything and check it. Push when ready."

The decoder's modules moved out of this folder into src/tensor24/decoder (reader-5 c94ecaa9), to the record's schema 1.0 (src/tensor24/record/schema.py). This folder keeps the first slice's run on the committed records.

## The files

- **src/tensor24/decoder/records.py,** the record reader. The schema's rules are its guards, checked in order:
  - every line is a JSON object with its kind;
  - the record holds a header and an end;
  - the header comes first, with a whole major version that is known;
  - the end comes last;
  - every event is of a known kind and stands at a whole round and site;
  - the events keep the schema's order.

  A record that breaks a rule is not read, with the cause named; nothing is raised (Sofer's first finding, 6475078370).
- **src/tensor24/decoder/books.py,** row 15's two readings:
  - the books at every whole click: windings and kept together gain nothing over its holdings, at its ends where it takes at both;
  - the ledger's clicks less its step, per round and train, against the round's clicks.

  A record with no whole click reads NOT READ, "no whole click" (Sofer's second finding).
- **src/tensor24/decoder/clocks.py,** each Node-clock's ticks counted from its rate lines.
- **tools/tensor24_decode.py,** the decoder's tool; **tests/test_the_tensor24_decoder.py,** 15 tests, each broken record failing without its own guard and each reading's law failing on its own mutant.
- **tools/tensor24_convert.py,** the converter (Animate's tool, outside src/tensor24): a head record in the schema 1.0. The head's proper time is written as rate lines that give its ticks exactly at each of its clicks, its books as holdings of the amounts it moved, and its winds as the ledger at "clicks" alone.
- **first_slice.py and first_slice.txt:** the three committed records (examples/records: bodies, chiral and hole) converted, read back by the package, counted against the head's own counts, read for row 15 beside the head's reader, and their whole clicks' ticks read against the head's own proper time.

## What it reads (first_slice.txt)

- **Every converted record reads under the schema's rules,** and its counts match the head's: whole clicks 138, 2,745 and 1,327; books 116, 54 and 71; turnovers 1,934, 861 and 1,073.
- **The ticks at the whole clicks,** read from the rate lines, are the head's own (its proper time by the full rate) at every click: 138, 2,745 and 1,327 of as many.
- **Row 15 reads NOT READ on all three:** the books close at every whole click (4,210 of 4,210, the chimes included), but no round of the converted ledger holds both its step and its clicks lines, since the head writes its winds once a round. The head's reader reads it SHOWN exact on the chiral and the hole, from the births alone, and NOT READ on the bodies.
- **The step's change, a reading of its own** (and no longer row 15's): the wind over every train moved on every round with no click (94 of 94, 5 of 5 and 12 of 12), light's train on all of them.

## Next

- The rows' readings by part C (ANIMATE-TENSOR24-READINGS.md, K1 to K8), each row with its two readings' fields disjoint, and a control record that reads SHOWN and one that reads NOT SHOWN.

---
Animate, reader-5.
