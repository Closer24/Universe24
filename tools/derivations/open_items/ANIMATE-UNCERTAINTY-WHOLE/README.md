# Fourier's support bound on Tensor24's board, in whole numbers: what of the uncertainty principle follows from the board alone

Big Pic (formerly Animate), 2026-10-30, the second text: the re-run of ANIMATE-UNCERTAINTY (held in git at scribe-5
6183738b1), which left the tree on the owner's word "Delete" because it drew 3,000 waves at random on each board. The
architecture document's Uncertainty lines stood on it (Sofer's 6523506996 item 3 and 6523641446 item 3). This probe
counts every wave of a class in place of the draw, and counts the waves at the bound a second time, independently.
Every division is Rule3's carry; nothing here holds a float, a root, a circular call, a random draw or a fraction.

The first text (reader-5 91e3b8e61) went to a hostile mathematician and a hostile physicist, each new to it. Both
agreed with changes: six and six blocking items. Every item is folded here, and section 7 lists them. **Status:
DRAFTED,** the second text for a new pair.

The owner's word that began it (2026-10-30, 03:1x UTC, in Hebrew; in translation, his first person plural rendered
without a person): "Summarize, then, how it all connects, and how uncertainty follows from the board with no specific
law. Explain each step by its logic and check it."

Run: `python3 tools/derivations/open_items/ANIMATE-UNCERTAINTY-WHOLE/uncertainty.py`, about two minutes, on main
9067de20d's engine and example files; the output is uncertainty.txt.

## 1. How it connects

- **The board:** Node-clocks on a board that wraps, each reading its six neighbours alone, each round once (decision
  42). A gear holds two moments, now and before. The run is fixed by the files, and it runs back exactly.
- **A motion of the board** is a pattern that a shift of the board by one Mesh leaves as itself, turned by one fixed
  turn at every Node-clock: a character of the board's group. A gear's own rate (its now less its before) is another
  thing, and the count below is on the motions of the board.
- **A click** (G5, terms 11 and 12, both DRAFTED and not agreed): a quantum taken where a train's swept area completes
  a key, and, at a split, a draw that says which part takes it. The click pushes nothing into the gears.
- **What follows from the board alone** is Fourier's support bound. What makes it Heisenberg's is owed to the clicks
  (section 4).

## 2. The steps, each with its check

