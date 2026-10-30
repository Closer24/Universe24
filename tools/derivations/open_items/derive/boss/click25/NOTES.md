# click25 working notes (saved as I go; the derivation goes to CLICK25.md)

Order (the lead's word, mid-task): 1 the clock's click at a moving 00 slot and the moving-clock defect
(terms 5, 9, 13 blocked); 2 what the click counts and its books; 3 handedness last, OPEN by name if short.

## Read so far
- engine: step.py (gear, drive, sources, driven, weight, teeth, tick, mirror, untick), carry.py (carry, flip, lit),
  contract.py, mesh.py, kinds.py, state.py, load.py, board.py, rewind.py, rounds.py.
- ARCHITECTURE.md whole; SYM24.md (second text), READER_PHYS.md (sym24), drift.py, candidate.py, plan.py, common.py;
  TERM11.md second text and its two readers.
- clockclick/ does not exist in the scratchpad (nothing stands there).

## The defect in one line (from SYM24 Algebra)
r+ is kept in W (the teeth this round read), the next round reads it in W+ = W(a+). The image a turn needs is
W+ - 1 - r+; the turned run holds W - 1 - r+. Mismatch W - W+ wherever the 00 slot moves. Mirror shares it.

## Layer 1 (moving clock), the algebra worked out before the probe
- Uniqueness: at a fixed reading teeth W the only map phi on [0, W) with carry(-n, W, phi(r)) = (-q, phi(r')) for all n
  is phi(r) = W - 1 - r (phi(r) + r constant, range forces W - 1). So the negated row's tooth MUST be flipped in the
  READING round's teeth; the kept tooth then is W_read - 1 - r', and the next round reads at W+ and needs W+ - 1 - r'.
  Mismatch W - W+ : no definition of the turned state mends it; the act must carry the tooth from W(b) to W(a).
- The flip-covariant carry-over: the tooth as a HALF-TOOTH position u = 2 r + beta in [0, 2 W(b)), kept at the
  before slot's teeth; the act shifts it by W(a) - W(b) (half-teeth), reads r = u div 2, beta = u mod 2, carries at
  W(a) as built, keeps u' = 2 r' + beta in [0, 2 W(a)). Check: flip then shift = shift then flip, bit for bit, for
  every dW (odd included). Equivalently the whole act is one carry at doubled teeth:
  q, u+ = carry(2 W(a) (a - b) + 2 push, 2 W(a), u + W(a) - W(b)).
- The mirror: (b, a, W(a) + W(b) - 1 - u): an involution on a moving clock; untick = mirror tick mirror exact.
- Run back of the act as built is ALREADY exact on a moving clock (untick's docstring says so); what is lost there is
  mirror.mirror = id and "one mirror about n ticks". Both return with the half-tooth.
- The drift: the tooth read is r_kept + (beta + dW) div 2, so the row-sum books gain + N dW / 2 per round which
  cancels the bias sum R_t (1/W_t - 1/W_{t-1}) to first order. Expect S bounded like the control.
- The (d_t W)(d_t a) term (momentum form W(b)(a-b)) is NOT time-symmetric: the run back would need the future's teeth.
  So the second-difference form (velocity kept on a free gear) is forced by the exact run back + one pass. G2's.
- The clock's click: q_c, beta' = carry(dW, 2, beta); r -> r + q_c. "Not odd": q_c(beta) + q_c(1 - beta) = dW; a
  translation of the dial, where the 48 act on the dial by the flip or the identity.
- Falling clock: breaks where u + dW < 0 or >= 2 W(a): both sides of the zero mark; OPEN as before (G2).

## Words received mid-task (to fold, the moving clock still first)
- The owner (via the lead): "In the clicks, think clocks; do not think quantum... clocks connect and come apart, and
  the aim of the system is that clocks connect. That is what clicks are for." Base: a click is the event where two
  clocks connect (a hand of one meshing with a hand of the other) or come apart; it counts the whole turns passed
  from the giver's dial to the taker's at the meshing; no energy or area quantum in itself; energy and momentum are
  read afterwards in the clicks' spacetime. Say what this makes of: the click beside the 24; its handedness; the
  clock's click at a moving 00 slot; the key; three clocks sharing a click.
- Big Pic (6525679128 item 1, 6525978806 item 2), TO TEST not to take: (1) the click counts the law's wind,
  D = now^2 - next x before (line 1021), every train has one; the net turn (U(1)) stays the charge's count; (2) it
  clicks where the forward and backward runs part (D given or taken), not D held; a steady beat has the same D both
  ways: the vacuum's quantum, never clicks (decision 40 (g)); (3) count the click tooth from its key's middle, as the
  gear's, so no odd key is needed (line 100 stays); is the key one notch of the clock?; (4) parity: the conversion
  click chooses its list by the converting quantum's helicity (re x im) . p; the 24 keep the sign, the reflections
  flip it; the click pushes nothing so the board keeps the 48; (5) the owner's word frames all.
- My output is the base of term 11's third text. Small files.

## Probe 1 result (probe_clock.txt, 8 rounds, J = 0)
- standing W = 10: built 24x8, half-tooth 24x8, both mutants 24x8 (nothing to tell at a standing clock).
- rising by 1 (odd dW): built [24, 3 x7]; half-tooth [24 x8]; mutant no-shift [3 x8]; mutant whole-change [3 x8].
- rising by 2 and by 3: the same pattern (built 24,3,3..; half-tooth 24 x8; mutants 3 x8).
- mirror twice = state: half-tooth True on every lay; built False on every moving lay (True standing).
- n unticks return the start: True for both acts (the run back as built is already exact on a moving clock).
- one mirror about n ticks returns the start: half-tooth True; built False on every moving lay.
- counts within 9 bits.

## Probe 2 (drift, 40 rounds, rising by 1 from W = 10) and probe 3 (48, evenness, laid plan)
- Drift, the 14 moving rows together at rounds 10/20/30/40: built -189/-273/-336/-371; half-tooth -62/-63/-56/-62;
  standing control -77/-76/-80/-81. |S - S0| at most: built 15/23/27/29; half-tooth 7/6/9/6; control 8/9/11/8.
  t1's three rows under the half-tooth: (-5, -5, -3) at round 40 against built (-28, -24, -26). The drift is mended.
- The 48 at J = 0 on the rising lay, 6 rounds: half-tooth 24 of 24 under g and 24 of 24 under u; built 0 of 24 (g).
- Not odd: q_c(beta) + q_c(1 - beta) = dW, 0 misses over dW in [-9, 9], beta in {0, 1}.
- Plan 1 laid (s = 3, T_k = 2, T_d = 5): standing W = 9: built 24 x4, half-tooth 24 x4, mutant (epsilon entry + 1)
  4 x4; rising by 1 from W = 9: built [24, 3, 3, 3], half-tooth [24, 24, 24, 24], mutant 4 x4; counts 93-96 bits.
drift done: 0

## Probe 2 tail: the row-sum books under the half-tooth act: 0 misses over 18 rows x 40 rounds; the clock's clicks
summed 9720 = 486 gears x 40 teeth / 2 (one whole tooth per two half-teeth of the clock's rise). Falling clock: as
built breaks before round 1, half-tooth at the lay already (178 of 486 gears carried below 0: the teeth near the zero
mark); neither act mends a falling clock (G2, OPEN as before).

## Probe 4 (probe_wind.txt, Animate's world, 6000 rounds, g = f div 10)
- D_L(lay) = 5,000,250,000 counts^2; W (D_L + D_M) moves by at most 264 millionths over 6000 rounds (the vertex's
  wind held once in each hand by Euler's theorem; the rest Rule3's turn).
- IDENTITY: tau_D,L + tau_D,M = -(S(t,t+1) - S(t-1,t)), S = g (L_t . M_t+1 + M_t . L_t+1): 0 misses of 6000.
- The area's tau_L + tau_M = 0: 0 misses of 6000.
- |W dD_M - tau_D,M| at most 2696 millionths of a key in a round (Rule3's turn): the work is the exact form, dD is not.
- The wind's click (key = W D_L / 7 made odd): counts -6 / +6, books miss in 46 rounds of 6000, the taker 0..7;
  with the meshing's S booked the books close (-dS at the end -2 thousandths of a key).
- The area's click: -6 / +6, 0 misses, the taker 0..7. Both: the taker holds a winding ~4920 rounds of 6000, the
  clocks connect 3 times.
- The giver on a line, the taker at rest: the wind's click takes 7 windings (count 6, 68 misses); the area 0 clicks.
- The wind's click tooth runs back by the lemma (checked).

## Big Pic's further words (6526070842 item 2, 6526201692 piece 4), to test
- The click as an escapement: counts the whole turns a hand passes to another, EACH SENSE APART; the sum of the
  senses = the law's wind (quanta), the difference = the net turn (charge); a line hand clicks by its sum, no charge;
  books hold sense by sense; Planck's n -/+ 1/2 closes as wording (the tick is whole, the hand is not).
- My test: the two senses are the hand's two eigen-turns; their areas sum to E / (2 W sin omega), which is no whole
  number (a root), and differ by Omega, whole. The whole forms are D = E / W^2 (the wind) and Omega (the charge): the
  escapement's sum is the wind only as D. Sense-by-sense books hold for the common-turn vertex by symmetry (the
  vertex does not mix the senses), but cannot be COUNTED exactly on the act.
- Handedness piece: the conversion click reads one hand by the quantum's helicity h = (re x im) . p (the epsilon
  table on the hand's two parts, dotted with the gradient along the Mesh): a pseudoscalar the readings and the tables
  already hold; OPEN by name; what it needs from the half-speed gear: the two parts (re, im) as T1 and the travel p.

## The owner's word (15:3x): the click counts D given or taken, never held. Derivation sketch (probe_count.py):
- A hold of the previous count in the state breaks the exact run back (a one-round state cannot restore n(t-1) from
  s(t+1): D(t-1) needs a(t-2)). So n_h(t) = (D_h(t) - D_h(lay) + k_0) div key is a FUNCTION of the round (now, before
  and the round's own next), the same in both runs (D is even under the mirror), and the click is the change of n
  between two rounds, written by the runner (which alone sees two rounds). D_h(lay) is the held wind (40 (g)), the
  one constant per train per Node-clock from the lay; k_0 = (key - 1) div 2 the birth at the half.
- Books: D_L + D_M = the act's invariant up to Rule3's turn; Euler puts the vertex's share once in each hand, so no
  third hold; misses only where Rule3's drift crosses a key boundary.

## Probe 5 (probe_count.txt): the owner's count on Animate's world, 6000 rounds, key = D_L(lay)/7 odd = 714,285,715
- giver -6, taker +6, the taker 0..7, 35 click rounds; books miss in 2 rounds of 6000; n_L + n_M in {-1, 0}.
- D_L + D_M drifts <= 1854 millionths of a key over the run, <= 3351 in one round (Rule3's turn): the cause of both.
- the taker's D read on the backward run = forward's at 6000 of 6000 (D even under the mirror).
- free hand: 0 clicks over 6000 rounds, its wind within 1855 millionths of a key of the lay's (born at the half).
- the giver on a line, taker at rest: the taker's count 0..7, 4 misses; the area 0 throughout (charge 0, wind passes).
done: 15:37 UTC

## 16:2x: term 11's count NOT PASSED (t11_math/REPORT.md, t11_phys/REPORT.md). Blocking:
- M1 the books of the per-Node-clock D-count fail at a steady rate (the wobble over the exchange per round); break
  cases: g = f/100 (4 misses of 5 click rounds), A = 1e5 (44 of 60), 1e4 (388 of 433), 1e3 (free hand clicks 4731);
  60,000 rounds: 40 of 355. Fix: count the exchanged wind X_M = g SUM (b_M a_L - a_M b_L), X_L = -X_M by construction;
  tooth per train at key_w: 0 misses, k_L + k_M = key - 1 always, the free hand's X = 0.
- M2 "no hold survives the run back" is false for a carried tooth of an odd increment: kept (not flipped) under the
  mirror, carry(-X, key, k+) = (-q, k). The law's (iii) read by the increment's parity.
- M3 a per-Node-clock D clicks on free travel (chain of five: hands 1-4 click as the wave passes); the law line
  dropped "its six neighbours".
- P1 one key of wind for the board = one energy per click at every beat, not Planck (7 counted at f, 4f, 16f while
  the areas stand 1 : 1/2 : 1/4). Fix: the key per train, K_D^2 W^4 = 4 f (2W - f) K_a^2 (a ratio of whole numbers;
  the nearest whole number on the train card at load); light has no own beat and is debited by the taker's quantum.
- P2 the state-function count clicks on free propagation through Meshes (ring: every Node-clock a packet crosses
  clicks +1,+1,+1,-1,-1,-1; 282 click lines per lap; light through a sea of bobs 945 lines, the bobs 0). Fix: count
  what the vertex passes, tau_D or X; run it on a board with Meshes.
- P3 D_lay is not 40 (g); set D_lay = 0 (with the exchange count there is no D_lay at all).
- Parity of the key (both): the books need an odd rounding; the floor carry with one shared birth is odd only at odd
  keys; EDGE's centred split with ties even is odd at every key at the cost of a tie counting 0 or 2; odd key CHOSEN.
- Minors: M4 identities marked as checks, cite probe_count's numbers; M5 the click reversed on the run back; |q| can
  exceed 1; the law's (i) birth key div 2; 40 (g) is the coupling family's; M6 push, not J; two conditions; M7 two
  Rule3 terms; M8 no dial where none is kept; M9 the key's scaling with W. P4 D per Node-clock not positive (the time
  Wronskian, kept in sum); P5 three trains: which term makes it whole is OPEN, not term 12; P6 momentum P = the space
  Wronskian across the Mesh, the recoil needs a taker with a stride (G3); P7 misses are one-round transits; the
  flicker scales as A/key; P8 the line train's sense is term 12's draw; P9 handedness: chirality not helicity, confine
  to the weak conversion, h = 0 cases, frame dependence; P10 two sentences.
- Both readers: the physicist's "half of S booked into each hand" equals (X(t) + X(t+1)) / 2: the two forms are one.

## Probe 6 (probe_x.txt, the exchange count X = SUM a J(b) - b J(a), 6000 rounds each)
- A the pair: SUM X = 0 in 6000/6000; |W dD_M - X_M| <= 2607 millionths of key_w; totals -6/+6, taker 0..7, 34 click
  rounds, 0 misses, k_L + k_M = key - 1 at 6001/6001; run back: X odd 6000/6000, tooth KEPT returns 6000 with -q 6000,
  FLIPPED 0; the D-count on the same run: 2 misses. Planck in whole numbers: key_X^2 W^2 / (4 f (2W-f) key_a^2) =
  1.000625; the loader's key from key_a 71406246511186446276006877897 vs key_w 71428571400000000000000000001.
- B1 g = f/100: 3 clicks, 0 misses; B2 g = f/300: 0 clicks; B3 A = 1e5: 0 misses; B4 A = 1e4: 0 misses (D-count 388);
  B5 A = 1e3: 0 misses, taker 0..6; B6 key/700 at g = f: |q| <= 10, 5793 click rounds, 0 misses; B7 key/7000:
  |q| <= 93, 0 misses; B8 three hands g, g: 73 misses, sum in [-1, 1]; B9 g, g/2: 64 misses, sum in [-1, 1].
- C free hand SUM |X| = 0. D line giver: taker 0..7, 0 misses. F1 taker 1.1 f: one key 0 misses (totals -2/+2, 0..4);
  Planck's keys per train: 46 misses (the counts part, the wind's books exact). F2 1.01 f: 0 misses / 62 misses.
- G cubic term g3 = g/1e6: SUM X != 0 in 5993/6000; k_L + k_M != key - 1 at 5993/6001 (the invariant lost; 0 misses
  only by the term's size).
## Probe 7 (probe_xring.txt): (a) free travel, no vertex: SUM |X| = 0, 0 click lines (the D-count 570 over 96 rounds);
(b) the sea of bobs: X_light + X_bob = 0 at 19200/19200 site-rounds; key div 7: 0/0 lines (645 thousandths of a key
over the sea); div 700: 1977 = 1977 lines, 0 misses; div 7000: 11850 = 11850, 0 misses; (c) the cube, plan 1, rising
clock, half-tooth act: X per train per site turns with the 24: 24 x4 (536 train-sites not 0).
## Reruns: all five first-text probes byte for byte (probe_clock once its two captured stderr lines are dropped).
second text done: 16:32 UTC

## 16:5x: the mathematician's second round (t11_math/REPORT2.md, probe_g): items 1, 2 CLOSED; item 3 NEW blocking:
the travel test ran an empty plan; a derivative vertex V = g SUM M_s (L_{s+1} - L_{s-1}) breaks the per-site identity
(18,756 of 19,200 site-rounds), 0 over the ring: a flux through the Meshes; a free train whose plan reads the force
writes 437 lines in 96 rounds. Fix (a) restrict the identity to legs read at the Node-clock; (b) "carried by the pull
passes nothing"; (c) name the derivative vertex and the force reading as the break beside the cubic; (d) say what the
term needs if G3 reads gradients: the Mesh flux booked or the exchange counted at the Mesh. N1 the cubic has no exact
exchange even in exact arithmetic (say so, not "G3's question"); N2 "a vertex laid from one potential"; N3 A = 1e3 is
bookkeeping without a wind; N4 the 46/62 misses are forced by construction, not found.
## Derived for the third text: for a two-leg term f y_s (x_{s+1} - x_{s-1}) the per-site imbalance X_x + X_y equals
Phi(s, s+1) - Phi(s-1, s) with Phi(s, s+1) = f [(a_x(s) b_y(s+1) - b_x(s) a_y(s+1)) + (b_y(s) a_x(s+1) - a_y(s) b_x(s+1))]:
the two trains' Wronskian across the Mesh, odd under the mirror. For the force self term V = (G/2) SUM (L_{s+1}-L_s)^2,
X(s) = Psi(s, s+1) - Psi(s-1, s), Psi = G (a_s b_{s+1} - b_s a_{s+1}): the space Wronskian (the physicist's momentum P).

## Probe 8 (probe_flux.txt): G2 derivative vertex: X_L + X_M != 0 at 18,756/19,200 (his number); = div Phi at
19,200/19,200; Phi odd under the mirror 400/400; booked, X~_L + X_M = 0 at 19,200/19,200; lines div 700: unbooked
light 274 / bobs 327, 504 off; booked 327 / 327, 0 off; div 7000: 2621 / 2962, 3584 off -> 2962 / 2962, 0 off.
G3 force self term: X = div Psi at 4,608/4,608; booked SUM |X - div Psi| = 0; lines 437 and 1887 -> 0 and 0.
## The physicist's second round: PASSED; minors (a) two bob kinds: light's one tooth cannot mirror two partners
(4,514 site-rounds off at div 700): the hand with the beat writes the line, light keeps no tooth, debited by the
identity; (b) a quartic own term makes a lone hand click (218 at 40 percent): the linear spring only; (c) the line
lay at the train's own key holds 3.5 quanta, the taker 0..4; (d) unequal beats: within Delta / (2 omega) per quantum.
third text done: 16:48 UTC
