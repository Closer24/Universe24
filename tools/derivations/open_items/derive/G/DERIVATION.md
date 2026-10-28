# Draft G: the tie at the half, and matter against antimatter

Drafter G, 2026-10-28, on the owner's question of 12:4x UTC (translated): "Maybe the tie is what produces the asymmetry between matter and antimatter?"

Read on the head as the scratchpad worktree t24 holds it (the engine of 526a5666d/834cfd72e). No file of the repository or of any worktree is changed: every variant is installed at run time by monkeypatching, and every probe runs with `/home/user/Universe24/venv314/bin/python -I`, its output beside it in S/derive/G.

| probe | what it does | output |
| --- | --- | --- |
| g0_lane.py | the runner: one engine process per lane, each job waiting while S/check.lock exists | queue_*.txt |
| g1_ties.py | the instrumented engine: the counts S1 to S7 and the tie rules | g1_*.txt |
| g2_toy.py | the one-gear and one-hand toy, pure integers | g2_toy.txt |
| g3_u_effect.py | where nature's three ties go | g3_u_effect.txt |
| g4_pair_diff.py | how the pair world's states differ under the rules | g4_pair_diff.txt |
| g5_table.py | the table of every g1 run | g5_table.txt |
| g6_u_halfup.py | a property test against the head's own rounding functions | g6_u_halfup.txt |
| g7_antiworld.py | a world against its antiworld under one rule, with the skew struck as a diagnosis | g7_*.txt |
| g9_kseed.py | which seeds are their own antiworld | g9_kseed.txt |

This draft covers the protocol's steps 1 to 4. Steps 5 and 6 belong to other hands. Every claim is marked PROVED (with its proof), CHECKED (with its probe's count) or OPEN.

## 0. The answer in one page

| question | finding | status |
| --- | --- | --- |
| How often does the driven carry tie (S1, tick.py:266)? | 135 times in the 21 shipped worlds' 20,537,340 driven carries, all on world_pair_3, on the light's three gear, all 27 clocks at once at five ticks. On the one big bang: 0 of 208,000 in 250 ticks. | CHECKED |
| How often does the impulse's u tie (S2, tick.py:231-232, half up in p as well)? | 45 times in 41,074,680 roundings: nature 3, polarization 6, collapse_500 12, collapse_1200 24. Every one is on the light's three gear, at tick 2 or 3. On the bang: 0 of 416,000. | CHECKED |
| The matter excess per bang, under (a) half up, (b) half even, (c) half down | 0 under each. The three runs of the bang are one run bit for bit (the same state hash at every one of its 250 ticks). Its antiworld also keeps every coupled charge at 0 at all 250 ticks under (a) and (b), with the same births and chimes. | CHECKED |
| What the tie does to matter against antimatter where it acts | Isolated on polarization (the skew struck), the world-antiworld excess at tick 12 is -1,128 under (a), 0 at every tick under (b), and +1,128 under (c): exactly opposite at every tick. Within the run it is +172 at tick 7 and -1,207 at tick 11. | CHECKED |
| Is the sign systematic? | No. The tie's own part changes sign within the one run where it was isolated (+172 at tick 7, -1,207 at tick 11). On the three worlds where the tie of u moves the run, (c) lowers the world's charge each time (-13,553, -5,841, -5,949), but that sign comes through the skew: with the skew struck, polarization's (c) - (a) is +1,128 and the collapse worlds make no charge at all. In the toy the tie's sign is even over seeds (169 against 178). | CHECKED |
| What does make matter outnumber antimatter on the head | The skew (Y-S3, meshes.skewed): the regulator's flow gears turn the hands by an angle even under C and under the lattice's reflections, so it breaks C and CP. On five seeds that are their own antiworld it makes net charges (bodies +2,849, packet -9,732, emission_one +2,570, collapse_500 +7,387, collapse_1200 +2,875) which stay exactly 0 at every tick with the skew struck, ties and all. On the hole and nature, which fit pairs, a charge remains with the skew struck (41,250 and 145); the fitting's twist rule (C- and P-odd by design) is the candidate there, not struck itself. | CHECKED; the twist rule OPEN |
| Which symmetries each rule breaks | (a) and (c) break C, K and the 48's sign flips about rest, and the head's turnover, at an exact tie only. (b) keeps all of them and breaks the one-notch shift at a tie. No rule keeps both at even teeth. | PROVED |
| Reversibility | Every rule's step is exactly invertible: the rewind is 250 of 250 on the bang and 400 of 400 on pair_3 through its 135 ties. Each rule has an exact involutive time reversal about its own centre (half up has the flip w - 1 - r). The carried mirror with half up is not an involution at ties. | PROVED, CHECKED |
| Can the tie be the source with no declaration? | No. It never acts on the bang. Its direction is a sign the rule declares: down gives the exact opposite (Theorem 3, CHECKED on the engine). Where it acts, its effect is 1e-3 of the charge with no fixed sign. | PROVED, CHECKED |

