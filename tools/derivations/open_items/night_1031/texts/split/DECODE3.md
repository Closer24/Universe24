# DECODE3: the decoder's readings of the three clicks, as rules for writer C

The Boss's deriver of SPLIT, 2026-10-31, 04:4x to 05:1x UTC. **Status: DRAFTED, for writer C and a hostile pair.** It
follows the owner's word ("... and then we will also know how to make the decoder") and the Boss's ruling of 04:4x
UTC: one click line for all three clicks, in schema 1.4. Big Pic's stage 1 records test it where they reach
(origin/bigpic-3clicks cf4126ff5).

**Files** (scratchpad/split/):
- decode3.py, run twice: decode3_run1.txt = decode3_run2.txt;
- st1/, Big Pic's stage 1 files, copied unchanged;
- st1run/, my runs of his edgeclick.py on node-live 1794d474b's src (split/nl/src, with the shipped click and mesh
  worlds beside it in split/nl/examples/):
  - the click world, first (carried) and third (turned), 200 rounds;
  - tensor24-clickswap, the click world's files with trains 3 and 4 (giver and taker) exchanged, gears with them.

Run one at a time, before the quiet window.

The worlds here are board worlds: the shipped example files, examples/tensor24-click and examples/tensor24-mesh.
Every reading below is a reading of a record, which the click world holds. Applied to stage 1's records, it is a
test of the rule, not a claim of physics.

## Verdict

- **The rules are below, each with what it reads, its rule, how it fails and its no.** Every count is a whole number,
  and every ratio is whole thousandths by Rule3's carry, th(a, b) = carry(1000 a, b, 0)'s quotient. There is no float
  and no root: a correlation is read as r^2 with the covariance's sign.
- **Stage 1's records give the following** (MEASURED, two runs alike):
  - **R1:** my runs reproduce Big Pic's digests exactly, first and third.
  - **The books:** they close at every place, 0 of 4,212 and 0 of 4,158 open, and every line's q is its sides' sum.
  - **The place's structure:** every one of the 27 sites is a triangle.
  - **The swap covariance:** the first click reads exactly swapped, 10,827 of 10,827 lines. The third click does not:
    the records part from round 8, with 7,317 of 10,719 lines alike. That is the turn's sense on the real act, and it
    is the label rule's NOT SHOWN.
  - **Lives on the one slow edge, (3, 4):** var over mean^2 931 thousandths in the third click against 69 in the
    first.
  - **R2** (Big Pic's cmp): 298 lines differ from round 18, all at Node-clock 0, in the third click; none in the first.
- **Stage 1's records cannot give:**
  - the weights or the shares against them, since they hold no tooth and no dial;
  - the edge closure q_tu + q_ut = 0 as a test that can fail, since they hold one c per edge;
  - CHSH, since they hold no pair.
- **One field and one line rule the writer must settle:**
  - A train line lists every side of its clock at that place and round, q_tu = 0 included, once any side carries.
    Without that, the split's weights at a take lack the takers that did not land.
  - Each side's k_before is read after the round's turn, just before its carry. Otherwise x = D q + k_after - k_before
    holds only in the first click.

## 0. The record the rules read (schema 1.4, the Boss's ruling)

- **A click line:** {"kind": "click", "round": r, "site": x, "train": t, "q": q, "sides": [[u, q_tu, k_before,
  k_after], ...]}, written for every (round, site, train) where a side carried.
  - q is the sum of the sides' q_tu.
  - u is the other clock of the edge at the same site.
  - q_tu is the edge's quotient at t's end.
  - k_before and k_after are t's tooth on that edge before and after its carry.
- **The header** carries each edge's dial D (on stage 1, the key times 3: 152,434,287 = 3 x 50,811,429) and the teeth's
  birth, (D - 1) div senses. They are read from the header, never typed.
- **The end line** carries every edge tooth at the run's end.
- There is no Third record and no label. A clock is (site, train), as schema 1.3 has it.

**A place** is (round, site). **The place's structure** is read from the sides alone:
- the clocks meeting there are the line's train and every u in its sides;
- its edges are the pairs {t, u};
- a site's structure is the union over its places.

Two clocks alone meet where the site has one edge. Three clocks meet where three clocks are pairwise joined, a
triangle; n clocks give the edges among them.

## 1. The first click: the books edge by edge

**Reads:** every place's lines.

**Rule:**
- (a) For every place and edge {t, u}, t's line holds the side (u, q_tu) and u's line holds (t, q_ut), with
  q_tu + q_ut = 0.
- (b) Their teeth are complementary, k_before + k'_before = D - 1, and so are their k_after.
- (c) A line's q is the sum of its sides' q_tu.
- (d) The place's lines sum to 0, which follows from (a) and (c).
- (e) Each side's passing is x_tu = D q_tu + k_after - k_before, the carry's law, and the two ends' passings are
  opposite: x_tu + x_ut = 0.

**Fails:** NOT SHOWN at the first place where any of (a) to (e) fails, naming it. NOT READ at a line lacking a field.
NO CLICK where no line is written.

**Its no:** each of the following must read NOT SHOWN:
- one side's q negated;
- a line's q one off its sides' sum;
- one tooth one off its complement;
- an edge's side in one clock's line with no side in the other's.

**On stage 1:**
- (c) and (d) hold at every place of both records: 0 places open, and 0 lines off their sides' sum. Stage 1 sides
  carry an edge index, not u, so the decoder named the edges' clocks from places where an edge carried alone. Edge
  (2, 4) never carries alone and was named by the triangle's elimination, so 1.4's u is needed to read it directly.
- (a) holds by stage 1's format, one c per edge, and cannot fail there.
- (b) and (e) are not readable, since stage 1 holds no teeth.
- The mesh world's one edge gives first and third records byte for byte alike (Big Pic's edge_mesh_*.txt), the
  one-edge control.

