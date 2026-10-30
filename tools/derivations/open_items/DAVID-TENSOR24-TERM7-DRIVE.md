# Term 7, the drive: one carry of the source at the drive's teeth, forced by the books, a finer dial for the source

David, 2026-10-30 (the second text, 23:3x UTC), on the owner's word of 11:1x UTC (derive what the Node-clock needs to
close; everything to stand with a hostile mathematician and a hostile physicist), for the architecture document's term 7
("the drive: one wheel carries the coupling's push for every row; q_d, r_d+ = carry(J, T_d, r_d); none of its own: the
clicks do not come from the drive; Rule3's carry at T_d; BUILT at T_d = 1; DERIVED (G3), to confirm under the owner's
rule of 13:0x (section 6)") and for the night's side list, NOT_CLOSED 14: at T_d = 1 the drive is the identity, q_d = J
and r_d = 0 always, so term 7's DERIVED rested on a no-op (g3_math item 13), and what closes it is a probe with r_d
moving. It reads the act on node-live f72067cdf: engine/step.py's drive, kick, act and mirror, the drive's tooth
State.rd within [0, T_d), the drive's teeth Gearing.drive and the kick's Gearing.kick per row. The probe is
derive/david_open/node/term7_drive.py (about 90 s), its output beside it, whole numbers alone, every division Rule3's
carry. The first text (toys-5 3175fdeca) went to a new hostile pair, who refused it: the mathematician on three items
and twelve minors, the physicist on two and eleven. Both found the form, the books, the three identities and the mirror
by parity standing. Big Pic's word (6535643629: the fold stands, and the key's inertia across rows is the canonical
one) is folded here with their items (section 7); section 8 says how the text checked itself.

**The finding in one line:** the drive is Rule3's carry of the row's source at the drive's teeth, and nothing else could
be: the books and Rule3's range for the tooth force it.
- **Forced:** J + r_d = T_d q_d + r_d+ (nothing lost, nothing made) with 0 <= r_d+ < T_d (Rule3's range) fixes q_d and
  r_d+ uniquely, by the uniqueness of the whole division. A tooth bounded to any other window of T_d values gives
  Rule3's drive up to a shift of the tooth; the range [0, T_d) is the law's convention (docs/ALGEBRA.md line 35).
- **Its books, read from outside with the tooth moving:** at T_d / T_k = 1/1, 2/2, 7/7, 2/1 and 7/1 the quotient is
  whole in 200 of 200 rounds, the kick read off the gear's momentum is T_k q_d in 200 of 200, and over the run T_d SUM K
  = T_k (SUM J + r_d(0) - r_d(end)) at every gear: the drive's part of the momentum stays within 4 T_k counts of the
  exact fraction at every round and never drifts.
- **The run back:** the mirror by parity is the carry's own, two identities: an even row's tooth flips, T_d - 1 - r_d,
  and an odd row's is kept, because the odd row's source changes sign under time's reversal. 400 rounds out and back,
  bit for bit, at T_d 1, 2 and 7; flipping the odd row's tooth too fails, and so does keeping the even rows'.
- **A finer dial for the source:** at standing teeth, for a source that reads no pull, the act with the drive at T_d
  and the kick at 1 is, count for count, the act with T_d times the teeth and T_d times the grips and the drive at 1,
  its edge tooth T_d s + 4 r_d + c, at every residue rho0 = (s + 2 W) mod 4 of the edge tooth, with c within
  [-T_d rho0, 3 - T_d rho0] (c = 0 at rest): 0 of 10,000 rounds differ, Mesh-less and with Meshes, and at the residue
  3 with c = -21 and -18; c = -22 parts. So the drive divides the source's strength by T_d against the gear's inertia
  and its grips, exactly in the counts, not on average.
- **No condition of its own:** inside the act's two passes (a first drive on J1 alone feeds the metric's push J5) the
  drive's run back holds at every T_d when J5 reads no row it pushes and J5's parity under the mirror is its target
  row's, the act's own hypotheses. When J5 reads a row it pushes, the run back fails only in a tick where the share
  the first kick misses carries a read momentum across a turn of the rest dial, at T_d = 1 as at any other; a drive
  above 1 makes that share smaller.
- **Not claimed:** the value of T_d on any row. Each strength's own term sets it, as term 5's books do for B6's dial on
  the square's rows. The drive clicks nothing.

## 1. In clocks

