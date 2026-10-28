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
   **CHECKED** (the owner's word of 15:3x UTC, "make sure the engine can really be written with these"; derive/closed_list): the engine's 29 acts, written on a whole number that allows addition, multiplication and the carry alone, each match their plain reference with 0 failures; their code holds no if and no comparison; and 12 of 12 mutants fail. The one promise is that every divisor is a teeth count of at least 1; light's w_c = 0 (M2) and W+ <= 0 (M1) break it until they close, before the first cut. A second promise stands beside it (Sofer, #2187 6476698665): every rate lies between 0 and the full rate, since the beat's k is read as a bit; with one clock at twice the full rate k reaches 2 and the rewind is not exact (his probe on the stage 3 engine). The load refuses a rate above the full rate by name at stage 6, its test a setting at two full rates that must not load.
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
3. **The turnover** (approved).
   - **In the clock:** T = J K on every gear, at the clock's own top, as a carry. The two slots of every gear exchange, and each gear's sign is its source's.
   - **In the tensors:** (a, a-) -> (T a-, T a).
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
- (g) the doubler;
- (w) one bang whose tops part.

(v), the local turnover, is withdrawn.

## 3. The end state

1. **One machine of tensors in integers, all clocks.**
   - Three operations only: multiplication, addition and Rule3.
   - The quotient leaves as an event, and the remainder stays.
2. **A new engine, in new files.** It replaces the head. The head stays beside it for comparison until the switch, on the owner's decision of 09:1x UTC.
3. **Two laws not to be crossed:**
   - **time is a circle:** forward to the top, the turnover, back, and the next bang;
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
4. **The turnover.**
   - **In the clock:** the clock's own act at the top of its time gear.
   - **The second trigger, the floor, is struck by law 11.** There is no trigger at the bottom.
   - **The top:** the weak maximum X0 <= X1 >= X2 is the law's own text (line 1602) and the head's, a comparison that Postulate 5 refuses in engine code. The top as the time gear's carry, q, r' = carry(X - Gamma, X_c - Gamma) with T applied q times as a choice, is OPEN 7 (David, Sofer). The threshold form as first written is refuted: it is an if.
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
   - **at a distance, with a late choice:** the composite clock must click as one (item (l));
   - **a late choice through the time reversal is refuted (BC's verifier):** the exact rewind brings no detector's axis back to the birth. Even with the clicks left undone (o), the next bang's pairs reach S = -82/29 only where their choices repeat;
   - this is a matter of Bell alone. The difference between bangs, through the detector's click, is law 10 (section 8).

## 7. The families and the kinds

1. **A train is a kind plus its integers in the universe file:** the pair, the spring, the couplings and the weight. The engine knows no train's name in nature.
2. **The five kinds of the 24:**
   - A1 (1), A2 (1), E (2), T1 (3), T2 (3); together 1 + 1 + 4 + 9 + 9 = 24;
   - all derived from the six Spokes, with no typed table.
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
   - **how strong:** an integer in the universe file. The couplings stand in the calibre as rows of integers (train, part, train, part, target, strength); the tensors are computed at load from the board's shape, and a row the 24 forbid is refused at load (the owner's question of 15:1x UTC; TENSOR24.md, section 28);
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
   - with a late choice it is a contradiction, until item (l).
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
   - **the kind table:** kinds, in engine/kinds.py;
   - **the tick:** step, with shift and pull, in engine/mesh.py and engine/step.py;
   - **the turnover:** turnover, in engine/step.py;
   - **the click:** click_whole and click_split, in engine/click.py;
   - **every bound a carry:** carry, in algebra/carry.py, and beat, in engine/step.py.
2. **Five folders:** algebra/ (new: Rule3 and the Gaussian integers), engine/, record/, readings/ and runner/, with decoder/ beside them.
   - The runner does not import the engine. A main.py of about 15 lines passes it the engine's functions.
3. **The state:** ten arrays, fixed for the whole run: a, b, r, rd and go for every gear, e for every hand, and ph, tb, tn and the beat count c for every Node-clock, that is, 5G + H + 4 integers per Node-clock (c added by the one architect's ruling, the going per gear by the tie rule). Nothing grows at run time, as line 98 sets.
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
     - one barrier, at the top.
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
    - the turnover's T^q as a choice by the bit q, not a power;
    - law 9's sorted draw as a rank count, with no sort and no law changed;
    - the width: Python integers in numpy object arrays, exact at 112 bits and beyond, int64 refused;
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
3. **Every push needs four approvals,** and then the full check exits 0:
   - Sofer;
   - David;
   - Animate;
   - a fresh hostile reader.
4. **What is built at each stage** (the owner's word to Sofer, 15:0x UTC; the one architect's ruling, section 6). Clocks first, then tensors, then the 24's operations. No line before stage 0; every test is shown failing on a broken copy; the record, the decoder and Animate's converter run in parallel from stage 0.

   | stage | what is built | its test that can fail | what closes first |
   | --- | --- | --- | --- |
   | 0 | the gate amended (algebra/, the closed list in engine/ and readings/, main.py); the three files and their checker; the record's schema; the harness on a trivial engine | the scan refuses a planted if, a literal 2 and a sort; the harness fails on a mutant | the owner's yes on the closed list and the gate |
   | 1 | algebra/carry.py: carry, nonneg, choose, home and flip, forward and at -1 | the carry exact and unique; q(-p) = -q(p) at both parities; nonneg exact across 0 | items (h) and (e), and the tie rule |
   | 2 | one clock: a gear with its fine tooth; beat: the rate dial, the count c, the due and allowed bits, tb and tn | the rewind 20 of 20, both ways; a stopped clock beats, its count advances, its gears stand | nothing |
   | 3 | two clocks over one Mesh: link, the slot read by tn, the arrivals rule; the synchronous pass and random masks | the order test: 40 random masks equal the synchronous pass, rates parted, one clock stopped; its mutant fails | item (u), past or lin |
   | 4 | the board: the six neighbours from the shape, the gather over the Spokes, the scalar light with its spring | the one-Mesh reach both ways; the formula against a naive loop model; equal to the head on the light, act by act | M1 (N, U_j, J, W+ >= 1); the cap's step; F2, F5 and the horizon; the doubler (g) |
   | 5 | the ring: the Gaussian integers, the hand, the twin hand | the ring's laws exact; T T = +1 on a hand, -1 on a twin hand | nothing |
   | 6 | the kinds and the contraction, from the board's shape; the load of the calibre's trains and coupling rows | the characters; a coupling the table lacks gives 0, named by the checker; the rename test | item (a); OPEN 3 before any twin train loads |
   | 7 | the one act on every train alike | the formula test; the head compared act by act, 0 unexplained differences | M1 on every train; the charge |
   | 8 | the 24's operations: the 24 on the state; the turnover T = J K per gear, T^q a choice; tick and untick | the 24 turns bit for bit, a board that is no cube as the control; T S T = S^-1 at every teeth count; the rewind through the top 20 of 20; the bang's spread 0 | (w), OPEN 7 |
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
8. **(g) The doubler's vacuum.**
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
13. **(l) A composite clock clicks as one, wherever its parts are.**
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
21. **(u) The asynchronous read: past or lin.**
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

24. **(x) A candidate big law: the board is dials and their carries** (Animate, 6473326413, ANIMATE-CLOCK-ROOTS.md, reader-5 ab860c82, on the owner's word to her of 15:2x UTC; a candidate big law, with no verifier): each clock's time is the carry of its own dial; clocks that meet share one dial; every carry keeps the kind of what feeds it. Its letters: A, time (the local tick: a fast clock ticks more often, one at rate 0 does not tick, light crosses one Mesh per local tick); B, state (the joint dial held where its clocks meet, so a winding may stand with no direction and the detector's click has something to decide); C, selection (still light lays the singlet, a lead lays the vector along its Mesh). Its toys: local_tick.py (the local tick holds, its rewind exact over 9,600 events, where one tick for all grows past 10^6); kind_kept.py (the singlet and vector lay keep the 24 at 72 of 72 cases, the head's lay at 12 of 72); the families' ladder (a vector light reaches the 24's five kinds by bang 3, all eight with the twins by bang 3 or 4). The owner's to decide with it: the light as a vector (T1, three Gaussian gears). OPEN: law 7's premise; Bell at a distance; the density step's form; the draw's fairness; the joint toy of A, B and C on the one big bang. Recommended: approve as a direction, checked in the build by the joint toy before it enters the law.

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