## 1. Every carry with a mid rounding in the head's engine

The one act is `acts.carry(total, w, r) = ((total + r) div w, (total + r) mod w)`. A carry is a rounding at the half when the r passed in is the fixed mid tooth `mid(w) = w div 2`, rather than a carried remainder.

| site | where | the rounding | chosen at the tie | does any symmetry negate its argument? |
| --- | --- | --- | --- | --- |
| S1, the driven carry | tick.py:266, `v, fine = carry(p, w_div, mid(w_div))`: every hand, the light, the offset's four gears, the held field | v = (p + mid W) div W, fine in [0, W) | at even W, p = (k + 1/2) W goes to k + 1: half up | yes: C, K and the 48's reflections negate gears, and the turnover reverses the stride |
| S2, the impulse's u | tick.py:231-232, `rates.rounded(p + p + 1, d)`, d = 2 t X | half up in p (lemma 2) | p = (k + 1/2) t X goes to k + 1 | yes, as S1 |
| S3, the tension | meshes.py:73, `carries(n_i + n_j + 1, 2)` | the mean of the mesh's two ends, half up | n_i + n_j odd goes up | no: the even sum is symmetric in the ends, the 48 permutes the tensions without a sign, the turnover reverses the regulator with the signs [1] * 10 (hands.signs), and C and K do not act on the regulator |
| S4, the carried carries | clock.py:166 (Rule3's turn of the regulator and the ratchet), clock.py:173 (every drive), tick.py:200, 224, 229, unwind.py:61 | the remainder is kept, so nothing is chosen; it is born at mid (trains.py:78-81, clock.py:109) | nothing; the one tie-like point is the remainder at 0 at even teeth, where the turnover's mirror misses -P | the turnover's mirror |
| S5, the rest lay | assembly/setting.py:213, `carry(total, w, mid w)` | half up, at the setting only | none occurs (lemma 4) | - |
| S6, the turnover's mirror | acts.mirror via clock.reverse | r to (2 mid - r) mod W, about mid | the fine tooth 0 maps to 0: P to -P - W | it is the T |
| S7, the mesh factor and the rates | rule3.py:61 `carry(G^2 (Gamma - t)^2, Gamma^2, half(Gamma^2))`; rates.py's table | half up of a positive quantity | none occurs (lemma 4); the rates' table is certified | no: positive arguments |

Every reader of a carry that is not the state's (draw.py's digits, the reckoner) is left out.

## 2. How often an exact tie occurs

**Lemma 2 (S2 is half up). PROVED.** rates.rounded(n, T) = (2n + T) div 2T for n >= 0 and (2n + T - 1) div 2T for n < 0. With n = 2p + 1 and T = d = 2 t X, where t X is even because t = 6 rim Gamma^2 G^2 is even:
- for p >= 0, the even numerator 2p + tX plus 1 crosses no multiple of the even 2tX;
- for p < 0, the numerator 4p + 2tX is a multiple of 4, so 4p + 2tX plus 1 crosses no multiple of 4tX.

So u = (p + tX div 2) div tX at every p. Then u(-1 - p) = -u(p) everywhere, and u(-p) = -u(p) fails exactly at p = tX/2 (mod tX).

CHECKED (g6): 100,000 of 100,000, with u(-p) = -u(p) failing at exactly the 20,000 ties among them and at none of the other 80,000. The driven carry is the same rounding at its own teeth (100,000 of 100,000).

**Lemma 3 (S2 against S1). PROVED.** In a tick whose regulator notches are equal (X before = X now = X), the mean teeth are w = tX, and P = w (n - b) + r - w/2 = r - w/2 (mod w). So:
- u_in ties exactly where r = 0, which only an S1 tie leaves;
- u_out ties where p = tX/2 (mod tX), the S1 tie when the end teeth are tX too.

An S2 tie without an S1 tie therefore needs the stretch to move within the tick. All 45 do: they fall at ticks 2 and 3, as the stretch leaves the full rate. Nature's 3 are at p = -313.5 tX; the 33 on the middle calibre are at p = 187.5 tX, sent up to 188.

**Lemma 4 (S5 and S7 never tie). PROVED.**
- S5: at the setting every driven gear's teeth are w = tX with X = Gamma, so w div rim = 6 Gamma^3 G^2. The tie reads rim = 2N (mod 2 rim), which needs rim even; every shipped den is odd (15162856759112389 and 1655909141).
- S7: a tie needs G^2 m^2 = Gamma^2/2 (mod Gamma^2). At Gamma = 1000 and G = 16 (every shipped calibre), every number of that class has 2-adic valuation exactly 5, while 256 m^2 is 0 or has valuation at least 8.

