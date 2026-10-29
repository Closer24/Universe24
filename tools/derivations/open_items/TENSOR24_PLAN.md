# Tensor24: the plan for the new engine, in short

For the owner and for everyone on the work, in English on the owner's word (2026-10-28, 15:2x UTC): "the plan in English, in a file, at once, that everyone can read". It goes to the owner at 16:00 UTC, 18:00 in Israel, and he approves it if it is good (his word of 13:09 UTC). The full plan is TENSOR24.md beside this file; the derivations' board is derive/INDEX.md; the architect's approved design is derive/architecture/ARCHITECTURE.md. Where this summary and TENSOR24.md differ, TENSOR24.md stands.

## 0. In one line

**APPROVED by the owner at 16:0x UTC** (Hebrew, translated, #2187 comment 6474211874): "Approved, build it. You on the engine. Animate on the decoder." The decisions stand as recommended.

**This is the plan of a purely algebraic engine.** It names its contradictions with nature, and it does not claim nature one to one.

**The picture, in the owner's words (15:0x UTC):** "It is more logical that the whole board is one big bang, but it must run synchronously, and the detectors' clicks change the information from bang to bang, and the clocks become more and more complex: that is the picture."
- Bangs in part of the board are withdrawn, and with them item (v).

**The owner approves two things:**
- a new engine, written from zero, where every Node-clock does one act: one formula for every gear of every train, with Rule3's carry;
- the decisions of section 14. He approved (o) and (s) at 14:37 UTC.

After the approval only the Boss writes the engine. Animate writes the decoder.

## 1. The general functions: what a Node-clock does

The owner's question (15:2x UTC): "In the engine there will be vector, tensor or scalar multiplication, or complex numbers, which solve many things here, yes or no? General functions. The node must do very, very simple operations. The code must be very short, no?" Yes, to all of it.

1. **The operations are three, on whole numbers: addition, multiplication and Rule3's carry** (the owner's word to Sofer, 15:0x UTC; Sofer's proposal for Postulate 5, for the owner's word). Nothing else is on the list, so nothing else needs forbidding. A whether is the bit nonneg(n) = 1 + n div (n n + 1), a choice is b x + (1 - b) y, and a bound is the remainder of a clock's carry.
   **CHECKED** (the owner's word of 15:3x UTC, "make sure the engine can really be written with these"; derive/closed_list): the engine's 29 acts, written on a whole number that allows addition, multiplication and the carry alone, each match their plain reference with 0 failures; their code holds no if and no comparison; and 12 of 12 mutants fail. The one promise is that every divisor is a teeth count of at least 1; light's w_c = 0 (M2) and W+ <= 0 (M1) break it until they close, before the first cut. A second promise stands beside it (Sofer, #2187 6476698665): every rate lies between 0 and the full rate, since the beat's k is read as a bit; with one clock at twice the full rate k reaches 2 and the rewind is not exact (his probe on the stage 3 engine). The refusal stands by name from stage 6 (runner/load.py's promises, with the fine tooth within [0, w)), tested on a board at two full rates, where the run back is not exact; the load applies it where the files give the rates and the teeth, stage 7.
2. **On them stand three general functions:**
   - **the carry (Rule3):** n + r = q d + r', with 0 <= r' < d. Every "whether" in the engine is its quotient: a full winding, the side of the draw, the turnover. It is the one place a division is written.
   - **the Gaussian product (complex numbers with integer parts):** a hand is z = a + i b, two integer gears.
     - One product, conj(z) w, gives the dot as its real part and the cross as its imaginary part.
     - Multiplying by i is a quarter of the hand's phase.
     - The conjugation K is half of the turnover, T = J K.
     - The norm z conj(z) = a^2 + b^2 is a click's size (Born).
     - The pair dial <T psi1, psi2> gives Pauli for matter and bunching for light (section 6).
   - **the contraction of the 24 (the tensors):** one table C[K1, K2 -> K3] for each pair of kinds, computed at load from the board's shape, never typed. It holds every product:
     - the scalar (A1 x A1 -> A1);
     - the dot (T1 x T1 -> A1);
     - the cross (T1 x T1 -> T1);
     - the tensor parts (T1 x T1 -> E + T2, the stress).

     A product the 24 forbid is 0 in the table, so no rule is written for it.
3. **What a Node-clock does, for every gear:** it reads itself and its six neighbours, multiplies and adds (the formula of section 4, four lines), and carries. Nothing else. The same functions serve every family (light, matter, the twin hands, the regulator), so no family has code of its own.
4. **The code is very short:**
   - the head: 19 modules, 2,990 lines;
   - the new engine: about 720 lines with algebra/, about 850 with the formulas that close the open items inside the build (the architect's approved design, section 11);
   - every function pure, and every number in the universe file;
   - no loop in the engine: every function acts on the whole board's arrays at once.

   Its largest parts are the kind table (the 24 computed, not typed, about 140 lines) and the clicks (the draw and the writes, about 180). Around the engine stand the record (60), the readings (120), the runner (260) and main.py (15); the decoder, Animate's and separate, is about 950.

## 2. The generic core: five laws

On the owner's word to David: "a generic solution for everything". This is David's core. Every law comes from the clock and is realized by the kind table, the tensors and the 24. The laws of section 5 are its readings.

1. **The kind table.**
   - **In the clock:** every family is one row: its turns, its fixed pairing B, its phase reversal T = J K, and the coefficients of its products. Nothing is typed per family.
   - **In the tensors:** 2O and its kinds, with T T as the kind's sign, and the contraction coefficients C_K.
2. **The tick.**
   - **In the clock:** the one formula. Every Mesh couples its two ends alike, so the wind and the charge are kept. With matter held as hands, the ceiling follows by itself.
   - **In the tensors:** p+ = p + s F + K, with the grip g_j equal at both ends; the charge kept by Noether, the ceiling by Bessel.
3. **The turnover** (approved; its act at the top cancelled by the owner's word to the Boss of 2026-10-29, 06:3x UTC, decision 27: it is not a local law).
   - **In the clock** (the former text, kept by name): T = J K on every gear, at the clock's own top, as a carry. The two slots of every gear exchange, and each gear's sign is its source's.
   - **In the tensors:** (a, a-) -> (T a-, T a).
   - **The trigger at the top goes** (the owner's word to David of 2026-10-29, 06:1x UTC, "Going with your recommendation", relayed in 6489403097): the top is the act's own turning point by the spring (David's step 9, 6488889537), so stage 8 writes no trigger at the top; the reversal at the top (ALGEBRA.md line 1602) is cancelled by his word of 06:3x UTC (decision 27): it is not a local law. T = J K stays each kind's time reversal (item (s)), which the tests read and no act applies.
4. **The click** (approved).
   - **In the clock:** law 6 on the composite clock:
     - two clocks that meet are read as one dial;
     - the composite clock is the detector of its parts;
     - equal quanta meet on the side of their pairing;
     - the click counts the action;
     - the reversed run leaves the clicks undone.
   - **In the tensors:** sigma_K = N(C_K(psi1, psi2)), and c sum sigma = t room + r.
5. **Every bound a carry.**
   - **In the clock:** the Mesh's rate is one dial. Its full turn means "no tick this tick".
   - **In the tensors:** n + r = q d + r'.

**What stays for the owner's decision under this core:**
- (m) the pair dial;
- (r) the click counting the action against law 5's fixed winding;
- (u) lin against past;
- (j) the second carry;
- (g) the doubler: decided as recommended, light at the speed 1/sqrt(6) (decision 27);
- (w) one bang whose tops part: closed by the spring, the trigger at the top gone (item 3 above).

(v), the local turnover, is withdrawn.

## 3. The end state

1. **One machine of tensors in integers, all clocks.**
   - Three operations only: multiplication, addition and Rule3.
   - The quotient leaves as an event, and the remainder stays.
2. **A new engine, in new files.** It replaces the head. The head stays beside it for comparison until the switch, on the owner's decision of 09:1x UTC.
3. **Two laws not to be crossed:**
   - **time is a circle:** forward to the top, the turnover, back, and the next bang (the turnover at the top cancelled by decision 27, not being a local law: the circle is the count's swing, the spring turning it at the top and the source at the bottom);
   - **every bang shows more than the one before.**

   They agree by (o), approved at 14:37 UTC: time is a circle for the gears, and the clicks carry the arrow.
4. **Nature one to one, as far as the lattice allows.** All 80 rows of the gates must show on the one bang.
5. **Nothing the head does is lost:**
   - the bit-for-bit rewind;
   - the books;
   - the clicks;
   - the order-free step;
   - the swing;
   - the stopping clock;
   - the held field;
   - the twin hands;
   - the reference clock.
6. **The 24 hold by construction.** The kinds come from the six Spokes alone, and the Spokes from the board's shape. No act knows an axis.
7. **No numbers, no circularity and no correction.**
   - No number in the code but 0 and 1.
   - No sine, no root, no search, and no formula written for a phenomenon.
   - Every number of a train stands in the universe file or the world file.
8. **Much shorter:** the head's 19 modules hold 2,990 lines; the new engine about 850 (section 1).

## 4. The Node-clock and the main formula

1. **In the clock:**
   - every Node-clock reads itself and its six neighbours (one Mesh), and nothing beyond;
   - it does one act for every gear of every train;
   - it writes only after every Node-clock has read.
2. **The formula, for every gear a:**
   - p = W (a - a-) + (r - mid W)
   - p+ = p + s F + K
   - a+ = a + (p+ + mid W+) div W+, r+ = (p+ + mid W+) mod W+
   - F = sum_j g_j (U_j a_j - a) - D a + J
3. **What each term means, in clock words:**
   - **W and s:** the time clock's rate (in the tensors, the lapse);
   - **g_j:** each Mesh's grip (in the tensors, the spatial metric);
   - **D:** the spring, that is, the mass;
   - **J:** the source, one contraction of the other trains by the product table;
   - **K:** the kick.
4. **Two halves:**
   - **the metric half:** the regulator's gears are driven by matter's stress;
   - **the matter half:** every hand moves alike, and the metric is its coefficients.
5. **Checked bit for bit on the head** (formula0.py):
   - 41,250 of 41,250 gears on the hole;
   - 27,500 of 27,500 on nature;
   - 9,216 of 9,216 on the one bang.
6. **The hand is a Gaussian integer:** z = 3 + 12 i, two integer gears. Every act is on the coefficients, so everything stays in integers. Multiplying by i is a quarter of the hand's phase.
7. **Rule3 and the carry:** n + r = q d + r', where 0 <= r' < d.
   - The quotient q leaves, and the remainder r' stays.
   - Every "whether" in the engine is a quotient: a full winding, the draw's side, the turnover.
8. **The ladder of carries:**
   - a gear's tooth is its fine gear's carry;
   - a hand's click is its wind's carry in the winding;
   - a Node-clock's turnover is its time gear's carry;
   - the great clock's swing is every Node-clock at its top at once.

## 5. The laws, one by one

1. **Rule3, the carry.**
   - **In the clock:** when the fine gear completes a turn, the coarse tooth advances.
   - **In the tensors:** n + r = q d + r'.
   - **Status:** PROVED and CHECKED.
2. **The step.**
   - **In the clock:** the formula of section 4, for every gear.
   - **Status:** CHECKED bit for bit on the head.
   - **OPEN, to close before the first cut (the second mathematician, M1):**
     - N, U_j and J are undefined;
     - the step breaks where W+ <= 0;
     - the probe cannot fail, since it reads the head's own F and K.
3. **The rewind.**
   - **In the clock:** every gear runs back, and every carry is reversed.
   - **In the tensors:** the same step, with a+ and a- exchanged.
   - **The going:** for the rewind to be exact at every teeth count, each gear keeps its own going, the parity of its own turnovers and negations, within line 98's fixed count: the 24's turns negate some gears of a Node-clock and not others, so a going shared by the Node-clock fails at even counts (the tie rule, derive/tie_rule: PROVED and CHECKED; Sofer's law passes, #2187 6474681064; David's formula owed). Draft H founded it, and its verifier confirmed it on 91,728 states. Without that bit only the step's invertibility is proved, and the head's 20 of 20 read its stack, that is, a log.
   - **The click is many to one,** so a click is undone only from its log.
4. **The turnover** (its act at the top cancelled by decision 27: it is not a local law).
   - **In the clock** (the former text): the clock's own act at the top of its time gear.
   - **The second trigger, the floor, is struck by law 11.** There is no trigger at the bottom.
   - **The top:** the weak maximum X0 <= X1 >= X2 is the law's own text (line 1602) and the head's, a comparison that Postulate 5 refuses in engine code. The top as the time gear's carry, q, r' = carry(X - Gamma, X_c - Gamma) with T applied q times as a choice, is OPEN 7 (David, Sofer). The threshold form as first written is refuted: it is an if. OPEN 7 closes by the spring (David's step 9): the top is the act's own turning point, and the trigger goes by the owner's word of 06:1x UTC (item 3 of the core).
   - **The one mirror is an involution** only where the fine tooth is not 0 at an even teeth count. At every teeth count it is exact only as the flip r -> w - 1 - r, with the going (H, confirmed).
   - **On every gear the turnover is its kind's T** (item (s), approved at 14:37 UTC). On twin hands that is T = i sigma_y K, and T T = -1, so a twin hand returns only after four turnovers.
5. **The whole click.**
   - **In the clock:** when a hand's wind completes a full winding, a quantum leaves, and the remainder is booked.
   - **In the tensors:** q = E div w_c: q quanta click, and the remainder is booked. That is the carry itself, with no if.
   - **OPEN, before the first cut (M2):**
     - light has w_c = 0, a division by 0;
     - a negative wind gives a negative quotient;
     - the quantum per mode is the sweep (draft F).
6. **The split click.**
   - **In the clock:** the winding is shared among parts, and the draw chooses by their sizes: c sum sigma = t room + r.
   - **On twin hands against a detector:** sigma_up = N(<phi, psi>) and sigma_down = N(<phi_perp, psi>), their sum rho rho_d (Lagrange's identity).
   - **Status:**
     - the identities PROVED;
     - the sizes defined, not derived;
     - OPEN: the draw's fairness. It is not uniform: on equal parts it gives 0.875 and 0.9375.
7. **Pauli, in the click. Status: a premise.**
   - **In the clock:** the clock of two equal clocks (section 6). Two equal quanta are read as one dial, and the exchange multiplies it by T T: minus in matter, plus in light.
   - **In the tensors:** sigma_ab = N(M_a1 M_b2 + eps M_b1 M_a2), where eps = T T.
   - **What is proved:** under the premise, PROVED and CHECKED in the clicks, and no train is given a declared sign.
   - **J's verifier:** "a premise, not derived from the clocks, equivalent to spin-statistics." It goes to the owner (item (m)).
   - **The board's degeneracy pressure:**
     - it follows from the one formula itself, where every Mesh couples its two ends alike and matter is held as hands (items (q) and (a));
     - CHECKED on 18 of 18 pairs;
     - no going is needed, and the costs found before are gone.
8. **The books.**
   - **In the clock:** every remainder of every carry is kept, with its sign.
   - **Status:**
     - CHECKED;
     - OPEN: the plug (E18);
     - their second reading is the ledger, in a file of its own.
9. **The draw.**
   - **In the clock:** one number, from the digits that do not change under the 24, modulo M.
   - **Status:**
     - CHECKED as the head's draw;
     - its fairness OPEN;
     - "that there is a choice" is the one thing the law declares.
10. **Time is a circle, and every bang shows more.**
    - **Status:** a law not to be crossed (the owner's), in the law since a4b98f45e.
    - **The palindrome (both second reviewers, BLOCKING):**
      - with the exact rewind and a whole-board turnover at the top, every orbit is a palindrome between two tops. So there are only two distinct bangs, or four where T T = -1;
      - bangs differ only where the turnover is local, or where the reversed run leaves the clicks undone;
      - the owner approved (o) at 14:37 UTC: the reversed run leaves the clicks, and they make the difference between bangs (section 8).
11. **Every bound a clock's carry.**
    - **Status:** a law not to be crossed (the owner's), in the law since d4ef8db4b.
    - **The floor is struck.**
    - **H's verifier:** none of H's replacements for the stability bounds is a carry. One is an if renamed, one a bound written as a division with a branch, and one a declaration per train (item (p)).

**And more, from Sofer:**
- **"The Node-clock has no if"** (Postulate 5).
- **The closed list** (a proposal for the owner's word): a Node-clock's operations are addition, multiplication and Rule3's carry, on whole numbers, and nothing else. So it has no if (section 1).
- **"Only generic laws are approved":** a sentence not explained from the clocks, and not realized by the tensors and the 24, is a premise by name.

## 6. The two clicks, and the big law

1. **The whole click:**
   - one hand holds the whole winding, there is nothing to choose, and the wind decides where;
   - examples: the chime, the lay of a born hand, and the two ends of a decay.
2. **The split click:**
   - the winding is shared between two twin hands, and both together hold it;
   - the great clock draws which one receives, by the sizes (Born);
   - this is the detector, and the one place where a choice enters;
   - **no one decides** (Animate, 15:1x UTC): the draw is law 9's, the vernier's number from the board's own digits. It is deterministic, written in the log so the rewind is exact, and its odds are the sizes. Its fairness is OPEN (item 6);
   - **for law 10, what makes the difference is the writing, not the choice** (Animate): a click writes a definite outcome that the reversed run leaves standing, and the next bang fits more. Up or down changes the next bang's details, not whether it shows more.
3. **There is no third click, and the turnover is no click.**
4. **The big law: the clock of two equal clocks** (draft J):
   - **the pair dial:** two equal quanta at one Node-clock are read as one dial. Each is read against the other's phase reversal: B(psi1, psi2) = <T psi1, psi2>;
   - **the exchange:** on this dial an exchange is one part's full turn, that is, two turnovers: B(psi2, psi1) = (T T) B(psi1, psi2);
   - **in twin clocks (matter):** T T = -1, so the exchange flips the sign. Two identical twin clocks give 0, and that is Pauli;
   - **in one-hand clocks (light):** T T = +1, so light bunches;
   - **status:** a premise, not derived from the clocks, equivalent to spin-statistics (J's verifier). It goes to the owner for approval (item (m));
   - **OPEN:** why the dial is read at one tick, and not through line 803's kept Omega, which would give the opposite sign.
5. **The composite clock and the big law:**
   - read literally, as the composite clock's own full turn, every train comes out a boson;
   - read as one part's full turn, it is exactly this law.
6. **Bell comes from the same dial:**
   - sigma_ab = N(det[phi1^a, phi2^b]) and E = -m1 m2 / (rho1 rho2). CHSH gives exactly S = -82/29;
   - **where it works:** on one Mesh, and where the detectors' frames are held from before the birth to the click (BC);
   - **what the probe put in by hand (the second physicist):** the frames and the singlet;
   - **at a distance, with a late choice:** the composite clock must click as one (item (l); retired by decision 28, Bell at a distance standing on two boards);
   - **a late choice through the time reversal is refuted (BC's verifier):** the exact rewind brings no detector's axis back to the birth. Even with the clicks left undone (o), the next bang's pairs reach S = -82/29 only where their choices repeat;
   - this is a matter of Bell alone. The difference between bangs, through the detector's click, is law 10 (section 8).

## 7. The families and the kinds

1. **A train is a kind plus its integers in the universe file:** the pinion, and on a hand its pair (pinion, sine) over den, the checker refusing a pair whose norm is not den den (David's (n3)); the spring, the couplings and the weight. The engine knows no train's name in nature.
2. **The five kinds of the 24:**
   - A1 (1), A2 (1), E (2), T1 (3), T2 (3); together 1 + 1 + 4 + 9 + 9 = 24;
   - all derived from the six Spokes, with no typed table (engine/kinds.py, stage 6): T1 the turn, A2 the sign of its permutation of the axes, E that permutation on the plane where the axes sum to 0, T2 = A2 T1; E has no whole basis the 24 permute, so no train holds it alone (the load refuses one by name; it stands beside A1 in the tensions, stage 7).
3. **On twin hands 2O acts,** the 24 with the twin's sign: every turn comes with two signs, and the full turn is -1.
   - There are three more kinds there: E1/2, E5/2 and G3/2.
   - **OPEN before the first cut (M5, M6):**
     - only the half turns are exact on the twin hands;
     - the Spokes build five kinds, and law 7 needs the eight of 2O;
     - the one architect's finding: in no basis of the twin hands' four integer rows do the third turns act as signed permutations, so no ring alone keeps the 24 bit for bit on them. David's route: carries on what the 24 permute, the axis form (rho, S).
   - The mirrors (the 48) are not in the law.
4. **The trains:**
   - **light:** A1, one Gaussian integer, spring 0;
   - **matter:** springy hands;
   - **spin one half:** twin hands;
   - **the regulator, the metric:** 10 gears in the plan;
   - **the shift, the potential:** A1 + T1;
   - **the held field;**
   - **the ratchet;**
   - **the reference clock;**
   - **the composite clock:** proposed.
5. **A coupling, in two parts:**
   - **whether there is a coupling:** by the kind, in the 24's table;
   - **how strong:** an integer in the universe file. The couplings stand in the calibre as rows of twelve integers, (train, kind, part, operand) for each of the two sides, (target, target_kind, target_part) and the strength, an operand naming the value, the gradient, the pull, the stride before or the stride after (David, 6481240750; the strides wait for stage 7, and a gradient is of an A1 train alone); the tensors are computed at load from the board's shape, and a row the 24 forbid is refused at load (the owner's question of 15:1x UTC; TENSOR24.md, section 28);
   - **gravity:** with no number;
   - R4 goes.
6. **The mirror's breaking:**
   - the spin (T1) contracts with a current (T1) to A1. The 24 allow it, and the mirror forbids it;
   - V-A needs chirality. The plan's S J is CPT-odd, so V-A is **OPEN**.
7. **Mass:**
   - the mass is the spring, read as a beat;
   - by the click's definition it is never negative, except for the vacuum at the stability's edge, where the form is only semi-definite;
   - a hand turning backward is the antiparticle, with the same mass.
8. **Charge (draft I and its verifier):**
   - **what is kept:** Q* is kept exactly in the rational step, where the triple is read in the frame and a conjugate hand turns over without K (item (n));
   - **on the whole board:** it moves by booked local terms;
   - **what the verifier said:**
     - exact conservation would need a second carry per gear, asserted and not proved (item (j));
     - the triple in the frame is forced only under a framing premise.
9. **Dark matter:**
   - **the candidate:** a real train of one gear. It is dark to light's current by its very kind, and it attracts;
   - **what is declared:** against light's A1 forms it stays dark only where its own Z2 and a coupling 0 are declared;
   - **the remainders** are refuted;
   - **measured on the head:** the share that never clicks is almost all the shift, that is, dark electromagnetism.

## 8. The one bang and the course of time

1. **What the head shows:**
   - every Node-clock alike, and the great clock moves as one clock;
   - a swing every five ticks, 50 turnovers in 250 ticks, and matter born only once;
   - that is what the head shows, not the aim.
2. **The aim:**
   - long bangs;
   - a seed that breaks;
   - black holes that turn clocks over in place;
   - many bangs, each carrying what came before.
3. **The course's closure is not general relativity** (the second physicist, BLOCKING):
   - draft C closes the course because the seed breaks the Hamiltonian constraint, so it solves no Einstein equation;
   - on T^3, with density and Lambda not negative, general relativity has no turn back once there is matter;
   - **so the circle is law 4's premise,** the owner's time reversal;
   - the universe's observed acceleration stands against it, and that is booked by name;
   - **written exactly (David):** the 00 equation is a pure brake with an exact rewind, and every swing repeats the one before. So "each top different" was an artifact of the velocity term read at the tick's start.
4. **Animate's bangs (and their verifier):**
   - one top per bang: every 47 ticks with 5,000,000 quanta, every 147 with 500,000;
   - no trigger at the bottom;
   - the top as a carry refuted;
   - X returns exactly, but the state does not;
   - F2 carries the load.
5. **The palindrome, and what the owner approved:**
   - **the problem:** with the exact rewind and a whole-board turnover, every orbit is a palindrome, and there are only two distinct bangs;
   - **approved at 14:37 UTC:** way (2) with (s). The reversed run leaves the clicks undone. What a click wrote runs on with the gears: a born hand, a winding taken, a detector's axis;
   - **(v), the local turnover, withdrawn (15:0x UTC):** the whole board is one bang, run synchronously;
   - **the owner's direction (14:44 UTC):** "Between bang and bang, what makes the difference is in fact the detector's clicks. That is the direction I would like you to go in. And it is in the law: there are recurring bangs, and every bang adds more; the clock becomes more and more complex."
   - **Draft K:** written on paper before the research stopped at 15:00 UTC. Its toy is unrun, and it has no verifier.
     - **K1:** the detector's click is many to one. So the reversed run retraces the past's mirror up to the first click, and there sets out on a new way. It is the one place where the click breaks the palindrome (PROVED).
     - **K2:** on a finite board every per-bang count is eventually periodic (PROVED).
     - **K3:** there are at most eight kinds (PROVED).
     - **K4:** the record of clicks grows at every bang that clicks. It is the one count that grows for ever (PROVED).
     - **The conclusion:** "every bang adds more" holds in the record of clicks, at every bang that clicks. On the gears it holds only on a board with no bound, where law 11's carries are kept and the clock grows more complex. That is **OPEN**, and closes in the build.
   - **Animate's measurement:**
     - **measured:** with the twin hands and F2's carry, the clicks rise at every bang: 64, 96, 256 and 1,152, four bangs in a row;
     - **missing:** two pieces, in the build: the one-turn step (the local tick), and the singlet's lay. With them the detector's click itself fires; in these runs it fires 0 times.
   - **The memory between bangs** (Animate, 6473533004, on the owner's word to her of 15:4x UTC, that the detector's choice in one bang influence its choice in the next): T reverses every spin and way 2 keeps what a click wrote, so a direction chosen in one bang reads reversed in the next. On the twin calibre the larger twin at clock (0, 0, 0) flips up, down, up, down from the 7th bang to the 10th, until new births write over it. Alone it is the palindrome's period of two, so each bang's new clicks are still needed; a fresh draw whose odds the last choice moves is the next toy. **The chosen path** (Animate, 6473633678, on the owner's word to her of 15:4x UTC: "the path it chose for the future should not disappear; it should influence it"): the twin pair a click wrote stays in its Node-clock's gears and is the next bang's detector there (law 6); through S . J it moves the next draw's odds, from a half up to certainty with the coupling (a toy of one Node-clock over 4,096 bangs). On the board it is OPEN, since it needs the detector's click to fire. Sofer: it passes in form, the record that carries it being the pair in the gears, never the outside record.
6. **Every bang shows more: the 24's ladder, after its verifier:**
   - **what holds:** the product table and the rungs;
   - **by David's rule** one family's kinds stay A1 and E1/2 at every bang;
   - **the eight kinds** exist only with unequal quanta, and they stop at eight;
   - **so law 10 needs** an act that makes something new at every bang, and decision (o).
7. **Matter's excess (draft G and its verifier):**
   - on the one bang there is no tie, and the excess is 0 under every rule;
   - elsewhere a tie alone makes almost no charge (below 0.001). But with the skew, its declared direction moves the net charge by about the charge's own size;
   - the sign is not robust, and the tie's direction is declared, not derived;
   - Gauss's law fixes the net charge at 0 on the torus;
   - **so the excess is OPEN, the seed's.**

## 9. What is derived and what is open

| draft | what it gives | where it stands |
| --- | --- | --- |
| A | what a click writes, the unspringing, the lay | verified with corrections; Q* found; signed by David with notes |
| B | the bounds, the held load, the release | verified; signed by David with notes |
| C | the course's closure | verified; not general relativity, the circle being law 4; written exactly a pure brake, and "each top different" an artifact; signed by David in its scope only |
| D | the split's closure (Bell) | verified with corrections; signed by David with notes |
| E | Pauli in the clicks | verified, under the premise; signed by David |
| F | roots II, III, V and VI; dark matter | verified with corrections |
| G | the tie and matter's excess | verified: the tie is not the source, and the sign is not robust |
| H | the rewind at every teeth count; the bounds | verified: the going confirmed; no replacement for a bound is a carry |
| I | the charge the step keeps | verified: kept under a framing premise; the second carry not proved |
| J | the click law from the clocks | verified: a premise, not derived |
| BC (Animate) | Bell through the cone | verified; it works for frames held from before the birth |
| the bangs (Animate) | one swing per bang | verified; the top as a carry refuted |
| the ladder (Animate) | every bang shows more | verified: it stops at A1 and E1/2 |
| K | the difference between bangs, through the detector's click | drafted on paper; its toy unrun, no verifier |
| David's | Pauli's act, the readings, general relativity's six items, the cap between clicks, one mass, the asynchronous step | owed |

**Closes before the first cut:** the second mathematician's M1, M2, M5 and M6.

## 10. The contradictions with nature that remain: six roots

1. **I. The head's fakes:** they go once the derivations stand.
2. **II. The lattice and the one tick:**
   - isotropy up to order k^2;
   - **no Lorentz invariance:** one limiting speed for every train is impossible for a continuum of rest beats;
   - the CFL bound: fixed;
   - the doublers: item (g).
3. **III. One field per train:**
   - **what works:** HOM and antibunching;
   - **Born for a position, with a token:** fails;
   - **what is missing:** an entangled state of many quanta, and the vacuum's fluctuations.
4. **IV. Locality against Bell:**
   - with frames held from before the birth it works;
   - with a late choice it is a contradiction, until item (l) (retired by decision 28: two boards on one Node-clock, one forward and one backward, keep locality and carry the late choice through the birth).
5. **V. The light's kind:**
   - T1 on the Meshes, and two transverse gears;
   - the exact link on Z[i] is Z4 alone. It is fixed.
6. **VI. The course:**
   - no general relativity in the closure;
   - the circle is law 4, against the observed acceleration.
7. **More, from the second physicist (M5):**
   - Planck's constant not universal;
   - the electron's Compton length;
   - E = m c^2 off by a factor of about 4.3;
   - the wind not kept in the carries;
   - the draw's bias;
   - a stopping clock that blocks infall;
   - the graviton's polarizations.

   TENSOR24.md's section 18 must carry them all.

## 11. The code: the architect's design (approved with changes)

1. **The five laws, in five places:**
   - **the kind table:** kinds, in engine/kinds.py; the tables C in runner/load.py, from each elementary seed in turn (the loop at load), made primitive; contract, one gather, one product and one scattered sum, in engine/contract.py;
   - **the tick:** step, with shift and pull, in engine/mesh.py and engine/step.py; from stage 7a every gear's sources (its force, and J on the value, the centred difference along each axis and the force), its drive (every source's one way in, the kick) and its carry, at coefficients the layout holds until stage 7b gears them from the lapse; stage 7c brings the regulator's block, the strides before and after with their mirror, and the head compared act by act on every train;
   - **the turnover:** cancelled as an act by decision 27; T = J K stands as each kind's time reversal, one per-row sign built at load and read by the tests alone (the architect's ruling of 2026-10-29 at stages 7b and 10);
   - **the click:** click_whole and click_split, in engine/click.py;
   - **every bound a carry:** carry, in algebra/carry.py, and beat, in engine/step.py.
2. **Five folders:** algebra/ (new: Rule3 and the Gaussian integers), engine/, record/, readings/ and runner/, with decoder/ beside them.
   - The runner does not import the engine. A main.py of about 15 lines passes it the engine's functions.
3. **The state:** eight arrays as built, fixed for the whole run: a, b, r, rd and go for every gear, and ph, tn and the beat count c for every Node-clock, that is, 5G + 3 integers per Node-clock, the time gear one A1 row among the G (the hand's e of the design went, the drive's remainder rd taking its part: the architect's ruling of 2026-10-29 at stages 7b and 10; c added by the one architect's ruling, the going per gear by the tie rule; tb, which lin alone read, dropped under past by Sofer's and David's yes, 6478702384 and 6479871986, the out carrying the replaced tn). Nothing grows at run time, as line 98 sets.
4. **The lines:** about 850 (section 1).
5. **Loops** stand only in the runner, the decoder and the tests.
6. **The undo log:** runner/rewind.py alone reads it, for the rewind check. The engine reads no log.
7. **How a Node-clock speaks to another, and the two runs** (the one architect's ruling):
   - **the rule:** a Node-clock never writes into a neighbour; the word is the Mesh's carry. Each Node-clock holds its beat count c, and its beat is due where each of its six neighbours stands at a count at least c (a product of six nonneg bits, inside the engine). Every allowed due beat advances c and turns the rate dial; the gears step only where the dial ticks, so a stopped clock blocks no one. A neighbour is read as of the reader's count, its now slot or its before slot by its tn;
   - **the runner** chooses only which due beats fire;
   - **synchronous, the main run:**
     - every dial at the full rate;
     - the bang is the whole board's: every Node-clock at its top in the same round;
     - the clicks break the palindrome.
   - **asynchronous, an option for huge boards:**
     - the same rule with the due beats fired by random masks or by regions;
     - nothing sticks on a Mesh: each end holds only its own two latest slots;
     - regions exchange only their borders (halos);
     - no barrier at the top: the act at the top is cancelled (decision 27).
   - **A check that can fail:** where every dial is equal, the two runs give the same record, bit for bit.
8. **The gate:** Sofer amends it for the new folders. The new engine starts at 0.
9. **What the Boss does not do:**
   - write a line before the gate's amendment, or a cut before its open formulas stand;
   - type a table, a sign, X_c or any number beyond 0 and 1;
   - write an if, a comparison, a clamp, a loop, a raise, a log read or a board-wide sum in the engine;
   - read a train's name, or branch on a kind;
   - write a struck bound: the clamps F1, F2 and F5, the floor, min(spring, 1), the room's ceiling;
   - let the engine see a round, a mode, a region or the record;
   - grow the state at run time;
   - write a meaning twice, or pin a value in a test.
10. **The architect's ruling:** APPROVED WITH CHANGES.
11. **One architecture** (the owner's word to Sofer, 15:0x UTC: one architect; centralize it): Sofer's SOFER-ARCHITECTURE-1.md (scribe-5) is the frame the owner reads, the design its detail, and the one architect's ruling (derive/architecture/RULING.md, 15:4x UTC) decides where they differed. Beside the rule above it fixes:
    - the turnover's T^q as a choice by the bit q, not a power (cancelled with the act at the top, decision 27);
    - law 9's sorted draw as a rank count, with no sort and no law changed;
    - the width: Python integers in numpy object arrays, exact at 112 bits and beyond, int64 refused; the index tables alone are integer arrays, since an index counts places and holds no integer of a Node-clock: the board's nb (sites below N) and meshes (Meshes below 3N), runner/board.py, and the plan's two rows of the readings per term, runner/load.py;
    - **the twin hands:** in no basis of their four integer rows do the third turns act as signed permutations, so no ring alone, Z[zeta8] included, keeps the 24 bit for bit on them under element-wise carries. The departure stands until David's route (OPEN 3), and no twin train loads before it.

12. **The standard of known engines** (the owner's word of 15:5x UTC: "in the standard of known engines in the world; everything generic; only simple operations in the Node-clock"). Each part of the design comes from engines the world already trusts (TENSOR24.md, section 31, the prior art):
    - **lattice field codes (Grid, Chroma, openQCD, QUDA):** one shift primitive across a Mesh with everything else local to the site, the link U_j on every Mesh, neighbour tables, storage as a structure of arrays, halos between regions, and Wilson's term for the doublers (item (g));
    - **reversible lattice automata (Toffoli and Margolus, 1987):** Fredkin's second-order form x+ = f(x) - x-, the two slots now and before, so the rewind is exact on integers;
    - **the bit-reversible integrator (Levesque and Verlet, 1993):** a leapfrog on integers whose rounding inverts exactly, the step with the carry;
    - **lifting (Calderbank, Daubechies, Sweldens and Yeo, 1998):** an integer shear that inverts exactly;
    - **parallel discrete-event simulation (Chandy, Misra and Bryant) and Kahn's process networks:** the beat count and the due bit, so every order of the beats gives the same state at equal counts;
    - **array programming (NumPy, in the pure-function style of JAX):** pure functions over the whole board's arrays, every input passed, no loop in the engine;
    - **the point-group codes (Quantum ESPRESSO's integer symmetry matrices, the Bilbao tables) and e3nn's equivariance check:** the 24 as integer matrices, the kinds computed, and the images test;
    - **event sourcing:** the record as immutable, versioned events, and the readings as pure folds over them;
    - **Hypothesis and mutation testing:** properties, not values, and every test shown failing on a broken copy;
    - **stricter than all of them:** the Node-clock's closed list. Only addition, multiplication and Rule3's carry on whole numbers, with no float, no if and no number beyond 0 and 1 (section 1).

## 12. Who builds and when

1. **Nothing is built before the owner's approval.**
2. **Who does what:**
   - **the Boss:** writes every line of the engine, alone;
   - **David:** derives, and writes no code;
   - **Animate:** until the approval, only toys that prove something; after it, the decoder and the viewer;
   - **Sofer:** the gate and the law, on the owner's word; he approves every piece of code against the laws.
3. **Every stage needs three approvals, and every two stages a fresh hostile reader and the architect,** and then the full check exits 0 (the owner's words of 2026-10-29, 02:5x UTC, decision 26, and 06:3x UTC, decision 27; before them, every push did); a review's follow-up commits are read by the three:
   - Sofer;
   - David;
   - Animate;
   - a fresh hostile reader, every two stages;
   - the architect, every two stages, approving that the whole stands.
4. **What is built at each stage** (the owner's word to Sofer, 15:0x UTC; the one architect's ruling, section 6). Clocks first, then tensors, then the 24's operations. No line before stage 0; every test is shown failing on a broken copy; the record, the decoder and Animate's converter run in parallel from stage 0. **The order** (decision 27, with 7c placed by the architect's ruling of 2026-10-29 at stages 7b and 10): stages 0 to 7b, then the runner (10), then 7c, 8, 9 and 11; decision 28's two boards enter the order when the big picture closes.

   | stage | what is built | its test that can fail | what closes first |
   | --- | --- | --- | --- |
   | 0 | the gate amended (algebra/, the closed list in engine/ and readings/, main.py); the three files and their checker; the record's schema; the harness on a trivial engine | the scan refuses a planted if, a literal 2 and a sort; the harness fails on a mutant | the owner's yes on the closed list and the gate |
   | 1 | algebra/carry.py: carry, nonneg, choose, home and flip, forward and at -1 | the carry exact and unique; q(-p) = -q(p) at both parities; nonneg exact across 0 | items (h) and (e), and the tie rule |
   | 2 | one clock: a gear with its fine tooth; beat: the rate dial, the count c, the due and allowed bits, tb and tn (tb out at stage 4, under past) | the rewind 20 of 20, both ways; a stopped clock beats, its count advances, its gears stand | nothing |
   | 3 | two clocks over one Mesh: link, the slot read by tn, the arrivals rule; the synchronous pass and random masks | the order test: 40 random masks equal the synchronous pass, rates parted, one clock stopped; its mutant fails | item (u), past or lin |
   | 4 | the board: the six neighbours from the shape, the gather over the Spokes, the scalar light with its spring | the one-Mesh reach both ways; the formula against a naive loop model; equal to the head on the light, act by act | M1 (N, U_j, J, W+ >= 1); the cap's step; F2, F5 and the horizon; the doubler (g) |
   | 5 | the ring: the Gaussian integers, the hand, the twin hand | the ring's laws exact; T T = +1 on a hand, -1 on a twin hand | nothing |
   | 6 | the kinds and the contraction, from the board's shape; the load of the calibre's trains and coupling rows | the characters; a coupling the table lacks gives 0, named by the checker; the rename test | item (a); OPEN 3 before any twin train loads |
   | 7 | the one act on every train alike (7a the act, 7b the time gear and its ruler) | the formula test; the composition by the sum of the counts | M1 on every train; the charge |
   | 7c | the regulator's block, the strides before and after with their mirror, U_j on the hands' Meshes, E beside A1 in the tensions (placed before stage 8 by the architect's ruling of 2026-10-29 at stages 7b and 10) | the head compared act by act on every train, 0 unexplained differences | E's pairing; the take's reach |
   | 8 | the 24's operations: the 24 on the state; T = J K per gear as each kind's time reversal, applied by no act (decision 27); tick and untick | the 24 turns bit for bit, a board that is no cube as the control; T S T = S^-1 at every teeth count; the rewind through the top 20 of 20 | (w) and OPEN 7, closed by the spring: no trigger and no act at the top |
   | 9 | the clicks: whole, split, the draw by a rank count, the take, the owed writes; the books | the books closed; the exchange sign on the eight kinds; the draw's distribution; each reading with its second reading | M2; the draw's fairness; the click law's derivation, or its exactness shown again |
   | 10 | the runner: the rounds, the ledger, the undo log and the rewind check; the asynchronous option (masks, regions, halos) | synchronous and asynchronous with every dial equal: the same record and ledger, byte for byte | lin's formula, if chosen |
   | 11 | the capability table on both engines' records; then the switch | the table read on both; the end check | every bang shows more, for its row; the owner's word on the switch |
5. **Before the first cut:** M1, M2, M5 and M6 close.

## 13. The tests

1. **Five tests that can fail:** locality, purity, renaming, the formula, and the 24's images. And three more: invertibility both ways, the derivation's probe, and every test shown failing on a broken copy.
2. **After every cut:**
   - the difference for every row;
   - the rewind 20 of 20;
   - the books closed;
   - the 24;
   - the suite under 30 seconds;
   - the scan with no rise;
   - the full check exits 0.
3. **The end check:** every law holds, and every count stands at 0.

## 14. The owner's decisions

1. **(o) The exact rewind and the turnover against "every bang shows more". APPROVED (14:37 UTC).** It decides (d) and (f) too.
   - **The problem:** with the exact rewind and a whole-board turnover, every orbit is a palindrome, and there are only two distinct bangs.
   - **Way (2), the recommendation:**
     - the reversed run leaves the clicks undone;
     - the clicks carry the arrow, and the gears turn in a circle;
     - the exact rewind stays as a check that reads the log;
     - it fits the law's inside and outside, and (d).
   - **Way (1):** local turnovers, every Node-clock at its own top. It was (v), withdrawn at 15:0x UTC.
2. **(a) One hand per quantum.**
   - **It gives:** Pauli on the board. Without it a third quantum enters (29,488 of 29,952).
   - **What is asked:** one hand per quantum as fixed rows by the kind's cap, which keeps line 98's fixed count (the design; Sofer). A list that grows at run time does not fit and is refused. Whether that cap is a bound or a clock's carry (law 11) is the owner's to weigh (the one architect).
   - **The recommendation:** approve. This is how nature counts quanta.
3. **(b) T with period four on twin hands.**
   - **It gives:** the 24 kept at the turnover.
   - **It cancels:** law 4's "involution".
   - **The recommendation:** approve. Sofer says yes too.
4. **(c) Equal quanta are one train and one direction.**
   - **It gives:** it closes line 1562's open question.
   - **The recommendation:** approve. Nature agrees.
5. **(d) The circle's closure.**
   - **It gives:** law 10 with no contradiction.
   - **It cancels:** the reading of "more" on the gears.
   - **The recommendation:** the carry is kept. The record of clicks, the outside, grows at every bang, and the gears turn in a circle. That is what the owner approved in (o).
   - **The alternative, Sofer's sentence:** "Every bang shows more than the one before, until the recurrence that closes the circle."
6. **(e) The fine tooth flips at the turnover,** r -> T_d - 1 - r.
   - **It gives:** the exact rewind at every teeth count.
   - **It cancels:** the one mirror at an even count.
   - **The recommendation:** approve, with the going (H).
7. **(f) Law 10 on the derived course.**
   - **It gives:** every bang shows more.
   - **The recommendation:** twin hands in the file, the composite clock and unequal quanta, measured on the bang. **OPEN**, and decided in (o).
8. **(g) The doubler's vacuum. APPROVED as recommended (the owner's word to the Boss of 2026-10-29, 06:3x UTC, decision 27).**
   - **The recommendation:** way (1), the hold in the vacuum, after Wilson.
     - It removes the doubler with the one term the kinds allow.
     - Its cost: light at the speed 1/sqrt(6), and the pairs derived anew.
   - **The two other ways:** (2) doubles every species, a second light included; (3) breaks the loads.
9. **(h) The tick is its own time reversal, gear by gear.**
   - **It gives:** a rewind with no log, at every teeth count.
   - **It cancels:** the one mirror at an even count. Its bit is each gear's going, within line 98's fixed count (the tie rule).
   - **Sofer adds:** it is the same object as David's turnover with the frame. The frame, the going, the pawl and the count of turnovers are one remainder of each gear's ratchet.
   - **The recommendation:** approve. The verifier confirmed it, and the bit is a tooth the ratchet already has; k is an integer of the universe file.
10. **(i) The light cone as one condition per Node-clock.**
    - **The recommendation:** do not approve it now. The verifier found no carry: it is a bound written as a division with a branch, and it erases the tension's A1 part.
11. **(j) A second carry per gear.**
    - **It cancels:** the owner's decision of 2026-10-19 (line 805).
    - **The recommendation:** first prove that the second carry is needed (David), and only then decide.
12. **(k) The one act as the stationary point of one action.**
    - **The recommendation:** approve as a direction only. It gives one of draft I's two changes, and the turnover as T stays an axiom (b).
13. **(l) A composite clock clicks as one, wherever its parts are.** RETIRED by decision 28 (the owner's word to the Boss of 2026-10-29, 07:4x UTC): Bell at a distance stands on two boards, with locality kept.
    - **It gives:** Bell at any distance, and with a late choice.
    - **It cancels:** "locality is never broken", at the moment of the click.
    - **The recommendation:** not now.
      - An exact fairness of the draw comes first (item 6). With the sorted vernier's 7/8 it would signal.
      - **Its cost:** a shared state held by no Node-clock (2^n Gaussian integers for n parts), a global order of clicks, and a list of composite clocks.
14. **(m) The clock of two equal clocks.**
    - **It gives:** Pauli and light's bunching from one law.
    - **It cancels:** the declaration per train (line 821).
    - **The recommendation:** approve. In its verifier's words: a premise, not derived from the clocks, equivalent to spin-statistics.
    - **On its exactness** (the owner's word to Sofer, 15:0x UTC: "or that you manage to show that it works exactly"): it works exactly on the eight kinds of 2O, and the books close. So the plan stands on it, and its derivation from a big law above is OPEN, due before the clicks' cut (Sofer).
15. **(n) A conjugate hand turns over without K.**
    - **It gives:** the charge survives the turnover.
    - **It cancels:** "every charge conjugated" (line 1602).
    - **The recommendation:** approve, with (b).
16. **(p) Law 11 against the stability bounds.**
    - **The problem:** no carry was found for the light cone, F5 and the horizon.
    - **The recommendation:** the bounds stay booked by name as the law's exceptions, until they are derived. Do not approve H's candidates.
17. **(q) Every tick is a rotation of the state** (David's ceiling).
    - **It gives:** matter's degeneracy pressure on the board. A state holds at most one quantum, with no extra ceiling law.
    - **David's correction:**
      - no going is needed. The one formula keeps the wind exactly where every Mesh couples its two ends alike, and that is a rotation;
      - CHECKED on 18 of 18 pairs;
      - the costs found before are gone. What the head lacks is only that matter be held as hands, and that is (a).
    - **The recommendation:** approve.
18. **(r) A click counts the hand's action** (David's one mass).
    - **It gives:** a train's mass is its pair, g = pinion + i s, and its sine is the exact reading. The quantum per mode is the action, kept exactly under every uniform change of the clock.
    - **It cancels:** law 5's fixed winding.
    - **The recommendation:** approve as a direction; David's law sentence.
19. **(s) The turnover is the kind's own T, on every gear. APPROVED (14:37 UTC).**
    - **It gives:** one sentence for three findings:
      - E's i sigma_y K on the twins;
      - the regulator's three flow gears, the cause of the moving state;
      - the charge kept by T (n).
    - **It cancels:** the same mirror on every gear. Each gear is even or odd as T makes it.
    - **The recommendation:** approve. It unites (b), (n) and the flow gears' correction. With it every bang of one clock is a copy, so it is decided together with (o).
20. **(t) Every meeting of clocks is one shared dial, which the 24 decompose into kinds, and the click draws a kind** (Animate).
    - **It gives:** one act for three things:
      - the composite clock, as law 6 on two clocks;
      - the Bell pair's singlet, as the A1 clock of the birth's two ends;
      - Pauli's click law.

      The ladder climbs only through the birth's unequal pair, and the eight kinds stand at the fourth bang. David: the composite clock is the big law above the click law.
    - **It cancels:** the click law's separate statement.
    - **The recommendation:** approve, as law 6's form for the composite clock. It gives no sign, so (m) stays.
    - **Animate's kind-keeping click** (checked again on the owner's word of 15:2x UTC): the 24's kind projection of a two-point tensor, one act for the whole click, the detector's click and the fusion. A candidate, not law 10's solution. OPEN: the local tick, Bell at a distance, the exchange sign, the density step's locality, and the fusion's books. Its risk: a first burst that spends the light.
21. **(u) The asynchronous read: past or lin. Past, as decision 25's reading derives it, put to the owner.**
    - **It gives:** a read that keeps the time reversal must see the new state after half a tick (PROVED).
      - **past** keeps the cone and breaks the reversal.
      - **lin** keeps the reversal, and reaches 318 of 372 Node-clocks faster than one Mesh per shortest tick.
    - **It cancels:** Postulate 3 against Postulate 2, in the teeth.
    - **The recommendation:** lin, as David and Sofer recommended. The great clock's tick is nothing observed. Sofer's moved to past on the stage 3 finding below (#2187 6476698665), and David's too (6478324607): in the beat a neighbour as of c is one of its two slots, which past reads exactly. Its price: where the dials part, the gears' run back after the turnover is not the forward run's mirror, while the rewind stays exact through the outs. The owner's word on the change is asked.
    - **Found on the stage 3 engine (derive/asynchronous_read, CHECKED):** past keeps the order test, 40 of 40 random schedules equal to the synchronous pass; lin as one carry by tn - tb fails it, 0 of 40, since a neighbour one count ahead holds its next tick. Stage 3 reads by past, the ruling's line 5; lin's formula with the order test's form under it, or past kept, is David's word.
22. **(v) The local turnover, at every Node-clock's top. WITHDRAWN (15:0x UTC):** the whole board is one bang, run synchronously.
    - **What it gave:** with the exact T, worlds where the clocks turn over at different ticks keep their clicks; only one-clock worlds copy themselves.
    - **Law 4 would have read:** "The turnover is T = J K on every gear, at the clock's own top, as a carry; each gear's sign is its source's."
    - **What it cancelled:** the whole board's turnover at once.
    - **What it was:** with (o), the generic way out of the palindrome. The clicks break it instead.
23. **(w) One bang whose tops part.**
    - **The problem:** a whole-board turnover, where the tops fall at different ticks, must read the whole board, and line 92 forbids that. David's trigger also types X_c.
    - **The recommendation:**
      - the trigger stays local, at every Node-clock's top;
      - the bang is the swing where the tops fall together;
      - how far the tops part is measured in the build, before a global read is asked of the owner.
    - **Closed** (the owner's word of 06:1x UTC, relayed in 6489403097): the top is the act's own turning point by the spring (David's step 9), so no trigger is written, local or whole-board.

24. **(x) A candidate big law: the board is dials and their carries** (Animate, 6473326413, ANIMATE-CLOCK-ROOTS.md, reader-5 ab860c82, on the owner's word to her of 15:2x UTC; a candidate big law, with no verifier): each clock's time is the carry of its own dial; clocks that meet share one dial; every carry keeps the kind of what feeds it. Its letters: A, time (the local tick: a fast clock ticks more often, one at rate 0 does not tick, light crosses one Mesh per local tick); B, state (the joint dial held where its clocks meet, so a winding may stand with no direction and the detector's click has something to decide); C, selection (still light lays the singlet, a lead lays the vector along its Mesh). Its toys: local_tick.py (the local tick holds, its rewind exact over 9,600 events, where one tick for all grows past 10^6); kind_kept.py (the singlet and vector lay keep the 24 at 72 of 72 cases, the head's lay at 12 of 72); the families' ladder (a vector light reaches the 24's five kinds by bang 3, all eight with the twins by bang 3 or 4). The owner's to decide with it: the light as a vector (T1, three Gaussian gears). OPEN: law 7's premise; Bell at a distance; the density step's form; the draw's fairness; the joint toy of A, B and C on the one big bang. Recommended: approve as a direction, checked in the build by the joint toy before it enters the law.

25. **(y) The time gear's law: Postulate 6, rates multiply along a gear train. APPROVED (the owner's word of 2026-10-29, 01:3x UTC, in translation: "Rates multiply along a gear train, so the time gear's law is linear in the logarithm of the rate. Let it enter as a law that is enforced, and as a postulate, in simple words").**
    - **The postulate, in simple words:** when a clock drives a clock, their rates multiply. So when two causes slow a clock, the slowdowns multiply, and what adds up is the logarithm of the rate. The time gear's law is therefore linear in the logarithm of the rate.
    - **What it decides:** David's family of time gear laws, each linear in (Gamma / N)^n, its member n = 0 the logarithm ln (Gamma / N), the family's limit (6484103660): n = 0, Einstein's, under which a planet's perihelion advances as in general relativity. The head's n = 4 gives a third of that: 14 arcseconds a century for Mercury, where nature shows 43.
    - **How it is enforced:** the time gear holds the count c, the logarithm of the rate in notches of one tooth in Gamma, so its law is the one act itself, linear in c, and no gear holds a power of the rate for a file to set. A test shows two slowdowns composing by their product: the strides of two sources add bit for bit, with the head's law (the same act on the stretch) as the mutant it must refuse. Sofer reads every push against it, as against the other postulates. The law's former text of Postulate 6 (ALGEBRA.md line 35) had the engine build the time gear's coupling with itself; it goes on the owner's "Cancel what contradicts it" (Sofer, 6489336828; scribe-5 203ed9d3f): the time gear holds the count c and steps by the one act, with no coupling of the time gear with itself and no file setting a strength for one, the load refusing a file that names one (the time gear stands after the file's trains, so a coupling or a gear on it is off the trains' rows).
    - **What follows, as the owner ruled it** (his words to David of 2026-10-29, at the minutes of David's record, 6489315667, item 4: at 03:18 UTC, "I am going with your recommendations", relayed in 6486960331; at 03:33 UTC, "Approved. Send to the Boss and to Sofer to enter as law. Cancel what contradicts it.", relayed by David at 03:40 UTC, 6487250651; at 06:1x UTC, "Going with your recommendation", relayed in 6489403097):
      - the time gear holds the count c, the clock's load (p0 = Gamma (1 - 1 / Gamma)^c): in c the law is the plain act, the grip per Mesh and the matter's source, with no self-source and the drive at fixed teeth, and the coefficients read the ruler Y = Gamma^2 / p0 from c by the law's rate line (David's p17; the ruler as the gear, the Boss's earlier reading, could not run back where Y falls);
      - item (u) is past: the due beat keeps a neighbour at most one count ahead, so the slot written at or before the reader's count is its value there, exactly;
      - G is K-S1's, derived at load from Gamma;
      - the time gear's spring is the clock's one notch, D / W = 2 / Gamma, the pinion rim - rim div Gamma, derived from den and Gamma (ALGEBRA.md line 352, **The volume holder's rest is the clock's one notch**): the board's mean count swings and returns (Postulate 4), where with no spring it rises with no top (David's p17); the metric's spin-2 part, the block and the flows, keeps the spring 0, so gravity's two polarizations stay massless and light bends as in general relativity;
      - the load's source is rho + 3p, the form plus the pressure (David's 6488709540, the owner's word of 06:1x UTC): J at the time gear is -2 value . force - D value . value over every row of the file's trains, D the row's spring at rest (light's 0), at the drive's teeth (T div 2) key, with the head's channel, D value . value alone, as its mutant; it replaces the alignment of 2026-10-25 (ALGEBRA.md line 1592, the form less the pressure), and TW-S1 keeps its weight 6 and its "light has no trace", its consequence clause going (Sofer's to cancel in place); the act reads the file's trace key nowhere, so whether the key stays in the format is the owner's.

26. **(z) The work made lighter. APPROVED (the owner's word of 2026-10-29, 02:5x UTC, in translation: "Approved", on the Boss's proposal; #2187 6486562433).**
    - **The tests' room by file:** each Tensor24 test file holds one budget in tools/tests_shape.py's ROOM, grows within it with no new entry, and is refused above it.
    - **A hostile review's report alone in the repo:** its probes stay in the reader's scratch, each named in the report.
    - **One hostile reader per stage, and the four approvals per stage** (section 12, item 3): a review's follow-up commits are read by Sofer, David and Animate, and the three branches move at a stage's end. Amended by decision 27: a hostile reader and the architect every two stages.
    - **The stage tests merged:** the laws that the test files of stages 2, 3, 4 and 7a repeat stand once, each still failing on its own mutant.
    - **One checker of formats:** the files' format as one table, and one checker that names every departure.

27. **(aa) The runner first, the act at the top cancelled, the doubler's hold, and a hostile reader every two stages. APPROVED (the owner's word to the Boss of 2026-10-29, 06:3x UTC, in Hebrew; in translation: "2 yes. 3 cancel, it is not a local law. 4 as recommended. Two stages are enough, and the architect to approve too that everything stands"; on the Boss's four questions).**
    - **The runner first:** stage 10 is built after stage 7, before stages 8 and 9, so that a run from the three files to the record stands first: light, matter and the time gear, with no click.
    - **The act at the top is cancelled:** it is not a local law. The top is the act's own turning point by the spring, and each bang goes on from where the last left it; the clicks carry the arrow. T = J K stays each kind's time reversal (item (s)), which the tests read and no act applies. The law's fifth act at the top (ALGEBRA.md line 1602) is Sofer's to cancel in place, the former sentence kept by name and dated.
    - **(g), the doubler's hold, as recommended:** light at the speed 1/sqrt(6), gravity's reach of the order of sqrt(Gamma / 12) Meshes; 7b's table is written so.
    - **The reviews:** a fresh hostile reader every two stages, and the architect approving at each that the whole stands; Sofer, David and Animate approve every stage, and the three branches move at the end of each pair of stages, after the reader and the architect.
28. **(ab) Bell at a distance on two boards. APPROVED (the owner's word to the Boss of 2026-10-29, 07:4x UTC, in Hebrew; in translation: "The two boards."; on the options of the big picture, TENSOR24-THE-BIG-PICTURE.md section 10.1 on toys-5 3f48ceef7).**
    - **The decision:** every Node-clock holds two boards, one forward from the bang and one backward from the clicks to come; the backward board is the one act run back. A detector's choice and outcome ride the backward board back along its twin to the birth, and the other twin's forward board brings them to its detector: every read within the six neighbours, so **locality is never broken**.
    - **Retired:** the closure across space at the board's cone as Bell's carrier, with its window and Bancal's catch, and item (l).
    - **Kept:** the arrow: the forward board alone writes records.
    - **Owed before the build resumes** (the owner's word of 07:4x UTC: "Stop building the engine for a moment until you close on the final picture. It must be hermetically closed."): the split click in two boards for Born's position, Grangier's g2 = 0, Bell's S and three parties with no signal; a history agreeing with itself at both ends, its existence, its uniqueness and the runner's search for it; no signal into the past; the state and the cost; the aim of ever more complex clocks kept.
29. **(ac) The product draw, the take by way (b), and the two boards switched in the universe file. APPROVED (the owner's word to the Boss of 2026-10-29, 08:3x UTC, in Hebrew; in translation: "Approved.. Reach a coherent picture. And one more thing: activating two boards will be in the universe file."; on the Boss's two questions of 08:2x with David's recommendations).**
    - **The product draw:** the split click draws by the product of the two dials' sizes, sigma_f sigma_b (David's #2187 6491076850): L = SUM_i sigma_f,i sigma_b,i, d = (c + V) mod L, the rank count over the cumulative products. With the future silent, sigma_b alike at every part, it is law 9 exactly, Born.
    - **The take on light's gears, way (b):** one carry of the sweep's linear term at the clicking Node-clock, the miss booked signed in light's kept (DAVID-TENSOR24-THE-TAKE-ON-THE-GEARS.md, toys-5 a21793e86), scoped as the page has it.
    - **The switch:** a universe runs the backward board or does not, and its file says which. Off: the forward board alone, sigma_b = 1 at every part, law 9 as written, the runner forward alone. On: both boards, the product draw, the runner's sweeps finding the history that agrees with itself, each sweep local. The key's form is the picture's (proposed: one whether among the universe's integers, `backward`, 0 or 1, named in the record's header).
    - **"Reach a coherent picture":** Sofer the one writer of the big picture; David's sections to the decisions, the switch's two runs side by side; a fresh hostile reader and the architect on the whole for coherence when it is called complete; then the owner's word to resume the build.
30. **(ad) The clicks lengthen the future forward, and the picture is two boards. APPROVED (the owner's word to the Boss of 2026-10-29, 10:0x UTC, in Hebrew; in translation: "4: the clicks lengthen the future forward. So one board or two, in your view? We chose two boards: bring everything into them... and show a closed picture. In the code the Node-clock is to be doubled so as not to duplicate code, no? Because they do similar acts... and maybe it is really two nodes in nature?"; on the Boss's question 4 of 09:4x and his verdict of 09:3x, #2187 6493239195).**
    - **The future rich by the clicks:** his phrase to David of 08:52 reads forward. A whole click that turns bound matter into light strengthens the time gear's push (rho + 3p, light twice), so the top comes later and the clicks give the future more time (the Boss's toy, tensor24-review 00c0573a4; on 7b's act, bb2ad4405). No weight is set on the future's boundary, and the principle's item (9) stands as written.
    - **The picture is two boards:** every phenomenon is brought into them and named by its board and its click (the big picture's 10.3), with the draw where the parts were one, ordered by cause (B). The switch of decision 29 stands: off, the forward board alone, Bell at a distance and Grangier out by name.
    - **One code for both boards (the Boss's design on his question):** the Node-clock doubled, each state array with one more axis of two, the forward half and the backward half; the forward half steps by tick and the backward half by untick, the same act run back, both built and exact; the split click reads the product of the two halves' sizes along that axis, and the 24 act on both halves alike. Owed: whether the same tick on a time-reversed copy steps the backward half exactly (T S T = S^-1 on 7b's whole state), which would leave one function for both halves.
    - **Two nodes in nature:** physics already computes real-time quantum dynamics on a forward and a backward copy of every field (Schwinger, 1961; Keldysh, 1964) and with two states (Aharonov, Bergmann and Lebowitz, 1964). No click reads the backward half, only the correlations it makes at the split click, so one Node-clock with two dials and two nodes at one place read the same in the record; the wording is his.
31. **(ae) One board with doubled Node-clocks, and the clicks derived exactly from the full picture. APPROVED (the owner's word to the Boss of 2026-10-29, 10:0x UTC, in Hebrew; in translation: "Better to see it as one board with doubled Node-clocks, which simulates a double board, no? Let the clicks be derived exactly from the full picture."; on decision 30's design).**
    - **The view:** one board, one geometry, one set of Meshes and one great clock, every Node-clock doubled into a forward half and a backward half. It is decision 28's two boards on one Node-clock as the build holds them: every read within the six neighbours, each half reading the same half of its neighbours.
    - **The whole click (how much), on the doubled Node-clock:** the forward half's drive carry at the train's winding writes the record; the backward half confirms it as a check on the forward record and writes nothing (Animate's reading 12).
    - **The split click (which), on the doubled Node-clock:** at the Node-clock where the parts were one, the backward half brings the basis of the clicks to come (the detectors' frames, or the absorbers' takes) with its own weights sigma_b; the forward half's hand read in that basis gives sigma_f, each the Gaussian norm of a whole-number overlap; the draw is law 9's over sigma_f sigma_b, ordered by cause (B). For separate parts this is decision 29's product of sizes, Born where the future is silent; for a pair it is the squared overlap of the shared hand with the two frames (tensor24-review 70ea1991b: S = -82/29, nothing typed but the frames). One rule for both.
    - **Status and owed:** stated on the doubled Node-clock and shown beside the engine (David's product draw, toys-5 f3661f524; joint_from_norms.py); owed on the act's own arrays at stage 9, with whether one tick steps both halves (decision 30's check of T S T = S^-1).
32. **(af) The order to the build: the closed picture, three fresh reviewers, then the engine. APPROVED (the owner's word to the Boss of 2026-10-29, 10:1x UTC, in Hebrew; in translation: "And to show the clocks' complexity rising... and everything we see, from the bang until now... And on all of it, bring an architect and a hostile mathematician and physicist after you have closed the picture, then unify it into the engine. Confirm that you understood.").**
    - **What the closed picture shows:**
      - the clocks' complexity rising: within one swing from the bang to now, and from swing to swing, as the counts of the big picture's 11.2 beside their controls;
      - everything nature shows from the bang to now, epoch by epoch, each with its board, its click and its status word; an epoch the engine does not reach is named a contradiction with nature, by name.
    - **The reviewers:** when Sofer calls the picture coherent and the four approve it by name, a fresh architect, a fresh hostile mathematician and a fresh hostile physicist read the whole, and their findings are answered before the next step.
    - **Then the engine:** the picture is unified into the engine in the plan's order (the doubled Node-clock's backward dial, stage 9's two clicks, the runner's passes, then 7c, 8 and 11), each stage under decision 27's rule of reviews; the owner is told when it starts.
    - **Until then:** no engine code; probes beside the engine alone.
33. **(ag) No switch: the Node-clock is always doubled. APPROVED (the owner's word to the Boss of 2026-10-29, 10:3x UTC, in Hebrew; in translation: "No need for a flag..."; read by the Boss as the universe file's switch of decision 29, and so told to him).**
    - **Retired:** decision 29's third part, the universe file's whether `backward`. No file switches the backward half on or off; every Node-clock of every world is doubled.
    - **The law's gain:** **The one Node-clock** (ALGEBRA.md line 504) needs no exception: nothing of the Node-clock is switched by any file. The gate's keys list drops INTEGERS.backward and UNIVERSE.integers.backward, and the record's header names no switch.
    - **What stays:** the product draw and the take by way (b), decision 29's first two parts.
    - **The control that the switch gave** (the big picture's 10.2, test 5) becomes a test of the engine: a backward dial held silent, sigma_b alike at every part, draws by law 9 exactly, Born, and leaves every count of the first aim as the forward board alone gives it.
    - **The one tick:** decision 30's check is in (tensor24-review 9a7db7432). The backward half is the same tick on the mirrored state (T S T = S^-1, exact on 7b's whole state), with the forward log's fire as its mask where counts are staggered.
34. **(ah) One Node-clock, one hand, run both ways. APPROVED (the owner's word to the Boss of 2026-10-29, 10:3x UTC, in Hebrew; in translation: "The picture closes without a flag. It is not really a doubled Node-clock, is it? Because there is one hand..?"; on decision 33 and the one tick).**
    - **The picture:** each Node-clock has one hand, its gears' state. The backward run is that same hand run back, the same tick on the mirrored state (9a7db7432), and no second clock; in a history that agrees with itself its gears retrace the forward run's tick for tick.
    - **What the backward run carries:** no hand but a tag, the basis and the weights of the clicks to come (the detectors' frames, the absorbers' takes, sigma_b per part), carried back one Mesh a step to the Node-clock where the parts were one.
    - **The split click** is where the forward reading of the one hand meets the tag that came back: law 9's draw over sigma_f sigma_b, ordered by cause (B). The whole click and the record are the forward run's alone.
    - **So:** decisions 28, 30 and 31 read as one Node-clock with one hand, run forward and back; "two boards" and "a doubled Node-clock" are the run's two directions, and the new array is the tag alone.
35. **(ai) Nothing declared: every particle is to appear by itself in the clicks. APPROVED (the owner's word to the Boss of 2026-10-29, 10:5x UTC, in Hebrew; in translation: "You wrote 'declared', but declaring is forbidden: the muon, the tau, the quarks, W, Z and the Higgs, not derived, some declared in the file and some open. They are to appear by themselves in the clicks."; on the Boss's report of the documents' check).**
    - **The rule:** no particle, mass or coupling is declared. A universe file that declares one, a train's pinion standing for a particle's mass, breaches **nothing declared**; it is no status. Every particle is to appear by itself in the clicks: a stable composite clock that the clicks build from the one seed, its mass its own beat, read on the record.
    - **The status words change:** "declared by the file" leaves the ledger. Each such number reads "not yet seen in the clicks", with the breach named wherever a file still declares it (the head's test worlds' pinions, the example universes' trains).
    - **The seed:** small clocks all alike (the principle's item (9)), one train; the kinds by the ladder (all five from one A1 train within three steps, DAVID-TENSOR24-THE-LADDER-AND-FUSION.md on toys-5); the masses as the composites' beats; the generations, Planck's key and a large number sought with them (the Boss's three probes, running).
    - **Owed:**
      - Sofer: what the universe file may still hold (the board, the seed, the scale) read against nothing declared;
      - David: the ladder's spectrum from one seed, the composites and their beats;
      - Animate: the record's reading of a particle, a stable composite's beat and windings;
      - the Boss: the act's own numbers and the three probes.

36. **(aj) The same clock and the same ruler for every act, the time gear among them: no exception to a generic rule, and no contradiction with nature. APPROVED (the owner's words to the Boss of 2026-10-29, 12:0x UTC, in Hebrew; in translation: "2 matches the usual generic rule. How did a rule that makes an exception get in at all?" and "3: there is no contradiction with nature."; on the Boss's report of 11:5x, items 2 and 3).**
    - **The rule:** **The same clock and the same ruler for every act** (ALGEBRA.md line 693) holds with no exception. The time gear's teeth read the ruler at its own count (W = Z_b + Z_n and W+ = Z_n + Z_+, Z = T Y^4 div Gamma^4), and its spring reads Y^2, as a massive train's do: David's road A (6495164657). It replaces "the time gear stands on its own teeth (T, 1) ... it never reads the ruler, so no clock stops": decision 25's "the drive at fixed teeth", the picture's section 4, and runner/load.py's gearing, where the time gear's row reads no ruler.
    - **What it gives** (derived in toys, owed on the act): with X = e^(4U) the time gear's momentum is W U' = X'/4, so its act is X'' = 4F, the volume's law in the time gear's own momentum, the 4 being 3 + 1. Its attractor is Friedmann's form for any mix of light and matter, with a stiff mode for the bounce and the spring as a slowly varying dark energy below its center (6495923568). Postulate 6 holds: the force stays linear in the count, and the statics are untouched.
    - **No exception to a generic rule:** an exception enters only where a symmetry derives it. An engineering problem that seems to force one is booked as open by name, and the exception does not enter. This one came in for two engineering problems, neither a law:
      - the step that reads its own count is implicit (the ruler as the gear could not run back, decision 25). It is to be solved within the rule: the step on the volume, explicit and reversible (the Boss's probe). A monotone search for the stride is struck (Sofer's A5, 2026-10-29): it is a loop and an ordering comparison, which Postulate 5 and the one pass refuse;
      - the ruler's end (past the stopped load the rate rounds to 0; David's course page, section 4). There the carry's remainder holds the impulse, so the clock slows and does not stop.
    - **No contradiction with nature:** no road C. What road A leaves stays open by name and is to close in agreement with nature, never booked as a contradiction:
      - the tensor waves: the spatial block's shears, E + T2, the other family;
      - the late acceleration: the spring's door, the act's ratio of D0 to the push;
      - the horizon: N = e^-U is never 0 (David's shadow test, 2 e M against 5.20 M);
      - the large-number relation, if the swing is the cosmic cycle;
      - the fixed point probe's ratchet: on 7b light's amplitude rises at each bang until the bang is lost, where nature's light keeps its number through an expansion.
    - **Owed:**
      - the Boss: road A on the act's own run (q per era, the run back, no clock stopping, the ruler's range, the wells, the cone); the sweep of every act's coefficients against line 693, running; the coupling rows' strength through the ruler, the second exception found (11:3x);
      - David: the late acceleration's door and the shears, in clocks;
      - Sofer: the picture's sections 4 and 12.3 brought to the rule, and "no exception to a generic rule" read into the method.

37. **(ak) Masses are measured only in clicks. APPROVED (the owner's word to the Boss of 2026-10-29, 12:0x UTC, in Hebrew; in translation: "4. Where do the masses enter at all? Masses are measured only in clicks, no?"; on the Boss's question of 11:5x, item 4: may a probe or a test lay a measuring train with a mass).**
    - **The rule:** a mass is no input of any file, test or probe. It is measured, at the clicks: the beat a clock shows at its clicks, read twice (its beat at each click and its windings booked there, agreeing through the one key; Animate's reading, 6494943325, item 3). It is the shadow's rule for one parameter: the board holds no parameter of nature (the owner's word of 11:5x).
    - **Where a mass enters as built:** in one place, a train's pinion in the universe file. runner/load.py lays its spring 12 (den - pinion) G^2 Gamma^2, so light at pinion = den has none. A pinion below den is a mass put in by hand, a breach of decision 35.
    - **What follows:**
      - every train a file lays is the seed, at pinion = den, and a train's spring is never an input;
      - tests and probes lay no massive train. The Boss's probes' "matter", the time gear's test's "dust" and the reviewers' toys are breaches named, frozen until the build replaces them;
      - a massive thing exists only where the clicks build it from the seed, and its mass is its beat read at its clicks;
      - the time gear's spring, the clock's one notch from den and Gamma, is the board's own and no particle's mass.
    - **What it makes decisive:** whether the act builds massive composites from the seed at all (David's ladder, its spectrum from one seed). Without them there is no matter and no matter's push; they are the next thing the clicks must show.
    - **Owed:**
      - David: the ladder's spectrum from one seed, now first;
      - Animate: the mass reading on the record, as the definition;
      - Sofer: the law's line 35, and the gate refusing a pinion below den in any file (on the owner's word);
      - the Boss: when the build resumes, the files' format without a mass, and the probes and the tests on the seed alone.

38. **(al) The Node-clock is one generic, simple node: every exception, restriction, block and fake out; an added family is allowed where it is generic. APPROVED (the owner's words to the Boss of 2026-10-29, 12:4x UTC, in Hebrew; in translation: "There is no problem with another family, because it is generic. But note that all the exclusions and restrictions ruin it for us, because then the generic law cannot be reached. When you put in a generic law it runs into all kinds of restrictions and blocks; that is why we throw out blocks and restrictions, there is none of that. All the fakes the writer has now found, throw them all out. The node is a generic and simple node. Confirm that you understood."; on the Boss's confirmation, "Approved. Reach a coherent picture within an hour, and go on to close the engine with the final picture.").**
    - **The rule:** one gear type; rows that differ only by data arrays made by one formula from the row's own numbers; one pass of the tick; every row reading the ruler at its own count; no row found by position, no mask, no clamp, no per-row constant and no second mode. An engineering problem meets the generic form, never a block: the implicit step by the volume coordinate (a monotone search struck, Sofer's A5: a loop and an ordering comparison), and the ruler's end as a variable of the files.
    - **Out, all of them:** the thirteen places of the keeper's reading (BIG_PICTURE.md 4.1, as he corrected it at 12:39: eleven standing after decision 36) and the Boss's sweep (6496744667, item 4).
    - **An added family is allowed where it is generic:** the same gear type, the same law, the same clock and ruler. So the great clock may be the whole metric, one family per part the 24 splits it into (the lapse and the ruler, A1; the shift, T1; the shears, E + T2), each with the one law and its own part of the one tensor (the Boss's road (II), 6496744667); and a rate family, the Higgs's place, may stand if the clicks need it (the Boss's probe).
    - **The order:** a coherent picture within the hour (by 13:4x UTC); decision 32's three fresh reviewers read it at once; then the engine is closed to the final picture.
    - **Owed:**
      - the Boss: the generic Node-clock beside the engine with the uniformity test (the time gear laid as an ordinary train gives the same record bit for bit, and permuted trains permute the record and nothing else), then the engine;
      - David: which of the time gear's stretch, kick and drive teeth are the clock's own by a symmetry, and road (II) in clocks;
      - Sofer: the picture to the rule (4.1's twelve out, the great clock as the whole metric) and the question of a two spelt 1 + 1;
      - Animate: the record without the turnover line.

39. **(am) The great clock is the whole metric, road (II): one law for every part, each pushed by its own part of the one tensor, the board's counts free clocks; the clicks see general relativity exactly. APPROVED (the owner's word to the Boss of 2026-10-29, 13:4x UTC, in Hebrew; in translation: "I approve", on the Boss's recommendation; before it, his words: "What is more generic in David's finding, what orders everything in the clicks, and in the board it is not seen... Think clocks... If it is exactly relativity, that is interesting.").**
    - **The rule, in clocks:** every Node-clock holds the metric's ten gears, the parts the 24 split it into: the rate (the lapse, A1), the length (the ruler, A1), the lean of its "now" toward its neighbours (the shift, T1, frame dragging) and the stretch that differs by direction (the shears, E + T2, gravity's waves). Every one is an ordinary family of the one gear type under decision 38, with one law, the Gauss law of its own count through the four-dimensional measure, in the wave form.
    - **The sources:** each gear is pushed by its own part of the one stress tensor of the trains' books (David's mend, 6497717375: the books' tensor, not the force form): the rate by rho + 3p (the owner's word of 06:1x), the length by rho - p, the lean by the momentum's flow, the shears by the stress's shear part. No source is chosen gear by gear: the 24 split the tensor as they split the metric.
    - **The board's own counts are free clocks:** d_mu (sqrt(-g) g^(mu nu)) = 0, no source pushes the tick or a Mesh's place. So the tick's weight h^3/N is still in time where the shift is 0, and every gear's step is explicit and runs back.
    - **What the clicks see:** general relativity exactly, in harmonic coordinates that no one measures: Friedmann's course with light and matter at their true weights; gamma = beta = 1 (gamma derived from the free count, h N = 1 the static field's identity, line 1841 read so); waves at light's speed with two polarizations; frame dragging. A stored energy that does not move pushes the length: the cosmological term's door, with nothing typed.
    - **The board's cost, not seen:** under the free count the lapse rises as a^3, so the board must span the rates the course needs: (2 Gamma)^(1/6) >= 1 + z of the light elements (about 10^9) asks Gamma of about 10^54 (David, 6496879911, item 4). Gamma is the board's number and no one measures it, so it is a demand on the board and no contradiction (decision 36).
    - **Road A** (decision 36) is the one law's uniform face with h N = 1; decision 39 keeps its rule (every gear reads the same clock and ruler) and frees the length from the rate.
    - **Owed:**
      - the Boss: the act's run of the ten gears (the two A1 first: run back exactly, q per era, the wells add), then the build's G2 and G4;
      - David: E's whole basis that the 24 permute (his mend), and the swing under the free count;
      - Sofer: the picture and the law's line 1841 to the rule;
      - Animate: the record's readings of the course, the waves and the drag.
40. **(an) The final picture approved and the build resumed: finish a generic engine; the Boss's recommendations (a) to (g) go in where no fake is found in them; only the Boss writes engine code and only Animate writes the decoder. APPROVED (the owner's words to the Boss of 2026-10-29, 15:0x UTC, in Hebrew; in translation: "Start. Go with the recommendations if there are no fakes in them. Finish a generic engine. Only you write engine code. Only Animate writes the decoder. Confirm that you understood."; the Boss confirmed. Before it, his words of 14:4x UTC: "Relativity has no links like ours... relativity is in the clicks, it is not in the board." and "The 24 breaks with the odd tooth... the light is not in the clicks.").**
    - **Relativity is in the clicks, not in the board** (the law's line 1507 said again): the board keeps its links and its own generic law, and what must be relativistic is the shadow. Decision 39's "the clicks see general relativity exactly" reads so: the requirement is on the record (q per era, the waves' speed and polarizations, gamma and beta, the shadow and the ringdown, the area law, the frame statistic), and "general relativity exactly on the board" is withdrawn. **The light is not in the clicks:** light lives on the board, the clicks are takes, and light alone never clicks.
    - **The recommendations, approved where no fake is found in them.** A fake is an exception, a declaration, a bound, an `if`, a typed number or a row apart. Each is checked before it is built, by the Boss on the code, by Sofer's gate and by a hostile reader; one in which a fake is found is not built and goes back to the owner.
      - (a) **Gravity gravitates:** every gear is pushed by the whole tensor of the books, the gears' own books included. This is decision 38 read on the gears: they are ordinary families, so their books are books like any train's, and leaving them out is an exception. The clicks then see full general relativity, horizons included; "the wells add" (Postulate 6) and line 1507's departure at the second post-Newtonian order hold at the first post-Newtonian order alone.
      - (b) **The slot rule:** a full slot refuses after the split click's draw, and the refused quantum goes back to its giver by 5.1's books line. "A full slot weighs 0" is withdrawn: it signals faster than light (measured: the clicks audit's joint_band.py, Animate's hand_slot.py).
      - (c) **The lapse is an ordinary family** of the one gear type (form B); the free count's tie is a residual the run measures, not a law the step imposes (the architect's B1).
      - (d) **One drive for every row:** the source clause's per-row drive and line 330's fixed teeth give way to one drive, with the coupling family, at G3 (the architect's B3).
      - (e) **The ruler's read is exact and computed** by the closed list, never a table with a refusal past its range: a bound is an if, line 106 (the architect's B4).
      - (f) **Gamma's role:** "unseen" is deleted. The range comes from den (the rate's resolution) and gravity from the notch, 1/Gamma; the notch's units are to derive (H0, Lambda, BBN, the Lorentz bounds).
      - (g) **The coupling family's steady count** is one quantum per Node-clock (Sofer's question), from the law and not from a file.
      - (h) **The odd tooth** (the odd kind A2, so that S4 goes to A4 and E to 1' + 1''; or the odd den): not chosen; open; it enters no code.
    - **The architect's final pass (15:2x UTC): APPROVED WITH CHANGES.** G0 starts now and G1 on (c), (d) and (e). Five items block G2 and later:
      - N1, the slicing is a law and not a run's choice: one weight w in d_mu ((-g)^w g^(mu nu)) = 0 gives N ~ a^(3w/(1-w)) in the course and gamma = w/(3w - 1) in the static field. w = 1/2 gives f = 1 and gamma = 1; f = 1/3 needs w = 1/4, which gives gamma = -1, and Cassini refuses it. "f chosen by the act's run" is struck. Under (c) the tie is measured and not imposed, so the course's slicing is the law's own, to derive.
      - N2, the books' tensor reads rates: a push that reads the stride must be shown to run back (the fix: a first-order form, each rate in its own slot).
      - N3, the ruler's source rho - p divides by 3. The ten (mu, nu) slots, each pushed by its own component of 2T - eta T, are integral and blind to kinds: the 00 slot gets rho + 3p and the diagonal triplet 3(rho - p) in all.
      - N4, the coupling family's leg is G3's under (d): places 5 and 6 stay named breaches until G3.
      - N5, the record's requirements wait on composites, since light alone never clicks: G2 and G4 test the board's structure, and G5 tests the decoder's rules on records built in memory.
      - On (a): one contraction, local, gated on a toy that stays bounded at lambda = 1/Gamma (the gears' own rates, the three-leg vertex, the conformal mode's sign). On (b): no if, local, no history removed; the backward tick tells a refusal from a take by the state, never by the log.
    - **Owed:**
      - the Boss: G0 now (the gates in memory, the permutation and 24-equivariance tests, no row apart, DECLARE), then G1 to G6 to a finished generic engine, each stage with its tests and a hostile reader; the fifteenth review's and the first architect's owed code changes;
      - Sofer: the law's lines to (a) to (g) (lines 35, 330, 1507 and 1841, the source clause, 5.1 and 5.2's slot case, Postulate 6's "the wells add"), and the gate on every head;
      - Animate: the decoder (D6 to D8: proper time, invariants only, the twin reading, the cone check) and the slot rule (b) in the scheduler;
      - David: (a)'s tensor with the gears' own books in the one law, the exact read of (e), the course's slicing on the act (his hole of 14:4x), and the odd tooth's two readings.

**For the owner's information:** the head's K on twin hands breaks the 24. It is a bug of the head; in the new engine the turnover is T.

## 15. The reviewers, the approvals and where it stands

1. **The second hostile reviewers:**
   - **the physicist:** "The group theory and the algebra hold. The plan merits approval as an engineering plan that names its contradictions, and not as 'nature one to one'."
   - **the mathematician:** once B1 to B3 are fixed, the group theory and the integer step are a sound base. M1, M2, M5 and M6 must close before the first cut.
2. **Where it stands:**
   - the algebra and the group theory stand;
   - the first decisions, (o) and (s), were approved at 14:37 UTC;
   - ruled on items 1, 3, 4, 5, 7, 8 and 9;
   - item 2, Bell with a late choice, stays a contradiction, with (l) for the owner;
   - item 6, the draw's fairness, is OPEN, and closes before (l).
3. **The approvals:**
   - **David:**
     - E signed;
     - A, B and D signed with notes. The lines excluded are named, and none of them is a line the plan stands on;
     - C signed in its scope only, its closure's text on hold;
     - **on the whole plan: YES** (edb27b24d, 6473424362), with two text notes, neither a blocker, both folded.
   - **Sofer:**
     - F passes as a draft, G as a measurement, I as a draft;
     - the law holds the owner's approved (o) and (s) at lines 98, 106 and 1602 since ef9149e94 (14:37 UTC), and his picture of 15:0x at line 106 since 4de7a1b68 (15:31 UTC);
     - **on the head for the owner: APPROVED** (8eaf350f2, 6473828939). The one architect's ruling is right on every point it corrects in his file, and his remaining wording points are folded.
   - **Animate: YES** (edb27b24d, 6473561890), with five text conditions to fold after 16:00, none of them blocking.
   - **The architect:** APPROVED WITH CHANGES (section 11); the one architect's ruling on Sofer's file and the design, one architecture (section 11, items 7 and 11; section 12, item 4).
4. **The research stopped at 15:00 UTC, on the owner's word.** Everything open is booked by name, and closes in the build.
