# The time gear's own law: the 00 row's split, derived locally

The Boss's deriver, 2026-10-30, 18:5x UTC. Derived beside EDGE2 (the tooth on the edge, the half-open convention, the
owner's word), after the readers' reports (mc_math, mc_phys) and under the owner's words of 18:1x UTC through the Boss:
"No price is allowed. Solve it with time forward and backward"; "the return in time is simply more gears, with
differences between them". Whole numbers; the engine's carry the one division in every probe but one, named below, which
computes a root by a search because the form it measures is a root. The example universe's trains through the loader;
src untouched; nothing written in any worktree. Files beside this page: tg_lib.py (the harness), probe_tg1 to probe_tg9
with their .txt, notes_01_derivation.md, notes_02_forward_backward.md. Status: DRAFTED, for a pair of readers; the
result is a theorem and a decision for the owner, not a form READY for code.

**The result in one line.** With time taken forward and backward, the in edge from the state the round reads and the
out edge from the state it produces, the 00 row's own law is unique: D_in^2 + D_out^2 = 8 W(a)^2 + 4 push + s - s+;
it keeps one cone, is a bijection with the same act both ways, writes nothing and is nature's form for the clock's own
motion (sqrt(W) v kept); its one division is an integer root. No carry meets the four conditions together: every carry
form of the 00 row pays with a second cone (the cut), a line outside the state (the order), a register pumped by the
clock's own jitter (the carried dial), a pair that parts at the frozen hand (the twin), or the edge's breathing physics
(every one-cone carry at W). The owner chooses: the root for the one gear whose count is its own clock, or a price.

## 1. The clock

Every gear's tooth lives on the edge between its two slots, in the dial D = W(before) + W(now) (EDGE2). The 00 gear is
the clock itself: its count is W, so the dial of its next edge, W(now) + W(next), is a count it has not yet made. The
question is what the clock's own gear reads for its teeth. Three answers are on the table from before (the cut: its
rest; the order: its now slot twice; the edge: the fixed point, no act), and this page adds three (a register, a twin,
the symmetric read) and judges all six by the owner's four conditions: one cone, a bijection on the state, nothing
written, no price.

## 2. The algebra

**Two conditions on any pair of dials** (notes_01). Write D_in(S) and D_out(S) for the dials of the round that reads
the state S. The tooth was split at 2 D_out(S_(t-1)) and is weighted by 2 D_in(S_t) in N = 2 (D_in v + 2 push) + s, so
(C1) D_out(S_(t-1)) = D_in(S_t) or (v, s) -> N collides; the mirror M swaps the slots, so (C2) D_out(S_t) =
D_in(M S_(t+1)) and D_in(S_t) = D_out(M S_(t+1)) or the run back is another act. The edge meets both because W(x) + W(y)
is the same number read from either end; the price is W(next).

