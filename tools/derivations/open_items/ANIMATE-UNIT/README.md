# n's unit and the click's key: in clocks, in the algebra with the 24, and in the clicks (G3's open item 3)

Animate, 2026-10-30, for David's G3 list (DAVID-TENSOR24-G3.md, section 4, item (3): "n's unit in counts: a standing
count sweeps no area, so term 11's quantum, counted on the swept area, does not count it") and the Boss's term 11
(derive/boss/term11/TERM11.md: "the key's value: one number for every train and every mode ... OPEN"), on the owner's
words to Animate (in Hebrew; in translation): "Check with David which pieces you can complete, perhaps the coupling
family?" and "Remember everything from the clocks to the algebra to the physics in the clicks; think of the 24
operations." The Boss gave the piece to Animate if David agrees (#2187 6523515918), and David agreed (6523872509),
naming the key hbar, not h, as his reader of term 11 found: one key carries the key times the beat.

The probe is unit.py, its output unit.txt beside it, on the Node-clock's own act (engine/step.py, main 6f31d41bb), in
whole numbers alone: Rule3's carry for every division, no float, no root, no circular call, no random draw, no fraction.
`python3 tools/derivations/open_items/ANIMATE-UNIT/unit.py`, about ten seconds. The page goes forward: the clock, then
the algebra, then the physics. Status words as the protocol's: DERIVED and CHECKED, CHOSEN, OPEN and REFUSED.

## The answer

1. **A count is not a quantum.** The click counts a turn, a swept area; a held count stands, and a hand that stands
   turns nothing. The mirror tells the two apart (it sends every turn to its opposite and keeps every count), and the
   24 keep both. So no click ever counts n, and n becomes a number of quanta only through a beat. DERIVED; CHECKED.
2. **The act fixes no key.** The click writes nothing, so the gears run alike at every key, and the clicks read only
   each strength times the key: every swing times 3, the key times 9 and a four-leg stop over 9 leave every click in its
   round with its sign. So the key's value is CHOSEN: one odd whole number for every train (the Boss's books), its
   calibration against nature coming with G3's strengths.
