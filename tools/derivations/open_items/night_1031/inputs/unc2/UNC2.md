# UNC2: what the click record fixes of the board's passing and teeth (the carry's band, a board check beside the click readings; node-all 9d75a4904)

UNC2, for the Boss, 2026-10-31, 08:5x to 09:3x UTC. It replaces UNC1 (frozen at S/unc1_frozen, UNC1.md sha256
2606e2f55a853f81..., 426 lines), corrected by its two readers and by the Boss's rulings of 08:4x and 08:5x. Read only:
nothing under /home/user/Universe24 was edited, committed or pushed; no worktree was touched; UNC1 was not touched. S is
S; everything new is in S/unc2.

Read whole: S/unc1_math/REPORT.md (the mathematician: PASSED, 7 MINOR), S/unc1_phys/REPORT.md (the physicist: NOT
PASSED, 4 BLOCKING, 6 MINOR), and S/BRIEF_PAIRS.md's 08:4x and 08:5x sections. The tree: node-all 9d75a4904, taken
read-only by `git archive 9d75a4904` into S/unc2/tree. The interpreter: the project's Python 3.14 (the live venv's), run
with -I -B, so that no bytecode is written into any tree.

Standing labels as before: DERIVED (proved here in whole numbers, or the text holding it named), MEASURED (a probe, its
count, run twice with outputs alike), OPEN or OWED (by name). Every relation below but U3 sets a click count against
the board's passing or a tooth, both board quantities; so each is a board check beside the click readings (the 07:5x
rule), named so, and none is a claim of physics. U3 sets two click readings against each other (a line's q and its
sides). Light and matter appear nowhere on the board.

## Summary

- **What this is.** UNC1's relations are the carry's band: what the click record fixes of the board's passing and
  teeth. They are not the click world's uncertainty principle. That name is kept for a relation between two click
  observables, place and motion, read by light's echo and Bondi's k: OWED, waiting on LIGHT3's lines and echo (section
  8). "Time-and-energy" is an analogy by name only and is out of every DERIVED item.
- **U1, the carry's band on the passing (DERIVED; a board check).** On every side and window,
  K Q_W = S_W + k_start - k_end, so |K Q_W - S_W| <= K - 1; from the birth (K - 1) div 2 the count is the passing's
  nearest whole number of quanta, never a tie; both bounds are attained over the fiber of a q-word. Its no is the
  plan's grain: every passing is a multiple of G (G = 24,000 on the click world, gcd(G, K) = 3; G = 30,000 on the mesh
  world, where K = 3 divides it and the tooth never moves).
- **U2, the tooth's flatness and its reader (DERIVED).** To the reader who admits every passing sequence, every tooth
  path stands over every q-word. A reader who reads a click word as balanced and takes it as a steady carry's fixes
  the tooth (UNC1's physicist, MEASURED); U2 names its reader.
- **U3, a line's q and the place's circulation (DERIVED; click-only).** The lines' q fix a triangle's edges only up to
  the circulation; the click world reads the sides, so it reads it. U3 is no uncertainty of the click world.
- **The teeth (Q11).** As built, the record's teeth are board fields carried for the checks (E's guard, the books, the
  run back); the click world's readings read the lines and the sides alone, and no click reading changes with the
  teeth. Q11's stake stands in the 08:5x ruling's two cases (section 6).
