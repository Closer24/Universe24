# The check-mode worlds of the new physics

The rows of the check-mode table of ALGEBRA.md 9.87 (4) and the all-families world of 9.87 (5)
as 9.92 (2) amends it, each world beside its blind expectation, no pin (the Boss's record 2133
(2) of 2026-09-26; the rule of reading 9.59 (6): a reading outside the mathematician's band
goes to him before any word). The generator is `make_worlds.py`; the unit test is
`tests/test_check_mode_worlds.py`. Every number is labelled: DETECTOR a click, GAMEBOARD a
diagnostic of the rows, COMPUTATION the declaration's arithmetic, HOST the machine's cost.

    PYTHONPATH=src python examples/events/check_mode/make_worlds.py

## 1. The words and the form

1. **The words are record 2128's.** A world names its `universe`
   (`examples/events/universe.json`, the families and the universe's integers); a body's
   signed number is `q`; its stocks of other families' quanta are `stocks`. The world keys the
   audit of 9.90 (3) deletes are not written (the law's name and version, `K`, `N`,
   `release`, `width`, the flags, the age bound, the universe's integers, the stamp).
2. **No momentum and no spin is declared** (record 2130; 9.98 (3)). A body at rest is its
   standing record: its `seed` is the bound mode's profile over the whole board, both levels
   the profile (as today). A moving body is its record with its tail: its `seed` is
   `{"now": [...], "before": [...]}` over the whole board, the mode times the character of the
   wave number K at which the mode's own group pace is the row's v (9.94 (6)), now at the
   phase K dx + omega_K / 2 and before at K dx - omega_K / 2 from the body's centre along the
   axis of motion (the standing start's symmetric point; at K = 0 the standing record scaled
   by cos(omega / 2)). The hop follows the record (9.98 (3)'s one seam). A spinning body is
   its record's winding: not written here (section 4).
3. **Every body is seeded on its own world** with the other bodies absent (9.96 (4), 9.94
   (2)): the separation rule of 9.35 is retired; two bodies of matter stand anywhere.
   **The bodies' rest pair is [800, 850] and their well [800, 801]** (HOST, the probe of
   2026-09-26): on a GameBoard open on three axes the shipped kind [800, 809] binds no mode on
   a well of side 5, 7 or 9 (the clock 1.9743 to 1.9753 against the band's top 1.9778: the
   band's depth ceiling 2 - 2 x 800 / 809 = 0.022 is too shallow for a small well in three
   dimensions; a well of side 13 binds at 1.9790, too wide for bodies 10 Links apart); the
   kind [800, 850] (omega_0 = 0.345 per interval) binds a well of side 5 at 1.8874 against its
   band's top 1.8824, and a layer's well of side 5 at 1.9165. A one-Node well binds nothing on
   an open board (1.8785 at side 1, 1.8788 at side 3): every body here that hops has its tail
   on a well of side 5 (9.98 (3)); the layer's source of side 10 binds at [800, 803] as well.
4. **The detectors are 9.92's.** A screen is pixels, one detector per Node of a column, the
   pattern compared. A counter is one Node, or the world's receiver face: on a GameBoard open
   on an axis, each face is a detector of its name (`face:+x` and the five others), a slab
   `face_depth` 1 deep; a count in time, no size to declare.
5. **These files load in no loader today.** The words land with the engine's writer (record
   2133, The 3); the loader's two hooks are section 4's. The test reads the structure.

## 2. The table: the rows built, each beside its blind expectation

| The physics | The row (ALGEBRA.md) | The world files | The detector (9.92) | The formula | The blind expectation |
| --- | --- | --- | --- | --- | --- |
| Masses attract and move (Newton) | 9.52 (3) (a) as a pair: two bodies of equal content falling together from rest at 20 Links | `newton_fall.json`: two bodies of 2000 quanta on wells of side 5 (the kind [800, 850], section 1 item 3), centres 20 Links apart on the 48^3 board | none: the meeting is a reading of the bodies' hops | d(t) = d_0 - (M R / (2 Gamma r^2)) t^2 at first order, both bodies | the meeting interval within one hop of the closed form; equivalence: two families alike. COMPUTATION from the formula at M = 2000, R = 2.5, r = d_0 = 20, Gamma = 10^4: the closed form meets at t = 179 intervals |
| Masses attract and move (Kepler) | 9.59 (5), 9.87 (5) (a) with the charges 0 | `kepler_pair.json`: the pair of 9.87 (5), M = 2000 each, 10 Links apart, A along +y and B along -y at v = 0.1 (HOST: K = 0.10697 per Link, omega_K = 0.34251, the rotation at the moving centre 0.33182 per interval, both bodies) | none: the period is a reading of the hops | T^2 = 4 pi^2 a^3 / G (M_1 + M_2) | the period 314 intervals (COMPUTATION, 9.87 (5)) within the draw (9.63 (3)); the falling packet's own row waits (section 4) |
| The charge's rows: Coulomb | 9.64 (1) | `coulomb_plus.json` (Q = +400), `coulomb_minus.json` (Q = -400), `coulomb_neutral.json` (Q = 0), `coulomb_neutral_packet.json` (the packet's q = 0): the layer [200, 120, 1], the source of side 10 and 64 quanta at [100, 60], the packet of q = -1 and one quantum on a well of side 5 passing at b = 20 at v = 1 / 4 along +x (HOST: K = 0.25434 per Link, omega_K = 0.32374, the rotation at the moving centre 0.26016; section 3) | a screen: pixels, one per Node of the column x = 199, the pattern compared | delta = Lambda abs(Q) R / (Gamma b v^2), toward the body for unlike signs and away for like | at Q = 400, R = 5, b = 20, v = 1 / 4: 0.16 radians, the centroid 16 Nodes off the neutral line at the screen; the shifts at +Q and -Q opposite and equal within about 1 percent and the draw; their half-sum the neutral record's shift; the packet at q = 0 reads no charge |
| Magnetism: Ampere and Lorentz | 9.77 (6) (a), 9.78 (9) (a) | `ampere_parallel.json` (the source hopping along +x at 1 / 4 with the packet), `ampere_opposite.json` (the source along -x): Coulomb's world with the source in motion (HOST: the source's K = 0.16646, omega_K = 0.21698, the rotation 0.17537) | the same screen | the force times 1 - (v / c_l)^2 for parallel motion, 1 + (v / c_l)^2 for opposite | 13 Nodes parallel and 19 opposite against 16 with the source at rest (`coulomb_plus.json`); a neutral pair unchanged |
| The recoil: radiation pressure | 9.84 (5) (a) | `radiation_pressure.json`: an emitter body of 64 quanta with a stock of 100 of the charge family's wave, its train of 8 periods along +x over [32, 5, 5] (the given clock [512, 1] on N = 1024, the wavelength 4 Links) on the board [400, 21, 21]; the target, a body of 64 quanta on a well of side 5 centred in the beam at x = 300; `radiation_pressure_beside.json`: the same target beside the beam, its Nodes outside the beam's cross-section | the faces (counters); the hop is a reading of the target's record | Delta n = (W P_body) div (M lambda_q) per quantum taken | the target hops along +x by the momentum's whole part after 100 quanta; the target beside the beam: no hop |
| The recoil: the emitter | 9.84 (5) (b) | `train_recoil.json`: the emitter body of 64 quanta giving 10 quanta along +x as a train; `point_recoil.json`: the same body as a point emitter at the window g = 4 | the faces (counters) | the same count of momentum, opposite | the train emitter recoils along -x by the same count; the point emitter: no net hop |
| Every family with every other | 9.87 (5), 9.92 (2) | `all_families.json`: the pair with q = 50 on both (Lambda Q = 50 at Lambda = 1), A a point emitter of a stock of 200 at the window g = 4, the 48^3 board open on every face, no D; A's spin waits (section 4) | the six faces, counters (an open face is a detector of its name) | 9.87 (5) (a) to (h) | (a) the period 363 +- 3 against 314 with the charges 0 (`kepler_pair.json`); (b) 1.4 intervals per orbit, 14 +- 3 over ten orbits; (e) at +x and -x the arrival intervals modulated by -+ 17 percent at the orbital period, the mean interval at every face 1.2 percent above A's own period; (f) the total momentum the start's at every interval; (g) the sum of q constant, the leak test on every unsourced component; (h) the backward run exact |

