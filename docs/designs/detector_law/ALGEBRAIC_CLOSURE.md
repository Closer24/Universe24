# The algebraic closure of every experiment: the rows that close on a small board in minutes, the rows replaced by a simpler experiment that closes, and the rows dropped (the chief physicist, 2026-09-23; docs only, no run)

The model owner's word of 2026-09-23, about 21:35Z (Hebrew, in substance):
"Verify that for every experiment you see the algebraic way to do it. Our
foreign object is simple: a few sentences. An experiment we do not know
how to realise algebraically, or whose proof you do not see, we do not do;
if needed we replace it by something simple that we can do. Newton we
surely want: that is classical physics. Experiments not proven
algebraically are not done; nor those whose board is too small or that
take hours. Only what is closed in the algebra, then the physics, then at
the end the pins, after we ran them without pins and showed they work.
And tell the Boss: some experiments are only predictions; he should go
over the papers of the world and see how these experiments are best done
to show the connection of the physics to us."

This page is that verification, one row at a time. CLOSED means: the
objects are declared in the one form (a record kind, a block of declared
cells with a pair, a table, a detector with a click), the number is
computed from the algebra before the run by a script beside this page,
the board is a chain, a layer or a box of at most 128^3, and the run takes
minutes. REPLACED means the row's own experiment does not close, and a
simpler experiment that tests the same physics does. DROPPED means no
simple experiment closes tonight; the row keeps its history and its
"not predicted" in the schedule. Every verdict is mine; the list is the
Boss's to close and the owner's to approve (`PLAN.md`).

## 1. The verdicts

