# ONELAW4: the cross terms' run back, where the mirror fails and what closes it

On writer F's 0ece4b19f (node-onelaw-f, on origin/node-onelaw 08c66fd40), extracted to onelaw4/f. Probes p1_gap.py,
p2_closure.py and p3_worlds.py, each run twice, with their .run1.txt and .run2.txt outputs byte for byte alike (p3's
progress in p3_progress.run1.log and .run2.log). Every probe uses whole numbers only, with Rule3's carry as the one
division. Each ran as python -I with the tree's src first, under nice -n 19, one process at a time, with
the load read first. Board readings are clock facts, never physics. Notation: senses = 2 (from the star). D = W(x) +
W(y) is an edge's dial. C(x) are the cross slots that the cross plan lands from the counts x, and C(x, y) = C(x) + C(y).
D_i is the centred difference and div is SUM_i D_i. tau is the mirror's parity: +1 on an even row, -1 on an odd one.

## 0. The answer first

- **No closure exists on the state as it stands, (a, b, r) per gear (DERIVED, section 2).** If one split per gear per
  round reads the next edge's dial and cross slots on the counts given first, then the run back is exact only when
  the round's net push is a function of the now slot alone (and of the rows given first). The joined act's cross
  terms are d_t(W b . D a) + d_i(W b^i d_t a). Written out, they are d_t(W b) . D a + [W b . D v + d_i(W b^i v)]. The
  bracket reads the value rows' velocity at the neighbours, so it cannot be carried exactly. F's gap is exactly this
  bracket (section 1).
- **The three candidates (section 3).**
  - The middle count on both edges and the split between the two edges come to one family, the pivot family. It is
    exact, but it carries d_t(W b) . D a alone, so at a uniform, constant shift it carries nothing.
  - No existing tooth can carry the bracket.
- **The closure needs one new element (section 4): the now slot's velocity u.**
  - It is one whole count per gear that the cross plan lands on, with no tooth.
  - It is carried by reflection, u+ = senses (a+ - a) - u.
  - It is mirrored by u -> tau (u - senses (a - b)).
  - Both edges read the cross term at the now slot's gradient, and the cross push reads u:
    Y = senses (C(a) . D u + div(C(a) u)).
  - The round is then a product of shears whose mirror is its inverse, and it carries all three cross terms,
    centred on the now slot.
  - MEASURED as a code check outside src:
    - the run back exact with the shift off 0, at 6 of 6 states for one round (wide counts) and on 3 of 3 drawn
      layouts over 100 rounds;
    - at a shift of 0, alike with F's act, state and clicks, at every round;
    - at a uniform shift, a velocity bump's centroid goes 20, 15, 10 over 100 rounds, as in F's act, while the
      pivot's stays at 20.
  - Sofer's rule: it is named for the owner's batch and not built. It is the same kind of element as HAT3's third
    count, but needs no second tooth.

## 1. Where the mirror fails (item 1)

1.1 The general round, as F built it (DERIVED). Take a value row with in-edge (b, a), tooth r, push P, and cross push
    Y(b, a). The kept momentum is M_in = senses D_in (a - b) - X_in(b, a) + r. Then N = M_in + Y + senses^2 P. The
    split is N + X_out(a, a+) = senses D_out (a+ - a) + r+. Rows 0 and 1 of the probes are given first, so on the
    mirrored state the next slot's cross slots are C(tau b) = -C(b). The mirrored round's split then lands at
    senses D_in (b - a) + (-1 - r) + m, with

        m = X_in(b, a) + X_out(tau a, tau b) - Y(b, a) - X_in(tau a+, tau a) - X_out(a, a+) + Y(tau a+, tau a).

    The run back is exact for every lawful state iff m = 0. Otherwise it returns the edge momentum
    Q = senses D (a - b) + r short by m, with the count a kept.