3. **n's unit is the key's.** The steady count holds kappa n^2 / (2 key omega_k) held quanta per Node-clock, its
   winding's energy over one held quantum's. Read so, the law's sentence "the coupling family's steady count is one
   quantum per Node-clock" (decision 40 (g); ALGEBRA.md line 35) puts the Mesh near the held boson's Compton length,
   about 10^-18 m, where the time of flight of the highest-energy photons bounds the Mesh below about 10^-26 m: REFUSED
   by nature, by about 10^8, if the held count is the Higgs field's counterpart. Nature reads about one held quantum per
   the held boson's own volume, 1 / (4 lambda) with lambda = m^2 / (2 v^2) = 0.13, so n's value is the held count's own
   quartic times the key (G3's item (2)): OPEN.
4. **The 24 on a steady count.** Only a count of kind A1 keeps all 24 turns; a count of any other kind is kept by 12 or
   fewer, by its direction; its size and its sign never enter. So a steady count breaks the 24 by its kind, not by being
   odd. CHECKED.

## 1. In clocks

- **A click counts a turn.** Two hands in mesh trade turns, and the click is the counter on the taker's side: one notch
  per key of area turned into it (term 11; the world of ANIMATE-CLICK/click.py, the Boss's TERM11.md). A turn is how far a hand stands from its centre times how
  fast it moves across: an area.
- **A held count is a winding that stands.** The held hand of G3 stands wound at n, its own spring holding it there. A
  hand that stands turns nothing, so the counter never moves for it. Laid off n it swings along one line (it has one
  part), and a swing along a line turns nothing either.
- **The mirror tells a winding from a turn.** Running every gear back keeps where each hand stands, read over the half
  round, and sends every turn to its opposite. So no turn is a function of where a hand stands, and a count is never a
  number of clicks by itself.
- **The 24 keep both.** The cube's turns move a hand's rows and never its parts, so the turn between the parts, summed
  over the rows, is the same in every frame, and so is a count of kind A1. The 24 do not tell a count from a turn; the
  mirror does.
- **A beat stands between a count and its quanta.** A hand of radius n turning at its beat sweeps n^2 times the teeth
  times the beat's sine. A hand that stands holds its winding as energy, and counts it in quanta as the clicks count
  every quantum: the energy over the key times its own beat in radians per round (E = n hbar omega, the key as
  hbar; unit.txt 6).
- **So the law's sentence can stand in the clocks in two ways.** (a) The coupling family turns: an ordinary family of
  two parts whose hand turns at one key of area per Node-clock; the books count one quantum there, nothing moves its
  area, and the tied families take the one spring from the square of its radius. (b) The held hand stands, and the
  sentence counts its winding's energy in held quanta. Either way a beat ties n to the key; section 3 reads both.
- **The key is how many fine teeth of area make one notch.** The counter pushes nothing, so the gears turn alike at
  every key and only the notches change. A key is the counter's setting, not a law of the gears; what the clicks read
  is a strength measured in notches.
- **A steady count of another kind points.** A count of kind A1 is the same seen from every face of the cube. A count
  with rows (A2, E, T1, T2) is carried by some turns onto another count, so it singles out the turns that keep it: it
  points along the cube. Twice the count, or minus it, points the same way, so its size and its sign never decide which
  turns keep it.

## 2. In the algebra, with the 24

- **The area.** For a hand of kind K with two parts (re, im), with C = C[K, K -> A1] the 24's table onto A1:
  Omega = SUM_{j,i} C_ji (re_j p_im,i - im_j p_re,i), p = W (a - b) + r. Exactly, Omega = W X + Y with
  X = SUM C_ji (im_j re^b_i - re_j im^b_i), the counts' own cross of before and now, and
  Y = SUM C_ji (re_j r_im,i - im_j r_re,i), the fine teeth's. A hand of one part has no im rows, so Omega = 0
  identically, at every count. DERIVED.
- **The mirror**, (a, b, r) -> (b, a, w - 1 - r), sends X to -X exactly (C is symmetric: swap j and i) and keeps a + b,
  the count over the half round. So X is odd and every count even under it, and an identity X = f(a + b) holds only
  with X = 0. DERIVED; CHECKED (unit.txt 1: 601 of 601 states, on both hands).
- **The 24.** A turn g acts on a kind K's rows by its matrix D_K(g), and D_K(g)^T C D_K(g) = C for each kind's table
  onto A1, so Omega and every A1 count are the 24's invariants. CHECKED (unit.txt 1: 24 of 24 turns, the five tables).
- **(a) The turning count.** K of kind A1 with two parts, the tied family X of kind T1 with two parts:
  V = F (K.K) + M (K.K)(X.X). The push on K is -2 (F + M X.X) K, along K itself, so the area it moves into K,
  SUM (K_re J_im - K_im J_re), is 0 identically, and Omega_K moves by Rule3's turn alone (David's c2 identity). Laid on
  a whole circle (the triple 5, 12, 13: the step's 2 - 2 F / W = 2 x 12 / 13, so the count turns on a circle of radius
  R from (R, 0) now and (12 R / 13, -5 R / 13) before), Omega_K = W R^2 x 5 / 13 exactly; the key it sets ties the
  radius to the key, R^2 = 13 key / (5 W). The tied spring is 2 M |K|^2 = 2 M R^2, a standing count's 2 G n at
  G = M and n = R^2. DERIVED; CHECKED (unit.txt 2 and 3).
- **(b) The standing count.** V = G k (X.X) + (kappa / 2)(k - n)^2 (G3's 2.1, G = g / 2). Its winding's energy above
  k = 0 is (kappa / 2) n^2; one held quantum carries key x omega_k, with kappa = 4 W sin^2(omega_k / 2), about
  W omega_k^2. So it holds N = kappa n^2 / (2 key omega_k), about W omega_k n^2 / (2 key), held quanta per Node-clock.
  DERIVED.
- **The key is no law of the act.** The click is q_c, k+ = carry(tau, key, k) and writes nothing into a, b, r or r_d
  (term 11), so the state's run is the same at every key. Scale every count by s, a three-leg strength by 1 / s and a
  four-leg one by 1 / s^2: the potential scales by s^2, every push by s, and the run scales with it, the areas by s^2.
  At the key times s^2 every click then falls in the same round with the same sign: the clicks read the laid areas
  over the key, lam x key and g^2 x key, never the key alone. DERIVED; CHECKED (unit.txt 4, s = 3).
- **The 24 on a steady count.** A steady count c of kind K is kept by the turns g with D_K(g) c = c. Over every whole
  count with entries from -2 to 2 (unit.txt 5):

  | kind | turns that keep it | where |
  | --- | --- | --- |
  | A1 | 24 | every count |
  | A2 | 12 | every count: the turns of sign +1 |
  | E | 8 or 4 | 8 on the three lines e1 = -e2, e2 = 2 e1 and e1 = 2 e2 (David's 2.6), 4 off them |
  | T1 | 4, 3, 2 or 1 | 4 on the axes, 3 on the body diagonals, 2 on the face diagonals, 1 elsewhere |
  | T2 | 6, 4, 2 or 1 | 6 on the body diagonals, 4 on the axes, 2 or 1 elsewhere |

  Each count times 2, 3 or -1 is kept by the same turns. CHECKED. So the 24 never read a count's parity: what can be
  odd at the grain is the teeth's, since the flip w - 1 - r keeps a tooth only for an odd w (the fact behind the
  Boss's click tooth born at (key - 1) div 2).

## 3. In the clicks

- **The books on the standing count:** 0 quanta per Node-clock in every round (unit.txt 2). While the held hand
  stands, the law's sentence names no quantum the books can count.
- **The books on the turning count:** one quantum per Node-clock in every round, its area within 0.14 per cent of the
  key over 4,000 rounds; it never clicks, since nothing moves its area; the tied family beats as it does beside the
  standing count, 64 and 64 sign changes in 4,000 rounds. So reading (a) makes the sentence a statement of the books.
- **Nature, on either reading.** If the coupling family's held count is the counterpart of the Higgs field, as G3's
  physics reads it (DAVID-TENSOR24-G3.md, section 3, the held boson), nature reads N. In units with hbar = c = 1, a
  static field v of a scalar of mass m holds N = m v^2 V / 2 quanta in a volume V by the harmonic count, four times
  fewer by a hat potential's depth (v^2 / (8 m^2) per Compton volume). With v = 246.2 GeV (from Fermi's constant) and
  m = 125.2 GeV:
  - per the held boson's Compton volume, N = v^2 / (2 m^2) = 1.9 (0.48 by the hat's depth): about one quantum per the
    held boson's own volume;
  - per Node-clock of side a, N = 1.9 (a / lambda_C)^3, with lambda_C = hbar / (m c) = 1.58 x 10^-18 m;
  - so one quantum per Node-clock needs a = 0.80 lambda_C = 1.3 x 10^-18 m. For any held boson's mass the board can
    beat (omega_k at most pi; m a = sqrt 6 omega_k, light being 1 / sqrt 6 of a Mesh per round), a is at least
    0.51 hbar c / v = 4 x 10^-19 m;
  - the board's light disperses: from sin(omega / 2) = sin(k a / 2) / sqrt 6, along an axis its speed falls as
    1 - (5 / 48)(k a)^2, and along a body diagonal by a fifth of that, never by 0. The time of flight of the
    highest-energy photons from gamma-ray bursts and blazars shows no quadratic dispersion below about 10^11 GeV
    (Fermi-LAT on GRB 090510; H.E.S.S. and MAGIC on flares and bursts; v / c = 1 - (3 / 2)(E / E_QG,2)^2), which
    bounds the Mesh below about 10^-26 m (7.5 x 10^-27 m along an axis, about twice that along a body diagonal);
  - so one quantum per Node-clock is REFUSED by nature, by about 10^8 in the Mesh. At a Mesh below 10^-26 m the steady
    count holds below about 5 x 10^-25 held quanta per Node-clock. A board of the refused Mesh would also hold no
    momentum above pi hbar / a, about 0.5 TeV / c, where the LHC measures jets of several TeV.
- **What nature reads instead.** lambda = m^2 / (2 v^2) = 0.13, and 1 / (4 lambda) is the held quanta per Compton
  volume. On the board (m a = sqrt 6 omega_k, kappa about W omega_k^2):
  lambda = 6^(3/2) kappa key / (2 W^2 n^2), so n^2 W^2 = (6^(3/2) / (2 lambda)) kappa key, about 57 kappa key at
  nature's lambda. n's unit in counts is the root of kappa key over W, and nature reads n at about 7.5 of those units.
  With a hat for the held count, -(mu / 2) k^2 + (nu / 4) k^4 (n^2 = mu / nu, kappa = 2 mu),
  lambda = 6^(3/2) nu key / W^2: the clicks read the held quartic times the key, as section 2 says of every strength.
  So n's value from the law is the held count's own potential (G3's item (2)) with the key: OPEN.
- **The key in nature is hbar.** The act leaves it free; the clicks fix it against any strength nature measures as a
  pure number (lambda above, or a coupling's square). So its value is CHOSEN on the train card with G3's strengths, odd
  for the Boss's books.
- **The 24 in the clicks.** A steady count of kind A1 keeps every reading alike in the 24 frames. A steady count of
  another kind is kept by 12 turns or fewer, and the turns it keeps are what the clicks would read as axes set apart,
  or as split beats (the architecture's families and the three hands; David's G3 2.6).

## 4. Measured (unit.txt)

1. The mirror sends the counts' cross to minus itself on both hands in 601 of 601 states of a run and keeps every
   count summed over now and before in 601 of 601; the 24 keep the five kinds' tables onto A1, 24 of 24.
2. One Node-clock, W = 1,352 x 10^18, F = 104 x 10^18, M = G = 10^10, R = 13,000, n = R^2 = 169,000,000, the tied
   swing 1,000, 4,000 rounds:
   - the standing count moves off n by at most 1 count, and the books hold 0 quanta of it in every round;
   - the turning count's area at the lay, the key it sets, is 87,880 x 10^24, W R^2 x 5 / 13 exactly; the push moves
     area into it in 0 of 4,000 rounds, and its area moves by anything but Rule3's turn in 0 of 4,000;
   - its area stays within 1,395,882 billionths of the key (0.14 per cent), the books holding 1 quantum in every round;
     its radius squared within 626,535 of R^2 (0.37 per cent);
   - the tied family: 64 sign changes beside either count, the two runs' counts parting by at most 33 of its swing
     1,000; its own area 0 throughout.
3. The 24 on the turning count's world: 24 of 24 runs turned state for state over 1,000 rounds, the count's area alike
   in every round.
4. The click world (ANIMATE-CLICK) with a stop lam = 1,251 on the giver, the key a seventh of its area at the lay:
   - 34 clicks, net 6; at three times the key the gears are alike in 6,001 of 6,001 rounds, with 10 clicks, net 2;
   - every swing x 3, the key x 9 and the stop / 9: the 34 clicks alike round for round, sign for sign;
   - every swing x 3 and the key x 9 with the stop kept: 14 clicks, 48 clicks in one run and not the other.
5. The 24 on a steady count, every count with entries from -2 to 2: A1, 24 for all 4; A2, 12 for all 4; E, 8 for 8
   and 4 for 16; T1, 4 for 12, 3 for 16, 2 for 24 and 1 for 72; T2, 6 for 16, 4 for 12, 2 for 72 and 1 for 24; the
   same for 2, 3 and -1 times every count.
6. A quantum carries the key times its beat: on the click world with no stop, the square of the taker's energy gained
   over its area gained, over its beat squared 2 F / W, is 1,032,317,608, 1,003,505,813, 1,002,984,505, 1,002,502,426,
   1,002,240,055, 1,002,169,758 and 1,000,245,221 billionths at its first seven clicks: the energy per key of area is
   the beat, within a few thousandths after the first click (whole numbers; the measure of ANIMATE-CLICK that left the
   tree, re-read).

## 5. What stands, and what is owed

- **DERIVED; CHECKED:** a count is no quantum (the mirror tells a turn from a count; the 24 keep both; a hand of one
  part has no area); the act fixes no key, and the clicks read each strength times the key; a turning count of one key
  per Node-clock is a quantum of the books and gives the tied families the one spring; the 24's turns that keep a
  steady count, by its kind and direction, never by its size or sign.
- **REFUSED by nature:** one quantum per Node-clock (decision 40 (g); line 35) in either reading, if the held count is
  the Higgs field's counterpart: the Mesh it needs, about 10^-18 m, is about 10^8 times what light's time of flight
  allows.
- **CHOSEN:** the key's value, one odd whole number on the train card for every train; its calibration with G3's
  strengths.
- **OPEN:** n's value (the held count's own quartic with the key, G3's item (2)); how the metric reads the turning
  count's uniform energy (G2); whether the held count is the Higgs field's counterpart at all (G3's section 3 lists
  three readings where it differs).

## 6. For the architecture document, through Sofer, when both readers agree

- **Term 6, the mass section's n:** "n's unit in counts OPEN" reads "n's unit is the key's: the steady count holds
  kappa n^2 / (2 key omega_k) held quanta per Node-clock; one per Node-clock is refused by light's time of flight (a
  Mesh near 10^-18 m against one below 10^-26 m); nature reads about one per the held boson's Compton volume,
  n^2 W^2 = (6^(3/2) / (2 lambda)) kappa key; n's value OPEN with the held count's own potential (G3's item (2))".
- **Term 11's status:** "the key's value OPEN (G3)" reads "the key's value CHOSEN: one odd whole number on the train
  card for every train; the act runs alike at every key, and the clicks read each strength times the key
  (ANIMATE-UNIT)".
- **The law's line 35 (Sofer's):** the sentence "the coupling family's steady count is one quantum per Node-clock" is
  refused by nature as read, and the owner's word on it is owed; beside it, "by a steady odd count": the 24's turns
  never read a count's parity, only its kind and direction.
