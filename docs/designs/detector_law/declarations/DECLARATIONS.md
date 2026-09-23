# The six declarations in the one form, before any run: Bell's CHSH sum (1a), the no-signalling marginals (1d), the Mach-Zehnder visibility (2b), the moving lamp's redshift (4b), Malus at 45 degrees (9) and Malus at three new settings (the chief physicist, 2026-09-23; docs only, no run)

The Boss's order of 2026-09-23, about 17:12Z, on the owner's word of 16:55Z
(everything anew on the new engine): the six PIN rows of `../SCHEDULE.md`
whose declaration was missing, each written in the one form of
`docs/designs/system_algebra/AUDIT.md` section 4 (the objects as ALGEBRA.md
objects, the declared integers with their kind, the verbs, the pins as
closed forms before any run, the readings by kind, the identity), then the
descent to the world file (the keys, nothing the declaration does not
name), the run once and headless, the reading by kind. Under the new law
(`../DESIGN.md`: the ray splits at every free Node inside the board; a
receiver is one of the four forms, the mirror, the sponge, the Port's take
or the TABLE; `../MASSIVE_RECORD.md` where a row needs mass). Nothing of
the previous engine's readings is a pin here; each row's old reading is
named as HISTORY in `../SCHEDULE.md`. A number whose kind is not named is
not a result.

