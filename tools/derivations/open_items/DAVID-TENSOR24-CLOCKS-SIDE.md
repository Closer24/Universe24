# The clocks' side of the third click: a clock's books under any turn, and its line

David, 2026-10-31, 06:3x UTC, beside THIRD7, for the THIRD pair, on the Boss's word (#2187 6539961086 item 2: "write
the clocks' side as a short text beside THIRD7, for the THIRD pair: the identity, B C = 0, and each clock's line its
passing's carry"). It rests on NOT_CLOSED 29 (DAVID-TENSOR24-PASSING4.md, DERIVED: the split at the rest and its pair
carry, section 14) and reads Big Pic's three clicks (bigpic-3clicks 6e7d5874d: PICTURE.md, its section 7's law and
proof, mode 11 in circ.py). Status: **PASSED by both readers of the THIRD pair** (the Boss's 6540720252 item 5); their
five MINORs are folded here (09:4x UTC), with the owner's two words of about 09:30 UTC that bear on section 4 (a clock
reads only its own clicks; the teeth go out of the record). Letters as in Big Pic's PICTURE.md: D the edge dial, K =
C^T C the turn's matrix, h the birth (D - 1) div 2.

**The finding in one line:** at an edge end the carry t + x = q D + r, and a turn then writes the next tooth r + d;
summed over any run, D times a clock's booked total is its swept passing, plus its end teeth at the birth less now,
plus every d at its ends. So a clock's books stay a bounded distance from its passing exactly when the turn's moves at
its ends stay bounded, and within its teeth when those moves sum to 0, wraps counted. Any move of C times anything
does that, since B C = 0, the boundary of a boundary; on one triangle the circulation is the only such move. Under
mode 11 a clock's line is made by its own edges' carries alone, the same whatever the triangle's tooth and twin hold,
and over any run it books its passing within its teeth; round by round it is neither one carry of its passing nor the
first click's line. Read from the clocks, the split click gives each edge the difference of its two clocks' passings
and each triangle its circulation, since B^T B + C C^T = 3 I on a triangle; on n clocks all pairwise joined it is n I,
so the split extends with no division and no pick where n is odd.

## 1. In clocks

- **An edge is a pair of clocks with one pair of teeth.** Two trains the split joins at a Node-clock share an edge. Its
  lower end's tooth carries the round's flow into the lower train, and the higher end, its tooth the complement, clicks
  the opposite quotient (NOT_CLOSED 29, section 14). A clock's line is the sum of the quotients at its edge ends.
- **A clock's books** are its booked total against the passing swept into it. Every quantum it books came through one
  of its edge teeth.
- **A turn between the carries moves teeth.** Whatever it moves at a clock's ends, unless those moves sum to 0 there,
  enters the clock's booked total with no passing behind it: the drift.
- **The circulation keeps every clock whole.** Moving one step around a triangle, each of its three clocks gains on one
  of its edges what it gives on the other. So a turn that moves teeth only around the triangle leaves every clock's
  books where its passing put them, and what it chooses is the path.

## 2. In the algebra

**The setting.** At one Node-clock: clocks V; edges E, the pairs of trains the split joins; triangles F, three clocks
pairwise joined. B (V by E) is each clock's sign on each edge, +1 at its lower end and -1 at its higher. C (E by F) is
each edge's sign on a triangle's boundary, [j, k] - [i, k] + [i, j] for i < j < k. D is the edge dial, odd. In a round,
x_e is the flow into edge e's lower end and t_e its lower end's tooth; the higher end holds D - 1 - t_e.

