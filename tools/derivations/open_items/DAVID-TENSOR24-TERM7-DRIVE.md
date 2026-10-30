# Term 7, the drive: one carry of the source at the drive's teeth, forced by the books, a finer dial for the source

David, 2026-10-30 (the first text, 21:xx UTC), on the owner's word of 11:1x UTC (derive what the Node-clock needs to
close; everything to stand with a hostile mathematician and a hostile physicist), for the architecture document's term 7
("the drive: one wheel carries the coupling's push for every row; q_d, r_d+ = carry(J, T_d, r_d); none of its own: the
clicks do not come from the drive; Rule3's carry at T_d; BUILT at T_d = 1; DERIVED (G3), to confirm under the owner's
rule of 13:0x (section 6)") and for the night's side list, NOT_CLOSED 14: at T_d = 1 the drive is the identity, q_d = J
and r_d = 0 always, so term 7's DERIVED rested on a no-op (g3_math item 13), and what closes it is a probe with r_d
moving. It reads the act on node-live f72067cdf: engine/step.py's drive, kick, act and mirror, the drive's tooth
State.rd within [0, T_d), the drive's teeth Gearing.drive and the kick's Gearing.kick per row. The probe is
derive/david_open/node/term7_drive.py (about 50 s), its output beside it, whole numbers alone, every division Rule3's
carry. Section 7 says how the text checked itself.

**The finding in one line:** the drive is Rule3's carry of the row's source at the drive's teeth, and nothing else could
be: the books and a bounded tooth force it.
- **Forced:** J + r_d = T_d q_d + r_d+ (nothing lost, nothing made) with 0 <= r_d+ < T_d (Rule3's range) fixes q_d and
  r_d+ uniquely, by the uniqueness of the whole division.
- **Its books, read from outside with the tooth moving:** at T_d / T_k = 1/1, 2/2, 7/7, 2/1 and 7/1 the quotient is
  whole in 200 of 200 rounds, the kick read off the gear's momentum is T_k q_d in 200 of 200, and over the run T_d SUM K
  = T_k (SUM J + r_d(0) - r_d(end)) at every gear: the drive's part of the momentum stays within 4 T_k counts of the
  exact fraction at every round and never drifts.
- **The run back:** the mirror by parity is the carry's own, two identities: an even row's tooth flips, T_d - 1 - r_d,
  and an odd row's is kept, because the odd row's source changes sign under time's reversal. 400 rounds out and back,
  bit for bit, at T_d 1, 2 and 7; flipping the odd row's tooth too fails, and so does keeping the even rows'.
- **A finer dial for the source:** at standing teeth, the act with the drive at T_d and the kick at 1 is, count for
  count, the act with T_d times the teeth and T_d times the grips and the drive at 1, its edge tooth T_d s + 4 r_d,
  whenever the edge tooth is born a multiple of 4, as at rest: 0 of 10,000 rounds differ. So the drive divides the
  source's strength by T_d against the gear's inertia and its grips, exactly in the counts, not on average.
- **No condition of its own:** inside the act's two passes (a first drive on J1 alone feeds the metric's push J5) the
  drive's run back holds at every T_d when J5 reads no row it pushes, the act's own hypothesis, and fails at every T_d,
  T_d = 1 included, when it does.
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
- **The force's path.** At T_d = 1 the wheel is the identity: q_d = J and r_d stays 0 (g3_math item 13). Every row the
  loader lays stands there until a strength sets T_d (decision 40 (d): one drive for every row).
- **A finer dial (section 2.5).** A drive of T_d teeth is the gear's own edge dial made T_d times finer for the source
  alone: the gear with the drive at T_d is the gear with T_d times the teeth and T_d times the grips, the source
  unscaled, count for count. The drive is the source's strength against the clock's inertia, and nothing else.
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
  Rule3's range [0, T_d) is the law's one convention for a remainder (law line 100: the carry, n + r = q d + r' with
  0 <= r' < d). A centred range would be another carry, which the law does not write.
- **One drive per row,** carrying the row's whole source J = J1 + J5 (decision 40 (d); step.act): a drive per term
  would keep a tooth per term, and the sum of their quotients differs from the quotient of the sum by up to the number
  of terms less one, more state for no gain.

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
  equal to T_k q_d in 200 of 200; T_d SUM K = T_k (SUM J + r_d(0) - r_d(end)) at every gear. **Probe (e):** at T_k 1,
  T_d SUM K - SUM J stays within -1..1 at T_d 2 and -6..6 at T_d 7, inside the bound -(T_d - 1)..T_d - 1.
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
- **Probe (c):** 400 rounds out and 400 back by untick on the cube of 3, every tooth moving in the lay, the start
  returned bit for bit at T_d 1, 2 and 7. **Probe (d),** at T_d 7: the law's mirror True; the odd row's tooth flipped
  too, False; the even rows' tooth kept, False.

### 2.4 The 24's turns on the drive's tooth

- **The negation:** carry(-J, T, T - 1 - r) = (-q, T - 1 - r+). Proof: -J + T - 1 - r = -(T q + r+) + T - 1 =
  T (-q) + (T - 1 - r+).
- A turn of the 24 that negates a row negates its count and its source, the potential being kept by the turn. By the
  negation the turned act equals the act turned when that row's drive tooth flips, T_d - 1 - r_d, which is the twisted
  action of the 24 on the state (NOT_CLOSED 25; A2's engine test at T_d = 7 on every row: 24 of 24 turns, and 3 of 24
  with the teeth kept).
- **Probe (h):** the three identities, the flip, the sign and the negation, at every T_d from 1 to 11, J from -60 to 60
  and r_d within [0, T_d): 7,986 of 7,986 each.

### 2.5 The finer dial, stated and proved

- **Statement.** Take a gear row at standing teeth W (its dial 2 D = 4 W at both edges), grips g on its Meshes, the
  drive at T_d, the kick at 1 and the stretch at 1, its source J, its edge tooth s and its drive tooth r_d. Take the
  same row at the teeth T_d W, the grips T_d g, the drive at 1 and the same source J, with the edge tooth s' = T_d s + 4
  r_d. If s + 2 W is a multiple of 4 (s a multiple of 4 at an even W, as at rest, where s = 0 and W = 6 den Gamma^2),
  the two take the same count at every round, and s'+ = T_d s+ + 4 r_d+.
- **The residue is kept.** At standing teeth the gear's numerator is n = 4 W (a - b) + 4 push + s, so n = s modulo 4,
  and the split at the dial's half (step.split) gives s+ = ((n + 2 W) mod 4 W) - 2 W = n modulo 4: the edge tooth's
  residue modulo 4 never changes, every push entering the momentum four times.
- **Proof.** The drive's row: n = 4 W (a - b) + 4 (F + q_d) + s with T_d q_d = J + r_d - r_d+. The teeth row reads the
  same counts, so its pull is T_d F: n' = 4 T_d W (a - b) + 4 (T_d F + J) + s' = T_d n + 4 r_d+. Write n + 2 W = 4 W q +
  rho with 0 <= rho < 4 W; rho = s + 2 W modulo 4, so rho is a multiple of 4 and at most 4 W - 4. Then n' + 2 T_d W =
  4 T_d W q + (T_d rho + 4 r_d+), and T_d rho + 4 r_d+ <= T_d (4 W - 4) + 4 (T_d - 1) < 4 T_d W. So both rows step by
  q, and s'+ = T_d (rho - 2 W) + 4 r_d+ = T_d s+ + 4 r_d+. By induction it holds at every round.
- **Where they part.** With rho of another residue the finer dial can carry a count one round sooner at the dial's top
  (rho within 3 of 4 W with r_d+ high). With the kick's teeth above 1 the teeth row needs the source T_k J, and the
  bound holds only while T_k (T_d - 1) < T_d, that is at T_k = 1.
- **Probe (f2):** the drive at the teeth 6,000 and T_d 7 against the teeth 42,000 at T_d 1, spring 73 on both, one lay
  on 27 Mesh-less Node-clocks, 10,000 rounds: with the edge tooth laid a multiple of 4, some count differs in 0 rounds,
  and the teeth row's tooth is 7 s + 4 r_d at every Node-clock in 10,000 rounds; laid at 3 modulo 4, the two part at
  round 22.

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

### 2.7 The drive inside the act's two passes

- **The act drives twice** from one tooth (step.act): a first drive on J1 alone gives a first kick, whose momenta, M_in
  = 2 D_in (a - b) + s and M_out = M_in + 4 (s F + K1), the metric's push J5 reads in the books' form (each read by the
  centred split at the rest dial); then the drive carries J = J1 + J5 from the same r_d.
- **Claim.** The drive's run back holds at every T_d when J5 reads no row it pushes, and fails at every T_d, T_d = 1
  included, when it does.
- **Proof.** On a row J5 reads and does not push, J = J1, so the first drive is the second: the first kick is the
  round's kick and M_out is the round's momentum. The mirror maps an even row's momentum M to -M - 1 (the slots swapped,
  the edge tooth s -> -1 - s), and the centred split is exactly odd under that map: with M + 2 rest = 4 rest q + rho,
  -M - 1 + 2 rest = 4 rest (-q) + (4 rest - 1 - rho). So the back round reads the two splits swapped and negated, and
  J5, kept under that swap as the books' form is, comes back; the pushed rows' drive returns by the flip on J. On a row J5
  both reads and pushes, the first kick misses J5's share, so the M_out it reads is not the round's momentum, and the
  back round reads the round's: J5 does not come back, at T_d = 1 as at any other, where the share is J5 itself.
- **So** the condition is the act's own, the mirror theorem's hypothesis (d), B2b's price (the 00 push reads only rows
  on the force's path, which J5 does not push; NOT_CLOSED 30), and the drive adds none: B6 may lay T_d above 1 on a row
  J5 reads, or on a row it pushes, so long as no row is both.
- **Probe (g):** two even rows on the cube of 3, each its own spring, J5 on row 0, 400 rounds out and 400 back:
  - J5 = 11 sigma_in(1) sigma_out(1), reading row 1, which it does not push: J5 not 0 in 400 of 400 rounds, the start
    returned bit for bit at T_d (7, 7), (7, 1) and (1, 1), row 0's tooth moving in 400 of 400 rounds at T_d 7;
  - J5 = 11 (sigma_in(0) sigma_out(1) + sigma_out(0) sigma_in(1)), reading the row it pushes: not returned at T_d (7,
    7), and not at (1, 1).

## 3. On the board

- **Local and in one pass.** Each gear row at each Node-clock carries its own source with its own tooth and reads
  nothing else; no Node-clock waits on another, and no tooth crosses a Mesh.
- **Its state.** The tooth State.rd is part of the state the round reads and produces, laid at load within [0, T_d);
  the run back needs it, as it needs the edge tooth. At T_d = 1 it stays 0.
- **Its coefficients.** T_d (Gearing.drive) and T_k (Gearing.kick) per row, whole numbers of at least 1; the stretch
  multiplies the pull and the kick alike.
- **The record.** The drive writes nothing to it; its quotient enters the gear through the kick alone.

## 4. In the clicks

- **None of its own.** The drive's quotient goes to the kick, not to the record: the whole click is the click tooth's
  carry of the passing (term 11), which reads J on the value legs at the before, the now and the next counts, not the
  drive's quotient. So the passing's books, summed over the trains, stand at any T_d.
- **What the clicks read of it: the strength.** A spring f at the drive T_d beats as the spring f on T_d times the
  teeth, count for count (section 2.5), so the rest beat the clicks read as a mass, through many clicks of one clock, is
  that of the strength s T_k f / T_d. The drive is the strength's dial in ratios of whole numbers, exact to one tooth.
- **A boundary with term 11, named.** The passing reads the source J, while the gear takes s T_k J / T_d of it. On a
  clicking train whose rows carry T_d above 1, one quantum of the passing is T_d / (s T_k) of a quantum of the gear's
  own energy, so the key must be read against that ratio, or the passing read the kick. The night's clicking worlds lay
  their trains at T_d = 1 (B4's pair world); B6's dial sits on the square's rows. OPEN, with term 11 (TERM11.md: "with s
  or T_k above 1 the area moved is the cross with the kick applied ... checked again when G3 lands").

## 5. What stands (term 7's row for the architecture document, when its readers agree)

- **Clock:** one wheel per gear row carries the row's source in whole turns of its teeth T_d and keeps the rest as its
  fine tooth; a drive of T_d teeth is the gear's own dial made T_d times finer for the source alone; back in time the
  wheel turns back with its tooth flipped on an even row and kept on an odd one.
- **Board:** q_d, r_d+ = carry(J, T_d, r_d) at every gear row and Node-clock, J = J1 + J5, one pass, the tooth in the
  state; K = s T_k q_d.
- **Clicks:** none of its own; the strength the clicks read is s T_k / T_d of the source, exact to one tooth; on a
  clicking train with T_d above 1 the key reads against T_d / (s T_k) (OPEN, with term 11).
- **Algebra:** Rule3's carry, forced by the books and the tooth's range; T_d SUM K = s T_k (SUM J + r_d(0) - r_d(end));
  the flip, the sign and the negation identities give the mirror by parity and the 24's twisted action; the act at
  T_d with the kick at 1 is the act at T_d W and T_d g with the drive at 1, count for count, when s + 2 W is a multiple
  of 4. **Home:** engine/step.py (drive, kick, act, mirror). **Status:** DERIVED, with the tooth moving on the act
  (node/term7_drive.py); the value of T_d on a row is its strength's term's.

## 6. OPEN

- **The values of T_d and T_k on each row:** each strength's own term (term 5's books for B6's dial on the square's
  rows; the coupling family's strengths, G3).
- **The key against the drive on a clicking train** (section 4), with term 11.
- **A moving clock.** At teeth that move with the 00 slot the edge's dial changes between the two edges, and the
  residue of section 2.5 is kept modulo 2 only, so the finer dial's count-for-count reading holds at standing teeth;
  the books and the run back hold at moving teeth as at standing ones (the identities do not read the teeth W).

## 7. How this text checked itself (the owner's word of 16:2x UTC, 6527238774)

- **Rerun:** the probe twice, its output byte for byte; its sections (a) to (e) byte for byte as the run the Boss's
  post 6533284737 cites (its first 22 lines).
- **Re-derived by hand:** the uniqueness of the whole division (2.1); the run's books (2.2); the three identities (2.3,
  2.4), each by its two-line proof, and in 7,986 cases by the probe; the finer dial's bound T_d (4 W - 4) + 4 (T_d - 1)
  < 4 T_d W and the residue's invariance (2.5); the centred split's oddness under the mirror's M -> -M - 1 (2.7).
- **Cases built to break it:**
  - the mutants of the mirror, the odd row's tooth flipped and the even rows' kept (d): both fail, as derived;
  - the edge tooth laid at 3 modulo 4 (f2): the finer dial parts at round 22, as 2.5 says it can;
  - J5 reading the row it pushes (g): the run back fails at T_d 7 and at T_d 1, the act's condition and not the
    drive's;
  - the drive at T_d 2 with a spring alone (b): the tooth never moves on the odd row, since a spring pushes by even
    counts, so the probe ties the even rows by an odd factor to make the tooth move.
- **A first try that broke:** (g)'s first mutant pushed row 0 by the square of its own momentum, 1001 sigma_in(0)
  sigma_out(0), which runs away (the push growing as the square of the velocity) before any run back can be read; the
  probe now reads the cross form at the factor 11, bounded over the 400 rounds, and stops any run whose count passes
  10^12.
- **What the probe does not test:** a moving clock (the 00 slot read into the teeth), the drive at T_k above 1 against
  the teeth row (2.5 holds at T_k = 1 only), and the key of a clicking train with T_d above 1 (section 4).
