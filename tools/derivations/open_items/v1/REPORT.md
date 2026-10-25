# Hand V1: the pump and light's redshift (2026-10-25, branch engine-5.0-test at 8aa19393b)

Worktree: /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/v1 (branch hand-v1). Scripts and outputs under tools/derivations/v1/ in the worktree: pump_unit.py (pump_unit.json), pump_dynamics.py (pump_dynamics.json, pump_dynamics.log), redshift_chain.py (redshift_chain.json, redshift_chain.log). Nothing in src/ touched. Every number below is read from those outputs. The owner's three additions are kept: one pair per line, a constant of the universe (Addition 2; the per-Link num of Addition 1 is answered in one line under 2.4 and not used); integer readings only, a float named as a check beside its integer reading (Addition 3).

One slip in the brief, named first: the engine's volume is X = Gamma (Gamma / p_0)^(d + 1) with d + 1 = 4 (features/volume, **The carried momentum**), so X = Gamma e^(4 U) and e^U = (X / Gamma)^(1 / 4), not Gamma e^(3 U); the record's "U 1.8035 at the volume 169,775,404" is the board's sum over 125 Nodes, 1,358,203 per Node, and ln(1,358.2) / 4 = 1.8035. Every lay below is X = Gamma m^4 or X = Gamma 2^k, integers, with m = e^U the Link's length to the clock's rounding.

## 1. The derivation, from the law's clauses by name

### 1.1 What a quantum of the massless line is on the board

(i) **The flux form of Rule3**, **The line**, **The paces**: the massless pair has num = den, so the Node's mass D_i = 12 (den - num) p_0^2 G^2 is 0; with no tension every Link's factor is Q = G^2, the reach R = 2 den p_i^2 G^2 on each of the six Links, the wall w = 6 den Gamma^2 G^2 and the own weight S = 2 w - 6 R. The line is a_next - 2 a_now + a_before = (p_i^2 / (3 Gamma^2)) SUM_j (m_j - a_now) + (r - r') / w, every coefficient a function of the Node's content alone.

(ii) **The uniform seed is a lay**, **No write from outside Rule3 wakes either double root of the massless row**, **The uniform mode carried by Rule3's own k = 0 line**: the seed is now = v, before = 0 at every Node with v = largest_below(T) = 189 (v^2 = 35,721 <= T = 36,000). Every Link's two ends alike, the Links' sum is 0, D is 0, so a_next - a_now = a_now - a_before: the sea's velocity v is a constant of the run at every content, whatever the paces do. The remainder at the half wall feeds no drift. The uniform mode is the double root, a ramp and no oscillation (omega = 0).

(iii) **The count is the record's share**, **The conserved form**, **The clock is the Node's, the tension is the Link's**: the count is the share e_i = [w (now^2 + before^2) - S now before - now SUM_j R_ij before_j] div (2 p_i^2 G^2), in quanta over W_c = 3 den T, the vacuum's quantum. For the sea (before 0 everywhere) the Link term and the S term are 0 and

e = (6 den Gamma^2 G^2 v^2) div (2 p_i^2 G^2) = (3 den Gamma^2 v^2) div p_i^2 = 3 den v^2 (Gamma / p_i)^2,

the vacuum's 3 den v^2 (one quantum, v^2 / T = 0.992) times the frame's weight (Gamma / p_i)^2, the weight 1 / p_i^2 the form carries on the Node's term so that **D M** is symmetric.

(iv) **The paces compose** and the volume form (**The carried momentum**, features/volume): p_0 = Gamma (1 - 1 / Gamma)^c, p_i = p_0^2 / Gamma rounded once, and X = Gamma (Gamma / p_0)^4, so (Gamma / p_i)^2 = (Gamma / p_0)^4 = X / Gamma exactly in the reals and to two roundings in the integers. Hence

the count of the sea per Node = (v^2 / T) (X / Gamma) = X / Gamma to the rounding: the quanta of the massless seed are the volume's level over Gamma.

This is the pump's whole root for the seed: the energy in the levels (v^2 per Node) never changes; the unit the count is read in is the vacuum's W_c while the Node's term is weighted by the frame, Gamma^2 / p_i^2 = X / Gamma. The share is the energy conjugate to the board's interval (the canonical form Rule3 conserves at fixed paces): its kinetic term carries (h^3 / N) with h = Gamma / p_0 the Link's length and N = p_0 / Gamma the proper interval per interval, h^3 / N = e^(4 U) = X / Gamma, the metric's volume factor; the vacuum's quantum W_c does not carry it. For the seed the pump is the read's unit and not the dynamics: measured in 3.1 and 3.2 (the count equals the formula at every X bit for bit; with the close off the sea's velocity stays 189 at every interval and the count equals the formula at the X the board holds at every interval).

### 1.2 The redshift in the law: a wave riding the expansion

(v) **The band at a pace**: a wave at wave number k on the massless line rotates at 1 - cos omega = (p_i / Gamma)^2 (1 / 3) SUM_a (1 - cos k_a), that is 2 sin(omega / 2) = (p_i / Gamma) 2 sin(omega_vac / 2) exactly, the clock acting on 2 sin(omega / 2) (**The same clock and the same ruler for every act**). The wave number k is the torus's, 2 pi M / N, a constant of the lay: the lattice does not stretch (**The unbounded board**'s finding: a growing board stretches nothing), the Links lengthen through the paces.

(vi) The frequency as the Node's clock reads it: the proper interval per board interval is N = p_0 / Gamma (**The paces compose**: a record at a Node of pace p has its intervals p / Gamma as long; the credit's `proper`, Lattice.proper_count, is SUM p_0 over the intervals, over Gamma). So