| Step | Its logic | Its check (uncertainty.txt) |
|---|---|---|
| 1. A place is a Node-clock | a click will stand at one site | the record's click lines carry one site (record/schema.py: Whole and Split); not in the probe |
| 2. A gear's own rate | a gear's rate is its now less its before; its force is its neighbours' differences | part 1, item 3: every round's before slot is the last round's now slot (engine/step.py, gear and sources) |
| 3. Six neighbours, a wrapped board, one Mesh a round | the board's own Meshes; a round reads a Node-clock's six Meshes and nothing else | part 1, item 1: 64 Node-clocks, six neighbours each, all different, each Spoke's opposite leading back, every neighbour one Mesh away across the wrap. One Mesh a round is the act's own (step.py reads seen(a, nb)), read from the code: on this example nothing travels (part 1, item 2) |
| 4. The board's shifts | a wave's motions are its parts under the board's shifts; a wave at one Node-clock is shifted to another, never to itself | part 1, item 1 (the board's shifts); on the engine's own example nothing moves: part 1, item 2, and section 5 |
| 5. The board's motions | a motion is a pattern a shift by one Mesh leaves as itself times one turn, the same at every Node-clock: the characters of the board's group, as many as its Node-clocks, every wave one sum of them | theorems (section 3), not checked here. Whether the engine's round leaves a motion as itself is not checked; with the carry it does not exactly ((-1)^x laid standing comes back 0 where it was 1) |
| 6. One Node-clock holds every motion | a wave at one Node-clock has every character in it, alike in size | part 3: one Node-clock holds 64 motions of 64 |
| 7. One motion fills the board | a character is alike in size at every Node-clock | part 3: the whole board alike holds 1 motion; the wave 1 0 -1 0 along z holds 32 Node-clocks and 2 motions (a wave of whole numbers holds a motion with its reverse) |
| 8. The trade-off, counted | the Node-clocks a wave holds times the motions it holds are never fewer than the board's Node-clocks | part 2: every wave of -1, 0 and 1 on rings of 2 to 10, the least exactly the ring. Part 3, the least exactly the board's Node-clocks in each class, by size: every wave of -1, 0 and 1 on the board of 2 by 2 by 2 (6,560); every wave of -1 and 1 on 1 to 3 Node-clocks of the board of 2 by 3 by 4 (17,344); every wave of -1 and 1 on 1 to 4 Node-clocks of the example's board of 4 by 4 by 4, its first Node-clock at 1 (325,627). In every class the waves at the bound are exactly the characterization's (section 3) |
| 9. The click | a click will stand at the Node-clock whose area completed a key (term 11), and at a split the draw says which part takes it (term 12). On the record a click is one site, so by step 6 the record's line holds every motion. The click pushes nothing into the gears, so the engine's wave is not localized by it | none: no click exists before G5 |
| 10. The same in time, as counting | a beat is a motion of the gear's own ring of rounds; one round fixes no beat, R rounds fix one to within 1 / R | part 1, item 5: the state at round 6 is the laid start, slot for slot, so the laid gear's beat repeats every 6 rounds exactly (the example's teeth are six grips, so with its neighbours silent the gear steps a+ = a - b). On that ring it holds 4 rounds and 2 beats, and one round alone holds 6 beats of 6, the transform of a one-round wave: an identity |
| 11. The run is fixed, and is not read from inside | the run is fixed and runs back exactly; a Node-clock sees its neighbours as they were a round before, one Mesh a round | part 1, item 4: 60 rounds run back slot for slot; the one Mesh a round is read from step.py |

## 3. The algebra

- **The motions.** A wave f on a wrapped board G = Z_a x Z_b x Z_c of N Node-clocks has N motions, the characters
  chi_k(x) = zeta^(e(k, x)), where e(k, x) = SUM_j (T / s_j) k_j x_j mod T, the sides are s_j, T is their least common
  multiple and zeta is a primitive T-th turn. Its motion k is held where f^(k) = SUM_x f(x) chi_k(x) is not 0.
- **Exact, in whole numbers.** f^(k) is the value at zeta of the whole-number polynomial
  P_k(z) = SUM_x f(x) z^(e(k, x)), and it is 0 exactly where the cyclotomic polynomial Phi_T divides P_k, since Phi_T
  is zeta's minimal polynomial over the rationals. Phi_T is monic, so the remainder in whole numbers is the rational
  one, one remainder per motion.
- **The bound,** |supp f| x |supp f^| >= N for every f not 0:
  - Donoho and Stark's (1989) on a ring Z_N;
  - Matolcsi and Szucs's (1973) and K. T. Smith's (1990, SIAM J. Appl. Math. 50, 876) on every finite abelian group.
    Smith also found the waves at it: exactly the constant multiples of a character on a coset of a subgroup (an
    elementary proof of both: Matusiak, Ozaydin and Przebinda, Acta Math. Univ. Comenianae 73, 155, 2004).
- **Its proof in two lines.** For k in supp f^, |f^(k)| <= SUM |f| <= sqrt(|supp f|) ||f||_2 by Cauchy and Schwarz.
  Parseval then gives N ||f||_2^2 = SUM_k |f^(k)|^2 <= |supp f^| |supp f| ||f||_2^2.
- **The waves at the bound, counted twice.** The probe finds them by the cyclotomic remainder, and counts them again,
  independently, as every constant times a character with values 1 and -1 on a coset of a subgroup (the subgroups by
  closure, the characters by their products). The two sets are the same in every class:
  - on the rings, 8, 8, 20, 12, 32, 16, 44, 26 and 48;
  - 256 on the board of 2 by 2 by 2;
  - 208 on the board of 2 by 3 by 4;
  - 99 on the example's class.

  A wrong table of characters would part them.

## 4. What follows

- **Fourier's support bound on the board.** No wave is sharp both in its Node-clock and in its motion: the Node-clocks
  a wave holds times the motions it holds are at least N, since a motion is alike in size at every Node-clock and a
  wave is one sum of motions.
  - This is the discrete counterpart of the uncertainty principle's mathematics, with the board's count N where a
    textbook holds h.
  - It is Heisenberg's only once a motion is read as a momentum, p = hbar k, and a wave as one quantum's amplitude. Both
    belong to the clicks (G5, terms 11 and 12, DRAFTED and not agreed).
  - It bounds counts of Node-clocks and motions, not spreads: two Node-clocks half a board apart hold 2 nodes and 32
    motions, yet are as wide in place as the board.
  - Kennard's sigma_x sigma_p >= hbar / 2 has no exact form on a finite board, since no two operators on N
    Node-clocks have [X, P] = i hbar (a commutator's trace is 0). The exact finite forms are this one and Maassen and
    Uffink's (entropies: H(x) + H(k) >= log N).
- **What is read from inside** (step 11): the run is fixed, and no Node-clock holds the next click, since what decides
  it arrives one Mesh a round. This is determinism read through a cone, not the uncertainty principle.
  - Whether a split's draw gives Born's shares is term 12's (DRAFTED, not agreed).
  - Distant correlations are decision 28's two boards, not this page's.
- **The record's past.** The record will hold two sites and two rounds, a lay's and a take's. Which lay is which take's
  is G5's (term 11, not agreed).
  - Between the two no motion is read: a quantum at one site holds every motion, backward as forward.
  - Heisenberg's remark allows such a retrodiction and calls it speculative, and this page claims no more.

## 5. What does not follow, and is not checked here

- **A travelling wave on the engine.** On the example nothing travels: the laid gear stays at its Node-clock in all 60
  rounds, and its neighbours' fine teeth move and never carry (part 1, item 2). A file that lays a travelling wave is
  the Boss's.
- **A character as the round's own pattern.** Not checked, and false at the probe's small amplitudes, where the carry's
  floor rules the step.
- **The click's back-action.** The click pushes nothing into the gears (term 11), so the disturbance a measurement
  makes, the other half of Heisenberg's argument, is not on this engine.
- **The click and its draw** (G5, terms 11 and 12) **and the slit** (bodies, G6). The slit is where the count would be
  read on clicks: the narrower the slit, the wider the clicks on a far screen.
- **Planck's constant.** The count has none, because it is Fourier's and not yet a momentum's. hbar enters where a
  motion becomes a momentum, term 11's key (ANIMATE-UNIT).
- **Kennard's and Robertson's forms with spreads:** no exact form on a finite board (section 4).

## 6. Status, for the architecture document's Uncertainty lines

- **Board and Algebra:** the bound is proven (section 3) and counted exactly on every wave of each class, the waves at
  the bound being the characterization's. Checked as Fourier's count on the board's group. The round's relation to the
  motions is not checked.
- **Clock:** checked as counting: the laid gear's beat, period 6 with 2 motions on its ring of rounds. It is not checked
  as energy and time, which needs E = n hbar omega (term 11).
- **Clicks:** OPEN until G5's click and draw stand. A one-round wave holding every beat is an identity and needs no
  click. A mass read as a beat (term 11), and the draw's place and shares (term 12, G6), are not this probe's.
- **For the document, when both readers pass,** the four lines read:
  - Clock: "one round holds every beat of its ring and only many rounds tell a beat; one Node-clock holds every motion
    of the board, and a sharp motion, laid alone or with its reverse, fills the board";
  - Board: "the Node-clocks a wave holds times the motions it holds are never fewer than the board's Node-clocks:
    Fourier's support bound on the board's group, a count with no law of its own (whole numbers with no draw, every
    ring of 2 to 10 and three boards, the example's among them, the waves at the bound exactly the characterization's;
    ANIMATE-UNCERTAINTY-WHOLE)";
  - Clicks: "OPEN (G5): it is Heisenberg's only once a motion is a momentum, p = hbar k (term 11's key), and a wave one
    quantum's amplitude (term 12's draw); it bounds counts, not spreads; the click pushes nothing, so the disturbance
    half of Heisenberg's argument is not on this engine";
  - Algebra: "|supp f| x |supp f^| >= N (Donoho and Stark on a ring; Matolcsi and Szucs, and K. T. Smith, on every
    finite abelian group), each motion read as held or not by its turn-sum's exact remainder on the cyclotomic
    polynomial. **Status:** DRAFTED: Board, Algebra and Clock checked as counting, with two readers; Clicks OPEN".

