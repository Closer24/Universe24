# Newton on the side, Side A: the moving detector with mass, read at a receiver body (2026-09-23)

The three worlds of Side A of
[Newton on the side](../../../docs/designs/newton_clicks/NEWTON_ON_THE_SIDE.md)
(sections 3 and 4; the model owner's words, records 1043, 1046 and 1098
of [the log](../../../docs/LOG_2026-09-20.md); the order of record 1128
(a), item 4), written by `make_worlds.py` beside them with the pins
before any run in `expectations.json`; the chain of steps between click
and click, the pins by kind with their arithmetic, the checks before the
run and, after the owner's go, the readings, in
[RUN_14.md](../../../docs/designs/fail_rows/RUN_14.md). The reading tool
is `tools/newton_side_readings.py`; its test
`tests/test_newton_side_readings.py`.

The side alone, never the law: series K's box (57 x 41 x 41, open), the
lamp A at (2, 26, 20), the held mass at (28, 20, 20) (the impact distance
b = 6), the receiver plane at x = 54 (L = 26 Links from the mass's plane,
52 from the lamp); the lamp's family the massive family `matter` on the
exact rung k = 19 of the ladder of velocities (M_row = 21 units per row,
the label magnitude p = 71: E'_0 = Q S M_row = 1344, E'_D = isqrt(1344^2
+ 3 x 71^2) = 1349 = 19 x 71, one Link per 19 counts with no remainder);
the pair `suspension` [1, 4096]; `optical` 1 declared (c_f = 2);
`clock_stamp` true; the receivers 1681 fixed bodies of `wall` measuring
the row, no detector set (a set without a body has no count, record
768). One declaration departs from the design's section 4.3, found by
the algebra of the steps before the run (RUN_14.md step 5, section 4):
the receivers' entry reads the presence and not the row's age, since a
body's clock counts the age moment of the rows at its Node on every
entry but one reading `presence`, and the arriving row is such a row at
the receiver's Node: under `age` every click would stretch the
receiver's own count by 979 / 4096 and no control click could read 979.

| World | The lamp's family | The held mass | The pins (COMPUTATION before the run; DETECTOR when read) |
| --- | --- | --- | --- |
| `control.json` | `matter` (21, 71) | none | the arrival count 979 on every click (n_B at the click less the row's ordinal; the birth's convention one count); the arrival Node the line's end; the pace 52 / 979 within 2 / 979 of 1 / 19; the count ratio 1.000 |
| `mass.json` | the same | 2^10 on series E's fan of 290 | the arrival 40.5 +- 3.5 counts earlier (the wall +0.68, the push -41.19; conditional on k_a(b) = 6.95 x 10^-4); the centroid 4.39 +- 0.5 pixels toward the mass (4.46 under the crossing count, not separable); the count ratio 1.000 within 1 per cent |
| `light.json` | `light` (series K's photon) | 2^16 (the gr_rows pin world's) | the deciding pin: the lever-arm centroid 4.63 +- 0.5 pixels toward the mass under the arrivals count against 5.47 +- 0.5 under the crossing count (the design's -4.63 against -5.47 in series K's sign); the wall's delay +3.96 +- 1 on the heading's 89, no advance |

Every number the tool prints is a DETECTOR reading (a click's Node, the
receiver's own count `clock`, the row's ordinal `record` mod 2^32, the
row's age), a COMPUTATION on them (a difference, a ratio, a centroid, the
control's count derived from the world's integers before it is read) or
a GAMEBOARD diagnostic (the tick), labelled; only the first is compared
with a pin. A control off 979, or two control clicks differing, refutes
the rung and stops the run (RUN_14.md section 3).

    PYTHONPATH=src python examples/events/newton_side/make_worlds.py
    PYTHONPATH=src python tools/run_series.py examples/events/newton_side --output artifacts/newton_side
    PYTHONPATH=src python tools/newton_side_readings.py artifacts/newton_side
