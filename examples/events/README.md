# The worlds of the law of the ray

Four world files of the one engine (`rays-v1`, [the law of the ray](../../docs/RAY_LAW.md),
[the engine](../../docs/ENGINE.md); [Highlights 5.4](../../docs/HIGHLIGHTS.md#54-the-detector),
"DECIDED: the law of the ray", the model owner, 2026-09-19). Each is a JSON
object with `"law": "rays"`: the board, K and N, the release, the
suspension, the declared directions, the families (each by its `quantum`:
0 a free family, 1 or more a paid one; the kind is never declared), the
measured events at the start (their tables generated from the families'
keys, a free family read and a paid one measured; a world declares only
the entries that differ, `tools/migrate_ray_worlds.py` having rewritten
these) and, where wanted, the detectors. The engine recognizes nothing by
physical name; a run is headless and its readings are made from the record
(`run.json`, `events.jsonl`, `state.json`). The board is open on every face
unless the world declares an axis periodic (`"boundary": {"z": "periodic"}`).
A ray flies at 1 / sqrt 3 on the digital line of its direction (the flight
table: at most one Link per interval); rays of one number and content that
meet at a Node are permuted by the collision table; a release costs the
emitter by its phase rate (E = h f) and a click measures that content.

| World | What it declares | What its record reads |
| --- | --- | --- |
| `one_content.json` | One measured event of the free family `m` (`quantum` 0; `"phase": false`: its rays carry phase 0 and it never turns), content 2^24, held in place at the centre of an open 25^3 board; K 2^22, N 64, release 1/128 per heading per unit per self-creation on the six headings, `suspension` 1; 200 intervals | The books close at every tick and the content stays constant (what comes home is created again); six ballistic beams of 2^17 per interval, Gauss's flux through every cube equal to the emission once the front has passed; the count on the axes constant with r (a beam does not spread) |
| `two_contents.json` | Two such measured events of `m` 8 Links apart on the x axis of an open 21^3 board, no suspension; 200 intervals | Equal and opposite pushes along the line, toward each other, each the content times the flow of the other's beam at its Node: the third law read on lone beams (read on 2026-09-19: the books close at every tick, the pushes +/-411217348788224 = 2^24 x 187 x 2^17 along x after 200 intervals; its faces click two beams of 2^17 in one interval and their records pass 2^63, exact, [validation](../../docs/VALIDATION.md)) |
| `two_slits.json` | A lamp of the paid family `light` (`quantum` 1; K 2^30, turn 8, 64 rays per self-creation on five directions toward the wall), a wall at x = 8 of the paid family `wall` measuring light (the rule the keys give; no table declared) with two openings at y = 55 and 65 that declare `rerelease` on a fan of 91 primitive directions, a screen at x = 52 of measured events declared as 121 one-Node detectors `screen_<y>` (the screen's pixels) under the reading `wave` (since 2026-09-19 a detector is a set with one record: one detector of 121 Nodes would read one record with no resolution in y); 60 x 121 x 1 with z periodic, no suspension; 500 intervals | The screen's plain count is additive to the unit (no interference in the count); its squared record fringes at lambda = period / sqrt 3, the interference term correlating with the two-source cosine above 0.85 (`tests/test_ray_worlds.py` (a)) |
| `one_slit.json` | The same with one opening | The control: the record without the two-source term |

Run one:

```bash
python -m event_universe --init examples/events/one_content.json --output artifacts/one_content
```

## The Bell run

The folder [bell/](bell/README.md) holds the ten worlds of the Bell run A2
under the law of the ray, written by `bell/make_worlds.py`: one bar of
21 x 1 x 1, a lamp of `light` at the centre releasing one ray per
self-creation on +X and on -X, and four counters with phase windows, Alice's
pair at x = 2 and 1 and Bob's at x = 18 and 19, the settings the only
difference between the files. `tools/bell_chsh.py` reads their records and
prints the counts, E, S and every criterion; the register entry is
[A2, under the law of the ray (2026-09-19)](../../docs/EXPERIMENTS.md#a2-under-the-law-of-the-ray-2026-09-19):
S = 2 exactly, the model's limit, unchanged from the law of events.

## The coupling series

The folder [coupling/](coupling/README.md) holds the twenty-one worlds of
the coupling series C under the law of the ray, written by
`coupling/make_worlds.py` from one base: a board of 121 x 121 x 1 with the z
axis periodic, a source of content 2^24 at the centre releasing six beams on
the six headings, and probes of content 1 that read (the push taken, the
rays go on). The items: the equivalence, the third law with unequal contents
(to the grain of the whole apportioning), superposition, retardation (the
front from the flight table), the far field (the ring means of the count,
the presence and the flow, the flux through the square, the escape; the
axis pattern at the probes), the clock (`suspension` 1: the ages replayed
from the presence read) and the electric reading. `tools/coupling_readings.py`
reads their records, replays the source-alone worlds through the API and
prints every criterion and every reading against the expectations of
[RAY_LAW section 8](../../docs/RAY_LAW.md#8-independent-expectations-for-the-re-registered-readings);
the register entry is
[C, the couplings under the law of the ray, on the plane (2026-09-19)](../../docs/EXPERIMENTS.md#c-the-couplings-under-the-law-of-the-ray-on-the-plane-2026-09-19).

## The orbit series

The folder [orbit/](orbit/README.md) holds the six worlds of the orbit
series D, written by `orbit/make_worlds.py`: the same plane, a fixed source
of content 2^10 releasing one shell every 10 intervals on a fan of 120
primitive in-plane directions (q = 12 units per interval), and a free probe
of content 1 at r = 12 or 24 with the tangential momentum the README derives
for a circular orbit under the measured push law, at the widths of the push
`width` 1, 8 and 32. `tools/orbit_readings.py` reads the probe's steps and
pushes and prints whether the orbit closed, its period, its mean radius,
its drift and the period ratio against the plane's k = 2; the register
entry is
[D, the orbit under the law of the ray, on the plane (2026-09-19)](../../docs/EXPERIMENTS.md#d-the-orbit-under-the-law-of-the-ray-on-the-plane-2026-09-19):
one orbit closes by the criterion (S = 32, r = 12, an eccentric loop), the
mean push reads as derived, the grain of the push breaks the rest.

## The detector definitions

The folder [detector/](detector/README.md) holds four worlds that place
reusable apparatus from `detector/entities/detectors.json` through the
[entity definitions loader](../../docs/ENTITY_DEFINITIONS.md): chains of
measured events measuring a carrier, declared as detectors with thresholds,
one of them reading the tensor component of the one reading.

The isolated tests of the engine are the ten `tests/test_ray_*.py` modules
([expectations](../../docs/TEST_EXPECTATIONS.md)); `tests/test_ray_worlds.py`
runs these worlds' designs on smaller boards and pins their readings as a
check that the engine does what the law says, not as a result.