**Theorem 1 (two slots, one carry).** For a gear whose own count is its clock, an in dial that moves with its before
slot makes blocks over the velocities of unequal width (gap -(2 v + 1) for W(b) + W(a), -(4 v + 2) for 2 W(b)), so the
forward map collides; an out dial that moves with its next count leaves integers under no quotient and under two (the
gap (2 q + 1) dD); (C1) then makes the in dial the now slot's alone and (C2) makes it constant. The only two-slot
one-carry act of the 00 row is the cut. Measured exhaustively (probe_tg1): the self-read edge 36 in-side collisions and
145 integers under no q of 312; the lag (2 W(b) in, 2 W(a) out) 30 collisions, 202 run-back misses; the order 72
collisions (the readers' 96 of 625 on another lay); the cut 0 and 0.

**Theorem 2 (the centre is forced).** Let the out dial move with the quotient, D_out(q) = W(a) + W(a + q), and let the
cell of q sit at any centre C(q). Tiling at fixed v and the run back (R) together force C(q) = 2 q D_out(q) - q^2 - v^2
+ c (notes_02): the round's law is D_in^2 + D_out^2 = 8 W(a)^2 + 4 push + s - s+, symmetric under (D_in, s) <->
(D_out, -1 - s+), as term 11's click runs back only with X(S) + X(S+). Its act: M = 8 W(a)^2 - D_in^2 + s + 4 push,
D_out the u with u (u - 1) <= M < u (u + 1), s+ = M - u^2, W(next) = u - W(a). The cells [u (u - 1), u (u + 1) - 1]
tile; the quotient is the integer nearest sqrt(M): a root. With the carried estimate c = 4 W(a) - D_in and R = 4 push -
2 v^2 + s, u = c + k where k is the cell of R among [k (2 c + k - 1) - c, k (2 c + k + 1) + c - 1]; the k^2 at the
cells' ends is what no carry does, and k = 0 is the carried dial. Any other centre, e.g. the cells laid end to end from
q = 0, keeps the forward bijection and loses the run back (probe_tg1: 95 misses of 176).

**Theorem 3 (a register is an involution).** A dial held in the state beyond the two slots meets (C1) by itself; (C2)
makes its update an involution at the pivot, f(a, f(a, D)) = D, so D -> g(a) - D; one cone on a standing clock fixes
g = 4 W(a). Its departure E from the edge's dial obeys E+ = -E - (W(next) - 2 W(now) + W(before)): the alternating sum of
the clock's second differences, damped by nothing, since an involution contracts nothing. Measured (probe_tg1): the
carried dial 0 collisions and 0 misses on 2,184 states; the mutant D + 1 (injective, no involution) 2,184 misses; the
mutant D + 2 (W(a) - W(b)) 328 collisions.

**The twin** (notes_02, lead 2). The 00 row as a forward half A and a backward half B, each the other's clock: A steps
on B's two slots (2 W(b_B), 2 W(a_B)), every other row on (W(b_B) + W(a_A), W(a_B) + W(a_A+)), B on A's new slots
(2 W(a_A), 2 W(a_A+)); the mirror swaps A and B. The run back is proved exact in notes_02; no register, no root, no cut.
The two halves are one field sampled at staggered half-rounds; their difference is a free field.

## 3. The board: what was measured

The example universe through edge_lib's board, the loader's lay (every row reads the 00 slot, the 00 row included, no
cut), the half-open split, one carry. The cone on a line of 6 (the mode 2A, A, -A, -2A, -A, A, A = grip / 1000, 6,000
rounds); the run back, the books and the 24 on the cube of 3, 12 rows at 27 sites, 40 rounds; the courses on one gear.

| form | the 00 wave's T_light^2 / T_00^2, W = 2 and 4 rest (1000 one cone) | run back, cube, 40 rounds | books | the 24 | the 00 gear's own free course (probe_tg9) |
|---|---|---|---|---|---|
| the cut (readers) | 2014, 4041 (W / rest) | exact | exact | 24 | v kept on its rest dial |
| the order (readers) | 1012, 1009 | 96 collisions of 625; a booked line | P_00 drifts | 24 | - |
| the carried 00 | 1000, 1000 | 40 of 40 and rewound on standing, rising, varying lays; falling lays end where the clock reaches 0 | 0 misses of 480 per lay | 24 at every round | W v kept; the register pumped at the half count: departure 20,001 of a dial 60,000 at round 30,000 |
| the carried board | 1000, 1000 | as above, one pass, no row first | 0 misses | 24 at every round | as above |
| the twin | 1000, 1000 | 40 of 40 and rewound | 0 misses of 14,040 gear-rounds | 24 at every round | W v kept; the halves part at the half count: A frozen at 19,999, B at 40,000 |
| the symmetric form (a root) | 1008, 1006 (the wave's mean drifts: nature's v^2 / 2 term) | 40 of 40 and rewound | the round's identity 0 misses; other rows 0 | 24 at every round | nature's: sqrt(W) v kept within 1.5 percent at v0 = 100 (W 3,115,855 against nature 1000, against W v kept 1386); at v0 = 1 the quotient never falls (W linear) |

Details, each from its probe's .txt:
- probe_tg2: the carried forms' 00 wave crosses zero at the same rounds as light's (275 periods over 5,965 rounds at
  W = 2 rest; 194 over 5,961 at 4 rest): 1000 permille; the cut 391 periods over 5,976 (2014, 4041); the order and the
  act as built 34 over 733 (1012) and 48 over 1,468 (1009), their wave drifting off its base after that.
- probe_tg3: untick(tick s) = s 40 of 40, rewound, books 0 of 480, departure 0 on the standing lay, 0.12 grip on the
  rising lay (the clock's own slowing), 0.5 grip under a mode of a grip on the 00 row, 0.02 grip under a hairspring
  swinging the clock by a grip; the self-driven falling lays end at round 7 from 12 grips and round 31 from 60 grips,
  the clock reaching 0 (D v kept hastens a fall); 78 to 82 bits.
- probe_tg4: 24 of 24 at every round, standing, rising, falling, and with the clock differing site by site.
- probe_tg5: the register laid off by k stays (-1)^t k for ever (an involution damps nothing); a hairspring f = D on the
  00 row (omega = pi, the leapfrog's edge) pumps the departure 4 A a round, linearly (-1.6 x 10^15 counts at round 400
  from A = 10^12), below the beat it stays within 6 A; a clock falling to a third in one round makes 4 W(a) - D = 0 and
  the promise names round 1; exhaustive two-gear states on one Node-clock, 87,024 and 261,072: 0 collisions, 0 misses.
- probe_tg6: with the clock given from outside, the carried dial is the edge act state for state on the uniform course
  (0 of 30,001 differ, departure 0) and the carried root dial the root dial (0 differ) on the smooth L course (v^2 W
  999, A / A0 1000, T^2 / W 992 to 1004); on probe_root's staircase (L + 1 every 300 rounds) the departure reaches 199,
  the dial's own size at L = 100, and the falling course breaks the promise (the hostile case: kicks of even spacing).
  The 00 gear its own clock under the carried dial: rising v0 = 1 from W = 10,000, departure 20,000; under the carried
  root dial from L = 100, departure 29,900; the hairspring's halves in proper ticks 1314 and 908 permille (the register
  off its dial).
- probe_tg7: the symmetric form exhaustive, 0 collisions and 0 misses on the lawful states (W(b) >= 1); the free gear
  v0 = 100 from W = 10^6: v^2 W 1005, 1014, 995, 1012 permille over W x 3 (nature 1000); the cube 40 of 40 and rewound
  on three lays, the identity and the books 0 misses, 24 at every round.
- probe_tg8: the twin on the cube, 40 of 40 and rewound, books 0 of 14,040, 24 at every round; the halves laid a grip
  apart stay a grip apart (standing), part by 1.7 grips at W = 33 grips on the rising lay (the difference scales with
  W), and a mode laid on A alone leaves a 2-grip wave in A - B.
- probe_tg9: the three forms on one course (section 4).

## 4. The physics behind the clicks

The clock's own gear must run on light's cone: a 00 wave faster than light is a second metric mode, which no reading of
nature gives (the physicist's item 2); so the 00 row's dial must be its own 2 W, and the cut is out. The remaining
forms all do that; what tells them apart is the clock's own motion.

- **The edge's physics is the price the owner refused.** Every one-cone carry at W puts the velocity's weight at the
  dial, so it keeps 2 D v + s with D ~ 2 W: W v kept, d_t (W d_t a) = F, the CHOSEN form whose amplitude breathes as
  W^(-1/4) within a swing (mc_phys item 3). The carried dial and the twin both inherit it (probe_tg9: 999 and 1002
  permille against W v kept at v0 = 100 and -10, 612 and 839 against nature).
- **Nature's form is the symmetric read.** 4 W (q - v) + q^2 + v^2 = 4 push + s - s+ is W dv/dt + v^2 / 2 = F with
  dW/dt = v: sqrt(W) d_t (sqrt(W) d_t a) = F, the lapse's own equation, at W linear in the count (no W = L^2), with the
  push entering whole (no floor). Measured: sqrt(W) v within 1.5 percent over W x 3 (probe_tg7 B), 1000 and 1002
  permille at the end of the v0 = 100 and -10 courses (probe_tg9 D). Its one quirk: at |v| = 1 count a round the
  tooth drifts 2 a round while the dial grows 2 a round, so the quotient never falls and the clock runs linearly, the
  act as built's course (at |v| >= 2 the tooth overflows and the quotient falls as nature has it; at v = 0 every form
  freezes a sub-half-count momentum, the mathematician's frozen hand).
- **The register's pump is the clock's own.** Once the 00 gear's momentum meets the half count (round 10,000 on the
  v0 = 1 course), its whole velocity jitters 1, 0, 1, 0: a second difference of alternating sign every round, the
  Nyquist drive of the involution's neutral mode, and the reflected dial grows 2 a round for ever (the dial 74,999
  against 2 W 57,498 at round 27,500, the course W 29,999 instead of 26,458). No lay avoids it: every free clock reaches
  the half count as its dial grows. At the real calibre the same jitter runs at the count level; its share of the dial
  is 2 counts a round against 2 W ~ 10^23, growing without bound where the jitter's spacing is even.