- **The seed test's twin (MEASURED).** Moved lawfully (the edge's one tooth on both sides, half the key), the clicks
  differ at the edge's two clocks, (13, 0) and (17, 0) at 122 rounds each, the edge's books closed at 200 of 200
  rounds and every one of 20,100 windows within one quantum on each side. The one-unit test reads NOT SHOWN on the
  click world's first click for every round and every lay of its files, by the plan's grain (DERIVED by UNC1's
  mathematician, reproduced). The
  one-quantum bound (U1e) holds for the first click's carries alone; the third click's freedom is MEASURED at tens of
  quanta on a window (42 and 35, UNC1's physicist), its band OPEN.
- **Bell under the owner's road (C).** The bound 2 holds for every form with settings independent of the hidden part,
  the pair's one hand included. Under (C) it is cited for the free-lay control alone (the member born at the middle);
  (C) passes it only through the seeds' law, OPEN. U2's flat tooth is the room that law would fill, not a bound on it.

## 1. The frame

### 1.1 The carry and the cocycle (UNC1 0.1; both readers SOUND)

At every edge side (two trains at one Node-clock, or across a Mesh), with K the edge dial (odd) and P_n the round's
passing (step.passing and step.crossing, a whole function of the board's window): q_n, k_(n+1) = carry(P_n, K, k_n),
so P_n + k_n = q_n K + k_(n+1) with 0 <= k_(n+1) < K and the birth k_0 = h = (K - 1) div 2. Over a window W = [m, n):

    (T)   K Q_W = k_m + S_W - k_n   (the telescoping law; (T), to keep apart from the owner's road (C)).

The board reads no tooth (step.py line 157, the act's last computation before its return); an edge's two sides carry P
and -P from teeth born summing to K - 1, so the edge holds one tooth: k(u, t) = K - 1 - k(t, u), q(u, t) = -q(t, u).

### 1.2 The record, and what the click world reads (the 08:5x ruling)

- run.clicked writes, wherever an edge side carried, a line for every clock joined to it there, listing every own side
  [u, q, k_before, k_after] (q 0 included) and each Mesh side that carried; the header holds the dial and the birth;
  the end holds every side's tooth.
- The teeth, the birth and the end's teeth are board fields carried for the checks: E's guard (sides.paired: mates,
  sums and teeth ranges; "admitted" means the mates close, not faithful to the act), the books, the run back. A passing
  recovered through them, P = K q + k_after - k_before, is a board check.
- The click world's readings read the lines and the sides alone: shadow.py's books, meetings, clock lines and cone read
  q, train, round and site; no line of shadow.py or clicks.py reads a click tooth.

### 1.3 Words

- A click is a line that passes a quantum; a meeting is one give and one take of a quantum on a side (shadow.met).
- A clock's own count between two of its meetings is the number of its own lines between them (FACE2). A line's q is
  the line's net quanta, the sum of its sides' q. They are two things and are named apart (UNC1 used "a clock's count"
  for the second in U3).
- Rounds are order alone, never a duration: D4 (Big Pic's section 8; DECODE3f section 5). UNC1 cited D7 for it.
- Two readers: the click world's, of the lines and the sides; and a board check through the record's teeth.

## 2. U1: the carry's band on the board's passing (a board check beside the click readings)

**U1a (DERIVED).** By (T), K Q_W - S_W = k_m - k_n exactly, on every side and every window.

**U1b (DERIVED).** |K Q_W - S_W| <= K - 1 on every window. From the birth, K Q_n - S_n = h - k_n lies in [-h, h], so
2 |K Q_n - S_n| <= K - 1; writing S_n = j K + r (0 <= r < K), Q_n = j + [r >= h + 1], and r <= h exactly when
r < K / 2 for K odd. So the count from the birth is the passing's nearest whole number of quanta, never a tie
(2 S_n = (2 j + 1) K would equate an even and an odd number).

**U1c (DERIVED).** The carry with its remainder kept is a bijection P <-> (q, k') given k. Over each q-word stands
exactly one passing sequence for each tooth path, P_n = K q_n + k_(n+1) - k_n, so over the fiber S_W - K Q_W = k_n - k_m
takes every value in [-(K - 1), K - 1] when m >= 1 and every value in [-h, h] when m = 0. Checked exhaustively on the
dials 3, 5 and 7 over 4 rounds (UNC1's unc1_toy.py, reproduced by the mathematician byte for byte): confirmations of
the carry's bijection, not evidence beyond it.

**U1d (DERIVED in its form; named only by analogy).** The band over a window is fixed, so against any clock's own count
T >= 1 the board's beat S_W / T lies in an interval of width 2 (K - 1) / T; the whole-number line
T x (2 (K - 1) div T) <= 2 (K - 1) < T x (2 (K - 1) div T + 1) is floor division's definition and carries nothing more.
U1d has the form of a counter's resolution of the board's hidden passing. The click world's own readings, Q_W and T,
are both sharp; only the board's passing is banded, and the band vanishes for a board check through the teeth. It is
named after the time-and-energy relation by analogy only, OWED as physics; nothing here claims a time or an energy.

**U1's no: the plan's grain (DERIVED; reproduced by unc2_grain.py).** step.passing books weight[i, u] x factor_i x (a
whole product of readings) on a side, and step.crossing books across[s, r, p] x (a whole number): so every passing of
every state is a whole multiple of G, the gcd of the nonzero weight x factor values and Mesh couplings. With
c = gcd(G, K), every tooth stays on its birth's coset h + c Z mod K, which holds at most K / c places (an upper bound:
click200's 200 rounds write 283 distinct teeth).

| world | nonzero weight x factor; Mesh couplings | G | K | c = gcd(G, K) | at most K / c places |
|---|---|---|---|---|---|
| click (its universe and piece) | 120,000, 240,000, 288,000; none | 24,000 | 152,434,287 | 3 | 50,811,429 |
| mesh (its universe and piece) | 120,000, 240,000; 750,000 | 30,000 | 3 | 3 | 1 |

On the mesh world c = K: the tooth never moves, S_W = K Q_W on every window and every lay of its files, and U1 reads
NOT SHOWN there by structure (the measured grain 30,000 over 125 rounds is the structural one). On the click world the
measured grain (48,000 over 200 rounds) is a multiple of the structural 24,000. G is read from the universe file's
strengths and the plan; it picks nothing and no number is set to make a band appear.

## 3. U2: the tooth's flatness, and its reader

**U2a (DERIVED, for the reader who admits every passing sequence).** By U1c, over every q-word every tooth path stands,
each by exactly one passing sequence. To that reader the count is sharp and the tooth is flat over the dial (within
its coset, a board fact the free reader does not know).

**U2's reader (the physicist's minor 1).** Balance is read in the clicks: a word whose windows of one length hold counts
apart by at most one. A reader who reads a click word as balanced from its q's alone and takes it as a steady carry's
word fixes the steady passing and the tooth: MEASURED by UNC1's physicist (steady_reader.py, K = 101, run twice): 1 of
10,201 (passing, tooth) pairs and 1 of 101 places at 200 rounds, 3 places at 30 and at 50 rounds. Its premise, that
the passing is steady, is a claim about the board's passing: a balanced word is consistent with it and, by U1c, with
every other tooth path too. So U2a's "no bit of the tooth" is the free reader's; the steady reader learns the tooth
under its premise. UNC1's "that reader reads the board, not the clicks" is withdrawn.

**U2b (DERIVED).** The count stands in every line, so no record makes the tooth sharp at the count's expense: U2 is an
access relation, not a trade-off. UNC1's number-state analogy is dropped.

**U2's no (a board check).** A board check through the teeth reads count and tooth together at every listing (25,272
on click200, 41,376 on mesh125); and where c = K the tooth is one place (the mesh world).

## 4. U3: a line's q and the place's circulation (click-only; no uncertainty of the click world)

**U3 (DERIVED).** At a place where three clocks t, u, v stand on three laid edges, each line's q is the sum of its
sides: q_t = q_tu - q_vt + (its other sides), and so for u and v. Adding a whole c' to the three oriented edges moves no
line's q, so the lines' q fix the edges only up to the circulation c = q_tu + q_uv + q_vt (MATH1 4.2's split; B C = 0).

**What it is.** The click world reads the sides (its meetings are sides), so it reads the circulation: U3 says only what
a reader of the lines' q alone would miss. It is no uncertainty of the click world. On a lone triangle a flow is a pure
gradient exactly when c = 0, so a nonzero c is mostly one edge carrying alone, not a circulation event; and, by the
08:4x ruling, c . q alone reads a circulation on any form's record, so U3 is no reading of the third click.

**MEASURED (UNC1, reproduced by both readers).** click200: 4,212 places hold the triangle of the held, the giver and the
taker; at 108 all three edges pass a quantum; c is not 0 at 4,158 of them. mesh125: no place holds a triangle of three
clocks (NOT READ).

## 5. Two records alike on the board: the seed test's two-record form

### 5.1 The twin, moved lawfully (the 08:5x ruling; the mathematician's m2)

The edge's one tooth is moved on both its sides: k(t, u) + d and k(u, t) - d, so the two teeth still sum to K - 1.
UNC1's twin moved one side alone, an off-lay state that sides.paired refuses; its readings are not cited as MEASURED.

### 5.2 What the carry gives the first click's two records (DERIVED)

- **U1e.** Two records alike on the board share every S_W, so by U1b on both, |Q_W - Q'_W| <= 1 on every side and
  window. This holds for the first click's carries alone.
- **U1f (with the wrap bracket, m4).** A side's tooth moved by v (0 < v < K): its moved birth is (k_0 + v) mod K, so the
  two lifts kappa = K Q + k differ by v - K [k_0 >= K - v] at every round, and

      Q'_n - Q_n = [k_n >= K - v] - [k_0 >= K - v],   k_n the first lay's tooth after round n.

  On the edge's two sides v = d and v = K - d. The clicks differ exactly at the rounds where the first lay's tooth
  enters or leaves the strip [K - v, K - 1], on both sides at once (the books q(t, u) + q(u, t) = 0 stay closed), so a
  lawful twin's clicks differ at the edge's two clocks: the seed test's "only at that clock" reads "only at that edge's
  two clocks".
- **The one-unit test (DERIVED by UNC1's mathematician from the plan; reproduced).** On the click world every passing
  is a multiple of G = 24,000 and K = 3 x 50,811,429, so every tooth stays h = 1 mod 3, for every round and every lay of
  the click world's universe and piece; a one-unit edge move changes a click only where the tooth stands at K - 1
  (2 mod 3, the side moved up) or at 0 (0 mod 3, its mirror moved down). So the owner's test (ii), one unit apart, reads
  NOT SHOWN on the click world's first click by structure. On the mesh world (c = K) no move of any tooth ever shows.
  The test's unit is the owner's: no unit or lay is changed to make it show (08:5x). To the owner's batch as a finding.

### 5.3 MEASURED: the lawful twin on click200

unc2_twin.py loads click200 as the run tool does and moves the tooth of round 1's busiest own edge: side 13, the held
and the giver's edge (2, 3) at site 0 (its first passing 768,000,000), with its mirror, side 17. Each run twice, outputs
alike byte for byte.

| reading | half the key, d = 76,217,143 | one unit, d = 1 |
|---|---|---|
| the teeth moved (+d on side 13, -d on side 17) | 76,217,143 and 76,217,143 to 152,434,286 and 0 | to 76,217,144 and 76,217,142 |
| the board alike (a board check) | 200 of 200 rounds | 200 of 200 rounds |
| (side, site) whose clicks differ, rounds each | (13, 0) at 122, (17, 0) at 122 | none |
| the moved lay's books q(t, u) + q(u, t) = 0 | 200 of 200 rounds | 200 of 200 rounds |
| the moved lay's two teeth summing to K - 1 | 200 of 200 rounds | 200 of 200 rounds |
| each side: windows, the largest abs(Q_W - Q'_W), windows that differ | 20,100, 1, 10,088 (both sides) | 20,100, 0, 0 (both sides) |
| U1f on side 13 (v = d, wrap bracket 0) | 200 of 200 rounds | 200 of 200 rounds |
| U1f on side 17 (v = K - d, wrap bracket 1) | 200 of 200 rounds | 200 of 200 rounds |
| rounds with the first lay's tooth in the strip [K - v, K - 1] | side 13: 97; side 17: 103 | side 13: 0 (the place K - 1); side 17: 200 (never at 0) |

The lawful twin keeps the record on the lay (the books and the teeth close at every round) and its clicks differ at the
edge's two clocks. Side 13's numbers are UNC1's one-side twin's (122 rounds, 10,088 windows, U1f 200 of 200), as the
mirror law carry(-P, K, K - 1 - k) = (-q, K - 1 - k') gives and the mathematician measured (twin_edge.py): they now
stand MEASURED on a lawful twin. The one-unit move writes no click apart: the first lay's tooth never stands at K - 1 or
0 (it stays 1 mod 3, section 5.2).

### 5.4 The third click's freedom (MEASURED by others; its band OPEN)

The law's choice lives at the third click; "on a lay the first click is fixed by its side's past" (07:5x). The carry's
one quantum does not bound the third click's member:
- UNC1's physicist (path3.py, run twice): the member at the click world's dial 3D = 457,302,861, two lays alike in y
  (the board alike) and one unit apart in the twin, 4,000 rounds: with y steady at 86 thousandths, 658 rounds whose W
  differ and a widest window of 42 quanta; with y swinging from 60 to 111 thousandths, 610 rounds and 35 quanta.
  Beside it, the first click's carry at the same passing reads 0 rounds apart one unit apart, and a widest window of 1
  at half the dial (U1e there).
- DECODE3f: the third click's twin SHOWN, 798 sides apart.
- So the third click's freedom is MEASURED at tens of quanta on a window, and its band is OPEN. UNC1's sentence "the
  owner's 'the clicks differ, the end is the same end' is so bounded" is struck: U1e bounds the first click's carries,
  where the law places no choice, and not the law of the path.

## 6. Q11: does the record keep writing the teeth? (the physicist's B2; the 08:5x ruling)

- **As built (case b).** The teeth are board fields carried for the checks (E's guard, the books, the run back). No
  click reading changes with them: shadow.py reads q alone, and the click world's readings read the lines and the sides.
  A passing recovered through the teeth is a board check: P = K q + k_after - k_before at every listing, and
  k_before(next) - k_after(prev) over every silent gap.
- **If the teeth were click content (case a).** The record would put the board's exact passing into the click world at
  every listing, and its sum over every silent gap; inside a gap a sub-window's passing would be fixed to the outer
  bound [-(K - 1), K - 1], and to K values where the sub-window starts or ends at a listed tooth (m6). That would breach
  the arrangement: the board's passing stays out of the click world.
- **What is withdrawn.** UNC1's "with the teeth written, the click world's uncertainty reads NOT SHOWN at every line"
  holds only in case (a). In case (b), as built, it reads: a board check through the teeth fixes the passing at every
  listing, and the click world's readings are the same with the teeth or without them.
- Q11 stays the owner's. Its stake is these two cases; the Boss rules which the record is, and has ruled (b) as built.

## 7. Bell under the owner's road (C) (the physicist's B3; the mathematician's m5)

- **The bound (DERIVED, classical: Bell 1964; Clauser, Horne, Shimony and Holt 1969).** For every form whose settings
  are independent of the hidden part, each wing's outcome a function of its own setting and the hidden part,
  |E(a, b) + E(a, b') + E(a', b) - E(a', b')| <= 2: per hidden value, A (B + B') + A' (B - B') is -2 or 2, and a mixture
  stays in [-2, 2]. The pair's one hand is included: a draw that reads a shared hand is a hidden part shared by both
  wings, and stays within 2 unless the far setting is read or the settings depend on the hand (the 08:4x and 08:5x
  rulings: a click-setting causes nothing on the board; a board influence that writes no click is measurement
  dependence). The 16 deterministic strategies give S = -2 or 2 (UNC1's unc1_toy.py; its settings are free inputs,
  independent by construction).
- **Under (C)** (the owner, about 08:35: "the settings and the hand meet through the seeds"). The bound is cited for the
  free-lay control alone: the member born at the middle, the 08:4x local control, which reads at most 2. (C) passes 2
  only through the seeds' law, OPEN (Big Pic's two-ended build): a law of the seeds' joint measure, covariant under the
  swap, S_3 and the 24, fixing the births to all their digits, with nothing picked; a seed rule chosen for S above 2 is
  a pick for an outcome. The act is one-to-one and keeps the count of states, so it cannot make the correlation itself.
- **U2 and (C).** U2's flat tooth, to the click world's reader, is the room (C)'s seeds' law would fill: the hidden part
  where its correlation would sit, not a bound on it.
- **What Q11 means for (C).** The seeds write no line, so the click world reads only the law's effect: the settings'
  lines and the outcomes' lines, their meetings and their order, no signal, and the free-lay control at most 2. In case
  (b), as built, the births and teeth are board fields: the settings' dependence on the hand is never a click reading,
  and a board check through the teeth could read the births beside the click readings. In case (a) the hand would
  stand in the click record at every listing, so the dependence R4's replaced part names ("the settings' dependence on
  the hand is the seeds' law's alone") would be legible in the click world itself, which would then hold the hidden
  part it is meant not to read.
- **On node-all's records** no setting is drawn and no pair event is named: Bell is NOT READ there.

## 8. The uncertainty principle proper (OWED)

A relation between two click observables, place and motion, read by light's echo between clocks and Bondi's k, is
what the name is kept for (08:5x). It waits on LIGHT3's lines and echo (reading 7) and on a world that lays a moving
clock: NOT READ today. Nothing in sections 2 to 7 is that relation.

## 9. The readings on the shipped worlds

- **The worlds and their ticks.** click200 is the shipped click world's first 200 rounds (its setting's ticks set to
  200, the only change). The shipped click world runs 3,751 of its declared 5,000 ticks: at round 3,752 a count passes
  the width and the runner writes no record (08:5x). mesh125 is the mesh world as shipped, 125 ticks.
- **UNC1's records and readings stand**, reproduced byte for byte by both readers: click200 run1 sha256
  750551cb5551e2b9515d0ac1f119922f042d814406619e2696dd1a6db3c3575c, mesh125 run1
  57203d4eb35669efcfb670440ecefcfb7e6bd43e82f32c47376f4d7f9b002426; unc1_read.py's outputs in S/unc1_frozen/out.

| reading (each a board check through the teeth unless named) | click200 | mesh125 |
|---|---|---|
| the listed teeth's chain, adjacent listings k_before(next) = k_after(prev) (a code check of the record) | 17,982 of 17,982 | 39,288 of 39,288 |
| silent gaps, their passing | 7,128, from -37,440,000 to 37,440,000 | 1,356, all 0 |
| the passings' grain over the run (a multiple of the plan's G) | 48,000 | 30,000 |
| distinct teeth written (at most K / c places) | 283 | 1 |
| U1 from the birth, h - k_after | -75,771,435 to 75,771,435, 994 per mille of h | 0 |
| one-quantum lines (q = 1, and -1): distinct passings | 9, spread 204,480,000, 670 per mille of 2 (K - 1) | 1 at every q: P = 3 q |
| one q carrying two passings | 24 q's, 6 of 6 distinct sides | none |
| one count from the birth with two teeth | 1,620 classes, every side | none |
| own-count windows between meetings (the windows click-only, their passings a board check): one (T, Q) with two passings | 54 clocks (2 a site), 270 windows (10 a site), 1 class of 3 windows | no place is a meeting: NOT READ |
| U3's circulation not 0 (click-only) | 4,158 of 4,212 places | no triangle: NOT READ |

The 27 sites of click200 write 6 distinct side histories, so "162 of 162" is "6 of 6". The alike histories come from
the alike lay; the board couples the sites with no click (NATURE2's mathematician), so they are not uncoupled copies.

## 10. Conduct, probes and outputs

- UNC2's runs: one process at a time, nice -n 19, each started only while the load stood below 8
  (S/unc2/out/run_unc2.log gives the load before each: 5.83 to 7.93 over the eight runs); Python 3.14 from the live
  venv, with -I -B; UNC2's own tree.
- UNC1's load line (its line 402, "7.0 to 9.2") is corrected: its logs read 7.49 to 8.08 before the world runs and 7.82
  to 9.74 before the probe runs, 20 of its 22 probe runs starting above 8. UNC1's conduct then asked only to read the
  load; its outputs were reproduced byte for byte by both readers under the stricter conduct.

| file (S/unc2/...) | what | sha256 (first 16) |
|---|---|---|
| probes/unc2_grain.py | the plan's grain G from the loaded layout (weights x factors, Mesh couplings) | 21696ed5b6b6f337 |
| out/grain_click200.a.txt (and .b) | its output on the click world's files | ed7db1f0611b05c7 |
| out/grain_mesh125.a.txt (and .b) | its output on the mesh world's files | f66e2aa487f982b2 |
| probes/unc2_twin.py | the lawful twin: the edge's one tooth moved on both sides, 200 rounds of click200 | fffe1ca78c99a226 |
| out/twin_edge_half.a.txt (and .b) | half the key | c1f541eb2b40061a |
| out/twin_edge_unit.a.txt (and .b) | one unit | 66c52f9dbca12cc4 |
| probes/run_unc2.sh | the batch, each probe twice, each run started with the load below 8; log out/run_unc2.log | 0d3451285000909a |
| tree/, worlds/ | node-all 9d75a4904 by git archive; click200 and mesh125 (the files UNC1 ran) | (as UNC1's) |

Cited, not rerun here: UNC1's unc1_read.py and unc1_toy.py outputs (S/unc1_frozen/out, reproduced by both readers);
UNC1's physicist's path3.py (beb94540f6bb5b26, output b64781652626f1ef) and steady_reader.py (fc4bafae0ddc907f,
output 160c29fb11dc6424), each run twice by that reader. Whole numbers only in every probe; Rule3's carry the one
division (Euclid's gcd by repeated carry, a reading outside the act).

## 11. The readers' items, one line each

| reader, item | how UNC2 meets it |
|---|---|
| mathematician m1: "time-and-energy" named, not derived | U1d is the form of a counter's resolution of the board's hidden passing, named after it by analogy only, OWED as physics; out of every DERIVED item (section 2) |
| mathematician m2: the twin moved one side's tooth | the edge's one tooth moved on both sides (5.1, unc2_twin.py); clicks differ at the edge's two clocks, the books closed 200 of 200; UNC1's twin not cited as MEASURED |
| mathematician m3: the grain left OPEN | closed by derivation from step.passing and step.crossing; unc2_grain.py reproduces G = 24,000 (gcd 3) and 30,000; the one-unit test NOT SHOWN for every round and lay (2, 5.2) |
| mathematician m4: U1f's lifts and the wrap | the lifts differ by v - K [k_0 >= K - v]; measured on the mirror side, whose bracket is 1 (5.2, 5.3) |
| mathematician m5: Bell and the pair's one hand | the bound covers the hand; 2 is passed only by reading the far setting or by settings depending on the hand (section 7) |
| mathematician m6: the gap's bound | named the outer bound [-(K - 1), K - 1], K values where a sub-window starts or ends at a listed tooth (section 6) |
| mathematician m7: K / c places | "at most K / c", 283 teeth written on click200 (sections 2, 9) |
| mathematician Q3: the interpreter | Python 3.14 from the live venv, -I -B, UNC2's own tree (header, section 10) |
| physicist B1: names | retitled as the carry's band, a board check beside the click readings; "uncertainty principle" kept for place and motion, OWED to LIGHT3 (Summary, sections 2, 8) |
| physicist B2: Q11 and the teeth | the 08:5x two cases; (b) as built, no click reading changes; UNC1's "NOT SHOWN at every line" held to case (a) (sections 1.2, 6) |
| physicist B3: Bell under (C) | the bound cited for the free-lay control alone; (C) only through the seeds' law, OPEN; U2's tooth the room it would fill; Q11's meaning for (C) (section 7) |
| physicist B4: M3's scope | U1e and the one-unit test scoped to the first click's carries; the M3 sentence struck; the third click's 42 and 35 quanta and DECODE3f's 798 sides cited, its band OPEN (5.2, 5.4) |
| physicist minor 1: a balanced word fixes the tooth | U2a names its reader (who admits every passing); the steady reader's result cited; UNC1's "reads the board" withdrawn (section 3) |
| physicist minor 2: U3 | no uncertainty of the click world; mostly one edge alone; "a line's q" named apart from the own count (1.3, section 4) |
| physicist minor 3: D7 for D4 | D4 cited (1.3) |
| physicist minor 4: line 375 against U1d | U1d claims no time or energy; the analogy is by name only (section 2) |
| physicist minor 5: the load | UNC1's load line corrected; UNC2's runs each waited for the load below 8 (section 10) |
| physicist minor 6: the click world's ticks | it runs 3,751 of its declared 5,000 ticks, named where its ticks are cited (section 9) |
| the Boss's 08:5x guard ruling | E's guard named by its reach: mates, sums and teeth ranges; "admitted" is the mates closing (1.2; the chain row named a code check of the record, 9) |
| the Boss's 08:5x islands ruling | "27 uncoupled copies" not said; the alike histories come from the alike lay, the board coupling the sites (9) |

## 12. For the Boss

1. Q11 in the 08:5x ruling's two cases (section 6): as built the teeth are board fields, and no click reading changes.
2. The owner's one-unit test (ii) reads NOT SHOWN on the click world's first click for every round and lay, by the
   plan's grain; a lawful twin's clicks differ at the edge's two clocks. To the owner's batch as a finding, with the
   third click's tens of quanta beside it.
3. Bell: the bound 2 is cited for the free-lay control alone; (C) waits on the seeds' law.

## Solution24

The click record fixes the board's passing to within one quantum either way (to the nearest quantum from the birth), and
a reader who admits every passing learns nothing of the tooth from the clicks; both are the carry's remainder, a board
check beside the click readings. The plan's grain fixes where that band is used: nowhere on the mesh world, and on the
click world never by one unit. The first click's two records differ by at most one quantum on every window; the third
click's by tens. The uncertainty principle of the click world, between place and motion, is OWED to LIGHT3.
