# The confrontation register: detector readings against nature

The physicist's register of 2026-09-21, on the model owner's fourth gap
(record 241 of [the day's log](LOG_2026-09-20.md), translated: "detector
readings must also be compared with real experiments, with the same
parameters and without re-fitting per experiment"). One row per registered
detector reading that has a dimensionless counterpart in nature; nothing
run for this register, nothing recomputed: every model number is a
registered value with its world file and its register key, every published
number has one source. The base is `origin/main` at `88d843ef`
(2026-09-21). The register is the first pass; the second pass, the
dimensional constants through the dictionary's conversion, is the closing
table.

Notation ([the workflow's rule](../skills/workflow.md#notation-every-symbol-named-its-kind-shown-the-model-owner-2026-09-21-record-184)):
a scalar plain, a vector in bold lowercase (**p** the momentum vector), a
matrix or an operator in bold uppercase (**G** the click's Gram matrix), a
Greek letter written as a word and named at its first use (gamma, the
Lorentz factor). A quantum of light is a row (a message in flight) and a
particle with content is a body (a measured event); the words photon,
electron, muon, neutron and star name nature's objects in the detector's
world, not things on the GameBoard.

## The rules of the register

- **(a) One parameter set for every row.** The grain as the registered
  worlds declare it and the registered family table; no width, clock or
  charge is moved to meet an experiment. The one set is stated in the
  next section; a row whose registered world declares another value says
  so in its "grain" column and is marked "not under the one set", with
  the differing key named. A flag on K records a declared clock (the
  lamp's phase rate with its content, E = h f with E the energy, h the cost
  of one phase step and f the frequency), set per world before any
  comparison and never after one; the flag is kept because the rule asks
  for it, and no verdict below depends on K.
- **(b) Dimensionless comparisons only** in this pass: a ratio, a
  correlation, a visibility, a fraction, a deceleration parameter, a
  bound. A comparison that needs a unit (metres, seconds, kilograms,
  joules, coulombs) needs the dictionary's conversion fixed once
  ([HIGHLIGHTS 5.7](HIGHLIGHTS.md#57-from-the-world-we-see-to-the-vector-world-the-conversions-the-principles-what-is-derived-and-what-is-input-2026-09-21))
  and is listed at the end under "What needs the conversion".
- **(c) One source per published value**: author, year, journal or arXiv
  identifier. Where the exact figure could not be checked against the
  source from this checkout, the value is given as known and marked "to
  verify against the source"; no precision is invented.
- **(d) Every model reading with its world file, its register key and its
  registered value**, nothing recomputed. A dimensionless ratio formed
  from two registered integers shows its arithmetic in the row's note.
  The reading is a detector reading (a click, a gather, a record's
  weight, a body's own `read` or `contact` record), never a GameBoard
  reading (record 163 (5); [the experiments register](EXPERIMENTS.md),
  "Two kinds of readings"), except where a row says the number is a
  derivation's pin whose run is not yet registered.
- **(e) One verdict per row**: PASS (within the stated uncertainty), FAIL
  (outside, with the number of the discrepancy), BOUND (the comparison
  bounds a free parameter, with the bound) or NOT YET (the reading is
  not registered, with the reading that would be needed). A FAIL is a
  result of the theory and not a defect of the register, and is stated
  with the same care as a pass; nothing is tuned after a verdict
  ([the physics comparison method](../skills/workflow.md#physics-comparison-method)).
  Where a derivation has pinned the reading and its run is not yet made,
  the verdict is given from the pin and says so ("pinned; the run not
  made"), under the owner's rule that a formula gives and a run proves
  (record 205): such a row is also a NOT YET for the run.

## The one set

The values every row is read under, as `origin/main` at `88d843ef`
declares them (the world-file keys in
[HIGHLIGHTS 5.6](HIGHLIGHTS.md#world-file-keys-eventsworldpy-parse_ray_world)):

| Width | Value in the one set | Where it is declared | Rows that declare another value |
| --- | --- | --- | --- |
| N, the phase circle | 64 | the world key `N` | the Bell resolution check at N = 1024 and 4096 (row 1a's note) |
| Q, the pace's grain and the label's scale | 64 | `events/world.py`, `Q = 64` (`LABEL_SCALE`), one constant for every world | none |
| P, the fan's width | a declaration per fan (record 175): the Farey fan of width 48 for the two slits, the 290 primitive directions with \|a\| + \|b\| + \|c\| <= 6 for the nucleus, the weak and the binding worlds, the 2616-direction shell for Bohr, one heading per arm on the bars | each world's `directions` (the bound `direction_bound`, 64 by default) | none: the fan is the apparatus, stated per row |
| W, the birth wheel | the birth ordinal mod N on `main` (u = t - 1); W = 4096 decided (records 163 and 180), in build on the click branch | the lamp's record | rows 2a and 2b say what the wheel changes |
| K, the clock's pair [1, K] | 2^20 | the world key `K` | the Bell pair lamps 15 x 2^20 (rows 1a, 1b); `slits_huygens`, Bohr and Heisenberg 2^30 (rows 2a, 6, 10); J2 4096 (row 8b); the Hubble stars 4 198 400 (rows 3, 4b) |
| S, the width of the push (what physics calls Newton's constant; an input of kind 2, record 189) | a world input, stated per row: 2^28 (the nucleus, J3, the binding), 45120 (Bohr), 2^20 (the Hubble stars), 1 (the bars, the default) | the world key `width` | not a grain; listed for completeness |
| gamma, the post-Newtonian parameter of the space part (the weak-field metric's g_ii = 1 + 2 gamma U beside g_00 = -(1 - 2 U); an input of kind 2 as S is, declared by the model owner on 2026-09-22, step 4 of the generic bending, [EVERY_FAMILY.md](designs/one_wall/EVERY_FAMILY.md) section 6: no derivation of the space part from the law exists, [DERIVATIONS_BEAM 5.4](DERIVATIONS_BEAM.md#54-light-no-optical-metric-on-main-the-meetings-turn-as-a-key)) | 1, nature's: gamma - 1 = (2.1 +- 2.3) x 10^-5 from the Cassini radio delay (Bertotti, Iess and Tortora 2003, Nature 425, 374) and 0.99992 +- 0.00012 from the VLBI deflection (Lambert and Le Poncin-Lafitte 2011, Astron. Astrophys. 529, A70) (to verify against the sources); 0 in the controls of the form (the time part alone) | the world key `optical` (its value gamma; the flight's coefficient 1 + gamma in the age wall's set) until step 5 puts the flight in the set always | the optical worlds at 0 (the wall's factor read as the ratio of the two, row 13); every other world without the key, unbent |
| The family table | each world's `entity_definitions` (the catalog's families): the proton of content 1836 with the charge 4 per unit, the neutron 1839, the strong column 10000 with the lifetime 3, the beta -7344 per unit of amount, a paid `light` of quantum 1 | [the entity catalog](ENTITY_CATALOG.md) | none: the same families wherever they appear |

The declared roundings at load (the tables at 1/256, T_D by `isqrt`, u_d)
are part of the one set (record 189, kind 1).

## The rows

The table gives the verdicts; the notes below give each row's arithmetic,
caveat and what would change it. "Pinned" in the verdict column means a
derivation's expectation whose run is not yet registered (rule (e)).

| Row | The dimensionless observable | Nature's value and its one source | The model's registered reading (world; register key; value) | Grain | Verdict, with the number |
| --- | --- | --- | --- | --- | --- |
| 1a | The CHSH sum S of a pair read at two detectors, the record's pair | S = 2.42 +- 0.20, Hensen et al. 2015, Nature 526, 682; the quantum bound 2 sqrt 2 = 2.828, Cirel'son 1980, Lett. Math. Phys. 4, 93 | `examples/events/amplitude/bell_*.json`; `amplitude/expectations.json` `pair.chsh_S` = 176 in the unit 64: S = 2.75; `pair.chsh.*.E` = 44, -44, 44, 44 | N = 64; K = 15 x 2^20: not under the one set (K) | PASS: 0.33 above the measured, 1.65 of its standard error; 0.078 below the quantum bound |
| 1b | The CHSH sum S under the phase-form window (the crowd form's Bell test) | the same | `examples/events/bell/a*_b*.json`; `bell/expectations.json` `chsh_sum` = 2, `primed_sum` = 2 | N = 64; K = 15 x 2^20: not under the one set (K) | a control (the local read-out's bound; superseded as the law's row by 1a), marked 2026-09-23 on the model owner's word (his plan for the rows, tier (c), about 00:56Z, through the Boss): Bell's bound S = 2 is a theorem of every local read-out (WHAT_IS_MISSING.md row 1b; CRITERIA.md row 1b (b)), the law's answer to nature the record's one gather of row 1a (2.75, DETECTOR, PASS); the verdict kept beside it: FAIL: S = 2 exactly, 0.42 below the measured, 2.1 standard errors; the local bound, the model's registered limit for the window form |
| 1d (beside 1c, the order form, not yet a row here; from PINS.md section 5, record 1190) | The no-signalling marginals of the pair, the count form: each party's + fraction at its setting, and its difference between the other party's two settings | 0 within the statistical error, in every Bell test that reports its marginals; the loophole-free Hensen et al. 2015, Nature 526, 682 (the marginals in the supplement; to verify against the source); Weihs et al. 1998, Phys. Rev. Lett. 81, 5039 (to verify against the source) | `examples/events/amplitude/bell_0_8.json`, `bell_0_24.json`, `bell_16_8.json`, `bell_16_24.json`; `amplitude/expectations.json` `pair.marginal` = 32 and `pair.chsh.*.counts` 27, 5, 5, 27 (5, 27, 27, 5 at (0, 24)): each party's + count 32 of 64 at every setting pair (DETECTOR, replayed at head by the tests); the difference between the other party's settings 0 exactly (COMPUTATION from the cells); Theorem 5 (ALGEBRA.md 4.9) | N = 64; K = 15 x 2^20: not under the one set (K), as row 1a | agrees: 0 against 0, exact, by Theorem 5 (ALGEBRA.md 4.9): a theorem of the click's form, a consistency check the law must pass and not an independent prediction, outside the referee's count of predictions; the tolerance nature's statistical error on 0; the same at the seven grains 512 to 16384 (`pair_n`) |
| 2a | The two-slit fringe visibility of one quantum at a time, (I_max - I_min) / (I_max + I_min) | no published single-quantum two-slit visibility at hand (the single-electron build-ups of Tonomura et al. 1989 and Bach et al. 2013 show the fringes without a visibility figure); the lower bound taken from row 2b's two-path 98 percent (Grangier, Roger and Aspect 1986, a Mach-Zehnder interferometer); the ideal for equal paths 1 | `examples/events/amplitude/slits_huygens.json` (the lamp's golden-rate `wheel` [2531, 4096], 4300 intervals, 4096 births under the exact phase at the click); the register entry L2b of [EXPERIMENTS](EXPERIMENTS.md#l-the-amplitude-law-2026-09-20), re-registered under the birth wheel, and the run's record beside the world ([the amplitude README, L2](../examples/events/amplitude/README.md#l2-the-two-slits-at-a-low-rate)): the clicks' visibility 0.966 (DETECTOR; the record's screen weights 0.954, record 164), the dark cells 0 to 3 as pinned (DETECTOR, the mean 0.68), the counts' Pearson with the two-source cosine 0.891 (DETECTOR; the weights' 0.895) against the pinned 0.96: a miss, the pin derived for the screen's fan and not this world's own Farey fan | N = 64; P = 48; K = 2^30: not under the one set (K); the wheel W = 4096 | FAIL: 0.966 against 0.98, 0.014 below the measured and 0.034 below the ideal; the cause named (the fan's grain); the fringes in the clicks as in the weights; the correlation pin 0.96 missed at 0.891, the pin the screen's fan's |
| 2b | The Mach-Zehnder visibility of one quantum at a time (the dark port's fraction) | 98 percent, one photon at a time in a Mach-Zehnder interferometer, Grangier, Roger and Aspect 1986, Europhys. Lett. 1, 173 (to verify against the source) | `examples/events/amplitude/mz_equal.json`; `mach_zehnder.mz_equal.offers` D1 = 1681/1682, D2 = 1/1682; `clicks` D1 = 64, D2 = 0 | N = 64; K = 2^20 | PASS: the clicks 64 / 0 over 64 births, the dark port 0, the visibility in the clicks 1.000 (DETECTOR) above the measured 0.98; beside it the offers' visibility (1681 - 1) / 1682 = 0.9988, a number of the apparatus layer (the record's ledger), a diagnostic and not a measurement (records 562 and 564) |
| 2c | The power of the click's form (Born's exponent 2; nature's counterpart the absence of third-order interference) | the Sorkin parameter kappa = 0.0064 +- 0.0119 (consistent with 0, the quadratic form), Sinha et al. 2010, Science 329, 418 (to verify against the source) | `mz_345.json` `mach_zehnder.mz_345.clicks` 63 / 1 and `bell_16_24.json`, `bell_16_24_far.json` `pair.chsh.16_24.counts` 27, 5, 5, 27 (`pair.far.bell_16_24` = 44); [DERIVATIONS_BEAM 6.5](DERIVATIONS_BEAM.md#65-the-uniqueness-of-the-clicks-square-a-lattice-gleason): the power k pinned to [1.917, 2.489) and [1.784, 2.054); the same (3, 4) split at N = 32 and 128, `mz_345_n32.json` 31 / 1 and `mz_345_n128.json` 125 / 3 (`expectations.json` under `mz_345_n`, [the README's section](../examples/events/amplitude/README.md#the-3-4-split-at-n--32-and-128-the-power-window-of-65-pinned-from-above), run 2026-09-21, every pin met): k in [1.548, 2.129) at 32 and [1.835, 2.012) at 128 | N = 64; K = 2^20 (mz_345), 15 x 2^20 (the pair); the per-row exception N = 32 and N = 128 (the split's two other worlds, everything else the same) | NOT COMPARED to this experiment (kappa not computed): the window [1.917, 2.012) from the click cells (the intersection of the four windows, 2 inside, 1 and 3 outside) is a read-back of an engine with the square built in, an implementation gate on the click's form and not evidence about nature; a three-opening world that reads kappa itself is not registered (the model owner, 2026-09-22) |
| 3 | The deceleration parameter q of the Hubble diagram | q_0 = Omega_m / 2 - Omega_Lambda = -0.53 +- 0.01 from Omega_m = 0.315 +- 0.007 (flat), Planck 2018, Aghanim et al. 2020, A&A 641, A6; the discovery of q_0 < 0: Riess et al. 1998, AJ 116, 1009, and Perlmutter et al. 1999, ApJ 517, 565 | `examples/events/hubble_stars/record/coasting_none.json` (the third run's `doppler/coasting_none.json` was deleted with the key on 2026-09-21, [MIGRATION](MIGRATION.md#the-crossing-rule-on-2026-09-21-the-step-before-the-law-a-row-and-a-body-met-once-the-key-doppler-and-the-grain-deleted); its readings stay as history in EXPERIMENTS); the register entry G2 (the second and third runs): q = -0.108 inside the coasting bracket -0.25 .. +0.25, H (t_0 + T_0) = 1.026; the gravity crowd +0.922 (record) and +0.345 (doppler), the double +1.500 and +1.190; [section 15](DERIVATIONS_BEAM.md#154-the-milne-case-and-the-registers-24-stars-at-rest)'s growing wall q = 0 (Milne). Read in the detector's own clock at head (the count of its self-creations under the age wall, r = 1.0000 with no crowd at the detector, DETECTOR; CRITERIA (f), the re-run of 2026-09-22), equal to the host's tick to the integer; the registered run's time base was the host's tick (record 768), superseded; a two-way light clock at the detector, not read, reads the same count in no crowd (series X) (the reviewer's read of the kind audit, record 1196). | N = 64; K = 4 198 400 and S = 2^20: not under the one set (K); the third run's worlds carried the key `doppler-v1` (deleted on 2026-09-21), the coasting reading identical with and without it | FAIL: the coasting -0.108 is 0.42 above nature's -0.53 (1.7 times the register's bracket); every gravitating reading is 0.87 to 2.0 above; the law has no term with q < 0 |
| 4a | The muon's lifetime in flight over its lifetime at rest | gamma = 29.33 at the CERN storage ring, the dilation confirmed as gamma to a fractional error of about 2 x 10^-3 at 95 percent confidence (the brief's 0.1 percent; to verify against the source), Bailey et al. 1977, Nature 268, 301 | series J4 ([HYPOTHESES 21](HYPOTHESES.md#21-a-moving-bodys-clock-the-engines-rate-is-one-at-every-speed-natures-gamma-a-limit-stated-so-that-it-can-fail), [light_speed/FORM.md section 4](designs/light_speed/FORM.md#4-lorentz-v1-stated-so-that-it-can-fail)): the `become` at tick 64 at every speed, the ratio 1; no world file, not run; lorentz-v1 would read 71 and 126 at 0.43 and 0.86 of c | the pinned world: N = 64, K = 2^20, S = 1 | FAIL (pinned; the run not made): the ratio 1 against 29.33, a factor 29.33; the open decision of record 230, routes A, B, C. Re-read under `covariant-readings-v1` (2026-09-21, record 270; series S, [the register](EXPERIMENTS.md#s-the-covariant-readings-2026-09-21)): the electron products' clicks on the +x face at 369 and 345 (DETECTOR; the design's 367 and 345 within two ticks, the decay tick derived back by the flight table: 70 and 124), the muon's 64th self-creation at the ticks 70 and 124 (the `become` lines, a body's own record, DETECTOR: ENGINE.md's readings by type, Highlights kind 9; labelled GAMEBOARD until 2026-09-23, [DISAGREES.md](designs/fail_rows/DISAGREES.md) (PR #1002, merged at 0d0865f7) section 2.2; the design's integers 70 and 124, the continuum's 70.9 and 125.2; gamma 1.1074 and 1.9558 at 0.43 c and 0.86 c): PASS under the key within its domain, gamma's form reached at gamma <= 2; the identity's declared domain \|**p**\|_1 <= Q S M ends at gamma 2 on a heading (beta 0.866), so this row's 29.33 is outside what the identity can run until form B lifts the cap (qualified 2026-09-23 by RUN_4AB.md section 2.3: the cap gamma <= 2 is the drive's own saturation under either drive, lifted neither by form B nor by a small body; a second declaration of the domain would be the design's writer's and the owner's, not a run's); the law's row stands as the FAIL beside it |
| 4b | The redshift z of a moving lamp against its speed (the Doppler with the clock's factor) | 1 + z = gamma (1 + beta) along the motion, the time-dilation factor confirmed to 2.3 x 10^-9 at beta = 0.338, Botermann et al. 2014, Phys. Rev. Lett. 113, 120405 (to verify against the source); the classic Ives and Stilwell 1938, J. Opt. Soc. Am. 28, 215 | `hubble_stars/coasting_none.json`, the star `s_mz2` at beta = 0.2674 ([the README's table](../examples/events/hubble_stars/README.md#the-readings-2026-09-20-measured-against-expected)): z = 0.2636; [DERIVATIONS_BEAM 4.3](DERIVATIONS_BEAM.md#43-a-moving-clock-the-rate-is-one-at-every-speed): nature's 0.315 at that beta, the classical 0.2674. Read in the detector's own clock at head (the count of its self-creations under the age wall, r = 1.0000 with no crowd at the detector, DETECTOR; CRITERIA (f), the re-run of 2026-09-22), equal to the host's tick to the integer; the registered run's time base was the host's tick (record 768), superseded; a two-way light clock at the detector, not read, reads the same count in no crowd (series X) (the reviewer's read of the kind audit, record 1196). | N = 64; K = 4 198 400: not under the one set (K) | FAIL: 0.2636 against 0.315, 0.051 below in z (17 grains of 0.003); the clock's factor gamma = 1.0378 absent. Re-read under `covariant-readings-v1` (2026-09-21, record 270; series S, [the register](EXPERIMENTS.md#s-the-covariant-readings-2026-09-21)): z = 0.3674 read at the centre's detector on the record form of the world at the declared momentum (DETECTOR, the pointer's z; the design's 0.369 +- 0.003 at beta 0.3040 under the identity's pace p / E, gamma 1.0497; nature's 0.315 only on a re-declared momentum, 17.6 M2), the star's 18 steps in the late window's 100 intervals GAMEBOARD: PASS under the key within its domain, this star at gamma 1.05 inside the identity's declared domain \|**p**\|_1 <= Q S M (gamma <= 2 on a heading); the law's row stands as the FAIL beside it |
| 4c (beside 4b; from PINS.md section 5, record 1190) | The round-trip Doppler off a receding transponder, the cart's counts apart between two returns over its ordinals apart between the births they carry, (1 + beta) / (1 - beta), r-free | (1 + beta) / (1 - beta) to all orders, the two-way form of every radar and two-way tracking, the same in Einstein's and in the ether form; a FORM row until a nature source is named (the register's rule (c)), as row 11b entered by a pin | `docs/designs/fail_rows/worlds/cart_k3_law.json`, `cart_k5_law.json`; RUN_4AB.md 6.3 (`run_4ab_readings.json`, `runs.<world>.readings.round_trip`): 3.70833 over 445 counts (120 returns) for the pin 151 / 41 = 3.68293 at k = 3 (beta 55/96), 2.05372 over 497 (241 returns) for 43 / 21 = 2.04762 at k = 5 (beta 11/32) (DETECTOR); under the key 4.774 for 4.708 and 2.308 for 2.302 at the identity's beta (DETECTOR, the hypothesis's, beside) | N = 64; K = 4 202 496, S = 2^20 (series O's numbers): not under the one set (K) | FORM row, outside the count until a nature source with a number is named (the register's rule (c)): the law's worlds read 3.708 and 2.054 for 151 / 41 and 43 / 21, +3.05 and +1.48 counts off the closed form over the window, outside the version-1 band 2 / W as pinned in RUN_4AB (FAIL there) and inside the preregistration's band in ordinals and the meeting remainder of 8.44 and 10.44 counts per end (RUN_4AB 6.3); reads nothing of r, so it changes nothing in rows 4a, 4b and 5b |
| 5a | The anisotropy of c by direction, delta c / c, from the grain | delta c / c below about 10^-17, Herrmann et al. 2009, Phys. Rev. D 80, 105011, and 9.2 +- 10.7 x 10^-19, Nagel et al. 2015, Nature Communications 6, 8174 (both to verify against the source) | the flight table at Q = 64: the Euclidean pace Q \|D\| / T_D from 0.5774 to 0.5818 over the 1 780 418 primitive directions within 64 ([light_speed/FORM.md section 1](designs/light_speed/FORM.md#1-the-statement-of-c-completed)); the run-time check record 144's cone (17 and 24 Links at age 29, `amplitude/expectations.json` `cone`) | Q = 64 | BOUND on Q: the registered 7.6 x 10^-3 falls as 1 / (sqrt 3 Q); below 10^-17 needs Q >= 5.8 x 10^16 (2^56), below 10^-18 needs Q >= 5.8 x 10^17 (2^59); beyond the 64-bit word at the register's fan radius 48 (13.3's bound Q \|D\| <= 2^61 / sqrt 3) |
| 5b | The anisotropy of c between a laboratory's two arms when the laboratory moves through the lattice's frame | the same bounds, the same sources; the Earth's orbital speed 30 km/s, beta = 10^-4 (Michelson and Morley 1887, Am. J. Sci. 34, 333, the first null) | [DERIVATIONS_BEAM 12.3](DERIVATIONS_BEAM.md#123-the-bond-clock-under-1-to-3): the round trip gamma^2 along the motion and gamma across, no contraction (12.1), the ether light clock; on the register's flight table 1.375 along and 1.140 across at beta = 0.4297 (the host script, no run) | the register's flight table at Q = 64 | FAIL (pinned; the pair in motion of 12.4 not run): the arms differ by gamma - 1 = beta^2 / 2 = 5 x 10^-9 at beta = 10^-4, eight to nine orders above the bound; only a contraction (route B or C of record 230) would remove it |
| 6 | Bohr's line ratio nu(H beta) / nu(H alpha) of the Balmer series | 1.3500: 656.279 nm / 486.135 nm (NIST Atomic Spectra Database, Kramida et al.; to verify at the fifth digit); Balmer's formula (1 / 4 - 1 / 16) / (1 / 4 - 1 / 9) = 27 / 20 = 1.35 exactly | series H, `examples/events/bohr/r*.json`: no line registered (the register entry H: "Bohr's lines were not read behind the detector, neither for nor against"); [DERIVATIONS_BEAM 7.2](DERIVATIONS_BEAM.md#72-bohrs-levels): the condition and the radii reached in form, the levels and the lines not reached | N = 64; K = 2^30 and S = 45120: not under the one set (K) | NOT YET: needed, the phase rate of the faces' `wave` record of two orbits closing with whole j (two closing radii), read as a ratio, and a transition between them, which the law lacks |
| 7a | The deuteron's binding energy as a fraction of its nucleons' mass | E_B / (m_p + m_n) = 2.2246 MeV / 1877.84 MeV = 0.1185 percent, AME2020, Wang et al. 2021, Chinese Physics C 45, 030003 | `examples/events/binding/deuteron_bond.json`; the register entry N (B1) and [the worlds' README](../examples/events/binding/README.md): the `bond` clicks on the border `lifetime`, escaped content 4 of the declared 3677 = 0.109 percent; the mass a detector reads 3673 | N = 64, K = 2^20, S = 2^28 | BOUND on the held `bond` per nucleon (a declared input, record 106: the law derives no binding energy): 2 units per nucleon gives 0.109 percent, 8 percent below nature; nature's 0.1185 percent is 4.35 units of 3677, between the whole gives 4 (0.109) and 5 (0.136) |
| 7b | The alpha's binding energy over the deuteron's | 28.296 MeV / 2.2246 MeV = 12.72, the same source | `examples/events/binding/alpha_square_bond.json`; the register entry N (B3): four `bond` clicks, escaped content 8, the ratio to the deuteron 2.0 | the same | FAIL: 2.0 against 12.72, a factor 6.4; stated before the run as the law's failure (the give is once per body, so the binding is linear in the nucleons) |
| 8a | The shape of the neutron's decay curve: the 10th-to-90th-percentile width of the decay times over their median | ln 9 / ln 2 = 3.17 for a memoryless (exponential) survival, the form of every lifetime measurement, e.g. the bottle measurement of Gonzalez et al. 2021, Phys. Rev. Lett. 127, 162501 (tau_n, the neutron's lifetime, 877.75 +- 0.28 s; to verify against the source) | `examples/events/weak/j1_lattice.json` and `j1_source.json`; the register entry J1 and [the worlds' README](../examples/events/weak/README.md): the shell's 64 beta clicks, the width over the median 0.036 and 0.038; every click the content 3 (a line) | N = 64, K = 2^20 | disagrees: a step, the width 0 in each neutron's own clock against nature's 3.17 (DETECTOR, the 64 clicks of content 3); the width over the median in the lattice's clock 0.036 (0.08 to 0.13 at head) GAMEBOARD, a diagnostic beside it, in no verdict (the reviewer's read of the kind audit, record 1196); the reading NOT MADE: the laboratory clock's counterpart, the shell detector's own count under `clock_stamp` (the shell's 4170 fixed bodies one beam reading set, their click lines carrying `clock`), its expectation the tick's width within 2^-20 at [1, 2^20], about 0.08 to 0.13; disagrees under either number ([DISAGREES.md](designs/fail_rows/DISAGREES.md) (PR #1002, merged at 0d0865f7) section 5) (the cell before 2026-09-23 kept as history: FAIL: 0.036 against 3.17, a factor 88 (a step where nature has an exponential; PREDICTIONS entry 10)); the line against nature's continuous beta spectrum a second FAIL without a number |
| 8b | The neutrino's passage: the count of an identical detector placed behind the first, over the first's count | about 1: the cross-section of a MeV neutrino, of order 10^-43 cm^2 (Formaggio and Zeller 2012, Rev. Mod. Phys. 84, 1307), attenuates a beam by less than a part in 10^16 per metre of ordinary matter, so two identical detectors in line read the same count | `examples/events/weak/j2_filter.json`; `weak/expectations.json` `j2.j2_filter.first_clicks` = 16 of 1024, the 127 readers behind it 0 (the ladder `j2_ladder`: each residue's reader 16, nothing behind the 64th) | N = 64; K = 4096: not under the one set (K) | FAIL: 0 against about 1 (a filter set by the window's residue, not an attenuation set by the depth; PREDICTIONS entries 7 and 8) |
| 8c | The neutrino's mass: the heaviest neutrino mass state over the electron's mass (one named observable: the heavier state of the atmospheric splitting; the lightest state is not bounded below by the oscillations, and the beta-decay bound is on the effective mass m_beta, the weighted mean of the squares over the electron flavour's mixing, not on one eigenstate) | at least sqrt(2.5 x 10^-3 eV^2) / 0.511 MeV = 0.050 eV / 0.511 MeV = 9.8 x 10^-8: the oscillations give the squared mass differences 7.4 x 10^-5 eV^2 and 2.5 x 10^-3 eV^2, which bound the heavier state of each split and leave the lightest free (the normal ordering allows a lightest state near 0 and a middle one near 0.0086 eV; PDG 2024, Navas et al., Phys. Rev. D 110, 030001, the review Neutrino masses, mixing and oscillations, sections 14.7 and 14.9); at most about 0.8 eV / 0.511 MeV = 1.6 x 10^-6 by inference from the direct bound m_beta below 0.8 eV (KATRIN, Aker et al. 2022, Nature Physics 18, 160): a heaviest state above that scale would make the three states degenerate within the splittings and m_beta above the bound (to verify against the source) | `examples/events/entities/families.json`: the `nu` family with `quantum` 0 and no content, one family for every state, a surrogate with no oscillation sector (no flavour, no mass eigenstates, no mixing), the register's neutrino massless ([DERIVATIONS_BEAM 19.5](DERIVATIONS_BEAM.md#195-the-rest-of-the-masses-as-readings-after-a-detector)) | the family table (a content is an input) | FAIL (refuted): 0 against at least 9.8 x 10^-8 for the heaviest state (a content above 0 is an input the register does not declare); the valid ground is that a sector of massless states cannot carry the observed nonzero splittings, not a floor on the lightest state; the oscillation itself, a family turning into another in flight, is not modelled (the catalog's gap list); corrected on 2026-09-21 (issue #556: the row had named the lightest state and read KATRIN's m_beta as a bound on each state) |
| 9 | Malus's law, the fraction transmitted through a polariser at 45 degrees | 1 / 2 (cos^2 of 45 degrees; a third polariser at 45 degrees between two crossed ones passes 1 / 4 of the polarised intensity), Malus 1809 (to verify the citation) | `examples/events/amplitude/malus_a.json`, `malus_b.json`, `malus_c.json` (one bar of 7, N = 256, the lamp on the wheel [159, 256], every row born on the label 0; the polariser the rotation of the label bit by a declared setting, `rotate` 64 on the GameBoard in `malus_c` or the `sum` set's window s = 64, 128, 64 at the end, and the which-path `read` at a `sum` set: the entries in force, no feature 11, [the note](designs/malus/NOTE.md)); the entry A12 of [EXPERIMENTS](EXPERIMENTS.md#a12-maluss-law-and-the-three-polarizer-chain-after-feature-11), re-run under the click (2026-09-21), and the run's record beside the worlds ([the amplitude README, A12 under the click](../examples/events/amplitude/README.md#a12-under-the-click-maluss-law-from-the-table-entries-in-force)): over the records 1 to 256 the cells (DETECTOR) (a) 0+ 128, 0- 128; (b) 0+ 0, 0- 256; (c) 0+ 64, 0- 64, 1+ 64, 1- 64, every pin met exactly (`expectations.json` under `malus`); the absorbed rows click in their own cells, no body sinks them | N = 256; W = 256; K = 2^50: not under the one set (K) | PASS: 128 of 256 = 1 / 2 exactly at 45 degrees, 0 of 256 crossed, 64 of 256 = 1 / 4 of the births and 1 / 2 of the 128 the first polariser passed with the third between: Malus's cos^2 exact at 45 and 90 degrees (the tables 181 = 181, 0 and 256, no rounding); at 22.5 degrees run on 2026-09-21 (the auditor's round 10 part 2; `malus_22_5.json`, `malus_67_5.json`, `malus_chain_22_5.json`, the register's `malus.run_22_5` and [EXPERIMENTS A12 extended](EXPERIMENTS.md#a12-maluss-law-and-the-three-polarizer-chain-after-feature-11), record 395): the cells over the records 1 to 256 (DETECTOR) 0+ 219, 0- 37 at 22.5 degrees, 219 / 256 = 0.85547 against cos^2 22.5 degrees = 0.85355; 37 / 219 at 67.5; the chain at 22.5-degree steps (the rotate 32, the read, the window 32) 0+ 187, 0- 32, 1+ 5, 1- 32, 187 / 256 = 0.73047 against cos^4 = 0.72855; every pin met exactly, the +0.0019 the tables' rounding at the scale 256 (the owner's declared input, record 328), engine-exact; the limit: one which-path read per arm, the four-polariser chain of A12 at 22.5-degree steps not covered |
| 10 | The single-opening spread, w x Delta(sin theta) / lambda (w the opening's width, theta the angle behind it, lambda the wavelength) | 0.886 (the full width at half maximum of the Fraunhofer single-slit pattern), verified with fullerene molecules by Nairz, Arndt and Zeilinger 2002, Phys. Rev. A 65, 032109 (to verify against the source) | `examples/events/heisenberg/w27_wave.json`; the register entry A10: the product 4.99 at w = 27 with lambda = 4.619 Links, 4.99 / 4.619 = 1.08; the crowd form's number, kept as history; the record form's re-run of `w27_beam` did not complete | N = 64; K = 2^30: not under the one set (K) | NOT YET under the one click: the last registered value 1.08 against 0.886 is 22 percent above (the Fresnel number 1.46 named as the cause); the smaller widths unread |
| 11a | The deceleration parameter q read from the brightness of a far lamp at rest under the growing wall (the second order of the Hubble diagram, d_L = (c / H)(z + (1 - q) z^2 / 2 + ...)) | q_0 = -0.53 +- 0.01, Planck 2018, Aghanim et al. 2020, A&A 641, A6 (row 3's source); the Hubble diagram's shape from the supernovae, Riess et al. 1998, AJ 116, 1009, and Perlmutter et al. 1999, ApJ 517, 565 | a derivation's pin, [the far lamp through a detector](designs/far_lamp/BRIGHTNESS.md) (record 282): the stream read at 1 / (1 + z) of the lamp's rate with the birth content per click (DERIVATIONS_BEAM 6.4), the flux L / (4 pi d^2 (1 + z)) with d = (c_0 / H) ln(1 + z), d_L = (c_0 / H) ln(1 + z) sqrt(1 + z) = (c_0 / H)(z - z^3 / 24 + ...): q_eff = +1; `far_lamp_map.out` section 2 | H = 1 / 400, T_D = 110, S_1 Q = 64 (section 15's stream); `expansion-v1` not built | FAIL: +1 against -0.53, 1.53 apart, on the decelerating side of Einstein-de Sitter (+0.5); pinned; the run not made |
| 11b | The stretch of a far lamp's stream over 1 + z (the time dilation of the light curve) | the exponent b of the stretch (1 + z)^b: b = 0.97 +- 0.10, Blondin et al. 2008, ApJ 682, 724 (to verify against the source); the expanding form's b = 1 | the same pin: 400 rows released over 400 intervals arrive over 1452 intervals at 300 Links, the factor 3.639 against e^(H d / c_0) = 3.629 (`far_lamp_map.out` section 4 (a)); the stretch equals 1 + z, b = 1 | the same | PASS: b = 1 within the measured 0.97 +- 0.10; pinned; the run not made |
| 11c | The surface brightness of a resolved source at z over its surface brightness at rest (Tolman's test) | (1 + z)^-4, Tolman 1930; measured as (1 + z)^-n with n between 2.3 and 3.1 in the R and I bands before any correction and consistent with 4 once the sources' own brightening is removed, Lubin and Sandage 2001, AJ 122, 1084 (to verify against the source) | the same pin: the board's Nodes and the fan's lines fixed under the wall (15.5), a ruler of l Nodes at d subtends l / d, the flux (1 + z)^-1: the surface brightness (1 + z)^-1, n = 1 (`far_lamp_map.out` section 4 (b)) | the same | FAIL: n = 1 against 4 (against 2.3 at the least), three powers of 1 + z at the most; at z = 1 the ratio 0.500 against 0.062; pinned; the run not made |
| 13 | The bending of light beside a mass, the full deflection over the time part's alone, 1 + gamma (the space part doubling the time part; the delay likewise) | 2 at the Sun's limb: 1.75 arcsec against the time part's 0.87 (Dyson, Eddington and Davidson 1920, Phil. Trans. R. Soc. A 220, 291, read 1.98 +- 0.16 in units of 0.87 arcsec; the VLBI 0.99992 +- 0.00012 of gamma above) (to verify against the source) | the optical pin worlds, [`examples/events/optical/`](../examples/events/optical/README.md) (series K's geometry at the pair [1, 16384], M = 2^16, the beam at b = 6 and 8; `expectations.json`, `run_2026_09_22_bresenham` and `run_2026_09_22_every_family`): the beam's centroid shift on the screen -1.993 / -3.989 pixels at gamma 0 / 1 (DETECTOR), the ratio 2.00 within the pinned 0.25; at b = 8 the ratio 1.92 within 0.66; the delays 2.95 / 4.94 intervals, the ratio 1.67 outside 2.00 +- 0.25 by 0.08 | N = 64; K = 2^30 (series K's); the pixel's 0.5 and the interval's 1 | disagrees on the law's own number (2026-09-23, the auditor's finding confirmed by the reviewer's re-run, [DISAGREES.md](designs/fail_rows/DISAGREES.md) (PR #1002, merged at 0d0865f7) sections 7 and 9): the time part alone, the centroid shift -1.993 pixel and the delay +2.95 intervals at gamma_PPN 0 (DETECTOR, `mass_g0` against `control_g0` at head, the pin -1.93 +- 0.5 met, equal to `run_2026_09_22_bresenham`'s to the last digit), half of the declared gamma 1 world's -3.989, a factor 2 against nature's 1 + gamma = 2 under the register's own conversion (COMPUTATION on two DETECTOR shifts through the declared weight rule (1 + gamma) content x e_D, the 1 the time part; record 1216); series K's 0.000 pixel the suspension 0 worlds' reading, history. For the ratio: NOT COMPARED (gamma an input of kind 2, the owner's declaration of 2026-09-22): the ratio 2.00 reads the declared 1 + gamma back, the form of the space part doubling the time part on the lattice's lines, an implementation gate as row 2c's and not evidence about nature; the reading that would compare is a derivation of the space part from the law, which no one has |
| 12 | The clock's field at two distances from a crowd at the same push (the same g): the ratio of the two clocks' shifts, the form of the field a clock reads (the potential, 1 / r, or the flux, 1 / r^2) | 2.00 at the distances 6 and 3: the potential Phi = g r at equal g, the form nature's clocks share between two heights: the GPS gravitational term 45.7 us per day equals the potential's G M (1 / R - 1 / r) / c^2 with the one constant fixed by the ground's gradient g h / c^2 (Ashby 2003, Living Rev. Relativity 6, 1; Pound and Rebka 1960, Phys. Rev. Lett. 4, 337: 2.46 x 10^-15 over 22.5 m), and the eccentric Galileo satellites' modulation follows the potential to 2.5 x 10^-5 (Delva et al. 2018, Phys. Rev. Lett. 121, 231101) (to verify against the source); a flux form would read 0.62 of the GPS term and twice the Galileo modulation | series T, `examples/events/clock_word/` (the register's entry [T, the clock's word](EXPERIMENTS.md#t-the-clocks-word-2026-09-21), `readings.json`, main afb533a8; REPLICATED by the Replicator, every reading of `readings.json` and every fingerprint equal, [REPLICATIONS.md's block `clock_word (T)`](REPLICATIONS.md#clock_word-t), PR #601): DETECTOR, the `1 + z` of a lamp's light at x = 110 from a lamp at 3 and at 6 Links from two crowds of the same release F in the windows 200 to 350 and 350 to 500: the presence word (the declared alternative, `reads: "presence"` on the entry; the law's default until the model owner's word of 2026-09-21, record 394, BEAM_LAW step 5 as first written: the owed rate a_r n / d, a_r the presence, n / d the suspension pair) 1.3000 / 1.3000 at 3 and 1.3000 / 1.3000 at 6, the ratio of the two rates 1.000; the age word (the law's default since record 394: the engine's `count_owed` counts the age moment by default and the presence only on an entry that reads presence, the chief physicist's audit of the generic laws on the owner's word, record 1264; `reads: "age"` on the lamp's entry, note 25) 2.6517 / 2.6514 at 3 and 4.1500 / 4.1506 at 6 (the rate a_tau n / d, a_tau the age moment), the ratio 3.1503 / 1.6516 = 1.907 (the pin 1.909, [the read](designs/clock_age/NOTE.md) section 6: the lattice's dwelling ages 5, 6 and 10, 11) | N = 64; `suspension` [1, 2^16], F = 4915 per source per interval, the owed rate 0.30 to 3.15 (the scale is the suspension pair's, not the word's: nature's G M / (r c^2) is 7 x 10^-10 at the Earth); the word declared per table entry | the presence word: history, superseded by the age word (the model owner's word of 2026-09-21, record 394: the age moment is the law's default word, clock-age-v1 the engine's default; marked 2026-09-23 on his word, tier (c)), its verdict kept beside it: FAIL on the form: 1.000 against 2.00 (the clock reads the flux, flat along the beam; at the Earth 0.62 of the GPS term and twice the Galileo modulation); the age word PASS on the form: 1.907 against 2.00, 4.7 percent below by the lattice's grain (the potential's form); the law's default word is the owner's to choose; replicated (the block `clock_word (T)` of REPLICATIONS.md) |

## The notes to the rows

**1a, the record's pair.** The reading is the click of one record at two
counters (series L3; the design's `bell.py`), the cells over 64 births
(the birth phase u = 0 .. 63) at the CHSH labels (0, 8), (0, 24), (16, 8),
(16, 24) on the circle of N = 64: E (the correlation at one pair of
settings) x 64 = 44, -44, 44, 44, S = 176 / 64 = 2.75, every marginal 32 / 64 (no-signalling exact). Against Hensen 2015:
(2.75 - 2.42) / 0.20 = 1.65 standard errors, within two, so PASS by rule
(e); and a measured S is the ideal S times the apparatus's own visibility,
so the measured value is a lower bound on what an ideal apparatus would
read, which the law's 2.75 satisfies. Against the quantum bound: 2.75 is
2 sqrt 2 - 0.078 at N = 64 (the design's epsilon(N), registered as not
meeting 4 / N at this N); at N = 1024 and 4096 the register reads S =
2896 / 1024 and 11584 / 4096 = 2.828125 (`pair_n`), 0.0003 below the
bound and 2.04 standard errors above the measured. The choosers on the
GameBoard (`bell_choosers.json`, `pair.registered_S` = 156 / 64 = 2.4375
on the ordered quadruple (0, 25) x (8, 29)) read within 0.09 standard
errors of Hensen's value, but on a quadruple that is not the CHSH optimum,
so the row's number is 2.75. The reading needs no wheel: both arms carry
the one u.

**1b, the phase-form window.** Under the one click the ten A2 worlds read
S = 2 exactly (every pair of a world in one cell, E = +1 or -1 by the
settings' half circles), the register's `chsh_sum` = 2 and `primed_sum` =
2, with 115 of the tool's 350 crowd-form criteria failing as registered.
S = 2 is the local bound: a window that reads each row's own phase against
its own setting is a local deterministic response, and A2's registered
verdict is "the model's limit, S = 2 against nature's 2.4 to 2.7". The
row is kept because the reading is registered; the law's Bell reading is
the record's pair (1a), which reads the one record at two places.

**2a, the two-slit visibility.** The registered visibility is of the
CLICKS: `slits_huygens` on `main` declares the lamp's golden-rate birth
wheel [2531, 4096] and runs 4300 intervals for 4096 births under the
exact phase at the click (the register entry L2b, re-registered under
the birth wheel; the run's record beside the world in the amplitude
README, L2; every one of the records 1 to 4096 gathered). The clicks
read the visibility 0.966 between the two-source cosine's bright pixels
(y = 35 to 38, 59 to 61, 82 to 85; 23.5 pixels apart, the exact two-path
law's 23.3, [DERIVATIONS_BEAM 7.1](DERIVATIONS_BEAM.md#71-youngs-fringes))
and its dark ones, from the Farey fan of width 48 with the angle weights;
the record's screen WEIGHTS (the Gram weight per cell: the cell's share
of the click) read 0.954 (record 164), and the wheel turns the weights
into counts: the histogram's Pearson with the first record's own rungs
1.000 over the 126 cells, every count within 2 of its width. Of the
pins set before the run, the dark cells 0 to 3 are met (the mean 0.68);
the counts' Pearson with the cosine, 0.891 against the pinned 0.96, is a
miss and not called met: the pin was derived for the screen's fan (the
map's section 8, the screen share 0.35) and not for this world's own
Farey fan (the screen share 0.418, the peak at 0.012 of the total), and
the weights' own Pearson is 0.895. Every number in this paragraph is a
detector reading (the clicks on the screen's cells), from the register
entry L2b and the run's record; the world's `expectations.json` pins the
sibling `two_slits` and not this run. The published value: Grangier, Roger and Aspect
1986 read a visibility of 98 percent with one photon at a time in a
Mach-Zehnder interferometer, the same two-path observable in another
geometry; the two-slit build-ups with single electrons (Tonomura et al.
1989, Am. J. Phys. 57, 117; Bach et al. 2013, New J. Phys. 15, 033018) show
the fringes without a published visibility figure, which is the caveat.
Nature's ideal for two equal openings is 1, and the measured 0.98 is a
lower bound on it, so the law's clicks at 0.966 are short by 0.014 of the
measured and 0.034 of the ideal (the weights' 0.954 by 0.026 and 0.046):
FAIL, with the cause registered (the fan's grain: the scratch map of
record 160 gives 0.94 at P = 32, 0.97 at P = 48 and 0.96 at P = 64 in the
weights, the run 0.954 at P = 48 in the weights and 0.966 in the clicks);
whether a wider fan or a finer weight grain closes the gap is not
registered.

**2b, the Mach-Zehnder.** `mz_equal`'s split is the Pythagorean (20, 21)
pair, whose offers at the two ports are 1681 / 1682 and 1 / 1682 (the
design's table; the (1, 1) balanced split of `mz_balanced` gives 1 and 0
with the dark port's rows cancelled on the GameBoard); the visibility of
the offers is (1681 - 1) / 1682 = 0.9988 and the clicks over 64 births are
64 and 0. The verdict rests on the clicks (DETECTOR: the two ports' click
records over 64 births, the dark port 0, the visibility in the clicks
1.000): against Grangier 1986's 98 percent, above the measured lower bound,
PASS. The offers' 0.9988 is a number of the apparatus layer (the record's
ledger of offers, `mach_zehnder.mz_equal.offers`), no measurement: it
stands beside the verdict as a diagnostic, labelled so, never the ground of
the PASS (the model owner's rule of 2026-09-22, records 562 and 564; the
audit of record 567). The 1 / 1682 is the register's own departure from the
ideal, the (20, 21) split's imbalance, a declared table and not a fit.

**2c, the power of the click.** [DERIVATIONS_BEAM 6.5](DERIVATIONS_BEAM.md#65-the-uniqueness-of-the-clicks-square-a-lattice-gleason)
reads the power k of the click's form off two registered click lists:
`mz_345`'s 63 / 1 holds iff 7^k lies in [125 / 3, 127), k in [1.917,
2.489), and the far pair's cells 27, 5, 5, 27 iff k in [1.784, 2.054); the
same split at N = 32 (`mz_345_n32`, 31 / 1) and N = 128 (`mz_345_n128`,
125 / 3; the auditor's round 4, run on 2026-09-21) reads k in [1.548,
2.129) and [1.835, 2.012); the intersection [1.917, 2.012) contains 2 and
excludes 1 and 3, its lower bound N = 64's and its upper N = 128's (until
2026-09-21 the intersection was [1.917, 2.054), the pair's upper bound). Nature's
counterpart of "the power is 2" is the vanishing of the third-order
interference term, Sorkin's parameter, read as kappa = 0.0064 +- 0.0119 by
Sinha et al. 2010 in a three-slit experiment: consistent with the
quadratic form. NOT COMPARED to this experiment (the model owner,
2026-09-22): the window is read back from click cells of an engine whose
click has the square built in, an implementation gate on the click's form
and not evidence about nature; kappa is not computed here, and a
three-opening world that would read it is not registered.

**3, the deceleration parameter.** The register's q is the second-order
coefficient of the Hubble diagram read by the detector at the centre: z
(the redshift) from each star's record against the light's age tau (the
light-travel time), H (the Hubble rate) free, over the late window 300 to
400 (`registered_window`); the coasting crowd (no gravity) reads -0.108,
inside the bracket -0.25 .. +0.25 of the exact Milne form q = 0, and H (t_0
+ T_0) = 1.026 (the Hubble rate times the age of the throw at the reading,
1 for the exact Milne form); the gravity crowd +0.922 under the source rule and +0.345
under the flux weight, the double crowd +1.500 and +1.190; the growing
wall of section 15 is the Milne case exactly, q = 0, the same z(tau) as
the throw. Nature's q_0 = Omega_m / 2 - Omega_Lambda (Omega_m the matter
density parameter, Omega_Lambda the dark-energy density parameter): with
Planck 2018's Omega_m = 0.315 +- 0.007 and a flat universe, -0.527 +-
0.011 (the register's design used -0.55, the round Omega_m = 0.3). The
discrepancy: -0.108 - (-0.53) = +0.42 for the coasting reading, 1.7 times
the register's own bracket; +0.87 to +2.0 for the gravitating readings.
FAIL, as G2's verdict says in its own words: "the law has no term that
gives q < 0: nothing here removes dark energy and nothing mimics it".
Two caveats on the observable: the supernova q_0 is read from luminosity
distances and the law has no luminosity distance (a beam does not dilute,
G2's open item), so the register's q is read against the light-travel
time, the second-order coefficient of the same diagram in another
distance; and q_0 is nature's value today, while the register's is the
crowd's over one window.

**4a, the muon.** HYPOTHESES 21 states the law's clock in motion: a body's
clock is the count of its self-creations, advanced at every interval in
which it owes nothing, so a body thrown at any speed ticks at the rate of
one at rest, and its `become` at 64 turns fires at tick 64 at every speed
(the ratio of the lifetime in flight to the lifetime at rest, 1);
[DERIVATIONS_BEAM 4.3](DERIVATIONS_BEAM.md#43-a-moving-clock-the-rate-is-one-at-every-speed),
[12.4](DERIVATIONS_BEAM.md#124-the-pins-for-the-run-written-before-it) and
[12b.3](DERIVATIONS_BEAM.md#12b3-the-seventh-verb-after-1-and-2) derive
the same: none of the six verbs carries gamma (the Lorentz factor) into a
body's own counter, and the bond clock of 12.3 slows anisotropically
(gamma^2 along, gamma across), which is not the muon's isotropic gamma.
The run J4 is defined (FORM.md section 4 pins the ticks under form B:
today's law 64 at every speed; lorentz-v1 71 and 126 at 0.43 and 0.86 of
c) and not made; no world file exists. Bailey et al. 1977 read the
lifetime of muons at gamma = 29.33 in the CERN storage ring dilated by
gamma, the dilation confirmed to a fractional error of about 2 x 10^-3 at
95 percent confidence (the Boss's brief gives 0.1 percent; the figure is
to verify against the source). FAIL by the factor 29.33, pinned; the open
decision is record 230's: (A) the six alone, the law predicting against
the measurement unless a detector-side reading gives gamma; (B) the
seventh verb, a root at a declared grain under lorentz-v1; (C) the
reading budget, the mover's owed count under the crossing count (section
12c ordered). The row is also the NOT YET of the run.

**4b, the moving lamp's clock.** The one registered reading of a clock in
motion is G2's coasting star: `s_mz2`, thrown at beta = 0.2674 (beta the
speed as a fraction of c), whose light the detector reads at z = 0.2636
(the README's per-star table, the clock-free world; the coasting clicks
identical in the second and third runs). 4.3 gives the comparison: the
classical Doppler 0.2674, and nature's 1 + z = gamma (1 + beta) with gamma
= 1.0378, z = 0.315; the register's reading is 0.0038 below the
classical (a grain and a third of the README's 0.003) and 0.051 below the
relativistic, 17 grains: "the absence of gamma is registered, not only
derived". The published value: the Ives-Stilwell experiment and its
successors read the time-dilation factor in the Doppler shifts of a moving
emitter; Botermann et al. 2014 at beta = 0.338 (near the register's star)
confirm gamma to 2.3 x 10^-9 (to verify against the source). FAIL by 0.051
in z. Row 4a and this row are one finding, a body's clock at rate 1,
read once as a pin and once as a click.

**5a, the grain's anisotropy.** The pace of a row on the direction D (D
the direction vector, |D| its Euclidean length, T_D = isqrt(3 |D|^2 Q^2)
its resolution, the root taken once at load) is Q |D| / T_D Links per
interval; FORM.md section 1 checked it over every primitive direction
within 64 at Q = 64: from 0.5774 (exact on the cube diagonals, where 3
|D|^2 Q^2 is a square) to 0.5818 (64 / 110 on a heading), so the fractional
anisotropy is (0.5818 - 0.5774) / 0.5774 = 7.6 x 10^-3. The scaling with Q
is not written in FORM.md as a formula and is elementary from the floor:
T_D loses less than one unit to isqrt, so a direction's pace exceeds
1 / sqrt 3 by less than 1 / T_D = 1 / (sqrt 3 |D| Q) of itself, largest on
the headings (|D| = 1), never below 1 / sqrt 3, and "vanishing as Q
grows" ([DERIVATIONS_BEAM 3.5](DERIVATIONS_BEAM.md#35-what-departs-and-where),
item 4): the anisotropy is bounded by 1 / (sqrt 3 Q - 1) = 9.1 x 10^-3 at
Q = 64, the registered 7.6 x 10^-3 being 0.84 of the bound (the heading's
110.85 rounded to 110). Under the bound 10^-17 the grain must satisfy sqrt 3
Q >= 10^17, Q >= 5.8 x 10^16, the first power of two 2^56 (7.2 x 10^16,
anisotropy 8 x 10^-18); under 10^-18, Q >= 5.8 x 10^17, 2^59 (1.0 x
10^-18) or 2^60. Against the word width ([DERIVATIONS_BEAM 13.3](DERIVATIONS_BEAM.md#133-the-grain-from-k-the-budget-equation-and-the-registers-widths):
Q |D|_max <= 2^61 / sqrt 3): at the register's fan radius |D| <= 48 the
largest Q is 2.8 x 10^16 (2^54.6), whose worst-case anisotropy is 2.1 x
10^-17, above the bound; the bound is reachable within 64 bits only with
the fan restricted to |D| = 1 (Q up to 1.3 x 10^18, anisotropy 4 x 10^-19)
or with a wider word. BOUND, on Q, and a statement of what the word
allows. The caveat of the dictionary: a resonator experiment compares two
arms whose lengths are themselves light-clock readings (5.7's distance
row), so how a rotated resonator reads on the lattice depends on that
reading; the row states the pace per direction as the flight table gives
it, which is what an arm of a declared Euclidean length would read.

**5b, the frame's anisotropy.** Section 12 finds the law's rows retarded
at c in the lattice's frame with nothing to contract (12.1: the bond is a
whole Link), so a light clock in motion at beta is the classical ether
clock, its round trip gamma^2 x 2 d / c along the motion and gamma x 2 d /
c across (d the arm's length; 12.3; on the register's flight table 1.375 and 1.140 at beta =
0.4297 by the host script, farther from gamma by the whole-Link steps).
Two arms of one length at right angles then differ in their round-trip
time by the factor gamma, a fractional anisotropy gamma - 1 = beta^2 / 2:
the quantity Michelson and Morley 1887 sought and did not find, and that
the resonator experiments bound at 10^-17 to 10^-18 today. A laboratory on
the Earth moves at 30 km/s (beta = 10^-4) around the Sun, so relative to
any frame fixed in space its speed is at least of that order for part of
the year (5 x 10^-9), and relative to the frame of the cosmic background
370 km/s (7.6 x 10^-7); a null at 10^-17 needs the laboratory below 1.3
m/s in the lattice's frame all year. FAIL by eight to twelve orders of
magnitude (5 x 10^-9 to 7.6 x 10^-7 against 10^-17 to 10^-18), pinned
by 12.3 (the pair in motion of 12.4 is the run, not made); what would
remove it is a contraction of the arm along the motion by 1 / gamma,
which is route B or C of record 230 and not the six verbs (12.5 (vi)).
The row is the second reading of one finding with row 4a: the law stands
nearer to Lorentz's ether than to Einstein's postulates (record 231) and
has not given Lorentz's number.

**6, Bohr's lines.** Series H registers the orbit, not a line: on the
base no orbit closed by the criterion; under the step drive r = 8 closed
four times and r = 12 five (r the radius in Links) with the coherence C(4)
= 1.01 against the expected 2.0; under the signed drive the loops precess out; and 7.2 finds
the design's closure 4 p r = j h to be the action 2 pi p r = j h (p the
momentum's magnitude, h the world's action, j the whole number of the
closure, pi the circle's ratio; r = 12 the one registered radius with a
whole j) and the levels and the Rydberg
lines not reached: the law has no energy of an orbit and no transition
between orbits, and what a detector reads of a closed orbit is its
orbital frequency, about 1 / j^3. NOT YET. The dimensionless target is
Balmer's ratio nu(H beta) / nu(H alpha) = 27 / 20 (nu the frequency), 1.3500
from the measured wavelengths 656.279 and 486.135 nm (the reduced mass and
the fine structure cancel in the ratio at this precision). The reading
that would be needed: the phase rate of the faces' `wave` record (the
click phases' slope) of two orbits at closing radii with whole j, as a
ratio, and a rule by which the electron leaves one closed orbit for
another, which the law does not have.

**7a and 7b, the deuteron and the alpha.** Series N's rule (binding-v1)
is one condition on one verb: at its first contact a nucleon gives its
held paid family `bond` (quantum 1, lifetime 3, held 2 per nucleon) to
the flight away from its partner, and the border `lifetime` clicks the
rows two Links away with their content, the released binding energy
read as clicks. B1 `deuteron_bond`: two `bond` clicks of content 2 each at
tick 19, the escaped content 4 of the declared 3677, 0.109 percent, the
mass a detector reads 3673; nature's E_B (the binding energy) over m_p +
m_n (the proton's and the neutron's masses) is 2.2246 / 1877.84 = 0.1185
percent (AME2020). The register itself pins 0.109 against nature's 0.1185.
The give is a declared width and not a derivation ("the law derives no
binding energy": the size of the give is the held `bond` per nucleon, an
input as record 106 makes every content an input), so the comparison is
a BOUND on that input: at the register's contents nature's fraction is
4.35 units of 3677, which no whole give reaches (4 units give 0.109, 5
give 0.136), the registered 2 per nucleon being the nearest below, 8
percent short. B3 `alpha_square_bond`: the give is once per body, so four
nucleons give 8 and the binding is linear in the nucleon count, the ratio
to the deuteron 2.0 where nature has 28.296 / 2.2246 = 12.72: FAIL by the
factor 6.4, stated before the run as the law's failure and not tuned; a
give that grows with the number of bonds a body makes is not the rule as
built. The square's dispersal (series I: the line p n n p holds, the
square shears apart) is the same finding without a number.

**8a, the decay curve.** J1 reads the shell's 64 beta clicks of 64
neutrons of one clock: a step, the 10th-to-90th-percentile width of the
click ticks over their median 0.036 (`j1_lattice`, the median 549) and
0.038 (`j1_source`), against 3.17 for a memoryless survival (the 10th and
90th percentiles of an exponential at ln(10 / 9) and ln 10 lifetimes over
the median's ln 2: (ln 10 - ln(10 / 9)) / ln 2 = ln 9 / ln 2 = 3.17, an
identity of the exponential form; the form itself is what every neutron
lifetime measurement fits, the bottle measurement of Gonzalez et al. 2021
among them). FAIL by the factor 88: the law's `become` fires at a clock
count, one tick for one clock, and a population of one clock decays at
once (PREDICTIONS entry 10, the exponential needing the declared bath of
the design, not built). The second reading of the same world, every beta
click at the one content 3 against nature's continuous beta spectrum, is
a FAIL of the same kind with no single number to put in the table.

**8b, the neutrino's filter.** J2's window admits the w consecutive steps
of the circle about its setting (w the window's width), so a reader
behind a source of stride coprime to N admits exactly w / N of its rows
(`j2_filter`: 16 of 1024 at w = 1) and an identical reader behind it,
reading the same residue, finds nothing (0 at every one of the 127 behind;
the ladder of 64 centres exhausts the beam and 64 more read nothing).
Nature's counterpart: two identical detectors in line read the same
neutrino rate, since a beam of MeV neutrinos is attenuated by less than a part in
10^16 per metre of ordinary matter at a cross-section of order 10^-43
cm^2 (Formaggio and Zeller 2012), so the ratio is 1 to that precision. FAIL:
0 against 1; the register's own words, "a filter set by the spread of its
centres, not an attenuation set by its depth" (PREDICTIONS entry 8), and a
fraction flat in the emitter's rate where nature's cross-section rises
with the energy (entry 7). The stride-2 worlds (`j2_stride2` 32 of 1024,
`j2_stride2_odd` 0) show the fraction to be the residue's and not the
rate's.

**9, Malus.** A polariser needs no feature: the two-state label is the
record's joint label bit, the rotation by the polariser's angle is the
`rotate` entry on the GameBoard or a `sum` set's window at the end (the
half-angle tables of 2N, the setting s the angle 180 s / N degrees), and
the projection is the which-path `read` at a `sum` set, whose factor
selects the label so that the click's cells split by it; the rows the
polariser absorbs go on and click in their own cells, and the fraction
transmitted is the pass cells' count over the births (the mathematician's
[note](designs/malus/NOTE.md), the owner's go of record 330). The three
worlds ran once, 300 intervals each, completed and conserved at every
tick; over the records 1 to 256 (u = ordinal x 159 mod 256 over every
residue once) the cells read (DETECTOR) 128 / 128 for one polariser at 45
degrees, 0 / 256 for two crossed, and 64 / 64 / 64 / 64 for the third at
45 degrees between two crossed: the pass 1 / 2, 0 and 1 / 4 of the births
exactly, every pin met and none moved, every cell within its rung width
over all 289 records gathered. PASS: at 45 and 90 degrees the tables are
exact (181 = 181; 0 and 256), so these three fractions carry no rounding;
where the rounding shows, at 22.5 degrees, the tables give 219 of 256
against cos^2 = 0.8536 (the note's section 3; run on 2026-09-21, the
auditor's round 10 part 2: 219 / 37 at 22.5 degrees, 37 / 219 at 67.5 and
the chain 187 / 32 / 5 / 32, DETECTOR, engine-exact, +0.0019 the tables'
rounding). The limit:
one which-path read per arm with a rotation before it, so the entry's
four-polariser chain at 22.5-degree steps (a second read after a
rotation) is not covered; a polariser here is a rotation and a which-path
read, not a body with a sink. Nothing entered the law: no identity, no
key, no rule.

**10, the single opening.** A10 read the `wave` record behind one opening
of w Nodes: the product w x FWHM(sin theta) reaches 0.886 lambda within 22
percent at w = 27 (4.99 against 4.09 in Links, 1.08 against 0.886 in units
of lambda), the Fresnel number 1.46 there named as the cause, and is not
read at w = 3 and 9, where the sparse fan does not form the lobe. Those
numbers are the crowd form's, kept as history since the one click; the
record form's `w27_beam` did not complete on the host. NOT YET under the
one click, with the crowd form's 22 percent as the last reading. Nature's
0.886 is the Fraunhofer constant of a single slit, read with molecules by
Nairz, Arndt and Zeilinger 2002 as the verification of the uncertainty
relation.

**13, the bending of light and gamma's standing.** The optical identity
(`optical-v1`, [the one-wall note](designs/one_wall/NOTE.md); every family
under one wall, [EVERY_FAMILY.md](designs/one_wall/EVERY_FAMILY.md))
stretches a row's flight wall by the crowd's age moment at the
coefficient 1 + gamma and pushes the row at the weight (E'^2 + 3 gamma
**p** . **p**) // E', gamma the world's key: at gamma 0 the time part alone
(the bending 2 G M / (b c^2) of a clock's rate, the delay of the wall),
at gamma 1 the space part beside it, the doubling nature reads. The
model's registered ratio 2.00 (the mass world's shifts; the far world's
1.92; the delays' 1.67, outside its bracket by 0.08 under the one floor)
is the engine reading back the coefficient declared in the key, as row
2c's window reads back the click's square: an implementation gate. What
would make it a comparison is a derivation of gamma from the six verbs,
which no one has ([DERIVATIONS_BEAM 5.4](DERIVATIONS_BEAM.md#54-light-no-optical-metric-on-main-the-meetings-turn-as-a-key));
the model owner declared gamma = 1 an input of kind 2 (the one set's
table; 2026-09-22, step 4 of the generic bending, on his word "continue
until the whole list is handled"), so the row is NOT COMPARED until such
a derivation exists, and the bending enters the law (step 5) with gamma
as an input, as S enters it.

**12, the clock's word.** [The read](designs/clock_age/NOTE.md) of
2026-09-21 pinned the test before the run (section 6): two crowds of the
same release at 3 and at 6 Links are the same push (on the lattice only
the two headings' rows dwell at the lamp's Node, two intervals each, so
the presence is 4 F at both distances), and only a clock counting the age
moment reads the distance (22 F and 42 F, the dwelling ages 5, 6 and 10,
11). Series T ran the four worlds under beam-v1 as declared, no change
under `src/`, and met every pin: the presence clock reads 1.3000 at both
distances, the age clock 2.65 and 4.15. Nature's clocks between two heights
follow the potential: the GPS gravitational term equals the potential's
form with the constant fixed by the ground's gradient (45.7 / 45.7 =
1.00), where the flux form gives 0.62 (28.3 us per day) and twice the
eccentric modulation of the Galileo satellites (`clock_age_map.py`
section D). The reading's own form is the ratio of the two clocks' fields
at the same push: the potential 2.00, the presence word 1.000, the age
word 1.907 (the grain of the dwelling ages; the continuum's 2.000 outside
the pin's 1.91 +- 0.05, as the read says). The scale is not the word's:
the world's `suspension` pair sets the owed rate (0.30 to 3.15 here),
nature's G M / (r c^2) is 7 x 10^-10 at the Earth's surface. The law's default word (BEAM_LAW step 5)
is the presence, and the age word is a declared option per entry (note
25); the row carries a verdict per word, and the owner chooses the default.
Since record 394 (the owner, 2026-09-21) the age word is the law's default
(clock-age-v1, the engine's default), and the presence word's verdict is
history (marked 2026-09-23 on the owner's word, tier (c)); nothing above is
deleted.
Measured by the G2 session and replicated bit-exact by the Replicator
(REPLICATIONS.md, the block `clock_word (T)`, PR #601).

**11a to 11c, the far lamp through a detector.** The pin is a derivation
([BRIGHTNESS.md](designs/far_lamp/BRIGHTNESS.md), the owner's order of
record 280, received as record 282), not a registered run: the rule of
section 15.2 on its own integers (the wall `2 T_D a`, `a = H_den + H_num
x tick`, H = 1 / 400, `T_D = 110`, `S_1 Q = 64`), a lamp at rest releasing
one row per interval, a detector at rest counting. The arithmetic: the
stream arrives `1 + z` times slower (clicks per interval 0.650 at 100
Links and 0.275 at 300, against `1 / (1 + z)` = 0.651 and 0.276) and every
click carries its birth content (6.4: no rule makes the content follow
the frequency in flight), so the flux has one factor of `1 / (1 + z)`
where the expanding form has two; with `d = (c_0 / H) ln(1 + z)` the
effective luminosity distance is `ln(1 + z) sqrt(1 + z)` in units of
`c_0 / H`, whose series `z - z^3 / 24` has no `z^2` term, `q_eff = +1`
(11a). Against flat Lambda-CDM at `Omega_m = 0.3` as the stand-in for the
measured curve with the intercept free, the shape residual is 0.339 mag
rms on z from 0.01 to 1.5 (Milne 0.055, Einstein-de Sitter 0.194); the
register's own Pantheon+ fit ([HYPOTHESES 7](HYPOTHESES.md#7-redshift-without-recession-and-no-dark-energy))
found the one-factor reading behind at every exponent. The stretch of
the stream is `1 + z` exactly (11b). The surface brightness falls as `(1
+ z)^-1` because the board's Nodes and the fan's lines are fixed under
the wall (11c). What would change 11a and 11c: a rule that lowers the
content a click reads with the redshift, not one of the six (it would
give `(1 + z) ln(1 + z)`, `q_eff = 0`, still not nature's); nothing in H,
the grain or the width S, which set the intercept. The run that would
register the pins: a lamp of rate 1 and a detector at 100 and 300 Links
on a periodic board under `expansion-v1` at H = 1 / 400, expected `1 + z`
= 1.539 and 3.639, clicks per interval 0.650 and 0.275, the content per
click unchanged.

## Readings with a counterpart in quantum theory but no published dimensionless figure at hand

Not tabulated, so that no source is invented: the Elitzur-Vaidman
fractions (`ev_29`: the absorber 1 / 2, D1 441 / 1682, D2 200 / 841 against
the ideal 1 / 2, 1 / 4, 1 / 4; Kwiat et al. 1995, Phys. Rev. Lett. 74, 4763,
made the measurement, its figure to be taken from the paper); GHZ's
products +1 and -1 exactly (`ghz_*`; the measured correlations of Pan et
al. 2000, Nature 403, 515, likewise); the neutrality of the neutron become
proton (the W world's charge [0, 1], the beta's -7344 against 4 x 1836: a
declared balance of the family table at load, not a prediction, against
nature's bound on the atom's neutrality). No Compton reading is
registered (the mass ladder A10 of section A is planned). Coulomb's and
Newton's inverse square are registered as shell means of the presence
(series E, k_s x r^2 constant within 7 percent over r = 6 to 14), which
are shell means by a replay, GAMEBOARD readings, and not admissible here
(records 163 (5), 562, 564 and 569: a probe's own record is a detector
reading at its Node, a replay or a shell mean is the board); the detector
form, Newton after a detector (a thrown body's clicks at a detector set at
two radii), awaits its run and is not yet registered.

## The tally

The register's rule (the physics-rule reviewer's line on PR #979, 2026-09-23): the tally counts what the cells say, and where the paper has moved ahead of a cell the tally says so per row; a history block is verbatim.

The count of 2026-09-23, the paper's: the register read at its head, the
rows above as they stand, the read of
[WHAT_IS_MISSING.md](designs/fail_rows/WHAT_IS_MISSING.md) section 0 and the
owner's words of records 941 and 955 (the model owner's plan for more rows
passing; the reconciler's read of 2026-09-23, 01:07Z).

| Verdict | Rows |
| --- | --- |
| PASS (3) | 1a (Bell, the record's pair, 1.65 standard errors), 2b (the Mach-Zehnder, the clicks 64 / 0 over 64 births, the visibility in the clicks 1.000), 9 (Malus, 128 / 256, 0 and 64 / 256 exact at 45 and 90 degrees; 219 / 256 and 187 / 256 at 22.5 degrees, the tables' rounding) |
| FAIL, in the table (12) | 1b (the window form, S = 2; a control, the local read-out's bound), 1c (the order channel: 15 / 16 under a = 0 and -1 / 16 under the cycle against nature's 0, DETECTOR; a row of the paper's register, WHAT_IS_MISSING.md section 1.2, not yet a row above), 2a (the two-slit visibility 0.966 in the clicks, 0.954 in the weights), 3 (q = -0.108 against -0.53), 4b (the moving lamp, 0.052 in z), 6 (Bohr's ratio: the electron escapes at 3407 intervals, DETECTOR, the runs of 2026-09-22; no line to read (the paper's row (Table 2); the register's cell above still reads NOT YET, to be re-read on its own order)), 7b (the alpha, a factor 6.4), 8a (the decay's step, a factor 88), 8b (the filter, 0 against 1), 8c (the massless neutrino, REFUTED by the oscillations), 13 (the bending of light: disagrees on the law's own number, the time part alone, the centroid shift -1.993 pixel at gamma_PPN 0 against the declared gamma 1 world's -3.989, DETECTOR, a factor 2 against nature's 1 + gamma = 2 under the register's own conversion (record 1216); the row's cell above: disagrees on the law's own number, NOT COMPARED for the ratio; series K's 0.000 pixel the suspension 0 worlds' reading, history), 14 (Newton's periods: T(24) / T(12) = 1.677 under the one constant and 1.512 under the line drive against the pin 2.00 +- 0.18; a row of the paper's register, WHAT_IS_MISSING.md section 1.13, not yet a row above) |
| FAIL, by their pins outside the table (4; no run) | 4a (the muon, a factor 29.33), 5b (the frame, eight to twelve orders), 11a (the far lamp's brightness, q_eff = +1 against -0.53), 11c (the surface brightness, one power of 1 + z against four) |
| BOUND (2) | 5a (Q >= 2^56 for 10^-17, beyond the word at the register's fan), 7a (the give per nucleon: 4 to 5 units of 3677 about nature's 4.35) |
| NOT COMPARED (1) | 2c (the power of the click: the window [1.917, 2.012) is an implementation gate, kappa not computed) |
| HISTORY (1) | 12 (the presence word, superseded by the age word; the age word's 1.907 against 2.00 not counted as a pass: record 394 made the age word the law's default, record 941 made the row history) |
| Not counted | 10 (NOT YET: the record form's `w27_beam` did not complete), 11b (PASS by a pin whose run needs expansion-v1, not built; the paper counts only rows read after a detector) |

The rows that moved between the block of 2026-09-21 (below, kept as
history) and this count, one line each with its record:

- 12: PASS under the age word then; HISTORY now (record 394, the age word
  the default; record 941, the row history).
- 11b: PASS by its pin then; not counted now (the paper counts only rows
  read after a detector; expansion-v1 not built; record 955).
- 6: NOT YET then; FAIL now (the runs of 2026-09-22, the escape at 3407
  intervals, DETECTOR; WHAT_IS_MISSING.md section 1.6); the paper's row
  (Table 2); the register's cell above still reads NOT YET, to be re-read
  on its own order.
- 13: NOT COMPARED then; FAIL for the law as built now (0.000 pixel,
  series K, DETECTOR; the generic entry a key; WHAT_IS_MISSING.md
  section 1.12); the paper's row (Table 2); re-read on 2026-09-23 (the
  reviewer's read of [DISAGREES.md](designs/fail_rows/DISAGREES.md) (PR #1002, merged at 0d0865f7)): the cell above
  reads disagrees on the law's own number (the time part, -1.993 pixel at
  gamma_PPN 0, DETECTOR) and NOT COMPARED for the ratio; series K's 0.000
  the suspension 0 worlds' reading, history.
- 1c and 14: added after the base 88d843ef (records 941 and 955;
  WHAT_IS_MISSING.md sections 1.2 and 1.13); their rows above are not yet
  written.
- 10: NOT YET then and now; not counted.

The sums: PASS 3, FAIL 12 in the table and 4 by their pins, BOUND 2, NOT
COMPARED 1, HISTORY 1, not counted 2. The block of 2026-09-21 read PASS 5 /
FAIL 13 / BOUND 2 / NOT YET 2 / NOT COMPARED 2.

## The tally by status (2026-09-23)

The model owner's GO on the form of the comparison with nature (record
1166, the Boss's order of 2026-09-23; a Highlights line): every row in
one of three statuses, "agrees" (within the stated tolerance),
"disagrees" (with the number) or "not predicted" (by the law as built,
the missing piece named in the row's line). The third status follows
from the structure of the law as built, in three lines:

- The law as built has no relativistic dynamics: a moving thing's count
  is r = 1 at every speed and nothing contracts. What depends on a moving
  clock's rate or a moving body's extent is not predicted by it; the
  identity under `covariant_readings` is a declared hypothesis, read
  beside such a row and never counted as the law's.
- The law as built has no term of the crowd's history: what depends on
  the emitters' clocks stretching with the flight time is not predicted
  by it; where the law's own crowd gives a sign, the sign is stated.
- A declared input is not a prediction: a content of the family table, a
  fan's width, a gamma declared per world are inputs of kind 2, and what
  reads them back is not predicted.

The referee's test every line must pass: a row sits in the same class had
its number matched nature. "Agrees" and "disagrees" are the rows the law
as built predicts, judged within the stated tolerance; "not predicted"
names the missing piece and prints the law's own number by a click all
the same. Every number's kind is named (DETECTOR a detector's click;
GAMEBOARD the host's view of the board; COMPUTATION the host's arithmetic
on a reading, or a pin before any run). Rows 12 (HISTORY), 2c (NOT
COMPARED), 10 (NOT YET) and 11b (PASS by a pin whose run needs
expansion-v1) keep their present words; row 1b keeps its mark of
2026-09-23 (a control); since the fold of records 1190, 1196 and 1204 (the
count paragraph below) the rows keeping their words are six, 2a among
them. The placement is the one to start from: the
physics-rule reviewer's read decides each line against
[WHAT_IS_MISSING.md](designs/fail_rows/WHAT_IS_MISSING.md) as merged.

The model owner's three kinds of "what is missing" (record 1173), named
once here and printed in brackets on every not-predicted line (a line may
carry two kinds):

- (1) the instrument is missing in the model: a moving thing's clock
  rate, a moving detector's count, a velocity from clicks, the crowd's
  history.
- (2) nature's number is a bound or a fitted parameter and not one
  measurement: said in the line beside the nature number.
- (3) no click definition yet for the quantity: a position, a brightness,
  a period.

The reviewer's rule (PR #979, 2026-09-23): a status is given only to a
measurement (a click's number with its kind); a number whose kind is
GAMEBOARD or a pin before its run waits outside the count with its run
named; the bracket of what is missing is printed on the not-predicted
lines alone and names the row's own missing piece.

The reviewer's principle, as the register's finding and not a decision
(the owner's word on a Highlights line pending): four rows (6, 10, 13,
14) read one thing: a fan bounded in Manhattan length is not a fan of
every direction (its angular density is the octahedron's, the axes 2.8
times denser in angle than the face diagonals, 5.2 times than the body
diagonals; its nearest direction to an axis at width P is atan(1 / (P -
1))); a pin may take the isotropic shell mean only where the fan is
declared uniform in angle at a grain finer than the reading or where a
click read the crowd; otherwise the law's number for that world is the
integral on the comb, computed before the run (the reviewer's read of
RUN_14, 2026-09-23).

The fold of 2026-09-23 on the owner's word (records 1190, 1196 and 1204;
the previous count and table kept below as history): of the ten
observables the law as built predicts (eleven once row 14 is read), four
agree within tolerance (1a, 2b, 9; 5a as a bound met), six disagree (1c,
6, 7b, 8a, 8b, 13), and eight are not predicted by construction (3, 4a,
4b, 5b, 7a, 8c, 11a, 11c); 2a NOT COMPARED until its source is verified.
The rows keeping their words are six (2a, 2c, 10, 11b, 12, 14); 1d is a
consistency check and 4c a FORM row, both outside the count. The rows
that moved, one line each with its record:

- 1d and 4c: entered from PINS.md section 5 as the reviewer's gate has
  them (record 1190); R2 and R4 placed beside 4a, 4b and 5b as the same
  family and not the same observable (record 1190).
- 7a: from agrees (a bound met) to not predicted, the give per nucleon a
  declared input read back (the owner's placement, record 1204, on the
  reviewer's read, record 1196).
- 2a: from not predicted to NOT COMPARED until the two-slit source is
  verified, the law's number a prediction under every fan (the owner's
  placement, record 1204; the grain's share at most 12 percent of the
  shortfall, KIND_AUDIT.md (docs/designs/fail_rows/, on main at 46c27396, PR #990) section 3).
- 8a: the row's cell from FAIL on the 0.036 to disagrees on the step, the
  width 0 in each neutron's own clock (record 1196).
- 3 and 4b: the time axis read in the detector's own clock at head, equal
  to the host's tick to the integer; statuses unchanged (record 1196).
- 12: the kind column names the ratio of two records' rates, the tick
  cancelling; HISTORY as it stands (record 1196).
- 4a, 5b, 11a, 11b, 11c: R3 in the kind column, a pin in closed form with
  no run a COMPUTATION, the law's own number; statuses unchanged (record
  1196).
- 13, 4a, 8a (2026-09-23, the reviewer's read of [DISAGREES.md](designs/fail_rows/DISAGREES.md) (PR #1002, merged at 0d0865f7); the count of record 1204 unchanged, the owner's word of record 1232): row 13 prints the law's own number on a coupled world (the time part, -1.993 pixel at gamma_PPN 0, DETECTOR) in place of series K's 0.000, the suspension 0 worlds' reading; row 4a's `become` line labelled DETECTOR (a body's own record); row 8a names the reading NOT MADE (the shell detector's own count under `clock_stamp`).

| Row | Status | The law's own number by a click, its kind | Nature | The tolerance met, the number missed, or the missing piece |
| --- | --- | --- | --- | --- |
| 1a | agrees | S = 2.75 (DETECTOR: the record's one gather over 64 births, the cells 27, 5, 5, 27) | 2.42 +- 0.20 | within 1.65 standard errors of nature's value; 0.078 below the quantum bound |
| 1b | a control (marked 2026-09-23) | S = 2 exactly (DETECTOR: the counters' clicks of the window form) | 2.42 +- 0.20 | a theorem of every local read-out, not counted; the law's row is 1a |
| 1d | agrees, outside the count (a consistency check) | each party's + count 32 of 64 at every setting pair (DETECTOR, replayed at head); the difference between the other party's settings 0 exactly (COMPUTATION from the cells) | 0 within the statistical error | 0 against 0, exact, by Theorem 5 (ALGEBRA.md 4.9): a theorem of the click's form, a consistency check the law must pass and not an independent prediction, outside the referee's count of predictions; the tolerance nature's statistical error on 0; the same at the seven grains 512 to 16384 (PINS.md section 5, record 1190) |
| 1c | disagrees | not a row of this table ([WHAT_IS_MISSING.md section 1.2](designs/fail_rows/WHAT_IS_MISSING.md#12-row-1c-the-order-channel)): 15 / 16 under a = 0 and -1 / 16 under the cycle, the second party's serial correlation at lag 1 (DETECTOR, met 16 of 16 against the algebra) | 0 | 15 / 16 against 0; the wheel a counter, the order deterministic |
| 2a | NOT COMPARED (the owner's placement, record 1204) | the visibility 0.966 in the clicks of `slits_huygens` (DETECTOR; the pin 0.9659 COMPUTATION, met bit for bit) | 0.98 (a Mach-Zehnder source; the two-slit figure unverified); the biprism's 0.94 | until the two-slit source is verified; the law's number 0.966 a prediction under every fan, the grain's share at most 12 percent of the shortfall (KIND_AUDIT.md (docs/designs/fail_rows/, on main at 46c27396, PR #990) section 3, COMPUTATION); a bound met against the biprism's 0.94 at the abstract's level; the Mach-Zehnder's 0.98 another geometry. Before the fold: not predicted by a declared fan width (an input of the third structure line; kind 2 in the inputs table of record 817) |
| 2b | agrees | the clicks 64 / 0 over 64 births, the visibility 1.000 (DETECTOR; the offers 0.9988 GAMEBOARD, a diagnostic) | 98 percent | above the measured 0.98 |
| 2c | NOT COMPARED | the power window [1.917, 2.012) (COMPUTATION from the click cells 63 / 1 and 27, 5, 5, 27, DETECTOR) | kappa = 0.0064 +- 0.0119 | kappa not computed; keeps its word |
| 3 | not predicted | q = -0.108 (DETECTOR, the pointer's z, read in the detector's own clock at head: the count of its self-creations under the age wall, r = 1.0000 with no crowd at the detector; CRITERIA (f), the re-run of 2026-09-22; equal to the host's tick to the integer; the registered run's time base was the host's tick (record 768), superseded; a two-way light clock at the detector, not read, reads the same count in no crowd (series X)); the law's own crowd q = +0.922 (DETECTOR, the record form) | -0.53 +- 0.01, a fitted parameter of the cosmological model, not one measurement | no term of the crowd's history; the sign the law's own crowd gives is the wrong one (a deceleration) [kinds (1) and (2): the crowd's history missing; nature's q_0 a fitted parameter] |
| 4a | not predicted | the muon's `become` at the count 64 at every speed, the ratio 1 (DETECTOR, a body's own record, the `become` line: ENGINE.md's readings by type, Highlights kind 9; labelled GAMEBOARD until 2026-09-23, corrected on the reviewer's read of [DISAGREES.md](designs/fail_rows/DISAGREES.md) (PR #1002, merged at 0d0865f7) section 2.2; the products' face clicks DETECTOR); beside it, under `covariant_readings`, the products' clicks at 369 and 345 (DETECTOR), gamma 1.1074 and 1.9558 by the declared identity; COMPUTATION, the law's own number by its pin, no run (R3, the kind audit's rule, record 1196) | 29.33 | no moving-clock rate (r = 1); the identity a declared hypothesis, not the law's [kind (1): a moving thing's clock rate] |
| 4b | not predicted | z = 0.2636 at beta = 0.2674 (DETECTOR, read in the detector's own clock at head: the count of its self-creations under the age wall, r = 1.0000 with no crowd at the detector; CRITERIA (f), the re-run of 2026-09-22; equal to the host's tick to the integer; the registered run's time base was the host's tick (record 768), superseded; a two-way light clock at the detector, not read, reads the same count in no crowd (series X)); beside it, under the key, 0.3674 (DETECTOR) for the pin 0.369 +- 0.003 | 0.315 | no moving-clock rate (the factor gamma = 1.0378 absent); the identity a declared hypothesis [kind (1): a moving thing's clock rate; a moving detector's count] |
| 4c | FORM row, outside the count until a nature source with a number is named | the round trip (1 + beta) / (1 - beta) read as the cart's own counts: 3.708 over 445 counts for the pin 151 / 41 at k = 3 and 2.054 over 497 for 43 / 21 at k = 5 (DETECTOR, RUN_4AB.md 6.3); under the key 4.774 and 2.308 beside them (DETECTOR, the hypothesis's) | (1 + beta) / (1 - beta) to all orders, the two-way form of every radar; no source with a number named yet | the law's worlds read 3.708 and 2.054 for 151 / 41 and 43 / 21, +3.05 and +1.48 counts off the closed form over the window, outside the version-1 band 2 / W as pinned in RUN_4AB (FAIL there) and inside the preregistration's band in ordinals and the meeting remainder (RUN_4AB 6.3); reads nothing of r, so it changes nothing in rows 4a, 4b and 5b (PINS.md section 5, record 1190) |
| R2, R4 (PINS.md sections 2 and 4) | beside 4a, 4b and 5b | R2 the Sagnac ratio (its run pending; the first arrangement not read: an emitter never clicks its own rows, the two pulses of one number collide at free Nodes, docs/designs/new_rows/RUNS.md section 4), R4 the round trip of row 4c: ratios of one detector's own counts (DETECTOR when run) | R2: Michelson-Gale 1925; R4: no source with a number yet | the same family and NOT the same observable: r-free by construction, reading nothing of the second order where rows 4a, 4b and 5b fail; never evidence on those rows (the reviewer's line on PR #988, record 1190) |
| 5a | agrees (a bound met) | the pace by direction 0.5774 to 0.5818 (COMPUTATION, the flight table); series Q's 290 of 290 face clicks at the derived tick, Node and face (DETECTOR) | delta c / c below 10^-17 | a bound on Q (Q >= 2^56 for 10^-17 at the register's fan), met as a bound |
| 5b | not predicted | the round trips gamma^2 along and gamma across, 1.375 and 1.140 at beta = 0.4297 (COMPUTATION on the flight table; the pair in motion not run; COMPUTATION, the law's own number by its pin, no run (R3, the kind audit's rule, record 1196)) | the null, beta^2 / 2 = 5 x 10^-9 at beta = 10^-4 | no contraction; the identity's reading beside it as a declared hypothesis [kind (1): a moving detector's count along and across, a velocity from clicks] |
| 6 | disagrees (the paper's row (Table 2); the register's cell above still reads NOT YET, to be re-read on its own order) | the electron escapes at 3407 intervals (DETECTOR, series H's world, the runs of 2026-09-22); no line read | Balmer's 27 / 20 = 1.35 | the loop opens, no line to compare ([WHAT_IS_MISSING.md section 1.6](designs/fail_rows/WHAT_IS_MISSING.md#16-row-6-the-atoms-loop-opening-and-balmers-ratio)) |
| 7a | not predicted (the owner's placement, record 1204) | the escaped content 4 of 3677 = 0.109 percent (DETECTOR, the border's `bond` clicks) | 0.1185 percent | the give per nucleon a declared input read back (record 106); the escaped 4 of 3677 (DETECTOR) brackets nature's 4.35 between the whole gives 4 and 5 [the missing piece a rule that derives the binding]. Before the fold: agrees (a bound met), a bound on the declared give |
| 7b | disagrees | the ratio 2.0 (DETECTOR: four border clicks against two, the escaped 8 against 4) | 12.72 | 2.0 against 12.72, a factor 6.4 |
| 8a | disagrees | the width 0 in each neutron's own clock (DETECTOR, the 64 clicks of content 3); the width over the median in the lattice's clock 0.036 (0.08 to 0.13 at head) GAMEBOARD, a diagnostic beside it, in no verdict (record 1196); the reading NOT MADE: the laboratory clock's counterpart, the shell detector's own count under `clock_stamp` (the shell's 4170 fixed bodies one beam reading set, their click lines carrying `clock`), its expectation the tick's width within 2^-20 at [1, 2^20], about 0.08 to 0.13; disagrees under either number ([DISAGREES.md](designs/fail_rows/DISAGREES.md) (PR #1002, merged at 0d0865f7) section 5) | ln 9 / ln 2 = 3.17 | 0 against 3.17, a step where nature has an exponential (the missing rule a decay fired by a met row of a declared bath, WHAT_IS_MISSING.md 1.8, none of the three pieces); the width in the lattice's clock 0.036 GAMEBOARD, the crowd's spread, a diagnostic |
| 8b | disagrees | 16 of 1024 at the first reader and 0 behind it (DETECTOR, series J2) | about 1 | 16 and 0 behind against about 1: a filter set by the window's residue, not an attenuation by depth |
| 8c | not predicted | the `nu` family's content 0, every click of `nu` carrying it (DETECTOR, series J2's 16 first clicks; the content an input of the family table) | at least 9.8 x 10^-8 of the electron's, a bound from the oscillations' squared mass differences and not one measurement | a declared content; the oscillation, a family turning into another in flight, not modelled [kind (2): nature's number a bound] |
| 9 | agrees | 128 / 256 at 45 degrees, 0 / 256 crossed, 64 / 256 with the third between; 219 / 256 at 22.5 degrees (DETECTOR) | 1 / 2, 0, 1 / 4; cos^2 22.5 degrees = 0.85355 | exact at 45 and 90 degrees against nature's fractions; +0.0019 the tables' rounding at 22.5 |
| R3 (Malus at three new settings; docs/designs/new_rows/RUNS.md section 3, on main at 688a93d3) | agrees, outside the count (a re-reading of row 9's identity) | 246, 199 and 177 of 256 (DETECTOR the cells; CONVERSION the fractions) | cos^2 x 256 = 246.26, 199.11 and 176.98 at 11.25, 28.125 and 33.75 degrees | agrees, with the number: 246, 199 and 177 of 256 against cos^2 x 256 = 246.26, 199.11 and 176.98 at 11.25, 28.125 and 33.75 degrees, the tolerance the tables' grain 1/256; a re-reading of row 9's identity at three new settings, outside the referee's count of independent predictions (the reviewer's line on PR #996) |
| 10 | NOT YET | the last registered 1.08 (the product 4.99 / 4.619 of the crowd form, history); the record form's `w27_beam` did not complete | 0.886 | keeps its word |
| 11a | not predicted | q_eff = +1 (COMPUTATION, the pin of `far_lamp_map.out` section 2; the run not made; COMPUTATION, the law's own number by its pin, no run (R3, the kind audit's rule, record 1196)) | -0.53 | no term of the crowd's history (the click's energy does not follow the row's rate) [kinds (1) and (3): the crowd's history; no click definition of a brightness yet] |
| 11b | PASS by a pin | b = 1 (COMPUTATION, the pin: 400 rows over 1452 intervals at 300 Links, the factor 3.639 against 3.629; COMPUTATION, the law's own number by its pin, no run (R3, the kind audit's rule, record 1196)) | 0.97 +- 0.10 | its run needs expansion-v1; keeps its word |
| 11c | not predicted | n = 1 (COMPUTATION, the pin of `far_lamp_map.out` section 4 (b); COMPUTATION, the law's own number by its pin, no run (R3, the kind audit's rule, record 1196)) | 4 (2.3 to 3.1 before correction), an exponent fitted to the sources and not one measurement | no term of the crowd's history; a ruler that grows with the redshift is no verb on the state [kinds (1) and (2): the crowd's history; Tolman's exponent a fitted parameter] |
| 12 | HISTORY | the ratio 1.907 under the age word and 1.000 under the presence word (DETECTOR: the `1 + z` of the lamp's light at x = 110); the ratio of two records' rates over the same intervals, the tick cancelling (DETECTOR; record 1196) | 2.00 | keeps its word (records 394 and 941) |
| 13 | disagrees (the row's cell above: disagrees on the law's own number, NOT COMPARED for the ratio) | the law's own number on a coupled world: the centroid shift -1.993 pixel and the delay +2.95 intervals at gamma_PPN 0 (DETECTOR, `optical/mass_g0` against `control_g0` at head, the pin -1.93 +- 0.5 met, equal to `run_2026_09_22_bresenham`'s to the last digit), half of the declared gamma 1 world's -3.989; series K's 0.000 pixel beside it as the suspension 0 worlds' reading (`lensing/mass`, `heavy`, `near` declare `suspension` 0 and no optical key), history since PR #855 (5b855791); the ring's mean radial shift 0.731 at the declared gamma_PPN = 1 (DETECTOR) and the pin worlds' ratio 2.00 (DETECTOR), an input of kind 2 read back | 1.75 arcsec at the Sun's limb, 1 + gamma = 2 | a factor 2 against nature's 1 + gamma = 2 under the register's own conversion (COMPUTATION on two DETECTOR shifts through the declared weight rule (1 + gamma) content x e_D, the 1 the time part; record 1216); NOT COMPARED for the ratio stands where it stands (the row's cell above); the ring's shift 0.731 and the ratio 2.00 read the declared gamma_PPN = 1 back (DETECTOR readings of a declared input, the third structure line); "the law as built 0.000 pixel (series K)" was the printed number until 2026-09-23, an n = 0 world's (the auditor's finding, confirmed by the reviewer's re-run, [DISAGREES.md](designs/fail_rows/DISAGREES.md) (PR #1002, merged at 0d0865f7) sections 7 and 9) ([WHAT_IS_MISSING.md section 1.12](designs/fail_rows/WHAT_IS_MISSING.md#112-row-13-the-bending-of-light)) |
| 14 | NOT YET READ against nature (RUN_14, 2026-09-23): the click algebra's rung confirmed by the control (979 then 980, DETECTOR); the conditional pins, the law's shell-mean form on an input no click read, FAIL on this fan by the comb (2.5 to 4 times, DETECTOR against a conditional pin); nature's period not compared; the paper's row FAIL (Table 2) by the D3 periods | not a row of this table ([WHAT_IS_MISSING.md section 1.13](designs/fail_rows/WHAT_IS_MISSING.md#113-row-14-newtons-periods)): T(24) / T(12) = 1.677 under the one constant and 1.512 under the line drive (COMPUTATION from two means of unclosed loops; the clicks DETECTOR, the escapes at 1208 and 2452) | the pin 2.00 +- 0.18 (nature's 2^(3/2) not compared) | 1.677 and 1.512 against 2.00 +- 0.18, a COMPUTATION on the host's tick of unclosed loops (WHAT_IS_MISSING.md 1.13: the reading missing, the moving detector's arrival click of RUN_14; a period is not yet a click) |

### The tally by status as written on 2026-09-23 before the fold of records 1190, 1196 and 1204 (history, nothing deleted)

Of the 11 observables the law as built predicts (12 once RUN_14 is read),
5 agree within tolerance (1a, 2b, 9; the bounds 5a and 7a as bounds met),
6 disagree (rows 1c, 6, 7b, 8a, 8b, 13; 14 after its read), and 8 are not
predicted by construction (rows 2a, 3, 4a, 4b, 5b, 8c, 11a, 11c), each
needing one of three pieces: a moving
thing's rate and contraction (4a, 4b, 5b), a term of the crowd's history
(3, 11a, 11c), a declared input made a reading (2a, 8c).

| Row | Status | The law's own number by a click, its kind | Nature | The tolerance met, the number missed, or the missing piece |
| --- | --- | --- | --- | --- |
| 1a | agrees | S = 2.75 (DETECTOR: the record's one gather over 64 births, the cells 27, 5, 5, 27) | 2.42 +- 0.20 | matches nature within 1.65 standard errors; 0.078 below the quantum bound |
| 1b | a control (marked 2026-09-23) | S = 2 exactly (DETECTOR: the counters' clicks of the window form) | 2.42 +- 0.20 | a theorem of every local read-out, not counted; the law's row is 1a |
| 1c | disagrees | not a row of this table ([WHAT_IS_MISSING.md section 1.2](designs/fail_rows/WHAT_IS_MISSING.md#12-row-1c-the-order-channel)): 15 / 16 under a = 0 and -1 / 16 under the cycle, the second party's serial correlation at lag 1 (DETECTOR, met 16 of 16 against the algebra) | 0 | 15 / 16 against 0; the wheel a counter, the order deterministic |
| 2a | not predicted | the visibility 0.966 in the clicks of `slits_huygens` (DETECTOR; the pin 0.9659 COMPUTATION, met bit for bit) | 0.98 (a Mach-Zehnder source; the two-slit figure unverified) | a declared fan width P (an input of the third structure line; kind 2 in the inputs table of record 817); NOT COMPARED until the two-slit figure is verified [kind (2): the 0.98 a Mach-Zehnder's figure, not one measurement of the two-slit visibility] |
| 2b | agrees | the clicks 64 / 0 over 64 births, the visibility 1.000 (DETECTOR; the offers 0.9988 GAMEBOARD, a diagnostic) | 98 percent | matches nature above the measured 0.98 |
| 2c | NOT COMPARED | the power window [1.917, 2.012) (COMPUTATION from the click cells 63 / 1 and 27, 5, 5, 27, DETECTOR) | kappa = 0.0064 +- 0.0119 | kappa not computed; keeps its word |
| 3 | not predicted | q = -0.108 (DETECTOR: the pointer's z per tick of an open-face detector, the tick GAMEBOARD); the law's own crowd q = +0.922 (DETECTOR, the record form) | -0.53 +- 0.01, a fitted parameter of the cosmological model, not one measurement | no term of the crowd's history; the sign the law's own crowd gives is the wrong one (a deceleration) [kinds (1) and (2): the crowd's history missing; nature's q_0 a fitted parameter] |
| 4a | not predicted | the muon's `become` at the count 64 at every speed, the ratio 1 (GAMEBOARD, a body's own record; the products' face clicks DETECTOR); beside it, under `covariant_readings`, the products' clicks at 369 and 345 (DETECTOR), gamma 1.1074 and 1.9558 by the declared identity | 29.33 | no moving-clock rate (r = 1); the identity a declared hypothesis, not the law's [kind (1): a moving thing's clock rate] |
| 4b | not predicted | z = 0.2636 at beta = 0.2674 (DETECTOR; the tick GAMEBOARD); beside it, under the key, 0.3674 (DETECTOR) for the pin 0.369 +- 0.003 | 0.315 | no moving-clock rate (the factor gamma = 1.0378 absent); the identity a declared hypothesis [kind (1): a moving thing's clock rate; a moving detector's count] |
| 5a | agrees (a bound met) | the pace by direction 0.5774 to 0.5818 (COMPUTATION, the flight table); series Q's 290 of 290 face clicks at the derived tick, Node and face (DETECTOR) | delta c / c below 10^-17 | a bound on Q (Q >= 2^56 for 10^-17 at the register's fan), met as a bound |
| 5b | not predicted | the round trips gamma^2 along and gamma across, 1.375 and 1.140 at beta = 0.4297 (COMPUTATION on the flight table; the pair in motion not run) | the null, beta^2 / 2 = 5 x 10^-9 at beta = 10^-4 | no contraction; the identity's reading beside it as a declared hypothesis [kind (1): a moving detector's count along and across, a velocity from clicks] |
| 6 | disagrees (the paper's row (Table 2); the register's cell above still reads NOT YET, to be re-read on its own order) | the electron escapes at 3407 intervals (DETECTOR, series H's world, the runs of 2026-09-22); no line read | Balmer's 27 / 20 = 1.35 | the loop opens, no line to compare ([WHAT_IS_MISSING.md section 1.6](designs/fail_rows/WHAT_IS_MISSING.md#16-row-6-the-atoms-loop-opening-and-balmers-ratio)) |
| 7a | agrees (a bound met) | the escaped content 4 of 3677 = 0.109 percent (DETECTOR, the border's `bond` clicks) | 0.1185 percent | a bound on the declared give (nature's 4.35 units between the whole gives 4 and 5), met as a bound |
| 7b | disagrees | the ratio 2.0 (DETECTOR: four border clicks against two, the escaped 8 against 4) | 12.72 | 2.0 against 12.72, a factor 6.4 |
| 8a | disagrees | the width 0 (DETECTOR: 64 clicks of content 3, each at its own clock's count); 0.036 in the lattice's clock (GAMEBOARD) | ln 9 / ln 2 = 3.17 | 0 against 3.17, a step where nature has an exponential (the missing rule a decay fired by a met row of a declared bath, WHAT_IS_MISSING.md 1.8, none of the three pieces); the width in the lattice's clock 0.036 GAMEBOARD, the crowd's spread, a diagnostic |
| 8b | disagrees | 16 of 1024 at the first reader and 0 behind it (DETECTOR, series J2) | about 1 | 16 and 0 behind against about 1: a filter set by the window's residue, not an attenuation by depth |
| 8c | not predicted | the `nu` family's content 0, every click of `nu` carrying it (DETECTOR, series J2's 16 first clicks; the content an input of the family table) | at least 9.8 x 10^-8 of the electron's, a bound from the oscillations' squared mass differences and not one measurement | a declared content; the oscillation, a family turning into another in flight, not modelled [kind (2): nature's number a bound] |
| 9 | agrees | 128 / 256 at 45 degrees, 0 / 256 crossed, 64 / 256 with the third between; 219 / 256 at 22.5 degrees (DETECTOR) | 1 / 2, 0, 1 / 4; cos^2 22.5 degrees = 0.85355 | matches nature exactly at 45 and 90 degrees; +0.0019 the tables' rounding at 22.5 |
| 10 | NOT YET | the last registered 1.08 (the product 4.99 / 4.619 of the crowd form, history); the record form's `w27_beam` did not complete | 0.886 | keeps its word |
| 11a | not predicted | q_eff = +1 (COMPUTATION, the pin of `far_lamp_map.out` section 2; the run not made) | -0.53 | no term of the crowd's history (the click's energy does not follow the row's rate) [kinds (1) and (3): the crowd's history; no click definition of a brightness yet] |
| 11b | PASS by a pin | b = 1 (COMPUTATION, the pin: 400 rows over 1452 intervals at 300 Links, the factor 3.639 against 3.629) | 0.97 +- 0.10 | its run needs expansion-v1; keeps its word |
| 11c | not predicted | n = 1 (COMPUTATION, the pin of `far_lamp_map.out` section 4 (b)) | 4 (2.3 to 3.1 before correction), an exponent fitted to the sources and not one measurement | no term of the crowd's history; a ruler that grows with the redshift is no verb on the state [kinds (1) and (2): the crowd's history; Tolman's exponent a fitted parameter] |
| 12 | HISTORY | the ratio 1.907 under the age word and 1.000 under the presence word (DETECTOR: the `1 + z` of the lamp's light at x = 110; the tick GAMEBOARD as the time base) | 2.00 | keeps its word (records 394 and 941) |
| 13 | disagrees (the paper's row (Table 2); the register's cell above still reads NOT COMPARED, to be re-read on its own order) | the law as built 0.000 pixel (DETECTOR, series K); beside it, at the declared gamma_PPN = 1, the ring's mean radial shift 0.731 (DETECTOR) and the pin worlds' ratio 2.00 (DETECTOR), an input of kind 2 read back | 1.75 arcsec at the Sun's limb, 1 + gamma = 2 | 0.000 against the bending; the ring's shift 0.731 and the ratio 2.00 beside it read the declared gamma_PPN = 1 back (DETECTOR readings of a declared input, the third structure line) ([WHAT_IS_MISSING.md section 1.12](designs/fail_rows/WHAT_IS_MISSING.md#112-row-13-the-bending-of-light)) |
| 14 | NOT YET READ against nature (RUN_14, 2026-09-23): the click algebra's rung confirmed by the control (979 then 980, DETECTOR); the conditional pins, the law's shell-mean form on an input no click read, FAIL on this fan by the comb (2.5 to 4 times, DETECTOR against a conditional pin); nature's period not compared; the paper's row FAIL (Table 2) by the D3 periods | not a row of this table ([WHAT_IS_MISSING.md section 1.13](designs/fail_rows/WHAT_IS_MISSING.md#113-row-14-newtons-periods)): T(24) / T(12) = 1.677 under the one constant and 1.512 under the line drive (COMPUTATION from two means of unclosed loops; the clicks DETECTOR, the escapes at 1208 and 2452) | the pin 2.00 +- 0.18 (nature's 2^(3/2) not compared) | 1.677 and 1.512 against 2.00 +- 0.18, a COMPUTATION on the host's tick of unclosed loops (WHAT_IS_MISSING.md 1.13: the reading missing, the moving detector's arrival click of RUN_14; a period is not yet a click) |

The row 13 entry of this block prints series K's 0.000 pixel, an n = 0 world's reading (its worlds declare `suspension` 0); corrected on 2026-09-23 in the live block above, on the reviewer's read of [DISAGREES.md](designs/fail_rows/DISAGREES.md) (PR #1002, merged at 0d0865f7): the law's own number on a coupled world is the time part, -1.993 pixel and +2.95 intervals at gamma_PPN 0 (DETECTOR). The block itself stands verbatim.

### The tally as written on 2026-09-21 (at the base 88d843ef; history, nothing deleted)

Written at the base 88d843ef on 2026-09-21 and not re-dated until
2026-09-23; the text verbatim.

| Verdict | Rows |
| --- | --- |
| PASS | 12 under the age word (the clock's field 1.907 against the potential's 2.00), 1a (Bell, the record's pair, 1.65 standard errors), 2b (the Mach-Zehnder, the clicks 64 / 0 over 64 births, the visibility in the clicks 1.000; the offers' 0.9988 beside it, the apparatus layer's number, a diagnostic), 9 (Malus, 128 / 256, 0 and 64 / 256 exact at 45 and 90 degrees; 219 / 256 and 187 / 256 at 22.5 degrees, the tables' rounding), 11b (the stretch of a far lamp's stream, 1 + z, pinned) |
| FAIL | 12 under the presence word, the law's default (the clock's field flat, 1.000 against 2.00), 1b (the window form, S = 2), 2a (the two-slit visibility 0.966 in the clicks, 0.954 in the weights), 3 (q = -0.108 against -0.53), 4a (the muon, a factor 29.33, pinned), 4b (the moving lamp, 0.052 in z), 5b (the frame, eight to twelve orders, pinned), 7b (the alpha, a factor 6.4), 8a (the decay's step, a factor 88), 8b (the filter, 0 against 1), 8c (the massless neutrino, REFUTED by the oscillations), 11a (the far lamp's brightness, q_eff = +1 against -0.53, pinned), 11c (the surface brightness, one power of 1 + z against four, pinned) |
| BOUND | 5a (Q >= 2^56 for 10^-17, beyond the word at the register's fan), 7a (the give per nucleon: 4 to 5 units of 3677 about nature's 4.35) |
| NOT YET | 6 (Bohr's ratio), 10 (the single opening under the one click); the runs of 4a, 5b and 11 |
| NOT COMPARED | 2c (the power of the click: the window [1.917, 2.012) is an implementation gate, kappa not computed), 13 (the bending of light: the ratio 2.00 reads the declared gamma = 1 back, an input of kind 2) |

What the tally says, in the register's terms: the click's form (Born,
the pair, the power) passes, and Malus's fractions pass exactly at 45 and
90 degrees (9), where the tables carry no rounding; the grain shows at the second digit of a
visibility; every reading that depends on a body's clock in motion fails
by nature's gamma, which is one finding read four ways (4a, 4b, 5b and the
absence of contraction), the open decision of record 230; the strong
binding fails in its ratio and bounds its input; the weak force fails in
its forms (a step, a line, a filter) and its neutrino's mass (8c, refuted); the expansion fails in its sign (3) and, read through a detector, in the brightness of a far lamp (11a, one factor of 1 + z short) and in the surface brightness (11c), while the stretch of the lamp's stream passes (11b). A
FAIL here is a prediction of the law stated so that it fails, as
[PREDICTIONS](PREDICTIONS.md) asks, never a number to move.

## Values marked "to verify against the source"

Grangier, Roger and Aspect 1986 (98 percent); Sinha et al. 2010 (kappa =
0.0064 +- 0.0119); Bailey et al. 1977 (the fractional error 2 x 10^-3 at 95
percent, against the brief's 0.1 percent); Botermann et al. 2014 (2.3 x
10^-9 at beta = 0.338); Herrmann et al. 2009 (10^-17) and Nagel et al. 2015
(9.2 +- 10.7 x 10^-19); the NIST wavelengths at the fifth digit; Gonzalez
et al. 2021 (877.75 +- 0.28 s); Nairz, Arndt and Zeilinger 2002 (the
figure of the paper); Malus 1809 (the citation); Formaggio and Zeller 2012
(the cross-section's order; the attenuation per metre in row 8b is an
order-of-magnitude estimate from it, not a figure of the paper); Blondin
et al. 2008 (the stretch's exponent 0.97 +- 0.10); Lubin and Sandage 2001
(the exponents 2.3 to 3.1 before correction); Bertotti, Iess and Tortora
2003 (gamma - 1 = (2.1 +- 2.3) x 10^-5) and Lambert and Le Poncin-Lafitte
2011 (0.99992 +- 0.00012); Dyson, Eddington and Davidson 1920 (1.98 +-
0.16 in units of 0.87 arcsec). The values not marked
(Hensen 2015's 2.42 +- 0.20, Cirel'son's 2 sqrt 2, Planck 2018's Omega_m,
AME2020's binding energies, Michelson and Morley 1887, the exponential's
ln 9 / ln 2, Balmer's 27 / 20) are known to the precision stated.

## What needs the conversion

The second pass compares dimensional values, which needs the dictionary's
conversion fixed once for the whole register and never per experiment:
one Link in metres, one interval in seconds, one unit of content in
kilograms, the cost h of one phase step in joules, one charge step in
coulombs ([HIGHLIGHTS 5.7](HIGHLIGHTS.md#57-from-the-world-we-see-to-the-vector-world-the-conversions-the-principles-what-is-derived-and-what-is-input-2026-09-21),
the transformation from the GameBoard to the observed values, record 210;
[DERIVATIONS_BEAM](DERIVATIONS_BEAM.md) section 16, in preparation on the
owner's word of record 239, tries every dimensionless number of nature
against the structure, which is where the ratios below come from before
any unit is chosen).

| The constant | Its place on the GameBoard (5.7's dictionary) | What the conversion needs | The dimensionless ratio that comes first (section 16) |
| --- | --- | --- | --- |
| c in metres per second | 1 / sqrt 3 Links per interval, the norm of the flight operator (record 191); a ruler-and-clock reading between two detectors | the Link in metres and the interval in seconds, fixed together by one reading (a unit conversion, record 191) | none: c is the unit's definition; its isotropy (rows 5a, 5b) is the dimensionless test |
| G, Newton's constant | the width S, the push per unit of content per unit of flow (record 189, kind 2); the push a body reads (target 3; series C reads it as a probe's own record at one Node, a detector reading of the push and not of the motion, records 564 and 569; the detector reading of Newton's law awaited) | the unit of content in kilograms and the Link and interval above | the gravitational coupling of two bodies of one content against their electric one at the same distance: the register's `Q^2 - G^2 - M^2` at the nucleus (series I, the threshold G = 7111) against nature's 10^36 between two protons |
| h, Planck's constant | the cost h of one phase step, E = h f (the family's `quantum`); the click's amount | the interval in seconds and the unit of content in joules | the fine-structure constant alpha = 1 / 137.036, the charge's square over h c, which section 16 must form from the register's charge per unit of content (4 on the proton, 15 on Bohr's electron), the cost h and c before any unit is chosen |
| e, the elementary charge | a whole number of phase steps per Link, a winding number (PREDICTIONS 26) | the charge step in coulombs, with h above | the same ratio; the neutrality of the atom exact by the family table |
| the masses | the content M, on the non-compact scale, free (PREDICTIONS 26); the minimal mass one unit (record 243) | the unit of content in kilograms | the mass ratios: m_p / m_e = 1836.153 against the register's 1836 / 1 (Bohr) or the ladder of the masses design, which found no ratio derived; the smallest unit count reproducing the ratio to the measured precision (record 243) |
| the muon's lifetime, the neutron's lifetime, the deuteron's binding in MeV | the `become` key `at` in turns; the escaped content of the give | the interval in seconds; the unit of content in joules | the ratios of rows 4a, 7a and 8a, which need no unit |

Until the conversion is fixed, every row of this register stands as
written: a dimensionless comparison under the one set, a verdict each,
and nothing moved to meet it.
