# The Node-clock, closed: its whole act in one place

The owner's word to the Boss of 2026-10-30, 06:1x UTC (in Hebrew; in translation): "Why not close the node completely?
The rest is easier than it.." and "Yes. It is tensorial and algebraic, right..?". This page is the Node-clock's whole
act, every term in one round, before any more of it is built. For each term it says what it reads, how it is computed,
where it comes from, and whether it is BUILT, DERIVED (owed in code only) or OPEN (owed a derivation, by name). When
every term is DERIVED or BUILT, the node is built at once, with one hostile reader, and only then the loader, the runner
and the decoder catch up.

## 1. The rules every term keeps

- **Algebraic:** whole numbers and Gaussian integers; addition, multiplication and Rule3's carry, the one division
  (algebra/carry.py). No root, no table typed, no float, no number beyond 0 and 1 in the code (a two comes from the
  structure it counts).
- **Tensorial:** every gear is one component of one of the 24's kinds (A1, A2, E, T1, T2) at one part. Every product of
  gears is a contraction through the 24's tables, derived once from the Node-clock's own star (decision 42). The metric
  is the four-vector's symmetric square, ten slots (00, the 0i, the ii, the jk by their third axis).
- **Local:** a Node-clock reads its own gears and its six neighbours' through its Meshes, at the now slot, and nothing
  else (Postulate 1; decision 42).
- **No if, no loop, no mask, no bound, no book in the act** (Postulate 5; the laws of 2026-10-30). A condition becomes a
  weight only through Rule3's carry, read by Sofer.
- **Nothing declared:** no particle, mass, coupling or strength in a file (decision 35). The files lay families (kinds,
  parts, pairs), the board and the start.
- **The run back is exact** in its stated domain, by the act on the mirrored state (G1b (ii)).

## 2. The state

Per gear row and Node-clock: a (now), b (before), r (the gear's fine tooth, within [0, W)), r_d (the drive's fine tooth,
within [0, T_d)). The rows are every family's kinds times their components times their parts, laid by the files:

- the files' families (light and matter seeds);
- the metric family: the train whose kinds' character is the square's, ten rows in the square's own basis (G1b (i));
- the coupling family (G3): an ordinary family, its steady count one quantum per Node-clock from the law (decision
  40 (g)), its kind OPEN (decision 40 (h), David).

## 3. One round, term by term

Every gear of every Node-clock steps once a round, in one pass, at the now slot (G1b (iii)):

    q, r+ = carry(W (a - b) + s F + K, W, r),    a+ = a + q,    b+ = a

