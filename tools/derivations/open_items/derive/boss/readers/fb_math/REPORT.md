Filed by the Boss from the reader's hand-back, 2026-10-30 (the reader's harness refused the file).

# The hostile mathematician on FWDBACK.md (the escapement)

The reader's report, 2026-10-30. The harness refused to write REPORT.md ("subagents return findings as text"), so the full text is given here for the Boss to file.

**Files.** All probes are in /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/fb_math/
- probe_m0 to probe_m9, each .py with its .txt.
- rerun/ holds the text's five probes, rerun.
- ALGEBRA_main.md is the origin/main copy (2bcf315b6) that the quotes below come from.

**Engine and method.**
- Every number was measured on the t24b engine (gather head 9067de20d), through the frozen fwdback_read/fb_lib.py and scratchpad/edge/edge_lib.py.
- The "model ring" cases run fb_lib's own one-site act at every site, with an integer Laplacian pull of mine. The engine's board cannot hold a standing non-uniform clock, because its 00 row moves.
- Whole numbers only; carry is the one division. Everything ran with python -I -B, so nothing was written into the frozen folder.
- The text's five probes reran byte-identical (6 to 37 s each).

**Messages.** Your pre-restart message with Big Pic's finding never reached me. I checked it as your later message summarised it (item 1).

VERDICT on FWDBACK: NOT PASSED

**What stands:**
- The escapement's algebra. Theorem 2 is a complete proof, and it holds on every state I enumerated.
- Theorem 3, within its hypotheses.
- The 24, locality, and the law's "whether".
- The physics at one Node-clock, which is an identity in proper time.

**What fails:**
- The board where Node-clocks differ. It keeps no momentum, its momentum mode grows, and its 00 row runs the clocks away. The drift the text calls nature's is not nature's.
- The domain c >= 0. It is a price of the physics, not a promise like W >= 1.

## Items

### 1. BLOCKING: the board where neighbouring Node-clocks release on different rounds

The board keeps no momentum there, its momentum mode grows exponentially, and the 00 row riding the escapement runs every clock away. The text calls the drift nature's.

**Place:**
- Section 4: "the lapse gradient's force, nature's d_t SUM pi = SUM N Lap a".
- Section 5, "One cone": "the 00 row needs no law of its own".
- Section 6, item 6.
- Solution24 step 6 ("nature's where the clocks differ") and step 10 ("the 00 row's own law and the cut both retire").

**Derived:**
- (a) Each round, dSUM_x P_x = SUM_x q_x push_x exactly, with P = rest v + r. That is minus the pushes the stood ends did not take. Measured: 0 misses in 400 rounds, every row.
- (b) No fixed weights c != 0 keep SUM c_x P_x. The coefficient of a_z is (Lap(c q))_z, so c q must be constant over the board at every round. That forces c = 0 on the released sites of any round where some sites release and others stand.
- (c) Nature, under a static lapse on flat slices, obeys d_t pi = div(N grad a). It keeps SUM pi exactly: that is the shift's charge, so d_t SUM pi = 0. The board's averaged law is d_t pi = N Lap a, which drops grad N . grad a.
- (d) The round's map preserves volume but is not symplectic where q differs across a Mesh. The kick's Jacobian is [[I, 0], [s Q Lap, I]], which is symplectic iff Q Lap is symmetric, i.e. iff q_x = q_y on every Mesh.
- (e) Two clocks at L_0 and 2 L_0, coupled with k per proper step^2. Their two-round map has the real eigenvalue 1 + mu, where mu^3 + (5k - 2k^2) mu^2 + (5k - 3k^2) mu - k^2 = 0, so mu is about k/5.
- (f) For the 00 row, N = L_0 / L(a) gives d_t SUM pi/N = SUM pi^2 |N'| / N > 0. That is a one-way pump toward depth.

**Measured:**
- Two clocks (probe_m5 B): 37, 9.2 and 2.2 bits per 2000 rounds at k = 1/8, 1/32 and 1/128. The derivation gives 37.4, 9.1 and 2.25.
- A ring of 8 clocks standing at different depths (probe_m5 A), laid at 20 bits:
  - steps of L_0/4, s = 625: up to 407 bits in 20,000 rounds;
  - steps of L_0/10, s = 39: from 21 to 49 bits in 40,000 rounds;
  - steps of 1 percent of L_0, s = 625: from 28 to 39 bits in 40,000 rounds.