1.2 F's build reads X(x, y) = C(x, y) . D x, the gradient at the edge's first slot, and Y(x, y) = div(C(x, y)(y - x)).
    As C is odd, C(tau y, tau x) = -C(x, y), and

        m = Z(a, a+) - Z(b, a),   Z(x, y) = C(x, y) . D(y - x) + div(C(x, y) (y - x)).

    Without the cross push, m = C_out . D(a+ - a) - C_in . D(a - b). This is F's gap C_out . D(a+ - a), confirmed:
    it is the out-edge's share, and the in-edge gives its twin. Each edge's gap is that edge's own velocity read by its
    cross slots. At a uniform constant C, Z = senses C . D(y - x), which is the gyroscopic term, the bracket of
    section 0. DERIVED.
1.3 F's pivot (the gradient at the now slot on both edges) gives m = Y(tau a+, tau a) - Y(b, a), so it is exact
    without the cross push and not with it. DERIVED.
1.4 MEASURED (p1_gap, F's p_runback2 layouts: row 1 odd and read by the cross plan into rows 2 and 3, wide counts, one
    round). The measured Q defect equals the formula's m at every site, on 3 of 3 layouts, in each of the four cases.
    The run back is exact as follows:

    | case | run back exact | sites off of 120 |
    |---|---|---|
    | built, with the cross push | 0 of 3 | 120 |
    | built, without it | 0 of 3 | 120 |
    | pivot, with the cross push | 0 of 3 | 120 |
    | pivot, without it | 3 of 3 | 0 |
    | the cross plan emptied | 3 of 3 | (none) |

    F's finding is reproduced and its cause located. The miss is on every board with a shift whose velocity field
    varies; F's expectation holds (DERIVED from 1.2).

## 2. Why no closure exists on (a, b, r) (DERIVED)

2.1 Write the round as senses D_out (a+ - a) + r+ = senses D_in (a - b) + r + R, where R is the whole net push.
    Running the mirrored window through the same act gives one condition for an exact run back on every lawful
    state: R is time-even, R(b, a, a+) = R(tau a+, tau a, tau b).
2.2 R may read a+ only through the rows given first, since the row's own a+ is what the split makes. The condition
    swaps b and a+, so R may read the row's b, and its tooth, only through the rows given first too.
    - In full: let M be the in-edge's momentum, f(M) the push, and g the same push read on the mirrored state.
      Exactness needs f(M) = g(-1 - M - f(M)) for every whole M.
    - If f(M) = c + L M with L local, this forces (1 + L')(1 + L) = 1: two local integer operators, each the other's
      inverse.
    - The act is the same at a uniform shift, so they are translation invariant. The act is also the same on every
      board, so read them on the unbounded one: there the units of Z[Z^3] are only plus or minus a translation
      (Higman). So either L = 0 or the push moves every momentum by a whole site per round, which is a chosen
      strength.
    - Doing it shear by shear (integer lifting) needs the board parted into two sets, which is a mask.
    - So R reads no velocity of the row it pushes.
2.3 What remains: R = X_out(a, a+) + X_out(tau a, tau b) + psi(a), with psi(tau a) = psi(a).
    - With X_out linear in C, this is (C(a+) - C(b)) . U(a). The pivot is its member with U = D a.
    - In the measure, (C(a+) - C(b)) . D a is about 4 d_t(W b) . D a, the first cross term.
    - The bracket W b . D v + d_i(W b^i v) is first order in the shift and reads v, so 2.2 forbids it.
2.4 F's other two roads.
    - A mirror that reads the neighbours: the tooth -1 - r - C . D(a - b) makes the edge's momentum odd. But it
      leaves teeth outside their dial, and it still misses the cross push by Y(a, a+) - Y(b, a).
    - An implicit step: a linear solve across the board, which is not local and is a search.
    - Neither is lawful.

## 3. The candidates weighed (item 2)

- **The gradient read at the middle count in both edges.**
  - If the middle count is the round's (the now slot), this is the pivot. It is exact (1.3; MEASURED 3 of 3), but by
    2.3 it carries only d_t(W b) . D a, nothing at a uniform constant shift.
  - If it is each edge's own middle (D x + D y), the out-edge needs D a+ of the row being made. That is implicit, and
    a predictor breaks exactness by 2.2.
  - Not a closure of the joined act. DERIVED.
- **The cross term split between the two edges, each read the other's mirror.** This is the family of 2.3 with the
  same content: exact, but without the bracket. Not a closure. DERIVED.
- **The cross term on its own existing tooth.** None serves:
  - r is the momentum's remainder, and the split uses all of it;
  - r_d is 0 on every train, where T_d = 1, and giving it teeth there changes the drive;
  - k is the click's remainder.
  - A count held in a tooth would mix a tooth with a count (HAT3 section 3, the same finding). DERIVED.

## 4. The new element and the closure (items 2 and 3)

4.1 **What must be new, and why.** By 2.2 the net push must read an odd quantity attached to the now slot, and
    (a, b, r) holds none: the velocity at the now slot needs a+. So the element is the now slot's velocity u.
    - It is one whole count per gear that the cross plan lands on. Today the loader lays these as every row except
      the square's 00 and 0i rows.
    - It needs no tooth, because its law is exact in whole numbers:

        u+ = senses (a+ - a) - u     (so u_n + u_(n+1) = senses (a_(n+1) - a_n)).

    - Mirror: on an even row u -> u - senses (a - b), on an odd row u -> senses (a - b) - u, that is
      tau (u - senses (a - b)). It is its own inverse.
    - It is a third count per gear, as in HAT3, but needs no second tooth.
4.2 **The round, in F's own functions** (each step a shear):
    1. M_in = senses D_in (a - b) - C_in . D a + r, the in-edge read at the now slot's gradient (F's pivot);
    2. N = M_in + Y + senses^2 push, with Y = senses (C(a) . D u + div(C(a) u));
    3. N + C_out . D a = senses D_out (a+ - a) + r+, F's split as built, its dial and cross slots read on the counts
       given first;
    4. u+ by reflection.
    - Net: senses D_out (a+ - a) + r+ = senses D_in (a - b) + r + senses^2 push + (C(a+) - C(b)) . D a + Y.
    - In the measure 4 this is d_t(W b) . D a + W b . D v + d_i(W b^i v), all three cross terms, with the velocity
      read at the now slot.