## 2. The split click: the weights from the sides, with no new field

**Reads:** the lines at places whose site has three clocks or more.

**Rule:**
- At such a place, a clock t whose line lists two sides or more has passings x_tu = D q_tu + k_after - k_before on
  each side.
- t gives along the sides where x_tu < 0 and takes where x_tu > 0. That is a reading of a recorded number, not a
  test in the act.
- The split's weights at that place and round are w_u = x_tu over the sum of x_tv over t's sides of one sign, kept as
  the pair of whole numbers (x_tu, X_t).

**Fails:**
- NOT READ where a side lacks a tooth, or where the line omits the sides with q_tu = 0, since a non-landing taker's x
  is then missing.
- NOT SHOWN where the far side's passing is not the negative, x_tu + x_ut != 0, which is (1e).

**Its no:** a record with one side's k_after one off must read NOT SHOWN at that place.

**On stage 1:** not readable, for lack of teeth and a header. Its sites are all triangles (27 of 27), so every place
would read weights under 1.4. Stage 1's passings are David's split flows, the coupling's own. The third click's
passing k a_giver s_i (THIRD5) is THIRD6's to write into the same field.

## 3. The third click: which side lands, and its readings

**Which side lands:** at a triangle place, the sides of a giving clock with q_tu != 0. Each landing names its taker u.
A side with abs(q_tu) > 1 lands abs(q_tu) quanta in one round. On stage 1's click world, edges (2, 3) and (2, 4) pass
about 3.6 and 10.6 quanta a site-round, so their timing is the passing's, not a draw's. Only (3, 4), about 0.07 a
site-round (0.055 in the first click), reads a draw.

**(3a) The shares against the weights, in blocks of one record** (P1's click-world reading; SPLIT2's physicist's
MINOR 1).
- Rule:
  - Cut the record into B blocks of consecutive rounds, B a reading's parameter named before reading.
  - Per block and taker u: N_u is the sum of abs(q_tu) over the block's landings. E_u in whole thousandths is the sum,
    over the block's take rounds, of carry(1000 n_r x_tu,r, X_r, 0)'s quotient, where n_r is the quanta landed that
    round. The truncation is at most one thousandth a round, named.
  - z^2 in thousandths is (1000 N_u - E_u)^2 / (1000 E_u), by the carry.
  - Read twice, on the first half of the blocks and on the second.
