# Hand dn1: the record's den beyond 128 bits, what it solves and what it costs (2026-10-25)

Worktree branch hand-dn1 at d55de5aae of engine-5.0-test; David's toy (toys-5 at 906122264) copied under tools/derivations/open_items/H-Den-Beyond-128-Bits-1/toy/ and never edited; this hand's scripts, files and outputs under tools/derivations/open_items/H-Den-Beyond-128-Bits-1/ (den_record.py, run_toy.py, laws.py, read_clicks.py; universe_record.json, universe_control.json, universe_record_T.json; the world files world_{record,control,recordT}_{hole3,hole5,bodies7}.json; out/). Python /home/user/Universe24/venv314/bin/python with PYTHONPATH=<worktree>/src, TMPDIR=/dev/shm/tmp. Integers only in every script (quotients with remainders, bit lengths, counts; the one float-free pi is the integer 6283185 per 10^6 in one labelled reading of the expected beat). No edit of src or of the toy; no commit; no push; every kept file under 1.5 MB (the one record above it, the 5-cube at the record's den with 539 credits, kept whole under /dev/shm/tmp/dn1_record_hole5.json and truncated to 200 log lines in out/).

The owner's word: "den need not stay within 128 if it solves many things". The law's letter (ALGEBRA.md, The Node): every integer of the state and of every act's transient within 128 bits; den the one exception, "its size bounded by the transients it makes, Rule3's total and the walls, which stay within 128"; the former sentence, den bounded by the width (w = 6 den Gamma^2 G^2 within 128 bits, den near 2^101 at Gamma 1,000 and G 16), kept by name. At the record's den (154 bits) the walls are 185 bits: the letter as written is broken there, and the owner's "if" asks what is bought. Below, every item measured at the record's den and at the control (the toy's own den, 54 bits), with the script and the command.

## 0. The two dens and the lay (den_record.py; `PYTHONPATH=src python tools/derivations/open_items/H-Den-Beyond-128-Bits-1/den_record.py`, outputs den_record.json, den_record.txt)

The record's den 21397363965165989151899244775347635252768274397 (154 bits) = 8909066857637 (44 bits, 2984806^2 + 1^2) x 79961009336473 (47 bits, 8942092^2 + 3^2) x 30036532038439967297 (65 bits, 5480559464^2 + 1^2), all 1 mod 4; 26 points in the open quadrant, 3 lifts (loader/circle.lift_points, the engine's order, the toy's file order): (0,0,2) the electron's, (0,2,0) the neutron's, (2,0,0) the proton's. The control den 15162856759112389 (54 bits) = 617 (19^2 + 16^2) x 196613 (338^2 + 287^2) x 124992409 (11180^2 + 3^2); 26 points, 3 lifts in the same order. The universe files in the toy's format: integers den, node_clock 1000, quantum_action 36000, link_unit 16; the rows light (den, den) shape 2, the three lifts shape 2 in lift_points' order, the volume holder shape 10 at (den - den div 1000, den), the sign shape 4 at (den, den), the phase row shape 1 at the wall 2 (the toy's rule for the held rows). The worlds: the hole seed (the sea on the massless row, the hole at the origin, one quantum more at (1,0,0)) on the 3-cube for 120 intervals and the 5-cube for 120; the bodies' seed (two conjugate-pair packets of the heaviest lift by its gap, the proton's (2,0,0) at the record's den, (0,2,0) at the control, 125 quanta each, width 2, at (3,3,2) and (3,3,5)) on the 7-cube for 60; the same worlds at the record's den with T raised to 2,740,279,732 (section 2e, the mend).

## 1. SOLVED or not, each with a number

### 1a. The three lifts' pairs and their leg ratios

| | the record's den | the control den |
|---|---|---|
| electron's lift: num bits / s bits / g | 154 / 123 / 66 per 10^18 (0 per 10^15) | 54 / 43 / 144,008,745 per 10^15 (0.000144) |
| proton's lift: g | 224 per 10^15 | 829 per 1000 |
| neutron's lift: g | 225 per 10^15 | 837 per 1000 |
| p over e (legs) per 10^9 | 1,836,152,655 (nature 1,836,152,673; miss 18 per 10^9) | 1,836,153,562 (miss 889 per 10^9) |
| n over p (legs) per 10^9 | 1,001,378,424 (nature 1,001,378,419; miss 5 per 10^9) | 1,001,377,773 (miss 646 per 10^9) |
| n over e per 10^9 | 1,838,683,653 | 1,838,683,366 |

SOLVED at the record's den: the three ratios to 18 and 5 parts in 10^9 (N2's finding reproduced from the engine's lift_points and sine_den). The control den holds the same ratios to 889 and 646 parts in 10^9: three primes 1 mod 4 with the sines in nature's ratios exist at 54 bits to one part in a million; the record's den buys three more decimal places, from 10^-6 to 10^-8 or 10^-9.

### 1b. The births (run_toy.py on the hole seed; `python tools/derivations/open_items/H-Den-Beyond-128-Bits-1/run_toy.py world_record_hole3.json out/record_hole3.json back 120`, and the control, and hole5 with back 60; the clicks read by read_clicks.py)

| | record 3-cube, 120 | control 3-cube, 120 | record 5-cube, 120 | control 5-cube, 120 |
|---|---|---|---|---|
| births | 11 (e 5, p 5, n 1) | 10 (e 5, p 4, n 1) | 22 (e 6, p 4, n 12) | 22 (e 5, p 5, n 12) |
| births' intervals | 6 to 20 | 6 to 19 | 6 to 16 | 6 to 17 |
| senses' sum (the charge) | 0 | 0 | 0 | 0 |
| every lift born as its conjugate pair (conversion.birth_of) | yes, 3 lists, the lightest first | yes, 3 lists | | |
| body credits | 44 | 49 | 539 | 28 |
| the draw's room | 173 bits on 11 of 11 | 73 bits on 10 of 10 | 173 bits on 22 of 22 | 73 bits on 22 of 22 |

SOLVED alike at both dens: the three lifts are born as conjugate pairs with the senses summing to 0; the counts are the same within one or two. Not a gain of the record's den. The born child's amplitude differs (1d, 2e): at the record's den every child is laid at one level.

### 1c. The conversion lists: does the law's exact list give n -> p + e? (den_record.py: conversion.birth_of, conversion.lists_of on the loader's families at each den; this hand's enumeration of a plane parent's exact lists by the clause of conversion.py, the children's Gaussian product equal to the parent's point scaled by den^(children - 1), the senses summing to the parent's, up to 3 children among the 26 points)

Derivation. The lift of the prime pi_k has the vector 2 e_k, the angle 2 theta_k turned into the quadrant by a unit; the point with vector v has the angle SUM v_i theta_i plus a quarter turn; the conversion's exactness (the Gaussian products agree once scaled) is the equality of angles, which for primes of irrational angles holds iff the exponent vectors agree, children's signed by their senses, and the units' turns agree. v_n = (0,2,0), v_p = (2,0,0), v_e = (0,0,2): no signed sum of v_p and v_e gives v_n, so n -> p + e is no exact list at ANY three-prime den; the third child needs the vector v_n - v_p + v_e = (-2,2,2) (or v_n - v_p - v_e = (-2,2,-2) by the senses), a composed point, no lift, never born.

Measured. At the record's den: the engine's lists_of for two massless quanta (bound 2): 26 lists, every one a point's conjugate pair; birth_of: the three lifts' pairs, the lightest first. The plane parent's exact lists up to 3 children: electron 75 lists (48 irreducible, none of two children), proton 90 (63), neutron 111 (84); two-child irreducible lists: 0 for every lift; lists holding both the proton's and the electron's lift: 2 for the neutron parent, [point (-2,2,2) +1, electron -1, proton +1] and [electron +1, proton -1, point (2,2,-2) +1]; 0 for the proton and the electron parents. At the control den: the same counts (75 / 90 / 111 across the three primes by leg), two-child irreducible 0, lists with both p and e for the neutron parent: 1, [point (-2,2,2) +1, electron -1, proton +1]. NOT SOLVED by den's size: the conversion n -> p + e + X exists at both dens with X a composed point of the same den at the sense +1 (the Gaussian identity's third factor, where nature has the antineutrino), never a two-child list; the record's den adds one list by its units' turn and nothing else. The charge in the law's letter: the neutron's lift at sense +1 carries the charge +1 (a plane's Wronskian), so the list is +1 -> +1 - 1 + 1; nature's neutron is neutral: the sense of a lift is not nature's charge at any den (N2's tension, measured again here).

### 1d. The gap of each lift, G's window, the bodies' seed (run_toy.py on the bodies' worlds, 7-cube, 60 intervals, back 20)

g = (den - num) / den: the record's den 66 per 10^18 (electron), 224 and 225 per 10^15 (proton, neutron); the control 144 per 10^9 (electron), 829 and 837 per 1000. G's window for a one-Node body 0.616 to 0.72: no lift of either den stands in it (the record's heavy lifts 10^12 below the window, the control's heavy lifts above it by 0.11 to 0.12). Compton lengths (isqrt(den^2 / 3 s^2), milli-Links): 1,582,101,240,925 / 861,639,273 / 860,453,203 at the record's den (10^9 and 10^6 Links; the board is 7); 1,075,796 / 585 / 585 at the control.

The two packets' share within one Link of each lay centre (per mille of the plane's weight re^2 + im^2) by interval:

| interval | record (T 36,000) | record (T 2,740,279,732) | control |
|---|---|---|---|
| 1 | 500, 500 | 99, 99 | 99, 99 |
| 2 | 0, 0 | 142, 142 | 375, 375 |
| 5 | 166, 166 | 7, 7 | 382, 382 |
| 10 | 166, 166 | 39, 39 | 372, 372 |
| 20 | 36, 36 | 12, 12 | 324, 324 |
| 40 | 70, 70 | 3, 3 | 449, 449 |
| 60 | 11, 11 | 41, 41 | 454, 454 |
| Nodes with levels at 60 (of 343) | 289 | 343 | 307 |
| the packet's weight bits at interval 1 | 4 | 21 | 18 |

Plainly: at the record's den the bodies' seed DISPERSES over the whole board within 20 intervals (11 per mille within one Link at 60; at T 36,000 the whole 125-quantum packet is laid at a weight of 2^4, one level per Node, so what disperses is the rounding; at the raised T the packet is resolved, 2^21, and disperses as a free packet, 7 per mille by interval 5). At the control den the two packets STAND (454 per mille at 60, from 375 at interval 2; 307 Nodes carry levels, the tails) with no turn (0 swaps) and 232 body credits. Binding is the gap's, and the gap is den's structure (the primes' angles), not den's size: nature's ratios at the record's den come with angles of 10^-7 and 10^-10, so g is 10^-13 and no body stands.

### 1e. The mass ratios from the clicks (read_clicks.py: the beats on the credit lines against the header's legs)

The beat of a rest rotation is 2 pi den / s intervals (the law's rotation by num/den per interval): expected at the record's den 17,217,684,507 (electron), 9,377,044 (proton), 9,364,132 (neutron) intervals; at the control 11,705 / 6 / 6. Measured on the credits: record 3-cube: the lightest lift 31 credits every one at the beat 2, the middle lift 13 credits at 9 to 23, the heaviest 0; record 5-cube: 536 credits of the lightest lift at beats 2 to 35 (median 4), 3 of the heaviest at 51 to 52; control 3-cube: 49 credits of the lightest lift at the beat 2; control 5-cube: 25 at 2 (lightest), 3 at 5 (middle; expected 6). The decoder's species solve (gate 8): record 3-cube 0 of 44 right (electron read as massless 12 and as neutron 19, proton as neutron 6 and massless 7), 5-cube 3 of 535; control 22 of 49 and 15 of 28. Gate 19 in the decoder is a fit of den's legs, not a reading of the beats. NOT SOLVED: at the record's den a beat of 10^7 to 10^10 intervals is unreadable in any run of this toy (at 12 ms per interval on the 3-cube, 9,377,044 intervals of the proton's beat take 31 hours; 17,217,684,507 of the electron's, 6 years), and the beats the credits carry (2 to 52) are the rounding's flips of a one-level record, not the rotation: the ratio of the lightest lift's beat to the middle's reads 153,846 per 10^6 against the legs' 1,836,152,655. At the control den the middle lift's beat 5 against the expected 6 is within one interval, the lightest lift's 2 against 11,705 is the same rounding flip (its one-quantum amplitude is 5 levels).

## 2. COST, each with a number

### 2a. The bit length of every class of integer (run_toy.py's census at the end of the 3-cube and 5-cube hole runs; the walls from den_record.py)

| class | record's den | control den | within 128 at the record's den |
|---|---|---|---|
| den | 154 | 54 | no (the exception) |
| w = 6 den Gamma^2 G^2, the rotation wall of every line | 185 | 85 | no |
| W_c = 3 den T, the light's quantum | 171 | 71 | no |
| the one-Link read's modulus 3 W_c | 173 | 73 | no |
| the volume's time write wall 54 den Gamma^4 T | 215 | 115 | no |
| the volume's axis write walls 54 den T Gamma^2 | 195 | 95 | no |
| the sign's write walls T, the phase wall 2 | 16, 2 | 16, 2 | yes |
| the lifts' quanta 3 T s | 140, 151, 151 | 60, 71, 71 | no |
| the mass D = 12 gap Gamma^2 G^2 at the vacuum | 122, 144, 144 | 63, 86, 85 | 122 yes, 144 no |
| the reach R = 2 num Gamma^2 G^2 | 183 | 83 | no |
| the rotation remainders (every line, in [0, w)) | 184 to 185 | 84 to 85 | no |
| the write remainders: volume row / sign row / light row | 215 / 15 / 15 | 115 / 16 / 15 | volume no, others yes |
| the levels now and before: volume / light / lifts / sign / phase | 18 / 14 / 4 to 5 / 0 / 0 | 18 / 14 / 7 to 8 / 6 / 12 | yes |
| the counters (standing, crossed, beats, proper, closes) | 16 | 16 | yes |
| the phase pair's amplitude X and the orbit table | 39 | 39 | yes |
| the Links' count K | 0 | 10 | yes |
| Rule3's transient (the flux line's total before the division) | 205 (3-cube), 207 (5-cube) | 105, 107 | no |
| the credit's frame integers | 182, 184 | 81 | no |
| the birth's numbers (taken, booked, room) | 173 | 73 | no |
| the largest integer of the state | 215 | 115 | no |
| the clock's memo's running fraction (K-S4) at the content filled, 3,095 | 30,860 / 30,855 | 30,860 / 30,855 | no at both (den-free) |
| integers per Node (arrays of the state) | 98 | 98 | fixed |

At the control den every integer of the state and every transient but the memo's fraction stands within 128 bits (115 and 107); at the record's den every integer that carries den as a factor stands beyond it: the walls (171 to 215), every rotation remainder (185: 25 lines x 185 bits is the bulk of the Node's width), the volume's write remainders (215), Rule3's total (207), the credit's frame (184), the births' numbers (173). The levels themselves stay within 18 bits at both dens. The largest is the volume's time write wall and remainder, 215 bits (231 at the raised T). The rule "den the one exception" must read "den and every integer that carries den as a factor: the walls, the remainders, Rule3's total, the quanta, the reach and the mass, the credit's and the birth's numbers": 18 of the 24 classes above.

### 2b. The time per interval (run_toy.py, integer milliseconds)

| cube, intervals | record's den: min / median / max / mean per interval, total | control: the same | milli-ms per Node-interval record / control |
|---|---|---|---|
| 3-cube, 120 | 7 / 12 / 56 / 12, 1,516 ms | 6 / 11 / 27 / 11, 1,415 ms | 467 / 436 |
| 5-cube, 120 | 10 / 25 / 54 / 27, 3,261 ms | 11 / 28 / 57 / 28, 3,372 ms | 217 / 224 |
| 7-cube bodies, 60 | 23 / 34 / 58 / 34, 2,077 ms | 21 / 33 / 59 / 33, 1,992 ms | 100 / 96 |
| the run back: 120 / 60 / 20 intervals | 1,037 / 888 / 516 ms | 815 / 862 / 639 ms | |

The time cost is within 10 per cent either way in Python's integers (object arrays): the toy's cost is the interpreter's, not the digits'. In a machine of 128-bit words the record's den does not fit at all (215-bit walls and remainders): that cost is the whole engine, not a factor.

### 2c. The run back exact and the 48 (run_toy.py back N; laws.py: `python tools/derivations/open_items/H-Den-Beyond-128-Bits-1/laws.py world_record_hole3.json 60 30 out/laws_record_hole3.json`, and the control, and recordT)

| | record's den | control den |
|---|---|---|
| run back, 3-cube 120 intervals | 120 of 120 exact (bit for bit, the state's hash) | 120 of 120 |
| run back, 5-cube, 60 of 120 | 60 of 60 | 60 of 60 |
| run back, bodies 7-cube, 20 of 60 | 20 of 20 | 20 of 20 |
| the 48 on the births and the volume and light rows (3-cube, 60 intervals, 11 / 10 births) | 48 of 48 | 48 of 48 |
| the 48 on the credit lines (interval, Node, line, beat, sense) | 8 of 48 (27 credits) | 48 of 48 (23 credits) |
| the same at T 2,740,279,732 | 8 of 48 (18 credits) | |
| the one-Link reach forward: lines differing / farthest L1 distance | 36 / 1 | 34 / 1 |
| the reach backward | 2 / 0 | 2 / 0 |

The run back is exact at both dens (the carried division is a bijection at every width). The 48 holds on the board at both dens; in the clicks it holds at the control (48 of 48) and breaks at the record's den (8 of 48): the credits of one-level records (1e, 2e) are the rounding's, and the rounding at the half wall is not the cube's. A conservation held on the board and lost in the clicks is not shown (THE_WAY step 4): the record's den fails this step. The reach is one Link forward at both dens, 0 backward.

### 2d. The clock's memo transient (K-S4) and the paces

Gamma 1,000 as the record's universe file carries it (node_clock 1000); the memo's running fraction after the runs 30,860 over 30,855 bits at the content 3,095 (the deepest filled by the loader's looked_up table) at BOTH dens: den does not enter the clock (p_0 = Gamma (1 - 1/Gamma)^c), so K-S4's transient is den-free, 30,860 bits either way, and the paces' group law rounds the same (the clock 276 and the Link pace 76 at the content 1,288 on the record's 5-cube; 256 and 66 at 1,363 on the control's). The largest odd Gamma within the width is moot at the record's den (w passes 128 bits at every Gamma; w passes 128 at den's 98th bit at Gamma 1,000 and G 16, den_record.json).

### 2e. The cost the brief did not name, derived and measured: the quantum below one level, the take's excess

Derivation (the toy's lay act, ALGEBRA.md the lay of the record out whole): one quantum of a lift is laid at the least A with (2 D + SUM_j R_j) A^2 >= unit x 4 p^2 G^2; at the vacuum C = 12 Gamma^2 G^2 (2 gap + num) and unit = 3 T s, so A^2 >= T s / den. Measured T s / den per 10^6: the record's den 13 (electron), 24,122 (proton), 24,155 (neutron): A = 1 for all three; one level holds 76,118 electron quanta or 41 nucleon quanta. The control den: 19,320,213 / 35,474,878,444 / 35,523,754,787: A = 5 / 140 / 140. So at the record's den no record of a lift is resolved by the integers at T 36,000: the born child, the laid body and the click all sit at one level, and everything read from them is the rounding (1d, 1e, 2c). The take: the identity taken >= booked holds on every birth at both dens; the excess at the record's den is 559,596 times the booking on the 3-cube (taken 10414770071826372376775990851955026288337109631754152 against booked 18611208610041337105369475458211872374932832000, 55,959,665 hundredths) and 194,820 times on the 5-cube; at the control 1.11 times (111 hundredths) on both cubes. One level of light at the record's den is worth about 10^7 electron pairs.

The mend within the laws (K-S2, T a resolution bounded by the lay): T >= den div s_e = 2,740,279,732 (32 bits, even), the least T at which every lift's quantum reaches one level (T s / den = 999,999 per 10^6 for the electron, A = 1; 1,836,152,655 for the proton, A = 43; 1,838,683,653 for the neutron, A = 43). Measured with universe_record_T.json: the run back 120 of 120 and 60 of 60 and 20 of 20 exact; births 6 (3-cube), 11 (5-cube), 30 (bodies' 7-cube), the senses 0; the walls W_c 187 bits, the volume's time write wall 231, the state's largest integer 230, Rule3's transient 208, the credit's frame 190; the take's excess 402 times (3-cube) and 671 times (5-cube), down from 559,596 and 194,820; the packets resolved (weight 2^21) and dispersing as free packets (7 per mille within one Link by interval 5); the credits' 48 still 8 of 48 (the electron's lift still at A = 1: T must rise again by 4 for A = 2, by 10^4 for A = 100, to 2^46, W_c then 201 bits). The mend buys the resolution of the heavy lifts at 16 more bits on every den-carrying wall; it does not buy a body (the gap) or a readable beat (the angle).

## 3. The sentence, dated, and the alternative

The sentence as it would stand in ALGEBRA.md under The Node (2026-10-25): "den is the one exception to the 128 bits, and with it the integers that carry den as a factor (the walls w = 6 den Gamma^2 G^2 and 3 den T, the held rows' write walls, every rotation remainder, Rule3's total, the quanta 3 T s, the reach and the mass, the credit's and the birth's numbers); every other integer (the levels, the counters, the phase, the sign's and the light's write remainders, the paces) within 128; the former sentence, den bounded by the transients it makes, kept by name." Solved by it at the record's den: the three lifts' legs in nature's ratios to 18 and 5 parts in 10^9 (the control's 54-bit den gives them to 889 and 646 parts in 10^9); the births, the charge, the run back, the board's 48 and the reach hold as at the control. Cost: 18 of 24 integer classes beyond 128 bits (the walls 171 to 215, every remainder 185, the largest 215 and 231 at the mended T); the lifts' quanta below one level at T 36,000 (A = 1, one level 76,118 electron quanta) and the take's excess 10^5 to 10^6 times the booking (1.11 at the control); the credits' 48 broken (8 of 48 against 48 of 48); the gaps 10^-13 so no body stands (the two packets disperse in 20 intervals, the control's stand at 454 per mille); the beats 10^7 to 10^10 intervals, unreadable; n -> p + e no two-child list at either den.

The alternative: "den within 128 bits, a three-prime den of the width with the heavy lifts' g in the window of the middle (K2's 1.00056; the control's 54-bit den gives n/p 1.001378 to 646 per 10^9 and p/e to 889 per 10^9 at g 0.83)". Solved: every integer within 128 bits (the control's largest 115, its transient 107), the quanta resolved (A 5 / 140 / 140), the take within 11 per cent, the 48 in the clicks 48 of 48, the two packets stand, the heavy lifts' beat 6 intervals readable (measured 5 on 3 credits); the ratios to one part in 10^6. Cost: nature's ratios to 10^-6 instead of 10^-9, and the electron's lift stays a near-light cloud (g 1.4 x 10^-4, its beat 11,705 intervals, its quantum 5 levels) at any den that carries p/e 1,836, since a sine of 1/1836 of the heaviest is a gap of 10^-7 at best.

## 4. The toy spec for David (the lay, the intervals, what to read, the pass in numbers)

The files under tools/derivations/open_items/H-Den-Beyond-128-Bits-1/ run as they are: `python tools/derivations/open_items/H-Den-Beyond-128-Bits-1/run_toy.py world_<tag>_<world>.json out/<name>.json back N` for tag record, control, recordT and world hole3 (120), hole5 (120), bodies7 (60); `python tools/derivations/open_items/H-Den-Beyond-128-Bits-1/laws.py world_<tag>_hole3.json 60 30 out/laws_<tag>.json`; `python tools/derivations/open_items/H-Den-Beyond-128-Bits-1/read_clicks.py out/<name>.json out/<name>.reading.json`. Read: the births and their senses' sum, the taken against the booked (hundredths), the beats per lift on the credits against 2 pi den div s, the packets' share within one Link per mille at 1, 2, 5, 10, 20, 40, 60, the census of bits per class, the ms per interval, the run back, the 48 on the births and on the credits. Pass for "den beyond 128 solves": the take within 2 of the booking, the credits' 48 at 48 of 48, the two packets above 300 per mille at 60, a heavy lift's beat read within one interval of 2 pi den div s on at least 3 credits; the record's den fails all four (559,596; 8 of 48; 11; none), the control passes all four (1.11; 48; 454; 5 against 6). Deviation from the law's letter: none in the files; the toy's close reaches more than one Link by David's own naming (not measured here beyond the reach test's 1 forward, 0 back).

## 5. The laws checked, with numbers (Addition 4)

The conserved form: not measured as the form (no act in the toy reads it); the count stands in for it: taken >= booked on every birth at both dens, the excess 11 per cent at the control and 559,596 times at the record's den. The run back: 120 of 120, 60 of 60, 20 of 20 at both dens and at the mended T. The one-Link reach: 1 forward (36 and 34 lines), 0 backward at both. The cube's 48: 48 of 48 on the births and the rows at both; 48 of 48 on the credits at the control, 8 of 48 at the record's den (the one law broken in the clicks). The fixed count: 98 arrays per Node at both. The 128 bits: the control within (115 state, 107 transient; the memo's 30,860 apart, den-free); the record's den beyond on 18 classes (215 state, 207 transient). Integers only: every script and reading an integer (the toy's census, bit lengths, quotients with remainders). One act on every row alike and the two kinds of act: the toy's rotate/write per row and the swap/close per Node, unchanged, read not re-measured. The exact take: the identity holds on 11 of 11, 22 of 22, 10 of 10 births at the record's den and 10 of 10, 22 of 22, 10 of 10 at the control; exactness (excess 0) on 0 births at either den. No name and no number in the code: the files carry the numbers, the toy's code none; this hand's scripts name the lifts for the reader alone. In the clicks: the charge 0 at both dens; the count as above; the energy (the beat unchanged click to click) 509 of 512 pairs unchanged at the record's 5-cube and 25 of 25 at the control's, but at the record's den the beat is the rounding's (1e); the momentum not read by the toy.

## 6. Verdict

DOES NOT WORK as a solution of "many things": den beyond 128 bits at the record's den solves one thing, the three ratios to 10^-9 (the control den has them to 10^-6), and costs the 128 bits on 18 integer classes (walls 171 to 215, every remainder 185, the state 215), the quantum's resolution (A = 1, one level 76,118 electron quanta, the take's excess 10^5 to 10^6), the 48 in the clicks (8 of 48), every body (g 10^-13: the two packets disperse in 20 intervals) and every beat (10^7 to 10^10 intervals). The one mend within the laws, T raised to den div s_e = 2,740,279,732, resolves the nucleons' quantum (A 43) at 16 more bits on every den-carrying wall and the excess still 402 to 671 times, and mends neither the body nor the beat nor the credits' 48. Laws checked: run back MATCH (120, 60, 20 of each), reach 1 / 0, the board's 48 at 48 of 48, the fixed count 98, integers only, the identity of the take; the one unmet at the record's den: the 48 in the clicks (8 of 48) and the 128 bits (18 classes), with the exact take's exactness unmet at both dens as before.
