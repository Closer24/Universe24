# Draft D2: the draw's uniformity (question 2) and exponential decay (question 3)

The Boss's helper, drafting for the Boss, 2026-10-29, 04:58 UTC, on tensor24-review at 298bec5d8. The probes are in
probes/ beside this file. Each `.py` sits beside its `.txt` output and runs on the engine's own `carry`, `beat` and
`tick`, in exact integers: from the repository's root, `PYTHONPATH=src:<this folder>/probes python <probe>`.
common.py builds the probes' small board. The Boss's verification is VERIFY.md.

## Question 2: the draw's uniformity

### The answer in plain words

No remainder on the board is random. Each is fixed by the setting and moved by the act. "Uniform" holds in a different
sense for each one:

- **The dial ph.** Over the ticks it is a rotation by the rate on [0, Gamma): it visits every residue once per period
  exactly when gcd(rate, Gamma) = 1. This confirms David's item 11. A click can happen only at a beat, though, and there
  the dial holds the beat carry's own remainder, which lies in [0, rate) and not in [0, Gamma). Read at a click, the
  dial's room is the rate. Its successive reads are a rotation, so they are not independent.
- **The gears' fine teeth r.** Each is the remainder of the gear's exact momentum, M = W (a - b) + r, and the act adds
  the push: M+ = M + push. Over the board's states a fine tooth stays exactly uniform for one tick. After that it stays
  uniform only where the push is a multiple of W, because the push reads the notches that the carry's quotient moved.
  After the first tick the uniformity is approximate. It is measured, not derived.
- **The drive's r_d** behaves like a fine tooth, as the remainder of the accumulated source. On the force's path
  (T_d = 1) it is always 0.

**The composition** that turns uniform reads into a c uniform on [0, room) exactly, with no sort, no if and no bound, is
the **sum through the carry**: d_1 + ... + d_m = q room + c. It is uniform as soon as one read is uniform on [0, room)
and independent of the others, whatever the others' law. It is symmetric in the reads, so the 24 permuting the six
Meshes change nothing, and the alike images draw alike with no sort.

The mixed radix through the carry (c = c b + d, room = the product of the bases) is a bijection and gives the larger
room. It needs an order that the 24 do not move, so it belongs across labelled reads (the hand's gears), not across the
Meshes.

The head's bias comes from the sort, not from the reads. Sorting is many-to-one: it keeps C(b+m-1, m) of the b^m tuples.

### The derivation

1. **Lemma 1 (the carry keeps a uniform remainder).** Fix the wind n and the teeth d >= 1. Then r -> r', with
   n + r = q d + r', is a bijection of [0, d), and the carry run back, r = (r' - n) mod d, is its inverse. So if r is
   uniform and independent of n, r' is uniform and independent of n. The quotient q is not: given n and q, r' lies in a
   sub-range. Hence **a remainder read at the tick its own carry fired is confined.** The dial after its beat lies in
   [0, rate), and the wind's remainder after a click lies below the wind's increment.
2. **Lemma 2 (the mixed radix).** c = c b_i + d_i with room = room b_i maps the product of the [0, b_i) one to one onto
   [0, product of b_i). Jointly uniform digits therefore give c exactly uniform. The room is the product with no cap,
   which is law 11's room.
3. **Lemma 3 (the sum, the one-digit lemma).** Apply Lemma 1 with n = the sum of the other reads. Then c = (sum) mod room
   is uniform when one read is uniform on [0, room) and independent of the rest. It is invariant under every permutation
   of the reads.
4. **Lemma 4 (the sort).** Sorted Horner depends only on the multiset of the digits. Its image therefore has at most
   C(b+m-1, m) values: 220 of 1,000 and 126 of 1,296, which gives 0.875 and 0.9375. The capped room min(product, M) is
   uniform exactly where M divides the product.