- **The wheel.** Each gear row at each Node-clock has one drive wheel beside its gear. Every round the wheel takes the
  row's source J, a whole count (the plan's contraction of whole readings and whole factors, and the metric's push),
  turns by the whole turns of its teeth T_d that J and its own fine tooth make together, and keeps the rest as its fine
  tooth r_d, at most T_d - 1. The kick hands the turns to the gear: K = s T_k q_d, s the stretch (1 throughout this
  page), T_k the kick's teeth.
- **Why a wheel.** The gear takes a whole push each round. A coupling weaker than one count a round per count of its
  source cannot be a whole push in every round; the wheel carries it whole over many rounds and loses nothing, as the
  gear's own edge tooth keeps the velocity's fraction.
- **The force's path.** At T_d = 1 the wheel is the identity: q_d = J and r_d stays 0 (g3_math item 13). On f72067cdf
  every row the loader lays stands there; from node-live 575973a20 (B2b) the loader lays T_d = 2 on the square's 00 and
  ii rows (term 5's half), and there the tooth moves in the shipped worlds (decision 40 (d): one drive for every row).
- **A finer dial (section 2.5).** A drive of T_d teeth is the gear's own edge dial made T_d times finer for the source
  alone: for a source that reads no pull, the gear with the drive at T_d is the gear with T_d times the teeth and T_d
  times the grips, the source unscaled, count for count. The drive is the source's strength against the clock's
  inertia, and nothing else.
- **Back in time.** On an even row, a count time's reversal pivots on, the wheel turns back the same turns with its
  fine tooth flipped, T_d - 1 - r_d. On an odd row, the metric's 0i slots, whose index pair holds one time index, the
  source changes sign under the reversal, the wheel turns back the negated turns, and its tooth is kept.

## 2. In the algebra

### 2.1 The form, forced

- **Statement.** Let J and r be whole numbers, T >= 1 and 0 <= r < T. Among maps (J, r) -> (q, r+) to whole numbers,
  the books J + r = T q + r+ and the range 0 <= r+ < T hold for exactly one: q = floor((J + r) / T), r+ = J + r - T q,
  that is (q, r+) = carry(J, T, r).
- **Proof.** If T q + r+ = T q' + r+' with both r+ and r+' in [0, T), then T (q - q') = r+' - r+ lies strictly between
  -T and T, so q = q' and r+ = r+'. Existence is Rule3's carry.
- **So** the drive's form is not a choice: the books (the source neither lost nor made) and a bounded tooth give it, and
  Rule3's range [0, T_d) is the law's convention for a remainder (docs/ALGEBRA.md line 35: the carry, n + r = q d + r'
  with 0 <= r' < d). A bounded tooth alone fixes the drive up to a shift of the window: any window of T_d tooth values
  gives a unique drive. The law's line 100 writes a centred carry, as step.split's edge tooth is centred; the drive's
  tooth takes Rule3's range.
- **One drive per row,** carrying the row's whole source J = J1 + J5 (decision 40 (d); step.act): a drive per term
  would keep a tooth per term, and the sum of their quotients differs from the quotient of the sum by up to the number
  of terms (less one with every tooth at 0), more state for no gain. One drive per row scales every term on the row
  alike (the physicist; 575973a20's loader notes the notch rides the same dial).

### 2.2 The books over a run

- Summing J(n) + r_d(n) = T_d q_d(n) + r_d(n + 1) over the rounds n = 0 to N - 1:
  T_d SUM q_d = SUM J + r_d(0) - r_d(N), and with K = s T_k q_d, T_d SUM K = s T_k (SUM J + r_d(0) - r_d(N)).
- Since 0 <= r_d < T_d at every round, |T_d SUM K - s T_k SUM J| <= s T_k (T_d - 1) at every N, not on average.
- **In the momentum.** The edge carries the gear's momentum P = 2 D (a - b) + s (D = W(b) + W(a), s the edge tooth)
  to P+ = P + 4 push exactly, the push s F + K. So the drive's part of the momentum after N rounds is 4 SUM K = (4 s
  T_k / T_d) SUM J + 4 s T_k (r_d(0) - r_d(N)) / T_d, within 4 s T_k counts of the exact fraction at every round: a
  bounded phase, never a walk.
- **Probe (a):** at T_d / T_k = 1/1, 2/2, 7/7, 2/1 and 7/1 on a cube of 3 with three rows (two even, one odd), 200
  rounds each: q_d = (J + r_d - r_d+) / T_d whole in 200 of 200; the kick read off the momentum, (P+ - P - 4 F) / 4,
  equal to T_k q_d in 200 of 200; T_d SUM K = T_k (SUM J + r_d(0) - r_d(end)) at every gear; r_d+'s range is the
  state's (State.rd within [0, T_d) by Rule3's carry). **Probe (e):** at T_k 1, read at the run's end, T_d SUM K -
  SUM J is within -1..1 at T_d 2 and -6..6 at T_d 7, inside the bound -(T_d - 1)..T_d - 1.