**The one declaration these six share, made here (DESIGN.md's fourth
receiver form, "the table", and Reviewer 3's SHOULD of 08:48Z): THE PHASE
READING.** Under the rule a record at a Node is the pair of levels
(a_before, a_now) and no phase label; a table (a polariser, a splitter)
reads the record's phase as THE ANGLE ON THE PHASE CIRCLE Z_N NEAREST TO
THE PAIR (a_before, a_now) AT THE RECORD'S CLOCK: with the family's clock
the pair [p, q] on N (the phase per Link, the period 2 pi q / p intervals)
the pair (a_before, a_now) = A (cos(phi - omega), cos phi) determines phi
on Z_N by the phase table at load (`core.phase.phase_cosines`, cos x 256,
immutable law data; the nearest table entry, an integer comparison, no
root and no float at run time); the table's action is then the algebra's
own on that phi (the rotation **U**_s of ALGEBRA.md 3.6 for a polariser,
the split's integer matrix of 4.6 for a splitter), and the click the
rung on the table's weights (4.12). The reading is a declared input of
kind 2 (the pair's nearest angle, its remainder the grain 1 / N); the
engine does not carry it yet (DESIGN.md: "until the reading is declared
in the engine, the tables of Malus and Bell are unchanged from the
amplitude law only in form"); it is one component under the key, written
by the builder against this paragraph, with one test: a record of a
declared phi read back as phi at every u of the wheel.

## 1. Row 1a, the CHSH sum S of a pair

1. The objects. The torus: a bar of 21 x 1 x 1, y and z periodic of one
   layer (the folded axes read the Node itself), x open, its two faces
   sponges that do not read (DESIGN.md's face forms; ALGEBRA.md 1.6). The
   phase circle Z_N. The family `light`, h = 1, the pair form of its clock.
   The pair record: one lamp at x = 10 releasing one record with two arms
   (+x Alice's, -x Bob's) and two joint labels 00 and 11 of weight 1 each,
   psi = (00) + (11) in Z^2 (x) Z^2 tensored with its phase in Z[Z_N]
   (ALGEBRA.md 3.6; the amplitude series' `arms` 2 and `branches` [[0, 1],
   [3, 1]]), born on one birth stamp with opposite trains (DESIGN.md 6.3).
   Two polarisers as foreign objects of the TABLE form at x = 7 (Alice)
   and x = 17 (Bob), each with its setting s (the `phase_window` integer)
   and the rotation **U**_s = [[C'[s], S'[s]], [-S'[s], C'[s]]] on the
   half-angle tables at 1 / 256 (**U**_s^T **U**_s = n_s **I** exactly);
   each a detector set of one Node reading the joint gather (3.1). The
   four CHSH worlds are the four settings pairs (a, b), (a, b'), (a', b),
   (a', b') at the labels 0, N / 8, N / 4, 3 N / 8 (the L3 series'
   `bell_<a>_<b>` and `bell_n<N>_<a>_<b>`), copied as declared integers.
2. The declared integers (kind 2): N = 2048 (the wheel [1, N], W = N; the
   finite-N Bell value at its limit, ALGEBRA.md 4.10), K, Q, S and the
   release as the L3 series declares them, h = 1, the train 128 periods
   (the coherence a fortieth of the path difference, DESIGN.md 6.2), the
   settings s_A in {0, N / 4}, s_B in {N / 8, 3 N / 8}, 300 intervals; the
   phase reading above.
3. The verbs. The flight (T, D) of each arm's row on its own line, the
   phase turned per Link, nothing of one arm written on the other (B1);
   the ray splitting at every free Node (the rule of DESIGN.md section 2);
   the rotation at the bar by **U**_s (verb (B), rule R, ALGEBRA.md 3.6)
   on the phase read as declared; the ONE GATHER (G) of the one record
   from both settings at the completion interval, the joint pointer
   J(o_A, o_B) = SUM over the labels l of U_a[o_A][l] U_b[o_B][l], the
   cell's weight R = J^2, the birth wheel's u selecting one of the four
   cells through the rung (E, D; B3, P6).
4. The pins (COMPUTATION, before the run, from ALGEBRA.md 4.9 and 4.10):
   the correlation E(a, b) at each settings pair the finite-N Bell value
   of the tables; S = E(a, b) - E(a, b') + E(a', b) + E(a', b') = 181 / 64
   = 2.828125 exactly at N = 2048 with the wheel [1, N] (the L3 series'
   COMPUTATION; the registered 2.75 in the unit 64 is the N = 64 pilot's,
   HISTORY); recomputed by the generator's `bell.py` under the declared
   phase reading before the run and written to `expectations.json`; the
   falsifier S outside 2.42 +- 0.40 (two standard errors of Hensen 2015)
   or above 2.828; the nature row S = 2.42 +- 0.20 (NATURE; the electron
   spins in diamond at 1.3 km; no medium).
5. The readings by kind: DETECTOR the joint clicks per cell (++, +-, -+,
   --) per settings pair over the births (the `gather` lines' chosen
   cells); COMPUTATION the correlations and S from the counts; GAMEBOARD
   the gathers' weights and the books; no CONVERSION.
6. The identity: `detector-law-v1` with the table form; the phase reading
   a declared input, no hypothesis beside the law.

The descent: `shape` [21, 1, 1], `boundary` {x open, y and z periodic},
`N`, `families` [light with `phase_per_link` the pair], the lamp's
`arms` 2 and `branches`, `train` 128, the two polarisers' `table` with
`phase_window` s (the TABLE form's key of the first build, `read` and
`sum` as the amplitude series names them), `detectors` Alice and Bob
reading the joint gather, `clock_stamp` true, `detector_law` true,
`ticks` 300. The generator `make_worlds.py` of the series writes the four
worlds and `expectations.json`. HOST: seconds per world (a bar of 21).
The earliest day: 2026-09-26, after the phase reading lands in the engine
and the ray law's series exists.

## 2. Row 1d, the no-signalling marginals of the pair

1. The objects: the four worlds of section 1, unchanged.
2. The declared integers: the same.
3. The verbs: the same; the reading is a different count on the same
   clicks.
4. The pin (COMPUTATION, ALGEBRA.md 4.9, Theorem 5): each party's +
   fraction at its setting is 1 / 2 exactly (N / 2 of N births: 1024 of
   2048 at every setting), and its difference between the other party's
   two settings is 0 exactly, by the tables' symmetry (**U**_s^T **U**_s =
   n_s **I**); the falsifier a marginal's difference above the counts'
   error; the nature row 0 within the statistical error (Hensen 2015;
   Weihs 1998; the marginals to verify against the sources).
5. The readings: DETECTOR each party's + count at its setting over the
   births; COMPUTATION the fractions and their differences; GAMEBOARD as
   in section 1.
6. The identity: as section 1.

The descent, HOST and the day: as section 1 (the same four runs read
twice; no world of its own).

## 3. Row 2b, the Mach-Zehnder visibility of one quantum at a time

1. The objects. The torus: a layer 33 x 33 x 1, z periodic (the folded
   axis), x and y open with sponge faces that do not read. Z_N. The family
   `light`, h = 1, its clock the pair [77, 25] on N = 64 (lambda = 12
   Links) or [51, 25] (16 Links), declared per world. One lamp at (2, 2,
   0) releasing one record per birth on the +x arm alone (the first
   splitter makes the two paths: no `turns` on the lamp, refused under the
   key). Two SPLITTERS as foreign objects of the TABLE form at (12, 2, 0)
   and (12, 12, 0)... the arrangement of `amplitude/mz_equal.json` scaled
   to the lattice's wavelength: the first splitter at the lamp's line,
   two free corridors of equal length L = 10 lambda between MIRROR
   receivers (the mirror form: the row held at 0, the whole packet
   returned with its sign reversed) at the corners, the second splitter
   where the corridors meet, the two ports D1 and D2 beyond it, each a
   detector set (a sponge that reads) of one line of Nodes across the
   corridor. The splitter's table: the split's integer matrix of
   ALGEBRA.md 4.6 (Theorem 2, an isometry up to the scaling: the weights
   [21, 20] and [20, 21] by the arrival's side, 21^2 + 20^2 = 29^2, and
   the turns [16, 0], [0, 16], a quarter turn on one output), acting on the
   record's phase read as declared above: a partial re-emission with a
   phase, the fourth receiver form.
2. The declared integers (kind 2): N = 64, the wheel [1, 64], W = 64, K,
   Q, S and the release as the first build's chain world declares them
   (`tests/test_detector_law.py`), h = 1, the train 128 periods, the arm
   length L = 10 lambda, the splitter's weights and turns above, 2000
   intervals; the phase reading above.
3. The verbs: the flight (T, D) with the ray splitting at every free Node;
   the mirrors' return (the mirror form, no verb: the row held at 0); the
   split (P, B, D, T) at each splitter on the pair (a_before, a_now) read
   as declared; the merge with the cancel at the ports (G); the click of
   the record by the ladder (E, D), one click per record.
4. The pins (COMPUTATION, before the run): with equal arms the offers at
   D1 and D2 are the bilinear form on the splitter's rows (ALGEBRA.md 4.8)
   at the lattice's wavelength, 1681 / 1682 and 1 / 1682 in the amplitude
   series' exact form; under the rule the dark port's clicks at most 1 of
   64 at a train of 128 periods (the lattice's band 0.02, DESIGN.md 6.2's
   coherence argument), the visibility 1.00 - 0.02; the number the pins
   script computes on this layer before the run (the two corridors' sums
   at the second splitter, the same form as `detector_law_pins.py` 6.2)
   is the pin, written to `expectations.json`; the falsifier a dark-port
   click beyond 1 of 64; the nature row 0.98 (Grangier, Roger and Aspect
   1986; air; the source's polarisation to verify).
5. The readings: DETECTOR the clicks per port over 64 births; COMPUTATION
   the visibility from the two counts; GAMEBOARD the splits' weights, the
   cancels and the books.
6. The identity: `detector-law-v1` with the table form.

The descent: `shape` [33, 33, 1], `boundary`, `N`, `families`, the lamp
with `train` 128, the two mirrors' form `mirror`, the two splitters'
`table` with `inputs`, `weights`, `turns` (the amplitude series' keys under
the first build's table form), `detectors` D1 and D2, `clock_stamp`,
`detector_law`, `ticks` 2000. HOST: seconds (a layer of 1089 Nodes).
The earliest day: 2026-09-26, after the splitter's table under the rule
(the phase reading) lands in the engine.

## 4. Row 4b, the redshift of a moving lamp against its speed

1. The objects. The torus: a chain of 2200 x 1 x 1, y and z periodic of
   one layer, x open for light (sponge faces) and the massive kind's faces
   open on x (zero faces). Z_N. Two families: `light`, h = 1, the pair [1,
   1]; the massive kind with the medium's pair [156, 157] (omega_0 =
   0.1129, lambda_0 = 32.1 Links). Two BLOCKS of the massive kind
   (MASSIVE_RECORD.md sections 4 to 7; BUILD.md section 3): the EMITTER A,
   side 12, the well [314, 315], seed 2^20, `emits` light (the source term
   of section 7, a birth at the start of each cycle of its own clock),
   coupling G = [1, 1], g = [1, 5], W = 64, starting at x = 700 and pushed
   to k = 3 on -x (receding from B) by the declared momentum over a ramp
   of 1500 intervals; the RECEIVER B, side 12, the same well, seed 0, the
   same coupling, W = 64, at rest at x = 1900, its cells the detector set
   (the block's click at W, section 6). A CONTROL world with A at rest at
   x = 1300.
2. The declared integers (kind 2): the pairs above; s = 12; G, g, W; A's
   momentum [Q S M, 0, 0] with the sign toward -x (k = 3: beta_c = 1 /
   sqrt 3; gamma_m the massive kind's own at the exact cone c_eff^2 = cos
   omega_0 (omega_0 / sin omega_0) c^2 of THIS medium's omega_0 = 0.1129,
   1.22606, MASSIVE_RECORD.md section 8; gamma(c_m) = 1.22675 at its
   second-order cone and light's gamma(c) = sqrt(3 / 2) CONTROLS beside;
   item 4 carries the same three); `ramp` 1500; the hold 8000 (a pin
   world); 9500 intervals; the seeds; the block's content M = 1.
3. The verbs: the massive rule (G, D by 3 den g_d with the coupling folded
   in the one division, T; section 7 (A)); the coupling's same-Node first
   differences in the engine's columns (section 7 (B)); A's step by T
   (the cells and the pair region move, the record re-forms; section 5);
   A's emission (the source term); B's driven record's rung at W, the
   click (E, D) stamped with B's count (section 6).
4. The pin (COMPUTATION, MASSIVE_RECORD.md sections 8 and 9 row 4b): the
   frequency B reads from A receding at beta_c, over the frequency B reads
   from A at rest (the control world), is 1 / (1 + z) with THE PIN 1 + z =
   (1 + beta_c) / (f / f_0)(world) = 1.9889 at k = 3, f / f_0 = 0.7931 the
   one formula omega_b(gamma_m s) / (gamma_m omega_b(s)) on THIS world's
   well (side 12, [314, 315] in [156, 157], half depth, eps 0.188, the mode
   0.10175) with gamma_m = 1.22606 at this medium's exact cone (omega_0 =
   0.1129), by `coupled_mode_pins.py` (c) (the Boss's ruling of 21:22Z:
   the pin per world by the one formula, as row 4a's); the free emitter's
   limit gamma_m (1 + beta_c) = 1.9339 beside as the (K) form, with the
   CONTROLS 1.9350 at this medium's second-order cone and 1.9319 at
   light's; the first draft's 1.9355 (with mu = 0.15's gamma_m, 1.22705,
   on this mu = 0.113 medium) is RETIRED, a correction before any run of
   4b, no reading against it (Reviewer 3's MUST 3 through the Boss,
   22:14Z); the character's frequency gamma_m omega_0 shifted by the
   medium's Doppler; the band the peak's grain over the hold, 0.3 percent;
   the falsifier a ratio off 1 / 1.9889 beyond the band; the nature row 1 + z = gamma (1 + beta) (Ives and Stilwell
   1938; Botermann 2014 at beta = 0.338, in vacuum), matched in form at
   the world's beta_c.
5. The readings: DETECTOR B's clicks (the count between clicks on B's own
   record over the hold, the frequency as a count ratio between the two
   worlds); GAMEBOARD B's driven record's spectral peak, A's count per
   interval, the energy account and the form J; COMPUTATION the pin; no
   CONVERSION (a ratio of counts).
6. The identity: `detector-law-v1` with `massive-record-v1`.

The descent: `massive_record` true, the families with `pair` and `faces`,
the two blocks with `side`, `pair`, `coupling`, `seed`, `emits` (A),
`momentum` and `ramp` (A), `wheel`, `probes` where the reader needs a
light amplitude (GAMEBOARD); the control world without the momentum.
HOST: a chain of 2200, seconds to a minute. The earliest day: 2026-09-25,
after (iv-a) reads (BUILD.md section 5 gains this world as (iv-c) on the
Boss's word).

## 5. Row 9, Malus's law at 45 degrees

1. The objects. The torus: a chain of 7 x 1 x 1 (DESIGN.md 6.3: the
   record's train arrives along the 7-Node line), y and z periodic of one
   layer, x open. Z_256. The family `light`, h = 1, the lamp on the wheel
   [159, 256] releasing one row per self-creation on +x, born on label 0
   (`malus_22_5.json`'s form, new_rows PINS.md section 3). The which-path
   `read` at x = 4 with no rotation (the whole beam on label 0, one cell).
   The POLARISER as a foreign object of the TABLE form at x = 6 with the
   setting s = 64 (the angle 180 s / 256 = 45 degrees), its detector set
   the cells + and -.
2. The declared integers (kind 2): N = 256, the wheel [159, 256] (every
   residue u once over 256 births), W = 256, K, Q, S and the release as
   registered for row 9, h = 1, s = 64, 300 intervals; the phase reading
   above.
3. The verbs: the flight (T, D) with the ray splitting at every free Node
   (on a chain the split is the line itself); the table's rotation
   **U**_s (B) on the phase read as declared; the click (E, D): the
   channels + and - weigh (256 C'[s])^2 and (256 S'[s])^2 on the
   half-angle tables of 2N, the rungs b = (2 W C + T) // (2 T) on the
   cumulative weight, one click per record (ALGEBRA.md 4.12).
4. The pin (COMPUTATION on the table, before the run): at s = 64, C'[64] =
   S'[64] = 181 (the half-angle tables at 45 degrees), the rungs 0, 128,
   256: the counts 128 of 256 in + and 128 in -, 0 crossed, 64 with a third
   between (PINS.md row 9); the falsifier any count other than the
   table's; the nature row 1 / 2 (Malus 1809; air; linearly polarised
   light).
5. The readings: DETECTOR the cells + and - over the records 1 to 256 (the
   `click` lines of the set); GAMEBOARD the lamp's births and the rows'
   flight; COMPUTATION the pass fraction.
6. The identity: `detector-law-v1` with the table form.

The descent: `malus_45.json` in the registered form of `malus_22_5.json`
with `detector_law` true, `clock_stamp` true and the table's
`phase_window` 64; HOST: seconds. The earliest day: 2026-09-26, with
section 1's phase reading.

## 6. Malus at three new settings (the scout's R3: 11.25, 28.125 and 33.75 degrees)

1. The objects: as section 5, the setting the one declaration changed: s
   = 16, 40, 48 (the worlds `new_rows/worlds/malus_s16.json`, `malus_s40`,
   `malus_s48`, re-declared with `detector_law` true).
2. The declared integers: as section 5 with s in {16, 40, 48}.
3. The verbs: as section 5.
4. The pins (COMPUTATION on the tables, new_rows PINS.md section 3,
   before the run): (C'[s], S'[s]) = (251, 50), (226, 121), (213, 142);
   the rungs 0, 246, 256; 0, 199, 256; 0, 177, 256; the counts (+, -) =
   (246, 10), (199, 57), (177, 79) of 256; the pass fractions 0.96094,
   0.77734, 0.69141 against cos^2 0.96194, 0.77779, 0.69134 (the tables'
   rounding predicted before the run at the grain 1 / 256: -0.00100,
   -0.00044, +0.00006); the falsifier any count other than the table's;
   the nature row cos^2 (Malus).
5. The readings: as section 5.
6. The identity: as section 5.

The descent, HOST and the day: as section 5; three worlds, seconds each.

## The reader of record of every clock row, declared once (2026-09-23, 20:05Z)

The clicks at W on the block's own record (the cells' sum as built, the
window the hold after the ramp) are the reader of record of every row
that reads a clock; the spectral peak of the summed record is a GAMEBOARD
diagnostic beside, never the pin. A pin world's seed is the bound mode's
shape as the margin module computes it, as integers at the world's
amplitude over the whole board, the same at both levels (a declaration
of kind 2), written into the world file by the generator so that the run
follows from the world file and the engine alone, byte for byte (the
profile printed at load the GAMEBOARD check); a row whose clicks beat is a diagnostic until they
read the mode (MASSIVE_RECORD.md section 11 item 7). Section 4 above (row
4b) reads B's clicks so.

## What the engine lacks for these six, in one list (for the builder, on the Boss's word)

- The phase reading of a record at a table Node from (a_before, a_now)
  by the phase table at load (the paragraph at the head), one component,
  one test (a declared phi read back at every u).
- The pair record's two arms under the ray law (the lamp's `arms` and
  `branches` keys of the amplitude series admitted under `detector_law`;
  the rule's part only that both trains reach their bars, DESIGN.md 6.3).
- The splitter's table under the rule (the split's integer matrix acting
  on the read phase, the two outputs re-emitted by the table form).
- The receiver block's world (iv-c) of section 4 in BUILD.md section 5
  (no new component: the block, the coupling, the emission and the click
  at W are STEP 3's, pushed at 2f44797c).