## 3. The moving records (HOST, the generator's numbers)

| World | Body | v (Links per interval) | K (per Link) | omega_K (per interval) | omega_K - K v |
| --- | --- | --- | --- | --- | --- |
| `kepler_pair.json`, `all_families.json` | A (+y), B (-y) | 0.1 | 0.10697 | 0.34251 | 0.33182 |
| `coulomb_plus.json`, `coulomb_minus.json`, `coulomb_neutral.json`, `coulomb_neutral_packet.json`, `ampere_parallel.json`, `ampere_opposite.json` | the packet (+x) | 0.25 | 0.25434 | 0.32374 | 0.26016 |
| `ampere_parallel.json` (+x), `ampere_opposite.json` (-x) | the source | 0.25 | 0.16646 | 0.21698 | 0.17537 |

The rotation at the moving centre is the mode's own dilation (9.63 (3), 9.94 (6)); the rule
alone is to produce it (9.98 (3)), and the rows read whether it does.

## 4. The rows that wait, each with its missing line

| The physics | The row | What is missing |
| --- | --- | --- |
| Einstein's rows: the redshift, the light clock in motion, the bending, Shapiro's delay | 9.59, 9.62, 9.65 | built in `../toward_nature/` and `../dark_body/` (one canonical copy); re-read in check mode after 9.98 (5) stage (a), in the words of record 2128 when the generators move to them |
| The point emitter's tick | 9.85 (5), 9.75 | built in `../point_emitter/`; row (iv) fixed at the stroke's commit 7 |
| Masses fall (the packet in a content gradient) | 9.98 (7) | the blind value waits for the mathematician's fix (record 2132 (2): measured on the envelope) |
| The vector part: the dragging on the ring, the gyroscope, the matter wave around the ring | 9.77 (6) (b), 9.78 (9) (e), 9.81 (8) (d) | the ring at R = 10 with the test body at r = 30 needs a board of 72^3 (373248 Nodes): a whole-board record of two levels per body, five bodies, is about 25 MB per world; waits for the record on its support alone (9.98 (3): 27 to 125 Nodes), the loader's line. The gyroscope's spin and A's spin S = 1000 wait for THE WINDING'S LINE: how a record's winding about an axis is written for a given S (the winding number as a function of S and the count s) |
| The tensor part: the wave of gravity | 9.78 (9) (c), (d) | the interferometer's arms of 600 Links need a board beyond a whole-board record; and 9.98 (5) stage (b) (the source from the record's stress) is held (record 2132 (3)) |
| Faraday's induction | 9.78 (9) (f) | a body that starts to hop at the tenth interval: under the rule alone a body moves by the paces around it, so the start of motion needs a cause in the world (a declared level, or a second body's passage); the world's line |
| The sign, body against wave; Aharonov and Bohm | 9.81 (8) (b), (a) | a declared uniform or curling vector level is no key of 9.90 (3); under record 2128 a level comes from a body's declaration (a wound record's dipole): the world's line, and the winding's |
| The atom's binding | 9.64 (2) | the charged record's bound mode on the charge well: the generator's eigenproblem on the charge family's reads, not built |
| The recoil: the heavy tool | 9.84 (5) (c) | a target of a million quanta is refused by the pace guard today (the amount is the content at the Node, and 10^6 is not below Gamma = 10^4; 9.48 (3)); it waits for P_0 = [1, 1000] (9.96 (3), the stroke's commit 5), under which its count is s = M div (1000 P); the generator's `WAITING` entry writes it by name then |
| The train emitter | 9.84 (5) (b), the train half | `train_recoil.json` and the beam worlds carry the emitter's `train` keys; 9.90 (3) deletes them when the point emitter lands (commit 7), and the row's train half goes with them |

The loader's two hooks for The 3 (record 2133: the exact lines go to the engine's writer):
1. `seed` as an object `{"now": [...], "before": [...]}` over the whole board on a body: the
   record's two levels, the moving body's (9.98 (3)); a list stays the standing profile at
   both levels.
2. The universe file's name and the three words of record 2128 (`universe`, `q`, `stocks`).

## 5. The generator's run

The thirteen worlds were written on 2026-09-26 by the generator on the branch stroke-side
(HOST): the cube's bodies seed in about 4 seconds each, the layer's in under a second, the
beam's emitter with its train's flux check in about a minute; the files hold the records over
the whole board, one line per integer list (`kepler_pair.json` and `all_families.json` about
1.5 MB each, `newton_fall.json` 0.75 MB, the layer's about 0.3 MB, the beam's 0.6 to 1.1 MB).
The sizes are the whole-board record's; the record on its support alone (9.98 (3)) is the
loader's line (section 4).