- **Probe (b), the tooth moving:** rounds of 200 in which some gear's r_d changes, per row (even, even, odd): 0, 0, 0 at
  T_d 1 (the no-op); 200, 200, 0 at T_d 2, the odd row's spring pushing by even counts (a spring's push -2 f x is even
  whatever f is, so the probe ties the even rows by an odd factor); 200, 200, 200 at T_d 7.

### 2.3 The mirror by parity, from the carry's own identities

Let carry(J, T, r) = (q, r+), with 0 <= r < T.
- **The flip:** carry(J, T, T - 1 - r+) = (q, T - 1 - r). Proof: J + T - 1 - r+ = J + T - 1 - (J + r - T q) =
  T q + (T - 1 - r), and 0 <= T - 1 - r < T.
- **The sign:** carry(-J, T, r+) = (-q, r). Proof: -J + r+ = r - T q, and 0 <= r < T.
- **The run back.** untick = mirror . tick . mirror (step.untick). After a forward round the mirror swaps an even row's
  slots, so the back round reads the forward's now slot again, and swaps and negates an odd row's, so it reads the
  forward's now slot negated. Wherever the source is kept under the mirror on even rows and negated on odd rows, which
  the act's own run back already needs (J's potential even in the odd rows' counts), the back round's drive reads:
  - on an even row (J, T_d - 1 - r_d+), which by the flip gives (q_d, T_d - 1 - r_d): the same kick, which runs the
    gear back on its swapped slots, and the mirror returns the tooth r_d;
  - on an odd row (-J, r_d+), which by the sign gives (-q_d, r_d): the negated kick on the negated counts, and the
    tooth r_d, which the mirror keeps.
- **So** the drive's tooth comes back bit for bit and adds no condition to the act's run back. The law's mirror in
  step.mirror flips the drive's tooth on even rows and keeps it on odd ones, as its docstring says, by the sign law.
- **The mutants fail,** since the identities fail with the other choice: carry(-J, T, T - 1 - r+) is not (-q, r) and
  carry(J, T, r+) is not (q, T - 1 - r) in general.
