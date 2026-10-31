# UNC1: the uncertainty principle read in the click world, from the carry and the cocycle (node-all 9d75a4904)

UNC1, for the Boss, 2026-10-31, 08:0x to 09:0x UTC. Read only: nothing under /home/user/Universe24 was edited,
committed or pushed; S/nodeall was not touched. S is
S; everything of this text is in
S/unc1 (the tree, the worlds, the runs, the probes and their outputs).

The owner's word (to the Boss, about 07:59 UTC, the Boss's translation): "Also look at the uncertainty principle from
the clicks, as if in the click world." In the same message: "Bell is in the clicks, not on the board."

What was read whole: S/BRIEF_PAIRS.md (its last three sections above all); S/math1_math/REPORT.md and
S/math1_phys/REPORT.md; S/math1_frozen/MATH1.md sections 3 and 7; FACE2's section 4 to 5.2 (S/face2_frozen/FACE2.md,
the own count). The code: node-all 9d75a4904 (origin/node-all), taken read-only by `git archive 9d75a4904` into
S/unc1/tree: engine/step.py and state.py whole, algebra/carry.py, runner/run.py, rounds.py and rewind.py whole,
record/schema.py, and decoder/ (clicks.py, measure.py, sides.py, shadow.py whole; records.py's reader).

Every claim carries its standing: DERIVED (the proof is here, in whole numbers, or the text holding it is named),
MEASURED (the probe, its count, run twice with outputs alike), OPEN (by name). A board fact is never physics: light and
matter exist only in the click world, and no sentence below says either of the board. Where a reading of the record
uses the teeth to recover the board's passing, it is named "a board check through the record's teeth" (the Boss's
ruling of 07:5x UTC: a law that sets clicks against the board's passings is a board check beside a click reading).

## Summary

The click world's uncertainty principle, as the carry and the cocycle give it, is Rule3's own sentence: the quotient
leaves, the remainder stays. A click line holds what leaves (q); the tooth k, the remainder, stays on the edge. Two
pairs cannot both be sharp to a reader of q alone, and a third to a reader of the lines' q without their sides; all
three are whole-number theorems of the carry and the structure:

- U1, the count and the beat (DERIVED). On every side and every window W of rounds, K Q_W = S_W + k_start - k_end, so
  |K Q_W - S_W| <= K - 1; from the birth (k_0 = (K - 1) div 2) the bound is (K - 1) div 2, so the count from the birth
  is the passing's nearest whole number of quanta, never a tie (K odd). Both bounds are attained over the fiber of a
  q-word: no reading of q alone fixes the passing behind a window more finely than 2K - 1 values (K from the birth).
  Measured by any clock's own count T, the beat S_W / T is fixed to a width of 2 (K - 1) / T: a short window blurs the
  beat, a sharp beat needs a long window. Corollary: two records alike on the board differ by at most one quantum on
  every window (|Q_W - Q'_W| <= 1).
- U2, the tooth and the count (DERIVED). Over every q-word, every tooth path in [0, K)^N stands, each by exactly one
  passing sequence (the carry is a bijection n <-> (q, r') given r). So a q-only record fixes the count and holds no
  bit of where the tooth stands: the count sharp, the tooth flat over the dial. It is an access relation, not a
  trade-off: no record makes the tooth sharp at the count's expense.
- U3, a clock's count and the place's circulation (DERIVED). At a triangle of three clocks, the lines' q (vertex sums)
  fix the edges' quanta only up to the circulation q_tu + q_uv + q_vt (B C = 0): no clock's count reads it; the sides
  do. node-all writes the sides, so the click world reads it; on click200 it is not 0 at 4,158 of 4,212 places
  (MEASURED).

Neither U1 nor U2 is an operator relation of Heisenberg's kind: both say what the record fixes (a quantizer's band, a
hidden remainder) while the whole state holds every value.

U1 and U2 need the teeth out of the record. node-all's 1.4 record writes [u, q, k_before, k_after] on every
listed side, so the record holds P = K q + k_after - k_before, the board's exact passing, at every listing, and the
passing summed over every silent gap: there both pairs are sharp at once (U1 closes at the listings, U2 reads NOT
SHOWN on every listing). The decoder's click-world readings (shadow.py) read q alone; only the sides' guard reads the
teeth. On the shipped worlds (MEASURED, twice): the click world (ticks set to 200, named click200) fills the band (from
the birth |D| reaches 994 per mille of its half; one-quantum lines carry 9 distinct passings, a spread of 670 per mille
of 2 (K - 1)), so the count fixes neither the beat nor the tooth (SHOWN, as a board check through the record's teeth);
the mesh world (125 rounds as shipped) reads NOT SHOWN for both: its key 3 divides the passings' grain 30,000, so its
teeth never move and every q is the passing over 3. The relation's no is exactly that: K dividing the grain leaves the
tooth one reachable place. Two click-world records alike on the board and one tooth apart (half the key, at the
busiest side) differ at 122 of 200 rounds on that side and by at most one quantum on all 20,100 windows (click-only,
MEASURED); a one-unit move changes no click there while every passing is a multiple of 3 (every tooth then stays 1
mod 3 and the top place is 2 mod 3; the grain was 48,000 on all 200 rounds), so the seed test's (ii) worded "one
hidden unit" reads NOT SHOWN on the click world as laid. The hidden tooth is a local variable: Bell's bound 2 holds
for every form whose wings read their own settings and the hidden state (the 16 strategies give S = -2 or 2), so
this uncertainty cannot pass Bell; 2 r2 needs the pair's one hand, OPEN. On node-all's records Bell is NOT READ: no
setting is drawn and no pair event is named.

## 0. The frame

### 0.1 The carry and the cocycle (from MATH1's readers; DERIVED there and here)

At every edge side sigma (two trains at one Node-clock, or across a Mesh), with K the edge dial (odd; the header's
"dial") and P_n the round's passing (step.passing and step.crossing, a whole function of the board's window (b, a, a+),
J's work over the window):

    q_n, k_(n+1) = carry(P_n, K, k_n):   P_n + k_n = q_n K + k_(n+1),   0 <= k_(n+1) < K,   k_0 = (K - 1) div 2.

step.py line 157 is this carry, the act's last computation before its return: the board (a, b, r, rd) is computed
before it and reads no k (MATH1 3.2; both readers: SOUND). Summed over a window W = [m, n) of rounds (the
telescoping law):

    (C)   K Q_W = k_m + S_W - k_n,   Q_W = q_m + ... + q_(n-1),   S_W = P_m + ... + P_(n-1).

The board is a factor and the clicks a cocycle over it: Q_n = floor((k_0 + S_n) / K) (MATH1 3.1; both readers SOUND).
An edge's two sides carry P and -P from teeth born summing to K - 1, so q(u, t) = -q(t, u) and k(u, t) = K - 1 - k(t, u)
forever: the edge holds one tooth.

### 0.2 What the record holds, and what the click world reads (read in the code)

- run.clicked writes, wherever an edge side carried at a round and Node-clock, a line for every clock joined to it
  there, listing every own side [u, q_tu, k_before, k_after], q 0 included, and each Mesh side that carried
  [u, place, q, k_before, k_after]. A Mesh side of q 0 is listed nowhere. The header holds the dial and the birth; the
  end holds every side's tooth.
- So a side carrying at a round is always listed then; between two listings its q is 0 at every round. From the record
  alone: P = K q + k_after - k_before at every listing, and G = k_before(next) - k_after(prev) is the passing summed
  over the silent rounds between two listings.
- The decoder's click-world readings read q alone: shadow.py's books, meetings, clock lines and cone read q, train,
  round and site (carried, silent, met, books, across); no line of shadow.py or clicks.py reads a click tooth. The
  click teeth are read only by the sides' guard (sides.sided: each tooth within [0, K); sides.mirrored: the two teeth
  of an edge summing to K - 1), a check of the record's faithfulness, a code check.

### 0.3 The click world's words (the brief, the FACE2 ruling)

- A click is a line that passes a quantum (a side with q not 0); a meeting is one give and one take of a quantum on a
  side (A4's shadow.met: the place's non-silent lines are q -1 and q +1 on one edge and its mirror); a side at q 0 is
  no meeting.
- A clock is a site and a train. Its own count between two of its meetings is its own (non-silent) lines strictly
  between them (FACE2, Big Pic's road). Rounds are order alone, never a duration (D7).
- Two readers are weighed throughout: case (i), a reader of q alone (the teeth out of the record); case (ii), a reader
  of q with k_before and k_after, as node-all's record is written today.

## 1. The pairs that cannot both be sharp

### 1.1 U1: the count and the beat

The count of a window is Q_W, the quanta a side passed over it; the beat is the passing behind them, S_W, read against
a duration (a clock's own count T, or the window's rounds as a board check).

**U1a (DERIVED, the identity).** By (C), K Q_W - S_W = k_m - k_n exactly, on every side and every window.

**U1b (DERIVED, the bounds).** Since 0 <= k_m, k_n <= K - 1: |K Q_W - S_W| <= K - 1 on every window. From the birth
(m = 0, k_0 = h, h = (K - 1) div 2, the header's birth): K Q_n - S_n = h - k_n lies in [-h, h], so
2 |K Q_n - S_n| <= K - 1. Write S_n = j K + r with 0 <= r < K. Then Q_n = floor((S_n + h) / K) = j + [r >= h + 1], and
since K is odd, r <= h exactly when r < K / 2. So Q_n is the nearest whole number of quanta to S_n / K, and there is
never a tie (2 S_n = (2 j + 1) K would set an even number equal to an odd one). In words: counted from the birth, a
side's clicks are its passing rounded to the nearest quantum; on a later window they are its passing to within one
quantum either way.

**U1c (DERIVED, attained: the fiber of a q-word).** Fix k_0 = h. The carry with its remainder kept is a bijection
P <-> (q, k') given k (Euclidean division; carry.py's docstring: "the quotient leaves ... and the remainder stays").
Chained over N rounds, (P_0, ..., P_(N-1)) <-> ((q_0, k_1), ..., (q_(N-1), k_N)). So over each q-word stands exactly
one passing sequence for each tooth path (k_1, ..., k_N) in [0, K)^N, namely P_n = K q_n + k_(n+1) - k_n. Over the
fiber, S_W - K Q_W = k_n - k_m takes every value in [-(K - 1), K - 1] when m >= 1 (k_m and k_n free and independent),
and every value in [-h, h] when m = 0. No function of the q's alone narrows S_W further; a reader who narrows it brings
in something of the board (its passings or its rule run on the header's files), which the click world does not read
(the owner's ban). Checked exhaustively on toy dials K = 3, 5, 7 over N = 4 rounds (unc1_toy.py T1 to T3, section 5).

**U1d (DERIVED, the trade-off with a duration).** Let the window be measured by any clock's own count T >= 1 (FACE2).
To a q-only reader the beat S_W / T is fixed to an interval of width 2 (K - 1) / T, and in whole numbers
T x (2 (K - 1) div T) <= 2 (K - 1) < T x (2 (K - 1) div T + 1): the band over the window is fixed, so the beat's
width falls only as the window grows, whatever clock measures it. A count localized in a short window leaves the beat
blurred; a sharp beat needs a long window. This is the counting form of the time-and-energy relation: the passing is
J's work over the window (step.py), the click is K units of it, and the dial K stands where Planck's unit stands
(an analogy, named and not claimed). It is not an operator relation: its "product" is the fixed band divided by the
window, a counter's plus or minus one count.

**U1e (DERIVED, two records alike on the board).** Two runs alike on the board, with any two tooth paths (two births,
or one tooth moved: the seed test's (ii)), share every P_n and so every S_W. By U1b on both,
K |Q_W - Q'_W| <= 2 (K - 1) < 2 K, so |Q_W - Q'_W| <= 1 on every window: the clicks may differ round after round, but
never by more than one quantum on any window. Checked exhaustively on the toy dials (T4) and MEASURED on the click
world (section 3.3).

**U1f (DERIVED, the two-record law).** Let the second lay's tooth on one side be moved by u, 0 < u < K, the boards
alike. The two lifts kappa = K Q + k then differ by u at every round, so

    Q'_n - Q_n = [k_n >= K - u] - [k_0 >= K - u],   k_n the first lay's tooth after round n.

The two records' counts differ, at every round, by one bit: whether the first lay's tooth stands in the dial's top u
places. No one record reads its tooth; two records alike on the board read one bit of it per round, and the moved
lay's clicks differ from the first's exactly at the rounds where the first lay's tooth enters or leaves that strip.
(U1e is the corollary |Q'_n - Q_n| <= 1.)

**U1's no (DERIVED condition; MEASURED on a shipped world).** Let g be the passings' grain, the gcd of every passing a
side meets, and c = gcd(g, K). The tooth moves on k_0 + c Z mod K, so it has K / c reachable places. Where K divides g
(c = K) the tooth never moves, k_n = k_0 at every round, S_W = K Q_W exactly on every window, and the count fixes the
beat: U1 reads NOT SHOWN. The mesh world is that lay (g = 30,000, K = 3: one reachable place, section 3.2). An edge key
1 (the three silent worlds' structure: no edge, NO CLICK) is the degenerate case, q = P. As a reading of a record with
teeth, U1 is: does one q carry two passings? SHOWN where it does, NOT SHOWN where every q carries one.

**The coset and the seed test's (ii) (DERIVED; MEASURED).** By U1f a move by u changes a click only if the tooth's
coset k_0 + c Z meets the strip [K - u, K - 1] and the tooth stands there. On the click world c = 3 over the record's
200 rounds (g = 48,000, MEASURED), k_0 = 76,217,143 = 1 mod 3 and K - 1 = 2 mod 3, so while every passing stays a
multiple of 3 a move by one unit, up or down (down, the strip is the place 0, which is 0 mod 3), changes no click at
any side (MATH1's S5 found 0 clicks moved in 300 rounds; this is why). That every passing stays a multiple of 3 at
every round is not derived here from the plan (OPEN; it holds on all 200 rounds read). The owner's seed test (ii),
worded "one hidden unit", therefore reads NOT SHOWN on the click world as laid; a move by two units or more
(K - 2 = 1 mod 3) can show, and half the key shows (section 3.3). On the mesh world (c = K over its 125 rounds) the
tooth never moves, so no move of any tooth changes a click there: (ii) reads NOT SHOWN on it for every move. The seed
test's "different clicks" needs U1's band in use.

### 1.2 U2: the tooth and the count

**U2a (DERIVED).** By U1c, over every q-word every tooth path stands, each exactly once. So to a reader of q alone the
count Q_n is sharp and the tooth k_n is flat over the whole dial: each of its K places is consistent with the record,
by exactly one passing sequence. The edge holds one tooth (0.1), so neither of its two clocks' lines holds it.

**U2b (DERIVED, no trade-off).** The count stands in every line, so no record makes the tooth sharp at the count's
expense; the pair is complementary in access (the two digits of kappa = K Q + k, the cylinder's lift, independent
coordinates of the passing sequence), not by a trade-off. Under a model of the board the tooth can be learned (a steady
passing makes the line a Christoffel word, whose one period fixes the tooth when gcd(P, K) = 1; MATH1 3.3): that reader
reads the board, not the clicks. The analogy is a number state's flat phase (named, not claimed).

**U2's no (MEASURED).** On a record that writes the teeth, every listing holds both the count and the tooth: U2 reads
NOT SHOWN at every listing (25,272 on click200, 41,376 on mesh125). And where K divides g, the tooth is one place even
to a reader who knows g: NOT SHOWN on the mesh world by structure. As a reading of a record with teeth, U2 is: does one
count from the birth stand with two teeth on one side? SHOWN where it does (click200), NOT SHOWN where it does not
(mesh125).

### 1.3 U3: a clock's count and the place's circulation

**U3 (DERIVED).** At a place where three clocks t, u, v stand on three laid edges (the owner's triangle: "each pair of
them is an edge"), each clock's line holds q, the sum of its sides: q_t = q_tu - q_vt + (its other sides), and so for u
and v. Adding any whole c' to the three oriented edges (q_tu, q_uv, q_vt) moves no line's q. So the clocks' counts fix
the edges' quanta only up to the circulation c = q_tu + q_uv + q_vt: a reader of the lines' q alone never reads it, a
reader of the sides reads it. This is MATH1 4.2's Hodge split read on the clicks (the circulation is the part in im C,
and B C = 0 makes every vertex sum blind to it), for every click form at a triangle, the first click's edges among
them; the third click's quanta are such circulations (L2, L4), which is the algebra under the Boss's reading of the
owner's "the third click is never seen alone" (no clock's own line carries the circulation's quantum alone).

**U3 read (MEASURED).** On click200: 4,212 places hold the triangle of the held, the giver and the taker on laid
edges; at 108 all three edges pass a quantum (the Boss's 108 of 4,212); the circulation is not 0 at 4,158 of the 4,212
(the least value -32; each value at a multiple of 27 places, the 27 alike sites): there a reader of the lines' q alone
misses it, SHOWN as that reader's loss. On a lone triangle a flow is a pure gradient exactly when c = 0, so most of
these are one edge's quanta, not a third click's; the lines' q are their sides' sums at all 4,212 (the guard's
identity, a code check). On mesh125: no place holds a triangle of three clocks on laid edges (the wave reaches the
hands through the Mesh alone): NOT READ. node-all's record writes every side's q, so the circulation is read from the
sides; the lines' q alone would miss it. (The sides are needed by the meetings, shadow.met, so they are no part of the
teeth question.)

### 1.4 Pairs not read today (OPEN)

- Place and motion (position and momentum): space is read only by light's echo between clocks (reading 7, OWED) and no
  world lays a moving clock (OWED): NOT READ.
- The third click's tooth and twin (bench only, not in src): its landing counts the wraps of tau when the circulating
  passing y is added, but tau also moves by the palindrome's shears (tau += 3 eta; MATH1 3.4), so (C) does not close on
  y alone and U1 does not carry over as it stands; its twin eta adds a coordinate no landing reads (MATH1 3.4's Z/3).
  What band its landings leave, and whether it survives a reader of the landings alone (THIRD7's and F4's horizons
  were read with the passings known, a board-informed reading), is OPEN.

## 2. What the relation depends on: the teeth in the record or out of it

### 2.1 Case (i): the click world reads q alone

- U1 and U2 hold as derived (1.1, 1.2). The click world's best reading of the passing is K Q_W, wrong by at most one
  quantum either way and by at most half a quantum from the birth; the tooth is unread. The board's passing stays out
  of the click world, as the owner's arrangement asks.
- Nothing the decoder reads as physics is lost: shadow.py reads q alone (0.2). The books (q + q' = 0 on every edge) and
  the meetings stay; the guard loses only its teeth's complementarity, a code check.
- The header's birth is structural ((K - 1) div 2 at the dial, laid by the loader); keeping it costs nothing to U1. The
  end's teeth, if kept, close the band once: the whole run's passing S_(0,N) = K Q_N + k_N - h becomes exact, every
  shorter window keeping its band. Keeping them out keeps U1 whole.

### 2.2 Case (ii): the click world reads q with k_before and k_after (node-all's record today)

- At every listing P = K q + k_after - k_before: the board's exact passing at that round, a board quantity written into
  the record. Over every silent gap, G = k_before(next) - k_after(prev) is the gap's exact passing. U1's band closes on
  every window whose ends are listings; it survives only inside silent gaps, where any sub-window's passing is fixed to
  [-(K - 1), K - 1] (DERIVED: q is 0 throughout, so the tooth stays in [0, K)) and the gap's total exactly.
- U2 is NOT SHOWN at every listing: count and tooth both written.
- So with the teeth written, the click world holds the fiber (the Boss's ruling, 07:5x: "the click world holds the
  fiber; 'hidden' means hidden from the board") and the board's passing at every line; the uncertainty of the click
  world is then only the order of the passing inside silent gaps.

### 2.3 What follows for the owner's question ("does the record keep writing the teeth?")

- DERIVED: U1 and U2 hold on every window of the click world only while the teeth stay out of its lines. While the
  record writes them, every listing reads the board's passing exactly, the two pairs are sharp at once there, and U1
  survives only inside silent gaps.
- DERIVED: no click-world reading of the decoder needs the teeth (0.2); the teeth serve the guard's faithfulness check
  and the recovery of the board's passing, and the latter is a board check by the Boss's ruling of 07:5x.
- The choice is the owner's. If he keeps the teeth, the uncertainty in the click world reads NOT SHOWN at every line
  and lives only in silent gaps. If he takes them out of the click lines (the birth in the header and, if wanted, the
  end's teeth for the books), U1 and U2 hold on every window but the whole run.

## 3. Read on the shipped worlds (MEASURED, each run twice)

### 3.1 The runs

- The worlds: S/unc1/worlds/click200 is examples/tensor24-click with its setting's ticks set to 200 (the only line
  changed; named click200; the shipped 5,000 rounds name a count past the width at round 3752 and write no record);
  S/unc1/worlds/mesh125 is examples/tensor24-mesh as shipped (125 ticks).
- Run by the copy's tools/tensor24_run.py, under nice -n 19, one process at a time, the load read before each
  (7.5 to 8.1 on 4 cores): mesh125 58 s and 50 s; click200 73 s and 94 s, each forward and back. Both records "exact".
  The two runs of each world are alike byte for byte in every line but the header's record name (run1, run2), and the
  ledgers alike byte for byte.
- Records: click200 12,638 lines (12,636 click lines, 4,212 places), sha256 of run1 750551cb5551e2b9515d0ac1f119922f042d814406619e2696dd1a6db3c3575c;
  mesh125 21,591 lines (21,589 click lines), sha256 of run1 57203d4eb35669efcfb670440ecefcfb7e6bd43e82f32c47376f4d7f9b002426.
- Read by unc1_read.py through the decoder's own reader (records.read, every guard, the sides' guard among them), from
  the click lines and the header's dial and birth alone. Run twice on run1 (outputs alike byte for byte) and once on
  run2 (alike but its name line).

### 3.2 The two worlds side by side

| reading | click200 | mesh125 |
|---|---|---|
| dial K, birth | 152,434,287, 76,217,143 (the half) | 3, 1 (the half) |
| sides listed | 162 own, 0 across (6 distinct histories: 27 alike sites x 6 sides) | 244 own, 488 across (610 distinct histories) |
| listings, with q not 0 | 25,272, 13,446 | 41,376, 36,192 |
| faithfulness (code check): adjacent listings k_before(next) = k_after(prev) | 17,982 of 17,982 | 39,288 of 39,288 |
| silent gaps, their passing G | 7,128, from -37,440,000 to 37,440,000 | 1,356, all 0 |
| passings' grain g, gcd(g, K), reachable tooth places K / gcd(g, K) | 48,000, 3, 50,811,429 | 30,000, 3, 1 |
| distinct teeth written | 283 | 1 |
| U1 from the birth: D = K Q_n - S_n = h - k_after | -75,771,435 to 75,771,435; 994 per mille of the half | 0 to 0 |
| U1 one-line windows: distinct q | 41, from -37 to 37 | 1,783, from -414,750,000 to 414,750,000 |
| U1 at q = 1 (and -1): distinct passings | 9, from 17,280,000 to 221,760,000; spread 204,480,000 = 670 per mille of 2 (K - 1) | 1 at every q: P = 3 q |
| U1: one q carrying two passings | SHOWN: 24 q's; 6 of 6 distinct sides (162 of 162 listed) | NOT SHOWN: 0 of 1,783 q's, 0 of 732 sides |
| U2: one count from the birth with two teeth | SHOWN: 1,620 classes; every side | NOT SHOWN: 0 |
| F2: clocks that meet; windows between consecutive meetings | 54 (2 distinct x 27 sites), 270 windows, none of own count 0 | 0: no place is a meeting (the q's run to 414,750,000), NOT READ |
| F2: D on the clocks' own sides | -117,668,574 to 83,520,000, inside [-(K - 1), K - 1] | NOT READ |
| F2: one (own count T, quanta Q) carrying two passings | SHOWN: 1 of 6 classes (T 6, Q -1: 3 passings, spread 20,160,000) | NOT READ |

Standing of the rows. The faithfulness rows are code checks. The rows reading S, D, G, g, the passings and the teeth
read the board's passing through the record's teeth: board checks beside the click readings, MEASURED. They show that
the band U1c derives is filled on the click world (994 per mille of the half from the birth, 670 per mille of the
full band at one quantum) and empty on the mesh world, where the q's are the passing over 3, a readout with no memory
(the Boss's ruling of 07:5x). The F2 row's SHOWN is thin: on 2 distinct clocks (x 27 alike sites) one class of three
windows. The 27 sites of click200 are alike (6 distinct side histories), so "162 of 162" is "6 of 6".

### 3.3 Two records alike on the board, one tooth apart (click-only; MEASURED)

unc1_twin.py loads click200 as the run tool does, moves the click tooth of round 1's busiest side (side 13, the held
and the giver's edge at site 0, its first passing 768,000,000; MATH1's S5b rule) and runs both lays 200 rounds.

| | tooth moved by half the key (76,217,143) | tooth moved by one unit |
|---|---|---|
| the board alike (a board check) | 200 of 200 rounds | 200 of 200 rounds |
| sides whose clicks differ | (13, 0) alone | none |
| rounds where the moved side's q differ | 122 of 200 | 0 of 200 |
| windows [m, n), 0 <= m < n <= 200 | 20,100 | 20,100 |
| largest abs(Q_W - Q'_W) | 1 | 0 |
| windows that differ by one | 10,088 | 0 |
| Q_n - Q'_n from the birth, values | -1, 0; the whole run's counts 1 and 1 | 0 alone; the whole run's counts 1 and 1 |
| U1f: Q'_n - Q_n = [k_n >= K - u] | 200 of 200 rounds | 200 of 200 rounds |
| rounds with the first lay's tooth in the strip [K - u, K - 1] | 97 of 200 | 0 of 200 (the strip is the place K - 1 = 2 mod 3; the tooth stays 1 mod 3) |
| end teeth | 47,622,856 and 123,839,999 (apart by the move, mod K) | 47,622,856 and 47,622,857 |

U1e reads SHOWN on the click world: the path differs at 122 rounds and the counts never by more than one quantum on any
window, and the end board is the same board. The comparison reads the two records' q's alone; the board row is the
board check beside it. Its no would be a window that differs by two: a board that read a tooth, or a q that is not the
carry's quotient. The unit move changed no click in 200 rounds, as the coset derives (1.1: the birth 1 mod 3, K - 1
2 mod 3, K 0 mod 3, the probe's line (g)): the room U1f gives a one-unit move is empty on this lay while the grain
holds, and the half-key move's room is the dial's upper half, where the first lay's tooth stood at 97 rounds.

## 4. Where it meets the third click's choice and Bell

The law of the choice (the owner, 03:3x): for each clock, nothing it can read before its click determines the outcome;
for the whole, no choice. Bell is read in the clicks (the owner, 07:59).

- **M1, the clock's own click past (DERIVED).** U2a is the derived form of R2's necessary reading: to a reader of q
  alone, a clock's click past fixes no tooth, so with its next passing unknown it fixes no next landing. It holds for
  every click that is a carry, the first click (which draws nothing) among them, so it is not the choice and reads no
  choice (the Boss's ruling of 05:3x: "the clock's own click past does not fix its landing", a necessary reading only).
- **M2, a reader of its past passings (DERIVED).** For a reader who holds its side's past passings and the birth,
  k_n = (h + S_n) mod K and the next click floor((k_n + P_n) / K) is fixed by the past and the present passing: the
  band is 0, as the Boss ruled at 07:5x ("on a lay the first click is fixed by its side's past"). In case (ii) the
  record itself hands every reader k_after at every line. So which reader the law means (the owner's batch question:
  "are a clock's sides, and its past board readings, what a clock can read?") decides whether U1 and U2 are any room at
  all; today's record answers it for the click world by writing the teeth.
- **M3, the path's freedom is one quantum (DERIVED; MEASURED).** U1e and U1f: two records alike on the board differ by
  at most one quantum on every window, however many rounds their clicks differ, and their difference at each round is
  one bit of the first lay's tooth. The owner's "the clicks differ, the end is the same end" is so bounded: the
  freedom of the path, for any carry form, lives inside U1's band, and where the band is unused (K dividing the grain)
  no tooth move shows at all. MEASURED on click200 (3.3): 122 rounds apart, every one of 20,100 windows within one; the
  unit move, by the coset, never apart in the 200 rounds.
- **M4, Bell (DERIVED, classical: Bell 1964, Clauser-Horne-Shimony-Holt 1969).** The tooth is a local variable: an
  edge's tooth sits at one Node-clock or across one Mesh, and its carry reads only that edge's passing, which reads the
  window there and across one Mesh (the act's locality, one Mesh a round). For wings read before either's setting can
  reach the other, each wing's outcome (plus or minus one) is a function of its own setting and of the hidden state
  (board and teeth); with the settings drawn independently of that state,
  S = E(a, b) + E(a, b') + E(a', b) - E(a', b') has
  |S| <= 2: per hidden state, A (B + B') + A' (B - B') is -2 or 2 (one bracket 0, the other plus or minus 2), and a
  mixture of such values stays within [-2, 2]. The 16 deterministic strategies give S in {-2, 2} (unc1_toy.py,
  section 5; the owner's 16). So the uncertainty U1 and U2 derive, however wide the band, cannot pass Bell's 2: it is
  of the hidden-variable kind, an uncertainty of what the record holds while the whole state holds every value (the
  law's second half). Passing 2 needs what the law names, the third click's draw reading the pair's one hand, or one of
  the two roads the Boss named OPEN (measurement dependence; a board influence that writes no click).
- **M5, Bell on node-all's records (NOT READ).** The act reads no setting, no draw stands in it, and the record names
  no pair event (R4 NOT READ, the Boss's ruling of 05:3x); so no CHSH is read on click200 or mesh125. OPEN, with the
  third click's build (bench only).
- **M6, the third click's band (OPEN).** If its tooth and twin are written into the record, every landing's room
  closes as in case (ii) (the next landing is the cat map's round on the written pair and the next passing). If they
  stay out, the record holds the landings alone, and the room is the pair's place in (Z/3D)^2 less what the landings
  reveal; THIRD7 and F4 read that horizon only with the passings known. Which the owner wants is the same question as
  2.3, asked again for the third click (MATH1's physicist, question 2).

Nothing above claims a choice, light, matter, a time or a place: the relations are what the click lines can and cannot
fix of the passing behind them, and Bell's bound is what such a hidden passing can do.

## 5. The probes and their outputs (S/unc1; whole numbers only; Rule3's carry the one division)

| file (S/unc1/...) | what | sha256 (first 16) |
|---|---|---|
| runs/run_worlds.sh | the two worlds by the copy's run tool, each twice; log runs/run_worlds.log | 5d3b6ae62da25c4e |
| probes/unc1_read.py | R0, R1, U1, U2, F2, U3, G0, G1 on one record, click lines and the header's dial and birth alone | 6d1d9b851678dab6 |
| out/read_click200.a.txt (and .b, .run2) | its output on click200 | f93600ff5f80cd84 |
| out/read_mesh125.a.txt (and .b, .run2) | its output on mesh125 | 4bb9c27b25375a4c |
| probes/unc1_twin.py | two lays alike on the board, one tooth moved (half the key, one unit), 200 rounds of click200 | 11ae8c4f74ad874d |
| out/twin_click200_half.a.txt (and .b) | the half-key pair | 788a06946e0e6400 |
| out/twin_click200_unit.a.txt (and .b) | the unit pair | 462f22571285d01e |
| probes/unc1_toy.py | T1 to T4 on the dials 3, 5, 7 over 4 rounds, exhaustive; the 16 CHSH strategies | 0b6a2b3647e81785 |
| out/toy.a.txt (and .b) | its output | 19aa48dfa0d5c1c2 |
| probes/run_probes.sh, run_probes2.sh, run_probes3.sh | the batches; logs out/run_probes.log, run_probes2.log, run_probes3.log | 7b73a2c4164e255f, 49652627bf0640cb, 39a47a245634f8ef |

The toy check (out/toy.a.txt): on K = 3, 5 and 7, no two passing sequences share one (q-word, tooth path); each of the
81 q-words with every |q| <= 1 stands over all K^4 tooth paths (81 of 81 on each dial); on every window from round 1
the consistent sums are exactly the 2K - 1 values, and from the birth exactly the K values (486 and 324 of 486 and 324
on each dial); 2 |K Q_n - S_n| <= K - 1 at every round; two births under one passing sequence never differ by more
than one quantum on any window, and do by one (21,609, 366,025 and 2,480,625 pairs). CHSH: S in {-2, 2}. The first
batch's twin outputs (before the line (f) was added) are kept in out/first_twin and agree with the second's lines (a)
to (e).

Every probe ran twice with its outputs alike byte for byte (S/unc1/out/run_probes.log), under nice -n 19, one process
at a time, the load read before each run (7.0 to 9.2 on 4 cores). The probes read the tree by joinpath and the
decoder's own reader; no float, root, table, search, sine or cosine; the gcd is Euclid's by repeated carry, a reading
outside the act.

## 6. For the Boss

1. To the owner's batch, beside "does the record keep writing the teeth?": with the teeth written, the click world's
   uncertainty reads NOT SHOWN at every line (2.2); with them out, U1 and U2 hold on every window but the whole run
   (2.1). No decoder reading of physics needs them (0.2).
2. U1's no is a lay whose key divides the passings' grain (the mesh world: g 30,000, K 3). The Boss's 07:5x ruling
   names a key finer than the grain as the owner's initialization; U1 is one more reason it matters, and it picks no
   key (no number is set here to make a band appear).
3. The seed test's (ii) as the owner words it ("one hidden unit") cannot show on the click world as laid while every
   passing stays a multiple of 3 (the coset, 1.1; true on all 200 rounds read), nor on the mesh world for any move
   over its 125 rounds. MATH1's S5b showed (ii) with half the key. The test's wording, or the move it uses, may want
   the owner's eye.
4. Bell: this uncertainty is local and cannot pass 2 (M4). It should be cited only so, never as a road to 2 r2.
5. The third click's band waits on the same record question (M6).

## Solution24

The click world's uncertainty, as the engine stands: the count is the passing rounded to the nearest quantum (from the
birth), and the passing behind any window is fixed only to within one quantum either way; the tooth is flat over the
dial to a reader of the clicks. Both are the carry's remainder kept on the edge, both vanish when the record writes the
teeth, and both are of the hidden-variable kind that Bell bounds by 2.