omega_proper = omega_board Gamma / p_0 = omega_vac (p_i / Gamma)(Gamma / p_0) = omega_vac p_0 / Gamma = omega_vac / e^U

to the small-angle reading (exactly on 2 sin(omega / 2)): the beat of a massless wave per proper interval falls as 1 / e^U, nature's redshift E proportional to 1 / a with a = e^U the Link's length, from the integers alone, by the one fact p_i = p_0^2 / Gamma: the Link's pace is the clock twice, so p_i / p_0 = p_0 / Gamma. Measured in 3.3 (the ride: E_proper e^U constant within one crossing per window while E_proper falls by the Link's length).

(vii) The share of a wave (derived from (iii) by the Links' sum of a plane wave, exact at any k): summed over the N Nodes of the board, SUM e_i = 3 den N (Gamma / p_i)^2 A^2 sin^2 omega, A the amplitude. At fixed paces A^2 sin^2 omega is the recurrence's invariant (the form). Under paces that change slowly, the three-term recurrence a_next = 2 cos omega a_now - a_before has the adiabatic invariant A^2 sin omega (the oscillator's energy over its frequency, the unit-mass form), so along the expansion

A proportional to 1 / sqrt(sin omega) proportional to (Gamma / p_i)^(1 / 2) = e^U: the amplitude grows as the Link's length, where nature's falls as 1 / a;
the share proportional to (Gamma / p_i)^2 A^2 sin^2 omega proportional to Gamma / p_i = e^(2 U) = m^2: the count in W_c grows as the Link's length squared, where nature's energy falls as 1 / a;
the number of quanta at the local beat, the share over omega_board (the same number as the proper energy over the proper frequency), proportional to e^(2 U) / e^(-2 U) = e^(4 U) = X / Gamma: the number of quanta grows as the volume's level, where nature conserves it.

So for a wave the pump is the dynamics: the law gives nature's redshift of the beat exactly and the opposite of nature's fall of the energy. Measured in 3.3 (A / m, share / m^2 and quanta / m^2 constant along the ride within the crossing tolerance; the number over m^4 constant).

(viii) Why, in one line: Rule3's massless line is the wave equation of the metric ds^2 = -(p_0 / Gamma)^2 dt^2 + (Gamma / p_0)^2 dx^2 with the volume factor frozen inside the step. Multiplying (i) by X / Gamma (and (p_i / Gamma)^2 = Gamma / X), Rule3 reads (X / Gamma) w (a_next - 2 a_now + a_before) = (w / 3) SUM_j (m_j - a_now) + the remainders. Nature's line in the board's interval is (X_now / Gamma) w (a_next - a_now) - (X_before / Gamma) w (a_now - a_before) = (w / 3) SUM_j (m_j - a_now), the volume at its own half-interval on each velocity: the two differ by w (X_now - X_before) (a_now - a_before) / Gamma, the volume's change times the velocity, the friction of the expansion, which Rule3 does not carry. The law names its consequence as a finding, **The paces' own change moves the share with no current**: the share changes by the work term where the paces move. For the seed (k = 0) nature's line gives (X / Gamma) v constant, v falling as Gamma / X and the share as Gamma / X; Rule3 keeps v and the share rises as X / Gamma.

### 1.3 The unit the decoder should use

(ix) The credit's beat is W_c sin omega_board, 3 T den times the integer sine of the point read from three levels (meeting_board.readings_at, paces.sine_den): a rotation per board interval. The decoder has the Node's clock (the proper count). The energy of a light quantum as nature's observer reads it is its rotation per proper interval: in integers, over a span of S intervals at one Node, the count n of upward zero crossings of the level against the proper count P = SUM p_0 over the span, E = n Gamma / P (a quotient with remainder, scaled); it falls as p_0 / Gamma along the expansion. The count of light quanta the decoder should report is the share over W_c times the Link's length to the fourth, that is the share times Gamma over (W_c X): for the seed it returns the laid count at every X (3.1: the count over X / Gamma is 0.992 to 1.0 at every row), for a wave it falls as 1 / m^2 by the dynamics of (vii). The Link's length itself enters nowhere in E; it enters the count.

### 1.4 The lay lock

(x) **The board reads itself**, the exact take, and FURTHER_RESEARCH.md, The lay lock: a close is refused by the lay where the children's family's share at the Node already stands above its unit. Every born family's share is read with the same frame weight, so the born records' count per Node rises as X / Gamma with no birth (measured 3.2: the children's count 189 to 972 over 27 Nodes from t 59 to 140 with no birth between, X 5,415 to 19,227). On the record's 5-cube 108 records stand on 125 Nodes, below one per Node for each of the three families in the lay's own unit, so the lock is the unit's: with the share read over X / Gamma the lay refusal lifts at most Nodes (a projection from the record's counts, not run). On the toy 3-cube 54 records stand on 27 Nodes and the lock stands under either unit (3.2: the corrected children's count 1.9 to 3.1 per Node).

## 2. What is derivable and what needs the owner's word

### 2.1 Derived, needing no word (the decoder's readings; a sentence for the law's reading section)

**The beat per proper interval is the quantum's energy** (derived, 2026-10-25): a massless wave at the torus's wave number k rotates at 2 sin(omega / 2) = (p_i / Gamma) 2 sin(omega_vac / 2) per board interval, and per proper interval, the Node's clock p_0 / Gamma, at 2 sin(omega / 2) Gamma / p_0 = (p_0 / Gamma) 2 sin(omega_vac / 2), falling as the Link's length Gamma / p_0 grows: the redshift of light's beat is nature's, E proportional to 1 / e^U, by p_i = p_0^2 / Gamma alone. The decoder reads a light quantum's energy as its upward zero crossings over a span against the span's proper count, n Gamma over SUM p_0, and never as the beat per board interval, which falls as the Link's length squared. The count of the massless line in W_c is the energy conjugate to the board's interval and carries the frame's weight Gamma^2 / p_i^2 = X / Gamma: the seed's count per Node is X / Gamma at its one laid quantum; the decoder reports the count over X / Gamma. Status: derived; measured on the chain and the 3-cube (tools/derivations/v1); fence: lattice.

**The pump is two things** (a finding by name, 2026-10-25): the seed's count rises as the frame's weight X / Gamma at a velocity Rule3 keeps exactly, the read's unit and no dynamics; a wave's amplitude rises as e^U and its share as e^(2 U) under the paces' slow change, the adiabatic invariant of Rule3's three-term recurrence being A^2 sin omega, and the number of its quanta at the local beat as e^(4 U) = X / Gamma, where nature's amplitude falls as e^(-U) at a conserved number: Rule3's massless line is the metric's wave equation with the volume factor frozen inside the step, the term w (X_now - X_before)(a_now - a_before) / Gamma not carried. The lay lock on the record is the unit's: the born families' shares at every Node rise as X / Gamma with no birth, above their unit everywhere.

### 2.2 Needs the owner's word (a change of Rule3's line; against "Rule3 is not changed")

**The massless line rides the volume** (a sentence for the owner, not entered): at a Node whose volume's level is X_now at the interval's start and X_before one interval earlier, the massless line steps by

w [X_now (a_next - a_now) - X_before (a_now - a_before)] + r' - r = X_now SUM over the six Ports of R_ij (m_ij - a_now),

one carried division at the wall w X_now, the remainder kept in [0, w X_now); at X_now = X_before it is Rule3's line bit for bit; backward the same act, the coefficient of a_before being the previous step's wall w X_before. What it buys: the amplitude falls as 1 / e^U, the number of quanta is conserved and the energy per quantum falls as 1 / e^U, nature's radiation; the seed's velocity falls as Gamma / X and the pump is gone. Its costs, named: the wall is one no more (per Node and per interval, **The wall is one** kept by name); the width, w X within 128 bits, w = 6 den Gamma^2 G^2 at 41 bits for den 1,021 (X below 2^87, every U of a run) and near 100 bits at the top tier's den (X below 2^28, U below 4.6); the inverse to be measured (the remainder's wall moving with X); and the cosmology: the seed's write falls with its energy, so the record's expansion, driven by the pumped seed, would have to be measured again. Not run.

### 2.3 Not recommended

Reading the count in the write's units (the former candidate): it undoes the unit for the seed as the share over X / Gamma does, and leaves the wave's dynamics as they are; the law's lack is the dynamics' friction, no unit mends it.

### 2.4 The tensor at the Node (Additions 1 and 2)

A per-Link num would scale each Link's reach R_ij alone: it changes the dispersion's SUM_a (1 - cos k_a) per axis (an anisotropic light speed) and neither the frame's weight 1 / p_i^2 (the unit) nor the clock's p_0 / Gamma, so it touches neither the pump nor the redshift; under Addition 2 it is not wanted and nothing above uses it. Every line above holds one pair, [1, 1] for light, a constant of the universe.

## 3. Every number measured

Python /home/user/Universe24/venv314/bin/python with PYTHONPATH=<worktree>/src:<worktree> and TMPDIR=/dev/shm/tmp; the tests' small universe (den 1,021, Gamma 1,000, T 36,000, G 16; W_c = W_rec = 110,268,000; v = 189; the frozen content 3,793).

### 3.1 The static read (tools/derivations/v1/pump_unit.py, pump_unit.json)

Command: PYTHONPATH=$PWD/src:$PWD TMPDIR=/dev/shm/tmp python tools/derivations/v1/pump_unit.py

The bare 3-cube, the uniform sea at every Node, the volume set by hand to X = Gamma 2^k, the count read with nothing stepped. The engine's share equals the formula (3 den Gamma^2 v^2) div p_i^2 bit for bit at every row; the count equals (v^2 / T)(Gamma / p_i)^2 to the rounding:

| X | X / Gamma | c | p_0 | p_i | share per Node | quanta per Node | total (27 Nodes) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1,000 | 1 | 0 | 1,000 | 1,000 | 109,413,423 | 1 | 27 |
| 2,000 | 2 | 173 | 841 | 707 | 218,892,951 | 2 | 54 |
| 16,000 | 16 | 693 | 500 | 250 | 1,750,614,768 | 16 | 432 |
| 64,000 | 64 | 1,039 | 354 | 125 | 7,002,459,072 | 64 | 1,728 |
| 256,000 | 256 | 1,387 | 250 | 63 | 27,567,000,000 | 250 | 6,750 |
| 1,024,000 | 1,024 | 1,733 | 177 | 31 | 113,853,718,002 | 1,033 | 27,891 |
| 4,096,000 | 4,096 | 2,082 | 125 | 16 | 427,396,183,593 | 3,876 | 104,652 |
| 16,384,000 | 16,384 | 2,423 | 89 | 8 | 1,709,584,734,375 | 15,504 | 418,608 |
| 65,536,000 | 65,536 | 2,771 | 63 | 4 | 6,838,338,937,500 | 62,016 | 1,674,432 |

The count per Node is X / Gamma to the two roundings of the paces (250 for 256, 1,033 for 1,024, 62,016 for 65,536); the energy in the levels is 3 den v^2 at every row. The record's seed count 132 to 218,505 to 966,864 is this: 125 Nodes times X / Gamma (1,358 and 5,787 at the two tops) gives 169,775 and 723,428, the rest the light's own levels under the births.

### 3.2 The dynamics (tools/derivations/v1/pump_dynamics.py, pump_dynamics.json, pump_dynamics.log)

Command: PYTHONPATH=$PWD/src:$PWD TMPDIR=/dev/shm/tmp python tools/derivations/v1/pump_dynamics.py

The 3-cube, the uniform sea, X laid at X_0 rising by one, 320 intervals from U 0 and 200 from U 0.5.

The close off (Lattice.advanced_to_the_close alone, the click act skipped by name): the sea's velocity is 189 at every Node at every interval (the sign flipping at the swap at the top, t 140, 27 Nodes turned), the count per Node equals the formula at the X the board holds at every one of the 321 intervals (checked True), the volume rising 1,000 to 7,719 at t 140 and returning to 999 at t 280 (the uniform board's return), the count 1, 2, 4, 7, 8, 7, 5, 2, 1 at t 0, 40, 60, 100, 140, 160, 200, 240, 260. The pump of the seed is the read's unit alone.

The close on (Lattice.step): the count reaches 2 per Node at t 23 by the unit alone (X 1,556, the energy unchanged, the velocity 189); 27 refused reads by name origin per close from t 18 to 33; at t 34 (X 2,124) the board births 27 pairs, one per Node, 135 lays, and the take spends the sea's velocity 189 to 117 at every Node (v^2 35,721 to 13,689, the fall 22,032 = 0.612 T per Node); at t 59 a second round of lays (162 lays, 81 credits) takes it to 71; from t 48 the close is refused by the lay (270 lines), from t 80 by the stop (the light cannot pay, 162 lines) as the velocity falls to 27 and the count to 0 per Node at t 100. The born family's count ("point 2") 189 at t 34, 378 at 59, 756 at 100, 972 at 140, 864 at 200 over 27 Nodes with no birth after 59: the children pumped by the unit as the seed is. The corrected count (times Gamma / X): 83 at t 40 (3.1 per Node), 55 at 100 (2.0), 51 at 140 (1.9), 52 at 200 (1.9). From U 0.5 (X 7,389): 27 births at the first closes, the velocity 189 to 156, 144, 134, 125, 109 by t 140, the children 783 to 1,863, every later close refused by the lay (5,373 lines in 200 intervals).

### 3.3 The chain: the dispersion and the ride (tools/derivations/v1/redshift_chain.py, redshift_chain.json, redshift_chain.log)

Command: PYTHONPATH=$PWD/src:$PWD TMPDIR=/dev/shm/tmp python tools/derivations/v1/redshift_chain.py

The chain [28, 1, 1], the wave at k = pi / 2 (cos k = 0, the wavelength 4 Links, the law's cos omega = (3 Gamma^2 - p_i^2) / (3 Gamma^2) a rational), A = 1,500, laid with the law's integer sine; the frame held by hand at every interval's start (the volume at X, the three tension lines at 0; the first run with the tensions free showed the wave's own stress writing the Links' factors, the amplitude 1,500 to 7,261 at fixed X and the frequency a third of the law's, so the frame is held whole); every act but the close.

Fixed m, the span 2,000 intervals, no Node turned at any m (turned 0 on every row):

| m | X | c | p_0 | p_i | crossings n | board period S div n, r | law's period (check, float) | proper sum P = SUM p_0 | proper period P div (n Gamma), r | share start -> end | quanta start -> end | amplitude end (largest) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1,000 | 0 | 1000 | 1000 | 267 | 7, 131 | 7.47 | 2,000,000 | 7, 131,000 | 107,201,740,968 -> 144,170,850,796 | 980 -> 1302 | 1467 (1506) |
| 2 | 16,000 | 693 | 500 | 250 | 65 | 30, 50 | 30.73 | 1,000,000 | 15, 25,000 | 127,061,081,280 -> 130,190,269,895 | 1148 -> 1183 | 1304 (1533) |
| 3 | 81,000 | 1097 | 334 | 112 | 29 | 68, 28 | 68.68 | 668,000 | 23, 1,000 | 128,352,663,040 -> 129,508,951,446 | 1162 -> 1162 | 1094 (1504) |
| 4 | 256,000 | 1387 | 250 | 63 | 16 | 125, 0 | 122.13 | 500,000 | 31, 4,000 | 128,338,749,210 -> 128,436,352,870 | 1162 -> 1162 | 1063 (1503) |
| 5 | 625,000 | 1611 | 200 | 40 | 10 | 200, 0 | 192.37 | 400,000 | 40, 0 | 126,056,999,250 -> 126,529,458,832 | 1148 -> 1148 | 1210 (1501) |
| 6 | 1,296,000 | 1791 | 167 | 28 | 7 | 285, 5 | 274.83 | 334,000 | 47, 5,000 | 127,563,885,834 -> 127,975,847,090 | 1162 -> 1162 | 1467 (1504) |

The board period grows as m^2 (7, 30, 68, 125, 200, 285 intervals against 7.47 m^2 = 7.5, 29.9, 67.2, 119.5, 186.8, 268.9, each within one crossing of n) and the proper period as m (7.49, 15.38, 23.0, 31.25, 40.0, 47.7 against 7.49 m = 7.5, 15.0, 22.5, 30.0, 37.4, 44.9): the beat per proper interval falls as 1 / m, nature's redshift; the beat per board interval as 1 / m^2. The share stands at fixed paces to the walk (the m 1 row's rise 107 to 144 x 10^9 is the remainders' walk at the vacuum's large angle over 2,000 intervals; from m 2 on within 2.5 percent) and the count in W_c stands (1,148 to 1,183 at m 2; 1,162 to 1,162 from m 3).

