# The final hostile mathematician on EDGE2.md (the tooth on the edge, its second text)

The report as the reader gave it, 2026-10-30, filed by the Boss (the file the reader names was not in its folder).
Files beside it: 00_first_pass_notes.md, probe_fm1_algebra.py/.txt, probe_fm2_board.py/.txt, probe_fm3_varying.py/.txt;
whole numbers, tensor24.algebra.carry.carry the one division. Note from the reader: edge/edge_lib.py changed (board()
gained integers/c00) and edge/probe_root_generic.py/.txt appeared at 17:00 UTC during the reading; EDGE2.md itself
(16:47) is unchanged and is what was judged.

VERDICT on EDGE2: PASSED (as a derivation with its CHOSEN and OPEN items named; nine MINOR items, none BLOCKING)

## Items (all MINOR)

1. Section 4 and section 5 bullet 2: the fixed-point cell counts (1,560 under no q; 119 / 10,199 under two) are the
   tie-even cells' and are called "either dial"; under the owner's half-open the cells are [2Dq-D, 2Dq+D-1], a gap
   misses (2q+1) dD integers for q >= 0, counts 1,600 / 109 / 10,099 (probe_fm1 C). Conclusion (no bijection)
   unchanged. Fix: give the half-open's numbers or say whose they are.
2. Section 4 table: "0 collisions of 573" is the centre-0 count in mc_math/probe_mc3; the half-open has 572 states, 0
   collisions. Fix: 572.
3. Section 2: "the law's k_giver + k_taker = m - 1" is not in docs/ALGEBRA.md; it is term 11's DRAFTED text
   (term11_v2/TERM11.md line 52, "k_giver + k_taker = key - 1", the key OPEN). Under the half-open at an even key the
   click's books need that paired birth, not (i)'s one birth, so section 1's "one law of the dial for every carry ...
   closes by itself" holds of (iii) only (the drive's r_d is also laid at 0 by the loader, not at T_d div 2). Fix:
   attribute to term 11's draft; narrow "one law" to the flip.
4. Section 3, root dial: "q_F = round(F / L) by rule (ii)" (half up) mislabels the probe's act, which is E.split, tie
   to even (odd under F -> -F); the deriver's own later probe_root_generic shows the (ii) rounding loses the 24 from
   round 3 on a moving clock ([24, 24, 3, 3, ...]) while an odd rounding keeps it. Fix: "dropped with the odd rounding
   (rule (iv))".
5. Section 3: "a second edge tooth for the push is the exact alternative" has no probe in the text; the later probe
   measures a push tooth kept at the pivot's dial at untick(tick s) = s 2 of 40 falling, 3 of 24 varying. Fix: strike
   "exact" or define the tooth's dial and measure it.
6. Case (vi) against (i)-(v): "a kept remainder belongs to the edge between the gear's two slots" over-generalises
   (r_d and the click tooth have no edge); "D_out = W(now) + W(next)" reads a count the round has not made: the line
   must say W(next) is the 00 row's next count given by the 00 row's own carry first in the round (today at its
   standing dial, the cut; its law OPEN by section 4), i.e. the edge round is two carries in sequence per Node-clock
   against ARCHITECTURE line 90's one act. Fix: "the gear's kept remainder" and name the 00 row's prior carry in (vi).
7. Section 3 table labels "at W x 1.86 (17,500 -> 32,500)" and "at W x 4" fit the built/edge rows; the root row's
   marks are W 15,625 -> 30,625 (x1.96) and 39,601 (probe_root A, B). Fix: label the root row's W.
8. Section 5 last bullet: the by-2 lay of probe_momentum runs 15 rounds (0 of 15, 15 of 15), not "0 of 30 ... 30 of
   30". Fix: say so.
9. The promise (W >= 1 at both slots) is sufficient, not necessary: the act is exact wherever D_in >= 1, D_out >= 1 and
   s in [-D_in, D_in-1]; measured with W(b) = -1 grip, W(a) = 5 grips and W(b) = 0, W(a) = 3 grips: 40/40 run back,
   24/24, books 0 (probe_fm2 C); one gear with W drawn in [-20, 40], 12,935 lawful rounds, 0 misses (probe_fm1 D).
   Fix: state the algebra's own condition or say the promise over-asks.

## Sound, with numbers (the reader's own probes)

- Half-open split, D in [1,30], n in [-3000,3000], 183,030 cases: n = 2Dq + s, s in [-D, D-1], one pair per n, 0
  misses; the flip n -> -1-n gives (-q, -1-s) 0 misses (the law's (iii) on m = 2D); the negation n -> -n fails exactly
  on the 11,986 ties n = D mod 2D and nowhere else; shift n -> n + 2Dk gives (q+k, s) 0 misses for k in [-3,3].
- One-sided half notch: W = 3000, k = +1500 -> 1, -1500 -> 0 as stated; at an odd W a push at rest never ties (80 tying
  pairs for W in [1,40], all at even W).
- Still clock, exhaustive, W in [1,12], all r, v in [-5,5], push in [-3W,3W], 43,758 cases: s = 4r - D reproduces the
  act as built's q and s' = 4r' - D exactly (4r' - 2W in [-2W, 2W-4]); tie-even's s = 4r + 2 - D exact too.
- One gear on courses given from outside (rising, falling, irregular, tiny dials): untick(tick s) = s and
  P' - P = 4 push 0 misses in 20,000 + 12,935 + 20,000 rounds; the flip's commutation 20,000 of 20,000.
- Board: the act written again (the 00 row's carry first, then every row at 2 D_out) equals edge_lib's half-open act
  bit for bit on 9 lays x 40 rounds; the text's three lays 24/24 at every round, untick 40/40, rewound, books 0 per
  gear, 78-81 bits; the 00 slot VARYING BY SITE (drawn per site, the 00 row pulled at 27 of 27 sites, D odd at 121-187
  of 324 gears, W not whole in grips): 24/24, 40/40, rewound, books 0 on three lays, 79-81 bits (the text did not run
  this; its claims hold there).
- Promise example: W(a) = 3 grips, W(b) = 13, v_00 = -10 grips gives D_in 16, D_out -4 grips, refused.
- Fixed-point theorem: the gap between consecutive cells is (2q+1) dD (tie-even) or (2q+1) dD + 1 (half-open); 2q+1
  is odd, so a dial moved by its own quotient never tiles the integers, in either convention and for any factor on the
  self-read.
- The readers' numbers the text cites stand in their outputs (2012/4039 vs 1012/1009 permille; 29, 64, 65 clicks; 15,
  8, 9 of 36; P_00 -4640 -> -908; 0 of 1 and 12 of 12 for two squares; about 12,500 rounds), and the physicist's
  probe_a agrees with probe_root to the digit (249, 3999, 857, 1166, 1003, 988).

## Solution24 (one line)

Step 10 should also count the act's divisions: the edge round is two carries in sequence (the 00 row's, then every
row's), and a law line that reads a next count names the carry that gives it.
