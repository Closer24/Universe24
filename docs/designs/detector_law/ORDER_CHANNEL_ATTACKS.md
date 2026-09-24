# The order channel's solution under attack: every objection, its answer, its status (the chief physicist, 2026-09-24, 04:15Z; docs only, no run, no pin moved)

The model owner's order (04:08Z, on the three declaration lines of
DECLARATIONS.md section 2 item 8, which he left to the Boss to declare):
"make sure it cannot be attacked in any form, any way, because they keep
attacking the same thing." This page lists every objection a referee can
raise against the solution of row 1c (the birth residue Inside: the
births in a seed-set order, the click stamped without the residue), the
answer, and the status of each: CLOSED (by derivation or by the engine as
built), CLOSED BY DECLARATION (a line DECLARED by the owner, 04:18Z
(record 1648), and by the Boss, 04:14Z on his word of 04:12Z (record
1647); the six lines are listed at the end), STATED (an honest limit the
paper says), FUTURE (a declared later test), CHECK (a check of a world
file, the World Generator's). The computations are
`order_channel_pins.py` and `order_channel_hidden_pins.py` (their `.out`
files); the engine lines are readings of `src/event_universe/events/detector_law.py`
at the GO's head, not runs.

**What the solution claims.** A deterministic integer model on the
GameBoard, nonlocal in ONE declared step (the pair's gather, POSTULATES.md
section 10; ALGEBRA.md 3.1 and 3.6), reproduces the CHSH counts exactly
(S = 181 / 64 at N = 2048, Theorem 5's marginals N / 2 of N at every
setting) with NO signalling Outside: none in the counts (exact, at every
N) and none in the order of the outcomes (for a reader without the seed,
exact for a uniformly random order). **What it does not claim.** That the
model is local Inside (Bell's theorem forbids it for S > 2), or that the
residue is unknowable in principle (it is Inside by the postulate P11, as
Bohm's configuration is under quantum equilibrium).

## The objections

1. **"A local deterministic model cannot exceed S = 2 (Bell)."** The
   model is not local Inside: the pair's outcome is assigned by the one
   gather from both settings, the record's one non-local step. The claim
   is exactly this, a deterministic integer model nonlocal in one
   declared step; the paper says it. STATED.
2. **"Then it signals."** In the counts, no: N / 2 of N at every setting,
   exact (Theorem 5; `order_channel_pins.py`). In the order, as first
   declared, yes: under the counter family [1, 1] the birth order is the
   residue order and B reads A's setting from his own list with certainty
   (the + fraction of his first N / 4 births 0.293 at a = 0 against 1.000
   at a = N / 4; four runs). Under the seed-set order, no: B's list at
   fixed b is a balanced multiset (N / 2 pluses for either a) in a
   uniformly random order, whose distribution is the uniform distribution
   over balanced strings for a and for a' alike, so no decoder fixed
   before the run, without the seed, does better than 1 / 2 (the theorem;
   `order_channel_hidden_pins.py` (b)). CLOSED BY DECLARATION (lines 1 to
   3).
3. **"The host knows the seed, so the model signals to the host."** The
   seed is Inside by P11 (Outside reads clicks only): what is accessible
   Outside is defined by the postulate, as in every theory (in quantum
   mechanics the Born statistics, in Bohm's theory the configuration
   under quantum equilibrium). The model's ontology is nonlocal and
   deterministic; its operational content is no-signalling. STATED.
4. **"A reader without the seed can search the seed space."** The
   statement is closure to a reader without the seed (Reviewer 3's word,
   03:44Z): exact for a uniformly random order; for the integer form,
   closure at the reader's means, the seed's width a declared integer (64
   bits in the script; any width the world declares). STATED.
5. **"The hash has structure (a linear congruential generator's low bits
   cycle); some statistic tells the two lists apart."** The script's
   generator is a mixing hash of SplitMix64's form (every output bit
   depends on every state bit), plain integers; a battery of five
   decoders fixed before the run (the first-quarter fraction, its
   threshold, the run count, the lag-one sameness, the halves' drift)
   over 200 seeds reads 0.47 to 0.535 right at N = 64, 256 and 2048
   (the binomial error 0.025 on 400 trials). The engine's form is the
   builder's under the requirement: a keyed permutation indistinguishable
   from uniform without its key. STATED (Reviewer 3, 04:38Z), not closed
   by declaration: a 64-bit keyed shuffle is closure to a reader with
   bounded means (2^64 keys against N! orders; the list of 2048 bits
   determines the seed information-theoretically), so the requirement is
   computational; SplitMix64's form is a mixing hash and not a
   cryptographic one; the battery is evidence for the requirement and not
   a proof; the same honest label as objection 4.
6. **"The birth-interval stamp reveals the ordinal; if u were a known
   function of the ordinal, B decodes."** u is the seed's permutation of
   the ordinal; without the seed the ordinal says nothing of u; the
   lamp's cadence of births is fixed and independent of the residues, so
   the birth-interval stamp carries nothing of u. CLOSED BY DECLARATION
   (line 5).
7. **"B's click TIME might depend on A's setting: the rotation at A's bar
   scales the record's norm by n_a / 65536."** CLOSED BY CONSTRUCTION,
   read in the engine and the algebra: nothing of one arm is written on
   the other (ALGEBRA.md 3.6, B1); the rotation at A's bar acts on A's
   arm's rows only and scales A's arm's offer, not B's; the record's norm
   is the birth's (set once at the release in the engine, `live.norm`,
   never by a table); B's first rung is B's own pointer against that
   norm; and the engine stamps a click with the chosen cell's own first
   rung (`_click`: the click's time is `live.first_rung[chosen]`), never
   with the completion tick. Line 6 declares what the engine does.
8. **"The completion tick, a host event, moves with A's setting."** The
   record completes when the motion left on the board is below a rung of
   what was absorbed, which A's rotation does change; but the completion
   tick is a HOST field of the gather line, not a reading; the DETECTOR
   reading is the cell's first rung. CLOSED BY DECLARATION (line 6).
9. **"The gather line prints the residue."** The engine's gather line as
   built carries `u` (the record's residue) beside the HOST fields `tick`
   and `arrived`: it is the books' record, Inside. The reader of record
   of the Bell rows reads the click lists per set (the cell, the count,
   the birth interval), never the gather's `u`; the gather line is
   labelled HOST wherever it appears. CLOSED BY DECLARATION (line 2, on
   the reader).
10. **"At a coarse grain the model exceeds Tsirelson (S = 3 at N = 16 and
    32)."** At every N the counts are no-signalling exact (Theorem 5), so
    at a coarse grain the model is a no-signalling box above the quantum
    bound, as a PR box is, without signalling; the declared world is N =
    2048 with S = 181 / 64 below 2 sqrt 2 (1.05 standard errors from Poh
    2015); nature's grain is bounded by row A2. The paper's S(N) sits on
    both sides of Tsirelson's bound and says so. STATED.
11. **"The uniform u is quantum equilibrium assumed, not derived."** Yes,
    a declared input of kind 1, said so; and stronger than typicality:
    the enumeration is exhaustive, one birth per residue, so the counts
    are exact rather than typical; only the ORDER is randomized. STATED.
12. **"Memory loophole: sequential dependence of outcomes."** The outcome
    of birth i is a function of (u_i, a, b) alone, with no dependence on
    earlier outcomes or settings. CLOSED.
13. **"Freedom of choice: the seed could correlate with the settings
    (superdeterminism)."** The seed is drawn independently of the
    settings (line 4). A world with the settings switched per birth by a
    second, independent seed is FUTURE: its counts are unchanged by
    derivation (each birth's cell depends on (u_i, a_i, b_i) only) and
    the order is closed identically (B's list mixes births of both a's
    without the residues). CLOSED BY DECLARATION (line 4) and FUTURE.
14. **"The four settings pairs are four worlds sharing one enumeration:
    a counterfactual definiteness no experiment has."** The counts per
    settings pair are the ladder's fractions over all residues, the same
    in any order and in any mixture of settings; the comparison with
    nature is of the counts, which the per-trial world of item 13
    reproduces by the same derivation. STATED.
15. **"Detection loophole."** Every record clicks exactly once (the ladder
    chooses one cell and deletes the offers, ALGEBRA.md 4.12); every
    birth is counted; the efficiency is 1. CLOSED.
16. **"The order channel's width equals the Bell excess (E_N = S_N / 4):
    the violation is signalling in disguise."** Signalling needs one
    party's list alone; the Bell excess needs both lists paired by the
    birth stamp. With the residue Inside the one-party lists carry
    nothing of the far setting, and the paired lists carry E_N, the
    standard Bell statistic. A reader with both lists and not the seed
    learns nothing beyond the two outcome bits per birth (u < N / 2 from
    A's outcome, the window from B's; Reviewer 3's word), neither the
    residues nor the counterfactual list. CLOSED.
17. **"Valentini: signal locality is contingent; a preparation of the
    hidden order would signal."** The model's own prediction, stated: a
    preparation that fixed the residues' order in a known way would open
    the channel, as nonequilibrium would in Bohm's theory; no such
    preparation is known in nature, and the model predicts none exists
    for a source at equilibrium (the seed drawn once, uniform). STATED.
18. **"The gather needs both settings at one step: superluminal."** The
    one non-local step is declared (POSTULATES.md section 10), the
    host's, and carries no signal; nothing Outside is superluminal; the
    same standing as the projection postulate. STATED.
19. **"Determinism, no-signalling and S > 2 contradict a theorem."** No:
    Bell's theorem excludes LOCAL determinism; nonlocal deterministic
    no-signalling models exist (Bohm's), and this is one, with bounded
    integers. CLOSED.
20. **"The exact counts need N births per world."** The pins are at N =
    2048 births per world; a shorter run reads a prefix, approximate.
    The Bell worlds must carry N births within their ticks (the lamp's
    rate against `ticks`): CHECK 2, the World Generator's, before the
    preliminary run: the shipped bell worlds carry `ticks` 300 at the
    rate [1, 1], about 300 births and not 2048; the regenerated worlds
    need `ticks` at least 2048 + the arm's transit + the completion; and
    since with more than W births the order repeats from the first
    residue (u = order[(ordinal - 1) mod W]), the preflight counts
    exactly W births per world (Reviewer 3's nit). His CHECK 1 (the seed
    form not built on main; the shipped bell worlds under the counter
    form) becomes a load-time refusal once the builder lands the keys:
    `residue_order` absent on a pair lamp is refused (DECLARATIONS.md
    section 2 item 8).
21. **"Settings that vary within one world's wheel cycle: the counts are
    no-signalling only for settings fixed over a cycle, and for varying
    settings the model signals" (the Opus referee's finding 4; Reviewer
    3's line of 06:50Z; `order_channel_sequential_pins.py`).** None of
    the twenty items above treats settings that vary within a cycle;
    this one does, in two statistics. (a) THE MARGINAL: for per-trial
    settings under the seed-set order, B's count among the births at a
    given first-party setting a is hypergeometric (W, W / 2, n) with
    mean n / 2, THE SAME DISTRIBUTION FOR EVERY a; a count that is "not
    32 of 64 with probability 0.80" is the finite-sample fluctuation of
    any random no-signalling box, not a marginal that depends on a; the
    referee's sentence "for varying settings the model signals" is
    false as a marginal claim, and the seed-set order is what makes the
    varying-settings marginal no-signalling in distribution (under the
    counter order a periodic switching of a could correlate with the
    residues, the channel of item 7 of DECLARATIONS.md section 2). (b)
    THE SEQUENTIAL STATISTIC (Reviewer 3's computation, confirmed with
    the exact overlap): two consecutive births carry two DISTINCT
    residues (a permutation, without replacement), so at a HELD setting
    a the probability that B's consecutive outcomes agree is (W / 2 - 1)
    / (W - 1), below 1 / 2, while across a SWITCH of a to a' it is (W /
    2 - 2 m / W) / (W - 1) with m = |S_a and S_a'|, so the difference is
    E / (W - 1), E the flip fraction of the pair (a, a') at that b (the
    finite-N correlation of item 7): 0.6875 / 63 = 1.09 x 10^-2 at W =
    64, 2.76 x 10^-3 at W = 256, 3.45 x 10^-4 at W = 2048 for the pair
    (0, N / 4) at b = 3 N / 8, zero at b = N / 8 (no flips); a Monte
    Carlo over 400 seeds at W = 64 reads 0.491 held against 0.501
    switched (exact 0.492 and 0.503). So B's sequential statistic
    carries A's SWITCHING PATTERN, not a's value, at order 1 / W: about
    1 / (4 d^2) = 2 x 10^6 consecutive pairs for one standard deviation
    at W = 2048, about 10^7 for a clear reading. THE MODEL'S OWN
    PREDICTION, declared as a falsifiable row for the confrontation
    register: in nature P(B_t = B_t+1) does not depend on whether A
    switched; in the model it does, by E / (W - 1); a measurement of
    the sequential agreement rate at that precision bounds the grain W
    from below, and item 17's concession is made explicit here: signal
    locality holds in the model exactly in the counts, in distribution
    for the marginal, and in the order of outcomes only to order 1 / W,
    the finite grain's own residue. (c) THE ALTERNATIVE that removes the
    signature: the residues drawn WITH replacement, one draw per birth;
    a draw, which P4 forbids, and it loses the exactness of S_N (the
    pins become statistical); THE OWNER'S CHOICE, a change of the
    declared form if taken, not the physicist's. (d) Both statements are
    true at once: the marginal blind to a; the order of B's outcomes not
    blind to whether A switched, at order 1 / W. STATED, with the
    prediction declared (Reviewer 3's word: an item STATED with its
    prediction declared has the standing of item 5, and the Bell run
    proceeds on it; every Bell world of the GO holds its settings fixed,
    four worlds, four seeds, where the theorem of item 8 is exact; S,
    the flips and the marginals stand; no pin moves).

## The six lines, DECLARED (the owner, 2026-09-24 04:18Z, record 1648; the Boss, 04:14Z on his word of 04:12Z, record 1647)

1. THE RESIDUES' ORDER: the births of the pair record take the residues
   of Z_N (one per u) in an order set by the world's seed through a
   declared integer hash (a keyed permutation indistinguishable from
   uniform without its key; the script's form a Fisher-Yates shuffle
   driven by a mixing hash), in place of the counter family's [1, 1].
2. THE STAMP AND THE READER: the click is stamped with the detector's
   count and the birth interval, never with the residue; the reader of
   record reads the click lists per set, and the gather line is HOST.
3. THE SEED: an input of kind 1, drawn once per world and INDEPENDENT
   PER WORLD (one draw per settings world, four seeds for rows 1a to 1d;
   a seed shared across a and a' would align B's lists across the
   settings, Reviewer 3's strongest attack), never read Outside (P11,
   clicks only); its width a declared integer.
4. THE SEED AND THE SETTINGS are drawn independently (no
   superdeterminism).
5. THE LAMP'S CADENCE of births is fixed and independent of the residues
   (the birth-interval stamp carries nothing of u).
6. THE CLICK'S STAMP is the cell's own first rung, never the gather's
   completion tick (as the engine's `_click` already does).

With the six lines declared, row 1c reads PASS in form Outside; the
Inside dependence E_N (`order_channel_pins.py`) is a GAMEBOARD
diagnostic and the model's declared nonlocality, said in the paper as
such; the counts and S_N are untouched; the falsifiable content of the
Bell rows is S_N against 2 sqrt 2 at the declared grain (row 1a).

THE GUARD (the Boss, 04:14Z): no run of any Bell world before this page
is on main under Reviewer 3's read with every objection in one of the
five statuses above and none OPEN; an objection Reviewer 3 marks OPEN
returns DECLARATIONS.md section 2 item 8 to PREPARED until it is closed
or stated; an item STATED with its prediction declared (item 21) has the
standing of item 5 and the run proceeds on it. The loader keys' names and
forms for the builder
(`residue_order`, `residue_seed`, the stamp's fields) stand in item 8,
in one place; this page does not repeat them.