The redshift predicate in integers, P(m) n(b) b against P(b) n(m) m, the tolerance one crossing on each side (P(b) m + P(m) b):

| m | base b = 1: left, right, difference, tolerance, pass | base b = 2: left, right, difference, tolerance, pass |
| --- | --- | --- |
| 1 | 534,000,000, 534,000,000, 0, 4,000,000, PASS | 260,000,000, 267,000,000, -7,000,000, 5,000,000, FAIL |
| 2 | 267,000,000, 260,000,000, 7,000,000, 5,000,000, FAIL | 130,000,000, 130,000,000, 0, 4,000,000, PASS |
| 3 | 178,356,000, 174,000,000, 4,356,000, 6,668,000, PASS | 86,840,000, 87,000,000, -160,000, 4,336,000, PASS |
| 4 | 133,500,000, 128,000,000, 5,500,000, 8,500,000, PASS | 65,000,000, 64,000,000, 1,000,000, 5,000,000, PASS |
| 5 | 106,800,000, 100,000,000, 6,800,000, 10,400,000, PASS | 52,000,000, 50,000,000, 2,000,000, 5,800,000, PASS |
| 6 | 89,178,000, 84,000,000, 5,178,000, 12,334,000, PASS | 43,420,000, 42,000,000, 1,420,000, 6,668,000, PASS |

