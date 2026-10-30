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