4.3 **Why the run back is exact (DERIVED).**
    - On the mirrored state, u reads -u, so with C(tau a) = -C(a) the push Y is unchanged.
    - The pivot terms swap to (C(b) - C(a+)) with a minus sign, which is again (C(a+) - C(b)) . D a.
    - So the mirrored split lands at senses D_in (b - a) + (-1 - r) exactly.
    - Reflecting u twice returns it, and the mirror returns the start.
    - This holds for every lawful state, with no bound on u.
4.4 **MEASURED, a code check outside src (p2_closure).**
    - (A) One round, wide counts across 2**256, the shift off 0 (180 to 300 cross slots off 0): exact at 6 of 6, with
      u drawn wide and with u = a - b on each of 3 layouts.
    - (B) 100 rounds inside the step's window: exact on 3 of 3 layouts. Rests are drawn in [200, 400), grips in
      [1, 4), the shift row in [-16, 16) and the value rows within 2**20. The widest count is 22 bits at round 100,
      the least W is 200, and 285 to 342 cross slots are off 0 at round 100.
    - (C) The cross plan emptied: the closure's state and clicks are alike with F's act at every round. That holds on
      the engine test's drawn layouts (J cubed, the Mesh plan, the grips' read; 4 rounds, wide counts) and on 3
      windowed layouts over 100 rounds.
    - (D) A uniform constant shift on a 40-site ring (W = 1000, C = 50, no grips; a velocity bump of sum 4000). The
      bump's centroid over rounds 0, 50 and 100, and the run back over 100 rounds:

      | act | centroid at 0, 50, 100 | run back over 100 |
      |---|---|---|
      | the closure | 20, 15, 10 | exact |
      | F's act | 20, 15, 10 | not exact |
      | the pivot | 20, 20, 20 | exact |

      The derived drift is 2 C / W = 0.1 site per round. It is a clock fact on the board, and it separates the
      three: only the closure both carries the cross terms and runs back.
    - p3_worlds: the shipped worlds laid by their files, the closure (u laid as a - b) against F's act, the state
      (a, b, r, r_d, k) and the clicks at every round. Every cross slot was 0 in every round.
      - Our bang: 10 of 10 rounds alike.
      - The live world: 100 of 100 rounds alike.
      - The mesh world: 125 of 125 rounds alike, its 7592 clicks among them.
      - The well and click worlds: not reached inside a 7-minute cap at a load of about 6, with other probes on the
        machine. OWED.
      - They are alike by derivation: every added term multiplies a cross slot, and every cross slot is 0 there.