- Controls stay flat over 40,000 rounds: the uniform rings at 20 bits, and the act as built on the same rings at 21 bits (probe_m7 A).
- At a 1 percent contrast with s = 39 (probe_m4 C), SUM P and SUM L P wander by up to 9.5 x 10^6 and 9.8 x 10^6 permille of their start values. The uniform control shows 0 at every window.
- On the engine's board (probe_m6, probe_m7 B):
  - probe_fb2's own "varying in space, standing" lay goes from L 52..72 grips to 1743..3395 grips in 400 rounds. Its own 40-round line already shows the top moving 72 -> 96.
  - A ring of 8 goes from 36..40 grips to 2909..3732 grips in 2000 rounds, with the light row going from 66 to 77 bits. The uniform ring stays at 36 grips and 66 bits.
  - The 00 row's SUM P is raised 288 times more than it is lowered over 1000 rounds.
  - probe_fb5 H's lay ("c = 0 and 12 grips") is already at 770 and 838 grips at the round where the text reads its -249,248 grips, and at 3914..4652 grips by round 2000.
- The run back stays exact throughout, and the 24 hold at every one of 200 rounds of the runaway (probe_m8). The defect is in the physics and the books, not the algebra.

**Big Pic's finding, checked:**
- (1) "The Mesh pull at each end's own release rate": this is the mechanism above.
- (2) "98 permille reflected at a lapse step": confirmed (probe_m9).
  - The board's law matches a and grad a at the step, which gives an impedance of omega/N and a reflected flux of ((N1 - N2)/(N1 + N2))^2. At a 2:1 step that is 1/9 = 111 permille in the continuum.
  - Measured: 101 permille (amplitude -318, transmitted 684). The act as built gives 121 permille (-349, 653).
  - So the reflection belongs to the plain Mesh, and both forms share it. Nature's div(N grad a) reflects nothing at normal incidence. The instability and the runaway belong to the escapement alone.
- (3) "A tooth on each Mesh" belongs to the second text. It must make both ends take the Mesh's transfer on one event, which restores the books and the symplectic kick. It must also weight that transfer at the edge's lapse, which removes the reflection. It then has to be measured over long runs.

**Fix:**
- Strike "nature's" and "the 00 row's own law retires".
- Either name the board's law where clocks differ as a price, or mend the Mesh.
- Then rerun the non-uniform lays for thousands of rounds, with the clocks' course and the books printed every round.

### 2. BLOCKING: the domain c >= 0 is a price of the physics

It is not "read by the promise as W >= 1 is today".

**Place:** section 0, last sentence; section 6's heading ("none a price of the physics") and item 2; section 5's "at every depth".

**Derived:**
- Below D = 2 L_0, every round releases, and the turn becomes 2 once tau >= 2 D - 2 L_0. So the escapement can only slow a clock, never run one faster than rest.
- At q = 2 the act is no step: a+ = a + 2q, b+ = 2a - b, r+ = 2r' - r.
- With c = -k, the turn 2 comes at round ceil((L_0 - 3k)/(2k)).

**Measured:**
- At c = -1 (probe_m2), the turn 2 comes at round 9999 (derived 9999). That round gives r+ = -2200, outside [0, 10000), and it does not run back.
- At k = 2, 10 and 1000, the turn 2 comes at rounds 4999, 999 and 9.
- On the example board, the 00 mode about rest breaks the promise at round 0, so it cannot be laid at all. probe_fb3's cone was measured only at 6, 18 and 54 grips.
- One site of a rest clock raised by ONE count breaks the promise at round 2.
- Exhaustively (probe_m1), outside D >= 2 L_0: 40,572 of 82,908 states turn 2 or more, and only 34,692 run back.

