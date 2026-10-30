# The Node-clock, closed: its whole act in one place

The owner's word to the Boss of 2026-10-30, 06:1x UTC (in Hebrew; in translation): "Why not close the node completely?
The rest is easier than it.." and "Yes. It is tensorial and algebraic, right..?". This page is the Node-clock's whole
act, every term in one round, before any more of it is built. For each term it says what it reads, how it is computed,
where it comes from, and whether it is BUILT, DERIVED (owed in code only) or OPEN (owed a derivation, by name). When
every term is DERIVED or BUILT, the node is built at once, with one hostile reader, and only then the loader, the runner
and the decoder catch up.

## 0. The Node-clock is atomic

The owner's words to David of 2026-10-30, 06:5x UTC (6516931362): one code, the same at every place; the board is
copies of it joined by Meshes.

- **In clocks:**
  - **its initialization, once:** it takes what it holds at the start, its gears' counts as the files lay the families,
    and derives the 24's operations from its own star (decision 42);
  - **its round, every tick:** its input, its six neighbours' counts through its six Meshes; the one act on its own
    state (section 3); its output, its own counts, which its neighbours read through their Meshes (it writes only its
    own state: line 92 (3), Locality), and its clicks, logged at it and read for the record from outside (line 92
    (5)). It holds no record, no round and no time (line 92 (4));
  - **no queue** (the owner's question to David, 07:2x UTC; 6517461101, with Sofer's clause, 6517481650): no
    Node-clock sends. Each round it reads its six neighbours' now counts through its Meshes, each Mesh read once from
    both ends, and every Node-clock steps in the one pass (the one pass is the engine's order of work and no law, line
    98). Different times are different counts: each clock's teeth set its rate, each Mesh's grip the speed through it.
    The round itself no act reads;
  - **around it, almost nothing:** joining Node-clocks by Meshes, and the promise read from outside before a round
    (line 92). The loader, the runner and the decoder come after.
- **In algebra:** the round is one tensor operation on arrays, at every Node-clock at once: the gather of the
  neighbours' counts (mesh.pull), the contraction of the readings through the plan (contract), and Rule3's carry
  elementwise (step.gear). The clicks are its outputs (terms 11 and 12).
- **No special code** (the owner's word to Sofer, 07:1x UTC; ALGEBRA.md line 90; the gate's SPECIAL, scribe-5
  d05351104): the slowing (term 2), the grips (term 3) and the sending and receiving (term 4) are the one act's own
  results. When a link lengthens or shortens and when a clock freezes is what that act gives on the metric's own gears,
  never a function, a key or a branch.

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
  weight through Rule3's carry only as a membership weight in what the start derives (kinds.turns, the square flag); in
  a round, a quotient that zeroes a term above a bound is a bound (line 106; Sofer, 6516548251).
- **Nothing declared:** no particle, mass, coupling or strength in a file (decision 35). The files lay families (kinds,
  parts, pairs), the board and the start.
- **The run back is exact** in its stated domain, by the act on the mirrored state (G1b (ii)).
- **Start from the simplest and close all three** (the owner's law (10), ALGEBRA.md line 35, in its form of 2026-10-30,
  09:1x UTC): each term is told by the clock or gear that makes it, by its algebra and by its physics, starting from
  the layer simplest for its question; the physics is always what the clicks read, never the board's numbers.

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
| 5 | the metric's push | every gear's four-vector here: its stride (a - b) and its gradient; the spring's part V here | each slot pushed by its component of 2T + 2 eta V: T each family's four-vector times itself through the 24's tables onto the square's ten slots, V the spring's part (term 6's potential); the trace reversal of the full stress S = T - eta (tr T / 2 + V), 2S - eta tr S, whole, with no trace term and no half (N3: the 00 slot by rho + 3p, each diagonal slot by rho - p); the metric's own gears in T (decision 40 (a)) | OPEN (G2): see 4.1 |
| 6 | the coupling vertex, and the gear's spring | the coupling family's gears and every other family's, here, and the unit | the one plan: each vertex a contraction of its legs through the 24's tables, pushing every leg, a term reading up to three readings with the unit for each it lacks; a held hand at its count pulls a gear back toward 0 inside its own Node-clock, D = g C n, the gear's own beat and its mass (decision 37) | BUILT the contraction (this push); OPEN (G3) the strengths and the plan: see 4.2 |
| 7 | the drive | J, the sources of 5 and 6 | q_d, r_d+ = carry(J, T_d, r_d): one drive for every row (decision 40 (d)) | DERIVED (G3) |
| 8 | the kick K | the drive's quotient | K = T_k s q_d; s = 1 | BUILT at T_k = 1 |
| 9 | the volume's notch | the metric family's own slots | the board's swing and its top (Postulate 4), the metric family's own; it pulls no other gear's count, so it gives no species a rest beat | OPEN (G2): see 4.3 |
| 10 | the shift and shears | the 0i and jk slots | read by the gradient's and the pull's contractions (frame dragging, waves) | OPEN (G4): see 4.4 |
| 11 | the whole click | the drive's carry of the swept area | q quanta click on the area the coupling moves in a round, summed over the train's rows through the A1 table, the key the teeth, the remainder kept in r_d: the record's how much and when | DERIVED (G5): see 4.5 |
| 12 | the split click | the parts' sizes sigma | the draw by a rank count over the sizes, after the carry whose quantum it places; a full slot refuses after the draw (decision 40 (b)) | OPEN (G5): see 4.5 |
| 13 | the frozen clock and the horizon | the teeth and the drive | a clock freezes where its teeth outgrow its drive and the carry never fires: no hold and no restore of its own | OPEN (G2): see 4.6 |

