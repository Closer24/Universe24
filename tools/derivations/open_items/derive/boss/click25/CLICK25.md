# The 24 and the click: the one operation beside the 24, in the four layers

The Boss's deriver, 2026-10-30, on the owner's word of 16:1x to 16:2x UTC ("to the 24 operations one more operation can
be added, one that is not odd, and that is in fact the click"), his word of 15:5x ("on a moving clock there is a click"),
and his word, relayed, "in the clicks, think clocks; do not think quantum ... clocks connect and come apart, and the aim
of the system is that clocks connect". Order, by the lead's word: the clock's click at a moving 00 slot first (it blocks
terms 5, 9 and 13), then what the click counts and its books, handedness last. Five probes beside this text, in whole
numbers with the engine's own carry, wrapping the real act (src untouched): `probe_clock.py`, `probe_drift.py`,
`probe_48.py` (the moving clock; the board of sym24_v2/common.py, a cube of side 3, 18 rows, 27 sites, J = 0 and
SYM24's plan 1 laid), `probe_wind.py` and `probe_count.py` (what the click counts; Animate's world through term11_v2/probe2.py). Their
outputs stand beside them (`*.txt`); `halftooth.py` holds the wrapped act. Every number below is theirs. Big Pic's
words (#2187 6525679128, 6525978806, 6526070842, 6526201692) are tested here, not taken.

**Status on the ladder:** the clock's click DRAFTED (the algebra, the probes and the physics written; no hostile pair
yet); term 11's count on the owner's word of 15:3x DRAFTED (probe_count.py); handedness OPEN by name.

## 0. The law in one paragraph

The 24 turn the board's rows and sites. The click is the one operation that touches neither: it acts on the Node-clock's
dials alone, on what Rule3 keeps, by Rule3's own carry. It has two faces, one algebra. **The clock's click:** where the
00 slot moves, every fine tooth at the Node-clock is carried from the dial it was kept on to the dial that now reads
it, by the clock's change: a tooth is a position on a dial of 2 W half-teeth, u, kept at the before slot's teeth, and
the act reads it at u + W(now) - W(before). **The meshing's click** (term 11, on the owner's word of 15:3x): where two
clocks connect, a hand of one meshing with a hand of the other through a vertex or a Mesh, the wind passes between
them, D = now^2 - next x before summed over the hand; its count in windings is Rule3's quotient n = (D - D_lay + k_0)
div key, the lay's wind the held quantum that is never counted, and the click is where n moves between two rounds, the
same in both runs. Both faces read only what every one of the 48 fixes (the 00 slot; an A1 form), both leave the rows
and sites alone, and both are translations of a dial where the 48 act on a dial by its flip or not at all: that is the
exact sense of "not odd". The board keeps the 24 and the 48; the one place a handedness can enter is a click that reads
a pseudoscalar, and the only such click is the conversion's (OPEN, section 4).

## 1. The clock's click: the moving 00 slot (Clock, Algebra, Board, Clicks)

### Clock

- A gear's fine tooth is what it keeps toward its next whole turn: a position on its dial. Time's reversal reads the
  dial backward, so a tooth at r becomes W - 1 - r: the reflection of the dial about the line through its zero mark
  and its half-turn mark.
- Where the clock deepens, the dial gains teeth. The reflection must stay a reflection, so the teeth are added at the
  zero mark, as many on each side: a tooth keeps its distance from the half-turn mark. With one tooth added, each side
  gains half a tooth; so the dial is counted in half-teeth, 2 W of them, and a position is u in [0, 2 W). The gear's
  carry reads the tooth r = u div 2 and keeps the half-tooth u mod 2 beside it; the clock's change moves u by W(now) -
  W(before). That move is the clock's click: q_c, beta+ = carry(W(now) - W(before), 2, beta), the tooth r moving by
  q_c, a whole tooth for every two half-teeth of the clock's change, and nothing where the clock stands.
- The Node-clock already holds both teeth: the 00 slot at its now and its before slot (the owner's question of today,
  SYM24 Open). Nothing is read from outside and nothing new is kept: u is one whole number per gear as r was.
- The mirror flips u on the two slots' dials together: u -> W(a) + W(b) - 1 - u. Mirrored twice, the state returns on a
  moving clock as on a standing one.

### Algebra

