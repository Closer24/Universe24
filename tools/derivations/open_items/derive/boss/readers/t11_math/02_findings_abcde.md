# Findings from probes A to E (outputs probe_a.txt .. probe_e.txt in this folder)

## A (the text's world, W = 10^20, A = 10^6, g = f/10, key 714,285,715 odd)
- A1 the per-gear identity W D_i = W q_i v_i - a_i J_i - a_i (r_i - r_i+): EXACT, 0 misses of 72,000 gear-rounds.
  But 2 E_shadow = SUM (W q v - a J) is itself NOT kept by the act (moves 32 millionths of itself over the run):
  the act's drift is rounded, so TWO Rule3 terms stand between D_L + D_M and a constant, not one.
- A2 D on the mirrored state = D forward, 6,000 of 6,000: a theorem (untick exact + the product next x before is
  symmetric), not a measurement.
- A3 the count: -6/+6, taker 0..7, 35 click rounds, 2 misses = ONE event: t=216 the giver clicks -1 with
  x_L = -0.500432 key while x_M = +0.499655 key (delta = -776 millionths); t=217 the taker clicks +1. The books are
  open for exactly 1 round. The wobble delta in [-1855, +1712] millionths; its per-round change up to 3351 (it
  alternates fast). The taker holds a winding 4,919 rounds of 6,001, connects 3 times (text: 4,920 / 3 from
  probe_wind's tooth-carry; close but not this count's numbers).
- A4 the four rounding rules agree on this run at the odd key and at the two even keys beside it (no ties fell).

## B (cases built to pass the stated rule and break)
- B1 vertex weakened: g = f/100: 5 click rounds, 4 MISSES, books open 2 rounds (4 of 5 click rounds wrong).
- B2 swing shrunk, key a seventh of D_L each time: A = 10^5: 60 click rounds, 44 misses, open 24 rounds, wobble
  1.9% of a key; A = 10^4: 433 click rounds, 388 misses, open 248 rounds; A = 10^3: the free hand clicks 4,731
  times (count -2..1): "a clock that keeps its beat does not click" FAILS for the D-count at small swing.
- B3 long run 60,000 rounds: delta bounded (no diffusion seen, range ~[-2133, 2024] millionths in every block);
  misses 40 of 355 click rounds (11%), books open 20 rounds. The misses are a steady rate, not an accident.
- B4 g = f, key a seventieth: max |q| = 1 here (3,493 click rounds, taker 0..70, 68 misses). Need a smaller key to
  show |q| >= 2 (rerun with key/700, key/7000).

## C (the exact exchanged wind X_M = g (b_M.a_L - a_M.b_L), X_L = -X_M by construction)
- |W dD_M - X_M| <= 2607 millionths of key_w per round, |W dD_M - tau_D,M| <= 2696: both are W dD up to Rule3's
  turn; X is the one that is exactly antisymmetric in the pair.
- The X tooth-carry (born (key_w - 1) div 2, key_w odd): -6/+6, 0..7, 34 click rounds, 0 misses, k_L + k_M =
  key_w - 1 at 6,001 of 6,001; the taker's X-count EQUALS the D-count at every round at A = 10^6 and is within 1
  at A = 10^4 (where the D-count's books miss 388 times). The free hand: X = 0 exactly, 0 clicks at any swing.
- Run back by the act alone: the mirrored round's X is -X; with the tooth KEPT the tooth returns 6,000 of 6,000 and
  the quotient is -q; with the tooth FLIPPED (law (iii)) 0 of 6,000. So a held tooth per train SURVIVES the run back;
  "no hold survives the run back" is a straw man (it is true of a held COUNT n(t-1), not of a carried tooth).

## D (parity): floor rules (CLICK25's and the law's (i)): 0 misses at odd keys, 120 at even keys (4,960 cases);
EDGE's ties-to-even and the law's (iv) half away from zero: 0 and 0. EDGE's split as a tooth-carry born at 0:
0 misses of 44,640; the plain carry born at (key-1) div 2 on the same data: 1,598 misses at even keys.
CLICK25's half-tooth prediction (miss iff 2x + key = 0 mod 2 key) agrees 4,960 of 4,960. SETTLED: both texts are
right about their own rule; the parity condition is the floor carry's, not the count's.

## E (a train over five emulated Node-clocks): hands 1..4 (D_lay = 0) click 12 to 15 rounds each as the wave
arrives (first clicks at rounds 218, 632, 1056, 1416); the five counts' sum in [-1, 1]; 66 rounds where the clicks
do not sum to 0; the whole train's wind kept to 2,072 millionths of a key. A train that keeps its beat as a whole
clicks at every Node-clock with the per-Node-clock D-count.
