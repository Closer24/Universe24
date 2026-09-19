# The worlds of the law of events

Four world files of the one engine (`events-v1`, [the engine](../../docs/ENGINE.md);
[Highlights 5.4](../../docs/HIGHLIGHTS.md#54-the-detector), "The law of
events", the model owner, 2026-09-19). Each is a JSON object with
`"law": "events"`: the board, K and N, the release, the suspension, the
families, the measured events at the start and, where wanted, the detectors.
The engine recognizes nothing by physical name; a run is headless and its
readings are made from the record (`run.json`, `events.jsonl`, `state.json`).
The board is open on every face unless the world declares an axis periodic
(`"boundary": {"z": "periodic"}`: the departures through one face are created
at the opposite face and nothing escapes on that axis; [the engine](../../docs/ENGINE.md)).

| World | What it declares | What its record reads |
| --- | --- | --- |
| `one_content.json` | One measured event of a free family, content 2^24, held in place at the centre of an open 25^3 board; K 2^22, N 64, release 1/128 per Port per unit per self-creation; 200 intervals | The books close at every tick and the content stays constant (what comes home is created again); the flux through every closed surface is the emission; the far field falls as 1/r^2 in the count and the push and as 1/r in the size |
| `two_contents.json` | Two such measured events 8 Links apart on the x axis of an open 21^3 board, no suspension; 200 intervals | Equal and opposite pushes along the line, toward each other: the third law by the symmetry of the two fields |
| `two_slits.json` | A lamp of a paid family (2^22 units per self-creation on every heading), a wall of measured events with two openings 14 apart, a screen of measured events declared as the detector `screen`; 23 x 41 x 9, K 2^34, no suspension; 200 intervals | The detector's clicks by y have a minimum and a maximum away from the axis (the lamp's clock stamps the phases; an event in transit does not turn) |
| `one_slit.json` | The same with one opening | The control: the clicks fall away from the axis without a rise |

Run one:

```bash
python -m event_universe --init examples/events/one_content.json --output artifacts/one_content
```

## The Bell run

The folder [bell/](bell/README.md) holds the ten worlds of the Bell run A2
under the law of events, written by `bell/make_worlds.py`: one bar of
21 x 1 x 1, a lamp of `light` at the centre releasing one unit per
self-creation on +X and on -X, and four counters with phase windows, Alice's
pair at x = 2 and 1 and Bob's at x = 18 and 19, the settings the only
difference between the files. `tools/bell_chsh.py` reads their records and
prints the counts, E, S and every criterion; the register entry is
[A2, under the law of events (2026-09-19)](../../docs/EXPERIMENTS.md#a2-under-the-law-of-events-2026-09-19):
S = 2 exactly, the model's limit, as the reviewers predicted.

## The coupling series

The folder [coupling/](coupling/README.md) holds the twenty-one worlds of
the coupling series C under the law of events, written by
`coupling/make_worlds.py` from one base: a board of 121 x 121 x 1 with the z
axis periodic (a true two-dimensional board, by the model owner's decision
of 2026-09-19 to run the series on two-dimensional boards), a source of
content 2^24 at the centre and probes of content 1 that read (the push
taken, the units mix on). The items: the equivalence (a probe of content m
pushed m times as much, record by record, and a free probe's steps the same
for every m), the third law with unequal contents (4 : 1), superposition,
retardation (the front derived by hand from the mixing rule), the far field
(the ring means of the count, the flow, the carried momentum and the size,
Gauss's flux through the square, the escape; the axis pattern at the
probes), the clock (`suspension` 1: the ages replayed from the sizes read)
and the electric reading (like and unlike charges on the same stream).
`tools/coupling_readings.py` reads their records, replays the source-alone
worlds through the API and prints every criterion; the register entry is
[C, the couplings under the law of events, on the plane (2026-09-19)](../../docs/EXPERIMENTS.md#c-the-couplings-under-the-law-of-events-on-the-plane-2026-09-19).

The isolated tests of the engine are `tests/test_node_mixing.py`,
`tests/test_event_transit.py`, `tests/test_event_suspension.py`,
`tests/test_event_clock.py`, `tests/test_periodic_axis.py` and
`tests/test_event_worlds.py`
([expectations](../../docs/TEST_EXPECTATIONS.md)); the last runs these
worlds' designs on smaller boards and pins their readings as a check that the
engine does what the law says, not as a result.