- **The defect is forced, not conventional.** At a reading teeth W the only map phi on [0, W) with carry(-n, W, phi(r))
  = (-q, phi(r')) for every n is phi(r) = W - 1 - r (phi(r) + r is one constant, and the range makes it W - 1). So a
  negated row's tooth must be flipped in the teeth of the round that READS it; that round keeps W - 1 - r', and the
  next round reads at W+ and needs W+ - 1 - r'. No definition of the turned state mends W - W+; the act must carry the
  tooth between the two dials (SYM24 Algebra, Rounds; its "only if" is this).
- **The half-tooth act.** The state (a, b, u, r_d), u in [0, 2 W(b)). One round: u' = u + W(a) - W(b); r = u' div 2,
  beta = u' mod 2; q, r+ = carry(W(a) (a - b) + s (F + T_k q_d), W(a), r) as built; a+ = a + q, b+ = a,
  u+ = 2 r+ + beta in [0, 2 W(a)). In one carry: q, u+ = carry(2 W(a) (a - b) + 2 push, 2 W(a), u + W(a) - W(b)):
  the act as built at doubled teeth and doubled push, the one new bit the half-tooth.
- **Covariance (the 24 and the 48).** A negated row's tooth, flipped in the keeping dial, 2 W(b) - 1 - u, is carried
  to 2 W(b) - 1 - u + W(a) - W(b) = 2 W(a) - 1 - u': the flip in the reading dial. Then r~ = W(a) - 1 - r and
  beta~ = 1 - beta, the sign law gives (-q, W(a) - 1 - r+), and u~+ = 2 W(a) - 1 - u+: the flip of the output in its
  keeping dial, which the output state's before slot (a) names. By induction every round holds, for every change of
  W, odd or even. Where J is 0 the act knows no kind, so the 48 hold under every lift as at a standing clock; where J
  is laid through the tables the 24 hold as the tables are kept by them.
- **The mirror** m(a, b, u) = (b, a, W(a) + W(b) - 1 - u) is an involution. untick = m tick m: m(tick s) carries its
  tooth to 2 W(a) - 1 - u+, the backward carry at W(a) gives (-(a - b), W(a) - 1 - r) by the sign law, the drive's
  tooth returns by the same lemma, and the second m gives back u. Exact on a moving clock, with "one mirror about n
  ticks" equal to n unticks again.
- **The drift.** Per gear W_t (v+ - v) = F + r_read - r+, with r_read = r_kept + q_c; over a row on the torus,
  W_t (S_t+1 - S_t) = R_t + Q_t - R_t+1 (R the row's kept teeth, Q its clocks' clicks), exact. The term Q_t = about
  N dW / 2 is what cancels the one-signed bias SUM R_t (1 / W_t - 1 / W_t-1) of the act as built, whose teeth have
  the mean (W - 1) / 2 and a range that grows with W.
- **The (d_t W)(d_t a) term** (step.py lines 44 to 49) is not this click's. The momentum form W(before) (a - b) + push
  is not time-symmetric (its run back would read the future's teeth), so the second-difference form, a free gear
  keeping its velocity, is forced by the exact run back in one pass; what the metric's motion does to a wave's
  momentum is G2's, read in the clicks, not a defect of the act.
- **What is not mended:** a falling clock. The dial loses teeth at its zero mark on both sides, and a tooth within
  |dW| half-teeth of the zero has nowhere to go: the promise breaks there (as built it breaks on one side, r >= W+).
  G2 owes the falling clock as before (step.py's comment); the half-tooth makes its break symmetric and names it.

### Board

- At every Node-clock alike, one more add before the carry: the tooth carried by the 00 slot's change, read at the
  Node-clock's own two slots. No Mesh is read for it, no table, no bound, no if; the order of work stays no law.
- The 24 and the 48 on a moving clock, measured (probe_clock.txt, probe_48.txt), the 00 slot rising by 1 from W = 10
  (an odd change), 8 rounds, J = 0: the act as built holds 24 of 24 at round 1 and 3 of 24 (the diagonal's stabilizer)
  from round 2; the half-tooth act holds 24 of 24 at every round; the mutant that reads the kept tooth unmoved, 3 of
  24 at every round; the mutant that moves it by the whole change (teeth added on one side of the zero mark), 3 of 24.
  Rising by 2 and by 3 the same. The 24 reflections over 6 rounds on the rising lay: 24 of 24 under the g lift and
  24 of 24 under the u lift (the act as built: 0 of 24). The counts stay within 9 bits.
- A plan laid through the 24's tables (SYM24's plan 1, s = 3, T_k = 2, T_d = 5), the 00 slot rising by 1 from W = 9:
  the act as built [24, 3, 3, 3], the half-tooth act [24, 24, 24, 24], the mutant with one entry of the epsilon table
  raised by 1 [4, 4, 4, 4]; standing at W = 9 both acts 24 of 24; the counts reach 96 bits.
- The mirror and the run back on the moving lays: mirror twice is the state, half-tooth yes, as built no; n unticks
  return the start, both yes (the run back as built was already exact on a moving clock: untick's docstring says so);
  one mirror about n ticks returns the start, half-tooth yes, as built no.
- The drift (probe_drift.txt, 40 rounds, rising by 1 from W = 10): the 14 moving rows' S = SUM (a - b) together at
  rounds 10, 20, 30, 40: as built -189, -273, -336, -371 (t1's rows -28, -24, -26 at round 40); the half-tooth act
  -62, -63, -56, -62 (t1 -5, -5, -3); the standing control -77, -76, -80, -81. |S - S0| at most 29 as built, 9 under
  the half-tooth, 11 standing (the bound at standing W is 24). The row-sum books with the clocks' clicks: 0 misses over
  18 rows x 40 rounds; the clicks summed 9,720 = 486 gears x 40 teeth / 2.
- The falling clock (W = 40 falling by 1 or 2): as built the promise breaks before round 1; under the half-tooth it
  breaks at the lay, at 178 of 486 gears, every one below the zero mark. Not mended, named.
- The half-tooth act is the act as built, bit for bit, wherever the clock stands (a, b alike and u div 2 = r at every
  round on the standing lay; where it moves they part, as they must).

### Clicks

- Terms 5, 9 and 13 were blocked by a conservation the board kept at standing W and lost under a moving W (SYM24,
  Solution24 step 6). Under the clock's click each row's zero-mode momentum is kept to the bound of the standing
  clock, the 24 and the 48 hold bit for bit on a moving clock and the mirror is its own inverse: the metric family may
  move its 00 slot, so term 5's push, the notch (term 9) and the frozen clock (term 13) can be derived on the act.
- A deeper 00 slot is a slower clock, read in the clicks as proper time, as before; the clock's click writes no click
  line of its own: its quotient goes into the tooth, not into the record. On a moving clock the clicks' spacetime
  gains the one thing it lacked, a time that may change its rate without a side of its own.
- The owner's idea of 15:5x, "on a moving clock there is a click", is this: one whole tooth at every gear of the
  Node-clock for every two half-teeth the clock deepens, and none where it stands.

## 2. The click as the one operation beside the 24

- **What it acts on:** the dials' remainders at one Node-clock: the fine tooth u of every gear (the clock's click) and
  the train's click tooth k (the meshing's click). Never a row, a site, a count a or b.
- **When it fires:** Rule3's quotient where a winding is whole: for the clock's click the winding is one tooth (two
  half-teeth) of the clock's change; for the meshing's click the winding is the key.
- **Its algebra with the 24:** the 24 move rows and sites and flip some dials; the click translates a dial (u -> u +
  dW) or carries a scalar onto one (k). It commutes with every one of the 24, and with the 24 reflections, because it
  reads only what all 48 fix: the 00 slot (fixed by every signed permutation) and A1 forms (the swept area summed
  through the A1 table; the wind D, a scalar). Measured: the 24 and the 48 on the board with the click laid, above;
  term 11's click under the 24, 24 of 24 (TERM11 Measured 4).
- **"Not odd", exact:** on a dial of 2 W positions the 48 act as the group of order 2, the flip or the identity; the
  click acts as a translation, which lies in neither coset of that group's action: it is not a reflection of the dial
  and not a turn of the board. Its quotient does not negate under the flip: q_c(beta) + q_c(1 - beta) = dW, 0 misses
  over dW in [-9, 9] and both half-teeth (probe_48.txt), where an odd operation would give -q_c.
- **With the mirror:** the clock's click is what makes the mirror an involution on a moving clock (section 1); the
  meshing's count is even under the mirror (D reads the same backward: 6,000 of 6,000, probe_count.txt), so the
  two runs hold the same count at every round and part only where it moves.
- **The owner's frame, "clocks connect":** a click is the event where two clocks connect or come apart: a hand of one
  meshing with a hand of the other through the vertex (one Node-clock) or the Mesh (two), and the whole winding passed
  from the giver's dial to the taker's at the meshing is the count; the clock's click is the case where the clock's
  own train (the metric's 00 slot) meshes with every gear at its Node-clock: the clock deepening passes half a tooth
  to every dial, and the whole tooth is the click. One operation, two meshings: the metric's with every gear, and a
  train's with a train's.

## 3. What the click counts: term 11's count on the owner's word (Physics, Board, Algebra, Clock)

The owner's word of 15:3x UTC: yes to the completion of line 35 (4)'s carry; the click counts where the two runs,
forward and backward, part, the wind D given or taken, never D held; a clock that keeps its beat does not click; a
click is clocks connecting and passing a turn; decision 40 (g)'s one held quantum per Node-clock and line 35 (4) stand
together. Derived here on the act; it passes its hostile pair before any code.

### Physics behind the clicks

- Two clocks connect: the taker's hand, at rest, is set turning by the giver's through the vertex; wind passes from
  the giver's dial to the taker's; later it passes back and the clocks come apart. On Animate's world (probe_count.txt,
  6,000 rounds, g = f div 10) the taker's count runs 0 to 7 and back, the giver's clicks sum to -6 and the taker's to
  +6, 35 rounds carry a click, and the taker holds at least one winding in about 4,920 rounds of 6,000, the clocks
  connecting 3 times (probe_wind.txt).
- The wind is the energy: D = now^2 - next x before over a hand's gears is the leapfrog's energy over W^2 (Algebra),
  whole, and even under time's reversal, so the forward run and the run back hold the same wind at every round
  (6,000 of 6,000 measured): the two runs part only where the wind moves, and there the forward run reads a take
  where the backward reads a give. A hand that keeps its beat keeps its wind to Rule3's turn (the free hand: within
  1,855 millionths of a key of the lay's over 6,000 rounds) and, born at the half of its key, never clicks (0 clicks).
- The charge's count stays the area's: the net turn of the hand's plane, Omega = SUM (re p_im - im p_re), whose
  exchange books close exactly under the common turn (0 misses of 6,000). The two counts agree where the hand turns
  one way (both 0..7 on the circle, both connect 3 times) and part where it does not: the giver on a line hands the
  taker 7 windings of wind and 0 of charge. That closes the physicist's items 2 and 9 of term 11's second text (a line
  hand and a one-part train have a wind) and keeps his item 1 as wording: the count is the nearest whole number of
  keys, so at the n-th click the hand has taken n - 1/2 keys and the remainder; the tick is whole, the hand is not.
- Big Pic's escapement (6526070842), tested: the two senses of a hand's turn are its two eigen-turns; their areas
  differ by Omega (whole) and sum to E / (2 W sin omega), no whole number; so "the sum of the senses is the wind" is
  exact only as D (counts^2), the law's form, and the senses cannot be counted apart on the act. The sense-by-sense
  books hold by the symmetry of the common-turn vertex, and they are the area's.
- E = n h-bar omega is the decoder's reading over many clicks (TERM11), not the board's; the key is an energy in the
  gears' own units (counts^2), the same for every train (one key for the board, the pair's books force it), so a key
  of wind is a key of energy at every beat, and the decoder's h-bar is the key over the beat it reads. That is what
  "do not think quantum" leaves on the board.

### Board

- **The hand's wind**, read in the round at the Node-clock from the train's own rows: D_h = SUM over the rows through
  the A1 table of a a - a+ b, the now squared less the round's own next times the before (the act computes a+ = a + q
  in the round; nothing beyond the now slot's readings is read).
- **The count:** n_h, k_h = carry(D_h - D_h,lay + k_0, key, 0), k_0 = (key - 1) div 2: the whole windings passed since
  the lay, the remainder its tooth. D_h,lay is the lay's wind, one whole number per train per Node-clock set at the
  lay and moved by no act: the held quantum of decision 40 (g), which is never counted. The birth at the half puts the
  lay's wind at the middle of a key, so Rule3's turn never clicks a steady hand.
- **The click** is where n_h moves between two rounds, q_h = n_h(t) - n_h(t-1); the runner, which alone sees two
  rounds, writes the click line (train, Node-clock, round, q); the act writes n_h each round and nothing else. No log
  is read, no hold is kept (Algebra: a hold would break the run back).
- **The books:** D_L + D_M is the act's invariant up to Rule3's turn (the vertex's wind held once in each hand by
  Euler's theorem, so no third hold is needed), so the pair's counts' sum is kept except where Rule3's turn crosses a
  key: on Animate's world the books miss in 2 rounds of 6,000 (the giver on a line, 4 of 6,000), n_L + n_M staying
  within {-1, 0}; D_L + D_M drifts by at most 1,854 millionths of a key over the run and 3,351 in one round. The
  area's books close in every round; the wind's close to Rule3's turn, and that is named, not hidden.
- **Nothing is pushed:** the count writes nothing into a, b, u or r_d; the 24 and the 48 keep it (D is a sum of
  products of each gear with itself, unchanged by any signed permutation of the rows), and the clock's click leaves it
  alone (D reads counts, not teeth).

### Algebra

- Per gear, W D_i = W q_i v_i - a_i J_i - a_i (r_i - r_i+) exactly (from W q + r+ = W v + J + r and a+ = a + q,
  b = a - v). Summed over every gear, W q v - a J is the leapfrog's invariant of one quadratic potential (Euler's
  theorem on -SUM a J = 2 V), so SUM over all gears of W D is kept to the remainders' term: measured, W (D_L + D_M)
  moves by at most 264 millionths over 6,000 rounds. Per hand, -SUM a_i J_i over the hand's gears holds its own
  spring's 2 f a.a and the vertex's g M.L once: the hand's share.
- The kick's work in a round, tau_D = SUM K (a+ - b), is the exact wind the meshing passes: tau_D,L + tau_D,M =
  -(S(t, t+1) - S(t-1, t)) with S(t, t+1) = g (L_t . M_t+1 + M_t . L_t+1), 0 misses of 6,000: the meshing's own
  wind is the giver's now against the taker's next and the taker's now against the giver's next, the meeting of the
  future with the past (line 1021) at the meshing itself. The count above uses D (the hand's wind with its share),
  not the work, so no third dial is needed; the work is what the meshing holds between the rounds.
- **No hold survives the run back.** A hold of n(t-1) in the state s_t cannot be restored from s_t+1: D(t-1) needs
  a_t-2, which no slot holds, and the backward round that gives a_t-1 is the one that needs it. So the count is a
  function of the round and the click a difference of two rounds. D is even under the mirror: the mirrored state
  (a_t, a_t+1) ticks to a_t-1, and a_t^2 - a_t-1 a_t+1 = D(t).
- **The key and its middle, in half-teeth** (Big Pic's (3), tested): with the count's tooth taken as a half-tooth
  u_k in [0, 2 key), the birth at the half is u_k = key for every key and the flip is exact on every key; the pair's
  books need the two teeth to sum to 2 key - 1, the two half-teeth beside the middle mark, which the flip exchanges:
  both born at u = key sum to 2 key and miss where 2 A + key is a multiple of 2 key, that is at an even key once per
  key of area and at an odd key never. So the odd key still closes the books with one shared birth, and an even key
  needs the giver and the taker born on the two sides of the middle. The odd key stays CHOSEN with its reason exact.
- **Three clocks:** no births close three (TERM11, forced); n hands born alike keep the counts' sum within
  (n - 1) div 2: the one winding in transit, whole on none, held by the connection until the draw (term 12).

### Clock

- A clock's spring holds its wind; the hand that keeps its beat holds it unchanged; when it meshes with another
  clock's hand, whole windings pass between them, and each whole winding passed is a click: the two clocks connected
  by one more, or come apart by one. The lay's wind is the clock's own, never counted.

## 4. Handedness (last, OPEN by name)

- **What stands:** the act as built keeps all 48 at a standing clock, and with the clock's click on a moving one (24
  reflections of 24 under both lifts, probe_48.txt); no kind carries a parity label; the one handed piece the tables
  hold is the epsilon channel T1 x T1 -> T1 (SYM24). The meshing's count reads D, a sum of each gear's products with
  itself, unchanged by every signed permutation; the charge's count reads the area through the A1 table, a true scalar
  (TERM11's physicist, item 3); the clock's click reads the 00 slot. None of the three can be handed. The board keeps
  the 48 and so do these clicks.
- **Where the click alone can be handed:** a click that READS a pseudoscalar and pushes nothing. The one pseudoscalar a
  hand of two T1 parts holds is its helicity, h = (re x im) . p: the cross of its two parts through the epsilon table,
  dotted with its travel p along the Mesh (the readings' gradients); even under the 24 turns, odd under the 24
  reflections. The conversion click (the weak force, line 344), which absorbs one train's quantum and gives it as
  quanta of others, chooses its list; choosing it by the sign of h (Rule3's sign test, up - down, as the load's tables
  use it) is a handedness of that click alone, while the act on a, b, u and r_d keeps all 48 because the click pushes
  nothing. Electromagnetism's and gravity's clicks are counts of D and of the area, even by construction, no label.
- **The least to declare:** one rule on one click: the conversion's list is read by the sign of the converting
  quantum's helicity. No label on any kind, no table changed, no act changed. Whether the rule is needed is asked of
  the clicks (Wu 1957, V - A: nature says yes); whether it is a declaration or follows from the draw's own form at the
  conversion is OPEN. The lead's word: parity is not needed to close the Node-clock, and the owner asks why it is
  needed at all; this section names it and derives nothing.
- **What it needs** (Big Pic's piece 4): the conversion click itself (G5/G6, the split click's draw and its list) and
  the converting hand's two parts as T1 with a direction of travel: from the half-speed gear (another agent's piece,
  unread here) this click needs exactly the pair (re, im) and p at the taking Node-clock, nothing more.

## 5. What each open problem becomes

- **The moving clock:** mended by the clock's click, the half-tooth act: the drift bounded as at a standing clock, the
  24 and the 48 bit for bit on a moving clock, the mirror its own inverse, one mirror about n ticks exact; terms 5, 9
  and 13 unblocked on the act; the falling clock stays G2's. The centred odd tooth (sym24_v2/candidate.py) is this
  act's case where every change is even; the half-tooth needs no odd W and no change of term 2's law.
- **What the click counts:** the wind given or taken, D = now^2 - next x before over the hand, counted from the lay's
  held wind at the half of the key; the click where the count moves between two rounds, the same in both runs; the
  area stays the charge's own count. The books: the area's exact, the wind's to Rule3's turn (2 misses of 6,000),
  named. The line train tied to a turning hand takes wind and clicks (and area, as TERM11's mathematician measured); a
  one-part train clicks by its wind; the board holds n -/+ 1/2 at a click as wording.
- **Parity:** the board and every click but one keep the 48; the conversion click alone may be handed by the
  quantum's helicity; OPEN.
- **The key:** one for the board (the pair's books force it); its middle in half-teeth is u = key for every key; the
  odd key stays CHOSEN with its reason exact (the two births beside the middle); its value an integer of the file
  (CHOSEN, Animate's unit page) in counts^2 of wind, no longer in teeth: the wind's key does not scale with W.
- **Three trains:** the one winding in transit, within (n - 1) div 2 of the books, the draw's to settle.

## 6. The law lines to change, old -> new (a law changes only on the owner's word)

1. **Line 35, item (4):** "how the click is computed: the wind of a hand is its stored energy counted in windings, a sum
   of products of its gears now and before over the Node-clock and its six neighbours, and the carry is wind + earlier
   remainder = q x whole winding + new remainder; with q = 0 there is no click, with q at least 1 the click fires, q
   whole quanta leaving as events and the remainder staying, and "q at least 1" is the quotient itself and no
   comparison" -> "how the click is computed: the wind of a hand is its stored energy counted in windings, D = now^2 -
   next x before summed over its gears, the meeting of the future with the past at the hand; the carry is the hand's
   wind less its lay's held wind plus the half key = n x whole winding + remainder, n the windings passed since the
   lay; the lay's held wind is the one quantum per Node-clock of decision 40 (g) and is never counted; the click is
   where n moves between two rounds, the wind given or taken, read alike in both runs; a clock that keeps its beat
   does not click; a click is two clocks connecting or coming apart by one winding; the move of n is a difference of
   two quotients and no comparison" (the owner's words of 15:3x and 16:1x to 16:2x UTC).
2. **Line 35, item (5):** after "the beat (the carry of the clock's dial) is the clock's own event and no kind of
   click" add "; and the clock's click, where the 00 slot moves, is no kind of click either but the one operation's
   other face: every fine tooth at the Node-clock, a position u on a dial of 2 W half-teeth kept at the before slot's
   teeth, is carried to the now slot's dial by the clock's change, u + W(now) - W(before), one whole tooth for every
   two half-teeth, and it writes no line" (the owner's word of 15:5x).
3. **Line 94:** "the step commutes with each of the cube's 24 turns, bit for bit, the click included" -> "the step
   commutes with each of the cube's 24 turns, bit for bit, the click included, on a moving clock as on a standing one
   (the clock's click carries each fine tooth between the two slots' dials)"; and "The reflections are not asked, so
   the great clock may be chiral." -> "The reflections hold on the board as the 24 do (the act is achiral, 48 of 48
   at a standing clock and, with the clock's click, on a moving one); the click alone may be handed, and only the
   conversion's (OPEN)."
4. **Line 344:** "And no click of the law carries a handedness: the draw is by the winds, a reflection-even measure,"
   -> "And no click of the law carries a handedness but the conversion's, where its list is read by the converting
   quantum's helicity, (re x im) . p, the one pseudoscalar a hand of two parts holds, the board keeping the 48 since
   the click pushes nothing (OPEN, the owner's word of 16:1x to 16:2x); every other draw is by the winds, a
   reflection-even measure,".
5. **Line 346:** "the law's great clock is parity-even as nature's, and so is its click" -> "the law's great clock is
   parity-even; its clicks are even but one, the conversion's, which alone may be handed, as nature's weak click is
   (the owner's word of 16:1x to 16:2x)"; and "Parity conserved stands, Wu 1957;" -> "Parity conserved on the board
   stands; in the conversion click it is OPEN (Wu 1957);".
6. **Line 1696:** "the 48 symmetries with the reflections, so parity is kept, no handedness, a finding by name against
   nature (Wu 1957)" -> "the 48 symmetries with the reflections on the board, parity kept there; the conversion click
   alone may be handed (OPEN)" (the disagreement SYM24 named between lines 94 and 1696 is settled by the owner's word:
   the board keeps the 48, the click alone may be handed).
7. **Owed in the architecture (the writer's):** term 2's Algebra "W = T + the sum of the 00 slots, linear" stands; the
   glossary's "Mirrored state: ... each fine tooth r flipped to W - 1 - r in its teeth W" -> "each half-tooth u
   flipped to W(now) + W(before) - 1 - u in the two slots' teeth together"; state.py's r "within [0, W)" -> u "within
   [0, 2 W(before))"; term 11's row -> the count of section 3; step.py lines 44 to 49 -> the moving clock mended, the
   falling clock still G2's.

## 7. What stays OPEN, readiness, Solution24

- **OPEN:** the falling clock (G2); the key's value (CHOSEN, Animate's unit page; one key for the board); the wind's
  books to Rule3's turn (named; whether a whole-number form of the act's energy with the teeth closes them exactly is
  the mathematician's question); the conversion click and its handedness; a train across its Node-clocks; the
  half-speed gear's two hands (another agent's); the metric family's own wind at the swing's top (term 9: a uniform
  rising 00 slot has D = (dW)^2, steady, and never clicks; what the notch does is G2's).
- **Ready for a hostile pair:** the clock's click (section 1), yes: the algebra is proved, every claim has its mutant
  and its number on the real act, nothing is declared. Term 11's count (section 3), yes for a first reading, with the
  books' Rule3 misses and the runner's click line named as the two items a pair will press. Handedness, no.
- **Solution24:** add to step 6: "every kept remainder names the dial it was kept on and the dial that reads it;
  where the two differ the carry between them is part of the act, checked under the 48 and under the mirror on a
  moving clock as on a standing one". Nothing else to add.
- **Method: addressed.** Which clock or gear makes it: the clock's own train at its two slots meshing with every
  dial at the Node-clock (the clock's click); the hand's own wind at the meshing (the count). What the clicks show,
  the books first: the row-sum books with the clocks' clicks exact (0 misses); the area's books exact (0 of 6,000);
  the wind's to Rule3's turn (2 of 6,000). What does not follow, asked of the clicks: the key's value and parity
  (CHOSEN); the falling clock (G2); the conversion's handedness (OPEN).