**The counts. CHECKED** (g5_table.txt; the head's rule):

| world (ticks) | S1 driven carries | S1 ties | S2 ties | S3 live ties | S4 at 0 | S6 | coupled charge, tick 0 to the end |
| --- | --- | --- | --- | --- | --- | --- | --- |
| bang (250) | 208,000 | 0 | 0 | 0 | 0 | 0 | 0 to 0 |
| hole (60) | 90,000 | 0 | 0 | 5,888 | 0 | 0 | 0 to -29,746 |
| nature (60) | 90,000 | 0 | 3 | 11,250 | 0 | 0 | 0 to 201 |
| pair_3 (400) | 129,600 | 135 | 0 | 0 | 0 | 0 | 0 to 0 |
| polarization (12) | 15,000 | 0 | 6 | 2,214 | 0 | 0 | 2,991,059 to 1,434,606 |
| collapse_500 (600) | 4,374,000 | 0 | 12 | 754,788 | 0 | 0 | 0 to 7,387 |
| collapse_800 (600) | 4,374,000 | 0 | 0 | 557,760 | 0 | 0 | 0 to -11,304 |
| collapse_1200 (600) | 4,374,000 | 0 | 24 | 407,796 | 0 | 0 | 0 to 2,875 |
| packet (150) | 1,093,500 | 0 | 0 | 130,128 | 0 | 0 | 0 to -9,732 |
| emission (300) | 1,029,000 | 0 | 0 | 63,948 | 0 | 0 | 0 to 2,919 |
| emission_one (300) | 1,029,000 | 0 | 0 | 97,560 | 0 | 0 | 0 to 2,570 |
| emission_none (300) | 1,029,000 | 0 | 0 | 0 | 0 | 0 | 0 to 0 |
| bodies (120) | 411,600 | 0 | 0 | 34,204 | 0 | 0 | 0 to 2,849 |
| plasma (400) | 600,000 | 0 | 0 | 0 | 0 | 0 | 28,000 to -321,875 |
| universe (400) | 600,000 | 0 | 0 | 0 | 0 | 0 | 0 to 2,750 |
| sea (400) | 600,000 | 0 | 0 | 0 | 0 | 0 | 0 to 0 |
| plasma_3 (400) | 129,600 | 0 | 0 | 0 | 0 | 0 | 6,048 to -69,525 |
| universe_3 (400) | 129,600 | 0 | 0 | 0 | 0 | 0 | 0 to 594 |
| sea_3 (240) | 77,760 | 0 | 0 | 0 | 0 | 0 | 0 to 0 |
| ga2 (230) | 147,200 | 0 | 0 | 128 | 0 | 0 | 0 to 0 |
| node (20) | 6,480 | 0 | 0 | 838 | 0 | 0 | 0 to 0 |

Notes on the table:
- The bang runs the plan's 250 ticks (section 23); every other world runs its own intervals.
- "S4 at 0" counts the regulator's turn and every drive. The ratchet's pawl bit is left out, being its two-teeth state and no remainder.
- S6 counts the turned driven gears whose fine tooth stood at 0, where the head's mirror misses -P.
- The S3 ties are frequent and harmless: no symmetry negates a tension (section 1).

**Why so few. PROVED for the structure, CHECKED for the counts.**
- At unstructured strides, an exact S1 tie needs p = W/2 (mod W), with W = (t div 2)(X + X') of order 1e28 on the toy and bang calibres and 1e21 on the middle calibre. That is a coincidence of order 1/W per carry, against 2e7 carries in all.
- Every tie seen is structural instead. The light's stride is an exact multiple of its old teeth: the sea lays a drift of whole notches with the fine tooth at mid. When the stretch moves, that stride is divided by new teeth whose ratio to the old is a ratio of small integers (sums of stretch notches near 1,000 to 6,000).
- On pair_3 the board is uniform and the light feels no pull, so p / W = v s / s', a half-integer at five ticks at all 27 clocks together. The S2 ties are the same mechanism at ticks 2 and 3.

## 3. The three rules on the shipped worlds

The rules, installed at S1 and S2 (g1_ties.py, `rule` and `urule`):
- (a) half up, the head's;
- (b) the exact tie to the even quotient (Animate's candidate);
- (c) half down.

Under (b) and (c) the fine tooth may stand at W, so the unwind's move reads it modulo its teeth: the head's move exactly wherever the fine tooth is below W. The turnover was run with the head's mirror and with an exact one (the stride reversed exactly and carried again under the rule in force).

A world with no tie gives one run under all three rules. PROVED: every patched function returns the head's integers at every call that is not a tie. 16 of the 21 worlds have no tie.

**3.1 The one big bang (250 ticks). CHECKED** (g1_bang250_*.txt):
- (a), (b) and (c), each with either mirror, give one run: the final hash is 0df326f55507... in all six, the per-tick digest is the same, and the rewind is 250 of 250 in all.
- Per bang, and in total:
  - the great clock turns over 50 times;
  - 64 pairs are fitted, at ticks 6 and 7, of hands 1 and 2, one + and one - each;
  - there are 0 unspringings;
  - the coupled charge SUM c_T Q_T is 0 at every one of the 250 ticks, and Q* is 0 per coupled hand at the end;
  - the chimes are +7,584/-7,584 (hand 1) and +6,784/-6,784 (hand 2), balanced in every tick;
  - the reckoner's row 68 reads 32/32, and row 70 reads 64 of 64.
- **The matter excess per bang is 0 under each rule.**

**3.2 pair_3: 135 ties on the light. CHECKED** (g1_pair3_400_*.txt, g4_pair_diff.txt):
- The three rules give three states (hashes b1a09c..., 688f45... and 8c4d9e...), yet every reading is equal at every tick: the stretch, the 54 turns, the 297 chimes of sense 0, and the coupled charge 0.
- The difference is the light's three gear alone, by one notch at all 27 clocks at once. Under (c) its notch is -1 at tick 29 (fine tooth +W, the same stride), -3 by tick 100 and -5 by tick 400, one per tie event. Under (b) it is -2 by tick 400.
- A common translation changes no difference and no n - b, so nothing reads it.
- The rewind is 400 of 400 under each rule, with either mirror.

**3.3 Nature: 3 ties of u, wiped. CHECKED** (g1_nature60_*.txt, g3_u_effect.txt):
- Sent down, the ties do change the forms (-216,479 to -217,000 at the first clock), the time gear's drive (not clamped) and the stress.
- But all three clocks turn over at tick 3, and the turnover returns them to their reversed pre-state. So all 60 ticks are the same bit for bit, under every combination of the rules at S1 and S2.

**3.4 Polarization: 6 ties of u. CHECKED** (g1_polar12_*.txt):
- Under (b) the ties round to 188, already even, so (b) is (a) bit for bit.
- Under (c) they round to 187. The run parts at tick 6 (the stretch), and two balanced pairs of hand 0 are fitted at tick 8.
- At tick 12:

  | reading | (a) and (b) | (c) |
  | --- | --- | --- |
  | coupled charge | 1,434,606 | 1,421,053 |
  | coupled Q* | -988,899 | -270,083 |

- The rewind is 12 of 12 under each.

**3.5 Collapse_500 and collapse_1200: 12 and 24 ties of u. CHECKED** (g1_collapse{500,1200}_*.txt):
- Under (b) the ties round to 188 again, so (b) is (a).
- Under (c), collapse_500's coupled charge ends at 1,546 against 7,387, and collapse_1200's at -3,074 against 2,875.
- The rewind is 20 of 20 under each.
- So on all three worlds where the tie of u moves the run, (c) - (a) in the world's coupled charge is negative: -13,553, -5,841, -5,949. It is one structural event each time: the light's u at 187.5 tX as the stretch first rises, on the middle calibre. Section 3.7 shows that the sign comes through the skew.

**3.6 Every other excess comes with no tie. CHECKED.** Hole, nature, packet, bodies, the emission worlds, collapse_800, plasma and universe meet no tie that moves them. Hole and nature are one run, bit for bit, under (a), (b) and (c), and so are their unspringings by sign and their chimes. These worlds still end with charges: hole -29,746, nature +201, packet -9,732, universe +2,750.

**3.7 The world against its antiworld. CHECKED** (g7_*.txt).
- The operational form of the owner's question compares a world with its charge conjugate under one rule.
- The antiworld is the seed under C = -K applied to the clock after the setting: every hand's three gear is negated, and its fine tooth and drive fine tooth are reflected about mid (r to w - r, so P goes to -P exactly).
- This is the engine's C:
  - it exchanges the fitted pair, (A, iB) and (-A, iB);
  - the release's push on the light's three gear is odd under it;
  - the meshes' turns are covariant under it once the offset train's angle flips (it is driven by the C-odd sweep and lead);
  - it negates the charge W.
- The asymmetry is A = Q(world) + Q(antiworld): it is 0 at every tick exactly when the pair is C-symmetric.
- If the head were C-covariant apart from the tie, Theorems 2 and 3 would give A_b = 0 and A_c = -A_a.

Results:
- **The bang.** Under (a) and under (b) the world and its antiworld both keep every coupled charge at 0 at all 250 ticks, with the same births (32 of hand 2 at tick 6, 32 of hand 1 at tick 7) and the same chimes. So the one big bang makes no excess of either. (Only the charges, births and chimes were compared, and the charges are 0 in both.)
- **Seeds that are their own antiworld.** g9_kseed.txt classifies them: on 14 of the 21 worlds every twelve gear stands at (0, 0, mid), so K leaves the seed unchanged (bodies, the three collapse worlds, the three emission worlds, hole, nature, node, packet, pair_3, sea, sea_3).
  - There any net charge is an excess that the dynamics alone makes. Nine of them make one: bodies +2,849, collapse_500 +7,387, collapse_800 -11,304, collapse_1200 +2,875, emission +2,919, emission_one +2,570, hole -29,746, nature +201, packet -9,732. That is 6 positive and 3 negative.
  - Their only ties are on the light's three gear, which K does not touch.
- **The skew is the source on those seeds.** With the skew struck (meshes.skewed made the identity in both runs, a diagnosis only), the coupled charge stays exactly 0 at every tick on bodies (120), packet (150), emission_one (300), collapse_500 (600) and collapse_1200 (600). The two collapse worlds keep their ties of u with the skew struck (12 at tick 3 and 24 at tick 2, the same strides; g1_world_collapse_500_4_noskew.txt, g1_world_collapse_1200_3_noskew.txt) and still make nothing.
  - With the skew, bodies' charge runs -481 (tick 10), -11,321 (20), -1,869 (40), +2,032 (60), +2,849 (120).
  - Hole and nature, which fit pairs, still make a charge with the skew struck under (b) (41,250 and 145). The candidate there is the fitting's twist rule, even under C by design; it was not struck here.
- **Polarization**, whose matter has a sense (not its own antiworld):

  | rule | A with the skew | A with the skew struck |
  | --- | --- | --- |
  | (a) | +16,816 | -1,128 |
  | (b) | +2,544 | 0 at every tick |
  | (c) | -11,009 | +1,128 |

  With the skew struck, (c) is exactly -(a) at every tick, and (a) on the antiworld is exactly the negative of (c) on the world at all 12 ticks (Theorem 3 on the engine). The tie's own part runs 0 through tick 6, then +172, +140, +140, +188, -1,207, -1,128. So it is about 1e-3 of the charge (1.43 million), flips with the rule, and changes sign within the run.
- **Theorem 3 on the engine with the skew.** On collapse_500 (its own antiworld, so -K x0 is its global negation, under which the skew is covariant), (a) on the image equals (c) on the seed at all 600 ticks, and (c) on the image equals (a) on the seed at all 600. Under (b) the image equals the world at 600 of 600.
  - On collapse_1200 the image parts from the world at tick 21 under all three rules alike. That break of the global negation is not the tie's. The release's push on the light is even under the global negation while the light's notch is odd; under -K it is covariant (OPEN: traced to no single act).

## 4. The symmetries each rule breaks

**The model.** One driven gear (b, n, r) at fixed even teeth W, mid = W/2, stride P = W (n - b) + r - mid. One tick: p = P + F(n), v = q(p), (b, n, r) to (n, n + v, p - W v + mid). This is tick.py's impulse and driven carry, with F odd (F(-n) = -F(n)): Rule3's pull is linear in the notches, and the meshes' turns round oddly.

The rules:
- q_u(p) = (p + W/2) div W, half up, r in [0, W);
- q_d(p) = (p + W/2 - 1) div W, half down, r in [1, W];
- q_e, the even one of the two at a tie and q_u elsewhere, r in [0, W] (0 and W only at an even v).

**Lemma 1 (the centre of a rule). PROVED.**
- (i) q_u(-1 - p) = -q_u(p); q_d(1 - p) = -q_d(p); q_e(-p) = -q_e(p).
- (ii) q_u and q_d keep the one-notch shift, q(p + W) = q(p) + 1. q_e keeps it except at a tie, where it moves by 0 or 2.
- (iii) q_d(p) = -q_u(-p).

Call c the centre: -1/2 for up, 0 for even, +1/2 for down.

Proof.
- (i) for up: -q_u(p) = ceil((-p - W/2) / W) = (-1 - p + W/2) div W = q_u(-1 - p).
- (iii): -q_u(-p) = ceil((p - W/2) / W) = (p + W/2 - 1) div W.
- (i) for down: q_d(1 - p) = -q_u(p - 1) = -q_d(p).
- (i) for even: off a tie no boundary lies between -1 - p and -p. At a tie the two candidate pairs have even members that are negatives of each other.
- (ii): read off the definitions.

**Theorem 1 (the no-go at even teeth). PROVED.** No nearest-integer rounding of p / W is both odd about rest and shift-equivariant. Proof: q(W/2) = q(-W/2) + 1 = 1 - q(W/2), so 2 q(W/2) = 1. At odd W no tie exists and q_u is both.

CHECKED (g2 part 3, p in [-60, 60]):
- at w = 8, 10, 12, 14, up and down fail oddness at 16, 12, 10 and 8 points and the shift at none;
- even fails the shift at 16, 12, 10 and 8 and oddness at none;
- at odd w nothing fails.

**Theorem 2 (each rule's exact conjugation and time reversal). PROVED.** Let r* = 2 mid + 2c - r: W - 1 - r for up (the head's former flip, acts.flip), W - r for even, W + 1 - r for down. Then:
- (a) C_c: (b, n, r) to (-b, -n, r*) commutes with the tick;
- (b) T_c: (b, n, r) to (n, b, r*) is an involution with T_c S T_c = S^-1, so the orbit after T_c retraces the orbit before it at every state;
- (c) C_c and T_c fix rest, and send P to -P, only for c = 0.

Proof.
- Both maps send P to 2c - P and keep r* in the rule's range.
- (a): from C_c x, p' = 2c - p, so v' = -v by Lemma 1 (i), and the new state is C_c S x.
- (b): T_c applied twice is the identity. For x with stride P, the previous state is (b - v_, b, r_) with P_ = P - F(b) and v_ = q(P_). From T_c x, p' = 2c - P_, so v' = -v_, and T_c S T_c x = (b - v_, b, r_) = S^-1 x.
- (c): r* = mid exactly when c = 0.

CHECKED (g2 part 1, every canonical state with notches in [-7, 7], F = -3n):

| rule | the map about its own centre | the head's mirror |
| --- | --- | --- |
| up | C_flip and T_flip: 0 failures of commuting, involution, retrace and T S T = S^-1, and no image hit twice | at w = 8: C fails at 420 of 1,800 states, the retrace at 420, and 8 images are hit twice |
| even | C_raw and T_raw: 0 failures | - |
| down | C_up1 and T_up1: 0 failures | - |

**Corollary (where the head's turnover misses). PROVED.** The head carries about -1/2 (S1 and S2, lemma 2) and turns over about 0 (the mirror). They part exactly at the tie, where the mirror sends P to -P - W (Animate's parity.txt). The former flip was the exact reversor of the head's carry, and it moved a gear at rest: by Theorem 1, a shift-equivariant rule's reversor cannot fix rest.

**Theorem 3 (the two asymmetric rules are each other's conjugates). PROVED.** C_0 (notches negated, r to W - r unreduced) maps the half-up states [0, W) onto the half-down states (0, W], and S_down = C_0 S_up C_0. So (c) on a seed is (a) on the negated seed, for every reading.

The same holds on the engine for the conjugation -K wherever the rest of the step commutes with it. CHECKED:
- toy: 400 of 400 seeds at every w;
- engine: polarization with the skew struck, 12 of 12 ticks; collapse_500, 600 of 600.

So (c) = -(a) holds on a pair of seeds only when the pair is C-symmetric. On single seeds in the toy it held on 74 to 230 of 400.

**Theorem 4 (half even keeps K). PROVED.** For a hand of two gears, K_0 (the twelve gear negated about mid) commutes with the tick under (b) (Theorem 2 (a) at c = 0), and the charge is odd under it, so a pair (A, K_0 A) keeps net charge 0 at every tick. CHECKED: 400 of 400 seeds, 400 ticks each, at every w.

**The sign of the tie's charge. CHECKED** (g2 part 2: 400 random K-symmetric pairs per w, 400 ticks, F = -(2w - 2K) n):

| w | seeds whose net charge leaves 0 | sign of the first nonzero net (- / +) |
| --- | --- | --- |
| 8 | 333 | 174 / 159 |
| 12 | 201 | 90 / 111 |
| 16 | 347 | 169 / 178 |
| 20 | 186 | 103 / 83 |

The tie always rounds up, but a +1 on the twelve notch changes the charge by -b3, whose sign the orbit's phase sets. At w = 10 and 14 no seed ties: even forces from seeds at mid keep P even, and W/2 is odd there.

**The skew breaks C and CP. PROVED from its spelling, CHECKED by striking it.**
- meshes.skewed turns each hand at a mesh by the tangent triple of m = 3 K odd_sum(V_a, spoke), with V the regulator's flow gears. The flow gears are driven by the pushes and the stress, which are even under C, so the angle is even under C.
- A turn R_m of a hand commutes with the conjugation only if m flips. So the skew breaks C (and K).
- Under a reflection of the axis a, V_a flips with the spoke's side, so odd_sum is even: the angle is P-even. The skew therefore breaks CP.
- Its T character is OPEN.
- The fitting's twist rule is the other C-breaking: the + end is chosen by the lead and the twist, both even under C. It breaks C and P and keeps CP (draft A's F1).

**The symmetries, rule by rule. PROVED** ("about rest": the maps that fix P = 0):

| symmetry about rest | (a) half up | (b) half even | (c) half down |
| --- | --- | --- | --- |
| C (-K: every hand's three gear negated) and K | broken at a tie of a negated gear | kept | broken at a tie: (a)'s conjugate (Theorem 3) |
| P, the 48: clocks permuted, and the reflections negate the axis gears (the offset's odd gears, the regulator's flows) | permutations exact; broken at a tie of a gear the image negates | kept | as (a) |
| T, the turnover's mirror | broken at a tie (P to -P - W) | kept with the mirror unreduced | broken at a tie |
| CP and CPT | broken where an odd number of the factors negates a tied gear | kept | as (a) |
| the one-notch shift (an advance or a move of whole notches) | kept | broken at a tie | kept |
| C, P and T about the rule's own centre | all exact (the flip) | the same maps as above | all exact (W + 1 - r) |

Every breaking is local to an exact tie. The skew and the twist rule break C apart from any rule.

## 5. Reversibility

1. **Every rule's step is exactly invertible. PROVED and CHECKED.** The carry keeps its remainder, and the step back carries the stride again under the same q. Rewinds:
   - the bang: 250 of 250 under (a), (b) and (c), with either mirror;
   - pair_3: 400 of 400 under each, through its 135 ties;
   - polarization: 12 of 12;
   - hole, nature and the collapse worlds: 20 of 20.
2. **An asymmetric rule can be exactly reversible. PROVED** (Theorem 2 (b)). Half up is reversed exactly by the flip: an involution, with T S T = S^-1 and the retrace at every state, and the log-free M (turnover at the top, step elsewhere) hits no image twice. Its asymmetry is the centre of its reversor, half a fine tooth below rest.
3. **The carried mirror with half up. PROVED and CHECKED.** As T(a, P) = (a - q(P), -P):
   - T S T = S^-1 holds for any q (0 failures);
   - T T (a, P) = (a - q(P) - q(-P), P), so at a tie it moves both slots by a notch: 225 of 1,800 states at w = 8;
   - the retrace fails at 224;
   - M hits 12 images twice (13, 11 and 13 at w = 10, 12, 14).

   So it does not make half up time-symmetric. With half even it is the unreduced mirror and exact.
4. **The images hit twice at the turnover. CHECKED** (the toy's log-free M):

   | rule and turnover map | images hit twice at w = 8, 10, 12, 14 |
   | --- | --- |
   | up with the head's mirror | 8, 9, 8, 10 |
   | up with the flip | 0 |
   | even with the unreduced mirror | 0 |
   | down with W + 1 - r | 0 |
   | up with the carried mirror | 12, 13, 11, 13 |

   On the engine no turned gear stood at the tie point on any run (S6 = 0), so the head's turnover was the exact P to -P on every gear it turned.
5. **The cost of (b). PROVED and CHECKED.** By Theorem 1, an odd advance of whole notches on a gear at a tie leaves (b) a state that is not its own carry: 678 per box in g2 part 3, and 0 under (a) and (c). So under (b) the release's advance, the unwind's move and the fitted hands' advances must carry the stride again at a tie. On the shipped runs it never bit: pair_3's (b) rewinds 400 of 400.

## 6. Sakharov, and CP violation in nature

Sakharov (JETP Lett. 5, 24 (1967); Pis'ma ZhETF 5, 32; repr. Sov. Phys. Usp. 34, 392 (1991)) named three conditions for a baryon excess from a symmetric start:
1. baryon-number violation;
2. C and CP violation;
3. departure from thermal equilibrium.

CP violation was seen in K_L to two pions (Christenson, Cronin, Fitch and Turlay, Phys. Rev. Lett. 13, 138 (1964)). Kobayashi and Maskawa (Prog. Theor. Phys. 49, 652 (1973)) placed it in one complex phase of the quark mixing matrix, which needs three generations: a constant of the law, acting in every weak process with one sign. The observed eta = n_B / n_gamma is about 6.1e-10 (Planck 2018 with BBN). The KM phase's strength at the electroweak scale (the Jarlskog invariant suppressed by the quark masses, of order 1e-20 in dimensionless form) is far too small for it, so baryogenesis is held to need CP violation beyond the KM phase.

On the head:
- **Condition 1 is met, but not by the tie. CHECKED.** The coupled charge is not kept by the step (draft A's verifier, V1), and it moves identically under (a), (b) and (c).
- **Condition 2 is met by the skew, apart from the tie. CHECKED.**
  - The skew is a constant coupling of the law (Y-S3), even under C and P, so CP-odd, much as the KM phase is a constant CP-odd coupling.
  - It makes net charges from seeds that are their own antiworld, and with it struck those charges are exactly 0.
  - Unlike the KM phase's asymmetries, its charge has no fixed sign: 6 worlds positive and 3 negative, and on bodies a change of sign within the run.
  - The tie adds a C-breaking only at an exact tie. Every tie seen falls on the light's three gear. Polarization is the one world whose matter is not its own antiworld, and there the tie's part is 1e-3 of the charge, with no fixed sign.
- **Condition 3 holds trivially in a reversible map. PROVED.**
  - If U commutes with S, U x0 = x0 and B U = -B, then B(S^t x0) = B(U S^t x0) = -B(S^t x0), so B = 0 at every t. This is why C and CP must break.
  - If R is an involutive reversor (R S R = S^-1) with R x0 = x0 and B R = -B, then only B(x_-t) = -B(x_t) follows.
  - So a single coherent seed is "out of equilibrium" by itself.
  - On the bang the coupled charge is 0 at every tick in the world and in its antiworld: whatever the skew and the twist do there cancels over the board (not traced further).

## 7. Can the tie be the source with no declaration?

**No. PROVED for the structure; CHECKED on the shipped worlds.**

1. **On the one big bang the tie never occurs.** 0 of 208,000 driven carries and 0 of 416,000 impulse roundings in 250 ticks. (a), (b) and (c) are one run, and the excess per bang is 0 under each, in the world and in its antiworld.
2. **Where it acts, the tie's matter-against-antimatter part is small and has no fixed sign.** Isolated on polarization (the skew struck), it is exactly -1,128 under (a), 0 under (b) and +1,128 under (c) at tick 12: the flip between (a) and (c), with none under (b), that Theorem 3 predicts. But it is +172 at tick 7 and -1,207 at tick 11, one part in a thousand of the charge. On seeds that are their own antiworld, the ties fall on the light's three gear, which K does not touch, and with the skew struck those worlds make no charge at all, ties and all.
3. **Its direction is a declaration.** Half up and half down are each other's conjugates (Theorem 3, CHECKED on the engine), so choosing up declares a sign exactly as typing one would; it is the same kind of declaration as draft A's one-hand sign. Theorem 1 forces every rule at the half to break either the conjugation about rest or the one-notch shift at even teeth. The tie's asymmetry is therefore the price of even teeth, and its sign is the rule's choice, not something the board derives.
4. **What does make matter outnumber antimatter on the head is the skew** (and, where pairs are fitted, the twist rule). Neither is the tie, and neither gives a sign of its own across the worlds.

## 8. OPEN

- The skew's character under T, and whether the new engine keeps it (it is the head's one CP-odd coupling found here).
- What breaks the global negation on collapse_1200 at tick 21 under every rule (the release's push on the light is the candidate), and on the hole with the skew struck at tick 37.
- Whether the fitting's twist rule makes the hole's and nature's charges with the skew struck (41,250 and 145): a run with both struck would tell.
- Why the light's tie of u, sent down, lowers the world's charge on all three middle-calibre worlds while the skew acts (and raises it by 1,128 on polarization with the skew struck).
- Whether a world laid so that a matter hand's twelve gear ties structurally would show a sign that survives many ties. The toy's K pair says no; no shipped world ties on a matter hand.
- T S T = S^-1 for the whole engine at any teeth count (the plan's item for David). By Theorem 2 the carry and the turnover must share one centre: up with the flip, even with the unreduced mirror and re-carried advances, or down with W + 1 - r.

## 9. The runs and their files

- g1 outputs:
  - g1_bang250_{head, up, even, down, even_exact, down_exact, head_exact}.txt;
  - g1_hole60_{head, up, even, down}.txt;
  - g1_nature60_{head, even, down, head_u, head_ueven, head_udown, even_ueven, down_udown}.txt;
  - g1_pair3_400_{head, up, even, down, even_exact, down_exact}.txt;
  - g1_polar12_{head, head_ueven, head_udown}.txt;
  - g1_collapse{500, 1200}_{head, ueven, udown}.txt;
  - g1_count_*.txt (every world at its own intervals).
- g1_first_bang250_head.txt and g1_first_hole60_head.txt are the first two runs, before the digest was added.
- g7 outputs (world against antiworld):
  - g7_bang250_{a, b}.txt;
  - g7_hole60_{a, b, b_noskew}.txt;
  - g7_nature60_{a, b_noskew}.txt;
  - g7_pair3_400_a.txt;
  - g7_polar12_{a, b, c, a_three, b_three, c_three, a_noskew, b_noskew, c_noskew}.txt;
  - g7_collapse{500, 1200}_{a, b, c, a_noskew}.txt;
  - g7_bodies120_{a, a_noskew}.txt;
  - g7_packet150_a_noskew.txt;
  - g7_emission_one300_a_noskew.txt.
- g1_world_collapse_500_4_noskew.txt and g1_world_collapse_1200_3_noskew.txt: the ties of u counted with the skew struck.
- The queues' logs: queue_*.txt; the job lists: jobs_*.txt.
