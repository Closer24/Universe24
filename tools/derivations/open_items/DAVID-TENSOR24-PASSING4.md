# The passing for four value legs: the held hand's tie booked by the held hand's own motion (NOT_CLOSED 29)

David, 2026-10-30 (the first text, 22:xx UTC), for the night's side list, NOT_CLOSED 29: "the hat needs a lawful
one-pass passing for monomials of four value legs" (the Boss's #2187 6533115084 item 1, to David and the click's
deriver, on the architect's measure: with the held hand still under the hat, the held train books the tied spring's
energy alone, X_held = 2 hold f (k_a . k_b)(|x_a|^2 - |x_b|^2), and B4's pair world opens its books from round 57). It
reads the act on node-live 575973a20: step.passing (each train's X over its pairs, a J(b) - b J(a) with J the value
legs' plan on the Node-clock's own counts) and step.act (S = X(S) + X(S+), the window's before, now and next). The
probes are derive/david_open/node/passing4.py and pair_world.py, whole numbers alone, their outputs beside them.

**The finding in one line:** for four value legs the act's passing leaves a residual, -f (e1 - e3), and two lawful forms
close the books exactly; the one that books a monomial joining the held train to another by the held train's own motion
leaves a still hand silent.
- **The residual.** For a monomial f x_1 x_2 x_3 x_4 the act's X sums over its legs to -f (e1 - e3), e1 with one leg at
  the now slot and three at the before, e3 the reverse. Two legs give e1 = e3, the bilinear identity behind COUNT5 M1;
  four legs do not, and the hat's own quartic leaves the residual inside the held train.
- **The middle form** closes the books for every even degree and gives a train's own monomials 0; a still held hand
  then clicks opposite its tied train.
- **The background form** books a monomial joining the held train to one other train by the held train's motion alone,
  S_held = -2 c P(now) (Q(next) - Q(before)), S_other = -S_held; a train's own monomials book nothing. The books close,
  the held hand clicks only where its size moves, and the turning hand's exact norm gives 0, as frame 6 has it.
- **Measured:** on four Mesh-less Node-clocks the books open in 1,600, 1,600 and 1,598 of 1,600 windows under the act's
  passing and in 0 under either form; on B4's own pair world, through the real loader and act, in 146 of 400 rounds from
  round 57 under the act's passing and in 0 under the background form.

## 1. In clocks

- **What the passing counts.** Each round a train's click tooth carries the train's two-round energy change, read on
  the window before, now and next; summed over the trains the passings are 0 (the books), so a click only moves a
  quantum from one train to another.
- **Why four legs break it.** A spring between two gears trades energy as a seesaw: what one gains the other loses,
  read off the two gears alone. A term of four legs is a seesaw whose pivot moves with the other legs; the act's passing
  reads each leg against the other three at the other slot, and the four readings no longer balance.
- **The held hand as the background.** The held hand is the vacuum the tied hands move in. The tie's energy is a tied
  hand's mass, its own; the held hand trades quanta with a tied hand only when its own size moves, as nature's held
  field trades through its own excitation. While the hand stands still, or turns at its exact norm, it trades nothing.

## 2. In the algebra

### 2.1 The residual

- For a monomial f PROD x_(l_i) over its positions i (a gear may hold several), J_g(y) = -f SUM over g's positions of
  PROD over the other positions of y. So SUM_g x_g J_g(y) = -f e1(x; y), e1 the sum over positions of one leg at x and
  the rest at y, and SUM_g X_g(x, y) = -f (e1(x; y) - e1(y; x)) = -f (e1 - e3), e3 = e1(y; x), three legs at x.
- Two legs: e1 = x_1 y_2 + y_1 x_2 = e3, so the books close for any symmetric bilinear J (COUNT5 M1).
- Four legs: e1 - e3 is not 0 in general; with two legs still (x = y on them) and two moving, e1 - e3 = 2 x_1 x_2
  (y_3 y_4 - x_3 x_4).

### 2.2 The middle form

- **Statement.** A monomial of even degree d (its value legs; the unit's legs read 1) pushes its leg at position i by
  (4 / d) SUM over the halves S of the value positions that hold i, PROD over S other than i at the first slot and over
  the rest at the second. Call it M_i(x, y). The train's passing is SUM over its gears' positions of
  -f (x_g M_i(x, y) - y_g M_i(y, x)) on (a, b) and on (a+, a).
- **The books.** SUM_i x_(l_i) M_i(x, y) = 2 Q(x, y), Q the sum over the halves S of PROD_S x PROD_rest y, each term
  counted d/2 times by its d/2 legs at x, times 4 / d. Swapping x and y maps each half to its complement, so
  Q(x, y) = Q(y, x) and the monomial's sum over trains is 0.
- **Oddness.** Each gear's share is antisymmetric in (x, y), so S on (b, a, a+) is minus S on (a+, a, b), and the click
  tooth runs back by the same act on the mirrored state (COUNT5 M1's lemma).
- **For d = 2** M_i is twice the other leg at the second slot: the act's X doubled. A train's own monomials give 0.
- **What it books:** the continuum split E_A = H_A + V/2, E_B = H_B + V/2, whose exchange (P dQ - Q dP) / 2 does not
  vanish when one side stands still: a still held hand clicks opposite its tied train.

### 2.3 The background form

- **Statement.** A monomial c PROD over its legs, joining the held train (flagged by character, load.trains_of) to one
  other train, factors as c P Q with P the other train's legs and Q the held legs. On the window (b, a, a+) it books
  S_held = -2 c P(a) (Q(a+) - Q(b)) and S_other = -S_held. A monomial whose value legs all lie in one train books
  nothing. Two-leg monomials keep the act's form.
- **The books** close by construction, monomial by monomial.
- **Oddness.** P(a) is the now slot's, kept by the reversal; Q(a+) - Q(b) changes sign under it. So each share is odd,
  and the click tooth runs back by the same act.
- **Whole, local, one pass:** products of the Node-clock's own counts at the three slots of the window S already reads,
  no division, no Mesh.
- **What it books:** the continuum split E_held = H_held, E_other = H_other + V, whose exchange is k' . dV/dk: 0 while
  the held hand stands still, whatever the tied hand does. Its one asymmetry is which train is the background: the held
  train, by its character, with no name.

## 3. On the board

- The loader lays J's potential as monomials from the kinds' tables, the zero entries among them at factor 0. On B4's
  pair world 532 of its 772 monomials have four value legs; 96 join the held train to one tied train, at the factor
  60,000 (hold f C), and the other 436 lie at factor 0 (pair_world.py's count).
- So on the night's worlds every live four-leg monomial joins the held train to one other, which the background form
  covers. A four-leg monomial joining two trains neither held, or three trains, would need the middle form (OPEN).

## 4. In the clicks

- **A still hand clicks nothing,** under the background form: on the act its held passing is non-zero exactly in the
  windows where the hand's size moved (below).
- **The tied hand's mass is its own:** a tied hand swinging in its mass term books nothing with the held hand.
- **The held hand trades through its size:** where |k|^2 moves, the tie's energy moves between the held hand and the
  tied hands, and the clicks count it.
- **The energy meaning holds to the leapfrog's own order:** for a quartic coupling the act keeps no energy exactly, so a
  passing that counts each train's energy exactly and closes the books exactly cannot exist; the books are exact.

## 5. Measured

- **passing4.py** (node-live 575973a20, also byte for byte on f72067cdf; four Mesh-less Node-clocks, 400 rounds; the
  held hand (k1, k2) under the hat 1 at n = 5^10, the tie 3, the tied train's own spring n, teeth 2000 n):

  | lay | books open: act / middle / background | held passing not 0: act / middle / background | windows where the size moved |
  |---|---|---|---|
  | (A) the hand laid at its rest | 1,600 / 0 / 0 | 1,600 / 1,600 / 1,565 | 1,565 |
  | (B) the size laid off its rest | 1,600 / 0 / 0 | 1,600 / 1,599 / 1,582 | 1,583 (one window with P(now) = 0) |
  | (C) a stiff hat 10^4, teeth 10^6 n | 1,598 / 0 / 0 | 1,598 / 1,598 / 365 | 365 |

  Every form is odd under the window's reversal in 1,600 of 1,600 windows of every lay.
- **pair_world.py** (B4's pair world from tests/test_the_tensor24_run.py's own files, the real loader and act of
  node-live 575973a20): over 400 rounds the act's passing opens the books in 146, the first at round 57, as the
  architect found where |k|^2 first reaches 2; the background form in 0. The held hand's |k|^2 runs from 0 to 2.

## 6. What stands, and OPEN

- **Stands, for the architect and the click's deriver:** the background form for the held hand's ties and the hat
  (whole, local, one pass, odd, the books exact), with the middle form named for four-leg monomials between trains
  neither held.
- **OPEN:**
  - the key's scale: the middle form runs at twice the act's, the background form at the act's;
  - odd degrees (a three-leg vertex) under the middle form;
  - a world where the hat swaps in for frame 6 with the background form, read end to end by the decoder;
  - the click's energy meaning beyond the leapfrog's order.

## 7. How this text checked itself

- The residual -f (e1 - e3) derived by hand and seen in the act's books on every lay; the middle form's symmetry and
  both forms' oddness proved, then measured in 1,600 of 1,600 windows.
- A case built to break the background form: the stiff hat, where the hand still jiggles by a count; its held passing
  is non-zero in exactly the 365 windows where the size moved.
- A slip of my own in pair_world.py's first run: it took a train's kind count for its row count (the tied trains hold
  six rows, not two); with the rows read from the firsts the result stands (146 against 0), and the factor-0 count above
  says why the slip did not show.