## 4. The open terms, each with its question and its deriver

### 4.1 The metric's push (term 5), G2: David derives, the Boss builds

- **The tensor:** for a family of kind K, each component x has its four-vector v_x = (the stride a_x - b_x, the
  gradient of a_x along each axis). T = sum over the families of C[K x K -> A1]_(x, y) v_x (x) v_y, symmetrised onto the
  square's ten slots: the same construction as kinds.square, read on the state (David, 6514906323, item 3).
- **The push:** each slot of the square gets its component of 2T + 2 eta V, T the outer product above and V the spring's
  part at the Node-clock (term 6's potential), at one strength per slot from the law. It is the trace reversal of the
  full stress S = T - eta (tr T / 2 + V): 2S - eta tr S = 2T + 2 eta V, whole (David, 6516715545, checked on 2,000
  four-vectors and springs). N3's numbers stand: a uniform swing with no spring, stride 7, gives the 00 slot 98 (rho +
  3p, rho = p) and each diagonal slot 0 (rho - p). "2T - eta T" with T the outer product, as this page first wrote it,
  gave 49 and 49, and is struck.
- **Postulate 6:** two sources' strides add bit for bit, and the rates compose by their product. The cross term
  c1 c2 / W0 comes from the metric's own gears in T (David, 6515406887); the test's mutant is the same act with the
  self-push off. OPEN: the self-push's exact form, and the order at which the cross term shows.
- **The run back (N2):** a push that reads the stride must run back. The matter steps first, so the metric reads its
  rates at both slots; a push that reads its own rate has no bijection. OPEN: the first-order form (each rate in its own
  slot), and with it the run back exact while the clock moves (G1's limit, the plan's G1 entry).
- **The slicing (N1):** the free count d_mu ((-g)^w g^(mu nu)) = 0 at w = 1/2, so the course and the static field agree
  with Cassini. w = 1/2 is the densitized slot form itself (decision 41): a conservation the act keeps and a test shows,
  not a term it adds (Sofer, 6516548251). OPEN: the test on the act.
- **The numbers** (the 2 of 2T + 2 eta V, w = 1/2): each comes out of the star or the pair, never typed and never from
  a file.

### 4.2 The coupling vertex (term 6), G3: David derives, the Boss builds

- **The one plan:** an ordinary coupling family, its leg in every source; each vertex pushes all its legs (energy kept).
- **What the Node-clock lacks to make a clock** (Animate, 6516545901, from Decoder4D2Clicks3D 1.4 and board2mass 3):
  - a beat of its own: a gear is pulled only sideways by its six neighbours (term 4), so it moves as light does. It
    becomes a clock, with a mass, only where a held hand inside its own Node-clock pulls it back toward 0, so that it
    swings even when its neighbours swing with it. That rest beat is its mass (decision 37);
  - the floor: the beat is the mass only for swings of about a count a round or more (board2mass 3.3);
  - to click, a second clock and the click on the act (4.5); to show a sharp mass, a life and a binding (G6).
- **The legs:** three-leg vertices alone hold no count (David's board2mass 3.6: a cubic form's stationary rays are flat,
  and the push drives the count below 0); a four-leg term bounds the whole potential, as nature's quartic. Decision
  40 (g)'s "an ordinary family" sets no number of legs, so the four-leg term is David's derivation and the Boss's; it
  goes to the owner only if that derivation reads 40 (g) otherwise.
