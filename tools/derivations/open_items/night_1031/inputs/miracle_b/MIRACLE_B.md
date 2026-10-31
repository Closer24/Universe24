# MIRACLE_B: road B, each edge's own dial, for the coupled families (NOT_CLOSED 37), on node-live 1794d474b

## Verdict first

- **Yes, for the round, in the gears as they are.** Road B gives an exact, time-symmetric step for the held and the
  tied families whose equation keeps a whole-polynomial energy exactly when nothing rounds. Each gear keeps its own now
  count, its before count and one tooth per edge: no third count, no second tooth, nothing doubled (the owner's
  "a node that goes both ways does not need double all the gear teeth").
- **The round (B-edge).**
  - First, every row not of the held train (the tied family T: the giver, the taker, and in the click world the wave
    and the metric) steps by the engine's own act, unchanged.
  - Then every held row steps on dials that are its edges' own:

    d = W(a) + W(a') + g_e,   g_e = SUM over the live monomials (f; r, r, o, o) of f o(start) o(end).

    g_e is the coefficient of the row's own square in the potential, with its two other legs read at the edge's two
    ends. For the in-edge these are the tied before and now counts; for the out-edge the tied now and next counts. The
    next counts are given, because the tied family stepped first.
  - The held push is -(g_in + g_out) a. The two pushes of each monomial's two held legs are read one on each of the
    row's two edges, in place of both at the now slot.
  - In one line: W (h+ - 2h + h-) = -[g_out (h + h+) + g_in (h- + h)] / 2. The held row moves by the mean of the
    difference quotients (g_e h'^2 - g_e h^2) / (h' - h) = g_e (h + h') of its own square over its two edges. That is
    the brief's candidate: whole, symmetric in each edge's two ends, no division.
  - The same round in a form that selects no row (every dial gains g, 0 off the held rows by its plan; every push
    J - J_g - (g_in + g_out) a) gives the run byte for byte.
- **It is acyclic.** No tied dial reads a held count; the held dials read only tied counts the round has already
  given.
- **Every edge's dial is its own.** It is one number written, read and mirrored, since g_e is symmetric in its two
  ends.
- **The run back is the engine's own.** From the end state alone: the engine's mirror, the same act N times, the
  mirror (the owner's seed test).
- **The 24 commute by structure.** g_e is the form's own contraction of the tied counts.
- **The energy.** Let 32 W E be

  E32 = SUM_held [16 W^2 (a - b)^2 + 16 W g_e (a^2 + b^2) + 4 g_e^2 (a + b)^2]
      + SUM_others 16 W^2 (a - b)^2 + 16 W SUM_(T's own monomials) f (o1(b) o2(a) + o1(a) o2(b))
      + 8 W SUM grip stretch(b) stretch(a),

  a whole polynomial in the state, g_e on the edge (b, a).
  - When nothing rounds, the round keeps E32 exactly (DERIVED, section 3.4).
  - In whole numbers, each round changes E32 by exactly the teeth's share:

    dE32 = SUM over all rows (s - s+) (4 W (a+ - b) + 2 g_out (a + a+) - 2 g_in (a + b)),   g = 0 off the held rows.

    MEASURED to the unit in every round of every run. No parametric term, no window term and no four-leg residual is
    left.
  - No polynomial energy is kept exactly by a slow gear whose count is the carry's quotient (a lemma, section 4.2;
    the coupled round's statement is OPEN as a written proof). So "exact in whole numbers" is not on road B. What the
    teeth create or lose is read exactly, round by round, by the identity.
- **The tie's four-leg residual (VARY3 B1, NOT_CLOSED 29) is gone on this round** (section 4.4).
  - Each monomial's exchange between its legs is exact and sums to 0 over them. In the passing's own units:
    - the tie's is 4 P, P = f k^2 o (o+ - o-). The held legs read it from their dial's change across the round's two
      edges, the tied legs from their force times their window;
    - the hands' tie's is f (C(b, a) + C(a, a+)), with C(u, v) = x(u) y(v) - x(v) y(u): the act's own two-leg form.
  - MEASURED: each clock's energy change equals its booked exchanges plus its own teeth's share at every clock and
    round: 0 misses of 3780 clock-rounds on the pair world, 0 of 3780 on the square-2 lay, and 0 of 25,000 at each
    of the click world's 27 Node-clocks (read on its one Node-clock, section 6.2).
  - The act's term 11 is still the two-leg form on the four-leg tie, and beside the exact exchange it leaves 225 keys
    at one clock over the pair world's run.
  - So on this round the passing to build for a four-leg monomial is the exchange P itself. That is OPEN for the
    writer and David, not built.
- **Measured (board clock facts, python3 -I, one process at a time, every run twice byte for byte alike):**
  - **The shipped pair world:** 1260 of 1260 rounds, no count past the width, the counts within 6 bits. Beside it:
    the engine falls at 766, road (a') at 531, and HAT2 holds 3 to 5 bits with its run back failing at 188.
    - The identity holds in 1260 of 1260 rounds.
    - The run back from the end state alone is exact over 1260 rounds.
    - The 24 are alike in 24 of 24 turns over 100 rounds.
    - The board is alike in 1260 of 1260 rounds for the hidden twin (one click unit apart at one clock).
  - **The shipped click world:** 5000 of 5000 rounds, past the engine's 3752 (5 bits at round 3750, 5 at 4000), no
    count past the width, the counts within 7 bits.
    - The identity holds in 5000 of 5000 rounds.
    - The run back from the end state alone is exact over 5000 rounds.
    - The 24 are alike in 24 of 24 turns over 8 rounds.
    - The two runs are byte for byte alike (38 minutes each, under the machine's load).
  - **The square-2 lay** (S/nc29/pair2; read beside STOP1's stop, not counted for or against the step): 1260 of 1260
    rounds within 5 bits, the run back exact. Beside it: the engine runs away at 1195, and HAT2's dg falls along
    x_g = -x_t to 50 bits.
- **Plainly, the coordinator's question.** Does a staggered order of the families make the edge's own dial acyclic
  with the gears as they are?
  - **A stagger in time** (the families on alternate half rounds) is acyclic, and its dials are the edges' own. But it
    cannot run back by the engine's mirror, because the mirror reverses which family leads (the centering lemma,
    section 2). MEASURED on the pair world: not exact over 1, 2, 5 or 1260 rounds.
    - It runs back only under a mirror that also takes the held family's step, M_s = M after P (MEASURED exact over 1,
      2, 5 and 1260 rounds), or with HAT3's third count.
    - Its energy is not kept even when nothing rounds, because the hands' tie sits inside the tied family's implicit
      step.
  - **A stagger in the order of the act, inside one round** (the tied first, the held second, both families on the
    same two slots) is acyclic with the gears as they are. Its edges' dials are their own, it runs back by the
    engine's mirror, and it keeps E32 when nothing rounds. That is the B-edge round.
    - It is the leapfrog's structure turned on the families: each held edge's far end is given when the edge is split.
    - It is also the engine's own rule for its 00 row ("the 00 row's own carry, given first"), extended to the tied
      rows, whose dials read no held row.
- **What it costs, and where it fails.**
  - **(1) The tied window.** The tied family's coupling curvature, 2 c |k|^2, stays explicit. Its window
    2 c |k|^2 < 4W is held by the motion, not by construction.
    - Largest readings: 24 permille of 4W on the pair world, 45 on the click world.
    - The held hand heats by the teeth's share: from one count to about 30 by round 5000 on the click world.
  - **(2) The held dial's sign.** g_e = spring + c t . t' is a polarized product. It falls below 0 where the tied counts
    change sign across one edge at a large size, and the dial W(a) + W(a') + g_e must stay at least 1 for Rule3's
    carry.
    - It is held by the motion. Smallest readings: 13,096,000 (545 permille of 4W, round 873) on the pair world,
      and 1,299,940,000 (541 permille of 4W, round 1405) on the click world.
  - **(3) Past the pair world's ticks** (a probe asked for 20000 rounds):
    - the files' open direction falls from about round 1640, the held hand still at one count, so |k|^2 is below the
      open region's 0.8 on average;
    - the giver's first row swings through 0 at 40 to 62 counts, and the held dial falls below 1 at round 1903;
    - the counts pass the width after round 1917.
    - The first is the files' (STOP1's stop). The second is the step's, and it follows the first.
- **HAT4's three-property claim is refuted.** HAT4 said "an exact run back by the same act, a dial that is the edge's
  own, and an acyclic read cannot all be had at once for two coupled families". That holds only when both families'
  dials carry the coupling's curvature; here only the held family's does.
  - Road (a') of HAT1 already had all three. Its reads were acyclic, its run back was exact, and its dial (the
    curvature at both of the edge's ends) was the edge's own.
  - What it lacked was the push: it read the curvature at the middle count, so its energy was not kept and the tied
    rows' window broke at 531.
  - B-edge is (a') with the dial polarized over the tied edge and the push read on the two edges.
- **The other ways.**
  - (i), the true stagger: measured and refused (above, section 2).
  - (ii), the palindrome with the difference quotient: it keeps the energy exactly when nothing rounds only if the
    tied family is split again (the giver and the taker as two families). It needs the half-stepped families' third
    counts for the engine's mirror (the centering lemma), and the owner's note sets those aside. It is not needed.
  - (iii), the books: the identity above is the energy's exact book, round by round, from the teeth alone, and section
    4.4's exchanges are each monomial's. Keeping the teeth's share as state would need a new tooth per gear, which is
    set aside (section 4.3).

## 0. The forms side by side (pair and click: the shipped worlds)

| form | state per gear | reads acyclic | each edge's dial its own | run back by the engine's mirror | energy, when nothing rounds | pair world | click world |
|---|---|---|---|---|---|---|---|
| the engine as built | a, b, one tooth | yes | yes (W alone) | exact | not kept: the tie's four-leg residual R (CONF1) | falls at 766 (the held window) | falls at 3752 |
| road (a'), HAT1 | a, b, one tooth | yes | yes | exact | not kept | falls at 531 | 5000 of 5000 |
| HAT2 (dg) | a, b, one tooth | yes | no: the round's | fails at round 188 | kept | 1260, 3 to 5 bits | 5000, at most 8 bits |
| HAT3's palindrome | a triple and two teeth on T | yes | yes | exact | not kept | 1260, 25 bits at 1250 | 3900 read, 35 bits at 3750 |
| the true stagger (way i) | a, b, one tooth | yes | yes, at midpoints | not exact over 1 round; exact by M_s | not kept: the hands' tie inside T's implicit step | 1260, at most 7 bits | not run |
| B-edge (this text) | a, b, one tooth | yes | yes, at both ends | exact | kept: E32 | 1260, at most 6 bits | 5000, at most 7 bits |

The rows other than this text's are HAT1, HAT2 and HAT3's own figures (node-live 1919dd64c, whose step.py is
1794d474b's).

## 1. The edge's rule, in the engine's terms

- **The gear.** n = 2 D_in (a - b) + 4 push + s, split at 2 D_out: n = 2 D_out q + s+ with -D_out <= s+ < D_out, then
  a+ = a + q and b+ = a (step.gear, step.split).
  - The tooth s lives on the edge (b, a). It is written as the out-edge's tooth of one round and read as the in-edge's
    of the next. The mirror (b, a, -1 - s) on an even row reads it again on the same dial.
  - So a dial is lawful only if it is the edge's own: one number for the edge, the same when written, when read and
    when mirrored. Otherwise a tooth written in [-D, D) is read in another interval and the mirrored split cannot
    return it (HAT2 section 3: the run back failed at round 188).
- **The edge's own dial from its two ends.** For a row r whose potential is g(t) r^2, the coefficient g read from the
  other family t:
  - the difference quotient over the edge (r, r'), (g r'^2 - g r^2) / (r' - r) = g (r + r'), is whole and symmetric;
  - but g must be read at a time that belongs to the edge.
  - With both families on the same two slots, the edge (h_n, h_(n+1)) has two ends at n and n + 1. A symmetric read
    takes t at both ends, so t_(n+1) must be given when h's out-edge is split.
  - If the tied family's dial also reads h at both ends, h_(n+1) must be given when t's out-edge is split: the cycle
    HAT2 and HAT4 found.
  - The cycle breaks only if one family's dial reads nothing of the other. Section 3 takes the tied family's.

## 2. Way (i): a stagger in time, and the centering lemma

- **The true stagger.**
  - The state holds the held family H at the times (n - 1, n) and the tied family T at (n - 1/2, n + 1/2).
  - The round is Q after P.
    - P is H's step. Its in-edge's dial reads T's before slot, the edge's midpoint n - 1/2; its out-edge's reads T's
      now slot, n + 1/2. The push is -(g_in + g_out) h.
    - Q is T's step. Its in-edge's dial reads H's before slot after P, the midpoint n; its out-edge's reads H's now
      slot, n + 1. Its push is -(g_T,in + g_T,out) t, plus T's own monomials and the Meshes at T's now slot.
  - Forward, every read is acyclic and every edge's dial is its own, read at the edge's midpoint.
- **The centering lemma (DERIVED).** With two slots per gear, the same act runs the mirrored state back only if every
  gear's two slots share one centre in the motion's time.
  - The engine's mirror sends each gear's (before, now) to (now, before). As times, a family centred at tau goes to
    one centred at 2c - tau, so an offset delta between two families' centres goes to -delta.
  - The act reads a family by slot role, for example the tied now slot for the held out-edge. It reads the same times
    in both directions only if delta = -delta, that is delta = 0.
  - In the true stagger delta = 1/2: the tied family leads. Mirrored, it trails by 1/2.
    - P on the mirrored state reads, for the held in-edge (h_n, h_(n-1)), the tied before slot t_(n+1/2).
    - That edge's midpoint is at n - 1/2: P misreads by one round.
  - HAT3's centred triple is this lemma's cure: the half-stepped family's three counts are centred with the held
    family's two.
- **Its own mirror (DERIVED).** P and Q are each the gear's split on dials read at the other family's two slots, with
  pushes symmetric in those slots. So M P M = P^-1 and M Q M = Q^-1, M the engine's mirror. Then:
  - M_s := M after P is an involution: M P M P = P^-1 P = 1;
  - and M_s (Q P) M_s = (M P M)(M Q M)(M P M) P = P^-1 Q^-1 = (Q P)^-1.
  - So the true stagger runs back exactly by the same act on the state mirrored by M_s.
  - Equivalently, M (P Q)^N M: the engine's mirror with the round's halves in the other order.
  - Either the mirror holds the held family's step, or the act changes. The engine's mirror alone does not serve.
- **Its energy (DERIVED): not kept even when nothing rounds.** T's own potential holds the hands' tie, x_g . x_t,
  between two of its rows. Inside T's implicit step it stays explicit, since making it implicit would read the
  other row's next count, a cycle within T. The node momentum's two readings then differ by 4 J_tie, and the round
  changes E by J_tie . (kappa_out (t + t+) - kappa_in (t- + t)) / (8 W) beside the teeth's share. It is kept exactly
  only where each family's potential, given the other, is its own square's coefficient alone (not these worlds).
- **Its 24 and its state.** Its dials read the form's dot products at the midpoints, so it commutes with the 24 by
  structure, as B-edge does (not measured here). It needs no new element, but its mirror M_s computes the held
  family's step.
- **Measured (stagger.py, the pair world, 1260 rounds; rec/stagger_pair_1.txt and _2.txt, alike):**

| reading | the true stagger |
|---|---|
| forward | 1260 rounds, the widest count 7 bits |
| the run back by the engine's mirror (M, the round N times, M) | not exact over 1, 2, 5 and 1260 rounds |
| the run back by the stagger's own mirror M_s = M after P | exact over 1, 2, 5 and 1260 rounds |
| M_s M_s = 1 | on the lay and on the end state |

## 3. Way (iv): the stagger in the act's order, the tied first (B-edge)

### 3.1 The worlds' potential, read by the structure

- **Families:** H is the held train's rows, found by the loader's character flag; T is every other row.
- **Why the held family takes the dial and the others step first, by the structure.**
  - The held hand is the board's one Mesh-less train (its grips are 0, a site-local oscillator), so an implicit dial
    on it reads only its own Node-clock.
  - Every gripped train (the tied hands, the board's wave, the metric) is pulled by its neighbours' now counts. An
    implicit dial there would read, for its Mesh, the neighbours' next counts (a cycle across the board), and, for
    its tie, the held next counts (the cycle of HAT2 and HAT4).
  - So the gripped trains step first, explicitly, as the engine steps them. The held train, whose curvature is the
    one that leaves the engine's window (NOT_CLOSED 37, CONF1), steps second on its edges' own dials.
- **Every live monomial is one of two kinds** (b_edge.py stops by name otherwise):
  - **(a) the held row twice.** Its two other legs are alike: one tied row or the unit. These are the held spring
    (spring; r, r, 1, 1) and the tie (hold f C_yy; x_y, x_y, k_r, k_r). Write g_r(t) = SUM f o(t)^2, the coefficient
    of the row's own square.
  - **(b) on T alone, with at most two tied legs:** the hands' tie (tie C; x_g, x_t, 1, 1).
- **Beside them,** the Meshes' pull on T is linear with grips that do not move (the ii slots stay 0), and the held rows
  hold no grip.
- **The metric's push and the gradient vertex are at factor 0** in both worlds (asserted). The held rows' push as the
  engine reads it is -2 g(a, a) a (asserted at the lay and at the end).
- **So V = SUM_r g_r(t) h_r^2 + V_T(t),** with V_T at most quadratic and of constant coefficients. On the pair world:
  V = 10^6 |k|^2 + 6000 |k|^2 (|x_g|^2 + |x_t|^2) + 9600 x_g . x_t, with W = 6 10^6 (CONF1 section 1). On the click
  world: 10^8, 60000 and 96000, with W = 6 10^8.

### 3.2 The round in the engine's terms

- **T's step,** for every row not held: the engine's own gear, n = 2 D (a - b) + 4 push + s, with
  D_out = W(a) + W(a') and its push s F + K at the now slot. It reads the held now slot and nothing of the held next.
- **H's step,** for every held row:
  - d_in = W(b) + W(a) + g(t_b, t_a) and d_out = W(a) + W(a') + g(t_a, t_a'), where g(x, y) = SUM f o(x) o(y) and t_a'
    is T's next count from T's step;
  - push = -(g(t_b, t_a) + g(t_a, t_a')) h_a;
  - the gear's own split: n = 2 d_in (a - b) + 4 push + s, split at 2 d_out.
- **The same round with no row selected** (b_edge.py's uniform act, byte for byte alike):
  - every row's in- and out-dial gains g on that edge, 0 off the held rows by the plan;
  - every row's push is J - J_g - (g(b, a) + g(a, a')) a.
    - J_g is the held-twice monomials' pushes on their held legs, by the vertex law, a plan laid once.
    - So each such monomial's two held legs are read one on each of the row's two edges, instead of both at the now
      slot. No 2 is typed.
  - a' is the count the split gives at the engine's own dials, exact for every row whose dial reads no held row. That
    is the engine's own pattern for its 00 row ("the count the split gives at the edge's own dial: the 00 row's, whose
    teeth read no row, so its dial is its own").
- **In the potential's own terms:** W (h+ - 2h + h-) = -[g_out (h + h+) + g_in (h- + h)] / 2.
  - The held row moves by the mean of its two edges' difference quotients, g_e (h + h') = (g_e h'^2 - g_e h^2) / (h'
    - h).
  - The tied rows move by the difference quotient of the polarized coupling over their window:
    (o_n o_(n+1) - o_(n-1) o_n) / (o_(n+1) - o_(n-1)) = o_n, the explicit force at the now slot.

### 3.3 Acyclic, the edge's own, the run back (DERIVED)

- **Acyclic.**
  - T's dials read the 00 row's next count, a tied row, and no held count. T's pushes read only the now slot.
  - H's dials read only T's before, now and next counts, all given before H is split.
- **The edge's own.**
  - The held edge (h_(n-1), h_n) is written in round n - 1 on g(t_(n-1), t_n). It is read in round n as the in-edge
    on g(T's before, T's now) = g(t_(n-1), t_n).
  - The mirror reads it on g(t_n, t_(n-1)), the same number, since g is symmetric (each monomial's two other legs are
    alike; asserted).
- **The run back by the engine's mirror.** The round from (h_(n-1), h_n; t_(n-1), t_n) gives (h_n, h_(n+1); t_n,
  t_(n+1)). Mirror it to (h_(n+1), h_n; t_(n+1), t_n), as (before, now), and run the same act:
  - T's step reads the held now slot h_n, as T's forward step did, and the engine's own mirror theorem returns
    t_(n-1) with its tooth;
  - H's in-edge is split on g(t_(n+1), t_n), the forward out-edge's dial, and its out-edge on g(t_n, t_(n-1)), the
    forward in-edge's;
  - its push -(g(t_(n+1), t_n) + g(t_n, t_(n-1))) h_n is the forward push, symmetric under before <-> next. The gear's
    own mirror law then returns h_(n-1) with its tooth.
  - The drive's fine tooth stays at 0 on the force's path (T_d = 1, asserted). The click tooth runs back as the
    engine's: the passing is odd under the window's reversal and pushes nothing into the gears.

### 3.4 The energy the step's equation keeps (DERIVED; the identity MEASURED)

- **The held edge's energy:** E_H(h, h'; g) = W (h' - h)^2 / 2 + g (h^2 + h'^2) / 2 + g^2 (h + h')^2 / (8 W).
  - By algebra alone it equals p^2 / (2W) + g h^2 at the start end, with p = W (h' - h) + g (h + h') / 2.
  - At the end end it equals p'^2 / (2W) + g h'^2, with p' = W (h' - h) - g (h + h') / 2.
- **The held step is the agreement of the node momentum's two readings.**
  - With no teeth, the held equation is exactly W (h_(n+1) - h_n) + g_out (h_n + h_(n+1)) / 2 = W (h_n - h_(n-1)) -
    g_in (h_(n-1) + h_n) / 2.
  - So E_H(out-edge) - E_H(in-edge) = (g_out - g_in) h_n^2.
- **The tied step is the leapfrog.**
  - With no teeth, W (t_(n+1) - 2 t_n + t_(n-1)) = J_T, and the tied kinetic W |t' - t|^2 / 2 changes by
    J_T . (t_(n+1) - t_(n-1)) / 2.
  - The coupling's part of J_T on a tied row o is -2 SUM_r f h_r,n^2 o_n. Its work is
    -SUM_r h_r,n^2 SUM f o_n (o_(n+1) - o_(n-1)) = -SUM_r (g_out - g_in) h_r,n^2.
  - That cancels the held change exactly.
  - The rest of J_T is linear with constant coefficients (the hands' tie, the Meshes). Its work is the change of their
    polarized edge potential, as for any leapfrog.
- **So E = SUM_held E_H(edge) + SUM_others W |a - b|^2 / 2 + V_T(b, a) polarized + the Meshes polarized is kept when
  nothing rounds.** E32 = 32 W E is whole (its formula in the verdict).
- **It is not definite where the files' tie opens it.** c (t . t') (h^2 + h'^2) against tie x_g . x_t, |k|^2 < 0.8:
  that is the files' open direction (HAT2 section 4; CONF1), not the step's.

### 3.5 The 24 (DERIVED; MEASURED in section 6)

- g_e is the form's own contraction of the tied counts (the dot product for T1 and T2 through the table onto A1).
  Every turn moves the tied components by a signed permutation, which keeps it.
- The held rows are A1 and A2, each multiplied by its character, +1 or -1, and the held push is linear in h.
- So the round commutes with the 24, as the engine's does. No row's dial differs by frame, since the tie's
  off-diagonal entries are at factor 0 (as in HAT2).

### 3.6 The state it needs

- **None new:** each gear's now, before, its edge's tooth, the drive's fine tooth (at 0) and each train's click tooth,
  as laid.
- The held rows read, at their own Node-clock, the tied rows' before, now and next counts. The next counts are the
  round's own, given first, as every row's teeth read the 00 row's next count today.
- No number is typed: g is the potential's own monomials, read at two slots in place of one.

### 3.7 The laws, line by line

- Whole numbers. The split's carry is the one division (step.gear, and the click's carry).
- No if, mask or bound. The uniform act selects no row; g is 0 off the held rows by its plan. There is no cap.
- No number beyond 0 and 1, and no two spelt as a sum. The held push's two terms are the monomial's two held legs, one
  per edge.
- No sign test or indicator quotient.
- Locality: one Node-clock's own gears.
- The run back is the engine's mirror and the same act, and the 24 act on everything.
- No chosen strength: the dial reads the files' spring and hold f C as laid.
- No light or matter: the families are clock trains, named by their characters.

## 4. The energy in whole numbers

### 4.1 The exact identity: the teeth's share (DERIVED; MEASURED in every round)

- With teeth, the held equation gains (s - s+) on its right side, (4W + 2 g_out) dh+ = (4W + 2 g_in) dh- -
  4 (g_in + g_out) h + (s - s+). So the node momentum's two readings differ by exactly 4 p - 4 p' = s - s+.
- E_H(out) - E_H(in) = (p - p')(p + p') / (2W) + (g_out - g_in) h^2, with
  4 (p + p') = 4 W (h+ - h-) + 2 g_out (h + h+) - 2 g_in (h- + h).
- The tied rows have the same form with g = 0: their kinetic gains (s - s+)(t+ - t-) / 8.
- Every term that is not a tooth's cancels as in section 3.4. Hence, over each round:

  E32(after) - E32(before) = SUM over rows and Node-clocks (s - s+) (4 W (a+ - b) + 2 g_out (a + a+) - 2 g_in (a + b)).

- **What it says.** The whole change is the teeth's: the momentum's fraction moved from one edge's tooth to the next,
  times the node's momentum. No parametric term (the coupling) and no window term are left.
- **Its size.** For a gear moving about one count a round it is of the order of its energy itself, since s / (2D) is
  the count's own rounding, up to half a count. CONF1 saw the same share keep the engine's held hand away from 0.

### 4.2 No polynomial is kept exactly by a carry-quotient count (a lemma, DERIVED for a slow gear)

- **The lemma.** Take one gear of the engine's form with a constant dial D and a linear force:
  n = 2 D (a - b) + s - 4 kappa a, q = floor((n + D) / (2D)), (a, b, s) -> (a + q, a, n - 2 D q), kappa >= 1.
  If a polynomial E(a, b, s) of degree m, with 8 kappa (m + 1) <= D, is kept by every round, E is a constant.
- **The proof.**
  - Read the state by its count a and its edge's momentum M = 2 D (a - b) + s. On the strip q(M) = j, which holds 2D
    consecutive M, E reads F_j(a, M) = E(a, a - j, M - 2 D j), a polynomial. The round maps (a, M) to
    (a + q(M - 4 kappa a), M - 4 kappa a).
  - (1) Take |a| <= D / (8 kappa) and M in the middle half of strip j. Then M - 4 kappa a stays in strip j, so
    F_j(a + j, M - 4 kappa a) = F_j(a, M) on a grid of more than m by more than m points. A polynomial of degree m
    that vanishes on such a grid vanishes, so the identity holds everywhere.
  - (2) Take M in [2Dj + D/2, 2Dj + 3D/4) and a in [-D / (2 kappa), -D / (8 kappa)]. Then M - 4 kappa a lies in
    strip j + 1, and on that grid F_(j+1)(a + j + 1, M - 4 kappa a) = F_j(a, M), again everywhere.
  - (3) Together these give E(A + 1, B, S - 2D) = E(A, B, S) wherever A - B = j. Since j is any strip, that is on all
    of Z^3, so it holds as polynomials. So E depends on its count and tooth only through the momentum:
    E(a, b, s) = G(b, 2D (a - b) + s).
  - (4) Then (1) reads G(a, M - 4 kappa a) = G(a - j, M) for every j. So G does not depend on its first argument,
    and G(M - 4 kappa a) = G(M) makes it constant.
- **What it covers.**
  - It covers a slow gear alone. A tied row at the lay is one: its force per count, 2 c |k|^2 + tie, is about 2 10^4
    against D = 1.2 10^7 on the pair world, so no polynomial of degree below about 70 is kept.
  - For the coupled round, the same strip argument branch by branch is OPEN as a written proof.
  - The held rows are stiff (2 g / 4W about 0.1 to 1), so the grids are too short: for them it is not derived.
  - MEASURED: E32 moves in the first rounds on both worlds, by exactly the teeth's share.
  - So in whole numbers the carry-quotient count leaves no exactly kept polynomial energy, DERIVED for a slow gear.
  - An exact whole-number invariant needs the counts to carry the motion with no rounding of the count, as an
    integrable map's own recurrence does (road A's question). It is not on road B.

### 4.3 Way (iii): the energy's books on the teeth

- The identity of 4.1 is the energy's exact book, read from the teeth and the counts alone, round by round:
  E32 + SUM of the teeth's shares = E32 at the lay. MEASURED to the unit in every round.
- Under the run back the shares are negated and the book returns to 0 at the start seed. This is the same act on the
  mirrored state: each share is odd under the window's reversal.
- **Keeping it as state** would need one more tooth per gear (a carry of the share at some key, the remainder kept),
  which the owner's note sets aside.
  - Kept that way, it would act on nothing: a book in the Node-clock.
  - Making it act, the hands answering to the books, would return a whole share by the momentum. A carry returns a
    share only to within a tooth, so the book would not close. OPEN, not built.

### 4.4 The tie's four-leg monomial: each monomial's passing exact on this round (VARY3 B1, NOT_CLOSED 29)

- **The residual on the engine's round.** The act's passing is the two-leg form, X(x, y) = SUM entry (x_one J_two(y) -
  y_one J_two(x)). On a four-leg monomial it sums over the legs to -f (e1 - e3) (David's NOT_CLOSED 29).
  - CONF1 showed it is also the engine's own energy books' residual, R_m = f (e1_m(b; a) - e1_m(a; b)).
  - The leapfrog's polarized energy is kept on two-leg monomials alone; on the tie, f x^2 k^2, R_m is left.
- **On B-edge it is not there (DERIVED).** Section 3.4's energy balance is per monomial:
  - The tie (f; o, o, k, k) changes its held leg's edge energy by (g_out - g_in) k^2 = f k_n^2 o_n (o_(n+1) - o_(n-1)).
  - It changes its tied leg's by J_o (o_(n+1) - o_(n-1)) / 2 = -f k_n^2 o_n (o_(n+1) - o_(n-1)).
  - Call it P. It is whole, it is received by one side and given by the other, and it sums to 0 over the legs. The
    held side reads it off its dial (the coefficient's change across the round's two edges, times its square), the
    tied side off its force at the now slot times its window.
  - The two-leg monomials (the hands' tie f x . y) exchange (f / 4)(C(b, a) + C(a, a+)) in E's units, with
    C(u, v) = x(u) y(v) - x(v) y(u) and each one's polarized potential split half to each leg. In the passing's units
    that is f (C(b, a) + C(a, a+)), exactly the act's own two-leg passing.
  - So each clock's energy (its rows' kinetic, the held rows' whole edge energy, half of each two-leg polarized
    potential) changes each round by its booked exchanges plus its own teeth's share. There is no residual, and no
    share of one by legs.
  - In the passing's units (E32 = 8 W S), the tie's exchange is 4 f k^2 o (o+ - o-).
- **MEASURED (b_edge.py books):**

| world (rounds) | clock-rounds with energy change not equal to booked + teeth's share | Node-clock-rounds where the exact exchanges do not sum to 0 over the legs | the act's two-leg passing beside the exact exchange: running residual at one clock | its sum over the trains at one Node-clock in one round |
|---|---|---|---|---|
| pair (1260) | 0 of 3780 | 0 | 138,636,000: 225 keys of 614,401 | 109,392,000 |
| square-2 (1260) | 0 of 3780 | 0 | 63,192,000: 102 keys | 60,312,000 |
| click, each Node-clock (5000) | 0 of 25,000 | 0 | 129,324,000,000: 2545 keys of 50,811,429 | 80,269,320,000 |

- **The reading that can fail is the first column.** It compares each clock's energy, read from the board's counts,
  with the booked exchanges and the identity's teeth's share. The second column holds by construction (P given is P
  received), stated as a check.
- **What it closes and what it does not.**
  - On B-edge, the tie's exchange is an exact whole number per round, carried from the tied legs to the held legs, and
    every clock's energy is its exchanges plus its own teeth's share.
  - The act's term 11, built on the two-leg form, does not carry P. Read beside it, its residual grows past the keys
    (225 keys at one clock in 1260 rounds on the pair world).
  - To close NOT_CLOSED 29 on this round, term 11's passing for a four-leg monomial is P (in the passing's units,
    4 f k_n^2 o_n (o_(n+1) - o_(n-1))), on the same window as today's passing and odd under its reversal (b <-> a+
    negates it).
  - The teeth's share is the gear's own, not an exchange: what the integer step creates or loses at one clock.
  - OPEN, not built: the passing's form for the writer and David, and its key's units (KEY3).

## 5. Way (ii): the palindrome with the difference quotient

- **The composition.** Let each sub-step be the exact discrete gradient of its family with the other frozen: the row's
  own square's difference quotient in its dial, its push the two edges' sum.
  - Then the palindrome T(1/2) H(1) T(1/2) keeps the energy exactly when nothing rounds, if each frozen family's
    potential is its own square's coefficient alone.
  - The tied family's is not: the hands' tie couples the giver with the taker, and inside T's implicit half step it is
    explicit, with the error of section 2.
  - To keep the energy exactly, the giver and the taker would step as two families: G(1/2) K(1/2) H K(1/2) G(1/2).
- **The state.** By the centering lemma, every half-stepped family then needs a centred triple for the engine's mirror,
  three counts and two teeth per gear: HAT3's element, twice over. The owner's note sets it aside.
- **Can the third count be dropped?** Not with the engine's mirror (section 2). With a mirror that holds a step, yes,
  but then the palindrome is not needed: B-edge keeps the energy as exactly with no third count.
- **Not built. The answer to "can the third count be dropped" is B-edge**, which needs no half step.

## 6. Measured (board clock facts; b_edge.py and stagger.py on the tree of 1794d474b; rec/)

### 6.1 The shipped pair world (the run test's NOT_CLOSED 37 record: held (1, 0) at rest, the giver at 14)

| reading (rec/pair_1.txt, rec/pair_2.txt) | B-edge |
|---|---|
| rounds | 1260 of 1260, no count past the width |
| widest count | 6 bits (3 to 6 at the readings every 60 rounds) |
| E32 | 4.94 10^14 at the lay; 3.75 10^14 to 2.58 10^16 over the run |
| the identity dE32 = the teeth's share | 1260 of 1260 rounds, to the unit |
| T's curvature, the explicit window | at most 24 permille of 4W (round 1260) |
| H's 2g, inside its dial | at most 1080 permille of 4W (round 131): past the engine's window, and held |
| the run back from the end state alone | exact over 1260 rounds |
| the 24 | alike in 24 of 24 turns over 100 rounds |
| the hidden twin (one unit in the held train's click tooth at the clock) | board alike in 1260 of 1260; clicks alike, as the unit met no carry edge |
| whole clicks, SUM of abs(q) by train | held 523, giver 3879, taker 3838 |
| two runs | byte for byte alike (sha256 of the output 899c47df5cd5...) |

- **Beside it:** the engine falls at 766 (the held window), road (a') at 531 (the tied window, with the counts at 31
  bits by round 500), and HAT2 holds 3 to 5 bits with its run back failing at 188.
- **The held curvature passes the engine's own window** (1080 permille at round 131). Under the engine's step that is
  the runaway; under B-edge the dial carries it and nothing happens.

### 6.2 The shipped click world (27 Node-clocks; the held hand at 1 and the giver at 40 at rest at every one)

| reading (rec/click_1.txt, rec/click_2.txt) | B-edge |
|---|---|
| rounds | 5000 of 5000, no count past the width |
| past the engine's 3752 | 5 bits at round 3750, 5 at 4000, 6 at 4500, 5 at 5000 |
| widest count | 7 bits (4 to 7 at the readings every 250 rounds) |
| E32 | 1.18 10^20 at the lay; at most 6.81 10^22 over the run; 6.58 10^22 at round 5000 |
| the identity dE32 = the teeth's share | 5000 of 5000 rounds, to the unit |
| T's curvature, the explicit window | at most 45 permille of 4W (round 4993) |
| H's 2g, inside its dial | at most 1038 permille of 4W (round 432): past the engine's window, and held; the 20 readings every 250 rounds from 84 to 510 |
| the run back from the end state alone | exact over 5000 rounds |
| the 24 | alike in 24 of 24 turns over 8 rounds |
| the hidden twin, over 300 rounds | board alike in 300 of 300; clicks alike, as the unit met no carry edge |
| whole clicks, SUM of abs(q) by train | wave 0, metric 0, held 3,605,499, giver 6,537,024, taker 7,594,560 |
| two runs | byte for byte alike |

- **Each Node-clock runs the one Node-clock's course.** The lay is the same at all 27 and the Meshes pull nothing
  between equal counts. Read on click1/ (the same universe, shape 1 x 1 x 1, the one Node-clock laid as each of the
  27; rec/click1_1.txt and _2.txt, alike, with probes/same27.py):
  - at all 20 readings the widest count is alike, and E32 and its held and other parts are exactly 27 times the one
    Node-clock's;
  - the whole clicks are 27 times: 133,537, 242,112 and 281,280;
  - the one Node-clock gives, every round, the held dial's smallest value (1,299,940,000, 541 permille of 4W, round
    1405) and the books (section 4.4: 0 misses of 25,000 clock-rounds). The identity holds in 5000 of 5000 and its
    run back is exact.
- **Beside it:** the engine falls at 3752; HAT2 holds 5000 at most 8 bits (its run back read over 400 rounds, and
  failing at 188 on the pair world); road (a') 5000 at 3 to 7 bits (its click run back not run); HAT3's palindrome
  read 3900 rounds, at 35 bits by 3750.
- **The held hand heats.** The energy walks up with falls: E32 at 3.5 10^20, 2.2 10^21, 1.4 10^22, 1.5 10^22 and
  6.6 10^22 at rounds 250, 1000, 2500, 3750 and 5000. Every unit of it is the teeth's share (the identity).
  - At round 5000 the held energy per Node-clock, 2.4 10^21 / 32W with g about 1.6 10^8, is an amplitude of about 28
    counts. T's curvature, at most 45 permille, puts it at about 30.
  - The tied window is at about 141 counts.

### 6.3 The square-2 lay (S/nc29/pair2; read beside STOP1's stop, not counted against the step)

| reading (rec/sq2_1.txt, rec/sq2_2.txt, alike) | B-edge |
|---|---|
| rounds | 1260 of 1260, no count past the width, the widest 5 bits |
| E32 | 9.87 10^14 at the lay; 9.34 10^14 to 2.12 10^16 |
| the identity | 1260 of 1260 rounds |
| T's curvature | at most 36 permille of 4W (round 506) |
| H's 2g | at most 325 permille of 4W (round 1117) |
| books (section 4.4) | 0 misses of 3780 clock-rounds |
| the run back from the end state alone | exact over 1260 rounds |
| the 24 | 24 of 24 over 20 rounds |
| whole clicks, SUM of abs(q) | held 2409, giver 8282, taker 4685 |

- **Beside it:** the engine runs away at 1195 (the held window, CONF1); HAT2's dg holds the window, and then the held
  count settles at 0 from round 432 and the tied pair falls along x_g = -x_t to 50 bits by 1250.
- **On B-edge the held hand does not settle.** E32's held part stays at 5.4 10^14 or more at every reading, where a
  held hand at rest at 0 would read 0. It keeps moving (the teeth's share, CONF1's mechanism), and within 1260 rounds
  the tied pair does not fall.
- This is a reading of the motion, not a confinement. The potential stays unbounded below there (HAT2 section 4), and
  the probe of section 6.4 shows it falling on the shipped lay later. STOP1's stop is the structural cure; this lay is
  read beside it when it lands.

### 6.4 The pair world past its ticks (a probe of the margin, named as a probe)

The shipped pair world's files, asked for 20000 rounds (rec/pair_long_1.txt and _2.txt, alike; the trace
rec/trace_fall_1.txt and _2.txt, alike, from probes/trace_fall.py):

| reading | B-edge |
|---|---|
| through round 1880 | the widest count at most 8 bits |
| from about round 1640 | the tied pair falls along the files' open direction. By round 1892 the giver's first row has gone from 14 to 157 and the taker's to -67, the held hand still at one count (0 or 1 in squares, below the open region's 0.8 on average) |
| rounds 1891 to 1902 | the tied pair swings back. The held hand is kicked from 1 to 3, 6, 8, 21 and 42 counts, and the giver's row goes through 0: 39, -1, -40, then 62 at round 1903 |
| round 1903 | the giver's row changes sign across the held edge: g_out = -14,852,000 and the held out-dial W(a) + W(a') + g_out = -2,852,000, below 1, so Rule3's carry has no teeth |
| then | the held count jumps to 502, T's curvature to 3.0 10^9 against 4W = 2.4 10^7, and the counts pass the width after round 1917 |
| the identity | 1917 of 1917 rounds, even through the fall |
| the run back from the end state alone | exact over 1917 rounds, even with the dial below 1 (the carry's algebra survives a negative divisor; its law does not) |

- **The fall is the files' first.** The held hand's |k|^2 at one count leaves the open direction open, as CONF1 and
  HAT2 name it.
- **The step's failure follows it.** The polarized dial's sign breaks only once the tied counts swing through 0 at more
  than about sqrt((2W + spring) / c) = 47 counts across one edge.
- On the shipped 1260 ticks neither happens. STOP1's stop is the road for the first. For the second, any lay that
  keeps the tied counts from changing sign across an edge at that size keeps the dial at least 1.

## 7. Limits and OPEN

- **The tied family's window** (2 c |k|^2 + its other stiffness < 4W) is held by the kept energy and the motion, not
  by construction. On the shipped worlds its largest reading is 24 permille of 4W (pair) and 45 (click).
  - The teeth's share walks the energy up: the click world's held hand goes from 1 count to about 30 in 5000 rounds,
    against the window's 141.
  - A long enough run could reach it. OPEN: no bound is held, and none may be ("a floor or a bound is an if").
- **The held dial's sign** (W(a) + W(a') + g_e >= 1, g_e = spring + c t . t') is held by the motion.
  - It breaks only where the tied counts change sign across one edge at more than about 47 counts (pair) or 147
    (click).
  - On the shipped runs its smallest reading is 13,096,000, 545 permille of 4W (pair), and 1,299,940,000, 541
    permille (click).
  - In the pair probe past its ticks it broke at round 1903, after the files' open direction had fallen. OPEN, with
    STOP1's stop.
- **Exactness covers the worlds' coupling family.** It holds for monomials holding a held row twice beside alike
  tied legs or units, and for tied potentials at most quadratic with constant coefficients.
  - A held quartic (the hat's (e; a, a, b, b)), a held row held once beside a tied leg, or an off-diagonal tie entry
    listed in one order would each need its own reading (the probe stops by name).
  - So would the metric's push, which reads the held rows' momenta on the engine's dials, and the gradient vertex.
    Both are at factor 0 in both worlds. OPEN for the worlds that turn them on.
  - The Meshes' exchange between Node-clocks is 0 on these uniform lays and is not booked in section 4.4. OPEN for a
    lay that is not uniform.
- **The click half of the owner's seed test (ii)** is not shown by these lays. The hidden unit met no carry edge, so
  the clicks stayed alike while the board stayed alike. The board half holds: the clicks push nothing into the
  gears, as built.
- **The square-2 lay and the late pair fall** are the files' open direction (CONF1). The tied pair's stop is STOP1's.
- **Term 11's passing for a four-leg monomial** on this round is section 4.4's P. Building it, and its key's units, is
  OPEN for the writer, David and KEY3.
- **Not built.** Nothing goes into src. The act is a probe's (b_edge.py) on the extracted tree. Building it is the
  writer's, after both hostile readers.

## Statuses

- **DERIVED:**
  - the edge's rule (section 1);
  - the centering lemma, and the true stagger's own mirror M_s = M after P and its energy's error (section 2);
  - the B-edge round: acyclic, its edges' own dials, the run back by the engine's mirror, the 24, no new state
    (section 3.3 to 3.6);
  - its energy E32, kept exactly when nothing rounds (section 3.4);
  - the whole-number identity, the teeth's share (section 4.1);
  - the lemma, that no polynomial is kept by a slow carry-quotient gear (section 4.2);
  - each monomial's exchange exact and summing to 0 over its legs, the tie's P (section 4.4);
  - the palindrome's needs (section 5).
- **MEASURED (board clock facts, two runs byte for byte alike each):** section 6 and section 4.4's table:
  - the pair world, the click world past 3752 and the square-2 lay;
  - the identity in every round;
  - the run back from the end state alone;
  - the 24;
  - the books per clock;
  - the stagger's two run backs;
  - the uniform act byte for byte the selecting act's;
  - the pair probe's fall at 1917, past its ticks.
- **OPEN:**
  - the tied window's and the held dial's hold past the runs read, by the motion alone;
  - the lemma's written proof for the coupled round, and any statement for the stiff held rows;
  - a world with the metric's push, the gradient vertex or a non-uniform Mesh on;
  - term 11's passing for four-leg monomials as P, and its key;
  - the energy's book kept as state (set aside with the new tooth);
  - the click half of seed test (ii) on these lays;
  - the square-2 lay and the late fall beside STOP1's stop.

## Files

All in S/miracle_b/ (S = S):

- MIRACLE_B.md, this text.
- b_edge.py: the B-edge round (its selecting and its uniform form), E32, the identity, the run back, the 24, the twin,
  and the options books (section 4.4), shares, dial and mode=engine.
- stagger.py: the true stagger, with its run back by the engine's mirror and by M_s.
- probes/trace_fall.py: the pair probe's rounds around its fall.
- tree/: git archive 1794d474b src examples, plus tests/frame.py and tests/test_the_tensor24_run.py (the same commit)
  for the 24's turned().
- pair/ and pair2/: the pair world's files and the square-2 lay's, as in S/nc29. click1/: the click world's one
  Node-clock (section 6.2's dial reading).
- probes/same27.py: the check that each of the click world's 27 Node-clocks runs the one Node-clock's course.
- rec/: every run's output, each twice, byte for byte alike:
  - pair_1/_2 (B-edge on the shipped pair world: the identity, the run back, the 24 over 100 rounds, the twin);
    pair_uniform (the uniform act, byte for byte pair_1);
  - click_1/_2 (the shipped click world, 5000 rounds: the identity, the run back, the 24 over 8 rounds, the twin over
    300) and click_cmp.txt; click1_1/_2 (one Node-clock: the books, the dial, the identity, the run back);
  - pair_books_1/_2 and pair_dial_1/_2; sq2_1/_2 (the square-2 lay, with the books); stagger_pair_1/_2;
    pair_long_1/_2 and trace_fall_1/_2 (the probe past the ticks).
- Digests: b_edge.py sha256 66f8bc57228b...; stagger.py dacda0d25f17...; rec/pair_1.txt 899c47df5cd5...;
  rec/click_1.txt 4d3f4bc56346.... The final b_edge.py reruns pair_1 byte for byte.
- Run with S/live/.venv/bin/python -I (python3 3.14.6, numpy 2.5.4), from S/miracle_b/, for example
  `python -I b_edge.py pair/universe.json pair/piece.json pair/setting.json every=60 turns=100 twin=1260`.