4.5 **OPEN, for the owner's batch with the element.**
    - The lay of u. No world lays a shift, so no world reads u today. A world that lays one must lay u with its
      counts. The reading u = a - b, the laid edge's own velocity, is a reading, not a number, but still a choice of
      lay.
    - The zigzag. u_n - v_n alternates, z_(n+1) = -z_n + O(v''), with an amplitude set by the lay (DERIVED). It is
      neutral, with |mu| = 1 while |beta| < 1. Here beta is the cross push's share of the dial for a mode,
      senses |C| sin k / D: a bound of the step's window, like ONELAW3 2.3, and not a number chosen.
    - The record's end digest reads the state, so a u field moves it unless u stands outside it: a build question.

## 5. What the closure does to J5, the units, the 24 and the books (item 4)

- **J5.** It keeps F's form, M_in and M_out = M_in + Y + senses^2 push, with M_in read at the now slot's gradient and
  Y the time-symmetric push.
  - Under the mirror, M_in -> -1 - M_out and M_out -> -1 - M_in.
  - Term 5's centred split negates both, since split(-1 - n) = -q (checked on paper), so hypothesis (d) is as before.
  - At b = 0 it is byte for byte (4.4 (C), the shipped worlds in p3). Its 00 term then reads W (v - b . D a) at the
    now slot.
  - The 0i slots stay pushed by nothing: the shift's own push stays OPEN, as F named it. DERIVED.
- **The units.** u is a count, laid as the counts are. Y and the pivot terms are linear in C, which scales with the
  teeth, so the act stays homogeneous of degree 1 in the factor (4A.1). That adds nothing to load.scaled, which the
  Boss has ruled cut from src. DERIVED, not run.
- **The 24.** A turn maps sites and axes, and C is a plane per axis turned as T1.
  - C(a) . D u and div(C(a) u) are scalars, and u turns as its row's counts, negated where the turn negates the
    row's counts, with the tooth rule (ONELAW3 2.1).
  - So the closure commutes with the 24 wherever F's act does. DERIVED, not run.
- **The books.**
  - The click pushes nothing into a, b, r, r_d or u.
  - The passing reads the value legs' plan on (b, a, a+), unchanged, and the per-edge books close by construction
    as before.
  - The cross terms' exchange with the 0i slots is booked by no click (OPEN, as F named it).
  - u enters no book. DERIVED.

## 6. DERIVED / MEASURED / OPEN

- **DERIVED:**
  - the defect formula m = Z(a, a+) - Z(b, a) and F's gap as its out-edge share;
  - the lemma of section 2: on (a, b, r), exact means a net push that reads no velocity, so the bracket cannot be
    carried;
  - the candidates reduced to the pivot family, and no existing tooth serving;
  - the element u, its law and mirror, and the closure's exactness;
  - J5's mirror, the units' homogeneity, the 24 and the books as stated.
- **MEASURED (code checks on F's tree, outside src; board clock facts):**
  - p1: the formula at every site in all four cases, 3 of 3 (two runs, byte for byte alike);
  - p2 (A) to (D) as in 4.4 (two runs, byte for byte alike);
  - p3: our bang, the live world and the mesh world alike at every round (the well and click worlds owed).
- **OPEN:**
  - the owner's answer on u (one count per gear the cross plan lands on);
  - u's lay and its zigzag;
  - the step's bound with the shift in both halves, with beta;
  - the shift's own push and the grips' W b b;
  - the record's digest with u;
  - the 24 and the units run on the closure;
  - p3 on the well world (128 rounds) and the click world (5000 rounds), owed to a quieter window;
  - every physics reading of the shift, owed to the click world.
