# The passing for four value legs: two lawful forms that close the books, and what their clicks mean (NOT_CLOSED 29)

David, 2026-10-30 (the second text, 23:3x UTC), for the night's side list, NOT_CLOSED 29: "the hat needs a lawful
one-pass passing for monomials of four value legs" (the Boss's #2187 6533115084 item 1, to David and the click's
deriver, on the architect's measure: with the held hand still under the hat, the held train books the tied spring's
energy alone, X_held = 2 hold f (k_a . k_b)(|x_a|^2 - |x_b|^2), and B4's pair world opens its books from round 57). It
reads the act on node-live 575973a20: step.passing (each train's X over its pairs, a J(b) - b J(a) with J the value
legs' plan on the Node-clock's own counts, the click's form the identity) and step.act (S = X(S) + X(S+), the window's
before, now and next). The probes are derive/david_open/node/passing4.py and pair_world.py, whole numbers alone, their
outputs beside them. The first text (toys-5 6141992a2) went to a new hostile pair, who refused it: the mathematician on
three items and thirteen minors, the physicist on five and nine. Both found the residual, both forms' books and every
form's oddness standing. Big Pic's word (6535643629 item 3: the middle form is the hat's road) is folded here with
their items (section 7); section 8 says how the text checked itself.

**The finding in one line:** for four value legs the act's passing leaves a residual, -f (e1 - e3), and two lawful
forms close the books exactly; they differ only in how they split a monomial's energy between its trains, and their
clicks mean energy where gears move many counts a round, not near the vacuum.
- **The residual.** For a monomial f x_1 x_2 x_3 x_4 the act's X sums over its legs to -f (e1 - e3), e1 with one leg at
  the now slot and three at the before, e3 the reverse. Two legs give e1 = e3, the bilinear identity behind COUNT5 M1;
  four legs do not, and the hat's own quartic leaves the residual inside the held train.
- **The middle form** books every monomial by its leg count: a train holding |A| of a monomial's d value legs keeps
  H_A + (|A| / d) V. It needs no flag, and at d = 2 it is the act's own two-leg passing, doubled. A still held hand then
  clicks back and forth with its tied train, as the shipped giver does under the act's two-leg passing.
- **The background form** books a monomial joining the held train to one other by the held train's own motion,
  S_held = -2 c P(now) (Q(next) - Q(before)), S_other = -S_held. It is right in the limit of a stiff or heavy held hand,
  with the back-reaction as its leading correction, and it picks its background by the held character, not by the
  dynamics.
- **Which form is the hat's road: the middle form** (Big Pic's word, 6535643629 item 3).
  - A tie's energy has no owner, in nature too: only the whole is kept, and a passing between trains is fixed only over
    beats and in decays, where both forms agree (the physicist's decay, within 48 permille).
  - So the record needs a rule for the back-and-forth part, and the middle form is the one with no flag: each monomial
    is shared by its legs, Euler's split of a homogeneous tie, one rule for every degree (2.2). At d = 2 it is the
    act's own two-leg passing up to the key's scale, so term 11 stands unchanged.
  - The background form is the stiff-limit reading of the same books, with the back-reaction as its leading
    correction, and not a law.
- **Measured:** on four Mesh-less Node-clocks the books open in 1,600, 1,600 and 1,598 of 1,600 windows under the act's
  passing and in 0 under either form; on B4's pair world, through the real loader and act, in 146 of 400 rounds from
  round 57 under the act's passing and in 0 under the background form. Read against the energy they split, both forms
  track it within about 1 per cent on the lays whose gears move many counts a round, and miss it near the vacuum, where
  the act's own integer drift is of the size of the exchange (section 4).

## 1. In clocks

- **What the passing counts.** Each round a train's click tooth carries the train's two-round energy change, read on
  the window before, now and next; summed over the trains the passings are 0 (the books), so over a run the clicks
  only move quanta from one train to another, up to what the teeth hold.
- **Why four legs break it.** A spring between two gears trades energy as a seesaw: what one gains the other loses,
  read off the two gears alone. A term of four legs is a seesaw whose pivot moves with the other legs; the act's passing
  reads each leg against the other three at the other slot, and the four readings no longer balance.
- **Two ways to share a term.** A term of four legs belongs to no one gear. The middle form gives each train the share
  of its legs. The background form gives it all to the moving train and treats the held hand as a stage that trades
  only when its size moves, which is right when the hand is too stiff or too heavy to be moved by the tie.
- **Where the clicks mean energy.** A click is a quantum of energy only where the act keeps energy well, which it does
  where gears move many counts a round. Near the vacuum, a hand moving less than a count a round keeps its motion in its
  tooth, and the counts the passing reads lose it.

## 2. In the algebra

### 2.1 The residual

- For a monomial f PROD x_(l_i) over its positions i (a gear may hold several), J_g(y) = -f SUM over g's positions of
  PROD over the other positions of y. So SUM_g x_g J_g(y) = -f e1(x; y), e1 the sum over positions of one leg at x and
  the rest at y, and SUM_g X_g(x, y) = -f (e1(x; y) - e1(y; x)) = -f (e1 - e3), e3 = e1(y; x), three legs at x.
- Two legs: e1 = x_1 y_2 + y_1 x_2 = e3, so the books close for any symmetric bilinear J with the click's form the
  identity (COUNT5 M1, git baaa5353e).
- Four legs: e1 - e3 is not 0 in general; with two legs still (x = y on them) and two moving, e1 - e3 = 2 x_1 x_2
  (y_3 y_4 - x_3 x_4).
- On the act the books' miss equals the summed residual exactly, in every window of passing4 and in 400 of 400 rounds of
  the pair world (the mathematician's residual_check and pw_check).

### 2.2 The middle form

- **Statement.** A monomial of even degree d (its value legs; the unit's legs read 1) pushes its leg at position i by
  w_d SUM over the halves S of the value positions that hold i, PROD over S other than i at the first slot and over the
  rest at the second. Call it M_i(x, y). The train's passing is SUM over its gears' positions of
  -f (x_g M_i(x, y) - y_g M_i(y, x)) on (a, b) and on (a+, a).
- **The books.** SUM_i x_(l_i) M_i(x, y) is w_d (d / 2) Q(x, y), Q the sum over the halves S of PROD_S x PROD_rest y.
  Swapping x and y maps each half to its complement, so Q(x, y) = Q(y, x) and the monomial's sum over trains is 0, at
  any weight w_d.
- **Oddness.** Each gear's share is antisymmetric in (x, y), so S on (b, a, a+) is minus S on (a+, a, b), and the click
  tooth runs back by the same act on the mirrored state, for monomials even under the mirror (COUNT5 M1's lemma).
- **What it books, by leg count.** At leading order in the window's differences train A's share is proportional to
  (|A| / d - 1) SUM over A's legs of dx / x + (|A| / d) SUM over the other legs, the exchange of the split
  E_A = H_A + (|A| / d) V. For the loader's 2 + 2 tie that is V / 2; for a 3 + 1 monomial it is 3 V / 4 and V / 4 (the
  physicist's p7: V / 4 tracks the form within 9 permille against 75 for V / 2; the mathematician's B3).
- **Why by leg count: Euler's split.** For a tie V homogeneous of degree d in the value legs, SUM over every leg of
  x dV/dx = d V. A train's share is the sum of x dV/dx over its own legs, divided by d; for a monomial each leg gives V,
  so train A's share is |A| V / d, one rule for every degree and no flag (Big Pic's word).
- **Its scale.** The share's prefactor is w_d times C(d - 1, d/2 - 1) d / (d - 1), which is 2 w_2, 4 w_4, 12 w_6 and 40
  w_8. The first text's w_d = 4 / d keeps one scale, twice the act's, at d = 2 and 4 only, and is not whole beyond.
  Whole weights at one scale for every degree present (w_d = L / K_d over a common L) are OPEN; the loader lays at most
  four legs.

### 2.3 The background form

- **Statement.** A monomial c PROD over its legs, joining a held train (flagged by character, load.trains_of) to one
  other train, factors as c P Q with P the other train's legs and Q the held legs. On the window (b, a, a+) it books
  S_held = -2 c P(a) (Q(a+) - Q(b)) and S_other = -S_held. A monomial whose value legs all lie in one train books
  nothing. Two-leg monomials keep the act's form. (passing4.py lays it without the 2; no count depends on it.)
- **The books** close by construction, monomial by monomial; whole, local, one pass, odd under the window's reversal,
  and its click tooth runs back by the same act (the mathematician: 400 rounds out and back on all three lays and on
  the pair world).
- **What it books:** the split E_held = H_held, E_other = H_other + V: the whole tie c x^2 |k|^2 goes to the tied train,
  the mass term c n x^2 and the interaction c x^2 (|k|^2 - n) alike. Nature's mass term is the first alone; the
  interaction belongs to neither particle, so its assignment is a convention.
- **Its regime.** The tie pushes the held hand radially, -2 c x^2 k, so a swinging tied hand moves the held hand's size
  and the form books that motion. The held hand is a stage only where its size is stiff or heavy against the tied
  dynamics, the back-reaction energy of order c^2 x^4 / (4 hat) its leading correction. In the first text's lay (A) the
  hat's radial frequency equals the tied train's, and at two sites the tie overturns the hat (|k|^2 runs from 36 to
  1.20 n and from 1 to 2.90 n): a strongly coupled lay. Only the stiff hat, lay (C), comes near the stage.
- **Its background is picked by a flag.** A heavy train of no held character can be the physical background: with a
  quartic tie c x x y y and y's teeth 10^4 times x's, the act opens the books in 400 of 400 rounds and the middle form
  books 12 times y's own energy change, where a background reading of y tracks it; the rule cannot choose y (the
  physicist's p10).

## 3. On the board

- The loader lays J's potential as monomials from the kinds' tables, the zero entries among them at factor 0. On B4's
  pair world 532 of its 772 monomials have four value legs; 96 join the held train to one tied train, of which 24 are
  live, all at 60,000 (hold f C: a tied train's diagonal pair times a held row), and 72 at factor 0; the other 436 lie
  at factor 0 too, so 508 of the 532 are at 0 (pair_world.py prints the count; the first text gave 96 live, a slip of
  mine).
- So on the worlds the loader can lay at 575973a20 every live four-leg monomial joins a held train to one other: the
  tie's factor carries the held flag. A four-leg monomial joining two trains neither held, or three trains, or two held
  trains, would need the middle form.

## 4. In the clicks

- **The energy each click carries.** Read the act's exact momentum M = 4 W (a+ - a) + s+ (M_out = M_in + 4 J exactly),
  and its kinetic part T(M) = R (M - 2 W R) / 4 with R = round(M / 4 W), the integral of the act's integer drift over
  the momentum (the physicist's measure; M^2 / (32 W) misses by 1,280 permille on a slow spring, T by 0). A form's
  energy meaning is its cumulative passing against the energy it splits.
- **Where it holds** (the physicist's p2 and the mathematician's energy_check, rerun by me byte for byte):
  - lay (A): the background form tracks E_held = H_held within 3 to 13 permille of the held excursion, the middle form
    its split within 1 to 9; the act's held passing misses the middle split by 2,338 to 3,784;
  - lays (A) and (B): the background form's cumulative held passing tracks twice the held energy change within 3,212
    and 2,567 ppm, the middle form within 5,896 and 4,767.
- **Where it fails:** near the vacuum. In lay (C), the stiff hat, the hand's counts move in only 28 of 400 rounds at a
  site while the tie moves its exact momentum every round; the background form misses 264 to 841 permille of the held
  excursion, while the middle form tracks within 0 to 14, and the act's own total energy misses by 555 to 3,642
  permille of the exchange. A lone held hand displaced 1 to 6 counts already misses its energy by 376 to 1,355 permille
  (p4).
- **The limit is the act's integer drift, for any coupling.** With every coupling bilinear the act's own energy moves
  about 0.3 per cent over 400 rounds while its books close (bilinear_energy), and the two-leg identity misses on the act
  in 320 of 400 rounds (p8). The first text's "for a quartic coupling the act keeps no energy exactly, so ... cannot
  exist" is withdrawn: the books are necessary, not sufficient, and the energy meaning is measured, not argued.
- **A decay is seen by both forms.** The held hand displaced 400 counts radially and the tied train seeded at 30: about
  97 per cent of the hand's excess passes to the tied train by round 2,000, and both forms track it within 48 permille;
  they differ only in the back-and-forth part (p5).
- **The pair world past the room.** Past round 57 the one-count hand's |k|^2 flickers among 0, 1 and 2. Under the
  background form the held train then fires up to 17,440 clicks a round (1,119,323 in summed size over 400 rounds),
  against 13,748 under the act; inside the room every train fires at most 1 a round (p12). So the night's click world
  holds only inside the room, as plans.holding's docstring says the books open past it; its room ends at frame 6's
  integer resolution, not at the passing alone.

## 5. Measured

- **passing4.py** (node-live 575973a20, also byte for byte on f72067cdf; four Mesh-less Node-clocks, 400 rounds; the
  held hand (k1, k2) under the hat 1 at n = 5^10, the tie 3, the tied train's own spring n, teeth 2000 n):

  | lay | books open: act / middle / background | held passing not 0: act / middle / background | windows where the size moved |
  |---|---|---|---|
  | (A) the hand laid at the hat's rest (it moves in every round) | 1,600 / 0 / 0 | 1,600 / 1,600 / 1,565 | 1,565 |
  | (B) the size laid off its rest | 1,600 / 0 / 0 | 1,600 / 1,599 / 1,582 | 1,583 (one window with P(now) = 0) |
  | (C) a stiff hat 10^4, teeth 10^6 n | 1,598 / 0 / 0 | 1,598 / 1,598 / 365 | 365 |

  Every form is odd under the window's reversal in 1,600 of 1,600 windows of every lay. The background form's held
  passing is non-zero exactly where the size moved, which is its definition; the mathematician checked it as sets.
- **pair_world.py** (B4's pair world from tests/test_the_tensor24_run.py's own files, the real loader and act of
  node-live 575973a20): the factors above; over 400 rounds the act's passing opens the books in 146, the first at round
  57, where |k|^2 first reaches 2 (the mathematician's pw_check prints it); the background form in 0.

## 6. What stands, and OPEN

- **Stands:** the residual; both forms whole, local, one pass, odd, with exact books; the middle form's split by leg
  count; the background form's split, right in the stiff or heavy limit; both forms' energy meaning where gears move
  many counts a round.
- **The hat's road: the middle form,** on Big Pic's word: one rule for every monomial, no flag, the hat's tie of
  degree 4 at weight 1. Its price, named:
  - a still train books |A| / d of each change of the tie's energy, bounded by its share and returned whenever the
    tie's energy returns; the giver held at 32 counts (the physicist's B2) is this;
  - where one train is heavy, most of its clicks are this back-and-forth (the physicist's 12 times its own energy
    change), so the clicks' energy meaning holds over beats and in decays, not click by click;
  - the background form stands beside it as the stiff-limit reading of the same books.
- **OPEN:**
  - for the stiff-limit reading, a background chosen by the dynamics (scale separation) rather than a flag;
  - a click-by-click energy meaning where one train is heavy;
  - whole weights at one scale for the middle form beyond d = 4;
  - the energy meaning near the vacuum and past the room, where the act's integer drift is of the exchange's size;
  - a monomial joining two held trains;
  - a world where the hat swaps in for frame 6, read end to end by the decoder.

## 7. The first text's readers, folded (the second text)

**Big Pic's word** (6535643629, item 3): the middle form is the hat's road.
- The tie's own energy has no owner, in nature too; a passing between trains is fixed only over beats and in decays,
  where both forms agree; so the record needs a rule for the back-and-forth part, and the middle form is the one with
  no flag, Euler's split of a homogeneous tie, at d = 2 the act's two-leg passing up to the key's scale (the finding;
  2.2; 6).
- The background form picks its owner by a flag, by character; the physicist's heavy train has no held character, so
  the flag misses it, though only a background reading tracks it. It is named the stiff-limit reading of the same
  books, with the back-reaction as its leading correction, not a law (the finding; 2.3; 6).
- The price, named: a still train's |A| / d share of each change of the tie's energy, returned when it returns; the
  clicks' energy meaning over beats and in decays, not click by click, where one train is heavy; degrees above 4 at
  whole weights of one scale, OPEN (6).
- The second text as listed; the click world's "valid inside the room" belongs on the candidate's showcase line too,
  for the Boss (4).

**The mathematician's three, and his minors:**
1. B1, section 3's count: 24 live of the 96, printed by pair_world.py now (3).
2. B2, section 4's impossibility claim: struck; the energy defined and the meaning measured, with his lays' figures and
   the act's drift for bilinear couplings (4).
3. B3, the middle form's split: by leg count, E_A = H_A + (|A| / d) V (2.2).
4. His minors: m1, the background form's 2 (2.3); m2, the size's motion as sets (5); m3, round 57 printed by his
   pw_check (5); m4, the residual equal to the books' miss (2.1); m5, w_d's scale and wholeness (2.2); m6, COUNT5 with
   its commit (2.1); m7, mirror-even monomials (2.2); m8, a held train among possibly two (2.3, 3, 6); m9, the gaps
   live in no world the loader lays (3); m10, pair_world.py's docstring (8); m11, the click's identity form (2.1); m12,
   lay (A) named as moving (5); m13, the clicks' sum up to the teeth (1).

**The physicist's five, and his minors:**
1. B1, the background form's regime: the stiff or heavy limit, the back-reaction, lay (A) strongly coupled, the mass
   term and the interaction (2.3).
2. B2, "a still hand clicks nothing": named a convention, right for a frozen background; the kept two-leg passing
   clicks a still train; the flag against the dynamics, with his p10 (the finding, 1, 2.3).
3. B3, the measurements: the books necessary, not sufficient; the energy meaning measured with his p2, p4, p5 and p8,
   and its limit the act's integer drift (4).
4. B4, the pair world past the room: the flicker and its clicks, and the click world valid inside the room (4, 5).
5. B5, as the mathematician's B3 (2.2).
6. His minors: m1 the 2 (2.3); m2 the count (3); m3 lay (A) moving (5); m4 lay (C)'s hand within 3,119 to 3,128 (5);
   m5 w_d (2.2); m6 one scale under one key (2.2, 6); m7 two held trains (3, 6); m8 the paths (2.1, 5); m9 the clicks
   up to the teeth (1).

## 8. How this text checked itself (the owner's word of 16:2x UTC, 6527238774)

- **The probes:** passing4.py unchanged, its output byte for byte; pair_world.py with its factor line, rerun in 2 s on
  node-live 575973a20, its other lines byte for byte.
- **The readers' scripts, rerun by me byte for byte:** the mathematician's pw_check, energy_check, energy_total,
  bilinear_energy, middle_check and residual_check; the physicist's p4_lone_hat, p5_decay, p6_layA, p7_middle_split,
  p8_two_leg, p10_heavy_nonheld, p11_stiffness and p12_pair_maxima.
- **Derived again by hand:** the middle form's split by leg count, from SUM_(S containing j) (|S n A| - |S^c n A|) =
  C(d - 1, d/2 - 1) (d - |A|) / (d - 1) for j in A and -C(d - 1, d/2 - 1) |A| / (d - 1) for j outside, against
  dE_A = V ((|A| / d - 1) SUM_A dx / x + (|A| / d) SUM_rest dx / x); the prefactors 2, 4, 12 and 40 at d = 2 to 8.
- **A slip of mine, caught by the readers:** the count of live monomials (96 for 24), cited to a probe that did not
  print it.
- **The first text's checks:** the residual by hand and in the books; the middle form's symmetry and both forms' oddness
  in 1,600 of 1,600 windows; the stiff hat's 365 windows; pair_world.py's first-run slip (a train's kind count for its
  rows), mended from the firsts.