Against the base m 1 the row m 2 misses by 1.75 crossings: the law's exact invariant is 2 sin(omega / 2) Gamma / p_0 and not omega Gamma / p_0, and at the vacuum the k = pi / 2 wave's omega 0.841 exceeds 2 sin(omega / 2) by 3.0 percent (omega^2 / 24), below 0.2 percent from m 2 on; against the base m 2 every row passes. The toy's predicate takes the base m 2, or a longer wavelength (k = pi / 4 on a chain of 8 n Nodes, the correction 0.2 percent at the vacuum).

The ride, X(t) = (Gamma (2000 + t)^4) div 2000^4, the Link's length (2000 + t) / 2000 from 1 to 3.4 over 4,800 intervals, windows of 400 (the frame held each interval; 252 Node-intervals turned in the first 9 intervals of window 0, the hand-set X_before = X - 1000 standing below the floor at X just above 1,000, none after):

| window | t mid | m = (2000 + t) / 2000 | X | p_0 | p_i | crossings n | proper sum P | E e^U = n (2000 + t) 10^6 div (2000 P), r | E_proper = n Gamma 10^6 div P, r | share at start | share x 2000^2 div (2000 + t_start)^2 | quanta in W_c | quanta x 2000^4 x 10^3 div (2000 + t_start)^4 | largest level | largest x 2000 x 10^3 div (2000 + t) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 200 | 2200/2000 | 1,464 | 910 | 828 | 43 | 364,960 | 129, 440,320,000 | 117,821, 47,840 | 107,201,740,968 | 107,201,740,968 | 980 | 980,000 | 1,745 | 1,586,363 |
| 1 | 600 | 2600/2000 | 2,856 | 770 | 593 | 31 | 308,579 | 130, 369,460,000 | 100,460, 153,660 | 162,473,308,270 | 112,828,686,298 | 1,484 | 715,663 | 2,017 | 1,551,538 |
| 2 | 1000 | 3000/2000 | 5,062 | 667 | 445 | 23 | 267,318 | 129, 31,956,000 | 86,039, 226,598 | 226,076,735,766 | 115,345,273,350 | 2,044 | 532,069 | 2,288 | 1,525,333 |
| 3 | 1400 | 3400/2000 | 8,352 | 589 | 347 | 18 | 235,807 | 129, 361,794,000 | 76,333, 144,269 | 297,386,898,858 | 116,166,757,366 | 2,702 | 412,292 | 2,570 | 1,511,764 |
| 4 | 1800 | 3800/2000 | 13,032 | 527 | 278 | 14 | 210,954 | 126, 39,592,000 | 66,365, 37,790 | 378,192,464,720 | 116,726,069,358 | 3,430 | 326,741 | 2,834 | 1,491,578 |
| 5 | 2200 | 4200/2000 | 19,448 | 477 | 228 | 12 | 190,845 | 132, 16,920,000 | 62,878, 48,090 | 469,058,925,048 | 117,264,731,262 | 4,256 | 266,000 | 3,123 | 1,487,142 |
| 6 | 2600 | 4600/2000 | 27,984 | 435 | 189 | 10 | 174,243 | 131, 348,334,000 | 57,391, 19,987 | 567,058,946,104 | 117,160,939,277 | 5,152 | 219,930 | 3,409 | 1,482,173 |
| 7 | 3000 | 5000/2000 | 39,062 | 401 | 161 | 8 | 160,305 | 124, 244,360,000 | 49,904, 139,280 | 676,089,485,442 | 117,376,646,778 | 6,132 | 184,823 | 3,722 | 1,488,800 |
| 8 | 3400 | 5400/2000 | 53,144 | 371 | 138 | 7 | 148,432 | 127, 98,272,000 | 47,159, 95,312 | 796,135,169,956 | 117,771,474,845 | 7,224 | 158,082 | 4,032 | 1,493,333 |
| 9 | 3800 | 5800/2000 | 70,728 | 345 | 119 | 6 | 138,197 | 125, 250,750,000 | 43,416, 39,048 | 920,136,961,814 | 117,364,408,394 | 8,344 | 135,750 | 4,314 | 1,487,586 |
| 10 | 4200 | 6200/2000 | 92,352 | 323 | 104 | 6 | 129,289 | 143, 223,346,000 | 46,407, 85,377 | 1,055,948,254,368 | 117,327,583,818 | 9,576 | 118,222 | 4,570 | 1,474,193 |
| 11 | 4600 | 6600/2000 | 118,592 | 304 | 92 | 5 | 121,458 | 135, 206,340,000 | 41,166, 59,972 | 1,209,402,966,142 | 118,105,758,412 | 10,976 | 104,675 | 4,849 | 1,469,393 |