- Fails: NOT SHOWN where both halves' summed z^2 pass the chi-square's upper 5 per cent point for their blocks, a
  cited reference value. NOT READ where (2) is.
- Its no: a record landing every quantum on its first taker must read NOT SHOWN.
- On stage 1: not readable, since there are no weights.

**(3b) The Fano factor against window length within one record (R3).**
- Rule:
  - Per side, for windows of w rounds with w = 1, 2, 4 and so on up to a quarter of the record (a reading's ladder,
    named), count each window's landed quanta C_k.
  - F(w) = var_k C_k over mean_k C_k, in thousandths.
  - Read twice, on the record's halves.
- Read: independent landings at a steady passing give about 1,000 at every w. A carried form falls toward 0 as w
  grows. A passing that moves raises F at large w; read F where (2) shows the weights steady.
- Its no: the first click's record, whose regularity grows with w, must not read as independent.
- On stage 1 the decoder had a sister record of the same board: the first click's record of one lay, where the board
  runs alike because the click pushes nothing into the gears. So it read the turn's own share directly: var(third's
  quanta less first's) over the quanta passed.

  | Edge | w = 5 | w = 10 | w = 20 | w = 40 |
  |---|---|---|---|---|
  | (2, 3) | 171 | 484 | 464 | 1,911 |
  | (2, 4) | 43 | 572 | 500 | 1,142 |
  | (3, 4) | 979 | 1,504 | 736 | 290 |

  The turn's share grows with the window on the fast edges, a wander, as Big Pic's readings.py names it. A sister
  record is a board luxury the click world does not hold; 1.4's F(w) needs none.

**(3c) The correlation between takers.**
- Rule: at a triangle site, the giving clock's two sides' window counts give cov's sign and r^2 = cov^2 / (var var),
  in thousandths, per w, read twice.
- Read: independent takers give r^2 near 1000 / K for K windows.
- On stage 1, on the held clock's two edges by the sister-record difference: r^2 of 41 (+), 5 (-), 214 (-) and 65 (-)
  thousandths at w = 5, 10, 20 and 40, over 1,080 to 135 windows. At w = 20 that is far above chance's 4, though
  windows of one site are not independent. Named, not settled.

**(3d) Lives by the exponential law.**
- Rule: per side, the gaps in rounds between consecutive landings, and var over mean^2 in thousandths. The whole-round
  law's reference is 1,000 - th(1, mean gap): for a landing chance p a round, var over mean^2 is 1 - p. Read twice.
- On stage 1, as (gaps, mean gap in thousandths of a round, var over mean^2):

  | Click | (2, 3) | (2, 4) | (3, 4) |
  |---|---|---|---|
  | first, carried | 4,023, 1,335, 124 | 2,349, 1,218, 114 | 270, 7,000, 69 |
  | third, turned | 4,023, 1,335, 124 | 2,403, 1,235, 132 | 351, 5,153, 931 |

  - The first click's lives are regular on every edge.
  - The fast edges' lives are the passing's in both clicks.
  - The slow edge's third-click lives sit near the law's spread: 931 against the whole-round reference of about 806.
    Its first-click lives, at 69, are a clock striking.

**(3e) The swap covariance** (the Boss's ruling: one world's counts are relabelling-covariant).
- Rule:
  - Take two records, one from a lay and one from its swap: two clocks of the same kinds and couplings exchanged in the
    files, their gears with them.
  - Relabel the second record's clocks back, which reverses the swapped edges' orientation by itself.
  - The two must be equal line for line, in the schema's order.
