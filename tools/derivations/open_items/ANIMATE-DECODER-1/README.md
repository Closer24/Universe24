# The decoder, first slice (Animate)

The owner's word to the Boss, 16:1x UTC (6474211874): "Approved, build it. You on the engine. Animate on the decoder." His word to Animate, 16:4x UTC (Hebrew, translated): "Are you building the decoder or waiting?"

The modules are staged here until stage 0a gives src/tensor24/decoder/, and then move there whole. Nothing here is engine code.

## The files

- **tools/tensor24_convert.py,** the converter (Animate's tool, outside src/tensor24): writes a head record in the record's schema version 1 (6474766574), with the three corrections below.
- **records.py,** the record reader. It checks four things as it reads:
  - the header comes first and the end last;
  - the major version is known;
  - every line kind is known;
  - the events stand in the schema's order.

  A record that breaks a rule is not read, with the cause named; nothing is raised. It uses the standard library alone.
- **books.py:** row 15's first reading, K3, the books at every whole click, or at each end where a click takes at both.
- **first_slice.py and first_slice.txt:** the three committed records (examples/records: bodies, chiral and hole) converted, read back, counted against the head's own counts, and read for row 15 beside the head's reader.

## What it reads

- **Every converted record reads under the schema's rules,** and its counts match the head's:
  - whole clicks equal credits and births: 138, 2,745 and 1,327;
  - the books entries: 116, 54 and 71;
  - the turnovers: 1,934, 861 and 1,073.
- **Row 15's first reading closes at every whole click on all three,** 4,210 clicks, the chimes included; the head's reader read the births alone. The hole holds 28 fittings, 6 of them pairs into light with their books per end.
- **Row 15 itself reads NOT READ on the converted records:** its second reading is the ledger's, and the converter writes no ledger. The head's reader reads it SHOWN exact on the chiral and the hole, from the births alone, and NOT READ on the bodies, which hold no birth.

## The schema's three corrections, for 0b

1. **`steps` beside `dial` at every click:** the Node-clock's whole dial turns so far (its proper ticks), which the runner counts from Out's k. The head's `proper` is steps times the full rate plus the dial (Rule3).
2. **A `books` line:** a remainder booked at a Node-clock, signed (law 8's books per Node-clock).
3. **`ends` on a whole click that takes at both ends** (a pair into light): each end's site, its books (taken, laid, remainder) and its push.

## Next

- The ledger, from the head's per-interval nodes: the conservation rows' second reading.
- The rows' readings by part C (ANIMATE-TENSOR24-READINGS.md, K1 to K8), each row with its two readings' fields disjoint, and a control record that reads SHOWN and one that reads NOT SHOWN.

---
Animate, reader-5.