**The law's texts:**
- ALGEBRA line 1955: "The one promise is that every divisor is a teeth count of at least 1".
- Today's runner reads only that every fine tooth lies in [0, W). That entails W >= 1, i.e. c >= 1 - rest, about 9 x 10^22 counts below rest.
- L >= L_0 is a second promise of another kind: a floor on a gear's count. Postulate 5 says such floors belong to the files.

**Fix:** put it to the owner as a price: the rest clock must be the fastest clock in the universe, and no 00 wave about it can exist. Alternatively, probe the lever: L_0 = 2 rest m^2, push 4 rest m (the text's "2 rest m" holds only per slot), domain c >= -2 rest m (m - 1). Under the lever the rest clock releases one round in m, so the mirror is not an involution even at rest.

### 3. MINOR: Theorem 1 is an outline

- (C1): the map is injective iff m_out(prev) <= m_in, and onto iff >=.
- (R1) needs the centred tooth. In [0, m) with the flip m - 1 - s, it also forces m_out = m_in within the round.
- "No polynomial gives sqrt(W)" binds only under line 35. With L linear, L(a) + L(b) gives nature's g, and the obstacle moves to the 1/L on the push.
- That branch rests on rd_phys item 1, which argues from one failed construction and is not a proof. As worded, the escapement itself refutes it at one Node-clock.
- "Every form" is too wide:
  - the cut's 00 row divides at a standing dial;
  - TIMEGEAR's register and twin hold two registers, outside the one-tooth hypothesis;
  - their prices (the second cone, the pump, the parting) are not Theorem 1's.
- The escapement itself divides time's push 2 L_0 at a moving dial, so as worded it is inside (H). What frees it is three properties: its carry is first order, its push never exceeds its dial, and its dial stands still on a stood round.

### 4. MINOR: Theorem 3's scope and wording

- Proved within (i)-(iii). On all 291,060 states, mirror o mirror = swap^(q_last + q_next), and the mirror's inverse is the mirror that reads q_next.
- "On a moving clock" should read "on every clock below rest, standing included" (probe_m3):
  - At a standing L = 1.5 L_0, mirror twice is the identity on 100 of 300 states. At 2 L_0, on 0 of 300.
  - mirror tick^n mirror = tick^-n, for n = 1..8, holds on [300, 100, 100, 200, 100, 100, 200, 100] of 300 states at 1.5 L_0, and on [300, 0, 150, 0, 150, 0, 150, 0] of 300 at 2 L_0.
  - The act as built holds it on all 300, for every n, on every standing W.
- "Nothing with a skipping clock can" goes beyond the theorem's hypotheses: every bijection is reversed by some involution.
- On the brief's question (does an exact run back with a non-involutive mirror meet "the run back is the same act on the mirrored state"?): yes per round, but not as the time reversal of motions on a deep clock.

### 5. MINOR: the stated domain is stronger than the proof needs, and the probes sit outside it

- The proof needs D_in, D_out >= 2 L_0, not c >= 0 at both slots. With one slot below 0, 61,740 rounds run back exactly.
- probe_fb1's rising lay has c(before) = -1, so D = 39,999: outside even the proof's domain. It runs back only by the phase of the tooth.
- probe_fb5 D's lay has L(before) = 0.
- No probe reads the promise (probe_m8 d).

### 6. MINOR: the bound in OPEN item 4 is not a bound

- The text bounds the phase by (1/2) ln(L_end / L_start), which is 347 permille of a step at L x 2.
- Measured: 500 permille at the end of the rising course (probe_m8 a).
- The phase is still bounded: the dial reads the clock one proper step late.

### 7. MINOR: "the 2's are the two slots"

- The push L_0 + L_0 is the dial at rest, so it is structural.
- L_0 = rest + rest is the derivative of the square: a unit choice that keeps line 35's one count of c equal to one count of W. It should be named as such.

### 8. MINOR (for the physicist): the 00 row's law is a choice

- The escapement's 00 gear keeps its proper velocity, which is tg_phys's c = 1/2.
- It moves in whole counts per proper step, so tg_phys item 1's lock-in applies.
- So "CHOSEN nowhere" (step 3) overclaims.

### 9. MINOR: the probes' wording

- probe_fb2's "largest drift" is end minus start. Per round it is also 0 on three uniform lays (probe_m4 B).
- "Stepped 0" at c = 0 is a wrong counter.
- "Drift 0 on nine lays" is in fact eight.
- The "varying [60, 70] grips" lay is uniform to the permille.
- probe_fb4, the J case, runs only 6 rounds.

## Item 3: the whether and the other laws (ALGEBRA.md at 2bcf315b6)

**Quoted:**
- Line 35: "no act holds a floor, a bound, a clamp, a mask or a branch".
- Line 106: a mask is "an indicator that zeroes a term above a bound is a bound spelt as a quotient"; and "the turn leaves as an event, a carry to the next clock, ... and the remainder stays on the dial".
- Line 1955: "a whether, a sign, a bound and a choice are sums and products of carries' quotients (... choose(k, x, y) = k x + (1 - k) y)".

**Whether or mask:** a+ = a + q_tau q is choose(q_tau, stepped, stood), with k equal to the escapement's own carry quotient. It gates no term by its own size, and nothing is lost. So it is the carry's whether, not a mask. That holds only while k is a bit, and only the promise guarantees that (item 2).

**Locality holds.** A neighbour reads a stood Node-clock's now slots, i.e. its counts at its last release, both forward and backward. Those stale reads, taken by a Mesh's two ends on different rounds, are the mechanism of item 1.

**The 24:** all 24 turns fix the 00 row with sign +1 (probe_m0), so tau is a site scalar.

## SOUND, with numbers

- All five of the text's probes rerun byte-identical.
- Theorem 2 is proved, and I re-derived (a) to (e). On every state of a one-Node-clock box (rest 3, L_0 6), all 155,232 in-domain rounds run back, with q_tau a bit and tau within D_out at all of them. The forward map has 0 collisions.
- The 24 commute with tick for 200 rounds and with the mirror on 504 of 504 states.
- On uniform clocks SUM P is exact at every round, and at c = 0 the act equals the act as built (40 of 40).
- The physics at one Node-clock is an identity in proper time.
- The book dSUM P = SUM q push: 0 misses in 400 rounds.

## DERIVED / MEASURED / OVERCLAIMED

**DERIVED (stands):** Theorems 2 and 3 within their hypotheses; q_tau is a bit in the domain; 2 L_0 / D proper steps per round.

**DERIVED here:**
- the book identity, and that no fixed-weight momentum is kept;
- nature keeps SUM pi, while the board's law is N Lap a;
- the non-symplectic kick and the two-site eigenvalue;
- the one-way pump in the 00 row;
- the impedance behind the reflection;
- outside the domain, q >= 1 always, and the round where q reaches 2;
- the mirror's inverse.

**MEASURED (stands):** every number the text prints.

**OVERCLAIMED:**
- "no price", "none a price of the physics", and "read as W >= 1 is today";
- "nature's d_t SUM pi = SUM N Lap a";
- "nature's where the clocks differ";
- "the 00 row's own law retires";
- "on light's cone at every depth";
- "nothing is pumped" beyond one site;
- "on a moving clock", and "nothing with a skipping clock can";
- Theorem 1 as the theorem the drafts share;
- the OPEN 4 bound;
- "nine lays";
- "CHOSEN nowhere".

## Questions for the Boss

1. Is a domain that excludes every clock faster than rest a price under "no price"? On the example board, the vacuum's one-count 00 fluctuation leaves it in 2 rounds. If the lever is the answer, it has to be probed.
2. Where clocks differ, which law is nature's: div(N grad a), which keeps SUM pi and gives no reflection, or N Lap a, which is what the act as built and the escapement use?
3. Must the time reversal be an involution? The act as built has one on every standing clock; the escapement only at c = 0.
4. Should every board lay be run for thousands of rounds, with the clocks' course printed, before anything is called nature's?

## Solution24

Steps 6 and 7 are met only at one Node-clock and on a uniform clock. Where the Node-clocks differ, the books, the stability and the clock's own course must be read at every round over thousands of rounds before any drift is called nature's. Step 12 should carry the board's law and the domain to the owner as prices.