- **One round at an edge.** t + x = q D + r, 0 <= r < D (Rule3's carry); the higher end carries (D - 1 - t) - x =
  (-q) D + (D - 1 - r), so the two ends click q and -q and keep their sum D - 1 (section 14). A turn then writes the
  next tooth r + d at the lower end and its complement at the higher, d any whole number; a turn that reduces a tooth
  on its own dial writes d less D times the wrap it drops.
- **The identity (DERIVED).** From D q = x + t - (t_next - d), summed over the rounds 1 to N:
  D (sum of q) = (sum of x) + t_1 - t_(N+1) + (sum of d). Applying B, for every clock v:
  D (v's booked total) = (v's swept passing) + B_v (t_1 - t_(N+1)) + B_v (sum of d).
  The probe checks this form at every place. For the bound, write r_N, the last carry's remainder, for t_(N+1) less
  the last move: D (v's booked total) = (v's swept passing) + B_v (t_1 - r_N) + B_v (the moves of rounds 1 to N - 1).
  Both teeth there lie in [0, D), so the middle term is less than D times v's number of edges. So v's books stay a
  bounded distance from its passing exactly when B_v (the moves so far) stays bounded, and within its teeth, for every
  N, when the moves of rounds 1 to N - 1 sum to 0 at its ends: at every N when B_v d = 0 each round.
- **B C = 0 (DERIVED).** For [i, j, k]: at i, B on [i, j] and [i, k] is +1 and +1, against C's +1 and -1; at j, B on
  [i, j] and [j, k] is -1 and +1, against +1 and +1; at k, B on [i, k] and [j, k] is -1 and -1, against -1 and +1. Each
  sums to 0. So d = C w, for any whole w per triangle and round, keeps every clock's books within its teeth.
- **On one triangle, only the circulation (DERIVED).** B d = 0 is three conditions on three moves, one of them the sum
  of the others (the columns of B sum to 0), so its whole solutions are d = C w.
- **Every row of the bench, read by the identity:**
  - no turn (mode 0): d = 0;
  - C C^T less its diagonal (mode 4): its shears move the edge teeth by 2 (C C^T - diag(C C^T)) h, and B diag(C C^T)
    h is not 0 (THIRD6's drift);
  - the full C C^T with each tooth reduced on its own dial (mode 8): the moves are C times something, less D times each
    edge's own wrap, and B of the wraps is not 0 (Big Pic's 6539776461);
  - the same with each wrap booked as a click on its edge (modes 9 and 10): booking the wrap's quotient is moving the
    tooth unreduced, so the moves are C times something, B d = 0, and the books hold; the identity says nothing of
    when the wraps land, so it is silent on their memory, which Big Pic measured;
  - the triangle's own tooth (mode 11): the edge teeth carry p = 3 x - C C^T x at the dial 3D and are not turned (d =
    0), and the triangle's landings book C W, so B q = B Q + B C W = B Q (Big Pic's L2), and the identity at the dial 3D
    with B p = 3 B x is his L3.
- **The line under mode 11 (DERIVED).** B Q reads the edge teeth and the passings alone, never the triangle's tooth or
  twin, so no hidden unit there moves a clock's line, and over any run the line books 3 B x within the teeth. But B Q is
  a signed sum of per-edge carries: two carries can each round down where one carry of their sum would round up, so
  round by round it is not one carry of the clock's passing, and it is not the first click's line, which carries x_e
  at the dial D edge by edge. A wording that fits all three: each clock's line is made by its own edges' carries of
  their shares alone, the same whatever path the third click takes, and over any run it books its own passing within
  its teeth.

## 2a. The split click, read from the clocks

- **On one triangle, B^T B + C C^T = 3 I (DERIVED; CHECKED).** So Big Pic's split, 3 x = (3 x - C C^T x) + C C^T x, is
  3 x = B^T B x + C C^T x. With P = B x, each clock's own passing, the edge's own share is (B^T B x)_e = P_lower -
  P_higher: each edge carries the difference of its two clocks' passings, and the triangle carries the rest, its
  circulation c (c . x). So on each edge the split click reads only its two clocks' own passings, and B (B^T B x) =
  (B B^T) P = 3 P - (sum of P) = 3 P, the clocks' passings summing to 0.
- **On n clocks all pairwise joined, with all their triangles, B^T B + C C^T = n I (DERIVED; CHECKED for n = 3 to 7).**
  On the diagonal, 2 (an edge's two ends) plus n - 2 (the triangles it lies on). Off it, two edges at one clock lie on
  exactly one triangle together, and by B C = 0 at that clock their boundary signs' product is minus their incidences'
  product, so the two matrices cancel; two edges with no clock in common share neither. So n x = B^T B x + C C^T x,
  with no division and no pick: each triangle's own tooth carries c_f . x, each edge the difference of its two clocks'
  passings at the dial n D, and B C = 0 keeps every clock's line its edges' alone, booking n P within the teeth. A lone
  edge at the dial n D carries n x_e from the birth n h + (n - 1) / 2, and for odd n its quotients are the first
  click's at D, as in Big Pic's L5 (n r + (n - 1) / 2 < n D for every remainder r below D).
- **The triangles are dependent for n >= 4.** K_n has n (n - 1) (n - 2) / 6 triangles, and their boundaries span its
  cycles, (n - 1) (n - 2) / 2 of them, so for n >= 4 they are more than the cycles: on four clocks the four triangles'
  boundaries, signed, sum to 0 (the boundary of the tetrahedron). So C has a kernel there and K = C^T C is singular:
  the split above stands, since C C^T x is well defined, but the triangles' teeth carry dependent shares, and a turn
  at K leaves K's kernel unturned.
- **Two limits, OPEN:**
  - for even n the dial n D is even, against the label rule's odd dial (Big Pic's 6539416690 item 4);
  - where a place's joined clocks are not all pairwise joined, an edge can lie on two triangles without the full set,
    and B^T B + C C^T is no multiple of I there (four clocks less one edge: rows 4; 3, 1; 1, 3; 3, 1; 1, 3), so the
    split's form there is open.