- **Probe (c):** 400 rounds out and 400 back by untick on the cube of 3, the start returned bit for bit at T_d 1, 2 and
  7 (every tooth moving at T_d 7; at T_d 1 none moves, and at T_d 2 the odd row's does not). **Probe (d),** at T_d 7:
  the law's mirror True; the odd row's tooth flipped too, False; the even rows' tooth kept, False.

### 2.4 The 24's turns on the drive's tooth

- **The negation:** carry(-J, T, T - 1 - r) = (-q, T - 1 - r+). Proof: -J + T - 1 - r = -(T q + r+) + T - 1 =
  T (-q) + (T - 1 - r+).
- A turn of the 24 that negates a row negates its count and its source, the potential being kept by the turn. By the
  negation the turned act equals the act turned when that row's drive tooth flips, T_d - 1 - r_d, provided the rows a
  turn exchanges carry equal T_d, T_k and s, uniform over the sites it moves: the twisted action of the 24 on the state
  (NOT_CLOSED 25; A2's engine test at T_d = 7 on every row: 24 of 24 turns, and 3 of 24 with the teeth kept).
- **Probe (h):** the three identities, the flip, the sign and the negation, at every T_d from 1 to 11, J from -60 to 60
  and r_d within [0, T_d): 7,986 of 7,986 each.

### 2.5 The finer dial, stated and proved

- **Statement.** Take a gear row at standing teeth W (its dial 2 D = 4 W at both edges), grips g on its Meshes, the
  drive at T_d, the kick at 1 and the stretch at 1, its source J, its edge tooth s and its drive tooth r_d. Take the
  same row at the teeth T_d W, the grips T_d g, the drive at 1 and the same source J, with the edge tooth
  s' = T_d s + 4 r_d + c. Let rho0 = (s + 2 W) mod 4. If c lies within [-T_d rho0, 3 - T_d rho0], the two take the
  same count at every round, and s'+ = T_d s+ + 4 r_d+ + c. At rest s = 0 and W = 6 den Gamma^2 is even, so rho0 = 0
  and c = 0 serves.
- **Its hypothesis: the same source.** J must be the same in both acts. A source that reads no pull is: the value legs'
  plan and the metric's push read counts and momenta, which the two acts share. A source that reads the Mesh plan's
  force reads T_d F in the teeth act and F in the drive act, and the two part at round 1 (the mathematician's grips-on
  runs).
- **The residue is kept.** At standing teeth the gear's numerator is n = 4 W (a - b) + 4 push + s, so n = s modulo 4,
  and the split at the dial's half (step.split) gives s+ = ((n + 2 W) mod 4 W) - 2 W, so s+ + 2 W = n + 2 W modulo 4:
  the residue rho0 never changes, every push entering the momentum four times.
- **Proof.** The drive's row: n = 4 W (a - b) + 4 (F + q_d) + s with T_d q_d = J + r_d - r_d+. The teeth row reads the
  same counts, so its pull is T_d F: n' = 4 T_d W (a - b) + 4 (T_d F + J) + s' = T_d n + 4 r_d+ + c. Write
  n + 2 W = 4 W q + rho with 0 <= rho < 4 W; rho = rho0 modulo 4, so rho0 <= rho <= 4 W - 4 + rho0. Then
  n' + 2 T_d W = 4 T_d W q + (T_d rho + 4 r_d+ + c), and T_d rho0 + c <= T_d rho + 4 r_d+ + c <=
  T_d (4 W - 4 + rho0) + 4 (T_d - 1) + c, so 0 <= T_d rho + 4 r_d+ + c < 4 T_d W for every rho and r_d+ exactly when
  -T_d rho0 <= c <= 3 - T_d rho0. So both rows step by q, and s'+ = T_d (rho - 2 W) + 4 r_d+ + c = T_d s+ + 4 r_d+ + c.
  By induction it holds at every round. The window holds four values at every rho0.
- **The mirror.** The mirror sends s to -1 - s, so a tooth of residue rho0 = 0 goes to rho0 = 3; c = 3 - 3 T_d, the top
  of the residue-3 window, is the mirror's image of c = 0 (the physicist's p6, 18,720 of 18,720 cases). So the offset
  form covers the time-reversed states, which the first text's c = 0 did not.
- **Where they part.** With c outside the window the finer dial carries a count at the dial's edge a round apart: at
  the residue 3, c = -22 parts at round 2,507 (probe (f2)). At c = 0 the window holds 0 only while T_d rho0 <= 3, so
  the residue 1 at T_d 2 or 3 does not part (the mathematician's m6). With the kick's teeth above 1 the teeth row needs
  the source T_k J, and the bound above holds only at T_k = 1; the physicist measured count for count wherever s T_k
  divides W and the grips (his p1, up to T_k = W / 6 with Meshes on), which this page does not derive.
- **Probe (f2):** the drive at the teeth 6,000 and T_d 7 against the teeth 42,000 at T_d 1, spring 73 on both, one lay
  on 27 Node-clocks, 10,000 rounds:
  - the edge tooth laid a multiple of 4, c = 0: some count differs in 0 rounds, and the teeth row's tooth is
    7 s + 4 r_d at every Node-clock in 10,000 rounds;
  - with Meshes, the grip 300 against 2,100: 0 rounds;
  - laid at 3 modulo 4: c = 0 parts at round 22; c = -21 and c = -18, the window's ends, 0 rounds; c = -22, one below
    it, parts at round 2,507.
- **Beyond the probe** (the physicist's p1): three coupled rows with Meshes, springs, two ties and a cubic vertex, drive
  teeth (1, 7, 1000), (7, 7, 7) and (2, 1, 999,983), residues (0, 0, 0), (1, 2, 3) and (3, 3, 3), c at both ends of
  the window: 18 runs, 0 of 3,000 rounds differing in each; a weak source, |J| below its row's T_d = 10^6 in essentially
  every round, 0 of 20,000.

### 2.6 The dial in the beat

- **Probe (f):** 27 Mesh-less Node-clocks, one even row each, 10,000 rounds, the sign changes of the counts summed:
  - the drive at the teeth 6,000 and T_d 7, spring 73 (J = -146 a, not a multiple of 7: the tooth moves in 10,000 of
    10,000 rounds): 5,065;
  - the teeth 42,000 at T_d 1, spring 73: 5,065;
  - the linear recurrence x+ = 2 x - x- - (146 / 42000) x from the same lay, at the scale 10^30, every division Rule3's
    carry: 5,065;
  - on each side, the drive at the springs 70 and 77 (whole multiples of 7, the tooth standing): 4,961 and 5,204.
- So the spring 73 at T_d 7 beats as the spring 73 / 7 on the gear, between 70 / 7 and 77 / 7, as the exact recurrence
  does: the dial is read in the beat, and the drive's rounding does not move it.
- The leapfrog's invariant 42000 SUM (a - b)^2 + 146 SUM a b spreads 4,805 parts per million over the run in both acts
  (the edge's own rounding of the count; the two acts are count for count one, section 2.5).
- **What a beat count does not see:** a count of sign changes cannot see a slow pump, a damping or an aliasing of the
  counts; it is (f2)'s count-for-count reading that rules them out (the physicist's m11).
- **The rest beat is the strength's** only where the gear's own rounding is small: at swings near 70 counts the drive
  and the teeth acts alike make 7,532 sign changes against the recurrence's 7,742 (the physicist's m5).

### 2.7 The drive inside the act's two passes

- **The act drives twice** from one tooth (step.act): a first drive on J1 alone gives a first kick, whose momenta, M_in
  = 2 D_in (a - b) + s and M_out = M_in + 4 (s F + K1), the metric's push J5 reads in the books' form (each read by the
  centred split at the rest dial, in whole turns of 4 rest); then the drive carries J = J1 + J5 from the same r_d.
- **Claim 1, J5 reads no row it pushes.** The drive's run back holds at every T_d when J5's parity under the mirror is
  its target row's: J5 kept on an even target row, negated on an odd one.
- **Proof.** On a row J5 reads and does not push, J = J1, so the first drive is the second: the first kick is the
  round's kick and M_out is the round's momentum.
  - An even read row: the mirror maps its momentum M to -M - 1 (the slots swapped, the edge tooth s -> -1 - s), and the
    centred split is exactly odd under that map: with M + 2 rest = 4 rest q + rho, -M - 1 + 2 rest = 4 rest (-q) +
    (4 rest - 1 - rho). So the back round reads the row's two splits swapped and negated.
  - An odd read row: the mirror swaps its slots and negates them, so its momenta swap with no negation, M_in -> M_out
    and M_out -> M_in, and the back round reads its two splits swapped (the mathematician).
  - So J5 comes back as its parity under that map says, and the target row's drive returns by the flip on an even row
    (J5 kept) and by the sign on an odd row (J5 negated), as section 2.3 has it for J. A J5 of the wrong parity fails
    at every T_d with no crossing: J5 = 11 sigma_in(0) sigma_out(0) on an odd row, reading an even row, is kept by the
    swap and does not come back (the mathematician's O3); with the right parity his O1, O2 and K3 return.
- **Claim 2, J5 reads a row it pushes.** The run back fails only in a tick where the share the first kick misses carries
  a read momentum across a turn of the rest dial, in the forward tick or the back one.
- **Proof.** The first kick misses J5's share of the quotient, so the M_out J5 reads differs from the round's momentum
  by 4 s T_k (q_d - q1). J5 reads it through the split at 4 rest, so J5 differs from its value on the round's momentum
  only where that difference carries M_out across a turn of the dial. Where no tick crosses, J5 reads the same split
  forward and back, and Claim 1's argument returns the state.
- **Measured** (the mathematician's t7_twopass and t7_twopass2): the probe's mutant at factor 1 on a lay of small
  counts returns bit for bit at T_d (7, 7), (1, 1) and (2, 3), 9 of 9, J5 not 0 in 400 of 400 rounds, with no
  crossing; over 24 lays the run back returns exactly when no tick crosses, in 48 of 48 runs at factor 1 and 54 of 54
  at the probe's factor 11; 22 of 24 lays return at T_d 7 against 14 of 24 at T_d 1, the missed share about T_d times
  smaller. Probe (g)'s two failures cross in every round, the missed share about 18 turns of the rest dial. The
  physicist's run returns at T_d 10^6.
- **So** both conditions are the act's own: the mirror theorem's hypothesis (d), B2b's price (the 00 push reads only
  rows on the force's path, which J5 does not push; NOT_CLOSED 30), and J's parity under the mirror, which the act's own
  run back needs. The drive adds none: B6 may lay T_d above 1 on a row J5 reads, or on a row it pushes, so long as no
  row is both. B2b's push reads the odd 0i rows' momenta, products of their two splits kept by their swap, onto the even
  00 row: the right parity.
- **Probe (g):** two even rows on the cube of 3, each its own spring, J5 on row 0, 400 rounds out and 400 back:
  - J5 = 11 sigma_in(1) sigma_out(1), reading row 1, which it does not push: J5 not 0 in 400 of 400 rounds, the start
    returned bit for bit at T_d (7, 7), (7, 1) and (1, 1), row 0's tooth moving in 400 of 400 rounds at T_d 7;
  - J5 = 11 (sigma_in(0) sigma_out(1) + sigma_out(0) sigma_in(1)), reading the row it pushes: not returned at T_d
    (7, 7), and not at (1, 1), the missed share crossing a turn of the dial in every round.
  - The odd rows' cases are the mathematician's (O1 to O3, K3), since the probe lays two even rows.

## 3. On the board

- **Local and in one pass.** Each gear row at each Node-clock carries its own source with its own tooth and reads
  nothing else; no Node-clock waits on another, and no tooth crosses a Mesh.
- **Its state.** The tooth State.rd is part of the state the round reads and produces, laid at load within [0, T_d);
  the run back needs it, as it needs the edge tooth. At T_d = 1 it stays 0.
- **Its coefficients.** T_d (Gearing.drive) and T_k (Gearing.kick) per row, whole numbers of at least 1; the stretch
  multiplies the pull and the kick alike.
- **Its birth.** The loader lays the drive's tooth at 0; the law births a remainder at the half of its teeth. At T_d = 1
  the two agree; at B2b's T_d 2 they part by one, which the run back does not see (it needs the tooth in range, not its
  birth), and the record names neither (the mathematician's m11).
- **The record.** The drive writes nothing to it; its quotient enters the gear through the kick alone.

## 4. In the clicks

- **None of its own.** The drive's quotient goes to the kick, not to the record: the whole click is the click tooth's
  carry of the passing (term 11 as COUNT5 builds it, git baaa5353e), which reads the value legs' plan alone at the
  before, the now and the next counts (neither J5 nor the Mesh plan enters a train's X; step.passing), not the drive's
  quotient. So the passing's books, summed over the trains, stand at any T_d.
- **What the clicks read of it: the strength.** At s = T_k = 1 a spring f at the drive T_d beats as the spring f on T_d
  times the teeth, count for count (section 2.5), so the rest beat the clicks read as a mass, through many clicks of one
  clock, is that of the strength f / T_d; at s T_k above 1 it is s T_k f / T_d where the physicist's measured count for
  count holds (s T_k dividing W and the grips). The drive is the strength's dial in ratios of whole numbers, exact to
  one tooth.
- **The boundary with term 11, as built** (the physicist's B1; his p3 and p3b).
  - The passing is exactly the two-round change of each hand's energy weighted by its drive. From the drive act's books
    at standing teeth (s = T_k = 1, no Mesh), with e(t) = T_d W v(t+1) v(t) - a(t) J(a(t)) and S(t) the round's
    passing, 4 e(t+1) - 4 e(t-1) = 4 S(t) plus the drive tooth's rounding terms. So one quantum of the passing is
    s T_k / T_d of a quantum of the gear's own energy: the first text had the ratio inverted, a slip of mine.
  - The books close at unequal drives. A giver row at T_d 1 and a taker row at T_d 7, 27 Mesh-less clocks, 6,000
    rounds: S_giver + S_taker = 0 in 162,000 of 162,000 site-rounds; the identity holds in 161,892 of 161,892
    site-rounds for each hand at W' = T_d W; the T_d-weighted energy, the one the act conserves, spreads 8,122 ppm over
    the run, while the gears' own energy spreads 860,252 ppm.
  - The two remedies the first text named both break the books at unequal drives, and are withdrawn. The key read
    against the ratio leaves the clicks unbalanced in 1,845 site-rounds, the taker clicking 320 times against the
    giver's 2,165. The passing read on the kick fails the books in 161,664 of 161,973 site-rounds, and even at a
    uniform drive it loses the passing's exact antisymmetry (161,855 of 161,973 at T_d 7 on both rows).
- **The key's inertia across rows: the canonical one** (Big Pic's word, 6535643629 item 2).
  - The act keeps the T_d-weighted energy (8,122 ppm against the gears' own 860,252), so T_d is each row's inertia in
    the books.
  - A key passed between rows is then one quantum of that energy, since the passing closes in it at every site-round,
    and both remedies open the books at unequal drives. So the books force the choice.
  - Read in a gear's own energy, one key is s T_k / T_d of the gear's quantum (the physicist's ratio), and a vertex
    across rows reads c over the geometric mean of the two rows' drives (the physicist's 1e, his p5), as nature reads
    couplings on canonically normalized fields.
  - It is a reading, not a step: the act keeps each gear's counts and its whole c, with no root.
  - The night's clicking worlds lay their trains at T_d = 1 (B4's pair world); B6's dial sits on the square's rows,
    which do not click. So the reading is read on the books (p3, p3b), and on no clicking world's clicks (section 6).

## 5. What stands (term 7's row for the architecture document, when its readers agree)

- **Clock:** one wheel per gear row carries the row's source in whole turns of its teeth T_d and keeps the rest as its
  fine tooth; a drive of T_d teeth is the gear's own dial made T_d times finer for a source that reads no pull; back in
  time the wheel turns back with its tooth flipped on an even row and kept on an odd one.
- **Board:** q_d, r_d+ = carry(J, T_d, r_d) at every gear row and Node-clock, J = J1 + J5, one pass, the tooth in the
  state; K = s T_k q_d.
- **Clicks:** none of its own; at s = T_k = 1 the strength the clicks read is f / T_d of the source, exact to one tooth;
  the passing counts the T_d-weighted energy the act conserves, its books exact at unequal drives, one quantum of it
  s T_k / T_d of the gear's own; the key's inertia across rows is the canonical one, the T_d-weighted energy's,
  forced by the books, a reading and not a step.
- **Algebra:** Rule3's carry, forced by the books and the tooth's range; T_d SUM K = s T_k (SUM J + r_d(0) - r_d(end));
  the flip, the sign and the negation identities give the mirror by parity and the 24's twisted action; at standing
  teeth the act at T_d with the kick at 1 is the act at T_d W and T_d g with the drive at 1, count for count, for a
  source that reads no pull, the edge tooth T_d s + 4 r_d + c with c within [-T_d rho0, 3 - T_d rho0]; inside the two
  passes the run back needs the act's own hypotheses alone. **Home:** engine/step.py (drive, kick, act, mirror).
  **Status:** DERIVED, with the tooth moving on the act (node/term7_drive.py); the value of T_d on a row is its
  strength's term's.

## 6. OPEN

- **The values of T_d and T_k on each row:** each strength's own term (term 5's books for B6's dial on the square's
  rows; the coupling family's strengths, G3).
- **A clicking world at unequal drives:** none is laid, so the canonical reading of the key (section 4) is read on
  the books, not on a world's clicks.
- **The finer dial at s T_k above 1:** measured where s T_k divides W and the grips (the physicist's p1), not derived.
- **A moving clock.** At teeth that move with the 00 slot the edge's dial changes between the two edges, and the
  residue of section 2.5 is kept modulo 2 only, so the finer dial's count-for-count reading holds at standing teeth;
  the books and the run back hold at moving teeth as at standing ones (the identities do not read the teeth W).
- **J5 reading a row it pushes:** the run back fails where the missed share crosses a turn of the rest dial; B2b keeps
  no row both read and pushed.

## 7. The first text's readers, folded (the second text)

**Big Pic's word** (6535643629, item 2): the fold stands.
- 2.7 as the crossing condition: a kick whose source reads the momenta it pushes is undone exactly only while that
  read stands, so the run back can break only in a tick that carries a read momentum across a turn of the rest dial,
  at T_d = 1 as at any other; the condition is the act's, and the drive adds none.
- The odd rows: J5's mirror parity must match its target row's, any source's condition for a run back. Nature has it
  too: a force that reads velocities keeps time's reversal only if its field flips as well (the magnetic field). The
  odd read row's case is proved in 2.7.
- 2.5: the hypothesis stated, a J that reads no pull, with the grips-on runs and the offset c.
- Section 4: the key's inertia across rows is the canonical one, forced by the books, a reading and not a step.

**The mathematician's three, and his minors:**
1. B1, "fails at every T_d, T_d = 1 included": false. Rewritten as Claim 2 of section 2.7, the crossing condition,
   with his counterexample and his mechanism over 48 and 54 runs (the finding; 2.7).
2. B2, the odd rows: Claim 1 names J5's parity as its target row's, with the odd read row's swap without negation, his
   O3 failing and his O1, O2 and K3 returning (the finding; 2.7). Probe (g) lays two even rows; the odd rows' cases are
   his.
3. B3, "with T_d times the grips" untested: (f2) runs with Meshes too, and the hypothesis that J reads no pull is
   stated, with his parting at round 1 when it does (the finding; 1; 2.5; 5).
4. His minors: m1, the range as the law's convention (the finding; 2.1); m2, the carry's line, docs/ALGEBRA.md 35, and
   line 100's centred carry (2.1); m3, the number of terms (2.1); m4, (a)'s range and (e)'s reading at the run's end
   (2.2); m5, the 24's twisted action on equal drives (2.4); m6, the residue condition, now the window (2.5); m7,
   s + 2 W in place of "born a multiple of 4" (the finding; 2.5); m8, the teeth moving (2.3); m9 and m10, section 4's
   count for count at s = T_k = 1 and the passing's value legs (4); m11, the tooth's birth (3); m12, "at standing
   teeth" in section 5, and s named at each place (the stretch in K = s T_k q_d, the edge tooth in the momentum).

**The physicist's two, and his minors:**
1. B1, section 4's boundary with term 11: rewritten on his p3 and p3b. The ratio is s T_k / T_d, the books close at
   unequal drives, the T_d-weighted energy is the conserved one, both remedies are withdrawn, and the key's inertia
   is the canonical one on Big Pic's word; COUNT5 is cited (4, 5, 6).
2. B2, as the mathematician's B1 (2.7), with his return at T_d 10^6.
3. His finding beyond the page: the finer dial at every residue with the offset c, the mirror's image c = 3 - 3 T_d,
   and count for count wherever s T_k divides W and the grips (2.5, 6).
4. His minors: m1, the range's convention (2.1); m2, at an even W, and the offset form (2.5); m3 and m4, s T_k above 1
   (2.5, 4); m5, the rest beat where the gear's rounding is small (2.6); m6, one drive per row scaling every term (2.1);
   m7, the teeth moving (2.3); m8, a coupled odd row (his p4b returns); m9, grips, coupled rows, large T_d and a weak
   source (2.5); m10, COUNT5 (4); m11, beats cannot see a pump (2.6).

## 8. How this text checked itself (the owner's word of 16:2x UTC, 6527238774)

- **The second text's probe:** term7_drive.py extended in (f2) with Meshes and the offset c, rerun in 91 s on node-live
  f72067cdf, its lines byte for byte against the first text's output but for (f2)'s four new lines.
- **The readers' scripts, rerun by me byte for byte:** the mathematician's t7_twopass2 (on f72067cdf) and t7_b2b (on
  575973a20); the physicist's p1_finer, p3_books, p3b_uniform, p1d_f2_offset and p6_mirror_map (on f72067cdf).
- **Re-derived by hand:** the offset window [-T_d rho0, 3 - T_d rho0] from 0 <= T_d rho + 4 r_d+ + c < 4 T_d W over rho
  from rho0 to 4 W - 4 + rho0; the mirror's image c = 3 - 3 T_d; the odd read row's swap without negation; the missed
  share 4 s T_k (q_d - q1) and its crossing; the passing's two-round identity at W' = T_d W.
- **Cases built to break it:** c = -22, one below the window, parts at round 2,507; the residue 3 at c = 0 parts at
  round 22; J5 of the wrong parity (the mathematician's O3) fails with no crossing.
- **The first text's checks:**
  - the probe twice, its output byte for byte; its sections (a) to (e) byte for byte as the run the Boss's post
    6533284737 cites (its first 22 lines);
  - re-derived by hand: the uniqueness of the whole division (2.1); the run's books (2.2); the three identities (2.3,
    2.4), each by its two-line proof, and in 7,986 cases by the probe; the finer dial's bound and the residue's
    invariance (2.5); the centred split's oddness under the mirror's M -> -M - 1 (2.7);
  - the mutants of the mirror, the odd row's tooth flipped and the even rows' kept (d): both fail, as derived;
  - the drive at T_d 2 with a spring alone (b): the tooth never moves on the odd row, since a spring pushes by even
    counts, so the probe ties the even rows by an odd factor to make the tooth move;
  - a first try that broke: (g)'s first mutant pushed row 0 by the square of its own momentum, which runs away before
    any run back can be read; the probe reads the cross form at the factor 11 and stops any run whose count passes
    10^12.
- **What the probe does not test:** a moving clock (the 00 slot read into the teeth), the drive at T_k above 1 against
  the teeth row, the odd rows inside the two passes (the mathematician's cases), and the key of a clicking train with
  T_d above 1 (section 4).
