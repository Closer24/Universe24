# What a whole click pushes back into the gears: nothing (G5, term 11)

Animate, 2026-10-30, for the Boss's G5 ask (#2187 6518694462, item 3: "what a click pushes back into the gears"),
taken in 6518779301. The probe is click.py, run on the Node-clock's own act (engine/step.py with term 6's contraction,
tensor24-review ed745f7cc as merged in reader-5), its output click.txt beside it:
`python3 tools/derivations/open_items/ANIMATE-CLICK/click.py`, about 15 seconds.

## In clocks

- **Two trains in mesh.** A giver and a taker are two hands whose wheels mesh (term 6's vertex). Every round the mesh
  pushes both wheels, each by the other: what one gives the other takes, and no motion leaves the pair.
- **The click is the counter on the taker's side.** It counts the whole teeth that have passed through the mesh into
  the taker, one notch per whole tooth, and keeps the part of a tooth in its own fine tooth, born half way as every
  fine tooth is. A tooth passing back out of the taker takes a notch back.
- **The counter pushes nothing.** The mesh has already moved every tooth it counts. A counter that also pushed the
  wheels would move each tooth twice.
- **The escapement's one tooth, split in two jobs.** In a clock one tooth of the escape wheel both pushes the balance
  and is counted. Here the mesh pushes and the click counts, and they are the same tooth: the area the vertex moves
  into the taker is exactly the area the click counts.

## In algebra

- **The world:** one Node-clock with no Mesh, two families of two parts each, a giver L and a taker M, each a T1 hand of
  three components with a re part and an im part, twelve gears. One potential through the 24's table of T1 with T1
  onto A1:

      V = f (L.L + M.M) + g Re(conj(M) . L)

  f is each hand's own spring and g the vertex. V is unchanged when both hands turn alike in their re-im plane.
- **The swept area** of a hand is Omega = SUM_i (re_i p_im,i - im_i p_re,i) through the same table, with
  p = W (a - b) + r the stride with its kept tooth. On the head's step, exactly,

      Omega+ - Omega = (re F_im - im F_re) + (q_re r+_im - q_im r+_re),

  the push's turn and Rule3's turn, q the quotient and r+ the tooth kept (David's c2).
- **The vertex moves area only between the two hands.** Each hand's own spring turns nothing, and the vertex's two
  turns are equal and opposite, so the two hands' areas change by Rule3's two turns alone.
- **The whole click** (term 11): tau, the area the vertex moves into the taker in a round, summed over its rows through
  the A1 table, carried at the key:

      q_c, k+ = carry(tau, key, k),   k born at key div 2

  The quotient leaves as the event, + for a quantum taken and - for one given back; the remainder stays. Nothing is
  written into a, b or r. So key x (the clicks) + (k - key div 2) = the area moved, exactly, every round.

## Measured (click.txt; W = 10^20, a beat of about 2 pi 20 rounds, g = f / 10, the key a seventh of the giver's area)

1. **The vertex moves area between the two hands and nowhere else:** in 0 of 6,000 rounds do the two areas change by
   anything but Rule3's two turns, and in 0 does the taker's change by anything but the area moved and its own turn.
   Rule3's turns over the run come to 1.9 x 10^-7 keys.
2. **The books are the board:** key x (the clicks) + (k - key div 2) equals the area moved in 0 of 6,000 rounds
   missed, and equals the taker's area less its Rule3 turns in 0 missed.
   - The clicks: 34, in order +7, -7, +7, -7, +6 as the area goes over and back.
   - The count runs from 0 to 7, and the area moved less the count stays within half a key.
3. **A quantum carries the key times the beat:** the taker's energy gained over its area gained is 0.05080, 0.05009,
   ..., 0.05001 at its first seven clicks, against its beat sqrt(2 f / W) = 0.05000. That is E = n h nu per mode,
   with the key as h.
4. **The run back:** 6,000 of 6,000 rounds run back to their way out's state, and the click's kept tooth returns to
   its birth, key div 2. The click adds nothing the gears do not hold.
5. **The 24:** under every one of the 24 turns, the run is turned state for state over 1,500 rounds, and the clicks
   and kept teeth are alike in every round. A gear sent to minus a gear has its fine tooth flipped in its teeth,
   W - 1 - r, as the mirror flips it: the carry of a negated sum is then the negated carry, exactly.
6. **No vertex, no click** (Sofer's hold, The light no bob, line 148): with g = 0 no area moves and nothing clicks,
   while the giver's own area moves by its Rule3 turns alone (3.8 x 10^-5 keys over the run). The click reads the
   area a coupling moves into a train, so a train no coupling touches is never credited by its own area.
7. **Mutants:**

   | mutant | what fails |
   | --- | --- |
   | a write at the click: the giver shrunk along itself by the clicked keys, way (b)'s write beside the vertex | at each click the two hands' area less Rule3's turns drops by 0.96, 0.94, 0.90 keys, where it moves by 0 without the write: each quantum is taken twice |
   | the click's tooth born at 0 | the taker's area dips 0.0006 keys below 0 at the return, and the record shows a click and its return there (2,496 and 2,511), and a quantum held 29 rounds at a peak 0.0043 keys past seven (1,241 and 1,270): 38 clicks against 34, the count down to -1 |
   | a gear's click: each component's area carried alone, laid along x and y at once | the net count agrees (12), and the clicks fall in other rounds in 102 rounds: gears clicking alone, which line 1556 forbids |

## In physics

- **Absorption and emission are one carry's two signs.** Two resonant hands trade a quantum back and forth, and each
  trade is a click, + where the taker's area passes a half key upward and - where it passes one downward. This is the
  Rabi exchange of an atom and one mode of light, absorbing and emitting in turn.
- **Planck's relation per mode:** a quantum is one key of swept area, and the energy it carries is the key times the
  taker's own beat.
- **The click writes nothing, so the run back is exact** (Postulate 4). A detector's click is not given back because
  its taker passes the area on to further hands, not because the click writes.
- **Way (b) and the vertex:** way (b)'s write (DAVID-TENSOR24-THE-TAKE-ON-THE-GEARS.md) was for an intensity channel,
  a coupling that modulates light and moves no area. Term 6's vertex is a phase partner, so it moves the area itself,
  and the click needs no write, as David's page says in its 6.1 ("the click would be the carry of M's sweep at its
  winding, with no write at the click"). This probe shows it on the node's act.

## What this closes, and what stays open

- **Closed (term 11, the whole click):** it pushes nothing back. Its carry is the area the vertex moves, its kept tooth
  is born at the half key (ALGEBRA.md, The one rule of the remainder, (i)), and it adds one count and one kept tooth
  per train and Node-clock.
- **The key's value** is the probe's here: one number for every train and every mode (TENSOR24_NODE.md 4.5), its unit
  owed by the train card and G3.
- **The split click's push back stays open** (term 12; the gathering). There the twins' areas sit in two takers, and
  the record credits the whole quantum to the one drawn. This probe's vertex moves area only between hands that one
  Node-clock couples. Three candidates are named, none derived:
  - **(a) A write at the Node-clock where the twins were one** (form B), moving the other twin's area into the drawn
    twin. Way (b)'s radial form divides by the twin's own area, a teeth count held at least 1 by a whether, which the
    node's rule of no bound in a round forbids; another form is owed.
  - **(b) A signed debt in the click's kept teeth, with no write.** Each detector's books and board then walk apart as
    the square root of the number of draws, unless the debt enters the next draw's sizes. That would correlate
    successive outcomes, where nature's are independent.
  - **(c) The two halves' product pushes.** After the draw, what clicks and what pushes the metric is the forward size
    times the backward confirmation, so a losing branch neither clicks nor pushes (Page and Geilker). That changes
    what the forward board alone does, so it is a new rule, the owner's.
- **The draw's source on this act: the node owes its dial** (draw.py, draw.txt; decision 29: d = (c + V) mod L, c the
  Node-clock's beat count, V the seven Node-clocks' A1 fine teeth in pitch units, L the sizes' total).
  - The node holds no round and no time (TENSOR24_NODE.md section 0), so it has no c, and the draw reads V alone.
  - On the act as built, its plan empty until G3, with one light train on a board of 6 by 6 by 6 at the example's
    W = 6 grip, a fine tooth takes six values in pitch units, so V spans 11 to 62 over the seven Node-clocks. For L
    of 2, 3 and 10 every value of d is reached; for L of 70, 97, 1,000, 16,384 and 1,048,583 only 51 are, so a part
    whose sizes lie beyond V's top is never drawn. A plan's strengths enter the pitch (the gcd of W and the push's
    coefficients) and may make it finer: that is for G3's strengths to measure.
  - Read on the rows' now counts in place of their fine teeth, d is flat for L of 10, 70 and 1,000 (chi-square 6.6,
    9.7 and 10.7 on 9), not at 97 (215.2; the rounds' samples run close together, so the chi-square counts them as
    more than they are), and not for 16,384 or more, beyond the counts' own span (-7,956 to 8,555).
  - So decision 29's exact fairness, each part drawn exactly its size times over any L beats, needs c, a count that
    steps once a beat and so turns through any L. Two candidates, for David and the Boss: (a) the Node-clock's own
    time gear, an A1 gear stepping one count a beat, which slows where the teeth grow (term 2) and which the decoder's
    clock reading needs as well; (b) the sizes read at a resolution within V's span, which is Born's rule only to that
    resolution.
  - A dial alone gives the exactness over L beats and not independence. With c stepping one count a round, two rounds
    in a row draw in one half 0.789, 0.850 and 1.000 of the time at L of 70, 97 and 1,000, and Node-clocks one Mesh
    apart 0.824, 0.871 and 1.000, where independent draws give 0.500 (as at L of 10). So independent draws need V's
    span to reach L. On the act as built it is about 50, while a part's size is a norm of counts, a sum of two
    squares. The plan's strengths (G3) may make the pitch finer; where they do not, the draw owes the node finer
    digits.
  - V's pitch moves with W on the slot form once the metric moves (G2); at rest it stands.