| Row | The experiment as scheduled | The algebraic path | Board and time | Verdict |
| --- | --- | --- | --- | --- |
| 1a to 1d, Bell's CHSH, its window, the order channel, no-signalling | a pair of records with two polariser tables acting on the pair (a_now, a_before) by the linear form (DECLARATIONS.md section 14; the clock pair [2464, 25] on N = 2048) | the table's cos^2 law on a shared record, summed at the four settings: 181 / 64 at N = 2048, exact (`DECLARATIONS.md` section 1); no-signalling 0 by the table's symmetry | a 64^2 layer, seconds | CLOSED (quantum, K) |
| 2a, the two slits | the ray splitting at every free Node behind two openings, the screen's clicks | the wave's own sum (the first build's gate test (a) passed); the visibility from the train's coherence, computed | a layer, a minute | CLOSED (quantum, K) |
| 2b, Mach-Zehnder | two corridors between mirror receivers with a splitter table | the splitter's table is the object; the visibility 1.00 - 0.02 by the corridors' equal lengths, computed | a layer, a minute | CLOSED (quantum, K); out of tonight's GO: a GAMEBOARD DIAGNOSTIC world of one record beside the algebra's answer, no pin, never MET or FAIL (the owner's question of 01:25Z; the Boss's order) |
| 2c, Born's exponent (Sorkin) | the three-opening sum | the rule is linear, so the three-opening record is the sum of the three; the click a quadratic form: the Sorkin sum 0 to the grain, EXACT | a layer, seconds | CLOSED (quantum, K), the theorem; out of tonight's GO: the seven-opening worlds as GAMEBOARD DIAGNOSTIC worlds of one record beside it, no pin, never MET or FAIL |
| 9 and Malus's three settings | the polariser table at 45 degrees and at 11.25, 28.125, 33.75 | the table's cos^2 on the counts of 256 | a layer, seconds | CLOSED (quantum, K) |
| 10, the single opening's spread | the wave's sum through an opening in a mirror block | the Rayleigh-Sommerfeld sum on the GameBoard, computed; 0.842 at F = 0.16 | a layer, seconds | CLOSED (quantum, K) as a COMPUTATION check of the rule against the wave law; out of tonight's GO: a GAMEBOARD DIAGNOSTIC world of one record beside it, no pin, never MET or FAIL |
| R5, complementarity | a which-path detector at one opening | NOT DECLARED: the detector's take on one opening and the visibility's fall need the take's declaration under the rule, and the number (V^2 + D^2 = 1) is a theorem of the click's quadratic form once declared | a layer, seconds | DROPPED tonight: the declaration is one page, not written; if the Boss wants it in the paper it is one day's work, else 2a and 2c carry the quantum |
| The atom's lines (item 7 of the plan) | a well of side 20 on a 64^2 layer, emitting through the coupling | the COUPLED mode of the block with light by the linear map of section 7's scheme (ALGEBRA.md 8.9, prediction 6: the lines at the modes' own frequencies; `coupled_mode_pins.py` (a) beside this page prints the coupled mode 0.09953 and the summed record's peak 0.09948 for the 64^2 world, the bare 0.09097 not the line); the lines at the coupled modes, none at their difference | a 64^2 layer, a minute | CLOSED (quantum, P) |
| M1, de Broglie (added 2026-09-23, 23:30Z, on the owner's word and the Boss's decision; the third draft 2026-09-24, 00:25Z) | a lamp of the matter family, a stock of 2048 records through two openings on a layer with open x faces and take lines, the screen's clicks | the band of ALGEBRA.md 8.1, cos omega = cos omega_0 cos omega_l(k), gives k(omega) per ray direction; the two-source sum with those k gives the maxima exactly, the side lobe's count centroid the statistic (`matter_wave_pins.py`) | a 128^2 layer, about 30 minutes | CLOSED (quantum of matter, K), conditional on the lamp verb accepting the matter family (else one generic builder line) |
| M2, the energy of a moving mass (added with M1) | its own chain world: one record, the first click at 84 Links from the lamp's birth stamp against the fringes' k of M1 | the same band: v_g(k) = d omega / dk and the front's first rung by the chain map in the click's own form; the rest limit omega_0 = m c_eff^2 exactly with m = 3 tan omega_0 at the kind's own cone (a derivation, ALGEBRA.md 8.1's two paces); the ratio c_eff^2 / c^2 is row A's | a chain of 200, seconds | CLOSED (K in the form; the rest-mass identity a derivation; no new prediction) |
| 6, Bohr's ladder | the 1 / r well's levels | NOT CLOSED: hydrogen's a_B is 527 Links at mu = 0.15; the box-limited ladder of `pair_field_pins.py` (d) is not a ladder | 256^3 or larger, hours | REPLACED by the atom's lines above (discrete lines at the modes: the atom's physics that closes) |
| 4a, the muon in flight | the block pushed to k = 3 on the layer | the one formula at the exact cone, 0.8116, computed | a 200^2 layer, 2 minutes | CLOSED (classical, K) |
| 4b, the moving lamp's redshift | the pushed block emitting through the coupling, a resting block reading | 1 + z = (1 + beta) / (f / f0)(world) by the one formula on the declared world of DECLARATIONS.md section 4 (the chain of 2200, the well [314, 315] in the medium [156, 157], half depth, eps 0.188): the pin 1.9889 by `coupled_mode_pins.py` (c), the free emitter's limit 1.9339 beside as the (K) form; the emitter's coupling gG = 2 x 10^-5, the receiver a light detector | a chain of 2200, a minute | CLOSED on the PUSHED block (a stepping well is not the object) |
| 4c, the round trip off a receding transponder | light off a hopping mirror face | the mirror's hop of one Link per three intervals: the reflected line at (1 + beta) / (1 - beta) = 3.732 in the mean, with the hop's sidebands at 2 pi / 3 declared beside (the cart worlds already read the form) | a chain, seconds | CLOSED (classical, K) with the sidebands named |
| 5a, the anisotropy of c | the fan of directions under the rule | the GameBoard's own dispersion by direction, computed (the phase pace 0.8, 0.4, 0.2 percent at 12, 16, 24 Links on the axis); read by the probes' phase advance per Link, GAMEBOARD (the first click cannot resolve it, DECLARATIONS.md section 7) | a layer, seconds | CLOSED (classical, K; a reading of the engine's board against the rule's band); a PARAMETER BOUND, not a pin against nature (the reader GAMEBOARD): the lower bound on the wavelength in Links, COMPUTATION, the bound named once: the phase pace's anisotropy between an axis and a face diagonal is k^2 (2 - 1 / 2) / 72 = k^2 / 48, so nature's null below 10^-17 (Herrmann and others 2009) needs k below 2.2 x 10^-8, the wavelength above 2.9 x 10^8 Links, the Link below 1.7 x 10^-15 m for 500-nm light, a bound far weaker than row A2's 10^-27 m |
| 5b, the two arms in motion (Michelson) | two blocks bound by light's standing wave, pushed together | NOT CLOSED: the arms' rigidity in motion is derived on the continuum pace (`PUSH_BALANCE.md`), not on the GameBoard; the bound pair's push is not built; a declared rigid arm would make the null trivial | a 200^2 layer, unknown | DROPPED from the pinned list; kept as the PREDICTION page it is (five's 1 and 1 from light-bound arms) |
| R2, Sagnac | two pushed blocks emitting toward each other, each clicked at the other | beta = v / c exactly by the pushed blocks' clocks and the chain's light, computed; the click's rise per direction from the map subtracted by the reader (DECLARATIONS.md section 13, third draft) | a chain, a minute | CLOSED (classical, K) on the PUSHED blocks |
| R6, aberration | a moving detector's reading of a direction | NOT DECLARED: a direction reading of a detector's set on a 12-Link wavelength has no simple object | a layer | DROPPED |
| The light clock of two bodies | A emitting, B returning, the round trip in A's clicks | 2 L / c with L face to face, the return read by a light detector at A's face, A's coupling gG = 2 x 10^-5 (my line 2), the ring-ups the front's | a chain of 1400, seconds | CLOSED (classical, K in 2 L / c) once the reader is re-declared (Reviewer 3's read) |
| The index at rest (v) and in motion (v-m) | the medium block on a chain | the closed form n^2 = 1 + G g / (omega_0^2 - omega^2); in motion the scheme's own scratch number | a chain, a minute | CLOSED (v: K CONTROL with the 4 percent open in size; v-m: P, Fizeau a declared non-match) |
| A, B, the two-pace bound and the bound clock's second term | no run: derivations read as bounds | the deficit omega_0^2 / 4 and the term eps (gamma^2 - 1) / 2, both printed on every massive world | none | CLOSED as BOUNDS |
| 12, the clock in a field (Newton's potential) | under `pair-field-v1` only: a source block, the pair field, a clock block at r and 2 r | the field is the lattice Green's function (1 / (4 pi r) within 0.5 percent from r = 6, `pair_field_pins.py` (a)); the clock's shift ratio 2.00 at r = 8 ((b)); the clock a block's clicks | a 96^3 box, the field settled in 200 intervals, the clocks read over 2000: minutes | CLOSED under the hypothesis (Newton's potential, K in form) |
| 13, the bending of light | a ray past a crowd | NOT CLOSED as bending: a 12-Link wavelength on a 128^2 board bends by less than the grain | | REPLACED by the DELAY (Shapiro's form, the same 1 + gamma): a light pulse through a medium block sitting in the field against the clock's shift there: 1 + gamma_eff = (n_m^2 - 1) / n_m at one declared coupling, nature's 2 at n_m = 1 + sqrt 2 ((c)); a chain, a minute; CLOSED under the hypothesis with one declared input |
| 14, Newton's 1 / r (the period ratio) | two blocks in orbit | NOT CLOSED: no orbit on a small board (a packet spreads; a well does not move) | hours | REPLACED by NEWTON'S FALL as a PREDICTION OF THE FORM under the hypothesis (section 2): a free massive packet's fall toward a source block, its number computed by the ray equations with the local mass in the declared box's field (`coupled_mode_pins.py` (d)), NOT pinned, not in the paper's list as a pin (the Boss's ruling of 22:14Z on Reviewer 3's MUSTs); Newton's potential, row 12, is the closed Newton row |
| 3, 11a to 11c, the far lamp (cosmology) | none | NOT CLOSED: the crowd's field on a ray over cosmological lengths has no small board; the second step (the field's push on a block) not derived | | DROPPED; "not predicted" stays |
| 7a, 7b, the nuclear bindings | none | NOT CLOSED: what a nucleus is under the rule is undeclared; the contact numbers of (e) are box-limited | | DROPPED |
| 8a to 8c, decays and the neutrino | none | NOT CLOSED: no lifetime from the rule | | DROPPED |
| The photoelectric effect (COVERAGE.md's proposal 1, judged 2026-09-23, 23:35Z) | a lamp at two frequencies and two intensities on a foreign object with a declared rung, the click's onset read | NOT CLOSED: the law's click is a rung on a record's AMPLITUDE (a quadratic form), so its onset moves with the lamp's intensity and not with its frequency; nature's stopping potential is linear in the frequency and blind to the intensity; a frequency rung is not in the law (E = h f is the quantum's identity, one click per quantum, not a threshold) | a layer, seconds | DROPPED from the paper's list; kept as the FIRST FALSIFIER to design on its own page (the row most likely to find a fault, as the coverage page says) |
| Kennedy-Thorndike (proposal 2) | the two-arm relay with unequal arms over a change of the laboratory's speed | NOT CLOSED for the same reason as 5b: the bound pair's push is not on the lattice | | DROPPED with 5b; returns with it |
| Cavendish (proposal 3) | two blocks at rest on a chain, the force at two distances | NOT CLOSED: the second step of `pair-field-v1` (the field's gradient as a block's push) is not derived; it is the reading that would fix kappa, so it is the FIRST world of the hypothesis's second step when that page exists | | DROPPED tonight; after the second step |

The count: CLOSED 19 rows (quantum: 1a to 1d, 2a, 2b, 2c, 9 with Malus's settings, 10, the atom's lines; matter waves: M1, M2; classical: 4a, 4b, 4c, 5a, R2, the light clock, the index at rest and in motion, A and B as bounds), plus 2 under the hypothesis `pair-field-v1` (12, Newton's potential; the delay for 13) and Newton's fall as a PREDICTION of the form, not pinned; REPLACED 3 (6, 13, 14); DROPPED 7 (R5, R6, 5b, 3, 11, 7, 8). The owner's "three from the quantum, three from the classical, a few from the far" is met with room: the Boss chooses the paper's set from the CLOSED rows; "Newton we surely want" is met by row 12's 1 / r and the fall's form.

## 2. Newton's fall: the derivation, and why it is a prediction of the form and not a pin (COMPUTATION; a hypothesis row under `pair-field-v1`)

The massive kind's band: cos omega = cos omega_0 cos omega_l(k). Near the
bottom, omega(k) = omega_0 + k^2 / (2 m) with the GameBoard's mass m = 3
tan omega_0 (0.451 at mu = 0.15), from the six-neighbour sum's k^2 / 6 and
the pair's cot omega_0. Under the hypothesis the pitch at a Node is
omega_0 - delta(r), delta(r) = 4 pi kappa phi(r) -> kappa / r beyond a few
Links (`pair_field_pins.py` (a)), so the MASS IS THE LOCAL PITCH'S, m(r) =
3 tan(omega_0 - delta(r)), and not a constant (Reviewer 3's MUST 1, 21:52Z:
the constant-m line of the first draft dropped it). A packet of the
massive kind wide against its Compton length has the local dispersion
omega(x, k) = arccos(cos(omega_0 - delta(x)) cos omega_l(k)); the
six-neighbour rule moves its mean position and mean phase gradient by
Hamilton's equations on the GameBoard (the discrete Ehrenfest identities
of the linear rule, exact for the means up to the packet's spread), so from
rest d^2 x / dt^2 = (1 / m(r)) d delta / dr = -kappa / (m(r) r^2): the fall
toward the source, Newton's inverse square in the weak field (kappa / r
small against omega_0, where m(r) -> m), with G M standing for kappa / m.
Newton's 4.00 for a(r) / a(2 r) is that WEAK-FIELD LIMIT, never the row's
number on a small board: at kappa = 1.0 the pitch shift at r = 10 is two
thirds of omega_0 and m(10) / m(20) = 0.50, so the ratio reads 8.0 on the
infinite board; at kappa = 0.277 it reads 4.46; a small kappa does not
rescue it, since at kappa = 0.03 the four-Link fall from r = 10 takes over
100 intervals against the packet's spread time of 29.

THE DECLARED BOX IS NOT THE INFINITE BOARD (his line of 21:36Z): on a
periodic box with the background subtracted the field carries the images'
harmonic term r^2 / (6 L^3) beside 1 / (4 pi r), whose gradient opposes the
fall; the box's own gradient ratio from its periodic Green's function is
4.22 at r = 10 and 20 on 96^3, 7.35 at r = 20 and 40 (`coupled_mode_pins.py`
(d), which runs 96^3 only), and 4.12 at r = 10 and 20 on 128^3 by Reviewer
3's own check with the same FFT (his 4.06 was the first term only,
withdrawn). And the fall's click has no room on 96^3 (his MUST 2): a
detector plane four Links inward of a packet of width 8 is covered by the
seed at t = 0; the r = 10 packet's inner edge sits inside the 7-Link floor
of the pitch at kappa = 1.0; between the Compton length 3.9, the spread (29
intervals at w = 8), the floor and the box, no start on 96^3 reads the
fall by a click, and at r = 20 and 40 the box's term spoils it.

THE RULING (the Boss, 22:14Z, on Reviewer 3's recommendation): Newton's
fall is a PREDICTION OF THE FORM under the hypothesis, its number computed
and printed before any run, NOT pinned and not in the paper's list as a
pin; Newton's potential (row 12, the clock's shift ratio 2.00 at r and
2 r) is the closed Newton row. The form's number, by the ray equations of
the exact band with the local pitch in the declared 96^3 box's field, a
point packet from rest to four Links inward (the spread not in it; the
floor IS in the last Link of the r = 10 fall at kappa = 1.0, since the
pitch reaches zero at r = 6.7 and the script's pitch floors at zero): at kappa = 1.0 the accelerations at the start 6.9 x 10^-2 and 8.1 x
10^-3 Link per interval^2 at r = 10 and 20 (the ratio 8.51), the fall times
11.2 and 30.3 intervals ((t20 / t10)^2 = 7.39); at kappa = 0.277 the ratio
4.70 and the times 29.9 and 67.0 ((t20 / t10)^2 = 5.05). The way that
would close the fall as a pin stays open for a later page, before any run:
the spread IN the printed number (the linear map of the massive rule in
the static field, the pin each start's first-click interval from that
map). Two-dimensional note: on a layer the field is logarithmic, not
1 / r; the fall's form needs a box.

## 3. What the Boss is asked (the owner's word)

1. Close the paper's list from the CLOSED rows only; the REPLACED rows
   enter under their new names; the DROPPED rows stay "not predicted".
2. Some rows are predictions only (the atom's lines, the index in motion,
   the bound clock's second term, Newton's fall's number at the declared
   kappa): the paper says so; a prediction is not a pass.
3. Go over the papers of the world for each CLOSED row (the Source
   Verifier's pass from the schedule's NATURE column) and set each
   experiment the way its published form is best matched by our objects.
4. The pair-field rows (12, the delay, Newton's fall) run only after the
   owner's word on the hypothesis and after the current pins, never in
   their place (`PLAN.md` section 4).

## 4. The provenance word per row (issue #1077, the model owner, 2026-09-24; the Boss's order of 01:30Z, record 1561; the chief physicist, 01:55Z)

The owner's test, applied to every row above: redact the NATURE value and
ask whether the same world parameters, tables, windows, reader corrections
and pin value can still be produced from the law and the independently
declared apparatus. One word per row: DERIVED_BLIND (the pin follows from
the law and inputs fixed without the target), APPARATUS_INPUT (a declared
table or apparatus property of kind 1 or 3 carries the form, chosen without
the target, and the pin follows from it: a check of the declared apparatus,
not a derivation of the form), CALIBRATED_FROM_TARGET (an input was chosen
from the value compared with), IMPLEMENTATION_GATE (a declared parameter
read back), FALSIFIER_ONLY (a nature value that stands as a requirement, no
prediction). Only DERIVED_BLIND counts as independent evidence; an
APPARATUS_INPUT row is evidence for the law only through its independent
falsifier. The (K) and (P) marks of the pins stay as they are; nothing here
moves a pin or a world.

| Row | Provenance word | The declaration that carries the target, or the blind inputs | The independent falsifier |
| --- | --- | --- | --- |
| 1a to 1d, Bell (S, the window, the order channel, no-signalling) | APPARATUS_INPUT | the cosine and sine tables at 1 / 256 (the phase circle's rounding, kind 1, the law's own grain) and the polariser's rotation U_s at the CHSH settings 0, N / 8, N / 4, 3 N / 8 (kind 3, the standard arrangement, not the measured S); the pin 181 / 64 follows from them with no use of nature's 2.42; the marginals 1 / 2 and no-signalling of the counts are DERIVED_BLIND theorems of the table's symmetry; the row does not derive the cos^2 law, it inserts the circle's rounding | S at settings other than the maximal four and at another N (the exact rational per N); the order channel (row 1c), open |
| 2a, the two slits | APPARATUS_INPUT | the lamp's train (the coherence, kind 3): the first draft's 128 periods WAS chosen from nature's 0.98 (PINS.md's own sentence) and is CALIBRATED_FROM_TARGET, withdrawn; the GO's train of 32 periods (DECLARATIONS.md section 15 L-3) is chosen by HOST, and the visibility 0.959 follows from it blind (DESIGN.md 6.2); a lamp's coherence is an independent property of a source, declarable without the target | the fringe positions (the maxima at 64 and 64 +- 27 for lambda L / d, DERIVED_BLIND, which no train length sets) and the visibility's rise with the train (a second world at 64 periods, the coherence argument's own number); the visibility 0.959 with its band [0.939, 0.979] does not meet nature's 0.98 and is NOT compared with it (Reviewer 3's line), the positions are the comparison |
| 2b, Mach-Zehnder (not in the GO) | APPARATUS_INPUT | the splitter's integer table [21, 20], [20, 21] over 29 with the quarter turn (kind 3, a balanced splitter by the design, not by nature's 0.98); the dark port 0 by the exact isometry (section 3 declares 0 of 64) follows blind; the first draft's 1 / 1682 was the amplitude series' rounding, without a source here, dropped | the visibility against an unequal-arm world (the dark port's rise with the path difference, the coherence's own number) |
| 2c, Born's exponent (Sorkin; not in the GO) | DERIVED_BLIND | the click's quadratic form (the law's click axiom P10, no target) and the rule's linearity; nature's 0.0064 +- 0.0119 nowhere in the inputs | any Sorkin sum beyond the counts' error in a three-opening world |
| 9 and Malus's three settings | APPARATUS_INPUT | the same tables as Bell's (kind 1) and the polariser's rotation at s (kind 3); the counts 128 / 128 at 45 degrees follow blind; the row is a check of the declared table, not a derivation of cos^2 | the three new settings 11.25, 28.125, 33.75 degrees with the table's rounding predicted before the run (-0.00100, -0.00044, +0.00006: DERIVED_BLIND numbers of the grain) |
| 10 (a) and (b), the single opening (not in the GO) | DERIVED_BLIND | the rule's own sum through a declared opening; the pins 0.842 and 0.886 are computations of wave optics (the datums' kinds, DESIGN.md 6.1), no nature value in the inputs; NATURE (Nairz 2002) is named beside, unused | the bell's width at a second Fresnel number |
| The atom's lines (P) | DERIVED_BLIND | the well (side, pair) and the coupling (kind 2, 3) chosen by the design; the coupled modes computed from them; nature has no atom at this scale | a line at the modes' difference, or a line off the coupled mode by more than the band |
| M1, de Broglie | DERIVED_BLIND | the lamp's omega (kind 3, 12 Links by the design), the openings and the screen; k(omega) from the band; the centroid follows; Joensson's spacing unused | the second wavelength (16 Links, the centroid 64 + 39.23) and any lobe off the two-source sum |
| M2, the energy of a moving mass | DERIVED_BLIND | the same lamp; the front's first rung from the band's v_g by the map; Bertozzi unused; E = m c^2 an identity of the band | the first rung at 16 Links (170) against the band's 177.6 |
| 4a, the muon in flight | DERIVED_BLIND | the one formula at the exact cone on the declared world; nature's gamma unused (the form 1 / gamma_m compared) | a second k within the floor (the form at two speeds) |
| 4b, the moving lamp's redshift | DERIVED_BLIND | the one formula on the declared world (the well [314, 315] in [156, 157], the coupling g G = 2 x 10^-5 chosen weak by the design after the builder's finding at g = 1 / 5, not by the target); Ives-Stilwell's form compared, its number unused | the control at rest (1.9350 / 1.9319) and the free emitter's limit 1.9339 beside; a reading off 1.9889 by more than the band |
| 4c, the receding transponder | DERIVED_BLIND | the hop of one Link per three intervals; (1 + beta) / (1 - beta) follows; no target in the inputs | the sidebands at 2 pi / 3 declared beside |
| 5a, the anisotropy of c | DERIVED_BLIND | the band's own dispersion by direction; nature's bound unused; a GAMEBOARD reading of the engine against the rule | a phase pace off k^2 (3 SUM n^4 - 1) / 72 by direction |
| R2, Sagnac | DERIVED_BLIND (Reviewer 3's word asked) | the two blocks' push (kind 3) and the chain's light; the reader's rise per direction (+4.1, +8.1 at W = 64) computed from the engine's own map before the run (`coupled_mode_pins.py` (f)), with no use of Michelson, Gale and Pearson's 0.975: the redaction test passes | the control world's click 109 +- 2; the two clicks per direction 250 +- 2 and 74 +- 2 as the DETECTOR readings the band is on |
| The light clock of two bodies, at rest | DERIVED_BLIND | 2 L / c and the rise from the map (218 at W = 64); no target | the pin's band +- 2; the rise's fall with W (216, 214, 212) |
| The light clock in motion (DECLARATIONS.md section 10 item 7; P) | DERIVED_BLIND (P) | the pushed pair at a declared separation: gamma^2 / gamma_m = 1.2224 along and gamma / gamma_m = 0.9981 across at k = 3 by the band and the transits, no target in the inputs; two words for the two arms: the across arm a MET in form, the along arm a predicted FAIL as declared against nature's null (Michelson-Morley, Kennedy-Thorndike); a row with a prediction is never FALSIFIER_ONLY (Reviewer 3's word); not a pass | the null itself; a light-held pair (Highlights' five, section 8b) is the world that could meet it |
| The index at rest (v) and in motion (v-m) | DERIVED_BLIND | the closed form n^2 = 1 + G g / (omega_0^2 - omega^2) from the declared coupling; (v-m) the scheme's own number, a prediction; Fizeau a declared non-match | the cavity's mode sum beside (the 4 percent open in size) |
| A, B, the two-pace bound and the bound clock's second term | DERIVED_BLIND | bounds printed from the band on every massive world; nature's bounds compared, unused as inputs | the bounds themselves |
| 12, the clock in a field (under `pair-field-v1`; not in the paper's list) | DERIVED_BLIND under the hypothesis | the lattice Green's function from the hypothesis's field; the shift ratio 2.00 at r and 2 r computed (`pair_field_pins.py` (b)), not taken from nature; the hypothesis itself is beside the law | the ratio at 4 r; the field's 1 / r against the box's images |
| 13, the bending of light, as the DELAY (under the hypothesis; not in the paper's list) | CALIBRATED_FROM_TARGET | the one declared coupling that puts n_m at 1 + sqrt 2 so that 1 + gamma_eff = 2: the target fixes the input; a form check only. The original row 13 (gamma_PPN = 1 declared, then compared with nature's 2) is CALIBRATED_FROM_TARGET as well (redact nature's 2 and gamma_PPN = 1 has no other source: Reviewer 3's word), checked as an IMPLEMENTATION_GATE of the declared parameter, as PINS.md's design question says | a second coupling (the form (n_m^2 - 1) / n_m at another n_m), or the same coupling's clock shift read beside |
| 14, Newton's fall (the form, under the hypothesis; not pinned) | DERIVED_BLIND (P, the form) | the ray equations with the local mass in the declared box's field; the spread not in it; no target | the fall's number against the box's gradient at two radii |
| 3, 11a to 11c, the far lamp (outside the paper's list) | FALSIFIER_ONLY | the registered nature values q_0, b, Tolman's 4 stand as requirements, not computed, not predicted (the owner's comment on issue #1077 is right); no world | the values themselves, when a derivation exists |
| 5b and Kennedy-Thorndike (dropped) | FALSIFIER_ONLY | the null as the requirement; the light-held pair's push not built; the pushed pair's number is the light clock in motion above | the null |
| R5, R6, 6, 7, 8, the photoelectric effect, Cavendish (dropped) | FALSIFIER_ONLY | nature's values stand as requirements the law does not reach or does not declare; the photoelectric effect the first falsifier to design (the click's onset moves with the intensity, not the frequency) | each row's own value |

THE COUNT by first word: APPARATUS_INPUT 4; DERIVED_BLIND 16; CALIBRATED_FROM_TARGET 1; FALSIFIER_ONLY 3. The paper's table carries the word per
row from this section (the writer, on the merge); Reviewer 3's own words on
1a, 2a, 2b, 9, 13 and R2 under the same test are asked independently and
decide where they differ from mine.