| # | Term | What it reads | How it is computed | Status |
|---|---|---|---|---|
| 1 | the readings | the gear's now count, its six neighbours' | the value a; the gradient, the neighbours contracted with the Spokes' directions (tensordot); the pull, F below | BUILT (G1b (iv)) |
| 2 | the teeth W | every square's 00 slot here | W = the rest + the 00 slots' now counts, linear (decision 41's slot form, line 35) | BUILT |
| 3 | the grips | every square's ii slot at both ends of each Mesh | each Spoke's grip = the rest grip + its axis's ii slots here and at the neighbour | BUILT (part 4) |
| 4 | the pull F | the neighbours' now counts, the grips | F = sum over the six Spokes of grip (neighbour - own) | BUILT |
| 5 | the metric's push | every gear's four-vector here: its stride (a - b) and its gradient | the stress tensor T, each family's four-vector contracted with itself through the 24's tables onto the square's ten slots; each slot pushed by its component of 2T - eta T (N3: the 00 slot by rho + 3p, the diagonal three by 3 (rho - p)); the metric's own gears in T (decision 40 (a)) | OPEN (G2): see 4.1 |
| 6 | the coupling vertex | the coupling family's gears and every other family's, here | the one plan: each vertex a contraction of its legs through the 24's tables, pushing every leg | OPEN (G3): see 4.2 |
| 7 | the drive | J, the sources of 5 and 6 | q_d, r_d+ = carry(J, T_d, r_d): one drive for every row (decision 40 (d)) | DERIVED (G3) |
| 8 | the kick K | the drive's quotient | K = T_k s q_d; s = 1 | BUILT at T_k = 1 |
| 9 | the spring | the gear's own count | the clock's one notch, D / W = 2 / Gamma (line 352), the swing's top (Postulate 4) | OPEN (G2): see 4.3 |
| 10 | the shift and shears | the 0i and jk slots | read by the gradient's and the pull's contractions (frame dragging, waves) | OPEN (G4): see 4.4 |
| 11 | the whole click | the drive's carry | q quanta click, the remainder kept in r_d: the record's how much and when | DERIVED (G5): see 4.5 |
| 12 | the split click | the parts' sizes sigma | the draw by a rank count over the sizes; a full slot refuses after the draw (decision 40 (b)) | OPEN (G5): see 4.5 |

## 4. The open terms, each with its question and its deriver

### 4.1 The metric's push (term 5), G2: David derives, the Boss builds

- **The tensor:** for a family of kind K, each component x has its four-vector v_x = (the stride a_x - b_x, the
  gradient of a_x along each axis). T = sum over the families of C[K x K -> A1]_(x, y) v_x (x) v_y, symmetrised onto the
  square's ten slots: the same construction as kinds.square, read on the state (David, 6514906323, item 3).
- **The push:** each slot of the square gets its component of 2T - eta T (N3), at one strength per slot from the law.
- **Postulate 6:** two sources' strides add bit for bit, and the rates compose by their product. The cross term
  c1 c2 / W0 comes from the metric's own gears in T (David, 6515406887); the test's mutant is the same act with the
  self-push off. OPEN: the self-push's exact form, and the order at which the cross term shows.
- **The run back (N2):** a push that reads the stride must run back. The matter steps first, so the metric reads its
  rates at both slots; a push that reads its own rate has no bijection. OPEN: the first-order form (each rate in its own
  slot), and with it the run back exact while the clock moves (G1's limit, the plan's G1 entry).
- **The slicing (N1):** the free count d_mu ((-g)^w g^(mu nu)) = 0 at w = 1/2, so the course and the static field agree
  with Cassini. OPEN: its form on the act.

### 4.2 The coupling vertex (term 6), G3: David derives, the Boss builds

- **The one plan:** an ordinary coupling family, its leg in every source; each vertex pushes all its legs (energy kept).
- **The legs:** three-leg vertices alone hold no count (David's board2mass 3.6: a cubic form's stationary rays are flat,
  and the push drives the count below 0). OPEN: the four-leg term that bounds the whole potential, as nature's quartic.
- **The strength:** in the vertex law, read through the ruler, no file holding it (decision 35); no single integer serves
  all tables (David, 6501657960, item 5). OPEN.
- **The tables:** read in the square's basis where E stands, so E's ten oblique tables are never read (David,
  6516176163, item 4). The tables' derivation with no seed and no search: the row of S = P times E's form at its first
  diagonal entry not 0 (the Boss's 6515929376, David's closed form). DERIVED.
- **The held count:** a family's components are read against no direction of the board, or the clicks see a turn change
  one species into another (David's G3 findings). OPEN: which vertices the one plan lays.

### 4.3 The spring (term 9), G2

- The clock's one notch, D / W = 2 / Gamma, derived from den and Gamma (line 352): the board's mean count swings and
  returns (Postulate 4); the metric's spin-2 part keeps the spring 0, so gravity's two polarizations stay massless.
- OPEN: its place in the slot form (decision 41), the swing's top as the act's own turning point (OPEN 7).

### 4.4 The shift and shears (term 10), G4

- The 0i slots (T1) read as the lean of the now toward each neighbour, the jk slots (E + T2) as the stretch by
  direction; read by the gradient's and the pull's contractions. OPEN: the reads' form, after G2.

### 4.5 The clicks (terms 11 and 12), G5

- **The whole click:** the drive's carry at the train's winding, q = E div w_c, the remainder kept. DERIVED, with M2's
  three questions OPEN (light's w_c = 0, a negative wind, the quantum per mode).
- **The split click:** the draw by a rank count over the parts' sizes (Born); the product draw over sigma_f sigma_b on
  the doubled Node-clock (the forward and the backward halves); a full slot refuses after the draw and the quantum goes
  back to its giver (decision 40 (b)). OPEN: the draw's fairness, and the doubled node's form on the act.

## 5. What is built, what is owed

- **Built (G0 to G1b, tensor24-review f80ccee4e):** terms 1 to 4 and 8, the run back by the mirror, every Node-clock in
  every round, the promise read from outside before every round.
- **Derived, owed in code:** the drive for every row (7), the tables' reading (4.2), the whole click's carry (11).
- **Open, by deriver:** David: 4.1 (the push, its self-push, its first-order form, the slicing), 4.2 (the legs, the
  strength, the vertices), 4.3 (the spring's place), 4.4 (the reads); Animate and David: 4.5 (the split click on the
  doubled node). Sofer reads each term against the law as it lands.

## 6. The order once closed

1. Every OPEN term derived, checked by Sofer against the law, and folded into this page.
2. The whole act built at once, every term with its law test and its mutant, one hostile reader on the whole node.
3. Then the loader (the families' rows, the tables, the coupling family's count), the runner and the decoder.