- **The gear's spring as one operation** (Animate, 6516692018; CHECKED on the head's gear step in whole numbers,
  reader-5 61610aeee, ANIMATE-SPRING). At every Node-clock, every round, at the now slot, with x a family's gears there
  and k the coupling family's held count there:
  - contract: c = the sum over i, j of C[i, j -> kind(k)] x_i x_j, through the 24's table (the dot x . x for a T1 family
    and an A1 count);
  - push each gear: P_i = -g k x_i - lam c x_i, the spring and its bound; push the held count: Q = -(g / 2) c - kappa
    (k - n). P and Q are sources of the drive (term 7) and reach the step through the kick (term 8);
  - both are minus the derivatives of one potential, V = (g / 2) k c + (lam / 4) c c + (kappa / 2) (k - n)^2, so the
    vertex pushes every leg. The halves and quarters are the potential's form, not the act's: each x leg of the vertex
    pushes once, so the 2 of the derivative of a square comes from the vertex's two x legs, and no fraction enters.
  - DERIVED: with k at its steady count n, each gear beats by itself with D = g n, 4 sin^2 (omega0 / 2) = D / W, its
    mass (decision 37); the potential is bounded below exactly when lam is at or above g^2 / (2 kappa); through A1,
    (x . x)^2, a T1 family beats alike along an axis and off it, where the sum of x_i^4 the 24 also allow reads the
    board's axes.
  - CHECKED: the beat at 10^5 (a period of about 126 rounds); the runaway with no four-leg term and at half the bound,
    held at twice it over 4,000 rounds; and the board's limit, every spring far below W, since at 10^8 the local spring
    passes 4 W and the step beats no more. A clock needs both: lam at or above g^2 / (2 kappa), and every spring below
    W.
  - Read against the law (Sofer, 6516740454): no breach. The 2 and the 4 come from the table's symmetric double count,
    each leg pushed by the product of the others, never typed; the condition lam at or above g^2 / (2 kappa) is an
    inequality between the law's strengths, derived, never checked by a bound in the act (line 106); "every spring
    below W" is the integer step's domain, read by the runner from outside as a promise (line 92), never a bound in the
    act.
  - OPEN (G3, David): g, lam, kappa and n from the law (decision 35; decision 40 (g)); a hat of the held family itself,
    -(mu / 2) k k + (nu / 4) k^4, giving n and kappa from its two strengths; which families the one plan ties to k.
  - **G3 started** (David, 6517738078, with his readers' corrections, 6518149703; toys-5 f89b76a33). In clocks: n is
    how far the held hand stands wound, g how hard the hairspring pulls the gear per count of it, kappa how firmly the
    held hand is held at n; lam stands in the gear's push alone and holds no held hand. In algebra: the bound is
    DERIVED, lam at or above g^2 / (2 kappa) (at equality 8 kappa V = (2 kappa (k - n) + g c)^2 + 4 kappa g n c, never
    below 0); the value is CHOSEN, any whole lam at or above it, and the least, (g^2 + 2 kappa - 1) div (2 kappa), is
    a choice by minimality that owes its sentence (Sofer, 6517919800; line 100). n's total is the law's, one quantum
    per Node-clock, its unit in counts OPEN; g and kappa stay free. Through an A1 held count every family the plan ties
    to k gets the one spring g n; light and the metric family stay off k (tied, they would take the common mass), and
    what keeps them off without a row apart is OPEN. E read through its form G keeps the one spring g n and one energy.
    No ratio against nature's is claimed: a held count's parts sit where its own potential is least (decision 40 (h)).
  - **The ceiling beside the floor** (Animate's readers, 6518153643): the beat is the mass only while the push moves
    the held count far less than n. At twice the bound, laid at 10^7 and 2 x 10^7, the gear stays bounded but the held
    count falls below 0 and the beat is 95 and 206 sign changes in 4,000 rounds, not the mass's 64. A probe of the act
    gives the same numbers, the held count's least -3,112,715 and -8,012,335.
  - **BUILT in the act** (the owner's word to the Boss, 07:4x UTC: start implementing; and of 08:4x UTC: everything
    generic now). In clocks: each gear's hairspring, its stiffness the held count's, and a spring that stiffens as it
    winds. In algebra:
    - J's contraction reads up to three readings a term, a gather, a product of three and a scattered sum, and the
      readings gain the unit as their last row (engine/contract.py, step.sources, the Plan's third reading), so the
      gear's spring, the three-leg vertex and the four-leg term are the same term;
    - **the vertex law is the engine's own** (contract.pushes): the potential is a list of monomials, each a whole
      factor times four legs, the unit (-1) for each it lacks, and every leg that is a gear's is pushed by minus the
      factor times the other three, so each vertex pushes all its legs and keeps one energy. The loader lays the
      potential, empty until G3 (no strength typed or laid), and main.py makes it the plan.
    - The tests read the vertex law as a generic part (tests/test_the_tensor24_engine.py, on the owner's word of
      2026-10-30, 09:2x UTC: "what is generic, test only it, and then the whole"): J is minus the gradient of its
      potential on any monomials, its work on a displacement the potential's rate read exactly by the five-point
      stencil, and the unit read as 0, the third reading ignored or the push without its sign each break it. The
      formula law reads three readings, any of them the unit, against the naive model; the sources turn under the 24
      with a third reading on the cube; the run back holds through them. The spring's phenomena at chosen g, lam, kappa
      and n (the beat within a round of the exact recurrence, the runaway below the bound and the swing held at twice
      it, the 24's turn, the beat alike along an axis and off it) left the suite with tests/test_the_tensor24_spring.py
      at the test cut; they stand in git's history at 2c87a07ed, and a probe of the act gives Animate's numbers exactly
      (the runaway at rounds 49 and 29 with no four-leg term, 205 and 50 at half the bound).
- **The strength:** in the vertex law, read through the ruler, no file holding it (decision 35); no single integer serves
  all tables (David, 6501657960, item 5). OPEN.
- **The tables:** read in the square's basis where E stands, so E's ten oblique tables are never read (David,
  6516176163, item 4). BUILT (the node's initialization, on the owner's word of 08:4x UTC: everything generic now), with
  no seed, no search, no greatest common divisor and no branch:
  - **in clocks:** the 24 turns of the Node-clock's own star are summed once, and each product of two kinds' gears onto a
    third is the one pattern every turn leaves as it is;
  - **in algebra:** every channel's group sum S, rho_m(g) Psi_m x rho_i(g^-1)^T Phi_i x rho_k(g^-1)^T Phi_k, with Psi
    and Phi the two forms each kind's matrices keep (the sum of rho rho^T and of rho^T rho, the identity's multiple on
    the orthogonal kinds and E's form and its adjugate on E), is c u u^T, as David found with E's form (6516176163).
    c is the diagonal's entry that divides every other (every table of the 24 has an entry 1 in size, and none above 2), u is S's row
    there over c, and the table is u times the sign of its first entry not 0, by Rule3's sign test; all 125 channels
    at once in the axes' cube (runner/load.py, tables; engine/kinds.py, stacked), equal to the old seed-by-seed tables
    bit for bit on every channel. The gate's last 12 BLOCK-tier hits of the new engine (tables, primitive and common)
    are gone; its notes are the membership weights at the start (the zero test, the sign test, "not 0" by one carry).
- **The held count:** a family's components are read against no direction of the board, or the clicks see a turn change
  one species into another (David's G3 findings). OPEN: which vertices the one plan lays.

### 4.3 The volume's notch (term 9), G2

- The board's mean count swings and returns (Postulate 4): the metric family's own swing, its top the act's own turning
  point (OPEN 7). The metric's spin-2 part keeps it 0, so gravity's two polarizations stay massless. It is not the
  gear's spring (term 6): it pulls no other gear's count.
- Line 352 (D / W = 2 / Gamma) and line 35's spring clause are the old engine's, outdated by decisions 40 (e) and 41. The
  head's notch has no law sentence yet: a new rule, the owner's, when this term closes (Sofer, 6516548251).
- OPEN: its form in the slot form (decision 41).

### 4.4 The shift and shears (term 10), G4

- The 0i slots (T1) read as the lean of the now toward each neighbour, the jk slots (E + T2) as the stretch by
  direction; read by the gradient's and the pull's contractions. OPEN: the reads' form, after G2.

### 4.5 The clicks (terms 11 and 12), G5

- **The derivation:** the page David and Animate unite on the owner's word (Decoder4D2Clicks3D, Animate's, with David's
  board2mass), G5 first on his word to David: every species read as parts of clocks, which parts click alone and by
  which of the two clicks.
- **A click credits a train's whole winding, never one of its rows** (lines 468 and 1556, and the schema). A click that
  takes one row would be a new rule, the owner's (Sofer's recommendation: no, since it would end confinement). One drive
  for every row (term 7) does not by itself give that winding (Animate's readers, 6518153643): a T1 train has no linear
  invariant (its 24 matrices sum to 0), so its winding is an A1 contraction of its rows, quadratic for T1. DERIVED in
  form (David, 6518474832): the area the drive reads is the swept area summed over the train's rows through the A1
  table, the dot of T1 with T1 as term 6's c, one quadratic invariant; term 11's drive carries it once a round at the
  key, one carry for the train however many rows it has. Owed in code at G5.
- **The whole click** (David, 6516852295; CHECKED on the head's gear, toys-5 b107499b9): counted on a two-part hand's
  swept area, Omega = re p_im - im p_re, with p = W (a - b) + r each part's stride and kept tooth, the wind over the
  frequency, the step's own invariant. The drive reads the area the coupling moves in a round, its teeth the key, the
  same for every train and every mode: q, r_d+ = carry(the area moved, key, r_d). M2's three questions close:
  - light's winding is no longer 0: the key is every train's winding;
  - the quantum per mode: at equal wind Omega grows as 1 / omega, so a click carries the key times the mode's own beat,
    E = n h nu per mode;
  - a negative wind gives Omega of the other sign and a negative quotient, its kept tooth in [0, key), with no if:
    quanta of the other sense.
  - **Held in the clock, not OPEN** (David, 6517080622, probe c2, toys-5 1550bd31a; Sofer, 6517112674): each round
    Omega moves by exactly Delta q_re r_im - Delta q_im r_re, and over 20,000 rounds the sum of those terms equals
    Omega's change bit for bit; run back 20,000 rounds by the head's mirror, the whole state and Omega return bit for
    bit. So no swept area leaves the clock: what Omega misses is written in the kept teeth, and no law is added. What the
    coupling moves is term 6's vertex, so the click's last form follows it.
  - **The hold beside it** (Sofer, 6517127689): the final form keeps CK-S1 and The light no bob (line 148: a free
    light train is not credited by its own click; the count on Omega and the crossing's beat agree at a whole), else it
    is a new rule, the owner's. "Light's winding is no longer 0" stands as David's derivation only with this line.
- **Both clicks in one round** (the owner's question of 06:5x UTC, put to David, Animate and Sofer in 6516945354):
  yes in one round, for different trains: a whole click of one, a split click of another. A split is the same carry
  shared by twins, with no whole click before it: the carry is the event of both kinds, the kind is how many hold the
  winding when it completes, and a quantum is credited once, by one kind (line 35 (5); David, 6517080622; Sofer,
  6516993036 and 6517127689). Animate's answer from the record's lines is owed.
- **The split click:** the draw by a rank count over the parts' sizes (Born); the product draw over sigma_f sigma_b on
  the doubled Node-clock (the forward and the backward halves); a full slot refuses after the draw and the quantum goes
  back to its giver (decision 40 (b)). OPEN: the draw's fairness, and the doubled node's form on the act.

### 4.6 The frozen clock and the horizon (term 13), G2

- On the slot form (W = the rest + c, linear, no bound), a clock freezes where its teeth outgrow its drive and the carry
  never fires; the horizon is where that holds. Derived so, line 106's two clauses that still hold a bound, The horizon
  and BH-S1's hold and restore, are struck on that derivation (Sofer, 6516548251; decision 40 (a): horizons included).
- OPEN: the derivation on the act.

## 5. What is built, what is owed

- **Built (G0 to G1b, tensor24-review 68c7245ef):** terms 1 to 4 and 8, the run back by the mirror, every Node-clock in
  every round, the promise read from outside before every round; the Mesh unit 1, the grip den Gamma^2 (K-S1 on the
  new act). The Node-clock's code holds no gate hit at any tier.
- **Built at this push:** term 6's contraction of up to three readings with the unit (4.2), its strengths the
  tests' until G3.
- **Derived, owed in code:** the drive for every row (7), the tables' reading (4.2), the whole click's carry (11).
- **Open, by deriver:** David and Animate first: 4.5 (the clicks, on the owner's word to David). Then David: 4.1 (the
  push, its self-push, its first-order form, the slicing test), 4.2 (the legs, the strength, the vertices, the gear's
  spring), 4.3 (the volume's notch), 4.4 (the reads), 4.6 (the frozen clock). Sofer reads each term against the law as
  it lands (his reading of 07568c3b5: no breach, 6516548251).

## 6. The order once closed

1. Every OPEN term derived, checked by Sofer against the law, and folded into this page.
2. The whole act built at once, every term with its law test and its mutant, one hostile reader on the whole node.
3. Then the loader (the families' rows, the tables, the coupling family's count), the runner and the decoder.