- **The twin parts at the frozen hand.** The halves' dials differ by one round of the clock's change, so one half meets
  the half count first and freezes while the other, whose dial then stands still, runs on at its whole velocity for
  ever (A at 19,999, B at 40,000). The free difference of the two halves is unstable in whole numbers.
- **The root dial beside.** With W = L^2 the involution D -> 4 L(a) - D keeps L v, nature's, with no root in the act;
  it is the same register with the same pump (departure 29,900 from L = 100, probe_tg6 B), plus the law change (6 den
  Gamma^2 is no square) and the push at the pivot's root (the fwdback deriver's matter). The symmetric form at L keeps
  sqrt(L) v, the wrong power: nature is linear at L (the fixed point, no act) or quadratic at W (the root); neither is a
  carry.

## 5. What the owner decides, and the law line each form would change

**No carry meets the four conditions.** That is the theorem of this page, proved in section 2 and measured in sections
3 and 4. The forms and their prices:

| form | one cone | bijection, same act both ways | writes nothing | the price | the law line it changes |
|---|---|---|---|---|---|
| the cut | no (2014, 4041) | yes | yes | a second cone | load.geared: the 00 row's teeth at rest (one row apart: an exception) |
| the order | yes | no (96 of 625) | no (a booked line) | a line outside the state | the act: the 00 row first on its now dial, a line kept |
| the carried dial | yes | yes | yes | the edge's physics; a register pumped by the clock's own jitter | the state: a dial per gear; the act: D+ = 4 W(now) - D |
| the twin | yes | yes | yes | the edge's physics; the 00 row doubled, the halves parting at the frozen hand | the state: two halves of the 00 row; the act: A, the rows, B, in turn |
| the symmetric form | yes | yes | yes | none measured but the quirk at one count a round | the act of the 00 row alone: D_in^2 + D_out^2 = 8 W(now)^2 + 4 push + s - s+, a root (decision 41) |

