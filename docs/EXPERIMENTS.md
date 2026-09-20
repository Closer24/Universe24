# Experiments register

This register lists the research runs of the ray-event model: section A, the
runs in which the model is confronted with a known measurement and can be
falsified; section B, the runs that demonstrate what the manuscript claims;
section C, the order in which they become possible as the features of issue
#169 land; section D, what this register replaces. It is a register, not an
essay: one entry per run, its rule stated before any code.

**What an entry is.** Every entry is a research run under
[Highlights](HIGHLIGHTS.md#55-acceptance-tests-and-open-decisions) 5.5: made
once, on a stated date, at one runtime source fingerprint (the SHA-256 of the
package files that every run records), with its expectation written before
the run and its result recorded with that fingerprint in the
[validation log](VALIDATION.md). None of these runs is a test of the test
suite, and no test of the test suite is an experiment: a test pins a contract
of the code, an experiment asks the model a question it may answer either way.
A stated acceptance requirement is not a passing test, and a passing run is
not a law of nature (Highlights 3.21, 5.5).

**Who decides.** The model owner decides which entries exist, in what order
they run, what each one pins, and what an outcome means for the model. A
specialist may propose an entry or a criterion; the register changes only by
the model owner's decision, dated.

**Two kinds of readings (the model owner, 2026-09-20: "in reality there is
no such thing").** Every number an entry registers is labelled one of two:
a **detector reading**, the record of a detector's set or of a measured event
in the world (a probe's `read`, a click, a pointer, an owed count), which is
the only kind of reading reality has; or a **GameBoard reading**, the host's
view of the deterministic GameBoard (a ray's position, the count or flow at a
Node, a body's steps, the shell means, the books), which exists for us and
not in reality. A comparison with nature (section A) uses detector readings
only; a GameBoard reading describes the mechanism, checks the books or
draws the picture. Where an entry of the past registered a GameBoard reading
as the measurement, it says so from this date, and the detector form is
added when the entry is re-run.

**The rule of every entry.** Before its run, an entry names the features it
needs (numbers 1 to 12 below), the GameBoard, the families, the Detector marks
with their settings, the return mode and the phase width, what is recorded,
and its pass or fail criterion as an exact statement. The families and
couplings it names are entries of the catalog of nature
(`catalog/nature.json`), whose `experiments` section lists per entry the
ids it uses, so that the register and the catalog agree. Nothing is retuned
against the result and no criterion is redefined after a failure
([physics comparison method](../skills/workflow.md#physics-comparison-method)).
A failed confrontation is recorded as the model's stated limit; it does not
reopen an adopted decision and does not authorize a new law.

**Features.** The numbers are the ten features of issue #169, the eleventh
of Highlights 3.26 and the twelfth of Highlights 3.5, in the order they land
(ray-event model): 1 ray state
(done on 2026-09-17, `ray-event-state-v1`); 2 the Node Detector bit (mark,
setting, ticket seed; done on 2026-09-17, `detector-mark-v1`, the
`detectors` key with `position`, `setting` `[n, d]` and `seed`); 3 the
return; 4 the inverse split with `return_mode`
(siblings, straight, annul); 5 layers; 6 the meeting of rays with N-to-M
conversion; 7 the field as the ray's own information in ray form; 7b the
external body, after 7 (Highlights 3.19, `external-body-v1`; named "fixed
body" earlier on 2026-09-17): a Node declared to hold a family with an
amount, if wanted a charge, and an initial momentum (`initial_momentum`,
zero at rest), radiating by the field rule, never spreading, moved by
fields only (an arriving field ray its coupling table names changes its
momentum by the table; its velocity, momentum over amount, is an exact
accumulator that steps one Link per full amount on an axis; the audit
carries the bodies' momentum as its own line) and never pushed by matter,
every arrival met by the declared coupling of its family, absorption into
an explicitly accounted sink by default (a wall, a screen, a beam stop) and
otherwise a mirror, a beam splitter, a phase plate or, after 11, a
polarizer; 8 binding and gravity by
delay; 9 every ray a wave ray with family, charge and `phase_bits`; 10 the
audits; 11 polarization (after the ten); 12 field spreading (Highlights 3.5,
model owner, 2026-09-17): light and the field of a charge one family of the
catalog, and every Node that field content reaches releasing it again in all
six headings by the family's declared split table, the backward heading
included, a quantum never waiting; until it lands the field lives on the six
axis lines of its source and light goes straight, and its cost is measured
before adoption.

**Status values.** `planned` (this page, criterion fixed, not run);
`measured` with date, commit and fingerprint, and the outcome in one word
(pass, fail, or the named alternative); `withdrawn` by the model owner, dated.
Today every entry of sections A and B is `planned`, except A2 under the law of
events, `measured` on 2026-09-19 as the model's limit, and C, the couplings
under the law of events on the plane, `measured` on 2026-09-19 with its
verdict per item; section E holds the dated demonstration runs, which
confront nothing and are `measured` as made.

**Conventions.** The GameBoard is the cubic Node GameBoard of Highlights 3.1 with
its boundary stated per entry; c is one Link per interval; a Detector setting
is the declared ratio n/d of its draw, the `setting` `[n, d]` of the mark
(1 = every arrival passes, 0 = every arrival returned); N is the
number of phase steps of the circle, N = 2^`phase_bits`; the steering table
is the Born rule as a coupling, cos²(δ/2) to sin²(δ/2) in bounded integer
ratios with the remainder owned (Highlights 3.3, 3.17). A statistical
criterion states its count and its standard error; an exactness criterion
states "exactly" and means integer equality at every tick.

## A. Confrontation with physics

### A1. Two-slit intensities against the Born rule

- **Confronts.** Young's two-slit fringes, intensity proportional to
  cos²(δ/2) with δ = 2π ΔL/λ for a path difference ΔL (the Born rule for two
  paths), built one quantum at a time (Tonomura and others, 1989, single
  electrons; Grangier, Roger and Aspect, 1986, single photons, fringe
  visibility 0.98).
- **Model prediction today.** Highlights 3.3: interference is steering; where
  two rays of one emitter meet in one layer the declared coupling reads their
  phase difference and splits the shared content between the two candidate
  Ports in the ratio cos²(δ/2) to sin²(δ/2); two paths of different length
  reach one place at one time only if their rays were emitted at different
  times, so δ is the emitter's rate times the path difference; light's own
  rate is zero; the Detector reads none of this and click intensity is the
  content that arrived. The fringe period is therefore λ = N/r Links for an
  emitter of rate r steps per interval.
- **Features.** 1, 2, 5, 6, 7b, 9, 10, 12.
- **Run.** A slab of 129 × 65 × 3 Nodes, open boundary. One emitter, a bound
  clock of rate r = 32 at N = 2^8 (λ = 8 Links, so that the integer path
  differences of the screen hit the table's exact zero), a marked Node with
  setting 1, emitting one light ray per interval toward two slit Nodes 16
  Links apart;
  each slit a declared catalog coupling that re-emits the arriving light ray
  over the forward headings with its phase unchanged. A screen row 48 Links
  behind the slits: at each screen Node the meeting of the two slit rays is
  steered by the declared table between the Port toward a marked Node behind
  the screen (setting 1, its click the record) and the sideways Port (a
  declared sink: an external body, feature 7b, `external-body-v1`,
  Highlights 3.19, at its default coupling, absorption into an explicitly
  accounted sink). No returns in the main run; a second run with the screen
  Detectors at setting 1/2 and `return_mode` siblings (features 3 and 4) as
  the control that returns change the normalization only. Recorded: per
  screen column, the content that clicked over 2^12 intervals; the path
  difference ΔL of that column in intervals on the declared pace; the audit
  totals per tick.
- **Criterion.** Pass: for every screen column the clicked content equals the
  content that arrived times the table entry for δ = r ΔL mod N, exactly,
  with the remainder owned; the columns of the maxima and minima of the
  clicked content are those of cos²(π ΔL/λ) with λ = N/r within one Node;
  the visibility (max − min)/(max + min) is at least 1 − 4/N; the control
  run's normalized pattern equals the main run's within its binomial error
  (2^12 draws per column at 1/2, error 1/64 of the column's content). Fail:
  any column off the table, a maximum or minimum displaced by more than one
  Node, visibility below 1 − 4/N, or content in unequal to content out at
  any tick.
- **Status.** planned; waits for feature 12, field spreading (Highlights
  3.5, 2026-09-17): light is the field and spreads by the split table of its
  family, so a slit is a gap in a wall that absorbs and the fringes are
  where a whole quantum, which never waits, is realized by the Detector;
  until it lands light goes straight and the slit coupling re-emits. What a
  field quantum returned with 0 does once the field spreads is an open
  decision of the model owner before this run (Highlights 5.5, 2026-09-17);
  until it is decided feature 12 implements the proposal, a walk back on the
  line of arrival with no inverse split, and says so. The sub-quantum
  remainder of a spread is owned by the Node per family and heading and
  leaves whole when it reaches one quantum (Highlights 3.5, decided
  2026-09-17 over the phase-selected heading; feature 12b), so the fringes
  are where whole quanta are realized after the Node's remainders have grown
  to one.

- **A1 repeated under the law of the bit (2026-09-18).**
  - **Claim.** The model owner's instruction of 2026-09-18: A1 repeated on
    the engine as it is on `origin/main` at `ffa4a56` (features 15 to 18 and
    16d part 1 merged) under the law of the bit (Highlights 5.4): one source
    of things, a lamp of the light family with a clock, behind a wall with
    two slits of separation d, a screen of marks at L; the lamp's shadow set
    given with the GameBoard (`initial_field`), N = 64, one K for the world,
    `wait_per_quantum` 1, the dense mode, no `spread`, `steering`,
    `mass_field` or `seed`; recorded the counts per mark over enough
    emissions to see a pattern, the pushed amount at the screen's Nodes for
    the source's shadow set, the fringe spacing measured against
    lambda_w L / d with lambda_w = K / (sqrt(3) M) (DERIVATIONS.md 27 (v),
    where K is the content per turn, N times the engine's K per step) and
    the depth; then one slit closed as the control. What is confronted: the
    law says a thing has one path and is steered by the pushes of the
    shadows (points 10, 15, 3: a thing meeting its own shadow is home, no
    push); the derivation (section 29) says the fringes are in the push, of
    the optical spacing lambda_w L / d at full depth for equal slits, and
    none in the counts of things, since marks count things and a thing
    shows no self-interference; section 30 says the wave needs about 256
    quanta per Node.
  - **Features.** 15 (`bit-law-v1`), 16b (`clock-readings-v1`), 16c
    (`node-mixing-v1`), 16d part 1 (`return-field-v1`), 17
    (`node-is-ports-v1`), 18 (`lanes-v1`), on 1, 2, 2c, 5, 9, 10.
  - **Run.** `examples/nature/a1_law/` (`make_worlds.py`), the law's form
    throughout. GameBoard 45 x 65 x 17, open. The lamp: a type holding `light`
    2^22 and the world's momentum at (4, 32, 8), emitting one light thing of
    amount 4 along +X every interval at `kerengonen_phase` 0, paid from its
    stock; `light` declares `clock` true and the world K = 1, so a thing of
    amount 4 advances 4 steps of 64 per interval, the derivation's period
    16: lambda_w = 64 x 1 / (sqrt(3) x 4) = 9.24 Links. The wall: the plane
    x = 16 of marks at setting [1, 1] but the two slit columns y = 24 and
    y = 40, all z (d = 16); a mark absorbs a thing into its counter and
    returns a shadow, which is what a wall does under the law, is silent in
    the record and reflects in the prefill as in the run (an external body's
    Node publishes a record every interval a shadow reaches it, and the
    prefill drops what reaches a body's Node, `prefill.py`, `_fill`). The
    screen: the row x = 40 (L = 24), y = 1 to 63, z = 8, marks at [1, 1].
    The optical spacing lambda_w L / d = 13.9 Links. The lamp's shadow set:
    `initial_field` `{"light": {"fill": 8}}` with `release` [1, 1], 2^22
    quanta per heading per interval of the fill; 8 is the longest fill the
    prefill admits for one lamp (from 16 it refuses "a third phase on one
    Port of a source", `prefill.py`, `_depart`, read before the runs), so
    the set is a shell of eight intervals of release that leaves the lamp at
    the first tick, 201,077,599 quanta of shadows at the start beside the
    lamp's 4,194,304 of things, and not a standing set; the prefill releases
    at phase 0 (`release_stock`: a record has no phase of its own) and a
    shadow that comes home is re-released with its own phase
    (`rerelease_shadow`), so the clock enters none of the shadows. The
    series (the model owner's decisions of 2026-09-18, Highlights 5.4: the
    GameBoard of a run is closed, PR #311, and only closed worlds are tested, PR
    #314, so a series carries no open-GameBoard control): one pair on the
    closed GameBoard, `two_slits_periodic` and its control `one_slit_periodic`
    with the column y = 16 closed, the lamp of stock 2^26 on a periodic
    GameBoard 45 x 49 x 9, the lamp at (4, 24, 4), the slits at y = 16 and 32,
    the screen row x = 40 over every y at z = 4, and a second wall of marks
    at x = 44 closing the wrap in x, without which the shell leaving the
    lamp toward -X would reach the screen from behind; the wrap in z makes
    the slit columns infinite and the wrap in y puts images of the lamp 49
    Links apart; 200 ticks each, run once through `tools/run_series.py
    --jobs 2`, the dense mode on, 282 s each, peak 0.71 GB. Measured first,
    earlier the same day and before the decisions, on the open GameBoard (the
    geometry above; recorded below, not in the series, the worlds no longer
    shipped): `two_slits` and `one_slit` with the column y = 24 closed (the
    stock 2^22; 566 s and 553 s, peak 1.66 GB each) and `two_slits_big` and
    `one_slit_big` (the stock 2^26, a shell sixteen times larger, declared
    after the first pair's records showed the shell below one whole quantum
    per Node before the screen; 828 s and 806 s, peak 1.65 GB). The
    screen's marks replayed by `record_screen.py` (a Recorder: a mark that only
    returns shadows publishes no record, so the shadows returned and the
    push J = the sum of amount x arrival heading at each mark's Node are
    read from the mark's resident rays after every tick of a replay checked
    against the run's events and fingerprint), and read by `analyze.py`
    (`record.json`). Recorded per world: `run.json`, `events.jsonl`,
    `screen.json`; the ray viewer's GIF of `two_slits` from the runner's
    record (no sidecar: a per-tick snapshot of this GameBoard is too large).
  - **Result, measured first on the open GameBoard (recorded, not in the
    series).** The first pair (`two_slits` 566 s, `one_slit` 553 s, peak
    1.66 GB each): 200 emissions of amount 4, 189 clicks at the wall's mark
    on the axis (16, 32, 8) from tick 12 (756 quanta absorbed, the marks'
    momentum (756, 0, 0)), 11 photons in flight at the end, and 0 clicks at
    the screen in both worlds; the lamp's things are its own, so its shadows
    are home to them and push nothing, and every photon walks its one path
    to the wall. The shell: 201,077,599 quanta of shadows at the start,
    197,714,530 escaped and 3,363,069 in the region at tick 200 (the open
    faces at 8 Links in z and 32 in y take it); behind the slits the peak
    amount per tick at a Node is 2,220 at (17, 24, 8) and (17, 40, 8) at tick
    20 and 431 at (18, 24, 8) and (18, 40, 8), so the instruction's 256
    quanta of an owner are held there while the shell passes; in the region
    beyond the wall at most 158,325 quanta at tick 32 (79,170 in the control),
    64,255 at the end; at (28, 32, 8) at most 39 per tick (tick 55), at
    (39, 32, 8) never one whole quantum; the wall returned 39,208,669 quanta
    over the run (peak 1,746,459 per tick at tick 31). The screen: not one
    whole quantum reached any of its 63 marks in 200 ticks in either world
    (n = 0 and J = (0, 0, 0) at every mark at every tick; no phase read), so
    the shell of 2^22 per heading is below one quantum per Node at L = 24
    behind the wall: the push at the screen 0, no fringe to read. The
    ledger at tick 200, both worlds: light real 4,194,304 initial, 4,193,548
    current, 756 absorbed by marks; shadow 201,077,599 initial, 3,363,069
    (3,325,222 in the control) current, the rest escaped, 0 absorbed at
    home; momentum (-756, 0, 0) current against (756, 0, 0) on the marks'
    line; every line balanced, `conserved_at_every_completed_tick` and
    `real_conserved` true.
  - **Result, the open GameBoard's second pair (recorded, not in the
    series).** `two_slits_big` (828 s)
    and `one_slit_big` (806 s), peak 1.65 GB: 3,217,240,686 quanta of
    shadows at the start beside the lamp's 67,108,864 of things; 189 clicks
    at the wall's mark on the axis from tick 12, 0 at the screen, 11
    photons in flight at the end, in both; the shell 45,413,458 (45,572,692
    in the control) in the region at tick 200, the rest escaped; every
    ledger line balanced, conserved at every completed tick. The screen
    (`record_screen.py`, `record.json`): the marks returned 218,618 quanta
    of shadows over the run with two slits and 91,601 with one, at phases 0
    and 32 of 64 only (127,947 and 90,671 quanta), owner 1; behind the
    slits the peak per tick 35,957 at (17, 24, 8) and (17, 40, 8) at tick 19,
    6,665 at x = 18, 1,056 at (28, 32, 8), 1,238 at (39, 32, 8) at tick 71
    (the 256 quanta of DERIVATIONS.md section 30 held while the shell
    passes); in the region beyond the wall at most 2,631,328 quanta at tick
    32. The returned amount summed over the run along the screen, two
    slits: maxima at y = 3, 12, 19, 21, 32, 43, 45 (6,241 at the axis),
    minima at y = 11, 13, 20, 26, 37, 44, 52 (974 at y = 37), the depth
    between the axis and its nearest minimum 0.73; the push J_x summed over
    the run: maxima at y = 3, 10, 12, 16, 19, 22, 32, 41, 43, 46, 54 (1,560
    at the axis), minima at 9, 11, 13, 17, 20, 28, 37, 42, 44, 51, 55 (224
    at y = 28, 30 at y = 37), the depth 0.75, the mean spacing of the
    maxima 5.1 Links against the optical 13.9. The control with one slit:
    the returned amount 2,384 at y = 19 (behind the open slit at 40 read
    through the mirror) and a nearly flat run elsewhere (depth 0.02 at the
    axis), the push flat (depth 0.11). Against the incoherent sum of the
    one-slit profile and its mirror image, the two-slit profile's cross
    term runs from -1,837 to 3,847 with
    10 sign changes along y (the push's from
    -549 to 1,116, 12
    sign changes); the totals 218,618 against 183,202.
    A first reading, to be completed on the closed GameBoard: the two-slit
    profile is modulated at full depth about the axis where the one-slit
    profile is flat, but at a spacing of 5 to 11 Links of a phase-0 shell
    (a broadband pulse, phases 0 and 32 only), not the optical 13.9 of a
    wave of lambda_w 9.24; the run holds no wave of that wavelength.
  - **Result, the series: the closed GameBoard (2026-09-18).**
    `two_slits_periodic` (282 s) and `one_slit_periodic` (282 s), peak
    0.71 GB, on the periodic GameBoard 45 x 49 x 9: 3,221,225,472 quanta of
    shadows at the start beside the lamp's 67,108,864 of things, nothing
    escaped (0 on every line at every tick), the shadow line 3,221,225,472
    at tick 200 in both worlds; 189 clicks at the wall's mark on the axis
    (16, 24, 4) from tick 12, 0 at the screen, 11 photons in flight at the
    end, in both; every ledger line balanced, conserved at every completed
    tick, `real_conserved` true. The screen (`record_screen.py`,
    `record.json`), 49 marks at x = 40, z = 4, first reached at tick 59
    (y = 11 to 21 and 27 to 37 with two slits, 27 to 37 with one): the
    marks returned 9,462,464 quanta of shadows over the run with two slits
    and 4,329,862 with one, at phases 0 and 32 of 64 only (6,455,849 and
    3,006,615 with two slits), owner 1; the two walls (the slit wall and
    the back wall at x = 44) returned 10,520,459,195 quanta over the run
    (10,000,662,586 in the control), peaking at 142,847,145 per tick;
    behind the slits the peak per tick 257,258 at (17, 16, 4) and 259,887
    at (17, 32, 4) at tick 169, 104,251 and 103,567 at x = 18 (tick 158),
    22,847 at (28, 24, 4), 35,155 at (39, 24, 4) at tick 158 and 13,748 at
    (43, 24, 4) before the back wall (in the control 307,156 at (17, 32, 4)
    at tick 128 behind the open slit, 31,809 behind the closed one and
    7,287 at (39, 24, 4)); in the region beyond the wall 38,897,522 quanta
    at tick 195 and 38,472,586 at the end (20,574,235 and 20,405,905 in the
    control): on the closed GameBoard the field behind the wall grows through
    the run and does not pass, the shell coming around and back off the
    walls. The returned amount summed over the run along the screen, two
    slits: maxima at y = 8, 12, 24, 36, 40 (319,615 at the axis, 254,709
    and 253,338 at y = 12 and 36), minima at y = 2, 9, 18, 30, 39, 46
    (73,939 at y = 18, 75,208 at y = 30), the depth between the axis and
    its nearest minimum 0.62, the three maxima about the axis 12 Links
    apart against the optical 13.9 (the analyzer's mean over all five
    maxima, 8.0); the push J_x summed over the run: maxima at y = 5, 8, 13,
    16, 20, 24, 27, 32, 35, 40, 43 (48,273 at the axis, 64,063 at y = 40),
    minima at 2, 6, 11, 15, 18, 22, 25, 30, 33, 38, 42, 46 (19,742 at
    y = 18), the depth 0.19 at the axis, the mean spacing of the maxima 3.8
    Links. The control with one slit (the column y = 16 closed): the
    returned amount 77,497 at the axis against 64,510 at y = 23, the depth
    0.09; its largest values on the far side of the axis, 133,557 at y = 7
    with maxima at y = 2, 7, 12 five Links apart (reached from the open
    slit at y = 32 through the wrap in y); the push at depth 0.25 at the
    axis (13,665 against 8,186 at y = 23), its maxima 4.7 Links apart on
    the mean. Against the incoherent sum of the one-slit profile and its
    mirror image, the two-slit profile's cross term runs from -76,263 to
    164,621 with 8 sign changes along y (the push's from -26,144 to 25,896,
    12 sign changes); the totals 9,462,464 against 8,659,724.
  - **Reading.** What the engine gave. The counts of things: no fringes
    and no pattern at all in any of the six worlds: no thing reached the
    screen, every photon walking its one path to the wall's mark on the
    axis, since a thing is steered only by the pushes of shadows of another
    owner and the lamp's shadows are home to its own photons (points 3 and
    10 as the engine reads them: the emitted thing carries the lamp's
    `thing` id, `spatial_plan.py`). The push, on the closed GameBoard (the run
    the model owner's decision asks for, nothing escaping): the amount the
    screen returns and the push at its Nodes are modulated about the axis
    where the one-slit control is nearly flat (depth 0.62 against 0.09 in
    the returned amount), the maxima nearest the axis 12 Links apart, near
    the optical 13.9 of a wave of lambda_w = 9.24, but the push's own
    maxima 3.8 Links apart and everything that arrived at phases 0 and 32
    only: the run holds a phase-0 shell circulating on the closed GameBoard and
    reflected by its walls, not the monochromatic wave of DERIVATIONS.md
    section 29, and a spacing near the optical one out of a broadband
    shell is a reading to be repeated with a wave in the shadows before it
    is called a fringe. On the open GameBoard: with the shell of 2^22 per
    heading not one whole quantum reached the screen at L = 24 (the open
    faces took 97 % of the shell); with 2^26, modulation at depth 0.73 at
    a mean spacing of 5.1 Links, the control flat. The integer rule of
    section 30 (256 quanta per Node) is not what limits the reading on the
    closed GameBoard: behind the slits the amount per Node reaches 2.6 x 10^5
    and the screen's marks return up to 22,107 quanta in a tick. The clock
    declared on the lamp's family enters none of its shadows (the prefill
    at phase 0, the re-release with the shadow's own phase), so the wave of
    DERIVATIONS.md 27 (v) cannot be built on this engine by a fill, and the
    prefill admits at most eight intervals of it. Nothing is registered as
    a law.
  - **Fingerprint.** Source
    `6fef7cc04a71706cfd5dfdb496e20f6318a6bdfd6bf0c36e1379dbdd7934addc`, the
    engine of `origin/main` at `ffa4a56` (the runs were made on it after
    `main` had moved on; the lane did not restart); initialization
    `two_slits`
    `242ba45abda1c205acc06fffc854bfa4fda7a053d1003019a32c4982a4f006e3`,
    `one_slit`
    `17bab17df094f604914fa072415b9bd0885b7273685c87521a1fe391ae67cbcc`,
    `two_slits_big`
    `4a25c852030bb89780e1f31be4be2ed7e65e339e98f2ef4f93f6c2c96e01defb`,
    `one_slit_big`
    `7af8061a22f1c298a99d0f3e19ba993e10cf85497532fb33e1a74da4c9b9197e`,
    `two_slits_periodic`
    `935aee67a98baa8516969a26048e51c034dd3a9ac1feda00eea6a5dfb150616c`,
    `one_slit_periodic`
    `fbda80979d1ef91e691f14e785b09f79ec30a000471798f1a6f3b95310458206`
    (the digests of the runs' `initialization.json`, written with the
    family's `phase_bits` 6 and `ray_slots` 24; the shipped closed-GameBoard
    worlds carry the world's `N` and no ray slot budget since the cleanup
    of 2026-09-18, parts 1 and 2, merged after the runs, and are
    `bit_law_migration.migrate` of the runs' worlds, the same worlds in the
    law's one form; the open-GameBoard worlds are no longer shipped);
    `record.json` beside the worlds holds the closed GameBoard's readings; the
    records stay outside the tree.
  - **Status.** measured, 2026-09-18, on the closed GameBoard (only closed
    worlds are tested, the model owner, 2026-09-18); outcome: no fringes
    in counts (no thing reached the screen); the push modulated at depth
    0.62 in the returned amount with the maxima about the axis 12 Links
    apart against the optical 13.9 and the control at 0.09, out of a
    phase-0 shell (no wave of lambda_w in the run). The open GameBoard,
    measured first and recorded: depth 0.73 at 5.1 Links (2^26) and nothing
    at the screen (2^22).

### A2. Bell test in phase form, symmetric geometry

- **Confronts.** The CHSH inequality, S ≤ 2 for every local model (Clauser,
  Horne, Shimony and Holt, 1969), and its violation with spacelike settings in
  the loophole-free experiments of 2015: Delft (Hensen and others, event-ready
  spins over 1.3 km, S = 2.42 ± 0.20), Vienna (Giustina and others) and NIST
  (Shalm and others), photons above the fair-sampling bound; the quantum
  maximum 2√2 = 2.828. In the phase form, Franson's two-photon interference
  (1989) with unbalanced interferometers, where the settings are phases and
  the quantum correlation is cos of the phase sum with visibility 1.
- **Model prediction today.** Highlights 5.4 and
  [hypothesis 11](HYPOTHESES.md#11-the-bell-prediction-of-the-ray-event-model-stated-so-that-it-can-fail),
  line 1: two Detectors at equal distance from the birth draw independently,
  the first Detector's value reaches the other only after the round trip
  through the birth event, so S ≤ 2 for symmetric spacelike settings; the
  passed pairs are a fair sample because the draw reads nothing.
- **Features.** 1, 2, 3, 4, 5, 6, 7b, 9, 10, 12. No polarization (feature 11)
  is needed: the settings are phases.
- **Run.** A GameBoard of 161 × 17 × 17 Nodes, open boundary; the pair source at
  the center, a marked Node with setting 1, emitting one pair per 8 intervals
  as two light rays of one birth event on opposite headings ±x carrying the
  source clock's phase. Each arm at 64 Links: a splitter with two outputs
  (an external body, feature 7b, `external-body-v1`, Highlights 3.19, with
  the beam-splitter coupling, a split by a declared table), a long path
  ΔL = 8 Links longer than the short one, a phase plate on the long path (an
  external body with the phase-plate coupling, a phase offset adding the
  setting to the phase), and a recombiner meeting steered by the table
  between a + Port and a − Port,
  each leading to a marked Detector Node with setting 1/2, `return_mode`
  siblings. Settings at N = 2^8 from a declared per-pair list switched in the
  interval before the ray arrives: Alice 0 and 64, Bob 32 and 96 (0°, 90°,
  45°, 135°), 4096 coincident pairs per setting pair, the singlet sign
  S = |E(a,b) − E(a,b') + E(a',b) + E(a',b')|. A coincidence is a click at
  one of Alice's two Detectors and one of Bob's in the same window of 2ΔL + 1
  intervals around the pair's arrival interval; a pair with a return on
  either side is unpaired and counted. Recorded: per setting pair the four
  click counts, E, the unpaired count; per Detector its click rate; S with
  its binomial standard error σ_S (about 0.03 at 4096 pairs per correlation);
  a control with `return_mode` straight; the audits.
- **Criterion.** Pass against physics requires S > 2 + 3σ_S. The model
  predicts S ≤ 2: a value at or below 2 + 3σ_S is a fail of the model
  against the 2015 data and is recorded as the model's stated limit
  (hypothesis 11, outcome 1); a value above 2 + 3σ_S in this geometry
  contradicts hypothesis 11 line 1 and stops the register's Bell entries
  until the mechanism is understood. In either case each Detector's click
  rate must equal its setting 1/2 within 3 binomial standard errors and move
  with the other side's setting by less than 3 standard errors
  (no-signalling; a larger shift is a fail whatever S is), and every pair
  with a return must be counted unpaired, not dropped.
- **Restated under the law of the bit (model owner, 2026-09-18; Highlights
  5.4, points 6, 10, 14 and "The price").** The pair is two things of one
  birth event, each carrying the source clock's phase; things move whole on
  their lines, so the arms need no spreading family and the wait on feature
  12 above is void. There is no draw: a mark meets a 0 or a 1, and what it
  meets was decided at birth and along the one path; a mark that misses a
  thing (its declared table, one arrival in d) returns it on its own steps to
  the birth event, where the inverse split sends its value along the
  partner's line at one Link per interval. Each outcome therefore depends
  only on the local setting and the arriving thing, and the pairs counted are
  a fair sample because the table reads nothing of the ray. The prediction
  is S ≤ 2 for spacelike settings, without qualification: the model's
  declared limit. The criterion above stands with "draw" read as "table";
  a value above 2 + 3σ_S in this geometry contradicts the law and stops the
  register's Bell entries until understood. `return_mode` is retired: the
  return is the missed thing walking back its steps. The splitters, phase
  plates and recombiners are things with declared tables (point 22). Waits
  for features 15 to 17.
- **Status.** planned; waits for feature 12, field spreading (Highlights
  3.5, 2026-09-17): the pair's light rays are field content, spreading by
  the split table of their family and combining by phase where they meet,
  and the arms run on that spreading family; until it lands light goes
  straight. Reading of 2026-09-17 (Highlights 5.4): a Detector reads the bit
  a ray carries (feature 2b), a ray carrying 1 passing without a draw and a
  ray carrying 0 never drawn, so the independence of the two draws and the
  fair sample stated above are to be re-derived under that rule by
  hypothesis 11 and A13 before the price is quoted again.

### A2, under the law of events (2026-09-19)

- **Confronts.** As A2: the CHSH inequality, S <= 2 for every local model,
  and its violation with spacelike settings in the loophole-free
  experiments of 2015 (Delft, S = 2.42 +- 0.20; Vienna; NIST; the quantum
  maximum 2 sqrt 2 = 2.828), in the phase form, the settings phases. Made at
  the model owner's request of 2026-09-19 (Highlights 5.4: "Can we do a
  Bell experiment with an emitter and two detectors, Alice and Bob? An
  executing agent does it after the mathematician and the physicist
  approved. A small GameBoard."), after the two reviewers pinned the verdict
  below and the owner said "Yes to both": the run is made and registered
  as the model's limit, never as a confrontation the model could pass.
- **Model prediction, pinned before the run (the physicist and the
  mathematician, Highlights 5.4, "The principles of the law of events").**
  With a deterministic local phase window each click is a function of the
  arriving phase and the local setting alone, so CHSH is at most 2 as an
  identity on the record; the correlation is the triangle
  E(a, b) = 1 - 4 k / N with d = (a - b) mod N and k = min(d, N - d); the
  CHSH settings give S = 2 exactly, the model's limit (outcome 1 of A2
  against the 2015 data), not a fluctuation.
- **Features.** The one engine (`events-v1`, [the engine](ENGINE.md)): a
  lamp of a paid family, detectors of threshold 1 and the phase window
  (`phase_window`, `tests/test_phase_window.py`). Nothing of the ray-event
  list above: no draw, no return, no splitter, no polarization.
- **Run.** `examples/events/bell/` (ten worlds written by `make_worlds.py`,
  the dictionary in the [README](../examples/events/bell/README.md)), one
  base world with the settings the only difference: `"law": "events"`, a
  bar of 21 x 1 x 1, open, K 2^20, N 64 (the phase tables read a single
  arrival's step exactly only up to N = 64), `release` [0, 1],
  `suspension` 0, the families `light` (paid) and `counter` (paid), every
  measured event `fixed`. The lamp of `light` at x = 10, content
  K + 2 = 1048578 (the release of age a stamped with the phase a mod 64
  exactly for every age of the run), `phase` 0, one unit per self-creation
  on +X and on -X, no window (the source cycles the whole circle). Four
  counters of content 1, each its own detector of threshold 1, the table
  `{"light": {"rule": "measure", "phase_window": s}}`: `alice_plus` at
  x = 2 (s = a), `alice_minus` at x = 1 (s = a + 32 mod 64), `bob_plus` at
  x = 18 (s = b), `bob_minus` at x = 19 (s = b + 32 mod 64). The unit
  released on -X reaches x = 2 after 8 Links; outside the window a it
  passes (a `pass` record) and reaches x = 1 at the next interval, where
  the complement takes it: the two windows of a side cover the circle
  exactly, so every unit clicks exactly once per side and nothing escapes.
  A pair is the two releases of one age of the lamp; A = +1 for a click at
  `alice_plus`, -1 at `alice_minus`, B likewise; the age of a click is its
  tick less its Node's offset, read off the record itself (the earliest
  click at a Node is the smallest age its window admits, whose phase is
  that age). 128 pairs analysed, the ages 0..127 (two full circles, so E is
  exact for any multiple of N / 2); `ticks` 138, so that the last minus
  click of age 127 (tick 137) is on the record, the ages 128 and after,
  still in flight, excluded. The settings: the CHSH quadruple
  (a, b) = (0, 8), (0, 24), (16, 8), (16, 24); the controls (0, 0), (0, 32),
  (0, 16); the non-saturating quadruple (0, 12), (4, 8), (4, 12) with
  (0, 8) reused. Static settings, no last-moment choice. Recorded per run:
  `run.json` (`audit`, `conserved_at_every_completed_tick`, `escaped`,
  `measured`, `detectors`) and `events.jsonl` (the `click` and `pass`
  records with their `detector`, `tick` and `phase`), read by
  `tools/bell_chsh.py` (standard library, `fractions.Fraction`, no float
  in a criterion), which prints the table and every criterion and exits
  nonzero on a failure. The commands: `python
  examples/events/bell/make_worlds.py`; for each of the ten worlds `python
  -m event_universe --init examples/events/bell/<name>.json --output
  artifacts/bell/<name>`; `python tools/bell_chsh.py artifacts/bell`.
- **Expected (written before the run).** Per run at 128 pairs,
  E = 1 - 4 k / 64: (0, 8) k 8, E +1/2, same 96 and different 32; (0, 24)
  k 24, -1/2, 32 and 96; (16, 8) k 8, +1/2, 96 and 32; (16, 24) k 8, +1/2,
  96 and 32; S = E(0, 8) - E(0, 24) + E(16, 8) + E(16, 24) = 2 exactly. The
  controls: (0, 0) E +1, 128 and 0; (0, 32) E -1, 0 and 128; (0, 16) E 0,
  64 and 64. The non-saturating quadruple: (0, 12) k 12, E +1/4, 80 and
  48; (4, 8) k 4, +3/4, 112 and 16; (4, 12) k 8, +1/2, 96 and 32;
  S' = E(0, 8) - E(0, 12) + E(4, 8) + E(4, 12) = 1/2 - 1/4 + 3/4 + 1/2
  = 3/2 exactly (the cosine of the phase difference at the same settings
  would give 2.828 and 1.739). Every run: the books balanced at every
  completed tick; `escaped` 0 for both families; each windowed Node clicks
  on exactly 64 of the 128 analysed pairs; exactly one outcome per side
  per age; no `home`, `read`, `rerelease`, `step`, `merged` or `escaped`
  record; the lamp's momentum [0, 0, 0] at the end (its two recoils cancel
  at each self-creation); every click's phase equal to its age mod 64 and
  inside its Node's window (d = (phase - s) mod 64 below 16 or from 48);
  every pass at a plus Node, outside its window, clicking at the minus
  Node next; the offsets plus tick = age + 9, minus tick = age + 10.
  No-signalling, exact: the set of ages at which `alice_plus` clicks
  identical across all runs with the same a whatever b, and Bob's likewise
  for the same b.
- **Criterion.** Every expectation is exact; a deviation is a defect of
  the engine, the width or the bookkeeping, to be reproduced minimally and
  reported, never tuned away. A2's verdict applies: S at or below 2 is
  outcome 1 against the 2015 data, the model's stated limit.
- **Result (2026-09-19, commit `1f9f280` on `main`, source fingerprint
  `53a70962c5f2c8c860a0895dbc9d6cb7cf125d53aa3d5f0ce6aa5464c79a87f9`,
  Python 3.14.0rc2, headless, about 0.12 s per run).** Every count as
  pinned. The four counts (++, +-, -+, --) over the 128 pairs and E:
  (0, 8) 48, 16, 16, 48, E +1/2; (0, 24) 16, 48, 48, 16, E -1/2; (16, 8)
  48, 16, 16, 48, E +1/2; (16, 24) 48, 16, 16, 48, E +1/2;
  S = 1/2 + 1/2 + 1/2 + 1/2 = 2 exactly. The controls: (0, 0) 64, 0, 0,
  64, E +1; (0, 32) 0, 64, 64, 0, E -1; (0, 16) 32, 32, 32, 32, E 0. The
  non-saturating quadruple: (0, 12) 40, 24, 24, 40, E +1/4; (4, 8) 56, 8,
  8, 56, E +3/4; (4, 12) 48, 16, 16, 48, E +1/2; S' = 3/2 exactly. The
  offsets read off the record: plus tick = age + 9, minus tick = age + 10,
  the same in every run. `tools/bell_chsh.py`: 326 criteria checked, 0
  failed, in every run the books balanced at all 138 ticks, nothing
  escaped, only `click` and `pass` records, the lamp at the end at age 138,
  phase 10, content K + 2 - 276, momentum [0, 0, 0], with 16 or 17 units
  in flight and every unit in the books; each plus Node also met the ages
  128 and 129 (ticks 137 and 138), clicked or passed by its window and
  excluded. No-signalling exact: Alice's click ages the same for a = 0
  across b in 0, 8, 12, 16, 24, 32, for a = 4 across b in 8, 12, for
  a = 16 across b in 8, 24; Bob's likewise for each b. A negative control
  of the analysis, not kept: one click's phase changed by one in a copy of
  a run fails the phase criterion and exits 1.
- **Verdict.** S = 2 exactly at the CHSH settings, the model's limit,
  outcome 1 of A2 against the 2015 data (Delft S = 2.42 +- 0.20; the
  quantum 2.828 at these settings), as the reviewers predicted before the
  run: the correlation is the triangle 1 - 4 k / N at every setting
  measured, not the cosine, and the non-saturating quadruple gives 3/2
  where the cosine would give 1.739. Not a law of nature; the model's
  stated limit, recorded.
- **Limits.** Static settings declared in the world, no last-moment
  choice (the bound here is an identity on the record, so no choice would
  change it); single units, one per interval per heading, the trivial
  regime of the law (no mixing, no suspension, a bundle of one at
  threshold 1), so nothing of the crowd's physics is exercised; N = 64;
  a bar of 21 Nodes with the sampling total by construction, every unit
  clicking once per side; no state of the pair beyond one phase stamped
  on both units.
- **Status.** measured, 2026-09-19: the model's limit (outcome 1), as
  A2's criterion states.

### C, the couplings under the law of events, on the plane (2026-09-19)

- **Confronts.** What physics calls the couplings of a static field and
  their tests: the gravitational constant G (the push of a content M on a
  content m at r; the pinned reading is G_push from the carried momentum of
  the stream); the clock at a potential (the fraction of its rate a clock
  at r from M loses, Pound and Rebka 1960, the model's `suspension` width
  against it); the index of the field (the size read at a Node, the
  isotropic index a detector reads); Gauss's law (the flux of the stream
  through every closed curve equal to the emission, 1 / r on the plane);
  the equivalence principle (the push proportional to the content pushed,
  so that every content falls alike, Eotvos to MICROSCOPE 2022, eta below
  10^-14); Newton's third law (the pushes of two contents on each other
  equal and opposite, here with unequal contents 4 : 1); the superposition
  of fields (the push of two sources the sum of the pushes of each alone);
  retardation (the field of a source arriving at r after r Links at c, one
  Link per interval); and Coulomb's law read in the same stream (the
  electric push of a charge Q on a charge q along the same units, its sign
  by the product of the charges, its ratio to the gravity push -Qq / (M m)).
  The physics-rule reviewer pinned the design and its identities on
  2026-09-19 for an open GameBoard of 61^3; the model owner cancelled that
  version the same day ("cancel the runs; let it run on two-dimensional
  GameBoards"), so the series runs on the plane: the same seven items and
  identities, the plane's exponents, the 3-D readings of the review as the
  prior, the plane's readings registered as the plane's.
- **Model prediction, pinned before the run (the physics-rule review of
  2026-09-19, credited to the reviewer; the plane's constants and exponents
  by the executing agent before the run).** Constants: a GameBoard of
  121 x 121 x 1 with `"boundary": {"z": "periodic"}` (with an extent of 1
  the two z Ports of every Node return to the same Node at the next
  interval: a true two-dimensional GameBoard, nothing leaks on z; the x and y
  faces open), the centre c = (60, 60, 0), K 2^22, N 64, `release`
  [1, 128], the free family `m` (charge 0 unless stated), the source a
  fixed measured event of content 2^24 at c (`by_clock` gives 2^17 per Port
  at every self-creation; the two z Ports' releases come home at the next
  interval as its own number and are created again in six shares, so at
  the fixed point the source releases 3 x 2^16 per Port and the net
  emission into the plane is q = 6 x 2^17 = 786432 units per interval,
  exact), the probes fixed measured events of content 1 with the default
  table (`read`: the push taken, the units mix on, transparent),
  `suspension` 0 in every world but item 6. In every world:
  `audit[t].balanced` at every interval, `measured_content` constant (read
  absorbs nothing), age + waited = the intervals completed for every
  surviving measured event. What the plane changes: a Node's count and the
  momentum a probe reads include what came back through its own z stub
  (about 2 / 9 of every mixing, one interval later), the radial flow does
  not; Gauss on a circle: 1 / r for the count, the flow and the carried
  momentum, 1 / sqrt(r) for the size; the front of the stream along an
  axis is the same lone-arrival chain as in three dimensions (the z shares
  come back one interval later); `cube_flux` sums the four in-plane faces
  (the z faces have no outside Node): Gauss's flux through the square.
  Item 1, equivalence (identity): a fixed probe of content m in 1, 4, 16 at
  (72, 60, 0), r = 12 on +x, reads push_m(t) = m x push_1(t) at every tick
  and axis; the same probe free steps identically for the three m, one
  x-step per interval, one `merged` record, the probe absent afterwards,
  the source's content 2^24 + m; the first read's tick and amount, the
  first step's tick and the merge's tick are the plane's, registered (the
  3-D prior on 61^3: the first read at tick 14 with amount 2, the first
  step at the first read, the merge at 2r + 1 = 25); the steps are the
  rule off the clock, by_clock(t - 1, |p|, m + |p|) on the reads'
  cumulative push p, x before y, at most one per interval (identity on the
  record).
  Item 2, the third law with unequal contents (a reading, not an
  identity): A = 2^22 at (56, 60, 0) and B = 2^20 at (64, 60, 0), both
  fixed, 200 intervals; P_A,x > 0 and P_B,x < 0 (toward each other);
  |P_A| / |P_B| within [1.0, 1.5] over each of the last two 50-interval
  windows, the two windows within 5 % of each other; transverse / axial
  below 5 % (on 21^3 the ratio read 1.28; no Newtonian scale on the plane).
  Item 3, superposition (identity): the item-2 pair with a fixed probe of
  content 1 at (60, 68, 0), and each source alone with the same probe:
  the probe's per-tick `read` records by `number` equal exactly, its total
  push exactly the sum (the numbers are separate groups).
  Item 4, retardation (exact where derived): the first `read` record
  (tick, amount) of a probe at r, derived by hand before the run from the
  mixing rule (the lone-arrival chain: isqrt(u x 32^2) amplitudes, the
  weights 4 : 1 : 1 : 1 : 1 : 1 reduced to 28 bits, the floors, the units
  left to the largest remainders in the tick's Port order, a group with no
  whole share going whole by its momentum; the table with its steps in the
  [README](../examples/events/coupling/README.md)): on +x r = 1..6 at tick
  r + 1: 131072, 14563, 1618, 180, 20, 3, then exhausted (the three units
  at r = 6 leave on -x and +y); on -x the same to r = 6 and (r + 1, 1) from
  r = 7; on +y 131072, 14564, 1618, 179, 20 and (r + 1, 2) from r = 6; on
  -y 131072, 14564, 1619, 180, 20 and (r + 1, 2) from r = 6. World 4 holds
  probes at r = 4 on -x, 6 on +y, 8 on -y and 12 on +x, and the +x probes
  of 1A, 7 (r = 12) and of 5P and 6 (r = 4, 6, 8, 12, 16, 20, 24, 30, 40)
  are read too: derived at -x 4 (5, 180), +y 6 (7, 2), -y 8 (9, 2), +x 4
  (5, 180), +x 6 (7, 3); registered, not derived, on +x past the front
  (r = 8 and r >= 12), the same in every world that holds a probe there;
  the push -amount x m along the axis at every first read (identity).
  Item 5, the far field (Gauss on a circle): world 5, the source alone,
  300 intervals, replayed through the API over ticks 251-300: the ring
  means (the Nodes at Euclidean distance |d - r| < 1 / 2 in the plane,
  about 2 pi r of them) per r in 4, 6, 8, 12, 16, 20, 24, 30, 40 of the
  count x r / q (a constant: flat within 10 % over r >= 8), the flow
  x 2 pi r / q (about 1 in the far field: within [0.90, 1.10] for
  r >= 8), the carried radial momentum x 2 pi r / q (likewise; from
  `sim.transits[0].fly_mom.sum(axis=(3, 4))` after `step()`, the six Ports,
  and the four in-plane Ports read beside it) and the size x sqrt(r) /
  sqrt(q) (a constant, flat within 10 % over r >= 8; the size in whole
  units, the engine's 32nds over 32); the log-log slopes over the nine
  radii count -1.00 +- 0.10, flow -1.00 +- 0.15, carried -1.00 +- 0.15,
  size -0.50 +- 0.10; `cube_flux` at h = 4, 8, 12, 20, 40 within 2 % of q
  (Gauss); the escape per interval over the window 0.95 to 1.00 of q (below
  0.95 the fixed point is not reached). World 5P, the source with content-1
  probes at r = 4, 6, 8, 12, 16, 20, 24, 30, 40 on +x: the axis readings
  push x 2 pi r / (m q), count x r / q and size x sqrt(r) / sqrt(q) at the
  probes' Nodes over ticks 151-200, registered as the axis pattern (the
  61^3 review found the axis strongly modulated: about 1.73, 1.34, 0.92,
  0.75 at r = 4, 6, 8, 12 on 31^3); no exponent is fitted through axis
  Nodes; the amount each probe reads equals the replay's count at every
  tick (identity).
  Item 6, the clock (`suspension` 1, the only world with a width): the
  probes of 5P; with the fix of 2026-09-19 a probe pays its count,
  self-creates, then reads the sizes at its Node (all other numbers) and
  owes read x 1 // 32. Expected: age + waited = 200; every count written
  equals size x 1 // 32 read at that self-creation and the ages match the
  replay exactly (identity); the clock slowed, never frozen (age(200) >
  age(60)); age(r) and the lost fraction 1 - age / 200 per r and its trend
  (the size ~ 1 / sqrt(r) on the plane, so k ~ 1 / sqrt(r)).
  Item 7, the electric reading (identity): the family `q` of kind free,
  the source with `charge` Q in 0, +2^23, -2^23 and a fixed probe of
  content 1 at (72, 60, 0) with `charge` q in 0, +2, -2, the pairs (0, 0),
  (+, +), (+, -), (-, +), (-, -), 200 intervals; D = 2^24, scale = Qq
  (D // 2^24) = +-2^24, whole = |carried| exactly: the electric part of
  each push sign(Qq) x carried (away from the emitter for like signs); the
  total push per read 0 for like signs and -2 x carried for unlike;
  `pushed` [0, 0, 0] exactly for like signs and exactly twice the (0, 0)
  world's for unlike; a (+, +) world with a probe of content 4 at the same
  Node gives the same electric part as the content-1 twin, the gravity
  parts in the ratio 4.
  Convergence, read after the runs: (a) G_push on the plane = the constant
  of carried x 2 pi r / q, flat within 5 % over r >= 5 and equal to the
  flow's within 5 %; G from step rates unreadable (every free probe steps
  one Link per interval; the equivalence identity is what is readable).
  (b) The clock: the lost fraction per r from item 6 against k / (k + 1)
  with k = size x width // 32, and the reviewer's limit: the suspension
  reads an amplitude, the size ~ sqrt(count), so the slowing scales as
  sqrt(M), on the plane as sqrt(M / r), while a potential is proportional
  to the count. (c) The exponents: |slope_count - slope_flow| <= 0.10,
  |2 slope_size - slope_count| <= 0.15, |slope_carried - slope_flow|
  <= 0.15. (d) electric / gravity = -Qq / (M m) per arrival exactly.
- **Features.** The one engine (`events-v1`, [the engine](ENGINE.md)): the
  periodic axis as a run parameter (`tests/test_periodic_axis.py`), a free
  family's release off the clock, the mixing, the push (gravity -M c,
  electric (q_A / M_A) q c), the suspension of a measured event read after
  its self-creation, the free step off the clock and the merge, the books,
  `shell_readings` and `cube_flux`. Nothing of the ray-event list above.
- **Run.** `examples/events/coupling/` (twenty-one worlds written by
  `make_worlds.py`, the dictionary in the
  [README](../examples/events/coupling/README.md), model ids
  `events-coupling-<name>-plane-v1`): `1a_m1`, `1a_m4`, `1a_m16`, `1b_m1`,
  `1b_m4`, `1b_m16`, `2`, `3`, `3a`, `3b`, `4`, `5` (300 intervals), `5p`,
  `6`, `7_00`, `7_pp`, `7_pm`, `7_mp`, `7_mm`, `7_pp_m4`, every one 200
  intervals unless stated, and `5_long` (the source alone, 1000 intervals),
  the one supplementary world, added after world 5 read an escape of 0.89 q
  over its last window, to read how the escape approaches q; not pinned.
  Commit `ddb4470a` (the base of the branch; the engine unchanged by this
  change), source fingerprint
  `06a050c9d27a5ab11febe10be40865866e7f0dcbc129400e08c2d7f6b71c8560`,
  Python 3.14.0rc2, headless, four runs at a time on four cores: 168 s of
  wall time for the twenty worlds (19 to 102 s per world) and 63 s for
  `5_long`. Recorded per run: `run.json` (`audit`,
  `conserved_at_every_completed_tick`, `measured_content`, `escaped`,
  `measured` with `pushed`, `age`, `waited`, `owed`) and `events.jsonl`
  (the `read`, `step` and `merged` records), read by
  `tools/coupling_readings.py` (integers and `fractions.Fraction` for the
  identities, floats for the ring means, the ripple bounds and the slopes;
  the replay of worlds 5 and 5_long through `EventSimulation`), which
  prints the tables and every criterion and exits nonzero on a failure.
  The commands: `python examples/events/coupling/make_worlds.py`; for each
  world `python -m event_universe --init examples/events/coupling/<name>.json
  --output artifacts/coupling/<name>`; `PYTHONPATH=src python
  tools/coupling_readings.py artifacts/coupling`.
- **Result (2026-09-19).** Every run completed; in every world the books
  balanced at every interval, the measured content constant and age +
  waited = the intervals completed. 390 criteria passed, 15 failed, exit 1;
  every failure a reading outside its bound, none an identity. Per item:
  Item 1: 185 reads per probe; push_m(t) = m x push_1(t) at every record
  and axis for m = 4 and 16 (the pushes have a transverse y part at most
  records: -amount x m on x exactly at 2 of the 185); `pushed`
  (-2634004, 5855, 0), (-10536016, 23420, 0), (-42144064, 93680, 0), m
  times exactly; the first read at tick 15 (r + 3) with amount 1 and push
  (-m, 0, 0). The free probes: 11 steps at ticks 16..26, x 72 down to 61,
  identical for the three m and their momenta m times 1b_m1's
  ((-3, 0, 0) at the first step to (-403785, 797, 0) at the last); the
  steps and the merge equal the rule off the clock on the reads' cumulative
  push at every tick (the first read of one unit gives p / (m + p) = 1 / 2
  and by_clock(14, 1, 2) = 0, so the first step comes at tick 16 after the
  second read, p = 3m, by_clock(15, 3, 4) = 1); one `merged` record at tick
  27 = 2r + 3 into the source with amount m; the source's content
  2^24 + m at the end; 13 reads per free probe, m times 1b_m1's.
  Item 2: per 50-interval window (P_A, P_B, the ratio of the axial parts)
  1-50 (135840923648, -41943040, 0), (-176993337344, 186646528, 0), 0.768;
  51-100 (280443748352, -2403336192, 0), (-307688898560, -2453667840, 0),
  0.912; 101-150 (375159521280, -1660944384, 0), (-298589356032,
  -1201668096, 0), 1.256; 151-200 (405610168320, 15309209600, 0),
  (-334517764096, -6669991936, 0), 1.213; cumulative (1197054361600,
  11202985984, 0), (-1117789356032, -10138681344, 0), 1.071; the last two
  windows 3.6 % apart; transverse / axial 0.0094 and 0.0091. Item 3: 187
  records per number, the probe's records of A and of B in world 3 equal
  to 3a's and 3b's exactly, `pushed` (-287187, -807291, 0) = (-423030,
  -647305, 0) + (135843, -159986, 0) exactly, A's and B's mutual records
  unchanged by the probe. Item 4: -x 4 (5, 180, push (180, 0, 0)), +y 6
  (7, 2, (0, -2, 0)), -y 8 (9, 2, (0, 2, 0)), +x 4 (5, 180, (-180, 0, 0)),
  +x 6 (7, 3, (-3, 0, 0)), every derived entry as derived; registered on +x
  past the front, the same in every world: r = 8 (11, 8), r = 12 (15, 1),
  16 (19, 1), 20 (23, 1), 24 (27, 1), 30 (33, 1), 40 (43, 1): past the
  front the first read comes three intervals after r Links, one unit whole
  by its momentum from r = 12 on. Item 5, world 5 over ticks 251-300 (r:
  count x r / q, flow x 2 pi r / q, carried x 2 pi r / q over the six
  Ports, over the four in-plane Ports, size x sqrt(r) / sqrt(q)): 4:
  0.3320, 1.0762, 1.5023, 1.2642, 0.8743; 6: 0.3252, 1.0325, 1.4468,
  1.1875, 0.9525; 8: 0.3375, 1.0294, 1.4890, 1.2463, 0.9012; 12: 0.3336,
  0.9577, 1.4571, 1.2098, 0.9135; 16: 0.3343, 0.9851, 1.4476, 1.1884,
  0.9465; 20: 0.3394, 0.9981, 1.4681, 1.1940, 0.9748; 24: 0.3343, 1.0007,
  1.4425, 1.1790, 0.9418; 30: 0.3331, 0.9503, 1.4340, 1.1753, 0.9427; 40:
  0.3352, 0.9461, 1.4468, 1.1971, 0.9088; the count flat within 1.9 % and
  the size within 8.2 % over r >= 8; the slopes count -0.993, flow -1.048,
  carried -1.014 (in-plane -1.023), size -0.481; the flux through the
  square / q 0.9948, 0.9929, 0.9876, 0.9793, 0.9311 at h = 4, 8, 12, 20,
  40; the escape 0.8921 q per interval. Outside the bound: carried
  x 2 pi r / q 1.43 to 1.49 at the seven far-field radii (about 1
  expected), the flux at h = 20 (0.9793) and h = 40 (0.9311), the escape
  (0.8921): the fixed point is not reached at 300 intervals. World 5_long
  (supplementary): the escape per interval / q over the 100-interval
  windows ending at 200 to 1000: 0.6596, 0.8885, 0.9177, 0.9262, 0.9310,
  0.9400, 0.9418, 0.9473, 0.9465 (0.9479 over ticks 951-1000, still below
  0.95); over ticks 951-1000 the flow x 2 pi r / q 0.96 to 1.10 and the
  flux through the square / q 0.9985, 0.9964, 0.9936, 0.9867, 0.9672,
  while the count x r / q has risen to 0.41-0.46, the carried to 1.69-1.89
  (in-plane 1.41-1.54) and the size to 0.88-0.98: the radial flow is
  Gauss's from 300 intervals on, the standing population at the rings is
  still growing at 1000 (the slopes there count -0.942, flow -1.050,
  carried -0.972, size -0.474). World 5P, the axis pattern over ticks
  151-200 (r: -push_x x 2 pi r / (m q), count x r / q, size x sqrt(r) /
  sqrt(q)): 4: 1.7148, 0.3113, 0.8910; 6: 1.5662, 0.3023, 0.8926; 8:
  1.4930, 0.2992, 0.8948; 12: 1.5358, 0.3194, 0.8962; 16: 1.4399, 0.3043,
  0.9084; 20: 1.3532, 0.2884, 0.9315; 24: 1.4013, 0.3002, 0.9476; 30:
  1.3018, 0.2801, 0.8590; 40: 1.2488, 0.2693, 0.7167; the amount read equal
  to the replay's count at every tick at every probe (identity), 196 to 147
  reads per probe. Item 6: (age, waited, owed) at 200 equal to the replay
  of the counts read at every radius (identity): r = 4 (6, 194, 222), 6
  (9, 191, 178), 8 (13, 187, 219), 12 (19, 181, 131), 16 (25, 175, 62), 20
  (31, 169, 43), 24 (38, 162, 134), 30 (47, 153, 21), 40 (63, 137, 8); age
  + waited = 200 everywhere; the source at age 200, waited 0; the lost
  fraction 0.970, 0.955, 0.935, 0.905, 0.875, 0.845, 0.810, 0.765, 0.685,
  falling with r; k over ticks 151-200 395, 323, 281, 229, 201, 185, 172,
  139, 100 (k x sqrt(r) 790 to 840 up to r = 24, then 762 and 636 where
  the field is still filling), k / (k + 1) 0.9975 to 0.9901; the count
  written at the last self-creation 403 (tick 19), 346 (32), 330 (89), 251
  (80), 183 (79), 186 (57), 190 (144), 147 (74), 118 (90). Outside the
  bound: age(200) = age(60) at r = 4, 6 and 20 (6, 9, 31): with k + 1 above
  100 at every radius the 200 intervals hold at most one self-creation
  after the field builds, so the criterion cannot separate slow from
  frozen there; the counts written are finite and being paid down (the
  rule stops no clock). Item 7: 185 records per world, the same ticks and
  amounts as 7_00 whose records equal 1a_m1's; every push (m - sign(Qq))
  times the (0, 0) push: 0 for (+, +) and (-, -) with `pushed` (0, 0, 0),
  2 for (+, -) and (-, +) with `pushed` (-5268008, 11710, 0) = 2 x
  (-2634004, 5855, 0), and 3 for the content-4 (+, +) probe with `pushed`
  (-7902012, 17565, 0); electric / gravity -1 and -1/4 on every axis of
  every record; the electric part of the content-4 probe equal to the
  content-1 twin's and equal to the carried momentum at every record.
  Convergence: (a) carried x 2 pi r / q over r >= 5: 1.4540 (min 1.4340,
  max 1.4890, flat within 3.8 %; 1.1972 over the four in-plane Ports); the
  flow's 0.9875 (0.9461 to 1.0325); not equal within 5 % (0.47 apart): the
  departures' momentum at a Node counts the back-scattered shares, which
  carry outward momentum while moving inward, and the stub's returns,
  while the flow counts the net units; the flow is Gauss's constant, the
  carried is 1.45 times it on the plane. (b) The lost fraction against
  k / (k + 1): 0.685 to 0.970 found against 0.990 to 0.998, the difference
  the self-creations before the front arrives and the field builds (age
  about the arrival tick plus a few); the reviewer's limit stands: the
  suspension reads an amplitude. (c) 0.055, 0.031, 0.034, within their
  bounds. (d) Exact. A negative control of the analysis, not kept: one
  push changed by one unit in a copy of 1a_m4's events fails the
  equivalence identity (16 failures against 15) and exits 1.
- **Verdict per item.** Item 1, identity held (the 3-D prior for the
  first read, the first step and the merge did not hold on the plane, by
  the arithmetic of the record: the plane's ticks registered). On
  2026-09-19 the model owner decided, on the mathematician's list, that
  item 1 is registered as an identity of the phase-less field of matter
  only, since under node-mixing v3 the fields of a family with a phase
  circle interfere, and that is the law and not a defect (the run read a
  family with a phase circle, before that decision; a correction of the
  register, not a law). Item 2,
  reading within the bound (1.256 and 1.213, within 5 % of each other;
  the cumulative 1.071). Item 3, identity held; on 2026-09-19 registered,
  by the same decision, as an identity of the phase-less field of matter
  only (the superposition of two fields of a family with a phase circle is
  their interference under v3). The one reading set of 2026-09-19 (the
  presence counting a measured event's content, here; a detector's
  threshold and window reading every number but the Node's own;
  [migration](MIGRATION.md#one-reading-set-for-every-coupling-on-2026-09-19))
  re-pins no reading of this series: its streams are free families, never
  suspended, and its probes read at threshold 1 without windows, where the
  set's gate is the number's; every reading and identity above stands as
  registered (old = new). Item 4, the front as
  derived at every derived Node; the +x pattern past the front registered.
  Item 5, the exponents within their bounds (count -0.99, flow -1.05,
  carried -1.01, size -0.48: Gauss on a circle) and the flow about 1;
  outside the bound: the carried momentum (1.45, a GameBoard reading of what
  the departures carry, not an engine bug: the books balance and the
  replay equals the audit) and the flux at h >= 20 with the escape 0.89 at
  300 and 0.948 at 1000 (a GameBoard limit: on the plane the back-scattered
  population fills the GameBoard slowly and the fixed point is approached, not
  reached, in 1000 intervals). Item 6, identity held; the bound age(200) >
  age(60) outside at three radii (a design limit of the 200-interval
  window against k + 1 above 100 on the plane, not a frozen clock). Item
  7, identity held. Convergence (a) flat, not equal to the flow; (b) the
  trend read, the limit stated; (c) within the bounds; (d) exact.
- **Limits.** No Newtonian regime: the far field on the plane is Gauss's
  1 / r, the push on a probe is the stream's carried momentum, and no G in
  the units of physics is read (G_push is a GameBoard constant, 1.45 over
  the six Ports and 1.20 over the in-plane Ports, in units of q / (2 pi
  r)). The axis pattern: the readings on the source's own GameBoard line are
  strongly modulated (push x 2 pi r / (m q) 1.71 at r = 4 falling to 1.25
  at r = 40) and are not the law; no exponent through axis Nodes. sqrt(M):
  the suspension reads an amplitude, so the clock's slowing scales as
  sqrt(M / r) on the plane, and at this source the size on the axis is 100
  to 400 whole units, so a probe self-creates once per 100 to 400
  intervals: a longer run is needed to read the slowed rate itself. The
  third law with unequal contents reads 1.2 to 1.3 in the late windows,
  not 1: the two contents read each other's stream through different
  cross-sections and the pushes ripple with the whole units. The plane
  against space: the stub returns 2 / 9 of every mixing to the same Node,
  so the count and the carried momentum at a Node are not those of a
  three-dimensional GameBoard, and the fixed point is approached slowly (the
  escape 0.948 q at 1000 intervals). Every reading is one run at one
  fingerprint; nothing is a law of nature.
- **Status.** measured, 2026-09-19: identities held (items 1, 3, 6, 7, the
  derived front of item 4, convergence (d)); readings within the bound
  (item 2, the exponents and the flow of item 5, convergence (c));
  readings outside the bound reported (the carried momentum, the flux at
  h >= 20 and the escape of item 5, the not-frozen bound of item 6 at three
  radii, convergence (a)'s equality with the flow).

### A2, under the Beam Law (2026-09-19)

- **Confronts.** As A2 and as the entry above: the CHSH inequality in the
  phase form, the settings phases, the loophole-free experiments of 2015
  (Delft, S = 2.42 +- 0.20; the quantum maximum 2 sqrt 2). Re-registered
  under `rays-v1` the night of 2026-09-19, when the Beam Law replaced
  the law of events ([the Beam Law](BEAM_LAW.md), section 8: "Bell A2
  unchanged: S = 2 exactly, E(a, b) the triangle 1 - 4 k / N").
- **Model prediction, pinned before the run (the physicist and the
  mathematician, Highlights 5.4; BEAM_LAW section 8).** Unchanged: with a
  deterministic local phase window each click is a function of the arriving
  phase and the local setting alone, so CHSH is at most 2 as an identity on
  the record; E(a, b) = 1 - 4 k / N; S = 2 exactly, S' = 3/2 exactly,
  no-signalling exact. What the Beam Law changes is the timing only: a ray
  flies at 1 / sqrt 3 by the flight table, so the eight Links to a plus Node
  take 13 walks after the ray's first walk and the ninth two more; the
  offsets are expected at plus 14 and minus 16 (the law of events: 9 and
  10) and the run needs 160 intervals for the 128 pairs.
- **Features.** The one engine (`rays-v1`): a lamp of a paid family releasing
  one ray per self-creation on +X and on -X (`lamp.directions`), detectors
  of threshold 1 and the phase window (`tests/test_nature_beam_window.py`); the
  window reads each ray's own phase. Nothing else: one ray per interval per
  direction, no collision on the bar (rays of one number on one line never
  meet head-on), no suspension.
- **Run.** `examples/events/bell/` (ten worlds written by `make_worlds.py`,
  the dictionary in the [README](../examples/events/bell/README.md)): the
  base of the entry above with `"law": "rays"`, `ticks` 160, the model ids
  `rays-bell-a{a}-b{b}-v1`; the same ten settings; the analysis
  `tools/bell_chsh.py` unchanged in its criteria (the `record` line admitted
  among the record kinds; the plus offset checked below the minus).
  `tests/test_nature_beam_worlds.py` (b) runs the ten worlds through the tool.
- **Result (2026-09-19, measured).** Branch `claude/universe24-new-3ytqde`,
  the Beam Law's commits on the base `ce0b22af`, source fingerprint
  `703f9427d9f70e6c619218e457edca0b7647381a8cc7a20d140e4a3d9dd3f671`, Python 3.14, headless, about 0.2 s per run. Every
  count as pinned: E +1/2 (96 / 32), -1/2 (32 / 96), +1/2, +1/2 at the CHSH
  settings, S = 2 exactly; the controls +1 (128 / 0), -1 (0 / 128), 0
  (64 / 64); E +1/4 (80 / 48), +3/4 (112 / 16), +1/2 on the non-saturating
  quadruple, S' = 3/2 exactly; the offsets plus 14, minus 16 in every run
  (expected 14 and 16); no-signalling exact; the books balanced at every
  tick, nothing escaped, the lamp's momentum [0, 0, 0]; 326 criteria, 0
  failed, exit 0. Measured = expected on every line. The model's limit,
  outcome 1 of A2 against the 2015 data; not a law of nature. Limits as in
  the entry above.
- **Re-read under the label along the unit vector (2026-09-19; measured).**
  The ten worlds run again on the source whose momentum label is along the
  unit vector u_d of the direction at the scale Q = 64 ([BEAM_LAW section
  10](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation),
  note 23; source fingerprint `0eaa589ab51cdc0a12a863cd23e535e1e8ac052e8b4f3f8facf30ef05a323c5a`): every count, phase, offset and
  book as registered, S = 2 exactly, S' = 3/2, no-signalling exact, the
  lamp's momentum [0, 0, 0] (its recoils on +X and -X cancel in label
  units as they did before), `tools/bell_chsh.py` 326 criteria, 0 failed;
  the paid labels x 64 appear in the momentum lines of the clicks only.
  Measured = expected; the Bell setup reads no momentum.

### C, the couplings under the Beam Law, on the plane (2026-09-19)

- **Confronts.** As the entry above (G, the clock at a potential, Gauss's
  law, the equivalence principle, the third law, superposition,
  retardation, Coulomb's law read in the same stream), re-registered under
  `rays-v1` the night of 2026-09-19 with the expectations of
  [the Beam Law](BEAM_LAW.md), section 8: the beams do not spread, so
  the readings of a ballistic stream replace the readings of a diffusive
  field; the 1b merge criteria become the refusal; item 6's slowing
  changes power (the accepted price: on the axis the presence does not
  fall with r).
- **Model prediction, pinned before the run (BEAM_LAW section 8, the design
  of 2026-09-19; the details by the executing agent before the rerun).**
  The base of the entry above with `"law": "rays"` and the source releasing
  on the six headings (`by_clock` 2^17 per heading per self-creation; the
  two z rays home at their first walk and created again in six shares, so
  q = 6 x 2^17 = 786432 per interval into the plane in four in-plane beams
  of 3 x 2^16). Expected: item 1 the identity push_m = m x push_1 record by
  record, the first read at tick 21 (1 + the flight table's first arrival
  at 12 Links) with amount 2^17 whole, the free probes stepping from the
  first read to the Node beside the source and every further step refused
  (no merge), no `merged` record; item 2 the third law 1.00 exactly where
  both streams are lone rays on the axis, here to the grain of the whole
  apportioning of 2^15 and 2^13 over six headings (the cumulative ratio
  1.0000 at four decimals, zero over the first window); item 3 the identity
  (the probe off both axes reads nothing); item 4 the front at r at tick
  1 + m^-1(r): r = 4 tick 8, 6: 11, 8: 14, 12: 21, 16: 28, 20: 35, 24: 42,
  30: 52, 40: 69, amount 2^17 whole; item 5 count x r / q constant within
  10 % for r >= 8, on the six headings a ring mean over mostly empty Nodes
  0.15 to 0.19, flow x 2 pi r / q 1.00 +- 0.10, the flux through the square
  within 2 % of q, the slopes -1.00 +- 0.10 (the flow +- 0.15); item 6 the
  count k ~ presence, ~ 1 / r in the mean over a ring, granular (a Node
  reads one ray or none), the replay of (age, waited, owed) exact; item 7
  electric / gravity = -Qq / (M m) exactly. Criteria (identities, books,
  timing) fail the tool; the far-field readings are registered inside or
  outside the expectation and never moved.
- **Features.** The one engine (`rays-v1`): the flight table, the six-heading
  release, the one reading (the push by the flow, the presence over rest
  and moving rays), the clock's count off the clock, the refused step, the
  face detectors. No collision acts (the beams of one number on one axis
  never meet head-on; the two sources of item 2 have different numbers and
  never collide).
- **Run.** `examples/events/coupling/` (twenty-one worlds written by
  `make_worlds.py`, the dictionary in the
  [README](../examples/events/coupling/README.md)), the model ids
  `rays-coupling-<name>-plane-v1`; `tools/run_series.py --jobs 4`;
  `tools/coupling_readings.py` rewritten for the ray record (the replay of
  world 5 reading the count, the presence and the flow at every tick, the
  flux through the square summed in the tool, the readings printed inside
  or outside).
- **Result (2026-09-19, measured against expected).** Branch
  `claude/universe24-new-3ytqde`, the Beam Law's commits on the base
  `ce0b22af`, source fingerprint `703f9427d9f70e6c619218e457edca0b7647381a8cc7a20d140e4a3d9dd3f671`, Python 3.14, headless;
  every run completed with the books balanced at every tick, the measured
  content constant, age + waited = the intervals completed; 0.5 to 3.3 s per
  run; 392 criteria passed, 0 failed, exit 0; 19 readings inside the
  expectation, 9 outside, registered, none moved.
  - Item 1 (expected the identity; the first read at tick 21 with 2^17; the
    steps to x = 61 then refused): measured the identity at all 180 records
    and three axes for m = 4, 16; the first read (21, 131072); the steps at
    ticks 21 to 31, x from 72 to 61, identical for the three m and equal to
    the rule off the clock; no `merged` record. Measured = expected.
  - Item 2 (expected 1.00 to the apportioning's grain): measured
    P_A = (9612145197056, 0, 0), P_B = (-9612088573952, 0, 0), the ratio
    1.0000, the sum 5.9e-6 of the push; per tick the difference at most
    0.05 %; zero over the first window (1881199869952 each way). Measured
    = expected.
  - Item 3 (expected the identity): measured 0 records of either number at
    the probe (off both axes) in `3`, `3a` and `3b`, the push (0, 0, 0):
    the identity holds trivially. Measured = expected; the item reads
    nothing under a law whose beams do not spread.
  - Item 4 (expected the flight table's ticks with 2^17 whole): measured
    (8, 131072) at r = 4 on -x, (11, 131072) at 6 on +y, (14, 131072) at 8
    on -y, (21, 131072) at 12 on +x, and on +x in `5p` and `6` (8, 11, 14,
    21, 28, 35, 42, 52, 69) at r = 4 to 40. Measured = expected.
  - Item 5 (world 5, ticks 251-300; expected count x r / q constant within
    10 %, 0.15 to 0.19 on the six headings; flow x 2 pi r / q 1.00 +- 0.10;
    the flux within 2 %; the slopes -1.00): measured count x r / q 0.125,
    0.150, 0.167, 0.176, 0.143, 0.179, 0.167, 0.150, 0.152 at r = 4, 6, 8,
    12, 16, 20, 24, 30, 40 (the ripple over r >= 8 0.25, outside; r = 16
    0.143, outside; the others inside: a ring mean of six beams is
    r / Nodes(r) x the axial count / q, and the GameBoard rings at r = 16 and
    r = 20 both hold 112 Nodes); presence x r / q twice the count at r >= 6
    (the presence / count 2.000: two rays of the beam at a Node in the mean,
    against 1 / c = 1.73); flow x 2 pi r / q 0.785, 0.942, 1.047, 1.109,
    0.898, 1.122, 1.047, 0.942, 0.952 (r = 12, 16, 20 outside 0.90 to 1.10,
    the same ring counts); the slopes count -0.944 and flow -0.944 (inside),
    presence -0.760 (outside); the flux through the square / q 1.0000 at
    h = 4, 8, 12, 20, 40 and the escape 1.0000 q (inside: Gauss exact for a
    ballistic stream). World 5_long over ticks 951-1000 reads the same.
  - Item 5P (the axis pattern): -push_x x 2 pi r / (m q) = 2 pi r / 4 at
    every r (6.28 to 62.83), count x r / q = r / 4 (the axial count q / 4
    per interval, constant with r), the presence 196609 at r = 4 and 393216
    to 393217 at r >= 6; the amount read equal to the replay's count at
    every tick at every probe.
  - Item 6 (expected the replay exact; k ~ 1 / r in the mean over a ring,
    granular): measured (age, waited, owed) equal to the replay at all nine
    radii; the clock counts until the front's arrival (age(200) = 8, 11,
    14, 21, 28, 35, 42, 52, 69 at r = 4 to 40) and is then owed 130880 to
    130941 intervals, the beam's presence 2^17 or 2^18 read at one
    self-creation: on the axis the slowing does not fall with r (the
    design's accepted price, section 8 item 6); off the axis a Node reads
    nothing. The reading "the share lost against k / (k + 1), k = q /
    (6 r)" 0.96 to 0.66 at r = 4 to 40 is inside the expectation at every r
    and says only that the clock counted before the front arrived.
  - Item 7 (expected -Qq / (M m) exactly): measured like signs `pushed`
    [0, 0, 0], unlike twice the uncharged world's (-70582384, 0, 0), the
    content-4 probe 3 times; electric / gravity -1 and -1/4 exactly.
    Measured = expected.
  - Convergence: (a) flow x 2 pi r / q mean 1.0075 over r >= 5, the ripple
    0.25 (outside 0.10); (c) |slope_count - slope_flow| 0.000 (inside),
    |slope_presence - slope_count| 0.18 (outside 0.10); (d) exact.
- **Re-read under the one push form (2026-09-19, the night; measured).**
  The twenty-one worlds run again on the source that reads the push as one
  bilinear form over the rays' labels with the emitter's factor on the
  record ([BEAM_LAW section 10](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation),
  notes 18 to 20; source fingerprint `cc7815756f50640ad10582af461cf58267c424eb8182177e580d0b5eedbd4769`): every `events.jsonl` is
  identical byte for byte to the run on the tip before it (fingerprint
  `70763568dc216a8b7a0ecdfac36654cdf1e1da80bb6b20d34eccfac2d8c62c8e`), the series 7 `read` records among them row by row (kappa 0
  in `7_pp` and `7_mm`, -2^25 and -2 in `7_mp` and `7_pm`, -12582912 and
  -3 in `7_pp_m4`, -2^24 and -1 in `7_00`); `tools/coupling_readings.py`:
  392 criteria passed, 0 failed, 19 readings inside and 9 outside, every
  printed line equal to the line above but the fingerprint. The one form
  equals the three-branch push integer by integer ([validation](VALIDATION.md)).
- **Re-read under the label along the unit vector (2026-09-19; measured).**
  The twenty-one worlds run again on the source whose momentum label is
  along the unit vector u_d of the direction at the flight table's scale
  Q = 64 ([BEAM_LAW section 2](BEAM_LAW.md#2-the-record-of-a-ray-and-the-world-file)
  and note 23; the model owner's decision on the physics-rule reviewer's
  verdict; source fingerprint `0eaa589ab51cdc0a12a863cd23e535e1e8ac052e8b4f3f8facf30ef05a323c5a`, Python 3.14, headless, four
  cores, 0.3 to 2.5 s per run). On the six headings the label of a unit is
  64 e_d, so every push, momentum and momentum book line of the record is
  the registered one times 64 exactly, the electric part included (q_A
  q_B / M_B is an integer on every series 7 world), while the counts, the
  presences, the clock and Gauss's flux off the Port crossings are
  unchanged; `tools/coupling_readings.py` divides the labels by Q where it
  compares with the emission q or an amount, so the expectations of BEAM_LAW
  section 8 keep their meaning: 392 criteria passed, 0 failed, 19 readings
  inside and 9 outside, every reading equal to the registered one (count x
  r / q 0.125 .. 0.152, flow x 2 pi r / q 0.785 .. 0.952 at r = 4 to 40,
  the flux through the square 1.0000 q, the slopes -0.944, -0.944, -0.760).
  In label units: item 1's first read (21, 131072, (-8388608, 0, 0)) and
  `pushed` (-2258636288, 0, 0) for m = 1; item 2 P_A = (615177292611584,
  0, 0), P_B = (-615173668732928, 0, 0), the ratio 1.0000, the sum
  5.89e-6 of the push; item 7 unlike signs `pushed` (-4517272576, 0, 0),
  the content-4 probe (-6775908864, 0, 0), electric / gravity -1 and -1/4
  exactly; the free probes' steps (ticks 21 to 31) identical, the rule off
  the clock now `by_clock(t - 1, |p|, 64 m + |p|)` on the cumulative push
  in label units. Measured = registered on every line.
- **Series 7 re-registered under the charge per unit of content
  (2026-09-20; measured).** The model owner's decision that charge is per
  unit of content of a family ([BEAM_LAW note 28](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)):
  the six item 7 worlds declare two free families, `q` for the source
  (`charge` [1, 2] or [-1, 2]: 2^23 on 2^24) and `p` for the probe ([2, 1]
  or [-2, 1] on content 1; [1, 2] on the content-4 probe of `7_pp_m4`), no
  `charge` on a measured event, and the push is one product `M_A x (rho_A
  rho_B - 1) x V_B` with the electric part `sign x by_clock(age_A, |V n_A
  n_B M_A|, d_A d_B)`. Run headlessly through `NatureBeamSimulation` on the tip
  before the change (the per-event charges, `q_A q_B / M_B`) and after it:
  the `read` records of every world equal tick by tick, number by number
  and integer by integer (181 records in `7_00`, `7_pp`, `7_pm`, `7_mp`,
  `7_mm`, 185 in `7_pp_m4`), the events counted equal (4635; 4663), every
  `pushed` and momentum equal (the probe's (-2258636288, 0, 0) in `7_00`,
  (0, 0, 0) in `7_pp` and `7_mm`, (-4517272576, 0, 0) in `7_pm` and
  `7_mp`, (-6775908864, 0, 0) in `7_pp_m4`; the source's (1073741824,
  0, 0), 0, (2147483648, 0, 0), (4026531840, 0, 0)), the books balanced
  with the recount. The probe's `read` records now carry the family `p`
  (the source reads the probe's rays under `p`, the probe the source's
  under `q`); `tools/coupling_readings.py` item 7 reads the declared
  charges (Q, q) off the families' pairs times the amounts (the tool's
  owner). No integer of the register moves.
- **Verdict.** Every identity, book and timing of the Beam Law holds on the
  plane exactly; the far-field readings of a six-beam source follow the
  GameBoard ring's Node count and not r, so the design's ±10 % expectation for
  the ring means is not met by six beams (the design expected 0.15 to 0.19
  on the six headings and 0.31 to 0.33 on a fan); the clock on a beam's axis
  is owed the beam's presence and does not slow as 1 / r. Whether the series
  should be rerun with a source releasing on a fan of directions is the
  model owner's decision (PROJECT_STATUS, "What is open"); nothing was
  tuned.

- **Re-read under the contact through the table (2026-09-20).** The
  free probes of `1b_m1`, `1b_m4` and `1b_m16` step to the Node beside
  the source as registered (11 steps, the same records); from tick 32
  every refused step hands the probe's x component to the fixed source
  (169 `contact` records, m times `1b_m1`'s), the probe's momentum 0 at
  the end where it was -2 260 249 792 (m = 1) and the source's
  -1 186 507 968 where it was 1 073 741 824; the sum of the two and the
  reads unchanged. The other eighteen worlds are byte-identical
  ([validation](VALIDATION.md#the-columns-the-lifetime-the-held-content-and-the-contact-through-the-table-the-66-example-worlds-compared---2026-09-20)).
- **Re-read under the step drive (2026-09-20).** The free probes of
  `1b_m1`, `1b_m4` and `1b_m16` make the same 11 steps to the Node beside
  the source, each one interval later than registered (the ticks 22 to
  32 in place of 21 to 31: the probe's drive begins at 0 when the first
  rows arrive), and hand their x component over from tick 33 (168
  `contact` records in place of 169 from tick 32, the first hand-over
  larger, -157 823 232 for m = 1 in place of -146 316 992); the probe's
  momentum 0 at the end and the source's -1 185 431 936 (m = 1),
  -3 667 985 920 (m = 4), -13 598 201 856 (m = 16) where they were
  -1 186 507 968, -2 598 548 224, -12 541 676 544; the reads and the sum
  of the two momenta as before. The eighteen other worlds have no free
  body and read the same (the record's new fields aside) ([migration](MIGRATION.md#the-step-drive-on-2026-09-20-the-count-of-links-as-the-whole-part-of-the-driven-distance)).


### D, the orbit under the Beam Law, on the plane (2026-09-19)

- **Confronts.** Whether a light free probe closes an orbit about a heavy
  fixed source under the measured push law with the width of the push (the
  model owner's D1 of 2026-09-19, the world key `width`, [BEAM_LAW section
  3](BEAM_LAW.md#3-the-nodes-interval-nature_beam) step 5 and note 15), and
  how its period scales with the radius: on the plane a ballistic stream
  falls as 1 / r (series C, Gauss exact), so the expected law is a flat
  rotation curve, T proportional to r, T(24)^2 / T(12)^2 = (24 / 12)^2 = 4
  (k = 2), not Kepler's k = 3 (8). The push's grain (whole units of m per
  arriving unit of flow, along the arrival Port's heading), the field's
  granularity (a fan's lines separate from r of about 16 on) and the
  flight's anisotropy (the speed per axis, x before y) were named before
  the run as what could break the orbit.
- **Model prediction, pinned before the runs
  ([the derivation](../examples/events/orbit/README.md#the-derivation-of-p-before-the-runs);
  re-derived the night of 2026-09-19 for the label the law reads).** The
  push a free probe takes from an arriving fan ray is its label, -m x
  amount x D[direction] ([BEAM_LAW section 2](BEAM_LAW.md#2-the-record-of-a-ray-and-the-world-file)),
  |D| units of momentum per unit of amount, so the push per interval on
  the probe of content m at r is m q L C / (2 pi r) toward the source, L
  the fan's mean label magnitude (the mean |D| over its 120 directions,
  5.194) and C = 1 from series C (flow x 2 pi r / q = 1.00 +- 0.10); with
  the width S the speed is p / (S m + p) per axis; a circular orbit needs
  p^2 / (S m + p) = m q L C / (2 pi), independent of r. With q = 12 and
  m = 1, A = q L / (2 pi) = 9.920: S = 1: p = 11 (n = 10.836), v = 0.917
  per axis, faster than the rays (1 / sqrt 3 = 0.577), no closed orbit
  expected; S = 8: p = 15 (15.156), v = 0.652, faster than the rays too,
  no closed orbit expected; S = 32: p = 23 (23.455), v = 0.418, T(12) =
  180, T(24) = 361, expected closed at both radii within the grain (a kick
  of |D| units per arriving ray, 1 to 8 on a momentum of 23: 2.5 to 20
  degrees). Criteria as first pinned: closed if at the first tick at which
  the angle about the source reaches 2 pi the probe is within one Link of
  its start on each axis with its momentum's y component of the initial
  sign; T within +- 15 %; the mean radius over the first orbit r +- 1;
  |drift| <= 1 Link per orbit; the ratio 4 +- 15 %; C measured on the
  orbit against m q L / (2 pi r) 1.00 +- 0.15. The record checks
  (completed, the books balanced) fail the tool; the readings are
  registered inside or outside, never moved.
- **The first registration (history; the engine of the D1 commit, before
  the moments change).** With the push the unit Link of a ray's last step
  the derivation took L = 1 (p = 3, 5, 9 at S = 1, 8, 32) and the six
  worlds read (source fingerprint
  `587cbf4852a7fafddc07b2ab35a6a530ed27607ea1aaaec8b17d89933e66d788`):
  one orbit closed by the criterion (S = 32, r = 12: one turn in 346
  intervals against 343 derived, the return one Link off, an eccentric
  loop of mean radius 13.83 whose later turns wandered and escaped), no
  closing at S = 8 (r = 12 spiralled in, r = 24 swung out to r = 75, one
  turn in 825), at S = 1 (the probe outran the field, zero reads) or at
  S = 32, r = 24 (fell inward, one turn in 541); T(24)^2 / T(12)^2 2.44;
  C 1.1 on the first turns. Under the engine of the moments change those
  worlds read no orbit at any S and C 4.51, 8.77, 1.34, 2.75 (the fan's
  labels), which is why p was re-derived; the worlds of that registration
  are in git at the D1 commit.
- **Features.** The width of the push in `_move`; the free release on a
  declared fan; the one push form over the rays' labels (the push of a fan
  ray its label); the face detectors (the escapes); `suspension` 0 (the
  clock's count not read); no collision at the source's or the probe's
  Node.
- **Run.** `examples/events/orbit/` (six worlds by `make_worlds.py`,
  `s<S>_r<r>` for S in 1, 8, 32 and r in 12, 24, 121 x 121 x 1 with z
  periodic, 4000 intervals each, the momenta since the label along the
  unit vector 192, 320, 576 in label units, that is 3, 5, 9 units of the
  probe's content; the second registration's 11, 15, 23 and the first's
  3, 5, 9 in the old units are in git), the model ids
  `rays-orbit-s<S>-r<r>-plane-v1`; `tools/run_series.py --jobs 4`;
  `tools/orbit_readings.py` (the trajectory from the probe's `step`
  records, the push from its `read` records in units of Q, C against
  m q L / (2 pi r), L the fan's mean |u_d| / Q).
- **Result (2026-09-19, the night, measured against expected).** The
  worktree of `claude/universe24-new-3ytqde` on the one-form commits,
  source fingerprint `cc7815756f50640ad10582af461cf58267c424eb8182177e580d0b5eedbd4769`, Python 3.14, headless, four cores; every run
  completed in 5.7 to 6.5 s with the books balanced at every tick; 12
  record checks passed, 0 failed, exit 0. The table (T the first closing
  of the angle; C measured on the first orbit, or over the run where no
  angle closed; "end" how the run ended):

  | World | S | r | p | Closed (expected) | T (expected) | Mean radius (expected r +- 1) | Drift per orbit | Turns | r min .. max | Reads / units | C (expected 1.00 +- 0.15) | End |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | `s1_r12` | 1 | 12 | 11 | no turn (no) | - (82) | - | - | 0.22 | 12.0 .. 61.2 | 0 / 0 | - | escaped through face:+y at tick 67 |
  | `s1_r24` | 1 | 24 | 11 | no turn (no) | - (165) | - | - | 0.19 | 24.0 .. 64.6 | 0 / 0 | - | escaped through face:+y at tick 67 |
  | `s8_r12` | 8 | 12 | 15 | no turn (no) | - (116) | - | - | 0.22 | 12.0 .. 61.2 | 0 / 0 | - | escaped through face:+y at tick 94 |
  | `s8_r24` | 8 | 24 | 15 | no turn (no) | - (231) | - | - | 0.19 | 24.0 .. 64.6 | 0 / 0 | - | escaped through face:+y at tick 94 |
  | `s32_r12` | 32 | 12 | 23 | no: the return (-2, 0), heading kept (yes) | 229 (180) | 17.30 | -2.00 | 1.57 | 3.0 .. 66.6 | 38 / 404 | 1.43 (the first turn: 21 reads, 242 units) | escaped through face:-x at tick 470 |
  | `s32_r24` | 32 | 24 | 23 | no turn (yes) | - (361) | - | - | 0.91 | 1.0 .. 71.6 | 28 / 221 | 0.30 (over the run, against the final radius) | escaped through face:+x at tick 415 |

  - S = 1 and S = 8 (expected no closed orbit: the derived speed exceeds
    the rays'): measured no push read at all in the four worlds, the probe
    off the GameBoard through +y at tick 67 (S = 1, 60 Links at 0.917 per
    interval) and 94 (S = 8, at 0.652); the first shell leaves the source
    at age 10 and reaches r = 12 near tick 31, when the probe is 18 to 27
    Links up the y axis and on no line of the fan at the moment a ray
    arrives. Measured = expected: the probe outruns the field.
  - S = 32, r = 12 (expected closed, T 180, mean radius 12 +- 1, C 1.00
    +- 0.15): measured not closed by the criterion: the angle reaches 2 pi
    at tick 229 (outside, +27 % of 180) with the return (-2, 0) (two Links
    off on x, outside the one Link) and the heading kept; the mean radius
    17.30 (outside); the radius at eighths of the turn 12.0, 16.3, 25.5,
    26.0, 22.0, 19.7, 13.9, 6.7, 10.0: an eccentric loop out to r = 26 and
    in to r = 6.7; 21 reads of 242 units over the turn (a mean of 11.5
    units per read on a momentum of 23: the kicks are whole labels of
    several rays at once when a shell passes), C 1.43 (outside); the
    probe then swings out to r = 66.6 and escapes through -x at tick 470.
    The first 31 intervals carry no field (the source starts empty), so
    the probe runs straight 7 Links up y before the first kick, part of
    the eccentricity as in the first registration.
  - S = 32, r = 24 (expected closed, T 361): measured no turn (0.91 of a
    turn): the probe falls inward to the Node beside the source (r = 1.0),
    28 reads of 221 units, and escapes through +x at tick 415; C over the
    run 0.30 against the final radius (not an orbit reading).
  - The ratio: no pair to take it of at any width (no T(24)).
- **Verdict of the second registration (history; the label along D).**
  Under the one push form no orbit closes at any width or
  radius: the S = 1 and S = 8 probes outrun the field (the derived speed
  exceeds the rays' at the label's magnitude), the S = 32 probe at r = 12
  makes one eccentric turn (229 intervals against 180, the return two
  Links off) and escapes, the S = 32 probe at r = 24 falls in. The reasons,
  with the numbers: the grain of the push is now the label of a fan ray,
  |D| units per unit of amount (1 to 8 here) and several rays at once when
  a shell passes (11.5 units per read in the mean on a momentum of 23), so
  a kick turns the momentum by up to 20 degrees; the field's burst and
  granularity and the start-up transient as before. A plainly stated
  finding for the model owner: **the magnitude of a fan ray's label grows
  with the integer length |D| of its direction**, equal amounts released
  on (1, 0, 0) and on (7, 5, 0) carrying the momenta 1 and sqrt 74; this
  is the law as designed (BEAM_LAW section 2, "momentum is content x amount
  x D") and it makes a fan source push 5.19 times harder than six headings
  at equal amounts; the open question is whether the label should be
  along the unit vector of the direction at the flight table's scale Q =
  64 (the same table as the flight, one table), which this implementation
  recommends the owner rule on (BEAM_LAW section 10, note 21;
  PROJECT_STATUS, "What is open"). Nothing was tuned; the widths and radii
  are the assignment's; the label's magnitude was not changed.
- **Model prediction re-derived under the label along the unit vector
  (2026-09-19, pinned before the runs; [the derivation](../examples/events/orbit/README.md#the-derivation-of-p-before-the-runs)).**
  The model owner decided the label along u_d, the unit vector of the
  direction at the flight table's scale Q = 64 ([BEAM_LAW section 2](BEAM_LAW.md#2-the-record-of-a-ray-and-the-world-file)
  and note 23), so the push a free probe takes from any arriving ray is
  Q per unit of amount within 1.35 %, along the ray's own line (radial
  from the source within 0.8 degrees: a central force to the fan's
  geometry), and the step rule reads the width in units of one free
  unit's label, `by_clock(age, |p|, Q x S x M + |p|)`. In those units
  L = 1 (the fan's mean |u_d| / Q is 1.0000, 0.994 .. 1.009 per
  direction), A = q L C / (2 pi) = 12 / 6.2832 = 1.910 with C = 1 from
  series C, and n = (A + sqrt(A^2 + 4 S A)) / 2 in units of the probe's
  content (the declared momentum n x 64): S = 1: n = 2.635, p = 3 (192),
  v = 0.750 per axis, faster than the rays (0.577), no closed orbit
  expected; S = 8: n = 4.979, p = 5 (320), v = 0.385, T(12) = 196, T(24)
  = 392, a kick of 64 on 320 turning 11.5 degrees per ray, marginal (the
  first registration at this grain did not close); S = 32: n = 8.831,
  p = 9 (576), v = 0.220, T(12) = 343, T(24) = 687, 6.4 degrees per ray:
  expected closed at both radii within the grain, the ratio 4. The
  criteria as first pinned (closed, T +- 15 %, the mean radius r +- 1,
  |drift| <= 1, the ratio 4 +- 15 %, C 1.00 +- 0.15); the field's burst
  (one shell per 10 intervals) and its GameBoard granularity (Nodes on no
  line from r of about 16) unchanged and the named risks.
- **Result (2026-09-19, the label along the unit vector; measured against
  expected).** The worktree of `claude/universe24-new-3ytqde` on the
  label commit, source fingerprint `0eaa589ab51cdc0a12a863cd23e535e1e8ac052e8b4f3f8facf30ef05a323c5a`, Python 3.14, headless,
  four cores; the six worlds regenerated by `make_worlds.py`; every run
  completed in 3.9 to 6.1 s with the books balanced at every tick; 12
  record checks passed, 0 failed, exit 0. The table (T the first closing
  of the angle; the drift per orbit for every closing; C on the first
  turn, or over the run where no angle closed; "end" how the run ended):

  | World | S | r | p (label units; units of m) | Closed (expected) | T (expected) | Mean radius (expected r +- 1) | Drift per orbit | Turns | r min .. max | Reads / units (label units) | C (expected 1.00 +- 0.15) | End |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | `s1_r12` | 1 | 12 | 192; 3 | no turn (no) | - (101) | - | - | 0.22 | 12.0 .. 61.2 | 0 / 0 | - | escaped through face:+y at tick 82 |
  | `s1_r24` | 1 | 24 | 192; 3 | no turn (no) | - (201) | - | - | 0.19 | 24.0 .. 64.6 | 0 / 0 | - | escaped through face:+y at tick 82 |
  | `s8_r12` | 8 | 12 | 320; 5 | no: the return (+5, 0), heading kept (no) | 198 (196) | 15.20 | +5.00 | 1.03 | 1.0 .. 60.8 | 24 / 3783 | 1.54 (the first turn: 17 reads, 3335 units) | escaped through face:+x at tick 271 |
  | `s8_r24` | 8 | 24 | 320; 5 | no turn (no) | - (392) | - | - | 0.93 | 7.1 .. 65.4 | 25 / 2425 | 0.25 (over the run, against the final radius) | escaped through face:+x at tick 449 |
  | `s32_r12` | 32 | 12 | 576; 9 | no: the return (-4, 0), heading kept (yes) | 289 (343) | 11.25 | -4.00, -2.00, +3.00, +5.04, -5.97, +8.97, -15.03 (seven turns) | 6.74 | 1.0 .. 60.2 | 307 / 49121 | 1.32 (the first turn: 34 reads, 5425 units) | escaped through face:-y at tick 2891 |
  | `s32_r24` | 32 | 24 | 576; 9 | no: the return (-13, 0), heading kept (yes) | 829 (687) | 28.27 | -13.00 | 1.46 | 5.0 .. 62.1 | 77 / 8052 | 1.27 (the first turn: 62 reads, 5954 units) | escaped through face:-x at tick 1054 |

  - S = 1 (expected no closed orbit: the derived speed 0.750 exceeds the
    rays'): measured no push read at all, the probe off the GameBoard through
    +y at tick 82 (60 Links at 0.750 per interval; the first shell reaches
    r = 12 near tick 31 when the probe is 23 Links up the y axis). Measured
    = expected.
  - S = 8, r = 12 (expected not closed, marginal; T 196 if it turned):
    measured the angle reaching 2 pi at tick 198 (inside +- 15 % of 196)
    with the return (+5, 0) (outside one Link) and the heading kept; the
    mean radius 15.20 (outside 12 +- 1); the radius at eighths 12.0, 15.0,
    20.8, 21.8, 20.0, 17.5, 10.8, 1.0, 17.0 (in to the Node beside the
    source and out again); 17 reads of 3335 label units over the turn
    (196 units of Q on a momentum of 320: several rays per read when a
    shell passes), C 1.54 (outside); then out to r = 60.8 and off through
    +x at tick 271. Not closed, as expected; one turn where the second
    registration had none.
  - S = 8, r = 24 (expected not closed): measured 0.93 of a turn, in to
    r = 7.1 and out, off through +x at tick 449; C 0.25 over the run (not
    an orbit reading). Measured = expected.
  - S = 32, r = 12 (expected closed, T 343, the mean radius 12 +- 1, C 1.00
    +- 0.15): measured **not closed by the criterion, but bound for 2891
    intervals and 6.74 turns** where the second registration escaped after
    one turn at tick 470: seven closings of the angle at the ticks 289,
    478, 694, 1027, 1363, 1691, 2653 (289, 189, 216, 333, 336, 328, 962
    intervals; the first 289 against 343 expected, -16 %, outside +- 15 %)
    with the returns (-4, 0), (-6, 0), (-3, 0), (+2, +1), (-4, +1), (+5,
    +1), (-10, 0) (every one outside one Link) and the heading kept at
    every closing; the mean radius over the turns 11.25 (inside 12 +- 1),
    7.80, 8.98, 12.98, 12.17, 13.66, 30.82; the radius at eighths of the
    first turn 12.0, 15.0, 16.6, 14.0, 13.0, 9.4, 5.0, 7.8, 8.0; the drift
    per orbit -4.00, -2.00, +3.00, +5.04, -5.97, +8.97, -15.03 (outside
    one Link); C 1.32, 1.47, 1.39, 1.45, 1.38, 1.31, 1.71 (outside 1.00
    +- 0.15, the push read about 1.4 times the derivation's mean: the
    kicks land where the probe meets a shell, inside the ring's mean
    radius more often than outside, and the derivation's C = 1 is the
    ring mean of series C); 307 reads of 49121 label units over the run;
    the seventh turn swings out to r = 60.2 and the probe leaves through
    -y at tick 2891. The motion is a precessing, eccentric, bound orbit
    about the source at the grain of the field (one shell per 10
    intervals, whole labels of 64 per ray), not the circle derived.
  - S = 32, r = 24 (expected closed, T 687): measured one closing of the
    angle at tick 829 (+21 % of 687, outside) with the return (-13, 0) and
    the heading kept, the mean radius 28.27 (outside 24 +- 1), the radius
    at eighths 24.0, 30.4, 21.0, 17.3, 23.4, 38.1, 42.5, 33.9, 11.0, C
    1.27 (outside); the probe falls in to r = 5.0 on the second turn and
    leaves through -x at tick 1054 (1.46 turns).
  - The ratio at S = 32: T(24)^2 / T(12)^2 = (829 / 289)^2 = 8.23
    (outside 4 +- 15 %; 8 would be Kepler's k = 3, but neither T is a
    closed orbit's period); at S = 8 no T(24).
- **Verdict (the third registration).** Under the label along the unit
  vector no orbit closes by the criterion (a return within one Link with
  the heading kept), at any width or radius; measured against the
  derivation: the S = 1 probes outrun the field as expected; the S = 8
  probe at r = 12 makes one turn in 198 intervals (the derived 196) and
  leaves; the S = 32 probe at r = 12, expected to close, is bound for
  2891 intervals and seven precessing turns (the first in 289 against
  343, the mean radius 11.25 within 12 +- 1, C 1.3 to 1.5) and the S = 32
  probe at r = 24 for one turn in 829 (against 687) before falling in.
  What changed against the second registration, with the numbers: the
  kick per ray is now 64 label units on 576 (6.4 degrees) along the ray's
  own line, radial from the source within 0.8 degrees, in place of |D|
  units on 23 (2.5 to 20 degrees) along the integer direction, and the
  probe stays bound six times longer; what remains, named before the run:
  the field's burst (one shell per 10 intervals, several rays per read:
  the mean read 160 label units, 2.5 rays) and the GameBoard granularity
  of the fan's lines, which together make the push read 1.3 to 1.5 times
  the ring mean and turn the circle into a precessing polygon; the
  start-up transient (31 intervals without field). Nothing was tuned; the
  widths and radii are the assignment's; the readings are registered
  outside their expectations where they fall outside.

- **Re-read under the contact through the table (2026-09-20).** `s8_r12`
  alone changes: at tick 174 the probe at the Node beside the source
  hands 251 of its y momentum to the source (one `contact` record)
  instead of keeping it, the angle then reaches 1.00 turn without
  closing (the registered closing at tick 198 with the return (+5, 0)
  is gone), C 0.30 over the run, and the probe leaves through face:+x
  at tick 260 instead of 271. The five other worlds are byte-identical
  ([validation](VALIDATION.md#the-columns-the-lifetime-the-held-content-and-the-contact-through-the-table-the-66-example-worlds-compared---2026-09-20)).
- **Re-read under the step drive (2026-09-20; measured, nothing
  pinned).** The S = 1 probes read the same (they take no push; the record's
  new fields aside).
  The four others move differently under the step drive (2026-09-20, BEAM_LAW note 17 as amended: a body's count of Links is the whole part of the distance its momentum has driven, on its own record; a body that receives a momentum begins its drive at 0 instead of stepping off its age): `s8_r12` closes one turn
  by the criterion's angle (T 226 in place of the derived 196, the
  return +7 Links, the mean radius 15.83, C 1.65), turns 1.93 times and
  leaves through face:+x at tick 571 (registered: one turn in 198, no
  closing, out at 260); `s8_r24` reverses its angle (-0.11 turns) and
  leaves through face:+x at tick 495 (0.93 turns, out at 449); `s32_r12`
  closes two turns (T 474, then 236; the returns +3, -7; the mean radii
  16.63, 10.96; C 1.29, 1.85) and leaves through face:-y at tick 1568
  (seven precessing turns, the first in 289, bound for 2891); `s32_r24`
  closes by the criterion, the return (-1, +1) with the heading kept, T
  623 against the derived 687, the mean radius 23.63 within 24 +- 1, C
  1.37, then a second turn in 464 (the return (-14, +1), the mean radius
  18.49) before leaving through face:+x at tick 1849 (one turn in 829,
  then fell in, out at 1054); T(24)^2 / T(12)^2 = 1.73 against the
  expected 4 (was 8.23). The record checks 0 failed. The verdict's clause
  "no orbit closes by the criterion at any width or radius" no longer
  holds: the S = 32 probe at r = 24 closes once; the rest of the verdict
  (the field's burst and the fan's grain turning the circle into a
  precessing polygon) stands as read ([migration](MIGRATION.md#the-step-drive-on-2026-09-20-the-count-of-links-as-the-whole-part-of-the-driven-distance)).


### A10, the width of an opening and the spread behind it, under the Beam Law (2026-09-20)

- **Confronts.** The uncertainty relation in its diffraction form: a
  plane wave through one opening of width w spreads behind it by an
  angle whose sine is about lambda / w, so that w x Delta(sin theta) is
  bounded below by a constant of the law. Asked for by the model owner
  on 2026-09-19 as the test of the detector's sensitivity (Highlights
  5.4: a detector is a set of Nodes with one record; the declared width
  is the position's uncertainty; the reading, not the GameBoard, is what is
  uncertain), under both readings a detector may declare, `wave` and
  `beam` ([BEAM_LAW section 5](BEAM_LAW.md#5-the-detectors-record-the-re-emission-the-face-detectors)).
- **Model prediction, pinned before the runs
  ([the derivation](../examples/events/heisenberg/README.md#the-derivation-before-the-runs)).**
  lambda = c x period = 8 / sqrt 3 = 4.619 Links (the lamp's turn 8 of
  64 per interval, the flight at 1 / sqrt 3). Under `wave` the record
  of w emitters one Link apart is the array factor [sin(pi w s / lambda)
  / (w sin(pi s / lambda))]^2 in s = sin theta times the fan's profile:
  below lambda a fan (w = 1: the declared fan; w = 3: FWHM 1.434 in s,
  beyond the screen), above it a beam of FWHM 0.457 (w = 9) and 0.152
  (w = 27) in s, the product w x FWHM 0.886 lambda = 4.09 for w >=
  lambda. The count (the plain clicks per pixel) is the fan's profile at
  every w and never narrows (the control). Under `beam` no expectation
  for the spread; two coherent beams click n1 + n2 at phase difference
  0 and |n1 - n2| at N / 2. Named as what can break the reading: the
  Fresnel number w^2 / (lambda L) = 1.46 at w = 27 (the border of the far
  field), the discrete fan (47 directions over 161 pixels: a pixel
  receives about 0.3 w of the w emitters per interval), the phases
  quantized to 45 degrees by the integer flight times.
- **Features.** The detector set (`opening` declared as one detector of
  w Nodes; the screen as 161 one-Node detectors), the two readings, the
  re-emission on a fan, the plane wave from a row of lamps releasing on
  one heading, the face detectors (the escapes), no suspension.
- **Run.** `examples/events/heisenberg/` (eight worlds by
  `make_worlds.py`, `w<w>_<reading>`, 120 x 161 x 1 with z periodic, 350
  intervals, the model ids `rays-heisenberg-w<w>-<reading>-v1`);
  `tools/run_series.py --jobs 4`; `tools/heisenberg_readings.py` (the
  FWHM of the record over sin theta after a five-pixel moving mean, the
  count's FWHM, the weighted rms of sin theta, the product).
- **Result (2026-09-20, measured against expected).** The worktree of
  `claude/universe24-new-3ytqde` after the detector-set commit, source
  fingerprint `f3fb33607190c86c...`, Python 3.14, headless, four cores;
  every run completed with the books balanced at every tick (2.1 to 52.7
  s); 16 record checks passed, 0 failed.

  | World | w | record FWHM in sin theta (expected) | count FWHM (the fan) | record rms | count rms | w x record FWHM (expected) | clicks | cancelled |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | `w1_wave` | 1 | 0.057 (the fan) | 0.057 | 0.319 | 0.319 | 0.06 (the fan) | 5497 | - |
  | `w3_wave` | 3 | 0.049 (1.434) | 0.063 | 0.290 | 0.324 | 0.15 (4.30) | 16703 | - |
  | `w9_wave` | 9 | 0.072 (0.457) | 0.168 | 0.222 | 0.324 | 0.64 (4.11) | 50099 | - |
  | `w27_wave` | 27 | 0.185 (0.152) | 0.761 | 0.224 | 0.325 | 4.99 (4.09) | 150187 | - |
  | `w1_beam` | 1 | 0.057 | 0.057 | 0.319 | 0.319 | 0.06 | 5497 | 0 |
  | `w3_beam` | 3 | 0.063 | 0.063 | 0.324 | 0.324 | 0.19 | 16703 | 0 |
  | `w9_beam` | 9 | 0.148 | 0.148 | 0.324 | 0.324 | 1.34 | 46999 | 3100 |
  | `w27_beam` | 27 | 0.486 | 0.486 | 0.330 | 0.330 | 13.11 | 98780 | 51407 |

  - The count never narrows (measured = expected): its rms 0.32 at every
    w under both readings, the fan's own spread.
  - The record narrows under `wave` (the rms 0.319, 0.290, 0.222, 0.224
    for w = 1, 3, 9, 27; measured as expected in direction, the floor of
    single-emitter spikes and the screen's edges keeping it from falling
    further at w = 27) and not under `beam` (0.32 to 0.33).
  - The FWHM meets the expectation at w = 27 only: 0.185 against 0.152
    (+22 %, the Fresnel number 1.46 there), the product 4.99 against
    4.09; at w = 3 and 9 the measured widths (0.049, 0.072) are the
    width of the central spike of the few converging lines and not the
    lobe (1.43, 0.46), the products 0.15 and 0.64 below the constant:
    the discrete fan leaves a pixel one to three emitters per interval
    and the lobe is not formed (finding (ii), measured).
  - Under `beam` the pairing cancels 0, 0, 3100 and 51407 clicks (0, 0,
    6 and 34 %), the cancelled rays escaping; the surviving count keeps
    the fan's spread, the product growing as w: no bound. The triangle
    the owner expects between the extremes is not resolved by one to
    four rays per pixel per interval.
- **Verdict.** The `wave` record narrows with the width of the opening
  and the count does not, as the law says; the product w x FWHM reaches
  0.886 lambda within 22 % at the one width where the sparse fan lets
  the lobe form (w = 27) and is not read at the smaller widths, a limit
  of the reading (the fan's 47 directions over 161 pixels) and not a
  verdict on the law; `beam` gives no bound. Nothing was tuned. For the
  model owner: a fan dense enough that every emitter reaches every pixel
  of the lobe (about L directions per radian) or pixels declared as sets
  of several Nodes, and a screen beyond L = 160 for w = 27, before the
  constant is read at every width. The page of the run (four panels, the
  rays behind the opening and the screen's record, with the table) is in
  the session's scratchpad, not published.

- **Re-read under the `wave` threshold on the pointer's square
  (2026-09-20, issue #359 step A).** `w27_wave` alone changes: 2312 rays
  that met a screen pixel in antiphase within one interval pass (the
  pointer 0 below the threshold 1) where until now they clicked and added
  0 to the record, and, going on, click at other pixels and on the faces
  (face:+x 0 -> 408, face:+y and face:-y 12 833 -> 13 613 each; the
  escaped 25 666 -> 27 634), so 38 of the 161 pixels' records differ (the
  sum of the screen's records 0.16 % higher). The row old -> new: the
  count FWHM 0.761 -> 0.758, the count rms 0.325 -> 0.321, the record FWHM
  0.185, the record rms 0.224 -> 0.225 and the product 4.99 unchanged,
  the clicks 150 187 -> 148 131. The finding stands: the count never
  narrows and the record narrows under `wave`. The seven other worlds are
  byte-identical (no pixel of theirs read a pointer below its threshold
  with an amount at it), `two_slits` and `one_slit` alike
  ([validation](VALIDATION.md#the-wave-threshold-on-the-pointers-square-the-66-example-worlds-compared-a10-and-bell-re-read---2026-09-20)).

### A10 at a low rate, the single-click build-up (2026-09-20)

- **Confronts.** The build-up of fringes one particle at a time (Merli
  1976, Tonomura 1989, Grangier 1986: the contrast independent of the
  intensity), against the physicist's entry 5 of the law's own
  predictions (2026-09-20, Highlights 5.4: "the wave only in the
  detector: fringes need two rays of one number in one interval, so a
  screen counting single clicks shows the fan's spots, against the
  single-particle build-up of fringes (Tonomura), the test being fringe
  contrast against source rate") under the model owner's go of the same
  day ("the two runs on the law's own predictions, ... the single-click
  build-up of fringes (A10 at a low rate)") and the owner's decision on
  issue #359 (step A yes, step B no: no memory in the detector; "if A10
  at a low rate shows no build-up one click at a time, that is registered
  as the law's limit (the wave in the crowd, not in the single event)").
  A run under the [experimenter skill](../skills/experimenter/SKILL.md);
  every number a detector reading (the screen's pixels).
- **Model prediction, pinned before the runs
  ([the derivation](../examples/events/buildup/README.md#the-derivation-and-the-expectation-before-the-runs)).**
  The registered A10 world at w = 27 under `wave`
  ([A10](#a10-the-width-of-an-opening-and-the-spread-behind-it-under-the-beam-law-2026-09-20))
  with the lamps' `rate` 47 (the registered rate), 8 and 1 units per
  interval, the opening's Nodes re-emitting n units on n consecutive
  directions of the 47-fan per interval (`apportion_whole`), so the
  screen receives about 6, 1 and 0.14 rays per pixel per interval; the
  runs 420, 1200 and 7780 intervals so that the window from tick 260 (every
  pixel has clicked by 235) holds the same 172 000 clicks. Derived: the
  record of a `wave` pixel is the square of the pointer of the rays it
  clicks in one interval, so the cross terms live only in the (pixel,
  interval) cells with two or more rays: at the rate 47 every cell,
  the lobe of A10 (the narrowing 1 - rms_R / rms_C of sin theta about
  0.3); at the rate 1 almost none, R = I (the sum of every unit's own
  square, through `coherent_pointer`), no lobe. Pinned: the narrowing at
  least 0.2 at the rate 47; at the rate 1 the narrowing 0 +- 0.02 and
  R / I at the record's peak pixel 1 +- 0.02; the rate 8 reported. Nature:
  the narrowing 0.3 at every rate. Read beside: the FWHM of the record
  and of the count (A10's reading), w x FWHM, the cells with two or more
  rays and their share of the cells and of the clicks. Criteria
  (completed, the books balanced) fail the tool; the readings are
  registered inside or outside and never moved.
- **Features.** The registered A10 world (the detector set, the
  re-emission on a fan, the plane wave from a row of lamps, one-Node
  `wave` pixels) at three lamp rates; the per-interval `record` and
  `click` lines of `events.jsonl`.
- **Run.** `examples/events/buildup/` (three worlds by `make_worlds.py`,
  which calls the A10 generator and changes the rate, the ticks and the
  model id, `w27_rate47`, `w27_rate8`, `w27_rate1`, the model ids
  `rays-buildup-w27-rate<n>-v1`); `tools/run_series.py --jobs 3`;
  `tools/buildup_readings.py` (the window sums per pixel, the incoherent
  sum off `coherent_pointer`, the spread off `tools/heisenberg_readings.py`;
  `tests/test_buildup_readings.py` pins it to the engine on a 14 x 5
  plane at the rates 2 and 1: R / I = 2 and 1 exactly).
- **Result (2026-09-20, measured against expected).** The worktree of
  `claude/universe24-new-3ytqde` at the tip `9fc895a2` (the Beam Law,
  `beam-v1`), source fingerprint
  `a1b2a949ccda2194537ecae4c6ff7380642f8f7d7877c01ab0e1649ba51c5d4b`,
  Python 3.14.0rc2, numpy 2.5.3, headless, four cores; every run
  completed (55, 39, 92 s) with the books balanced at every tick; 0
  record checks failed, 2 readings inside, 1 outside, none moved. All
  DETECTOR:

  | World | rate | clicks | rays per pixel per interval | cells with 2+ rays (share of the cells, of the clicks) | record FWHM (count) | w x FWHM | record rms (count) | narrowing | R / I at the peak (at the centre y = 80) | R / I least .. greatest | Expected |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | `w27_rate47` | 47 | 172753 | 6.67 | 25921 (1.000, 1.000) | 0.184 (0.904) | 4.98 | 0.236 (0.341) | 0.307 | 5.50 at y = 80 (5.50) | 0.03 .. 5.50 | narrowing >= 0.2: inside |
  | `w27_rate8` | 8 | 171871 | 1.13 | 46174 (0.433, 0.648) | 0.075 (0.904) | 2.02 | 0.324 (0.341) | 0.052 | 2.86 at y = 80 (2.86) | 0.39 .. 2.86 | reported |
  | `w27_rate1` | 1 | 171742 | 0.14 | 10560 (0.066, 0.123) | 0.278 (0.904) | 7.51 | 0.347 (0.341) | -0.017 | 1.20 at y = 58 (0.84) | 0.43 .. 1.20 | narrowing 0 +- 0.02: inside; R / I 1 +- 0.02: outside |

  - The narrowing (the law 0.3 then 0; nature 0.3 at both): 0.307, 0.052,
    -0.017 at the rates 47, 8, 1: inside at both ends; nature's 0.3 at
    the lowest rate outside by 0.3. At the rate 1 the record's spread is
    the count's: no lobe.
  - R / I at the record's peak at the rate 1: 1.200 at y = 58, outside
    1 +- 0.02. The peak is not the lobe's centre (y = 80 reads 0.843) but
    the pixel of the most constructive coincidence of the synchronized
    comb: the lamps are in step, the 27 opening Nodes re-emit in the same
    interval on the same direction, and two directions released in
    different intervals coincide at a pixel when their flight times differ
    by the same amount, which the fan's 47-interval cycle produces for
    some pairs (6.6 % of the cells, 12.3 % of the clicks); the cross terms
    are in phase at some pixels and in antiphase at others (R / I from
    0.43 to 1.20), their sum over the screen negative, a fixed pattern and
    not a lobe. Registered outside as pinned.
  - The count's FWHM 0.904 at every rate (the shadow, the control); the
    record's 0.184 at the rate 47 (A10's 0.185, w x FWHM 4.98 against the
    law's 4.09) and 0.278 at the rate 1, the half width of the comb's
    spikes.
- **Verdict.** Fringes do not build up one click at a time in this law:
  the lobe (the narrowing 0.31) exists at six rays per pixel per interval,
  is a sixth of itself at about one, and is gone at 0.14, where nature
  builds the same lobe click by click. The law's prediction held in its
  substance (the wave is a reading of the crowd in one interval) and
  missed one letter (the record at the lowest rate is the count plus the
  rare coincidences of the synchronized comb, not the count exactly:
  spikes, no lobe). The physicist's entry 5 is registered as measured, a
  plain disagreement with nature and, by the owner's decision on #359,
  the law's limit: the wave is in the crowd, not in the single event.
  Nothing was tuned. What the law lacked: a single ray that carries
  something of the wave (a spread at the Node, deleted on 2026-09-19) or
  a memory between intervals in the detector (refused on 2026-09-20);
  nature's single particle interferes with itself, this law's single
  event does not. A follow-up without a change of law: the opening's
  fans rotated Node by Node (breaking the comb's fixed coincidences) and
  a rate of one ray on the whole screen per interval. The page of the
  run is in the session's scratchpad, not published.

- **Re-read under the `wave` threshold on the pointer's square
  (2026-09-20, issue #359 step A; after the merge of the strong force's
  commits).** All three worlds change: a pair of rays that meets a pixel
  in antiphase within one interval passes (the pointer 0 below the
  threshold 1) where it clicked with the record 0, and goes on; the
  clicks in the window fall (172 753 -> 169 855, 171 871 -> 158 878,
  171 742 -> 158 622), the cells with 2+ rays fall (the share 1.000,
  0.433 -> 0.395, 0.066 -> 0.026), the record's FWHM, the product w x
  FWHM and R / I at the peak are unchanged at every rate, and the count's
  FWHM at the rates 8 and 1 reads 0.617 and 0.600 where it read 0.904
  (the pairs that passed were the comb's own). Every verdict stands: the
  narrowing 0.292 (was 0.307, >= 0.2: inside) at the rate 47, 0.050
  (reported) at 8, -0.005 (was -0.017, 0 +- 0.02: inside) at 1, R / I at
  the record's peak 1.200 at y = 58 (outside) at 1; 0 record checks
  failed, 2 readings inside and 1 outside as before, none moved; source
  fingerprint `0b39130239c775492fe336818039801e572af6bb0128b9f8be41bcd031163228`
  ([validation](VALIDATION.md#the-wave-threshold-on-the-pointers-square-the-66-example-worlds-compared-a10-and-bell-re-read---2026-09-20)):

  | World | clicks in the window | rays per pixel per interval | cells with a click | cells with 2+ rays (share) | clicks in such cells (share) | record FWHM (count FWHM) | w x record FWHM | record rms (count rms) | narrowing (expected) | R / I at the record's peak | R / I at y = 80 | R / I over the window |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | `w27_rate47` old | 172753 | 6.665 | 25921 | 25921 (1.000) | 172753 (1.000) | 0.184 (0.904) | 4.98 | 0.236 (0.341) | 0.307 (>= 0.2: inside) | 5.498 at y = 80 | 5.498 | 0.034 .. 5.498 |
  | `w27_rate47` new | 169855 | 6.553 | 25277 | 25277 (1.000) | 169855 (1.000) | 0.184 (0.904) | 4.98 | 0.237 (0.335) | 0.292 (inside) | 5.498 at y = 80 | 5.498 | 0.073 .. 5.498 |
  | `w27_rate8` old | 171871 | 1.134 | 106737 | 46174 (0.433) | 111308 (0.648) | 0.075 (0.904) | 2.02 | 0.324 (0.341) | 0.052 (reported) | 2.862 at y = 80 | 2.862 | 0.393 .. 2.862 |
  | `w27_rate8` new | 158878 | 1.049 | 99446 | 39263 (0.395) | 98695 (0.621) | 0.075 (0.617) | 2.02 | 0.326 (0.343) | 0.050 (reported) | 2.862 at y = 80 | 2.862 | 0.616 .. 2.862 |
  | `w27_rate1` old | 171742 | 0.142 | 161182 | 10560 (0.066) | 21120 (0.123) | 0.278 (0.904) | 7.51 | 0.347 (0.341) | -0.017 (0 +- 0.02: inside) | 1.200 at y = 58 (1 +- 0.02: outside) | 0.843 | 0.429 .. 1.200 |
  | `w27_rate1` new | 158622 | 0.131 | 154622 | 4000 (0.026) | 8000 (0.050) | 0.278 (0.600) | 7.51 | 0.347 (0.345) | -0.005 (inside) | 1.200 at y = 58 (outside) | 0.843 | 0.764 .. 1.333 |

### E, the clock's redshift in space under the age reading (2026-09-20)

- **Confronts.** Whether a clock beside a mass in space slows as M / r
  under the age reading while the presence, what the push reads, falls as
  M / r^2: Einstein's pair from two readings of the same rays (the model
  owner, 2026-09-19, Highlights 5.4, "the clock beside a mass ... Go for
  it"; [BEAM_LAW section 10](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation),
  note 25: the ray's age kept whole on the record, the age moment of the
  one reading, `reads: "age"` on the clock's table entry), and whether the
  ratio of two such clocks' rates is the redshift 1 / r law. The accepted
  price of series C item 6 (the clock reads the presence, M / r^2) is
  confronted in space, where the fan dilutes as 4 pi r^2 and not as a ring.
- **Model prediction, pinned before the runs
  ([the derivation](../examples/events/redshift/README.md#the-derivation-before-the-runs)).**
  An open 31^3 cube, a fixed source of content 2^12 at the centre
  releasing one ray per self-creation on the 290 primitive directions with
  |a| + |b| + |c| <= 6 (q = 290 per interval), probes of content 1 that
  `pass` at every Node of the shells r = 4, 6, 8, 10, 12, 14 (6984
  probes), the `scalar` world counting the presence at `suspension` [1, 1]
  and the `age` world the age moment at [1, 2]. Expected: the shell mean
  of the presence q x dwell / (4 pi r^2), so k_s x r^2 constant (40 with
  the heading's dwell) within +- 15 % of its mean over r >= 6; the age of a
  ray at r about r sqrt 3, so k_a x r constant within +- 15 %, the ratio of
  the constants sqrt 3 / 2; the ratio of the age clocks' rates (1 +
  k_a(14)) / (1 + k_a(r)) against the 1 / r law fitted at r = 14 within
  15 % of the law's shift; the first-order line 1 - C (1 / r1 - 1 / r2)
  printed and expected to fail (k of 2 to 9, not a weak field); the single
  probes on the axis and the diagonals reading their line's beam (the
  presence about 2 whatever r), the laws living in the shell means; the
  fraction of a shell's probes counting anything falling to about 0.2 at
  r = 14. Criteria (completed, the books balanced) fail the tool; the
  readings are registered inside or outside their expectation and never
  moved.
- **Features.** The age whole on the record and read modulo the period by
  the flight; the age moment of the one reading and `reads: "age"` on a
  table entry; the clock's count off the clock from what it counted
  (`Measured.counted`, `measured.count_component`); `pass` probes (no push,
  no record, the count read); the free release on a declared fan in space;
  the face detectors; the world key `age_bound` at its default (the flight
  bound of the 31^3 cube doubled).
- **Run.** `examples/events/redshift/` (two worlds by `make_worlds.py`,
  `scalar` and `age`, 300 intervals each), the model ids
  `rays-redshift-<kind>-space-v1`; `tools/run_series.py --jobs 2`;
  `tools/redshift_readings.py` (the shell means over the window 100 to 300
  by a replay of the world through the API, the single probes, the
  redshift ratios).
- **Result (2026-09-20, measured against expected).** The worktree of
  `claude/universe24-new-3ytqde` on the age commit, source fingerprint
  `cd90313373651164e7f1a1e5f2d0f5019356cd5fb4bc9d3f909511b4f783be52`,
  Python 3.14.0rc2, numpy 2.5.3, headless, four cores; both runs completed
  in 16 s with the books balanced at every tick; 0 record checks failed,
  11 readings inside, 3 outside, registered, none moved.

  | r | direction | k scalar | k age | k scalar x r^2 | k age x r | expected |
  | --- | --- | --- | --- | --- | --- | --- |
  | 4 | shell (210 Nodes) | 2.521 | 8.748 | 40.34 | 34.99 | reported (many lines per Node) |
  | 6 | shell (450) | 1.092 | 5.711 | 39.30 | 34.27 | 41.5 +- 15 % and 36.1 +- 15 %: inside, inside |
  | 8 | shell (762) | 0.700 | 4.904 | 44.82 | 39.23 | inside, inside |
  | 10 | shell (1250) | 0.416 | 3.657 | 41.56 | 36.57 | inside, inside |
  | 12 | shell (1814) | 0.297 | 3.097 | 42.74 | 37.17 | inside, inside |
  | 14 | shell (2498) | 0.199 | 2.366 | 38.99 | 33.12 | inside, inside |
  | 4 | +x, (1, 1, 0), (1, 1, 1) | 1.000 | 3.545 | 16.0 | 14.2 | the line's beam (the grain) |
  | 6 | +x / (1, 1, 0) / (1, 1, 1) | 2.030 / 1.000 / 0 | 10.77 / 4.88 / 0 | 73.1 / 36.0 / 0 | 64.6 / 29.3 / 0 | the beam; the diagonal Node off every line |
  | 8 | +x / (1, 1, 0) / (1, 1, 1) | 2.030 / 1.000 / 0 | 13.29 / 7.33 / 0 | 129.9 / 64.0 / 0 | 106.3 / 58.7 / 0 | the beam; off every line |
  | 10 | +x / (1, 1, 0) / (1, 1, 1) | 1.985 / 1.000 / 1.000 | 17.18 / 8.52 / 9.00 | 198.5 / 100.0 / 100.0 | 171.8 / 85.2 / 90.0 | the beam |
  | 12 | +x / (1, 1, 0) / (1, 1, 1) | 1.985 / 0 / 1.000 | 21.22 / 0 / 10.11 | 285.9 / 0 / 144.0 | 254.7 / 0 / 121.3 | the beam; the (1, 1, 0) Node off every line |
  | 14 | +x, (1, 1, 0), (1, 1, 1) | 1.000 | 11.50 | 196.0 | 161.0 | the beam (one interval's dwell at that Link) |

  - k_s x r^2 (expected constant): 39.0 to 44.8 over r = 6 to 14, the mean
    41.5, the ripple +- 7 %: inside at every r >= 6. Measured = expected:
    the fan dilutes as the shell's Nodes in space.
  - k_a x r (expected constant): 33.1 to 39.2, the mean 36.1, the ripple
    +- 9 %: inside at every r >= 6; the ratio of the constants 0.870
    against sqrt 3 / 2 = 0.866. Measured = expected: the clock beside the
    mass reads M / r from the same rays whose presence reads M / r^2.
  - The redshift (expected the 1 / r law within 15 % of its shift): the
    measured ratios rate(r) / rate(14) = 0.3453, 0.5015, 0.5701, 0.7227,
    0.8215 at r = 4 to 12 against the law 0.3627, 0.5162, 0.6548, 0.7805,
    0.8951 (C = 33.12 fitted at r = 14; 0.3570, 0.5101, 0.6492, 0.7763,
    0.8928 with C the shell mean 36.07): inside at r = 6, outside at
    r = 8, 10, 12 (the deviations 0.085, 0.058, 0.074 on shifts of 0.345,
    0.220, 0.105), the ripple of k_a x r entering the ratio (1 + k_ref) /
    (1 + k_r) whole while the shift shrinks as 1 / r - 1 / 14; the form is
    the 1 / r law's (the nearer clock slower). The first-order line fails
    as expected (-4.9 to 0.6 at r = 4 to 12: k of 2 to 9 is not a weak
    field).
  - The grain (expected the beam on a line, a Node off every line reading
    0, the counting fraction about 0.2 at r = 14): measured as the table;
    the fractions 1.00, 0.63, 0.42, 0.32, 0.20, 0.17. No radius up to 14
    leaves a shell reading nothing.
  - Host cost: 16.0 s (`scalar`) and 15.5 s (`age`) per run of 300
    intervals with 6985 measured events: the age reading costs nothing
    measurable.
- **Verdict.** In space the pair holds by two readings of the same rays:
  the presence M / r^2 and the age moment M / r, their ratio the flight's
  sqrt 3 / 2. The clocks' ratio has the 1 / r law's form and misses the
  pinned 15 %-of-shift criterion at three radii by the ripple of the shell
  means; a weak-field confrontation (k << 1: a larger `suspension`
  denominator or a smaller q) is the follow-up for the model owner.
  Nothing was tuned.

### G, the Hubble diagram behind the detector (2026-09-20)

- **Confronts.** The model owner's question (2026-09-20, Highlights 5.4,
  "DECIDED: series G"): "let it check whether what is observed today is
  also seen in our detector." Sources thrown from a centre with a spread
  of momenta, each a family of its own releasing rays with its phase; a
  detector at the centre reads, per source, the redshift (the rate at
  which the pointer of its record turns against the emitter's own rate)
  and the distance (the age of the arriving rays, the flight time); the
  curve of redshift against distance is compared in shape with what is
  observed today (the linear law near, and far the supernova curve of an
  accelerating recession, q about -0.55) and with the two curves the law
  can give, a coasting recession (the Milne form, q = 0) and a
  decelerating one (the push of the crowd, q > 0). The orchestrator's
  expectation, flagged before the run: the redshift is the Doppler of the
  throw and the clocks' rates, the Hubble law comes out by itself, nothing
  in the law gives an acceleration, and the age clock is the one reading
  that could bend the curve. A run under the
  [experimenter skill](../skills/experimenter/SKILL.md): every number
  labelled a detector reading (the record of the detector's set or of a
  measured event) or a GameBoard reading (the host's view: a source's
  position, steps, momentum, the books); the diagram and its fits are
  detector readings only.
- **Model prediction, pinned before the runs
  ([the derivation](../examples/events/hubble/README.md#the-derivation-before-the-runs)).**
  An open 301^3 cube, twenty-four free sources (a family each) on chains
  of four along the six axes at r_0 = 3, 5, 7, 9 Links, the speeds v = c x
  V(axis) x (2 i - 1) / 7 with V = 0.6 .. 0.35 (0.05 c to 0.6 c, c = 32 /
  55 Links per interval read off the flight table; `width` 2^20, the
  momenta p = Q S M v / (1 - v)), each releasing one row per self-creation
  toward the centre with its clock's phase (the turn 1 step per
  self-creation, K = M) and nothing outward; a detector of one Node at the
  centre (the paid family `detector`, `wave`, every entry `{"rule":
  "measure", "reads": "age"}`); six masses inside at one Link releasing
  outward. Two crowds: coasting (rows of 1, the masses of content 1) and
  pushing (rows of 16, the masses 64 per self-creation, the net pull on
  rank i being i x 16 per interval inward); two clocks: the emitters'
  clocks counting the presence (`suspension` [1, 2^12]) or the age moment
  ([1, 2^19]); 400 intervals, the record read over [100, 200), [200, 300)
  and the registered late window [300, 400). Expected: 1 + z = (1 + k)(1 +
  v / c) within 2 % (k the emitter's clock, v its speed, both from the
  record); the coasting throw the Milne form z = H tau / (1 - H tau) with
  H t_0 = 1 within 10 % (t_0 the window's centre) and q = 0 the nearest of
  the three exact forms at the near fit's H with rms below 0.02 (the
  initial distances shifting it by r_0 / c in tau); the pushing throw
  decelerating, H t_0 < 1, q_eff > 0 and the accelerating form the
  farthest; the bend of the age clock reported, no bracket; what is
  observed today (q = -0.55 the nearest) expected outside in every run.
  Criteria (completed, the books balanced) fail the tool; the readings are
  registered inside or outside and never moved.
- **Features.** The free release on one heading stamping the clock's
  phase; the momentum step of a free measured event with the width of the
  push; the push of a free row on a reader (kappa = -M_A) and a fixed
  reader's momentum; `wave` on a set of one Node with the age moment on
  the click record (`reads: "age"`); the clock's count of the presence or
  the age moment; `pass` on the masses; the face detectors (nothing left).
- **Run.** `examples/events/hubble/` (four worlds by `make_worlds.py`,
  `coasting_scalar`, `coasting_age`, `pushing_scalar`, `pushing_age`, the
  model ids `rays-hubble-<crowd>-<clock>-space-v1`); `tools/run_series.py
  --jobs 4`; `tools/hubble_readings.py` (the pointer's turn per detector
  interval by a least-squares slope of the `record` lines' unwrapped
  phases, the ages off the click records, m(tau) and c off the engine's
  `flight_table`, the replay for the checks; `tests/test_hubble_readings.py`
  pins it to the engine on a bar). The first throw of the series, with a
  row released outward from every source and the detector's event as the
  mass inside, is in git before the registered worlds; it found that a
  source stepping into the Node of its own row takes it home and that the
  detector's clock, reading `age` beside every arrival, paced the mass's
  release down to 0.29 (the README).
- **Result (2026-09-20, measured against expected).** The worktree of
  `claude/universe24-new-3ytqde` at the merge of the charge per unit of
  content (`b9a0e6c6`), source fingerprint
  `5a93868357b564b3c0448e04db424eaf3acb1617e1ab1a448a42989e88481776`,
  Python 3.14.0rc2, numpy 2.5.3, headless, four cores; every run completed
  in 36 to 37 s with the books balanced at every tick; 0 record checks
  failed, the reading's formula 288 of 288 inside, 22 pinned readings
  inside and 26 outside, none moved. The late window, t_0 = 350 (detector
  readings unless marked; the full table per source in the README):

  | Reading | coasting (scalar = age) | pushing scalar | pushing age | Expected |
  | --- | --- | --- | --- | --- |
  | z of the slowest and the fastest source (mz1, px4) | 0.0496, 0.6001 | 0.119, 0.604 | 0.092, 0.619 | v / c 0.05, 0.60 times the clock |
  | rms of z - v / c declared (GameBoard, the throw) | 0.003 | 0.034 | 0.028 | - |
  | k of the emitters' clocks (rank 1 .. rank 4) | 0 | 0.02 .. 0.07 / 0.004 .. 0.035 | 0 .. 0.05 / 0 .. 0.05 | small |
  | (1 + z) / ((1 + k)(1 + v / c)), 24 sources | 0.995 .. 1.005 | 0.994 .. 1.007 | 0.992 .. 1.008 | within 2 %: 72 of 72 inside |
  | H t_0, the near fit | 1.029 inside (0.875, 0.949 at t_0 = 150, 250) | 1.292 outside | 1.120 outside | coasting 1 +- 10 %, pushing < 1 |
  | rms far at the near H: q = +0.5 / 0 / -0.55 | 0.153 / 0.066 / 0.021 | 0.432 / 0.223 / 0.142 | 0.219 / 0.106 / 0.052 | coasting q = 0 nearest, < 0.02; pushing -0.55 farthest |
  | best-H rms: q = +0.5 / 0 / -0.55 | 0.007 / 0.008 / 0.012 | 0.037 / 0.032 / 0.030 | 0.028 / 0.027 / 0.029 | - |
  | q_eff of the free quadratic | 4.6 | -0.55 outside | 3.7 inside | pushing > 0 |
  | the momentum left, p(400) / p(0), ranks 1 .. 4 (GameBoard) | 1.03 .. 1.00 | 0.68 .. 0.79, 0.85 .. 0.91, 0.89 .. 0.94, 0.91 .. 0.96 | the same | coasting 1, pushing < 1 |
  | the Doppler part alone, H t_0 (after the runs, not pinned) | 1.024 | 0.918 | 0.990 | - |
  | the nearest of the three at the near H | q = -0.55 outside | q = -0.55 outside | q = -0.55 outside | outside in every run |

  - The reading's formula: 288 of 288 inside over the three windows; the
    coasting worlds read z = v / c declared to 0.003 and tau to 1.3
    intervals of the throw's own form (r_0 + v t_0) / (c + v); their clocks
    counted nothing (k = 0), so `coasting_scalar` and `coasting_age` read
    alike to the last digit.
  - The linear law: H t_0 = 0.875, 0.949, 1.029 at t_0 = 150, 250, 350
    (outside, inside, inside): the Hubble time is the age of the throw
    once the initial distances are small against it.
  - The coasting form: inside at t_0 = 150 (q = 0 the nearest; its rms
    0.026 outside), outside at 250 and 350, where q = -0.55 is the nearest
    (0.018, 0.021 against 0.033, 0.066): every source reads the Milne form
    shifted by its own r_0 / c, and the far sources' r_0 is three times
    the near ones', so at the near fit's H the far part lies below the
    coasting form, the accelerating form's signature. With H free per form
    the three fit within 0.005 of one another.
  - The decelerating form: on the GameBoard every pushing source
    decelerated (p(400) / p(0) from 0.68 at rank 1 to 0.96 at rank 4, the
    inner ranks losing the larger fraction as derived) and the Doppler
    part of the reading fell with it (v / c from the record 0.04 .. 0.58);
    the detector's curve nevertheless read H t_0 > 1 in five of six
    pushing windows, q_eff > 0 in five of six, and the accelerating form
    the nearest of the three in all six: outside on every count but
    q_eff. The cause is the emitters' clocks: the inner ranks sit in the
    thickest part of the crowd's rays and their clocks run slowest (k up
    to 0.07 with the scalar clock), which reddens the near part and
    inflates the near fit's H. The Doppler part alone (the clock removed;
    printed after the runs) reads H t_0 = 0.80 .. 0.99 in all six windows
    and q = +0.5 or 0 the nearest in four of them.
  - The bend of the age clock (reported): zero in the coasting crowd; in
    the pushing crowd z_age - z_scalar from -0.089 to +0.081 per source,
    no monotone bend, within the grain of the step rule (about 0.03 in z
    per hundred-interval window).
  - What is observed today: the accelerating form q = -0.55 is the nearest
    of the three at the near fit's H in ten of the twelve windows (all but
    the coasting first window): outside the expectation in every run but
    that one.
  - Host cost: 36 to 37 s per run of 400 intervals (about 6 000 rows in
    flight, 31 measured events, the 301^3 GameBoard's per-interval arrays);
    the tool with the replay 3 minutes.
- **Verdict.** The detector reads the linear Hubble law by itself, z =
  v / c to 0.003 and H t_0 = 1.03 at t_0 = 350 in the coasting throw, the
  Hubble time the age of the throw. At large distance its curve falls
  below the coasting form of its own near fit in every run, and of the
  three forms the one observed today, q = -0.55, is the nearest in ten of
  twelve windows; but nothing accelerates on the GameBoard (the coasting
  momenta within 3 %, the pushing momenta down by 4 to 32 %). The
  resemblance comes from what the detector cannot see: the throw's initial
  distances in the coasting throw (an exact, parameter-free coasting form
  fits) and the emitters' clocks in the pushing crowd (the near ones
  slowest); with H free per form the three forms agree within 0.005 in z,
  so the shape at this precision does not tell q = +0.5 from 0 from -0.55.
  The age clock bends nothing beyond the grain. Nothing was tuned. What
  the law lacked (the README): a straight throw off the axes (the step
  rule, x before y before z); a three-dimensional gravity of a crowd of
  points (a beam does not dilute, a fan's lines miss the Nodes off them);
  a source that releases along its own motion without taking its row home;
  emitters' clocks that count only their own crowd (the reading's factor
  1 + k is the model's); and a step rule whose whole part does not cluster
  under a changing momentum.
- **Follow-up (the physicist's review of the verdict, 2026-09-20; the
  runs unchanged, nothing pinned, nothing moved).** The tool's
  `--from-one-point` option fits every window again with each source's
  tau reduced by (r_0 / c) / (1 + z), the exact equivalent of a coasting
  throw from the centre (a source from r_0 at v is the source from the
  centre at the time -r_0 / v), and prints what the near fit itself reads
  off an exact coasting form at the window's taus. Found: (i) the near fit
  through the origin on z <= 0.2 reads an exact coasting throw from one
  point, with no offset at all, as H t_0 = 1.10 to 1.15 (the Milne
  curvature (H tau)^2 read as a larger H: the "near" part reaches H tau =
  0.16), so the far part of the coasting form itself lies below the
  coasting form at that H and q = -0.55 is "the nearest" for a pure
  coasting throw: the criterion "the nearest of the three at the near
  fit's H" cannot tell a coasting throw from an accelerating one, and the
  ten of twelve windows are the criterion's bias, not a signature; (ii)
  the initial distances depress every source below the Milne form of H =
  1 / t_0 by (r_0 / c) / (t_0 - tau), 0.016 at rank 1 to 0.074 at rank 4
  at t_0 = 350, and pull the near fit down (0.83, 0.93, 0.98 for the exact
  throw at t_0 = 150, 250, 350), the two biases nearly cancelling in the
  late window (1.03 read); (iii) from one point the coasting readings lie
  on the Milne form with H t_0 = 1.01 to 1.04 at a best-H rms of 0.0045
  to 0.0056 in z, the accelerating form within 0.001 of it and the
  decelerating one at 0.012 to 0.013: at this range (z <= 0.6) and grain
  (0.003 in z, 1.3 intervals in tau) the reading tells q = +0.5 from q =
  0 but not q = 0 from q = -0.55 (the exact forms with H free differ by
  0.0055 rms in z, and by 0.009 to 0.012 against q = +0.5); a fifth run of
  the coasting world with r_0 = 2, 3, 4, 5 (the review's scratchpad, not
  registered) read H t_0 = 0.98, 1.03, 1.09 and q = -0.55 "the nearest" in
  all three windows, as the exact throw predicts; (iv) in the pushing
  worlds the emitters' clocks add k / (v / c) = 0.8 to the near sources
  against 0.1 to the far ones (the scalar clock, t_0 = 350), inflating the
  near fit's H by 1.08 to 1.41 over the Doppler part; the Doppler part
  from one point reads H t_0 3 to 11 % below the coasting run's by the
  same method (the deceleration, as derived) and the best-H form q = 0 in
  four of six windows, q = -0.55 by 0.001 or less in the other two, at an
  rms of 0.009 to 0.017 (the step rule's grain).
  The surprise is a limit of the reading and an artefact of the world, not
  a finding of the law; the register keeps the verdict above as read.
- **Re-read under the step drive (2026-09-20; measured, nothing
  pinned).** Every source is a lamp whose recoil changes its momentum at
  every self-creation, so all four worlds move differently under the step drive (2026-09-20, BEAM_LAW note 17 as amended: a body's count of Links is the whole part of the distance its momentum has driven, on its own record; a body that receives a momentum begins its drive at 0 instead of stepping off its age),
  by little: the near fit's H t_0 in the windows [100, 200), [200, 300),
  [300, 400) and [200, 400) reads 0.877, 0.969, 1.017, 0.996 in both
  coasting worlds (registered 0.875, 0.949, 1.029, 0.985), 1.144, 1.182,
  1.305, 1.292 in `pushing_scalar` (1.079, 1.072, 1.292, 1.235) and
  0.866, 0.932, 1.057, 1.036 in `pushing_age` (0.912, 1.017, 1.120,
  1.060); the throw's own coasting form against the reading rms 0.0034
  in z (0.0033) and 1.3 intervals in tau; the detector's own clock over
  the run 0.8275, 0.9950, 0.2925, 0.9800 self-creations per interval
  (0.8300, 1.0000, 0.3000, 0.9750). Of the three forms, q = -0.55 is the
  nearest in 8 of the 12 windows (10 of 12 registered): `pushing_age`
  now reads q = 0 the nearest in [100, 200) and [200, 300). 309 readings
  inside and 27 outside (310 and 26); the reading's formula 288 of 288
  inside 2 %. The verdict and the follow-up stand as read ([migration](MIGRATION.md#the-step-drive-on-2026-09-20-the-count-of-links-as-the-whole-part-of-the-driven-distance)).


### H, Bohr's lines behind the detector (2026-09-20)

- **Confronts.** Whether Bohr's lines come out by themselves behind the
  detector once a body's phase is tied to its momentum (the model owner,
  2026-09-20, Highlights 5.4: "Bohr should come out by itself behind the
  detector; what is missing on the GameBoard by the laws?"; the answer: the
  tie between a body's momentum and its phase that E = h f gives a
  released ray; "DECIDED: On Bohr, go, and put it as parameters outside
  the GameBoard like the age"): an electron that is a body on a set of three
  Nodes ([BEAM_LAW note 30](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)
  (i), the physicist's proposal 1) and turns its phase by its momentum at
  every Link it steps (note 30 (ii), proposal 5, the world key `action`,
  the identity `bohr-v1`), about a fixed proton, releasing rays that carry
  its phase to the open faces of the GameBoard, the `wave` detectors that
  receive what comes out of the atom (proposal 6: the coherent record of
  those rays over many turns adds in line only for an orbit whose phase
  closes). The owner's rule of the page: to show atoms no detector is
  needed; a detector receives their radiation, if it comes out.
- **Model prediction, pinned before the runs
  ([the derivation](../examples/events/bohr/README.md#the-derivation-before-the-runs-gameboard-readings-of-the-design)).**
  Two free families, `p` (content 1836, `charge` [1, 1], fixed at the
  centre of an open cube of 2 (r + 14) + 1 Nodes a side, releasing one
  ray per direction of the physicist's shell of 2616 primitive directions
  with 1016 <= |D|^2 <= 1032 every 10 intervals) and `e` (content 1836,
  `charge` -15: electricity 15 times gravity), the electron a free body at
  (c + r, c, c) of `span` [1, 1, 3] with the tangential momentum p of the
  derivation, `phase_by_momentum` under the action h, releasing one ray
  per in-plane heading every 10 intervals; `suspension` 0, `width` 45120
  (v = 0.06 at r = 8), K 2^30, N 64. Derived from the engine's own flight
  lines (the entries per shell the body's three Nodes receive, E_body(r)):
  the orbit's p, v, T per radius; the closure 4 p(r) r = j h (the turn by
  momentum sums |p_axis| over the Links stepped, 4 p r on a circle of the
  GameBoard against the circle's 2 pi p r) with h = 16 p(8) so that j = 2 at
  r = 8: j = 0.946 (r = 2), 1.463 (4), 1.725 (6), 2.000 (8), 2.555 (12),
  2.873 (15), 3.248 (16); the fan's ring flux falls as about r^-1.83 and
  is not smooth at r >= 13, so j = 3 falls between the GameBoard radii 15
  and 16. Expected: an orbit closed (the return within r / 4 at the
  closing of the angle, T within 15 %), the phase's turn per orbit whole
  at a closing radius; the coherence ratio of the faces' records (the
  cumulative coherent pointer squared over the sum of the per-turn
  squares, through the engine's `coherent_pointer`) C(T) >= T / 2 after
  T >= 2 turns at a closing radius (the record growing as T^2) and C(T)
  < 2 between (bounded); the closing radii in the ratio of j^2; fewer
  than two closed turns: no coherence reading, the finding is the orbit.
  Named before the runs as what could break the orbit: the whole-kick
  lumps every 10 intervals (12 to 204 per orbit), the fan's ring
  anisotropy, the close pass. Criteria (completed, the books balanced)
  fail the tool; the readings are registered inside or outside their
  expectation and never moved.
- **Features.** A body on a set of Nodes with one record (`span`); the
  turn by momentum (`action`, `phase_by_momentum`); the charge per unit of
  content and the push as one product; the free release on a declared fan
  in space; the face detectors' `wave` records and `click` lines; the
  `step` line's phase; `suspension` 0.
- **Two kinds of readings.** DETECTOR: the faces' cumulative records, the
  clicks of the electron's rays with their phases, the electron's own
  `read` records (its pushes taken). GAMEBOARD: the orbit from the
  electron's `step` lines (the turns, T, the return, the mean radius, the
  escape), the body's phase at each closing, the design's numbers. Bohr's
  lines are a detector reading; the orbit's r, T and closure describe the
  mechanism. The owner's standing principle of the same day, "Our laws are
  on the GameBoard; in the detector one sees other laws" (Highlights 5.4):
  the turn by momentum is a GameBoard rule, a generic key on the body's
  phase, and Bohr's rule is a law of the detector's world, so the series
  compares the faces' records with Bohr's lines and never the turn's form
  with Bohr's form.
- **Run.** `examples/events/bohr/` (seven worlds by `make_worlds.py`,
  `r<r>` for r in 2, 4, 6, 8, 12, 15, 16, 3000 to 10300 intervals each),
  the model ids `rays-bohr-r<r>-space-v1`; `tools/run_series.py --jobs 4`;
  `tools/bohr_readings.py` (every line labelled by its kind).
- **Result (2026-09-20, measured against expected).** The worktree of
  `claude/universe24-new-3ytqde` on the turn-by-momentum commit, source
  fingerprint `d29df4af8cfd79512d827d32df7b885948b2a90a4865cf1993b01bb74b76095c`,
  Python 3.14.0rc2, numpy 2.5.3, headless, four cores; every run completed
  in 19 to 87 s with the books balanced at every tick; 0 record checks
  failed; of the two coherence readings taken, 1 inside and 1 outside,
  registered, none moved; five worlds gave no coherence reading (fewer
  than two closed turns).

  | World | r | j (kind) | Expected | Turns of the angle | Closings: T (derived) | Mean radius | Return (Links) | r min .. max | End | Phase turn per orbit, the fraction (design) | C(2), slope | Verdict |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | `r2` | 2 | 0.946 (closing) | C >= T / 2 | 1.47 | 1: 79 (117) | 1.74 | 1.0 | 1.0 .. 16.3 | face:-x at 254 | - | - | no reading: fell to the Node beside the proton, thrown out |
  | `r4` | 4 | 1.463 (between) | C < 2 | 1.28 | 1: 138 (294) | 2.66 | 2.0 | 1.0 .. 18.4 | face:+y at 540 | - | - | no reading: fell inward, thrown out |
  | `r6` | 6 | 1.725 (between) | C < 2 | 0.89 | 0 | - | - | 4.5 .. 25.6 | face:+x at 1045 | - | - | no reading: no turn |
  | `r8` | 8 | 2.000 (closing) | C >= 1.0 | 2.15 | 2: 722, 736 (838) | 8.11, 7.95 | 5.0, 4.0 | 3.0 .. 27.8 | face:+y at 1864 | 0.234 (0.000) | 0.84, 1.66 | outside |
  | `r12` | 12 | 2.555 (between) | C < 2 | 0.95 | 0 | - | - | 12.0 .. 28.2 | face:+x at 2097 | - | - | no reading: no turn |
  | `r15` | 15 | 2.873 (between) | C < 2 | 2.88 | 2: 1640, 2291 (2022) | 14.36, 18.67 | 8.1, 12.0 | 1.0 .. 40.3 | face:+x at 4683 | 0.188 (0.873) | 0.52, 2.78 | inside (two eccentric turns only) |
  | `r16` | 16 | 3.248 (between) | C < 2 | 1.24 | 1: 2917 (2040) | 22.12 | 5.0 | 8.0 .. 31.6 | face:+y at 3568 | - | - | no reading: one wide turn |

  The turns of the angle, the closings, the radii, the returns, the ends
  and the phase's turn per orbit are GAMEBOARD readings; C and the slope
  are DETECTOR readings (the four side faces pooled, the per-face values
  in the tool's output); the ends are the electron's own click on the face.
  - The orbit (expected closed within r / 4, T within 15 %): measured no
    orbit closed by the criterion at any radius. At r = 8, the reference,
    the two turns kept the mean radius (8.11, 7.95 against 8) with T 14 %
    short (722, 736 against 838, outside), returned 5 and 4 Links off
    (outside r / 4 = 2) on an eccentric loop from r = 3 to 28, and the
    close pass of the third turn threw the electron out through face:+y.
    The other radii fell inward (r = 2, 4, 15: to the Node beside the
    proton at r = 2 and 15) or swung outward (r = 6, 12, 16) within the
    first turn or two and escaped. The electron's own reads (DETECTOR):
    the mean inward push per interval on the GameBoard at r = 8 was 40 600 in
    units of Q per unit of content against the derivation's 39 660 (1.02):
    the mean flux the body reads is the derived one; the orbit is broken
    by the lumps (84 per orbit of 4.3 degrees at r = 8) and the close
    pass, not by the mean push.
  - The phase's turn per orbit (expected 0 beyond whole circles at r = 8):
    measured 0.234 of a circle over the one pair of closings, the
    eccentric loop's sum of |p_axis| over its Links being 12 % more than
    the circle's 4 p r; at r = 15, 0.188 against the design's 0.873.
  - The coherent record (expected C(T) >= T / 2 at r = 8): C(2) = 0.84 and
    the slope 1.66 over the two turns, outside (the per-face C 0.32, 1.52,
    0.93, 0.82); at r = 15 C(2) = 0.52, inside the bounded bracket, over two
    turns of different radii, which is not the reading the design meant.
    No ladder of closing radii was read.
- **Verdict.** The finding is the orbit, registered and not tuned: with
  the electron on three Nodes the mean push reads as derived and the
  reference orbit holds its mean radius for two turns, but no orbit closes
  well enough for the coherence reading, so Bohr's lines were not read
  behind the detector in this series, neither for nor against. What the
  law lacked here is not the turn (it turned as pinned in
  `tests/test_nature_beam_body.py` (d)) but a stable closed orbit under whole
  kicks: the next step, for the model owner, is a smoother field (a shell
  every interval at the same emission, or a larger `width` for more lumps
  per orbit), the orbit tilted out of the GameBoard plane (the physicist's
  1.6 bound turns at one Node), or a body of 27 Nodes (`span` [3, 3, 3]);
  and the second reading of the owner's page contract, a lamp shooting a
  beam at the atom (absorption: a paid family's rays aimed at the
  electron's set, the electron's table entry for that family with a
  threshold and a phase window as the coherence condition between the
  beam's phase and the electron's own, a `wave` detector behind the atom,
  a control without the atom, the fraction taken against the beam's phase
  rate), is registered as the next step with this design, not run.
  Nothing was tuned.

- **Re-read under the contact through the table (2026-09-20).** `r2`
  and `r4` change, the electron beside the proton handing its momentum
  component to it instead of keeping it: `r2` takes 7 hand-overs (from
  tick 72), turns 2.07 times with two closings (T 84 and 166, mean
  radii 1.74 and 2.66), reads the phase's turn per orbit 0.688 against
  the design's 0.946 and C(2) = 0.60 (outside), and leaves through
  face:+x at tick 688 instead of face:-x at tick 254; `r4` takes one
  hand-over at tick 454 and leaves through face:+y at tick 600 instead
  of 540, its one closing the same. The verdict stands: no orbit closed
  well enough for the coherence reading. `r6`, `r8`, `r12`, `r15` and
  `r16` are byte-identical ([validation](VALIDATION.md#the-columns-the-lifetime-the-held-content-and-the-contact-through-the-table-the-66-example-worlds-compared---2026-09-20)).
- **Re-read under the step drive (2026-09-20; measured, nothing
  pinned).** Every world changes under the step drive (2026-09-20, BEAM_LAW note 17 as amended: a body's count of Links is the whole part of the distance its momentum has driven, on its own record; a body that receives a momentum begins its drive at 0 instead of stepping off its age); the design, the widths and
  the radii are the assignment's. `r2` closes once (T 262, the mean
  radius 3.62), turns 1.64 times and leaves through face:-y at tick 410
  (registered under the contact: two closings, C(2) = 0.60, out at 688);
  `r4` closes twice (T 459 and 1074, the mean radii 5.21 and 11.62), one
  return within 0.25 r, C(2) = 1.38 (inside the between radius's bound),
  out through face:+y at 1871 (one closing, out at 600); `r6` closes
  three times (597, 1088, 550), C(3) = 0.52, out through face:-y at 2682
  (no closing, out at 1045); `r8`, the design's closing radius j = 2,
  closes four times (T 944, 588, 1209, 1281; the mean radii 8.84, 6.50,
  11.45, 13.15; three returns within 0.25 r) and is on the GameBoard at
  the end of 4200 intervals, the phase's turn per orbit 0.828, 0.750,
  0.797 of a circle beyond whole circles against the design's 0, C(4) =
  1.01 against the expected T / 2 = 2.0 (outside; two closings, C(2) =
  0.84, out at 1864); `r12` closes five times (1454, 1658, 1416, 1334,
  1290; the mean radii 12.46, 13.68, 11.97, 11.66, 11.37; r from 9.4 to
  15.7), every return within 0.25 r, on the GameBoard at the end of 7400,
  the phase's turn 0.609, 0.250, 0.141, 0.078 against 0.555, C(5) = 0.49
  (inside, bounded; 0.95 turns and out at 2097); `r15` closes once (T
  2291) and leaves through face:-x at 3597 (two closings, out at 4683);
  `r16` turns 0.48 and leaves through face:-x at 1851 (one closing, out
  at 3568). The ladder takes no ratio (fewer than two closing radii with
  two turns; was r = 8 / r = 2 = 4.00). 3 readings inside and 1 outside
  (1 and 2). What changed in the finding: the orbit at r = 8 and r = 12
  now holds for the run with returns within a quarter radius, so the
  verdict's "what the law lacked here is a stable closed orbit under
  whole kicks" is answered by the step rule, not by a smoother field; the
  coherence reading at the closing radius stays outside (C(4) = 1.01
  against 2.0, the phase's turn per orbit not 0), so Bohr's lines are
  still not read behind the detector, neither for nor against ([migration](MIGRATION.md#the-step-drive-on-2026-09-20-the-count-of-links-as-the-whole-part-of-the-driven-distance)).


### I, the nucleus (2026-09-20)

- **Confronts.** Whether the one mechanism of the model owner's decisions
  of 2026-09-20 (Highlights 5.4: "one mechanism for all the laws on the
  GameBoard", the one coupling a signed inner product over the columns a
  family declares per unit of content; "the strong force's range is a
  lifetime, L"; the contact through the table, on the physicist's design
  of the strong force) gives a nucleus: a deuteron bound at one Link and
  free at three (the square well's depth and width), two protons bound or
  repelled by the sign of `Q^2 - G^2 - M^2` (the binding condition `G^2 +
  M^2 > Q^2`), Coulomb's repulsion less gravity beyond the reach, and
  which four-nucleon shape holds, the square p n / n p or the line p n n
  p (the alpha's shape). Read at the nucleons themselves, external things
  whose `read` and `contact` records and steps are the readings; no
  detector is declared on these GameBoards.
- **Model prediction, pinned before the runs
  ([the expectations](../examples/events/nucleus/README.md#the-expectations-pinned-before-the-runs-the-physicists-integers)).**
  Three free families without a phase circle, `p` (charge 4), `n` and
  `nuclear` (the column `strong` with the value G = 10000 and the sign
  minus, `lifetime` 3); a proton 1836 of `p` holding one unit of `nuclear`
  (M 1837, Q 7344, G 10000), a neutron 1839 of `n` holding one (1840, 0,
  10000); every body a free body releasing one row of its held content per
  direction of the 290 primitive directions with |a| + |b| + |c| <= 6 per
  interval; an open 21^3 GameBoard, `suspension` 0, `width` 2^28, K 2^20,
  N 64, 3000 intervals; the contact through the table. The push per
  interval between two bodies at mirror Nodes within the reach is `(Q_A
  Q_B - G_A G_B - M_A M_B) x U(r)` per unit per direction (U(1) = 3008 on
  the axis, the sum of the x components of the 57 unit vectors whose
  first step is along it). Expected (the physicist's integers): the
  deuteron at one Link reads 310 967 280 640 per interval on each body
  toward the other (the `n` rows 1837 x 1839 x 3008, the `nuclear` rows
  (10^8 + 1837) x 3008) and never steps, the label 0 after every
  hand-over and the largest hand-over about 7 x 10^12, the border
  `lifetime` clicking 290 rows per body per interval from tick 4; at
  three Links no strong ray is read, gravity alone 1 067 524 788, and the
  pair kicked outward by 10^12 separates beyond 10 Links and never
  returns (the same kick at one Link outweighed by tick 5); two protons at
  one Link attract by 148 716 220 864 and hold, at G = 7000 repel by 4 691
  779 136 and separate (the first step within 200 intervals), at three
  Links repel by 15 977 466 864 from tick 6 and separate (the first step at
  tick 30 .. 60, the design's steady toy); the square p n / n p reads the
  designed push per body (p1 (355 957 892 670, 320 048 730 393, 0) and the
  mirrors) and a shear of 49 090 283 970 per row per interval (the p-p
  diagonal bond weaker than the n-n one by exactly Q^2 x U_d), a proton
  steps within the first hundred intervals and the cluster disperses; the
  line p n n p holds (the push on its first proton 403 332 137 616, no
  step in 3000 intervals, the label 0 after every hand-over). A record
  check (completed, the books balanced at every tick) fails the tool; the
  readings are registered inside or outside their expectation and never
  moved. Cut for the budget: I7 (the clock beside the nucleus, the
  binding energy as a clock rate), I8 (the cube of 64, the drip of Z), I9
  (the core family and He-5) and I10 (the lifetimes across three fans).
- **Features.** The columns of the one coupling (`columns`, `columns-v1`),
  the lifetime of a family and the border `lifetime`, the content a
  measured event holds of several families (`held`), the contact through
  the table (`contact` records); the free release on a declared fan in
  space; the free body's step off its clock with the width of the push;
  `suspension` 0.
- **Run.** `examples/events/nucleus/` (eight worlds written by
  `make_worlds.py`, the model ids `beam-nucleus-<name>-space-v1`),
  `tools/run_series.py --jobs 3`, 3000 intervals each; the readings by
  `tools/nucleus_readings.py` (every line labelled DETECTOR or GAMEBOARD).
  The worktree of `claude/universe24-new-3ytqde` on the commits of the one
  mechanism (the columns `de6c4968`, the lifetime and the held content
  `7a77fa0c`, the contact `b2c164c2`), source fingerprint
  `a86447318c757023605e4ba33ab1ef1a15726fef839b893d5d50b899750188f5`,
  Python 3.14.0rc2, numpy 2.5.3, headless, four cores; every run completed
  in 4 to 87 s with the books balanced at every tick; 0 record checks
  failed; 29 readings inside, 1 outside, none moved.

  | World | Expected (kind) | Measured | Verdict |
  | --- | --- | --- | --- |
  | `deuteron_1` | the push on p 310 967 280 640 toward n, the mirror on n (DETECTOR); no step; the label 0 after every hand-over, the largest 10^12 .. 10^13 (DETECTOR); 290 border clicks per body per interval from tick 4 (DETECTOR) | 310 967 280 640 (the `n` rows 10 161 754 944, the `nuclear` rows 300 805 525 696) and -310 967 280 640; no step in 3000; 191 hand-overs on p from tick 16 and 148 on n from tick 32, the label 0 after each, the largest 7 152 247 454 720; 580 clicks per interval from tick 4 | inside (6 of 6) |
  | `deuteron_3` | no strong read; gravity 1 067 524 788 on p (DETECTOR); separates beyond 10 Links, never returns, both out (GAMEBOARD) | 0 strong reads; 1 067 524 788 (n reads -1 067 523 840); the first steps at tick 34 outward, 3 to 19 Links, n out through face:+x at 285, p through face:-x at 358 | inside (4 of 4) |
  | `deuteron_1_kick` | the kick 10^12 outweighed by the pushes read by tick 5 (DETECTOR); no step; the first refused step toward the other | tick 5 on both; no step; 190 hand-overs on p from tick 13 (the largest 9 329 018 419 200), 147 on n from tick 138 | inside (3 of 3) |
  | `pp_1` | the push 148 716 220 864 toward the other (DETECTOR); no step; the label 0 after every hand-over | 148 716 220 864 (the `nuclear` rows 300 805 525 696, the `p` rows -152 089 304 832) and the mirror; no step; 171 hand-overs on p1 from tick 16, 0 after each, the largest 7 138 378 601 472 | inside (3 of 3) |
  | `pp_1_weak` (G 7000) | the push -4 691 779 136, repulsion (DETECTOR); separates, never returns; the first step within 200 intervals (GAMEBOARD) | -4 691 779 136 (the `nuclear` rows 147 397 525 696) and the mirror; the first steps at tick 167, 1 to 19 Links, out through face:+x at 334 and face:-x at 379; 169 strong reads per body before the reach was passed | inside (3 of 3) |
  | `pp_3` | the push -15 977 466 864 from tick 6, no strong read (DETECTOR); the first step at tick 30 .. 60; separates, never returns (GAMEBOARD) | -15 977 466 864 and the mirror; 0 strong reads; the first steps at tick 66; 3 to 19 Links, out at 269 and 282 | 3 of 4 inside: the first step at tick 66, outside the steady toy's 30 .. 60 (the pushes begin at tick 6 and the fan's lines arrive over the next ticks, which the toy lacked) |
  | `alpha_square` | the push per body at L = 3 as designed (DETECTOR); the shear 49 090 283 970 per row per interval (GAMEBOARD); a proton's step within 100 intervals; disperses beyond 3 Links (GAMEBOARD) | p1 (355 957 892 670, 320 048 730 393, 0), n2 (-405 048 176 640, 376 205 857 440, 0), n3 and p4 the mirrors; the rows' x pushes -49 090 283 970 and +49 090 283 970; p4 steps +y at tick 57, n3 at 63, n2 at 70, p1 at 84; n3 out through face:+x at 180, p4 face:+y at 236, p1 face:-y at 393, n2 face:-x at 538; the largest separation 23.6 at the end; 3, 11, 8 and 4 hand-overs, 0 after each | inside (4 of 4) |
  | `alpha_line` | the push on p1 403 332 137 616 on x (DETECTOR); no step in 3000; the label 0 after every hand-over | 403 332 137 616 (n 13 702 153 608, nuclear 405 607 450 872, p -15 977 466 864), on n2 108 358 928 000; no step; 257, 247, 11 and 251 hand-overs, 0 after each, the largest 16 500 521 232 560 (the toy's number) | inside (3 of 3) |

  The pushes, the hand-overs and the border's clicks are DETECTOR
  readings (the bodies' own records); the steps, the separations and the
  shear are GAMEBOARD readings (the bodies' `step` records, the sums over
  a row).
- **Verdict.** The one mechanism gives what the design said, integer by
  integer: the deuteron is bound at one Link and free at three (a square
  well of depth 3.1 x 10^11 per interval and width two Links: the strong
  reading is the electric reading's own 1 / r^2 with the opposite sign and
  a cut at the reach, no Yukawa tail); two protons bind or repel by the
  sign of `Q^2 - G^2 - M^2` (a threshold at G = 7111); beyond the reach
  Coulomb's repulsion less gravity remains; the contact through the table
  gives a bound pair bounded books (the labels handed over and 0 after
  each hand-over). The model's alpha is the line p n n p, not the square:
  the square's rows are sheared apart by exactly Q^2 x U_d per interval, a
  proton leaves at tick 57 and the four disperse by tick 538, while the
  line holds for 3000 intervals with every hand-over cancelled by its
  mirror. The readings of the worlds with contacts (the deuterons, the
  pairs, the square, the line) are readings of the declared order of the
  bodies: the frame steps the bodies in number order, a declared tie
  (BEAM_LAW note 31 (ix); the closing gate's finding G1, 2026-09-20), so
  a permutation of the measured events moves the holder of a hand-over
  and, in the square, which neutron leaves first; the sum of the momenta
  and the verdicts (bound at one Link, free at three, the line rigid and
  the square sheared) do not depend on it. The engine's flight delays and the fan's lumps moved one number
  outside the steady toy's bracket (the first step of two protons at three
  Links) and none of the designed pushes. What the law lacked, as read
  here: a bond that resists shear (the bonds are central pushes and the
  contacts frictionless; nature's alpha is a tetrahedron), the exclusion
  principle (a fifth nucleon binds by one bond wherever it is added; not
  run), a binding energy in the content (no mass defect; the clock's count
  under a suspension is the one reading that can carry it, I7, not run)
  and a spread of decay times (I10, not run). None is a defect of the
  column, the lifetime or the contact. Nothing was tuned. The page for the
  model owner: the scratchpad's `nucleus/nucleus.html` with the frame
  player of `nucleus.gif` (the square dispersing, one frame per 5
  intervals), published by Boss.
- **Re-read under the step drive (2026-09-20; measured, nothing
  pinned).** Every world changes under the step drive (2026-09-20, BEAM_LAW note 17 as amended: a body's count of Links is the whole part of the distance its momentum has driven, on its own record; a body that receives a momentum begins its drive at 0 instead of stepping off its age), the DETECTOR pushes at
  tick 20 the same wherever the bodies have not moved: `deuteron_1` 169
  hand-overs on p from tick 16 and 158 on n from tick 17, the largest
  4 664 509 209 600 (191 and 148, the largest 7 152 247 454 720), no step,
  6 of 6 inside; `deuteron_3` the first steps at ticks 33 and 34, out
  through face:-x at 346 and face:+x at 311 (34; 358 and 285), inside;
  `deuteron_1_kick` the kick outweighed by tick 5, no step, 168 and 157
  hand-overs from ticks 19 and 20 (190 from 13 and 147 from 138),
  inside; `pp_1` no step, 119 hand-overs on p1 from tick 23 and 115 on
  p2 from tick 24 (171 on p1, none on p2), inside; `pp_1_weak` the first
  steps at tick 118, out at 364 and 345, 120 strong reads per body (167;
  379 and 334; 169), inside; `pp_3` the first steps at tick 68 (66), the
  one reading outside as before; `alpha_square` disperses sooner, p4
  stepping +x at tick 15, n2 at 22, p1 and n3 at 31, out through face:-y
  at 125, face:+y and face:+x at 133, face:+x at 177 (57, 63, 70, 84;
  180 to 538), so at tick 20 the bodies are no longer the design's square
  and its two readings at that tick (the push per body, the shear) fall
  outside, the dispersal inside; `alpha_line` holds, no step, 230, 190,
  140 and 230 hand-overs, the label 0 after each, the largest
  7 380 392 774 624 (257, 247, 11, 251; 16 500 521 232 560, the toy's
  number). 27 readings inside and 3 outside (29 and 1). The verdict
  stands: bound at one Link, free at three, the line rigid and the square
  sheared ([migration](MIGRATION.md#the-step-drive-on-2026-09-20-the-count-of-links-as-the-whole-part-of-the-driven-distance)).


### K, light beside a mass (2026-09-20)

- **Confronts.** The bending and the delay of light by a mass (Eddington
  1919: 1.75 arcseconds at the Sun's limb, 4 G M / (b c^2); the Shapiro
  delay, Cassini 2003; lensing), against the physicist's entry 2 of the
  law's own predictions (2026-09-20, Highlights 5.4, "the physicist's
  design of the weak force and the list of the law's own predictions":
  "light is neither bent nor delayed by a mass, since no rule lets a ray
  in transit read the crowd, a plain disagreement") under the model
  owner's go of the same day ("go on everything; just make sure again
  that it is good and generic": "the two runs on the law's own
  predictions, light beside a mass (series K) ..."). The derivation says
  the law disagrees with nature; the run decides, and the derivation may
  be wrong. A run under the
  [experimenter skill](../skills/experimenter/SKILL.md): every number
  labelled a detector reading or a GameBoard reading; the comparison with
  nature uses detector readings only.
- **Model prediction, pinned before the runs
  ([the derivation](../examples/events/lensing/README.md#the-derivation-before-the-runs)).**
  An open 57 x 41 x 41 box, a lamp of the paid family `light` at
  (2, 20 + b, 20) (the turn 8, lambda = 4.65 Links) releasing one unit
  per interval on each of five directions within 5 degrees of (1, 0, 0),
  a fixed mass of the free phase-less family `m` at the centre releasing
  on series E's fan of 290 directions (one ray per direction per interval
  at M = 2^12, two at 2^13), a screen of 1681 one-Node `wave` pixels at
  x = 54 with `reads: "age"` for `light` and `pass` for `m`, `suspension`
  0 (no clock slowed: the flight alone is read); a control without the
  mass, the mass at b = 6, twice the mass at b = 6, the mass at b = 3.
  Derived: the collision acts per family's store and per (number,
  content) class (`nature_beam.collide`), so a ray of the beam and a ray
  of the mass never enter one slot state and the table's mean deflection
  of a beam ray meeting a radial ray is exactly 0 (the rule does not act;
  were they one class, "+x +y" is fixed and only a head-on pair moves,
  which the geometry never forms); no other rule reads the crowd for a
  ray's step. Expected at every M and b: the deflection of the arrival's
  centroid off the beam's axis 0 within 0.5 pixel (y and z), the mean age
  of the arrivals the control's within 1 interval (the flight table's 89
  and 90 intervals), the count the control's within 1 % (the beam clears
  the mass in every world), the phase rate the lamp's turn 8 within 0.05.
  Nature scaled to the world: the law's equivalent of G M / (b c^2) is the
  age moment a clock reads at b (series E's form, q x dwell / (4 pi b^2)
  x b / c): 11.4 at b = 6 (22.7 for 2 M or b = 3), so nature's 4 G M /
  (b c^2) is 46 to 91 radians and 2 G M / c^2 is 137 to 273 Links, beyond
  b: nature would capture the beam; the dense crowd is kept as the
  sharper test of a coupling (the beam's Nodes hold about one ray of the
  crowd per interval). Criteria (completed, the books balanced) fail the
  tool; the readings are registered inside or outside and never moved.
- **Features.** A lamp of a paid family on a declared fan of five
  directions; a free phase-less mass on a fan in space (series E's form);
  one-Node `wave` detectors with the age moment on the click record
  (`reads: "age"`); `pass` on the screen and the lamp for the mass's rays;
  the face detectors; `suspension` 0.
- **Two kinds of readings.** DETECTOR: the screen's clicks per pixel over
  the window [110, 400] (the centroid, the width, the mean age, the first
  click, the count), the pixels' `record` lines (the phase rate), the
  faces' clicks of light, the mass's clicks of light. GAMEBOARD: the
  world replayed through `NatureBeamSimulation`: the beam's rows in
  flight, the rows at rest or off the lamp's directions (a ray a
  collision would have turned) and the Nodes holding a ray of the beam
  and a ray of the crowd in one interval (the meetings).
- **Run.** `examples/events/lensing/` (four worlds by `make_worlds.py`,
  `control`, `mass`, `heavy`, `near`, 400 intervals, the model ids
  `rays-lensing-<name>-space-v1`); `tools/run_series.py --jobs 4`;
  `tools/lensing_readings.py` (the window sums off `events.jsonl`, the
  turn and the mass's rays per direction off `by_clock`, the speed and
  the dwell off `flight_table`, the replay; `tests/test_lensing_readings.py`
  pins it to the engine on a 13 x 5 x 3 box).
- **Result (2026-09-20, measured against expected).** The worktree of
  `claude/universe24-new-3ytqde` at the tip `9fc895a2` (the Beam Law,
  `beam-v1`), source fingerprint
  `a1b2a949ccda2194537ecae4c6ff7380642f8f7d7877c01ab0e1649ba51c5d4b`,
  Python 3.14.0rc2, numpy 2.5.3, headless, four cores; every run
  completed in 6.5 to 9.9 s with the books balanced at every tick; 0
  record checks failed, 16 readings inside, 0 outside, none moved.

  | World | M | b | crowd at b: presence, age moment | clicks | deflection y, z (pixels) | width rms y | mean age (delta) | first click | count ratio | phase rate | light on the faces, taken by the mass | Expected |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | `control` | - | 6 | 0, 0 | 1455 | - | 2.828 | 89.40 | 90 | - | 8.000 | 0, 0 | the turn 8: inside |
  | `mass` | 2^12 | 6 | 1.10, 11.4 | 1455 | 0.000, 0.000 | 2.828 | 89.40 (0.00) | 90 | 1.0000 | 8.000 | 0, 0 | 0 +- 0.5, 0 +- 1, 1 +- 1 %, 8 +- 0.05: inside, inside, inside, inside, inside |
  | `heavy` | 2^13 | 6 | 2.20, 22.7 | 1455 | 0.000, 0.000 | 2.828 | 89.40 (0.00) | 90 | 1.0000 | 8.000 | 0, 0 | all inside |
  | `near` | 2^12 | 3 | 4.41, 22.7 | 1455 | 0.000, 0.000 | 2.828 | 89.40 (0.00) | 90 | 1.0000 | 8.000 | 0, 0 | all inside |

  - The deflection (DETECTOR; expected 0, nature 46 to 91 radians or the
    capture): 0.000 pixel in y and z in every world, the centroid on the
    beam's axis to the last digit; nature's value outside.
  - The delay (DETECTOR; expected 0, nature hundreds of intervals): the
    mean age 89.40 in every world, the delta 0.00, the first click at 90.
  - The count and the phase rate (DETECTOR): 1455 clicks in every world,
    the ratio 1.0000, nothing on the faces, nothing taken by the mass;
    8.000 steps per interval, no redshift of the light in flight.
  - The replay (GAMEBOARD): 447 rows of the beam in flight at most, none
    at rest, none off the lamp's directions in any world; the crowd's
    rows 13618 at most; 162 Nodes per interval (156 in `near`) holding a
    ray of the beam and a ray of the crowd: the beam crossed the crowd at
    a third of its Nodes every interval and met it nowhere, as derived.
- **Verdict.** Light is neither bent nor delayed beside a mass in this
  law, exactly (0.000 pixel, 0.00 interval, the count and the phase rate
  the control's), at a crowd where nature would capture the beam, at
  twice that crowd and at half the impact distance. The derivation held;
  the physicist's entry 2 is registered as measured, a plain disagreement
  with nature. Nothing was tuned. What the law lacked: a rule by which a
  ray in transit reads the crowd at the Node it enters (a wait per whole
  unit of presence, or a turn of its direction by the flow), removed on
  2026-09-19 to keep the flight a bijection blind to the crowd; the
  collision, the one rule that turns a ray, acts within one family and
  number only. Giving a ray a reading is the model owner's decision, not
  a parameter. The page of the run (the GameBoard as a drawing with the
  world-file names, the moving picture with a time control, the
  readings, the conclusion) is in the session's scratchpad, not
  published.

### A2 with the choosers on the GameBoard (2026-09-20)

- **Confronts.** Issue #363, the model owner's question of 2026-09-20
  ("Alice and Bob are part of the GameBoard, no?") and his go: a
  measurement, not a change of law. In A2 the settings (the counters'
  `phase_window`) are numbers in the world file, a hand from outside the
  universe, so its S = 2 is established only given a free choice from
  outside; a fully deterministic model in which everything is on the
  GameBoard is suspect of superdeterminism, the settings and the pairs
  correlated through a common past, and then S says nothing either way
  ([HYPOTHESES 11](HYPOTHESES.md#11-the-bell-prediction-of-the-ray-event-model-stated-so-that-it-can-fail)).
  Here the suspicion is measured: each counter's window is read from the
  phase of a ray arriving from a third source (Alice's) and a fourth
  (Bob's), far from each other and from the pair lamp, with no causal
  meeting between the three (different strides and starting phases, no
  suspension, every stream passing every table with `pass`); the settings
  are events of the GameBoard with a past of their own, and the question
  is whether the law carries a correlation from the shared initial state
  to things that never met. A run under the
  [experimenter skill](../skills/experimenter/SKILL.md): every number
  labelled a detector reading or a GameBoard reading.
- **Model prediction, pinned before the run (the owner's, issue #363;
  the physicist and the mathematician on A2, BEAM_LAW section 8).** S = 2
  exactly with every E on the triangle 1 - 4 k / N in the settings'
  difference, the marginals 1/2 exactly (no-signalling), the largest S
  over every quadruple of settings that occurred 2 (the triangle's own).
  Not 2: the mechanism is the first thing to find; if it is in the file
  (a shared clock, a common release) it is our tuning and not physics
  (control 3 shows what that looks like), if it is in the law it is a
  real finding. Nothing tuned after the run; S is read from the click
  lines only, binned by the window they carry.
- **Features.** One additive engine key
  ([BEAM_LAW note 34](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation);
  [ENGINE, the world](ENGINE.md#the-beam-law-beam-v1)): a table entry's
  `phase_window` as `{"reads": "<family>", "offset": s}`, the centre the
  phase of the coherent pointer of the named family's rows present at the
  set plus the offset, the width the law's, a `pass` naming `window` None
  without a setting row, the `window` used on every click
  (`tests/test_nature_beam_window_reads.py`; 21 example worlds
  byte-identical without the key, [validation](VALIDATION.md#the-choosers-on-the-gameboard-the-key-replayed-and-the-run---2026-09-20)).
  Free families with a phase circle as the streams (`sa`, `sb`), one row
  per interval from a free measured event held in place, `pass` on every
  table for them; the face detectors.
- **Run.** `examples/events/bell/` (seven worlds by
  `make_chooser_worlds.py`, whose docstring derives the design from the
  engine's flight table and `by_clock` before the run; the dictionary in
  the [README](../examples/events/bell/README.md#the-choosers-on-the-gameboard-issue-363-2026-09-20)):
  A2's bar and pair lamp (K = 15 x 2^20 so that the pair lamp's turn stays
  exactly 1 over the run), Alice's counters at 7 Links (plus, x = 7) and
  4 Links (minus, x = 4) from her lamp at x = 0, one `sa` row at each
  Node at every interval, the setting a ray's phase plus the offset; Bob's
  at 3 (plus, x = 17) and 2 (minus, x = 18) Links from his at x = 20, two
  `sb` rows each, the setting the pointer of two consecutive releases;
  the streams' phases periodic with the odd periods 5 (Alice, the turns
  12, 13, 13, 13, 13) and 3 (Bob, the turns 21, 21, 22), coprime to each
  other and to the circle, so that the two counters of a side read one
  setting per pair (the minus window the exact complement, `offset` +
  32) and every combination of settings meets every phase of the pair
  equally (the joint period 15, over 960 pairs each combination sees each
  phase once). A two-valued setting from one clock (0 / 16) is impossible
  without a period dividing 64, which would share a residue of the
  interval with the pair's phase, a correlation built by the file; the
  odd periods are the generic choice, and the quadruple read is an
  ordered one within a half circle, Alice's 0 and 25 with Bob's 8 and 29,
  on which the triangle gives 2. The settings: Alice's 0, 12, 25, 38, 51
  and Bob's 8, 29, 51 (the bisectors read with the engine's tables). The
  ages 7..1926, 1920 pairs (128 per combination), after the warm-up of 7
  pairs before the first `sa` ray reaches Alice's plus counter; 1940
  intervals. The reading `tools/bell_choosers.py` (the offsets off the
  record, the bins by the window carried on the plus counters' lines, the
  complement, one outcome per side per age, every E against the triangle,
  S on the quadruple, the largest S over every quadruple that occurred,
  the marginals; `--replay` the streams' rows at the counters, GAMEBOARD;
  `tests/test_bell_choosers.py` pins it to the engine on a minimal case).
  Controls, all registered: (1) the four `written_a<a>_b<b>` worlds, the
  same GameBoard and streams with the windows written in the file (A2's
  form) at the quadruple's settings, 128 pairs each; and A2's ten worlds
  replayed on the engine with the key, byte-identical to the registered
  run; (2) `fixed`, the streams released with the settings fixed (the
  turn 0: Alice's 0, Bob's 8); (3) `one_clock`, the three lamps fed from
  one clock (the setting lamps with the pair lamp's stride 1 and phase 0).
- **Result (2026-09-20, measured against expected).** The worktree of
  `claude/universe24-new-3ytqde` from its tip `9379b01c` with the key
  added, source fingerprint
  `38792132301970e7c276cfee4184534dcd2223fe3a4d906c78be3714afd5c142`,
  Python 3.14.0rc2, numpy 2.5.3, headless, about 5 s per 1940 intervals,
  the books balanced at every tick, the pair lamp's momentum [0, 0, 0].

  | Reading | Kind | Expected | Measured | Verdict |
  | --- | --- | --- | --- | --- |
  | The offsets (tick = age + offset) | detector | 6, 11, 13, 14 (the flight table) | 6, 11, 13, 14, one value per counter | inside |
  | The warm-up, the pairs before every counter had a setting | detector | 7 | 7 (3 of them escaped on -x, the other 4 clicked at Alice's minus) | inside |
  | The settings read | detector | Alice 0, 12, 25, 38, 51; Bob 8, 29, 51 | the same, 15 bins of 128 pairs | inside |
  | Every minus window the plus window's complement | detector | every pair | every pair | inside |
  | E per bin | detector | the triangle 1 - 4 k / 64 | E(0, 8) = 1/2 (48, 16, 16, 48), E(0, 29) = -13/16, E(0, 51) = 3/16, E(12, 8) = 3/4, E(12, 29) = -1/16, E(12, 51) = -9/16, E(25, 8) = -1/16, E(25, 29) = 3/4, E(25, 51) = -5/8, E(38, 8) = -7/8, E(38, 29) = 7/16, E(38, 51) = 3/16, E(51, 8) = -5/16, E(51, 29) = -3/8, E(51, 51) = 1: every one the triangle exactly | inside |
  | S on (0, 25) x (8, 29) | detector | 2 | E(0,8) - E(0,29) + E(25,8) + E(25,29) = 1/2 + 13/16 - 1/16 + 3/4 = 2 exactly | inside |
  | The largest S over the 5 x 3 settings' quadruples | detector | 2 | 2, on (0, 12) x (8, 29), the triangle's own | inside |
  | No-signalling: each side's marginal per own setting | detector | 1/2, equal across the other side's settings | 1/2 exactly in every one of the 15 bins | inside |
  | Control 1a: A2's ten worlds replayed with the key in the engine | detector | byte-identical, S = 2 | `events.jsonl`, `state.json`, `run.json` identical; `tools/bell_chsh.py` 326 criteria, 0 failed | inside |
  | Control 1b: the four written worlds, the streams present and unread | detector | S = 2 | E 1/2, -13/16, -1/16, 3/4; S = 2 exactly; 91 criteria, 0 failed | inside |
  | Control 2: the streams at fixed phases (0 and 8) | detector | E(0, 8) = 1/2 as A2's a0_b8 | 1/2 (48, 16, 16, 48), 24 criteria, 0 failed | inside |
  | Control 3: the three lamps fed from one clock | detector | not the triangle (a correlation built in) | 64 bins of one pair phase each, E = 1 in every bin, both plus counters clicking every pair and the minus counters never, no quadruple of settings occurring (Alice's and Bob's settings locked 13 steps apart), 68 of 214 criteria failed | seen, as it must be |
  | The streams at the counters | gameboard | one `sa` row at x = 4 and 7 at every interval from ticks 8 and 13, two `sb` rows at x = 17 and 18 from ticks 7 and 5 | as expected (`--replay`), the phases 7, 19, 32, 45, 58 and 40, 61, 18 | inside |

  46 criteria checked on the run, 0 failed; 141 on the controls 1b and 2,
  0 failed; every reading inside, none moved.
- **Verdict.** S = 2 exactly with every E on the triangle and the
  marginals 1/2, with the choosers on the GameBoard: the law does not
  correlate the settings with the pair through their common past (the
  initial state, the one clock of the intervals); when a correlation IS
  built in by the file (control 3) the same reading sees it at once.
  What A2 established given a free choice from outside is now established
  with the choice made by GameBoard events: Bell's assumption, an
  assumption in the universe, is a measurement in the model. The model's
  limit stands as it was, S = 2 against nature's 2.4 to 2.7; this run
  cleans the measurement and does not change the outcome (entanglement
  stays with #362). What the law lacked: nothing for this run. What the
  design could not do: a two-valued setting from one clock without a
  period that divides the circle; the odd periods replace it, and the
  quadruple is an ordered one within a half circle rather than the
  owner's 0/16 and 8/24. The page of the run (the GameBoard drawn with
  the three lamps and the four counters, why it was tested, the moving
  picture with a time control, the readings, the conclusion) is in the
  session's scratchpad, not published.
### K under the meeting (2026-09-20)

- **Confronts.** The same question, the bending and the delay of light by
  a mass, under the model owner's decision of the same day on the meeting
  (Highlights 5.4, "DECIDED: the meeting, M-R": "an event in transit reads
  the crowd as a body does, a report, not a balance"; the physicist's and
  the mathematician's design, `scratchpad/meeting/MEETING.md`, the identity
  `meeting-v1` under the world key `meeting`;
  [BEAM_LAW section 3 step 3 and note 35](BEAM_LAW.md#3-the-nodes-interval-nature_beam)):
  every paid unit of the beam reads the mass's free crowd at each
  free-space Node it shares with it and turns toward the mass by one grain
  step of the direction table per N = 64 crowd units met, the count kept
  on its phase register, the crowd untouched. What the run reads: the
  sign, the M / b form and the grain (the smallest step on K's table is
  2.4 degrees, 10^4 times nature's 1.75 arcseconds at the Sun's limb, so
  the value is out of reach by the grain and is not claimed), the delay in
  time (none is predicted: the flight table is one speed), the phase
  offset per pixel (the crowd met along the path modulo N, the
  interferometric Shapiro reading) and a lens of two beams. Nothing was
  tuned; a reading outside its bracket is reported with its numbers.
- **Model prediction, pinned before the runs** (the design's offline
  flight of the beam beside the replayed crowd, `k_deflection.py`, the
  register N = 64; the brackets fixed in `tools/lensing_readings.py`
  before the runs): `mass` the centroid -3.0 +- 0.5 pixels in y toward the
  mass and 0 +- 0.5 in z, the width about 6.0, the mean age about 90.4
  (+- 1: the bent path's extra Links, no delay in time), about 1547 of
  1553 rays landing (the count ratio 0.996 +- 0.05), no ray on the faces;
  `heavy` -4.3 with 209 rays wrapped to the faces (+- a quarter); `near`
  -2.6 with 136; the phase offset of the arrivals about 55 steps of 64
  (`mass`, `near`: 119 and 183 crowd units met modulo 64) and 24 (`heavy`:
  216 modulo 64), +- 8 steps; the phase rate the lamp's turn 8 +- 0.05;
  the control unchanged, byte for byte; the lens world's two beams at
  +-b = 6 crossing about 70 Links past the mass, a grain of the fan and
  not a focal law (no bracket). The sign toward the mass in every world,
  the deflection growing with M at fixed b and with 1 / b at fixed M
  within the finite path.
- **Features.** The world key `meeting: true` on the four worlds of K
  (`<name>_meeting.json`, the model ids `beam-lensing-<name>-meeting-v1`)
  and the lens world `lens_meeting.json` (two lamps at y = 26 and 14 on a
  105 x 41 x 41 box, the mass at x = 28, the screen at x = 102, 600
  intervals); the books' `turned` line; the readings tool extended to the
  phase offset per pixel, the `turned` line and the centroid per lamp.
- **Two kinds of readings.** DETECTOR: the screen's clicks per pixel over
  the window [110, 400] ([110, 600] in the lens world; the centroid, the
  width, the mean age, the count, the faces, the mass's clicks of light),
  the pixels' `record` lines (the phase rate), the click records' phase
  against the lamp's phase at the birth (the offset per pixel); the lens
  world's centroid per lamp and the crossing they imply. GAMEBOARD: the
  world replayed through `NatureBeamSimulation` (the beam's rows in
  flight, the rows turned off the lamp's directions, the meetings), the
  books' `turned` line, the x where the lens world's two beams are closest.
- **Run.** `examples/events/lensing/` (`make_worlds.py` writes the five
  meeting worlds beside the four of K); `tools/run_series.py --jobs 2`;
  `tools/lensing_readings.py` (the record checks, the DETECTOR tables of
  both kinds of world and the GAMEBOARD replay; `tests/test_lensing_readings.py`
  pins it to the engine).
- **Result (2026-09-20, measured against expected).** The worktree of
  `claude/universe24-new-3ytqde` from the tip `329c5660` with the meeting's
  commits, source fingerprint
  `dc1cce964db367167732b1727d9dc8d2fcf73a27bf13e33a1822cc5a84fff1a3`,
  Python 3.14.0rc2, numpy 2.5.3, headless, four cores under the load of
  the replay of the register (the elapsed seconds are not a measurement);
  every run completed (17.6, 36.5, 28.9, 29.0 and 55.2 s for `control`,
  `mass`, `heavy`, `near` and `lens`) with the books balanced at every
  tick; 0 record checks failed, 14 readings inside, 9 outside, none moved.

  | World | M | b | clicks | centroid y shift (expected) | z | width rms y | mean age (expected) | count ratio (expected) | light on the faces (expected) | light the mass took | phase offset, steps (expected), resultant | phase rate | verdicts |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | `control` | - | 6 | 1455 | 26.000 (0) | 20.000 | 2.828 | 89.40 (89.40) | - | 0 (0) | 0 | 0.0 (0), 1.00 | 8.000 | phase rate, phase offset: inside |
  | `mass` | 2^12 | 6 | 1350 | -1.790 (-3.0) | 0.000 | 3.907 | 89.90 (90.43) | 0.928 (0.996) | 0 (0) | 122 | 19.7 (55), 0.09 | 8.191 | centroid y outside; z inside; delay inside; count outside; faces inside; offset outside; rate outside |
  | `heavy` | 2^13 | 6 | 1242 | -4.359 (-4.3) | 0.000 | 5.277 | 90.64 (90.64) | 0.854 (0.858) | 210 (209) | 1 | 34.3 (24), 0.21 | 7.101 | centroid y, z, delay, count, faces inside; offset outside; rate outside |
  | `near` | 2^12 | 3 | 1237 | -2.301 (-2.6) | 0.000 | 4.470 | 89.71 (89.72) | 0.850 (0.901) | 77 (136) | 169 | 62.3 (55), 0.31 | 11.273 | centroid y, z, delay, offset inside; count outside; faces outside; rate outside |
  | `lens` | 2^12 | +-6 | 3958 | -6.255 and +6.255 per lamp: the crossing 71.0 Links past the mass (about 70) | - | - | 173.89 | - | 2 | 394 | 56.3, 0.58 | 6.364 | a grain, registered without a bracket |

  - **The sign** (DETECTOR): toward the mass in every world, the centroid
    at smaller y (-1.79, -4.36, -2.30 pixels), 0.000 in z. Inside.
  - **The form** (DETECTOR): at twice the mass the engine reproduced the
    offline flight almost integer by integer (-4.36 against -4.29; 210
    rays on the faces against 209; the age 90.64 against 90.64; the width
    5.28 against 5.28): inside. At half the impact distance -2.30 against
    -2.59: inside. At (2^12, 6) -1.79 against -3.0: outside, and the count
    ratio 0.928 against 0.996 outside, for one reason the offline flight
    did not have: the mass is a measured event whose table measures a paid
    arrival, and 122 rays of the beam, the most turned ones, clicked on it
    (the flight let a ray pass through the mass's Node and land far down
    the screen); in `near` 169 clicked on the mass and 77 reached the faces
    where the flight wrapped 136 to the faces, so its count and faces read
    outside too; in `heavy` the rays wrap to the faces before they reach
    the mass's x (1 taken).
  - **No delay in time** (DETECTOR): the mean age moved by the extra Links
    of the bent digital lines, +0.50, +1.24, +0.31 intervals against the
    control (the expected 90.43, 90.64, 89.72): inside in all three; the
    flight table is one speed.
  - **The phase offset** (DETECTOR): 0.000 exactly at every pixel of the
    control (the check of the reading); under the meeting sharp at every
    lit pixel (the resultant 0.92 to 0.98 at the nine most lit pixels of
    `mass`, 0.71 to 1.00 in `near`, 0.30 to 0.90 in `heavy`) and tens of
    steps apart from pixel to pixel (in `mass` 15.5, 51.8, 38.9, 23.2, 19.9,
    48.2, 24.5, 4.9, 12.4 at (29, 20), (25, 20), (23, 20), (27, 20), (16,
    20), (24, 20), (28, 20), (18, 20), (17, 20)), so the screen-wide
    circular mean (19.7, 34.3, 62.3) has a small resultant (0.09, 0.21,
    0.31) and reads outside the expected 55 and 24 in `mass` and `heavy`,
    inside in `near`. The expectation "about 55 steps" was the mean crowd
    met over all the rays; a pixel is reached by the rays of one path, and
    the crowd met differs from path to path: the interferometric Shapiro
    reading is per path, and an interferometer of two paths would read
    their difference. 182, 40 and 146 click groups of several rows were
    left out of the offset (their ages cannot be told apart on the record).
  - **The phase rate** (DETECTOR): 8.191, 7.101, 11.273 against the turn
    8 +- 0.05, outside in the three mass worlds, 8.000 in the control. Not
    a redshift: the tool's estimator is the least-squares slope of a
    pixel's unwrapped `record` phases, and under the meeting a pixel's
    pointer mixes rays of different offsets from interval to interval, so
    the unwrapping adds spurious turns; the per-click offsets above, with
    their resultants, are the clean reading, and they say the phase is the
    lamp's plus a constant per path. Registered outside as the bracket
    was set; the estimator's limit is named, the bracket not moved.
  - **The lens** (DETECTOR): the two beams' centroids at the screen 74
    Links past the mass at y = 19.745 and 20.255, the shifts -6.255 and
    +6.255 toward the mass's line, 0.51 pixel apart: on a straight flight
    after the mass each crosses the line 71.0 Links past it (the expected
    about 70), a grain of the fan. The mass took 394 of the two beams' rays
    over 600 intervals, 2 reached the faces, the mean age 173.89. GAMEBOARD:
    the two beams' mean lines are closest at x = 86.1 on average over the
    window, 58 Links past the mass (49 to 101 from interval to interval).
  - **The replay** (GAMEBOARD): the beam's rows in flight 447 at most in
    `mass` (462 in `heavy`, 441 in `near`, 1662 in the lens world), none at
    rest; rows on a direction off the lamp's five 21290 row-intervals over
    the run in `mass` (54452, 29893, 175638) seen at 233 (559, 340, 1480)
    Nodes; the Nodes holding a ray of the beam and a ray of the crowd in
    one interval 164.9 per interval on average (190.7, 166.9, 413.8); the
    crowd's rows 13618 at most (15501 in the lens world). The books'
    `turned` line of `light` at the end: (-8016, -85088, 0) in `mass`,
    (-142936, -215752, 0) in `heavy`, (-102000, -112152, 0) in `near`,
    (-32448, 0, 0) in the lens world (the two beams' y turns cancel), 0 in
    the control; the y component toward the mass, a report as `pushed` is.
  - **The control** (DETECTOR, GAMEBOARD): every reading the control's of
    series K, and `control_meeting`'s `events.jsonl` is byte-identical to
    the control's replay (the sha256 `22ec156b13a2aa21...`): the key
    without a crowd does nothing.
  - **The cost** (host): `mass` stepped in-process for 400 intervals on an
    idle machine, 19.9 ms per interval without the key and 24.5 ms with
    it, the meeting 4.6 ms per interval (1.8 s over the run) for 13618
    crowd rows and 447 rows of the beam, 67 permutations built in the
    whole run at 0.58 ms each (0.04 s in all; the targets a beam meets
    repeat); the elapsed seconds of the series above were taken under the
    replay's load and are not a measurement.
- **Verdict.** Under the meeting light is bent toward a mass with the
  sign of gravity, the M / b form and the grain of the fan (the sign in
  every world; twice the mass and half the impact distance inside their
  brackets; the lens crossing 71 Links where about 70 was expected), it is
  not delayed in time (the ages the bent path's) and not redshifted (the
  phase the lamp's plus a sharp offset per path); the grain is the law's
  limit, 10^4 times nature's angle, so the value is not claimed. What the
  engine added that the offline flight lacked: the mass measures the
  light that reaches it, so at (2^12, 6) the most turned rays click on
  the mass (122) and the centroid reads -1.79 where -3.0 was expected,
  outside; at b = 3 (169 taken) the count and the faces read outside for
  the same reason. The interferometric Shapiro phase is per path, not per
  screen: the expectation of one offset was the mean over rays, and the
  per-pixel offsets are sharp and different; the phase-rate estimator is
  not clean under the meeting and its three readings outside are the
  estimator's, not the light's. Nothing was tuned. The register keeps the
  physicist's entry 2 as it was measured without the key, and this entry
  as the reading under it. The page of the run (the GameBoard as a
  drawing, the moving picture of `mass_meeting` against the control with
  a time control, the readings, the conclusion) is in the session's
  scratchpad, not published.
### J, the weak force (2026-09-20)

- **Confronts.** The model owner's decision of 2026-09-20 (Highlights 5.4,
  "Arrange the weak force according to our world, and check whether we
  predict more things"; "DECIDED: go on everything; just make sure again
  that it is good and generic"): the weak force in the world's terms, in
  the recommended order of the physicist's design (scratchpad/weak/WEAK.md):
  the neutrino first with the table-entry key `phase_width` and no change
  of law (J2), then the transformation `become` with the identity
  `weak-v1` (J1, J3), then the W world. Under the owner's standing
  principle, "our laws are on the GameBoard; in the detector one sees
  other laws": the GameBoard gets the generic mechanism only, and the laws
  of nature (the cross-section's rise with energy, the half-life law) are
  compared with detector readings only, never with a rule of the
  GameBoard.

**J2, the neutrino's passage through a filled bar (the neutrino first, no
change of law).**

- **Model prediction, pinned before the runs
  ([the expectations](../examples/events/weak/README.md#the-expectations-pinned-before-the-runs-the-physicists-integers)).**
  A window admits the w consecutive steps of the circle about its setting
  whatever the ray's amount, content or emitter's rate, so the fraction
  admitted of a source of stride s coprime to N is exactly w / N (WEAK.md
  1.2; `weak_integers.out` 1.2: 10 of 640 at w = 1, N = 64), and a reader
  behind an identical reader finds no ray of its residue left. A bar of
  200 x 1 x 1, K 4096, N 64, `release` [1, 4096], `suspension` 0, 1037
  intervals; a fixed source of the free family `nu` (a phase circle, no
  charge, no content on its rays) of content 4096 at x = 0 releasing one
  ray per self-creation on +x with the stride 1 (the turn 4096 / 4096) or
  2 (K 2048); 128 fixed readers of the paid family `d` at x = 8 .. 135
  measuring `nu` under a window; a far detector at x = 190 measuring
  without a window. The first reader's arrivals over the run are exactly
  1024 (the rays born at the ticks 1 .. 1024; the first-arrival age at 8
  Links is 13 off the flight table); 711 rays reach 190 Links within the
  run (the age 326). Expected: `j2_filter` (every centre 0, width 1) the
  first reader 16 of 1024 exactly, the 127 behind it 0, the far detector
  699 (63 / 64); `j2_ladder` (the centre x mod 64, width 1) the readers at
  x = 8 .. 71 16 each and the rest 0, the far detector 0; `j2_default`
  (the half circle) 512 of 1024 at the first reader, the far detector
  352; `j2_stride2` (K 2048, width 1) 32 of 1024, the far detector 688
  (31 / 32); `j2_stride2_odd` (the centre 1) no click at any reader, the
  far detector 711. Against nature (PREDICTIONS entries 7 and 8, the
  law's own): a fraction flat in the emitter's rate where nature's
  cross-section rises linearly with the neutrino's energy, and a filter
  where nature attenuates exponentially in the depth; both registered as
  the law's limits, nothing tuned.
- **Features.** The window's width `phase_width` (BEAM_LAW note 36 (i);
  `tests/test_window_width.py`); the free release at the world's rate; the
  clock's turn as the stride.
- **Run.** `examples/events/weak/` (the five `j2_*.json` worlds written by
  `make_worlds.py`, the model ids `beam-weak-j2_<name>-v1`),
  `tools/run_series.py --jobs 4`, 1037 intervals each; the readings by
  `tools/weak_readings.py` (every line labelled DETECTOR or GAMEBOARD).
  The worktree of `claude/universe24-new-3ytqde` from its tip `6a596b34`
  on the commit of the window's width, source fingerprint
  `55f30af0309c2812646384a0caf4d16a956e5ae525df878a008c6bf075e90941`,
  Python 3.14.0rc2, numpy 2.5.3, headless, four cores; every run
  completed in about 3 s with the books balanced at every tick; 0 record
  checks failed; 13 readings inside, 0 outside, none moved.

  | World | Expected (kind) | Measured | Verdict |
  | --- | --- | --- | --- |
  | `j2_filter` | the first reader 16 of 1024, exactly 1 / 64 (DETECTOR); the 127 behind it 0 (DETECTOR); the far detector 699 of the 711 that reach it (DETECTOR; the 711 GAMEBOARD, off the flight table) | 16 of 1024; 0 at every reader behind; 699 | inside (3 of 3) |
  | `j2_ladder` | the readers at x = 8 .. 71 take their residue, 16 each, the readers at 72 .. 135 nothing (DETECTOR); the far detector 0 (DETECTOR) | 64 readers clicked, x = 8 .. 71, 16 each; the far detector 0 | inside (2 of 2) |
  | `j2_default` | the first reader 512 of 1024, the half circle (DETECTOR); nothing behind (DETECTOR); the far detector 352 (DETECTOR) | 512 of 1024; 0 behind; 352 | inside (3 of 3) |
  | `j2_stride2` | the first reader 32 of 1024, 1 / 32 (DETECTOR); nothing behind (DETECTOR); the far detector 688 (DETECTOR) | 32 of 1024; 0 behind; 688 | inside (3 of 3) |
  | `j2_stride2_odd` | no reader clicks (DETECTOR); the far detector 711 (DETECTOR) | 0 at every reader; 711 | inside (2 of 2) |

- **Verdict (J2).** The detector's world sees a cross-section where the
  GameBoard has a stride: the admitted fraction is w / N exactly, a
  deterministic residue and not a lottery, the same at every rate of the
  emitter (the window reads the phase alone; a free ray carries no
  content), and a slab of identical readers is a filter set by the spread
  of its centres, not an attenuation set by its depth (the ladder of 64
  centres exhausts the beam; 64 more readers behind it read nothing). Both
  are the law's own predictions against nature (entries 7 and 8): the
  flat cross-section a plain disagreement with the linear rise, the
  filter a difference that nature could test with two identical detectors
  behind a source of one clock. Nothing was tuned; no law changed. The
  page for the model owner: the scratchpad's `weak_impl/weak.html`,
  published by Boss.

**J1, the free neutron's decay count against its clock, and J3, the bound
neutron (the transformation `become`, the identity `weak-v1`).**

- **Model prediction, pinned before the runs
  ([the expectations](../examples/events/weak/README.md#j1-and-j3-the-neutrons-decay-against-its-clock),
  `examples/events/weak/expectations.json`, written by the generator).**
  The clock trigger fires at the self-creation whose clock reaches `at`
  (BEAM_LAW note 36 (iii)); at the suspension [1, 2^20] a clock that
  reads a constant count c at every self-creation owes `by_clock(a, c,
  2^20)` after each, and the sum over the ages 0 .. at - 1 telescopes to
  floor(at x c / 2^20), so the self-creation that takes the age to `at`
  is the tick at + floor(at x c / 2^20) (WEAK.md 2.4, `weak_integers.out`
  7.1); a neutron alone counts nothing and fires at `at` exactly. The
  generator pinned each neutron's tick from the count its clock read at
  tick 100 of a warm run of the same world without its `become` keys (a
  GAMEBOARD reading of the engine's own presence), the reading inside
  when the neutron fires at that tick or up to three intervals before it
  (the crowd's build-up), never after. J1: 64 neutrons of the register's
  `n` (content 1839, fixed, no strong unit held) on a lattice of pitch 4
  (4 x 4 x 4) about the centre of an open 41^3 GameBoard, K 2^20, N 64,
  `release` [1, 1], `suspension` [1, 2^20], each with `become` at 512
  into `p` (the charge 4 per unit on the content 1836) with the products
  `beta` (1, 3; the charge -7344 per unit of amount against `p`'s 4 x
  1836: the register's scale of series I) and `nu` (1, 0), each passing
  every family; a shell of the paid family `d` at r = 18 (the 4170 Nodes
  within a half Link of 18) as one `beam` detector set measuring `beta`
  with `reads` `age` and passing everything else; 650 intervals (the
  design's 512 neutrons at `at` 2048 cut to 64 at 512 for the record's
  budget: the law is linear in the key, the reading its ratio). Expected:
  `j1_lattice` (the neutrons alone, each clock reading its line-mates'
  rows on its three axis lines: the warm counts 22068, 23907 and 25746,
  12, 13 and 14 rows of 1839) the ticks 522 .. 524; `j1_source` (a fixed
  source `s` of content 4096 at the centre releasing one row per
  direction of the 290 primitive directions with |a| + |b| + |c| <= 6 per
  interval, a crowd with a gradient: the warm counts 25746 .. 36195) the
  ticks 524 .. 529; the shell's 64 beta clicks a step (the
  10th-to-90th-percentile width of the click ticks over their median
  below 0.1, against ln 9 / ln 2 = 3.17 for nature's memoryless decay),
  every click the content 3 (a line, against nature's continuous
  spectrum), the shell's count the neutrons' (64). J3: the deuteron of
  series I (`p` 1836 and `n` 1839 each holding one unit of `nuclear`, the
  strong column G = 10000 with the lifetime 3, the whole fan of 290
  directions, the width of the push 2^28, at one Link about the centre of
  an open 21^3 GameBoard) with `become` at 512 on the neutron, a shell of
  `d` at r = 8 (762 Nodes), 700 intervals: `j3_deuteron` fires at 574
  (the warm count 128590 at one Link from the proton: later than the
  free neutron's 512, not never, PREDICTIONS entry 18), then two protons
  at one Link holding (no step: every attempted step refused as a
  hand-over, series I's binding; the design's "two protons repelling" is
  corrected by series I's registered result), the beta reaching the
  shell; `j3_deuteron_crowd` (`crowd` 65536) never fires in 700
  intervals (the count above the gate at every pulse of the key, the
  second pulse at the age 1024 beyond the run); `j3_neutron_free` (the
  neutron alone, 600 intervals) fires at 512 exactly. Against nature
  (PREDICTIONS entries 10 and 18, the law's own): a step where nature's
  survival is exponential, a line where nature's beta spectrum is
  continuous, a bound neutron that decays later (or is held by a gate on
  the count) where nature's is stable by its binding energy; nothing
  tuned.
- **Features.** The transformation `become` with its clock trigger `at`
  and gate `crowd` (BEAM_LAW note 36 (iii); `tests/test_become.py`), D-1
  for the beta's charge (note 36 (ii)), the strong column and the
  lifetime (series I), the `beam` detector set with `reads` `age`.
- **Run.** `examples/events/weak/` (`j1_lattice`, `j1_source`,
  `j3_deuteron`, `j3_deuteron_crowd`, `j3_neutron_free`, the model ids
  `beam-weak-<name>-v1`, written by `make_worlds.py` with
  `expectations.json`), `tools/run_series.py --jobs 3`; the worktree of
  `claude/universe24-new-3ytqde` from its tip `6a596b34` on the commit of
  the transformation, source fingerprint `071197bc5d0f08cbe52aa44dca0e0d7ad9adf99ef6bf6023231310b9bb8f211c`,
  Python 3.14.0rc2, numpy 2.5.3, headless, four cores; the runs completed
  in 231, 238, 82, 70 and 53 s with the books balanced at every tick; 0
  record checks failed; 15 readings inside, 3 outside, none moved.

  | World | Expected (kind) | Measured | Verdict |
  | --- | --- | --- | --- |
  | `j1_lattice` | every neutron fires at its pinned tick or up to 3 before it: 522 for the 8 inner and the 8 corners, 523 for the 24 faces, 524 for the 24 edges (GAMEBOARD, the warm counts 12, 12, 13 and 14 rows of 1839) | the inner 8 at 522 with the count 22068 (12 rows), the faces 24 at 522 with 23907 (13), the edges 24 at 523 with 25746 (14): 56 inside; the corners 8 at 524 with the count 27585 at the trigger, 15 rows (their three line-mates at 4, 8 and 12 Links on each of three axes: one row dwelling one interval at 4 Links, m(7) = 4, two at 8 and two at 12), where the warm run read 12 rows at tick 100 (a gap: the corners' mates at 4 Links, the edges, one class with one clock, had skipped the self-creation whose row would have been there), the constant-count tick of 15 rows 525: outside by 2 against the pinned 522, the estimator's error and not the clock's | outside (56 of 64 neutrons inside) |
  | | the shell's 64 beta clicks a step: the width over the median below 0.1 (DETECTOR) | 64 clicks from tick 541 to 563, the median 549, the 10th and 90th percentiles 542 and 562, the width over the median 0.036 (nature's 3.17) | inside |
  | | every click the content 3, a line (DETECTOR); the count the neutrons' (DETECTOR) | {3: 64}; 64 of 64 (the beta of every neutron on -x, the flight ages 17 .. 41) | inside; inside |
  | `j1_source` | every neutron fires at its pinned tick or up to 3 before it: 524 .. 529 by its warm count 25746 .. 36195 (GAMEBOARD) | 8 at 522 (the count 25746, pinned 524) and 8 at 527 (36195, pinned 529) inside; 16 at 525 (25746, pinned 524), 8 at 527 (26164, pinned 524), 8 at 528 (31681, pinned 527) and 16 at 530 (32096, pinned 527) one to three intervals after their pinned tick: the count read at the trigger is the warm count, the counts read over the clock's history under the fan's dwells at times higher than the one tick's count the estimator took | outside (16 of 64 neutrons inside; every neutron within 3 intervals of its pinned tick) |
  | | the shell's 64 clicks a step (DETECTOR); every click the content 3 (DETECTOR); the count the neutrons' (DETECTOR) | 64 clicks from 541 to 571, the median 555, the percentiles 544 and 565, the width over the median 0.038; {3: 64}; 64 of 64 | inside; inside; inside |
  | `j3_deuteron` | the neutron fires at 574 or up to 3 before it (GAMEBOARD, the warm count 128590 at one Link from the proton); the pair holds after (GAMEBOARD: no step, every attempted step a hand-over); the beta reaches the shell with the content 3 (DETECTOR) | fired at 577 with the count 128590 at the trigger (65 intervals after the free neutron's 512: later, not never; 3 after the constant-count tick, the counts over the history under the proton's fan at times higher than the one tick's); 0 steps of 39 and 21 attempted, 21 and 39 hand-overs taken, the two protons at one Link at the end; one click at tick 590 with the content 3 (the age 13 on the fan direction (1, 3, -2)) | outside (by 3); inside; inside |
  | `j3_deuteron_crowd` | no transformation in 700 intervals, the count 128590 above the gate 65536 at every pulse (GAMEBOARD); no beta click (DETECTOR) | none (0 of 1 transformed; the pair holding, 0 steps of 40 and 22 attempted); 0 clicks | inside; inside |
  | `j3_neutron_free` | the neutron fires at 512 exactly (GAMEBOARD); the beta reaches the shell with the content 3 (DETECTOR) | 512 with the count 0; one click at tick 526 with the content 3 (the age 14 on the fan direction (1, 3, -2)) | inside; inside |

- **Verdict (J1, J3).** What the detector's world sees is the law's own:
  a population of neutrons decays in a step (the shell's 64 clicks within
  23 intervals about the tick 549, a width of 0.036 of the median
  against nature's 3.17 for a memoryless decay), every beta carries the
  one declared content (a line, not a spectrum), and a neutron beside a
  proton decays later than a free one (577 against 512) or, under the
  gate, not within the run: PREDICTIONS entries 10 and 18, plain
  disagreements with nature's exponential survival, continuous spectrum
  and stable bound neutron, registered as the law's limits and not tuned
  (the exponential would need the declared bath of WEAK.md 2.4, J1b, not
  built: not one key of one rule). The three readings outside are the
  one GAMEBOARD criterion, the trigger tick against the count the warm
  run read at a single tick: the corners of `j1_lattice` fired 2
  intervals after their pinned tick because the estimator's tick had
  caught a gap in their line-mates' rows (their count at the trigger, 15
  rows, gives 525 by the law's own sum, and they fired at 524), and 48
  neutrons of `j1_source` and the deuteron's neutron fired 1 to 3
  intervals after theirs because the count a clock reads under a fan's
  dwells is not one number over its history; the ticks are the engine's
  (the clock slowed by its count as every clock is, `by_clock` at the
  world's suspension) and the pins were the estimator's; nothing was
  moved, and the lesson for the next series is to pin a range from the
  count's history over a dwell period, not one tick's count. The bound
  neutron's stability under `crowd` is a gate on the count at its Node, a
  difference from nature that is itself a prediction (entry 18: any crowd
  dense enough stabilises a neutron, bound or not). Nothing was tuned; no
  law changed beyond the one rule added. The page for the model owner:
  the scratchpad's `weak_impl/weak.html`, published by Boss.
- **Re-read under the step drive (2026-09-20; measured, nothing
  pinned).** `j3_neutron_free` reads the same (no push; the record's new fields
  aside). Under the step drive (2026-09-20, BEAM_LAW note 17 as amended: a body's count of Links is the whole part of the distance its momentum has driven, on its own record; a body that receives a momentum begins its drive at 0 instead of stepping off its age)
  `j3_deuteron`'s neutron fires at tick 572 (577 registered; the pinned
  574 or up to 3 before it: inside now), the count 128590 at the trigger,
  the shell's one beta click at 583 with the content 3, the neutron's
  clock 626 of 700 (620); but the pair does not hold: each body makes 3
  steps of 33 and 27 attempted (24 and 30 hand-overs; registered 0 of 39
  and 21, every attempt refused), the GAMEBOARD reading "the pair holds
  after the transformation" outside. `j3_deuteron_crowd`: no
  transformation and no beta click, inside, the bodies 2 steps each of
  35 and 29 attempted. 9 readings inside and 1 outside (10 and 0). The
  verdict stands on the detector's readings (a step decay, a line, the
  bound neutron later than the free one); the deuteron's holding at one
  Link under the drive is series I's question (its deuterons hold; this
  one, with the neutron's `become` and the shell, does not for 3 steps)
  ([migration](MIGRATION.md#the-step-drive-on-2026-09-20-the-count-of-links-as-the-whole-part-of-the-driven-distance)).


**The W world, the exchange form at one Link (no key added).**

- **Model prediction, pinned before the run
  ([the expectations](../examples/events/weak/README.md#the-w-world-the-exchange-at-one-link),
  `expectations.json` under `w`).** The W is a paid family with a whole
  charge per unit of amount and the lifetime 1 (BEAM_LAW note 36 (iv)):
  a row born at a self-creation is at one Link at the age 1 (m(1) = 1)
  and is measured there by the keys' rule for a paid arrival, its units
  clicked and its label the push, or booked on the border `lifetime` at
  the end of that interval where no table took it. A bar of 7 x 1 x 1,
  K 2^20, N 64, `release` [1, 2^20], `suspension` 0; `n` (1839, charge
  0), `p` (charge 4 per unit of content), `w` (paid, charge -7344 per
  unit of amount, `lifetime` 1, no column); the neutron fixed at x = 2
  with `become` at 8 into `p` with the one product `[["w", 1, 3]]` on
  `directions` `[[1, 0, 0]]` (the charges 4 x 1836 - 7344 = 0), the
  proton of 1836 fixed at x = 3; 16 intervals. Expected: the neutron's
  `become` at tick 8 with the W on +x (GAMEBOARD); the proton's click of
  `w` at tick 9, one Link and one interval later (DETECTOR); the proton's
  charge 0 and content 1839 after, a neutron's in the detector's terms
  (DETECTOR); no W on the border `lifetime` (DETECTOR); the momentum
  exchanged, -192 on the neutron become proton and +192 on the proton
  (GAMEBOARD: the label 64 x 1 x 3). The contact form (L = 0, no
  carrier) is series J1 and J3's `become` itself; no Z family.
- **Features.** `become` (note 36 (iii)), D-1 (note 36 (ii)), the
  lifetime (note 31 (vii)); `tests/test_w_world.py`.
- **Run.** `examples/events/weak/w_exchange.json` (the model id
  `beam-weak-w_exchange-v1`, written by `make_worlds.py`),
  `tools/run_series.py`; the worktree of `claude/universe24-new-3ytqde`
  from its tip `6a596b34` on the commit of the W world, source
  fingerprint `071197bc5d0f08cbe52aa44dca0e0d7ad9adf99ef6bf6023231310b9bb8f211c` (the transformation's, no source
  changed), Python 3.14.0rc2, numpy 2.5.3, headless; 0.1 s, the books
  balanced at every tick; 0 record checks failed; 5 readings inside, 0
  outside.

  | World | Expected (kind) | Measured | Verdict |
  | --- | --- | --- | --- |
  | `w_exchange` | the neutron's `become` at tick 8 into `p` with [["w", 1, 3]] on +x (GAMEBOARD); the proton's click of `w` at tick 9 (DETECTOR); the proton's charge [0, 1] and content 1839 after (DETECTOR); the border `lifetime` 0 for `w` (DETECTOR); the momentum -192 and +192 (GAMEBOARD) | `become` at tick 8, the products [["w", 1, 3, [1, 0, 0]]], the recoil [-192, 0, 0]; the click at tick 9, the clicks {w: 1}; the charge [0, 1], the content 1839 (the neutron become proton: [7344, 1] and 1836); the border {n: 0, p: 0, w: 0}; the momenta [-192, 0, 0] and [192, 0, 0] | inside (5 of 5) |

- **Verdict (the W world).** The exchange is complete at the click: the
  W carries the charge -7344 and the momentum 192 over one Link and one
  interval and is held by the proton, which then has a neutron's charge
  and content with no rule of its own fired; the family name it keeps is
  the GameBoard's label, not a reading. The design's sketch of a
  `become` entry on the proton (`into n` with a beta) is refused by the
  law's balance (the W unit held keeps its charge), and balances only
  with a positive product (a positron, `tests/test_w_world.py` (c)),
  which the register does not use. What nature's W has and this does not
  (the physicist's WEAK.md 5.3): the electroweak scale, the W and Z
  masses fixing it, the propagator's rise, V-A; registered as the law's
  limits, nothing tuned. The page for the model owner: the scratchpad's
  `weak_impl/weak.html`, published by Boss.

### L, the amplitude law (2026-09-20)

- **Confronts.** The model owner's decision of 2026-09-20 (Highlights 5.4,
  "DECIDED: `amplitude-v1` is built, with the four recommendations and the
  four unifications"; the ten principles, the corrected sentence "the
  world is the list of clicks"): under the world key `amplitude` the
  GameBoard computes every path of a record, locally and exactly, and the
  world's list of clicks is read from it by the birth phase u on the
  ladder of the record's offers, normalised by their sum with the rungs
  at the nearest integer ([BEAM_LAW note 37](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation);
  the physicist's and the mathematician's design,
  docs/designs/amplitude-v1/DESIGN.md, every integer from its check scripts).
  The acceptance tests of the design, written before any run: the
  Mach-Zehnder interferometer always at one port (test 1), Elitzur-Vaidman
  (3), determinism (8), the two slits at a low rate (2), the register's
  replay (10), and, in the second half, the pair with the choosers (4),
  GHZ (5), the which-path world (6), no maintenance (9) and the gate. Not
  claimed: that quantum mechanics is solved; claimed, once the runs pass:
  that the engine's own tables give Born, interference, Bell with exact
  marginals and S below Tsirelson at finite N, GHZ, which-path, CNOT and
  Grover, with the named departures and the open items.

**L1, the Mach-Zehnder interferometer and Elitzur-Vaidman (the design's
section 3.4; the acceptance tests 1, 3 and 8).**

- **Model prediction, pinned before the runs
  ([the expectations](../examples/events/amplitude/README.md#l1-the-mach-zehnder-interferometer-and-elitzur-vaidman),
  `examples/events/amplitude/expectations.json`, written by the
  generator from the design's `mz.txt`).** A plane of 5 x 5, K 2^20, N 64,
  75 intervals; the source at (0, 0) births one record per self-creation
  on two arms (the birth phase u = t - 1 at tick t: 64 births span the
  circle and complete by tick 75), mirrors at (3, 0) and (0, 3), the
  splitter at (3, 3) with its split table selected by the arrival
  ((20, 21): transmitted 20, reflected 21 with the quarter turn), D1 at
  (4, 3) and D2 at (3, 4) reading `sum`. Expected over the 64 births
  (DETECTOR, the gathers): `mz_equal` D1 64 and D2 0 (the offers
  1681/1682 and 1/1682); `mz_half` 0 and 64; `mz_quarter` 32 and 32;
  `mz_balanced` ((1, 1)) 64 and 0 with D2's rows cancelled on the GameBoard
  (GAMEBOARD); `mz_345` ((3, 4)) 63 and 1, the same u = 63 falling in D2
  where the rung moved; the unequal arms (arm 2 two intervals longer) at
  `phase_per_link` 0: 64 and 0, at [8, 1]: 32 and 32, at [16, 1]: 0 and
  64; Elitzur-Vaidman `ev_29` (arm 2 absorbed at (0, 3)): absorber 32,
  D1 17, D2 15 (D2 the dark port of the unblocked device, 15/64 against
  the ideal 16); `ev_169` ((119, 120)): 32, 16, 16; one gather per
  completed record, the same list on a second run of the same world
  (determinism), the record's `total` within 0.0019 of 1 on the (20, 21)
  worlds (the tables' rounding).
- **Features.** The world key `amplitude`, the split (`rerelease` with
  `weights`, `turns` and `inputs`), the normal form's cancel, the pair
  form of `phase_per_link`, the reading `sum`, the layer and its ladder;
  `tests/test_amplitude_record.py`, `tests/test_amplitude_split.py`.
- **Run (2026-09-20, the ten worlds of `examples/events/amplitude/`, 80
  intervals each, `tools/run_series.py --jobs 3`, the source fingerprint
  `ff5c382d672f` (the stage (v) source; `a7b924b3297a` at stage (iii),
  the same integers), every run completed and conserved at every tick,
  0.2 s each; the readings by `tools/amplitude_path.py --check`, whose
  replay equals `run.json`'s `world` on every run; DETECTOR unless
  said).** The
  gathers over the 64 births of the ticks 1 .. 64 (the design's table
  reproduced on every world):

  | world | D1 | D2 | absorber | the design |
  | --- | --- | --- | --- | --- |
  | `mz_equal` | 64 | 0 | | 64, 0 |
  | `mz_half` | 0 | 64 | | 0, 64 |
  | `mz_quarter` | 32 | 32 | | 32, 32 |
  | `mz_balanced` | 64 | 0 | | 64, 0 |
  | `mz_345` | 63 | 1 | | 63, 1 |
  | `mz_unequal_f0` | 64 | 0 | | 64, 0 |
  | `mz_unequal_f8` | 32 | 32 | | 32, 32 |
  | `mz_unequal_f16` | 0 | 64 | | 0, 64 |
  | `ev_29` | 17 | 15 | 32 | 17, 15, 32 |
  | `ev_169` | 16 | 16 | 32 | 16, 16, 32 |

  One gather per birth, the last of the 64 at tick 75 (76 on
  `mz_quarter`), the 11 records born after open at the end; the same list
  on a second run (test 8). The record's `total` (GAMEBOARD, the sum of
  the offers in the unit 2^58) is not the design's "1 within 0.0019" for
  every u: over the 64 births it takes 8 values, 65448/65536 to
  65773/65536 (within 237/65536 of 1), the same 8 on every one of the
  ten worlds, the tables' rounding (C^2 + S^2 within 361 of 65536)
  depending on u and the sum over the ports not seeing the split
  (unitarity); pinned as measured beside the design's bound, marked
  failing (`tests/test_amplitude_layer.py`). The split takes no click
  gate (the decision on the review's B1): on `mz_quarter` the two arms
  reach the splitter a half turn apart and both split, where the crowd's
  pointer gate would have passed them (130 passes, a which-path device
  reading 32/32 by coincidence); on `mz_unequal_f8` the rows of two
  records reach it together and both split.

**L2, the two slits at a low rate (the design's test 2).**

- **Model prediction, pinned before the run
  (`expectations.json` under `two_slits`, the generator's reading of one
  birth by the design's `slits_read.py` on the reference world
  `slits_one`, independent of the layer).** The shipped 60 x 121 world
  under the key, the lamp at rate [1, 1] with the content K (u = t - 1
  at the birth tick t), `phase_per_link` [8591334592, 2^30], the pixels
  `sum`, the wall freed within 6 of each opening (every fan row leaves
  the plane) and the lamp's three rows that miss the openings absorbed at
  (7, 58), (7, 60), (7, 62) (a fan row and a lamp row at one set would
  carry the multiplicities 455 and 5, refused). The reading, coherent
  within one Node and incoherent across the Nodes of a set (the decision
  of 2026-09-20 on the owner's point 5; a face of 24 Nodes hit is one
  cell of the sum of its Nodes' squares): 80 sets with rows (3 wall Nodes,
  75 pixels, the faces +y and -y), the total 847181/745472 = 1.136 of the
  birth norm (the wall's rows 3/5, the fans 2/5, the cross terms of paths
  meeting at one Node: 27 pixels receive two paths), the shares wall
  0.528, screen 0.244, faces 0.228; the clicks over the 64 births by the
  ladder: wall 34 (11, 12, 11), screen 15 (one each at y = 11, 29, 36, 43,
  50, 56, 59, 60, 70, 77, 82, 90, 107 and two at 61), faces 15 (8, 7);
  Pearson of the record's screen weights 0.744 with the incoherent sum,
  0.368 with the Euclidean two-source cosine (the design's
  shipped-geometry 0.753 and 0.381), the screen-alone histogram 0.931
  with the weights (0.963). The design's "wall 3/5, screen 2/5" is not
  this geometry's reading: the freed fans reach the open faces in y, a
  third destination. (Before the per-Node decision the faces summed their
  rows coherently, the total 1.258 and the shares 0.477 / 0.221 / 0.302,
  the clicks 31 / 14 / 19: dated history of the same day.)
- **Run (2026-09-20, `slits_low`, 230 intervals, 2.4 s, the fingerprint
  `ff5c382d672f`, completed and conserved; `slits_one` 220 intervals
  without the key, 0.7 s).** DETECTOR: 64 gathers of the 64 births by
  tick 213 (the births go on: 230 records, 81 gathered, 149 open at the
  end); the first record's cells are the reading's 80 sets with the
  reading's rungs, its weight and total the reading's exactly, its click
  at the wall Node (7, 58, 0) with the content 1; the clicks per set equal
  the reading's on every one of the 80 sets (wall 34, screen 15, faces
  15; a face's click at a Node of its edge); 3 distinct cell lists over
  the 64 births, 32 with u = 0's (the tables' rounding by u, no rung
  moved); the reading tool's replay equals `run.json`'s `world`.

**L3, the pair with the choosers, the CHSH labels, the which-path world
and no maintenance (the design's section 4; the acceptance tests 4, 6
and 9).**

- **Model prediction, pinned before the runs (`expectations.json` under
  `pair`, the design's `bell.py` in the generator).** The registered A2
  world under the key (the lamp's `arms` 2 and `branches` [[0, 1], [3,
  1]], Alice's arm first; the four counters reading `sum`; at the CHSH
  labels the chooser sources removed and the windows the integers). The
  cells (oA, oB) over the 64 births: (0, 8) 27, 5, 5, 27 (E x 64 = 44);
  (0, 24) 5, 27, 27, 5 (-44); (16, 8) and (16, 24) 27, 5, 5, 27 (44); S =
  176/64 = 2.75 (2 sqrt 2 = 2.828; the discreteness: S = 2 sqrt 2 -
  epsilon(N), the design's epsilon at most 4/N, not met at N = 64: 0.078
  against 0.0625, as the design's own |E - cos| at this N, 0.0352 over
  all pairs, is above 1/N); every marginal 32/64. The choosers'
  15 setting pairs: E x 64 = 44, -60, 20, 60, -8, -48, -8, 60, -52, -64,
  40, 20, -28, -36, 64 for a in (0, 12, 25, 38, 51) by b in (8, 29, 51);
  on the registered quadruple (0, 25) x (8, 29) S = 156/64 = 2.4375 (2
  exactly under A2's window gate). The which-path `read` on Alice's arm:
  E x 64 = 44, -44, 0, 0, S = 88/64. Bob's counters 116 Links farther:
  E(16, 24) x 64 = 44 (44 with the read: 0).
- **Run (2026-09-20, `examples/events/amplitude/bell_*`, `path_*`, the
  fingerprint `ff5c382d672f` (`ccb244fc112f` at stage (iv), the same
  integers), every run completed and conserved, 0.2 s
  each, `bell_choosers` 1000 intervals 3.3 s; the reading tool's replay
  equals `run.json`'s `world` on every run; DETECTOR).** Every integer
  above reproduced: the CHSH cells and E, S = 176/64, the marginals 32/64
  exact (Alice + for u < 32), the 15 pairs' E and S = 156/64 on the
  registered quadruple, the which-path E and S = 88/64, the far counters
  E 44 and 0 with every record gathered at least 200 intervals after its
  birth (`tests/test_amplitude_pair.py`). The tables' rounding does not
  enter: both arms' rows carry the one phase u, whose factor is common
  to every cell.

**L4, GHZ (the design's 4.5; the acceptance test 5).**

- **Model prediction, pinned before the run (`expectations.json` under
  `ghz`).** Three arms on a plane of 7 x 7 (`branches` [[0, 1], [7, 1]]),
  the counters' setting 16 with the turn 0 (X) or 16 (Y): XXX allows
  +++, +--, -+-, --+ (16 births each, the product +1) and XYY, YXY, YYX
  allow ++-, +-+, -++, --- (the product -1), the other four triples of
  weight exactly 0 (39588699237876835586664300544 on the allowed, in
  1/256^12); YYY allows all eight, 8 each.
- **Run (2026-09-20, `ghz_xxx` .. `ghz_yyy`, 80 intervals, the
  fingerprint `ff5c382d672f`, completed and conserved, 0.2 s each;
  DETECTOR).** Every triple and count as pinned; the register's replay
  equals `run.json`'s `world`.

**L5, the gate between records (the design's section 10).**

- **Model prediction, pinned before the runs (`expectations.json` under
  `gate`, the design's `gate.py` on the host's joint state).** The
  Hadamard on the GameBoard (a `rerelease` with `rotate` at the setting
  N/4) turns |0> into {00: +, 10: -} (the amounts 181 of the 128 tables,
  the phases u and u + 32, the multiplicity 65536); the CNOT at a gate
  with the target's |0> gives {00: +, 11: -}, the pair; with Bob's window
  at -b the CHSH labels give E x 64 = 44, -44, 44, 44, S = 176/64 (as
  4.3); CNOT twice is the identity; GHZ by one gate of three parties
  gives {000, 111} and the products -1 (XXX), +1 (XYY, YXY, YYX), this
  convention's H; the register's ceiling: three label rotations on a
  path (m = 2^48) fit, four (2^64) do not, Grover's six (2^96) are not a
  world of the GameBoard, as the design's section 10 states (exact on the
  host's integers, not on a Node); after n gates a record has at most
  n x 2^n rows (the pair 4, GHZ 6).
- **Run (2026-09-20, `cnot_pair_<a>_<b>`, `cnot_twice`, `cnot_ghz_*`,
  `rotations_3`, the fingerprint `ff5c382d672f`, completed and
  conserved, 0.3 s each; `rotations_4` refused at load).** Every integer
  above reproduced on the GameBoard: the Hadamard's rows, the gate's rows
  (the `gate` lines: the survivor, the joined record, the labels
  [[0, 1], [3, 1]], 4 rows; GHZ [[0, 1], [7, 1]], 6 rows), S = 176/64,
  CNOT twice's labels {0, 1} on both arms, GHZ's allowed triples and
  products; the reading tool's replay equals `run.json`'s `world`
  (`tests/test_amplitude_gate.py`). Departures: the gate joins records of
  distinct lamps (one per lamp, the earliest born), the control the
  record arriving on the entry's declared `control` direction, and acts
  when rows of `parties` emitters are pending; a record that reaches a
  gate with units elsewhere or an offer already made is refused (the
  design's lazy relabelling of rows elsewhere is not built: two
  sequential gates on an entangled record are one gate of three parties
  here, or one gate per arm as in `cnot_twice`). Re-run after the review
  of (v) (the gate's copies booked on the live count, the control
  declared, the hold local): every integer above unchanged.

**L6, the pair at N = 1024 and N = 4096 (the owner's paper numbers).**

- **Model prediction, pinned before the runs (`expectations.json` under
  `pair_n`).** The registered A2 board at the CHSH labels 0, N/8, N/4,
  3N/8, one birth per u: S = 2896/1024 = 2.828125 at N = 1024 (the
  design's), E x 1024 = 724, -724, 724, 724, |E - cos| <= 1/N on every
  pair; S = 11584/4096 = 2.828125 at N = 4096, E x 4096 = 2900, -2900,
  2892, 2892 against the cosine's 2896.3: the tables' entries in 1/256
  round E by 0.0009, beyond 1/4096 = 0.00024, so the design's bound
  |E - cos| <= 1/N holds at N = 1024 (0.00008 against 0.00098) and not
  at 4096, nor at 64 (0.0196 against 0.0156), while S = 2 sqrt 2 -
  epsilon with epsilon at most 4/N holds at 1024 and 4096 (0.0003) and
  not at 64 (0.078 against 0.0625); S stays below 2 sqrt 2 = 2.828427
  at every N. At N = 4096 the half-angle tables of 2N do
  not exist: an even setting reads the 4096 table at s / 2.
- **Run (2026-09-20, `bell_n1024_*` 1044 intervals 1.9 s each,
  `bell_n4096_*` 4116 intervals 8.4 s each, the fingerprint
  `ff5c382d672f`, completed and conserved; DETECTOR).** Every count the
  reading's; S = 176/64, 2896/1024, 11584/4096 (2.75, 2.828125,
  2.828125); the births counted by the record's ordinal (a lamp's clock
  skips a step as the births spend its content: 4096 births take 4099
  intervals); the reading tool's replay equals `run.json`'s `world`.

**L, open items (2026-09-20, after (v)).** The one click (the design's
section 6) is not landed: the record form as the default changes worlds
outside the crowd-threshold series on the gate set
([MIGRATION](MIGRATION.md), (vi)), so the key `amplitude` stays. The K
finding under the record's click (the lensing worlds of `mass_meeting`
under the key, the coordinator's record of 2026-09-20): the record's
click beside the mass moved to smaller y against the control's in every
world, -2.115, -5.208 and -4.432 pixels at the three (M, b) against the
crowd's -2.021, -4.345 and -2.465, and the 464 records that reached the
mass were absorbed whole by it; the two changes it asks for, u as the
record's own field beside the running phase and a row's push by its share
amount^2 / (m x norm) of the label, are the next item ([BEAM_LAW note 37](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)
(ix)). The pushes are untouched by the columns: a branched row pushes
matter by its amount as every row does (the owner's (c), the sum over the
branches). Not built: unification (3) (refused: three columns under three
keys), Grover (six rotations beyond the register's ceiling), two
sequential gates on an entangled record, the full register replay.

### A3. Bell test in phase form, delayed geometry

- **Confronts.** The same CHSH data as A2 and the quantum value at the
  settings of A2, 2√2; on the 256-step integer table, whose cosine of 45°
  is 181/256, the exact expectation of a mechanism obeying the singlet law
  is 724/256 = 2.828125.
- **Model prediction today.** Highlights 5.4 and hypothesis 11, line 2: the
  joint law's value appears only when the second ray's path exceeds the round
  trip through the first Detector; then the first Detector's value, carried
  through the birth event by the inverse split, meets the delayed share, and
  the declared coupling of that meeting can give the quantum value.
- **Features.** 1, 2, 3, 4, 5, 6, 7b, 9, 10, and an output-clock delay on
  Bob's line (Highlights 3.28, existing). The coupling between the
  transmission and the held ray is a declared table, written before the run,
  and its exact
  expectation on the 256-step circle is computed independently before the
  run.
- **Run.** The GameBoard of A2 with one change: Bob's ray is held by an
  output-clock delay k_out = 160 intervals at the Node before his analyzer,
  longer than the 128 intervals of the round trip through Alice's Detector,
  so that a value returned by Alice, which reaches that Node 128 intervals
  after Bob's ray did, finds the share still standing. Same settings, same counts, same
  window measured from Bob's release. Recorded as in A2, plus the tick at
  which each transmission meets the held share and the invariants at that
  Node.
- **Criterion.** Pass: S > 2 + 3σ_S in the delayed geometry, S within 3σ_S
  of the declared joint law's exact expectation, every Detector's click rate
  equal to its setting within 3 standard errors and moved by the other
  side's setting by less than 3 standard errors, and the energy and momentum
  at every meeting of a transmission with a held share exact. Fail: S ≤
  2 + 3σ_S in this geometry (the joint law as declared gives no violation;
  hypothesis 11 line 2 fails and a different table must be declared before
  another run), or a marginal that moves with the other side's setting
  (signalling: the table as declared is not admissible against physics), or
  an inexact meeting.
- **Restated under the law of the bit (model owner, 2026-09-18).** The
  model's own prediction in this geometry is the same as A2's: S ≤ 2, the
  declared limit. What line 2 of hypothesis 11 described is not a claim of
  the model but of a table: when Bob's path is longer than the round trip
  through Alice's mark (128 intervals), the value Alice's missed thing
  carries back through the birth event reaches Bob's line while Bob's thing
  is still on it, and the two meet as things meet, by a declared table (point
  4); only such a declared joint table could give more than 2, and the model
  does not supply one. The output-clock delay on Bob's line is retired (point
  21: every ray moves one Link per interval); the delay is a longer path, at
  least 129 Links more on Bob's arm. A3 therefore tests a declared table, not
  the law, and runs only if the owner declares one; the criterion stands
  with "draw" read as "table". Waits for features 15 to 17.
- **Status.** planned.

### A4. Single-Detector PASS statistics against the declared setting

- **Confronts.** The Born rule for one detector: at a splitter of
  transmission T a quantum clicks on one side only, never on both (Grangier,
  Roger and Aspect, 1986, anticorrelation 0.18 ± 0.06 < 1), and the click
  count over M quanta is binomial with mean T M; independent detectors give
  independent clicks.
- **Model prediction today.** Highlights 3.19 and 5.4: a marked Node draws
  1 or 0 once for each arriving transfer, independently for up to six
  arrivals in one interval, reads nothing of the ray, and the distribution is
  its declared setting, not an assumed 50/50; the click is the record of 1
  only; replay never redraws.
- **Features.** 1, 2, 3, 4, 9, 10.
- **Run.** A GameBoard of 17 × 17 × 17 Nodes, open boundary; one source (marked,
  setting 1) emitting one ray per interval toward a marked Node 8 Links away,
  `return_mode` annul so that a returned ray leaves the world into the
  accounted sink at its event Node. Settings 1/8, 1/2 and 7/8; three
  families (light, rate 0; a massive neutral family, rate 3; a massive
  charged family, rate 3, charge −1); three amounts (1, 16, 256); 2^12
  arrivals per cell. One further run with six sources around the marked Node
  at setting 1/2, one arrival per Port per interval, 2^12 intervals; and a
  replay of one run with the same seed. Recorded: arrivals, clicks and
  returns per Port and per cell; the 2^6-cell joint click table of the
  six-Port run; the annulled total per tick; the click sequence of the run
  and of its replay.
- **Criterion.** Pass, all of: clicks + returns = arrivals exactly in every
  cell; |clicks/arrivals − n/d| ≤ 3 √(n/d (1 − n/d)/arrivals) in every cell;
  the click fraction differs between families, amounts and phases at one
  setting by less than 3 standard errors; in the six-Port run the chi-square
  of the 64-cell table against the product of its six marginals is below the
  99.9 percent quantile for 57 degrees of freedom; the replay's click
  sequence equals the run's bit for bit; initial = current + escaped +
  annulled at every tick. Fail: any one.
- **Restated under the law of the bit (model owner, 2026-09-18; Highlights
  5.4, points 6 and 14).** There is no draw. A thing that arrives at a mark
  is absorbed and counted; a mark of setting n/d misses by a declared table,
  one arrival in d returned on its steps, deterministic, so the click count
  over M arrivals is exactly ⌊M·n/d⌋ up to the table's phase, not a binomial
  variable, and two runs of one world are byte-identical. The binomial
  criterion of the Born rule below therefore no longer applies to the
  counts; what A4 tests under the law is (i) never a click on both sides of
  a splitter for one quantum (a thing is whole, one path), (ii) the counted
  fraction equal to the setting exactly, (iii) independence of two marks
  (their tables run separately). The binomial statistics of nature, if they
  are to come from the model, must come from the histories of the arrivals
  (their births and paths), which this run's regular source does not vary;
  a run with a source of varied phase and timing is the test of that.
  `return_mode` annul is retired; a returned thing walks back to its birth
  event. Waits for features 15 to 17.
- **Status.** planned.

### A5. Electron-electron repulsion through released fields

- **Confronts.** Coulomb's law, force k e²/r² (its inverse-square exponent
  verified to 1 part in 10^15 by Williams, Faller and Hill, 1971), and
  Rutherford's scattering law for charged rays: at speed v and impact
  parameter b a small-angle pass transfers momentum 2 k e²/(b v), inversely
  proportional to b; equal and opposite recoil; attraction for opposite
  charges.
- **Model prediction today.** Highlights 3.5: a ray's field is its own
  information spreading in ray form in all directions with the outward
  dilution; where a field ray meets a ray whose declared coupling responds
  the meeting changes that ray's trajectory, and the field ray returns
  reversed with the opposite momentum to the ray that released it, which
  recoils when the return arrives at finite speed; until its field meets
  something a traveling ray pays nothing; momentum is exact (3.14, 3.16).
  Charge is a family property read at the meeting (3.26).
- **Features.** 1, 2, 5, 6, 7, 9, 10.
- **Run.** A GameBoard of 49 × 49 × 49 Nodes, open boundary, N = 2^12. Two
  electron rays (charge −1, rate r_e, equal content) from two marked sources
  at setting 1, on antiparallel lines along x with impact parameter b = 4,
  6, 8, 12 and 16 Links, one run per b; the same with an electron and a
  positron (+1); a control with a neutral family of the same rate and
  content. The coupling "electron field ray meets a charged ray" is a
  declared integer table over the arriving field content and the charge
  product, written before the run. Recorded per tick: each matter ray's
  momentum components; every field ray in flight; the tick at which the first
  field return reaches each releaser; the transverse momentum transfer Δp(b)
  of each ray read when both are 3b past closest approach; the audits.
- **Criterion.** Pass, all of: the component-wise momentum sum over matter
  rays, field rays and returns equals the initial sum at every tick exactly;
  after all returns have arrived the two rays' Δp are equal and opposite
  exactly, and before that their difference equals the momentum carried by
  field rays in flight exactly; the first recoil of each releaser arrives at
  exactly twice the transit of the field ray to the meeting; the log-log
  least-squares exponent of |Δp(b)| over the five b is −1.0 ± 0.15 (standard
  error from the five points); like charges deflect apart and the
  electron-positron pair together; the neutral control goes straight; no
  ray meets a field ray of its own event (the audit reads the carried
  record). Fail: any one; an exponent outside the band is a fail of the
  outward dilution or of the declared table against Coulomb, stated as
  which.
- **Made.** 2026-09-17, on `main` at `6f35705` (feature 12b,
  `field-remainder-v1`, in it), as `examples/nature/a5_coulomb/`: thirteen
  worlds written by `make_worlds.py`, the records read by `analyze.py`, its
  integers in `record.json`, the dictionary in the
  README.
  The world: GameBoard 97 × 49 × 49, open, N = 2^12; ray a of amount 64 from
  (0, 24 − b/2, 24) heading +X and ray b of amount 64 from (96, 24 + b/2, 24)
  heading −X, closest approach at x = 48 at tick 48, the read-off at tick
  48 + 3b; each ray's field `light` declared `field_of` it with `release`
  [1, 4] (16 per heading), `spread` [6, 1, 1, 1, 1, 1] and the engine's
  `source_sign`; `electron_field_turn` as the momentum table of
  ray-momentum-turn-v1, sign +1 in the electron-electron worlds and −1 in the
  electron-positron worlds. Deviations from the run planned above, each
  stated: (i) the x extent is 97, not 49, so that both rays are on the GameBoard
  3b past closest approach at b = 16 (the transverse extents are 49); (ii)
  the two rays are two families of identical properties, `electron_a` and
  `electron_b` (charge −3, rest rate 1; +3 for the positron; 0 for the
  control), because the engine names one light family per releaser, so each
  ray's field is its own family, `light_a` and `light_b`; (iii) the sign of
  the releasing charge reaches the coupling through the family, not through
  a guard: the engine gives a `when` guard no view of `source_sign`
  (`RAY_PROPERTIES` holds amount, heading, phase, advance, delay, family,
  charge and detector), so the table names the family that carries the sign
  and its entry is the sign of the charge product, written before the run;
  the phase is read nowhere; (iv) the electron amount is 64, the smallest
  at which the release gives 16 per heading and the register resolves one
  quantum in 64 (256 costs 4.8 times more at 24 ticks and would have put
  each run far over ten minutes); (v) each coupling names the other ray's
  field only, and the self-meeting clause is read from the record as a ray
  arriving at a Node together with content of its own light family
  (`spatial_received`); (vi) the runs continue 8 ticks past the read-off
  for b ≤ 12 to see whether the transfer is complete, and end at the
  read-off for b = 16 (ray a is then at the GameBoard's last Node); (vii) the
  neutral control (`nn_b4.json`, b = 4) keeps the released field, so it
  differs from `ee_b4.json` by the charge and the coupling alone; (viii)
  a check without `spread` at b = 4 and 16 (`ee_b{4,16}_nospread.json`),
  the E6 geometry, is recorded beside the series. Run times under two to
  four runs in parallel on four cores: 176, 167, 183, 266 and 255 s
  for the electron-electron worlds at b = 4, 6, 8, 12, 16, the same within
  two seconds for the electron-positron worlds, 143 s for the control, 21
  and 35 s without spread.
- **Shows.** Δp(b), the change of each ray's momentum register at the
  read-off and at the end alike, in quanta on the impact axis y: at b = 4,
  (0, −3, 0) for ray a and (0, 3, 0) for ray b in the electron-electron
  world (apart), (0, 3, 0) and (0, −3, 0) in the electron-positron world
  (together), from two pushes each, at tick 50 by 2 quanta and at tick 53
  by 1 quantum, the field ray heading ±y and returned reversed; at b = 6,
  8, 12 and 16, (0, 0, 0) for both rays in both charge pairs, no push at
  all. Without `spread` the transfer is one whole meeting
  of 16 at tick 48 + b/2 for every b (the E6 geometry: the field on the six
  axis lines of its source). The field in flight of a ray at c is a steady
  wake that moves with it: on the line at transverse distance 4 the +y
  content of ray a is 2 quanta at x = t − 4 and 1 quantum at x = t − 10 at
  every tick t of the pass, ray b sweeps through each column once, and
  Δp(4) = 3 is that wake's amplitude; in the control's record the +y quanta
  of ray a over ticks 40 to 68 are 667, 464, 290, 87 and 29 at distances 1
  to 5 and none beyond, the release of 16 thinned by floor(A × 6/11) at
  every Link (16, 8, 4, 2, 1, 0) and the rest owned by the Nodes: at tick
  96 of the b = 16 world 7572 quanta of `light_a` are in the world, 310 of
  them rays in flight (the same 310 at every tick from tick 16) and 7262 in
  remainder registers, which fill by 1/11 or 6/11 per arrival and do not
  release during a pass. No return ever reaches a releaser: a ray at one
  Link per interval outruns its recoil (the recoil's Manhattan distance to
  the ray is at least 2b at the push and grows by one per interval while
  the ray stays on its line), so the recoils walk back to the line the ray
  left 2b intervals earlier and spread there. A turned ray does share Nodes
  with its own field: at b = 4 ray a, on the register (64, −3, 0), takes
  its first −y Link at tick 65 and arrives with 18 quanta of `light_a`
  (its own −y release of 16 from the Node it left, which skips the
  dominant-axis line only, plus 2), then with 2 and 1 at ticks 66 and 67
  (its earlier transverse releases spread forward along the new line, one
  Link behind the x it gave up); six co-arrivals per b = 4 world, none at
  b ≥ 6 (no turn) and none in the control; without `spread` the same at
  every fifth Link, with the 16-quantum release. In these worlds they are
  crossings; under the catalog's single `light` family the same co-arrival
  is a push by the ray's own field. Every ledger line balanced at every
  tick of every world, `conserved_at_every_completed_tick` true, the
  momentum sourced (0, 0, 0) at every tick by the pair's symmetry (each
  ray's release and spread sources cancel the other's).
- **Outcome per clause.** (1) Pass: the sum over matter rays, field rays
  and returns is (0, 0, 0) at every tick of every world, exactly, and
  initial + sourced = current + escaped holds; (2) pass: after the last
  push Δp is equal and opposite exactly, (0, ∓3, 0) at b = 4 and zero
  elsewhere, and the imbalance equals the momentum of the field rays in
  flight at every tick, both being (0, 0, 0) by the symmetry, so this
  geometry does not test the clause beyond zero; (3) fail, the named
  alternative: no first return, the recoil never reaches a releaser moving
  at c (the transit of the axis field ray is b, the recoil would be due at
  tick 48 + 3b/2 at a releaser at rest, and the first co-arrival with own
  field, tick 65 at b = 4, is the turned ray's own release, not the
  recoil); (4) fail: |Δp(b)| = 3, 0, 0, 0, 0 over b = 4, 6, 8, 12, 16 for
  both rays in both charge pairs, no logarithm of four zeros and no
  exponent, a fail of the outward dilution of the declared table against
  Coulomb, stated as such: floor(A × 6/11) per Link empties a release of 16
  into the Nodes' registers within five Links, so nothing in flight reaches
  b ≥ 6 during a pass, and the fall is geometric, not 1/b; (5) fail as
  written: like charges apart and the electron-positron pair together at
  b = 4, the signs as Coulomb's, and no deflection either way at b ≥ 6,
  where the clause asks for one; (6) pass: the
  control's rays go straight, no push, register unchanged; (7) fail for a
  turned ray: six co-arrivals with its own field per b = 4 world after the
  turn, by the GameBoard geometry of the turn (the release skips the
  dominant-axis line only), none for a straight ray. The result is the
  model's stated limit under this table and this amount; nothing was
  retuned. The model owner may want to read (3) and (7) against Highlights
  3.5 (the recoil "arrives at finite speed", the field never met by its
  own ray): for a free ray at c the recoil is never delivered and the
  turned ray meets its own release.
- **Status.** measured on 2026-09-17, commit
  `6f357052b6c18ab186e67d0113a0c82ff8b5a99d`, source
  `4c6e313ce9f0b14be95ce85b3c4f256d4072f2e81715ddf1f1071b44c11d33bb`;
  initialization fingerprints, electron-electron b = 4, 6, 8, 12, 16:
  `2bd610daaf5706bb22f0cf96e195a4d0f66d955192834742fa6266357dc7af31`,
  `435bc94e6b25dc34b176fc5ac70f7d03e36fc2714a0c926d5ae8dbfc03c6f95e`,
  `f5b459b4b328d6c4a94729a25344935de4ce482a98138551ebd008f82d3b7c06`,
  `4c6d9a0eb0aff4012ee0a1ba4164433079d552eb1c7efcbda91003922ed48194`,
  `44e9ac92c9894b9262aa9fdb2be2d9da5122409a7ab603c5c84a19919eafee0b`;
  electron-positron b = 4, 6, 8, 12, 16:
  `eee0b52036ebc7efb85b2c0ee1add0cfddd327ba0d1de0e2a71cd961f520f94e`,
  `40d1ea11b19cf6c76755eae9474edadf04f82582b4a7922d1fb8e5a02a5285ee`,
  `286e18a60aae4f6658a3277d065c51c6250a05a06c4c5287ddb6020bc960552b`,
  `09e82044c2df5845072463ef3dd6497ea5c79b9f8637f005fa5822468c4dc9a2`,
  `1f5b00f392a8ec65c647428dc0c3858ef6f65806c70ce6bb88716e79ef46a26e`;
  the control
  `27a8b3cca5764501a33a289a977a64f74f8e724c9a1e1ccbdf9fa8123fb6eeb5`;
  without spread, b = 4 and 16,
  `d34f56206ec9e36201971ed2ba5cad45b436c9d8987582b43aca44de6679b5e0` and
  `9b597d2e49842ba504ab1473d416e6d7e80440248e847e876eed67d406717be0`;
  outcome: fail, the exponent clause (4), by the outward dilution of the
  declared table, with (3), (5) and (7) failing as stated and (1), (2) and
  (6) passing; the records stay outside the tree. Earlier reading of
  2026-09-17 (before the run, kept): the sign of the releasing charge
  travels on the field ray as a visible property (`source_sign`, feature
  12), never in the phase, and the attraction of opposite charges
  (`opposite_charge`) closes with it. Under Highlights 5.5 (2026-09-17)
  the release ratio and the strength table are inputs until hypothesis 17
  says what fixes them: this entry confronts the form of Coulomb's law,
  the exponent -1 in b, and not the value of the coupling. Runnable after
  feature 8b (`ray-momentum-turn-v1`, 2026-09-17), which turns a free ray
  gradually by the momentum of every field ray it meets under a coupling's
  `momentum_table`, so Δp(b) is a register the audit reads and not a count
  of whole Ports.

### A5s. Coulomb's force law between two charges at rest

- **Confronts.** Coulomb's law, the force F = k q₁ q₂ / r² between two
  charges at rest (its inverse-square exponent verified to 1 part in 10^15
  by Williams, Faller and Hill, 1971): the force itself, not Rutherford's
  Δp of A5; equal and opposite on the two charges; like charges pushed
  apart and opposite charges pulled together, with the same magnitude.
- **Model prediction today.** Highlights 3.5: the field of a source at rest
  fills space; its density falls as 1/r and the net momentum its rays carry
  through a Node, which is what a met ray feels, falls as 1/r² because the
  same flux crosses every shell (Gauss), exact on average once the Node
  owns the remainder (feature 12b); the GameBoard's anisotropy is of higher
  order, and its residue is measured, not assumed. A5 (measured today, PR
  #239) could not test this: a free ray at one Link per interval outruns
  its own field, so its field is a short wake behind it that never reaches
  a second passing ray at impact parameter 6 or more. Coulomb's law is a
  statement about charges at rest, the case the rule of 3.5 speaks of, and
  this entry measures the force between two static sources directly.
- **Features.** 7b, 12, 12b (on 1, 7, 9, 10).
- **Run.** Two external bodies at rest (`external-body-v1`, Highlights
  3.19): body A of a family of the proton's charge (+3, the body's whole
  charge; charge-per-thing-v1, 2026-09-18), body
  B of the proton's charge for the like-charge series and of the electron's
  (−3) for the opposite-charge series, each of amount 2^28 radiating its
  light on all six headings every interval by `release` [1, 65536], 4096
  quanta per heading per interval, the light declared once per releaser
  (`light_a` `field_of` A's family, `light_b` `field_of` B's, the engine
  naming one light family per releaser) with `spread` [6, 1, 1, 1, 1, 1],
  the catalog's table, the Node-owned remainder (`field-remainder-v1`) and
  the engine's `source_sign` from the body's declared charge; every
  arrival at a body ends in its exact sink (the default coupling), and A's
  `momentum_table` names `light_b` and B's names `light_a`, each with the
  sign of the charge product, +1 (repulsion) for like charges and −1
  (attraction) for opposite charges, written before the run; no matter
  rays anywhere, no Detector. Distances: B at (r, 0, 0) from A on the +X
  axis for r = 4, 6, 8, 12 and 16, one world per r for each of the two
  charge signs (`pp_r{r}`, `pe_r{r}`); a diagonal series in the plane, B
  at (d, d, 0) from A for d = 3, 4, 6 and 8 (Euclidean 4.24, 5.66, 8.49,
  11.31), like charges only, for the GameBoard's anisotropy (`pp_d{d}`); a
  control, one body alone at the same settings (`p_alone`), its table
  naming its own light, whose register must stay (0, 0, 0) by symmetry
  (its own backward-spread light returns to it from all sides). GameBoard:
  open boundary, a margin of 5 empty Nodes beyond each body on every side
  (the far field escapes; the margin is a stated deviation, below), N =
  2^3 (the phase is read nowhere in these worlds). Ticks: 2r + 32 for the
  Manhattan distance r (64 for the control); the push per interval on each
  body is the change of its momentum register per interval, read from the
  `external_body_absorbed` records, and its steady state is read as the
  mean over the last 32 ticks, the per-tick series recorded so that a
  reader sees the transient and the steady state (the front reaches the
  other body at tick r; at 4096 per heading the axis is lit at once and
  the registers fill over time). Recorded per tick: each body's momentum
  register and position, the world ledger with the bodies' momentum line,
  the audits. Made as `examples/nature/a5_static/`: fifteen worlds
  written by `make_worlds.py`, the records read by `analyze.py`, its
  integers in `record.json`, the dictionary in the
  README.
- **Criterion.** Pass, all of: (1) every ledger line balanced and
  `conserved_at_every_completed_tick` at every tick of every world; (2)
  the control's register (0, 0, 0) at every tick; (3) in every two-body
  world the two registers equal and opposite at every tick (both bodies
  radiate the same release, so this is the exact symmetry of the pair; had
  A and B differed in release the clause would read: the two registers
  in the ratio of the releases, the momentum absorbed from each field
  proportional to its source); (4) the steady-state push per interval F(r)
  over the five axis r, the mean over the last 32 ticks of the push on B
  along x, has log-log least-squares exponent −2.0 ± 0.2 (standard error
  from the five points); (5) like charges pushed apart (A's register on
  −X, B's on +X) and opposite charges together, with the same magnitudes;
  (6) the diagonal series: F at Euclidean distance d against the axis fit
  of (4) evaluated at the same d, the ratio reported per point, no
  pass/fail (A6's anisotropy), and the direction of the push, along the
  diagonal (F_x = F_y, F_z = 0), exact by symmetry. Fail: any of (1) to
  (5), stated as which and why (the table, the remainder rule, the GameBoard,
  the box or the transient).
- **Planning, before the run (not the measurement).** The engine's cost was
  measured first, on the r = 4 world of the plan (GameBoard 21 × 17 × 17, the
  margin of 8) for 16 ticks: 85 s, then 56 s at N = 2^3, that is 2.3 ms
  per Node cycle, and every Node of the GameBoard cycles once the field has
  filled it (a Node holding a remainder register is active until it
  empties, and under a steady source none does), so a world's cost is its
  volume times its ticks: the plan's r = 16 world (33 × 17 × 17, 96
  ticks) would take about 35 minutes and the r = 4 world 25, against the
  budget of about eight minutes per world with two in parallel. A
  mean-field transport of the same split table outside the engine (the
  linear map of the split with the remainders averaged, the two sinks and
  the open faces; validated against that engine probe, whose pushes on B
  per interval, 664, 665, 699, 699, 717, 717, 725, 727, 732, 732, 736,
  737, 740 over ticks 4 to 16, it reproduces within one quantum) sized the
  run and says what to expect. At the run's settings (margin 5, 2r + 32
  ticks) it gives F(r) ≈ 742, 252, 89, 13.1, 2.4 for r = 4 to 16, exponent
  −4.2 ± 0.4; at the plan's settings (margin 8, 2r + 64) 753, 264, 99,
  17.8, 4.4, exponent −3.7 ± 0.3; in free space at its steady state
  (margin 24, 600 ticks) 751, 270, 107, 25.2, 10.1, exponent −3.2 ± 0.1;
  the diagonal at d = 3, 4, 6, 8 about 0.16, 0.26, 0.41, 0.47 of the axis
  fit at the same Euclidean distance at the run's settings. Its reading,
  to be confirmed or refuted by the engine's integers: the split table's
  field at short range is the unscattered part, 4096 × (6/11)^(r−1) on the
  axis, a fall like e^(−r/ℓ) with ℓ = 1/ln(11/6) ≈ 1.65 Links, which
  dominates F below r ≈ 10 (665 of the 752 at r = 4, 59 of 106 at r = 8);
  the 1/r² flux of Gauss is the diffusive tail beyond it, which builds up
  over r²/(4D) intervals with D = 4/9 Link² per interval (the persistent
  walk of the table, forward 6/11, backward 1/11) and which the open
  boundary drains; so the exponent clause is expected to fail at these r,
  and by more than the box and the transient account for. The run measures
  it in the engine exactly; nothing is tuned to pass.
- **Deviations from the plan above, each stated before the run.** (i) The
  amount is 2^28 at `release` [1, 65536], not 2^20 at [1, 256]: the same
  4096 quanta per heading per interval, and the body's axis accumulator,
  which adds the register every interval and steps a Link at a whole
  amount, stays far below a Link (F t²/2 ≈ 6 × 10^5 at r = 4 over 40
  ticks, against 2^20 ≈ 10^6, which a longer run would have crossed); (ii)
  the margin is 5, not at least 8, and the ticks 2r + 32, not at least
  2r + 64, by the cost above (the largest worlds, r = 16 and d = 8, about
  8 to 10 minutes each); the mean field puts the cost of the smaller box
  and the shorter run at 1 % of F at r = 4, 5 % at r = 6, 10 % at r = 8, 27
  % at r = 12 and 46 % at r = 16 against the plan's settings, which
  themselves sit 40 % below the free-space steady state at r = 16; the
  far points are transient readings either way, and the per-tick series
  shows it; (iii) N = 2^3, the reference Born width, since the coherent sum
  of a spread costs one pass over the circle per register and no phase is
  read; (iv) the control's table names its own light, which no two-body
  world's does (the plan's "same settings" would leave its table empty and
  the clause vacuous): so the clause tests the symmetry of the returning
  field, and the two-body worlds omit each body's push by its own
  returning light, which under the catalog's single light family would
  add the shadow of the other body's sink in that returning field to the
  force, not measured here; (v) one unseeded lamp per light family, an
  emission of amount 1 with `recoil_field` momentum that is never seeded,
  binds the momentum field to the light, the engine's one way to bind it,
  so that the ledger carries the momentum line (its every value is zero by
  the mirror symmetry of each world, which is what it then shows); (vi)
  the opposite-charge series is expected to be the exact negation of the
  like-charge series, tick by tick, since the two light fields are the same
  in both and only the tables' sign differs; it is run in full as planned
  and the clause reads the equality.
- **Deviations seen in the run, stated after it.** (vii) The front: the
  entry above says the front reaches the other body at tick r and the
  axis is lit at once; so it is for r ≤ 12 (the first push on B at tick
  4, 6, 8 and 12), but at r = 16 the forward share that never scatters,
  4096 × (6/11)^15 = 0.46 quanta per interval, is below one quantum, so
  the first quantum reaches B at tick 18 (tick 19 on the diagonal at d =
  8), through the remainder registers. (viii) The records were made in
  two sittings of one runner script (two worlds at a time, each world in
  its own sibling record directory): ten records in the first sitting;
  the session was then resumed while the first sitting's runner was still
  working, and the resumed runner's collision with it (each deletes an
  incomplete record directory before it runs) destroyed the record
  directories of `pp_r4` and `pe_r4` (both sittings' attempts, the engine
  refusing the second lease: "artifact path already has an active
  writer", "artifact path was replaced during its writer lease") and the
  first sitting's `run.json` of `pe_r6` and `p_alone`; these four were
  run again from the same world files under the same source (the
  fingerprints below are the records'), their viewer documents extracted
  from the re-runs; `pp_r6` is the first sitting's. (ix) After the run
  the analyzer's clause-4 entry was found to have its list of (r, F)
  points overwritten by the fit's count of the same name (`points`); the
  list's key was renamed `series` and the record rewritten from the same
  runs, no number changed.
- **Status.** measured on 2026-09-17, commit
  `b701ea779d14c7aa319c58f67db324b8802f29c5` (`main` at `1868324` with
  this entry planned; no engine change), source
  `4c6e313ce9f0b14be95ce85b3c4f256d4072f2e81715ddf1f1071b44c11d33bb`;
  initialization fingerprints, like charges r = 4, 6, 8, 12, 16:
  `58abf9051ab315163b5cf08d906271568155d63fab05f75845d18ad524cccdab`,
  `b1d3ca6d0318b9834f6ed6886b44698c029a4aee993707c757d1b03c5e57f4a0`,
  `e1dd71bda82ee646dd792603a101f072403d66aa5beee416bc24ecc64d4324ea`,
  `2f47e912389aedf19d8e3c542ddf420f5e507f827e90c68eebfa0243f7887658`,
  `624292813b31ac95fa60b6287b9a6dd869f345fe1936e777960c2327af933cb1`;
  opposite charges r = 4, 6, 8, 12, 16:
  `1037e95e2ad521ad132612644496839ce9478756cbc5314acde078472e8292e2`,
  `86fc91c11af22769fde7f3a57321dd18900d83a41caf9b9fe113d8184230a302`,
  `47bf17836e2fe9022cac235013b8be14303975692ccffab8f8845f52fdc3866c`,
  `437448ce62dd153c68468b8ff2de59da0b5284acbc5f29b56bfbb5977b917096`,
  `ef3cbe5d76c988e56126a3f57f01029d4042c1ad09a0fd850fbeb0bdd044cc24`;
  the diagonal d = 3, 4, 6, 8:
  `fabca15ee719b60cb8b73c104a13487956dc1391c9a5bf19796fcc60814e43d0`,
  `0772cb34169010481b5aa09dc904e6d604301b5ea4fb5319e5aa06bc675b1247`,
  `54c30a7cd8ac5e280b586ce1a1d69e2f68cb035fec58b1a469f4e9ab038b7f19`,
  `7a1b520bc7232128917bdc9223190b425033a31066ce2b7ee021d8a5a2dbecc8`;
  the control
  `150c99afb724cb0ade43920a2046afda80c95773a4922324502f2921cdd7479a`;
  outcome: fail, the exponent clause (4), with (1), (2), (3) and (5)
  passing and (6) reported: (1) every ledger line balanced and
  `conserved_at_every_completed_tick` true at every tick of every world
  (at the end of `pp_r4`, `light_a` sourced 983040 = current 421226 +
  escaped 383590 + absorbed 178224; the momentum line and the bodies'
  momentum line (0, 0, 0) throughout); (2) the control's register (0, 0,
  0) at every tick, with 378 absorptions of its own light; (3) the two
  registers equal and opposite at every tick of every two-body world; (4)
  F(r) on B, the mean push per interval over the last 32 ticks, 742.81,
  252.81, 89.75, 13.19 and 2.41 quanta per interval at r = 4, 6, 8, 12,
  16 (the window sums 23770, 8090, 2872, 422, 77; r²F 11885, 9101, 5744,
  1899, 616), exponent −4.14 ± 0.37, outside −2.0 ± 0.2; (5) like charges
  apart (A's push on −X, B's on +X) and opposite charges together at every
  r, the opposite-charge series the exact negation of the like-charge
  series tick by tick; (6) the diagonal, B at (d, d, 0): |F| = 133.42,
  66.69, 19.75 and 6.98 at d = 3, 4, 6, 8 (Euclidean 4.24, 5.66, 8.49,
  11.31) against the axis fit at the same distance 849.2, 257.9, 48.09
  and 14.61, the ratios 0.157, 0.259, 0.411 and 0.478, the push along the
  diagonal exactly (the window sums 3019, 1509, 447, 158 on both axes, 0
  on z). The fail is the one the mean field predicted, to within a
  quantum per interval (predicted 742, 252, 89, 13.1, 2.4; −4.2 ± 0.4;
  the ratios 0.16, 0.26, 0.41, 0.47): at these r the force falls like the
  forward share that never scatters, 4096 × (6/11)^(r−1) = 665, 198, 59,
  5.2 and 0.46 (the rest of F, 78, 55, 31, 8.0 and 1.9, is the scattered
  field, drained by the open boundary and still rising at the far r),
  that is, the short range of the declared table and not the box or the
  transient alone (the mean field at the plan's settings gives −3.7 ±
  0.3, in free space at its steady state −3.2 ± 0.1). The records stay
  outside the tree; `record.json` holds the integers and the
  README the
  tables. Run times with two runs in parallel on four cores shared with
  other work: 156, 197, 239, 341, 448 s for the like-charge axis worlds,
  154, 328, 247, 342, 443 s for the opposite-charge ones, 209, 264, 396,
  570 s for the diagonal, 111 s for the control.
- **Computed after the run (2026-09-17;
  `examples/nature/a5_static/mean_field_gauss.py`, a computation, not an
  engine run).** Method: the table's mean field, per-heading amounts on the
  cubic GameBoard in floating point (the split is exact on average under the
  remainder rule, so this is the expectation of the engine's integers), the
  source releasing 4096 on each heading every interval and absorbing what
  returns to it, a sink absorbing everything that arrives and booking amount
  × heading, the open faces absorbing, the steady states solved as the fixed
  points of the linear map (BiCGSTAB, residual 10^−10) and the transients
  stepped; the source alone in an octant of the cube of half-width 96
  (193³, the boundary 2r beyond r = 48), the simple walk [1, 1, 1, 1, 1, 1]
  in the same box for the GameBoard Laplacian's Green's function, and the
  sink at r = 4, 6, 8, 12, 16, 24 and 32 with the boundary 2r from both
  bodies (3r and 4r checked at r = 8, 12, 16). Verdict: the table gives
  Gauss's law, exactly for the Link current through every closed surface
  and as 1/r² on the axis from r ≈ 21 on, reached after about 1.5 r²
  intervals, while the run's window r = 4 to 16 is the beam's and shows −2
  at no box size and no duration. What it gives, in order. (1) Free space:
  the effective source S = 20132 per interval (24576 released, 4444
  returning to the source's sink); the outflow through the cube of
  half-width r equals S to 10^−7 at r = 2 to 64, Gauss exact on the GameBoard
  by conservation. The net momentum arriving at a Node, J (amount × heading
  of the arrivals, what a sink absorbs and a met ray feels), is exactly 11/8
  of the mean Link current through it, Φ, at every Node: on any axis the two
  Links' currents sum to J + (g₊ − g₋) = J (1 + 5/11), the transverse shares
  cancelling, so J = 2 Φ / (1 + c) with the table's persistence cosine c =
  5/11 (2 Φ for the simple walk). Gauss's S/(4π r²) is the Link current, and
  on the axis Φ/(S/4π r²) = 5.09, 4.12, 2.91, 1.58, 1.19, 1.05, 1.03, 1.02
  at r = 4, 6, 8, 12, 16, 24, 32, 48 (J: 7.00, 5.67, 4.00, 2.17, 1.64, 1.45,
  1.41, 1.41); on the (1, 1, 0) diagonal Φ is 1.01, 0.99, 0.99 of Gauss at
  r = 11.3, 22.6, 33.9 and on the (1, 1, 1) diagonal 0.93, 0.97, 0.98 at r =
  13.9, 20.8, 27.7: the current is isotropic to 5 % from r ≈ 24 and to 3 %
  from r ≈ 30. The density is the GameBoard Laplacian's Green's function
  scaled by D_simple / D = 3/8, within 1.5 % from r = 20 and 1 % from r =
  31 (D = 4/9 Link² per interval). The beam 4096 (6/11)^(r−1) is 0.95,
  0.78, 0.59, 0.22, 0.045 and 0.0009 of J at r = 4, 6, 8, 12, 16, 24 and the
  scattered part exceeds it from r = 9; the log-log exponent of J over
  windows of r: 2..4 −1.55, 3..6 −2.24, 4..8 −2.81, 6..12 −3.41, 8..16
  −3.31, 12..24 −2.55, 16..32 −2.19, 24..48 −2.04 ± 0.004; the local
  exponent stays within −2.0 ± 0.2 from r = 21 on and within ± 0.1 from r =
  26 on; over the run's r = 4, 6, 8, 12, 16 it is −3.11 ± 0.11. (2) The
  sink: F = 753.10, 269.09, 106.11, 25.32, 10.67, 4.149, 2.272 per interval
  at r = 4, 6, 8, 12, 16, 24, 32 (r² F = 12050, 9687, 6791, 3647, 2731,
  2390, 2327), F/J = 1.07 to 1.03 (the sink's own shadow), the boundary at
  3r and 4r raising F by 0.4 and 0.5 % at r = 8, 1.2 and 1.5 % at r = 12,
  1.7 and 2.2 % at r = 16; the exponent over r ≥ 12 is −2.44 ± 0.13, over
  r ≥ 16 −2.24 ± 0.07 (−2.09 between 24 and 32), and over the run's r = 4
  to 16 at steady state −3.14 ± 0.11: the run's window shows the beam at
  any box size and any duration. (3) The time to 90 % of the steady push,
  t90 = 6, 16, 44, 164, 354, 866, 1564 ticks at r = 4 to 32 (t50 = 4, 6, 8,
  34, 94, 246, 450; t99 = 22, 74, 170 at r = 4, 6, 8 and beyond 3 r² + 64
  ticks from r = 12), t90 / r² rising to 1.53 at r = 32 against the
  continuum's 1.93 r² for D = 4/9, t90 ∝ r^2.29 ± 0.09 over r ≥ 12 and
  r^2.76 ± 0.10 over all r (the near r are the beam's, at tick r + 2); at
  the run's 2r + 32 ticks the push is 99.8, 97.5, 91.5, 65.2, 35.3 % of the
  steady state at r = 4 to 16 and 7.8, 1.5 % at r = 24, 32, at the plan's
  2r + 64 ticks 100, 99.1, 95.8, 77.8, 51.4, 16.8, 4.4 %. (4) The beam is
  0.883, 0.735, 0.555, 0.206, 0.043, 0.0009 and 0.0000 of F at r = 4 to 32;
  the rest, (F − beam) r² = 1414, 2568, 3025, 2897, 2613, 2388, 2327, is the
  diffusive field, converging from above to about 11/8 × 1.03 × S/(4π) ≈
  2300. At the engine's measured 2.3 ms per Node cycle, a world with the
  boundary 2r away run to t90 costs 342 k Nodes × 354 ticks ≈ 78 hours at
  r = 16, 1.14 M × 866 ≈ 26 days at r = 24 and 2.68 M × 1564 ≈ 110 days at
  r = 32: the field of a charge at rest is established, in this table's
  sense, at no r the engine reaches today, and the exponent clause can be
  met only from r ≈ 24 up. CPU: 607 s for the four computations and 244 s
  for the free-space part with its Link-current column, on one core.
- **Run 2, to the steady state (dense mode), planned before the run
  (2026-09-17).** The same two bodies under the dense mode (`dense_field:
  true`, `dense-field-v1`, PR #251, [the dense
  mode](SPATIAL_FIELDS.md#the-dense-mode-dense-field-v1): the pure-field
  Nodes cycled as one vectorized step with the same integers, `state.json`
  and the ledger byte for byte the engine's), which makes the boxes and
  durations of the computation above feasible: the boundary 2r from both
  bodies, the box [5r + 1, 4r + 1, 4r + 1] with A at (2r, 2r, 2r) and B
  at (3r, 2r, 2r), run for t90 + 32 ticks, t90 the first tick at which the
  mean field's push in that box reaches 90 % of its steady state (t90 ∝
  r^2.29 over r ≥ 12): like charges at r = 12, 16, 20 and 24
  (`pp_r{r}d`: [61, 49, 49] for 196 ticks, [81, 65, 65] for 386, [101,
  81, 81] for 622, [121, 97, 97] for 898), opposite charges at r = 16 for
  the sign (`pe_r16d`, 386 ticks) and the control alone in the cube of r =
  16's margin, 65³, for 386 ticks (`p_alone_16d`, its register zero by
  symmetry as in Run 1); the six worlds written by `make_worlds.py`
  beside the fifteen of Run 1 (`dense_cases`), the mode's admission met
  (no `conservation` key, no polarization, no ray interaction, one Node
  worker), and run one at a time, smallest first (r = 12; r = 16 like,
  opposite, the control; r = 20; r = 24 last and only if the machine has
  8 GB available when its turn comes). Memory, measured before the run on
  the r = 12 GameBoard: the dense arrays and their temporaries cost about 6
  KB per Node (the 16-tick run peaks at 1.0 GB) and the runner's final
  snapshot, `state.json`, every filled Node read back as Node state and
  written as text, about 16 KB per filled Node (an 80-tick run with
  62 k of the 146 k Nodes filled peaks at 1.9 GB), so a full GameBoard peaks
  at about 22 KB per Node: 3.3 GB at r = 12, 7.8 at r = 16, 3.1 for the
  control, 15 at r = 20 and 26 at r = 24, against 16 GB on the machine;
  the series script runs a world only if the available memory covers its
  projection when its turn comes, so r = 20 is a borderline attempt and
  r = 24 cannot run on this machine until the runner writes the snapshot
  Node by Node (a runner change, not made here). Smoke test before the
  run: the r = 12 world's document for 16 ticks with the key and without
  it gives the same `state.json` (SHA-256
  `ab54313628ce06f00598ea1be3c8c87a7f78f3b340531005491e93eda93108e7`),
  the same ledger, totals and body registers (B's register (29, 0, 0)
  after tick 16, the first push at tick 12), in 63 s against 76 s (at 16
  ticks the field covers about 7 k of the 146 k Nodes; the engine alone
  would cost about 5 minutes per tick once the GameBoard is full). Predictions,
  written before the run by `predict_dense.py` into `predictions.json`
  beside the worlds (the mean field of `mean_field_gauss.py` at exactly
  these boxes and ticks, the push averaged over the last 32 ticks as
  `analyze.py` reads it): F(r) = 23.137, 9.675, 5.604 and 3.747 quanta per
  interval at r = 12, 16, 20, 24 (r² F = 3332, 2477, 2242, 2158), 91.4,
  90.7, 90.5 and 90.3 % of the box's steady state 25.324, 10.668, 6.193
  and 4.149, the window before the last one 22.400, 9.519, 5.548 and
  3.721 (the push still rising by about 1 % per 32 ticks at t90), t50 =
  34, 94, 164, 246; the first push at tick r in the mean field, the beam
  5.21, 0.46, 0.041 and 0.0036 quanta per interval, below one quantum
  from r = 16 (in Run 1 the first quantum reached B at tick 18 at r = 16,
  through the remainder registers, and it will come later still at r =
  20 and 24: reported, not a clause); the log-log exponent of the
  predicted F over r = 12, 16, 20 is −2.79 ± 0.16 and over 12, 16, 20, 24
  −2.63 ± 0.14 (of the steady state in the same boxes −2.77 and −2.61).
  The mean field's asymptote is −2: the local exponent of the box's
  steady push is −3.01, −2.44, −2.20 and −2.09 between r = 12 and 16, 16
  and 20, 20 and 24, 24 and 32, and in free space the local exponent of
  the axis flux stays within −2.0 ± 0.2 from r = 21 on and within ± 0.1
  from r = 26 on (the computation above); so at these r the run reads the
  approach to Gauss's law, not its asymptote, and the criterion is the
  agreement with the mean field, the expectation of the engine's
  integers, clause by clause. Criterion, pre-registered, pass, all of:
  (1) every ledger line balanced and `conserved_at_every_completed_tick`
  at every tick of every world; (2) the two registers equal and opposite
  at every tick of every two-body world, the control's (0, 0, 0) at every
  tick; (3) the engine's steady-state push F(r) on B, the mean over the
  last 32 ticks, equals the prediction above within 3 % at every r run;
  (4) the log-log exponent of F(r) over the r run (12, 16, 20, and 24 if
  run) equals the mean field's over the same points, −2.79 (−2.63 with r
  = 24), within ± 0.1, the asymptote −2 stated beside it with the r from
  which it holds; (5) the opposite-charge series at r = 16 the exact
  negation of the like-charge series, tick by tick. Fail: any of the
  five, stated as which and why (the remainder rule's integers against
  the mean, the box, the transient, or the mode); nothing is tuned after
  the fact. `analyze_dense.py` evaluates the five clauses from the
  records against `predictions.json` (a run not yet made is reported as
  missing). Expected cost at the measured 26 µs per Node and tick: 12
  minutes at r = 12, 57 minutes each at r = 16 (the control, one family,
  about 23), 3 hours at r = 20 and 7.4 hours at r = 24, about 13 hours in
  all; initialization fingerprints, `pp_r12d`, `pp_r16d`, `pp_r20d`,
  `pp_r24d`, `pe_r16d`, `p_alone_16d`:
  `722fd4815761d5dd27416d4785543eb2bb1c05193c2a185a23acfdbeb2f1163d`,
  `9bd1c35590668b892be8492ac6c65fbe8a311003cb49aca00ab59f7f4b38ebbf`,
  `0a249b0f7134f16695f7d4df3feb76186ffbae9d771e35feb49b99d9a45b7e1b`,
  `7c91c70988cc45e0459cf255af68bd3c0969a870043a49c7ac354f2556e08add`,
  `470b1f5e5c693edd2a3f4efa7ae02b437a425a4d08994f367bcd468ace321d22`,
  `20943c970bc264e33bf5cf3c776381a0b5eda9d81a3350b3f892e2fe68e03599`.
  Status: launched on 2026-09-17 (the engine of `main` at `c879d9e`, no engine
  change on the branch); measured on 2026-09-18 for r = 12 and 16 at commit
  `f6196d4e37ede23a1e06092abab5bc8d4773f8df`, source
  `25ecd24e87cea58753089a9b38c0d21620ec0eae8401a17d2b55b6352883f038`
  (`pp_r12d` 843 s, `pp_r16d` 4249 s, `pe_r16d` 4185 s, `p_alone_16d` 1655
  s; the numbers in `record_dense.json`): (1) pass, every ledger line
  balanced and `conserved_at_every_completed_tick` at all 196, 386, 386 and
  386 ticks; (2) pass, the registers equal and opposite at every tick (final
  (-3502, 0, 0) and (3502, 0, 0) at r = 12, (-2692, 0, 0) and (2692, 0, 0)
  at r = 16), the control's (0, 0, 0) at every tick with no push; (3) pass,
  F = 23.156 at r = 12 against the predicted 23.137 (0.08 % away; the window
  before 22.406 against 22.400) and F = 9.6875 at r = 16 against 9.675 (0.13
  %; the window before 9.500 against 9.519): the engine's integers reproduce
  the mean field to a part in a thousand; the first quantum reached B at
  tick 12 at r = 12 (the beam) and at tick 18 at r = 16 (through the
  registers, as Run 1 saw); (4) not yet evaluable with two points (the
  two-point slope -3.03, the mean field's -3.03 over the same points); (5)
  pass, `pe_r16d` the exact negation of `pp_r16d` tick by tick (final
  registers (2692, 0, 0) and (-2692, 0, 0)). Run times 14, 71, 70 and 28
  minutes, peak memory 7.9 GB at r = 16 (the runner's final snapshot);
  `pp_r20d` launched at 23:51 with 14 GB projected against 15 available,
  `pp_r24d` skipped for memory; the series was relaunched twice after the
  machine restarted; `pp_r20d` completed its 622 ticks (14313 s; the last
  tick's records written at 03:49 UTC on 2026-09-18) and the runner was
  killed by the memory cgroup while writing the final snapshot (exit 137,
  11.4 GB resident against the 15 GB limit), so it has `events.jsonl`
  (SHA-256 `b08ee36382f89aaf3cff4b1c0edd252a86872c53da05dd7f87c50cfa5a80399a`)
  and `initialization.json`
  (`0a249b0f7134f16695f7d4df3feb76186ffbae9d771e35feb49b99d9a45b7e1b`) but no
  `run.json` and no `state.json`, and `record_dense.json` reports it missing.
  Read from the events alone by the same rule as `analyze.py` (the register
  of each body after each tick from the `external_body_absorbed` records,
  13888 of them, the last at tick 622; the steady push the mean over the
  last 32 ticks): (2) the registers equal and opposite at every one of the
  622 ticks, final (-2433, 0, 0) and (2433, 0, 0); (3) F = 5.594 at r = 20
  against the predicted 5.604 (0.18 % away; the window before 5.563 against
  5.548), the third point of the part-in-a-thousand agreement; (4) pass,
  the log-log exponent over r = 12, 16, 20 is -2.793 ± 0.161 against the
  mean field's -2.788 ± 0.165 over the same points (the local slopes -3.03
  and -2.46 against -3.01 and -2.44), 0.005 apart, within the clause's 0.1;
  the asymptote stated beside it as the plan requires: the mean field's
  local exponent in these boxes -2.20 at 20 to 24 and -2.09 at 24 to 32, the
  boxes' outward dilution, the free-space law approaching -2 from below
  (the mean-field research entry); (1) not evaluable at r = 20 without the
  ledger (the audit lives in `run.json`; at r = 12 and 16 every line
  balanced); (5) unchanged. `pp_r24d` was skipped by the memory rule
  (projected 25 GB against 12 available) and the series ended there
  (`SERIES_DONE` at 03:49 UTC); r = 24 waits for a runner that writes the
  snapshot Node by Node.
  The records stay outside the tree.

### A5s repeated under the law of the bit (2026-09-18)

- **Claim.** Coulomb's law between two things at rest, confronted on the
  engine under the law of the bit (Highlights 5.4; features 15 to 18, 16d
  parts 1 and 2, 16e, 16f and the cleanup on `main` at `1a88785`) against
  round 4 of
  [DERIVATIONS](DERIVATIONS.md#31-round-4-coulomb-and-newton-under-the-mixed-field)
  (section 31: the product law k_C q_A q_B / r^2 with k_C = G, a fixed
  GameBoard anisotropy (15/8) omega^2 K_4, the retardation sqrt 3 r, a clock
  required on the source and 256 quanta per Node at the receiver; section
  32: the third law exact through the field, the recoil arriving at the
  owner; section 30: the wave alive above about 256 quanta per Node), on the
  closed GameBoard the model owner decided the confrontation runs are made on,
  with only closed worlds tested (Highlights 5.4, "The GameBoard of a run is
  closed", PRs #311 and #314): the push per interval on each of two bodies
  at rest once the field has settled, its scaling with the distance d, the
  product law over three pairs of contents, and the recoil arriving through
  the field, with the two things' momentum lines and the shadows' in-flight
  momentum summing to zero at every interval. Nothing is registered as a
  law; what came out is recorded.
- **Features.** 15, 16b, 16c, 16d (parts 1 and 2), 17, 18, the cleanup, the
  dense mode, the standing-set search and the series runner, as E11 repeated
  above; 16e and 16f present and not declared.
- **Run.** `examples/nature/a5s_law/` (eight closed worlds written by
  `make_worlds.py`, the dictionary in the
  README),
  on the law as E11 repeated: `N` 64 declared once, K 1, `wait_per_quantum`
  1, the dense mode, no retired key, `boundary` periodic, 120 ticks,
  `standing_field` on, a margin of 12 empty Nodes beyond each body (the
  image of B across the boundary 25 Links from A on the axis, 18.4 and 22.5
  Links off it). Two external bodies of the `proton` family, A of 2^28
  (whole charge 3 x 2^28) at (12, 12, 12) and B at A + (d, 0, 0) for d = 4,
  6, 8, 12 (`pp_d{d}_closed`, the GameBoards [d + 25, 25, 25]), at A + (8, 8, 0)
  and A + (8, 8, 8) (`pp_d8_110_closed`, `pp_d8_111_closed`, r = 11.31 and
  13.86), and at d = 8 the pairs of contents (2^28, 2^27) and (2^27, 2^27)
  (`pq_d8_closed`, `qq_d8_closed`; 2^26 was the first choice and is refused
  by the prefill at fill 12, a third phase on one Port of a source). Each
  body's shadow set is given with the GameBoard by `initial_field` `{"fill": 12}`
  with `release` [1, 512]: 37748736 quanta for 2^28 and 18874368 for 2^27,
  both sets in one family told apart by their owner. Each body's
  `momentum_table` `{"proton": 1}` is read by charge (point 16: sign x
  amount x heading x (the owner's charge over its content) x the charge per
  quantum of what is pushed, 3 x 3 = 9 per shadow quantum here, repulsion);
  a shadow of its own owner is home and never a push, and every shadow that
  pushes turns back with the opposite sign carrying -dp (point 3). The push
  per interval on each body is the change of its momentum per tick, read
  from the runner's `momentum` line (things 2 and 3); the momentum in flight
  on the shadows is read by `analyze.py` replaying every world in-process
  (every shadow's `momentum` on its way and parked, from the layer's arrays
  and the engine's Nodes; the runner's ledger line of the momentum field does
  not sum the momentum carried on rays, so the world's zero is read there),
  the replay's momentum lines checked against the record's tick by tick and
  the reading checked against the inventory view on one world. The push per
  interval is reported per window of twenty intervals and settled as its
  mean over ticks 101 to 120 with its standard error and the settling tick
  (the first from which every later window of twenty stays within 10 % of
  the last); the scaling with d is the log-log least-squares slope over d =
  4, 6, 8, 12 of the settled push; the anisotropy is the (110) and (111)
  worlds against the axis fit at the same Euclidean distance; the product
  law is the settled push on each body at d = 8 over the three pairs,
  against the product of the whole charges and against each body's own and
  the other's charge. The bodies' rest is read from their positions per
  tick. The records were made with `tools/run_series.py --jobs 4` on the
  dedicated machine (703 to 1319 s per axis world at four at a time, 2.5 to
  2.9 GB peak; the three 33^3 worlds were killed by the machine's memory
  limit at four at a time beside the replays and were run again two at a
  time), the `run.json` of every world kept gzipped in `records/` beside the worlds,
  the readings in `record.json` and `tables.md`, the page in `a5s_law.html`.
  The open-GameBoard form of the eight worlds, written first as the control, was
  dropped before it ran by the model owner's decision of the same hour that
  only closed worlds are tested (PR #314). Stated before the run: E11
  repeated above shows that on the closed GameBoard the prefilled field of a
  thing at rest is a train that circles the periodic GameBoard at about 1 /
  sqrt 3 Link per interval and reconverges at its owner once per round trip
  of 57 intervals, without a fixed point or a cycle within 120 ticks; so
  "once the field has settled" is read as the last window of twenty, with
  its time course beside it.
- **Result (partial: seven of the eight worlds recorded, one replayed).**
  The series stopped on the model owner's word before it was complete:
  `pp_d8_111_closed` (the 33^3 GameBoard, 5.0 GB at peak) was killed twice by
  the machine's memory limit beside the other jobs and its third run, alone,
  was stopped; the other seven worlds completed, and `pq_d8_closed` alone
  was replayed for the momentum in flight. Per prediction, whether the
  engine gave it, with the number. *The books:* given. Every ledger line
  per bit balanced at every tick of the seven worlds, nothing escaped, both
  sets constant to the quantum (75497472, 56623104, 37748736), both bodies
  at rest at every tick. *The third law through the field:* given exactly
  in the books where read: in `pq_d8_closed` the two bodies' momenta plus
  the momentum in flight on the shadows sum to zero at every one of the 120
  ticks (at tick 120: A +43116, B -72623, the shadows +29507 on x), the
  replay's momentum lines equal to the record's; in the like pair at d = 8
  the pushes on A and B are equal and opposite at every interval (the
  windows -2725 against +2700, -2606 against +2689, ..., +18291 against
  -19126), and the bodies' momenta do not sum to zero on their own (-28195
  on x at tick 120 for d = 8, -12699 for d = 4, +19048 for d = 12), the
  rest in flight on the shadows. *The standing set:* not reached, as in E11
  repeated: no fixed point and no cycle within 120 ticks in any world (the
  residual at the last comparison 92.4 to 93.4 M quanta moved per interval
  out of 75.5 M on the GameBoard for the like pairs, 70.2 M of 56.6 M and 47.1
  M of 37.7 M for the others); the push never settled (no two consecutive
  windows of twenty within 10 %). *The push once settled and its scaling
  with d:* not given. The push per interval on B along the line from A,
  positive away from A: in the first twenty ticks, the train's first
  passage, +42135, +7248, +2700 and +363 at d = 4, 6, 8, 12 (repulsion; the
  train reaches d = 12 at tick 6; a log-log slope of about -4.3 over d, the
  front of the train and not a far field); afterwards the sign turns: the
  windows of twenty at d = 4 read -765, -3846, -42680, -6783 and -13059 +-
  8185 (ticks 101 to 120), at d = 6 +5964, -2078, -12285, -6432, +14940 +-
  10704, at d = 8 +2689, +4541, +14681, -8918, -19126 +- 9765, at d = 12
  +925, +5609, -9163, -10615, -4784 +- 4263: on the periodic GameBoard A's
  train comes around from the far side (A's image 25 Links beyond B on the
  axis) and pushes B toward A, B's train pushes A likewise, and the two
  bodies of every pair are pushed toward each other over most of the run
  after the first passage; the sign changes 46 to 60 times in 119
  intervals. The log-log slope of the settled push (101 to 120) over d =
  4, 6, 8, 12 is -0.80 +- 0.74 in size with mixed signs, against -2 for
  Coulomb; the (110) pair at r = 11.31 reads -2269 +- 2094 (its first
  window +8892) against the axis fit's 7807 in size. *The product law:*
  not given; a sum law instead. At d = 8 the settled push on B is -19126
  for the pair (2^28, 2^28), -19147 for (2^28, 2^27) and -9359 for (2^27,
  2^27), the ratios 1.000, 1.001 and 0.489 where the product of the whole
  charges gives 1, 0.5 and 0.25; the push on A 18291, 9304 and 9333, the
  ratios 1.000, 0.509 and 0.510: the push on each body is proportional to
  the other body's content (its shadow set) and independent of its own,
  and the same in the first window (2700, 2700, 1110 on B; -2725, -1123,
  -1123 on A). The engine's electricity reading multiplies a shadow's
  amount by its owner's charge over its content and by the charge per
  quantum of the family of what is pushed (3 for every proton body here),
  not by the pushed body's whole charge; the model owner's amendment of
  point 16 the same day ("charge per thing", PR #317: the charge of a thing
  is one declared number of its family, whatever its content) names the
  whole charge, so this is a finding about the engine's reading against
  the amended rule, recorded and not patched in a run lane. *The
  anisotropy and the retardation:* the (111) pair was not recorded; the
  (110) pair's first push arrives at tick 6 for r = 11.31 as at d = 12 on
  the axis (sqrt 3 r = 19.6 and 20.8; the fill's train starts 7 Links out).
  *Cost.* 703 to 1319 s per world at four at a time (2.5 to 2.9 GB peak),
  913 and 738 s for the (110) pair and d = 12 at two at a time (3.7 and 3.2
  GB); the inventory replay of `pq_d8_closed` 120 ticks at about 10 s per
  tick.
- **Reading.** On the closed GameBoard two things at rest do not push each
  other by a settled force: each reads the other's train as it passes and,
  after one round trip of the periodic GameBoard, as it comes around from the
  far side, so the push alternates and turns toward the other body, with no
  scaling law in d and no settled value within 120 ticks; the books per bit
  close at every interval and the third law holds exactly through the
  field, the recoil in flight on the shadows. The product law is not read:
  the engine's charge reading gives each body a push proportional to the
  other's shadow set alone, a sum law, which the amended point 16 does not
  intend. The same evening the model owner reversed the rule the series was
  made under: a thing emits, nothing is given with the GameBoard, the GameBoard of
  a run is open (Highlights 5.4, "A thing emits; nothing is given with the
  GameBoard", PR #319), and the series is repeated after feature 19 with the
  emitted field and its fixed point.
- **Fingerprint.** Source
  `051d716825c4785baffba01e46ea7348698fdfe82ca9ddc70eafab9871a49be5` (the
  package of `main` at `1a88785` merged into the branch, as E11 repeated; no
  engine change on the branch), the initializations in
  `examples/nature/a5s_law/records/*.json.gz` (the `run.json` of the seven
  recorded worlds, `initialization_sha256` inside each), the worlds the
  files beside them at this commit less the family key `ray_slots`, retired
  by `main` after the runs (PR #315; the physics unchanged);
  `pp_d8_111_closed.json` written and not recorded.
- **Status.** partial, measured on 2026-09-18 for seven of eight closed
  worlds at the fingerprint above, one replayed for the momentum in flight;
  recorded here; superseded the same evening by the model owner's decision
  that a thing emits and the GameBoard is open (PR #319): to be repeated after
  feature 19. Nothing is registered as a law.

### A6. Light bending by a bound group and G_eff N² over N = 2^8 to 2^16

- **Confronts.** The deflection of light by a mass, α = 4GM/(c² b) for
  impact parameter b (1.75 arcsec at the solar limb, Dyson, Eddington and
  Davidson, 1920; the post-Newtonian γ within 2 × 10^-4 of 1 by VLBI,
  Shapiro and others, 2004): inversely proportional to b, linear in M, and
  twice the Newtonian value for a slow body at the same b.
- **Model prediction today.** Highlights 3.28: gravity is bending by delay;
  the retained content of a Node (its mass) makes it slow, the information
  that it is heavy spreads in ray form in all directions, a met ray is
  delayed more on its nearer side and bends toward the heavy Node, and the
  field ray returns with the opposite momentum; nothing is inserted as a
  force and momentum is exact. On the ladder of
  [hypothesis 12](HYPOTHESES.md#12-one-mass-ladder-and-the-composite-spectrum-from-binding),
  m₀ = h/(N δt c²), the model owner's statement of 2026-09-17 is
  G = ħc/(N m₀)², N m₀ the Planck mass, so that the coupling measured in
  GameBoard units scales as 1/N²: G_eff · N² is constant across the phase
  width. This statement is not yet in Highlights or on the hypotheses page;
  the run pins it as stated.
- **Features.** 1, 2, 5, 6, 7, 7b, 8, 9, 10, 12.
- **Run.** A GameBoard of 65 × 65 × 9 Nodes, open boundary. The star at the
  center: an external body (feature 7b, `external-body-v1`, Highlights 3.19)
  of declared family and amount M, no charge, at rest (`initial_momentum`
  zero), at its default coupling, absorption into its explicitly accounted
  sink (the mirror, beam-splitter, phase-plate and polarizer couplings are
  not used here); its motion is caused by fields only (model owner,
  2026-09-17): every recoil field ray that returns to it changes its
  momentum by its coupling table and is booked on the audit's bodies'
  momentum line, and its velocity, momentum over amount M, is an exact
  accumulator that completes no Link during the run at this M, so against
  the light ray it stands still; its computation field released in all
  directions (3.28); one control series with the same M declared instead as
  an ordinary bound group of declared families with retained content M
  (feature 8), when the star's recoil is wanted; a light source
  (marked, setting 1) launching one light ray on a line parallel to x at
  impact parameter b = 4, 6, 8, 12 and 16, one ray per run, on both sides
  of the group, and the same passes on lines parallel to the (1,1,0)
  diagonal at equal Euclidean b rounded to the GameBoard (Highlights 3.5,
  2026-09-17: the field is a diamond at the scale of Links and a sphere at
  large scale by path counting, and the axis-versus-diagonal bending is a
  measurable prediction, not an assumption); a slow massive ray (rate r,
  content equal to the light ray's)
  on the same lines; a control run with no group. The phase width N = 2^8,
  2^10, 2^12, 2^14 and 2^16, with the group's retained content M fixed at
  2^6 units of m₀ = 1 phase step per interval (its rate 64 steps per
  interval at every N); M doubled once at N = 2^12. The delay table of the computation
  field is a declared integer table written before the run. Recorded: the
  ray's heading and momentum components before and after the pass (the
  deflection α from the integer heading), the delay k_out incurred per Node,
  the returning field rays' momentum delivered to the body (the audit's
  bodies' momentum line and its accumulator per tick; in the bound-group
  series, the group's momentum per tick), the audits. G_eff(N) := α b /(4 M)
  with M in units of
  m₀ and α in radians from the heading change.
- **Criterion.** Pass, all of: momentum exact at every tick over the ray, the
  body's momentum line (the group, in the bound-group series) and every
  field ray; the control goes straight; the ray bends toward the body on
  both sides; the
  log-log exponent of α over the five b is
  −1.0 ± 0.1; α at 2M is 2α at M within 1/16 relative; G_eff(N) · N² is
  constant over the five N within 1/16 relative of its value at N = 2^12;
  the diagonal α at equal Euclidean b is within 1/8 relative of the axial α
  (a GameBoard effect larger than that is measured and recorded under
  Highlights 3.23, not hidden).
  Reported and not pinned: the ratio of the light ray's α to the slow ray's
  α at equal b and M against the value 2 of general relativity. Fail: momentum
  inexact or a control that bends (the engine); an exponent or a linearity
  outside its band (the delay table as declared against nature); G_eff · N
  constant instead of G_eff · N², or neither (the identification of m₀ or of
  the unit of action in the derivation, not the engine); a diagonal α
  outside its band (the GameBoard, Highlights 3.5, recorded under 3.23), each
  stated as which.
- **Status.** measured on 2026-09-18 on the engine of `main` at `9cc830f`
  (no engine change on the branch; source
  `25ecd24e87cea58753089a9b38c0d21620ec0eae8401a17d2b55b6352883f038`, the
  fingerprints of the forty-six worlds in `record.json`), as
  `examples/nature/a6_bending/` (`make_worlds.py`, `predict.py`,
  `analyze.py`, the dictionary and the computation in the
  README;
  `tests/test_a6_bending.py`). The mechanism the delay table drives today,
  read from the code before the series: `Ray.lag` of `ray-binding-v1`, spent
  as one Link toward the lagging side when a transverse component reaches
  the light's phase modulus N = 2^`phase_bits` (`lag_bits` open) and as one
  interval of wait on the ray's own axis, not the momentum register of
  feature 8b; and two facts of the engine that the spreading field exposes:
  a meeting with outputs takes one field ray per interval (`participant_groups`
  selects one group and the light's slot is used; the rays at a Node are
  ordered by heading, so the ray met is the ±X one whenever field arrives
  from ahead or behind, every interval on a filled GameBoard), and its output is
  a fresh ray whose lag is that meeting's delay alone (`_output`), so nothing
  accumulates. The pre-registered form therefore predicts no bending at any
  b, N or M, and the series was run in both forms: `delay_*`, the catalog's
  `mass_field_delay` with the table `[1, 1, 1, 1, 1, 1]` per 1 declared
  before the run, and `turn_*`, the momentum register the status names
  (`ray-momentum-turn-v2`, `momentum_table` `{"mass_field": -1}`). The
  construction and its deviations, each stated before the run: the star an
  external body of the catalog's `neutron` (no charge, its only field the
  mass field, its rest rate declared 1 for the run), amount 2^28, release
  [1, 2^15], 8192 quanta per heading per interval, instead of 2^6 m₀: the
  body's amount is both the source of its field (through the release) and
  its inertia (the accumulator that steps a Link at a whole amount), and 2^6
  gives at most 64 quanta per heading, 3.8 net quanta over the whole pass at
  b = 16 in the mean field, which resolves no exponent to ± 0.1, and an
  inertia below one photon of the amount the resolution needs; so M is
  2^28 m₀ by the body's amount, 2M is 2^29 at the same release, and the
  forms (the exponent, the linearity, the N scan, the diagonal, the ratio)
  are what the run reads, G_eff's value a convention of M and the release as
  the entry allows; the light one ray of 2^18 (the register reads the
  deflection to one part in 2^18 and the DDA completes no transverse Link
  over the pass), without `spread` and without polarization; the lamp plain
  (a marked Node draws on every arriving field ray) and one Node below a
  launcher body at the start of the ray's line, a declared coupling of the
  body sending the ray out on +X after 192 intervals of `delay`, so that the
  ray passes the star in a field 192 ticks old (the mean field's pass at
  b = 16 within 0.5 % of the box's steady state) at ticks 193 to 258 of 260;
  the mass field, the star and the launcher at `phase_bits` 3 (read nowhere;
  the spread's admission allows at most 12 and the coherent sum costs one
  pass over the circle per register) and the light at the case's N, 2^12 in
  the b series and 2^8, 2^10, 2^14, 2^16 at b = 8; the slow ray an electron
  of rest rate 1 (every ray moves one Link per interval; slow is a nonzero
  rate); the momentum field bound to the light by the lamp's `recoil_field`
  and to the mass field by an unseeded lamp; the GameBoard the entry's 65 × 65
  × 9 (the smallest with the boundary 2b beyond the farthest pass in z as
  well, 65 deep, is 275 k Nodes and 6 GB, outside the machine and the
  budget), so the (0, 1, 1) diagonal passes, which leave a slab 9 deep, ran
  on a cube of 49 × 33 × 33 with their own axis passes at b = 4, 6, 8 for the
  comparison (a ray along (1, 1, 0) is not expressible: a heading is a Port
  heading and a register is set only by a push); the other side and the
  diagonal run after the axis series passed its ledger and control checks.
  The mean field of the split table (`predict.py`, the kernel of A5s's
  `mean_field_gauss.py`) on exactly these boxes and schedule predicted,
  before the run, the transverse push on the light 3417.70, 1660.36, 862.41,
  269.84 and 94.32 quanta at b = 4, 6, 8, 12, 16 (α = 0.0130367, 0.0063337,
  0.0032898, 0.0010294, 0.0003598), the exponent −2.59 ± 0.21 on this GameBoard
  (a slab 9 deep drains the field through z; the same pass at the steady
  state on GameBoards 17 and 33 deep −1.95 and −1.59, in free space −1.38 ± 0.03
  over b = 4 to 16 and −1.20 over 8 to 32, the local exponent −1.11 to −1.13
  between 16 and 32: the model's own law approaches −1 from below, the
  unscattered beam 8192 (6/11)^(b−1), 39 % of the push at b = 4 and 1 % at
  16, and the GameBoard's short-range anisotropy steepening it at these b),
  the linearity exact, the N scan flat (a register has no modulus), the
  light's α equal to the slow ray's, and the diagonal 0.49, 0.59 and 0.71 of
  the cube's axis fit at b = 4.24, 5.66, 8.49 (the axis fed by the beam).
  Measured, the turn form (`record.json`; the register at the end of the
  pass, α = atan2(|p_⊥|, p_x)): b = 4, 6, 8, 12, 16 the registers (262144, −3423, 0), (262144, −1661, 0), (262144, −862, 0), (262144, −269, 0), (262144, −93, 0), α = 0.013057, 0.0063361, 0.0032883, 0.0010262, 0.0003548 (the mean field 3417.70, 1660.36, 862.41, 269.84, 94.32; ratios 1.0016, 1.0004, 0.9995, 0.9969, 0.9860), the pushes 295, 281, 274, 248, 214 per pass, the first at tick 198 at x = 5; the other side (262144, +3423, 0) to (262144, +93, 0), the exact mirror; 2M (262144, −1727, 0), α = 0.0065879; the N scan (262144, −862, 0) at every N; the slow ray (262144, −862, 0); the control (262144, 0, 0) with no push; the cube's axis (262144, −3697, 0), (262144, −2019, 0), (262144, −1246, 0) at b = 4, 6, 8 and the diagonal (262144, −1169, −1169), (262144, −900, −900), (262144, −578, −578) at d = 3, 4, 6; every ray escaping on its line at (64, y, 4) at tick 258 (the DDA completes no transverse Link); the star's register (0, 222, 0), (0, 26, 0), (0, 4, 0), (0, 0, 0), (0, 0, 0) at b = 4 to 16 and its sink about 2.087 × 10^6 per pass.
  Measured, the delay form: the register (262144, 0, 0) in every one of the twenty-three worlds, no push, the escape on the line at tick 258, one meeting per Node on the line (66 to 91 per pass) with the lag on x alone, the star's register at most (−2, 2, 0) (the returned field rays' recoil).
  The criterion clause by clause, the turn form: (1) pass, momentum exact,
  every ledger line balanced and `conserved_at_every_completed_tick` at all
  260 ticks of all twenty-three worlds, the bodies' momentum line the star's
  register (222, 26, 4, 0, 0 on y at b = 4 to 16, the recoils' net after the
  spread); (2) pass, the control straight (the register (262144, 0, 0), no
  push, the escape at (64, 40, 4) at tick 258); (3) pass, the ray bends
  toward the star on both sides (p_y < 0 above, > 0 below, p_z = 0 at every
  b); (4) fail, the exponent −2.595 ± 0.210 against −1.0 ± 0.1, the GameBoard and the
  GameBoard (the mean field's −2.59 on this slab, reproduced within 0.4 % (the fit of the prediction on these boxes −2.586 ± 0.207);
  the model's free-space law −1.38 at these b, Highlights 3.5 and 3.23, the
  beam and the slab recorded, not hidden); (5) pass, α at 2M is 2.0035 α at
  M (1727 against 862 quanta); (6) fail, G_eff N² grows as N² (the register
  is N-independent: (262144, −862, 0) at N = 2^8, 2^10, 2^12, 2^14, 2^16, G_eff N² =
  1.61 × 10^−6, 2.57 × 10^−5, 4.11 × 10^−4, 6.58 × 10^−3, 0.105 (G_eff = α b / 4M = 2.45 × 10^−11 at every N, G_eff N = 6.27 × 10^−9 to 1.61 × 10^−6)), G_eff itself constant over the five N; the cause is not the
  engine: a push has no modulus, and the entry's own construction, M fixed
  in m₀ with a fixed table, cannot give 1/N² in either form (the delay form,
  had it accumulated, gives α = Σlag / N ∝ 1/N, G_eff N constant; the test of
  feature 8 got N² by scaling the mass with N); the identification named in
  the fail clause: with m₀ = h/(N δt c²) the unit of action m₀ c² δt is h/N,
  so ħ is N/2π in units of (m₀, Link, interval) and G = ħc/(N m₀)² is
  1/(2πN) there, G_eff N constant, while the 1/N² of the model owner's
  statement holds only if m₀ is ħ/(δt c²), one radian per interval rather
  than one step; (7) fail, the diagonal 0.486, 0.587, 0.711 of the cube's axis fit at
  b = 4.24, 5.66, 8.49 against 1 ± 1/8, the GameBoard (Highlights 3.5, 3.23,
  recorded: the mean field's 0.49, 0.59, 0.71 reproduced), the axis pass fed
  by the unscattered beam at short range; the ratio light/slow 1.0000
  exactly (the same push on the same content, the register the same to the
  quantum), reported against 2: the momentum form gives no factor 2 since
  the push reads the field's momentum and nothing of the ray's rate; the
  engine's push against the mean field's prediction within 1.4 % in every
  case (the ratios 1.0016, 1.0004, 0.9995, 0.9969, 0.9860 on the axis, 1.0001, 1.0004, 0.9989 on the cube's axis, 0.9959, 0.9980, 1.0033 on the diagonal, 1.0013 at 2M, the same 0.9995 at every N and for the slow ray), the mean field the expectation of the
  engine's integers here as in A5s. The delay form: (1) pass and (2) pass as
  above; (3) fail, no bending on either side (the register unchanged, the
  escape on the line at the straight tick in all twenty-three worlds, the
  meetings one per Node with the lag on x alone); (4) to (7) fail with α = 0
  at every b, N and M and on the diagonal, and the ratio light/slow
  undefined (0/0); the cause the engine as stated above, the pre-registered
  form of the coupling not runnable on a spreading field until a meeting
  takes every field ray at the Node and its output keeps the input's lag, a
  change of `ray-binding-v1` this run does not make. Run times 130 to 306 s per world in the dense mode, two worlds at a time beside another job, 8760 s in all, the predictor 851 s;
  viewer documents for `turn_b4`, `turn_b16`, `turn_control`, `delay_b4`,
  `delay_b16`, `delay_control` beside the records, which stay outside the
  tree. What this run does not decide: the value of G (Highlights 5.5), the
  release ratio and the table (inputs, hypothesis 17); what it contradicts
  in Highlights 3.28's "G_eff across the phase width" and hypothesis 14: the
  constancy of G_eff N² was the construction of the test of feature 8 (the
  mass scaled with N) and not a property of either coupling at fixed M.
### A6 repeated under the law of the bit (2026-09-18)

- **Claim.** The four gravitational tests against Einstein under the law of
  the bit with the wait of point 23 (features 15 to 18, 16e, 16f;
  DERIVATIONS.md rounds 5 and 6), each registered as what came out and not
  as a law: (1) the clock of a thing at rest at r = 3, 5, 8 and 4, 6, 10,
  the deficit 1 − rate fitted to A/r and B/r² (GR: 1 − GM/r, the
  coefficient 1 at the GR w; round 6 under `amplitude`: 1 − (w/3) 0.537
  √(GM)/r for the star as one owner; round 5 under `amount`: 1 − (√3 w/2)
  GM/r²); (2) the redshift between two radii, z = rate(r_far)/rate(r_near)
  − 1 against GM(1/r_near − 1/r_far); (3) the bending of a light thing at
  b = 3, 4, 6, 8, its deflection from the momentum line and its exit
  heading, against 4GM/b (GR), 2GM/b (Newton) and GM/b (the derivation's
  image); (4) the Shapiro delay, the arrival tick at a mark behind the mass
  against the same path without the mass, against 2GM ln(4x_Ax_B/b²) (GR),
  the derivation's (w/3) 0.537 √(GM) ln(4x_Ax_B/b²) under `amplitude` and
  2.72 w GM/b under `amount`; (5) the options of feature 16e, `shadow_wait`
  `thing` and `field`, on the body-diagonal geometry of DERIVATIONS.md
  section 37 (ix) (the mass at impact parameter 8 from the line, S = 40):
  the receiver's momentum first-move tick per option. Under `wait_reads`
  `amount` and `amplitude`, at w = 1 first and then at the GR w of round 6,
  w = 1.861 √(GM) in the derivation's unit for the star as one owner,
  declared to the engine as 3 × 1.861 √(GM) (the engine counts 3|u|).
- **Features.** 15 (bit-law-v1), 16b (clock-readings-v1), 16c
  (node-mixing-v1), 16d (return-field-v1), 17 (node-is-ports-v1), 18
  (lanes-v1), 16e (shadow-wait-v1), 16f (wait-reads-v1, with the amplitude
  remainder of PR #312), the dense mode and the standing set
  (standing-field-v1); N = 64, K = 1.
- **Run.** `examples/nature/a6_law/` (`make_worlds.py` writes the thirty-seven
  worlds, `analyze.py` reads the records, `probe_field.py` reads the
  prefilled field through the API, `make_page.py` writes the page
  `a6_law.html`; the README row in
  examples/nature).
  A closed GameBoard (`boundary` `periodic`, the model owner's decision of
  2026-09-18) of 33 × 33 × 33 Nodes with the mass at its centre (16, 16,
  16), so that the field wraps around 16 Links from the mass on every axis,
  beyond the farthest clock (r = 10, its outer mirror at 11), the farthest
  bending line (b = 8) and the reach of the field's whole quanta (r = 8, the
  probe below); the prefill of F intervals reaches the Manhattan radius F
  before tick 0, so the wrap-around meets itself at the boundary planes at
  tick 16 − F = 2 of the run for the fill of 14 (a cube of 41 was tried
  first, the wrap-around at 20: its runs take 5 GB each and 10 s per tick,
  two at a time on the machine of the day, 16 GB and four cores, and the
  series did not fit). The
  field settled before it is read: `standing_field` declared, the dense
  region looking for a repeat of its state within the run and replaying the
  cycle from then on, the record carrying the iterations to the cycle and
  the residual. The mass an external body of the family `star` (amount
  2^20) with `release` [1, 2^20/X], X quanta per heading per interval of the
  prefill `initial_field` `{"fill": 14}` (the longest fill the prefill
  admits on this GameBoard: 20 is refused, "the prefill cannot hold a third
  phase on one Port of a source"), absorbing things, returning shadows and
  radiating nothing during the run; the flux S = 6X, the derivation's
  GM = S/(2π): `m256` (X = 256, S = 1536, GM = 244.5, w_GR = 87.29 as
  [8729, 100]), `m64` (X = 64, S = 384, GM = 61.1) and `m16` (X = 16,
  S = 96, GM = 15.3). The light a thing of the `light` family of content 1
  (K 1, clock declared), one per lamp, pushed by the momentum table
  `{"star": −1}` read by content (one shadow quantum read is one whole step
  toward the source of that shadow at the next departure when the push is
  transverse to the heading, and w intervals of wait). (1), (2): four
  cavities per world, one on each half-axis +Y, −Y, +Z, −Z,
  each a light thing between two mirror bodies (`mirror`, the coupling
  `reflect`) at r − 1 and r + 1 along the half-axis, launched outward from
  the centre at tick 0 (a mirror body's token heads +X and lanes-v1 refuses
  a light thing leaving a mirror on +X, so no cavity lies on the X axis), so that it alternates between the centre and a
  mirror and reads the field at the centre on every other interval; a
  closed cavity of six walls shields the clock completely (a body returns
  every shadow, the WIP smoke run of the morning), so the cavity is open on
  its four sides and a transverse push turns the thing out of it, its rate
  read until then; every cavity one Link aside of the axis on X, since a
  mirror on the axis returns the star's shadows straight to the source and
  the prefill is refused (the Euclidean r is √(r² + 1)); batch `a` r = 3,
  5, 8 and 5 again on −Z, batch `b` r = 4, 6, 10 and 6 again; 300 ticks;
  `m256` under both readings at w = 1 and at the GR w, `m64` under both at
  w = 1, one control per batch without the star. (3), (4): twelve lines parallel to X per world, six per b
  (y = 16 ± b, z = 16 and 16 ± 1), b = 3 and 6 in one world and 4 and 8 in
  the other (sixteen thing types at most), one light thing per line
  launched at x = 0 on +X at tick 0, a mark (setting [1, 1]) at x = 40 on
  each line recording the arrival tick, 32 for a straight pass, x_A = x_B =
  16; 100 ticks; `m256` under both readings at w = 1 and the GR w, `m64` and
  `m16` under `amount` at w = 1, the two controls without the star. (5): a source body A of the family `source` (X = 1024, fill 14) at
  (14, 2, 8) and a receiver B, a light thing in a Y cavity at (30, 18, 24)
  whose coupling names `source` only, on the body diagonal through both,
  the mass M at the centre at impact parameter √72 = 8.5 from the line,
  M with X = 7 (S = 42, the S = 40 of section 37) and once more `m256`;
  A's front at Manhattan radius 14 at tick 0, B at Manhattan distance 48
  (Euclidean 27.7) from A; `shadow_wait` absent, `thing` and `field` at w = 1, and the
  control without M; 150 ticks. Recorded per run: the runner's record
  (`run.json`: the momentum line per thing per tick, the ledger, the
  standing set's record, the fingerprint), the events (every arrival of a
  light thing), the world; the records stay outside the tree, the
  analyzer's `record.json` beside the worlds. No world of the series is
  open: "only closed worlds are tested" (the model owner, 2026-09-18,
  Highlights 5.4 "The GameBoard of a run is closed", PR #314); the two open
  controls first written were withdrawn before they ran.
- **The field the runs read** (the probe, before the series, on the 41³
  GameBoard): the whole quanta of the prefilled field are a transient that parks as
  ninths within about 100 intervals (X = 16: 855 quanta arriving per
  interval at tick 1, 182 at tick 40, 1159 of 1440 parked; X = 256: 18 631
  at tick 1, 10 936 at tick 40, 10 566 of 21 504 parked), reaching r = 4 at
  X = 16 (n = 2.4, 2.2, 1.0, 0.1 quanta per Node per interval at r = 1 to 4
  on the axis over ticks 20 to 40, zero beyond) and r = 8 at X = 256 (6.5,
  17.4, 10.5, 14.6, 9.2, 2.5, 0.95, 0.25 at r = 1 to 8, zero beyond; r² n
  = 232 at r = 4 and 16 at r = 8, no power law), the standing set not
  reached within 40 intervals (the residual 1265 cells and 2073 quanta at
  X = 16, 30 426 and 54 987 at X = 256); 10.75 s per tick on 41³, the build
  of the fill 136 s at a peak of 4.6 GB. So `m256` is the mass whose field
  the clocks at r = 3 to 8 read at all, and the clocks at r = 10 and the
  lines at b = 8 read the tail of the transient or nothing.
- **Result (1), the clock, `m256` at w = 1** (eight cavities, two worlds
  per reading, 300 ticks; the rate is the intervals moved over the intervals
  the thing stayed between its mirrors, the deficit 1 − rate; the standing
  set was not reached in 300 intervals in any of the four runs, the field of
  the closed GameBoard circulating at the end with a residual of 15 947 to
  17 224 array cells and 25 741 to 27 910 quanta between consecutive states,
  20 837 quanta of shadow on the GameBoard throughout; every ledger line
  balanced). Under `amount`: r = 3 (Euclidean 3.16) rate 0.0067, 298 waits,
  1339 quanta read in 271 push ticks, never left; r = 4 (4.12) 0.0067, 298
  waits, 629 quanta; r = 5 (5.10, −Y) 0.0133, 296 waits, 391 quanta; r = 5
  (5.10, −Z) 0.0133, 296 waits, 356 quanta; r = 6 (6.08, −Y) 0.923, one
  wait, 3 quanta, turned out of the cavity at tick 14; r = 6 (6.08, −Z)
  0.042, 274 waits, 216 quanta, out at tick 287; r = 8 (8.06) 0.982, one
  wait, 2 quanta, out at tick 56; r = 10 (10.05) 0.996, one wait, 2 quanta,
  out at tick 238. Under `amplitude`: the same rates at every cavity but
  the −Z clock at r = 6 (0.048, 236 waits, 198 quanta, out at tick 249),
  the frozen clocks reading 1334, 623, 386, 352 quanta. The fits of the
  deficit through the origin over the eight cavities: `amount` A/r with
  A = 3.538 (rss 0.900), B/r² with B = 14.38 (rss 1.077); `amplitude`
  A = 3.535 (rss 0.895), B = 14.37 (rss 1.070); per world, batch a A = 3.66
  and B = 13.3, batch b A = 3.35 and B = 17.2, under both readings alike.
  Against GM = 244.5: A/GM = 0.0145 (GR's coefficient is 1 at the GR w;
  round 6's `amplitude` coefficient at w = 1, halved for a cavity that
  reads every other interval, is (w/3) 0.537 √(GM)/2 = 1.40, round 5's
  count (√3 w/2) GM/2 = 106). What came out is a step, not a slope: inside
  r = 5 the clock is frozen (it reads one to four quanta in every interval
  it stays, w n > 1, the horizon of section 43 (ix): r_h = 0.93 √(wGM) =
  14.5 under the count, w · 0.537 √(GM) = 8.4 under the amplitude), and
  from r = 6 outward it reads two or three whole quanta of the transient's
  tail in its first 12 to 236 intervals and the first transverse one turns
  it out of the open cavity; the two readings differ nowhere a clock is
  frozen (both exceed one unit per interval) and nowhere it is sparse (a
  single quantum is one unit of amplitude), and by 14 % of the waits at the
  one cavity that read tens of quanta over hundreds of intervals (274
  against 236).
- **Result (2), the redshift, `m256` at w = 1.** Within one world, z =
  rate(r_far)/rate(r_near) − 1: batch a, 5 → 8 (5.10 → 8.06): 72.8 (a frozen
  clock against a running one); batch b, 6 → 10 (6.08 → 10.05): 0.079
  with the −Y clock at 6 and 22.7 with the −Z one; 4 → 6: 137 and 5.3.
  Against GR's GM(1/r_near − 1/r_far) = 15.9 for 6 → 10 at the GR w,
  round 6's (w/3) 0.537 √(GM)(1/r₁ − 1/r₂)/2 = 0.091 at w = 1 and round 5's
  (√3 w/2) GM (1/r₁² − 1/r₂²)/2 = 1.80: the one pair of running clocks,
  6 → 10, gives 0.079 against the amplitude's 0.091, two whole quanta
  against three, a coincidence of small integers and not a law; every
  pair with a frozen clock gives the horizon, not a redshift.
- **Result (3) and (4), the bending and the Shapiro delay, `m256` at w = 1**
  (twelve lines per world, 100 ticks, a straight pass arriving at tick 32;
  no ledger line unbalanced; the standing set not reached, the residual
  25 760 to 27 507 cells at the end). b = 3 (six lines, Euclidean 3 and
  3.16): every line stops at x = 10 or 11, r = 5.8 to 6.8 from the star,
  at tick 10 to 12, and never moves again, reading 63 to 81 quanta (68 to
  85 under `amplitude`) in the 88 to 90 intervals it waits, the pushes on
  every axis and in both senses (toward the star 16 to 37 quanta, away 6 to
  31, along the line 25 to 36 forward, 10 to 16 back), the net transverse
  push toward the star 2.2 quanta per line (3.2 under `amplitude`); none
  arrives. b = 4: every line stops at x = 10 or 11, r = 6.4 to 7.2, at tick
  10 to 13 (one at tick 70 at r = 4.1 under `amplitude`), 73 quanta per
  line, net −23 (away; −21 under `amplitude`); none arrives. b = 6: every
  line stops at x = 11 to 13, r = 6.8 to 7.9, at tick 11 to 14, 62 quanta
  per line (74 under `amplitude`), net −1.7 (+25 under `amplitude`); none
  arrives. b = 8: five of six lines read nothing and arrive at tick 32, the
  delay 0 under both readings; the sixth (y = 8, z = 16) reads one quantum
  at x = 20, four Links past the star's plane, turns toward the star at
  tick 20, reads 64 to 68 more and stops at r = 5.4 (6.4 under `amplitude`)
  at tick 43 (31). So the image: at b ≤ 6 the light thing of content 1
  does not bend and does not pass, it enters the region r ≤ 7 where the
  whole quanta of the field arrive faster than one per interval and is
  frozen there (the horizon of the clocks above, r_h = 8.4 to 14.5 by the
  derivation, 6 to 8 measured); at b = 8 it passes straight five times in
  six and is captured once. Against GR's 4GM/b = 326, 244, 163, 122 rad at
  b = 3, 4, 6, 8 (GM = 244.5, in the derivation's unit: every b of this
  GameBoard is inside the capture radius b_c = GM), Newton's 2GM/b and the
  derivation's GM/b = 82, 61, 41, 31: a mass this heavy captures, and the
  register reads no angle. The Shapiro delay: 0 ticks on the ten lines
  that arrived (b = 8), against GR's 2GM ln(4x_Ax_B/b²) = 1354 ticks,
  round 6's (w/3) 0.537 √(GM) ln(1024/64) = 7.8 under `amplitude` and
  round 5's 2.72 w GM/b = 83 under `amount`; a line that reads no whole
  quantum is not late, and one that reads a whole quantum at this mass is
  frozen. The weaker masses `m64` and `m16` below read the passes.
- **Result (1) and (2) at `m64`, w = 1** (S = 384, GM = 61.1; eight
  cavities per reading, 300 ticks; the standing set not reached but nearly,
  the residual 41 to 152 cells and 0 to 272 quanta at the end; every ledger
  line balanced). Under `amount`: r = 3 (3.16) frozen from tick 2, 238
  waits and 176 quanta in 240 intervals, then turned out at tick 241; r = 4
  (4.12) 0.889, one wait, 3 quanta, out at tick 10; r = 5 (5.10) 0.957 and
  0.970, one wait, 2 quanta, out at ticks 24 and 34; r = 6 (6.08) 0.991
  and 0.992, one wait, 2 quanta, out at 108 and 130; r = 8 and 10 read
  nothing, rate 1.000, stayed. Under `amplitude`: the same at every cavity
  but r = 3 (0.012: 165 waits and 161 quanta in 167 intervals, out at tick
  168, a third fewer waits for the same field) and one of the r = 6 clocks
  (nothing read, 1.000). Pooled fits: `amount` A = 1.136 (rss 0.592), B =
  5.98 (rss 0.346); `amplitude` A = 1.127 (rss 0.591), B = 5.95 (rss
  0.346); A/GM = 0.019 against GR's 1; round 6's halved coefficient at
  w = 1 is 0.70 and round 5's 26.5. Against `m256`: A = 3.54 → 1.14 and B =
  14.4 → 5.98 for S = 1536 → 384, a factor 3.1 and 2.4 for a factor 4 in
  S (round 6 gives √S, 2; round 5 gives S, 4), but the fit is of a step,
  the frozen radius moving from 5 to 3 with the reach of the whole quanta,
  and the redshift 5 → 8 within batch a is 0.045 (2 quanta against none),
  6 → 10 within batch b 0.009 and 0.008 (`amount`), 0 and 0.008
  (`amplitude`), against GR's 15.9 · (61.1/244.5) = 4.0 at the GR w, round
  6's 0.045 and round 5's 0.45 at w = 1.
- **The controls.** Without the star every clock runs at 1.000 in both
  batches (no wait, no push, the thing bouncing between its mirrors for 300
  intervals), the standing set of the empty GameBoard reached after 66
  intervals with the period 64 (the clocks' bounce on the phase circle of
  64) and replayed for 234; every bending line arrives at tick 32 with no
  push, the standing set reached after 34 intervals with the period 1.
- **Result (5), the separating run, M with S = 42** (150 ticks; the source
  A at X = 1024, 86 604 quanta of shadow on the GameBoard; every ledger line
  balanced; the standing set not reached, the residual 121 620 to 121 646
  cells). The receiver's momentum never moves, under `shadow_wait` absent,
  `thing` and `field` alike and without M: no whole quantum of A's field
  reaches B, 27.7 Links from A (Manhattan 48), within 150 intervals, while
  A's own Node receives about 400 quanta per Port per interval at tick 1
  (the mixing's returns) and 10 to 20 from tick 2 on; the mass's Node, 17.3
  Links from A (Manhattan 30), receives no whole quantum of A's field
  either, so the front never crosses M's field in whole quanta. The
  observable of section 37 (ix), the tick B's register first moves, is not
  reached on this GameBoard at this flux: the front of a field in whole quanta
  ends where its quanta park (about r = 8 at X = 256, and short of 17 at
  X = 1024), and a receiver near enough to A to read its quanta would not
  have M's field between them.
- **Result (1) at the GR w, `m256`** (w = 87.29 as [8729, 100], the
  engine's 3 × 1.861 √(GM); eight cavities per reading, 300 ticks; every
  ledger line balanced; the standing set not reached, the residual 16 629
  to 17 519 cells). Under `amount`: r = 3, 4, 5 and one of the 6 frozen as
  at w = 1 (rates 0.0067 to 0.040, 288 to 298 waits, 237 to 1365 quanta);
  r = 8: 0.180, 246 waits for 78 quanta (the two quanta read by tick 54
  cost 87 intervals each, and the thing, waiting, reads on); r = 10: 0.867,
  40 waits for 3 quanta; the other clock at 6: 0.040. Under `amplitude`:
  the same numbers at every cavity. Pooled fits: A = 4.356 (rss 0.474),
  B = 16.44 (rss 1.529) under both readings, A/GM = 0.018 against GR's 1
  at this w; the step of w = 1 with its outer edge moved from r = 6 to
  r = 10, since a single whole quantum now costs 87 intervals, more than
  the run's tail.
- **Result (3) and (4) at `m64`, w = 1, b = 3 and 6** (`amount`; the
  standing set not reached, the residual 5547 cells; the ledger balanced).
  b = 3: every line stops at x = 11 to 14, r = 3.7 to 5.9 from the star,
  at ticks 11 to 18 (one at 62), frozen for the rest of the run, reading
  59 to 79 quanta, the net transverse push toward the star 24.7 quanta per
  line; none arrives. b = 6: every line reads nothing and arrives at tick
  32, delay 0. So at S = 384 the frozen region ends between r = 4 and 6
  (between 5 and 7 at S = 1536) and outside it a line of content 1 reads
  no whole quantum at all: the image is a capture radius, GM/b reads no
  angle at either mass, and the Shapiro delay is 0 on every line that
  arrives, against GR's 2GM ln(4x_Ax_B/b²) = 322 ticks at b = 6 (GM = 61.1),
  round 6's (w/3) 0.537 √(GM) ln(1024/36) = 4.7 under `amplitude` and round
  5's 2.72 w GM/b = 28 under `amount` at w = 1.
- **Whether the field settles.** In every world with the star the dense
  region found no fixed point and no cycle within the run (the window 1024
  deliveries): the residual between consecutive states at the last tick
  was 15 947 to 17 519 array cells and 25 741 to 28 775 quanta for `m256`
  (300 ticks, 20 837 to 21 341 quanta of shadow on the GameBoard throughout),
  25 760 to 27 507 cells for the bending worlds (100 ticks), 121 620 to
  121 646 cells for the separating worlds (86 016 to 86 604 quanta), and 1
  to 152 cells and 0 to 272 quanta for `m64` (5235 to 5376 quanta): the
  weak field parks almost entirely within 300 intervals, the strong one
  keeps circulating. The content per shell over time is the probe's (the
  41³ GameBoard, X = 256, the +Y axis, the mean over ticks 1 to 10, 11 to 20,
  21 to 30, 31 to 40): r = 1: 41.4, 5.3, 6.8, 6.1; r = 2: 24.4, 21.9, 16.6,
  18.1; r = 3: 16.9, 15.8, 12.7, 8.2; r = 4: 10.1, 15.4, 14.9, 14.2; r = 5:
  7.0, 8.6, 9.3, 9.0; r = 6: 0.9, 2.7, 2.5, 2.4; r = 7: 0.1, 0.6, 0.7, 1.2;
  r = 8: 0, 0, 0.2, 0.3; nothing beyond; the arrivals over the GameBoard
  17 619, 14 860, 12 562, 11 335 per interval while the parked ninths grow
  3791, 6635, 8934, 10 163. The sign of the radial push per shell over
  time was not read (the region publishes no per-Node events, and the
  probe read counts, not headings); the frozen things at r < 7 were pushed
  in every direction and in both senses (the bending lines above: toward
  the star 16 to 98 quanta, away 5 to 54, per line), which is the same
  fact at the things. Without the star the empty GameBoard's standing set is
  found after 34 (bending) and 66 (clocks) intervals. So the closed GameBoard
  with one body holds no static field under point 7 as it stood, which
  the E11 lane found on its GameBoard the same afternoon, and every reading
  above is a reading on a field that does not settle.
- **Reading.** Registered as what came out, on the engine of `main` at
  `3b4a31c` (features 15 to 18, 16e, 16f with PR #312), and not as a law:
  (1) the clock is a step at the edge of the whole-quanta field (frozen
  inside, untouched outside, two or three quanta in between), the same
  under `amount` and `amplitude` at w = 1 and at the GR w, its fits A/r
  and B/r² fits of a step (A/GM 0.015 to 0.019 against GR's 1); (2) the
  redshift between two running clocks is two whole quanta against three;
  (3) the image is a capture, GM/b reads no angle; (4) the Shapiro delay is
  0 on every line that arrives; (5) the front of a field in whole quanta
  never reaches the receiver. Two readings of the wait differ by a third of
  the waits at the one clock that read tens of quanta over hundreds of
  intervals (m64, r = 3: 238 against 165). The field these numbers were
  read on does not settle on the closed GameBoard (above); the model owner
  reversed point 7 the same evening (a thing emits; nothing is given with
  the GameBoard; Highlights, PR #319), and the series is repeated after
  DERIVATIONS.md round 7 and feature 19 (emission and the sink).
- **Not read.** The bending and the Shapiro delay of `m64` at b = 4 and 8
  and of `m16` at every b, the bending at the GR w, and the separating run
  with M = `m256`: their worlds are written and were stopped before or
  during their runs at the orchestrator's instruction of 13:40Z (the lane
  stopped so that the law is closed first).
- **Fingerprint.** Every run of the series: `source_sha256`
  `3f490e4265d59e0d4a55cccaf32e999cc8ebb692a972f701f08c8ba5394e4349`, the
  engine of `main` at `3b4a31c` merged into the branch at `16dbd39`; each
  world's `initialization_sha256` in `record.json` (the run's world files
  declared `ray_slots`, which `main` retired the same afternoon with
  lanes-v1's cleanup; the files in the tree are the same worlds without
  that key, so that they parse on the current engine, and the run's own
  files are preserved with the records); Python 3.14.0rc2,
  numpy 2.5.3, four cores, 16 GB, four runs at a time, 6.3 s per tick on
  33³ (2160 to 2260 s per clock world, 640 to 700 s per bending world, 830
  to 1700 s per separating world). The GIF of the page is `tools/ray_viewer`
  on `bend_m256_w1_amount_b3_6` (Three.js r128 from the npm package
  three@0.128.0, the pinned digest).
- **Status.** measured on 2026-09-18, on a field that does not settle; to
  be repeated after round 7 and feature 19.
### A7. Newtonian attraction between two bound groups

- **Confronts.** Newton's law, force G M₁ M₂/r², G = 6.674 30 × 10^-11
  m³ kg^-1 s^-2 (CODATA 2022), equal and opposite, with no deviation from the
  inverse square found by torsion balances down to 52 µm (Lee and others,
  2020).
- **Model prediction today.** Highlights 3.28 as in A6: the field ray of a
  heavy Node that meets a ray whose coupling responds returns reversed with
  the opposite momentum, and the heavy Node is drawn toward the ray; for two
  bodies, bound groups or external bodies alike (Highlights 3.19: an
  external body's motion is caused by fields only, model owner, 2026-09-17),
  each is met by the other's field, so each is drawn toward the other,
  retarded by the field's transit, with the field's content falling by the
  outward dilution of the GameBoard, 1/r² by exact shell counts.
- **Features.** 1, 5, 6, 7, 7b, 8, 9, 10.
- **Run.** A GameBoard of 97 × 33 × 33 Nodes, open boundary, N = 2^10. Two
  bodies of amount M₁ and M₂, in two series: two ordinary bound groups of
  retained content M₁ and M₂ (feature 8), and two external bodies (feature
  7b, `external-body-v1`) of declared family and amount M₁ and M₂, each at
  rest (`initial_momentum` zero) and each with its coupling table naming
  the other's field family, so that the arriving field rays change its
  momentum by the table and its velocity, momentum over amount, is an exact
  accumulator that steps one Link when a full amount has accumulated on an
  axis; at separations r = 6, 8, 12, 16, 24 and 32 along x, one run per r,
  and the same separations along the (1,1,0) diagonal at equal Euclidean
  length rounded to the GameBoard; M₁ doubled once at r = 12; 4r intervals
  after the first meeting. Recorded per tick: each body's momentum (the sum
  over its bound rays for a group; the audit's bodies' momentum line and
  the accumulator for an external body), every field ray in flight, the
  tick of the first return, the audits. The rate of momentum gain dp/dt of
  body 1 is read over the 2r intervals after its first return.
- **Criterion.** Pass, all of, in each series: momentum exact at every tick
  over both bodies and all field rays; each body's momentum points toward
  the other; the
  log-log exponent of dp/dt over the six axial r is −2.0 ± 0.1; dp/dt at
  2M₁ is twice its value at M₁ within 1/16 relative; the diagonal value at
  equal Euclidean r is within 1/8 relative of the axial value (a GameBoard
  effect larger than that is measured and recorded under Highlights 3.23,
  not hidden). Fail: any one, stated as engine (inexact momentum), table
  (exponent) or GameBoard (direction).
- **Status.** planned.

### A8. Hydrogen-like binding and the Balmer ratio

- **Confronts.** The hydrogen levels E_n = −13.606 eV / n² (Balmer 1885,
  Rydberg, Bohr 1913): the ratio of the two lowest transition frequencies,
  Lyman-α (121.57 nm) to Balmer-α (656.3 nm), is (1 − 1/4)/(1/4 − 1/9) =
  27/5 = 5.4; the ionization energy of the ground state, 13.6 eV, equals its
  binding.
- **Model prediction today.** Highlights 3.4: matter is a bound group, an
  electron ray around a bound proton whose trajectory is changed at every
  step by the field rays the pair releases; the group's phase advance is its
  clock; it is unbound by an arriving ray through the declared coupling.
  Highlights 3.3: light carries the phase of the clock that emitted it, so
  the frequency of light is the rate of its emitter's clock. No level
  structure is stated anywhere: whether bound orbits exist only at discrete
  retained energies, and which clock an emitted light ray carries, the
  group's rest rate or the orbit's, is what the run decides.
- **Features.** 1, 2, 5, 6, 7, 7b, 8, 9, 10.
- **Run.** A GameBoard of 33 × 33 × 33 Nodes, open boundary, N = 2^12. The fixed
  proton at the center: an external body (feature 7b, `external-body-v1`,
  Highlights 3.19) of the proton family, charge +1, amount M_p, at rest
  (`initial_momentum` zero), at its default coupling, absorption into its
  explicitly accounted sink (the mirror, beam-splitter, phase-plate and
  polarizer couplings are not used here); its motion is caused by fields
  only (model owner, 2026-09-17): the electron's field rays that reach it
  change its momentum by its coupling table, the audit's bodies' momentum
  line carries it, and its velocity, momentum over amount M_p, is an exact
  accumulator that completes no Link during the run, so against the
  electron it stands still and its whole content stays at one Node; marked
  as a source with setting 1; when the proton's
  recoil is wanted, the same proton is declared instead as an ordinary bound
  group (charge +1, retained content M_p, feature 8), and then it spreads and
  is pushed like all matter; an electron ray (charge −1, rate r_e) launched
  at distances d = 2 to 8 Links with transverse momentum p = 1 to 8 units,
  one run per
  (d, p), 2^14 intervals each, the field coupling of A5 and the binding
  coupling of feature 8 as declared tables. A second series: onto each bound
  state found, a light ray of content E from a marked source, E swept from 1
  to 64 units. Recorded: the electron ray's trajectory per tick; the group's
  retained energy per tick; every light ray leaving the group, its emission
  tick and the phase it carries (the rate read from consecutive emissions);
  the content E at which the electron ray leaves; the audits.
- **Criterion.** Pass, all of: at least two distinct bound electron
  trajectories with distinct retained energies E₁ < E₂ (< E₃) each stable
  for 2^12 intervals; with three states, (E₁ − E₂)/(E₂ − E₃) = 27/5 within
  1/8 relative; the light emitted at the two lowest transitions carries
  rates in the ratio 27/5 within 1/8 relative; the smallest content E_ion
  that unbinds the lowest state equals its binding energy E₁ within one
  unit. Reported and not pinned: the content of each emitted light ray
  against the rate it carries, for E = hf. Fail: a continuum of bound
  energies with no discrete states (the model as stated has no levels); every
  emitted ray carrying the group's rest rate (the frequency of light as the
  emitter's clock fails against the Balmer series as stated in 3.3); a ratio
  outside 27/5 ± 1/8 (the declared field table); E_ion unequal to E₁ (the
  binding accounting); each stated as which.
- **Status.** planned.

### A9. Neutron decay from the bound-group draw

- **Confronts.** The free neutron's mean lifetime 878.4 ± 0.5 s (Particle
  Data Group, 2024), half-life 878.4 ln 2 = 608.8 s, exponential survival;
  the decay n → p + e⁻ + ν̄ with electron endpoint m_n − m_p − m_e = 782 keV;
  the proton stable (lifetime above 10^34 years) and the neutron stable when
  bound in the deuteron.
- **Model prediction today.** Highlights 3.26: a free particle never decays;
  a neutron is a bound group whose ticks are events; a bound group that can
  decay is a source, and a source is a Detector, so at each tick it draws
  with its declared ratio as the setting, 1 = the conversion fires (an
  N-to-M conversion with charge, energy and momentum exact), 0 = the group
  ticks on unchanged; half-life follows, T½ = −ln 2 / ln(1 − n/d) intervals,
  and nothing else in the world draws. In the loop form as implemented
  (`decay-draw-v1`, 2026-09-17, [a decaying group
  draws](SPATIAL_FIELDS.md#a-decaying-group-draws-decay-draw-v1)) the
  group's ticks are its corner meetings and the draw is the `draw` setting
  of the conversion's rule, taken once at every meeting of the group's rays
  under it, so the survival law is (1 − n/d)^k over k meetings and the
  half-life above is in meetings, divided by the ring's meetings per
  interval to read it in intervals (four on the eight-ray unit square, two
  on the four-ray one).
- **Features.** 1, 2, 5, 6, 8, 9, 10.
- **Run.** A GameBoard of 65 × 65 × 65 Nodes, periodic, N = 2^10. 4096 neutron
  groups (the binding coupling of feature 8, catalog masses in keV: neutron
  939 565, proton 938 272, electron 511), each at its own Node 4 Links from
  any other so that products never meet, each marked with setting n/d =
  1/1024 and the conversion n → p + e⁻ + ν̄ declared as the event of a 1 with
  its invariants; 2^14 intervals. A control of 64 proton groups with setting
  0. Recorded: per group the tick of its firing or its survival; the
  products' families, charges, energies and momenta at every conversion;
  the number of draws per tick (from the ticket consumption, feature 10);
  the audits. Recorded as a finding, not pinned: the ratio n/d that the
  physical half-life needs at one Planck time per interval, about 2^-154,
  and whether the bounded setting of feature 2 can hold it.
- **Criterion.** Pass, all of: exactly one draw per neutron group per tick
  and exactly one conversion per group ever; the Kolmogorov-Smirnov distance
  between the empirical survival curve and (1 − 1/1024)^t is below 0.0255
  (the 1 percent critical value at 4096); the half-life fitted by maximum
  likelihood is 709.4 intervals within 3 standard errors (about 33
  intervals); at every conversion charge sums to zero, energy and momentum
  are exact component by component, and the electron's energy never exceeds
  782 keV; no proton group ever fires. Fail: any one; a survival curve that
  is not memoryless is a fail of the draw as the decay against nature.
- **Restated under the law of the bit (model owner, 2026-09-18; Highlights
  5.4, points 14 and 20).** The decay draw is retired: a decay is a declared
  condition on the group's own state (its content, its phase pattern, the
  number of its periods), a table like every meeting of things, and its
  outputs are things. A population of identical groups with identical
  histories then decays at one moment, not exponentially; the exponential
  survival of nature, if the model gives it, must come from the variety of
  the groups' states and phases at birth and of what their shadows meet.
  What A9 tests under the law: (i) the conversion fires when and only when
  the declared condition is met, with charge, amount and momentum exact;
  (ii) the survival curve of 4096 groups born with varied phases and
  contents (a declared spread), read against the exponential; (iii) the
  proton and the bound neutron never meet their condition. The half-life
  formula above is void; the run's settings n/d become the table's
  condition. Waits for features 15 to 17 and the owner's table.
- **Status.** planned.

### A10. The mass ladder against the known spectrum

- **Confronts.** The measured mass ratios m_μ/m_e = 206.768 28 (relative
  uncertainty 2 × 10^-8), m_τ/m_e = 3477.23 (7 × 10^-5) and m_p/m_e =
  1836.152 67 (2 × 10^-11), CODATA 2022.
- **Model prediction today.** Hypothesis 12, the ladder: every rest mass is
  an integer number of phase steps per interval on one circle of N steps,
  m₀ = h/(N δt c²), so every ratio is a ratio of integers; the rungs of the
  elementary families are catalog values, not predictions; the test is
  representability at one N within the declared encoding error
  (reference units). The self-field of the unit-square
  ring selects no content
  ([E10](#e10-the-ring-meets-its-own-field-the-loop-under-its-own-light-contents-32-to-128),
  2026-09-17): with the catalog's turn declared beside the corner table, a
  ring ray is met by one rule per cycle, so every content survives under
  the corner first and every content disperses at tick 3 under the turn
  first, and the ladder at this ring stays the corner table's.
- **Features.** 9 (and, for the real N, A11).
- **Run.** A catalog fit, no GameBoard: at N = 2^12 (the engine's circle today)
  and at the N of A11, find the smallest integer k (the electron's rung,
  r_e = k) such that k · 206.768 28, k · 3477.23 and k · 1836.152 67 are
  each within their measured relative uncertainty of an integer, and the
  largest rung k · 3477.23 is below N. Recorded: the smallest k at each N or
  its absence; whether k = 1 fits (the electron as the first rung).
- **Criterion.** Pass: a k exists at the real N. Fail: no k with the largest
  rung below N (the ladder fails at that width). Reported: at N = 2^12 no k
  fits (k = 1 puts the muon at 207, 1.1 × 10^-3 off, and k = 4 puts the tau
  above N), so the ladder is a statement about the real N only, and the
  smallest k found there is the electron's rung; k = 1 does not fit since
  206.768 28 is not an integer, so the electron is not the first rung.
- **Status.** planned; after feature 14, binding as a loop (Highlights 3.4,
  2026-09-17): the rungs it counts are the contents that close a loop under
  the declared tables, which the held-ray binding of feature 8, holding any
  content, cannot show. The counting procedure, ring by ring over the
  corner table, is written in
  loop binding
  (design of 2026-09-17), with its finding that the Port-form corner and
  the Born table give no content ladder and that the ladder needs the
  ring's turn produced by its own field.
  Closed by decision (the model owner, 2026-09-20, issue #369; Highlights
  5.4 and the log's record 106): the masses and the charges are the
  initialisation, the catalog's declared contents and charge per unit, not
  derivable in the Beam Law (the standalone map of the paid exchange
  reproduces the engine and selects no content); the rungs are inputs and
  there is nothing to count. Kept as history; the number A10 also names the
  Heisenberg run registered below under the Beam Law, a different
  experiment.

### A11. The wide-phase run at the real N

- **Confronts.** The identification of the phase circle with nature's scale:
  with N m₀ the Planck mass and m₀ the electron's rung, N = m_P/m_e = 2.39 ×
  10^22 = 2^74.3 (the 74-bit phase; a register of 75 bits holds it, and the
  exact integer is the model owner's declaration before the run); the
  electron's Compton wavelength ħ/(m_e c) = 3.86 × 10^-13 m is then N Planck
  lengths, and the gravitational coupling of two electrons, G m_e²/(ħc) =
  (m_e/m_P)² = 1.75 × 10^-45 = 1/N², is 4.2 × 10^42 times smaller than their
  electric coupling.
- **Model prediction today.** Highlights 3.11 and 3.17: bounded integers,
  overflow rejecting before mutation; hypothesis 12 for m₀; the statement of
  A6 for G. At the real N a clock of rate 1 advances one step per interval,
  so over any GameBoard of feasible size the phase difference between two rays
  of one emitter is below 2^-50 of a turn, the steering table sends all
  shared content to the first Port, and the bending of A6 at G_eff = C/N² is
  below one heading step; the charge coupling reads charge and content, not
  the phase width, so A5 is unchanged.
- **Features.** 1, 5, 6, 7, 8, 9 with `phase_bits` = 75 and a bounded
  evaluation of the steering table at that width (no table of N entries), 10.
- **Run.** The worlds of A1, A5 and A6 repeated at `phase_bits` = 75 with the
  emitter of A1 at rate 1, the electron rays of A5 at rate k of A10, and the
  group of A6 at content 2^40 m₀; 2^12 intervals each; a replay of each with
  the same seed. Recorded: the audits per tick; the phase carried by every
  ray as a 75-bit integer; the content per Port at the screen of A1; Δp(b)
  of A5; the heading of the light ray of A6 before and after; any overflow
  rejection; the host time per tick separately (Highlights 3.10).
- **Criterion.** Pass, all of: no overflow rejection and every audit identity
  exact at every tick at 75 bits; the replay equal bit for bit; at the screen
  of A1 the phase difference of the two arriving rays equals r ΔL exactly
  and all shared content leaves by the first Port; Δp(b) of A5 equals its
  value at N = 2^12 exactly for every b; the light ray of A6 leaves with its
  heading unchanged (a deflection below the heading's resolution of one part
  in 2^30), consistent with nature's ratio 2^-142 of gravitational to
  electric coupling and not a measurement of it. Fail: an overflow or an
  inexact audit (the width,
  not physics); a fringe at the real N or a changed Δp (the phase width
  leaking into a coupling that must not read it); a deflection (G_eff · N²
  not constant to the real N).
- **Status.** planned. Reading of 2026-09-17 (Highlights 3.28): the run
  remains a width check, that `phase_bits` = 75 leaks into no coupling, and
  nothing on the road to the confrontation runs requires the wide phase, the
  N of nature being a register of any width that enters no phase sum (the
  momentum register of feature 8b for the turn, `ray-momentum-turn-v1`,
  2026-09-17; the lag's own modulus for the delay, open) and not the phase
  circle.

### A12. Malus's law and the three-polarizer chain (after feature 11)

- **Confronts.** Malus's law (1809), transmitted intensity I₀ cos²θ through a
  polarizer at angle θ to the light's polarization; crossed polarizers pass
  nothing, and a third polarizer at 45° between them passes 1/8 of the
  unpolarized intensity (1/4 of the polarized).
- **Model prediction today.** Highlights 3.26: polarization is a family
  property, a transverse mode perpendicular to the heading with two states
  for light (the two GameBoard axes perpendicular to an axial heading), read by
  the declared couplings at a meeting; a polarizer is then a coupling table.
  Whether a two-state property carries the intermediate polarizer's angle
  through the chain is what the run decides; Highlights states no more.
- **Features.** 1, 2, 5, 6, 7b, 9, 10, 11.
- **Run.** A GameBoard of 65 × 9 × 9 Nodes, open boundary, N = 2^8. A source
  (marked, setting 1) of light rays polarized along y; a polarizer as an
  external body (feature 7b, `external-body-v1`, Highlights 3.19) with the
  polarizer coupling, a polarization read once feature 11 exists, splitting
  content between the pass Port and its declared sink by the table
  cos²(θ − θ_ray) for θ = 0,
  22.5, 45, 67.5 and 90 degrees, one run each, a marked Node (setting 1)
  behind it; then chains: y, 90°; y, 45°, 90°; y, 22.5°, 45°, 67.5°, 90°.
  Recorded: the content that clicks behind the last polarizer per run; the
  polarization state of every ray leaving each polarizer; the audits.
- **Criterion.** Pass, all of: one polarizer passes the table's cos²θ of the
  content exactly with the remainder owned; the chain y, 90° passes 0; the
  chain y, 45°, 90° passes 1/4 of the content within the table's rounding;
  the chain of four polarizers passes cos⁸(22.5°) = 0.531 within the
  rounding; content
  exact at every tick. Fail: the chain y, 45°, 90° passing 0 or 1/2 (the
  two-state property does not carry the intermediate angle and the catalog
  needs a transverse direction, as 3.26 allows for the circular case), or
  any inexact split.
- **Deviations from the plan above, each stated before the run.** (i) The
  property landed as the transverse direction itself, not as a two-state
  property that would then be found wanting: feature 11
  (`ray-polarization-v1`, polarization)
  gives every light ray an integer step of a circle of 2^`polarization_bits`
  steps per half turn, the phase width by default, whose steps 0 and half
  the circle are the two GameBoard axes of Highlights 3.26 and whose other
  steps are the direction the circular case would turn, without its
  handedness bit; a polarizer sets the passed ray's polarization to its own
  angle, so the question the entry asks, whether the intermediate angle is
  carried through the chain, is answered by construction and the run
  confirms it in the engine's integers rather than deciding it. (ii) N =
  2^8 is the polarization circle (256 steps per half turn, 22.5°, 45°,
  67.5° and 90° the steps 32, 64, 96 and 128 exactly) and the table is
  cos²(d × 180 / 256 degrees) in 256-ths, rounded, written by
  `make_worlds.py`; the phase is 2^8 too and read nowhere. (iii) The
  polarizer's sink is the body's sink counter (the `absorbed_by_bodies`
  line), not a second Port: the rest of the content ends in the body, as a
  sheet polarizer absorbs it; the two-channel form A13 names is not
  declared. (iv) The remainder below one quantum is owned by the body's
  registers exactly as a spread's is owned by the Node's (feature 12b), and
  since every pulse is 256 quanta, a multiple of D, the single-polarizer
  splits are exact and the remainder rule is exercised only in the chains
  from the second polarizer on. (v) The source is a beam: a lamp on a
  marked Node (setting 1) at (2, 4, 4) emitting 256 quanta per interval
  along +X for eight intervals, 2048 in all, polarized along +Y (step 0),
  and light declares no `spread`; a polarizer confrontation needs a beam
  (a spreading field would reach the polarizer on every heading and the
  screen from everywhere), so "the field spreads" (Highlights 3.5) is set
  aside here, the one Malus geometry needs a collimated source, and the
  spread of polarized content is tested in isolation
  (`test_ray_polarization.py`, its axial-mean rule) and not by this run.
  (vi) The polarizers stand ten Links apart at x = 12, 22, 32, 42 and the
  marked Node (setting [1, 1]) at x = 52 in every world, so that every world
  has the same geometry; the passed content clicks there and escapes
  through the open face at x = 64; 72 ticks let every quantum click, sink,
  wait or escape. Made as `examples/nature/a12_malus/`: eight worlds
  written by `make_worlds.py`, the records read by `analyze.py`, its
  integers in `record.json`, the dictionary in the
  README.
- **Status.** measured on 2026-09-17, commit
  `54d159390071534de4409647b928ca9139f298f9` (the feature's commit
  `cd4d971` merged with `main` at `b64de24`), source
  `aec35d9ec38c9c3778a3e2ef3966d996d0ffcadfb547c4626defa526b754d705`;
  initialization fingerprints, one polarizer at 0°, 22.5°, 45°, 67.5°,
  90°:
  `7cfc9c0d64925654af6b649b02d8184bd7d343457a1a0f752d2c1dce433cf902`,
  `16985a3fdb8034c1d99930ccd72ec74ae54358b8c261769d0beb2ce95c762efc`,
  `98e9c1384d08ec0a2a73fb4f2a7366736dd7cb7708bcffd477c03c4fc6b0f406`,
  `7724631239265cf1f10401660fd0eac67d0ab37bb8fa06b778d7a0cd8225c282`,
  `35bdcf336aff8f559a2eb812e0c7bc3896e922340a51f17994b3243c6e76fbcc`;
  the chains y, 90°; y, 45°, 90°; y, 22.5°, 45°, 67.5°, 90°:
  `7ec4d8e3f359eb752e93d46d095d1a218193bc868a26acd755c7290290fc1626`,
  `b1e0a394497642ebf20905e771fd8c1c1baa2dde07f884f2184350f20eadf906`,
  `757144db2eb8d7a6772cb042fc24835bd5aa1a00910b60257c1d320d181d359c`;
  outcome: pass, every clause: (1) one polarizer passes the table's share
  exactly, 2048, 1752, 1024, 296 and 0 of 2048 at 0°, 22.5°, 45°, 67.5°,
  90° (the table's entries 256, 219, 128, 37, 0 in 256-ths; Malus's cos²
  gives 2048, 1748.1, 1024, 299.9, 0, the difference the table's rounding,
  219/256 = 0.8555 for cos² 22.5° = 0.8536), every `polarizer` record
  exact and no register ever nonzero, the remainder rule not exercised in
  the singles (every pulse a multiple of D); (2) the chain y, 90° passes 0;
  (3) the chain y, 45°, 90° passes 512, exactly a quarter (1024 after the
  first polarizer, half of it after the second), neither 0 nor 1/2, so the
  intermediate angle is carried; (4) the chain of four passes 1095 of
  2048, 0.5347, against cos⁸(22.5°) × 2048 = 1087.1 (0.5308): the table's
  own compounded value is (219/256)⁴ = 0.5356, 1096.9, and the exact
  integer rule with the registers gives 1095 clicked with 3 quanta still
  held at the end (one in each of the last three polarizers' registers,
  200 + 56, 126 + 130 and 219 + 37 in 256-ths), which the run reproduces
  to the quantum; the distance from cos⁸, 7.9 quanta, is the table's
  rounding (9.8) less what the floors withhold; the four polarizers passed
  1752, 1498, 1281, 1095 and sank 296, 253, 216, 185, their registers
  releasing 2 + 5, 7 + 0 and 5 + 2 whole quanta to the pass Port and the
  sink over the eight pulses; (5) every ledger line balanced and
  `conserved_at_every_completed_tick` true in all eight worlds, every
  arriving ray's record exact (amount = passed + sunk + the whole quantum
  its two fractions make), and clicked + sunk + held = 2048 in every world
  (the chain of four: 1095 + 950 + 3). The polarization of every ray
  leaving each polarizer is the body's angle (32, 64, 96, 128 in the chain
  of four), read from the `polarizer` records and carried on every segment
  of the viewer documents. Run times 0.08 to 0.34 s per world; the records
  and the viewer documents (`ray-recording.json`, `viewer/runs.json` per
  world) stay outside the tree, `record.json` holds the integers and the
  README the
  tables. Nothing was tuned after the first look: the eight worlds were run
  once on the feature's commit and once more on the merge with `main`
  (PRs #246 to #248, records byte for byte the same in every number that
  the analysis reads), and the second run is the one recorded.

### A13. Bell test with polarization settings (after feature 11)

- **Confronts.** The CHSH violation with polarizers, S = 2.697 ± 0.015
  (Aspect, Grangier and Roger, 1982, two-channel polarizers; Aspect,
  Dalibard and Roger, 1982, time-varying analyzers) and the 2015 photon
  experiments of A2, at the settings 0°, 45°, 22.5°, 67.5°, quantum value
  2√2.
- **Model prediction today.** The same as A2 and A3: S ≤ 2 in the symmetric
  geometry (hypothesis 11 line 1), the joint law's value only in the delayed
  geometry (line 2); polarization changes the settings' form, not the
  mechanism (3.26).
- **Features.** 1, 2, 3, 4, 5, 6, 7b, 9, 10, 11.
- **Run.** The GameBoard and counts of A2 with each analyzer a polarizer of A12
  at the setting, its pass Port and sink Port each leading to a marked
  Detector at setting 1/2, the pair source emitting two light rays of one
  birth event carrying the same polarization record; the settings from a
  declared per-pair list; the symmetric geometry and then the delayed
  geometry of A3.
- **Criterion.** As A2 for the symmetric geometry and A3 for the delayed one,
  with the same no-signalling and unpaired-count conditions.
- **Status.** planned. Reading of 2026-09-17 (Highlights 5.4): a Detector
  reads the bit a ray carries (feature 2b), so the price of 5.4, S ≤ 2 in
  the symmetric geometry, is to be re-derived under that rule by hypothesis
  11 and this entry before it is quoted again; the prediction above stands
  as recorded until then.

### A9, the graviton detector: one click per whole unit (planned, 2026-09-19)

- **Confronts:** the single-graviton detector proposed by Tobar, Manikandan, Beitel and Pikovski (Nature Communications 15, 7229, 2024; construction begun in 2026): a massive acoustic resonator cooled to its ground state, weakly monitored, whose single quantum jump to its first level during a passing gravitational wave is one graviton absorbed, a gravito-phononic photoelectric effect; the key is to read individual transitions, since the mean energy is always consistent with a classical wave.
- **Under the law of events:** quantum gravity is not a property of the GameBoard but what a declared detector reads at a point (the model owner, 2026-09-19: "quantum gravity is behind a detector; we need a detector for it"). The detector is a measured event with the table `measure` for the family read and `threshold` 1: one click per whole unit, its record carrying the emitter's number, the momentum entered and the phase read. The GameBoard is whole by construction, so such a detector always reads whole units; what is measured is the count per interval against the distance and the time, and the size of one click against the detector's declared width.
- **What is missing before the run:** the units of the free family (the field of matter) carry no energy and no recoil, so they are not the graviton of nature, which is a quantum of a gravitational WAVE, emitted by accelerating masses and carrying energy. The run needs a paid family of gravitational waves (released at a measured event's acceleration, with recoil, with a phase circle and two polarizations as a second circle if wanted), not yet declared; the free family's suspension reads presence, not clicks.
- **Reading planned:** a lamp of the wave family and a detector at threshold 1 far from it: clicks per interval, their record, and the digital slowing of a clock at the detector's Node; the negative control a threshold above the bundle (no click).
- **Status:** planned; a catalog entry, no engine change until the wave family is declared by the owner.

## B. Proof for the paper

### B1. Exact conservation at every tick under every operation

- **Claim.** Highlights 3.15: "Every declared invariant is exact across an
  interaction so that the event can be rebuilt from its pieces when they
  return"; "Exact integer arithmetic is what makes the undoing exact."
- **Features.** 1, 2, 3, 4, 5, 6, 7, 8, 9, 10.
- **Run.** One world of 33 × 33 × 33 Nodes, open boundary, N = 2^8, that
  performs every operation of the engine within 2^12 intervals: a step on a
  Link, a split at an event, a meeting with N-to-M conversion, a field
  released and returned with recoil, a bound group formed and unbound, a
  Detector pass and a Detector return with its inverse split in each of the
  three modes (three runs), an escape at the open boundary. The audit sums
  energy, each momentum component, charge and family counts over resident,
  bound, in-flight, escaped and annulled content at every tick.
- **Shows.** A table of the per-tick sums, one constant line per invariant
  over the whole run, beside the count of operations of each kind per tick,
  and the residual line at zero; and, for the return, the invariants before
  the split and after the return equal, with the other shares untouched.
- **Status.** planned.

### B2. One draw only at a marked Node, and replay determinism

- **Claim.** Highlights 3.19: "For each transfer that arrives, whatever it
  is, it draws 1 or 0, the only lottery in the model"; 3.20: "Replaying one
  committed Detector decision returns the same result without another draw,
  emission or inventory charge."
- **Features.** 1, 2, 10.
- **Run.** A GameBoard of 33 × 33 × 33 Nodes, one marked Node with setting 1/2
  and 2^10 unmarked Nodes crossed by rays, 2^10 intervals; the audit counts
  tickets consumed per tick against arrivals at marked Nodes; a replay with
  the same seed; a second run with a different seed.
- **Shows.** Tickets consumed equal to arrivals at the marked Node at every
  tick and zero elsewhere; the replay's click record equal to the run's; and
  a spacetime diagram of the Nodes that differ between the two seeds, all
  inside the forward cone of the marked Node's first differing draw, one
  Link per interval.
- **Status.** planned.

### B3. The return retracing its steps, and the inverse split in three modes

- **Claim.** Highlights 3.19: "On 0 the Node returns that wave ray on the
  same line in the opposite direction, unchanged, back the same number of
  steps it has made since its event"; 3.20: "A return is the inverse split"
  and "Return modes": siblings, straight, annul.
- **Features.** 1, 2, 3, 4, 10.
- **Run.** A GameBoard of 65 × 65 × 65 Nodes; one event at the center with six
  outputs; a marked Node at distance d = 16 on the +x line with setting 0
  (every arrival returned); one run per mode. In the siblings run one sibling
  share is held by an output-clock delay on its line so that the transmission
  catches it. Recorded per tick: the returning ray's position and content;
  the transmission on the other lines; the sink total in annul mode; the
  audits.
- **Shows.** Three spacetime panels: the returned ray at position d − t
  reaching its event Node at tick 2d with steps 0 and content unchanged;
  siblings, the share and bit transmitted on the five other lines one Link
  per interval and the held share cancelled exactly where it is caught, with
  the invariants restored; straight, the ray continuing on the opposite
  line; annul, initial = current + escaped + annulled at every tick.
- **Status.** planned.

### B4. Two events at one Node in different layers

- **Claim.** Highlights 5.1: "two events can happen at the same Node in the
  same interval in layers that do not communicate, because rays whose
  families have no declared coupling never meet; they cross as if the other
  were not there."
- **Features.** 1, 5, 6, 10.
- **Run.** Four families A, B, C, D with couplings declared for {A, B} and
  {C, D} only; two rays A and B and two rays C and D arriving at one Node in
  one interval; the same two pairs run alone in two further worlds.
- **Shows.** A table of the events leaving the Node in the joint run beside
  the two solo runs, equal bit for bit, and the invariants of each layer
  summed separately and together.
- **Status.** planned.

### B5. N-to-M conversion with its invariants

- **Claim.** Highlights 3.3: "its result is at most six events, one per
  Port"; 3.26: "The weak interaction is a change of family: an N-to-M
  conversion at an event with its declared invariants (charge, energy,
  momentum)."
- **Features.** 1, 5, 6, 9, 10.
- **Run.** Five meetings on a small GameBoard in catalog keV units: 1 to 3
  (neutron to proton, electron, antineutrino), 2 to 2 (a Compton-like
  exchange), 2 to 3 (electron-positron to three light rays), 4 to 2 (a joint
  conversion), and a declared 1 to 7 that must be refused before commit.
- **Shows.** One table: inputs and outputs per meeting with energy, each
  momentum component, charge and family counts summed per column and the
  residual zero; the refusal of the seventh output with nothing mutated.
- **Status.** planned.

### B6. The field released in all directions, the recoil, and the free ray paying nothing

- **Claim.** Highlights 3.5: "The field is released in all directions";
  "the field ray itself returning reversed: the return is the opposite
  momentum of the field, carried back along the field ray's line to the ray
  that released it, which recoils when the return arrives, at finite speed";
  "Until its field meets something, a traveling ray pays nothing for it."
- **Features.** 1, 5, 6, 7, 9, 10.
- **Run.** A GameBoard of 33 × 33 × 33 Nodes; one charged ray on a straight
  line, 2^6 intervals, its field rays counted per shell per tick; a second
  world with a target ray of a responding family at distance 8.
- **Shows.** The shell of field rays at successive ticks in three orthogonal
  cross-sections with the count per shell; the releasing ray's content
  constant tick by tick in the first world; in the second, the momentum
  lines of the releaser, the target and the field in flight summing to a
  constant, the target's change at tick 8 and the releaser's recoil at tick
  16, equal and opposite.
- **Status.** planned.

### B7. A straight ray never meets its own field

- **Claim.** Highlights 3.5: "A ray traveling straight never meets its own
  field: the field is born where the ray is and leaves at the causal speed,
  ahead of the ray or away from it, and the ray is never faster than its
  field; no exclusion rule is needed."
- **Features.** 1, 7, 10, and an output-clock delay (3.28, existing).
- **Run.** One ray with output-clock delay k = 1, 2, 4 and 8 on a straight
  line for 2^10 intervals; the audit counts every meeting of a ray with a
  field ray whose carried record is the ray's own event; a parallel ray at
  distance 3 as the control that is met; a run with one mirror event after
  which the ray crosses field it released earlier.
- **Shows.** A table: self-meetings per k, zero in every row; meetings with
  the parallel ray, nonzero; after the mirror event, the crossing counted as
  an ordinary meeting.
- **Status.** planned.

### B8. Binding as a delay, and unbinding by an arriving ray

- **Claim.** Highlights 3.4: "Binding is the interaction whose result is zero
  events: the rays stay at the Node and interact again every interval"; "The
  binding may be nothing more than a very large output-clock delay"; "It is
  unbound the same way anything else happens on the GameBoard: a ray arrives."
- **Features.** 1, 5, 6, 7, 8, 9, 10.
- **Run.** Two rays of declared families meeting at a Node under the binding
  coupling, held for 2^12 intervals; then a light ray of content E arriving,
  E below and above the declared threshold.
- **Shows.** The group's residence, retained energy and phase against tick
  (zero events, the phase advancing once per interval); the arrival below
  threshold crossing or returned by the coupling with the group intact; the
  arrival above threshold producing the events that leave, with the
  invariants exact.
- **Status.** planned.

### B9. Interference as steering by the declared table

- **Claim.** Highlights 3.3: "interference is steering: where rays meet in one
  layer, the declared coupling reads their phase difference and decides
  through which Port the shared content leaves, with every invariant exact;
  nothing is erased"; the table "cos²(δ/2) to sin²(δ/2)"; "It is declared,
  not derived."
- **Features.** 1, 5, 6, 9, 10.
- **Run.** Two rays of one event meeting again at one Node with phase
  difference δ swept over all N = 2^8 steps, content 2^8 units per ray; and
  the two-slit world of A1.
- **Shows.** A table of δ against the content on the first Port, the second
  Port and the owned remainder, equal to the declared table at every δ (all
  to one Port at 0, all to the other at N/2, half at N/4); and the fringe of
  A1 as the figure, with nothing read by any Detector.
- **Status.** planned.

### B10. Charge conservation

- **Claim.** Highlights 3.15 with 3.26: charge is "a family property in the
  catalog or a coupling table, read only at a meeting"; every declared
  invariant "exact across an interaction".
- **Features.** 1, 5, 6, 9, 10.
- **Run.** A world with electron (−1), positron (+1), proton (+1) and light
  (0) rays performing every conversion of B5 and a pair creation; and one
  declared conversion that would not conserve charge.
- **Shows.** The per-tick sum of charge over resident, bound, in-flight,
  escaped and annulled rays as one constant line; the non-conserving
  conversion refused before commit with nothing mutated.
- **Status.** planned.

### B11. The wide phase breaks nothing

- **Claim.** Highlights 3.11: "Ordinary core operations and their
  intermediates use bounded integers, without floating point, roots or
  trigonometry"; 3.17: "An overflow or unsupported numerical representation
  rejects the operation before mutation."
- **Features.** 1, 6, 9 with `phase_bits` from 12 to 75, 10.
- **Run.** The worlds of B1, B3 and B9 repeated at `phase_bits` = 12, 32, 64
  and 75, with a replay at each width; the steering table evaluated by the
  bounded rule at each width and compared at the 2^12 angles of the
  12-bit table.
- **Shows.** One table: width against audit residual (zero), draws, replay
  equality, the largest difference between the wide table at the 12-bit
  angles and the 12-bit table (within the declared rounding), and the host
  time per tick reported separately as host cost, not model time.
- **Status.** planned.

### B12. Siblings of one event: the record and the bit travel one Link per interval

- **Claim.** Highlights 3.20: "Rays that left the same last event carry the
  same record of it, and nothing reads that record until a Detector; that
  shared record, and the trajectory back to the event, are all there is to
  entanglement"; 5.4: "the value was carried through the birth event in event
  spacetime, one Link per interval."
- **Features.** 1, 2, 3, 4, 10.
- **Run.** The pair GameBoard of A2 without analyzers: the source at the center,
  Alice's Detector at 32 Links with setting 0 (every arrival returned), Bob's
  at 96 Links with setting 1, `return_mode` siblings; 2^8 pairs.
- **Shows.** A spacetime diagram of one pair: Alice's return at tick 32, the
  ray at the birth Node at tick 64, the transmission on Bob's line, and Bob's
  Detector receiving the bit at tick 64 + 96 = 160, after Bob's own ray
  arrived at tick 96; the table of arrival ticks over the 2^8 pairs, all
  equal.
- **Status.** planned.

### A14. Kinematic time dilation of a moving bound group

- **Confronts:** the Lorentz factor, clock rate √(1 − v²) (the muon lifetime in flight, 2.2 µs at rest, longer by γ in flight; Rossi–Hall 1941 and every accelerator since).
- **Model's prediction today:** hypothesis 15: everything moves at c, matter is slow only by its output clock, and a bound group's tick fires only while it is resident, so a group moving one Link every k intervals ticks at (k − 1)/k = 1 − v to first order; the per-face clocks of Highlights 3.28 may change the curve.
- **Features required:** 8 (binding, `ray_delay`), 9 (rest rate as the tick's phase advance).
- **Run design:** one bound group of a declared massive family at rest, and the same group given an initial motion of v = 1/2, 1/3, 1/4, 1/8 Links per interval along an axis and along a diagonal (DDA line), on a GameBoard long enough for 64 intervals with an open boundary; record the number of ticks (binding-rule firings) and the phase advanced in 64 intervals for each v and direction; totals exact.
- **Criterion:** the tick ratio moving/rest is compared with 1 − v and with √(1 − v²) at each v; the model's curve is the one it matches within the remainder tolerance of Highlights 3.17; a direction dependence beyond that tolerance is a GameBoard anisotropy and is reported as such. Pass for the paper is a clean curve; the confrontation is then the curve against nature's.
- **Status:** planned (after feature 8; after feature 14, binding as a loop,
  Highlights 3.4, 2026-09-17, the moving group's motion being its corners
  shifting and its clock the period of its loop).

## C. Order

The features land in the order 1 to 12. Each line names what its feature
unlocks; an entry runs when the last feature it names has landed.

1. Feature 1, ray state (done on 2026-09-17): unlocks no run by itself; every
   entry needs it.
2. Feature 2, the Node Detector bit (done on 2026-09-17): B2, whose
   return-free part can run today.
3. Feature 3, the return: the retrace panel of B3.
4. Feature 4, the inverse split with `return_mode`: B3 complete, B12, A4.
5. Feature 5, layers: B4.
6. Feature 6, the meeting with N-to-M conversion: B5 (its charge column
   after 9), B9 (its table at N = 2^12 today; the sweep after 9).
7. Feature 7, the field: B6, B7. Feature 7b, the external body, after it:
   no run by itself; the sinks, splitters, phase plates and polarizers of
   A1, A2, A3, A12 and A13 and the bodies of A6, A7 (its external-body
   series) and A8 are external bodies and wait for 8, 9 or 11.
8. Feature 8, binding and gravity by delay: B8, A7.
9. Feature 9, every ray a wave ray with charge and `phase_bits`: A1, A2, A3,
   A5, A6, A8, A9, A10, A11, B10, B11.
10. Feature 10, the audits: B1, and the exactness clauses of every entry
    above in their final form.
11. Feature 11, polarization: A12, A13.
12. Feature 12, field spreading (Highlights 3.5, 2026-09-17): A1, A2 and the
    diagonal series of A6.
13. Feature 14, binding as a loop (Highlights 3.4, 2026-09-17; design done
    on 2026-09-17, loop binding; implementation after
    feature 8b): E5, the ladder count of A10 in its loop form, and A14 once
    a moving loop exists.

## D. What is deleted

The historical example worlds and the study directories of the repository
(the dated research explorations of 2026-09-16, the named-particle gallery,
the family-conversion, isotropy, relativity, gravity and double-slit probes,
and the other example worlds and their runners) were removed on 2026-09-17
under the model owner's instruction that everything not used is deleted
(issue #164). Their dated results stay in the
[validation log](VALIDATION.md) with their original scope and fingerprints,
as history and not as evidence for the ray-event model. This register
replaces them: an experiment exists as an entry here, runs once at one
fingerprint under its pinned criterion, and is recorded in the validation
log; no experiment directory, harness or example world is kept in the tree.

## E. Demonstrations of events

Dated research runs under Highlights 5.5 that show one event of nature each
in the engine's language, with the rules that exist on `main` today. They are
not confrontations (no measured value is compared) and not tests: each is
made once by the runner (`run_initialization`) from its world file under
`examples/nature/`, whose README is the
dictionary from each physical word to the engine word, recorded here with
its fingerprint, and rendered with the ray viewer;
the records and the renders stay outside the tree. They stand beside B8,
which stays `planned`: B8 holds its group for 2^12 intervals and pins the
threshold criterion, while these runs show the events over a dozen ticks.
The families are catalog rays (`light`, `electron`, `proton`, `neutron`, the
charge unit e/3, the electron's rest rate 1); the couplings of E1 to E3 are
the worlds' own declarations, since the catalog holds no photon-absorption, no
photon-emission and no photofission coupling, and the proton's and the
neutron's rest rates, undecided in the catalog, are set to 1 for the picture;
E4's attraction is the world's declaration standing in for the catalog's open
sign rule, and its other couplings are catalog entries.

### E1. A photon absorbed by a bound electron

- **Claim.** Highlights 3.4 (model owner, 2026-09-17): binding is a periodic
  orbit of the meeting rule, and "an arriving ray meets a ring ray at a
  corner by the table declared for the families present, and its outputs
  leave the ring or join it". Here that table, `absorb`, is a corner table
  over `[electron, electron, light]`: the two electron rays turn as at every
  corner and the light leaves through the same Port as one of them, so the
  photon joins the loop and the group's content is 8 + 3 (3.28, mass as
  content).
- **Features.** 1, 5, 6, 9, 10, 14.
- **Run.** `examples/nature/absorption.json`: GameBoard 12 x 12 x 11, open,
  N = 8, no Detector, 24 ticks; the unit-square ring of E5 at the catalog's
  rest rate 1 (eight `electron` rays of amount 1, charge -3, one of each
  sense at every corner of P0 = (5,5,5), P1 = (6,5,5), P2 = (6,6,5),
  P3 = (5,6,5)); one light ray of amount 3 from (5,5,0) heading +Z, at P0
  after tick 5; `absorb` declared before `corner`.
- **Shows.** Ticks 1 to 4: the ring, every corner meeting every interval,
  phase t mod 8. Tick 5: the light at P0 with the corner's two rays; in the
  cycle of tick 5 `absorb` fires, the electrons turn as at every corner and
  the light leaves through +Y with the L ray, amount 3, phase 0, the event's
  Ports +X and +Y with shares 1 and 4. From tick 6 the photon walks the edge
  P0-P3 with the ring's rays, up with the L ray and down with the R ray,
  meeting the corner's pair at both ends in every interval: a period-2 orbit
  inside the ring's period-8 one, the group's content 11. The momentum the
  light's turns move is booked at the corner as the electrons' turns are,
  (0, 3, -3) after the odd ticks and (0, -3, -3) after the even ones in the
  world's sources and total. At every tick: totals electron 8, light 3, the
  charge line electron -24, every audit line balanced,
  `conserved_at_every_completed_tick` true. The record's reading (the ray
  viewer's extractor, ring):
  one group on the square, content 11 (electron 8, light 3), period 8, clock
  electron 1 and light 0, read from tick 5 to tick 23.
- **The literal translation refused.** As in the first record: the outputs
  rule "light a + electron m to electron rays only, content m + a" is
  refused at initialization with the electron's charge -3 (`ray meeting
  output 2 of family electron (charge -3) would change the total charge`)
  and, with the charge set to 0, at the meeting (`ray meeting absorb changes
  the stock of a family`). The missing generic rule, a meeting whose outputs
  change family stock under declared invariants with a `converted` line in
  the audit, is stated in the dictionary and is not added by this run.
- **Status.** measured on 2026-09-17, commit `e3f5182ea614f84ffd6eee3a0343885800cc0ce0`,
  source `693ba4693afc98315b18cb616f3a2a35ce272573ada7b9beb52be6bf54b71077`,
  initialization `af9fd7819bd05c91b5bf95efa3b28e95f88891947d1a929dd201df8b0bdadd10`;
  outcome: the photon taken into the ring and kept there, exact at every
  tick. The first record, under the interim held form (commit
  `a2aea30888ca6969d8036ae5737b54cc5818b3c7`, source
  `5f89c465b235083ebb2e9284db1f172a094cefa8003b94ea38a04003a10d23cc`,
  initialization
  `8887461754ef2b5a32530f7fe86deaae4fcfef1b0e1f883fd99a23a3d605cac7`: the
  group `[electron, electron, light]` held at one Node with `ray_delay` 3),
  stays as the record of that form, removed by feature 14 the same day.

### E2. Photofission of a two-body nucleus, with the control below threshold

- **Claim.** Highlights 3.4 (a bound group "is unbound the same way anything
  else happens on the GameBoard: a ray arrives (a high-energy light ray, for
  instance)") and 3.26 (the threshold is a table entry read at the meeting):
  the outputs rule fires only when the light's amount is at least 4, its
  guard `gt(amount of the light, 3)`, and a photon below that crosses; under
  binding as a loop the photon above threshold stops the corner's turn and
  the pair flies apart on its own headings, momentum exact by heading, and
  the ring, its partners gone, disperses.
- **Features.** 1, 5, 6, 9, 10, 14.
- **Run.** `examples/nature/photofission.json`: GameBoard 26 x 26 x 11, open,
  N = 8, no Detector, 32 ticks; the four-ray ring of the design (two rays per
  sense at opposite corners), a proton ray (amount 6, charge +3, rest rate 1)
  circulating one way from P0 = (20,20,5) and P2 = (21,21,5) and a neutron
  ray (amount 6, charge 0, rest rate 1) the other, under the corner table
  `strong` over `[proton, neutron]` (the Port form); the low light of amount
  2 from (0,20,5) heading +X, at P0 after tick 20, and the high light of
  amount 6 from (20,0,5) heading +Y, at P3 = (20,21,5) after tick 21;
  `photofission`, declared before `strong`, with outputs proton, neutron and
  light each on its own heading (`"same"`), invariants energy and momentum,
  and the guard above.
- **Shows.** Tick 1: the pairs at P1 and P3; from tick 2 the pairs at P0 and
  P2 after the even ticks and at P1 and P3 after the odd ones, the corners
  turning them, content 24, the state repeating every 8 ticks: the record
  reads one group, ring the square, content 24 (proton 12, neutron 12),
  period 8, clock 1 and 1, from tick 1 to tick 19. Ticks 20 and 21: the low
  light meets the pair at P0 and then at P1; the guard reads 2 > 3 as 0 both
  times, `strong` turns the pair and the light crosses, walking on along +X
  to the boundary (escaped at tick 26). Tick 21: the high light at P3 with
  the pair, the proton heading -X from P2 and the neutron +Y from P0; in the
  cycle of tick 21 the guard reads 6 > 3 as 1 and `photofission` fires: the
  proton continues -X to (19,21,5), the neutron +Y to (20,22,5) and the
  light +Y with it, three new event rays of the event's Ports -X and +Y with
  shares 6 and 12; momentum amount x heading (-6, 12, 0) before and after,
  exact, nothing booked. The other pair turns at P1 in the same cycle and
  arrives at P2 and P0 alone at tick 22: no partner, no rule, and each
  crosses off the ring at tick 23; no group from tick 20. Ticks 26 and 27:
  the neutron and the light of the split and then the lone proton leave
  through +Y; at tick 32 the proton of the split is at (9,21,5) and the lone
  neutron at (10,20,5), walking -X. At every tick: totals proton 12, neutron
  12, light 8 (in the world with the escaped), momentum exact with the
  corner turns booked as the corners' sources, the charge line proton +36,
  every audit line balanced, `conserved_at_every_completed_tick` true.
- **Status.** measured on 2026-09-17, commit `e3f5182ea614f84ffd6eee3a0343885800cc0ce0`,
  source `693ba4693afc98315b18cb616f3a2a35ce272573ada7b9beb52be6bf54b71077`,
  initialization `89e2e6d897dbb41d5ee81702034b8b1973c16df0c3806cb8db74777a34814816`;
  outcome: the control crosses and the split happens as stated, the ring
  dispersing after it, exact at every tick. The first record, under the
  interim held form (commit `a2aea30888ca6969d8036ae5737b54cc5818b3c7`,
  source `5f89c465b235083ebb2e9284db1f172a094cefa8003b94ea38a04003a10d23cc`,
  initialization
  `7f8a490db98a1658860c54d3a6b0bb03781366122de31a7a1421dcc65f83bf7f`: one
  proton and one neutron held at one Node), stays as the record of that
  form, removed by feature 14 the same day.

### E3. Absorption and emission: the photon carried in a bound electron and released

- **Claim.** Highlights 3.4 (a group is unbound, or changed, by the coupling
  declared for the families present) and 3.3 (a light ray carries the phase
  of the clock that emitted it): the light ray taken into the ring leaves it
  again when the ring's clock reaches a declared phase, on a new heading and
  with the group's phase at emission, and the ground ring continues.
- **Features.** 1, 5, 6, 9, 10, 14.
- **Run.** `examples/nature/absorption_emission.json`: the GameBoard and ring
  of E1, 32 ticks; a light ray of amount 4 from (5,5,1) heading +Z, at P0
  after tick 4; `emit`, declared first, a corner table over
  `[electron, electron, light]` with the guard `eq(phase of the electron,
  1)` whose outputs are the electrons' turns and the light through Port +Z
  with the electron's phase; `absorb` (the table of E1) second; `corner`
  third.
- **Shows.** Tick 4: the light at P0 with the pair, the electron phase 4;
  the guard of `emit` is false and `absorb` fires: the photon joins the
  ring. Ticks 5 to 9: the photon walks the edge P0-P3 with the ring's rays
  (P3 after the odd ticks, P0 after the even), content 11, the electron
  phases 5, 6, 7, 0, 1. Cycle 9, at P3: the phase reads 1 and `emit` fires,
  the electrons turning as at every corner and the light leaving through +Z
  with phase 1, the event's Ports +X, -Y and +Z with shares 1, 1 and 4.
  Tick 10: the light at (5,6,6) heading +Z, phase 1, steps 1; the ring in
  its ground state, content 8; the momentum the photon brought in, (0, 0,
  4), leaves with it and the world's sources return to (0, 0, 0). Tick 14:
  the light at (5,6,10); tick 15: escaped. Ticks 10 to 31: the ground ring,
  which the record reads as one group, content 8, period 8, clock 1, from
  tick 10 (the excited state of ticks 4 to 9 is shorter than two of its
  periods and is read as no group). At every tick: totals electron 8, light
  4 (in the world with the escaped), the charge line electron -24, every
  audit line balanced, `conserved_at_every_completed_tick` true.
- **The lifetime is declared.** Five intervals, one integer, the ticks
  until the electron phase reads 1 at the corner where the light is. The
  half-life draw of Highlights 3.26 (a decaying group as a source, a source
  as a Detector drawing at each tick) is not in the engine, whose Detector
  mark draws on arrivals through Ports only; under the loop that draw would
  be at the corner meeting, the mark's setting applied once per meeting of
  the group's rays, and it is not added by this run.
- **Status.** measured on 2026-09-17, commit `e3f5182ea614f84ffd6eee3a0343885800cc0ce0`,
  source `693ba4693afc98315b18cb616f3a2a35ce272573ada7b9beb52be6bf54b71077`,
  initialization `3f76be865e45f36c7c0b3cf2b1c56243610db2813c7e7a90e5d4b0155d245a1a`;
  outcome: photon in, carried five intervals, photon out on a new heading
  with the group's phase, the ring back in its ground state, exact at every
  tick. The first record, under the interim held form (commit
  `84854f95da55ca3fc6dd6a43a7e7104bf94ad89e`, source
  `5f89c465b235083ebb2e9284db1f172a094cefa8003b94ea38a04003a10d23cc`,
  initialization
  `b0ba05326c876703651bbd80b25f09fa42efd562b057824c03ef5fe28f8eb8bf`: the
  photon held five intervals in a group at one Node), stays as the record
  of that form, removed by feature 14 the same day.

### E4. The helium ion: one electron at a nucleus of charge +2

- **Claim.** Highlights 3.19: the external body is "the approximation of
  infinite mass, used for the confrontation runs: ... an electron near a
  large charge, a hydrogen-like spectrum around a fixed proton"; 3.5: the
  body's field is its ordinary field rays, released on the six headings,
  and where a field ray meets a ray whose coupling responds the meeting
  changes that ray's trajectory and the field ray returns reversed; 3.4: the
  electron's trajectory "is changed at every step by the field rays" the
  nucleus releases. The model owner asked (2026-09-17) to see the He+ ion
  and to compute the orbit and the frequency a stable, closed orbit needs.
- **Features.** 1, 5, 6, 7, 7b, 9, 10.
- **Run.** `examples/nature/helium_ion.json`: GameBoard 41^3, open, N = 256, no
  Detector, 128 ticks (two computed periods). The nucleus: an external body
  of the `proton` family at (20, 20, 20), charge +6 (two protons), amount
  2^20, radiating light, the field of its charge (Highlights 3.5; the family
  `light_of_nucleus`, `field_of` `proton`, `release` [1, 4096]: 256 per axis
  ray per interval), coupled to the electron by the catalog's `phase_plate`
  at setting 0 (transparent) and pulled by absorbed field rays
  (`momentum_table` -1). The electron: one `electron` ray of amount 4 (rest
  rate 1, charge -3) from (28, 12, 20) heading +Y, the lower end of the side
  x = 28 of the square of half-side r = 8, releasing its own light
  (`light_of_electron`, [1, 4]); the catalog names one family per releaser.
  Couplings: `nucleus_turn` over `[electron, light_of_nucleus]`, the world's
  own declaration standing in for the open `opposite_charge` entry of
  `electron_field_turn` (A5): the electron leaves on the negation of the
  field ray's heading, the field ray returns reversed; `electron_field_turn`
  over `[electron, light_of_electron]` (never met); `phase_plate`. The
  catalog change of this run is one line: the proton among the releasers of
  `light`. The dictionary, the orbit computed and the limits are in the
  README.
- **Computed.** The square orbit of half-side r at speed 1/k: period
  T = 8 r k intervals, frequency 1/T; r = 8, k = 1: T = 64, f = 1/64. Its
  stability as integer equalities at every turn: the turn where the field
  is (the corners, which no axis line reaches); a whole quarter turn per
  turn (any field amount from 1 under the Port table; exactly
  floor(A t_p / u) = N under a delay table, one quantum low no turn, one
  quantum high an extra Link every N circuits); the four recoils of A on
  +x, +y, -x, -y summing to zero at the nucleus; the clock closing on the
  phase circle, 8 r k = j N once a table reads the phase difference (at
  N = 256, k = 1 the smallest square has r = 32).
- **Shows.** Ticks 1 to 8: the electron runs the side to the axis crossing
  (28, 20, 20), where the field ray released at tick 1 arrives in the same
  interval. Tick 9: the turn, a quarter turn toward the nucleus (-X), the
  recoil reversed behind it; not the square's next side. Ticks 9 to 15: the
  fall along the axis, a meeting and a recoil at every Node. Tick 16: the
  electron passes the nucleus; the eight recoils of 256 arrive in that one
  interval, the sink takes 2048, the body's momentum becomes (2048, 0, 0).
  Ticks 17 to 128: the cage, the electron turned back at the first Node
  past the nucleus on either side, positions 21, 20, 19, 20, 21, ..., one
  recoil of 256 every second interval alternating in sign, the body's
  momentum between 2048 and 1792, no Link stepped (2^20 needed). Observed
  period 4 intervals against the computed 64: the engine's bound state of
  He+ is a two-Link cage through the nucleus, for every r, m and field
  amount, because the body's field is on its six axis lines only and the
  landed turn is whole. At every tick: electron 4, none escaped;
  the nucleus's light sourced 1536 per tick, 16384 in the sink by tick 128
  (64 recoils); the momentum line balanced with the turns booked as its source
  (initial (0, 0, 0), sourced and current (-4, -4, 0) or (4, -4, 0)); the
  charge line electron -12, the bodies' line count 1, charge 6; every audit
  line balanced, `conserved_at_every_completed_tick` true.
- **The missing rules.** (i) The field off the axes: a field ray
  re-releasing its information on the five other headings by a declared
  table, the catalog's open `spread` of `light` (feature 12; the path
  counting of Highlights 3.5; today a field has no field).
  (ii) A turn proportional to the field: the lag of feature 8 is spent as a
  sideways Link with the heading unchanged and cannot reverse a ray, so a
  transverse lag that reaches N should be spent as a quarter turn of the
  heading toward the lagging side, the lag register being the transverse
  momentum the audit reads (Highlights 3.28, feature 8b). Neither is added
  by this run; with both, the orbit is a staircase circle of period 8 r k.
  Feature 8b landed on 2026-09-17 as `ray-momentum-turn-v1`: the transverse
  momentum is the ray's momentum register, pushed by a coupling's
  `momentum_table` and walked by the DDA ([a free ray turns by
  momentum](SPATIAL_FIELDS.md#a-free-ray-turns-by-momentum-ray-momentum-turn-v2));
  this run is not repeated. With both rules on `main` (feature 12 and 12b,
  feature 8b) the demonstration is made again as
  [E8](#e8-the-helium-ion-with-the-field-spreading-and-the-momentum-turn).
  The extractor of the ray viewer was corrected for this record: a ray a
  body's sink takes is not in the receiver's reading, so its transit now
  takes the amount from the `external_body_absorbed` record, and at a
  coupled body only the absorbed families end there.
- **Status.** measured on 2026-09-17, commit `12c387a05c2670bf472067110a7ba0bd32ab20e1`,
  source `5f89c465b235083ebb2e9284db1f172a094cefa8003b94ea38a04003a10d23cc`,
  initialization `3a72a69f4443222ee0280bb5815f55f4d051b76beb9e8d26f016d582b4fb6d98`;
  outcome: no closed orbit, the fall and the two-Link cage as stated, exact
  at every tick.

### E5. The ring: an electron at rest as a loop

- **Claim.** Highlights 3.4 (model owner, 2026-09-17): "Binding is a
  periodic orbit of the meeting rule": a ray never stops, a bound group is
  a set of rays whose meetings, under the ordinary coupling table, reproduce
  the rays that entered them, the smallest loop on the cubic GameBoard is a
  unit square of four Nodes with rays circulating both ways, each corner
  meeting every interval two rays that leave through each other's Ports,
  and a pattern whose meeting does not close disperses; 3.28: the group's
  mass is its content and its clock the period of its loop.
- **Features.** 1, 5, 6, 9, 10 for the meetings; 14 (`loop-binding-v1`,
  landed 2026-09-17 after 8b: the removal of the held form, the record's
  reading of a group).
- **Run.** `examples/nature/ring.json`: GameBoard 12 x 12 x 11, open, N = 8,
  no Detector, 16 ticks; eight `electron` rays of amount 1 (charge -3, rest
  rate 2) from eight lamps at the corners P0 = (5,5,5), P1 = (6,5,5),
  P2 = (6,6,5), P3 = (5,6,5), four circulating each way, one of each sense
  at every corner in every interval; the one rule `corner` over
  `[electron, electron]`, each input's amount and phase leaving through the
  Port the other input came in by (the Port form of the corner table).
  `examples/nature/ring_open.json`: the same with the catalog's Born table
  (`born_steering`) at the corner and the senses in phase, the control that
  disperses. The dictionary and the tick-by-tick states are in the
  README;
  the rule, the closure condition and the open points in
  loop binding.
- **Computed.** The closure of the unit square as integer equalities: a
  partner at every corner (two rays per sense at opposite corners at
  least, content 4; eight for every corner every interval), the headings by
  geometry, the amounts by the table (every amount under the Port form;
  equal senses at d = N/4 or 3N/4 under the Born table), and the phase
  `4 r = 0 (mod N)` for one circuit, r = 2 at N = 8; at the catalog's r =
  1 the state repeats after two circuits. A general rectangle a x b closes
  with `(a + b) / gcd(a, b)` rays per sense and `2 (a + b) r = 0 (mod N)`.
  The phase difference at a corner is a constant of the motion, so the rate
  is read at no meeting of one family; the Port form gives no ladder.
- **Shows (pinned before the run).** `ring.json`:
  from tick 2 every corner holds one ray of each sense, amount 1, steps 1,
  phase 2t mod 8, stamped by the corner it last left; the state after tick
  t + 4 is the state after tick t; each corner books the momentum of its two
  quarter turns as its source, (2, 2, 0) at P0 and the like, the four
  summing to zero; electron 8, momentum (0, 0, 0), the charge line -24,
  every ledger line balanced, no `bound_groups` in the snapshot (the key is
  gone with the held form), no `bound_tick`; the record's reading by the
  ray viewer's extractor: one group, ring P0, P1, P2, P3, content 8, period
  4, clock 2 on the 8-step circle, from tick 1. `ring_open.json`: after
  tick 2 one ray of amount 2 at each corner, walking +Y or -Y off the
  square, the GameBoard empty from tick 8, 8 escaped, every line balanced, no
  group read. The integers are pinned in
  test expectations beside the
  rate-1, four-ray and quadrature cases. A check run on `main` at
  `c21e03e` (2026-09-17, not this demonstration) agreed with every pinned
  line: the engine already held the ring under the Port form before the
  held form was removed.
- **Status.** measured on 2026-09-17, commit `e3f5182ea614f84ffd6eee3a0343885800cc0ce0`,
  source `693ba4693afc98315b18cb616f3a2a35ce272573ada7b9beb52be6bf54b71077`;
  `ring.json` initialization
  `7908d327bd9163414cf3c019aec9919c2a0cbdb79c086b6fd081e52b69f83fa8`,
  `ring_open.json` initialization
  `deeae3635bb5924ff90f36e9996f4acd7c7b6e235a5c6315630c62a5e442e539`;
  outcome: every pinned line as stated, the ring held and read as one group
  of content 8, period 4, clock 2, the control dispersed and read as none,
  exact at every tick.

### E6. The screen: the field of an electron at rest on seven marks

- **Claim.** Highlights 5.4 ("everything begins and is realized at a marked
  Node": the picture of the world is the list of PASS clicks, the eye view)
  and 3.5 (light is the field of a charge, and the field spreads by the
  split table of its family): an electron at rest releasing its field in
  front of a screen of Detector marks is seen as clicks, and the remainder
  rule of the split decides whether one mark or the whole screen is lit.
- **Features.** 1, 2, 7, 8, 9, 10 for the first record; 12
  (`field-spreading-v1`) for the second; 12b (`field-remainder-v1`) for the
  third.
- **Run.** `examples/nature/screen.json`: GameBoard 12 × 11 × 11, open, N = 8
  (`phase_bits` 3), 24 ticks; the electron at rest is the bound group of the
  dictionary, two `electron` lamps of amount 4 meeting at (1, 5, 5) at tick
  1 and held by `bind` (`delay` 1, `ray_delay` 1), content 8; `light` is its
  field (`field_of` electron, `release` [1, 4], the catalog's ratio),
  released on all six headings every interval; the screen is seven marks at
  (7, 2, 5) through (7, 8, 5), setting [1, 1], at distance 6 along +X.
  `examples/nature/screen_spread.json`: the same with `spread` `[6, 1, 1, 1,
  1, 1]` declared on `light`, the catalog's table, and nothing else changed;
  since feature 12b it runs 48 ticks (`ticks` raised from 24 on 2026-09-17,
  24 showing nothing off the axis).
  The dictionary and the eye view are in the
  README.
- **Shows.** Before spreading the field lives on the six axis lines of the
  group, so the +X line reaches the on-axis mark (7, 5, 5) alone: one click
  of amount 2 every tick from 7 to 24, eighteen clicks at that mark and none
  at the six others; light released 12 per interval (276 by tick 24, 214
  escaped at the open boundary, 62 in the world), electron 8, momentum (0,
  0, 0), the charge line electron -24, every ledger line balanced. With the
  split table the released rays of 2 spread at the first Node they reach, 1
  forward by the table and the remainder 1 through the entry the group's
  phase selects, and a single quantum then turns the same way at every Node,
  so the +X line still feeds the on-axis mark alone: twelve clicks at (7, 5,
  5), amount 24 in all, from tick 7, the six other marks never; light
  released 276, 207 escaped, 69 in the world at tick 24, electron 8,
  momentum (0, 0, 0), every ledger line balanced. The single-quantum
  finding: a phase-selected remainder sends a single quantum along one fixed
  line and leaves every Node off the axis dark, the reason for the model
  owner's decision of 2026-09-17 that the Node owns the remainder per family
  and heading and lets it leave whole when it reaches one quantum
  (Highlights 3.5, feature 12b). With the Node owning the remainder
  (`field-remainder-v1`, 2026-09-17) the field is whole quanta released
  where the registers fill, six of eleven parts forward per arrival at every
  Node: in 48 ticks the on-axis mark (7, 5, 5) clicks four times, at ticks
  19, 30, 39 and 48, amount 1 each, and the six other marks not yet (a
  transverse release takes eleven arrivals at one Node, then five forward
  ones); light released 564, 112 escaped, 452 in the world (376 in the
  registers), electron 8, momentum (0, 0, 0), every ledger line balanced.
  Run for 240 ticks (the same world under the runner's `ticks` override,
  the record registered below) it clicks all seven marks, symmetric about
  the axis and the on-axis mark most: 27 at (7, 5, 5) from tick 19, 6 each
  at (7, 4, 5) and (7, 6, 5) from tick 82, 3 each at (7, 3, 5) and (7, 7,
  5) from tick 122, 1 each at (7, 2, 5) and (7, 8, 5) at tick 193, 47
  clicks of amount 1 and 10 passes (4 on the axis, 2 at each of the next
  pair, 1 at each of the pair after, none at the ends); light 1710 in the
  world and 1158 escaped at tick 240, electron 8, momentum (0, 0, 0), every
  ledger line balanced: the whole screen lit by the field of a charge at
  rest.
- **Status.** measured, 2026-09-17: `screen.json`, source
  `5f89c465b235083ebb2e9284db1f172a094cefa8003b94ea38a04003a10d23cc`,
  initialization
  `35dde6ad84145b5042285baadbb27810b5d30527554646cc67f5a69eac941cff`;
  `screen_spread.json`, source
  `3426aa1ddf25f30348d6238edb66b0454e484a237f40fcf9367bdb948d99c2c9`,
  initialization
  `34ce343eeb204d9a8b7b1b0c6e6b5c79a21eeb799f717b76d13514a18718fa2d`;
  outcome: one mark clicks in both records, eighteen times before spreading
  and twelve times with the split table, the single-quantum finding;
  `screen_spread.json` at 48 ticks after feature 12b (`field-remainder-v1`,
  2026-09-17), source
  `4c6e313ce9f0b14be95ce85b3c4f256d4072f2e81715ddf1f1071b44c11d33bb`,
  initialization
  `9b0473248483faf4e0bcc97100e40e411674c5846df130973ac503338c3983b8`;
  outcome: the on-axis mark clicks four times, the others not yet; the same
  world for 240 ticks (`ticks` override of the runner, `requested_ticks`
  240, the same two fingerprints, 33 s), commit
  `6f357052b6c18ab186e67d0113a0c82ff8b5a99d`; outcome: all seven marks
  click, 27, 6, 6, 3, 3, 1, 1 from the axis outward, the whole screen lit;
  the records stay outside the tree. Retired on 2026-09-17 with feature 14
  (`loop-binding-v1`): the three records ran under the interim held form
  (`bind`, `delay` 1, `ray_delay` 1), the last at commit `6f35705`, and the
  world files `screen.json` and `screen_spread.json` are removed from the
  tree with the held form, their fingerprints kept here. A loop of content
  8 releases nothing at the catalog's ratio `[1, 4]` (a ray of amount 1
  releases floor(1 / 4) = 0), and a radiating loop needs rays of amount 4,
  content 32 at least, a different demonstration: the screen under a loop
  is to be written and pinned anew, after A1's table and width, not
  silently rerun with another source. That demonstration is E9 below
  (`screen_loop.json`, 2026-09-17): this entry's screen and marks, the
  source the ring of E5 with rays of amount 4. E9 was measured the same day
  at commit `ed2078f`: the ring of content 32 lights all seven marks, 17, 4,
  4, 1, 1, 1, 1 from the axis outward, the first at tick 11, and stays bound
  while it radiates.

### E8. The helium ion with the field spreading and the momentum turn

- **Claim.** The claim of E4 (Highlights 3.19, 3.5, 3.4: an electron near a
  fixed large charge, its trajectory changed at every step by the field rays
  the nucleus releases) on the engine that holds the two rules E4 found
  missing: the field spreads off the axes by the catalog's split table with
  the Node-owned remainder (features 12 and 12b, `field-spreading-v1`,
  `field-remainder-v1`) and a free ray turns gradually by the momentum of the
  field rays it meets (feature 8b, `ray-momentum-turn-v1`). The model owner's
  request of 2026-09-17, to see the nucleus with the electron around it and to
  compute the orbit and the frequency a stable, closed orbit needs, is
  answered in the rule's own dynamics before the run and confronted with the
  record.
- **Features.** 1, 5, 6, 7, 7b, 8b, 9, 10, 12, 12b.
- **Run.** `examples/nature/helium_orbit.json`: GameBoard 15^3, open, N = 256, no
  Detector, 152 ticks. The nucleus: an external body of the `proton` family
  at (7, 7, 7), charge +6, amount 2^20, radiating `light_of_nucleus`
  (`field_of` `proton`, `release` [1, 749]: A = 1399 per heading per
  interval, `source_sign` +1) with `spread` [6, 1, 1, 1, 1, 1], coupled to
  the electron by `phase_plate` at setting 0 and pulled by what its sink takes
  (`momentum_table` -1). The electron: one `electron` ray of amount 256 (rest
  rate 1, charge -3) from a lamp at (13, 5, 7) heading +Y, held forty
  intervals by a launcher body at (13, 6, 7) (the coupling `launch`, an output
  `delay` under the guard `eq(phase, 1)`) so that the field fills the GameBoard
  before it moves, released at tick 42 through the tangent point (13, 7, 7)
  of the circle of radius 6. Couplings: `nucleus_turn` over `[electron,
  light_of_nucleus]` with `momentum_table` `{"light_of_nucleus": -1}`, the
  catalog's `electron_field_turn` in the momentum-table form with the sign of
  opposite charges, standing in for the open `opposite_charge` entry (A5);
  `launch`; `phase_plate`. No field of the electron is declared (a turning
  ray's transverse Links carry its own releases with it). The catalog is
  unchanged. `examples/nature/helium_orbit_axes.json`: the same without
  `spread`, the control. The GameBoard is 15^3 and the radius 6 rather than E4's
  41^3 and 8 because a spreading field keeps every Node of the GameBoard active
  at about 2.5 ms per Node and interval (the parallel backend is slower), so
  the smallest GameBoard around the orbit took about an hour for 152 ticks; the
  dictionary, the computation and the readings are in the
  README,
  and `examples/nature/helium_orbit_table.py` prints the record tick by tick
  with the verdict.
- **Computed.** In the rule's dynamics (the register turned by the net flux
  k / r^2, the ray walking one Link per interval along it) a circular orbit
  exists at every radius, register P = k / r and period 8 r in the L1 metric
  (frequency 1 / (8 r)), and is a neutral equilibrium: a radial displacement
  grows as t^2 / (2 r^2) with nothing to restore it, since the speed is the
  one speed of the GameBoard and the curvature k / (r^2 P) falls faster than 1 / r
  as the electron drifts out (Kepler's stability comes from the speed falling
  as the body climbs). So no stable closed orbit exists at any radius; the
  push per interval that keeps the circle of radius 6 is m tan(pi / 24) = 34
  for m = 256, T = 48. The exact mean field of the split table on this GameBoard
  (a linear map the Node-owned remainders realize on average): the nucleus's
  sink takes back 1.014 A of the 6 A released per interval; the mean inward
  push on the 48 Nodes of the digital circle is 0.0241 A per interval, 2.2
  times the isotropic S / (4 pi 36), the forward weight keeping a beam on each
  axis (0.065 A at the axis crossing, 0.011 A on the diagonals); 90 percent of
  its steady value at tick 40; hence A = 34 / 0.0241 = 1399. A push
  perpendicular to the register lengthens it by p^2 / (2 m) = 2.3 per
  interval, a second-order term of the integer map. The recoil of head-on
  content walks with the electron and cancels its push one interval later,
  content from behind drags it by 0.0114 A = 16 per interval, the transverse
  content pushes it inward by 0.0177 A = 25 (computed after the control's
  record and before the orbit's). Expected before the run: circulation for a
  fraction of a period, then a fall or an escape, the fall the likelier sign.
- **Shows.** Ticks 1 to 41: the field fills the GameBoard, a spread at 1757 of
  the 3375 Nodes by tick 12 and at every Node but the bodies' by tick 40,
  the sink's rate rising toward one sixth of the release as computed; the
  electron waits at the launcher.
  Tick 42: at the tangent point (13, 7, 7) five field rays push it, the +X
  axis beam 94 (the mean field 91) and 7, 11, 11, 11 on -X, -Y, +Z, -Z, the
  register (0, 256, 0) to (-87, 267, 0), five recoils reversed. Ticks 43 to
  49: straight up the line x = 13, one Link per interval, six field rays at
  every Node (the recoil of the head-on content among them, walking with the
  electron and pushing it back), the +X push 35 (the mean field 34), 25, 18,
  11, 8, 5, 3, the register (-118, 264, 0) to (-181, 256, 0); the accumulators
  reset at every push, so the DDA steps along the dominant axis only. Tick
  50: the electron leaves through the +Y face at (13, 14, 7), 7 Links from
  the nucleus, register (-181, 256, 0), escaped electron 256; the distance
  rose from 6.00 to 9.22 without a turn; 46 pushes summing to (-181, 0, 0).
  Ticks 51 to 152: the field alone. The control: the fall of E4 in the
  register's language, one push (-1399, 0, 0) at the axis crossing, two
  cancelling pushes per Node down the axis (the beam and its recoil), the
  nucleus at tick 48, the two-Link cage stepping outward along +Y late in
  the run, the body's momentum (1399, 37773, 0). At every tick: the light line exact (released 8394 per
  interval, 1275888 by tick 152, 258398 in the world, 798078 escaped, 219412
  in the two sinks), the momentum line balanced (sourced (-181, 0, 0),
  current (0, -256, 0), escaped (-181, 256, 0)), the bodies' line count 2,
  charge 6, momentum (-29, 12, 0); every audit line balanced,
  `conserved_at_every_completed_tick` true.
- **Verdict.** Escape, by the rules: (i) a ray pushed in every interval
  walks its register's dominant axis, since the push resets the DDA's
  accumulators, so in a field that reaches every Node the gradual turn has
  no Link to show on and the path is axis runs with whole quarter turns; (ii)
  the transverse impulse a straight half-line gathers from the 1/r^2 flux is
  k / R, 214 here by the mean field against the register's 256, so the axis
  never flips and the electron passes straight, on a GameBoard of any size; (iii)
  the neutral equilibrium of the computation. The engine on `main` gives the
  helium ion no circulating electron: a straight pass (this record) or an
  axis fall into E4's cage (the control). The mean field of the split table
  agrees with the record push by push (94 against 91, 35 against 34). The
  request of the model owner is answered as computed: a closed orbit at every
  radius at register k / r, none stable, and on the GameBoard none while every
  interval carries a push; what to decide is stated in the README's limits
  (the accumulators kept through a push; the speed of a heavy register).
- **Status.** measured on 2026-09-17, commit `6f357052b6c18ab186e67d0113a0c82ff8b5a99d`
  (`main` with features 12, 12b and 8b); `helium_orbit.json`, source
  `4c6e313ce9f0b14be95ce85b3c4f256d4072f2e81715ddf1f1071b44c11d33bb`,
  initialization
  `3504b35d676da504734c550970bdbfce8e0a4850f6fa06ea8da8e5d93a3a7422`,
  1589 s; `helium_orbit_axes.json`, source the same, initialization
  `7d5bf8977e64ce3420fb5f7d35f2bd051698bfd2d877a57b3a7ca9f46c87ffec`, 7 s;
  outcome: no closed orbit, the straight pass and the escape at tick 50 as
  stated, the control's fall at tick 48 and its cage, exact at every tick;
  the records stay outside the tree. The escape was recorded under
  `ray-momentum-turn-v1`, whose push reset the DDA's accumulators;
  `ray-momentum-turn-v2` (2026-09-17,
  [migration](MIGRATION.md#a-push-keeps-the-walk-on-2026-09-17-ray-momentum-turn-v2))
  keeps them. Repeated under v2 on 2026-09-17, commit
  `781ce52306091848b214a71109bcbd34dec0f2c7`, source
  `57d6c941dede850cb952948ad739e1e4216bc0e788ae38c37fdc52a710a23de2`:
  `helium_orbit.json` (initialization the same, 1621 s), outcome: an arc,
  not a straight pass: from the tangent point (13, 7, 7) the electron
  curves around the nucleus through (12, 9), (11, 11), (9, 13), (7, 13),
  (5, 13), (3, 12) to (0, 10), 23 pushed Links, distance 5.0 to 8.06 (L1 6
  to 11), the register (0, 256, 0) to (-174, -119, 0), and leaves through
  the x = 0 face at tick 64 with the far side of its path one Node outside
  the GameBoard, so the record ends at the GameBoard's edge; the ledger exact at
  every tick. And `helium_orbit_21.json`, the same world on 21 x 21 x 21
  with the nucleus at (10, 10, 10), the launch at (16, 10, 10) and 200
  ticks, initialization
  `9de7a51ac7e8808d8f41594950c138e8c957d766d9e44e644e4bd2e1b156dfe4`,
  5546 s: a quarter turn, from (16, 10) through (15, 12), (14, 14), (12,
  16) to (10, 17) at distance 7 with the register (-251, 26, 0), then a
  straight run along y = 17 with one -Y step, out through the x = 0 face at
  tick 66 at distance 11.66, 25 pushed Links, 154 pushes, no circuit; the
  ledger exact at all 200 ticks; outcome: escape, the transverse impulse
  the field delivers on the far side (about 50 over ten Links at distance
  7 to 11) far below the 256 a turn needs, as (ii) computed; so under v2
  the electron curves where the field is strong and goes straight where it
  is weak, and no GameBoard size closes the orbit at this m, R and A.

### E9. The screen with a loop source: the ring radiating on seven marks

- **Claim.** The claim of E6 (Highlights 5.4, the picture of the world is
  the list of PASS clicks; 3.5, light is the field of a charge and the field
  spreads by the split table of its family) with the source in the loop form
  of binding (3.4, 3.28; feature 14): an electron at rest is a ring of rays,
  and every ray in motion releases its field on the five headings other than
  its own at every Node it departs (3.5), booked as a source (3.15), so a
  ring radiates under nothing but the corner table and the catalog's release
  ratio, stays bound while it radiates because a release costs the ray
  nothing, and its spreading field lights the whole screen as E6's did. A
  ring of content 8 releases nothing at `[1, 4]`; this entry is the radiating
  ring E6's retirement asked for, written and pinned anew.
- **Features.** 1, 2, 5, 6, 7, 9, 10, 12, 12b, 14.
- **Run.** `examples/nature/screen_loop.json`: E6's GameBoard 12 x 11 x 11,
  open, N = 8 (`phase_bits` 3), 240 ticks in the file (E6's registered
  length, no override); E6's seven marks at (7, 2, 5) through (7, 8, 5),
  setting [1, 1] (every arrival passes), at distance 6 along +X from the
  source's first Node (1, 5, 5) and 5 from its second (2, 5, 5). The source:
  the ring of E5 with rays of amount 4, eight `electron` lamps (charge -3,
  the catalog's rest rate 1) at the corners of the unit square P0 =
  (1,5,5), P1 = (2,5,5), P2 = (2,5,6), P3 = (1,5,6), one of each sense at
  every corner, the R lamps on +X at P0, +Z at P1, -X at P2, -Z at P3 and
  the L lamps on +Z at P0, -X at P1, -Z at P2, +X at P3 (`ring.json`'s
  lamps with Y read as Z), content 32; the one rule `corner` over
  `[electron, electron]`, the Port form. `light` is declared as in the
  retired `screen_spread.json`: `field_of` electron, `release` [1, 4],
  `spread` [6, 1, 1, 1, 1, 1], rest rate 0, charge 0, its `source_sign` set
  by the engine from the electron's charge; 24 ray slots (E8's field
  family), since a corner receives field content on six Ports with up to
  three phases per Port. No rule names `light`: layers are derived, so it is
  a layer of its own and crosses the ring's Nodes unmet (`ray-layers-v1`),
  spreading there like at any Node; nothing is declared to say so, where
  E1's world declares `absorb` to say the opposite. The square lies in the
  plane y = 5, which contains the axis and is perpendicular to the marks'
  line, not in the plane z = 5 of the marks' line: a unit square in that
  plane would put two of its Nodes at y = 6 (or 4), one of them on the line
  of the mark (7, 6, 5) with an axis beam of its own, and the mirror about
  y = 5 that clause (3) of the criterion demands would be broken by
  construction; in the plane y = 5 the source, the marks and the split table
  are exactly symmetric under y -> 10 - y. The dictionary, the computation
  and the readings are in the
  README;
  `tests/test_screen_loop.py` pins the first ticks in isolation
  (expectations).
- **Computed (before the run).** The content: at `[1, 4]` a ray of amount a
  releases floor(a / 4) per heading, 0 for a < 4, so 4 is the least amount
  that radiates, and with one ray of each sense at every corner, as
  `ring.json` declares the electron (eight rays), content 32 is the least
  radiating ring of that electron; the four-ray loop of E5's `half` case
  would radiate at 16 but is not that electron. The rate: the catalog's 1,
  not `ring.json`'s 2 (chosen there so that the hand table closes in one
  circuit), because the light carries its releaser's clock and the source
  here is the catalog's electron, as E1's ring and E6's held group had it;
  at rate 1 the ring closes in two circuits, period 8, every ray at phase t
  mod 8 after tick t (E5's `slow` case), nothing lost. The release: the
  lamps' rays are fresh at tick 0 and release nothing; from the cycle of
  tick 1, every interval, each of the eight rays releases 1 on the five
  headings other than the one it departs on (the release is taken from the
  trajectory that leaves the corner meeting), 40 quanta per interval against
  E6's 12, 40 (t - 1) sourced by tick t, 9560 by tick 240. Per corner 10:
  the two departing rays' releases merge per heading (one phase, one sign),
  so P1 sends 2 on +X along the axis line y = 5, z = 5 toward the screen, 1
  on -X and 1 on +Z along the edges to P0 and P2, 2 on -Z, 2 on +Y and 2 on
  -Y; P2 sends 2 on +X along y = 5, z = 6, one Link beside the marks' plane;
  P0 and P3 send 2 on -X away from the screen; per interval the ring sends 6
  on each of +X, -X, +Z, -Z and 8 on each of +Y, -Y, of which 8 run along
  the four edges and reach the neighbouring corners in the next interval,
  where they are not met (no rule) and spread, so the corners' registers
  are sources of spread content as any Node's are. The phase: every release
  of the cycle of tick t carries the ring's phase t mod 8 and light's rate
  0 keeps it, so the source has a clock and the screen reads it: a quantum
  that reaches a mark on whole-quantum steps carries the phase of its
  release tick, and a quantum a register releases carries the phase of the
  coherent sum of the shares that filled it, which over eight consecutive
  intervals of this clock cancels to step 0 and otherwise is the phase of
  the shares beyond whole circles; the phases the marks see are read from
  the recording. The momentum: `light` binds no momentum field, so a spread
  and a release book none (as in E6) and the world's momentum is the
  corners' bookings of their two quarter turns, (8, 0, 8) at P0, (-8, 0, 8)
  at P1, (-8, 0, -8) at P2, (8, 0, -8) at P3 per interval, summing to zero:
  momentum (0, 0, 0) at every tick; electron 32 in the world and none
  escaped at every tick, the charge line -96; light current (rays and
  registers) plus escaped equal to sourced. The order of the first clicks:
  the on-axis mark (7, 5, 5) first, fed by the axis line from P1, two fresh
  quanta per interval plus P1's register releases (the edge light of P0
  arriving on +X fills P1's +X register by 6/11 per interval), a stronger
  beam than E6's 2 starting one Node nearer the screen, so before E6's tick
  19; then (7, 4, 5) and (7, 6, 5) in one tick, then (7, 3, 5) and (7, 7, 5),
  then (7, 2, 5) and (7, 8, 5), each pair in the same tick with the same
  amount by the mirror, the counts falling outward as E6's 27, 6, 6, 3, 3,
  1, 1; the ticks are the run's to give.
- **Criterion (written before the run).** Pass, all of: (1) every ledger
  line balanced at every completed tick and
  `conserved_at_every_completed_tick` true; (2) the record's group reader
  (the ray viewer's extractor with the recording) reads exactly one group,
  ring P0, P1, P2, P3, content 32, `{"electron": 32}`, period 8, clock 1 on
  8 steps, from tick 1 to tick 239, so that the eight ring rays' states
  recur at every corner through the whole run: the source stays bound while
  radiating and its content does not change, because a release is booked as
  a source (Highlights 3.15); (3) all seven marks click within 240 ticks,
  the pairs (7, 4, 5) and (7, 6, 5), (7, 3, 5) and (7, 7, 5), (7, 2, 5) and
  (7, 8, 5) with equal click counts, and the on-axis mark (7, 5, 5) with
  the most; (4) no light ray meets a ring ray: `ray_layer_families` in
  `run.json` lists `light` in a layer of its own, the events of the record
  are of the kinds `spatial_cycle` (the corner meetings and the releases,
  read in its `source_delta`), `spatial_sent`, `spatial_received`,
  `spatial_escaped`, `field_spread`, `detector_click` and `detector_pass`
  only, beside the host's cycle records, and the electron line has no
  source, no escape, no annulment and no absorption at any tick. Fail: any
  one clause, stated as which and why. The run is made once; nothing is
  tuned after it, and if its first look forces a change, both records are
  kept and said so.
- **Shows.** Run once, 240 ticks, 92 s. The clicks: 29, every one of
  family `light`, bit 1, 28 of amount 1 and one of amount 2 (tick 63, two
  whole quanta merged on one Port in one interval); (7, 5, 5) 17 at ticks
  11, 15, 18, 22, 27, 27, 31, 34, 37, 41, 42, 43, 51, 59, 63, 67 and 69
  (the first eight ticks before E6's 19, as computed; the one at 43
  through the +Z face from the line y = 5, z = 6 of P2, the others through
  the -X face, the axis line from P1); (7, 4, 5) and (7, 6, 5) 4 each at
  34, 46, 54 and 72; (7, 2, 5) and (7, 8, 5) once each at 70; (7, 3, 5) and
  (7, 7, 5) once each at 71; the pairs tick for tick with the same amount;
  the last click at tick 72, and from 73 to 240 no mark clicks. The passes:
  378 `detector_pass` (376 of amount 1, 2 of amount 2, all bit 1), 120 at
  the on-axis mark from tick 46, 61, 42 and 26 at each mark of the pairs
  outward from ticks 43, 50 and 95, mirrored tick for tick, against E6's 10
  passes among 47 clicks: a mark is a Node that spreads, and a spread's
  departures carry the combined bit of the interval's arrivals (1 outranks
  0 outranks none, Highlights 5.4), so the read bit leaves a mark on all six
  headings, along the screen and back toward the source, and from tick 71
  every axis-line arrival at (7, 5, 5) carries it: the screen's own read
  light fills the field in front of it and the marks stop clicking, a
  finding of the record. The phases, from the `field_spread` record at the
  mark at each click: on the axis 3, 1, 2, 1, 2, 2, 0, then 1, 1, 1, then
  step 2 at every click from tick 42, off the axis step 2 but the outermost
  pair's 3; 102 of the 113 spreads at the on-axis mark record step 2: the
  ring's clock is not read at the marks as a rotation, the registers'
  coherent sums settling at one step. The ledger after tick 240: light
  sourced 9560, current 3680 (620 on 594 rays, 3060 in the registers of
  1177 Node-and-sign blocks), escaped 5880; electron 32 at every tick with
  no source, escape, annulment or absorption; momentum (0, 0, 0); charge
  electron -96, light 0; every line balanced at every tick,
  `conserved_at_every_completed_tick` true. The group: the extractor with
  the recording reads exactly one, ring (1, 5, 5), (2, 5, 5), (2, 5, 6),
  (1, 5, 6), content 32, `{"electron": 32}`, period 8, clock 1 on 8 steps,
  from tick 1 to tick 239 over 1912 electron chains, every tick row from 1
  to 239 bound `{"electron": [32]}`, the eight rays at the corners at
  amount 4 and phase 0 after tick 240 as after tick 8. The events:
  `spatial_cycle` 181351, `spatial_sent` 98825, `spatial_received` 62808,
  `field_spread` 62403, `spatial_escaped` 5444, `detector_click` 29,
  `detector_pass` 378, `cycle_started` and `cycle_committed` 960 each, no
  other kind; `ray_layer_families` `[["electron"], ["light"]]`. The
  readings tick by tick, the eye view and the deviations from the
  computation are in the
  README.
- **Status.** measured, 2026-09-17, commit
  `ed2078f1dfc73f97f682d0bc3cf1c5dab6eb8810` (the commit that carries this
  entry and the world); `screen_loop.json`, source
  `693ba4693afc98315b18cb616f3a2a35ce272573ada7b9beb52be6bf54b71077`,
  initialization
  `e1984daf7ff47f2cc243a8fed7d60a3717da1b7c150af49a79656150b1640ac9`, 240
  ticks, 92 s; outcome: pass in every clause. (1) every ledger line
  balanced at every completed tick, `conserved_at_every_completed_tick`
  true; (2) one group, the ring, content 32, `{"electron": 32}`, period 8,
  clock 1 on 8 steps, from tick 1 to tick 239; (3) all seven marks click,
  17, 4, 4, 1, 1, 1, 1 from the axis outward, the pairs equal, the on-axis
  mark most; (4) `light` in a layer of its own, the events of the kinds
  listed only, the electron line without source, escape, annulment or
  absorption at every tick. Deviations from the computation, none from the
  criterion: the order of the first clicks (the outermost pair at tick 70,
  one interval before the next pair at 71; computed: the pairs from the
  axis outward), the counts (the two outer pairs equal at 1; computed:
  falling as E6's 27, 6, 6, 3, 3, 1, 1), one click of amount 2 (computed:
  whole quanta of 1), and the 378 passes, which the computation did not
  consider and which end the clicking at tick 72. The isolated test
  (`tests/test_screen_loop.py`, 32 ticks) pins the first seven clicks, the
  light line and the group reading from the first run of its GameBoard
  (expectations). The
  record stays outside the tree; nothing was tuned after the run.
- **Repeated under `detector-absorb-v1` (2026-09-18).** Status: repeated on
  2026-09-18 under the decision of Highlights 5.4, "A click is an
  absorption" (model owner, 2026-09-18; feature 2c, [a click is an
  absorption](SPATIAL_FIELDS.md#a-click-is-an-absorption-detector-absorb-v1)),
  taken on this experiment's finding, the screen that remembers: a click on
  a field family now absorbs the quantum into the mark's exact counter, per
  family, with its momentum on the marks' line, and nothing of it spreads
  on. The world is unchanged (`screen_loop.json`, initialization
  `e1984daf7ff47f2cc243a8fed7d60a3717da1b7c150af49a79656150b1640ac9`, the
  marks on the `on_click` default of a field family, `light` being
  `field_of` `electron`), run once for 240 ticks on the engine of commit
  `10edd1dd` (the engine commit of feature 2c; source
  `2578f911f59a3883031b3ccf1d83f871569df8b217662c20f652d8fcb6823f52`), 94 s,
  read with the extractor and the recording (the 96-tick viewer document
  `runs_96.json`, "E9 under detector-absorb-v1: the screen counts", and a
  full reading for the group). The clicks: 265, every one of family
  `light`, amount 1, bit 1 and `absorbed` 1, the last at tick 240; per mark
  from the axis outward 109, 38, 38, 25, 25, 15, 15 against the first
  record's 17, 4, 4, 1, 1, 1, 1 (the pairs tick for tick with the same
  amount; the first click of each mark at 11, 34, 34, 50, 50, 70, 70, the
  first record's first arrivals, and (7, 3, 5) and (7, 7, 5) now click at 50
  where the first record's screen passed); the on-axis mark 92 through its
  -X face, 13 through +Z and 4 through -Z. The passes: none, against the
  first record's 378: no ray carries a bit any more, since what a mark
  realizes is no longer there to spread. The count keeps growing to tick
  240, as an intensity: 4, 14, 24, 19, 29, 34, 33, 32, 42, 34 clicks in the
  ten 24-tick windows over the whole screen (the on-axis mark 4, 10, 10, 9,
  13, 12, 13, 12, 14, 12), 14, 33, 58, 83 and 109 at the on-axis mark by
  ticks 48, 96, 144, 192 and 240, against the first record's last click at
  tick 72. The marks' counters after tick 240: light 15, 25, 38, 109, 38,
  25, 15, the marks' momentum (218, 0, -27) in all ((92, 0, -9) on the
  axis), the two sinks' totals light 265 and 0. The ledger after tick 240:
  light sourced 9560, current 3489, escaped 5806, absorbed by marks 265
  (on the way, sourced, current, escaped, absorbed by marks: tick 8: 280,
  264, 16, 0; 16: 600, 528, 70, 2; 32: 1240, 1009, 224, 7; 48: 1880, 1388,
  474, 18; 96: 3800, 2291, 1448, 61; 192: 7640, 3169, 4282, 189), against
  the first record's 9560, 3680, 5880 and no sink; electron 32 at every tick
  with no source, escape, annulment or absorption; momentum (0, 0, 0);
  charge electron -96, light 0; every line balanced at every tick,
  `conserved_at_every_completed_tick` true. The group: exactly one, the
  ring (1, 5, 5), (2, 5, 5), (2, 5, 6), (1, 5, 6), content 32, `{"electron":
  32}`, period 8, clock 1 on 8 steps, from tick 1 to tick 239 over 1912
  electron chains, every tick row bound `{"electron": [32]}`, as in the
  first record. The events: `spatial_cycle` 176018, `spatial_sent` 96225,
  `spatial_received` 60685, `field_spread` 60065, `spatial_escaped` 5369,
  `detector_click` 265, `cycle_started` and `cycle_committed` 960 each, no
  `detector_pass` and no other kind; `ray_layer_families` `[["electron"],
  ["light"]]`. Outcome: the criterion holds in every clause, (3) now with
  every mark counting through the run; the finding of the first record is
  what the decision removed, and the record shows it removed. The isolated
  test (`tests/test_screen_loop.py`, 32 ticks) was re-pinned from the new
  engine on 2026-09-18 with its expectations written first ([the screen
  with a loop](TEST_EXPECTATIONS.md#the-screen-with-a-loop)): the same
  seven clicks, each absorbed, the light line current 1009 and absorbed 7.
  The record stays outside the tree, the first record beside it; nothing
  was tuned after the run.

- **E9 repeated under the law of the bit (2026-09-18).**
  - **Claim.** The model owner's instruction of 2026-09-18: E9 repeated on
    the engine as it is on `origin/main` at `ffa4a56` (features 15 to 18 and
    16d part 1 merged) under the law of the bit (Highlights 5.4): the ring, a
    bound loop of one family, with its prefilled shadow set (a thing does not
    emit; `initial_field`), a screen of marks at distance L, N = 64, one K for
    the world, `wait_per_quantum` 1, the dense mode, no `spread`, `steering`,
    `mass_field` or `seed`; recorded per mark the things absorbed (the
    counts), the shadows returned and the pushed amount read at the mark's
    Node; then the same with the ring's things given a clock (K), and the
    fringes, if any, in counts and in the push. What the law says of it:
    point 24 (the Node mixes the six), point 6 (a mark absorbs things and
    returns shadows), point 10 (a thing has one path), point 14 (no lottery),
    point 3 (the return is a field); the settled rules of 5.4: "a screen
    beside a ring at rest counts nothing"; DERIVATIONS.md section 29 (a
    mirror in front of a source makes a standing wave of period lambda_w / 2
    in the push) and section 30 (the wave survives the integer rule above
    about 256 quanta per Node).
  - **Features.** 15 (`bit-law-v1`), 16b (`clock-readings-v1`), 16c
    (`node-mixing-v1`), 16d part 1 (`return-field-v1`), 17
    (`node-is-ports-v1`), 18 (`lanes-v1`), on 1, 2, 5, 6, 9, 10, 14.
  - **Run.** `examples/nature/e9_law/` (`make_worlds.py`): E9's
    `screen_loop.json` migrated by `bit_law_migration.migrate` and declared
    on the law: GameBoard 12 x 11 x 11, periodic (the model owner's decisions of
    2026-09-18, Highlights 5.4: the GameBoard of a run is closed, PR #311, and
    only closed worlds are tested, PR #314, so the series carries no
    open-GameBoard world), with a wall of marks over the plane x = 11 closing
    the wrap in x, as A1's closed GameBoard has, so that the shadows leaving the
    ring toward -X do not reach the screen from behind through the wrap
    (121 marks beside the screen's seven; what passes beside the screen's
    marks is returned by that wall toward -X, so the screen is reached from
    both sides); the ring of E5 on the unit square P0 = (1,5,5),
    P1 = (2,5,5), P2 = (2,5,6), P3 = (1,5,6) under the `corner` table, E6's
    seven marks at (7, 2, 5) to (7, 8, 5) at setting [1, 1], N = 64 (the
    world's `N`, the cleanup of 2026-09-18), K = 4096, `wait_per_quantum` 1,
    no `light` family (there is no field family: the ring's field is
    electron shadows, bit 0, point 12), the electron's `release` [1, 1], no
    ray slot budget (retired with the lanes, cleanup-law-v1 part 2, PR
    #315), rays of amount M = 32768 (content 262144): a thing's shadow set
    per interval of the fill is at most its content (`release` n at most
    d), so the content is what the instruction's size of the set forces
    (256 quanta of an owner at the screen's Nodes); the ring's eight corner
    lamps are eight things, since the engine makes every disturbance type a
    distinct thing (a shared `thing` is refused: "every disturbance type is
    a distinct thing"), so the ring's field is eight shadow sets;
    `initial_field` `{"electron": {"fill": 5}}`, declared when the engine
    at `ffa4a56` admitted no longer fill (below). The clock a family
    declares is 8 steps of 64 per interval per ray (content / K), E9's
    eighth of a turn: the derivation's period 8, lambda_w = 8 / sqrt(3)
    = 4.62 Links, lambda_w / 2 = 2.31 (DERIVATIONS.md 27 (v), 29). Three
    worlds: `ring_screen` (no clock), `ring_screen_clock` (`clock` true) and
    `ring_screen_clock_fill1` (the fill of 1, kept from the first
    measurement as the third world). 240 ticks, run once each through
    `tools/run_series.py --jobs 3` on the engine of `origin/main` at
    `204a513` (the cleanup part 2 merged, the ray slot budget retired; 338
    s, 355 s and 324 s, peak 860 to 865 MB, the dense mode on); the
    screen's marks replayed by `examples/nature/a1_law/record_screen.py`
    (`--screen-x 7 --wall-x 11`, probes on the axis at x = 3 to 7: a mark
    that only returns shadows publishes no record, so the shadows returned
    and the push J = the sum of amount x arrival heading at each mark's
    Node are read from the mark's resident rays after every tick of a
    replay checked against the run's events and fingerprint);
    `scan_fill.py` reads which fills the engine admits (`scan.json`);
    `analyze.py` reads the records (`record.json`). Measured first, earlier
    the same day, on the engine at `ffa4a56` (recorded below, not in the
    series): the same three worlds on the open GameBoard and then on this
    closed GameBoard, both refused by the ray slot budget.
  - **Result.** The three worlds complete their 240 ticks. The fills
    (`scan_fill.py`, 40 ticks asked of each, the clocked ring): 1 to 8 and
    16 all admitted and completed, 1,835,008 shadows at the start of the
    fill of 1 rising to 25,427,968 at 16; the prefill's refusal of a third
    phase on one Port of a source (fill 7 and above at `ffa4a56`) is not
    met any more. The runs:

    | World | Fill | Clock | Status | Ticks | Shadows at the start | Things | Clicks | Returned by the screen over the run | Elapsed |
    | --- | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
    | `ring_screen` | 5 | no | completed | 240 | 7,864,320 | 262,144 | 0 | 18,203,210 | 338 s |
    | `ring_screen_clock` | 5 | yes | completed | 240 | 7,864,320 | 262,144 | 0 | 18,203,210 | 355 s |
    | `ring_screen_clock_fill1` | 1 | yes | completed | 240 | 1,572,864 | 262,144 | 0 | 2,067,670 | 324 s |

    The counts: 0 at every mark in every world over 240 ticks (no thing
    leaves the ring: the real line 262,144 at every tick, nothing
    converted, escaped or absorbed). The books, all three: nothing escaped
    (the GameBoard is closed), nothing absorbed at home, nothing absorbed by
    the marks, the momentum line 0 throughout, every ledger line balanced,
    `conserved_at_every_completed_tick` and `real_conserved` true; the
    shadow line 7,864,320 (1,572,864 under the fill of 1) at the start and
    at tick 240. The clock: `ring_screen_clock` is identical to
    `ring_screen` tick for tick (the same `state.json` digest, the same
    ledger, the same screen record), since the prefill releases at phase 0
    and a re-release keeps a shadow's phase, so the clock enters no shadow.
    The screen, the fill of 5 (`record_screen.py`, `record.json`): the
    seven marks returned 18,203,210 quanta over the run, peaking at 268,596
    in tick 39, at phases 0 and 32 of 64 only (10,510,904 and 7,692,306),
    from the axis outward 4,635,928 at (7, 5, 5), 1,704,908 and 1,716,270
    at y = 4 and 6, 2,095,188 and 2,070,596 at y = 3 and 7, 2,992,160 and
    2,988,160 at y = 2 and 8 (the outer marks are 5 Links from the ring's
    plane through the wrap in y as well as 3 across it); the peak per tick
    104,764 on the axis (tick 39), 17,530 and 17,904 beside it; the first
    arrival at tick 1 on the axis and its neighbours (the prefilled shell
    of five intervals already reaches x = 7). The push J at the marks'
    Nodes summed over the run, (x, y, z), from y = 2 to 8: (76,034,
    715,212, -33,498), (-72,536, 0, -28,684), (107,136, 0, -50,092),
    (-247,026, 0, -219,682), (93,504, 0, -36,134), (-87,436, 0, -19,952),
    (84,580, -721,512, -22,800): J_x changes sign mark by mark along the
    screen, -247,026 on the axis (toward the ring: more arrives at that
    Node from the back wall's side than from the ring's) against +107,136
    and +93,504 beside it, a period of 2 Links; J_y is large at the two
    outer marks only, opposite in sign, and 0 elsewhere; the peak J_x per
    tick -68,156 on the axis. On the axis the peak amount per tick 116,920
    at (3, 5, 5) at tick 1, 35,658 at (4, 5, 5) at tick 72, 30,316 at
    (5, 5, 5) at tick 39, 39,398 at (6, 5, 5) at tick 92, 104,764 at
    (7, 5, 5) at tick 39, and 9,386, 11,950, 10,092, 4,356, 12,766 at tick
    240; the wall of 121 marks returned 95,453,010 quanta over the run
    (peak 522,078 per tick). The fill of 1: 2,067,670 returned (peak
    44,602 at tick 40; phases 0 and 32, 1,538,428 and 529,242), from the
    axis outward 446,766, 213,916 and 209,562, 258,690 and 259,782, 346,746
    and 332,208; J_x negative at every mark (-29,830 on the axis, -7,310
    to -1,106 elsewhere), J_y 68,584 and -69,168 at the outer marks; the
    first arrivals at ticks 4, 5, 6, 7 from the axis outward; the wall
    returned 17,371,346.

    Measured first, on the engine at `ffa4a56` (recorded, not in the
    series): the ray slot budget of a coupled layer (32 rays) refused the
    ring with its shadow set, on the open GameBoard and on this closed GameBoard
    alike, row for row: fills 1 to 5 admitted and failed at a corner ("ray
    slot budget exceeded") at tick 5 under the fill of 1, tick 2 under 2
    and tick 1 from 3 on (at 24 slots tick 3, 1 and refused at the
    prefill), fill 6 refused by the prefill on the same budget, fills 7, 8
    and 16 refused as "the prefill cannot hold a third phase on one Port of
    a source"; the three worlds failed at 0, 0 and 4 completed ticks (2.8
    to 2.9 s on the open GameBoard, 7.4 to 7.8 s on the closed one), 7,963,692
    (open) and 8,126,464 (closed) quanta at the start of the fill-5 worlds;
    the fill-1 record's four ticks: on the open GameBoard the shadow line
    1,435,300 at tick 4 with 137,564 escaped through the open faces and 8
    quanta returned by (7, 5, 5) at tick 4 at phase 0 with the push
    (8, 0, 0); on the closed GameBoard nothing escaped and nothing whole
    returned before the failure; the counts 0 in every case.
  - **Reading.** What the engine gave, against the predictions. The counts:
    0 at every mark over 240 ticks in all three worlds, the settled rule
    ("a screen beside a ring at rest counts nothing"), given in full: no
    thing leaves the ring, and the marks absorb nothing. The push: the
    marks turn back the ring's shadows every tick, an amount falling from
    the axis to its neighbours and rising again toward the outer marks
    (which the wrap in y brings as close to the ring's plane as the axis),
    and the push J_x along the screen alternates in sign mark by mark, a
    period of 2 Links against the lambda_w / 2 = 2.31 of section 29's
    standing wave in front of a mirror; but the clocked world is identical
    to the unclocked one, tick for tick, so no wave of lambda_w is in the
    run (the clock enters no shadow: the prefill releases at phase 0,
    `release_stock`, and a re-release keeps the shadow's phase,
    `rerelease_shadow`), and what arrived is at phases 0 and 32 only, the
    two phases the mixing makes of a phase-0 set (the half turn being the
    minus of point 24): the alternation is that of a real-valued shell
    mixed on the GameBoard and reflected by the screen and the back wall, not
    the standing wave of a monochromatic field, which this engine cannot
    build by a fill. The fringes of the derivation (sections 29 and 30):
    not given, for that reason; the integer rule is not what limits it (the
    axis Node holds 10^4 to 10^5 quanta per tick). The effect of the clock:
    none, as read from the code before the runs. The books hold on the
    closed GameBoard: nothing escapes, the field of the ring at rest circulates
    (Highlights 5.4, "The GameBoard of a run is closed"). Nothing is registered
    as a law.
  - **Fingerprint.** The series (the closed GameBoard, the engine with the
    lanes): source
    `67808df765d4bdfce1103fef3152d82149bc013070534a8459acc3ffaca5a828`,
    the engine of `origin/main` at `204a513` merged into the lane;
    initialization `ring_screen`
    `9e6343f9abde260cac2982d6331ed0d9d22f90aefb7d227f45743b5df0a693f3`,
    `ring_screen_clock`
    `5dffb272940b01c3cfc70517a452492605e1fe5bb3c5d3cc617b24024f6c19ba`,
    `ring_screen_clock_fill1`
    `a85395bf9ff59430ae6397a0bf008ca8df3deca0a43f4244dfa98ebdf97cbaf9`;
    `record.json` and `scan.json` beside the worlds hold the readings; the
    ray viewer's GIF of `ring_screen`. Measured first, at `ffa4a56` (source
    `6fef7cc04a71706cfd5dfdb496e20f6318a6bdfd6bf0c36e1379dbdd7934addc`):
    the open GameBoard `ring_screen`
    `09d27693188e5d8222f55f771c7481d0ffa93c96fb65bee06d4c64de0a5461c7`,
    `ring_screen_clock`
    `31c8ef78e33d4c5b5cca4c547b9008392c3193ae42832d980819141e8f4e730c`,
    `ring_screen_clock_fill1`
    `6d6f60fa05c0d5a245c154d0cd482bb54659b1db4105e4425aac14c61bb3b794`
    (those worlds declared the width as the family's `phase_bits` 6); the
    closed GameBoard at `1a88785` (source
    `051d716825c4785baffba01e46ea7348698fdfe82ca9ddc70eafab9871a49be5`)
    `4351f0ff34987b678d7cf6a1c4eed1d27effe88959e6b404ddd4ce56c0040df5`,
    `64c940104b8b69277bf07161f7e49fd28a9341aacfb9c3e77eeaad8409973918`,
    `545ce3c1314ec874427f02eb4687a68bb5458c87e2f1e5387739ec04372b789a`
    (those worlds carried `ray_slots` 32). The records stay outside the
    tree.
  - **Status.** measured, 2026-09-18, on the closed GameBoard (only closed
    worlds are tested, the model owner, 2026-09-18), on the engine with the
    lanes; outcome: the counts 0 at every mark over 240 ticks; the push
    read, the returned amount largest on the axis and J_x alternating in
    sign mark by mark out of a phase-0 shell, the clocked world identical
    to the unclocked (no wave of lambda_w in the run), no fringe of the
    derivation given; nothing escaped, the books balanced. Measured first
    at `ffa4a56`: refused by the ray slot budget, since retired.

### E10. The ring meets its own field: the loop under its own light, contents 32 to 128

- **Claim.** Highlights 3.5 (only after a change of trajectory can a ray
  cross field it released earlier, and that is a meeting like any other; the
  field is matter's message about itself, read by the table of the ray that
  meets it) with 3.4 (the ladder of hypothesis 12 is the set of contents
  that close a loop under the table) and loop binding
  sections 6, 7 and 11: on a ring every corner is a change of trajectory,
  so a ring meets its own field, and a content ladder can come only from
  the ring's rays meeting the group's own field rays under a table whose
  turn is produced by what is met. The question: does the E9 ring survive
  the field its own rays release when the catalog's `electron_field_turn`
  (feature 8b's momentum-table form, like charges repel) is declared beside
  the corner table, and does its content select which rings survive.
- **Features.** 1, 5, 6, 7, 8b (`ray-momentum-turn-v2`), 9, 10, 12, 12b, 14.
- **Run.** `examples/nature/e10_self_field/` (written by `make_worlds.py`):
  nine worlds, three per content. The ring of E5 (`ring.json`'s unit square
  P0 = (5,5,5), P1 = (6,5,5), P2 = (6,6,5), P3 = (5,6,5) in the plane
  z = 5, eight `electron` lamps, one of each sense at every corner, the Port
  form of the corner table) with E9's rays (amount 4, 8 or 16 per ray,
  content 32, 64 or 128, the catalog's rest rate 1, N = 8) on a
  12 x 12 x 12 open GameBoard, no Detector, 96 ticks (twelve periods of the
  rate-1 ring); `light` declared as in `screen_loop.json` (`field_of`
  electron, `release` [1, 4], `spread` [6, 1, 1, 1, 1, 1], rest rate 0,
  charge 0, 24 ray slots, its `source_sign` set by the engine), so a ray of
  amount a releases q = a / 4 = 1, 2 or 4 per heading. Per content:
  `control`, the corner table alone (E9's form, no rule names `light`);
  `corner_first`, the corner table and then `electron_field_turn` over
  `[electron, light]` with `momentum_table` `{"light": 1}`; `turn_first`,
  the same two rules in the other order. The two orders are two worlds
  because the engine meets a Node's rays in declared order and a ray one
  rule took is not available to a later rule in the same cycle (computed
  below). Recorded per world: `run.json`, `events.jsonl`, the recording of
  `record_sidecar.py` and the extractor's `runs.json`, kept outside the
  tree; `analyze.py` prints the per-tick reading, the pushes and the verdict
  table and writes `record.json`. The dictionary, the computation and the
  readings are in the
  README;
  `tests/test_ring_self_field.py` pins the content-32 worlds for 16 ticks
  (expectations).
- **Computed (before the run, from the code and the tables).** (i) A corner
  meeting resets the register: a meeting's outputs are fresh rays
  (`_output` in `src/event_universe/fields/ray_interactions.py`: heading,
  accumulators (0, 0, 0), amount, phase, `momentum` at its default `None`,
  the register amount x heading with an empty walk), so whatever push a ring
  ray carries into a corner is erased there; a push could accumulate only
  along one edge of the ring, one Link, and the unit square erases it at
  every corner. (ii) The declared order decides which rule meets a ring ray:
  `_meet` fires a layer's rules in declared order; a rule with outputs
  removes its participants and marks their slots used; a momentum-table
  rule takes one receiver per rule per Node per interval (the first group
  in role order then slot order, so the electron in the lower slot, the
  resident with the lower heading index: the L ray at P0 and P2, the R ray
  at P1 and P3) and every resident light ray, in heading-index order,
  returning each reversed; a slot an earlier rule used is not available to a
  later rule in the same cycle. On the unit square every ring Node is a
  corner and every ring ray arrives at a corner in every interval with its
  partner. So under `corner_first` the corner takes both electrons at every
  corner in every cycle, `electron_field_turn` finds none, no push ever
  happens, the light is met by nothing and spreads at the corners as in the
  control, and the coupled record is the control's event for event (the one
  difference the runner's `ray_layer_families`, one layer
  `[["electron", "light"]]`). Under `turn_first`, in the first cycle in
  which light is resident at the corners, the cycle of tick 2 (the releases
  of the cycle of tick 1 walk the edges and are received at the
  neighbouring corners at tick 2), one electron per corner is pushed by
  every light ray there and taken, the corner finds one electron and does
  not fire, both electrons cross straight, the pushed one along the DDA of
  its register and the other on its line, and the ring is off its Nodes at
  tick 3 for every content; the eight rays then walk through the field to
  the open boundary, pushed on the way wherever their line meets light.
  Neither order lets a ring ray be turned by the corner and pushed by its
  field in one cycle: the coupling can be declared beside the corner table
  (the nine worlds are admitted at initialization) but cannot act beside it
  at a corner, and on the unit square there is no other Node. (iii) The near
  field, the light met at a corner per interval, from the release and the
  split table, checked on 16-tick control probes made for this computation:
  the two departing rays of a corner release q on five headings each, the R
  ray's release on the L edge and the L ray's on the R edge run along the
  ring, so from tick 2 every corner receives two light rays of amount q on
  its two edge headings (at P0 heading -X from P1 and -Y from P3), 2, 4 and 8
  in all at contents 32, 64 and 128, the forward beam; the other eight
  releases leave the ring and their shares return through the neighbours'
  registers, the spread adding from tick 7, 5 and 4 respectively (the first
  whole quanta the registers release), the total per corner per interval
  reaching 6, 12 and 24 by tick 16, with at most 3, 5 and 10 on the two
  Ports of one axis. (iv) The push per interval at a corner, were it to
  act: +1 x amount x heading of each light ray met, so the edge rays push
  the receiver away from the neighbouring corners, (-q, -q, 0) at P0,
  (+q, -q, 0) at P1, (+q, +q, 0) at P2, (-q, +q, 0) at P3, outward along
  the diagonal, the four summing to zero; against a register of a on the
  ray's axis, a transverse push of q = a / 4 per edge ray, and at most 3, 5
  and 10 per interval from the near field read above against a = 4, 8 and
  16, is below a, so no interval's push flips the dominant axis: the DDA
  keeps the line and banks the transverse component toward a Link that
  would come after a / q = 4 intervals of the same push, which no edge of
  length 1 gives. Under `turn_first` at tick 2 the pushes are: at P0 the L
  ray (heading -X) from (-a, 0, 0) by (-q, 0, 0) then (0, -q, 0) to
  (-a - q, -q, 0); at P1 the R ray (+X) from (a, 0, 0) by (q, 0, 0) then
  (0, -q, 0) to (a + q, -q, 0); at P2 the L ray (+X) from (a, 0, 0) by
  (q, 0, 0) then (0, q, 0) to (a + q, q, 0); at P3 the R ray (+Y) from
  (0, a, 0) by (-q, 0, 0) then (0, q, 0) to (-q, a + q, 0): eight
  `ray_push` records at tick 2, two per corner, each field ray of amount q
  returned reversed (eight recoils), the four pushes summing to zero so the
  world's momentum line stays (0, 0, 0). (v) The prediction per content:
  `control` closed at 32, 64 and 128 (the Port form reproduces every amount,
  E5; the light sourced 40, 80 and 160 per interval); `corner_first` closed
  at 32, 64 and 128 with 0 pushes, event for event the control;
  `turn_first` dispersed at tick 3 at 32, 64 and 128 with 8 pushes at tick
  2 and more off the ring, no group read (fewer than two periods at the
  corners). No content is selected: the expected answer to section 7's
  question at this ring is that the self-field gives no ladder on the unit
  square, for a structural reason, one rule per ring ray per cycle, before
  any table is read, so the ladder at this ring stays the corner table's.
- **Criterion (written before the run).** For each world: "closed" if the
  record's group reader (the extractor with the recording) reads exactly one
  group on the ring's four Nodes with content `{"electron": C}` constant
  over the last 32 ticks (every tick row from 64 to 95 bound at C, the
  group's window from tick 64 or earlier to tick 95), C = 32, 64 or 128,
  the light not counted, and no electron packet received at a Node off the
  ring; else "dispersed at tick t", t the first tick an electron packet is
  received off the ring's Nodes or, if none, the first tick the reader's
  bound row lacks C. Every world: every ledger line balanced at every
  completed tick and `conserved_at_every_completed_tick` true; the recoils
  (the returned light) booked, one per push; the pushes per interval per
  content counted from `ray_push`. The outcome is the table content ->
  closed / dispersed for `corner_first` and `turn_first` beside the
  controls, and the answer to section 7's question: the self-field selects
  contents (a ladder: some contents closed, some dispersed), or every
  content survives (no ladder from this coupling on the unit square, the
  ladder then being the corner table's, the Born form's phase condition),
  or every content disperses (the loop needs the field not to push its own
  rays). The runs are made once; nothing is tuned after them, and if the
  first look forces a change, both records are kept and said so.
- **Shows.** Run once each, 96 ticks; the controls in 21.7, 44.7 and 79.4
  s (contents 32, 64, 128), `corner_first` in 22.7, 47.1 and 85.3 s,
  `turn_first` in 2.8, 4.8 and 7.9 s. The table:

  | Content | `control` | `corner_first` | `turn_first` |
  | --- | --- | --- | --- |
  | 32 | closed | closed, 0 pushes, the control's record line for line | dispersed at tick 3, 20 pushes |
  | 64 | closed | closed, 0 pushes, the control's record line for line | dispersed at tick 3, 20 pushes |
  | 128 | closed | closed, 0 pushes, the control's record line for line | dispersed at tick 3, 24 pushes |

  The six closed records: one group each, ring P0, P1, P2, P3, content C,
  `{"electron": C}`, period 8, clock 1 on 8 steps, from tick 1 to tick 95,
  every tick row from 1 to 95 bound at C, no electron packet received off
  the ring, no `ray_push`; the `corner_first` record equal to the control's
  in every event line with the host's `cost` removed (the digests of the
  cost-stripped lines equal at each content) and differing in the `cost`
  of every cycle record, which counts the light rays the one-layer meeting
  reads before it finds no electron free, and in `ray_layer_families`. The
  light met at the corners (all four together) 8, 16 and 32 per interval
  from tick 2, the spread adding from tick 7, 5 and 4; the largest amount
  at one corner in one interval over 96 ticks 8, 16 and 29, on the two
  Ports of one axis 4, 6 and 11 against a = 4, 8 and 16. The light line
  after tick 96: sourced 3800, current 3276, escaped 524 (32); 7600, 5456,
  2144 (64); 15200, 8232, 6968 (128); electron C at every tick; momentum
  (0, 0, 0) at every tick, each corner booking its two quarter turns. The
  three `turn_first` records: at tick 2 eight `ray_push` events, two per
  corner, the receiver the electron in the lower slot pushed by the two
  edge rays of amount q in heading-index order, the registers as computed
  at P0, P1 and P2 and at P3 from (-a, 0, 0) to (-a - q, 0, 0) to
  (-a - q, q, 0) (the R ray arrives at P3 heading -X; the computation had
  written +Y, the L ray's arrival), each corner booking its receiver's net
  push, (-q, -q, 0) at P0 and the like, the four summing to zero, eight
  recoils; the corner rule fires at no corner from tick 2, at tick 3 all
  eight electron packets are received off the ring and none reaches a
  corner again, no group is read; off the ring the escaping rays are pushed
  by the light released beside them, eight pushes at tick 3 along their
  lines and four (eight at 128) at tick 6 across, no line flipped; half the
  content escaped after tick 8 and all after tick 9; light sourced 300, 600
  and 1200 in all, the momentum line (0, 0, 0) and every ledger line
  balanced at every tick. Deviations from the computation, none from the
  criterion: the receiver's arrival heading at P3; the `cost` line of the
  `corner_first` record; the pushes after tick 3; the one-axis near field
  at content 32 reaching the ray's amount once over 96 ticks (the
  computation over 16 ticks had 3 below 4). The reading tick by tick is in
  the README.
- **Status.** measured, 2026-09-17, commit
  `2ababa5a6bd45618bdfc47686832d149cacd3061` (the worlds, the computation
  and the criterion; the readings, `record.json` and this status in the
  next commit of the same branch); source
  `aec35d9ec38c9c3778a3e2ef3966d996d0ffcadfb547c4626defa526b754d705`;
  initialization `c32_control`
  `8820f4c831b6ee77bfd3a78122efbd73b38793a3de24bdd93ee88b495de1d9b7`,
  `c32_corner_first`
  `ccc09423aa2b1b79f56b5003d961aa56655cef174c0c7ce34713369e437281d0`,
  `c32_turn_first`
  `41f9fb9d2b72d55c0de8f3285da79e40ef41fb76fabc994efebb799c987062e5`,
  `c64_control`
  `1dbbfd0b66571b9aabe7a2f984fcbb4de3b70ee0163e0b2ec5ca46c2b9599da4`,
  `c64_corner_first`
  `d5e8bcb70545e88ac2f2142d4da943c3afd050e309fd4af655bc28a222c2fdee`,
  `c64_turn_first`
  `b6538871347e8b2ace203f5bc4750490502ca2e0f88ed950634e9b47609a1265`,
  `c128_control`
  `837da1c3b47fb32c1ca549df934bf2c6c8c8808d49d5fe8e9e5a27e0619f9ae7`,
  `c128_corner_first`
  `04d72372be16a1dd5cd6140b9090ae50258c542f13f63754d8aea79d8873e8c7`,
  `c128_turn_first`
  `e51ea4b597c995c90b5f94a139bcba025b3db8fb0248924b7ac7dcbb3674bc83`; 96
  ticks each; outcome: no content selected. Under the corner first every
  content survives (no ladder from this coupling on the unit square, the
  ladder there being the corner table's); under the turn first every
  content disperses at tick 3 (the loop needs the field not to take its
  rays out of the corner meeting). Both are the one structural fact
  computed before the run, one rule per ring ray per cycle on a ring whose
  every Node is a corner, and no table entry was read: a self-field
  closure needs a ring Node where a ray is met by its field and not turned
  (a longer ring's side Nodes), or one table at the corner that reads the
  field met, which is the catalog's to write; the ledger exact at every
  tick in all nine records; nothing tuned after the runs; the records stay
  outside the tree, `record.json` beside the worlds. The isolated test
  (`tests/test_ring_self_field.py`, the content-32 worlds, 24 ticks) pins
  the pushes, the identity of the records and the group readings
  (expectations).

### E11. The field's books: the profile of a point source shell by shell, and the momentum between release and meeting

- **Claim.** The model owner's two questions of 2026-09-18, registered as
  asked, with tables and no power law assumed. (a) Highlights 3.15 (every
  declared invariant exact across every interaction and transfer, over all
  owners, fields, in-flight values and remainders included; a gain needs a
  loss, a transfer or an explicitly accounted source), 3.5 (the field
  spreads before it meets anything; a traveling ray pays nothing for its
  field until the field meets something; the release is booked as a source;
  the return is the opposite momentum of the field, carried back along the
  field ray's line to what released it, which recoils when the return
  arrives at finite speed), 3.14 (the recoil is a ray) and 3.19 (what a
  body radiates is booked as a source, what it absorbs as a sink, its
  momentum on its own line): the question is to show, in the books, where
  the energy and the momentum are between the release and the meeting, not
  only that the balance closes afterward. (b) Highlights 3.5 (the field of
  a static charge fills space; its density falls as 1/r and the net
  momentum its rays carry through a Node, what a met ray feels, as 1/r²,
  because the same flux crosses every shell) and [POSTULATES](../POSTULATES.md)
  (the addition of 2026-09-17: the net momentum through a node falling as
  1/r², Gauss): the question is a point source measured shell by shell,
  the total content, the content per Node, the radial momentum and the
  flux, and what actually comes out.
- **Features.** 7, 7b, 8b (`ray-momentum-turn-v2`), 10, 12, 12b, the dense
  mode (`dense-field-v1`).
- **Run.** `examples/nature/e11_field_books/` (written by `make_worlds.py`;
  the dictionary and the tables in the
  README).
  (b) `point_source.json`: one external body of family `proton` (amount
  2^20, charge +3) at (24, 24, 24) of a 49 × 49 × 49 open GameBoard, its
  `light` `field_of` `proton` with `release` [1, 256], 4096 quanta per
  heading per interval, `spread` [6, 1, 1, 1, 1, 1], the source sign from
  the body's charge, `dense_field` true, no mark, no second body, no
  matter ray; the body's table names its own light with +1 (the control of
  A5s), so its register must stay (0, 0, 0) by symmetry and the ledger
  shows it; one unseeded lamp binds the momentum field to the light
  (a5_static's device). `profile.py` runs it in-process and reads, per
  completed tick, the ledger (sourced, in flight, registers, escaped,
  absorbed, the momentum line, the body's register) and every L1 shell's
  total, and at the end, per L1 shell (|dx| + |dy| + |dz| = k) and per
  Euclidean shell (round(|r|) = k) for k = 1 to 22: the Nodes, the content
  in flight and in the registers, the content per Node, the radial
  momentum (Σ amount × (heading · r) as an integer and Σ amount ×
  (heading · r) / |r| as a real, per shell and per Node), the outward flux
  through the shell (the content that crossed the surface between k and
  k + 1 in the last interval: what arrived on shell k + 1 from shell k less
  what arrived on shell k from shell k + 1, from the arrivals and their
  headings; about the body, the release less the sink's take), the net
  momentum at the axis Node and at a diagonal Node of the shell, then the
  local log-log slopes between consecutive shells of the content per Node,
  the radial momentum per Node and the flux; and beside every column the
  mean field of the split table (`a5_static/mean_field_gauss.py`, the
  expectation of the engine's integers) in the same box at the same tick
  and at the box's steady state. Ticks: the plan says 600 or until every
  shell's total stops changing to 1 % over 32 ticks; the dense engine costs
  1.45 s per tick on this GameBoard (12 µs per Node and tick, the whole arrays
  every tick, measured before the run), so the budget of five minutes per
  world on the shared machine allows 192 ticks, six windows of 32, and the
  run is fixed at 192 with the criterion evaluated per shell and reported
  (a deviation, stated before the run). The reading: at the end of an
  interval every ray is resident at the Node it reached, so a Node's
  content in flight is what arrived there in the last interval, per
  heading, the mean field's f[j] at the same instant; the registers hold
  the shares below one quantum; the runner's `state.json` holds per Node a
  family's total and its ray count and not the amount per heading, so the
  per-Node reading is the inventory view in-process (the region's Nodes
  read back as Node state, the snapshot's own reading), the per-tick shell
  totals from the region's arrays, checked against the inventory at the
  end (a Recorder, Highlights 3.29). (a) `books.json`: a body A of family
  `proton` (amount 2^20, charge +3) at (10, 10, 10) of a 21 × 21 × 21 open
  GameBoard, its light with `release` [1, 4096], 256 per heading per interval,
  `spread` declared, `dense_field` true; one free `electron` ray of amount
  64 (charge −3, rest rate 1, no field of its own: nothing declares
  `field_of` `electron`) emitted by a lamp at (0, 14, 10) along +X, the
  line parallel to x at impact parameter b = 4 from A; the coupling
  `electron_field_turn` in its momentum-table form, `{"light": -1}`,
  attraction: the electron is pushed toward the source of every light ray
  it meets and each light ray is returned reversed; A's `momentum_table`
  `{"light": -1}` books what its sink takes; 2 × 10 + 16 = 36 ticks (ten
  Links from the entry to the closest approach). `books_axis.json`: the
  same without `spread` (the engine alone, which the dense mode does not
  admit without a spreading family): A's field lives on its six axis
  lines, the electron's line crosses A's +Y line at (10, 14, 10), and the
  one field ray met there returns whole along that line to A, four Links.
  The axis world is the picture Highlights 3.5 draws in words; the spread
  world is the catalog's rule; both are registered. `books.py` runs each
  in-process and prints per completed tick the light released and the
  source line, the light in flight and in the registers, the momentum of
  the light in flight (Σ amount × heading over the light rays, from the
  inventory; the recoils among them, event-stamped light rays not yet
  spread, counted apart), the pushes of the tick with the electron's change
  and the reversal they book, the electron's register and its change from
  its launch, A's register and its sink's momentum and amount, what
  escaped, and the identity at every tick.
- **Computed (from the code and the tables, checked on probes of the two
  book worlds before the registered runs).** (i) The labels: the engine
  labels a cycle's events (`ray_push`, `field_spread`) with the tick at the
  start of their interval and an arrival's, an absorption's or an escape's
  with the completed tick; the row T of the tables is the state after
  interval T with that interval's events. (ii) The axis world: the
  electron is at (t, 14, 10) after tick t; A's +Y ray released in interval
  t is at (10, 10 + s, 10) after tick t + s − 1; so the ray released at
  tick 7 and the electron are both resident at (10, 14, 10) after tick 10,
  the push is in interval 11, the recoil (a fresh event ray of 256 on −Y)
  walks back four Links and is absorbed by A at the end of interval 14:
  t0 = 7, t1 = 11, t2 = 14. The push moves the electron by −1 × 256 ×
  (0, 1, 0), the register (64, 0, 0) → (64, −256, 0), the DDA then taking
  four −Y Links per +X Link, and the meeting books the push (0, −256, 0)
  and the reversal −2 × 256 × (0, 1, 0) as its source; the light's momentum
  in flight, zero by the symmetry of the six lines, becomes (0, −512, 0):
  the met ray's +256 gone and the recoil's −256; when the recoil reaches A
  its −256 moves to the `absorbed` line and A's register gains −1 × 256 ×
  (0, −1, 0) = (0, 256, 0), toward the electron; the +Y ray taken out of
  the beam leaves its −Y partner unpaired, which escapes at tick 17 as
  (0, −256, 0) on the `escaped` line: the meeting's −3 × 256 on y is the
  electron's −256, A's absorbed −256 and the shadow's −256, every one on a
  ledger line. The turned electron then crosses A's +X line at (11, 10, 10)
  (a push of (−256, 0, 0) in interval 16, the recoil one Link from A,
  absorbed the same tick) and its −Y line at (10, 9, 10) (interval 18),
  walks −X along y = 9 and escapes at x = 0 after tick 27. (iii) The spread
  world: the electron meets whole quanta off A's axes from L1 distance 7
  on, the first push in interval 8 at (7, 14, 10) by two rays of amount 1
  (on −X and +Y, the front's content, released at tick 1 and spread at
  every Node since: t0 = 1, t1 = 8); at (10, 14, 10) in interval 11 the +Y
  beam (46 of the 256 → 139 → 75 → 40 chain plus what the registers and
  the neighbours added) pushes it toward A and its recoil walks −Y one
  Link, where the electron, now stepping −Y too, meets it again in
  interval 12 and reverses it a second time; the recoil of the 82 met at
  (10, 13, 10) in interval 12 is spread at (10, 12, 10) and again at
  (10, 11, 10), 44 then about 20 forward, and A's register first moves at
  tick 14, by (0, 20, 0): t2 = 14, a share and not a whole ray. A push's
  recoil is a fresh outbound event ray (`_recoil` in
  `fields/ray_interactions.py`, `source_sign` 0), and field spreading's
  "Consequences" paragraph applies to it: what walks back to the source is
  the forward share of each spread, the rest spreads sideways and escapes
  or meets the electron. The pull of 256-per-heading light at b = 4 on a
  ray of 64 is not a small deflection: the register turns from (64, 0, 0)
  through (66, −55, 0) at tick 11 to (−126, −128, 0) at tick 17, and the
  electron swings round A (below) instead of passing it; 36 ticks were planned
  for a passing electron and are kept. (iv) The profile: Gauss on the
  GameBoard is exact for the flux through every closed surface at the steady
  state (A5s, computed after the run: the outflow through every cube equals
  S to 10^−7), so at the box's steady state the flux column must be the same
  number at every k inside the box and the transient's flux must fall with
  k, the field still filling; the content per Node falls like the GameBoard
  Laplacian's Green's function scaled by 3/8 far from the source and like
  the beam 4096 (6/11)^(k−1) near it; the radial momentum per Node, the
  net momentum of the arrivals J, is 11/8 of the Link current, so at the
  steady state it falls as 1/k² where the current does (from k ≈ 21 in
  free space, A5s) and steeper inside the beam's range; at tick 192 the
  shells k ≲ 8 are near their steady state (t90 = 44 at r = 8), k = 12 at
  about 90 % (t90 = 164), k ≥ 16 well below (t90 = 354 at r = 16), and the
  box's boundary at 24 drains the outer shells, so the engine's columns are
  compared with the mean field at the same tick in the same box, the
  prediction, and the steady state of the box is given beside them.
- **Criterion (written before the run).** (b) No pass or fail clause: the
  model owner asked for the numbers; the tables are printed with the mean
  field beside them and the local slopes, and the ledger per tick shows the
  source's content unchanged while the field's total grows. (a) One
  clause, pass, all of: at every completed tick of both worlds every ledger
  line balanced (`ray-event-audit-v1`, re-checked from the integers), the
  momentum identity with the source line, sourced = light in flight +
  (the electron's register − its launch) + absorbed + escaped, the light's
  amount identity, sourced = in flight + registers + absorbed + escaped,
  and the electron's amount 64 (in the world or escaped); with t0, t1 and
  t2 marked in the table; and the plain statement of what the books say.
  The runs are made once; nothing is tuned after them.
- **Shows.** Run once each on 2026-09-18 (the point source 343 s for 192
  ticks, the spread book world 9.0 s, the axis book world 0.8 s); every
  ledger line balanced at every completed tick of all three; the tables in
  the README, the
  integers in `record.json`. (b) The profile. The ledger: the body's content
  2^20 at every tick and its register (0, 0, 0) at every tick; light sourced
  24576 per tick; at tick 192 sourced 4718592 = in flight 3492438 + registers
  278058 + escaped 159516 + absorbed 788580; nothing escapes before tick 88,
  and at tick 192 the escape is 3828 per interval and the sink's take 4288
  (the mean field's 4291 at the same tick, 4369 at the steady state) against
  the release of 24576, so the field is still filling the box (at the
  steady state the escape is the effective source S = 20206.7); the shells
  steady to 1 % over the last 32 ticks are k = 1 and 2 (0.2 and 0.6 %), k =
  8 changed by 4.4 %, k = 12 by 6.6 %, k = 16 by 10.1 %, k = 22 by 15.9 %.
  The engine's shells against the mean field at the same tick in the same
  box, per Node (L1 shells, in flight plus registers): 5639.0 / 5639.8 at k
  = 1, 2502.7 / 2504.3 at 2, 1075.8 / 1074.1 at 4, 438.5 / 436.6 at 8,
  230.5 / 229.9 at 12, 132.3 / 131.4 at 16, 60.9 / 59.3 at 22: the engine's
  integers are the mean field's expectation to a part in a thousand through
  k = 16 and to 3 % at k = 22, where the registers hold 5334 of the shell's
  118068. The box's steady state per Node: 5713.6, 2589.6, 1163.9, 524.2,
  310.9, 202.9, 113.7 at k = 1, 2, 4, 8, 12, 16, 22. The radial momentum per
  Node (Σ amount × (heading · r) / |r| over the shell's rays, over 4k² + 2
  Nodes), engine / mean field steady: 3651.0 / 3636.6, 1107.4 / 1104.3,
  273.4 / 272.4, 68.2 / 69.5, 30.3 / 31.7, 15.6 / 18.1, 7.3 / 9.7 at k = 1,
  2, 4, 8, 12, 16, 22; the shell's radial sum is nearly constant, 21906 at
  k = 1, 17591 at 8, 15999 at 16, 14210 at 22. The flux through the surface
  between shells k and k + 1 in the last interval, engine / mean field at the
  same tick: 20286 / 20285 at k = 1, 20166 / 20197 at 4, 19680 / 19783 at
  8, 19446 / 18867 at 12, 17304 / 17405 at 16, 13788 / 14418 at 22, the
  release less the sink's take 20286 about the body; the mean field's steady
  flux is 20206.7 through every one of the 22 shells, L1 and Euclidean
  alike, to one part in 10^8 (Gauss on the GameBoard), and the engine's
  transient flux is within 0.3 % of S through k = 7, 96 % at k = 12, 86 %
  at k = 16, 68 % at k = 22, the integer crossings of one interval
  scattering by a few per cent about the mean field's from k ≈ 12 on. The
  local log-log slopes between consecutive L1 shells, engine / mean field at
  the tick / mean field steady: the content per Node −1.17 / −1.17 / −1.14
  at 1–2, −1.21 to −1.27 through 5–6 (steady −1.13 to −1.14), −1.35 at 6–8,
  −1.51 at 8–10, −1.63 to −1.77 at 10–13, −1.9 to −2.3 at 13–18 and −2.3
  to −3.1 beyond, the transient's steepening; the steady state's −1.13
  through k = 6 steepening to −2.06 at 21–22, the wall at 24 draining. The
  radial momentum per Node −1.72 / −1.72 / −1.72 at 1–2, then −2.01, −2.04,
  −2.04, −1.99, −1.96, −2.02, −1.89, −2.13, −2.10, −1.86, −2.28, −2.43,
  −1.87, −2.70, −2.30, −2.44, −2.04, −3.19, −2.08, −2.16 (engine) against
  the steady state's −2.01, −2.03, −2.00, −1.97, −1.95, −1.94, −1.93,
  −1.93, −1.94, −1.94, −1.95, −1.95, −1.95, −1.96, −1.96, −1.96, −1.95,
  −1.95, −1.94, −1.93: 1/k² from k = 2 on, in the transient and at the
  steady state, with the integer noise growing outward. The flux 0.00 at
  every shell at the steady state and between 0 and −0.3 in the transient
  to k = 12, noisier beyond. At a Node the direction decides: the axis Node
  (k, 0, 0) reads 3651, 2089, 1208, 705, 419, 254, 156, 99, 64, 43, 30,
  21, 16, 14, 9, 7, 7, 7, 4, 3, 3, 3 for k = 1 to 22, the beam falling by
  6/11 per Link to k ≈ 9 and then a few whole quanta, and the diagonal Node
  (⌈k/2⌉, ⌊k/2⌋, 0) 3651, 617, 404, 281, 195, 140, 105, 78, 60, 50, 38,
  31, 25, 21, 18, 16, 11, 11, 10, 9, 8, 6, smoother and above the axis
  Node's from k = 10 on. The Euclidean shells (18, 62, 98, 210, 350, 450,
  602, 762, 1142, 1250, 1458, 1814, 2178, 2498, 2622, 3338, 3722, 4170,
  4358, 5034, 5714, 5982 Nodes) give the same picture with the shells'
  irregular counts in the slopes: the radial momentum per Node's steady
  slope −1.86, −1.49, −1.92, −2.36, −1.80, −1.98, −1.86, −2.09, −2.02,
  −1.93, −1.99, −1.96, −2.03, −1.92, −2.00, −2.02, −2.04, −1.97, −1.97,
  −2.05, −1.91, the flux the same S through every shell at the steady
  state. In one sentence: the flux through every shell is the same number
  once the field is steady, the radial momentum per Node on a shell falls
  as 1/k² from k = 2 on because that constant flux is shared by the shell's
  ≈ 4k² Nodes, the content per Node falls as k^−1.15 near the source and
  steepens toward the box's wall, and at one Node the number depends on
  the direction to the source and, far out, on which whole quanta arrived
  in that interval. (a) The books. Both worlds: every ledger line balanced
  at every tick; the momentum identity with the source line, sourced =
  light in flight + (the electron's register − its launch) + absorbed +
  escaped light, at every tick; the light's amount identity at every tick;
  the electron's amount 64 at every tick (in the world through tick 27 of
  the axis world and escaped from tick 28; in the world throughout the
  spread world); the lamp's register (−64, 0, 0) constant; the inventory's
  light equal to the ledger's in flight at every tick. The axis world: t0 =
  7, t1 = 11, t2 = 14 as computed. Ticks 1 to 10: the electron walks
  (t, 14, 10) with (64, 0, 0), the light 1536 per tick on the six lines, in
  flight 1536 t, momentum (0, 0, 0). Tick 11 (the push at (10, 14, 10) by
  the ray of 256 on +Y released at tick 7): the electron (64, −256, 0), the
  light's momentum in flight (0, −512, 0) with one recoil of 256 among the
  rays, sourced (0, −768, 0) = the push (0, −256, 0) + the reversal
  (0, −512, 0). Ticks 12 and 13: the electron steps −Y with the recoil and
  meets at (10, 13, 10) and (10, 12, 10) both the next beam ray and the
  recoil walking beside it, two pushes that cancel, the recoil re-reversed
  and walking out, the beam ray reversed anew. Tick 14: the recoil of the
  ray met at (10, 12, 10) reaches A: absorbed (0, −256, 0), A's register
  (0, 256, 0), the light in flight (0, −256, 0). Tick 16: the electron
  crosses A's +X line at (11, 10, 10), the push (−256, 0, 0), the recoil at
  A the same tick, A (256, 256, 0); tick 17: the −Y partner of the ray
  taken at tick 11 escapes unpaired, escaped light (0, −256, 0); tick 18:
  the −Y line at (10, 9, 10), the push (0, 256, 0), the recoil at A, A
  (256, 0, 0); the re-reversed recoils and the unpaired partners escape
  through tick 27; tick 28: the electron escapes at x = 0 with
  (−192, 0, 0). Over the encounter the electron's change is (−256, 0, 0)
  and A's register (256, 0, 0), equal and opposite; the source line holds
  (−768, 0, 0) = the electron's (−256, 0, 0) + absorbed (−256, 0, 0) +
  escaped light (−256, 0, 0), that is, per meeting −3 × amount × heading:
  the push, the recoil the sink takes, and the partner ray left unpaired
  on the opposite line. The spread world: t1 = 8 (two rays of amount 1 at
  (7, 14, 10)), t0 = 1 (the front), t2 = 14 (A's register (0, 20, 0), the
  forward share of the recoil of 82 after two spreads); 157 pushes, 2 to 8
  per tick from tick 8 to 34 and none at 35 and 36; the electron's
  register (65, −1, 0) at tick 8, (66, −55, 0) at 11, (42, −113, 0) at 14,
  (−126, −128, 0) at 17, (−160, 48, 0) at 21, (−27, 84, 0) at 36, its path
  (10, 14) → (10, 13) → (11, 13) → (11, 12) → (11, 11) → (12, 11) →
  (12, 10) → (12, 9) → (11, 9) → (11, 8) → (10, 8) → (9, 8) → (8, 8) →
  (8, 9) → (7, 9) → (7, 10) → (6, 10) → (6, 11) → (5, 11) → (5, 12) →
  (5, 13) → (4, 13) → (4, 14) → (4, 15) → (4, 16) → (3, 16) → (3, 17) in
  the plane z = 10: not a passing electron but a swing round A, turned by
  108° and leaving on the far side; the recoils in flight 2 to 8 rays of up
  to 204 quanta between spreads; A's register (0, 20, 0) at 14, (2, 24, 0)
  at 16, (70, 24, 0) at 18, (71, 22, 0) at 21, (70, −46, 0) at 22,
  (47, −45, 0) at 36; the momentum line at tick 36: sourced (−145, 106, 0)
  = the pushes (−91, 84, 0) + the reversals (−182, 168, 0) + the spreads'
  bookings (128, −146, 0), and sourced = light in flight (−5, −17, 0) +
  the electron's change (−91, 84, 0) + absorbed (−47, 45, 0) + escaped
  light (−2, −6, 0); light sourced 55296 = in flight 33760 + registers
  12510 + escaped 750 + absorbed 8276. So in the spread world A receives
  about half of the electron's change and the field keeps the rest: the
  recoils are spread on their way and mostly walk off their lines. What the
  books say, for the model owner: the field's energy is created at the
  release and booked as a source, the emitter's content unchanged (A holds
  2^20 at every tick of every world and its register moves only by what its
  sink absorbs); the field's momentum is zero net at the release (six equal
  headings) and is carried in flight by the rays, amount × heading each,
  between t0 and t1, where the books list it ray by ray; at t1 the meeting
  gives the electron −amount × heading and the field ray −2 × amount ×
  heading, both booked as the meeting's source; the recoil walks back and
  is absorbed at t2 (whole in the axis world, as a share in the spread
  world, the rest spread and escaping); everything not met escapes; and the
  balance closes at every tick with the source line. What is not conserved
  without that line: the amount, at every release (the emitter pays
  nothing, 24576 quanta per interval from nothing in (b)), and the momentum,
  at every meeting (−3 × amount × heading created by the declared table:
  attraction toward the source of a ray that arrives from the source cannot
  be paid by that ray) and at every spread (the shares that enter the
  registers carry none). Highlights 3.15 says exactly this, a gain by "an
  explicitly accounted source"; Highlights 3.5 says the emitter pays nothing
  until the meeting and that the recoil is carried back along the field
  ray's line to what released it: true whole in the axis world (the
  electron −256, A +256), true in part in the spread world (the recoil is
  spread from the next Node, the field spreading rule's own "Consequences"
  paragraph), and the emitter never pays in energy at all, only the sink's
  momentum booking moves it. Two sharpenings for the documents, no rule
  changed: a push's recoil carries `source_sign` 0 (`_recoil` builds a
  fresh ray), where the spreading rule's text says a meeting's output keeps
  its field's sign; and the recoil and the pushed electron walk the same
  Link when the push turns the electron along the ray's line, so the recoil
  is met again one interval later and re-reversed (both worlds).
  Deviations from the plan, stated before the runs: 192 ticks instead of
  600 (the cost); the reading in-process instead of from `state.json`; the
  axis world added beside the spread world; stated after: the electron of
  the spread world is captured for a swing round A rather than passing, and
  the first run of the profile was started on a world file still at 600
  ticks and stopped at tick 208, the worlds regenerated at 192 and the run
  made again from the start (its integers to tick 192 were the same).
- **Status.** measured on 2026-09-18, the engine of `main` at
  `9cc830f5` (no engine change on the branch; the branch's own commit is
  the pull request's head), source
  `25ecd24e87cea58753089a9b38c0d21620ec0eae8401a17d2b55b6352883f038`;
  initialization `point_source`
  `3fed14baaab130c06ce61d24636a2d9bae3a7ddb42e92d28d7a8fd7bd51fd8c9`,
  `books` `f17911100c20162400ddefac16f770f142815bffd13f4e9cfd238f86566b44a1`,
  `books_axis`
  `40f7047ba94f46cf4b588eca52a26922c3bd838593fb85644ad464f0fd285b0d`;
  192, 36 and 36 ticks; outcome: (b) reported, the numbers above, no clause;
  (a) pass, the one clause, the identity with the source line at every
  tick of both worlds and the plain statement; nothing tuned after the
  runs; `record.json` beside the worlds holds every row; the isolated test
  `tests/test_field_books.py` pins the worlds and the shell reader on a 9^3
  point source (expectations).

### E11 repeated under the law of the bit (2026-09-18)

- **Claim.** The first confrontation of the engine under the law of the bit
  (Highlights 5.4, the model owner's decisions of 2026-09-18; features 15 to
  18, 16d, 16e, 16f and the cleanup on `main` at `1a88785`) with round 4 of
  [DERIVATIONS](DERIVATIONS.md#26-round-4-the-node-mixes-the-six-as-an-operator)
  (sections 26 to 33) and round 6 (section 39), on one thing at rest and its
  field: the field is a standing set given with the GameBoard (points 11, 13, "A
  thing does not emit"), a shadow spreads by the Node's mixing (point 24),
  the return is a field (point 3), a thing reads the shadows' message by its
  content or its charge (point 16), there is one shadow set per thing and no
  field family (points 12, 18), a thing's clock is its content (point 19) and
  it pays a tick per whole quantum read (point 23). By the model owner's
  decisions of the same day the GameBoard of a run is closed and only closed
  worlds are tested (Highlights 5.4, "The GameBoard of a run is closed", PRs #311
  and #314): the series is made on a periodic GameBoard, where every shadow
  comes around and the field of a thing at rest is meant to be a steady
  circulation, read once settled. The predictions confronted, each answered
  below with its number: (i) no tubes, 89 % of a release off the coordinate
  planes at t = 30 (section 27 (ii)); (ii) the front at sqrt 3 r in every
  direction, sharp on (111) and smeared on the axes (27 (iii)); (iii) 1/r^2
  at every angle with a fixed first-order anisotropy of order (15/8) omega^2
  K_4 between an axis and (111) for a clocked source, and no far field for a
  clockless one (27 (v)); (iv) the wave surviving the integer rule above
  about 256 quanta per Node (section 30); (v) the third law exact through
  the field, the recoil arriving at the owner (sections 32 and 33); (vi) the
  books per bit balanced at every interval (point 7); and, new, (vii) the
  amplitude a thing reads, 0.5373 sqrt(G M) / r, the potential's 1/r
  (section 39). Nothing is registered as a law; what came out is recorded.
  The same evening, on this measurement (no fixed point on the closed GameBoard,
  the push without a law) and on the A6 lane's escape on the open GameBoard, the
  model owner reversed the rule the series was made under: a thing emits and
  nothing is given with the GameBoard, a shadow is never made to disappear, and
  the GameBoard of a run is open (Highlights 5.4, "A thing emits; nothing is
  given with the GameBoard", PR #319, superseding "A thing does not emit" and
  "only closed worlds are tested" of the same day); the series is repeated
  after feature 19, which implements the emission. What is recorded here is
  the engine under the rule of the afternoon, as run.
- **Features.** 15 (`bit-law-v1`), 16b (`clock-readings-v1`), 16c
  (`node-mixing-v1`), 16d (`return-field-v1`, parts 1 and 2: the returning
  shares in the dense layer), 16e and 16f present and not declared
  (`shadow_wait`, `wait_reads` absent: the wait and the push are point 23's),
  17 (`node-is-ports-v1`), 18 (`lanes-v1`), the cleanup (`cleanup-law-v1`:
  one `N` for the world), the dense mode (`dense-field-v1`), the standing-set
  search (`standing-field-v1`) and the series runner of `perf-arrays-v1`.
- **Run.** `examples/nature/e11_law/` (the worlds written by `make_worlds.py`,
  the dictionary in the
  README),
  every world on the law: `N` 64 declared once for the world, K 1,
  `wait_per_quantum` 1, the dense mode, no `spread`, `steering`,
  `mass_field`, `seed` or `field_of` key. The thing at rest is an external
  body of the catalog's `proton` family, amount 2^28, whole charge 3 x 2^28,
  at the centre of a 33^3 GameBoard; its shadow set is given with the GameBoard by
  `initial_field` `{"fill": 12}` with `release` [1, 512]: 2^19 per Port
  heading per interval of the fill, 6 x 2^19 x 12 = 37748736 quanta (the
  fill is 12 because the prefill admits no longer one: at 13 a third phase
  arrives back at the source on one Port and its two phase layers refuse it;
  the release amount keeps every read Node above 256 quanta while the train
  passes). The series, ten closed worlds of 120 ticks with `boundary`
  periodic and `standing_field` on (the runner's search for the shadow
  layer's fixed point or cycle, reporting the iterations to the repeat or
  the residual at the last comparison): `standing_closed.json`, the body
  alone, the field read shell by shell per tick by `analyze.py` in-process
  (the dense layer publishes no per-Node event; the replay is checked
  against the record tick by tick, the shadows on the GameBoard, the escapes,
  the body's momentum and the books; on a probe world the replay also reads
  the momentum on the shadows from the layer's momentum cells and the
  engine's Nodes, since the runner's ledger line of the momentum field does
  not sum the momentum carried on rays, and checks probe + shadows + body =
  0 at every tick); and nine probe worlds,
  `probe_axis_r{4,8,12}_closed`, `probe_110_m{3,6,9}_closed` ((m, m, 0), r =
  4.24, 8.49, 12.73) and `probe_111_m{2,5,7}_closed` ((m, m, m), r = 3.46,
  8.66, 12.12): the standing world with one test thing each, a real ray of
  the catalog's `electron` family of content 1 emitted by a lamp one Link
  outward of the read Node and heading inward, standing at the read Node
  after tick 1; its coupling `read` over [electron, proton] is the momentum
  table `{"proton": 1}` read by content, so every push is +amount x heading,
  the signed flux J of the body's shadows at its Node in quanta, and the
  thing's momentum line per tick (the runner's `momentum`) is the pushed
  amount itself; under point 23 a thing that reads thousands of quanta never
  moves again, so the test thing is a probe at rest (it waited 115 to 119 of
  its 119 read intervals in every world). It heads inward because under
  `return-field-v1` a share arriving through the Port the thing arrived by
  rides with it and pushes nothing (one meeting, one push): the ignored lane
  carries the wave's backward share. One probe per world, since every push
  returns as field. The settled push per direction is the probe's mean
  radial push per interval over the last twenty ticks (101 to 120), with its
  standard error and beside it every window of twenty and the settling tick
  (the first from which every later window of twenty stays within 10 % of
  the last); the 1/r^2 fit is the log-log least-squares slope over the three
  radii per direction and the anisotropy the axis fit over the (111) fit at
  r = 8 and 12. The amplitude at the test thing's Node is the size of the
  coherent sum of the shadows that arrived there in the interval, formed by
  `analyze.py` from the arrivals of the replay (the layer's arrays and the
  engine's Node) with the engine's own `arrival_amplitude` of wait-reads-v1,
  once per group (owner, sign, flow) and summed: |sum_p A_p| = 3 |u| of
  section 39, in quanta^(1/2); no world declares `wait_reads`, since the
  record carries no per-tick amplitude either way and the push is the same
  under both; the same sum is read at the same Nodes of the free field
  (`standing_closed`), and the wave fraction |sum A|^2 / (3 n) (1 for a pure
  wave, 0 for standing flat-band content, up to 2 for six arrivals in one
  phase) beside it. The records were made with `tools/run_series.py --jobs
  4` on a dedicated machine (4 cores, 16 GB; 479 to 1016 s per world, 2.5 GB
  peak each), the `run.json` of every world kept gzipped in `records/` beside the
  worlds, the readings in `record.json` and `tables.md`, the page in
  `e11_law.html`. Stated before the run: the prefill drops what reaches the
  lamp's Node during the fill, so the probe worlds whose lamp lies within
  the fill's train start with slightly fewer shadows (37733842 at r = 4,
  37716989 at (110) m = 3, 37514574 at (111) m = 2, 37748734 at r = 8, the
  full 37748736 elsewhere); the books open with the counted content. Before
  the decision that only closed worlds are tested, eight open-GameBoard worlds
  of 40 ticks (`pulse`, one release of 2^19 per heading on 41^3; `standing`;
  the three axis and the three (110) probes) were recorded on `main` at
  `ffa4a56` (features 15 to 18 and 16d part 1); they stand outside the
  series' reading and are kept as recorded, their numbers quoted below
  where a prediction was read only there (the front, the release off the
  planes) and in the tables' last section.
- **Result (the closed series).** Per prediction, whether the engine gave it,
  with the number. *(vi) The books:* given. Every ledger line per bit
  balanced at every tick of all ten worlds, `real_conserved` true
  throughout, nothing escaped, the shadow set constant to the quantum, and
  in the four probe worlds whose replay reads the momentum on the shadows
  (the three axis probes and (110) m = 3) the probe's momentum plus the
  momentum in flight on the shadows plus the body's is zero at every one of
  the 120 ticks (the other five probe worlds were replayed before that
  reading was added and not again, the lane stopping on the model owner's
  word; their amplitude rows stand, their momentum in flight is not read).
  *The standing set:* not reached. The runner's
  search found no fixed point and no cycle within 120 ticks in any of the
  ten worlds (the residual at the last comparison 46.6 to 47.0 M quanta
  moved over 622 k to 953 k array cells, out of 37.7 M on the GameBoard): the
  field of the thing at rest on the closed GameBoard is not a steady
  circulation within 120 ticks but a train that circles the GameBoard. In
  `standing_closed` the train leaves the body (the L1 shell k = 4: 40312
  quanta per Node at t = 1, 9140 at t = 10, 1684 at t = 20, 294 at t = 40),
  the GameBoard fills to a near-uniform haze by t = 40 to 60 (220 to 350 per
  Node at k = 4 to 16, 0.94 to 0.96 of the content off the coordinate
  planes, 0.3 % parked), and the train comes around the periodic GameBoard and
  reconverges at the body: the body's Node holds 395 quanta at t = 40,
  16429 at t = 80, 40922 at t = 84, 72786 at t = 92 and 44238 at t = 104,
  the k = 4 shell rises to 4390 per Node at t = 88, and the train leaves
  again (459 per Node at k = 4 at t = 120). The round trip of 33 Links at
  the derived front speed 1 / sqrt 3 is 57 intervals; the first reconvergence
  is spread over t = 72 to 116. The mean over ticks 101 to 120 differs from
  the mean over 81 to 100 by a factor 2 to 3 at every shell, and no read
  Node settled (no two consecutive windows of twenty within 10 %). *(i) No
  tubes:* given. The content off the coordinate planes is 0.83 at t = 5,
  0.87 at t = 20, 0.91 at t = 30, 0.94 at t = 40, 0.955 to 0.958 at t = 50
  to 60, 0.80 to 0.89 during the reconvergence (mean of the last twenty
  0.86), on the axes below 1 % from t = 5; the release measured earlier on
  the open GameBoard (`pulse`) had 0.891 off the planes at t = 30 against the
  derivation's 0.890. *(ii) The front at sqrt 3 r:* given, read on the open
  GameBoard earlier (on the closed GameBoard the first passage is the same until the
  train reaches the boundary at about t = 28): the pulse's content at the
  read Nodes peaks at ticks 7, 16, 22 on (111) (sqrt 3 r = 6.0, 15.0, 21.0),
  9, 19, 29 on (110) (7.3, 14.7, 22.0) and 9, 29, 37 on the axis (6.9, 13.9,
  20.8): on time and sharp on the body diagonal, 2 to 7 intervals late on
  (110), 2 to 16 late and smeared on the axis, with the axis peak 30 times
  below the (111) peak at r = 12 (241 against 7786), as section 27 (iii)
  derives. *(iii) 1/r^2 at every angle:* not given. The settled push per
  interval (ticks 101 to 120, +- its standard error) is 637 +- 588, 1155 +-
  685 and 1846 +- 621 on the axis at r = 4, 8, 12 (log-log slope +0.96 +-
  0.08), 1064 +- 542, 409 +- 883 and 453 +- 252 on (110) at r = 4.24, 8.49,
  12.73 (-0.84 +- 0.43), 444 +- 827, 562 +- 403 and 319 +- 219 on (111) at
  r = 3.46, 8.66, 12.12 (-0.15 +- 0.41); the window 81 to 100 gives 1916,
  1344, 1939 on the axis (-0.05 +- 0.37), 1348, 223, -123 on (110), -341,
  267, 317 on (111); the anisotropy axis / (111) of the settled push is 2.87
  at r = 8 and 4.51 at r = 12 (5.6 and 5.7 of the window 81 to 100), against
  the derived 1 - 1.25 omega^2 = 1 for this source (omega = 0: the body has
  no clock); the push changes sign every two to three intervals (36 to 66
  sign changes in 119 intervals; single intervals of +-10000 around means
  of hundreds), the probe reading the train as it passes outward and,
  after the round trip, inward, and its own returned shares. What the probe
  reads is not a far field but the circling train; the derivation's clause
  that a clockless source has no far field is not contradicted, and its
  1/r^2 for a clocked source was not put to the test (no world of the series
  has a clocked source). *(iv) The wave above 256 quanta per Node:* given
  where read. The wave came around the GameBoard and reconverged at the body
  (above) with 220 to 3000 quanta per Node on the way, and the wave fraction
  |sum A|^2 / (3 n) at the free read Nodes is 0.77 to 1.67 over the last
  twenty ticks (a pure wave 1, standing content 0) and 0.9 to 2.8 at the
  probes' Nodes: the field the probes read is a wave, not parked residue
  (0.3 % parked at t = 120). *(v) The third law through the field:* the
  books exact (above); the recoil arriving at the owner, not within 120
  ticks beyond a few per cent: of the probe's cumulative push the body's
  momentum at tick 120 is 2.0 %, 0.3 % and 0.1 % on the axis at r = 4, 8,
  12 (-3284 of 167837, -257 of 76386, -58 of 93060), 4.2 %, 1.1 % and 0.3 %
  on (110), 17.3 %, 4.2 % and 1.5 % on (111) (-29934, -30205, -32802 of
  310224 at (2, 2, 2)); the rest is in flight on the shadows, which do not
  find the owner in one round trip (read at tick 120 on the four replayed
  worlds: -164553, -76129, -93002 on the axis and -212166 on x at (110)
  m = 3, the probe's push with the opposite sign less the body's). *(vii) The amplitude 1/r:* given at the
  probe's Node, not in the free field. At the test thing's Node the size of
  the coherent sum over ticks 101 to 120 is 264, 172, 103 quanta^(1/2) on
  the axis at r = 4, 8, 12 (slope -0.83 +- 0.17), 214, 192, 85 on (110)
  (-0.77 +- 0.49), 393, 53, 127 on (111) (-1.17 +- 1.01; the window 81 to
  100: 259, 191, 143; 192, 91, 73; 346, 99, 94), the anisotropy axis / (111)
  1.28 at r = 8; at the same Nodes of the free field (`standing_closed`, the
  probe absent) it is 86, 73, 97 on the axis (+0.07 +- 0.24), 63, 86, 84 on
  (110) (+0.28 +- 0.12), 47, 55, 127 on (111) (+0.66 +- 0.49): flat, as the
  count there is flat (2603, 3038, 3059 per Node on the axis). The 1/r at
  the probe's Node comes with a count that exceeds the free field's by 5.5,
  4.1 and 0.85 at r = 4, 8, 12 (14200, 12360, 2589 quanta arriving per
  interval): the probe returns every share it reads, a point mirror, and
  piles the field near itself the more the nearer it stands to the body's
  reconvergence; the amplitude read is that pile's square root, not the
  free field's potential, and the derived 0.5373 sqrt(G M) / r (a clocked
  source's far field) was not put to the test. *Cost.* 479 s (`standing_closed`)
  and 550 to 1016 s per probe world, four at a time, 2.5 GB peak each; the
  replays 182 to 569 s.
- **Result (the open GameBoard, measured earlier, outside the series).** Eight
  worlds on `main` at `ffa4a56`, 40 ticks: the books balanced at every tick;
  the set falls from 37748736 to 19372497 by tick 40 (18376239 escaped); the
  cumulative radial push at tick 40 on the axis 115328, 17204, 6572 (slope
  -2.62 +- 0.10) and on (110) 235703, 69914, 15481 (-2.40 +- 0.52), the axis
  0.315 of the (110) fit at r = 8; the inventory's J at the nine Nodes of
  `standing` over ticks 2 to 21 has slopes -2.95, -2.03, -1.25 (axis, (110),
  (111)) and the axis reads 0.10 of (111) at r = 8; the recoil home by tick
  40: 1.4 % at r = 4, 3.5 % and 0.8 % at (110) r = 4.24 and 8.49, nothing at
  r >= 8 on the axis; the (111) probes were never run.
- **Reading.** On the closed GameBoard the engine gives, within 120 ticks, no
  standing set and no steady circulation: the prefilled field of a thing at
  rest is a wave train that circles the periodic GameBoard at about 1 / sqrt 3
  Link per interval, thins to a haze and reconverges at its owner once per
  round trip, and the search for a fixed point or a cycle finds none. What a
  test thing at rest reads is that train, outward and then inward, with the
  sign alternating every few intervals and a twenty-interval mean as large
  at r = 12 as at r = 4 on the axis: 1/r^2 is not read, at any angle, and
  the field of this clockless source has no far field to read, as section 27
  (v) derives; the wave itself survives the integer rule and a round trip.
  The books per bit close at every interval and the third law holds exactly
  in the books, the recoil in flight on the shadows and at the owner only by
  a few per cent within one round trip. The amplitude falls as 1/r at the
  probe's Node and not in the free field: it is the probe's own mirror. The
  predictions that need a clocked source (1/r^2 with the fixed anisotropy,
  the amplitude 0.5373 sqrt(G M) / r) were not confronted by this series,
  whose source has no clock; whether the circulation settles over several
  round trips is beyond 120 ticks.
- **Fingerprint.** The series: source
  `051d716825c4785baffba01e46ea7348698fdfe82ca9ddc70eafab9871a49be5` (the
  package of `main` at `1a88785` merged into the branch: features 15 to 18,
  16d parts 1 and 2, 16e, 16f, `cleanup-law-v1`; no engine change on the
  branch), the initializations in `examples/nature/e11_law/records/*_closed.json.gz`
  (the `run.json` of every world, `initialization_sha256` inside each;
  `standing_closed`
  `872d63acd3178537f31b577b40aed15e7185d36b62aa59637210ed91fcf568da`), the
  worlds the files beside them at this commit less the family key
  `ray_slots`, which `main` retired with the lanes after the runs (PR #315)
  and the engine now refuses: the shipped worlds drop it, their textual
  fingerprint changing and their physics not. The open GameBoard, earlier:
  source `6fef7cc04a71706cfd5dfdb496e20f6318a6bdfd6bf0c36e1379dbdd7934addc`
  (`main` at `ffa4a56`), `records/{pulse,standing,probe_axis_*,probe_110_*}.json.gz`,
  whose worlds carried the per-family `phase_bits` 6 that the migration to
  the world key `N` rewrites (the physics unchanged).
- **Status.** measured on 2026-09-18 for the ten closed worlds at the
  fingerprint above (and, earlier the same day, for eight open worlds at
  theirs); recorded here; superseded the same evening by the model owner's
  decision that a thing emits and the GameBoard is open (PR #319): to be
  repeated after feature 19. Nothing is registered as a law.

### E12. The screen without a draw: a counter against a drawn mark, and interference in counts

- **Claim.** The model owner's question of 2026-09-18: does the model need
  the Detector's draw at all? The screens E6 and E9 ran with the marks at
  setting [1, 1], no draw refused, and all seven marks clicked with counts
  proportional to the intensity (27, 6, 6, 3, 3, 1, 1 in E6; 17, 4, 4, 1, 1,
  1, 1 in E9), the order of the clicks coming from the remainder registers
  deterministically; so perhaps a Detector is a counter, every whole quantum
  that arrives absorbed and counted (Highlights 5.4, "A click is an
  absorption", 2026-09-18), and the draw of 3.19 ("the only lottery in the
  model") is a declarable option, a mark with an efficiency below 1. Two
  numerical questions: (1) is a counter's count the mean-field intensity at
  its Node, mark by mark, and does a drawn mark give the same pattern scaled
  by its setting, with nothing in the record needing the draw (the order of
  the clicks the same on a rerun and under another ticket seed); (2) does
  interference of light show in the counts of a counter under the spread
  alone (the coherent sum of 3.5 and 3.20 setting the phase of the combined
  content), or only under the steering coupling of 3.3 (`born_steering`
  declared over `[light, light]`).
- **Features.** 1, 2, 2b, 3, 5, 6, 7, 7b, 9, 10, 12, 12b, 14; and 2c
  (`detector-absorb-v1`, a click is an absorption) when it is on the base the
  runs are made on, which the Status says.
- **Run.** `examples/nature/e12_no_draw/` (written by `make_worlds.py`),
  eight worlds. Part 1, a counter against a drawn mark: E9's world (the ring
  of E5 with rays of amount 4, content 32, at the catalog's rate 1 on the
  unit square P0 = (1,5,5), P1 = (2,5,5), P2 = (2,5,6), P3 = (1,5,6) in the
  plane y = 5, `light` `field_of` electron with `release` [1, 4] and `spread`
  [6, 1, 1, 1, 1, 1], N = 8, seven marks at (7, 2, 5) to (7, 8, 5), GameBoard
  12 x 11 x 11 open, 240 ticks) with the marks at setting [1, 1]
  (`screen_d1`, a counter), [1, 2] (`screen_d2`) and [1, 4] (`screen_d4`, a
  draw per arrival, the refused quanta returned on their lines), and the
  counter with ticket seed 7 at every mark (`screen_d1_seed7`); `screen_d1`
  is run twice, the second record kept as `screen_d1_rerun`. All five in the
  engine (no dense mode), so that the recording of `record_sidecar.py` can be
  made where the returned quanta are to be followed. Part 2, interference in
  counts: two external bodies of one `proton` family (charge +3, amount 256)
  at (1, 4, 4) and (1, 12, 4), 8 Links apart on the y axis, radiating one
  `light` family (`field_of` proton, `release` [1, 4]: 64 quanta per heading
  per interval each, `spread` [6, 1, 1, 1, 1, 1], N = 8, `source_sign` +1
  set by the engine from the charge), on a line of fifteen counters at
  (12, y, 4), y = 1 to 15, GameBoard 16 x 17 x 9 open (the plan's y = 0 to 14
  shifted by one, so that the world is symmetric under y -> 16 - y and no
  mark lies on a face); `two_inphase` (both bodies at phase 0) and
  `two_antiphase` (the second at phase 4, half the circle), 240 ticks in the
  dense mode (`dense-field-v1`: the clicks and the ledger are the engine's
  byte for byte, the performance record), and the same two worlds in the
  engine for 96 ticks (`two_inphase_e96`, `two_antiphase_e96`) for the
  recording and the viewer document, whose clicks must be the first 96
  ticks of the dense record's; `two_inphase_steer` and `two_antiphase_steer`,
  the same two worlds with the catalog's `born_steering` declared over
  `[light, light]` (the table [8, 7, 4, 1, 0, 1, 4, 7] between +Y and -Y),
  96 ticks in the engine, since the dense mode does not admit a coupling on
  field rays and the engine costs about 1.3 s per tick once the field fills
  this GameBoard (62 s for a 48-tick probe made before the runs), read against
  the plain worlds' first 96 ticks. Recorded per world: `run.json`,
  `events.jsonl`; for `screen_d1`, `screen_d1_rerun`, `screen_d2`,
  `screen_d4`, the two `_e96` worlds and the two steering worlds the
  recording and the extractor's `runs.json` (`--ticks 96`), kept outside the
  tree, no GIF; `analyze.py` prints the readings and writes `record.json`;
  `mean_field.py` writes `predictions.json`, the computation below. The
  dictionary and the readings are in the
  README;
  `tests/test_screen_no_draw.py` pins the smallest world of the question
  (expectations).
- **Computed (before the run).** (i) The mean field, `mean_field.py`: the
  split table as the linear map it is on average (A5s Run 2 measured the
  engine's integers against it to a part in a thousand at 4096 per heading),
  stepped on E9's open GameBoard with the ring's four corners releasing per
  interval from the cycle of tick 1 what E9's README computes (P1 sends 2 on
  +X along the axis, 1 on -X and +Z along the edges, 2 on the other three;
  the corners ordinary Nodes for light, spreading what reaches them), the
  seven marks absorbing whatever arrives (2c). The arrivals per interval at
  the steady state: 0.5817 at (7, 5, 5), 0.2742 at (7, 4, 5) and (7, 6, 5),
  0.2085 at (7, 3, 5) and (7, 7, 5), 0.1700 at (7, 2, 5) and (7, 8, 5), the
  first mean-field arrival at ticks 6, 7, 8, 9 from the axis outward;
  integrated over 240 ticks, the counter's predicted count in quanta:
  132.6, 60.8, 60.8, 45.8, 45.8, 36.9, 36.9 (378.6 in all), the pattern
  2.18 : 1 : 0.75 : 0.61 from the axis outward, flatter than E6's and E9's
  counts because the marks absorb what they count and the mean field has
  no register waiting. With the marks transparent (the clicked quantum
  spreading on, the rule before 2c) the same numbers are 193.6, 118.2,
  118.2, 92.9, 92.9, 70.0, 70.0. A drawn mark at [1, d] is the same sink
  for the spreading field (a returned quantum walks back on its line and is
  not spread), so its expected count is 1 / d of the counter's: 66.3, 30.4,
  30.4, 22.9, 22.9, 18.5, 18.5 at [1, 2] and 33.2, 15.2, 15.2, 11.4, 11.4,
  9.2, 9.2 at [1, 4], with the binomial noise of a draw per arriving ray.
  The engine's integers lag the mean field: a whole quantum leaves a Node
  only when its register reaches eleven (E9's first click was at tick 11
  against the mean field's tick 6), so the transient is slower and the
  240-tick totals are expected below the mean field's, the more so at the
  weaker marks; the claim confronted is the proportionality mark by mark,
  read as the spread of the ratio count / prediction over the seven marks.
  (ii) The draw at setting [1, 1] (`ticket_bit`,
  `src/event_universe/core/spatial_state.py`): the bit is 1 when the drawn
  number times the denominator is below the numerator times the ticket
  modulus, and every drawn number is below the modulus, so at [1, 1] the bit
  is 1 whatever the number; the mark's ticket stream still advances once
  per drawn arrival (a ticket is consumed, one per click or return, none
  for a pass of a ray that carries a bit), and the outcome reads nothing of
  it. Predicted: `screen_d1_seed7` and `screen_d1_rerun` give the counter's
  record event for event (the `events.jsonl` digests equal; the
  initialization digest of the seed-7 world differs by the seed alone), and
  the tickets consumed per tick at every mark equal its drawn arrivals, the
  B2 line, with no draw anywhere else (no decaying rule). (iii) The returns
  at [1, 2] and [1, 4]: a returned field quantum reverses on the line it
  arrived by and walks back until it is absorbed by the first content its
  coupling responds to or reaches its source, with no inverse split (the
  proposal of Highlights 5.5 that feature 12 implements); the light is the
  electron's field, so a return that reaches a ring corner, where electron
  rays are resident in every interval, ends there with its release unbooked
  (`field_returned` with `by` electron, a negative step of the light line's
  `sourced`); the ring's content is untouched, since the unbooking is the
  field's line and not the electron's. Only the on-axis mark's arrivals
  through its -X face walk back along the axis line y = 5, z = 5 into P1;
  every other line of arrival (the -X lines at y != 5, the +-Y lines along
  the screen, the +-Z lines) misses the ring, and a returning ray crosses
  the marks on its way undrawn, so those returns escape at the open boundary
  or are still walking at tick 240. (iv) Part 2, from the code: the content
  arriving at a Node combines by phase before it spreads, and the
  combination sets the phase of the whole (`phase_of_sum`, the step nearest
  the coherent sum; for amounts a at phase 0 and b at phase 4 it is 0 when
  a > b, 4 when b > a, 0 on a tie) and never its amount (`spread_content`
  adds the amounts per arriving heading and sign; "the coherence of the
  arrivals is recorded and never applied to the amount"), so a counter's
  counts in phase and in antiphase are predicted identical, click for
  click, and equal to the mean field of the two sources: with the bodies
  and the fifteen marks absorbing, the arrivals per interval at the steady
  state 0.617 at the marks facing the sources (y = 4 and 12), 0.452 at the
  middle (y = 8), 0.258 at the ends (y = 1 and 15), integrated over 240
  ticks 131.3, 100.6, 95.8, 92.5, 91.4 from y = 4 inward and 86.9, 68.0,
  53.0 outward (1347.5 in all), the first mean-field arrival at tick 11 at
  y = 4 and 12 and tick 15 at y = 8; symmetric under y -> 16 - y. The
  phase difference the geometry gives a mark is r x dL mod N for an emitter
  of rate r and the path difference dL: a body's release carries its
  declared phase and light's rate is 0 (Highlights 3.3: the frequency of
  light is its emitter's rate), so r = 0, the fringe period N / r is
  infinite, and the only phase difference on the screen is the declared
  one, 0 in phase and 4 in antiphase, at every mark; the path differences
  are in `predictions.json` for the record (Euclidean 0 at y = 8 to 4.16
  Links at the ends, GameBoard 0 to 8), and no alternation of the counts
  along y can come from the geometry in either world. Under the coupling:
  the layers become `[["light"], ["proton"]]` with a rule in light's layer
  (the body's family has no rays and no rule), so the sources' own light
  meets itself at every Node where two light rays are resident, the pairs
  taken in slot order (`participant_groups`) and the odd ray crossing; each
  meeting takes the two rays' sum and sends it through +Y at phase
  difference 0 (table[0] = 8) and through -Y at 4 (table[4] = 0), whatever
  the headings the rays arrived on, as fresh event rays that spread from
  the next Node. In phase every meeting is at difference 0 (all light at
  phase 0), so the coupling turns the field toward +Y everywhere; in
  antiphase a meeting of one source's light with itself is at 0 and of the
  two sources' light at 4, so the field is turned toward +Y where one
  source dominates and toward -Y where they mix, the registers' releases
  carrying 0 or 4 by the rule above. Predicted therefore: the counts change
  under the coupling and differ between the two phase worlds, the mirror
  symmetry y -> 16 - y broken toward +Y in phase, with no fringe of the
  geometric kind (its period is infinite); the numbers are the run's to
  give, and the 24-tick probe made to admit the world already showed the
  light line differing (absorbed by the bodies 3627 against 2406 without
  the coupling at tick 24).
- **Criterion (written before the run).** Part 1, pass, all of: (1) every
  ledger line balanced at every completed tick and
  `conserved_at_every_completed_tick` true in every record, the electron
  line 32 with no source, escape, annulment or absorption at every tick;
  (2) the counter clicks at all seven marks within 240 ticks, the pairs
  (7, 4, 5) and (7, 6, 5), (7, 3, 5) and (7, 7, 5), (7, 2, 5) and (7, 8, 5)
  with equal counts tick for tick and the on-axis mark with the most, and
  under 2c every click is an absorption (no `detector_pass`, the light
  line's `absorbed_by_marks` equal to the quanta clicked and the marks'
  counters the quanta per mark); (3) the counter's record
  is reproduced event for event by the rerun and by the seed-7 world, and
  every mark's tickets consumed equal its clicks plus its returns at every
  tick; (4) proportionality: the counter's quanta per mark against the
  mean field's 240-tick integral (marks absorbing) have a ratio whose
  largest over smallest across the seven marks is below 2, so that the
  pattern is the intensity's up to one factor and the integer lag; (5) the
  drawn marks: the quanta per mark at [1, 2] and [1, 4] within the binomial
  noise of the counter's over d (|n_d - n_1 / d| at most 2 sqrt(n_1 / d) + 1
  at every mark), every returned quantum accounted for (returned = ended by
  `field_returned` + escaped or still walking, the ledger exact), and the
  only returns that end at the ring those of the on-axis mark. Part 2,
  pass: (6) `two_inphase` and `two_antiphase` give the same clicks, click
  for click, and the same ledger, both mirror symmetric under y -> 16 - y,
  and the `_e96` engine records are the first 96 ticks of the dense records'
  clicks; (7) the steering worlds run to completion (the world admitted,
  no slot budget exceeded), their counts read: whether they differ from the
  plain worlds' first 96 ticks and between the two phases, and whether a
  fringe appears, read as sign changes of the counts along y beyond the
  two maxima the sources face (predicted: none of the geometric kind, the
  period being infinite; a difference between the phases, yes). A failure
  of (7) to admit the world is itself the finding of the coupling question.
  Fail: any clause of (1) to (6), stated as which and why. The runs are made
  once; nothing is tuned after them, and if the first look forces a change,
  both records are kept and said so.
- **Shows.** Run once each on 2026-09-18, on the engine of feature 2c (the
  merge of PR #257, engine commit `10edd1dd`, source
  `2578f911f59a3883031b3ccf1d83f871569df8b217662c20f652d8fcb6823f52`, the same engine as
  E9's repeat), the marks on the `on_click` default of a field family.
  Part 1, the counter (`screen_d1`, 240 ticks, 74 s): 265 clicks,
  every one of family `light`, amount 1, bit 1 and `absorbed` 1, no pass and
  no return, the counters 109 at (7, 5, 5), 38 at (7, 4, 5) and (7, 6, 5),
  25 at (7, 3, 5) and (7, 7, 5), 15 at (7, 2, 5) and (7, 8, 5), E9's repeat
  under 2c to the click; the first click of each mark at ticks 11, 34, 34,
  50, 50, 70, 70; the count growing through the run, 4, 14, 24, 19, 29, 34,
  33, 32, 42, 34 clicks in the ten 24-tick windows over the screen, and in
  the last 96 ticks 51, 21, 21, 14, 14, 10, 10; the marks' momentum (218, 0,
  -27); light sourced 9560, current 3489 (still growing, the registers
  filling), escaped 5806, absorbed by marks 265; electron 32 at every tick,
  momentum (0, 0, 0), every line balanced, `conserved_at_every_completed_tick`
  true. Against the mean field with the marks absorbing (the 240-tick
  integral 132.6, 60.8, 60.8, 45.8, 45.8, 36.9, 36.9, whose sum is 419.7,
  misadded as 378.6 in the Computed item above; the per-mark numbers stand):
  the ratio count / prediction is 0.82, 0.62, 0.62, 0.55, 0.55, 0.41, 0.41
  (mean 0.57, largest over smallest 2.02), falling outward; over the last 96
  ticks against 96 x the steady arrivals (55.8, 26.3, 26.3, 20.0, 20.0, 16.3,
  16.3) it is 0.91, 0.80, 0.80, 0.70, 0.70, 0.61, 0.61 (largest over smallest
  1.49). The counter's pattern 109 : 38 : 25 : 15 = 1 : 0.35 : 0.23 : 0.14
  is steeper than the mean field's 1 : 0.46 : 0.35 : 0.28, the shortfall
  growing outward, and it flattens toward the mean field as the registers
  fill; against the transparent mean field (193.6, 118.2, 92.9, 70.0) the
  ratio is 0.31, so a counter is the absorbing sink the computation took it
  for. The drawn marks: `screen_d2` (82 s) 139 clicks, 55, 20, 20,
  13, 13, 9, 9, with 54, 18, 18, 12, 12, 6, 6 returns (126 quanta);
  `screen_d4` (83 s) 65 clicks, 25, 9, 9, 6, 6, 5, 5, with 84, 29, 29,
  19, 19, 10, 10 returns (200 quanta). In both, the drawn arrivals (clicks
  plus returns) at every mark and every tick are exactly the counter's
  clicks, 109, 38, 38, 25, 25, 15, 15, tick for tick: the draw partitions
  the same arrivals and changes nothing before the mark. Against the
  counter over d the ratio is 1.01 to 1.20 at [1, 2] (mean 1.09) and 0.92 to
  1.33 at [1, 4] (mean 1.06), every mark within the binomial clause
  (|n_d - n_1 / d| at most 2 sqrt(n_1 / d) + 1: the largest deviation 1.5
  against 6.5 at [1, 2], 2.25 against 11.4 at [1, 4]). The returned quanta:
  at [1, 2] 44 ended at the ring corner P1 = (2, 5, 5) (`field_returned`
  with `by` electron, walked back along the axis line from the on-axis
  mark's -X face, its release unbooked: light sourced 9516 = 9560 - 44, no
  `restored`), 74 escaped at the open boundary and 8 were still walking at
  tick 240 (the recording); at [1, 4] 67 at P1 (sourced 9493), 121 escaped,
  12 walking; the on-axis mark's returns through its -X face 45 and 70, through
  +Z 6 and 10, through -Z 3 and 4, and no return of another mark reached the
  ring, as computed; the ring's electron line 32 with no source, escape,
  annulment or absorption at every tick in both; light current 3497 and
  3501, escaped 5880 and 5927, absorbed by marks 139 and 65; the marks'
  momentum (117, 0, -12) and (54, 0, -7); every line balanced, conserved
  true. Determinism: `screen_d1_rerun` (73 s) and `screen_d1_seed7`
  (78 s, every mark's seed 7) give the counter's record event for event
  (`events.jsonl` digests identical with and without the host's `cost`, the
  ledger identical at every tick, the same 265 clicks in the same order),
  the seed-7 world's initialization digest differing by the seed alone. The
  tickets: one per drawn arrival, so at [1, 1] every mark's tickets equal
  its clicks at every tick (109, 38, 38, 25, 25, 15, 15 in all), at [1, 2]
  and [1, 4] its clicks plus returns, the same numbers; a pass consumes
  none and none occurred; no other Node draws. Part 2, the plain worlds in
  the dense mode (`two_inphase` 7 s, `two_antiphase` 7 s, 240
  ticks): the two records are identical click for click and in every
  ledger line, as computed from the code: 963 clicks carrying 969 quanta
  (six of amount 2), per counter from y = 1 to 15: 33, 46, 62, 104, 74, 68,
  65, 65, 65, 68, 74, 104, 62, 46, 33, mirror symmetric under y -> 16 - y,
  two maxima at the marks facing the sources and nothing else along y; the
  first clicks at ticks 19 (y = 4 and 12), 49 (y = 8) and 57 (the ends);
  2, 26, 55, 77, 118, 123, 130, 148, 142, 148 quanta in the ten 24-tick
  windows; the marks' momentum (697, 0, 0); light sourced 184320, current
  15961, escaped 139496, absorbed by the bodies 27894 (13947 each), absorbed
  by marks 969; the proton line 0; every line balanced, conserved true.
  Against the mean field (53.0, 68.0, 86.9, 131.3, 100.6, 95.8, 92.5, 91.4
  and the mirror) the ratio is 0.71 (0.62 to 0.79). The engine records of
  the same worlds for 96 ticks (`two_inphase_e96` 137 s, `two_antiphase_e96`
  137 s) are the first 96 ticks of the dense records click for click, 160
  quanta each (4, 7, 10, 24, 12, 10, 9, 8, 9, 10, 12, 24, 10, 7, 4). The
  steering worlds (`born_steering` over `[light, light]`, 96 ticks in the
  engine, `two_inphase_steer` 38 s, `two_antiphase_steer` 48 s): admitted,
  `ray_layer_families` `[["light"], ["proton"]]`, run to completion with no
  slot budget exceeded, and NO click at any counter in either world. The
  coupling takes every pair of light rays resident at a Node and sends
  their sum through +Y at phase difference 0 or -Y at 4, so the sources'
  own field, which arrives at every Node on several headings, meets itself
  everywhere and is turned off its way at once: in phase (every meeting at
  difference 0) light escaped 48152 of 73728 sourced, 43140 of it through
  the +Y face, 165 through -Y, 3910 through -X and 937 through +-Z, the
  bodies' sinks took 17141 and 8435 was in the world; the spreads reach
  x = 11 once and x = 12 never, so the screen is dark. In antiphase (a
  meeting of the two sources' light at difference 4, of one source's with
  itself at 0; the spreads' phases 0 and 4 only) light escaped 41244, 25527
  through +Y and 9038 through -Y, 5498 through -X, the sinks took 17422,
  11070 at the phase-0 body and 6352 at the phase-4 body, 15062 in the
  world, again nothing at x = 12. Without the coupling the same 96 ticks
  gave 160 quanta on the screen. So the counts change under the coupling,
  from 160 to 0 in both phases, the two phases differ in where the field
  goes (the +Y face, or +Y and -Y and the two sinks unequally) and not in
  what the screen counts, and no fringe appears: none of the geometric kind
  was possible (the period is infinite), and the coupling declared over one
  family at every meeting does not confront two paths at the screen but
  deflects the whole field before it gets there. The viewer documents
  (`runs.json`, 96 ticks) of the counter, the two plain 96-tick records and
  the two steering records read the meetings of the field with itself
  from the recording; their counts are in `record.json`.
- **Status.** measured, 2026-09-18, the runs at commit `dbfe7ed` of this
  branch (the engine that of commit `10edd1dd`, source
  `2578f911f59a3883031b3ccf1d83f871569df8b217662c20f652d8fcb6823f52`, feature 2c on
  main since PR #257); initialization digests `screen_d1` and
  `screen_d1_rerun` `64ad573029635e459460e468fe8824963fb2ed2b13d1926d38e34b39ddac8e27`, `screen_d1_seed7`
  `3e371b9695d7b692b09b07accf34987f94d3823325b1e60751189736101ad5ae`, `screen_d2`
  `7dccc7eec7965409cd5130daeb096241252604a947c7ff678360c3855e97108e`, `screen_d4`
  `c6cdbe0859cf92435fc56891e3895d2feaa8c0d6c7a840e4a5e5f1aeff9f6efe`, `two_inphase` (and `_e96`, `_steer`
  by its own file) `4191a92269a2ac0aebf8796402543f46586b5b7259dba0083696c6359003f52d`, `two_antiphase`
  `5829f8eae83dcf00dacbf937a3bb9fdad9a4b827413bf219e3c49f36e77c732a`, `two_inphase_steer`
  `1529fa8016cbacd178803d0ede6a3740993c26163f89bc3d8b8915e77d214401`, `two_antiphase_steer`
  `034f6574988cf986adb7a6a68e978d40387cd1c980b826b33f3c9ae588c0ce49`; `record.json` beside the worlds
  holds every reading, the records stay outside the tree. Outcome: Part 1
  clauses (1), (2), (3) and (5) pass; clause (4) fails as written, the
  largest over smallest ratio being 2.02 over 240 ticks (1.49 over the last
  96), stated as such: the counter's counts are the intensity's pattern up
  to the integer field's lag, which is larger at the weaker marks and
  shrinks as the registers fill, and not a proportionality at one factor
  within 240 ticks. Part 2: clause (6) passes; clause (7) read: the worlds
  admitted and completed, the counts 0 in both phases against 160 without
  the coupling, no fringe. Deviations from the plan, all stated before the
  runs: the counters at y = 1 to 15 and the sources at y = 4 and 12 (the
  plan's y = 0 to 14 shifted by one), the steering worlds 96 ticks in the
  engine, the plain Part 2 worlds in the dense mode with their first 96
  ticks repeated in the engine; and the sum 378.6 in the Computed item,
  corrected to 419.7 above. Nothing was tuned after the runs. The plain
  answer for the model owner: nothing in these runs needs a draw. A counter
  reproduces by itself everything the screens showed, the whole screen lit
  in the intensity's order with the count growing as an intensity, the
  order of its clicks fixed by the remainder registers and the same on a
  rerun and under another seed; a drawn mark sees exactly the same arrivals
  at the same ticks and keeps a declared share of them, so the draw's only
  work is the efficiency below 1 (and the return it sends back, which
  mostly escapes and partly reaches the source and unbooks its release);
  the lottery of 3.19 is consumed at [1, 1] and decides nothing. What the
  counter does not give is interference: two sources in phase and in
  antiphase count the same, since the coherent sum sets a phase and never
  an amount, and the steering coupling of 3.3, declared over light meeting
  light, does not make fringes on this screen but turns the whole field
  away before it arrives; A1's fringes need a meeting of two paths at the
  screen and not of the field with itself at every Node, which is a point
  for the model owner on where `born_steering` may be declared.

### E7. The string: gluon loops between two quarks (after feature 14)

- **Claim.** Highlights 3.26 in the language of binding as a loop (3.4,
  model owner, 2026-09-17): the strong field differs from light by one
  catalog line, its rays couple to each other (`gluon_gluon_binding`), so
  the field between two quarks closes into loops of gluon rays along the
  line between them, a string whose content, and so whose mass, grows with
  the distance; only colour-neutral patterns close a loop, confinement as a
  closure condition, and a string stretched to the content at which a new
  loop closes with a quark and an antiquark breaks into two hadrons,
  hadronization. Nothing is inserted: hypothesis 13 says whether the two
  catalog lines produce it.
- **Features.** 1, 5, 6, 9, 10, 12, 14, with the quark families, colour and
  the couplings `quark_binding` and `gluon_gluon_binding` as declared tables
  (catalog work after feature 10, hypothesis 13).
- **Run.** Two quark rays of declared colours at a declared separation on a
  small open GameBoard, their gluon field released and spreading by its family's
  table, the field-to-field table declared before the run; the content held
  between them read against the separation d = 2, 4, 8 and 16 Links; the
  pull, one quark stepped away one Link per k intervals until the held
  content reaches the content at which a new loop closes; the control, two
  charges with light in place of the gluon under `electron_field_turn`.
- **Shows (to be pinned before the run).** The content between the quarks
  growing with d while the field off the line falls to nothing beyond a
  declared distance, a string, against the control's 1/r; the loop closing
  for colour-neutral pairs only; the string breaking into two colour-neutral
  groups at the declared content, no quark ray alone on a straight line at
  any tick; every ledger line exact.
- **Status.** planned, hypothesis 13, after feature 14 (binding as a loop)
  and the strong catalog entries; its outcomes are those of hypothesis 13:
  the content grows and no lone quark appears, or it falls off as for a
  charge, or the pattern does not close.

### E13. A shared physical detector retains incoming phase

- **Scope and authority.** The model owner's detector implementation and small
  GameBoard request, 2026-09-19; issue #342. The opt-in
  [reversible-detector-v1 contract](DETECTOR_REQUIREMENTS.md) supplies the
  local contact and finite physical pointer. This is a demonstration of that
  candidate, separate from the historical ray-event catalog features above.
- **Frozen setup.** `examples/events/detector/shared_3_nodes.json`: open
  9-by-9-by-1 world; three material Nodes at x=3,4,5, y=4, z=0; one shared
  output at x=5. One +X carrier starts at x=2. Two preparations differ only
  in carrier phase, 0 or 16 of N=32. K=1024, local reference 0, threshold 1,
  capacity 31, four intervals each. No law, calibration or threshold is fitted.
- **Acceptance fixed before execution.** Output values at ticks 0 through 4
  are exactly 0,0,0,0,1 for both preparations; the complete live physical
  states remain different at all five times; total amount is 4, total
  material-plus-transit momentum is (1,0,0), and nothing escapes throughout.
- **Status.** Measured, pass within this scope, 2026-09-19 10:01 UTC, source
  commit `17dd34c0f8d54b045ab0e4ff9c28e0399dfe6911`, fingerprint
  `5d4d2dcf360f8a0f8375977e151b451b64d42fa76ff163ad5561887d6c57b84b`.
  Each case was run once through the active engine. Exact outcomes, input
  digests, checks and display verification are recorded in
  [the validation entry](VALIDATION.md#reversible-detector-a-shared-output-retains-incoming-phase---2026-09-19).
  The saved report is `universe24_physical_detector_9x9.html`, with embedded
  records and motion; visible plane z=0, one Link per grid spacing, one
  interval per frame. No absorption, reset, energy law, uncertainty relation
  or quantum entanglement is established.

### E14. An external detector definition with a periodic return

- **Scope and authority.** The model owner's approved periodic axes and
  separate entity definitions, 2026-09-19. The published
  [topology](ENGINE.md#per-axis-gameboard-topology-2026-09-19-implementation-amendment)
  and [loading contract](ENTITY_DEFINITIONS.md) compose the existing detector
  candidate; they do not introduce an absorption or energy law.
- **Frozen setup.** `examples/events/detector/periodic_z_node.json` loads
  `single_node_detector` from `entities/detectors.json` at (4,4,0), on a
  9-by-9-by-1 world with periodic Z and open X/Y. One +Z carrier, identity
  route, N=32, K=1024, threshold 1, reference 0, capacity 31; three intervals.
  The two preparations differ only in carrier phase, 0 or 16.
- **Acceptance fixed before execution.** Pointer values 0,1,2,3 at ticks
  0 through 3, from repeated contacts with the same carrier; one transit
  unit and one material unit remain, momentum (0,0,1), no escapes; owner,
  signed Port and incoming phase retained; live states remain distinct.
- **Status.** Measured, pass within scope, 2026-09-19 11:15 UTC, source
  `32235267e55ac8c9df5b1d4bafa3f02a209b7faf`, fingerprint
  `7e6367eeed29b3d44e48aee05b3ecd2a68d7c3f9fc122fbfa6efd17da679c0c2`.
  Each case ran once through the canonical runner. The separate report
  `universe24_periodic_detector_entities_9x9.html` embeds original, portable
  and expanded inputs, dependencies, records and motion. Exact fingerprints,
  the 458-test gate and display checks are in the
  [validation entry](VALIDATION.md#external-detector-definition-with-a-periodic-return---2026-09-19).
  This is a compact graph demonstration, not arbitrary 3D equivalence or a
  derivation of quantum measurement laws.