5. **Lemma 5 (Born's pick on a uniform c).** Part k is picked by ceil(sig_<=k room / S) - ceil(sig_<k room / S) values
   of c. That count is exactly sig_k room / S where S divides room, and within one count otherwise.
6. **The dial.** (k, ph') = carry(ph, Gamma, rate) is a rotation by the rate on Z_Gamma. Its orbit is the coset
   ph_0 + gcd(rate, Gamma) Z. At the beats, ph'_(n+1) = (ph'_n - Gamma) mod rate, so it is a rotation on [0, rate) by
   -Gamma mod rate, uniform over the beats iff gcd(rate, Gamma) = 1. At the full rate it does not move. When the count
   moves the rate (stage 7b), each beat's window [0, rate_n) moves too, and there is no fixed room.
7. **The fine tooth.** At W+ = W, p + push + home = W (a - b) + r + push = v W + r+. With M = W (a - b) + r this gives
   M+ = M + push, so r_t = (r_0 + the sum of the pushes) mod W. Lemma 1 gives uniformity at tick 1. From tick 2 on, the
   push mod W depends on a+, which the carry moved by a quotient that knows r. So uniformity is kept exactly only where
   s D and the grips are 0 mod W.
8. **The run back.** The whole step is a bijection of the full state, so it keeps the counting measure of the full state
   (Liouville in integers). It does not keep a uniform law of the remainders alone.

### The probes

- **probes/q2_compose.py, q2_compose.txt** (exact enumeration):
  - The mixed radix is uniform at all 5 base sets, with every value hit once: rooms 315, 1,000, 1,296, 512 and 120.
  - The sum carry is uniform at all 5.
  - **The sorted mutant fails at all 5:**
    - (10,10,10): 220 of 1,000 values hit, P(up) = 7/8;
    - (6,6,6,6): 126 of 1,296 values hit, P(up) = 15/16;
    - (2,3,4,5): 58 of 120 values hit, P(up) = 4/5.
  - The capped mutant fails exactly where M does not divide the product: (5,7,9) with M = 100, counts 3 and 4.
  - **The one-digit lemma:** one uniform digit plus the sorted mutant's biased c gives 1,000 per residue, uniform. Two
    biased reads with no uniform one give 30,502 to 144,622, not uniform.
  - **The 24 on the six Meshes:**
    - the cube's 24 rotations are generated as face permutations;
    - over 729 tuples times 24 turns, the mixed radix changed 16,128 times and the sum carry 0 times;
    - the sum is uniform (243, 243, 243).
  - **Born's pick:** 50,955 part-cases (rooms below 80, sizes below 6), all within one count, and exact at every case
    where S divides room.
- **probes/q2_dial.py, q2_dial.txt** (the engine's `beat`):
  - Over the ticks, coprime rates visit all residues: 12/12, 12/12 and 1,000/1,000. Rates with gcd > 1 visit 3/12,
    2/12 and 8/1,000.
  - At the beats, the phases lie in [0, rate - 1] and step by -Gamma mod rate in every case. **Read on room Gamma,
    P(up) = 1.0000** at rates 5 (of 12), 375 and 600 (of 1,000); it is 1 by the bound at every rate up to Gamma / 2.
    Read on room rate, P(up) = 0.5005 at rate 999.
  - At the full rate the phase is a single value.
  - **Not coprime:** at Gamma 12 with rate 4 or 8, P(up) is 1/3 or 2/3 depending on the start phase.
  - **A rate moved by the count:** every post-beat phase stays below that beat's rate. On room Gamma, P(up) is 0.6464,
    0.7894 and 0.8274 for the three laws of the rate, the last being Gamma (1 - 1/Gamma)^n by carries.
  - **Two successive draws** at Gamma 1,000, rate 377: P(up, up) = 2/13 against P(up)^2 = 0.2513. The pair
    (c_n, c_n+1) lies on 377 of 142,129 points.
- **probes/q2_board.py, q2_board.txt** (the engine's `tick`, a ring of 4, W 7):
  - **M+ = M + push** holds at every site and tick over 40 ticks.
  - **Site 0's fine tooth over all of [0, 7):**
    - at D 1 and grip 1, it is uniform at tick 1, then hits 4, 5, 5, 5 and 5 of the 7 residues;
    - at D 0 and grip 1, the same failure: 5, 3, 6, 6, 5;
    - **at D 7 (0 mod 7) and grip 0, it is uniform at every tick.**
  - **Jointly over [0, 7)^4:** 2,401 distinct images at tick 1, 1,267 at tick 2 and 1,526 at tick 13. Site 0's law at
    tick 13 runs from 267 to 399 against 343 for uniform: approximately uniform, not exactly.

### Against David's item 11

- **CONFIRMS:** with the rate coprime to Gamma, the dial visits every residue alike over the ticks (q2_dial part 1).
- **EXTENDS:**
  - with gcd(rate, Gamma) > 1 it visits only a coset (parts 1 and 3);
  - **read at a click, which happens only at a beat, the dial's room is the rate, not Gamma**: [0, rate), rotated by
    -Gamma mod rate (part 2);
  - at the full rate it stands still.
- **CONTRADICTS the dial as the draw's source:**
  - on room Gamma at a beat, P(up) = 1 at every rate up to Gamma / 2 (part 2);
  - a rate moved by the count gives no fixed room (part 4);
  - successive reads are dependent (part 5) and wait by three gaps (q3_wait part 2).
- **On "whether the bias M5 found is the read's": it is the composition's.** The same digits unsorted give an exactly
  uniform c (q2_compose part 1).

### What stays open

1. **The sign flips.** A reflection or a half turn sends a fine tooth to w - 1 - r. The sum carry is invariant under the
   permutations of the 24 but not under the flips. The head's framing by the gear's displacement sense is the known
   mend, and I did not probe it.
2. **No theorem that the board's remainders stay uniform after the first tick.** It is measured (q2_board) and holds
   only approximately.
3. **The independence of c from the sizes S**, whose gears are the same gears that are read. I did not probe it.
4. **Exact Born odds need S to divide room.** With room = W the odds are within 1/W, and a product room needs several
   independent reads.
5. **The distribution test as a gate** (section 30): the octiles of c over the room, on every record.

**Method: addressed.**
- (a) What produces each term:
  - the dial is the clock's beat, the carry of its count with the rate as addend;
  - the fine teeth are the gears' notch remainders, M = W (a - b) + r moved by the push, which follows from the one act
    (checked);
  - the composition is Rule3's carry and products, with nothing new;
  - which remainder is read, and that it is read at a beat, is the clock's order of reads.
- (b) What the clicks show, the books first:
  - each carry runs back exactly, the mixed radix is a bijection and the sum carry books its quotient, so nothing is
    lost;
  - the 24 are kept by the sum carry (0 changes) and broken by the mixed radix across the Meshes (16,128);
  - Born's odds are within one count of room, and exact where S divides room.
- (c) What does not follow and is asked of the clicks: the uniformity of the board's remainders after the first tick,
  the flips, and the independence of c from S. Each is asked of a distribution test on every record.

## Question 3: exponential decay

### The answer in plain words

The split is enough, and no third form of click is needed. **A fresh uniform c at each beat gives geometric waiting
times exactly**, with the constant hazard h = g / room (exactly sigma_go / S where S divides room): the discrete
exponential.

The board, however, never draws fresh. Its c is a deterministic function of remainders that the act moves (case ii). On
a finite board every read is eventually periodic (draft K, K2). The waiting times depend on the regime:

- **Not geometric:** at the extremes the law is exact.
  - The dial is a rotation, so its gaps between goes take at most three values (the three-gap theorem), its waits are
    bounded and it has no exponential tail.
  - A still hand never changes its whether.
  - A hand near rest moves its fine teeth by a few teeth a beat, and its whether persists.
- **Geometric within the test:** when the push moves the read fine teeth by many, varying teeth each beat, the waiting
  times over the setting's seeds pass the geometric test.

So the law's reading, "the decay periodic at the beat and not exponential", stands for the dial and for a quantum near
rest. Exponential decay would need c refreshed each beat by a read the act moves enough. That is measured on a lively
board and not derived.

### The derivation

1. **(i) A fresh draw.** With c_1, c_2, ... independent and uniform on [0, room), each beat goes with probability
   h = g / room, where g = room - ceil(sigma_stay room / S) by Lemma 5. Independence gives
   P(tau = t) = (1 - h)^(t - 1) h. The memorylessness is the draws' independence, and the constant hazard is the fixed
   sizes.
2. **(ii) A read the act moves.** The whether at beat n is f(state_n), and the state moves by the act's bijection. On a
   finite set every orbit is a cycle, so tau is a function of the entry state, and its law over entry states is that of
   first hitting times in a permutation.
   - **The dial:** c_n = c_0 + n delta mod rate, a rotation, and the go set is one bracket, an interval. By the
     three-gap theorem (Steinhaus; Slater for the return times) the gaps between goes take at most three values. Their
     mean is Kac's 1/h, but the law is supported on at most three values, and the waits are bounded by the largest gap.
   - **The still hand:** push 0, so r is constant and tau is 1 or never.
   - **A gear's fine tooth:** r_(n+1) = (r_n + push_n) mod W. Its whethers decorrelate only as far as push_n mod W
     varies from beat to beat.

### The probes

- **probes/q3_wait.py, q3_wait.txt:**
  - **(1) Every sequence of 5 beats enumerated:** the first go at beat t is counted (room - g)^(t-1) g room^(5-t) times
    exactly. This holds at room 8 with sizes (3,1), where h = 1/4 = Born; at room 8 with sizes (2,1), where h = 1/4
    against Born 1/3 (S does not divide room); and at room 6 with sizes (5,1), where h = 1/6.
  - **(2) The dial mutant** (sizes (3,1), over every entry phase):

    | Gamma, rate | gaps between goes | waits (values; longest) | P(wait > 8) | geometric |
    | --- | --- | --- | --- | --- |
    | 1,000, 377 | {3, 8, 11} | 11 values; longest 11 | 0.0398 | 0.1008 |
    | 1,000, 401 | {2, 41, 43} | 43 values; longest 43 | 0.4264 | 0.1008 |
    | 1,000, 999 | {1, 751} | 551 of 999 never go in 200 beats | 0.7437 | 0.1009 |
    | 12, 12 (full rate) | none | 1 or never | 0.75 | 0.1001 |

  - **(3) The board** (4 x 4 x 1, W 64, every tick a beat; c = own fine tooth + the +x Mesh's digit by the sum carry;
    h = 1/4; 2,000 seeds; 60 beats):

    | regime | chi-square (12 dof, 5% line 21.0) | P(go \| go the beat before) |
    | --- | --- | --- |
    | lively: notches up to 1,000 | 12.3 | 0.2545 |
    | small: notches up to 3 | 12.4 | 0.2450 |
    | still: push 0 | 33,925 | 1.0 |

    In the still regime 502 seeds go at beat 1, then none go, and 1,498 never go.
- **probes/q3_rest.py, q3_rest.txt** (near rest, notches in {-1, 0, 1}):
  - at W 64, the fine tooth moves a median 10 teeth a beat; chi-square 68.2;
  - at W 4,096, it moves a median 73 teeth a beat; chi-square 25,266. Beat 1 gives 501 goes against 500 expected, beat
    2 gives 6 against 375, and 196 seeds never go.

### What stays open

1. **Whether a quantum at rest can decay exponentially on the board.** Its own fine teeth move too little. A read from a
   lively neighbour (the Mesh's digit of a moving train, such as the light) might refresh it. That is not derived and
   not probed on a bound hand.
2. **The board's cycle length** (K2) against the lifetime.
3. **The geometric pass is over the setting's seeds**, which numpy's generator draws, outside the board. Along one run
   the whether has only lag-1 independence measured.
4. **The draw on the twins' actual sizes** with the hand that decays: not probed.

**Method: addressed.**
- (a) What produces each term, and whether it follows:
  - the beat is the clock's own carry, and the whether is the split's second carry, its c from the gears' notch
    remainders;
  - the geometric law follows by itself from the split given fresh draws, so there is no third form;
  - the freshness of c is not the act's by itself: the act moves the remainders deterministically (M+ = M + push).
- (b) What the clicks show:
  - the waiting times are the clicks to read, and each go is booked once by the split's carry, its remainder staying;
  - the rotation, still and near-rest regimes fail the geometric law, and the lively regime passes.
- (c) What does not follow, and what is asked of the clicks: a fresh uniform c per beat for a quantum near rest. It is
  asked of the clicks as a gate: the waiting-time histogram of a quantum at rest against the geometric law, before any
  claim of exponential decay.