- Fails: NOT SHOWN at the first round with a line apart.
- On stage 1 (tensor24-clickswap, trains 3 and 4):
  - first click: SHOWN, 10,827 of 10,827 lines alike, no round apart;
  - third click: NOT SHOWN, 7,317 of 10,719 lines alike (10,800 in the swapped), apart from round 8 at 65 rounds.
  - That is the triangle turn's sense on the real act: it takes the triangle's roles from the trains' order in the
    files, a label behind a count. It is the no this reading must catch. SPLIT3's swap-symmetric palindrome is THIRD6's
    road.

**(3f) R2: the law's own reading for one clock.**
- Rule: two records from lays one hidden unit apart, in a tooth no line writes, must be alike in every line up to a
  round r* and apart from it. SHOWN where r* exists.
- Its no: a carried record, where no line ever differs.
- On stage 1 (Big Pic's cmp_click_200.txt, not rerun): the third click differs at 298 lines from round 18, all at
  Node-clock 0, so SHOWN. The first click differs at 0, so it is the no.

**(3g) R1: one lay, one record.**
- Rule: one lay run twice gives one record byte for byte: the digest of its click lines, and the record whole.
- Its no: a run with any input from outside the files.
- On stage 1: SHOWN across two sessions. My runs give Big Pic's digests, first 1d221a1b... and third 59d3a811...,
  exactly.

## 4. At a pair: CHSH from the click counts and no signal (R4; waits on Big Pic's stage 4)

**Reads:**
- two sites, A and B, whose landings belong to the pair's one hand, its clocks named by their sides;
- each place's setting as the record names it, the side pair its draw read, drawn by the act and never typed;
- each landing's outcome, + or -, as the taker its side names.

**Rule:**
- For each setting pair (a, b), count N_ab(++), N_ab(+-), N_ab(-+) and N_ab(--).
- E_ab in thousandths is th(N++ + N-- - N+- - N-+, N_ab).
- S = E_00 + E_01 + E_10 - E_11, in thousandths, with no root: S above 2,000 passes the local bound, and the pair's
  limit is S^2 <= 8,000,000.
- No signal: A's share of + at setting a, read under b = 0 and under b = 1, as th(N_a+|b, N_a|b). The two must agree
  within the binomial's spread, z^2 in thousandths by the carry, and B's alike. Read twice, on the record's halves.

**Fails:** NOT SHOWN where S <= 2,000 in both halves, or where a share moves with the far setting beyond the spread.
NOT READ where a setting is not in the record.

**Its no:**
- the local road, each place drawing from its own past: S <= 2,000 (Big Pic's toy 2.0000);
- a draw that reads the far setting: no signal NOT SHOWN.

**On stage 1:** there is no pair, so NOT READ.

## 5. What stage 1's records can and cannot give

| Reading | Can | Number on stage 1 |
|---|---|---|
| R1 | yes | digests equal to Big Pic's, first and third |
| the place's structure | yes, partly | 27 of 27 sites triangles; one edge named by elimination |
| (1) the books, a line its sides' sum | yes | 0 of 4,212 and 0 of 4,158 open; 0 lines off |
| (1) edge closure, complementary teeth, the passing | no | one c per edge, no teeth |
| (2) the weights | no | no teeth, no header |
| (3a) the shares against the weights | no | no weights |
| (3b) Fano against the window | yes, by the sister record | see (3b) |
| (3c) the takers' correlation | yes, by the sister record | r^2 41, 5, 214 and 65 thousandths |
| (3d) lives | yes | (3, 4): 931 third, 69 first |
| (3e) swap covariance | yes, with a swapped lay | first SHOWN; third NOT SHOWN from round 8 |
| (3f) R2 | yes (Big Pic's cmp) | third 298 lines from round 18; first 0 |
| (4) CHSH and no signal | no | no pair |

**OPEN for writer C:**
- the sides with q_tu = 0 on a line;
- k_before after the turn;
- D and the birth in the header;
- the end teeth in the end line.

**OPEN for THIRD6:** a sense-free turn (3e); the passing k a_giver s_i written into the sides (2).

**OPEN for Big Pic's stage 4:** the pair's settings in the record (4).