## 7. The readers' items, folded

- **The physicist:**
  - (1) the title, and Fourier's bound named, not Heisenberg's; Kennard's form and the spreads (section 4);
  - (2) the logic of the board's shifts, not the engine's step (steps 4 to 7);
  - (3) one Mesh a round read from the code;
  - (4) a gear's rate told apart from a motion of the board (step 2);
  - (5) the click per terms 11 and 12, with no back-action (step 9, section 5);
  - (6) determinism through a cone, not uncertainty (section 4);
  - (7) the beat's ring as counting (step 10);
  - (8) the record's past, with Heisenberg's remark (section 4);
  - (9) Planck's constant, Kennard and Robertson, and the round's pattern (section 5);
  - (10) the beat is the example's isolated gear (step 10);
  - (11) a sharp motion laid with its reverse (section 6, Clock);
  - (12) the statuses, Clicks OPEN (section 6);
  - (13) the timing.
- **The mathematician:**
  - (1) the attributions, and the equality case in both directions (section 3);
  - (2) step 5 as theorems, not checked, with the carry's counterexample;
  - (3) part 1, item 2 now prints what moves and states that nothing travels;
  - (4) step 4's check corrected;
  - (5) the example's class on 1 to 4 Node-clocks with a shift and a sign fixed, the least by size, and the waves at
    the bound counted again by the characterization, the probe printing whether the two sets agree;
  - (6) Clicks OPEN, and no readers' agreement claimed before it exists;
  - (7) the period read off the whole state at round 6;
  - (8) e(k, x) with each side's scaling;
  - (9) no change;
  - (10) "each Spoke's opposite leads back";
  - (11) the timing;
  - (12) the class of the board of 2 by 2 by 2 named as every wave of -1, 0 and 1;
  - (13) the check column's sources named;
  - (14) the bound's proof in two lines (section 3).
