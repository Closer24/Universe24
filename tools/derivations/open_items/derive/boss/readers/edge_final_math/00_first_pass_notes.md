# First pass notes (before reading the earlier readers' reports)

Read: EDGE2.md, edge_lib.py, probe_halfopen/.txt, probe_root/.txt, probe_plan/.txt, probe_momentum/.txt,
probe_edge/.txt, probe_record/.txt, probe_pump.txt; carry.py, step.py, load.py, state.py, contract.py;
ALGEBRA.md lines 100 and 122; ARCHITECTURE.md Solution24.

## Algebra as I rebuild it (half-open)
- split_up(n, m): carry(n + D, 2D, 0) -> (q, r0); s = r0 - D in [-D, D-1]; n = 2Dq + s. Bijection Z -> Z x [-D, D-1]: exact.
- Flip: n -> -1 - n gives (q, s) -> (-q, -1 - s); -1 - s in [-D, D-1]. (iii) on r0 = s + D: m - 1 - r0 = D - 1 - s -> s' = -1 - s. Exact.
- Shift n -> n + 2Dk: (q + k, s) exact for every k (floor carry).
- Round: N = 2 D_in v + 4 push + s split at 2 D_out, D_in = W(b)+W(a), D_out = W(a)+W(a+).
- Run back: mirror (a+, a, s') -> (a, a+, -1 - s'); D_in' = D_out; push' = push(a) same; N' = 2 D_in (b - a) + (-1 - s);
  split at 2 D_out' where D_out' = W(a) + W(b) = D_in (00 row's provisional split exact because its dial is constant under the cut);
  -1 - s in [-D_in, D_in - 1] => q' = b - a, s'' = -1 - s; mirror -> (a, b, s). Exact given the promise s in [-D_in, D_in-1], D_in >= 1, D_out >= 1.
- 24: flipped row (a, b, s) -> (-a, -b, -1 - s): N -> -N - 1 (push odd, W even under the turn), split gives (-q, -1 - s'). Exact.
- Books: per gear 2 D_out q + s' = N = 2 D_in v + 4 push + s, so P_(t+1) - P_t = 4 SUM push per gear, exact.
- Still clock D = 2W: s = 4r - D gives N = 4(Wv + push + r) - 2W = 4Wq + (4r' - 2W), 4r' - 2W in [-2W, 2W - 4]: exact state for state; cell (s + D) div 4 = r'.
- Half notch: N = D mod 2D: q = (N + D) div 2D, so +D -> 1, -D -> 0. One-sided, as stated.
- Cells of a dial moved by its own quotient D(q) = 2W + q: tie-even cells gap (2q+1) dD; half-open cells gap (2q+1) dD + 1 with 2q+1 integers missed (q >= 0), so 1,600 over q = 0..39 (not 1,560). Check by probe.

## Things to probe (own code)
1. exhaustive algebra (split, flip, shift, half notch) over a range
2. one-gear edge act with a course given (rising, falling, irregular), run back, books, cell correspondence with the act as built on a still clock
3. the board: non-uniform 00 slot (varying by site), 24 + run back + books; W(b) <= 0 with D >= 1
4. the fixed-point cells in the half-open convention
5. the promise example W(a) = 3 grips, W(b) = 13 grips, v_00 = -10 grips
6. (vi)'s wording against (i)-(v): "a kept remainder belongs to the edge" over-generalizes (r_d, click tooth do not)

## Possible items so far
- (vi) wording: "a kept remainder" should be the gear's fine tooth; r_d and the click tooth are kept remainders with no edge.
- The 1,560 count is the tie-even cells'; the half-open cells miss 1,600 over q = 0..39 (if confirmed) while the text says "either dial" with 1,560.
- The edge act as probed is two splits per gear per round (a provisional one at 2 D_in for every row, used only through the 00 row's read), i.e. the 00 row's carry before the others': a stage inside the Node-clock; the text names it in section 5 ("one carry before the round").
- probe_momentum by-2 lay runs 15 rounds, text says "0 of 30" for both lays (minor).
- Root dial measured with the tie-even split and the mirror -s, not the owner's half-open (stated in the text; a consistency gap).

## After probe_fm1 (own algebra) and the two readers' reports
- probe_fm1: split bijection 0 misses (183,030), flip law 0, negation fails exactly on ties (11,986 ties), shift 0 for k in -3..3;
  half notch one-sided (+1500 -> 1, -1500 -> 0); still clock exhaustive 43,758 cases exact (both conventions);
  one gear run back 0 misses on drawn courses incl. W <= 0 at a slot (D >= 1): the promise W >= 1 both slots over-asks;
  flip commutation 20,000/20,000.
- Cells: tie-even none 1560; half-open none 1600 (q 0..39), twice 109 (L=10), 10,099 (L=100). Text's section 4 cites 1,560/119/10,199 = the
  tie-even cells, calls it "either dial"; the owner's convention gives 1,600/109/10,099. MINOR (same conclusion).
- mc3: half-open 572 states 0 collisions; the text cites "0 collisions of 573" (tie-even count). MINOR.
- Readers' reports: mc_math passed the second text in recheck (mc8); mc_phys passed with minors (notes_05) incl. "W x 3" label -> text now says 1.86 (folded).
- Root row of section 3's table: root's W at the marks is 15,625 -> 30,625 (x1.96), not 17,500 -> 32,500 (x1.86): the column label is the built/edge rows'. MINOR.
- probe_momentum by-2 lay is 15 rounds; text says "0 of 30 ... 30 of 30" for "falling by 1 and 2". MINOR.
- Root dial: "q_F = round(F/L) by rule (ii)" (half up) but the probe's split is tie-to-even (E.split): a wording/act mismatch at exact ties; the root's 24 not measured (one gear). MINOR.
- (vi): "W(next)" needs its reading named (the 00 row's own carry first, at its standing dial); "a kept remainder" over-generalizes (r_d has no edge).

## After probe_fm2 (board) and probe_fm3 (varying by site)
- My own act (00 row's carry first, then every row at 2 D_out) = edge_lib's half-open act bit for bit on every lay (A, B, C: 40 of 40 each).
- Text's lays: 24/24 at 40 rounds, run back 40/40, rewound, books 0 per gear (78-81 bits). SOUND.
- Varying by site (00 slot drawn per site, pulled at 27 of 27 sites, D odd at 121-187 of 324 gears): 24/24 at 40 rounds, run back 40/40, books 0, 79-81 bits. SOUND (the text did not run this; its claims hold there).
- W <= 0 at one slot with D >= 1 (W(b) = -1 grip, W(a) = 5 grips; W(b) = 0, W(a) = 3): exact 40/40, 24/24, books 0: the text's promise (W >= 1 both) is sufficient, not necessary. SOUND note.
- Promise example: D_in = 16 grips, D_out = -4 grips, refused. SOUND.
- The new probe_root_generic (17:00, after EDGE2): rounding half up (rule (ii)'s words) loses the 24 from round 3 on a moving clock; the odd rounding keeps it;
  the push tooth kept at the pivot's dial runs back 2 of 40 falling / 3 of 24 varying. EDGE2 says "q_F = round(F / L) by rule (ii)" and "a second edge tooth for the push is the exact alternative": the first mislabels the probe's act, the second is unproved (and false as the pivot-dial tooth).