- **For the law's case** (Sofer's 6540070751 item 3 (b)): Big Pic's proof as written covers each edge on at most one
  triangle, the case the law now names. The split and the clocks' books extend to every place whose joined clocks are
  pairwise joined and odd in number. The third click's turn there, with several triangles sharing edges (K no longer
  3 I, and singular for n >= 4), and its run back and memory, are THIRD7's to derive and measure.

## 3. On the board

The probe is derive/david_open/node/clocks_side.py, its output clocks_side.txt beside it: tensor24-click as node-live
1794d474b's loader lays it, 27 Node-clocks, 200 rounds, whole numbers alone. It steps the real act and books the split's
pair flows (split_d.py's own form, n = 0) on the edges (2, 3), (2, 4) and (3, 4), one triangle (2, 3, 4) at every
Node-clock, at D = 3 x key = 152,434,287. Its turns take their moves from the board's own numbers, with no stand-in
stream: along the circulation, w is the centred remainder of the triangle's circulating passing; per edge, d_e is the
centred remainder of the edge's own passing. With Big Pic's three_clicks folder given, it runs his own edgeclick.py and
circ.py for the lines.

## 4. In the clicks

- **What a record can show.** Under mode 11 a clock's line cannot show the third click. The sides carry it only in
  sum: c . q, the three sides read along the boundary, gives 3 W within 1 in 197 of 200 rounds, while a whole
  circulation stands alone in the sides in 3 of 145 landings (the THIRD pair's reading). The third click's "no" is a
  clock's line that moves with the hidden teeth: two records one hidden unit apart, as the owner's seed test lays them.
  A line that merely differs from the first click's is mode 11's own edge carry, not the third click seen alone.
- **The owner's two words of about 09:30 UTC:** a clock reads only its own clicks, and the teeth go out of the record.
  So a reading of c . x, which reads the teeth, is a board check, and the third click's own click reading is OPEN,
  Big Pic's (THIRD9's readers). This text's identity is a board identity, read on the board's own teeth; it needs no
  tooth in the record.
- **What does not follow:**
  - memory, either way: the identity is silent on when quanta land;
  - an edge on two triangles: B C = 0 still holds, but mode 11's split needs C^T C's own form there (Big Pic's open);
  - any physics from these board readings.

## 5. Measured (clocks_side.txt)

- From the structure alone: B^T B + C C^T = n I on n clocks pairwise joined, for n = 3 to 7 (1, 4, 10, 20 and 35
  triangles); four clocks less one edge: rows 4; 3, 1; 1, 3; 3, 1; 1, 3, no multiple of I.
- B C = 0 at every clock of the click world's triangle.
- **The identity:** off at 0 of the 16,200 (clock, Node-clock, round) places, under every turn.
- **Each clock's largest |D booked - swept| over the run,** against two teeth's range, 304,868,572:
  - no turn: 150,089,166;
  - along the circulation: 141,805,722, with B (every d) 0 at every clock;
  - per edge: 1,764,082,323, about 11.6 dials, with B (every d) reaching 292,354,296, 1,801,152,000 and 1,508,797,704 at
    the three clocks.
- **The lines, on Big Pic's code (mode 0 and mode 11):**
  - 4,644 of the (round, Node-clock, train) lines differ round by round (10,827 and 10,611 lines);
  - every clock's total is the same in both (0 difference at every clock), a reading of these 200 rounds, not a law;
  - one hidden unit in the triangle's twin at Node-clock 0 moves 0 lines and 244 sides;
  - the books open at 0 places, and the run back holds, in all three runs.

## 6. What stands, and OPEN

- **Stands (PASSED by both readers; DERIVED, CHECKED on the board):** the identity for any turn; B C = 0; on one
  triangle the circulation is the only move that keeps every clock's books; under mode 11 each clock's line is made by
  its own edges' carries alone, the same whatever path the third click takes, booking its passing within its teeth
  over any run; the split click as each edge's difference of its two clocks' passings plus the triangles'
  circulations, B^T B + C C^T = n I on n clocks all pairwise joined.
- **OPEN:** even n; a place whose joined clocks are not all pairwise joined; the turn with several triangles sharing
  edges, K singular for n >= 4; the third click's own click reading with no tooth in the record (Big Pic's); the
  memory of mode 11's per-clock lines on the board, THIRD7's rows; which turn the act takes.

## 7. How this text checked itself

clocks_side.py run once on node-live 1794d474b's src with Big Pic's folder at bigpic-3clicks 9c78397e5 (its
edgeclick.py and circ.py unchanged through 6e7d5874d), about 2 minutes; the identity checked in code at every place,
not only its bound; B C summed in code at every clock; the lines read through Big Pic's own run functions, not a copy;
the derivation's two signs at each vertex checked by hand above; the probe types no train, row or number of the world
(the factor 3 of the dial, kappa 6 and n = 0 are NOT_CLOSED 29's). The notes' fold (09:4x) renamed the dial D in the
probe's printed lines and reran it; every number printed is unchanged.