The symmetric form's law line: "the gear whose count is its own clock splits its round by the square: the squares of its
two edges' dials sum to eight times the square of its teeth at the pivot, plus four times the push and the tooth's
change; its quotient is the whole count nearest the root". It touches Postulate 6's "linear in c" nowhere (W stays
rest + c) and decision 41's "no root" everywhere. By decision 41 it goes back to the owner as a finding: the one gear
whose teeth are its own count needs the one division that is not Rule3's.

**What this page does not do.** It writes no code and names no form READY. The moving clock's form for every other
row is the fwdback deriver's (scratchpad/fwdback/); whatever it finds, the 00 row's own law stays this page's theorem,
since the fixed point is the 00 row's alone. OPEN: the owner's word on the root against the prices; the symmetric
form's course at |v| = 1 against nature's (a second tooth for the velocity's fraction?); the readers' pair.

## Solution24

1 (does it follow by itself: no two-slot carry gives the 00 row its own dial but the cut, so the law does not follow;
what the clicks show is named, one cone and the clock's own course); 3 (the big things only: the dial, the mirror, the
carry, the involution, the root; a strength the law leaves free is named CHOSEN, here the edge's W v); 4 (four layers);
6 (the books: P = 2 D v + s per gear in every carry form, the round's identity in the symmetric form, 0 misses; the run
back the same act on the mirrored state, every form judged by its own mirror); 7 (nature the test: the cone, then the
clock's own course, where the edge's physics and the register's pump are named, never hidden); 8 (run locally, probes
on the real act); 9 (for a pair); 10 (one law of the dial for every carry: the half-open split throughout; the
involution D -> 4 W - D is the mirror's own shape w - 1 - r on a dial).