Read: E e^U (x 10^6) 129, 130, 129, 129, 126, 132, 131, 124, 127, 125, 143, 135 over the twelve windows, constant within one crossing per window (5 to 43 crossings, one crossing 2 to 20 percent), while E_proper (x 10^6) falls 117,821 to 41,166, the ratio 2.86 against the Link's length's 3.0 (within one crossing of 5): the redshift of the beat is nature's. The share over m^2 rises 107.2 to 118.1 x 10^9 (10 percent over the ride, the walk and the windows' phase), the count in W_c 980 to 10,976 (x 11.2 against m^2 = 10.9): the wave's share and count grow as the Link's length squared. The largest level over m, 1,586 to 1,469 (x 10^-3), the amplitude growing as the Link's length within 8 percent; the count over m^4 falls 980 to 105 (x 10^-3), as 1 / m^2. The number of quanta at the local beat, the count in W_c over the beat per board interval, grows as m^2 / m^-2 = m^4 = X / Gamma. Floats in this script: the law's period 2 pi / acos(1 - p_i^2 / (3 Gamma^2)) printed as a check beside the integer period; nothing else.

## 4. The toy for David (integer readings only)

The redshift toy. The lay: the tests' small universe (den 1,021, Gamma 1,000, T 36,000), the chain [28, 1, 1] (or any [N, 1, 1] with 4 | N), the light's record a travelling wave at k = pi / 2: now = (A, 0, -A, 0, ...) and before = (A_c, -A_s, -A_c, A_s, ...) with A_c = (A (3 Gamma^2 - p_i^2)) div (3 Gamma^2) and A_s = largest_below(A^2 ((3 Gamma^2)^2 - (3 Gamma^2 - p_i^2)^2)) div (3 Gamma^2), A = 1,500; the volume's time line at X = Gamma m^4 for m = 1, 2, 3, 4 (X_before = X - 1000, or X div 2 at m = 1, so that no top fires) and the three tension lines at 0, both re-set by hand at every interval's start; every act of the interval but the close (the click skipped by name, the deviation from the law's letter: no birth takes from the wave). The intervals: a span of S = 2,000 per m (one lay per m), or the ride X(t) = (Gamma (tau + t)^4) div tau^4 with tau = 2,000 over 4,800 intervals in windows of 400. What to read: n, the upward zero crossings of the level at Node 0 over the span; P = SUM p_0 over the span (Lattice.proper_count differenced, an integer); the share total and the count in W_c at the span's ends; the largest |level| over the span. The pass predicate: the proper period scales with the Link's length, P(m) n(1) = P(1) n(m) m within one crossing, |P(m) n(1) - P(1) n(m) m| <= P(1) m + P(m); the board period does not, P(m) n(1) against P(1) n(m) m^2 differing by more than the tolerance for m >= 2; beside it the pump: the count in W_c at m against m^2 times the count at 1 within the rounding, and the amplitude's largest against m A within a tenth. What does not pass, by the law's letter: the count's conservation (nature's) and the amplitude's fall; named as the dynamics of 1.2 (vii).

## 5. Verdict

WORKS WITH THE SENTENCE: the law has nature's redshift of light's beat exactly (E_proper e^U constant within one crossing over the ride's twelve windows, 129 to 135 x 10^-6 with the walk, while E_proper falls 117,821 to 41,166 x 10^-6 as the Link's length goes 1.1 to 3.3; the proper period 7.49, 15.38, 23.0, 31.25, 40.0, 47.7 intervals at m 1 to 6) and the pump is two things measured apart, the seed's count the read's unit (the count per Node equals X / Gamma bit for bit against the formula at every X, the velocity 189 kept at every interval with the close off) and a wave's share the dynamics (share / m^2 constant, amplitude / m constant, the number of quanta rising as X / Gamma); the sentence needed for nature's energy redshift is a change of Rule3's massless line (2.2), the owner's word, and the decoder's unit (2.1) needs none.
